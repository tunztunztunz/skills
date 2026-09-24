#!/usr/bin/env python3
"""Install work-theme branding into the explainer template: a logo, an accent colour, or both.

Writes into TEMPLATE.html once. Generated documents carry the result with no per-run token cost,
because the template is copied rather than read.
"""
import argparse
import base64
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "wtf-html" / "TEMPLATE.html"
WORK_SURFACE = "#fffdfa"
DEFAULT_BUILD, DEFAULT_WASH = "#2b56c4", "#eef2fd"


def slot(text, name, inner):
    open_tag, close_tag = f"<!--WORK-{name}-->", f"<!--/WORK-{name}-->"
    i, j = text.index(open_tag) + len(open_tag), text.index(close_tag)
    return text[:i] + inner + text[j:]


def hex_to_rgb(value):
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        sys.exit(f"not a hex colour: {value}")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c))) for c in rgb)


def luminance(rgb):
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def darken_to_readable(rgb, background, target=4.5):
    """A brand colour bright enough to be a fill is usually too bright to be a label."""
    current = list(rgb)
    for _ in range(80):
        if contrast(current, background) >= target:
            break
        current = [c * 0.94 for c in current]
    return tuple(current)


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode:
        sys.exit(f"{cmd[0]} failed: {result.stderr.strip() or result.stdout.strip()}")


def rasterize(src, work):
    """sips and Pillow both read pixels, not paths, so vector input renders first."""
    if src.suffix.lower() != ".svg":
        return src
    if not shutil.which("rsvg-convert"):
        sys.exit("SVG input needs rsvg-convert — install it with: brew install librsvg")
    png = work / "source.png"
    run(["rsvg-convert", "-h", "256", "-b", "none", str(src), "-o", str(png)])
    return png


def encode_logo(src, work):
    png, webp = work / "logo.png", work / "logo.webp"
    run(["sips", "-Z", "96", str(src), "--out", str(png)])
    run(["cwebp", "-quiet", "-q", "90", "-alpha_q", "100", str(png), "-o", str(webp)])
    data = base64.b64encode(webp.read_bytes()).decode()
    return f"data:image/webp;base64,{data}", webp.stat().st_size


def encode_favicon(src, work):
    png = work / "fav.png"
    run(["sips", "-Z", "32", str(src), "--out", str(png)])
    data = base64.b64encode(png.read_bytes()).decode()
    return f"data:image/png;base64,{data}", png.stat().st_size


def accent_from_logo(src):
    """The brand colour is the most-used colour that a human would call a colour: transparent,
    near-white, near-black and near-grey pixels are chrome, not identity."""
    from PIL import Image
    image = Image.open(src).convert("RGBA").resize((64, 64))
    counts = {}
    for r, g, b, a in image.getdata():
        if a < 128:
            continue
        high, low = max(r, g, b), min(r, g, b)
        if high < 40 or low > 225 or high - low < 40:
            continue
        counts[(r // 24, g // 24, b // 24)] = counts.get((r // 24, g // 24, b // 24), 0) + 1
    if not counts:
        return None
    bucket = max(counts, key=counts.get)
    return rgb_to_hex([c * 24 + 12 for c in bucket])


def set_accent(text, hex_value):
    rgb = hex_to_rgb(hex_value)
    readable = darken_to_readable(rgb, hex_to_rgb(WORK_SURFACE))
    build = rgb_to_hex(readable)
    wash = rgb_to_hex([c + (255 - c) * 0.92 for c in rgb])
    return replace_accent(text, build, wash), build, wash, contrast(readable, hex_to_rgb(WORK_SURFACE))


def replace_accent(text, build, wash):
    start = text.index('[data-theme="work"] {')
    end = text.index("}", start)
    block = text[start:end]
    block = re.sub(r"--build-wash:\s*#[0-9a-fA-F]{3,6};", f"--build-wash:{wash};", block)
    block = re.sub(r"--build:\s*#[0-9a-fA-F]{3,6};", f"--build:{build};", block)
    return text[:start] + block + text[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--logo", help="image file to use as the work-theme logo")
    parser.add_argument("--accent", help="hex colour for the work theme's --build; omit with --logo to read it off the logo")
    parser.add_argument("--clear", action="store_true", help="remove work branding")
    args = parser.parse_args()

    if not (args.logo or args.accent or args.clear):
        parser.error("give --logo, --accent, or --clear")

    text = TEMPLATE.read_text()
    changes = []

    if args.clear:
        text = slot(slot(text, "LOGO", ""), "FAVICON", "")
        text = replace_accent(text, DEFAULT_BUILD, DEFAULT_WASH)
        changes.append(f"cleared work logo and favicon, accent back to {DEFAULT_BUILD}")

    if args.logo:
        src = Path(args.logo).expanduser()
        if not src.is_file():
            sys.exit(f"no such file: {src}")
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            raster = rasterize(src, work)
            logo_uri, logo_bytes = encode_logo(raster, work)
            fav_uri, fav_bytes = encode_favicon(raster, work)
            sampled = None if args.accent else accent_from_logo(raster)
        text = slot(text, "LOGO",
                    f'<span class="brand-work tab shrink-0 px-3">'
                    f'<img src="{logo_uri}" alt="" class="h-10 w-auto"></span>')
        text = slot(text, "FAVICON",
                    f'<link rel="icon" class="fav-work" type="image/png" sizes="32x32" href="{fav_uri}">')
        added = round((logo_bytes + fav_bytes) * 4 / 3 / 3)
        changes.append(f"logo {logo_bytes:,} B + favicon {fav_bytes:,} B  (~{added:,} tokens if read unfiltered)")

        if not args.accent:
            args.accent = sampled
            if sampled:
                changes.append(f"accent read off the logo: {sampled}")
            else:
                changes.append("no brand colour found in the logo — accent left as it was")

    if args.accent:
        text, build, wash, ratio = set_accent(text, args.accent)
        note = "" if ratio >= 4.5 else "  [could not reach 4.5:1 — check legibility]"
        shifted = "" if build.lower() == args.accent.lower().rstrip() else f" (darkened from {args.accent} for text contrast)"
        changes.append(f"accent --build:{build}{shifted}  --build-wash:{wash}  contrast {ratio:.1f}:1{note}")

    TEMPLATE.write_text(text)
    for line in changes:
        print(line)
    print(f"\ntemplate: {TEMPLATE}  {len(text):,} B")


if __name__ == "__main__":
    main()
