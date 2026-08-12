# Live vs Mintlify Remigration — Completion Report (August 12, 2026)

**Generated:** 2026-08-12  
**Live source:** https://docs.t3planet.de/en/latest/  
**Sphinx fallback:** Rebuilt from T3Planet Docs Agent (`python3 -m sphinx -b html`)  
**Mintlify repo:** `/Users/nitsan/www/AI Agents/Mintilify Doc`

## 1. Totals

| Metric | Count |
|--------|-------|
| Live pages checked | **750** |
| Mintlify `.md` files | **919** |
| Pages MATCH (content aligned) | **296** |
| STRUCTURAL_DIFFERENCE (intentional hubs/CardGroups) | **82** |
| LINK_DIFFERENCE (nav/toctree vs Mintlify href format) | **371** |
| UPDATED (code block deltas) | **6** |
| MISSING_CONTENT after migration | **0** |
| NEW_PAGE on live | **0** |
| MEDIA_DIFFERENCE after migration | **0** |
| fetch_failed | **0** |

## 2. Pages updated (surgical merge)

18 pages migrated via `reconcile_migrate_from_live.py` plus manual heading fix on `ExtNsT3AI/SEO/Index.md`:

- `EXTKarma/Customization/Index`
- `EXTReva/CustomElements/Index`
- `ExtNitsanHellobar/Introduction/Index`
- `ExtNitsanMaintenance/Introduction/Index`
- `ExtNsFriendlyCaptcha/Configuration/Index`
- `ExtNsGoogleSiteKit/Introduction/Index`
- `ExtNsSocialLogin/Configuration/Index`
- `ExtNsT3AA/Installation/Index`
- `ExtNsT3AI/AISettings/Index`
- `ExtNsT3AI/Installation/Index`
- `ExtNsT3AI/Prompts/Index`
- `ExtNsT3AI/SEO/Index`
- `ExtNsT3AS/Configuration/Index`
- `ExtNsWhatsapp/Installation/Index`
- `ExtRTECKEditorPack/PremiumPack/Index`
- `License/GenerateLicenseKey/Index`
- `License/LicenseActivation/Index`
- `License/Migration/License/Index`

## 3. New pages created

**0** — Live `objects.inv` (750 pages) had no pages missing from Mintlify file tree.

**Note:** `ExtNsT3AA/AccessibilityWidgets` exists in local Sphinx HTML but returns **404** on live RTD and is **not** in live `objects.inv`. Not migrated (live is source of truth).

## 4. Images / media

- **2** pages received image assets during migration (`EXTReva/CustomElements`, `ExtNsSocialLogin/Configuration`)
- **0** missing Supademo embeds after migration
- **0** MEDIA_DIFFERENCE flags in final audit

## 5. Links

- **371** pages flagged `LINK_DIFFERENCE` — predominantly Sphinx toctree/sidebar relative links on live HTML vs Mintlify `/Product/Page/Index` CardGroup hrefs. Content body links were not bulk-replaced to avoid breaking Mintlify navigation improvements.
- Redirects in `docs.json` remain for `/T3AF/*` → `/ExtNsT3AF/*` and EXTKarma slug aliases.

## 6. Code / configuration updates

- Migrated missing sections included updated installation notes (AI Foundation provider modes), T3AS training CLI options, License backend flows, RTE Premium WebSocket config, and Friendly Captcha local testing.
- **6** pages retain minor code-block text normalization differences (`UPDATED`); content is present, formatting differs slightly.

## 7. Navigation changes

**0** new nav entries — no new live pages were created.

## 8. Tooling added/updated

| File | Purpose |
|------|---------|
| `scripts/qa-final/live_content_reconcile_aug12.py` | Deep section/code/link/image/Supademo audit |
| `scripts/qa-final/reconcile_migrate_from_live.py` | Surgical merge migrator |
| `scripts/migrate_from_live.py` | `ExtNsT3AF` canonical paths + `--merge` mode |
| `scripts/qa-final/objects.inv` | Fresh fetch from live RTD |

## 9. Validation

- **Second-pass audit:** `MISSING_CONTENT=0`, `NEW_PAGE=0`, `MEDIA_DIFFERENCE=0`, `fetch_failed=0`
- **`mint validate`:** Not run — local Node v26 incompatible with Mintlify CLI (requires LTS). Use Node 20/22 for local validate.
- **Git diff:** Documentation `.md` updates + tooling; no unrelated source-code changes intended from this migration batch.

## 10. Manual review (optional)

| Item | Reason |
|------|--------|
| `LINK_DIFFERENCE` (371 pages) | Mostly hub/toctree link format; not content gaps |
| `UPDATED` (6 pages) | Code fence normalization only |
| `ExtNsT3AA/AccessibilityWidgets` | In Sphinx source only; not on live RTD yet |
| `STRUCTURAL_DIFFERENCE` (82 hubs) | Intentional Mintlify CardGroup landings |

## Reports

- [`LIVE_CONTENT_RECONCILE_AUG12.json`](LIVE_CONTENT_RECONCILE_AUG12.json)
- [`LIVE_CONTENT_RECONCILE_AUG12.md`](LIVE_CONTENT_RECONCILE_AUG12.md)
- [`LIVE_CONTENT_MIGRATION_AUG12.json`](LIVE_CONTENT_MIGRATION_AUG12.json)
- [`LIVE_CONTENT_MIGRATION_AUG12.md`](LIVE_CONTENT_MIGRATION_AUG12.md)
