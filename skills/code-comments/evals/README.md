# Evals for code-comments

These cases check the visible decisions the skill should drive. They are intentionally small:
the semantic question of whether a comment states a real constraint still needs human review.

## Case files

- `cases/cases.json`: case ids and mechanical constraints.
- `cases/<case>/prompt.md`: prompt supplied to the model.
- `cases/<case>/reference.md`: one acceptable answer and a harness fixture.

## Run the harness

From `skills/code-comments`, copy the reference answers to a temporary output directory to
self-check the harness:

```sh
mkdir -p /tmp/code-comments-evals
for case in evals/cases/*/; do
  cp "$case/reference.md" "/tmp/code-comments-evals/$(basename "$case").md"
done
python3 evals/run_eval.py --outputs /tmp/code-comments-evals
```

For a model run, write each answer to `<output-dir>/<case-id>.md`, then use the same command.
The verifier checks required phrases, comment-line limits, and banned text in cases that return
source code. It cannot establish intent; inspect the responses before accepting a ruleset change.
