---
title: "Using License Key in T3Planet License"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "License"
  - "Using License Key in T3Planet License"
  - "LicenseManager"
sidebarTitle: "Using License Key"
---

## Purpose

Use this workflow to activate a license key, bind it to your domain, and monitor
license health from a centralized TYPO3 dashboard.

## Demo

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmn4aw73y0ooaz3qm7owt0691?embed_v=2&utm_source=embed&step=1" loading="lazy" title="Activate and Manage Extension Licenses with Statistics" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe></div>

## Steps

1. Open TYPO3 Backend and go to `[NITSAN] > [T3Planet License]`.
2. Paste your key into the `[License Key]` field.
3. Click `[Activate License & Download Extension]` to start activation.
4. Confirm domain binding for the current TYPO3 instance when prompted.
5. Open the dashboard statistics area to review license insights.

## License Statistics View

You can typically review:

- Active install/license status
- Expiry and renewal information
- Usage/download-related statistics
- Extension metadata, such as rating/documentation links

[Screenshot: T3Planet License Dashboard]

<Note>

If activation fails, verify that the registered domain matches the current TYPO3
instance URL and that the key has not expired.

</Note>

## Managing Multiple Licenses

1. Stay on the same T3Planet License dashboard.
2. Select another extension/license entry.
3. Repeat activation, renewal, and status checks for each product.
