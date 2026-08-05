#!/usr/bin/env python3
"""Deprecated: page-level sidebar icons are disabled. Use remove_nav_icons.py instead."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)
ICON_RE = re.compile(r"^icon:\s*.+$", re.M)

SEGMENT_ICONS = {
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
    "helpfullinks": "link",
    "helpsupport": "life-buoy",
    "migration": "arrow-left-right",
    "seo": "search",
    "content": "file-text",
    "media": "image",
    "pages": "files",
    "translation": "languages",
    "appendix": "paperclip",
    "demosite": "monitor",
    "localization": "languages",
    "speedperformance": "gauge",
    "templateslayouts": "layout",
    "contentblockelements": "blocks",
    "captchaconfiguration": "shield-check",
    "licenseactivation": "key",
    "licensemanager": "key",
    "generatelicensekey": "key",
    "registerandmanagedomains": "globe",
    "otherproducts": "package",
    "licensedeactivation": "key",
    "extendtrial": "clock",
    "renewpurchase": "credit-card",
    "sitesets": "layers",
    "checknewversion": "refresh-cw",
    "noncomposer": "terminal",
    "composer": "terminal",
    "dashboard": "layout-dashboard",
    "datasource": "database",
    "trainingcenter": "graduation-cap",
    "frontendplugin": "plug",
    "performanceconfiguration": "gauge",
    "databasechunking": "database",
    "verifyindexeddata": "list-checks",
    "aistatistics": "chart-column",
    "prompts": "message-square-text",
    "aisettings": "bot",
    "formsettings": "file-input",
    "gallery": "images",
    "slider": "gallery-horizontal",
    "comments": "message-square",
    "news": "newspaper",
    "maps": "map-pin",
    "webhook": "webhook",
    "backup": "hard-drive",
    "snow": "snowflake",
    "event": "calendar",
    "timeline": "git-branch",
    "guestbook": "book-user",
    "feedback": "message-circle-heart",
    "helpdesk": "headphones",
    "social": "share-2",
    "twitter": "x",
    "instagram": "camera",
    "whatsapp": "phone",
    "youtube": "circle-play",
    "hubspot": "building-2",
    "zoho": "building",
    "personio": "users",
    "cookiebot": "cookie",
    "lazyload": "eye-off",
    "pwa": "smartphone",
    "cloudflare": "cloud",
    "protectsite": "shield",
    "revolutionslider": "gallery-horizontal-end",
    "ckeditor": "file-text",
    "ckeditorpack": "file-text",
    "gridtocontainer": "grid-2x2",
    "wpmigration": "arrow-right-left",
    "extcompatibility": "puzzle",
    "maintenance": "wrench",
    "allchat": "messages-square",
    "alllightbox": "expand",
    "allsliders": "gallery-horizontal",
    "friendlycaptcha": "shield-check",
    "disquscomment": "message-square",
    "facebookcomment": "message-square",
    "publicationcomment": "message-square",
    "newscomments": "message-square",
    "newsadvancedsearch": "search",
    "newsslickslider": "gallery-horizontal",
    "newsslider": "gallery-horizontal",
    "googlesitekit": "chart-column",
    "statcounter": "chart-column",
    "googledocs": "file-text",
    "googlemap": "map",
    "openstreetmap": "map-pin",
    "hellobar": "megaphone",
    "sharethis": "share-2",
    "sociallogin": "log-in",
    "cachewebhook": "webhook",
    "cookieshint": "cookie",
    "cookieyes": "cookie",
    "themes": "layout-template",
    "karma": "palette",
    "bootstrap": "grid-3x3",
    "shop": "shopping-bag",
    "ayu": "zap",
    "reva": "sparkle",
    "shiva": "mountain",
    "avatar": "user",
    "t3ai": "sparkles",
    "t3ac": "message-circle",
    "t3as": "search",
    "t3al": "languages",
    "t3aa": "accessibility",
    "t3ab": "blocks",
}


def icon_for_path(rel: str) -> str:
    parts = Path(rel).parts
    for part in reversed(parts):
        key = part.lower().replace("_", "").replace("-", "")
        if key in SEGMENT_ICONS:
            return SEGMENT_ICONS[key]
        for seg, icon in SEGMENT_ICONS.items():
            if seg in key:
                return icon
    if rel.endswith("Support.md"):
        return "life-buoy"
    if rel.endswith("BuyNow.md"):
        return "shopping-cart"
    return "file-text"


def add_icon_to_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return False
    fm = m.group(1)
    if ICON_RE.search(fm):
        return False
    icon = icon_for_path(str(path.relative_to(ROOT)))
    new_fm = fm.rstrip() + f'\nicon: "{icon}"'
    new_text = f"---\n{new_fm}\n---" + text[m.end() :]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    print("Skipped: page-level sidebar icons are disabled.")
    return

    updated = 0
    skipped = 0
    for md in ROOT.rglob("*.md"):
        if ".venv" in md.parts or "scripts" in md.parts:
            continue
        if add_icon_to_file(md):
            updated += 1
        else:
            skipped += 1
    print(f"Added icons to {updated} files ({skipped} already had icons or no frontmatter)")


if __name__ == "__main__":
    main()
