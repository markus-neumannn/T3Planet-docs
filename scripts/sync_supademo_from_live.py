#!/usr/bin/env python3
"""Sync missing Supademo iframes from live/local Sphinx HTML into Mintlify MD."""
from __future__ import annotations

import json
import re
import time
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
LIVE = "https://docs.t3planet.de/en/latest/"
# Prefer Live-docs build (fresher offline SoT), then legacy docs/_build.
BUILD_CANDIDATES = [
    ROOT / "Live-docs" / "docs" / "_build" / "html",
    ROOT / "docs" / "_build" / "html",
]
BUILD = next((p for p in BUILD_CANDIDATES if p.is_dir()), BUILD_CANDIDATES[-1])
GAP_REPORT = ROOT / "scripts/supademo-gap-report.json"

IFRAME_RE = re.compile(
    r'<iframe[^>]+src=["\'](https?://(?:app\.)?supademo\.com/[^"\']+)["\'][^>]*>',
    re.I,
)


def embed_id(src: str) -> str | None:
    m = re.search(r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", src, re.I)
    return m.group(1).lower() if m else None


def normalize_src(src: str) -> str:
    src = unescape(src.strip())
    # Prefer /embed/ over /demo/ and strip edit paths
    src = src.replace("/demo/", "/embed/")
    src = re.sub(r"/edit(?=[?#]|$)", "", src)
    return src


def clean_heading(text: str) -> str:
    text = re.sub(r"\s*¶\s*$", "", text)
    text = re.sub(r"\s*\s*$", "", text)
    return re.sub(r"\s+", " ", text).strip()


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


def extract_ordered_embeds(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one('[role="main"]') or soup.select_one(".document") or soup.body or soup
    out = []
    seen = set()
    for iframe in main.select('iframe[src*="supademo"]'):
        src = normalize_src(iframe.get("src") or "")
        eid = embed_id(src)
        key = eid or src
        if key in seen:
            continue
        seen.add(key)
        heading = ""
        for prev in iframe.find_all_previous(["h1", "h2", "h3", "h4"], limit=1):
            heading = clean_heading(prev.get_text(" ", strip=True))
            break
        out.append(
            {
                "src": src,
                "title": iframe.get("title") or heading or "Interactive demo",
                "heading": heading,
                "id": eid,
            }
        )
    return out


def load_html(live_doc: str) -> str | None:
    local = BUILD / f"{live_doc}.html"
    if local.exists():
        return local.read_text(encoding="utf-8", errors="replace")
    try:
        with urlopen(
            Request(LIVE + live_doc + ".html", headers={"User-Agent": "Mozilla/5.0"}),
            timeout=45,
        ) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def existing_ids(text: str) -> set[str]:
    return {
        m.group(1).lower()
        for m in re.finditer(r"supademo\.com/(?:embed|demo)/([a-z0-9]+)", text, re.I)
    }


def insert_after_heading(md: str, heading: str, block: str) -> tuple[str, bool]:
    if not heading:
        return md, False
    # Match ## / ### headings ignoring trailing punctuation differences
    escaped = re.escape(heading)
    # Allow optional trailing punctuation / emoji noise
    hashes = r"#{1,6}"
    pattern = re.compile(
        rf"(?m)^({hashes})\s+{escaped}\s*$"
    )
    # Try exact, then relaxed (prefix match on first 40 chars)
    m = pattern.search(md)
    if not m:
        short = re.escape(heading[:40].rstrip())
        pattern = re.compile(rf"(?m)^({hashes})\s+{short}[^\n]*$")
        m = pattern.search(md)
    if not m:
        return md, False
    # Insert after heading line (and any immediately following blank lines stay)
    end = m.end()
    # Skip one newline
    if end < len(md) and md[end] == "\n":
        end += 1
    # Avoid double-insert if block already follows
    window = md[end : end + 500]
    eid = embed_id(block)
    if eid and eid in window.lower():
        return md, True
    return md[:end] + block + md[end:], True


def append_section(md: str, blocks: list[str]) -> str:
    section = "\n## Interactive demos\n\n" + "".join(blocks)
    if "## Interactive demos" in md:
        # append into existing section end
        return md.rstrip() + "\n" + "".join(blocks) + "\n"
    return md.rstrip() + "\n" + section + "\n"


def sync_page(live: str, mint_rel: str) -> dict:
    mint_path = ROOT / mint_rel
    if not mint_path.exists():
        return {"live": live, "mint": mint_rel, "status": "missing_file"}
    html = load_html(live)
    if not html:
        return {"live": live, "mint": mint_rel, "status": "html_fetch_failed"}
    embeds = extract_ordered_embeds(html)
    if not embeds:
        return {"live": live, "mint": mint_rel, "status": "no_embeds_on_live"}

    md = mint_path.read_text(encoding="utf-8")
    have = existing_ids(md)
    inserted = 0
    appended_blocks: list[str] = []

    # Remove TODO placeholders once we start attaching real demos
    md2 = re.sub(
        r"<Note>\s*TODO: Replace with AI Foundation Supademo embed[\s\S]*?</Note>\s*",
        "",
        md,
        flags=re.I,
    )

    for emb in embeds:
        eid = emb["id"]
        if eid and eid in have:
            continue
        block = make_block(emb["src"], emb["title"])
        md2, ok = insert_after_heading(md2, emb["heading"], block)
        if ok:
            inserted += 1
            if eid:
                have.add(eid)
        else:
            appended_blocks.append(block)
            inserted += 1
            if eid:
                have.add(eid)

    if appended_blocks:
        md2 = append_section(md2, appended_blocks)

    if md2 != md:
        mint_path.write_text(md2, encoding="utf-8")
        return {
            "live": live,
            "mint": mint_rel,
            "status": "updated",
            "inserted": inserted,
            "live_embeds": len(embeds),
        }
    return {
        "live": live,
        "mint": mint_rel,
        "status": "unchanged",
        "inserted": 0,
        "live_embeds": len(embeds),
    }


def main() -> None:
    gaps = json.loads(GAP_REPORT.read_text())["gaps"]
    # unique by mint path
    by_mint: dict[str, dict] = {}
    for g in gaps:
        mint = g.get("mint")
        if not mint:
            continue
        by_mint[mint] = g

    results = []
    for mint, g in sorted(by_mint.items()):
        live = g["live"]
        print(f"Sync {live} -> {mint}")
        res = sync_page(live, mint)
        results.append(res)
        print(" ", res["status"], "inserted=", res.get("inserted"))
        if g.get("source") == "live":
            time.sleep(0.15)

    out = ROOT / "scripts/supademo-sync-report.json"
    out.write_text(json.dumps({"results": results}, indent=2))
    updated = sum(1 for r in results if r["status"] == "updated")
    inserted = sum(r.get("inserted") or 0 for r in results)
    print(f"\nDone. Pages updated: {updated}, embeds inserted: {inserted}")
    print("Report:", out)


if __name__ == "__main__":
    main()
