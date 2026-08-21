#!/usr/bin/env python3
"""Navigation fix regression — video scenario + nested product pages."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
RESULTS = []


def log(*a):
    print(*a, flush=True)


def record(name, ok, detail=""):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": str(detail)[:240]})
    log(("PASS" if ok else "FAIL"), name, detail)


def wait_nav(page, substr, timeout=12):
    t0 = time.time()
    last = ("?", {})
    while time.time() - t0 < timeout:
        try:
            u = page.url
            st = page.evaluate(
                """() => ({
              holding: document.documentElement.classList.contains('t3-holding'),
              text: (document.body.innerText||'').trim().length,
              h1: (document.querySelector('h1')||{}).innerText||'',
              qs: location.search
            })"""
            )
            last = (u, st)
            if substr in u and st["text"] > 80 and not st["holding"]:
                return True, u, st
        except Exception:
            pass
        page.wait_for_timeout(150)
    return False, last[0], last[1]


def click_href(page, href):
    for sel in (f'a[href="{href}"]:visible', f'a[href="{href}"]'):
        loc = page.locator(sel).first
        try:
            if loc.count() == 0:
                continue
            loc.scroll_into_view_if_needed(timeout=3000)
            loc.click(no_wait_after=True, timeout=5000)
            return True
        except Exception:
            continue
    return False


def expand(page, label):
    loc = page.locator(f'button[aria-expanded]:has-text("{label}")').first
    try:
        if loc.count() == 0:
            return False
        if loc.get_attribute("aria-expanded") == "true":
            return True
        loc.scroll_into_view_if_needed(timeout=3000)
        loc.click(no_wait_after=True, timeout=5000)
        page.wait_for_timeout(350)
        return loc.get_attribute("aria-expanded") == "true"
    except Exception:
        return False


def run_port(port: int):
    log(f"\n======== PORT {port} ========")
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        base = f"http://127.0.0.1:{port}"

        def go(path):
            page.goto(base + path, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(600)

        go("/ExtNsT3AF/Index")
        page.wait_for_timeout(900)
        ok = click_href(page, "/ExtNsT3AF/Introduction/Index")
        ok2, u, st = wait_nav(page, "Introduction")
        record(f"{port} video T3AF→Introduction", ok and ok2, f"{u} h1={st.get('h1')}")

        go("/ExtNsT3AF/Index")
        page.wait_for_timeout(350)
        ok = click_href(page, "/ExtNsT3AF/Installation/Index")
        ok2, u, st = wait_nav(page, "Installation")
        record(f"{port} early-click→Installation", ok and ok2 and "_t3r" not in u, u)

        go("/ExtNsT3AF/Index")
        box = page.locator('a[href="/ExtNsT3AF/HelpfulLinks/Index"]').first.bounding_box()
        page.mouse.move(box["x"] + 8, box["y"] + 8)
        page.mouse.down()
        page.wait_for_timeout(150)
        holding = page.evaluate("document.documentElement.classList.contains('t3-holding')")
        page.mouse.up()
        ok2, u, st = wait_nav(page, "HelpfulLinks")
        record(
            f"{port} pointerdown-race→HelpfulLinks",
            ok2 and (port != 3001 or holding is False),
            f"preHold={holding} {u}",
        )

        go("/ExtNsT3AF/Index")
        exp = expand(page, "Configuration")
        record(f"{port} expand Configuration", exp)
        ok = click_href(page, "/ExtNsT3AF/Configuration/AIProviders/Index")
        ok2, u, st = wait_nav(page, "AIProviders")
        record(f"{port} sub-sub AIProviders", ok and ok2, f"{u} h1={st.get('h1')}")

        go("/ExtNsT3AF/Index")
        exp = expand(page, "T3Planet Credits")
        record(f"{port} expand Credits", exp)
        ok = click_href(page, "/ExtNsT3AF/T3Planet-Credit-System/Overview/Index")
        ok2, u, st = wait_nav(page, "Overview")
        record(f"{port} sub-sub Credits Overview", ok and ok2, u)

        go("/ExtNsT3AF/Index")
        expand(page, "Integrations")
        ok = click_href(page, "/ExtNsT3AF/Integrations/MCPServer/Index")
        ok2, u, _ = wait_nav(page, "MCPServer")
        record(f"{port} sub-sub MCPServer", ok and ok2, u)

        cases = [
            ("/ExtThemes/Index", "/ExtThemes/Introduction/Index", "ExtThemes Intro"),
            ("/EXTKarma/Index", "/EXTKarma/Installation/Index", "EXTKarma Install"),
            ("/EXTAvatar/Index", "/EXTAvatar/EditorGuide/Index", "EXTAvatar Editor"),
            ("/ExtNsT3AI/Index", "/ExtNsT3AI/Content/Index", "T3AI Content"),
            ("/License/Index", "/License/LicenseActivation/Index", "License Activation"),
        ]
        for hub, target, label in cases:
            go(hub)
            ok = click_href(page, target)
            if not ok:
                page.evaluate(
                    """() => {
                  document.querySelectorAll('button[aria-expanded=\"false\"]').forEach((b) => {
                    const t = (b.innerText || '').trim();
                    if (t && t.length < 48) b.click();
                  });
                }"""
                )
                page.wait_for_timeout(300)
                ok = click_href(page, target)
            ok2, u, _ = wait_nav(page, target)
            record(f"{port} {label}", ok and ok2, u)

        go("/ExtNsT3AF/Configuration/AIFeatures/Index")
        st = page.evaluate(
            '() => ({t:(document.body.innerText||"").trim().length,h1:(document.querySelector("h1")||{}).innerText||""})'
        )
        record(f"{port} direct deep AIFeatures", st["t"] > 80, st)
        page.reload(wait_until="domcontentloaded")
        page.wait_for_timeout(500)
        st = page.evaluate(
            '() => ({t:(document.body.innerText||"").trim().length,u:location.pathname,h1:(document.querySelector("h1")||{}).innerText||""})'
        )
        record(f"{port} refresh deep AIFeatures", st["t"] > 80 and "AIFeatures" in st["u"], st)

        go("/ExtNsT3AF/Introduction/Index")
        go("/ExtNsT3AF/Support/Index")
        page.go_back()
        page.wait_for_timeout(800)
        record(f"{port} back", "Introduction" in page.url, page.url)
        page.go_forward()
        page.wait_for_timeout(800)
        record(f"{port} forward", "Support" in page.url, page.url)

        page.set_viewport_size({"width": 390, "height": 844})
        go("/ExtNsT3AF/Index")
        ham = page.locator('button[aria-label*="Open" i], button[aria-label*="menu" i]').first
        try:
            if ham.count() and ham.is_visible():
                ham.click()
                page.wait_for_timeout(400)
        except Exception:
            pass
        ok = click_href(page, "/ExtNsT3AF/Support/Index")
        ok2, u, _ = wait_nav(page, "Support")
        record(f"{port} mobile→Support", ok and ok2, u)

        page.set_viewport_size({"width": 768, "height": 1024})
        go("/ExtThemes/Index")
        try:
            if ham.count() and ham.is_visible():
                ham.click()
                page.wait_for_timeout(400)
        except Exception:
            pass
        ok = click_href(page, "/ExtThemes/Installation/Index")
        ok2, u, _ = wait_nav(page, "ExtThemes/Installation")
        record(f"{port} tablet ExtThemes→Install", ok and ok2, u)

        browser.close()


def main():
    for port in (3000, 3001):
        try:
            run_port(port)
        except Exception as e:
            record(f"{port} suite error", False, repr(e))
            log("ERR", e)
    failed = [r for r in RESULTS if not r["ok"]]
    log("\n==== SUMMARY ====")
    log("total", len(RESULTS), "pass", len(RESULTS) - len(failed), "fail", len(failed))
    for r in failed:
        log(" FAIL", r["name"], r["detail"])
    out = ROOT / "scripts" / "remigration" / "NAV_FIX_REGRESSION.json"
    out.write_text(
        json.dumps(
            {"results": RESULTS, "failed": failed, "verdict": "PASS" if not failed else "FAIL"},
            indent=2,
        )
    )
    log("wrote", out)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
