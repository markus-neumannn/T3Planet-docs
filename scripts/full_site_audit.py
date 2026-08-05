#!/usr/bin/env python3
"""Full documentation audit: live site sync, links, images, HTTP, SEO."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "scripts" / "full_site_audit_report.json"
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")

# Live website slug → documentation folder slug
LIVE_EXTENSION_MAP = {
    "ckeditor-pack": "ExtRTECKEditorPack",
    "typo3-news-comment-extension": "ExtNsNewsComments",
    "typo3-slider-revolution-extension": "ExtNsRevolutionSlider",
    "sitekit-by-google-for-typo3": "ExtNsGoogleSiteKit",
    "typo3-wordpress-migration-extension": "ExtNsWpMigration",
    "typo3-backup-extension": "ExtNsBackup",
    "t3ai-typo3-extension": "ExtNsT3AI",
    "t3aa-typo3-extension": "ExtNsT3AA",
    "t3al-typo3-extension": "ExtNsT3AL",
    "typo3-hubspot-extension": "ExtNsHubspot",
    "typo3-event-extension": "ExtNsEvent",
    "typo3-feedback-extension": "ExtNsFeedback",
    "typo3-gallery-extension": "ExtNsGallery",
    "typo3-helpdesk-extension": "ExtNsHelpDesk",
    "typo3-social-login-extension": "ExtNsSocialLogin",
    "typo3-openstreetmap-extension": "ExtNsOpenStreetMap",
    "typo3-lightbox-extension": "ExtNsAllLightbox",
    "typo3-maintenance-mode-extension": "ExtNitsanMaintenance",
    "typo3-faq-extension": "ExtNsFAQ",
    "typo3-googledocs-extension": "ExtNsGoogleDocs",
    "typo3-news-slider-extension": "ExtNsNewsSlider",
    "typo3-slider-extension": "ExtNsAllSliders",
    "typo3-publication-comment-extension": "ExtNsPublicationComment",
    "typo3-page-comment-extension": "ExtNsComments",
    "typo3-slick-slider-extension": "ExtNsNewsSlickSlider",
    "typo3-whatsapp-extension": "ExtNsWhatsapp",
    "typo3-timeline-extension": "ExtNsTimeLine",
    "typo3-upgrade-extension-compatibility": "ExtNsExtCompatibility",
    "typo3-google-map-extension": "ExtNsGoogleMap",
    "typo3-cookieyes-extension": "ExtNsCookieYes",
    "typo3-cloudflare-extension": "ExtNsCloudflare",
    "typo3-pwa-extension": "ExtNsPWA",
    "typo3-friendly-captcha-extension": "ExtNsFriendlyCaptcha",
    "typo3-personio-extension": "ExtNsPersonio",
    "typo3-zoho-extension": "ExtNsZoho",
    "typo3-gridelements-container": "ExtNsGridtoContainer",
    "typo3-chat-extension": "ExtNsAllChat",
    "typo3-sharethis-extension": "ExtNsSharethis",
    "typo3-hellobar-extension": "ExtNitsanHellobar",
    "typo3-youtube-extension": "ExtNsYoutube",
    "typo3-disqus-comment-extension": "ExtNsDisqusComment",
    "typo3-instagram-extension": "ExtNsInstagram",
    "typo3-cookiebot-extension": "ExtNsCookiebot",
    "typo3-guestbook-extension": "ExtNsGuestbook",
    "typo3-news-search-extension": "ExtNsNewsAdvancedSearch",
    "typo3-twitter-extension": "ExtNsTwitter",
    "typo3-snowfall-extension": "ExtNsSnow",
}

LIVE_TEMPLATE_MAP = {
    "typo3-multipurpose-template": "EXTKarma",
    "t3-karma": "EXTKarma",
    "t3-avatar-multipurpose-typo3-template": "EXTAvatar",
    "t3-bootstrap-multipurpose-typo3-template": "EXTBootstrap",
    "t3-shiva-reactjs-typo3-template": "EXTShiva",
    "t3-reva-reactjs-nextjs-headless-typo3-template": "EXTReva",
    "t3-reactbootstrap-headless-typo3-template": "EXTReactBootstrap",
    "t3-ayu": "EXTAyu",
    "typo3-shop-template": "EXTShop",
}

DOC_TEMPLATE_SLUGS = {
    "ExtThemes", "EXTKarma", "EXTAvatar", "EXTAyu", "EXTBootstrap",
    "EXTReactBootstrap", "EXTReva", "EXTShiva", "EXTShop",
}

DOC_EXTENSION_SLUGS = set()  # filled from docs.json

IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']")
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)\s]+)\)|href=\"(/[^\"]+)\"")
FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def fetch_url(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "T3Planet-Docs-Audit/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def crawl_live_products(url: str) -> list[dict]:
    html = fetch_url(url)
    products = []
    for m in re.finditer(r'href="(?:https://t3planet\.de)?/en/([^"]+)"', html):
        slug = m.group(1).rstrip("/")
        if slug and slug not in ("typo3-extensions", "typo3-templates", "typo3-ai"):
            products.append({"slug": slug, "url": f"https://t3planet.de/en/{slug}"})
    seen = set()
    unique = []
    for p in products:
        if p["slug"] not in seen:
            seen.add(p["slug"])
            unique.append(p)
    return unique


def load_doc_products() -> tuple[set[str], set[str]]:
    docs = json.loads((ROOT / "docs.json").read_text())
    templates = set()
    extensions = set()
    ai = {"ExtNsT3AI", "ExtNsT3AC", "ExtNsT3AS", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB"}
    tpl = {"ExtThemes", "EXTKarma", "EXTAvatar", "EXTAyu", "EXTBootstrap", "EXTReactBootstrap", "EXTReva", "EXTShiva", "EXTShop"}
    skip = {"Home", "Startseite", "License, Installation & Updates", "Lizenz, Installation und Updates",
            "Overview", "Überblick", "Quick start", "Erste Schritte", "Popular docs", "Beliebte Docs",
            "AI Foundation", "KI-Universum", "All Templates", "Alle TYPO3-Vorlagen", "All Extensions", "Alle TYPO3-Erweiterungen"}

    for lang in docs["navigation"]["languages"]:
        if lang["language"] != "en":
            continue
        for dd in lang["dropdowns"]:
            if dd["dropdown"] in skip:
                continue
            pages = []
            for g in dd.get("groups", []):
                pages.extend(g.get("pages", []))
            if not pages:
                pages = dd.get("pages", [])
            if pages:
                slug = pages[0].split("/")[0]
                if slug in tpl:
                    templates.add(slug)
                elif slug not in ai:
                    extensions.add(slug)
    return templates, extensions


def collect_nav_routes() -> list[str]:
    docs = json.loads((ROOT / "docs.json").read_text())
    paths: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "pages" and isinstance(v, list):
                    for p in v:
                        if isinstance(p, str):
                            route = "/" + p.replace(".md", "")
                            if route.endswith("/index"):
                                route = route[:-5] or "/"
                            paths.add(route if route != "" else "/")
                else:
                    walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(docs["navigation"])
    return sorted(paths)


def check_internal_links() -> list[tuple[str, str]]:
    broken = []
    for md in ROOT.rglob("*.md"):
        if any(s in md.parts for s in ("scripts", ".venv-translate", "node_modules")):
            continue
        text = md.read_text(encoding="utf-8")
        for t in set(LINK_RE.findall(text)):
            target = (t[0] or t[1]).split("#")[0].rstrip("/")
            if not target or re.search(r"\.(png|jpg|svg|pdf|zip)$", target, re.I):
                continue
            cand = ROOT / (target.lstrip("/") + ".md")
            if not cand.exists():
                broken.append((str(md.relative_to(ROOT)), target))
    return broken


def check_images() -> dict:
    missing = []
    large = []
    no_alt = []
    for md in ROOT.rglob("*.md"):
        if any(s in md.parts for s in ("scripts", ".venv-translate")):
            continue
        text = md.read_text(encoding="utf-8")
        for m in IMG_RE.finditer(text):
            src = m.group(1) or m.group(2)
            if not src or src.startswith("http"):
                continue
            if m.group(1) and "!" in text[max(0, m.start() - 2): m.start() + 1]:
                alt_m = re.search(r"!\[([^\]]*)\]", text[max(0, m.start() - 80): m.end()])
                if alt_m and not alt_m.group(1).strip():
                    no_alt.append((str(md.relative_to(ROOT)), src))
            path = src.split("?")[0]
            if path.startswith("/"):
                fp = ROOT / path.lstrip("/")
            else:
                fp = (md.parent / path).resolve()
            if not fp.exists():
                missing.append((str(md.relative_to(ROOT)), src))
            elif fp.suffix.lower() in {".png", ".jpg", ".jpeg"} and fp.stat().st_size > 300_000:
                large.append({"file": str(fp.relative_to(ROOT)), "kb": round(fp.stat().st_size / 1024)})
    return {
        "missing_count": len(missing),
        "missing_samples": missing[:20],
        "large_count": len(large),
        "large_samples": sorted(large, key=lambda x: -x["kb"])[:20],
        "empty_alt_count": len(no_alt),
    }


def check_seo() -> dict:
    missing_title = []
    missing_desc = []
    for md in ROOT.rglob("*.md"):
        if any(s in md.parts for s in ("scripts", ".venv-translate")):
            continue
        text = md.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        if not m:
            missing_title.append(str(md.relative_to(ROOT)))
            continue
        fm = m.group(1)
        if "title:" not in fm:
            missing_title.append(str(md.relative_to(ROOT)))
        if "description:" not in fm:
            missing_desc.append(str(md.relative_to(ROOT)))
    return {
        "missing_title": len(missing_title),
        "missing_description": len(missing_desc),
        "samples_title": missing_title[:10],
        "samples_desc": missing_desc[:10],
    }


def http_check(paths: list[str]) -> dict:
    results = []

    def fetch(path: str):
        url = BASE + path
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "T3Planet-Audit/1.0"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return {"path": path, "status": r.status, "ok": True}
        except urllib.error.HTTPError as e:
            return {"path": path, "status": e.code, "ok": False}
        except Exception as e:
            return {"path": path, "status": 0, "ok": False, "error": str(e)}

    workers = int(os.environ.get("AUDIT_WORKERS", "4"))
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(fetch, p): p for p in paths}
        for fut in as_completed(futs):
            results.append(fut.result())
    failed = [r for r in results if not r["ok"]]
    return {"checked": len(results), "failed": len(failed), "failed_samples": failed[:30]}


def compare_live_vs_docs() -> dict:
    live_ext_html = fetch_url("https://t3planet.de/en/typo3-extensions")
    live_tpl_html = fetch_url("https://t3planet.de/en/typo3-templates")
    live_ext_slugs = {p["slug"] for p in crawl_live_products("https://t3planet.de/en/typo3-extensions")}
    live_tpl_slugs = {p["slug"] for p in crawl_live_products("https://t3planet.de/en/typo3-templates")}

    doc_tpl, doc_ext = load_doc_products()

    mapped_live_ext = {LIVE_EXTENSION_MAP[s] for s in live_ext_slugs if s in LIVE_EXTENSION_MAP}
    unmapped_live_ext = sorted(live_ext_slugs - set(LIVE_EXTENSION_MAP.keys()))

    mapped_live_tpl = set()
    for s in live_tpl_slugs:
        if s in LIVE_TEMPLATE_MAP:
            mapped_live_tpl.add(LIVE_TEMPLATE_MAP[s])
        elif "t3-karma" in s or "multipurpose" in s:
            mapped_live_tpl.add("EXTKarma")
        elif "avatar" in s:
            mapped_live_tpl.add("EXTAvatar")
        elif "bootstrap" in s and "react" not in s:
            mapped_live_tpl.add("EXTBootstrap")
        elif "shiva" in s:
            mapped_live_tpl.add("EXTShiva")
        elif "reva" in s:
            mapped_live_tpl.add("EXTReva")
        elif "reactbootstrap" in s or "react-bootstrap" in s:
            mapped_live_tpl.add("EXTReactBootstrap")
        elif "ayu" in s:
            mapped_live_tpl.add("EXTAyu")
        elif "shop" in s:
            mapped_live_tpl.add("EXTShop")

    missing_in_docs_ext = sorted(mapped_live_ext - doc_ext)
    extra_in_docs_ext = sorted(doc_ext - mapped_live_ext - {
        "ExtNsT3AC", "ExtNsT3AB", "ExtNsProtectSite", "ExtNsCacheWebhook",
        "ExtNsStatcounter", "EXTNsZohoCrm", "ExtNsRevolutionSlider",
    })  # some may be valid but not on listing page

    missing_in_docs_tpl = sorted(mapped_live_tpl - doc_tpl)
    extra_in_docs_tpl = sorted(doc_tpl - mapped_live_tpl - {"ExtThemes"})

    return {
        "live_extensions_found": len(live_ext_slugs),
        "live_templates_found": len(live_tpl_slugs),
        "unmapped_live_extensions": unmapped_live_ext[:25],
        "missing_extensions_in_docs": missing_in_docs_ext,
        "extra_extensions_in_docs_not_on_live": extra_in_docs_ext,
        "missing_templates_in_docs": missing_in_docs_tpl,
        "extra_templates_in_docs_not_on_live": extra_in_docs_tpl,
        "live_only_templates": sorted(
            s for s in live_tpl_slugs
            if not any(k in s for k in ("karma", "avatar", "bootstrap", "shiva", "reva", "reactbootstrap", "ayu", "shop"))
        )[:15],
    }


def main():
    print("Running full site audit...")
    routes = collect_nav_routes()
    sample_size = 120 if "--sample" in sys.argv else min(len(routes), 300)
    priority = [r for r in routes if any(x in r for x in ("ExtNsT3", "EXTKarma", "AllExtensions", "License", "index"))]
    http_paths = list(dict.fromkeys(priority + routes))[:sample_size]

    report = {
        "mintlify_url": BASE,
        "routes_total": len(routes),
        "http_sample_size": sample_size,
        "broken_links": check_internal_links(),
        "images": check_images(),
        "seo": check_seo(),
        "live_sync": compare_live_vs_docs(),
    }

    print(f"HTTP checking {sample_size} routes...")
    report["http"] = http_check(http_paths)

    broken_count = len(report["broken_links"])
    report["summary"] = {
        "broken_links": broken_count,
        "missing_images": report["images"]["missing_count"],
        "large_images": report["images"]["large_count"],
        "http_404": report["http"]["failed"],
        "seo_missing_desc": report["seo"]["missing_description"],
        "extra_templates_not_on_live": report["live_sync"]["extra_templates_in_docs_not_on_live"],
        "extra_extensions_not_on_live": len(report["live_sync"]["extra_extensions_in_docs_not_on_live"]),
    }

    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    print(f"Full report: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
