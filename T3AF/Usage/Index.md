---
title: "Usage"
description: "Practical usage of T3AF for admins, editors, and stakeholders."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "Usage"
sidebarTitle: "Usage"
---

This guide focuses on practical operation for editors, administrators, and
non-technical stakeholders.

## For administrators

Daily responsibilities:

- Keep provider API keys valid in **T3AF → AI Providers**.
- Maintain the default provider and model selections.
- Monitor OpenAI usage trends (requires `openai_admin_api_key` when used).
- Keep credentials and access permissions under control.

### Admin checklist

1. Confirm a default provider is enabled in **AI Providers**.
2. Run **Test connection** on critical provider rows.
3. Test extension-dependent AI features in your connected modules.
4. Review usage statistics regularly (cost/rate-control).

## For editors

Editors usually do not configure providers directly. They interact with
features built by other extensions that depend on T3AF.

When AI features fail in a backend module:

- Retry once.
- Capture exact error text.
- Inform administrator with module/page context.

## For non-technical stakeholders

T3AF helps organizations by:

- Reducing duplicated AI integration work across extensions.
- Centralizing provider and model governance.
- Improving consistency of AI capabilities across teams.

## What to expect operationally

- Some providers have rate limits and temporary outages.
- Model behavior can differ between providers and versions.
- Statistics data may be cached and not always real-time.

## Known boundaries

- No standalone frontend plugin is provided by this extension.
- This package is a service layer; UI features come from dependent extensions.
