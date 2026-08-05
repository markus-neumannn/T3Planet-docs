---
title: "FAQ"
description: "FAQ for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "FAQ"
---

Common questions about **T3AF** (`ns_t3af`).

## General

**What is T3AF?**

The shared AI foundation for T3Planet TYPO3 extensions — providers, MCP, credits, logs, and governance. See [What Does It Do?](/T3AF/WhatDoesItDo/Index).

**Does it work on the frontend?**

No standalone frontend plugin. It powers backend AI features and MCP agents. Visitors see AI through child extensions such as T3AI or T3AC.

**Which TYPO3 versions are supported?**

TYPO3 12.4, 13.4, and 14.x with PHP 8.2 or higher. See [System Requirements](/T3AF/SystemRequirements/Index).

## Providers

**Which provider should I use?**

OpenAI GPT-4o and Claude Sonnet are popular for quality. Gemini Flash is fast and cost-effective for bulk tasks. See [AI Providers](/T3AF/AIProviders/Index).

**Can I use Ollama locally?**

Yes — via Custom endpoint or Ollama provider type. Useful for development without cloud API costs.

**Test connection fails but key is correct.**

Check model ID spelling, outbound HTTPS, and vendor service status. See [Known Problems](/T3AF/KnownProblems/Index).

## Credits

**Toggle is ON but AI fails.**

Click **Activate** after enabling credits. The toggle alone is not enough. See [T3Planet Credits](/T3AF/T3PlanetCredits/Index).

**Own keys vs credits?**

**Own keys** — you pay the vendor directly (OpenAI, Anthropic, and so on).

**Credits** — you pay T3Planet; one pool for the whole install.

**Zero balance error.**

Purchase credits through T3Planet. Check balance on the [Dashboard](/T3AF/Dashboard/Index).

## MCP

**What is MCP?**

Model Context Protocol — a standard for AI tools (Cursor, Claude Desktop) to connect to TYPO3. See [MCP Server](/T3AF/MCPServer/Index).

**Is MCP safe?**

Yes with HTTPS and OAuth. Limit which backend users can authorize agents. Test writes in draft workspaces first.

**Cursor won’t connect.**

Check MCP is enabled, site uses HTTPS, and OAuth metadata URLs return HTTP 200. See health check in [MCP Server](/T3AF/MCPServer/Index).

## Privacy

**Is data sent to US providers?**

Yes with OpenAI and Claude unless you use EU options (Azure EU, Mistral). Check your DPA with the vendor.

**Are prompts logged?**

Depends on [AI Permissions](/T3AF/GovernanceAndAccess/Index) privacy level. Use **Minimal** or **Standard** for GDPR-friendly defaults.

## Installation

**How do I install the premium version?**

Follow [https://docs.t3planet.de/en/latest/License/Index.html](/License/Index) then [Installation](/T3AF/Installation/Index).

**Composer conflict with another MCP package.**

Remove conflicting MCP server packages before installing T3AF through your T3Planet Premium Composer repository. See [Known Problems](/T3AF/KnownProblems/Index).

## Still stuck?

Open [Support](/T3AF/Support) with TYPO3 version, PHP version, `ns_t3af` version, error text, and billing mode (BYOK vs credits).
