#!/usr/bin/env python3
"""
Canonical geometry of the tectonic j. The single source of truth.

Before this module the mark was drawn from coordinates copied into seventeen
files, so a geometry change meant seventeen correct edits and nothing failed
loudly when one was missed. Everything that draws the mark now imports from
here.

Design space is 1024x1024. Three pieces, each offset from the others:

    dot     circle, shifted left
    stem    rounded rectangle, centred
    hook    curved base, shifted right

This module owns the numbers. It does not own how finely a curve is
tessellated or what a caller does with the result — those are rendering
concerns, and callers differ deliberately (the flat renderer snaps to integer
pixels, the rotational one keeps floats so it can rotate before rasterising).

No Pillow import. This is arithmetic and strings.
"""

DESIGN_SIZE = 1024

# Framing offset applied to all three pieces (decision 0005). The glyph's
# bounding box is x 280..660, centre 470, so +42 centres it on the 1024 canvas.
# This is padding, not geometry: the shapes and their relative positions are
# untouched. Set to 0 to reproduce pre-0005 assets.
GLYPH_DX = 0
GLYPH_DY = 0

# --- the mark, stated once ------------------------------------------------

DOT = {"cx": 470, "cy": 190, "r": 70}
STEM = {"x": 460, "y": 340, "w": 160, "h": 280, "r": 6}

# Hook outline as path ops. "L" is a line to a point, "Q" is a quadratic with
# one control point. Kept in this form so both the polygon and the SVG path can
# be generated from it rather than maintained in parallel.
HOOK = [
    ("M", (500, 640)),
    ("L", (660, 640)),
    ("L", (660, 720)),
    ("Q", (660, 860), (520, 860)),
    ("L", (370, 860)),
    ("Q", (280, 860), (280, 780)),
    ("L", (280, 750)),
    ("Q", (280, 710), (330, 710)),
    ("L", (410, 710)),
    ("Q", (500, 710), (500, 640)),
]

# Corner radius of the plate, in design units. Roughly 17% of DESIGN_SIZE, but
# stated as 174 rather than as 0.17: 0.17 * 1024 is 174.08, which rounds to a
# different pixel from 174 at some scales (192px is one) and silently shifts
# every plate corner.
PLATE_RADIUS = 174


def plate_radius(size):
    """Corner radius for a plate rendered at `size` pixels."""
    return max(1, round(PLATE_RADIUS * size / DESIGN_SIZE))


# --- curves ---------------------------------------------------------------

def quad_bezier(p0, p1, p2, steps=16):
    """Points along a quadratic bezier, excluding p0 and including p2."""
    out = []
    for i in range(1, steps + 1):
        t = i / steps
        u = 1 - t
        out.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return out


# --- polygons, for rasterising -------------------------------------------

def hook_polygon(scale=1.0, steps=16, snap=False, dx=None, dy=None):
    """The hook as a closed polygon.

    steps controls tessellation of each curve. snap rounds to whole pixels,
    which the flat renderer wants and the rotational one must not do, since it
    transforms the points before they reach the raster.
    """
    dx = GLYPH_DX if dx is None else dx
    dy = GLYPH_DY if dy is None else dy
    pts, cur = [], None
    for op in HOOK:
        if op[0] == "M":
            cur = op[1]
            pts.append(cur)
        elif op[0] == "L":
            cur = op[1]
            pts.append(cur)
        else:
            pts += quad_bezier(cur, op[1], op[2], steps)
            cur = op[2]
    out = [((x + dx) * scale, (y + dy) * scale) for x, y in pts]
    return [(round(x), round(y)) for x, y in out] if snap else out


def circle_polygon(cx, cy, r, steps=72):
    from math import cos, sin, pi
    return [(cx + r * cos(2 * pi * i / steps), cy + r * sin(2 * pi * i / steps))
            for i in range(steps)]


def round_rect_polygon(x, y, w, h, r, steps=6):
    """Rounded rectangle as a polygon, corners counter-clockwise from top-left."""
    from math import cos, sin, radians
    pts = []
    for cx, cy, a0, a1 in ((x + r, y + r, 180, 270),
                           (x + w - r, y + r, 270, 360),
                           (x + w - r, y + h - r, 0, 90),
                           (x + r, y + h - r, 90, 180)):
        for i in range(steps + 1):
            a = radians(a0 + (a1 - a0) * i / steps)
            pts.append((cx + r * cos(a), cy + r * sin(a)))
    return pts


def glyph_polygons(dx=None, dy=None, hook_steps=24):
    """All three pieces as polygons, for callers that transform before drawing."""
    dx = GLYPH_DX if dx is None else dx
    dy = GLYPH_DY if dy is None else dy
    shift = lambda pts: [(x + dx, y + dy) for x, y in pts]
    return [
        shift(circle_polygon(DOT["cx"], DOT["cy"], DOT["r"])),
        shift(round_rect_polygon(STEM["x"], STEM["y"], STEM["w"], STEM["h"], STEM["r"])),
        hook_polygon(1.0, steps=hook_steps, dx=dx, dy=dy),
    ]


def dot_box(scale=1.0, dx=None, dy=None):
    """Pillow ellipse bbox. Width is rounded separately from the origin so the
    result matches what the original inline arithmetic produced."""
    dx = GLYPH_DX if dx is None else dx
    dy = GLYPH_DY if dy is None else dy
    x = round((DOT["cx"] - DOT["r"] + dx) * scale)
    y = round((DOT["cy"] - DOT["r"] + dy) * scale)
    d = round(DOT["r"] * 2 * scale)
    return [x, y, x + d, y + d]


def stem_box(scale=1.0, dx=None, dy=None):
    """Pillow rounded_rectangle bbox and radius."""
    dx = GLYPH_DX if dx is None else dx
    dy = GLYPH_DY if dy is None else dy
    x = round((STEM["x"] + dx) * scale)
    y = round((STEM["y"] + dy) * scale)
    w = round(STEM["w"] * scale)
    h = round(STEM["h"] * scale)
    return [x, y, x + w, y + h], max(1, round(STEM["r"] * scale))


# --- SVG ------------------------------------------------------------------

def hook_path_d(dx=None, dy=None):
    dx = GLYPH_DX if dx is None else dx
    dy = GLYPH_DY if dy is None else dy
    f = lambda p: f"{p[0] + dx:g} {p[1] + dy:g}"
    parts = []
    for op in HOOK:
        if op[0] == "M":
            parts.append(f"M {f(op[1])}")
        elif op[0] == "L":
            parts.append(f"L {f(op[1])}")
        else:
            parts.append(f"Q {f(op[1])} {f(op[2])}")
    return " ".join(parts) + " Z"


def svg_shapes(fill=None, indent="  ", dx=None, dy=None, extra=""):
    """The three pieces as SVG elements.

    fill=None leaves them to inherit from a parent. `extra` is appended to every
    element verbatim, which is how the outline treatments get their stroke
    without a second copy of the coordinates.
    """
    dx = GLYPH_DX if dx is None else dx
    dy = GLYPH_DY if dy is None else dy
    f = (f' fill="{fill}"' if fill else "") + extra
    return (
        f'{indent}<circle cx="{DOT["cx"] + dx:g}" cy="{DOT["cy"] + dy:g}"'
        f' r="{DOT["r"]:g}"{f}/>\n'
        f'{indent}<rect x="{STEM["x"] + dx:g}" y="{STEM["y"] + dy:g}"'
        f' width="{STEM["w"]:g}" height="{STEM["h"]:g}" rx="{STEM["r"]:g}"{f}/>\n'
        f'{indent}<path d="{hook_path_d(dx, dy)}"{f}/>\n'
    )


def svg_document(background, glyph, size=DESIGN_SIZE, rounded=True,
                 label="jeffols signature icon"):
    """A complete single-mark SVG. background=None omits the plate entirely,
    which is what the transparent exports want."""
    rx = plate_radius(size) if rounded else 0
    plate = (f'  <rect width="{size}" height="{size}" rx="{rx}"'
             f' fill="{background}"/>\n' if background else "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}"'
        f' role="img" aria-label="{label}">\n'
        f'{plate}{svg_shapes(glyph)}'
        f'</svg>\n'
    )


def data_uri(background, glyph, size=DESIGN_SIZE, rounded=True):
    """Percent-encoded SVG for a CSS url(). Keeps watermark.css generated
    rather than hand-maintained."""
    svg = svg_document(background, glyph, size, rounded)
    svg = " ".join(svg.split())
    out = []
    for ch in svg:
        if ch in "#<>\"{}|\\^`?&%":
            out.append(f"%{ord(ch):02X}")
        else:
            out.append(ch)
    return "data:image/svg+xml," + "".join(out)


if __name__ == "__main__":
    xs = [x for p in glyph_polygons() for x, _ in p]
    ys = [y for p in glyph_polygons() for _, y in p]
    print(f"framing offset   dx {GLYPH_DX}  dy {GLYPH_DY}")
    print(f"glyph bbox       x {min(xs):.0f}..{max(xs):.0f}  y {min(ys):.0f}..{max(ys):.0f}")
    print(f"bbox centre      x {(min(xs)+max(xs))/2:.1f}  y {(min(ys)+max(ys))/2:.1f}"
          f"   (canvas centre {DESIGN_SIZE/2:.0f})")
    print(f"margins          left {min(xs):.0f}  right {DESIGN_SIZE-max(xs):.0f}")
