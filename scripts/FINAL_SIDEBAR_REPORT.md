# T3Planet Docs — Unified Sidebar Redesign Report

**Date:** June 2026  
**Reference:** [Coinbase CDP Docs](https://docs.cdp.coinbase.com/)  
**Status:** Production-ready

---

## Summary

Replaced the multi-dropdown Mintlify navigation with a **single Coinbase-style hierarchical sidebar**:

| Section | Contents |
|---------|----------|
| **Home** | index, AI Foundation hub, Templates hub, Extensions hub |
| **Get Started** | License & Installation (nested) |
| **AI Foundation** | T3AI, T3AC, T3AS, T3AL, T3AA, T3AB (each with full doc tree) |
| **T3 Templates & Themes** | 9 themes (Karma, Bootstrap, Shop, Ayu, etc.) |
| **TYPO3 Extensions** | 52 extensions (Help Desk, FAQ, Revolution Slider, etc.) |

---

## Removed (per requirements)

- [x] Product dropdown selector (drag-and-drop field)
- [x] Sidebar search box
- [x] Sidebar filter input
- [x] Bottom EN/DE language switcher
- [x] Browse dropdowns (All Extensions, All AI, All Templates)

Search remains in the **top navbar** (`⌘K`). Language switching remains in the **navbar language selector**.

---

## Icons

- [x] **1,406 pages** — `icon` added to frontmatter via `scripts/add_nav_icons.py`
- [x] **All product groups** — icons in `docs.json` (`sparkles`, `puzzle`, `palette`, etc.)
- [x] **Nested feature sections** — icons on FeatureGuide, Updates, Migration groups

---

## Configuration (single source of truth)

| File | Purpose |
|------|---------|
| `scripts/build_unified_sidebar.py` | Generates `docs.json` navigation groups from product catalog |
| `scripts/_nav_dropdowns_backup.json` | Source dropdown archive for rebuilds |
| `scripts/add_nav_icons.py` | Adds page-level Lucide icons to MD frontmatter |
| `sidebar-nav.js` | Active state, expand/collapse persistence, mobile drawer, keyboard nav |
| `custom.css` | Coinbase-style sidebar UI, hides legacy controls |

Regenerate navigation:

```bash
python3 scripts/build_unified_sidebar.py
python3 scripts/add_nav_icons.py   # after new pages added
mint validate
```

---

## QA Checklist

| Test | Result |
|------|--------|
| `mint validate` | PASS |
| Broken internal links | 0 |
| Missing nav targets | 0 |
| Nav pages covered | 1,406 |
| Desktop sidebar structure | PASS |
| Dark mode sidebar | PASS |
| Mobile drawer | PASS |
| No sidebar search/filter/footer/dropdown | PASS |
| Product page routes (sample) | PASS |
| Active page highlight | PASS |

---

## End-client & marketing review

- **Clarity:** Products grouped by category (AI / Templates / Extensions) — no mixing
- **Discovery:** All 66 products visible in one scrollable tree
- **Premium feel:** Rounded active states, section dividers, consistent icons
- **Trust:** Professional labels (T3AI not EXT:ns_t3ai), clean spacing

---

## Preview

```bash
mint dev --port 3333
# http://localhost:3333
```

Hard-refresh (`Cmd+Shift+R`) after changes.
