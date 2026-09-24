---
name: code-comments
description: Comment rules — the constraint test a comment passes before it is written. Use when writing or editing a comment or doc comment, reviewing the comments in a diff, or auditing comments across a codebase.
---

# code-comments

A code comment states a constraint the code cannot carry: change the code so it contradicts that
constraint, and the code is wrong. Ask of every comment: *what change does this comment forbid?*
No answer, no comment.

These rules govern comments and doc comments inside source files. Prose written for humans —
README and docs pages, tutorials, commit messages, PR bodies, tickets, changelogs — keeps its
narrative and its history.

## Procedure

1. Read the code in its immediate context and the requested change.
2. Run the deletion test. Change the code or link to the source of truth when that preserves the
   needed information. Stop when only a forcing constraint remains.
3. Give that constraint the right altitude and form.
4. Run the quality check before returning the change.

## The deletion test

Each gate makes the comment unnecessary. Run all three first.

1. **Rename or extract.** A comment explaining a name or a dense block is a naming bug. Fix the
   name or lift a helper so the code says it.
2. **Link, don't redefine.** When the concept lives elsewhere, point at it (`see ListRepos`, a
   docs page, an ADR) and stop.
3. **No forcing constraint, no comment.** Most changes need none. Write one only when something
   invisible shaped the code: a rule the syntax can't hold, an external API's behaviour, a
   deliberate rejection of the obvious alternative.

## Altitude

- **Interface** comments (above a func, type, class, or package) fly *higher* than the code:
  what it does, when to reach for it, what it costs the caller. How it works stays out.
- **Implementation** comments (inside) fly *at or below*: the constraint the syntax cannot
  carry — why a value is that value, an ordering dependency, a deliberate omission.

## Form

Present tense, stating what holds now. Inline comments fit one line; a doc block fits a hover
tooltip. Name a domain concept with the project's own term when it publishes one (glossary,
`CONTEXT.md`, ADR).

Write the standing rule, not the story that produced it:

| Write | Not |
|---|---|
| `error stays out of the column list until a collector can fail` | `we decided during an earlier fix not to write error yet` |
| `every installation token reaches this endpoint whatever the App's grants are` | `ListRepos was 403ing so this was changed` |
| `normalised at construction so one package cannot fork into two identities` | `fixes the duplicate-purl bug` |

Issue and ticket identifiers belong in work records. Commit messages and PR bodies hold history;
comments hold the contract.

## Banned phrasing

Delete or replace these with a concrete constraint:

| Do not write | Write instead |
|---|---|
| a ticket or issue identifier (`#123`, `ABC-123`, `issue 123`, `ticket 123`) | the current constraint |
| `load-bearing` in any spelling, or `earns its place` | the invariant or constraint |
| `this comment`, `this code`, `the code below`, or `the following code` | the behavior or constraint |
| `simply`, `just`, `robust`, `clean`, `elegant`, or `best practice` | nothing; delete the intensifier |
| `ensures correctness`, `handles edge cases`, `prevents errors`, or `improves performance` | the condition and outcome |

Exact markers required by a compiler, linter, generator, or repository convention are syntax,
not comment prose. `TODO` follows the repository's convention.

## Quality check

- Every remaining comment names a current constraint the code could contradict.
- The code and its names carry everything they can; a comment holds only what they cannot.
- Interface comments describe the caller's contract, and implementation comments name the local
  constraint.
- The text states the standing rule, not the work that led to it.
- No phrase from the **Do not write** table appears in the comment.

Done when every remaining comment passes every check.

## Generated files

Comment the source the generator reads — the `.sql` behind sqlc, the `.proto` behind protoc,
the schema behind an ORM's models — and let it regenerate. Generated output and vendored
third-party code stay as they are.

## Audit sweep

Asked to audit or clean up comments across a scope, read the `AUDIT.md` beside this file and
follow it.
