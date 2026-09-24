---
name: wtf
description: Answer at whiteboard altitude - shortest plain-English version, drawn rather than described. No args re-answers the last reply.
disable-model-invocation: true
---

# wtf

Answer like you're at a **whiteboard** with a marker, not writing a document. Sketch the shape, say the short thing out loud, stop. The drawing carries the explanation; the words caption it.

Two branches:

- **Arguments given** (`/wtf explain X`) — X is the subject.
- **No arguments** — the subject is your own last reply. Re-answer it at whiteboard altitude. Same content, redrawn. Never apologise for the first version, never reference it.

## Steps

1. **Find the one sentence.** What does the reader walk away knowing? Everything else ranks against it.
2. **Storyboard.** List every fact the subject carries, one line each — for a PR: what changed, why, what it touches, what could break. Then name the shape that carries each cluster, before drawing anything. Most subjects need two shapes, not one. A cluster whose shape is "a paragraph" is one you haven't understood — find its shape or fold it into its neighbour. Done when nothing in the source material is unlisted and every survivor has a named shape.
3. **Draw it.** Pick each shape from the match table below, then read its worked example and rules in [`SHAPES.md`](SHAPES.md) before you draw. At least one drawing, always. Type arrows as three characters — `-->`, `<--` — never `→ ▶ ➔`, which are ambiguous-width and shift every row they sit in. The font ligates the ASCII into a longer, better arrow than the one you'd reach for. Done when each drawing matches the geometry of its `SHAPES.md` example — same column structure, same connectors, nothing borrowed from a neighbouring shape.
4. **Caption it.** Plain sentences under the drawing, each one earning its line.
5. **Cut to one screen.** Roughly 25 lines tall, 60 columns wide, drawings included. What the screen can't hold gets one closing line naming it — `not covered: migration order, rollback`. A map with no edges reads as complete.

Done when a sharp person from outside this field could repeat the answer back correctly, in their own words, having read it once.

## Drawing vocabulary

Match the kind of idea to the shape:

- one thing happens after another --> **Flow**
- the stages are components rather than steps --> **Boxed flow**
- two or more parties exchanging messages --> **Sequence**
- one decision, different outcomes --> **Branch**
- old name becomes new name --> **Mapping**
- what overrides what --> **Tree**
- something moves between modes and back --> **State machine**
- what lives inside what --> **Nesting**
- before and after --> **Split**
- proportion of a whole --> **Bars**
- when things happen and for how long --> **Timeline**
- the shape of a series --> **Sparkline**
- two values on a real scale --> **Number line**
- several things compared on several axes --> **Table**

[`SHAPES.md`](SHAPES.md) holds the worked example of each, and the rules that belong to one shape rather than all of them.

Never improvise a shape — the usual failure is a hand-drawn grid, and a grid is a Table. When a cluster genuinely has no shape on the list, its caption carries it alone; the clusters that do have shapes still get drawn.

Label the arrows. A drawing nobody can read without the paragraph underneath is a failed drawing — redraw it.

## Colour

Three rules. There is no fourth — nothing else survives.

- **`ini` fence for every drawing.** The lexer leaves the art alone and turns `#` annotations green. That is the whole in-drawing colour system. An annotation is one line — a wrapped one loses its colour halfway through.
- **`diff` fence for a Split only.** Red and green already mean before and after.
- **Nothing reliably colours a single node.** To single one out, point at it with a `#` leader. Don't reach for `yaml` — it paints the entire drawing one colour.

## Alignment

The terminal renders these in a monospace grid, so alignment is the whole drawing.

- **One column, one start position.** Every arrow in a drawing begins at the same screen column, every label at the same one. Ragged columns read as separate drawings stacked on top of each other.
- **Every column carries a value on every row**, or it isn't a column — a half-empty column reads as "these rows produce nothing". Fold it into the caption instead.
- **60 columns.** A drawing that wraps is destroyed, not degraded.
- **Two drawings in one answer get different shapes and their own fences.** A sequence and a comparison that look alike tell the reader they are the same kind of thing; two shapes sharing one fence read as one drawing that contradicts itself.

## Voice

- Lead with the answer. The first line is the conclusion, not the setup.
- Every word passes the stranger test: a smart person outside this field knows it. A term with no plain substitute gets four words of definition in the same breath, then gets used.
- Short sentences. Fragments land.
- Concrete over abstract. Name the actual file, the actual number, the actual thing on screen.
- State it straight. Flag uncertainty only where being wrong would change what they do.
- No preamble, no recap, no "hope that helps."
