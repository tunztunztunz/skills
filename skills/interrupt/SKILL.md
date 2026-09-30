---
name: interrupt
description: Draws a random lateral-thinking card and reads the problem at hand through it. Use whenever an Interrupt card arrives already drawn, when stuck, when looping on one approach, when the user asks for an interrupt or an oblique strategy, or to show a specific card by number.
---

# Interrupt

A deck of 64 cards. Each one exists to change the next experiment; none of them
give advice.

## Draw

The binary chooses the card. Your work starts once it prints one.

**A card may already be in your context.** `interrupt draw --notify` posts the
four text lines from the user's own terminal, and they arrive labelled as coming
from another Claude session — the message itself says it came from the user's
terminal, and that is what to trust. It is a completed draw: interpret it and
run nothing. Drawing again would replace their card with one they never saw.

Otherwise draw it yourself:

```bash
interrupt draw
```

Either way you get four plain lines — title with disruption level, family, body,
card number. Work from those.

**Render is a terminal's job; your reply carries the text.** The 29-row card
holds trailing whitespace that does not survive being copied. When the user
wants the card itself, give them a command to run rather than a description of
what they are getting.

Prefer whatever passthrough your host offers: a way to run a command in the
user's own terminal rather than capturing its output as a tool result. That
route renders the card for them and puts the same draw in your context, one run
serving both. In Claude Code it is `! interrupt draw --full`.

Failing that, `interrupt draw --full --notify` run in a second terminal in this
directory renders the card there and sends its text here.

Draw → Render → Interpret. The draw is unweighted and context-independent;
context enters at the interpretation and nowhere earlier. Every card shown comes
from an `interrupt` run in this conversation, and one run yields one card — when
a card feels wrong for the situation, that friction is the mechanism working, so
interpret the card that came up.

`--id N` shows a specific card when the user asks for one by number. It
inspects; it is not a draw.

If `interrupt` is not on `PATH`, say so and give the user the install command:

```bash
go install github.com/tunztunztunz/interrupt/cmd/interrupt@latest
```

Inside a clone of the repo, `go run ./cmd/interrupt draw` works right away.

## Output

Name the card in one line, then two sections. Reproduce the four compact lines
if the user has not seen the draw; leave the card frame to the terminal.

```
**REMOVE THE MIDDLE** ◇2 · REDUCE · 001

**Interpretation**
One or two sentences reading the card against the problem at hand.

**Experiment**
One thing to try next, naming a file, command, or symbol in this codebase.
```

## Interpreting

Stay **oblique**. A card is a *motion*, not a recommendation.

- Apply the card's motion — remove, invert, disturb, observe, displace,
  exaggerate, rename, interrupt — to something named: this function, this test,
  this assumption, this dependency.
- Read it against *this* problem, in this codebase, at this moment.
- An oblique reading still surprises after it is restated; a collapsed one turns
  into standard practice. "REMOVE THE MIDDLE" reads as *take the middle out and
  watch what the ends do*, not as "refactor the middle layer".
- Commit to one reading. Ambiguity is the card's job; choosing among it is yours.
- The disruption level sets the risk available: `◇1` observes and reverses
  cleanly, `◇2` changes something local, `◇3` breaks something on purpose. For
  `◇3`, name what breaks and where it is safe to break it.

Done when the drawn card is named, one reading is committed to, and the
experiment names something that already exists in this codebase.
