---
title: "Extension Integration"
description: "Extension Integration for EXT:ns_t3af (T3AF)."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "ns_t3af"
sidebarTitle: "Extension Integration"
---

Use `AiServiceInterface` when your TYPO3 extension needs AI completions, streaming, or embeddings through T3AF. Do not call provider adapters, provider repositories, or vendor SDKs directly from feature code.

## Purpose

T3AF acts as the shared AI gateway for child extensions such as AI Assistant, AI Search, AI Chatbot, AI Accessibility, and custom agency extensions. The child extension prepares the prompt, context, and feature metadata. T3AF resolves the provider, executes the request, and records usage attribution.

## Request lifecycle

1. Your extension builds the prompt and context.
2. Your service calls `AiServiceInterface`.
3. T3AF resolves the requested provider or the default provider.
4. The matching adapter performs the completion, stream, or embedding request.
5. Request metadata is logged for usage, analytics, and troubleshooting.

## Dependency injection

Inject the interface into your own service.

```
use NITSAN\NsT3AF\Api\AiServiceInterface;

final class MyAiService
{
    public function __construct(
        private readonly AiServiceInterface $aiService,
    ) {}
}
```

## Minimal working example

Pass `AiOptions` with stable feature metadata. This makes logs and usage analytics useful.

```
use NITSAN\NsT3AF\Api\AiOptions;
use NITSAN\NsT3AF\Api\AiServiceInterface;

final class SeoDescriptionGenerator
{
    public function __construct(
        private readonly AiServiceInterface $aiService,
    ) {}

    public function generate(string $prompt, int $pageUid): string
    {
        $response = $this->aiService->complete(
            $prompt,
            new AiOptions(
                extensionKey: 'my_extension',
                featureKey: 'seo.meta_description',
                featureLabel: 'SEO meta description',
                requestSource: 'backend_module',
                contentEntityType: 'pages',
                contentEntityUid: $pageUid,
            ),
        );

        return $response->content;
    }
}
```

## What to put in AiOptions

**`extensionKey`**

TYPO3 extension key that initiated the request.

**`featureKey`**

Stable machine key for the feature. Keep it unchanged across releases.

**`featureLabel`**

Human-readable label for logs and dashboards.

**`requestSource`**

Source of the request, such as `backend_module`, `scheduler`, or `cli`.

**`contentEntityType` and `contentEntityUid`**

Optional record context used for drilldown and troubleshooting.

## Best practices

- Use `AiServiceInterface` as the only runtime AI integration surface.
- Keep `featureKey` stable so analytics history remains meaningful.
- Treat AI output as untrusted content before rendering or saving it.
- Do not log API keys, provider secrets, or sensitive prompt payloads.
- Handle provider failures and empty responses in your feature code.
- For CLI or Scheduler usage, configure an absolute TYPO3 site base URL when required by your environment.

## Troubleshooting

**No provider is resolved**

- Confirm a provider is connected in T3AF > AI Providers.
- Confirm your feature-level provider override, if used, points to an enabled provider.

**Request is missing in logs**

- Confirm `extensionKey` and `featureKey` are set in `AiOptions`.
- Check [AI Usage & Logs](/T3AF/Configuration/AIUsageAndLogs/Index).

## Related documentation

- [Feature Provider Overrides](/T3AF/DeveloperGuide/FeatureProviderOverrides/Index)
- [Custom AI Providers](/T3AF/DeveloperGuide/CustomProviders/Index)
- [AI Providers](/T3AF/Configuration/AIProviders/Index)
- [AI Usage & Logs](/T3AF/Configuration/AIUsageAndLogs/Index)
