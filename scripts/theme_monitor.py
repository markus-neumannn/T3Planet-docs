#!/usr/bin/env python3
"""Continuous dark/light theme compatibility monitor for T3Planet docs."""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

BASE = os.environ.get("DOCS_URL", "http://localhost:3333")
INTERVAL = int(os.environ.get("THEME_INTERVAL", "30"))

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


def fetch(path: str) -> tuple[int, str]:
    req = urllib.request.Request(BASE + path)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status, r.read().decode("utf-8", errors="replace")


def check_page(path: str) -> dict:
    try:
        status, html = fetch(path)
        return {
            "path": path,
            "status": status,
            "has_custom_css": "custom.css" in html or "--t3-primary" in html,
            "has_scripts": "language-switcher.js" in html,
            "has_dark_support": "dark" in html[:3000],
            "title_ok": "<title>" in html and "T3Planet" in html,
            "ok": status == 200,
        }
    except Exception as e:
        return {"path": path, "ok": False, "error": str(e)}


def run_cycle(cycle: int) -> dict:
    results = [check_page(p) for p in SAMPLE_PATHS]
    failed = [r for r in results if not r.get("ok")]
    return {
        "cycle": cycle,
        "time": datetime.now(timezone.utc).isoformat(),
        "base": BASE,
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": failed,
        "all_ok": len(failed) == 0,
    }


def main():
    cycle = 0
    print(f"[theme-monitor] Watching {BASE} every {INTERVAL}s (Ctrl+C to stop)", flush=True)
    while True:
        cycle += 1
        report = run_cycle(cycle)
        line = (
            f"[{report['time']}] cycle={cycle} "
            f"passed={report['passed']}/{report['total']} "
            f"base={BASE}"
        )
        if report["all_ok"]:
            print(f"{line} OK", flush=True)
        else:
            print(f"{line} FAIL {json.dumps(report['failed'])}", flush=True)
        sys.stdout.flush()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
