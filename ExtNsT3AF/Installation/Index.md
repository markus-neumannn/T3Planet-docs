---
title: "Installation"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "Installation"
sidebarTitle: "Installation"
---

## Quick start

The recommended way to install this extension is via Composer.

AI Foundation is 100% free and open source (GPL-2.0-or-later). No licence key, no registration and no activation. Use it on development, staging and production.

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmrbnnxgy0cp3qmo5e1ciofeq?utm_source=link" loading="lazy" title="AI Foundation Quick Setup Demo" allow="clipboard-write; fullscreen" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

Install via Composer

```bash
composer require nitsan/ns-t3af
./vendor/bin/typo3 extension:setup
./vendor/bin/typo3 cache:flush
```

Classic TYPO3 sites can also install from the
[TYPO3 Extension Repository (TER)](https://extensions.typo3.org/extension/ns_t3af).

After installation:

1. Activate the extension in Admin Tools > Extensions.
2. Open AI Foundation > Dashboard and confirm the module group is
available.
3. Connect providers and API keys in AI Foundation > AI Providers.
4. Complete guided options with Quick Setup in the AI Foundation
module header.
5. Clear caches in Admin Tools > Maintenance.

Follow this interactive walkthrough for Quick Setup, then continue with the
details below.

![AI Foundation Quick Setup wizard welcome step](./images/quick-setups.webp)

Quick Setup wizard — guided first-time configuration in the AI Foundation module.

Continue with [Configuration](/en/latest/ExtNsT3AF/Configuration/Index#ns-t3af-configuration) for providers, MCP, and
day-to-day module setup.

## Composer installation

### Requirements

Ensure your system meets these requirements:

- **TYPO3** — 12.4 LTS, 13.4 LTS, or 14.x
- **PHP** — 8.2 or higher (8.3 recommended), including `ext-sodium`
- **Composer** — 2.x
- **Database** — MySQL 8.0+ or MariaDB 10.3+
- **Network** — Outbound HTTPS for AI provider API calls

### Required Extensions

Activate these TYPO3 system extensions before AI Foundation:

- **scheduler** — Background AI jobs and scheduled tasks
- **workspaces** — Draft workspaces, MCP workflows, and safe content editing

Both ship with TYPO3. Activate them if they are not already enabled.

### Install AI Foundation

Find it on the [TYPO3 Extension Repository](https://extensions.typo3.org/extension/ns_t3af) or on Packagist as `nitsan/ns-t3af`.

Install AI Foundation via Composer

```bash
composer require nitsan/ns-t3af
```

Or use Admin Tools > Extensions > Get Extensions, search for
`ns_t3af` (or **T3AF**), install and activate it, then flush caches.

No licence key is needed. After installation, AI Foundation is ready to configure.

Product page: [https://t3planet.de/en/ai-foundation-for-typo3](https://t3planet.de/en/ai-foundation-for-typo3)

#### Activate the extension

Confirm `ns_t3af` is active in Admin Tools > Extensions.

#### Set up the database and clear caches

Extension setup and cache flush

```bash
./vendor/bin/typo3 extension:setup
./vendor/bin/typo3 cache:flush
```

## Manual installation

If you cannot use Composer, install the extension from the TER:

1. Open Admin Tools > Extensions > Get Extensions.
3. Search for `ns_t3af` (or **T3AF**), install and activate it.
4. Run **Analyze Database Structure**.
5. Flush caches.

<Warning>
Manual installation requires manual dependency management. Composer
installation is strongly recommended.
</Warning>

## Verify the installation

Confirm that:

- `ns_t3af` is listed as active in Admin Tools > Extensions
- The **AI Foundation** module group appears in the backend sidebar
- **Analyze Database Structure** reports no pending changes for `ns_t3af`

If the module is missing, flush caches and run
`./vendor/bin/typo3 extension:setup` again.

## Next steps

Open AI Foundation > AI Providers to connect at least one provider,
then review [Configuration](/en/latest/ExtNsT3AF/Configuration/Index#ns-t3af-configuration).
