#!/usr/bin/env python3
"""Translate navigation labels (dropdown/group/tab/anchor) in the de language
block of docs.json into German. Page paths are never translated. Product and
extension names (T3 Karma, EXT:*, ns_*) are left to Google, which preserves them.
"""
import json
import os
import re
import time

from deep_translator import GoogleTranslator

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs.json")
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".de_cache.json")

_t = GoogleTranslator(source="en", target="de")
CACHE = {}
if os.path.exists(CACHE_PATH):
    with open(CACHE_PATH, encoding="utf-8") as fh:
        CACHE = json.load(fh)

LABEL_KEYS = {"dropdown", "group", "tab", "anchor"}
# Leave purely technical identifiers untouched.
SKIP_RE = re.compile(r"^(EXT:|ns_|T3 |T3-|EXT |rte_)", re.I)


def tr(s):
    if not isinstance(s, str) or not s.strip():
        return s
    if SKIP_RE.match(s):
        return s
    if s in CACHE:
        return CACHE[s]
    for attempt in range(5):
        try:
            res = _t.translate(s) or s
            CACHE[s] = res
            return res
        except Exception:  # noqa: BLE001
            time.sleep(1.5 * (attempt + 1))
    CACHE[s] = s
    return s


def walk(node):
    if isinstance(node, dict):
        for k, v in node.items():
            if k in LABEL_KEYS and isinstance(v, str):
                node[k] = tr(v)
            else:
                walk(v)
    elif isinstance(node, list):
        for item in node:
            walk(item)


def main():
    with open(DOCS, encoding="utf-8") as fh:
        data = json.load(fh)
    langs = data.get("navigation", {}).get("languages", [])
    for lang in langs:
        if lang.get("language") == "de":
            walk(lang)
    with open(DOCS, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    with open(CACHE_PATH, "w", encoding="utf-8") as fh:
        json.dump(CACHE, fh, ensure_ascii=False)
    print("docs.json de nav labels translated.")


if __name__ == "__main__":
    main()
