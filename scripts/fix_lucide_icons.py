#!/usr/bin/env python3
"""Normalize docs.json dropdown icons to valid Lucide names."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"

# Legacy / invalid names -> current Lucide kebab-case
LUCIDE_ALIASES = {
    "help-circle": "circle-question-mark",
    "bar-chart-3": "chart-column",
    "user-circle": "circle-user",
    "instagram": "camera",
    "twitter": "x",
    "youtube": "circle-play",
    "code-2": "square-code",
    "puzzle-piece": "puzzle",
    "circle-help": "circle-question-mark",
}

# Semantic icon per product dropdown (current NS / T3 labels)
ICON_MAP = {
    "Home": "house",
    "Startseite": "house",
    "License, Installation & Updates": "key",
    "Lizenz, Installation und Updates": "key",
    "T3 Karma": "palette",
    "NS CKEditor Pack": "file-text",
    "NS News Comments": "message-square",
    "NS Revolution Slider": "gallery-horizontal",
    "NS T3AI": "bot",
    "NS T3AS": "search",
    "NS T3AC": "message-circle",
    "NS T3AL": "audio-lines",
    "NS T3AA": "accessibility",
    "NS T3AB": "blocks",
    "TYPO3 Templates": "layout-template",
    "TYPO3-Vorlagen": "layout-template",
    "T3 Avatar": "circle-user",
    "T3 Ayu": "sparkles",
    "T3 Bootstrap": "layout-grid",
    "T3 ReactBootstrap": "square-code",
    "T3 Reva": "brush",
    "T3 Shiva": "flame",
    "T3 Shop": "shopping-cart",
    "NS All Chat": "messages-square",
    "NS All Lightbox": "image",
    "NS All Sliders": "gallery-horizontal-end",
    "NS Backup": "hard-drive",
    "NS Cloudflare": "cloud",
    "NS Comments": "message-circle",
    "NS Cookieyes": "cookie",
    "NS Cookiebot": "shield-check",
    "NS Cookies": "cookie",
    "NS Disqus Comments": "message-square-text",
    "NS Ext Compatibility": "plug",
    "NS Event": "calendar",
    "NS Facebook Comment": "thumbs-up",
    "NS FAQ": "circle-question-mark",
    "NS Feedback": "star",
    "NS Friendlycaptcha": "shield",
    "NS Gallery": "images",
    "NS Googledocs": "file-text",
    "NS Google Map": "map-pin",
    "NS Google Site Kit": "chart-column",
    "NS Gridtocontainer": "grid-3x3",
    "NS Guestbook": "book-open",
    "NS Hellobar": "bell",
    "NS Helpdesk": "life-buoy",
    "NS Hubspot": "building-2",
    "NS Instagram": "camera",
    "NS Lazy Load": "eye",
    "NS Maintenance": "wrench",
    "NS News Advance Search": "search",
    "NS News Slick": "gallery-horizontal",
    "NS News Slider": "images",
    "NS Open Streetmap": "map",
    "NS Personio": "users",
    "NS Protect Site": "lock",
    "NS Publication Comment": "newspaper",
    "NS PWA": "smartphone",
    "NS Sharethis": "share-2",
    "NS Snow": "snowflake",
    "NS Statcounter": "chart-line",
    "NS Social Login": "log-in",
    "NS Timeline": "clock",
    "NS Twitter": "x",
    "NS Whatsapp": "phone",
    "NS Wp Migration": "arrow-right-left",
    "NS Cache Webhook": "zap",
    "NS Youtube": "circle-play",
    "NS Zoho": "building",
    "NS Zoho CRM": "contact-round",
}


def normalize_icon(name: str | None) -> str:
    if not name:
        return "puzzle"
    return LUCIDE_ALIASES.get(name, name)


def apply_icons() -> None:
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    updated = 0
    fixed_aliases = 0
    missing: list[str] = []

    for lang in data["navigation"]["languages"]:
        for dd in lang.get("dropdowns", []):
            label = dd["dropdown"]
            icon = ICON_MAP.get(label) or dd.get("icon", "puzzle")
            if label not in ICON_MAP and label not in ("Home", "Startseite"):
                missing.append(f'{lang["language"]}: {label}')
            normalized = normalize_icon(icon)
            if dd.get("icon") != normalized:
                if dd.get("icon") in LUCIDE_ALIASES:
                    fixed_aliases += 1
                dd["icon"] = normalized
                updated += 1

    DOCS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {updated} dropdown icons ({fixed_aliases} alias fixes).")
    if missing:
        print("Unmapped dropdowns (used existing/alias icon):")
        for m in sorted(set(missing)):
            print(f"  - {m}")


if __name__ == "__main__":
    apply_icons()
