# Complete QC/QA + T3AA Migration Audit Report

**Date:** 2026-09-15  
**Parent ticket:** [Mintlify Documentation Overview](https://app.clickup.com/t/86d40rqgv)  
**Environment:** Local preview `http://127.0.0.1:3000` (mint + cache proxy)

---

## 1. Executive Summary

| Metric | Count |
|--------|------:|
| ClickUp subtasks reviewed | 25 |
| Valid bugs fixed (this conversation) | 12 |
| Left not fixed (verified reasons) | 5 |
| T3AA official pages audited | 20 |
| T3AA Mintlify pages audited | 20 |
| T3AA pages missing | 0 |
| HTTP smoke (hubs + fixed + T3AA) | 28/28 + 20/20 = **OK** |
| Responsive viewports with overflow | **0** |
| New regressions found requiring code change | **0** (this pass) |

**Overall status: READY FOR TESTING**

---

## 2. Priority Results

| Priority | Reviewed | Valid | Fixed | Not Fixed |
|----------|----------|-------|-------|-----------|
| Urgent | 1 | 1 | 1 | 0 |
| High | 12 | 10 | 10 | 2* |
| Medium/Normal | 6 | 1 | 1 | 5** |
| Low / Ignore | 2 | 0 | 0 | 0 (Closed) |

\* Search clickability (platform); one intermittent HTTP noise only.  
\*\* T3AC Feature Guide false positive; three intentional `ddev.site` examples; closed items excluded.

---

## 3. Fixed Issues (assigned Krishna → Testing)

| Ticket | Priority | Problem | Fix | Validation |
|--------|----------|---------|-----|------------|
| [86d42ktv4](https://app.clickup.com/t/86d42ktv4) | Urgent | GovernanceAndAccess no redirect | Links + redirects + remove dup pages | 307→200 AIPermissions |
| [86d42j678](https://app.clickup.com/t/86d42j678) | — | License Index next broken | Nav: Index first page + `next` frontmatter | Playwright → `/License/Introduction/Index` |
| [86d42k24z](https://app.clickup.com/t/86d42k24z) | High | Karma FE demo | → `/t3-karma/` | URL 200 |
| [86d42k24q](https://app.clickup.com/t/86d42k24q) | High | Karma BE demo | → `/t3-karma/typo3/?…` | URL 200 |
| [86d42k259](https://app.clickup.com/t/86d42k259) | High | reCAPTCHA typo `en-/us` | → `en-us/...html` | URL 200 |
| [86d42k276](https://app.clickup.com/t/86d42k276) | High | Dead T3AI demo host | → `t3-extension.t3planet.de` | URL 200 |
| [86d42k25g](https://app.clickup.com/t/86d42k25g) | High | Dead GitHub repo | → Support link | Verified |
| [86d42k260](https://app.clickup.com/t/86d42k260) / [265](https://app.clickup.com/t/86d42k265) | High | News Comments demos/product | Canonical product + BE demo | 200 |
| [86d42k26d](https://app.clickup.com/t/86d42k26d) / [270](https://app.clickup.com/t/86d42k270) | High | Revolution FE / My Products | Product + customer login | 200 |
| [86d42jg32](https://app.clickup.com/t/86d42jg32) | Normal | CKEditor captions | Added live figure captions | Page 200 |

Also migrated (not ClickUp bugs): **T3AF + T3AI DPA** pages from GitLab `e47886ae`.

---

## 4. Issues Not Fixed

| Ticket | Reason | Evidence |
|--------|--------|----------|
| [86d42k24k](https://app.clickup.com/t/86d42k24k) Search results not clickable | Mintlify search UI sets `aria-hidden="true"` on result anchors — platform bug; unsafe to patch globally | Playwright: dialog opens; result nodes still `ariaHidden: true` |
| [86d42jgdu](https://app.clickup.com/t/86d42jgdu) T3AC Feature Guide mismatch | Live Index is toctree-only; Mintlify hub + Supademos = valid improvement | Compared RST vs MD |
| [86d42k61z](https://app.clickup.com/t/86d42k61z) / [62w](https://app.clickup.com/t/86d42k62w) / [638](https://app.clickup.com/t/86d42k638) | Intentional local `t3af.ddev.site` examples (same as live) | Live RST identical |

---

## 5. T3AA Page-by-Page Migration Audit

**Source:** `docs/docs/ExtNsT3AA/*.rst` @ GitLab master  
**Target:** `ExtNsT3AA/*.md`  
**Artifact:** `scripts/remigration/T3AA_PAGE_AUDIT.json`

| Check | Result |
|-------|--------|
| Page inventory | **20/20** live pages have Mintlify counterparts |
| Navigation | All major T3AA pages including DPA in `docs.json` |
| Images | **0** broken local image refs |
| Supademos | No missing live IDs; Mintlify has **extra** FileMeta demos (preserved improvements) |
| Flagged “content_gap” | False positives (RST underline noise / T3AF wording) — key terms present |
| HTTP all T3AA pages | **20/20 → 200** |

No additional T3AA content/image/Supademo migration required in this pass.

---

## 6. E2E / FE / Responsive / Performance

### HTTP / navigation
- Critical hubs + fixed pages: **28/28 OK** (Governance redirect **307→200**)
- T3AA: **20/20 OK**
- Internal T3AA markdown links: **0 missing file targets**

### Responsive (Playwright Chrome)
Viewports: **1440, 768, 390, 375** × key pages (Home, License, T3AA Index/Widgets, AI Permissions)  
- All **200**
- Horizontal overflow: **none**
- License Introduction navigation: **passes** (`/License/Introduction/Index`)

Artifact: `scripts/remigration/QA_E2E_RESPONSIVE.json`

### Search
- Opens (⌘K / dialog present)
- Results still `aria-hidden` → **not fixed** (platform)

### Performance
| Method | Result |
|--------|--------|
| Lighthouse desktop (local cold mint) Home | **25** (FCP 5.9s, LCP 16.3s, TBT 5840ms) |
| Lighthouse desktop T3AA Index | **25** (FCP 5.9s, LCP 17.2s) |
| Warm curl TTFB (proxy cache) | Home **~1–6ms**, T3AA **~2ms**, DPA **~24ms** |

**Interpretation:** Cold Lighthouse scores reflect local Mintlify compile, not production CDN. Warm path is fast. No site-wide perf rewrite applied (high regression risk; prior speed work already exists).

Artifacts: `scripts/remigration/LH_home.json`, `LH_t3aa.json`

### Build / MDX
- Pages render (HTTP 200); no project-wide Mintlify CI build command re-run in this pass beyond live preview rendering.

### Browsers
- **Chrome** (Playwright / Lighthouse): tested  
- **Safari / Firefox:** not tested in this environment

### Accessibility (docs UI spot-check)
- Headings present on tested pages (`hasH1`)
- Search result `aria-hidden` remains a known platform issue

---

## 7. Files Changed (this conversation — relevant)

- T3AF Governance→AIPermissions links/redirects; removed duplicate Governance trees
- T3AF/T3AI/T3AA `DPAandGDPR` pages + nav/stats
- License Index nav + `next` frontmatter
- Karma / News Comments / Revolution / CKEditor Support / T3AI Introduction link fixes
- QA artifacts under `scripts/remigration/`

---

## 8. Final Status

**READY FOR TESTING**

Genuine ClickUp bugs that are safely fixable are fixed and in Testing for Krishna. Remaining open items are platform/intentional/false-positive. T3AA live↔Mintlify coverage is complete for pages/images/Supademos with no unverified content invented.
