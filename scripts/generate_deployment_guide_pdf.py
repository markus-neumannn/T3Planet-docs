#!/usr/bin/env python3
"""Generate T3Planet Docs deployment guide PDF for project managers."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "T3Planet_Docs_Deployment_Guide.pdf"

PRIMARY = colors.HexColor("#0052FF")
PRIMARY_DARK = colors.HexColor("#0041CC")
PRIMARY_LIGHT = colors.HexColor("#EFF6FF")
PRIMARY_BORDER = colors.HexColor("#BFDBFE")
TEXT = colors.HexColor("#0F172A")
MUTED = colors.HexColor("#475569")
BORDER = colors.HexColor("#E2E8F0")
WHITE = colors.white
WARN = colors.HexColor("#D97706")
WARN_BG = colors.HexColor("#FFFBEB")
CONTENT_W = A4[0] - 4 * cm


def build_styles():
    base = getSampleStyleSheet()
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle", parent=base["Title"], fontSize=30, leading=36,
            textColor=WHITE, alignment=TA_CENTER, spaceAfter=14, fontName="Helvetica-Bold",
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub", parent=base["Normal"], fontSize=13, leading=19,
            textColor=colors.HexColor("#DBEAFE"), alignment=TA_CENTER,
        ),
        "h1": ParagraphStyle(
            "H1", parent=base["Heading1"], fontSize=17, leading=21,
            textColor=PRIMARY, spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold",
        ),
        "h2": ParagraphStyle(
            "H2", parent=base["Heading2"], fontSize=12, leading=15,
            textColor=PRIMARY_DARK, spaceBefore=12, spaceAfter=6, fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontSize=10.5, leading=15,
            textColor=TEXT, alignment=TA_JUSTIFY, spaceAfter=8,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontSize=10.5, leading=15,
            textColor=TEXT, leftIndent=12, spaceBefore=2, spaceAfter=5,
        ),
        "cell": ParagraphStyle(
            "Cell", parent=base["Normal"], fontSize=10, leading=14, textColor=TEXT,
        ),
        "callout": ParagraphStyle(
            "Callout", parent=base["Normal"], fontSize=10, leading=14,
            textColor=colors.HexColor("#1E40AF"), spaceAfter=0,
        ),
        "callout_warn": ParagraphStyle(
            "CalloutWarn", parent=base["Normal"], fontSize=10, leading=14,
            textColor=colors.HexColor("#92400E"), spaceAfter=0,
        ),
        "toc": ParagraphStyle(
            "TOC", parent=base["Normal"], fontSize=10.5, leading=18, textColor=TEXT,
        ),
        "footer": ParagraphStyle(
            "Footer", parent=base["Normal"], fontSize=8, textColor=MUTED, alignment=TA_CENTER,
        ),
        "section_num": ParagraphStyle(
            "SectionNum", parent=base["Normal"], fontSize=9, leading=11,
            textColor=WHITE, alignment=TA_CENTER, fontName="Helvetica-Bold",
        ),
    }


def callout_box(text: str, styles, variant: str = "info") -> Table:
    """Render callout inside a table — avoids Paragraph backColor clipping bugs."""
    bg = PRIMARY_LIGHT if variant == "info" else WARN_BG
    border = PRIMARY_BORDER if variant == "info" else colors.HexColor("#FDE68A")
    pstyle = styles["callout"] if variant == "info" else styles["callout_warn"]
    inner = Paragraph(text, pstyle)
    t = Table([[inner]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 1, border),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def section_header(num: str, title: str, styles) -> list:
    badge = Table([[Paragraph(num, styles["section_num"])]], colWidths=[0.9 * cm], rowHeights=[0.9 * cm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PRIMARY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    header_row = Table(
        [[badge, Paragraph(f"<b>{title}</b>", styles["h1"])]],
        colWidths=[1.1 * cm, CONTENT_W - 1.1 * cm],
    )
    header_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [header_row, HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=14)]


def checklist_table(items: list[str], styles) -> Table:
    data = [[Paragraph("☐", styles["cell"]), Paragraph(item, styles["cell"])] for item in items]
    t = Table(data, colWidths=[0.7 * cm, CONTENT_W - 0.7 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (0, -1), 6),
        ("LEFTPADDING", (1, 0), (1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [WHITE, colors.HexColor("#F8FAFC")]),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, BORDER),
    ]))
    return t


def phase_table(phases: list[tuple[str, str, str]], styles) -> Table:
    header = [
        Paragraph("<b>Phase</b>", styles["cell"]),
        Paragraph("<b>Focus</b>", styles["cell"]),
        Paragraph("<b>Key actions</b>", styles["cell"]),
    ]
    rows = [header]
    for phase, focus, actions in phases:
        rows.append([
            Paragraph(f"<b>{phase}</b>", styles["cell"]),
            Paragraph(focus, styles["cell"]),
            Paragraph(actions, styles["cell"]),
        ])
    t = Table(rows, colWidths=[1.6 * cm, 3.2 * cm, CONTENT_W - 4.8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8FAFC")]),
    ]))
    return t


def requirements_table(items: list[str], styles) -> Table:
    rows = [[Paragraph(f"• {item}", styles["cell"])] for item in items]
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.75, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def draw_page_frame(canvas, doc):
    canvas.saveState()
    if doc.page == 1:
        canvas.setFillColor(PRIMARY)
        canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#1D4ED8"))
        canvas.circle(A4[0] + 1 * cm, A4[1] + 1 * cm, 5.5 * cm, fill=1, stroke=0)
        canvas.setFillColor(colors.HexColor("#3B82F6"))
        canvas.circle(-1 * cm, -1 * cm, 4 * cm, fill=1, stroke=0)
    else:
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(2 * cm, A4[1] - 1.5 * cm, A4[0] - 2 * cm, A4[1] - 1.5 * cm)
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(PRIMARY)
        canvas.drawString(2 * cm, A4[1] - 1.25 * cm, "T3Planet Documentation")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawRightString(A4[0] - 2 * cm, A4[1] - 1.25 * cm, "Mintlify Deployment Guide")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.1 * cm, f"© T3Planet · {date.today().year}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(OUT), pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2.2 * cm, bottomMargin=2 * cm,
        title="T3Planet Docs Deployment Guide", author="T3Planet",
    )
    story = []

    # Cover
    story.append(Spacer(1, 4.2 * cm))
    story.append(Paragraph("T3Planet Documentation", styles["cover_title"]))
    story.append(Paragraph("Mintlify Deployment &amp; Operations Guide", styles["cover_sub"]))
    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph(
        f"Prepared for Project Management<br/>{date.today().strftime('%B %d, %Y')}",
        styles["cover_sub"],
    ))
    story.append(Spacer(1, 2.2 * cm))
    meta = Table([
        [Paragraph("<b>Platform</b>", styles["cover_sub"]), Paragraph("Mintlify (hosted documentation)", styles["cover_sub"])],
        [Paragraph("<b>Source</b>", styles["cover_sub"]), Paragraph("Private GitLab repository", styles["cover_sub"])],
        [Paragraph("<b>Stack</b>", styles["cover_sub"]), Paragraph("docs.json · Markdown · custom CSS/JS", styles["cover_sub"])],
        [Paragraph("<b>Preview</b>", styles["cover_sub"]), Paragraph("mint dev (Node 22 LTS)", styles["cover_sub"])],
    ], colWidths=[4.2 * cm, 10.3 * cm])
    meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1E3A8A")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#93C5FD")),
        ("TEXTCOLOR", (1, 0), (1, -1), WHITE),
        ("ALIGN", (0, 0), (0, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#3B82F6")),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#2563EB")),
    ]))
    story.append(meta)
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("Contents", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=14))
    for i, item in enumerate([
        "Deploy from private GitLab?",
        "Post-deployment update process",
        "Mintlify + private GitLab setup",
        "Custom domain connection",
        "Easiest &amp; safest deployment plan",
        "Pre-deployment checklist",
        "Post-deployment checklist",
        "Ongoing edit &amp; maintenance workflow",
        "Performance &amp; quality recommendations",
        "Roles, risks &amp; rollback",
    ], 1):
        story.append(Paragraph(f"<b>{i:02d}</b>&nbsp;&nbsp;&nbsp;{item}", styles["toc"]))
    story.append(PageBreak())

    # Q1
    story.extend(section_header("01", "Can I deploy from a private GitLab repository?", styles))
    story.append(Paragraph(
        "<b>Yes.</b> Mintlify officially supports connecting a <b>private GitLab project</b> "
        "on gitlab.com, or a <b>publicly reachable</b> self-hosted GitLab instance.",
        styles["body"],
    ))
    story.append(Paragraph("Requirements for private repositories:", styles["h2"]))
    story.append(requirements_table([
        "Project Access Token (or Personal Access Token) with <b>Maintainer</b> role",
        "Token scopes: <b>api</b> and <b>read_api</b>",
        "GitLab <b>Project ID</b> from Settings → General",
        "GitLab <b>webhook</b> pointing to Mintlify (automatic deploys on push)",
    ], styles))
    story.append(Spacer(1, 12))
    story.append(KeepTogether([
        callout_box(
            "<b>Important:</b> Self-hosted GitLab must be reachable from Mintlify cloud "
            "(app.mintlify.com). Instances behind VPN-only firewalls need alternative hosting "
            "(e.g. static export with your own CDN).",
            styles, "warn",
        ),
    ]))

    # Q2
    story.append(Spacer(1, 16))
    story.extend(section_header("02", "How to edit/update documentation after deployment?", styles))
    story.append(Paragraph(
        "After deployment, <b>GitLab remains the source of truth</b>. Day-to-day documentation "
        "changes are made in the repository — not in the Mintlify dashboard.",
        styles["body"],
    ))
    story.append(Paragraph("Standard update workflow:", styles["h2"]))
    for n, s in [
        ("1", "Edit Markdown pages, docs.json, images, or assets locally (or in GitLab UI)"),
        ("2", "Preview locally: <font name='Courier'>mint dev</font> (Node 22 LTS required)"),
        ("3", "Validate build: <font name='Courier'>mint validate</font>"),
        ("4", "Optional: <font name='Courier'>mint broken-links</font> before merge"),
        ("5", "Commit and push to the connected branch (typically <font name='Courier'>main</font>)"),
        ("6", "GitLab webhook triggers Mintlify → automatic production deployment"),
        ("7", "Larger changes: use a branch + Merge Request for review and preview URL"),
    ]:
        story.append(Paragraph(f"<b>Step {n}.</b> {s}", styles["bullet"]))
    story.append(PageBreak())

    # Q3
    story.extend(section_header("03", "Mintlify private GitLab — setup process", styles))
    story.append(Paragraph(
        "<b>Official guide:</b> "
        "<font color='#0052FF'>mintlify.com/docs/deploy/gitlab</font>",
        styles["body"],
    ))
    story.append(Spacer(1, 6))
    for i, s in enumerate([
        "Create Mintlify account at app.mintlify.com",
        "Ensure repo contains docs.json, .md pages, custom.css, _static/ assets",
        "Mintlify Dashboard → Git Settings → Connect to GitLab",
        "GitLab: Settings → Access Tokens → create token (Maintainer, api + read_api)",
        "In Mintlify wizard: enter Project ID, token, deploy branch (e.g. main)",
        "GitLab: Settings → Webhooks → URL: leaves.mintlify.com/gitlab-webhook",
        "Webhook secret: Webtoken from Mintlify dashboard",
        "Events: Push events (all branches) + Merge request events",
        "Test webhook — Push events should return HTTP 200",
        "Local CLI: run <font name='Courier'>mint login</font> for authenticated features",
    ], 1):
        story.append(Paragraph(f"<b>{i}.</b> {s}", styles["bullet"]))

    # Q4
    story.append(Spacer(1, 14))
    story.extend(section_header("04", "Custom domain — can you connect one?", styles))
    story.append(Paragraph(
        "<b>Yes.</b> Mintlify supports custom domains with automatic TLS (Let's Encrypt).",
        styles["body"],
    ))
    story.append(Paragraph("Recommended example: <b>docs.t3planet.de</b>", styles["h2"]))
    for i, s in enumerate([
        "Mintlify Dashboard → Custom domain setup → Add your domain",
        "Add two DNS TXT verification records (values shown in dashboard)",
        "Wait until both TXT records show verified (green checks)",
        "Add CNAME record: <font name='Courier'>docs → cname.mintlify.builders</font>",
        "Do NOT switch CNAME before TXT verification (see Mintlify Cloudflare notes)",
        "Wait for DNS propagation (1–24 hours) and TLS certificate provisioning",
        "After go-live: add canonical URL in docs.json seo.metatags for SEO",
    ], 1):
        story.append(Paragraph(f"<b>{i}.</b> {s}", styles["bullet"]))
    story.append(PageBreak())

    # Q5
    story.extend(section_header("05", "Easiest &amp; safest deployment plan", styles))
    story.append(phase_table([
        ("A", "Prepare", "mint validate · mint broken-links · confirm Mintlify plan · no secrets in repo"),
        ("B", "Connect", "Link GitLab in Mintlify · add webhook · first deploy to *.mintlify.app URL"),
        ("C", "Verify", "Test Home, AI Foundation, Extensions, Templates, License, search, mobile"),
        ("D", "Domain", "Add TXT records → verify → CNAME → HTTPS → canonical URL"),
        ("E", "Operate", "Branch + MR for changes · merge to main → auto deploy · rotate tokens"),
    ], styles))
    story.append(Spacer(1, 20))

    # Pre-deploy
    story.append(Paragraph("Pre-Deployment Checklist", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))
    story.append(Paragraph(
        "Complete all items before connecting GitLab to Mintlify production.",
        styles["body"],
    ))
    story.append(Spacer(1, 8))
    story.append(checklist_table([
        "Confirm Mintlify plan supports private GitLab hosting",
        "Run <font name='Courier'>mint validate</font> — build passes with zero errors",
        "Run <font name='Courier'>mint broken-links</font> — fix critical broken internal links",
        "Verify docs.json navigation matches actual .md file paths",
        "Confirm English-only: de/ excluded via .mintignore, redirects configured",
        "Review custom assets: custom.css and _static/t3-docs.min.js load correctly",
        "No secrets, API keys, or .env files in repository",
        "GitLab Maintainer token created with api + read_api scopes",
        "GitLab Project ID documented for Mintlify connection",
        "Deploy branch decided (recommended: main)",
        "Webhook URL and secret token ready for GitLab",
        "Stakeholders informed of go-live window and rollback contact",
        "Spot-check 10 key pages locally: Home, T3AA, T3AI, Extensions, License",
        "Note: production CDN is much faster than local mint dev",
        "GitLab main branch tagged or release noted before first deploy",
    ], styles))
    story.append(PageBreak())

    # Post-deploy
    story.append(Paragraph("Post-Deployment Checklist", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))
    story.append(checklist_table([
        "Production URL loads (*.mintlify.app) — HTTP 200 on homepage",
        "Sidebar navigation works on deep pages (e.g. T3AA System Requirements)",
        "Search opens and returns results (Cmd+K / Ctrl+K)",
        "Dark / light mode switches without layout break",
        "Mobile and tablet layouts verified on real devices",
        "Images and WebP assets load on screenshot-heavy pages",
        "German /de URLs redirect to English equivalents",
        "404 page behaves correctly",
        "Run Lighthouse on production URL — record baseline scores",
        "Custom domain DNS verified (if applicable)",
        "HTTPS certificate active on custom domain",
        "Share production URL with team; update internal wiki/links",
        "Confirm GitLab → Mintlify webhook works (test push deploy)",
        "Set calendar reminder to rotate GitLab token before expiry",
    ], styles))
    story.append(PageBreak())

    # Ongoing
    story.append(Paragraph("Ongoing Edit &amp; Maintenance", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))
    story.append(Paragraph(
        "Treat documentation like application code: branch, review, validate, merge, auto-deploy.",
        styles["body"],
    ))
    for o in [
        "<b>Small fixes</b> (typos): edit → mint validate → push to main",
        "<b>Medium changes</b> (new section): feature branch → MR → preview URL → merge",
        "<b>Large changes</b> (nav restructure): dedicated branch → full QA → staged merge",
        "<b>New extension docs</b>: add .md pages + update docs.json + broken-links check",
        "<b>Images</b>: prefer WebP, compress screenshots, use lazy loading",
        "<b>Never edit production directly</b> — always commit to GitLab",
        "<b>Monthly</b>: broken-links check, analytics review, search gap review",
        "<b>Quarterly</b>: rotate GitLab token, review .mintignore, audit unused assets",
    ]:
        story.append(Paragraph(f"• {o}", styles["bullet"]))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Performance &amp; Quality", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))
    for p in [
        "Production Mintlify CDN eliminates local dev compilation delays",
        "Custom JS: single 3KB bundle (_static/t3-docs.min.js) — avoid root-level .js files",
        "custom.css minified (~39KB) — avoid duplicate or unused styles",
        "de/ excluded via .mintignore — keeps search index lean",
        "Use mint validate in CI or pre-push hook",
        "Target Web Vitals on live URL: LCP &lt; 2.5s · CLS &lt; 0.1 · FCP &lt; 1.8s",
    ]:
        story.append(Paragraph(f"• {p}", styles["bullet"]))

    story.append(Spacer(1, 14))
    story.append(Paragraph("Roles, Risks &amp; Rollback", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceAfter=12))
    roles = Table([
        [Paragraph("<b>Role</b>", styles["cell"]), Paragraph("<b>Responsibility</b>", styles["cell"])],
        [Paragraph("Doc author", styles["cell"]), Paragraph("Edit .md content, images, local preview", styles["cell"])],
        [Paragraph("Tech lead", styles["cell"]), Paragraph("docs.json, navigation, mint validate, MR approval", styles["cell"])],
        [Paragraph("DevOps / PM", styles["cell"]), Paragraph("GitLab token, webhook, DNS, custom domain, go-live", styles["cell"])],
        [Paragraph("QA", styles["cell"]), Paragraph("Post-deploy checklist, mobile, search, broken links", styles["cell"])],
    ], colWidths=[3.5 * cm, CONTENT_W - 3.5 * cm])
    roles.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY_LIGHT),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(roles)
    story.append(Spacer(1, 14))
    story.append(Paragraph("Common risks &amp; mitigations:", styles["h2"]))
    risks = Table([
        [Paragraph("<b>Risk</b>", styles["cell"]), Paragraph("<b>Mitigation</b>", styles["cell"])],
        [Paragraph("Webhook failure", styles["cell"]), Paragraph("Test webhook after any GitLab settings change", styles["cell"])],
        [Paragraph("Token expiry", styles["cell"]), Paragraph("Set expiry reminder; use project access token", styles["cell"])],
        [Paragraph("Broken navigation", styles["cell"]), Paragraph("Run mint validate + broken-links before merge", styles["cell"])],
        [Paragraph("DNS misconfiguration", styles["cell"]), Paragraph("TXT records first, then CNAME — follow Mintlify order", styles["cell"])],
        [Paragraph("Bad deploy", styles["cell"]), Paragraph("git revert + push to main triggers automatic redeploy", styles["cell"])],
    ], colWidths=[4 * cm, CONTENT_W - 4 * cm])
    risks.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), WARN),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, WARN_BG]),
    ]))
    story.append(risks)
    story.append(Spacer(1, 16))
    story.append(callout_box(
        "<b>References:</b> mintlify.com/docs/deploy/gitlab · "
        "mintlify.com/docs/customize/custom-domain · "
        "mintlify.com/docs/organize/mintignore",
        styles,
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "Generated for T3Planet Documentation · No documentation content was modified.",
        styles["footer"],
    ))

    doc.build(story, onFirstPage=draw_page_frame, onLaterPages=draw_page_frame)
    print(f"Created: {OUT}")


if __name__ == "__main__":
    main()
