#!/usr/bin/env python3
"""Convert legacy docs.t3planet.de RTD URLs to Mintlify internal paths."""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "node_modules", ".git", ".venv-translate"}

RTD_RE = re.compile(
    r"https?://docs\.t3planet\.de/en/latest/([^)\s\"'>]+?)(?:\.html)?",
    re.I,
)


def to_mintlify(path: str, is_de: bool) -> str:
    path = path.strip("/")
    if path.endswith("/Index"):
        path = path[:-6] + "/Index"
    internal = f"/{path}"
    if is_de:
        return f"/de{internal}"
    return internal


def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = Path(dirpath) / fn
            rel = str(path.relative_to(ROOT))
            is_de = rel.startswith("de/")
            text = path.read_text(encoding="utf-8")

            def repl(m):
                return to_mintlify(m.group(1), is_de)

            new = RTD_RE.sub(repl, text)
            if new != text:
                path.write_text(new, encoding="utf-8")
                changed += 1
    print(f"Fixed legacy RTD links in {changed} files.")


if __name__ == "__main__":
    main()
