---
name: wtf-html
description: Build a single elegant HTML explainer that answers the question in diagrams and plain English, then open it.
disable-model-invocation: true
---

# wtf-html

Turn the question in the arguments into one self-contained HTML **explainer** — a designed page a smart person outside the field reads once and understands. Diagrams carry the explanation. Prose captions them.

Write to `~/Desktop/<kebab-slug>.html` unless the arguments name a path.

## Steps

1. **Do the work.** Read the code, the files, the docs the question points at. Where the question asks what something *would* take, find what exists today before describing what's missing. Done when every claim on the page traces back to something you actually read — no placeholder sections, no invented module names, no "TBD".
2. **Storyboard.** List the sections in order, and for each one name the single visual that carries it *before* writing any prose. A section whose visual is "a paragraph" is a section that hasn't been thought through — find its shape or merge it into its neighbour. Done when every section has a named visual and the sequence answers the question end to end.
3. **Copy the skeleton** — `TEMPLATE.html` sits beside this file, so `cp <this skill's directory>/TEMPLATE.html <path>` — then fill it. It carries the stack, the component classes, the colour legend, the animation engine, and one worked example of every pattern. To see its structure, read it filtered:

   ```
   grep -v 'base64,' <path>
   ```

   Two lines hold the inlined logo and favicon as base64 — about 2,900 tokens of data with nothing in it for you, already carried into your copy by `cp`. Edit around those lines; never read, rewrite, or delete them. The script block needs no reading and no editing either. Done when every `FILL`, every `XXX`, and every unused pattern block is gone.
4. **Open it** — `open <path>` — and report the path plus a three-line summary of what the page argues.

## Visual spine

Every section leads with its visual. Prose is caption-length: two or three sentences under the diagram, never a wall above it.

**Mermaid is the default.** It is the cheapest thing to author and the easiest to get right — reach for it first and only fall out when the table below says to:

| Idea | Mermaid type |
|---|---|
| Pipeline, a request's life, any boxes-and-arrows | `flowchart LR` |
| What contains what, what can reach what | `flowchart` + `subgraph` |
| Across systems, in order, over time | `sequenceDiagram` |
| Phases, order of work, dependencies | `timeline` or `gantt` |
| States and what moves between them | `stateDiagram-v2` |
| Data model, tables, relationships | `erDiagram` — renders oversized in a card; prefer `flowchart` |
| Architecture layers | `block-beta` |
| Effort against value | `quadrantChart` |
| Volume moving through a system | `sankey-beta` |
| Numbers over time | `xychart-beta` |

Three things stay out of mermaid, because mermaid is worse at them or has nothing:

- **Proportion inline with the prose** → `.bars` from the template.
- **Today vs. after** → `.col2`, same row labels both sides.
- **Several things on several axes** → `.tbl`, a plain `<table>` whose cells do the work (`✓` / gap / partial). The class styles every `th` and `td`; never put `.lbl` on a header cell.

For real charts of real numbers, invoke the `dataviz` skill before writing chart code.

## Engine API

The template's script block is the whole implementation — never read it, never edit it, never write
an `IntersectionObserver` or a keyframe by hand. This is everything it exposes.

**Hero diagrams.** Nodes are divs on a grid; edges are declared, not drawn:

```html
<div class="scroller">
  <div class="graph" id="g1" style="min-width:40rem">
    <div class="node" id="hub" data-col="2" data-row="1" data-span="2" data-step="2"
         data-detail="Shown in the panel on hover.">
      <b>Bold label</b><code>the real symbol — line 117</code>
    </div>
  </div>
</div>
<div class="panel" id="d1">Resting text.</div>
```

```js
edges('a→hub:trigger', 'hub→out:danger')   // line styles: plain trigger danger note
play('a→hub→out')                          // a dot traces the order, on reveal
inspect('#g1', { panel: '#d1' })           // dim the rest, light what connects, fill the panel
```

`data-col`/`data-row` place the node and `data-span` straddles rows — never write `grid-column` or
`grid-row` by hand. `data-step` pins a numbered badge to the corner when order matters. Add
`class="accent"` to the one node the diagram is about, and keep the `.scroller` wrapper so the
graph survives a narrow window. Put the calls in a `<script>` right after the graph; they are
queued and replayed once layout settles.

**Components.** `.card` `.lbl` `.g3` `.col2` `.bars` `.bar` `.track` `.tbl` `.panel` `.hint` `.note`
`.legend` `.chip`. A bare `<code>` in prose styles itself as a chip — never hand-style one.
Colour comes from three CSS variables — `--today`, `--build`, `--retire` — used
as `.card.build`, `.track.retire`, `<i class="swatch today">`. Render the `.legend` chips once near
the top and hold those meanings for the whole page. Never reach for a raw Tailwind colour.

**Themes.** The page ships loud: logo, lime nav, 2px black outlines, hard offset shadows, halftone
paper. Every page also carries an **Export for sharing** button that saves a copy in the work
theme — same warm paper, but thin borders, soft shadows, blue and red accents, no logo and no WTF
favicon — for people outside the team. Leave the logo and the button in place, and leave the
`<html>` tag alone. Setting `data-theme="work"` on it also hides the export button, so the choice
is one-way — do it only when the arguments name an outside audience in so many words. Both themes
run off the same variables; never hand-edit colours to fake either one. `/wtf-brand` puts your own
logo and accent into that work theme.

**Verbs.** Each takes an element and an optional `{delay}`; all respect reduced-motion:

```js
onReveal(el, fn)     // run fn when el scrolls into view — the only trigger you need
draw(path)           // an SVG stroke draws itself
grow(el)             // width animates up from zero
walk(path, {loop})   // a dot travels a path
fade(el)             // in and up
count(el, to)        // a number ticks to its value
stagger(els, verb)   // apply any verb across children, in sequence
```

Section reveal, `.bars` growth, and `.count` all fire on their own — no call needed. `edges()`
returns the real paths, so anything it draws is fair game for `draw`, `walk`, or your own
`onReveal`. Reach past the API only when no combination of these fits.

## Voice

Same bar as `/wtf`, applied to the page:

- Every word passes the stranger test — a smart person outside this field knows it. A term with no plain substitute gets defined in four words at first use, then gets used freely.
- Lead each section with its conclusion, then show why.
- Concrete: real file paths, real table names, real counts.
- Where something is unknown or a judgement call, say so in a `.note` callout rather than writing confident filler.
- No emoji. No stock icons. No lorem. No collapsed sections hiding the substance.
