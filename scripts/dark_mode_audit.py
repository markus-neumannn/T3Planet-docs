#!/usr/bin/env python3
"""Comprehensive dark-mode contrast audit across all documentation pages."""
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")
REPORT = ROOT / "scripts" / "dark_mode_audit_report.json"

JS_AUDIT = """
() => {
  const parseRgb = (c) => {
    const m = c.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
    if (!m) return null;
    return [+m[1], +m[2], +m[3]];
  };
  const luminance = ([r, g, b]) => {
    const f = (v) => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const contrast = (fg, bg) => {
    const l1 = luminance(fg);
    const l2 = luminance(bg);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
  };
  const getBg = () =>
    parseRgb(getComputedStyle(document.body).backgroundColor) || [20, 18, 14];

  const selectors = [
    { sel: 'h1', min: 4.5, label: 'heading-h1' },
    { sel: 'h2', min: 4.5, label: 'heading-h2' },
    { sel: 'h3', min: 4.5, label: 'heading-h3' },
    { sel: 'h4', min: 4.5, label: 'heading-h4' },
    { sel: '#pagination a', min: 4.5, label: 'pagination' },
    { sel: '#footer a', min: 3.0, label: 'footer-link' },
    { sel: '#footer p', min: 4.5, label: 'footer-text' },
    { sel: '.card [data-component-part="card-title"]', min: 4.5, label: 'card-title' },
    { sel: '#page-title', min: 4.5, label: 'page-title' },
    { sel: 'article p, main p', min: 4.5, label: 'paragraph' },
    { sel: '#table-of-contents-content a', min: 3.0, label: 'toc-link' },
  ];

  const issues = [];
  for (const { sel, min, label } of selectors) {
    const els = [...document.querySelectorAll(sel)].slice(0, 8);
    for (const el of els) {
      const text = (el.textContent || '').replace(/\\u200b/g, '').trim();
      if (!text || text.length < 2) continue;
      const rect = el.getBoundingClientRect();
      if (rect.width < 2 || rect.height < 2) continue;
      const fg = parseRgb(getComputedStyle(el).color);
      if (!fg) continue;
      const bg = getBg();
      const ratio = contrast(fg, bg);
      if (ratio < min) {
        issues.push({
          label,
          tag: el.tagName,
          text: text.slice(0, 60),
          ratio: Math.round(ratio * 100) / 100,
          min,
          fg: getComputedStyle(el).color,
        });
      }
    }
  }
  return { issues, dark: document.documentElement.classList.contains('dark') };
}
"""


def _product_sample_paths() -> list[str]:
    """One page per product dropdown in EN + DE."""
    with open(ROOT / "docs.json", encoding="utf-8") as fh:
        docs = json.load(fh)
    paths = ["/", "/de/"]
    for lang in docs["navigation"]["languages"]:
        prefix = "" if lang["language"] == "en" else "/de"
        for dd in lang.get("dropdowns", []):
            found = None
            for g in dd.get("groups", []):
                for p in g.get("pages", []):
                    if isinstance(p, str):
                        found = p.removesuffix(".md")
                        if found == "index":
                            found = "Index"
                        if not found.startswith("/"):
                            found = "/" + found
                        break
                if found:
                    break
            for p in dd.get("pages", []):
                if isinstance(p, str):
                    found = p.removesuffix(".md")
                    if not found.startswith("/"):
                        found = "/" + found
                    break
            if found:
                route = found if found.startswith("/de") else prefix + found
                if route not in paths:
                    paths.append(route)
    return paths


def collect_paths() -> list[str]:
    paths = set()
    for dp, _, fns in os.walk(ROOT):
        if any(skip in dp for skip in ("scripts", "node_modules", ".git", "_static", ".review")):
            continue
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            rel = Path(dp, fn).relative_to(ROOT)
            parts = list(rel.parts)
            if parts[-1].lower() in ("index.md", "readme.md"):
                parts = parts[:-1]
            route = "/" + "/".join(parts)
            if route == "/":
                continue
            paths.add(route)
            paths.add("/de" + route)
    paths.add("/")
    paths.add("/de/")
    return sorted(paths)


def main():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed", file=sys.stderr)
        sys.exit(1)

    sample_only = "--sample" in sys.argv
    products_only = "--products" in sys.argv
    paths = collect_paths()
    if sample_only:
        paths = [
            "/",
            "/ExtNsWhatsapp/Installation/Index",
            "/EXTKarma/Customization/Index",
            "/ExtNsT3AI/AISettings/Index",
            "/License/UpdateVersion/CheckNewVersion/Index",
            "/de/",
            "/de/ExtNsWhatsapp/Installation/Index",
            "/de/EXTKarma/Customization/Index",
        ]
    elif products_only:
        paths = _product_sample_paths()

    all_issues = []
    failed_pages = []
    total = len(paths)

    def enable_dark(page):
        page.evaluate(
            """() => {
              localStorage.setItem('mintlify-color-scheme', 'dark');
              document.documentElement.classList.add('dark');
            }"""
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.add_init_script(
            "localStorage.setItem('mintlify-color-scheme', 'dark');"
        )

        for i, path in enumerate(paths, 1):
            url = BASE + path
            try:
                page.set_default_timeout(12000)
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=12000)
                except Exception:
                    page.goto(url, wait_until="commit", timeout=8000)
                page.wait_for_timeout(600)
                enable_dark(page)
                page.wait_for_timeout(800)
                result = page.evaluate(JS_AUDIT)
                if result.get("issues"):
                    for issue in result["issues"]:
                        issue["path"] = path
                        all_issues.append(issue)
            except Exception as e:
                failed_pages.append({"path": path, "error": str(e)})

            if i % 50 == 0 or i == total:
                print(
                    f"[audit] {i}/{total} checked, issues={len(all_issues)}, failed={len(failed_pages)}",
                    flush=True,
                )

        browser.close()

    report = {
        "summary": {
            "total_pages": total,
            "issue_count": len(all_issues),
            "failed_pages": len(failed_pages),
            "unique_issue_types": len({i["label"] for i in all_issues}),
        },
        "issues": all_issues[:200],
        "failed_pages": failed_pages[:50],
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    if all_issues:
        by_label = {}
        for issue in all_issues:
            by_label.setdefault(issue["label"], 0)
            by_label[issue["label"]] += 1
        print("By type:", json.dumps(by_label, indent=2))
    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
