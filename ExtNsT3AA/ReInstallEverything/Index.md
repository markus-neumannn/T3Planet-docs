---
title: "Reinstall After Upgrading to Extension v14.x.x"
description: "The steps below are required only when upgrading to Extension v14.x.x from an earlier version."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AA"
  - "Reinstall After Upgrading to Extension v14.x.x"
sidebarTitle: "Reinstall After Upgrading to Extension v14.x.x"
---

<Info>
This upgrade introduces major breaking changes.

The steps below are required **only when upgrading to Extension v14.x.x** from an earlier version.

Before starting the reinstallation process, ensure that you review and complete every step in the order provided.

Skipping or changing the sequence of these steps may result in configuration issues, missing functionality, or data inconsistencies.

If you are performing a fresh installation or upgrade extension, please follow the instructions in the [Installation](/ExtNsT3AA/Installation/Index) section.
</Info>

## Overview

T3AA now works as a child extension of T3AF (`ns_t3af`).
If you used T3AA before the new architecture, this guide explains how to move your accessibility-related workflows to the shared T3AF setup.

## Previous Version

Earlier T3AA projects usually followed this pattern:

1. Install T3AA directly
2. Configure AI-related services inside the extension flow
3. Start using metadata, audio, accessibility, or optimization features

## New Architecture

T3AA still provides the editor-facing accessibility and content-support features, but the shared AI setup now belongs to T3AF.
That means provider setup, common AI features, prompts, and shared services should be managed in the parent extension first.

## Before Updating

Before you update, make sure you:

- back up your files and database
- test the migration on staging first
- verify TYPO3 and PHP compatibility
- install or update T3AF
- prepare the provider credentials used for metadata, audio, or related workflows

Helpful references:

- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- T3AF System Requirements
- [T3AF Configuration](/ExtNsT3AF/Configuration/Index)
- [AI Providers](/ExtNsT3AF/Configuration/AIProviders/Index)

## Migration Steps

1. Back up the TYPO3 project.
2. Install or update T3AF (`ns_t3af`).
3. Configure the required providers in T3AF.
4. Verify that T3AF can complete a basic AI request.
5. Install or update T3AA.
6. Run the Database Analyzer and apply pending changes.
7. Clear TYPO3 caches.
8. Re-check T3AA prompt and feature settings if your project uses custom behavior.
9. Test the T3AA features your editors rely on most.

## What users should do after updating

After the update, ask users or project owners to confirm that:

- image metadata and alt-text generation still work
- audio or voiceover output still uses the expected provider
- accessibility-related checks still open and run correctly
- simplified text or related content-support actions still return usable results

## Recommended Post-Update Checks

- Test one image metadata action
- Test one audio or voiceover action if those modules are used
- Open the CKEditor accessibility checker and confirm it still works
- Review AI logs for failed requests
- Re-check provider access if output stops or changes unexpectedly

## Common Migration Issues

- **T3AF is not installed**: T3AA now depends on `ns_t3af` and cannot run correctly without it.
- **Provider setup is incomplete**: audio, metadata, or other AI actions may fail until the provider configuration is finished.
- **Output changed after the update**: review prompts and feature settings if your project used custom wording or provider rules.
- **A feature opens but does not complete**: clear caches and review the related AI logs.

## Related Documentation

- [Installation](/ExtNsT3AA/Installation/Index)
- [System Requirements](/ExtNsT3AA/SystemRequirements/Index)
- [Update Guide](/ExtNsT3AA/UpdateGuide/Index)
- [T3AF Installation](/ExtNsT3AF/Installation/Index)
- [T3AF Configuration](/ExtNsT3AF/Configuration/Index)
