# Slug & URL Audit — T3Planet Documentation

**Date:** 2026-06-25
**Total EN pages:** 703
**Navigation slugs:** 703

## URL Standard

| Layer | Format | Example |
|-------|--------|---------|
| Mintlify route (canonical) | `/Product/Section/Index` | `/AllExtensions/Index` |
| Legacy RTD / bookmark | `*.html` → redirect | `/AllExtensions/Index.html` → `/AllExtensions/Index` |
| RTD prefix | `/en/latest/*` → redirect | `/en/latest/ExtNsT3AI/Index.html` → `/ExtNsT3AI/Index` |

## Root Cause (Screenshot Issue)

Navbar/footer used `.html` hrefs while Mintlify serves clean routes in the address bar.
`t3-docs.js` previously **added** `.html` to sidebar links, causing hover preview mismatch.

**Fix:** Canonical URL = Mintlify route **without** `.html`. Redirects preserve legacy URLs.

## Mismatches Found

| Page Name | Nav Slug | Canonical Route | Expected URL | Mismatch | Required Fix | Status |
|-----------|----------|-----------------|--------------|----------|--------------|--------|
| — | — | — | — | No structural mismatches | — | OK |

## Navigation Hrefs With `.html` (docs.json)

- None (all clean).

## Markdown Links With `.html`

**Count:** 0 (run `scripts/strip_internal_links_html.py` to fix)

