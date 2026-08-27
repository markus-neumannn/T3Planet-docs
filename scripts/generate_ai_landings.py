#!/usr/bin/env python3
"""Generate Coinbase-style sectioned landing pages for T3AF products."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

AI_PRODUCTS = {
    "ExtNsT3AI": {
        "en": {
            "eyebrow": "AI Universe Extensions",
            "hero_title": "T3AI — TYPO3 AI Content & SEO",
            "hero_subtitle": "Generate content, translations, SEO metadata, and media with AI directly inside TYPO3.",
            "prefix": "",
            "sections": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Configuration", "configuration", "Configuration/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Pages", "pages", "Pages/Index"),
                    ("Content", "content", "Content/Index"),
                    ("SEO", "seo", "SEO/Index"),
                    ("AI Settings", "settings", "AISettings/Index"),
                    ("Prompts", "prompts", "Prompts/Index"),
                ],
                "optimize": [
                    ("Translation", "translation", "Translation/Index"),
                    ("Media", "media", "Media/Index"),
                    ("Video Tutorials", "video", "VideoTutorials/Index"),
                    ("Upgrade Guide", "upgrade", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Support", "support", "Support"),
                    ("Get Extension", "buy", "BuyNow"),
                ],
            },
        },
        "de": {
            "eyebrow": "KI-Universum",
            "hero_title": "T3AI — TYPO3 KI-Inhalte & SEO",
            "hero_subtitle": "Erstellen Sie Inhalte, Übersetzungen, SEO-Metadaten und Medien mit KI direkt in TYPO3.",
            "prefix": "/de",
            "sections": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Konfiguration", "configuration", "Configuration/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Seiten", "pages", "Pages/Index"),
                    ("Inhalte", "content", "Content/Index"),
                    ("SEO", "seo", "SEO/Index"),
                    ("KI-Einstellungen", "settings", "AISettings/Index"),
                    ("Prompts", "prompts", "Prompts/Index"),
                ],
                "optimize": [
                    ("Übersetzung", "translation", "Translation/Index"),
                    ("Medien", "media", "Media/Index"),
                    ("Video-Tutorials", "video", "VideoTutorials/Index"),
                    ("Upgrade-Anleitung", "upgrade", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Support", "support", "Support"),
                    ("Erweiterung holen", "buy", "BuyNow"),
                ],
            },
        },
    },
    "ExtNsT3AS": {
        "en": {
            "eyebrow": "AI Universe Extensions",
            "hero_title": "T3AS — TYPO3 AI Search",
            "hero_subtitle": "AI-powered search across your TYPO3 content with embeddings, custom LLM, and performance tuning.",
            "prefix": "",
            "sections": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Configuration", "configuration", "Configuration/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Search Plugin", "pages", "FrontendPlugin/Index"),
                    ("Custom LLM", "llm", "CustomLLMSupport/Index"),
                    ("Hosting Policy", "settings", "T3ASHostingPolicyforCustomLLM/Index"),
                    ("Database Chunking", "content", "DatabaseChunking/Index"),
                ],
                "optimize": [
                    ("Performance Tuning", "seo", "PerformanceConfiguration/Index"),
                    ("Update Guide", "upgrade", "UpdateGuide/Index"),
                    ("Screenshots", "screenshots", "Screenshots/Index"),
                ],
                "resources": [
                    ("Known Problems", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Get Extension", "buy", "BuyNow"),
                ],
            },
        },
        "de": {
            "eyebrow": "KI-Universum",
            "hero_title": "T3AS — TYPO3 KI-Suche",
            "hero_subtitle": "KI-gestützte Suche in Ihren TYPO3-Inhalten mit Embeddings, Custom LLM und Performance-Tuning.",
            "prefix": "/de",
            "sections": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Konfiguration", "configuration", "Configuration/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Such-Plugin", "pages", "FrontendPlugin/Index"),
                    ("Custom LLM", "llm", "CustomLLMSupport/Index"),
                    ("Hosting-Richtlinie", "settings", "T3ASHostingPolicyforCustomLLM/Index"),
                    ("Datenbank-Chunking", "content", "DatabaseChunking/Index"),
                ],
                "optimize": [
                    ("Performance", "seo", "PerformanceConfiguration/Index"),
                    ("Update-Anleitung", "upgrade", "UpdateGuide/Index"),
                    ("Screenshots", "screenshots", "Screenshots/Index"),
                ],
                "resources": [
                    ("Bekannte Probleme", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Erweiterung holen", "buy", "BuyNow"),
                ],
            },
        },
    },
    "ExtNsT3AC": {
        "en": {
            "eyebrow": "AI Universe Extensions",
            "hero_title": "T3AC — TYPO3 AI Chatbot",
            "hero_subtitle": "Deploy an AI chatbot trained on your TYPO3 content with analytics, logs, and custom LLM support.",
            "prefix": "",
            "sections": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Configuration", "configuration", "Configuration/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Feature Guide", "features", "FeatureGuide/Index"),
                    ("Custom LLM", "llm", "CustomLLMSupport/Index"),
                    ("Screenshots", "screenshots", "Screenshots/Index"),
                ],
                "optimize": [
                    ("Update Guide", "upgrade", "UpdateGuide/Index"),
                ],
                "resources": [
                    ("Known Problems", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Get Extension", "buy", "BuyNow"),
                ],
            },
        },
        "de": {
            "eyebrow": "KI-Universum",
            "hero_title": "T3AC — TYPO3 KI-Chatbot",
            "hero_subtitle": "KI-Chatbot auf Basis Ihrer TYPO3-Inhalte mit Analysen, Logs und Custom-LLM-Unterstützung.",
            "prefix": "/de",
            "sections": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Konfiguration", "configuration", "Configuration/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Feature Guide", "features", "FeatureGuide/Index"),
                    ("Custom LLM", "llm", "CustomLLMSupport/Index"),
                    ("Screenshots", "screenshots", "Screenshots/Index"),
                ],
                "optimize": [
                    ("Update-Anleitung", "upgrade", "UpdateGuide/Index"),
                ],
                "resources": [
                    ("Bekannte Probleme", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Erweiterung holen", "buy", "BuyNow"),
                ],
            },
        },
    },
    "ExtNsT3AL": {
        "en": {
            "eyebrow": "AI Universe Extensions",
            "hero_title": "T3AL — TYPO3 AI Localization",
            "hero_subtitle": "Automate TYPO3 translations with AI localization, XLIFF workflows, and glossary support.",
            "prefix": "",
            "sections": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Configuration", "configuration", "Configuration/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("AI Localization", "translation", "AILocalization/Index"),
                    ("Manual Localization", "content", "StartManualLocalization/Index"),
                    ("XLIFF Import & Export", "pages", "SeamlessXLIFFImport&Export/Index"),
                    ("T3AL for Everyone", "features", "T3ALforEveryone/Index"),
                ],
                "optimize": [
                    ("Localization Logs", "settings", "AILocalizationLogs/Index"),
                    ("Video Tutorials", "video", "VideoTutorials/Index"),
                    ("Glossary", "prompts", "T3ALTerms(Glossary)/Index"),
                ],
                "resources": [
                    ("Known Problems", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Get Extension", "buy", "BuyNow"),
                ],
            },
        },
        "de": {
            "eyebrow": "KI-Universum",
            "hero_title": "T3AL — TYPO3 KI-Lokalisierung",
            "hero_subtitle": "Automatisieren Sie TYPO3-Übersetzungen mit KI-Lokalisierung, XLIFF-Workflows und Glossar.",
            "prefix": "/de",
            "sections": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Konfiguration", "configuration", "Configuration/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("KI-Lokalisierung", "translation", "AILocalization/Index"),
                    ("Manuelle Lokalisierung", "content", "StartManualLocalization/Index"),
                    ("XLIFF Import & Export", "pages", "SeamlessXLIFFImport&Export/Index"),
                    ("T3AL für alle", "features", "T3ALforEveryone/Index"),
                ],
                "optimize": [
                    ("Lokalisierungs-Logs", "settings", "AILocalizationLogs/Index"),
                    ("Video-Tutorials", "video", "VideoTutorials/Index"),
                    ("Glossar", "prompts", "T3ALTerms(Glossary)/Index"),
                ],
                "resources": [
                    ("Bekannte Probleme", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Erweiterung holen", "buy", "BuyNow"),
                ],
            },
        },
    },
    "ExtNsT3AA": {
        "en": {
            "eyebrow": "AI Universe Extensions",
            "hero_title": "T3AA — TYPO3 AI Accessibility",
            "hero_subtitle": "Improve accessibility with AI alt text, voiceover, CKEditor checks, and simplified text.",
            "prefix": "",
            "sections": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Configuration", "configuration", "Configuration/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("AI FileMeta", "media", "AIFilemeta/Index"),
                    ("AI Audio Generator", "content", "AIAudioGenerator/Index"),
                    ("T3AA Voiceover", "video", "T3AAVoiceover/Index"),
                    ("CKEditor A11y Check", "features", "CkeditorAccessibilityChecker/Index"),
                ],
                "optimize": [
                    ("Simplify Text", "translation", "SimplifiedText/Index"),
                    ("Core Web Vitals", "seo", "SpeedCoreWebVitals/Index"),
                    ("Update Guide", "upgrade", "UpdateGuide/Index"),
                ],
                "resources": [
                    ("Known Problems", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Get Extension", "buy", "BuyNow"),
                ],
            },
        },
        "de": {
            "eyebrow": "KI-Universum",
            "hero_title": "T3AA — TYPO3 KI-Barrierefreiheit",
            "hero_subtitle": "Verbessern Sie Barrierefreiheit mit KI-Alt-Text, Voiceover, CKEditor-Prüfungen und vereinfachtem Text.",
            "prefix": "/de",
            "sections": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Konfiguration", "configuration", "Configuration/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("KI FileMeta", "media", "AIFilemeta/Index"),
                    ("KI Audio Generator", "content", "AIAudioGenerator/Index"),
                    ("T3AA Voiceover", "video", "T3AAVoiceover/Index"),
                    ("CKEditor A11y", "features", "CkeditorAccessibilityChecker/Index"),
                ],
                "optimize": [
                    ("Text vereinfachen", "translation", "SimplifiedText/Index"),
                    ("Core Web Vitals", "seo", "SpeedCoreWebVitals/Index"),
                    ("Update-Anleitung", "upgrade", "UpdateGuide/Index"),
                ],
                "resources": [
                    ("Bekannte Probleme", "known", "KnownProblems/Index"),
                    ("Support", "support", "Support"),
                    ("Erweiterung holen", "buy", "BuyNow"),
                ],
            },
        },
    },
    "ExtNsT3AB": {
        "en": {
            "eyebrow": "AI Universe Extensions",
            "hero_title": "T3AB — TYPO3 AI Builder",
            "hero_subtitle": "Build TYPO3 content elements, forms, and blocks with AI-assisted workflows.",
            "prefix": "",
            "sections": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Configuration", "configuration", "Configuration/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("How T3AB Works", "introduction", "HowT3ABWorks/Index"),
                    ("AI Builder", "features", "T3ABAIBuilder/Index"),
                    ("Content Blocks", "content", "T3ABContentBlocks/Index"),
                    ("Forms", "pages", "Forms/Index"),
                ],
                "optimize": [
                    ("Update Guide", "upgrade", "UpdateGuide/Index"),
                ],
                "resources": [
                    ("Support", "support", "Support"),
                    ("Get Extension", "buy", "BuyNow"),
                ],
            },
        },
        "de": {
            "eyebrow": "KI-Universum",
            "hero_title": "T3AB — TYPO3 KI-Builder",
            "hero_subtitle": "Erstellen Sie TYPO3-Inhaltselemente, Formulare und Blöcke mit KI-gestützten Workflows.",
            "prefix": "/de",
            "sections": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Konfiguration", "configuration", "Configuration/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("So funktioniert T3AB", "introduction", "HowT3ABWorks/Index"),
                    ("KI-Builder", "features", "T3ABAIBuilder/Index"),
                    ("Content Blocks", "content", "T3ABContentBlocks/Index"),
                    ("Formulare", "pages", "Forms/Index"),
                ],
                "optimize": [
                    ("Update-Anleitung", "upgrade", "UpdateGuide/Index"),
                ],
                "resources": [
                    ("Support", "support", "Support"),
                    ("Erweiterung holen", "buy", "BuyNow"),
                ],
            },
        },
    },
}

SECTIONS_EN = {
    "get_started": ("Get started", "Installation & setup"),
    "configure": ("Build", "Features & configuration"),
    "optimize": ("Advanced", "Upgrades & optimization"),
    "resources": ("Resources", "Help & support"),
}
SECTIONS_DE = {
    "get_started": ("Erste Schritte", "Installation & Einrichtung"),
    "configure": ("Entwickeln", "Funktionen & Konfiguration"),
    "optimize": ("Erweitert", "Upgrades & Optimierung"),
    "resources": ("Ressourcen", "Hilfe & Support"),
}

ICON = {
    "introduction": "book-open",
    "installation": "download",
    "configuration": "settings",
    "update": "refresh-cw",
    "pages": "file-text",
    "content": "pen-line",
    "seo": "search",
    "settings": "sliders-horizontal",
    "prompts": "message-square",
    "translation": "languages",
    "media": "image",
    "video": "play-circle",
    "upgrade": "arrow-up",
    "faq": "circle-question-mark",
    "support": "life-buoy",
    "buy": "shopping-cart",
    "features": "bot",
    "llm": "cpu",
    "screenshots": "camera",
    "known": "triangle-alert",
}


def read_fm(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.S)
    return m.group(0) if m else ""


def render_product(slug: str, locale: dict, lang: str) -> str:
    sections = SECTIONS_DE if lang == "de" else SECTIONS_EN
    lines = [
        '<div className="t3-template-landing">',
        '  <div className="t3-landing-hero">',
        f'    <p className="t3-landing-eyebrow">{locale["eyebrow"]}</p>',
        f'    <h1 className="t3-landing-title">{locale["hero_title"]}</h1>',
        f'    <p className="t3-landing-subtitle">{locale["hero_subtitle"]}</p>',
        "  </div>",
        "",
    ]
    for key in ("get_started", "configure", "optimize", "resources"):
        cards = locale["sections"].get(key, [])
        if not cards:
            continue
        eyebrow, title = sections[key]
        lines.append('<section className="t3-landing-section">')
        lines.append(f'  <p className="t3-landing-eyebrow">{eyebrow}</p>')
        lines.append(f'  <h2 className="t3-landing-section-title">{title}</h2>')
        lines.append("  <CardGroup cols={2}>")
        for card_title, meta, page in cards:
            href = f"{locale['prefix']}/{slug}/{page}"
            icon = ICON.get(meta, "file-text")
            lines.append(f'  <Card title="{card_title}" icon="{icon}" href="{href}" />')
        lines.append("  </CardGroup>")
        lines.append("</section>")
        lines.append("")
    lines.append("</div>")
    return "\n".join(lines)


def main():
    updated = 0
    for slug, locales in AI_PRODUCTS.items():
        for lang in ("en", "de"):
            path = ROOT / ("de/" if lang == "de" else "") / slug / "Index.md"
            if not path.exists():
                continue
            body = render_product(slug, locales[lang], lang)
            path.write_text(read_fm(path) + "\n" + body, encoding="utf-8")
            updated += 1
            print(f"Updated {path.relative_to(ROOT)}")
    print(f"Done. {updated} AI landing pages.")


if __name__ == "__main__":
    main()
    from sync_doc_stats import sync_homepage_stats
    sync_homepage_stats()
