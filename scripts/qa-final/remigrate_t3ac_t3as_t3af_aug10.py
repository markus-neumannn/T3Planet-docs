#!/usr/bin/env python3
"""Compare + remigrate ExtNsT3AC / ExtNsT3AS / ExtNsT3AF vs live RTD (Aug 10, 2026).

Keeps Mintlify folder ExtNsT3AF (does not rename to T3AF).
Does not delete existing Mintlify content; creates missing pages and fills gaps.
"""
from __future__ import annotations

import json
import re
import shutil
import zlib
from copy import deepcopy
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup, NavigableString, Tag

_BASE = Path("/Users/nitsan/www/AI Agents")
ROOT = next(
    p
    for p in _BASE.iterdir()
    if (p / ".git").exists() and (p / "ExtNsT3AF").exists() and (p / "docs.json").exists()
)
LIVE_BASE = "https://docs.t3planet.de/en/latest/"
LOCAL_HTML = Path("/Users/nitsan/www/AI Agents/T3Planet Docs Agent/docs/docs/_build/html")
SPHINX_IMAGES = LOCAL_HTML / "_images"
PRODUCTS = ["ExtNsT3AC", "ExtNsT3AS", "ExtNsT3AF"]
UA = "Mozilla/5.0 (compatible; MintlifyRemigrateBot/1.0; +https://docs.t3planet.de)"
TIMEOUT = 45

OUT_JSON = ROOT / "scripts/qa-final/T3AC_T3AS_T3AF_REMIGRATE_AUG10.json"
OUT_MD = ROOT / "scripts/qa-final/T3AC_T3AS_T3AF_REMIGRATE_AUG10.md"

SUPADEMO_RE = re.compile(r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", re.I)
MD_IMG_RE = re.compile(
    r"!\[([^\]]*)\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']",
    re.I,
)
FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.M)

ADMONITION_TAGS = {
    "note": "Note",
    "tip": "Tip",
    "hint": "Tip",
    "important": "Info",
    "info": "Info",
    "seealso": "Info",
    "warning": "Warning",
    "caution": "Warning",
    "attention": "Warning",
    "danger": "Warning",
    "error": "Warning",
}

SKIP_IMG_PARTS = ("_static", "logo", "icon", "favicon", "badge", "sprites")


def fetch_bytes(url: str) -> bytes | None:
    try:
        req = Request(url, headers={"User-Agent": UA})
        with urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read()
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        print(f"  WARN fetch failed {url}: {exc}")
        return None


def load_objects_inv() -> str | None:
    raw = fetch_bytes(LIVE_BASE + "objects.inv")
    if not raw:
        return None
    rest = raw
    for _ in range(4):
        nl = rest.find(b"\n")
        if nl < 0:
            return None
        rest = rest[nl + 1 :]
    try:
        return zlib.decompress(rest).decode("utf-8")
    except Exception:
        return None


def live_docs_from_inv(inv: str, prefix: str) -> list[str]:
    docs: list[str] = []
    for line in inv.splitlines():
        parts = line.split()
        if len(parts) < 4 or parts[1] != "std:doc":
            continue
        name = parts[0]
        if not (name == prefix or name.startswith(prefix + "/")):
            continue
        uri = parts[3].split("#")[0]
        slug = uri[:-5] if uri.endswith(".html") else name
        docs.append(unquote(slug))
    return sorted(set(docs))


def live_docs_from_sphinx(prefix: str) -> list[str]:
    d = LOCAL_HTML / prefix
    out: list[str] = []
    if not d.is_dir():
        return out
    for h in d.rglob("*.html"):
        if h.name in {"genindex.html", "search.html", "py-modindex.html"}:
            continue
        rel = h.relative_to(LOCAL_HTML).as_posix()
        if rel.endswith(".html"):
            out.append(unquote(rel[:-5]))
    return sorted(set(out))


def mint_docs(prefix: str) -> list[str]:
    d = ROOT / prefix
    out: list[str] = []
    if not d.is_dir():
        return out
    for m in d.rglob("*.md"):
        rel = m.relative_to(ROOT).as_posix()
        out.append(rel[:-3] if rel.endswith(".md") else rel)
    return sorted(out)


def mint_path_for(slug: str) -> Path:
    slug = unquote(slug)
    parts = slug.strip("/").split("/")
    if parts[-1] == "Index":
        return ROOT.joinpath(*parts[:-1]) / "Index.md" if len(parts) > 1 else ROOT / "Index.md"
    # leaf like BuyNow / Support
    return ROOT.joinpath(*parts).with_suffix(".md")


def html_path_for(slug: str) -> Path | None:
    local = LOCAL_HTML / f"{slug}.html"
    if local.exists():
        return local
    # try encoded &
    alt = LOCAL_HTML / f"{slug.replace('&', '%26')}.html"
    if alt.exists():
        return alt
    return None


def get_html(slug: str, prefer_live: bool = False) -> tuple[str, str]:
    """Return (html, source). Prefer local Sphinx (stable); live on demand."""
    lp = html_path_for(slug)
    if lp and lp.exists() and not prefer_live:
        return lp.read_text(encoding="utf-8", errors="replace"), "local_sphinx"
    url = LIVE_BASE + slug.replace("&", "%26") + ".html"
    raw = fetch_bytes(url)
    if raw and len(raw) > 500 and b"Just a moment" not in raw[:2000]:
        return raw.decode("utf-8", "replace"), "live"
    if lp and lp.exists():
        return lp.read_text(encoding="utf-8", errors="replace"), "local_sphinx"
    raise FileNotFoundError(slug)


def clean_heading(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"\s*[¶]\s*", "", text)
    return re.sub(r"\s+", " ", text).strip()


def norm_heading(text: str) -> str:
    t = clean_heading(text).lower()
    t = t.replace("ai foundation", "t3af")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def content_root(soup: BeautifulSoup) -> Tag:
    rst = soup.select_one("div.rst-content")
    if rst:
        main = rst.select_one("div[role=main], article, div.document") or rst
        return main
    return soup.select_one("[role=main]") or soup.body or soup


def strip_junk(root: Tag) -> None:
    for sel in [
        "script",
        "style",
        "nav",
        ".headerlink",
        ".toctree-wrapper",
        ".contents",
        "#table-of-contents",
        ".sphinxsidebar",
        ".related",
        ".footer",
        "a.headerlink",
    ]:
        for el in root.select(sel):
            el.decompose()


def extract_live(html: str) -> dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    root = content_root(soup)
    strip_junk(root)
    text = root.get_text(" ", strip=True)
    headings = []
    for h in root.find_all(["h2", "h3"]):
        headings.append({"level": h.name, "text": clean_heading(h.get_text())})
    images = []
    for img in root.find_all("img"):
        src = img.get("src") or ""
        if any(p in src for p in SKIP_IMG_PARTS):
            continue
        name = Path(unquote(urlparse(src).path)).name
        if name:
            images.append(name)
    supademos = sorted(set(SUPADEMO_RE.findall(html)))
    return {
        "text_len": len(text),
        "headings": headings,
        "images": images,
        "supademo_ids": supademos,
    }


def extract_mint(md_path: Path) -> dict[str, Any]:
    raw = md_path.read_text(encoding="utf-8", errors="replace")
    body = FRONTMATTER_RE.sub("", raw, count=1)
    # visible-ish text: strip tags roughly
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"\s+", " ", text).strip()
    headings = []
    for m in HEADING_RE.finditer(body):
        headings.append({"level": "h2" if m.group(1) == "##" else "h3", "text": clean_heading(m.group(2))})
    imgs = set()
    for m in MD_IMG_RE.finditer(body):
        src = m.group(2) or m.group(3) or ""
        name = Path(unquote(src.split("?")[0])).name
        if name:
            imgs.add(name)
    disk = set()
    img_dir = md_path.parent / "images"
    if img_dir.is_dir():
        for f in img_dir.iterdir():
            if f.is_file():
                disk.add(f.name)
    return {
        "text_len": len(text),
        "headings": headings,
        "images": sorted(imgs),
        "disk_images": sorted(disk),
        "supademo_ids": sorted(set(SUPADEMO_RE.findall(raw))),
        "path": str(md_path.relative_to(ROOT)),
    }


def basename_variants(name: str) -> set[str]:
    stem = Path(name).stem
    return {name, stem + ".png", stem + ".webp", stem + ".jpg", stem + ".jpeg", stem + ".gif"}


def missing_images(live_names: list[str], mint: dict) -> list[str]:
    have = set()
    for n in mint.get("images", []) + mint.get("disk_images", []):
        have |= basename_variants(n)
    miss = []
    for n in live_names:
        if not (basename_variants(n) & have):
            miss.append(n)
    return miss


def missing_sections(live_h: list[dict], mint_h: list[dict]) -> list[str]:
    mint_n = {norm_heading(h["text"]) for h in mint_h}
    miss = []
    for h in live_h:
        n = norm_heading(h["text"])
        if not n:
            continue
        if n in mint_n:
            continue
        if any(n in m or m in n for m in mint_n if m):
            continue
        miss.append(h["text"])
    return miss


def make_supademo_block(demo_id: str, title: str = "Interactive demo") -> str:
    src = f"https://app.supademo.com/embed/{demo_id}?embed_v=2&utm_source=embed"
    title = title.replace('"', "'")
    return (
        f'\n<div className="t3-embed">'
        f'<iframe src="{src}" loading="lazy" title="{title}" '
        f'allow="clipboard-write" frameBorder="0" '
        f'webkitallowfullscreen="true" mozallowfullscreen="true" '
        f"allowfullscreen></iframe>"
        f"</div>\n"
    )


# ---- HTML → MD conversion (keep product path as ExtNs*) ----

def rewrite_href(href: str, page_live_rel: str) -> str:
    if not href or href.startswith(("mailto:", "javascript:", "#")):
        return href
    fragment = ""
    if "#" in href:
        href, fragment = href.split("#", 1)
        fragment = "#" + fragment
    if href.startswith("http") and "docs.t3planet.de" not in href:
        return href + fragment
    # map to mint path under ExtNs*
    abs_url = urljoin(f"{LIVE_BASE}{page_live_rel}.html", href)
    path = unquote(urlparse(abs_url).path)
    if "/latest/" in path:
        rel = path.split("/latest/", 1)[1]
    else:
        rel = href
    if rel.endswith(".html"):
        rel = rel[:-5]
    rel = unquote(rel)
    # keep ExtNsT3AF (do not map to T3AF)
    if not rel.startswith("/"):
        rel = "/" + rel
    # Index paths
    if rel.endswith("/Index") or rel.endswith("Index"):
        return rel + fragment
    return rel + fragment


def find_sphinx_image(basename: str) -> Path | None:
    if not SPHINX_IMAGES.is_dir():
        return None
    for cand in basename_variants(basename):
        p = SPHINX_IMAGES / cand
        if p.exists():
            return p
    # fuzzy stem
    stem = Path(basename).stem
    for p in SPHINX_IMAGES.glob(stem + ".*"):
        return p
    return None


def ensure_image(src: str, page_live_rel: str, mint_md: Path) -> str:
    name = Path(unquote(urlparse(src).path)).name
    if not name:
        return src
    img_dir = mint_md.parent / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    dest = img_dir / name
    if dest.exists() and dest.stat().st_size > 10:
        return f"images/{name}"
    # try webp sibling already there
    for v in basename_variants(name):
        alt = img_dir / v
        if alt.exists() and alt.stat().st_size > 10:
            return f"images/{v}"
    local = find_sphinx_image(name)
    if local:
        # prefer keeping original name; also copy webp if converting not required
        shutil.copy2(local, dest)
        return f"images/{name}"
    abs_url = urljoin(f"{LIVE_BASE}{page_live_rel}.html", src)
    raw = fetch_bytes(abs_url)
    if raw:
        dest.write_bytes(raw)
        return f"images/{name}"
    return abs_url


def inline_children(el: Tag, ctx: dict) -> str:
    return "".join(inline(c, ctx) for c in el.children)


def inline(node, ctx: dict) -> str:
    if isinstance(node, NavigableString):
        return str(node).replace("\xa0", " ")
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in {"script", "style", "svg"}:
        return ""
    if name == "br":
        return "\n"
    if name in {"strong", "b"}:
        return f"**{inline_children(node, ctx).strip()}**"
    if name in {"em", "i"}:
        return f"*{inline_children(node, ctx).strip()}*"
    if name in {"code", "kbd", "samp", "tt"}:
        return f"`{node.get_text()}`"
    if name == "a":
        classes = node.get("class") or []
        if "headerlink" in classes:
            return ""
        text = inline_children(node, ctx).strip()
        if "toc-backref" in classes:
            return text
        href = node.get("href") or ""
        if not text:
            text = href
        return f"[{text}]({rewrite_href(href, ctx['page_live_rel'])})"
    if name == "span":
        return inline_children(node, ctx)
    if name == "img":
        src = node.get("src") or ""
        if any(p in src for p in SKIP_IMG_PARTS):
            return ""
        alt = node.get("alt") or "image"
        local = ensure_image(src, ctx["page_live_rel"], ctx["mint_md"])
        return f"![{alt}]({local})"
    if name == "iframe":
        src = node.get("src") or ""
        m = SUPADEMO_RE.search(src)
        if m:
            return make_supademo_block(m.group(1), node.get("title") or "Interactive demo")
        return ""
    return inline_children(node, ctx)


def convert_list(el: Tag, ctx: dict, ordered: bool = False) -> str:
    lines: list[str] = []
    items = [c for c in el.children if isinstance(c, Tag) and c.name == "li"]
    for idx, li in enumerate(items, 1):
        prefix = f"{idx}. " if ordered else "- "
        parts: list[str] = []
        nested: list[str] = []
        for child in li.children:
            if isinstance(child, Tag) and child.name in {"ul", "ol"}:
                nested.append(convert_list(child, ctx, ordered=(child.name == "ol")))
            elif isinstance(child, Tag) and child.name == "p":
                parts.append(inline_children(child, ctx).strip())
            else:
                t = inline(child, ctx).strip()
                if t:
                    parts.append(t)
        text = " ".join(p for p in parts if p).strip()
        lines.append(f"{prefix}{text}")
        for n in nested:
            for nl in n.splitlines():
                lines.append(f"  {nl}")
    return "\n".join(lines)


def convert_table(table: Tag, ctx: dict) -> str:
    rows: list[list[str]] = []
    for tr in table.select("tr"):
        cells = tr.find_all(["th", "td"], recursive=False) or tr.find_all(["th", "td"])
        vals = [inline_children(c, ctx).replace("\n", " ").strip() for c in cells]
        rows.append(vals)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    has_th = bool(table.select("th"))
    if has_th:
        header, body = rows[0], rows[1:]
    else:
        header, body = [f"Col {i + 1}" for i in range(width)], rows
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * width) + " |",
    ]
    for r in body:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def convert_admonition(div: Tag, ctx: dict) -> str:
    classes = [c.lower() for c in (div.get("class") or [])]
    kind = "note"
    for c in classes:
        if c in ADMONITION_TAGS:
            kind = c
            break
    tag = ADMONITION_TAGS.get(kind, "Note")
    title = div.select_one(".admonition-title")
    if title:
        title.decompose()
    body_parts: list[str] = []
    for child in list(div.children):
        if isinstance(child, NavigableString):
            t = str(child).strip()
            if t:
                body_parts.append(t)
        elif isinstance(child, Tag):
            converted = convert_block(child, ctx)
            if converted:
                body_parts.append(converted)
    body = "\n\n".join(body_parts).strip()
    return f"<{tag}>\n{body}\n</{tag}>"


def convert_block(el: Tag, ctx: dict) -> str:
    name = el.name.lower()
    classes = el.get("class") or []
    if name in {"script", "style", "nav"}:
        return ""
    if "contents" in classes or "toctree-wrapper" in classes:
        links = []
        for a in el.select("a.reference"):
            href = rewrite_href(a.get("href") or "", ctx["page_live_rel"])
            text = a.get_text(strip=True)
            if text and href:
                links.append(f"- [{text}]({href})")
        return "\n".join(links)
    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(name[1])
        if level == 1:
            return ""
        level = min(level, 4)
        text = clean_heading(inline_children(el, ctx))
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text).strip()
        return f"{'#' * level} {text}"
    if name == "p":
        text = inline_children(el, ctx).strip()
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text
    if name == "pre" or (name == "div" and any(str(c).startswith("highlight") for c in classes)):
        pre = el if name == "pre" else el.select_one("pre")
        if pre is None:
            return ""
        lang = "text"
        for c in classes:
            cs = str(c)
            if cs.startswith("highlight-"):
                lang = cs.replace("highlight-", "").split()[0]
                break
        parent = el.find_parent("div", class_=re.compile(r"highlight"))
        if parent:
            for c in parent.get("class") or []:
                cs = str(c)
                if cs.startswith("highlight-"):
                    lang = cs.replace("highlight-", "").split()[0]
        if lang in {"default", "none", "notranslate"}:
            lang = "text"
        if lang == "console":
            lang = "bash"
        return f"```{lang}\n{pre.get_text().rstrip()}\n```"
    if name == "ul":
        return convert_list(el, ctx, ordered=False)
    if name == "ol":
        return convert_list(el, ctx, ordered=True)
    if name == "table" or (name == "div" and "table-wrapper" in classes):
        table = el if name == "table" else el.select_one("table")
        return convert_table(table, ctx) if table else ""
    if name == "div" and "admonition" in classes:
        return convert_admonition(el, ctx)
    if name == "blockquote":
        text = inline_children(el, ctx).strip()
        return "\n".join(f"> {ln}" if ln else ">" for ln in text.splitlines())
    if name == "hr":
        return "---"
    if name == "dl":
        lines: list[str] = []
        for child in el.children:
            if not isinstance(child, Tag):
                continue
            if child.name == "dt":
                lines.append(f"**{inline_children(child, ctx).strip()}**")
            elif child.name == "dd":
                dd_parts: list[str] = []
                for gc in child.children:
                    if isinstance(gc, Tag):
                        c = convert_block(gc, ctx)
                        if c:
                            dd_parts.append(c)
                    elif isinstance(gc, NavigableString) and str(gc).strip():
                        dd_parts.append(str(gc).strip())
                lines.append("\n\n".join(dd_parts) if dd_parts else inline_children(child, ctx).strip())
                lines.append("")
        return "\n".join(lines).strip()
    if name in {"section", "div", "article", "main"}:
        parts: list[str] = []
        for child in el.children:
            if isinstance(child, Tag):
                c = convert_block(child, ctx)
                if c:
                    parts.append(c)
            elif isinstance(child, NavigableString) and str(child).strip():
                parts.append(str(child).strip())
        return "\n\n".join(parts)
    return inline_children(el, ctx).strip()


def html_to_md_body(html: str, page_live_rel: str, mint_md: Path) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.title.string if soup.title else ""
    page_title = (
        clean_heading(title_tag.split("—")[0].split("–")[0].strip()) if title_tag else Path(page_live_rel).parent.name
    )
    root = content_root(soup)
    strip_junk(root)
    # also drop breadcrumbs / prev-next
    for sel in [".wy-breadcrumbs", ".rst-footer-buttons", "#furo-main-content .related"]:
        for el in soup.select(sel):
            el.decompose()
    ctx = {"page_live_rel": page_live_rel, "mint_md": mint_md}
    parts: list[str] = []
    for child in root.children:
        if isinstance(child, Tag):
            c = convert_block(child, ctx)
            if c:
                parts.append(c)
    body = "\n\n".join(parts)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"
    # ensure iframes from raw html not lost
    for m in SUPADEMO_RE.finditer(html):
        demo_id = m.group(1)
        if demo_id not in body:
            body += make_supademo_block(demo_id)
    return page_title, body


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def frontmatter(title: str, product: str) -> str:
    desc = f"Documentation for {title} ({product})."
    return (
        "---\n"
        f'title: "{yaml_escape(title)}"\n'
        f'description: "{yaml_escape(desc)}"\n'
        "keywords:\n"
        '  - "TYPO3"\n'
        '  - "T3Planet"\n'
        f'  - "{product}"\n'
        f'sidebarTitle: "{yaml_escape(title[:40])}"\n'
        "---\n\n"
    )


def create_page_from_live(slug: str) -> Path:
    mint_md = mint_path_for(slug)
    mint_md.parent.mkdir(parents=True, exist_ok=True)
    html, _src = get_html(slug)
    title, body = html_to_md_body(html, slug, mint_md)
    product = slug.split("/")[0]
    mint_md.write_text(frontmatter(title, product) + body, encoding="utf-8")
    return mint_md


def insert_after_heading(md: str, heading: str, block: str) -> tuple[str, bool]:
    # find ##/### heading fuzzy
    target = norm_heading(heading)
    lines = md.splitlines(keepends=True)
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,3})\s+(.+?)\s*$", line.rstrip("\n"))
        if not m:
            continue
        if norm_heading(m.group(2)) == target or target in norm_heading(m.group(2)):
            # insert after this heading line
            j = i + 1
            lines.insert(j, block if block.endswith("\n") else block + "\n")
            return "".join(lines), True
    return md, False


def extract_section_md(html: str, heading_text: str, page_live_rel: str, mint_md: Path) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    root = content_root(soup)
    strip_junk(root)
    target = norm_heading(heading_text)
    ctx = {"page_live_rel": page_live_rel, "mint_md": mint_md}
    for h in root.find_all(["h2", "h3"]):
        if norm_heading(h.get_text()) != target and target not in norm_heading(h.get_text()):
            continue
        level = int(h.name[1])
        parts = [convert_block(h, ctx)]
        for sib in h.next_siblings:
            if isinstance(sib, Tag) and sib.name and re.match(r"h[1-6]", sib.name or ""):
                sib_level = int(sib.name[1])
                if sib_level <= level:
                    break
            if isinstance(sib, Tag):
                c = convert_block(sib, ctx)
                if c:
                    parts.append(c)
        return "\n\n".join(parts).strip()
    return None


def append_missing_sections(slug: str, miss_secs: list[str], mint_md: Path, html: str) -> list[str]:
    added = []
    raw = mint_md.read_text(encoding="utf-8")
    chunks: list[str] = []
    for sec in miss_secs:
        # skip if already present after fuzzy
        if norm_heading(sec) in {norm_heading(m.group(2)) for m in HEADING_RE.finditer(raw)}:
            continue
        chunk = extract_section_md(html, sec, slug, mint_md)
        if chunk and len(chunk) > 40:
            chunks.append(chunk)
            added.append(sec)
    if chunks:
        addition = "\n\n---\n\n## Additional content from live docs\n\n" + "\n\n".join(chunks) + "\n"
        # avoid duplicate append marker spam
        if "## Additional content from live docs" in raw:
            # append only new chunks under existing marker
            mint_md.write_text(raw.rstrip() + "\n\n" + "\n\n".join(chunks) + "\n", encoding="utf-8")
        else:
            mint_md.write_text(raw.rstrip() + addition, encoding="utf-8")
    return added


def sync_supademos(slug: str, live_ids: list[str], mint_md: Path, html: str) -> list[str]:
    raw = mint_md.read_text(encoding="utf-8")
    have = set(SUPADEMO_RE.findall(raw))
    missing = [i for i in live_ids if i not in have]
    if not missing:
        return []
    soup = BeautifulSoup(html, "html.parser")
    root = content_root(soup)
    # map id -> nearest preceding heading
    id_heading: dict[str, str] = {}
    for iframe in root.find_all("iframe"):
        src = iframe.get("src") or ""
        m = SUPADEMO_RE.search(src)
        if not m:
            continue
        demo_id = m.group(1)
        heading = "Interactive demos"
        for prev in iframe.find_all_previous(["h2", "h3"]):
            heading = clean_heading(prev.get_text())
            break
        id_heading[demo_id] = heading
    # also raw regex near context
    for demo_id in missing:
        block = make_supademo_block(demo_id)
        heading = id_heading.get(demo_id, "")
        if heading:
            raw2, ok = insert_after_heading(raw, heading, block)
            if ok:
                raw = raw2
                continue
        if "## Interactive demos" in raw:
            raw = raw.replace("## Interactive demos", "## Interactive demos" + block, 1)
        else:
            raw = raw.rstrip() + "\n\n## Interactive demos\n" + block
    mint_md.write_text(raw, encoding="utf-8")
    return missing


def sync_images(slug: str, live_names: list[str], mint_md: Path, html: str) -> list[str]:
    mint = extract_mint(mint_md)
    miss = missing_images(live_names, mint)
    if not miss:
        return []
    soup = BeautifulSoup(html, "html.parser")
    root = content_root(soup)
    added = []
    raw = mint_md.read_text(encoding="utf-8")
    for img in root.find_all("img"):
        src = img.get("src") or ""
        name = Path(unquote(urlparse(src).path)).name
        if name not in miss:
            continue
        if any(p in src for p in SKIP_IMG_PARTS):
            continue
        local = ensure_image(src, slug, mint_md)
        alt = img.get("alt") or Path(name).stem.replace("_", " ")
        # find heading
        heading = ""
        for prev in img.find_all_previous(["h2", "h3"]):
            heading = clean_heading(prev.get_text())
            break
        md_img = f"\n![{alt}]({local})\n"
        if local in raw or name in raw:
            added.append(name)
            continue
        if heading:
            raw2, ok = insert_after_heading(raw, heading, md_img)
            if ok:
                raw = raw2
                added.append(name)
                continue
        raw = raw.rstrip() + "\n\n## Figures\n" + md_img
        added.append(name)
    mint_md.write_text(raw, encoding="utf-8")
    return added


def add_nav_pages(slugs: list[str]) -> list[str]:
    """Insert missing slugs into docs.json under matching product groups."""
    docs_path = ROOT / "docs.json"
    data = json.loads(docs_path.read_text(encoding="utf-8"))
    added: list[str] = []

    def flatten_pages(pages: list) -> list[str]:
        out: list[str] = []
        for p in pages:
            if isinstance(p, str):
                out.append(p)
            elif isinstance(p, dict) and "pages" in p:
                out.extend(flatten_pages(p["pages"]))
        return out

    def insert_into_group(obj: Any, product: str, slug: str) -> bool:
        if isinstance(obj, dict):
            pages = obj.get("pages")
            if isinstance(pages, list):
                flat = flatten_pages(pages)
                if any(p.startswith(product + "/") or p == product + "/Index" for p in flat):
                    # prefer nested group with matching prefix
                    # insert near related parent
                    parent = "/".join(slug.split("/")[:2])
                    # already present?
                    if slug in flat:
                        return True
                    # try insert into deepest matching subgroup
                    def try_insert(ps: list) -> bool:
                        for i, item in enumerate(ps):
                            if isinstance(item, dict) and "pages" in item:
                                if try_insert(item["pages"]):
                                    return True
                        # insert into this list if any sibling shares prefix
                        sibs = [x for x in ps if isinstance(x, str)]
                        if any(s.startswith(parent) for s in sibs) or (
                            product in "".join(sibs) and len(slug.split("/")) <= 3
                        ):
                            # place after last sibling with same first 2 segments
                            insert_at = len(ps)
                            for i, s in enumerate(ps):
                                if isinstance(s, str) and s.startswith(parent):
                                    insert_at = i + 1
                            if slug not in ps:
                                ps.insert(insert_at, slug)
                                return True
                        return False

                    if try_insert(pages):
                        return True
                    # fallback append to this group's pages
                    pages.append(slug)
                    return True
            for v in obj.values():
                if insert_into_group(v, product, slug):
                    return True
        elif isinstance(obj, list):
            for v in obj:
                if insert_into_group(v, product, slug):
                    return True
        return False

    for slug in slugs:
        product = slug.split("/")[0]
        # special: put credit system under T3AF group
        if insert_into_group(data, product, slug):
            added.append(slug)
        else:
            print(f"  WARN could not place nav for {slug}")

    docs_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added


def audit_product(product: str, inv: str | None) -> dict[str, Any]:
    live = live_docs_from_inv(inv, product) if inv else live_docs_from_sphinx(product)
    if not live:
        live = live_docs_from_sphinx(product)
    mint = mint_docs(product)
    mint_set = set(mint)
    missing_pages = [p for p in live if p not in mint_set]
    extra_pages = [p for p in mint if p not in set(live)]
    page_reports = []
    counts = {
        "missing_page": len(missing_pages),
        "missing_supademo": 0,
        "missing_images": 0,
        "missing_sections": 0,
        "thin": 0,
    }
    for slug in live:
        if slug in missing_pages:
            page_reports.append({"live": slug, "status": "MISSING_PAGE"})
            continue
        md = mint_path_for(slug)
        try:
            html, src = get_html(slug)
        except FileNotFoundError:
            page_reports.append({"live": slug, "status": "NO_HTML"})
            continue
        live_ex = extract_live(html)
        mint_ex = extract_mint(md)
        miss_s = [i for i in live_ex["supademo_ids"] if i not in mint_ex["supademo_ids"]]
        miss_i = missing_images(live_ex["images"], mint_ex)
        miss_sec = missing_sections(live_ex["headings"], mint_ex["headings"])
        ratio = (mint_ex["text_len"] / live_ex["text_len"]) if live_ex["text_len"] else 1.0
        thin = ratio < 0.45 and live_ex["text_len"] > 600
        # Index landing pages: HTML-heavy mint — skip thin if file size healthy
        if slug.endswith("/Index") and slug.count("/") == 1:
            if md.stat().st_size > 2500:
                thin = False
        counts["missing_supademo"] += len(miss_s)
        counts["missing_images"] += len(miss_i)
        counts["missing_sections"] += len(miss_sec)
        if thin:
            counts["thin"] += 1
        page_reports.append(
            {
                "live": slug,
                "status": "ok",
                "html_source": src,
                "ratio": round(ratio, 3),
                "thin": thin,
                "missing_supademo": miss_s,
                "missing_images": miss_i,
                "missing_sections": miss_sec,
                "live_len": live_ex["text_len"],
                "mint_len": mint_ex["text_len"],
            }
        )
    return {
        "live_count": len(live),
        "mint_count": len(mint),
        "missing_pages": missing_pages,
        "extra_pages": extra_pages,
        "counts": counts,
        "pages": page_reports,
    }


def remigrate(before: dict[str, Any]) -> dict[str, Any]:
    actions = {
        "pages_created": [],
        "pages_updated": [],
        "supademos_added": {},
        "images_added": {},
        "sections_added": {},
        "nav_added": [],
        "files_modified": [],
    }
    created_slugs: list[str] = []

    for product, pdata in before["products"].items():
        for slug in pdata["missing_pages"]:
            print(f"CREATE {slug}")
            path = create_page_from_live(slug)
            actions["pages_created"].append(slug)
            actions["files_modified"].append(str(path.relative_to(ROOT)))
            created_slugs.append(slug)

        for pref in pdata["pages"]:
            if pref.get("status") != "ok":
                continue
            slug = pref["live"]
            md = mint_path_for(slug)
            need = (
                pref.get("missing_supademo")
                or pref.get("missing_images")
                or pref.get("missing_sections")
                or pref.get("thin")
            )
            if not need:
                continue
            html, _ = get_html(slug)
            changed = False
            if pref.get("missing_supademo"):
                added = sync_supademos(slug, pref["missing_supademo"], md, html)
                if added:
                    actions["supademos_added"][slug] = added
                    changed = True
            if pref.get("missing_images"):
                added = sync_images(slug, pref["missing_images"], md, html)
                if added:
                    actions["images_added"][slug] = added
                    changed = True
            if pref.get("missing_sections") or pref.get("thin"):
                # For thin pages without section list, pull all live h2 not in mint
                live_ex = extract_live(html)
                mint_ex = extract_mint(md)
                miss = pref.get("missing_sections") or missing_sections(
                    live_ex["headings"], mint_ex["headings"]
                )
                if miss:
                    print(f"FILL sections {slug}: {len(miss)}")
                    added = append_missing_sections(slug, miss, md, html)
                    if added:
                        actions["sections_added"][slug] = added
                        changed = True
                elif pref.get("thin"):
                    # append full body under a marker without wiping landing
                    title, body = html_to_md_body(html, slug, md)
                    raw = md.read_text(encoding="utf-8")
                    if "## Full documentation content" not in raw and len(body) > 400:
                        md.write_text(
                            raw.rstrip()
                            + "\n\n---\n\n## Full documentation content\n\n"
                            + body,
                            encoding="utf-8",
                        )
                        actions["sections_added"][slug] = ["(full live body appended)"]
                        changed = True
            if changed:
                actions["pages_updated"].append(slug)
                rel = str(md.relative_to(ROOT))
                if rel not in actions["files_modified"]:
                    actions["files_modified"].append(rel)

    if created_slugs:
        actions["nav_added"] = add_nav_pages(created_slugs)
        if "docs.json" not in actions["files_modified"]:
            actions["files_modified"].append("docs.json")

    return actions


def main() -> None:
    print("ROOT", ROOT)
    inv = load_objects_inv()
    print("objects.inv", "ok" if inv else "fallback-sphinx")

    before = {"products": {}}
    for product in PRODUCTS:
        print(f"\n=== AUDIT BEFORE {product} ===")
        before["products"][product] = audit_product(product, inv)
        c = before["products"][product]["counts"]
        print(
            "missing_page",
            c["missing_page"],
            "supademo",
            c["missing_supademo"],
            "images",
            c["missing_images"],
            "sections",
            c["missing_sections"],
            "thin",
            c["thin"],
        )
        for p in before["products"][product]["missing_pages"]:
            print("  MISSING_PAGE", p)

    print("\n=== REMIGRATE ===")
    actions = remigrate(before)

    after = {"products": {}}
    for product in PRODUCTS:
        print(f"\n=== AUDIT AFTER {product} ===")
        after["products"][product] = audit_product(product, inv)
        c = after["products"][product]["counts"]
        print(
            "missing_page",
            c["missing_page"],
            "supademo",
            c["missing_supademo"],
            "images",
            c["missing_images"],
            "sections",
            c["missing_sections"],
            "thin",
            c["thin"],
        )

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "live_base": LIVE_BASE,
        "local_sphinx": str(LOCAL_HTML),
        "before": before,
        "after": after,
        "actions": actions,
        "summary": {},
    }
    for product in PRODUCTS:
        b = before["products"][product]["counts"]
        a = after["products"][product]["counts"]
        report["summary"][product] = {
            "missing_page": f"{b['missing_page']}→{a['missing_page']}",
            "missing_supademo": f"{b['missing_supademo']}→{a['missing_supademo']}",
            "missing_images": f"{b['missing_images']}→{a['missing_images']}",
            "missing_sections": f"{b['missing_sections']}→{a['missing_sections']}",
            "thin": f"{b['thin']}→{a['thin']}",
            "extra_pages_before": len(before["products"][product]["extra_pages"]),
            "extra_pages_after": len(after["products"][product]["extra_pages"]),
        }

    OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# T3AC / T3AS / T3AF remigrate — Aug 10, 2026",
        "",
        f"Repo: `{ROOT}`",
        f"Live: {LIVE_BASE}",
        f"Sphinx fallback: `{LOCAL_HTML}`",
        "",
        "## Summary (before → after)",
        "",
    ]
    for product, s in report["summary"].items():
        lines.append(f"### {product}")
        lines.append(f"- missing_page: **{s['missing_page']}**")
        lines.append(f"- missing_supademo: **{s['missing_supademo']}**")
        lines.append(f"- missing_images: **{s['missing_images']}**")
        lines.append(f"- missing_sections: **{s['missing_sections']}**")
        lines.append(f"- thin: **{s['thin']}**")
        lines.append("")
    lines.append("## Actions")
    lines.append(f"- pages_created: {len(actions['pages_created'])}")
    for p in actions["pages_created"]:
        lines.append(f"  - `{p}`")
    lines.append(f"- pages_updated: {len(actions['pages_updated'])}")
    for p in actions["pages_updated"]:
        lines.append(f"  - `{p}`")
    lines.append(f"- nav_added: {actions['nav_added']}")
    lines.append("")
    lines.append("## Files modified")
    for f in actions["files_modified"]:
        lines.append(f"- `{f}`")
    lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\nWrote", OUT_JSON)
    print("Wrote", OUT_MD)


if __name__ == "__main__":
    main()
