---
title: "Upgrade Guide"
description: "Upgrade Guide for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Upgrade Guide"
---

Safe upgrades for **EXT:ns_t3af**. Always test on staging before production.

## Before upgrade

1. Read release notes on the T3Planet product page or in official TYPO3 docs
2. Backup database and `composer.lock`
3. Test the upgrade on staging with the same PHP and TYPO3 version as production

## Upgrade commands

```
composer update nitsan/ns-t3af
vendor/bin/typo3 extension:setup -e ns_t3af
vendor/bin/typo3 upgrade:run
vendor/bin/typo3 cache:flush
```

## v1 to v2 migration

If you upgrade from v1 with API keys in Extension Configuration:

```
vendor/bin/typo3 upgrade:run ns_t3afMigrateExtConfProviders
```

This moves legacy API keys into the AI Providers table. Then verify providers in [AI Providers](/ExtNsT3AF/AIProviders/Index).

## Post-upgrade checklist

- Dashboard loads without errors
- Provider Test connection returns green
- MCP shows online (if you use MCP)
- AI Logs show no new errors after a test request
- T3Planet Credits still active (if used) — click **Activate** again if needed

## Rollback

If the upgrade fails on staging:

1. Restore `composer.lock` from backup
2. Run `composer install`
3. Run `vendor/bin/typo3 extension:setup -e ns_t3af`
4. Restore database backup if schema changed

Do not rollback production without a maintenance window.

## When to run full upgrade:run

Always after `composer update nitsan/ns-t3af`. TYPO3 may register new database fields or wizards. Skipping `upgrade:run` causes missing columns or broken backend modules.

## MCP after upgrade

If MCP was enabled before upgrade:

1. Flush all caches
2. Re-run health check from [MCP Server](/ExtNsT3AF/MCPServer/Index)
3. Re-authorize OAuth clients if token lifetime changed

See also [Update Version](/ExtNsT3AF/UpdateVersion/Index) for routine updates.
