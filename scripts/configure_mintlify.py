#!/usr/bin/env python3
"""Apply production Mintlify UI/UX, SEO, and branding settings to docs.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"

FOOTER_EN = {
    "socials": {
        "website": "https://t3planet.de/en/",
        "x": "https://x.com/t3planetde",
        "linkedin": "https://www.linkedin.com/company/t3planet/",
        "youtube": "https://www.youtube.com/@t3planet",
    },
    "links": [
        {
            "header": "Products",
            "items": [
                {"label": "TYPO3 Extensions", "href": "https://t3planet.de/en/typo3-extensions"},
                {"label": "TYPO3 Templates", "href": "https://t3planet.de/en/typo3-templates"},
                {"label": "AI Solutions", "href": "https://t3planet.de/en/typo3-ai"},
            ],
        },
        {
            "header": "Resources",
            "items": [
                {"label": "Support", "href": "https://t3planet.de/en/support"},
                {"label": "FAQ", "href": "https://t3planet.de/en/faq"},
                {"label": "Blog", "href": "https://t3planet.de/en/blog"},
                {"label": "Contact", "href": "https://t3planet.de/en/contact"},
            ],
        },
    ],
}

FOOTER_DE = {
    "socials": {
        "website": "https://t3planet.de/",
        "x": "https://x.com/t3planetde",
        "linkedin": "https://www.linkedin.com/company/t3planet/",
        "youtube": "https://www.youtube.com/@t3planet",
    },
    "links": [
        {
            "header": "Produkte",
            "items": [
                {"label": "TYPO3 Extensions", "href": "https://t3planet.de/typo3-extensions"},
                {"label": "TYPO3 Templates", "href": "https://t3planet.de/typo3-templates"},
                {"label": "KI-Lösungen", "href": "https://t3planet.de/typo3-ai"},
            ],
        },
        {
            "header": "Ressourcen",
            "items": [
                {"label": "Support", "href": "https://t3planet.de/support"},
                {"label": "FAQ", "href": "https://t3planet.de/faq"},
                {"label": "Blog", "href": "https://t3planet.de/blog"},
                {"label": "Kontakt", "href": "https://t3planet.de/kontakt"},
            ],
        },
    ],
}


def main():
    with open(DOCS, encoding="utf-8") as fh:
        d = json.load(fh)

    d["theme"] = "mint"
    d["name"] = "T3Planet Docs"
    d["description"] = (
        "Official T3Planet documentation for TYPO3 extensions, templates, "
        "AI solutions, licensing, and installation guides."
    )

    d["logo"] = {
        "light": "/_static/t3planet-light.svg",
        "dark": "/_static/t3planet-white-logo.svg",
        "href": "https://t3planet.de/en/",
    }

    d["colors"] = {
        "primary": "#f49700",
        "light": "#fff8ee",
        "dark": "#c97800",
    }

    d["appearance"] = {
        "default": "system",
        "strict": False,
    }

    d["styling"] = {
        "eyebrows": "breadcrumbs",
        "codeblocks": {
            "theme": {
                "light": "github-light",
                "dark": "github-dark",
            }
        },
    }

    d["scripts"] = ["/_static/t3-docs.min.js"]

    d["fonts"] = {
        "family": "Inter",
        "heading": {"family": "Inter", "weight": 600},
        "body": {"family": "Inter", "weight": 400},
    }

    d["icons"] = {"library": "lucide"}

    d["background"] = {"decoration": "grid"}

    d["seo"] = {
        "indexing": "all",
        "metatags": {
            "og:site_name": "T3Planet Documentation",
            "og:type": "website",
            "og:image": (
                "https://t3planet.de/fileadmin/ns_theme_t3planet/"
                "Contact/T3Planet_OG_Image_en.png"
            ),
            "twitter:card": "summary_large_image",
            "twitter:site": "@t3planetde",
        },
    }

    d["metadata"] = {"timestamp": True}

    d["footer"] = FOOTER_EN

    d["navbar"] = {
        "links": [
            {"label": "T3Planet", "href": "https://t3planet.de/en/"},
            {"label": "Support", "href": "https://t3planet.de/en/support"},
        ],
        "primary": {
            "type": "button",
            "label": "Browse Extensions",
            "href": "https://t3planet.de/en/typo3-extensions",
        },
    }

    for lang in d["navigation"]["languages"]:
        if lang["language"] == "en":
            lang["navbar"] = d["navbar"]
            lang["footer"] = FOOTER_EN
        elif lang["language"] == "de":
            lang["navbar"] = {
                "links": [
                    {"label": "T3Planet", "href": "https://t3planet.de/"},
                    {"label": "Support", "href": "https://t3planet.de/support"},
                ],
                "primary": {
                    "type": "button",
                    "label": "Erweiterungen durchsuchen",
                    "href": "https://t3planet.de/typo3-extensions",
                },
            }
            lang["footer"] = FOOTER_DE

    d["redirects"] = [
        {"source": "/en/latest/:path*", "destination": "/:path*"},
        {"source": "/en/:path*", "destination": "/:path*"},
    ]

    with open(DOCS, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
    print("docs.json configured for production UI/UX, SEO, and branding.")


if __name__ == "__main__":
    main()
    from sync_doc_stats import sync_homepage_stats
    sync_homepage_stats()
