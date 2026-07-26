#!/usr/bin/env python3
"""Generate LinkedIn banners for all palette/mode combinations."""

import subprocess
import json
from pathlib import Path

PALETTES = {
    "signal_yellow": {
        "dark":  {"bg": "#111827", "glyph": "#FFD60A"},
        "light": {"bg": "#FFF7E0", "glyph": "#B8960A"},
    },
    "electric_blue": {
        "dark":  {"bg": "#0B1020", "glyph": "#7DD3FC"},
        "light": {"bg": "#F6FBFF", "glyph": "#005A9C"},
    },
    "amber_utility": {
        "dark":  {"bg": "#1F1B16", "glyph": "#FFB000"},
        "light": {"bg": "#FFF8E1", "glyph": "#8B5E00"},
    },
    "terminal_lime": {
        "dark":  {"bg": "#151515", "glyph": "#B6FF4D"},
        "light": {"bg": "#F7FFE8", "glyph": "#3D6600"},
    },
    "slate_mono": {
        "dark":  {"bg": "#0F172A", "glyph": "#F8FAFC"},
        "light": {"bg": "#F8FAFC", "glyph": "#0F172A"},
    },
}

J_PARTS = """<circle cx="470" cy="190" r="70" fill="none" stroke="{glyph}" stroke-width="{sw}"/>
    <rect x="460" y="340" width="160" height="280" rx="6" fill="none" stroke="{glyph}" stroke-width="{sw}"/>
    <path d="M 500 640 H 660 V 720 Q 660 860 520 860 H 370 Q 280 860 280 780 V 750 Q 280 710 330 710 H 410 Q 500 710 500 640 Z" fill="none" stroke="{glyph}" stroke-width="{sw}"/>"""

J_SOLID = """<circle cx="470" cy="190" r="70" fill="{glyph}"/>
    <rect x="460" y="340" width="160" height="280" rx="6" fill="{glyph}"/>
    <path d="M 500 640 H 660 V 720 Q 660 860 520 860 H 370 Q 280 860 280 780 V 750 Q 280 710 330 710 H 410 Q 500 710 500 640 Z" fill="{glyph}"/>"""


def darken(hex_color, factor=0.6):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"


def dark_svg(bg, glyph):
    bg2 = darken(bg, 0.7)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1584 396" width="1584" height="396">
  <defs>
    <filter id="glow-1" x="-120%" y="-120%" width="340%" height="340%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="24" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="60" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-2" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="16" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="40" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-3" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="24" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glow-4" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="14" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="mark-halo" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="10"/>
    </filter>
    <radialGradient id="vignette" cx="0.6" cy="0.5" r="0.7">
      <stop offset="0" stop-color="{bg}"/>
      <stop offset="1" stop-color="{bg2}"/>
    </radialGradient>
  </defs>
  <rect width="1584" height="396" fill="{bg}"/>
  <rect width="1584" height="396" fill="url(#vignette)" opacity="0.5"/>
  <g opacity="0.015" stroke="#CBD5E1" stroke-width="0.5">
    <line x1="0" y1="99" x2="1584" y2="99"/><line x1="0" y1="198" x2="1584" y2="198"/>
    <line x1="0" y1="297" x2="1584" y2="297"/><line x1="396" y1="0" x2="396" y2="396"/>
    <line x1="792" y1="0" x2="792" y2="396"/><line x1="1188" y1="0" x2="1188" y2="396"/>
  </g>
  <g transform="translate(-741,-391) scale(1.15)" opacity="0.07" filter="url(#glow-1)">
    {J_PARTS.format(glyph=glyph, sw=24)}
  </g>
  <g transform="translate(-64,-237) scale(0.85)" opacity="0.08" filter="url(#glow-2)">
    {J_PARTS.format(glyph=glyph, sw=22)}
  </g>
  <g transform="translate(448,-135) scale(0.65)" opacity="0.11" filter="url(#glow-3)">
    {J_PARTS.format(glyph=glyph, sw=18)}
  </g>
  <g transform="translate(817,-58) scale(0.50)" opacity="0.15" filter="url(#glow-4)">
    {J_PARTS.format(glyph=glyph, sw=16)}
  </g>
  <g transform="translate(1042,-7) scale(0.40)" opacity="0.20" filter="url(#glow-4)">
    {J_PARTS.format(glyph=glyph, sw=14)}
  </g>
  <g transform="translate(1130,24) scale(0.34)" opacity="0.18" filter="url(#mark-halo)">
    {J_SOLID.format(glyph=glyph)}
  </g>
  <g transform="translate(1130,24) scale(0.34)">
    {J_SOLID.format(glyph=glyph)}
  </g>
  <line x1="0" y1="0.5" x2="1584" y2="0.5" stroke="{glyph}" stroke-width="1" opacity="0.035"/>
  <line x1="0" y1="395.5" x2="1584" y2="395.5" stroke="{glyph}" stroke-width="1" opacity="0.035"/>
</svg>"""


def light_svg(bg, glyph):
    bg2 = darken(bg, 0.95)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1584 396" width="1584" height="396">
  <defs>
    <filter id="soft-1" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="18" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="45" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft-2" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="30" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft-3" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="18" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft-4" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="b1"/>
      <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="b2"/>
      <feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="mark-shadow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="8"/>
    </filter>
    <linearGradient id="bg-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg}"/>
      <stop offset="1" stop-color="{bg2}"/>
    </linearGradient>
  </defs>
  <rect width="1584" height="396" fill="url(#bg-grad)"/>
  <g opacity="0.04" stroke="{glyph}" stroke-width="0.5" opacity="0.03">
    <line x1="0" y1="99" x2="1584" y2="99"/><line x1="0" y1="198" x2="1584" y2="198"/>
    <line x1="0" y1="297" x2="1584" y2="297"/><line x1="396" y1="0" x2="396" y2="396"/>
    <line x1="792" y1="0" x2="792" y2="396"/><line x1="1188" y1="0" x2="1188" y2="396"/>
  </g>
  <g transform="translate(-741,-391) scale(1.15)" opacity="0.06" filter="url(#soft-1)">
    {J_PARTS.format(glyph=glyph, sw=24)}
  </g>
  <g transform="translate(-64,-237) scale(0.85)" opacity="0.07" filter="url(#soft-2)">
    {J_PARTS.format(glyph=glyph, sw=22)}
  </g>
  <g transform="translate(448,-135) scale(0.65)" opacity="0.09" filter="url(#soft-3)">
    {J_PARTS.format(glyph=glyph, sw=18)}
  </g>
  <g transform="translate(817,-58) scale(0.50)" opacity="0.12" filter="url(#soft-4)">
    {J_PARTS.format(glyph=glyph, sw=16)}
  </g>
  <g transform="translate(1042,-7) scale(0.40)" opacity="0.16" filter="url(#soft-4)">
    {J_PARTS.format(glyph=glyph, sw=14)}
  </g>
  <g transform="translate(1130,24) scale(0.34)" opacity="0.08" filter="url(#mark-shadow)">
    {J_SOLID.format(glyph=glyph)}
  </g>
  <g transform="translate(1130,24) scale(0.34)">
    {J_SOLID.format(glyph=glyph)}
  </g>
  <line x1="0" y1="0.5" x2="1584" y2="0.5" stroke="{glyph}" stroke-width="1" opacity="0.06"/>
  <line x1="0" y1="395.5" x2="1584" y2="395.5" stroke="{glyph}" stroke-width="1" opacity="0.06"/>
</svg>"""


def html_wrap(svg):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>*{{margin:0;padding:0;}}body{{width:1584px;height:396px;overflow:hidden;}}</style>
</head><body>{svg}</body></html>"""


def render_png(html_path, png_path):
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    subprocess.run([
        chrome, "--headless", "--disable-gpu",
        f"--screenshot={png_path}",
        "--window-size=1584,396",
        f"file://{html_path}",
    ], capture_output=True, timeout=15)


def main():
    out = Path("linkedin-banners")
    out.mkdir(exist_ok=True)
    tmp = out / "_tmp.html"

    manifest = []

    for name, modes in PALETTES.items():
        for mode in ("dark", "light"):
            colors = modes[mode]
            bg, glyph = colors["bg"], colors["glyph"]

            svg = dark_svg(bg, glyph) if mode == "dark" else light_svg(bg, glyph)
            tmp.write_text(html_wrap(svg), encoding="utf-8")

            png_name = f"linkedin-{name}-{mode}.png"
            png_path = out / png_name
            render_png(str(tmp.resolve()), str(png_path.resolve()))

            manifest.append({"palette": name, "mode": mode, "file": png_name, "bg": bg, "glyph": glyph})
            print(f"  {png_name}")

    tmp.unlink()

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Build comparison HTML
    cards = []
    for entry in manifest:
        cards.append(f"""
    <div class="card-wrap">
      <h3>{entry["palette"].replace("_"," ").title()} — {entry["mode"]}</h3>
      <div class="card" style="background:{entry["bg"]}">
        <img src="{entry["file"]}" alt="{entry["palette"]} {entry["mode"]}">
      </div>
    </div>""")

    compare = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>LinkedIn Banner — All Palettes</title>
<style>
  *{{margin:0;padding:0;box-sizing:border-box;}}
  body{{background:#F4F2EE;font-family:-apple-system,system-ui,sans-serif;padding:2rem 2rem 4rem;color:#333;}}
  h1{{font-size:1rem;font-weight:500;color:#888;margin-bottom:0.5rem;}}
  .subtitle{{font-size:0.8rem;color:#aaa;margin-bottom:2rem;}}
  .grid{{display:grid;grid-template-columns:1fr 1fr;gap:2rem;max-width:1600px;}}
  .card-wrap h3{{font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;color:#999;margin-bottom:0.5rem;}}
  .card{{border-radius:8px;overflow:hidden;box-shadow:0 0 0 1px rgba(0,0,0,0.08),0 2px 4px rgba(0,0,0,0.04);}}
  .card img{{width:100%;display:block;}}
</style></head><body>
<h1>LinkedIn Banners — All Palettes</h1>
<p class="subtitle">Shown against LinkedIn's page background (#F4F2EE)</p>
<div class="grid">{"".join(cards)}
</div></body></html>"""

    (out / "compare.html").write_text(compare, encoding="utf-8")
    print(f"\nDone — {len(manifest)} banners in {out}/")
    print(f"Open {out}/compare.html to view all")


if __name__ == "__main__":
    main()
