---
title: "Migration Guide:FlexForm to Content Block"
description: "Migration Guide:FlexForm to Content Block."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3 Bootstrap"
  - "Migration Guide:FlexForm to Content Block"
  - "FlexFormtoContentBlockMigration"
sidebarTitle: "Migration Guide:FlexForm to Content Block"
---

<div className="t3-embed">
<iframe src="https://app.supademo.com/embed/cmpf1zpbo2ciaqm8q3ng5amnj?preview=true&step=1" loading="lazy" title="Upgrade Product >= v13.0.2" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

## Upgrade Product ≥ v13.1.0 (Migration from FlexForm Elements to Content Blocks)

From version **13.1.0** onwards, this product introduces major changes by migrating from outdated **FlexForm-based elements** to modern **Content Blocks (EXT)**. Please follow the step-by-step migration guide below.

1. Go to **Admin Tools → T3planet License** and update **T3Bootstrap Theme (EXT)** to the latest version.
2. Make sure the **Content Blocks extension (EXT)** is installed, as it is required for this migration.
3. Go to **Admin Tools → Maintenance** module and clear the cache. Also, click on the **Dump Autoload** button.
  For composer-based TYPO3 installations, run the following command:
  ```
  composer dump-autoload
  ```

<Warning>
Before running the **Upgrade Wizard**, please ensure that you create a **backup of your database**.
</Warning>

1. Go to **Admin Tools → Upgrade** and click **Run Upgrade Wizard**.
2. Click the **Execute** button for **T3Bootstrap: Content Block Migration**.

After completing these steps, all **Custom Elements (structure and data)** will be successfully migrated from **FlexForm Elements** to **Content Blocks (EXT)**.
