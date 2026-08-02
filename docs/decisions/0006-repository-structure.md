# 0006 — Repository structure and asset naming

**Date:** 2026-08-01
**Status:** Accepted

## Decision

Adopt the structure `BRAND.md` section 12 recommends, and rename the plate-form
SVG from `signature-*` to `icon-*`.

```text
scripts/     geometry.py + the five generators
assets/      marks/{primary,rotational}, banners/linkedin, watermarks/
docs/        guidance, decision records, generated comparison sheets
examples/    homepage, linkedin, github, article-covers
palettes/            primary mark, per palette and mode
palettes-rotational/ signature variant, same layout
explorations/        reference/, linkedin-v1/, rotational/
```

## Asset naming

Three SVG forms per palette and mode directory, named for what they are:

| Name | Form |
|---|---|
| `icon-<palette>-<mode>.svg` | rounded plate + glyph |
| `avatar-<palette>-<mode>.svg` | full-bleed plate + glyph |
| `mark-<palette>-<mode>.svg` | bare glyph, transparent |

`signature-*` is gone. It named the flat mark on disk while `BRAND.md` section 5
uses "signature variant" for the rotational one, and the identical filename in
both trees meant two different marks.

The original plan was `signature-*` → `mark-*`. That became impossible when
Phase 2 introduced the transparent export and took the name. `icon-*` is the
better outcome anyway: three forms, three names, each describing the artefact
rather than its status.

## Why `assets/` and `palettes/` are both top-level

`BRAND.md` section 12 lists them as siblings without saying how they differ.
The split adopted here:

- **`palettes*/`** — the generated palette × mode matrix. 12 cells, 22 files each.
- **`assets/marks/`** — palette-independent canonicals only: `currentColor`,
  black, white. Things that have no palette and therefore no cell to live in.

Nothing exists in both. The alternative — `assets/marks/` mirroring the palette
tree — would have duplicated 264 files with no new information.

## Path handling

Generators previously resolved output relative to the working directory, so
moving them into `scripts/` would have silently written into `scripts/` when run
from there. Output defaults are now anchored with
`Path(__file__).resolve().parent.parent`, and every generator produces identical
results run from the repository root or from `scripts/`. Verified both ways.

## Consequences

- **Every public asset path changed.** `v1.0.0` still resolves the old layout;
  anything hotlinking `raw.githubusercontent.com/.../palettes/...` should be
  repointed or pinned to that tag. Tagged `v2.0.0` after the move.
- `watermark.css` moved to `assets/watermarks/`. It is generated — regenerate
  with `--watermark`, do not edit it.
- The seven root-level LinkedIn files from the first banner attempt moved to
  `explorations/linkedin-v1/`. `linkedin-banner.png` was deleted as a
  byte-identical duplicate of `linkedin-banner-dark.png`.
- `bead.jpeg` moved to `explorations/reference/`. It is the reference photo for a
  retired direction, kept deliberately — see the duct-tape note in `0001`'s
  history and the commit `62bee5d`.
- `examples/` is scaffolded and empty. It fills from real surfaces as they are
  built; nothing there may redraw the mark.

## Sequencing

Deliberately last. `BRAND.md` section 12 says not to reorganise working generator
paths until consumers are updated and tested, so this ran after the geometry
extraction and asset work, against a verified baseline, as a single move commit.
