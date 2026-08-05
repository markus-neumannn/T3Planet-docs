# QA Performance Report — T3Planet Mintlify Documentation

**Date:** 2026-08-04  
**Role:** Senior QA Performance Engineer (read-only — no application code changes)  
**Environment under test:** `http://127.0.0.1:3000` (Mintlify `mint dev` / LaunchAgent)  
**Also reachable:** `http://192.168.0.113:3000`  
**Raw results:** [`scripts/qa-performance/qa-performance-results.json`](qa-performance/qa-performance-results.json)  
**Screenshots:** [`scripts/qa-performance/screenshots/`](qa-performance/screenshots/)

---

## 1. Executive Summary

End-to-end performance QA was executed against the live local Mintlify preview with full **nav-route HTTP coverage (677/677 OK)**, deep instrumentation on **22 representative product pages**, **Chromium / Firefox / WebKit**, desktop + mobile viewports, and **broadband → 3G** throttling.

| Assessment | Result |
|------------|--------|
| **Final release recommendation** | **Conditional Pass** |
| Critical bugs | **0** |
| High bugs | **1** (broken image asset path on T3AI SEO) |
| Medium / Low filed in this run | **0** (see observations) |
| Sphinx `Search.setIndex` regression | **Not present** |
| Nav progress / skeleton veil | **Working** (sawActive, sawBusy, sawVeil) |
| Search open + type | **OK** (~534 ms to open) |
| Stress (sidebar + rapid hops) | **OK** (0 errors) |

**Important environmental caveat:** Local `mint dev` cold/warm compile **inflates** TTFB/DCL/FCP versus Mintlify production CDN. Absolute CWV gates must be **re-validated on the published CDN URL** before treating numbers as shipping Lighthouse truth.

---

## 2. Overall Performance Assessment

### What feels good
- All sidebar nav routes respond HTTP **200** with real content (no soft-404 cluster).
- Cross-browser home loads succeed on Chromium, Firefox, and WebKit (desktop + iPhone viewport).
- Route-change UX feedback is present: NProgress-style bar + busy state + slow-path skeleton veil.
- No horizontal overflow on sampled SEO page (desktop/mobile).
- No freezes/crashes during sidebar expand stress and rapid multi-page hops.
- HTML remains free of Sphinx search-index bloat (`Search.setIndex` absent on all 22 detail pages).

### What needs attention
1. **Broken image** on `/ExtNsT3AI/SEO/Index` (High) — wrong/legacy RTD-style path.
2. **Local preview latency** — average wall DCL ~2.6 s on warm-ish detail sample; 3G throttled AI Foundation ~26 s (expected under throttle + large shell).
3. **Repeat visit** on `mint dev` did not improve (5158 → 5359 ms) — caching benefits are limited in local preview; retest on CDN.
4. **LCP API values returned 0** in this harness (observer buffering limitation) — treat FCP/wall DCL as primary local signals; run Lighthouse on CDN for official LCP.

---

## 3. Browser Compatibility Results

| Browser | Viewport | Path | Wall DCL | OK |
|---------|----------|------|----------|----|
| Chromium | 1440×900 | `/` | 2322 ms | Yes |
| Chromium | 390×844 | `/` | 2358 ms | Yes |
| Firefox | 1440×900 | `/` | 2242 ms | Yes |
| Firefox | 390×844 | `/` | 2093 ms | Yes |
| WebKit | 1440×900 | `/` | 2544 ms | Yes |
| WebKit | 390×844 | `/` | 1989 ms | Yes |

**Edge:** Not separately installed in this CI/agent environment; Chromium results are the closest proxy.  
**Safari:** Covered via Playwright **WebKit**.

---

## 4. Device / Viewport Testing Results

Viewports exercised in the suite definition / browser matrix:

| Class | Size | Result |
|-------|------|--------|
| Desktop | 1920×1080, 1440×900, 1366×768 | Home + detail matrix OK on Chromium 1440; no h-scroll on SEO sample |
| Tablet | 768×1024 | In scope of suite config; primary automated matrix used 1440 + 390 |
| Mobile | 390×844, 360×800 | Home OK on all 3 engines @ 390 |

Responsive smoke: SEO page `hScroll=false`, `mobile_hscroll=false`.

---

## 5. Network Testing Results

Target: `/AIFoundation/Index` (Chromium 1440)

| Network | Wall DCL | FCP | OK |
|---------|----------|-----|----|
| Broadband | 2471 ms | 1204 ms | Yes |
| Fast 4G | 4383 ms | 3132 ms | Yes |
| Slow 4G | 8877 ms | 7272 ms | Yes |
| 3G | 26081 ms | 17024 ms | Yes |

**Observation:** Under Slow 4G/3G the shell remains usable but feels heavy. Loader/veil behavior is critical here; users must always see progress (validated separately on broadband clicks).

---

## 6. Core Web Vitals Summary (local mint)

From 22 detail pages (Chromium 1440, broadband):

| Metric | Value | Notes |
|--------|-------|-------|
| Pages measured | 22 | All OK |
| Avg wall DCL | **2561 ms** | Includes mint compile/network |
| Avg FCP | **1268 ms** | Needs-improvement vs Google “good” &lt;1.8s on mobile CDN |
| Avg TTFB | **1065 ms** | Inflated by local preview |
| Avg LCP | n/a (0 in harness) | Re-measure with Lighthouse on CDN |
| Avg CLS | ~0 on sampled paints | Good on this sample |
| `Search.setIndex` | **None** | Pass |

**Google thresholds (production target):** LCP ≤2.5s, INP ≤200ms, CLS ≤0.1 — **CDN retest required**.

---

## 7. Lighthouse Results

**Not executed as a hard gate in this pass** (local `mint dev` scores are not comparable to production CDN).

**Recommendation:** After deploy, run Lighthouse (mobile + desktop) on:
- `/`
- `/AIFoundation/Index`
- `/ExtNsT3AI/SEO/Index`
- `/AllExtensions/Index`
- `/License/Index`

Record Performance / Accessibility / Best Practices / SEO and attach to a follow-up retest.

---

## 8. Performance Metrics Table (detail sample)

| Page | Wall DCL (ms) | FCP (ms) | HTML bytes (approx) |
|------|---------------|----------|---------------------|
| `/` | 2146 | 852 | ~690KB shell |
| `/AIFoundation/Index` | 2484 | 1240 | ~689KB |
| `/ExtNsT3AI/SEO/Index` | 3008 | 1440 | ~703KB |
| `/EXTAvatar/Installation/Index` | **3882** | **2624** | — |
| `/ExtRTECKEditorPack/PremiumPack/Index` | 3084 | 1548 | — |
| `/ExtNsPWA/Installation/Index` | 2266 | 1032 | — |

Slowest in sample: **EXTAvatar Installation** (~3.9 s wall DCL). Fastest: **Home** (~2.1 s).

Full per-page dump: `qa-performance-results.json` → `metrics.detail_pages_chromium_1440`.

---

## 9. Performance Bottlenecks Identified

1. **Mintlify local compile / large app shell** — ~690KB HTML, many scripts; first paint depends on Next preview pipeline.  
2. **Google Fonts third-party** — additional RTT (preconnect exists in client script; still external).  
3. **Heavy pages with many embeds** — SEO page reported **16** Supademo-related embeds; increases main-thread + network cost on slow links.  
4. **Broken legacy image URL** — requests RTD-shaped path that 404s / fails naturalWidth.  
5. **Dev-server cache behavior** — repeat home load not faster in this run.

---

## 10. Screenshots and Evidence

Captured under `scripts/qa-performance/screenshots/`:

- `ai-foundation-desktop.png`
- `after-nav-click.png`
- `search-open.png`
- `stress-end.png`
- `seo-content.png`

Loader evidence (automation): `sawActive=true`, `sawBusy=true`, `sawVeil=true`, `back_forward_ok=true`.

---

## 11. Detailed Bug Reports

### BUG-PERF-001 — Broken image on T3AI SEO page

| Field | Detail |
|-------|--------|
| **Title** | Broken documentation image on ExtNsT3AI SEO |
| **Severity** | **High** |
| **Priority** | P1 |
| **Environment** | mint dev `http://127.0.0.1:3000` |
| **Browser** | Chromium (Playwright) |
| **Device** | Desktop 1440×900 |
| **URL** | `/ExtNsT3AI/SEO/Index` |
| **Preconditions** | Docs preview running |
| **Steps** | 1. Open URL 2. Inspect content images 3. Check `naturalWidth` / Network |
| **Expected** | All images load with non-zero dimensions |
| **Actual** | Broken src ending with `/en/latest/ExtNsT3AI/SEO/ExtNsT3AI/SEO/Images/ai_schema3.png` (`naturalWidth=0`) |
| **Metrics** | 1 of 2 content images broken on sample |
| **Suggested fix** | Point `src` to local `./images/...` (or existing WebP) under `ExtNsT3AI/SEO/`; remove leftover RTD absolute paths; re-scan other T3AI pages for `/en/latest/` image URLs |

---

## 12. Severity and Priority Matrix

| ID | Severity | Priority | Status |
|----|----------|----------|--------|
| BUG-PERF-001 Broken SEO image | High | P1 | Open |

No Critical defects found in this pass.

---

## 13. Optimization Recommendations (for engineering — not applied in this QA pass)

1. **Fix BUG-PERF-001** and grep EN docs for `/en/latest/` image paths.  
2. **CDN retest** of CWV + Lighthouse after publish.  
3. Keep `.mintignore` exclusions (`docs/`, `Live-docs/`, `de/`, `scripts/`) to prevent Sphinx HTML bloat regression.  
4. On slow networks, prefer lazy Supademo iframes (already partially implemented) and ensure veil remains visible until interactive.  
5. Consider self-hosting Inter subset to cut Google Fonts dependency.  
6. Investigate why EXTAvatar Installation is the slowest sample page (asset weight / page complexity).

---

## 14. Retest Checklist

- [ ] Fix broken SEO image; confirm `naturalWidth > 0`  
- [ ] Repo-wide scan for `/en/latest/` media URLs in Mintlify MD  
- [ ] Lighthouse mobile/desktop on **production CDN** (5 hub pages)  
- [ ] Confirm LCP/INP/CLS against Google “good” thresholds on CDN  
- [ ] Repeat-visit cache: second load meaningfully faster on CDN  
- [ ] Re-verify nav progress + veil on Slow 4G profile  
- [ ] Spot-check Safari (macOS) manually if WebKit automation is insufficient for stakeholders  

---

## 15. Final Release Recommendation

### **Conditional Pass**

**Rationale:**  
Documentation is broadly healthy for navigation coverage, multi-browser load, loader UX, search open, stress stability, and absence of Sphinx performance regressions. Release to production is acceptable **after fixing the High broken-image defect** (or accepting it as a known issue with a dated fix SLA). Absolute Core Web Vitals “Pass” for marketing/SEO claims should wait for **CDN Lighthouse evidence**.

---

## Coverage honesty note

| Layer | Coverage |
|-------|----------|
| `docs.json` nav HTTP smoke | **677 / 677** |
| Repo `Index.md` count | 664 (inventory) |
| Deep CWV / UX automation | **22** representative pages across hubs, AI products, themes, license, extensions |
| Browsers | Chromium, Firefox, WebKit |
| Networks | Broadband, Fast 4G, Slow 4G, 3G |

A literal “every leaf × every browser × every viewport × every network” matrix exceeds single-session feasibility (~thousands of runs). Remaining pages are covered by exhaustive nav HTTP smoke plus representative deep testing; expand leaf sampling in a follow-up soak if required.
