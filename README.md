# Agent Skills Marketplace

A working library of **Claude Code agent skills**, packaged as namespaced plugins, with
harness-enforced policy hooks and a vendoring pipeline that mirrors skills into the
projects that consume them.

These are not prompt snippets. Each skill is a packaged instruction set with its own
trigger surface, and several ship executable assets (Python generators, PDF templates)
that the agent runs as part of the workflow.

---

## Why it is built this way

**Skills are packaged into plugins, and the plugin name is the namespace.** A skill is
invoked as `plugin:skill` (`gtm:icp-builder`, `token-tools:token-tracker`). Grouping by
plugin means a whole category can be installed, versioned, or renamed as a unit, and the
origin of a third-party skill stays visible in its own name (`par3-<source>`).

**Policy is enforced by the harness, not requested of the model.** A skill description is
a hint the model can talk itself out of. A `PreToolUse` hook is not. `hooks/cost-gate.sh`
intercepts every cost-incurring tool call (subagents, web search, web fetch) and returns
an `ask` decision, which forces the harness to pause for explicit human approval before
the call runs. The model cannot route around it.

```bash
# hooks/cost-gate.sh returns this to the harness:
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask", ...}}
```

Wiring lives in `settings.example.json`. The honest limit is documented in the hook
itself: matchers catch the enumerable tools, but cost-incurring *Bash* (a `claude -p`
self-call, a curl to a paid API) cannot be matched reliably, so that case is handled by a
written self-gate instruction rather than pretending the hook covers it.

**Skills are vendored into consuming repos, not installed from a marketplace.**
`scripts/sync-skills.sh` copies `skills-marketplace/*/skills/*/` into a target project's
`.claude/skills/`. A cloud session then loads them natively from the clone with no
marketplace, token, or network dependency at startup. This repo stays the single source of
truth; the vendored copy is a mirror, re-synced and committed when a skill changes
upstream.

```bash
git clone --depth 1 <this-repo> /tmp/skills
scripts/sync-skills.sh /tmp/skills      # run from the consuming project
```

---

## What is here

| Plugin | Skill | What it does |
|---|---|---|
| `research` | `boer` | Evidence-cited business-opportunity research; emits `.md` + `.pdf` |
| `gtm` | `icp-builder` | Ideal Customer Profile research producing a reusable `icp-*.md` artifact |
| `par3-pd` | `offer-validator` | Scores a specific offer 1-100; also emits the same ICP artifact |
| `par3-pd` | `listbuilder` | Scored outbound prospect list; consumes an `icp-*.md`; `scripts/generate_list.py` |
| `par3-remy` | `llm-council` | Runs a decision through five advisor lenses plus a chairman synthesis |
| `career` | `interview-prep` | Interviewer research, live mock, PDF prep pack; `assets/pdf_template.py` |
| `core` | `level-reframing` | Calibrated honesty; audits overstated claims and corrects framing |
| `core` | `summary-carryover` | Writes a structured handoff doc to resume work in a fresh session |
| `core` | `resume-carryover` | Ingests that handoff as authoritative context |
| `token-tools` | `token-tracker` | Rolling usage read against plan meters |
| `token-tools` | `token-efficiency` | In-flight output compression during generation |
| `token-tools` | `token-analysis-for-artifacts` | Pre-flight cost estimate before building a file |

**Three skills wire together by artifact convention.** `icp-builder` is the canonical
producer of `icp-*.md` (schema in its `references/icp-schema.md`); `offer-validator` emits
the same artifact as a side output; `listbuilder` consumes it in place of its intake
interview. The handoff is by filename and header convention rather than a runtime file
read, which keeps the skills independently usable but means renaming any of the three
requires updating the cross-references in all three bodies.

**`summary-carryover` and `resume-carryover` are a pair** (one writes the handoff, one
reads it). Renaming one without the other breaks the loop.

---

## Repo layout

```
skills-marketplace/<plugin>/skills/<skill>/SKILL.md   # the skill itself
                                        /scripts/     # executable assets, where used
                                        /references/  # schemas the skill loads on demand
hooks/cost-gate.sh                                    # PreToolUse policy enforcement
settings.example.json                                 # hook wiring
scripts/sync-skills.sh                                # vendoring pipeline
```

---

## Scope note

This is a **curated public subset** of a larger private library. Skills that carry
personal data are kept private and are not published here.
