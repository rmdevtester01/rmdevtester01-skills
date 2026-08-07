#!/usr/bin/env bash
# PreToolUse cost-gate — HARD RULE.
#
# Any tool call that incurs *additional* API / usage cost beyond the normal
# conversation must be cleared by the user before it runs. This hook is registered
# in .claude/settings.json against the cost-incurring tools (subagents, web
# search, web fetch) and returns an "ask" decision, which forces the harness to
# pause for the user's explicit approval. The model cannot bypass this — a
# skill description is only a hint, but a PreToolUse hook is enforced by the
# harness itself.
#
# Note: this covers the enumerable harness cost drivers. Cost-incurring *Bash*
# commands (e.g. `claude -p ...` self-calls, curls to paid APIs) can't be caught
# reliably by a matcher, so CLAUDE.md instructs the model to self-gate those and
# ask first as well.
set -euo pipefail

input="$(cat)"
tool="$(printf '%s' "$input" | jq -r '.tool_name // "unknown"')"

reason="HARD RULE (cost-gate): \"${tool}\" draws down the user's Claude Pro usage allowance (extra usage, not a dollar bill). The user must clear this before it runs — state the expected scope/usage and get explicit approval first. Do not proceed on your own."

jq -cn --arg r "$reason" '{
  hookSpecificOutput: {
    hookEventName: "PreToolUse",
    permissionDecision: "ask",
    permissionDecisionReason: $r
  }
}'
