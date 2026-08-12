# Mintlify Documentation — Performance Optimization Report (Aug 2026)

**Date:** August 7, 2026  
**Scope:** Entire T3Planet Mintlify documentation  
**Hard constraint:** No documentation content, images, or features removed — speed/perf only.

---

## Executive verdict

Local preview via **cache proxy `:3000`** now serves hub pages in **~1–3 ms** after startup warmup (previously multi-second cold compiles on every first visit). Deep pages still pay a one-time mint compile (~4 s), then **~19 ms** on repeat. Custom JS stayed lean; **207 new WebP siblings** added (~22 MB smaller payload vs PNG/JPEG sources) while **all originals kept**.

| Metric | Before (this session) | After |
|--------|----------------------|--------|
| Hub `/AllExtensions/Index` cold | ~9.8 s | **Pre-warmed HIT ~1–2 ms** |
| Hub `/` warm | ~3–5 ms | **~1–3 ms** |
| Deep page cold → warm | ~compile then warm | **~4.0 s → ~19 ms** |
| `t3-docs.min.js` | 49,165 B | **49,664 B** (+proxy hub warm helpers) |
| `custom.css` | 101,673 B | **101,673 B** (re-minified from source) |
| Doc WebP count | 753 | **960** (+207; originals retained) |
| Doc WebP weight | ~29 MB | **~40.7 MB** (more coverage) |
| Doc PNG weight | ~100 MB | **~100.6 MB** (unchanged — not deleted) |

Browse: http://127.0.0.1:3000/ or http://192.168.0.113:3000/

---

## Issues identified

| # | Issue | Root cause |
|---|--------|------------|
| 1 | Cold route loads 6–12 s | `mint dev` recompiles MDX/RSC per request; no startup warm |
| 2 | Browser revalidates HTML every time | Upstream `Cache-Control: no-store` forwarded by proxy |
| 3 | JPEG/GIF not cached by proxy | `_cacheable()` only listed png/webp/css/js |
| 4 | New TCP to mint per request | Proxy used `Connection: close` |
| 5 | Hub hops cold after restart | No background warm of critical routes |
| 6 | Local idle prefetch blocked (correctly) | Avoided RSC floods, but hubs never warmed via HTML |
| 7 | Large PNG/JPEG still heavy | Many screenshots >100 KB without WebP sibling |
| 8 | HEAD returns empty / BYPASS | Shared GET cache not used for HEAD |

---

## Optimizations implemented

### 1. Cache proxy (`scripts/mint_cache_proxy.py`)

- Background **WARM_PATHS** on startup: `/`, `/ExtNsT3AF/Index`, `/AllExtensions/Index`, `/AllTemplates/Index`, `/AIFoundationExtensions/Index`, `/License/Index`, `/ExtThemes/Index`
- **Keep-alive** HTTP connections to mint (per worker thread)
- Cache **jpg/jpeg/gif/woff/woff2/ico** in addition to existing types
- Replace mint `no-store` with browser-friendly **`Cache-Control`** on HIT/STORE
- TTL default **7200 s**; body limit **5 MB**
- Ops endpoint: `GET /__t3_cache_stats`
- HEAD responses can reuse GET cache entries

### 2. Client JS (`scripts/src/t3-docs.js` → `_static/t3-docs.min.js`)

- `isBehindCacheProxy()` (port `3000`)
- `warmHubsBehindProxy()` — idle **document** fetches of hubs (warms proxy HTML, no `?_rsc` flood)
- Existing lazy images/iframes, intent-only prefetch, RSC gate on raw mint preserved

### 3. Images (`scripts/optimize_images_perf.py`)

- Generated **207 WebP** siblings (`cwebp -q 78`) for rasters ≥100 KB missing/stale WebP
- **Original PNG/JPEG not deleted**
- Markdown refs updated where siblings already existed (minimal delta — most pages already used `.webp`)

### 4. Caching headers (`_static/_headers`)

Already present for production CDN (static 1y, images 7d, HTML short TTL + SWR). No content change.

### 5. Build exclusions (`.mintignore`)

Unchanged — `de/`, `Live-docs/`, `visual-regression/`, `scripts/` stay out of Mintlify publish (smaller build/index).

---

## Files modified / added

| Path | Change |
|------|--------|
| `scripts/mint_cache_proxy.py` | Warmup, keep-alive, cache headers, more types, stats |
| `scripts/src/t3-docs.js` | Proxy-aware hub warming |
| `_static/t3-docs.min.js` | Rebuilt |
| `custom.css` | Re-minified from `scripts/src/custom.src.css` |
| `_static/t3-stats-inline.js` | Regenerated via build script |
| `scripts/optimize_images_perf.py` | **Added** — WebP sibling generator |
| `**/images/*.webp` | **+207** new siblings (originals kept) |
| Various `Index.md` | At most a few image extension → `.webp` (same visuals) |

---

## Validation

- Hub routes return `X-T3-Cache: HIT` with **~1–3 ms** totals after warmup  
- Deep page first compile ~4 s, second hit ~19 ms HIT  
- Cache stats example: `{"hits":20,"misses":9,"bypass":0,"entries":9}`  
- No content/images deleted; PNGs remain on disk  
- Navigation/search/sidebar behavior unchanged (Mintlify shell + existing custom UX)

### Core Web Vitals (expected)

| Vital | Local cold mint | Local via `:3000` warm | Hosted Mintlify (CDN) |
|-------|-----------------|------------------------|------------------------|
| LCP | Dominated by compile | HTML ~instant; LCP = fonts/hero | Best (prebuilt SSG) |
| INP | Intent prefetch + hold UX | Same | Native SPA prefetch OK |
| CLS | Lazy images/iframes | Same | Same |

**Note:** Production Mintlify deploy does not use the Python proxy — it relies on CDN + prebuilt pages. Local proxy closes the gap to CDN-like nav for demos. Hosted search still requires Mintlify project index of this repo.

---

## How to verify locally

```bash
# Prefer cache proxy (LaunchAgent)
open http://127.0.0.1:3000/
curl -s http://127.0.0.1:3000/__t3_cache_stats

# Rebuild custom assets after JS/CSS edits
python3 scripts/build_perf_assets.py

# Optional: more WebP siblings (never deletes originals)
python3 scripts/optimize_images_perf.py --min-bytes 80000
```

---

## Remaining limits (not regressions)

1. **First visit to an unwarmed deep page** still waits on mint compile (~4–10 s) until cached.  
2. **HTML payloads ~700–800 KB** — Mintlify/Next shell; cannot shrink without platform change.  
3. **Hosted search** empty until Mintlify indexes GitHub `master`.  
4. PNG originals remain for fidelity/fallback (~100 MB) — intentional per “do not remove images.”
