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
| **3. Treatments** | glow, watermark, crop, palette, animation | Applied *to* level 1 or 2 | `watermark.css`, `linkedin-banners/` |

Level 3 is never a logo in its own right. The rotational variant never replaces
the primary mark as the default.

**Size rule:** under 48 px, primary mark only. Between 48 and 80 px, primary
unless you have checked the rotational at that exact size. Favicons always use
the primary mark. Full rules in [`docs/logo-usage.md`](docs/logo-usage.md);
validate against [`docs/size-validation.html`](docs/size-validation.html).

## Palettes

| Palette | Dark | Light | Dark BG | Dark Glyph | Light BG | Light Glyph |
|---|---|---|---|---|---|---|
| **Signal Yellow** (default) | ![](palettes/signal_yellow/dark/favicon-64x64.png) | — | `#111827` | `#FFD60A` | dark-only | — |
| **Electric Blue** | ![](palettes/electric_blue/dark/favicon-64x64.png) | ![](palettes/electric_blue/light/favicon-64x64.png) | `#0B1020` | `#7DD3FC` | `#F6FBFF` | `#005A9C` |
| **Amber Utility** | ![](palettes/amber_utility/dark/favicon-64x64.png) | ![](palettes/amber_utility/light/favicon-64x64.png) | `#1F1B16` | `#FFB000` | `#FFF8E1` | `#8B5E00` |
| **Terminal Lime** | ![](palettes/terminal_lime/dark/favicon-64x64.png) | ![](palettes/terminal_lime/light/favicon-64x64.png) | `#151515` | `#B6FF4D` | `#F7FFE8` | `#3D6600` |
| **Deep Indigo** | ![](palettes/deep_indigo/dark/favicon-64x64.png) | ![](palettes/deep_indigo/light/favicon-64x64.png) | `#190A24` | `#DDB0FF` | `#FBF5FF` | `#4B0082` |
| **Slate Mono** | ![](palettes/slate_mono/dark/favicon-64x64.png) | ![](palettes/slate_mono/light/favicon-64x64.png) | `#0F172A` | `#F8FAFC` | `#F8FAFC` | `#0F172A` |

**Signal Yellow is dark-only** ([decision 0003](docs/decisions/0003-signal-yellow-is-dark-only.md)).
Its light variant sat at 2.65:1 against a sibling range of 5.34 to 17.06, and
darkening it collapsed it into Amber Utility. On light surfaces use Slate Mono or
Amber Utility. The palette matrix is therefore not symmetric — generators use
`modes_for()` rather than assuming both modes exist.

Geometry is constant; palette is contextual. Signal Yellow is the default
recognition palette, not a requirement. Semantic roles per palette are
provisional — see `BRAND.md` section 11. Measured contrast and palette separation:
[`docs/accessibility.md`](docs/accessibility.md).

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
| `signature-*.svg`, `avatar-*.svg` | scalable | Vector embed, watermark |
| `site.webmanifest` | — | PWA manifest |
| `metadata.json` | — | Palette, colour, and construction reference |

## Run

```bash
pip install pillow

# Primary mark — all palettes, both modes
python generate_favicon_assets.py --out ./out --palette all --mode both
python generate_favicon_assets.py --list-palettes

# Custom colours
python generate_favicon_assets.py --out ./out --background "#111827" --glyph "#FFD60A"

# Signature variant — canonical construction is "plates" (decision 0002)
python generate_rotational_logo.py --list-presets
python generate_rotational_logo.py --preset plates --palette all --mode both --assets

# Comparison sheets
python generate_rotational_logo.py --preset-sheet
python generate_validation_sheet.py        # docs/size-validation.html
```

## HTML integration

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

`watermark.css` is a drop-in page watermark — `body::after`, data URI, bottom
right. See the file for customisation.

## Layout

```
BRAND.md                      strategic source of truth
docs/                         operational guidance, decision records
  logo-usage.md               which mark, what size, which file
  accessibility.md            measured contrast ratios
  size-validation.html        naked vs rotational at true pixel size
  decisions/                  numbered decision records
generate_favicon_assets.py    primary mark generator
generate_rotational_logo.py   signature variant generator
generate_validation_sheet.py  comparison sheet builder
generate_linkedin_banners.py  banner compositions (needs headless Chrome)
watermark.css                 drop-in page watermark
palettes/<name>/<mode>/       primary mark, per palette and mode
palettes-rotational/…         signature variant, same layout
linkedin-banners/             generated banner compositions
explorations/                 not brand assets. Do not ship from here
```

## Licence

Split. The scripts are Apache-2.0 ([`LICENSE`](LICENSE)). The mark and every
generated asset are all rights reserved ([`ASSETS-LICENSE.md`](ASSETS-LICENSE.md)).
Running the generators does not grant rights in the mark they produce.
