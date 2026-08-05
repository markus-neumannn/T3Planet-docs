# Live vs Mintlify Performance — Benchmark, Optimization & Validation

**Benchmark (gold standard):** https://docs.t3planet.de/en/latest/ (Sphinx / Read the Docs)  
**Candidate:** Mintlify docs (`mint dev` @ `http://127.0.0.1:3000` + production CDN after deploy)  
**Date:** 2026-08-04

---

## 1. Benchmark analysis (live docs)

| Signal | Live RTD observation |
|--------|----------------------|
| Architecture | Prebuilt static HTML + light Sphinx JS |
| HTML size (home) | ~97 KB |
| JS transfer | **~192 KB** |
| Requests / page | **~17–19** |
| Fonts | Theme/FontAwesome only — **no Google Fonts** |
| TTFB (sampled) | ~100–440 ms (CDN) |
| FCP (sampled) | ~980–1260 ms |
| Full navigation hop | **~212–365 ms** (full document load) |
| Rendering | Server-prebuilt HTML — no React hydration |

Why it feels fast: **static HTML from CDN**, tiny JS, few requests, no MDX compile, no large React runtime.

---

## 2. Mintlify audit (before → after speed pack)

### Before (key gaps vs live)

| Metric | Live | Mintlify (local) | Gap |
|--------|------|------------------|-----|
| JS transfer | ~192 KB | **~793 KB** | ~4× |
| Requests | ~18 | **45–71** | ~3× |
| Fonts | Local/theme | **Google Inter + theme woff2** | Extra RTT |
| Nav hop | ~0.2–0.4 s | Often **2–6 s on mint dev** | Compile-bound |
| Custom hold | — | Full DOM clone (main-thread heavy) | Self-inflicted cost |

### Root causes (evidence-based)

1. **Mintlify React/Next runtime (~780–800 KB JS)** — framework floor; cannot remove from docs repo.
2. **`mint dev` on-demand MDX/RSC compile** — dominates TTFB and SPA hops locally (not representative of CDN).
3. **Google Fonts Inter** — extra network vs live (removed).
4. **Prefetch floods** — idle prefetch of hundreds of routes saturated mint compile queue (fixed/throttled).
5. **Heavy page-hold clone** — expensive on large pages (replaced with light hold).

---

## 3. Optimizations implemented (this pass)

| Change | File(s) | Intent |
|--------|---------|--------|
| Removed Google Fonts (`fonts.Inter`) | `docs.json` | Match live: no fonts.googleapis RTT |
| System UI font stack + `font-display: optional` | `custom.css` | Instant text paint like Sphinx |
| Light navigation hold (title + skeleton, no DOM clone) | `_static/t3-docs.js` | No blank screen **without** main-thread clone cost |
| Removed Google font preconnects | `t3-docs.js` | Fewer early connections |
| Intent-first prefetch; **cap 24**; no local route flood | `t3-docs.js` | Stop compile-queue thrash on mint dev |
| Route manifest generated | `_static/t3-routes.json` (+ inline helper) | Production-safe prefetch list |
| Faster progress timers / quicker release | `t3-docs.js` | Snappier perceived transitions |
| Cache headers retained | `_static/_headers` | CDN asset caching |

---

## 4. Before vs after (measured)

### Home load (Chromium, after speed pack)

| Site | TTFB | FCP | DCL | JS KB | Reqs | Google Fonts |
|------|------|-----|-----|-------|------|--------------|
| Live | 99–393 ms | 980–1244 ms | ~974–1295 | 192 | 19 | 0 (FA only) |
| Mintlify | 457–485 ms | **512–568 ms** | ~539–566 | ~781–793 | ~39–41 | **0** |

Notes:
- Mintlify **FCP can beat live** once compile is warm and Google Fonts are gone.
- JS KB remains ~4× live — **Mintlify platform floor**.

### Navigation

| Scenario | Result |
|----------|--------|
| Live hop | ~212–365 ms |
| Mintlify warm SPA (local mint) | Still often **1–4 s** — dominated by local compile, not our CSS/JS |
| Hold `pointerdown` cost | Light hold (ms-level), not full clone |
| Google Font requests after fix | **0** |

---

## 5. Lighthouse / CWV

**Not gateable on `mint dev`.** Local compile inflates TTFB/LCP.

**Required gate:** Lighthouse mobile+desktop against the **published Mintlify CDN URL** after deploy.

Targets (production):

- LCP < 2.0 s, FCP < 1.0 s, CLS < 0.05, INP < 200 ms

---

## 6. Bundle / network comparison

| | Live | Mintlify |
|--|------|----------|
| JS | ~192 KB | ~780–800 KB (framework) |
| Transfer (home) | ~302 KB | ~990–1000 KB |
| Requests | ~19 | ~40 |
| Controllable docs JS (`t3-docs.min.js`) | — | ~25 KB (ours) |

---

## 7. Test drive / regression

Validated:
- Init (`t3-sidebar-ready`) after `routePath` restore
- No Google Font network requests
- Light hold activates on pointerdown
- Prefetch no longer floods local compile queue
- Syntax check `node --check` on `t3-docs.js` PASS

Known remaining (platform):
- Mintlify theme still loads **its own** woff2 files (not Google) — expected
- Local SPA hops remain slower than live until **production deploy**

---

## 8. Honest success criteria status

| Criterion | Status |
|-----------|--------|
| No blank screens | Improved (light hold) |
| No Google Fonts RTT (match live strategy) | **Done** |
| Controllable JS overhead reduced | **Done** |
| Prefetch safe for mint dev | **Done** |
| Exact hop parity with live on `mint dev` | **Impossible** (compile + React floor) |
| Exact hop/CWV parity on Mintlify **CDN** | **Pending deploy + Lighthouse** |

---

## 9. What you must do for “exact match” feel

1. **Hard-refresh** local preview (`Cmd+Shift+R`).
2. **Deploy to Mintlify production CDN** (this is where comparison becomes fair).
3. Run Lighthouse on the production URL vs `docs.t3planet.de`.
4. Keep treating `mint dev` timings as **dev-only**, never as release SLOs.

---

## 10. Remaining limitations & next upgrades

1. Cannot shrink Mintlify’s ~800 KB React runtime from the docs repo.
2. Theme-bundled fonts still download (smaller issue than Google Fonts).
3. Optional: self-host a single Inter woff2 if brand requires Inter without Google.
4. Optional: `mint export` static snapshot for air-gapped/static hosting closer to Sphinx architecture.
5. Re-enable broader production-only route prefetch via `window.__T3_ROUTES__` after CDN deploy.

---

*Optimization log complete. Controllable bottlenecks addressed; platform floor documented; production CDN is the remaining gate for live-parity CWV.*
