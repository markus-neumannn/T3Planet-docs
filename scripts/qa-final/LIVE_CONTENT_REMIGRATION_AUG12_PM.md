# Live vs Mintlify Remigration — August 12 PM (2026)

**Generated:** 2026-08-12T12:10:05.562735+00:00
**Live source:** https://docs.t3planet.de/en/latest/ (388 pages fetched live; Sphinx fallback for remainder after Cloudflare 429)
**Sphinx rebuild:** refreshed before audit

## Summary

| Metric | Count |
|--------|-------|
| Live pages checked | **751** |
| Mintlify `.md` files | **921** |
| MATCH | **298** |
| NEW_PAGE (after migration) | **0** |
| MISSING_CONTENT | **0** |
| MEDIA_DIFFERENCE | **0** |
| UPDATED (code fence format only) | **5** |
| STRUCTURAL_DIFFERENCE (hubs) | **82** |
| LINK_DIFFERENCE (toctree vs Card href format) | **371** |
| fetch_failed | **0** |

## Migrated this pass

### New page
- `ExtNsT3AA/AccessibilityWidgets/Index` — created from live/Sphinx, Supademo included
- Added to `docs.json` navigation (after Configuration)
- Added Card on `ExtNsT3AA/Index.md` landing

### Full-body remigrated (Installation + DataSource)
- `ExtNsT3AA/Installation/Index`
- `ExtNsT3AC/Installation/Index`
- `ExtNsT3AI/Installation/Index`
- `ExtNsT3AS/Installation/Index`
- `ExtNsT3AC/FeatureGuide/DataSource/Index` (includes `nst3af:training` CLI)

### Kept (already denser / current)
- `ExtNsT3AF/Integrations/MCPTesting/Index`

## Remaining review notes
- **UPDATED (5):** composer/`only` JSON and MCP curl snippets exist in Mintlify; audit flags whitespace/line-break differences vs Sphinx HTML extraction — not missing content.
- **LINK_DIFFERENCE (371):** Sphinx toctree relative links vs Mintlify absolute CardGroup hrefs — intentional structural difference.
- **STRUCTURAL_DIFFERENCE (82):** Mintlify hub/landing CardGroups vs live prose index pages — preserved on purpose.

## Validation
- Second-pass audit: NEW_PAGE=0, MISSING_CONTENT=0, MEDIA_DIFFERENCE=0
- AccessibilityWidgets status: MATCH
