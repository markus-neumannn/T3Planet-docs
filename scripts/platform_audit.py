#!/usr/bin/env python3
"""Full platform audit: live HTTP routes, SEO frontmatter, footer/nav links."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")
REPORT = ROOT / "scripts" / "platform_audit_report.json"
WORKERS = int(os.environ.get("AUDIT_WORKERS", "3"))

PRIORITY_PREFIXES = [
    "ExtNsT3AI", "ExtNsT3AC", "ExtNsT3AS", "ExtNsT3AL", "ExtNsT3AA", "ExtNsT3AB",
    "EXTKarma", "ExtThemes", "License",
]

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)


def collect_nav_paths() -> list[str]:
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    paths: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "pages" and isinstance(v, list):
                    for p in v:
                        if isinstance(p, str):
                            route = "/" + p.replace(".md", "").replace("index", "")
                            if route == "/":
                                paths.add("/")
                            else:
                                paths.add(route)
                else:
                    walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(docs["navigation"])
    return sorted(paths)


def fetch(path: str) -> dict:
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "T3Planet-Platform-Audit/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", errors="replace")
            return {
                "path": path,
                "status": r.status,
                "ok": r.status == 200,
                "has_title": "<title>" in html,
                "has_og": 'property="og:' in html or "og:title" in html,
                "error": None,
            }
    except urllib.error.HTTPError as e:
        return {"path": path, "status": e.code, "ok": False, "error": str(e)}
    except Exception as e:
        return {"path": path, "status": 0, "ok": False, "error": str(e)}


def audit_seo() -> dict:
    missing_desc = []
    missing_title = []
    for md in ROOT.rglob("*.md"):
        if any(s in md.parts for s in ("scripts", "node_modules", ".git", ".venv-translate")):
            continue
        text = md.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(text)
        if not m:
            missing_title.append(str(md.relative_to(ROOT)))
            continue
        fm = m.group(1)
        if "title:" not in fm:
            missing_title.append(str(md.relative_to(ROOT)))
        if "description:" not in fm:
            missing_desc.append(str(md.relative_to(ROOT)))
    return {
        "missing_title": len(missing_title),
        "missing_description": len(missing_desc),
        "samples_title": missing_title[:10],
        "samples_desc": missing_desc[:10],
    }


def main():
    paths = collect_nav_paths()
    priority = [p for p in paths if any(x in p for x in PRIORITY_PREFIXES)]
    sample = priority[:80] if "--sample" in sys.argv else paths

    print(f"[platform] Checking {len(sample)} routes at {BASE}", flush=True)
    results = []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch, p): p for p in sample}
        for i, fut in enumerate(as_completed(futures), 1):
            results.append(fut.result())
            if i % 100 == 0 or i == len(sample):
                failed = sum(1 for r in results if not r.get("ok"))
                print(f"[platform] {i}/{len(sample)} checked, failed={failed}", flush=True)

    failed = [r for r in results if not r.get("ok")]
    seo = audit_seo()
    report = {
        "base": BASE,
        "summary": {
            "routes_checked": len(results),
            "http_failed": len(failed),
            "http_passed": len(results) - len(failed),
            "seo": seo,
        },
        "failed_routes": failed[:100],
        "priority_failures": [r for r in failed if any(p in r["path"] for p in PRIORITY_PREFIXES)],
    }
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
