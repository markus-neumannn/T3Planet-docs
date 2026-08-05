#!/usr/bin/env python3
"""Convert docs-master-md (MyST/Sphinx markdown) into Mintlify-ready .md, overlaid on docs root."""
from __future__ import annotations

import re
import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import migrate_v2 as mv  # noqa: E402

ROOT = Path("/Users/nitsan/www/Mintilify Doc")
SRC = Path("/Users/nitsan/www/docs-master-md-source-backup/docs")
RST = mv.RST_ROOT

ADMON = {
    "note": "Note", "warning": "Warning", "attention": "Warning",
    "caution": "Warning", "danger": "Warning", "error": "Warning",
    "important": "Info", "seealso": "Info", "admonition": "Note",
    "tip": "Tip", "hint": "Tip",
}

SKIP_BASENAMES = {"readme.md", "history.md"}


def title_from_heading(text: str) -> str | None:
    for line in text.splitlines():
        m = re.match(r"#{1,6}\s+(.+)", line.strip())
        if m:
            return m.group(1).strip()
    return None


def out_slug(child: Path) -> str:
    rel = child.relative_to(SRC).as_posix()
    rel = re.sub(r"\.md$", "", rel)
    return "/" + rel


def build_landing(src_md: Path, toc: list[str]) -> str:
    base = src_md.parent
    items = []
    for entry in toc:
        entry = entry.strip()
        if not entry:
            continue
        child = None
        for c in (base / f"{entry}.md", base / entry / "Index.md", base / entry / "index.md"):
            if c.is_file():
                child = c
                break
        if child is None:
            continue
        t = title_from_heading(child.read_text(encoding="utf-8")) or entry.split("/")[-1]
        items.append(f'  <Card title="{t}" href="{out_slug(child)}" />')
    if not items:
        return ""
    return "<CardGroup cols={2}>\n" + "\n".join(items) + "\n</CardGroup>"


def handle_eval_rst(inner: list[str], src_md: Path) -> str:
    content = "\n".join(inner)
    toc = mv.parse_toctree(content)
    if toc:
        return build_landing(src_md, toc)
    # other RST (list-table, rst-class, figures) -> reuse the RST converter
    roles, lines = mv.parse_role_images(inner)
    return mv.convert_body(lines, roles)


def process_lines(lines: list[str], src_md: Path, depth: int = 0) -> str:
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        # bare RST include / labels / comments
        if re.match(r"\.\.\s+include::", s) or re.match(r"\.\.\s+_[\w-]+:\s*$", s):
            i += 1
            continue

        # fenced directive: ```{name} arg
        mf = re.match(r"`{3,}\{([a-zA-Z-]+)\}(.*)$", s)
        if mf:
            name = mf.group(1).lower()
            arg = mf.group(2).strip()
            j = i + 1
            inner = []
            while j < n and not re.match(r"`{3,}\s*$", lines[j].strip()):
                inner.append(lines[j])
                j += 1
            i = j + 1
            if name == "include":
                continue
            if name == "raw":
                out.append("\n".join(inner))
            elif name == "eval-rst":
                out.append(handle_eval_rst(inner, src_md))
            elif name == "image":
                if arg:
                    out.append(f"![]({arg})")
            else:
                out.append("\n".join(inner))
            out.append("")
            continue

        # colon-fence directive: :::{name} arg
        mc = re.match(r":{3,}\{([a-zA-Z-]+)\}(.*)$", s)
        if mc:
            name = mc.group(1).lower()
            arg = mc.group(2).strip()
            j = i + 1
            inner = []
            d = 1
            while j < n:
                t = lines[j].strip()
                if re.match(r":{3,}\{[a-zA-Z-]+\}", t):
                    d += 1
                elif re.match(r":{3,}\s*$", t):
                    d -= 1
                    if d == 0:
                        break
                inner.append(lines[j])
                j += 1
            i = j + 1

            if name == "figure" or name == "image":
                alt = ""
                for opt in inner:
                    am = re.match(r":alt:\s*(.+)", opt.strip())
                    if am:
                        alt = am.group(1).strip()
                        break
                out.append(f"![{alt}]({arg})")
                out.append("")
            else:
                comp = ADMON.get(name, "Note")
                # strip option lines like :class: at top of admonition body
                body_lines = [l for l in inner if not re.match(r":[a-zA-Z-]+:", l.strip())]
                inner_md = process_lines(body_lines, src_md, depth + 1).strip()
                out.append(f"<{comp}>\n\n{inner_md}\n\n</{comp}>")
                out.append("")
            continue

        out.append(line)
        i += 1
    return "\n".join(out)


def convert_file(src_md: Path) -> tuple[str, str]:
    raw = src_md.read_text(encoding="utf-8").replace("\ufeff", "")
    fm_title = None
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            fmatch = re.search(r"title:\s*(.+)", parts[1])
            if fmatch:
                fm_title = fmatch.group(1).strip().strip('"')
            raw = parts[2]
    title = fm_title or title_from_heading(raw) or "Documentation"
    body = process_lines(raw.split("\n"), src_md)
    # Drop a leading H1 (frontmatter title renders as the page heading)
    body = re.sub(r"^\s*#\s+.+?(\n|$)", "", body, count=1)
    body = re.sub(r"\n{3,}", "\n\n", body).strip()
    return title, body


def main() -> None:
    converted = 0
    for src_md in sorted(SRC.rglob("*.md")):
        if src_md.name.lower() in SKIP_BASENAMES:
            continue
        if any(p.endswith(".zip") for p in src_md.parts):
            continue
        rel = src_md.relative_to(SRC)
        # normalize lowercase index.md (non-root) -> Index.md to match nav
        rel_parts = list(rel.parts)
        if rel_parts[-1] == "index.md" and len(rel_parts) > 1:
            rel_parts[-1] = "Index.md"
        rel = Path(*rel_parts)

        title, body = convert_file(src_md)
        dst = ROOT / rel

        # Master file empty/blank -> fall back to converting the original RST source
        if not body.strip():
            rst_equiv = RST / rel.with_suffix(".rst").as_posix()
            if rst_equiv.is_file():
                mv.convert_rst(rst_equiv, {})
                converted += 1
                continue

        dst.parent.mkdir(parents=True, exist_ok=True)
        safe = title.replace('"', '\\"')
        dst.write_text(f'---\ntitle: "{safe}"\n---\n\n{body}\n', encoding="utf-8")
        converted += 1

    # homepage from master index.md if present
    home = SRC / "index.md"
    if home.exists():
        title, body = convert_file(home)
        (ROOT / "index.md").write_text(
            f'---\ntitle: "{title}"\n---\n\n{body}\n', encoding="utf-8"
        )

    print(f"Converted {converted} master files")


if __name__ == "__main__":
    main()
