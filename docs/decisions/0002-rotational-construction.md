# 0002 — Canonical rotational construction

**Date:** 2026-08-01
**Status:** Accepted
**Supersedes:** the undocumented `plates-4` default

## Decision

The canonical rotational echo mark is **`plates`** — three layers.

| Parameter | Value |
|---|---|
| Layers | 3 |
| Angular step | 6° |
| Rear opacity floor | 0.08 |
| Falloff (gamma) | 3.0 |
| Recession (scale step) | 0.06 |
| Pivot | plate centre, `(512, 512)` |
| Opacity ramp, back to front | 0.080 · 0.195 · 1.000 |

The front layer stays upright at full opacity. Everything behind it is a
fading, rotated, slightly smaller echo.

```bash
python generate_rotational_logo.py --preset plates --palette all --mode both --assets
```

## Context

`generate_rotational_logo.py` shipped eight presets built as a comparison family,
each moving one axis from the three-layer original. `plates-4` became the
effective default and was described in `CLAUDE.md` as "chosen," but no decision
was ever made — the tag came off a sample sheet. `BRAND.md` section 23 still
listed echo count and spacing as open.

Decision `0001` deliberately left this open and pointed here.

## Options considered

All eight presets were rendered side by side at 512, 64, 32 and 16 px, in both
dark and light Signal Yellow, in `docs/size-validation.html`, and judged against
the section 9 success criteria.

**`plates-4`** — four layers, ramp 0.08 / 0.11 / 0.35 / 1.00. The incumbent.
Rejected: the rear two layers sit 0.03 apart at the bottom of the range and merge
into a single soft smear. It pays for a fourth layer and does not get a fourth
plate.

**`plates-even`** — falloff 0.8, ramp 0.08 / 0.61 / 1.00. The middle plate reads
as a genuine plate. Rejected: at 0.61 the echo starts competing with the front
mark rather than sitting behind it, which weakens "keeps the frontmost mark
dominant."

**`plates-bloom`**, **`plates-flat`**, **`plates-tight`**, **`plates-wide`**,
**`plates-deep`** — single-axis variants on recession, step angle, and layer
count. Each isolates one parameter usefully but none improved on the original
against the criteria.

**`plates`** — three layers, ramp 0.08 / 0.195 / 1.00. Chosen.

## Rationale

Three layers give one clearly readable echo and one faint trace. That is the
minimum needed to communicate *prior state* rather than *motion blur*, and
`BRAND.md` section 9 is explicit that the simplest version which communicates the
idea should win.

The fourth layer in `plates-4` added density without adding legibility. Two
layers below 0.12 opacity are not two echoes; they are one shadow with soft
edges.

At 6° the hook stays clean. The echo separates enough to read as a distinct
plate, and not so much that the three components stop reading as one letterform.

## Consequences

- `palettes-rotational/` regenerated at three layers. `metadata.json` in every
  directory records the construction, so any asset can be traced back to this
  record.
- `plates-4`'s preset label no longer claims to be the pick. All eight presets
  stay in the CLI as the comparison family that produced this decision — they are
  how the choice can be re-examined, and deleting them would leave the record
  unfalsifiable.
- The construction is now standardised, which is one of the four triggers in
  `docs/legal-and-protection-notes.md` for considering separate protection of the
  rotational variant.
- Unblocks the motion identity in `docs/website-direction.md`: echoes appear,
  components rotate toward alignment, echoes fade, primary mark remains.
- Closes one of the open items in `BRAND.md` section 23.

## Not settled here

The minimum size at which the rotational mark may be used. Section 1 of
`docs/size-validation.html` tests it; `docs/logo-usage.md` currently carries the
provisional 48/80 px thresholds from `BRAND.md` section 8.
