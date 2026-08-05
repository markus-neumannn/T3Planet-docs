# Full Live → Mintlify Re-Audit

**Date:** 2026-07-27  
**Workspace:** `/Users/nitsan/www/AI Agents/Mintilify Doc`  
**Source of truth:** https://docs.t3planet.de/en/latest/  
**Verdict:** **PASS**

## Scope

- Live inventory: Sphinx `searchindex.js` → **741** content pages  
- Excluded non-product Sphinx pages: `history`, `readme`, `genindex`, `search`  
- Compared every mapped page for: word volume, headings, images, callouts, code blocks, tables  
- Global EN checks: broken local image paths, AI Foundation nav parity  

## Pre-fix findings (22 defects / 17 pages)

| Kind | Count |
| --- | --- |
| heading | 8 |
| admon (callouts) | 6 |
| image_missing | 5 |
| code | 2 |
| thin | 1 |

Pages resynced from live include Avatar/Karma/Bootstrap customization & upgrade guides, Event plugin pages, FriendlyCaptcha, HelpDesk, News Advanced Search, Personio, T3AB, T3AL XLIFF, T3AS Verify Indexed Data, Timeline, Themes upgrade, Backup schedule, and others. See `scripts/full-reaudit-pre.json`.

## Post-fix verification

| Check | Result |
| --- | --- |
| Existence parity | **741 / 741** |
| Missing pages | **0** |
| Content/heading/image/callout/code/table defects | **0** |
| Broken local EN images | **0** |
| AI Foundation nav gaps | **0** |
| Thin pages remaining | **0** |

Artifacts:

- `scripts/full-reaudit-pre.json` — defects before migration  
- `scripts/full-reaudit-report.json` — final PASS report  

## Notes

- Mintlify landing heroes are kept when live Index pages are TOC-only.  
- Image parity treats webp conversions and Sphinx size-suffixed filenames as equivalents when the asset exists.  
- Code fences indented inside lists are counted correctly.
