# 0003 — Signal Yellow is dark-only

**Date:** 2026-08-01
**Status:** Accepted

## Decision

`signal_yellow` defines a dark mode only. The light variant
(`#B8960A` on `#FFF7E0`) is removed from the palette table and its generated
assets are deleted.

The palette × mode matrix is no longer symmetric. Generators use `modes_for()`
and `resolve_modes()` rather than assuming both keys exist.

## Context

Signal Yellow light measured 2.65:1 — every other light palette lands between
5.34 and 17.06. It was the only cell in twelve that did not work.

It was never designed. `generate_favicon_assets.py` loops over palette × mode and
emits every cell, so the variant existed because the loop existed. `BRAND.md`
section 11 describes the canonical palette as "Signal Yellow on dark charcoal or
navy" — dark is the definition, and the light cell was an artifact.

## Options considered

**A. Darken the glyph.** The obvious fix, and wrong. Measured against
`amber_utility` light (`#8B5E00`) with CIEDE2000:

| signal_yellow light | Contrast | ΔE vs amber |
|---|---|---|
| `#B8960A` current | 2.65 | 21.2 — distinct |
| `#937808` | 3.98 | 11.0 — close |
| `#806907` | 4.98 | **8.0 — collides** |
| `#776106` | 5.61 | 7.8 — collides |

The two light plates are already `#FFF7E0` vs `#FFF8E1`, **ΔE 0.49** — below the
threshold of human perception. Fixing the contrast would have produced two
palettes with identical backgrounds and glyphs 8 apart. The defect was the only
thing keeping them distinct.

**B. Adjust the plate instead.** Arithmetically impossible. At luminance 0.320
the glyph cannot reach 3:1 against any lighter background — pure white gives
2.84:1, and that is the ceiling. Reaching 3:1 requires a plate *darker* than the
glyph, around `#3A3529`, which is a second dark theme rather than a light one.

**C. Remove the light variant.** Chosen.

**D. Leave it.** Rejected. Logos are exempt from contrast requirements, so this
was defensible, but keeping a cell that is half the contrast of every sibling and
duplicates another palette is carrying a defect for no benefit.

## Rationale

`amber_utility` light already occupies warm-on-cream at 5.34:1, with a plate
indistinguishable from Signal Yellow's. There was never room for both. Amber is
the one that works.

Signal Yellow's recognition value is bound to the dark plate — high contrast,
technical, slightly industrial. Diluted onto cream it was neither recognisable
nor legible.

## Consequences

- `palettes/signal_yellow/light/` and `palettes-rotational/signal_yellow/light/`
  deleted. 38 files.
- `--palette all --mode both` now yields 11 combinations, not 12.
- `--palette signal_yellow --mode light` exits with an explanation rather than a
  `KeyError`. `--mode both` skips the missing mode quietly.
- On light surfaces, use `slate_mono` light or `amber_utility` light. Both are
  correct; neither is Signal Yellow, and that is the point.
- The favicon and avatar forms carry their own opaque plate, so Signal Yellow
  dark still works on any page. The light variant was only needed when a light
  *plate* was wanted specifically.
- `docs/accessibility.md` keeps the measurements and the reasoning.

## Note on method

The failure was invisible in the space the colour was chosen in and obvious in
the space it is measured in. Signal Yellow's light glyph was 24% lighter than its
nearest sibling in HSL and 2.4× brighter in perceived luminance, because yellow
collects 93% of the luminance weighting against blue's 7%.

Any hand-picked multi-hue palette drifts this way. Check luminance and CIEDE2000
separation when adding or changing a palette; neither is visible on a colour
picker.
