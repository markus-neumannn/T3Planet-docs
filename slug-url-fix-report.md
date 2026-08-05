# Slug & URL Fix Report

**Date:** 2026-06-25

## Summary

| Metric | Count |
|--------|-------|
| Total pages checked | 703 |
| Navigation slugs verified | 703 |
| docs.json nav hrefs fixed | 7 |
| t3-docs.js URL strategy | Strip `.html`, canonical clean routes |
| Markdown `.html` links pending strip | 0 |
| Redirect rules (legacy) | 1305 in docs.json |

## Changes Applied

1. **`docs.json`** — Navbar + footer + Get Started use `/Product/Index` (no `.html`).
2. **`_static/t3-docs.js`** — `cleanRoute()` strips `.html` from all internal links; `canonicalCleanUrl()` normalizes address bar.
3. **`scripts/strip_internal_links_html.py`** — Batch strip `.html` from markdown links.
4. **Redirects unchanged** — `.html` and `/en/latest/*` still redirect to canonical routes.

## Remaining Issues

- None.
