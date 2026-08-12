---
title: "Dashboard"
description: "Dashboard for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Dashboard"
---

## Purpose

The Dashboard is your **control center** for AI health on this TYPO3 instance. Open it daily for a quick status check.

**Path:** T3AF → Dashboard

## What the dashboard shows

- **Provider status** — Connected, failed, or not tested
- **Default provider** — Active model name
- **T3Planet Credits** — Balance and plan (if credits mode is enabled)
- **Recent usage** — Last requests and token count
- **Quick actions** — Links to AI Providers, MCP Server, and Quick Setup

## Daily admin routine (2 minutes)

1. Open Dashboard
2. Confirm provider status is **green**
3. Check credit balance if you use T3Planet Credits
4. Skim **AI Logs** if usage looks unusual — see [AI Usage & Logs](/ExtNsT3AF/AIUsageAndLogs/Index)

## Status meanings

- **Green** — Provider OK. No action needed.
- **Yellow** — Not tested recently. Run a Test connection in [AI Providers](/ExtNsT3AF/AIProviders/Index).
- **Red** — Connection failed. Check API key, model ID, and outbound HTTPS.

## Quick links from the dashboard

- **AI Providers** → [AI Providers](/ExtNsT3AF/AIProviders/Index)
- **MCP Server** → [MCP Server](/ExtNsT3AF/MCPServer/Index)
- **Quick Setup** → [Quick Setup](/ExtNsT3AF/SetupWizard/Index)
- **View Logs** → [AI Usage & Logs](/ExtNsT3AF/AIUsageAndLogs/Index)

## Tips

- Set one clear **default provider** — avoids confusion for editors
- Test providers after every key rotation
- Review usage weekly for cost control
- If credits balance is low, purchase more before editors hit errors

## When the dashboard shows red

1. Open [AI Providers](/ExtNsT3AF/AIProviders/Index) → run **Test connection**
2. Check vendor status page (OpenAI, Anthropic, etc.)
3. Verify firewall allows outbound HTTPS
4. Check [AI Logs](/ExtNsT3AF/AIUsageAndLogs/Index) for the exact error message
5. See [Known Problems](/ExtNsT3AF/KnownProblems/Index) if the issue persists
