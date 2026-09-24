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

Short answers about **AI Foundation** (`EXT:ns_t3af`).

## General

**What is AI Foundation?**

The shared AI foundation for T3Planet TYPO3 extensions. It manages providers, MCP, brand context, prompts, access roles, and usage in one backend module. See [Overview](/en/latest/ExtNsT3AF/Introduction/Index).

**Does it include a frontend plugin?**

No. AI Foundation is a backend foundation layer. Visitors see AI through child extensions such as AI Assistant or AI Chatbot.

**Which TYPO3 and PHP versions are supported?**

TYPO3 12.4–14.x with PHP 8.2 or higher. See [System Requirements](/en/latest/ExtNsT3AF/Installation/Index).

## Installation

**How do I install it?**

With Composer (`composer require nitsan/ns-t3af`) or from the TYPO3 Extension Repository. See [Installation](/en/latest/ExtNsT3AF/Installation/Index).

**Do I need a licence key?**

No. AI Foundation is 100% free and open source (GPL-2.0-or-later). There is no licence key, no registration and no activation, on any domain, production included.

**Is a commercial license required?**

No. T3Planet Credits is optional and pays for AI usage only.

**Composer reports a conflict with another MCP package.**

Remove conflicting MCP server packages first, then install AI Foundation. See [Known Problems](/en/latest/ExtNsT3AF/Troubleshooting/KnownProblems/Index).

## Providers and MCP

**Can I use local models such as Ollama?**

Yes. Use the Ollama provider type or a custom OpenAI-compatible endpoint. See [AI Providers](/en/latest/ExtNsT3AF/Configuration/AIProviders/Index).

**What is T3Planet Credits?**

An optional mode that uses a shared T3Planet credit balance instead of your
own vendor API keys. See [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index).

**Test connection fails even with a valid key.**

Check the model ID, outbound HTTPS, and provider status. See the provider checklist in [Known Problems](/en/latest/ExtNsT3AF/Troubleshooting/KnownProblems/Index).

**What is MCP?**

Model Context Protocol connects AI clients such as Cursor to your TYPO3 instance. See [MCP Server](/en/latest/ExtNsT3AF/Integrations/MCPServer/Index).

## Privacy

**Where does request data go?**

AI Foundation is self-hosted. With **Your Own API Keys**, prompts and responses
go from your server to the AI provider you configure. T3Planet is not in that
AI data path. With [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index) active,
billable AI calls go through T3Planet and use your credit balance. AI Foundation itself has no licence check and sends nothing to T3Planet.

## Still stuck?

Open [Support](/en/latest/ExtNsT3AF/Support/Index) with your TYPO3, PHP, and `ns_t3af` versions and the exact error text.
