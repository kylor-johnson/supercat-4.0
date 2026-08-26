---
id: SYNTHESIS
title: Who we serve, and what we should build — synthesis
version: 0.1
status: draft
date: 2026-08-25
owner: Kylor Johnson
note: Synthesis only. No new analysis. Every figure is sourced in the files this points to.
depends_on: [TAX-A, TAX-B, TAX-MAP, PER-00, JTBD-REG, PROD-MAP, PROD-GAPS, PROS-CRIT]
---

# Synthesis

Twenty files sit behind this one. This is the two-page version.

---

## 1. What we now believe about who we serve — and what changed

**Three things we believed were wrong.**

**Our segments are stamped human judgment, not a computation.** We have been describing the v4.0
selling-motion segments as derived from first-party Postgres data. They are not. An authored rule
over the four defining fields — average order value, price-code count, customer count, order volume
— reproduces the stamped label **38.5% of the time against a 34.9% majority baseline**, with a
**50% ceiling** even when thresholds are fitted to the answer key. The segments came from v3.2
selling-motion judgment; Postgres *confirmed* them, it did not *produce* them. This does not weaken
the segmentation — stamped judgment about observed behaviour is legitimate under our own epistemic
standard — but it changes the operating rule: **the authority is a roster lookup, not a
recomputation.** New order data does not re-segment anyone.

**You cannot put a segment label on a prospect.** Everything that discriminates selling motion only
exists after a company is a customer. We tested a second method to be sure: binary feature
extraction across 87 roster companies' public websites reached **33.3% against a 34.5% baseline** —
no better than guessing the largest segment. One archetype of four beat baseline (trade-gated
access → Luxury Specification, 65%), and its most useful property was **exclusion**: 0 of 20
trade-gated companies were Mid-Market Multi-Channel.

**But the honest claim is narrower than "public data doesn't work."** The earlier holistic run — an
LLM reading whole sites — reached ~53%. Same web, different method. The worked case is Interlude
Home: unmistakably a trade brand, scored `TRADE_GATE = 0`, because it gates by "DESIGNER RESOURCES"
rather than "to the trade." A person sees that in three seconds. So: **binary extraction cannot
predict segment; holistic reading gets to roughly 53%; neither is good enough to label a prospect.**
That gap is why the field kit sends a person.

**Consequence:** two explicitly separate layers. Account Segment (post-sale, roster lookup) and
Prospect Archetype (pre-sale, named for what is observed, never inheriting a segment name).
Corrections to `02_who_we_serve.md` and `CEO_SYSTEM_CONTEXT.md` are drafted and **held** in
`FOUNDATION-CORRECTIONS.md`.

---

## 2. The persona → analytics → surface answer

**7 personas, 31 jobs, one primary metric each.** 20 candidate jobs were cut — six because the data
does not exist, four because no decision changed.

**The headline is build-once-parameterise.** Only **4 of 31 jobs vary by Account Segment**. And the
four that do vary track **catalog scale, territory count and price-code count** — structural facts
any org can read off its own data — **not selling motion**. A job does not need to know an org is
Luxury Specification; it needs to know how many price codes it has. **One surface serves everyone,
parameterised on org structure.** That is the simpler and cheaper build, and it is far better
supported than the alternative given Layer A reproduces at 38.5%.

**Two population facts reshaped the persona set.** Buyers are **87,927 enabled / 17,532 active**
against **4,058 iPad-active reps** — and only **593 users** are active on both surfaces. Reps and
buyers are near-disjoint populations who share no session and no mental model. The buyer was missing
from the original scope and is now the largest persona in the register, tagged
*our-customer's-customer*, with jobs justified by what **our client** gains from serving them.

**And there is no incumbent rep analytics surface.** The Sales Portal Territory Dashboard is enabled
for **zero organisations**; Reports reaches six. Nothing is being displaced — but there is also no
usage evidence, so every design assumption is untested.

---

## 3. What we'd build, in priority order

**We build it** (engineering, ours to control):

| | Item | Size | Why first |
|---|---|---|---|
| 1 | Export/UI reconciliation (EBR-91) | S | A defect fix that gates trust in every Portal number |
| 2 | Ungate rep activity | S | Data exists; on for **7 of 257 orgs** |
| 3 | Catalog completeness view | S | No new fields — pure aggregation |
| 4 | Inventory snapshot age in the UI | S | One timestamp; unblocks every staleness rule |
| 5 | Product launch date | S | One nullable column unblocks a whole job |
| 6 | Per-account baseline store | M | Unblocks "fading account" for both rep and owner |

Four of the first six need **no new data at all** — an aggregation, a config flip, a defect fix and
a surfaced timestamp.

**Client must send it** (a conversation, not a sprint):

**The invoice feed is the single biggest constraint in the register — present for 38 of 109 orgs,
degrading 13 of 31 jobs.** No surface work fixes it. Critically, the 13 do not fail uniformly:
**seven degrade to a usable order-based view** and are shippable with a mandatory label (eCat runs
0.22–3.10× invoiced truth, usually understating), while **six fail outright** — anything whose job
is "what really happened commercially," including both toplines and both agency-value jobs.
Onboarding an invoice feed is the highest-leverage single change available for those 71 accounts.

**Deliberately not in the first tier:** the rep agency entity (L — and **PER-02 is not servable at
all** until it exists; 11,873 free-text company names is a migration, not a schema change), and the
iPad rep-analytics component, which should wait until the surface conflict below is settled.

---

## 4. What HPMKT is actually testing

**The frame is already worked.** 26 of 30 checked candidates are in HubSpot; three carry open deals;
**72 of 693 exhibitors are already customers**. Fresh-prospect rate ~**17%**.

**So market week is not a discovery exercise.** The kit's script is **displacement and
re-engagement** — most booths will be a known name, and every walk-list row must carry its HubSpot
state before the conversation starts.

**What it does test** is whether a person with a browser can classify a prospect more reliably than
a checklist — four live hypotheses, each with the observation that kills it. The designated test is
the lane-1/lane-2 boundary, where two candidates (Designmaster, Home Trends and Design) carry both
designer *and* dealer vocabulary and no checklist resolves them.

**Lane 3 runs thin, deliberately.** Savoy House is not a High Point exhibitor and the HPMKT lighting
category is décor houses, not program lighting. Coast Lamp Mfg is the single genuine test, and the
thin yield is itself the finding: **mid-market decorative lighting is not a High Point population.**

**The strongest signal found was not in the criteria at all.** Eleven exhibitors run **AmpTab** and
three run **WizCommerce** — all 11 AmpTab installs confirmed as real deployments, two with
per-tenant IDs. Zero RepZio, Pepperi or MarketTime across 437 homepages. A company running a
competitor's platform has self-certified every qualification condition plus willingness to pay, and
**five of the 14 are not in HubSpot at all** — a better fresh yield from a cheaper signal than the
entire lane screen produced. It is a **qualification** signal, not a segment signal, and has not
been folded into the archetypes.

---

## 5. Open decisions — yours

| # | Decision | Why it needs you |
|---|---|---|
| **1** | **Apply the foundation corrections?** | `02_who_we_serve.md` and `CEO_SYSTEM_CONTEXT.md` currently tell every agent the segments are data-derived and knowable at first touch. Both are wrong. Drafted and held; `CEO_SYSTEM_CONTEXT.md` is the runtime file and should go first |
| **2** | **Sales Portal — leadership+CS, or reps first?** | Two stamped documents disagree and it changes what gets built for JTBD-011/021/031. The asymmetry matters: getting it wrong one way costs a wrapper; the other way costs the wrapper *and* leaves the field case unsolved. Cheapest way to settle it is asking reps at market |
| **3** | **Expose buyer purchase history?** | A config change reaching **~13,800 additional active buyers**, not a build. Blocked on a client-risk review — pricing-entitlement and competitive exposure are our client's call about their own customers, not ours |
| **4** | **Commit to PER-02 rep agency, or say no?** | Not servable before the agency entity exists. Recommend saying no this cycle rather than shipping an approximation that silently merges distinct agencies |
| **5** | **Invoice-feed push for the 71 orgs without one?** | Largest constraint in the register; a commercial motion rather than engineering work |
| **6** | **Delete `Customer Segmentation 2`** | Byte-identical duplicate of the answer key. On the ignore list; you said you'd remove it |

---

## Where things are

| Layer | File |
|---|---|
| Taxonomy | `taxonomy/account-segments.md` · `prospect-archetypes.md` · `segment-archetype-mapping.md` |
| Personas | `personas/PER-00-persona-set.md` + 7 persona files |
| Jobs | `analytics/jtbd-register.md` — all 31, flat |
| Product | `product/surface-mapping.md` · `product/data-gaps.md` |
| Prospects | `prospects/` — lane criteria, 3 lanes, disqualified, competitor signal |
| Field kit | `field-kit/test-design.md` · `worked-example-the-manual-read.md` |
| Held | `FOUNDATION-CORRECTIONS.md` · `ASSUMPTIONS.md` (5 assumptions, 4 data-quality items, 22 findings) |
