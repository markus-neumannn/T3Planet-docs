# T3Planet Documentation — Performance Optimization Report

**Date:** July 1, 2026  
**Scope:** Full Mintlify documentation (729 EN nav pages)  
**Constraint:** No URL, navigation, or content changes

---

## Executive summary

This round focused on **CPU/memory efficiency**, **deferred heavy embeds**, and **faster initial sidebar render**. Custom assets remain small (**~8 KB JS**, **~42 KB CSS**). The dominant load time is Mintlify’s Next.js shell (~2 MB first visit); custom code is no longer a bottleneck.

| Metric | Before (Jun 25) | After (Jul 1) |
|--------|-----------------|---------------|
| `t3-docs.min.js` | ~6.2 KB | **8.2 KB** (+lazy iframes, −polling) |
| `custom.css` | ~41 KB | **~42 KB** (+iframe placeholder) |
| Route polling | `setInterval` every **200 ms** | **Removed** → `MutationObserver` |
| Supademo iframes | Eager load on every page | **Viewport lazy-load** via `data-t3-src` |
| T3AF sidebar | `expanded: true` | **`expanded: false`** (less initial DOM) |
| Median SPA navigation | ~3.6 s (warm) | **~3.6 s** (unchanged — Mintlify-bound) |
| Median cold DOM | ~6 s | **~6 s** (dev server; production CDN faster) |

---

## Optimizations applied

### 1. JavaScript (`_static/t3-docs.js` → `t3-docs.min.js`)

| Optimization | Impact |
|--------------|--------|
| **Removed `setInterval(200)` path polling** | Eliminates perpetual main-thread wakeups |
| **`MutationObserver` on `#content-area`** | Route changes detected only when content swaps |
| **Debounced route handler (80 ms)** | Fewer duplicate lazy-image/iframe passes |
| **Debounced hover prefetch (60 ms)** | Less prefetch churn on fast mouse movement |
| **Lazy Supademo iframes** | `src` deferred to `data-t3-src` until `IntersectionObserver` (120px margin) |
| **Resize-only navbar sync** | `syncNavbarHeight` no longer runs every navigation |
| **Passive listeners** | `mouseover`, `resize` marked passive |

### 2. CSS (`custom.css`)

| Rule | Purpose |
|------|---------|
| `#content-area`, `#navigation-items` `contain` + `content-visibility` | Limits layout/paint scope |
| `.t3-embed iframe[data-t3-src]` placeholder | Prevents CLS while iframe deferred |
| `touch-action: manipulation` on sidebar | Faster tap (INP) |
| `scroll-behavior: auto` globally | No smooth-scroll jank |

### 3. Navigation (`docs.json`)

- **T3AF** group and **T3AF Foundation** root set to `expanded: false` — reduces initial sidebar node count on cold load.

### 4. Caching (`_static/_headers`)

Unchanged — production CDN should serve:

- `/_static/*` → 1 year immutable  
- `/custom.css` → 1 day  
- Images → 7 days  

### 5. Build exclusion (`.mintignore`)

- `de/` mirror excluded → **~156 MB** smaller search index and build  
- Operational reports excluded from publish  

---

## Files modified

| File | Change |
|------|--------|
| `_static/t3-docs.js` | Lazy iframes, MutationObserver, debounce, remove polling |
| `_static/t3-docs.min.js` | Regenerated min bundle |
| `custom.css` | Iframe lazy placeholder styles |
| `docs.json` | T3AF groups `expanded: false` |
| `scripts/PERFORMANCE_AUDIT_REPORT.md` | Fresh audit run |
| `scripts/performance_audit_report.json` | Fresh metrics |

---

## Validation (Jul 1, 2026)

**Tool:** `python3 scripts/performance_audit.py http://localhost:3000`

| Check | Result |
|-------|--------|
| 10 sample pages load | ✅ |
| SPA hops (3) | ✅ 2.7–4.7 s (Mintlify dev) |
| Mobile home DOM | 4.4 s |
| Custom JS errors | None from `t3-docs` |
| Console errors (sample) | 18 (Mintlify/third-party — not custom script) |

**Warm navigation transfer:** 0.6–1.3 KB per hop (SPA working efficiently).

---

## Remaining opportunities (optional, not blocking)

| Priority | Item | Notes |
|----------|------|-------|
| P1 | **Production deploy** | CDN + HTTP/2 cuts first load vs `mint dev` |
| P2 | **Large PNG → WebP** | ~30 EN images >300 KB (mostly T3AI screenshots) |
| P3 | **`trim_custom_css.py`** | Further purge unused sidebar rules |
| P3 | **Lighthouse on production URL** | `scripts/run_performance_suite.py` after deploy |
| P4 | **Supademo `loading="lazy"` in MDX** | Redundant once JS defer is active; optional cleanup |

---

## Automation

```bash
# Minify assets after JS/CSS edits
python3 scripts/build_perf_assets.py

# Playwright page + SPA audit (requires mint dev)
python3 scripts/performance_audit.py http://localhost:3000

# Full suite (audit + Lighthouse if configured)
python3 scripts/run_performance_suite.py
```

---

## Definition of done

| Criterion | Status |
|-----------|--------|
| No perpetual JS polling | ✅ |
| Heavy iframes deferred until visible | ✅ |
| Images lazy-loaded with IO | ✅ |
| Sidebar collapsed by default for largest group | ✅ |
| Assets minified | ✅ |
| Cache headers configured | ✅ |
| Audit script passes on sample pages | ✅ |
| No custom-script regressions | ✅ |

**Production-ready:** Yes — deploy to Mintlify production for full CDN, Brotli, and `llms.txt`/search indexing benefits not available in local dev.
