# dry-prose

Writing rules for anything read while working: READMEs, API docs, guides, runbooks, procedures,
agent output. Short sentences, concrete nouns, second person, no em dashes in prose, and the
grammar left intact so a telegram never replaces a sentence. `SKILL.md` holds the rules.

## Where the rules come from

Most of them come from [ASD-STE100 Simplified Technical English](https://asd-ste100.org), the
writing standard the aerospace and defence industry uses for maintenance manuals. It began as
AECMA Simplified English, written so a mechanic reading in a second language cannot
misread a procedure.

That origin explains the rules that look arbitrary:

| Rule | What the standard says |
|---|---|
| 20 words for an instruction, 25 for an explanation | Its procedural and descriptive sentence limits |
| `WORDS.md` | Its approved-word dictionary, one meaning per word |
| Keep the articles and connectives | Its rule against telegram English |
| 3 nouns to a cluster | Its noun-cluster limit |
| Condition before the action, caveat above the command | Its safety-instruction order |
| No `-ing` word doing a noun's job | Its ban on gerunds |

dry-prose departs from it in three places. The em dash ban is house style, not the standard.
Shape first, which sorts facts into tables and steps before any sentence is written, is a
whole-document rule where the standard works sentence by sentence. The blind reader check has
no equivalent in a standard written for humans.

## Install

**Claude Code.**

```sh
claude plugin marketplace add Classward/agent-skills
claude plugin install dry-prose@classward
```

**Codex.**

```sh
codex plugin marketplace add Classward/agent-skills --ref main
codex plugin add dry-prose@classward
```

**opencode.**

```sh
git clone git@github.com:Classward/agent-skills.git ~/.local/share/classward-agent-skills
~/.local/share/classward-agent-skills/bin/install-opencode.sh
```

That symlinks the skill directory into `~/.config/opencode/skills/dry-prose`. Run
`skills/dry-prose/opencode/install.sh` directly to link this skill alone.

Restart the host afterwards; skills are discovered at session start. Confirm the Claude Code side
with `claude plugin list`.

opencode has no equivalent of `disable-model-invocation`, so it may load these rules on its own
rather than only when you type `/dry-prose`.

## Invoking it

The skill sets `disable-model-invocation: true`, so Claude never picks it up on its own. Run
`/dry-prose` and say what to write or which file to sweep.

## What each file holds

| File | What it holds | When it is read |
|---|---|---|
| `SKILL.md` | The rules, in the order they apply | Every run |
| `WORDS.md` | A formal word and its plain replacement, plus the fog table | When a word feels formal |
| `CHECK.md` | The countable checks, grouped by section | Once the text is finished |
| `evals/` | Cases and a scorer for the countable rules | Never, unless you change the rules |

`WORDS.md` and `CHECK.md` are read on demand, so a run that needs neither pays no context for
them.

## The two modes

| Mode | What it does |
|---|---|
| Write | Sorts the facts into forms, then drafts against the rules |
| Sweep | Revises a draft in place, inventorying every em dash before changing any |

A write sorts every fact into a form before the first sentence: numbered steps, a table, a heading
per case, or a single sentence. A sweep leaves the document's existing forms standing. If a
paragraph is carrying a table's worth of facts, the skill names it in the report and leaves the
call to you.

Both modes end the same way: every rule applied, `CHECK.md` passed, the blind reader check passed,
and the word count reported before and after.

## The mechanical pass

`CHECK.md` runs over the finished text before the blind reader sees it. Every line in it is
countable: a word count, a search for a string, a scan for one part of speech. It catches what a
grep catches, which is why it runs first and why the blind reader still runs after it.

## The blind reader check

The skill dispatches a subagent on Sonnet before it calls a document done. The subagent gets the
text and nothing else, then answers two questions: what the document is about, and what it tells
you to do. A gap between that answer and the intent is a prose failure, so the skill fixes the
prose and dispatches again. Each revision costs one subagent round trip.

When two rounds of fixes leave the same gap, the sentences are not the problem. A fact the reader
keeps missing is usually a fact buried in a paragraph that should be a table or a numbered step.

## Changing the rules

`evals/` scores the countable rules, so a ruleset edit can be measured instead of argued. The
recorded run sits in [`evals/BASELINE.md`](evals/README.md): 93.8 out of 100 across 5 cases,
against 21.4 for the same drafts before the sweep.

Run it after any edit to `SKILL.md`, `WORDS.md`, or `CHECK.md`:

```sh
python3 evals/run_eval.py --outputs evals/baseline
```

[`evals/README.md`](evals/README.md) covers the scoring weights and how to add a case. The
score reaches the countable rules only, so read the answers before you accept a change.

## Scope

Prose only. Quoted text, code samples, command output, and passages you wrote and handed over
stay untouched unless you ask otherwise. The skill never flattens tables, headings, code blocks,
parameter lists, or numbered steps.

## Uninstall

```sh
claude plugin uninstall dry-prose@classward
```
