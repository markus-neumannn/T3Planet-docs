#!/usr/bin/env python3
"""QA tests for T3Planet sidebar navigation."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")
REPORT = ROOT / "scripts" / "sidebar_qa_report.json"

TEST_PAGES = [
    "/",
    "/ExtNsT3AI/Installation/Index",
    "/EXTKarma/Index",
    "/de/index",
    "/de/ExtNsT3AI/Installation/Index",
]


def http_ok(path: str) -> bool:
    try:
        req = urllib.request.Request(f"{BASE}{path}", method="HEAD")
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status == 200
    except Exception:
        try:
            with urllib.request.urlopen(f"{BASE}{path}", timeout=8) as r:
                return r.status == 200
        except Exception:
            return False


def run_playwright() -> list[dict]:
    script = r'''
from playwright.sync_api import sync_playwright
import json

BASE = "%s"
pages = %s
results = []

def check(page, name, viewport, setup=None):
    page.set_viewport_size(viewport)
    for path in pages:
        page.goto(BASE + path, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2800)
        if setup:
            setup(page)
        data = page.evaluate("""() => {
          const content = document.getElementById('sidebar-content');
          const sidebar = document.getElementById('sidebar');
          return {
            path: location.pathname,
            sidebarVisible: sidebar ? getComputedStyle(sidebar).display !== 'none' : false,
            searchBtn: !!document.querySelector('[data-t3-sidebar-search]'),
            filterInput: !!document.getElementById('t3-sidebar-filter-input'),
            footer: !!document.querySelector('[data-t3-sidebar-footer]'),
            dropdown: !!document.querySelector('button.nav-dropdown-trigger'),
            icons: document.querySelectorAll('#sidebar-content svg').length,
            groups: document.querySelectorAll('.sidebar-group-header').length,
            activeLink: !!content && !!content.querySelector('a[aria-current="page"]'),
            groupHeaders: [...document.querySelectorAll('.sidebar-group-header')].map(h => h.textContent.trim()).slice(0,6),
            ariaExpanded: [...document.querySelectorAll('.sidebar-group-header[aria-expanded]')].length,
          };
        }""")
        results.append({"suite": name, "path": path, **data})

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    check(page, "desktop", {"width": 1440, "height": 900})

    def dark_setup(pg):
        pg.evaluate("() => document.documentElement.classList.add('dark')")
    check(page, "desktop-dark", {"width": 1440, "height": 900}, dark_setup)

    check(page, "mobile", {"width": 390, "height": 844})

    # Collapse test desktop
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(BASE + "/ExtNsT3AI/Installation/Index", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    header = page.locator('.sidebar-group-header').first
    if header.count():
        header.click()
        page.wait_for_timeout(400)
        collapsed = page.evaluate("""() => {
          const g = document.querySelector('.t3-sidebar-group.t3-sidebar-collapsed');
          return !!g;
        }""")
        results.append({"suite": "collapse", "path": "/ExtNsT3AI/Installation/Index", "collapsed": collapsed})

    # Filter test
    page.goto(BASE + "/", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(2500)
    filt = page.locator('#t3-sidebar-filter-input')
    if filt.count():
        filt.fill("T3AI")
        page.wait_for_timeout(500)
        visible = page.evaluate("""() => document.querySelectorAll('#sidebar-content a[href^="/"]:not(.t3-sidebar-filter-hidden)').length""")
        results.append({"suite": "filter", "path": "/", "visibleAfterFilter": visible, "passed": visible > 0 and visible < 50})

    browser.close()

print(json.dumps(results))
''' % (
        BASE,
        json.dumps(TEST_PAGES),
    )

    proc = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=180,
        cwd=str(ROOT),
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr or proc.stdout or "playwright failed")
    return json.loads(proc.stdout.strip().split("\n")[-1] if "\n" in proc.stdout else proc.stdout)


def main() -> int:
    print(f"Sidebar QA — {BASE}\n")

    if not http_ok("/"):
        print("ERROR: Dev server not reachable. Start with: mint dev --port 3333")
        return 1

    link_checks = [{"path": p, "ok": http_ok(p)} for p in TEST_PAGES]
    failed_links = [c for c in link_checks if not c["ok"]]

    try:
        pw = run_playwright()
    except Exception as e:
        pw = []
        print(f"Playwright tests skipped: {e}")

    summary = {
        "base_url": BASE,
        "route_checks": link_checks,
        "playwright": pw,
        "failed_routes": len(failed_links),
        "passed": len(failed_links) == 0 and len(pw) > 0,
    }

    if pw:
        for row in pw:
            suite = row.get("suite", "?")
            path = row.get("path", "?")
            if suite in ("desktop", "desktop-dark", "mobile"):
                ok = (
                    row.get("groups", 0) >= 3
                    and not row.get("searchBtn")
                    and not row.get("filterInput")
                    and not row.get("footer")
                    and not row.get("dropdown")
                )
                status = "PASS" if ok else "FAIL"
                print(f"[{status}] {suite} {path} — groups={row.get('groups')} icons={row.get('icons')} active={row.get('activeLink')}")
            elif suite == "collapse":
                print(f"[{'PASS' if row.get('collapsed') else 'FAIL'}] collapse toggle — {path}")
            elif suite == "filter":
                print(f"[{'PASS' if row.get('passed') else 'FAIL'}] filter — visible={row.get('visibleAfterFilter')}")

    for c in link_checks:
        print(f"[{'PASS' if c['ok'] else 'FAIL'}] route {c['path']}")

    REPORT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\nReport: {REPORT}")
    return 0 if summary["passed"] and not failed_links else 1


if __name__ == "__main__":
    raise SystemExit(main())
