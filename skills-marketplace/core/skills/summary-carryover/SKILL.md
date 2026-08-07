---
name: summary-carryover
description: Use this skill whenever the user types the command "/summary-carryover" (or close variants like "/summary carryover", "summary carryover", or "create a carryover doc"). Generates a structured Markdown handoff document that captures the entire current conversation — goals, decisions, current state, open threads, key files/links, and user preferences — and saves it as a downloadable .md file the user can re-ingest at the start of a new chat to continue work without losing context. Trigger on the command itself, even if no other context is given.
---

# Summary Carryover

This skill produces a single Markdown file that distills the current conversation into a handoff document for use in a new chat.

## When to trigger

Trigger when the user types `/summary-carryover` or an obvious variant. No other arguments are required. If the user adds a focus area after the command (e.g. `/summary-carryover focus on the API design decisions`), weight the summary accordingly but still cover all sections.

## What to do

1. **Scan the conversation** from the start. Identify:
   - The user's overall goal or the project being worked on
   - Concrete decisions that were made (and the reasoning, briefly)
   - Anything that is currently in-progress or unresolved
   - Files, links, or external references that came up
   - Stated user preferences (tone, format, constraints, tools)
   - Specific names, IDs, versions, or values that would be lost without writing them down
2. **Generate the file** using the structure below.
   - **In Claude.ai Chat:** save it to `/mnt/user-data/outputs/carryover-YYYY-MM-DD.md` (use today's actual date) with the `create_file` tool, then call `present_files` so the user can download it.
   - **In Claude Code:** those paths/tools don't exist. Instead write the file to `status/carryover-YYYY-MM-DD.md` in the repo and commit it (or hand it back with the file-send tool). The repo is the store — the committed file is what the user re-ingests later.
3. **In the chat reply**, give the user a 2–3 sentence summary of what was captured and the exact phrase they should paste at the top of the new chat to re-ingest the doc. Do not re-paste the full document content into the chat.

## File structure

The output file must follow this template. Omit any section that has no content rather than padding it.

```markdown
# Carryover Document — [Project/Topic Name]
**Generated:** [Date]
**Source chat:** [1-line description of what this conversation was about]

## How to use this document
Paste the following at the start of a new Claude chat, then attach this file:
> "Please read this carryover document as authoritative context for our continuing work. Confirm you've ingested it by summarizing the current state in one paragraph before we proceed."

---

## 1. Goal
[1–3 sentences. What is the user ultimately trying to accomplish?]

## 2. Current state
[Where things stand right now. What's done, what's in progress.]

## 3. Decisions made
[Bulleted list of concrete decisions, each with a brief "why" if it matters.]

## 4. Open threads
[Things that were raised but not resolved. Questions still pending.]

## 5. Key references
[Files, URLs, commands, IDs, version numbers, names — anything specific that should not be re-derived from memory.]

## 6. User preferences (for this project)
[Tone, format, tools, constraints the user has stated. Only include preferences specific to this work, not generic profile preferences.]

## 7. Suggested next step
[One concrete action to start the next chat with.]
```

## Rules

- **Be faithful, not generative.** Only include things that actually appeared in the conversation. If a section would require inventing content, omit it.
- **Be concise.** Each section should be as short as it can be while still being useful. Bullets over prose where it fits.
- **Preserve specifics.** Exact file paths, version numbers, command flags, error messages, and proper nouns matter more than narrative flow — these are what get lost otherwise.
- **No commentary in the chat reply** beyond the short summary and the re-ingestion phrase. The user wants the file, not a recap.

## Example chat reply after generating the file

> Carryover doc saved. It captures the auth refactor goal, the three architecture decisions we landed on, and the two open questions about token rotation. To resume in a new chat, attach the file and start with: *"Please read this carryover document as authoritative context for our continuing work. Confirm you've ingested it by summarizing the current state in one paragraph before we proceed."*
