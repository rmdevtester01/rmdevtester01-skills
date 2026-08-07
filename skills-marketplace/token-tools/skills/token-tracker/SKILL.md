---
name: token-tracker
description: Apply this skill at the start of every new conversation or project request, BEFORE responding to the user's actual request. It surfaces a verbal summary of the user's current rolling Pro usage-window status versus historical project totals, so the user knows where they stand against their plan's rolling limit before committing to new work. Trigger on the first user message of any new conversation. Do NOT re-trigger within the same conversation unless explicitly asked.
---

# Token Tracker

## Purpose
The user is on a **Claude Pro** subscription: usage is metered over a rolling window (historically ~5 hours) plus weekly caps — a rate limit on how much they can do, **not** per-token billing and **not** rollover. Pro limits are not published as a fixed token count and shift over time, so **do not assert a specific cap as official** — treat any hard number as the user's personal working proxy, and point them at their own Claude usage/settings UI for the authoritative figure and reset time. They need visibility into:
1. **Current window usage** — roughly how much of the rolling window they've spent
2. **Historical project totals** — cumulative spend per active project (where a ledger exists)
3. **Headroom for the new request** — whether they have allowance for what they're about to ask

This skill delivers a concise summary at the top of every new conversation so the user can plan their session.

## Pro plan structure (stable facts, not a cap)
From the account's Settings → Usage, the Pro plan exposes **three separate meters**. These are the durable facts; the *percentages* shown in the UI are momentary — read them live, never bake them in:
1. **Current session** — a rolling ~5-hour window; governs the active work stretch.
2. **Weekly — All models** — the shared weekly cap everything draws from (the usual binding constraint). Resets weekly at a fixed time in the account's local timezone.
3. **Weekly — Fable** — a **separate** weekly bucket for Fable (Fable 5); heavy Fable use is metered on its own, not against the general weekly cap. Resets on the same weekly boundary.

Still **not** per-token billing and **not** rollover. When you can't see live figures (e.g. in Claude Code), describe this structure and point the user at Settings → Usage for the current numbers — do not invent percentages.

## Surface differences (Chat vs Claude Code)
The rolling ledger lives in Claude.ai artifact storage under the key `token_tracker:v2` — that store exists **only in Claude.ai Chat**. In **Claude Code** there is no artifact ledger to read. When running in Code (or any time the ledger is unavailable): say so plainly and give a qualitative, session-scoped read of where things stand — **do not fabricate window/project numbers**. The Chat ledger remains the source of truth for actual token totals.

<!--
  NOTE (placement): moved from 'core' to 'token-tools' (2026-07 skills audit, item 6) so all
  three token skills share one plugin. The old core placement was justified by name-uniqueness,
  which validate-naming.sh already enforces across plugins, so it bought nothing. Pairs with
  token-tools:token-analysis-for-artifacts (prospective forecast) as the retrospective ledger.
  token-tracker references the artifact storage key `token_tracker:v2` — that key is
  namespace-independent and did NOT change with the move; see the skills-index
  cross-reference notes before any further rename.

  This body appears shorter than the others; if your account version has more sections
  (ledger format, output template, examples), paste the rest below.
-->
