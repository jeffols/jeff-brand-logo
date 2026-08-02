#!/usr/bin/env python3
"""
Generate favicon/app-icon assets for the jeffols tectonic j mark.

The icon is a geometric lowercase j split into three offset pieces:
dot (circle, shifted left), stem (rectangle, centered), hook (curved, shifted right).

Dependencies:
    pip install pillow

Examples:
    python generate_favicon_assets.py --out ./out
    python generate_favicon_assets.py --out ./out --palette signal_yellow --mode both
    python generate_favicon_assets.py --out ./out --palette all --mode both
    python generate_favicon_assets.py --out ./out --background "#111827" --glyph "#FFD60A"
    python generate_favicon_assets.py --list-palettes
"""

from pathlib import Path
from PIL import Image, ImageDraw
import argparse
import json

import geometry
from geometry import DESIGN_SIZE, quad_bezier, svg_document

# Every palette but signal_yellow puts its colour in the glyph and its neutral in
# the plate. signal_yellow light inverts that (decision 0004): the plate carries
# the yellow and the glyph is the dark navy. A dark yellow glyph is an olive, and
# an olive on cream is amber_utility — there was no room for both. Inverting keeps
# the same two colours, the same 12.57:1, and no collision.
#
# The matrix is not guaranteed symmetric. Use modes_for() / resolve_modes() rather
# than assuming both keys exist.
PALETTES = {
    "signal_yellow": {
        "label": "Signal Yellow",
        "dark":  {"background": "#111827", "glyph": "#FFD60A"},
        "light": {"background": "#FFD60A", "glyph": "#111827"},
    },
    "electric_blue": {
        "label": "Electric Blue",
        "dark":  {"background": "#0B1020", "glyph": "#7DD3FC"},
        "light": {"background": "#F6FBFF", "glyph": "#005A9C"},
    },
    "amber_utility": {
        "label": "Amber Utility",
        "dark":  {"background": "#1F1B16", "glyph": "#FFB000"},
        "light": {"background": "#FFF8E1", "glyph": "#8B5E00"},
    },
    "terminal_lime": {
        "label": "Terminal Lime",
        "dark":  {"background": "#151515", "glyph": "#B6FF4D"},
        "light": {"background": "#F7FFE8", "glyph": "#3D6600"},
    },
    "deep_indigo": {
        "label": "Deep Indigo",
        "dark":  {"background": "#190A24", "glyph": "#DDB0FF"},
        "light": {"background": "#FBF5FF", "glyph": "#4B0082"},
    },
    "slate_mono": {
        "label": "Slate Mono",
        "dark":  {"background": "#0F172A", "glyph": "#F8FAFC"},
        "light": {"background": "#F8FAFC", "glyph": "#0F172A"},
    },
}
DEFAULT_SIZES = [16, 24, 32, 48, 64, 80, 128, 180, 192, 256, 512]
SUPERSAMPLE = 4
MODES = ("dark", "light")


def modes_for(palette_key):
    """Modes this palette actually defines, in canonical order."""
    return [m for m in MODES if m in PALETTES[palette_key]]


def resolve_modes(palette_key, requested):
    """Modes to generate, and whether an explicit request was unsatisfiable.

    `--mode both` quietly skips a mode a palette does not define. Naming that
    mode explicitly is an error, because silently producing nothing is worse
    than saying why.
    """
    available = modes_for(palette_key)
    if requested == "both":
        return available
    if requested not in available:
        raise SystemExit(
            f"{palette_key} has no {requested} mode "
            f"(available: {', '.join(available)}). See docs/decisions/0003."
        )
    return [requested]


def hex_to_rgba(value):
    value = value.strip().lstrip("#")
    if len(value) != 6:
        raise ValueError(f"Expected 6-digit hex color, got {value}")
    return tuple(int(value[i:i+2], 16) for i in (0, 2, 4)) + (255,)


def normalize_hex(value):
    value = value.strip()
    if not value.startswith("#"):
        value = "#" + value
    hex_to_rgba(value)
    return value.upper()


def render_icon(size, background, glyph, rounded=True):
    """Render the mark at `size`. Geometry comes from geometry.py.

    rounded=True gives the favicon form: a rounded-rect plate on a transparent
    canvas. Browsers render favicons as-is and want that shape.

    rounded=False gives the avatar form: a full-bleed opaque square with no alpha
    anywhere. Social platforms (Substack, LinkedIn, GitHub) apply their own corner
    mask, so a pre-rounded asset fights theirs, and any transparency left in the
    corners gets flattened to whatever the platform assumes. Substack assumes
    white, which is why a pre-rounded upload shows white slivers at the corners.

    background=None omits the plate: a bare glyph on transparency.
    """
    render_size = size * SUPERSAMPLE
    s = render_size / DESIGN_SIZE
    gl = hex_to_rgba(glyph)

    img = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if background is not None:
        bg = hex_to_rgba(background)
        if rounded:
            draw.rounded_rectangle([0, 0, render_size - 1, render_size - 1],
                                   radius=max(1, round(geometry.PLATE_RADIUS * s)),
                                   fill=bg)
        else:
            draw.rectangle([0, 0, render_size - 1, render_size - 1], fill=bg)

    draw.ellipse(geometry.dot_box(s), fill=gl)
    box, radius = geometry.stem_box(s)
    draw.rounded_rectangle(box, radius=radius, fill=gl)
    draw.polygon(geometry.hook_polygon(s, steps=16, snap=True), fill=gl)

    out = img.resize((size, size), Image.Resampling.LANCZOS)
    if not rounded and background is not None:
        # Drop the alpha channel entirely so no platform can flatten it wrongly.
        out = out.convert("RGB")
    return out


def build_svg(background, glyph, size=DESIGN_SIZE, rounded=True):
    """SVG twin of render_icon. Both now read the same geometry module, so the
    two cannot drift. background=None omits the plate."""
    return svg_document(background, glyph, size=size, rounded=rounded)


def parse_sizes(value):
    return [int(x.strip()) for x in value.split(",") if x.strip()]


def write_assets(out_dir, palette_key, mode, background, glyph, sizes):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    svg_name = f"signature-{palette_key}-{mode}.svg"
    (out_dir / svg_name).write_text(build_svg(background, glyph), encoding="utf-8")

    # Avatar form: full-bleed opaque square, no rounding, no alpha. Upload this to
    # Substack, LinkedIn, GitHub and let each apply its own corner mask.
    avatar_svg = f"avatar-{palette_key}-{mode}.svg"
    (out_dir / avatar_svg).write_text(
        build_svg(background, glyph, rounded=False), encoding="utf-8"
    )
    for avatar_size in (512, 1024):
        render_icon(avatar_size, background, glyph, rounded=False).save(
            out_dir / f"avatar-{avatar_size}x{avatar_size}.png"
        )

    # Transparent form: the glyph alone, no plate, for headers, footers, print,
    # and anywhere the surface supplies its own background. Choose the variant
    # matching the PAGE rather than your other assets — a dark-mode glyph on a
    # light page falls under 2:1. See docs/accessibility.md.
    (out_dir / f"mark-{palette_key}-{mode}.svg").write_text(
        build_svg(None, glyph, rounded=False), encoding="utf-8")
    for mark_size in (512, 1024):
        render_icon(mark_size, None, glyph).save(
            out_dir / f"mark-{mark_size}x{mark_size}.png")

    for size in sizes:
        render_icon(size, background, glyph).save(out_dir / f"favicon-{size}x{size}.png")

    render_icon(180, background, glyph).save(out_dir / "apple-touch-icon.png")
    render_icon(192, background, glyph).save(out_dir / "android-chrome-192x192.png")
    render_icon(512, background, glyph).save(out_dir / "android-chrome-512x512.png")

    render_icon(256, background, glyph).save(
        out_dir / "favicon.ico",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )

    manifest = {
        "name": "jeffols",
        "short_name": "jeffols",
        "icons": [
            {"src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": background,
        "background_color": background,
        "display": "standalone",
    }
    (out_dir / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    metadata = {
        "palette": palette_key,
        "mode": mode,
        "background": background,
        "glyph": glyph,
        "sizes": sizes,
        "svg": svg_name,
        "svg_compatibility": "inline fill colors; no CSS variables",
    }
    (out_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


# Palette-independent canonical marks. These carry no palette, so they live
# outside the palettes tree — see decision 0001 on where each form belongs.
MONO_VARIANTS = [
    ("mark-mono", "currentColor", "inherits colour from the surrounding CSS"),
    ("mark-black", "#000000", "print, engraving, embroidery, single-colour"),
    ("mark-white", "#FFFFFF", "knockout on any dark surface"),
]


def write_canonical_marks(out_dir, renderer=None, label="jeffols mark",
                          svg_builder=None):
    """The mark with no plate and no palette: monochrome and currentColor.

    BRAND.md section 20 asks for a monochrome SVG and a print-ready vector. This
    is both. currentColor cannot be rasterised, so only the concrete fills get
    PNGs.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    renderer = renderer or (lambda size, fill: render_icon(size, None, fill))
    svg_builder = svg_builder or (
        lambda fill: svg_document(None, fill, rounded=False, label=label))

    written = []
    for name, fill, note in MONO_VARIANTS:
        (out_dir / f"{name}.svg").write_text(svg_builder(fill), encoding="utf-8")
        written.append(f"{name}.svg")
        if fill != "currentColor":
            renderer(1024, fill).save(out_dir / f"{name}-1024.png")
            written.append(f"{name}-1024.png")

    (out_dir / "README.md").write_text(
        "# Canonical marks\n\n"
        "Palette-independent. No plate, no background, transparent everywhere.\n\n"
        + "".join(f"- `{n}.svg` — {note}\n" for n, _, note in MONO_VARIANTS)
        + "\nGenerated. Do not edit by hand; regenerate with `--canonical`.\n",
        encoding="utf-8")
    return written


WATERMARK_TEMPLATE = """/*
 * Signature Watermark — bottom-right page mark
 *
 * GENERATED by generate_favicon_assets.py --watermark. Do not edit by hand:
 * the data URI below is built from geometry.py, so a geometry change reaches
 * this file only by regenerating it.
 *
 * Usage:
 *   <link rel="stylesheet" href="watermark.css">
 *
 * Customization:
 *   --watermark-size     Icon size (default: 32px)
 *   --watermark-opacity  Opacity 0-1 (default: 0.18)
 *   --watermark-offset   Distance from corner (default: 16px)
 *
 *   body {{ --watermark-size: 48px; --watermark-opacity: 0.25; }}
 *
 * To hide: body {{ --watermark-opacity: 0; }}
 *
 * Palette: {palette} {mode} — plate {background}, glyph {glyph}
 */

body::after {{
  content: "";
  position: fixed;
  bottom: var(--watermark-offset, 16px);
  right: var(--watermark-offset, 16px);
  width: var(--watermark-size, 32px);
  height: var(--watermark-size, 32px);
  opacity: var(--watermark-opacity, 0.18);
  pointer-events: none;
  z-index: 9999;
  background-image: url("{uri}");
  background-size: contain;
  background-repeat: no-repeat;
}}

@media print {{
  body::after {{
    position: fixed;
    opacity: var(--watermark-opacity, 0.12);
  }}
}}
"""


def write_watermark(path, palette_key="signal_yellow", mode="dark"):
    """Regenerate watermark.css from canonical geometry.

    This file used to carry a hand-written copy of the mark, which made it one
    of the seventeen places the geometry lived.
    """
    c = PALETTES[palette_key][mode]
    Path(path).write_text(WATERMARK_TEMPLATE.format(
        palette=palette_key, mode=mode,
        background=c["background"], glyph=c["glyph"],
        uri=geometry.data_uri(c["background"], c["glyph"]),
    ), encoding="utf-8")


def list_palettes():
    for key, palette in PALETTES.items():
        available = modes_for(key)
        suffix = "" if len(available) == len(MODES) else f"  ({available[0]}-only)"
        print(f"{key}: {palette['label']}{suffix}")
        for mode in available:
            c = palette[mode]
            print(f"  {mode}: background {c['background']} glyph {c['glyph']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="favicon_output")
    parser.add_argument("--palette", default="signal_yellow", choices=list(PALETTES.keys()) + ["all"])
    parser.add_argument("--mode", default="dark", choices=["dark", "light", "both"])
    parser.add_argument("--background", help="Custom background color, e.g. #111827")
    parser.add_argument("--glyph", help="Custom glyph color, e.g. #FFD60A")
    parser.add_argument("--sizes", default=",".join(str(s) for s in DEFAULT_SIZES))
    parser.add_argument("--list-palettes", action="store_true")
    parser.add_argument("--canonical", metavar="DIR",
                        help="write the palette-independent monochrome marks "
                             "to DIR and exit, e.g. assets/marks/primary")
    parser.add_argument("--watermark", metavar="PATH",
                        help="regenerate the CSS watermark at PATH and exit")
    args = parser.parse_args()

    if args.list_palettes:
        list_palettes()
        return

    if args.canonical:
        for name in write_canonical_marks(args.canonical):
            print(f"  {name}")
        print(f"Canonical marks in {args.canonical}")
        return

    if args.watermark:
        write_watermark(args.watermark)
        print(f"Wrote {args.watermark}")
        return

    sizes = parse_sizes(args.sizes)
    out = Path(args.out)

    if args.background or args.glyph:
        if not (args.background and args.glyph):
            raise SystemExit("For custom colors, provide both --background and --glyph.")
        background = normalize_hex(args.background)
        glyph = normalize_hex(args.glyph)
        write_assets(out, "custom", "custom", background, glyph, sizes)
        print(f"Generated custom assets in {out}")
        return

    palette_keys = list(PALETTES.keys()) if args.palette == "all" else [args.palette]

    for palette_key in palette_keys:
        for mode in resolve_modes(palette_key, args.mode):
            colors = PALETTES[palette_key][mode]
            target = out
            if args.palette == "all":
                target = out / palette_key / mode
            elif args.mode == "both":
                target = out / mode

            write_assets(target, palette_key, mode, colors["background"], colors["glyph"], sizes)
            print(f"Generated {palette_key} {mode} assets in {target}")


if __name__ == "__main__":
    main()
