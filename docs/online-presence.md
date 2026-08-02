# Online presence

Strategy: `BRAND.md` sections 15 to 19. This file tracks what each channel uses,
what is done, and what is outstanding.

## Channel map

| Channel | Job | Mark | Status |
|---|---|---|---|
| jeffols.com | Canonical hub and synthesis | Horizontal lockup in header, primary in footer, rotational as hero background | Rebuilt 2026-08-01. Consumes generated assets, compliant |
| Substack | Long-form thinking, subscription | Primary as avatar (`avatar-512x512.png`) | Not aligned |
| LinkedIn | Professional conversation, distribution | Headshot as profile, echo composition as banner | Banners done, all 12 palette/mode pairs |
| GitHub | Technical evidence, artifacts | Primary as org/profile avatar | Repo metadata done. Profile README not written |
| This repository | Visual and verbal source of truth | — | Foundation in place |

Every channel links back to `jeffols.com`. The site links out to every active
channel.

## Repository metadata — done

Set 2026-08-01:

- Description: "Source assets, generators, palettes, usage guidance, and visual identity for the Jeffols brand."
- Homepage: `https://www.jeffols.com`
- Topics: branding, design-system, favicon, identity, logo, personal-brand, svg
- Licence: Apache-2.0 detected, with `ASSETS-LICENSE.md` reserving the mark

## LinkedIn

**Profile image: keep the headshot.** A headshot and a logo do different jobs —
the headshot buys human recognition and professional trust, which matters more on
LinkedIn than symbol repetition. Build symbol recognition in the banner and on
article graphics instead.

**Banner.** The existing echo composition is approved. It is a wide surface, so
the composition carries the expression; see `docs/logo-usage.md`. Requirements:
keep content out of LinkedIn's profile-image obstruction area, little or no text,
no generic role-title language, visually related to the site hero.

Banners live in `assets/banners/linkedin/`, regenerated from the canonical
`PALETTES` so every palette and mode is covered.

**Headline.** Connect role and point of view, not a technology list. Structure:

> Distinguished Engineer | Enterprise AI, Architecture and Knowledge Systems | Making Hidden Work Visible

Wording should match current professional constraints.

**Featured section**, in order: best introductory Working Faster essay,
jeffols.com, a technical proof-of-work item, a second essay or field guide.

## GitHub

**Profile README** — not written. Should carry: current focus, one-sentence
positioning, Working Faster, context engineering and knowledge systems, selected
original repositories, latest writing, and links to jeffols.com, Substack,
LinkedIn.

**Pinned repositories** — curate for the present brand. Prefer original work,
active experiments, public artifacts, this repository, and the site repository.
Old forks and unrelated experiments should not be the first impression.

**Repository hygiene** — for each important public repo: description, website
URL, topics, strong README, a screenshot or diagram, current status, and its
relationship to the broader body of work.

## Substack

Positioning:

> Practical systems thinking for seeing where work really is, where time goes,
> and what is worth changing.

Navigation entry points: Start here, Working Faster concepts, Latest essays,
Field guide or glossary, About Jeff, jeffols.com.

Brand consistency: same mark, same canonical palette, consistent article-cover
system, same short bio.

Upload `avatar-512x512.png`, never a favicon PNG — Substack flattens leftover
transparency to white and a pre-rounded asset shows white corner slivers.

A custom publication domain is optional and lower priority than consistent
navigation and identity.

## Publishing loop

Each substantial idea should produce: long-form Substack article, LinkedIn post,
recognisable visual card, field-guide or glossary entry, website index entry, and
optionally a downloadable artifact. This is what turns individual posts into
cumulative intellectual property.

## Constraint

Do not add new platforms before the existing ones are connected. The gap is
connective tissue, not reach.
