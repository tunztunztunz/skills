# skills

Claude Code skills. `dry-prose` is written here. `wtf` is a verbatim copy of a plugin maintained in another repo.

| Skill | Source | What it does |
|---|---|---|
| [`dry-prose`](skills/dry-prose) | here | Writes short, plain prose for READMEs, docs, runbooks, and PR descriptions. Writes new text, or sweeps a draft you already have. |
| [`wtf`](skills/wtf) | [Classward/agent-skills](https://github.com/Classward/agent-skills) | Answers at whiteboard altitude: a drawing, then a short caption. Ships 3 commands, `/wtf`, `/wtf-html`, and `/wtf-brand`. |

Every skill here sets `disable-model-invocation: true`, so Claude never reaches for one on its own. Type the command to run it.

## Install dry-prose

Symlink it into `~/.claude/skills/` to use it everywhere:

```bash
git clone git@github.com:tunztunztunz/skills.git
cd skills
ln -s "$PWD/skills/dry-prose" ~/.claude/skills/dry-prose
```

To limit it to one project, symlink it into that project's `.claude/skills/` instead.

## Install wtf

Install it from the upstream marketplace rather than from this repo:

```sh
claude plugin install wtf@classward
```

[`skills/wtf/README.md`](skills/wtf/README.md) covers Codex, opencode, and what `/wtf-html` and `/wtf-brand` need installed. That file is upstream's, so its links and paths describe the upstream repo.

## Update the vendored wtf

The copy here matches `origin/main` of `Classward/agent-skills`. Refresh it from a clone of that repo:

```bash
git rm -r skills/wtf
git -C <path-to-agent-skills> archive origin/main skills/wtf | tar -x -C .
```
