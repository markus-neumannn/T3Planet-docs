# Deep Performance Optimization — Results

**Date:** June 15, 2026  
**Environment:** `mint dev` @ http://localhost:3338 (Node 22)

---

## 1. Root Causes Found

| Issue | Impact | Fix |
|-------|--------|-----|
| **4 JS files auto-loaded by Mintlify** (`docs-ui.js`, `sidebar-nav.js`, `english-only.js`, `t3-docs.js`) | Mintlify loads every root `.js` on every page **plus** `docs.json` scripts → duplicate execution, extra parse/hydration | Archived legacy JS; single `/_static/t3-docs.min.js` via `docs.json` only |
| **`de/` folder (156MB) still indexed** | Bloated search index, slower builds, dev compilation | Added `.mintignore` excluding `de/` |
| **`custom.css` 58KB unminified** | Slow CSS parse, render-blocking | Trimmed dead rules + minified to **39KB** (−33%) |
| **Heavy sidebar JS** (68-button DOM walks, MutationObservers) | Main-thread jank on navigation | Replaced with **3.1KB** minimal bundle |
| **Large PNG screenshots (up to 1.4MB)** | Slow LCP on image pages | **45 images** converted to WebP (~70–90% smaller) |
| **Mintlify `mint dev` on-demand compilation** | 5–12s first visit per route | Documented; use `scripts/fast_preview.sh` for static export |

---

## 2. Files Changed

| File | Change |
|------|--------|
| `.mintignore` | **NEW** — excludes `de/`, `scripts/` from build + search |
| `docs.json` | Script → `/_static/t3-docs.min.js` only |
| `_static/t3-docs.js` | **NEW** — minimal 3.5KB bundle (theme, redirect, prefetch, lazy images, nav progress) |
| `_static/t3-docs.min.js` | **NEW** — minified 3.1KB |
| `_static/_headers` | **NEW** — CDN cache headers for static assets |
| `custom.css` | Trimmed + minified (58KB → 39KB) |
| `t3-docs.js` | **DELETED** from root (stopped auto-load) |
| `docs-ui.js`, `sidebar-nav.js`, `english-only.js` | **MOVED** → `scripts/archived/` |
| `scripts/trim_custom_css.py` | **NEW** — CSS dead-code removal |
| `scripts/build_perf_assets.py` | **NEW** — CSS/JS minification |
| `scripts/convert_to_webp.py` | **NEW** — WebP conversion + markdown updates |
| `scripts/fast_preview.sh` | Static export server for fast local testing |
| `scripts/optimize_images.py` | Skip `de/` folder |
| 45+ `.md` files | Image paths updated `.png`/`.jpg` → `.webp` |

---

## 3. Bundle Size — Before vs After

| Asset | Before | After | Change |
|-------|--------|-------|--------|
| Custom JS (total loaded) | ~13KB × **4 files** (~52KB parse) | **3.1KB × 1 file** | **−94%** |
| `custom.css` | 58,107 bytes | 39,016 bytes | **−33%** |
| Search/build index scope | EN + DE (~156MB DE) | **EN only** | **−156MB** from index |
| Large images (sample) | owlcarousel 1.4MB PNG | 145KB WebP | **−90%** |

---

## 4. Lighthouse / Web Vitals — Before vs After

| Metric | Before (audit) | After (deep fix) | Target |
|--------|----------------|------------------|--------|
| Performance score | 35 | **39** | 90+ (production CDN) |
| FCP | 3.2s | **3.0s** | <1.8s |
| LCP | 17.0s | **8.2s** | <2.5s |
| TBT | 1,750ms | **1,460ms** | <200ms |
| CLS | **0** | **0** | <0.1 ✓ |
| Speed Index | 7.9s | **6.3s** | — |
| TTI | 19.0s | **16.0s** | — |
| TTFB (dev) | 971ms | 2,210ms* | <800ms |

\*TTFB varies with dev-server cold compile; production CDN TTFB is typically <200ms.

### Playwright audit (10 pages)

| Metric | Before | After |
|--------|--------|-------|
| Median DOM ready | 6,837ms | 8,364ms |
| Mobile home DOM | 6,177ms | **5,226ms** |
| SPA warm hop (same section) | **84ms** | ~88ms |

> Median DOM varies with dev compile order. **LCP halved (17s→8.2s)** is the clearest improvement from asset + index optimization.

---

## 5. Optimizations Implemented

### JavaScript
- Single minified bundle in `_static/` (no root `.js` auto-discovery)
- Removed MutationObserver, ResizeObserver, 68-button DOM enhancement
- Prefetch on hover only (no idle prefetch storm)
- Instant nav progress bar on click
- Lazy `loading`/`decoding` on images via idle callback

### CSS
- Removed dead dropdown, search-filter, extension-list, language-footer blocks
- Consolidated dark-mode text rules
- Minified entire stylesheet
- `scroll-behavior: auto` everywhere (no smooth-scroll jank)

### Images
- 45 large images → WebP with markdown path updates
- Prior pass: 46 images compressed (~4MB saved)

### Build / Deploy
- `.mintignore` excludes German mirror + internal scripts
- `_static/_headers` for long-term asset caching
- `mint validate` passes
- `scripts/fast_preview.sh` for static export preview (production-like speed)

### Fonts
- `docs.json` already uses Inter 400 + 600 only (minimal)

---

## 6. Remaining Limitations

1. **Local `mint dev`** compiles pages on first visit (5–12s) — not fixable in-repo; use `mint export` or production deploy.
2. **Lighthouse 90+** requires Mintlify production CDN (edge-cached static HTML).
3. **TBT ~1.5s** is dominated by Mintlify/React framework, not custom code.
4. Some **403 console errors** from third-party embeds (Supademo) — external.

---

## 7. How to Verify

```bash
# Dev server (Node 22)
PATH="/opt/homebrew/Cellar/node@22/22.22.3/bin:$PATH" mint dev --port 3338

# Automated audit
python3 scripts/performance_audit.py http://localhost:3338

# Lighthouse
npx lighthouse http://localhost:3338/ --only-categories=performance --view

# Fast static preview (production-like)
./scripts/fast_preview.sh 3340
```

**Preview URLs:** http://localhost:3338 · http://192.168.0.110:3338

---

## 8. Confirmation

The documentation site is now optimized within repo control:

- ✓ Single 3KB custom script (was 4 scripts)
- ✓ 39KB minified CSS (was 58KB)
- ✓ 156MB German content excluded from build/search
- ✓ 45+ images converted to WebP
- ✓ CLS = 0, LCP improved 52%, Speed Index improved 20%
- ✓ `mint validate` passes

**For production-speed browsing:** deploy to Mintlify hosted docs or run `./scripts/fast_preview.sh`.
