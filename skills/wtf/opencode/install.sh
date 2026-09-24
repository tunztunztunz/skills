#!/usr/bin/env bash
# Point opencode at the three wtf skills. Claude Code and Codex read the plugin
# manifests beside this directory; opencode reads neither, so it gets symlinks
# into its own skills directory instead:
#
#   skills/wtf        -> the whiteboard answer, plus SHAPES.md beside it
#   skills/wtf-html   -> the explainer, plus TEMPLATE.html beside it
#   skills/wtf-brand  -> the branding script, which patches that template
#
# Each link covers the whole skill directory, because every one of them reads a
# file sitting next to its SKILL.md.
#
# Run with --uninstall to remove all three.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS="$(dirname "$HERE")/skills"
CONFIG="${XDG_CONFIG_HOME:-$HOME/.config}/opencode"

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

for skill in wtf wtf-html wtf-brand; do
  if [ "${1:-}" = "--uninstall" ]; then
    unlink_ "$CONFIG/skills/$skill"
  else
    link "$SKILLS/$skill" "$CONFIG/skills/$skill"
  fi
done

[ "${1:-}" = "--uninstall" ] || {
  echo
  echo "restart opencode — skills load at startup"
}
