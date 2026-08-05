# Search activation status (2026-08-05)

## Done
- CLI logged in as `dhruv.rathod@mail.nitsan.ai` (org: Nitsan)
- Local preview no longer shows "Run mint login…"
- Search modal opens (⌘K) and calls `/_mintlify/api-public/search/<subdomain>` → HTTP 200

## Result of functional test
- Queries tested: `T3AI`, `License` on `:3001` and `:3000`
- UI shows **Results: 0** (only “Ask Assistant…” suggestion)
- API body: `{"results":[]}`

## Root cause
Mintlify local search uses the **cloud search index of the linked deployment**, not local MD files.

Linked hosted deployments are still Mintlify starter kits (no T3Planet content):
- https://t3planet.mintlify.app → “Mintlify Starter Kit”
- https://nitsan-81630f36.mintlify.app → “Mintlify Starter Kit”

So search is *activated* but the index has nothing from this docs repo.

## Unblock real search results
1. In [Mintlify Dashboard](https://dashboard.mintlify.com): open project `t3planet` (or create one)
2. Connect this GitHub repo and deploy the docs (push to the linked branch)
3. Wait for Mintlify to build + index
4. Re-run local `mint dev` / LaunchAgent and retest ⌘K for `T3AI` / `License`

Until that deploy+index exists, local search will stay at Results: 0.

## Note on subdomain
- CLI project that works for this login: `nitsan-81630f36` (search API 200, empty index)
- `t3planet` local search currently returns 404 `Deployment "t3planet" not found` for this account session; hosted starter still exists at https://t3planet.mintlify.app
