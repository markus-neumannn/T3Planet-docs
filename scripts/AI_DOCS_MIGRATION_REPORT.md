# AI Documentation Migration Report

**Source of truth:** https://docs.t3planet.de/en/latest/  
**Scope completed:** AI products — T3AF, T3AI, T3AC, T3AS, T3AA  
**Date:** 2026-07-13

## Documentation Audit Summary

| Metric | Count |
|--------|------:|
| Live AI product pages scanned | 123 |
| Mintlify AI pages before | 97 |
| Missing pages before | 24 |
| Missing pages after | 0 |
| New T3AF pages migrated | 16 |
| Other new pages (ReInstall/UpdateGuide) | 5 |
| Major pages resynced from live | 25+ |
| `mint validate` | PASSED |

## Product-wise Summary

### T3AF (AI Foundation)
- **New pages:** Architecture, Usage, Troubleshooting, Privacy, Release Notes, T3Planet Credits QA, MCP Testing, Developer Guide (+ 8 child pages)
- **Updated:** All existing AI Foundation module/guide pages synced from live `ExtNsT3AF`
- **Navigation:** `docs.json` updated to match live TOC order
- **Remaining:** Live Release Notes is still a stub; full non-AI site parity not in this pass

### T3AI
- **New:** ReInstallEverything, UpdateGuide
- **Updated:** Installation (AI Foundation steps), SEO, Prompts
- **Remaining:** Minor heading-label diffs vs frontmatter titles

### T3AC
- **New:** ReInstallEverything
- **Updated:** Installation, Configuration, FeatureGuide DataSource & Chatbot
- **Remaining:** Prerequisites page already present under `&` path

### T3AS
- **New:** ReInstallEverything
- **Updated:** Installation, Configuration, FrontendPlugin
- **Remaining:** Prerequisites page already present under `&` path

### T3AA
- **New:** ReInstallEverything
- **Updated:** Installation, Configuration, AIFilemeta, T3AAVoiceover
- **Remaining:** Minor heading-label diffs

## Final Verification Checklist

- [x] All live AI product pages exist in Mintlify (mapped BuyNow→GetThisExtension, AIPermissions→GovernanceAndAccess)
- [x] Missing AI Foundation developer/ops docs migrated
- [x] Navigation updated for new pages
- [x] Mintlify documentation builds successfully (`mint validate`)
- [ ] Full-site (templates/extensions beyond AI) parity — **not completed in this pass**
- [ ] Exhaustive broken-link crawl after migration — recommended follow-up

## Notes

- Live path for AI Foundation is `ExtNsT3AF/` → Mintlify folder `AIFoundation/`
- MDX required escaping of `{ }` / placeholders / `<?php` outside protected JSX on migrated pages
