# Performance Optimization Report — Mintlify Docs

**Date:** 2026-08-04  
**Workspace:** `/Users/nitsan/www/AI Agents/Mintilify Doc`  
**Preview:** http://127.0.0.1:3000 / http://192.168.0.113:3000  
**Scope:** Client UX layer (Mintlify customization: `_static/t3-docs.js`, `custom.css`, `_static/_headers`, `docs.json` scripts)

---

## 1. Root cause analysis

| Bottleneck | Evidence | Root cause |
|------------|----------|------------|
| No navigation feedback | Users saw blank waits while SPA compiled | `#t3-nav-progress` was created in JS but **had no CSS** — invisible loader |
| Slow first navigations on local preview | Warm DCL often 2–10s in `mint dev` | Mintlify/Next **dev cold compile** per route (not CDN production) |
| Large HTML (~690KB) | Home/AI/SEO samples | Mintlify app shell + search runtime (acceptable); **no** Sphinx `Search.setIndex` regression |
| Font latency | `fonts.googleapis.com` / `fonts.gstatic.com` in HTML | Extra RTT without early preconnect |
| Layout shift risk on embeds | Supademo iframes | No reserved aspect ratio before load |
| Prefetch under-used | `PREFETCH_MAX=24`, sidebar-only hover | Missed navbar/docs-wide intent prefetch |

**Platform constraint:** Mintlify owns the React/Next bundle, search index, and SSR. We cannot tree-shake Mintlify internals or raise production Lighthouse from local `mint dev` alone. Optimizations focus on **perceived performance**, **route feedback**, **prefetch**, **CLS**, and **caching headers**.

---

## 2. Optimizations implemented

### Navbar loader (NProgress-style)
- Slim top bar `#t3-nav-progress` with animated trickle
- Starts ~80ms after navigation (avoids flash on instant hops)
- Completes to 100% on route settle; respects `prefers-reduced-motion`
- Wired to: link clicks, `popstate`, Next `routeChangeStart/Complete/Error`, history `pushState`

### Soft page loader (skeleton veil)
- `#t3-page-veil` shimmer placeholders appear only if navigation exceeds **~300ms**
- Content dims slightly (`html.t3-route-loading`) without blank white screens
- Auto-clears when route completes

### Navigation / prefetch
- `PREFETCH_MAX`: 24 → **40**
- Sidebar idle prefetch: 60 → **80** links
- Hover/focus prefetch expanded to **entire document** (sidebar + navbar + content)
- Pointer-down prefetch retained

### Assets / CLS / caching
- Font + Supademo **preconnect / dns-prefetch** injected at init
- `.t3-embed` **aspect-ratio 16:9** + `content-visibility: auto` for embeds/tables/pre
- `_headers`: long-cache `woff2`, CSS day cache, HTML `stale-while-revalidate`
- Rebuilt `_static/t3-docs.min.js` (**custom.css not minified in place**)

### Stability fix during this pass
- Sanitized `":ns_*"` keyword entries that contributed to Mintlify frontmatter parse noise after earlier description cleanup

---

## 3. Before vs after (local `mint dev`)

| Metric | Before | After |
|--------|--------|-------|
| Visible nav progress bar | Missing (no CSS) | **Visible** on click (`sawProgress: true`) |
| Slow-nav skeleton | None | **Veil after 300ms** |
| Prefetch budget | 24 | **40** |
| `Search.setIndex` in HTML | Absent | Absent (guard held) |
| Home HTML size | ~677–692KB | ~692KB (shell; no Sphinx junk) |
| Client script | 14.2KB min | **17.7KB** min (loader/prefetch features) |

Warm SPA timings on local preview remain dominated by Mintlify compile — treat CDN production as the real CWV target.

Artifacts: `scripts/perf-after-opt.json`

---

## 4. Core Web Vitals / Lighthouse

| Note | Detail |
|------|--------|
| Local Lighthouse | **Non-blocking** — `mint dev` cold compile ≠ production CWV |
| Expected CDN gains | Earlier font connect, fewer CLS from embeds, instant nav feedback (INP perception), better cache headers |
| Target | Lighthouse ≥90 on **deployed** Mintlify CDN after publish |

---

## 5. Remaining limitations / recommendations

1. **Publish to Mintlify production** and re-run Lighthouse/CWV on the CDN URL.  
2. Consider **self-hosting Inter** subset (woff2) to drop Google Fonts RTTs if brand allows.  
3. Continue converting large PNGs → WebP where not already done.  
4. Mintlify search UX is platform-owned — debounce/result rendering cannot be deeply customized.  
5. Keep `.mintignore` excluding `docs/`, `docs/_build/`, `de/`, `Live-docs/`, `scripts/` forever.

---

## 6. Success criteria checklist

- [x] Professional navbar loading indicator on route changes  
- [x] Skeleton/veil for slow navigations (>300ms); no intentional blank screens  
- [x] Stronger prefetch for smoother hops  
- [x] CLS guards for embeds; font preconnect  
- [x] Caching headers improved  
- [x] No Sphinx HTML regression  
- [x] Production-ready client changes tested (progress bar activates on nav)  
