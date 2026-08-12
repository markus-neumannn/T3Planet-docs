# URL Mismatches Only

**Scope:** only non-1:1 exceptions between original RTD canonical URLs and Mintlify canonical URLs

## Summary

| Type | Count |
|------|-------|
| Mintlify-only | 3 |
| RTD-only | 5 |
| Total mismatches | 8 |

## Actionable List

| Type | Product | Original RTD canonical URL | Mintlify canonical URL | Reason | Suggested Action |
|------|---------|----------------------------|------------------------|--------|------------------|
| mintlify_only | T3AF | `—` | `http://192.168.0.137:3000/ExtNsT3AF/Index` | New Mintlify hub page; no 1:1 RTD canonical page | Keep as Mintlify-only hub page |
| mintlify_only | AllTemplates | `—` | `http://192.168.0.137:3000/AllTemplates/Index` | New Mintlify hub page; no 1:1 RTD canonical page | Keep as Mintlify-only hub page |
| mintlify_only | AllExtensions | `—` | `http://192.168.0.137:3000/AllExtensions/Index` | New Mintlify hub page; no 1:1 RTD canonical page | Keep as Mintlify-only hub page |
| rtd_only | EXTAyu | `https://docs.t3planet.de/en/latest/EXTAyu/Localization/Installationt3ayu_reactjs.zip.html` | `—` | RTD-only zip artifact path; not migrated as Mintlify canonical page | Optional: create placeholder page or keep excluded from canonical page set |
| rtd_only | EXTReva | `https://docs.t3planet.de/en/latest/EXTReva/Localization/Installationt3reva_reactjs.zip.html` | `—` | RTD-only zip artifact path; not migrated as Mintlify canonical page | Optional: create placeholder page or keep excluded from canonical page set |
| rtd_only | EXTShiva | `https://docs.t3planet.de/en/latest/EXTShiva/Localization/Installationt3shiva_reactjs.zip.html` | `—` | RTD-only zip artifact path; not migrated as Mintlify canonical page | Optional: create placeholder page or keep excluded from canonical page set |
| rtd_only | history | `https://docs.t3planet.de/en/latest/history.html` | `http://192.168.0.137:3000/` | Legacy RTD utility page; not a canonical Mintlify documentation page | Keep redirect to home or leave out of canonical page set |
| rtd_only | readme | `https://docs.t3planet.de/en/latest/readme.html` | `http://192.168.0.137:3000/` | Legacy RTD utility page; not a canonical Mintlify documentation page | Keep redirect to home or leave out of canonical page set |
