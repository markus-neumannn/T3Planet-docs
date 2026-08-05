# Drawer × Loading Skeleton Overlap Fix — Aug 2026

## Root cause

Three stacking conflicts during `t3-holding` (page skeleton) + open hamburger:

1. **`#t3-page-hold` and Mintlify drawer both used `z-index: 40`** — skeleton and drawer competed in the same layer.
2. **Close control was fixed at the top-left of the viewport** — sat on the navbar T3PLANET logo (looked like X overlapping the brand).
3. **Navbar + Navigation strip stayed interactive/visible** while the drawer chrome (logo + theme pill) also rendered → dual-header appearance.
4. **Global 44×44 touch rule** inflated `.t3-drawer-close`, so on narrow gutters the X spilled into the drawer.

## Solution

| Change | File |
|--------|------|
| Hide page-hold while drawer open; raise drawer shell to z-80/81; close at z-90 | `custom.css` |
| Hide navbar row + hamburger strip while drawer open | `custom.css` |
| Position close button in the left gutter beside the right drawer (JS) | `_static/t3-docs.js` → `t3-docs.min.js` |
| Exclude drawer-close from forced 44px mins; size to gutter | `custom.css` + JS |
| Phone drawer width leaves ≥3rem gutter | `custom.css` |

## Validation (hold + drawer open)

| Viewport | Hold hidden | Navbar hidden | Close clear of drawer/logo |
|----------|-------------|---------------|----------------------------|
| 320 | ✓ | ✓ | ✓ |
| 390 | ✓ | ✓ | ✓ |
| 430 | ✓ | ✓ | ✓ |
| 681 | ✓ | ✓ | ✓ |

Screenshots: `scripts/responsive-audit/enterprise-2026-08/drawer-hold-ok-*.png`

## Notes

Hard-refresh after deploy so `custom.css` and `t3-docs.min.js` are not cached.
