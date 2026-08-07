# Updating Skills — Workflow

**The one rule: this repo is the source of truth.** Make every change here, push, then sync
down into Claude. Don't edit skills in the Customize UI anymore, or the repo and your account
will drift.

## Where things live

```
<repo root>/
├── .claude-plugin/marketplace.json            # lists every plugin (MUST be at repo root)
└── skills-marketplace/
    ├── validate-naming.sh                     # run before every commit
    ├── <plugin>/.claude-plugin/plugin.json    # plugin manifest (name + version)
    ├── <plugin>/skills/<skill>/SKILL.md       # a skill
    ├── <plugin>/skills/<skill>/scripts/       # optional supporting scripts
    └── core/skills/skills-index/SKILL.md      # the map — keep it current
```

> **Why the root manifest?** Claude resolves a marketplace by looking for
> `.claude-plugin/marketplace.json` at the **repo root**. The plugins live under
> `skills-marketplace/`, and each manifest entry's `source` points to `./skills-marketplace/<plugin>`.

## Two steps that apply to EVERY change

1. **Validate:** `./skills-marketplace/validate-naming.sh` → must print `OK`. Catches bad
   names, a `par3-*` plugin missing its `<source>` suffix, duplicate skill names across
   plugins, and missing `SKILL.md`.
2. **Bump the version** in the affected `plugin.json` (e.g. `"0.1.0"` → `"0.1.1"`). ⚠️ This is
   the step people forget. Versions are explicit, so Claude only pulls an update when the
   number changes. (Alternative: delete the `version` field and every commit auto-counts as a
   new version — simpler but noisier. Recommended: keep explicit versions and bump them.)

---

## Task A — Edit an existing skill (most common)

1. Edit `skills-marketplace/<plugin>/skills/<skill>/SKILL.md` — the body and/or the
   `description` (the `description` is what makes the skill trigger, so keep it tight).
2. Bump that plugin's `plugin.json` version.
3. Validate.
4. Commit + push on a branch, then open a PR and merge (see **Git** below).
5. Sync into Claude: in the `/plugin` manager, refresh the marketplace, then update the plugin.

## Task B — Add a new skill to an existing category

1. Create `skills-marketplace/<plugin>/skills/<new-skill>/SKILL.md` (add a `scripts/` folder
   only if it needs one).
2. Frontmatter: `name:` must match the folder name; write a tight `description:`.
3. Bump that plugin's `plugin.json` version.
4. Add a row to `core/skills/skills-index/SKILL.md` under the right category, and bump `core`'s
   version too.
5. Validate → commit + push → sync.

## Task C — Add a whole new category (new plugin)

For example a `consulting` bucket, or `par3-<newsource>` for a new third-party creator.

1. Scaffold:
   ```
   skills-marketplace/<plugin>/.claude-plugin/plugin.json
   skills-marketplace/<plugin>/skills/<skill>/SKILL.md
   ```
   Third-party plugins **must** be named `par3-<source>` — the validator enforces the suffix.
2. Register it in the root `.claude-plugin/marketplace.json`: add an entry to the `plugins`
   array with `name`, `source: "./skills-marketplace/<plugin>"`, and a description.
3. Add its rows to `skills-index` (a new category table).
4. Validate → commit + push.
5. Sync: in `/plugin`, refresh the marketplace, then **install** the new plugin (install, not
   update, since it's new).

---

## Naming rules (enforced by `validate-naming.sh`)

- Third-party skills → plugin named `par3-<source>` (`par3` = 3rd-party tier; `<source>` = where
  it came from, e.g. `pd` = Patrick Dang, `remy` = aiwithremy). Origin is encoded in the name.
- Your own categories → plain names (`token-tools`, `research`, `core`, `consulting`, …).
- Plugin/skill names: lowercase, start with a letter, letters/digits/hyphens only.
- Skill names must be unique across all plugins (don't duplicate one skill in two plugins).
- Record a third-party skill's true author in that plugin's `README.md`, even if you got it
  second-hand (e.g. `llm-council` is sourced from aiwithremy but authored by Ole Lehmann).

## Fork-graduation rule (when a par3 skill stops being third-party)

The `par3-<source>` namespace promises provenance: the skill's *method* is still the
original author's. Two kinds of edits keep that promise and stay in `par3`:

- **Trigger fencing** — description edits that change when the skill fires or point to
  sibling skills ("NOT for X, use Y"), without touching how it works.
- **Surface portability** — output paths, tool-name fixes (Chat vs Code), and similar
  plumbing.

Anything beyond that — rewriting the persona/register, changing stages or scoring, adding
or removing steps — is a **fork**. A fork graduates to an own-category plugin (e.g. `gtm`,
`career`) in the same PR that makes the edit:

1. Move the skill folder to the destination plugin; keep or rename the skill deliberately
   (renames change the slash command — check skills-index rename-safety notes).
2. Keep provenance in an `ORIGIN NOTE` comment in the SKILL.md body (the pattern
   `llm-council` uses) and credit the original author in the destination plugin's README.
3. Update skills-index, bump both plugins' versions, validate, and note the graduation in
   the PR description.

When unsure whether an edit crosses the line, treat it as a fork — a provenance claim that
has drifted is worse than an extra move.

## Git

`main` is the default branch — don't commit straight to it. Each change is:

```
branch → edit → ./skills-marketplace/validate-naming.sh → commit → push → PR → merge → sync
```

**Easiest path:** tell Claude Code what you want ("update boer's revenue rubric", "add a
`consulting` plugin with a `discovery-call` skill") and it runs the whole loop for you — branch,
edit, version bump, validate, and open the PR.

## Test before you ship (optional)

Load a single plugin for one session without touching your live setup:

```
claude --plugin-dir ./skills-marketplace/<plugin>
```

## First-time install (reference)

```
/plugin marketplace add rmdevtester01/claude-status
/plugin install par3-pd
/plugin install par3-remy
/plugin install token-tools
/plugin install research
/plugin install core
```

Then delete the old standalone copies in Customize → Skills to avoid duplicates.
