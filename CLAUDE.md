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

## Palettes
signal_yellow (default), electric_blue, amber_utility, terminal_lime, slate_mono

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
