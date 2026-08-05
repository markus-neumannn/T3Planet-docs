#!/usr/bin/env python3
"""Compare old RTD docs (docs.t3planet.de) slugs with current Mintlify documentation."""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RST_ROOT = ROOT / "Live-docs" / "docs"
REPORT = ROOT / "scripts" / "crawl_compare_report.json"
OLD_BASE = "https://docs.t3planet.de/en/latest"
NEW_BASE = os.environ.get("MINTLIFY_URL", "http://127.0.0.1:3000")

SKIP_DIRS = {"scripts", "node_modules", ".git", ".venv-translate", "logo", "_snippets", "de"}


def rst_to_mintlify_slug(rst_path: Path) -> str:
    rel = rst_path.relative_to(RST_ROOT)
    parts = list(rel.parts)
    stem = parts[-1].replace(".rst", "")
    if stem in {"Index", "Support", "BuyNow", "GetThisExtension"}:
        parts = parts[:-1]
    else:
        parts[-1] = stem
    if not parts:
        return ""
    return "/".join(parts)


def old_url_paths(slug: str) -> list[str]:
    if not slug:
        return ["/en/latest/index.html", "/en/latest/"]
    product, *rest = slug.split("/", 1)
    paths = [f"/en/latest/{product}/Index.html"]
    if rest:
        joined = rest[0]
        paths.append(f"/en/latest/{product}/{joined}/Index.html")
        paths.append(f"/en/latest/{product}/{joined}.html")
    return paths


def mintlify_route(slug: str) -> str:
    if not slug:
        return "/"
    if slug.endswith("/Index"):
        return f"/{slug}"
    return f"/{slug}/Index"


def collect_rst_slugs() -> dict[str, list[str]]:
    slugs: dict[str, list[str]] = {}
    for rst in RST_ROOT.rglob("*.rst"):
        slug = rst_to_mintlify_slug(rst)
        slugs.setdefault(slug, []).append(str(rst.relative_to(RST_ROOT)))
    return slugs


def collect_mintlify_slugs() -> set[str]:
    out: set[str] = set()
    for md in ROOT.rglob("*.md"):
        if any(p in md.parts for p in SKIP_DIRS):
            continue
        rel = md.relative_to(ROOT)
        parts = list(rel.parts)
        if parts[-1].lower() in ("index.md", "readme.md"):
            parts = parts[:-1]
        else:
            parts[-1] = parts[-1].replace(".md", "")
        slug = "/".join(parts) if parts else ""
        out.add(slug)
    return out


def collect_nav_slugs() -> set[str]:
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    pages: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "pages" and isinstance(v, list):
                    for p in v:
                        if isinstance(p, str):
                            pages.add(p.replace(".md", "").replace("/Index", "").rstrip("/"))
                else:
                    walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(docs["navigation"])
    en_only = {p for p in pages if not p.startswith("de/")}
    return en_only


def http_check(url: str, timeout: int = 15) -> int:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "T3Planet-Crawl/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def main():
    rst_slugs = collect_rst_slugs()
    md_slugs = collect_mintlify_slugs()
    nav_slugs = collect_nav_slugs()

    rst_set = set(rst_slugs.keys())
    missing_in_mintlify = sorted(rst_set - md_slugs)
    extra_in_mintlify = sorted(md_slugs - rst_set)

    # Normalize: Index pages may differ by trailing /Index
    def norm(s: str) -> str:
        return s.replace("/Index", "").rstrip("/")

    missing_norm = [s for s in missing_in_mintlify if norm(s) not in {norm(m) for m in md_slugs}]

    redirect_candidates = []
    for slug in sorted(rst_set & md_slugs):
        route = mintlify_route(slug)
        for old in old_url_paths(slug):
            redirect_candidates.append({"source": old, "destination": route})

    # Sample HTTP validation on priority slugs
    priority = [s for s in rst_set if any(x in s for x in (
        "ExtNsT3AI", "ExtNsT3AC", "ExtNsT3AS", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB",
        "License", "EXTKarma", "ExtThemes",
    ))]
    http_samples = []
    for slug in priority[:30]:
        route = mintlify_route(slug)
        old = old_url_paths(slug)[0] if old_url_paths(slug) else "/en/latest/"
        http_samples.append({
            "slug": slug,
            "old_url": OLD_BASE + old.replace("/en/latest", ""),
            "new_route": route,
            "new_status": http_check(NEW_BASE + route),
        })

    report = {
        "counts": {
            "rst_pages": len(rst_set),
            "mintlify_en_pages": len(md_slugs),
            "nav_en_pages": len(nav_slugs),
            "matched_slugs": len(rst_set & md_slugs),
            "missing_in_mintlify": len(missing_norm),
            "extra_in_mintlify": len(extra_in_mintlify),
        },
        "missing_in_mintlify": [
            {"slug": s, "rst_files": rst_slugs[s], "expected_route": mintlify_route(s)}
            for s in missing_norm[:50]
        ],
        "extra_in_mintlify_sample": extra_in_mintlify[:30],
        "redirect_count": len(redirect_candidates),
        "http_sample": http_samples,
        "slug_mapping_examples": [
            {"old": old_url_paths(s), "new": mintlify_route(s)}
            for s in sorted(rst_set)[:10]
        ],
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    (ROOT / "scripts" / "redirect_map.json").write_text(
        json.dumps(redirect_candidates[:500], indent=2), encoding="utf-8"
    )
    print(json.dumps(report["counts"], indent=2))
    if missing_norm:
        print("\nMissing (first 10):")
        for s in missing_norm[:10]:
            print(f"  {s} -> {mintlify_route(s)}")


if __name__ == "__main__":
    main()
