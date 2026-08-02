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
| amber_utility | light | `#FFF8E1` | `#8B5E00` | 5.34 | AA |
| terminal_lime | light | `#F7FFE8` | `#3D6600` | 6.59 | AA |
| electric_blue | light | `#F6FBFF` | `#005A9C` | 6.85 | AA |
| amber_utility | dark | `#1F1B16` | `#FFB000` | 9.34 | AAA |
| deep_indigo | dark | `#190A24` | `#DDB0FF` | 10.56 | AAA |
| electric_blue | dark | `#0B1020` | `#7DD3FC` | 11.36 | AAA |
| deep_indigo | light | `#FBF5FF` | `#4B0082` | 12.09 | AAA |
| signal_yellow | dark | `#111827` | `#FFD60A` | 12.57 | AAA |
| signal_yellow | light | `#FFD60A` | `#111827` | 12.57 | AAA — inverted, `0004` |
| terminal_lime | dark | `#151515` | `#B6FF4D` | 15.13 | AAA |
| slate_mono | dark | `#0F172A` | `#F8FAFC` | 17.06 | AAA |
| slate_mono | light | `#F8FAFC` | `#0F172A` | 17.06 | AAA |

## Resolved: signal_yellow light inverts (decisions 0003, 0004)

The light variant measured 2.65:1 and every fix inside the usual pattern
collapsed it into `amber_utility`. `0003` removed it. `0004` restored it by
inverting the dark mode instead — plate `#FFD60A`, glyph `#111827`, 12.57:1.

The analysis below is why darkening the glyph does not work. It is still the
reason not to try it again, and it is the method to reuse when adding or changing
any palette.

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

### Why darkening the glyph was rejected

The obvious fix collapses Signal Yellow into Amber Utility. CIEDE2000 distance
from `amber_utility` light (`#8B5E00`):

| Candidate | Contrast | ΔE vs amber |
|---|---|---|
| `#B8960A` current | 2.65 | 21.2 — distinct |
| `#937808` | 3.98 | 11.0 — close |
| `#806907` | 4.98 | **8.0 — collides** |
| `#776106` | 5.61 | 7.8 — collides |

The two light plates were already `#FFF7E0` vs `#FFF8E1` — **ΔE 0.49**, below
human perception. The low contrast was the only thing separating the palettes.

Adjusting the plate instead is arithmetically impossible: at luminance 0.320 the
glyph cannot reach 3:1 against any lighter background. Pure white gives 2.84:1
and that is the ceiling.

Removing the variant was the only move that did not trade one defect for another.
Recorded in `0003`.

## Palette separation

Contrast is one axis; whether two palettes look like different palettes is
another. CIEDE2000 on glyphs, since the plates carry almost no differentiation.

**Rule of thumb:** under 10 is a collision, 10–20 is close, 20+ reads as
unambiguously different.

Closest pairs:

| Mode | Pair | ΔE | |
|---|---|---|---|
| dark | signal_yellow / amber_utility | **13.1** | closest in the system |
| dark | electric_blue / slate_mono | 21.7 | fine |
| light | deep_indigo / slate_mono | 20.7 | fine |
| light | amber_utility / terminal_lime | 26.8 | fine |

Every other pair is 21.7 or higher. Signal Yellow and Amber Utility are the only
marginal pair, and only in dark mode.

This matters less than it looks: `BRAND.md` section 11 treats palettes as
contextual, one at a time. It would matter if two palettes ever had to be told
apart side by side — a legend, a category key, a matrix of covers. Do not build
one that depends on distinguishing those two.

Dark plates are all near-black (ΔE 2.2 to 9.5 apart) and light plates include two
imperceptible pairs. **Separation lives in the glyph. Do not rely on the plate to
distinguish anything** — with one deliberate exception: `signal_yellow` light
carries its identity in the plate (`0004`), which is why it does not collide with
`amber_utility` the way a darkened glyph would.

### Under colour blindness

Measured with `scripts/generate_palette_audit.py`; see `docs/palette-audit.html`.

| View | Closest pair | ΔE | |
|---|---|---|---|
| normal | signal_yellow / amber_utility | 13.1 | no collisions |
| tritanopia | signal_yellow / amber_utility | 10.4 | no collisions |
| protanopia | electric_blue / deep_indigo | 6.1 | 3 collisions |
| **deuteranopia** | **electric_blue / deep_indigo** | **0.3** | 4 collisions |

`electric_blue` and `deep_indigo` are the same colour to a deuteranope — roughly
6% of men — while being 30.4 apart in normal vision. Nothing reveals this without
simulating it.

Low impact while palettes appear one at a time. **Never build a legend, category
key, or cover grid that requires telling those two apart.**

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
