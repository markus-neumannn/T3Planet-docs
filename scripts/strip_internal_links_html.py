#!/usr/bin/env python3
"""Strip .html suffix from internal Mintlify markdown link targets (canonical clean routes)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "node_modules", ".git", ".venv-translate", "de"}

LINK_RE = re.compile(
    r"\]\("
    r"(?P<prefix>/de)?"
    r"(?P<path>/[A-Za-z][A-Za-z0-9_./%-]*\.html)"
    r"(?P<anchor>#[^)]*)?"
    r"\)"
)


def strip_html_href(prefix: str, path: str, anchor: str) -> str:
    clean = path[:-5] if path.endswith(".html") else path
    if clean == "/index":
        clean = "/"
    return f"{prefix or ''}{clean}{anchor or ''}"


def main() -> None:
    changed = 0
    for md in ROOT.rglob("*.md"):
        rel = str(md.relative_to(ROOT))
        if rel.startswith("de/") or any(part in SKIP for part in rel.split("/")):
            continue
        text = md.read_text(encoding="utf-8")

        def repl(m: re.Match[str]) -> str:
            return "](" + strip_html_href(
                m.group("prefix") or "",
                m.group("path"),
                m.group("anchor") or "",
            ) + ")"

        new = LINK_RE.sub(repl, text)
        if new != text:
            md.write_text(new, encoding="utf-8")
            changed += 1
    print(f"Stripped .html from markdown links in {changed} files.")


if __name__ == "__main__":
    main()
