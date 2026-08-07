#!/usr/bin/env bash
# Enforce the skills-marketplace naming conventions (see CONTRIBUTING.md).
# Exit non-zero on any violation so it can gate a commit or CI job.
set -euo pipefail

cd "$(dirname "$0")"

fail=0
err() { echo "FAIL: $*" >&2; fail=1; }

name_re='^[a-z][a-z0-9-]*$'   # lowercase, start with a letter, letters/digits/hyphens

# Track skill names globally to catch cross-plugin duplicates.
declare -A seen_skill

for plugin_dir in */; do
  plugin="${plugin_dir%/}"
  [ "$plugin" = ".claude-plugin" ] && continue
  [ -d "$plugin_dir/skills" ] || [ -f "$plugin_dir/.claude-plugin/plugin.json" ] || continue

  # Rule 3: general plugin-name shape.
  if [[ ! "$plugin" =~ $name_re ]]; then
    err "plugin '$plugin' is not lowercase-letter-first alphanumeric-hyphen"
  fi

  # Rule 1: any par3 plugin must be par3-<source> with a real suffix.
  if [[ "$plugin" == par3* && ! "$plugin" =~ ^par3-[a-z0-9]+$ ]]; then
    err "3rd-party plugin '$plugin' must be 'par3-<source>' (e.g. par3-pd)"
  fi

  # Rule 4: unique skill names.
  if [ -d "$plugin_dir/skills" ]; then
    for skill_dir in "$plugin_dir"skills/*/; do
      [ -d "$skill_dir" ] || continue
      skill="$(basename "$skill_dir")"
      if [[ ! "$skill" =~ $name_re ]]; then
        err "skill '$plugin/$skill' is not lowercase-letter-first alphanumeric-hyphen"
      fi
      if [ -n "${seen_skill[$skill]:-}" ]; then
        err "skill '$skill' is duplicated across plugins ('${seen_skill[$skill]}' and '$plugin')"
      else
        seen_skill[$skill]="$plugin"
      fi
      [ -f "$skill_dir/SKILL.md" ] || err "skill '$plugin/$skill' is missing SKILL.md"
    done
  fi
done

# Sanity: the marketplace manifest exists at the repo root (where Claude looks for it).
[ -f "../.claude-plugin/marketplace.json" ] || err "missing ../.claude-plugin/marketplace.json (must be at repo root)"

if [ "$fail" -eq 0 ]; then
  echo "OK: naming conventions pass"
fi
exit "$fail"
