#!/usr/bin/env bash
# Point opencode at this skill. Claude Code picks it up as a plugin on its own;
# opencode has no plugin system that can read that, so it gets symlinks into its
# own config instead:
#
#   plugins/code-comments.js  -> plugin.js, the always-on ruleset injection
#   skills/code-comments      -> the skill directory, so the skill and any
#                                commands added later are invokable
#
# Run with --uninstall to remove both links.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"

PLUGIN_SRC="$HERE/plugin.js"
PLUGIN_DEST="$CONFIG/plugins/code-comments.js"
# The whole directory, not just SKILL.md — AUDIT.md has to resolve beside it.
SKILL_SRC="$(dirname "$HERE")"
SKILL_DEST="$CONFIG/skills/code-comments"

link() {
  local src="$1" dest="$2"
  mkdir -p "$(dirname "$dest")"
  # Only ever replace our own link. Anything else there belongs to someone else.
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    echo "error: $dest exists and is not a symlink — move it and re-run" >&2
    exit 1
  fi
  ln -sfn "$src" "$dest"
  echo "linked    $dest -> $src"
}

unlink_() {
  local dest="$1"
  if [ -L "$dest" ]; then
    rm "$dest"
    echo "removed   $dest"
  else
    echo "nothing   no link at $dest"
  fi
}

if [ "${1:-}" = "--uninstall" ]; then
  unlink_ "$PLUGIN_DEST"
  unlink_ "$SKILL_DEST"
  exit 0
fi

link "$PLUGIN_SRC" "$PLUGIN_DEST"
link "$SKILL_SRC" "$SKILL_DEST"
echo
echo "restart opencode — plugins load at startup"
