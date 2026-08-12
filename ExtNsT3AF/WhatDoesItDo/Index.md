---
title: "What Does It Do?"
description: "What Does It Do? for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "What Does It Do?"
---

## Purpose

T3AF is **shared infrastructure**. It does not replace your CMS — it makes AI reliable inside TYPO3.

Child extensions and MCP agents send requests to T3AF. T3AF routes them to your configured AI provider or to T3Planet Credits. The provider (OpenAI, Claude, Gemini, Mistral, and others) returns the result. Every call is logged.

```
Your extensions / MCP agents
         ↓
   T3AF (ns_t3af)
         ↓
   AI provider OR T3Planet Credits
         ↓
   OpenAI · Claude · Gemini · Mistral · …
```

## 1. AI Providers

**Path:** T3AF → AI Providers

Connect to major AI vendors from one backend screen.

- Add multiple providers (OpenAI, Anthropic, Gemini, Azure, Mistral, DeepSeek, xAI, custom, Ollama)
- Store API keys encrypted
- Pick models and run **Test connection**
- Set one default provider for the whole system

See [AI Providers](/ExtNsT3AF/AIProviders/Index) for step-by-step setup.

## 2. MCP Server

**Path:** T3AF → MCP Server

Expose TYPO3 to external AI assistants via the Model Context Protocol.

- **Remote OAuth** — production (Cursor, Claude Desktop)
- **mcp-remote** — URL token for simple clients
- **Local CLI** — DDEV and development

Core tools: read pages, list content, read/write database records (with permissions).

See [MCP Server](/ExtNsT3AF/MCPServer/Index).

## 3. AI Context

**Path:** T3AF → AI Context

Store brand identity once: company name, audience, tone, keywords. Injected into AI prompts automatically for on-brand output.

See [AI Context](/ExtNsT3AF/AIContext/Index).

## 4. AI Prompts

**Path:** T3AF → AI Prompts

Central library of prompt templates. Extensions can sync and reuse them.

See [AI Prompts](/ExtNsT3AF/AIPrompts/Index).

## 5. AI Features

**Path:** T3AF → AI Features

Assign different providers per task type (SEO, pages, content, translation).

See [AI Features](/ExtNsT3AF/AIFeatures/Index).

## 6. Usage & Logs

**Path:** T3AF → AI Usage / AI Logs / Scheduler & CLI

- **AI Usage** — charts, tokens, credits
- **AI Logs** — per-request detail for audits
- **Scheduler & CLI** — background jobs

See [AI Usage & Logs](/ExtNsT3AF/AIUsageAndLogs/Index).

## 7. AI Permissions

**Path:** T3AF → AI Permissions

Control who uses which provider, which capabilities, budgets, rate limits, and log privacy. Off by default — enable when your team grows.

See [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index).

## Supported providers

- **OpenAI** — Chat, vision, embeddings, images
- **Claude / Anthropic** — Long-form text, analysis
- **Google Gemini** — Fast multimodal tasks
- **Azure OpenAI** — Enterprise deployments
- **Mistral** — EU-friendly option
- **DeepSeek** — Cost-effective chat
- **xAI** — Grok models
- **Custom / Ollama** — Private or local models

## Public API (for developers)

Child extensions call `AiServiceInterface` only:

- `complete()` — Full AI text response
- `stream()` — Real-time text chunks
- `embed()` — Vector embeddings
- `provider()` — Active provider record

Extensions never call vendor APIs directly — T3AF handles keys, logging, credits, and governance.

Full reference: [Developer Guide](/ExtNsT3AF/DeveloperGuide/Index)

## Typical admin workflow

1. Install extension → [Installation](/ExtNsT3AF/Installation/Index)
2. Add provider and run **Test connection** → [AI Providers](/ExtNsT3AF/AIProviders/Index)
3. Run Quick Setup → [Quick Setup](/ExtNsT3AF/SetupWizard/Index)
4. (Optional) Enable MCP → [MCP Server](/ExtNsT3AF/MCPServer/Index)
5. (Optional) Set governance rules → [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index)
6. Monitor usage weekly → [AI Usage & Logs](/ExtNsT3AF/AIUsageAndLogs/Index)

## Requirements at a glance

- **TYPO3** — 12.4 LTS, 13.4 LTS, or 14.x
- **PHP** — 8.2 or higher (8.3 recommended)
- **System extensions** — `workspaces` and `scheduler`
- **Billing** — API key or T3Planet Credits (at least one)
- **Composer** — Recommended for TYPO3 installs

See [System Requirements](/ExtNsT3AF/SystemRequirements/Index) for full details.
