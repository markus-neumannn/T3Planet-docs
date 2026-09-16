---
title: "Lighthouse"
description: "**Lighthouse** is available under **Scanner → Lighthouse**."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AA"
sidebarTitle: "Lighthouse"
---

**Lighthouse** is available under **Scanner → Lighthouse**.

It uses the **Google PageSpeed Insights API** to analyse **one public page
URL** and returns category scores plus accessibility audit details.

In older documentation this workflow was named **Speed Core Web Vital**. In the
current product, use **Lighthouse**.

Lighthouse results stay on this tab. They are **not** sent to
[Fix Hub](/en/latest/ExtNsT3AA/FeatureGuide/FixHub/Index) — Fix Hub shows
**Scanner** findings only.

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmu2a1u8o0lzaqmrxpu3so1lv?utm_source=link" loading="lazy" title="T3AA Lighthouse Feature Demo" allow="clipboard-write; fullscreen" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

## Steps

1. Configure the **Google PageSpeed API key** in
   **AI Foundation → AI Features → General Settings**.
2. Open **AI Accessibility**.
3. Select the page whose frontend URL should be tested.
4. Open **Scanner → Lighthouse**.
5. Click **Run Lighthouse Scan** and wait for results.
6. Review category scores and accessibility audits.
7. Review failed / manual audits on this Lighthouse results view (not in Fix Hub).

## What you get

* Category scores: Performance, Accessibility, Best Practices, SEO
* Accessibility Health Score gauge
* Failed / passed / manual / not-applicable audits
* Audit rows you can open for detail

Lighthouse analyses **one URL per run**. It is not a multi-page tree scan like
the Scanner.

## Important notes

* **Only a public URL will work.** Google PageSpeed cannot crawl
  `.ddev.site` or `localhost`. Point Site Settings at a public staging URL
  when you need Lighthouse locally.
* Without a PageSpeed API key, Lighthouse cannot run.
* A high accessibility score is a health indicator, not a WCAG conformance
  proof.
* For local HTML checks without a public URL, use the
  [Scanner](/en/latest/ExtNsT3AA/FeatureGuide/Scans/Scanner/Index) instead.
