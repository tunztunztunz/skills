# skills

Claude Code skills, vendored from [Classward/agent-skills](https://github.com/Classward/agent-skills). Each copy is verbatim, so re-extracting one stays clean.

| Skill | Vendored from | What it does |
|---|---|---|
| [`code-comments`](skills/code-comments) | `code-comments-constraint-test` | Holds a comment to one job: state a constraint the code cannot carry. Hooks inject the rules at session start, so they apply without being invoked. Carries its own eval harness. |
| [`dry-prose`](skills/dry-prose) | `add-dry-prose-skill` | Writes short, plain prose for READMEs, docs, runbooks, and PR descriptions. Writes new text, or sweeps a draft you already have. Carries its own eval harness. |
| [`wtf`](skills/wtf) | `main` | Answers at whiteboard altitude: a drawing, then a short caption. Ships 3 commands, `/wtf`, `/wtf-html`, and `/wtf-brand`. |

`add-dry-prose-skill` and `code-comments-constraint-test` have not merged, so those two can change before they land on `main`.

Every skill sets `disable-model-invocation: true`, so Claude never reaches for one on its own. Type the command to run it.

## Install

Clone first:

```bash
git clone git@github.com:tunztunztunz/skills.git
cd skills
```

`code-comments` needs the plugin route, not a symlink. Its hooks resolve `${CLAUDE_PLUGIN_ROOT}`, which only a plugin install sets, so a symlinked copy gives you the skill without the session-start injection. [`skills/code-comments/README.md`](skills/code-comments/README.md) covers it.

`dry-prose` installs as a single symlink:

```bash
ln -s "$PWD/skills/dry-prose" ~/.claude/skills/dry-prose
```

`wtf` holds 3 skills, so symlink each:

```bash
for s in wtf wtf-brand wtf-html; do
  ln -s "$PWD/skills/wtf/skills/$s" ~/.claude/skills/"$s"
done
```

Restart Claude Code afterwards, because it finds skills at startup.

`/wtf-html` and `/wtf-brand` need a browser, `cwebp`, `sips`, and Pillow, plus `rsvg-convert` for SVG logos. [`skills/wtf/README.md`](skills/wtf/README.md) lists them and covers the marketplace route for Claude Code, Codex, and opencode. Each skill's README is upstream's file, so its links and paths describe the upstream repo.

## Update a vendored skill

Refresh it from a clone of the upstream repo, using the ref in the table:

```bash
git rm -r skills/dry-prose
git -C <path-to-agent-skills> archive origin/add-dry-prose-skill skills/dry-prose | tar -x -C .
```
