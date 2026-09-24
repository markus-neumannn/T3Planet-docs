# Deployment checklist (quick)

- [ ] `git remote -v` → `nitsan-technologies/T3Planet-docs`
- [ ] Branch `master`
- [ ] Markus author for commit
- [ ] Diff reviewed; no secrets
- [ ] **No** `docs-master/` or `workshops/` in staging
- [ ] No blind `git add .`
- [ ] `mintlify validate` (Node 20) when possible
- [ ] Push `origin HEAD:master` (no force)
- [ ] Mintlify Activity: correct Git repo + Successful build
- [ ] Live URL shows new content
- [ ] HTTP / nav / search / responsive / theme / latest-change QA
- [ ] History entry + final status
