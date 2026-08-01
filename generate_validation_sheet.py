#!/usr/bin/env python3
"""
Build the canonical comparison sheet for the naked and rotational marks.

Two questions this page exists to answer:

  1. Where does the rotational mark stop reading, so the naked mark must be
     used instead?  (BRAND.md section 8)
  2. Which rotational construction is canonical?  (BRAND.md section 9, and the
     open item in section 23)

Renders at the exact sizes BRAND.md section 8 names, and displays them at 1:1
CSS pixels, because that is the size the rule is written in.

Dependencies:
    pip install pillow

Usage:
    python generate_validation_sheet.py
    python generate_validation_sheet.py --palette electric_blue
"""

from pathlib import Path
import argparse

from generate_favicon_assets import PALETTES, render_icon
from generate_rotational_logo import PIVOT, PRESETS, ramp, render_stack, resolve

# The ladder from BRAND.md section 8. Note 24 and 80: they bracket the stated
# threshold and are absent from the generators' DEFAULT_SIZES.
#
# Split deliberately. The section 8 decision happens between 16 and 128 px, so
# those sizes share one table and stay comparable at a glance. 256 and 512 are
# reference only; left in the same table they are 20x the width of the cells
# that matter and push the decision zone into a corner.
LADDER = [16, 24, 32, 48, 64, 80, 128]
REFERENCE = [256, 512]
ALL_SIZES = LADDER + REFERENCE
PRESET_SIZES = [512, 64, 32, 16]
CANONICAL = "plates-4"

# BRAND.md section 9. The page states these so a choice is made against them
# rather than on first impression.
CRITERIA = [
    "Reads as prior states, not motion blur",
    "Does not muddy the hook",
    "Keeps the frontmost mark dominant",
    "Works on light and dark backgrounds",
    "Survives PNG export and social-media compression",
    "Does not rely on glow for readability",
]


def stack_args(preset):
    c = resolve(preset, None, {})
    return c["layers"], c["step"], c["min_opacity"], c["gamma"], c["scale_step"]


def render_all(out, palette, modes):
    for mode in modes:
        c = PALETTES[palette][mode]
        bg, gl = c["background"], c["glyph"]

        for size in ALL_SIZES:
            render_icon(size, bg, gl).save(out / f"naked-{mode}-{size}.png")
            render_stack(size, bg, gl, *stack_args(CANONICAL),
                         pivot=PIVOT).save(out / f"rot-{mode}-{size}.png")

        for key in PRESETS:
            for size in PRESET_SIZES:
                render_stack(size, bg, gl, *stack_args(key),
                             pivot=PIVOT).save(out / f"preset-{key}-{mode}-{size}.png")


def ladder_table(mode, sizes):
    """One row per mark, cells at true pixel size, so the eye does the judging."""
    rows = []
    for label, prefix in (("naked", "naked"), ("rotational", "rot")):
        cells = "".join(
            f'<td><img src="validation/{prefix}-{mode}-{s}.png" '
            f'width="{s}" height="{s}" alt="{label} {s}px"></td>'
            for s in sizes
        )
        rows.append(f'<tr><th>{label}</th>{cells}</tr>')
    head = "".join(f"<td>{s}</td>" for s in sizes)
    return (f'<table><tr><th></th>{head}</tr>' + "".join(rows) + '</table>')


def preset_cards(mode):
    cards = []
    for key, p in PRESETS.items():
        c = resolve(key, None, {})
        opacities = " ".join(f"{o:.2f}" for o in ramp(c))
        canon = ' <span class="flag">current default</span>' if key == CANONICAL else ""
        small = "".join(
            f'<img src="validation/preset-{key}-{mode}-{s}.png" '
            f'width="{s}" height="{s}" alt="{s}px">'
            for s in PRESET_SIZES[1:]
        )
        cards.append(f"""<figure>
  <img class="big" src="validation/preset-{key}-{mode}-512.png" alt="{key}">
  <figcaption>
    <b>{key}</b>{canon}
    <span>{p["label"]}</span>
    <span class="note">{p["note"]}</span>
    <span class="spec">{c["layers"]} layers &middot; {c["step"]:g}&deg; &middot;
      recession {c["scale_step"]:g}</span>
    <span class="spec">opacity {opacities}</span>
    <span class="row">{small}</span>
  </figcaption>
</figure>""")
    return "\n".join(cards)


CSS = """
:root { color-scheme: dark; }
body { margin:0; padding:48px; background:#0e0f12; color:#eceef0;
       font:14px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace; }
h1 { font-size:19px; letter-spacing:-.01em; margin:0 0 6px; }
h2 { font-size:13px; font-weight:600; letter-spacing:.14em; text-transform:uppercase;
     color:#6b707b; margin:56px 0 18px; padding-top:22px; border-top:1px solid #22252b; }
p.lede { color:#9ba0aa; margin:0 0 8px; max-width:62ch; }
p.q { color:#FFD60A; margin:0 0 40px; max-width:62ch; }
table { border-collapse:collapse; margin:0 0 34px; }
td, th { padding:14px 16px; text-align:center; vertical-align:bottom; }
th { color:#6b707b; font-weight:500; text-align:right; padding-right:20px; white-space:nowrap; }
tr:first-child td { color:#6b707b; font-size:12px; padding-bottom:4px; }
img { display:block; }
td img { margin:0 auto; }
.mode { display:inline-block; padding:3px 9px; border-radius:4px; font-size:11px;
        letter-spacing:.1em; text-transform:uppercase; background:#1b1e24; color:#9ba0aa;
        margin-bottom:14px; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:32px; }
figure { margin:0; }
.big { width:100%; border-radius:16px; }
figcaption { margin-top:12px; display:flex; flex-direction:column; gap:4px; }
figcaption b { color:#FFD60A; font-weight:600; }
figcaption span { color:#9ba0aa; font-size:12px; }
.note, .spec { color:#6b707b !important; }
.flag { color:#8ce99a !important; font-size:11px; }
.row { display:flex; align-items:flex-end; gap:12px; margin-top:10px; }
.row img { border-radius:3px; }
ul.crit { color:#9ba0aa; max-width:62ch; padding-left:20px; }
ul.crit li { margin-bottom:5px; }
.rule { background:#15171c; border-left:2px solid #FFD60A; padding:16px 20px;
        margin:0 0 34px; max-width:62ch; color:#c9ced6; }
"""


def build_html(palette, modes):
    parts = [f"""<!doctype html>
<meta charset="utf-8">
<title>mark validation &mdash; {palette}</title>
<style>{CSS}</style>
<h1>Mark validation &mdash; {palette}</h1>
<p class="lede">Rendered at true pixel size and displayed 1:1. BRAND.md section 8
writes its rule in CSS pixels, so this page is measured in them too.</p>

<h2>1 &middot; Size ladder &mdash; where the echoes stop reading</h2>
<div class="rule">Working rule under test: below roughly 64&ndash;80 px use the naked
mark. Read along each row and find the size where the rotational echoes stop
looking deliberate and start looking like blur, shadow, or bad registration.
That size is the real threshold.</div>"""]

    for mode in modes:
        parts.append(f'<div class="mode">{mode}</div>'
                     + ladder_table(mode, LADDER))

    parts.append('<h2>1b &middot; Reference sizes</h2>'
                 '<p class="lede">Not part of the threshold decision. Here to show '
                 'what each mark is meant to look like when it has room.</p>')
    for mode in modes:
        parts.append(f'<div class="mode">{mode}</div>'
                     + ladder_table(mode, REFERENCE))

    parts.append("""<h2>2 &middot; Rotational constructions</h2>
<p class="lede">Every preset, same palette, same pivot. Only the construction
changes.</p>
<p class="q">Which of these is the canonical rotational mark? BRAND.md section 23
still lists this as undecided.</p>
<ul class="crit">""" + "".join(f"<li>{c}</li>" for c in CRITERIA) + "</ul>")

    for mode in modes:
        parts.append(f'<div class="mode">{mode}</div>'
                     f'<div class="grid">{preset_cards(mode)}</div>')

    return "\n".join(parts) + "\n"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--palette", default="signal_yellow", choices=list(PALETTES))
    p.add_argument("--out", default="docs")
    a = p.parse_args()

    docs = Path(a.out)
    (docs / "validation").mkdir(parents=True, exist_ok=True)
    modes = ["dark", "light"]

    render_all(docs / "validation", a.palette, modes)
    page = docs / "size-validation.html"
    page.write_text(build_html(a.palette, modes), encoding="utf-8")
    print(f"wrote {page}")


if __name__ == "__main__":
    main()
