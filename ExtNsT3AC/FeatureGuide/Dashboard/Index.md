---
title: "Dashboard"
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AC"
  - "Dashboard"
sidebarTitle: "Dashboard"
---

## Purpose


<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmraci4jy0dt1qmhxv2wo4p5p?utm_source=link" loading="lazy" title="T3AC Dashboard Demo" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>
The Dashboard gives an overview of your AI training pipeline for the current site.

## What you see

- Which AI/embedding model is in use (e.g. OpenAI, Gemini, Mistral, Custom).
- Status of the **Search** and **Chatbot** modules (if installed): active/inactive, AI engine, base model, embedding model.
- Status of your data sources and training (e.g. how many items are pending, completed, or failed).
- **Training Pipeline** section: data sources count, queue size, and a link to CLI reference.
- **Usage Analytics** summary (e.g. total interactions, search queries, chat sessions over the last 7 days).
- A link to the **Scheduler** to run or check the automatic training task.

## Scheduler link

From the Dashboard you can open the TYPO3 Scheduler and locate the automatic training task (typically named **T3AC Training** for this site). Use **Run All** or **Run Task Now** to process the training queue immediately.
