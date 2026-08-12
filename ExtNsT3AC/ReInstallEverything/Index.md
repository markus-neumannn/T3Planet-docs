---
title: "Reinstall After Upgrading to Extension v14.x.x"
description: "The steps below are required only when upgrading to Extension v14.x.x from an earlier version."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Reinstall After Upgrading to Extension v14.x.x"
sidebarTitle: "Reinstall After Upgrading to Extension v14.x.x"
---

<Info>
This upgrade introduces major breaking changes.

The steps below are required **only when upgrading to Extension v14.x.x** from an earlier version.

Before starting the reinstallation process, ensure that you review and complete every step in the order provided.

Skipping or changing the sequence of these steps may result in configuration issues, missing functionality, or data inconsistencies.

If you are performing a fresh installation or upgrade extension, please follow the instructions in the [Installation](/ExtNsT3AC/Installation/Index) section.
</Info>

## Overview

T3AC now works as a child extension of T3AF (`ns_t3af`).
If you used T3AC with the previous standalone setup, this guide explains how to move your chatbot project to the new parent-extension architecture.

## Previous Version

Earlier T3AC projects usually followed this pattern:

1. Install T3AC directly
2. Configure chatbot-related AI settings inside the child extension
3. Start training content and serving chatbot answers

## New Architecture

T3AC still provides the chatbot, training, and embed workflows, but T3AF now handles the shared provider setup, prompts, AI features, and common AI services used by those workflows.

## Before Updating

Before you update, make sure you:

- complete the **Backup Project** steps below (trained `t3cs_` data and AI API keys)
- test the migration on staging first
- verify TYPO3 and PHP compatibility
- install or update T3AF
- prepare the provider credentials used for chatbot answers and training

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
4. Verify that T3AF can complete a test AI request.
5. Install or update T3AC.
6. Run the Database Analyzer and apply pending changes.
7. Clear TYPO3 caches.
8. Re-check chatbot configuration, prompts, and provider access.
9. Re-sync or retrain data if your chatbot depends on indexed content.
10. Test the chatbot in the backend and on the frontend.

## What users should do after updating

After the update, confirm that:

- the chatbot opens correctly
- training still completes without errors
- answers still use the expected data and tone
- source links or embed behavior still work where enabled
- logs and usage tracking still show activity

## Recommended Post-Update Checks

- Test one chatbot question with a real project query
- Review greeting, welcome text, and prompt behavior
- Verify the training pipeline and data source sync
- Check one external embed if your project uses it
- Review AI logs for failed requests or training issues

## Common Migration Issues

- **T3AF is not installed**: T3AC now depends on `ns_t3af`.
- **Provider setup is incomplete**: chatbot requests may fail until the shared provider setup is finished.
- **Answers changed after the update**: review chatbot prompts and training data.
- **Chatbot opens but has weak results**: re-check training, source data, and prompt instructions.

## Related Documentation

- [Installation](/ExtNsT3AC/Installation/Index)
- [Configuration](/ExtNsT3AC/Configuration/Index)
- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index)
