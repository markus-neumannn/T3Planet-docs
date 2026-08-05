#!/usr/bin/env python3
"""Fix migrated content: heading hierarchy, RST numbered lists, inline code."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fix_numbered_lists(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    counter = 0
    in_list = False

    for line in lines:
        if re.match(r"^#\.\s+", line):
            counter += 1
            in_list = True
            content = re.sub(r"^#\.\s+", "", line)
            content = re.sub(r"``([^`]+)``", r"`\1`", content)
            out.append(f"{counter}. {content}")
        elif in_list and line.strip() == "":
            in_list = False
            counter = 0
            out.append(line)
        elif in_list and not line.startswith(" "):
            in_list = False
            counter = 0
            out.append(line)
        else:
            out.append(line)
    return "\n".join(out)


def fix_headings(body: str, title: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    first_heading_skipped = False

    for line in lines:
        if line.startswith("# ") and not first_heading_skipped:
            heading_text = line[2:].strip()
            if heading_text.lower() == title.lower():
                first_heading_skipped = True
                continue
        if line.startswith("# "):
            out.append("## " + line[2:])
        elif line.startswith("## "):
            out.append("### " + line[3:])
        elif line.startswith("### "):
            out.append("#### " + line[4:])
        else:
            out.append(line)
    return "\n".join(out)


def fix_inline_code(text: str) -> str:
    return re.sub(r"``([^`]+)``", r"`\1`", text)


def fix_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    if not original.startswith("---"):
        return False

    parts = original.split("---", 2)
    if len(parts) < 3:
        return False

    frontmatter = f"---{parts[1]}---"
    body = parts[2]

    title_match = re.search(r"^title:\s*(.+)$", parts[1], re.MULTILINE)
    title = title_match.group(1).strip().strip('"') if title_match else ""

    body = fix_numbered_lists(body)
    body = fix_inline_code(body)
    if title:
        body = fix_headings(body, title)

    new_text = frontmatter + body
    if not new_text.endswith("\n"):
        new_text += "\n"

    if new_text != original:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    fixed = 0
    for path in ROOT.rglob("*"):
        if path.suffix in {".md", ".mdx"} and "scripts" not in path.parts:
            if fix_file(path):
                fixed += 1
    print(f"Fixed content in {fixed} files")


if __name__ == "__main__":
    main()
