#!/usr/bin/env python3
"""Add browse dropdowns to docs.json for quick sidebar jumps to all products."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"

sys.path.insert(0, str(ROOT / "scripts"))
from generate_hub_landings import (  # noqa: E402
    AI_META,
    EXT_CATEGORY,
    TEMPLATE_META,
    parse_catalog,
)

BROWSE_DROPDOWNS = {
    "en": {
        "extensions": ("All Extensions", "puzzle"),
        "ai": ("All AI Products", "bot"),
        "templates": ("All Templates", "layout-template"),
    },
    "de": {
        "extensions": ("Alle Erweiterungen", "puzzle"),
        "ai": ("Alle KI-Produkte", "bot"),
        "templates": ("Alle Vorlagen", "layout-template"),
    },
}


def _index_path(product: dict, lang: str) -> str:
    return product["nav_path"]


def build_extension_groups(lang: str) -> list[dict]:
    products = [p for p in parse_catalog(lang) if p["category"] == "extension"]
    by_cat: dict[str, list[dict]] = {}
    for product in products:
        cat_en, cat_de = EXT_CATEGORY.get(product["slug"], ("Extensions", "Erweiterungen"))
        cat = cat_de if lang == "de" else cat_en
        by_cat.setdefault(cat, []).append(product)

    groups = []
    for cat in sorted(by_cat.keys()):
        items = sorted(by_cat[cat], key=lambda p: p["dropdown"].lower())
        groups.append(
            {
                "group": cat,
                "expanded": cat in ("Content", "Inhalte", "Comments", "Kommentare", "Analytics"),
                "pages": [_index_path(p, lang) for p in items],
            }
        )
    return groups


def build_ai_groups(lang: str) -> list[dict]:
    products = [p for p in parse_catalog(lang) if p["category"] == "ai"]
    products.sort(key=lambda p: p["dropdown"].lower())
    label = "T3AF" if lang == "en" else "KI-Universum"
    return [
        {
            "group": label,
            "expanded": True,
            "pages": [_index_path(p, lang) for p in products],
        }
    ]


def build_template_groups(lang: str) -> list[dict]:
    products = [p for p in parse_catalog(lang) if p["category"] == "template"]
    by_cat: dict[str, list[dict]] = {}
    for product in products:
        meta = TEMPLATE_META.get(product["slug"])
        if meta:
            cat = meta["category_de" if lang == "de" else "category_en"]
        else:
            cat = "Templates" if lang == "en" else "Vorlagen"
        by_cat.setdefault(cat, []).append(product)

    groups = []
    for cat in sorted(by_cat.keys()):
        items = sorted(by_cat[cat], key=lambda p: p["dropdown"].lower())
        groups.append(
            {
                "group": cat,
                "expanded": cat in ("Overview", "Überblick"),
                "pages": [_index_path(p, lang) for p in items],
            }
        )
    return groups


def make_browse_dropdown(lang: str, kind: str) -> dict:
    label, icon = BROWSE_DROPDOWNS[lang][kind]
    if kind == "extensions":
        groups = build_extension_groups(lang)
    elif kind == "ai":
        groups = build_ai_groups(lang)
    else:
        groups = build_template_groups(lang)
    return {"dropdown": label, "icon": icon, "groups": groups}


def upsert_browse_dropdowns() -> None:
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    for entry in data["navigation"]["languages"]:
        lang = entry["language"]
        if lang not in BROWSE_DROPDOWNS:
            continue

        browse = [
            make_browse_dropdown(lang, "extensions"),
            make_browse_dropdown(lang, "ai"),
            make_browse_dropdown(lang, "templates"),
        ]
        browse_labels = {b["dropdown"] for b in browse}

        dropdowns = entry.get("dropdowns", [])
        kept = [d for d in dropdowns if d.get("dropdown") not in browse_labels]
        insert_at = 1
        for i, d in enumerate(kept):
            if d.get("dropdown") in ("Home", "Startseite"):
                insert_at = i + 1
                break
        entry["dropdowns"] = kept[:insert_at] + browse + kept[insert_at:]

    DOCS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Inserted browse sidebar menus into docs.json")


if __name__ == "__main__":
    upsert_browse_dropdowns()
