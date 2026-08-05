# SLA Skills — T3Planet Documentation

Operational checklist for documentation quality, performance, and release validation.

---

## Documentation Performance Testing Checklist

Use this checklist before every production deploy and after major content or platform changes.

### 1. Page Speed Testing

- [ ] Start local preview: `mint dev --no-open` (or use staging/production URL)
- [ ] Run Playwright audit: `python3 scripts/performance_audit.py <BASE_URL>`
- [ ] Review `scripts/performance_audit_report.json` and `scripts/PERFORMANCE_AUDIT_REPORT.md`
- [ ] Confirm **CLS = 0** on homepage, hub, and one image-heavy product page
- [ ] Confirm warm SPA navigation **< 500 ms** within the same product section
- [ ] Run Lighthouse: `python3 scripts/run_performance_suite.py <BASE_URL>`
- [ ] Record Performance / Accessibility / SEO scores from `scripts/lighthouse_latest.json`
- [ ] Compare against previous run in `performance-optimization-report.md`
- [ ] **Production:** Re-run Lighthouse on live Mintlify URL (dev scores are not SLA targets)

**SLA targets (production CDN):**

| Metric | Target |
|--------|--------|
| CLS | < 0.1 |
| LCP | < 2.5 s (content pages) |
| Warm in-app navigation | < 500 ms |
| Custom JS (`t3-docs.min.js`) | < 10 KB |

---

### 2. Asset Optimization

- [ ] Verify `docs.json` loads `/_static/t3-docs.min.js` (not unminified or legacy scripts)
- [ ] Run `python3 scripts/build_perf_assets.py --dry-run` and confirm sizes
- [ ] Scan large images: no EN PNG/JPG **> 500 KB** without WebP alternative
- [ ] Run `python3 scripts/convert_to_webp.py` on new screenshots before merge
- [ ] Confirm `_static/_headers` cache rules present for static assets
- [ ] Confirm new images use lazy loading (handled by `t3-docs.js` for content area)
- [ ] Check `custom.css` size stays **< 50 KB** after theme changes

---

### 3. Regression Testing

- [ ] Run migration QA: `python3 scripts/migration_qa_full.py` (or spot-check after nav edits)
- [ ] Verify **0 broken internal links** in EN content
- [ ] Test canonical URLs: `/Product/Section/Index` opens (200)
- [ ] Test legacy `.html` redirects: `/Product/Section/Index.html` → `/Product/Section/Index`
- [ ] Test RTD shorthand redirects: `/en/latest/Product/Section/Index.html`
- [ ] Test leaf pages: `Support.html`, `BuyNow.html`, `GetThisExtension.html`
- [ ] Sidebar: expand/collapse all levels; arrows visible and tappable
- [ ] Search: query product name + section title; results navigate correctly
- [ ] Pagination prev/next on long product sections
- [ ] German `/de/` paths redirect to EN equivalents
- [ ] No JavaScript errors in browser console on homepage + 3 random product pages

---

### 4. Mobile Performance

- [ ] Test viewport **390×844** (Playwright audit includes mobile home DOM)
- [ ] Open mobile nav menu; confirm no layout shift
- [ ] Tap sidebar expand buttons — response **< 300 ms** perceived
- [ ] Scroll long sidebar list — no visible jank
- [ ] Scroll image-heavy page — below-fold images load on approach
- [ ] Verify `touch-action: manipulation` on sidebar (no 300 ms tap delay)
- [ ] Lighthouse mobile performance recorded and archived

---

### 5. Release Validation

- [ ] All changes merged to deploy branch
- [ ] `python3 scripts/build_perf_assets.py` run (minify JS; optional CSS)
- [ ] `python3 scripts/apply_seo_redirects.py` run if pages added/renamed
- [ ] `docs.json` validates (no parse errors from reports in `scripts/`)
- [ ] Deploy to Mintlify production
- [ ] Post-deploy smoke test: homepage + License + one Extension + one Template
- [ ] Post-deploy Lighthouse on production URL
- [ ] Update `performance-optimization-report.md` with before/after scores
- [ ] Archive reports: `scripts/performance_audit_report.json`, `scripts/lighthouse_latest.json`

---

## Documentation URL Testing Checklist

Use after URL/slug changes, navigation edits, or redirect updates.

### 1. Slug Validation

- [ ] Every `docs.json` navigation slug has a matching `Product/Section/Index.md` file
- [ ] No orphan MD files at repo root (operational reports are in `.mintignore`)
- [ ] Page slug format: `Product/Section/Index` (matches folder path, PascalCase preserved from RTD)
- [ ] Run: `python3 scripts/slug_url_audit.py` → review `slug-url-audit.md`

### 2. URL Consistency

- [ ] **Canonical URL** = Mintlify route **without** `.html` (e.g. `/AllExtensions/Index`)
- [ ] Address bar, sidebar href, navbar href, and footer href all match on the same page
- [ ] Hover preview URL matches address bar (no `.html` mismatch)
- [ ] `docs.json` navbar/footer/internal hrefs use clean routes (no `.html`)
- [ ] Markdown internal links use clean routes (no `.html` suffix)

### 3. Redirect Testing

- [ ] `/Product/Section/Index.html` → `/Product/Section/Index` (308/301)
- [ ] `/Product/Section.html` → `/Product/Section/Index` (RTD shorthand)
- [ ] `/en/latest/Product/Section/Index.html` → `/Product/Section/Index`
- [ ] `/de/*` → EN equivalent
- [ ] Leaf pages: `/ExtNsT3AI/Support.html` → `/ExtNsT3AI/Support`
- [ ] No redirect loops (`.html` must not redirect back to `.html`)
- [ ] Re-run after nav changes: `python3 scripts/apply_seo_redirects.py`

### 4. Internal Link Testing

- [ ] `python3 scripts/migration_qa_full.py` — 0 broken internal links (EN)
- [ ] Pagination prev/next opens correct sibling pages
- [ ] Breadcrumb / “On this page” anchors work
- [ ] No markdown links to `/Index` (homepage confusion) — use `/License/Index`
- [ ] Do **not** run deprecated `fix_internal_links_html.py` (adds `.html`); use `strip_internal_links_html.py`

### 5. SEO URL Rules

| Rule | Value |
|------|-------|
| Canonical | `/Product/Section/Index` |
| Legacy public URL | `*.html` redirects to canonical |
| RTD compatibility | `/en/latest/*` redirects to canonical |
| Duplicate content | Avoid serving same page at two URLs without redirect |
| External links | Unchanged (`https://t3planet.de/...`) |

### 6. Release URL Validation

- [ ] `slug-url-fix-report.md` updated after bulk fixes
- [ ] `broken-url-report.md` shows 0 broken sampled URLs
- [ ] Hard-refresh test: Extensions hub — URL bar = `/AllExtensions/Index`, sidebar hover matches
- [ ] Search result URLs open correct pages without 404

---

## Quick Reference — Automation Scripts

| Script | Purpose |
|--------|---------|
| `scripts/performance_audit.py` | Playwright metrics, SPA hops, console errors |
| `scripts/run_performance_suite.py` | Full suite + `frontend-performance-report.md` |
| `scripts/build_perf_assets.py` | Minify `t3-docs.js` and `custom.css` |
| `scripts/convert_to_webp.py` | Batch image format conversion |
| `scripts/optimize_images.py` | Compress images with size report |
| `scripts/migration_qa_full.py` | Nav/link/image parity vs RTD |
| `scripts/apply_seo_redirects.py` | Regenerate `.html` redirects in `docs.json` |
| `scripts/slug_url_audit.py` | Slug/URL consistency audit + reports |
| `scripts/strip_internal_links_html.py` | Remove `.html` from markdown internal links |

---

## Related Documents

- `performance-audit.md` — Current issues, root causes, priorities
- `performance-optimization-report.md` — Changes and before/after metrics
- `scripts/frontend-performance-report.md` — Latest automated run output
- `slug-url-audit.md` — Slug/URL mismatch audit
- `slug-url-fix-report.md` — Fixes applied summary
- `broken-url-report.md` — Broken URL scan results
