#!/usr/bin/env python3
"""
Phase 1 & 2 - Refresh source/Mintlify inventory, build the source-to-Mintlify
migration matrix, and run a structural content-parity diff for every page.

Source of truth: local .rst tree under docs/docs (per task instructions).
Output:
  scripts/remigration/matrix.json   - full per-page matrix + diff data
  scripts/remigration/matrix.md     - human summary report
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SRC_ROOT = ROOT / "docs" / "docs"
OUT_JSON = Path(__file__).resolve().parent / "matrix.json"
OUT_MD = Path(__file__).resolve().parent / "matrix.md"

SKIP_TOP = {"docs", "scripts", ".git", "node_modules", "de", "live-docs", ".venv-translate", "visual-regression"}

# Mintlify pages that are intentionally new (not derived from an .rst file) or
# whose corresponding RST source does not exist / is out of scope.
INTENTIONAL_EXTRA_PREFIXES = (
    "extnst3af/",  # AI Foundation extension - added after RST source freeze
    "extnst3ai/configuration",
)
INTENTIONAL_EXTRA_EXACT = {
    "allextensions", "alltemplates", "aifoundationextensions", "index",
}

# Manually reviewed during Phase 2 - confirmed NOT real content gaps (see matrix.md notes).
REVIEWED_NON_ISSUES = {
    "extnsbackup/introduction": "RST 'Features' table is a degenerate single-column grid table; "
                                 "Mintlify converts it to a bullet list with identical content - no data lost.",
    "history": "docs/docs/history.rst only does '.. include:: ../HISTORY.rst', which does not exist in the "
                "source tree. The live site's /history.html also renders with <no title> and an empty body "
                "(verified via live fetch) - this page is empty on the live site too, so there is nothing to migrate.",
}


def norm(p: str) -> str:
    return p.replace("\\", "/").rstrip("/")


# ---------------------------------------------------------------------------
# RST parsing
# ---------------------------------------------------------------------------

RST_DIRECTIVE_NOTE = re.compile(
    r"^\s*\.\.\s+(note|warning|tip|important|attention|caution|danger|hint)::[ \t]*\n((?:[ \t]+\S.*\n?)+)",
    re.I | re.M,
)
RST_CODEBLOCK = re.compile(r"^\s*\.\.\s+code-block::\s*(\S+)?", re.M)
RST_IMAGE = re.compile(r"^\s*\.\.\s+(?:image|figure)::\s*(\S+)", re.M)
RST_TABLE_DIRECTIVE = re.compile(r"^\s*\.\.\s+(?:csv-table|list-table|table)::", re.M)
RST_GRID_TABLE_ROW = re.compile(r"^\s*\+[-=+]+\+\s*$", re.M)
RST_SUPADEMO = re.compile(r"supademo\.com", re.I)
RST_HEADING_UNDERLINE = re.compile(r"^([=\-~^\"'#*+_.:`])\1{3,}\s*$", re.M)
RST_LINK = re.compile(r"`[^`<>]+<([^`<>]+)>`_")
RST_DOC_REF = re.compile(r":(?:doc|ref):`[^`]+`")


def parse_rst(text: str) -> dict:
    lines = text.splitlines()
    headings = []
    for i in range(1, len(lines)):
        prev = lines[i - 1].strip()
        line = lines[i].strip()
        if not prev or not line:
            continue
        if RST_HEADING_UNDERLINE.match(line) and len(line) >= max(3, len(prev) - 2):
            headings.append(prev)
    title = headings[0] if headings else ""

    callouts = [d for d, body in RST_DIRECTIVE_NOTE.findall(text) if body.strip()]
    code_blocks = RST_CODEBLOCK.findall(text)
    images = RST_IMAGE.findall(text)
    tables = len(RST_TABLE_DIRECTIVE.findall(text)) + (1 if RST_GRID_TABLE_ROW.search(text) else 0)
    supademo = len(RST_SUPADEMO.findall(text))
    ext_links = [u for u in RST_LINK.findall(text) if u.startswith("http")]
    doc_refs = len(RST_DOC_REF.findall(text))

    return {
        "title": title,
        "headings": headings,
        "heading_count": len(headings),
        "callouts": len(callouts),
        "callout_types": callouts,
        "code_blocks": len(code_blocks),
        "images": images,
        "image_count": len(images),
        "tables": tables,
        "supademo_count": supademo,
        "external_links": ext_links,
        "external_link_count": len(ext_links),
        "internal_doc_refs": doc_refs,
        "char_len": len(text),
    }


# ---------------------------------------------------------------------------
# Mintlify MD/MDX parsing
# ---------------------------------------------------------------------------

MD_FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.S)
MD_TITLE_FIELD = re.compile(r'^title:\s*"?([^"\n]+)"?', re.M)
MD_HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.M)
MD_CALLOUT = re.compile(r"<(Note|Warning|Tip|Info|Check|Danger)\b", re.I)
MD_CODEBLOCK = re.compile(r"^[ \t]*```(\S*)", re.M)
MD_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img\s+[^>]*src=[\"']([^\"']+)[\"']", re.I)
MD_FRAME = re.compile(r"<Frame\b", re.I)
MD_TABLE_ROW = re.compile(r"^\s*\|.+\|\s*$", re.M)
MD_SUPADEMO = re.compile(r"supademo\.com", re.I)
MD_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_md(text: str) -> dict:
    fm_match = MD_FRONTMATTER.match(text)
    title = ""
    body = text
    if fm_match:
        fm = fm_match.group(1)
        t = MD_TITLE_FIELD.search(fm)
        if t:
            title = t.group(1).strip()
        body = text[fm_match.end():]

    headings = [h[1].strip() for h in MD_HEADING.findall(body)]
    callouts = MD_CALLOUT.findall(body)
    code_blocks = [c for c in MD_CODEBLOCK.findall(body)]
    # every fence has an open + close match; halve
    code_block_count = len(code_blocks) // 2 if len(code_blocks) % 2 == 0 else len(code_blocks)
    images = MD_IMAGE.findall(body)
    image_count = len([i for i in images if any(i)]) + len(MD_FRAME.findall(body))
    table_rows = len(MD_TABLE_ROW.findall(body))
    supademo = len(MD_SUPADEMO.findall(body))
    links = MD_LINK.findall(body)
    ext_links = [u for u in links if u.startswith("http")]

    return {
        "title": title,
        "headings": headings,
        "heading_count": len(headings),
        "callouts": len(callouts),
        "callout_types": callouts,
        "code_blocks": code_block_count,
        "image_count": image_count,
        "tables": 1 if table_rows >= 2 else 0,
        "table_rows": table_rows,
        "supademo_count": supademo,
        "external_link_count": len(ext_links),
        "char_len": len(body),
    }


# ---------------------------------------------------------------------------
# Inventory collection
# ---------------------------------------------------------------------------

def collect_rst() -> dict:
    result = {}
    for dp, dirs, files in os.walk(SRC_ROOT):
        parts = Path(dp).relative_to(SRC_ROOT).parts
        if parts and parts[0] == "_build":
            dirs[:] = []
            continue
        rel_dir = norm(str(Path(dp).relative_to(SRC_ROOT))) if dp != str(SRC_ROOT) else ""
        for f in files:
            if not f.lower().endswith(".rst"):
                continue
            stem = f[:-4]
            page_id = rel_dir if stem.lower() == "index" else (f"{rel_dir}/{stem}" if rel_dir else stem)
            page_id = page_id if page_id else "index"
            full = os.path.join(dp, f)
            try:
                text = Path(full).read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                text = ""
            result[page_id.lower()] = {
                "page_id": page_id,
                "src_path": str(Path(full).relative_to(ROOT)),
                **parse_rst(text),
            }
    return result


def collect_md() -> dict:
    result = {}
    for dp, dirs, files in os.walk(ROOT):
        rel_dir = norm(str(Path(dp).relative_to(ROOT))) if dp != str(ROOT) else ""
        top = rel_dir.split("/")[0].lower() if rel_dir else ""
        if rel_dir == "" :
            dirs[:] = [d for d in dirs if d.lower() not in SKIP_TOP and not d.startswith(".")]
        elif top in SKIP_TOP:
            dirs[:] = []
            continue
        for f in files:
            if not (f.endswith(".md") or f.endswith(".mdx")):
                continue
            stem = f.rsplit(".", 1)[0]
            page_id = rel_dir if stem.lower() == "index" else (f"{rel_dir}/{stem}" if rel_dir else stem)
            page_id = page_id if page_id else "index"
            full = os.path.join(dp, f)
            try:
                text = Path(full).read_text(encoding="utf-8", errors="replace")
            except Exception:
                text = ""
            result[page_id.lower()] = {
                "page_id": page_id,
                "mint_path": str(Path(full).relative_to(ROOT)),
                **parse_md(text),
            }
    return result


def classify(rst: dict | None, md: dict | None) -> tuple[str, list[str]]:
    if rst is None and md is not None:
        return "INTENTIONALLY_ADDED", ["No RST source; page added directly in Mintlify (new extension/hub/report)."]
    if rst is not None and md is None:
        return "PAGE_MISSING", ["Source RST has no corresponding Mintlify md/mdx file."]

    issues = []
    # callouts (notes/warnings/tips) should not have been dropped
    if rst["callouts"] > 0 and md["callouts"] < rst["callouts"]:
        issues.append(f"callouts: rst={rst['callouts']} mint={md['callouts']} (possible dropped note/warning/tip)")
    if rst["image_count"] > 0 and md["image_count"] < rst["image_count"]:
        issues.append(f"images: rst={rst['image_count']} mint={md['image_count']} (possible missing image)")
    if rst["code_blocks"] > 0 and md["code_blocks"] < rst["code_blocks"]:
        issues.append(f"code_blocks: rst={rst['code_blocks']} mint={md['code_blocks']} (possible missing code example)")
    if rst["supademo_count"] > 0 and md["supademo_count"] < rst["supademo_count"]:
        issues.append(f"supademo: rst={rst['supademo_count']} mint={md['supademo_count']} (possible missing embed)")
    if rst["tables"] > 0 and md["tables"] == 0:
        issues.append("tables: rst has table directive, mint has no markdown table")
    # thin content heuristic (only meaningful when rst has real body text)
    if rst["char_len"] > 400 and md["char_len"] > 0 and (md["char_len"] / max(rst["char_len"], 1)) < 0.15:
        issues.append(f"thin_content: rst_len={rst['char_len']} mint_len={md['char_len']} ratio={round(md['char_len']/max(rst['char_len'],1),3)}")

    if issues:
        return "CONTENT_MISSING" if any("possible" in i or "table" in i for i in issues) else "EXISTS_BUT_INCOMPLETE", issues
    return "MIGRATED_CORRECTLY", []


def main() -> None:
    print("Collecting RST inventory...")
    rst_pages = collect_rst()
    print(f"  {len(rst_pages)} RST page-units")

    print("Collecting Mintlify md/mdx inventory...")
    md_pages = collect_md()
    print(f"  {len(md_pages)} Mintlify page-units")

    all_ids = sorted(set(rst_pages) | set(md_pages))
    matrix = []
    status_counts: dict[str, int] = {}
    for pid in all_ids:
        rst = rst_pages.get(pid)
        md = md_pages.get(pid)

        if rst is None and md is not None:
            low = pid.lower()
            if low.startswith(INTENTIONAL_EXTRA_PREFIXES) or low in INTENTIONAL_EXTRA_EXACT or low.startswith("scripts/") :
                status, issues = "INTENTIONALLY_ADDED", ["No RST source; new/hub/report page."]
            else:
                status, issues = "INTENTIONALLY_ADDED", ["No RST source found for this Mintlify page (review manually)."]
        else:
            status, issues = classify(rst, md)

        if pid in REVIEWED_NON_ISSUES:
            status = "REVIEWED_OK"
            issues = [REVIEWED_NON_ISSUES[pid]]

        status_counts[status] = status_counts.get(status, 0) + 1
        matrix.append({
            "page_id": pid,
            "status": status,
            "issues": issues,
            "rst": rst,
            "mint": md,
        })

    OUT_JSON.write_text(json.dumps({
        "generated_pages": len(matrix),
        "status_counts": status_counts,
        "matrix": matrix,
    }, indent=2), encoding="utf-8")

    # Markdown summary
    lines = ["# Re-Migration Matrix - Summary", ""]
    lines.append(f"Total page ids compared: **{len(matrix)}**")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---|")
    for k, v in sorted(status_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {k} | {v} |")
    lines.append("")

    flagged = [m for m in matrix if m["status"] in ("CONTENT_MISSING", "EXISTS_BUT_INCOMPLETE", "PAGE_MISSING")]
    reviewed_ok = [m for m in matrix if m["status"] == "REVIEWED_OK"]
    lines.append(f"## Flagged pages requiring review ({len(flagged)})")
    lines.append("")
    for m in flagged:
        lines.append(f"### `{m['page_id']}` - {m['status']}")
        for i in m["issues"]:
            lines.append(f"- {i}")
        if m["rst"]:
            lines.append(f"- src: `{m['rst']['src_path']}`")
        if m["mint"]:
            lines.append(f"- mint: `{m['mint']['mint_path']}`")
        lines.append("")

    if reviewed_ok:
        lines.append(f"## Manually reviewed - confirmed non-issues ({len(reviewed_ok)})")
        lines.append("")
        for m in reviewed_ok:
            lines.append(f"### `{m['page_id']}`")
            for i in m["issues"]:
                lines.append(f"- {i}")
            lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {OUT_JSON} and {OUT_MD}")
    print(json.dumps(status_counts, indent=2))
    print(f"\nFlagged for review: {len(flagged)}")


if __name__ == "__main__":
    main()
