---
title: "Appendix"
description: "Appendix for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Appendix"
---

Terms used in **T3AF** documentation.

## A–C

- **AI Context** — Brand profile injected into prompts. See [AI Context](/ExtNsT3AF/AIContext/Index).
- **AI Provider** — Connection to an AI vendor (OpenAI, Claude, and others).
- **API key** — Secret for AI or translation APIs. Stored encrypted in T3AF.
- **BYOK** — Bring Your Own Key. You pay the vendor directly.
- **Credits** — T3Planet billing units. About 1 credit per 1,000 tokens by default.
- **CLI** — Command line interface (`vendor/bin/typo3`).

## G–M

- **GDPR** — EU data protection regulation (DSGVO in German).
- **Governance** — Access control, budgets, and rate limits for AI. See [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index).
- **JSON-LD** — Schema markup format for structured data.
- **MCP** — Model Context Protocol. Connects AI agents to TYPO3. See [MCP Server](/ExtNsT3AF/MCPServer/Index).
- **Meta description** — Short text shown in Google search results.

## O–T

- **OAuth** — Secure authentication for MCP remote connections.
- **Prompt** — Instruction sent to the AI. See [AI Prompts](/ExtNsT3AF/AIPrompts/Index).
- **Provider** — AI vendor connection configured in the backend.
- **Scheduler** — TYPO3 system extension for background jobs.
- **Stdio** — MCP transport via command line (local development).
- **Token** — Unit of AI text; also used for auth tokens in MCP.
- **TYPO3** — The content management system.

## W

- **Workspace** — Draft content version in TYPO3. `0` = live; `1+` = draft.

## Extension key

- `ns_t3af` — T3AF (this extension)

## Developer API

Child extensions integrate through `AiServiceInterface`:

- `complete()` — Full AI text response
- `stream()` — Real-time text chunks
- `embed()` — Vector embeddings
- `provider()` — Active provider record

Extensions must not call vendor APIs directly. T3AF handles keys, logging, credits, and governance.

Full API reference: [Developer Guide](/ExtNsT3AF/DeveloperGuide/Index)

## Related pages

- [What Does It Do?](/ExtNsT3AF/WhatDoesItDo/Index) — Feature overview
- [Configuration](/ExtNsT3AF/Configuration/Index) — Extension Configuration keys
- [Helpful Links](/ExtNsT3AF/HelpfulLinks/Index) — External documentation and API portals
