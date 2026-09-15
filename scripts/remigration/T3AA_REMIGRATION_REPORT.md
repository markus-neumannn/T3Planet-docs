# T3AA Live Documentation Re-Migration Report

**Date:** 2026-09-15  
**Source:** GitLab `t3terminal/docs` @ `e47886ae` (local `docs/` clone)  
**Target:** Mintlify `ExtNsT3AA/`  
**Scope:** T3AA only (controlled remigration; no unrelated extension overwrites)

## Migration Summary

Only one T3AA-relevant change existed between the previous remigration baseline and current GitLab master: commit **e47886ae** added a new **DPA & GDPR** page for T3AA and linked it from the product index.

Earlier T3AA feature work from **cd0440f4** (Accessibility Widgets / Installation / Index) was already present in Mintlify and was **not** overwritten.

## Previous migration baseline

- Nested Sphinx clone HEAD before this pass: already at `e47886ae` (up to date with GitLab master).
- Prior full Mintlify remigration had covered post-`062c31cc` deltas for HelpDesk / T3AC / T3AS / T3AI Translation, but **T3AA DPA did not exist yet** until `e47886ae` (Sep 14, 2026).
- Reasonable baseline for T3AA: content as of last Mintlify sync; **new** delta = `e47886ae` T3AA files only.

## GitLab Commits Reviewed

| Commit | Title | T3AA relevant? | Action |
|--------|-------|----------------|--------|
| `e47886ae` | Added DPA section in all AI extensions | **Yes** (new `DPAandGDPR`, Index toctree) | Migrated |
| `cd0440f4` | T3AA New feature Doc update | Yes historically | **Already migrated** — verified key phrases/Supademo present |
| `138e4c8f` / `13c794f9` | T3AI docs | No | Skipped |
| `fd8c57df` | ns_helpdesk | No | Skipped |
| `f8cb24c4` / `56be4009` / `d0930dc1` | T3AC/T3AS DPA/history | Shared AI family; T3AC/T3AS already migrated earlier | Skipped in this T3AA pass |
| Other listed commits | T3AF/Karma/License/etc. | No for T3AA | Skipped |

## Change map (T3AA)

| Path | Classification | Notes |
|------|----------------|-------|
| `ExtNsT3AA/DPAandGDPR/Index` | **NEW** | Created Mintlify MD from live RST |
| `ExtNsT3AA/Index` | **MODIFIED** | Added DPA & GDPR card |
| `docs.json` AI Accessibility nav | **MODIFIED** | Inserted `ExtNsT3AA/DPAandGDPR/Index` after Accessibility Widgets |
| `ExtNsT3AA/AccessibilityWidgets/Index` | **MODIFIED (anchor only)** | Added `{#ns-t3aa-accessibility-widgets}` for DPA cross-links; body preserved |
| Other T3AA pages | **UNCHANGED / ALREADY MIGRATED** | No GitLab delta since baseline |

## T3AA Pages Updated

1. `ExtNsT3AA/DPAandGDPR/Index.md` *(new)*
2. `ExtNsT3AA/Index.md`
3. `ExtNsT3AA/AccessibilityWidgets/Index.md` *(anchor only)*
4. `docs.json` (+ redirects)
5. Homepage stats hubs via `compute_doc_stats.py` (772 pages)

## New Content Added

- Full T3AA DPA/GDPR page: product controls, DPA considerations, Q&A table (server storage areas), PageSpeed/alttext/TTS/MCP answers.
- Internal Mintlify links (not live docs.t3planet.de HTML URLs) to Credits, AI Usage & Logs, MCP Server, and T3AA feature pages.

## Existing Content Updated

- Product Index landing card for DPA & GDPR.
- Accessibility Widgets heading anchor for deep links from DPA.

## Existing Mintlify Content Preserved

- Accessibility Widgets body, Supademo (`cmspx6nk71m45qm339sebmr9a`), and structure from prior migration.
- Installation / Configuration / Feature pages not rewritten.
- Landing-page CardGroup layout and SEO-oriented frontmatter retained.

## Content Removed

None.

## Navigation Updated

- Sidebar: `ExtNsT3AA/DPAandGDPR/Index` under AI Accessibility.
- Index card: DPA & GDPR → `/ExtNsT3AA/DPAandGDPR/Index`.
- Redirects: `.html` variants → Mintlify path.

## Link Validation

- All internal links on the new DPA page resolve to existing Mintlify `.md` files (**14/14 OK**).
- Local preview HTTP: `/ExtNsT3AA/DPAandGDPR/Index`, `/ExtNsT3AA/AccessibilityWidgets/Index`, `/ExtNsT3AA/Index` → **200**.

## Build / Validation

- `scripts/compute_doc_stats.py` run successfully → **772 pages**, 68 products.
- Local preview routes smoked for T3AA pages above.

## Test Drive

Started from AI Accessibility index → Accessibility Widgets → new DPA & GDPR (HTTP 200). Feature-guide tree named Dashboard/Scans/Fix Hub in the task brief is **not** present in current live T3AA Sphinx or Mintlify trees (T3AA uses Accessibility Widgets, Speed, FileMeta, Audio, Voiceover, CKEditor checker, Simplified Text). No invented Feature Guide pages were added.

## Conflicts

None unresolved. RST list-table converted to Markdown table; Sphinx `:doc:` / `:ref:` converted to Mintlify links.

## Unable to Verify / Intentionally Skipped

- Legal wording: retained official “technical capabilities” scope; no legal advice invented.
- Typo **Accesstive** kept as in official RST (not “corrected” without source change).

## Follow-up (2026-09-15): T3AF + T3AI DPA migrated

Same GitLab commit `e47886ae` pages that were out of T3AA-only scope are now migrated:

| Path | Action |
|------|--------|
| `ExtNsT3AF/DPAandGDPR/Index.md` | **NEW** from live RST; Mintlify links; `{#ns-t3af-dpa-gdpr}` |
| `ExtNsT3AI/DPAandGDPR/Index.md` | **NEW** from live RST; Mintlify links |
| `ExtNsT3AF/Index.md` / `ExtNsT3AI/Index.md` | DPA & GDPR cards |
| `docs.json` | Nav (T3AF after Credits; T3AI after AISettings) + `.html` redirects |
| Stats | `compute_doc_stats.py` → **774 pages**, 68 products |

Internal DPA links: **19/19 OK**. Preserved existing Mintlify improvements elsewhere; no unrelated rewrites.

## Accuracy statement

Migration was performed by inspect → compare → migrate verified T3AA delta only → validate links/nav/stats → smoke preview. No unrelated extension docs were overwritten.
