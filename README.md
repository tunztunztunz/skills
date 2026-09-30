# skills

My Claude Code skills, installable from one marketplace. Some live in this repo; the ones that ship a Go binary live in their own repos and are listed here.

| Skill | Lives in | What it does |
|---|---|---|
| [`code-comments`](skills/code-comments) | here | Holds a comment to one job: state a constraint the code cannot carry. Hooks inject the rules at session start, so they apply without being invoked. Carries its own eval harness. |
| [`dry-prose`](skills/dry-prose) | here | Writes short, plain prose for READMEs, docs, runbooks, and PR descriptions. Writes new text, or sweeps a draft you already have. Carries its own eval harness. |
| [`wtf`](skills/wtf) | here | Answers at whiteboard altitude: a drawing, then a short caption. Ships 3 commands, `/wtf`, `/wtf-html`, and `/wtf-brand`. |
| [`grilled-cheese`](https://github.com/tunztunztunz/grilled-cheese) | its own repo | Runs a grilling session in a browser: clickable options, per-question threads, a live decision log, and vim keys. |
| [`interrupt`](https://github.com/tunztunztunz/interrupt) | its own repo | Draws a lateral-thinking card above the prompt and reads the problem through it. |

`code-comments`, `dry-prose`, and `wtf` are copied verbatim from [Classward/agent-skills](https://github.com/Classward/agent-skills), so each skill's own README describes that repo's paths.

## Install

Add the marketplace, then install the plugins you want:

```bash
claude plugin marketplace add tunztunztunz/skills
claude plugin install code-comments@tunztunztunz
claude plugin install dry-prose@tunztunztunz
claude plugin install wtf@tunztunztunz
claude plugin install grilled-cheese@tunztunztunz
claude plugin install interrupt@tunztunztunz
```

Restart Claude Code afterwards, because it loads plugins at startup.

To work on the skills in a clone, add the clone instead: `claude plugin marketplace add ~/path/to/skills`. The skills in this repo then install from your working tree. `grilled-cheese` and `interrupt` still install from GitHub, so they pick up only what's pushed.

After editing a skill, refresh the installed copy and restart:

```bash
claude plugin marketplace update tunztunztunz
claude plugin update <name>@tunztunztunz
```

If an update misses an edit, raise `version` in that plugin's `.claude-plugin/plugin.json`.

### Skills with a binary

`grilled-cheese` and `interrupt` drive a Go binary on `PATH`, which the plugin does not install:

```bash
go install github.com/tunztunztunz/grilled-cheese@latest
go install github.com/tunztunztunz/interrupt/cmd/interrupt@latest
```

The `interrupt` plugin needs `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS=1`.

### Other requirements

`/wtf-html` and `/wtf-brand` need a browser, `cwebp`, `sips`, and Pillow, plus `rsvg-convert` for SVG logos. [`skills/wtf/README.md`](skills/wtf/README.md) lists them.

## Update a copied skill

Refresh it from a clone of Classward/agent-skills:

```bash
git rm -r skills/dry-prose
git -C <path-to-agent-skills> archive origin/add-dry-prose-skill skills/dry-prose | tar -x -C .
```

The refs: `code-comments` from the local branch `code-comments-constraint-test` (drop the `origin/` prefix), `dry-prose` from `add-dry-prose-skill`, and `wtf` from `main`.
