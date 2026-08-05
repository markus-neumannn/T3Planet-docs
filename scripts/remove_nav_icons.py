#!/usr/bin/env python3
"""Remove icon frontmatter from documentation pages (sidebar subsection icons)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)
ICON_RE = re.compile(r"^icon:\s*.+(?:\n|$)", re.M)


def main() -> None:
    removed = 0
    for md in ROOT.rglob("*.md"):
        if "scripts" in md.parts or ".venv" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        if not m or not ICON_RE.search(m.group(1)):
            continue
        fm = ICON_RE.sub("", m.group(1))
        new_text = f"---\n{fm}---" + text[m.end() :]
        md.write_text(new_text, encoding="utf-8")
        removed += 1
    print(f"Removed icon from {removed} files")


if __name__ == "__main__":
    main()
