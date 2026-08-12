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

The Quick Setup wizard guides you through first-time configuration. **Go live in 7 steps.**

**Path:** T3AF → Quick Setup

## When to use

- First install of `ns_t3af`
- New admin taking over T3AF
- After a major upgrade when providers need re-checking

## Before you start

- TYPO3 admin login
- T3Planet license key (see [https://docs.t3planet.de/en/latest/License/Index.html](/License/Index))
- Decision: Your Own API Keys (BYOK) or T3Planet Credits
- About 15 minutes

## Wizard steps

**Step 1 — Welcome** — Overview of what T3AF does.

**Step 2 — License** — Verify your T3Planet license key.

**Step 3 — Provider** — Add your first AI provider (API key and model).

**Step 4 — Test connection** — Confirm the test is green before continuing.

**Step 5 — Credits** — Choose BYOK or T3Planet Credits.

**Step 6 — MCP** — Optionally enable the MCP server.

**Step 7 — Complete** — Summary and links to next tasks.

## Why use the wizard

The wizard prevents common mistakes: missing default provider, credits toggle without **Activate**, or MCP enabled without HTTPS. It is faster than configuring each screen manually on first setup.

## After the wizard

Use these follow-up tasks after the wizard completes:

- **Brand context** — [AI Context](/ExtNsT3AF/AIContext/Index)
- **Tune prompts** — [AI Prompts](/ExtNsT3AF/AIPrompts/Index)
- **Enable governance** — [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index)
- **Connect MCP** — [MCP Server](/ExtNsT3AF/MCPServer/Index)
- **Daily health check** — [Dashboard](/ExtNsT3AF/Dashboard/Index)

## Scenario: agency onboarding a new client

1. Install on staging → run wizard with client’s API key or credits
2. Fill [AI Context](/ExtNsT3AF/AIContext/Index) with brand voice
3. Test one connected extension (for example T3AI)
4. Enable governance before handing over to client editors
5. Repeat on production in a low-traffic window
