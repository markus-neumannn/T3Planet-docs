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

Short answers about **T3AF** (`EXT:ns_t3af`).

## General

**What is T3AF?**

The shared AI foundation for T3Planet TYPO3 extensions. It manages providers, MCP, brand context, prompts, access roles, and usage in one backend module. See [Overview](/ExtNsT3AF/Introduction/Index).

**Does it include a frontend plugin?**

No. T3AF is a backend foundation layer. Visitors see AI through child extensions such as AI Assistant or AI Chatbot.

**Which TYPO3 and PHP versions are supported?**

TYPO3 12.4–14.x with PHP 8.2 or higher. See [System Requirements](/ExtNsT3AF/Installation/Index).

## Installation

**How do I install it?**

With Composer (`composer require nitsan/ns-t3af`) or from the TYPO3 Extension Repository. See [Installation](/ExtNsT3AF/Installation/Index).

**Composer reports a conflict with another MCP package.**

Remove conflicting MCP server packages first, then install T3AF. See [Known Problems](/ExtNsT3AF/Troubleshooting/KnownProblems/Index).

## Providers and MCP

**Can I use local models such as Ollama?**

Yes. Use the Ollama provider type or a custom OpenAI-compatible endpoint. See [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index).

**Test connection fails even with a valid key.**

Check the model ID, outbound HTTPS, and provider status. See the provider checklist in [Known Problems](/ExtNsT3AF/Troubleshooting/KnownProblems/Index).

**What is MCP?**

Model Context Protocol connects AI clients such as Cursor to your TYPO3 instance. See [MCP Server](/ExtNsT3AF/Integrations/MCPServer/Index).

## Privacy

**Where does request data go?**

T3AF is self-hosted. Prompts and responses go from your server to the AI provider you configure, using your API keys. T3Planet is not in the AI data path. License validation only sends the license key and domain.

## Still stuck?

Open [Support](/ExtNsT3AF/Support/Index) with your TYPO3, PHP, and `ns_t3af` versions and the exact error text.
