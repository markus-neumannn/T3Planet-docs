#!/usr/bin/env python3
"""Full production-readiness audit: live RTD inventory vs Mintlify docs.

Usage:
  python3 scripts/production_readiness_audit.py
  python3 scripts/production_readiness_audit.py --searchindex-file scripts/_cache_searchindex.js
  python3 scripts/production_readiness_audit.py --skip-http --concurrency 12
"""
from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from migrate_from_live import (  # noqa: E402
    PRODUCT_ROOT_MAP,
    SEGMENT_MAP,
    live_to_mint_path,
    normalize_live_rel,
)

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None  # type: ignore

LIVE_BASE = "https://docs.t3planet.de/en/latest/"
SEARCHINDEX_URL = urljoin(LIVE_BASE, "searchindex.js")
SEARCHINDEX_CACHE = SCRIPTS / "_cache_searchindex.js"
_LOCAL_HTML_CANDIDATES = [
    ROOT / "Live-docs" / "docs" / "_build" / "html",
    ROOT / "docs" / "_build" / "html",
]
LOCAL_HTML_ROOT = next(
    (p for p in _LOCAL_HTML_CANDIDATES if p.is_dir()),
    _LOCAL_HTML_CANDIDATES[-1],
)
MINT_BASE = os.environ.get("MINTLIFY_URL", "http://127.0.0.1:3000").rstrip("/")
USER_AGENT = "MintlifyDoc-ProductionReadinessAudit/1.0"
EXCLUDE_DOCNAMES = {"genindex", "search", "history", "readme"}

REPORT_JSON = SCRIPTS / "production-readiness-audit.json"
REPORT_MD = SCRIPTS / "PRODUCTION_READINESS_AUDIT.md"

IMG_MD_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_HTML_RE = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
LINK_MD_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```", re.M)
TABLE_PIPE_RE = re.compile(r"^\|.+\|$", re.M)
CALLOUT_RE = re.compile(
    r"<(Note|Warning|Tip|Info|Check|Danger)\b|^>\s*\*\*(?:Note|Warning|Tip|Info)\*\*",
    re.M | re.I,
)
HEADING_MD_RE = re.compile(r"^#{1,3}\s+\S", re.M)
FM_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.S)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9\-']*")


def fetch(url: str, timeout: int = 60, retries: int = 6) -> str:
    last_err: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/javascript,*/*"},
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            last_err = exc
            if exc.code in (429, 503, 502, 500) and attempt < retries - 1:
                ra = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    delay = float(ra) if ra and str(ra).isdigit() else (2.5 * (2 ** attempt) + random.random())
                except Exception:  # noqa: BLE001
                    delay = 2.5 * (2 ** attempt) + random.random()
                delay = min(delay, 90.0)
                print(f"  retry {attempt + 1}/{retries} after HTTP {exc.code} sleep {delay:.1f}s")
                time.sleep(delay)
                continue
            raise
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            if attempt < retries - 1:
                time.sleep(min(2.0 * (2 ** attempt) + random.random(), 60.0))
                continue
            raise
    raise RuntimeError(f"fetch failed for {url}: {last_err}")


def fetch_status(url: str, timeout: int = 30, retries: int = 3) -> tuple[int, str]:
    last_exc: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
                return int(resp.status), body
        except urllib.error.HTTPError as exc:
            try:
                body = exc.read().decode("utf-8", errors="replace")
            except Exception:  # noqa: BLE001
                body = ""
            return int(exc.code), body
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(0.8 * (attempt + 1))
    return 0, str(last_exc)


def parse_docnames(js: str) -> list[str]:
    m = re.search(r'"docnames"\s*:\s*\[(.*?)\]', js, re.S)
    if not m:
        raise RuntimeError("Could not parse docnames from searchindex.js")
    names = re.findall(r'"([^"]+)"', m.group(1))
    out: list[str] = []
    for n in names:
        leaf = n.rsplit("/", 1)[-1].lower()
        if n.lower() in EXCLUDE_DOCNAMES or leaf in EXCLUDE_DOCNAMES:
            continue
        out.append(n)
    return out


def mint_candidates(live_docname: str) -> list[str]:
    live_rel = normalize_live_rel(live_docname)
    if not live_rel.endswith(".html"):
        live_rel = f"{live_rel}.html" if live_rel != "index" else "index.html"

    cands: list[str] = []

    def add(p: str) -> None:
        p = p.replace("\\", "/")
        if p not in cands:
            cands.append(p)

    try:
        add(live_to_mint_path(live_rel))
    except Exception:  # noqa: BLE001
        pass

    parts = [p for p in live_docname.split("/") if p]
    if parts:
        product = parts[0]
        mint_root = PRODUCT_ROOT_MAP.get(product, product)
        rest = parts[1:]
        if not rest:
            add(f"{mint_root}/Index.md" if mint_root != "index" else "index.md")
        else:
            mapped_rest = []
            for seg in rest:
                if seg in {"BuyNow", "buynow"} and mint_root == "T3AF":
                    mapped_rest.append("GetThisExtension")
                elif seg == "QuickSetup":
                    mapped_rest.append("SetupWizard")
                else:
                    mapped_rest.append(seg)
            last = mapped_rest[-1]
            if last == "Index":
                add(f"{mint_root}/{'/'.join(mapped_rest)}.md")
            elif len(mapped_rest) == 1:
                add(f"{mint_root}/{last}/Index.md")
                add(f"{mint_root}/{last}.md")
            else:
                add(f"{mint_root}/{'/'.join(mapped_rest)}/Index.md")
                add(f"{mint_root}/{'/'.join(mapped_rest)}.md")

            seg_rest = [SEGMENT_MAP.get(s, s) for s in rest]
            if seg_rest != mapped_rest:
                last = seg_rest[-1]
                if last == "Index":
                    add(f"{mint_root}/{'/'.join(seg_rest)}.md")
                else:
                    add(f"{mint_root}/{'/'.join(seg_rest)}/Index.md")

            leaf = rest[-1] if rest[-1] != "Index" else (rest[-2] if len(rest) > 1 else None)
            if leaf and mint_root == "T3AF":
                for hit in sorted((ROOT / mint_root).rglob(f"{leaf}/Index.md")):
                    add(str(hit.relative_to(ROOT)))
                leaf2 = SEGMENT_MAP.get(leaf, leaf)
                if leaf2 != leaf:
                    for hit in sorted((ROOT / mint_root).rglob(f"{leaf2}/Index.md")):
                        add(str(hit.relative_to(ROOT)))

    if live_docname == "index":
        add("index.md")
    return cands


def resolve_mint_path(live_docname: str) -> tuple[str | None, list[str]]:
    cands = mint_candidates(live_docname)
    for c in cands:
        if (ROOT / c).is_file():
            return c, cands
    return None, cands


def strip_frontmatter(md: str) -> str:
    return FM_RE.sub("", md, count=1)


def basename_stem(path: str) -> str:
    name = Path(unquote(path.split("?")[0].split("#")[0])).name
    return Path(name).stem.lower()


def extract_live_metrics(html: str) -> dict[str, Any]:
    if BeautifulSoup is None:
        raise RuntimeError("BeautifulSoup required")
    soup = BeautifulSoup(html, "html.parser")
    body = (
        soup.select_one("div.rst-content")
        or soup.select_one("[itemprop=articleBody]")
        or soup.select_one("article")
        or soup.select_one("div[role=main]")
        or soup.body
    )
    if body is None:
        return {
            "headings": 0, "images": 0, "tables": 0, "admonitions": 0,
            "code": 0, "words": 0, "image_stems": [], "error": "no body",
        }

    for sel in (
        "div[aria-label='Related Topics']", "footer", "nav",
        "div.wy-breadcrumbs", "div.rst-footer-buttons",
    ):
        for node in body.select(sel):
            node.decompose()

    headings = len(body.find_all(re.compile(r"^h[1-3]$")))
    imgs = body.find_all("img")
    image_stems = [basename_stem(img.get("src") or "") for img in imgs if img.get("src")]
    tables = len(body.find_all("table"))
    admonitions = len(
        body.select(
            "div.admonition, div.note, div.warning, div.tip, div.important, "
            "div.caution, div.danger, div.hint, div.seealso, div.attention, div.error"
        )
    )
    # Count highlight blocks once (avoid double-count pre inside div.highlight)
    highlights = body.select("div.highlight")
    pres_outside = [pre for pre in body.find_all("pre") if not pre.find_parent("div", class_="highlight")]
    code_blocks = len(highlights) + len(pres_outside)
    text = body.get_text(" ", strip=True)
    words = len(WORD_RE.findall(text))
    return {
        "headings": headings,
        "images": len(imgs),
        "tables": tables,
        "admonitions": admonitions,
        "code": code_blocks,
        "words": words,
        "image_stems": sorted(set(s for s in image_stems if s)),
    }


def extract_mint_metrics(md_text: str) -> dict[str, Any]:
    body = strip_frontmatter(md_text)
    headings = len(HEADING_MD_RE.findall(body))
    img_paths = [m.group(1).strip().strip("<>") for m in IMG_MD_RE.finditer(body)]
    img_paths += [m.group(1).strip() for m in IMG_HTML_RE.finditer(body)]
    image_stems = [basename_stem(p) for p in img_paths if p and not p.startswith("http")]
    images = len(img_paths)
    tables = max(0, len(body.lower().split("<table")) - 1)
    if TABLE_PIPE_RE.findall(body):
        blocks = 0
        in_block = False
        for line in body.splitlines():
            if TABLE_PIPE_RE.match(line.strip()):
                if not in_block:
                    blocks += 1
                    in_block = True
            else:
                in_block = False
        tables = max(tables, blocks)
    callouts = len(CALLOUT_RE.findall(body))
    fences = FENCE_RE.findall(body)
    code = max(0, len(fences) // 2) if fences else 0
    code += len(re.findall(r"<pre\b", body, flags=re.I))
    card_titles = re.findall(r'<Card\b[^>]*\btitle="([^"]+)"', body)
    fence_bodies = re.findall(r"```[\w-]*\n(.*?)```", body, flags=re.S)
    no_fence = re.sub(r"```.*?```", " ", body, flags=re.S)
    no_tags = re.sub(r"<[^>]+>", " ", no_fence)
    words = (
        len(WORD_RE.findall(no_tags))
        + len(WORD_RE.findall(" ".join(card_titles)))
        + len(WORD_RE.findall(" ".join(fence_bodies)))
    )
    return {
        "headings": headings,
        "images": images,
        "tables": tables,
        "admonitions": callouts,
        "code": code,
        "words": words,
        "image_stems": sorted(set(s for s in image_stems if s)),
        "has_cards": bool(card_titles),
    }


def compare_metrics(live: dict[str, Any], mint: dict[str, Any], mint_raw: str | None = None) -> list[str]:
    defects: list[str] = []
    lw, mw = live.get("words", 0), mint.get("words", 0)
    hub = bool(mint_raw and "<Card" in mint_raw and mint_raw.count("<Card") >= 3)
    if (not hub) and lw > 80 and mw < 0.55 * lw:
        defects.append("words")
    if mint.get("headings", 0) < live.get("headings", 0) - 2:
        defects.append("headings")
    live_stems = set(live.get("image_stems") or [])
    mint_stems = set(mint.get("image_stems") or [])
    if live.get("images", 0) > 0:
        mint_media = mint.get("images", 0)
        if mint_raw:
            mint_media += len(re.findall(r"<iframe\b", mint_raw, flags=re.I))
            mint_media += len(re.findall(r"supademo\.com|youtube\.com|youtu\.be", mint_raw, flags=re.I))
        if mint_media < live.get("images", 0) - 1:
            if live_stems and len(mint_stems & live_stems) >= max(0, len(live_stems) - 1):
                pass
            else:
                defects.append("images")
    if mint.get("code", 0) < live.get("code", 0) - 1:
        defects.append("code")
    if mint.get("tables", 0) < live.get("tables", 0) - 1:
        defects.append("tables")
    if mint.get("admonitions", 0) < live.get("admonitions", 0) - 1:
        defects.append("callouts")
    return defects


def collect_nav_pages(docs: dict) -> list[str]:
    pages: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, str):
            pages.append(node)
        elif isinstance(node, list):
            for x in node:
                walk(x)
        elif isinstance(node, dict):
            if "pages" in node:
                walk(node["pages"])
            if "groups" in node:
                walk(node["groups"])
            for key in ("root", "page"):
                if isinstance(node.get(key), str):
                    pages.append(node[key])

    walk(docs.get("navigation"))
    seen: set[str] = set()
    out: list[str] = []
    for p in pages:
        p = p.strip().lstrip("/")
        if p.endswith(".md"):
            p = p[:-3]
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def route_to_url(route: str) -> str:
    r = route.strip().lstrip("/")
    if r.endswith(".md"):
        r = r[:-3]
    return f"{MINT_BASE}/{r}"


def md_path_for_route(route: str) -> Path:
    r = route.strip().lstrip("/")
    if r.endswith(".md"):
        return ROOT / r
    p1 = ROOT / f"{r}.md"
    if p1.is_file():
        return p1
    p2 = ROOT / f"{r}/Index.md"
    if p2.is_file():
        return p2
    return p1


def scan_broken_images_and_links() -> tuple[list[dict], list[dict]]:
    broken_imgs: list[dict] = []
    broken_links: list[dict] = []
    skip_prefixes = ("de/", "scripts/", "docs/", "visual-regression/", ".venv")

    md_files = []
    for p in ROOT.rglob("*.md"):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if any(rel.startswith(s) for s in skip_prefixes) or "/de/" in rel:
            continue
        md_files.append(p)

    valid_routes: set[str] = set()
    for p in md_files:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel.endswith(".md"):
            route = rel[:-3]
            valid_routes.add(route)
            valid_routes.add(route.lower())
            if route.endswith("/Index"):
                valid_routes.add(route[: -len("/Index")])
                valid_routes.add(route[: -len("/Index")].lower())
            if route == "index":
                valid_routes.add("")
                valid_routes.add("index")

    for p in md_files:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        text = p.read_text(encoding="utf-8", errors="replace")
        body = strip_frontmatter(text)
        for m in IMG_MD_RE.finditer(body):
            src = m.group(1).strip().strip("<>").split()[0] if m.group(1).strip() else ""
            src = src.split("#")[0].split("?")[0]
            if not src or src.startswith(("http://", "https://", "data:", "mailto:")):
                continue
            target = ROOT / src.lstrip("/") if src.startswith("/") else (p.parent / src).resolve()
            try:
                target.relative_to(ROOT.resolve())
            except ValueError:
                broken_imgs.append({"file": rel, "src": src, "reason": "outside root"})
                continue
            if not target.is_file():
                alt = None
                if target.suffix.lower() == ".png":
                    alt = target.with_suffix(".webp")
                elif target.suffix.lower() == ".webp":
                    alt = target.with_suffix(".png")
                elif target.suffix.lower() in {".jpg", ".jpeg"}:
                    alt = target.with_suffix(".webp")
                if alt and alt.is_file():
                    continue
                broken_imgs.append({"file": rel, "src": src})

        for m in LINK_MD_RE.finditer(body):
            href = m.group(1).strip().strip("<>").split()[0] if m.group(1).strip() else ""
            if not href or href.startswith(
                ("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:", "linkhttp://", "linkhttps://")
            ):
                continue
            if href.startswith("//"):
                continue
            path = href.split("#")[0].split("?")[0]
            if not path:
                continue
            if not path.startswith("/"):
                if path.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf", ".zip", ".md")):
                    target = (p.parent / path).resolve()
                    if not target.is_file():
                        broken_links.append({"file": rel, "href": href, "reason": "missing relative"})
                    continue
                route = str(Path(rel).parent / path).replace("\\", "/")
            else:
                route = path.lstrip("/")
            if route.endswith(".md"):
                route = route[:-3]
            route = route.rstrip("/")
            if "." in Path(route).name and not route.endswith("Index"):
                asset = ROOT / route
                if not asset.is_file():
                    broken_links.append({"file": rel, "href": href, "reason": "missing asset route"})
                continue
            candidates = {route, route + "/Index", f"{route}/Index"}
            if not any(c in valid_routes or c.lower() in valid_routes for c in candidates):
                if (
                    not (ROOT / f"{route}.md").is_file()
                    and not (ROOT / route / "Index.md").is_file()
                    and not (ROOT / f"{route}/Index.md").is_file()
                ):
                    broken_links.append({"file": rel, "href": href, "route": route, "reason": "missing route"})
    return broken_imgs, broken_links


def pick_http_routes(nav_pages: list[str], missing_mint: list[str], all_index_mds: list[str]) -> list[str]:
    routes: list[str] = []
    seen: set[str] = set()

    def add(r: str) -> None:
        r = r.strip().lstrip("/")
        if r.endswith(".md"):
            r = r[:-3]
        if r and r not in seen:
            seen.add(r)
            routes.append(r)

    for p in sorted(ROOT.glob("*/Index.md")):
        add(str(p.relative_to(ROOT).with_suffix("")).replace("\\", "/"))
    add("index")
    for m in missing_mint:
        add(m[:-3] if m.endswith(".md") else m)
    for rel in all_index_mds:
        add(rel[:-3] if rel.endswith(".md") else rel)
    for n in nav_pages:
        add(n)
    return routes


def quick_verify() -> dict[str, Any]:
    mintignore = (ROOT / ".mintignore").read_text(encoding="utf-8") if (ROOT / ".mintignore").is_file() else ""
    excludes_docs = "docs/" in mintignore
    excludes_de = bool(re.search(r"(?m)^de/?\s*$", mintignore)) or mintignore.startswith("de/")
    css = (ROOT / "custom.css").read_text(encoding="utf-8") if (ROOT / "custom.css").is_file() else ""
    has_hardening = "RESPONSIVE HARDENING" in css or "responsive hardening" in css.lower()
    sample_route = "T3AF/Introduction/Index"
    status, body = fetch_status(route_to_url(sample_route), timeout=45, retries=4)
    return {
        "mintignore_excludes_docs": excludes_docs,
        "mintignore_excludes_de": excludes_de,
        "custom_css_responsive_hardening": has_hardening,
        "sample_page": sample_route,
        "sample_http_status": status,
        "sample_has_Search_setIndex": "Search.setIndex" in body if status == 200 else None,
    }


def load_live_html(live_docname: str) -> tuple[str, str, str]:
    live_html_path = f"{live_docname}.html" if live_docname != "index" else "index.html"
    local = LOCAL_HTML_ROOT / live_html_path
    url = urljoin(LIVE_BASE, live_html_path)
    if local.is_file():
        return local.read_text(encoding="utf-8", errors="replace"), "local", str(local)
    html = fetch(url, timeout=90, retries=5)
    return html, "live", url


def content_job(live_docname: str, mint_rel: str | None) -> dict[str, Any]:
    url = urljoin(LIVE_BASE, f"{live_docname}.html" if live_docname != "index" else "index.html")
    result: dict[str, Any] = {"live": live_docname, "mint": mint_rel, "url": url}
    try:
        html, source, src = load_live_html(live_docname)
        result["html_source"] = source
        result["html_src"] = src
        live_m = extract_live_metrics(html)
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"live fetch: {exc}"
        result["defects"] = ["fetch_error"]
        return result
    result["live_metrics"] = {k: v for k, v in live_m.items() if k != "image_stems"}
    result["live_image_stems"] = live_m.get("image_stems", [])

    if not mint_rel:
        result["defects"] = ["missing"]
        return result
    md_path = ROOT / mint_rel
    if not md_path.is_file():
        result["defects"] = ["missing"]
        return result
    try:
        md_text = md_path.read_text(encoding="utf-8", errors="replace")
        mint_m = extract_mint_metrics(md_text)
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"mint read: {exc}"
        result["defects"] = ["mint_error"]
        return result
    result["mint_metrics"] = {k: v for k, v in mint_m.items() if k not in {"image_stems", "has_cards"}}
    result["mint_image_stems"] = mint_m.get("image_stems", [])
    result["defects"] = compare_metrics(live_m, mint_m, md_text)
    return result


def write_reports(report: dict[str, Any]) -> None:
    REPORT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    missing = report.get("missing", [])
    defects = report.get("content_defects", [])
    by_type = report.get("defect_counts_by_type", {})
    lines = [
        "# Production Readiness Audit",
        "",
        f"**Generated:** {report.get('generated_at')}",
        f"**Live SoT:** {LIVE_BASE}",
        f"**Mint preview:** {MINT_BASE}",
        "",
        "## Summary",
        "",
        f"- Live pages (filtered): **{report['live_pages']}**",
        f"- Mint mapped (file exists): **{report['mint_mapped']}**",
        f"- Missing: **{report['missing_count']}**",
        f"- Content defects (pages): **{report['content_defect_pages']}**",
        f"- Fetch errors (unchecked vs live HTML): **{report.get('fetch_error_pages', 0)}**",
        f"- Broken images: **{report['broken_images_count']}**",
        f"- Broken internal links: **{report['broken_links_count']}**",
        f"- HTTP failures: **{report['http_fail_count']}** / {report.get('http_checked', 0)} checked",
        f"- Nav paths missing files: **{report.get('nav_missing_files_count', 0)}**",
        f"- Orphan EN product Index.md (warn): **{report.get('orphan_index_count', 0)}**",
        f"- Verdict: **{report['verdict']}**",
        "",
        "### Defect counts by type",
        "",
    ]
    for k, v in sorted(by_type.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {k}: {v}")
    if not by_type:
        lines.append("- (none)")
    lines += ["", "### Quick verify", ""]
    for k, v in (report.get("quick_verify") or {}).items():
        lines.append(f"- `{k}`: {v}")
    if missing:
        lines += ["", "## Missing pages", ""]
        for m in missing[:100]:
            lines.append(f"- `{m['live']}` → expected `{m.get('expected')}`")
    if defects:
        lines += ["", "## Content defect pages", ""]
        for d in defects[:150]:
            lines.append(
                f"- `{d['live']}` → `{d.get('mint')}` defects={d.get('defects')} "
                f"live_words={d.get('live_metrics', {}).get('words')} "
                f"mint_words={d.get('mint_metrics', {}).get('words')}"
            )
    http_fails = report.get("http_failures", [])
    if http_fails:
        lines += ["", "## HTTP failures", ""]
        for h in http_fails[:80]:
            lines.append(f"- `{h.get('route')}` status={h.get('status')} {h.get('error', '')}")
    lines += ["", f"Full JSON: `{REPORT_JSON.relative_to(ROOT)}`", ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Production readiness audit vs live RTD")
    parser.add_argument("--concurrency", type=int, default=12)
    parser.add_argument("--skip-content", action="store_true")
    parser.add_argument("--skip-http", action="store_true")
    parser.add_argument("--http-limit", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--searchindex-file", help="Use local/cached searchindex.js")
    parser.add_argument("--skip-live-fetch", action="store_true", help="Only compare pages with local Sphinx HTML")
    args = parser.parse_args(argv)

    t0 = time.time()
    print(f"ROOT={ROOT}", flush=True)

    js = None
    source = None
    if args.searchindex_file:
        path = Path(args.searchindex_file)
        if not path.is_absolute():
            path = ROOT / path
        print(f"Loading searchindex from {path} …", flush=True)
        js = path.read_text(encoding="utf-8", errors="replace")
        source = str(path)
    else:
        print(f"Downloading {SEARCHINDEX_URL} …", flush=True)
        try:
            js = fetch(SEARCHINDEX_URL, timeout=90, retries=4)
            source = SEARCHINDEX_URL
            SEARCHINDEX_CACHE.write_text(js, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            print(f"  live searchindex failed: {exc}", flush=True)
            if SEARCHINDEX_CACHE.is_file() and SEARCHINDEX_CACHE.stat().st_size > 10000:
                print(f"  using cache {SEARCHINDEX_CACHE}", flush=True)
                js = SEARCHINDEX_CACHE.read_text(encoding="utf-8", errors="replace")
                source = str(SEARCHINDEX_CACHE)
            else:
                raise
    print(f"searchindex source: {source}", flush=True)
    docnames = parse_docnames(js)
    print(f"Live docnames (filtered): {len(docnames)}", flush=True)

    mapping: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for dn in docnames:
        mint, cands = resolve_mint_path(dn)
        row = {"live": dn, "mint": mint, "candidates": cands[:8]}
        mapping.append(row)
        if not mint:
            missing.append({"live": dn, "expected": cands[0] if cands else None, "candidates": cands[:8]})
    mint_mapped = sum(1 for m in mapping if m["mint"])
    print(f"Mapped: {mint_mapped}  Missing: {len(missing)}", flush=True)

    content_results: list[dict[str, Any]] = []
    content_defects: list[dict[str, Any]] = []
    fetch_errors: list[dict[str, Any]] = []
    defect_counts: Counter[str] = Counter()

    if not args.skip_content:
        jobs = [(m["live"], m["mint"]) for m in mapping]
        local_jobs, live_jobs = [], []
        for live, mint in jobs:
            live_html_path = f"{live}.html" if live != "index" else "index.html"
            if (LOCAL_HTML_ROOT / live_html_path).is_file():
                local_jobs.append((live, mint))
            else:
                live_jobs.append((live, mint))
        if args.skip_live_fetch:
            print(f"Skipping live fetch for {len(live_jobs)} pages without local HTML", flush=True)
            for live, mint in live_jobs:
                fetch_errors.append({"live": live, "mint": mint, "defects": ["fetch_error"], "error": "skipped (no local HTML)"})
                defect_counts["fetch_error"] += 1
            live_jobs = []
        print(
            f"Content comparison: local={len(local_jobs)} live_needed={len(live_jobs)} concurrency={args.concurrency}",
            flush=True,
        )

        def _ingest(res: dict[str, Any]) -> None:
            content_results.append(res)
            defs = list(res.get("defects") or [])
            if defs == ["missing"]:
                return
            if "fetch_error" in defs or "mint_error" in defs:
                fetch_errors.append(res)
                for d in defs:
                    defect_counts[d] += 1
                return
            defs = [d for d in defs if d != "missing"]
            if defs:
                content_defects.append(res)
                for d in defs:
                    defect_counts[d] += 1

        done = 0
        total = len(local_jobs) + len(live_jobs)
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futs = {ex.submit(content_job, live, mint): live for live, mint in local_jobs}
            for fut in as_completed(futs):
                done += 1
                if done % 50 == 0 or done == total:
                    print(f"  content {done}/{total}", flush=True)
                _ingest(fut.result())

        live_workers = max(1, min(2, args.concurrency // 4 or 1))
        if live_jobs:
            print(f"  fetching {len(live_jobs)} from live (workers={live_workers}) …", flush=True)
            with ThreadPoolExecutor(max_workers=live_workers) as ex:
                futs = {}
                for live, mint in live_jobs:
                    time.sleep(0.5)
                    futs[ex.submit(content_job, live, mint)] = live
                for fut in as_completed(futs):
                    done += 1
                    if done % 5 == 0 or done == total:
                        print(f"  content {done}/{total}", flush=True)
                    _ingest(fut.result())

    print("Scanning EN markdown for broken images/links …", flush=True)
    broken_imgs, broken_links = scan_broken_images_and_links()
    print(f"  broken images={len(broken_imgs)} broken links={len(broken_links)}", flush=True)

    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    nav_pages = collect_nav_pages(docs)
    nav_missing_files: list[str] = []
    for route in nav_pages:
        p = md_path_for_route(route)
        if not p.is_file() and not (ROOT / f"{route}.md").is_file() and not (ROOT / route / "Index.md").is_file():
            nav_missing_files.append(route)

    nav_set = set(nav_pages)
    nav_set |= {p + "/Index" for p in nav_pages}
    nav_set |= {p[: -len("/Index")] for p in nav_pages if p.endswith("/Index")}

    orphan_indexes: list[str] = []
    all_index_mds: list[str] = []
    for p in ROOT.rglob("Index.md"):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith(("de/", "scripts/", "docs/", "visual-regression/")):
            continue
        all_index_mds.append(rel)
        route = rel[:-3]
        if rel.count("/") == 1 and route not in nav_set and route.split("/")[0] not in nav_set:
            orphan_indexes.append(route)

    http_failures: list[dict[str, Any]] = []
    http_checked = 0
    if not args.skip_http:
        routes = pick_http_routes(
            nav_pages,
            [m["expected"] for m in missing if m.get("expected")],
            all_index_mds,
        )
        if args.http_limit and args.http_limit > 0:
            # keep tops + random sample
            tops = [r for r in routes if r.count("/") <= 1]
            rest = [r for r in routes if r not in tops]
            random.Random(args.seed).shuffle(rest)
            routes = tops + rest[: max(0, args.http_limit - len(tops))]
        print(f"HTTP smoke checking {len(routes)} routes against {MINT_BASE} …", flush=True)

        def http_job(route: str) -> dict[str, Any]:
            url = route_to_url(route)
            status, body = fetch_status(url, timeout=12, retries=2)
            ok = status == 200 and "Search.setIndex" not in body
            err = ""
            if status != 200:
                err = f"status {status}"
            elif "Search.setIndex" in body:
                err = "Search.setIndex present"
            return {"route": route, "url": url, "status": status, "ok": ok, "error": err}

        with ThreadPoolExecutor(max_workers=8) as ex:
            futs = [ex.submit(http_job, r) for r in routes]
            for i, fut in enumerate(as_completed(futs), 1):
                if i % 50 == 0 or i == len(futs):
                    print(f"  http {i}/{len(futs)}", flush=True)
                res = fut.result()
                http_checked += 1
                if not res["ok"]:
                    http_failures.append(res)

    qv = quick_verify()
    print("Quick verify:", json.dumps(qv), flush=True)

    hard_http = [h for h in http_failures if h.get("status") not in (0,)]
    soft_http = [h for h in http_failures if h.get("status") == 0]
    fail_reasons = []
    if missing:
        fail_reasons.append(f"missing={len(missing)}")
    if content_defects:
        fail_reasons.append(f"content_defects={len(content_defects)}")
    if hard_http:
        fail_reasons.append(f"http_fail={len(hard_http)}")
    elif soft_http and http_checked and len(soft_http) / max(http_checked, 1) > 0.05:
        fail_reasons.append(f"http_soft_fail={len(soft_http)}")
    if not qv.get("mintignore_excludes_docs") or not qv.get("mintignore_excludes_de"):
        fail_reasons.append("mintignore")
    if not qv.get("custom_css_responsive_hardening"):
        fail_reasons.append("custom.css")
    if qv.get("sample_has_Search_setIndex"):
        fail_reasons.append("Search.setIndex")
    if len(broken_imgs) > 25 or len(broken_links) > 50:
        fail_reasons.append("broken_assets")

    verdict = "FAIL" if fail_reasons else "PASS"
    report: dict[str, Any] = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "elapsed_sec": round(time.time() - t0, 1),
        "live_base": LIVE_BASE,
        "mint_base": MINT_BASE,
        "live_pages": len(docnames),
        "mint_mapped": mint_mapped,
        "missing_count": len(missing),
        "missing": missing,
        "content_defect_pages": len(content_defects),
        "fetch_error_pages": len(fetch_errors),
        "defect_counts_by_type": dict(defect_counts),
        "fetch_errors_sample": [{"live": x["live"], "error": x.get("error")} for x in fetch_errors[:50]],
        "content_defects": [
            {
                "live": d["live"],
                "mint": d.get("mint"),
                "defects": d.get("defects"),
                "live_metrics": d.get("live_metrics"),
                "mint_metrics": d.get("mint_metrics"),
                "error": d.get("error"),
            }
            for d in content_defects
        ],
        "broken_images_count": len(broken_imgs),
        "broken_links_count": len(broken_links),
        "broken_images_sample": broken_imgs[:100],
        "broken_links_sample": broken_links[:100],
        "http_checked": http_checked,
        "http_fail_count": len(http_failures),
        "http_hard_fail_count": len(hard_http),
        "http_soft_fail_count": len(soft_http),
        "http_failures": http_failures[:200],
        "nav_pages": len(nav_pages),
        "nav_missing_files_count": len(nav_missing_files),
        "nav_missing_files": nav_missing_files[:100],
        "orphan_index_count": len(orphan_indexes),
        "orphan_indexes": orphan_indexes[:100],
        "quick_verify": qv,
        "verdict": verdict,
        "fail_reasons": fail_reasons,
        "migrated": [],
    }
    write_reports(report)
    print(f"\nVerdict: {verdict} ({', '.join(fail_reasons) or 'ok'})", flush=True)
    print(f"Wrote {REPORT_JSON}", flush=True)
    print(f"Wrote {REPORT_MD}", flush=True)
    print(f"Elapsed {report['elapsed_sec']}s", flush=True)
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
