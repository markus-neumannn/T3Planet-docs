#!/usr/bin/env python3
"""Final pre-manager QA: crawl every nav page on local Mintlify + content checks.

Outputs:
  scripts/FINAL_MANAGER_QA_REPORT.md
  scripts/final-manager-qa.json
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = os.environ.get("MINTLIFY_URL", "http://127.0.0.1:3000").rstrip("/")
LIVE = os.environ.get("LIVE_DOCS_URL", "https://docs.t3planet.de/en/latest").rstrip("/")
OUT_JSON = ROOT / "scripts" / "final-manager-qa.json"
OUT_MD = ROOT / "scripts" / "FINAL_MANAGER_QA_REPORT.md"
UA = "T3Planet-FinalManagerQA/1.0"

PLACEHOLDER_RE = re.compile(
    r"\b(TODO|FIXME|TBD|lorem ipsum|coming soon|placeholder|xxx+|\[insert|under construction)\b",
    re.I,
)
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
MD_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_IMG_RE = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']", re.I)
HTML_HREF_RE = re.compile(r"<a[^>]+href=[\"']([^\"']+)[\"']", re.I)


def load_nav_pages() -> list[str]:
    data = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    pages: set[str] = set()

    def walk(obj):
        if isinstance(obj, dict):
            for p in obj.get("pages") or []:
                if isinstance(p, str) and not p.startswith("http"):
                    pages.add(p.strip("/"))
                else:
                    walk(p)
            for key in ("groups", "tabs", "anchors"):
                walk(obj.get(key))
            for k, v in obj.items():
                if k not in ("pages", "groups", "tabs", "anchors"):
                    walk(v)
        elif isinstance(obj, list):
            for x in obj:
                walk(x)

    walk(data.get("navigation"))
    # home
    pages.add("index")
    out = []
    for p in sorted(pages):
        out.append("/" + p if not p.startswith("/") else p)
    return out


def fetch(url: str, timeout: int = 90) -> tuple[int, float, int, str]:
    t0 = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            code = getattr(resp, "status", None) or resp.getcode()
            elapsed = time.time() - t0
            return int(code), elapsed, len(body), body.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        body = e.read() if e.fp else b""
        return int(e.code), elapsed, len(body), body.decode("utf-8", "replace")
    except Exception as e:
        elapsed = time.time() - t0
        return 0, elapsed, 0, str(e)


def looks_blank(html: str) -> bool:
    if len(html) < 800:
        return True
    text = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text) < 80


def path_to_md(path: str) -> Path | None:
    rel = path.strip("/")
    if rel in ("", "index"):
        return ROOT / "index.md"
    candidates = [
        ROOT / f"{rel}.md",
        ROOT / rel / "Index.md",
        ROOT / rel / "index.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def scan_markdown() -> dict:
    issues = {
        "missing_md_for_nav": [],
        "empty_or_thin": [],
        "placeholders": [],
        "broken_images": [],
        "broken_internal_links": [],
    }
    nav = load_nav_pages()
    for path in nav:
        md = path_to_md(path)
        if not md:
            # redirects may cover some; still flag
            issues["missing_md_for_nav"].append(path)
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        body = text
        if body.startswith("---"):
            parts = body.split("---", 2)
            if len(parts) >= 3:
                body = parts[2]
        content = re.sub(r"^#+\s+.*$", "", body, flags=re.M).strip()
        if len(content) < 40:
            issues["empty_or_thin"].append({"path": path, "file": str(md.relative_to(ROOT)), "len": len(content)})
        for m in PLACEHOLDER_RE.finditer(body):
            # skip common false positives in code/URLs
            snip = body[max(0, m.start() - 40) : m.end() + 40].replace("\n", " ")
            if "http" in snip.lower() and m.group(0).lower() in ("xxx",):
                continue
            issues["placeholders"].append({"path": path, "match": m.group(0), "snippet": snip[:120]})

        # images
        imgs = MD_IMG_RE.findall(body) + HTML_IMG_RE.findall(body)
        for src in imgs:
            src = src.strip().split()[0].strip("\"'")
            if src.startswith(("http://", "https://", "data:", "//")):
                continue
            # relative to md file
            target = (md.parent / src).resolve()
            if not target.exists():
                # also try from root
                alt = (ROOT / src.lstrip("/")).resolve()
                if not alt.exists():
                    issues["broken_images"].append({"path": path, "src": src})

        # internal md links
        for href in MD_LINK_RE.findall(body) + HTML_HREF_RE.findall(body):
            href = href.strip().split()[0].strip("\"'")
            if href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            if href.startswith(("http://", "https://", "//")):
                continue
            clean = href.split("#")[0].split("?")[0]
            if not clean:
                continue
            target = (md.parent / clean).resolve()
            if target.exists():
                continue
            # try as docs route (.md / Index.md)
            route = clean.lstrip("/")
            if route.endswith(".md"):
                route = route[:-3]
            candidates = [
                ROOT / f"{route}.md",
                ROOT / route / "Index.md",
                ROOT / route / "index.md",
                ROOT / route,
            ]
            if any(c.exists() for c in candidates):
                continue
            issues["broken_internal_links"].append({"path": path, "href": href})

    # dedupe placeholders lightly
    seen = set()
    uniq = []
    for p in issues["placeholders"]:
        key = (p["path"], p["match"].lower())
        if key in seen:
            continue
        seen.add(key)
        uniq.append(p)
    issues["placeholders"] = uniq
    return issues


def http_crawl(paths: list[str], workers: int = 6) -> dict:
    results = []
    failures = []
    blank = []
    slow = []
    runtime_err = []

    def one(path: str):
        url = BASE + path
        code, elapsed, size, html = fetch(url)
        row = {
            "path": path,
            "code": code,
            "elapsed_s": round(elapsed, 3),
            "bytes": size,
            "blank": False,
            "error_markers": [],
        }
        if code != 200:
            # follow simple redirect manually for reporting
            if code in (301, 302, 307, 308):
                row["note"] = "redirect"
            else:
                failures.append(row)
        else:
            if looks_blank(html):
                row["blank"] = True
                blank.append(row)
            low = html.lower()
            markers = []
            for needle in (
                "application error",
                "internal server error",
                "uncaught",
                "something went wrong",
                "page not found",
                "404 not found",
            ):
                if needle in low:
                    markers.append(needle)
            row["error_markers"] = markers
            if markers:
                runtime_err.append(row)
            if elapsed > 8:
                slow.append(row)
        return row

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one, p): p for p in paths}
        for i, fut in enumerate(as_completed(futs), 1):
            results.append(fut.result())
            if i % 50 == 0:
                print(f"  crawled {i}/{len(paths)}", flush=True)

    ok = [r for r in results if r["code"] == 200 and not r["blank"] and not r["error_markers"]]
    times = [r["elapsed_s"] for r in results if r["code"] == 200]
    times.sort()
    perf = {}
    if times:
        perf = {
            "count": len(times),
            "p50": times[len(times) // 2],
            "p90": times[int(len(times) * 0.9)],
            "p99": times[min(len(times) - 1, int(len(times) * 0.99))],
            "max": times[-1],
            "avg": round(sum(times) / len(times), 3),
        }
    return {
        "results": results,
        "ok_count": len(ok),
        "failures": failures,
        "blank": blank,
        "slow": slow,
        "runtime_err": runtime_err,
        "perf": perf,
    }


def live_spot_check(sample: list[str]) -> list[dict]:
    """Compare a sample of local pages against live Sphinx equivalents when mappable."""
    out = []
    for path in sample:
        local_code, local_t, _, _ = fetch(BASE + path, timeout=60)
        # Heuristic live path: /en/latest/<path>/ or without Index
        live_path = path
        if live_path.endswith("/Index"):
            live_path = live_path[: -len("/Index")] + "/"
        elif live_path.endswith("/index"):
            live_path = live_path[: -len("/index")] + "/"
        else:
            live_path = live_path.rstrip("/") + "/"
        live_url = LIVE + live_path
        live_code, live_t, _, _ = fetch(live_url, timeout=60)
        out.append(
            {
                "path": path,
                "local": {"code": local_code, "ttfb_s": round(local_t, 3)},
                "live": {"url": live_url, "code": live_code, "ttfb_s": round(live_t, 3)},
            }
        )
    return out


def write_report(report: dict) -> None:
    md = []
    md.append("# Final Manager QA Report — Mintlify Docs")
    md.append("")
    md.append(f"**Generated:** {report['generated_at']}")
    md.append(f"**Local base:** `{report['base']}`")
    md.append(f"**Live base:** `{report['live']}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- Nav pages crawled: **{report['nav_page_count']}**")
    md.append(f"- HTTP 200 OK (non-blank): **{report['http']['ok_count']}**")
    md.append(f"- HTTP failures: **{len(report['http']['failures'])}**")
    md.append(f"- Blank pages: **{len(report['http']['blank'])}**")
    md.append(f"- Runtime error markers: **{len(report['http']['runtime_err'])}**")
    md.append(f"- Slow pages (>8s): **{len(report['http']['slow'])}**")
    md.append(f"- Missing MD for nav: **{len(report['content']['missing_md_for_nav'])}**")
    md.append(f"- Empty/thin pages: **{len(report['content']['empty_or_thin'])}**")
    md.append(f"- Placeholder matches: **{len(report['content']['placeholders'])}**")
    md.append(f"- Broken images (MD): **{len(report['content']['broken_images'])}**")
    md.append(f"- Broken internal links (MD): **{len(report['content']['broken_internal_links'])}**")
    md.append("")
    perf = report["http"].get("perf") or {}
    if perf:
        md.append("## Performance (local HTTP HTML)")
        md.append("")
        md.append(f"- Avg: {perf['avg']}s | p50: {perf['p50']}s | p90: {perf['p90']}s | p99: {perf['p99']}s | max: {perf['max']}s")
        md.append("")
    md.append("## Recommendation")
    md.append("")
    md.append(f"**{report['recommendation']}**")
    md.append("")
    md.append(report.get("recommendation_notes", ""))
    md.append("")

    def section(title: str, rows: list, limit: int = 40):
        md.append(f"## {title}")
        md.append("")
        if not rows:
            md.append("_None_")
            md.append("")
            return
        for r in rows[:limit]:
            md.append(f"- `{json.dumps(r, ensure_ascii=False)[:240]}`")
        if len(rows) > limit:
            md.append(f"- … and {len(rows) - limit} more")
        md.append("")

    section("HTTP failures", report["http"]["failures"])
    section("Blank pages", report["http"]["blank"])
    section("Runtime markers", report["http"]["runtime_err"])
    section("Slow pages", report["http"]["slow"])
    section("Missing MD", report["content"]["missing_md_for_nav"])
    section("Empty/thin", report["content"]["empty_or_thin"])
    section("Placeholders", report["content"]["placeholders"], 60)
    section("Broken images", report["content"]["broken_images"], 60)
    section("Broken internal links", report["content"]["broken_internal_links"], 80)
    section("Live spot checks", report.get("live_spot") or [], 30)

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    # slim JSON (drop full results body list optionally keep summary)
    slim = dict(report)
    slim["http"] = {
        **report["http"],
        "results": [
            r
            for r in report["http"]["results"]
            if r["code"] != 200 or r["blank"] or r["error_markers"] or r["elapsed_s"] > 5
        ],
        "all_count": len(report["http"]["results"]),
    }
    OUT_JSON.write_text(json.dumps(slim, indent=2), encoding="utf-8")


def main() -> None:
    print(f"Base={BASE}")
    paths = load_nav_pages()
    print(f"Nav pages: {len(paths)}")
    print("Scanning markdown…")
    content = scan_markdown()
    print(
        "MD issues:",
        {k: len(v) for k, v in content.items()},
    )
    print("HTTP crawl…")
    http = http_crawl(paths, workers=int(os.environ.get("QA_WORKERS", "6")))
    print("HTTP done:", {k: (len(v) if isinstance(v, list) else v) for k, v in http.items() if k != "results"})

    sample = [
        "/",
        "/index",
        "/T3AF/Index",
        "/AllExtensions/Index",
        "/AllTemplates/Index",
        "/License/Index",
        "/ExtNsT3AA/Index",
        "/ExtNsT3AI/Index",
        "/EXTAvatar/Index",
        "/ExtNsT3AA/CkeditorAccessibilityChecker/Index",
    ]
    sample = [p for p in sample if p in paths or p in ("/", "/index")]
    # ensure listed even if path form differs
    for p in list(sample):
        if p not in paths and p not in ("/", "/index"):
            sample.remove(p)
    live_spot = live_spot_check(
        [
            "/T3AF/Index",
            "/AllExtensions/Index",
            "/License/Index",
            "/ExtNsT3AA/Index",
            "/EXTAvatar/Index",
        ]
    )

    critical = (
        len(http["failures"])
        + len(http["blank"])
        + len(http["runtime_err"])
        + len([p for p in content["empty_or_thin"] if p.get("len", 0) == 0])
        + len(content["broken_images"])
    )
    high = len(content["broken_internal_links"]) + len(content["placeholders"]) + len(http["slow"])

    if critical == 0 and high == 0:
        rec = "Ready for Manager Review"
        notes = "No critical or high-priority automated findings. Manual UI/responsive checks still required in report body."
    elif critical == 0:
        rec = "Conditional — Ready after high-priority cleanup"
        notes = f"{high} high-priority items remain (links/placeholders/slow). Fix before final manager share if they affect demos."
    else:
        rec = "Not ready — critical issues remain"
        notes = f"{critical} critical findings must be fixed and re-tested."

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "live": LIVE,
        "nav_page_count": len(paths),
        "http": http,
        "content": content,
        "live_spot": live_spot,
        "recommendation": rec,
        "recommendation_notes": notes,
        "critical_count": critical,
        "high_count": high,
    }
    write_report(report)
    print("Wrote", OUT_MD)
    print("Wrote", OUT_JSON)
    print("RECOMMENDATION:", rec)


if __name__ == "__main__":
    main()
