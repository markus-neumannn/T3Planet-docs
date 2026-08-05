#!/usr/bin/env python3
"""Audit migrated .md pages: find empty/thin pages and compare to source RST."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path("/Users/nitsan/www/Mintilify Doc")
RST_ROOT = Path("/Users/nitsan/www/T3Planet Docs/docs/docs")


def body_of(md_text: str) -> str:
    if md_text.startswith("---"):
        parts = md_text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return md_text.strip()


def strip_headings(body: str) -> str:
    lines = [ln for ln in body.splitlines() if not ln.strip().startswith("#")]
    return "\n".join(lines).strip()


def rst_body_len(rst_path: Path) -> int:
    try:
        txt = rst_path.read_text(encoding="utf-8")
    except Exception:
        return 0
    # remove directives/underlines roughly
    txt = re.sub(r"^\s*\.\..*$", "", txt, flags=re.MULTILINE)
    txt = re.sub(r"^[=\-~^`#'\"]{3,}$", "", txt, flags=re.MULTILINE)
    return len(txt.strip())


def main() -> None:
    empties = []
    thin = []
    total = 0
    for md in sorted(ROOT.rglob("*.md")):
        if "scripts" in md.parts or "de" in md.parts or "docs-master-md" in md.parts:
            continue
        if md.name == "index.md" and md.parent == ROOT:
            continue
        total += 1
        body = body_of(md.read_text(encoding="utf-8"))
        content = strip_headings(body)
        rel = md.relative_to(ROOT)

        # map back to RST
        rst = RST_ROOT / str(rel).replace(".md", ".rst")
        rlen = rst_body_len(rst) if rst.exists() else -1

        if len(content) == 0:
            empties.append({"page": str(rel), "rst_len": rlen, "rst_exists": rst.exists()})
        elif len(content) < 40:
            thin.append({"page": str(rel), "content_len": len(content), "rst_len": rlen})

    report = {
        "total_pages": total,
        "empty_count": len(empties),
        "thin_count": len(thin),
        "empties": empties,
        "thin": thin,
    }
    (ROOT / "audit-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Total EN pages: {total}")
    print(f"Empty (no body): {len(empties)}")
    print(f"Thin (<40 chars): {len(thin)}")
    print("\n-- EMPTY --")
    for e in empties[:60]:
        print(f"  {e['page']}  (rst_exists={e['rst_exists']}, rst_len={e['rst_len']})")
    print("\n-- THIN --")
    for t in thin[:60]:
        print(f"  {t['page']}  content={t['content_len']} rst_len={t['rst_len']}")


if __name__ == "__main__":
    main()
