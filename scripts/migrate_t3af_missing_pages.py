#!/usr/bin/env python3
"""Migrate missing ExtNsT3AF live Sphinx HTML pages into T3AF/ Mintlify MDX."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "T3AF"
CACHE = Path("/tmp/t3af_migrate")
LIVE_BASE = "https://docs.t3planet.de/en/latest/ExtNsT3AF/"

PAGES = [
    ("Architecture/Index", "Architecture", "Architecture of EXT:ns_t3af — services, adapters, caching, and constraints."),
    ("Usage/Index", "Usage", "Practical usage of T3AF for admins, editors, and stakeholders."),
    ("Troubleshooting/Index", "Troubleshooting", "Common T3AF issues and how to resolve them."),
    ("Privacy/Index", "Privacy", "Privacy, logging levels, and data handling for T3AF."),
    ("ReleaseNotes/Index", "Release Notes", "Version-wise release notes for T3AF."),
    ("ReleaseNotes/1.0.0/Index", "1.0.0", "T3AF v1.0.0 release notes."),
    ("T3PlanetCreditsQA/Index", "T3Planet Credits QA", "QA checklist and verification steps for T3Planet Credits."),
    ("MCPTesting/Index", "MCP Testing", "Testing guide for the T3AF MCP server."),
    ("DeveloperGuide/Index", "Developer Guide", "Build TYPO3 extensions on top of T3AF."),
    ("DeveloperGuide/ExtensionIntegration/Index", "Extension Integration", "Integrate your TYPO3 extension with T3AF services."),
    ("DeveloperGuide/CustomProviders/Index", "Custom AI Providers", "Create custom AI provider adapters for T3AF."),
    ("DeveloperGuide/CustomAiPrompts/Index", "Custom AI Prompts", "Register and manage custom AI prompts."),
    ("DeveloperGuide/CustomAiFeatures/Index", "Custom AI Features", "Register custom AI feature cards and settings."),
    ("DeveloperGuide/FeatureProviderOverrides/Index", "Feature Provider Overrides", "Override AI providers per feature."),
    ("DeveloperGuide/CustomMcpTools/Index", "Custom MCP Tools", "Register custom MCP tools from your extension."),
    ("DeveloperGuide/CustomAiAccess/Index", "Custom AI Access", "Extend AI access and permissions catalogs."),
    ("DeveloperGuide/T3PlanetCredits/Index", "T3Planet Credits (Dev)", "Developer reference for T3Planet Credits integration."),
]

SIDEBAR_TITLES = {
    "ReleaseNotes/1.0.0/Index": "1.0.0",
    "DeveloperGuide/CustomProviders/Index": "Custom Providers",
    "DeveloperGuide/CustomAiPrompts/Index": "Custom AI Prompts",
    "DeveloperGuide/CustomAiFeatures/Index": "Custom AI Features",
    "DeveloperGuide/FeatureProviderOverrides/Index": "Feature Overrides",
    "DeveloperGuide/CustomMcpTools/Index": "Custom MCP Tools",
    "DeveloperGuide/CustomAiAccess/Index": "Custom AI Access",
    "DeveloperGuide/T3PlanetCredits/Index": "T3Planet Credits",
    "DeveloperGuide/ExtensionIntegration/Index": "Extension Integration",
    "T3PlanetCreditsQA/Index": "Credits QA",
    "MCPTesting/Index": "MCP Testing",
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


def fetch_html(rel: str) -> Path:
    out = CACHE / f"{rel}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists() or out.stat().st_size < 500:
        url = f"{LIVE_BASE}{rel}.html"
        req = urllib.request.Request(url, headers={"User-Agent": "MintlifyDoc-Migrator/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            out.write_bytes(resp.read())
    return out


def clean_heading(text: str) -> str:
    return text.replace("\uf0c1", "").replace("¶", "").strip()


def rewrite_href(href: str, page_rel: str) -> str:
    if not href or href.startswith("#") or href.startswith("mailto:") or href.startswith("javascript:"):
        return href
    if href.startswith("http://") or href.startswith("https://"):
        # Absolute live ExtNsT3AF → T3AF
        m = re.match(r"https?://docs\.t3planet\.de/(?:[a-z]{2}/)?latest/ExtNsT3AF/(.+?)(?:\.html)?(?:#(.*))?$", href)
        if m:
            path = m.group(1).rstrip("/")
            if path.endswith("/Index") or path.endswith("Index"):
                pass
            elif not path.endswith("Index"):
                # file like BuyNow → GetThisExtension
                if path == "BuyNow" or path.endswith("/BuyNow"):
                    return "/T3AF/GetThisExtension/Index"
            frag = f"#{m.group(2)}" if m.group(2) else ""
            if path.endswith(".html"):
                path = path[:-5]
            if not path.endswith("/Index") and "/Index" not in path and path.count("/") == 0:
                # Support.html style
                if path in {"Support", "BuyNow"}:
                    path = "GetThisExtension" if path == "BuyNow" else "Support"
                    return f"/T3AF/{path}/Index{frag}"
            return f"/T3AF/{path}{frag}" if path.endswith("Index") or "/Index" in path else f"/T3AF/{path}/Index{frag}"
        return href

    # Relative .html
    base_url = urljoin(f"{LIVE_BASE}{page_rel}.html", href)
    parsed = urlparse(base_url)
    path = unquote(parsed.path)
    frag = f"#{parsed.fragment}" if parsed.fragment else ""

    if "/ExtNsT3AF/" in path:
        rel_path = path.split("/ExtNsT3AF/", 1)[1]
    elif path.endswith(".html"):
        # resolve relative to page
        rel_path = Path(page_rel).parent.joinpath(href.split("#")[0]).as_posix()
        rel_path = Path(rel_path).resolve().as_posix()  # may be absolute weirdness
        # Better: use urljoin relative logic already in base_url
        rel_path = path
        if "/ExtNsT3AF/" in rel_path:
            rel_path = rel_path.split("/ExtNsT3AF/", 1)[1]
        else:
            # fallback from href only
            rel_path = href.split("#")[0]
            joined = (Path(page_rel).parent / rel_path).as_posix()
            while "/../" in joined:
                joined = re.sub(r"[^/]+/\.\./", "", joined)
            rel_path = joined.lstrip("./")
    else:
        return href

    rel_path = rel_path.replace(".html", "")
    if rel_path.endswith("/"):
        rel_path = rel_path.rstrip("/") + "/Index"
    if rel_path in {"BuyNow", "Support"}:
        mapped = "GetThisExtension" if rel_path == "BuyNow" else "Support"
        return f"/T3AF/{mapped}/Index{frag}"
    if not rel_path.endswith("Index") and "/" not in rel_path:
        # sibling like Usage → Usage/Index unlikely; keep
        pass
    # Normalize ../ paths that survived
    parts = []
    for part in rel_path.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
            continue
        parts.append(part)
    rel_path = "/".join(parts)
    if not rel_path.endswith("Index"):
        # ExtNsT3AF/Installation style already has Index in path usually
        if Path(rel_path).suffix == "":
            # could be Architecture already as Architecture/Index from html
            pass
    return f"/T3AF/{rel_path}{frag}"


def inline_children(el: Tag, page_rel: str) -> str:
    parts: list[str] = []
    for child in el.children:
        parts.append(inline(child, page_rel))
    return "".join(parts)


def inline(node, page_rel: str) -> str:
    if isinstance(node, NavigableString):
        text = str(node)
        # collapse excessive whitespace but keep single spaces
        return text.replace("\xa0", " ")
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name in {"script", "style", "svg"}:
        return ""
    if name == "br":
        return "\n"
    if name in {"strong", "b"}:
        return f"**{inline_children(node, page_rel).strip()}**"
    if name in {"em", "i"}:
        return f"*{inline_children(node, page_rel).strip()}*"
    if name == "code":
        return f"`{node.get_text()}`"
    if name == "a":
        if "headerlink" in (node.get("class") or []):
            return ""
        href = node.get("href") or ""
        text = inline_children(node, page_rel).strip()
        if not text:
            text = href
        if "toc-backref" in (node.get("class") or []):
            return text
        new_href = rewrite_href(href, page_rel)
        if new_href.startswith("#") and not text:
            return ""
        return f"[{text}]({new_href})"
    if name == "span":
        classes = node.get("class") or []
        if "pre" in classes or "literal" in " ".join(classes):
            return f"`{node.get_text()}`"
        return inline_children(node, page_rel)
    if name == "img":
        src = node.get("src") or ""
        alt = node.get("alt") or "image"
        local = download_image(src, page_rel)
        return f"![{alt}]({local})"
    if name in {"kbd", "samp"}:
        return f"`{node.get_text()}`"
    if name == "tt":
        return f"`{node.get_text()}`"
    return inline_children(node, page_rel)


def download_image(src: str, page_rel: str) -> str:
    if not src:
        return src
    abs_url = urljoin(f"{LIVE_BASE}{page_rel}.html", src)
    name = Path(urlparse(abs_url).path).name
    img_dir = DEST / Path(page_rel).parent / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    dest = img_dir / name
    if not dest.exists():
        try:
            req = urllib.request.Request(abs_url, headers={"User-Agent": "MintlifyDoc-Migrator/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                dest.write_bytes(resp.read())
        except Exception as exc:  # noqa: BLE001
            print(f"  WARN image download failed: {abs_url} ({exc})")
            return abs_url
    return f"./images/{name}"


def pre_text(pre: Tag) -> str:
    # Prefer plain text without span noise
    return pre.get_text()


def convert_table(table: Tag, page_rel: str) -> str:
    rows = []
    for tr in table.select("tr"):
        cells = tr.find_all(["th", "td"], recursive=False)
        if not cells:
            cells = tr.find_all(["th", "td"])
        vals = [inline_children(c, page_rel).replace("\n", " ").strip() for c in cells]
        rows.append(vals)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    # If first row is all th, treat as header; else synthesize
    has_th = bool(table.select("th"))
    lines = []
    if has_th:
        header = rows[0]
        body = rows[1:]
    else:
        header = [f"Col {i+1}" for i in range(width)]
        body = rows
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * width) + " |")
    for r in body:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)


def convert_list(el: Tag, page_rel: str, ordered: bool = False) -> str:
    lines: list[str] = []
    items = [c for c in el.children if isinstance(c, Tag) and c.name == "li"]
    for idx, li in enumerate(items, 1):
        # Nested lists
        prefix = f"{idx}. " if ordered else "- "
        parts: list[str] = []
        nested: list[str] = []
        for child in li.children:
            if isinstance(child, Tag) and child.name in {"ul", "ol"}:
                nested.append(convert_list(child, page_rel, ordered=(child.name == "ol")))
            elif isinstance(child, Tag) and child.name == "p":
                parts.append(inline_children(child, page_rel).strip())
            else:
                t = inline(child, page_rel).strip()
                if t:
                    parts.append(t)
        text = " ".join(p for p in parts if p).strip()
        lines.append(f"{prefix}{text}")
        for n in nested:
            for nl in n.splitlines():
                lines.append(f"  {nl}")
    return "\n".join(lines)


def convert_admonition(div: Tag, page_rel: str) -> str:
    classes = [c.lower() for c in (div.get("class") or [])]
    kind = "note"
    for c in classes:
        if c in ADMONITION_TAGS:
            kind = c
            break
    tag = ADMONITION_TAGS.get(kind, "Note")
    # Remove title
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
            converted = convert_block(child, page_rel)
            if converted:
                body_parts.append(converted)
    body = "\n\n".join(body_parts).strip()
    return f"<{tag}>\n{body}\n</{tag}>"


def convert_block(el: Tag, page_rel: str) -> str:
    name = el.name.lower()
    classes = el.get("class") or []

    if name in {"script", "style", "nav"}:
        return ""
    if "contents" in classes or "toctree-wrapper" in classes:
        # Expand toctree links if present
        links = []
        for a in el.select("a.reference"):
            href = rewrite_href(a.get("href") or "", page_rel)
            text = a.get_text(strip=True)
            if text and href:
                links.append(f"- [{text}]({href})")
        return "\n".join(links)

    if name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
        level = int(name[1])
        # Drop page h1 — frontmatter title covers it
        if level == 1:
            return ""
        text = clean_heading(inline_children(el, page_rel))
        # strip nested markdown link wrappers from toc-backref already handled
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text).strip()
        return f"{'#' * level} {text}"

    if name == "p":
        text = inline_children(el, page_rel).strip()
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text

    if name == "pre" or (name == "div" and any(c.startswith("highlight") for c in classes)):
        pre = el if name == "pre" else el.select_one("pre")
        if pre is None:
            return ""
        lang = "text"
        for c in classes:
            if c.startswith("highlight-"):
                lang = c.replace("highlight-", "").split()[0]
                break
        parent = el.find_parent("div", class_=re.compile(r"highlight"))
        if parent:
            for c in parent.get("class") or []:
                if c.startswith("highlight-"):
                    lang = c.replace("highlight-", "").split()[0]
        if lang in {"default", "none", "notranslate"}:
            lang = "text"
        if lang == "console":
            lang = "bash"
        code = pre_text(pre).rstrip("\n")
        # strip leading empty span marker line artifacts
        return f"```{lang}\n{code}\n```"

    if name == "ul":
        return convert_list(el, page_rel, ordered=False)
    if name == "ol":
        return convert_list(el, page_rel, ordered=True)
    if name == "table" or (name == "div" and "table-wrapper" in classes):
        table = el if name == "table" else el.select_one("table")
        return convert_table(table, page_rel) if table else ""
    if name == "div" and "admonition" in classes:
        return convert_admonition(el, page_rel)
    if name == "blockquote":
        text = inline_children(el, page_rel).strip()
        return "\n".join(f"> {ln}" if ln else ">" for ln in text.splitlines())
    if name == "hr":
        return "---"
    if name == "section":
        parts = []
        for child in el.children:
            if isinstance(child, Tag):
                c = convert_block(child, page_rel)
                if c:
                    parts.append(c)
        return "\n\n".join(parts)
    if name == "div":
        # generic container
        parts = []
        for child in el.children:
            if isinstance(child, Tag):
                c = convert_block(child, page_rel)
                if c:
                    parts.append(c)
            elif isinstance(child, NavigableString) and str(child).strip():
                parts.append(str(child).strip())
        return "\n\n".join(parts)
    if name in {"dl"}:
        lines = []
        for child in el.children:
            if not isinstance(child, Tag):
                continue
            if child.name == "dt":
                lines.append(f"**{inline_children(child, page_rel).strip()}**")
            elif child.name == "dd":
                lines.append(inline_children(child, page_rel).strip())
                lines.append("")
        return "\n".join(lines).strip()
    # fallback
    return inline_children(el, page_rel).strip()


def html_to_mdx(html: str, page_rel: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.title.string if soup.title else ""
    page_title = clean_heading(title_tag.split("—")[0].split("–")[0].strip()) if title_tag else Path(page_rel).parent.name

    main = soup.select_one("[role=main]") or soup.select_one(".document") or soup.body
    for junk in main.select(".headerlink, .sphinxsidebar, script, style, .related"):
        junk.decompose()

    # Prefer articleBody
    body_root = main.select_one("[itemprop=articleBody]") or main

    parts: list[str] = []
    for child in body_root.children:
        if isinstance(child, Tag):
            converted = convert_block(child, page_rel)
            if converted:
                parts.append(converted)

    body = "\n\n".join(parts)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()

    # Determine h1 from content if better
    h1 = main.select_one("h1")
    if h1:
        page_title = clean_heading(h1.get_text())
    # Sphinx sometimes uses <no title> for leaf version pages
    if not page_title or page_title.lower() in {"<no title>", "no title"}:
        page_title = Path(page_rel).parent.name

    return page_title, body


def frontmatter(title: str, description: str, sidebar: str) -> str:
    return (
        "---\n"
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        "keywords:\n"
        '  - "TYPO3"\n'
        '  - "T3Planet"\n'
        '  - "T3AF"\n'
        f'  - "{title}"\n'
        f'sidebarTitle: "{sidebar}"\n'
        "---\n\n"
    )


def enrich_release_notes_index(body: str) -> str:
    """Live Index toctree is empty in article body; add child link from known TOC."""
    if "/T3AF/ReleaseNotes/1.0.0/Index" in body:
        return body
    extra = (
        "## Versions\n\n"
        "- [1.0.0](/T3AF/ReleaseNotes/1.0.0/Index)\n"
    )
    return (body + "\n\n" + extra).strip() if body else extra


def main() -> None:
    created = []
    for rel, title_hint, description in PAGES:
        print(f"Converting {rel} ...")
        html_path = fetch_html(rel)
        html = html_path.read_text(encoding="utf-8", errors="replace")
        page_title, body = html_to_mdx(html, rel)
        if not page_title or page_title.lower() in {"<no title>", "no title"}:
            page_title = title_hint
        title_overrides = {
            "Privacy/Index": "Privacy",
            "ReleaseNotes/1.0.0/Index": "1.0.0",
            "T3PlanetCreditsQA/Index": "T3Planet Credits QA",
            "MCPTesting/Index": "MCP Testing",
            "DeveloperGuide/T3PlanetCredits/Index": "T3Planet Credits (v1.1+)",
        }
        if rel in title_overrides:
            page_title = title_overrides[rel]
        sidebar = SIDEBAR_TITLES.get(
            rel,
            title_hint if title_hint != "T3Planet Credits (Dev)" else "T3Planet Credits",
        )
        if rel == "ReleaseNotes/Index":
            body = enrich_release_notes_index(body)
        content = frontmatter(page_title, description, sidebar) + body + "\n"
        out = DEST / f"{rel}.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        created.append((str(out.relative_to(ROOT)), page_title, len(body)))
        print(f"  -> {out.relative_to(ROOT)} ({len(body)} chars)")

    print("\nDone:")
    for path, title, n in created:
        print(f"  {path}: {title} ({n} chars)")


if __name__ == "__main__":
    main()
