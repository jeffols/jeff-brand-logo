# jeff-brand-logo

Jeffols brand system repository. Geometric lowercase **j** ("tectonic j") — three
offset pieces: dot, stem, hook.

**`BRAND.md` is the strategic source of truth.** Do not change logo geometry,
palette meaning, positioning, or usage hierarchy without explicitly identifying
the proposed brand decision. Generated assets must derive from canonical source
geometry. Prefer simple, reproducible generation over manual one-off edits. Do
not modify the website repository until the brand guidance and required assets
are stable.

## Stack
- Python 3 + Pillow (only dependency; banner generator also needs headless Chrome)
- Pure SVG generation (no external fonts/images)

## Layout
```
BRAND.md                     — strategy. Read before changing anything visual
docs/                        — operational guidance + numbered decision records
generate_favicon_assets.py   — CLI: primary mark, all assets (PNG, ICO, SVG, manifest)
generate_rotational_logo.py  — CLI: signature variant; imports PALETTES + quad_bezier
                               from generate_favicon_assets but RE-DECLARES the glyph
                               coordinates. They can drift. Phase 2 extracts geometry.py
generate_validation_sheet.py — CLI: builds docs/size-validation.html
generate_linkedin_banners.py — CLI: banner compositions. Own 5-palette dict, missing
                               deep_indigo. Hardcoded macOS Chrome path
watermark.css                — drop-in CSS watermark (body::after, data URI)
palettes/<name>/dark|light/  — primary mark per palette+mode
palettes-rotational/…        — signature variant, same layout
explorations/                — not brand assets. Never ship from here
```

## Hierarchy (decision 0001)
1. **Primary mark** — naked j. Default. Favicons always. Under 48 px always.
2. **Signature variant** — rotational echo j. Needs size; never replaces level 1.
3. **Treatments** — glow, watermark, crop, palette, animation. Never a logo.

Wide surfaces (banners, covers) are governed by composition, not by size.

## Two forms
- **Favicon** — rounded-rect plate, transparent outside the radius.
- **Avatar** — full-bleed opaque square, no rounding, no alpha. Upload to Substack,
  LinkedIn, GitHub. They apply their own mask; a pre-rounded asset fights it and
  leftover transparency flattens to white slivers.

## Palettes
signal_yellow (default, **dark-only** — decision 0003), electric_blue, amber_utility,
terminal_lime, deep_indigo, slate_mono. The matrix is NOT symmetric: use
`modes_for(key)` / `resolve_modes(key, requested)`, never `["dark","light"]`.
`--palette all --mode both` yields 11 combinations, not 12.
Separation lives in the glyph, not the plate — see docs/accessibility.md.

## Run
```bash
pip install pillow
python generate_favicon_assets.py --out ./out --palette all --mode both
python generate_rotational_logo.py --preset plates --palette all --mode both --assets
python generate_validation_sheet.py
```

## Rotational variant
N copies rotated `--step` degrees apart, opacity ramping to opaque at the front,
each layer back shrunk by `--scale-step`. Front layer stays upright at full opacity.
Canonical construction is **`plates`** (decision 0002): 3 layers, 6°, rear 0.08,
falloff 3.0, recession 0.06 — ramp 0.08 / 0.195 / 1.00. The other seven presets stay
in the CLI as the comparison family that produced the decision; do not ship from them.

## Design reference
- Canvas 1024×1024, 4× supersample, LANCZOS downscale
- Geometry currently duplicated in 17 files — keep `render_icon()` and `build_svg()`
  in sync until Phase 2 extracts it
- SVG uses inline fills, no CSS variables — intentional for max compatibility
- Rounded-rect radius ≈ 17% of size

## Guardrails
Prefer simple over clever. Fix root causes, not presentation patches. Do not invent
brand strategy without flagging it. Do not replace the naked mark with the rotational
one. Signal Yellow is not mandatory. Keep contrast accessible. Update all consumers
when canonical asset paths change.
