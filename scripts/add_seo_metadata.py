#!/usr/bin/env python3
"""Add SEO description and keywords to all documentation pages."""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "node_modules", ".git", ".venv-translate", "logo", "_snippets"}

PRODUCT_NAMES = {
    "ExtNsT3AI": "T3AI",
    "ExtNsT3AS": "T3AS",
    "ExtNsT3AC": "T3AC",
    "ExtNsT3AL": "T3AL",
    "ExtNsT3AA": "T3AA",
    "ExtNsT3AB": "T3AB",
    "EXTKarma": "T3 Karma",
    "EXTBootstrap": "T3 Bootstrap",
    "EXTAvatar": "T3 Avatar",
    "EXTAyu": "T3 Ayu",
    "EXTReva": "T3 Reva",
    "EXTShiva": "T3 Shiva",
    "EXTShop": "T3 Shop",
    "License": "License",
}


def product_from_path(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if parts[0] == "de" and len(parts) > 1:
        parts = parts[1:]
    if not parts:
        return "T3Planet"
    top = parts[0]
    return PRODUCT_NAMES.get(top, top.replace("ExtNs", "EXT:ns_").replace("EXT", ""))


def page_context(rel: str, title: str) -> str:
    parts = Path(rel).parts
    if parts[-1] == "Index.md":
        section = parts[-2] if len(parts) > 1 else "Documentation"
    else:
        section = parts[-1].replace(".md", "")
    product = product_from_path(rel)
    tl = title.lower()
    if "installation" in tl or section.lower() == "installation":
        return f"install {product}"
    if "configuration" in tl or section.lower() == "configuration":
        return f"configure {product}"
    if "introduction" in tl:
        return f"overview of {product}"
    if "update" in tl:
        return f"update {product}"
    if "support" in tl or "help" in tl:
        return f"support for {product}"
    return f"{title} for {product}"


def make_description(title: str, rel: str, is_de: bool) -> str:
    ctx = page_context(rel, title)
    if is_de:
        return (
            f"{title} – Offizielle T3Planet-Dokumentation. "
            f"Anleitung und Referenz für {ctx} in TYPO3."
        )
    return (
        f"{title} – Official T3Planet documentation. "
        f"Guide and reference for {ctx} in TYPO3."
    )


def make_keywords(title: str, rel: str) -> list[str]:
    product = product_from_path(rel)
    base = ["TYPO3", "T3Planet", product, title]
    parts = Path(rel).parts
    if len(parts) > 2:
        base.append(parts[-2])
    return list(dict.fromkeys(k for k in base if k and len(k) > 1))[:8]


def update_frontmatter(text: str, rel: str) -> str:
    is_de = rel.startswith("de/") or rel.startswith("de\\")
    m = re.match(r"^(---\n)(.*?)(\n---\n)(.*)$", text, re.S)
    if not m:
        return text
    fm, body = m.group(2), m.group(4)
    title_m = re.search(r'^title:\s*"(.*?)"', fm, re.M)
    if not title_m:
        title_m = re.search(r"^title:\s*(.+)$", fm, re.M)
    title = title_m.group(1).strip().strip('"') if title_m else "Documentation"

    desc = make_description(title, rel, is_de)
    kw = make_keywords(title, rel)

    fm = re.sub(r"^description:.*\n", "", fm, flags=re.M)
    fm = re.sub(r"^keywords:.*\n", "", fm, flags=re.M)
    fm = re.sub(r"^sidebarTitle:.*\n", "", fm, flags=re.M)

    sidebar = title if len(title) <= 28 else title[:25] + "..."
    extra = (
        f'description: "{desc.replace(chr(34), chr(39))}"\n'
        f"keywords:\n"
        + "".join(f'  - "{k}"\n' for k in kw)
        + f'sidebarTitle: "{sidebar.replace(chr(34), chr(39))}"\n'
    )
    fm = fm.rstrip("\n") + "\n" + extra
    return f"---\n{fm}---\n{body}"


def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = Path(dirpath) / fn
            rel = str(path.relative_to(ROOT))
            text = path.read_text(encoding="utf-8")
            new = update_frontmatter(text, rel)
            if new != text:
                path.write_text(new, encoding="utf-8")
                changed += 1
    print(f"Added SEO metadata to {changed} pages.")


if __name__ == "__main__":
    main()
