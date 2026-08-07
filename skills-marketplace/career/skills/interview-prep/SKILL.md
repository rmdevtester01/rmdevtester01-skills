---
name: interview-prep
description: Use this skill whenever the user is preparing for a job interview — including phrases like "help me prep for an interview," "interview tomorrow," "mock interview," "interview prep for [company]," or the explicit command "/interview-prep." Also trigger when the user shares a job description, an interviewer's LinkedIn URL, or a company link in the context of an upcoming interview. Produces a structured interview prep package — interviewer research, company fit narrative, competitive landscape, questions to ask, role-specific talking points, JD-specific themes, a response bank built through a live mock interview, and a downloadable PDF.
---

# Interview Prep Skill

This skill produces a comprehensive interview prep package built on the **four-beat answer structure**: Thesis → Example → Resolution → Company Tie-In. The skill is built around a live mock interview (5 questions, one pass, real-time feedback) where the user's actual answers become the response bank in the final PDF.

## When to use this skill

Trigger on:
- Explicit phrases: "help me prep for an interview," "interview tomorrow," "interview prep," "mock interview," "I have an interview"
- The explicit command `/interview-prep`
- The user shares a job description, an interviewer's LinkedIn URL, or company links in the context of an upcoming interview
- Follow-up sessions where the user wants to continue interview prep work

Do NOT trigger on:
- Generic career advice questions ("should I take this job," "how do I negotiate salary")
- Resume editing without interview context
- Performance reviews or other workplace prep (unless user explicitly asks to adapt this skill)

## Core workflow

The skill runs in five phases. Move through them sequentially, confirming with the user at each transition.

### Phase 1: Intake & Research

0. **Check any prior triage record first (when available).** If the workspace carries a
   structured record of this company from an earlier screening pass, read it before asking
   anything — it typically carries role type, industry, fit scoring, and named gaps, all of
   which pre-fill intake and shape JD themes (a gap named at triage is a theme to prep).
   If no such record is accessible, proceed without it — never block on this step.

1. **Ask the user for the basics if not already provided:**
   - Company name
   - Role title
   - Interviewer name (and LinkedIn URL if available)
   - Job description (paste or upload)
   - Interview round (screening, hiring manager, executive, panel, final)
   - Date of the interview (so urgency can be calibrated)
2. **Research the web for all items the user didn't fill in:**
   - Web search for the company (recent news, press releases, leadership changes, growth phase)
   - Web search for the interviewer (current role, tenure, background, public statements, LinkedIn endorsements)
   - Web search for company's competitive landscape if relevant
   - Read the job description carefully for explicit themes (e.g., AI enablement, technical translator, specific platforms)
3. **After research, identify gaps:**
   - Tell the user what was found and what's still missing
   - Ask the user to fill in only the gaps that matter (e.g., "I couldn't find your past role at X — can you confirm dates and key wins?")
   - Proceed once gaps are filled or the user signals to proceed
4. **Confirm before moving to Phase 2.** Summarize what you have: "I've got the JD, found public info on [interviewer name], and identified [company] competes with [list]. Ready to start the mock interview?"

### Phase 2: Live Mock Interview

Run **5 questions, one pass, with feedback after each answer.**

**Ground rules to state at the start:**
- One question at a time
- User aims for ~60-90 seconds per answer
- After each answer, give brief feedback on the four required dimensions (see below)
- Adapt feedback in real time based on what the user struggles with
- Full debrief at the end before moving to Phase 3

**The 5 questions should cover this mix (adjust to role and interview round):**
1. **Opening pitch / why this role + why now** — tests narrative clarity and company tie-in
2. **Behavioral story (achievement under pressure)** — tests STAR structure and quantified impact
3. **Role-specific scenario (e.g., difficult client, technical translation, conflict)** — tests judgment and the "answer the actual question" muscle
4. **Career arc / personal motivation (e.g., five-year plan, why this transition)** — tests self-awareness and strategic fit
5. **Their turn: "What questions do you have for me?"** — tests preparation and strategic thinking

**Required feedback dimensions (cover all four every time, adapt emphasis based on what's struggling):**
- **Conciseness** — Are answers ~60-90 seconds? Is there a clear thesis in the first 5-7 seconds?
- **Hedging language** — Flag "maybe," "kind of," "I feel like," "I'm sure," "just," "I don't have X but"
- **Multi-part question discipline** — Did the user answer ALL parts of the question, or only the easiest one?
- **Company tie-in** — Did the answer connect back to the specific company/interviewer's mandate?

**Adapt in real time.** If the user is hedging heavily, lean harder on that. If they're missing multi-part questions, drill that specifically. If they're nailing all four dimensions, push on advanced structure (resolution piece, role framing).

**For each answer, provide:**
- A short "Strengths" note
- A short "Gaps" note
- A "Refined version" that demonstrates the four-beat structure (Thesis → Example → Resolution → Company Tie-In)
- If an answer is significantly off-target, offer a retry

### Phase 3: Final Debrief

After all 5 questions, deliver a consolidated debrief:
- Top 3 fixes before the real interview
- What's working — don't change
- Lower-priority polish items
- An honest read on the user's readiness

Ask: *"Before I build the PDF, is there anything else you want to add or adjust? For example, a specific story you didn't get to share, additional context about the interviewer, or a section you want emphasized?"*

### Phase 4: Build the Prep Package

Once the user confirms readiness, build the PDF using the structure below. Use the `assets/pdf_template.py` script as the starting point — it produces a landscape-orientation PDF with bordered quote blocks (using single-cell tables to avoid background-bleed bugs) and styled response-bank tables.

**Required sections in the PDF:**

| Section | Title | Purpose |
|---|---|---|
| 1 | Interviewer Brief | Title, tenure, background, education, location, reporting line, reputation, mandate. Always include "What [Company] actually does" with concrete numbers. |
| 2 | Why [User] Is a Strong Fit | Mapping table: 3-column (Interviewer's Need → User's Direct Match → Evidence to Cite). End with a one-sentence fit pitch in a quote block. |
| 3 | Competitive Landscape | Only if the role is in a contested market. Tables of competitors with their strengths/weaknesses and where the user's company wins/loses. Strategic synthesis paragraph. Suggested questions to ask about competitive losses. |
| 4 | Questions to Ask [Interviewer] | Table of 3-4 tailored questions with rationale for why each works for this specific interviewer. Customize to interviewer's mandate, tenure, and role. |
| 5 | [Subject] Talking Points | Subject changes based on interviewer focus — e.g., "Headless CMS Talking Points" for a technical interview, "GTM Strategy Talking Points" for a sales role, "Product Vision Talking Points" for a PM role. Include a 60-second pitch in a quote block, key concept distinctions, when-to-use vs. when-not-to-use framing, and honest framing for areas where the user has lighter experience. |
| 6 | JD-Specific Themes | 1-3 prepared four-beat answers for themes the JD explicitly calls out (e.g., "AI Enablement," "Technical Translator," "Cross-functional Leadership"). |
| 7 | Response Bank | Five-column table (#, Question, Thesis, Example, Resolution, Company Tie-In). Rows are populated from the user's actual mock interview answers, refined to the four-beat structure. |
| 8 | Pre-Interview Checklist | Two-column table (Item, Why It Matters). End with a "Final read on [Interviewer]" paragraph synthesizing what to lean into and what to avoid. |

**Quote blocks must use the single-cell table pattern** (not ReportLab's `backColor` on ParagraphStyle) to avoid background-bleed into headings above them. See the template script for the `quote_block()` helper.

### Phase 5: Deliver & Close

1. Deliver the PDF (`present_files` in Chat; the file-send tool in Claude Code — see File handling)
2. Briefly summarize what's in the package (one or two sentences)
3. Offer day-of basics: camera/lighting test, resume file naming, rehearsal advice
4. Wish the user well — do not be heavy-handed or over-coach

## Style notes for the skill

- Keep tone honest and direct. The user is preparing for a high-stakes conversation; flattery wastes their time.
- When the user pushes back or asks for clarification, treat it as a calibration signal, not criticism.
- If the user gives a weak answer in the mock, give a refined version — never just say "try again" without showing what better looks like.
- Always tie feedback to evidence from the user's own words. Quote what they actually said when flagging hedges or buried impact.
- Use the four-beat structure consistently. It's the skill's spine.
- Don't fabricate interviewer or company facts. If web search returns nothing, say so and ask the user.
- Don't claim specific tenures or dates without showing the math (e.g., "press release dated X, today is Y, so roughly Z weeks").

## File handling

- The PDF generation script lives at `assets/pdf_template.py`
- Output path convention, by surface:
  - **Claude.ai Chat:** `/mnt/user-data/outputs/[UserFirstName]_[Company]_[Role]_Interview_Prep.pdf`, delivered with `present_files`
  - **Claude Code:** those paths/tools don't exist. Write the PDF to the session scratchpad (or `status/` in the repo if it should persist) and deliver it with the file-send tool
- If the user requests revisions, increment with `_v2`, `_v3`, etc.
- Always use landscape orientation for readability of the wide response-bank tables

## Reference

See `assets/pdf_template.py` for the working PDF generation script with all styles, helpers, and table definitions pre-configured. Adapt the section content for each user; keep the structure consistent.
