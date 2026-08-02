# Legal and protection notes

Strategy: `BRAND.md` sections 5, 6, and 21. This file records what is actually in
force and what is still open.

**Not legal advice.** Clearance and registration need a qualified trademark
attorney.

## Licensing, as implemented

Split deliberately across two files.

| File | Covers | Terms |
|---|---|---|
| `LICENSE` | The generator scripts, `assets/watermarks/watermark.css` | Apache-2.0 |
| `ASSETS-LICENSE.md` | The mark, both palette trees, all generated assets | All rights reserved |

Apache-2.0 rather than MIT because of its section 6: it grants copyright and
patent rights while granting **no** trademark rights. On a public repository that
contains a mark intended for registration, a blanket permissive licence on
everything would undercut the claim.

`ASSETS-LICENSE.md` states explicitly that running the generators does not grant
rights in the mark they produce. Without that line, the scripts' licence could be
read as licensing their output.

## Bundled typefaces

Three, all SIL OFL, in `assets/fonts/` with their licence texts.

| Face | Reserved Font Name | Constraint |
|---|---|---|
| Inter | none | subset freely, keep the name |
| iA Writer Duo S | `iA Writer`, `Plex` | **a subset may not keep the name** |
| IBM Plex Sans | `Plex` | design-time only; never ships |

OFL clause 3 forbids a Modified Version from using a Reserved Font Name, and
subsetting produces a Modified Version. Serve iA Writer Duo unmodified, or
subset it and rename the family internally.

Lockup wordmarks are converted to outlines. Embedding glyph outlines in artwork
is not distributing font software, which is the normal reading and standard
practice for logo construction. See decision `0007`.

The typefaces are licensed to their respective authors and are **not** covered by
this repository's asset reservation below.

## Trademark posture

- **jeffols** and the tectonic j are claimed as common-law trademarks.
- All rights reserved, including the right to pursue registration.
- No registration filed.

## What is distinctive

Per `BRAND.md` section 6, the protectable value is specific, not general.

**Strong:** the precise three-part construction — geometric lowercase j, three
separately displaced components, dot shifted left, stem centred, hook shifted
right, consistent tectonic plate-shift logic.

**Weak:** "a geometric letter j." Generic geometric letterforms are common.

**Weak on its own:** "a J with echoes." Letterforms with motion trails, repeated
translucent copies, and neon echo effects are a crowded category. What is
defensible is the tectonic j *carrying* rotated traces of prior states — the
combination, not the echo idea.

Practical consequence: never reduce the rotational variant to a solid J with a
motion trail. The tectonic geometry must stay legible inside it, or the variant
loses the thing that makes it protectable.

## Registration triggers

Revisit separate protection for the rotational variant when it:

- appears repeatedly in public marketing
- functions independently as a source identifier
- has a standardised construction (blocked on decision `0002`)
- carries strategic value beyond decoration

Do not treat every palette, opacity, or echo-count variation as an independent
identity. That dilutes rather than broadens.

## Open questions

- Whether to pursue registration for the primary mark, and in which classes
- Whether the rotational variant warrants separate registration
- Whether a formal clearance search has been run — assume not
- Whether `jeffols` as a word mark is separable from the design mark
- Whether the repository should be renamed `jeffols-brand`, and what that does to
  existing public URLs

## Governance rules in force

From `BRAND.md` section 21, restated as things this repository must do:

- Do not redraw the mark in downstream repositories. Generate or export from
  canonical geometry.
- Keep palette definitions centralised.
- Document every intentional geometry change in a decision record.
- Keep explorations separate from approved assets.
- Do not silently replace approved assets.
- Tag stable asset sets. Current: `v1.0.0`.
