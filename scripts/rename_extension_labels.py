#!/usr/bin/env python3
"""Rename EXT:ns_* labels to NS Extension Name (no EXT:, no underscores)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

UPPER_WORDS = {
    "t3ai", "t3ac", "t3as", "t3al", "t3aa", "t3ab",
    "faq", "pwa", "seo", "crm", "rte", "llm", "ai", "api",
}

SPECIAL_PHRASES = {
    "ckeditor pack": "CKEditor Pack",
    "ckeditor": "CKEditor",
    "sitekit": "Site Kit",
    "zoho crm": "Zoho CRM",
}


def beautify_words(text: str) -> str:
    lower = text.lower()
    for phrase, replacement in SPECIAL_PHRASES.items():
        if lower == phrase:
            return replacement
    words = text.split()
    out = []
    for w in words:
        wl = w.lower()
        if wl in UPPER_WORDS:
            out.append(wl.upper())
        elif wl.startswith("t3") and len(wl) <= 5:
            out.append(wl.upper())
        else:
            out.append(w.capitalize())
    result = " ".join(out)
    for phrase, replacement in SPECIAL_PHRASES.items():
        if phrase in result.lower():
            idx = result.lower().find(phrase)
            result = result[:idx] + replacement + result[idx + len(phrase) :]
    return result


def format_extension_display_name(raw: str) -> str:
    """EXT:ns_news_comments -> NS News Comments"""
    s = raw.strip()
    if not s.upper().startswith("EXT:"):
        return s
    s = s[4:]
    for prefix in ("ns_", "nitsan_", "rte_"):
        if s.lower().startswith(prefix):
            s = s[len(prefix) :]
            break
    s = s.replace("_", " ")
    return "NS " + beautify_words(s)


def format_slug_display_name(slug: str) -> str:
    """ExtNsRevolutionSlider -> NS Revolution Slider"""
    name = slug
    for prefix in ("ExtNs", "EXTNs", "ExtNitsan", "ExtRTEC"):
        if name.startswith(prefix):
            name = name[len(prefix) :]
            break
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", name)
    spaced = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", spaced)
    return "NS " + beautify_words(spaced.replace("_", " "))


def update_docs_json() -> int:
    path = ROOT / "docs.json"
    docs = json.loads(path.read_text())
    count = 0

    def walk(node):
        nonlocal count
        if isinstance(node, dict):
            for key in ("dropdown", "group"):
                if key in node and isinstance(node[key], str):
                    new = format_extension_display_name(node[key])
                    if new != node[key]:
                        node[key] = new
                        count += 1
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(docs)
    path.write_text(json.dumps(docs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return count


def is_extension_index(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))
    return bool(
        re.match(
            r"^(de/)?(ExtNs|EXTNs|ExtNitsan|ExtRTEC)[^/]+/Index\.md$",
            rel,
        )
    )


def update_frontmatter_field(text: str, field: str, new_value: str) -> str:
    pattern = rf'^({field}:\s*")(.+?)(")\s*$'
    return re.sub(pattern, rf'\1{new_value}\3', text, count=1, flags=re.M)


def update_md_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False
    m = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.S)
    if not m:
        return False
    fm = m.group(0)
    original = fm

    for field in ("title", "sidebarTitle"):
        fm_match = re.search(rf'^{field}:\s*"(.+?)"\s*$', fm, re.M)
        if fm_match:
            old = fm_match.group(1)
            new = format_extension_display_name(old)
            if new != old:
                fm = update_frontmatter_field(fm, field, new)

    desc_match = re.search(r'^description:\s*"(.+?)"\s*$', fm, re.M)
    if desc_match:
        desc = desc_match.group(1)
        new_desc = desc
        for old_part in re.findall(r"EXT:[^\s–]+", desc):
            new_part = format_extension_display_name(old_part)
            new_desc = new_desc.replace(old_part, new_part)
        if new_desc != desc:
            fm = update_frontmatter_field(fm, "description", new_desc)

    kw_block = re.search(r"^keywords:\s*\n((?:\s+- .+\n)+)", fm, re.M)
    if kw_block:
        lines = kw_block.group(1).splitlines()
        new_lines = []
        changed = False
        for line in lines:
            item = re.search(r'-\s*"(.+)"', line)
            if item and item.group(1).upper().startswith("EXT:"):
                new_item = format_extension_display_name(item.group(1))
                new_lines.append(f'  - "{new_item}"')
                changed = True
            else:
                new_lines.append(line)
        if changed:
            fm = fm.replace(kw_block.group(0), "keywords:\n" + "\n".join(new_lines) + "\n")

    if fm == original:
        return False
    path.write_text(fm + text[m.end() :], encoding="utf-8")
    return True


def main() -> None:
    docs_count = update_docs_json()
    print(f"Updated {docs_count} labels in docs.json")

    md_count = 0
    for md in ROOT.rglob("Index.md"):
        if "scripts" in md.parts or not is_extension_index(md):
            continue
        if update_md_file(md):
            md_count += 1
            print(f"  {md.relative_to(ROOT)}")

    print(f"Updated {md_count} extension Index.md frontmatter files")
    print("Done. Run: python3 scripts/generate_hub_landings.py")


if __name__ == "__main__":
    main()
