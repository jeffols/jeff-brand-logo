# Favicon artifacts

Included:
- `generate_favicon_assets.py`
- `source_icon.png`
- `palettes/<palette>/<mode>/`
- `svg_verification.json`
- `svg_render_check.png`

Usage:
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
```
