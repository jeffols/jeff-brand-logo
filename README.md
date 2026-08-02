# jeffols brand system

Source assets, generators, palettes, and usage guidance for the Jeffols visual
identity.

**[`BRAND.md`](BRAND.md) is the strategic source of truth.** Start there for
positioning, brand architecture, and governance. This README covers what is in
the repository and how to run it.

## The mark

A deconstructed lowercase **j** — three geometric pieces, each slightly offset,
like shifted tectonic plates:

- **Dot** — circle, shifted left
- **Stem** — vertical rectangle, centred
- **Hook** — curved base, shifted right

The offset creates tension and motion. Together the pieces read as *j*;
separately they read as abstract geometry. The precise three-part construction is
what makes the mark distinctive — not the letterform itself.

> The shape identifies Jeffols. Colour sets the context.

## Three levels

| Level | | Use for | Assets |
|---|---|---|---|
| **1. Primary mark** | naked deconstructed j | Favicons, avatars, small sizes, monochrome, anywhere echo detail would be lost | `palettes/` |
| **2. Signature variant** | rotational echo j | Hero areas, banners, covers, posters, presentation slides, motion | `palettes-rotational/` |
| **3. Treatments** | glow, watermark, crop, palette, animation | Applied *to* level 1 or 2 | `assets/watermarks/`, `assets/banners/` |

Level 3 is never a logo in its own right. The rotational variant never replaces
the primary mark as the default.

**Size rule:** under 48 px, primary mark only. Between 48 and 80 px, primary
unless you have checked the rotational at that exact size. Favicons always use
the primary mark. Full rules in [`docs/logo-usage.md`](docs/logo-usage.md);
validate against [`docs/size-validation.html`](docs/size-validation.html).

## Palettes

| Palette | Dark | Light | Dark BG | Dark Glyph | Light BG | Light Glyph |
|---|---|---|---|---|---|---|
| **Signal Yellow** (default) | ![](palettes/signal_yellow/dark/favicon-64x64.png) | ![](palettes/signal_yellow/light/favicon-64x64.png) | `#111827` | `#FFD60A` | `#FFD60A` | `#111827` |
| **Electric Blue** | ![](palettes/electric_blue/dark/favicon-64x64.png) | ![](palettes/electric_blue/light/favicon-64x64.png) | `#0B1020` | `#7DD3FC` | `#F6FBFF` | `#005A9C` |
| **Amber Utility** | ![](palettes/amber_utility/dark/favicon-64x64.png) | ![](palettes/amber_utility/light/favicon-64x64.png) | `#1F1B16` | `#FFB000` | `#FFF8E1` | `#8B5E00` |
| **Terminal Lime** | ![](palettes/terminal_lime/dark/favicon-64x64.png) | ![](palettes/terminal_lime/light/favicon-64x64.png) | `#151515` | `#B6FF4D` | `#F7FFE8` | `#3D6600` |
| **Deep Indigo** | ![](palettes/deep_indigo/dark/favicon-64x64.png) | ![](palettes/deep_indigo/light/favicon-64x64.png) | `#190A24` | `#DDB0FF` | `#FBF5FF` | `#4B0082` |
| **Slate Mono** | ![](palettes/slate_mono/dark/favicon-64x64.png) | ![](palettes/slate_mono/light/favicon-64x64.png) | `#0F172A` | `#F8FAFC` | `#F8FAFC` | `#0F172A` |

**Signal Yellow light inverts its dark mode** — the plate carries the yellow and
the glyph is the dark navy ([decision 0004](docs/decisions/0004-signal-yellow-light-inverts.md)).
Every other palette does the reverse. A dark yellow glyph is an olive, and an
olive on cream is Amber Utility, so inverting was the only construction that kept
both palettes distinct at full contrast.

Geometry is constant; palette is contextual. Signal Yellow is the default
recognition palette, not a requirement. Semantic roles per palette are
provisional — see `BRAND.md` section 11.

Measured contrast, palette separation, and colour-blind simulation:
[`docs/accessibility.md`](docs/accessibility.md) and
[`docs/palette-audit.html`](docs/palette-audit.html).

## Two forms of every icon

Both generators emit both forms. Picking the wrong one is the most common
mistake.

**Favicon form** — `favicon-*.png`, `apple-touch-icon.png`, `android-chrome-*.png`.
Rounded-rect plate, transparent outside the radius. Browsers render favicons
as-is.

**Avatar form** — `avatar-512x512.png`, `avatar-1024x1024.png`, `avatar-*.svg`.
Full-bleed opaque square, no rounding, no alpha channel. **Upload this to
Substack, LinkedIn, and GitHub.** They apply their own corner mask, so a
pre-rounded asset fights it, and leftover transparency gets flattened to whatever
the platform assumes — Substack assumes white, which shows as white slivers at
the corners.

## Generated assets

Per palette and mode:

| File | Size | Use |
|---|---|---|
| `favicon.ico` | 16/32/48/64 | Browser tab |
| `favicon-{N}x{N}.png` | 16–512 | General use |
| `apple-touch-icon.png` | 180 | iOS home screen |
| `android-chrome-{192,512}.png` | 192, 512 | Android, PWA |
| `avatar-{512,1024}.png` | 512, 1024 | Social profiles |
| `mark-{512,1024}.png`, `mark-*.svg` | scalable | **Transparent** — no plate |
| `icon-*.svg`, `avatar-*.svg` | scalable | Vector embed, watermark |
| `site.webmanifest` | — | PWA manifest |
| `metadata.json` | — | Palette, colour, and construction reference |

Palette-independent canonicals live in `assets/marks/`:

| File | Use |
|---|---|
| `mark-mono.svg` | `currentColor` — inherits from surrounding CSS |
| `mark-black.svg` / `.png` | Print, engraving, embroidery, single-colour |
| `mark-white.svg` / `.png` | Knockout on any dark surface |

**Transparent marks have no plate**, so the glyph meets whatever the page
supplies. Pick the variant matching the *page*, not your other assets — a
dark-mode glyph on a light background falls under 2:1. See
[`docs/accessibility.md`](docs/accessibility.md).

## Run

```bash
pip install pillow

# Primary mark — all palettes, both modes
python scripts/generate_favicon_assets.py --out ./out --palette all --mode both
python scripts/generate_favicon_assets.py --list-palettes

# Custom colours
python scripts/generate_favicon_assets.py --out ./out --background "#111827" --glyph "#FFD60A"

# Signature variant — canonical construction is "plates" (decision 0002)
python scripts/generate_rotational_logo.py --list-presets
python scripts/generate_rotational_logo.py --preset plates --palette all --mode both --assets

# Palette-independent monochrome marks
python scripts/generate_favicon_assets.py --canonical assets/marks/primary
python scripts/generate_rotational_logo.py --canonical assets/marks/rotational

# Regenerate the CSS watermark from geometry.py
python scripts/generate_favicon_assets.py --watermark assets/watermarks/watermark.css

# Lockups (needs fonttools)
python scripts/generate_lockups.py

# LinkedIn banners (needs headless Chrome)
python scripts/generate_linkedin_banners.py

# Comparison sheets
python scripts/generate_rotational_logo.py --preset-sheet
python scripts/generate_validation_sheet.py        # docs/size-validation.html
python scripts/generate_palette_audit.py           # docs/palette-audit.html
```

## HTML integration

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

`assets/watermarks/watermark.css` is a drop-in page watermark — `body::after`,
data URI, bottom right. It is generated from `scripts/geometry.py`; do not edit
it by hand.

## Layout

```
BRAND.md                      strategic source of truth
docs/                         operational guidance, decision records
  logo-usage.md               which mark, what size, which file
  accessibility.md            measured contrast ratios
  size-validation.html        naked vs rotational at true pixel size
  decisions/                  numbered decision records
scripts/
  geometry.py                 THE mark. Single source of truth for coordinates
  generate_favicon_assets.py  primary mark; also --canonical and --watermark
  generate_rotational_logo.py signature variant; also --canonical
  generate_validation_sheet.py  size + construction comparison sheet
  generate_palette_audit.py     distinctiveness and colour-blind simulation
  generate_linkedin_banners.py  banner compositions (needs headless Chrome)
assets/
  lockups/                    mark + wordmark; wordmark outlined, no font dependency
  fonts/                      Inter + iA Writer Duo (ship), Plex Sans (design-time)
  marks/{primary,rotational}/ palette-independent canonicals (mono, black, white)
  banners/linkedin/           generated banner compositions
  watermarks/watermark.css    generated drop-in page watermark
palettes/<name>/<mode>/       primary mark, per palette and mode
palettes-rotational/…         signature variant, same layout
examples/                     worked applications on real surfaces
explorations/                 not brand assets. Do not ship from here
```

## Licence

Split. The scripts are Apache-2.0 ([`LICENSE`](LICENSE)). The mark and every
generated asset are all rights reserved ([`ASSETS-LICENSE.md`](ASSETS-LICENSE.md)).
Running the generators does not grant rights in the mark they produce.
