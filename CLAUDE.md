# jeff-brand-logo

Personal brand icon/favicon toolkit. Geometric lowercase **j** ("tectonic j") — three offset pieces: dot, stem, hook.

## Stack
- Python 3 + Pillow (only dependency)
- Pure SVG generation (no external fonts/images)
- CSS watermark via data URI

## Layout
```
generate_favicon_assets.py   — CLI: renders all assets (PNG, ICO, SVG, manifest)
watermark.css                — drop-in CSS watermark (body::after, data URI)
palettes/<name>/dark|light/  — pre-generated assets per palette+mode
```

## Two forms of the mark
- **Favicon** (`favicon-*.png`, `apple-touch-icon`, `android-chrome-*`) — rounded-rect
  plate, transparent outside the radius. Browsers render favicons as-is.
- **Avatar** (`avatar-512x512.png`, `avatar-1024x1024.png`, `avatar-*.svg`) — full-bleed
  opaque square, no rounding, no alpha channel. Upload this to Substack, LinkedIn,
  and GitHub. They apply their own corner mask, so a pre-rounded asset fights it, and
  leftover transparency gets flattened to whatever the platform assumes (Substack
  assumes white, which shows as white slivers at the corners).

## Palettes
signal_yellow (default), electric_blue, amber_utility, terminal_lime, deep_indigo, slate_mono

## Run
```bash
pip install pillow
python generate_favicon_assets.py --out ./out --palette all --mode both
python generate_favicon_assets.py --list-palettes
```

## Design reference
- Canvas: 1024×1024, 4× supersample, LANCZOS downscale
- Geometry defined in `render_icon()` and `build_svg()` — keep in sync
- SVG uses inline fills, no CSS variables — intentional for max compatibility
- Rounded-rect background, radius ≈ 17% of size
