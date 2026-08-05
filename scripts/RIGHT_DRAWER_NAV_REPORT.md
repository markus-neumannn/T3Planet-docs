# Right-Side Mobile/Tablet Drawer — Implementation Report

**Date:** 2026-08-04

## Root cause
Mintlify’s `#mobile-nav` mounts in a shell with `justify-start` and `data-swipe-direction="left"`, so the panel always opened from the left (negative `translateX` entrance).

## Solution
1. **Dock right** — wrapper `justify-content: flex-end` + forced `data-swipe-direction="right"`.
2. **Enter/exit animation** — override left-entry with `translate3d(104% → 0)` open and reverse close.
3. **Close UX** — backdrop tap, ESC, swipe-right-to-close, close control in the left backdrop gap.
4. **Visual polish** — rounded left corners, left-edge shadow, backdrop blur, 44px+ touch rows, active leading bar.
5. **Widths** — phones leave a ~60px content gap; tablets ~350–400px panel.

## Validation (Chromium)
| Viewport | Docked right | Reopen stable | Overflow | Close clear of drawer |
|----------|--------------|---------------|----------|------------------------|
| 390×844  | Yes | Yes | 0 | Yes |
| 768×1024 | Yes | Yes | 0 | Yes |
| 820×1180 | Yes | Yes | 0 | Yes |

## Files
- `custom.css`
- `_static/t3-docs.js` → `t3-docs.min.js`
