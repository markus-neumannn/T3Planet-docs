#!/usr/bin/env python3
"""Compare Mintlify docs against original docs.t3planet.de URL inventory."""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "scripts" / "docs_migration_audit.json"
BASE = "http://192.168.0.137:3000"
SKIP = {"scripts", "node_modules", ".git", ".venv-translate", "de"}

# Original product roots from docs.t3planet.de
ORIGINAL_PRODUCTS = """
License EXTKarma ExtRTECKEditorPack ExtNsNewsComments ExtNsRevolutionSlider
ExtNsT3AI ExtNsT3AS ExtNsT3AC ExtNsT3AL ExtNsT3AA ExtNsT3AB ExtThemes
EXTAvatar EXTAyu EXTBootstrap EXTReactBootstrap EXTReva EXTShiva EXTShop
ExtNsAllChat ExtNsAllLightbox ExtNsAllSliders ExtNsBackup ExtNsCloudflare
ExtNsComments ExtNsCookieYes ExtNsCookiebot ExtNsCookiesHint ExtNsDisqusComment
ExtNsExtCompatibility ExtNsEvent ExtNsFacebookComment ExtNsFAQ ExtNsFeedback
ExtNsFriendlyCaptcha ExtNsGallery ExtNsGoogleDocs ExtNsGoogleMap ExtNsGoogleSiteKit
ExtNsGridtoContainer ExtNsGuestbook ExtNitsanHellobar ExtNsHelpDesk ExtNsHubspot
ExtNsInstagram ExtNsLazyload ExtNitsanMaintenance ExtNsNewsAdvancedSearch
ExtNsNewsSlickSlider ExtNsNewsSlider ExtNsOpenStreetMap ExtNsPersonio
ExtNsProtectSite ExtNsPublicationComment ExtNsPWA ExtNsSharethis ExtNsSnow
ExtNsStatcounter ExtNsSocialLogin ExtNsTimeLine ExtNsTwitter ExtNsWhatsapp
ExtNsWpMigration ExtNsCacheWebhook ExtNsYoutube ExtNsZoho EXTNsZohoCrm
T3AF AllTemplates AllExtensions
""".split()


def md_to_route(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if parts[-1].lower() == "index.md":
        parts = parts[:-1]
        slug = "/".join(parts)
        return f"/{slug}/Index" if slug else "/"
    stem = parts[-1][:-3]
    parts[-1] = stem
    return "/" + "/".join(parts)


def collect_routes() -> set[str]:
    routes: set[str] = set()
    for md in ROOT.rglob("*.md"):
        rel = str(md.relative_to(ROOT))
        if rel.startswith("de/") or any(p in SKIP for p in rel.split("/")):
            continue
        routes.add(md_to_route(rel))
    return routes


def http_status(path: str) -> int:
    url = BASE + path
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "audit/1.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main() -> None:
    routes = collect_routes()
    missing_products = []
    html_failures = []

    for product in ORIGINAL_PRODUCTS:
        route = f"/{product}/Index"
        html = f"{route}.html"
        legacy = f"/en/latest/{product}/Index.html"
        if route not in routes and route != "/T3AF/Index":
            # hub pages may exist differently
            if not any(r.startswith(f"/{product}/") for r in routes):
                missing_products.append(product)
                continue
        for path in (html, legacy):
            code = http_status(path)
            if code not in (200, 301, 302, 307, 308):
                html_failures.append({"path": path, "status": code})

    report = {
        "mintlify_en_pages": len(routes),
        "original_products": len(ORIGINAL_PRODUCTS),
        "missing_products": missing_products,
        "html_url_failures": html_failures[:50],
        "html_failure_count": len(html_failures),
        "sample_routes": sorted(routes)[:20],
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
