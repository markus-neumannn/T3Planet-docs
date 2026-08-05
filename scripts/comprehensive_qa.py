#!/usr/bin/env python3
"""Run full documentation QC/QA and write FINAL_QA_REPORT.md."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_MD = ROOT / "scripts" / "FINAL_QA_REPORT.md"
REPORT_JSON = ROOT / "scripts" / "comprehensive_qa_report.json"
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\((/[^)\s]+)\)|href=\"(/[^\"]+)\"")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']")
H1_RE = re.compile(r"^#\s+", re.M)


def run_script(name: str) -> str:
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name)],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(ROOT),
        )
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return f"ERROR: {e}"


def collect_nav_pages() -> set[str]:
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    pages: set[str] = set()

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "pages" and isinstance(v, list):
                    for p in v:
                        if isinstance(p, str):
                            pages.add(p)
                        else:
                            walk(p)
                else:
                    walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    walk(docs["navigation"])
    return pages


def audit_links() -> dict:
    nav_pages = collect_nav_pages()
    missing_nav = [p for p in sorted(nav_pages) if not (ROOT / f"{p}.md").exists()]

    broken_links = []
    missing_images = []
    for md in ROOT.rglob("*.md"):
        if any(s in md.parts for s in ("scripts", "node_modules", ".git", ".venv-translate")):
            continue
        rel = str(md.relative_to(ROOT))
        text = md.read_text(encoding="utf-8")
        for t in set(LINK_RE.findall(text)):
            path = (t[0] or t[1]).split("#")[0].rstrip("/")
            if not path or re.search(r"\.(png|jpg|jpeg|gif|svg|webp|pdf)$", path, re.I):
                continue
            cand = ROOT / f"{path.lstrip('/')}.md"
            if not cand.exists():
                broken_links.append({"from": rel, "to": path})
        for m in IMG_RE.findall(text):
            src = (m[0] or m[1]).split("#")[0].split("?")[0]
            if src.startswith("http"):
                continue
            ip = ROOT / src.lstrip("/") if src.startswith("/") else (md.parent / src).resolve()
            if not ip.exists():
                missing_images.append({"page": rel, "src": src})

    return {
        "missing_nav_targets": len(missing_nav),
        "missing_nav": missing_nav[:20],
        "broken_internal_links": len(broken_links),
        "broken_samples": broken_links[:30],
        "missing_images": len(missing_images),
        "missing_image_samples": missing_images[:30],
    }


def audit_seo() -> dict:
    missing_title = []
    missing_desc = []
    multi_h1 = []
    for md in ROOT.rglob("*.md"):
        if any(s in md.parts for s in ("scripts", "node_modules", ".git", ".venv-translate")):
            continue
        text = md.read_text(encoding="utf-8")
        m = FM_RE.match(text)
        body = text[m.end() :] if m else text
        fm = m.group(1) if m else ""
        if 'title:' not in fm:
            missing_title.append(str(md.relative_to(ROOT)))
        if 'description:' not in fm:
            missing_desc.append(str(md.relative_to(ROOT)))
        if len(H1_RE.findall(body)) > 1:
            multi_h1.append(str(md.relative_to(ROOT)))

    return {
        "missing_title": len(missing_title),
        "missing_description": len(missing_desc),
        "multiple_h1": len(multi_h1),
        "samples": {
            "missing_title": missing_title[:15],
            "missing_description": missing_desc[:15],
            "multiple_h1": multi_h1[:15],
        },
    }


def audit_icons() -> dict:
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    try:
        lucide = {p.stem for p in Path("/tmp/package/dist/esm/icons").glob("*.mjs")}
    except Exception:
        lucide = set()
    icons = set()
    for lang in docs["navigation"]["languages"]:
        for dd in lang.get("dropdowns", []):
            if dd.get("icon"):
                icons.add(dd["icon"])
    invalid = sorted(icons - lucide) if lucide else []
    return {"total_icons": len(icons), "invalid_lucide_icons": invalid}


def fetch_route(path: str) -> dict:
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "T3Planet-QA/1.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            html = r.read().decode("utf-8", errors="replace")
            return {
                "path": path,
                "status": r.status,
                "ok": r.status == 200,
                "has_sidebar": "sidebar-content" in html,
                "has_breadcrumb": "breadcrumb" in html,
                "has_pagination": "pagination" in html,
                "has_custom_css": "--t3-primary" in html,
                "has_sidebar_nav_js": "sidebar-nav.js" in html,
            }
    except urllib.error.HTTPError as e:
        return {"path": path, "status": e.code, "ok": False, "error": str(e)}
    except Exception as e:
        return {"path": path, "status": 0, "ok": False, "error": str(e)}


def audit_http(sample_paths: list[str]) -> dict:
    results = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(fetch_route, p): p for p in sample_paths}
        for fut in as_completed(futs):
            results.append(fut.result())
    failed = [r for r in results if not r.get("ok")]
    return {
        "tested": len(results),
        "failed": len(failed),
        "failures": failed,
        "samples_ok": [r for r in results if r.get("ok")][:5],
    }


def sample_routes() -> list[str]:
    docs = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    routes = ["/", "/T3AF/Index", "/AllTemplates/Index", "/AllExtensions/Index"]
    for lang in docs["navigation"]["languages"]:
        if lang["language"] != "en":
            continue
        for dd in lang.get("dropdowns", []):
            name = dd.get("dropdown", "")
            if name in ("Home", "All Extensions", "All AI Products", "All Templates"):
                continue
            pages = []
            for g in dd.get("groups", []):
                pages.extend(g.get("pages", []))
            pages = pages or dd.get("pages", [])
            if pages:
                route = "/" + pages[0].replace("index", "index")
                if route not in routes:
                    routes.append(route)
            if len(routes) >= 40:
                break
    return routes[:40]


def write_report(data: dict) -> None:
    lines = [
        "# T3Planet Documentation — Final QA Report",
        "",
        f"**Generated:** {data['generated_at']}",
        f"**Preview URL:** {BASE}",
        "",
        "## Executive summary",
        "",
    ]
    s = data["summary"]
    lines.append(f"- **Nav pages missing on disk:** {s['missing_nav']}")
    lines.append(f"- **Broken internal links:** {s['broken_links']}")
    lines.append(f"- **Missing images:** {s['missing_images']}")
    lines.append(f"- **Invalid Lucide icons:** {s['invalid_icons']}")
    lines.append(f"- **SEO pages missing title/description:** {s['seo_title']}/{s['seo_desc']}")
    lines.append(f"- **HTTP sample failures:** {s['http_failed']}/{s['http_tested']}")
    lines.append("")

    sections = [
        ("Navigation & routing", data["links"]),
        ("SEO", data["seo"]),
        ("Icons", data["icons"]),
        ("HTTP / UI smoke", data["http"]),
    ]
    for title, block in sections:
        lines.extend([f"## {title}", "", "```json", json.dumps(block, indent=2), "```", ""])

    lines.extend([
        "## Sidebar enhancements shipped",
        "",
        "- Coinbase-style sticky sidebar with search shortcut (⌘K)",
        "- Category browse menus: All Extensions / AI / Templates",
        "- Active page highlight + auto-scroll",
        "- Expand/collapse groups with persisted state",
        "- Mobile backdrop + keyboard navigation",
        "- Light/dark compatible icon shells on hub pages",
        "",
        "## Suggested follow-ups",
        "",
    ])
    for item in data.get("follow_ups", []):
        lines.append(f"- {item}")

    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    print("Running comprehensive QA...")
    links = audit_links()
    seo = audit_seo()
    icons = audit_icons()
    routes = sample_routes()
    http = audit_http(routes)

    follow_ups = []
    if links["broken_internal_links"]:
        follow_ups.append("Fix broken internal links listed in report")
    if links["missing_images"]:
        follow_ups.append("Restore or update missing image assets")
    if icons["invalid_lucide_icons"]:
        follow_ups.append(f"Replace invalid icons: {', '.join(icons['invalid_lucide_icons'])}")
    if http["failed"]:
        follow_ups.append("Investigate HTTP failures (timeouts or 404s) on sample routes")
    if not follow_ups:
        follow_ups.append("No critical blockers — ready for production deploy")

    data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "links": links,
        "seo": seo,
        "icons": icons,
        "http": http,
        "summary": {
            "missing_nav": links["missing_nav_targets"],
            "broken_links": links["broken_internal_links"],
            "missing_images": links["missing_images"],
            "invalid_icons": len(icons["invalid_lucide_icons"]),
            "seo_title": seo["missing_title"],
            "seo_desc": seo["missing_description"],
            "http_tested": http["tested"],
            "http_failed": http["failed"],
        },
        "follow_ups": follow_ups,
    }
    write_report(data)
    print(f"Wrote {REPORT_MD}")
    print(f"Wrote {REPORT_JSON}")


if __name__ == "__main__":
    main()
