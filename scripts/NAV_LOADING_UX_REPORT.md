# Navigation Loading UX — Redesign Report

## 1. Root cause analysis

Mintlify’s SPA router (Next-style) **unmounts the current page content as soon as navigation starts**, often while the next route is still compiling (`Compiling…` in local `mint dev`). Our earlier top progress bar + delayed skeleton did not prevent that gap:

1. Click → content DOM cleared immediately  
2. Content column becomes empty white/dark surface  
3. Progress bar alone remains visible  
4. Skeleton (if any) appeared *after* the blank was already visible  

So the blank screen was not a missing loader — it was **content removal racing ahead of any overlay**.

## 2. Chosen transition strategy

**Freeze → adaptive overlay → crossfade release** (Linear/Vercel-style perceived continuity):

| Phase | Timing | Behavior |
|-------|--------|----------|
| Freeze | 0 ms (sync on click) | Clone `#content-area` / `#content` into `#t3-page-hold` over the content column |
| Progress | ≥ ~80 ms | Top NProgress-style bar (skipped on ultra-fast hops) |
| Skeleton | ≥ ~220 ms | `#t3-page-veil` crossfades over the frozen page |
| Release | When next content is ready | Wait for real content text/nodes + double `rAF`, fade hold out, soft enter on new content |

Header, sidebar, search, and theme controls stay mounted (only the content column is covered).

## 3. Loading state implementation

**Files**
- `_static/t3-docs.js` (+ rebuilt `_static/t3-docs.min.js`)
- `custom.css` (`T3 PERF: NAV PROGRESS + ROUTE VEIL`)

**Key pieces**
- `captureHold()` — synchronous DOM snapshot before Mintlify unmount  
- `contentLooksReady()` — release gate so we don’t uncover a blank shell  
- Adaptive timers + `prefers-reduced-motion`  
- `aria-busy` + polite live region (`#t3-nav-live`)  
- Existing hover/pointer prefetch retained (`PREFETCH_MAX=40`)

## 4. Performance impact

| Concern | Assessment |
|---------|------------|
| Clone cost | One content-tree clone per nav; discarded on release |
| Main thread | Sync clone on click is intentional (must beat unmount) |
| Paint | Hold/veil use `transform`/`opacity` (compositor-friendly) |
| CWV | No extra network; may improve CLS perception during hops |
| Memory | Hold HTML cleared after exit animation |

Local `mint dev` compile time is unchanged; **perceived** wait no longer shows blank chrome.

## 5. Cross-browser validation

Chromium re-validation after freeze fix (cache-busted assets):

| Metric | Result |
|--------|--------|
| `sidebarReady` / init | PASS |
| Hold on pointerdown | PASS (`holdLen` matched prior page ~2512 chars) |
| Skeleton on slow path | PASS (`saw_veil`) |
| Blank frames while busy | **0** |
| Held frames sampled | 103 / 106 |

Evidence: `scripts/qa-performance/screenshots-v2/nav-hold-*.png`, `scripts/qa-performance/nav-hold-validation.json`.

## 6. Before vs after

| Before | After |
|--------|-------|
| Content vanishes → blank white/dark | Previous page stays visible (frozen) |
| Only thin top bar | Bar + optional skeleton over freeze |
| Skeleton could flash alone | Skeleton only after ~220 ms slow path |
| Abrupt swap | Crossfade hold → new content + light enter |

## 7. Limitations & follow-ups

1. **Cannot keep the live React tree** — Mintlify owns routing; freeze is a snapshot (links in the hold are inert).  
2. **popstate** may race; we fall back to skeleton if freeze isn’t possible.  
3. **Clone fidelity** — complex widgets/iframes are neutralized in the hold.  
4. **CDN CWV** should still be measured post-deploy; local mint timings remain non-gating.  
5. Optional next step: route-type skeletons (hub vs article) for even closer layout match.

## Acceptance checklist

- [x] No intentional blank content column during nav  
- [x] Previous page preserved until next is ready (snapshot)  
- [x] Adaptive bar + skeleton  
- [x] Header/sidebar persistent  
- [x] Prefetch retained  
- [x] Reduced motion respected  
- [x] a11y busy/live announcements  

*Hard-refresh the preview (`Cmd+Shift+R`) to load the new `t3-docs.min.js` + `custom.css`.*
