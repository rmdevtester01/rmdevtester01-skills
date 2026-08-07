"""
Interview Prep PDF Template
============================
Reusable PDF generator for the interview-prep skill.

This script produces a landscape-orientation, multi-section interview prep PDF
with bordered quote blocks and styled response-bank tables.

Key design decisions:
- Landscape orientation for readability of wide response-bank tables (5-6 columns)
- Quote blocks use single-cell Tables (not ParagraphStyle backColor) to avoid
  background-bleed into headings above them — a ReportLab rendering quirk
- All section content is parameterized so the script can be reused across users,
  companies, and roles by populating the data dicts at the bottom

Usage pattern:
    Fill in the data dicts (interviewer_brief, fit_mapping, competitive_landscape,
    questions_to_ask, talking_points, jd_themes, response_bank, checklist),
    then call build_pdf(output_path, user_name, company, role).
"""

from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch


# =========================================================================
# STYLES
# =========================================================================

def get_styles():
    """Return all paragraph styles used in the PDF."""
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleX", parent=styles["Title"], fontSize=16, spaceAfter=4,
            textColor=colors.HexColor("#1a1a1a"),
        ),
        "subtitle": ParagraphStyle(
            "SubtitleX", parent=styles["Normal"], fontSize=10,
            textColor=colors.HexColor("#666666"), spaceAfter=12,
        ),
        "section": ParagraphStyle(
            "SectionX", parent=styles["Heading2"], fontSize=13,
            spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1a1a1a"),
        ),
        "sub_section": ParagraphStyle(
            "SubSectionX", parent=styles["Heading3"], fontSize=11,
            spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#2c3e50"),
        ),
        "body": ParagraphStyle(
            "BodyX", parent=styles["Normal"], fontSize=9, leading=12, spaceAfter=6,
        ),
        "quote": ParagraphStyle(
            "QuoteX", parent=styles["Normal"], fontSize=9, leading=13,
            textColor=colors.HexColor("#333333"), fontName="Helvetica-Oblique",
        ),
        "cell": ParagraphStyle(
            "CellX", parent=styles["Normal"], fontSize=8, leading=10,
        ),
        "cell_header": ParagraphStyle(
            "CellHeaderX", parent=styles["Normal"], fontSize=9, leading=11,
            textColor=colors.white, alignment=1,
        ),
        "q_bold": ParagraphStyle(
            "QuestionX", parent=styles["Normal"], fontSize=8, leading=10,
            fontName="Helvetica-Bold",
        ),
    }


# =========================================================================
# HELPERS
# =========================================================================

def header_cell(text, styles):
    return Paragraph(f"<b>{text}</b>", styles["cell_header"])


def styled_table(data, col_widths):
    """Standard table styling used throughout the PDF."""
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7f7f7")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def quote_block(text, styles, doc):
    """
    Render a quote block as a single-cell table with background.
    Using a Table (not Paragraph backColor) prevents the background from
    bleeding upward into any heading or text above the quote.
    """
    p = Paragraph(text, styles["quote"])
    t = Table([[p]], colWidths=[doc.width])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0f4f8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#d0d8e0")),
    ]))
    return t


def p(text, styles, key="body"):
    """Shortcut for Paragraph."""
    return Paragraph(text, styles[key])


def cell(text, styles):
    return Paragraph(text, styles["cell"])


# =========================================================================
# PDF BUILDER
# =========================================================================

def build_pdf(output_path, content):
    """
    Build the interview prep PDF.

    `content` is a dict with these keys (any can be omitted to skip the section):
        - user_name (str): First name for filename and references
        - company (str): Company name
        - role (str): Role title
        - interviewer_name (str): Interviewer's name
        - interviewer_brief (dict): Keys: title, announced_date, background,
            education, location, reports_to, reputation, mandate_bullets,
            company_facts_bullets
        - fit_mapping (list[dict]): Each dict has keys 'need', 'match', 'evidence'
        - fit_pitch (str): One-sentence fit pitch (rendered in quote block)
        - competitive_landscape (dict, optional): Keys: intro, tables (list of
            {title, headers, rows}), synthesis_paragraphs (list of str),
            synthesis_quotes (list of str)
        - questions_to_ask (list[dict]): Each dict has 'question', 'rationale'
        - talking_points (dict, optional): Keys: section_title, intro,
            pitch_60s (str rendered as quote), distinctions (str),
            when_right_vs_overkill (str), honest_framing (str rendered as quote)
        - jd_themes (list[dict]): Each dict has 'theme_title', 'thesis',
            'example', 'resolution', 'company_tie'
        - response_bank (list[dict]): Each dict has 'number', 'question',
            'thesis', 'example', 'resolution', 'company_tie'
        - checklist (list[dict]): Each dict has 'item', 'why_it_matters'
        - final_read (str): Closing paragraph synthesizing read on interviewer

    Returns the output_path on success.
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=0.4 * inch,
        rightMargin=0.4 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
    )

    styles = get_styles()
    story = []

    # ---- TITLE ----
    user_name = content.get("user_name", "")
    company = content.get("company", "Company")
    role = content.get("role", "Role")
    interviewer_name = content.get("interviewer_name", "Interviewer")

    title_text = f"{user_name} — {company} {role} Interview Prep" if user_name else f"{company} {role} Interview Prep"
    story.append(p(title_text, styles, "title"))
    story.append(p(
        f"Interviewer intel, fit narrative, talking points, and response bank tailored to {interviewer_name}.",
        styles, "subtitle",
    ))

    # ---- SECTION 1: INTERVIEWER BRIEF ----
    if content.get("interviewer_brief"):
        ib = content["interviewer_brief"]
        story.append(p(f"1. Interviewer Brief — {interviewer_name}", styles, "section"))

        brief_inline_parts = []
        for k_label, k_key in [
            ("Title", "title"), ("Announced", "announced_date"),
            ("Background", "background"), ("Education", "education"),
            ("Location", "location"), ("Reports to", "reports_to"),
        ]:
            if ib.get(k_key):
                brief_inline_parts.append(f"<b>{k_label}:</b> {ib[k_key]}")
        if brief_inline_parts:
            story.append(p(" &nbsp;|&nbsp; ".join(brief_inline_parts), styles, "body"))

        if ib.get("reputation"):
            story.append(p(f"<b>Reputation:</b> {ib['reputation']}", styles, "body"))

        if ib.get("mandate_bullets"):
            story.append(p(f"{interviewer_name}'s mandate:", styles, "sub_section"))
            story.append(p("<br/>".join(f"• {b}" for b in ib["mandate_bullets"]), styles, "body"))

        if ib.get("company_facts_bullets"):
            story.append(p(f"What {company} actually does (use these in your answers):", styles, "sub_section"))
            story.append(p("<br/>".join(f"• {b}" for b in ib["company_facts_bullets"]), styles, "body"))

        story.append(PageBreak())

    # ---- SECTION 2: WHY USER FITS ----
    if content.get("fit_mapping"):
        story.append(p(f"2. Why {user_name or 'You'} Is a Strong Fit for {interviewer_name}'s Team", styles, "section"))
        story.append(p(
            f"{interviewer_name} is building a function and needs people who help <i>prove the model</i>. "
            f"Here's the explicit mapping of {user_name or 'the candidate'}'s background to their stated needs:",
            styles, "body",
        ))

        fit_data = [[
            header_cell(f"{interviewer_name}'s Need", styles),
            header_cell(f"{user_name or 'Candidate'}'s Direct Match", styles),
            header_cell("Evidence to Cite in Interview", styles),
        ]]
        for row in content["fit_mapping"]:
            fit_data.append([cell(row["need"], styles), cell(row["match"], styles), cell(row["evidence"], styles)])
        story.append(styled_table(fit_data, [2.6 * inch, 3.5 * inch, 3.6 * inch]))

        if content.get("fit_pitch"):
            story.append(Spacer(1, 10))
            story.append(p("The One-Sentence Fit Pitch (memorize this):", styles, "sub_section"))
            story.append(quote_block(f'"{content["fit_pitch"]}"', styles, doc))

        story.append(PageBreak())

    # ---- SECTION 3: COMPETITIVE LANDSCAPE (optional) ----
    if content.get("competitive_landscape"):
        cl = content["competitive_landscape"]
        story.append(p(f"3. Competitive Landscape — Know Who {company} Plays Against", styles, "section"))
        if cl.get("intro"):
            story.append(p(cl["intro"], styles, "body"))

        for table_spec in cl.get("tables", []):
            story.append(p(table_spec["title"], styles, "sub_section"))
            headers = [header_cell(h, styles) for h in table_spec["headers"]]
            data = [headers]
            for row in table_spec["rows"]:
                data.append([cell(c, styles) for c in row])
            n_cols = len(table_spec["headers"])
            total_width = 9.7 * inch
            col_widths = [total_width / n_cols] * n_cols
            story.append(styled_table(data, col_widths))
            story.append(Spacer(1, 8))

        for para in cl.get("synthesis_paragraphs", []):
            story.append(p(para, styles, "body"))

        for quote in cl.get("synthesis_quotes", []):
            story.append(quote_block(f'"{quote}"', styles, doc))

        story.append(PageBreak())

    # ---- SECTION 4: QUESTIONS TO ASK ----
    if content.get("questions_to_ask"):
        story.append(p(f"4. Questions to Ask {interviewer_name}", styles, "section"))
        q_data = [[
            header_cell("#", styles),
            header_cell("Question", styles),
            header_cell(f"Why It Works for {interviewer_name}", styles),
        ]]
        for i, qd in enumerate(content["questions_to_ask"], 1):
            q_data.append([str(i), cell(qd["question"], styles), cell(qd["rationale"], styles)])
        story.append(styled_table(q_data, [0.7 * inch, 5.0 * inch, 4.0 * inch]))
        story.append(Spacer(1, 12))

    # ---- SECTION 5: TALKING POINTS (optional) ----
    if content.get("talking_points"):
        tp = content["talking_points"]
        story.append(p(f"5. {tp.get('section_title', 'Talking Points')}", styles, "section"))
        if tp.get("intro"):
            story.append(p(tp["intro"], styles, "body"))
        if tp.get("pitch_60s"):
            story.append(p("60-second pitch:", styles, "sub_section"))
            story.append(quote_block(f'"{tp["pitch_60s"]}"', styles, doc))
        if tp.get("distinctions"):
            story.append(p("Key distinctions:", styles, "sub_section"))
            story.append(p(tp["distinctions"], styles, "body"))
        if tp.get("when_right_vs_overkill"):
            story.append(p("When to use vs. when not to:", styles, "sub_section"))
            story.append(p(tp["when_right_vs_overkill"], styles, "body"))
        if tp.get("honest_framing"):
            story.append(p("Honest framing if asked about lighter experience:", styles, "sub_section"))
            story.append(quote_block(f'"{tp["honest_framing"]}"', styles, doc))
        story.append(PageBreak())

    # ---- SECTION 6: JD THEMES ----
    if content.get("jd_themes"):
        story.append(p("6. JD-Specific Themes — Prepared Four-Beat Answers", styles, "section"))
        for theme in content["jd_themes"]:
            story.append(p(theme["theme_title"], styles, "sub_section"))
            t_data = [
                [header_cell("Thesis", styles), header_cell("Example", styles),
                 header_cell("Resolution", styles), header_cell("Company Tie-In", styles)],
                [cell(theme["thesis"], styles), cell(theme["example"], styles),
                 cell(theme["resolution"], styles), cell(theme["company_tie"], styles)],
            ]
            story.append(styled_table(t_data, [2.4 * inch, 3.2 * inch, 2.2 * inch, 1.9 * inch]))
            story.append(Spacer(1, 12))
        story.append(PageBreak())

    # ---- SECTION 7: RESPONSE BANK ----
    if content.get("response_bank"):
        story.append(p("7. Response Bank — From the Mock Interview", styles, "section"))
        rb_data = [[
            header_cell("#", styles), header_cell("Question", styles),
            header_cell("Thesis", styles), header_cell("Example", styles),
            header_cell("Resolution", styles), header_cell("Company Tie-In", styles),
        ]]
        for r in content["response_bank"]:
            rb_data.append([
                cell(r["number"], styles),
                Paragraph(r["question"], styles["q_bold"]),
                cell(r["thesis"], styles),
                cell(r["example"], styles),
                cell(r["resolution"], styles),
                cell(r["company_tie"], styles),
            ])
        story.append(styled_table(rb_data, [0.4 * inch, 1.5 * inch, 1.6 * inch, 2.6 * inch, 2.0 * inch, 2.0 * inch]))
        story.append(Spacer(1, 12))

    # ---- SECTION 8: CHECKLIST + FINAL READ ----
    if content.get("checklist"):
        story.append(p("8. Pre-Interview Checklist", styles, "section"))
        cl_data = [[header_cell("Item", styles), header_cell("Why It Matters", styles)]]
        for item in content["checklist"]:
            cl_data.append([cell(item["item"], styles), cell(item["why_it_matters"], styles)])
        story.append(styled_table(cl_data, [4.5 * inch, 5.2 * inch]))
        story.append(Spacer(1, 10))

    if content.get("final_read"):
        story.append(p(f"<b>Final read on {interviewer_name}:</b> {content['final_read']}", styles, "body"))

    doc.build(story)
    return output_path


# =========================================================================
# EXAMPLE USAGE
# =========================================================================

if __name__ == "__main__":
    # Minimal example. Populate the dicts below from the mock interview + research.
    example_content = {
        "user_name": "Alex",
        "company": "ExampleCo",
        "role": "Sr. Product Manager",
        "interviewer_name": "Jane Doe",
        "interviewer_brief": {
            "title": "VP of Product",
            "background": "Consumer SaaS, growth-stage",
            "location": "San Francisco",
            "reputation": "Detail-oriented, data-first.",
            "mandate_bullets": ["Scale product org from 5 to 15", "Launch enterprise tier"],
            "company_facts_bullets": ["100K+ customers", "Series C, $50M raised"],
        },
        "fit_mapping": [
            {
                "need": "Scale a growing product org",
                "match": "Has hired and managed 3 PMs at previous role",
                "evidence": "Grew team from 1 to 4 PMs at LastCo over 18 months",
            },
        ],
        "fit_pitch": "I've scaled product teams before and I'm ready to do it at ExampleCo.",
        "questions_to_ask": [
            {
                "question": "What does success look like for this role in the first 90 days?",
                "rationale": "Standard execution-focused question.",
            },
        ],
        "response_bank": [
            {
                "number": "Q1",
                "question": "Walk me through your background.",
                "thesis": "Product leader with growth-stage focus.",
                "example": "Led product at LastCo from Series A to Series B.",
                "resolution": "Grew MAUs 5x in 18 months.",
                "company_tie": "ExampleCo's Series C stage matches my zone of strength.",
            },
        ],
        "checklist": [
            {"item": "Resume saved", "why_it_matters": "Send before the call."},
        ],
        "final_read": "Jane wants execution, not just ideas. Lead with what you've shipped.",
    }

    output = build_pdf("/tmp/example_interview_prep.pdf", example_content)
    print(f"PDF generated at: {output}")
