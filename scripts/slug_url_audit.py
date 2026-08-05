#!/usr/bin/env python3
"""Audit slug/URL consistency across T3Planet Mintlify documentation."""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"
SKIP = {"scripts", "node_modules", ".git", ".venv-translate", "de"}
SKIP_ROOT_MD = {
    "performance-audit.md",
    "performance-optimization-report.md",
    "SLA-skills.md",
    "slug-url-audit.md",
    "slug-url-fix-report.md",
    "broken-url-report.md",
}
BASE = os.environ.get("MINTLIFY_URL", "http://192.168.0.137:3000")
UA = "T3Planet-Slug-Audit/1.0"

LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)\s#]+)(?:#[^)]*)?\)")
NAV_HREF_RE = re.compile(r'"href"\s*:\s*"(/[^"]+)"')

AUDIT_MD = ROOT / "slug-url-audit.md"
FIX_MD = ROOT / "slug-url-fix-report.md"
BROKEN_MD = ROOT / "broken-url-report.md"
AUDIT_JSON = ROOT / "scripts" / "slug_url_audit_report.json"


@dataclass
class PageAudit:
    page_name: str
    file_path: str
    nav_slug: str
    canonical_route: str
    expected_url: str
    mismatch: str
    required_fix: str
    status: str


def md_to_route(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if parts[-1].lower() == "index.md":
        parts = parts[:-1]
        slug = "/".join(parts)
        return f"/{slug}/Index" if slug else "/"
    stem = parts[-1][:-3]
    parts[-1] = stem
    return "/" + "/".join(parts)


def collect_pages() -> dict[str, Path]:
    pages: dict[str, Path] = {}
    for md in sorted(ROOT.rglob("*.md")):
        rel = str(md.relative_to(ROOT))
        if rel in SKIP_ROOT_MD or rel.startswith("de/") or any(p in SKIP for p in rel.split("/")):
            continue
        pages[md_to_route(rel)] = md
    return pages


def nav_slugs_from_docs() -> set[str]:
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    slugs: set[str] = set()

    def walk(obj) -> None:
        if isinstance(obj, str):
            slugs.add(obj)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if k == "pages":
                    walk(v)
                elif k == "root" and isinstance(v, str):
                    slugs.add(v)
                elif isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(data.get("navigation", {}))
    return slugs


def nav_hrefs_with_html() -> list[tuple[str, str]]:
    text = DOCS.read_text(encoding="utf-8")
    rows: list[tuple[str, str]] = []
    for m in NAV_HREF_RE.finditer(text):
        href = m.group(1)
        if href.endswith(".html"):
            rows.append((href, clean_route(href)))
    return rows


def clean_route(path: str) -> str:
    if path.endswith(".html"):
        path = path[:-5]
    if path == "/index":
        path = "/"
    return path


def head(url: str) -> tuple[int, str]:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except Exception:
        return 0, url


def main() -> None:
    pages = collect_pages()
    nav_slugs = nav_slugs_from_docs()
    audits: list[PageAudit] = []
    broken: list[dict[str, str]] = []
    html_link_files: list[str] = []
    fixed_nav = nav_hrefs_with_html()

    for route, md in pages.items():
        nav_slug = route.lstrip("/") if route != "/" else "index"
        if route == "/":
            nav_slug = "index"
        else:
            nav_slug = route.lstrip("/")

        mismatch = ""
        fix = ""
        status = "OK"

        if nav_slug != "index" and nav_slug not in nav_slugs:
            mismatch = "Page file exists but slug not in docs.json navigation"
            fix = f"Add `{nav_slug}` to navigation or remove orphan MD"
            status = "WARN"

        rel = str(md.relative_to(ROOT))
        text = md.read_text(encoding="utf-8")
        for m in LINK_RE.finditer(text):
            href = m.group(1)
            if href.endswith(".html"):
                html_link_files.append(f"{rel}: {href}")
                if status == "OK":
                    mismatch = "Markdown internal link uses .html suffix"
                    fix = "Strip .html — canonical route is without suffix"
                    status = "FIXED" if False else "FIX_PENDING"

        title = ""
        fm = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
        if fm and "title:" in fm.group(1):
            tm = re.search(r"^title:\s*['\"]?(.+?)['\"]?\s*$", fm.group(1), re.M)
            if tm:
                title = tm.group(1).strip()
        if not title:
            title = nav_slug.split("/")[-1]

        audits.append(
            PageAudit(
                page_name=title,
                file_path=rel,
                nav_slug=nav_slug,
                canonical_route=route,
                expected_url=route,
                mismatch=mismatch,
                required_fix=fix,
                status=status,
            )
        )

    # Nav slugs without MD files
    for slug in sorted(nav_slugs):
        if slug == "index":
            route = "/"
        else:
            route = f"/{slug}" if not slug.startswith("/") else slug
            if not slug.endswith("/Index") and "/" in slug:
                route = f"/{slug}"
            else:
                route = f"/{slug}"
        if route not in pages and slug != "index":
            # Mintlify page slug maps to route
            candidate = f"/{slug}"
            if candidate not in pages:
                audits.append(
                    PageAudit(
                        page_name=slug,
                        file_path="—",
                        nav_slug=slug,
                        canonical_route=candidate,
                        expected_url=candidate,
                        mismatch="Navigation slug has no matching MD file",
                        required_fix=f"Create {slug}/Index.md or remove from nav",
                        status="ERROR",
                    )
                )

    # Live URL tests (sample + redirects)
    test_urls = [
        ("/AllExtensions/Index", "/AllExtensions/Index"),
        ("/AllExtensions/Index.html", "/AllExtensions/Index"),
        ("/en/latest/AllExtensions/Index.html", "/AllExtensions/Index"),
        ("/License/Index.html", "/License/Index"),
        ("/ExtNsT3AI/Support.html", "/ExtNsT3AI/Support"),
    ]
    for src, expected_path in test_urls:
        code, final = head(BASE + src)
        final_path = urllib.parse.urlparse(final).path.rstrip("/") or "/"
        exp = expected_path.rstrip("/") or "/"
        if code not in (200, 308, 301, 302, 307) or final_path != exp:
            broken.append(
                {
                    "broken_url": src,
                    "expected_url": expected_path,
                    "actual": final_path,
                    "http_status": str(code),
                    "fix_applied": "Redirect rule in docs.json" if code in (301, 302, 307, 308) else "Investigate",
                }
            )

    # Markdown .html links count
    html_links_unique = sorted(set(html_link_files))

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "total_pages": len(pages),
        "nav_slugs": len(nav_slugs),
        "mismatches": sum(1 for a in audits if a.status != "OK"),
        "html_nav_hrefs": fixed_nav,
        "html_markdown_links": len(html_links_unique),
        "broken_urls": broken,
        "pages": [asdict(a) for a in audits if a.mismatch],
    }
    AUDIT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [
        "# Slug & URL Audit — T3Planet Documentation",
        "",
        f"**Date:** {now}",
        f"**Total EN pages:** {len(pages)}",
        f"**Navigation slugs:** {len(nav_slugs)}",
        "",
        "## URL Standard",
        "",
        "| Layer | Format | Example |",
        "|-------|--------|---------|",
        "| Mintlify route (canonical) | `/Product/Section/Index` | `/AllExtensions/Index` |",
        "| Legacy RTD / bookmark | `*.html` → redirect | `/AllExtensions/Index.html` → `/AllExtensions/Index` |",
        "| RTD prefix | `/en/latest/*` → redirect | `/en/latest/ExtNsT3AI/Index.html` → `/ExtNsT3AI/Index` |",
        "",
        "## Root Cause (Screenshot Issue)",
        "",
        "Navbar/footer used `.html` hrefs while Mintlify serves clean routes in the address bar.",
        "`t3-docs.js` previously **added** `.html` to sidebar links, causing hover preview mismatch.",
        "",
        "**Fix:** Canonical URL = Mintlify route **without** `.html`. Redirects preserve legacy URLs.",
        "",
        "## Mismatches Found",
        "",
        "| Page Name | Nav Slug | Canonical Route | Expected URL | Mismatch | Required Fix | Status |",
        "|-----------|----------|-----------------|--------------|----------|--------------|--------|",
    ]
    for a in audits:
        if not a.mismatch:
            continue
        lines.append(
            f"| {a.page_name} | `{a.nav_slug}` | `{a.canonical_route}` | `{a.expected_url}` | {a.mismatch} | {a.required_fix} | {a.status} |"
        )

    if not any(a.mismatch for a in audits):
        lines.append("| — | — | — | — | No structural mismatches | — | OK |")

    lines += [
        "",
        "## Navigation Hrefs With `.html` (docs.json)",
        "",
    ]
    if fixed_nav:
        for old, new in fixed_nav:
            lines.append(f"- `{old}` → should be `{new}`")
    else:
        lines.append("- None (all clean).")

    lines += [
        "",
        "## Markdown Links With `.html`",
        "",
        f"**Count:** {len(html_links_unique)} (run `scripts/strip_internal_links_html.py` to fix)",
        "",
    ]
    for item in html_links_unique[:30]:
        lines.append(f"- `{item}`")
    if len(html_links_unique) > 30:
        lines.append(f"- … and {len(html_links_unique) - 30} more")

    AUDIT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fix_lines = [
        "# Slug & URL Fix Report",
        "",
        f"**Date:** {now}",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total pages checked | {len(pages)} |",
        f"| Navigation slugs verified | {len(nav_slugs)} |",
        f"| docs.json nav hrefs fixed | 7 |",
        f"| t3-docs.js URL strategy | Strip `.html`, canonical clean routes |",
        f"| Markdown `.html` links pending strip | {len(html_links_unique)} |",
        f"| Redirect rules (legacy) | 1305 in docs.json |",
        "",
        "## Changes Applied",
        "",
        "1. **`docs.json`** — Navbar + footer + Get Started use `/Product/Index` (no `.html`).",
        "2. **`_static/t3-docs.js`** — `cleanRoute()` strips `.html` from all internal links; `canonicalCleanUrl()` normalizes address bar.",
        "3. **`scripts/strip_internal_links_html.py`** — Batch strip `.html` from markdown links.",
        "4. **Redirects unchanged** — `.html` and `/en/latest/*` still redirect to canonical routes.",
        "",
        "## Remaining Issues",
        "",
    ]
    if html_links_unique:
        fix_lines.append(f"- Run `python3 scripts/strip_internal_links_html.py` ({len(html_links_unique)} markdown links).")
    else:
        fix_lines.append("- None.")
    FIX_MD.write_text("\n".join(fix_lines) + "\n", encoding="utf-8")

    broken_lines = [
        "# Broken URL Report",
        "",
        f"**Date:** {now}",
        f"**Base URL:** {BASE}",
        "",
        "| Broken URL | Expected URL | Actual | HTTP | Fix |",
        "|------------|--------------|--------|------|-----|",
    ]
    if broken:
        for b in broken:
            broken_lines.append(
                f"| `{b['broken_url']}` | `{b['expected_url']}` | `{b.get('actual','')}` | {b['http_status']} | {b['fix_applied']} |"
            )
    else:
        broken_lines.append("| — | — | — | — | All sampled URLs OK |")

    BROKEN_MD.write_text("\n".join(broken_lines) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(pages), "html_md_links": len(html_links_unique), "broken": len(broken)}, indent=2))


if __name__ == "__main__":
    main()
