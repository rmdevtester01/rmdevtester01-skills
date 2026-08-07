---
name: token-efficiency
description: >
  Apply this skill during generation of any output — reports, templates, PDFs, artifacts, summaries, tables, documents, or inline responses — to produce the same quality with fewer tokens. It governs in-flight choices: phrasing, structural compression, avoiding redundant scaffolding, omitting filler. Defers to token-analysis-for-artifacts for the pre-flight cost estimate before file creation, and to token-tracker for current usage status checks. Use proactively on every output task, especially when the user asks to "recreate," "regenerate," "update," or "optimize" prior work, or when output length matters.
---

# Token Efficiency Skill

## Core Principle

Every output should deliver maximum information density. Tokens spent on redundancy, verbose prose, or repeated structure are wasted. The goal: **same structure, same completeness, fewer tokens** — unless a structural change is warranted, in which case ask the user first.

---

## The 5 Token-Efficiency Rules

Apply all five rules before generating any substantial output.

### Rule 1 — Merge Redundant Parallel Sections
**Pattern to catch:** Multiple sections that cover the same topic with slight variations (e.g., "Top 20 Organic Keywords" + "Top 20 Organic Keyword Opportunities" = two lists covering the same category).

**Fix:** Merge into one unified table with a column that captures the variation (e.g., a "Type" or "Status" column: `Current | Opportunity | ★ Priority`).

**Evidence from SEO Template audit:**
- Sections 5+6+7+8 (four 20-item keyword lists) → merged to 2 unified tables
- Saved ~880 tokens (the single largest saving in the audit)

**Rule:** If two sections share the same subject and same format, they should be one section with a differentiating column.

---

### Rule 2 — Consolidate Scattered Callouts
**Pattern to catch:** Tips, warnings, or interview hints embedded inside analytical sections throughout a document.

**Fix:** Move all callouts to a dedicated section at the end (e.g., "Interview Prep," "Tips & Tactics," "Key Reminders"). Within analytical sections, replace the callout with a ★ marker or inline bold flag only if critical.

**Evidence from SEO Template audit:**
- 6 interview tips scattered across 8 sections → consolidated into Section 12 (Interview Prep)
- Saved ~120 tokens + improved document flow

**Rule:** Callouts that repeat or reference section content belong in a dedicated callout section, not mid-analysis.

---

### Rule 3 — Replace Verbose Prose Intros with 1-Line Context
**Pattern to catch:** A paragraph of prose before a table that restates what the table is about to show.

**Fix:** One sentence of context maximum. Let the table carry the information.

**Bad:**
> "The Advanced Practice Provider (APP) Compliance Market is driven by the regulatory backdrop: in 22+ states, NPs are still legally required to have a collaborating or supervising physician to practice. PAs require physician collaboration in all 50 states. With over 2 million annual healthcare job openings growing 40% per BLS, organizations are racing to deploy NPs and PAs — but compliance complexity at scale is a massive bottleneck. the platform removes that bottleneck."

**Good:**
> "In 22+ states, NPs legally require a collaborating physician; PAs in all 50. With 2M+ annual openings growing 40% (BLS), compliance at scale is a critical bottleneck — the platform removes it."

**Evidence from SEO Template audit:** Saved ~220 tokens across 3 sections.

**Rule:** If a table or structured section follows immediately, the prose intro should be ≤2 sentences.

---

### Rule 4 — Trim Lists to Their Useful Subset
**Pattern to catch:** Exhaustive bullet lists (8–10+ items) where the bottom items add diminishing value and are never referenced again.

**Fix:** Keep the top 4–6 most relevant items. For lists that must stay complete (e.g., 20 keywords per client request), compress the annotation column rather than cutting rows.

**Evidence from SEO Template audit:**
- 10-item "Industry Categories" list → trimmed to inline prose with top 5
- Saved ~60 tokens; no meaningful information lost

**Rule:** Any list of 8+ items should be audited. If the bottom items are not referenced elsewhere in the document, trim or compress.

---

### Rule 5 — Never Duplicate Table Data in Prose
**Pattern to catch:** A table is present, and the text below it restates the same information in prose or bullet form.

**Fix:** Remove the prose restatement. If a synthesis point is needed, write one sentence that adds insight the table doesn't show — not a restatement of what it already shows.

**Evidence from SEO Template audit:**
- Budget table (Sec 17) had prose bullets that restated channel priorities already in the table and in Sec 13
- Saved ~80 tokens

**Rule:** After a table, the next element should either (a) add new information, (b) transition to the next section, or (c) be blank. Never restate the table.

---

## Before Generating Any Output: The Pre-Flight Checklist

Run this mentally before writing:

- [ ] **Are there parallel sections on the same topic?** → Merge with a differentiating column (Rule 1)
- [ ] **Are callouts/tips scattered throughout?** → Consolidate into a dedicated section (Rule 2)
- [ ] **Does any section start with a long prose intro before a table?** → Trim to 1–2 sentences (Rule 3)
- [ ] **Are there lists with 8+ items?** → Audit for trimming or compression (Rule 4)
- [ ] **Does prose after a table restate what the table shows?** → Delete the prose (Rule 5)

---

## Structural Change Protocol

**Never make a structural change silently.** If applying these rules would require a structural change (merging sections, removing a section entirely, changing the number of sections), ask the user first:

> "To reduce token usage I'd suggest [specific change]. This would affect [what changes]. Want me to proceed?"

**What counts as structural:** merging two named sections, removing a section entirely, changing section order.

**What does NOT require asking:** trimming prose intros, removing redundant prose below tables, consolidating tips within an existing section, compressing annotation columns.

---

## Benchmark Reference (SEO Insights Template)

| Metric | Original | Optimized | Change |
|--------|----------|-----------|--------|
| Estimated tokens | ~5,840 | ~4,200 | -28% |
| Sections | 19 | 13 | -32% |
| Keyword lists | 4 × 20 items | 2 unified tables | -50% |
| Scattered tips | 6 locations | 1 section | Consolidated |
| Prose intro avg length | 4–6 sentences | 1–2 sentences | Compressed |

The 28% reduction was achieved with **zero content loss** — every data point, keyword, competitor, KPI, and insight is present in the optimized version.

---

## Quick Application Guide by Output Type

| Output Type | Primary Rules to Apply | Expected Savings |
|---|---|---|
| Multi-section reports / templates | Rules 1, 2, 3 | 20–35% |
| Keyword / competitor / KPI tables | Rules 1, 4 | 30–50% |
| Interview prep / briefing docs | Rules 2, 3, 5 | 15–25% |
| PDFs with tables + prose | Rules 3, 5 | 15–20% |
| Artifacts / dashboards | Rules 4, 5 | 10–20% |
| Simple summaries / emails | Rules 3, 5 | 10–15% |

---

## What This Skill Does NOT Do

- Does not cut content that adds unique value
- Does not merge sections with genuinely different purposes
- Does not compress tables that the user has explicitly asked to keep full
- Does not make structural changes without asking first
- Does not apply to short outputs (< ~500 tokens) where the overhead of optimization exceeds the benefit
