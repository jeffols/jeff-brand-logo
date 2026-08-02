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

## Channel copy is stale, 2026-08-02

Decision `0008` changed the headline and how seniority is stated. The site is
updated. **Every other channel still carries the retired positioning** and needs a
pass by hand:

| Channel | State |
|---|---|
| LinkedIn | Headline drafted below, ready to paste. About section still to write |
| Substack | Description and About drafted below, ready to paste |
| GitHub | Profile README still unwritten. Write it against `0008` |

Copy below is current. Anything elsewhere in this file that quotes positioning
language predates `0008`; the structural guidance in it still holds.

## Copy to paste

Neither profile can be edited from here. These are final drafts for Jeff to apply.

**LinkedIn headline**, 132 characters, within the 220 limit.

> Distinguished Engineer | I build systems that understand before they act | Security, data, scale and architecture held in one design

Rank rather than elapsed time, per `0008`. The range clause is the differentiator
and is the reason this was chosen over a domain list, which is also what section 15
warns the headline must not become. It survives feed truncation, since the first 60
characters carry both the rank and the thesis.

**Substack description**, 187 characters.

> Long-form thinking on complex systems and the work of making them understandable. Delivery, ontology, context engineering, and the models I build along the way. Start with Working Faster.

**Substack About page.**

> I'm Jeff Olsen. I build systems that understand before they act, and this is where I work out the thinking behind that.
>
> Some of it is forward looking. Some of it is what I learned from a project that is already finished. Delivery, ontology, context engineering, architecture. What holds it together is that every piece tries to leave you with something usable, a model or a question you can take into a real room.
>
> Working Faster is the first of it. It's about delay, and specifically the kind that hides inside a status report. A week in someone else's queue looks identical to a week of work, and the calendar moves either way.
>
> Start anywhere. New writing most weeks.

The second paragraph carries the range without predicting a form, so a
retrospective piece fits it as naturally as a forward looking one. No colons and no
em dashes in any of the above, per `BRAND.md` section 2.

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

Positioning is the publication description under **Copy to paste** above. The
publication is the hub voice and carries the whole body of thinking. Working Faster
is the first thing published in it, not its subject. `BRAND.md` section 17.

The line previously recorded here, "practical systems thinking for seeing where
work really is, where time goes, and what is worth changing," is the Working Faster
*path* description. It still describes that path on the site. It is not the
publication description.

Navigation entry points: Start here, Working Faster concepts, Latest essays,
Field guide or glossary, About Jeff, jeffols.com.

Brand consistency: same mark, same canonical palette, consistent article-cover
system, same short bio.

Upload `palettes/signal_yellow/light/avatar-512x512.png`, the **light** mode, never
a favicon PNG. Substack flattens leftover transparency to white and a pre-rounded
asset shows white corner slivers. Mode rationale in `docs/logo-usage.md`.

**Site appearance settings**, applied 2026-08-02.

| Field | Value |
|---|---|
| Background | `FFFFFF` |
| Accent | `111827` |

The accent is Signal Yellow's plate colour, which is also the background of
jeffols.com, so the two surfaces share a colour identity. It leaves the yellow
avatar as the only colour on the page.

Previously `4B0082`, which is the deep_indigo glyph, while the avatar was
signal_yellow. That ran two palettes on one surface. **Signal Yellow itself cannot
be the accent**, since Substack puts white label text on it and yellow measures
1.41 against white. See `docs/accessibility.md`.

A custom publication domain is optional and lower priority than consistent
navigation and identity. `braindini.com` is already owned and is the candidate if
one is ever wanted. Recorded so it is not lost, not as a recommendation to use it.

## Publishing loop

Each substantial idea should produce: long-form Substack article, LinkedIn post,
recognisable visual card, field-guide or glossary entry, website index entry, and
optionally a downloadable artifact. This is what turns individual posts into
cumulative intellectual property.

## Constraint

Do not add new platforms before the existing ones are connected. The gap is
connective tissue, not reach.
