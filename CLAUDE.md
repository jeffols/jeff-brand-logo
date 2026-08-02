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
scripts/geometry.py          — THE mark. Every coordinate lives here, once. No Pillow
                               import. Change the mark ONLY here
scripts/generate_favicon_assets.py   — primary mark. Also --canonical, --watermark
scripts/generate_rotational_logo.py  — signature variant. Also --canonical
scripts/generate_validation_sheet.py — builds docs/size-validation.html
scripts/generate_palette_audit.py    — builds docs/palette-audit.html (CVD sim)
scripts/generate_linkedin_banners.py — banners. Needs headless Chrome
scripts/generate_lockups.py  — mark + wordmark lockups. Needs fonttools
scripts/generate_social.py   — Open Graph 1200x630. Needs fonttools + Chrome
assets/lockups/              — mark + wordmark, wordmark OUTLINED (no font dep)
assets/social/               — Open Graph preview 1200x630
docs/site-handoff.md         — what jeffols.github.io copies, and where it goes
assets/fonts/                — Inter + iA Writer Duo (ship) · Plex Sans (design-time)
assets/marks/{primary,rotational}/   — palette-independent canonicals
assets/banners/linkedin/     — generated banner compositions
assets/watermarks/watermark.css      — GENERATED. Do not hand-edit; use --watermark
palettes/<name>/dark|light/  — primary mark per palette+mode
palettes-rotational/…        — signature variant, same layout
examples/                    — worked applications on real surfaces
explorations/                — not brand assets. Never ship from here

Scripts run from anywhere; outputs anchor to the repo root, not the CWD.

## Asset naming (decision 0006)
Three SVG forms per palette+mode dir, named for what they are:
`icon-*` rounded plate · `avatar-*` full-bleed plate · `mark-*` bare glyph, transparent.
`signature-*` is GONE — it meant the rotational variant in BRAND.md and named the
flat mark on disk.
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
signal_yellow (default), electric_blue, amber_utility, terminal_lime, deep_indigo,
slate_mono. 6 × 2 = 12 combinations.
- **signal_yellow light INVERTS** (0004): plate #FFD60A, glyph #111827. The only
  palette whose colour is in the plate. Do not "fix" it to match the others.
- Matrix is not guaranteed symmetric: use `modes_for(key)` / `resolve_modes(key, m)`,
  never a literal `["dark","light"]`.
- Separation lives in the glyph, not the plate. electric_blue and deep_indigo are
  dE 0.3 apart under deuteranopia — never require telling them apart.
See docs/accessibility.md and docs/palette-audit.html.

## Run
```bash
pip install pillow
python scripts/generate_favicon_assets.py --out ./out --palette all --mode both
python scripts/generate_rotational_logo.py --preset plates --palette all --mode both --assets
python scripts/generate_validation_sheet.py
```

## Rotational variant
N copies rotated `--step` degrees apart, opacity ramping to opaque at the front,
each layer back shrunk by `--scale-step`. Front layer stays upright at full opacity.
Canonical construction is **`plates`** (decision 0002): 3 layers, 6°, rear 0.08,
falloff 3.0, recession 0.06 — ramp 0.08 / 0.195 / 1.00. The other seven presets stay
in the CLI as the comparison family that produced the decision; do not ship from them.

## Typography (decision 0007)
Wordmark/lockups: IBM Plex Sans SemiBold, OUTLINED — design-time only, never ships.
UI: Inter. Essays: iA Writer Duo S. Both ship from assets/fonts/.
- **Never** set the mark horizontally beside lowercase `jeffols` — reads "j jeffols".
  Horizontal lockups use "Jeff Olsen"; `jeffols` only ever stacks.
- iA Writer Duo has Reserved Font Names: a subset may NOT keep the name.
- `currentColor` inherits only when the SVG is INLINED, not via `<img>`.
- The typeface does not touch the mark. Geometry is geometry.py, always.

## Design reference
- Canvas 1024×1024, 4× supersample, LANCZOS downscale
- **All geometry is in `geometry.py`.** Nothing else defines a coordinate
- `PLATE_RADIUS` is 174 DESIGN UNITS, not 0.17 of the canvas. 0.17×1024 = 174.08,
  which rounds to a different pixel at 192px and silently shifts every corner
- Hook is stored as path ops so the SVG `d` and the raster polygon come from one
  description. Tessellation is a caller argument: flat renderer snaps to integer
  pixels, rotational must not
- SVG uses inline fills, no CSS variables — intentional for max compatibility

## Guardrails
Prefer simple over clever. Fix root causes, not presentation patches. Do not invent
brand strategy without flagging it. Do not replace the naked mark with the rotational
one. Signal Yellow is not mandatory. Keep contrast accessible. Update all consumers
when canonical asset paths change.
