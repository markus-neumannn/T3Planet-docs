#!/usr/bin/env python3
"""Fix corrupted internal links and bare //License paths across all MD files."""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "node_modules", ".git", ".venv-translate", "logo", "_snippets"}

# Corrupted path fragments from legacy migration
CORRUPT_REPLACEMENTS = [
    ("/L/icense/", "/License/"),
    ("/E/xt", "/Ext"),
    ("/d/e/", "/de/"),
]

BARE_LICENSE_RE = re.compile(
    r"(?<!\[)(?<!\()//License(/[^\s\])<>,;]+)"
)
GO_HERE_RE = re.compile(
    r"Go here //License(/[^\s]+)"
)
PLAIN_DE_LICENSE_RE = re.compile(
    r"(?<!\[)(?<!\()(/de/License/[^\s\])<>,;]+)"
)
PLAIN_LICENSE_RE = re.compile(
    r"(?<!\[)(?<!\()(?<!/)(/License/[^\s\])<>,;#]+)"
)


def license_label(path: str, is_de: bool) -> str:
    if "UpdateVersion" in path:
        return "Lizenz-Update-Anleitung" if is_de else "License Update Version guide"
    if path.endswith("/License/Index") or path.endswith("/License"):
        return "Lizenz- & Installationsanleitung" if is_de else "License & Installation guide"
    if "NonComposer" in path:
        return "Update für Non-Composer-Instanzen" if is_de else "Non-Composer update guide"
    if "Composer" in path:
        return "Update für Composer-Instanzen" if is_de else "Composer update guide"
    return "Dokumentation" if is_de else "documentation"


def fix_content(text: str, rel: str) -> str:
    is_de = rel.startswith("de/")
    prefix = "/de" if is_de else ""

    for old, new in CORRUPT_REPLACEMENTS:
        text = text.replace(old, new)

    def bare_license(m):
        path = f"{prefix}/License{m.group(1)}"
        label = license_label(path, is_de)
        return f"[{label}]({path})"

    text = BARE_LICENSE_RE.sub(bare_license, text)

    def go_here(m):
        path = f"{prefix}/License{m.group(1)}"
        label = license_label(path, is_de)
        return f"See the [{label}]({path})"

    text = GO_HERE_RE.sub(go_here, text)

    # Fix markdown links with wrong visible text like [/License/...html](/License/...)
    text = re.sub(
        r"\[/[Ll]icense/[^\]]*\.html\]\((/[^)]+)\)",
        lambda m: f"[{license_label(m.group(1), is_de)}]({m.group(1)})",
        text,
    )

    # Repair links that lost the /License prefix in a prior run
    text = re.sub(
        r"\]\((/de)?/UpdateVersion/",
        lambda m: f"]({m.group(1) or ''}/License/UpdateVersion/",
        text,
    )
    text = re.sub(
        r"\]\((/de)?/LicenseActivation/",
        lambda m: f"]({m.group(1) or ''}/License/LicenseActivation/",
        text,
    )
    text = re.sub(
        r"\]\((/de)?/LicenseDeActivation/",
        lambda m: f"]({m.group(1) or ''}/License/LicenseDeActivation/",
        text,
    )
    text = re.sub(
        r"\]\((/de)?/Migration/Composer/",
        lambda m: f"]({m.group(1) or ''}/License/Migration/Composer/",
        text,
    )
    text = re.sub(
        r"\]\((/de)?/Introduction/Index#",
        lambda m: f"]({m.group(1) or ''}/License/Introduction/Index#",
        text,
    )

    return text


def main():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            path = Path(dirpath) / fn
            rel = str(path.relative_to(ROOT))
            text = path.read_text(encoding="utf-8")
            new = fix_content(text, rel)
            if new != text:
                path.write_text(new, encoding="utf-8")
                changed += 1
    print(f"Fixed internal links in {changed} files.")


if __name__ == "__main__":
    main()
