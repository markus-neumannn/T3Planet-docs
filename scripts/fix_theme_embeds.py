#!/usr/bin/env python3
"""Normalize Supademo/iframe embed markup for theme-aware CSS classes."""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "node_modules", ".git", ".venv-translate"}

EMBED_CONTAINER_STYLE = re.compile(
    r"""style=\{\{position:\s*'relative',\s*boxSizing:\s*'content-box',\s*"""
    r"""maxHeight:\s*'80vh',\s*width:\s*'100%',\s*"""
    r"""aspectRatio:\s*'[\d.]+',\s*padding:\s*'[^']*'\}\}"""
)

EMBED_IFRAME_STYLE = re.compile(
    r"""style=\{\{position:\s*'absolute',\s*top:\s*'0',\s*left:\s*'0',\s*"""
    r"""width:\s*'100%',\s*height:\s*'100%'\}\}"""
)

BARE_EMBED_DIV = re.compile(
    r'<div(?:\s+className="t3-embed")?\s+style=\{\{position:\s*\'relative\','
    r'\s*boxSizing:\s*\'content-box\',\s*maxHeight:\s*\'80vh\',\s*'
    r'width:\s*\'100%\',\s*aspectRatio:\s*\'[\d.]+\',\s*'
    r'padding:\s*\'[^\']*\'\}\}>'
)


def normalize(text: str) -> str:
    text = EMBED_CONTAINER_STYLE.sub("", text)
    text = EMBED_IFRAME_STYLE.sub("", text)
    text = BARE_EMBED_DIV.sub('<div className="t3-embed">', text)
    text = re.sub(
        r'<div className="t3-embed"\s*>',
        '<div className="t3-embed">',
        text,
    )
    text = re.sub(
        r'<div className="t3-embed"\s+>',
        '<div className="t3-embed">',
        text,
    )
    return text


def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = Path(dirpath, fn)
            text = path.read_text(encoding="utf-8")
            if "aspectRatio" not in text and "t3-embed" not in text:
                continue
            new = normalize(text)
            if new != text:
                path.write_text(new, encoding="utf-8")
                changed += 1
    print(f"Normalized embed markup in {changed} files.")


if __name__ == "__main__":
    main()
