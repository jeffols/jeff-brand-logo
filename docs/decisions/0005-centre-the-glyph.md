# 0005 — Centre the glyph in the plate

**Date:** 2026-08-01
**Status:** Accepted

## Decision

Shift the glyph **+42 units right** in the 1024 design space, centring its
bounding box on the canvas.

| | Before | After |
|---|---|---|
| Glyph bbox | x 280..660 | x 322..702 |
| Bbox centre | 470 | **512** |
| Margins | 280 left / 364 right | **322 / 322** |

Implemented as `geometry.GLYPH_DX`. Set it to 0 to reproduce pre-0005 assets.

## This is framing, not geometry

The three shapes and their positions relative to one another are untouched. Only
the padding around them changes. `BRAND.md` section 21 requires documenting every
intentional geometry change; this is not one, but it changes every generated
asset, so it gets a record.

## Context

Noticed on a Substack avatar, where the circular crop makes the imbalance
plainer than the square plate does. Measurement confirmed it: the bbox sat 42
units left of centre, 4.1% of the canvas.

Two things made it subtle rather than obvious. The **bounding box** centre is 470,
but the **area-weighted centroid** is 503 — the stem's mass at x 540 pulls right,
so the eye reads somewhere between the two.

## The second reading

The mark is also read as a figure seated in profile: dot as head, stem as torso,
hook as legs and seat. The hook extends to x 280 while the stem and dot begin at
460, so the figure faces **left**.

Photographic framing gives a subject lead room — more space in the direction it
faces. The mark had the opposite: 364 units behind, 280 in front. So the letterform
reading ("it looks off-centre") and the figure reading ("it needs room in front")
both asked for the same correction, which is why this is +42 and not a compromise.

## Options considered

| Option | Shift | Margins | |
|---|---|---|---|
| leave it | 0 | 280 / 364 | reads left; lead room reversed |
| **centred** | **+42** | **322 / 322** | chosen |
| lead 55/45 | +74 | 354 / 290 | genuine lead room |
| lead 60/40 | +106 | 386 / 258 | classic nose room |

Rendered side by side, circle-masked and square, before choosing.

**Against changing anything:** typographically a lowercase j is positioned by its
stem with the descender overhanging left, so the original framing was the natural
letterform position. Rejected because the imbalance is visible in the circular
crops that most profile surfaces apply, and those are where the mark does the
most work.

**Against +74 and +106:** both hold up in a circle but begin to read
right-shifted in the square plate. Lead room is a photographic convention for
subjects moving through a frame; a logo wants to feel stable. Removing the
reversed bias is worth doing, committing to a photographic one is not.

## Consequences

- Every raster and vector in `palettes/`, `palettes-rotational/` and
  `assets/marks/` regenerated. This is the first change since `v1.0.0` that moves
  pixels in existing files.
- Assets already published elsewhere (the site, Substack, LinkedIn) are now 42
  units out of register with the repository. Not urgent — the difference is 4% —
  but re-upload when convenient.
- The rotational variant rotates about the plate centre (512, 512), which is
  unchanged, so the echo geometry is unaffected.

## Not settled here

**Vertical.** The area-weighted centroid sits at y 590, seventy-eight units below
canvas centre — nearly twice the horizontal offset that prompted this. The bbox
centre says the opposite, 490, twenty-two units above. Same two-centres problem,
larger magnitude, and deliberately left alone so this change could be judged on
its own.
