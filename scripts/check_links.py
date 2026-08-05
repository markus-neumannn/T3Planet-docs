#!/usr/bin/env python3
"""Verify nav pages exist, find orphans, broken internal links, missing images."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def collect_nav_pages(node, out: set[str]):
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "pages" and isinstance(v, list):
                for p in v:
                    if isinstance(p, str):
                        out.add(p)
                    else:
                        collect_nav_pages(p, out)
            else:
                collect_nav_pages(v, out)
    elif isinstance(node, list):
        for x in node:
            collect_nav_pages(x, out)


def main():
    docs = json.loads((ROOT / "docs.json").read_text())
    nav_pages: set[str] = set()
    collect_nav_pages(docs["navigation"], nav_pages)

    # 1. nav pages that don't exist on disk
    missing_nav = []
    for p in sorted(nav_pages):
        if not (ROOT / (p + ".md")).exists():
            missing_nav.append(p)

    # 2. md files not referenced in nav (orphans)
    all_md = set()
    for md in ROOT.rglob("*.md"):
        if "scripts" in md.parts or "docs-master-md" in md.parts:
            continue
        rel = str(md.relative_to(ROOT))[:-3]
        all_md.add(rel)
    orphans = sorted(all_md - nav_pages)

    # 3. broken internal links + missing local images
    broken_links = []
    missing_images = []
    link_re = re.compile(r"\[[^\]]*\]\((/[^)\s]+)\)")
    href_re = re.compile(r'href="(/[^"]+)"')
    img_re = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
    for md in ROOT.rglob("*.md"):
        if "scripts" in md.parts or "docs-master-md" in md.parts:
            continue
        rel = str(md.relative_to(ROOT))
        text = md.read_text(encoding="utf-8")
        targets = set(link_re.findall(text)) | set(href_re.findall(text))
        for t in targets:
            tt = t.split("#")[0].rstrip("/")
            if not tt or tt == "":
                continue
            # skip asset links
            if re.search(r"\.(png|jpg|jpeg|gif|svg|webp|pdf|zip|mp4)$", tt, re.I):
                cand = ROOT / tt.lstrip("/")
                if not cand.exists():
                    missing_images.append((rel, t))
                continue
            cand = ROOT / (tt.lstrip("/") + ".md")
            cand_idx = ROOT / tt.lstrip("/") / "index.md"
            if not cand.exists() and not cand_idx.exists():
                broken_links.append((rel, t))
        for img in img_re.findall(text):
            if img.startswith("http"):
                continue
            ip = img.split("#")[0].split("?")[0]
            if ip.startswith("/"):
                cand = ROOT / ip.lstrip("/")
            else:
                cand = (md.parent / ip).resolve()
            if not cand.exists():
                missing_images.append((rel, img))

    print(f"Nav pages: {len(nav_pages)} | MD files: {len(all_md)}")
    print(f"Missing nav targets: {len(missing_nav)}")
    for m in missing_nav[:40]:
        print(f"   MISSING NAV: {m}")
    print(f"Orphan md (not in nav): {len(orphans)}")
    for o in orphans[:40]:
        print(f"   ORPHAN: {o}")
    print(f"Broken internal links: {len(broken_links)}")
    for b in broken_links[:40]:
        print(f"   BROKEN: {b[0]} -> {b[1]}")
    print(f"Missing images: {len(missing_images)}")
    for mi in missing_images[:40]:
        print(f"   IMG: {mi[0]} -> {mi[1]}")


if __name__ == "__main__":
    main()
