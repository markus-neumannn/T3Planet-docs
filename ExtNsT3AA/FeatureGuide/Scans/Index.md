---
title: "Scanner"
description: "**Scanner** is the AI Accessibility area where you **check pages** for accessibility problems for the page selected in the TYPO3 page tree."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AA"
sidebarTitle: "Scanner"
---

**Scanner** is the AI Accessibility area where you **check pages** for
accessibility problems for the page selected in the TYPO3 page tree.

Completed runs list findings for the selected scope. Continue remediation in
[Fix Hub](/en/latest/ExtNsT3AA/FeatureGuide/FixHub/Index) — assign, track, and close work there.

The main tab is labelled **Scanner**. Inside it you will find:

* **Scanner** — interactive accessibility check (this is the primary engine)
* **Lighthouse** — Google PageSpeed Insights for one public URL
* **Bulk Scans** — queue pages for scheduled / repeated Scanner runs
  (not a separate scan engine)

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmu2a13j50luqqmrxl9rczxir?utm_source=link" loading="lazy" title="T3AA Scanner Feature Demo" allow="clipboard-write; fullscreen" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

## How it works

1. Open **AI Accessibility**.
2. Select the page (or site root) to use as the scan root.
3. Open the **Scanner** tab.
4. Stay on the **Scanner** sub-tab.
5. Confirm the site URL, set **Depth**, then click
   **Run Accessibility Check**.
6. When the run finishes, review the summary cards and issue list.
7. Open a finding to continue in **Fix Hub**.

## What the Scanner checks

The Scanner checks the **HTML content** of pages in your selected scope
(page + depth) against WCAG-oriented rules.

* It focuses on **page content** (not repeating header/footer chrome), so
  sibling pages can differ.
* When depth includes multiple pages, findings are **merged into one report**
  for the selected root.
* There is **no separate URL list** to maintain — pick a page in the tree,
  choose depth, run (similar to TYPO3 LinkValidator).
* The Scanner needs **no AI provider and no API key**.

Open an issue from the results list to continue in
[Fix Hub](/en/latest/ExtNsT3AA/FeatureGuide/FixHub/Index).

License **scan page quota** applies: each page scanned in the run counts
against **Pages remaining**. See [Dashboard](/en/latest/ExtNsT3AA/FeatureGuide/Dashboard/Index) for how
quota works.

## Scanner vs other Scanner-tab tools

| Area | Role |
| --- | --- |
| **Scanner** | Interactive WCAG-oriented HTML check. Primary button: **Run Accessibility Check**. This is the main scan engine. |
| **Lighthouse** | Calls Google PageSpeed Insights for **one public URL**. Separate tool; needs a PageSpeed API key. See [Lighthouse](/en/latest/ExtNsT3AA/FeatureGuide/Scans/Lighthouse/Index). |
| **Bulk Scans** | **Queue / schedule** for repeated **Scanner** runs — not a third scan engine. See [Bulk Scans](/en/latest/ExtNsT3AA/FeatureGuide/Scans/BulkScans/Index). |

## Common controls

* **Selected page** — from the page tree
* **Depth** — this page only, 1–3 levels, or infinite
* **Scan page quota** — pages scanned / remaining / license limit
* Optional: add the current scope to the Bulk Scans queue

## After a scan

* **Scanner** findings appear on the **Fix Hub** board for the same scope (not Lighthouse)
* Dashboard tiles update from completed results
* Re-run after publishing fixes to verify improvements

Detailed guides:

## Important notes

* Scanner needs a valid T3AA license for accessibility scans; it does **not**
  need an AI provider.
* For licensed remote audits, the site URL must be a **publicly reachable**
  absolute URL (for example `https://example.com/`). Relative bases such as
  `/finance/` can break URL building.
* **Lighthouse** always needs a Google PageSpeed API key and a URL Google can
  reach (`.ddev.site` / `localhost` will not work).
* Bulk Scans depends on Scheduler configuration for automated processing.

## Scanner areas

<CardGroup cols={2}>
  <Card title="Scanner" icon="scan-search" href="/en/latest/ExtNsT3AA/FeatureGuide/Scans/Scanner/Index" />
  <Card title="Bulk Scans" icon="layers" href="/en/latest/ExtNsT3AA/FeatureGuide/Scans/BulkScans/Index" />
  <Card title="Lighthouse" icon="gauge" href="/en/latest/ExtNsT3AA/FeatureGuide/Scans/Lighthouse/Index" />
</CardGroup>
