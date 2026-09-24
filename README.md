# skills

Claude Code skills, vendored from [Classward/agent-skills](https://github.com/Classward/agent-skills). Each copy is verbatim, so re-extracting one stays clean.

| Skill | Vendored from | What it does |
|---|---|---|
| [`dry-prose`](skills/dry-prose) | `add-dry-prose-skill` | Writes short, plain prose for READMEs, docs, runbooks, and PR descriptions. Writes new text, or sweeps a draft you already have. Carries its own eval harness. |
| [`wtf`](skills/wtf) | `main` | Answers at whiteboard altitude: a drawing, then a short caption. Ships 3 commands, `/wtf`, `/wtf-html`, and `/wtf-brand`. |

`add-dry-prose-skill` has not merged, so `dry-prose` can change before it lands on `main`.

Every skill sets `disable-model-invocation: true`, so Claude never reaches for one on its own. Type the command to run it.

## Install

Clone first:

```bash
git clone git@github.com:tunztunztunz/skills.git
cd skills
```

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
