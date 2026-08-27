#!/usr/bin/env python3
"""Compute documentation page and product counts for hub landing stats."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"
STATS_JSON = ROOT / "_static" / "t3-stats.json"
STATS_INLINE_JS = ROOT / "_static" / "t3-stats-inline.js"

STAT_MARKDOWN_FILES = [
    "index.md",
    "AllTemplates/Index.md",
    "AllExtensions/Index.md",
    "AIFoundationExtensions/Index.md",
    "de/index.md",
    "de/AllTemplates/Index.md",
    "de/AllExtensions/Index.md",
    "de/T3AF/Index.md",
]

SKIP_PARTS = {"scripts", "node_modules", ".git", ".venv-translate", "de", "docs"}
HUB_SLUGS = {"index", "AIFoundationExtensions", "AllTemplates", "AllExtensions"}

AI_SLUGS = {
    "ExtNsT3AI",
    "ExtNsT3AC",
    "ExtNsT3AS",
    "ExtNsT3AL",
    "ExtNsT3AA",
    "ExtNsT3AB",
}


def _collect_nav_paths(node, paths: set[str]) -> None:
    """Collect page paths from docs.json navigation (pages + roots)."""
    if isinstance(node, dict):
        for key in ("root", "href", "page"):
            value = node.get(key)
            if isinstance(value, str) and value and not value.startswith("http"):
                paths.add(value.split("#", 1)[0].rstrip("/"))
        for page in node.get("pages", []) or []:
            if isinstance(page, str):
                paths.add(page.split("#", 1)[0].rstrip("/"))
            else:
                _collect_nav_paths(page, paths)
        for key, value in node.items():
            if key != "pages":
                _collect_nav_paths(value, paths)
    elif isinstance(node, list):
        for item in node:
            _collect_nav_paths(item, paths)


def _resolve_md_path(path: str, lang: str) -> Path | None:
    """Resolve a nav path to an existing markdown file."""
    candidates = [ROOT / f"{path}.md", ROOT / path / "Index.md"]
    for candidate in candidates:
        if not candidate.exists():
            continue
        rel = candidate.relative_to(ROOT).as_posix()
        if lang == "de":
            if not rel.startswith("de/"):
                continue
        elif rel.startswith("de/"):
            continue
        parts = rel.split("/")
        if any(part in SKIP_PARTS for part in parts):
            continue
        return candidate
    return None


def count_pages(lang: str = "en") -> int:
    """Count real published documentation pages from docs.json navigation."""
    docs = json.loads(DOCS.read_text(encoding="utf-8"))
    nav_paths: set[str] = set()
    _collect_nav_paths(docs.get("navigation", {}), nav_paths)

    resolved: set[str] = set()
    for path in nav_paths:
        if lang == "de" and not path.startswith("de/"):
            continue
        if lang == "en" and path.startswith("de/"):
            continue
        md = _resolve_md_path(path, lang)
        if md is not None:
            resolved.add(md.relative_to(ROOT).as_posix())
    return len(resolved)


def _walk_nav_products(groups: list, lang: str, products: set[str]) -> None:
    for node in groups:
        if isinstance(node, dict):
            root = node.get("root")
            if root:
                slug = root.split("/")[0]
                if lang == "de" and slug == "de":
                    slug = root.split("/")[1]
                if slug in HUB_SLUGS or slug == "License":
                    pass
                elif (ROOT / f"{root}.md").exists():
                    products.add(slug)
            if "pages" in node:
                _walk_nav_products(node["pages"], lang, products)
        elif isinstance(node, list):
            _walk_nav_products(node, lang, products)


def count_products(lang: str = "en") -> int:
    """Count product roots listed in docs.json navigation."""
    docs = json.loads(DOCS.read_text(encoding="utf-8"))
    products: set[str] = set()

    nav = docs.get("navigation", {})
    if nav.get("groups"):
        _walk_nav_products(nav["groups"], lang, products)
        return len(products)

    for entry in nav.get("languages", []):
        if entry.get("language") != lang:
            continue
        for dropdown in entry.get("dropdowns", []):
            for group in dropdown.get("groups", []):
                _walk_nav_products([group], lang, products)
        return len(products)
    return 0


def count_ai_products() -> int:
    """AI extension products plus T3AF Foundation."""
    return len(AI_SLUGS) + 1


def format_number(value: int, lang: str) -> str:
    if lang == "de":
        return f"{value:,}".replace(",", ".")
    return f"{value:,}"


def get_stats(lang: str = "en") -> dict[str, int]:
    return {
        "pages": count_pages(lang),
        "products": count_products(lang),
        "ai_products": count_ai_products(),
        "languages": 2,
    }


def sync_markdown_stats() -> None:
    """Keep fallback numbers in hub markdown aligned with computed stats."""
    for rel in STAT_MARKDOWN_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        lang = "de" if rel.startswith("de/") else "en"
        stats = get_stats(lang)
        text = path.read_text(encoding="utf-8")
        changed = False
        for key, value in stats.items():
            if not isinstance(value, int):
                continue
            display = format_number(value, lang)
            text, count = re.subn(
                rf'(<span className="t3-stat-value" data-t3-stat="{re.escape(key)}">)[^<]*(</span>)',
                rf"\g<1>{display}\2",
                text,
            )
            if count:
                changed = True
        if changed:
            path.write_text(text, encoding="utf-8")
            print(f"  synced stats in {rel}")


def write_stats_inline_js(payload: dict) -> None:
    """Zero-fetch stats for hub pages (loaded before t3-docs.min.js)."""
    # Always warm Mintlify icon/CDN origins before Lucide SVG flood starts.
    early_preconnect = (
        "(function(){try{var o=["
        "['preconnect','https://d3gk2c5xim1je2.cloudfront.net','anonymous'],"
        "['dns-prefetch','https://d3gk2c5xim1je2.cloudfront.net'],"
        "['preconnect','https://d4tuoctqmanu0.cloudfront.net','anonymous'],"
        "['dns-prefetch','https://d4tuoctqmanu0.cloudfront.net']"
        "];"
        "o.forEach(function(r){var l=document.createElement('link');"
        "l.rel=r[0];l.href=r[1];if(r[2])l.crossOrigin=r[2];"
        "document.head.appendChild(l);});}catch(e){}})();"
    )
    # Early Next.js prefetch gate: mint dev otherwise fires hundreds of ?_rsc
    # compiles for every in-viewport link before t3-docs.min.js can load.
    early_gate = (
        "(function(){try{var h=location.hostname||'';"
        "if(!(h==='localhost'||h==='127.0.0.1'||/^192\\.168\\./.test(h)||/^10\\./.test(h)))return;"
        "window.__t3PrefetchGateOpen=false;"
        "try{if(typeof window.fetch==='function'&&!window.fetch.__t3RscGated){"
        "var of=window.fetch.bind(window);"
        "window.fetch=function(i,n){var u='';"
        "try{u=typeof i==='string'?i:(i&&i.url)||'';}catch(e){}"
        "if(u&&(u.indexOf('?_rsc=')!==-1||u.indexOf('&_rsc=')!==-1)&&!window.__t3PrefetchGateOpen"
        "&&!(document.documentElement&&document.documentElement.classList.contains('t3-nav-busy')))"
        "{return Promise.resolve(new Response('',{status:204,statusText:'No Content'}));}"
        "return of(i,n);};window.fetch.__t3RscGated=1;}}catch(e0){}"
        "var n=0,t=setInterval(function(){n++;"
        "try{if(!window.next||!window.next.router||!window.next.router.prefetch){if(n>80)clearInterval(t);return;}"
        "if(window.next.router.__t3PrefetchGated){clearInterval(t);return;}"
        "var o=window.next.router.prefetch.bind(window.next.router);"
        "window.next.router.prefetch=function(){"
        "if(!window.__t3PrefetchGateOpen&&!(document.documentElement&&document.documentElement.classList.contains('t3-nav-busy')))"
        "return typeof Promise!=='undefined'?Promise.resolve():void 0;"
        "return o.apply(null,arguments);};"
        "window.next.router.__t3PrefetchGated=1;clearInterval(t);}"
        "catch(e){if(n>80)clearInterval(t);}},40);}catch(e){}})();"
    )
    STATS_INLINE_JS.write_text(
        "window.__T3_DOC_STATS__="
        + json.dumps(payload, separators=(",", ":"))
        + ";\n"
        + early_preconnect
        + "\n"
        + early_gate
        + "\n",
        encoding="utf-8",
    )


def write_stats_json() -> dict:
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "en": get_stats("en"),
        "de": get_stats("de"),
    }
    STATS_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATS_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_stats_inline_js(payload)
    sync_markdown_stats()
    return payload


def stat_value_html(key: str, lang: str, stats: dict | None = None) -> str:
    """Render a stat value span with data attribute for client hydration."""
    if stats is None:
        stats = get_stats(lang)
    value = stats.get(key, 0)
    if isinstance(value, int):
        display = format_number(value, lang)
    else:
        display = str(value)
    return f'<span className="t3-stat-value" data-t3-stat="{key}">{display}</span>'


def render_stats_bar(lang: str, keys: list[tuple[str, str]] | None = None) -> str:
    """Build a stats bar HTML fragment with dynamic counts."""
    stats = get_stats(lang)
    if keys is None:
        if lang == "de":
            keys = [
                ("pages", "Dokumentationsseiten"),
                ("products", "Produkte"),
                ("languages", "Sprachen"),
            ]
        else:
            keys = [
                ("pages", "Documentation pages"),
                ("products", "Products"),
                ("languages", "Languages"),
            ]

    cards = []
    for key, label in keys:
        if key == "languages" and lang == "de":
            extra = (
                '<div className="t3-stat-card">'
                '<span className="t3-stat-value" data-t3-stat="locale">EN + DE</span>'
                '<span className="t3-stat-label">Vollständig lokalisiert</span></div>'
            )
            cards.append(
                f'<div className="t3-stat-card">{stat_value_html(key, lang, stats)}'
                f'<span className="t3-stat-label">{label}</span></div>'
            )
            cards.append(extra)
            continue
        if key == "languages" and lang == "en":
            cards.append(
                f'<div className="t3-stat-card">{stat_value_html(key, lang, stats)}'
                f'<span className="t3-stat-label">{label}</span></div>'
            )
            cards.append(
                '<div className="t3-stat-card">'
                '<span className="t3-stat-value" data-t3-stat="locale">EN + DE</span>'
                '<span className="t3-stat-label">Fully localized</span></div>'
            )
            continue
        cards.append(
            f'<div className="t3-stat-card">{stat_value_html(key, lang, stats)}'
            f'<span className="t3-stat-label">{label}</span></div>'
        )
    return f'<div className="t3-stats-bar">{"".join(cards)}</div>'


def sync_homepage_stats(*, quiet: bool = False) -> dict:
    """Regenerate homepage Documentation pages / Products counts from docs.json.

    Call this after adding, removing, or renaming a documentation page or
    product. Updates `_static/t3-stats.json`, `_static/t3-stats-inline.js`,
    and the fallback numbers in hub markdown files.
    """
    payload = write_stats_json()
    if not quiet:
        en = payload["en"]
        de = payload["de"]
        print(f"Wrote {STATS_JSON.relative_to(ROOT)}")
        print(f"Wrote {STATS_INLINE_JS.relative_to(ROOT)}")
        print(f"  EN: {en['pages']} pages, {en['products']} products, {en['ai_products']} AI products")
        print(f"  DE: {de['pages']} pages, {de['products']} products")
    return payload


def main() -> None:
    sync_homepage_stats()


if __name__ == "__main__":
    main()
