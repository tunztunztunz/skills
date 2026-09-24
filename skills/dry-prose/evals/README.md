# Evals for dry-prose

These cases score the mechanical rules, the ones `CHECK.md` already states as countable. The
semantic question, whether the text carries the idea, still belongs to the blind reader.

The harness takes its shape from [`blagoySimandov/asd-ste100-writer-skill`](https://github.com/blagoySimandov/asd-ste100-writer-skill),
which scores the same standard dry-prose draws its rules from. Two things differ, and both
are in `run_eval.py`.

## Case files

| File | What it holds |
|---|---|
| `cases/cases.json` | Case ids, sentence limits by text type, required patterns |
| `cases/<case>/source.md` | The draft handed to the model |
| `cases/<case>/reference.md` | One answer that scores 100 |
| `fixtures/prompt-template.md` | The prompt wrapped around each source |
| `baseline/` | The recorded run, one file per case |

## Scoring

Each case starts at 100 and loses points per hit. A sentence limit comes from the case's
text type: 20 words for procedural, 25 for descriptive.

| Hit | Cost | Why that much |
|---|---|---|
| Sentence over the limit | 15 | The rule the reader feels first |
| Fog word | 12 | Stands in for a fact nobody supplied |
| Em dash in prose | 10 | The rule with no exceptions in prose |
| Formal word | 8 | `WORDS.md` already holds its replacement |
| Passive voice | 5 | Sometimes the right call, so it only shaves |
| Narrator frame or intensifier | 5 | Same |
| Spelled-out number | 3 | Costs the scanning reader a moment |

A missing required pattern sets the case to 0 instead. A dropped fact is not a style
gradient, so it does not shave the score, it fails the case.

## Two departures from the harness it came from

**Structure is not scored as voice.** `run_eval.py` strips fenced code blocks, table rows,
and headings before it counts anything. A reference answer that moves a paragraph into a
table would otherwise lose points for the table.

**A short answer can still fail.** The upstream harness rewards shortness without a floor,
so it would rank a telegram above real English. The `over-correction-guard` case exists to
catch that: its source is already short, and its required patterns are the articles and
connectives that a telegram drops. Its source scores 0.

## Adding a case

1. Create `cases/<id>/source.md`, the draft to sweep.
2. Create `cases/<id>/reference.md`, one answer you believe scores 100.
3. Add the case to `cases.json` with its text type and required patterns.
4. Run the harness over `reference.md` and fix whichever the score says is wrong.

Two rules for `required_patterns`, both learned by getting them wrong:

**Require a fact, never a phrasing.** A sweep may move `retried 3 times` into a table row
reading `| Retries | 3 |`. The fact survived, so match `\b3\b` and not `3 times`. A pattern
that pins the wording fails every correct rewrite that picked a different form.

**Require nothing the source does not hold.** A pattern for a fact absent from `source.md`
asks the model to invent one. The sweep is then scored on a rule the skill forbids.

## The word lists are not copied here

`run_eval.py` reads the formal and fog tables out of `../WORDS.md` at run time. A word added
to the skill is scored without a second edit, and the two lists cannot drift apart.

## Run the harness

From `skills/dry-prose`, copy the reference answers into the outputs directory to check the
harness itself:

```sh
for case in evals/cases/*/; do
  cp "$case/reference.md" "evals/outputs/$(basename "$case").md"
done
python3 evals/run_eval.py --outputs evals/outputs
```

That reports 100.0. For the opposite control, score the sources the same way and expect
roughly 21.

For a model run, fill `fixtures/prompt-template.md` with one source, write the answer to
`<output-dir>/<case-id>.md`, then point the harness at that directory.

## Re-checking the baseline

`BASELINE.md` records a run: the model, the date, and a score per case. The answers sit in
`baseline/`, so the numbers can be checked without a model:

```sh
python3 evals/run_eval.py --outputs evals/baseline
```

A ruleset change that moves those numbers wants a new baseline and a note saying what moved.
The scores measure the countable rules only, so read the answers before you accept a change.
