# Production Readiness Audit — Mintlify vs Live-docs

**Date:** 2026-08-05  
**Live source of truth used:** `Live-docs/` (prefer **RST** over stale `_build/html` where they diverge)  
**Mintlify preview:** `http://127.0.0.1:3000/` (cache proxy) · LAN `http://192.168.0.113:3000/`  
**Public live site:** `https://docs.t3planet.de/en/latest/`

---

## Final release decision

### **Not Production Ready**

Mintlify content is **very close** to Live-docs after this migration pass, and is suitable for **manager walkthrough on `:3000`**, but it is **not** cleared for production cutover yet.

### Blocking before production

1. **Hosted Mintlify deploy required** — local `mint dev` + cache proxy is not a production surface (cold compiles, cache staleness, websocket noise).
2. **Search is inactive until Mintlify auth/hosting** — UI shows “Run mint login in the cli to activate search”.
3. **Live HTML build in `Live-docs/docs/_build/html` is stale** for some AI pages vs current RST (e.g. old T3AA Admin Tools copy in HTML while RST already matches T3AF). Production parity must track **RST + redeployed RTD**, not only the checked-in HTML build.
4. **Post-edit cache invalidation** — after MD changes, proxy can serve stale HTML until restart/warm (observed empty title / 0 embeds on cached hits).

### Non-blocking (accepted equivalents)

- Screenshot filenames converted to `.webp` with same visual content (`install_ext3.jpeg` → `install_ext.webp`, etc.).
- Product hub Index pages use Mintlify `CardGroup` instead of Sphinx toctree text (same destinations).
- EXTKarma live paths renamed (`ConfigureCaptcha` → `CaptchaConfiguration`, etc.) with **redirects added**.

---

## Documentation summary

| Metric | Count |
|--------|------:|
| Live HTML pages inventoried | 687 |
| Live RST pages inventoried | 741 |
| Mintlify EN markdown pages | ~791 |
| Live pages missing in Mintlify (after renames) | **0** |
| Pages migrated/updated this run (Supademo sync) | **24** (18 + 6) |
| Supademo embeds inserted from Live RST | **74** (47 + 27) |
| Remaining RST Supademo ID gaps | **0** |
| EXTKarma redirects added | **9** |
| License screenshots restored | **3** |
| Doc image refs broken (excluding `node_modules`) | **0** |

Artifacts:

- `scripts/qa-final/live-mint-parity-fresh.json`
- `scripts/qa-final/production-parity-strict.json`
- `scripts/qa-final/rst-supademo-sync-report.json`
- `scripts/qa-final/rst-supademo-gaps.json`
- `scripts/qa-final/production-e2e-final.json`
- `scripts/sync_supademo_from_rst.py` (new)

---

## Content comparison summary

### Missing pages

Initially flagged:

- `EXTKarma/ConfigureCaptcha/Index`
- `EXTKarma/CustomElements/Index`
- `EXTKarma/UpgradeGuide/Index`

**Resolution:** Content exists under renamed Mintlify paths with richer/equal body text:

| Live path | Mintlify path |
|-----------|---------------|
| ConfigureCaptcha | CaptchaConfiguration |
| CustomElements | ContentBlockElements |
| UpgradeGuide | UpgradeGuideForContainer |

Redirects added in `docs.json` for `.html` and clean URLs.

### Supademos

- HTML-build sync reported 0 gaps (stale HTML).
- **RST sync found real gaps** (unquoted `src=` iframes in RST).
- Migrated missing embeds into Mintlify MD; **0 remaining RST ID gaps**.
- Notable fix: `ExtNsT3AA/Configuration/Index.md` now includes all **5** Live RST Supademos (removed stale wrong ID).

### Images

- Strict basename compare flagged ~79 pages; almost all are **equivalent WebP renames** (files present under `images/`).
- Restored explicit screenshots on `License/UpdateVersion/CheckNewVersion/Index.md` (were present on disk but not referenced).

### Headings / copy

- Many “missing heading” hits were Sphinx `permalink` noise (`… Link`) or intentional title branding (`EXT:ns_*` vs marketing H1).
- FAQ / Support stubs match Live (short pages that link to t3planet.de).
- Product Index pages are card hubs (expected Mintlify pattern).

---

## QA summary

### Functional / E2E (local `:3000`)

| Check | Result |
|-------|--------|
| Home, T3AF, T3AA Config, CKEditor Supademo, T3AI Translation, License CheckNewVersion, Karma Captcha | Pass |
| Karma old URLs redirect to new titles | Pass (`CustomElements` → Content Block Elements, `UpgradeGuide` → Upgrade Guide For Container) |
| Broken images on sampled pages | None |
| Theme / prev-next / logo (prior suite) | Pass |
| Copy code (prior suite) | Pass |
| Search results | **Blocked** (Mintlify login) |

### Responsive

| Viewport | Overflow-X | Notes |
|----------|------------|-------|
| Desktop 1440 | No | T3AA Configuration OK |
| Tablet 768 | No | 5 iframes in DOM after warm |
| Mobile 390 | No | 5 iframes in DOM after warm |

Screenshots: `scripts/qa-final/prod-*-t3aa-config.png`

### Browsers

| Engine | Result |
|--------|--------|
| Chromium | Pass |
| Firefox | Pass (License) |
| WebKit | Pass (License) |
| Edge | Not installed (Chromium-equivalent expected) |

### Performance

- Warm cached pages: fast on `:3000`.
- Cold mint compiles: multi-second (not production-grade).
- After content edits: **must restart/warm proxy** or reviewers see stale pages.

### Console

- Local-only socket.io / Lucide preload noise via cache proxy — not a production CDN issue.

---

## What was fixed in this session

1. Built fresh Live-docs ↔ Mintlify inventory and parity reports.
2. Synced **74** missing Supademo embeds from Live RST → Mintlify MD.
3. Cleaned stale wrong Supademo on T3AA Configuration.
4. Restored License “Check New Version” screenshots.
5. Added **9** EXTKarma legacy URL redirects.
6. Re-tested navigation/responsive/browsers on critical pages after cache restart.

---

## Required actions before marking Production Ready

1. **Deploy to Mintlify hosting** (production CDN + search indexing).
2. Confirm search works on the hosted URL (not localhost).
3. Rebuild/publish Live RTD from current RST so public live HTML matches the RST SoT we migrated from.
4. Warm/purge caches after every content push.
5. Spot-check T3AI Translation / SEO / Pages / Media / AS Configuration on the **hosted** URL for embed count and layout.
6. Optional: regenerate any remaining JPEG references to WebP consistently if brand wants one format only.

---

## Bottom line

| Question | Answer |
|----------|--------|
| Does Mintlify miss whole Live pages? | **No** (after renames/redirects) |
| Do Live RST Supademos match Mintlify? | **Yes — 0 ID gaps after migration** |
| Are images effectively present? | **Yes** (WebP equivalents + License restore) |
| Ready for manager demo on LAN `:3000`? | **Yes, with caveats** (use `:3000`, hard refresh after restart, don’t demo search) |
| Ready for production cutover? | **No — not until hosted Mintlify deploy + search + cache strategy are verified** |
