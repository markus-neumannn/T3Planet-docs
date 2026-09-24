---
title: "Installation"
description: "Install Free TonicTypes Core (k3n/tonictypes) or Premium Professional (k3n/tonictypes_pro) with Site Sets or TypoScript."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TonicTypes"
  - "tonictypes"
  - "tonictypes_pro"
sidebarTitle: "Installation"
---

TonicTypes is available as a **Free** Core package (`k3n/tonictypes`) and a **Premium** Professional package (`k3n/tonictypes_pro`).

Installation differs by version. Site Sets, TypoScript, and cache clearing are shared — see **Configuration** after you install.

## Compatibility

- **TYPO3:** 12.4 – 14.9
- **PHP:** 8.2 – 8.5
- **Free Core:** Composer `k3n/tonictypes`, extension key `tonictypes`
- **Professional:** Composer `k3n/tonictypes_pro`, extension key `tonictypes_pro` (requires Core 2.x, `nitsan/ns-license`, and `nitsan/ns-t3af`)

Free TonicTypes Extension: [https://extensions.typo3.org/extension/tonictypes](https://extensions.typo3.org/extension/tonictypes)

## Install Free Version of the Extension

The Free version is the TonicTypes Core package (`k3n/tonictypes`, extension key `tonictypes`).

### Composer (recommended)

```bash
composer require k3n/tonictypes
```

### Extension Manager / ZIP

Install from the [TER page for tonictypes](https://extensions.typo3.org/extension/tonictypes) if you do not use Composer.

In the TYPO3 backend, open **Admin Tools** → **Extensions**, switch to **Get Extensions**, search for `tonictypes`, then download and install the extension.

![TonicTypes Free extension (tonictypes) in TYPO3 Extension Manager Get Extensions search](Images/tonictypes_em_search_free.webp)

*Extension Manager — search for Tonictypes / `tonictypes`*

![TonicTypes extension listed in the TYPO3 Extension Manager](Images/extension_list.webp)

*Extension Manager after installation*

After install, continue with [Configuration](#configuration).

## Install Premium Version of the Extension

The Premium version is **TonicTypes Professional** (`k3n/tonictypes_pro`, extension key `tonictypes_pro`). Professional depends on Free/Core (`k3n/tonictypes`). Install Core first (see Free install above), then Professional.

### Install Professional

After Core is working:

```bash
composer require k3n/tonictypes_pro
```

Ensure `nitsan/ns-license` and `nitsan/ns-t3af` are available (declared dependencies of `k3n/tonictypes_pro`).

Details: [TonicTypes Professional](/en/latest/TonicTypes/Professional/Index).

### For Premium Version - License Activation

To activate the license and install this premium TYPO3 product, refer to the [License documentation](/en/latest/License/Index).

After install and license activation, continue with [Configuration](#configuration).

## Configuration

Use **either** Site Sets (recommended on TYPO3 v13+) **or** classic TypoScript static templates. You can combine them if you disable **Clear constants** / **Clear setup** on the root `sys_template` so Site Set TypoScript is not wiped.

These steps apply after Free or Premium installation. Premium needs Core configuration plus the Professional set or static template.

### Site Sets (recommended for TYPO3 v13+)

In `config/sites/{identifier}/config.yaml` or via **Sites > Setup**.

**Free (Core only):**

```yaml
dependencies:
  - k3n/tonictypes
```

**Premium (Core + Professional):**

```yaml
dependencies:
  - k3n/tonictypes
  - k3n/tonictypes_pro
```

Plugin options (cache lifetime, Fluid paths, variable names) are available under **Sites > Settings** and stay aligned with `plugin.tx_tonictypes.*` constants.

List sets:

```bash
vendor/bin/typo3 site:sets:list
```

### TypoScript static template (classic)

These steps are the same for Free and Premium:

1. Open the **Template** module on the site root.
2. **Info/Modify** → **Edit the whole template record** → **Includes**.
3. Include **[Tonictypes] General Configuration**.
4. For Premium / Professional, also include **[Tonictypes] Tonictypes Professional**.

![Including TonicTypes static templates (General Configuration and Professional) in the site template](./Images/static_template.webp)

*Static template includes — General Configuration; add Professional for Premium*

### Clear caches

Clear all TYPO3 caches after install or upgrade. After upgrading Core, also run **Analyze Database Structure**.

## Additional configuration

### Predefine templates in TypoScript

```typoscript
plugin.tx_tonictypes.templates {
    myTemplateIdentifier {
      group = General
      icon = EXT:tonictypes/Resources/Public/Icons/Datatype/animal-dog.png
      name = My Test Template
      file = EXT:yourtemplateext/Resources/Private/Templates/Tonictypes/TemplateOne.html
    }
}
```

![Predefined template shown in the TonicTypes template selector](Images/template_selection.webp)

*Predefined template in the selector*

Render with `dv:template.render`. See [ViewHelpers](/en/latest/TonicTypes/ViewHelpers/Index).

### DocHeader “Add record” buttons (Professional)

With Professional installed, show create buttons for selected datatypes in the list module DocHeader. Set Page TSconfig:

```typoscript
tx_tonictypes.docHeaderDatatypes = 1,2,3
```

![Record creation buttons added to the list module DocHeader](Images/docheader_datatypes.webp)

*DocHeader buttons for selected Datatype UIDs*

You can also enable this by selecting a datatype behaviour on the page. See [TonicTypes Professional](/en/latest/TonicTypes/Professional/Index).

### Toolbar item (Professional)

Professional registers a backend toolbar item for recent records and quick create.

![TonicTypes Professional toolbar item in the TYPO3 backend](Images/toolbar_item.webp)

*Professional toolbar item*

Disable per user / group with User TSconfig:

```typoscript
options.tonictypes.disableTonictypesToolbarItem = 1
```

### Frontend record edit button (Core)

When a backend **admin** is logged in and previewing a detail view, Core can show a frontend edit button. Enable with User TSconfig:

```typoscript
options.tonictypes.enableRecordEditButton = 1
```

![Frontend record edit button](Images/record_edit_button.webp)

*Edit button (admin backend session only — not for anonymous frontend users)*

### Branding overrides (typically with Professional)

```typoscript
options.tonictypes.customSupportEmail = support@example.com
options.tonictypes.customLogo = EXT:tonictypes/Resources/Public/Images/logo_tonictypes_pro.svg
options.tonictypes.customLogoBright = EXT:tonictypes/Resources/Public/Images/logo_tonictypes_pro_bright.svg
options.tonictypes.disableSupportMessage = 1
options.tonictypes.disableTonictypesLogo = 1
```

## Upgrade notes (2.1.0+)

- PHP 8.2 or higher
- Use Professional with Core 2.1.0+ (datatype transfer module lives in Core)
- Professional-only field types require `k3n/tonictypes_pro`
- After upgrade: **Analyze Database Structure**, then clear all caches

## Next steps

Continue with [Getting Started](/en/latest/TonicTypes/GettingStarted/Index).
