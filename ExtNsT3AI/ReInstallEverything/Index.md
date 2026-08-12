---
title: "Reinstall After Upgrading to Extension v14.x.x"
description: "The steps below are required only when upgrading to Extension v14.x.x from an earlier version."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AI"
  - "Reinstall After Upgrading to Extension v14.x.x"
sidebarTitle: "Reinstall After Upgrading to Extension v14.x.x"
---

<Info>
This upgrade introduces major breaking changes.

The steps below are required **only when upgrading to Extension v14.x.x** from an earlier version.

Before starting the reinstallation process, ensure that you review and complete every step in the order provided.

Skipping or changing the sequence of these steps may result in configuration issues, missing functionality, or data inconsistencies.

If you are performing a fresh installation or upgrade extension, please follow the instructions in the [Installation](/ExtNsT3AI/Installation/Index) section.
</Info>

## Overview

T3AI now runs as a child extension of T3AF (`ns_t3af`).
If you used T3AI before the new architecture, this guide helps you move your existing setup to the shared T3AF model.

## Previous Version

Earlier T3AI projects usually followed a simpler setup:

1. Install T3AI directly
2. Configure the provider inside the child-extension flow
3. Start using page, content, SEO, translation, or media features

## New Architecture

T3AI now depends on T3AF for shared providers, authentication, AI features, prompts, and core services.
T3AI continues to provide the editor-facing workflows, but the shared AI setup now belongs to the parent extension.

## Before Updating

Before you update, make sure you:

- back up your files and database
- test the update on staging first
- check that your TYPO3 and PHP versions are still supported
- install or update T3AF
- prepare access to the AI provider credentials used by your project

Review these pages before you start:

- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- [T3AF Configuration](/ExtNsT3AF/Configuration/Index)
- [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index)

## Migration Steps

1. Back up the TYPO3 project.
2. Install or update T3AF (`ns_t3af`).
3. Configure the provider and model setup in T3AF.
4. Verify that T3AF is active and can complete one test request.
5. Install or update T3AI.
6. Run the Database Analyzer and apply pending changes.
7. Clear TYPO3 caches.
8. Review T3AI prompts and feature settings if your project uses custom output rules.
9. Test one workflow from each important area you use, such as page generation, SEO, translation, or media.

## What to do after updating

After the update, confirm that:

- T3AI opens correctly in the TYPO3 backend
- the shared provider from T3AF is available
- prompts still produce the expected writing style
- page, SEO, translation, or media workflows still return usable results
- logs do not show unexpected provider or request errors

## Recommended Post-Update Checks

- Run one page or content generation test
- Test one SEO action if your project uses SEO automation
- Test one translation or media action if those modules are in use
- Review [AI Logs](/ExtNsT3AI/AISettings/Index) for failures
- Re-check [AI Prompts](/ExtNsT3AI/Prompts/Index) if the wording changed after migration

## Common Migration Issues

- **T3AF is missing**: install `ns_t3af` before updating T3AI.
- **No provider is available**: complete the shared provider setup in T3AF.
- **Generated results look different**: review prompt rules and feature settings after the migration.
- **Modules open but requests fail**: clear caches and check the provider credentials again.

## Related Documentation

- [Installation](/ExtNsT3AI/Installation/Index)
- [System Requirements](/ExtNsT3AI/SystemRequirements/Index)
- [Upgrade Guide](/ExtNsT3AI/UpgradeGuide/Index)
- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- [T3AF Configuration](/ExtNsT3AF/Configuration/Index)
