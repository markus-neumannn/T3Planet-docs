---
title: "Data Processing Agreement (DPA) & General Data Protection Regulation (GDPR)"
description: "T3AC controls for chatbot history storage, retention, and DPA/GDPR considerations."
keywords:
  - "TYPO3"
  - "T3AC"
  - "DPA"
  - "GDPR"
sidebarTitle: "DPA & GDPR"
---

T3AC provides data-management capabilities for stored chatbot usage history and **Data Processing Agreement (DPA)** and **General Data Protection Regulation (GDPR)** requirements.

## Save Chatbot History

T3AC allows administrators to control whether visitor chatbot history is stored.

The **Save chatbot history** option is available under the AI Chatbot configuration.
For this setting, see [Save chatbot history](/ExtNsT3AC/FeatureGuide/Chatbot/Index#t3ac-save-chatbot-history).

Follow these steps in the backend (see the demo below):

1. Open **AI Chatbot** in the TYPO3 backend.
2. Click the **Chatbot** tab.
3. In **Settings**, enable or disable **Save chatbot history**.

<div className="t3-embed"><iframe src="https://app.supademo.com/embed/cmragm93i0mj0qmhx6fir2bke?embed_v=2&utm_source=embed" loading="lazy" title="T3AC Chatbot settings — Save chatbot history" allow="clipboard-write" frameBorder="0" webkitallowfullscreen="true" mozallowfullscreen="true" allowfullscreen></iframe></div>

When enabled, T3AC can store chatbot-related history such as visitor conversations and generated answers.

When disabled:

- New chatbot conversations and answers are not stored as chatbot history.
- Past-chat history is not retained for new conversations.
- Thumbs-up/down feedback is hidden.
- No new chatbot history is retained by T3AC.

This option can be used when your privacy requirements do not allow visitor chatbot history to be stored.

<Important>
Disabling chatbot history affects newly generated chatbot and feedback data. Existing records are not automatically removed when this option is disabled. Use the history cleanup scheduler to remove previously stored records. See [History cleanup](/ExtNsT3AS/Configuration/Index#t3as-history-cleanup).
</Important>

Chatbot usage history can be removed automatically with `t3af:history:cleanup`. The default retention period is **90** days and is configurable.

For the Scheduler cleanup task, see [History cleanup](/ExtNsT3AS/Configuration/Index#t3as-history-cleanup).

## Data Processing Agreement (DPA) Considerations

Administrators should consider:

- Visitor chatbot data storage
- Data retention
- Data deletion
- Data Processing Agreements (DPA)
- General Data Protection Regulation (GDPR) and applicable data-protection requirements

<Note>
This documentation describes technical data-management capabilities. It does not constitute legal advice.
</Note>
