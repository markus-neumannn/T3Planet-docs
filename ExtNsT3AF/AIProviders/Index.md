---
title: "AI Providers"
description: "AI Providers for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "AI Providers"
---

## Purpose

Connect TYPO3 to AI models. This is the **most important** T3AF screen. Without at least one working provider, no AI feature runs.

**Path:** T3AF → AI Providers

## Add a provider (step by step)

1. Click **Add provider**
2. Choose vendor (OpenAI, Anthropic, Gemini, Azure, Mistral, DeepSeek, xAI, custom, Ollama)
3. Paste API key (encrypted on save)
4. Select model
5. Click **Test connection**
6. Enable **Default** on exactly one provider

## Supported vendors

OpenAI, Anthropic (Claude), Google Gemini, Azure OpenAI, Mistral, DeepSeek, xAI, Custom OpenAI-compatible endpoints, and Ollama (local).

## Capabilities

Pick a model that supports what you need. **Test connection** validates your choice.

- **Chat** — Text generation
- **Streaming** — Live response display in the backend
- **Embeddings** — Search and similarity features
- **Vision** — Image analysis
- **Tool use** — MCP agent workflows

## Multiple providers — when and why

**Dev and live** — Two provider rows with different API keys per environment.

**Cost saving** — Cheap model as global default; premium model assigned in [AI Features](/ExtNsT3AF/AIFeatures/Index) for important tasks.

**EU hosting** — Mistral or Azure in an EU region for data residency requirements.

## Billing modes

**Your Own API Keys (BYOK)** — Pay the vendor directly. This is the default mode.

**T3Planet Credits** — Toggle in AI Providers, then click **Activate**. See [T3Planet Credits](/ExtNsT3AF/T3PlanetCredits/Index).

## Troubleshooting

**Test fails** — Check key, model ID, and firewall (outbound HTTPS must be allowed).

**Rate limit** — Wait or upgrade your vendor plan.

**Vision returns empty** — Use a vision-capable model (for example GPT-4o with vision).

**Module works but child extension fails** — Check [AI Features](/ExtNsT3AF/AIFeatures/Index) for per-task overrides.

## Security

- Rotate keys every 90 days
- Use one key per environment (dev, staging, live)
- Restrict access via [AI Permissions](/ExtNsT3AF/GovernanceAndAccess/Index)
- Never commit API keys to Git

## Where to get API keys

<Note>
- OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- Anthropic: [https://console.anthropic.com/](https://console.anthropic.com/)
- Google Gemini: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- Mistral: [https://console.mistral.ai/](https://console.mistral.ai/)
- Azure OpenAI: [https://portal.azure.com/](https://portal.azure.com/)
</Note>

More links: [Helpful Links](/ExtNsT3AF/HelpfulLinks/Index)
