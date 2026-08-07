---
name: token-analysis-for-artifacts
description: Use this skill ONLY as a pre-flight cost estimate before creating a file artifact (docx, pdf, pptx, xlsx, or any other downloadable file). It runs once, before generation begins, to surface the projected token cost of producing the artifact so the user can decide whether to proceed, scope down, or defer under the current plan limits. Do NOT use this skill for inline responses, for status checks of current usage (that's token-tracker), or for in-flight output reduction (that's token-efficiency). Trigger automatically whenever the user asks for a downloadable file or whenever an artifact-creating skill (docx, pdf, pptx, xlsx) is about to fire.
---

# Token Analysis for Artifacts

## Purpose
Before building any artifact (HTML widget, React component, docx, pptx, xlsx, PDF, or long-form file), perform a brief pre-build token analysis. This helps the user understand the estimated cost of the generation and requires their explicit approval before tokens are spent.

## When to trigger this skill
Trigger whenever:
- The user asks to create a visual artifact (interactive table, dashboard, chart, diagram)
- The user asks to generate a file (Word doc, PDF, slide deck, spreadsheet)
- The output will require more than ~300 tokens to generate
- The task involves multiple tool calls (web search + file creation, etc.)
- The response involves web search + synthesis (any inline response that pulls from one or more web searches and summarizes/analyzes the results)

Do NOT trigger for:
- Very short inline responses under ~300 tokens (brief prose, small tables in chat, code snippets under 20 lines)
- Simple factual questions answered from existing knowledge (no web search)
- Conversational replies

## Pre-Build Analysis Format

Before writing any code or calling any file-creation tool, output a short analysis block like this:

---

## Token analysis

| Factor | Estimate |
|---|---|
| [Component 1, e.g. HTML/CSS/JS artifact] | ~X–Y tokens |
| [Component 2, e.g. web searches] | ~X–Y tokens |
| [Component 3, e.g. keyword rationale prose] | ~X–Y tokens |
| [Component 4, e.g. table data] | ~X–Y tokens |
| **Estimated total output tokens** | **~X–Y tokens** |

**Complexity:** Low / Medium / High
**Recommendation:** [Proceed as requested / Suggest simplification / Recommend Research feature for 20+ tool calls]

---

## MANDATORY APPROVAL GATE

**STOP. Do not proceed to build.** After displaying the analysis, explicitly ask the user:

> *"Approve this scope and proceed?"*

Wait for explicit confirmation (e.g., "yes," "proceed," "approved," "go ahead," "build it") before any file creation, code generation, or build-related tool calls. If the user requests changes, iterate on the scope until aligned, then re-ask for approval.

**This applies regardless of estimated token size — even small builds require approval.**

The only exception is if the user has explicitly stated in the current conversation that approval can be skipped (e.g., "just build small things under 1k without asking" or "skip the approval step for this session").

**Behaviors that violate this skill:**
- Running token analysis and immediately proceeding to build in the same turn
- Treating "pause briefly" as sufficient
- Inferring approval from prior unrelated approvals
- Proceeding because the task seems "obviously aligned"

**Behaviors that satisfy this skill:**
- Posting analysis → asking for approval → waiting for user reply → building only after explicit "yes"
- Iterating on scope when the user pushes back, then re-asking before building

## Estimation Guidelines

Use these rough benchmarks when estimating:

| Artifact type | Typical token range |
|---|---|
| Simple HTML widget (no chart library) | 800–1,500 |
| Interactive HTML with Chart.js or D3 | 1,500–3,000 |
| React component (moderate complexity) | 1,200–2,500 |
| docx (1–3 pages) | 1,500–3,000 |
| pptx (5–10 slides) | 2,000–5,000 |
| xlsx (simple table) | 800–1,500 |
| PDF (generated via Python/bash) | 1,000–2,500 |
| Web search (per call) | 300–600 |
| Prose rationale / explanation | 100–300 per paragraph |
| Large multi-platform data table | 1,000–2,000 |

## Complexity Ratings

- **Low** — Single artifact, no external research needed, <1,500 tokens estimated
- **Medium** — Artifact + 1–5 web searches + rationale prose, 1,500–4,000 tokens
- **High** — Multi-tool workflow, rich artifact, extensive research, 4,000+ tokens → suggest Research feature if 20+ tool calls anticipated

## Simplification Options to Offer

If the estimate is high or the user pushes back, proactively suggest one or more of these:
- Reduce the number of platforms, columns, or data rows
- Use a static table in chat instead of an interactive artifact
- Split into phases (e.g., build MVP now, iterate later)
- Use the Research feature for deep multi-source tasks

## Post-Build Note (optional)

After completing the artifact, you may optionally note the approximate actual token usage if it differed significantly from the estimate, so the user can calibrate expectations for future iterations.

## Example Flow

**Request:** Interactive paid ad opportunity table — 6 platforms × 6 keyword columns.

**Step 1 — Post analysis:**

| Factor | Estimate |
|---|---|
| HTML/CSS/JS interactive table artifact | ~2,000–2,500 tokens |
| Web searches (3 calls) | ~900–1,500 tokens |
| Keyword rationale prose | ~600–900 tokens |
| **Estimated total** | **~3,500–4,900 tokens** |

**Complexity:** High
**Recommendation:** Proceed — well within single-session range.

**Step 2 — Ask:** "Approve this scope and proceed?"

**Step 3 — Wait for user reply.**

**Step 4 — Build only after explicit approval.**
