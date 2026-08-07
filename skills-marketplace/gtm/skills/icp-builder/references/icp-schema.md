# ICP Artifact Schema (canonical)

This is the single source of truth for what an ICP document looks like across the
skill library. `gtm:icp-builder` produces it; `par3-pd:offer-validator` emits the same
artifact as a side output of validation; `par3-pd:listbuilder` consumes it in place of
its intake interview. Because plugins install independently, skills do **not** read this
file at runtime — they recognize the artifact by its filename and header convention below
(same pattern as `carryover-*.md`).

## File convention

- **Filename:** `icp-<offer-or-segment-slug>-<YYYY-MM-DD>.md`
- **First line:** `# ICP — <Offer / Segment Name>`
- **Storage:** Claude.ai Chat → `/mnt/user-data/outputs/`; Claude Code → `status/` in the repo (commit it), or hand back with the file-send tool.

## Required sections

Omit a section only with a stated reason (e.g. "7. Watering holes — not researched, out of scope for this engagement"). Never pad an empty section.

| # | Section | Contents |
|---|---------|----------|
| 1 | Segment definition | One paragraph: exactly who this profile covers, and the offer/context it was built for |
| 2 | Firmographics | Company size / revenue / stage, verticals, geography |
| 3 | Buyer roles | Economic buyer, champion, day-to-day users — specific titles, not categories |
| 4 | Pains | Top 3–5 problems **in the buyer's own language**, each with a source |
| 5 | Current alternatives | What they do today instead — competitors, workarounds, and "do nothing" |
| 6 | Budget reality | What this segment actually spends on this class of solution |
| 7 | Watering holes | Where they congregate: communities, events, media, platforms |
| 8 | Buying triggers | Events/moments that start a search for this solution |
| 9 | Objections | Likely resistance points and the evidence that answers each |
| 10 | Disqualifiers | Who *looks like* the ICP but isn't — negative filters (listbuilder uses these) |
| 11 | Evidence log | Sources behind the claims above; anything unsourced is marked `[Hypothesis]` inline where it appears |

## Lineage

Sections 1–8 descend from `par3-pd:offer-validator` Stage 2 ("ICP Deep Dive"). Sections
9–11 add the positioning lens (objections), the list-building lens (disqualifiers), and
the `core:level-reframing` evidence discipline (evidence log, `[Hypothesis]` labels).
