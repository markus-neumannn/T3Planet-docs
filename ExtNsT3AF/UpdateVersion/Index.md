---
title: "Update Version"
description: "Update Version for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Update Version"
---

Keep **EXT:ns_t3af** up to date for security fixes, new providers, and MCP improvements.

## Update commands

```
composer update nitsan/ns-t3af
vendor/bin/typo3 extension:setup -e ns_t3af
vendor/bin/typo3 upgrade:run
vendor/bin/typo3 cache:flush
```

## After every update

1. Run `extension:setup` — applies database schema changes
2. Flush all caches — backend module and MCP routes refresh
3. Test provider connection in [AI Providers](/ExtNsT3AF/AIProviders/Index)
4. Test MCP if enabled — see [MCP Server](/ExtNsT3AF/MCPServer/Index)
5. Check [AI Usage & Logs](/ExtNsT3AF/AIUsageAndLogs/Index) for errors after a test AI request

## Migration wizard

After upgrade from v1:

```
vendor/bin/typo3 upgrade:run ns_t3afMigrateExtConfProviders
```

Verify all providers migrated correctly before deleting old Extension Configuration keys.

## Best practice

1. Backup database and `composer.lock` before every update
2. Update on **staging** first
3. Update **production** in a low-traffic window
4. Notify editors if MCP or provider settings change

## Rollback

```
# Restore composer.lock from backup first
composer install
vendor/bin/typo3 extension:setup -e ns_t3af
vendor/bin/typo3 cache:flush
```

Restore database only if the new version changed schema and you cannot fix forward.

## Difference between update and upgrade

- **Update** — Routine `composer update` to the latest compatible version
- **Upgrade** — Major version jump (for example v1 to v2) — follow [Upgrade Guide](/ExtNsT3AF/UpgradeGuide/Index) with migration wizards

## Check current version

In TYPO3: Admin Tools → Extensions → `ns_t3af` version column.

Or via Composer:

```
composer show nitsan/ns-t3af
```
