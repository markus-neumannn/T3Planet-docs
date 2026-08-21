# Loader Improvement Report

## Final Status

### LOADER IMPROVED — READY FOR REVIEW

## Current Loader Analysis

Custom loader in `scripts/src/t3-docs.js` + `scripts/src/custom.src.css`:

- Top progress bar `#t3-nav-progress`
- Opaque content hold + skeleton on raw mint `:3001` only
- Progress-only on cache proxy `:3000` / production-like SPA

Weaknesses addressed: heavy glow, short flicker threshold (50ms), blank hold flash, noisy screen-reader announces on fast hops, abrupt show/hide.

## Improvements Implemented

- 2px brand progress line with subtle shimmer (no heavy glow)
- 120ms show threshold (`PROGRESS_SHOW_MS`) to prevent fast-nav flicker
- Announce loading only when bar actually shows; skip complete announce on invisible hops
- Slow-path brand status (`t3-hold-status`) before skeleton on `:3001`
- Softened skeleton shimmer; dark-mode token `#6b9fff`
- `prefers-reduced-motion` covers new loader parts
- Hold remains `pointer-events: none` (no click steal)

## Files Changed

- `scripts/src/t3-docs.js`
- `scripts/src/custom.src.css`
- `_static/t3-docs.min.js` (built)
- `custom.css` (built)

## Testing Performed

- progress active after transition PASS
- nav Introduction PASS
- settled clean PASS
- nested AIProviders PASS
- dark token PASS
- mobile reduced-motion PASS
- 3001 Support PASS
- 3001 settled PASS
- back: PASS
- forward: PASS
- bf settled: PASS
- progress tablet: PASS
- progress desktop-wide: PASS
- progress mobile-narrow: PASS
- loader DOM ready: PASS

## Verdict

LOADER IMPROVED — READY FOR REVIEW
