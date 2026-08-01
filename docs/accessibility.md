# Accessibility

Strategy: `BRAND.md` section 11. This file holds the measured numbers and the
rules that follow from them.

Ratios are WCAG 2.1 relative luminance, glyph against its own plate. Recompute
with any palette change.

## What the thresholds mean, and which apply

A contrast ratio runs 1:1 (identical) to 21:1 (black on white). It compares
perceived lightness only — hue is not part of it.

| Reference | Requires | Applies to |
|---|---|---|
| SC 1.4.3 "AA" | 4.5:1 body text, 3:1 large text | Text |
| SC 1.4.6 "AAA" | 7:1 body, 4.5:1 large | Text |
| SC 1.4.11 | 3:1 | Icons, UI components, meaningful graphics |

**Logos are exempt.** SC 1.4.11 carves out "logotypes: parts of a logo or brand
name have no minimum contrast requirement," and SC 1.4.3 does the same for text
in a logo. Nothing in this repository is *required* to meet any of these numbers.

They are still worth measuring. A mark that is hard to see is hard to see whether
or not a standard obliges it, and the favicon does real interface work at 16 px.
Treat the numbers below as legibility evidence, not as compliance results.

## Glyph on its own plate

| Palette | Mode | Background | Glyph | Ratio | Status |
|---|---|---|---|---|---|
| signal_yellow | light | `#FFF7E0` | `#B8960A` | **2.65** | **outlier — see below** |
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

## Open finding: signal_yellow light is an outlier

`#B8960A` on `#FFF7E0` is **2.65:1**. Every other light mode lands between 5.34
and 17.06. It is not a standards failure — logos are exempt — but it is roughly
half the contrast of the next-lowest palette, in the canonical default.

Introduced in `e8d3e12` (2026-06-21).

### Why this one and not the others

The palettes are not generated from a formula. Backgrounds *are* systematic —
every light plate is a ~97% lightness tint of its own hue. The glyphs are
hand-picked, and that is where the inconsistency lives.

Two effects compound:

| Palette (light) | Glyph | HSL lightness | Perceived luminance |
|---|---|---|---|
| signal_yellow | `#B8960A` | **38.0** | **0.320** |
| electric_blue | `#005A9C` | 30.6 | 0.097 |
| amber_utility | `#8B5E00` | 27.3 | 0.135 |
| deep_indigo | `#4B0082` | 25.5 | 0.031 |
| terminal_lime | `#3D6600` | 20.0 | 0.105 |
| slate_mono | `#0F172A` | 11.2 | 0.009 |

**1. It is the lightest glyph chosen.** 38.0 against a next-highest of 30.6.

**2. Yellow converts lightness into luminance faster than any other hue.**
Perceived luminance weights green at 0.7152, red at 0.2126, blue at 0.0722.
Yellow is red plus green, so it collects 93% of the available weight; blue
collects 7%. At equal HSL lightness a yellow is far brighter to the eye than a
blue.

So signal_yellow is 24% lighter than its nearest sibling in the space a designer
picks colours in, and **2.4× brighter** in the space contrast is measured in. The
gap is invisible while choosing and obvious when measured.

This is the standard trap in hand-tuned palettes, not a mistake specific to this
one. Any palette picked by eye across multiple hues will drift this way unless
luminance is checked.

### Consequence

Limited today: the light plate is opaque, so the mark is low-contrast but
present. It becomes material when the transparent mark ships and the glyph meets
arbitrary page backgrounds, and it is already visible at 16 px where the hook
softens into the plate.

Candidate replacements, same hue, darkened:

| Candidate | Ratio | Note |
|---|---|---|
| `#937808` | 3.98 | still reads light; below every sibling |
| `#806907` | 4.98 | inside the sibling band, still recognisably yellow |
| `#776106` | 5.61 | matches amber_utility light (5.34); arguably no longer yellow |

**Recommendation: `#806907`** — the darkest value that still reads as the same
colour family as the dark mode, which matters because both modes have to be
recognisable as one palette.

**Doing nothing is defensible.** The mark is exempt, the plate is opaque, and
brand recognition is a real argument against darkening the signature colour. The
case for changing it is consistency with the other five palettes and legibility
at favicon sizes, not compliance.

Either way it is a palette decision: it needs a decision record and sign-off
before Phase 2 regenerates anything.

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
