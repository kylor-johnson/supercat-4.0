---
id: FK-EX-01
title: Worked example — what the manual read is for
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
purpose: Field-kit training material. Why a person reads the site instead of running a checklist.
depends_on: [TAX-B, TAX-MAP]
---

# Worked example — what the manual read is for

Training material for anyone using the field kit. One company, one contradiction, and the reason the
kit is built around a human read rather than a form.

---

## The case

**Interlude Home** is a stamped **SEG-01 Luxury Specification** account — designer-specified
furniture, trade buyers, no public pricing. It is the anchor for lane 1. It is about as clear an
example of the segment as exists on the roster.

**The automated feature extractor scored it `TRADE_GATE = 0`.**

Not "uncertain." Zero. The single marker most associated with designer-led selling did not fire on
the company chosen to exemplify designer-led selling.

## Why

The extractor searched for the phrases the industry is *supposed* to use: *"to the trade"*, *"trade
only"*, *"trade program"*, *"trade account"*, *"designer program"*.

Interlude Home's homepage nav reads `[OBSERVED: interludehome.com, 2026-08-25]`:

```
NEW | SALE | DESIGNER RESOURCES | CREATE ACCOUNT | Log In | OUR STORY |
SHOWROOMS | CREATE AN ACCOUNT | CONTRACT | CAREERS | FIND A REP | CONTACT US
```

The gate is **completely real**: you cannot see a price, you cannot buy, and the resources section is
addressed to designers. It is expressed as **"DESIGNER RESOURCES" + "CREATE AN ACCOUNT"** — words the
pattern did not contain.

A person reading that nav identifies the gate in about three seconds. `CONTRACT` and `FIND A REP` sit
right next to it. No experienced reader would hesitate.

## The contrast

Braxton Culler, the lane-2 anchor, reads:

```
Find A Store | Dealer Portal | Apply to Become a Dealer | Dealer Locator |
Showroom Information | Room Planner | Warranty
```

Same industry, same "no public prices", same market. **Designer** vocabulary versus **dealer**
vocabulary — and that is the entire lane-1/lane-2 distinction, visible in the top nav of each site,
invisible to a keyword list.

## What this costs, measured

Across the full back-test the binary approach scored **33.3% against a 34.5% majority baseline
(n=87)** — no better than guessing the largest segment. The earlier holistic run, an LLM reading whole
sites, scored **~53% against a 30% baseline**. Same public web. Different method.

**The gap between those two numbers is what the human read buys.** Neither is good enough to put a
v4.0 segment label on a prospect — that limit is real and stated in
[`../taxonomy/segment-archetype-mapping.md`](../taxonomy/segment-archetype-mapping.md) §5.1 — but
the difference between them is the reason the kit sends a person.

## The rules that follow

1. **Read for the function, never the phrase.** The question is *"can a consumer see a price and
   buy?"* and *"who is this copy addressed to?"* — not *"does the site say 'to the trade'?"*
2. **Nav vocabulary is the fastest lane signal available.** Designer / showroom / contract / rep
   → lane 1. Dealer / become a dealer / find a store → lane 2. Check the top nav first.
3. **A missing marker is not a negative finding.** It means the words were absent, not the practice.
   Record **UNKNOWN**, not "not met", unless you actively looked and it genuinely is not there.
4. **When the checklist and your reading disagree, your reading wins — and write down the cue.**
   The cue is the finding. This example exists only because someone recorded that Interlude gates by
   "DESIGNER RESOURCES."

## Where this shows up on the walk list

Two lane-1 candidates carry *both* vocabularies and are the designated boundary tests for hypothesis
H1 in [`test-design.md`](test-design.md):

- **Designmaster Furniture** — `Designer Resources` **and** `Dealer Portal`, plus a Hospitality line.
- **Home Trends and Design** — a designer gate **and** `Find A Rep` **and** a `Store locator`.

No checklist resolves these. Two readers, independently, with the cue recorded — that is the test.
