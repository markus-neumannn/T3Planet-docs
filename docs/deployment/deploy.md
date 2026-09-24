# T3Planet Documentation Deployment Guide

Human-readable SOP for production docs releases. Cursor agents follow the same flow via `.cursor/skills/t3planet-deploy/SKILL.md` when you say **start the deployment process**, **start deployment**, or **deploy latest documentation**.

## 1. Purpose

Move **verified production documentation** from the local Git worktree → GitHub → Mintlify → [https://docs.t3planet.de/en/latest/](https://docs.t3planet.de/en/latest/), then prove the live site is healthy (HTTP, navigation, search, responsive, themes, latest-change regression). A green `git push` alone is **not** a successful deployment.

## 2. Production URL

```text
https://docs.t3planet.de/en/latest/
```

Also useful:

```text
https://docs.t3planet.de/en/latest/sitemap.xml
https://docs.t3planet.de/en/latest/llms.txt
```

## 3. GitHub Repository

```text
https://github.com/nitsan-technologies/T3Planet-docs.git
```

Local remote (required):

```text
origin → https://github.com/nitsan-technologies/T3Planet-docs.git
branch: master
```

Verify before every push:

```bash
git remote -v
git branch --show-current
git rev-parse --show-toplevel
```

If the remote is not the org repo: **STOP**. Do not silently change remotes. Report current vs expected.

## 4. Mintlify Project

| Field | Expected / verified |
| --- | --- |
| Project | **T3Planet Docs** (workspace **nitsan-81630f36**) |
| Live status | Live |
| Production URL | `docs.t3planet.de/en/latest` |
| **Desired** Git connection | `nitsan-technologies/T3Planet-docs` · `master` |
| Dashboard | [Mintlify Activity](https://app.mintlify.com/t3planet/t3planet/activity) |

**Always re-verify** Activity / Git settings before treating a push as live. A screenshot can be stale.

### Known mismatch (do not ignore)

If Activity still shows `markus-neumannn / t3planet-docs` while we push only to `nitsan-technologies/T3Planet-docs`, live will **not** update from `origin`.

1. Prefer reconnecting Mintlify Git to the org repo.
2. Emergency unblock (authorized, temporary): sync the same SHA to the fork that Mintlify still watches, then remove the temporary remote. See `.cursor/rules/mintlify-deployment.mdc`.
3. Tell the operator clearly when an emergency fork sync was used.

Do **not** change domain, org, env vars, or Git connection without explicit authorization.

## 5. Authorized Git Identity

Commit author (name ≠ fork repo):

```text
Markus <248457632+markus-neumannn@users.noreply.github.com>
```

Prefer one-shot env for the commit (do **not** rewrite global `git config` unless the operator asks):

```bash
GIT_AUTHOR_NAME='Markus' \
GIT_AUTHOR_EMAIL='248457632+markus-neumannn@users.noreply.github.com' \
GIT_COMMITTER_NAME='Markus' \
GIT_COMMITTER_EMAIL='248457632+markus-neumannn@users.noreply.github.com' \
git commit -m "…"
```

Never forge credentials, expose tokens, or commit secrets.

## 6. Production source vs exclusions

### Production source

Repository root of `nitsan-technologies/T3Planet-docs` (Mintlify docs at repo root: `docs.json`, product folders, `custom.css`, `_static/`, etc.). Discover with `git rev-parse --show-toplevel` — do not assume every folder under the parent path is deployable.

### Production Deployment Exclusions

**NEVER** stage, commit, push, copy into the build, or deploy through Mintlify:

```text
/Users/nitsan/www/AI Agents/Mintilify Doc/docs-master
/Users/nitsan/www/AI Agents/Mintilify Doc/workshops
```

Also never deploy by default (unless explicitly requested):

```text
scripts/remigration/**
RST Format */**
*.env / credentials / tokens
node_modules/
local QA dumps, screenshots-only artifacts, debug JSON
```

These paths are local development / workshop / QA resources. Local changes there must be **preserved** (do not delete, reset, or stash automatically). Leave them unstaged.

**NEVER use `git add .` or `git add -A` without validating the exact staging set.**

## 7. Pre-deployment checklist

- [ ] Correct worktree / remote / branch
- [ ] Markus author identity available
- [ ] Diff reviewed; exclusions confirmed absent from staging
- [ ] No secrets
- [ ] `mintlify validate` (Node 20) when possible
- [ ] Stats regenerated if nav/pages changed (`python3 scripts/compute_doc_stats.py`)
- [ ] Intended pages/assets/Supademos spot-checked locally

## 8. Git status check

```bash
git status --short
git status -sb
```

## 9. Review changes

```bash
git diff --stat
git diff
# if already staged:
git diff --cached --stat
git diff --cached
```

Classify each path: `PRODUCTION` | `EXCLUDED` | `UNRELATED` | `GENERATED` | `TEMPORARY` | `UNKNOWN`.

## 10. Validate documentation

- Markdown/MDX, frontmatter, `docs.json` nav, redirects
- Internal links, images, icons, Supademo embeds on **changed** pages
- `mintlify validate` on Node 20

## 11. Deployment manifest

Before commit, list **Included** and **Excluded**. Example:

```text
Included:
- ExtNsT3AI/Media/Index.md
- TonicTypes/Installation/Index.md
- custom.css
- docs/deployment/deploy.md
…

Excluded:
- docs-master/**
- workshops/**
- scripts/remigration/**
```

Final gate:

```bash
git diff --cached --name-only
```

Abort if any path under `docs-master/` or `workshops/` appears.

## 12. Commit

Meaningful message, e.g. `docs: ship Media/TonicTypes updates and footer flush CSS`.

```bash
git status
git log -1 --format='%h %an <%ae> %s'
```

## 13. Push to GitHub

```bash
git push origin HEAD:master
```

**Never** `git push --force` unless the operator explicitly authorizes it.

Record commit hash, message, branch, remote.

## 14. Mintlify deployment

1. Open Activity; confirm connected repo/branch.
2. Confirm new commit appears (or emergency fork sync if still on Markus fork).
3. Wait for **Successful** + Live — do not start final QA while building.

## 15. Wait for deployment

Poll Activity and/or live HTML for new content markers (not HTTP 200 alone). Cap retries: investigate → one fix → second deploy → stop and report if still failing.

## 16. Verify production

Confirm `https://docs.t3planet.de/en/latest/` is the live docs site (not localhost/preview) and reflects the release.

## 17. Discover documentation routes

Build inventory from `docs.json`, sidebar/nav, `sitemap.xml`, `llms.txt`, internal links, hub cards. Record discovered / tested / skipped.

## 18. HTTP status testing

Expect `200` (and intentional redirects). Fail on unexpected `404` / `500` / `502` / `503` and other 5xx.

## 19. Broken link testing

Sample internal links from hubs + every **changed** page; flag dead routes and wrong casing.

## 20. Navigation testing

Logo, hubs, sidebar, product roots, prev/next, footer, no stuck loaders / blank hubs.

## 21. Search testing

Open search; query real terms (e.g. `TYPO3`, `T3AI`, `Installation`, `Media`, `TonicTypes`); open a result; confirm correct page on desktop and mobile.

## 22. Responsive testing

Viewports: 1440, 1280, ~1024, ~768, ~390, ~375 — header, drawer, search, cards, tables, footer, overflow.

## 23. Light / dark mode testing

Both themes: contrast, sidebar, cards, code, icons, active nav.

## 24. Image testing

Changed pages: images load, correct assets, no broken icons.

## 25. Supademo testing

Changed embeds: iframe loads, correct demo, usable on desktop/mobile.

## 26. Icon testing

Cards/sidebar: valid Lucide names, no missing icons on affected pages.

## 27. Performance testing

Note stuck loaders, extreme slowness, huge assets. Quote Lighthouse only if actually run.

## 28. Latest-change regression

For each deployed area (page + parent + sidebar + search + responsive + theme), verify the intended edit is live.

## 29. Critical issue handling

Classify: SOURCE / NAVIGATION / MINTLIFY / BUILD / CSS / JS / ASSET / GIT / DEPLOYMENT / CACHE / UNKNOWN. Do not ignore site-wide 404/blank/nav/search failures.

## 30. Hotfix process

Reproduce → minimal fix → validate → commit Markus → push origin (and emergency fork sync if needed) → wait → retest affected + related flows. No drive-by refactors.

## 31. Final deployment checklist

See Definition of Done in `.cursor/skills/t3planet-deploy/SKILL.md`. Success requires GitHub + Mintlify + LIVE + QA evidence.

## 32. Deployment report template

```text
Deployment date:
Operator:
Repository:
Branch:
Commit / message:
Git push:
Mintlify project / connected repo / branch:
Deployment status:
Production URL:
Pages discovered / checked:
404 / 500 / 502 / 503:
Blank pages:
Navigation / Search / Responsive / Theme:
Images / Icons / Supademos:
Latest changes verified:
Issues / Fixes:
Final status: PASS | PASS WITH NON-BLOCKING WARNINGS | BLOCKED | FAILED
```

Use **NOT VERIFIED** when a check could not be performed — never invent.

## 33. Troubleshooting

| Symptom | Check |
| --- | --- |
| Push OK, live stale | Mintlify Git still on fork? Activity SHA? CDN cache? |
| Build failed | Mintlify logs, MDX/`docs.json`, `mintlify validate` |
| Many 404s | Nav vs files, redirects, path renames |
| Search empty | Index lag after deploy; retry later; confirm pages in sitemap |
| Footer / CSS missing | `custom.css` in commit? hard refresh |

## 34. Deployment history

Append each release to [deployment-history.md](./deployment-history.md).

## Trigger phrases

When the operator says any of:

- start the deployment process  
- start deployment  
- deploy the documentation / latest docs  
- push latest docs live  
- release the documentation  

run this SOP via `.cursor/skills/t3planet-deploy/SKILL.md`.
