---
title: "AI Credits"
description: "AI Credits for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "AI Credits"
---

## Purpose

AI Credits is optional billing for T3AF — **one balance on your account**, usable on any install, simple activation, no licence key. Use it when you do not want separate vendor API accounts.

**Path:** T3AF → AI Providers → AI Credits

## How it works

1. Admin turns the credits toggle **ON**
2. Admin clicks **Activate** (toggle alone is not enough)
3. Bearer token is stored (encrypted)
4. All AI calls route through the T3Planet API

**Important:** You **must** click **Activate** after enabling the toggle.

## Credits vs Your Own API Keys

**Your Own API Keys (BYOK)** — Add provider keys in [AI Providers](/en/latest/ExtNsT3AF/AIProviders/Index). Billing goes directly to OpenAI, Anthropic, or other vendors. Best for agencies that already have vendor accounts.

**AI Credits** — Toggle plus **Activate**. Billing uses T3Planet packages. Best for fast start and simple budget control.

When credits are **off**, local provider keys are used normally.

## Credit calculation

```text
Credits = max(1, ceil(total_tokens / tokens_per_credit))
```

Default: **1 credit ≈ 1,000 tokens**

## Credits are active when both are true

1. Credit mode is ON
2. Bearer token exists (after **Activate**)

## Dashboard and balance

After activation you see:

- Current balance
- Plan name
- Buy Credits and Pricing links

Check balance regularly on the [Dashboard](/en/latest/ExtNsT3AF/Dashboard/Index).

## When to use credits

- New project without vendor accounts yet
- Fixed monthly AI budget for editors
- Simplified billing through T3Planet instead of multiple vendor invoices

## When to use own keys

- Enterprise with existing OpenAI or Azure contracts
- Strict data residency with your own EU endpoint
- Very high volume where direct vendor pricing is lower

## Troubleshooting

**AI fails after toggle** — Click **Activate** again. Check that the server can reach the T3Planet API over HTTPS.

**Zero balance** — Purchase credits through T3Planet.

**Empty token after activate** — Flush caches and activate again.

See also [FAQ](/en/latest/ExtNsT3AF/FAQ/Index) and [Known Problems](/en/latest/ExtNsT3AF/KnownProblems/Index).
