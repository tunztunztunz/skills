# Audit sweep

The audit branch of [`code-comments`](SKILL.md): auditing or cleaning up the comments across a
scope, rather than writing one. The rules being applied are in `SKILL.md`.

1. Enumerate every comment in scope. Confirm the scope if it was not given.
2. Disposition each one: delete it, fix the name it was compensating for, replace it with a
   link, or rewrite it at the right altitude.
3. Report the count dispositioned per file.

Done when every enumerated comment states a current constraint or is gone — each one decided,
none skipped as probably fine.
