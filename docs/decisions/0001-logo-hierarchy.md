# 0001 — Logo hierarchy

**Date:** 2026-08-01
**Status:** Accepted

## Decision

Three levels, permanently ranked:

1. **Primary mark** — the naked deconstructed j. The durable identity.
2. **Signature variant** — the rotational echo j. Used deliberately, never as a
   substitute for level 1.
3. **Presentation treatments** — glow, watermark, crop, palette, animation.
   Applied to level 1 or 2. Never a logo in their own right.

The shape identifies Jeffols. Colour sets the context.

## Context

The repository had grown two full asset trees — `palettes/` and
`palettes-rotational/` — with no recorded statement of which one is the logo.
Both were generated, both were current, and `CLAUDE.md` described them as
"pick per surface." A LinkedIn banner used a third construction again. Nothing
said which was canonical, so nothing prevented drift.

## Options considered

**A. Rotational as primary.** It is the more distinctive image and the more
memorable one at large sizes. Rejected: it fails at favicon and avatar sizes,
depends on opacity to read, and its broad design category — letterform with
motion trails — is crowded. The protectable value is the three-part tectonic
construction, which the naked mark states most clearly.

**B. Two co-equal marks, chosen per surface.** This is what the repository
actually did before this record. Rejected: co-equal marks are two brands. It also
gives no rule for the ambiguous middle sizes, which is exactly where the choice
is hard.

**C. Naked primary, rotational as a named variant.** Chosen.

## Rationale

The naked mark has the clearest silhouette, survives one-colour reproduction,
works in print and engraving, and stays recognisable through palette changes. It
is the strongest form to standardise and protect.

The rotational version earns its place by saying something the naked mark cannot:
the echoes read as prior states, accumulated context, motion that leaves
evidence. That is a real brand idea and worth keeping — as a behaviour of the
mark, not a replacement for it.

## Consequences

- The primary mark is the default. Reaching for the rotational one requires a
  reason and enough size.
- Favicons use the primary mark without exception.
- Both asset trees stay generated and current. `palettes/` is canonical;
  `palettes-rotational/` is the variant.
- Wide surfaces are governed by composition rather than by this hierarchy — see
  `docs/logo-usage.md`. The LinkedIn banner's glow-echo composition is a level 3
  treatment, not a fourth mark.
- Downstream repositories must not redraw the mark. `jeffols.github.io` currently
  inlines the geometry twice and is out of compliance; scheduled for Phase 4.
- Trademark strategy follows the hierarchy: the primary mark is the thing to
  protect first. See `docs/legal-and-protection-notes.md`.

## Addendum, 2026-08-01

The consequence above is discharged. `jeffols.github.io` was rebuilt to consume
generated assets and inlines no hand-authored geometry. The count in the original
text is left as written: the audit later found **three** copies, not two, and the
third was a modified mark. That the record undercounted is itself the point, and
`docs/website-direction.md` carries the corrected finding.

## Open

The canonical rotational construction — echo count, angular step, opacity ramp —
is **not** settled by this record. `generate_rotational_logo.py` currently
defaults to `plates-4`, which was a comparison-sheet tag that became a default
without ever being chosen. Decided separately in `0002`, using
`docs/size-validation.html`.
