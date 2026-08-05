---
title: "AI Prompts"
description: "AI Prompts for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "AI Prompts"
---

## Purpose

Central **prompt templates** for T3AF and connected extensions. Same prompt quality for every user and every extension.

**Path:** T3AF → AI Prompts

## What is a prompt?

The instruction sent to the AI. Examples:

- “Write a meta description, max 155 characters”
- “Translate to German, formal Sie”

Central prompts mean **consistent quality** across your team.

## Manage prompts

1. Open AI Prompts
2. Select feature category
3. Edit template text
4. Save and test with one real request

Extensions can sync default prompts from T3AF.

## Writing good prompts

1. **Be specific** — length, format, language
2. **Set tone** — formal, friendly, technical
3. **Say what to avoid** — no emojis, no hype, no legal claims
4. **Use placeholders** — `&#123;title&#125;`, `&#123;content&#125;`, `&#123;language&#125;`

## Example template

```
Write a meta description for this page.
Language: {language}
Max: 155 characters.
Tone: professional.
Keyword: include naturally.
Title: {title}
Content: {content}
```

Pair prompts with [AI Context](/T3AF/AIContext/Index) for brand voice. Context handles who you are; prompts handle what to do.

## Reset to default

If results worsen after edits, use **Reset to default** in the UI. Then change one variable at a time and test again.

## When to customize prompts

- SEO team has strict meta description rules
- Legal requires disclaimers in generated text
- German formal (Sie) must appear in every output
- Extension default is too generic for your industry

## When to leave defaults

- Small team still learning AI features
- You have not yet filled [AI Context](/T3AF/AIContext/Index)
- Results are already good — do not over-edit

## Governance note

Prompt changes affect all users. Coordinate with [AI Permissions](/T3AF/GovernanceAndAccess/Index) before large template changes on production.
