# Product rename report — AI Foundation → T3AF

**Date:** 2026-08-05  
**Validation URL:** http://192.168.0.113:3000/AIFoundation/Index  
**Scope:** User-facing product branding only (page slugs / folder names unchanged)

---

## 1. Totals

| Metric | Count |
|--------|------:|
| Files scanned (md/mdx/json/js/css/html/yml/py/txt, excl. Live-docs/node_modules) | **~809** first pass + DE restore |
| Files updated with branding replacements | **108** (104 EN + generators, then **4** DE) |
| Branding replacements (`AI Foundation` → `T3AF`) | **670** (660 + 10 DE) |
| Remaining `AI Foundation` in published content (excl. `scripts/` audit archives) | **0** |
| Preserved `AIFoundation` path/slug token occurrences | **1272** (intentional) |

Also: product card tagline on AI Universe hub set to **Shared AI engine** (avoid redundant “T3AF / T3AF”).

---

## 2. Intentionally preserved technical identifiers

| Identifier | Why preserved |
|------------|---------------|
| Folder / URL slug `AIFoundation/` | Page slugs unchanged per requirements |
| Hub path `AIFoundationExtensions/` | Route / redirects |
| Extension key `ns_t3af` / `EXT:ns_t3af` | TYPO3 technical id |
| Composer package `nitsan/ns-t3af` | Package name |
| GitHub path `ns_t3af` | Repository name |
| Phrase “shared AI foundation” (lowercase descriptive English) | Not the product name |
| Historical files under `scripts/*` QA/audit JSON & old migration reports | Internal archives, not published (`.mintignore` excludes `scripts/`) |

---

## 3. What was updated

- All EN product docs under `AIFoundation/**`, child AI extensions (`ExtNsT3A*`), hubs (`AIFoundationExtensions`, etc.)
- `docs.json` sidebar group label: **AI Foundation** → **T3AF** (paths unchanged)
- Frontmatter titles, descriptions, keywords, iframe titles, breadcrumbs/path labels, FAQs, install steps
- DE mirrors restored from git and updated (`de/ExtNsT3AC`, `de/ExtNsT3AS`)
- Selected migration generators under `scripts/` that would re-emit old branding

---

## 4. Build status

| Check | Result |
|-------|--------|
| Local preview `:3000` / `:3001` | Up (LaunchAgent restarted after edits) |
| `mint validate` | **Exit 1** — **pre-existing** issues, not caused by this rename |

Known `mint validate` failures (unchanged by branding):

- `AIFoundation/Integrations/MCPTesting/Index.md` — invalid MDX around ``Bearer `<token>` ``
- `License/UpdateVersion/Composer/Index.md` — unquoted HTML attribute parse
- `ExtNsRevolutionSlider/.../Installation` & `MigrationFrom3toLatest` — same class of HTML parse warnings

---

## 5. QA results (Playwright on local preview)

| Page | Old branding | Shows T3AF | Status |
|------|--------------|------------|--------|
| `/AIFoundation/Index` | No | Yes (title/H1 **T3AF**) | PASS |
| `/AIFoundation/Introduction/Index` | No | Yes | PASS |
| `/AIFoundationExtensions/Index` | No | Yes | PASS |
| `/ExtNsT3AI/Installation/Index` | No | Yes | PASS |
| `/` (home) | No | Yes | PASS |

Artifacts: `scripts/qa-final/t3af-rename-*.png`, `scripts/qa-final/t3af-rename-qa.json`

---

## 6. Responsive testing (`/AIFoundation/Index`)

| Viewport | Overflow-X | H1 |
|----------|------------|-----|
| Desktop 1440 | No | T3AF |
| Tablet 768 | No | T3AF |
| Mobile 390 | No | T3AF |

---

## 7. Remaining issues

1. **Hosted search index** still empty until Mintlify deploy of this content — local search may not list “T3AF” from cloud index yet.
2. **`mint validate` pre-existing MDX/HTML parse errors** (MCPTesting, License Composer, Revolution Slider) — separate cleanup.
3. Historical **`scripts/`** audit reports still mention “AI Foundation” (not published).
4. **Production cutover** still blocked by hosted Mintlify deploy (unchanged from prior readiness verdict).

---

## 8. Production readiness status (rename scope)

| Question | Answer |
|----------|--------|
| User-facing **AI Foundation** → **T3AF** complete on published docs? | **Yes** |
| Slugs / extension keys intact? | **Yes** |
| Local preview branding verified? | **Yes** |
| Ready for **production cutover** of the whole docs site? | **No** — still needs Mintlify hosted deploy + search index + prior blockers |

**Rename success criteria:** met for branding.  
**Site-wide production ready:** still **Not Production Ready** pending hosted deploy (see `scripts/PRODUCTION_READINESS_FINAL.md`).
