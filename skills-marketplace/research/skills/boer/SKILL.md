---
name: boer
description: Business Opportunities Exhaustive Research (BOER). Use this skill whenever the user asks about business niches, side hustles, "what business should I start," profitable industries, market gaps, untapped problems, niche opportunities, small business ideas, or evaluating a specific niche/industry for a small business. Triggers on phrases like "find me a niche," "what's a good business to start," "research opportunities in X industry," or any request for evidence-backed business opportunity DISCOVERY across a niche or industry. Produces a stack-ranked, evidence-cited report covering industry-specific problems (sourced from Reddit, X, Bluesky, public LinkedIn and Meta content where accessible, LLM/search queries), Impact + Revenue scoring, ideal buyer mix, cross-industry edge cases, build format (Digital / Non-Digital / Mix), and whether the opportunity is better delivered as a skill vs. artifact. Outputs both a .md and .pdf file inside a dedicated folder. This is NOT for validating one specific offer or idea the user already has in hand — "is MY idea worth it," "should I pursue this," "is this niche profitable for my offer" go to par3-pd:offer-validator — and NOT for building an ideal customer profile document (use gtm:icp-builder).
---

# BOER — Business Opportunities Exhaustive Research

A research skill for evaluating business niches with evidence, not vibes.

## Prerequisite skill ordering

Before running BOER, run any earlier user skills that are configured to run first. In particular:

1. **token-tracker** — surface rolling token usage at the start of the conversation (only if this is the first message of the chat).
2. **token-analysis-for-artifacts** — run before producing the final artifact (the .md + .pdf), since BOER outputs files.
3. **token-efficiency** — apply while writing the report.
4. **level-reframing** — apply to every claim (no overstated "moats," "10x markets," etc. without evidence).

If any of these skills aren't available in the current environment, proceed without them — but never skip them when they are available.

## Step 1 — Always confirm scope first

Never auto-run. Even if the user gives a clear niche, ask a short scope-confirmation question before any research. Use the `ask_user_input_v0` tool with 1–3 buttoned questions covering whichever of these are still ambiguous:

- **Starting point**: Do they have a specific industry/niche in mind, a rough theme (e.g. "anything in healthcare"), or a totally open "surprise me"?
- **Builder profile**: Solo operator, small team, or unclear? This affects which opportunities are realistic.
- **Constraints**: Geography, budget ceiling, time-to-revenue urgency, hard "no"s (e.g. "no physical inventory").

Skip questions whose answers are already in the conversation. If the user pushes back ("just run it"), proceed with stated assumptions written inline at the top of the report.

## Step 2 — Calibrate research depth to the niche

Research depth is **not fixed**. Scale it to the industry and the specificity of problems being investigated:

- **Narrow, well-defined niche** (e.g. "pickleball coaching software for clubs"): ~3–6 targeted searches across 2–3 source types.
- **Mid-scope industry** (e.g. "opportunities in dental practice ops"): ~7–12 searches across 4+ source types.
- **Broad / open-ended** (e.g. "what's a good niche in healthcare"): 12–20+ searches, multiple sub-niches probed, then stack-ranked.

State the chosen depth and rationale in the report's opening paragraph so the user can see why N searches were used.

## Step 3 — Source coverage (industry problems)

For each niche under evaluation, pull evidence from a mix of these. Don't rely on a single source type; triangulate.

- **Reddit**: search relevant subreddits for complaints, "I wish there was a tool for..." threads, and rant posts. **Important search-tool quirk**: `site:reddit.com` queries often return nothing in this environment. Instead, use natural-language queries that include subreddit names or content words (e.g. `r/mtgfinance small seller advice`, or `MTG Commander deck buying frustrating`) — Reddit results frequently come through mirror domains (libreddit, redlib, applefritter, etc.) and are valid sources. Quote sparingly (≤15 words per quote, one quote per source — copyright rules apply). Paraphrase otherwise.
- **X (Twitter)**: similarly, `site:twitter.com` and `site:x.com` queries are unreliable. Use natural-language queries naming a known community figure or topic, and accept that X content often surfaces second-hand via news articles that quote tweets. Treat those secondary citations as valid evidence.
- **Always attempt Reddit and X at least once per run.** If neither surfaces useful results after one search each, disclose this in the "What was NOT investigated" section of the report rather than silently skipping them.
- **Social platforms**: X, Bluesky, public LinkedIn posts/articles, and public Meta content (Threads, public Facebook groups/pages). LinkedIn and Meta are largely behind auth walls — pull what's publicly accessible via search indexes, but don't treat them as required for every query. If nothing public surfaces, note it and move on.
- **LLM-style queries**: search engines for "[industry] biggest problems 2026," "[role] daily frustrations," "why [tool category] sucks," etc.
- **Search engines**: Google, Bing, DuckDuckGo — different result mixes surface different evidence. Don't only rely on one.
- **Industry-specific sources**: trade publications, niche forums, Indie Hackers, Hacker News "Ask HN: what would you pay for?" threads.

Every claimed "problem" must have at least one citation. If a problem is asserted without a source, drop it or label it explicitly as `[Hypothesis — unverified]`.

## Step 4 — Score each problem on Impact and Revenue

For every distinct problem identified, score on two 0–10 scales. Be honest, not generous. Apply level-reframing: don't call something a "10" without the evidence to back it.

**Impact (0–10)** — How worthwhile is solving this problem as a small business?
- 0 = impossible / not worth the setup
- 5 = solvable but mediocre payoff, crowded or capped market
- 10 = worth the struggle, long-term growth potential, durable demand

**Revenue (0–10)** — How fast can realistic profitability be reached? Calibrate to what is actually achievable, not aspirational.
- 0–2 = no revenue likely for 6+ months; long build, slow sales cycle, heavy capital or trust required (e.g. regulated B2B SaaS, marketplaces)
- 3–4 = first revenue in 2–6 months; meaningful build time before profitability
- 5–6 = first revenue in roughly 30–60 days with consistent effort; profitability within a few months
- 7–8 = first revenue in 1–4 weeks; small but real cash flow quickly (e.g. low-cost digital products, services with warm audience)
- 9–10 = profitable in days to ~2 weeks; very low setup cost, immediate-demand offerings to existing audiences (rare and usually short-lived edges)

Present problems in a stack-ranked table sorted by **(Impact + Revenue) / 2** descending, with both scores visible. Include a one-sentence justification per row citing the evidence.

## Step 5 — Identify the audience and buyer mix

For the top-ranked opportunities (top 3–5), describe the ideal buyer along this spectrum:

- **High volume / low price** (e.g. $5–$30 digital products to a broad audience)
- **Mid volume / mid price** (e.g. $50–$500 tools, services, courses to a defined segment)
- **Low volume / high price** (e.g. $1k–$50k+ B2B contracts, consulting, enterprise tools)
- **Anything in between**, with reasoning

Include: who they are, where they hang out (so the user knows where to market), and rough willingness-to-pay evidence. If willingness-to-pay can't be sourced, mark it as estimated.

## Step 6 — Cross-industry / edge-case opportunities

If a problem or solution applies across multiple industries or audiences, call it out explicitly. For each cross-industry opportunity:

- Why it works in multiple verticals (with evidence — shared workflows, shared regulations, shared tooling gaps, etc.)
- How to structure: start narrow in one vertical, then expand? Horizontal play from day one? Platform vs. point solution?
- How to scale after initial traction: productize, hire, license, franchise, etc.

## Step 7 — Build format: Digital, Non-Digital, or Mix

For each top opportunity, recommend the build format with reasoning:

- **Digital products**: templates, frameworks, courses, SaaS, AI tools, content, communities. Best for high-margin, low-overhead, fast iteration.
- **Non-digital products**: physical goods, stickers, printed items, hands-on services, local labor. Best when the problem genuinely requires atoms or human presence.
- **Mix**: digital core with physical fulfillment, services productized into templates, etc.

Justify the choice based on the problem's nature, not the user's preferences (unless they stated a constraint in scope).

## Step 8 — Skill vs. Artifact vs. Other delivery

For each recommended opportunity, advise on the best delivery mechanism for scalability:

- **Skill**: repeatable workflow, benefits from triggering across many conversations, has consistent inputs/outputs.
- **Artifact**: one-off deliverable, presentation-style output, or interactive tool the user runs once.
- **Better alternative**: sometimes neither fits — a standalone web app, a Notion template, a Gumroad product, a service offering, etc. Recommend honestly if so.

## Step 9 — Final Recommendations and Honest Synthesis (path forward)

The most important section. After all the stack-ranking, deep-dives, and cross-industry plays, the user needs one clear answer: **given their actual constraints, what should they do?**

This section is where level-reframing matters most. Do not pad with "all options have merit" hedging. The job is to name the realistic shortlist for the *stated* builder profile, capital, and constraints — and call out which opportunities are unrealistic for *this* operator, even if they ranked high on the abstract scale.

Required structure:

- **The realistic shortlist (1–3 opportunities max).** Name them. Explain why these specifically survive the user's constraints — capital, audience, skill, time, geography. If the answer is "only one opportunity is realistic," say so.
- **What was high-ranked but is NOT realistic for this user.** Be specific about why. Example: "Custom alters ranked Avg 5.0 but requires existing artistic skill — not viable here without that pre-condition." This prevents the user from chasing a high score that doesn't apply to them.
- **The honest first move.** One sentence: what's the very first action the user should take this week to test the top recommendation? Concrete, not aspirational.
- **What would change the recommendation.** Briefly: if the user had +$X capital, an existing audience, or skill Y, which other opportunity would move up?

This section is short — typically 200–400 words. Its job is decisive synthesis, not new analysis. If the BOER report has done its job, this section writes itself.

**Validation handoff.** After delivering the report, if the user wants to pursue a shortlist item, offer to run `par3-pd:offer-validator` on it — and carry the BOER evidence forward (the problem citations, buyer-mix findings, and stated constraints) so the validator's intake questions that BOER already answered are not re-asked.

## Output format

Produce **two files in a dedicated report folder**, with the location depending on the surface:

**In Claude.ai Chat:**
1. Create folder: `/mnt/user-data/outputs/BOER/reports/BOER-<short-niche-slug>-<YYYYMMDD>/`
   (If the `/mnt/user-data/outputs/BOER/reports/` parent doesn't exist yet, create it. This keeps every BOER report grouped together over time, alongside the canonical skill file at `/mnt/user-data/outputs/BOER/skill/SKILL.md`.)
2. Write `report.md` inside the report folder (full analysis).
3. Generate `report.pdf` from the same content (use the pdf skill if needed for generation — never `pypdf` for creation).
4. Call `present_files` with both filepaths (md first, pdf second).

**In Claude Code:** those paths and tools don't exist. Instead:
1. Create folder: `status/boer-reports/BOER-<short-niche-slug>-<YYYYMMDD>/` in the repo.
2. Write `report.md` there and commit it (the repo is the store, same as the carryover docs).
3. Generate `report.pdf` with whatever tooling the environment has (e.g. markdown → HTML → headless-Chromium print). If no PDF tooling is available, deliver the .md alone and say so — don't block the report on the PDF.
4. Deliver with the file-send tool (md first, pdf second if produced).

Also note: the scope-confirmation questions in Step 1 reference the `ask_user_input_v0` tool — that is the Chat form tool. In Claude Code, use the AskUserQuestion tool for the same buttoned questions.

### Report structure (use this exact template)

```markdown
# BOER Report: [Niche / Theme]
*Generated: [date] · Research depth: [N searches across M source types] · Rationale: [why this depth]*

## 1. Scope confirmation
- Starting point: ...
- Builder profile: ...
- Constraints: ...
- Assumptions made: ...

## 2. Industries and problems investigated
[Brief 2-3 sentence summary of what was researched and where.]

## 3. Stack-ranked opportunities
| Rank | Problem | Industry | Impact (0–10) | Revenue (0–10) | Avg | Evidence |
|------|---------|----------|---------------|----------------|-----|----------|
| 1 | ... | ... | 8 | 7 | 7.5 | [source] |
...

## 4. Deep dive: top 3–5 opportunities
For each:
### [Opportunity name]
- **The problem** (with evidence and citations)
- **Audience and buyer mix** (high-volume/low-price ↔ low-volume/high-price + reasoning)
- **Build format** (Digital / Non-Digital / Mix + why)
- **Delivery mechanism** (Skill / Artifact / Other + why)
- **Risks and counter-evidence** (what could make this not work)

## 5. Cross-industry / edge-case plays
[Only if any exist — otherwise state "None surfaced in this pass."]

## 6. What was NOT investigated
[Honest list of niches/sources skipped and why — keeps the user's expectations calibrated.]

## 7. Sources
[Full list of cited sources with URLs.]

## 8. Final Recommendations and Honest Synthesis
- **The realistic shortlist:** [1–3 named opportunities that survive the user's constraints]
- **High-ranked but NOT realistic for this user:** [list with reasons]
- **The honest first move:** [one concrete action for this week]
- **What would change the recommendation:** [conditions under which a different opportunity moves up]
```

## Quality bar (non-negotiable)

- **No fabricated citations.** Ever. If a source can't be found, omit the claim.
- **No overstated levels.** "Underserved," "huge market," "high moat" — all require evidence in context or get rewritten with weaker, accurate language.
- **Copyright**: ≤15-word quotes, one quote per source, paraphrase everything else.
- **Disclosures**: Where a score or claim is an estimate rather than sourced, label it `[Estimate]` inline.
- **Token efficiency**: don't pad. Stack-rank tables and bullets beat long prose for this output type.

## Examples of when to trigger

- "What's a good business I could start this month?"
- "Find me a niche in the pet industry"
- "What digital product categories are underserved right now?"
- "What problems are dentists complaining about online?"
- "I want to start a side hustle, give me options"
- "Research the market for X" (when X is a business concept)

## Examples of when NOT to trigger

- Generic business advice that doesn't ask for niche research ("how do I write a business plan?")
- Help with an existing business's operations (marketing copy, pricing for a specific product they already sell)
- Pure career advice ("should I quit my job?")
- Validating one specific offer/idea the user already has — "is selling resume templates viable," "should I pursue this," "is my idea worth it" → hand off to `par3-pd:offer-validator`
- Building an ideal customer profile document → `gtm:icp-builder`
