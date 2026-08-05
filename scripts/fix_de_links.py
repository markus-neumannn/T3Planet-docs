#!/usr/bin/env python3
"""Prefix internal doc links in de/ with /de/ so language routing stays in German.

Fixes Card href="/ExtNs.../Index" -> href="/de/ExtNs.../Index" and markdown
links ](/License/...) -> ](/de/License/...) without touching external URLs.
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DE = os.path.join(ROOT, "de")

# Root-relative internal paths only (not already /de/, not external, not anchor-only)
HREF_RE = re.compile(r'(href=")(/[^"]+)(")')
MD_RE = re.compile(r'(\]\()(/[^)]+)(\))')


def should_prefix(path: str) -> bool:
    if not path.startswith("/"):
        return False
    if path.startswith("/de/"):
        return False
    if path.startswith(("http://", "https://", "//", "mailto:", "#")):
        return False
    return True


def prefix_path(path: str) -> str:
    return "/de" + path if path != "/" else "/de/"


def fix_text(text: str) -> str:
    def href_sub(m):
        path = m.group(2)
        return m.group(1) + (prefix_path(path) if should_prefix(path) else path) + m.group(3)

    def md_sub(m):
        path = m.group(2)
        return m.group(1) + (prefix_path(path) if should_prefix(path) else path) + m.group(3)

    text = HREF_RE.sub(href_sub, text)
    text = MD_RE.sub(md_sub, text)
    return text


def main():
    changed = 0
    for dirpath, _, filenames in os.walk(DE):
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            with open(path, encoding="utf-8") as fh:
                orig = fh.read()
            new = fix_text(orig)
            if new != orig:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(new)
                changed += 1
    print(f"Fixed internal links in {changed} de/ files.")


if __name__ == "__main__":
    main()
