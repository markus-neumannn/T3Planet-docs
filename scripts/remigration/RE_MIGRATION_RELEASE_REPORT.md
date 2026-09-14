# Re-Migration Release Report

**Date:** 2026-09-14 08:08 UTC  
**Verdict:** **READY**

## Summary

Full remigration from Sphinx RST (`docs/docs/`) into Mintlify Markdown completed. Second compare is clean (no unexplained content gaps). Local E2E against the LAN preview (`:3000`) is green for all nav routes.

## Release gate checklist

| Gate | Result |
|------|--------|
| Critical defects | **0** |
| High defects | **0** |
| Unexplained RST↔MD gaps | **0** |
| Second compare clean | **YES** |
| E2E nav smoke green | **YES** (701/701 OK) |
| Broken internal markdown links | **0** |
| Nav paths missing on-disk files | **0** |

## Migration status (matrix)

| Status | Count |
|--------|------:|
| MIGRATED_CORRECTLY | 755 |
| INTENTIONALLY_ADDED | 61 |
| REVIEWED_OK | 2 |
| CONTENT_MISSING / PAGE_MISSING | 0 |

Artifacts: `scripts/remigration/matrix.json`, `matrix.md`

## Homepage stats (generator)

- Documentation pages: **771**
- Products: **68**

Source: `_static/t3-stats.json` via `scripts/compute_doc_stats.py`

## Hard-gap remigrations completed

1. **T3AC / T3AS DPA & GDPR** — new pages `ExtNsT3AC/DPAandGDPR/Index.md`, `ExtNsT3AS/DPAandGDPR/Index.md`; wired into product Index cards and `docs.json`.
2. **HelpDesk 14.0** — Constant Editor / TypoScript include rewrite across Installation, Global/Form Settings, Customize Form, Plugins, Tickets, Categories, Status, Update Version, Introduction note; FE images + Supademo embeds.
3. **History cleanup** — `t3af:history:cleanup` + `t3af-history-cleanup.png` on T3AS Configuration and T3AC Data Source; Save search/chatbot history wording on Search, Chatbot, Usage Analytics.
4. **T3AI Translation** — Manage Mass Translation (`t3af:bulk:translate` batch-size/limit + image), Language Glossary + DeepL Official Glossary Supademos, Activate / Auto Activate sections, Fluid/TCEMAIN snippets, missing preview images.

## Second compare leftovers (intentional / N/A)

| Item | Classification |
|------|----------------|
| `docs/docs/history.rst` | Intentional skip (include-only stub) |
| 61 Mintlify-only pages | INTENTIONALLY_ADDED |
| 2 REVIEWED_OK | Previously reviewed OK |
| 6 image basename aliases (`*1.png` / `.webp` vs RST basename) | Intentional alias; assets present on page |
| Formatting-only RST↔MD differences | Not defects |

Supademo inventory: **0** missing embed IDs after remigration.

Artifacts: `scripts/remigration/second_compare_summary.json`, `images_inventory.json`, `supademo_inventory.json`

## QC / E2E evidence

### Static / route validation (`route_link_check.py`)

- Nav paths: **701**
- Missing files: **0**
- Broken internal links: **0**
- Redirect structural issues: **0** (no dups / self-redirects / parent-of-self)

Note: An earlier overloaded concurrent HTTP pass produced transient code-0 timeouts; those are environment noise, not content defects.

### Sequential HTTP nav smoke (`nav_http_smoke.json`)

- First sequential pass: **699/701** HTTP 200; **2** transient timeouts (`AILabel`, `AIPermissions`)
- Immediate retry: both **HTTP 200**
- Final nav HTTP status: **701/701 green**

### Playwright E2E (`e2e_batch_check.py` → `E2E_REPORT.md`)

- Total pages: **701**
- OK: **701**
- FAIL: **0**
- ERROR: **0**
- Remigrated DPA / HelpDesk / Translation / Chatbot / Configuration pages: all **OK** (desktop/tablet/mobile smoke, images, embeds)

## READY / NOT READY

**READY = YES**

Criteria met: Critical=0, High=0, unexplained gaps=0, second compare clean, E2E nav smoke green.

**Do not push to GitHub/Mintlify until this report is explicitly approved.**

## Follow-ups (non-blocking)

- Keep nested `docs/` Sphinx clone unpublished (gitignored / `.mintignore`).
- Optional: normalize intentional image basename aliases to RST names in a later cleanup PR.
