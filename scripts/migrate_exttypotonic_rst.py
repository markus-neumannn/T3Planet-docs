#!/usr/bin/env python3
"""Convert ExtTypoTonic RST docs to Mintlify Markdown (in place), then remove RST."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = next(
    p
    for p in Path("/Users/nitsan/www/AI Agents").iterdir()
    if p.is_dir() and p.name == "Mintilify Doc"
)
SRC = ROOT / "ExtTypoTonic"

TITLE_MAP = {
    "Index": "TypoTonic",
    "Introduction": "Introduction",
    "Installation": "Installation",
    "GettingStarted": "Getting Started",
    "CreatingAField": "Creating a Field",
    "CreatingADatatype": "Creating a Datatype",
    "CreatingATemplateVariable": "Creating a Template Variable",
    "Templating": "Templating",
    "FrontendPlugins": "Frontend Plugins",
    "DisplayRecordsPlugin": "Display Records Plugin",
    "ViewHelpers": "ViewHelpers",
    "Screenshots": "Screenshots",
    "TypoTonicProfessional": "TypoTonic Professional",
    "FAQ": "FAQ",
    "Support": "Support",
}

DOC_LINKS = {
    "../Installation/Index": "/ExtTypoTonic/Installation/Index",
    "../Support/Index": "/ExtTypoTonic/Support/Index",
    "../GettingStarted/Templating/Index": "/ExtTypoTonic/GettingStarted/Templating/Index",
    "../FAQ/Index": "/ExtTypoTonic/FAQ/Index",
    "../CreatingATemplateVariable/Index": "/ExtTypoTonic/GettingStarted/CreatingATemplateVariable/Index",
    "../Templating/Index": "/ExtTypoTonic/GettingStarted/Templating/Index",
    "../CreatingADatatype/Index": "/ExtTypoTonic/GettingStarted/CreatingADatatype/Index",
    "../../ViewHelpers/Index": "/ExtTypoTonic/ViewHelpers/Index",
    "../../GettingStarted/Templating/Index": "/ExtTypoTonic/GettingStarted/Templating/Index",
    "CreatingAField/Index": "/ExtTypoTonic/GettingStarted/CreatingAField/Index",
    "CreatingADatatype/Index": "/ExtTypoTonic/GettingStarted/CreatingADatatype/Index",
    "CreatingATemplateVariable/Index": "/ExtTypoTonic/GettingStarted/CreatingATemplateVariable/Index",
    "Templating/Index": "/ExtTypoTonic/GettingStarted/Templating/Index",
    "DisplayRecordsPlugin/Index": "/ExtTypoTonic/FrontendPlugins/DisplayRecordsPlugin/Index",
}


def page_title(rst: Path) -> str:
    parts = rst.relative_to(SRC).parts
    if rst.name == "Index.rst" and len(parts) == 1:
        return "TypoTonic"
    stem = parts[-2] if parts[-1] == "Index.rst" and len(parts) > 1 else parts[-1].replace(".rst", "")
    return TITLE_MAP.get(stem, stem)


def convert_inline(text: str) -> str:
    text = re.sub(r"``([^`]+)``", r"`\1`", text)
    text = re.sub(
        r"`([^`<]+)\s+<(https?://[^>]+)>`__",
        r"[\1](\2)",
        text,
    )

    def doc_repl(m: re.Match) -> str:
        target = m.group(1)
        href = DOC_LINKS.get(target)
        if not href:
            clean = target.replace("../", "").replace("../../", "")
            href = "/ExtTypoTonic/" + clean
        if target.endswith("/Index") or target.endswith("Index"):
            key = Path(target).parent.name if "/" in target else "Index"
            label = TITLE_MAP.get(key, key)
        else:
            label = TITLE_MAP.get(Path(target).stem, target)
        return "[{0}]({1})".format(label, href)

    text = re.sub(r":doc:`([^`]+)`", doc_repl, text)
    text = re.sub(r":ref:`([^`<]+)`", r"**\1**", text)
    text = re.sub(r":guilabel:`([^`]+)`", r"**\1**", text)
    return text


def convert_rst(content: str, rst_path: Path) -> str:
    content = re.sub(r"^\.\.\s+include::.*$", "", content, flags=re.M)
    content = re.sub(r"^\.\.\s+_[\w-]+:\s*$", "", content, flags=re.M)
    content = re.sub(r"^\.\.\s+toctree::\n(?:[ \t]+.*\n)*", "", content, flags=re.M)

    lines = content.splitlines()
    out: list[str] = []
    i = 0
    skip_title = True

    def flush_note(note_lines: list[str]) -> None:
        body = convert_inline(" ".join(x.strip() for x in note_lines if x.strip()))
        out.append("")
        out.append("<Note>")
        out.append(body)
        out.append("</Note>")
        out.append("")

    def flush_code(code_lang: str, code_lines: list[str]) -> None:
        out.append(("```" + code_lang).rstrip())
        out.extend(code_lines)
        out.append("```")
        out.append("")

    while i < len(lines):
        line = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""

        m_code = re.match(r"^\.\.\s+code-block::\s*(\w+)?\s*$", line)
        if m_code:
            code_lang = m_code.group(1) or ""
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            while i < len(lines):
                if lines[i].startswith("    ") or lines[i].startswith("\t"):
                    code_lines.append(re.sub(r"^(    |\t)", "", lines[i]))
                    i += 1
                elif lines[i].strip() == "" and i + 1 < len(lines) and (
                    lines[i + 1].startswith("    ") or lines[i + 1].startswith("\t")
                ):
                    code_lines.append("")
                    i += 1
                else:
                    break
            flush_code(code_lang, code_lines)
            continue

        if re.match(r"^\.\.\s+note::\s*$", line):
            note_lines: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            while i < len(lines):
                if lines[i].startswith("   ") or lines[i].startswith("\t"):
                    note_lines.append(lines[i].strip())
                    i += 1
                elif lines[i].strip() == "" and i + 1 < len(lines) and (
                    lines[i + 1].startswith("   ") or lines[i + 1].startswith("\t")
                ):
                    note_lines.append("")
                    i += 1
                else:
                    break
            flush_note(note_lines)
            continue

        m_fig = re.match(r"^\.\.\s+figure::\s+(\S+)\s*$", line)
        if m_fig:
            img = m_fig.group(1)
            alt = ""
            caption = ""
            i += 1
            while i < len(lines):
                m_alt = re.match(r"^\s+:alt:\s+(.*)$", lines[i])
                if m_alt:
                    alt = m_alt.group(1)
                    i += 1
                    continue
                if lines[i].strip() == "":
                    i += 1
                    if i < len(lines) and lines[i].strip() and not lines[i].startswith(".."):
                        n2 = lines[i + 1] if i + 1 < len(lines) else ""
                        if (
                            n2.strip() == ""
                            or n2.startswith("..")
                            or re.match(r"^[=\-~]{3,}\s*$", n2.strip())
                            or lines[i].startswith("   ")
                        ):
                            if not re.match(r"^[=\-~]{3,}\s*$", lines[i].strip()):
                                caption = lines[i].strip()
                                i += 1
                    break
                if lines[i].startswith("   ") and not lines[i].strip().startswith(":"):
                    caption = lines[i].strip()
                    i += 1
                    break
                break
            if img.startswith("Images/"):
                img_md = "./" + img
            elif img.startswith("./") or img.startswith("/"):
                img_md = img
            else:
                img_md = "./Images/" + img
            out.append("![{0}]({1})".format(alt or caption or "Screenshot", img_md))
            if caption and caption != alt:
                out.append("")
                out.append("*" + caption + "*")
            out.append("")
            continue

        if nxt and re.match(r"^[=\-~^\"]{3,}\s*$", nxt) and line.strip() and not line.startswith(" "):
            level = {"=": 2, "-": 3, "~": 4, "^": 4, '"': 4}.get(nxt.strip()[0], 2)
            title = line.strip()
            if skip_title and level == 2:
                skip_title = False
                i += 2
                continue
            skip_title = False
            out.append("")
            out.append("#" * level + " " + convert_inline(title))
            out.append("")
            i += 2
            continue

        if re.match(r"^#\.\s+", line):
            text = re.sub(r"^#\.\s+", "1. ", line)
            out.append(convert_inline(text))
            i += 1
            continue

        if re.match(r"^-\s+", line):
            out.append(convert_inline(line))
            i += 1
            continue

        if line.strip() == "":
            if out and out[-1] != "":
                out.append("")
            i += 1
            continue

        if line.strip().startswith(".."):
            i += 1
            continue

        out.append(convert_inline(line.rstrip()))
        i += 1

    body = "\n".join(out)
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    title = page_title(rst_path)
    desc = "{0} — TypoTonic (EXT:tonic) documentation.".format(title)
    fm = (
        "---\n"
        'title: "{0}"\n'
        'description: "{1}"\n'
        "keywords:\n"
        '  - "TYPO3"\n'
        '  - "T3Planet"\n'
        '  - "TypoTonic"\n'
        '  - "tonic"\n'
        '  - "TONICTYPES"\n'
        'sidebarTitle: "{0}"\n'
        "---\n\n"
    ).format(title, desc)
    return fm + body


def main() -> None:
    rst_files = sorted(SRC.rglob("*.rst"))
    print("Converting {0} RST files...".format(len(rst_files)))
    for rst in rst_files:
        md_path = rst.with_suffix(".md")
        # Root Index gets a card hub below; still convert children only first
        if rst == SRC / "Index.rst":
            continue
        text = rst.read_text(encoding="utf-8")
        md = convert_rst(text, rst)
        md_path.write_text(md, encoding="utf-8")
        print("  OK", md_path.relative_to(ROOT))

    hub = SRC / "Index.md"
    hub.write_text(
        """---
title: "TypoTonic"
description: "TypoTonic (EXT:tonic) — build custom TYPO3 record types with TCA, without writing a dedicated extension."
keywords:
  - "TYPO3"
  - "T3Planet"
  - "TypoTonic"
  - "tonic"
  - "TONICTYPES"
sidebarTitle: "TypoTonic"
---

TypoTonic (extension key `tonic`) lets you build custom record types in the TYPO3 backend with TCA — without writing a new extension for every content type.

<CardGroup cols={2}>
  <Card title="Introduction" href="/ExtTypoTonic/Introduction/Index" />
  <Card title="Installation" href="/ExtTypoTonic/Installation/Index" />
  <Card title="Getting Started" href="/ExtTypoTonic/GettingStarted/Index" />
  <Card title="Frontend Plugins" href="/ExtTypoTonic/FrontendPlugins/Index" />
  <Card title="ViewHelpers" href="/ExtTypoTonic/ViewHelpers/Index" />
  <Card title="Screenshots" href="/ExtTypoTonic/Screenshots/Index" />
  <Card title="TypoTonic Professional" href="/ExtTypoTonic/TypoTonicProfessional/Index" />
  <Card title="FAQ" href="/ExtTypoTonic/FAQ/Index" />
  <Card title="Support" href="/ExtTypoTonic/Support/Index" />
</CardGroup>
""",
        encoding="utf-8",
    )
    print("  OK ExtTypoTonic/Index.md (hub cards)")

    removed = 0
    for rst in rst_files:
        if rst.exists():
            rst.unlink()
            removed += 1
    inc = SRC / "Includes.txt"
    if inc.exists():
        inc.unlink()
        removed += 1
    print("Removed {0} RST/Includes files.".format(removed))


if __name__ == "__main__":
    main()
    from sync_doc_stats import sync_homepage_stats
    sync_homepage_stats()
