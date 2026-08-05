#!/usr/bin/env python3
"""Upgrade common doc patterns to Mintlify interactive components."""
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP = {"scripts", "node_modules", ".git", ".venv-translate"}

BLOCKQUOTE_NOTE = re.compile(
    r"^>\s*\*\*(Note|Warning|Tip|Check):\*\*\s*(.+)$", re.M | re.I
)


def convert_blockquote_callouts(text: str) -> str:
    def repl(m):
        kind = m.group(1).strip().capitalize()
        if kind.lower() == "warning":
            kind = "Warning"
        body = m.group(2).strip()
        return f"<{kind}>\n\n{body}\n\n</{kind}>"
    return BLOCKQUOTE_NOTE.sub(repl, text)


STEP_BLOCK_RE = re.compile(
    r"^\*\*Step\s+(\d+)\.?\*\*\s*(.*?)(?=\n\*\*Step\s+\d+|\n#{1,3}\s|\n<|\Z)",
    re.M | re.S,
)


def convert_steps(text: str) -> str:
    if "<Steps>" in text:
        return text
    matches = list(STEP_BLOCK_RE.finditer(text))
    if len(matches) < 2:
        return text
    if matches[-1].start() - matches[0].start() > 5000:
        return text
    block = text[matches[0].start() : matches[-1].end()]
    if re.search(r"^\s*[-*]\s", block, re.M) or "```" in block:
        return text

    first, last = matches[0].start(), matches[-1].end()
    steps_xml = ["<Steps>"]
    for m in matches:
        steps_xml.append(f'  <Step title="Step {m.group(1)}">')
        steps_xml.append(m.group(2).strip())
        steps_xml.append("  </Step>")
    steps_xml.append("</Steps>")
    return text[:first] + "\n".join(steps_xml) + "\n\n" + text[last:]


def process(text: str) -> str:
    text = convert_blockquote_callouts(text)
    text = convert_steps(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def main():
    targets = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP]
        for fn in filenames:
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), ROOT)
            if "**Step" in open(os.path.join(dirpath, fn), encoding="utf-8").read():
                targets.append(os.path.join(dirpath, fn))

    changed = 0
    for path in targets:
        text = open(path, encoding="utf-8").read()
        new = process(text)
        if new != text:
            open(path, "w", encoding="utf-8").write(new)
            changed += 1
    print(f"Enhanced components in {changed} pages.")


if __name__ == "__main__":
    main()
