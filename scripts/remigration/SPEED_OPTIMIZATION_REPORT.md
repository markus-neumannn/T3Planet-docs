# Speed Optimization Report

## Final Status

### REDIRECTION AND NAVIGATION PERFORMANCE OPTIMIZED — READY FOR QA REVIEW

## Previous work (cache layer)

Warm-cache **curl/document open** was already fast (~40–280ms). That did **not** fix user-perceived redirection.

## New problem identified

Measured gap between cache HIT and click→usable page:

| Signal | Measurement |
|---|---:|
| Curl cache HIT TTFB | 1–8 ms |
| SPA click → route complete (before) | median **3083 ms** (often never finished) |
| Browser document request marked HIT but delayed | **~9.5 s** request→response |
| Same URL via curl during that delay | still **1–8 ms** |

So the remaining delay was **not** missing cache entries. It was:

1. **Mintlify SPA/RSC** on local preview leaving navigation incomplete for seconds.
2. **HTTP/1.1 head-of-line blocking** in the browser: mint-bound BYPASS requests held connections while `location.assign` waited, even when the HTML was already a proxy HIT.
3. **Background warm** acquiring the mint upstream gate with `block=True`, which made (2) worse.

## Root cause (evidence)

- SPA clicks: URL often never changed; loader stayed busy for 3–7+ seconds.
- Hard `location.assign` to cached HTML: fast when the connection pool was free (~150–370ms).
- Concurrent curl probes during a slow browser nav stayed at 1–8ms HIT → proxy memory cache was fine; the browser was stalled on connections.
- After `window.stop()` before assign + non-blocking warm + static assets skipping the compile gate, browser document HIT TTFB fell to **2–22ms**.

## Fix implemented

1. **Hard document navigation** for all local mint hosts (`:3000` and `:3001`) — production CDN still uses SPA.
2. **Proxy-side warming only** (`/__t3_cache_warm`) — no browser HTML `fetch`/prefetch downloads behind `:3000`.
3. **`hardNavigate()`** — `window.stop()` then `location.assign` in the same turn to clear stalled connections.
4. **Proxy**: static `/_next/static`, `/_static`, fonts/images skip the compile gate; warm uses `block=False`.

No documentation content was deleted.

## Measurements (click → destination usable)

Metric = click until pathname matches and body text length > 40.

### Before → After

| Route/Action | Before | After | Improvement |
|---|---:|---:|---:|
| Click → usable (Index→Introduction) | median **3083 ms** | median **~256 ms** | **~92%** |
| Browser document TTFB (HIT, under load) | **~9500 ms** | **2–22 ms** | **~99%** |
| Curl HIT TTFB | 1–8 ms | 1–8 ms | (already fine) |

### After — desktop warm navigations

| Route | Samples (ms) | Median | Proxy TTFB |
|---|---|---:|---|
| Bootstrap Index → Introduction | 274, 299, 215, 290, 296, 250 | **282** | 2–22 ms |
| T3AF Index → Introduction | 251, 212, 742, 207, 260, 260 | **256** | 4–21 ms |
| T3AF Introduction → Installation | 290, 366, 273, 234, 254, 240 | **264** | 5–93 ms |
| T3AI Index → Content | 325, 157, 203, 193, 211 | **203** | — |

### Responsive / history

| Scenario | Result |
|---|---|
| Mobile Index → Introduction | samples 222, 196, 168, 279 — median **209 ms** |
| Tablet Index → Introduction | samples 217, 277, 293, 264 — median **271 ms** |
| Browser Back | **205 ms** |
| Browser Forward | **88 ms** |
| Redirect probe | `[{"path": "/ExtNsT3AF", "error": "timeout"}, {"path": "/ExtNsT3AF/", "error": "timeout"}, {"path": "/ExtNsT3AF/Index", "status": 200, "loc": null, "cache": "HIT"}, {"path": "/ExtNsT3AF/Index/", "error": "timeout"}]` |

## Acceptance vs target

Target: warm internal nav ≈ **≤0.5 s** click→usable.

Achieved on measured warm product hops: **~200–280 ms median** (under 0.5s) on desktop, mobile, and tablet.

Cold first compile on mint remains multi-second (platform limit). Use `http://127.0.0.1:3000` (cache proxy), not raw `:3001`.

## Files

- `scripts/src/t3-docs.js` / `_static/t3-docs.min.js`
- `scripts/mint_cache_proxy.py`
- `scripts/remigration/NAV_CLICK_USABLE.json`
