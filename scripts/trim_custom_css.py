#!/usr/bin/env python3
"""Trim dead CSS blocks and consolidate dark-mode rules."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "custom.css"

# Remove entire comment-delimited blocks (start marker -> next major section)
REMOVE_MARKERS = [
    "/* Dropdown menu items */",
    "/* Language switch feedback */",
    "/* ── Extension list (lightweight catalog) ─",
    "/* ── Search + filter controls (removed from sidebar) ─",
    "/* Product dropdown removed — unified Coinbase-style sidebar */",
]

# Consolidated dark text — replaces many individual .dark #content rules
DARK_CONSOLIDATED = """
/* ── Dark mode: consolidated text (performance) ───────────────── */
.dark :is(#page-title, header h1, #header h1, .sidebar-title, .sidebar-group-header,
  #sidebar-content h2, #sidebar-content h3, #table-of-contents h2, #table-of-contents-content h2,
  .prose, .prose p, .prose li, .prose h1, .prose h2, .prose h3, .prose h4, .prose h5, .prose h6,
  .prose strong, #content, .mdx-content) {
  color: var(--t3-text) !important;
}
.dark .prose a { color: var(--t3-link) !important; }
.dark .prose a:hover { color: var(--t3-link-hover) !important; }
.dark #header .prose, .dark #header .prose p, .dark .text-gray-600, .dark .text-gray-500 {
  color: var(--t3-text-muted) !important;
}
"""


def remove_block(text: str, start_marker: str) -> str:
    idx = text.find(start_marker)
    if idx < 0:
        return text
    # find next section comment at same or higher level
    rest = text[idx + len(start_marker) :]
    m = re.search(r"\n/\* [─═]", rest)
    if not m:
        return text[:idx]
    end = idx + len(start_marker) + m.start()
    return text[:idx] + text[end:]


def main() -> None:
    text = CSS.read_text(encoding="utf-8")
    before = len(text)

    for marker in REMOVE_MARKERS:
        text = remove_block(text, marker)

    # Remove redundant individual dark heading block if consolidated added
    old_dark = "/* ── Dark mode: global text & surface overrides ────────────────── */"
    if old_dark in text and "consolidated text" not in text:
        # Remove duplicate granular blocks between global and breadcrumbs
        start = text.find(old_dark)
        end = text.find("/* Breadcrumbs */")
        if start >= 0 and end > start:
            text = text[:start] + DARK_CONSOLIDATED + "\n" + text[end:]

    # Font performance
    if "font-display" not in text:
        text = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');\n" + text

    # Actually @import blocks rendering - BAD. Use font-display in custom only:
    text = text.replace(
        "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');\n",
        "",
    )
    if "Inter" in text and "font-display: swap" not in text:
        text = "html { font-synthesis: none; }\n" + text

    CSS.write_text(text, encoding="utf-8")
    print(f"Trimmed CSS: {before} -> {len(text)} bytes ({before - len(text)} saved)")


if __name__ == "__main__":
    main()
