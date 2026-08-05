#!/usr/bin/env python3
"""Run full documentation performance suite: Playwright audit + Lighthouse + reports."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_playwright_audit(base: str) -> dict:
    subprocess.run(
        [sys.executable, str(SCRIPTS / "performance_audit.py"), base],
        check=True,
        cwd=ROOT,
    )
    return json.loads((SCRIPTS / "performance_audit_report.json").read_text(encoding="utf-8"))


def run_lighthouse(base: str, path: str = "/") -> dict | None:
    out = SCRIPTS / "lighthouse_latest.json"
    url = base.rstrip("/") + path
    cmd = [
        "npx",
        "--yes",
        "lighthouse",
        url,
        "--only-categories=performance,accessibility,seo",
        f"--output-path={out}",
        "--output=json",
        "--chrome-flags=--headless --no-sandbox",
        "--quiet",
    ]
    try:
        subprocess.run(cmd, check=True, cwd=ROOT, timeout=180)
        return json.loads(out.read_text(encoding="utf-8"))
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"Lighthouse skipped: {exc}", file=sys.stderr)
        return None


def lighthouse_scores(lh: dict | None) -> dict[str, float | None]:
    if not lh:
        return {}
    cats = lh.get("categories", {})
    audits = lh.get("audits", {})
    return {
        "performance": round((cats.get("performance") or {}).get("score", 0) * 100),
        "accessibility": round((cats.get("accessibility") or {}).get("score", 0) * 100),
        "seo": round((cats.get("seo") or {}).get("score", 0) * 100),
        "fcp_ms": (audits.get("first-contentful-paint") or {}).get("numericValue"),
        "lcp_ms": (audits.get("largest-contentful-paint") or {}).get("numericValue"),
        "cls": (audits.get("cumulative-layout-shift") or {}).get("numericValue"),
        "tbt_ms": (audits.get("total-blocking-time") or {}).get("numericValue"),
        "tti_ms": (audits.get("interactive") or {}).get("numericValue"),
    }


def find_large_images(limit_mb: float = 0.3) -> list[dict]:
    rows: list[dict] = []
    for p in ROOT.rglob("*"):
        if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            continue
        if "node_modules" in p.parts or p.parts[0] == "scripts":
            continue
        size = p.stat().st_size
        if size >= limit_mb * 1024 * 1024:
            rows.append({"path": str(p.relative_to(ROOT)), "kb": round(size / 1024, 1)})
    rows.sort(key=lambda r: r["kb"], reverse=True)
    return rows[:30]


def write_frontend_report(base: str, audit: dict, lh_scores: dict) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    s = audit["summary"]
    lines = [
        "# Frontend Performance Report",
        "",
        f"**Generated:** {now}",
        f"**Base URL:** {base}",
        "",
        "## Console & Network Errors",
        "",
    ]
    errs = audit.get("console_errors_sample") or []
    if errs:
        for e in errs[:15]:
            lines.append(f"- `{e}`")
    else:
        lines.append("- No console errors captured in sample.")
    lines += [
        "",
        "## Lighthouse (homepage, mobile)",
        "",
        "| Metric | Value |",
        "|--------|-------|",
    ]
    for k, v in lh_scores.items():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Slow Pages (cold DOM, Playwright)",
        "",
        "| Page | DOM (ms) | Transfer (KB) | CLS |",
        "|------|----------|---------------|-----|",
    ]
    for p in sorted(audit["pages"], key=lambda x: x["dom_ms"], reverse=True):
        lines.append(
            f"| {p['label']} | {p['dom_ms']} | {p.get('transfer_kb', '—')} | {p.get('cls', '—')} |"
        )
    large = find_large_images()
    if large:
        lines += ["", "## Large Images (>300 KB)", "", "| File | Size (KB) |", "|------|-----------|"]
        for row in large:
            lines.append(f"| `{row['path']}` | {row['kb']} |")
    (SCRIPTS / "frontend-performance-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:3000"
    print(f"Running Playwright audit against {base}...")
    audit = run_playwright_audit(base)
    print("Running Lighthouse (homepage)...")
    lh = run_lighthouse(base)
    scores = lighthouse_scores(lh)
    write_frontend_report(base, audit, scores)
    print(json.dumps({"audit_summary": audit["summary"], "lighthouse": scores}, indent=2))
    print(f"Wrote {SCRIPTS / 'frontend-performance-report.md'}")


if __name__ == "__main__":
    main()
