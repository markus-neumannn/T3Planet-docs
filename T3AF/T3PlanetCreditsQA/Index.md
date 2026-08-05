---
title: "T3Planet Credits — QA setup guide"
description: "QA checklist and verification steps for T3Planet Credits."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "T3Planet Credits — QA setup guide"
sidebarTitle: "Credits QA"
---

This guide walks QA through **connecting T3Planet Credits** on a TYPO3 install
and verifying that AI requests (backend and MCP Native mode) route through the
T3Planet cloud API.

For product background see [T3Planet Credits (v1.1+)](/T3AF/DeveloperGuide/T3PlanetCredits/Index) and [T3Planet Credits (v1.1+)](/T3AF/DeveloperGuide/T3PlanetCredits/Index).

## What “connected” means

Credits mode is **fully active** only when **all three** are true:

1. **Credits toggle** is ON (`credit_mode = 1` in `tx_nst3af_runtime_setting`)
1. At least one **valid T3Planet license key** exists in `ns_product_license`
1. **Activate** succeeded and a **Bearer token** was stored (encrypted in
   `tx_nst3af_runtime_setting.token_enc`)

Until **Activate** completes, the UI may show “Credits mode selected” but AI
traffic still uses **Your Own API Keys** (local provider adapters).

## Part A — Prerequisites

### TYPO3 instance

- **TYPO3** — 13.4+ (or the version required by the project).
- **PHP** — 8.2+.
- **Extensions** — `ns_t3af` plus child extensions under test (for example `ns_t3ai`, `ns_t3aa`).
- **License extension** — `nitsan/ns-license` (license rows in `ns_product_license`).
- **Backend user** — Admin, or a user with T3AF module access.

### Network

The TYPO3 server must reach the T3Planet composer API over HTTPS:

- `https://composer.t3planet.cloud/API/AI/*` (Token, Balance, Charge, Stream, …)

On **DDEV/local**, confirm outbound HTTPS from the web container works. Activation
fails with API or connection errors when the host cannot reach T3Planet.

### T3Planet license keys

- Valid license rows in **`ns_product_license`** (T3Planet shop / license activation in TYPO3)
- License is **non-expired** or **lifetime**
- **Domain binding**: the install’s public hostname should match domains registered
  on the license (production, staging, or local as configured on T3Planet). Domain
  mismatches often cause token or API errors.

### MCP + Native AI testing (optional)

- **MCP mode** — **Native** on T3AF → **MCP Server** tab.
- **Credits** — Fully active (see Part B).
- **Expected `aiProvider` in MCP tools** — Single option: `t3planet_credits` (**T3Planet Credits (active)**).

## Part B — Connect T3Planet Credits

### Step 1 — Start the instance

```bash
ddev start
ddev composer install
```

Log in to the **TYPO3 backend** as admin.

### Step 2 — Open T3AF → AI Providers

1. Go to **T3AF**
1. Open the **AI Providers** tab

You should see **AI Provider Mode** with:

- **T3Planet Credits** (recommended)
- **Your Own API Keys**

### Step 3 — Select T3Planet Credits

1. Click the **T3Planet Credits** card
1. Confirm the switch dialog (**Switch to T3Planet Credits**)
1. Expect a notice such as: *Credits mode selected. Click Activate to connect your license.*

Credits are **selected** but **not yet connected**.

### Step 4 — Activate (required)

1. Click **Activate** (on the T3Planet Credits card or dashboard toolbar)
1. The system will:

   - Collect valid license keys from `ns_product_license`
   - Call `POST /API/AI/Token.php` with `license_keys` and `domain`
   - Store the Bearer token (encrypted)
   - Set `credit_mode = 1`
   - Load balance from the T3Planet API

1. On success:

   - Toast: **Credits mode is active.**
   - Page reloads
   - Credits dashboard shows balance, plan, and bundles

### Step 5 — Verify in the backend UI

- **Provider mode** — **T3Planet Credits** selected with **ACTIVE** badge.
- **Provider list** — Read-only; banner that local providers are preserved but not used.
- **Dashboard** — Credit balance visible (not “Activate to load balance”).
- **Buy Credits tab** — Bundles load when the API is reachable.
- **AI Usage log** — After an AI action: provider `t3planet_credits`, status success, credits debited.

### Step 6 — AI smoke test

Without configuring local OpenAI (or other) API keys:

1. Run any T3AI feature (translate content, SEO meta, MCP native tool, …)
1. Open **AI Usage** and confirm:

   - Provider: `t3planet_credits`
   - Status: success
   - Credits debited

If this passes, credits connection is correct.

## Part C — MCP testing (optional)

### Step 1 — Set MCP mode to Native

1. **T3AF → MCP Server**
1. Set mode to **Native** (not Context)
1. Confirm **MCP mode saved.** and refresh to verify persistence

### Step 2 — Connect MCP client

Use MCP Inspector, Claude Desktop, stdio, or HTTP as documented on the MCP Server
tab (OAuth or token as configured).

### Step 3 — Check tool schema

On a native AI tool (for example `t3ai_translate_content`):

- **`aiProvider`** — Dropdown shows `t3planet_credits` only.
- **Description** — States that **T3Planet Credits mode is active**.

Leave `aiProvider` empty or select `t3planet_credits` — both route through credits.

### Step 4 — Run tool and verify log

Same as Part B Step 6: **AI Usage** must show `t3planet_credits`, not local
provider identifiers such as `openai-1`.

## Part D — Switch back to Your Own API Keys

For comparison testing:

1. **AI Providers** → **Your Own API Keys** → confirm switch
1. Configure at least one **connected** provider (API key + **Test connection**)
1. MCP Native tools should list local providers in `aiProvider`
1. **AI Usage** should show the local provider identifier, not `t3planet_credits`

## Part E — Troubleshooting

- **Activate: “No T3Planet license keys found”** — No valid `ns_product_license` rows. Activate T3Planet extension licenses in TYPO3 first.
- **Activate: API / network error** — Cannot reach `composer.t3planet.cloud`. Fix outbound HTTPS and retry Activate.
- **Toggle ON but no balance / “click Activate”** — Token not minted. Click **Activate** (toggle alone is insufficient).
- **Credits “on” but AI uses local provider** — Credits not fully active (no token). Re-run Activate; check `tx_nst3af_runtime_setting`.
- **MCP lists `openai-1`, `mistral-…` in `aiProvider`** — Credits not active or stale MCP schema. Confirm ACTIVE plus balance; flush caches; reconnect MCP client.
- **Domain / license errors from API** — Hostname not on license. Register DDEV or staging domain on the T3Planet license.
- **AI fails: proxy unreachable** — Credits ON but API unreachable. Fix connectivity or switch to **Your Own API Keys** temporarily.

### Optional DB check (dev/QA)

```sql
SELECT credit_mode,
       license_keys,
       CASE WHEN token_enc != '' THEN 'yes' ELSE 'no' END AS has_token
FROM tx_nst3af_runtime_setting
WHERE uid = 1;
```

**Active** ≈ `credit_mode = 1`, non-empty `license_keys`, `has_token = yes`.

## Part F — QA checklist

Copy for test runs:

```text
[ ] ns_t3af + child extensions installed and active
[ ] nitsan/ns-license present; valid key(s) in ns_product_license
[ ] Outbound HTTPS to composer.t3planet.cloud works
[ ] Backend: T3Planet Credits selected
[ ] Backend: Activate clicked → success toast + reload
[ ] Balance visible on dashboard
[ ] Provider list read-only under credits mode
[ ] One backend AI action → AI Usage shows t3planet_credits
[ ] (MCP) Native mode saved on MCP Server tab
[ ] (MCP) Tool schema shows t3planet_credits only in aiProvider
[ ] (MCP) Native tool call → credits debited in AI Usage log
[ ] Switch to Your Own API Keys → local providers usable again
```

## Summary

1. **License first** — valid T3Planet keys in TYPO3
1. **AI Providers** → **T3Planet Credits**
1. Click **Activate** (mandatory)
1. Confirm **balance** and **ACTIVE**
1. Smoke-test AI → log must show **`t3planet_credits`**
1. For MCP: **Native** mode + `aiProvider` = `t3planet_credits`
