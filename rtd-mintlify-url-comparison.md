# RTD vs Mintlify URL Comparison

**Comparison type:** one-to-one canonical page mapping

## Summary

| Metric | Count |
|--------|-------|
| Mintlify canonical pages | 703 |
| Exact structural 1:1 matches | 700 |
| Mintlify-only hub pages | 3 |
| RTD-only canonical pages without Mintlify twin | 5 |

## Interpretation

- `exact_structural_match`: same page exists in both systems; only the URL format changed.
- `mintlify_only_hub`: new Mintlify landing/hub page, so no old RTD canonical equivalent exists.
- `rtd_only`: old RTD canonical page with no 1:1 Mintlify canonical page.

## URL Rule

- Original RTD canonical: `https://docs.t3planet.de/en/latest/<route>.html`
- Mintlify canonical: `http://192.168.0.137:3000/<route>`
- Example: `https://docs.t3planet.de/en/latest/License/Index.html` -> `http://192.168.0.137:3000/License/Index`

## Mintlify-Only Hub Pages

- `http://192.168.0.137:3000/T3AF/Index` — New Mintlify hub page; no 1:1 RTD canonical page
- `http://192.168.0.137:3000/AllExtensions/Index` — New Mintlify hub page; no 1:1 RTD canonical page
- `http://192.168.0.137:3000/AllTemplates/Index` — New Mintlify hub page; no 1:1 RTD canonical page

## RTD-Only Canonical Pages

- `https://docs.t3planet.de/en/latest/EXTAyu/Localization/Installationt3ayu_reactjs.zip.html` — RTD-only artifact path not migrated as a canonical Mintlify page
- `https://docs.t3planet.de/en/latest/EXTReva/Localization/Installationt3reva_reactjs.zip.html` — RTD-only artifact path not migrated as a canonical Mintlify page
- `https://docs.t3planet.de/en/latest/EXTShiva/Localization/Installationt3shiva_reactjs.zip.html` — RTD-only artifact path not migrated as a canonical Mintlify page
- `https://docs.t3planet.de/en/latest/history.html` — Legacy RTD utility page redirected to home in Mintlify
- `https://docs.t3planet.de/en/latest/readme.html` — Legacy RTD utility page redirected to home in Mintlify

## Sample Exact 1:1 Matches

| Original RTD canonical URL | Mintlify canonical URL |
|----------------------------|------------------------|
| `https://docs.t3planet.de/en/latest/EXTAvatar/Customization/Index.html` | `http://192.168.0.137:3000/EXTAvatar/Customization/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/EditorGuide/Index.html` | `http://192.168.0.137:3000/EXTAvatar/EditorGuide/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/GlobalSettingsConfiguration/Index.html` | `http://192.168.0.137:3000/EXTAvatar/GlobalSettingsConfiguration/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/HelpSupport/Index.html` | `http://192.168.0.137:3000/EXTAvatar/HelpSupport/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/HelpfulLinks/Index.html` | `http://192.168.0.137:3000/EXTAvatar/HelpfulLinks/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/Index.html` | `http://192.168.0.137:3000/EXTAvatar/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/Installation/Index.html` | `http://192.168.0.137:3000/EXTAvatar/Installation/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/Introduction/Index.html` | `http://192.168.0.137:3000/EXTAvatar/Introduction/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/Localization/Index.html` | `http://192.168.0.137:3000/EXTAvatar/Localization/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/MaskElements/Index.html` | `http://192.168.0.137:3000/EXTAvatar/MaskElements/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/SEO/Index.html` | `http://192.168.0.137:3000/EXTAvatar/SEO/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/SpeedPerformance/Index.html` | `http://192.168.0.137:3000/EXTAvatar/SpeedPerformance/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/TemplatesLayouts/Index.html` | `http://192.168.0.137:3000/EXTAvatar/TemplatesLayouts/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/UpdateVersion/Index.html` | `http://192.168.0.137:3000/EXTAvatar/UpdateVersion/Index` |
| `https://docs.t3planet.de/en/latest/EXTAvatar/UpgradeGuide/Index.html` | `http://192.168.0.137:3000/EXTAvatar/UpgradeGuide/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/CustomElements/Index.html` | `http://192.168.0.137:3000/EXTAyu/CustomElements/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/Customization/Index.html` | `http://192.168.0.137:3000/EXTAyu/Customization/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/DemoSite/Index.html` | `http://192.168.0.137:3000/EXTAyu/DemoSite/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/FAQ/Index.html` | `http://192.168.0.137:3000/EXTAyu/FAQ/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/GlobalSettingsConfiguration/Index.html` | `http://192.168.0.137:3000/EXTAyu/GlobalSettingsConfiguration/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/HelpSupport/Index.html` | `http://192.168.0.137:3000/EXTAyu/HelpSupport/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/Index.html` | `http://192.168.0.137:3000/EXTAyu/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/InstallationT3AyuReactjs/Index.html` | `http://192.168.0.137:3000/EXTAyu/InstallationT3AyuReactjs/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/InstallationT3AyuTheme/Index.html` | `http://192.168.0.137:3000/EXTAyu/InstallationT3AyuTheme/Index` |
| `https://docs.t3planet.de/en/latest/EXTAyu/Introduction/Index.html` | `http://192.168.0.137:3000/EXTAyu/Introduction/Index` |

## Full Dataset

- Markdown report: `rtd-mintlify-url-comparison.md`
- CSV report: `scripts/rtd_mintlify_url_comparison.csv`

The CSV contains all rows for spreadsheet-style review.
