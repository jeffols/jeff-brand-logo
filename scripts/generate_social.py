#!/usr/bin/env python3
"""
Generate the social preview (Open Graph) composition.

Without one of these, anything shared from jeffols.com previews as a bare link
on LinkedIn, Slack, iMessage and everywhere else. 1200x630 is the size those
platforms crop to.

A wide surface, so composition governs rather than the size rule: the lockup
carries the identity and an oversized rotational mark bleeds off the right edge
as background. BRAND.md section 14 asks for exactly that — the naked geometry
must stay recoverable inside the echoes.

Deliberately almost no text. BRAND.md section 23 still lists the final homepage
headline as undecided, and an OG image with a tagline baked in goes stale the
day that changes. Mark plus name plus domain does not.

Dependencies:
    pip install pillow fonttools      (headless Chrome to rasterise)

Usage:
    python scripts/generate_social.py
    python scripts/generate_social.py --palette deep_indigo --mode dark
"""

from pathlib import Path
import argparse
import subprocess

from geometry import svg_shapes
from generate_favicon_assets import PALETTES, modes_for
from generate_linkedin_banners import find_chrome
from generate_lockups import MARK_BOX, MARK_H, MARK_W, WORDMARK_FONT, outline
from generate_rotational_logo import PIVOT, layer_specs, resolve

REPO = Path(__file__).resolve().parent.parent
W, H = 1200, 630
SIZES = [(1200, 630), (1600, 840)]      # OG, and a 2x-ish for retina crops


def rotational_group(scale, tx, ty, fill, opacity):
    """The canonical 3-layer stack, oversized, as background."""
    cfg = resolve("plates", None, {})
    px, py = PIVOT
    body = []
    for angle, op, sc in layer_specs(cfg["layers"], cfg["step"], cfg["min_opacity"],
                                     cfg["gamma"], cfg["scale_step"], PIVOT):
        tf = (f'rotate({angle:g} {px:g} {py:g}) translate({px:g} {py:g}) '
              f'scale({sc:.4f}) translate({-px:g} {-py:g})')
        body.append(f'      <g transform="{tf}" opacity="{op:.3f}">\n'
                    + svg_shapes(indent="        ") + '      </g>\n')
    return (f'  <g transform="translate({tx:.1f} {ty:.1f}) scale({scale:.4f})"'
            f' fill="{fill}" opacity="{opacity}">\n' + "".join(body) + '  </g>\n')


def build(background, glyph, domain="jeffols.com"):
    lock_size = 74
    d, text_w, cap = outline("Jeff Olsen", WORDMARK_FONT, lock_size)
    mark_scale = (cap * 2.15) / MARK_H
    mw, mh = MARK_W * mark_scale, MARK_H * mark_scale

    pad = 96
    baseline = 300 + mh / 2 + cap / 2
    mark_tx = pad - MARK_BOX[0] * mark_scale
    mark_ty = 300 - MARK_BOX[1] * mark_scale
    text_tx = pad + mw + lock_size * 0.42

    dom_d, _, _ = outline(domain, WORDMARK_FONT, 30)

    # Background echo: sized and placed by the GLYPH box, not the 1024 canvas.
    # Scaling the canvas cropped so hard that only disconnected fragments showed,
    # which breaks the section 14 requirement that the naked geometry stay
    # recoverable inside the echoes. Whole mark, large, slight bleed right.
    bg_scale = 0.75
    glyph_h = MARK_H * bg_scale
    bg_tx = (W - 330) - MARK_BOX[0] * bg_scale
    bg_ty = (H - glyph_h) / 2 - MARK_BOX[1] * bg_scale

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"
     width="{W}" height="{H}" role="img" aria-label="Jeff Olsen — jeffols.com">
  <rect width="{W}" height="{H}" fill="{background}"/>
{rotational_group(bg_scale, bg_tx, bg_ty, glyph, 0.13)}  <g transform="translate({mark_tx:.2f} {mark_ty:.2f}) scale({mark_scale:.5f})" fill="{glyph}">
{svg_shapes(indent="    ")}  </g>
  <path transform="translate({text_tx:.2f} {baseline:.2f})" d="{d}" fill="{glyph}"/>
  <path transform="translate({pad} {H - 84})" d="{dom_d}" fill="{glyph}" opacity="0.55"/>
  <line x1="0" y1="0.5" x2="{W}" y2="0.5" stroke="{glyph}" stroke-width="1" opacity="0.10"/>
  <line x1="0" y1="{H - 0.5}" x2="{W}" y2="{H - 0.5}" stroke="{glyph}" stroke-width="1" opacity="0.10"/>
</svg>
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--palette", default="signal_yellow", choices=list(PALETTES))
    p.add_argument("--mode", default="dark", choices=["dark", "light", "both"])
    p.add_argument("--out", default=str(REPO / "assets" / "social"))
    a = p.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()
    tmp = out / "_tmp.html"

    for mode in ([m for m in modes_for(a.palette)] if a.mode == "both" else [a.mode]):
        c = PALETTES[a.palette][mode]
        svg = build(c["background"], c["glyph"])
        stem = f"social-{a.palette}-{mode}"
        (out / f"{stem}.svg").write_text(svg, encoding="utf-8")

        for w, h in SIZES:
            tmp.write_text(
                f'<!doctype html><meta charset="utf-8">'
                f'<style>*{{margin:0;padding:0}}body{{width:{w}px;height:{h}px;'
                f'overflow:hidden}}svg{{width:{w}px;height:{h}px;display:block}}</style>'
                f"{svg}", encoding="utf-8")
            png = out / f"{stem}-{w}x{h}.png"
            subprocess.run([chrome, "--headless", "--disable-gpu",
                            f"--screenshot={png}", f"--window-size={w},{h}",
                            f"file://{tmp.resolve()}"],
                           capture_output=True, timeout=30)
            if not png.exists() or png.stat().st_size == 0:
                raise SystemExit(f"Chrome produced no output for {png}")
            print(f"  {png.name}")

    tmp.unlink(missing_ok=True)
    (out / "README.md").write_text(
        "# Social preview\n\n"
        "Generated by `scripts/generate_social.py`. Do not edit by hand.\n\n"
        "`*-1200x630.png` is the Open Graph size every major platform crops to. "
        "Point `og:image` and `twitter:image` at it.\n\n"
        "Almost no text by design: the final homepage headline is still open "
        "(BRAND.md section 23), and a tagline baked into an OG image goes stale "
        "the day it changes.\n",
        encoding="utf-8")
    print(f"Social previews in {out}")


if __name__ == "__main__":
    main()
