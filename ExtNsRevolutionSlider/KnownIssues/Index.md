---
title: "Known Issues"
description: "Faced Date field error when setting up an extension or analyzing the database?"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_RevolutionSlider"
  - "Known Issues"
  - "KnownIssues"
sidebarTitle: "Known Issues"
---

## Resolving Date Field Error in Extension Setup and Database Analysis

**Faced Date field error when setting up an extension or analyzing the database? here is the solution!**

The problem occures because of SQL version> **sql_modes**,

To fix this error you need to remove **NO_ZERO_IN_DATE** and **NO_ZERO_DATE** from the sql_modes variable.

For this operation, they need to run the below command in SQL.

```
set global sql_mode = 'ONLY_FULL_GROUP_BY,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
```

You can also fix this issues to Upgrading your MariaDB version to **>=10.5.xx**.
