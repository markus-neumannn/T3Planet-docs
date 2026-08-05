---
title: "Privacy"
description: "Privacy, logging levels, and data handling for T3AF."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "Privacy"
sidebarTitle: "Privacy"
---

When **T3Planet Credits** mode is enabled, completion, streaming, and embedding requests are sent to the T3Planet composer API (`Charge`, `Stream`, and `Embed` endpoints).

## Data sent to T3Planet

- **Domain** of the TYPO3 installation (for license and pool matching).
- **License keys** (comma-separated) during activation only via `Token` — stored encrypted locally as `token_enc`.
- **Bearer token** — stored encrypted locally; never exposed to browser JavaScript.
- `meta_json` on debit calls may include the **full prompt text**, feature key, and optional entity metadata for server-side request logging and support.
- **Streaming** sends the same `meta_json` as Charge; partial or full model output may be logged server-side when the stream completes or is aborted.

## Data not sent

- Local provider API keys (BYO mode) are not transmitted when credits mode is active.
- Bearer tokens are never written to TYPO3 request logs or `sys_log` by this extension.

## Retention

Server-side retention of prompts and request metadata is governed by T3Planet's credits platform policy. Contact T3Planet support for export or deletion requests tied to your license pool.

## Legal basis

Ensure your site's privacy policy mentions third-party AI processing when credits mode is enabled, including that prompts may be logged on T3Planet infrastructure for billing and abuse prevention.

## Request log privacy (Your Own API Keys)

When using your own API keys, request log detail is controlled by governance privacy levels
(`standard`, `reduced`, and `none`) on provider records and by UserTSconfig
`nst3af.privacyLevel`. Per-user budgets use `nst3af.budget.*` keys (for example
`nst3af.budget.maxCost` and `nst3af.budget.maxTokens`). See [AI Permissions](/T3AF/GovernanceAndAccess/Index)
documentation for full details.
