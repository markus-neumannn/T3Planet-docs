#!/usr/bin/env python3
"""Responsive dark-mode contrast check at multiple viewport sizes."""
import json
import os
import sys

BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")
REPORT = os.path.join(os.path.dirname(__file__), "dark_mode_responsive_report.json")

VIEWPORTS = [
    ("mobile", 390, 844),
    ("tablet", 768, 1024),
    ("laptop", 1280, 800),
    ("desktop", 1920, 1080),
]

SAMPLE_PATHS = [
    "/",
    "/ExtNsWhatsapp/Installation/Index",
    "/EXTKarma/Customization/Index",
    "/ExtNsT3AI/AISettings/Index",
    "/de/",
    "/de/ExtNsWhatsapp/Installation/Index",
]

JS_CHECK = """
() => {
  const parseRgb = (c) => {
    const m = c.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
    return m ? [+m[1], +m[2], +m[3]] : null;
  };
  const lum = ([r,g,b]) => {
    const f = v => { v/=255; return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4); };
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);
  };
  const ratio = (fg, bg) => {
    const l1=lum(fg), l2=lum(bg);
    return (Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05);
  };
  const bg = parseRgb(getComputedStyle(document.body).backgroundColor) || [20,18,14];
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    return r.width > 2 && r.height > 2;
  };
  const issues = [];
  const sels = ['#content h1','#content h2','#content h3','#page-title','#pagination a','#footer a'];
  for (const sel of sels) {
    for (const el of document.querySelectorAll(sel)) {
      const t = (el.textContent||'').replace(/\\u200b/g,'').trim();
      if (!t || !visible(el)) continue;
      const fg = parseRgb(getComputedStyle(el).color);
      if (fg && ratio(fg, bg) < 4.5) {
        issues.push({ tag: el.tagName, text: t.slice(0,40), ratio: ratio(fg,bg).toFixed(2) });
      }
    }
  }
  return {
    issues,
    sidebarVisible: !!document.querySelector('#sidebar-content'),
    menuBtn: [...document.querySelectorAll('button')].some(b => b.className.includes('lg:hidden')),
  };
}
"""


def main():
    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for vp_name, w, h in VIEWPORTS:
            page = browser.new_page(viewport={"width": w, "height": h})
            page.add_init_script(
                "localStorage.setItem('mintlify-color-scheme', 'dark');"
            )
            for path in SAMPLE_PATHS:
                page.goto(BASE + path, wait_until="domcontentloaded", timeout=45000)
                page.wait_for_timeout(600)
                page.evaluate(
                    """() => {
                      localStorage.setItem('mintlify-color-scheme', 'dark');
                      document.documentElement.classList.add('dark');
                    }"""
                )
                page.wait_for_timeout(800)
                data = page.evaluate(JS_CHECK)
                results.append({
                    "viewport": vp_name,
                    "size": f"{w}x{h}",
                    "path": path,
                    "issues": data["issues"],
                    "sidebarVisible": data["sidebarVisible"],
                    "menuBtn": data["menuBtn"],
                })
        browser.close()

    failures = [r for r in results if r["issues"]]
    report = {
        "summary": {
            "total_checks": len(results),
            "failed": len(failures),
            "passed": len(results) - len(failures),
            "failures": failures,
        },
        "results": results,
    }
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report["summary"], indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
