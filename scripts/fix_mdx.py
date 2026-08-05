#!/usr/bin/env python3
"""Post-process migrated MD/MDX files to fix Mintlify parsing issues."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MDX_COMPONENTS = {
    "Note", "Warning", "Tip", "Info", "Check", "Card", "CardGroup",
    "Accordion", "AccordionGroup", "Tabs", "Tab", "Steps", "Step",
    "CodeGroup", "Frame", "Tooltip", "Icon", "Mermaid",
}

HTML_TAGS = {
    "div", "iframe", "style", "script", "table", "tbody", "thead", "tr", "td", "th",
    "a", "span", "p", "ul", "ol", "li", "strong", "em", "br", "hr", "img", "h1",
    "h2", "h3", "h4", "caption", "colgroup", "col", "link", "meta", "head", "body", "html",
}


def escape_placeholders(text: str) -> str:
    """Escape <PLACEHOLDER> patterns that MDX interprets as JSX tags."""

    def replacer(match: re.Match) -> str:
        tag = match.group(1)
        if tag in MDX_COMPONENTS or tag.lower() in HTML_TAGS:
            return match.group(0)
        return f"`{match.group(0)}`"

    return re.sub(r"<([A-Za-z][A-Za-z0-9-]*)>", replacer, text)


def fix_iframe_src(text: str) -> str:
    return re.sub(
        r'(<iframe\s+src=)(https?://[^>\s]+)',
        r'\1"\2"',
        text,
    )


def fix_orphan_underlines(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"^[=\-~^`#'\"]{3,}$", line.strip()):
            i += 1
            continue
        if line.strip() == "::":
            i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def fix_duplicate_h1(text: str) -> str:
    """Remove stray # prefix when RST title underline was converted."""
    lines = text.splitlines()
    out: list[str] = []
    in_frontmatter = False
    frontmatter_done = False
    for i, line in enumerate(lines):
        if i == 0 and line.strip() == "---":
            in_frontmatter = True
            out.append(line)
            continue
        if in_frontmatter:
            out.append(line)
            if line.strip() == "---":
                in_frontmatter = False
            continue
        if not frontmatter_done and line.startswith("# ") and i + 1 < len(lines) and lines[i + 1].startswith("# "):
            # Keep only the second heading if duplicate
            continue
        out.append(line)
    return "\n".join(out)


def fix_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original

    # Split frontmatter from body
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---"
            body = parts[2]
        else:
            frontmatter = ""
            body = text
    else:
        frontmatter = ""
        body = text

    body = fix_orphan_underlines(body)
    body = fix_iframe_src(body)
    body = escape_placeholders(body)
    body = re.sub(r"\n{3,}", "\n\n", body)

    new_text = (frontmatter + body) if frontmatter else body
    if not new_text.endswith("\n"):
        new_text += "\n"

    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def sync_nav_with_files() -> None:
    """Update docs.json nav to only reference files that exist."""
    import json

    docs_path = ROOT / "docs.json"
    docs = json.loads(docs_path.read_text(encoding="utf-8"))

    def resolve_page(slug: str) -> str | None:
        for ext in (".mdx", ".md"):
            if (ROOT / f"{slug}{ext}").exists():
                return slug
        return None

    def filter_pages(pages: list) -> list:
        result = []
        for page in pages:
            if isinstance(page, str):
                resolved = resolve_page(page)
                if resolved:
                    result.append(resolved)
            elif isinstance(page, dict) and "group" in page:
                page["pages"] = filter_pages(page.get("pages", []))
                if page["pages"]:
                    result.append(page)
            else:
                result.append(page)
        return result

    def walk_nav(nav: dict) -> None:
        if "tabs" in nav:
            for tab in nav["tabs"]:
                if "groups" in tab:
                    for group in tab["groups"]:
                        group["pages"] = filter_pages(group.get("pages", []))
        if "groups" in nav:
            nav["groups"] = filter_pages(nav["groups"])

    walk_nav(docs["navigation"])
    docs_path.write_text(json.dumps(docs, indent=2), encoding="utf-8")


def main() -> None:
    fixed = 0
    for path in ROOT.rglob("*"):
        if path.suffix in {".md", ".mdx"} and "scripts" not in path.parts:
            if fix_file(path):
                fixed += 1
    print(f"Fixed {fixed} files")
    sync_nav_with_files()
    print("Synced docs.json navigation with existing files")


if __name__ == "__main__":
    main()
