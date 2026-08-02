#!/usr/bin/env python3
"""
Generate the mark + wordmark lockups.

The wordmark is set in IBM Plex Sans SemiBold and converted to outlines, so a
lockup is artwork rather than font software: it renders identically anywhere,
with no webfont to load and no font to install. Plex is therefore a design-time
dependency only — it never ships to a site. See decision 0007.

Two constructions, and only two (decision 0007):

    horizontal   mark beside "Jeff Olsen"
    stacked      mark above "jeffols"

The mark is a lowercase j and "jeffols" begins with one, so setting them side by
side reads as "j jeffols". The capital J breaks that echo, which is why the
horizontal lockup uses the full name and the compact brand only ever stacks.

Dependencies:
    pip install fonttools

Usage:
    python scripts/generate_lockups.py
    python scripts/generate_lockups.py --palette electric_blue
"""

from pathlib import Path
import argparse

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

import geometry
from geometry import DESIGN_SIZE, svg_shapes
from generate_favicon_assets import PALETTES, modes_for

REPO = Path(__file__).resolve().parent.parent
WORDMARK_FONT = REPO / "assets" / "fonts" / "design-time" / "IBMPlexSans-SemiBold.ttf"

# Glyph bounding box within the 1024 design space, after the 0005 framing shift.
MARK_BOX = (322, 120, 702, 860)
MARK_W = MARK_BOX[2] - MARK_BOX[0]
MARK_H = MARK_BOX[3] - MARK_BOX[1]

# Tuned against the specimens: the mark reads as a peer of the type rather than
# an icon bolted to it when its height is a little over twice the cap height.
CAP_MULTIPLE = 2.15
GAP_RATIO = 0.42          # horizontal gap, as a fraction of font size
STACK_GAP_RATIO = 0.30    # vertical gap for the stacked construction
TRACKING = -0.015         # em, tightens the wordmark slightly


def outline(text, font_path, size, tracking=TRACKING):
    """Text as a single SVG path, plus its advance width and cap height.

    Returns coordinates in a Y-down space with the baseline at y=0, which is
    what SVG wants and the opposite of what font files store.
    """
    font = TTFont(str(font_path))
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    glyphset = font.getGlyphSet()
    hmtx = font["hmtx"]

    pen = SVGPathPen(glyphset)
    x = 0.0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            raise SystemExit(f"{font_path.name} has no glyph for {ch!r}")
        # Flip Y, scale to size, place at the running pen position.
        glyphset[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
        x += hmtx[name][0] * scale + tracking * size

    cap = getattr(font.get("OS/2"), "sCapHeight", None) or upem * 0.7
    return pen.getCommands(), x - tracking * size, cap * scale


def mark_group(scale, tx, ty, fill):
    """The mark, scaled and placed. Geometry still comes from geometry.py."""
    return (f'  <g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.5f})"'
            f' fill="{fill}">\n'
            + svg_shapes(indent="    ")
            + '  </g>\n')


def build(kind, text, background, glyph, size=200, pad_ratio=0.5):
    """One lockup SVG. background=None leaves it transparent."""
    d, text_w, cap = outline(text, WORDMARK_FONT, size)
    mark_scale = (cap * CAP_MULTIPLE) / MARK_H
    mw, mh = MARK_W * mark_scale, MARK_H * mark_scale
    pad = size * pad_ratio

    if kind == "horizontal":
        gap = size * GAP_RATIO
        w = pad * 2 + mw + gap + text_w
        h = pad * 2 + mh
        # Optical centring: align the mark's centre to the cap-height midpoint.
        baseline = pad + mh / 2 + cap / 2
        mark_tx = pad - MARK_BOX[0] * mark_scale
        mark_ty = pad - MARK_BOX[1] * mark_scale
        text_tx = pad + mw + gap
    else:
        gap = size * STACK_GAP_RATIO
        w = pad * 2 + max(mw, text_w)
        h = pad * 2 + mh + gap + cap
        baseline = pad + mh + gap + cap
        mark_tx = pad + (max(mw, text_w) - mw) / 2 - MARK_BOX[0] * mark_scale
        mark_ty = pad - MARK_BOX[1] * mark_scale
        text_tx = pad + (max(mw, text_w) - text_w) / 2

    plate = (f'  <rect width="{w:.2f}" height="{h:.2f}" fill="{background}"/>\n'
             if background else "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg"'
        f' viewBox="0 0 {w:.2f} {h:.2f}" role="img"'
        f' aria-label="{text}">\n'
        f'{plate}'
        + mark_group(mark_scale, mark_tx, mark_ty, glyph)
        + f'  <path transform="translate({text_tx:.2f} {baseline:.2f})"'
          f' d="{d}" fill="{glyph}"/>\n'
        f'</svg>\n'
    )


CONSTRUCTIONS = [("horizontal", "Jeff Olsen"), ("stacked", "jeffols")]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--palette", default="signal_yellow", choices=list(PALETTES))
    p.add_argument("--out", default=str(REPO / "assets" / "lockups"))
    a = p.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    written = []

    for kind, text in CONSTRUCTIONS:
        # Monochrome: no plate, inherits colour from the surrounding CSS.
        name = f"lockup-{kind}-mono.svg"
        (out / name).write_text(build(kind, text, None, "currentColor"),
                                encoding="utf-8")
        written.append(name)

        for mode in modes_for(a.palette):
            c = PALETTES[a.palette][mode]
            # On a plate, and transparent for placing on an existing surface.
            for suffix, bg in ((mode, c["background"]), (f"{mode}-transparent", None)):
                name = f"lockup-{kind}-{a.palette}-{suffix}.svg"
                (out / name).write_text(build(kind, text, bg, c["glyph"]),
                                        encoding="utf-8")
                written.append(name)

    (out / "README.md").write_text(
        "# Lockups\n\n"
        "Generated by `scripts/generate_lockups.py`. Do not edit by hand.\n\n"
        "The wordmark is IBM Plex Sans SemiBold **converted to outlines**, so "
        "these are artwork, not font software. They render anywhere with no "
        "webfont and no font installed.\n\n"
        "Two constructions only (decision 0007):\n\n"
        "- `lockup-horizontal-*` — mark beside **Jeff Olsen**\n"
        "- `lockup-stacked-*` — mark above **jeffols**\n\n"
        "Never set the mark horizontally beside lowercase `jeffols`: the mark is "
        "a lowercase j and the word starts with one, so it reads as "
        "\"j jeffols\". The capital J in the full name breaks that echo.\n\n"
        "`-mono` inherits `currentColor`. `-transparent` has no plate.\n",
        encoding="utf-8")

    for n in written:
        print(f"  {n}")
    print(f"{len(written)} lockups in {out}")


if __name__ == "__main__":
    main()
