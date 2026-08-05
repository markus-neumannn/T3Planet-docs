#!/usr/bin/env python3
"""Compress large documentation images for faster page loads."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "scripts" / "image_optimization_report.json"
MIN_SIZE_KB = 400
MAX_WIDTH = 1400
JPEG_QUALITY = 80

SKIP_DIRS = {".git", "node_modules", ".venv-translate", "scripts", ".review-frames", "de"}


def should_skip(path: Path) -> bool:
    return any(p in SKIP_DIRS for p in path.parts)


def optimize_with_pillow(path: Path) -> tuple[bool, int, int]:
    from PIL import Image

    before = path.stat().st_size
    with Image.open(path) as img:
        img.load()
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_size = (MAX_WIDTH, max(1, int(img.height * ratio)))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        if path.suffix.lower() in {".jpg", ".jpeg"}:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(path, "JPEG", optimize=True, quality=JPEG_QUALITY)
        elif path.suffix.lower() == ".png":
            img.save(path, "PNG", optimize=True, compress_level=9)
        else:
            return False, before, before
    after = path.stat().st_size
    return after < before, before, after


def optimize_with_sips(path: Path) -> tuple[bool, int, int]:
    before = path.stat().st_size
    try:
        if path.suffix.lower() in {".jpg", ".jpeg"}:
            subprocess.run(
                ["sips", "-Z", str(MAX_WIDTH), "--setProperty", "format", "jpeg",
                 "--setProperty", "formatOptions", str(JPEG_QUALITY), str(path)],
                check=True,
                capture_output=True,
            )
        else:
            subprocess.run(["sips", "-Z", str(MAX_WIDTH), str(path)], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        return False, before, before
    after = path.stat().st_size
    return after < before, before, after


def optimize_file(path: Path, use_pillow: bool) -> dict | None:
    before = path.stat().st_size
    if before < MIN_SIZE_KB * 1024:
        return None
    try:
        if use_pillow:
            changed, b, a = optimize_with_pillow(path)
        else:
            changed, b, a = optimize_with_sips(path)
    except Exception as e:
        return {"path": str(path.relative_to(ROOT)), "error": str(e), "before": before}
    if not changed:
        return None
    return {
        "path": str(path.relative_to(ROOT)),
        "before_kb": round(b / 1024, 1),
        "after_kb": round(a / 1024, 1),
        "saved_kb": round((b - a) / 1024, 1),
    }


def add_lazy_loading_hints() -> int:
    """Add loading=lazy to markdown images missing the attribute."""
    updated = 0
    for md in ROOT.rglob("*.md"):
        if should_skip(md):
            continue
        text = md.read_text(encoding="utf-8")
        new = text
        # ![alt](path) without loading hint in HTML img tags only in raw HTML
        if "loading=" not in text and "<img " in text:
            new = new.replace("<img ", '<img loading="lazy" decoding="async" ')
        if new != text:
            md.write_text(new, encoding="utf-8")
            updated += 1
    return updated


def main() -> None:
    use_pillow = False
    try:
        import PIL  # noqa: F401
        use_pillow = True
    except ImportError:
        pass

    dry_run = "--dry-run" in sys.argv
    limit = 0
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=", 1)[1])

    results = []
    total_saved = 0
    count = 0
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        if path.stat().st_size < MIN_SIZE_KB * 1024:
            continue
        if limit and count >= limit:
            break
        if dry_run:
            results.append({"path": str(path.relative_to(ROOT)), "size_kb": round(path.stat().st_size / 1024, 1)})
            count += 1
            continue
        row = optimize_file(path, use_pillow)
        if row:
            results.append(row)
            total_saved += row.get("saved_kb", 0)
            count += 1
            if count % 50 == 0:
                print(f"  optimized {count}...")

    REPORT.write_text(
        json.dumps(
            {
                "tool": "pillow" if use_pillow else "sips",
                "min_size_kb": MIN_SIZE_KB,
                "optimized_count": len(results),
                "total_saved_kb": round(total_saved, 1),
                "samples": results[:30],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Done. {'Would optimize' if dry_run else 'Optimized'} {len(results)} images, saved ~{total_saved:.0f} KB")
    print(f"Report: {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
