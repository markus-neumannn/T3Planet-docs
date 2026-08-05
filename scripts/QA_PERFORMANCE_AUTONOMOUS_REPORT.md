# Autonomous End-to-End Performance QA Report

**Site:** T3Planet Docs (Mintlify)  
**Environment:** `http://127.0.0.1:3000` (`mint dev`)  
**Date:** 2026-08-04T08:36:20Z  
**Verdict:** **Conditional Pass**  
**Overall rating:** B+ (local mint); CDN CWV not gateable from this environment  
**Release readiness:** CONDITIONAL — fix BUG-PERF-001 before production sign-off; retest CWV on CDN after publish

---

## 1. Executive Summary

Full autonomous performance / stability / UX audit against the local Mintlify preview, with mandatory self-validation (3× repro where applicable), false-positive elimination, and regression scope checks.

**Gate result:** Conditional Pass — **1 verified High bug** blocks unconditional release sign-off. Navigation, search, nav loader, multi-browser smoke, and HTTP nav coverage otherwise pass. Local DCL/FCP are inflated by `mint dev` compile cost and must **not** be treated as production Core Web Vitals.

| Area | Result |
|------|--------|
| Nav HTTP (docs.json routes) | 672 OK; 2 prior timeouts revalidated 200 |
| Nav progress + veil | PASS 3/3 |
| Search usability | PASS 3/3 (after FP rejection) |
| Broken content images | **FAIL** — BUG-PERF-001 |
| Chromium / Firefox / WebKit | PASS (+ mobile viewport) |
| Network throttle | Expected degradation (3G ~27s wall) |
| Local warm SPA hops | INFO only (mint compile) |

---

## 2. Overall Performance Rating

**B+ on local mint** for structural readiness (loaders, search, routing, browser smoke).  
**CDN CWV grade: Not measured in this run** — local TTFB/DCL are dominated by Mintlify on-demand compile (often ~1.8–3.0s TTFB on warm content pages). Production rating requires Lighthouse/CWV on the published CDN URL.

---

## 3. Browser Compatibility Matrix

| Engine | Home load | Mobile 390×844 | Notes |
|--------|-----------|----------------|-------|
| Chromium | PASS | PASS | Primary automation browser |
| Firefox | PASS | PASS | Title + body content OK |
| WebKit | PASS | PASS | Safari-engine smoke |
| Edge | Not separate | — | Chromium-equivalent; not dual-run |
| Safari macOS | Via WebKit | — | Full Safari UI not instrumented |

---

## 4. Device Compatibility Matrix

| Class | Viewport | Result |
|-------|----------|--------|
| Desktop | 1280×800 / 1440×900 | PASS |
| Mobile | 390×844 | PASS (emulated) |
| Tablet | Not exhaustive this run | Covered in prior responsive QC (0 high-severity layout issues) |

---

## 5. Network Performance Comparison

From autonomous throttle suite (home-ish load):

| Profile | Wall (ms) | TTFB (ms) | FCP (ms) | DCL (ms) |
|---------|-----------|-----------|----------|----------|
| Broadband | 3987 | 2549 | 3120 | 3313 |
| Fast 4G | 4154 | 1377 | 3372 | 3398 |
| Slow 4G | 12762 | 3597 | 11804 | 12091 |
| 3G | 27290 | 2926 | 19460 | 26636 |

**Assessment:** Degradation tracks network class as expected. Not filed as a product defect; CDN publish + HTTP/2 caching should improve real-user TTFB/FCP vs local mint.

---

## 6. Core Web Vitals Summary

| Metric | Local mint (indicative) | Production gate |
|--------|-------------------------|-----------------|
| TTFB | Often 0.4–2.8s (compile) | Measure on CDN |
| FCP | Often ~0.6–3.0s | Measure on CDN |
| LCP | Not reliably isolated from mint compile | Measure on CDN |
| CLS | No CLS defect filed this run | Spot-check after image URL fix |
| INP / TBT / TTI | Loader/search interactions PASS | CDN Lighthouse |

**Do not fail release on local mint CWV numbers.**

---

## 7. Lighthouse Results

Not executed against production CDN in this session. **Required follow-up:** Lighthouse mobile+desktop on published docs host after BUG-PERF-001 fix.

---

## 8. Page-by-Page Performance Results (warm local samples)

| Path | TTFB range | FCP range | DCL range | Requests | Transfer |
|------|------------|-----------|-----------|----------|----------|
| `/` | 421–1948 ms | 584–2120 | 602–2140 | 73 | ~1004 KB |
| `/ExtNsT3AI/Index` | 1887–2117 | 2068–2316 | 2082–2333 | 56 | ~1004 KB |
| `/AIFoundation/Introduction/Index` | 1860–2775 | 2064–2964 | 2082–2979 | 63–64 | ~1090 KB |
| `/License/Index` | 1795–2094 | 1972–2316 | 1986–2327 | 56 | ~1004 KB |
| `/AllExtensions/Index` | 1993–2296 | 2172–2472 | 2188–2486 | 68 | ~1004 KB |

---

## 9. Verified Performance / UX Issues

### BUG-PERF-001 — Broken image(s) on ExtNsT3AI SEO page
| Field | Value |
|-------|-------|
| Severity | **High** |
| Priority | P1 |
| Browser | Chromium (repro); content defect — all browsers |
| Device | Desktop 1440×900 |
| Environment | http://127.0.0.1:3000 |
| URL | `/ExtNsT3AI/SEO/Index` |
| Preconditions | Preview running |
| Steps | 1) Open URL 2) Wait for images 3) Inspect `main`/`article` imgs `naturalWidth` 4) Repeat fresh page 3× |
| Expected | All content images `naturalWidth > 0` |
| Actual | Broken src `https://docs.t3planet.de/en/latest/ExtNsT3AI/SEO/ExtNsT3AI/SEO/Images/ai_schema3.png` (`naturalWidth=0`) |
| Reproducibility | Confirmed when images settle (2/3 final recheck; 3/3 earlier suite) |
| Regression scope | **12 MD files / ~31 absolute `docs.t3planet.de/en/latest` image URLs** |
| Evidence | `scripts/qa-performance/screenshots-v2/seo-broken-img.png` |
| Root cause | Migrated/absolute live-docs image URLs with duplicated path segments; not local `./images/` |
| Suggested fix | Rewrite to local assets; grep MD for `docs.t3planet.de/en/latest` media |

---

## 10. Root Cause Observations

1. **Broken images:** Absolute RTD URLs with bad path duplication after migration.
2. **Local slowness:** Mintlify `mint dev` on-demand compile — rejected as product CWV defect (FP).
3. **Nav “failures”:** Transient request timeouts under short HTTP timeout — rejected after 200 OK recheck.
4. **Search “unusable”:** Playwright Cmd+K/focus race — rejected after click-based 3/3 PASS.

---

## 11. Performance Metrics Dashboard (summary)

- Home warm best: TTFB **421 ms**, FCP **584 ms**, DCL **602 ms**, load **998 ms**
- Content pages warm typical: TTFB **~1.8–2.3 s**, FCP/DCL **~2.0–2.5 s**
- Transfer ~1.0–1.1 MB on sampled pages (includes JS/CSS/fonts)
- Nav loader: active + busy + veil present
- Prefetch / progress bar: present in DOM

---

## 12. Screenshots and Evidence

| Artifact | Path |
|----------|------|
| SEO broken image | `scripts/qa-performance/screenshots-v2/seo-broken-img.png` |
| Search revalidation | `scripts/qa-performance/screenshots-v2/search-reval-1.png` (+2, +3) |
| Machine JSON | `scripts/qa-performance/qa-performance-final.json` |
| FP recheck | `scripts/qa-performance/qa-fp-recheck.json` |
| Autonomous raw | `scripts/qa-performance/qa-performance-autonomous.json` |

---

## 13. Prioritized Bug List

| ID | Severity | Status | Action |
|----|----------|--------|--------|
| BUG-PERF-001 | High | **Open** | Fix absolute live image URLs (12 files) |
| BUG-PERF-003 | Medium | **Rejected FP** | No fix |
| BUG-PERF-006 | High | **Rejected FP** | No fix |

---

## 14. Regression Testing Results

| Check | Result |
|-------|--------|
| Similar SEO/media pages | Same class of absolute live URLs in 12 files |
| Nav smoke after timeout suspicion | Both License routes 200 ×3 |
| Search after typed=false suspicion | PASS ×3 |
| Loader after perf engineering | PASS ×3 |
| Multi-engine home | PASS ×3 |

---

## 15. Release Readiness Assessment

**CONDITIONAL PASS**

Ship blockers:
1. Fix BUG-PERF-001 (and preferably bulk-fix the other 11 MD files with live absolute image URLs).

Non-blockers / follow-ups:
2. Run Lighthouse CWV on CDN after publish.
3. Keep treating local mint DCL as non-gating.

---

## 16. Recommendations for Optimization

1. **P0 content:** Replace `https://docs.t3planet.de/en/latest/...` image refs with local `./images/`.
2. **CI:** Add a check that fails on absolute live-docs media URLs in shipped MD.
3. **Post-deploy:** Mobile+desktop Lighthouse on production; watch LCP on image-heavy pages.
4. **Keep:** Nav progress/veil + hover prefetch — validated working.
5. **Avoid:** Using local mint timings as production performance SLOs.

---

*Report generated by autonomous Senior Performance QA pass with self-validation. Only verified issues retained.*
