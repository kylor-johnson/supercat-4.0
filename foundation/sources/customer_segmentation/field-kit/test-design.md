---
id: FK-TEST
title: Field kit test design — falsifiable hypotheses
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
depends_on: [PROS-CRIT, PROS-L1, PROS-L2, PROS-L3, PROS-DQ]
---

# Field kit test design

These are the Phase 4 pre-registered failure expectations converted to falsifiable form. Not a new
exercise — the same claims, each with the observation that kills it.

**What the field kit is measuring:** not whether the candidates are good companies, but whether
**a person with a browser and a market floor can classify a prospect more reliably than a feature
checklist can** — and whether the lane definitions survive contact with real companies.

---

| # | Hypothesis | Kill condition | Data captured at market |
|---|---|---|---|
| **H1** | **The lane-1/lane-2 boundary is real and a human can call it.** A rep reading a showroom or homepage can assign designer-led vs dealer-led within ~2 minutes, and two independent readers agree. | **Killed if** inter-reader agreement on lane assignment is **≤70%** across the walk list, or if ≥3 of the qualified candidates cannot be assigned to either lane without more information. | Two readers independently assign lane per candidate, blind to each other. Record both calls, time taken, and the one cue each relied on. Designmaster Furniture and Home Trends and Design are the designated boundary tests — both carry designer *and* dealer signals. |
| **H2** | **Holistic reading beats binary extraction.** A human read of the same public site predicts the eventual segment better than the ARCH rules did (33.3% vs a 34.5% majority baseline, n=87). | **Killed if** human predictions, checked against Layer A labels once any candidate becomes a customer, land **≤40%** — i.e. no better than the checklist. | For every candidate, the reader records a predicted SEG **before** seeing the ARCH output. Resolve later against the stamped roster. Long-dated; log now, settle on conversion. |
| **H3** | **Category filtering over-selects, and Gate 0 is what actually does the work.** Most HPMKT exhibitors clear the category criterion; qualification is carried by Gate 0. | **Killed if** Gate-0 rejects **<25%** of category-passing candidates walked — that would mean category was already doing the qualifying and Gate 0 is redundant. | Record Gate-0 pass/fail per booth walked, with the failing criterion. Desk baseline to beat: of the ~110 lighting companies reaching observation, roughly a third were décor/accessory or antiques houses. |
| **H4** | **The manual-only criteria carry real discriminating power.** HPMKT footprint (building, space, tenure) and headcount separate qualified from disqualified, justifying their collection cost. | **Killed if** building/neighborhood/tenure distributes **the same** across qualified and disqualified candidates — no separation. | Record building, space number, floor, approximate square footage and stated years at market for every booth walked, qualified or not. **This has never been collected for any roster org** — the discriminating power is unknown, not merely uncertain. |
| **H5** | ~~The HPMKT frame contains enough net-new prospects to justify working it for discovery.~~ **ANSWERED AT THE DESK — KILLED.** | Kill condition was ≤25% fresh. **Measured: 5 of 30 checked are fresh = ~17%**, plus 72 of 693 frame exhibitors are already customers `[MEASURED 2026-08-25]`. No market-week data required. | Nothing to collect. Confirm opportunistically: record fresh / lead / SQL / open-deal / customer per booth walked, to check the desk figure holds at scale. |

### H5 is settled, and it changes what the kit is for

The frame is already worked. **The field kit's script is displacement and re-engagement, not
discovery.** That is a change to the kit's job, not just its list:

- **Most booths will be a known name.** The opener is "where did we leave this" or "what changed",
  not an introduction. Every walk-list row must carry its HubSpot state *before* the conversation,
  and the three open deals (Jensen Outdoor, Lexington, JDouglas) must not be approached as new.
- **Displacement needs a different question set** than discovery. For the 14 companies running a
  competitor platform (see [`../prospects/competitor-platform-signal.md`](../prospects/competitor-platform-signal.md)),
  the useful questions are about what their current platform does badly — not whether they have one.
- **Net-new discovery, where it happens, is more likely to come from the competitor-platform signal
  than from category screening.** Five of 14 competitor installs are absent from HubSpot — a better
  fresh yield from a cheaper signal than the whole lane screen produced.

H1–H4 remain live and are what market week actually tests.

---

## Two findings that already constrain the test

**Lane 3 is blocked before it starts.** The anchor, Savoy House, is **not an HPMKT exhibitor**
`[MEASURED]`, and the HPMKT Lamp & Lighting category is décor-accessory houses rather than
program-driven lighting manufacturers. Only 4 candidates could be listed, one of which (Coast Lamp
Mfg) is genuine. **H1–H5 should be run on lanes 1 and 2 at High Point; lane 3 needs a Dallas frame
or a re-anchor.** Running lane 3 at High Point as specified tests the frame, not the criteria.

**The strongest signal found was not in the criteria at all.** Seven candidates run **AmpTab** and
three run **WizCommerce** — both named direct competitors. A company running a competitor's B2B
platform has already proven every Gate-0 condition plus willingness to pay. If H5 is killed (likely),
**competitor-platform detection is the more promising sourcing method than category screening**, and
deserves its own pass rather than a footnote here.

---

## What would make the whole exercise a failure

If the field kit produces a qualified list that nobody can reproduce — because the calls rested on
tacit judgment that was never written down — then it has not been tested, only performed. Every
hypothesis above therefore requires **two readers and a recorded cue**, not a single verdict.
