# Navigation + Icon Smoothness Test Cycle

**Verdict:** PASS (7 passed, 0 failed)

## Fixes

- Early `bindHardNavClicks()` so first home click is not lost to Mintlify SPA
- `hardNavigate`: `window.stop()` then deferred `location.assign` (HOL-safe)
- Canonicalize `/…/index` → `/…/Index`; path-scoped cache purge
- Responsive product icon shells centered and sized for phones

## Results

- PASS **home_first_click**: `{"fails": 0, "n": 15, "p50": 237, "hubs": ["/AllTemplates/Index", "/AllExtensions/Index", "/AIFoundationExtensions/Index", "/License/Index", "/ExtNsT3AF/Index"]}`
- PASS **icons_390**: `{"bad": 0, "n": 8, "sample": [{"sw": 44, "gw": 22, "dx": 0, "dy": 0}, {"sw": 44, "gw": 22, "dx": 0, "dy": 0}]}`
- PASS **icons_420**: `{"bad": 0, "n": 8, "sample": [{"sw": 44, "gw": 22, "dx": 0, "dy": 0}, {"sw": 44, "gw": 22, "dx": 0, "dy": 0}]}`
- PASS **icons_768**: `{"bad": 0, "n": 8, "sample": [{"sw": 40, "gw": 20, "dx": 0, "dy": 0}, {"sw": 40, "gw": 20, "dx": 0, "dy": 0}]}`
- PASS **lowercase_index_canon**: `{"path": "/AllTemplates/Index"}`
- PASS **warm_usable**: `{"samples": [305, 288, 257, 256], "p50": 288}`
- PASS **mobile_home_click**: `{"path": "/AllTemplates/Index", "dest": "/AllTemplates/Index"}`
