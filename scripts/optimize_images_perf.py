#!/usr/bin/env python3
"""Create WebP siblings for large doc images without deleting originals.

- Never deletes PNG/JPEG/GIF
- Writes/updates .webp next to source when missing or stale
- Rewrites Markdown image refs to .webp when a sibling exists (same visual)

Skips: .git, Live-docs, visual-regression, de/, scripts/, node_modules
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {
    ".git",
    "Live-docs",
    "visual-regression",
    "de",
    "scripts",
    "node_modules",
    ".venv-translate",
    ".review-frames",
    "docs",
}
MIN_BYTES = 80_000  # only compress heavier rasters
CWEBP_Q = 78


def should_skip(path: Path) -> bool:
    return any(p in SKIP_PARTS for p in path.parts)


def find_cwebp() -> str | None:
    return shutil.which("cwebp")


def convert(src: Path, dest: Path, cwebp: str) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        cwebp,
        "-quiet",
        "-q",
        str(CWEBP_Q),
        "-m",
        "4",
        str(src),
        "-o",
        str(dest),
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return dest.exists() and dest.stat().st_size > 0
    except subprocess.CalledProcessError:
        return False


def rewrite_md_refs() -> tuple[int, int]:
    """Point Markdown image refs at existing .webp siblings. Returns (files, refs)."""
    files = 0
    refs = 0
    pat = re.compile(r"(!\[[^\]]*\]\()([^)\s]+\.(?:png|jpe?g|gif))(\))", re.I)
    for md in ROOT.rglob("*.md"):
        if should_skip(md):
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")

        def repl(m: re.Match[str]) -> str:
            nonlocal refs
            rel = m.group(2)
            full = (md.parent / rel).resolve()
            if not full.exists():
                return m.group(0)
            webp = full.with_suffix(".webp")
            if not webp.exists():
                return m.group(0)
            # Keep relative path shape; only change extension
            new_rel = str(Path(rel).with_suffix(".webp")).replace("\\", "/")
            if new_rel == rel:
                return m.group(0)
            refs += 1
            return m.group(1) + new_rel + m.group(3)

        new_text, n = pat.subn(repl, text)
        # subn counts all matches; we need only successful — recompute
        if new_text != text:
            md.write_text(new_text, encoding="utf-8")
            files += 1
    return files, refs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--min-bytes", type=int, default=MIN_BYTES)
    ap.add_argument("--limit", type=int, default=0, help="Max conversions (0=all)")
    args = ap.parse_args()

    cwebp = find_cwebp()
    if not cwebp:
        print("ERROR: cwebp not found (brew install webp)", file=sys.stderr)
        return 1

    candidates: list[Path] = []
    for pattern in ("*.png", "*.jpg", "*.jpeg"):
        for f in ROOT.rglob(pattern):
            if should_skip(f):
                continue
            if f.stat().st_size < args.min_bytes:
                continue
            webp = f.with_suffix(".webp")
            if webp.exists() and webp.stat().st_mtime >= f.stat().st_mtime:
                continue
            candidates.append(f)

    candidates.sort(key=lambda p: -p.stat().st_size)
    if args.limit:
        candidates = candidates[: args.limit]

    print(f"Candidates to (re)encode: {len(candidates)}")
    created = 0
    saved = 0
    for src in candidates:
        dest = src.with_suffix(".webp")
        before = src.stat().st_size
        if args.dry_run:
            print(f"DRY {before/1024:.0f}KB → {src.relative_to(ROOT)}")
            continue
        if convert(src, dest, cwebp):
            after = dest.stat().st_size
            created += 1
            saved += max(0, before - after)
            print(
                f"OK {before/1024:.0f}KB → {after/1024:.0f}KB webp "
                f"({src.relative_to(ROOT)})"
            )
        else:
            print(f"FAIL {src.relative_to(ROOT)}", file=sys.stderr)

    if not args.dry_run:
        files, refs = rewrite_md_refs()
        print(f"Markdown updated: {files} files, {refs} image refs → webp")
    print(f"Created/updated webp: {created}; bytes saved vs source: {saved/1024/1024:.1f}MB")
    print("Original PNG/JPEG files kept (not deleted).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
