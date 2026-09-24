---
name: t3planet-deploy
description: >-
  Production deployment for T3Planet Mintlify docs: inspect, validate, commit as
  Markus, push nitsan-technologies/T3Planet-docs, verify Mintlify/live, full QA.
  Use when the user says start deployment, start the deployment process, deploy
  latest docs, push docs live, or release documentation.
---

# T3Planet docs production deploy

Source of truth for humans: [`docs/deployment/deploy.md`](../../../docs/deployment/deploy.md).  
Safety guardrails: [`.cursor/rules/deployment-safety.mdc`](../../rules/deployment-safety.mdc) and [`.cursor/rules/mintlify-deployment.mdc`](../../rules/mintlify-deployment.mdc).

## Triggers

- start the deployment process / start deployment
- deploy the documentation / deploy latest docs
- push latest docs live / release the documentation

## Hard exclusions (never stage/commit/push/deploy)

```text
docs-master/
workshops/
```

Absolute paths when the worktree is this machine’s checkout:

```text
/Users/nitsan/www/AI Agents/Mintilify Doc/docs-master
/Users/nitsan/www/AI Agents/Mintilify Doc/workshops
```

Also exclude unless explicitly requested: `scripts/remigration/**`, QA dumps, secrets, `node_modules/`.

**Never** `git add .` / `git add -A` without printing and verifying `git diff --cached --name-only`.

Do not delete, reset, or stash excluded directories.

## State machine

```text
DISCOVERY → PRECHECK → CHANGE REVIEW → LOCAL VALIDATION → MANIFEST
→ STAGE → COMMIT (Markus) → PUSH origin master → VERIFY GITHUB
→ VERIFY MINTLIFY CONNECTION → WAIT BUILD → LIVE VERIFY
→ ROUTE DISCOVERY → HTTP/UI/SEARCH/RESPONSIVE/THEME/REGRESSION
→ HOTFIX LOOP IF CRITICAL → REPORT
```

Never jump from `PUSH` to `PASS`.

## Procedure

1. **Discovery** — `git rev-parse --show-toplevel`, `remote -v`, branch, status, log, identity.
2. **Remote** — must be `nitsan-technologies/T3Planet-docs`. Mismatch → STOP.
3. **Identity** — commit as Markus `<248457632+markus-neumannn@users.noreply.github.com>` via env (do not rewrite git config unless asked).
4. **Classify diffs** — PRODUCTION vs EXCLUDED vs TEMPORARY.
5. **Validate** — links/images/Supademos on changed pages; `mintlify validate` (Node 20); `compute_doc_stats.py` if nav/pages changed.
6. **Manifest** — list Included/Excluded; stage only Included paths.
7. **Gate** — abort if cached names include `docs-master/` or `workshops/`.
8. **Commit** — meaningful `docs: …` message.
9. **Push** — `git push origin HEAD:master` (no force).
10. **Mintlify** — verify Activity Git connection. Desired: org repo `master`. If still `markus-neumannn/t3planet-docs`, prefer reconnect; emergency same-SHA fork sync only if live is blocked (see mintlify-deployment rule). Tell user which path was used.
11. **Wait** — Successful + content markers on live (not HTTP 200 alone).
12. **QA** — sitemap/llms/nav inventory; HTTP; blank pages; nav; search; responsive (1440/1280/1024/768/390/375); light/dark; images/icons/Supademos; latest-change regression.
13. **Critical issues** — minimal hotfix → push → retest; max two deploy attempts then STOP + report.
14. **Report** — use template in `deploy.md`; final status exactly one of `PASS` | `PASS WITH NON-BLOCKING WARNINGS` | `BLOCKED` | `FAILED`. Use `NOT VERIFIED` when needed.
15. **History** — append `docs/deployment/deployment-history.md`.

## Definition of done

GitHub push **and** Mintlify deploy **and** live verification **and** post-deploy QA evidence. Do not claim PASS without evidence.
