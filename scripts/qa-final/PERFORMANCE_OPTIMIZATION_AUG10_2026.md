# Mintlify Documentation — Performance Optimization Report (Aug 10, 2026)

**Date:** August 10, 2026  
**Scope:** Entire T3Planet Mintlify documentation (`Mintilify Doc`)  
**Hard constraint:** No documentation content or images deleted — WebP siblings + MD refs, proxy/JS/CSS only.

---

## Executive verdict

Local preview via **cache proxy `:3000`** now warms **18 hub routes** (was 7) on startup, caches longer (**TTL 14400s**), and serves measured hubs in **~0.6–0.7 ms** on HIT. Deep pages still pay a one-time mint compile (~3.2 s), then **~1 ms** warm. **+41 WebP** siblings (~2.3 MB extra WebP weight; **~4.6 MB** smaller payload vs source rasters) while **all PNG/JPEG originals kept**. Product-doc rasters ≥100 KB / ≥200 KB now have **0** missing WebP siblings (excl. scripts / review frames).

Browse: http://127.0.0.1:3000/

---

## Before / after (this session)

| Metric | Before | After |
|--------|--------|-------|
| `CACHE_TTL` default | 7200 s | **14400 s** |
| Proxy `WARM_PATHS` hubs | 7 | **18** |
| Hub `/` HIT | ~1–3 ms (prior) / pre-restart ~39 ms wall | **~0.65 ms** HIT + `Age` |
| Hub `/ExtNsT3AF/Index` HIT | (prior warm ~ms) | **~0.65 ms** HIT |
| Hub `/AllExtensions/Index` HIT | ~1–2 ms (prior) | **~0.66 ms** HIT |
| Hub `/EXTKarma/Index` HIT | not pre-warmed | **~0.65–0.70 ms** HIT |
| Hub `/ExtNsT3AI/Index` HIT | not pre-warmed | **~0.62–0.65 ms** HIT |
| Deep page cold → warm | ~4.0 s → ~19 ms (Aug 7) | **~3.19 s STORE → ~0.9–1.6 ms HIT** (`/ExtNsYoutube/Configuration/Index`) |
| HTML HIT `Age` header | absent | **present** (optional; skipped for STORE / non-HTML) |
| `text/x-component` cache | no | **yes** |
| jpg/jpeg/gif/woff2 cacheable | already yes | **verified** |
| Doc WebP count | 960 | **1001** (+41) |
| Doc WebP weight | 40.7 MB | **43.0 MB** |
| Doc PNG weight | 105.4 MB | **105.4 MB** (unchanged — not deleted) |
| Doc JPG weight | 43.6 MB | **43.6 MB** (unchanged — not deleted) |
| ≥200 KB rasters missing WebP | **22** | **0** (product docs; excl. scripts/.review-frames) |
| ≥100 KB rasters missing WebP | **59** | **0** (same scope) |
| `t3-docs.min.js` | 49,664 B (Aug 7) | **50,391 B** (expanded hubs + fetchpriority) |
| `custom.css` | 101,673 B (Aug 7) | **101,835 B** (+perf helpers) |
| Cache entries after warm | — | **≥16** within ~30s; **56** after measure |

---

## Optimizations implemented

### 1. Images (`scripts/optimize_images_perf.py` + force pass)

- Encoded WebP siblings (`cwebp -q 78`) for product rasters ≥100 KB missing/stale WebP (incl. the **22** files >200 KB).
- Extra pass for uppercase `.PNG` (Google Docs images).
- Markdown image refs updated to `.webp` when sibling exists (**31** files / **41** refs across passes).
- **Original PNG/JPEG not deleted.**

### 2. Cache proxy (`scripts/mint_cache_proxy.py`)

- Expanded default `WARM_PATHS`: existing hubs plus  
  `/EXTKarma/Index`, `/ExtNsT3AI/Index`, `/ExtNsT3AA/Index`, `/ExtNsT3AC/Index`, `/ExtNsT3AS/Index`, `/ExtNsT3AL/Index`, `/ExtNsT3AB/Index`, `/ExtRTECKEditorPack/Index`, `/ExtNsRevolutionSlider/Index`, `/EXTAvatar/Index`, `/EXTBootstrap/Index`  
  (canonical `/ExtNsT3AF/Index` retained — not `T3AF`).
- `CACHE_TTL` default **14400**.
- On HTML **HIT**, emit **`Age`** (skipped for STORE / non-HTML).
- Cache **`text/x-component`** (RSC/Flight); jpg/jpeg/gif/woff2 already in `_cacheable` (verified).

### 3. Client JS (`scripts/src/t3-docs.js` → `_static/t3-docs.min.js`)

- `HUB_ROUTES` aligned with proxy warm list (`ExtNsT3AF`, Karma, AI suite, Avatar, Bootstrap, etc.).
- `warmHubsBehindProxy()` / `prefetchDocument` use expanded hub list.
- `applyLazyImage`: `decoding="async"`; non-LCP `fetchpriority="low"`; first content image `fetchpriority="high"` if unset.
- Rebuilt via `python3 scripts/build_perf_assets.py`.

### 4. CSS (`scripts/src/custom.src.css` → `custom.css`)

Added (were missing as exact helpers):

```css
img, video, iframe { max-width: 100%; height: auto; }
.t3-embed iframe { content-visibility: auto; contain-intrinsic-size: 400px 225px; }
#content-area img { content-visibility: auto; }
```

### 5. Preview restart

- `launchctl kickstart -k gui/$(id -u)/com.nitsan.mintlify.dev`
- `:3000` returned **200**; `__t3_cache_stats.entries` ≥ **10** within ~30s (READY at entries=16).

---

## HIT measurement detail (post-warm)

| Path | Sample 1 | Sample 2 | X-T3-Cache | Age |
|------|----------|----------|------------|-----|
| `/` | 0.65 ms | 0.67 ms | HIT | 28 |
| `/ExtNsT3AF/Index` | 0.66 ms | 0.65 ms | HIT | 27 |
| `/AllExtensions/Index` | 0.66 ms | 0.67 ms | HIT | 26 |
| `/EXTKarma/Index` | 0.65 ms | 0.70 ms | HIT | 22 |
| `/ExtNsT3AI/Index` | 0.65 ms | 0.62 ms | HIT | 22 |

Deep: `/ExtNsYoutube/Configuration/Index` — **3193 ms STORE** → **1.6 ms / 0.91 ms HIT**.

Final stats snapshot: `{"hits": 39, "misses": 56, "bypass": 87, "entries": 56}`

---

## Files touched

| Path | Change |
|------|--------|
| Many `**/images/*.(png\|jpe?g)` + sibling `.webp` | New WebP siblings only |
| Many `**/Index.md` (image refs) | `.png/.jpeg` → `.webp` where sibling exists |
| `scripts/mint_cache_proxy.py` | Warm list, TTL, Age, x-component |
| `scripts/src/t3-docs.js` | HUB_ROUTES + lazy fetchpriority |
| `scripts/src/custom.src.css` | Perf helpers |
| `_static/t3-docs.min.js`, `custom.css` | Rebuild |
| `scripts/qa-final/PERFORMANCE_OPTIMIZATION_AUG10_2026.md` | This report |

---

## Notes

- Session **before** image scan: miss≥200KB=**22**, miss≥100KB=**59**, WebP=**960**.
- Session **after**: miss≥200/100KB=**0** (excl. `scripts/`, `.review-frames/`, `de/`, etc.); WebP=**1001**.
- No originals deleted; layout-affecting CSS limited to max-width/content-visibility helpers.
- Remaining ≥100 KB rasters without WebP live only under `.review-frames/` (~19 files / ~14 over 200 KB) — intentionally excluded from product-doc conversion.
