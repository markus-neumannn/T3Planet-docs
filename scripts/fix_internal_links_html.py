#!/usr/bin/env python3
"""DEPRECATED: Use strip_internal_links_html.py — canonical URLs omit .html suffix."""
from __future__ import annotations

import sys

if __name__ == "__main__":
    print(
        "fix_internal_links_html.py is deprecated.\n"
        "Canonical Mintlify routes omit .html (redirects handle legacy URLs).\n"
        "Run: python3 scripts/strip_internal_links_html.py",
        file=sys.stderr,
    )
    sys.exit(1)
