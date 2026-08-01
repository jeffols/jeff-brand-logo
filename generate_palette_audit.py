#!/usr/bin/env python3
"""
Audit the palette system for distinctiveness and differentiation.

Contrast (docs/accessibility.md) asks whether a mark is legible on its own
plate. This asks a different question: can two palettes be told apart, and does
that survive colour blindness?

Colour-vision deficiency is simulated with the Machado et al. (2009) matrices at
full severity, applied in linear RGB. Deuteranopia and protanopia together affect
roughly 8% of men.

Dependencies:
    pip install pillow

Usage:
    python generate_palette_audit.py
"""

from pathlib import Path
import argparse
import colorsys
import itertools
import math

from generate_favicon_assets import PALETTES, render_icon

# Machado et al. 2009, severity 1.0, linear-RGB.
CVD = {
    "protanopia": ((0.152286, 1.052583, -0.204868),
                   (0.114503, 0.786281, 0.099216),
                   (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322, 0.860646, -0.227968),
                     (0.280085, 0.672501, 0.047413),
                     (-0.011820, 0.042940, 0.968881)),
    "tritanopia": ((1.255528, -0.076749, -0.178779),
                   (-0.078411, 0.930809, 0.147602),
                   (0.004733, 0.691367, 0.303900)),
}
VIEWS = ["normal"] + list(CVD)
PREVALENCE = {
    "normal": "typical vision",
    "deuteranopia": "~6% of men",
    "protanopia": "~2% of men",
    "tritanopia": "rare, under 0.01%",
}
SIZES = [128, 32]


# ---------------------------------------------------------------- colour maths

def _to_linear(hexstr):
    h = hexstr.lstrip("#")
    return [(lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
            (int(h[i:i + 2], 16) / 255) for i in (0, 2, 4)]


def _from_linear(v):
    out = []
    for c in v:
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        out.append(round(c * 255))
    return "#%02X%02X%02X" % tuple(out)


def simulate(hexstr, view):
    """What this colour looks like to a viewer with `view`."""
    if view == "normal":
        return hexstr
    r, g, b = _to_linear(hexstr)
    m = CVD[view]
    return _from_linear([m[i][0] * r + m[i][1] * g + m[i][2] * b for i in range(3)])


def _lab(hexstr):
    r, g, b = _to_linear(hexstr)
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b)
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de2000(c1, c2):
    """CIEDE2000. <10 collides, 10-20 close, 20+ unambiguously different."""
    L1, a1, b1 = _lab(c1)
    L2, a2, b2 = _lab(c2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb > 0 else 0
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    else:
        dhp = h2p - h1p - 360 if h2p > h1p else h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if (h1p + h2p) < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30))
         + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6))
         - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp > 0 else 0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * (30 * math.exp(-(((hbp - 275) / 25) ** 2))))) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))


def hue_of(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    H, _, S = colorsys.rgb_to_hls(r, g, b)
    return H * 360, S * 100


# ---------------------------------------------------------------------- render

def render_all(out, keys):
    for key in keys:
        c = PALETTES[key]["dark"]
        for view in VIEWS:
            bg = simulate(c["background"], view)
            gl = simulate(c["glyph"], view)
            for size in SIZES:
                render_icon(size, bg, gl).save(out / f"{key}-{view}-{size}.png")


def band(d):
    if d < 10:
        return "collides", "bad"
    if d < 20:
        return "close", "warn"
    return "distinct", "ok"


def view_block(keys, view):
    cards = "".join(
        f'<figure><img src="audit/{k}-{view}-128.png" width="128" height="128" alt="{k}">'
        f'<img class="sm" src="audit/{k}-{view}-32.png" width="32" height="32" alt="">'
        f'<figcaption>{k}</figcaption></figure>' for k in keys)

    pairs = sorted(
        (de2000(simulate(PALETTES[a]["dark"]["glyph"], view),
                simulate(PALETTES[b]["dark"]["glyph"], view)), a, b)
        for a, b in itertools.combinations(keys, 2))
    worst = "".join(
        f'<tr class="{band(d)[1]}"><td>{a} / {b}</td><td>{d:.1f}</td>'
        f'<td>{band(d)[0]}</td></tr>' for d, a, b in pairs[:4])
    collisions = sum(1 for d, _, _ in pairs if d < 10)

    verdict = (f'<b class="bad">{collisions} colliding pairs</b>' if collisions
               else '<b class="ok">no collisions</b>')

    return f"""<section>
  <h2>{view} <span class="prev">{PREVALENCE[view]}</span></h2>
  <p class="verdict">{verdict} &middot; closest pair {pairs[0][0]:.1f}</p>
  <div class="row">{cards}</div>
  <table><tr><th>closest pairs</th><th>&Delta;E</th><th></th></tr>{worst}</table>
</section>"""


def hue_strip(keys):
    """Pins on a hue ramp. Labels stagger downward when neighbours are close,
    which happens exactly where the clustering this chart exists to show is."""
    pins = sorted(((hue_of(PALETTES[k]["dark"]["glyph"]), k) for k in keys),
                  key=lambda p: p[0][0])
    marks, prev_h, tier = "", -999, 0
    for (h, s), k in pins:
        tier = tier + 1 if h - prev_h < 45 else 0
        prev_h = h
        cls = " neutral" if s < 60 else ""
        g = PALETTES[k]["dark"]["glyph"]
        marks += (f'<div class="pin{cls}" style="left:{h / 360 * 100:.1f}%">'
                  f'<span class="dot" style="background:{g}"></span>'
                  f'<span class="lbl" style="margin-top:{52 + tier * 30}px">'
                  f'{k}<br>{h:.0f}&deg;</span></div>')
    return f'<div class="wheel">{marks}</div>'


CSS = """
:root { color-scheme: dark; }
body { margin:0; padding:48px; background:#0e0f12; color:#eceef0;
       font:14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace; }
h1 { font-size:19px; margin:0 0 6px; }
h2 { font-size:13px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
     color:#eceef0; margin:0 0 4px; }
.prev { color:#6b707b; letter-spacing:0; text-transform:none; font-weight:400;
        margin-left:10px; font-size:12px; }
p.lede { color:#9ba0aa; max-width:66ch; margin:0 0 10px; }
section { margin-top:46px; padding-top:26px; border-top:1px solid #22252b; }
.verdict { color:#9ba0aa; margin:0 0 20px; }
.row { display:flex; flex-wrap:wrap; gap:26px; margin-bottom:22px; }
figure { margin:0; position:relative; }
figure img { display:block; border-radius:22px; }
.sm { position:absolute; right:-10px; bottom:26px; border-radius:6px;
      box-shadow:0 0 0 3px #0e0f12; }
figcaption { margin-top:9px; color:#9ba0aa; font-size:12px; }
table { border-collapse:collapse; font-size:12px; }
td, th { padding:4px 16px 4px 0; text-align:left; }
th { color:#6b707b; font-weight:500; }
.bad td, b.bad { color:#ff6b6b; }
.warn td { color:#ffd43b; }
.ok td, b.ok { color:#8ce99a; }
.wheel { position:relative; height:118px; margin:22px 0 40px;
         background:linear-gradient(to right,
           hsl(0,85%,55%),hsl(60,85%,55%),hsl(120,85%,55%),hsl(180,85%,55%),
           hsl(240,85%,55%),hsl(300,85%,55%),hsl(360,85%,55%));
         border-radius:6px; opacity:.95; }
.pin { position:absolute; top:0; transform:translateX(-50%); text-align:center; }
.pin .dot { display:block; width:20px; height:20px; border-radius:50%;
            box-shadow:0 0 0 3px #0e0f12; margin:-6px auto 0; }
.pin .lbl { display:block; margin-top:52px; font-size:11px; color:#eceef0;
            background:#0e0f12; padding:3px 5px; border-radius:4px; white-space:nowrap; }
.pin.neutral .dot { box-shadow:0 0 0 3px #0e0f12, 0 0 0 4px #6b707b; }
.rule { background:#15171c; border-left:2px solid #FFD60A; padding:16px 20px;
        margin:24px 0 0; max-width:66ch; color:#c9ced6; }
"""


def build(keys):
    return f"""<!doctype html>
<meta charset="utf-8"><title>palette audit</title>
<style>{CSS}</style>
<h1>Palette audit &mdash; distinctiveness and differentiation</h1>
<p class="lede">Can two palettes be told apart, and does that survive colour
blindness? Marks are shown as a viewer with each condition would see them.
Separation is CIEDE2000 on the dark-mode glyph, where the differentiation
actually lives &mdash; the plates are near-black and carry almost none of it.</p>
<div class="rule">&Delta;E under 10 is a collision: two palettes that read as the
same colour. 10&ndash;20 is close. 20+ is unambiguously different.</div>

<section>
  <h2>hue distribution</h2>
  <p class="lede">Where each palette sits on the wheel. Ringed marker is
  effectively neutral (low saturation).</p>
  {hue_strip(keys)}
</section>
{"".join(view_block(keys, v) for v in VIEWS)}
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="docs")
    a = p.parse_args()

    docs = Path(a.out)
    (docs / "audit").mkdir(parents=True, exist_ok=True)
    keys = list(PALETTES)

    render_all(docs / "audit", keys)
    page = docs / "palette-audit.html"
    page.write_text(build(keys), encoding="utf-8")
    print(f"wrote {page}")


if __name__ == "__main__":
    main()
