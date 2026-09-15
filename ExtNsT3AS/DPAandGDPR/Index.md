---
title: "Data Processing Agreement (DPA) & General Data Protection Regulation (GDPR)"
description: "T3AS controls for search history storage, retention, and DPA/GDPR considerations."
keywords:
  - "TYPO3"
  - "T3AS"
  - "DPA"
  - "GDPR"
sidebarTitle: "DPA & GDPR"
---

T3AS provides controls that help administrators manage visitor search data and address **Data Processing Agreement (DPA)** and **General Data Protection Regulation (GDPR)** requirements.

## Save Search History

T3AS allows administrators to control whether visitor search history is stored.

The **Save search history** option is available under the AI Search configuration.
For this setting, see [Save search history](/en/latest/ExtNsT3AS/Configuration/Index#t3as-search-global-settings).

Follow these steps in the backend (see the demo below):

1. Open the **T3AS** module.
2. Click the **Search** tab.
3. In **Settings**, enable or disable **Save search history**.

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmrajjqug0tgfqmhx211jb110?embed_v=2&utm_source=embed" loading="lazy" title="T3AS Search settings — Save search history" allow="clipboard-write; fullscreen" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

When enabled, T3AS can store search-related history such as visitor queries and generated answers.

When disabled:

- New search queries and answers are not stored as search history.
- Recent-search suggestions are hidden.
- Thumbs-up/down feedback is hidden.
- No new search history is retained by T3AS.

This option can be used when your privacy requirements do not allow visitor search history to be stored.

<Important>
Disabling search history affects newly generated search and feedback data. Existing records are not automatically removed when this option is disabled. Use the history cleanup scheduler to remove previously stored records. See [History cleanup](/en/latest/ExtNsT3AS/Configuration/Index#t3as-history-cleanup).
</Important>

Existing search history can be removed using the TYPO3 Scheduler cleanup task. The task is configurable. The default retention period is **90** days. The command is `t3af:history:cleanup`.

For this task, see [History cleanup](/en/latest/ExtNsT3AS/Configuration/Index#t3as-history-cleanup).

## Data Processing Agreement (DPA) Considerations

Administrators should consider:

- Visitor search data storage
- Data retention periods
- Data deletion requirements
- Data Processing Agreements (DPA)
- General Data Protection Regulation (GDPR) and applicable data-protection requirements

<Note>
This documentation describes technical data-management capabilities. It does not constitute legal advice.
</Note>

## Data Processing Agreement (DPA) Questions

Dedicated documentation for common DPA questions can be provided or referenced when it is available.
