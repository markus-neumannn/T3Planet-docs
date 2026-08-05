# Responsive Whitespace & Spacing Optimization Report

**Date:** 2026-08-04  
**Viewport:** 430×932 (iPhone 14 Pro Max emulation)

## Root cause analysis

| Issue | Cause | Impact |
|-------|--------|--------|
| Huge blank regions during/after load | `.t3-landing-section { content-visibility: auto; contain-intrinsic-size: auto 240px }` reserved empty height while Mintlify RSC hydrated | Looked like broken empty pages |
| Tall section chrome | Mobile `.t3-section-header { flex-direction: column }` stacked title + View all (~135px) | Extra scroll between sections |
| Low information density | Hero padding, Mintlify `py-5`/`my-2` cards, 5.5rem FAB bottom inset on landings | Half-viewport hero, sparse cards |
| “Invisible” gaps | White cards on white page + oversized shells | Screenshots read as empty whitespace |

## Spacing improvements

- Disabled `content-visibility` on landing/product sections  
- Section headers stay **row/wrap** on mobile  
- Mobile spacing scale (8–32px) for hero, cards, sections, CTA, MDX  
- Compact card padding (~0.75–0.95rem); removed outer card margins  
- Reduced landing bottom padding vs global FAB inset  

## Before → after (homepage @ 430px)

| Metric | Before | After |
|--------|--------|-------|
| Document scroll height | ~8273px | ~5528px (−33%) |
| Hero height | ~477px | ~386px |
| First card height | ~204px | ~113px |
| Hero → first card gap | ~24px+ | **16px** |
| Section header height | ~135px | ~88px |
| AI section block | ~1510px | ~717px |
| `content-visibility` | `auto` | `visible` |

## Artifacts

- After: `scripts/responsive-audit/whitespace-after-430.png`  
- Report screenshots also under Cursor assets `whitespace-after-430.png`

## Regression notes

- Desktop spacing rules unchanged outside `max-width: 1023px`  
- Docs page heading rhythm tightened only on mobile  
- FAB still clears content; landing pages use smaller bottom inset  

## Remaining recommendations

1. Consider moving homepage search into the header on ≤480px to reclaim ~48px in the hero.  
2. Restore/ensure `.t3-category-nav` renders above the hero if product still wants hub pills.  
3. Re-check production CDN after deploy (local `mint dev` RSC latency exaggerates empty shells).
