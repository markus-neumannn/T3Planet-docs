---
title: "Migration to License System"
description: "If you are old customers of T3Planet (means the customers who bought product(s) before launching of the new license system of T3Planet), then follow this step-by-step guide to migrate from your non-license to license based our TYPO3."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "License"
  - "Migration to License System"
sidebarTitle: "Migration to License System"
---

# Migration to License System

## What's Migration?

If you bought T3Planet products before the license system was launched, follow this step-by-step guide to move from your non-license version to the license-based version of our TYPO3 products.

<Warning>

Before you start the migration, we recommend taking a backup (code & database) of your TYPO3 instance. If any problem occurs during the migration, you can roll back your TYPO3 instance.

</Warning>

## Get Your License Key

- We have already sent the license keys for your purchased TYPO3 products to your email address.
- Here is the sample license email: [documentation](/en/latest/License/Introduction/Index#sample-license-email)
- If you did not receive the license email, please submit a support ticket and our team will get back to you: https://t3planet.de/support

## Migration on Normal TYPO3 Instance

<Steps>
  <Step title="Step 1">
Go to Admin Tools > Extensions > Deactivate Extension
  </Step>
  <Step title="Step 2">
From Extension Manager > Delete Extension
  </Step>
  <Step title="Step 3">
Follow the step-by-step installation guide at [documentation](/en/latest/License/LicenseActivation/Index#install-via-extension-manager)
  </Step>
</Steps>

## Migration on Composer-based TYPO3 Instance

**Step 1.** Go to Admin Tools > Extensions > Deactivate Extension

**Step 2.** Remove your existing non-license TYPO3 extension

```bash
composer remove nitsan/<PACKAGE-NAME>
composer dump-autoload
composer clear-cache
```

**Step 3.** Manually remove the folder:

```bash
rm -rf typo3conf/ext/extension_key
```

**Step 4.** Follow the Composer installation guide at [documentation](/en/latest/License/LicenseActivation/Index#install-via-composer)
