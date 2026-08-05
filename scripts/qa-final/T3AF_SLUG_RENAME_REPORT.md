# Slug rename — AIFoundation → T3AF

**Date:** 2026-08-05

## Change
- Folder: `AIFoundation/` → `T3AF/` (and `de/AIFoundation/` → `de/T3AF/`)
- Canonical URL: `/T3AF/Index` (was `/AIFoundation/Index`)
- Hub slug `AIFoundationExtensions/` **unchanged**

## Updates
- `docs.json` navigation roots/pages → `T3AF/...`
- Internal links across docs → `/T3AF/...`
- Redirects added: `/AIFoundation`, `/AIFoundation/Index`, `/AIFoundation/:path*`, `.html` variants, and `/de/AIFoundation...` → `/T3AF/...`
- Client redirects in `scripts/src/t3-docs.js` + rebuilt `_static/t3-docs.min.js`

## QA
| Check | Result |
|-------|--------|
| `/T3AF/Index` renders H1 **T3AF** | PASS |
| `/AIFoundation/Index` → `/T3AF/Index` | PASS |
| `/AIFoundation/Introduction/Index` → `/T3AF/Introduction/...` | PASS |
| AI Universe hub card → `/T3AF/Index` | PASS |

Artifacts: `scripts/qa-final/t3af-slug-*.png`, `scripts/qa-final/t3af-slug-qa.json`

## Use this URL
http://192.168.0.113:3000/T3AF/Index
