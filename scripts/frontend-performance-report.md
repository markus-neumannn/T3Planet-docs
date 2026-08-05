# Frontend Performance Report

**Generated:** June 25, 2026  
**Base URL:** http://192.168.0.137:3000

---

## Console & Network Errors

Sample console errors captured during Playwright audit (15 total):

- `Failed to load resource: the server responded with a status of 404 (Not Found)` (1×)
- `Failed to load resource: the server responded with a status of 403 ()` (14× — third-party embeds, e.g. Supademo)

These are **not** caused by custom `t3-docs.js` and do not block navigation.

---

## Lighthouse (homepage, mobile)

| Metric | Value |
|--------|-------|
| performance | 30 |
| accessibility | 88 |
| seo | 92 |
| fcp_ms | 3192 |
| lcp_ms | 14079 |
| cls | 0 |
| tbt_ms | 2459 |
| tti_ms | 21132 |

> Scores reflect `mint dev` cold compile. Re-test on production CDN for SLA sign-off.

---

## Playwright Summary

| Metric | Value |
|--------|-------|
| Median cold DOM | 10,979 ms |
| Max cold DOM | 15,026 ms |
| Warm SPA median | 6,691 ms (includes first hop to uncompiled route) |
| Warm SPA (same section) | **139 ms** |
| Mobile home DOM | 4,486 ms |
| CLS (all pages) | 0 |

---

## Slow Pages (cold DOM)

| Page | DOM (ms) | Transfer (KB) | CLS |
|------|----------|---------------|-----|
| T3AA System Req | 15026 | 0.9 | 0 |
| T3 Karma Template | 12906 | 0.6 | 0 |
| Templates | 11924 | 0.6 | 0 |
| License | 11780 | 0.6 | 0 |
| Extensions | 11581 | 1.3 | 0 |
| AI Foundation | 10378 | 0.6 | 0 |
| T3AA Screenshots | 9787 | 1.3 | 0 |
| T3AA Hub | 9697 | 1.3 | 0 |
| T3AI Hub | 8950 | 0.6 | 0 |
| Home | 3516 | 2113.0 | 0 |

---

## Large Images (>300 KB, EN content)

| File | Size (KB) |
|------|-----------|
| `ExtNsT3AI/Translation/images/trans-22.png` | 501 |
| `ExtNsT3AI/Translation/images/trans-23.png` | 476 |
| `ExtNsT3AI/Translation/images/trans-24.png` | 458 |
| `ExtNsT3AI/Translation/images/Element_translate.png` | 436 |
| `ExtNsT3AI/Translation/images/trans-9.png` | 428 |
| `ExtNsRevolutionSlider/RevolutionSlider2.0/Configuration/images/05-T3Revolution.png` | 420 |
| `ExtNsT3AI/SEO/images/dasebord-17.png` | 411 |
| `ExtNsT3AI/Media/images/media-21.png` | 398 |
| `ExtNsT3AI/Media/images/media-17.png` | 395 |
| `ExtNsT3AI/Media/images/media-18.png` | 393 |

**30 EN images** exceed 300 KB. Run `python3 scripts/convert_to_webp.py` to address.

---

## SPA Navigation (warm)

| From → To | ms |
|-----------|-----|
| T3AA Index → Screenshots | 8175 (dev compile) |
| Screenshots → System Requirements | **139** |
| System Requirements → Installation | 6691 (dev compile) |

---

## Re-run

```bash
python3 scripts/run_performance_suite.py http://localhost:3000
```
