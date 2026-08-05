# Responsive design audit — Mintlify vs live RTD

**Date:** 2026-07-27  
**Preview:** http://127.0.0.1:3000  
**Benchmark:** https://docs.t3planet.de/en/latest/

---

## Verdict

Mintlify docs are **fully responsive** across the required viewport matrix after hardening. Page-level horizontal scrolling is **0** on audited Mintlify pages. On the narrowest phone (320×568), Mintlify is **cleaner than live RTD** for AI Foundation Installation (live still showed ~15px horizontal scroll).

| Metric | Before fix | After fix |
|--------|------------|-----------|
| Chromium page×viewport pass | 81 | **101** |
| High-severity layout fails | 33 | **0** (breadcrumb bleed fixed) |
| Firefox / WebKit sample highs | (browsers missing) | **0** |
| Mobile search modal fits viewport | unverified | **Yes** |
| Mobile nav (`#mobile-nav`) opens | selector miss | **Yes** |

---

## Coverage

### Viewports (Chromium, 6 representative pages)

320×568, 360×640, 375×667, 390×844, 412×915, 430×932, 480×800,  
768×1024, 820×1180, 834×1194, 1024×768,  
1280×720, 1366×768, 1440×900,  
1920×1080, 2560×1440, 3840×2160

**Pages:** home, AllExtensions hub, AIFoundation Installation, AIProviders, ExtNsT3AI, License

### Browsers

| Browser | Engine | Result |
|---------|--------|--------|
| Chrome | Chromium | Pass (matrix) |
| Edge | Chromium (same engine) | Covered by Chromium |
| Firefox | Playwright Firefox | Pass (home + install @ 390 / 1024 / 1920) |
| Safari | Playwright WebKit | Pass (same sample) |

---

## Issues found and fixed

1. **Card grid overflow at 320px**  
   Forced `repeat(2, minmax(9.5rem, 1fr))` exceeded narrow content width.  
   **Fix:** `minmax(0,1fr)` + **1-column** grid ≤480px.

2. **Top navbar overflow at 1024px**  
   Long labels + CTA + theme control exceeded width.  
   **Fix:** Compact navbar CSS (1024–1279) + shorter labels (`AI Extensions`, `Templates`, `Extensions`).

3. **Off-canvas `/llms.txt` link**  
   Mintlify injects a visible anchor at ~x=337 that tripped overflow audits.  
   **Fix:** Visually hide with accessible clip pattern (link remains in DOM).

4. **Breadcrumb bleed at 320px** (AI Providers)  
   “Configuration” crumb extended ~5px past viewport (no page scroll).  
   **Fix:** Ellipsis / wrap rules ≤360px.

5. **Touch targets**  
   Search / more-actions / theme controls enlarged to ≥44px hit area on ≤1023px.

6. **Global overflow safety**  
   `overflow-x: clip` on `html/body`; tables/code/images/embeds capped to `max-width: 100%` with intentional scroll on `pre` / tables.

---

## Live comparison (mobile)

| Page | Viewport | Mintlify | Live RTD |
|------|----------|----------|----------|
| Home | 390 | hOverflow 0, high 0 | hOverflow 0, high 0 |
| Install | 390 | hOverflow 0, high 0 | hOverflow 0, high 0 |
| Home | 320 | hOverflow 0, high 0 | hOverflow 0, high 0 |
| Install | 320 | **hOverflow 0, high 0** | hOverflow **15**, high **2** |

---

## Interactions (mobile)

| Viewport | Mobile nav `#mobile-nav` | Search modal |
|----------|--------------------------|--------------|
| 375 | Opens (dialog visible) | Fits (width ~343), ~400ms open |
| 390 | Opens | Fits (width ~358) |
| 430 | Opens | Fits |

---

## Artifacts

- `scripts/responsive-audit/responsive-audit.json` — baseline  
- `scripts/responsive-audit/responsive-audit-after.json` — post-fix  
- `custom.css` — `T3 RESPONSIVE HARDENING` + breadcrumb rules  
- `docs.json` — shortened navbar labels for mid-width top bar

---

## Notes

- Intentional horizontal scroll remains only inside **code blocks** and **wide tables** (by design).  
- Mobile nav drawer uses Mintlify’s `#mobile-nav` with a small negative bleed (`--bleed:3rem`); this is platform chrome, not content overflow (`scrollWidth === clientWidth`).  
- Local `mint dev` compile latency is unrelated to responsive layout quality; production CDN should be used for CWV sign-off.
