#!/usr/bin/env python3
"""Full QA validation for AI Foundation Mintlify documentation."""
from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "T3AF"
DOCS = ROOT / "docs.json"
BASE = "http://localhost:3000"
REPORT_JSON = ROOT / "scripts" / "ai_universe_qa_report.json"
REPORT_MD = ROOT / "scripts" / "AI_UNIVERSE_QA_REPORT.md"

# Original upload filenames (migrated to T3AF/; source folder removed)
MIGRATED_SOURCE_COUNT = 26

FEATURE_PAGES = {
    "Dashboard/Index", "AIProviders/Index", "T3PlanetCredits/Index", "MCPServer/Index",
    "MCPTools/Index", "AIContext/Index", "AIPrompts/Index", "AIFeatures/Index",
    "AIUsageAndLogs/Index", "GovernanceAndAccess/Index", "SetupWizard/Index",
    "Installation/Index", "Configuration/Index", "WhatDoesItDo/Index",
}


@dataclass
class PageQA:
    path: str
    has_frontmatter: bool
    has_description: bool
    has_supademo_or_todo: bool
    internal_links: int
    broken_links: list[str]
    http_status: int | None
    word_count: int


def collect_nav_slugs() -> set[str]:
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    slugs: set[str] = set()

    def walk(obj) -> None:
        if isinstance(obj, str):
            if obj.startswith("T3AF"):
                slugs.add(obj)
        elif isinstance(obj, dict):
            if obj.get("group") == "AI Foundation Foundation" or obj.get("root", "").startswith("T3AF"):
                pass
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    for g in data["navigation"]["groups"]:
        if g.get("group") == "AI Foundation":
            walk(g)
    return slugs


def route_exists(href: str, routes: set[str]) -> bool:
    if not href.startswith("/T3AF"):
        return True
    clean = href.rstrip("/")
    if clean in routes:
        return True
    if clean + "/Index" in routes:
        return True
    rel = clean.lstrip("/")
    return (ROOT / rel / "Index.md").exists() or (ROOT / f"{rel}.md").exists()


def head(url: str) -> int:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "T3AF-QA/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def audit_page(md: Path, routes: set[str]) -> PageQA:
    text = md.read_text(encoding="utf-8")
    rel = md.relative_to(DEST).as_posix()
    if rel == "Index.md":
        route = "/T3AF/Index"
    elif rel.endswith("/Index.md"):
        route = f"/T3AF/{rel[:-9]}/Index"
    else:
        route = f"/T3AF/{rel}"
    has_fm = text.startswith("---\n")
    has_desc = "description:" in text[:500]
    has_demo = "supademo.com" in text or "TODO: Replace with AI Foundation Supademo" in text
    links = re.findall(r"\]\((/T3AF/[^)\s#]+)", text)
    broken = [l for l in links if not route_exists(l, routes)]
    status = head(BASE + route) if route.startswith("/T3AF") else None
    words = len(re.findall(r"\w+", text))
    return PageQA(route, has_fm, has_desc, has_demo, len(links), broken, status, words)


def main() -> None:
    routes: set[str] = set()
    for md in DEST.rglob("*.md"):
        rel = md.relative_to(ROOT).as_posix()
        if rel == "T3AF/Index.md":
            routes.add("/T3AF/Index")
        elif rel.endswith("/Index.md"):
            routes.add("/" + rel[:-9])

    pages = sorted(DEST.rglob("*.md"))
    results = [audit_page(p, routes) for p in pages]
    nav = collect_nav_slugs()
    mint_paths = {p.relative_to(DEST).as_posix().replace("/Index.md", "").replace("Index.md", "Index") for p in pages}
    mint_slugs = set()
    for p in mint_paths:
        if p == "Index":
            mint_slugs.add("T3AF/Index")
        else:
            mint_slugs.add(f"T3AF/{p}/Index")

    orphans = sorted(mint_slugs - nav)
    missing_nav = sorted(nav - mint_slugs - {"T3AF/Index"})

    supademo_missing = [
        r.path for r in results
        if any(r.path.endswith(f"/{fp.replace('/Index', '')}/Index") or r.path.endswith(f"/{fp}") for fp in FEATURE_PAGES)
        and not r.has_supademo_or_todo
    ]

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "source_pages": MIGRATED_SOURCE_COUNT,
        "mintlify_pages": len(pages),
        "nav_slugs": len(nav),
        "orphan_pages": orphans,
        "missing_from_nav": missing_nav,
        "broken_links_total": sum(len(r.broken_links) for r in results),
        "http_failures": [r.path for r in results if r.http_status not in (200, None)],
        "pages": [asdict(r) for r in results],
        "supademo_missing": supademo_missing,
    }
    REPORT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# AI Foundation — Documentation QA Report",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Summary",
        "",
        f"| Check | Result |",
        f"|-------|--------|",
        f"| Source pages migrated | {MIGRATED_SOURCE_COUNT} |",
        f"| Mintlify pages | {len(pages)} |",
        f"| Nav entries (AI Foundation Foundation) | {len(nav)} |",
        f"| Broken internal links | {payload['broken_links_total']} |",
        f"| HTTP failures (sample) | {len(payload['http_failures'])} |",
        f"| Orphan pages | {len(orphans)} |",
        f"| All pages have frontmatter | {all(r.has_frontmatter for r in results)} |",
        f"| All pages have description | {all(r.has_description for r in results)} |",
        "",
        "## Page Status",
        "",
        "| Route | HTTP | Words | Links | Demo |",
        "|-------|------|-------|-------|------|",
    ]
    for r in results:
        demo = "✅" if r.has_supademo_or_todo else "—"
        http = r.http_status or "—"
        lines.append(f"| `{r.path}` | {http} | {r.word_count} | {r.internal_links} | {demo} |")

    if payload["http_failures"]:
        lines += ["", "## HTTP Failures", ""]
        for p in payload["http_failures"]:
            lines.append(f"- `{p}`")

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in payload.items() if k != "pages"}, indent=2))


if __name__ == "__main__":
    main()
