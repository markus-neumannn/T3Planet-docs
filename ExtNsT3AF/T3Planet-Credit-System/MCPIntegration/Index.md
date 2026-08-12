---
title: "MCP Integration"
description: "Documentation for MCP Integration (ExtNsT3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ExtNsT3AF"
sidebarTitle: "MCP Integration"
---

## Purpose

Clarify how Credits works with MCP — they are separate settings.

**Path:** AI Foundation > MCP Server

## Credits vs MCP mode

- **Credits** (AI Providers) — how AI is billed/fulfilled
- **MCP mode** (`context` / `native`) — how MCP tools behave

**Context** mode lets the external client (for example Cursor) generate content,
while MCP tools only apply results in your TYPO3 instance. **Native** mode runs
AI generation inside your TYPO3 instance through AI Foundation providers — that
is when Credits can apply.

Turning on Native does **not** turn on Credits. Turning on Credits does
**not** change MCP mode.

## Do MCP tools use credits?

Only if they call AI Foundation AI services while Credits is **active**
(typically Native mode tools that generate or rewrite content).

Tools that only query or write records do **not** spend credits —
for example `pages_get`, `content_list`, `table_schema`, and
`write_table`.

For how to confirm Credits traffic in the log, see
[Dashboard & AI Usage](/ExtNsT3AF/T3Planet-Credit-System/AIUsage/Index#t3planet-credits-ai-usage).
