#!/usr/bin/env python3
"""Surgical merge migrator: apply reconcile report deltas from live/Sphinx into Mintlify.

Preserves CardGroups, frontmatter, and Mintlify MDX. Does not full-file overwrite.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_BASE = Path("/Users/nitsan/www/AI Agents")
ROOT = Path(__file__).resolve().parents[2]

RECONCILE_JSON = ROOT / "scripts/qa-final/LIVE_CONTENT_RECONCILE_AUG12.json"
OUT_JSON = ROOT / "scripts/qa-final/LIVE_CONTENT_MIGRATION_AUG12.json"
OUT_MD = ROOT / "scripts/qa-final/LIVE_CONTENT_MIGRATION_AUG12.md"

# Import remigrate module for shared migration functions
_rem_path = ROOT / "scripts/qa-final/remigrate_t3ac_t3as_t3af_aug10.py"
_spec = importlib.util.spec_from_file_location("remigrate", _rem_path)
_rem = importlib.util.module_from_spec(_spec)
sys.modules["remigrate"] = _rem
_spec.loader.exec_module(_rem)

# Import remigrate module for shared migration functions
create_page_from_live = _rem.create_page_from_live
mint_path_for = _rem.mint_path_for
get_html = _rem.get_html
extract_live = _rem.extract_live
extract_mint = _rem.extract_mint
missing_sections = _rem.missing_sections
sync_supademos = _rem.sync_supademos
sync_images = _rem.sync_images
append_missing_sections = _rem.append_missing_sections
html_to_md_body = _rem.html_to_md_body
add_nav_pages = _rem.add_nav_pages


def needs_migration(row: dict[str, Any]) -> bool:
    status = row.get("status") or []
    if "NEW_PAGE" in status:
        return True
    if "fetch_failed" in status and "NEW_PAGE" in status:
        return True
    if any(
        s in status
        for s in (
            "MISSING_CONTENT",
            "UPDATED",
            "MEDIA_DIFFERENCE",
            "LINK_DIFFERENCE",
        )
    ):
        return True
    if row.get("thin"):
        return True
    return False


def migrate_row(row: dict[str, Any], actions: dict[str, Any]) -> bool:
    doc = row["live"]
    status = row.get("status") or []

    if "NEW_PAGE" in status or (row.get("mint") is None):
        print(f"CREATE {doc}")
        try:
            path = create_page_from_live(doc)
            actions["pages_created"].append(doc)
            actions["files_modified"].append(str(path.relative_to(ROOT)))
            actions["nav_added"].extend(add_nav_pages([doc]))
            return True
        except Exception as exc:
            actions["errors"].append({"live": doc, "error": str(exc)})
            return False

    mint_rel = row.get("mint")
    if not mint_rel:
        return False
    md = ROOT / mint_rel
    if not md.is_file():
        try:
            path = create_page_from_live(doc)
            actions["pages_created"].append(doc)
            actions["files_modified"].append(str(path.relative_to(ROOT)))
            return True
        except Exception as exc:
            actions["errors"].append({"live": doc, "error": str(exc)})
            return False

    # Skip pure structural hub pages
    if status == ["STRUCTURAL_DIFFERENCE"]:
        return False

    try:
        html, _src = get_html(doc)
    except Exception as exc:
        actions["errors"].append({"live": doc, "error": str(exc)})
        return False

    changed = False

    miss_sup = row.get("missing_supademo") or []
    if miss_sup:
        added = sync_supademos(doc, miss_sup, md, html)
        if added:
            actions["supademos_added"][doc] = added
            changed = True

    miss_img = row.get("missing_images") or []
    if miss_img:
        added = sync_images(doc, miss_img, md, html)
        if added:
            actions["images_added"][doc] = added
            changed = True

    miss_sec = row.get("missing_sections") or []
    thin = row.get("thin", False)
    code_diff = row.get("code_diff") or {}
    link_diff = row.get("link_diff") or {}

    if miss_sec or thin or code_diff.get("has_diff") or link_diff.get("has_diff"):
        if miss_sec:
            added = append_missing_sections(doc, miss_sec, md, html)
            if added:
                actions["sections_added"][doc] = added
                changed = True
        elif thin or code_diff.get("has_diff"):
            live_ex = extract_live(html)
            mint_ex = extract_mint(md)
            miss = missing_sections(live_ex["headings"], mint_ex["headings"])
            if miss:
                added = append_missing_sections(doc, miss, md, html)
                if added:
                    actions["sections_added"][doc] = added
                    changed = True
            elif thin:
                title, body = html_to_md_body(html, doc, md)
                raw = md.read_text(encoding="utf-8")
                if "## Full documentation content" not in raw and len(body) > 400:
                    md.write_text(
                        raw.rstrip() + "\n\n---\n\n## Full documentation content\n\n" + body,
                        encoding="utf-8",
                    )
                    actions["sections_added"][doc] = ["(full live body appended)"]
                    changed = True

    if changed:
        actions["pages_updated"].append(doc)
        rel = str(md.relative_to(ROOT))
        if rel not in actions["files_modified"]:
            actions["files_modified"].append(rel)
    return changed


def run_migrate(rows: list[dict[str, Any]], dry_run: bool = False) -> dict[str, Any]:
    actions: dict[str, Any] = {
        "pages_created": [],
        "pages_updated": [],
        "supademos_added": {},
        "images_added": {},
        "sections_added": {},
        "nav_added": [],
        "files_modified": [],
        "errors": [],
        "skipped": [],
    }
    to_migrate = [r for r in rows if needs_migration(r)]
    print(f"Pages needing migration: {len(to_migrate)} / {len(rows)}")

    if dry_run:
        actions["would_migrate"] = [r["live"] for r in to_migrate]
        return actions

    created_slugs: list[str] = []
    for row in to_migrate:
        if migrate_row(row, actions):
            if row["live"] in actions["pages_created"]:
                created_slugs.append(row["live"])

    if created_slugs:
        nav = add_nav_pages(created_slugs)
        for s in nav:
            if s not in actions["nav_added"]:
                actions["nav_added"].append(s)
        if "docs.json" not in actions["files_modified"] and nav:
            actions["files_modified"].append("docs.json")

    return actions


def write_md(report: dict[str, Any]) -> None:
    actions = report["actions"]
    lines = [
        "# Live Content Migration — August 12, 2026",
        "",
        f"**Generated:** {report['generated']}",
        f"**Repo:** `{report['repo']}`",
        "",
        "## Summary",
        "",
        f"- pages_created: **{len(actions['pages_created'])}**",
        f"- pages_updated: **{len(actions['pages_updated'])}**",
        f"- nav_added: **{len(actions['nav_added'])}**",
        f"- errors: **{len(actions['errors'])}**",
        "",
        "## Created pages",
        "",
    ]
    for p in actions["pages_created"]:
        lines.append(f"- `{p}`")
    lines += ["", "## Updated pages", ""]
    for p in actions["pages_updated"]:
        lines.append(f"- `{p}`")
    lines += ["", "## Files modified", ""]
    for f in actions["files_modified"]:
        lines.append(f"- `{f}`")
    if actions["errors"]:
        lines += ["", "## Errors", ""]
        for e in actions["errors"][:30]:
            lines.append(f"- `{e['live']}`: {e['error']}")
    lines.append("")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Surgical migrate from reconcile report")
    parser.add_argument("--dry-run", action="store_true", help="List pages only, no writes")
    parser.add_argument("--report", type=Path, default=RECONCILE_JSON, help="Reconcile JSON path")
    args = parser.parse_args()

    if not args.report.is_file():
        print(f"Missing reconcile report: {args.report}")
        print("Run live_content_reconcile_aug12.py first")
        return 1

    data = json.loads(args.report.read_text(encoding="utf-8"))
    rows = data.get("pages") or []
    actions = run_migrate(rows, dry_run=args.dry_run)

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "repo": str(ROOT),
        "reconcile_report": str(args.report),
        "actions": actions,
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_md(report)
    print(f"Wrote {OUT_JSON}")
    print(f"Wrote {OUT_MD}")
    print(
        f"Created: {len(actions.get('pages_created', []))}, "
        f"Updated: {len(actions.get('pages_updated', []))}, "
        f"Errors: {len(actions.get('errors', []))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
