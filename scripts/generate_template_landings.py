#!/usr/bin/env python3
"""Generate Claude Platform docs-style landing pages for TYPO3 template Index.md files."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SECTIONS_EN = {
    "get_started": ("Get started", "Installation & setup"),
    "configure": ("Configure", "Theme & content"),
    "optimize": ("Optimize", "Performance & customization"),
    "resources": ("Resources", "Help & support"),
}

SECTIONS_DE = {
    "get_started": ("Erste Schritte", "Installation & Einrichtung"),
    "configure": ("Konfigurieren", "Theme & Inhalte"),
    "optimize": ("Optimieren", "Leistung & Anpassung"),
    "resources": ("Ressourcen", "Hilfe & Support"),
}

CARD_META = {
    "introduction": ("book-open", "Overview, features, and system requirements.", "Überblick, Funktionen und Systemanforderungen."),
    "installation": ("download", "Install the theme extension in your TYPO3 instance.", "Installieren Sie die Theme-Erweiterung in Ihrer TYPO3-Instanz."),
    "installation_notes": ("circle-alert", "Important prerequisites before you begin installation.", "Wichtige Voraussetzungen vor der Installation."),
    "installation_react": ("code", "Set up the React.js frontend build for this theme.", "Richten Sie den React.js-Frontend-Build für dieses Theme ein."),
    "update": ("refresh-cw", "Upgrade to the latest theme version safely.", "Aktualisieren Sie sicher auf die neueste Theme-Version."),
    "theme_options": ("settings", "Configure global theme settings and constants.", "Konfigurieren Sie globale Theme-Einstellungen und Konstanten."),
    "templates_layouts": ("layout-template", "Assign frontend and backend page layouts.", "Weisen Sie Frontend- und Backend-Seitenlayouts zu."),
    "content_blocks": ("blocks", "Use and customize pre-built content block elements.", "Nutzen und passen Sie vorgefertigte Inhaltsblöcke an."),
    "custom_elements": ("blocks", "Create and manage custom content elements.", "Erstellen und verwalten Sie benutzerdefinierte Inhaltselemente."),
    "mask_elements": ("blocks", "Configure Mask-based content elements.", "Konfigurieren Sie Mask-basierte Inhaltselemente."),
    "editor_guide": ("pencil", "Guide for editors working with theme content.", "Leitfaden für Redakteure, die mit Theme-Inhalten arbeiten."),
    "localization": ("languages", "Translate and localize your theme content.", "Übersetzen und lokalisieren Sie Ihre Theme-Inhalte."),
    "speed": ("gauge", "Optimize loading speed and Core Web Vitals.", "Optimieren Sie Ladegeschwindigkeit und Core Web Vitals."),
    "seo": ("search", "Configure SEO settings for better search visibility.", "Konfigurieren Sie SEO-Einstellungen für bessere Sichtbarkeit."),
    "customization": ("palette", "Extend and customize templates without losing upgrades.", "Erweitern und passen Sie Vorlagen an, ohne Updates zu verlieren."),
    "captcha": ("shield-check", "Set up captcha protection for forms.", "Richten Sie Captcha-Schutz für Formulare ein."),
    "upgrade_container": ("arrow-up", "Migrate container-based layouts to content blocks.", "Migrieren Sie Container-Layouts zu Inhaltsblöcken."),
    "upgrade_typo3": ("arrow-up", "Prepare your site for the next TYPO3 major version.", "Bereiten Sie Ihre Website auf die nächste TYPO3-Hauptversion vor."),
    "upgrade_guide": ("arrow-up", "Step-by-step guide for upgrading your theme.", "Schritt-für-Schritt-Anleitung zum Theme-Upgrade."),
    "frontend_build": ("hammer", "Compile assets with the theme frontend build pipeline.", "Kompilieren Sie Assets mit der Theme-Frontend-Build-Pipeline."),
    "preview": ("eye", "Preview content changes before publishing.", "Vorschau von Inhaltsänderungen vor der Veröffentlichung."),
    "demo": ("monitor", "Explore the live demo site and backend.", "Erkunden Sie die Live-Demo-Website und das Backend."),
    "shop_config": ("shopping-cart", "Configure shop pages, products, and checkout.", "Konfigurieren Sie Shop-Seiten, Produkte und Checkout."),
    "helpful_links": ("link", "Quick links to demos, product pages, and tools.", "Schnelllinks zu Demos, Produktseiten und Tools."),
    "help_support": ("life-buoy", "Get help from the T3Planet support team.", "Hilfe vom T3Planet-Support-Team erhalten."),
    "faq": ("circle-question-mark", "Answers to frequently asked questions.", "Antworten auf häufig gestellte Fragen."),
}

TEMPLATES = [
    {
        "slug": "ExtThemes",
        "en": {
            "path_prefix": "/ExtThemes",
            "eyebrow": "TYPO3 Templates",
            "hero_title": "Start building with TYPO3 Templates",
            "hero_subtitle": "Everything you need to install, configure, and customize T3Planet TYPO3 templates. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Templates & Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Custom Elements", "custom_elements", "CustomElements/Index"),
                    ("Localization", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Speed and Performance", "speed", "SpeedPerformance/Index"),
                    ("SEO (Search Engine Optimization)", "seo", "SEO/Index"),
                    ("Customization", "customization", "Customization/Index"),
                    ("Frontend Build", "frontend_build", "FrontendBuild/Index"),
                    ("Upgrade Guide TYPO3 v10 to v12", "upgrade_guide", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("Demo Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/ExtThemes",
            "eyebrow": "TYPO3-Vorlagen",
            "hero_title": "Starten Sie mit TYPO3-Vorlagen",
            "hero_subtitle": "Alles, was Sie brauchen, um T3Planet TYPO3-Vorlagen zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Vorlagen und Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Benutzerdefinierte Elemente", "custom_elements", "CustomElements/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Geschwindigkeit und Leistung", "speed", "SpeedPerformance/Index"),
                    ("SEO (Suchmaschinenoptimierung)", "seo", "SEO/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                    ("Frontend-Build", "frontend_build", "FrontendBuild/Index"),
                    ("Upgrade-Anleitung TYPO3 v10 auf v12", "upgrade_guide", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("Demo-Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTKarma",
        "en": {
            "path_prefix": "/EXTKarma",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Karma",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Karma in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Templates & Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Content Block Elements", "content_blocks", "ContentBlockElements/Index"),
                    ("Editor Guide", "editor_guide", "EditorGuide/Index"),
                    ("Localization", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Speed and Performance", "speed", "SpeedPerformance/Index"),
                    ("SEO (Search Engine Optimization)", "seo", "SEO/Index"),
                    ("Customization", "customization", "Customization/Index"),
                    ("Captcha Configuration", "captcha", "CaptchaConfiguration/Index"),
                    ("Upgrade Guide For Container", "upgrade_container", "UpgradeGuideForContainer/Index"),
                    ("Pre-Upgrade Guide — TYPO3 v13.x to v14.x", "upgrade_typo3", "UpgradeV13xToV14x/Index"),
                ],
                "resources": [
                    ("Helpful Links", "helpful_links", "HelpfulLinks/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTKarma",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Karma",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Karma in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Vorlagen und Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Inhaltsblockelemente", "content_blocks", "ContentBlockElements/Index"),
                    ("Herausgeberhandbuch", "editor_guide", "EditorGuide/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Geschwindigkeit und Leistung", "speed", "SpeedPerformance/Index"),
                    ("SEO (Suchmaschinenoptimierung)", "seo", "SEO/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                    ("Captcha-Konfiguration", "captcha", "CaptchaConfiguration/Index"),
                    ("Upgrade-Anleitung für Container", "upgrade_container", "UpgradeGuideForContainer/Index"),
                    ("Leitfaden vor dem Upgrade – TYPO3 v13.x auf v14.x", "upgrade_typo3", "UpgradeV13xToV14x/Index"),
                ],
                "resources": [
                    ("Hilfreiche Links", "helpful_links", "HelpfulLinks/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTBootstrap",
        "en": {
            "path_prefix": "/EXTBootstrap",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Bootstrap",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Bootstrap in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Templates & Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Custom Elements", "custom_elements", "CustomElements/Index"),
                    ("Localization", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Speed and Performance", "speed", "SpeedPerformance/Index"),
                    ("SEO (Search Engine Optimization)", "seo", "SEO/Index"),
                    ("Customization", "customization", "Customization/Index"),
                    ("Upgrade Guide", "upgrade_guide", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("Helpful Links", "helpful_links", "HelpfulLinks/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTBootstrap",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Bootstrap",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Bootstrap in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Vorlagen und Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Benutzerdefinierte Elemente", "custom_elements", "CustomElements/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Geschwindigkeit und Leistung", "speed", "SpeedPerformance/Index"),
                    ("SEO (Suchmaschinenoptimierung)", "seo", "SEO/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                    ("Upgrade-Anleitung", "upgrade_guide", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("Hilfreiche Links", "helpful_links", "HelpfulLinks/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTAvatar",
        "en": {
            "path_prefix": "/EXTAvatar",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Avatar",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Avatar in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Templates & Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Mask Elements", "mask_elements", "MaskElements/Index"),
                    ("Editor Guide", "editor_guide", "EditorGuide/Index"),
                    ("Localization", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Speed and Performance", "speed", "SpeedPerformance/Index"),
                    ("SEO (Search Engine Optimization)", "seo", "SEO/Index"),
                    ("Customization", "customization", "Customization/Index"),
                    ("Upgrade Guide", "upgrade_guide", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("Helpful Links", "helpful_links", "HelpfulLinks/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTAvatar",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Avatar",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Avatar in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Vorlagen und Layouts", "templates_layouts", "TemplatesLayouts/Index"),
                    ("Maskenelemente", "mask_elements", "MaskElements/Index"),
                    ("Herausgeberhandbuch", "editor_guide", "EditorGuide/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                ],
                "optimize": [
                    ("Geschwindigkeit und Leistung", "speed", "SpeedPerformance/Index"),
                    ("SEO (Suchmaschinenoptimierung)", "seo", "SEO/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                    ("Upgrade-Anleitung", "upgrade_guide", "UpgradeGuide/Index"),
                ],
                "resources": [
                    ("Hilfreiche Links", "helpful_links", "HelpfulLinks/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTAyu",
        "en": {
            "path_prefix": "/EXTAyu",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Ayu",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Ayu in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Important notes before Installation", "installation_notes", "InstallationT3AyuTheme/Index"),
                    ("React.js Setup", "installation_react", "InstallationT3AyuReactjs/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Mask Elements", "mask_elements", "CustomElements/Index"),
                    ("Localization", "localization", "Localization/Index"),
                    ("Customization", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Preview Feature", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("Demo Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTAyu",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Ayu",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Ayu in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Wichtige Hinweise vor der Installation", "installation_notes", "InstallationT3AyuTheme/Index"),
                    ("React.js-Einrichtung", "installation_react", "InstallationT3AyuReactjs/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Maskenelemente", "mask_elements", "CustomElements/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Vorschaufunktion", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("Demo-Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTReva",
        "en": {
            "path_prefix": "/EXTReva",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Reva",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Reva in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Important notes before Installation", "installation_notes", "InstallationT3RevaTheme/Index"),
                    ("React.js Setup", "installation_react", "InstallationT3RevaReactjs/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Mask Elements", "mask_elements", "CustomElements/Index"),
                    ("Localization", "localization", "Localization/Index"),
                    ("Customization", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Preview Feature", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("Demo Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTReva",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Reva",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Reva in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Wichtige Hinweise vor der Installation", "installation_notes", "InstallationT3RevaTheme/Index"),
                    ("React.js-Einrichtung", "installation_react", "InstallationT3RevaReactjs/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Maskenelemente", "mask_elements", "CustomElements/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Vorschaufunktion", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("Demo-Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTShiva",
        "en": {
            "path_prefix": "/EXTShiva",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Shiva",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Shiva in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Important notes before Installation", "installation_notes", "InstallationT3ShivaTheme/Index"),
                    ("React.js Setup", "installation_react", "InstallationT3ShivaReactjs/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Custom Elements", "custom_elements", "CustomElements/Index"),
                    ("Localization", "localization", "Localization/Index"),
                    ("Customization", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Preview Feature", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("Demo Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTShiva",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Shiva",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Shiva in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Wichtige Hinweise vor der Installation", "installation_notes", "InstallationT3ShivaTheme/Index"),
                    ("React.js-Einrichtung", "installation_react", "InstallationT3ShivaReactjs/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Benutzerdefinierte Elemente", "custom_elements", "CustomElements/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Vorschaufunktion", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("Demo-Site", "demo", "DemoSite/Index"),
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTReactBootstrap",
        "en": {
            "path_prefix": "/EXTReactBootstrap",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 ReactBootstrap",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 ReactBootstrap in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Important notes before Installation", "installation_notes", "InstallationT3ReactBootstrapTheme/Index"),
                    ("React.js Setup", "installation_react", "InstallationT3ReactBootstrapjs/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Custom Elements", "custom_elements", "CustomElements/Index"),
                    ("Localization", "localization", "Localization/Index"),
                    ("Customization", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Preview Feature", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTReactBootstrap",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 ReactBootstrap",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 ReactBootstrap in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Wichtige Hinweise vor der Installation", "installation_notes", "InstallationT3ReactBootstrapTheme/Index"),
                    ("React.js-Einrichtung", "installation_react", "InstallationT3ReactBootstrapjs/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "GlobalSettingsConfiguration/Index"),
                    ("Benutzerdefinierte Elemente", "custom_elements", "CustomElements/Index"),
                    ("Lokalisierung", "localization", "Localization/Index"),
                    ("Anpassung", "customization", "Customization/Index"),
                ],
                "optimize": [
                    ("Vorschaufunktion", "preview", "PreviewFeature/Index"),
                ],
                "resources": [
                    ("FAQ", "faq", "FAQ/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
    {
        "slug": "EXTShop",
        "en": {
            "path_prefix": "/EXTShop",
            "eyebrow": "TYPO3 Template",
            "hero_title": "Start building with T3 Shop",
            "hero_subtitle": "Everything you need to install, configure, and customize T3 Shop in TYPO3. From first setup to production.",
            "cards": {
                "get_started": [
                    ("Introduction", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Update Version", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Theme Options", "theme_options", "ThemeConfiguration/Index"),
                    ("Shop Configuration", "shop_config", "ShopConfiguration/Index"),
                ],
                "optimize": [],
                "resources": [
                    ("Demo Site", "demo", "DemoSite/Index"),
                    ("Help & Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
        "de": {
            "path_prefix": "/de/EXTShop",
            "eyebrow": "TYPO3-Vorlage",
            "hero_title": "Starten Sie mit T3 Shop",
            "hero_subtitle": "Alles, was Sie brauchen, um T3 Shop in TYPO3 zu installieren, zu konfigurieren und anzupassen.",
            "cards": {
                "get_started": [
                    ("Einführung", "introduction", "Introduction/Index"),
                    ("Installation", "installation", "Installation/Index"),
                    ("Version aktualisieren", "update", "UpdateVersion/Index"),
                ],
                "configure": [
                    ("Themenoptionen", "theme_options", "ThemeConfiguration/Index"),
                    ("Shop-Konfiguration", "shop_config", "ShopConfiguration/Index"),
                ],
                "optimize": [],
                "resources": [
                    ("Demo-Site", "demo", "DemoSite/Index"),
                    ("Hilfe und Support", "help_support", "HelpSupport/Index"),
                ],
            },
        },
    },
]


def read_frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n.*?\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"No frontmatter in {path}")
    fm = match.group(0)
    fm = re.sub(r'(")\s*mode:\s*wide', r'\1\nmode: wide', fm)
    if "mode:" not in fm:
        fm = fm.rstrip("---\n").rstrip() + "\nmode: wide\n---\n"
    return fm


def card_description(meta_key: str, lang: str) -> str:
    icon, en_desc, de_desc = CARD_META[meta_key]
    return de_desc if lang == "de" else en_desc


def render_card(title: str, meta_key: str, href: str, lang: str) -> str:
    icon = CARD_META[meta_key][0]
    desc = card_description(meta_key, lang)
    return (
        f'  <Card title="{title}" icon="{icon}" href="{href}">\n'
        f"    {desc}\n"
        f"  </Card>"
    )


def render_section(section_key: str, cards: list, path_prefix: str, lang: str) -> str:
    if not cards:
        return ""
    sections = SECTIONS_DE if lang == "de" else SECTIONS_EN
    eyebrow, section_title = sections[section_key]
    lines = [
        f'<section className="t3-landing-section">',
        f'  <p className="t3-landing-eyebrow">{eyebrow}</p>',
        f'  <h2 className="t3-landing-section-title">{section_title}</h2>',
        "  <CardGroup cols={2}>",
    ]
    for title, meta_key, page_path in cards:
        href = f"{path_prefix}/{page_path}"
        lines.append(render_card(title, meta_key, href, lang))
    lines.extend(["  </CardGroup>", "</section>"])
    return "\n".join(lines)


def render_body(locale: dict, lang: str) -> str:
    parts = [
        '<div className="t3-template-landing">',
        '  <div className="t3-landing-hero">',
        f'    <p className="t3-landing-eyebrow">{locale["eyebrow"]}</p>',
        f'    <h1 className="t3-landing-title">{locale["hero_title"]}</h1>',
        f'    <p className="t3-landing-subtitle">{locale["hero_subtitle"]}</p>',
        "  </div>",
        "",
    ]
    for section_key in ("get_started", "configure", "optimize", "resources"):
        section = render_section(
            section_key,
            locale["cards"].get(section_key, []),
            locale["path_prefix"],
            lang,
        )
        if section:
            parts.append(section)
            parts.append("")
    parts.append("</div>")
    return "\n".join(parts).rstrip() + "\n"


def output_path(slug: str, lang: str) -> Path:
    if lang == "de":
        return ROOT / "de" / slug / "Index.md"
    return ROOT / slug / "Index.md"


def main() -> None:
    updated = 0
    for template in TEMPLATES:
        slug = template["slug"]
        for lang in ("en", "de"):
            path = output_path(slug, lang)
            if not path.exists():
                print(f"SKIP missing: {path}")
                continue
            frontmatter = read_frontmatter(path)
            body = render_body(template[lang], lang)
            path.write_text(frontmatter + "\n" + body, encoding="utf-8")
            updated += 1
            print(f"Updated {path.relative_to(ROOT)}")
    print(f"\nDone. Updated {updated} template landing pages.")


if __name__ == "__main__":
    main()
    from sync_doc_stats import sync_homepage_stats
    sync_homepage_stats()
