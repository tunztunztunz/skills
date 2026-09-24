# code-comments

A code comment states a constraint the code cannot carry: change the code so it contradicts that
constraint, and the code is wrong. `SKILL.md` holds the full rules, `AUDIT.md` holds the sweep
procedure for auditing comments across an existing codebase.

This directory is both a skill and a Claude Code plugin. The plugin part registers three hooks
that put the rules in context automatically, so they apply to comments the agent writes without
anyone invoking anything.

## Install

**Claude Code.** Delivers the skill, the `/code-comments` command, and the hooks together. The
repo [`README`](../../README.md) covers adding the marketplace, updating, and uninstalling.

```sh
claude plugin install code-comments@classward
```

**opencode.** Its own step, because opencode cannot read Claude Code plugins. The repo `README`
covers the clone-and-run bootstrap; `bin/install-opencode.sh` is the normal entry point and
re-running it updates. To drive just this skill from an existing clone:

```sh
skills/code-comments/opencode/install.sh             # link it
skills/code-comments/opencode/install.sh --uninstall # remove the links
```

Restart Claude Code and opencode afterward. Both read this at startup, and neither route writes to
`~/.claude/settings.json`.

## What the hooks do

`hooks/hooks.json` registers three entries, all running `hooks/code-comments-context.sh`:

| Event | What it injects | Cost |
|---|---|---|
| `SessionStart` | The full ruleset, once per session | ~600 tokens per session |
| `SubagentStart` | The full ruleset, into each spawned subagent | ~600 tokens per subagent |
| `UserPromptSubmit` | A one-line anchor that survives context compaction | ~20 tokens per prompt |

The script reads `SKILL.md` at runtime rather than embedding a copy, so the skill file stays the
single source of truth. There is no build step — but the installed copy under
`~/.claude/plugins/cache/` is overwritten on the next `claude plugin update`, so edit the rules in
this repo and push rather than in place.

## What opencode gets

opencode has no session-start event, so `opencode/plugin.js` appends the ruleset to the system
prompt before each request instead. Same rules, delivered per request rather than per session.

`opencode/install.sh` makes two symlinks, and re-running it is safe — it refuses to overwrite
anything that is not its own link.

| Link | Gets you |
|---|---|
| `~/.config/opencode/plugins/code-comments.js` | The always-on injection |
| `~/.config/opencode/skills/code-comments` | The invokable skill, and any commands added later |

The second links the whole skill directory rather than `SKILL.md` alone, because the audit sweep
reads `AUDIT.md` beside it.

## Editing the rules

`SKILL.md` is the single source of truth. The hook script, the opencode plugin, and the skill
itself all read it, so a change to that file reaches every path on the next restart.

Two lines are written by hand rather than read from the file: the one-line anchor in
`hooks/code-comments-context.sh`, and its counterpart header in `opencode/plugin.js`. Change the
rules in a way that makes those wrong, and they need updating too.

## Evals

`evals/` has focused prompts for the decisions the skill makes: omit decoration, name the code,
state an external contract, keep interface comments at their altitude, protect generated sources,
and complete an audit.
They are a regression check for observable behavior, not a claim that a script can judge whether
a comment states a real constraint.

```sh
mkdir -p /tmp/code-comments-evals
for case in skills/code-comments/evals/cases/*/; do
  cp "$case/reference.md" "/tmp/code-comments-evals/$(basename "$case").md"
done
python3 skills/code-comments/evals/run_eval.py --outputs /tmp/code-comments-evals
```

To evaluate a model, give it each `prompt.md`, write its response as `<case-id>.md` in an output
directory, and run the same command. The verifier returns a failure status for missing outputs or
the explicit case constraints. Read the output itself before changing the skill.

## Known limits

- The `SubagentStart` event is present in Claude Code 2.1.220, which is where it was verified. A
  build without it ignores that entry; the other two still work.
- Hooks load once at session start. Restart Claude Code after installing, and after any change to
  `hooks/hooks.json`.
- The opencode route is a symlink into a clone, not a copy. Move or delete the clone and opencode
  silently stops injecting the rules.
- Invoking the skill in opencode puts the ruleset in context a second time, since the plugin has
  already injected it. Harmless, and the reason to invoke it there is the audit sweep.
