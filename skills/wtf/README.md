# wtf

Explains something at whiteboard altitude: the shortest plain-English version, drawn rather than
described. `/wtf` on its own redraws the reply above it, which is the usual way it gets used. Ask
normally, and when the answer is a wall, ask for the drawing.

One plugin, three commands. They share a voice and a template, so they install together.

| Command | What you get |
|---|---|
| `/wtf` | The last reply, redrawn at whiteboard altitude |
| `/wtf <question>` | That question answered the same way |
| `/wtf-html <question>` | A self-contained HTML explainer on your Desktop, opened |
| `/wtf-brand --logo <path>` | Your logo and accent in the explainer's shareable theme |

Each command loads only its own `SKILL.md`, so a terminal answer never pays for the page.

## Install

```sh
claude plugin install wtf@classward      # Claude Code
codex plugin add wtf@classward           # Codex
skills/wtf/opencode/install.sh           # opencode, from a clone
```

The repo [`README`](../../README.md) covers adding the marketplace, the opencode bootstrap,
updating, and uninstalling. Restart the host afterwards; skills are discovered at startup.

## Prerequisites

`/wtf` needs nothing. The other two do:

| Tool | Needed for | Check |
|---|---|---|
| A browser | `/wtf-html`, which writes the page to disk and opens it | — |
| `cwebp`, `sips` | `/wtf-brand`, for logo encoding | `brew install webp` |
| Pillow | `/wtf-brand`, for reading the accent off the logo | `python3 -c 'import PIL'` |
| `rsvg-convert` | `/wtf-brand`, SVG logos only | `brew install librsvg` |

## Layout

```
skills/wtf/SKILL.md           # the whiteboard rules
skills/wtf/SHAPES.md          # a worked example of every drawing shape, read when drawing
skills/wtf-html/SKILL.md      # the explainer procedure, the visual spine, the engine API
skills/wtf-html/TEMPLATE.html # the explainer skeleton: stack, components, animation engine
skills/wtf-brand/SKILL.md
skills/wtf-brand/brand.py     # patches a logo and accent into TEMPLATE.html
```

Every file a skill reads sits in that skill's own directory, so the three work whether the host
installs a plugin directory or symlinks each skill on its own. `brand.py` reaches the template as
`../wtf-html/TEMPLATE.html`, which holds under both.

## Notes

Branding is written into `TEMPLATE.html` where it is installed. Under Claude Code and Codex each
version installs into its own directory, so re-run `/wtf-brand` after updating. Under opencode the
skills are symlinks into your clone, so it survives until a `git pull` touches the template.

All three carry `disable-model-invocation: true`. Claude Code honours it, so there they fire when you
ask and never on their own.
