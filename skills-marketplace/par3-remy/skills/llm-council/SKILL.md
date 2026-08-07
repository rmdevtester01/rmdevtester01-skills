---
name: llm-council
description: Runs a high-stakes decision through five independent advisors (Contrarian, First Principles Thinker, Expansionist, Outsider, Executor), peer-reviews their reasoning anonymously, and has a chairman synthesize a final verdict. Use when someone says "council this," "run the council," "war room this," "pressure-test this," "stress-test this," or "debate this," or asks "should I X or Y," "which option," "what would you do," "is this the right move" about a decision with real tradeoffs. Not for factual lookups, simple yes/no questions, or creative writing.
---

# LLM Council Skill

This tool implements Andrej Karpathy's LLM Council methodology, dispatching decisions through five independent advisors with distinct thinking styles, followed by peer review and chairman synthesis.

## Core Concept

Rather than asking one AI for a single perspective, the council generates multiple angles simultaneously. The Contrarian hunts for fatal flaws. The First Principles Thinker reframes the problem entirely. The Expansionist chases upside. The Outsider provides naive fresh eyes. The Executor asks "what do we do Monday morning?"

These five create natural tensions: downside versus upside, rethinking versus doing, expert knowledge versus outsider clarity.

## Activation Triggers

**Mandatory:** "council this," "run the council," "war room this," "pressure-test this," "stress-test this," "debate this"

**Strong (with real tradeoffs):** "should I X or Y," "which option," "what would you do," "is this the right move"

Avoid triggering on factual lookups, simple yes/no questions, or casual "shoulds" without genuine stakes.

## Process Flow

1. **Frame the question** with workspace context enrichment (scan for CLAUDE.md, memory files, relevant data)
2. **Convene advisors in parallel** — each produces 150-300 word independent analysis
3. **Peer review in parallel** — each advisor evaluates all responses anonymously, identifying strongest analysis, blind spots, and missed considerations
4. **Chairman synthesis** — produces final verdict with agreement points, clashes, blind spots, clear recommendation, and one concrete first step
5. **Present verdict** in chat as scannable markdown
6. **Save transcript** only if significant

## Key Safeguards

All advisors spawn simultaneously to prevent sequential influence. Peer reviews work with anonymized responses (A-E labels randomized) to eliminate deference bias. The chairman can override majority opinion if reasoning warrants it.

<!--
ORIGIN NOTE (kept for provenance, per the par3-<source> convention):
  Source you obtained it from: https://github.com/aiwithremy/claude-skills-llm-council  (aiwithremy / Remy)
  Original author: Ole Lehmann, based on Andrej Karpathy's LLM Council methodology.
  This body was reproduced from the public SKILL.md. If the upstream skill updates,
  re-sync from the repo above.
-->
