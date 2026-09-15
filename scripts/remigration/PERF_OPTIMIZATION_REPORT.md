# Documentation performance optimization

Date: 2026-09-15  
Environment: local preview `:3000` cache proxy → `:3001` mint

## Changes shipped

1. **WebP retarget (content)** — 236 new WebP siblings for MD-referenced PNG/JPEG; **249** markdown image refs updated across **135** pages. Verified **1042** image refs OK / **0** broken. Saved **~8.4 MB** vs source rasters for converted set. Remaining MD refs are almost all `.webp` (1026), with a few tiny PNG/JPEG left.
2. **Minified published assets** — `custom.css` **111 KB** (−27%), `_static/t3-docs.min.js` **58 KB** (−26%).
3. **Cache proxy** — `__t3_cache_warm?all=1` fixed; warm waits for mint readiness + retries; sequential warm uses the compile gate (no more skipped hubs); expanded `WARM_PATHS` (DPA, AIPermissions, product hubs).
4. **Preview starter** — `start_fast_preview.sh` reuses a healthy mint on `:3001` instead of killing mintlify-dev’s process (avoids restart/502 loops).

## Measured timings (local `:3000`)

| Mode | Sample | Result |
|------|--------|--------|
| Cold first compile | `/`, `/License/Index` | ~23–27 s (mint MDX cost) |
| Subsequent cold (compiled) | most hubs | ~1.3–3 s |
| **Warm cache HIT** | 12/12 hubs | **~1.3 ms avg** (max ~3 ms) |

Proxy stats after run: `hits=15`, `entries=16`.

## How to browse fast

Use **http://127.0.0.1:3000/** (or LAN `:3000`), not raw mint `:3001`. After deploy, Mintlify CDN serves prebuilt HTML; WebP + minified CSS/JS still reduce transfer on every page.
