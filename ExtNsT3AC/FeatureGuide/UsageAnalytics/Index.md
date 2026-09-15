---
title: "Usage Analytics"
description: "View recent search and chatbot activity if the corresponding extensions are installed."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Usage Analytics"
sidebarTitle: "Usage Analytics"
---

## Purpose

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmracyax70em8qmhxmigmckrv?utm_source=link&embed_v=2&utm_source=embed" loading="lazy" title="T3AC Usage Analytics Demo" allow="clipboard-write; fullscreen" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

View recent search and chatbot activity (if the corresponding extensions are installed).

## What you see

### Chatbot

Recent conversations: e.g. IP, first input/output, message count, time.

## Filtering and export

- **Search queries or responses** – Search within the logs.
- **All Modules** / **All Languages** – Filter by module and language.
- **Export** – Download analytics data.

## Deletion / cleanup

You can delete individual entries (for privacy or cleanup):

- Deleting **search** entries affects search history.
- Deleting **chatbot** entries can be per IP (all conversations from that IP).

Enable **Save chatbot history** in **Chatbot → Settings** so conversations appear in this log. Enable **Save search history** in **T3AS → Search → Settings** so search queries and answers appear here.

To delete old usage history automatically, use the `t3af:history:cleanup` scheduler task. Set the **days** argument for the retention period (default `90`). See **Scheduler** in [Data Source](/en/latest/ExtNsT3AC/FeatureGuide/DataSource/Index).

When no data has been recorded yet, the message shown is: *“No interaction logs yet. Search and chatbot history will appear here when the modules are loaded and users interact.”*
