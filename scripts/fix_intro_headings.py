#!/usr/bin/env python3
"""Replace ## EXT:ns_* headings with NS readable names in introduction pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

from rename_extension_labels import format_extension_display_name


def main() -> None:
    updated = 0
    for md in ROOT.rglob("**/Introduction/Index.md"):
        if "scripts" in md.parts:
            continue
        text = md.read_text(encoding="utf-8")
        new = re.sub(
            r"^## (EXT:[^\n]+)$",
            lambda m: f"## {format_extension_display_name(m.group(1).strip())}",
            text,
            flags=re.M,
        )
        if new != text:
            md.write_text(new, encoding="utf-8")
            updated += 1
            print(md.relative_to(ROOT))
    print(f"Updated {updated} introduction headings")


if __name__ == "__main__":
    main()
