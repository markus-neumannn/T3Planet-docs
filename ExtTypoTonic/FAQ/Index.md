---
title: "FAQ"
description: "Frequently asked questions about TonicTypes Core and Professional."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TonicTypes"
  - "tonictypes"
  - "tonictypes_pro"
sidebarTitle: "FAQ"
---

## General

### What is TonicTypes?

TonicTypes is a TYPO3 extension (`k3n/tonictypes`, key `tonictypes`) that lets you model, manage, and render TCA-based records without creating your own extension. It integrates with FormEngine, TCA, and Workspaces. It is the successor to TypoTonic.

### Free vs Professional?

- **Core** — Datatypes, fields, List/Detail/Dynamic/Plain plugins, ViewHelpers, export/import, dashboard import widget, `default_hidden`.
- **Professional** (`k3n/tonictypes_pro`) — Advanced field types, MCP tools, toolbar, DocHeader buttons, link handler, Form hooks, branding options. Requires Core plus `ns_license` and `ns_t3af`.

### Where do I get the free extension?

[https://extensions.typo3.org/extension/tonictypes](https://extensions.typo3.org/extension/tonictypes)

## Installation and Compatibility

### How do I install TonicTypes?

```bash
composer require k3n/tonictypes
```

Then add Site Set `k3n/tonictypes` or include **[Tonictypes] General Configuration**, and clear caches. Full steps: [Installation](/en/latest/ExtTypoTonic/Installation/Index).

### Which TYPO3 / PHP versions are supported?

TYPO3 12.4–14.9 and PHP 8.2–8.5 (Core and Professional 2.1.x).

## Templates and Rendering

### How do I use my own templates?

Predefine templates under `plugin.tx_tonictypes.templates`, then select them in a plugin or render with `dv:template.render`. See [Templating](/en/latest/ExtTypoTonic/GettingStarted/Templating/Index).

### Which Fluid namespace should I use?

Use **`dv:`** (`K3n\Tonictypes\ViewHelpers`). The old `t:` / `Aix\Tonic` namespace is obsolete.

## Features

### Is export/import Professional-only?

No. From Core 2.1.0, datatype export/import is under **System > Export / Import**.

### What does default_hidden do?

On a Datatype, **Default hidden** makes newly created records start disabled until an editor enables them.

## Didn't find your question?

Vendor support for the extension and Professional: see [Support](/en/latest/ExtTypoTonic/Support/Index).
