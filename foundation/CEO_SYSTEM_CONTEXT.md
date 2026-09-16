# SuperCat — Agent Context (CEO System)

Use this to ground judgments about ICP fit, competitive positioning, pricing
sensitivity, strategic alignment, **and how to treat any figure you report**.
This is the **agent-optimized condensation** of the full foundation set
(`foundation/01`–`07`). When you need depth, read the source doc named at the end
of each section.

**Last updated:** 2026-09-15 (**SuperCat personas = who consumes which product.** Buyer → eOL; rep analytics → iPad-EC. Motion is a job pack, not eight extra people. Withdrawn: "build once, only 4 of 31 jobs vary." Lineage still holds: Lens 2 is a stamped roster lookup, post-sale only; never label a prospect. Prior version: `_archive/CEO_SYSTEM_CONTEXT_2026-09-15_pre-persona-groups.md`.
Prior: 2026-08-27 persona added as a third axis — 7 personas / 31 jobs, orthogonal, plus the now-withdrawn build-once rule. Archive: `_archive/CEO_SYSTEM_CONTEXT_2026-08-27_pre-persona-axis.md`.
Prior: 2026-08-26 Lens 2 corrected — selling-motion segments are a **stamped roster
lookup, not a computation**, and are **post-sale only**; never label a prospect. Source pointer
fixed from the non-existent `skills/customer_segmentation/` to
`foundation/sources/customer_segmentation/`. Prior version:
`_archive/CEO_SYSTEM_CONTEXT_2026-08-26_pre-segmentation-lineage-correction.md`.
Prior: 2026-07-22 buyer-type index expanded via 20-org dual-socialize preflight — trade-showroom +
designer goldens; coverage note 19 reads / 8 orgs. 2026-07-14 redesigned Who-We-Serve as runtime
judgment contract; 2026-07-10 added Selling Motion lens + account buyer-type resolver).

---

## Data & number discipline (read first — how we treat figures)

Before you state any number, apply the epistemic standard (full version:
`foundation/07_how_we_establish_truth.md`; authority:
`skills/insightful_product/00_provenance_spine.md`):

- **No bare numbers.** Every total carries **confidence** (FULL / STRONG /
  PARTIAL / LIMITED / NONE) and, for any total/denominator, a **completeness**
  read. When you can't stand behind a figure, **suppress rather than guess.**
- **A composite inherits the *lowest* confidence of its inputs.** Confidence
  never rises by combining sources.
- **Name the source of truth.** For commercial outcomes, invoiced/ERP is truth;
  an app order, cart, quote, or pipeline stage is **intent**, not a transaction.
- **Capture ≠ attribution.** What flows through our own rails is a fact; our
  *share of* a larger whole is a gated estimate — never present one as the other.
- **Billed ≠ collected.** Never imply cash, AR, or "money in the bank" from
  billing/invoiced data alone.
- **Identity gaps are real; silence ≠ zero.** When a mapping (rep→revenue,
  entity→parent) is incomplete, degrade the grain or suppress — never silently
  drop unmapped rows (that fabricates a ranking).
- **First-party behavior over imposed labels.** Segments/scores derive from what
  customers do; external enrichment is validated against, never seeded from.
- **Label live vs. illustrative**, and **lead with the decision**, caveats below.

*Source: `foundation/07_how_we_establish_truth.md`.*

---

## What We Are

- Commercial operating system for furniture, lighting, and home-décor manufacturers.
- **Five connected surfaces, not five products** — they share one catalog, one
  customer file, one user file, one configuration model.
- Deepest CPQ in the competitive set — configurable products with option sets
  (up to 8 or 20), option mappings, riser pricing, matrix options, and kits.
- The commercial value is packaged as the **Insights Layer** (80+ value moments
  across 13 domains, provenance-governed; see below) — the defining T3 differentiator.
- Install base ~104–118 active accounts (count varies by inclusion rule — see
  ICP note). ~$6.5M annual GMV through the reference deployment (Braxton Culler).

### The five surfaces (adoption out of 118, Jan 2026 capability audit)

| Surface | Adoption | Price | What it is |
|---|---|---|---|
| **eCat iPad app** | 88 | $725/mo (25 users incl.) | Center of gravity — **rep selling instrument** (browse → configure → present → write), fully offline. Submit is optional; consummation often lands in ERP / other channels. |
| **eCat Online — Catalog** | 48 | $295/mo | Public buyer browsing (same catalog as iPad, on web). |
| **eCat Online — B2B Cart** | 26 | $295/mo | Buyer self-serve ordering when the account chooses that path — not a universal upgrade mandate. |
| **eCat Online — Closed Site** | 43 | $100/mo | Authenticated-only access; pairs with self-service enrollment (feature name — not “make them order on eCat”). |
| **Sales Portal** | 32 | $395/mo | Where sales leaders / CS live: dashboards, top products/customers/territories, order & invoice management, CSV/XLSX export. |
| **Admin Console** | (all iPad) | included | Back-office: catalog, taxonomy, users, price levels, and config screens for every gated capability. |
| **Data integration / platform** | — | — | FTP import (default-on), ERP order export (STD JSON v2), address verification, CDN, external API, Bluelink. This is the "you're our system of record" layer. |

The **adoption ladder** (iPad → Online Catalog → Closed Site → Portal → Cart)
is the maturity path and the best read on expansion readiness. Architecture is
currently **modular** (add surfaces à la carte) and is being collapsed into
T1/T2/T3. *Source: `foundation/01_what_we_do.md`.*

---

## The Insights Layer — 80+ value moments across 13 domains (the moat)

What we ship is the surfaces; **what customers get** is a catalog of discrete,
named insights/recommendations the platform produces (value moment catalog
**v4.2**). Delivered per-customer via Cursor operator prompts (packaged-product
vs. operator-deliverable is an open commercial decision).

| # | Domain group | Examples |
|---|---|---|
| 1–8 | **eCat / behavioral families** — Rep Performance *(anchor)*, Instance Health, Customer & Buyer, Ordering & Commerce, Product & Inventory, **Cross-Instance Benchmarking** *(LIVE in BigQuery)*, SuperCat-Internal (health/churn/expansion), Portal & Demand-Side *(Clicky)* | VM-01→50 |
| 9–13 | **Commerce Intelligence Stack** *(4.0 — ERP-grounded)* — Commerce Economics (C-series, the "Money Map"), Channel / "Where You Sell", Customer Economics (K-series), Rep Outcome & Copilot (R-series), Exception Push | VM-C, VM-CHAN, VM-K, VM-R, VM-S |

**Why it matters for judgments:** Domain 1 ties per-rep behavior to order
outcomes via a validated correlation model (r > 0.96 for customer targeting).
**No competitor in the audit has cross-customer benchmarking** — it's the
strongest counter to WizCommerce's AI-first positioning. The killer worked
example is "find your Katrinka": a rep strong on targeting/discovery but weak on
configuration conversion, with a quantified coaching upside. The 4.0 stack
(Domains 9–13) adds ERP-grounded economics — but every money number ships with a
confidence + completeness stamp or is suppressed (see Data & number discipline
above). *Source: `foundation/01_what_we_do.md`; catalog at
`skills/insightful_product/04_value_moment_catalog.md`, truth/confidence
authority at `00_provenance_spine.md`.*

---

## Entity Chain (get this right)

- **SuperCat** = the platform vendor. We build and sell the software.
- **Our customers** = furniture/lighting/home-décor manufacturers who subscribe.
  They own the catalog, the rep relationships, and the dealer network.
- **Our customers' customers** = dealers, designers, retailers, contractors who
  buy from manufacturers through the platform (the four buyer roles below).
- **Reps** belong to the manufacturer, NOT to SuperCat. When a rep writes an
  order on the iPad, that is the manufacturer's sales motion — we provide the tool.
- **"SuperCat helps manufacturers do X"** is almost always correct.
  **"SuperCat does X"** is almost always wrong (unless X is building software,
  selling subscriptions, or providing support).

### The four buyer roles (our customers' customers)

| Buyer role | What they need | How SuperCat shows up |
|---|---|---|
| **Designer** (interior, hospitality, contract) | Curated selections for a project; visuals, finishes, lead times | Smart stacks, PDF catalogs, configurable products, spec sheets |
| **Retailer** (furniture store, lighting showroom, dealer) | Restock bestsellers; routine reorders | Reorder workflows, contract pricing, inventory visibility, B2B Cart, portal |
| **Contractor / Builder** (commercial, hospitality, multifamily) | Large project orders; spec compliance; ship-date predictability | CPQ for built-to-spec, kits, address verification, ship/cancel-date controls, RMA |
| **Project-based commercial buyer** | Mixed designer/retailer-led; flexibility, on-demand access | Closed-site portal, eOL projects, enrollment workflows |

**Account-level buyer type (sharper than the four roles).** The four roles are the
coarse platform-surface view. When profiling or writing to a *specific* account,
resolve its buyer type from **its own evidence (start with the customer's website)** —
never inherit it from the brand's segment. Four resolved types:

- **Retailer — consumer / e-commerce / omnichannel** — storefront + DTC cart/pricing +
  promotions + multi-brand assortment; sells *through to consumers*. Voice: sell-through,
  merchandising, bestsellers, fulfillment.
- **Showroom / dealer (trade-led)** — appointment / "to the trade," no consumer cart,
  display floor of multiple lines. Voice: display + trade, not consumer sell-through.
- **Designer / trade** — A&D, login-gated pricing, project portfolio, no storefront.
  Voice: what they *specify* into projects; cadence usually not meaningful.
- **Distributor / mass / institutional** — wholesale / bulk / logistics-led; use
  **commercial velocity** artifact mode (category/program/fill), not a forged taste spine.
  Still in scope for brand-to-customer and sales-rep copilot.

The load-bearing rule: **the brand's segment sets product vocabulary; the account's
buyer type sets the framing; artifact mode (0c) sets letter/coaching shape — never
conflate them, and never treat Volume/Mid-Market brands as out of product scope.**
The retailer sub-distinction (consumer/omnichannel vs trade-led) is the most common miss.
*Source: `foundation/02_who_we_serve.md`; resolver in
`skills/agent_research/brand_to_customer/PROFILE_SYNTHESIS.md` (Steps 0a/0b/0c).*

---

## Who We Serve — judgment contract (apply on every customer claim)

This is the runtime customer ontology. The 10 CEO prompts read *this file*, not
`foundation/02_who_we_serve.md` — so the rules below are the operating contract, not
a summary. Detail follows in the two lens sections; this is how to *use* them.

**Lens router — pick the lens by the question, never collapse them:**

| If the question is about... | Use | Never |
|---|---|---|
| Pricing, WTP, tier fit, expansion path | **Lens 1 — Digital Selling Maturity** | reading tier off selling motion |
| GTM, messaging, positioning, buyer mix, per-account taste | **Lens 2 — Selling Motion** | reading vocabulary off maturity |
| Portfolio / an account's full posture (e.g. an upgrade play with the right message) | **Both** (cross-tab) | assuming one predicts the other |
| **Who *uses* the product, what job they're doing, what to build for them** | **SuperCat persona** (who consumes which product — admin / VP / exec / sales rep / buyer) | treating login seats (PER-01…08) as the persona set, or shipping one analytics home screen for every rep / one eOL bet for every buyer |

The two lenses are **orthogonal** — a Luxury Specification brand can be Catalog-Focused
or Platform-Embedded; a Platform-Embedded account can be any selling motion. **Segment
is not tier**: ~19 accounts are behaviorally Commerce-Active but modularly T1 (the top
upgrade cohort). Both lenses reject revenue band, vertical, and org scale as classifiers.

**SuperCat personas are who consumes which product**, not a third axis that ignores selling motion. A segment is a property of the client *organisation* (roster lookup). Motion parameterizes jobs on **sales rep** and **buyer** only. Do not mint eight SuperCat people. Do not put a segment on a prospect. See § Persona groups.

**Channel honesty — binds every customer-of-customer figure (inherits the Provenance Spine):**

- eCat / iPad orders are **intent through one rail, not the account's business.** Where an
  ERP feed exists, invoiced net is the commercial truth and eCat is a labeled secondary.
- eCat is **directionally unreliable** as a size proxy — it ran **0.22–3.10x** the invoiced
  truth across the brand_to_customer cohort (usually understating 2–4.5x). Never state an
  account's size from eCat alone.
- Carry a **channel posture**: `ALL_CHANNEL` (ERP feed present + account resolves at
  `customer_bill_to_number`) → lead with invoiced net; `ECAT_ONLY` → absolute eCat $ only
  + completeness caveat, never "total business." **Capture ≠ attribution** (no wallet-share
  rate). This is the same discipline as the Data & number section above, applied to customers.

**Selling vs consummation — binds every agent narrative (not just dollar labels):**

- eCat iPad = **rep selling instrument**. Order consummation often stays in ERP / phone /
  EDI / market / the account’s own ecommerce even when the rep sold well on iPad.
- Do **not** pathologize ERP-active accounts with low SuperCat-submitted history as failed
  “eCat adoption,” or pitch bare “streamline *their* ordering” / “convert them to eCat.”
- **Also do not erase enablement:** email/phone → ERP re-key is a real industry pain.
  When that pain is plausible, coach a digitally enabled path (structured submit → ERP) as
  optional partnership value — named pain, not capture shame.
- Default ask: get the **rep** in the loop (present, stock, story). Escalate to process
  enablement only with a concrete pain named.
- Full doctrine: `foundation/02_who_we_serve.md` § Selling instrument vs order consummation.

**ICP anti-patterns (do not do these):**

- Inherit an account's framing from its brand's segment (a Luxury Spec brand's book still
  holds retailers — resolve buyer type from the account's own evidence/website).
- Treat the external marketing niche ("$10–250M … reps/dealers/showrooms/designers") as the
  analytical ICP. It is an outside-in pitch only.
- Present eCat GMV as an account's real revenue, or collapse segment into tier.
- Narrate bare “eCat adoption / streamline their workflow” with no named pain (selling-vs-
  consummation failure mode). Equally: refuse to mention digital enablement when re-key /
  email→ERP pain is the real story (overcorrection failure mode).
- Assert WTP or NRR-by-segment as fact — they are hypothesized. JTBD is registered by persona group; still unvalidated by customer interview.

**Coverage & what is still unvalidated (do not overclaim certainty):**

- **Buyer-type census is still a seed, not a census** — the evidence index
  (`foundation/sources/customer_segmentation/account_buyer_type_reads.csv`) holds **31 reads across
  15 of ~109 orgs** (recounted 2026-08-26 on the same basis as the original — all rows, any
  confidence. The prior note said 19 reads / 8 orgs as of 2026-07-22, which the file reproduces
  exactly at that cutoff; it grew by 12 rows on 7/23–7/24).
  Includes website-verified **trade-led showroom** (A. Hoke, CAI Designs, Gorrod
  Gallery) and **designer / trade** (Michelle Gerson) goldens — not only omnichannel retailers.
  Still use as illustration, not distribution. Name alone is unreliable ("Kathy Kuo Designs" is a
  luxury e-comm retailer).
- **JTBD is registered by SuperCat persona** (admin / VP / exec / sales rep / buyer) (2026-09-15).
  Buyer jobs land on eCat Online; rep analytics is an iPad-embedded component. Selling motion
  changes grain on those two only (eOL fit; iPad-EC job pack). Admin / VP / exec stay three
  surfaces. Still outstanding: customer-interview validation. Do not cite "only 4 of 31 jobs vary."
- **Still hypothesized**: WTP/value-driver ranking, NRR/churn/expansion by segment, install-base
  geography, the full Lens 1 × Lens 2 count matrix, and a single as-of customer count
  (104/109/110/118/132 all valid under different rules).

*Source: `foundation/02_who_we_serve.md`; channel doctrine `skills/insightful_product/00_provenance_spine.md` + `skills/agent_research/brand_to_customer/CHANNEL_PROVENANCE.md`.*

---

## ICP Segments — Lens 1: Digital Selling Maturity (pricing / WTP / expansion)

We hold **two complementary, orthogonal first-party lenses** on the same base.
This is Lens 1 (pricing/expansion); Lens 2 (Selling Motion) is below. Both reject
revenue band, vertical, and org scale as classifiers; they cross-tabulate.

Segmentation is **behavioral posture, NOT revenue band or vertical.** Revenue
band, vertical, org scale, digital-surface readiness, and tech sophistication
were each tested against install-base data and **explicitly rejected** (they
don't predict product need, willingness-to-pay, or expansion path). A $200M
manufacturer can be Catalog-Focused. Baseline n=104 (M1 stamped 2026-01-28).

| Segment (tier) | Accounts | Median MRR | Channel | Vertical mix | GMV per $1 MRR (capture) | Segment GMV (capture) |
|---|---|---|---|---|---|---|
| **Catalog-Focused (T1)** | 56 (54%) | $778 | 100% iPad | 55% Light / 23% Furn | ~$480 | ~$82M |
| **Commerce-Active (T2)** | 28 (27%) | $1,822 | 96% iPad / 4% eOL | 43% Furn / 40% Light | ~$852 | ~$161M |
| **Platform-Embedded (T3)** | 20 (19%) | $2,173 | 49% iPad / 51% eOL | 57% Light / 33% Furn | ~$2,561 | ~$768M |

*GMV columns are **platform capture** (GMV flowing through SuperCat's rails), not the accounts' total commercial volume — do not present them as the customers' revenue (see channel honesty in the judgment contract).*

- **Catalog-Focused** — digitizing catalog + rep tools; ordering is rep-led /
  off-platform. Not "small companies" (includes WAC/Modern Forms at 332K
  products, Visual Comfort Signature). Expansion: **T1→T2, activate the Online
  Catalog gateway** then add Cart + Order/Invoice Tracking.
- **Commerce-Active** — digital ordering alongside field sales. **Strongest
  engagement intensity per dollar**; ~67% still missing B2B Cart. Exemplars:
  Palecek, Hubbardton Forge, Crystorama, Craftmade. Expansion: **T2→T3
  analytics/dashboards/territory views**.
- **Platform-Embedded** — SuperCat is core infrastructure. Defining marker is
  the **49/51 iPad/eOL parity**. Highest switching cost; the real risk is
  build-internally, not replacement. Expansion lever is **services / premium
  support / brand expansion**, not price (60% already at/above book). Exemplars:
  Summer Classics ($466M GMV), Jamie Young, Wildwood/Chelsea House, Currey & Co.

**Segment ≠ tier 1:1 (expansion signal):** ~19 accounts are behaviorally
Commerce-Active but modularly T1 — the **highest-conversion T1→T2 upgrade
targets** in the install base. Segments inform *how we talk to customers*; tiers
inform *what they pay*. Keep both lenses.

**Count caveat:** different valid sources cite **104** (master data v3, M1
segmentation), **110** (Q425 readout), **118** (capability audit / active orgs),
**132** (cross-instance BigQuery). Different inclusion rules and dates — none is
wrong; no single "as-of now" number is canonical. Use the one matching your data
window and say which. *Source: `foundation/02_who_we_serve.md`.*

---

## ICP Segments — Lens 2: Selling Motion (v4.0) (GTM / product-identity / buyer)

The **complementary** cut of the same install base (Client Segmentation v4.0,
stamped 2026-07-09, roster n=109). Where Digital Selling Maturity predicts *what
they pay and how they expand*, Selling Motion predicts *how they go to market, who
they sell to, and how their assortment reads* — the axis that governs messaging
vocabulary, buyer-type expectations, and per-account taste (it powers
`brand_to_customer`). Use Lens 1 for pricing/tier work; Lens 2 for GTM, positioning,
and customer-identity work.

| Segment (motion) | n | How they sell | Signature |
|---|---|---|---|
| **Luxury Specification** | 33 | Designers/architects specify into projects | High AOV ($5K+), aesthetic collections; e.g. Palecek, Theodore Alexander, Visual Comfort Signature, Currey & Co. |
| **Premium Trade Brand** | 38 | Dealers carry the line on brand reputation | Broad dealer network, territory coverage; e.g. Braxton Culler, Summer Classics, Jamie Young, Hubbardton Forge |
| **Mid-Market Multi-Channel** | 24 | Trade + retail + online + contract | Many price codes, collection-heavy catalogs; e.g. Savoy House, Craftmade, Kichler |
| **Volume Distribution** | 14 | Commodity, high volume, low touch | Low AOV, very high order counts, flat pricing; e.g. Abaline, Home Essentials, Kennedy Int'l |

**Three axes:** *how they sell* is the classifier; *what they sell* (vertical:
furniture/lighting/outdoor/decor/accessories/rugs/textiles) is a tag, not a cut —
it sets the product's attribute vocabulary; *who they sell to* (buyer type) is
predicted by motion at the brand level but resolved per-account from evidence (see
"Account-level buyer type" above). Price is a continuous correlate, not a boundary.

**Lens 2 is post-sale only.** Every field that defines a selling-motion segment — average order
value, price-code count, customer count, order volume — exists only in SuperCat's Postgres and only
after an instance is loaded. **Never assign a selling-motion segment to a prospect**, in a CRM field
or otherwise. For pre-sale classification use the Prospect Archetypes
(`foundation/sources/customer_segmentation/taxonomy/prospect-archetypes.md`), which are named for
what is observable and never inherit a segment name — per `07_how_we_establish_truth.md`
principle 7, enrichment is validated *against* a first-party segment, never seeded *from* one.

**The segment assignment is a stamped roster lookup, not a computation.** v4.0 is Kjael's
selling-motion judgment (2026-07-09) carried forward from v3.2 and *corroborated* by Postgres, not
produced by it: an authored rule over the four defining fields reproduces the stamped label only
**38.5% of the time against a 34.9% majority baseline (n=109)**, with a 50.0% ceiling even when
thresholds are fitted to the answer key. Look the org up in the MASTER roster; do not re-derive it,
and do not treat a refresh of the underlying numbers as a re-segmentation.

State the pre-sale limit precisely: **binary public feature extraction cannot predict a segment
(33.3% vs a 34.5% majority baseline, n=87); holistic site reading reaches roughly 53% vs a 30%
baseline; neither is good enough to label a prospect.** Do not compress this to "public data cannot
predict segment" — that overstates it.

*Source: `foundation/sources/customer_segmentation/` (README + `taxonomy/`);
`Customer Segmentation/current/` (stamped v4.0 md + MASTER csv);
`foundation/02_who_we_serve.md`.*

---

## Persona groups (who consumes which product)

**A login seat is not a persona.** PER-01…PER-08 are headcounts. PG-01…08 are **job packs** on
rep/buyer, not eight SuperCat users. The persona set:

| Persona | Consumes | Analytics jobs land |
|---|---|---|
| **Admin** | Admin Console | Catalog completeness, import landed, order keyed right |
| **VP of sales** | Sales Portal | Export=screen (EBR-91 first), team using it, reconstruct account, slipping accounts |
| **Executive** | Insightful | One invoiced topline. Suppress without a feed |
| **Sales rep** | eCat iPad | Selling: existing iPad (protect). Book analytics: **new iPad-EC**. Pack by stamped segment |
| **Customer / dealer / buyer** ⚠️ | **eCat Online** | Order without a rep, my price + stock, what I ordered/billed. Fit follows motion |

⚠️ = *our customer's customer*. Jobs exist only if they pay the manufacturer.

**Motion packs (not extra personas):** spec-rep 24-month by collection ≠ trade dealer-line ≠ skip-volume. eOL: spec highest, trade high, multi-channel long-tail, volume core never. Do not fold designer / dealer / chain into one eOL bet.

**Seats (still true):** ~4k iPad-active internals vs ~19k eOL-active buyers; almost no overlap; a buyer cannot reach rep views. Mixpanel is iPad-only — reps search products, they do not live in Portal. Agency principal is unservable this cycle.

Look the org's motion up in the v4.0 roster. Do not recompute it. Do not label a prospect.

*Depth: `foundation/sources/customer_segmentation/personas/00-PERSONA-GROUPS.md`; jobs in
`analytics/jtbd-register.md`; surfaces in `product/surface-mapping.md`.*

---

## Build buyer jobs on eOL; rep analytics as iPad-EC; HQ stays split

**Do not ship one analytics surface and swap adjectives.** Spec-rep book (project/collection,
24-month) is not volume-rep catalog reference.

**Do** put all buyer jobs on eCat Online, and target eOL expansion by motion (spec/trade high,
multi-channel long-tail, volume core never). **Do** build one **iPad-EC shell** and load the
JOB-REP-1 pack from the stamped segment. **Do** keep admin / VP / exec on Admin / Portal /
Insightful — they are three personas, not one HQ blob.

*Source: `foundation/sources/customer_segmentation/analytics/jtbd-register.md`;
`foundation/sources/customer_segmentation/product/surface-mapping.md`.*

---

## Pricing (2026 Tiers — stamped)

| Tier | Platform | Included users | Hero capability |
|------|----------|----------------|-----------------|
| T1 Catalog Essentials | $749/mo | 10 | Online Product Catalog gateway |
| T2 Commerce Professional | $1,295/mo | 15 | B2B Cart + Order & Invoice Tracking |
| T3 Commerce Enterprise | $2,295/mo | 40 | Sales Intelligence + Insights Layer |

User expansion: $25 → $22 → $20 → $18 (step-declining beyond included). No annual
discount. Implementation: Included / $2,500 / $5,000 by data readiness.
**Win line:** when setup fees are amortized, SuperCat's Y1-effective cost is at
or below AmpTab at **every** tier; T3 ($2,545 at 50 users) is 15% below AmpTab
Pro ($3,000). *Source: `foundation/03_how_we_make_money.md`, `04_market_and_competitors.md`.*

---

## What We Sell Against (buyer friction, in customers' own words)

From 89–110 customer-facing meetings across 45 companies, FY2025. This is the
market-sensing vocabulary — the language buyers actually use.

- **Pain (what's broken):** visibility gaps (36), manual process burden (34),
  error/mistake risk (17), configuration complexity (16), inconsistent messaging (12).
- **Impact (what it costs):** velocity drag (48), missed opportunities (41),
  error & rework (36), efficiency loss (24), admin overload / "80% admin, 20% selling" (12).
- **Objections (what blocks the deal):** time/bandwidth (98), adoption/training (12),
  price/cost/budget (12), integration lift (12), feature parity (7).

**The wedge:** the problem is *manual coordination → rework → velocity drag*;
the objection is *time and bandwidth*, not price (only 12 of 110+ cited price).
We remove the manual-coordination tax — we do not compete on price.
*Source: `foundation/04_market_and_competitors.md`.*

---

## Competitive Set

| Competitor | Threat | Their message | Our counter |
|------------|--------|---------------|-------------|
| **AmpTab** | Medium (most common) | Same vertical, unlimited users, transparent G/B/B | Y1 TCO lower at every tier; Order & Invoice Tracking at T2 (they gate at $3K Pro); deeper CPQ |
| **WizCommerce** | **High (one to watch)** | AI-first, sub-30-day impl, $8M raised, 500+ customers | CPQ gap (they don't have it); depth for complex furniture/lighting data; Insights Layer vs generative AI |
| **Pepperi** | Medium (enterprise) | Enterprise breadth, unlimited users, multi-language, DSD | ~60% less cost; vertical depth vs horizontal breadth (lose fast on multi-language/DSD) |
| **MarketTime** | Low-Med | Network — 6,500 brands, 300K buyers, $5B+ orders | Platform vs marketplace — different value prop; price transparency (they're quote-only) |
| **RepZio / ShopZio** | Low | $25/user, no tiers, ANDMORE trade-show bundle | Rep tool vs commerce platform — show the feature gap |
| **Status quo / "we can build it"** | **Most common loss path** | "Our IT / a dev shop / Shopify can build this" | Total build cost > 5 yrs of SuperCat; you're buying ongoing product investment, not a one-time build |

**Where we win:** vertical depth; deepest CPQ (only AmpTab has any, and it's
gated); Order & Invoice Tracking at T2; Insights Layer at T3; price transparency
(78% of B2B buyers demand upfront pricing); Y1 TCO ≤ AmpTab.
**Watch (not yet in the named set):** ERP / horizontal encroachment — NetSuite,
Acumatica, Salesforce B2B Commerce, Shopify B2B (the "build it on Shopify"
pattern). *Source: `foundation/04_market_and_competitors.md`.*

---

## Strategic Bets (12–24 months)

1. **Monetization Refresh** — T1/T2/T3 migration correcting the modular
   below-book/above-book inequity. ACV is the success metric.
2. **Insights Layer** — the value moment catalog (v4.2, 80+ VMs, provenance-governed)
   as the T3 differentiator and moat; cross-instance BigQuery is live. No competitor
   has cross-customer benchmarking.
3. **FY26 Target** — $2.12M subscription revenue (+15.2%), $2.27M implied ARR
   (+23.4%), year-end ACV $20,166 (+14.0%), ~120 accounts.
4. **ROI Calculator** — sales acceleration; prospects see payback from their own
   data without overclaiming.

*Source: `foundation/05_strategic_direction.md`.*

---

## Market Shape

- TAM ~4,651 wholesale home-furnishings firms (68% Furniture, 17% Lighting,
  7% Home & Décor).
- 71% run the dealer + trade selling motion (our sweet spot); ~81% have
  low-to-medium digital readiness (natural T1/T2 prospects).
- TAM vertical mix is **inverted** from the install base (TAM Furniture-heavy;
  base Lighting-heavy) — the behavioral segmentation generalizes across
  verticals, so growth into Furniture is not a different segmentation question.
- **Marketing niche (external line only):** "mid-market furniture, lighting &
  home-décor manufacturers ($10–250M) selling through reps, dealers, showrooms,
  designers." A useful outside-in simplification — NOT the analytical
  segmentation. *Source: `foundation/02_who_we_serve.md`.*
