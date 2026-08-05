---
title: "Migration from v2 to v3"
description: "Migration from v2 to v3 — T3Planet documentation."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "ns_RevolutionSlider"
  - "Migration from v2 to v3"
  - "MigrationFrom2to3"
sidebarTitle: "Migration from v2 to v3"
---

# Migration from v2 to v3

What's TYPO3 Slider Revolution v3? T3Planet is now official partner of Slider Revolution core guys - Themepunch. Team T3Planet feeling proud to launch v3 which includes whole WordPress slider revolution plugin into TYPO3.

We have major breaking changes with v3, now whole approach to create slider is changed. You will able to create slider as just like in WordPress version.

<Warning>

You will need to manually re-create all your sliders in v3. Unfortunately technically it's very difficult to setup migration from v2 to v3.

</Warning>

**Steps to Migration**

> You will need to completely delete existing EXT.ns_revolution_slider v2 extension from your TYPO3 Instance; and Install new v3. Please follows the Step-by-step Guide to migrate from TYPO3 Slider Revolution v2 to v3.
>
>
> 1. Before start, please make sure to take backup of your TYPO3 website.
> 2. Please make sure to latest released version EXT.ns_license https://extensions.typo3.org/extension/ns_license
> 3. Go to Admin Tools > Extensions Manager > De-Activate EXT.ns_revolution_slider v2.
> 4. Go to Admin Tools > Extensions Manager > Delete EXT.ns_revolution_slider from your Extension manager or composer.
> 5. Go to NITSAN > License Management > De-Activate License, Check [documentation](/License/LicenseDeActivation/Index#how-to-de-activate-license-key)
> 6. Follow Installation Steps at /ExtNsRevolutionSlider/RevolutionSlider3./0/Installation/Index
> 7. Follow Configuration Steps at /ExtNsRevolutionSlider/RevolutionSlider3./0/Configuration/Index
