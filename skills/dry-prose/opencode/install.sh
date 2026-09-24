#!/usr/bin/env bash
# Point opencode at this skill. Claude Code and Codex read the plugin manifests
# beside this directory; opencode reads neither, so it gets a symlink into its
# own skills directory instead.
#
# The link covers the whole skill directory, not just SKILL.md: SKILL.md links
# to WORDS.md and CHECK.md beside it, and opencode resolves those paths inside
# whatever it linked.
#
# Run with --uninstall to remove the link.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$(dirname "$HERE")"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"
DEST="$CONFIG/skills/dry-prose"

if [ "${1:-}" = "--uninstall" ]; then
  if [ -L "$DEST" ]; then
    rm "$DEST"
    echo "removed   $DEST"
  else
    echo "nothing   no link at $DEST"
  fi
  exit 0
fi

mkdir -p "$(dirname "$DEST")"
# Only ever replace our own link. Anything else there belongs to someone else.
if [ -e "$DEST" ] && [ ! -L "$DEST" ]; then
  echo "error: $DEST exists and is not a symlink — move it and re-run" >&2
  exit 1
fi

ln -sfn "$SKILL_SRC" "$DEST"
echo "linked    $DEST -> $SKILL_SRC"
echo
echo "restart opencode — skills load at startup"
echo "note: opencode has no equivalent of disable-model-invocation, so it may"
echo "      load these rules on its own rather than only on /dry-prose"
