#!/usr/bin/env python3
"""
Build Coinbase-style unified sidebar navigation in docs.json.

Replaces product dropdowns with a single hierarchical groups tree:
  Home → Get Started → T3AF → T3 Templates & Themes → TYPO3 Extensions
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"

SKIP_DROPDOWNS = {
    "Home",
    "Startseite",
    "All Extensions",
    "Alle Erweiterungen",
    "All AI Products",
    "Alle KI-Produkte",
    "All Templates",
    "Alle Vorlagen",
}

LICENSE_DROPDOWNS = {
    "License, Installation & Updates",
    "Lizenz, Installation und Updates",
}

AI_SLUGS = {
    "ExtNsT3AI", "ExtNsT3AC", "ExtNsT3AS", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB",
}

TEMPLATE_SLUGS = {
    "ExtThemes", "EXTKarma", "EXTAvatar", "EXTAyu", "EXTBootstrap",
    "EXTReactBootstrap", "EXTReva", "EXTShiva", "EXTShop",
}

AI_DISPLAY = {
    "ExtNsT3AI": ("T3AI", "sparkles"),
    "ExtNsT3AC": ("T3AC", "message-circle"),
    "ExtNsT3AS": ("T3AS", "search"),
    "ExtNsT3AL": ("T3AL", "languages"),
    "ExtNsT3AA": ("T3AA", "accessibility"),
    "ExtNsT3AB": ("T3AB", "blocks"),
}

TEMPLATE_DISPLAY = {
    "EXTKarma": ("T3 Karma", "palette"),
    "EXTBootstrap": ("T3 Bootstrap", "grid-3x3"),
    "EXTShop": ("T3 Shop", "shopping-bag"),
    "EXTAyu": ("T3 Ayu", "zap"),
    "EXTReva": ("T3 Reva", "sparkle"),
    "EXTShiva": ("T3 Shiva", "mountain"),
    "EXTAvatar": ("T3 Avatar", "user"),
    "EXTReactBootstrap": ("T3 React Bootstrap", "component"),
    "ExtThemes": ("T3 Themes", "layout-template"),
}

LABELS = {
    "en": {
        "home": "Home",
        "get_started": "Get Started",
        "license": "License & Installation",
        "ai": "T3AF",
        "templates": "T3 Templates & Themes",
        "extensions": "TYPO3 Extensions",
    },
    "de": {
        "home": "Startseite",
        "get_started": "Erste Schritte",
        "license": "Lizenz & Installation",
        "ai": "KI-Universum",
        "templates": "T3 Templates & Themes",
        "extensions": "TYPO3 Erweiterungen",
    },
}


def slug_from_path(path: str, lang: str) -> str:
    parts = path.split("/")
    if lang == "de" and parts[0] == "de":
        return parts[1] if len(parts) > 1 else parts[0]
    return parts[0]


def collect_pages(dropdown: dict) -> list[str]:
    pages: list[str] = []
    for group in dropdown.get("groups", []):
        pages.extend(group.get("pages", []))
    if not pages:
        pages = list(dropdown.get("pages", []))
    return pages


def product_group(dropdown: dict, lang: str) -> dict | None:
    pages = collect_pages(dropdown)
    if not pages:
        return None

    root = pages[0]
    slug = slug_from_path(root, lang)
    name = dropdown["dropdown"]
    icon = dropdown.get("icon", "puzzle")

    if slug in AI_DISPLAY:
        name, icon = AI_DISPLAY[slug]
    elif slug in TEMPLATE_DISPLAY:
        name, icon = TEMPLATE_DISPLAY[slug]

    child_pages = pages[1:] if len(pages) > 1 else []
    nested = build_page_tree(child_pages, lang, flat=False)

    group: dict = {
        "group": name,
        "root": root,
        "expanded": False,
        "pages": nested,
    }
    return group


def segment_icon(segment: str) -> str:
    s = segment.lower().replace(" ", "")
    icons = {
        "index": "book-open",
        "introduction": "book-open",
        "screenshots": "image",
        "videotutorials": "play-circle",
        "systemrequirements": "cpu",
        "installation": "download",
        "quickinstallation": "download",
        "configuration": "settings",
        "globalsettingsconfiguration": "settings",
        "updateversion": "history",
        "updateguide": "history",
        "releases": "history",
        "updating": "history",
        "faq": "circle-question-mark",
        "knownproblems": "triangle-alert",
        "knownissues": "triangle-alert",
        "support": "life-buoy",
        "buynow": "shopping-cart",
        "featureguide": "layers",
        "customization": "paintbrush",
        "editorguide": "pen-line",
        "helpfulinks": "link",
        "helpsupport": "life-buoy",
        "migration": "arrow-left-right",
        "seo": "search",
        "content": "file-text",
        "media": "image",
        "pages": "files",
        "translation": "languages",
        "appendix": "paperclip",
    }
    for key, icon in icons.items():
        if key in s:
            return icon
    return "file-text"


NEST_PARENTS = {
    "featureguide": ("Features", "layers"),
    "revolutionsliderlatest": ("Revolution Slider (Latest)", "gallery-horizontal-end"),
    "revolutionslider3.0": ("Revolution Slider 3.0", "gallery-horizontal-end"),
    "updateversion": ("Updates", "history"),
    "migration": ("Migration", "arrow-left-right"),
    "customllmsupport": ("Custom LLM", "bot"),
}


def build_page_tree(pages: list[str], lang: str, flat: bool = False) -> list:
    """Flat pages by default; nest only multi-page feature sections."""
    if flat:
        return pages

    singles: list[str] = []
    by_prefix: dict[str, list[str]] = {}

    for page in pages:
        parts = page.split("/")
        if lang == "de" and parts[0] == "de":
            parts = parts[1:]

        if len(parts) >= 3 and parts[1].lower() in NEST_PARENTS:
            prefix = "/".join(parts[:2])
            by_prefix.setdefault(prefix, []).append(page)
        else:
            singles.append(page)

    result: list = list(singles)

    for prefix, group_pages in sorted(by_prefix.items()):
        folder = prefix.split("/")[-1]
        label, icon = NEST_PARENTS.get(folder.lower(), (folder, segment_icon(folder)))
        if len(group_pages) == 1 and folder.lower() not in NEST_PARENTS:
            result.extend(group_pages)
            continue
        result.append(
            {
                "group": label,
                "expanded": False,
                "pages": group_pages,
            }
        )

    return result


def extract_products(entry: dict, lang: str) -> tuple[dict | None, list[dict], list[dict], list[dict]]:
    license_dd = None
    ai: list[dict] = []
    templates: list[dict] = []
    extensions: list[dict] = []

    for dropdown in entry.get("dropdowns", []):
        name = dropdown["dropdown"]
        if name in SKIP_DROPDOWNS:
            continue
        if name in LICENSE_DROPDOWNS:
            license_dd = dropdown
            continue

        pages = collect_pages(dropdown)
        if not pages:
            continue
        slug = slug_from_path(pages[0], lang)

        pg = product_group(dropdown, lang)
        if not pg:
            continue

        if slug in AI_SLUGS:
            ai.append(pg)
        elif slug in TEMPLATE_SLUGS:
            templates.append(pg)
        else:
            extensions.append(pg)

    def sort_key(g: dict) -> str:
        return g["group"].lower()

    ai.sort(key=sort_key)
    templates.sort(key=sort_key)
    extensions.sort(key=sort_key)
    return license_dd, ai, templates, extensions


def license_nested(license_dd: dict | None, lang: str) -> dict | None:
    if not license_dd:
        return None
    pages = collect_pages(license_dd)
    if not pages:
        return None
    L = LABELS[lang]
    return {
        "group": L["license"],
        "root": pages[0],
        "expanded": False,
        "pages": build_page_tree(pages[1:], lang, flat=True) if len(pages) > 1 else [],
    }


def build_groups(entry: dict) -> list[dict]:
    lang = entry["language"]
    L = LABELS[lang]
    prefix = "de/" if lang == "de" else ""

    license_dd, ai, templates, extensions = extract_products(entry, lang)

    home_pages = (
        ["de/index", "de/T3AF/Index", "de/AllTemplates/Index", "de/AllExtensions/Index"]
        if lang == "de"
        else ["index", "T3AF/Index", "AllTemplates/Index", "AllExtensions/Index"]
    )
    groups: list[dict] = [
        {
            "group": L["home"],
            "icon": "house",
            "pages": home_pages,
        },
    ]

    get_started_pages: list = []
    lic = license_nested(license_dd, lang)
    if lic:
        get_started_pages.append(lic)

    if get_started_pages:
        groups.append(
            {
                "group": L["get_started"],
                "icon": "rocket",
                "expanded": False,
                "pages": get_started_pages,
            }
        )

    if ai:
        groups.append(
            {
                "group": L["ai"],
                "icon": "sparkles",
                "expanded": True,
                "pages": ai,
            }
        )

    if templates:
        groups.append(
            {
                "group": L["templates"],
                "icon": "layout-template",
                "expanded": False,
                "pages": templates,
            }
        )

    if extensions:
        groups.append(
            {
                "group": L["extensions"],
                "icon": "puzzle",
                "expanded": False,
                "pages": extensions,
            }
        )

    return groups


BACKUP = ROOT / "scripts" / "_nav_dropdowns_backup.json"


def _ensure_dropdowns(entry: dict) -> None:
    if entry.get("dropdowns"):
        return
    if not BACKUP.exists():
        raise SystemExit(f"Missing dropdowns in docs.json and no backup at {BACKUP}")
    backup = json.loads(BACKUP.read_text(encoding="utf-8"))
    entry["dropdowns"] = backup.get(entry["language"], [])


def apply() -> None:
    data = json.loads(DOCS.read_text(encoding="utf-8"))

    # Snapshot dropdowns before first migration
    if not BACKUP.exists():
        snap = {}
        for entry in data["navigation"]["languages"]:
            if entry.get("dropdowns"):
                snap[entry["language"]] = entry["dropdowns"]
        if snap:
            BACKUP.write_text(json.dumps(snap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    for entry in data["navigation"]["languages"]:
        _ensure_dropdowns(entry)
        groups = build_groups(entry)
        entry.pop("dropdowns", None)
        entry.pop("navbar", None)
        entry.pop("footer", None)
        entry["groups"] = groups
        print(f"  {entry['language']}: {len(groups)} top-level groups")

    DOCS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote unified sidebar to {DOCS}")


if __name__ == "__main__":
    apply()
