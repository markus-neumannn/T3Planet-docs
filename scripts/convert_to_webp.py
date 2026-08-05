#!/usr/bin/env python3
"""Convert large doc images to WebP and update markdown references."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "scripts" / "webp_conversion_report.json"
MIN_KB = 300
SKIP = {".git", "node_modules", "scripts", "de", ".mintlify"}


def should_skip(p: Path) -> bool:
    return any(s in SKIP for s in p.parts)


def convert(path: Path) -> dict | None:
    from PIL import Image

    before = path.stat().st_size
    webp = path.with_suffix(".webp")
    with Image.open(path) as img:
        img.save(webp, "WEBP", quality=82, method=6)
    after = webp.stat().st_size
    if after >= before * 0.92:
        webp.unlink(missing_ok=True)
        return None
    rel_old = path.name
    rel_new = webp.name
    updated = 0
    parent = path.parent
    for md in ROOT.rglob("*.md"):
        if should_skip(md):
            continue
        try:
            rel = md.parent.relative_to(ROOT)
        except ValueError:
            continue
        if path.parent != md.parent and path.parent not in md.parents:
            # only update markdown in same tree as image
            if not str(path).startswith(str(md.parent)):
                continue
        text = md.read_text(encoding="utf-8")
        # relative refs like ./images/foo.png or images/foo.png
        patterns = [
            rel_old,
            f"./{path.relative_to(md.parent).as_posix()}",
            path.relative_to(ROOT).as_posix(),
        ]
        new_text = text
        for pat in patterns:
            if pat in new_text:
                new_text = new_text.replace(pat, pat.replace(rel_old, rel_new))
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            updated += 1
    path.unlink()
    return {
        "from": str(path.relative_to(ROOT)),
        "to": str(webp.relative_to(ROOT)),
        "before_kb": round(before / 1024, 1),
        "after_kb": round(after / 1024, 1),
        "md_files": updated,
    }


def main() -> None:
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Pillow required")
        sys.exit(1)

    limit = 30
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1])

    results = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        if path.stat().st_size < MIN_KB * 1024:
            continue
        if len(results) >= limit:
            break
        row = convert(path)
        if row:
            results.append(row)
            print(f"  {row['from']} -> {row['after_kb']}KB ({row['md_files']} md)")

    REPORT.write_text(json.dumps({"converted": len(results), "items": results}, indent=2), encoding="utf-8")
    print(f"Converted {len(results)} images")


if __name__ == "__main__":
    main()
