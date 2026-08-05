---
title: "Custom AI Features"
description: "Add AI Features cards and settings for your extension."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "Custom AI Features"
sidebarTitle: "Custom AI Features"
---

Use custom AI Features when your extension needs settings cards inside **T3AF → AI Features**.
These cards are used for extension-specific AI configuration such as feature toggles, defaults, API-related options, and provider choices.

## Purpose

AI Features are not prompt templates and not MCP tools.
They are configuration surfaces for extensions that use T3AF.

T3AF renders the card, drawer, AJAX save/load flow, and per-site storage.
Your extension provides the card metadata, allowed settings scope, and field schema.

## Architecture

**Settings schema**
`Configuration/ExtensionSettings/schema.php` points to the field definition file.

**Field definitions**
`Configuration/ExtensionSettings/fields.typoscript` defines the fields shown in the drawer.

**Card provider**
`AiFeatureCardProviderInterface` returns one or more cards for the AI Features overview.

**Scope provider**
`ExtensionSettingsScopeProviderInterface` declares which settings scopes your extension accepts.

**Storage**
Values are stored by T3AF in `tx_nst3af_extension_setting` for the selected site context.

## Implementation steps

1. Add `schema.php` and `fields.typoscript` to your extension.
2. Implement `AiFeatureCardProviderInterface`.
3. Implement `ExtensionSettingsScopeProviderInterface`.
4. Tag both services in your extension.
5. Read saved values at runtime through the T3AF settings service.
6. Flush caches and verify the card in **T3AF → AI Features**.

## Schema example

*Configuration/ExtensionSettings/schema.php*

```php
<?php

declare(strict_types=1);

return [
    'fieldsTemplate' => __DIR__ . '/fields.typoscript',
];
```

## Field example

The category in `# cat=` must match the card's `settingsScope`.

*Configuration/ExtensionSettings/fields.typoscript*

```typoscript
# cat=my ext settings//01; type=boolean; label=Enable AI-assisted generation
enableAiFeature = 0

# cat=my ext settings//02; type=int+; label=Default number of suggestions
defaultSuggestionCount = 3
```

## Service registration

```yaml
services:
  _defaults:
    autowire: true
    autoconfigure: true

  _instanceof:
    NITSAN\NsT3AF\Contract\AiFeatureCardProviderInterface:
      tags: ['t3af.ai_feature_card_provider']
    NITSAN\NsT3AF\Contract\ExtensionSettingsScopeProviderInterface:
      tags: ['t3af.extension_settings_scope']

  MyVendor\MyExt\Feature\:
    resource: '../Classes/Feature/'
```

## Runtime usage

Read settings through the T3AF settings API instead of parsing extension configuration manually.
The saved values are merged with schema defaults.

```php
$settings = $this->extensionSettingsService->getAll('my_ext', $storagePid);
$enabled = ($settings['enableAiFeature'] ?? '0') === '1';
```

## Best practices

- Keep `settingsScope` stable.
- Use clear labels because editors see them in the backend drawer.
- Do not overload one card with unrelated feature groups.
- Use [Feature Provider Overrides](/T3AF/DeveloperGuide/FeatureProviderOverrides/Index) when a feature needs its own provider dropdown.
- Flush caches after changing schema or DI definitions.

## Verification

1. Select a site in T3AF.
2. Open **T3AF → AI Features**.
3. Confirm your card appears.
4. Open the drawer and verify fields from `fields.typoscript`.
5. Save settings and reopen the drawer.
6. Confirm your runtime service reads the saved value.

## Troubleshooting

**Card is missing**

- Confirm the card provider is tagged with `t3af.ai_feature_card_provider`.
- Confirm `isAvailable()` returns `true`.
- Flush TYPO3 caches.

**Drawer says the scope is invalid**

- Confirm the card `settingsScope` is listed by your scope provider.
- Confirm the `# cat=` category matches the same scope.

## Related documentation

- [Feature Provider Overrides](/T3AF/DeveloperGuide/FeatureProviderOverrides/Index)
- [Custom AI Prompts](/T3AF/DeveloperGuide/CustomAiPrompts/Index)
- [AI Features](/T3AF/AIFeatures/Index)
