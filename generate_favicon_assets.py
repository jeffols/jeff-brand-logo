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
DESIGN_SIZE = 1024
DEFAULT_SIZES = [16, 32, 48, 64, 128, 180, 192, 256, 512]
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


def quad_bezier(p0, p1, p2, steps=16):
    points = []
    for i in range(1, steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        points.append((x, y))
    return points


def hook_polygon(s):
    pts = [(500 * s, 640 * s), (660 * s, 640 * s), (660 * s, 720 * s)]
    pts += quad_bezier((660 * s, 720 * s), (660 * s, 860 * s), (520 * s, 860 * s))
    pts.append((370 * s, 860 * s))
    pts += quad_bezier((370 * s, 860 * s), (280 * s, 860 * s), (280 * s, 780 * s))
    pts.append((280 * s, 750 * s))
    pts += quad_bezier((280 * s, 750 * s), (280 * s, 710 * s), (330 * s, 710 * s))
    pts.append((410 * s, 710 * s))
    pts += quad_bezier((410 * s, 710 * s), (500 * s, 710 * s), (500 * s, 640 * s))
    return [(round(x), round(y)) for x, y in pts]


def render_icon(size, background, glyph, rounded=True):
    """Render the mark at `size`.

    rounded=True gives the favicon form: a rounded-rect plate on a transparent
    canvas. Browsers render favicons as-is and want that shape.

    rounded=False gives the avatar form: a full-bleed opaque square with no alpha
    anywhere. Social platforms (Substack, LinkedIn, GitHub) apply their own corner
    mask, so a pre-rounded asset fights theirs, and any transparency left in the
    corners gets flattened to whatever the platform assumes. Substack assumes
    white, which is why a pre-rounded upload shows white slivers at the corners.
    """
    render_size = size * SUPERSAMPLE
    s = render_size / DESIGN_SIZE
    bg = hex_to_rgba(background)
    gl = hex_to_rgba(glyph)

    img = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if rounded:
        r = max(1, round(174 * s))
        draw.rounded_rectangle([0, 0, render_size - 1, render_size - 1], radius=r, fill=bg)
    else:
        draw.rectangle([0, 0, render_size - 1, render_size - 1], fill=bg)

    dx, dy, dw, dh = round(400 * s), round(120 * s), round(140 * s), round(140 * s)
    draw.ellipse([dx, dy, dx + dw, dy + dh], fill=gl)

    sx, sy, sw, sh = round(460 * s), round(340 * s), round(160 * s), round(280 * s)
    sr = max(1, round(6 * s))
    draw.rounded_rectangle([sx, sy, sx + sw, sy + sh], radius=sr, fill=gl)

    draw.polygon(hook_polygon(s), fill=gl)

    out = img.resize((size, size), Image.Resampling.LANCZOS)
    if not rounded:
        # Drop the alpha channel entirely so no platform can flatten it wrongly.
        out = out.convert("RGB")
    return out


def build_svg(background, glyph, size=1024, rounded=True):
    """SVG twin of render_icon. Keep the geometry here in sync with it."""
    rx = round(size * 0.17) if rounded else 0
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"'
        f' role="img" aria-label="jeffols signature icon">\n'
        f'  <rect width="{size}" height="{size}" rx="{rx}" fill="{background}"/>\n'
        f'  <rect x="400" y="120" width="140" height="140" rx="70" fill="{glyph}"/>\n'
        f'  <rect x="460" y="340" width="160" height="280" rx="6" fill="{glyph}"/>\n'
        f'  <path d="M 500 640 H 660 V 720 Q 660 860 520 860 H 370'
        f' Q 280 860 280 780 V 750 Q 280 710 330 710 H 410'
        f' Q 500 710 500 640 Z" fill="{glyph}"/>\n'
        f'</svg>\n'
    )


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
    args = parser.parse_args()

    if args.list_palettes:
        list_palettes()
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
