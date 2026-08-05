#!/usr/bin/env python3
"""Apply SEO-safe redirects: legacy RTD paths + per-page .html canonical URLs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs.json"
SKIP = {"scripts", "node_modules", ".git", ".venv-translate", "de"}


def md_to_route(rel: str) -> str:
    parts = rel.replace("\\", "/").split("/")
    if parts[-1].lower() == "index.md":
        parts = parts[:-1]
        slug = "/".join(parts)
        return f"/{slug}/Index" if slug else "/"
    stem = parts[-1][:-3]
    parts[-1] = stem
    return "/" + "/".join(parts)


def collect_routes() -> list[str]:
    routes: list[str] = []
    for md in sorted(ROOT.rglob("*.md")):
        rel = str(md.relative_to(ROOT))
        if rel.startswith("de/") or any(part in SKIP for part in rel.split("/")):
            continue
        routes.append(md_to_route(rel))
    return routes


def build_redirects(routes: list[str]) -> list[dict[str, str]]:
    redirects: list[dict[str, str]] = [
        {"source": "/de/:path*", "destination": "/:path*"},
        {"source": "/de/index", "destination": "/"},
        {"source": "/de", "destination": "/"},
        {"source": "/en/latest", "destination": "/"},
        {"source": "/en/latest/", "destination": "/"},
        {"source": "/en/latest/index.html", "destination": "/"},
        {"source": "/en/latest/:path*", "destination": "/:path*"},
        {"source": "/en/:path*", "destination": "/:path*"},
        {"source": "/index", "destination": "/"},
        {"source": "/index/Index", "destination": "/"},
        {"source": "/readme", "destination": "/"},
        {"source": "/readme/Index", "destination": "/"},
        {"source": "/history", "destination": "/"},
        {"source": "/history/Index", "destination": "/"},
    ]
    seen: set[str] = set()

    def add(source: str, destination: str) -> None:
        if source in seen or source == destination:
            return
        seen.add(source)
        redirects.append({"source": source, "destination": destination})

    for route in routes:
        if route == "/":
            add("/index.html", "/")
            continue

        # Canonical .html URL -> Mintlify route (Support.html, Index.html, etc.)
        add(f"{route}.html", route)

        # Legacy RTD shorthand: /Product/Section.html -> /Product/Section/Index
        if route.endswith("/Index"):
            shorthand = route[: -len("/Index")] + ".html"
            add(shorthand, route)

    return redirects


def main() -> None:
    routes = collect_routes()
    redirects = build_redirects(routes)
    data = json.loads(DOCS.read_text(encoding="utf-8"))
    data["redirects"] = redirects
    DOCS.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {len(redirects)} redirects ({len(routes)} EN pages).")

    from compute_doc_stats import write_stats_json

    write_stats_json()


if __name__ == "__main__":
    main()
