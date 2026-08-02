# Website direction

Strategy: `BRAND.md` sections 13 and 14. This file is the build checklist for
`jeffols.github.io`.

The guidance and the required assets are stable. The transparent and monochrome
exports shipped, the `signal_yellow` light contrast finding was resolved by
inverting the mode (`0004`), and the rotational construction is settled (`0002`).

The site was rebuilt against this document on 2026-08-01. Read
`docs/site-handoff.md` before changing what it consumes.

## The shift

The site read as a manifesto. It should function as a front door. A new visitor
answers five questions fast:

1. Who is Jeff?
2. What does he work on?
3. What does he think differently?
4. Where can I see evidence?
5. What should I do next?

Rebuilt to this structure on 2026-08-01. Questions 1 to 3 and 5 are answered.
Question 4 is answered thinly and by design: the arc of work is real but mostly
applied inside organizations, so it is stated as a sequence rather than linked.
That gap closes by publishing, not by redesigning. See the note under
**Proof of work** below.

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

**The footer brand line is optional, and it must be an external formulation.**
`BRAND.md` section 3 lists the publishable ones. The internal organizing phrase
"make hidden systems visible" is not among them and must never appear on a public
surface. It shipped here on 2026-08-01 and was removed on 2026-08-02.

The footer is the last thing read, so the line has to survive being the only
sentence someone remembers. It also must not re-tilt a two-path page toward one
path, which rules out "hidden" vocabulary. Currently:

> The deliberate pursuit of simplicity in complex domains.

Hero, settled by decision `0008`:

> I build systems that understand before they act.

> Distinguished engineer. Ontology, context engineering, agentic development, and
> knowledge systems, designed across security, infrastructure, data, scale,
> networking, and architecture. The deliberate pursuit of simplicity in complex
> domains.

CTAs: Read Working Faster / Explore the work / Connect on LinkedIn.

Do not explain every concept in the hero. Do not state seniority as elapsed time:
"distinguished engineer" carries it, a year count does not, and `0008` explains
why. The anticipation thesis that justifies the range belongs in the principles,
not here.

**Two paths** — each needs: a one-line description, a featured item, a link out
(Substack for Working Faster, GitHub for Context Engineering), and a current-focus
statement.

**Featured thinking** — each card answers: what is it, why should I care, what
will I learn or use. Candidates: *On Track Is Not a State*; *Complaints Don't
Travel Upward. Costs Do.*; a Working Faster overview or field guide; a
context-engineering artifact; an open-source project.

### As built, 2026-08-01

The seven sections are all present. Two carry less than this document asks for,
and in both cases the constraint is inventory rather than design.

**Featured thinking** shows 2 items, not 3 to 5. Those are the two essays that
exist. A field guide or a third essay fills the gap; padding it with a repository
that is not writing would not.

**Proof of work** carries no case cards and no outbound links. The arc it
describes is real, but the work sits inside organizations and cannot be published
as sanitized diagrams or before-and-after examples without separating employer
specifics from the underlying models first. The section states the sequence
instead, and says plainly that it is doing so. That is the honest form of the
section until a public artifact exists to link, and the markup is structured so a
card drops in without a redesign.

The two paths are visually co-equal per `BRAND.md` section 1, but their evidence
is not. Working Faster carries published essays. Context Engineering carries a
current-focus statement rather than links.

Revised 2026-08-02 by `0008`: that statement now leads with original method work
on retrieval accuracy, cost, and risk, and mentions the proprietary constraint
second. Leading with the constraint made the path sound like an absence. Leading
with the invention makes it a body of work that happens to be mostly unpublished,
which is what it is. The asymmetry is still real and still named.

### Revised 2026-08-02

The hero, the About section, and the three meta descriptions changed with `0008`,
and a fourth principle was added: **Speed comes from anticipation**. The page no
longer leads with Working Faster vocabulary, so the two paths now hang off a
headline that belongs to neither of them.

## Mark usage on site

| Slot | Mark | Rule |
|---|---|---|
| Header | Primary, beside "Jeff Olsen" or "jeffols" | |
| Hero | Large rotational, **or** primary in the lockup with echoes as oversized background | Naked geometry must stay clearly recoverable |
| Favicon | Primary | Always. No exceptions |
| Social preview | Rotational or a larger branded composition | Underlying naked geometry must remain visible |
| Watermark | Glow treatment | Subordinate to content; must not reduce text contrast; must not read as a second competing logo; must respond on mobile; must be hideable |
| Footer | Primary | |

## Compliance gap, closed 2026-08-01

**Resolved.** The site now consumes generated assets and inlines no hand-authored
geometry. What it does today:

| Slot | Asset | Form |
|---|---|---|
| Header | `assets/lockups/lockup-horizontal-mono.svg` | inlined verbatim, `currentColor` |
| Hero | `palettes-rotational/signal_yellow/dark/mark-1024x1024.png` | `<img>`, 8.5% opacity |
| Footer | `assets/marks/primary/mark-mono.svg` | inlined verbatim, `currentColor` |
| Favicon | `palettes/signal_yellow/dark/` package | copied, primary mark |
| Social | `assets/social/social-signal_yellow-dark-1200x630.png` | copied |

Both inline SVGs are byte-identical to the generated files, verified by
comparison rather than by eye. A geometry change here now reaches the site by
re-copying, and a divergence is detectable.

Two deliberate divergences from `docs/site-handoff.md`, both recorded in the site
repository's `CLAUDE.md`:

- **`iAWriterDuoS-Bold` is not shipped.** Nothing on the page sets bold in the
  essay register, so the file and its `@font-face` rule would both be dead. Add
  it with the long-form content that needs it.
- **Inter is subset to Latin**, 344 KB to 60 KB. Permitted by `0007` because
  Inter carries no Reserved Font Name. Both variable axes preserved and the
  rendered page is pixel-identical. iA Writer Duo is a container conversion only
  and is never subset.

The audit that produced this section is kept below, because the failure mode it
describes is the one to watch for.

### What was wrong

Audited 2026-08-01 against `jeffols.github.io` at commit `1a5ee0e`.

`index.html` inlined the mark geometry in **three** places, not two:

| Line | Copy |
|---|---|
| 8 | favicon data URI |
| 233–235 | `glow-bg` — a stroke-outline construction that exists **nowhere** in this repository |
| 243 | header mark, plus `stroke="#FFD60A" stroke-width="2"` on the plate |

The third was the serious one: the header carried a **modified** mark, not a copy
of a generated one. No canonical asset has a stroked plate. The second was a
fourth construction of the mark that was never a brand decision.

All three used pre-`0005` coordinates (`x=400/460/500`), so they were 42 units out
of register with everything this repository now produces.

The site referenced no file this repository generates, so a geometry change here
could not reach it and nothing failed loudly when they diverged. That is the
failure mode, and it is silent by construction: hand-copied geometry keeps
rendering correctly long after it stops being the mark.

The fix was to consume exported assets per `docs/site-handoff.md`. The site
repository owns implementation, content, deployment, page accessibility,
performance, and *copies of generated assets required to deploy*. It does not own
the mark.

Also found, and outside this document's scope but worth recording: the site has
no Open Graph tags, exactly one external link on the whole page, and no calls to
action.

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
