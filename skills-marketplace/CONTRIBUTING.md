# Conventions

## 1. Third-party skills must be `par3-<source>`

Every plugin that wraps a skill you did **not** author yourself lives in a plugin named:

```
par3-<source>
```

- `par3` marks it as the 3rd-party tier.
- `<source>` is a short lowercase tag for where you got it (the creator/handle), so the origin is
  encoded in the namespace and shows up in every skill name (`par3-<source>:<skill>`).

Current sources:

| Source            | Tag    | Plugin      |
| ----------------- | ------ | ----------- |
| Patrick Dang      | `pd`   | `par3-pd`   |
| aiwithremy (Remy) | `remy` | `par3-remy` |

Add a new creator by creating a new `par3-<them>/` plugin — never mix two sources in one plugin.
Record the true original author in that plugin's `README.md` even if you got it second-hand
(e.g. LLM Council is sourced from aiwithremy but authored by Ole Lehmann).

## 2. Your own categories use plain names

`token-tools`, `research`, `core`, and future categories (e.g. `consulting`, `personal-research`)
are named plainly, no `par3-` prefix.

## 3. General plugin-name rules

Lowercase letters, digits, and hyphens only. Prefer starting with a letter.

## 4. Skill names are unique per plugin

A skill folder name must be unique within its plugin's `skills/` directory. Don't duplicate the same
skill across two plugins (e.g. `token-tracker` lives in `token-tools` only — one home per skill).

## Enforcement

Run `./validate-naming.sh` before committing. It checks rules 1–4 and the marketplace manifest.
