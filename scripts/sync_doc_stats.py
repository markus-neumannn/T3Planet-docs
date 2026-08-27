#!/usr/bin/env python3
"""Regenerate homepage Documentation pages / Products counts.

Import and call `sync_homepage_stats()` after adding a page or product.
Also runnable as: python3 scripts/sync_doc_stats.py
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from compute_doc_stats import sync_homepage_stats, write_stats_json

__all__ = ["sync_homepage_stats", "write_stats_json"]


if __name__ == "__main__":
    sync_homepage_stats()
