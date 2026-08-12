#!/usr/bin/env python3
"""Live RTD vs Mintlify content parity audit — August 2026.

Phase 1: fetch live pages, compare to Mintlify MD, write JSON + MD reports.
"""
from __future__ import annotations

import json
import re
import time
import zlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, NavigableString, Tag

# Prefer real git repo (name may contain a space); fall back to adjacent MintilifyDoc.
_BASE = Path("/Users/nitsan/www/AI Agents")
ROOT = next(
    (
        p
        for p in _BASE.iterdir()
        if (p / ".git").exists() and (p / "ExtNsT3AF").exists()
    ),
    next(p for p in _BASE.iterdir() if p.name == "MintilifyDoc"),
)
LIVE_BASE = "https://docs.t3planet.de/en/latest/"
# Offline Sphinx HTML fallback when Cloudflare challenges live RTD (not Live-docs/).
LOCAL_HTML_CANDIDATES = [
    Path("/Users/nitsan/www/AI Agents/T3Planet Docs Agent/docs/docs/_build/html"),
    ROOT / "docs" / "_build" / "html",
]
LOCAL_HTML = next((c for c in LOCAL_HTML_CANDIDATES if c.is_dir()), None)
OUT_JSON = ROOT / "scripts/qa-final/LIVE_CONTENT_PARITY_AUG2026.json"
OUT_MD = ROOT / "scripts/qa-final/LIVE_CONTENT_PARITY_AUG2026.md"
UA = "Mozilla/5.0 (compatible; MintlifyParityBot/1.0; +https://docs.t3planet.de)"
SLEEP = 0.12
TIMEOUT = 30
WORKERS = 3

SKIP_NAMES = {"genindex", "search", "py-modindex", "history", "readme"}
SUPADEMO_RE = re.compile(
    r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", re.I
)
MD_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']",
    re.I,
)
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.M)


def resolve_mint_path(live_doc: str) -> Path | None:
    """Map live Sphinx doc path to a Mintlify .md file."""
    live_doc = unquote(live_doc)
    parts = live_doc.strip("/").split("/")
    if not parts:
        return None

    # T3AF ↔ ExtNsT3AF (canonical mint is ExtNsT3AF)
    if parts[0] == "T3AF":
        parts = ["ExtNsT3AF"] + parts[1:]

    # EXTKarma renames
    if parts[0] == "EXTKarma" and len(parts) >= 2:
        renames = {
            "ConfigureCaptcha": "CaptchaConfiguration",
            "CustomElements": "ContentBlockElements",
            "UpgradeGuide": "UpgradeGuideForContainer",
        }
        if parts[1] in renames:
            parts = [parts[0], renames[parts[1]]] + parts[2:]

    # Prefer Index.md under folder, else Support.md style leaf
    candidates: list[Path] = []
    base = ROOT.joinpath(*parts)
    if parts[-1] == "Index":
        candidates.append(ROOT.joinpath(*parts[:-1], "Index.md") if len(parts) > 1 else ROOT / "Index.md")
        candidates.append(base.with_suffix(".md"))
    else:
        candidates.append(base.with_suffix(".md"))
        candidates.append(base / "Index.md")

    # Also try ExtNsT3AF if still T3AF somehow
    for c in list(candidates):
        s = str(c)
        if "/T3AF/" in s or s.endswith("/T3AF.md"):
            candidates.append(Path(s.replace("/T3AF/", "/ExtNsT3AF/").replace("/T3AF.md", "/ExtNsT3AF.md")))

    seen = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        if c.is_file():
            return c
    return None


def load_live_pages() -> list[str]:
    """Load doc paths from objects.inv or homepage toctree."""
    pages: list[str] = []
    inv_local = ROOT / "scripts/qa-final/objects.inv"
    inv_bytes: bytes | None = None
    if inv_local.is_file():
        inv_bytes = inv_local.read_bytes()
    else:
        try:
            with urlopen(Request(LIVE_BASE + "objects.inv", headers={"User-Agent": UA}), timeout=TIMEOUT) as r:
                inv_bytes = r.read()
            inv_local.write_bytes(inv_bytes)
        except Exception:
            inv_bytes = None

    if inv_bytes:
        try:
            rest = inv_bytes.split(b"\n", 4)[-1]
            data = zlib.decompress(rest).decode("utf-8", errors="replace")
            for line in data.splitlines():
                if not line.strip() or line.startswith("#"):
                    continue
                # name domain role priority uri dispname
                bits = line.split(" ", 4)
                if len(bits) < 5:
                    continue
                name, domain_role, priority, uri = bits[0], bits[1], bits[2], bits[3]
                if domain_role != "std:doc":
                    continue
                doc = uri.replace(".html", "").rstrip("/")
                if doc.startswith("-") or doc == "-":
                    doc = name
                doc = doc.split("#", 1)[0]
                base = doc.split("/")[-1].lower()
                if base in SKIP_NAMES:
                    continue
                if doc and doc not in pages:
                    pages.append(doc)
        except Exception as e:
            print("objects.inv parse failed:", e)
            pages = []

    if not pages and LOCAL_HTML:
        for html_path in LOCAL_HTML.rglob("*.html"):
            rel = html_path.relative_to(LOCAL_HTML).as_posix()
            if rel.startswith("_"):
                continue
            doc = rel[:-5]
            base = doc.split("/")[-1].lower()
            if base in SKIP_NAMES:
                continue
            if doc and doc not in pages:
                pages.append(doc)

    if not pages:
        # scrape homepage (may fail under Cloudflare)
        try:
            with urlopen(Request(LIVE_BASE, headers={"User-Agent": UA}), timeout=TIMEOUT) as r:
                html = r.read().decode("utf-8", errors="replace")
            soup = BeautifulSoup(html, "html.parser")
            for a in soup.select("a[href]"):
                href = a.get("href") or ""
                if "#" in href:
                    href = href.split("#", 1)[0]
                if not href.endswith(".html"):
                    continue
                href = href.replace("./", "").lstrip("/")
                if href.startswith("http"):
                    continue
                doc = href[:-5]
                base = doc.split("/")[-1].lower()
                if base in SKIP_NAMES:
                    continue
                if doc and doc not in pages:
                    pages.append(doc)
        except Exception as e:
            print("homepage scrape failed:", e)

    pages.sort()
    return pages


def fetch(url: str, retries: int = 5) -> tuple[int, str]:
    last_status = 0
    for attempt in range(retries):
        try:
            with urlopen(Request(url, headers={"User-Agent": UA}), timeout=TIMEOUT) as r:
                return r.status, r.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            last_status = e.code
            if e.code in (429, 503, 502):
                time.sleep(2.0 * (attempt + 1))
                continue
            return e.code, ""
        except (URLError, TimeoutError, Exception):
            last_status = 0
            time.sleep(1.0 * (attempt + 1))
            continue
    return last_status, ""


def visible_text(el: Tag) -> str:
    for bad in el.find_all(["script", "style", "noscript"]):
        bad.decompose()
    return re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()


def extract_live(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    main = (
        soup.select_one('[role="main"]')
        or soup.select_one("div.document")
        or soup.select_one("article")
        or soup.body
        or soup
    )
    text = visible_text(main) if isinstance(main, Tag) else ""
    headings = []
    for h in main.find_all(["h2", "h3"]):
        t = re.sub(r"\s*[¶]\s*$", "", h.get_text(" ", strip=True))
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            headings.append({"level": h.name, "text": t})
    imgs = []
    for img in main.find_all("img"):
        src = (img.get("src") or "").strip()
        if not src:
            continue
        if src.startswith("data:"):
            continue
        # relative _images/ or local
        if "_images/" in src or not src.startswith("http"):
            imgs.append(src)
        elif "docs.t3planet.de" in src:
            imgs.append(src)
    ids = set()
    for m in SUPADEMO_RE.finditer(str(main)):
        ids.add(m.group(1).lower())
    for iframe in main.select("iframe[src]"):
        src = iframe.get("src") or ""
        m = SUPADEMO_RE.search(src)
        if m:
            ids.add(m.group(1).lower())
    return {
        "text_len": len(text),
        "headings": headings,
        "image_count": len(imgs),
        "image_srcs": imgs,
        "supademo_ids": sorted(ids),
    }


def extract_mint(md_path: Path) -> dict[str, Any]:
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    body = FRONTMATTER_RE.sub("", raw, count=1)
    # strip obvious MDX component noise lightly for length
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"[#*_`>\[\]\(\)!|-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    headings = []
    for m in HEADING_RE.finditer(body):
        headings.append({"level": "h2" if m.group(1) == "##" else "h3", "text": m.group(2).strip()})
    img_count = 0
    for m in MD_IMG_RE.finditer(body):
        src = m.group(2) or m.group(3) or ""
        if src and not src.startswith("data:"):
            img_count += 1
    ids = {m.group(1).lower() for m in SUPADEMO_RE.finditer(body)}
    return {
        "text_len": len(text),
        "headings": headings,
        "image_count": img_count,
        "supademo_ids": sorted(ids),
        "path": str(md_path.relative_to(ROOT)),
    }


def classify(live: dict, mint: dict | None) -> list[str]:
    tags: list[str] = []
    if mint is None:
        tags.append("missing_page")
        return tags
    live_ids = set(live.get("supademo_ids") or [])
    mint_ids = set(mint.get("supademo_ids") or [])
    missing_ids = sorted(live_ids - mint_ids)
    if missing_ids:
        tags.append("missing_supademo")
    lt = live.get("text_len") or 0
    mt = mint.get("text_len") or 0
    if lt > 800 and mt < 0.4 * lt:
        tags.append("thin_content")
    if (live.get("image_count") or 0) > (mint.get("image_count") or 0) + 2:
        tags.append("missing_images")
    return tags


def load_local_html(doc: str) -> str | None:
    if not LOCAL_HTML:
        return None
    # try exact + unquoted variants
    candidates = [doc, unquote(doc)]
    for d in candidates:
        path = LOCAL_HTML / f"{d}.html"
        if path.is_file():
            return path.read_text(encoding="utf-8", errors="replace")
    return None


def process_page(doc: str) -> dict[str, Any]:
    time.sleep(SLEEP)
    url = LIVE_BASE + doc + ".html"
    status, html = fetch(url)
    source = "live"
    if status != 200 or not html:
        local = load_local_html(doc)
        if local:
            html = local
            status = 200
            source = "local_html_fallback"
    mint_path = resolve_mint_path(doc)
    row: dict[str, Any] = {
        "live": doc,
        "live_url": url,
        "http_status": status,
        "html_source": source if html else "none",
        "mint": str(mint_path.relative_to(ROOT)) if mint_path else None,
    }
    if status != 200 or not html:
        row["live_extract"] = None
        row["mint_extract"] = extract_mint(mint_path) if mint_path else None
        row["issues"] = ["fetch_failed"] + (["missing_page"] if not mint_path else [])
        row["missing_supademo_ids"] = []
        return row
    live_ex = extract_live(html)
    mint_ex = extract_mint(mint_path) if mint_path else None
    issues = classify(live_ex, mint_ex)
    missing_ids = sorted(set(live_ex["supademo_ids"]) - set((mint_ex or {}).get("supademo_ids") or []))
    row["live_extract"] = {
        "text_len": live_ex["text_len"],
        "heading_count": len(live_ex["headings"]),
        "headings": live_ex["headings"],
        "image_count": live_ex["image_count"],
        "supademo_ids": live_ex["supademo_ids"],
    }
    row["mint_extract"] = mint_ex
    row["issues"] = issues
    row["missing_supademo_ids"] = missing_ids
    if mint_ex and live_ex["text_len"]:
        row["text_ratio"] = round(mint_ex["text_len"] / live_ex["text_len"], 3)
    else:
        row["text_ratio"] = None
    return row


def write_md(report: dict) -> None:
    c = report["counts"]
    lines = [
        "# Live Content Parity — August 2026",
        "",
        f"**Generated:** {report['generated']}",
        f"**Repo:** `{report['repo']}`",
        f"**Live base:** {LIVE_BASE}",
        "",
        "## Summary counts",
        "",
        f"- Live pages audited: **{c['live_pages']}**",
        f"- missing_page: **{c['missing_page']}**",
        f"- missing_supademo: **{c['missing_supademo']}**",
        f"- thin_content: **{c['thin_content']}**",
        f"- missing_images: **{c['missing_images']}**",
        f"- ok (no issues): **{c['ok']}**",
        f"- fetch_failed: **{c['fetch_failed']}**",
        "",
        "## Top gaps",
        "",
        "### Missing pages",
        "",
    ]
    mp = [r for r in report["pages"] if "missing_page" in r.get("issues", [])]
    for r in mp[:40]:
        lines.append(f"- `{r['live']}`")
    if len(mp) > 40:
        lines.append(f"- … and {len(mp) - 40} more")
    lines += ["", "### Missing Supademo", ""]
    ms = [r for r in report["pages"] if "missing_supademo" in r.get("issues", [])]
    for r in sorted(ms, key=lambda x: -len(x.get("missing_supademo_ids") or []))[:40]:
        ids = ", ".join(r.get("missing_supademo_ids") or [])
        lines.append(f"- `{r['live']}` → `{r.get('mint')}` missing IDs: {ids}")
    if len(ms) > 40:
        lines.append(f"- … and {len(ms) - 40} more")
    lines += ["", "### Thin content (worst ratios)", ""]
    th = [r for r in report["pages"] if "thin_content" in r.get("issues", [])]
    th.sort(key=lambda x: (x.get("text_ratio") is None, x.get("text_ratio") or 0))
    for r in th[:40]:
        lt = (r.get("live_extract") or {}).get("text_len")
        mt = (r.get("mint_extract") or {}).get("text_len")
        lines.append(
            f"- `{r['live']}` ratio={r.get('text_ratio')} live={lt} mint={mt} file=`{r.get('mint')}`"
        )
    if len(th) > 40:
        lines.append(f"- … and {len(th) - 40} more")
    lines += ["", "### Missing images", ""]
    mi = [r for r in report["pages"] if "missing_images" in r.get("issues", [])]
    for r in mi[:40]:
        li = (r.get("live_extract") or {}).get("image_count")
        mi_ = (r.get("mint_extract") or {}).get("image_count")
        lines.append(f"- `{r['live']}` live_imgs={li} mint_imgs={mi_} file=`{r.get('mint')}`")
    if len(mi) > 40:
        lines.append(f"- … and {len(mi) - 40} more")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    import os
    print(f"ROOT={ROOT}")
    print(f"LOCAL_HTML={LOCAL_HTML}")
    local_only = os.environ.get("PARITY_LOCAL_ONLY", "").strip() in {"1", "true", "yes"}
    if local_only:
        print("PARITY_LOCAL_ONLY=1 — skipping live HTTP, using local Sphinx HTML")
        global SLEEP, WORKERS
        SLEEP = 0
        WORKERS = 16
    pages = load_live_pages()
    print(f"Live pages: {len(pages)}")

    def process_page_local(doc: str) -> dict[str, Any]:
        if not local_only:
            return process_page(doc)
        url = LIVE_BASE + doc + ".html"
        html = load_local_html(doc)
        mint_path = resolve_mint_path(doc)
        row: dict[str, Any] = {
            "live": doc,
            "live_url": url,
            "http_status": 200 if html else 0,
            "html_source": "local_html_fallback" if html else "none",
            "mint": str(mint_path.relative_to(ROOT)) if mint_path else None,
        }
        if not html:
            row["live_extract"] = None
            row["mint_extract"] = extract_mint(mint_path) if mint_path else None
            row["issues"] = ["fetch_failed"] + (["missing_page"] if not mint_path else [])
            row["missing_supademo_ids"] = []
            return row
        live_ex = extract_live(html)
        mint_ex = extract_mint(mint_path) if mint_path else None
        issues = classify(live_ex, mint_ex)
        missing_ids = sorted(set(live_ex["supademo_ids"]) - set((mint_ex or {}).get("supademo_ids") or []))
        row["live_extract"] = {
            "text_len": live_ex["text_len"],
            "heading_count": len(live_ex["headings"]),
            "headings": live_ex["headings"],
            "image_count": live_ex["image_count"],
            "supademo_ids": live_ex["supademo_ids"],
        }
        row["mint_extract"] = mint_ex
        row["issues"] = issues
        row["missing_supademo_ids"] = missing_ids
        if mint_ex and live_ex["text_len"]:
            row["text_ratio"] = round(mint_ex["text_len"] / live_ex["text_len"], 3)
        else:
            row["text_ratio"] = None
        return row

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = {ex.submit(process_page_local, doc): doc for doc in pages}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 50 == 0 or done == len(pages):
                print(f"  processed {done}/{len(pages)}")

    results.sort(key=lambda r: r["live"])
    counts = {
        "live_pages": len(results),
        "missing_page": sum(1 for r in results if "missing_page" in r.get("issues", [])),
        "missing_supademo": sum(1 for r in results if "missing_supademo" in r.get("issues", [])),
        "thin_content": sum(1 for r in results if "thin_content" in r.get("issues", [])),
        "missing_images": sum(1 for r in results if "missing_images" in r.get("issues", [])),
        "fetch_failed": sum(1 for r in results if "fetch_failed" in r.get("issues", [])),
        "ok": sum(1 for r in results if not r.get("issues")),
    }
    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "live_base": LIVE_BASE,
        "counts": counts,
        "pages": results,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_md(report)
    local_n = sum(1 for r in results if r.get("html_source") == "local_html_fallback")
    live_n = sum(1 for r in results if r.get("html_source") == "live")
    counts["html_from_live"] = live_n
    counts["html_from_local_fallback"] = local_n
    print("\n=== SUMMARY ===")
    for k, v in counts.items():
        print(f"{k}: {v}")
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
