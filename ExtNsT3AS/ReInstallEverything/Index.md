---
title: "Reinstall After Upgrading to Extension v14.x.x"
description: "The steps below are required only when upgrading to Extension v14.x.x from an earlier version."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AS"
  - "Reinstall After Upgrading to Extension v14.x.x"
sidebarTitle: "Reinstall After Upgrading to Extension v14.x.x"
---

<Info>
This upgrade introduces major breaking changes.

The steps below are required **only when upgrading to Extension v14.x.x** from an earlier version.

Before starting the reinstallation process, ensure that you review and complete every step in the order provided.

Skipping or changing the sequence of these steps may result in configuration issues, missing functionality, or data inconsistencies.

If you are performing a fresh installation or upgrade extension, please follow the instructions in the [Installation](/ExtNsT3AS/Installation/Index) section.
</Info>

## Overview

T3AS now works as a child extension of T3AF (`ns_t3af`).
If you used T3AS with the previous standalone setup, this guide shows how to move your AI search project to the new parent-extension architecture.

## Previous Version

Earlier T3AS projects usually followed this pattern:

1. Install T3AS directly
2. Configure the search-related AI setup inside the child extension
3. Start indexing, training, and answering search requests

## New Architecture

T3AS still provides the search, training, analytics, and frontend answer workflows.
T3AF now provides the shared provider setup, prompts, AI features, and core services used by those workflows.

## Before Updating

Before you update, make sure you:

- complete the **Backup Project** steps below (trained `t3cs_` data and AI API keys)
- test the migration on staging first
- verify TYPO3 and PHP compatibility
- install or update T3AF
- prepare the provider credentials used for search and training

Helpful references:

- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- [T3AF Configuration](/ExtNsT3AF/Configuration/Index)
- [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index)

## Migration Steps

### Backup Project

Before upgrading, make sure to back up the following:

- Already trained database content (all database tables prefixed with `t3cs_`). This allows you to retain your trained data and avoids the need to re-train your content after the upgrade.
- Your AI engine API keys. In the latest version, API keys are managed through the AI Provider configuration, so you will need them when reconfiguring your providers after the upgrade.

Also create a complete backup of your TYPO3 files and full database before you continue.

1. Back up the TYPO3 project as described above.
2. Install or update T3AF (`ns_t3af`).
3. Configure the provider and model setup in T3AF.
4. Verify that T3AF can complete a test request.
5. Install or update T3AS.
6. Run the Database Analyzer and apply pending changes.
7. Run the TYPO3 Upgrade Wizard after updating to TYPO3 v14 so existing plugins are migrated from `list_type` to `CType`. This should be done after the extension update and database changes. The expected result is that legacy plugin registrations are converted to the TYPO3 v14-compatible format. Clear TYPO3 caches afterwards if needed.
8. Clear TYPO3 caches.
9. Re-check T3AS search settings, prompts, and provider access.
10. Re-sync data sources if needed.
11. Run training and test frontend search output.

## What users should do after updating

After the update, confirm that:

- data sources still sync correctly
- training can run without errors
- search answers still return relevant content
- source links, feedback, or chatbot mode still work if enabled
- usage logs and statistics still show activity

## Recommended Post-Update Checks

- Open the Dashboard and confirm the expected provider and model are shown
- Test one sync from a real data source
- Run one training cycle
- Perform a frontend search and review the answer quality
- Confirm the Scheduler task still runs as expected
- Review AI logs for failed training or answer requests

## Common Migration Issues

- **T3AF is not installed**: T3AS now depends on `ns_t3af`.
- **Provider setup is incomplete**: training or answer generation may fail until the shared provider setup is finished.
- **AI Provider Not Connected**: AI features require a successfully connected AI provider. Common causes include a provider that is not connected, no default provider selected, failed authentication, or a model that is not configured. Open T3AF, configure the provider, select a default provider, save the configuration, and verify the connection before testing AI features again.
- **Answers are empty or weak**: re-check prompts, data sources, and training status.
- **Training does not run**: verify the Scheduler task and pending queue items.

## Related Documentation

- [Installation](/ExtNsT3AS/Installation/Index)
- [Update Guide](/ExtNsT3AS/UpdateGuide/Index)
- [Configuration](/ExtNsT3AS/Configuration/Index)
- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index)
