# Icon / Text Spacing Report

## Final Status

### RESPONSIVE ICON AND TEXT SPACING IMPROVED — READY FOR REVIEW

## 1. Issue Identified
On responsive view, Mintlify Card icons sat flush against titles (0px gap). Mobile density CSS had set card title `margin: 0 0 0.35rem`, collapsing Mintlify’s default `mt-4` under the icon.

## 2. Implementation
- Restored spacing via sibling rule: `[data-component-part="card-icon"] + .w-full` → `margin-top: 0.65–0.75rem`
- Applies to landing/hub/template cards site-wide
- Reinforced mobile nav/sidebar `column-gap` and common inline-flex icon rows
- Desktop unchanged in structure; same breathing room (~10.4px measured)

## 3. Files Changed
- `scripts/src/custom.src.css`
- `custom.css` (built)

## 4. Testing Completed
- EXTBootstrap, ExtNsT3AF, Home cards
- Viewports: 320, 375, 440, 768, 1440
- Light + dark
- Measured icon→title gap: **10.4px** (was **0px**)
