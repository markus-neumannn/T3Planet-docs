#!/usr/bin/env python3
"""Local caching reverse proxy in front of mint dev.

Mintlify `mint dev` recompiles MDX/RSC on every request (often 6–12s). Live RTD
serves prebuilt HTML in <1s. This proxy caches successful HTML + RSC responses
so repeat views and SPA hops hit memory cache (~instant), matching the 1–2s
target after the first warm compile.

Usage:
  1. mint dev on :3001  (or set MINT_ORIGIN)
  2. python3 scripts/mint_cache_proxy.py   # listens on :3000

Browse http://127.0.0.1:3000 — first hit warms, next hits are cached.
"""
from __future__ import annotations

import hashlib
import os
import threading
import time
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

LISTEN_HOST = os.environ.get("PROXY_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("PROXY_PORT", "3000"))
MINT_ORIGIN = os.environ.get("MINT_ORIGIN", "http://127.0.0.1:3001")
CACHE_TTL_SEC = int(os.environ.get("CACHE_TTL", "3600"))
MAX_BODY = int(os.environ.get("CACHE_MAX_BODY", str(3 * 1024 * 1024)))

_cache: dict[str, tuple[float, int, list[tuple[str, str]], bytes]] = {}
_lock = threading.Lock()
_stats = {"hits": 0, "misses": 0, "bypass": 0}


def _origin_parts():
    u = urlsplit(MINT_ORIGIN)
    return u.hostname or "127.0.0.1", u.port or 80


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
    # Static assets from mint / our _static — cache aggressively
    if path.startswith("/_next/static/") or path.startswith("/_static/"):
        return True
    if path.endswith((".css", ".js", ".svg", ".webp", ".png", ".woff2")):
        return True
    return False


def _key(method: str, path: str) -> str:
    return hashlib.sha1(f"{method}:{path}".encode()).hexdigest()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args) -> None:
        sys_stderr = __import__("sys").stderr
        print(f"[cache-proxy] {self.address_string()} {fmt % args}", file=sys_stderr)

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
        key = _key(method, path)
        now = time.time()

        if method == "GET":
            with _lock:
                hit = _cache.get(key)
                if hit and hit[0] > now:
                    _stats["hits"] += 1
                    exp, status, headers, body = hit
                    self.send_response(status)
                    for k, v in headers:
                        if k.lower() in ("transfer-encoding", "connection", "content-length"):
                            continue
                        self.send_header(k, v)
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("X-T3-Cache", "HIT")
                    self.end_headers()
                    self.wfile.write(body)
                    return

        # Forward to mint
        host, port = _origin_parts()
        length = int(self.headers.get("Content-Length") or 0)
        body_in = self.rfile.read(length) if length > 0 else b""
        headers_out = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "connection")}
        headers_out["Host"] = f"{host}:{port}"
        headers_out["Connection"] = "close"

        try:
            conn = HTTPConnection(host, port, timeout=180)
            conn.request(method, path, body=body_in, headers=headers_out)
            resp = conn.getresponse()
            raw = resp.read()
            status = resp.status
            resp_headers = [(k, v) for k, v in resp.getheaders()]
            conn.close()
        except Exception as exc:
            self.send_error(502, f"mint upstream error: {exc}")
            return

        ct = ""
        for k, v in resp_headers:
            if k.lower() == "content-type":
                ct = v
                break

        cached = False
        if method == "GET" and _cacheable(method, path, status, ct) and len(raw) <= MAX_BODY:
            with _lock:
                _cache[key] = (now + CACHE_TTL_SEC, status, resp_headers, raw)
                _stats["misses"] += 1
                cached = True
        else:
            with _lock:
                _stats["bypass"] += 1

        self.send_response(status)
        for k, v in resp_headers:
            if k.lower() in ("transfer-encoding", "connection", "content-length"):
                continue
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("X-T3-Cache", "STORE" if cached else "BYPASS")
        self.end_headers()
        if method != "HEAD":
            self.wfile.write(raw)


def main() -> None:
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), Handler)
    print(
        f"T3 mint cache proxy → {MINT_ORIGIN}\n"
        f"Browse: http://{LISTEN_HOST}:{LISTEN_PORT}/\n"
        f"TTL={CACHE_TTL_SEC}s  (hits feel like live CDN after first compile)\n",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("stats", _stats, "cache_entries", len(_cache))


if __name__ == "__main__":
    main()
