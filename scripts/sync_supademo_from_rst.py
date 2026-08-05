#!/usr/bin/env python3
"""Sync Supademo iframes from Live-docs RST sources into Mintlify MD.

The Sphinx HTML build under Live-docs can be stale. RST is the fresher SoT.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIVE_RST = ROOT / "Live-docs" / "docs"
REPORT = ROOT / "scripts" / "qa-final" / "rst-supademo-sync-report.json"

IFRAME_RE = re.compile(
    r'<iframe[^>]+src=["\'](https?://(?:app\.)?supademo\.com/[^"\']+)["\'][^>]*>',
    re.I,
)
SECTION_RE = re.compile(r"^(?P<title>\S.*)\n(?P<underline>[=\-~\"'^]{3,})\s*$", re.M)


def embed_id(src: str) -> str | None:
    m = re.search(r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", src, re.I)
    return m.group(1).lower() if m else None


def normalize_src(src: str) -> str:
    src = src.strip().replace("/demo/", "/embed/")
    src = re.sub(r"[ \t]+", "", src)  # strip accidental whitespace in attrs
    src = re.sub(r"loading=.*$", "", src)  # drop broken trailing junk
    src = src.rstrip("?&")
    if "utm_source=" not in src:
        src += ("&" if "?" in src else "?") + "utm_source=embed"
    return src


def make_block(src: str, title: str) -> str:
    src = normalize_src(src)
    title = (title or "Interactive demo").replace('"', "'")
    return (
        f'\n<div className="t3-embed">'
        f'<iframe src="{src}" loading="lazy" title="{title}" '
        f'allow="clipboard-write" frameBorder="0" '
        f'webkitallowfullscreen="true" mozallowfullscreen="true" '
        f"allowfullscreen></iframe>"
        f"</div>\n"
    )


def extract_rst_embeds(rst_text: str) -> list[dict]:
    """Return embeds with nearest preceding section title."""
    embeds: list[dict] = []
    # Map char offsets of section titles
    sections: list[tuple[int, str]] = []
    for m in SECTION_RE.finditer(rst_text):
        sections.append((m.start(), m.group("title").strip()))

    for m in IFRAME_RE.finditer(rst_text):
        src = normalize_src(m.group(1))
        eid = embed_id(src)
        title_attr = ""
        tag = m.group(0)
        tm = re.search(r'title=["\']([^"\']+)["\']', tag, re.I)
        if tm:
            title_attr = tm.group(1)
        heading = ""
        for off, title in reversed(sections):
            if off < m.start():
                heading = title
                break
        embeds.append(
            {
                "src": src,
                "id": eid,
                "heading": heading,
                "title": title_attr or heading or "Interactive demo",
            }
        )
    # dedupe by id/src preserving order
    seen = set()
    out = []
    for e in embeds:
        key = e["id"] or e["src"]
        if key in seen:
            continue
        seen.add(key)
        out.append(e)
    return out


def existing_ids(text: str) -> set[str]:
    return {
        m.group(1).lower()
        for m in re.finditer(r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", text, re.I)
    }


def insert_after_heading(md: str, heading: str, block: str) -> tuple[str, bool]:
    if not heading:
        return md, False
    variants = [heading, heading.replace(">=", "≥").replace("<=", "≤")]
    for h in variants:
        esc = re.escape(h)
        m = re.search(r"(?m)^(#{1,6})\s+" + esc + r"\s*$", md)
        if not m:
            short = re.escape(h[:48].rstrip())
            m = re.search(r"(?m)^(#{1,6})\s+" + short + r"[^\n]*$", md)
        if not m:
            continue
        end = m.end()
        if end < len(md) and md[end] == "\n":
            end += 1
        eid = embed_id(block) or ""
        if eid and eid in md[end : end + 800].lower():
            return md, True
        return md[:end] + block + md[end:], True
    return md, False


def append_section(md: str, blocks: list[str]) -> str:
    joined = "".join(blocks)
    if "## Interactive demos" in md:
        return md.rstrip() + "\n" + joined + "\n"
    return md.rstrip() + "\n\n## Interactive demos\n" + joined + "\n"


def resolve_md(rel: str) -> Path | None:
    renames = {
        "EXTKarma/ConfigureCaptcha/Index": "EXTKarma/CaptchaConfiguration/Index",
        "EXTKarma/CustomElements/Index": "EXTKarma/ContentBlockElements/Index",
        "EXTKarma/UpgradeGuide/Index": "EXTKarma/UpgradeGuideForContainer/Index",
        "ExtNsT3AF": "T3AF",  # prefix handled below
    }
    mapped = renames.get(rel, rel)
    if mapped.startswith("ExtNsT3AF/") or mapped == "ExtNsT3AF":
        mapped = mapped.replace("ExtNsT3AF", "T3AF", 1)
    for c in [ROOT / f"{mapped}.md", ROOT / mapped / "Index.md"]:
        if c.exists():
            return c
    return None


def sync_all() -> dict:
    results = []
    updated = 0
    inserted_total = 0
    for rst_path in sorted(LIVE_RST.rglob("*.rst")):
        if "_build" in rst_path.parts:
            continue
        # skip nested docs/docs
        parts = rst_path.parts
        if parts.count("docs") > 1 and "Live-docs" in parts:
            # Live-docs/docs is one; Live-docs/docs/docs is nested
            idx = parts.index("docs")
            if "docs" in parts[idx + 1 :]:
                continue
        rel = rst_path.relative_to(LIVE_RST).as_posix()
        if rel.endswith(".rst"):
            rel = rel[:-4]
        if rel.lower() in {"readme", "history", "authors", "index"} and "/" not in rel:
            # root index handled separately if needed
            pass
        rst_text = rst_path.read_text(encoding="utf-8", errors="replace")
        embeds = extract_rst_embeds(rst_text)
        if not embeds:
            continue
        md_path = resolve_md(rel)
        if not md_path:
            results.append({"rst": rel, "status": "missing_md"})
            continue
        md = md_path.read_text(encoding="utf-8")
        have = existing_ids(md)
        missing = [e for e in embeds if not e["id"] or e["id"] not in have]
        if not missing:
            results.append(
                {
                    "rst": rel,
                    "mint": str(md_path.relative_to(ROOT)),
                    "status": "ok",
                    "rst_embeds": len(embeds),
                }
            )
            continue

        md2 = md
        appended: list[str] = []
        inserted = 0
        for emb in missing:
            block = make_block(emb["src"], emb["title"])
            md2, ok = insert_after_heading(md2, emb["heading"], block)
            if ok:
                inserted += 1
                if emb["id"]:
                    have.add(emb["id"])
            else:
                appended.append(block)
                inserted += 1
                if emb["id"]:
                    have.add(emb["id"])
        if appended:
            md2 = append_section(md2, appended)
        if md2 != md:
            md_path.write_text(md2, encoding="utf-8")
            updated += 1
            inserted_total += inserted
            results.append(
                {
                    "rst": rel,
                    "mint": str(md_path.relative_to(ROOT)),
                    "status": "updated",
                    "inserted": inserted,
                    "missing_before": [e["id"] for e in missing],
                }
            )
        else:
            results.append(
                {
                    "rst": rel,
                    "mint": str(md_path.relative_to(ROOT)),
                    "status": "unchanged",
                    "missing": [e["id"] for e in missing],
                }
            )

    report = {
        "updated_pages": updated,
        "inserted_embeds": inserted_total,
        "results": results,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    # Fix broken regex in insert - rewrite carefully without f-string mess
    r = sync_all()
    print(
        f"Updated pages={r['updated_pages']} inserted_embeds={r['inserted_embeds']}"
    )
    print("Report:", REPORT)
