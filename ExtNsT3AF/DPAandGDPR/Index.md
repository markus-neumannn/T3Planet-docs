---
title: "Data Processing Agreement (DPA) & General Data Protection Regulation (GDPR)"
description: "T3AF GDPR-related questions for providers, prompts, usage, logs, and technical data-management capabilities."
keywords:
  - "TYPO3"
  - "T3AF"
  - "DPA"
  - "GDPR"
  - "AI Foundation"
sidebarTitle: "DPA & GDPR"
---

This page describes GDPR-related questions about providers, prompts, usage,
and logs, and the **technical data-management capabilities** in AI Foundation.

T3AF is the shared backend AI layer. It has **no frontend visitor plugin**.
Visitors only hit AI through child extensions (T3AS, T3AC, T3AA).

- T3AS / T3AC — yes, frontend search and chatbot. See
  [T3AS DPA & GDPR](/en/latest/ExtNsT3AS/DPAandGDPR/Index) and
  [T3AC DPA & GDPR](/en/latest/ExtNsT3AC/DPAandGDPR/Index).
- T3AA — accessibility overlay; different processing than LLM chat. See
  [T3AA DPA & GDPR](/en/latest/ExtNsT3AA/DPAandGDPR/Index).

## Product controls

- **Your Own API Keys (BYOK)** — default. AI traffic: customer server →
  configured provider. T3Planet is not on this path.
- **T3Planet Credits** — optional. Billable calls go to T3Planet
  (`/API/AI/*`). Prompts/inputs may be stored in T3Planet billing records
  (`meta_json`) for support, fraud prevention, and cost reconciliation.
- **AI Logs cleanup** — `t3af:ai-logs:cleanup`, default **90 days**, not
  created automatically.
- **MCP cleanup** — `t3af:mcp:cleanup` (expired OAuth tokens/codes and
  stale MCP sessions). Not created automatically.

## AI provider mode (BYOK vs Credits)

### Your Own API Keys (BYOK) — default

AI requests go from the customer TYPO3 server to the AI provider you
configure, using your own API keys. **T3Planet is not in the AI data path.**

AI Foundation makes **no product licence call** and sends T3Planet nothing
for T3AF activation.

Premium extensions that depend on AI Foundation use `ns_license` for their
own licence management. That is separate from the AI request path.

### T3Planet Credits — optional

When Credits is enabled, billable calls (`complete`, `stream`, `embed`,
and related billed features) go to the T3Planet composer API
(`/API/AI/*`).

What may be transmitted in Credits mode:

- Site domain and optional contact name/email (trial token identity)
- `feature_key`, `request_uuid`, and billing metadata
- Prompts and model inputs **may be stored** in T3Planet billing records
  (`meta_json`) for support, fraud prevention, and cost reconciliation —
  see T3Planet terms and DPA

More details: [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index).

## Logging privacy level

On each AI provider record: **standard** / **reduced** / **none** (optional
UserTSconfig `nst3af.privacyLevel`; the strictest of provider + user
applies).

Local logs never store prompt or response text. Privacy level controls
**local AI Usage telemetry only**. It does **not** redact, strip, or block
prompts, brand context, or documents sent to the AI provider.

See [AI Providers](/en/latest/ExtNsT3AF/Configuration/AIProviders/Index)
(privacy level) and
[AI Usage & Logs](/en/latest/ExtNsT3AF/Configuration/AIUsageAndLogs/Index).

| Level | Local AI Usage (`tx_nst3af_request_log`) |
| --- | --- |
| **standard** (default) | Row written: tokens, timing, SHA-256 prompt fingerprint, technical `raw_meta`. Prompt and response text are not stored. |
| **reduced** | Row written: counters and identifiers only (tokens, timing, cost, provider, feature, user). Fingerprint and `raw_meta` stripped. Prompt and response text are not stored. |
| **none** | No request-log row. |

## AI Logs cleanup

```bash
vendor/bin/typo3 t3af:ai-logs:cleanup --days=90
```

- Cleans AI Foundation **system log** (`sys_log`) channels
- Default **90 days** when scheduled
- The task is **not created automatically**

**AI Usage** rows (`tx_nst3af_request_log`) have **no automatic purge** by
default (delete in the backend). Provider field `retention_days_override`
is stored but **not wired** to cleanup.

## Data Processing Agreement (DPA) Considerations

Administrators should consider and document:

- Local request logging vs outbound AI provider transfer (independent)
- BYOK vs Credits (who is a processor)
- Retention of AI Logs vs AI Usage vs visitor history (three different stores)
- Brand context and AI prompts stored in TYPO3 and injected into provider
  calls
- Provider contract / DPA must cover no model training

## Data Processing Agreement (DPA) Questions

**Question:** Does AI Foundation collect frontend visitor information?

**Answer:** **No.** AI Foundation is a backend foundation. It does not provide a public plugin and does not store visitor IP addresses, cookies, or frontend-user accounts as dedicated fields.

**Question:** What is stored in AI Usage?

**Answer:** Table `tx_nst3af_request_log`, typically:

- Provider, extension, feature, request source
- Token counts, latency, success/failure
- Backend user (`0` for anonymous frontend)
- **SHA-256 prompt fingerprint** — not the full prompt or response
- Technical `raw_meta` (adapter type, page id, error message, credits
  request uuid) at standard privacy

See [AI Usage & Logs](/en/latest/ExtNsT3AF/Configuration/AIUsageAndLogs/Index).

**Question:** What is stored in AI Logs?

**Answer:** Operational `sys_log` lines (extension, channel, message, user). For anonymous frontend the user is `0`.

**Question:** Are IP, session, cookies stored in AI Usage?

**Answer:** **No dedicated visitor IP / session / cookie fields.**

**Question:** Can logging be reduced?

**Answer:** **Yes.** Privacy level **reduced** = counters and identifiers only; no fingerprint and no raw metadata. **none** = no AI Usage row.

A user may only tighten logging (UserTSconfig), never loosen a stricter
provider setting. This does not change what is sent to the AI provider.

**Question:** Retention — AI Logs?

**Answer:** Cleanup command available; default **90 days** when scheduled.

**Question:** Retention — AI Usage?

**Answer:** **No automatic purge** by default. Delete in the backend. Provider `retention_days_override` is stored but **not wired** to cleanup.

**Question:** What is sent to the AI provider (BYOK)?

**Answer:** Prompt / editorial or search payload built by the child extension, plus system/brand context. T3Planet is not in the path.

**Question:** What is sent if Credits is on?

**Answer:** Feature key, request metadata, site domain, optional contact; prompts/inputs may be stored by T3Planet for billing. Do not enable Credits for a minimisation setup.

See [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index).

**Question:** MCP?

**Answer:** If enabled, MCP clients can access configured TYPO3 tools. Treat as a separate access-control topic, not visitor Usage Analytics.

See [MCP Server](/en/latest/ExtNsT3AF/Integrations/MCPServer/Index).

<Note>
This documentation describes technical data-management capabilities. It does not constitute legal advice.
</Note>
