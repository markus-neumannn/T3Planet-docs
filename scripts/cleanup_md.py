#!/usr/bin/env python3
"""Post-migration cleanup of generated Mintlify Markdown.

Operates in-place on all *.md files under the project root (EN) and de/ mirror.

Fixes:
  A. Strip leftover MyST target labels:  (installation)=  (help)=  (configuration)=
  B. Remove generated system text:       "Generated content elements are stored on colpos 0"
  C. Convert leftover MyST figure/image directives  :::{figure} path ... :::  -> ![alt](path)
     (also handles blockquote `> ` and definition-list `: ` prefixed variants)
  D. Convert leftover RST figure/image directives  .. figure:: path / :alt: ...  -> ![alt](path)
     (also handles MyST-commented "% .. figure::" variants)
  E. Convert RST inline links  `Text <url>`_  -> [Text](url)
  F. Remove orphan RST option lines (:alt:/:width:/...) and stray MyST comment lines (^%)
  G. Remove empty fenced code blocks (```lang\n\n```)
  H. Collapse 3+ blank lines to 1
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {".git", "node_modules", "scripts", "logo", "images", "_snippets"}

IMG_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp")
OPTION_RE = re.compile(r"^\s*:(alt|width|height|target|class|name|align|scale|figwidth|figclass|loading):", re.I)


def resolve_image(md_path, ref):
    """Return the actual-cased relative path for an image ref, or None if missing."""
    ref = ref.strip().strip('"').strip("'")
    if ref.startswith(("http://", "https://", "//")):
        return ref
    base = os.path.dirname(md_path)
    # Always resolve actual on-disk casing (macOS FS is case-insensitive but
    # the deploy target may be case-sensitive).
    parts = ref.replace("\\", "/").split("/")
    cur = base
    out_parts = []
    for part in parts:
        if part in ("", "."):
            continue
        if part == "..":
            cur = os.path.dirname(cur)
            out_parts.append("..")
            continue
        try:
            entries = os.listdir(cur)
        except OSError:
            return None
        match = None
        for e in entries:
            if e.lower() == part.lower():
                match = e
                break
        if match is None:
            return None
        out_parts.append(match)
        cur = os.path.join(cur, match)
    return "/".join(out_parts) if out_parts else None


def strip_prefix(line):
    """Remove leading blockquote '>' markers and a single deflist ': ' marker.

    Careful NOT to consume the ':::' that begins a MyST directive (no space
    follows the first colon there)."""
    m = re.match(r"^(\s*(?:>\s?)*)(.*)$", line)
    rest = m.group(2)
    had = bool(m.group(1).strip())
    # single leading deflist marker ': ' (colon + whitespace). '::' (no space)
    # is not a deflist marker and won't match this pattern.
    m2 = re.match(r"^:\s+(.*)$", rest)
    if m2:
        rest = m2.group(1)
        had = True
    return rest, had


def make_image(md_path, path, alt):
    resolved = resolve_image(md_path, path)
    if resolved is None:
        return None
    alt = (alt or os.path.splitext(os.path.basename(path))[0]).strip()
    alt = alt.replace("[", "").replace("]", "")
    return f"![{alt}]({resolved})"


def convert_myst_figures(lines, md_path):
    """Handle :::{figure}/:::{image} blocks, possibly prefixed with > or :."""
    out = []
    i = 0
    n = len(lines)
    fig_re = re.compile(r"^:::*\{(figure|image)\}\s*(.+?)\s*$")
    while i < n:
        raw = lines[i]
        clean, _ = strip_prefix(raw)
        m = fig_re.match(clean.strip())
        if m:
            path = m.group(2).strip()
            alt = ""
            j = i + 1
            while j < n:
                cl, _ = strip_prefix(lines[j])
                cl = cl.strip()
                if cl.startswith(":::"):
                    j += 1
                    break
                mo = re.match(r":alt:\s*(.*)$", cl, re.I)
                if mo:
                    alt = mo.group(1).strip()
                elif cl and not OPTION_RE.match(cl) and not cl.startswith(":"):
                    # not an option line: directive block ended without explicit close
                    break
                j += 1
            img = make_image(md_path, path, alt)
            if img:
                if out and out[-1].strip():
                    out.append("")
                out.append(img)
                out.append("")
            i = j
            continue
        out.append(raw)
        i += 1
    return out


def convert_rst_figures(lines, md_path):
    """Handle '.. figure:: path' / '.. image:: path' blocks (incl. '% ' commented)."""
    out = []
    i = 0
    n = len(lines)
    rst_re = re.compile(r"^(?:%\s*)?\.\.\s+(figure|image)::\s*(.+?)\s*$")
    while i < n:
        line = lines[i]
        m = rst_re.match(line.strip())
        if m:
            path = m.group(2).strip()
            alt = ""
            j = i + 1
            while j < n:
                nxt = lines[j].strip()
                nxt_nc = re.sub(r"^%\s*", "", nxt)
                if nxt_nc == "":
                    j += 1
                    continue
                mo = re.match(r":alt:\s*(.*)$", nxt_nc, re.I)
                if mo:
                    alt = mo.group(1).strip()
                    j += 1
                    continue
                if OPTION_RE.match(nxt_nc):
                    j += 1
                    continue
                break
            img = make_image(md_path, path, alt)
            if img:
                out.append(img)
                out.append("")
            i = j
            continue
        out.append(line)
        i += 1
    return out


ADMON_MAP = {
    "warning": "Warning", "caution": "Warning", "attention": "Warning",
    "danger": "Warning", "error": "Warning",
    "tip": "Tip", "hint": "Tip",
    "note": "Note", "important": "Note", "seealso": "Note", "info": "Info",
    "check": "Check",
}
TRANSPARENT_RST = ("rst-class", "only", "highlights", "default-role",
                   "contents", "sectnum", "container", "rubric")

OPENER_RE = re.compile(r"^(\s*(?:>\s?)*)([-*+]\s+|:\s+)?```\{([a-zA-Z-]+)\}\s*(.*)$")


def _strip_block(line):
    """Remove leading whitespace and blockquote markers from a body line."""
    return re.sub(r"^\s*(?:>\s?)*", "", line)


def _convert_html_anchors(text):
    return re.sub(
        r'<a\s+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>',
        r"[\2](\1)", text, flags=re.I | re.S,
    )


def _grid_table_to_md(inner):
    rows = []
    for l in inner:
        s = l.strip()
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            rows.append(cells)
    if not rows:
        return None
    maxcols = max(len(r) for r in rows)
    if maxcols <= 1:
        return [f"- {r[0]}" for r in rows if r and r[0]]
    out = []
    header = rows[0] + [""] * (maxcols - len(rows[0]))
    out.append("| " + " | ".join(header) + " |")
    out.append("| " + " | ".join(["---"] * maxcols) + " |")
    for r in rows[1:]:
        r = r + [""] * (maxcols - len(r))
        out.append("| " + " | ".join(r) + " |")
    return out


def convert_fenced_directives(lines, md_path):
    out = []
    i = 0
    n = len(lines)
    while i < n:
        m = OPENER_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        list_marker = (m.group(2) or "").strip()
        name = m.group(3).lower()
        # collect body until closing fence
        body = []
        j = i + 1
        while j < n:
            if _strip_block(lines[j]).strip() == "```":
                break
            body.append(lines[j])
            j += 1
        inner = [_strip_block(b) for b in body]
        i = j + 1  # skip past closing fence

        if name == "include":
            continue
        if name == "raw":
            html = _convert_html_anchors("\n".join(inner).strip())
            if list_marker:
                first = html.strip()
                out.append(f"{list_marker} {first}" if list_marker in "-*+" else first)
            else:
                out.extend(html.split("\n"))
                out.append("")
            continue
        if name == "eval-rst":
            grid = _grid_table_to_md(inner)
            if grid:
                if out and out[-1].strip():
                    out.append("")
                out.extend(grid)
                out.append("")
                continue
            meaningful = [l for l in inner if l.strip() and not l.strip().startswith("..")]
            if not meaningful:
                continue  # only transparent directives -> drop
            try:
                import importlib.util as _ilu
                if "_mv" not in globals():
                    _spec = _ilu.spec_from_file_location(
                        "migrate_v2", os.path.join(os.path.dirname(__file__), "migrate_v2.py"))
                    _m = _ilu.module_from_spec(_spec)
                    _spec.loader.exec_module(_m)
                    globals()["_mv"] = _m
                conv = globals()["_mv"].convert_body(inner, {})
                out.extend(conv.split("\n"))
            except Exception:
                out.extend(meaningful)
            out.append("")
            continue
        if name in ADMON_MAP:
            label = ADMON_MAP[name]
            out.append(f"<{label}>")
            out.append("")
            out.extend([l for l in inner])
            out.append("")
            out.append(f"</{label}>")
            out.append("")
            continue
        # unknown directive: drop fence wrapper, keep inner
        out.extend(inner)
    return out


def prefix_relative_images(text):
    """Mintlify treats bare 'images/x.png' as root-relative (/images/x.png).
    Prefix relative image refs with './' so they resolve from the source file."""
    text = re.sub(
        r"(!\[[^\]]*\]\()(?!/|\.{1,2}/|https?://|data:|#|mailto:)([^)\s]+\))",
        r"\1./\2",
        text,
    )
    text = re.sub(
        r'(<img\b[^>]*?\bsrc=")(?!/|\.{1,2}/|https?://|data:|#)([^"]+")',
        r"\1./\2",
        text,
    )
    return text


def standardize_helpful_links(text):
    """Normalize bullets inside 'Helpful Links' sections for consistency."""
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)
    head_re = re.compile(r"^(#+)\s*Helpful Links?\s*$", re.I)
    while i < n:
        hm = head_re.match(lines[i])
        if not hm:
            out.append(lines[i])
            i += 1
            continue
        level = len(hm.group(1))
        out.append(lines[i])
        i += 1
        # process until next heading of same/higher level or EOF
        while i < n:
            line = lines[i]
            hm2 = re.match(r"^(#+)\s+\S", line)
            if hm2 and len(hm2.group(1)) <= level:
                break
            out.append(normalize_help_bullet(line))
            i += 1
    return "\n".join(out)


def normalize_help_bullet(line):
    m = re.match(r"^(\s*[-*]\s+)(.*)$", line)
    if not m:
        return line
    indent, content = m.group(1), m.group(2)
    # fix trailing "... support center.- https://..." -> "...support center: https://..."
    content = re.sub(r"\.\-\s*(https?://)", r": \1", content)
    # bold a leading "Label:" if not already styled
    bm = re.match(r"^([A-Za-z][A-Za-z0-9 /&'()\-]{1,40}):\s+(.+)$", content)
    if bm and not content.startswith("**") and not content.startswith("["):
        label, rest = bm.group(1).strip(), bm.group(2).strip()
        content = f"**{label}:** {rest}"
    return f"{indent}{content}"


def remove_empty_code_fences(text):
    return re.sub(r"```[A-Za-z0-9_-]*\s*\n\s*\n```\n?", "", text)


def clean_empty_notes(text):
    # remove <Note>/<Warning>/<Info>/<Tip> blocks that contain only whitespace
    return re.sub(r"<(Note|Warning|Info|Tip|Check)>\s*</\1>\s*", "", text)


def process(text, md_path):
    # B. generated system text (line-level, case-insensitive)
    text = re.sub(r"(?im)^\s*Generated content elements are stored on colpos\s*0\.?\s*$\n?", "", text)

    lines = text.split("\n")

    # A. strip MyST target labels
    lines = [l for l in lines if not re.match(r"^\s*\([A-Za-z0-9_-]+\)=\s*$", l)]

    # B2. convert leftover fenced directives (eval-rst/raw/include/admonitions)
    lines = convert_fenced_directives(lines, md_path)

    # C. MyST figure/image directives
    lines = convert_myst_figures(lines, md_path)

    # D. RST figure/image directives (and commented)
    lines = convert_rst_figures(lines, md_path)

    cleaned = []
    for l in lines:
        s = l.strip()
        # F. drop orphan RST option lines
        if OPTION_RE.match(s):
            continue
        # drop stray MyST comment lines
        if re.match(r"^\s*%(\s|$)", l):
            continue
        # drop empty headings (e.g. trailing "##" with no text)
        if re.match(r"^\s*#{1,6}\s*$", l):
            continue
        cleaned.append(l)
    lines = cleaned

    text = "\n".join(lines)

    # E. RST inline links  `Text <url>`_  -> [Text](url)
    text = re.sub(r"`([^`<>]+?)\s*<((?:https?://|mailto:)[^>`]+)>`__?", r"[\1](\2)", text)

    # E2. normalize messy/broken "api/draft?slug=<slug>" code spans (incl. forms
    # mangled by translation) into one clean inline code span.
    text = re.sub(
        "[`\u201e\u201c\u201d\"]*\\s*`?api/draft\\?slug=`?<slug>`*\\s*[`\u201e\u201c\u201d\"]*",
        "`api/draft?slug=<slug>`",
        text,
    )

    # I. standardize Helpful Links sections
    text = standardize_helpful_links(text)

    # J. prefix relative image paths with ./ for Mintlify resolution
    text = prefix_relative_images(text)

    # G. empty fenced code blocks
    text = remove_empty_code_fences(text)

    # empty admonition components
    text = clean_empty_notes(text)

    # H. collapse 3+ blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


def iter_md_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.endswith(".zip")]
        for f in filenames:
            if f.endswith(".md"):
                yield os.path.join(dirpath, f)


def main():
    changed = 0
    total = 0
    for path in iter_md_files():
        total += 1
        with open(path, "r", encoding="utf-8") as fh:
            orig = fh.read()
        new = process(orig, path)
        if new != orig:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
            changed += 1
    print(f"Processed {total} files, changed {changed}.")


if __name__ == "__main__":
    main()
