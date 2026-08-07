---
name: icp-builder
description: >
  Build a consulting-grade Ideal Customer Profile (ICP) as a standalone, reusable
  document. Use whenever the user says "build an ICP", "ideal customer profile",
  "/icp-builder", "who exactly is the buyer for X", "define my/the target customer",
  "profile the buyer", or needs to understand a new industry's buyers as groundwork for
  messaging, positioning, or GTM strategy work. Produces an evidence-cited icp-*.md
  artifact that downstream skills consume. This is NOT for validating whether an offer
  is worth pursuing (use par3-pd:offer-validator — it emits this same ICP artifact as a
  side output), NOT for building a prospect list (use par3-pd:listbuilder — it consumes
  the artifact this skill produces), and NOT for discovering niches (use research:boer).
---

# ICP Builder

Produce an Ideal Customer Profile as a **standalone consulting deliverable** — the
upstream artifact that messaging, positioning, strategy, and list-building consume. The
register is consultant-to-client: precise, evidence-cited, no coaching filler. This
skill is the front end of the ICP → positioning → messaging chain and doubles as PMM
practice reps (see Step 4).

The output must follow the canonical schema in `references/icp-schema.md` — filename
`icp-<slug>-<YYYY-MM-DD>.md`, first line `# ICP — <Offer / Segment Name>`, sections 1–11.
Downstream skills recognize the artifact by that convention.

## Step 1 — Intake (short; skip anything already in context)

Establish four things, grouping questions naturally:

1. **The offer or segment** the ICP is for (a specific service, a product, or "I'm
   ramping on industry X" with no offer yet — both are valid).
2. **Intended use** — messaging/positioning work, a prospect list, industry ramp-up, or
   a client deliverable. This sets which sections get the most depth.
3. **What's already known** — prior research, an existing offer-validator report, client
   notes, or a boer report. Ingest rather than re-derive.
4. **Constraints** — geography, company-size bounds, verticals in/out of scope.

## Step 2 — Research

Web research draws on plan usage — in Claude Code the cost-gate applies, so state the
intended search scope (roughly how many searches, which sections they feed) and get
approval before running. Scale depth to intended use: an industry ramp needs sections
4–5–8 deep; a list-building input needs 2–3–10 sharp.

Search patterns per section (adapt, don't run mechanically):

- **Pains (4):** `[buyer role] "struggling with" OR "biggest challenge" [problem area]`,
  Reddit/community threads, "I wish there was" posts. Capture verbatim buyer language.
- **Alternatives (5):** `[solution category] alternatives OR "instead of"`, competitor
  positioning pages, "how do you handle X today" threads.
- **Budget (6):** pricing pages, `[category] pricing OR cost OR budget`, procurement
  discussions.
- **Watering holes (7):** `[role/industry] community OR slack OR conference OR podcast`.
- **Triggers (8):** funding/leadership-change/regulation news patterns for the segment;
  `"we just" OR "we're now" [situation]` posts.
- **Objections (9):** review-site complaints about the category, "why we didn't buy"
  posts, churn discussions.

Every claim gets a source in the evidence log (section 11). Anything asserted without a
source is labeled `[Hypothesis]` inline — never silently presented as researched fact.
`core:level-reframing` applies in full: no "underserved," "huge market," or "moat"
without evidence in context.

## Step 3 — Draft the artifact

Write all 11 schema sections. Omit a section only with a stated reason. Disqualifiers
(10) deserve real thought — they're what keeps a prospect list clean and messaging
focused; "looks like the ICP but isn't" is often the most valuable section for a
consulting client.

**Drafts stay out of the repo.** Present the draft directly in chat for review (or
render a .pdf/.docx if the user prefers a file — scratchpad, not the repo). The
committed `icp-*.md` is written only at Step 5, after the pressure-test — it is the
final pipeline artifact, not a working copy.

## Step 4 — Pressure-test (the PMM rep)

Before finalizing, run one short rep with the user — this is deliberate practice, not a
formality, and the user does the work:

1. Ask the user to answer, in their own words: *"Given this profile, what's the one-line
   positioning claim you'd lead with, and which pain does it answer?"*
2. Critique their answer against the artifact — does the claim match a top pain (4), beat
   the real alternative (5), and survive the objections (9)? Point to specific sections.
3. One revision pass, then record their final line in section 1 as "working positioning
   hypothesis `[Hypothesis]`" — it's an input to future positioning work, not a
   conclusion of this one.

If the user declines the rep, skip it without ceremony.

## Step 5 — Emit

- **Claude.ai Chat:** save to `/mnt/user-data/outputs/icp-<slug>-<YYYY-MM-DD>.md` with
  `create_file`, then `present_files`.
- **Claude Code:** write to `status/icp-<slug>-<YYYY-MM-DD>.md` in the repo and commit it
  (Tier 1 record), or hand back with the file-send tool. Offer a .pdf rendering alongside
  for reading — the .md is for the pipeline, not necessarily for the user's eyes.

Close by naming the handoffs: `par3-pd:listbuilder` accepts this file in place of its
intake; positioning/messaging work builds on sections 4, 5, and 9.

## Quality bar

- No fabricated sources or invented quotes; quote ≤15 words per source.
- Buyer language verbatim in section 4 — paraphrase everywhere else.
- Blank-with-reason beats filled-and-uncertain.
- Token efficiency applies: tables and tight bullets; the artifact is a working document,
  not a report.
