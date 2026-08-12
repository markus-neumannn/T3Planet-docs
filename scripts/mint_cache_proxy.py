#!/usr/bin/env python3
"""Local caching reverse proxy in front of mint dev.

Mintlify `mint dev` recompiles MDX/RSC on every request (often 6–12s). Live RTD
serves prebuilt HTML in <1s. This proxy caches successful HTML + RSC + static
responses so repeat views and SPA hops hit memory cache (~instant).

Usage:
  1. mint dev on :3001  (or set MINT_ORIGIN)
  2. python3 scripts/mint_cache_proxy.py   # listens on :3000

Browse http://127.0.0.1:3000 — first hit warms, next hits are cached.
On startup, critical hub routes are warmed in the background.
"""
from __future__ import annotations

import hashlib
import os
import sys
import threading
import time
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

LISTEN_HOST = os.environ.get("PROXY_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("PROXY_PORT", "3000"))
MINT_ORIGIN = os.environ.get("MINT_ORIGIN", "http://127.0.0.1:3001")
CACHE_TTL_SEC = int(os.environ.get("CACHE_TTL", "14400"))
MAX_BODY = int(os.environ.get("CACHE_MAX_BODY", str(5 * 1024 * 1024)))
WARM_PATHS = [
    p.strip()
    for p in os.environ.get(
        "WARM_PATHS",
        ",".join(
            [
                "/",
                "/ExtNsT3AF/Index",
                "/ExtNsT3AF/Introduction/Index",
                "/ExtNsT3AF/Installation/Index",
                "/ExtNsT3AF/Configuration/Index",
                "/ExtNsT3AF/Configuration/Dashboard/Index",
                "/ExtNsT3AF/Configuration/AIProviders/Index",
                "/AllExtensions/Index",
                "/AllTemplates/Index",
                "/AIFoundationExtensions/Index",
                "/License/Index",
                "/License/ExtendTrial/Index",
                "/License/GenerateLicenseKey/Index",
                "/ExtThemes/Index",
                "/EXTKarma/Index",
                "/ExtNsT3AI/Index",
                "/ExtNsT3AA/Index",
                "/ExtNsT3AC/Index",
                "/ExtNsT3AS/Index",
                "/ExtNsT3AL/Index",
                "/ExtNsT3AB/Index",
                "/ExtRTECKEditorPack/Index",
                "/ExtNsRevolutionSlider/Index",
                "/EXTAvatar/Index",
                "/EXTBootstrap/Index",
            ]
        ),
    ).split(",")
    if p.strip()
]

_cache: dict[str, tuple[float, int, list[tuple[str, str]], bytes]] = {}
_lock = threading.Lock()
_stats = {"hits": 0, "misses": 0, "bypass": 0, "rejected_incomplete": 0}
_conn_local = threading.local()
# mint dev wedges under parallel MDX/RSC compiles; serialize upstream.
_upstream_gate = threading.Semaphore(int(os.environ.get("MINT_UPSTREAM_CONCURRENCY", "1")))


def _origin_parts():
    u = urlsplit(MINT_ORIGIN)
    return u.hostname or "127.0.0.1", u.port or 80


def _get_conn() -> HTTPConnection:
    """Reuse one keep-alive connection per worker thread."""
    host, port = _origin_parts()
    conn = getattr(_conn_local, "conn", None)
    if conn is None:
        conn = HTTPConnection(host, port, timeout=180)
        _conn_local.conn = conn
    return conn


def _reset_conn() -> None:
    conn = getattr(_conn_local, "conn", None)
    if conn is not None:
        try:
            conn.close()
        except Exception:
            pass
        _conn_local.conn = None



def _complete_enough(path: str, status: int, content_type: str, body: bytes) -> bool:
    """Reject caching truncated/error shells that freeze the UI on skeleton forever.

    Mintlify full HTML docs are typically 500KB–900KB and include a <title>.
    A ~100KB body without title/`self.__next_f` is an incomplete flight payload.
    """
    if status != 200 or not body:
        return False
    ct = (content_type or "").lower()
    # RSC payloads are smaller; still require non-empty
    if "_rsc=" in path or "&_rsc=" in path:
        return len(body) >= 64
    if "text/html" not in ct:
        return True
    # Incomplete HTML shell — never cache (serves blank/skeleton forever as HIT)
    if len(body) < 200_000:
        # Allow tiny legitimate pages only if they have a real title + next markers
        low = body[:8000].lower()
        if b"<title" not in low:
            return False
        if b"self.__next_f" not in body and b"__next_data__" not in low:
            # Mintlify App Router uses flight; require substantial body
            if len(body) < 350_000:
                return False
    # Always require a title for HTML documents
    if b"<title" not in body[:12000].lower() and b"<title" not in body.lower()[:50000]:
        return False
    return True


def _cacheable(method: str, path: str, status: int, content_type: str) -> bool:
    if method != "GET" or status != 200:
        return False
    if path.startswith("/_next/webpack") or "hot-update" in path:
        return False
    ct = (content_type or "").lower()
    if "_rsc=" in path or "&_rsc=" in path:
        return True
    if "text/html" in ct:
        return True
    # Next.js RSC / Flight payloads
    if "text/x-component" in ct:
        return True
    if path.startswith("/_next/static/") or path.startswith("/_static/"):
        return True
    if path.endswith(
        (
            ".css",
            ".js",
            ".svg",
            ".webp",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".woff",
            ".woff2",
            ".ttf",
            ".ico",
        )
    ):
        return True
    return False


def _browser_cache_control(path: str, content_type: str) -> str:
    """Mint sends no-store; replace with browser-friendly TTLs on cached hits."""
    ct = (content_type or "").lower()
    if path.startswith("/_next/static/") or path.startswith("/_static/"):
        return "public, max-age=31536000, immutable"
    if path.endswith((".woff2", ".woff", ".ttf")):
        return "public, max-age=31536000, immutable"
    if path.endswith((".css", ".js")):
        return "public, max-age=86400"
    if path.endswith((".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico")):
        return "public, max-age=604800"
    if "text/html" in ct:
        # Never let the browser keep a bad HTML document (stuck skeleton).
        # Proxy memory cache still serves sub-ms HITs.
        return "no-store"
    if "_rsc=" in path:
        return "no-store"
    return "public, max-age=300"


def _key(method: str, path: str) -> str:
    return hashlib.sha1(f"{method}:{path}".encode()).hexdigest()


def _content_type(headers: list[tuple[str, str]]) -> str:
    for k, v in headers:
        if k.lower() == "content-type":
            return v
    return ""


def _send_cached(
    handler: BaseHTTPRequestHandler,
    status: int,
    headers: list[tuple[str, str]],
    body: bytes,
    path: str,
    tag: str,
    expires: float | None = None,
) -> None:
    ct = _content_type(headers)
    handler.send_response(status)
    for k, v in headers:
        lk = k.lower()
        if lk in ("transfer-encoding", "connection", "content-length", "cache-control", "age"):
            continue
        handler.send_header(k, v)
    handler.send_header("Cache-Control", _browser_cache_control(path, ct))
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("X-T3-Cache", tag)
    # Age on HTML HIT only (optional skip for STORE / non-HTML)
    if tag == "HIT" and "text/html" in (ct or "").lower() and expires is not None:
        age = max(0, int(CACHE_TTL_SEC - (expires - time.time())))
        handler.send_header("Age", str(age))
    handler.end_headers()
    if handler.command != "HEAD":
        handler.wfile.write(body)


def _upstream(method: str, path: str, headers_in, body_in: bytes):
    host, port = _origin_parts()
    headers_out = {
        k: v for k, v in headers_in.items() if k.lower() not in ("host", "connection")
    }
    headers_out["Host"] = f"{host}:{port}"
    headers_out["Connection"] = "keep-alive"

    last_exc = None
    with _upstream_gate:
        for _attempt in range(2):
            try:
                conn = _get_conn()
                conn.request(method, path, body=body_in, headers=headers_out)
                resp = conn.getresponse()
                raw = resp.read()
                status = resp.status
                resp_headers = [(k, v) for k, v in resp.getheaders()]
                return status, resp_headers, raw
            except Exception as exc:
                last_exc = exc
                _reset_conn()
    raise last_exc  # type: ignore[misc]


def _warm_paths() -> None:
    """Compile + cache hub routes so the first human visit is already warm."""
    time.sleep(3.0)
    print(f"[cache-proxy] warming {len(WARM_PATHS)} routes sequentially…", flush=True)
    for path in WARM_PATHS:
        try:
            t0 = time.time()
            status, headers, raw = _upstream("GET", path, {}, b"")
            ct = _content_type(headers)
            if _cacheable("GET", path, status, ct) and len(raw) <= MAX_BODY and _complete_enough(path, status, ct, raw):
                with _lock:
                    _cache[_key("GET", path)] = (
                        time.time() + CACHE_TTL_SEC,
                        status,
                        headers,
                        raw,
                    )
                    _stats["misses"] += 1
            dt = time.time() - t0
            print(f"[cache-proxy] warm {path} → {status} {len(raw)}B in {dt:.1f}s", flush=True)
        except Exception as exc:
            print(f"[cache-proxy] warm failed {path}: {exc}", flush=True)
            _reset_conn()
    print(f"[cache-proxy] warm done; cache_entries={len(_cache)}", flush=True)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:
        print(f"[cache-proxy] {self.address_string()} {fmt % args}", file=sys.stderr)

    def do_GET(self):  # noqa: N802
        self._proxy("GET")

    def do_HEAD(self):  # noqa: N802
        self._proxy("HEAD")

    def do_POST(self):  # noqa: N802
        self._proxy("POST")

    def do_OPTIONS(self):  # noqa: N802
        self._proxy("OPTIONS")

    def _proxy(self, method: str) -> None:
        path = self.path
        # Lightweight health / stats for ops (not forwarded to mint)
        
        if method == "GET" and path in ("/__t3_cache_purge", "/__t3_cache_purge/"):
            with _lock:
                n = len(_cache)
                _cache.clear()
                _stats["hits"] = 0
                _stats["misses"] = 0
                _stats["bypass"] = 0
            payload = ("{\"purged\": %d}" % n).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        if method == "GET" and path in ("/__t3_cache_stats", "/__t3_cache_stats/"):
            import json

            with _lock:
                payload = json.dumps({**_stats, "entries": len(_cache)}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        key = _key("GET", path)  # HEAD shares GET cache body
        now = time.time()

        if method in ("GET", "HEAD"):
            with _lock:
                hit = _cache.get(key)
                if hit and hit[0] > now:
                    _exp, status, headers, body = hit
                    ct_hit = _content_type(headers)
                    path_only = path.split("?", 1)[0]
                    if not _complete_enough(path_only, status, ct_hit, body):
                        _cache.pop(key, None)
                        _stats["rejected_incomplete"] = _stats.get("rejected_incomplete", 0) + 1
                        hit = None
                    else:
                        _stats["hits"] += 1
                        _send_cached(self, status, headers, body, path, "HIT", _exp)
                        return

        length = int(self.headers.get("Content-Length") or 0)
        body_in = self.rfile.read(length) if length > 0 else b""

        try:
            status, resp_headers, raw = _upstream(method, path, self.headers, body_in)
        except Exception as exc:
            self.send_error(502, f"mint upstream error: {exc}")
            return

        ct = _content_type(resp_headers)
        cached = False
        # Cache from GET only; HEAD often returns empty body from upstream
        if method == "GET" and _cacheable(method, path, status, ct) and len(raw) <= MAX_BODY and _complete_enough(path, status, ct, raw):
            with _lock:
                _cache[key] = (now + CACHE_TTL_SEC, status, resp_headers, raw)
                _stats["misses"] += 1
                cached = True
        else:
            with _lock:
                _stats["bypass"] += 1

        if cached or (method == "HEAD" and key in _cache):
            # Prefer serving with browser-friendly cache headers
            with _lock:
                entry = _cache.get(key)
            if entry:
                _send_cached(
                    self,
                    entry[1],
                    entry[2],
                    entry[3] if method != "HEAD" else b"",
                    path,
                    "STORE" if cached else "HIT",
                    entry[0],
                )
                return

        self.send_response(status)
        for k, v in resp_headers:
            if k.lower() in ("transfer-encoding", "connection", "content-length"):
                continue
            self.send_header(k, v)
        self.send_header("Content-Length", str(0 if method == "HEAD" else len(raw)))
        self.send_header("X-T3-Cache", "BYPASS")
        self.end_headers()
        if method != "HEAD":
            self.wfile.write(raw)


def main() -> None:
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler)
    # Faster TIME_WAIT reuse under concurrent SPA navigation
    server.daemon_threads = True
    print(
        f"T3 mint cache proxy → {MINT_ORIGIN}\n"
        f"Browse: http://{LISTEN_HOST}:{LISTEN_PORT}/\n"
        f"TTL={CACHE_TTL_SEC}s  warm={len(WARM_PATHS)} hubs\n",
        flush=True,
    )
    threading.Thread(target=_warm_paths, name="t3-warm", daemon=True).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("stats", _stats, "cache_entries", len(_cache))


if __name__ == "__main__":
    main()
