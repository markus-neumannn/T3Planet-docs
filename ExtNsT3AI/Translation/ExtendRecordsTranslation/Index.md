---
title: "Extend Records Translation"
description: "Configure TCA l10n_mode prefixLangTitle so ns_t3ai can translate specific record fields."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AI"
  - "Translation"
sidebarTitle: "Extend Records Translation"
---

ns_t3ai supports translation of specific fields of TCA records. It understands fields which need to be translated, only if their l10n_mode is set to prefixLangTitle.

For detecting translatable fields, ns_t3ai uses a DataHandler hook.

The following setup is needed, to get ns_t3ai work on your table:

`<extension_key>`/Configuration/TCA/Overrides/`<table_name>`.php

```python
$GLOBALS['TCA']['<table_name>']['columns']['<field_name>']['l10n_mode'] = 'prefixLangTitle';
$GLOBALS['TCA']['<table_name>']['columns']['<field_name>']['l10n_mode'] = 'prefixLangTitle';
```

