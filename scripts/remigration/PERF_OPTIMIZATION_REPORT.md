# Mintlify Documentation — Performance Optimization Report

Date: 2026-08-21  
Environment: local preview (`:3000` cache proxy → `:3001` mint)

## A. Performance Issues Identified

| Area | Root cause | User impact |
|------|------------|-------------|
| Embeds (Supademo/iframes) | Up to 21 iframes started `src` loads immediately on heavy pages (e.g. T3AI Translation) | Slow first paint, network contention, jank |
| Images | Large PNG/JPEG screenshots (many 200KB–1MB+); lazy hints applied late / not below-fold aware | Heavy bandwidth; layout risk |
| Icon preloads | 7 Lucide SVG preloads on every page | Extra early connections competing with content |
| Iframe deferral timing | `lazyIframes()` only in deferred idle path (~200–300ms+) | Browser often began embed navigations first |
| Nav hold (prior) | Skeleton hold on `pointerdown` stole clicks (fixed earlier) | Nested pages appeared broken / stuck loading |
| Asset weight | Published raster corpus ~220MB; 148 files ≥200KB | Slow image-heavy docs pages |

## B. Optimizations Implemented

1. **Critical-path iframe deferral** (`scripts/src/t3-docs.js`)  
   - Run `lazyIframes()` inside `enhanceContentCritical()` and early timeouts  
   - MutationObserver re-applies when Mintlify hydrates late nodes  
   - Benefit: zero eager iframe `src` on Translation/Introduction at measurement time

2. **Smarter image lazy-loading**  
   - Below-fold detection + skip chrome logos  
   - Optional width/height from `naturalWidth/Height` to reduce CLS  
   - Benefit: Translation content images 7/7 `loading=lazy`

3. **Fewer icon preloads** (7 → 3: house, sparkles, puzzle)

4. **CSS media stability** (`scripts/src/custom.src.css` → `custom.css`)  
   - `content-visibility: auto` for lazy images / deferred iframes  
   - Min-height placeholder for deferred iframes

5. **Published image compression** (content preserved; originals kept when WebP added)  
   - Re-encoded 40 large rasters (~2.3MB saved)  
   - WebP + markdown retarget for additional large screenshots (~2.4MB est. transfer savings)  
   - Reports: `PERF_IMAGE_OPT.json`, `PERF_WEBP_OPT.json`

6. **Rebuilt** `_static/t3-docs.min.js` + `custom.css` via `scripts/build_perf_assets.py`

## C. Content Preservation

- No documentation pages deleted  
- No instructions/tables/code blocks removed  
- Images retained (WebP added alongside; markdown points to WebP where converted)  
- Supademo/embeds remain available (activate on scroll / near viewport)  
- Navigation hierarchy unchanged  

Integrity samples (all OK): Introduction, Translation, ExtThemes Introduction, EXTKarma Installation.

## D. Testing Completed

- Baseline + after metrics (Playwright)  
- Warm-cache remasure  
- Client navigation Index → Introduction  
- Translation page embed deferral (desktop + mobile 390×844)  
- Content integrity on key product pages  
- Horizontal overflow check (mobile Translation: none)  

## E. Before / After (measured)

### Embed / image behavior (warm, `:3000`)

| Page | Before | After |
|------|--------|-------|
| `/ExtNsT3AI/Translation/Index` | 21 iframes with `src` eager | **0** `src`, **21** deferred (`data-t3-src`); **7/7** content images lazy |
| `/ExtNsT3AF/Introduction/Index` | 6 iframes eager | **0** `src`, **6** deferred |
| Client nav Index→Introduction (prior hot) | ~0.22s | Warm remasure ~sub-second when cache hot (cold mint TTFB still dominates after purge) |

### Asset optimization

| Pass | Result |
|------|--------|
| In-place reencode (≥150KB) | 40 files, **~2.31 MB** saved |
| WebP + MD retarget (≥200KB) | 7 files, **~2.39 MB** est. transfer saved |

### Notes on wall-clock TTFB

Local mint cold compiles (multi-second TTFB) dominate first load after cache purge. That is environment/compile cost, not content removal. Proxy `:3000` warm hits remain the realistic preview path.

## F. Final Status

### PERFORMANCE OPTIMIZED — READY FOR REVIEW

Remaining (non-blocking): Mintlify still inlines large HTML/RSC payloads (~0.7MB uncompressed document on hubs); further gains would need Mintlify platform/config changes beyond safe local asset/JS work. Legacy `docs/docs` Sphinx trees were left untouched (not served by Mintlify nav).
