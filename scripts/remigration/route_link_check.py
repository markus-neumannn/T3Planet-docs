#!/usr/bin/env python3
"""
Phase 4 - Validate every docs.json route/redirect and all internal links.

Checks:
  1. Every navigation path in docs.json resolves to an actual .md/.mdx file.
  2. Every redirect source/destination is well-formed; destinations resolve to
     a real nav page (or another redirect); no redirect points a page at its
     own parent index (the License Activation bug class); no duplicate sources.
  3. Every internal markdown link ([text](/path)) found in content resolves to
     a known nav path, a redirect source, or an on-disk file.
  4. HTTP-checks every nav route against the local preview (localhost:3000).

Output: scripts/remigration/route_link_report.json + .md
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_JSON = ROOT / "docs.json"
OUT_JSON = Path(__file__).resolve().parent / "route_link_report.json"
OUT_MD = Path(__file__).resolve().parent / "route_link_report.md"
BASE_URL = os.environ.get("MINT_BASE", "http://localhost:3000")

SKIP_TOP = {"docs", "scripts", ".git", "node_modules", "de", "live-docs", ".venv-translate", "visual-regression"}


def load_docs_json() -> dict:
    return json.loads(DOCS_JSON.read_text(encoding="utf-8"))


def collect_nav_paths(nav) -> set[str]:
    """Walk only 'pages' arrays (Mintlify nav schema): each entry is either a
    page-path string, or a nested {'group', 'pages': [...]} object. Other keys
    like 'group', 'icon', 'tab' are labels/metadata, not routes."""
    paths = set()

    def walk_pages(pages):
        for entry in pages:
            if isinstance(entry, str):
                if entry.startswith("http://") or entry.startswith("https://"):
                    continue
                paths.add(entry if entry.startswith("/") else "/" + entry)
            elif isinstance(entry, dict) and "pages" in entry:
                walk_pages(entry["pages"])

    def walk(o):
        if isinstance(o, dict):
            if "pages" in o and isinstance(o["pages"], list):
                walk_pages(o["pages"])
            for k, v in o.items():
                if k == "pages":
                    continue
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(nav)
    return paths


def path_to_file(path: str) -> Path | None:
    p = path.lstrip("/")
    if p == "" or p == "index":
        p = "index"
    for ext in (".md", ".mdx"):
        candidate = ROOT / (p + ext)
        if candidate.exists():
            return candidate
    return None


def wildcard_prefix_exists(dst: str) -> bool:
    """Handle Next.js-style wildcard destinations like /Foo/:path* by checking
    that at least one real page exists under that prefix."""
    prefix = dst.split(":path*")[0].strip("/")
    if not prefix:
        return True
    folder = ROOT / prefix
    if folder.is_dir():
        return any(folder.rglob("*.md")) or any(folder.rglob("*.mdx"))
    return False


def main() -> None:
    data = load_docs_json()
    nav_paths = collect_nav_paths(data.get("navigation"))
    redirects = data.get("redirects", [])

    print(f"Nav paths discovered: {len(nav_paths)}")
    print(f"Redirect entries: {len(redirects)}")

    # 1. Nav paths -> file existence
    nav_missing_file = []
    for p in sorted(nav_paths):
        if not path_to_file(p):
            nav_missing_file.append(p)

    # 2. Redirect sanity
    seen_sources = {}
    dup_sources = []
    self_redirect = []
    redirect_to_parent_of_self = []
    redirect_dest_unresolved = []
    nav_path_set_norm = {p.rstrip("/") for p in nav_paths}

    for r in redirects:
        src = r.get("source", "")
        dst = r.get("destination", "")
        if src in seen_sources and seen_sources[src] != dst:
            dup_sources.append({"source": src, "dest1": seen_sources[src], "dest2": dst})
        seen_sources[src] = dst

        dst_norm = dst.rstrip("/")
        # Only a real bug if src == dst verbatim (ignoring trailing slash) -
        # legacy `.html` sources demangling to a clean dest is intentional.
        if not src.endswith(".html") and src.rstrip("/") == dst_norm:
            self_redirect.append(r)

        # Bug class: /Foo/Bar redirecting to /Foo/Index instead of /Foo/Bar/Index
        src_norm = src.rstrip("/").replace(".html", "")
        if dst_norm.endswith("/Index") and not dst_norm.startswith(src_norm + "/") and src_norm != dst_norm[:-len("/Index")]:
            parent_of_src = "/".join(src_norm.split("/")[:-1])
            if dst_norm == parent_of_src + "/Index" and src_norm.split("/")[-1].lower() != "index":
                redirect_to_parent_of_self.append(r)

        if not (dst.startswith("http://") or dst.startswith("https://")):
            if dst_norm in ("", "/"):
                continue
            if ":path*" in dst:
                if not wildcard_prefix_exists(dst):
                    redirect_dest_unresolved.append(r)
                continue
            if dst_norm not in nav_path_set_norm and dst_norm not in seen_sources and not path_to_file(dst):
                redirect_dest_unresolved.append(r)

    # 3. Internal link extraction across all .md/.mdx files
    md_link_re = re.compile(r"\[[^\]]*\]\((/[^)\s#]+)(#[^)]*)?\)")
    broken_internal_links: list[dict] = []
    total_internal_links = 0
    files_scanned = 0

    known_targets = set(p.rstrip("/") for p in nav_paths) | set(seen_sources.keys())

    for dp, dirs, files in os.walk(ROOT):
        rel_dir = str(Path(dp).relative_to(ROOT)).replace("\\", "/")
        top = rel_dir.split("/")[0].lower() if rel_dir != "." else ""
        if rel_dir == ".":
            dirs[:] = [d for d in dirs if d.lower() not in SKIP_TOP and not d.startswith(".")]
        elif top in SKIP_TOP:
            dirs[:] = []
            continue
        for f in files:
            if not (f.endswith(".md") or f.endswith(".mdx")):
                continue
            fp = Path(dp) / f
            text = fp.read_text(encoding="utf-8", errors="replace")
            files_scanned += 1
            for m in md_link_re.finditer(text):
                link = m.group(1)
                total_internal_links += 1
                link_norm = link.rstrip("/")
                if link_norm in known_targets:
                    continue
                if path_to_file(link):
                    continue
                broken_internal_links.append({
                    "file": str(fp.relative_to(ROOT)),
                    "link": link,
                })

    # 4. HTTP check every nav path against local preview
    http_results = []
    http_failures = []

    def http_status(path: str) -> int:
        url = BASE_URL + path
        try:
            req = urllib.request.Request(url, method="GET", headers={"User-Agent": "route-check/1.0"})
            with urllib.request.urlopen(req, timeout=25) as resp:
                return resp.status
        except urllib.error.HTTPError as e:
            return e.code
        except Exception:
            return 0

    check_paths = sorted(nav_paths)
    print(f"HTTP-checking {len(check_paths)} nav paths against {BASE_URL} ...")
    for i, p in enumerate(check_paths):
        code = http_status(p)
        if code == 0:
            code = http_status(p)  # one retry for transient local-server hiccups
        http_results.append({"path": p, "code": code})
        if code not in (200,):
            http_failures.append({"path": p, "code": code})
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(check_paths)} checked, {len(http_failures)} failures so far")

    report = {
        "nav_paths": len(nav_paths),
        "redirects": len(redirects),
        "nav_missing_file": nav_missing_file,
        "dup_redirect_sources": dup_sources,
        "self_redirects": self_redirect,
        "redirect_to_parent_of_self": redirect_to_parent_of_self,
        "redirect_dest_unresolved": redirect_dest_unresolved[:50],
        "redirect_dest_unresolved_count": len(redirect_dest_unresolved),
        "files_scanned_for_links": files_scanned,
        "total_internal_links": total_internal_links,
        "broken_internal_links": broken_internal_links,
        "http_failures": http_failures,
        "http_checked": len(check_paths),
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = ["# Route & Link Validation Report", ""]
    lines.append(f"- Nav paths: **{len(nav_paths)}**")
    lines.append(f"- Redirect entries: **{len(redirects)}**")
    lines.append(f"- Nav paths missing a file: **{len(nav_missing_file)}**")
    lines.append(f"- Duplicate redirect sources (conflicting dest): **{len(dup_sources)}**")
    lines.append(f"- Self-redirects: **{len(self_redirect)}**")
    lines.append(f"- Redirect-to-parent-of-self (License Activation bug class): **{len(redirect_to_parent_of_self)}**")
    lines.append(f"- Redirect destinations unresolved: **{len(redirect_dest_unresolved)}**")
    lines.append(f"- Files scanned for internal links: **{files_scanned}**")
    lines.append(f"- Total internal markdown links found: **{total_internal_links}**")
    lines.append(f"- Broken internal links: **{len(broken_internal_links)}**")
    lines.append(f"- Nav paths HTTP-checked: **{len(check_paths)}**")
    lines.append(f"- HTTP failures (non-200): **{len(http_failures)}**")
    lines.append("")

    if nav_missing_file:
        lines.append("## Nav paths missing a file")
        for p in nav_missing_file:
            lines.append(f"- `{p}`")
        lines.append("")
    if dup_sources:
        lines.append("## Duplicate redirect sources")
        for d in dup_sources:
            lines.append(f"- `{d['source']}` -> `{d['dest1']}` vs `{d['dest2']}`")
        lines.append("")
    if self_redirect:
        lines.append("## Self redirects")
        for r in self_redirect:
            lines.append(f"- {r}")
        lines.append("")
    if redirect_to_parent_of_self:
        lines.append("## Redirect-to-parent-of-self (bug class)")
        for r in redirect_to_parent_of_self:
            lines.append(f"- {r}")
        lines.append("")
    if redirect_dest_unresolved:
        lines.append(f"## Unresolved redirect destinations (showing {min(50,len(redirect_dest_unresolved))} of {len(redirect_dest_unresolved)})")
        for r in redirect_dest_unresolved[:50]:
            lines.append(f"- `{r['source']}` -> `{r['destination']}`")
        lines.append("")
    if broken_internal_links:
        lines.append(f"## Broken internal links ({len(broken_internal_links)})")
        for b in broken_internal_links:
            lines.append(f"- `{b['file']}` -> `{b['link']}`")
        lines.append("")
    if http_failures:
        lines.append(f"## HTTP failures ({len(http_failures)})")
        for h in http_failures:
            lines.append(f"- `{h['path']}` -> {h['code']}")
        lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[:20]))


if __name__ == "__main__":
    main()
