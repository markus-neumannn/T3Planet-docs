---
title: "Update Version"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_RevolutionSlider"
  - "Update Version"
  - "UpdateVersion"
sidebarTitle: "Update Version"
---

To update this premium product's version, please refer to this documentation: [License Update Version guide](/License/UpdateVersion/Index)

<Warning>

Before you update `EXT:ns_revolution_slider`, carefully follow the upgrade rules below. Skipping a major version can break your sliders and migrations.

</Warning>

### Upgrade One Major Version at a Time

When you update `EXT:ns_revolution_slider`, always move **one major version at a time**. Do not jump directly to a much newer major version.

This extension includes WordPress and Slider Revolution. Each major version may include required WordPress and Slider Revolution migrations for database tables, slides, and addons.

If you skip a major version, those migrations will not run. You may then face issues such as:

- Slider Revolution modules opening with *"No active slides found"*
- Missing or incomplete slides
- Broken frontend sliders
- Missing or incorrectly migrated addons

### Required Upgrade Path

Before you move to the next major version, first install the **latest patch release** of your current major version.

**General rule:**

```text
vN → latest vN → vN+1 → vN+2 → … → target version
```

Use the table below to plan your update path:

| Current Version | Target Version | Required Upgrade Path |
| --- | --- | --- |
| v11 | v13 | Latest v11 → v12 → v13 |
| v12 | v14 | Latest v12 → v13 → v14 |
| v13 | v14 | Latest v13 → v14 |

### Examples

**Do not update like this:**

```text
v12.x → v14.x
```

This skips the v13 WordPress/Slider Revolution migration.

**Do not update like this:**

```text
v3 → v12  or  v3 → v14
```

This skips all required major-version migrations between your current and target versions.

**Update like this instead:**

Upgrade one major version at a time. Always install the latest patch release of each major version before moving to the next.

### Steps to Follow After Every Major Version Upgrade

After each major version upgrade, complete these steps before continuing to the next major version:

1. Take a backup of the code and database before starting the upgrade.
2. Run the TYPO3 extension setup and upgrade wizards.
3. Open **TYPO3 → Slider Revolution** and complete the WordPress and Slider Revolution migration points.
4. Check the frontend and confirm that all sliders are working correctly.

### If You Already Skipped a Major Version

If you already skipped a major version, restore the affected module from a backup created before that upgrade.

Then follow the correct upgrade sequence:

```text
Current version → latest patch → next major → latest patch → next major → … → target version
```

This ensures that all required WordPress and Slider Revolution migrations run in the correct order.
