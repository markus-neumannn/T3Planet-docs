---
title: "Known Problems"
description: "Known Problems for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Known Problems"
---

Known issues for **EXT:ns_t3af** (June 2026). Check release notes for fixes in newer versions.

## Installation

**``extension:setup`` fails on non-Composer install**

Run autoload merge in Install Tool. Confirm PHP 8.2 or higher. Ensure `scheduler` and `workspaces` are active.

**Composer MCP conflict**

Remove other MCP server packages (`marekskopal/typo3-mcp-server`, `hn/typo3-mcp-server`, and similar) before installing `nitsan/ns-t3af`.

## Providers and credits

**Credits ON but AI fails**

Click **Activate** again after enabling the toggle. See [T3Planet Credits](/ExtNsT3AF/T3PlanetCredits/Index).

**Test connection fails**

Check model ID, API key, and outbound HTTPS. Verify the model exists on your vendor account.

**Empty token after activate**

Verify license domain matches site URL. Re-save license keys at [https://docs.t3planet.de/en/latest/License/Index.html](/License/Index)

## MCP

**Cursor stdio wrong directory**

Wrap the command so the working directory is correct:

```
bash -lc 'cd /project && ddev exec php vendor/bin/typo3 ns_t3af:mcp:serve --no-startup-message -u admin -w 0'
```

**OAuth OK but writes fail**

Check backend user permissions and active workspace. User needs rights on the target table.

**``write_table`` creates hidden records**

Set `hidden=0` after create, or adjust permissions. Test in draft workspace `1` first.

## Documentation

**Old docs mention TYPO3 11 or PHP 7.4**

Incorrect for current `ns_t3af`. Use TYPO3 12.4+ and PHP 8.2+. See [System Requirements](/ExtNsT3AF/SystemRequirements/Index).

## Backend module not visible

Flush all caches. Confirm extension is active. Re-run:

```
vendor/bin/typo3 extension:setup -e ns_t3af
vendor/bin/typo3 cache:flush
```

## High token usage spike

Check [AI Usage & Logs](/ExtNsT3AF/AIUsageAndLogs/Index) for repeating feature names. May be a script loop. Apply rate limits in [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index).

## Report issues

Include:

- TYPO3 version
- PHP version
- `ns_t3af` extension version
- Steps to reproduce
- Exact error message
- Provider mode (BYOK vs T3Planet Credits)
- Whether MCP is enabled

Submit via [Support](/ExtNsT3AF/Support) or [https://t3planet.de/support](https://t3planet.de/support)
