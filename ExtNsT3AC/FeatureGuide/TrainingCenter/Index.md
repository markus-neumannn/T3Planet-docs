---
title: "Training Center"
description: "View the training queue items collected from all data sources and control training and cleanup."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Training Center"
sidebarTitle: "Training Center"
---

## Purpose


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmracqklk0e92qmhxeuqwubf8?utm_source=link" loading="lazy" title="T3AC Training Center Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
View the training queue (items collected from all data sources) and control training and cleanup.

## What you see

- **Summary counts**: Total items, Pending, Embedding (processing), Completed, Failed, and Tokens used.
- **All Sources**: List or summary of data sources and item counts.
- **Training Queue** table: Items with columns such as **Item**, **Status**, **Tokens**, **Created**, **Actions**.
- **Filters**: By data source, status (All Statuses), or search text.
- **Actions**: Select All, Delete, Re-queue (reset).

Queue item statuses:

- **Pending** – Waiting to be processed.
- **Processing / Embedding** – Currently being sent to the embeddings service.
- **Completed** – Successfully trained.
- **Failed** – Error during training.

## Actions

### Sync

Refreshes content from the data source into the queue (same as in the **Data Source** tab).

### Reset (Re-queue)

Puts a **failed** or **completed** item back to **Pending** so it will be processed again on the next training run.

### Delete

Removes selected queue items.

<Info>
Deleted items will not be trained again unless they are added again by a new sync.
</Info>

### Run training

Use the link to the **Scheduler** module and run the **T3AC Training** task for this site.

When the task runs, it:

- Processes all **Pending** queue items (generates embeddings).
- Runs cleanup of old completed/failed items according to the retention setting.

## Training behaviour (simple terms)

- Only items in status **Pending** are processed when training runs.
- **Processing** means: the text is sent to the configured embeddings service, and the result is stored for search/chatbot usage.
- After success, the item is marked **Completed**; on error, **Failed**.
- How often training runs depends on the Sync interval of your data sources and on the Scheduler actually being triggered (e.g. via cron).
