---
title: "Bulk Scans"
description: "**Bulk Scans** (under **Scanner → Bulk Scans**) manages a **queue of pages** for repeated **Scanner** runs."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AA"
sidebarTitle: "Bulk Scans"
---

**Bulk Scans** (under **Scanner → Bulk Scans**) manages a **queue of pages**
for repeated **Scanner** runs.

It is **not** a separate scan engine. The engine that runs is still the
**Scanner**. Bulk Scans only decides *which pages* are queued and lets a TYPO3
**Scheduler** task process them on a schedule.

## How to use it

1. Open **AI Accessibility**.
2. Select a page / site root in the page tree.
3. Open **Scanner → Bulk Scans**.
4. Check **Scan page quota** (same license quota as interactive Scanner).
5. Set **Depth**, then add pages with **Add all in scope to queue**,
   **Add selected to Queue**, or per-row **Add to Queue**.
6. Confirm pages show as **Pending** in the **Bulk Scans queue**.
7. Create / enable a **T3AA Bulk Scans** (or **T3AA Monitor Scan**) task under
   **Admin Tools → Scheduler**.
8. After the task runs, review findings in [Fix Hub](/en/latest/ExtNsT3AA/FeatureGuide/FixHub/Index)
   and the [Dashboard](/en/latest/ExtNsT3AA/FeatureGuide/Dashboard/Index).

## Scan page quota

Same license counters as Scanner:

* **Pages scanned** / **Pages remaining** / **Page limit**

Each queued page that is processed counts against the quota. Check remaining
pages before adding a large scope.

## Queue and scope

* **Depth** — this page only, 1–3 levels, or infinite
* **Pages in this scope** — scannable pages under the selected root + depth
* **Bulk Scans queue** — Pending / OK / Error, last scan time, remove actions

You can also tick **Also add this scope to the Bulk Scans queue** when running
an interactive Scanner pass.

## CLI (integrators)

```bash
vendor/bin/typo3 nst3aa:monitor:run
```

## Important notes

* Without Scheduler (or CLI), pages stay **Pending**.
* Bulk Scans does not replace a one-off interactive
  [Scanner](/en/latest/ExtNsT3AA/FeatureGuide/Scans/Scanner/Index) run.
* License quota limits how many pages you can include.
