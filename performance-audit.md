# Performance Audit — T3Planet Mintlify Docs

**Date:** July 1, 2026  
**Environment:** Local `mint dev` @ http://localhost:3000

---

## Key findings

### What is fast (custom layer)

- Custom JS bundle: **8.2 KB** minified  
- Custom CSS: **~42 KB** minified  
- Warm SPA navigation: **0.6–1.3 KB** transfer per hop  
- No `setInterval` polling in custom scripts  
- Supademo iframes lazy-loaded until near viewport  

### What dominates load time (platform layer)

- **First visit** pulls Mintlify Next.js chunks (~2 MB on home — dev server)  
- This is expected for `mint dev`; **production CDN** is significantly faster  
- `/llms.txt` and `/sitemap.xml` are **not served locally** — only on Mintlify hosting  

### Link Grabber vs full site

- Homepage DOM links: **~102**  
- Full documentation pages in nav: **729**  
- Use `scripts/all_mintlify_urls.txt` for complete URL list  

---

## Core Web Vitals (sample, local dev)

| Page | DOM ready | Load | Transfer |
|------|-----------|------|----------|
| Home | 6.3 s | 0.9 s | 2.1 MB (first cold) |
| License | 5.5 s | 0.02 s | 0.6 KB (warm) |
| T3AA Hub | 5.4 s | 0.1 s | 1.3 KB |
| T3AI Hub | 5.9 s | 0.1 s | 1.3 KB |

**SPA hops (warm):** 2.7–4.7 s between T3AA pages.

---

## Bottleneck classification

| Layer | Severity | Action |
|-------|----------|--------|
| Mintlify platform bundle | High (first load) | Deploy to production CDN |
| Large doc images (PNG) | Medium | WebP batch (`scripts/convert_to_webp.py`) |
| Custom JS/CSS | Low | Optimized this round |
| Sidebar initial DOM | Low | T3AF collapsed by default |
| Search index size | Low | `de/` excluded via `.mintignore` |

---

## Full report

See `scripts/PERFORMANCE_AUDIT_REPORT.md` and `performance-optimization-report.md`.
