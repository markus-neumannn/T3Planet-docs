#!/usr/bin/env python3
"""Sync all Images/ folders from RST source to migrated Mintlify paths."""

from __future__ import annotations

import shutil
from pathlib import Path

from rst_to_mdx import OUT_ROOT, RST_ROOT, product_slug

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


def copy_images(src: Path, dst: Path) -> int:
    count = 0
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.rglob("*"):
        if item.is_file() and item.suffix.lower() in IMAGE_EXT:
            rel = item.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copy2(item, target)
                count += 1
    return count


def main() -> None:
    total = 0
    for product_dir in sorted(RST_ROOT.iterdir()):
        if not product_dir.is_dir() or product_dir.name.startswith("_"):
            continue
        if not (product_dir / "Index.rst").exists():
            continue

        out_base = OUT_ROOT / product_slug(product_dir.name)
        for images_dir in product_dir.rglob("Images"):
            if "_build" in images_dir.parts:
                continue
            rel = images_dir.relative_to(product_dir)
            dst = out_base / rel
            total += copy_images(images_dir, dst)

        for images_dir in product_dir.rglob("images"):
            if "_build" in images_dir.parts:
                continue
            rel = images_dir.relative_to(product_dir)
            dst = out_base / rel
            total += copy_images(images_dir, dst)

    print(f"Synced {total} new image files")


if __name__ == "__main__":
    main()
