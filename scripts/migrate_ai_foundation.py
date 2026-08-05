#!/usr/bin/env python3
"""Migrate ai universe documentation/ to Mintlify T3AF/ pages.

Migration completed July 2026. Source folder removed; content lives in T3AF/.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "ai universe documentation"
DEST = ROOT / "T3AF"

if not SRC.is_dir():
    print("Source folder removed. T3AF content is in T3AF/ (27 pages).")
    print("No re-migration needed.")
    sys.exit(0)

PAGES = [
    ("01-Introduction.md", "Introduction/Index", "Introduction", "Introduction to EXT:ns_t3af — the shared AI foundation for TYPO3."),
    ("02-What-Does-It-Do.md", "WhatDoesItDo/Index", "What Does It Do?", "Complete overview of T3AF capabilities — providers, MCP, credits, governance, and more."),
    ("03-Helpful-Links.md", "HelpfulLinks/Index", "Helpful Links", "Official product links, API portals, and related documentation."),
    ("04-Screenshots.md", "Screenshots/Index", "Screenshots", "Backend screenshots of the T3AF module."),
    ("05-Video-Tutorials.md", "VideoTutorials/Index", "Video Tutorials", "Recommended video tutorials and training order for T3AF."),
    ("06-System-Requirements.md", "SystemRequirements/Index", "System Requirements", "TYPO3, PHP, and server requirements for T3AF."),
    ("07-Installation.md", "Installation/Index", "Installation", "Install EXT:ns_t3af via Composer on TYPO3."),
    ("08-Configuration.md", "Configuration/Index", "Configuration", "Configure providers, extension settings, MCP, and credits."),
    ("09-Update-Version.md", "UpdateVersion/Index", "Update Version", "Update T3AF and run post-update checks."),
    ("10-AI-Universe-Dashboard.md", "Dashboard/Index", "Dashboard", "T3AF dashboard — health, providers, credits, and quick actions."),
    ("11-AI-Providers.md", "AIProviders/Index", "AI Providers", "Connect OpenAI, Claude, Gemini, and other AI providers."),
    ("12-T3Planet-Credits.md", "T3PlanetCredits/Index", "T3Planet Credits", "Use T3Planet credits instead of separate vendor API keys."),
    ("13-MCP-Server.md", "MCPServer/Index", "MCP Server", "Connect Cursor, Claude Desktop, and n8n to TYPO3 via MCP."),
    ("14-AI-Context.md", "AIContext/Index", "AI Context", "Brand voice and business profile for consistent AI output."),
    ("15-AI-Prompts.md", "AIPrompts/Index", "AI Prompts", "Central prompt template library for all AI extensions."),
    ("16-AI-Features.md", "AIFeatures/Index", "AI Features", "Assign different AI providers per task type."),
    ("17-AI-Usage-and-Logs.md", "AIUsageAndLogs/Index", "AI Usage & Logs", "Usage charts, request logs, scheduler, and CLI."),
    ("18-Governance-and-Access.md", "GovernanceAndAccess/Index", "Governance & Access", "Provider access, budgets, rate limits, and privacy."),
    ("19-Setup-Wizard.md", "SetupWizard/Index", "Setup Wizard", "7-step Quick Setup wizard for T3AF."),
    ("20-Upgrade-Guide.md", "UpgradeGuide/Index", "Upgrade Guide", "Upgrade workflow, migration, and rollback."),
    ("21-FAQ.md", "FAQ/Index", "FAQ", "Frequently asked questions about T3AF."),
    ("22-Known-Problems.md", "KnownProblems/Index", "Known Problems", "Known issues and workarounds."),
    ("23-Appendix.md", "Appendix/Index", "Appendix", "Glossary and developer API reference."),
    ("24-Support.md", "Support/Index", "Support", "Get help with T3AF."),
    ("25-Get-This-Extension.md", "GetThisExtension/Index", "Get This Extension", "Purchase and install EXT:ns_t3af."),
]

LINK_MAP = {
    "01-Introduction.md": "/T3AF/Introduction/Index",
    "02-What-Does-It-Do.md": "/T3AF/WhatDoesItDo/Index",
    "03-Helpful-Links.md": "/T3AF/HelpfulLinks/Index",
    "04-Screenshots.md": "/T3AF/Screenshots/Index",
    "05-Video-Tutorials.md": "/T3AF/VideoTutorials/Index",
    "06-System-Requirements.md": "/T3AF/SystemRequirements/Index",
    "07-Installation.md": "/T3AF/Installation/Index",
    "08-Configuration.md": "/T3AF/Configuration/Index",
    "09-Update-Version.md": "/T3AF/UpdateVersion/Index",
    "10-AI-Universe-Dashboard.md": "/T3AF/Dashboard/Index",
    "11-AI-Providers.md": "/T3AF/AIProviders/Index",
    "12-T3Planet-Credits.md": "/T3AF/T3PlanetCredits/Index",
    "13-MCP-Server.md": "/T3AF/MCPServer/Index",
    "14-AI-Context.md": "/T3AF/AIContext/Index",
    "15-AI-Prompts.md": "/T3AF/AIPrompts/Index",
    "16-AI-Features.md": "/T3AF/AIFeatures/Index",
    "17-AI-Usage-and-Logs.md": "/T3AF/AIUsageAndLogs/Index",
    "18-Governance-and-Access.md": "/T3AF/GovernanceAndAccess/Index",
    "19-Setup-Wizard.md": "/T3AF/SetupWizard/Index",
    "20-Upgrade-Guide.md": "/T3AF/UpgradeGuide/Index",
    "21-FAQ.md": "/T3AF/FAQ/Index",
    "22-Known-Problems.md": "/T3AF/KnownProblems/Index",
    "23-Appendix.md": "/T3AF/Appendix/Index",
    "24-Support.md": "/T3AF/Support/Index",
    "25-Get-This-Extension.md": "/T3AF/GetThisExtension/Index",
    "Index.md": "/T3AF/Index",
}

SUPADEMO_FEATURES = {
    "Dashboard/Index": "T3AF Dashboard",
    "AIProviders/Index": "AI Providers",
    "T3PlanetCredits/Index": "T3Planet Credits",
    "MCPServer/Index": "MCP Server",
    "AIContext/Index": "AI Context",
    "AIPrompts/Index": "AI Prompts",
    "AIFeatures/Index": "AI Features",
    "AIUsageAndLogs/Index": "AI Usage & Logs",
    "GovernanceAndAccess/Index": "Governance & Access",
    "SetupWizard/Index": "Setup Wizard",
    "Installation/Index": "Installation",
    "Configuration/Index": "Configuration",
}


def frontmatter(title: str, description: str, sidebar: str) -> str:
    slug = sidebar.replace(" ", "")
    return (
        "---\n"
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        "keywords:\n"
        '  - "TYPO3"\n'
        '  - "T3Planet"\n'
        '  - "T3AF"\n'
        f'  - "{title}"\n'
        f'sidebarTitle: "{sidebar}"\n'
        "---\n\n"
    )


def rewrite_links(text: str) -> str:
    for old, new in LINK_MAP.items():
        text = text.replace(f"]({old})", f"]({new})")
        text = text.replace(f"]({old}#", f"]({new}#")
    def repl(m: re.Match[str]) -> str:
        target = LINK_MAP.get(m.group(1), m.group(1))
        return f"]({target})"

    text = re.sub(r"\]\((\d{2}-[^)]+\.md)\)", repl, text)
    text = re.sub(r"!\[([^\]]*)\]\(\./images/", r"![\1](./images/", text)
    return text


def supademo_block(feature: str) -> str:
    return (
        "\n## Interactive demo\n\n"
        "<Note>\n"
        f"TODO: Replace with T3AF Supademo embed for **{feature}**.\n"
        "</Note>\n\n"
    )


def convert_body(src_file: str, rel_path: str, body: str) -> str:
    body = rewrite_links(body)
    if body.startswith("# "):
        body = re.sub(r"^# [^\n]+\n+", "", body, count=1)
    if rel_path in SUPADEMO_FEATURES:
        body = supademo_block(SUPADEMO_FEATURES[rel_path]) + body
    return body


def migrate_pages() -> list[str]:
    nav_slugs: list[str] = []
    for src_name, rel_path, title, desc in PAGES:
        src = SRC / src_name
        if not src.exists():
            raise FileNotFoundError(src)
        body = src.read_text(encoding="utf-8")
        content = frontmatter(title, desc, title) + convert_body(src_name, rel_path, body)
        out_file = DEST / f"{rel_path}.md"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(content, encoding="utf-8")
        nav_slugs.append(rel_path)
    return nav_slugs


def write_index_landing() -> None:
    content = '''---
title: "T3AF"
description: "EXT:ns_t3af — the shared AI foundation for TYPO3. Providers, MCP, credits, prompts, and governance in one place."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "T3AF"
---

<div className="t3-template-landing">
  <div className="t3-landing-hero">
    <p className="t3-landing-eyebrow">T3AF</p>
    <h1 className="t3-landing-title">T3AF</h1>
    <p className="t3-landing-subtitle">Connect providers, manage credits, expose MCP, and govern AI usage — one engine for all T3Planet AI extensions.</p>
  </div>

<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">Get started</p>
  <h2 className="t3-landing-section-title">Installation & setup</h2>
  <CardGroup cols={2}>
  <Card title="Introduction" icon="book-open" href="/T3AF/Introduction/Index" />
  <Card title="What Does It Do?" icon="sparkles" href="/T3AF/WhatDoesItDo/Index" />
  <Card title="System Requirements" icon="server" href="/T3AF/SystemRequirements/Index" />
  <Card title="Installation" icon="download" href="/T3AF/Installation/Index" />
  <Card title="Configuration" icon="settings" href="/T3AF/Configuration/Index" />
  <Card title="Setup Wizard" icon="wand-sparkles" href="/T3AF/SetupWizard/Index" />
  </CardGroup>
</section>

<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">Modules</p>
  <h2 className="t3-landing-section-title">T3AF backend</h2>
  <CardGroup cols={2}>
  <Card title="Dashboard" icon="layout-dashboard" href="/T3AF/Dashboard/Index" />
  <Card title="AI Providers" icon="cpu" href="/T3AF/AIProviders/Index" />
  <Card title="T3Planet Credits" icon="coins" href="/T3AF/T3PlanetCredits/Index" />
  <Card title="MCP Server" icon="plug" href="/T3AF/MCPServer/Index" />
  <Card title="AI Context" icon="building-2" href="/T3AF/AIContext/Index" />
  <Card title="AI Prompts" icon="message-square" href="/T3AF/AIPrompts/Index" />
  <Card title="AI Features" icon="layers" href="/T3AF/AIFeatures/Index" />
  <Card title="Usage & Logs" icon="chart-line" href="/T3AF/AIUsageAndLogs/Index" />
  <Card title="Governance & Access" icon="shield" href="/T3AF/GovernanceAndAccess/Index" />
  </CardGroup>
</section>

<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">Connected extensions</p>
  <h2 className="t3-landing-section-title">Powered by T3AF</h2>
  <CardGroup cols={3}>
  <Card title="T3AI" icon="sparkles" href="/ExtNsT3AI/Index" />
  <Card title="T3AC" icon="message-circle" href="/ExtNsT3AC/Index" />
  <Card title="T3AS" icon="search" href="/ExtNsT3AS/Index" />
  <Card title="T3AL" icon="languages" href="/ExtNsT3AL/Index" />
  <Card title="T3AA" icon="accessibility" href="/ExtNsT3AA/Index" />
  <Card title="T3AB" icon="blocks" href="/ExtNsT3AB/Index" />
  </CardGroup>
</section>

<section className="t3-landing-section">
  <p className="t3-landing-eyebrow">Resources</p>
  <h2 className="t3-landing-section-title">Help & support</h2>
  <CardGroup cols={2}>
  <Card title="FAQ" icon="circle-question-mark" href="/T3AF/FAQ/Index" />
  <Card title="Known Problems" icon="triangle-alert" href="/T3AF/KnownProblems/Index" />
  <Card title="Upgrade Guide" icon="arrow-up" href="/T3AF/UpgradeGuide/Index" />
  <Card title="Support" icon="life-buoy" href="/T3AF/Support/Index" />
  <Card title="Get Extension" icon="shopping-cart" href="/T3AF/GetThisExtension/Index" />
  <Card title="Appendix" icon="book" href="/T3AF/Appendix/Index" />
  </CardGroup>
</section>

</div>
'''
    (DEST / "Index.md").write_text(content, encoding="utf-8")


def write_products_hub() -> None:
    """Preserve original multi-product hub as Connected Products page."""
    old = ROOT / "T3AF" / "Index.md"
    # only if we haven't overwritten yet - called after write_index_landing
    pass


def update_docs_json(nav_pages: list[str]) -> None:
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    groups = data["navigation"]["groups"]
    ai_group = next(g for g in groups if g.get("group") == "T3AF")
    foundation = {
        "group": "T3AF Foundation",
        "root": "T3AF/Index",
        "expanded": True,
        "pages": [
            "T3AF/Introduction/Index",
            "T3AF/WhatDoesItDo/Index",
            "T3AF/HelpfulLinks/Index",
            "T3AF/Screenshots/Index",
            "T3AF/VideoTutorials/Index",
            "T3AF/SystemRequirements/Index",
            "T3AF/Installation/Index",
            "T3AF/Configuration/Index",
            {
                "group": "Modules",
                "expanded": False,
                "pages": [
                    "T3AF/Dashboard/Index",
                    "T3AF/AIProviders/Index",
                    "T3AF/T3PlanetCredits/Index",
                    "T3AF/MCPServer/Index",
                    "T3AF/AIContext/Index",
                    "T3AF/AIPrompts/Index",
                    "T3AF/AIFeatures/Index",
                    "T3AF/AIUsageAndLogs/Index",
                    "T3AF/GovernanceAndAccess/Index",
                ],
            },
            "T3AF/SetupWizard/Index",
            "T3AF/UpgradeGuide/Index",
            "T3AF/FAQ/Index",
            "T3AF/KnownProblems/Index",
            "T3AF/Appendix/Index",
            "T3AF/Support/Index",
            "T3AF/GetThisExtension/Index",
            {
                "group": "Updates",
                "expanded": False,
                "pages": ["T3AF/UpdateVersion/Index"],
            },
        ],
    }
    # Insert at beginning of T3AF pages
    if not any(p.get("group") == "T3AF Foundation" for p in ai_group["pages"] if isinstance(p, dict)):
        ai_group["pages"].insert(0, foundation)
    DOCS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    nav = migrate_pages()
    write_index_landing()
    update_docs_json(nav)
    print(f"Migrated {len(PAGES)} pages to {DEST}")
    print("Updated docs.json navigation")


if __name__ == "__main__":
    main()
