#!/usr/bin/env python3
"""
Scan TYPO3 backend Editor pages for visual-editor load failures / exceptions.

Logs in to TYPO3, opens the Editor module, and checks each page ID for:
  - visual-editor iframe chrome-error (sad document icon in backend)
  - editMode=1 request failures (CSP block, network error, HTTP 5xx)
  - "Whoops, looks like something went wrong" TYPO3 exception banner

Usage:
  TYPO3_USER=nitsan-developer TYPO3_PASS='...' python3 scripts/typo3_page_error_scanner.py
  python3 scripts/typo3_page_error_scanner.py --start 1 --end 100 --headed
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE = "https://staging.nitsantech.de"
DEFAULT_REPORT = ROOT / "scripts" / "typo3_page_error_report.json"
DEFAULT_PROGRESS = ROOT / "scripts" / "typo3_page_error_progress.json"

WHOOPS_TEXT = "Whoops, looks like something went wrong"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Scan TYPO3 Editor pages for exception errors.")
    p.add_argument("--base-url", default=os.environ.get("TYPO3_BASE_URL", DEFAULT_BASE))
    p.add_argument("--user", default=os.environ.get("TYPO3_USER", ""))
    p.add_argument("--password", default=os.environ.get("TYPO3_PASS", ""))
    p.add_argument("--start", type=int, default=1)
    p.add_argument("--end", type=int, default=2367)
    p.add_argument("--wait-seconds", type=float, default=6.0, help="Max wait for visual editor iframe")
    p.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    p.add_argument("--progress", type=Path, default=DEFAULT_PROGRESS)
    p.add_argument("--resume", action="store_true", help="Skip page IDs already recorded in progress file")
    p.add_argument("--headed", action="store_true")
    return p.parse_args()


def load_progress(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"checked": {}, "errors": []}


def save_progress(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def login(page, base_url: str, user: str, password: str) -> None:
    page.goto(f"{base_url}/typo3", wait_until="domcontentloaded", timeout=90_000)
    page.fill('input[name="username"]', user)
    page.fill('input[type="password"]', password)
    page.click('button[type="submit"], input[type="submit"], .btn-login')
    page.wait_for_load_state("networkidle", timeout=90_000)


def check_page(page, base_url: str, page_id: int, wait_seconds: float) -> dict:
    edit_url = f"{base_url}/typo3/module/web/edit?id={page_id}"
    failed_editmode: list[tuple[str, str]] = []
    bad_status: list[tuple[str, int]] = []

    def on_failed(request) -> None:
        if "editMode=1" in request.url:
            failed_editmode.append((request.url, request.failure or "unknown"))

    def on_response(response) -> None:
        if "editMode=1" in response.url and response.status >= 400:
            bad_status.append((response.url, response.status))

    page.on("requestfailed", on_failed)
    page.on("response", on_response)

    try:
        page.goto(edit_url, wait_until="domcontentloaded", timeout=60_000)
    except Exception as exc:
        return {
            "page_id": page_id,
            "error": True,
            "reason": f"navigation_failed: {exc}",
        }

    deadline = time.time() + wait_seconds
    ve_frame = None
    while time.time() < deadline:
        for frame in page.frames:
            if frame.name == "visual-editor-iframe":
                ve_frame = frame
                if not frame.url.startswith("chrome-error://"):
                    break
        if ve_frame and not ve_frame.url.startswith("chrome-error://"):
            break
        time.sleep(0.25)

    reasons: list[str] = []

    if ve_frame and ve_frame.url.startswith("chrome-error://"):
        reasons.append("visual_editor_iframe_failed")

    for _url, failure in failed_editmode:
        reasons.append(f"editmode_request_failed:{failure}")

    for _url, status in bad_status:
        reasons.append(f"editmode_http_{status}")

    if ve_frame and not ve_frame.url.startswith("chrome-error://"):
        try:
            has_whoops = ve_frame.evaluate(
                f"() => document.body && document.body.innerText.includes({json.dumps(WHOOPS_TEXT)})"
            )
            if has_whoops:
                reasons.append("whoops_exception_banner")
        except Exception:
            pass

    # Also check list_frame body for backend-side exceptions
    for frame in page.frames:
        if frame.name == "list_frame":
            try:
                has_whoops = frame.evaluate(
                    f"() => document.body && document.body.innerText.includes({json.dumps(WHOOPS_TEXT)})"
                )
                if has_whoops:
                    reasons.append("whoops_in_list_frame")
            except Exception:
                pass

    iframe_src = None
    for frame in page.frames:
        if frame.name == "list_frame":
            try:
                iframe_src = frame.evaluate(
                    "() => document.getElementById('visual-editor-iframe')?.src || null"
                )
            except Exception:
                pass

    return {
        "page_id": page_id,
        "error": bool(reasons),
        "reasons": reasons,
        "visual_editor_url": ve_frame.url if ve_frame else None,
        "iframe_src": iframe_src,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    args = parse_args()
    if not args.user or not args.password:
        print("ERROR: Set TYPO3_USER and TYPO3_PASS environment variables or use --user/--password.", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed. Run: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    progress = load_progress(args.progress) if args.resume else {"checked": {}, "errors": []}
    error_ids = set(progress.get("errors", []))

    print(f"Scanning TYPO3 pages {args.start}–{args.end} on {args.base_url}")
    print(f"Progress file: {args.progress}")
    print(f"Report file:   {args.report}")

    t0 = time.time()
    checked_count = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        print("Logging in…")
        login(page, args.base_url, args.user, args.password)
        print("Login OK. Starting page scan…")

        for page_id in range(args.start, args.end + 1):
            key = str(page_id)
            if args.resume and key in progress.get("checked", {}):
                continue

            result = check_page(page, args.base_url, page_id, args.wait_seconds)
            progress.setdefault("checked", {})[key] = result
            if result.get("error"):
                if page_id not in error_ids:
                    progress.setdefault("errors", []).append(page_id)
                    error_ids.add(page_id)

            checked_count += 1
            if checked_count % 10 == 0 or result.get("error"):
                status = "ERROR" if result.get("error") else "ok"
                reasons = ", ".join(result.get("reasons", [])) or "-"
                elapsed = time.time() - t0
                rate = checked_count / elapsed if elapsed else 0
                print(
                    f"[{page_id}/{args.end}] {status} | errors so far: {len(error_ids)} | "
                    f"{rate:.2f} pages/s | last: {reasons}",
                    flush=True,
                )

            if checked_count % 25 == 0:
                save_progress(args.progress, progress)

        browser.close()

    save_progress(args.progress, progress)

    report = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "base_url": args.base_url,
        "range": {"start": args.start, "end": args.end},
        "total_checked": len(progress.get("checked", {})),
        "error_count": len(progress.get("errors", [])),
        "error_page_ids": sorted(progress.get("errors", [])),
        "details": {
            pid: progress["checked"][str(pid)]
            for pid in sorted(progress.get("errors", []))
            if str(pid) in progress.get("checked", {})
        },
    }
    args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")

    elapsed = time.time() - t0
    print("\n" + "=" * 60)
    print(f"Scan complete in {elapsed / 60:.1f} minutes")
    print(f"Pages with errors: {len(report['error_page_ids'])}")
    print(f"Error page IDs: {report['error_page_ids']}")
    print(f"Full report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
