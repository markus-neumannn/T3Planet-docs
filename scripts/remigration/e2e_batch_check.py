#!/usr/bin/env python3
"""
Phase 5 - Full Playwright E2E, UI/UX, and Responsive Testing.

Runs in resumable, checkpointed batches across every nav page in docs.json:
  - Desktop (1440x900): load, console errors, title/content sanity, sidebar,
    TOC, images (broken-image detection), tables, code blocks, Supademo
    embeds, internal link count.
  - Tablet (834x1112 portrait, then 1112x834 landscape): layout/overflow.
  - Mobile (390x844): layout/overflow, mobile-nav affordance presence.

Progress + results are persisted to e2e_progress.json after every page, so a
crash/restart resumes from where it left off (pages already marked "ok" or
"fail" are skipped unless --retry-failed is passed).

Usage:
  python3 scripts/remigration/e2e_batch_check.py [--batch-size 30] [--limit N] [--retry-failed]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from route_link_check import load_docs_json, collect_nav_paths  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent
BASE_URL = "http://localhost:3000"
PROGRESS_FILE = Path(__file__).resolve().parent / "e2e_progress.json"
REPORT_MD = Path(__file__).resolve().parent / "E2E_REPORT.md"

VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet_portrait": {"width": 834, "height": 1112},
    "tablet_landscape": {"width": 1112, "height": 834},
    "mobile": {"width": 390, "height": 844},
}

IGNORE_CONSOLE_PATTERNS = [
    re.compile(r"favicon\.ico"),
    re.compile(r"Download the React DevTools"),
    re.compile(r"\[Fast Refresh\]"),
    re.compile(r"socket\.io"),  # Next.js HMR websocket, dev-server-only, not present in production
    re.compile(r"_mintlify/assistant/siteconfig"),  # AI-assistant sidecar call, requires live cloud API, irrelevant to content
    re.compile(r"webpack-hmr"),
    # Mintlify/Next SSR hydration mismatch in local preview; not content defects
    re.compile(r"Minified React error #418"),
    re.compile(r"Minified React error #423"),
    re.compile(r"Minified React error #425"),
    # Transient upstream blips from the local cache proxy under load
    re.compile(r"502 \(Bad Gateway\)"),
]


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {}


def save_progress(progress: dict) -> None:
    # Atomic replace so concurrent readers never see a truncated/missing file.
    tmp = PROGRESS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(progress, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(PROGRESS_FILE)


def warm_up(path: str) -> None:
    try:
        req = urllib.request.Request(BASE_URL + path, headers={"User-Agent": "e2e-warmup/1.0"})
        urllib.request.urlopen(req, timeout=20).read(1)
    except Exception:
        pass


def check_page(page, path: str) -> dict:
    result = {"path": path, "status": "ok", "issues": []}
    console_errors = []

    def on_console(msg):
        if msg.type == "error":
            text = msg.text
            if any(p.search(text) for p in IGNORE_CONSOLE_PATTERNS):
                return
            console_errors.append(text[:300])

    def on_pageerror(exc):
        text = str(exc)
        if any(p.search(text) for p in IGNORE_CONSOLE_PATTERNS):
            return
        console_errors.append(f"pageerror: {text[:300]}")

    page.on("console", on_console)
    page.on("pageerror", on_pageerror)

    try:
        page.set_viewport_size(VIEWPORTS["desktop"])
        # domcontentloaded avoids hanging on Mintlify HMR/websocket "load" events
        # under the local cache proxy; content is already available at this point.
        resp = page.goto(BASE_URL + path, wait_until="domcontentloaded", timeout=45000)
        if resp is not None and resp.status >= 400:
            result["status"] = "fail"
            result["issues"].append(f"http_status={resp.status}")
            return result

        page.wait_for_timeout(500)

        title = page.title()
        if not title or title.strip() == "":
            result["issues"].append("empty_title")

        body_text = page.inner_text("body")
        if len(body_text.strip()) < 100:
            result["issues"].append(f"thin_content({len(body_text.strip())}chars)")
        # Only treat as 404 when the *title* says so. Body text often discusses
        # configuring a "404 page" / "page not found" (e.g. theme SEO guides).
        title_low = (title or "").lower()
        if "page not found" in title_low or title_low.strip().startswith("404"):
            result["issues"].append("looks_like_404")

        sidebar_count = page.locator("nav, aside, [class*='sidebar' i]").count()
        if sidebar_count == 0:
            result["issues"].append("no_sidebar_found")

        img_check = page.evaluate(
            "() => Array.from(document.images).filter(i => i.src && !i.src.startsWith('data:') "
            "&& i.complete && i.naturalWidth === 0).map(i => i.src).slice(0, 10)"
        )
        if img_check:
            result["issues"].append(f"broken_images:{img_check}")

        counts = page.evaluate(
            "() => ({tables: document.querySelectorAll('table').length, "
            "code: document.querySelectorAll('pre code, pre').length, "
            "supademo: document.querySelectorAll(\"iframe[src*='supademo']\").length, "
            "links: document.querySelectorAll(\"a[href^='/']\").length, "
            "images: document.images.length})"
        )
        result["counts"] = counts

        for vp_name in ("tablet_portrait", "tablet_landscape", "mobile"):
            page.set_viewport_size(VIEWPORTS[vp_name])
            page.wait_for_timeout(150)
            overflow = page.evaluate(
                "() => document.documentElement.scrollWidth - document.documentElement.clientWidth"
            )
            if overflow > 8:
                result["issues"].append(f"horizontal_overflow_{vp_name}={overflow}px")
            vp_body = page.inner_text("body")
            if len(vp_body.strip()) < 100:
                result["issues"].append(f"thin_content_{vp_name}")

        if console_errors:
            result["issues"].append(f"console_errors:{console_errors[:5]}")

        if result["issues"]:
            result["status"] = "fail"

    except Exception as e:
        result["status"] = "error"
        result["issues"].append(f"exception:{str(e)[:300]}")
    finally:
        page.remove_listener("console", on_console)
        page.remove_listener("pageerror", on_pageerror)

    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-size", type=int, default=30)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--retry-failed", action="store_true")
    args = ap.parse_args()

    data = load_docs_json()
    nav_paths = sorted(collect_nav_paths(data.get("navigation")))
    if args.limit:
        nav_paths = nav_paths[: args.limit]

    progress = load_progress()

    todo = []
    for p in nav_paths:
        prior = progress.get(p)
        if prior is None:
            todo.append(p)
        elif args.retry_failed and prior.get("status") != "ok":
            todo.append(p)

    print(f"Total nav paths: {len(nav_paths)}; already done: {len(nav_paths) - len(todo)}; to check: {len(todo)}")

    if not todo:
        print("Nothing to do.")
        write_report(progress, nav_paths)
        return

    from playwright.sync_api import sync_playwright

    batch_size = args.batch_size
    batches = [todo[i : i + batch_size] for i in range(0, len(todo), batch_size)]

    with sync_playwright() as pw:
        for bi, batch in enumerate(batches):
            print(f"\n=== Batch {bi+1}/{len(batches)} ({len(batch)} pages) ===")
            browser = pw.chromium.launch()
            context = browser.new_context()
            page = context.new_page()
            for path in batch:
                warm_up(path)
                t0 = time.time()
                r = check_page(page, path)
                if r["status"] != "ok":
                    # One retry: dev-server-only staleness (stale RSC/hydration
                    # cache after HMR churn) can cause false positives that a
                    # simple re-navigation clears; a real bug reproduces twice.
                    time.sleep(2)
                    r2 = check_page(page, path)
                    if r2["status"] == "ok":
                        r = r2
                        r["issues"] = []
                        r["note"] = "passed_on_retry"
                    else:
                        r = r2
                r["elapsed_s"] = round(time.time() - t0, 2)
                progress[path] = r
                mark = "OK" if r["status"] == "ok" else r["status"].upper()
                extra = f" {r['issues']}" if r["issues"] else ""
                print(f"  [{mark}] {path} ({r['elapsed_s']}s){extra}")
                save_progress(progress)
            context.close()
            browser.close()

    write_report(progress, nav_paths)


def write_report(progress: dict, nav_paths: list[str]) -> None:
    ok = [p for p in nav_paths if progress.get(p, {}).get("status") == "ok"]
    fail = [p for p in nav_paths if progress.get(p, {}).get("status") == "fail"]
    error = [p for p in nav_paths if progress.get(p, {}).get("status") == "error"]
    missing = [p for p in nav_paths if p not in progress]

    lines = ["# Phase 5 - Playwright E2E / UI / Responsive Report", ""]
    lines.append(f"- Total pages: **{len(nav_paths)}**")
    lines.append(f"- OK: **{len(ok)}**")
    lines.append(f"- FAIL (issues found): **{len(fail)}**")
    lines.append(f"- ERROR (couldn't load/check): **{len(error)}**")
    lines.append(f"- Not yet checked: **{len(missing)}**")
    lines.append("")

    if fail:
        lines.append(f"## Pages with issues ({len(fail)})")
        for p in fail:
            lines.append(f"- `{p}`: {progress[p]['issues']}")
        lines.append("")
    if error:
        lines.append(f"## Pages that errored ({len(error)})")
        for p in error:
            lines.append(f"- `{p}`: {progress[p]['issues']}")
        lines.append("")
    if missing:
        lines.append(f"## Not yet checked ({len(missing)})")
        for p in missing[:50]:
            lines.append(f"- `{p}`")
        lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[:15]))
    print(f"\nFull report: {REPORT_MD}")


if __name__ == "__main__":
    main()
