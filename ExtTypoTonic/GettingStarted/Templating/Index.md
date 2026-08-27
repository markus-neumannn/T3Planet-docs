---
title: "Templating"
description: "Templating — TypoTonic (EXT:tonic) documentation."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TypoTonic"
  - "tonic"
  - "TONICTYPES"
sidebarTitle: "Templating"
---

TypoTonic renders your records with standard TYPO3 Fluid templates. This page lists the variables and namespace you need to know.

## Namespace

TypoTonic registers its Fluid namespace automatically once the extension is active.
You do **not** need to add this line to your templates yourself:

```html
{namespace t = Aix\Tonic\ViewHelpers}
```

## Available Variables

- **Records** — When a plugin injects a list of records, they are available as `{records}` by default. This marker name can be changed in the Tonic Constants.
- **Record** — In a single-record context, the current record is available as `{record}`. This marker name can also be changed in the Tonic Constants.
- **Field value** — Read a field's value with `{record.fieldname}`, for example `{record.myfield}`. The value type depends on the field's **Frontend Type Definition**, set on the **Frontend Settings** tab of the field. TYPO3's DataMapper processes the value before it reaches the template.

   Use `<f:debug>{record.fieldname}</f:debug>` to inspect a single value, or `<f:debug>{_all}</f:debug>` to see every variable available in the current template.

## Predefining Templates in TypoScript

You can predefine templates for the template selector instead of choosing a file manually every time.
Add this to your root page TypoScript:

```typoscript
plugin.tx_tonic.templates {
    myTemplateIdentifier {
      group = General
      icon = EXT:tonic/Resources/Public/Icons/Datatype/brick.png
      name = My Test Template
      file = EXT:tonic_templates/Resources/Private/Templates/tonic_test1.html
    }
}
```

![Predefined template shown in the TypoTonic template selector](./Images/template_selection.jpg)

*A predefined template appearing in the template selector*

Once a template is predefined, render it in Fluid with the `Template.RenderViewHelper`:

```html
<t:template.render template="myTemplateIdentifier" arguments="{record:record}" />
```

See [ViewHelpers](/ExtTypoTonic/ViewHelpers/Index) for the full list of ViewHelpers and their arguments.

## Next Step

Continue with [Frontend Plugins](/ExtTypoTonic/FrontendPlugins/Index) to display your records on a page.
