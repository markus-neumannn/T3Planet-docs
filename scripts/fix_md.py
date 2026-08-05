#!/usr/bin/env python3
"""Post-process .md files for Mintlify compatibility."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML_TAGS = {
    "div", "iframe", "style", "script", "table", "tbody", "thead", "tr", "td", "th",
    "a", "span", "p", "ul", "ol", "li", "strong", "em", "br", "hr", "img",
    "b", "i", "u", "code", "pre", "blockquote", "h1", "h2", "h3", "h4", "h5", "h6",
    "figure", "figcaption", "video", "source", "picture", "small", "sub", "sup",
    # Mintlify components
    "Note", "Warning", "Info", "Tip", "Check", "Card", "CardGroup", "Frame",
    "Accordion", "AccordionGroup", "Tabs", "Tab", "Steps", "Step", "Columns",
    "Expandable", "Update", "Tooltip", "Icon", "CodeGroup", "ResponseField",
}


def escape_placeholders(text: str) -> str:
    """Wrap placeholder-like <tag> tokens in backticks, but never inside code spans/blocks."""
    def repl(m: re.Match) -> str:
        tag = m.group(1)
        if tag in HTML_TAGS or tag.lower() in HTML_TAGS:
            return m.group(0)
        return f"`<{tag}>`"

    pat = re.compile(r"\\?<([A-Za-z][A-Za-z0-9_-]*)>")
    out = []
    # 1) keep fenced code blocks untouched
    for i, block in enumerate(re.split(r"(```[\s\S]*?```)", text)):
        if i % 2 == 1:
            out.append(block)
            continue
        # 2) within prose, keep inline `code` spans untouched
        seg_out = []
        for j, seg in enumerate(re.split(r"(`[^`\n]*`)", block)):
            if j % 2 == 1:
                seg_out.append(seg)
            else:
                seg_out.append(pat.sub(repl, seg))
        out.append("".join(seg_out))
    return "".join(out)


def fix_iframe_src(text: str) -> str:
    return re.sub(r'(<iframe\s+src=)(https?://[^>\s]+)', r'\1"\2"', text)


def fix_orphan_underlines(text: str) -> str:
    """Drop stray RST section-underline lines, but never code-fence backticks/tildes."""
    out = []
    in_fence = False
    for line in text.splitlines():
        st = line.strip()
        if re.match(r"^(```+|~~~+)", st):
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            if re.match(r"^[=\-^#'\"]{3,}$", st):
                continue
            if st == "::":
                continue
        out.append(line)
    return "\n".join(out)


def fix_typoscript_less_equal(text: str) -> str:
    return re.sub(r"<=(v?\d+)", r"v\1 and below", text)


def fix_autolinks(text: str) -> str:
    """Convert MyST/markdown autolinks <https://x> to bare URLs (MDX rejects them as JSX)."""
    out = []
    for i, block in enumerate(re.split(r"(```[\s\S]*?```)", text)):
        if i % 2 == 1:
            out.append(block)
            continue
        seg_out = []
        for j, seg in enumerate(re.split(r"(`[^`\n]*`)", block)):
            if j % 2 == 1:
                seg_out.append(seg)
            else:
                seg = re.sub(r"<(https?://[^>\s]+)>", r"\1", seg)
                seg = re.sub(r"<mailto:([^>\s]+)>", r"\1", seg)
                seg = re.sub(r"<((?:tel|ftp|mailto):[^>\s]+)>", r"\1", seg)
                seg_out.append(seg)
        out.append("".join(seg_out))
    return "".join(out)


def remove_style_blocks(text: str) -> str:
    return re.sub(r"<style>.*?</style>", "", text, flags=re.DOTALL)


def fix_double_backticks(text: str) -> str:
    """Convert RST inline ``code`` to `code`, but never touch fenced code blocks."""
    parts = re.split(r"(```[\s\S]*?```)", text)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(part)
        else:
            out.append(re.sub(r"``([^`]+)``", r"`\1`", part))
    return "".join(out)


def fix_preview_feature(text: str) -> str:
    text = re.sub(
        r"`+api/draft\?slug=`?<slug>`+",
        "`api/draft?slug=<slug>`",
        text,
    )
    text = text.replace(
        "To swtich to preview mode simpy call",
        "To switch to preview mode simply call",
    )
    return text


def _css_to_jsx(css: str) -> str:
    props = []
    seen = set()
    for decl in css.split(";"):
        decl = decl.strip()
        if not decl or ":" not in decl:
            continue
        key, val = decl.split(":", 1)
        key = key.strip()
        val = val.strip().replace("\\", "\\\\").replace("'", "\\'")
        parts = key.split("-")
        jkey = parts[0] + "".join(p.capitalize() for p in parts[1:])
        if not jkey or jkey in seen:
            continue
        seen.add(jkey)
        props.append(f"{jkey}: '{val}'")
    return "style={{" + ", ".join(props) + "}}"


def fix_inline_styles(text: str) -> str:
    """Convert raw HTML style="..." strings to JSX style objects (MDX requirement)."""
    out = []
    for i, block in enumerate(re.split(r"(```[\s\S]*?```)", text)):
        if i % 2 == 1:
            out.append(block)
            continue
        block = re.sub(r'style="([^"]*)"', lambda m: _css_to_jsx(m.group(1)), block)
        # Minimal safe attribute fixes (others are React warnings, not errors)
        block = re.sub(r"\bframeborder=", "frameBorder=", block)
        block = re.sub(r'(<[a-zA-Z][^>]*?)\sclass="([^"]*)"', r'\1 className="\2"', block)
        out.append(block)
    return "".join(out)


def fix_broken_iframes_multiline(text: str) -> str:
    # Collapse broken multi-line iframe tags
    text = re.sub(
        r'<iframe\s+src="([^"]*)\n\s*loading=',
        r'<iframe src="\1" loading=',
        text,
    )
    return text


def _actual_case_rel(base: Path, rel: str) -> str | None:
    """Resolve `rel` under `base` returning the path with real on-disk casing, or None."""
    cur = base
    real_parts = []
    for part in rel.split("/"):
        if part in ("", "."):
            continue
        if not cur.is_dir():
            return None
        entries = os.listdir(cur)
        if part in entries:
            chosen = part
        else:
            m = [e for e in entries if e.lower() == part.lower()]
            if not m:
                return None
            chosen = m[0]
        real_parts.append(chosen)
        cur = cur / chosen
    return "/".join(real_parts)


def fix_image_paths(body: str, path: Path) -> str:
    """Rewrite image refs to match real on-disk case; recover refs missing Images/ prefix."""
    def repl(m: re.Match) -> str:
        alt, ip = m.group(1), m.group(2)
        raw = ip.split("#")[0].split("?")[0]
        if raw.startswith("http") or raw.startswith("/") or not raw:
            return m.group(0)
        # exact on-disk (case-correct) resolution
        real = _actual_case_rel(path.parent, raw)
        if real:
            return f"![{alt}]({real})" if real != raw else m.group(0)
        # try common image folders if prefix is missing
        base = os.path.basename(raw)
        for folder in ("Images", "images"):
            real = _actual_case_rel(path.parent, f"{folder}/{base}")
            if real:
                return f"![{alt}]({real})"
        return m.group(0)
    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", repl, body)


def fix_file(path: Path) -> bool:
    orig = path.read_text(encoding="utf-8")
    if not orig.startswith("---"):
        return False
    parts = orig.split("---", 2)
    if len(parts) < 3:
        return False
    body = parts[2]
    body = fix_image_paths(body, path)
    body = fix_orphan_underlines(body)
    body = remove_style_blocks(body)
    body = fix_iframe_src(body)
    body = fix_broken_iframes_multiline(body)
    body = fix_inline_styles(body)
    body = fix_preview_feature(body)
    body = fix_double_backticks(body)
    body = fix_typoscript_less_equal(body)
    body = fix_autolinks(body)
    body = escape_placeholders(body)
    body = re.sub(r"\n{3,}", "\n\n", body)
    new = f"---{parts[1]}---{body}"
    if not new.endswith("\n"):
        new += "\n"
    if new != orig:
        path.write_text(new, encoding="utf-8")
        return True
    return False


IMG_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
SKIP_TOP = {"de", "scripts", "node_modules", ".git", ".vscode", "logo", "_static"}


def sync_de() -> None:
    de = ROOT / "de"
    if de.exists():
        shutil.rmtree(de)
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[0] in SKIP_TOP:
            continue
        if path.suffix.lower() != ".md" and path.suffix.lower() not in IMG_EXTS:
            continue
        target = de / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    (de / "index.md").write_text("""---
title: "T3Planet Dokumentation"
description: "Offizielle T3Planet TYPO3 Dokumentation."
---

Willkommen in der T3Planet-Dokumentation.

> **Hinweis:** Die deutsche Übersetzung wird eingeführt. Inhalte entsprechen vorübergehend der englischen Version.
""", encoding="utf-8")
    # Prefix internal Card/markdown links with /de/
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "fix_de_links", ROOT / "scripts" / "fix_de_links.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


def main() -> None:
    n = 0
    for md in ROOT.rglob("*.md"):
        if "scripts" in md.parts:
            continue
        if fix_file(md):
            n += 1
    print(f"Fixed {n} files")
    sync_de()
    print("Synced de/ mirror")


if __name__ == "__main__":
    main()
