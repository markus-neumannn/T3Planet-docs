#!/usr/bin/env python3
"""Performance audit for T3Planet Mintlify docs (local dev server)."""
from __future__ import annotations

import json
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPORT_JSON = ROOT / "scripts" / "performance_audit_report.json"
REPORT_MD = ROOT / "scripts" / "PERFORMANCE_AUDIT_REPORT.md"

PAGES = [
    ("/", "Home"),
    ("/T3AF/Index", "AI Foundation"),
    ("/AllTemplates/Index", "Templates"),
    ("/AllExtensions/Index", "Extensions"),
    ("/License/Index", "License"),
    ("/ExtNsT3AA/Index", "T3AA Hub"),
    ("/ExtNsT3AA/Screenshots/Index", "T3AA Screenshots"),
    ("/ExtNsT3AA/SystemRequirements/Index", "T3AA System Req"),
    ("/ExtNsT3AI/Index", "T3AI Hub"),
    ("/EXTKarma/Index", "T3 Karma Template"),
]

SPA_HOPS = [
    ("/ExtNsT3AA/Index", "/ExtNsT3AA/Screenshots/Index"),
    ("/ExtNsT3AA/Screenshots/Index", "/ExtNsT3AA/SystemRequirements/Index"),
    ("/ExtNsT3AA/SystemRequirements/Index", "/ExtNsT3AA/Installation/Index"),
]


@dataclass
class PageMetrics:
    path: str
    label: str
    dom_ms: int
    load_ms: int | None
    lcp_ms: int | None
    cls: float | None
    sidebar_links: int
    images: int
    scripts_kb: float
    transfer_kb: float
    errors: list[str]


def run_audit(base: str) -> dict[str, Any]:
    from playwright.sync_api import sync_playwright

    results: list[dict[str, Any]] = []
    spa_results: list[dict[str, Any]] = []
    console_errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)

        for path, label in PAGES:
            errors: list[str] = []
            t0 = time.perf_counter()
            try:
                page.goto(base + path, wait_until="domcontentloaded", timeout=120000)
            except Exception as exc:
                errors.append(str(exc))
                results.append(asdict(PageMetrics(path, label, -1, None, None, None, 0, 0, 0, 0, errors)))
                continue
            dom_ms = int((time.perf_counter() - t0) * 1000)

            load_ms = None
            t1 = time.perf_counter()
            try:
                page.wait_for_load_state("load", timeout=15000)
                load_ms = int((time.perf_counter() - t1) * 1000)
            except Exception:
                pass

            vitals = page.evaluate(
                """() => {
                  const nav = performance.getEntriesByType('navigation')[0];
                  let lcp = null;
                  try {
                    const l = performance.getEntriesByType('largest-contentful-paint');
                    if (l.length) lcp = l[l.length - 1].startTime;
                  } catch (e) {}
                  let cls = 0;
                  try {
                    for (const e of performance.getEntriesByType('layout-shift')) {
                      if (!e.hadRecentInput) cls += e.value;
                    }
                  } catch (e) {}
                  const resources = performance.getEntriesByType('resource');
                  const transfer = resources.reduce((s, r) => s + (r.transferSize || 0), 0);
                  const scripts = resources.filter(r => r.initiatorType === 'script').reduce((s, r) => s + (r.transferSize || 0), 0);
                  return {
                    sidebarLinks: document.querySelectorAll('#sidebar-content a[href^="/"]').length,
                    images: document.querySelectorAll('img').length,
                    transfer,
                    scripts,
                    lcp,
                    cls,
                    ttfb: nav ? nav.responseStart : null,
                  };
                }"""
            )

            results.append(
                asdict(
                    PageMetrics(
                        path=path,
                        label=label,
                        dom_ms=dom_ms,
                        load_ms=load_ms,
                        lcp_ms=int(vitals["lcp"]) if vitals.get("lcp") else None,
                        cls=round(vitals.get("cls") or 0, 4),
                        sidebar_links=vitals.get("sidebarLinks", 0),
                        images=vitals.get("images", 0),
                        scripts_kb=round((vitals.get("scripts") or 0) / 1024, 1),
                        transfer_kb=round((vitals.get("transfer") or 0) / 1024, 1),
                        errors=errors,
                    )
                )
            )
            time.sleep(0.3)

        # Warm SPA navigation — measure until content paints, not just URL change
        page.goto(base + SPA_HOPS[0][0], wait_until="domcontentloaded", timeout=120000)
        time.sleep(2)
        for src, dst in SPA_HOPS:
            page.goto(base + src, wait_until="domcontentloaded", timeout=120000)
            time.sleep(0.5)
            dst_clean = dst.rstrip("/")
            dst_html = dst if dst.endswith(".html") else dst + ".html"
            loc = page.locator(
                f'#sidebar-content a[href="{dst}"], #sidebar-content a[href="{dst_html}"]'
            ).first
            if not loc.count():
                spa_results.append({"from": src, "to": dst, "ms": None, "error": "link missing"})
                continue
            t0 = time.perf_counter()
            loc.click()
            try:
                page.wait_for_function(
                    f"""() => {{
                      const p = location.pathname.replace(/\\/$/, '');
                      const want = '{dst_clean}';
                      if (p !== want && p !== want + '.html') return false;
                      const root = document.getElementById('content-area') || document.getElementById('content');
                      if (!root) return true;
                      return !!(root.querySelector('h1') || root.querySelector('[data-component-part="content"] h1'));
                    }}""",
                    timeout=90000,
                )
                spa_results.append({"from": src, "to": dst, "ms": int((time.perf_counter() - t0) * 1000)})
            except Exception as exc:
                spa_results.append({"from": src, "to": dst, "ms": int((time.perf_counter() - t0) * 1000), "error": str(exc)})

        # Mobile viewport sample
        mobile = context.new_page()
        mobile.set_viewport_size({"width": 390, "height": 844})
        t0 = time.perf_counter()
        mobile.goto(base + "/", wait_until="domcontentloaded", timeout=120000)
        mobile_dom = int((time.perf_counter() - t0) * 1000)

        browser.close()

    dom_times = [r["dom_ms"] for r in results if r["dom_ms"] > 0]
    spa_times = [r["ms"] for r in spa_results if r.get("ms")]

    summary = {
        "base_url": base,
        "pages_tested": len(results),
        "dom_ms_median": int(statistics.median(dom_times)) if dom_times else None,
        "dom_ms_max": max(dom_times) if dom_times else None,
        "spa_ms_median": int(statistics.median(spa_times)) if spa_times else None,
        "spa_ms_max": max(spa_times) if spa_times else None,
        "mobile_home_dom_ms": mobile_dom,
        "console_error_count": len(console_errors),
    }

    payload = {
        "summary": summary,
        "pages": results,
        "spa_navigation": spa_results,
        "console_errors_sample": console_errors[:20],
    }
    return payload


def write_markdown(data: dict[str, Any]) -> None:
    s = data["summary"]
    lines = [
        "# T3Planet Docs — Performance Audit Report",
        "",
        f"**Base URL:** {s['base_url']}",
        f"**Pages tested:** {s['pages_tested']}",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Median DOM ready (cold) | {s.get('dom_ms_median')} ms |",
        f"| Max DOM ready (cold) | {s.get('dom_ms_max')} ms |",
        f"| Median SPA navigation (warm) | {s.get('spa_ms_median')} ms |",
        f"| Max SPA navigation (warm) | {s.get('spa_ms_max')} ms |",
        f"| Mobile home DOM ready | {s.get('mobile_home_dom_ms')} ms |",
        f"| Console errors (sample) | {s.get('console_error_count')} |",
        "",
        "## Page Results",
        "",
        "| Page | DOM (ms) | Load (ms) | LCP (ms) | CLS | Transfer (KB) | Sidebar links |",
        "|------|----------|-----------|----------|-----|---------------|---------------|",
    ]
    for p in data["pages"]:
        lines.append(
            f"| {p['label']} | {p['dom_ms']} | {p.get('load_ms') or '—'} | {p.get('lcp_ms') or '—'} | {p.get('cls') or '—'} | {p.get('transfer_kb')} | {p.get('sidebar_links')} |"
        )
    lines += ["", "## SPA Navigation (warm)", "", "| From → To | ms |", "|-----------|-----|"]
    for hop in data["spa_navigation"]:
        lines.append(f"| {hop.get('from')} → {hop.get('to')} | {hop.get('ms', '—')} |")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3338"
    data = run_audit(base)
    REPORT_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")
    write_markdown(data)
    print(json.dumps(data["summary"], indent=2))
    print(f"Wrote {REPORT_JSON} and {REPORT_MD}")


if __name__ == "__main__":
    main()
