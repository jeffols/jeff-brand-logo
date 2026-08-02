#!/usr/bin/env python3
"""
Rotational depth-stack exploration for the tectonic j.

Stacks N copies of the mark, each rotated by a fixed step, and ramps opacity so
the back of the stack is nearly invisible and the front copy is fully opaque.
Reads as depth: the mark spiralling toward the viewer.

Geometry comes from geometry.py, which is the single source of truth for the
mark. Nothing here redefines a coordinate; this module owns only the stack.

Dependencies:
    pip install pillow

Examples:
    python generate_rotational_logo.py --out ./explorations/rotational
    python generate_rotational_logo.py --out ./out --step 45 --layers 8
    python generate_rotational_logo.py --out ./out --sheet
"""

from pathlib import Path
from PIL import Image, ImageDraw
import argparse
import json
import math

import geometry
from geometry import DESIGN_SIZE, glyph_polygons, plate_radius, svg_shapes
from generate_favicon_assets import (
    DEFAULT_SIZES, PALETTES, hex_to_rgba, parse_sizes, resolve_modes,
    write_canonical_marks,
)

SUPERSAMPLE = 4

# Outputs are anchored to the repo, not the CWD, so the scripts behave the
# same whether run from the root or from scripts/.
REPO = Path(__file__).resolve().parent.parent
PIVOT = (512.0, 512.0)          # rotate about the plate centre, not the glyph bbox
GLYPH_PIVOT = (470.0, 490.0)    # glyph bounding-box centre, for a tighter sweep

# Neutral starting point for exploring the parameter space. Not a brand asset.
BASE = {"layers": 8, "step": 8.0, "min_opacity": 0.10, "gamma": 1.8, "scale_step": 0.02}

# Named settings worth keeping. Opt in with --preset; individual flags still win.
# The plates-* family are all near neighbours of "plates": each moves one axis
# only, so a side-by-side comparison isolates what that axis actually buys.
PRESETS = {
    "plates": {
        "label": "CANONICAL — one clear echo, one faint trace, solid mark in front",
        "note": "decision 0002; the 3-layer original",
        "layers": 3, "step": 6.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": 0.06,
    },
    "plates-4": {
        "label": "One more layer, which buys density not legibility",
        "note": "rejected in 0002; the rear two merge into a single wider shadow",
        "layers": 4, "step": 6.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": 0.06,
    },
    "plates-even": {
        "label": "Middle plate reads as its own plate",
        "note": "falloff 3.0 -> 0.8, so the echo stops being a ghost",
        "layers": 3, "step": 6.0, "min_opacity": 0.08, "gamma": 0.8, "scale_step": 0.06,
    },
    "plates-tight": {
        "label": "Narrower fan",
        "note": "step 6 -> 4 degrees",
        "layers": 3, "step": 4.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": 0.06,
    },
    "plates-wide": {
        "label": "More separation between plates",
        "note": "step 6 -> 9 degrees",
        "layers": 3, "step": 9.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": 0.06,
    },
    "plates-flat": {
        "label": "Pure rotation, no perspective",
        "note": "recession 0.06 -> 0, plates stay the same size",
        "layers": 3, "step": 6.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": 0.0,
    },
    "plates-bloom": {
        "label": "Rear plates larger, blooming outward",
        "note": "recession 0.06 -> -0.025",
        "layers": 3, "step": 6.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": -0.025,
    },
    "plates-deep": {
        "label": "One more echo in the stack",
        "note": "layers 3 -> 4",
        "layers": 4, "step": 6.0, "min_opacity": 0.08, "gamma": 3.0, "scale_step": 0.06,
    },
}
PRESET_KEYS = [k for k in PRESETS]

# Opacity ramps, orthogonal to the geometry presets. Compose them:
#   --preset plates-wide --layers 4 --fade even
#
# Why the floor matters more than the curve: a layer at alpha a composites to
# bg + a*(glyph - bg). On a dark plate with a bright glyph, anything under about
# 0.15 lands in a muddy near-background olive that the eye reads as noise rather
# than as a plate. Lifting min_opacity is what makes the stack legible; gamma
# only decides how the remaining headroom is distributed.
FADES = {
    "whisper": {"label": "Barely-there ghost", "min_opacity": 0.08, "gamma": 3.0},
    "soft":    {"label": "Visible but clearly secondary", "min_opacity": 0.18, "gamma": 1.6},
    "even":    {"label": "Evenly spaced ladder", "min_opacity": 0.28, "gamma": 1.0},
    "graded":  {"label": "Even to the eye, not to the maths", "min_opacity": 0.26, "gamma": 1.45},
    "strong":  {"label": "Near-solid plates", "min_opacity": 0.40, "gamma": 0.8},
}
FADE_KEYS = [k for k in FADES]


def resolve(preset, fade, overrides):
    """BASE < preset < fade < explicit flags."""
    cfg = dict(BASE)
    if preset:
        cfg.update({k: v for k, v in PRESETS[preset].items()
                    if k not in ("label", "note")})
    if fade:
        cfg.update({k: v for k, v in FADES[fade].items() if k != "label"})
    cfg.update({k: v for k, v in overrides.items() if v is not None})
    return cfg


def ramp(cfg):
    """The actual per-layer opacities, for reporting."""
    return [o for _, o, _ in layer_specs(cfg["layers"], cfg["step"], cfg["min_opacity"],
                                         cfg["gamma"], cfg["scale_step"], PIVOT)]


# --------------------------------------------------------------------------
# The glyph arrives from geometry.py as pure polygons, so it can be rotated and
# scaled exactly rather than resampled. Pillow cannot rotate an ellipse or a
# rounded_rectangle in place, which is why this path exists at all.
# --------------------------------------------------------------------------

def glyph_parts():
    """The three pieces of the mark in 1024x1024 design space."""
    return glyph_polygons()


# --------------------------------------------------------------------------
# Stack parameters
# --------------------------------------------------------------------------

def layer_specs(layers, step, min_opacity, gamma, scale_step, pivot):
    """Back-to-front list of (angle_cw_degrees, opacity, scale).

    Layer index 0 is furthest back. The front layer sits at 0 degrees and full
    opacity so the canonical upright mark always stays legible; everything
    behind it is a fading, rotated echo.
    """
    specs = []
    for i in range(layers):
        depth = layers - 1 - i                        # 0 = frontmost
        t = i / (layers - 1) if layers > 1 else 1.0
        opacity = min_opacity + (1.0 - min_opacity) * (t ** gamma)
        specs.append((depth * step, opacity, 1.0 - depth * scale_step))
    return specs


def transform(pts, angle_cw, scale, pivot):
    """Scale about pivot, then rotate clockwise about pivot (SVG convention)."""
    a = math.radians(angle_cw)
    ca, sa = math.cos(a), math.sin(a)
    px, py = pivot
    out = []
    for x, y in pts:
        x = px + (x - px) * scale
        y = py + (y - py) * scale
        dx, dy = x - px, y - py
        out.append((px + dx * ca - dy * sa, py + dx * sa + dy * ca))
    return out


# --------------------------------------------------------------------------
# Raster
# --------------------------------------------------------------------------

def render_stack(size, background, glyph, layers=8, step=8.0, min_opacity=0.10,
                 gamma=1.8, scale_step=0.02, pivot=PIVOT, rounded=True):
    render_size = size * SUPERSAMPLE
    s = render_size / DESIGN_SIZE
    bg = hex_to_rgba(background) if background is not None else None
    gl = hex_to_rgba(glyph)

    base = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(base)
    if background is not None:
        if rounded:
            draw.rounded_rectangle([0, 0, render_size - 1, render_size - 1],
                                   radius=max(1, round(geometry.PLATE_RADIUS * s)),
                                   fill=bg)
        else:
            draw.rectangle([0, 0, render_size - 1, render_size - 1], fill=bg)

    parts = glyph_parts()
    for angle, opacity, scale in layer_specs(layers, step, min_opacity, gamma,
                                             scale_step, pivot):
        layer = Image.new("RGBA", (render_size, render_size), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        fill = gl[:3] + (round(255 * opacity),)
        for part in parts:
            ld.polygon([(x * s, y * s) for x, y in transform(part, angle, scale, pivot)],
                       fill=fill)
        base = Image.alpha_composite(base, layer)

    out = base.resize((size, size), Image.Resampling.LANCZOS)
    if background is None:
        return out                      # transparent: keep the alpha channel
    return out if rounded else out.convert("RGB")


# --------------------------------------------------------------------------
# SVG
# --------------------------------------------------------------------------

SHAPES = svg_shapes(indent="    ")


def build_svg(background, glyph, layers=8, step=8.0, min_opacity=0.10, gamma=1.8,
              scale_step=0.02, pivot=PIVOT, rounded=True, spin_seconds=None):
    size = DESIGN_SIZE
    rx = plate_radius(size) if rounded else 0
    px, py = pivot
    body = []
    for angle, opacity, scale in layer_specs(layers, step, min_opacity, gamma,
                                             scale_step, pivot):
        tf = (f'rotate({angle:g} {px:g} {py:g}) '
              f'translate({px:g} {py:g}) scale({scale:.4f}) translate({-px:g} {-py:g})')
        body.append(f'  <g transform="{tf}" opacity="{opacity:.3f}">\n{SHAPES}  </g>\n')

    stack = "".join(body)
    if spin_seconds:
        stack = (
            f'  <g>\n'
            f'    <animateTransform attributeName="transform" type="rotate"'
            f' from="0 {px:g} {py:g}" to="360 {px:g} {py:g}"'
            f' dur="{spin_seconds}s" repeatCount="indefinite"/>\n'
            + stack + '  </g>\n'
        )

    plate = (f'  <rect width="{size}" height="{size}" rx="{rx}"'
             f' fill="{background}"/>\n' if background is not None else "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"'
        f' role="img" aria-label="jeffols rotational mark">\n'
        f'{plate}'
        f'  <g fill="{glyph}">\n{stack}  </g>\n'
        f'</svg>\n'
    )


# --------------------------------------------------------------------------
# Contact sheet
# --------------------------------------------------------------------------

SHEET_STEPS = [3, 6, 10, 15, 22.5, 45]


def write_sheet(out_dir, palette_key, mode, background, glyph, layers,
                min_opacity, gamma, scale_step, pivot):
    cards = []
    for step in SHEET_STEPS:
        name = f"rot-{palette_key}-{mode}-step{str(step).replace('.', '_')}"
        svg = build_svg(background, glyph, layers, step, min_opacity, gamma,
                        scale_step, pivot)
        (out_dir / f"{name}.svg").write_text(svg, encoding="utf-8")
        render_stack(512, background, glyph, layers, step, min_opacity, gamma,
                     scale_step, pivot).save(out_dir / f"{name}.png")
        render_stack(32, background, glyph, layers, step, min_opacity, gamma,
                     scale_step, pivot).save(out_dir / f"{name}-32.png")
        cards.append(
            f'<figure><img src="{name}.png" alt="step {step}">'
            f'<figcaption>{step}&deg; step '
            f'<img class="tiny" src="{name}-32.png" alt="32px"></figcaption></figure>'
        )

    spin = build_svg(background, glyph, layers, 8, min_opacity, gamma,
                     scale_step, pivot, spin_seconds=9)
    (out_dir / f"rot-{palette_key}-{mode}-spin.svg").write_text(spin, encoding="utf-8")

    html = f"""<!doctype html>
<meta charset="utf-8"><title>rotational j &mdash; {palette_key} {mode}</title>
<style>
  body {{ margin:0; padding:40px; background:#0b0b0f; color:#e7e7ea;
         font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace; }}
  h1 {{ font-size:15px; font-weight:600; letter-spacing:.08em; text-transform:uppercase;
        color:#8b8b95; margin:0 0 28px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:28px; }}
  figure {{ margin:0; }}
  img {{ width:100%; display:block; border-radius:14px; }}
  figcaption {{ margin-top:10px; color:#8b8b95; display:flex; align-items:center; gap:10px; }}
  .tiny {{ width:32px; height:32px; border-radius:6px; }}
  .spin {{ margin-top:44px; }}
  .spin img {{ width:240px; }}
</style>
<h1>{layers} layers &middot; opacity {min_opacity:g}&rarr;1.0 (gamma {gamma:g})
&middot; scale step {scale_step:g} &middot; {palette_key} {mode}</h1>
<div class="grid">
{chr(10).join(cards)}
</div>
<div class="spin">
  <h1>animated &mdash; 8&deg; step, 9s spin</h1>
  <img src="rot-{palette_key}-{mode}-spin.svg" alt="spinning">
</div>
"""
    (out_dir / f"sheet-{palette_key}-{mode}.html").write_text(html, encoding="utf-8")
    return out_dir / f"sheet-{palette_key}-{mode}.html"


def write_rot_assets(out_dir, palette_key, mode, background, glyph, cfg, pivot, sizes):
    """Full favicon + avatar set rendered with the rotational stack.

    Mirrors write_assets() in generate_favicon_assets.py, including the two-form
    split: rounded-rect plate with transparency for favicons, full-bleed opaque
    square with no alpha for avatars.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    g = (cfg["layers"], cfg["step"], cfg["min_opacity"], cfg["gamma"], cfg["scale_step"])

    def stack(size, rounded=True):
        return render_stack(size, background, glyph, *g, pivot=pivot, rounded=rounded)

    (out_dir / f"icon-{palette_key}-{mode}.svg").write_text(
        build_svg(background, glyph, *g, pivot=pivot), encoding="utf-8")
    (out_dir / f"avatar-{palette_key}-{mode}.svg").write_text(
        build_svg(background, glyph, *g, pivot=pivot, rounded=False), encoding="utf-8")

    for avatar_size in (512, 1024):
        stack(avatar_size, rounded=False).save(
            out_dir / f"avatar-{avatar_size}x{avatar_size}.png")

    # Transparent form: the echo stack with no plate behind it. The rear layers
    # sit at 0.08 opacity, so on a busy surface they vanish. Use over flat
    # backgrounds only.
    (out_dir / f"mark-{palette_key}-{mode}.svg").write_text(
        build_svg(None, glyph, *g, pivot=pivot, rounded=False), encoding="utf-8")
    for mark_size in (512, 1024):
        render_stack(mark_size, None, glyph, *g, pivot=pivot).save(
            out_dir / f"mark-{mark_size}x{mark_size}.png")

    for size in sizes:
        stack(size).save(out_dir / f"favicon-{size}x{size}.png")

    stack(180).save(out_dir / "apple-touch-icon.png")
    stack(192).save(out_dir / "android-chrome-192x192.png")
    stack(512).save(out_dir / "android-chrome-512x512.png")
    stack(256).save(out_dir / "favicon.ico",
                    sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    (out_dir / "site.webmanifest").write_text(json.dumps({
        "name": "jeffols", "short_name": "jeffols",
        "icons": [
            {"src": "android-chrome-192x192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "android-chrome-512x512.png", "sizes": "512x512", "type": "image/png"},
        ],
        "theme_color": background, "background_color": background, "display": "standalone",
    }, indent=2), encoding="utf-8")

    (out_dir / "metadata.json").write_text(json.dumps({
        "palette": palette_key, "mode": mode,
        "background": background, "glyph": glyph, "sizes": sizes,
        "variant": "rotational depth stack",
        "layers": cfg["layers"], "step_degrees": cfg["step"],
        "min_opacity": cfg["min_opacity"], "gamma": cfg["gamma"],
        "scale_step": cfg["scale_step"], "pivot": list(pivot),
        "layer_opacities": [round(o, 4) for o in ramp(cfg)],
    }, indent=2), encoding="utf-8")


def write_preset_sheet(out_dir, palette_key, mode, background, glyph, pivot):
    """Every preset side by side at 512px, 32px and 16px, for picking between them."""
    cards = []
    for key in PRESET_KEYS:
        cfg = resolve(key, None, {})
        name = f"preset-{key}-{palette_key}-{mode}"
        (out_dir / f"{name}.svg").write_text(
            build_svg(background, glyph, cfg["layers"], cfg["step"],
                      cfg["min_opacity"], cfg["gamma"], cfg["scale_step"], pivot),
            encoding="utf-8")
        for size in (512, 32, 16):
            render_stack(size, background, glyph, cfg["layers"], cfg["step"],
                         cfg["min_opacity"], cfg["gamma"], cfg["scale_step"],
                         pivot).save(out_dir / f"{name}-{size}.png")
        cards.append(
            f'<figure><img src="{name}-512.png" alt="{key}">'
            f'<figcaption><b>{key}</b>'
            f'<span>{PRESETS[key]["label"]}</span>'
            f'<span class="note">{PRESETS[key]["note"]}</span>'
            f'<span class="tiny"><img src="{name}-32.png" alt="32px" width="32" height="32">'
            f'<img src="{name}-16.png" alt="16px" width="16" height="16"></span>'
            f'</figcaption></figure>'
        )

    html = f"""<!doctype html>
<meta charset="utf-8"><title>plates presets &mdash; {palette_key} {mode}</title>
<style>
  body {{ margin:0; padding:40px; background:#0e0f12; color:#eceef0;
         font:14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace; }}
  h1 {{ font-size:13px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
        color:#6b707b; margin:0 0 30px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:30px; }}
  figure {{ margin:0; }}
  figure > img {{ width:100%; display:block; border-radius:16px; }}
  figcaption {{ margin-top:12px; display:flex; flex-direction:column; gap:4px; }}
  figcaption b {{ color:#FFD60A; font-weight:600; }}
  figcaption span {{ color:#9ba0aa; font-size:12px; }}
  .note {{ color:#6b707b !important; }}
  .tiny {{ display:flex; align-items:flex-end; gap:10px; margin-top:8px; }}
  .tiny img {{ border-radius:4px; }}
</style>
<h1>plates presets &middot; {palette_key} {mode}</h1>
<div class="grid">
{chr(10).join(cards)}
</div>
"""
    path = out_dir / f"presets-{palette_key}-{mode}.html"
    path.write_text(html, encoding="utf-8")
    return path


def list_presets():
    for key in PRESET_KEYS:
        cfg = resolve(key, None, {})
        print(f"{key}: {PRESETS[key]['label']} ({PRESETS[key]['note']})")
        print(f"  layers {cfg['layers']} · step {cfg['step']:g}° · rear {cfg['min_opacity']:g}"
              f" · falloff {cfg['gamma']:g} · recession {cfg['scale_step']:g}")
    print("\nfade ramps (--fade, overrides rear opacity + falloff):")
    for key in FADE_KEYS:
        print(f"  {key}: {FADES[key]['label']}"
              f" — rear {FADES[key]['min_opacity']:g}, falloff {FADES[key]['gamma']:g}")
        for n in (3, 4):
            cfg = resolve("plates", key, {"layers": n})
            print(f"      {n} layers: " + " → ".join(f"{o:.2f}" for o in ramp(cfg)))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(REPO / "explorations" / "rotational"))
    p.add_argument("--palette", default="signal_yellow",
                   choices=list(PALETTES.keys()) + ["all"])
    p.add_argument("--mode", default="dark", choices=["dark", "light", "both"])
    p.add_argument("--preset", choices=PRESET_KEYS,
                   help="named setting; individual flags below still override it")
    p.add_argument("--fade", choices=FADE_KEYS,
                   help="opacity ramp; overrides the preset's rear opacity and falloff")
    p.add_argument("--layers", type=int)
    p.add_argument("--step", type=float, help="degrees between layers")
    p.add_argument("--min-opacity", type=float)
    p.add_argument("--gamma", type=float,
                   help=">1 pushes the trail dimmer, <1 makes it heavier")
    p.add_argument("--scale-step", type=float,
                   help="each layer back shrinks by this fraction")
    p.add_argument("--pivot", default="plate", choices=["plate", "glyph"])
    p.add_argument("--sheet", action="store_true",
                   help="comparison sheet across step angles")
    p.add_argument("--preset-sheet", action="store_true",
                   help="comparison sheet across every preset")
    p.add_argument("--assets", action="store_true",
                   help="full favicon + avatar + ICO + manifest set, per palette/mode")
    p.add_argument("--sizes", default=",".join(str(s) for s in DEFAULT_SIZES))
    p.add_argument("--list-presets", action="store_true")
    p.add_argument("--canonical", metavar="DIR",
                   help="write the palette-independent monochrome rotational "
                        "marks to DIR and exit, e.g. assets/marks/rotational")
    a = p.parse_args()

    if a.list_presets:
        list_presets()
        return

    if a.canonical:
        cfg = resolve(a.preset or "plates", a.fade, {})
        g = (cfg["layers"], cfg["step"], cfg["min_opacity"], cfg["gamma"],
             cfg["scale_step"])
        for name in write_canonical_marks(
                a.canonical,
                renderer=lambda size, fill: render_stack(size, None, fill, *g),
                label="jeffols rotational mark",
                svg_builder=lambda fill: build_svg(None, fill, *g, rounded=False)):
            print(f"  {name}")
        print(f"Canonical rotational marks in {a.canonical}")
        return

    cfg = resolve(a.preset, a.fade, {
        "layers": a.layers, "step": a.step, "min_opacity": a.min_opacity,
        "gamma": a.gamma, "scale_step": a.scale_step,
    })
    pivot = PIVOT if a.pivot == "plate" else GLYPH_PIVOT
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    keys = list(PALETTES) if a.palette == "all" else [a.palette]
    slug = "-".join(x for x in (a.preset or "custom", a.fade) if x)

    # Flat list of the palette/mode pairs that actually exist, so a dark-only
    # palette does not have to be special-cased downstream and the nesting
    # decision below stays a single count.
    combos = [(k, m) for k in keys for m in resolve_modes(k, a.mode)]

    for key, mode in combos:
        c = PALETTES[key][mode]
        bg, gl = c["background"], c["glyph"]

        if a.assets:
            target = out / key / mode if len(combos) > 1 else out
            write_rot_assets(target, key, mode, bg, gl, cfg, pivot, parse_sizes(a.sizes))
            print(f"assets: {target}")
            continue
        if a.preset_sheet:
            print(f"preset sheet: {write_preset_sheet(out, key, mode, bg, gl, pivot)}")
            continue
        if a.sheet:
            print(f"sheet: {write_sheet(out, key, mode, bg, gl, cfg['layers'],
                                        cfg['min_opacity'], cfg['gamma'],
                                        cfg['scale_step'], pivot)}")
            continue

        name = f"rot-{slug}-{key}-{mode}"
        (out / f"{name}.svg").write_text(
            build_svg(bg, gl, cfg["layers"], cfg["step"], cfg["min_opacity"],
                      cfg["gamma"], cfg["scale_step"], pivot),
            encoding="utf-8")
        (out / f"{name}-spin.svg").write_text(
            build_svg(bg, gl, cfg["layers"], cfg["step"], cfg["min_opacity"],
                      cfg["gamma"], cfg["scale_step"], pivot, spin_seconds=9),
            encoding="utf-8")
        for size in (512, 128, 32):
            render_stack(size, bg, gl, cfg["layers"], cfg["step"],
                         cfg["min_opacity"], cfg["gamma"], cfg["scale_step"],
                         pivot).save(out / f"{name}-{size}.png")
        print(f"generated {name} in {out}")


if __name__ == "__main__":
    main()
