# Live Content Parity — August 2026

**Generated:** 2026-08-10T08:37:08.675612+00:00
**Repo:** `/Users/nitsan/www/AI Agents/Mintilify Doc`
**Live base:** https://docs.t3planet.de/en/latest/

## Summary counts

- Live pages audited: **741**
- missing_page: **0**
- missing_supademo: **0**
- thin_content: **9**
- missing_images: **0**
- ok (no issues): **732**
- fetch_failed: **0**

## Top gaps

### Missing pages


### Missing Supademo


### Thin content (worst ratios)

- `ExtRTECKEditorPack/Index` ratio=0.0 live=1915 mint=0 file=`ExtRTECKEditorPack/Index.md`
- `License/Index` ratio=0.0 live=1741 mint=0 file=`License/Index.md`
- `ExtNsRevolutionSlider/Index` ratio=0.04 live=1715 mint=68 file=`ExtNsRevolutionSlider/Index.md`
- `ExtNsT3AF/Index` ratio=0.081 live=3633 mint=293 file=`ExtNsT3AF/Index.md`
- `ExtNsT3AS/Index` ratio=0.094 live=3130 mint=293 file=`ExtNsT3AS/Index.md`
- `ExtNsT3AC/Index` ratio=0.099 live=2784 mint=277 file=`ExtNsT3AC/Index.md`
- `ExtNsT3AI/Index` ratio=0.105 live=2376 mint=250 file=`ExtNsT3AI/Index.md`
- `index` ratio=0.142 live=12470 mint=1770 file=`index.md`
- `ExtNsT3AA/Index` ratio=0.174 live=1551 mint=270 file=`ExtNsT3AA/Index.md`

### Missing images



## After migration

**Validated:** 2026-08-10T08:37:18.491134+00:00

### Before → After

| Issue | Before | After |
|------|--------|-------|
| missing_page | 0 | 0 |
| missing_supademo | 1 | 0 |
| thin_content | 9 | 9 |

### What changed

- Patched `License/GenerateLicenseKey/Index.md`: inserted missing Supademo embeds (`cmshc993i0pb3qmaaoqrn3oma`, `cmshcdtkx0pe3qmaa5qqg8dw1`) and appended live sections **Get Trial License from Backend** + **Purchase License from Backend** (kept existing Mintlify website flow).
- EXTKarma redirects (`ConfigureCaptcha` → `CaptchaConfiguration`, `CustomElements` → `ContentBlockElements`, `UpgradeGuide` → `UpgradeGuideForContainer`) already present in `docs.json` — no duplicates created.
- Remaining `thin_content` (9) are intentional Mintlify hub/landing pages (`CardGroup` / `t3-template-landing` / home) with no live h2/h3 gaps to append — left unchanged per “do not wipe CardGroups”.

### Live fetch note

Cloudflare challenged `docs.t3planet.de` (HTTP 429 / `cf-mitigated: challenge`) during the full crawl. Audit + migration used the local Sphinx HTML build at `T3Planet Docs Agent/docs/docs/_build/html` as fallback (not a Live-docs folder). Re-run with live network when CF clears (`PARITY_LOCAL_ONLY=0`).

### HTTP checks

- `curl http://127.0.0.1:3000/ExtNsT3AF/Index` → **200**
- `curl http://127.0.0.1:3000/License/GenerateLicenseKey/Index` → **200**

### Files created/modified

- Created: `scripts/qa-final/live_content_parity_aug2026.py`
- Created: `scripts/qa-final/LIVE_CONTENT_PARITY_AUG2026.json`
- Created: `scripts/qa-final/LIVE_CONTENT_PARITY_AUG2026.md`
- Created: `scripts/qa-final/LIVE_CONTENT_MIGRATION_AUG2026.json`
- Modified: `License/GenerateLicenseKey/Index.md`


## Image / Supademo deep scan (August 2026)

**Generated:** 2026-08-10T08:39:07.560087+00:00
**Sphinx HTML:** `/Users/nitsan/www/AI Agents/T3Planet Docs Agent/docs/docs/_build/html`
**Repo:** `/Users/nitsan/www/AI Agents/Mintilify Doc`

### Counts

| Metric | Value |
|--------|-------|
| pages_scanned | 754 |
| missing_supademo_before | 0 |
| missing_supademo_after | 0 |
| missing_images_before | 116 |
| missing_images_after | 0 |
| files_modified | 66 |
| image_copies | 116 |
| image_downloads | 0 |
| download_cap | 200 |

### Live sample (15 pages, 1s sleep)

- Status: **blocked_429**
- HTTP 200: 0
- HTTP 429: 2
- Blocked: True
- Attempted: 2

### Notes

- Image matching: Sphinx `img` basenames vs Mintlify `![]()` / `<img src>` and on-disk `{page}/images/`; `.webp`/`.png` swaps accepted.
- Prefer copy from Sphinx `_images/`; network download only when missing locally (capped at 200).
- Supademo inserts use `t3-embed` iframe blocks (same format as `scripts/sync_supademo_from_live.py`).
- No content deleted.

### Sample remaining gaps (after)


No remaining missing Supademo IDs after sync.

No remaining missing images (or only unresolved after download cap).

