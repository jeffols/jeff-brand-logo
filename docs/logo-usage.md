# Logo usage

Strategy and rationale: `BRAND.md` sections 4 to 8. This file is the operational
rule — what to reach for, at what size, from which path.

## The three levels

| Level | Name | What it is | Where it lives |
|---|---|---|---|
| 1 | Primary mark | Naked deconstructed j. Dot, stem, hook. | `palettes/<palette>/<mode>/` |
| 2 | Signature variant | Rotational echo j. Same geometry, rotated traces behind it. | `palettes-rotational/<palette>/<mode>/` |
| 3 | Treatments | Glow, watermark, crop, palette change, animation. | `watermark.css`, `linkedin-banners/` |

Level 3 is applied *to* level 1 or 2. It is never a third logo.

## Which mark

**Square or near-square surface** — pick by size, using the table below.

**Wide surface** (banner, cover, hero strip) — the aspect ratio is doing the
expressive work, so the composition is the variant. The LinkedIn banner's
scale-and-glow echo composition is approved for these. It is not a competing
mark; it is a level 3 treatment of the primary mark in a wide frame.

**Any size where echo detail is lost** — primary mark. No exceptions.

## Size rule

Validate with `docs/size-validation.html` before changing this table.

| Rendered size | Use |
|---|---|
| Under 48 px | Primary mark only |
| 48 to 80 px | Primary mark. Rotational only if you have checked it at that exact size |
| Over 80 px | Either |
| Favicon, any size | Primary mark, always |

If the echoes read as blur, shadow, poor registration, or compression artifacts,
you are below the threshold. Drop to the primary mark.

## Which file

| Surface | File | Why |
|---|---|---|
| Browser tab | `favicon.ico` | 16/32/48/64 in one file |
| Browser, modern | `favicon-<N>x<N>.png` | rounded plate, transparent outside the radius |
| iOS home screen | `apple-touch-icon.png` | 180 px |
| Android, PWA | `android-chrome-<192\|512>.png` + `site.webmanifest` | |
| Substack, LinkedIn, GitHub avatar | `avatar-512x512.png` or `avatar-1024x1024.png` | full-bleed, opaque, no alpha |
| Vector embed, print | `signature-<palette>-<mode>.svg` | inline fills, no CSS variables |
| Page watermark | `watermark.css` | `body::after`, data URI |

**Never upload a favicon PNG as an avatar.** The favicon form is a rounded plate
on transparency. Substack, LinkedIn, and GitHub apply their own corner mask, so a
pre-rounded asset fights theirs, and the leftover transparent corners get
flattened to whatever the platform assumes. Substack assumes white, which shows
as white slivers. Use the `avatar-*` files.

## Palette

Geometry is constant. Palette is contextual. Signal Yellow is the default
recognition palette, not a requirement.

Semantic roles are provisional (`BRAND.md` section 11) — treat them as a working
hypothesis until repeated use proves them. Do not use colour alone to distinguish
content categories.

Check `docs/accessibility.md` before using a palette on a new surface. One
palette/mode pair currently fails contrast.

## Do not

- Redraw the mark by hand. Generate it. See `docs/decisions/0001-logo-hierarchy.md`.
- Replace the primary mark with the rotational one as the default.
- Distort component geometry with a treatment.
- Treat a palette, opacity, or echo-count change as a new logo.
- Add a glow that the mark needs in order to be readable.
