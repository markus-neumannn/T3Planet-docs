#!/usr/bin/env python3
"""Assign semantic Lucide icons to every product dropdown in docs.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"

# Semantic icon per product (Lucide kebab-case names)
ICON_MAP = {
    "Home": "house",
    "License, Installation & Updates": "key",
    "T3 Karma": "palette",
    # AI extensions
    "EXT:ns_t3ai": "bot",
    "EXT:ns_t3as": "search",
    "EXT:ns_t3ac": "message-circle",
    "EXT:ns_t3al": "audio-lines",
    "EXT:ns_t3aa": "accessibility",
    "EXT:ns_t3ab": "blocks",
    # Templates & themes
    "TYPO3 Templates": "layout-template",
    "T3 Avatar": "user-circle",
    "T3 Ayu": "sparkles",
    "T3 Bootstrap": "layout-grid",
    "T3 ReactBootstrap": "code",
    "T3 Reva": "brush",
    "T3 Shiva": "flame",
    "T3 Shop": "shopping-cart",
    # Editor & content
    "EXT:rte_ckeditor_pack": "file-text",
    "EXT:ns_news_comments": "message-square",
    "EXT:ns_revolution_slider": "gallery-horizontal",
    "EXT:ns_all_chat": "messages-square",
    "EXT:ns_all_lightbox": "image",
    "EXT:ns_all_sliders": "gallery-horizontal-end",
    # Infrastructure
    "EXT:ns_backup": "hard-drive",
    "EXT:ns_cloudflare": "cloud",
    "EXT:ns_cache_webhook": "zap",
    "EXT:ns_protect_site": "lock",
    "EXT:nitsan_maintenance": "wrench",
    "EXT:ns_lazy_load": "eye",
    "EXT:ns_pwa": "smartphone",
    "EXT:ns_wp_migration": "arrow-right-left",
    "EXT:ns_ext_compatibility": "plug",
    "EXT:ns_gridtocontainer": "grid-3x3",
    # Comments & social
    "EXT:ns_comments": "message-circle",
    "EXT:ns_disqus_comments": "message-square-text",
    "EXT:ns_facebook_comment": "thumbs-up",
    "EXT:ns_publication_comment": "newspaper",
    # Cookies & consent
    "EXT:ns_cookieyes": "cookie",
    "EXT:ns_cookiebot": "shield-check",
    "EXT:ns_cookies": "cookie",
    # Maps & location
    "EXT:ns_google_map": "map-pin",
    "EXT:ns_open_streetmap": "map",
    # Google & analytics
    "EXT:ns_googledocs": "file-text",
    "EXT:ns_google_sitekit": "bar-chart-3",
    "EXT:ns_statcounter": "chart-line",
    # CRM & integrations
    "EXT:ns_hubspot": "building-2",
    "EXT:ns_zoho": "building",
    "EXT:ns_zoho_crm": "contact",
    "EXT:ns_personio": "users",
    # Social & media
    "EXT:ns_instagram": "instagram",
    "EXT:ns_youtube": "youtube",
    "EXT:ns_twitter": "twitter",
    "EXT:ns_whatsapp": "phone",
    "EXT:ns_social_login": "log-in",
    "EXT:ns_sharethis": "share-2",
    # News & content
    "EXT:ns_news_advance_search": "search",
    "EXT:ns_news_slick": "gallery-horizontal",
    "EXT:ns_news_slider": "images",
    "EXT:ns_gallery": "images",
    "EXT:ns_event": "calendar",
    "EXT:ns_timeline": "clock",
    # Support & feedback
    "EXT:ns_helpdesk": "life-buoy",
    "EXT:ns_faq": "help-circle",
    "EXT:ns_feedback": "star",
    "EXT:ns_guestbook": "book-open",
    "EXT:ns_hellobar": "bell",
    # Security & captcha
    "EXT:ns_friendlycaptcha": "shield",
    # Misc
    "EXT:ns_snow": "snowflake",
}


def first_page(dropdown: dict) -> str:
    if dropdown.get("pages"):
        return dropdown["pages"][0]
    if dropdown.get("groups"):
        return dropdown["groups"][0]["pages"][0]
    return ""


def apply_icons():
    with open(DOCS, encoding="utf-8") as fh:
        data = json.load(fh)

    en_icons = []
    updated = 0
    missing = []

    for lang in data["navigation"]["languages"]:
        is_en = lang["language"] == "en"
        for i, dd in enumerate(lang.get("dropdowns", [])):
            name = dd["dropdown"]
            if is_en:
                icon = ICON_MAP.get(name)
                if not icon:
                    missing.append(name)
                    icon = dd.get("icon", "puzzle-piece")
                dd["icon"] = icon
                en_icons.append(icon)
                updated += 1
            else:
                # DE: same order as EN — apply by index
                if i < len(en_icons):
                    dd["icon"] = en_icons[i]
                    updated += 1

    with open(DOCS, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)

    unique = len(set(en_icons))
    print(f"Updated {updated} dropdown icons ({unique} unique icons).")
    if missing:
        print("Unmapped products (kept existing icon):")
        for m in missing:
            print(f"  - {m}")


if __name__ == "__main__":
    apply_icons()
