#!/usr/bin/env python3
"""Fetch Sphinx RST HTML from docs.t3planet.de and convert to Mintlify MDX.

Usage:
  python3 scripts/migrate_from_live.py ExtNsT3AF/Installation/Index.html ExtNsT3AF/Installation/Index.md
  python3 scripts/migrate_from_live.py --merge ExtNsT3AF/Installation/Index
  python3 scripts/migrate_from_live.py --batch scripts/migration-batch-ai.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
LIVE_BASE = "https://docs.t3planet.de/en/latest/"
USER_AGENT = "MintlifyDoc-Migrator/2.0"

# Product root remaps (live folder → mint folder). Canonical mint paths use ExtNsT3AF.
PRODUCT_ROOT_MAP: dict[str, str] = {}

# Live-only alias folders that map to canonical mint roots
LIVE_ROOT_ALIASES = {
    "T3AF": "ExtNsT3AF",
}

# Leaf pages that become GetThisExtension/Index under ExtNsT3AF
BUYNOW_ALIASES = {"BuyNow", "buynow"}

# Path segment remaps applied inside product trees
SEGMENT_MAP = {
    "AIPermissions": "GovernanceAndAccess",
    "QuickSetup": "SetupWizard",
}

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

PROTECTED_TAGS = {
    "Note",
    "Warning",
    "Tip",
    "Info",
    "Check",
    "Card",
    "CardGroup",
    "Accordion",
    "AccordionGroup",
    "Tabs",
    "Tab",
    "Steps",
    "Step",
    "CodeGroup",
    "Frame",
    "Tooltip",
    "Icon",
    "Mermaid",
    "div",
    "iframe",
    "span",
    "a",
    "img",
    "br",
    "hr",
    "table",
    "thead",
    "tbody",
    "tr",
    "td",
    "th",
    "ul",
    "ol",
    "li",
    "p",
    "strong",
    "em",
    "b",
    "i",
    "code",
    "pre",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
}

PRODUCT_KEYWORDS = {
    "ExtNsT3AF": "AI Foundation",
    "ExtNsT3AI": "T3AI",
    "ExtNsT3AC": "T3AC",
    "ExtNsT3AS": "T3AS",
    "ExtNsT3AA": "T3AA",
}


def normalize_live_rel(live: str) -> str:
    """Normalize a live path relative to /en/latest/ (no leading slash)."""
    live = live.strip()
    live = re.sub(r"^https?://docs\.t3planet\.de/(?:[a-z]{2}/)?latest/", "", live)
    live = live.lstrip("/")
    live = unquote(live)
    if live.endswith(".html"):
        live = live[:-5]
    parts = [p for p in live.split("/") if p and p != "."]
    if parts and parts[0] in LIVE_ROOT_ALIASES:
        parts[0] = LIVE_ROOT_ALIASES[parts[0]]
    return "/".join(parts)


def map_segment(seg: str, mint_root: str) -> str:
    if seg in BUYNOW_ALIASES and mint_root == "ExtNsT3AF":
        return "GetThisExtension"
    return SEGMENT_MAP.get(seg, seg)


def live_product(live_rel: str) -> str:
    return normalize_live_rel(live_rel).split("/", 1)[0]


def mint_root_for(product: str) -> str:
    return PRODUCT_ROOT_MAP.get(product, product)


def live_to_mint_path(live_rel: str) -> str:
    """Convert live HTML path to mint .md path."""
    live_rel = normalize_live_rel(live_rel)
    if live_rel.endswith(".html"):
        live_rel = live_rel[:-5]
    parts = [p for p in live_rel.split("/") if p and p != "."]
    if not parts:
        raise ValueError(f"Empty live path: {live_rel}")
    product = parts[0]
    mint_root = mint_root_for(product)
    rest = [map_segment(p, mint_root) for p in parts[1:]]

    if not rest:
        return f"{mint_root}/Index.md"

    last = rest[-1]
    # Flat leaf pages (BuyNow.html / Support.html)
    if len(rest) == 1 and last != "Index":
        if mint_root == "ExtNsT3AF":
            if last == "GetThisExtension":
                return f"{mint_root}/GetThisExtension/Index.md"
            if last == "Support":
                return f"{mint_root}/Support/Index.md"
            return f"{mint_root}/{last}/Index.md"
        return f"{mint_root}/{last}.md"

    if last == "Index":
        return f"{mint_root}/{'/'.join(rest)}.md"

    return f"{mint_root}/{'/'.join(rest)}/Index.md"


def mint_href_from_live_path(live_rel: str, fragment: str = "") -> str:
    md = live_to_mint_path(live_rel)
    slug = md[:-3] if md.endswith(".md") else md
    frag = f"#{fragment}" if fragment else ""
    return f"/{slug}{frag}"


def fetch_html(live_rel: str) -> str:
    live_rel = normalize_live_rel(live_rel)
    if not live_rel.endswith(".html"):
        live_rel = f"{live_rel}.html" if not live_rel.endswith("/") else f"{live_rel}Index.html"
    url = urljoin(LIVE_BASE, live_rel)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read().decode("utf-8", errors="replace")


def clean_heading(text: str) -> str:
    return (
        text.replace("\uf0c1", "")
        .replace("¶", "")
        .replace("\u00a0", " ")
        .strip()
    )


def rewrite_href(href: str, page_live_rel: str) -> str:
    if not href or href.startswith(("#", "mailto:", "javascript:", "data:")):
        return href

    page_live_rel = normalize_live_rel(page_live_rel)
    if not page_live_rel.endswith(".html"):
        page_live_rel = f"{page_live_rel}.html"

    fragment = ""
    if "#" in href:
        href, fragment = href.split("#", 1)

    # Absolute docs.t3planet.de links
    m = re.match(
        r"https?://docs\.t3planet\.de/(?:[a-z]{2}/)?latest/(.+)$",
        href,
        flags=re.I,
    )
    if m:
        rel = unquote(m.group(1))
        if rel.endswith(".html") or "/Ext" in rel or rel.startswith("License/") or rel.startswith("EXT"):
            try:
                return mint_href_from_live_path(rel, fragment)
            except ValueError:
                return href if not fragment else f"{href}#{fragment}"
        return href if not fragment else f"{href}#{fragment}"

    if href.startswith("http://") or href.startswith("https://"):
        return href if not fragment else f"{href}#{fragment}"

    # Relative link resolved against the live page URL
    abs_url = urljoin(f"{LIVE_BASE}{page_live_rel}", href)
    parsed = urlparse(abs_url)
    path = unquote(parsed.path)
    frag = fragment or parsed.fragment

    marker = "/latest/"
    if marker in path:
        rel = path.split(marker, 1)[1]
    else:
        # Fallback: join relative to page dir
        rel = str((Path(page_live_rel).parent / href).as_posix())
        while "/../" in rel:
            rel = re.sub(r"[^/]+/\.\./", "", rel)
        rel = rel.lstrip("./")

    if not rel.endswith(".html") and not rel.endswith("/"):
        # May already be directory-ish; leave external-ish anchors alone
        if "." in Path(rel).name and not rel.endswith(".html"):
            return href if not frag else f"{href}#{frag}"

    try:
        return mint_href_from_live_path(rel, frag)
    except ValueError:
        return href if not frag else f"{href}#{frag}"


def download_image(src: str, page_live_rel: str, mint_md: Path) -> str:
    if not src:
        return src
    page_live_rel = normalize_live_rel(page_live_rel)
    if not page_live_rel.endswith(".html"):
        page_live_rel = f"{page_live_rel}.html"
    abs_url = urljoin(f"{LIVE_BASE}{page_live_rel}", src)
    name = Path(urlparse(unquote(abs_url)).path).name
    if not name:
        return abs_url
    img_dir = mint_md.parent / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    dest = img_dir / name
    if not dest.exists() or dest.stat().st_size < 10:
        try:
            req = urllib.request.Request(abs_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=90) as resp:
                dest.write_bytes(resp.read())
        except Exception as exc:  # noqa: BLE001
            print(f"  WARN image download failed: {abs_url} ({exc})")
            return abs_url
    return f"./images/{name}"


def inline_children(el: Tag, ctx: dict) -> str:
    return "".join(inline(child, ctx) for child in el.children)


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
    if name == "code":
        return f"`{node.get_text()}`"
    if name in {"kbd", "samp", "tt"}:
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
        new_href = rewrite_href(href, ctx["page_live_rel"])
        return f"[{text}]({new_href})"
    if name == "span":
        classes = node.get("class") or []
        joined = " ".join(classes)
        if "pre" in classes or "literal" in joined:
            return f"`{node.get_text()}`"
        return inline_children(node, ctx)
    if name == "img":
        src = node.get("src") or ""
        alt = node.get("alt") or "image"
        local = download_image(src, ctx["page_live_rel"], ctx["mint_md"])
        return f"![{alt}]({local})"
    return inline_children(node, ctx)


def pre_text(pre: Tag) -> str:
    return pre.get_text()


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
            return ""  # frontmatter title
        level = min(level, 4)
        text = clean_heading(inline_children(el, ctx))
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text).strip()
        return f"{'#' * level} {text}"

    if name == "p":
        text = inline_children(el, ctx).strip()
        text = re.sub(r"[ \t]+\n", "\n", text)
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
        code = pre_text(pre).rstrip("\n")
        return f"```{lang}\n{code}\n```"

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
                # Prefer block conversion for nested content
                dd_parts: list[str] = []
                for gc in child.children:
                    if isinstance(gc, Tag):
                        c = convert_block(gc, ctx)
                        if c:
                            dd_parts.append(c)
                    elif isinstance(gc, NavigableString) and str(gc).strip():
                        dd_parts.append(str(gc).strip())
                if dd_parts:
                    lines.append("\n\n".join(dd_parts))
                else:
                    lines.append(inline_children(child, ctx).strip())
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


def html_to_mdx(html: str, page_live_rel: str, mint_md: Path) -> tuple[str, str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.title.string if soup.title else ""
    page_title = (
        clean_heading(title_tag.split("—")[0].split("–")[0].strip()) if title_tag else ""
    )

    meta_desc = ""
    desc_el = soup.select_one('meta[name="description"]')
    if desc_el and desc_el.get("content"):
        meta_desc = desc_el["content"].strip()

    rst = soup.select_one("div.rst-content")
    if rst is None:
        rst = soup.select_one("[role=main]") or soup.select_one(".document") or soup.body
    if rst is None:
        raise RuntimeError("No content root found in HTML")

    for junk in rst.select(
        ".headerlink, .sphinxsidebar, script, style, .related, .wy-breadcrumbs, "
        ".rst-breadcrumbs-buttons, footer, .contentfooter"
    ):
        junk.decompose()

    body_root = rst.select_one("[itemprop=articleBody]") or rst.select_one("article") or rst

    ctx = {"page_live_rel": page_live_rel, "mint_md": mint_md}
    parts: list[str] = []
    for child in body_root.children:
        if isinstance(child, Tag):
            converted = convert_block(child, ctx)
            if converted:
                parts.append(converted)

    body = "\n\n".join(parts)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    h1 = body_root.select_one("h1")
    if h1:
        page_title = clean_heading(h1.get_text())
    if not page_title or page_title.lower() in {"<no title>", "no title"}:
        page_title = mint_md.parent.name if mint_md.name == "Index.md" else mint_md.stem

    if not meta_desc:
        # First non-empty paragraph as description (truncated)
        for para in body.split("\n\n"):
            plain = re.sub(r"[*`_\[\]()#>!-]", "", para).strip()
            plain = re.sub(r"\s+", " ", plain)
            if len(plain) > 40 and not plain.startswith("<"):
                meta_desc = plain[:180].rstrip(" ,;")
                if len(plain) > 180:
                    meta_desc = meta_desc.rsplit(" ", 1)[0] + "…"
                break
    if not meta_desc:
        meta_desc = f"{page_title} documentation."

    return page_title, meta_desc, body


def escape_mdx(body: str) -> str:
    """Escape MDX-sensitive tokens outside fenced code and protected tags."""
    parts: list[str] = []
    # Split on fenced code blocks
    chunks = re.split(r"(```[\s\S]*?```)", body)
    for i, chunk in enumerate(chunks):
        if i % 2 == 1:
            parts.append(chunk)
            continue
        # Protect JSX/HTML tags we intentionally emit
        placeholders: list[str] = []

        def stash(m: re.Match[str]) -> str:
            placeholders.append(m.group(0))
            return f"\x00TAG{len(placeholders) - 1}\x00"

        tag_pattern = (
            r"</?(?:"
            + "|".join(re.escape(t) for t in sorted(PROTECTED_TAGS, key=len, reverse=True))
            + r")\b[^>]*>"
        )
        protected = re.sub(tag_pattern, stash, chunk, flags=re.I)

        # Escape bare <?php
        protected = protected.replace("<?php", "`<?php`")

        # Escape bare <Placeholder> style tokens (not already stashed)
        def escape_angle(m: re.Match[str]) -> str:
            inner = m.group(1)
            if inner in PROTECTED_TAGS or inner.lower() in {t.lower() for t in PROTECTED_TAGS}:
                return m.group(0)
            # Already code-like or closing
            return f"`<{inner}>`"

        protected = re.sub(r"<([A-Za-z][A-Za-z0-9._:-]*)>", escape_angle, protected)

        # Escape { } outside inline code
        sub_parts: list[str] = []
        for j, sub in enumerate(re.split(r"(`[^`]*`)", protected)):
            if j % 2 == 1:
                sub_parts.append(sub)
            else:
                sub_parts.append(sub.replace("{", "&#123;").replace("}", "&#125;"))
        protected = "".join(sub_parts)

        for idx, tag in enumerate(placeholders):
            protected = protected.replace(f"\x00TAG{idx}\x00", tag)
        parts.append(protected)
    return "".join(parts)


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def frontmatter(title: str, description: str, sidebar: str, product_key: str) -> str:
    product_label = PRODUCT_KEYWORDS.get(product_key, product_key)
    keywords = ["TYPO3", "T3Planet", product_label, title]
    # de-dupe preserving order
    seen: set[str] = set()
    kw_lines = []
    for k in keywords:
        if k and k not in seen:
            seen.add(k)
            kw_lines.append(f'  - "{yaml_escape(k)}"')
    return (
        "---\n"
        f'title: "{yaml_escape(title)}"\n'
        f'description: "{yaml_escape(description)}"\n'
        "keywords:\n"
        + "\n".join(kw_lines)
        + "\n"
        f'sidebarTitle: "{yaml_escape(sidebar)}"\n'
        "---\n\n"
    )


def sidebar_from_title(title: str, mint_rel: str) -> str:
    # Prefer short leaf folder name for deep pages when title is long
    if len(title) <= 48:
        return title
    leaf = Path(mint_rel).parent.name if mint_rel.endswith("Index.md") else Path(mint_rel).stem
    return leaf


def migrate_one(live: str, mint: str | None = None, product: str | None = None, key: str | None = None) -> dict:
    live_rel = normalize_live_rel(live)
    mint_rel = mint or live_to_mint_path(live_rel)
    mint_md = ROOT / mint_rel
    product = product or live_product(live_rel)
    key = key or product

    print(f"Migrating {live_rel} -> {mint_rel}")
    try:
        html = fetch_html(live_rel)
    except urllib.error.HTTPError as exc:
        return {"live": live_rel, "mint": mint_rel, "ok": False, "error": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"live": live_rel, "mint": mint_rel, "ok": False, "error": str(exc)}

    if "rst-content" not in html and "articleBody" not in html:
        return {"live": live_rel, "mint": mint_rel, "ok": False, "error": "No rst-content in response"}

    mint_md.parent.mkdir(parents=True, exist_ok=True)
    title, description, body = html_to_mdx(html, live_rel, mint_md)
    body = escape_mdx(body)
    sidebar = sidebar_from_title(title, mint_rel)
    content = frontmatter(title, description, sidebar, key) + body + "\n"
    mint_md.write_text(content, encoding="utf-8")
    return {
        "live": live_rel,
        "mint": mint_rel,
        "ok": True,
        "title": title,
        "chars": len(body),
    }


def run_batch(batch_path: Path) -> dict:
    entries = json.loads(batch_path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise SystemExit("Batch JSON must be a list of {live, mint, product, key}")

    results = {"migrated": [], "failed": [], "skipped": []}
    for entry in entries:
        live = entry.get("live")
        if not live:
            results["skipped"].append({"entry": entry, "reason": "missing live"})
            continue
        if entry.get("skip"):
            results["skipped"].append({"live": live, "reason": entry.get("reason", "skip flag")})
            continue
        result = migrate_one(
            live=live,
            mint=entry.get("mint"),
            product=entry.get("product"),
            key=entry.get("key"),
        )
        if result.get("ok"):
            results["migrated"].append(result)
            print(f"  OK ({result['chars']} chars) {result['title']}")
        else:
            results["failed"].append(result)
            print(f"  FAIL: {result.get('error')}")
    return results


def merge_one(live: str, mint: str | None = None) -> dict:
    """Surgical merge one page using reconcile migrator (preserves CardGroups)."""
    import importlib.util

    live_rel = normalize_live_rel(live)
    mint_rel = mint or live_to_mint_path(live_rel)
    reconcile_path = ROOT / "scripts/qa-final/reconcile_migrate_from_live.py"
    rem_path = ROOT / "scripts/qa-final/remigrate_t3ac_t3as_t3af_aug10.py"
    spec = importlib.util.spec_from_file_location("remigrate", rem_path)
    rem = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rem)

    mint_md = ROOT / mint_rel
    row = {
        "live": live_rel,
        "mint": mint_rel,
        "status": ["MISSING_CONTENT"],
        "missing_sections": [],
        "missing_images": [],
        "missing_supademo": [],
        "thin": False,
        "code_diff": {"has_diff": True},
        "link_diff": {"has_diff": False},
    }
    actions = {
        "pages_created": [],
        "pages_updated": [],
        "supademos_added": {},
        "images_added": {},
        "sections_added": {},
        "nav_added": [],
        "files_modified": [],
        "errors": [],
    }
    spec2 = importlib.util.spec_from_file_location("reconcile_migrate", reconcile_path)
    rec = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(rec)

    try:
        html, _ = rem.get_html(live_rel)
        live_ex = rem.extract_live(html)
        if mint_md.is_file():
            mint_ex = rem.extract_mint(mint_md)
            row["missing_sections"] = rem.missing_sections(live_ex["headings"], mint_ex["headings"])
            row["missing_images"] = rem.missing_images(live_ex["images"], mint_ex)
            row["missing_supademo"] = [
                i for i in live_ex["supademo_ids"] if i not in mint_ex["supademo_ids"]
            ]
            ratio = mint_ex["text_len"] / live_ex["text_len"] if live_ex["text_len"] else 1.0
            row["thin"] = ratio < 0.45 and live_ex["text_len"] > 600
        else:
            row["status"] = ["NEW_PAGE"]
    except Exception as exc:
        return {"live": live_rel, "mint": mint_rel, "ok": False, "error": str(exc)}

    changed = rec.migrate_row(row, actions)
    if row["status"] == ["NEW_PAGE"] and not changed:
        try:
            path = rem.create_page_from_live(live_rel)
            changed = True
            actions["pages_created"].append(live_rel)
            actions["files_modified"].append(str(path.relative_to(ROOT)))
        except Exception as exc:
            return {"live": live_rel, "mint": mint_rel, "ok": False, "error": str(exc)}

    return {
        "live": live_rel,
        "mint": mint_rel,
        "ok": True,
        "merged": changed,
        "actions": actions,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Migrate live Sphinx HTML to Mintlify MDX")
    parser.add_argument("live", nargs="?", help="Live path e.g. ExtNsT3AF/Installation/Index.html")
    parser.add_argument("mint", nargs="?", help="Mint path e.g. ExtNsT3AF/Installation/Index.md")
    parser.add_argument("--batch", help="Batch JSON file with {live, mint, product, key} entries")
    parser.add_argument(
        "--merge",
        action="store_true",
        help="Surgical merge (preserve CardGroups) instead of full-file overwrite",
    )
    args = parser.parse_args(argv)

    if args.batch:
        results = run_batch(Path(args.batch))
        print("\n=== Summary ===")
        print(f"Migrated: {len(results['migrated'])}")
        print(f"Failed:   {len(results['failed'])}")
        print(f"Skipped:  {len(results['skipped'])}")
        if results["failed"]:
            for f in results["failed"]:
                print(f"  - {f['live']}: {f.get('error')}")
        out = ROOT / "scripts" / "migrate_from_live_report.json"
        out.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"Report: {out.relative_to(ROOT)}")
        return 1 if results["failed"] else 0

    if not args.live:
        parser.error("Provide LIVE MINT paths or --batch FILE")

    if args.merge:
        result = merge_one(args.live, args.mint)
        if not result.get("ok"):
            print(f"FAIL: {result.get('error')}", file=sys.stderr)
            return 1
        print(f"Merged {result['mint']} (changed={result.get('merged')})")
        return 0

    result = migrate_one(args.live, args.mint)
    if not result["ok"]:
        print(f"FAIL: {result.get('error')}", file=sys.stderr)
        return 1
    print(f"Wrote {result['mint']} ({result['chars']} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
