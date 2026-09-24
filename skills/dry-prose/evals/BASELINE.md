# Baseline

The skill scores **93.8/100** across 5 cases. Two cases lose points, and both losses are
vocabulary, not structure.

| Field | Value |
|---|---|
| Date | 2026-09-23 |
| Model | Claude Sonnet 5, one subagent per case |
| Ruleset | `SKILL.md`, `WORDS.md`, and `CHECK.md` at commit `8a5c0c3` |
| Prompt | `fixtures/prompt-template.md` |
| Answers | `baseline/`, one file per case |

## Scores

| Case | Score | What it lost points for |
|---|---|---|
| `procedure-install` | 84 | `previous`, `requirement` |
| `descriptive-api` | 85 | `supports`, `two` written as a word |
| `over-correction-guard` | 100 | |
| `em-dash-sweep` | 100 | |
| `shape-first` | 100 | |
| **Average** | **93.8** | |

## Read the score against two other numbers

| Run | Average | What it tells you |
|---|---|---|
| `cases/*/reference.md` | 100.0 | The harness agrees with a hand-written answer |
| `baseline/` | 93.8 | What the skill gets from a model |
| `cases/*/source.md` | 21.4 | What the drafts scored before the sweep |

The gap from 21.4 to 93.8 is the skill's effect. The gap from 93.8 to 100 is what the
ruleset did not reach.

## What the model did well

It moved 4 of the 5 drafts into tables or numbered steps without being told which form to
use, so Shape first carries. It restored the dropped articles and connectives in
`over-correction-guard`, which is the case built to catch a sweep that cuts too far. It kept
the en dash in the `2-8 seconds` range while removing every em dash around it.

## What it missed

Both misses are words with a plain replacement sitting in `WORDS.md`. `previous` and
`requirement` appeared in `procedure-install`, one of them inside a table header.
`descriptive-api` kept the fog word `supports` and spelled out `two`.

Neither miss is a structural failure, so the ruleset's weak point is the vocabulary pass and
not the shape pass. A ruleset edit aimed at 100 belongs in the word rules.

## Re-check these numbers

```sh
python3 evals/run_eval.py --outputs evals/baseline
```

The answers are committed, so the scores can be checked without a model. Re-run the model
only when the ruleset changes, and record a new baseline when it does.
