# Website direction

Strategy: `BRAND.md` sections 13 and 14. This file is the build checklist for
`jeffols.github.io`.

**Do not edit the site repository until the brand guidance and required assets
are stable.** Remaining blockers: the transparent and monochrome exports, and the
`signal_yellow` light contrast finding. The rotational construction is settled —
decision `0002`.

## The shift

The site currently reads as a manifesto. It should function as a front door. A
new visitor answers five questions fast:

1. Who is Jeff?
2. What does he work on?
3. What does he think differently?
4. Where can I see evidence?
5. What should I do next?

## Homepage sections

| # | Section | Contains | Mark |
|---|---|---|---|
| 1 | Hero | Name, one positioning statement, one supporting sentence, 2–3 CTAs | Restrained primary, or rotational as expressive visual |
| 2 | Two paths | Working Faster / Context Engineering | — |
| 3 | Featured thinking | 3–5 selected items, not a feed | Article card system |
| 4 | Proof of work | Compact case cards: problem → insight → artifact → result | — |
| 5 | About Jeff | Concise. Link to LinkedIn for full career detail | — |
| 6 | Subscribe and connect | Substack, LinkedIn, GitHub, contact | — |
| 7 | Footer | Name, links, copyright, optional brand line | Primary mark |

Working hero draft:

> I make hidden work and complex systems easier to see.

> I write and build practical models for organizational delivery, context
> engineering, knowledge systems, and enterprise technology.

CTAs: Read Working Faster / Explore the work / Connect on LinkedIn.

Do not explain every concept in the hero.

**Two paths** — each needs: a one-line description, a featured item, a link out
(Substack for Working Faster, GitHub for Context Engineering), and a current-focus
statement.

**Featured thinking** — each card answers: what is it, why should I care, what
will I learn or use. Candidates: *On Track Is Not a State*; *Complaints Don't
Travel Upward. Costs Do.*; a Working Faster overview or field guide; a
context-engineering artifact; an open-source project.

## Mark usage on site

| Slot | Mark | Rule |
|---|---|---|
| Header | Primary, beside "Jeff Olsen" or "jeffols" | |
| Hero | Large rotational, **or** primary in the lockup with echoes as oversized background | Naked geometry must stay clearly recoverable |
| Favicon | Primary | Always. No exceptions |
| Social preview | Rotational or a larger branded composition | Underlying naked geometry must remain visible |
| Watermark | Glow treatment | Subordinate to content; must not reduce text contrast; must not read as a second competing logo; must respond on mobile; must be hideable |
| Footer | Primary | |

## Compliance gap

`index.html` inlines the mark geometry twice — once as a favicon data URI, once
as the hero SVG. It references no file this repository produces, so a geometry
change here will not reach the site and nobody will notice.

Required fix (Phase 4): consume exported assets. The site repository owns
implementation, content, deployment, page accessibility, performance, and *copies
of generated assets required to deploy*. It does not own the mark.

## Motion

The mark has a natural animation: echo states appear, the three components rotate
toward alignment, the echoes fade, the primary mark remains. The echo mark
resolves into the durable state.

Calm and intentional. Must respect `prefers-reduced-motion`. Construction settled
in `0002`; `scripts/generate_rotational_logo.py` can emit an animated SVG via
`spin_seconds`, which is the starting point rather than the finished behaviour.

## Validate before ship

- Mobile layout
- Accessibility, including the watermark's effect on text contrast
- Performance
- Reduced-motion behaviour
- Favicon renders as the primary mark at 16 px
