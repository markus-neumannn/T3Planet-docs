---
title: "AI Usage & Logs"
description: "AI Usage & Logs for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "AI Usage & Logs"
---

## Purpose

**Transparency** for every AI request on your TYPO3 instance. Use these screens for budget control, debugging, and compliance.

## AI Usage

**Path:** T3AF → AI Usage

Shows:

- **Request count** — Total AI calls in the selected period
- **Tokens** — Input and output volume
- **Credits** — Consumption when T3Planet Credits is active
- **By extension** — Which extension called AI (T3AI, T3AC, and others)
- **By feature** — For example `seo.meta_description`
- **Time range** — Day, week, or month

**Use for:** budget control, team planning, anomaly detection.

Compare usage trends with credit balance on the [Dashboard](/ExtNsT3AF/Dashboard/Index).

## AI Logs

**Path:** T3AF → AI Logs

Per-request detail includes:

- Timestamp, user, extension, feature
- Provider, model, tokens
- Success or failure

**Use for:** debugging failed requests and compliance audits.

## Scheduler & CLI

**Path:** T3AF → Scheduler & CLI

Background jobs and CLI commands. Example:

```
vendor/bin/typo3 ns_t3af:cache:flush
```

Ensure **scheduler cron** runs every minute on production.

## OpenAI org statistics (optional)

Set `openai_admin_api_key` in Extension Configuration for organization-level usage charts. This is **not** the chat API key. See [Configuration](/ExtNsT3AF/Configuration/Index).

## Privacy

Log detail depends on [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index) privacy level. Configure for GDPR needs before enabling **Full** logging.

## Weekly admin habit

1. Open AI Usage → check trend vs last week
2. Compare to T3Planet Credits balance if applicable
3. Scan AI Logs for repeated failures (same user, same feature)
4. Escalate persistent errors to [Support](/ExtNsT3AF/Support/Index) with log details

## When logs show high usage

- Check [AI Features](/ExtNsT3AF/AIFeatures/Index) — bulk tasks may need a cheaper model
- Review [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index) budgets and rate limits
- Ask editors if a script or loop triggered many requests

## When logs show failures

- Run Test connection in [AI Providers](/ExtNsT3AF/AIProviders/Index)
- Check vendor status and rate limits
- See [Known Problems](/ExtNsT3AF/KnownProblems/Index) and [FAQ](/ExtNsT3AF/FAQ/Index)
