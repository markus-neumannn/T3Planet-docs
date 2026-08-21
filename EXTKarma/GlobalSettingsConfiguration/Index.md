---
title: "Theme Options"
description: "Theme options for T3 Karma"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3 Karma"
  - "Theme Options"
  - "GlobalSettingsConfiguration"
sidebarTitle: "Theme Options"
---

Use the configuration method that matches your TYPO3 version:

- **TYPO3 v14 and above** — Site Sets
- **TYPO3 v13 and below** — Theme Options (global and page-level)

<Note>

Theme Options is supported on **TYPO3 v13 and below**. On TYPO3 v14 and above, use [Site Sets and Configuration](#site-sets-and-configuration) instead.

</Note>

## Global-Level Configuration

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmevcuuj3lk6nr99m7i3h5af" loading="lazy" title="Global-Level Configuration" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

This module allows you to configure global settings for the theme and control important aspects of your website from a central place.

### Steps to Configure

1. Navigate to **NITSAN → Theme Options** in the TYPO3 backend.
2. Select the **Root/Main** page from the Page Tree.
3. Configure the available settings such as **General, SEO, Style, Integration**, and other global options.

All theme options are designed to be easy to understand and manage. It is recommended to review and configure these settings during the **initial setup of your website** to ensure everything works correctly.

### General

This tab includes settings related to the **Header, Navigation Menu, Footer, and Site Maintenance**.

You can configure important layout and display options for these elements to maintain consistent behavior across the entire website.

### SEO

This tab contains configuration options related to the site's **SEO settings**.

You can manage basic SEO configurations that help improve your website's visibility in search engines.

### Style

You can manage the **Global styling of the entire website** from this section.

Settings for elements like the **Header, Navigation Menu, and Footer** can be defined here to maintain a consistent design.

<Note>

These global style settings can also be overridden at the page level if needed. To overwrite them, go to **Page Properties → Extended tab** and adjust the settings for that specific page.

</Note>

### Integration

This section allows you to add **custom CSS** as well as **third-party integration scripts**, such as analytics, tracking tools, or other external services.

Using these options, you can easily integrate external services and apply additional styling **without modifying the core theme files**.

## Page-Level Configuration

<Note>

This page-level Theme Options flow applies to **TYPO3 v13 and below**.

</Note>

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmmetrfmf3ka2nr99usu9m6b9" loading="lazy" title="Page-Level Configuration" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

From the **Theme Options** tab, you can directly select a page and create an **Extension Template** to configure the desired style for that specific page.

After creating the extension template for the selected page, you can configure all theme options for that page only. These settings will **override the global theme configuration** for that particular page.

This allows you to customize the **layout or styling of individual pages** without affecting the overall settings of the website.

## Site Sets and Configuration

<Note>

Site Sets apply to **TYPO3 v14 and above**.

</Note>

Site Sets provide a more structured and organized way to manage TYPO3 configuration.

Instead of handling everything manually, you can group configurations into reusable sets. This makes your setup cleaner and easier to maintain.

<div className="t3-embed">
  <iframe src="https://app.supademo.com/embed/cmniqpv2812claburo4qx4t52?preview=true&step=1" loading="lazy" title="Editor Guide" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen ></iframe>
</div>

With Site Sets:

- Configuration becomes more structured
- Reuse of settings is easier
- Setup is more consistent across projects

You can use Site Sets as shown in the demo to simplify your TYPO3 project configuration.

This approach helps reduce complexity and improves long-term maintainability.
