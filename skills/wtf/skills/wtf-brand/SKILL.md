---
name: wtf-brand
description: Install a work logo and accent colour into the wtf-html template, so Export for sharing carries your own branding instead of none.
disable-model-invocation: true
---

# wtf-brand

One-time setup for `/wtf-html`. Writes a logo and an accent colour into `TEMPLATE.html`, so every
document generated afterwards carries them and **Export for sharing** swaps the WTF branding for
yours instead of stripping branding entirely.

Run once. Costs nothing per document — the template is copied, not read.

## Steps

1. **Work out what was asked for.** A path to an image is enough on its own — the accent is read
   off the logo unless a hex is given. `--clear` undoes both. If the arguments name a file that
   isn't an image, or a colour that isn't hex, say so and stop rather than guessing.
2. **Run the script.** `brand.py` sits beside this file, and finds the template itself. A logo alone
   is the normal case:

   ```
   python3 <this skill's directory>/brand.py --logo <path>
   python3 <this skill's directory>/brand.py --logo <path> --accent '#1f6feb'   # override
   ```

   It resizes to 96px, converts to WebP, encodes, picks the brand colour out of the artwork,
   derives the light wash from it, darkens it until it reaches 4.5:1 against the page for text use,
   and patches the template. Report its output verbatim — the accent and contrast lines matter.
3. **Verify in the browser.** Write a work-theme preview and open it, passing the template path the
   script just reported:

   ```
   python3 -c "import os, pathlib, sys; \
   s=pathlib.Path(sys.argv[1]).read_text() \
     .replace('<html lang=\"en\">','<html lang=\"en\" data-theme=\"work\">'); \
   open(os.environ['TMPDIR']+'/work-preview.html','w').write(s)" <template> \
   && open "$TMPDIR/work-preview.html"
   ```

   Done when the work logo shows in the nav, the WTF logo does not, and the `.card.build` /
   `.track.build` colours read as the accent. The favicon stays the WTF one here — a `<link>` cannot
   be themed, so yours appears only in a file saved by **Export for sharing**.

## What it touches

| Slot in `TEMPLATE.html` | Holds |
|---|---|
| `<!--WORK-LOGO-->` | the `.brand-work` nav tab, hidden outside the work theme |
| `<!--WORK-FAVICON-->` | a `link.fav-work` the export keeps when it drops `link.fav-wtf` |
| `[data-theme="work"]` | `--build` and `--build-wash` |

Nothing else changes. The default theme, the WTF logo, and the engine are untouched, and the
accent overwrites existing values in place so the template does not grow.

## Notes

- **The accent comes from the logo.** The script takes the most-used colour a human would call a
  colour — transparent, near-white, near-black and near-grey pixels are chrome, not identity. Pass
  `--accent` when the logo's loudest colour isn't the one the brand actually uses.
- **A bright brand colour cannot be both.** `--build` is text and strokes, `--build-wash` is the
  fill behind them. The script keeps your hex for the wash and darkens it for the text, so a yellow
  brand gives a yellow fill with a readable olive label rather than illegible yellow type.
- **A plugin update clears it.** Each version installs into its own directory, so the branding lives
  only in the template you patched. Re-run `/wtf-brand` after updating the plugin. An opencode
  install is symlinked into the clone instead, so there it survives until the next `git pull` that
  touches the template.
- **Documents already written keep whatever they were built with.** They are finished files;
  re-run `/wtf-html` to pick up new branding.
- **Only the work theme is brandable.** The default theme is the WTF identity and stays as it is.
