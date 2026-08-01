# 0004 — Signal Yellow light inverts the dark mode

**Date:** 2026-08-01
**Status:** Accepted
**Supersedes:** `0003`

## Decision

`signal_yellow` has a light mode again, built by inverting the dark mode rather
than by darkening the glyph.

| Mode | Plate | Glyph | Contrast |
|---|---|---|---|
| dark | `#111827` | `#FFD60A` | 12.57 |
| light | `#FFD60A` | `#111827` | 12.57 |

Two colours, swapped. No new colour enters the system.

## Context

`0003` removed the light variant because it measured 2.65:1 and every fix
collapsed it into `amber_utility`. That analysis was correct and still holds —
see `0003` for the numbers. What it missed was an assumption.

Every palette in the system puts its colour in the **glyph** and a neutral in the
**plate**. Working inside that pattern, a light Signal Yellow required a dark
yellow glyph. A dark yellow is an olive. An olive on cream is Amber Utility.
There was no room for both, so the conclusion was to delete one.

The assumption was the pattern itself.

## Rationale

Yellow's character is its brightness. Darkening it to make it legible destroys
the thing that makes it Signal Yellow — the result was neither recognisable nor
legible. Inverting keeps the brightness where it belongs and moves the contrast
burden to the glyph, which is already a dark navy that works.

Measured against the alternatives:

| Option | Contrast | ΔE vs amber plate | ΔE vs slate plate |
|---|---|---|---|
| **invert** `#FFD60A` / `#111827` | **12.57** | 24.2 | 31.8 |
| softer `#FFE066` / `#111827` | 13.61 | 19.5 | 28.1 |
| paler `#FFEFA8` / `#2B2410` | 13.33 | 12.0 | 21.8 |
| darkened glyph (`0003`, rejected) | 4.98 | **0.5** | 10.8 |

The inversion is also the most robust under colour vision deficiency, because the
identity now rests on a large bright field rather than on a hue: ΔE 23.4 from the
amber plate under deuteranopia, 24.4 under protanopia.

## Consequences

- `palettes/signal_yellow/light/` and `palettes-rotational/signal_yellow/light/`
  regenerated. The matrix is 6 × 2 again; `--palette all --mode both` yields 12.
- **Signal Yellow light is the only palette whose colour lives in the plate.**
  The general rule in `docs/accessibility.md` — separation lives in the glyph —
  has one exception, and this is it.
- The transparent export of Signal Yellow light is a dark navy mark, which is the
  correct thing to place on a light page.
- `modes_for()` and `resolve_modes()` are retained even though every palette now
  defines both modes. They cost little, they give a real error instead of a
  `KeyError`, and the matrix is not guaranteed symmetric in future.
- `0003` is superseded but kept. Its analysis of why the obvious fix fails is the
  reason this one exists.

## Note on method

The fix took four attempts because the first three searched inside a constraint
nobody had stated. When every option in a space is bad, check whether the space
is the problem before concluding the feature is.
