---
title: "Data Processing Agreement (DPA) & General Data Protection Regulation (GDPR)"
description: "T3AA GDPR-related questions for accessibility features and technical data-management capabilities."
keywords:
  - "TYPO3"
  - "T3AA"
  - "DPA"
  - "GDPR"
  - "Accessibility"
sidebarTitle: "DPA & GDPR"
---

This page describes GDPR-related questions about accessibility features
(frontend widget, alt text, voiceover, PageSpeed, RTE audit) and the
**technical data-management capabilities** in T3AA.

## Product controls

- Do not place the frontend accessibility widget if browser storage or
  Accesstive third-party requests must be avoided. See
  [Accessibility Widgets](/en/latest/ExtNsT3AA/AccessibilityWidgets/Index#ns-t3aa-accessibility-widgets).
- Alt text: Vision AI via T3AF, and/or **alttext.ai** if that provider is
  configured. See [AI FileMeta](/en/latest/ExtNsT3AA/AIFilemeta/Index).
- Voiceover: **OpenAI** TTS and/or **ElevenLabs**. Files are stored in TYPO3
  FAL with **no automatic expiry**. See
  [T3AA Voiceover](/en/latest/ExtNsT3AA/T3AAVoiceover/Index) and
  [AI Audio Generator](/en/latest/ExtNsT3AA/AIAudioGenerator/Index).
- PageSpeed: **Google PageSpeed Insights API** when a key is set (page URL
  sent from the backend). See
  [Speed Core Web Vitals](/en/latest/ExtNsT3AA/SpeedCoreWebVitals/Index).
- LLM text features (simplify, and similar) follow T3AF **BYOK vs Credits**.
  See [Simplified Text](/en/latest/ExtNsT3AA/SimplifiedText/Index) and
  [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index).
- ElevenLabs is **own-keys only**.

## Data Processing Agreement (DPA) Considerations

Administrators should consider and document:

- Browser local storage for widget preferences
- Generated audio in FAL without TTL — plan deletion if required
- Backend PageSpeed / alttext.ai / TTS vendors
- Cookie/storage notices for the widget
- Provider DPA / no model training for any LLM or TTS vendor used

## Data Processing Agreement (DPA) Questions

**Question:** Does T3AA collect frontend visitor search or conversation logs?

**Answer:** **No.** T3AA does not write visitor query/conversation transcript tables.

**Question:** Frontend widget — what is stored?

**Answer:** Accessibility preferences (contrast, profiles, fonts, and similar) are typically kept in the visitor’s **browser local storage**. That is not a TYPO3 database log.

See [Accessibility Widgets](/en/latest/ExtNsT3AA/AccessibilityWidgets/Index#ns-t3aa-accessibility-widgets).

**Question:** Voiceover files?

**Answer:** Generated audio is stored in fileadmin / FAL (`pages.voiceover` flag; `sys_file_metadata.t3aa_audio_source_identifier`). **No built-in expiry.** Delete files operationally if required.

See [T3AA Voiceover](/en/latest/ExtNsT3AA/T3AAVoiceover/Index).

**Question:** What else does T3AA store on the server?

**Answer:** Ops / editor data, for example:

| Area | Examples |
| --- | --- |
| File metadata | Alt text / title / description on `sys_file_metadata`; `t3aa_image_source_identifier` |
| Bulk metadata queue | `tx_nst3aa_domain_model_bulkmeta` |
| Page flag | `pages.voiceover` |
| Activity | AI Foundation logs for T3AA operations |

See [AI Usage & Logs](/en/latest/ExtNsT3AF/Configuration/AIUsageAndLogs/Index).

**Question:** PageSpeed?

**Answer:** When used, the **absolute page URL** is sent from the **backend** to `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`. Visitor IP and visitor queries are not part of that payload.

See [Speed Core Web Vitals](/en/latest/ExtNsT3AA/SpeedCoreWebVitals/Index).

**Question:** Alt text processors?

**Answer:**

- Vision via T3AF (BYOK or Credits)
- **alttext.ai** if that adapter/provider is configured (image data goes to that vendor)

See [AI FileMeta](/en/latest/ExtNsT3AA/AIFilemeta/Index).

**Question:** TTS processors?

**Answer:**

- **OpenAI** and/or **ElevenLabs** (own keys)
- Credits mode can route OpenAI TTS via T3Planet; ElevenLabs is not supported in Credits mode

See [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index).

**Question:** IP / cookies / FE users of website visitors?

**Answer:** T3AA **does not store** visitor IP, cookies, or frontend-user IDs as dedicated database fields for the widget. Widget preferences stay in the browser.

**Question:** MCP?

**Answer:** If AI Foundation MCP is enabled, T3AA tools can run accessibility and media operations through connected clients. That is backend/editor access, not public-visitor processing. Restrict MCP as an access-control topic.

See [MCP Server](/en/latest/ExtNsT3AF/Integrations/MCPServer/Index).

<Note>
This documentation describes technical data-management capabilities. It does not constitute legal advice.
</Note>
