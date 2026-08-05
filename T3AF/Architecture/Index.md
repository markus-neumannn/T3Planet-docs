---
title: "Architecture"
description: "Architecture of EXT:ns_t3af — services, adapters, caching, and constraints."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "Architecture"
sidebarTitle: "Architecture"
---

## Overview

T3AF is a shared foundation layer:

```php
Consuming Extension Code
        |
        v
AiServiceInterface
        |
        v
AdapterRegistry -> Provider adapters
        |
        v
   Provider APIs
```

Parallel support:

```php
AiStatisticsService -> OpenAiOrganizationUsageService -> OpenAI Usage API
HttpAuthUtility    -> Protected URL fetching with optional Basic Auth
```

## AI Prompts (T3AI)

Management UI for T3AI global and sidebar prompts lives in **T3AF → AI Prompts**.
Built-in defaults are defined in `ns_t3ai` (`PromptContractRegistry`); the database stores custom overrides only.

See `PromptManagementProvidersAndFeatures.md` and `PromptsSystemReference.md` in this directory for routes, UI behaviour, and class reference.

## Main components

- **Request orchestration**: `AiServiceInterface` and `AiService`
- **Provider adapters**: `AdapterRegistry` and `AdapterInterface` implementations
- **Statistics processing**: `AiStatisticsService` and `OpenAiOrganizationUsageService`
- **Engine configuration filtering**: `AiEngineConfiguration`
- **Utility and environment helpers**: `AiUniverseUtilityHelper`
- **HTTP auth helper**: `HttpAuthUtility`

## Configuration model

Runtime behavior is mostly driven by extension configuration keys from
`ext_conf_template.txt`.

This includes:

- provider keys and models
- default engine selection
- token/temperature values
- basic auth settings

## Caching

The extension registers cache `nst3af_statistics` in
`ext_localconf.php`.

Statistics service stores processed data in this cache to reduce repeated
usage API calls.

## Constraints

- No native frontend plugin and no Fluid frontend output in this package.
- Primary role is reusable service infrastructure.
