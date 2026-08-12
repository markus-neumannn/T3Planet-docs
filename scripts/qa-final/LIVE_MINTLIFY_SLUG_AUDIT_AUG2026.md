# Live RTD vs Mintlify Slug Audit — August 2026

**Repo:** `/Users/nitsan/www/AI Agents/Mintilify Doc`

## Summary counts

| Metric | Count |
| --- | ---: |
| total_live_pages | 746 |
| total_mintlify_pages_canonical | 779 |
| total_mintlify_Index_md | 664 |
| total_nav_page_entries | 674 |
| LIVE_ONLY | 39 |
| MINT_ONLY | 73 |
| CASE_MISMATCH | 0 |
| PATH_MISMATCH_known_renames | 0 |
| redirects_in_docs_json | 1398 |
| LIVE_ONLY_with_redirect | 1 |
| LIVE_ONLY_without_redirect | 38 |
| LIVE_ONLY_content | 35 |
| LIVE_ONLY_sphinx_utils | 4 |

### Sources

- **objects_inv:** 746
- **rtd_index_html:** 664
- **toc_markdown_latest_0:** 661
- **live_union_html_paths:** 746
- **sitemap_xml:** 404 not available
- **Live-docs mirror:** Live-docs/ mirror not present in repo

## Top-level products

- Shared tops: 68
- Live-only tops: ExtNsT3AF, genindex, history, py-modindex, readme, search
- Mint-only tops: AIFoundationExtensions, AllExtensions, AllTemplates, SLA-skills, T3AF

### Navigation order notes

- Live RTD still exposes **ExtNsT3AF** as a product tree; Mintlify renamed it to **T3AF**.
- Mintlify-only hubs: **AllExtensions**, **AllTemplates**, **AIFoundationExtensions**.
- Special-character folders: live uses percent-encoding (`%26`, `%28`/`%29`); Mintlify uses literal `&` / `()` in path segments.
- Sphinx utility pages (`genindex`, `search`, `py-modindex`, `history`) appear in live inventory but are not Mintlify content pages.

Mintlify navigation labels (sample):

- **Home** — index, AIFoundationExtensions/Index, AllTemplates/Index, AllExtensions/Index
- **Get Started** — License & Installation
- **License & Installation** — License/Introduction/Index, License/GenerateLicenseKey/Index, License/LicenseManager/Index, License/ExtendTrial/Index, License/RenewPurchase/Index
- **AI Universe Extensions** — T3AF, T3AA, T3AB, T3AC, T3AI
- **T3AF** — ExtNsT3AF/Introduction/Index, ExtNsT3AF/Installation/Index, Configuration, Integrations, User Guide
- **Configuration** — ExtNsT3AF/Configuration/Index, ExtNsT3AF/Configuration/Dashboard/Index, ExtNsT3AF/Configuration/AIProviders/Index, ExtNsT3AF/Configuration/AIContext/Index, ExtNsT3AF/Configuration/AIPrompts/Index
- **Integrations** — ExtNsT3AF/Integrations/Index, ExtNsT3AF/Integrations/MCPServer/Index, ExtNsT3AF/Integrations/MCPTools/Index, ExtNsT3AF/Integrations/MCPTesting/Index
- **User Guide** — ExtNsT3AF/UserGuide/Index, ExtNsT3AF/UserGuide/RolesAndDailyUse/Index
- **Developer Guide** — ExtNsT3AF/DeveloperGuide/Index, ExtNsT3AF/DeveloperGuide/Architecture/Index, ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index, ExtNsT3AF/DeveloperGuide/CustomProviders/Index, ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index
- **Troubleshooting** — ExtNsT3AF/Troubleshooting/Index, ExtNsT3AF/Troubleshooting/KnownProblems/Index, ExtNsT3AF/Troubleshooting/FAQ/Index
- **T3AA** — ExtNsT3AA/Introduction/Index, ExtNsT3AA/Screenshots/Index, ExtNsT3AA/SystemRequirements/Index, ExtNsT3AA/Installation/Index, ExtNsT3AA/ReInstallEverything/Index
- **Updates** — ExtNsT3AA/UpdateVersion/Index
- **T3AB** — ExtNsT3AB/Introduction/Index, ExtNsT3AB/SystemRequirements/Index, ExtNsT3AB/Installation/Index, ExtNsT3AB/Configuration/Index, ExtNsT3AB/HowT3ABWorks/Index
- **Updates** — ExtNsT3AB/UpdateVersion/Index
- **T3AC** — ExtNsT3AC/Introduction/Index, ExtNsT3AC/Screenshots/Index, ExtNsT3AC/Installation/Index, ExtNsT3AC/ReInstallEverything/Index, ExtNsT3AC/Configuration/Index
- **Custom LLM** — ExtNsT3AC/CustomLLMSupport/Index, ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites&SOWCustomLLM/Index, ExtNsT3AC/CustomLLMSupport/T3ACHostingPolicyforCustomLLM/Index
- **Features** — ExtNsT3AC/FeatureGuide/Index, ExtNsT3AC/FeatureGuide/Dashboard/Index, ExtNsT3AC/FeatureGuide/DataSource/Index, ExtNsT3AC/FeatureGuide/TrainingCenter/Index, ExtNsT3AC/FeatureGuide/Chatbot/Index
- **Updates** — ExtNsT3AC/UpdateVersion/Index
- **T3AI** — ExtNsT3AI/Introduction/Index, ExtNsT3AI/Screenshots/Index, ExtNsT3AI/VideoTutorials/Index, ExtNsT3AI/SystemRequirements/Index, ExtNsT3AI/Installation/Index
- **Updates** — ExtNsT3AI/UpdateVersion/Index
- **T3AL** — ExtNsT3AL/Introduction/Index, ExtNsT3AL/Screenshots/Index, ExtNsT3AL/VideoTutorials/Index, ExtNsT3AL/SystemRequirements/Index, ExtNsT3AL/Installation/Index
- **Updates** — ExtNsT3AL/UpdateVersion/Index
- **T3AS** — ExtNsT3AS/Introduction/Index, ExtNsT3AS/Screenshots/Index, ExtNsT3AS/Installation/Index, ExtNsT3AS/ReInstallEverything/Index, ExtNsT3AS/Configuration/Index
- **Custom LLM** — ExtNsT3AS/CustomLLMSupport/Index, ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites&SOWCustomLLM/Index, ExtNsT3AS/CustomLLMSupport/T3ASHostingPolicyforCustomLLM/Index
- **Updates** — ExtNsT3AS/UpdateVersion/Index

## LIVE_ONLY

Total: **39** (content: **35**, sphinx utils: **4**)

- `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index`
- `/ExtNsT3AF/Configuration/AIContext/Index`
- `/ExtNsT3AF/Configuration/AIFeatures/Index`
- `/ExtNsT3AF/Configuration/AIPermissions/Index`
- `/ExtNsT3AF/Configuration/AIPrompts/Index`
- `/ExtNsT3AF/Configuration/AIProviders/Index`
- `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index`
- `/ExtNsT3AF/Configuration/Dashboard/Index`
- `/ExtNsT3AF/Configuration/Index`
- `/ExtNsT3AF/DeveloperGuide/Architecture/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index`
- `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index`
- `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index`
- `/ExtNsT3AF/DeveloperGuide/Index`
- `/ExtNsT3AF/HelpfulLinks/Index`
- `/ExtNsT3AF/Index`
- `/ExtNsT3AF/Installation/Index`
- `/ExtNsT3AF/Integrations/Index`
- `/ExtNsT3AF/Integrations/MCPServer/Index`
- `/ExtNsT3AF/Integrations/MCPTesting/Index`
- `/ExtNsT3AF/Integrations/MCPTools/Index`
- `/ExtNsT3AF/Introduction/Index`
- `/ExtNsT3AF/Support/Index`
- `/ExtNsT3AF/Troubleshooting/FAQ/Index`
- `/ExtNsT3AF/Troubleshooting/Index`
- `/ExtNsT3AF/Troubleshooting/KnownProblems/Index`
- `/ExtNsT3AF/UserGuide/Index`
- `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index`
- `/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index`
- `/ExtNsT3AL/T3ALTerms%28Glossary%29/Index`
- `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index`
- `/genindex`
- `/history`
- `/py-modindex`
- `/search`

## PATH_MISMATCH / known renames

| Live | Mintlify | Reason | Target exists |
| --- | --- | --- | --- |
| `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index` | `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites&SOWCustomLLM/Index` | url_decode_special_chars | True |
| `/ExtNsT3AF/Configuration/AIContext/Index` | `/ExtNsT3AF/Configuration/AIContext/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIFeatures/Index` | `/ExtNsT3AF/Configuration/AIFeatures/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIPermissions/Index` | `/ExtNsT3AF/Configuration/AIPermissions/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIPrompts/Index` | `/ExtNsT3AF/Configuration/AIPrompts/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIProviders/Index` | `/ExtNsT3AF/Configuration/AIProviders/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index` | `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/Dashboard/Index` | `/ExtNsT3AF/Configuration/Dashboard/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/Index` | `/ExtNsT3AF/Configuration/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/Architecture/Index` | `/ExtNsT3AF/DeveloperGuide/Architecture/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index` | `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index` | `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index` | `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index` | `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index` | `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index` | `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index` | `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/Index` | `/ExtNsT3AF/DeveloperGuide/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/HelpfulLinks/Index` | `/ExtNsT3AF/HelpfulLinks/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Index` | `/ExtNsT3AF/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Installation/Index` | `/ExtNsT3AF/Installation/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/Index` | `/ExtNsT3AF/Integrations/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/MCPServer/Index` | `/ExtNsT3AF/Integrations/MCPServer/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/MCPTesting/Index` | `/ExtNsT3AF/Integrations/MCPTesting/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/MCPTools/Index` | `/ExtNsT3AF/Integrations/MCPTools/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Introduction/Index` | `/ExtNsT3AF/Introduction/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Support/Index` | `/ExtNsT3AF/Support/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Troubleshooting/FAQ/Index` | `/ExtNsT3AF/Troubleshooting/FAQ/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Troubleshooting/Index` | `/ExtNsT3AF/Troubleshooting/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Troubleshooting/KnownProblems/Index` | `/ExtNsT3AF/Troubleshooting/KnownProblems/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/UserGuide/Index` | `/ExtNsT3AF/UserGuide/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index` | `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index` | `/ExtNsT3AL/SeamlessXLIFFImport&Export/Index` | url_decode_special_chars | True |
| `/ExtNsT3AL/T3ALTerms%28Glossary%29/Index` | `/ExtNsT3AL/T3ALTerms(Glossary)/Index` | url_decode_special_chars | True |
| `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index` | `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites&SOWCustomLLM/Index` | url_decode_special_chars | True |

## Redirect coverage (docs.json)

- docs.json redirects total: **1398**
- Sources containing `ExtNsT3AF`: **0**
- Sources containing `AIUniverse`: **12**
- Sources containing `AIFoundation`: **10**
- LIVE_ONLY with matching redirect: **1**
- LIVE_ONLY without redirect: **38**

_Live product slug is ExtNsT3AF; Mintlify uses T3AF. Critical: add /ExtNsT3AF/* → /ExtNsT3AF/* redirects if missing._

### Covered by redirects

- `/ExtNsT3AF/Index` ← `/AIUniverse` → `/ExtNsT3AF/Index`

### Without redirects

- `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index`
- `/ExtNsT3AF/Configuration/AIContext/Index`
- `/ExtNsT3AF/Configuration/AIFeatures/Index`
- `/ExtNsT3AF/Configuration/AIPermissions/Index`
- `/ExtNsT3AF/Configuration/AIPrompts/Index`
- `/ExtNsT3AF/Configuration/AIProviders/Index`
- `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index`
- `/ExtNsT3AF/Configuration/Dashboard/Index`
- `/ExtNsT3AF/Configuration/Index`
- `/ExtNsT3AF/DeveloperGuide/Architecture/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index`
- `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index`
- `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index`
- `/ExtNsT3AF/DeveloperGuide/Index`
- `/ExtNsT3AF/HelpfulLinks/Index`
- `/ExtNsT3AF/Installation/Index`
- `/ExtNsT3AF/Integrations/Index`
- `/ExtNsT3AF/Integrations/MCPServer/Index`
- `/ExtNsT3AF/Integrations/MCPTesting/Index`
- `/ExtNsT3AF/Integrations/MCPTools/Index`
- `/ExtNsT3AF/Introduction/Index`
- `/ExtNsT3AF/Support/Index`
- `/ExtNsT3AF/Troubleshooting/FAQ/Index`
- `/ExtNsT3AF/Troubleshooting/Index`
- `/ExtNsT3AF/Troubleshooting/KnownProblems/Index`
- `/ExtNsT3AF/UserGuide/Index`
- `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index`
- `/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index`
- `/ExtNsT3AL/T3ALTerms%28Glossary%29/Index`
- `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index`
- `/genindex`
- `/history`
- `/py-modindex`
- `/search`

## Suggested redirects

| Live | Suggested Mintlify | Reason | Exists |
| --- | --- | --- | --- |
| `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index` | `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites&SOWCustomLLM/Index` | url_decode_special_chars | True |
| `/ExtNsT3AF/Configuration/AIContext/Index` | `/ExtNsT3AF/Configuration/AIContext/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIFeatures/Index` | `/ExtNsT3AF/Configuration/AIFeatures/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIPermissions/Index` | `/ExtNsT3AF/Configuration/AIPermissions/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIPrompts/Index` | `/ExtNsT3AF/Configuration/AIPrompts/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIProviders/Index` | `/ExtNsT3AF/Configuration/AIProviders/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index` | `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/Dashboard/Index` | `/ExtNsT3AF/Configuration/Dashboard/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Configuration/Index` | `/ExtNsT3AF/Configuration/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/Architecture/Index` | `/ExtNsT3AF/DeveloperGuide/Architecture/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index` | `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index` | `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index` | `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index` | `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index` | `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index` | `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index` | `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/DeveloperGuide/Index` | `/ExtNsT3AF/DeveloperGuide/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/HelpfulLinks/Index` | `/ExtNsT3AF/HelpfulLinks/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Index` | `/ExtNsT3AF/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Installation/Index` | `/ExtNsT3AF/Installation/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/Index` | `/ExtNsT3AF/Integrations/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/MCPServer/Index` | `/ExtNsT3AF/Integrations/MCPServer/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/MCPTesting/Index` | `/ExtNsT3AF/Integrations/MCPTesting/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Integrations/MCPTools/Index` | `/ExtNsT3AF/Integrations/MCPTools/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Introduction/Index` | `/ExtNsT3AF/Introduction/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Support/Index` | `/ExtNsT3AF/Support/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Troubleshooting/FAQ/Index` | `/ExtNsT3AF/Troubleshooting/FAQ/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Troubleshooting/Index` | `/ExtNsT3AF/Troubleshooting/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/Troubleshooting/KnownProblems/Index` | `/ExtNsT3AF/Troubleshooting/KnownProblems/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/UserGuide/Index` | `/ExtNsT3AF/UserGuide/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index` | `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index` | ExtNsT3AF_to_T3AF | True |
| `/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index` | `/ExtNsT3AL/SeamlessXLIFFImport&Export/Index` | url_decode_special_chars | True |
| `/ExtNsT3AL/T3ALTerms%28Glossary%29/Index` | `/ExtNsT3AL/T3ALTerms(Glossary)/Index` | url_decode_special_chars | True |
| `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index` | `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites&SOWCustomLLM/Index` | url_decode_special_chars | True |
| `/genindex` | `None` | sphinx_utility_page | False |
| `/history` | `None` | sphinx_utility_page | False |
| `/py-modindex` | `None` | sphinx_utility_page | False |
| `/search` | `None` | sphinx_utility_page | False |

## MINT_ONLY (grouped)

Total: **73**

### intentional_hub_or_T3AF:AIFoundationExtensions (1)

- `/AIFoundationExtensions/Index`

### intentional_hub_or_T3AF:AllExtensions (1)

- `/AllExtensions/Index`

### intentional_hub_or_T3AF:AllTemplates (1)

- `/AllTemplates/Index`

### intentional_hub_or_T3AF:T3AF (64)

- `/ExtNsT3AF/AIContext/Index`
- `/ExtNsT3AF/AIFeatures/Index`
- `/ExtNsT3AF/AIPrompts/Index`
- `/ExtNsT3AF/AIProviders/Index`
- `/ExtNsT3AF/AIUsageAndLogs/Index`
- `/ExtNsT3AF/Appendix/Index`
- `/ExtNsT3AF/Architecture/Index`
- `/ExtNsT3AF/Configuration/AIContext/Index`
- `/ExtNsT3AF/Configuration/AIFeatures/Index`
- `/ExtNsT3AF/Configuration/AIPermissions/Index`
- `/ExtNsT3AF/Configuration/AIPrompts/Index`
- `/ExtNsT3AF/Configuration/AIProviders/Index`
- `/ExtNsT3AF/Configuration/AIUsageAndLogs/Index`
- `/ExtNsT3AF/Configuration/Dashboard/Index`
- `/ExtNsT3AF/Configuration/GovernanceAndAccess/Index`
- `/ExtNsT3AF/Configuration/Index`
- `/ExtNsT3AF/Dashboard/Index`
- `/ExtNsT3AF/DeveloperGuide/Architecture/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomAiAccess/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomAiFeatures/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomAiPrompts/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index`
- `/ExtNsT3AF/DeveloperGuide/CustomProviders/Index`
- `/ExtNsT3AF/DeveloperGuide/ExtensionIntegration/Index`
- `/ExtNsT3AF/DeveloperGuide/FeatureProviderOverrides/Index`
- `/ExtNsT3AF/DeveloperGuide/Index`
- `/ExtNsT3AF/DeveloperGuide/T3PlanetCredits/Index`
- `/ExtNsT3AF/FAQ/Index`
- `/ExtNsT3AF/GetThisExtension/Index`
- `/ExtNsT3AF/GovernanceAndAccess/Index`
- `/ExtNsT3AF/HelpfulLinks/Index`
- `/ExtNsT3AF/Index`
- `/ExtNsT3AF/Installation/Index`
- `/ExtNsT3AF/Integrations/Index`
- `/ExtNsT3AF/Integrations/MCPServer/Index`
- `/ExtNsT3AF/Integrations/MCPTesting/Index`
- `/ExtNsT3AF/Integrations/MCPTools/Index`
- `/ExtNsT3AF/Introduction/Index`
- `/ExtNsT3AF/KnownProblems/Index`
- `/ExtNsT3AF/MCPServer/Index`
- `/ExtNsT3AF/MCPTesting/Index`
- `/ExtNsT3AF/MCPTools/Index`
- `/ExtNsT3AF/Privacy/Index`
- `/ExtNsT3AF/ReleaseNotes/1.0.0/Index`
- `/ExtNsT3AF/ReleaseNotes/Index`
- `/ExtNsT3AF/Screenshots/Index`
- `/ExtNsT3AF/SetupWizard/Index`
- `/ExtNsT3AF/Support/Index`
- `/ExtNsT3AF/SystemRequirements/Index`
- `/ExtNsT3AF/T3PlanetCredits/Index`
- `/ExtNsT3AF/T3PlanetCreditsQA/Index`
- `/ExtNsT3AF/Troubleshooting/FAQ/Index`
- `/ExtNsT3AF/Troubleshooting/Index`
- `/ExtNsT3AF/Troubleshooting/KnownProblems/Index`
- `/ExtNsT3AF/UpdateVersion/Index`
- `/ExtNsT3AF/UpgradeGuide/Index`
- `/ExtNsT3AF/Usage/Index`
- `/ExtNsT3AF/UserGuide/Index`
- `/ExtNsT3AF/UserGuide/RolesAndDailyUse/Index`
- `/ExtNsT3AF/VideoTutorials/Index`
- `/ExtNsT3AF/WhatDoesItDo/Index`

### product:ExtNsT3AC (1)

- `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites&SOWCustomLLM/Index`

### product:ExtNsT3AI (1)

- `/ExtNsT3AI/Configuration/Index`

### product:ExtNsT3AL (2)

- `/ExtNsT3AL/SeamlessXLIFFImport&Export/Index`
- `/ExtNsT3AL/T3ALTerms(Glossary)/Index`

### product:ExtNsT3AS (1)

- `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites&SOWCustomLLM/Index`

### product:SLA-skills (1)

- `/SLA-skills`

## HTTP sample verification

- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/AIContext/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/AIFeatures/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/AIPermissions/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/AIPrompts/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/AIProviders/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/AIUsageAndLogs/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/Dashboard/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Configuration/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/DeveloperGuide/Architecture/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/DeveloperGuide/CustomAccessCatalogs/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/DeveloperGuide/CustomFeatureCards/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/DeveloperGuide/CustomMcpTools/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/DeveloperGuide/CustomPromptCatalogs/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/DeveloperGuide/CustomProviders/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AL/T3ALTerms%28Glossary%29/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index.html
- `200` — https://docs.t3planet.de/en/latest/ExtNsT3AF/Index.html
- `200` — https://docs.t3planet.de/en/latest/search.html


### Critical redirect assessment

- `/AIUniverse/:path*` → `/ExtNsT3AF/:path*` and `/AIFoundation/:path*` → `/ExtNsT3AF/:path*` exist.
- **`/ExtNsT3AF/:path*` is missing** — live RTD uses `ExtNsT3AF` (verified HTTP 200).
- Only `/ExtNsT3AF/Index` loosely matches via `/AIUniverse` → `/ExtNsT3AF/Index` if someone used the old name; deep ExtNsT3AF URLs are uncovered.
- Percent-encoded LIVE_ONLY (`%26`, `%28`/`%29`) map to Mintlify pages with literal `&`/`()` — encoding mismatch, not missing content.

## Notes

- Sitemap `/en/latest/sitemap.xml` → 404; used objects.inv + homepage HTML + TOC markdown.
- No `Live-docs/` mirror present; audit did not modify docs content.
- Prefer adding `/ExtNsT3AF/*` → `/ExtNsT3AF/*` redirects over renames.

## Fixes applied (Aug 7 2026)

Added **17** SEO/compat redirects in `docs.json` (skipped sources that already existed):

### ExtNsT3AF → T3AF

- `/ExtNsT3AF/Index` → `/ExtNsT3AF/Index`
- `/ExtNsT3AF` → `/ExtNsT3AF/Index`
- `/ExtNsT3AF/:path*` → `/ExtNsT3AF/:path*`
- `/ExtNsT3AF/Index.html` → `/ExtNsT3AF/Index`
- `/ExtNsT3AF.html` → `/ExtNsT3AF/Index`
- `/de/ExtNsT3AF/Index` → `/ExtNsT3AF/Index`
- `/de/ExtNsT3AF` → `/ExtNsT3AF/Index`
- `/de/ExtNsT3AF/:path*` → `/ExtNsT3AF/:path*`

### Percent-encoded special-character live paths

- `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index` → `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites&SOWCustomLLM/Index`
- `/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index` → `/ExtNsT3AL/SeamlessXLIFFImport&Export/Index`
- `/ExtNsT3AL/T3ALTerms%28Glossary%29/Index` → `/ExtNsT3AL/T3ALTerms(Glossary)/Index`
- `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index` → `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites&SOWCustomLLM/Index`

### Sphinx / RTD utility paths

- `/history.html` → `/`
- `/readme.html` → `/`
- `/genindex` → `/`
- `/search` → `/`
- `/py-modindex` → `/`

Also updated client-side `redirectLegacyPath` in `scripts/src/t3-docs.js` for `/ExtNsT3AF/*` and `/de/ExtNsT3AF/*` → `/ExtNsT3AF/*`, then rebuilt `t3-docs.min.js` via `python3 scripts/build_perf_assets.py`.

## Post-rename re-audit

_Re-run after Mintlify product folder rename **T3AF → ExtNsT3AF** (exact live slug match). Source: live `objects.inv` (746 pages) vs Mintlify Index.md / non-Index.md / `docs.json` pages._

| Metric | Count |
| --- | ---: |
| total_live_pages (objects.inv) | 746 |
| mintlify Index.md | 663 |
| mintlify non-Index.md pages | 115 |
| docs.json nav page entries | 674 |
| mintlify union (canonical) | 780 |
| LIVE_ONLY (exact) | 10 |
| LIVE_ONLY sphinx utils | 5 |
| LIVE_ONLY content | 5 |
| … encoding-only (OK w/ redirects) | 4 |
| … Index-suffix mismatch (OK; page exists as `/…/Index`) | 1 |
| … true missing | 0 |
| ExtNsT3AF LIVE_ONLY content | **0** |

### ExtNsT3AF

**LIVE_ONLY for ExtNsT3AF: 0** — exact path match with live RTD after rename.

### LIVE_ONLY content (exact list)

- `/ExtNsFriendlyCaptcha/FAQ` — Index-suffix mismatch; Mintlify has `/ExtNsFriendlyCaptcha/FAQ` (`Index.md` on disk)
- `/ExtNsT3AC/CustomLLMSupport/T3ACPrerequisites%26SOWCustomLLM/Index` — encoding-only; decoded folder on disk (OK with redirects)
- `/ExtNsT3AL/SeamlessXLIFFImport%26Export/Index` — encoding-only; decoded folder on disk (OK with redirects)
- `/ExtNsT3AL/T3ALTerms%28Glossary%29/Index` — encoding-only; decoded folder on disk (OK with redirects)
- `/ExtNsT3AS/CustomLLMSupport/T3ASPrerequisites%26SOWCustomLLM/Index` — encoding-only; decoded folder on disk (OK with redirects)

### Sphinx utils (excluded from content)

- `/genindex`
- `/history`
- `/py-modindex`
- `/readme`
- `/search`

### Notes

- `mint_cache_proxy.py` `WARM_PATHS` default updated: `/T3AF/Index` → `/ExtNsT3AF/Index`.
- `docs.json` navigation page entries with bare `T3AF/` path: **0** (redirects `/T3AF` → `/ExtNsT3AF` remain).
- Content `*.md` hrefs to `/T3AF/` outside `scripts/qa-final/`: **none**.

### Local mint probe (:3000 / :3001)

- Proxy on `:3000` and mint on `:3001` were listening.
- `GET /T3AF/Index` → **200** (`X-T3-Cache: HIT`, title still “T3AF”) — stale warm cache from pre-rename `WARM_PATHS`.
- `GET /ExtNsT3AF/Index` → **timeout** (origin `:3001` did not respond within 90s). Re-warm after proxy restart with updated `WARM_PATHS`.
