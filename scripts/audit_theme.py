#!/usr/bin/env python3
"""Audit documentation pages for dark/light theme contrast issues."""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = os.environ.get("MINTLIFY_URL", "http://localhost:3333")

SAMPLE_PATHS = [
    "/",
    "/License/UpdateVersion/CheckNewVersion/Index",
    "/EXTKarma/Installation/Index",
    "/ExtThemes/Customization/Index",
    "/ExtNsT3AI/AISettings/Index",
    "/ExtNsT3AC/FeatureGuide/Chatbot/Index",
    "/ExtNsHelpDesk/Introduction/Index",
    "/de/",
    "/de/License/UpdateVersion/CheckNewVersion/Index",
    "/de/ExtNsT3AI/AISettings/Index",
]

ISSUE_PATTERNS = [
    (r'color:\s*#(000|000000|333|333333)\b', "hardcoded dark text color"),
    (r'background:\s*#(fff|ffffff|f5f5f5)\b', "hardcoded white background"),
    (r"aspectRatio:\s*'[\d.]+'", "inline embed style (use t3-embed class)"),
    (r'Index\.html', "legacy .html link in source"),
]


def audit_sources():
    issues = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in {"scripts", "node_modules", ".git"}]
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            rel = str(Path(dp, fn).relative_to(ROOT))
            text = open(Path(dp, fn), encoding="utf-8").read()
            for pat, label in ISSUE_PATTERNS:
                if re.search(pat, text, re.I):
                    issues.append({"file": rel, "issue": label})
    return issues


def check_pages():
    results = []
    for path in SAMPLE_PATHS:
        try:
            req = urllib.request.Request(BASE + path)
            with urllib.request.urlopen(req, timeout=30) as r:
                html = r.read().decode("utf-8", errors="replace")
                results.append({
                    "path": path,
                    "status": r.status,
                    "has_dark_class": 'class="' in html and "dark" in html.split("<html")[1][:200],
                    "has_custom_css": "custom.css" in html or "--t3-primary" in html,
                    "title_ok": "<title>" in html,
                })
        except Exception as e:
            results.append({"path": path, "error": str(e)})
    return results


def main():
    source_issues = audit_sources()
    page_results = check_pages()
    report = {"source_issues": source_issues[:50], "source_issue_count": len(source_issues), "pages": page_results}
    print(json.dumps(report, indent=2))
    failed = [p for p in page_results if p.get("error") or p.get("status") != 200]
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
