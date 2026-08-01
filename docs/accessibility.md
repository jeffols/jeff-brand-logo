# Accessibility

Strategy: `BRAND.md` section 11. This file holds the measured numbers and the
rules that follow from them.

Ratios are WCAG 2.1 relative luminance, glyph against its own plate. Recompute
with any palette change.

## Glyph on its own plate

Applicable threshold for a logo is **SC 1.4.11 non-text contrast, 3.0:1**. Text
thresholds (4.5 AA, 7.0 AAA) are shown because the mark sits next to wordmarks
and is used at text-adjacent sizes.

| Palette | Mode | Background | Glyph | Ratio | Status |
|---|---|---|---|---|---|
| signal_yellow | light | `#FFF7E0` | `#B8960A` | **2.65** | **FAILS 1.4.11** |
| amber_utility | light | `#FFF8E1` | `#8B5E00` | 5.34 | AA |
| terminal_lime | light | `#F7FFE8` | `#3D6600` | 6.59 | AA |
| electric_blue | light | `#F6FBFF` | `#005A9C` | 6.85 | AA |
| amber_utility | dark | `#1F1B16` | `#FFB000` | 9.34 | AAA |
| deep_indigo | dark | `#190A24` | `#DDB0FF` | 10.56 | AAA |
| electric_blue | dark | `#0B1020` | `#7DD3FC` | 11.36 | AAA |
| deep_indigo | light | `#FBF5FF` | `#4B0082` | 12.09 | AAA |
| signal_yellow | dark | `#111827` | `#FFD60A` | 12.57 | AAA |
| terminal_lime | dark | `#151515` | `#B6FF4D` | 15.13 | AAA |
| slate_mono | dark | `#0F172A` | `#F8FAFC` | 17.06 | AAA |
| slate_mono | light | `#F8FAFC` | `#0F172A` | 17.06 | AAA |

## Open finding: signal_yellow light fails

`#B8960A` on `#FFF7E0` is **2.65:1**, below the 3.0 non-text minimum. It is the
only failing pair, and it is in the canonical default palette. Every other light
mode clears 5.3.

Introduced in `e8d3e12` (2026-06-21), not by any recent change.

Impact is limited today because the light plate is opaque — the mark is still
*visible*, just low contrast. It becomes a real problem the moment the
transparent mark ships and the glyph sits directly on page backgrounds.

Candidate replacements, same hue, darkened:

| Candidate | Ratio | Note |
|---|---|---|
| `#937808` | 3.98 | clears 1.4.11, still light |
| `#806907` | 4.98 | clears AA text, closest to sibling palettes |
| `#776106` | 5.61 | matches amber_utility light (5.34) |

**Recommendation: `#806907`.** Changing it is a palette decision, so it needs a
decision record and Jeff's sign-off before Phase 2 regenerates anything.

## Transparent mark rule

When the mark ships without its plate, the glyph colour is being asked to work
against an unknown background. It usually cannot.

Glyph directly on a white or black page:

| Palette | Mode | On white | On black |
|---|---|---|---|
| slate_mono | dark | 1.05 | 20.07 |
| terminal_lime | dark | 1.21 | 17.40 |
| signal_yellow | dark | 1.41 | 14.88 |
| electric_blue | dark | 1.67 | 12.60 |
| deep_indigo | dark | 1.79 | 11.73 |
| amber_utility | dark | 1.83 | 11.46 |
| signal_yellow | light | 2.84 | 7.40 |
| electric_blue | light | 7.14 | 2.94 |
| terminal_lime | light | 6.78 | 3.10 |
| deep_indigo | light | 12.95 | 1.62 |
| amber_utility | light | 5.68 | 3.70 |
| slate_mono | light | 17.85 | 1.18 |

**Rule: a dark-mode glyph on a light background is invisible, and the reverse.**
Every dark-mode glyph falls under 2.0 on white. Pick the transparent variant that
matches the *page*, not the one that matches your other assets.

`slate_mono` is the safe choice when the background is unknown or user-themed:
its two modes are exact inverses, so shipping both covers every case.

## Not yet tested

- Colour-blind simulation (deuteranopia, protanopia, tritanopia)
- Social-platform compression (LinkedIn and Substack re-encode uploads)
- Print viability, CMYK conversion
- The rotational mark's echo layers, which sit at 0.08 and 0.195 opacity and are
  not intended to meet contrast minimums — they are texture, not information

The last point matters: the echoes must never carry meaning that the front layer
does not also carry.
