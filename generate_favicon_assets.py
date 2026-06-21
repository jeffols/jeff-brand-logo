#!/usr/bin/env python3
"""
Generate favicon/app-icon assets from the selected source icon.

SVG behavior:
- SVG fills are written inline: fill="#FFD60A"
- No CSS variables
- No <style> dependency

Dependencies:
    pip install pillow opencv-python numpy

Examples:
    python generate_favicon_assets.py --source source_icon.png --out ./out
    python generate_favicon_assets.py --source source_icon.png --out ./out --palette signal_yellow --mode both
    python generate_favicon_assets.py --source source_icon.png --out ./out --palette all --mode both
    python generate_favicon_assets.py --source source_icon.png --out ./out --background "#111827" --glyph "#FFD60A"
    python generate_favicon_assets.py --list-palettes
"""

from pathlib import Path
from PIL import Image
import numpy as np
import cv2
import argparse
import json

PALETTES = {
    "signal_yellow": {
        "label": "Signal Yellow",
        "dark":  {"background": "#111827", "glyph": "#FFD60A"},
        "light": {"background": "#FFF7E0", "glyph": "#B8960A"},
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
    "slate_mono": {
        "label": "Slate Mono",
        "dark":  {"background": "#0F172A", "glyph": "#F8FAFC"},
        "light": {"background": "#F8FAFC", "glyph": "#0F172A"},
    },
}
DEFAULT_SIZES = [16, 32, 48, 64, 128, 180, 192, 256, 512]

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

def extract_masks(source_path):
    img = Image.open(source_path).convert("RGBA")
    arr = np.array(img)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    white = (rgb[:, :, 0] > 238) & (rgb[:, :, 1] > 238) & (rgb[:, :, 2] > 238)
    icon_mask_np = (~white & (alpha > 0)).astype(np.uint8) * 255

    glyph_mask_np = ((rgb[:, :, 0] > 175) & (rgb[:, :, 1] > 125) & (rgb[:, :, 2] < 90) & (alpha > 0)).astype(np.uint8) * 255

    kernel = np.ones((3, 3), np.uint8)
    icon_mask_np = cv2.morphologyEx(icon_mask_np, cv2.MORPH_CLOSE, kernel)
    glyph_mask_np = cv2.morphologyEx(glyph_mask_np, cv2.MORPH_CLOSE, kernel)

    return Image.fromarray(icon_mask_np, "L"), Image.fromarray(glyph_mask_np, "L"), glyph_mask_np

def render_from_masks(size, icon_mask, glyph_mask, background, glyph):
    imask = icon_mask.resize((size, size), Image.Resampling.LANCZOS)
    gmask = glyph_mask.resize((size, size), Image.Resampling.LANCZOS)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bg_layer = Image.new("RGBA", (size, size), hex_to_rgba(background))
    glyph_layer = Image.new("RGBA", (size, size), hex_to_rgba(glyph))

    out = Image.composite(bg_layer, out, imask)
    out = Image.composite(glyph_layer, out, gmask)
    return out

def contour_to_svg_paths(mask_np, glyph, size=1024, simplify=2.2):
    contours, _ = cv2.findContours(mask_np, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    h, w = mask_np.shape
    pieces = []
    contours = sorted(contours, key=lambda c: (cv2.boundingRect(c)[1], cv2.boundingRect(c)[0]))
    for c in contours:
        if cv2.contourArea(c) < 100:
            continue
        approx = cv2.approxPolyDP(c, simplify, True)
        pts = approx.reshape(-1, 2)
        sx, sy = size / w, size / h
        d = [f"M {pts[0][0]*sx:.2f} {pts[0][1]*sy:.2f}"]
        for x, y in pts[1:]:
            d.append(f"L {x*sx:.2f} {y*sy:.2f}")
        d.append("Z")
        pieces.append(f'<path d="{" ".join(d)}" fill="{glyph}"/>')
    return "\n  ".join(pieces)

def build_svg(glyph_mask_np, background, glyph, size=1024):
    paths = contour_to_svg_paths(glyph_mask_np, glyph, size=size)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" role="img" aria-label="Abstract signature icon">',
        f'  <rect x="0" y="0" width="{size}" height="{size}" rx="{size * 0.17:.0f}" fill="{background}"/>',
        f'  {paths}',
        '</svg>',
        ''
    ]
    return "\n".join(lines)

def parse_sizes(value):
    return [int(x.strip()) for x in value.split(",") if x.strip()]

def write_assets(out_dir, icon_mask, glyph_mask, glyph_mask_np, palette_key, mode, background, glyph, sizes):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    svg_name = f"signature-{palette_key}-{mode}.svg"
    (out_dir / svg_name).write_text(build_svg(glyph_mask_np, background, glyph), encoding="utf-8")

    for size in sizes:
        render_from_masks(size, icon_mask, glyph_mask, background, glyph).save(out_dir / f"favicon-{size}x{size}.png")

    render_from_masks(16, icon_mask, glyph_mask, background, glyph).save(out_dir / "favicon-16x16.png")
    render_from_masks(32, icon_mask, glyph_mask, background, glyph).save(out_dir / "favicon-32x32.png")
    render_from_masks(180, icon_mask, glyph_mask, background, glyph).save(out_dir / "apple-touch-icon.png")
    render_from_masks(192, icon_mask, glyph_mask, background, glyph).save(out_dir / "android-chrome-192x192.png")
    render_from_masks(512, icon_mask, glyph_mask, background, glyph).save(out_dir / "android-chrome-512x512.png")

    ico = render_from_masks(512, icon_mask, glyph_mask, background, glyph)
    ico.save(out_dir / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    manifest = {
        "name": "Signature App Icon",
        "short_name": "Signature",
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
        print(f"{key}: {palette['label']}")
        for mode in ["dark", "light"]:
            c = palette[mode]
            print(f"  {mode}: background {c['background']} glyph {c['glyph']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="source_icon.png")
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
    source = Path(args.source)
    out = Path(args.out)
    icon_mask, glyph_mask, glyph_mask_np = extract_masks(source)

    if args.background or args.glyph:
        if not (args.background and args.glyph):
            raise SystemExit("For custom colors, provide both --background and --glyph.")
        background = normalize_hex(args.background)
        glyph = normalize_hex(args.glyph)
        write_assets(out, icon_mask, glyph_mask, glyph_mask_np, "custom", "custom", background, glyph, sizes)
        print(f"Generated custom assets in {out}")
        return

    palette_keys = list(PALETTES.keys()) if args.palette == "all" else [args.palette]
    modes = ["dark", "light"] if args.mode == "both" else [args.mode]

    for palette_key in palette_keys:
        for mode in modes:
            colors = PALETTES[palette_key][mode]
            target = out
            if args.palette == "all":
                target = out / palette_key / mode
            elif args.mode == "both":
                target = out / mode

            write_assets(
                target,
                icon_mask,
                glyph_mask,
                glyph_mask_np,
                palette_key,
                mode,
                colors["background"],
                colors["glyph"],
                sizes,
            )
            print(f"Generated {palette_key} {mode} assets in {target}")

if __name__ == "__main__":
    main()
