---
title: "Upgrade Guide For Container"
description: "Upgrade Product ≥ v3.3.0 Migration from Grid Elements to Container"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "EXTKarma"
  - "Upgrade Guide For Container"
sidebarTitle: "Upgrade Guide For Container"
---

## Upgrade Product ≥ v3.3.0 (Migration from Grid Elements to Container)


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmmfzb7e34zyenr99ilwz0i7z" loading="lazy" title="Upgrade Product >= v3.3.0" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
From version **3.3.0** onwards, this product introduces major changes by
migrating from the outdated **Grid Elements (EXT)** extension to the modern
**Container (EXT)** extension. Please follow the step-by-step migration
guide below.

1. Go to **NITSAN → License Manager** and update **T3Karma Theme (EXT)**
to the latest version.
2. Update **Base Theme (EXT)** to at least **v11.5.x**.
3. Go to **Admin Tools → Maintenance** module and clear the cache.
Also click the **Dump Autoload** button. For composer-based TYPO3 installations, run the following command:

```bash
composer dump-autoload
```
4. Install the **Container extension (EXT)**.
5. Go to **Admin Tools → Upgrade** and click **Run Upgrade Wizard**.
6. Execute the **Grid to Container Migration** wizard.
7. Go to **Admin Tools → Extensions**, then **deactivate and delete**
**Grid Elements (EXT)**.
8. Go to **Admin Tools → Maintenance** and clear the cache again.

<Tip>
After completing these steps, all **grids (including structure and data)**
will be successfully migrated from **Grid Elements (EXT)** to the
**Container extension (EXT)** in TYPO3.
</Tip>

## Upgrade Product ≥ v13.0.2 (Migration from FlexForm Elements to Content Blocks)


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmmfzynh40001ye0j95r9zk92" loading="lazy" title="Upgrade Product >= v13.0.2" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
From version **13.0.2** onwards, this product introduces major changes by
migrating from outdated **FlexForm-based elements** to modern
**Content Blocks (EXT)**. Please follow the step-by-step migration guide below.

1. Go to **NITSAN → License Manager** and update **T3Karma Theme (EXT)** to the latest version.
2. Make sure the **Content Blocks extension (EXT)** is installed, as it is required for this migration.
3. Go to **Admin Tools → Maintenance** module and clear the cache. Also, click on the **Dump Autoload** button. For composer-based TYPO3 installations, run the following command:

```bash
composer dump-autoload
```

<Warning>
Before running the **Upgrade Wizard**, please ensure that you create a **backup of your database**.
</Warning>

1. Go to **Admin Tools → Upgrade** and click **Run Upgrade Wizard**.
2. Click the **Execute** button for **T3Karma: Content Block Migration**.

<Note>
Due to a technical limitation, **Carousel elements** cannot be migrated automatically to **Content Blocks** and must be migrated manually.
</Note>

After completing these steps, all **Custom Elements (structure and data)** will be successfully migrated from **FlexForm Elements** to **Content Blocks (EXT)**.

## Figures

![typo3_dumpautoload](./images/typo3_dumpautoload2.jpeg)

![typo3_upgrade_wizard](images/typo3_upgrade_wizard2.webp)

![migrate_gridelement_to_container](images/migrate_gridelement_to_container2.webp)
