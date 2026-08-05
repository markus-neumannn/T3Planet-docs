#!/usr/bin/env python3
"""Verify every product has a visible active icon in light and dark mode."""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"
BASE = "http://localhost:3333"


def get_products():
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    products = []
    for lang in data["navigation"]["languages"]:
        if lang["language"] != "en":
            continue
        for dd in lang["dropdowns"]:
            page = dd.get("pages", [None])[0]
            if not page and dd.get("groups"):
                page = dd["groups"][0]["pages"][0]
            products.append({
                "name": dd["dropdown"],
                "icon": dd.get("icon", ""),
                "page": "/" + page.replace("index", "index") if page else "/",
            })
    return products


def audit_product(page, product, dark: bool) -> dict:
    path = product["page"] if product["page"] != "/index" else "/"
    page.goto(BASE + path, wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(1000)
    page.evaluate(
        f"() => {{ document.documentElement.classList.toggle('dark', {str(dark).lower()}); }}"
    )
    page.wait_for_timeout(400)
    try:
        page.locator("button.nav-dropdown-trigger").click(timeout=8000)
    except Exception:
        return {"ok": False, "error": "dropdown trigger not found"}
    page.wait_for_timeout(500)
    result = page.evaluate(
        """() => {
        const active = document.querySelector('a.nav-dropdown-item[aria-current="location"]');
        const icon = active?.querySelector('.nav-dropdown-item-icon');
        const svg = icon?.querySelector('svg');
        const rect = icon?.getBoundingClientRect();
        const inactiveShown = [...document.querySelectorAll(
            'a.nav-dropdown-item:not([aria-current="location"]) .nav-dropdown-item-icon'
        )].filter(i => getComputedStyle(i).display !== 'none').length;
        return {
            activeItem: active?.getAttribute('data-dropdown-item'),
            iconVisible: icon && getComputedStyle(icon).display !== 'none',
            svgPresent: !!svg,
            iconW: rect?.width || 0,
            iconH: rect?.height || 0,
            inactiveShown: inactiveShown,
        };
    }"""
    )
    page.keyboard.press("Escape")
    ok = (
        result.get("activeItem") == product["name"]
        and result.get("iconVisible")
        and result.get("svgPresent")
        and result.get("iconW", 0) >= 28
        and result.get("inactiveShown", 1) == 0
    )
    return {"ok": ok, **result}


def main():
    products = get_products()
    failed = []
    passed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1440, "height": 900})
        for product in products:
            for dark in (False, True):
                r = audit_product(pg, product, dark)
                if r.get("ok"):
                    passed += 1
                else:
                    failed.append({
                        "product": product["name"],
                        "icon": product["icon"],
                        "dark": dark,
                        **r,
                    })
        # mobile sample
        pg.set_viewport_size({"width": 390, "height": 844})
        for product in products[:5]:
            r = audit_product(pg, product, True)
            if r.get("ok"):
                passed += 1
            else:
                failed.append({"product": product["name"], "mobile": True, **r})
        browser.close()

    report = {
        "total_checks": passed + len(failed),
        "passed": passed,
        "failed_count": len(failed),
        "products": len(products),
        "failed": failed[:20],
    }
    print(json.dumps(report, indent=2))
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
