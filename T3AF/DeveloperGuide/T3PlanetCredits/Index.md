---
title: "T3Planet Credits (v1.1+)"
description: "Developer reference for T3Planet Credits integration."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "T3AF"
  - "T3Planet Credits (v1.1+)"
sidebarTitle: "T3Planet Credits"
---

When **T3Planet Credits** mode is active, `AiServiceInterface` routes
`complete()`, `stream()`, and `embed()` through the T3Planet composer API
(`Charge` / `Stream` / `Embed`). Billing is **token-based on the server**
— there are no fixed credits per `feature_key` in `Features.php`.

## Credit mode changes (streaming)

The following applies when credits mode is **on** (see [T3Planet Credits](/T3AF/T3PlanetCredits/Index) for activation):

- **`POST /API/AI/Charge.php`** — `AiServiceInterface::complete()` returns `AiResponse` plus `CreditsUsage`.
- **`POST /API/AI/Stream.php`** — `AiServiceInterface::stream()` returns incremental `string` chunks; read `StreamSummary` via `getReturn()`.
- **`POST /API/AI/Embed.php`** — `AiServiceInterface::embed()` returns `EmbeddingResponse` plus `CreditsUsage`.
- **`POST /API/AI/Abort.php`** — called automatically when a stream is cancelled or ends without settlement (see [Abort on cancel](#abort-on-cancel)).

**Streaming** uses the same JSON body as Charge (`domain`, `request_uuid`, `feature_key`, `meta_json`, optional top-level `extension_key`). The server emits **normalized SSE** (not raw OpenAI): `token` deltas, optional `ping`, mandatory `usage` settlement, optional `done`. Debit runs **after** the stream ends from real token usage (post-settle), like Charge.

When credits mode is **off**, `stream()` uses local adapters unchanged (generator return is `void`).

## Token billing model

- The server debits **after** upstream AI using actual token usage:
  `credits = max(1, ceil(total_tokens / tokens_per_credit))`.
- **Charge / Stream:** `total_tokens = tokens_input + tokens_output`.
- **Embed:** `total_tokens = tokens_input`.
- Default **1 credit = 1000 tokens** (overridable server-side via
  `tokens_per_credit` in the API `pricing` object).

Do **not** hardcode per-feature credit costs in child extensions. Use
[Pre-submit estimate (child extensions)](#pre-submit-estimate-child-extensions) before submit and read
`CreditsUsage` after the call for the **actual** debit.

## Pre-submit estimate (child extensions)

Before calling `complete()`, `stream()`, or `embed()`, call **Estimate.php** with the
same `feature_key` and `meta_json` you will send to Charge/Stream/Embed. Use
`endpoint` `charge` for completion and streaming; `embed` for embeddings. The
response `estimated_credits` is approximate (shown as “≈ X credits”), not
guaranteed.

Inject the public service:

```php
use NITSAN\NsT3AF\Api\AiOptions;
use NITSAN\NsT3AF\Api\AiServiceInterface;
use NITSAN\NsT3AF\Credits\Exception\CreditsApiException;
use NITSAN\NsT3AF\Credits\Service\CreditModeResolver;
use NITSAN\NsT3AF\Credits\Service\CreditsEstimateService;

final class SeoGenerator
{
    public function __construct(
        private readonly AiServiceInterface $ai,
        private readonly CreditModeResolver $creditMode,
        private readonly CreditsEstimateService $creditsEstimate,
    ) {
    }

    public function generateMetaDescription(string $input): string
    {
        $options = new AiOptions(
            extensionKey: 'ns_t3ai',
            featureKey: 'seo.meta_description',
            featureLabel: 'SEO Meta Description',
            requestSource: 'backend_module',
        );

        if ($this->creditMode->isActive()) {
            try {
                $estimate = $this->creditsEstimate->estimate(
                    'seo.meta_description',
                    ['prompt' => $input],
                    'charge',
                );
                // Show $estimate->label() in UI, e.g. "≈ 1 credits"
            } catch (CreditsApiException $e) {
                // Optional: surface insufficient balance (402) before submit
            }
        }

        $response = $this->ai->complete($input, $options);

        if ($response->credits !== null) {
            // Actual debit: $response->credits->charged
            // Tokens: $response->credits->tokensTotal, tokensInput, tokensOutput
        }

        return $response->content;
    }
}
```

**Estimate request shape** (handled by `CreditsEstimateService`):

- `feature_key` — extension-local key in `AiOptions`; normalized to composer catalog keys before the API call.
- `meta_json` — must include `prompt` (and any fields your feature sends).
- `endpoint` — `charge` (default) or `embed`.

## Feature key mapping (all extensions)

Child extensions keep their own telemetry keys in `AiOptions::featureKey` (for example
`seo.meta_description` or `translation.openai`). In credits mode,
`CreditsFeatureKeyMapper` maps them to composer `ns_ai_feature_cost.feature_key` values
(`seo_meta_description`, `content_translation`, …) immediately before Charge / Stream / Embed.

The original caller key is copied to `meta_json.client_feature_key` for cross-extension analytics.

Register additional aliases in your extension `ext_localconf.php`:

```php
$GLOBALS['TYPO3_CONF_VARS']['EXTCONF']['ns_t3af']['creditsFeatureKeyAliases']['my_extension'] = [
    'my.custom.action' => 'content_generation',
];
```

Catalog constants live in `CreditsFeatureKeyCatalog`. Stream requests always bill as `stream`;
embed requests as `embedding`.

## Streaming (Stream.php)

Inject `AiServiceInterface` only — routing is handled by `T3PlanetCreditAiService` and
`ProxyAiExecutor`.

```php
use NITSAN\NsT3AF\Api\AiOptions;
use NITSAN\NsT3AF\Api\AiServiceInterface;
use NITSAN\NsT3AF\Api\StreamSummary;
use Symfony\Component\Uid\Uuid;

final class StreamingSeoTitle
{
    public function __construct(
        private readonly AiServiceInterface $ai,
    ) {
    }

    public function generate(string $prompt): string
    {
        $options = new AiOptions(
            extensionKey: 'ns_t3ai',
            featureKey: 'seo_page_title',
            featureLabel: 'SEO page title',
            requestSource: 'backend_module',
            temperature: 0.7,
            maxTokens: 500,
            requestUuid: Uuid::v4()->toRfc4122(),
        );

        $stream = $this->ai->stream($prompt, $options);
        $assembled = '';

        foreach ($stream as $delta) {
            $assembled .= $delta;
            // Update UI with incremental $delta (not cumulative).
        }

        $summary = $stream->getReturn();
        if ($summary instanceof StreamSummary) {
            $fullText = $summary->content !== '' ? $summary->content : $assembled;
            $usage = $summary->credits;
            // $summary->raw contains license_key_selection, charged, pricing, …
            return $fullText;
        }

        return $assembled;
    }
}
```

## SSE events (server → client)

- **`token`** — Append `data.delta` to the UI buffer (incremental, not cumulative).
- **`ping`** — Ignore (keepalive).
- **`usage`** — Mandatory settlement; builds `StreamSummary` and `CreditsUsage`.
- **`done`** — Optional; the stream may end after `usage` only.

If any `token` was received but the connection ends without `usage`, the client throws
`CreditsApiException` — never treat that as success.

Pre-stream errors (JSON, not SSE) use the same codes as Charge (402 insufficient credits,
409 `stream_in_progress`, 422 `feature_unknown`, etc.).

## Abort on cancel

When the user cancels, closes the tab, or the PHP request aborts (`connection_aborted()`),
`ProxyAiExecutor` stops reading SSE and calls `POST /API/AI/Abort.php` with the same
`request_uuid` (within a few seconds). The server returns proportional `cost_units` /
`credits` for partial output; the client may store a receipt row for the dashboard.

Call **Abort** explicitly only if you implement custom cancel UX outside `AiServiceInterface`.

## Idempotency

- Reuse the same `AiOptions::$requestUuid` on network retry after failure.
- After a completed stream, the server may replay one `token` (full content) + `usage` — no second charge.
- **409 `stream_in_progress`:** another stream with the same UUID is still open on the server. The client throws `CreditsApiException` (no auto-retry). Wait for the first stream to finish and retry the same UUID, or use a **new** UUID for a parallel request.

Do **not** send embed-only `inputs[]` in `meta_json` for Stream.

## Caller attribution (Charge / Stream / Embed / Estimate)

Always set `extensionKey` on `AiOptions` (e.g. `ns_news_comments`). In credits
mode, `CreditsMetaJsonBuilder` adds these fields to `meta_json` (and duplicates
`extension_key` at the top level of the API body for forward-compatible servers):

- `extension_key` — TYPO3 extension that initiated the call (not the license product).
- `feature_label`, `request_source`, `content_entity_type`, `content_entity_uid` when set.

For manual estimates, pass the same `AiOptions` as the 4th argument to
`CreditsEstimateService::estimate()` or call
`CreditsMetaJsonBuilder::withAttribution($meta, $options)`.

Until the license server persists `caller_extension_key`, the usage UI may still show
`extension_key` from `ns_product_license` (the product tied to `license_key_used`).

## Backend module JavaScript (optional)

```javascript
import { estimateCredits } from '@nitsan/nst3af/credits-mode.js';

const result = await estimateCredits('seo.meta_description', { prompt: text }, 'charge');
if (result?.estimate_label) {
  // e.g. "≈ 1 credits"
}
```

Requires TYPO3 backend AJAX route `nst3af_credits_estimate` and an active
credits session.

## After Charge / Stream / Embed

Read `AiResponse::$credits`, `EmbeddingResponse::$credits`, or
`StreamSummary::$credits` (`CreditsUsage`):

- `charged` — actual credits debited (`charged.amount` from API).
- `tokensTotal`, `tokensInput`, `tokensOutput` — from the API response.
- `pricing` — shared `pricing` object when present.

Display copy using `CreditsPricing::footnote()` when you need a static hint
(e.g. “1 credit ≈ 1,000 tokens (min 1 credit per request)”).

## Features catalog

`Features.php` lists `feature_key`, `label`, `default_model`,
`default_backend`, `sort` — **not** fixed `cost` fields. Use it for
routing and UI labels only.

## Purchase / checkout

Product checkout URLs come from `Products.php` with `redirect_to` set to
your TYPO3 backend return URL. Use `checkout_url` **as returned** — do not
append extra Pabbly query parameters client-side. The client rewrites Pabbly
custom fields named `cf_credittoken*` to the install **Bearer token** (from
`RuntimeSettingsService::getTokenPlain()`), not the license key.

Checkout opens in a TYPO3 backend modal iframe. The host must allow embedding
(`frame-ancestors` / CSP) and its checkout API (e.g. `/api/user/checksteps`)
must accept requests from the embedded checkout page. A **403** on that API is
returned by **t3planet.shop**, not TYPO3 — fix on the shop/API side or use
**Open in new tab** in the modal until embedding is supported.
`Configuration/ContentSecurityPolicies.php` extends backend `frame-src` and
`connect-src` for T3Planet/Pabbly hosts.

## CLI, scheduler, and `domain_mismatch`

Every Charge / Stream / Embed body includes `domain`. The license server only
accepts hostnames registered for that install. Backend HTTP requests use
`HTTP_HOST` (unchanged). **CLI and scheduler** contexts have no web request; without
a stored hostname the client previously fell back to `localhost` and the API
returned `domain_mismatch`.

`CreditsDomainResolver` (since v1.1+) resolves hostname in this order when
`HTTP_HOST` is empty:

1. `credits_domain` in `tx_nst3af_runtime_setting` (set at token activation
   and on the first backend request with a real host)
1. `$GLOBALS['TYPO3_CONF_VARS']['SYS']['reverseProxyBaseUrl']`
1. First site configuration with an absolute `base` URL (`https://host/`)
1. `DDEV_PRIMARY_URL` in DDEV containers
1. Extension Configuration `t3planetCreditsDomain` (optional override)

**After upgrading:** open any backend module once (or re-activate Credits) so
`credits_domain` is persisted, or set `base: 'https://your-production-host/'`
in site config. Child extensions (t3cs, t3as, …) do not pass `domain` manually —
inject `AiServiceInterface` and call `embed()` / `complete()` as in the backend.

## Further reading

- [T3Planet Credits](/T3AF/T3PlanetCredits/Index) — product overview
- [Privacy — T3Planet Credits](/T3AF/Privacy/Index) — data sent when credits mode is on
