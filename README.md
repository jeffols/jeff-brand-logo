# Signature Favicon & Branding Kit

Personal signature icon for projects by Jeff Olsen. An abstract glyph on a rounded-square background, available in five color palettes with dark and light modes.

## The Icon

The signature mark is a stylized abstract glyph — a vertical stroke with a notched top-left corner and a circular dot at bottom-left. It reads as a bold, geometric maker's mark.

- Source: `source_icon.png` (master raster)
- SVG: `palettes/<palette>/<mode>/signature-<palette>-<mode>.svg` (vector, inline fills, no CSS dependencies)

## Color Palettes

| Palette | Dark | Light | Dark BG | Dark Glyph | Light BG | Light Glyph |
|---|---|---|---|---|---|---|
| **Signal Yellow** (default) | ![](palettes/signal_yellow/dark/favicon-64x64.png) | ![](palettes/signal_yellow/light/favicon-64x64.png) | `#111827` | `#FFD60A` | `#FFF7E0` | `#B8960A` |
| **Electric Blue** | ![](palettes/electric_blue/dark/favicon-64x64.png) | ![](palettes/electric_blue/light/favicon-64x64.png) | `#0B1020` | `#7DD3FC` | `#F6FBFF` | `#005A9C` |
| **Amber Utility** | ![](palettes/amber_utility/dark/favicon-64x64.png) | ![](palettes/amber_utility/light/favicon-64x64.png) | `#1F1B16` | `#FFB000` | `#FFF8E1` | `#8B5E00` |
| **Terminal Lime** | ![](palettes/terminal_lime/dark/favicon-64x64.png) | ![](palettes/terminal_lime/light/favicon-64x64.png) | `#151515` | `#B6FF4D` | `#F7FFE8` | `#3D6600` |
| **Slate Mono** | ![](palettes/slate_mono/dark/favicon-64x64.png) | ![](palettes/slate_mono/light/favicon-64x64.png) | `#0F172A` | `#F8FAFC` | `#F8FAFC` | `#0F172A` |

## Generated Assets

Each palette/mode combo produces:

| File | Size | Use |
|---|---|---|
| `favicon.ico` | 16/32/48/64 | Browser tab |
| `favicon-{N}x{N}.png` | 16–512 | General use |
| `apple-touch-icon.png` | 180 | iOS home screen |
| `android-chrome-{192,512}.png` | 192, 512 | Android/PWA |
| `signature-*.svg` | scalable | Vector embed, watermark |
| `site.webmanifest` | — | PWA manifest |
| `metadata.json` | — | Palette/color reference |

## HTML Integration

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
```

## Watermark

A drop-in CSS watermark is included at `watermark.css`. It places the signature SVG in the bottom-right corner of the page. See the file for usage and customization.

## Usage

```bash
pip install pillow opencv-python numpy

# Default: Signal Yellow dark mode
python generate_favicon_assets.py --source source_icon.png --out ./out

# One palette, both modes
python generate_favicon_assets.py --source source_icon.png --out ./out --palette electric_blue --mode both

# All suggested palettes, both modes
python generate_favicon_assets.py --source source_icon.png --out ./out --palette all --mode both

# Custom colors
python generate_favicon_assets.py --source source_icon.png --out ./out --background "#111827" --glyph "#FFD60A"

# List available palettes
python generate_favicon_assets.py --list-palettes
```

## Repo Structure

```
source_icon.png              # Master raster source
generate_favicon_assets.py   # Asset generator
watermark.css                # Drop-in page watermark
palettes/
  <palette>/
    dark/                    # Dark mode assets + metadata
    light/                   # Light mode assets + metadata
```
