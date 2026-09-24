#!/usr/bin/env bash
# Puts the code-comments rules in front of the agent without anyone invoking the
# skill: `session` and `subagent` emit the full ruleset, `prompt` emits a one-line
# anchor that survives context compaction.
#
# Reads SKILL.md at runtime, so the skill file stays the single source of truth.
set -u

skill="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/SKILL.md"
[ -f "$skill" ] || exit 0

case "${1:-session}" in
  session|subagent)
    echo "CODE-COMMENT RULES ACTIVE — apply when writing or editing comments in source files."
    # Strip YAML frontmatter; the body is the ruleset.
    awk 'NR==1 && /^---$/ {f=1; next} f && /^---$/ {f=0; next} !f' "$skill"
    ;;
  prompt)
    echo "CODE-COMMENT RULES ACTIVE — comments state constraints code cannot carry; run the deletion test first. Source files only."
    ;;
esac
