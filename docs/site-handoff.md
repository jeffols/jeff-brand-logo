# Site handoff

What `jeffols.github.io` copies from this repository, and where each file goes.

This is the interface between the two repos. The brand repository owns the mark,
the palettes, the typography, and the rules. The website repository owns
implementation, content, deployment, and **copies of the assets it needs to
deploy** — nothing more. See `BRAND.md` section 12.

Source paths assume the brand repo at `../jeff-brand-logo`. Destination paths
assume the site serves from its root.

## Copy list

### Favicon package

Signal Yellow dark is the canonical recognition palette.

| From | To |
|---|---|
| `palettes/signal_yellow/dark/favicon.ico` | `/favicon.ico` |
| `palettes/signal_yellow/dark/favicon-16x16.png` | `/favicon-16x16.png` |
| `palettes/signal_yellow/dark/favicon-32x32.png` | `/favicon-32x32.png` |
| `palettes/signal_yellow/dark/apple-touch-icon.png` | `/apple-touch-icon.png` |
| `palettes/signal_yellow/dark/android-chrome-192x192.png` | `/android-chrome-192x192.png` |
| `palettes/signal_yellow/dark/android-chrome-512x512.png` | `/android-chrome-512x512.png` |
| `palettes/signal_yellow/dark/site.webmanifest` | `/site.webmanifest` |

### Marks and lockups

| From | To | Used for |
|---|---|---|
| `assets/lockups/lockup-horizontal-mono.svg` | inline in HTML | Header |
| `assets/marks/primary/mark-mono.svg` | inline in HTML | Footer |
| `palettes-rotational/signal_yellow/dark/mark-1024x1024.png` | `/assets/hero-mark.png` | Hero background |
| `assets/social/social-signal_yellow-dark-1200x630.png` | `/assets/social-preview.png` | Open Graph |
| `assets/watermarks/watermark.css` | `/assets/watermark.css` | Optional page watermark |

### Fonts

| From | To |
|---|---|
| `assets/fonts/InterVariable.ttf` | `/assets/fonts/` (convert to woff2) |
| `assets/fonts/iAWriterDuoS-Regular.ttf` | `/assets/fonts/` (convert to woff2) |
| `assets/fonts/iAWriterDuoS-Bold.ttf` | `/assets/fonts/` (convert to woff2) |
| `assets/fonts/Inter-LICENSE.txt` | `/assets/fonts/` |
| `assets/fonts/iAWriterDuoS-LICENSE.md` | `/assets/fonts/` |

Ship the licence files. OFL requires it.

## Head block

```html
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<meta property="og:title" content="Jeff Olsen">
<meta property="og:url" content="https://www.jeffols.com">
<meta property="og:image" content="https://www.jeffols.com/assets/social-preview.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://www.jeffols.com/assets/social-preview.png">
```

`og:image` must be an absolute URL. Relative paths silently fail on most
platforms.

## Fonts in CSS

```css
@font-face { font-family: 'Inter'; font-weight: 100 900; font-display: swap;
             src: url('/assets/fonts/InterVariable.woff2') format('woff2'); }
@font-face { font-family: 'iA Writer Duo S'; font-weight: 400; font-display: swap;
             src: url('/assets/fonts/iAWriterDuoS-Regular.woff2') format('woff2'); }
@font-face { font-family: 'iA Writer Duo S'; font-weight: 700; font-display: swap;
             src: url('/assets/fonts/iAWriterDuoS-Bold.woff2') format('woff2'); }

:root {
  --font-ui:    'Inter', system-ui, sans-serif;
  --font-essay: 'iA Writer Duo S', ui-monospace, monospace;
}
```

Inter for interface, navigation and headings. iA Writer Duo S for essays and
long-form. Decision `0007`.

## Which mark where

| Slot | Asset | Rule |
|---|---|---|
| Header | `lockup-horizontal-mono.svg`, inlined | Never beside lowercase `jeffols` |
| Hero | rotational, large | Naked geometry must stay recoverable |
| Footer | `mark-mono.svg`, inlined | |
| Favicon | primary mark | Always. No exceptions |
| Social preview | `social-*-1200x630.png` | |

Full rules in `docs/logo-usage.md`.

## Rules that are easy to get wrong

**Do not redraw or inline the mark geometry.** The site currently has two
hand-copied copies of the path data — one favicon data URI, one hero SVG. Both
must be replaced with references to generated assets. A geometry change here
cannot reach a hand-copied path, and nothing fails loudly when they diverge.
`BRAND.md` section 21.

**`currentColor` only inherits when the SVG is inlined.** Through
`<img src="...">` an SVG is an isolated document with no parent colour, and the
mono mark renders black. Inline the `-mono` files; use a palette variant for
`<img>`.

**Do not ship a subset of iA Writer Duo under its own name.** It carries
Reserved Font Names (`iA Writer`, `Plex`) and OFL clause 3 forbids a Modified
Version from using them. Serve it unmodified, or subset and rename the family.
Inter has no reserved name and may be subset freely.

**Never upload a favicon PNG as an avatar.** Favicons are a rounded plate on
transparency; avatars are full-bleed and opaque. Use `avatar-*` files.

**Respect `prefers-reduced-motion`** on any mark animation.

## Re-syncing

Assets are versioned by tag. `v2.0.0` is current. When the brand repo changes:

1. Check `docs/decisions/` for what moved and why.
2. Re-copy the files above.
3. Regenerate the woff2 conversions if a font changed.

Paths changed at `v2.0.0` — anything pinned to `v1.0.0` still resolves there.

## Known drift

As of `v2.0.0` the site is behind on two counts:

- **Framing.** Decision `0005` shifted the glyph 42 units right. Every published
  asset predating it is 4% out of register.
- **Naming.** `signature-*.svg` became `icon-*.svg` in decision `0006`.

Both are fixed by re-copying from the list above.
