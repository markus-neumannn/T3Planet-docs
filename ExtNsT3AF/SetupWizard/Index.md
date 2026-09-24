---
title: "Quick Setup"
description: "Quick Setup for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Quick Setup"
---

## Purpose

The Quick Setup wizard guides you through first-time configuration in 8 steps. Every step can be skipped and configured later from the matching module tab.

**Path:** T3AF → Quick Setup

## When to use

- First install of `ns_t3af`
- New admin taking over T3AF
- After a major upgrade when providers need re-checking

## Before you start

- TYPO3 admin login
- Decision: Your Own API Keys (BYOK, the default) or AI Credits
- No licence key: AI Foundation is free and open source
- A few minutes

## Wizard steps

**Step 1 — Welcome** — Overview of what will be configured.

**Step 2 — Mode** — Choose **Your Own API Keys** or **AI Credits**.

**Step 3 — Provider** — Pick the AI provider that powers your extensions.

**Step 4 — API Key** — Enter the key for that provider.

**Step 5 — Extensions** — Enable the AI extensions you use.

**Step 6 — Context** — Set a brand context profile.

**Step 7 — MCP** — Optionally enable the MCP server.

**Step 8 — Done** — Summary and links to next tasks.

## Why use the wizard

The wizard prevents common mistakes: missing default provider, credits toggle without **Activate**, or MCP enabled without HTTPS. It is faster than configuring each screen manually on first setup.

## After the wizard

Use these follow-up tasks after the wizard completes:

- **Brand context** — [AI Context](/en/latest/ExtNsT3AF/AIContext/Index)
- **Tune prompts** — [AI Prompts](/en/latest/ExtNsT3AF/AIPrompts/Index)
- **Enable governance** — [AI Permissions](/en/latest/ExtNsT3AF/Configuration/AIPermissions/Index)
- **Connect MCP** — [MCP Server](/en/latest/ExtNsT3AF/MCPServer/Index)
- **Daily health check** — [Dashboard](/en/latest/ExtNsT3AF/Dashboard/Index)

## Scenario: agency onboarding a new client

1. Install on staging → run wizard with client’s API key or credits
2. Fill [AI Context](/en/latest/ExtNsT3AF/AIContext/Index) with brand voice
3. Test one connected extension (for example T3AI)
4. Enable governance before handing over to client editors
5. Repeat on production in a low-traffic window
