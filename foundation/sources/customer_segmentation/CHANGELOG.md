---
id: CHANGELOG
title: Change history — two-layer taxonomy subtree
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
source_lineage: []
depends_on: []
---

# Changelog

## 2026-08-25 — Phase 0 + Phase 1 (draft)

### Added
- `taxonomy/account-segments.md` (**TAX-A**) — Layer A, SEG-01..04 plus SEG-00 abstention.
  Definitions, field-level lineage, measured per-segment distributions, an authored precedence
  rule with its justification, and the rule's real reproduction rate. Marked
  `availability: post-sale-only` in the schema.
- `taxonomy/prospect-archetypes.md` (**TAX-B**) — Layer B, ARCH-01..04 built only from pre-sale
  observable features. Full feature register including what was pruned and why.
- `taxonomy/segment-archetype-mapping.md` (**TAX-MAP**) — measured A↔B matrix and per-archetype
  back-test against the answer key.
- `ASSUMPTIONS.md` — 5 assumptions, 4 data-quality items, 14 findings carried forward.
- `FOUNDATION-CORRECTIONS.md` — proposed corrections to `CEO_SYSTEM_CONTEXT.md` and
  `02_who_we_serve.md`. **Held, not applied**, pending Layer A/B hardening.
- Empty directories for later phases: `personas/`, `analytics/`, `product/`, `prospects/`,
  `field-kit/`.

### Changed
- `README.md` — capped link repair only. The two files it named as living here now point at
  `Customer Segmentation/current/` (the path `build_v4.py` writes); no file was copied in. Dead
  `agent_research/` links marked as not-imported. New taxonomy subtree indexed. `Last updated`
  bumped to 2026-08-25.

### Not changed (deliberate)
- `foundation/CEO_SYSTEM_CONTEXT.md`, `foundation/02_who_we_serve.md` — corrections held.
- Stamped v4.0 narrative, `build_v4.py`, MASTER CSV — read-only.
- Insightful Product 4.0 profiles and `industry_context.md` — the "Brand-Building" alias was not swept.
- Lens 1 (Digital Selling Maturity) and T1/T2/T3 pricing — untouched.
- Postgres — read-only throughout, including the three malformed `company_website` values.
- `Customer Segmentation 2/` — added to ignore list, not deleted.

### Headline results
| Result | Value |
|---|---|
| Layer A authored rule reproduces stamped label | **38.5%** (majority baseline 34.9%; fitted ceiling 50.0%) |
| Layer B overall, a-priori mapping | **33.3%** (majority baseline 34.5% — fails) |
| ARCH-01 Trade-Gated Access → SEG-01 | **65.0%**, n=20 — the only archetype that beats baseline |
| ARCH-01 exclusion of SEG-03 | **0 of 20** — strong disqualifier |
| Layer B collection coverage | 87 of 109 automated; 94 of 109 with manual observation |

### Open
- Volume Distribution's 89% predictability did not reproduce (F-04) — unresolved, not blocking.
- HPMKT footprint and LinkedIn headcount remain uncollected (F-07).

---

## 2026-08-25 — revision 2 (review corrections + Phase 4 criteria)

### Changed
- `taxonomy/account-segments.md` — **reframed.** New §0 makes the headline finding explicit:
  Layer A is **stamped human judgment** (Kjael 2026-07-09, carried from v3.2), corroborated by
  Postgres rather than computed from it. Frontmatter gains `authority` and `derivation` keys.
  §2 reframed as corroborating fields. §4.3 reduced to consequences.
- `taxonomy/prospect-archetypes.md` — new §5 **"The method gap"**. The 33.3% vs 53% difference is
  method (binary feature extraction vs holistic LLM reading), not data. Worked failure case:
  Interlude Home scores `TRADE_GATE=0` while gating by "DESIGNER RESOURCES".
- `taxonomy/segment-archetype-mapping.md` — all three baselines now labelled with their n
  (34.9% n=109 / 34.5% n=87 / 30.0% prior run). New §5.1 narrows the claim and forbids the
  overstatement "public data cannot predict segment".
- `FOUNDATION-CORRECTIONS.md` — Correction 2 **upgraded**. The error in `02_who_we_serve.md` is not
  one sentence: the whole section describes the segments as data-derived. Two compounding errors
  (E1 lineage, E2 first-touch knowability) with replacement text for both. **Still held.**
- `ASSUMPTIONS.md` — F-02 promoted to HEADLINE; F-04 marked not-blocking (no lane is SEG-04);
  F-15 (method gap), F-16 (baseline labelling), F-17 (Phase 4 needs no classifier) added.

### Added
- `prospects/hpmkt-lane-criteria.md` — **Phase 4 lane criteria, pre-sourcing.** Screen reframed as
  category filter → lookalike match → ARCH-01 exclusion. 6 criteria per lane, each tagged
  observable-where / auto-or-manual / include-or-exclude. Exemplar reference vectors for Interlude
  Home, Braxton Culler and Savoy House. Recording contract mandating that every predicted segment
  is labelled a prediction with its accuracy caveat. **No company sourced.**

### Not changed
- Layer B was **not** re-run with more features. The negative result stands as the finding.
- No foundation file edited. Corrections remain held.

### Next
- Review gate on lane criteria, then Phase 2 personas (including the buyer persona, F-14).

---

## 2026-08-25 — revision 3 (Phase 4 sourcing + Phase 5)

### Changed
- `prospects/hpmkt-lane-criteria.md` — **four amendments applied.**
  - New **§0 Sampling frame**: the HPMKT exhibitor directory, not general web search. 693 unique
    exhibitors harvested with building/space/floor/neighborhood. **Upgrades HPMKT footprint from
    MANUAL to MEASURED.**
  - New **§1a Gate 0**: lane-independent pass/fail qualification (manufacturer/brand owner ·
    indirect channel · catalog complexity · size band). Size band bounded from Lens 1 in
    `02_who_we_serve.md` (~37–44 median employees, ~$10M median revenue, $10–250M niche), used to
    exclude at the extremes only — Lens 1 is explicit that scale is not the ICP.
  - Criterion **1.6 dropped** (weak on its own evidence, 5/17). Criterion **2.4 demoted** to
    supporting evidence (4/6 on n=6 cannot carry inclusion).
  - Cohort rates now labelled **cohort-derived, not validating** — same features that back-tested
    at 33.3%; they describe the neighborhood, they are not accuracy.
- `ASSUMPTIONS.md` — F-18..F-22 added (frame already worked; lane 3 anchor absent; competitor
  platforms; dedupe insufficiency; directory attributes do not separate lanes).

### Added
- `prospects/hpmkt-luxury-spec-furniture.md` — 8 ranked candidates, per-criterion observations.
- `prospects/hpmkt-premium-trade-furniture.md` — 9 ranked candidates.
- `prospects/hpmkt-mid-market-lighting.md` — **4 candidates, status `draft-blocked`.**
- `prospects/disqualified.md` — 60+ entries across three distinct reasons.
- `field-kit/test-design.md` — H1–H5, each with its kill condition.
- `field-kit/worked-example-the-manual-read.md` — the Interlude Home `TRADE_GATE=0` case as
  field-kit training material.

### Headline findings
| Finding | Evidence |
|---|---|
| **Lane 3 is blocked** — Savoy House is not an HPMKT exhibitor and the HPMKT lighting category is décor houses | S listing Saatva→Sauder, 60 names, no Savoy; 3/42 lighting candidates publish a where-to-buy |
| **The frame is already worked** — ~17% fresh | 26 of 30 checked exist in HubSpot; 3 open deals |
| **Competitor platforms are the strongest signal found** | 7 AmpTab, 3 WizCommerce, 0 RepZio/Pepperi/MarketTime |
| **Dedupe needs hand-adjudication** | Sauder reached a lane ranking before manual catch |
| 72 exhibitors excluded as existing customers | 51 exact + 21 hand-adjudicated brand families |

### Next
- Review gate on candidates, then **Phase 2 personas** including the buyer persona (F-14).

---

## 2026-08-25 — revision 4 (decisions 1–3 + Phase 2)

### Decisions applied
- **Lane 3: run thin at High Point, not Dallas** (Kylor). Coast Lamp Mfg is the single genuine test.
  The thin yield is recorded in the lane file **as a result** — *mid-market decorative lighting is
  not a High Point population* — not as a shortfall. Closed.
- **H5 answered at the desk and marked KILLED** in `field-kit/test-design.md`, with the consequence
  spelled out: the kit's script is displacement and re-engagement, not discovery.
- Sauder / dedupe insufficiency and the 26-of-30 HubSpot result: logged, not fixed.

### Added
- `prospects/competitor-platform-signal.md` — scoped promotion of the competitor-tech finding.
  Explicitly a **qualification** signal (Gate 0 + willingness to pay), **not** a segment signal; not
  folded into the archetypes. Detection method, and a **measured** false-positive rate: strict
  hostname matching vs loose tokens caught **7 fictional NuOrder installs** (`"menuOrder":3` in Wix
  JSON). Positive control: scanning for SuperCat's own domain returned exactly one hit — Furniture
  Classics, a known customer. **Full 693-exhibitor frame, 437 homepages scanned: 11 AmpTab,
  3 WizCommerce, 0 RepZio/Pepperi/MarketTime.** One pass, complete.
- **Phase 2 — the persona × analytics JTBD layer:**
  - `personas/PER-00-persona-set.md` — the set, with every keep and drop justified.
  - `personas/PER-01`…`PER-06`, `PER-08` — 7 persona files.
  - `analytics/jtbd-register.md` — **31 jobs, flat**, plus 20 cut candidates with reasons.

### Phase 2 headline results
| Result | Detail |
|---|---|
| **7 personas kept, 4 dropped or folded** | IT/integrations dropped as an analytics persona (consumes job status, not analytics; its one analytics job is JTBD-034 under sales ops). Manager folds into PER-03. Buyer sub-types fold into PER-08. SuperCat-internal staff out of frame |
| **31 jobs, 3–6 per persona, one primary metric each** | 20 candidate jobs cut — 6 for schema-absent data, 4 for no decision changing, 5 wrong system, 3 cross-client governance, 1 against our client's interest, 1 false precision |
| **Segment variation: 4 of 31** | And the variation is driven by **catalog scale, territory count, price-code count** — an org's own structure — **not by selling motion**. Build once, parameterise on org structure, do not condition on segment |
| **Reps and buyers are near-disjoint** | Only **593 users** active on both iPad and eOL `[MEASURED]` |
| **Biggest single blocker: the invoice feed** | Present for 38 of 109 roster orgs; degrades **13 of 31 jobs** |
| **PER-02 cannot be served at all today** | No agency entity in the schema — only a boolean on a user type and 11,873 free-text `company_name` values |

### Next
- **Phase 3** — surface mapping, offline constraints for iPad-embedded components, `data-gaps.md`.

---

## 2026-08-25 — revision 5 (Phase 3 + synthesis) — FINAL

### Added
- `product/surface-mapping.md` — **all 31 jobs mapped.** Surface, data dependencies, missing fields,
  build size, offline risk. Includes the buyer-history **config track** (separated from the build
  ranking), the no-incumbent-rep-surface finding as a first-class result, the PER-02 agency-entity
  spec, offline constraints for the 5 iPad-embedded components, and the anatomy-vs-spec conflict
  scoped with its cost asymmetry.
- `product/data-gaps.md` — backlog **split by owner**: WE BUILD IT (14 items) vs CLIENT MUST SEND IT
  (3 items). Plus §C *job exists, data doesn't* retaining the 6 schema-absent cuts.
- `00-SYNTHESIS.md` — exec-readable, 2 pages, no new analysis.

### Changed
- `prospects/competitor-platform-signal.md` — **disambiguation pass done, file closed.** All 5
  build-attribution hits also carry a dealer login on `cms.amptab.com`, two with per-tenant
  manufacturer IDs. **11 of 11 CONFIRMED PLATFORM, 0 build-attribution-only.** The caveat in the
  earlier draft was wrong and is corrected in place.
- `prospects/hpmkt-mid-market-lighting.md` — lane 3 decision recorded: run thin at HPMKT.
- `field-kit/test-design.md` — H5 marked killed at the desk.
- `analytics/jtbd-register.md` — schema-absent cuts now point at `data-gaps.md` §C.

### Phase 3 headline results
| Result | Detail |
|---|---|
| **Mapping** | iPad-EC 5 · Portal 14 · Admin 5 · eOL 5 · Insightful 1 · existing 6. Sizes: **S 12 · M 8 · L 6** |
| **Invoice feed: 7 of 13 jobs ship, 6 do not** | Jobs asking *"what is the trend"* degrade to a labelled order-based proxy. Jobs asking *"what really happened commercially"* fail outright — both toplines, both agency-value jobs, both order-status jobs |
| **PER-02 is not servable** | Stated plainly. The agency entity is an **L** whose cost is a migration over 11,873 free-text `company_name` values, not a schema change |
| **Offline components are read-only by design** | Which removes write-conflict handling entirely. Extract ≈6–8 MB typical, budget 15 MB. Permission scope baked in at sync — so revocation is not real-time, and the product must not claim it is |
| **Conflict cost is asymmetric** | Getting the surface question wrong toward the Portal costs the wrapper *and* leaves the field case unsolved; the other way costs only the wrapper. Argues for resolving before committing to JTBD-011 |
| **Four of the first six build items need no new data** | An aggregation, a config flip, a defect fix, a surfaced timestamp |

### Scope closed
Phases 0–5 complete. Six open decisions carried to `00-SYNTHESIS.md` §5.
No foundation file was ever edited; corrections remain held.

---

## 2026-08-26 — foundation corrections APPLIED

Authorised by Kylor. The hold condition — *apply after Layer A/B is hardened* — was discharged by
flipping the three taxonomy files to `status: hardened`.

### Changed in `foundation/`
- **`CEO_SYSTEM_CONTEXT.md`** (the runtime file the 10 CEO System prompts read) — Lens 2 now states
  that selling-motion segments are **post-sale only** and are **a stamped roster lookup, not a
  computation** (38.5% vs a 34.9% baseline, n=109; 50% fitted ceiling). Carries the precise pre-sale
  limit and forbids compressing it to "public data cannot predict segment". Dead source pointer
  `skills/customer_segmentation/` replaced with `foundation/sources/customer_segmentation/`.
- **`02_who_we_serve.md`** — both errors fixed. **E1**: new lineage paragraph after the v4.0 segment
  table. **E2**: the "knowable at first-touch" bullet replaced with the measured result.
- **`00_README.md`** — date bumped, one-line pointer to both corrections.
- **`foundation/_archive/`** — created; prior versions of both edited files preserved.

### Changed here
- `taxonomy/account-segments.md`, `prospect-archetypes.md`, `segment-archetype-mapping.md` →
  `status: hardened`, `hardened: 2026-08-26`.
- `FOUNDATION-CORRECTIONS.md` → `status: applied`; now the record of what changed, not a proposal.

### Untouched, deliberately
Lens 1 / D-001a · T1/T2/T3 pricing · segment names and counts (33/38/24/14) · the
orthogonality-to-Lens-1 argument · the stamped v4.0 narrative · `build_v4.py` · the MASTER CSV ·
the "Brand-Building" alias in Insightful profiles.

**Open decision #1 in `00-SYNTHESIS.md` §5 is now closed.** Five remain.

---

## 2026-09-15 — persona groups restored (motion × seat)

The Aug 25 Phase 2/3 pack treated SuperCat **login seats** (PER-01…08) as personas and concluded
**only 4 of 31 jobs vary by selling motion / build once, do not condition on segment.** That inverted
the July thesis (personas live *inside* selling-motion segments) and the June eOL-by-motion targeting.

### Added
- `personas/00-PERSONA-GROUPS.md` — **canonical persona set**: PG-01…08 (field/buyer × four motions) + PG-HQ.

### Rewrote
- `analytics/jtbd-register.md` — `JOB-*` per group. Old JTBD-0xx IDs retired.
- `product/surface-mapping.md` — eOL for buyers (fit follows motion); iPad-EC for field-rep analytics (one shell, job pack by segment); HQ on Portal/Admin/Insightful.
- `personas/PER-00-persona-set.md` — demoted to login-seat / headcount index.
- `00-SYNTHESIS.md` — section 2/3/5 rewritten; CS2 deletion recorded.

### Changed
- PER-01…08 — banners pointing at persona groups. Seat evidence kept.
- `product/data-gaps.md`, `_measured/README.md` — scope notes (old IDs; measurements of seats still valid).
- Foundation runtime: `CEO_SYSTEM_CONTEXT.md`, `02_who_we_serve.md`, `01_what_we_do.md`, `00_README.md` — withdrawn "jobs don't differ / build once not on segment" as product doctrine. Lineage (roster lookup, no segment on prospects) kept. Prior versions in `foundation/_archive/*_2026-09-15_pre-persona-groups.md`.
- Deleted `Customer Segmentation 2/` (byte-identical duplicate).

### Untouched
Stamped v4.0 roster · Lens 1 / D-001a / T1/T2/T3 · HPMKT / prospects / field-kit · factory copy (still hold).

---

## 2026-09-15 — Layer 1 vs Layer 2 (consumption personas)

Kylor: the SuperCat personas are admin / VP of sales / executives / sales reps / customers-dealers-buyers, because they consume different products. That is correct. v0.2 over-named motion × seat cells as the persona set and mashed HQ.

### Changed
- `personas/00-PERSONA-GROUPS.md` v0.3 — Layer 1 = five SuperCat personas (surfaces). Layer 2 = selling-motion job packs (PG-01…08 kept as pack IDs). Mixpanel + Postgres consumption evidence in-file.
- `PERSONA-GROUPS-REVIEW.html` — verdict rewritten to agree + two pushbacks (buyer eOL fit; rep analytics grain).

---

## 2026-09-15 — wrap-up (internal consistency before GitHub)

Debris from the Aug 25/31 pack still argued the withdrawn seat doctrine. Closed in this pass:

### Changed
- `engineering/01-NO-NEW-DATA-PACK.md`, `02-IPAD-ACCOUNT-BRIEF-SPEC.md`, `03-ROADMAP.md` — rewritten onto `JOB-*` / persona groups. EBR-91 first, A2/A3/A4, extract/offline/fail-closed kept. `02` is **PG-01 only** (24-month by collection); not a universal rep brief.
- `PERSONA-READOUT.html`, `CEO-READOUT.html`, `CEO-BRIEF.html` — replaced with withdrawn stubs that redirect to `PERSONA-GROUPS-REVIEW.html`.
- `_measured/00-FINDINGS.md`, `_measured/06-SEGMENT-VARIATION.md` — banners: measured seats; “4 of 31” is not current doctrine.
- `ASSUMPTIONS.md` F-10 — CS2 recorded as deleted.

### Still not this pass (not an agent job)
Interview validation of JOB-* · factory copy (hold) · commit/push · Postgres re-measure.


