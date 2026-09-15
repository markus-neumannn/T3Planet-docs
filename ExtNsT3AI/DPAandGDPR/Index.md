---
title: "Data Processing Agreement (DPA) & General Data Protection Regulation (GDPR)"
description: "T3AI GDPR-related questions for backend editorial AI and technical data-management capabilities."
keywords:
  - "TYPO3"
  - "T3AI"
  - "DPA"
  - "GDPR"
sidebarTitle: "DPA & GDPR"
---

T3AI provides the following information for GDPR-related questions about
backend editorial AI (SEO, translation, content generation, RTE commands,
image generation) and describes **technical data-management capabilities**.

## Product controls

- Disable unused feature groups (SEO, page, content, translation, media) so
  those prompts are never sent. See [T3AI Features](/en/latest/ExtNsT3AI/AISettings/Index).
- Choose the translation engine: AI Foundation provider, **DeepL**,
  **Google Translate**, Gemini, Claude, or Mistral. Each enabled vendor is a
  separate processor. See [Translation](/en/latest/ExtNsT3AI/Translation/Index).
- Disable unused image/stock features (DALL-E, MidJourney, Stability,
  Unsplash, Openverse, Pixabay, Pexels). See [Media](/en/latest/ExtNsT3AI/Media/Index).
- All LLM traffic goes through AI Foundation — same **BYOK vs Credits**
  choice as T3AF. See
  [T3Planet Credits](/en/latest/ExtNsT3AF/T3Planet-Credit-System/Index).

## Data Processing Agreement (DPA) Considerations

Administrators should consider and document:

- Editorial content and prompts sent to the configured AI / translation /
  image vendor
- Generated text and images stored as normal TYPO3 pages, content, and files
- Glossary, mass SEO queue, and bulk-translation queue (operations data)
- Logs via T3AF AI Logs and AI Usage
- Additional processors (DeepL, Google Translate, image APIs) if enabled
- Exception-solving payloads (stack traces can contain sensitive data)
- Provider DPA / no model training

## Data Processing Agreement (DPA) Questions

**Question:** Does T3AI process frontend visitor information?

**Answer:** **No.** Editors trigger T3AI in the backend. T3AI does not collect visitor IP addresses, cookies, or frontend-user accounts.

**Question:** What data does T3AI send to the AI provider?

**Answer:** Editorial prompts and selected content, for example:

- Page text, SEO fields, translation jobs
- RTE selections (rewrite / assist / translate in the editor)
- Image prompts, and image bytes/URLs when vision or image-generation
  features are used
- Published page content when **content analysis** is run (the rendered page
  as CMS content, not visitor identifiers)

**Question:** Where are results stored?

**Answer:** In the TYPO3 records the editor saves (pages, content elements, news/blog, FAL files). That is CMS content, not a usage log.

**Question:** Does T3AI store full prompts and responses in its own tables?

**Answer:** **No.** T3AI does not keep a local prompt/response transcript table. Operational logging goes to AI Foundation (see Logging). Prompt templates are stored in AI Foundation (`tx_nst3af_ai_prompt`).

See [Prompts](/en/latest/ExtNsT3AI/Prompts/Index) and
[AI Usage & Logs](/en/latest/ExtNsT3AF/Configuration/AIUsageAndLogs/Index).

**Question:** Extra processors besides the LLM?

**Answer:**

| Feature | Possible processors (only if enabled) |
| --- | --- |
| Translation | DeepL, Google Translate, Gemini, Claude, Mistral, or the T3AF default provider |
| AI images | OpenAI DALL-E, MidJourney, Stability AI |
| Stock search | Unsplash, Openverse, Pixabay, Pexels |

**Question:** Glossary?

**Answer:**

- AI glossary term pairs: `tx_nst3ai_domain_model_glossary` (local TYPO3)
- DeepL official glossary IDs if that integration is on (those IDs are sent
  to DeepL with the translation job)

See [Translation](/en/latest/ExtNsT3AI/Translation/Index).

**Question:** Bulk translation queue?

**Answer:** `tx_nst3ai_domain_model_bulktranslation` stores page IDs, status, error message, and timestamps. This is an operations queue.

**Question:** Mass SEO queue?

**Answer:** `tx_nst3ai_domain_model_bulkseo` stores queued pages for mass SEO. Schema markup can be stored in `tx_nst3ai_domain_model_schema` / page field `tx_nst3ai_schema_content` when that feature is used.

See [Mass SEO](/en/latest/ExtNsT3AI/MassSEO/Index).

**Question:** Can logging be reduced?

**Answer:** **Yes.** Privacy level **reduced** = counters and identifiers only; no fingerprint and no raw metadata. **none** = no AI Usage row.

A user may only tighten logging (UserTSconfig), never loosen a stricter
provider setting. This does not change what is sent to the AI provider.

See [AI Providers](/en/latest/ExtNsT3AF/Configuration/AIProviders/Index)
(privacy level).

**Question:** IP / cookies / FE users of website visitors?

**Answer:** **Not collected by T3AI** for public visitors. The backend user is attributed on AI Logs when an editor runs a job.

**Question:** MCP?

**Answer:** If AI Foundation MCP is enabled, T3AI tools can generate or update editorial content through connected clients. That is backend/editor access, not public-visitor processing. Restrict MCP as an access-control topic.

See [MCP Server](/en/latest/ExtNsT3AF/Integrations/MCPServer/Index).

<Note>
This documentation describes technical data-management capabilities. It does not constitute legal advice.
</Note>
