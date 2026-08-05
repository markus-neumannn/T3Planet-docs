# Why Link Grabber Shows 102 URLs vs 700+ on Live RTD

**Generated:** July 1, 2026

## Short answer

| What you measured | Count | What it actually is |
|-------------------|-------|---------------------|
| Link Grabber on Mintlify **homepage** | ~102 | Links **visible in that one page's HTML** (nav, cards, footer, anchors) |
| Mintlify **documentation pages** (full site) | **729** | Every page in `docs.json` navigation |
| RTD live site **unique pages** | **703** | Canonical English pages in `rtd_equivalent_urls.txt` |
| RTD URL list with **anchors & duplicates** | **764+** | Same pages + `#section` links + repeated `#` + external links |

**There is no missing migration of 600+ pages.** The homepage simply does not link to every doc page. Deep pages (e.g. `/ExtNsGallery/ZoomView/Index`) are reached via the **sidebar** after you open a product — they are not in the homepage DOM.

---

## Proof: deep pages work

These pages are **not** in your 102-link homepage list but return **HTTP 200**:

- http://192.168.0.137:3000/ExtNsT3AI/SEO/Index
- http://192.168.0.137:3000/ExtNsGallery/ZoomView/Index
- http://192.168.0.137:3000/ExtNsZoho/BuyNow
- http://192.168.0.137:3000/EXTKarma/CaptchaConfiguration/Index

---

## Full URL list (all Mintlify pages)

Complete manifest: **`scripts/all_mintlify_urls.txt`** (729 URLs)

One route per line, e.g.:

```
http://192.168.0.137:3000/ExtNsT3AI/SEO/Index
http://192.168.0.137:3000/License/LicenseActivation/Index
...
```

Route-only list: **`scripts/all_mintlify_routes.txt`**

---

## RTD ↔ Mintlify mapping

| Status | Count | Meaning |
|--------|-------|---------|
| Exact structural match | **700** | `/en/latest/Product/Section/Index.html` → `/Product/Section/Index` |
| Mintlify-only hubs | **3** | `AIFoundation`, `AllTemplates`, `AllExtensions` (new hub pages) |
| RTD-only (intentional) | **5** | 3 zip artifacts, `history`, `readme` — not doc pages |

Details: `url-mismatches-only.md`

---

## Why `/llms.txt` shows HTML (not 700 URLs)

On **local** `mint dev`, `/llms.txt` and `/sitemap.xml` return **404** or an error page. These endpoints are generated on **production Mintlify hosting** only.

Do **not** use Link Grabber on `llms.txt` locally to count pages. Use `scripts/all_mintlify_urls.txt` instead.

---

## How to verify yourself

### Option A — Open sidebar

1. Go to http://192.168.0.137:3000/ExtNsT3AI/Index
2. Expand sidebar → Translation, SEO, Content, etc.
3. Every item is a real route (700+ across all products)

### Option B — Direct URL test

Pick any RTD URL and convert:

```
https://docs.t3planet.de/en/latest/ExtNsFAQ/FAQPlugin/Index.html
→ http://192.168.0.137:3000/ExtNsFAQ/FAQPlugin/Index
```

### Option C — Count manifest

```bash
wc -l scripts/all_mintlify_urls.txt
# → 729
```

---

## RTD 764 vs Mintlify 729 — what's the difference?

The **764** figure from RTD includes:

1. **~703 unique RTD pages** (canonical, in `rtd_equivalent_urls.txt`)
2. **~60 anchor URLs** like `.../SEO/Index.html#how-to-use-mass-seo` (same page, different fragment)
3. **Duplicates** (`#`, homepage listed multiple times)
4. **External links** (`t3planet.de`, social media)
5. **Mintlify adds 3 hub pages** not on RTD
6. **RTD has 5 non-doc paths** (zip files, history, readme) excluded from Mintlify

**Net result:** Mintlify matches or exceeds RTD documentation coverage.
