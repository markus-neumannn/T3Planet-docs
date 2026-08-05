#!/usr/bin/env python3
"""Post-process T3AF pages: related links, supademo on feature pages, polish."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "T3AF"

SUPADEMO_PAGES = {
    "WhatDoesItDo/Index.md": "T3AF Overview",
    "Installation/Index.md": "Installation",
    "Configuration/Index.md": "Configuration",
    "Dashboard/Index.md": "T3AF Dashboard",
    "AIProviders/Index.md": "AI Providers",
    "T3PlanetCredits/Index.md": "T3Planet Credits",
    "MCPServer/Index.md": "MCP Server",
    "MCPTools/Index.md": "MCP Tools",
    "AIContext/Index.md": "AI Context",
    "AIPrompts/Index.md": "AI Prompts",
    "AIFeatures/Index.md": "AI Features",
    "AIUsageAndLogs/Index.md": "AI Usage & Logs",
    "GovernanceAndAccess/Index.md": "Governance & Access",
    "SetupWizard/Index.md": "Setup Wizard",
    "Screenshots/Index.md": "Backend Screenshots",
}

RELATED = {
    "Introduction/Index.md": ["/T3AF/WhatDoesItDo/Index", "/T3AF/Installation/Index", "/T3AF/SetupWizard/Index"],
    "Installation/Index.md": ["/T3AF/Configuration/Index", "/T3AF/SetupWizard/Index", "/T3AF/SystemRequirements/Index"],
    "Configuration/Index.md": ["/T3AF/AIProviders/Index", "/T3AF/MCPServer/Index", "/T3AF/AIFeatures/Index"],
    "MCPServer/Index.md": ["/T3AF/MCPTools/Index", "/T3AF/GovernanceAndAccess/Index", "/T3AF/AIUsageAndLogs/Index"],
    "FAQ/Index.md": ["/T3AF/KnownProblems/Index", "/T3AF/Support/Index", "/T3AF/UpgradeGuide/Index"],
}


def supademo_block(feature: str) -> str:
    return (
        "\n## Interactive demo\n\n"
        "<Note>\n"
        f"TODO: Replace with T3AF Supademo embed for **{feature}**.\n"
        "</Note>\n\n"
    )


def related_block(links: list[str]) -> str:
    lines = ["\n---\n\n## Related pages\n\n"]
    for href in links:
        label = href.split("/")[-2] if href.endswith("/Index") else href.split("/")[-1]
        lines.append(f"- [{label}]({href})")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    for md in sorted(DEST.rglob("*.md")):
        rel = md.relative_to(DEST).as_posix()
        text = md.read_text(encoding="utf-8")
        changed = False

        if rel in SUPADEMO_PAGES and "Interactive demo" not in text:
            # insert after frontmatter
            if text.startswith("---\n"):
                end = text.find("\n---\n", 4)
                if end != -1:
                    text = text[: end + 5] + supademo_block(SUPADEMO_PAGES[rel]) + text[end + 5 :]
                    changed = True

        if rel in RELATED and "## Related pages" not in text:
            text = text.rstrip() + related_block(RELATED[rel])
            changed = True

        # Normalize legacy arrow-only next steps at end
        if changed:
            md.write_text(text, encoding="utf-8")
            print("enhanced", rel)

    print("done")


if __name__ == "__main__":
    main()
