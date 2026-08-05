#!/usr/bin/env python3
"""
Convert Sphinx RST documentation to Mintlify MDX.

Usage:
  python scripts/rst_to_mdx.py --product License
  python scripts/rst_to_mdx.py --product ExtNsT3AI
  python scripts/rst_to_mdx.py --all
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

RST_ROOT = Path("/Users/nitsan/www/T3Planet Docs/docs/docs")
OUT_ROOT = Path(__file__).resolve().parent.parent

PRODUCT_MAP = {
    "License": "license",
    "ExtNsT3AI": "extensions/ns-t3ai",
    "ExtNsT3AS": "extensions/ns-t3as",
    "ExtNsT3AC": "extensions/ns-t3ac",
    "ExtNsT3AL": "extensions/ns-t3al",
    "ExtNsT3AA": "extensions/ns-t3aa",
    "ExtNsT3AB": "extensions/ns-t3ab",
    "ExtRTECKEditorPack": "extensions/ckeditor-pack",
    "EXTKarma": "templates/t3-karma",
    "EXTBootstrap": "templates/t3-bootstrap",
    "EXTAyu": "templates/t3-ayu",
    "EXTReva": "templates/t3-reva",
    "EXTShiva": "templates/t3-shiva",
    "EXTAvatar": "templates/t3-avatar",
    "EXTReactBootstrap": "templates/t3-react-bootstrap",
    "EXTShop": "templates/t3-shop",
    "ExtThemes": "templates",
}

ADMONITION_MAP = {
    "note": "Note",
    "Note": "Note",
    "attention": "Warning",
    "warning": "Warning",
    "Warning": "Warning",
    "important": "Warning",
    "tip": "Tip",
    "Tip": "Tip",
    "hint": "Tip",
}

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def product_slug(name: str) -> str:
    if name in PRODUCT_MAP:
        return PRODUCT_MAP[name]
    if name.startswith("ExtNs"):
        return "extensions/" + re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name[5:]).lower()
    if name.startswith("EXT"):
        return "extensions/" + re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name[3:]).lower()
    if name.startswith("Ext"):
        return "extensions/" + re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", name[3:]).lower()
    return name.lower()


def page_slug(rst_path: Path, product_dir: Path) -> str:
    rel = rst_path.relative_to(product_dir)
    parts = list(rel.parts)
    if parts[-1] in {"Index.rst", "Support.rst", "BuyNow.rst", "GetThisExtension.rst"}:
        parts = parts[:-1]
    leaf = rel.stem.lower()
    if leaf == "index":
        leaf = parts[-1].lower() if parts else "index"
    elif leaf in {"buynow", "getthisextension"}:
        leaf = "get-this-extension"
    elif leaf == "support":
        leaf = "support"
    else:
        parts = parts[:-1] + [leaf]
    slug = "/".join(p.lower() for p in parts) if parts else leaf
    return slug.replace("_", "-")


def mdx_path(product: str, rst_path: Path) -> Path:
    base = OUT_ROOT / product_slug(product)
    slug = page_slug(rst_path, RST_ROOT / product)
    return base / f"{slug}.mdx"


def parse_toctree(content: str) -> list[str]:
    entries: list[str] = []
    in_toctree = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith(".. toctree::"):
            in_toctree = True
            continue
        if in_toctree:
            if not stripped:
                if entries:
                    break
                continue
            if stripped.startswith(":"):
                continue
            entries.append(stripped)
    return entries


def title_from_content(content: str) -> str:
    lines = [ln.rstrip() for ln in content.splitlines()]
    for i, line in enumerate(lines):
        if i + 1 < len(lines) and re.match(r"^[=\-~^`#'\"]+$", lines[i + 1]) and line.strip():
            return line.strip()
    for line in lines:
        if line.strip() and not line.strip().startswith(".."):
            return line.strip()[:80]
    return "Documentation"


def convert_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"`\1`", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"**\1**", text)
    text = re.sub(r"`([^<`]+)\s*<([^>]+)>`_", r"[\1](\2)", text)
    text = re.sub(r"`([^`]+)`_", r"[\1](\1)", text)
    return text


def convert_body(rst_text: str, rst_file: Path) -> str:
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

        if i + 1 < len(lines) and re.match(r"^[=\-~^`#'\"]+$", lines[i + 1].strip()) and stripped:
            level_char = lines[i + 1].strip()[0]
            level = {"=": 1, "-": 2, "~": 3, "^": 4, "`": 5, "#": 1, '"': 2, "'": 3}.get(level_char, 2)
            heading = convert_inline(stripped)
            out.append(f"{'#' * level} {heading}")
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
            body = "\n".join(convert_inline(ln) for ln in body_lines).strip()
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
            out.append(convert_inline(stripped))
            i += 1
            continue

        if stripped.startswith(".. ") and not stripped.startswith(".. |"):
            i += 1
            while i < len(lines) and (lines[i].startswith("   ") or lines[i].strip() == ""):
                i += 1
            continue

        if stripped:
            out.append(convert_inline(line.rstrip()))
        else:
            if out and out[-1] != "":
                out.append("")
        i += 1

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def _copy_image_tree(src: Path, dst: Path) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            _copy_image_tree(item, target)
        elif item.suffix.lower() in IMAGE_EXT:
            shutil.copy2(item, target)


def copy_images(rst_file: Path, mdx_out: Path) -> None:
    rst_dir = rst_file.parent
    mdx_dir = mdx_out.parent
    for img_dir_name in ("Images", "images", "_images"):
        src_img_dir = rst_dir / img_dir_name
        if src_img_dir.is_dir():
            dst = mdx_dir / img_dir_name
            if dst.exists():
                shutil.rmtree(dst)
            _copy_image_tree(src_img_dir, dst)


def convert_rst_file(rst_file: Path, product: str) -> dict | None:
    if rst_file.name == "Includes.txt":
        return None
    if rst_file.name == "Index.rst" and rst_file.parent == RST_ROOT / product:
        return convert_index_file(rst_file, product)

    content = rst_file.read_text(encoding="utf-8")
    title = title_from_content(content)
    body = convert_body(content, rst_file)
    out_path = mdx_path(product, rst_file)

    frontmatter = f"---\ntitle: {title}\n---\n\n"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(frontmatter + body + "\n", encoding="utf-8")
    copy_images(rst_file, out_path)

    return {
        "rst": str(rst_file.relative_to(RST_ROOT)),
        "mdx": str(out_path.relative_to(OUT_ROOT)),
        "slug": str(out_path.relative_to(OUT_ROOT)).replace(".mdx", ""),
        "title": title,
    }


def convert_index_file(rst_file: Path, product: str) -> dict:
    content = rst_file.read_text(encoding="utf-8")
    title = title_from_content(content)
    entries = parse_toctree(content)
    body_lines = [f"# {title}", ""]
    if entries:
        body_lines.append("Browse the sections in the sidebar, or jump to:")
        body_lines.append("")
        for entry in entries:
            name = entry.split("/")[-1].replace(".rst", "").replace("Index", "").strip("/") or entry
            slug_part = name.lower().replace("_", "-")
            body_lines.append(f"- [{name}](./{slug_part})")
    body = "\n".join(body_lines)
    out_path = OUT_ROOT / product_slug(product) / "index.mdx"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(f"---\ntitle: {title}\n---\n\n{body}\n", encoding="utf-8")
    return {
        "rst": str(rst_file.relative_to(RST_ROOT)),
        "mdx": str(out_path.relative_to(OUT_ROOT)),
        "slug": str(out_path.relative_to(OUT_ROOT)).replace(".mdx", ""),
        "title": title,
        "toctree": entries,
    }


def collect_products(selected: list[str] | None) -> list[str]:
    if selected:
        return selected
    return sorted(
        p.name
        for p in RST_ROOT.iterdir()
        if p.is_dir() and not p.name.startswith("_") and p.name != "docs"
    )


def build_nav_pages(product: str) -> list[str]:
    index_rst = RST_ROOT / product / "Index.rst"
    if not index_rst.exists():
        return []
    entries = parse_toctree(index_rst.read_text(encoding="utf-8"))
    pages: list[str] = [f"{product_slug(product)}/index"]
    base = product_slug(product)

    def resolve_rst_file(entry: str) -> Path | None:
        entry_path = RST_ROOT / product / entry
        candidates = [
            entry_path,
            entry_path.with_suffix(".rst"),
            entry_path / "Index.rst",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        if entry_path.is_dir():
            sub_index = entry_path / "Index.rst"
            if sub_index.is_file():
                return sub_index
        return None

    def resolve_entry(entry: str) -> list[str]:
        entry_path = RST_ROOT / product / entry
        if entry_path.is_dir():
            sub_index = entry_path / "Index.rst"
            if sub_index.exists():
                sub_entries = parse_toctree(sub_index.read_text(encoding="utf-8"))
                if sub_entries:
                    result = []
                    for sub in sub_entries:
                        result.extend(resolve_entry(str(Path(entry) / sub)))
                    return result

        rst_file = resolve_rst_file(entry)
        if not rst_file:
            return []

        slug = page_slug(rst_file, RST_ROOT / product)
        return [f"{base}/{slug}"]

    for entry in entries:
        pages.extend(resolve_entry(entry))

    seen = set()
    unique = []
    for p in pages:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    return unique


def convert_product(product: str) -> dict:
    product_dir = RST_ROOT / product
    if not product_dir.is_dir():
        raise FileNotFoundError(f"Product not found: {product}")

    results = []
    for rst_file in sorted(product_dir.rglob("*.rst")):
        if "_build" in rst_file.parts:
            continue
        meta = convert_rst_file(rst_file, product)
        if meta:
            results.append(meta)

    nav_pages = build_nav_pages(product)
    return {"product": product, "slug": product_slug(product), "pages": results, "nav": nav_pages}


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert Sphinx RST to Mintlify MDX")
    parser.add_argument("--product", action="append", help="Product folder name (e.g. License, ExtNsT3AI)")
    parser.add_argument("--all", action="store_true", help="Convert all products")
    parser.add_argument("--report", default="migration-report.json", help="Output report path")
    args = parser.parse_args()

    if args.all:
        products = collect_products(None)
    elif args.product:
        products = args.product
    else:
        products = ["License", "ExtNsT3AI"]

    report = {"products": [], "summary": {}}
    for product in products:
        print(f"Converting {product}...")
        data = convert_product(product)
        report["products"].append(data)
        print(f"  -> {len(data['pages'])} pages -> {data['slug']}/")

    report["summary"] = {
        "total_products": len(report["products"]),
        "total_pages": sum(len(p["pages"]) for p in report["products"]),
    }

    report_path = OUT_ROOT / args.report
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nReport written to {report_path}")


if __name__ == "__main__":
    main()
