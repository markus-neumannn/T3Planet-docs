---
title: "Migration To New Composer"
description: "Good news Team T3Planet proudly launches a new composerway installation, heaven for our beloved TYPO3 customers and their TYPO3 team."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "License"
  - "Migration To New Composer"
sidebarTitle: "Migration To New Composer"
---

## What’s Migration?

Good news! Team T3Planet proudly launches a new composer-way installation, heaven for our beloved TYPO3 customers and their TYPO3 team.

In the past, we used the concept of **composer vcs + local :@dev`** TYPO3 extension installation and manually downloaded the latest version from the TYPO3 backend license manager module. It was challenging to install, update & maintain the version of your premium TYPO3 extensions.

Our new composer way of TYPO3 extensions installation is just like official composer-things like packagist.org & packagist.com

You will use **`composer req`** for installation and **`composer update`** to automatically get the latest version of your purchased TYPO3 extensions. For example, We support **DevOps Auto-deployment CI/CD**.

We highly recommend migrating the new composer way with the below step-by-step guide.

<Note>
Before you start the migration, we recommend taking a backup (code & database) of your TYPO3 instance. During the migration, If any problem occurs, then you can roll back your TYPO3 instance. So, please take a backup now :)
</Note>

## Migration on New Composer-way

<Warning>
For EXT:ns_revolution_slider TYPO3 extension, please follow special migration guide at https://docs.t3planet.de/en/latest/ExtNsRevolutionSlider/RevolutionSliderLatest/MigrationFrom3toLatest/Index.html
</Warning>

**Step 1.** Remove your TYPO3 extensions

```python
composer remove nitsan/EXTENSION-NAME
composer dump-autoload
composer clear-cache
```

**Step 2.** Manually remove existing TYPO3 Extensions Folder & Symlink

```python
rm -rf typo3conf/ext/extension_key
rm -rf exensions/EXTENSION-NAME
```

**Step 3.** Update EXT:ns_license

```python
composer update nitsan/ns-license

vendor/bin/typo3 typo3 extension:setup
```

**Step 4.** Run Composer Command

```python
composer config repositories.nitsan '{
   "type": "composer",
   "url": "https://composer.t3planet.cloud",
   "only": ["nitsan/EXTENSION-NAME"]
}'
```

```python
composer config http-basic.composer.t3planet.cloud USERNAME LICENSE-KEY
```

```python
composer req nitsan/EXTENSION-NAME --with-all-dependencies
```

```python
vendor/bin/typo3 typo3 extension:setup
```

<Note>
We have already sent the license key & composer credentials (like username, license key) via Email. If you need any help, then write to our support team [https://t3planet.de/support](https://t3planet.de/support)
</Note>
