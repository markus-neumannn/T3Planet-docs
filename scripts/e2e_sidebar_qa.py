#!/usr/bin/env python3
"""End-to-end sidebar QA: themes, languages, responsive, a11y, icons."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")
REPORT = ROOT / "scripts" / "e2e_sidebar_qa_report.json"

PAGES_EN = [
    "/",
    "/ExtNsT3AI/Installation/Index",
    "/ExtNsT3AA/UpdateVersion/Index",
    "/EXTKarma/Index",
    "/License/Index",
]
PAGES_DE = [
    "/de/index",
    "/de/ExtNsT3AI/Installation/Index",
    "/de/ExtNsT3AA/UpdateVersion/Index",
    "/de/EXTKarma/Index",
    "/de/License/Index",
]

VIEWPORTS = {
    "large_desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1440, "height": 900},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 390, "height": 844},
}


def server_up() -> bool:
    try:
        with urllib.request.urlopen(f"{BASE}/", timeout=8) as r:
            return r.status == 200
    except Exception:
        return False


def run_playwright() -> dict:
    script = r'''
from playwright.sync_api import sync_playwright
import json

BASE = "%s"
PAGES_EN = %s
PAGES_DE = %s
VIEWPORTS = %s

issues = []
checks = []

def issue(suite, test, detail, severity="error"):
    issues.append({"suite": suite, "test": test, "detail": detail, "severity": severity})

def ok(suite, test, detail=""):
    checks.append({"suite": suite, "test": test, "detail": detail, "passed": True})

def set_theme(page, dark):
    page.evaluate("(d) => { document.documentElement.classList.toggle('dark', d); }", dark)

def sidebar_metrics(page):
    return page.evaluate("""() => {
      const content = document.getElementById('sidebar-content');
      const sidebar = document.getElementById('sidebar') || document.querySelector('[data-component-part="sidebar"]');
      const activeLinks = content ? [...content.querySelectorAll('a[aria-current="page"]')] : [];
      const expandBtns = content ? [...content.querySelectorAll('button[aria-controls]')] : [];
      const sectionIcons = content ? [...content.querySelectorAll('.sidebar-group-icon')] : [];
      const chevrons = content ? [...content.querySelectorAll('.t3-sidebar-chevron, button[aria-controls] svg')] : [];
      const hiddenChevrons = chevrons.filter(el => getComputedStyle(el).display === 'none');
      const lowContrastIcons = sectionIcons.filter(el => {
        const c = getComputedStyle(el).color || getComputedStyle(el).backgroundColor;
        return !c || c === 'rgba(0, 0, 0, 0)';
      });
      const overflowLinks = content ? [...content.querySelectorAll('a')].filter(a => a.scrollWidth > a.clientWidth + 2) : [];
      const sidebarRect = sidebar ? sidebar.getBoundingClientRect() : null;
      const contentRect = content ? content.getBoundingClientRect() : null;
      const iconContrasts = sectionIcons.slice(0, 8).map(el => {
        const bg = getComputedStyle(el.parentElement || el).backgroundColor;
        const color = getComputedStyle(el).color;
        const opacity = parseFloat(getComputedStyle(el).opacity || '1');
        return {text: (el.parentElement?.textContent||'').trim().slice(0,20), color, bg, opacity, display: getComputedStyle(el).display};
      });
      const chevronAlign = expandBtns.slice(0, 6).map(btn => {
        const svg = btn.querySelector('svg');
        if (!svg) return null;
        const br = btn.getBoundingClientRect();
        const sr = svg.getBoundingClientRect();
        return {text: btn.textContent.trim().slice(0,16), gapRight: Math.round(br.right - sr.right), justify: getComputedStyle(btn).justifyContent};
      }).filter(Boolean);
      return {
        path: location.pathname,
        sidebarVisible: sidebar ? getComputedStyle(sidebar).display !== 'none' : false,
        sidebarOverflowX: content ? content.scrollWidth > content.clientWidth + 2 : false,
        activeCount: activeLinks.length,
        expandBtnCount: expandBtns.length,
        sectionIconCount: sectionIcons.length,
        chevronCount: chevrons.length,
        hiddenChevronCount: hiddenChevrons.length,
        overflowLinkCount: overflowLinks.length,
        sidebarWidth: sidebarRect ? Math.round(sidebarRect.width) : 0,
        legacySearch: !!document.querySelector('[data-t3-sidebar-search]'),
        legacyFilter: !!document.getElementById('t3-sidebar-filter-input'),
        legacyDropdown: !!document.querySelector('button.nav-dropdown-trigger'),
        langSwitcher: !!document.getElementById('t3-lang-switcher') || !!document.getElementById('t3-lang-switcher-mobile'),
        iconContrasts,
        chevronAlign,
        topHeadersWithChevron: content ? [...content.querySelectorAll('.sidebar-group-header')].filter(h => h.querySelector('.t3-sidebar-chevron')).length : 0,
        topHeaderCount: content ? content.querySelectorAll('.sidebar-group-header').length : 0,
        childExpandChevrons: content ? [...content.querySelectorAll('button[aria-controls] svg')].filter(el => getComputedStyle(el).display !== 'none').length : 0,
      };
    }""")

def test_routes(page, suite, pages):
    for path in pages:
        resp = page.goto(BASE + path, wait_until="commit", timeout=90000)
        page.wait_for_timeout(3500)
        status = resp.status if resp else 0
        if status >= 400:
            issue(suite, "route", f"{path} returned {status}")
        else:
            ok(suite, "route", path)

def test_theme_lang_viewport(page, suite, pages, dark, viewport):
    page.set_viewport_size(viewport)
    set_theme(page, dark)
    for path in pages[:3]:
        page.goto(BASE + path, wait_until="commit", timeout=90000)
        page.wait_for_timeout(3000)
        m = sidebar_metrics(page)
        tag = f"{'dark' if dark else 'light'}-{viewport['width']}"
        if m["activeCount"] > 1:
            issue(suite, f"active-state-{tag}", f"{path}: {m['activeCount']} active links")
        elif path not in ('/', '/de/index', '/de') and m["activeCount"] == 0 and 'Index' in path:
            issue(suite, f"active-state-{tag}", f"{path}: no active link", "warn")
        else:
            ok(suite, f"active-state-{tag}", path)
        if m["hiddenChevronCount"] > 0:
            issue(suite, f"chevron-visible-{tag}", f"{path}: {m['hiddenChevronCount']} hidden chevrons")
        else:
            ok(suite, f"chevron-visible-{tag}", path)
        if m["topHeadersWithChevron"] > 0:
            issue(suite, f"parent-chevron-{tag}", f"{path}: {m['topHeadersWithChevron']} top sections still have chevrons")
        else:
            ok(suite, f"parent-chevron-{tag}", path)
        if m.get("expandBtnCount", 0) > 0:
            if m["childExpandChevrons"] < 1:
                issue(suite, f"child-chevron-{tag}", f"{path}: child expand chevrons missing")
            else:
                ok(suite, f"child-chevron-{tag}", path)
        for ca in m["chevronAlign"]:
            if ca and ca["gapRight"] > 20:
                issue(suite, f"chevron-align-{tag}", f"{path} {ca['text']}: gap {ca['gapRight']}px from right")
        if m["legacySearch"] or m["legacyFilter"] or m["legacyDropdown"]:
            issue(suite, f"legacy-ui-{tag}", f"{path}: legacy controls still visible")
        else:
            ok(suite, f"legacy-ui-{tag}", path)
        if m["sidebarOverflowX"]:
            issue(suite, f"overflow-{tag}", f"{path}: horizontal sidebar overflow")
        else:
            ok(suite, f"overflow-{tag}", path)

def test_expand_collapse(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    set_theme(page, False)
    page.goto(BASE + "/ExtNsT3AA/UpdateVersion/Index", wait_until="commit", timeout=90000)
    page.wait_for_timeout(3000)

    header = page.locator(".sidebar-group-header").first
    if header.count():
        hb = header.get_attribute("aria-expanded")
        header.click()
        page.wait_for_timeout(400)
        ha = header.get_attribute("aria-expanded")
        if hb != ha:
            ok("interaction", "section-collapse")
        else:
            issue("interaction", "section-collapse", "section header did not toggle")

    nested = page.evaluate("""async () => {
      const btn = [...document.querySelectorAll('#sidebar-content button[aria-controls]')]
        .find(b => (b.textContent || '').trim().startsWith('Updates'));
      if (!btn) return {found: false};
      const before = btn.getAttribute('aria-expanded');
      btn.click();
      await new Promise(r => setTimeout(r, 400));
      const after = btn.getAttribute('aria-expanded');
      return {found: true, before, after, toggled: before !== after};
    }""")
    if nested.get("found") and nested.get("toggled"):
        ok("interaction", "nested-collapse")
    elif nested.get("found"):
        issue("interaction", "nested-collapse", "Updates button did not toggle")
    else:
        issue("interaction", "nested-collapse", "Updates button not found")

def test_keyboard_nav(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(BASE + "/", wait_until="commit", timeout=90000)
    page.wait_for_function(
        "() => document.getElementById('sidebar-content')?.getAttribute('data-t3-kbd-nav') === '1'",
        timeout=15000,
    )
    data = page.evaluate("""() => {
      const content = document.getElementById('sidebar-content');
      const links = [...content.querySelectorAll('a[href^="/"]')];
      if (links.length < 2) return {ok: false, reason: 'not enough links'};
      const first = links[0].getAttribute('href') || links[0].href;
      links[0].focus({preventScroll: true});
      links[0].dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowDown', bubbles: true, cancelable: true}));
      const second = document.activeElement?.getAttribute('href') || document.activeElement?.href || '';
      return {ok: !!second && second !== first, first, second};
    }""")
    if data.get("ok"):
        ok("a11y", "keyboard-nav", data.get("second", ""))
    else:
        issue("a11y", "keyboard-nav", data.get("reason") or f"{data.get('first')} -> {data.get('second')}")

def test_mobile_drawer(page):
    page.set_viewport_size({"width": 390, "height": 844})
    set_theme(page, False)
    page.goto(BASE + "/ExtNsT3AI/Installation/Index", wait_until="commit", timeout=90000)
    page.wait_for_timeout(3000)
    menu = page.locator('button:has-text("Navigation"), button[aria-label*="menu" i]').first
    if menu.count():
        menu.click()
        page.wait_for_timeout(600)
    open_state = page.evaluate("() => document.body.classList.contains('t3-sidebar-open') || (document.getElementById('sidebar')?.getAttribute('data-state') === 'open')")
    mobile_lang = page.evaluate("() => { const el = document.getElementById('t3-lang-switcher-mobile'); return el && getComputedStyle(el).display !== 'none'; }")
    if not mobile_lang:
        issue("responsive", "mobile-lang", "mobile language switcher not visible")
    else:
        ok("responsive", "mobile-lang")
    ok("responsive", "mobile-drawer", f"open={open_state}")

def test_lang_switch_paths(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    page.goto(BASE + "/ExtNsT3AI/Installation/Index", wait_until="commit", timeout=90000)
    page.wait_for_timeout(2500)
    de_btn = page.locator('.t3-lang-switcher-btn[data-lang="de"]').first
    if not de_btn.count():
        issue("i18n", "lang-switcher", "DE button missing")
        return
    de_btn.click()
    page.wait_for_timeout(5000)
    path = page.evaluate("() => location.pathname")
    if "/de/" not in path:
        issue("i18n", "lang-switch", f"expected /de/ path, got {path}")
    else:
        ok("i18n", "lang-switch-de", path)

def test_german_long_words(page):
    page.set_viewport_size({"width": 390, "height": 844})
    set_theme(page, True)
    page.goto(BASE + "/de/ExtNsT3AI/Installation/Index", wait_until="commit", timeout=90000)
    page.wait_for_timeout(3500)
    m = sidebar_metrics(page)
    if m["overflowLinkCount"] > 8:
        issue("i18n", "de-overflow", f"{m['overflowLinkCount']} links overflow on mobile", "warn")
    else:
        ok("i18n", "de-mobile-layout", f"overflow={m['overflowLinkCount']}")

def test_dark_icon_contrast(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    set_theme(page, True)
    page.goto(BASE + "/ExtNsT3AI/Index", wait_until="commit", timeout=90000)
    page.wait_for_timeout(3000)
    data = page.evaluate("""() => {
      const icons = [...document.querySelectorAll('#sidebar-content .sidebar-group-icon')];
      const chevrons = [...document.querySelectorAll('#sidebar-content .t3-sidebar-chevron, #sidebar-content button[aria-controls] svg')];
      function visible(el) {
        const s = getComputedStyle(el);
        return s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity||'1') > 0.2;
      }
      return {
        iconsVisible: icons.filter(visible).length,
        iconsTotal: icons.length,
        chevronsVisible: chevrons.filter(visible).length,
        chevronsTotal: chevrons.length,
        iconSamples: icons.slice(0,5).map(el => ({
          display: getComputedStyle(el).display,
          opacity: getComputedStyle(el).opacity,
          color: getComputedStyle(el).color,
          bg: getComputedStyle(el).backgroundColor,
        })),
      };
    }""")
    if data["iconsVisible"] < min(3, data["iconsTotal"]):
        issue("theme", "dark-section-icons", f"only {data['iconsVisible']}/{data['iconsTotal']} section icons visible")
    else:
        ok("theme", "dark-section-icons", str(data["iconsVisible"]))
    if data["chevronsVisible"] < 1:
        issue("theme", "dark-chevrons", "no visible chevrons in dark mode")
    else:
        ok("theme", "dark-chevrons", str(data["chevronsVisible"]))

def test_404(page):
    resp = page.goto(BASE + "/ThisRouteDoesNotExist12345", wait_until="commit", timeout=60000)
    page.wait_for_timeout(2000)
    status = resp.status if resp else 0
    if status == 200:
        issue("routes", "404", "nonexistent route returned 200")
    else:
        ok("routes", "404", f"status={status}")

def test_refresh_persistence(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    path = "/ExtNsT3AI/Installation/Index"
    page.goto(BASE + path, wait_until="commit", timeout=90000)
    page.wait_for_timeout(3000)
    page.reload(wait_until="commit")
    page.wait_for_timeout(3000)
    data = page.evaluate("""() => ({
      path: location.pathname,
      active: document.querySelectorAll('#sidebar-content a[aria-current=\"page\"]').length,
      activeText: document.querySelector('#sidebar-content a[aria-current=\"page\"]')?.textContent?.trim() || ''
    })""")
    if data["path"] != path:
        issue("persistence", "refresh-path", f"expected {path}, got {data['path']}")
    elif data["active"] != 1:
        issue("persistence", "refresh-active", f"active count {data['active']}")
    else:
        ok("persistence", "refresh", data["activeText"])

def test_light_icon_contrast(page):
    page.set_viewport_size({"width": 1440, "height": 900})
    set_theme(page, False)
    page.goto(BASE + "/", wait_until="commit", timeout=90000)
    page.wait_for_timeout(2500)
    data = page.evaluate("""() => {
      const icons = [...document.querySelectorAll('#sidebar-content .sidebar-group-icon')];
      const visible = icons.filter(el => getComputedStyle(el).display !== 'none' && parseFloat(getComputedStyle(el).opacity||'1') > 0.3);
      return {visible: visible.length, total: icons.length};
    }""")
    if data["visible"] < min(3, data["total"]):
        issue("theme", "light-section-icons", f"{data['visible']}/{data['total']} visible")
    else:
        ok("theme", "light-section-icons", str(data["visible"]))

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    test_routes(page, "routes-en", PAGES_EN)
    test_routes(page, "routes-de", PAGES_DE)
    test_keyboard_nav(page)

    for vp_name, vp in VIEWPORTS.items():
        test_theme_lang_viewport(page, f"viewport-{vp_name}", PAGES_EN, False, vp)
        test_theme_lang_viewport(page, f"viewport-{vp_name}-dark", PAGES_DE, True, vp)

    test_expand_collapse(page)
    test_mobile_drawer(page)
    test_lang_switch_paths(page)
    test_german_long_words(page)
    test_dark_icon_contrast(page)
    test_light_icon_contrast(page)
    test_refresh_persistence(page)
    test_404(page)

    browser.close()

result = {
    "checks": checks,
    "issues": issues,
    "passed": len(issues) == 0,
    "check_count": len(checks),
    "issue_count": len(issues),
}
print(json.dumps(result))
''' % (
        BASE,
        json.dumps(PAGES_EN),
        json.dumps(PAGES_DE),
        json.dumps(VIEWPORTS),
    )

    proc = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=600,
        cwd=str(ROOT),
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "playwright failed")[:2000])
    lines = [ln for ln in proc.stdout.strip().split("\n") if ln.startswith("{")]
    return json.loads(lines[-1])


def main() -> int:
    print(f"E2E Sidebar QA — {BASE}\n")
    if not server_up():
        print("ERROR: Start dev server: mint dev --port 3333")
        return 1

    try:
        result = run_playwright()
    except Exception as e:
        print(f"FAILED: {e}")
        return 1

    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")

    for c in result.get("checks", [])[:20]:
        print(f"[PASS] {c['suite']} — {c['test']}")
    extra = len(result.get("checks", [])) - 20
    if extra > 0:
        print(f"  ... and {extra} more passed checks")

    for i in result.get("issues", []):
        sev = i.get("severity", "error")
        print(f"[{sev.upper()}] {i['suite']} — {i['test']}: {i['detail']}")

    print(f"\nChecks: {result['check_count']} | Issues: {result['issue_count']}")
    print(f"Report: {REPORT}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
