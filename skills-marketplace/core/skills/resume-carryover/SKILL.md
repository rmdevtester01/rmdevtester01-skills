---
name: resume-carryover
description: Use this skill whenever the user types the command "/resume-carryover" (or close variants like "/resume carryover", "resume carryover", or "ingest carryover doc"), or when the user attaches a file named like "carryover-*.md" at the start of a chat. Reads the attached carryover document as authoritative project context, confirms ingestion by summarizing the current state in one paragraph, and is ready to continue the prior work without re-deriving context. Pairs with the summary-carryover skill which generates the document.
---

# Resume Carryover

This skill ingests a carryover document produced by the `summary-carryover` skill and re-establishes context at the start of a new chat.

## When to trigger

Trigger when any of the following happen:
- The user types `/resume-carryover` or an obvious variant
- The user attaches a file matching `carryover-*.md` at the start of a chat
- The user pastes content that begins with `# Carryover Document —`

## What to do

1. **Locate the document.** Check for an attached file in the conversation. In **Claude Code** the doc is usually a committed `status/carryover-*.md` file rather than an attachment — look there and read the most recent one from the repo. If the user typed the command but nothing is attached and no `status/carryover-*.md` exists, ask once: *"Please attach the carryover .md file or paste its contents."* Do not proceed without the document.
2. **Read it as authoritative.** Treat the contents as a faithful record of prior work. Do not second-guess decisions recorded in section 3 or invent context that isn't in the file.
3. **Confirm ingestion in one paragraph.** Reply with a single paragraph (4–6 sentences) that covers:
   - The project/goal (from section 1)
   - Where things currently stand (from section 2)
   - The most important 1–2 decisions or constraints to keep in mind (from section 3 or 6)
   - The open thread or next step that's most likely to be the user's immediate focus (from section 4 or 7)
   Do not bullet-list the whole document back. The point is to prove the context landed, not to recite it.
4. **End the confirmation by handing the turn back.** Close with a short prompt like *"Ready to continue — what would you like to tackle first?"* or, if section 7 has a clear next step, propose starting there.

## Rules

- **No re-derivation.** If something is in the document, accept it. Don't ask the user to re-explain decisions that are already recorded.
- **Surface conflicts honestly.** If something the user says in the new chat contradicts the carryover doc, flag it briefly rather than silently overriding either source. Example: *"The doc lists Postgres as the chosen DB, but you just mentioned MongoDB — should I update the assumption?"*
- **Don't summarize sections that are empty.** The original skill omits empty sections; treat their absence as "nothing to report there," not as a gap to fill.
- **Keep the confirmation tight.** One paragraph. The user wants to start working, not read a recap.

## Example confirmation

> Got it — picking up the auth refactor for the internal billing service. Current state: the token-rotation module is drafted but not yet wired into the middleware, and the integration tests are stubbed out. Two constraints to keep in mind from our earlier work: we committed to JWT over session cookies for cross-service calls, and we're keeping the refresh window at 15 minutes. The open thread was whether to handle revocation via a denylist or short-lived tokens only. Ready to continue — want to start with the revocation question, or push on wiring up the middleware?
