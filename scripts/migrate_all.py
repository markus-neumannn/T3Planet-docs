#!/usr/bin/env python3
"""Full T3Planet Sphinx RST -> Mintlify migration pipeline."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from rst_to_mdx import (
    ADMONITION_MAP,
    OUT_ROOT,
    RST_ROOT,
    build_nav_pages,
    collect_products,
    convert_body,
    convert_index_file,
    copy_images,
    page_slug,
    parse_toctree,
    product_slug,
    title_from_content,
)

AI_PRODUCTS = {
    "ExtNsT3AI", "ExtNsT3AS", "ExtNsT3AC", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB",
}
TEMPLATE_PRODUCTS = {
    "EXTAvatar", "EXTAyu", "EXTBootstrap", "EXTKarma", "EXTReactBootstrap",
    "EXTReva", "EXTShiva", "EXTShop", "ExtThemes",
}
PRIORITY_EXTENSIONS = {
    "ExtRTECKEditorPack", "ExtNsNewsComments", "ExtNsRevolutionSlider",
}

PRODUCT_DISPLAY_NAMES = {
    "License": "License, Installation & Updates",
    "ExtNsT3AI": "T3AI",
    "ExtNsT3AS": "T3AS",
    "ExtNsT3AC": "T3AC",
    "ExtNsT3AL": "T3AL",
    "ExtNsT3AA": "T3AA",
    "ExtNsT3AB": "T3AB",
    "ExtRTECKEditorPack": "CKEditor Pack",
    "EXTKarma": "T3 Karma",
    "EXTBootstrap": "T3 Bootstrap",
    "EXTAyu": "T3 Ayu",
    "EXTReva": "T3 Reva",
    "EXTShiva": "T3 Shiva",
    "EXTAvatar": "T3 Avatar",
    "EXTReactBootstrap": "T3 React Bootstrap",
    "EXTShop": "T3 Shop",
    "ExtThemes": "TYPO3 Themes",
    "EXTNsZohoCrm": "Zoho CRM",
}


def camel_to_kebab(name: str) -> str:
    name = name.replace("&", "-and-")
    return re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name).lower()


def display_name(product: str) -> str:
    if product in PRODUCT_DISPLAY_NAMES:
        return PRODUCT_DISPLAY_NAMES[product]
    if product.startswith("ExtNs"):
        return product[5:]
    if product.startswith("ExtNitsan"):
        return product[9:]
    if product.startswith("EXT"):
        return product[3:]
    return product


def needs_mdx(body: str) -> bool:
    return any(
        tag in body
        for tag in ("<Note>", "<Warning>", "<Tip>", "<Info>", "<div", "<iframe", "<style")
    )


def rst_to_old_url_paths(product: str, rst_path: Path) -> list[str]:
    rel = rst_path.relative_to(RST_ROOT / product)
    parts = list(rel.parts)
    stem = parts[-1].replace(".rst", "")
    if stem in {"Index", "Support", "BuyNow", "GetThisExtension"}:
        parts = parts[:-1]
    else:
        parts[-1] = stem

    paths = []
    if parts:
        joined = "/".join(parts)
        paths.append(f"/en/latest/{product}/{joined}/Index.html")
        paths.append(f"/en/latest/{product}/{joined}.html")
    paths.append(f"/en/latest/{product}/Index.html")
    return paths


def convert_list_table(lines: list[str], start: int) -> tuple[str, int]:
    title = ""
    header_rows = 0
    i = start + 1
    while i < len(lines) and lines[i].startswith("   :"):
        opt = lines[i].strip()
        if opt.startswith(":header-rows:"):
            header_rows = int(opt.split(":")[-1].strip())
        if opt.startswith(".. list-table::"):
            title = opt.split("::", 1)[1].strip()
        i += 1

    rows: list[list[str]] = []
    current: list[str] = []
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith(".. ") and not line.strip().startswith("* "):
            break
        if line.strip().startswith("* -"):
            if current:
                rows.append(current)
            cell = line.strip()[3:].strip()
            current = [cell]
        elif line.strip().startswith("- ") and current:
            current.append(line.strip()[2:].strip())
        elif not line.strip() and rows:
            break
        i += 1
    if current:
        rows.append(current)

    if not rows:
        return "", start + 1

    md: list[str] = []
    if title:
        md.append(f"### {title}")
        md.append("")

    for ri, row in enumerate(rows):
        if ri == 0 and header_rows:
            md.append("| " + " | ".join(row) + " |")
            md.append("| " + " | ".join("---" for _ in row) + " |")
        else:
            md.append("| " + " | ".join(row) + " |")
    md.append("")
    return "\n".join(md), i


def convert_body_enhanced(rst_text: str, rst_file: Path) -> str:
    lines = rst_text.splitlines()
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
            table_md, i = convert_list_table(lines, i)
            out.append(table_md)
            continue

        if stripped.startswith(".. image::"):
            img = stripped.split("::", 1)[1].strip()
            alt = ""
            i += 1
            while i < len(lines) and lines[i].startswith("   :"):
                if ":alt:" in lines[i]:
                    alt = lines[i].split(":", 2)[-1].strip()
                i += 1
            out.append(f"![{alt or 'image'}]({img})")
            out.append("")
            continue

        if i + 1 < len(lines) and re.match(r"^[=\-~^`#'\"]+$", lines[i + 1].strip()) and stripped:
            level_char = lines[i + 1].strip()[0]
            level = {"=": 1, "-": 2, "~": 3, "^": 4, "`": 5}.get(level_char, 2)
            out.append(f"{'#' * min(level, 4)} {stripped}")
            out.append("")
            i += 2
            continue

        if stripped.startswith(".. figure::"):
            img = stripped.split("::", 1)[1].strip()
            alt = ""
            i += 1
            while i < len(lines) and lines[i].startswith("   :"):
                if ":alt:" in lines[i]:
                    alt = lines[i].split(":", 2)[-1].strip()
                i += 1
            out.append(f"![{alt or 'image'}]({img})")
            out.append("")
            continue

        admonition_match = re.match(r"\.\.\s+(\w+)::\s*$", stripped)
        if admonition_match and admonition_match.group(1) in ADMONITION_MAP:
            tag = ADMONITION_MAP[admonition_match.group(1)]
            i += 1
            body_lines: list[str] = []
            while i < len(lines):
                if lines[i].startswith("   ") or lines[i].strip() == "":
                    body_lines.append(lines[i][3:] if lines[i].startswith("   ") else "")
                    i += 1
                else:
                    break
            body = "\n".join(body_lines).strip()
            out.append(f"<{tag}>")
            out.append(body)
            out.append(f"</{tag}>")
            out.append("")
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
            if lang == "python" and "composer" in "\n".join(lines[i : i + 10]).lower():
                lang = "bash"
            i += 1
            code_lines: list[str] = []
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                code_lines.append(lines[i][3:] if lines[i].startswith("   ") else "")
                i += 1
            out.append(f"```{lang}")
            out.extend(code_lines)
            out.append("```")
            out.append("")
            continue

        if stripped.startswith("|"):
            out.append(stripped)
            i += 1
            continue

        if stripped.startswith(".. ") and not stripped.startswith(".. |"):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
            continue

        if re.match(r"^#\.\s+", stripped):
            out.append(stripped)
            i += 1
            continue

        if stripped:
            text = stripped
            text = re.sub(r"`([^<`]+)\s*<([^>]+)>`_", r"[\1](\2)", text)
            text = re.sub(r"``([^`]+)``", r"`\1`", text)
            text = re.sub(r"`([^`]+)`", r"`\1`", text)
            out.append(text)
        else:
            if out and out[-1] != "":
                out.append("")
        i += 1

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def output_path(product: str, rst_path: Path, ext: str) -> Path:
    base = OUT_ROOT / product_slug(product)
    slug = page_slug(rst_path, RST_ROOT / product)
    return base / f"{slug}.{ext}"


def convert_rst_file(rst_file: Path, product: str, link_map: dict[str, str]) -> dict | None:
    if rst_file.name == "Includes.txt":
        return None

    if rst_file.name == "Index.rst" and rst_file.parent == RST_ROOT / product:
        return convert_index_file_enhanced(rst_file, product, link_map)

    content = rst_file.read_text(encoding="utf-8")
    title = title_from_content(content)
    body = convert_body_enhanced(content, rst_file)
    ext = "mdx" if needs_mdx(body) else "md"
    out_path = output_path(product, rst_file, ext)

    frontmatter = f"---\ntitle: {json.dumps(title)[1:-1]}\n---\n\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(frontmatter + body + "\n", encoding="utf-8")
    copy_images(rst_file, out_path)

    slug = str(out_path.relative_to(OUT_ROOT)).rsplit(".", 1)[0]
    for old_path in rst_to_old_url_paths(product, rst_file):
        link_map[old_path] = f"/{slug}"

    return {
        "rst": str(rst_file.relative_to(RST_ROOT)),
        "output": str(out_path.relative_to(OUT_ROOT)),
        "slug": slug,
        "title": title,
        "format": ext,
    }


def convert_index_file_enhanced(rst_file: Path, product: str, link_map: dict[str, str]) -> dict:
    content = rst_file.read_text(encoding="utf-8")
    title = title_from_content(content)
    entries = parse_toctree(content)
    base_slug = product_slug(product)

    body_lines = [f"# {title}", ""]
    if entries:
        body_lines.append("Browse the sections in the sidebar, or jump to:")
        body_lines.append("")
        for entry in entries:
            rst = resolve_rst_for_entry(product, entry)
            if rst:
                slug = page_slug(rst, RST_ROOT / product)
                label = slug.split("/")[-1].replace("-", " ").title()
                body_lines.append(f"- [{label}](/{base_slug}/{slug})")
            else:
                name = entry.split("/")[-1].replace("Index", "").strip("/") or entry
                body_lines.append(f"- {name}")

    out_path = OUT_ROOT / base_slug / "index.mdx"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"---\ntitle: {json.dumps(title)[1:-1]}\n---\n\n" + "\n".join(body_lines) + "\n", encoding="utf-8")

    slug = str(out_path.relative_to(OUT_ROOT)).rsplit(".", 1)[0]
    for old_path in rst_to_old_url_paths(product, rst_file):
        link_map[old_path] = f"/{slug}"

    return {
        "rst": str(rst_file.relative_to(RST_ROOT)),
        "output": str(out_path.relative_to(OUT_ROOT)),
        "slug": slug,
        "title": title,
        "format": "mdx",
        "toctree": entries,
    }


def resolve_rst_for_entry(product: str, entry: str) -> Path | None:
    entry_path = RST_ROOT / product / entry
    for candidate in [entry_path, entry_path.with_suffix(".rst"), entry_path / "Index.rst"]:
        if candidate.is_file():
            return candidate
    if entry_path.is_dir():
        sub = entry_path / "Index.rst"
        if sub.is_file():
            return sub
    return None


def rewrite_links(link_map: dict[str, str]) -> int:
    replacements = 0
    patterns = sorted(link_map.keys(), key=len, reverse=True)

    for path in OUT_ROOT.rglob("*"):
        if path.suffix not in {".md", ".mdx"}:
            continue
        text = path.read_text(encoding="utf-8")
        original = text

        for old in patterns:
            new = link_map[old]
            text = text.replace(f"https://docs.t3planet.de{old}", new)
            text = text.replace(f"http://docs.t3planet.de{old}", new)

        # Generic pattern for any remaining old docs links
        def replace_old_link(match: re.Match) -> str:
            url = match.group(1)
            parsed = re.sub(r"https?://docs\.t3planet\.de", "", url)
            parsed = parsed.split("#")[0]
            if parsed in link_map:
                return f"]({link_map[parsed]})"
            # Try without /Index.html
            alt = re.sub(r"/Index\.html$", ".html", parsed)
            if alt in link_map:
                return f"]({link_map[alt]})"
            return match.group(0)

        text = re.sub(r"\]\((https?://docs\.t3planet\.de[^)]+)\)", replace_old_link, text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            replacements += 1
    return replacements


def categorize_product(product: str) -> str:
    if product == "License":
        return "getting_started"
    if product in AI_PRODUCTS:
        return "ai"
    if product in TEMPLATE_PRODUCTS:
        return "templates"
    return "extensions"


def build_navigation(report: dict) -> dict:
    groups_by_tab: dict[str, list] = {
        "getting_started": [],
        "ai": [],
        "templates": [],
        "extensions": [],
    }

    license_nav = []
    for pdata in report["products"]:
        product = pdata["product"]
        nav = pdata.get("nav") or []
        if not nav:
            continue
        cat = categorize_product(product)
        if product == "License":
            license_nav = nav
            continue
        groups_by_tab[cat].append({
            "group": display_name(product),
            "pages": nav,
        })

    tabs = [
        {
            "tab": "Home",
            "groups": [
                {"group": "Welcome", "pages": ["index"]},
                {"group": "License, Installation & Updates", "pages": license_nav},
            ],
        },
        {
            "tab": "AI Extensions",
            "icon": "robot",
            "groups": sorted(groups_by_tab["ai"], key=lambda g: g["group"]),
        },
        {
            "tab": "Templates",
            "icon": "palette",
            "groups": sorted(groups_by_tab["templates"], key=lambda g: g["group"]),
        },
        {
            "tab": "Extensions",
            "icon": "puzzle-piece",
            "groups": sorted(groups_by_tab["extensions"], key=lambda g: g["group"]),
        },
    ]
    return {"tabs": tabs}


def build_redirects(link_map: dict[str, str]) -> list[dict]:
    redirects = []
    seen = set()
    for source, dest in sorted(link_map.items()):
        if source in seen:
            continue
        seen.add(source)
        redirects.append({"source": source, "destination": dest})
    return redirects


def convert_product(product: str, link_map: dict[str, str]) -> dict:
    product_dir = RST_ROOT / product
    if not product_dir.is_dir():
        return {"product": product, "error": "not found", "pages": [], "nav": []}

    results = []
    for rst_file in sorted(product_dir.rglob("*.rst")):
        if "_build" in rst_file.parts:
            continue
        meta = convert_rst_file(rst_file, product, link_map)
        if meta:
            results.append(meta)

    nav_pages = build_nav_pages(product)
    # Ensure all converted pages appear in nav even if toctree missed them
    converted_slugs = [r["slug"] for r in results]
    for slug in converted_slugs:
        if slug not in nav_pages:
            nav_pages.append(slug)
    nav_pages = sorted(set(nav_pages), key=lambda s: (s.count("/"), s))

    return {
        "product": product,
        "slug": product_slug(product),
        "pages": results,
        "nav": nav_pages,
        "page_count": len(results),
    }


def main() -> None:
    print("=" * 60)
    print("T3Planet Full Documentation Migration")
    print("=" * 60)

    products = [p for p in collect_products(None) if (RST_ROOT / p / "Index.rst").exists()]
    print(f"Products to migrate: {len(products)}")

    link_map: dict[str, str] = {}
    report: dict = {"products": [], "issues": []}

    for product in products:
        print(f"  Converting {product}...", end=" ", flush=True)
        try:
            data = convert_product(product, link_map)
            report["products"].append(data)
            print(f"{data['page_count']} pages -> {data['slug']}/")
        except Exception as exc:
            report["issues"].append({"product": product, "error": str(exc)})
            print(f"ERROR: {exc}")

    print(f"\nRewriting internal links ({len(link_map)} mappings)...")
    rewritten = rewrite_links(link_map)
    print(f"  Updated {rewritten} files")

    print("Generating docs.json...")
    docs = {
        "$schema": "https://mintlify.com/docs.json",
        "name": "T3Planet Docs",
        "theme": "mint",
        "logo": {
            "light": "/logo/t3planet-logo.svg",
            "dark": "/logo/t3planet-logo.svg",
        },
        "favicon": "/logo/favicon.png",
        "colors": {
            "primary": "#f49700",
            "light": "#fff8ee",
            "dark": "#c97800",
        },
        "navbar": {
            "links": [
                {"label": "T3Planet", "href": "https://t3planet.de"},
                {"label": "Support", "href": "https://t3planet.de/support"},
            ],
            "primary": {
                "type": "button",
                "label": "Browse Extensions",
                "href": "https://t3planet.de/typo3-extensions",
            },
        },
        "footer": {
            "socials": {"website": "https://t3planet.de"},
        },
        "navigation": build_navigation(report),
        "redirects": build_redirects(link_map),
    }

    docs_path = OUT_ROOT / "docs.json"
    docs_path.write_text(json.dumps(docs, indent=2), encoding="utf-8")

    report["summary"] = {
        "total_products": len(report["products"]),
        "total_pages": sum(p.get("page_count", 0) for p in report["products"]),
        "md_files": sum(1 for p in report["products"] for pg in p.get("pages", []) if pg.get("format") == "md"),
        "mdx_files": sum(1 for p in report["products"] for pg in p.get("pages", []) if pg.get("format") == "mdx"),
        "link_mappings": len(link_map),
        "files_rewritten": rewritten,
        "redirects": len(docs["redirects"]),
    }

    report_path = OUT_ROOT / "migration-report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n" + "=" * 60)
    print("Migration Complete")
    print(f"  Products:  {report['summary']['total_products']}")
    print(f"  Pages:     {report['summary']['total_pages']}")
    print(f"  .md:       {report['summary']['md_files']}")
    print(f"  .mdx:      {report['summary']['mdx_files']}")
    print(f"  Redirects: {report['summary']['redirects']}")
    if report["issues"]:
        print(f"  Issues:    {len(report['issues'])}")
    print("=" * 60)


if __name__ == "__main__":
    main()
