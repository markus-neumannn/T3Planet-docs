---
title: "Frontend Plugins"
description: "TonicTypes frontend plugins — List, Detail, Dynamic, and Plain."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TonicTypes"
  - "tonictypes"
  - "tonictypes_pro"
sidebarTitle: "Frontend Plugins"
---

TonicTypes Core registers four frontend plugins under the **tonictypes** content-element group:

| Plugin | Purpose |
| --- | --- |
| **List** | Multiple records → typically `{records}` |
| **Detail** | One fixed record selected in the plugin → `{record}` |
| **Dynamic** | One record resolved from the URL → `{record}` |
| **Plain** | Fluid only (no record load) |

Add them via the **New content element** wizard.

![Selecting a TonicTypes plugin in the New Content Element wizard](Images/plugin_wizard.webp)

*Selecting a TonicTypes plugin*

<Note>
Before all FlexForm fields are available, select a **Record Storage Page** and save the content element once. This refreshes the form.
</Note>

Configuration details (filters, sorting, templates, overrides): [Plugin configuration](/en/latest/ExtTypoTonic/FrontendPlugins/DisplayRecordsPlugin/Index).
