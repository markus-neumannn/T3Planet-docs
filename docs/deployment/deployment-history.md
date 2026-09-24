# T3Planet documentation deployment history

Append one entry per production release.

---

## Template

```text
### YYYY-MM-DD — <short title>
- Commit:
- Push remote:
- Mintlify connected repo (verified):
- Live URL check:
- QA summary:
- Final status:
```

---

<!-- entries below -->

### 2026-09-24 — Media / TonicTypes / footer / deploy SOP
- Commit tip: `36cf8f0` (content `105c568`, SOP `0f3974d`, gitignore `018a601`/`58ec5b0`)
- Push remote: `origin` → `nitsan-technologies/T3Planet-docs` (`master`)
- Mintlify connected repo: Activity still showed `markus-neumannn/t3planet-docs` — emergency same-SHA sync to fork so live updated
- Live URL check: markers OK (`tonictypes_em_search_free`, footer CSS rule)
- QA: sitemap 841 routes (834×200, 7×308 redirects, 0 blank); Playwright search/responsive/theme + changed-page regression
- Final status: PASS WITH NON-BLOCKING WARNINGS (reconnect Mintlify Git to org repo)
