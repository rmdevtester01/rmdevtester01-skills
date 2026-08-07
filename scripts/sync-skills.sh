#!/usr/bin/env bash
# Re-sync the vendored skills in .claude/skills/ from the upstream marketplace,
# rmdevtester01/rmdevtester01-skills, which remains the single source of truth.
#
# The skills are mirrored into this repo (see CLAUDE.md "Skills are vendored") so
# cloud sessions load them from the clone with no marketplace/token/network. When
# a skill changes upstream, run this to refresh the mirror, then commit the diff.
#
# Usage:
#   scripts/sync-skills.sh /path/to/rmdevtester01-skills      # an existing clone
# or fetch a fresh copy first:
#   git clone --depth 1 https://github.com/rmdevtester01/rmdevtester01-skills /tmp/skills
#   scripts/sync-skills.sh /tmp/skills
set -euo pipefail

SRC="${1:?usage: sync-skills.sh <path-to-rmdevtester01-skills-clone>}"
MP="$SRC/skills-marketplace"
DEST="$(cd "$(dirname "$0")/.." && pwd)/.claude/skills"

[ -d "$MP" ] || { echo "error: no skills-marketplace/ under $SRC" >&2; exit 1; }

mkdir -p "$DEST"
for d in "$MP"/*/skills/*/; do
  [ -d "$d" ] || continue
  name="$(basename "$d")"
  rm -rf "${DEST:?}/$name"
  cp -r "$d" "$DEST/$name"
done

echo "Synced $(find "$DEST" -maxdepth 1 -mindepth 1 -type d | wc -l | tr -d ' ') skills into $DEST"
echo "Upstream commit: $(git -C "$SRC" rev-parse HEAD 2>/dev/null || echo unknown)"
echo "Next: review the diff and commit  ->  git add .claude/skills && git commit"
