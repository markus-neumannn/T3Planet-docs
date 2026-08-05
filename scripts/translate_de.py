#!/usr/bin/env python3
"""Translate the English Markdown docs into German, writing the de/ mirror.

Strategy: mask all non-translatable spans (code fences, raw HTML/iframe blocks,
images, inline code, URLs, HTML/JSX tags) with @@Pn@@ placeholders that survive
Google translation, translate the remaining prose (markdown markup such as
**bold**, headings, lists and [text](url) links is preserved by Google), then
restore the placeholders.

Usage:
  translate_de.py [subpath-prefix ...]      # limit to given top-level prefixes
  translate_de.py --all                     # translate everything
"""
import json
import os
import re
import sys
import time

from deep_translator import GoogleTranslator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".de_cache.json")
EXCLUDE_DIRS = {".git", "node_modules", "scripts", "logo", "images", "_snippets",
                ".venv-translate", "de"}
MAX_CHARS = 4000

_translator = GoogleTranslator(source="en", target="de")

if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, encoding="utf-8") as fh:
        CACHE = json.load(fh)
else:
    CACHE = {}

_dirty = 0


def save_cache():
    tmp = CACHE_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(CACHE, fh, ensure_ascii=False)
    os.replace(tmp, CACHE_PATH)


def translate_raw(text):
    if not text.strip():
        return text
    if text in CACHE:
        return CACHE[text]
    last_err = None
    for attempt in range(5):
        try:
            res = _translator.translate(text)
            if res is None:
                res = text
            CACHE[text] = res
            global _dirty
            _dirty += 1
            return res
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(1.5 * (attempt + 1))
    # give up: keep original
    print(f"  ! translate failed: {str(last_err)[:80]}", file=sys.stderr)
    CACHE[text] = text
    return text


def mask(body):
    store = []

    def repl(m):
        store.append(m.group(0))
        return f"@@P{len(store) - 1}@@"

    patterns = [
        r"```[\s\S]*?```",            # fenced code
        r"~~~[\s\S]*?~~~",            # fenced code (tilde)
        r"<div[\s\S]*?</div>",        # raw html embed blocks
        r"<iframe[\s\S]*?</iframe>",  # iframes
        r"<table[\s\S]*?</table>",    # raw html tables
        r"!\[[^\]]*\]\([^)]*\)",       # images
        r"``[^\n]+?``",               # double-backtick inline code
        r"`[^`\n]+`",                 # inline code
        r"(?:https?://|mailto:)[^\s)\]]+",  # urls
        r"</?[A-Za-z][^>]*>",          # html/jsx tags
    ]
    for pat in patterns:
        body = re.sub(pat, repl, body)
    return body, store


def unmask(body, store):
    def restore(m):
        idx = int(m.group(1))
        return store[idx] if 0 <= idx < len(store) else m.group(0)

    prev = None
    while prev != body:
        prev = body
        body = re.sub(r"@@P(\d+)@@", restore, body)
    return body


def translate_attr_titles(line):
    """Translate title="..."/description="..." values inside component tags."""
    def sub(m):
        return f'{m.group(1)}="{translate_raw(m.group(2))}"'
    if "<Card" in line or "<Columns" in line or "<Accordion" in line or "<Tab" in line:
        line = re.sub(r'(title|description|label)="([^"]+)"', sub, line)
    return line


def translate_body(body):
    # translate component attribute titles first (before masking strips tags)
    body = "\n".join(translate_attr_titles(l) for l in body.split("\n"))

    masked, store = mask(body)
    paras = masked.split("\n\n")

    # group paragraphs into <=MAX_CHARS chunks
    chunks = []
    cur, cur_len = [], 0
    for p in paras:
        if cur and cur_len + len(p) + 2 > MAX_CHARS:
            chunks.append(cur)
            cur, cur_len = [], 0
        cur.append(p)
        cur_len += len(p) + 2
    if cur:
        chunks.append(cur)

    out_paras = []
    for chunk in chunks:
        joined = "\n\n".join(chunk)
        res = translate_raw(joined)
        parts = res.split("\n\n")
        if len(parts) == len(chunk):
            out_paras.extend(parts)
        else:
            # alignment lost: translate paragraph by paragraph
            for p in chunk:
                out_paras.append(translate_raw(p))

    translated = "\n\n".join(out_paras)
    return unmask(translated, store)


def translate_file(en_path, de_path):
    with open(en_path, encoding="utf-8") as fh:
        text = fh.read()

    fm = ""
    body = text
    m = re.match(r"^(---\n.*?\n---\n)(.*)$", text, re.S)
    if m:
        fm, body = m.group(1), m.group(2)
        fm = re.sub(
            r'(title:\s*")([^"]+)(")',
            lambda mm: mm.group(1) + translate_raw(mm.group(2)) + mm.group(3),
            fm,
        )

    new_body = translate_body(body)
    os.makedirs(os.path.dirname(de_path), exist_ok=True)
    with open(de_path, "w", encoding="utf-8") as fh:
        fh.write(fm + new_body)


def iter_en_files(prefixes):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.endswith(".zip")]
        for f in filenames:
            if not f.endswith(".md"):
                continue
            full = os.path.join(dirpath, f)
            rel = os.path.relpath(full, ROOT)
            if rel.startswith("de/") or rel.startswith("de\\"):
                continue
            if prefixes and not any(rel.startswith(p) for p in prefixes):
                continue
            yield rel


def prefix_de_links(text: str) -> str:
    """Ensure Card/markdown internal links in de/ use /de/ prefix."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "fix_de_links", os.path.join(os.path.dirname(__file__), "fix_de_links.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.fix_text(text)


def main():
    args = [a for a in sys.argv[1:] if a != "--all"]
    prefixes = args  # empty -> everything
    files = sorted(iter_en_files(prefixes))
    print(f"Translating {len(files)} files...")
    for n, rel in enumerate(files, 1):
        en_path = os.path.join(ROOT, rel)
        de_path = os.path.join(ROOT, "de", rel)
        try:
            translate_file(en_path, de_path)
            # rewrite internal links to stay in German routes
            with open(de_path, encoding="utf-8") as fh:
                body = fh.read()
            fixed = prefix_de_links(body)
            if fixed != body:
                with open(de_path, "w", encoding="utf-8") as fh:
                    fh.write(fixed)
        except Exception as e:  # noqa: BLE001
            print(f"  ERROR {rel}: {str(e)[:120]}", file=sys.stderr)
        if n % 10 == 0:
            print(f"  [{n}/{len(files)}] {rel}  (cache={len(CACHE)})")
            save_cache()
    save_cache()
    print(f"Done. {len(files)} files, cache size {len(CACHE)}.")


if __name__ == "__main__":
    main()
