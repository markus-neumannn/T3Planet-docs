#!/usr/bin/env python3
"""End-to-end QA: HTTP routes, links, images, Playwright navigation + console errors."""
from __future__ import annotations

import json
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "scripts" / "e2e_production_qa_report.json"
REPORT_MD = ROOT / "scripts" / "E2E_PRODUCTION_QA_REPORT.md"

SKIP_PARTS = {"scripts", "node_modules", ".git", ".venv-translate", "de", "ai universe documentation"}
MINTIGNORE_NAMES: set[str] | None = None


def load_mintignore() -> set[str]:
    global MINTIGNORE_NAMES
    if MINTIGNORE_NAMES is not None:
        return MINTIGNORE_NAMES
    names: set[str] = set()
    ignore = ROOT / ".mintignore"
    if ignore.exists():
        for line in ignore.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            names.add(line.rstrip("/"))
    MINTIGNORE_NAMES = names
    return names


def is_excluded_md(rel: str) -> bool:
    if rel.startswith("de/") or any(p in SKIP_PARTS for p in rel.split("/")):
        return True
    base = Path(rel).name
    if base in load_mintignore():
        return True
    return False
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)\s]+)\)|href=\"(/[^\"]+)\"")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']")


def md_to_route(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if parts[-1].lower() == "index.md":
        parts = parts[:-1]
        return f"/{'/'.join(parts)}/Index" if parts else "/"
    return "/" + "/".join(parts[:-1] + [parts[-1][:-3]])


def collect_en_routes() -> list[str]:
    routes: list[str] = []
    for md in sorted(ROOT.rglob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        if is_excluded_md(rel):
            continue
        routes.append(md_to_route(rel))
    return sorted(set(routes))


def http_check(base: str, path: str, timeout: float = 30.0) -> dict:
    url = base.rstrip("/") + (path if path != "/" else "/")
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "T3Planet-E2E-QA/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(2048)
            ms = int((time.perf_counter() - t0) * 1000)
            return {"path": path, "status": resp.status, "ms": ms, "ok": resp.status == 200}
    except Exception as exc:
        ms = int((time.perf_counter() - t0) * 1000)
        return {"path": path, "status": 0, "ms": ms, "ok": False, "error": str(exc)}


def audit_markdown() -> dict:
    broken_links: list[dict] = []
    missing_images: list[dict] = []
    for md in ROOT.rglob("*.md"):
        if is_excluded_md(md.relative_to(ROOT).as_posix()):
            continue
        rel = md.relative_to(ROOT).as_posix()
        text = md.read_text(encoding="utf-8")
        for t in set(LINK_RE.findall(text)):
            path = (t[0] or t[1]).split("#")[0].rstrip("/")
            if not path or path.startswith("//") or re.search(r"\.(png|jpg|jpeg|gif|svg|webp|pdf)$", path, re.I):
                continue
            cand = ROOT / f"{path.lstrip('/')}.md"
            if not cand.exists() and path not in ("/",):
                broken_links.append({"from": rel, "to": path})
        for m in IMG_RE.findall(text):
            src = (m[0] or m[1]).split("#")[0].split("?")[0]
            if src.startswith("http"):
                continue
            # Skip placeholder references in backticks, e.g. `[Screenshot: images/foo.png]`
            if f"`{src}`" in text or f"`[Screenshot: {src}]`" in text:
                continue
            ip = ROOT / src.lstrip("/") if src.startswith("/") else (md.parent / src).resolve()
            if not ip.exists():
                missing_images.append({"page": rel, "src": src})
    return {
        "broken_internal_links": len(broken_links),
        "broken_link_samples": broken_links[:25],
        "missing_images": len(missing_images),
        "missing_image_samples": missing_images[:25],
    }


def playwright_suite(base: str) -> dict:
    from playwright.sync_api import sync_playwright

    hops = [
        ("/", "/AllTemplates/Index", "#sidebar-content"),
        ("/AllTemplates/Index", "/AllExtensions/Index", "#sidebar-content"),
        ("/License/Index", "/License/Introduction/Index", "#content"),
        ("/License/Introduction/Index", "/License/GenerateLicenseKey/Index", "#sidebar-content"),
        ("/License/GenerateLicenseKey/Index", "/License/LicenseManager/Index", "#pagination"),
        ("/ExtNsT3AI/Index", "/ExtNsT3AI/Introduction/Index", "#sidebar-content"),
    ]
    hub_checks = [
        ("/", ".t3-view-all"),
        ("/AllExtensions/Index", ".t3-extension-row"),
        ("/License/Index", 'a[href="/License/Introduction/Index"]'),
    ]
    console_errors: list[str] = []
    spa_times: list[dict] = []
    ui_issues: list[dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        page.goto(base, wait_until="domcontentloaded", timeout=120000)
        time.sleep(1.5)

        for path, selector in hub_checks:
            page.goto(base.rstrip("/") + path, wait_until="domcontentloaded", timeout=120000)
            time.sleep(0.8)
            loc = page.locator(selector).first
            if not loc.count():
                ui_issues.append({"page": path, "issue": f"missing {selector}"})
                continue
            if selector == ".t3-view-all":
                box = loc.bounding_box()
                text = loc.inner_text()
                if box and box["width"] < 50:
                    ui_issues.append({"page": path, "issue": f"clipped view-all: {text!r}"})
            if selector == ".t3-extension-row":
                meta = page.locator(".t3-extension-meta").first
                if meta.count():
                    display = meta.evaluate("el => getComputedStyle(el).display")
                    if display != "flex":
                        ui_issues.append({"page": path, "issue": "extension meta not flex"})

        for src, dst, scope in hops:
            page.goto(base.rstrip("/") + src, wait_until="domcontentloaded", timeout=120000)
            time.sleep(0.5)
            if " a[href" in scope or scope.startswith("a[href"):
                link = page.locator(scope).first
            else:
                link = page.locator(
                    f'{scope} a[href="{dst}"], {scope} a[href="{dst}.html"]'
                ).first
            if not link.count():
                spa_times.append({"from": src, "to": dst, "ms": None, "error": "link not found"})
                continue
            t0 = time.perf_counter()
            try:
                link.scroll_into_view_if_needed(timeout=5000)
            except Exception:
                pass
            link.click(timeout=30000, force=("navbar" in scope))
            try:
                page.wait_for_function(
                    f"() => location.pathname.replace(/\\/$/, '') === '{dst.rstrip('/')}'",
                    timeout=90000,
                )
                spa_times.append({"from": src, "to": dst, "ms": int((time.perf_counter() - t0) * 1000)})
            except Exception as exc:
                spa_times.append(
                    {
                        "from": src,
                        "to": dst,
                        "ms": int((time.perf_counter() - t0) * 1000),
                        "error": str(exc),
                    }
                )

        browser.close()

    times = [h["ms"] for h in spa_times if h.get("ms")]
    return {
        "spa_navigation": spa_times,
        "spa_ms_median": int(statistics.median(times)) if times else None,
        "spa_ms_max": max(times) if times else None,
        "console_errors": console_errors[:30],
        "console_error_count": len(console_errors),
        "ui_issues": ui_issues,
    }


def write_report(payload: dict) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    s = payload["summary"]
    lines = [
        "# T3Planet Docs — End-to-End Production QA Report",
        "",
        f"**Generated:** {now}",
        f"**Base URL:** {s['base_url']}",
        "",
        "## Summary",
        "",
        f"| Check | Result |",
        f"|-------|--------|",
        f"| EN routes | {s['route_count']} |",
        f"| HTTP 200 | {s['http_ok']}/{s['route_count']} |",
        f"| HTTP median | {s.get('http_ms_median')} ms |",
        f"| Broken internal links | {s['broken_internal_links']} |",
        f"| Missing images | {s['missing_images']} |",
        f"| SPA median | {s.get('spa_ms_median')} ms |",
        f"| Console errors | {s.get('console_error_count', 0)} |",
        f"| UI issues | {s.get('ui_issue_count', 0)} |",
        "",
    ]
    if payload.get("ui_issues"):
        lines += ["## UI Issues", ""]
        for u in payload["ui_issues"]:
            lines.append(f"- `{u['page']}`: {u['issue']}")
        lines.append("")
    if payload.get("http_failures"):
        lines += ["## HTTP Failures", ""]
        for f in payload["http_failures"][:20]:
            lines.append(f"- `{f['path']}` — {f.get('error', f.get('status'))}")
        lines.append("")
    if payload.get("spa_navigation"):
        lines += ["## SPA Navigation", "", "| From → To | ms |", "|-----------|-----|"]
        for hop in payload["spa_navigation"]:
            err = f" ({hop['error']})" if hop.get("error") else ""
            lines.append(f"| {hop.get('from')} → {hop.get('to')} | {hop.get('ms', '—')}{err} |")
        lines.append("")
    if payload.get("error"):
        lines += ["## Playwright Error", "", f"```\n{payload['error']}\n```", ""]
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
    routes = collect_en_routes()
    md_audit = audit_markdown()

    print(f"HTTP checking {len(routes)} routes against {base}...")
    http_results: list[dict] = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(http_check, base, r): r for r in routes}
        for fut in as_completed(futs):
            http_results.append(fut.result())

    http_ok = sum(1 for r in http_results if r["ok"])
    http_times = [r["ms"] for r in http_results if r["ok"]]
    failures = [r for r in http_results if not r["ok"]]

    print("Running Playwright E2E...")
    try:
        pw = playwright_suite(base)
    except Exception as exc:
        pw = {"error": str(exc), "spa_navigation": [], "ui_issues": [], "console_errors": []}

    payload = {
        "summary": {
            "base_url": base,
            "route_count": len(routes),
            "http_ok": http_ok,
            "http_ms_median": int(statistics.median(http_times)) if http_times else None,
            "broken_internal_links": md_audit["broken_internal_links"],
            "missing_images": md_audit["missing_images"],
            "spa_ms_median": pw.get("spa_ms_median"),
            "spa_ms_max": pw.get("spa_ms_max"),
            "console_error_count": pw.get("console_error_count", 0),
            "ui_issue_count": len(pw.get("ui_issues", [])),
        },
        "markdown_audit": md_audit,
        "http_failures": failures,
        "http_slowest": sorted(http_results, key=lambda r: r["ms"], reverse=True)[:15],
        **pw,
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_report(payload)
    print(json.dumps(payload["summary"], indent=2))
    print(f"Wrote {REPORT_MD}")


if __name__ == "__main__":
    main()
