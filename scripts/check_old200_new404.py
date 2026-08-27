#!/usr/bin/env python3
"""Find old RTD pages (HTTP 200) whose Mintlify twin is missing / 404."""
from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OLD_INDEX = Path(
    "/Users/nitsan/.cursor/projects/Users-nitsan-www-AI-Agents-Mintilify-Doc/uploads/latest-1.md"
)
OLD_BASE = "https://docs.t3planet.de/en/latest"
NEW_BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3001"
REPORT = ROOT / "scripts" / "old200_new404_report.json"
UA = "Mozilla/5.0 (compatible; T3Planet-404-Audit/1.1)"

# Not real content pages — artifacts / Sphinx utilities.
SKIP_SUFFIXES = (".zip.html",)
SKIP_PATHS = {
    "/",
    "/index.html",
    "/history.html",
    "/readme.html",
    "/genindex.html",
    "/search.html",
    "/py-modindex.html",
}


def extract_old_paths() -> list[str]:
    text = OLD_INDEX.read_text(encoding="utf-8")
    urls = set(re.findall(r"https://docs\.t3planet\.de/en/latest/[^\s\)\]\"]+", text))
    paths = []
    for u in urls:
        path = u.replace(OLD_BASE, "", 1)
        if not path.startswith("/"):
            path = "/" + path
        paths.append(path.rstrip(".,;)"))
    return sorted(set(paths))


def old_path_to_new_route(old_path: str) -> str:
    path = old_path.lstrip("/")
    if path.endswith(".html"):
        path = path[:-5]
    if not path or path in {"index", "Index"}:
        return "/"
    return f"/{path}"


def route_to_md(route: str) -> Path | None:
    if route == "/":
        return ROOT / "index.md"
    parts = route.strip("/").split("/")
    # /ExtNsT3AI/Index -> ExtNsT3AI/Index.md
    # /ExtNsT3AI/Installation/Index -> ExtNsT3AI/Installation/Index.md
    candidate = ROOT.joinpath(*parts).with_suffix(".md")
    if candidate.exists():
        return candidate
    # fallback Index.md under folder
    if parts[-1] != "Index":
        alt = ROOT.joinpath(*parts, "Index.md")
        if alt.exists():
            return alt
    return candidate if candidate.exists() else None


def http_status(url: str, method: str = "GET") -> int:
    try:
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as r:
            return int(r.status)
    except urllib.error.HTTPError as e:
        return int(e.code)
    except Exception:
        return 0


def check_old(path: str) -> tuple[str, int]:
    url = f"{OLD_BASE}{path}"
    code = http_status(url, "HEAD")
    if code in (0, 405, 403):
        code = http_status(url, "GET")
    return path, code


def check_new(route: str) -> int:
    url = NEW_BASE.rstrip("/") + route
    code = http_status(url, "HEAD")
    if code in (0, 405):
        code = http_status(url, "GET")
    return code


def wait_for_new(timeout: int = 120) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if http_status(NEW_BASE + "/", "GET") == 200:
            return True
        time.sleep(2)
    return False


def main() -> None:
    old_paths = extract_old_paths()
    print(f"Old index linked pages: {len(old_paths)}", flush=True)

    # Phase 1: filesystem — every mapped Mintlify page must exist
    missing_md = []
    mapped = []
    skipped = []
    for old_path in old_paths:
        if old_path in SKIP_PATHS or any(old_path.endswith(s) for s in SKIP_SUFFIXES):
            skipped.append(old_path)
            continue
        route = old_path_to_new_route(old_path)
        md = route_to_md(route)
        mapped.append((old_path, route, md))
        if md is None or not md.exists():
            missing_md.append(
                {
                    "old_path": old_path,
                    "new_route": route,
                    "md": None if md is None else str(md.relative_to(ROOT)),
                }
            )

    print(f"Content pages mapped: {len(mapped)}", flush=True)
    print(f"Skipped utilities/artifacts: {len(skipped)}", flush=True)
    print(f"Missing Mintlify .md files: {len(missing_md)}", flush=True)

    # Phase 2: confirm old pages are HTTP 200 (rate-limited)
    print("Checking old RTD HTTP status (workers=4)...", flush=True)
    old_status: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(check_old, p): p for p, _, _ in mapped}
        done = 0
        for fut in as_completed(futs):
            path, code = fut.result()
            old_status[path] = code
            done += 1
            if done % 100 == 0:
                print(f"  old {done}/{len(mapped)}", flush=True)

    old_200 = [p for p, c in old_status.items() if c == 200]
    old_other = {p: c for p, c in old_status.items() if c != 200}
    print(f"Old HTTP 200: {len(old_200)} / {len(mapped)}", flush=True)
    if old_other:
        counts: dict[int, int] = {}
        for c in old_other.values():
            counts[c] = counts.get(c, 0) + 1
        print(f"Old non-200: {counts}", flush=True)

    # Phase 3: HTTP check Mintlify for pages that were old-200
    print(f"Waiting for Mintlify at {NEW_BASE}...", flush=True)
    mint_up = wait_for_new(150)
    print(f"Mintlify ready: {mint_up}", flush=True)

    regressions = []
    new_status: dict[str, int] = {}
    if mint_up:
        targets = [(p, r) for p, r, md in mapped if old_status.get(p) == 200]
        print(f"Checking {len(targets)} new routes...", flush=True)
        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = {ex.submit(check_new, r): (p, r) for p, r in targets}
            done = 0
            for fut in as_completed(futs):
                p, r = futs[fut]
                code = fut.result()
                new_status[r] = code
                done += 1
                if done % 100 == 0:
                    print(f"  new {done}/{len(targets)}", flush=True)
                md = route_to_md(r)
                if code == 404 or (md is None or not md.exists()):
                    regressions.append(
                        {
                            "old_url": f"{OLD_BASE}{p}",
                            "old_status": 200,
                            "new_route": r,
                            "new_url": NEW_BASE.rstrip("/") + r,
                            "new_status": code,
                            "md_exists": bool(md and md.exists()),
                        }
                    )
    else:
        # Fall back to filesystem-only for old-200 pages
        for p, r, md in mapped:
            if old_status.get(p) != 200:
                continue
            if md is None or not md.exists():
                regressions.append(
                    {
                        "old_url": f"{OLD_BASE}{p}",
                        "old_status": 200,
                        "new_route": r,
                        "new_url": NEW_BASE.rstrip("/") + r,
                        "new_status": None,
                        "md_exists": False,
                    }
                )

    report = {
        "old_base": OLD_BASE,
        "new_base": NEW_BASE,
        "old_index_urls": len(old_paths),
        "content_pages_checked": len(mapped),
        "skipped": skipped,
        "old_http_200": len(old_200),
        "old_non_200": {str(k): v for k, v in sorted(
            ((c, sum(1 for x in old_other.values() if x == c)) for c in set(old_other.values())),
            key=lambda x: x[0],
        )},
        "missing_md_count": len(missing_md),
        "missing_md": missing_md,
        "regressions_old200_new404": len(regressions),
        "regressions": regressions,
        "mintlify_http_checked": mint_up,
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    summary = {
        "old_index_urls": report["old_index_urls"],
        "content_pages_checked": report["content_pages_checked"],
        "old_http_200": report["old_http_200"],
        "missing_md": report["missing_md_count"],
        "regressions_old200_new404": report["regressions_old200_new404"],
        "mintlify_http_checked": mint_up,
        "report": str(REPORT),
    }
    print(json.dumps(summary, indent=2), flush=True)
    if regressions:
        print("\nREGRESSIONS (old 200 → new missing/404):", flush=True)
        for r in regressions[:40]:
            print(f"  {r['old_url']}  →  {r['new_route']}  (new={r['new_status']}, md={r['md_exists']})", flush=True)
    else:
        print("\nOK: No old HTTP 200 content page maps to a missing/404 Mintlify page.", flush=True)


if __name__ == "__main__":
    main()
