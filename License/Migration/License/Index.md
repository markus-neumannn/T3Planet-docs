---
title: "Migration to License System"
description: "If you are old customers of T3Planet (means the customers who bought product(s) before launching of the new license system of T3Planet), then follow this ste…"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "License"
  - "Migration to License System"
sidebarTitle: "Migration to License System"
---

# Migration to License System

## What's Migration?

If you are old customers of T3Planet (means the customers who bought product(s) before launching of the new license system of T3Planet), then follow this step-by-step guide to migrate from your non-license to license based our TYPO3 products.

<Warning>

Before you start the migration, we recommend taking a backup (code & database) of your TYPO3 instance. During the migration, If any problem occurs, then you can roll back your TYPO3 instance. So, please take a backup now :)

</Warning>

## Get Your License Key

- We have already sent your license keys of your purchased TYPO3 products at your email address.
- Here is the sample license email [documentation](/License/Introduction/Index#sample-license-email)
- In case, if you did not such “license email”, please submit support ticket and our executive will get back to you asap https://t3planet.de/support

## Migration on Normal TYPO3 Instance

<Steps>
  <Step title="Step 1">
Go to Admin Tools > Extensions > Deactivate Extension
  </Step>
  <Step title="Step 2">
From Extension Manager > Delete Extension
  </Step>
  <Step title="Step 4">
Follow step-by-step guide installation guide at [documentation](/License/LicenseActivation/Index#install-via-extension-manager)
  </Step>
  <Step title="Step 1">
Go to Admin Tools > Extensions > Deactivate Extension
  </Step>
  <Step title="Step 2">
Remove your existing non-license TYPO3 extension

```python
composer remove nitsan/extension-key-name
composer dump-autoload
composer clear-cache
```
  </Step>
  <Step title="Step 3">
Manually remove folder from `rm -rf typo3conf/ext/extension_key`
  </Step>
  <Step title="Step 4">
Follow step-by-step guide composer based installation guide at [documentation](/License/LicenseActivation/Index#install-via-composer)
  </Step>
</Steps>

---

## Additional content from live docs

## Migration on Composer-based TYPO3 Instance

**Step 1.** Go to Admin Tools > Extensions > Deactivate Extension

**Step 2.** Remove your existing non-license TYPO3 extension

```python
composer remove nitsan/extension-key-name
composer dump-autoload
composer clear-cache
```

**Step 3.** Manually remove folder from rm -rf typo3conf/ext/extension_key

**Step 4.** Follow step-by-step guide composer based installation guide at [https://docs.t3planet.de/en/latest/License/LicenseActivation/Index.html#install-via-composer](/License/LicenseActivation/Index#install-via-composer)
