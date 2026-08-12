---
title: "Installation"
description: "This guide helps you install T3AI Premium EXT:nst3ai on a TYPO3 project for the first time."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AI"
  - "Installation"
sidebarTitle: "Installation"
---

This guide helps you install **T3AI Premium** (`EXT:ns_t3ai`) on a TYPO3 project for the first time.

T3AI needs **AI Foundation** (`EXT:ns_t3af`). AI Foundation connects your AI providers (API keys, models, prompts, and shared AI services). Without it, T3AI cannot run.

## Quick overview for new customers

You will install and activate these pieces:

1. **License Manager** (`EXT:ns_license`) — unlocks your Premium download
2. **T3AI** (`EXT:ns_t3ai`) — the AI Assistant extension
3. **AI Foundation** (`EXT:ns_t3af`) — shared AI engine used by T3AI
4. **Database updates** — so TYPO3 creates the required tables
5. **AI provider setup** — so T3AI can send AI requests
6. **Final check** — confirm modules load and the license is active

Follow the steps below in order. Choose **either** Non-Composer **or** Composer in Step 2 — not both.

<Info>
If you are upgrading from an older version (**13.7.0** or earlier) to the latest release,
follow [Reinstall After Upgrading](/ExtNsT3AI/ReInstallEverything/Index) instead of this installation guide.
</Info>

## Before you start

Make sure you have:

- Backend access as an administrator
- Your **T3AI license key** from T3Planet (for Premium)
- Decided whether your project uses **Composer** or the **TYPO3 Extension Manager**
- An AI provider account/API key ready (for example OpenAI) for Step 5

Looking for the Free version instead? Jump to [For Free Version](#t3ai-free-version) at the end of this page.

## Step 1 — Install the License Manager

Install the latest version of `EXT:ns_license` before continuing.

The License Manager controls access to T3Planet Premium packages and is required to download and activate T3AI.

## Step 2 — Activate the License

Pick the path that matches your project.

### Non-Composer Installation

Use this workflow when your project installs T3Planet extensions from the TYPO3 backend:

1. Open **Admin tools** → **T3planet License Manager**.
2. Enter your T3AI license key.
3. Activate the license.
4. Confirm that the latest T3AI package is downloaded.
5. Confirm that AI Foundation (`EXT:ns_t3af`) is installed automatically or available after activation.

### Composer Installation

Use this workflow when your TYPO3 project is managed with Composer:

1. Check the T3Planet Composer repository configuration.
2. Update the `only` parameter so the project can download T3AI:

```json
"only": [
  "nitsan/ns-t3ai"
]
```

3. Install the T3AI package:

```bash
composer require nitsan/ns-t3ai
```

4. Verify that the installation completed successfully.
5. Confirm that AI Foundation (`nitsan/ns-t3af` / `EXT:ns_t3af`) is installed. If it is missing, install it using **Step 3 — Install AI Foundation**.

Full license activation details:
[https://docs.t3planet.de/en/latest/License/LicenseActivation/Index.html](/License/LicenseActivation/Index)

## Step 3 — Install AI Foundation

AI Foundation (`EXT:ns_t3af`) is required before T3AI can be used.
It provides the shared AI provider configuration, models, API access, logs, and service layer used by T3AI.

If AI Foundation was already installed in Step 2, you can skip to Step 4.

**AI Foundation** is the shared AI infrastructure for T3Planet AI Universe extensions.
Complete the parent setup first, then continue with the remaining T3AI steps below.

AI Foundation is available from the TYPO3 Extension Repository (TER).

Download / TER page: [https://extensions.typo3.org/extension/ns_t3af](https://extensions.typo3.org/extension/ns_t3af)

### AI Foundation has two provider modes

In **AI Foundation → AI Providers**, choose how T3AI gets AI access:

**Your Own API Keys**

Use this mode when you want to connect your own AI vendor accounts. You store
and manage your API keys (for example OpenAI, Anthropic, Gemini) in AI
Foundation and run AI features through those providers.

**T3Planet Credits**

**T3Planet Credits** is T3Planet’s managed AI access for AI Foundation. It lets
your TYPO3 site use AI features **without storing or managing your own vendor
API keys**.

**Link for T3Planet Credits:** [T3Planet Credits Documentation](/ExtNsT3AF/T3Planet-Credit-System/Index)

### Option 1 — Extension Manager (TER)

1. Open **Admin Tools** → **Extensions**.
2. Select **Get Extensions**.
3. Search for `ns_t3af` or **AI Foundation**.
4. Install and activate the extension.
5. Flush all TYPO3 caches.

### Option 2 — Composer

If AI Foundation is not already present after installing T3AI, install it with:

```bash
composer require nitsan/ns-t3af
```

Then flush all TYPO3 caches.

Helpful AI Foundation references:

- [AI Foundation Installation](/ExtNsT3AF/Installation/Index)
- [AI Foundation Configuration](/ExtNsT3AF/Configuration/Index)
- [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index)
- [T3Planet Credits](/ExtNsT3AF/T3Planet-Credit-System/Index)

## Step 4 — Run Database Analyzer

After installing the extension, apply all pending database changes:

1. Open **Admin Tools**.
2. Go to **Maintenance**.
3. Open **Analyze Database Structure**.
4. Apply all pending database schema updates.

Run this before using T3AI modules in the TYPO3 backend.

## Step 5 — Configure the AI Provider

After installation:

1. Open **AI Foundation** in the TYPO3 backend.
2. Configure your preferred AI provider.
3. Save the provider and model configuration.
4. Verify the AI connection with a test request.

T3AI will not function correctly until AI Foundation has a working AI provider configuration.

## Step 6 — Verify the Installation

Before handing the system to editors, verify that:

- `EXT:ns_t3ai` is installed and active.
- `EXT:ns_t3af` is installed and active.
- The T3AI license is active.
- Database Analyzer changes are applied.
- The AI provider is configured in AI Foundation.
- TYPO3 caches are cleared.
- T3AI backend modules load without errors.

If all items above are true, installation is complete and you can start using T3AI.

## For Free Version

To install the free version, open the TYPO3 Extension Manager and search for `ns_t3ai`.

**Step 1:** Open the **Extension Manager** module.

**Step 2:** Select **Get the extension** from the dropdown.

**Step 3:** Search for the extension key `ns_t3ai`.

**Step 4:** Click **Retrieve/Update** to import the extension from the repository.

Get the latest version from typo3.org: [ns_t3ai](https://extensions.typo3.org/extension/ns_t3ai//)

## For Premium Version - License Activation

For license activation and premium installation details, see:
[https://docs.t3planet.de/en/latest/License/Index.html](/License/Index)
