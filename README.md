# T3Planet Docs (Mintlify)

Official **T3Planet** product documentation. This repository is the **Mintlify source of truth** for TYPO3 extensions, templates, AI Universe products, and license/installation guides.

| | |
|---|---|
| **GitHub** | [nitsan-technologies/T3Planet-docs](https://github.com/nitsan-technologies/T3Planet-docs) |
| **Hosted Mintlify** | [nitsan-81630f36.mintlify.app](https://nitsan-81630f36.mintlify.app/) |
| **Public docs (migration target)** | [docs.t3planet.de](https://docs.t3planet.de/) |
| **Shop / support** | [t3planet.de](https://t3planet.de/en/) · [Support](https://t3planet.de/support) |

Approx. **769** documentation pages across **68** products (counts are generated — see [Homepage stats](#homepage-stats-pages--products)).

---

## What Mintlify covers

Mintlify turns this repo into the live documentation site. It handles:

| Area | How it works here |
|------|-------------------|
| **Pages** | Markdown (`.md`) files under product folders |
| **Navigation** | Sidebar groups in `docs.json` (Home, Get Started, AI, Templates, Extensions) |
| **URLs** | Path mirrors folders, e.g. `ExtNsT3AF/Installation/Index.md` → `/ExtNsT3AF/Installation/Index` |
| **Redirects** | Legacy `.html` / RTD-style paths mapped in `docs.json` → `redirects` |
| **Search** | Mintlify search index (full search after `mint login` / hosted deploy) |
| **Theme** | Mintlify `mint` theme + `custom.css` + `_static/` scripts |
| **Assets** | Images next to pages; logos and JS under `_static/` |
| **Build ignore** | `.mintignore` excludes `de/`, `docs/`, `Live-docs/`, `scripts/`, and internal reports from the published build |

Mintlify does **not** publish the Python tooling under `scripts/` or local Sphinx clones — only documentation content and site config.

---

## What this documentation covers

Content is organized the same way readers see it in the sidebar:

### 1. Get started — License & installation

Folder: `License/`

- Generate / activate license keys  
- T3Planet Shop license manager and **All Licenses**  
- Trial extend, renew, domains, updates  
- Shared install and update patterns for premium products  

Start here: [/License/Index](https://nitsan-81630f36.mintlify.app/License/Index)

### 2. AI Universe (AI Extensions)

Hub: `AIFoundationExtensions/`  
Shared foundation: `ExtNsT3AF/` (AI Foundation)

| Product folder | Product |
|----------------|---------|
| `ExtNsT3AF/` | AI Foundation (providers, credits, AI Label, …) |
| `ExtNsT3AI/` | AI Assistant |
| `ExtNsT3AC/` | AI Chatbot |
| `ExtNsT3AS/` | AI Search |
| `ExtNsT3AA/` | AI Accessibility |
| `ExtNsT3AL/` | AI Localization |
| `ExtNsT3AB/` | AI Extension Builder |

Typical page set per product: Introduction → Installation → Configuration → Feature guides → FAQ / Support / Known Problems.

### 3. TYPO3 Templates & Themes

Hub: `AllTemplates/`  
Folders such as `EXTAvatar/`, `EXTAyu/`, `EXTBootstrap/`, `EXTKarma/`, `EXTReactBootstrap/`, `EXTReva/`, `EXTShiva/`, `EXTShop/`, `ExtThemes/`.

### 4. TYPO3 Extensions

Hub: `AllExtensions/`  
Folders such as `ExtNsRevolutionSlider/`, `ExtRTECKEditorPack/`, `ExtNsBackup/`, `ExtNsGoogleSiteKit/`, `TonicTypes/` (TonicTypes), cookies/privacy, comments, maps, and many more.

Each extension usually documents installation, configuration, updates, and support links.

---

## How to use the documentation (readers)

1. Open the hosted site (Mintlify URL above, or docs.t3planet.de after cutover).  
2. Use the **sidebar** to pick a product, or the top nav: AI Extensions · Templates · Extensions · Get Started.  
3. Use **search** (`⌘K` / `Ctrl+K`) for features, settings, or error messages.  
4. Follow pages in order when learning a product: **Introduction → Installation → Configuration**.  
5. For licenses and Shop issues, use **License** docs and [T3Planet Support](https://t3planet.de/support).  
6. Prefer **site package overrides** and the steps in the guide — do not invent paths or settings that are not documented.

---

## How to work on this repo (authors)

### Prerequisites

- **Node 22 LTS** (Node 26+ breaks the Mintlify CLI)  
- Git + access to this GitHub repo  
- Optional: `mint login` for local search against the project index  

### Local preview

```bash
npm i -g mint@latest
mint login    # optional, for search
mint dev      # local Mintlify preview
```

### Fast LAN preview (recommended)

Serves a cache proxy on **:3000** (Mintlify compile on **:3001**) so phones / other PCs on the network can open the docs:

```bash
./scripts/start_fast_preview.sh
# http://127.0.0.1:3000/  or  http://<lan-ip>:3000/
```

After content changes, purge cache:

```bash
curl -s http://127.0.0.1:3000/__t3_cache_purge
```

### Add or edit a page

1. Create or edit `ProductFolder/.../Index.md` (Mintlify frontmatter: `title`, `description`, `sidebarTitle` where used).  
2. Register the page in `docs.json` navigation if it is new.  
3. Put images under that page’s `Images/` or `images/` folder and link with relative paths.  
4. Preview locally, then commit and push.  
5. Refresh homepage stats if you added/removed a page or product (see below).

### Page conventions

- Prefer **`Index.md`** as the page file name (URL ends with `/Index`).  
- Keep **one product = one top-level folder** (`ExtNs…`, `EXT…`).  
- Do **not** invent TYPO3 settings, version numbers, or screenshots.  
- Convert RST/Sphinx content carefully to Markdown (notes → `<Note>`, code fences, tables).  
- Internal links should use Mintlify paths (e.g. `/License/Index`), not old `/en/latest/...html` URLs inside new content.

### Homepage stats (pages & products)

Never hardcode **Documentation pages** / **Products** on hub pages.

```bash
python3 scripts/compute_doc_stats.py
# same as:
python3 scripts/sync_doc_stats.py
```

Updates `_static/t3-stats.json`, `_static/t3-stats-inline.js`, and hub Markdown. Migration / hub scripts and the LAN preview starter call this automatically.

### Useful scripts

| Script | Purpose |
|--------|---------|
| `scripts/compute_doc_stats.py` | Regenerate homepage page/product counts |
| `scripts/sync_doc_stats.py` | Same sync (importable helper) |
| `scripts/start_fast_preview.sh` | LAN-friendly Mintlify + cache proxy |
| `scripts/generate_hub_landings.py` | Rebuild AI / Templates / Extensions hubs |
| `scripts/migrate_from_live.py` | Bring content from live Sphinx HTML when needed |

---

## Important paths

| Path | Purpose |
|------|---------|
| `docs.json` | Name, theme, navbar, sidebar, redirects, scripts |
| `index.md` | Homepage |
| `AIFoundationExtensions/` | AI Universe hub |
| `AllTemplates/` · `AllExtensions/` | Catalog hubs |
| `License/` | License & installation |
| `ExtNsT3AF/` … / `TonicTypes/` … | Product documentation trees |
| `custom.css` | Custom UI styling |
| `_static/` | Logos, favicon, `t3-docs.min.js`, stats |
| `.mintignore` | Files/folders excluded from Mintlify publish |
| `COPYING` | License notice |

---

## Deploy to Mintlify

**Live URL:** https://docs.t3planet.de/en/latest  
**Mintlify project:** T3Planet Docs (workspace **nitsan-81630f36**)

### Which GitHub repo updates live?

Mintlify **Git settings** are connected to the Markus fork:

| Remote | Repository | Role |
|--------|------------|------|
| `markus` | https://github.com/markus-neumannn/T3Planet-docs | **Live Mintlify source** (`master`) |
| `origin` | https://github.com/nitsan-technologies/T3Planet-docs | Org / official mirror |

Pushing only to `origin` does **not** update live docs while Git settings point at the fork.

### Release steps

1. Commit documentation as **Markus** (`248457632+markus-neumannn@users.noreply.github.com`).
2. Validate locally: Node 20 + `mintlify validate` (+ preview on `:3001`).
3. Push live source: `git push markus HEAD:master`
4. Mirror to org when required: `git push origin HEAD:master`
5. Confirm [Mintlify dashboard](https://dashboard.mintlify.com) → **Activity** (Successful update by Markus).
6. Spot-check https://docs.t3planet.de/en/latest for the intended content (not HTTP 200 alone).

If Activity does not move: use **Manual update** in the dashboard, or an empty trigger commit on **`markus`**.

Full agent/runbook details: [`context.md`](./context.md).

---

## License

Documentation content © T3Planet / NITSAN. See repository license notice (`COPYING`).

<!-- deploy: markus-only contributor history -->
