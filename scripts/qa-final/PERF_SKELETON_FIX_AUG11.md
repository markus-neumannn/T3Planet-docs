# Performance / Skeleton Fix — Aug 11, 2026

## Problem
`/ExtNsT3AF/Configuration/Dashboard/Index` showed a permanent skeleton UI.
Root cause: cache proxy served a **truncated HTML HIT** (~118 KB, no `<title>`, no page body). Full mint response is ~730 KB.

## Fixes
1. **`scripts/mint_cache_proxy.py`**
   - `_complete_enough()` — refuse to cache incomplete HTML shells
   - `/__t3_cache_purge` endpoint
   - Expanded `WARM_PATHS` (25 hubs including Dashboard)
2. **`scripts/src/t3-docs.js`**
   - Safety timer: clear hold/skeleton after 12s if stuck
3. Rebuilt `_static/t3-docs.min.js` + restarted LaunchAgent (cleared bad memory cache)

## After
| Check | Result |
|-------|--------|
| Dashboard STORE | 200, ~730 KB, title + Purpose present (~4s cold) |
| Dashboard HIT | 200, ~3 ms, full content |
| LAN | http://192.168.0.117:3000/ExtNsT3AF/Configuration/Dashboard/Index → 200 |

Hard-refresh the browser (Cmd+Shift+R) if an old broken response was cached by the browser.
