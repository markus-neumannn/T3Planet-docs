#!/usr/bin/env python3
import sys
from playwright.sync_api import sync_playwright

shots = [
    ("http://localhost:3333/ExtNsT3AI/Index", "/tmp/shot_t3ai_index.png"),
    ("http://localhost:3333/ExtNsT3AI/Introduction/Index", "/tmp/shot_t3ai_intro.png"),
    ("http://localhost:3333/ExtNsT3AS/Configuration/Index", "/tmp/shot_t3as_config.png"),
    ("http://localhost:3333/de/ExtNsT3AI/Index", "/tmp/shot_de_t3ai.png"),
]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 1000})
    for url, out in shots:
        try:
            pg.goto(url, wait_until="networkidle", timeout=60000)
            pg.wait_for_timeout(2500)
            pg.screenshot(path=out, full_page=False)
            print("OK", out)
        except Exception as e:
            print("ERR", url, e)
    b.close()
