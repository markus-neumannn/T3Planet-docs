# T3Planet Docs — Agent Context

Last verified: 2026-09-16 (content-craft section refreshed)  
Maintainers: T3Planet / NITSAN (internal docs team; releases often attributed to **Markus** on GitHub)

This file is the **authoritative runbook** for AI agents working in this repository.  
Prefer it over chat memory. When instructions conflict, **user message in the current task** wins, then this file, then `.cursor/rules/`.

---

## Who we write for (client / audience model)

**Assume the reader is a TYPO3 professional**, not a first-time CMS user.

| Reader | Expectation |
|--------|-------------|
| Integrators, agencies, in-house TYPO3 teams | Know backend modules, page tree, File List, Scheduler, TypoScript basics |
| T3Planet customers | Bought extensions/themes; need license, config, feature workflows, edge cases |
| AI Universe users | Understand that **AI Foundation** (`EXT:ns_t3af`) is shared infra for T3AA, T3AI, T3AC, etc. |

### Editorial tone (match T3Planet client expectations)

- **Direct and accurate** — no filler, no “AI slop”, no marketing fluff in technical steps.
- **Do not patronize** — omit obvious navigation like “Open TYPO3 → click module → select page in tree” unless the page is explicitly *Getting started for non-TYPO3 users*.
- **Prefer Supademos + concise prose** over duplicate full-page screenshots when both show the same UI.
- **Use product names customers see** — e.g. **AI Foundation**, **AI Accessibility** (not only internal slugs like “T3AF” in customer-facing intro text; extension keys in backticks are fine).
- **Preserve legal/privacy nuance** — DPA/GDPR pages describe *capabilities* and *options*, not over-claiming compliance.
- **Links must work on live** — host-at prefix `/en/latest`, full paths under product folders (see Link conventions).

When the user says customers “have TYPO3 knowledge”, **delete or shorten** elementary backend navigation sections (example: Dashboard “How to open it” steps).

---

## How to prepare and write content (client feedback lessons)

Use this when creating or rewriting Feature Guide / product pages. Learned from live QC with T3Planet.

### Content structure that works

| Page type | Preferred structure |
|-----------|---------------------|
| Feature overview (e.g. Content tab) | Short intro + **one section per UI card** (1–2 lines) + link to the dedicated Feature Guide page. No beginner “Steps: open module / page tree”. |
| Info / sales-adjacent (e.g. Human Expert) | What it is + when to use + optional comparison table. **No numbered Steps** unless the flow is non-obvious. |
| Tool feature (e.g. Color contrast checker) | Treat as a **major capability**: purpose, how to open, screenshot if provided, what you can do. Prefer attached product screenshots for unique tools. |
| Scanner / Fix Hub | Accurate source of findings: **Fix Hub = Scanner issues only** (product rule as of 2026-09). Do not invent slogans. |
| CLI for integrators | Always document **both**: Composer (`vendor/bin/typo3 …`) and Non-Composer (`php typo3/sysext/core/bin/typo3 …`). |

### Voice rules from feedback (do / don’t)

**Do**

- Write complete sentences. Never ship truncated frontmatter `description` (live meta shows the cut-off — e.g. “…voiceover, s”).
- Separate **license** vs **AI provider**: put provider requirements in feature/setup prose; keep **Important notes** focused (e.g. “valid T3AA license required”) when the client says provider wording there misleads.
- Prefer concrete verbs: “Open an issue from the results list to continue in Fix Hub” over taglines.
- Match product reality. If Scanner/Lighthouse run **both** desktop and mobile, do **not** document “Choose Desktop or Mobile”.
- For settings sentences, prefer clear subjects: `Settings are saved per site in config.yaml. It does not change page content in the database.` (client-approved shape).
- After local edits: purge LAN preview cache (`curl -s http://127.0.0.1:3000/__t3_cache_purge`) and give the **LAN URL** (`http://<LAN>:3000/...`).

**Don’t**

- Slogan / poster lines the client rejects, e.g. “A scan reports findings. Fix Hub is where work happens.”
- Over-explain negatives the client then removes (e.g. repeated “Lighthouse is not in Fix Hub” / “Fix Hub does not run the scan itself”) unless they asked for that clarification.
- Generic “How to open it” for TYPO3-experienced readers.
- Leave empty headings (`## Module overview` with no body).
- Invalid Lucide icons (`sliders`, `text`) — use `sliders-horizontal`, `type`, etc.
- RST leftovers (`::`, `.. code-block::`) on live-facing pages.
- Short links (`/en/latest/FixHub/Index`) or double host-at (`/en/latest/en/latest/...`).

### Feedback loop (how the client works)

1. They browse **local LAN preview** or paste a **live URL** + screenshot / purple box.
2. They ask for a **precise** edit (remove line X, rewrite sentence Y, add table Z).
3. Expect **local-first**; deploy only when they say push / live / Markus.
4. When they say “train yourself / improve context.md” — update this file and `.cursor/rules/` in the same turn.

### T3AA product facts agents must not contradict

- **Fix Hub** displays/manages **Scanner** findings only (not Lighthouse). Lighthouse stays under Scanner → Lighthouse.
- **Bulk Scans** queues pages for the **Scanner** engine + Scheduler/CLI (`nst3aa:monitor:run`).
- **AI generation** (alt text, audio, voiceover, simplify) needs AI Foundation provider/features; inventory/review alone may not call AI.
- Extension code (when fixing product behaviour) may live under TYPO3 setups, e.g. `…/packages/ns_t3aa` — docs repo alone cannot “fix” Fix Hub backend without that package.

---

## How this client typically works with agents

Patterns observed from real tasks — follow them unless the user says otherwise.

| User intent | Agent behavior |
|-------------|----------------|
| “Fix locally / migrate / QA” | Change files in workspace; **do not push** until they ask for release/deploy. |
| “Remove image on [live URL]” | Edit the matching `.md` under the product tree; confirm **local vs live** in the reply. |
| “Add icon” on Feature Guide cards | Fix Lucide `icon=` on `<Card>` in `FeatureGuide/Index.md`; invalid names render **blank** on live. |
| “Improve code snippet UI” | Replace RST leftovers (`::`, `.. code-block::`) with fenced blocks (` ```bash ` / ` ```json `). |
| “Deploy / push / live” | Local QA → commit as **Markus** → **`git push origin HEAD:master`** → Activity + **live content** proof. If live stale and Mintlify Git still on fork → emergency same-SHA sync (see deploy §4). |
| “Train context / deployment” | Update this `context.md` and `.cursor/rules/` so the next session does not repeat mistakes. |
| Attached screenshot of Mintlify dashboard | Treat dashboard as source of truth for **which GitHub repo** is connected. |
| “Start network / LAN preview” | Ensure `:3001` mint + `:3000` cache proxy; give `http://<LAN-IP>:3000/`; purge cache after edits. |
| “Remove this line / rewrite this” | Exact surgical edit; purge preview; do not redeploy unless asked. |
| “Add comparison / highlight feature + image” | Expand as a real section; copy image under product `images/`; prefer WebP when tooling allows. |
| Product behaviour vs docs (e.g. Fix Hub sources) | Fix **extension code** if in scope; align docs to product — never document features the product does not have. |

### Always clarify: local vs live

After edits, state clearly:

- **Local** = files in this workspace; preview via **`:3000`** (LAN/fast proxy) or `:3001` (raw mint).
- **Live** = https://docs.t3planet.de/en/latest after Mintlify deploy from **`origin`** (`nitsan-technologies/T3Planet-docs`).

Do not say “fixed on the site” until live HTML shows the change.

---

## Project identity

| Item | Value |
|------|--------|
| Local workspace | Directory containing `docs.json` (path may be `Mintilify Doc` with a space) |
| Docs product name | T3Planet Docs |
| Live URL | https://docs.t3planet.de/en/latest |
| Mintlify workspace / project | **nitsan-81630f36** / **T3Planet Docs** |
| Mintlify dashboard | https://dashboard.mintlify.com → Activity, Git settings, Manual update |
| Host-at path | `/en/latest` |
| Local preview | `mintlify dev --no-open --port 3001` with **Node 20** (`/opt/homebrew/opt/node@20/bin`); Node 25+ breaks CLI |
| Validation | `mintlify validate` (strict; must pass before release) |
| Custom assets | `custom.css`, `_static/t3-docs.min.js`, `_static/t3-stats*.json` |
| Nav / redirects | `docs.json` (large; dedupe redirects carefully) |

---

## CRITICAL: which GitHub repo Mintlify deploys from

**Deploy only from the org repository** (updated 2026-09-23):

| Setting | Value |
|---------|--------|
| Connected repository (required) | **`nitsan-technologies/T3Planet-docs`** |
| Branch | **`master`** |
| Live domain | `docs.t3planet.de/en/latest` |
| Do not use | `markus-neumannn/T3Planet-docs` |

### Remotes

```text
origin  https://github.com/nitsan-technologies/T3Planet-docs.git   # ONLY deploy remote
```

Do not configure or push a `markus` remote for live deploys.

### Author vs repository

| Concept | Value |
|---------|--------|
| Git **author name** for releases | **Markus** (required) |
| Git **author email** | `248457632+markus-neumannn@users.noreply.github.com` |
| Push **remote** | **`origin`** only → `nitsan-technologies/T3Planet-docs` |
| Do not confuse | Markus **author** ≠ `markus-neumannn/T3Planet-docs` **fork** |

### Deployment rule

1. **`git push origin HEAD:master`** updates the org repo and (when Mintlify Git is connected to org) triggers live.
2. Never force-push unless explicitly authorized.
3. Prefer Mintlify dashboard **Git** → connect **`nitsan-technologies/T3Planet-docs`** / `master` so live always follows `origin`.
4. **Emergency live unblock (incident 2026-09-23):** if Activity still shows the Markus fork and `/new-path` is 404 on live while org already has the commit, temporarily push the **same SHA** to the fork (`git push markus origin/master:master`), poll live until content matches, then remove the `markus` remote again. Tell the user this was emergency-only.

### Never push / never deploy

- `workshops/` (local workshop PPT/site; gitignored)
- `docs-master/` (already gitignored)
- `scripts/remigration/*` QA dumps, `scripts/live_e2e_qa/*`, unless explicitly requested

### Verify live deploy (evidence-based)

Poll production until **content** matches, e.g.:

- Feature Guide: `sliders-horizontal` / `type` icons present (not broken `sliders` / `text`).
- Dashboard: no `dashboard-overview.webp` in page when removed.
- Bulk Scans: bash fence for `vendor/bin/typo3 nst3aa:monitor:run`, no RST `::`.

HTTP 200 alone is **not** sufficient.

---

## Git author for documentation releases

| Field | Value |
|-------|--------|
| Name | **Markus** |
| Email (use this; do not invent) | `248457632+markus-neumannn@users.noreply.github.com` |

```bash
GIT_AUTHOR_NAME='Markus' \
GIT_AUTHOR_EMAIL='248457632+markus-neumannn@users.noreply.github.com' \
GIT_COMMITTER_NAME='Markus' \
GIT_COMMITTER_EMAIL='248457632+markus-neumannn@users.noreply.github.com' \
git commit -m "docs: …"
```

Only commit when the user asks (or an explicit release task). Stage **docs only**, not QA dumps.

---

## Standard release procedure

### Gate A — Local

1. Working tree = source of truth; no full RST re-migration unless needed.
2. Stage: product `Ext*` / `EXT*` trees, `License/`, hubs, `docs.json`, `custom.css`, `_static/`, `index.md`, `context.md` when requested.
3. **Exclude** by default: `RST Format */`, `scripts/remigration/*`, `scripts/live_e2e_qa/*`, logs, JSON QA reports.
4. Nav/page count changes → `python3 scripts/compute_doc_stats.py`.
5. `mintlify validate` (Node 20).
6. Preview smoke on `:3001` for touched URLs (restart preview if 500).
7. Review `git diff --cached`.

### Gate B — GitHub

```bash
git remote -v && git branch --show-current
git push origin HEAD:master    # only deploy remote
```

Verify: https://github.com/nitsan-technologies/T3Planet-docs/commits/master (author Markus, files present).

### Gate C — Mintlify

Dashboard → **Git** must show **`nitsan-technologies/T3Planet-docs`** / `master`.  
Dashboard → **Activity** → Successful update for the commit (author often Markus).  
If stuck: **Manual update**, or emergency same-SHA sync to the fork only while Git is still on the fork (see Deployment rule §4), then reconnect Git to org.

### Gate D — Production QA

Minimum for T3AA Feature Guide releases: Index cards (icons), pages where screenshots were removed, Supademos, internal links, code blocks, one responsive width if UI changed.

---


## TonicTypes documentation paths (2026-09-23)

| Item | Value |
|------|--------|
| Product folder / URL | **`TonicTypes/`** |
| Old folder (redirect only) | `ExtTypoTonic/` → `/TonicTypes/` |
| Professional page | **`TonicTypes/Professional/`** |
| Old Professional URL | `…/TypoTonicProfessional/` → `/TonicTypes/Professional/` |
| Primary product framing | **EXT:tonictypes_pro** (`k3n/tonictypes_pro`) |
| Required dependency | Core **EXT:tonictypes** (`k3n/tonictypes`) — install order / shared plugins / ViewHelpers |
| Live Index | https://docs.t3planet.de/en/latest/TonicTypes/Index/ |
| ClickUp example | [86d4cb2rx](https://app.clickup.com/t/86d4cb2rx) rename + Pro focus |

When renaming product trees: `git mv`, rewrite `/en/latest/...` hrefs + `docs.json` nav, add specific redirects **before** `/:path*` wildcards, run `compute_doc_stats.py`, `mintlify validate`, then deploy.

---
## Documentation conventions (Mintlify)

### Links

- Internal: `/en/latest/ExtNsT3AA/FeatureGuide/...` (full product path).
- **Wrong:** `/en/latest/FixHub/Index`, `/en/latest/Dashboard/Index`, `/en/latest/en/latest/...` (double prefix).

### Feature Guide hub (`ExtNsT3AA/FeatureGuide/Index.md`)

- `<CardGroup>` with Lucide icons (`docs.json` → `"icons": { "library": "lucide" }`).
- **Working examples:** `layout-dashboard`, `image`, `sliders-horizontal`, `scan`, `wrench`, `file-text`, `type`, `accessibility`.
- **Broken examples:** `sliders`, `text` (empty icon on live).

### Embeds

- Supademos: `<div className="t3-embed"><iframe … allow="clipboard-write; fullscreen" …></iframe></div>`
- Prefer keeping Supademos when user removes **static screenshots** of the same screen.
- Human Expert: no Supademo on page when user requested removal.

### RST → MD hygiene

- No `.. code-block::`, no standalone `::`, no `:ref:` — use Markdown links and fenced code.
- Tables: GitHub-flavored; fix converter damage before release.

### Images

- Prefer WebP where repo already migrated; do not leave MD pointing at deleted PNG/JPEG.
- User may remove overview images from Feature Guide pages intentionally; do not re-add without ask.

---

## T3AA remigration (controlled)

| Item | Path |
|------|------|
| RST source (local only) | `RST Format ExtNsT3AA/` |
| Mintlify product | `ExtNsT3AA/` |
| Feature Guide | 15 pages under `FeatureGuide/` (Dashboard, AI Alt Text, Scans subtree, Fix Hub, etc.) |

Inventory gate: 28 RST files ↔ 28 matching MD paths; Feature Guide set parity verified (`REMIGRATION_GATE_VERIFY.json` under `scripts/remigration/` when generated).

Remigration default: **local migrate + QA → stop for approval → then release** (push/deploy).

---

## Agent prompting cheat sheet (reply like their release engineer)

1. **Small content fix** — edit MD, one-line summary, note local-only unless they said deploy.
2. **Release request** — gates A–D, commit hash, both remotes, live poll result, honest NOT VERIFIED items.
3. **“Is it live?”** — curl/check live HTML; explain fork vs origin if mismatch.
4. **Icons / UI** — Playwright or fetch live; show what was wrong (invalid Lucide name vs deploy lag).
5. **Never** claim all pages tested unless crawled.
6. **Commits** — Markus author; message style: `docs: …` or `chore: trigger Mintlify …`.

---

## Do not

- Push without user approval (except when explicit release/deploy task).
- Push only to `origin` and call deployment done without checking live HTML (Mintlify may still be on the Markus fork).
- Confuse Markus **commit author** with the `markus-neumannn/T3Planet-docs` fork.
- Leave `ExtTypoTonic` URLs as primary after the TonicTypes rename (use redirects only).
- Commit `workshops/` or `docs-master/`.
- Force-push, invent emails, commit secrets or remigration noise.
- Re-add removed screenshots or patronizing TYPO3 steps without user ask.
- Hardcode homepage page/product counts (use `compute_doc_stats.py`).
- Use Node 25+ for Mintlify CLI.

---

## Quick checklist

- [ ] Audience-appropriate prose (TYPO3-professional, not beginner)
- [ ] Local validate + preview OK
- [ ] Commit author = Markus (if committing)
- [ ] `git push origin HEAD:master` for live (only deploy remote)
- [ ] Mintlify Activity Successful
- [ ] Live URL shows intended content (specific checks, not just 200)

---

## Related files

| File | Role |
|------|------|
| `README.md` | Human deploy summary |
| `.cursor/rules/mintlify-deployment.mdc` | Always-on deploy remote rule |
| `.cursor/rules/homepage-stats.mdc` | Stats regeneration |
| `.cursor/rules/t3planet-client.mdc` | Audience + client workflow |
| `scripts/qa-final/GITHUB_DEPLOYMENT_REPORT.md` | Historical fork vs org notes |

## Lessons learned — 2026-09-23

1. **Org-only deploy policy:** day-to-day remote is `origin` (`nitsan-technologies/T3Planet-docs`). Keep local `markus` remote removed unless emergency.
2. **Live lag diagnosis:** org tip can be correct while live 404s a new path — Mintlify Activity “Connected repository” is the truth for which GitHub Mintlify builds.
3. **TonicTypes rename:** folder + nav + redirects + Pro framing shipped as `5d8e875`; live needed fork sync until Mintlify Git points at org.
4. **Workshop PPT** lives under `workshops/` and must never be committed or deployed with docs.
5. **ClickUp docs tasks:** update status, leave evidence comment (commit SHA, live URLs, any Mintlify Git blocker).

