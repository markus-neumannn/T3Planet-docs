#!/usr/bin/env python3
"""Deep Live RTD vs Mintlify reconciliation audit — August 12, 2026.

Section-level, code, link, image, and Supademo comparison for every live page.
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
import time
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, Tag

_BASE = Path("/Users/nitsan/www/AI Agents")
ROOT = Path(__file__).resolve().parents[2]
LIVE_BASE = "https://docs.t3planet.de/en/latest/"
LOCAL_HTML = Path("/Users/nitsan/www/AI Agents/T3Planet Docs Agent/docs/docs/_build/html")
INV_PATH = ROOT / "scripts/qa-final/objects.inv"
OUT_JSON = ROOT / "scripts/qa-final/LIVE_CONTENT_RECONCILE_AUG12.json"
OUT_MD = ROOT / "scripts/qa-final/LIVE_CONTENT_RECONCILE_AUG12.md"
UA = "Mozilla/5.0 (compatible; MintlifyReconcileBot/1.0; +https://docs.t3planet.de)"
SLEEP = 0.08
WORKERS = 8
TIMEOUT = 30
SKIP_NAMES = {"genindex", "search", "py-modindex", "history", "readme"}


def resolve_mint_path(live_doc: str) -> Path | None:
    """Map live Sphinx doc path to a Mintlify .md file."""
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
        candidates.append(ROOT.joinpath(*parts[:-1], "Index.md") if len(parts) > 1 else ROOT / "Index.md")
        candidates.append(base.with_suffix(".md"))
    else:
        candidates.append(base.with_suffix(".md"))
        candidates.append(base / "Index.md")

    for c in list(candidates):
        s = str(c)
        if "/T3AF/" in s or s.endswith("/T3AF.md"):
            candidates.append(Path(s.replace("/T3AF/", "/ExtNsT3AF/").replace("/T3AF.md", "/ExtNsT3AF.md")))

    seen: set[Path] = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if c.is_file():
            return c
    return None

# Load remigrate helpers
_rem_path = ROOT / "scripts/qa-final/remigrate_t3ac_t3as_t3af_aug10.py"
_spec2 = importlib.util.spec_from_file_location("remigrate", _rem_path)
_rem = importlib.util.module_from_spec(_spec2)
sys.modules["remigrate"] = _rem
_spec2.loader.exec_module(_rem)

clean_heading = _rem.clean_heading
norm_heading = _rem.norm_heading
content_root = _rem.content_root
strip_junk = _rem.strip_junk
extract_live = _rem.extract_live
extract_mint = _rem.extract_mint
missing_images = _rem.missing_images
missing_sections = _rem.missing_sections
mint_path_for = _rem.mint_path_for

SUPADEMO_RE = _rem.SUPADEMO_RE
FRONTMATTER_RE = _rem.FRONTMATTER_RE
HEADING_RE = _rem.HEADING_RE
SKIP_IMG_PARTS = _rem.SKIP_IMG_PARTS

CODE_BLOCK_RE = re.compile(r"```[\w-]*\n(.*?)```", re.S)
LINK_MD_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HUB_CARDGROUP_RE = re.compile(r"<CardGroup", re.I)

HUB_EXEMPT = {
    "index",
    "License/Index",
    "AllExtensions/Index",
    "AllTemplates/Index",
    "AIFoundationExtensions/Index",
}


def load_live_pages() -> list[str]:
    pages: list[str] = []
    inv_bytes = INV_PATH.read_bytes() if INV_PATH.is_file() else None
    if inv_bytes:
        try:
            rest = inv_bytes.split(b"\n", 4)[-1]
            data = zlib.decompress(rest).decode("utf-8", errors="replace")
            for line in data.splitlines():
                if not line.strip() or line.startswith("#"):
                    continue
                bits = line.split(" ", 4)
                if len(bits) < 5:
                    continue
                name, domain_role, _prio, uri = bits[0], bits[1], bits[2], bits[3]
                if domain_role != "std:doc":
                    continue
                doc = uri.replace(".html", "").rstrip("/")
                if doc.startswith("-") or doc == "-":
                    doc = name
                doc = unquote(doc.split("#", 1)[0])
                base = doc.split("/")[-1].lower()
                if base in SKIP_NAMES:
                    continue
                if doc and doc not in pages:
                    pages.append(doc)
        except Exception as exc:
            print("objects.inv parse failed:", exc)
    if not pages and LOCAL_HTML.is_dir():
        for html_path in LOCAL_HTML.rglob("*.html"):
            rel = html_path.relative_to(LOCAL_HTML).as_posix()
            if rel.startswith("_"):
                continue
            doc = unquote(rel[:-5])
            base = doc.split("/")[-1].lower()
            if base in SKIP_NAMES:
                continue
            if doc and doc not in pages:
                pages.append(doc)
    pages.sort()
    return pages


def fetch(url: str, retries: int = 3) -> tuple[int, str]:
    for attempt in range(retries):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=TIMEOUT) as r:
                return r.status, r.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code in (429, 503, 502):
                time.sleep(2.0 * (attempt + 1))
                continue
            return e.code, ""
        except (URLError, TimeoutError, OSError):
            time.sleep(1.0 * (attempt + 1))
    return 0, ""


def load_local_html(doc: str) -> str | None:
    for d in [doc, unquote(doc)]:
        path = LOCAL_HTML / f"{d}.html"
        if path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
    return None


def extract_code_live(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    root = content_root(soup)
    strip_junk(root)
    codes: list[str] = []
    for pre in root.find_all("pre"):
        t = pre.get_text().strip()
        if t and len(t) > 3:
            codes.append(t)
    return codes


def extract_code_mint(body: str) -> list[str]:
    return [m.group(1).strip() for m in CODE_BLOCK_RE.finditer(body) if m.group(1).strip()]


def normalize_code(c: str) -> str:
    return re.sub(r"\s+", " ", c).strip()


def code_diff(live_codes: list[str], mint_codes: list[str]) -> dict[str, Any]:
    live_norm = [normalize_code(c) for c in live_codes]
    mint_norm = [normalize_code(c) for c in mint_codes]
    live_set = set(live_norm)
    mint_set = set(mint_norm)
    missing = [c[:120] for c in live_norm if c not in mint_set]
    extra = [c[:120] for c in mint_norm if c not in live_set]
    return {
        "live_count": len(live_codes),
        "mint_count": len(mint_codes),
        "missing_in_mint": missing[:20],
        "extra_in_mint": extra[:10],
        "has_diff": bool(missing),
    }


def extract_links_live(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    root = content_root(soup)
    links: list[str] = []
    for a in root.find_all("a", href=True):
        href = a.get("href") or ""
        if href.startswith(("#", "mailto:", "javascript:", "data:")):
            continue
        if any(p in href for p in SKIP_IMG_PARTS):
            continue
        links.append(href)
    return sorted(set(links))


def extract_links_mint(body: str) -> list[str]:
    links = []
    for m in LINK_MD_RE.finditer(body):
        href = m.group(2).strip()
        if href.startswith(("#", "mailto:", "javascript:")):
            continue
        links.append(href)
    return sorted(set(links))


def normalize_link(href: str) -> str:
    href = unquote(href.split("#", 1)[0].strip())
    if href.endswith(".html"):
        href = href[:-5]
    if href.startswith("http") and "docs.t3planet.de" in href:
        if "/latest/" in href:
            href = href.split("/latest/", 1)[1]
    return href.lstrip("/")


def link_diff(live_links: list[str], mint_links: list[str], doc: str) -> dict[str, Any]:
    product = doc.split("/")[0] if doc else ""

    def norm_ctx(href: str) -> str:
        h = normalize_link(href)
        if not h:
            return h
        if h.startswith("http"):
            return h
        if product and not h.startswith(product):
            if h.startswith("/"):
                h = h.lstrip("/")
            return f"{product}/{h}"
        return h

    live_norm = {norm_ctx(l) for l in live_links}
    mint_norm = {norm_ctx(l) for l in mint_links}
    # Mintlify internal paths often use leading /
    mint_norm |= {f"/{p}" for p in mint_norm}
    mint_norm |= {p.lstrip("/") for p in mint_norm}
    missing = sorted(live_norm - mint_norm)
    return {"missing_in_mint": missing[:30], "has_diff": bool(missing)}


def is_hub_page(doc: str, mint_path: Path | None) -> bool:
    if doc in HUB_EXEMPT:
        return True
    if doc.endswith("/Index") and doc.count("/") == 1:
        return True
    if mint_path and mint_path.is_file():
        raw = mint_path.read_text(encoding="utf-8", errors="replace")
        body = FRONTMATTER_RE.sub("", raw, count=1)
        if HUB_CARDGROUP_RE.search(body) and len(body.strip()) < 3500:
            return True
    return False


def classify_status(
    doc: str,
    mint_path: Path | None,
    live_ex: dict,
    mint_ex: dict | None,
    code_d: dict,
    link_d: dict,
    miss_sec: list[str],
    miss_img: list[str],
    miss_sup: list[str],
    thin: bool,
) -> list[str]:
    tags: list[str] = []
    if mint_path is None:
        return ["NEW_PAGE"]
    if is_hub_page(doc, mint_path):
        if miss_sec or miss_sup or miss_img:
            if miss_sec:
                tags.append("MISSING_CONTENT")
            if miss_sup:
                tags.append("MEDIA_DIFFERENCE")
            if miss_img:
                tags.append("MEDIA_DIFFERENCE")
        else:
            tags.append("STRUCTURAL_DIFFERENCE")
        return tags if tags else ["MATCH"]
    if miss_sec or thin:
        tags.append("MISSING_CONTENT")
    if code_d.get("has_diff"):
        tags.append("UPDATED")
    if miss_img or miss_sup:
        tags.append("MEDIA_DIFFERENCE")
    if link_d.get("has_diff"):
        tags.append("LINK_DIFFERENCE")
    if not tags:
        tags.append("MATCH")
    return tags


def process_page(doc: str, local_only: bool) -> dict[str, Any]:
    if not local_only:
        time.sleep(SLEEP)
    url = LIVE_BASE + doc + ".html"
    html: str | None = None
    source = "none"
    status = 0
    if local_only:
        html = load_local_html(doc)
        if html:
            source = "local_sphinx"
            status = 200
    else:
        status, html = fetch(url)
        source = "live"
        if status != 200 or not html:
            html = load_local_html(doc)
            if html:
                source = "local_sphinx"
                status = 200

    mint_path = resolve_mint_path(doc)
    row: dict[str, Any] = {
        "live": doc,
        "live_url": url,
        "http_status": status,
        "html_source": source,
        "mint": str(mint_path.relative_to(ROOT)) if mint_path else None,
    }

    if status != 200 or not html:
        row["status"] = ["fetch_failed"]
        if not mint_path:
            row["status"].append("NEW_PAGE")
        return row

    live_ex = extract_live(html)
    mint_ex = extract_mint(mint_path) if mint_path else None
    body = ""
    if mint_path and mint_path.is_file():
        body = FRONTMATTER_RE.sub("", mint_path.read_text(encoding="utf-8", errors="replace"), count=1)

    miss_sec = missing_sections(live_ex["headings"], mint_ex["headings"] if mint_ex else [])
    miss_img = missing_images(live_ex["images"], mint_ex or {"images": [], "disk_images": []})
    miss_sup = [i for i in live_ex["supademo_ids"] if i not in (mint_ex or {}).get("supademo_ids", [])]
    ratio = (mint_ex["text_len"] / live_ex["text_len"]) if mint_ex and live_ex["text_len"] else 0.0
    thin = ratio < 0.45 and live_ex["text_len"] > 600 and not is_hub_page(doc, mint_path)

    code_d = code_diff(extract_code_live(html), extract_code_mint(body))
    link_d = link_diff(extract_links_live(html), extract_links_mint(body), doc)

    row["live_extract"] = {
        "text_len": live_ex["text_len"],
        "heading_count": len(live_ex["headings"]),
        "headings": [h["text"] for h in live_ex["headings"]],
        "image_count": len(live_ex["images"]),
        "supademo_ids": live_ex["supademo_ids"],
    }
    row["mint_extract"] = {
        "text_len": (mint_ex or {}).get("text_len"),
        "heading_count": len((mint_ex or {}).get("headings", [])),
        "path": (mint_ex or {}).get("path"),
    }
    row["missing_sections"] = miss_sec
    row["missing_images"] = miss_img
    row["missing_supademo"] = miss_sup
    row["text_ratio"] = round(ratio, 3)
    row["thin"] = thin
    row["code_diff"] = code_d
    row["link_diff"] = link_d
    row["status"] = classify_status(doc, mint_path, live_ex, mint_ex, code_d, link_d, miss_sec, miss_img, miss_sup, thin)
    return row


def write_md(report: dict) -> None:
    c = report["counts"]
    lines = [
        "# Live Content Reconcile — August 12, 2026",
        "",
        f"**Generated:** {report['generated']}",
        f"**Repo:** `{report['repo']}`",
        f"**Live base:** {LIVE_BASE}",
        f"**Sphinx fallback:** `{report.get('sphinx_html')}`",
        "",
        "## Summary",
        "",
        f"- Live pages audited: **{c['live_pages']}**",
        f"- Mintlify pages in repo: **{c['mint_pages']}**",
        f"- MATCH: **{c['MATCH']}**",
        f"- UPDATED: **{c['UPDATED']}**",
        f"- MISSING_CONTENT: **{c['MISSING_CONTENT']}**",
        f"- NEW_PAGE: **{c['NEW_PAGE']}**",
        f"- STRUCTURAL_DIFFERENCE: **{c['STRUCTURAL_DIFFERENCE']}**",
        f"- LINK_DIFFERENCE: **{c['LINK_DIFFERENCE']}**",
        f"- MEDIA_DIFFERENCE: **{c['MEDIA_DIFFERENCE']}**",
        f"- REQUIRES_REVIEW: **{c['REQUIRES_REVIEW']}**",
        f"- fetch_failed: **{c['fetch_failed']}**",
        "",
        "## NEW_PAGE",
        "",
    ]
    for r in report["pages"]:
        if "NEW_PAGE" in r.get("status", []):
            lines.append(f"- `{r['live']}`")
    lines += ["", "## MISSING_CONTENT (sample)", ""]
    mc = [r for r in report["pages"] if "MISSING_CONTENT" in r.get("status", [])]
    for r in mc[:50]:
        secs = ", ".join(r.get("missing_sections") or [])[:120]
        lines.append(f"- `{r['live']}` → `{r.get('mint')}` sections: {secs}")
    if len(mc) > 50:
        lines.append(f"- … and {len(mc) - 50} more")
    lines += ["", "## MEDIA_DIFFERENCE (sample)", ""]
    md = [r for r in report["pages"] if "MEDIA_DIFFERENCE" in r.get("status", [])]
    for r in md[:40]:
        lines.append(
            f"- `{r['live']}` imgs={len(r.get('missing_images') or [])} "
            f"supademo={len(r.get('missing_supademo') or [])}"
        )
    lines += ["", "## LINK_DIFFERENCE (sample)", ""]
    ld = [r for r in report["pages"] if "LINK_DIFFERENCE" in r.get("status", [])]
    for r in ld[:30]:
        miss = (r.get("link_diff") or {}).get("missing_in_mint") or []
        lines.append(f"- `{r['live']}` missing links: {len(miss)}")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    local_only = os.environ.get("PARITY_LOCAL_ONLY", "").strip() in {"1", "true", "yes"}
    if local_only:
        global SLEEP, WORKERS
        SLEEP = 0
        WORKERS = 16
        print("PARITY_LOCAL_ONLY=1 — using rebuilt Sphinx HTML")

    pages = load_live_pages()
    mint_count = len(list(ROOT.rglob("*.md")))
    print(f"Live pages: {len(pages)}, Mintlify md files: {mint_count}")

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process_page, doc, local_only): doc for doc in pages}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 100 == 0 or done == len(pages):
                print(f"  processed {done}/{len(pages)}")

    results.sort(key=lambda r: r["live"])
    status_counts: dict[str, int] = {
        "MATCH": 0,
        "UPDATED": 0,
        "MISSING_CONTENT": 0,
        "NEW_PAGE": 0,
        "STRUCTURAL_DIFFERENCE": 0,
        "LINK_DIFFERENCE": 0,
        "MEDIA_DIFFERENCE": 0,
        "REQUIRES_REVIEW": 0,
        "fetch_failed": 0,
    }
    for r in results:
        for s in r.get("status", []):
            if s in status_counts:
                status_counts[s] += 1

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "live_base": LIVE_BASE,
        "sphinx_html": str(LOCAL_HTML),
        "counts": {
            "live_pages": len(results),
            "mint_pages": mint_count,
            **status_counts,
        },
        "pages": results,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_md(report)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print("Counts:", status_counts)


if __name__ == "__main__":
    main()
