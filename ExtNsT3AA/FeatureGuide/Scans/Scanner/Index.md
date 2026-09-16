---
title: "Scanner"
description: "The **Scanner** is the interactive accessibility checker under **AI Accessibility → Scanner → Scanner**."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AA"
sidebarTitle: "Scanner"
---

The **Scanner** is the interactive accessibility checker under
**AI Accessibility → Scanner → Scanner**.

It checks the HTML of pages in your selected **scope** (page + depth), then
lists findings you can open in [Fix Hub](/en/latest/ExtNsT3AA/FeatureGuide/FixHub/Index).

## How to run a scan

1. Open **AI Accessibility**.
2. Select a page in the page tree.
3. Open the **Scanner** tab → **Scanner** sub-tab.
4. Confirm the site URL shown for the selected page.
5. Choose **Depth** and **Device**.
6. Optionally tick **Also add this scope to the Bulk Scans queue**.
7. Click **Run Accessibility Check** and wait for results.
8. Review summary cards and the issue list.
9. Click **Open issues to work on** or an issue row to continue in Fix Hub.

## Scan page quota

* **Pages scanned** / **Pages remaining** / **Page limit**

Each page included in the run counts against your license quota when the scan
runs. One click can cover many pages if depth is deep — check remaining pages
first. Details: [Dashboard](/en/latest/ExtNsT3AA/FeatureGuide/Dashboard/Index).

## What to scan

* **Site URL** — frontend base URL of the selected site
* **Selected page** — from the page tree
* **Depth** — this page only, 1–3 levels, or infinite
* **Device** — Desktop, Mobile, or Both (where offered)
* **Run Accessibility Check** — starts the run

Below the controls:

* **N pages in scope** — how many pages will be included
* When depth includes multiple pages, findings are merged into one report for
  the selected root

## Results

After a successful run:

* Summary cards: Critical, Serious, Moderate, Minor, Needs review
* **Accessibility Health Score** for the scanned scope
* WCAG-level breakdown (A / AA / AAA / Best Practice) — what the Scanner
  recorded, not a legal conformance claim
* **All issues found** table — click a row to open Fix Hub

Footer guidance in the product:

   **A scan reports; Fix Hub is where work happens.**

## Important notes

* The Scanner needs **no AI provider and no API key**.
* A valid T3AA license / registered domain is required.
* **Only a public URL will work** for licensed remote audits. The site base
  must be an absolute, publicly reachable URL (for example
  `https://example.com/`). Relative bases such as `/finance/` can break
  URL building in CLI / scheduler.
* Google **Lighthouse** (separate sub-tab) cannot crawl `.ddev.site` /
  `localhost` — use a public staging URL there.
* If scanning is not authorized, the UI shows a clear license/domain message.
