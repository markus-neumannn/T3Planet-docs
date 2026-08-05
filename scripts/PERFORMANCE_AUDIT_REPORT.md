# T3Planet Docs — Performance Audit Report

**Base URL:** http://127.0.0.1:3000
**Pages tested:** 10

## Summary

| Metric | Value |
|--------|-------|
| Median DOM ready (cold) | 20497 ms |
| Max DOM ready (cold) | 55240 ms |
| Median SPA navigation (warm) | 12994 ms |
| Max SPA navigation (warm) | 57851 ms |
| Mobile home DOM ready | 39011 ms |
| Console errors (sample) | 27 |

## Page Results

| Page | DOM (ms) | Load (ms) | LCP (ms) | CLS | Transfer (KB) | Sidebar links |
|------|----------|-----------|----------|-----|---------------|---------------|
| Home | 52263 | 296 | — | — | 1877.7 | 0 |
| AI Foundation | 55240 | 139 | — | — | 241.1 | 19 |
| Templates | 41398 | 27 | — | — | 1.3 | 4 |
| Extensions | 31544 | 57 | — | — | 1.3 | 4 |
| License | 21401 | 41 | — | — | 1.3 | 22 |
| T3AA Hub | 19593 | 16 | — | — | 0.6 | 19 |
| T3AA Screenshots | 14939 | 54 | — | — | 1.3 | 19 |
| T3AA System Req | 18991 | 32 | — | — | 0.6 | 19 |
| T3AI Hub | 15250 | 25 | — | — | 0.9 | 24 |
| T3 Karma Template | 11118 | 37 | — | — | 0.6 | 19 |

## SPA Navigation (warm)

| From → To | ms |
|-----------|-----|
| /ExtNsT3AA/Index → /ExtNsT3AA/Screenshots/Index | 57851 |
| /ExtNsT3AA/Screenshots/Index → /ExtNsT3AA/SystemRequirements/Index | 10528 |
| /ExtNsT3AA/SystemRequirements/Index → /ExtNsT3AA/Installation/Index | 12994 |
