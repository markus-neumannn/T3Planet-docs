---
title: "Installation"
description: "This guide helps you install T3AC Premium EXT:nst3ac on a TYPO3 project for the first time."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Installation"
sidebarTitle: "Installation"
---

This guide helps you install **T3AC Premium** (`EXT:ns_t3ac`) on a TYPO3 project for the first time.

T3AC needs **T3AF** (`EXT:ns_t3af`). T3AF connects your AI providers (API keys, models, prompts, and shared AI services). Without it, T3AC cannot run.

These extensions do **not** change how your website looks on the frontend by themselves. They work in the backend and power the AI chatbot. **Keep both T3AC and T3AF enabled.**

## Quick overview for new customers

You will install and activate these pieces:

1. **License Manager** (`EXT:ns_license`) — unlocks your Premium download
2. **T3AC** (`EXT:ns_t3ac`) — the AI Chatbot extension (and related packages such as T3CS where required)
3. **T3AF** (`EXT:ns_t3af`) — shared AI engine used by T3AC (free on TER)
4. **Database updates** — so TYPO3 creates the required tables
5. **TypoScript includes** — load the required static TypoScript
6. **AI provider setup** — so T3AC can send AI requests
7. **Final check** — confirm modules load and the license is active

Follow the steps below in order. Choose **either** Non-Composer **or** Composer in Step 2 — not both.

After installation, you will use the T3AC backend module to:

- Manage **data sources** such as sitemaps, PDFs, TYPO3 pages, web pages, and Q&A records.
- Run a **training pipeline** that keeps chatbot answers in sync with your project content.
- Configure and monitor the **AI chatbot**.
- View **usage analytics** for chatbot activity.

<Info>
If you are upgrading from an older version (**2.2.1** or earlier) to the latest release,
follow [Reinstall After Upgrading](/ExtNsT3AC/ReInstallEverything/Index) instead of this installation guide.
</Info>

## Before you start

Make sure you have:

- Backend access as an administrator
- Your **T3AC license key** from T3Planet
- Decided whether your project uses **Composer** or the **TYPO3 Extension Manager**
- An AI provider account/API key ready (for example OpenAI) for Step 6

## Step 1 — Install the License Manager

Install the latest version of `EXT:ns_license` before continuing.

The License Manager controls access to T3Planet Premium packages and is required to download and activate T3AC.

## Step 2 — Activate the License

Pick the path that matches your project.

### Non-Composer Installation

Use this workflow when your project installs T3Planet extensions from the TYPO3 backend:

1. Open **Admin tools** → **T3planet License Manager**.
2. Enter your T3AC license key.
3. Activate the license.
4. Confirm that the latest T3AC package is downloaded.
5. Confirm that T3AF (`EXT:ns_t3af`) is installed automatically or available after activation.

### Composer Installation

Use this workflow when your TYPO3 project is managed with Composer:

1. Check the T3Planet Composer repository configuration.
2. Update the `only` parameter so the project can download T3AC and T3CS: "only": [
  "nitsan/ns-t3ac",
  "nitsan/ns-t3cs"
]
3. Install the T3AC package: composer require nitsan/ns-t3ac
4. Verify that the installation completed successfully.
5. Confirm that T3AF (`nitsan/ns-t3af` / `EXT:ns_t3af`) is installed. If it is missing, install it using **Step 3 — Install T3AF**.

Full license activation details:
[https://docs.t3planet.de/en/latest/License/LicenseActivation/Index.html](/License/LicenseActivation/Index)

## Step 3 — Install T3AF

T3AF (`EXT:ns_t3af`) is required before T3AC can be used.
It provides the shared AI provider configuration, models, API access, logs, and service layer used by T3AC.

If T3AF was already installed in Step 2, you can skip to Step 4.

**T3AF** is the shared AI infrastructure for T3Planet AI Universe extensions.
Complete the parent setup first, then continue with the remaining T3AC steps below.

T3AF is available from the TYPO3 Extension Repository (TER).

Download / TER page: [https://extensions.typo3.org/extension/ns_t3af](https://extensions.typo3.org/extension/ns_t3af)

### Option 1 — Extension Manager (TER)

1. Open **Admin Tools** → **Extensions**.
2. Select **Get Extensions**.
3. Search for `ns_t3af` or **T3AF**.
4. Install and activate the extension.
5. Flush all TYPO3 caches.

### Option 2 — Composer

If T3AF is not already present after installing T3AC, install it with:

```bash
composer require nitsan/ns-t3af
```

Then flush all TYPO3 caches.

Helpful T3AF references:

- [T3AF Installation](/T3AF/Installation/Index)
- [T3AF Configuration](/T3AF/Configuration/Index)
- [AI Providers](/T3AF/Configuration/AIProviders/Index)

## Premium Version

**T3AC** is a Premium extension and requires a valid T3Planet license for download and activation.

For license activation and access to premium features, see:
[https://docs.t3planet.de/en/latest/License/Index.html](/License/Index)

<Note>
**T3AF** (`EXT:ns_t3af`) is free and available from the TYPO3 Extension Repository (TER).
Premium licensing applies to **T3AC** — not to T3AF.
</Note>

## Step 4 — Run Database Analyzer

After installing the extension, apply all pending database changes:

1. Open **Admin Tools**.
2. Go to **Maintenance**.
3. Open **Analyze Database Structure**.
4. Apply all pending database schema updates.

Run this before using T3AC modules in the TYPO3 backend.

## Step 5 — Configure/Load required TypoScripts

T3AC and T3CS ship static TypoScript that must be included on your site.

1. Switch to the root page of your site.
2. Open the **TypoScript** module and select **Edit TypoScript Record** / **Info/Modify**.
3. Click **Edit the whole template record** and open the **Includes** tab.
4. Under **Include static (from extensions)** / site sets, add:
  - `AI Chatbot/Search - TYPO3 Extension [nitsan/ns-t3cs]`
  - `AI Chatbot - TYPO3 Extension [nitsan/ns-t3ac]`
5. Save the template and flush TYPO3 caches.

## Step 6 — Configure the AI Provider

After installation:

1. Open **T3AF** in the TYPO3 backend.
2. Configure your preferred AI provider.
3. Save the provider and model configuration.
4. Verify the AI connection with a test request.

T3AC will not function correctly until T3AF has a working AI provider configuration.

## Step 7 — Verify the Installation

Before handing the system to editors, verify that:

- `EXT:ns_t3ac` is installed and active.
- `EXT:ns_t3af` is installed and active.
- The T3AC license is active.
- Database Analyzer changes are applied.
- The AI provider is configured in T3AF.
- TYPO3 caches are cleared.
- T3AC backend modules load without errors.

If all items above are true, installation is complete. Next, add data sources and run training in the T3AC module.
