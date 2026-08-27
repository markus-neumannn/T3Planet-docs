#!/usr/bin/env python3
"""Generate Coinbase-style hub landing pages and home page from docs.json catalog."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UPPER_WORDS = {
    "t3ai", "t3ac", "t3as", "t3al", "t3aa", "t3ab",
    "faq", "pwa", "seo", "crm", "rte", "llm", "ai", "api",
}

SPECIAL_PHRASES = {
    "ckeditor pack": "CKEditor Pack",
    "ckeditor": "CKEditor",
    "sitekit": "Site Kit",
    "zoho crm": "Zoho CRM",
}


def beautify_words(text: str) -> str:
    lower = text.lower()
    for phrase, replacement in SPECIAL_PHRASES.items():
        if lower == phrase:
            return replacement
    words = text.split()
    out = []
    for w in words:
        wl = w.lower()
        if wl in UPPER_WORDS:
            out.append(wl.upper())
        elif wl.startswith("t3") and len(wl) <= 5:
            out.append(wl.upper())
        else:
            out.append(w.capitalize())
    return " ".join(out)


def format_extension_display_name(raw: str) -> str:
    s = raw.strip()
    if not s.upper().startswith("EXT:"):
        return s
    s = s[4:]
    for prefix in ("ns_", "nitsan_", "rte_"):
        if s.lower().startswith(prefix):
            s = s[len(prefix) :]
            break
    return "NS " + beautify_words(s.replace("_", " "))


SLUG_DISPLAY_OVERRIDES = {
    "ExtRTECKEditorPack": "NS CKEditor Pack",
    "EXTNsZohoCrm": "NS Zoho CRM",
}

LUCIDE_ALIASES = {
    "help-circle": "circle-question-mark",
    "bar-chart-3": "chart-column",
    "user-circle": "circle-user",
    "instagram": "camera",
    "twitter": "x",
    "youtube": "circle-play",
    "code-2": "square-code",
    "puzzle-piece": "puzzle",
    "contact": "contact-round",
    "circle-help": "circle-question-mark",
}


def normalize_icon(name: str | None) -> str:
    if not name:
        return "puzzle"
    return LUCIDE_ALIASES.get(name, name)


def icon_tag(name: str, size: int = 22, cls: str = "t3-product-icon") -> str:
    icon = normalize_icon(name)
    shell = "t3-extension-icon-shell" if cls == "t3-extension-icon" else "t3-product-icon-shell"
    return (
        f'<span className="t3-icon-shell {shell}">'
        f'<Icon icon="{icon}" size={{{size}}} className="{cls}" />'
        f"</span>"
    )


def format_slug_display_name(slug: str) -> str:
    if slug in SLUG_DISPLAY_OVERRIDES:
        return SLUG_DISPLAY_OVERRIDES[slug]
    name = slug
    for prefix in ("ExtNs", "EXTNs", "ExtNitsan", "ExtRTEC"):
        if name.startswith(prefix):
            name = name[len(prefix) :]
            break
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    spaced = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", spaced)
    return "NS " + beautify_words(spaced.replace("_", " "))

AI_SLUGS = {
    "ExtNsT3AI",
    "ExtNsT3AC",
    "ExtNsT3AS",
    "ExtNsT3AL",
    "ExtNsT3AA",
    "ExtNsT3AB",
}

TEMPLATE_SLUGS = {
    "ExtThemes",
    "EXTKarma",
    "EXTAvatar",
    "EXTAyu",
    "EXTBootstrap",
    "EXTReactBootstrap",
    "EXTReva",
    "EXTShiva",
    "EXTShop",
}

SKIP_DROPDOWNS = {
    "Home",
    "Startseite",
    "License, Installation & Updates",
    "Lizenz, Installation und Updates",
    "All Extensions",
    "Alle Erweiterungen",
    "All AI Products",
    "Alle KI-Produkte",
    "All Templates",
    "Alle Vorlagen",
}

AI_META = {
    "ExtNsT3AI": {
        "icon": "sparkles",
        "name": "T3AI",
        "tagline_en": "AI Content & SEO",
        "tagline_de": "KI-Inhalte & SEO",
        "desc_en": "Generate content, translations, SEO metadata, and media with AI directly inside TYPO3.",
        "desc_de": "Erstellen Sie Inhalte, Übersetzungen, SEO-Metadaten und Medien mit KI direkt in TYPO3.",
        "features_en": ["AI content & pages", "SEO automation", "Translation & media"],
        "features_de": ["KI-Inhalte & Seiten", "SEO-Automatisierung", "Übersetzung & Medien"],
    },
    "ExtNsT3AC": {
        "icon": "message-circle",
        "name": "T3AC",
        "tagline_en": "AI Chatbot",
        "tagline_de": "KI-Chatbot",
        "desc_en": "Deploy an AI chatbot trained on your TYPO3 content with analytics, logs, and custom LLM support.",
        "desc_de": "KI-Chatbot auf Basis Ihrer TYPO3-Inhalte mit Analysen, Logs und Custom-LLM-Unterstützung.",
        "features_en": ["Content-trained chatbot", "Custom LLM", "Analytics & logs"],
        "features_de": ["Inhaltsbasierter Chatbot", "Custom LLM", "Analysen & Logs"],
    },
    "ExtNsT3AS": {
        "icon": "search",
        "name": "T3AS",
        "tagline_en": "AI Search",
        "tagline_de": "KI-Suche",
        "desc_en": "AI-powered search across your TYPO3 content with embeddings, custom LLM, and performance tuning.",
        "desc_de": "KI-gestützte Suche in Ihren TYPO3-Inhalten mit Embeddings, Custom LLM und Performance-Tuning.",
        "features_en": ["Semantic search", "Embeddings", "Performance tuning"],
        "features_de": ["Semantische Suche", "Embeddings", "Performance-Tuning"],
    },
    "ExtNsT3AL": {
        "icon": "languages",
        "name": "T3AL",
        "tagline_en": "AI Localization",
        "tagline_de": "KI-Lokalisierung",
        "desc_en": "Automate TYPO3 translations with AI localization, XLIFF workflows, and glossary support.",
        "desc_de": "Automatisieren Sie TYPO3-Übersetzungen mit KI-Lokalisierung, XLIFF-Workflows und Glossar.",
        "features_en": ["AI translation", "XLIFF import/export", "Glossary support"],
        "features_de": ["KI-Übersetzung", "XLIFF Import/Export", "Glossar-Unterstützung"],
    },
    "ExtNsT3AA": {
        "icon": "accessibility",
        "name": "T3AA",
        "tagline_en": "AI Accessibility",
        "tagline_de": "KI-Barrierefreiheit",
        "desc_en": "Improve accessibility with AI alt text, voiceover, CKEditor checks, and simplified text.",
        "desc_de": "Verbessern Sie Barrierefreiheit mit KI-Alt-Text, Voiceover, CKEditor-Prüfungen und vereinfachtem Text.",
        "features_en": ["AI alt text", "Voiceover", "A11y checker"],
        "features_de": ["KI-Alt-Text", "Voiceover", "A11y-Prüfung"],
    },
    "ExtNsT3AB": {
        "icon": "blocks",
        "name": "T3AB",
        "tagline_en": "AI Builder",
        "tagline_de": "KI-Builder",
        "desc_en": "Build TYPO3 content elements, forms, and blocks with AI-assisted workflows.",
        "desc_de": "Erstellen Sie TYPO3-Inhaltselemente, Formulare und Blöcke mit KI-gestützten Workflows.",
        "features_en": ["AI content blocks", "Form builder", "Workflow automation"],
        "features_de": ["KI-Inhaltsblöcke", "Formular-Builder", "Workflow-Automatisierung"],
    },
}

TEMPLATE_META = {
    "ExtThemes": {
        "icon": "layout-template",
        "name_en": "TYPO3 Templates",
        "name_de": "TYPO3-Vorlagen",
        "category_en": "Overview",
        "category_de": "Überblick",
        "desc_en": "Central hub for all T3Planet TYPO3 theme documentation — installation, configuration, and customization.",
        "desc_de": "Zentrale Dokumentation für alle T3Planet TYPO3-Themes — Installation, Konfiguration und Anpassung.",
    },
    "EXTKarma": {
        "icon": "palette",
        "name_en": "T3 Karma",
        "name_de": "T3 Karma",
        "category_en": "Business",
        "category_de": "Business",
        "desc_en": "Premium business theme with content blocks, SEO tools, and full TYPO3 v13/v14 upgrade paths.",
        "desc_de": "Premium-Business-Theme mit Inhaltsblöcken, SEO-Tools und Upgrade-Pfaden für TYPO3 v13/v14.",
    },
    "EXTAvatar": {
        "icon": "circle-user",
        "name_en": "T3 Avatar",
        "name_de": "T3 Avatar",
        "category_en": "Portfolio",
        "category_de": "Portfolio",
        "desc_en": "Creative portfolio theme with Mask elements, editor guides, and performance optimization.",
        "desc_de": "Kreatives Portfolio-Theme mit Mask-Elementen, Redakteur-Leitfäden und Performance-Optimierung.",
    },
    "EXTAyu": {
        "icon": "zap",
        "name_en": "T3 Ayu",
        "name_de": "T3 Ayu",
        "category_en": "React",
        "category_de": "React",
        "desc_en": "Modern React.js-powered theme with preview features, demo site, and Mask-based elements.",
        "desc_de": "Modernes React.js-Theme mit Vorschaufunktion, Demo-Site und Mask-basierten Elementen.",
    },
    "EXTBootstrap": {
        "icon": "grid-3x3",
        "name_en": "T3 Bootstrap",
        "name_de": "T3 Bootstrap",
        "category_en": "Bootstrap",
        "category_de": "Bootstrap",
        "desc_en": "Bootstrap-based TYPO3 theme with custom elements, SEO configuration, and upgrade guides.",
        "desc_de": "Bootstrap-basiertes TYPO3-Theme mit benutzerdefinierten Elementen, SEO-Konfiguration und Upgrade-Anleitungen.",
    },
    "EXTReactBootstrap": {
        "icon": "square-code",
        "name_en": "T3 ReactBootstrap",
        "name_de": "T3 ReactBootstrap",
        "category_en": "React + Bootstrap",
        "category_de": "React + Bootstrap",
        "desc_en": "React.js and Bootstrap combined — custom elements, localization, and frontend build pipeline.",
        "desc_de": "React.js und Bootstrap kombiniert — benutzerdefinierte Elemente, Lokalisierung und Frontend-Build.",
    },
    "EXTReva": {
        "icon": "sparkle",
        "name_en": "T3 Reva",
        "name_de": "T3 Reva",
        "category_en": "React",
        "category_de": "React",
        "desc_en": "Elegant React.js theme with preview, demo site, and comprehensive customization options.",
        "desc_de": "Elegantes React.js-Theme mit Vorschau, Demo-Site und umfassenden Anpassungsoptionen.",
    },
    "EXTShiva": {
        "icon": "mountain",
        "name_en": "T3 Shiva",
        "name_de": "T3 Shiva",
        "category_en": "React",
        "category_de": "React",
        "desc_en": "Feature-rich React.js theme with custom elements, localization, and performance tuning.",
        "desc_de": "Funktionsreiches React.js-Theme mit benutzerdefinierten Elementen, Lokalisierung und Performance-Tuning.",
    },
    "EXTShop": {
        "icon": "shopping-bag",
        "name_en": "T3 Shop",
        "name_de": "T3 Shop",
        "category_en": "E-Commerce",
        "category_de": "E-Commerce",
        "desc_en": "TYPO3 e-commerce theme with shop configuration, product pages, and checkout setup.",
        "desc_de": "TYPO3-E-Commerce-Theme mit Shop-Konfiguration, Produktseiten und Checkout-Einrichtung.",
    },
}

EXT_CATEGORY = {
    "ExtRTECKEditorPack": ("Editor", "Editor"),
    "ExtNsNewsComments": ("News & Comments", "News & Kommentare"),
    "ExtNsRevolutionSlider": ("Sliders", "Slider"),
    "ExtNsAllChat": ("Chat", "Chat"),
    "ExtNsAllLightbox": ("Media", "Medien"),
    "ExtNsAllSliders": ("Sliders", "Slider"),
    "ExtNsBackup": ("System", "System"),
    "ExtNsCloudflare": ("Performance", "Performance"),
    "ExtNsComments": ("Comments", "Kommentare"),
    "ExtNsCookieYes": ("Privacy", "Datenschutz"),
    "ExtNsCookiebot": ("Privacy", "Datenschutz"),
    "ExtNsCookiesHint": ("Privacy", "Datenschutz"),
    "ExtNsDisqusComment": ("Comments", "Kommentare"),
    "ExtNsExtCompatibility": ("System", "System"),
    "ExtNsEvent": ("Content", "Inhalte"),
    "ExtNsFacebookComment": ("Comments", "Kommentare"),
    "ExtNsFAQ": ("Content", "Inhalte"),
    "ExtNsFeedback": ("Forms", "Formulare"),
    "ExtNsFriendlyCaptcha": ("Forms", "Formulare"),
    "ExtNsGallery": ("Media", "Medien"),
    "ExtNsGoogleDocs": ("Integration", "Integration"),
    "ExtNsGoogleMap": ("Maps", "Karten"),
    "ExtNsGoogleSiteKit": ("Analytics", "Analytics"),
    "ExtNsGridtoContainer": ("Migration", "Migration"),
    "ExtNsGuestbook": ("Forms", "Formulare"),
    "ExtNitsanHellobar": ("Marketing", "Marketing"),
    "ExtNsHelpDesk": ("Support", "Support"),
    "ExtNsHubspot": ("Integration", "Integration"),
    "ExtNsInstagram": ("Social", "Social Media"),
    "ExtNsLazyload": ("Performance", "Performance"),
    "ExtNitsanMaintenance": ("System", "System"),
    "ExtNsNewsAdvancedSearch": ("News", "News"),
    "ExtNsNewsSlickSlider": ("News", "News"),
    "ExtNsNewsSlider": ("News", "News"),
    "ExtNsOpenStreetMap": ("Maps", "Karten"),
    "ExtNsPersonio": ("Integration", "Integration"),
    "ExtNsProtectSite": ("Security", "Sicherheit"),
    "ExtNsPublicationComment": ("Comments", "Kommentare"),
    "ExtNsPWA": ("Performance", "Performance"),
    "ExtNsSharethis": ("Social", "Social Media"),
    "ExtNsSnow": ("Effects", "Effekte"),
    "ExtNsStatcounter": ("Analytics", "Analytics"),
    "ExtNsSocialLogin": ("Social", "Social Media"),
    "ExtNsTimeLine": ("Content", "Inhalte"),
    "ExtNsTwitter": ("Social", "Social Media"),
    "ExtNsWhatsapp": ("Social", "Social Media"),
    "ExtNsWpMigration": ("Migration", "Migration"),
    "ExtNsCacheWebhook": ("Performance", "Performance"),
    "ExtNsYoutube": ("Media", "Medien"),
    "ExtNsZoho": ("Integration", "Integration"),
    "EXTNsZohoCrm": ("Integration", "Integration"),
}


def _walk_nav_pages(node, acc: list[str]) -> None:
    if isinstance(node, str):
        acc.append(node)
    elif isinstance(node, dict):
        if "pages" in node:
            for p in node["pages"]:
                _walk_nav_pages(p, acc)
    elif isinstance(node, list):
        for item in node:
            _walk_nav_pages(item, acc)


def _collect_product_groups(groups: list, lang: str) -> list[dict]:
    """Extract nested product groups from unified sidebar tree."""
    products = []
    section_keys = {
        "T3AF", "KI-Universum",
        "T3 Templates & Themes", "TYPO3 Extensions", "TYPO3 Erweiterungen",
    }

    def walk(group_list: list, in_product_section: bool = False) -> None:
        for g in group_list:
            if not isinstance(g, dict) or "group" not in g:
                continue
            name = g["group"]
            pages = g.get("pages", [])
            is_section = name in section_keys or name in ("Get Started", "Erste Schritte")

            if g.get("root") and pages:
                root = g["root"]
                slug = root.split("/")[-2] if root.endswith("/Index") else root.split("/")[0]
                if lang == "de" and slug == "de":
                    slug = root.split("/")[1]
                if slug in AI_SLUGS:
                    category = "ai"
                elif slug in TEMPLATE_SLUGS:
                    category = "template"
                elif slug == "License":
                    continue
                else:
                    category = "extension"
                disk = ROOT / f"{root}.md"
                if disk.exists():
                    prefix = "/de" if lang == "de" else ""
                    products.append(
                        {
                            "slug": slug,
                            "dropdown": name,
                            "icon": normalize_icon(g.get("icon")),
                            "category": category,
                            "nav_path": root,
                            "href": f"{prefix}/{slug}/Index",
                            "has_update": (ROOT / (f"de/{slug}" if lang == "de" else slug) / "UpdateVersion" / "Index.md").exists(),
                            "has_install": (ROOT / (f"de/{slug}" if lang == "de" else slug) / "Installation" / "Index.md").exists(),
                        }
                    )
            elif is_section or pages:
                nested = [p for p in pages if isinstance(p, dict) and "group" in p]
                if nested:
                    walk(nested, True)
                elif in_product_section:
                    walk([{"group": name, **g}] if "root" not in g else [g], True)

    walk(groups)
    return products


def parse_catalog(lang: str) -> list[dict]:
    docs = json.loads((ROOT / "docs.json").read_text())
    for entry in docs["navigation"]["languages"]:
        if entry["language"] != lang:
            continue
        if entry.get("groups"):
            return _collect_product_groups(entry["groups"], lang)
        products = []
        prefix = "/de" if lang == "de" else ""
        for dropdown in entry.get("dropdowns", []):
            name = dropdown["dropdown"]
            if name in SKIP_DROPDOWNS:
                continue
            pages = []
            for group in dropdown.get("groups", []):
                pages.extend(group.get("pages", []))
            if not pages:
                pages = dropdown.get("pages", [])
            if not pages:
                continue
            nav_path = pages[0]
            slug = nav_path.split("/")[-2] if nav_path.endswith("/Index") else nav_path.split("/")[0]
            if lang == "de" and slug == "de":
                slug = nav_path.split("/")[1]
            if slug in AI_SLUGS:
                category = "ai"
            elif slug in TEMPLATE_SLUGS:
                category = "template"
            else:
                category = "extension"
            disk = ROOT / f"{nav_path}.md"
            if not disk.exists():
                continue
            products.append(
                {
                    "slug": slug,
                    "dropdown": name,
                    "icon": normalize_icon(dropdown.get("icon")),
                    "category": category,
                    "nav_path": nav_path,
                    "href": f"{prefix}/{slug}/Index",
                    "has_update": (ROOT / (f"de/{slug}" if lang == "de" else slug) / "UpdateVersion" / "Index.md").exists(),
                    "has_install": (ROOT / (f"de/{slug}" if lang == "de" else slug) / "Installation" / "Index.md").exists(),
                }
            )
        return products
    return []


def read_description(slug: str, lang: str) -> str:
    path = ROOT / ("de/" if lang == "de" else "") / slug / "Index.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    m = re.search(r'^description:\s*"(.+?)"', text, re.M)
    if m:
        desc = m.group(1)
        if " – Official T3Planet" in desc:
            desc = desc.split(" – Official T3Planet")[0]
        return desc
    return ""


def fm(title: str, description: str, sidebar: str, keywords: list[str]) -> str:
    kw = "\n".join(f'  - "{k}"' for k in keywords)
    return (
        f"---\ntitle: \"{title}\"\n"
        f"description: \"{description}\"\n"
        f"keywords:\n{kw}\n"
        f"sidebarTitle: \"{sidebar}\"\n---\n"
    )


def hub_nav(lang: str, active: str) -> str:
    prefix = "/de" if lang == "de" else ""
    home_href = "/de/index" if lang == "de" else "/"
    items = [
        ("home", home_href, "Home" if lang == "en" else "Startseite"),
        ("ai", f"{prefix}/AIFoundationExtensions/Index", "AI Universe Extensions" if lang == "en" else "KI-Universum"),
        ("templates", f"{prefix}/AllTemplates/Index", "TYPO3 Templates & Themes" if lang == "en" else "Vorlagen"),
        ("extensions", f"{prefix}/AllExtensions/Index", "TYPO3 Extensions" if lang == "en" else "Erweiterungen"),
    ]
    links = []
    for key, href, label in items:
        cls = "active" if key == active else ""
        links.append(f'<a className="{cls}" href="{href}">{label}</a>')
    return f'<nav className="t3-category-nav">{"".join(links)}</nav>'


def render_stats_bar(lang: str) -> str:
    from compute_doc_stats import render_stats_bar as _render

    if lang == "de":
        return _render(
            lang,
            [
                ("pages", "Dokumentationsseiten"),
                ("products", "Produkte"),
                ("languages", "Sprachen"),
            ],
        )
    return _render(
        lang,
        [
            ("pages", "Documentation pages"),
            ("products", "Products"),
            ("languages", "Languages"),
        ],
    )


def render_hero_panel(lang: str, eyebrow: str, title: str, subtitle: str) -> str:
    search = "Search documentation..." if lang == "en" else "Dokumentation durchsuchen..."
    return f"""<div className="t3-hero-panel">
  <div className="t3-landing-hero t3-hero-large">
    <p className="t3-landing-eyebrow">{eyebrow}</p>
    <h1 className="t3-landing-title">{title}</h1>
    <p className="t3-landing-subtitle">{subtitle}</p>
    <button type="button" className="t3-search-trigger" data-t3-search-trigger aria-label="{search}">
      <span>{search}</span>
      <kbd>⌘K</kbd>
    </button>
  </div>
</div>"""


def render_recent_section(lang: str) -> str:
    prefix = "/de" if lang == "de" else ""
    if lang == "de":
        eyebrow, heading = "Aktuell", "Häufig aktualisierte Anleitungen"
        items = [
            (f"{prefix}/License/UpdateVersion/Index", "↻", "Version aktualisieren"),
            (f"{prefix}/ExtNsT3AI/UpdateVersion/Index", "✦", "T3AI Updates"),
            (f"{prefix}/ExtNsT3AC/UpdateVersion/Index", "💬", "T3AC Updates"),
            (f"{prefix}/EXTKarma/UpdateVersion/Index", "🎨", "T3 Karma Updates"),
            (f"{prefix}/License/Migration/Index", "⇄", "Migrations-Anleitung"),
            (f"{prefix}/ExtNsT3AS/UpdateGuide/Index", "🔍", "T3AS Update Guide"),
        ]
    else:
        eyebrow, heading = "Recently updated", "Frequently referenced guides"
        items = [
            (f"{prefix}/License/UpdateVersion/Index", "↻", "Update version"),
            (f"{prefix}/ExtNsT3AI/UpdateVersion/Index", "✦", "T3AI updates"),
            (f"{prefix}/ExtNsT3AC/UpdateVersion/Index", "💬", "T3AC updates"),
            (f"{prefix}/EXTKarma/UpdateVersion/Index", "🎨", "T3 Karma updates"),
            (f"{prefix}/License/Migration/Index", "⇄", "Migration guide"),
            (f"{prefix}/ExtNsT3AS/UpdateGuide/Index", "🔍", "T3AS update guide"),
        ]
    recent = "".join(
        f'<a className="t3-recent-item" href="{href}">'
        f'<span className="t3-recent-icon">{icon}</span>{label}</a>'
        for href, icon, label in items
    )
    return f"""<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">{eyebrow}</p>
  <h2 className="t3-landing-section-title">{heading}</h2>
  <div className="t3-recent-grid">{recent}</div>
</section>"""


def render_ai_hub(lang: str) -> str:
    prefix = "/de" if lang == "de" else ""
    if lang == "de":
        title = "KI-Universum"
        hero = "TYPO3-KI-Lösungen von T3Planet"
        sub = "Chatbots, Suche, Lokalisierung, Barrierefreiheit und Content-Automatisierung — alles in einem KI-Ökosystem für TYPO3."
        section = "Alle KI-Produkte"
    else:
        title = "AI Universe Extensions"
        hero = "TYPO3 AI solutions by T3Planet"
        sub = "Chatbots, search, localization, accessibility, and content automation — one AI ecosystem built for TYPO3."
        section = "All AI products"

    lines = [
        '<div className="t3-hub-landing t3-template-landing">',
        hub_nav(lang, "ai"),
        render_hero_panel(lang, title, hero, sub),
        render_stats_bar(lang),
        f'<section className="t3-landing-section">',
        f'  <p className="t3-landing-eyebrow">{section}</p>',
        '  <div className="t3-product-grid">',
    ]
    for slug in ["ExtNsT3AI", "ExtNsT3AC", "ExtNsT3AS", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB"]:
        meta = AI_META[slug]
        name = meta["name"]
        tagline = meta[f"tagline_{lang}"]
        desc = meta[f"desc_{lang}"]
        features = meta[f"features_{lang}"]
        install_label = "Installation" if lang == "en" else "Installation"
        feat_html = "".join(f'<span className="t3-feature-tag">{f}</span>' for f in features)
        doc_href = f"{prefix}/{slug}/Index"
        lines.extend([
            '    <a className="t3-product-card" href="' + doc_href + '">',
            f'      <div className="t3-product-card-header">',
            f'        {icon_tag(meta["icon"])}',
            f'        <div>',
            f'          <h3 className="t3-product-name">{name}</h3>',
            f'          <p className="t3-product-tagline">{tagline}</p>',
            f'        </div>',
            f'      </div>',
            f'      <p className="t3-product-desc">{desc}</p>',
            f'      <div className="t3-feature-tags">{feat_html}</div>',
            f'      <div className="t3-product-links">',
            f'        <span className="t3-link-pill">{install_label}</span>',
            f'        <span className="t3-link-pill t3-link-pill-muted">Update</span>',
            f'      </div>',
            '    </a>',
        ])
    lines.extend(["  </div>", "</section>", "", "</div>"])
    return "\n".join(lines)


def render_template_hub(lang: str) -> str:
    prefix = "/de" if lang == "de" else ""
    if lang == "de":
        hero_title = "Alle TYPO3-Vorlagen"
        hero_sub = "Durchsuchen Sie alle T3Planet TYPO3-Themes — von Business-Templates bis zu React.js- und E-Commerce-Lösungen."
        section = "Vorlagen-Katalog"
    else:
        hero_title = "All TYPO3 Templates & Themes"
        hero_sub = "Browse every T3Planet TYPO3 theme — from business templates to React.js and e-commerce solutions."
        section = "Template catalog"

    eyebrow = "TYPO3 Templates & Themes" if lang == "en" else "TYPO3-Vorlagen"
    lines = [
        '<div className="t3-hub-landing t3-template-landing">',
        hub_nav(lang, "templates"),
        render_hero_panel(lang, eyebrow, hero_title, hero_sub),
        render_stats_bar(lang),
        f'<section className="t3-landing-section">',
        f'  <p className="t3-landing-eyebrow">{section}</p>',
        '  <div className="t3-product-grid">',
    ]
    for slug in ["ExtThemes", "EXTKarma", "EXTAvatar", "EXTAyu", "EXTBootstrap", "EXTReactBootstrap", "EXTReva", "EXTShiva", "EXTShop"]:
        meta = TEMPLATE_META[slug]
        name = meta[f"name_{lang}"]
        cat = meta[f"category_{lang}"]
        desc = meta[f"desc_{lang}"]
        doc_href = f"{prefix}/{slug}/Index"
        lines.extend([
            f'    <a className="t3-product-card" href="{doc_href}">',
            f'      <div className="t3-product-card-header">',
            f'        {icon_tag(meta["icon"])}',
            f'        <div>',
            f'          <h3 className="t3-product-name">{name}</h3>',
            f'          <span className="t3-category-badge">{cat}</span>',
            f'        </div>',
            f'      </div>',
            f'      <p className="t3-product-desc">{desc}</p>',
            f'      <div className="t3-product-links">',
            f'        <span className="t3-link-pill">{"View docs" if lang == "en" else "Dokumentation"}</span>',
            f'      </div>',
            f'    </a>',
        ])
    lines.extend(["  </div>", "</section>", "", "</div>"])
    return "\n".join(lines)


def render_extensions_hub(lang: str) -> str:
    prefix = "/de" if lang == "de" else ""
    products = [p for p in parse_catalog(lang) if p["category"] == "extension"]
    products.sort(key=lambda p: (EXT_CATEGORY.get(p["slug"], ("Other", "Sonstige"))[0], p["dropdown"]))

    if lang == "de":
        hero_title = "Alle TYPO3-Erweiterungen"
        hero_sub = "Vollständiger Katalog aller T3Planet TYPO3-Erweiterungen — Kommentare, Medien, Integrationen, Performance und mehr."
        section = "Erweiterungs-Katalog"
        view = "Dokumentation"
        update = "Update"
        sidebar_tip = (
            '<Tip>Öffnen Sie <strong>Alle Erweiterungen</strong> im Produktmenü oben in der Seitenleiste, '
            "um nach Kategorie zu allen Erweiterungen zu springen.</Tip>"
        )
    else:
        hero_title = "All TYPO3 Extensions"
        hero_sub = "Complete catalog of every T3Planet TYPO3 extension — comments, media, integrations, performance, and more."
        section = "Extension catalog"
        view = "View docs"
        update = "Update"
        sidebar_tip = (
            '<Tip>Open <strong>All Extensions</strong> in the product menu at the top of the sidebar '
            "to jump to any extension by category.</Tip>"
        )

    eyebrow = "TYPO3 Extensions" if lang == "en" else "TYPO3-Erweiterungen"
    by_cat: dict[str, list] = {}
    for p in products:
        cat_en, cat_de = EXT_CATEGORY.get(p["slug"], ("Extension", "Erweiterung"))
        cat = cat_de if lang == "de" else cat_en
        by_cat.setdefault(cat, []).append(p)

    lines = [
        '<div className="t3-hub-landing t3-template-landing">',
        hub_nav(lang, "extensions"),
        render_hero_panel(lang, eyebrow, hero_title, hero_sub),
        render_stats_bar(lang),
        sidebar_tip,
    ]
    for cat in sorted(by_cat.keys()):
        lines.extend([
            f'<section className="t3-landing-section t3-extension-section">',
            f'  <p className="t3-landing-eyebrow">{cat}</p>',
            '  <div className="t3-extension-list">',
        ])
        for p in by_cat[cat]:
            update_badge = (
                f'<span className="t3-extension-badge">Update</span>'
                if p["has_update"]
                else ""
            )
            lines.append(
                f'    <a className="t3-extension-row" href="{p["href"]}">'
                f'<span className="t3-extension-row-start">'
                f'{icon_tag(p["icon"], size=18, cls="t3-extension-icon")}'
                f'<span className="t3-extension-name">{p["dropdown"]}</span></span>'
                f'<span className="t3-extension-meta">{update_badge}'
                f'<span className="t3-category-badge">{cat}</span></span></a>'
            )
        lines.extend(["  </div>", "</section>"])
    lines.extend(["", "</div>"])
    return "\n".join(lines)


def render_home(lang: str) -> str:
    prefix = "/de" if lang == "de" else ""
    hub_ai = f"{prefix}/T3AF/Index"
    hub_tpl = f"{prefix}/AllTemplates/Index"
    hub_ext = f"{prefix}/AllExtensions/Index"
    license = f"{prefix}/License/Index"

    if lang == "de":
        return f"""---
title: "Willkommen bei T3Planet Docs"
description: "Offizielle T3Planet-Dokumentation für TYPO3-Erweiterungen, Templates, KI-Lösungen, Lizenzierung, Installation und Konfiguration."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TYPO3 Erweiterungen"
  - "TYPO3 Templates"
  - "Dokumentation"
sidebarTitle: "Startseite"
---

<div className="t3-home-landing">

{hub_nav(lang, "home")}
{render_hero_panel(lang, "T3Planet Dokumentation", "Willkommen bei T3Planet Docs", "Schneller entwickeln mit TYPO3-Erweiterungen, Templates und KI — offizielle Anleitungen für Installation, Lizenzierung, Konfiguration und Updates.")}
{render_stats_bar(lang)}

<CardGroup cols={{4}}>
  <Card title="Erste Schritte" icon="rocket" href="{license}">
    Lizenz, Installation und Updates für alle T3Planet-Produkte.
  </Card>
  <Card title="KI-Universum" icon="bot" href="{hub_ai}">
    6 KI-Produkte — Chatbot, Suche, Lokalisierung, Barrierefreiheit und mehr.
  </Card>
  <Card title="Vorlagen" icon="layout-template" href="{hub_tpl}">
    9 TYPO3-Themes — Business, React.js und E-Commerce.
  </Card>
  <Card title="Erweiterungen" icon="puzzle" href="{hub_ext}">
    50+ TYPO3-Erweiterungen — Kommentare, Medien, Integrationen und mehr.
  </Card>
</CardGroup>

<section className="t3-landing-section">
  <div className="t3-section-header">
    <div>
      <p className="t3-landing-eyebrow">KI-Universum</p>
      <h2 className="t3-landing-section-title">TYPO3-KI-Lösungen</h2>
    </div>
    <a className="t3-view-all" href="{hub_ai}">Alle anzeigen →</a>
  </div>
  <CardGroup cols={{3}}>
    <Card title="T3AI — KI-Inhalte &amp; SEO" icon="sparkles" href="{prefix}/ExtNsT3AI/Index">Inhalte, Übersetzungen und SEO mit KI generieren.</Card>
    <Card title="T3AC — KI-Chatbot" icon="message-circle" href="{prefix}/ExtNsT3AC/Index">KI-Chatbot auf Basis Ihrer TYPO3-Inhalte.</Card>
    <Card title="T3AS — KI-Suche" icon="search" href="{prefix}/ExtNsT3AS/Index">Semantische Suche mit Embeddings und Custom LLM.</Card>
    <Card title="T3AL — KI-Lokalisierung" icon="languages" href="{prefix}/ExtNsT3AL/Index">Automatisierte Übersetzungen und XLIFF-Workflows.</Card>
    <Card title="T3AA — KI-Barrierefreiheit" icon="accessibility" href="{prefix}/ExtNsT3AA/Index">Alt-Text, Voiceover und A11y-Prüfungen.</Card>
    <Card title="T3AB — KI-Builder" icon="blocks" href="{prefix}/ExtNsT3AB/Index">Inhaltselemente und Formulare mit KI erstellen.</Card>
  </CardGroup>
</section>

<section className="t3-landing-section">
  <div className="t3-section-header">
    <div>
      <p className="t3-landing-eyebrow">Vorlagen</p>
      <h2 className="t3-landing-section-title">TYPO3-Themes</h2>
    </div>
    <a className="t3-view-all" href="{hub_tpl}">Alle anzeigen →</a>
  </div>
  <CardGroup cols={{3}}>
    <Card title="T3 Karma" icon="palette" href="{prefix}/EXTKarma/Index">Premium-Business-Theme mit Inhaltsblöcken.</Card>
    <Card title="T3 Bootstrap" icon="grid-3x3" href="{prefix}/EXTBootstrap/Index">Bootstrap-basiertes TYPO3-Theme.</Card>
    <Card title="T3 Shop" icon="shopping-bag" href="{prefix}/EXTShop/Index">E-Commerce-Theme mit Shop-Konfiguration.</Card>
    <Card title="T3 Ayu" icon="zap" href="{prefix}/EXTAyu/Index">React.js-Theme mit Vorschaufunktion.</Card>
    <Card title="T3 Reva" icon="sparkle" href="{prefix}/EXTReva/Index">Elegantes React.js-Theme.</Card>
    <Card title="T3 Shiva" icon="mountain" href="{prefix}/EXTShiva/Index">Funktionsreiches React.js-Theme.</Card>
  </CardGroup>
</section>

<section className="t3-landing-section">
  <div className="t3-section-header">
    <div>
      <p className="t3-landing-eyebrow">Erweiterungen</p>
      <h2 className="t3-landing-section-title">Beliebte TYPO3-Erweiterungen</h2>
    </div>
    <a className="t3-view-all" href="{hub_ext}">Alle anzeigen →</a>
  </div>
  <CardGroup cols={{3}}>
    <Card title="{format_slug_display_name("ExtNsRevolutionSlider")}" icon="images" href="{prefix}/ExtNsRevolutionSlider/Index">Premium-Slider für TYPO3.</Card>
    <Card title="{format_slug_display_name("ExtNsFAQ")}" icon="circle-question-mark" href="{prefix}/ExtNsFAQ/Index">FAQ-Verwaltung und Frontend-Anzeige.</Card>
    <Card title="{format_slug_display_name("ExtNsGallery")}" icon="image" href="{prefix}/ExtNsGallery/Index">Bildergalerien und Medienverwaltung.</Card>
    <Card title="{format_slug_display_name("ExtNsHelpDesk")}" icon="life-buoy" href="{prefix}/ExtNsHelpDesk/Index">Helpdesk- und Ticket-System.</Card>
    <Card title="{format_slug_display_name("ExtNsSocialLogin")}" icon="log-in" href="{prefix}/ExtNsSocialLogin/Index">Social-Login für TYPO3.</Card>
    <Card title="{format_slug_display_name("ExtRTECKEditorPack")}" icon="file-text" href="{prefix}/ExtRTECKEditorPack/Index">Premium CKEditor-Paket.</Card>
  </CardGroup>
</section>

{render_recent_section(lang)}

<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">Schnelllinks</p>
  <h2 className="t3-landing-section-title">Häufig benötigte Anleitungen</h2>
  <div className="t3-quick-links">
    <a className="t3-quick-link" href="{prefix}/License/Introduction/Index">Installation</a>
    <a className="t3-quick-link" href="{prefix}/License/UpdateVersion/Index">Version aktualisieren</a>
    <a className="t3-quick-link" href="{prefix}/License/LicenseActivation/Index">Lizenz aktivieren</a>
    <a className="t3-quick-link" href="{prefix}/License/HelpSupport/Index">Hilfe &amp; Support</a>
    <a className="t3-quick-link" href="{prefix}/ExtNsT3AI/Installation/Index">T3AI installieren</a>
    <a className="t3-quick-link" href="{prefix}/EXTKarma/Installation/Index">T3 Karma installieren</a>
  </div>
</section>

<div className="t3-cta-banner">
  <div>
    <h3 className="t3-cta-title">Brauchen Sie Hilfe?</h3>
    <p className="t3-cta-subtitle">Unser Support-Team hilft bei Installation, Lizenzierung und Konfiguration.</p>
  </div>
  <div className="t3-cta-actions">
    <a className="t3-cta-btn t3-cta-btn-primary" href="https://t3planet.de/en/support">Support kontaktieren</a>
    <a className="t3-cta-btn t3-cta-btn-secondary" href="https://t3planet.de/en/typo3-extensions">Erweiterungen durchsuchen</a>
  </div>
</div>

<Tip>
Über den Sprachumschalter in der oberen Navigation wechseln Sie zwischen Deutsch und Englisch. Der aktuelle Seitenpfad bleibt beim Wechsel erhalten.
</Tip>

</div>
"""
    return f"""---
title: "Welcome to T3Planet Docs"
description: "Official T3Planet documentation for TYPO3 extensions, templates, AI solutions, licensing, installation, and configuration guides."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TYPO3 extensions"
  - "TYPO3 templates"
  - "documentation"
sidebarTitle: "Home"
---

<div className="t3-home-landing">

{hub_nav(lang, "home")}
{render_hero_panel(lang, "T3Planet Documentation", "Welcome to T3Planet Docs", "Build faster with TYPO3 extensions, templates and AI — official guides for installation, license, configuration, and updates.")}
{render_stats_bar(lang)}

<CardGroup cols={{4}}>
  <Card title="Get started" icon="rocket" href="{license}">
    License, installation, and update guides for all T3Planet products.
  </Card>
  <Card title="AI Universe Extensions" icon="bot" href="{hub_ai}">
    6 AI products — chatbot, search, localization, accessibility, and more.
  </Card>
  <Card title="TYPO3 Templates & Themes" icon="layout-template" href="{hub_tpl}">
    9 TYPO3 themes — business, React.js, and e-commerce.
  </Card>
  <Card title="TYPO3 Extensions" icon="puzzle" href="{hub_ext}">
    50+ TYPO3 extensions — comments, media, integrations, and more.
  </Card>
</CardGroup>

<section className="t3-landing-section">
  <div className="t3-section-header">
    <div>
      <p className="t3-landing-eyebrow">AI Universe Extensions</p>
      <h2 className="t3-landing-section-title">TYPO3 AI solutions</h2>
    </div>
    <a className="t3-view-all" href="{hub_ai}">View all →</a>
  </div>
  <CardGroup cols={{3}}>
    <Card title="T3AI — AI Content &amp; SEO" icon="sparkles" href="{prefix}/ExtNsT3AI/Index">Generate content, translations, and SEO with AI.</Card>
    <Card title="T3AC — AI Chatbot" icon="message-circle" href="{prefix}/ExtNsT3AC/Index">AI chatbot trained on your TYPO3 content.</Card>
    <Card title="T3AS — AI Search" icon="search" href="{prefix}/ExtNsT3AS/Index">Semantic search with embeddings and custom LLM.</Card>
    <Card title="T3AL — AI Localization" icon="languages" href="{prefix}/ExtNsT3AL/Index">Automated translations and XLIFF workflows.</Card>
    <Card title="T3AA — AI Accessibility" icon="accessibility" href="{prefix}/ExtNsT3AA/Index">Alt text, voiceover, and a11y checks.</Card>
    <Card title="T3AB — AI Builder" icon="blocks" href="{prefix}/ExtNsT3AB/Index">Build content elements and forms with AI.</Card>
  </CardGroup>
</section>

<section className="t3-landing-section">
  <div className="t3-section-header">
    <div>
      <p className="t3-landing-eyebrow">TYPO3 Templates & Themes</p>
      <h2 className="t3-landing-section-title">TYPO3 themes</h2>
    </div>
    <a className="t3-view-all" href="{hub_tpl}">View all →</a>
  </div>
  <CardGroup cols={{3}}>
    <Card title="T3 Karma" icon="palette" href="{prefix}/EXTKarma/Index">Premium business theme with content blocks.</Card>
    <Card title="T3 Bootstrap" icon="grid-3x3" href="{prefix}/EXTBootstrap/Index">Bootstrap-based TYPO3 theme.</Card>
    <Card title="T3 Shop" icon="shopping-bag" href="{prefix}/EXTShop/Index">E-commerce theme with shop configuration.</Card>
    <Card title="T3 Ayu" icon="zap" href="{prefix}/EXTAyu/Index">React.js theme with preview features.</Card>
    <Card title="T3 Reva" icon="sparkle" href="{prefix}/EXTReva/Index">Elegant React.js theme.</Card>
    <Card title="T3 Shiva" icon="mountain" href="{prefix}/EXTShiva/Index">Feature-rich React.js theme.</Card>
  </CardGroup>
</section>

<section className="t3-landing-section">
  <div className="t3-section-header">
    <div>
      <p className="t3-landing-eyebrow">TYPO3 Extensions</p>
      <h2 className="t3-landing-section-title">Popular TYPO3 extensions</h2>
    </div>
    <a className="t3-view-all" href="{hub_ext}">View all →</a>
  </div>
  <CardGroup cols={{3}}>
    <Card title="{format_slug_display_name("ExtNsRevolutionSlider")}" icon="images" href="{prefix}/ExtNsRevolutionSlider/Index">Premium slider for TYPO3.</Card>
    <Card title="{format_slug_display_name("ExtNsFAQ")}" icon="circle-question-mark" href="{prefix}/ExtNsFAQ/Index">FAQ management and frontend display.</Card>
    <Card title="{format_slug_display_name("ExtNsGallery")}" icon="image" href="{prefix}/ExtNsGallery/Index">Image galleries and media management.</Card>
    <Card title="{format_slug_display_name("ExtNsHelpDesk")}" icon="life-buoy" href="{prefix}/ExtNsHelpDesk/Index">Helpdesk and ticket system.</Card>
    <Card title="{format_slug_display_name("ExtNsSocialLogin")}" icon="log-in" href="{prefix}/ExtNsSocialLogin/Index">Social login for TYPO3.</Card>
    <Card title="{format_slug_display_name("ExtRTECKEditorPack")}" icon="file-text" href="{prefix}/ExtRTECKEditorPack/Index">Premium CKEditor pack.</Card>
  </CardGroup>
</section>

{render_recent_section(lang)}

<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">Quick links</p>
  <h2 className="t3-landing-section-title">Frequently needed guides</h2>
  <div className="t3-quick-links">
    <a className="t3-quick-link" href="{prefix}/License/Introduction/Index">Installation</a>
    <a className="t3-quick-link" href="{prefix}/License/UpdateVersion/Index">Update version</a>
    <a className="t3-quick-link" href="{prefix}/License/LicenseActivation/Index">License activation</a>
    <a className="t3-quick-link" href="{prefix}/License/HelpSupport/Index">Help &amp; support</a>
    <a className="t3-quick-link" href="{prefix}/ExtNsT3AI/Installation/Index">Install T3AI</a>
    <a className="t3-quick-link" href="{prefix}/EXTKarma/Installation/Index">Install T3 Karma</a>
  </div>
</section>

<div className="t3-cta-banner">
  <div>
    <h3 className="t3-cta-title">Need help?</h3>
    <p className="t3-cta-subtitle">Our support team can assist with installation, licensing, and configuration.</p>
  </div>
  <div className="t3-cta-actions">
    <a className="t3-cta-btn t3-cta-btn-primary" href="https://t3planet.de/en/support">Contact support</a>
    <a className="t3-cta-btn t3-cta-btn-secondary" href="https://t3planet.de/en/typo3-extensions">Browse extensions</a>
  </div>
</div>

<Tip>
Use the language switcher in the top navigation to switch between English and German. Your current page path is preserved when switching languages.
</Tip>

</div>
"""


SIDEBAR_SHORT = {
    "All TYPO3 Templates & Themes": "TYPO3 Templates & Themes",
    "Alle TYPO3-Vorlagen": "Vorlagen",
    "All TYPO3 Extensions": "TYPO3 Extensions",
    "Alle TYPO3-Erweiterungen": "Erweiterungen",
    "AI Universe Extensions": "AI Universe Extensions",
    "KI-Universum": "KI-Universum",
}


def write_hub(slug: str, lang: str, body: str, title_en: str, title_de: str, desc_en: str, desc_de: str) -> None:
    title = title_de if lang == "de" else title_en
    desc = desc_de if lang == "de" else desc_en
    sidebar = SIDEBAR_SHORT.get(title, title)
    keywords = ["TYPO3", "T3Planet", title]
    rel = f"de/{slug}/Index.md" if lang == "de" else f"{slug}/Index.md"
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(fm(title, desc, sidebar, keywords) + "\n" + body, encoding="utf-8")
    print(f"Wrote {rel}")


def update_docs_json() -> None:
    path = ROOT / "docs.json"
    docs = json.loads(path.read_text())
    for entry in docs["navigation"]["languages"]:
        if entry["language"] == "en":
            for d in entry["dropdowns"]:
                if d["dropdown"] == "Home":
                    d.pop("pages", None)
                    d["groups"] = [
                        {
                            "group": "Overview",
                            "pages": [
                                "index",
                                "T3AF/Index",
                                "AllTemplates/Index",
                                "AllExtensions/Index",
                            ],
                        },
                        {
                            "group": "Quick start",
                            "pages": [
                                "License/Index",
                                "License/Introduction/Index",
                                "License/UpdateVersion/Index",
                                "License/LicenseActivation/Index",
                                "License/HelpSupport/Index",
                            ],
                        },
                        {
                            "group": "Popular docs",
                            "pages": [
                                "ExtNsT3AI/Index",
                                "ExtNsT3AC/Index",
                                "EXTKarma/Index",
                                "ExtNsRevolutionSlider/Index",
                                "ExtRTECKEditorPack/Index",
                            ],
                        },
                    ]
        if entry["language"] == "de":
            for d in entry["dropdowns"]:
                if d["dropdown"] == "Startseite":
                    d.pop("pages", None)
                    d["groups"] = [
                        {
                            "group": "Überblick",
                            "pages": [
                                "de/index",
                                "de/T3AF/Index",
                                "de/AllTemplates/Index",
                                "de/AllExtensions/Index",
                            ],
                        },
                        {
                            "group": "Erste Schritte",
                            "pages": [
                                "de/License/Index",
                                "de/License/Introduction/Index",
                                "de/License/UpdateVersion/Index",
                                "de/License/LicenseActivation/Index",
                                "de/License/HelpSupport/Index",
                            ],
                        },
                        {
                            "group": "Beliebte Docs",
                            "pages": [
                                "de/ExtNsT3AI/Index",
                                "de/ExtNsT3AC/Index",
                                "de/EXTKarma/Index",
                                "de/ExtNsRevolutionSlider/Index",
                                "de/ExtRTECKEditorPack/Index",
                            ],
                        },
                    ]
    path.write_text(json.dumps(docs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Updated docs.json navigation")


def main() -> None:
    write_hub(
        "T3AF",
        "en",
        render_ai_hub("en"),
        "T3AF",
        "KI-Universum",
        "Explore all T3Planet AI products — T3AI, T3AC, T3AS, T3AL, T3AA, and T3AB for TYPO3.",
        "Entdecken Sie alle T3Planet KI-Produkte — T3AI, T3AC, T3AS, T3AL, T3AA und T3AB für TYPO3.",
    )
    write_hub(
        "T3AF",
        "de",
        render_ai_hub("de"),
        "T3AF",
        "KI-Universum",
        "Explore all T3Planet AI products — T3AI, T3AC, T3AS, T3AL, T3AA, and T3AB for TYPO3.",
        "Entdecken Sie alle T3Planet KI-Produkte — T3AI, T3AC, T3AS, T3AL, T3AA und T3AB für TYPO3.",
    )
    write_hub(
        "AllTemplates",
        "en",
        render_template_hub("en"),
        "All TYPO3 Templates",
        "Alle TYPO3-Vorlagen",
        "Browse all T3Planet TYPO3 templates — business, React.js, Bootstrap, and e-commerce themes.",
        "Durchsuchen Sie alle T3Planet TYPO3-Vorlagen — Business-, React.js-, Bootstrap- und E-Commerce-Themes.",
    )
    write_hub(
        "AllTemplates",
        "de",
        render_template_hub("de"),
        "All TYPO3 Templates",
        "Alle TYPO3-Vorlagen",
        "Browse all T3Planet TYPO3 templates — business, React.js, Bootstrap, and e-commerce themes.",
        "Durchsuchen Sie alle T3Planet TYPO3-Vorlagen — Business-, React.js-, Bootstrap- und E-Commerce-Themes.",
    )
    write_hub(
        "AllExtensions",
        "en",
        render_extensions_hub("en"),
        "All TYPO3 Extensions",
        "Alle TYPO3-Erweiterungen",
        "Complete catalog of all T3Planet TYPO3 extensions with documentation links and update guides.",
        "Vollständiger Katalog aller T3Planet TYPO3-Erweiterungen mit Dokumentationslinks und Update-Anleitungen.",
    )
    write_hub(
        "AllExtensions",
        "de",
        render_extensions_hub("de"),
        "All TYPO3 Extensions",
        "Alle TYPO3-Erweiterungen",
        "Complete catalog of all T3Planet TYPO3 extensions with documentation links and update guides.",
        "Vollständiger Katalog aller T3Planet TYPO3-Erweiterungen mit Dokumentationslinks und Update-Anleitungen.",
    )

    (ROOT / "index.md").write_text(render_home("en"), encoding="utf-8")
    (ROOT / "de" / "index.md").write_text(render_home("de"), encoding="utf-8")
    print("Wrote index.md and de/index.md")

    from build_unified_sidebar import apply as apply_unified_sidebar

    apply_unified_sidebar()
    print("Done.")


if __name__ == "__main__":
    main()
    from sync_doc_stats import sync_homepage_stats
    sync_homepage_stats()
