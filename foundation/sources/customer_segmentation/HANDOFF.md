---
id: HANDOFF
title: Handoff — start here in a new session
version: 0.1
status: reference
date: 2026-08-26
owner: Kylor Johnson
---

# Handoff

Phases 0–5 are complete and committed. This is the cold-start page.

## Read order

1. **[`00-SYNTHESIS.md`](00-SYNTHESIS.md)** — two pages, the whole picture. Always first.
2. **The one file for the track you own** (below). You do not need the other twenty.
3. [`ASSUMPTIONS.md`](ASSUMPTIONS.md) only if you are about to challenge a number — 5 assumptions,
   5 data-quality items, 22 findings, and the process defects.

## The three tracks

| Track | Owner | Entry point | What it needs next |
|---|---|---|---|
| **Foundation & decisions** | **Kylor** | `00-SYNTHESIS.md` §5 | Five open decisions. Correction #1 is already applied — `CEO_SYSTEM_CONTEXT.md` and `02_who_we_serve.md` were corrected 2026-08-26 (`FOUNDATION-CORRECTIONS.md` is now the record, not a proposal) |
| **Field kit** | **UNNAMED — this is the gap** | `field-kit/test-design.md` + `prospects/` | **HPMKT Fall is 17–21 Oct.** The only deadline-driven item in the register, and nothing is built. Candidates, criteria and hypotheses exist; the kit does not |
| **Engineering** | **Brent** | `product/data-gaps.md` §D | Four S-sized items needing no new data: export/UI reconciliation (gates trust in every Portal number), ungate rep activity, catalog completeness, inventory snapshot age |

## The five open decisions

1. **Sales Portal — leadership+CS, or reps first?** Two stamped docs disagree; it changes what gets built for JTBD-011/021/031. Cost is asymmetric — see `product/surface-mapping.md` §6. Cheapest way to settle it is asking reps at market.
2. **Expose buyer purchase history?** A config change reaching ~13,800 active buyers, not a build. Blocked on a client-risk review (pricing-entitlement and competitive exposure), not on job strength.
3. **Commit to PER-02 rep agency, or say no?** Not servable before an agency entity exists. Recommendation on file: say no this cycle.
4. **Invoice-feed push for the 71 orgs without one?** The largest constraint in the register. A commercial motion, not engineering work.
5. **Delete `Customer Segmentation 2`** — byte-identical duplicate of the answer key, on the ignore list.

## Reproducibility — [`_working/`](_working/)

**Committed and reusable:** the 693-exhibitor HPMKT frame, dedupe verdicts, directory-declared
attributes, the roster feature matrix, back-test rows, and 8 scripts. 580 KB, no client data.

**Not preserved:** the 437 fetched homepages (99 MB). Re-fetching is ~45 minutes, and **re-running
the marker scripts against fresh pages will produce different numbers** — sites change. Cite the
back-test figures with their **2026-08-25** date; do not silently recompute them.

**Two steps a re-run must not skip:** hand-adjudication of brand-family duplicates (automation alone
put Sauder, an existing customer, on a prospect list), and hostname-not-token matching for
competitor detection (tokens produced 7 fictional NuOrder installs from `"menuOrder"` in Wix JSON).

## Settled — do not re-litigate

Each of these cost real work and is written up with its evidence. Reopening them without new data
is waste.

- **Layer A is stamped human judgment, not a computation.** An authored rule over the four defining
  fields reproduces the stamped label 38.5% against a 34.9% majority baseline (n=109), 50% ceiling
  when fitted. The authority is a roster lookup. New order data does not re-segment anyone.
- **Prospects cannot carry a segment label.** Binary public feature extraction reaches 33.3% against
  a 34.5% baseline (n=87). Holistic reading reaches ~53%. **Neither is good enough.** State it that
  precisely — "public data cannot predict segment" overstates it and misdescribes what a person
  qualifying a prospect does.
- **Build once, parameterise on org structure.** Only 4 of 31 jobs vary by segment, and they vary on
  catalog scale, territory count and price-code count — readable from an org's own data. Do not
  build segment-conditional variants.
- **H5 is killed at the desk.** The HPMKT frame is ~83% already worked (26 of 30 checked are in
  HubSpot; 72 of 693 exhibitors are customers). Market week is **displacement and re-engagement,
  not discovery** — that changes the kit's script, not just its list.
- **Lane 3 runs thin at High Point, by decision.** Savoy House is not an exhibitor and HPMKT lighting
  is décor houses. Coast Lamp Mfg is the single genuine test; the thin yield is the finding. Not
  re-framing to Dallas.

## Two things that will bite whoever picks this up

- **The invoice feed is present for 38 of 109 orgs and degrades 13 of 31 jobs.** Seven of those
  degrade to a usable order-based view and ship with a mandatory label; six fail outright. No
  surface work fixes it — see `product/data-gaps.md` §B1.
- **PER-02 has no data structure behind it.** A boolean on 142 user types and 11,873 free-text
  `company_name` values. The cost is the migration, not the schema.
