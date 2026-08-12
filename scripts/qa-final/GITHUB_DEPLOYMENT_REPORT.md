# Deployment Report — T3Planet Mintlify → GitHub

**Date:** 2026-08-05  
**Actor:** GitHub user `markus-neumannn` (CLI authenticated)

---

## Final status

### **Deployment Blocked** (org repo write) — **Fork deploy succeeded**

| Target | Result |
|--------|--------|
| [nitsan-technologies/T3Planet-docs](https://github.com/nitsan-technologies/T3Planet-docs) | **Blocked** — account has **pull-only** (`push: false`); direct push returns **403** |
| [markus-neumannn/T3Planet-docs](https://github.com/markus-neumannn/T3Planet-docs) (fork) | **Success** — full Mintlify docs force-pushed to `master` |

PR to the org repo could not be opened: histories are unrelated, and merging upstream’s root `LICENSE` file collides with the docs folder `License/` on macOS case-insensitive volumes.

---

## Repository summary

| Field | Value |
|-------|--------|
| Official repo | https://github.com/nitsan-technologies/T3Planet-docs |
| Deployed fork | https://github.com/markus-neumannn/T3Planet-docs |
| Branch on fork | `master` (also mirrored as `main`) |
| Commit | `637e2f51825e1b05ff2ab2a13d96dbfb50eef2a3` |
| Message | `feat(docs): deploy complete Mintlify documentation for production` |

---

## Deployment summary (what was pushed to the fork)

| Item | Count / note |
|------|----------------|
| Documentation pages (`Index.md`) | ~664 |
| Image assets (webp/png/jpg/svg/gif) | ~3300+ |
| Config | `docs.json` (navigation + ~1398 redirects), `custom.css`, `_static/` |
| Product slug | `ExtNsT3AF/` (with redirects from `/AIFoundation/*`) |
| Build | **`mint validate` PASSED** after MDX fixes |

Excluded from git publish set: `Live-docs/`, `visual-regression/`, `.mintlify/`, `node_modules/` (see `.gitignore`).  
`.mintignore` still excludes `de/` and `scripts/` from Mintlify’s build/index (files may still be in git for maintainers).

---

## QA summary

| Check | Result |
|-------|--------|
| Project structure (`docs.json`, assets, T3AF hub) | Pass |
| `mint validate` | **Pass** |
| MDX blockers fixed | MCPTesting placeholders; `<=` / `>=` JSX breaks in License/Revolution Slider pages |
| Local preview smoke (prior session) | T3AF slug + redirects Pass |
| Search on hosted Mintlify | **Pending** — needs Mintlify project connected to this GitHub repo + deploy |
| Org-repo production cutover | **Blocked** on write permission |

---

## Git summary

| Action | Status |
|--------|--------|
| Remotes | `origin` → fork; `upstream` → org repo |
| Commit created | Yes (`637e2f5`) |
| Push to fork `master` | **Success** (force update; replaced placeholder README/LICENSE-only tree) |
| Push to org `master` | **Failed 403** |
| PR org ← fork | **Failed** (unrelated histories; LICENSE vs `License/` collision) |

---

## Corrective actions (required to finish org deployment)

1. **Grant write access** on `nitsan-technologies/T3Planet-docs` to `markus-neumannn` (or deploy from an org admin account), **then either:**
   - Force-push the fork tip to the org repo:
     ```bash
     git remote add org https://github.com/nitsan-technologies/T3Planet-docs.git
     git push org 637e2f5:master --force
     ```
   - Or: org admin merges/replaces `master` from https://github.com/markus-neumannn/T3Planet-docs
2. **Do not** add a root file named `LICENSE` beside the `License/` docs folder on a case-insensitive disk — keep GPL text as `COPYING` (already included).
3. In [Mintlify Dashboard](https://dashboard.mintlify.com): connect **nitsan-technologies/T3Planet-docs**, deploy branch `master`, wait for build + search index.
4. Verify hosted site + search (`T3AF`, `License`, etc.).

---

## Bottom line

- **Mintlify docs are fully published on the fork:** https://github.com/markus-neumannn/T3Planet-docs  
- **Official org repo is not updated yet** due to missing push permission.  
- After an org admin force-syncs `master` from the fork (or grants write), connect Mintlify and the production GitHub→Mintlify pipeline can go live.
