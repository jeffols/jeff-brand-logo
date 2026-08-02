# 0008 — Homepage headline, range, and how seniority is stated

**Date:** 2026-08-02
**Status:** Accepted

## Decision

The homepage headline is:

> **I build systems that understand before they act.**

Supported by:

> Distinguished engineer. Ontology, context engineering, agentic development, and
> knowledge systems, designed across security, infrastructure, data, scale,
> networking, and architecture. The deliberate pursuit of simplicity in complex
> domains.

Three consequences follow, and they are the substance of this record:

1. **Range is part of the identity**, recorded in `BRAND.md` section 1.
2. **Seniority is stated as rank, never as elapsed time.**
3. **Context engineering is original method work**, not applied reading.

This closes the last "still to decide" item that blocked the website work.

## Why the previous draft was retired

`BRAND.md` section 13 carried "I make hidden work and complex systems easier to
see." The site shipped it on 2026-08-01.

It is an accurate umbrella and it fails as a headline. **"Hidden work" is Working
Faster's signature phrase.** Section 1 defines a brand connecting *two* co-equal
bodies of work, so leading with the vocabulary of one collapses the umbrella into
one of its halves. The page then read as delivery consulting, with the deep
systems half demoted to a card below the fold. That is the same defect the
2026-08-01 audit found in the opposite direction, when the site said only
"ontology, context engineering, simplicity" and was narrower than the brand.

The positioning statement in section 1 is unchanged and still correct. A
positioning statement and a headline do different jobs: one has to be complete,
the other has to be the first thing a stranger reads. This record separates them.

## Why this headline

It survived both the narrow and the broad failure, which is why it is chosen over
newly drafted alternatives. It was the thesis on the original site, it is the
through-line already used in the LinkedIn draft, and it does double duty:

- It is the property built *into* the systems: context before action.
- It is the method the work is *done* by: understand the domain before designing.

The range claim below it is what makes the second reading credible.

## Range

The differentiator is not depth in any single domain. It is fluency across enough
of them to anticipate what each will ask, and to design so that no pillar is
traded against another:

> The only way to move fast is to anticipate the concerns and questions of every
> team and bake them into the design.

This is a speed claim that is not Working Faster, which is precisely why it works
as connective tissue between the two paths. It also carries directly into current
work: "is the data encrypted, who has access, what is the risk" are the questions
generative AI systems meet immediately, and the position is that they are design
constraints rather than gates to clear afterwards.

Stated on the site as a fourth principle, "Speed comes from anticipation."

## Seniority: rank, not years

**Do not state seniority as elapsed time.** No year counts, no "over two decades,"
no start decade.

The options considered, all describing the same person:

| Option | Verdict |
|---|---|
| "since the early nineties" | Accurate. Maximum ageism exposure, and invites arithmetic |
| "over two decades" | **Worst of the three.** Carries most of the same exposure while understating the actual span. Pays the cost without taking the credit |
| no time claim | **Chosen** |

The reasoning: **"Distinguished engineer" already carries the signal.** It is a
rank that only exists at the top of the individual-contributor ladder and nobody
reaches it early. It communicates the same seniority as a start date, as a claim
about *level* rather than about *birthday*, and it cannot be turned into an age.

A time claim is also weaker evidence. It is an argument from seniority that the
reader cannot check. A range claim is testable against the rest of the page. Many
people can claim twenty years; few can claim fluency from security through data
and scale to the C-suite, which is why the range is the differentiator and the
years are not.

The risk of dropping time is that breadth reads as unearned. The answer is
**specificity, not a number.** Nobody junior writes "feedback latency,"
"measurement distortion," or a palette audit that checks deuteranopia. The
writing carries the seniority on every screen.

## Hobby, passion, vocation

The same curiosity runs through the side projects, the writing, and the paid work.

This earns its place in the brand because it answers a question the site otherwise
raises and does not resolve. The context engineering path says its models come
from self-directed projects, and without this, a reader has no reason to find that
credible rather than defensive. It is also the honest account of why the applied
work can be proprietary while the thinking behind it is publishable.

## Consequences

- `BRAND.md` section 1 gains **Range** and **Hobby, passion, vocation**. Section
  13's hero and About drafts are replaced. Section 23 moves the headline from
  *still to decide* to *decided*.
- The site changes the `h1`, the lede, the three meta descriptions, the About
  section, and adds a fourth principle. "Distinguished engineer" is removed from
  About, since the hero now carries it.
- The context engineering path states original method work on retrieval accuracy,
  cost, and risk. This is the first thing that makes that path stand on its own
  rather than on future publication.
- **Channel copy is now out of date.** The LinkedIn headline, the Substack
  description, and the unwritten GitHub profile README all derive from the retired
  draft. Tracked in `docs/online-presence.md`.
- `docs/website-direction.md` quoted the retired hero in two places. Updated.

## Not settled here

Whether the section 1 positioning statement should itself be rewritten. It leads
with "hidden work" and has the same bias as the retired headline, but it is doing
a different job and nothing currently reads it aloud to a stranger. Revisit if it
ever becomes a headline anywhere.
