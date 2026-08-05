# Production → Mintlify sync report

**Date:** 2026-07-27  
**Source of truth:** https://docs.t3planet.de/en/latest/  
**Validate:** `mint validate` — **passed**

## Summary

| Check | Result |
| --- | --- |
| Live crawl (prior inventory) | 730 pages, 0 crawl errors |
| Gaps after restructure | 21 missing → **0 remaining** |
| AI Foundation live pages | **31 / 31** present |
| Mintlify build | **validation passed** |

## AI Foundation (`ExtNsT3AF` → `AIFoundation`)

Production restructured T3AF. Mintlify now mirrors the live tree:

- Introduction, Installation
- **Configuration/** — Dashboard, AI Providers, AI Context, AI Prompts, AI Features, AI Usage & Logs, AI Permissions
- **Integrations/** — MCP Server, MCP Tools, MCP Testing
- **User Guide/** — Roles and Daily Use
- **Developer Guide/** — Architecture, Extension Integration, Custom Providers, Custom Prompt Catalogs, Custom Feature Cards, Feature Provider Overrides, Custom MCP Tools, Custom Access Catalogs
- **Troubleshooting/** — Known Problems, FAQ
- Helpful Links, Support

`docs.json` AI Foundation navigation was rebuilt to match this live TOC (obsolete flat nav entries removed).

Landing `AIFoundation/Index.md` restored as Mintlify product landing (live Index is TOC-only).

## Other gaps closed

- `ExtNsFriendlyCaptcha/FAQ`
- `ExtNsT3AS/BasicAuthentication`

## Artifacts

- `scripts/full-live-parity-audit.json` — initial full-site audit
- `scripts/full-live-parity-audit-after.json` — 21/21 gaps resolved
- `scripts/af-live-parity-after.json` — T3AF 31/31

## Notes / remaining scope

- Existence parity for the former 21 gaps is complete; older Mintlify-only AI Foundation pages (e.g. flat `WhatDoesItDo`, `Screenshots`) remain on disk but are **out of navigation** because they are gone from production.
- Broader product-by-product deep content/image diffs beyond the gap list were not re-certified in this pass.
- Prefer nested paths under `Configuration/` and `Integrations/` for all new links.
