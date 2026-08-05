#!/usr/bin/env python3
"""
T3Planet RST -> Mintlify MD migration (v2).
- Original Sphinx folder structure preserved
- Output .md only (no .mdx)
- Navigation matches index.rst order
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

RST_ROOT = Path("/Users/nitsan/www/T3Planet Docs/docs/docs")
OUT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}

ADMONITIONS = {"note", "Note", "warning", "Warning", "attention", "important", "tip", "Tip", "hint"}


def parse_toctree(content: str) -> list[str]:
    entries: list[str] = []
    in_tree = False
    for line in content.splitlines():
        s = line.strip()
        if s.startswith(".. toctree::"):
            in_tree = True
            continue
        if in_tree:
            if not s:
                if entries:
                    break
                continue
            if s.startswith(":"):
                continue
            entries.append(s)
    return entries


def title_from_content(content: str) -> str:
    lines = [ln.rstrip() for ln in content.splitlines()]
    for i, line in enumerate(lines):
        if i + 1 < len(lines) and re.match(r"^[=\-~^`#'\"]+$", lines[i + 1].strip()) and line.strip():
            return line.strip()
    for line in lines:
        if line.strip() and not line.strip().startswith(".."):
            return line.strip()[:120]
    return "Documentation"


def rst_path_to_md(rst_path: Path) -> Path:
    rel = rst_path.relative_to(RST_ROOT)
    return OUT_ROOT / str(rel).replace(".rst", ".md")


def md_slug(rst_path: Path) -> str:
    return str(rst_path.relative_to(RST_ROOT)).replace(".rst", "").replace("\\", "/")


def parse_role_images(lines: list[str]) -> tuple[dict[str, str], list[str]]:
    roles: dict[str, str] = {}
    out: list[str] = []
    for line in lines:
        m = re.match(r"\.\.\s+\|([^|]+)\|\s+image::\s+(.+)$", line.strip())
        if m:
            roles[m.group(1)] = m.group(2).strip()
            continue
        out.append(line)
    return roles, out


def convert_list_table(lines: list[str], start: int) -> tuple[str, int]:
    title = ""
    header_rows = 0
    i = start + 1
    while i < len(lines) and lines[i].strip().startswith(":"):
        opt = lines[i].strip()
        if ":header-rows:" in opt:
            header_rows = int(opt.split(":")[-1].strip())
        if "list-table::" in opt:
            title = opt.split("::", 1)[-1].strip()
        i += 1

    rows: list[list[str]] = []
    current: list[str] = []
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith(".. ") and not s.startswith("* "):
            break
        if s.startswith("* -"):
            if current:
                rows.append(current)
            current = [s[3:].strip()]
        elif s.startswith("- ") and current:
            current.append(s[2:].strip())
        elif not s and rows:
            break
        i += 1
    if current:
        rows.append(current)

    md: list[str] = []
    if title:
        md.extend([f"### {title}", ""])
    for ri, row in enumerate(rows):
        md.append("| " + " | ".join(row) + " |")
        if ri == 0 and header_rows:
            md.append("| " + " | ".join("---" for _ in row) + " |")
    md.append("")
    return "\n".join(md), i


def convert_body(lines: list[str], roles: dict[str, str]) -> str:
    out: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith(".. include::"):
            i += 1
            continue
        if stripped.startswith(".. _") and stripped.endswith(":"):
            i += 1
            continue
        if stripped.startswith(".. toctree::"):
            i += 1
            while i < len(lines):
                s = lines[i].strip()
                if not s or s.startswith(":"):
                    i += 1
                    continue
                if s.startswith(".."):
                    break
                i += 1
            continue

        if stripped.startswith(".. list-table::"):
            table, i = convert_list_table(lines, i)
            out.append(table)
            continue

        if stripped.startswith(".. figure::") or stripped.startswith(".. image::"):
            img = stripped.split("::", 1)[1].strip()
            alt = ""
            i += 1
            while i < len(lines) and lines[i].startswith("   :"):
                if ":alt:" in lines[i]:
                    alt = lines[i].split(":", 2)[-1].strip()
                i += 1
            out.extend([f"![{alt or 'image'}]({img})", ""])
            continue

        if re.match(r"\.\.\s+(\w+)::\s*$", stripped):
            kind = stripped.split()[1].replace("::", "")
            if kind in ADMONITIONS:
                label = "Warning" if kind in {"warning", "Warning", "attention", "important"} else "Note"
                i += 1
                body: list[str] = []
                while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                    body.append(lines[i][3:] if lines[i].startswith("   ") else "")
                    i += 1
                text = "\n".join(body).strip()
                out.extend([f"> **{label}:** {text}", ""])
                continue

        if stripped.startswith(".. raw:: html"):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                out.append(lines[i][3:] if lines[i].startswith("   ") else "")
                i += 1
            out.append("")
            continue

        if stripped.startswith(".. code-block::"):
            lang = stripped.split("::", 1)[1].strip() or "text"
            if lang == "language":
                lang = "text"
            if lang == "python" and "composer" in "\n".join(lines[i : i + 8]).lower():
                lang = "bash"
            i += 1
            code: list[str] = []
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                code.append(lines[i][3:] if lines[i].startswith("   ") else "")
                i += 1
            out.extend([f"```{lang}", *code, "```", ""])
            continue

        if i + 1 < len(lines) and re.match(r"^[=\-~^`#'\"]+$", lines[i + 1].strip()) and stripped:
            level_char = lines[i + 1].strip()[0]
            level = min({"=": 2, "-": 3, "~": 4, "^": 5}.get(level_char, 3), 4)
            out.extend([f"{'#' * level} {stripped}", ""])
            i += 2
            continue

        if re.match(r"^#\.\s+", stripped):
            # RST auto-numbered list; actual numbering fixed in post-process
            out.append("__RSTOL__" + re.sub(r"^#\.\s+", "", stripped))
            i += 1
            continue

        # Transparent wrapper directives: drop the directive line but KEEP the body
        if re.match(r"\.\.\s+(rst-class|container|highlights|epigraph|bignums|admonition)::", stripped):
            i += 1
            continue

        if stripped.startswith(".. "):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
            continue

        if stripped:
            text = stripped
            for role, img in roles.items():
                text = text.replace(f"|{role}|", f"![]({img})")
            text = re.sub(r"`([^<`]+)\s*<([^>]+)>`_", r"[\1](\2)", text)
            if "``" in text and not text.startswith("```"):
                text = re.sub(r"``([^`]+)``", r"`\1`", text)
            out.append(text)
        else:
            if out and out[-1] != "":
                out.append("")
        i += 1

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    body = fix_numbered_lists(body)
    body = body.replace("`api/draft?slug=`<slug>``", "`api/draft?slug={slug}`")
    return body


def copy_images_for_page(rst_file: Path, md_file: Path) -> None:
    rst_dir = rst_file.parent
    md_dir = md_file.parent
    for name in ("Images", "images", "_images"):
        src = rst_dir / name
        if not src.is_dir():
            continue
        dst = md_dir / name
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("*.code-workspace", "*.zip"))


def resolve_rst(product: str, entry: str) -> Path | None:
    base = RST_ROOT / product
    p = base / entry
    for c in (p, p.with_suffix(".rst"), p / "Index.rst"):
        if c.is_file():
            return c
    if p.is_dir() and (p / "Index.rst").is_file():
        return p / "Index.rst"
    return None


def resolve_rst_from(base_dir: Path, entry: str) -> Path | None:
    entry = entry.strip()
    if not entry:
        return None
    p = base_dir / entry
    for c in (p.with_suffix(".rst"), p / "Index.rst", p):
        if c.is_file():
            return c
    # tolerate source typos like "HelpSupport/Indexs"
    if entry.endswith("s"):
        return resolve_rst_from(base_dir, entry[:-1])
    return None


def nav_pages_for_product(product: str) -> list[str]:
    index = RST_ROOT / product / "Index.rst"
    if not index.exists():
        return []
    pages: list[str] = []
    visited: set[str] = set()

    def walk(rst: Path) -> None:
        slug = md_slug(rst)
        if slug in visited:
            return
        visited.add(slug)
        pages.append(slug)
        try:
            content = rst.read_text(encoding="utf-8").replace("\ufeff", "")
        except Exception:
            return
        for entry in parse_toctree(content):
            child = resolve_rst_from(rst.parent, entry)
            if child:
                walk(child)

    walk(index)

    # Include any real pages under the product not reachable via toctree (source orphans),
    # so nothing is hidden from the sidebar. Skip artifact ".zip" folders.
    for rst in sorted((RST_ROOT / product).rglob("Index.rst")):
        if any(part.endswith(".zip") for part in rst.parts):
            continue
        slug = md_slug(rst)
        if slug not in visited:
            visited.add(slug)
            pages.append(slug)
    return pages


def build_landing_list(index_rst: Path, toc: list[str]) -> str:
    """Generate a card-style link list for a toctree-only landing page."""
    base = index_rst.parent
    items: list[str] = []
    for entry in toc:
        entry = entry.strip()
        if not entry:
            continue
        p = base / entry
        child = None
        for c in (p.with_suffix(".rst"), p / "Index.rst", p):
            if c.is_file():
                child = c
                break
        if child is None:
            continue
        try:
            title = title_from_content(child.read_text(encoding="utf-8").replace("\ufeff", ""))
        except Exception:
            title = entry.replace("/Index", "").replace("/", " ")
        slug = "/" + md_slug(child)
        items.append(f'  <Card title="{title}" href="{slug}" />')
    if not items:
        return ""
    return "<CardGroup cols={2}>\n" + "\n".join(items) + "\n</CardGroup>"


def convert_rst(rst_file: Path, link_map: dict[str, str]) -> None:
    if rst_file.name == "Includes.txt":
        return
    content = rst_file.read_text(encoding="utf-8").replace("\ufeff", "")
    roles, lines = parse_role_images(content.splitlines())
    title = title_from_content(content)
    body = convert_body(lines, roles)

    # Landing pages: source only has a toctree (no prose) -> generate a link list.
    toc = parse_toctree(content)
    if toc:
        prose = "\n".join(
            ln for ln in body.splitlines()
            if ln.strip()
            and not ln.lstrip().startswith("#")
            and not re.match(r"^[=\-~^`#'\"]{3,}$", ln.strip())
        ).strip()
        if len(prose) < 40:
            body = (body.rstrip() + "\n\n" + build_landing_list(rst_file, toc)).strip()

    md_file = rst_path_to_md(rst_file)
    md_file.parent.mkdir(parents=True, exist_ok=True)
    safe_title = title.replace('"', '\\"')
    md_file.write_text(f'---\ntitle: "{safe_title}"\n---\n\n{body}\n', encoding="utf-8")
    copy_images_for_page(rst_file, md_file)

    slug = f"/{md_slug(rst_file)}"
    rel = rst_file.relative_to(RST_ROOT)
    path_no_ext = str(rel).replace(".rst", "")
    for prefix in ("/en/latest", ""):
        link_map[f"{prefix}/{path_no_ext}/Index.html"] = slug
        link_map[f"{prefix}/{path_no_ext}.html"] = slug
        if path_no_ext.endswith("/Index"):
            base = path_no_ext[: -len("/Index")]
            link_map[f"{prefix}/{base}/Index.html"] = slug


def rewrite_links(link_map: dict[str, str]) -> None:
    for md in OUT_ROOT.rglob("*.md"):
        if md.parts[0] == "scripts" or md.parts[0] == "de":
            continue
        text = md.read_text(encoding="utf-8")
        orig = text
        for old, new in sorted(link_map.items(), key=lambda x: -len(x[0])):
            if old:
                text = text.replace(f"https://docs.t3planet.de{old}", new)
                text = text.replace(f"http://docs.t3planet.de{old}", new)
        if text != orig:
            md.write_text(text, encoding="utf-8")


def product_title(product: str) -> str:
    idx = RST_ROOT / product / "Index.rst"
    if idx.exists():
        return title_from_content(idx.read_text(encoding="utf-8"))
    return product


def build_en_navigation() -> list[dict]:
    root_index = RST_ROOT / "index.rst"
    products = parse_toctree(root_index.read_text(encoding="utf-8"))
    groups = [{"group": "Welcome", "pages": ["index"]}]
    for product_entry in products:
        product_name = product_entry.replace("/Index", "").strip()
        if not (RST_ROOT / product_name).is_dir():
            continue
        pages = nav_pages_for_product(product_name)
        if not pages:
            continue
        groups.append({
            "group": product_title(product_name),
            "icon": "grip-vertical",
            "pages": pages,
        })
    return groups


def sync_all_images() -> None:
    for images_dir in RST_ROOT.rglob("Images"):
        if "_build" in images_dir.parts:
            continue
        rel = images_dir.relative_to(RST_ROOT)
        dst = OUT_ROOT / rel
        dst.mkdir(parents=True, exist_ok=True)
        for f in images_dir.rglob("*"):
            if f.is_file() and f.suffix.lower() in IMAGE_EXT:
                target = dst / f.relative_to(images_dir)
                target.parent.mkdir(parents=True, exist_ok=True)
                if not target.exists():
                    shutil.copy2(f, target)


def create_homepage() -> None:
    content = """---
title: "T3Planet Documentation"
description: "Official documentation for T3Planet TYPO3 extensions, templates, and license guides."
---

Welcome to the T3Planet documentation. Use the sidebar to browse all products in the same order as the original documentation at [docs.t3planet.de](https://docs.t3planet.de/en/latest/).

## Browse Documentation

Select any product from the sidebar. Each parent section can be expanded to view all pages for that extension, template, or guide.
"""
    (OUT_ROOT / "index.md").write_text(content, encoding="utf-8")


def fix_numbered_lists(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    n = 0
    for line in lines:
        if line.startswith("__RSTOL__"):
            n += 1
            out.append(f"{n}. {line[len('__RSTOL__'):]}")
        else:
            if line.strip() == "":
                n = 0
            out.append(line)
    return "\n".join(out)


def setup_german_mirror() -> None:
    de_root = OUT_ROOT / "de"
    if de_root.exists():
        shutil.rmtree(de_root)
    for md in OUT_ROOT.rglob("*.md"):
        if "scripts" in md.parts or "de" in md.parts:
            continue
        rel = md.relative_to(OUT_ROOT)
        target = de_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(md, target)

    de_index = de_root / "index.md"
    de_index.write_text("""---
title: "T3Planet Dokumentation"
description: "Offizielle Dokumentation für T3Planet TYPO3 Erweiterungen, Templates und Lizenzleitfäden."
---

Willkommen in der T3Planet-Dokumentation. Wählen Sie ein Produkt in der Seitenleiste aus.

> **Hinweis:** Die deutsche Übersetzung wird derzeit eingeführt. Inhalte entsprechen vorübergehend der englischen Version, bis vollständige DE-Übersetzungen verfügbar sind.
""", encoding="utf-8")


def build_de_navigation() -> list[dict]:
    en = build_en_navigation()
    de_groups = []
    for g in en:
        pages = [f"de/{p}" if p != "index" else "de/index" for p in g.get("pages", [])]
        de_groups.append({**g, "pages": pages})
    return de_groups


AI_PRODUCTS = {"ExtNsT3AI", "ExtNsT3AS", "ExtNsT3AC", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB"}
TEMPLATE_PRODUCTS = {
    "EXTAvatar", "EXTAyu", "EXTBootstrap", "EXTKarma", "EXTReactBootstrap",
    "EXTReva", "EXTShiva", "EXTShop", "ExtThemes",
}


def product_icon(product: str) -> str:
    if product == "License":
        return "key"
    if product in AI_PRODUCTS:
        return "robot"
    if product in TEMPLATE_PRODUCTS:
        return "palette"
    return "puzzle-piece"


def build_dropdowns(prefix: str = "") -> list[dict]:
    """Each product becomes a dropdown (drill-down). prefix '' for en, 'de/' for de."""
    root_index = RST_ROOT / "index.rst"
    products = parse_toctree(root_index.read_text(encoding="utf-8"))

    def pfx(slug: str) -> str:
        return f"{prefix}{slug}"

    dropdowns = [{
        "dropdown": "Home",
        "icon": "house",
        "pages": [pfx("index")],
    }]

    for product_entry in products:
        product_name = product_entry.replace("/Index", "").strip()
        if not (RST_ROOT / product_name).is_dir():
            continue
        pages = nav_pages_for_product(product_name)
        if not pages:
            continue
        dropdowns.append({
            "dropdown": product_title(product_name),
            "icon": product_icon(product_name),
            "groups": [{
                "group": product_title(product_name),
                "pages": [pfx(p) for p in pages],
            }],
        })
    return dropdowns


def cleanup_old_structure() -> None:
    keep = {"scripts", "de", "_static", "logo", ".git"}
    for item in OUT_ROOT.iterdir():
        if item.name in keep or item.name.startswith("."):
            if item.name == "index.mdx":
                item.unlink()
            continue
        if item.is_dir():
            shutil.rmtree(item)
        elif item.suffix in {".mdx", ".md", ".json", ".png"} and item.name not in {"docs.json", "migration-report.json"}:
            item.unlink()
    for mdx in OUT_ROOT.rglob("*.mdx"):
        mdx.unlink()


def main() -> None:
    print("Cleaning old migration output...")
    cleanup_old_structure()

    products_with_index = sorted(
        p.name for p in RST_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith("_") and p.name != "docs" and (p / "Index.rst").exists()
    )
    print(f"Migrating {len(products_with_index)} products...")

    link_map: dict[str, str] = {}
    converted = 0
    for rst in sorted(RST_ROOT.rglob("*.rst")):
        if "_build" in rst.parts or rst.name == "Includes.txt":
            continue
        if any(part.endswith(".zip") for part in rst.parts):
            continue
        if rst.parent == RST_ROOT and rst.name in {"history.rst", "readme.rst"}:
            continue
        convert_rst(rst, link_map)
        converted += 1

    create_homepage()
    rewrite_links(link_map)
    sync_all_images()
    setup_german_mirror()

    logo_src = RST_ROOT / "_static"
    logo_dst = OUT_ROOT / "_static"
    if logo_src.exists():
        shutil.copytree(logo_src, logo_dst, dirs_exist_ok=True)

    docs = {
        "$schema": "https://mintlify.com/docs.json",
        "name": "T3Planet Docs",
        "theme": "mint",
        "logo": {
            "light": "/_static/t3planet-light.svg",
            "dark": "/_static/t3planet-white-logo.svg",
        },
        "favicon": "/_static/favicon.png",
        "colors": {"primary": "#f49700", "light": "#fff8ee", "dark": "#c97800"},
        "navbar": {
            "links": [
                {"label": "T3Planet", "href": "https://t3planet.de/en/"},
                {"label": "Support", "href": "https://t3planet.de/en/support"},
            ],
            "primary": {
                "type": "button",
                "label": "Browse Extensions",
                "href": "https://t3planet.de/en/typo3-extensions",
            },
        },
        "navigation": {
            "languages": [
                {
                    "language": "en",
                    "default": True,
                    "dropdowns": build_dropdowns(""),
                    "navbar": {
                        "links": [
                            {"label": "T3Planet", "href": "https://t3planet.de/en/"},
                            {"label": "Support", "href": "https://t3planet.de/en/support"},
                        ],
                        "primary": {
                            "type": "button",
                            "label": "Browse Extensions",
                            "href": "https://t3planet.de/en/typo3-extensions",
                        },
                    },
                },
                {
                    "language": "de",
                    "dropdowns": build_dropdowns("de/"),
                    "navbar": {
                        "links": [
                            {"label": "T3Planet", "href": "https://t3planet.de/"},
                            {"label": "Support", "href": "https://t3planet.de/support"},
                        ],
                        "primary": {
                            "type": "button",
                            "label": "Erweiterungen durchsuchen",
                            "href": "https://t3planet.de/typo3-extensions",
                        },
                    },
                },
            ],
        },
        "redirects": [
            {"source": "/en/latest/:path*", "destination": "/:path*"},
        ],
    }

    light_src = OUT_ROOT / "logo" / "t3planet-light.svg"
    if not light_src.exists():
        import urllib.request
        try:
            urllib.request.urlretrieve(
                "https://t3planet.de/fileadmin/images/logo.svg",
                logo_dst / "t3planet-light.svg",
            )
        except Exception:
            shutil.copy2(logo_dst / "t3planet-white-logo.svg", logo_dst / "t3planet-light.svg")
    else:
        shutil.copy2(light_src, logo_dst / "t3planet-light.svg")

    (OUT_ROOT / "docs.json").write_text(json.dumps(docs, indent=2), encoding="utf-8")

    report = {
        "converted_rst": converted,
        "products": len(products_with_index),
        "md_files": len(list(OUT_ROOT.rglob("*.md"))),
        "link_mappings": len(link_map),
    }
    (OUT_ROOT / "migration-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
