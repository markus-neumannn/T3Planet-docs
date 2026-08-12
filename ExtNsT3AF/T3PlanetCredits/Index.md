---
title: "T3Planet Credits"
description: "T3Planet Credits for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "T3Planet Credits"
---

## Purpose

T3Planet Credits is optional billing for T3AF — **one credit pool** per TYPO3 install, simple activation. Use it when you do not want separate vendor API accounts.

**Path:** T3AF → AI Providers → T3Planet Credits

## How it works

1. Admin turns the credits toggle **ON**
2. Admin clicks **Activate** (toggle alone is not enough)
3. System reads T3Planet license keys
4. Bearer token is stored (encrypted)
5. All AI calls route through the T3Planet API

**Important:** You **must** click **Activate** after enabling the toggle.

## Credits vs Your Own API Keys

**Your Own API Keys (BYOK)** — Add provider keys in [AI Providers](/ExtNsT3AF/AIProviders/Index). Billing goes directly to OpenAI, Anthropic, or other vendors. Best for agencies that already have vendor accounts.

**T3Planet Credits** — Toggle plus **Activate**. Billing uses T3Planet packages. Best for fast start and simple budget control.

When credits are **off**, local provider keys are used normally.

## Credit calculation

```
Credits = max(1, ceil(total_tokens / tokens_per_credit))
```

Default: **1 credit ≈ 1,000 tokens**

## Credits are active when all three are true

1. Credit mode is ON
2. Valid license keys exist in the system
3. Bearer token exists (after **Activate**)

## Dashboard and balance

After activation you see:

- Current balance
- Plan name
- Buy Credits and Pricing links

Check balance regularly on the [Dashboard](/ExtNsT3AF/Dashboard/Index).

## When to use credits

- New project without vendor accounts yet
- Fixed monthly AI budget for editors
- Simplified billing through T3Planet instead of multiple vendor invoices

## When to use own keys

- Enterprise with existing OpenAI or Azure contracts
- Strict data residency with your own EU endpoint
- Very high volume where direct vendor pricing is lower

## Troubleshooting

**AI fails after toggle** — Click **Activate** again. Verify license at [https://docs.t3planet.de/en/latest/License/Index.html](/License/Index)

**Zero balance** — Purchase credits through T3Planet.

**Wrong domain** — Site URL must match the license domain.

**Empty token after activate** — Re-save license keys and activate again.

See also [FAQ](/ExtNsT3AF/FAQ/Index) and [Known Problems](/ExtNsT3AF/KnownProblems/Index).
