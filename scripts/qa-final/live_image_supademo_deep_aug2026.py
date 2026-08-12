#!/usr/bin/env python3
"""Deep offline parity: Sphinx HTML vs Mintlify — Supademo IDs + image basenames.

August 2026 deep scan: migrate missing embeds/images, sample live fetch, write reports.
"""
from __future__ import annotations

import json
import re
import shutil
import time
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

_BASE = Path("/Users/nitsan/www/AI Agents")
ROOT = next(
    (
        p
        for p in _BASE.iterdir()
        if (p / ".git").exists() and (p / "ExtNsT3AF").exists()
    ),
    next(p for p in _BASE.iterdir() if p.name == "Mintilify Doc"),
)
LIVE_BASE = "https://docs.t3planet.de/en/latest/"
LOCAL_HTML_CANDIDATES = [
    Path("/Users/nitsan/www/AI Agents/T3Planet Docs Agent/docs/docs/_build/html"),
    Path("/Users/nitsan/www/AI Agents/Docs/docs/docs/_build/html"),
    ROOT / "docs" / "_build" / "html",
]
LOCAL_HTML = next((c for c in LOCAL_HTML_CANDIDATES if c.is_dir()), None)
SPHINX_IMAGES = (LOCAL_HTML / "_images") if LOCAL_HTML else None

OUT_JSON = ROOT / "scripts/qa-final/LIVE_IMAGE_SUPADEMO_DEEP_AUG2026.json"
OUT_MD = ROOT / "scripts/qa-final/LIVE_CONTENT_PARITY_AUG2026.md"
UA = "Mozilla/5.0 (compatible; MintlifyParityBot/1.0; +https://docs.t3planet.de)"
TIMEOUT = 30
MAX_IMAGE_DOWNLOADS = 200
SLEEP_LIVE = 1.0

SKIP_HTML = {
    "genindex",
    "search",
    "py-modindex",
    "history",
    "readme",
    "404",
    "objects.inv",
}
SKIP_IMG_PARTS = ("_static", "logo", "icon", "favicon", "badge", "sprites")
SUPADEMO_RE = re.compile(r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", re.I)
MD_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']",
    re.I,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)

IFRAME_RE = re.compile(
    r'<iframe[^>]+src=["\'](https?://(?:app\.)?supademo\.com/[^"\']+)["\'][^>]*>',
    re.I,
)


def make_block(src: str, title: str) -> str:
    src = unescape(src.strip())
    src = src.replace("/demo/", "/embed/")
    src = re.sub(r"/edit(?=[?#]|$)", "", src)
    title = (title or "Interactive demo").replace('"', "'")
    return (
        f'\n<div className="t3-embed">'
        f'<iframe src="{src}" loading="lazy" title="{title}" '
        f'allow="clipboard-write" frameBorder="0" '
        f'webkitallowfullscreen="true" mozallowfullscreen="true" '
        f"allowfullscreen></iframe>"
        f"</div>\n"
    )


def clean_heading(text: str) -> str:
    text = re.sub(r"\s*¶\s*$", "", text)
    text = re.sub(r"\s*\s*$", "", text)
    return re.sub(r"\s+", " ", text).strip()


def resolve_mint_path(live_doc: str) -> Path | None:
    live_doc = unquote(live_doc)
    parts = live_doc.strip("/").split("/")
    if not parts:
        return None
    if parts[0] == "T3AF":
        parts = ["ExtNsT3AF"] + parts[1:]
    if parts[0] == "EXTKarma" and len(parts) >= 2:
        renames = {
            "ConfigureCaptcha": "CaptchaConfiguration",
            "CustomElements": "ContentBlockElements",
            "UpgradeGuide": "UpgradeGuideForContainer",
        }
        if parts[1] in renames:
            parts = [parts[0], renames[parts[1]]] + parts[2:]

    candidates: list[Path] = []
    base = ROOT.joinpath(*parts)
    if parts[-1] == "Index":
        candidates.append(
            ROOT.joinpath(*parts[:-1], "Index.md") if len(parts) > 1 else ROOT / "Index.md"
        )
        candidates.append(base.with_suffix(".md"))
    else:
        candidates.append(base.with_suffix(".md"))
        candidates.append(base / "Index.md")

    # index.html special
    if live_doc in ("index", "Index"):
        candidates = [ROOT / "index.md", ROOT / "Index.md"] + candidates

    for c in list(candidates):
        s = str(c)
        if "/T3AF/" in s or s.endswith("/T3AF.md"):
            candidates.append(
                Path(s.replace("/T3AF/", "/ExtNsT3AF/").replace("/T3AF.md", "/ExtNsT3AF.md"))
            )

    seen: set[Path] = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if c.is_file():
            return c
    return None


def list_sphinx_pages() -> list[tuple[str, Path]]:
    assert LOCAL_HTML
    pages: list[tuple[str, Path]] = []
    for html_path in sorted(LOCAL_HTML.rglob("*.html")):
        rel = html_path.relative_to(LOCAL_HTML).as_posix()
        if rel.startswith("_") or "/_" in rel:
            continue
        if rel.endswith(".html"):
            doc = rel[: -len(".html")]
        else:
            continue
        base = doc.split("/")[-1].lower()
        if base in SKIP_HTML:
            continue
        # skip pure redirect stubs? keep all product pages
        pages.append((doc, html_path))
    return pages


def basename_variants(name: str) -> set[str]:
    name = unquote(name.split("?")[0].split("#")[0])
    name = Path(name).name
    if not name:
        return set()
    out = {name.lower()}
    stem = Path(name).stem
    suf = Path(name).suffix.lower()
    for alt in (".webp", ".png", ".jpg", ".jpeg", ".gif", ".svg"):
        if alt != suf:
            out.add((stem + alt).lower())
    return out


def should_skip_img_src(src: str) -> bool:
    low = src.lower()
    if not src or src.startswith("data:"):
        return True
    for part in SKIP_IMG_PARTS:
        if part in low:
            return True
    return False


def extract_sphinx_images(html: str, page_url_hint: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one('[role="main"]') or soup.select_one(".document") or soup.body or soup
    out: list[dict] = []
    seen: set[str] = set()
    for img in main.select("img[src]"):
        src = unescape(img.get("src") or "").strip()
        if should_skip_img_src(src):
            continue
        base = Path(unquote(src.split("?")[0])).name
        if not base or base.lower() in seen:
            continue
        seen.add(base.lower())
        heading = ""
        for prev in img.find_all_previous(["h1", "h2", "h3", "h4"], limit=1):
            heading = clean_heading(prev.get_text(" ", strip=True))
            break
        alt = (img.get("alt") or "").strip()
        # Resolve possible live URL
        if src.startswith("http"):
            abs_url = src
        elif src.startswith("/"):
            abs_url = urljoin(LIVE_BASE, src.lstrip("/"))
        else:
            # relative to page or _images
            abs_url = urljoin(LIVE_BASE + page_url_hint + ".html", src)
        out.append(
            {
                "basename": base,
                "src": src,
                "abs_url": abs_url,
                "heading": heading,
                "alt": alt or base,
            }
        )
    return out


def extract_sphinx_supademos(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one('[role="main"]') or soup.select_one(".document") or soup.body or soup
    out: list[dict] = []
    seen: set[str] = set()
    for iframe in main.select('iframe[src*="supademo"]'):
        src = unescape(iframe.get("src") or "").strip()
        src = src.replace("/demo/", "/embed/")
        src = re.sub(r"/edit(?=[?#]|$)", "", src)
        m = SUPADEMO_RE.search(src)
        eid = m.group(1).lower() if m else None
        key = eid or src
        if key in seen:
            continue
        seen.add(key)
        heading = ""
        for prev in iframe.find_all_previous(["h1", "h2", "h3", "h4"], limit=1):
            heading = clean_heading(prev.get_text(" ", strip=True))
            break
        out.append(
            {
                "id": eid,
                "src": src,
                "title": iframe.get("title") or heading or "Interactive demo",
                "heading": heading,
            }
        )
    # also raw regex fallback
    for m in IFRAME_RE.finditer(html):
        src = unescape(m.group(1))
        src = src.replace("/demo/", "/embed/")
        eid_m = SUPADEMO_RE.search(src)
        eid = eid_m.group(1).lower() if eid_m else None
        key = eid or src
        if key in seen:
            continue
        seen.add(key)
        out.append({"id": eid, "src": src, "title": "Interactive demo", "heading": ""})
    return out


def mint_supademo_ids(text: str) -> set[str]:
    return {m.group(1).lower() for m in SUPADEMO_RE.finditer(text)}


def mint_image_basenames(text: str) -> set[str]:
    found: set[str] = set()
    for m in MD_IMG_RE.finditer(text):
        url = m.group(2) or m.group(3) or ""
        url = unescape(url.strip().split()[0] if url.strip() else "")
        base = Path(unquote(url.split("?")[0])).name
        if base:
            found.add(base.lower())
    return found


def disk_image_basenames(page_dir: Path) -> set[str]:
    imgs_dir = page_dir / "images"
    if not imgs_dir.is_dir():
        return set()
    return {p.name.lower() for p in imgs_dir.iterdir() if p.is_file()}


def insert_after_heading(md: str, heading: str, block: str) -> tuple[str, bool]:
    if not heading:
        return md, False
    escaped = re.escape(heading)
    pattern = re.compile(rf"(?m)^(#{1,6})\s+{escaped}\s*$")
    m = pattern.search(md)
    if not m:
        short = re.escape(heading[:40].rstrip())
        pattern = re.compile(rf"(?m)^(#{1,6})\s+{short}[^\n]*$")
        m = pattern.search(md)
    if not m:
        return md, False
    end = m.end()
    if end < len(md) and md[end] == "\n":
        end += 1
    eid_m = SUPADEMO_RE.search(block)
    if eid_m and eid_m.group(1).lower() in md[end : end + 800].lower():
        return md, True
    return md[:end] + block + md[end:], True


def append_interactive(md: str, blocks: list[str]) -> str:
    if "## Interactive demos" in md:
        return md.rstrip() + "\n" + "".join(blocks) + "\n"
    return md.rstrip() + "\n\n## Interactive demos\n\n" + "".join(blocks) + "\n"


def insert_image_md(md: str, heading: str, rel_path: str, alt: str) -> tuple[str, bool]:
    line = f"\n![{alt}]({rel_path})\n"
    # already linked?
    if Path(rel_path).name.lower() in mint_image_basenames(md):
        return md, False
    if heading:
        md2, ok = insert_after_heading(md, heading, line)
        if ok:
            return md2, True
    # append under a figures section
    if "## Figures" in md:
        return md.rstrip() + "\n" + line, True
    return md.rstrip() + "\n\n## Figures\n" + line, True


def find_sphinx_image_file(basename: str) -> Path | None:
    if not SPHINX_IMAGES or not SPHINX_IMAGES.is_dir():
        return None
    # exact
    p = SPHINX_IMAGES / basename
    if p.is_file():
        return p
    # case-insensitive + webp/png swap
    want = basename_variants(basename)
    for f in SPHINX_IMAGES.iterdir():
        if f.is_file() and f.name.lower() in want:
            return f
    return None


def download_image(url: str, dest: Path) -> bool:
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=TIMEOUT) as r:
            data = r.read()
        if len(data) < 50:
            return False
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def sync_page(
    doc: str,
    html_path: Path,
    *,
    dry_images: bool,
    download_budget: list[int],
) -> dict:
    mint = resolve_mint_path(doc)
    if not mint:
        return {"doc": doc, "status": "no_mint", "missing_supademo": [], "missing_images": []}

    html = html_path.read_text(encoding="utf-8", errors="replace")
    embeds = extract_sphinx_supademos(html)
    images = extract_sphinx_images(html, doc)

    md = mint.read_text(encoding="utf-8")
    have_ids = mint_supademo_ids(md)
    text_bases = mint_image_basenames(md)
    disk_bases = disk_image_basenames(mint.parent)
    present_bases = set()
    for b in text_bases | disk_bases:
        present_bases |= basename_variants(b)

    missing_sd = [e for e in embeds if e.get("id") and e["id"] not in have_ids]
    missing_img = []
    for im in images:
        variants = basename_variants(im["basename"])
        if variants & present_bases:
            continue
        # also check if any variant on disk with different casing
        missing_img.append(im)

    result = {
        "doc": doc,
        "mint": str(mint.relative_to(ROOT)),
        "status": "ok",
        "missing_supademo_before": [e["id"] for e in missing_sd],
        "missing_images_before": [im["basename"] for im in missing_img],
        "missing_supademo_after": [],
        "missing_images_after": [],
        "modified": False,
        "actions": [],
    }

    md2 = md
    # Supademo sync
    appended: list[str] = []
    for emb in missing_sd:
        block = make_block(emb["src"], emb["title"])
        md2, ok = insert_after_heading(md2, emb["heading"], block)
        if not ok:
            appended.append(block)
        result["actions"].append(f"supademo:{emb['id']}")
        have_ids.add(emb["id"])
    if appended:
        md2 = append_interactive(md2, appended)

    # Images
    page_images = mint.parent / "images"
    for im in missing_img:
        if dry_images:
            continue
        src_file = find_sphinx_image_file(im["basename"])
        dest_name = im["basename"]
        if src_file:
            dest_name = src_file.name  # keep actual extension from sphinx
        dest = page_images / dest_name
        got = False
        if src_file and src_file.is_file():
            page_images.mkdir(parents=True, exist_ok=True)
            if not dest.exists():
                shutil.copy2(src_file, dest)
            got = True
            result["actions"].append(f"img_copy:{dest_name}")
        elif download_budget[0] < MAX_IMAGE_DOWNLOADS:
            # try live URL variants
            urls = [im["abs_url"]]
            # common _images path
            urls.append(urljoin(LIVE_BASE, f"_images/{im['basename']}"))
            stem = Path(im["basename"]).stem
            for alt in (".webp", ".png", ".jpg"):
                urls.append(urljoin(LIVE_BASE, f"_images/{stem}{alt}"))
            for u in urls:
                if download_budget[0] >= MAX_IMAGE_DOWNLOADS:
                    break
                # dest may need alt extension
                cand_name = Path(urlparse(u).path).name or dest_name
                cand = page_images / cand_name
                if download_image(u, cand):
                    dest_name = cand_name
                    dest = cand
                    got = True
                    download_budget[0] += 1
                    result["actions"].append(f"img_dl:{dest_name}")
                    time.sleep(0.05)
                    break
        if got:
            rel = f"./images/{dest_name}"
            md2, linked = insert_image_md(md2, im["heading"], rel, im["alt"])
            if linked:
                result["actions"].append(f"img_md:{dest_name}")
            present_bases |= basename_variants(dest_name)
        else:
            result["missing_images_after"].append(im["basename"])

    # recompute remaining missing after
    have_ids2 = mint_supademo_ids(md2)
    result["missing_supademo_after"] = [
        e["id"] for e in embeds if e.get("id") and e["id"] not in have_ids2
    ]
    text2 = mint_image_basenames(md2)
    disk2 = disk_image_basenames(mint.parent)
    present2: set[str] = set()
    for b in text2 | disk2:
        present2 |= basename_variants(b)
    still_img = []
    for im in images:
        if not (basename_variants(im["basename"]) & present2):
            still_img.append(im["basename"])
    result["missing_images_after"] = still_img

    if md2 != md:
        mint.write_text(md2, encoding="utf-8")
        result["modified"] = True
        result["status"] = "updated"
    elif result["actions"]:
        result["status"] = "assets_only"
        result["modified"] = True
    return result


LIVE_SAMPLE = [
    "ExtNsT3AF/Index",
    "ExtNsT3AI/Index",
    "ExtNsT3AA/Index",
    "ExtNsT3AC/Index",
    "ExtNsT3AS/Index",
    "License/GenerateLicenseKey/Index",
    "EXTKarma/Installation/Index",
    "EXTBootstrap/Installation/Index",
    "ExtNsGallery/Introduction/Index",
    "ExtNsComments/Index",
    "AllExtensions/Index",
    "AIFoundationExtensions/Index",
    "ExtNsT3AF/Installation/Index",
    "ExtNsT3AI/Installation/Index",
    "index",
]


def live_sample_compare() -> dict:
    status = {
        "attempted": 0,
        "http_200": 0,
        "http_429": 0,
        "http_other": {},
        "blocked": False,
        "pages": [],
    }
    for doc in LIVE_SAMPLE:
        status["attempted"] += 1
        url = LIVE_BASE + doc + ".html"
        page_info = {"doc": doc, "url": url, "http": None, "sphinx_ids": [], "live_ids": [], "mint_ids": [], "match": None}
        mint = resolve_mint_path(doc)
        if mint and mint.is_file():
            page_info["mint_ids"] = sorted(mint_supademo_ids(mint.read_text(encoding="utf-8", errors="replace")))
        # local sphinx
        if LOCAL_HTML:
            lp = LOCAL_HTML / f"{doc}.html"
            if lp.is_file():
                page_info["sphinx_ids"] = sorted(
                    e["id"] for e in extract_sphinx_supademos(lp.read_text(encoding="utf-8", errors="replace")) if e.get("id")
                )
        try:
            req = Request(url, headers={"User-Agent": UA})
            with urlopen(req, timeout=TIMEOUT) as r:
                code = r.status
                body = r.read().decode("utf-8", errors="replace")
                page_info["http"] = code
                if code == 200:
                    status["http_200"] += 1
                    live_ids = sorted({m.group(1).lower() for m in SUPADEMO_RE.finditer(body)})
                    page_info["live_ids"] = live_ids
                    mint_set = set(page_info["mint_ids"])
                    page_info["match"] = set(live_ids).issubset(mint_set) if live_ids else True
                    page_info["live_only"] = sorted(set(live_ids) - mint_set)
        except HTTPError as e:
            page_info["http"] = e.code
            if e.code == 429:
                status["http_429"] += 1
                status["blocked"] = True
            else:
                status["http_other"][str(e.code)] = status["http_other"].get(str(e.code), 0) + 1
        except Exception as e:
            page_info["http"] = f"error:{type(e).__name__}"
            status["http_other"][str(page_info["http"])] = status["http_other"].get(str(page_info["http"]), 0) + 1
        status["pages"].append(page_info)
        time.sleep(SLEEP_LIVE)
        if status["blocked"] and status["http_429"] >= 2:
            # stop early if clearly blocked
            break
    return status


def update_parity_md(summary: dict) -> None:
    section = f"""

## Image / Supademo deep scan (August 2026)

**Generated:** {summary["generated"]}
**Sphinx HTML:** `{summary["sphinx_html"]}`
**Repo:** `{summary["repo"]}`

### Counts

| Metric | Value |
|--------|-------|
| pages_scanned | {summary["pages_scanned"]} |
| missing_supademo_before | {summary["missing_supademo_before"]} |
| missing_supademo_after | {summary["missing_supademo_after"]} |
| missing_images_before | {summary["missing_images_before"]} |
| missing_images_after | {summary["missing_images_after"]} |
| files_modified | {summary["files_modified"]} |
| image_copies | {summary["image_copies"]} |
| image_downloads | {summary["image_downloads"]} |
| download_cap | {MAX_IMAGE_DOWNLOADS} |

### Live sample (15 pages, 1s sleep)

- Status: **{summary["live_sample_status"]}**
- HTTP 200: {summary["live_sample"].get("http_200", 0)}
- HTTP 429: {summary["live_sample"].get("http_429", 0)}
- Blocked: {summary["live_sample"].get("blocked", False)}
- Attempted: {summary["live_sample"].get("attempted", 0)}

### Notes

- Image matching: Sphinx `img` basenames vs Mintlify `![]()` / `<img src>` and on-disk `{{page}}/images/`; `.webp`/`.png` swaps accepted.
- Prefer copy from Sphinx `_images/`; network download only when missing locally (capped at {MAX_IMAGE_DOWNLOADS}).
- Supademo inserts use `t3-embed` iframe blocks (same format as `scripts/sync_supademo_from_live.py`).
- No content deleted.

### Sample remaining gaps (after)

"""
    rem_sd = summary.get("remaining_supademo_examples") or []
    rem_img = summary.get("remaining_image_examples") or []
    if rem_sd:
        section += "\n**Supademo still missing:**\n\n"
        for row in rem_sd[:15]:
            section += f"- `{row['doc']}`: {', '.join(row['ids'][:5])}\n"
    else:
        section += "\nNo remaining missing Supademo IDs after sync.\n"
    if rem_img:
        section += "\n**Images still missing:**\n\n"
        for row in rem_img[:15]:
            section += f"- `{row['doc']}`: {', '.join(row['names'][:5])}\n"
    else:
        section += "\nNo remaining missing images (or only unresolved after download cap).\n"

    text = OUT_MD.read_text(encoding="utf-8") if OUT_MD.is_file() else "# Live Content Parity — August 2026\n"
    marker = "## Image / Supademo deep scan (August 2026)"
    if marker in text:
        # replace existing section through EOF or next ## at same level after our block — append replace from marker
        pre = text.split(marker)[0].rstrip()
        text = pre + "\n" + section
    else:
        text = text.rstrip() + "\n" + section
    OUT_MD.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    if not LOCAL_HTML:
        raise SystemExit("No local Sphinx HTML found")
    print("ROOT", ROOT)
    print("SPHINX", LOCAL_HTML)
    pages = list_sphinx_pages()
    print(f"Sphinx product pages: {len(pages)}")

    download_budget = [0]
    results = []
    missing_sd_before = 0
    missing_sd_after = 0
    missing_img_before = 0
    missing_img_after = 0
    files_modified = 0
    image_copies = 0
    image_downloads = 0
    remaining_sd_ex = []
    remaining_img_ex = []

    for i, (doc, html_path) in enumerate(pages):
        if i % 100 == 0:
            print(f"  scan {i}/{len(pages)} {doc}")
        r = sync_page(doc, html_path, dry_images=False, download_budget=download_budget)
        results.append(r)
        missing_sd_before += len(r.get("missing_supademo_before") or [])
        missing_sd_after += len(r.get("missing_supademo_after") or [])
        missing_img_before += len(r.get("missing_images_before") or [])
        missing_img_after += len(r.get("missing_images_after") or [])
        if r.get("modified"):
            files_modified += 1
        for a in r.get("actions") or []:
            if a.startswith("img_copy:"):
                image_copies += 1
            elif a.startswith("img_dl:"):
                image_downloads += 1
        if r.get("missing_supademo_after"):
            remaining_sd_ex.append({"doc": doc, "ids": r["missing_supademo_after"]})
        if r.get("missing_images_after"):
            remaining_img_ex.append({"doc": doc, "names": r["missing_images_after"]})

    print("Live sample fetch...")
    live = live_sample_compare()
    if live.get("blocked"):
        live_status = "blocked_429"
    elif live.get("http_200", 0) > 0:
        live_status = "ok_200"
    else:
        live_status = "failed_or_empty"

    summary = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "sphinx_html": str(LOCAL_HTML),
        "pages_scanned": len(pages),
        "missing_supademo_before": missing_sd_before,
        "missing_supademo_after": missing_sd_after,
        "missing_images_before": missing_img_before,
        "missing_images_after": missing_img_after,
        "files_modified": files_modified,
        "image_copies": image_copies,
        "image_downloads": image_downloads,
        "live_sample_status": live_status,
        "live_sample": live,
        "remaining_supademo_examples": remaining_sd_ex[:30],
        "remaining_image_examples": remaining_img_ex[:30],
        "pages_updated": [
            {
                "doc": r["doc"],
                "mint": r.get("mint"),
                "actions": r.get("actions"),
                "missing_supademo_before": r.get("missing_supademo_before"),
                "missing_images_before": r.get("missing_images_before"),
                "missing_supademo_after": r.get("missing_supademo_after"),
                "missing_images_after": r.get("missing_images_after"),
            }
            for r in results
            if r.get("modified") or r.get("missing_supademo_before") or r.get("missing_images_before")
        ],
    }

    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    update_parity_md(summary)
    print(json.dumps({k: summary[k] for k in [
        "pages_scanned",
        "missing_supademo_before",
        "missing_supademo_after",
        "missing_images_before",
        "missing_images_after",
        "files_modified",
        "image_copies",
        "image_downloads",
        "live_sample_status",
    ]}, indent=2))
    print("Wrote", OUT_JSON)
    print("Updated", OUT_MD)


if __name__ == "__main__":
    main()
