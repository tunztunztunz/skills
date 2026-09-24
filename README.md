# skills

Claude Code skills, one directory each. Both of these shape writing rather than code.

| Skill | What it does |
|---|---|
| [`dry-prose`](skills/dry-prose) | Writes short, plain prose for READMEs, docs, runbooks, and PR descriptions. Writes new text, or sweeps a draft you already have. |
| [`wtf`](skills/wtf) | Answers with an ASCII drawing and a short caption, held to 1 screen. With no arguments, it redraws the last reply. |

Both set `disable-model-invocation: true`, so Claude never reaches for them on its own. Type `/dry-prose` or `/wtf` to run one.

## Install

Symlink a skill into `~/.claude/skills/` to use it everywhere:

```bash
git clone git@github.com:tunztunztunz/skills.git
cd skills
ln -s "$PWD/skills/dry-prose" ~/.claude/skills/dry-prose
ln -s "$PWD/skills/wtf" ~/.claude/skills/wtf
```

To limit a skill to one project, symlink it into that project's `.claude/skills/` instead.
