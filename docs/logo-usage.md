# Logo usage

Strategy and rationale: `BRAND.md` sections 4 to 8. This file is the operational
rule — what to reach for, at what size, from which path.

## The three levels

| Level | Name | What it is | Where it lives |
|---|---|---|---|
| 1 | Primary mark | Naked deconstructed j. Dot, stem, hook. | `palettes/<palette>/<mode>/` |
| 2 | Signature variant | Rotational echo j. Same geometry, rotated traces behind it. | `palettes-rotational/<palette>/<mode>/` |
| 3 | Treatments | Glow, watermark, crop, palette change, animation. | `assets/watermarks/`, `assets/banners/` |

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
| Substack, LinkedIn, GitHub avatar | `avatar-512x512.png` or `avatar-1024x1024.png`, **light mode** | full-bleed, opaque, no alpha |
| Vector embed, print | `icon-<palette>-<mode>.svg` | inline fills, no CSS variables |
| Page watermark | `assets/watermarks/watermark.css` | `body::after`, data URI |

**Never upload a favicon PNG as an avatar.** The favicon form is a rounded plate
on transparency. Substack, LinkedIn, and GitHub apply their own corner mask, so a
pre-rounded asset fights theirs, and the leftover transparent corners get
flattened to whatever the platform assumes. Substack assumes white, which shows
as white slivers. Use the `avatar-*` files.

### Avatar mode: light on light-first platforms

**Use the light-mode avatar on Substack, LinkedIn, and GitHub.** For
`signal_yellow` that is the yellow plate with the dark glyph, decision `0004`.

An avatar plate carries its own background, so it is either a hard block against
the page or it dissolves into it. There is no middle. Rendered at 40 to 96 px on
both page themes:

| Avatar | On white | On a dark page |
|---|---|---|
| `signal_yellow` dark | stark block, 17.74 plate against page | plate dissolves, 1.02 |
| `signal_yellow` light | reads clearly | strong block, 12.33 |

The dark plate is the only variant with a bad state, and it has two. The light
plate holds on both, which matters because every one of these platforms lets the
reader choose a theme.

It is also better recognition behaviour. Signal Yellow is the recognition palette,
so leading with yellow is what makes the avatar findable in a crowded list.
Leading with charcoal makes the yellow a detail inside a dark square.

**The plate contrast number is the wrong tool here.** `signal_yellow` light
measures 1.41 against white, which reads as invisible and is not. Contrast ratio
is luminance only and hue is not part of it, so a saturated yellow separates from
white by chroma. Render it before trusting the number. See `docs/accessibility.md`.

The site favicon stays `signal_yellow` **dark**, because the site's own page is
`#111827`. Match the surface, not the sibling asset.

## Lockups

Mark plus wordmark. Two constructions only — decision `0007`.

| Construction | Text | File |
|---|---|---|
| Horizontal | **Jeff Olsen** | `assets/lockups/lockup-horizontal-*.svg` |
| Stacked | **jeffols** | `assets/lockups/lockup-stacked-*.svg` |

**Never set the mark horizontally beside lowercase `jeffols`.** The mark is a
lowercase j and the word starts with one, so side by side they read as
*"j jeffols"* — the mark stops being a symbol and becomes a letter. The capital
J in the full name breaks the echo, which is why horizontal lockups use
**Jeff Olsen** and the compact brand only ever stacks.

The wordmark is IBM Plex Sans SemiBold converted to outlines, so lockups carry
no font dependency. Do not re-set them in live text.

### currentColor needs inlining

`lockup-*-mono.svg` and `assets/marks/*/mark-mono.svg` use `fill="currentColor"`.
That inherits **only when the SVG is inlined into the HTML**. Referenced through
`<img src="...">` the SVG is an isolated document with no parent colour and the
mark renders black.

Inline the mono variants. Use a palette variant for `<img>`.

## Typography

| Register | Face | Ships to the web |
|---|---|---|
| Wordmark, lockups | IBM Plex Sans SemiBold, outlined | No — design-time only |
| UI, navigation, headings | Inter | Yes |
| Essays, long-form | iA Writer Duo S | Yes |

Files in `assets/fonts/`. **Do not ship a subset of iA Writer Duo under its own
name** — it carries Reserved Font Names and OFL clause 3 forbids it. Serve it
unmodified, or subset and rename. Inter has no reserved name and may be subset
freely. See `docs/legal-and-protection-notes.md`.

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
