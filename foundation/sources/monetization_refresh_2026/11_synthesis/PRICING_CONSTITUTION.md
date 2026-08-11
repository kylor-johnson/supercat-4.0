# SuperCat Pricing Constitution

> **Purpose**: The authoritative, living record of stamped decisions for the 2026 pricing refresh. Each decision is numbered, dated, and final unless explicitly reopened. Exploratory-phase work is preserved in adjacent files as reference — this document contains only what has been decided.

> **Governance**: CEO is executive sponsor and final decision authority. Pricing Lead prepares decision materials. Cross-functional advisors (Sales, CS, Finance, Product) provide input per-milestone.

---

## Decision Log

| ID | Decision | Milestone | Date Stamped | Status |
|---|---|---|---|---|
| D-000a | Problem statements (5) defined | M0 | 2026-01-28 | **Stamped** |
| D-000b | ACV as primary success metric; lightweight guardrails | M0 | 2026-01-28 | **Stamped** |
| D-000c | CEO-accountable governance | M0 | 2026-01-28 | **Stamped** |
| D-001a | Primary segmentation: digital selling maturity (3 segments) | M1 | 2026-01-28 | **Stamped** |
| D-002a | Primary value metric: billable users | M2 | 2026-01-28 | **Stamped** |
| D-002b | No secondary value metric; feature-gating as packaging axis | M2 | 2026-01-28 | **Stamped** |
| D-002c | Expansion: metric-driven (user growth) + feature-driven (tier upgrades) | M2 | 2026-01-28 | **Stamped** |
| D-003a | Packaging model: Good/Better/Best tiers + unpublished à la carte (add-ons absorbed into T2/T3; revised 2026-03-11) | M3 | 2026-01-28 | **Stamped (v2)** |
| D-003b | Tier fences: T1 Catalog Essentials / T2 Commerce Professional / T3 Commerce Enterprise | M3 | 2026-01-28 | **Stamped** |
| D-003c | Expansion: within-tier (users) + cross-tier (upgrades) + à la carte (premium) | M3 | 2026-01-28 | **Stamped (v2)** |
| D-003d | Implementation: tiered by data readiness (Essentials included / Guided $2,500 / Comprehensive $5,000); integrations excluded | M3 | 2026-01-28 | **Stamped (v2 — 2026-03-11)** |
| D-003e | Sales Portal decomposition: Option A (Buyer Self-Serve in T2, Sales Intelligence in T3) | M3 | 2026-02-25 | **Stamped** |
| D-004a | Tier price points: T1 $749, T2 $1,295, T3 $2,295 | Phase 2B | 2026-02-25 | **Stamped** |
| D-004b | User expansion pricing: step-declining $25/$22/$20/$18; included users revised to 10/15/40 (v4 sensitivity sweep) | Phase 2B | 2026-02-25 | **Stamped** |
| D-004c | Per-brand pricing: natural-tier at 90% of book $674/$1,166/$2,066 (10% discount); 1 brand included per tier; per-brand included users (no pooling). **Consolidation-only (Path B)** — brand pricing is reactive, not applied on default migration path. Multi-org discount sunset at account level. | Phase 2B | 2026-02-25 | **Stamped (v2), revised v4/v5** |
| D-004d | À la carte premium schedule: Commerce $795, SI $995, Premium Support $495 (unpublished, response-only) | Phase 2B | 2026-02-25 | **Stamped** |
| D-003f | Data integration pricing: Self-Serve (included) / Certified Pipeline $2,500 / Managed $5,000 build + $300/mo hosting; Data Assessment $1,500 (creditable) | Phase 2B | 2026-03-11 | **Stamped** |
| D-004e | Annual vs. monthly: same rate, no discount; annual is committed term + simplified billing | Phase 2B | 2026-03-11 | **Stamped** |
| D-004f | Discounting: onboarding/services as primary lever; subscription discounting rare (CEO approval, 10% max, 12-month limit) | Phase 2B | 2026-03-11 | **Stamped** |

---

## M0: Strategic Foundation

### D-000a: Problem Statements — STAMPED 2026-01-28

The pricing refresh exists to solve five specific, interconnected problems. These are ordered by commercial surface, not priority — all five are in scope.

---

#### Problem 1: Per-user value metric is poorly executed

The per-user value metric is the right metric (confirmed via team workshop — no viable alternative). The problem is its implementation:

- **Included base is arbitrary.** The 25-user included base does not map to common customer usage patterns. Actual user counts vary widely across accounts, and the 25-user threshold creates a cliff rather than a curve.
- **No volume incentive.** Additional users are priced at a flat rate with no discount curve. The 26th user costs the same as the 200th, which removes the incentive to expand and penalizes scale.
- **Arrears billing hurts both sides.** Users are billed in arrears, which impairs SuperCat's cash flow predictability and makes customer costs unpredictable (they don't know their bill until after the month closes).

**What this means for the refresh**: Fix the user pricing mechanics (included base, discount curve, billing cadence) — do not replace the metric itself.

---

#### Problem 2: Per-module pricing does not support natural expansion or tier logic

Each module (eCat Catalog, Cart, Portal) is priced independently at a flat $395/mo with no structural relationship between them. This creates three specific issues:

- **No bundle logic.** There is no pricing signal that the full stack compounds value — a customer on iPad + Catalog sees no economic reason to add Cart beyond raw need.
- **No tier differentiation.** The flat per-module model offers no "good / better / best" progression. Every customer is on the same plan with different add-ons, which flattens the upgrade path.
- **No expansion gravity.** Without tier logic or bundle incentives, expansion is purely event-driven (customer decides they need a feature) rather than aspiration-driven (customer sees value in growing into the next tier).

**What this means for the refresh**: Design packaging that creates coherent tiers or bundles with built-in expansion incentive — not just a menu of independent modules.

---

#### Problem 3: Legacy pricing creates fairness gaps and suppresses monetization

Years of custom deals, grandfathered rates, and one-off discounts have created structural pricing inequity across the install base. Quantified evidence from the exploratory phase:

- Accounts range from **56% below book price to 42% above book price** for equivalent value delivered.
- Discount drivers include: early-adopter grandfathering (back to 2011), custom iPad base rates (as low as $350 vs. $725 book), discounted user rates ($15–$22 vs. $25 book), extra provided users (up to 100 vs. 25 standard), and bundled/free modules.
- This is not a handful of exceptions — it is the structural norm. The majority of the install base is on non-standard pricing.

**What this means for the refresh**: The new model must establish a defensible, fair price book and include a migration path that systematically corrects legacy pricing over a defined timeline.

---

#### Problem 4: Implementation fees are front-loaded and disconnected from data readiness

The current implementation fee is a fixed, upfront charge that does not account for the primary variable driving actual implementation cost: the customer's data readiness. This creates:

- **Misaligned incentives.** Customers pay the same whether their data is pristine or requires extensive cleaning and transformation.
- **Cross-subsidization.** Simple implementations subsidize complex ones, and SuperCat likely undercharges data-heavy implementations while overcharging simple ones.
- **Front-loading risk.** A large upfront fee before the customer has experienced value creates friction and buyer's remorse, particularly for smaller accounts.

**What this means for the refresh**: Implementation pricing should be variable (tiered or scoped) based on data readiness and complexity, and may benefit from a phased or milestone-based structure.

---

#### Problem 5: Support model does not contemplate revenue or client-specific support burden

Support and customer success are currently unmonetized and un-tiered, delivered uniformly regardless of account value or support consumption. This creates:

- **Invisible cross-subsidization.** High-touch accounts consume disproportionate CS/support resources with no revenue offset.
- **No scalability.** As the customer base grows, support scales as a pure cost center with no mechanism to differentiate delivery by willingness-to-pay or need.
- **No premium pathway.** Customers who would pay for enhanced support (faster SLAs, dedicated CSM, priority escalation) have no option to do so.

**What this means for the refresh**: Explore tiered support as a packaging lever (potentially as a tier differentiator or standalone add-on), and establish a framework for understanding support cost-to-serve by account.

---

### D-000b: Success Metric + Guardrails — STAMPED 2026-01-28

**Primary success metric: ACV (Average Contract Value)**

ACV is the measure of whether the pricing refresh is working. It directly reflects the economic value captured per customer relationship and is attributable to pricing and packaging decisions without being confounded by sales volume or unrelated churn dynamics.

**Lightweight guardrails** (watch, don't formally instrument):

- **Gross retention** — The refresh should not cause involuntary churn. If accounts begin churning citing pricing as the reason, that's a signal to pause and reassess migration pacing.
- **Win rate** — New-business close rates should not deteriorate as a result of the new model. If they do, the issue is likely messaging or price-point calibration, not architecture.

These are not formal KPIs with dashboards — they're "check engine lights" that would naturally surface through normal business operations.

---

### D-000c: Governance — STAMPED 2026-01-28

**CEO is fully accountable for all pricing decisions.** Cross-functional input (Sales, CS, Finance, Product) is sought per-milestone as appropriate, but decision authority is not distributed. This keeps the process fast and avoids design-by-committee dilution.

No formal RACI required at this stage. If the refresh scales to a point where delegation is needed, governance can be revisited.

---

## M1: Customer Understanding & Segmentation

> **Critical terminology (clarified 2026-01-28)**: *Active users* = accounts with a login. *Billable users* = the metric that triggers additional-user charges. These are weakly correlated (r=0.25). All user economics, discount analysis, and list_mrr calculations in this document use billable users, not active users.

### D-001a: Primary Segmentation — STAMPED 2026-01-28

**Segmentation axis: Digital Selling Maturity**

Customers and prospects are segmented by how digitally enabled their selling and commercial operation is — from digitized catalog and rep tools, through online ordering and self-serve, to fully integrated enterprise commerce. This axis is:

- **Prospect-friendly.** A company that has never heard of SuperCat can self-identify in seconds: "Are you digitizing your catalog, or are you running digital commerce?"
- **Non-judgmental.** A $200M manufacturer with a mature dealer network and trade show program has low digital selling maturity — that's an accurate description of their digital commerce posture, not a statement about their business sophistication.
- **Commercially meaningful.** The segments predict product needs, willingness-to-pay, and expansion path.

The axis maps directly to three tiers (packaging to be decided in M3) and was validated through team workshop, founder input, and quantitative analysis of the customer base and TAM universe.

#### Alternative axes evaluated and rejected

| Axis | Finding | Why Rejected |
|---|---|---|
| Industry vertical (Lighting / Furniture / Home & Décor) | Similar MRR, usage, and stack profiles across verticals | Does not predict pricing behavior, product needs, or WTP |
| Organizational scale (FIT sub-dimension) | Enterprise-scale companies have *lower* median MRR than small-scale | Counterintuitive; does not map to commercial relationship |
| Digital surface readiness (FIT sub-dimension) | No correlation with MRR, stack adoption, or usage intensity | Non-differentiating |
| Tech sophistication (ERP/PIM presence) | 95 of 104 accounts have both ERP and PIM | Table stakes in vertical; completely non-differentiating |
| Revenue band | Correlates with stack but adds no independent information | Derivative, not causal |

---

#### Segment 1: Catalog-Focused

**Tier mapping**: Catalog Essentials
**Digital selling maturity**: Early-stage
**One-liner**: Digitizing product content, pricing, and field selling tools. Buyers can browse the online product catalog, but ordering is rep-led — digital commerce is handled through traditional channels or not yet activated.

##### Profile & Firmographics

- Moving from PDF/Excel catalogs and manual order workflows to a digital catalog platform
- May range from a small emerging brand to a large, operationally sophisticated manufacturer — "Catalog-Focused" describes digital selling posture, not business maturity
- Limited integrations; lightweight IT requirements; nearly all have ERP+PIM but don't connect them to SuperCat
- Est. median employee count: ~37; est. median company revenue: ~$10M (wide range — includes Visual Comfort entities and WAC alongside smaller brands)
- Industry mix: Lighting 55%, Furniture 23%, Home & Décor 20%
- Median customer tenure: 3 years (2022 cohort); 30% are pre-2018 (long-tenured iPad-only accounts)
- Entity composition: 64% standalone, 36% rollup children (highest rollup-child ratio of any segment — several are children of large multi-brand groups)

##### Jobs to Be Done *(hypothesis — needs validation via customer interviews)*

1. **"Get our product data out of spreadsheets and into the hands of reps."** Replace PDF/Excel catalogs with a live, searchable, always-current digital catalog that reps carry on iPad.
2. **"Let buyers browse without calling us."** Provide a self-service product browsing experience for buyers — see products, pricing, availability — through the Online Product Catalog (included in T1 as a gateway to digital commerce). Many current accounts haven't activated this yet, making it a high-value enablement opportunity.
3. **"Stop the chaos of price updates."** Centralize pricing and content updates so reps always have current information and buyers never see stale data.

##### Value Driver Ranking *(hypothesis — needs validation)*

| Rank | Value Driver | Evidence |
|---|---|---|
| 1 | Catalog accuracy & freshness | Core use case; median 22k products managed per account |
| 2 | Rep productivity (field selling tools) | 100% iPad-only; median 20 logins/active user per quarter |
| 3 | Buyer browsing access (Online Product Catalog — included in T1) | Low buyer activation (median <0.1%) but large buyer base (median 14.5k customers loaded) — gateway to digital commerce |
| 4 | Content management simplicity | Median 22k products; frequent pricing/seasonal updates |
| 5 | Speed to value / ease of go-live | Price-sensitive segment; needs ROI quickly |

##### Behavior & Value Derived

- **Usage**: Median 22k products, 20 active users, 24 orders/quarter, $153k GMV/quarter
- **Channel split**: 100% iPad orders (no eOL — they don't have online ordering modules)
- **Engagement**: Median 366 total logins/quarter, 20 logins per active user — consistent but not heavy
- **Buyer activation**: Median 2 customers ordering per quarter out of 14.5k loaded — very low buyer-side commerce activity, consistent with catalog/browse use case
- **Value derived**: Median $480 GMV per $1 MRR (annualized). Even without commerce modules, some accounts drive significant transaction volume through iPad orders (e.g., Dainolite: 3,267 orders; Uniware: 3,763 orders)
- **Wide variance**: Segment includes both single-user $366/mo accounts AND WAC (332k products, 83 users, 1,283 orders) — the segment is defined by what they use SuperCat for, not by their scale

##### Representative Accounts

| Account | MRR | Products | Orders (Q4) | Users | Why representative |
|---|---|---|---|---|---|
| WAC/Modern Forms | $1,842 | 331,977 | 1,283 | 83 | Large, sophisticated — uses SuperCat for catalog only |
| Visual Comfort Signature | $1,538 | 96,206 | 314 | 45 | Major brand; catalog-focused despite scale |
| Hooker Furnishings | $864 | 36,815 | 199 | 26 | Mid-market furniture; traditional commerce channels |
| Accord Lighting | $1,077 | 6,876 | 24 | 40 | Typical mid-tier; moderate usage |
| Troy Lighting | $366 | 21,649 | 1 | 43 | Deeply discounted rollup child; minimal ordering |

##### Baseline Economics

| Metric | Value |
|---|---|
| Accounts | 56 (54% of base) |
| Total MRR | $51,563 (35% of total) |
| Total ARR | $618,756 |
| Mean / Median MRR | $921 / $778 |
| P25–P75 MRR | $690–$1,141 |
| MRR split | Platform $39,079 (76%) / Users $12,484 (24%) |
| Avg provided users | 25 (standard) |
| Avg additional users (billable) | ~10 |
| Avg effective user rate | ~$21 (vs. $25 book) |

> **Note on user metrics**: "Additional users" throughout this document refers to *billable* users — the metric that triggers additional-user charges — not *active* users (logins). These are weakly correlated (r=0.25); many accounts have significantly more logins than billable users. All discount analysis uses billable-user-based decomposition.

##### Discount Position & Correction Headroom *(corrected per Angie audit + billable-user decomposition — v3)*

| Metric | Value |
|---|---|
| Mean discount vs. book | +6.9% |
| Median discount vs. book | +1.9% |
| At or above book | 27 accounts (48%) |
| Slight discount (1–15%) | 17 accounts (30%) |
| Meaningful discount (15–30%) | 5 accounts (9%) |
| Steep discount (>30%) | 7 accounts (12%) |
| Total MRR gap to book | $6,063/mo ($72,751/yr) |
| ↳ Platform gap | $4,129/mo ($49,547/yr) |
| ↳ User gap | $2,499/mo ($29,988/yr) |
| Avg gap per below-book account | $209/mo (29 accounts) |

This segment has the **largest aggregate correction headroom** of any segment ($73k/yr) despite individual gaps being modest. The volume of accounts (29 below book) drives the total. The gap is **~2:1 platform vs. users** — most of the correction opportunity is in iPad base and module discounts, not user rates.

##### Expansion Path

- **Tier upgrade (T1 → T2)**: Primary expansion lever. 100% of this segment is a candidate for Commerce Professional — adding online ordering (B2B Cart), buyer self-service (Order & Invoice Tracking), and authenticated buyer access. Online Product Catalog is already included in T1 as the gateway; activating it and demonstrating buyer engagement is the natural path toward T2 adoption.
- **User expansion**: Low current additional-user counts (avg 10 billable) with room to grow as digital selling adoption deepens.
- **Price correction**: 29 accounts (52%) are below book — modest per-account gaps ($209/mo avg) but the largest aggregate headroom of any segment ($73k/yr). Correction is primarily on the platform side (iPad base and module discounts).
- **CPQ/PCI upsell**: CPQ and Credit Card/PCI are available as unpublished à la carte options for T1 accounts, though lower adoption likelihood at T1 given catalog-only use case. For accounts that do need CPQ, the T1→T2 upgrade narrative is strong ("upgrade and get CPQ included plus commerce capabilities").

##### Price Sensitivity Posture *(hypothesis — needs validation)*

- **Moderate sensitivity**. This segment includes the most price-diverse accounts (ranging from deeply discounted rollup children to above-book accounts on configurable iPad). Newer cohorts (post-2020) are closer to book rate; legacy accounts have more correction to absorb.
- **Key risk**: Accounts using SuperCat for a narrow capability (catalog + browse only) may perceive less value anchor than commerce-active accounts — price increases without corresponding value expansion could trigger "do I still need this?" evaluations. The Online Product Catalog gateway in T1 is designed to strengthen this value anchor before the T2 upgrade conversation.
- **Competitive alternatives**: Highest alternative availability. PDF catalogs, basic product database tools, Shopify-powered B2B catalogs, and manual processes are all viable substitutes for the catalog-only use case. Switching cost is moderate.

---

#### Segment 2: Commerce-Active

**Tier mapping**: Commerce Professional
**Digital selling maturity**: Mid-stage
**One-liner**: Running digital ordering and/or self-serve buyer channels through SuperCat alongside field sales tools. Buyer self-service (order tracking, invoices) and operational workflow management are active needs — full sales analytics is an emerging aspiration addressed in T3.

##### Profile & Firmographics

- Multi-line distributors or growing manufacturers with increasing channel complexity
- Clear seasonality and workflow peaks; need predictable platform capacity
- Integrations becoming important but not yet mission-critical — data pipelines, ERP sync are active or planned
- Est. median employee count: ~44; est. median company revenue: ~$10M
- Industry mix: Furniture 43%, Lighting 40%, Home & Décor 13% (most balanced mix)
- Median customer tenure: 7 years (2018 cohort); 53% are pre-2018 — most tenured segment proportionally
- Entity composition: 83% standalone, 17% rollup children (lowest rollup-child ratio — these are mostly independent operators)

##### Jobs to Be Done *(hypothesis — needs validation via customer interviews)*

1. **"Let our buyers order without calling a rep."** Enable self-serve ordering through online channels so buyers can browse, build orders, and submit 24/7 — reducing rep burden and manual order processing.
2. **"Give reps better tools to sell more."** Equip field sales with digital ordering on iPad alongside catalog tools — faster order capture, fewer errors, real-time pricing.
3. **"Know the status of every order and keep buyers informed."** Give buyers and reps real-time visibility into order status, invoices, and shipment tracking (Order & Invoice Tracking, included in T2) — eliminating "where's my order?" calls and manual lookups. *(Note: full sales analytics — dashboards, territory views, pipeline reporting — is a T3 capability; this JTBD addresses the operational self-serve layer, not the analytical layer.)*
4. **"Handle our busy season without breaking."** Manage seasonal order spikes (market weeks, trade shows, fiscal year-end pushes) without manual workarounds or system strain.

##### Value Driver Ranking *(hypothesis — needs validation)*

| Rank | Value Driver | Evidence | Tier mapping |
|---|---|---|---|
| 1 | Ordering efficiency (rep + self-serve) | Median 416 orders/quarter across mixed channels | T2 core |
| 2 | Buyer self-service (order tracking, invoices) | Median 34 customers ordering per quarter; growing buyer activation — need to keep buyers informed without manual effort | T2 (Order & Invoice Tracking) |
| 3 | Rep productivity | 50 median active users; 32 logins/user — high engagement | T1 base |
| 4 | Operational management & workflow | Multi-module stack; managers need to manage orders and buyer relationships across channels | T2 operational |
| 5 | Seasonal capacity & predictability | Industry-driven seasonality; Q4 is peak for many | T2 operational |
| 6 | Integration readiness | ERP/PIM integration emerging as active need | T2/T3 |
| — | *Sales analytics & reporting (upgrade trigger)* | *Cross-channel dashboards, pipeline views, territory reporting — emerging need for accounts maturing toward T3* | *T3 upgrade path* |

##### Behavior & Value Derived

- **Usage**: Median 26k products, 50 active users, 416 orders/quarter, $1.3M GMV/quarter
- **Channel split**: 96% iPad orders / 4% eOL orders — digital commerce is emerging but iPad/rep-led selling still dominates
- **Engagement**: Median 1,034 total logins/quarter, 32 logins per active user — significantly higher engagement intensity than Catalog-Focused (2.8x logins, 1.6x per-user)
- **Buyer activation**: Median 34 customers ordering per quarter out of 42.5k loaded — 17x higher than Catalog-Focused, reflecting active commerce
- **Value derived**: Median $852 GMV per $1 MRR (annualized). Segment generates $161M total GMV on $53k MRR — strong value-to-price ratio
- **Stack diversity**: 47% on iPad+Catalog+Portal (closest to T3 readiness), 33% on iPad+Catalog+Cart (T2-aligned), 20% on iPad+Catalog (closest to T1, candidates for T2 upgrade). 67% missing Cart and 53% missing Portal — meaningful upsell surface within the segment, now expressed as tier completion rather than module add-ons

##### Representative Accounts

| Account | MRR | Products | Orders (Q4) | Users | Why representative |
|---|---|---|---|---|---|
| Palecek | $3,251 | 22,543 | 2,733 | 107 | High-order-volume catalog-only; top of segment |
| Hubbardton Forge | $3,025 | 11,432 | 1,580 | 185 | Full Portal user; high rep count |
| Crystorama | $2,540 | 11,483 | 122 | 36 | Above-book pricing (100 provided users); premium deal |
| Craftmade | $2,395 | 27,927 | 201 | 80 | Typical mid-tier Commerce-Active |
| Sabine Pools | $580 | 113,587 | 137 | 6 | Unusual profile: massive catalog, minimal users |

##### Baseline Economics

| Metric | Value |
|---|---|
| Accounts | 28 (27% of base) |
| Total MRR | $51,208 (34% of total) |
| Total ARR | $614,499 |
| Mean / Median MRR | $1,829 / $1,822 |
| P25–P75 MRR | $1,387–$2,209 |
| MRR split | Platform $38,632 (75%) / Users $12,576 (25%) |
| Avg provided users | ~28 (slightly above standard 25) |
| Avg additional users (billable) | ~22 |
| Avg effective user rate | ~$18 (vs. $25 book) |

##### Discount Position & Correction Headroom *(corrected per Angie audit + billable-user decomposition — v3)*

| Metric | Value |
|---|---|
| Mean discount vs. book | +2.9% |
| Median discount vs. book | +1.0% |
| At or above book | 11 accounts (39%) |
| Slight discount (1–15%) | 12 accounts (43%) |
| Meaningful discount (15–30%) | 3 accounts (11%) |
| Steep discount (>30%) | 2 accounts (7%) |
| Total MRR gap to book | $4,054/mo ($48,648/yr) |
| ↳ Platform gap | $2,495/mo ($29,941/yr) |
| ↳ User gap | $4,116/mo ($49,392/yr) |
| Avg gap per below-book account | $238/mo (17 accounts) |

This segment has the **highest user-rate correction opportunity** of any segment ($49k/yr in user gaps alone) — driven by the combination of high additional-user counts (avg 22 billable) and the lowest effective rate ($18/user vs. $25 book). Platform gap is secondary. A user discount curve fix (Problem 1) has the largest absolute impact in this segment.

##### Expansion Path

- **Within-tier completion (T2)**: ~67% missing B2B Cart and ~53% missing Order & Invoice Tracking — substantial intra-tier activation opportunity. Natural motion: accounts add online ordering and buyer self-serve as their commerce activity grows.
- **Tier upgrade (T2 → T3)**: The 47% already on full stack (iPad+Catalog+Portal) are natural T3 candidates — adding Sales Intelligence (dashboards, territory views, analytics) and expanded included users (15→40). The T2→T3 upgrade trigger is when operational management gives way to strategic visibility needs.
- **User expansion**: Highest additional-user counts (avg 22 billable) and growing engagement create natural user-seat expansion. Discount curve improvements would accelerate this — this segment's user gap alone ($49k/yr) exceeds most segments' total gaps.
- **Brand expansion**: As multi-brand accounts in this segment grow, additional brands at $895/mo per brand (T2 rate) become an expansion lever.
- **Price correction**: 17 accounts (61%) below book — moderate per-account gaps ($238/mo avg), $49k/yr aggregate. The correction is **user-rate-led**, not platform-led.
- **Commerce deepening**: As buyer activation grows, order volume and GMV will increase — this is the segment most likely to organically evolve toward Platform-Embedded (T3).

##### Price Sensitivity Posture *(hypothesis — needs validation)*

- **Moderate-to-low sensitivity**. These accounts derive clear, measurable operational value from SuperCat (ordering efficiency, rep tools, buyer self-service). The value anchor is stronger than Catalog-Focused because SuperCat is embedded in daily ordering workflows, not just content management. The T2 value proposition — "your buyers can check orders and invoices themselves" — is concrete and immediately demonstrable.
- **Key risk**: Accounts early in the Commerce-Active journey (iPad+Catalog only, low order volume) may feel more like Catalog-Focused in terms of price sensitivity. The 53% pre-2018 tenure cohort has high relationship equity but also the most legacy pricing to correct. Additionally, the T2/T3 boundary (Order & Invoice Tracking vs. Sales Intelligence) needs clear communication — accounts that associate "visibility" generically with SuperCat may expect analytics in T2.
- **Competitive alternatives**: Moderate. Full B2B commerce platforms (BigCommerce B2B, Shopify B2B, NuOrder) exist but switching cost is higher — they'd lose embedded workflows, rep adoption, and buyer relationships. SuperCat's vertical specialization in furniture/lighting is a meaningful moat here.

---

#### Segment 3: Platform-Embedded

**Tier mapping**: Commerce Enterprise
**Digital selling maturity**: Advanced
**One-liner**: SuperCat is core commerce infrastructure — governing multi-channel ordering, buyer self-service, integrations, and operational analytics at scale.

##### Profile & Firmographics

- National distributors or major manufacturers; many brands/collections; heavy governance requirements
- Integrations and data pipelines are mission-critical — ERP, PIM, DAM connections are live and actively managed
- Cross-functional buying committees; procurement may be involved
- Est. median employee count: ~40; est. median company revenue: ~$10M (note: enrichment estimates likely understate for several of these accounts)
- Industry mix: Lighting 57%, Furniture 33%, Generic B2B 5%
- Median customer tenure: 8 years (2017 cohort); 57% are pre-2018 — longest-tenured segment
- Entity composition: 71% standalone, 29% rollup children

##### Jobs to Be Done *(hypothesis — needs validation via customer interviews)*

1. **"Run our entire B2B commerce operation on one platform."** SuperCat is the system of record for rep-led and self-serve ordering, buyer management, pricing governance, and operational reporting. It's not a tool — it's infrastructure.
2. **"See the full picture across our sales channels."** Gain strategic visibility into order volume, rep activity, buyer engagement, territory performance, and pipeline — through Sales Intelligence dashboards and analytics (T3 exclusive). *(Note: the operational self-serve layer — order tracking, invoices, buyer account management — is T2. This JTBD addresses the analytical / management intelligence layer on top.)*
3. **"Maintain control as we scale."** Governance at scale: user permissions, pricing rules, order approval workflows, territory management, and audit trails. As the operation grows, control cannot degrade.
4. **"Connect our systems so data flows without manual intervention."** ERP/PIM/DAM integrations that keep product data, inventory, pricing, and order data synchronized across the tech stack.
5. **"Give our buyers a world-class self-serve experience."** Buyers can browse, order, track shipments, check invoices, and manage their accounts independently — at the quality level they expect from consumer e-commerce. *(The buyer-facing capabilities are largely T2; T3 adds management-side visibility into how buyers are using those capabilities.)*

##### Value Driver Ranking *(hypothesis — needs validation)*

| Rank | Value Driver | Evidence |
|---|---|---|
| 1 | Multi-channel commerce (rep + self-serve) | 51% eOL orders — only segment with meaningful online ordering |
| 2 | Reliability & uptime | Infrastructure-grade dependency; any outage = lost revenue |
| 3 | Buyer self-service at scale | Median 208 customers ordering/quarter; $8.2M GMV/quarter |
| 4 | Sales Intelligence & analytics (T3 exclusive) | 136 median active users; managers need enterprise-grade dashboards, territory views, pipeline reporting |
| 5 | Governance & control | User management, pricing rules, approval workflows at scale |
| 6 | Integration stability | ERP/PIM pipelines are live; data integrity is mission-critical |
| 7 | Support responsiveness | High operational dependency → low tolerance for unresolved issues |

##### Behavior & Value Derived

- **Usage**: Median 40k products, 136 active users, 2,327 orders/quarter, $8.2M GMV/quarter
- **Channel split**: 49% iPad orders / 51% eOL orders — the only segment where digital self-serve ordering has reached parity with rep-led selling. This is the defining behavioral marker of Platform-Embedded.
- **Engagement**: Median 1,613 total logins/quarter, 37 logins per active user — highest absolute engagement; comparable per-user intensity to Commerce-Active
- **Buyer activation**: Median 208 customers ordering per quarter out of 37.4k loaded — 104x higher than Catalog-Focused, 6x higher than Commerce-Active
- **Value derived**: Median $2,561 GMV per $1 MRR (annualized). Segment generates **$768M total GMV on $47k MRR** — the value-to-price ratio is extraordinary. For every dollar these accounts pay SuperCat monthly, they process ~$2,561 in commerce annually. This is the strongest quantitative argument for price correction in the install base.
- **Tight MRR clustering**: P25–P75 is $2,022–$2,338 — remarkably narrow. Despite massive variance in usage and GMV (Summer Classics: $467M GMV; Kalco: $174 orders), most accounts pay within a $316/mo band. This reflects legacy pricing compression, not equivalent value.

##### Representative Accounts

| Account | MRR | Products | Orders (Q4) | Users | GMV (Q4) | Why representative |
|---|---|---|---|---|---|---|
| Summer Classics Retail | $3,232 | 11,371 | 20,772 | 74 | $466.5M | Highest order volume; massive GMV |
| Jamie Young Company | $2,950 | 19,949 | 8,201 | 211 | $25.7M | High user count; strong engagement |
| Wildwood/Chelsea House | $3,362 | 19,050 | 5,842 | 84 | $6.7M | Top MRR; above-book pricing |
| Currey & Company | $2,173 | 15,503 | 3,116 | 102 | $11.7M | Median MRR; typical Platform-Embedded |
|?"?"  Lighting | $2,338 | 39,574 | 2,327 | 136 | $8.2M | Archetypal full-stack operator |

##### Baseline Economics

| Metric | Value |
|---|---|
| Accounts | 20 (19% of base) |
| Total MRR | $45,827 (31% of total) |
| Total ARR | $549,926 |
| Mean / Median MRR | $2,291 / $2,173 |
| P25–P75 MRR | $2,025–$2,359 |
| MRR split | Platform $36,234 (79%) / Users $9,593 (21%) |
| Avg provided users | ~25 |
| Avg additional users (billable) | ~24 |
| Avg effective user rate | ~$20 (vs. $25 book) |

##### Discount Position & Correction Headroom *(corrected per Angie audit + billable-user decomposition — v3)*

| Metric | Value |
|---|---|
| Mean discount vs. book | +2.6% |
| Median discount vs. book | -1.3% (majority are AT or ABOVE book) |
| At or above book | 12 accounts (60%) |
| Slight discount (1–15%) | 6 accounts (30%) |
| Meaningful discount (15–30%) | 2 accounts (10%) |
| Steep discount (>30%) | 0 accounts (0%) |
| Total MRR gap to book | $3,021/mo ($36,255/yr) |
| ↳ Platform gap | $1,278/mo ($15,332/yr) |
| ↳ User gap | $2,412/mo ($28,944/yr) |
| Avg gap per below-book account | $378/mo (8 accounts) |

**Major correction from v2**: This segment was previously identified as the largest correction opportunity ($77k/yr). After Angie's audit — which revealed that many "above book" appearances were actually standard pricing with bundled users, add-on products (CPQ, Closed Site), and corrected module rates ($295 Cart vs. our assumed $395) — the gap dropped to $36k/yr. **60% of Platform-Embedded accounts are actually at or above book rate.** The decomposition reveals the remaining gap is **~2:1 user vs. platform** — the story here is discounted per-user rates ($20 effective vs. $25 book across 24 avg billable users), not platform fee discounts.

The GMV-to-MRR ratio remains extraordinary: $768M GMV on $46k MRR means SuperCat captures roughly **0.07% of the commerce value it enables**.

##### Expansion Path

- **Tier-level position**: 100% are already full-stack users (Cart + Portal) — they are natural T3 customers. Expansion is vertical (deeper feature adoption, Sales Intelligence activation) rather than horizontal (tier upgrades). The T3 value proposition — analytics dashboards, territory reporting, priority support, dedicated CSM, CPQ and PCI included — aligns directly with this segment's scale and operational complexity.
- **Brand expansion**: Many Platform-Embedded accounts operate multiple trade names (e.g., Generation Brands with 3 Visual Comfort instances). Brand pricing at 90% of natural tier ($674/$1,166/$2,066 per brand) is available as a reactive consolidation option — see D-004c. Consolidation is not incentivized (2-6% savings range).
- **User expansion**: Highest billable-user counts (avg 24) with high active user counts (median 136). User pricing mechanics improvements have the largest absolute revenue impact here — the user gap ($29k/yr) is nearly double the platform gap ($15k/yr).
- **Price correction**: Only 8 accounts (40%) are below book — the lowest percentage of any segment. But per-account gaps are the largest ($378/mo), and the value justification for correction is strongest given the extraordinary GMV-to-MRR ratio.
- **Services & support monetization**: This segment is the natural buyer for managed integrations, premium support SLAs, executive business reviews, and advanced analytics — all currently un-monetized or under-monetized surfaces. This is the primary revenue expansion lever for Platform-Embedded, not price correction.

##### Price Sensitivity Posture *(hypothesis — needs validation)*

- **Low sensitivity (highest value anchor)**. SuperCat is infrastructure. The switching cost is substantial: re-training hundreds of users, migrating buyer relationships, rebuilding integrations, and disrupting live commerce operations. These accounts cannot easily leave.
- **Key risk**: Not churn, but resentment. These are the longest-tenured, most committed customers. They've been loyal for 8+ years. A ham-fisted price increase — even a justified one — risks damaging the relationship and creating vocal detractors. Migration must be framed around value, with advance notice and respect for tenure.
- **Competitive alternatives**: Lowest. No off-the-shelf competitor replicates the vertical specialization + embedded workflow combination for furniture/lighting B2B. Enterprise B2B platforms (SAP Commerce, Salesforce Commerce Cloud) exist but are dramatically more expensive and not vertically specialized. The real competitive risk is not a platform switch but a decision to build internally.

---

#### Cross-Segment Summary

| Dimension | Catalog-Focused | Commerce-Active | Platform-Embedded |
|---|---|---|---|
| Accounts | 56 (54%) | 28 (27%) | 20 (19%) |
| Total MRR / % of total | $51,563 (35%) | $51,208 (34%) | $45,827 (31%) |
| Median MRR | $778 | $1,822 | $2,173 |
| Avg billable addl users | ~10 | ~22 | ~24 |
| Avg effective user rate | ~$21 | ~$18 | ~$20 |
| Median orders/quarter | 24 | 416 | 2,327 |
| GMV per $1 MRR (med) | ~$480 | ~$852 | ~$2,561 |
| Total segment GMV (Q4) | ~$82M | ~$161M | ~$768M |
| eOL order share | 0% | ~4% | ~51% |
| Buyer activation (med) | 2 | 34 | 208 |
| Median tenure (cohort) | 2022 | 2018 | 2017 |
| % below book *(v3)* | 52% | 61% | 40% |
| Correction headroom/yr *(v3)* | **$73k** | $49k | $36k |
| ↳ Platform gap/yr | $50k | $30k | $15k |
| ↳ User gap/yr | $30k | **$49k** | $29k |
| Competitive alternatives | Highest | Moderate | Lowest |
| Primary expansion lever | Tier upgrade (T1→T2) + platform correction | Within-tier completion + user rate correction + T2→T3 upgrades | Brand expansion + services + user mechanics |

---

#### Segment → Tier Crosswalk *(added 2026-02-25, per Phase 2B Exercise 1)*

M1 segments describe **behavioral maturity** (what the customer *does*). Tier assignments describe **commercial position** (what the customer *pays for*). These are intentionally different lenses, and they do not map 1:1:

| | M1 Segment (behavioral) | Natural Tier (by module) | Delta |
|---|:---:|:---:|---|
| Catalog-Focused / T1 | 56 | 61 | +5 accounts are modularly T1 but behaviorally Commerce-Active |
| Commerce-Active / T2 | 28 | 9 | -19 accounts are behaviorally T2 but modularly T1 or T3 |
| Platform-Embedded / T3 | 20 | 34 | +14 accounts have Portal (T3 module) but were behaviorally classified as Commerce-Active |

**Why the gap exists**: M1 segments cluster on behavioral signals (order volume, channel mix, buyer activation, engagement intensity). Tier assignment maps on module presence (what's in the contract). An account can be behaviorally Commerce-Active — high order volume, growing buyer engagement — while still on an iPad-only contract (no commerce modules purchased).

**Why the gap is commercially valuable**: The ~19 accounts that are behaviorally Commerce-Active but modularly T1 are the **highest-conversion T1→T2 upgrade targets**. They already behave like T2 customers but haven't bought T2 capabilities. This is the primary T1→T2 upgrade pipeline for Sales.

**Why we preserve both frameworks**: Segments inform *how we talk to customers* (JTBD, value drivers, messaging). Tiers inform *what they pay* (price points, included capacity, feature gates). Collapsing them would lose the upgrade-opportunity signal.

> **Source**: `11_synthesis/2026-02-25__install_base_tier_mapping_wtp__d004a_exercise1__v1.md`

---

#### TAM Perspective

The 4,651-prospect TAM universe supports this segmentation:
- ~81% have low-to-medium digital surface readiness (0–75) — natural Catalog-Focused and Commerce-Active prospects
- ~19% have high digital readiness (76–100) — potential Commerce-Active or Platform-Embedded prospects
- Industry mix skews Furniture (68%) vs. Lighting (17%), inverted from the current customer base — the segmentation generalizes across verticals
- "Are you digitizing your catalog or running digital commerce?" is a first-call qualification question that maps directly to segment and tier

---

#### M1 Open Items — Validation Required *(carried forward to Phase 2)*

The segment profiles above are grounded in quantitative data where available and clearly labeled hypotheses where not. M3 was stamped with these items open; they are now addressed in Phase 2, Workstream A (Customer Validation) and Workstream B (Price Point Modeling). The JTBD and value driver hypotheses above have been updated to align with the M3 packaging architecture (tier fences, portal decomposition, brand expansion) — concept testing will validate or revise them.

| Gap | What's missing | Recommended exercise | Where addressed |
|---|---|---|---|
| Jobs to be Done validation | JTBD are hypothesized from usage data, not confirmed by customers | 10–15 structured JTBD interviews per segment (30–45 total) | Phase 2, Workstream A (concept testing + validation artifact) |
| Value driver ranking validation | Rankings are inferred from behavior, not force-ranked by customers | MaxDiff survey (100+ responses) or direct ranking in interviews | Phase 2, Workstream A |
| Retention & expansion history | No historical MRR data to calculate actual NRR, churn, or expansion rates by segment | Pull 12–24 months of MRR history from billing system; calculate segment-level retention and expansion | Phase 2, Workstream B (price point modeling) + Workstream C (operational readiness) |

Additional inputs that would strengthen the profiles (lower priority):
- **Support burden by segment**: CS/support ticket volume and resolution time per account, if available from support tooling
- **Competitive loss analysis**: Historical win/loss reasons from CRM, segmented by digital selling maturity
- **Buyer journey mapping**: Sales cycle length, stakeholder count, and common objections per segment from Sales team interviews

---

## M2: Value Metric Selection

### D-002a: Primary Value Metric — STAMPED 2026-01-28

**Primary value metric: Billable users**

Billable users — the metric that triggers additional-user charges — is the primary value metric. This decision was reached through systematic elimination of alternatives, not by defaulting to the status quo.

#### Methodology note: circularity correction

The initial correlation analysis showed billable users with r(MRR) = +0.713 — apparently the strongest candidate by a wide margin. However, this was **partly mechanical**: billable users is a direct input to MRR (MRR = platform_fee + users × rate), so the correlation overstates true value alignment. When user charges are stripped out and billable users is correlated against platform-fee-only MRR, the correlation drops to +0.337 overall, and is near-zero or negative within Catalog-Focused (-0.095) and Platform-Embedded (-0.275). This circularity was identified and corrected before stamping.

#### Why billable users — the honest case

Billable users is not chosen because the data proves it is perfectly aligned with value. It is chosen because:

1. **Every alternative has disqualifying flaws**:

| Candidate | r(MRR) | Disqualifier |
|---|---|---|
| SKU Count | +0.088 | Near-zero correlation with everything; ICP avg is 3.5k but range is 0–428k; iPad performance ceiling at ~20k; would incentivize pursuit of high-SKU segments that are not the core ICP; definitional ambiguity (published vs. active vs. loaded); negative correlation with MRR in Commerce-Active segment |
| Orders | +0.486 | SuperCat does not own the order surface outright (orders are processed via ERP); gameable via "quotes"; 113x variance between segment medians (24 → 2,662) makes standardized banding impossible; includes zero-order accounts; bypassable |
| GMV | +0.197 | "Success tax" perception; 72x variance between segment medians ($121k → $8.7M); 4.8x coefficient of variation; unpredictable month-to-month; triggers "why do you need to know my revenue?" resistance |
| Buyer Accounts | +0.439 | Not under customer control; 127x P10/P90 ratio; definitionally ambiguous (active vs. loaded vs. ordered); not a metric customers naturally track |
| Platform Fee (flat) | n/a | No expansion engine; zero natural revenue growth; only grows through price increases or tier upgrades |

2. **Billable users wins on simplicity and growth** — the two dimensions that matter most for a value metric that must survive first contact with customers and Sales:
   - **Simplicity (5/5)**: "You have X users, each costs $Y." Every B2B SaaS buyer understands this instantly. No counting exercise, no definitional debates.
   - **Growth (4/5)**: As companies digitize more of their selling, they add more reps, buyers, and internal users. 58% of accounts are already expanding on this axis, generating $416k/yr (23% of total MRR).

3. **The known weaknesses are execution problems, not evidence the metric is wrong**:
   - "Seat anxiety" and login sharing → solvable with a more generous included base and discount curve (M3/M4)
   - Flat per-user rate with no volume incentive → solvable with tiered or declining user pricing (M4)
   - Arrears billing → solvable with committed user blocks or prepaid models (M4)
   - These map directly to Problem 1 in the Constitution.

4. **Correlation with non-billing outcomes** confirms genuine (if moderate) alignment: billable users correlates with GMV (+0.680 log), orders (+0.625 log), and active users (+0.687 log) — outcomes that have no mechanical relationship to the billing formula.

#### Candidates evaluated (full scorecard)

| Candidate | Alignment | Simplicity | Growth | Total (15) | r(MRR) | r(Platform only) | Disposition |
|---|---|---|---|---|---|---|---|
| **Billable Users** | 4 | **5** | **4** | **13** | +0.713* | +0.337 | **Selected** |
| Orders | 3 | 3 | 3 | 9 | +0.486 | +0.454 | Eliminated — not owned, gameable, extreme variance |
| GMV | 3 | 2 | 3 | 8 | +0.197 | +0.170 | Eliminated — success tax, extreme variance |
| Buyer Accounts | 2 | 2 | 3 | 7 | +0.439 | +0.258 | Eliminated — not under customer control, ambiguous |
| Platform Fee | 1 | 5 | 1 | 7 | n/a | n/a | Eliminated — no expansion engine |
| SKU Count | 2 | 2 | 2 | 6 | +0.088 | -0.026 | Eliminated — near-zero alignment, ICP distortion |

*\*Includes mechanical inflation from user charges being a component of MRR. The circularity-corrected correlation (platform fee only) is +0.337.*

#### Input sources

- Quantitative: 104-account master data (v3), billable-user-based decomposition, correlation analysis with circularity correction
- Qualitative: Team workshop (2026-02-06), CEO observations on SKU/Order/GMV viability
- Framework: Campbell three-criteria scoring (Alignment, Simplicity, Growth)

---

### D-002b: Secondary / Hybrid Metric — STAMPED 2026-01-28

**No secondary value metric. Feature-gating serves as the packaging axis.**

Feature-gating (which modules/capabilities are included) determines tier selection. It is a packaging mechanism, not a metered value metric. This means:

- **Tier selection** = which capabilities you need (feature-gated) → determines platform fee
- **Expansion within tier** = how many users you need (billable users) → drives usage-based revenue

These are complementary, not competing. Adding a second metered axis (e.g., orders or SKUs alongside users) would add complexity without proportional value capture, and every candidate for a second axis has the same disqualifying flaws that prevented it from being the primary metric.

---

### D-002c: Expansion Mechanism — STAMPED 2026-01-28

**Expansion is both metric-driven and feature-driven.**

Revenue expansion happens through two distinct channels:

1. **Within-tier (metric-driven)**: User and brand growth as the customer's digital selling organization expands. This is organic, predictable, and already proven (58% of accounts, $416k/yr on users alone).
2. **Cross-tier (feature-driven)**: Tier upgrades as digital selling maturity increases. The customer moves from Catalog Essentials (T1) to Commerce Professional (T2) to Commerce Enterprise (T3) by unlocking capabilities — not by consuming more of the same resource. *(M3 codified this as T1→T2→T3 progression with Online Product Catalog as the T1 gateway.)*

Both channels are already present in the current model. M3 established the tier structure and fences; Phase 2, Workstream B (Price Points) will set the specific rates and discount mechanics.

---

### M2 Open Items — Status Update

The value metric decision deferred four mechanics questions. M3 resolved two; the remainder carries forward to Phase 2:

| Item | Question | Status | Resolution |
|---|---|---|---|
| Included user base | How many users are included per tier? (Current: 25 for all) | **Resolved in M3, revised v4** | T1: 10, T2: 15, T3: 40 included users (revised from 15/25/50 per v4 sensitivity sweep) |
| Included brand base | How many brands are included per tier? | **Resolved in M3; revised in D-004c v2** | 1 brand included per tier (all tiers). Revised from 1/3/5 — see D-004c v2 rationale. |
| User discount curve | Flat rate vs. volume/declining pricing | **Resolved in D-004b** | Step-declining: $25/$22/$20/$18 per excess user (1–10/11–25/26–50/51+) |
| Billing cadence | Arrears vs. prepaid vs. committed blocks | **Deferred** | Committed floor model validated as superior to arrears and blocks; deferred to subsequent iteration. Existing annual arrangements already operate a committed floor model (declared estimate + quarterly reconciliation). See D-004b stress test (2026-01-28). |
| Billable user definition | Current definition vs. refinement | Stable | No change required — current definition carries forward |

---

## M3: Packaging Architecture

> **Inputs**: Product capability map (code- and database-verified, 27 capabilities across 5 surfaces), competitive packaging audit (AmpTab, Pepperi, WizCommerce, MarketTime, RepZio), Feature-Value Matrix, segment profiles (M1), value metric (M2).
>
> **Reference document**: `11_synthesis/2026-01-28__m3_packaging_architecture__v1.md`

### D-003a: Packaging Model — STAMPED 2026-01-28

**Good/Better/Best tiers + unpublished à la carte modules.**

> **Revised 2026-03-11**: CPQ and Credit Card/PCI absorbed into T2 and T3 (preserved as unpublished à la carte for T1 only). FlipBook / Interactive PDFs removed from pricing material. Named add-ons section eliminated — all modularity now expressed through tiers or the unpublished à la carte shelf.

Three tiers mapped to the three digital selling maturity segments from M1:

| Tier | Name | Target Segment | Positioning |
|------|------|---------------|-------------|
| **T1** | **Catalog Essentials** | Catalog-Focused | Digitize your product content and field sales |
| **T2** | **Commerce Professional** | Commerce-Active | Enable digital commerce across rep and buyer channels |
| **T3** | **Commerce Enterprise** | Platform-Embedded | Run your entire B2B commerce operation |

Tiers were selected over modular or pure hybrid based on seven factors (competitive alignment, segment fit, GTM clarity, expansion path, revenue capture, Problem 2 resolution, M2 compatibility) — tiers scored higher on all seven. See packaging architecture reference for the full comparison.

The architecture accommodates one form of modularity:

1. **À la carte modules at a documented premium**: Tier-included capabilities sold individually for prospects with overlapping established digital sales capabilities, or niche capabilities (CPQ, Credit Card/PCI) offered to T1 accounts that need them without a full tier upgrade. NOT published, NOT promoted by Sales — a response mechanism. See D-004d for pricing and tier-push economics.

---

### D-003b: Tier Fences — STAMPED 2026-01-28

#### T1: Catalog Essentials

- eCat iPad App (catalog + ordering + sync)
- Admin Console (full catalog/user/order management)
- **eCat Online Catalog (buyer-facing browse)** — included as a "gateway drug" per founder input; easy to turn on, creates natural pull toward T2
- Camera/barcode scanning, smart stacks & user lists, library/documents
- Product reports & tearsheets
- Multi-price-level support, inventory display
- Customer favorites / sales data
- FTP data import + ERP order export
- Standard support
- 15 included users (draft — to be refined in M4)

#### T2: Commerce Professional (Hero Tier)

Everything in T1, plus:

- **B2B Cart** (buyer-facing ordering + checkout)
- **Closed Site** (authenticated access)
- **Self-service enrollment**
- **Contract pricing**
- **Gridview ordering**
- **Address verification**
- **Order & Invoice Tracking** (order status, invoice lookup, customer dashboard, basic customer views) — per D-003e
- **CPQ / Configurable Products** (option sets, option mappings, riser prices, matrix options, kit items) — absorbed from add-on per 2026-03-11 revision
- **Credit Card Capture + PCI** (in-app payment processing) — absorbed from add-on per 2026-03-11 revision
- 25 included users (draft — to be refined in Phase 2B)

#### T3: Commerce Enterprise

Everything in T2, plus:

- **Sales Intelligence** (analytics dashboard, sales graphs, territory views, reports, data export) — per D-003e
- Image upgrade (12 product images)
- Priority support SLA
- Dedicated CSM + Executive business reviews
- 50 included users (draft — to be refined in Phase 2B)

#### Add-ons — ELIMINATED (2026-03-11)

> CPQ and Credit Card/PCI moved into T2 and T3 as included capabilities. FlipBook / Interactive PDFs removed from pricing material. There are no published add-ons. CPQ ($195/mo) and Credit Card/PCI ($195/mo) remain available as unpublished à la carte options for T1 accounts only — see à la carte shelf below. Install-base revenue impact of absorption: $975/mo ($11,700/yr) from 5 T3 accounts that currently pay for CPQ; zero PCI absorption (no T2/T3 accounts have PCI).

#### T1→T2 fence: "Browse vs. Buy+Serve"

The defining question: *"Do your buyers place orders through SuperCat and self-serve on order status?"*

Including Online Catalog in T1 means every customer starts with buyer browsing. The T2 upgrade is triggered when buyers should be able to *order* and *self-serve*, not just browse.

#### T2→T3 fence: "Operate vs. Optimize+Govern"

The defining question: *"Do your managers and executives need sales analytics, territory views, and operational intelligence?"*

T3 adds the analytics/intelligence layer plus premium support — addressing both the need for operational visibility and the unmonetized support burden (Problem 5).

#### D-003e: Sales Portal Decomposition — STAMPED 2026-02-25

**Option A: Buyer Self-Serve in T2, Sales Intelligence in T3.**

Confirmed by Sales and CTO in live discussion (2026-02-25). The structural decomposition and the specific allocation are now final:

- **T2 (Commerce Professional)**: Order & Invoice Tracking — order status, invoice lookup, customer dashboard, basic customer views. Completes the buy→track flow alongside B2B Cart.
- **T3 (Commerce Enterprise)**: Sales Intelligence — analytics dashboard, sales graphs, territory views, reports, data export. The T3 exclusive that drives the upgrade trigger.

**Rationale for Option A**:
- Preserves buyer experience coherence: the buy→track flow is unbroken at T2
- Aligns with competitive pattern (AmpTab gates analytics at its top tier)
- Sales and CTO confirmed that the buyer self-serve story strengthens T2 demos and creates a natural "now let's give you visibility into all that activity" upgrade pitch to T3

**Code feasibility**: Existing permission infrastructure supports this. `should_display_portal_dashboard?`, `should_display_advanced_reports?`, and `allow_export_eol_data?` already gate the analytics cluster independently. A new flag (e.g., `enable_buyer_portal`) would gate the self-serve cluster. Engineering scoping remains a Workstream C deliverable.

**Option B (rejected)**: Analytics in T2, Buyer Self-Serve in T3. Rejected due to broken buy→track flow risk at T2, which could suppress Cart adoption and undermine the hero tier's commerce narrative.

#### Feature Allocation Matrix (Pricing Page Direction)

This matrix is the market-facing view of the tier architecture — organized by capability group the way a prospect reads a pricing page. Price points are deferred to M4; this establishes what goes where.

**Option A is reflected below** (stamped as D-003e, 2026-02-25).

**Naming note (revised 2026-01-28)**: All feature names use customer-facing language. See naming crosswalk in validation artifact (`09_website/2026-01-28__pricing_validation_artifact__v1.md`) for internal/code name mapping.

| | **Catalog Essentials** | **Commerce Professional** | **Commerce Enterprise** |
|---|:---:|:---:|:---:|
| | *Browse* | *Buy + Serve* | *Optimize + Govern* |
| **CORE PLATFORM** | | | |
| Admin Console | ✓ | ✓ | ✓ |
| Automated Data Import | ✓ | ✓ | ✓ |
| ERP Integration | ✓ | ✓ | ✓ |
| Multi-Price List Support | ✓ | ✓ | ✓ |
| Real-Time Inventory | ✓ | ✓ | ✓ |
| Product Images | 6 | 6 | **12** |
| **eCAT iPAD APP** | | | |
| eCat iPad App | ✓ | ✓ | ✓ |
| Barcode Scanning | ✓ | ✓ | ✓ |
| Curated Product Lists | ✓ | ✓ | ✓ |
| Document Library | ✓ | ✓ | ✓ |
| Product Sheets & Reports | ✓ | ✓ | ✓ |
| Customer History & Favorites | ✓ | ✓ | ✓ |
| **DIGITAL COMMERCE** | | | |
| Online Product Catalog | ✓ | ✓ | ✓ |
| Online Ordering | | ✓ | ✓ |
| Private Storefront | | ✓ | ✓ |
| Buyer Registration | | ✓ | ✓ |
| Customer-Specific Pricing | | ✓ | ✓ |
| Quick-Order Grid | | ✓ | ✓ |
| Address Validation | | ✓ | ✓ |
| Order & Invoice Tracking | | ✓ | ✓ |
| **CONFIGURABLE PRODUCTS & PAYMENTS** | | | |
| CPQ / Configurable Products | à la carte | ✓ | ✓ |
| Credit Card Capture + PCI | à la carte | ✓ | ✓ |
| **SALES INTELLIGENCE** | | | |
| Sales Intelligence Dashboard | | | ✓ |
| Territory & Performance Views | | | ✓ |
| Sales Reports & Summaries | | | ✓ |
| Data Export (CSV / XLSX) | | | ✓ |
| **SUPPORT & SUCCESS** | | | |
| Standard Support | ✓ | ✓ | ✓ |
| Executive Business Reviews | | | ✓ |
| **INCLUDED USERS** | **15** | **25** | **50** |
| **INCLUDED BRANDS** | **1** | **1** | **1** |
| **Additional Brand Rate** | **$495/mo** | **$895/mo** | **$1,495/mo** |
| **PRICE** | *Phase 2B* | *Phase 2B* | *Phase 2B* |

**À la carte modules** (unpublished — not on pricing page) — **stamped in D-004d, revised 2026-03-11**:

| À la carte Module | Price | Available To | Capabilities | Notes |
|---|---:|---|---|---|
| CPQ / Configurable Products | $195/mo | T1 only | Option sets, option mappings, riser prices, matrix options, kit items | Included in T2/T3. Unpublished fallback for T1 deal-breaking objections. |
| Credit Card Capture + PCI | $195/mo | T1 only | In-app payment processing | Included in T2/T3. Unpublished fallback for T1 deal-breaking objections. |
| B2B Commerce | $795/mo | Any tier | Full T2 increment: Cart, Closed Site, enrollment, contract pricing, gridview, address verification, Order & Invoice Tracking | 46% premium vs implied. |
| Sales Intelligence | $995/mo | Any tier | T3 analytics: dashboard, territory views, reports, data export | 53% premium vs implied. |
| Premium Support | $495/mo | Any tier | Priority SLA, dedicated CSM, executive business reviews | 41% premium vs implied. |

Response mechanism only, not promoted by Sales. Requires Sales leadership sign-off. Flagged for tier migration when usage evolves. See D-004d for tier-push economics.

---

### D-003c: Expansion Mechanism — STAMPED 2026-01-28

Four expansion vectors, building on M2's metric-driven + feature-driven framework:

| Vector | Mechanism | Trigger |
|--------|-----------|---------|
| **Within-tier (users)** | Additional billable users (declining rate curve) | Digital selling org grows; more reps/buyers need access |
| **Within-tier (brands)** | Additional brands beyond included base | Customer acquires new brands, launches new product lines, or consolidates instances |
| **Cross-tier** | T1→T2→T3 upgrade | Digital selling maturity increases; customer needs commerce then analytics |
| **À la carte** | Individual modules at premium | Edge case: prospect has overlapping established capability, or T1 account needs CPQ/PCI without full tier upgrade |

> **Revised 2026-03-11**: Add-ons vector eliminated. CPQ and Credit Card/PCI absorbed into T2/T3 as included capabilities (available as unpublished à la carte for T1 only). FlipBook removed from pricing material. See D-003a v2.

Included users by tier — **revised 2026-04-15** (originally validated in D-004b at 15/25/50; tightened to 10/15/40 per v4 sensitivity sweep):

| Tier | Included Users | Included Brands | Addl Brand Rate | % Accounts Expanding (Users) | Rationale |
|------|:-------------:|:---------------:|:---:|:---:|-----------|
| T1 | **10** | **1** | **$495/mo** | 78% | Captures steepest part of marginal curve ($898/user dropped); 42/54 accounts exceed → strong expansion |
| T2 | **15** | **1** | **$895/mo** | 50% | Median T2 account has 16 users; at 25u, only $983/mo captured. At 15u, revenue doubles to $2,134/mo |
| T3 | **40** | **1** | **$1,495/mo** | 65% | Captures 65% of T3 accounts (vs 47% at 50u); Sig>30% stays flat; zero decrease accounts |

> **D-004c v2 change (2026-02-25)**: Included brands revised from 1/3/5 to 1/1/1 across all tiers. Brands are a separate value dimension from features and users — tiers differentiate on capabilities and included user count, not brand count. Per-brand rates are tier-scaled (65–69% of governing tier) to reflect that higher-tier brands deliver more value. See D-004c v2 analysis for full rationale.

User discount curve — **proposed in D-004b** (step-declining, uniform across tiers):

| Excess Users | Rate/User/Mo | Book Discount | Competitive Position |
|---|---:|---:|---|
| 1–10 | **$25** | 0% | Equal to RepZio ($25), below Pepperi ($48), below Onsight ($65) |
| 11–25 | **$22** | 12% | Below all except AmpTab (unlimited) |
| 26–50 | **$20** | 20% | At revealed effective; below all non-unlimited competitors |
| 51+ | **$18** | 28% | Deep volume discount; rewards largest teams |

> **Billing mechanic: graduated/marginal rates.** The curve uses marginal pricing (like tax brackets), not flat-rate-at-total. Each tranche is billed at its own rate — the first 10 excess users always cost $25/user, regardless of total volume. A customer with 30 excess users pays $250 (10×$25) + $330 (15×$22) + $100 (5×$20) = $680/mo ($22.67 effective), NOT 30×$20 = $600. This avoids the cliff effect where adding one user could retroactively cheapen all previous users, ensures the total cost curve is strictly increasing (no scenario where adding more users lowers the bill), and preserves revenue integrity at every volume level.

> **D-004b key findings (revised v4)**: The included-user allocation and discount curve are interdependent. The original D-004b analysis (15/25/50) was validated against v1 tier assignments. The v3 product audit and v4 sensitivity sweep led to a tightened allocation of 10/15/40 — this restores user MRR to 22% of the mix (vs 17% under 15/25/50), preserving the expansion mechanic that drives NRR while adding +$9,790/mo in user revenue. Full original analysis: `11_synthesis/2026-02-25__user_discount_curve__d004b__v1.md`. Sensitivity sweep: `03_data/2026-04-15__included_user_sensitivity__v1.md`

**Brand definition** *(tightened in D-004c v2)*: A brand, for pricing purposes, is a distinct catalog deployment on the platform that maintains its own product catalog AND its own customer or dealer base. Channel variants, regional configurations, and operational separations each constitute a brand when they operate separate catalogs with separate buyer relationships. Internal organizational trade names that do not produce separate catalog deployments (product categories, market events, workflow states) do not count.

> **Why deployment-based, not marketing-based**: The prior definition ("a go-to-market identity a buyer would recognize") was subjective and created a negotiation surface at the revised brand rates. At $1,495/brand (T3), the marketing test would allow GW to argue that Summer Classics Wholesale, Contract, and Retail are one brand (2 brands total instead of 4) — a $35,880/yr dispute. The deployment test is objective, verifiable from platform configuration, and aligned with value consumed. Full enforcement guidelines to be developed in Phase 2, Workstream D.

**Multi-brand addresses two problems**: (1) Consolidation — existing multi-instance customers (e.g., Generation Brands / Visual Comfort with 4 separate instances) can merge into one instance with multi-brand pricing that preserves comparable revenue; (2) Gaming — prospects cannot cram multiple distinct brands into a single instance at single-brand pricing. Additional brands beyond the 1 included are priced per-brand at natural-tier rates ($674/$1,166/$2,066 — a 10% discount from tier price, mirroring the legacy multi-org discount — see D-004c stress test revision).

Cross-tier upgrade narratives:

| Transition | Trigger | Pitch |
|-----------|---------|-------|
| T1→T2 | Buyers should order online and self-serve | "Your buyers are already browsing — let's let them order and track status too." |
| T2→T3 | Management needs analytics and operational intelligence | "Your commerce is running — now let's give you the analytics to optimize it." |

> **Expansion cannibalization stress test (2026-01-28)**: Tier bundling absorbs some old-model module-sale expansion paths ($20.6K/mo of theoretical white space), but the net expansion ceiling *increases* 64% because tier upgrades capture 2–5× more per conversion, and two net-new vectors (brand expansion, premium support) are created. Same commercial effort yields 111% more expansion revenue under the tier model. See ST-001 in Phase 2B Stress Tests for full analysis.

---

### D-003d: Implementation/Onboarding Treatment — STAMPED (v2 — 2026-03-11)

**Tiered implementation pricing, segmented by data readiness and support need.** Directly addresses Problem 4.

> **Revised 2026-03-11**: Replaced v1 ranges (Standard $2.5–5K / Professional $5–15K / Enterprise $15–30K) with specific price points grounded in cost-to-serve analysis. Renamed tiers to Essentials / Guided / Comprehensive. Custom integrations explicitly excluded (separate pricing surface). Activation deposit mechanism designed but deferred pending billing operations readiness.

#### Segmentation Axis

The primary segmentation axis is **data readiness and support need**, not platform tier. Platform tier determines *scope* (what gets set up — iPad, commerce, portal), but data readiness determines *effort* (how much hand-holding SuperCat provides). A T1 customer with messy data may need Comprehensive; a T3 customer with automated data feeds might qualify for Guided. In practice, the furniture/lighting market's low tech maturity means most current customers index toward Comprehensive.

#### Implementation Packages

| | **Essentials** | **Guided** | **Comprehensive** |
|---|---|---|---|
| **Price** | **Included** | **$2,500** | **$5,000** |
| **For** | Data-ready customers with internal admin capacity | Typical customers needing data remediation and guided setup | Complex data environments, extensive hand-holding, managed onboarding |
| **Data posture** | Clean product data in required format; photography ready; designated admin available | Data needs transformation/cleanup; photography gaps; shared admin responsibility | Multiple data sources; no standardized format; significant remediation required |
| **SuperCat role** | Validate & import; configure; checklist handoff | Lead configuration; remediate common data issues; guide admin through setup | Dedicated onboarding lead; extensive data remediation; full configuration management |
| **Admin training** | 1 session | 2 sessions | 2 sessions + ongoing office hours |
| **User training** | 1 session | 2 sessions | 2 sessions + role-specific enablement |
| **Value realization** | Go-live checklist + 30-day check-in | Go-live + 30-day check-in + 90-day adoption review | Go-live + 30-day check-in + 90-day adoption review + QBR alignment |
| **Timeline** | 4–6 weeks | 6–10 weeks | 10–14 weeks |
| **Billing** | No incremental charge | One-time fee, billed at activation | One-time fee, billed at activation |

#### Cost Basis

Fully loaded onboarding cost-to-serve (salary + payroll taxes + benefits + overhead):

| Role | Hourly Rate (loaded) | Typical Hours (Comprehensive) |
|---|---:|---:|
| Onboarding Manager | $75/hr | 12–15 hrs |
| CTO / Engineering | $94/hr | 3–4 hrs |
| Support | $25/hr | 2–4 hrs |
| **Total cost per onboarding** | | **$1,500–$2,000** |

Essentials costs ~$500–800 (absorbed into subscription). Guided costs ~$1,200–1,600. Comprehensive costs ~$1,500–2,000. At stamped price points, margins are: Essentials = absorbed, Guided = ~1.5x, Comprehensive = ~2.5x.

#### Scope Boundaries

Each package includes explicit boundaries:

- Number of import cycles included (Essentials: 1, Guided: 2–3, Comprehensive: unlimited within timeline)
- Supported data sources and file formats (SuperCat standard templates, CSV, FTP)
- Definition of "customer-ready" product photography and data
- **Out of scope (all packages)**: custom integrations, bespoke data transformations, net-new API development — these are priced separately as integration engagements

#### Upgrade Rules

- If a customer booked at Essentials proves not to be data-ready, the project moves to Guided ($2,500) or Comprehensive ($5,000). The customer is notified at the earliest sign of data-readiness mismatch, not after weeks of drag.
- Custom programming and training beyond scope is handled as Professional Services per the overarching agreement.

#### Activation Deposit Mechanism — DESIGNED, DEFERRED

A deposit mechanism has been designed to solve implementation drag:

| Package | Total Fee | Activation Deposit (20%) | On-Time Outcome | Delayed Outcome |
|---|---:|---:|---|---|
| Guided | $2,500 | $500 | Credited to first invoice(s) | Funds dedicated PM to finish onboarding |
| Comprehensive | $5,000 | $1,000 | Credited to first 1–2 invoices | Funds dedicated PM to finish onboarding |

**Why deferred**: SuperCat currently bills for the entire onboarding fee and first period of subscription at activation (onboarding kickoff). The deposit mechanism requires the ability to issue post-go-live subscription credits, which is not supported by the current billing process. This is a Phase 2 / billing operations enhancement — the pricing architecture accommodates it when ready.

**Design intent**: The deposit is not punitive. On-time completion rewards the customer with a subscription credit (net implementation cost drops by 20%). Delayed completion reallocates the deposit to dedicated PM time to finish the project. Both outcomes serve the customer — one rewards speed, the other funds rescue.

#### Competitive Context

AmpTab charges $5K–$30K setup (SuperCat's Comprehensive at $5,000 sits at the floor of this range). WizCommerce uses "<30 days, low-cost" as a competitive weapon. SuperCat's Essentials (included) neutralizes WizCommerce's positioning while Guided and Comprehensive reflect the genuine complexity of furniture/lighting vertical implementations.

---

### D-003f: Data Integration Pricing — STAMPED 2026-03-11

**Tiered integration pricing, independent of platform tier.** Complements D-003d (onboarding) — onboarding gets the platform configured, populated, and users trained; integration gets external systems connected. Priced separately because the complexity spectrum is too wide to bundle.

#### Data Assessment — $1,500 one-time (creditable)

The gate before any paid integration work. Required before Tier B or Tier C.

| Deliverable | Detail |
|---|---|
| Source system inventory | ERP/PIM/data warehouse identification and ownership map |
| Field coverage assessment | Gap analysis against SuperCat schema; quality risks; the "80/20 unknowns" |
| Complexity rating | Low / Medium / High with recommended tier (A/B/C) |
| Proposed cadence | Hourly / daily / etc., with constraints (SuperCat is offline-first, not real-time) |
| Scoped SOW | Build tasks, acceptance criteria, change-control rules (if Tier B or C) |

Credited against Tier B or C build if customer proceeds within 30 days.

#### Tier A — Self-Serve FTP: Included

Customer produces SuperCat-format CSVs and uploads to FTP.

SuperCat provides:
- Canonical file specification, templates, and examples
- Validation tooling (import checks, error surfacing, reconciliation exports)
- Office hours and knowledge base support

No incremental cost. Available to any platform tier.

#### Tier B — Certified Pipeline (customer-owned): $2,500 one-time

SuperCat certifies the customer's (or their vendor's) integration pipeline. Customer owns and runs the pipeline post-certification.

| Deliverable | Detail |
|---|---|
| Source-system discovery | Identify data sources, endpoints, formats |
| Mapping guidance | Map customer fields → SuperCat CSV schema |
| Test imports | Validate data quality, error handling, reconciliation |
| Acceptance checklist | Formal sign-off on data completeness and accuracy |
| Go-live runbook | Cadence, error handling, escalation procedures |

**Effort ceiling**: ≤20 hours of engineering/onboarding time. No recurring fee — customer owns the running cost.

**Cost basis**: ~$1,700 fully loaded (20 hrs × ~$85/hr blended). Margin: ~1.5x.

#### Tier C — Managed Integration (SuperCat-run): $5,000 build + $300/mo hosting

SuperCat builds AND operates the integration pipeline. Ongoing operational obligation.

**Build (one-time — $5,000):**
- Extraction/mapping from customer API/exports
- Generate SuperCat CSVs and deliver to FTP on agreed cadence
- Testing, acceptance, go-live
- For genuinely exceptional complexity (multiple source systems, extensive special-casing): SOW-based pricing above $5,000, documented as exception

**Hosting (recurring — $300/mo):**

| Included in Hosting | Billable ($200/hr) |
|---|---|
| Monitoring and alerting | New endpoints / systems |
| Incident response and break/fix | New feature development |
| Compatibility updates from SuperCat platform changes | Custom reporting outside standard dashboards |
| Minor configuration adjustments | Large-scale data restructuring |
| 2 hours/month change budget | After-hours emergency work |

**Service Level Agreement:**

| Severity | Definition | Response Time |
|---|---|---:|
| **Sev 1** | Pipeline down / no data updates / order submission impacted | ≤ 4 business hours |
| **Sev 2** | Partial degradation / intermittent failures | ≤ 1 business day |
| **Sev 3** | Questions / minor issues / change requests | ≤ 2 business days |

Business Hours: 9:00 AM – 5:00 PM EST, Monday through Friday (excluding Company holidays).

**Cost basis**: Build ~$2,000-$3,000 (20-30 hrs engineering). Hosting ~$170-$250/mo (2-3 hrs CTO time). Build margin: ~2x. Hosting margin: ~1.5x.

#### Structural Decisions

| Decision | Resolution |
|---|---|
| **Tier availability** | Fully independent of platform tier — available to any customer regardless of T1/T2/T3 |
| **Billing cadence (hosting)** | Monthly, aligned with subscription. Annual prepay discount to follow D-004e |
| **Existing customer migration** | Coaster ($3,000/yr) grandfathered for current term; migrated to $300/mo ($3,600/yr) at renewal |
| **Change requests beyond budget** | $200/hr, scoped and approved before work begins |

#### Pricing Coherence

Onboarding and integration follow a parallel pricing structure:

| | **Included** | **Mid** | **Full** |
|---|---|---|---|
| **Onboarding** | Included (Essentials) | $2,500 (Guided) | $5,000 (Comprehensive) |
| **Integration** | Included (Self-Serve FTP) | $2,500 (Certified Pipeline) | $5,000 build + $300/mo (Managed) |
| **Gate** | — | $1,500 Data Assessment (creditable) | $1,500 Data Assessment (creditable) |

#### Sales Positioning

- **Default**: "We support a self-serve FTP upload path that every customer can use — it's the lowest-friction way to get live."
- **If they want automation**: "You can run your own pipeline and we'll certify it, or we can build and run it for you as a managed service."
- **If they ask for real-time**: "SuperCat is offline-first — we optimize for reliable snapshots on a cadence, not transactional real-time sync."
- **If they push on hosting fee**: "If we run the pipeline, we're on the hook for monitoring, incidents, platform compatibility, and change control. The $300/mo funds that obligation and prevents best-effort surprises."

> **Reference**: Full integration commercialization analysis in `11_synthesis/2026-02-06__data_integration_commercialization__v1.md`. Coaster SLA template in `Downloads/SuperCat _ Coaster Furniture - SLA ERP Data Integration.docx` (to be revised per SLA structure above).

---

### M3 Open Items — To Be Resolved in Phase 2 and via Concept Testing

| Item | Resolution Path | Priority |
|------|----------------|----------|
| ~~Sales Portal decomposition direction (Option A vs. B)~~ | ~~Phase 2, Workstream A~~ | **RESOLVED — D-003e stamped 2026-02-25. Option A confirmed by Sales + CTO.** |
| ~~Price points for T1/T2/T3~~ | ~~Phase 2, Workstream B (price point modeling)~~ | **RESOLVED — D-004a stamped 2026-02-25. T1 $749, T2 $1,295, T3 $2,295.** |
| ~~User discount curve design~~ | ~~Phase 2, Workstream B~~ | **RESOLVED — D-004b proposed 2026-02-25. Step-declining $25/$22/$20/$18. Included users revised to 10/15/40 (2026-04-15 v4 sensitivity sweep).** |
| ~~À la carte module pricing (premium schedule)~~ | ~~Phase 2, Workstream B (price point modeling)~~ | **RESOLVED — D-004d stamped 2026-02-25. Commerce $795, SI $995, Premium Support $495. Unpublished, response-only.** |
| ~~Per-brand pricing (additional brands beyond included)~~ | ~~Phase 2, Workstream B (price point modeling)~~ | **RESOLVED — D-004c stamped (v2) 2026-02-25, revised per v4/v5 stress test. Natural-tier at 90% of book (10% discount): $674/$1,166/$2,066 per additional brand. 1 brand included per tier. Per-brand included users (no pooling). Governing tier rule retired. Consolidation-only (Path B) — not applied on default migration path.** |
| Brand definition enforcement guidelines | Phase 2, Workstream D (migration policy) + Sales/CS enablement | Phase 2 — definition tightened to deployment-based in D-004c v2; enforcement playbook and edge-case guidance still needed |
| Multi-instance consolidation migration playbook | Phase 2, Workstream D (migration policy) + CS + Finance | Phase 2 — entity migration table produced (`entity_migration_table__v1.csv`). Path B confirmed: consolidation is reactive, not proactively offered. |
| Order & Invoice Tracking (T2) vs. Sales Intelligence (T3) gating implementation | Phase 2, Workstream C (operational readiness) + Engineering scoping — **direction settled per D-003e; scoping needed** | Phase 2 |
| Sales team 60-second test | Phase 2, Workstream A (validation gate) | Before strategy lock |
| Competitive response plan (unlimited users narrative) | Phase 4 (operational buildout) + GTM readiness | Before pilot |

---

## Phase 2B: Price Point Modeling — IN PROGRESS

> **Status**: Exercise 1 (Install-Base Tier Mapping & Revealed WTP) complete. Exercise 2 (Competitive Price Benchmarking) pending.
>
> **Reference document**: `11_synthesis/2026-02-25__install_base_tier_mapping_wtp__d004a_exercise1__v1.md`

### D-004a: Set Price Points for Each Tier — IN PROGRESS

#### Exercise 1: Install-Base Tier Mapping & Revealed WTP (completed 2026-02-25)

Every active account (104) was assigned to its natural tier based on current module stack, then current pricing was analyzed by tier-equivalent group to establish revealed willingness-to-pay.

**Tier assignment methodology**: T1 = no Cart, no Portal (iPad-only or iPad+Catalog). T2 = has Cart but NOT Portal. T3 = has Portal (regardless of Cart). Add-ons (CPQ, PCI) are orthogonal.

##### Tier Distribution

| | T1: Catalog Essentials | T2: Commerce Professional | T3: Commerce Enterprise |
|---|:---:|:---:|:---:|
| **Accounts** | 61 (59%) | **9 (9%)** | 34 (33%) |
| **Total MRR** | $59,132/mo (40%) | $13,735/mo (9%) | $75,731/mo (51%) |

##### Revealed WTP — Platform-Only MRR (excluding users and add-ons)

This is the core pricing signal: what accounts currently pay for the capability bundle that a tier price replaces.

| | T1 | T2 | T3 |
|---|---:|---:|---:|
| **P25 (floor)** | $652 | $1,387 | $1,515 |
| **Median** | **$725** | **$1,414** | **$1,670** |
| **P75 (ceiling)** | $725 | $1,427 | $1,810 |
| **Current book** | $725 | $1,315 | $1,710 |
| **T(n)/T1 ratio** | 1.0x | 2.0x | 2.3x |

##### Key Findings

1. **T2 is the growth tier with a real install-base foothold.** 16 accounts (15%) now map to T2 after CPQ/CC corrections (was 9 in v2). T2's price attracts T1 upgrades and new customers, and the corrected tier assignments validate T2 as a meaningful install-base tier.

2. **T3/T2 ratio is too tight at 1.2x.** Typical G/B/B models step 1.5–2.5x per tier. The gap needs widening — either by raising T3 or lowering T2 — to create meaningful upgrade aspiration.

3. **M1 segment → tier crosswalk gap.** M1 classified 28 accounts as Commerce-Active, but only 9 have T2 modules. ~19 accounts are behaviorally Commerce-Active but modularly T1 — prime T1→T2 upgrade candidates.

4. **Effective user rate is $20/user across all tiers** (vs. $25 book). The market has spoken: $20 is the revealed baseline for the user discount curve (D-004b).

5. **T3 accounts missing Cart (14 of 34) gain it free in the new model.** Strongest value-add migration narrative.

6. **T1 is bimodal**: ~31 accounts at/above $725 (standard), ~30 below (legacy discounts). Migration sequencing, not pricing.

7. **"More value at comparable cost"** is the migration narrative. T2 accounts gain 6 new capabilities; T3 accounts gain 8+ including analytics and premium support.

##### Preliminary Price Ranges (pre-competitive benchmarking)

| Tier | Revealed Anchor | Suggested Range | Rationale |
|---|---:|---:|---|
| **T1** | $725 | $695–$795 | At or near current book. Online Catalog inclusion justifies modest uplift. |
| **T2** | $1,414 | $1,195–$1,395 | Below revealed median to maximize T1→T2 upgrade pull. Hero tier = priced for adoption. |
| **T3** | $1,670 | $1,795–$2,195 | Above revealed median. Sales Intelligence + premium support + 50 users justifies uplift. |

These ranges would produce tier ratios of ~1.5–2.0x (T2/T1) and ~1.3–1.8x (T3/T2) — wider than the 1.2x revealed gap.

##### Open Concerns from Exercise 1

**Concern 1: Barbell distribution vs. expected bell curve**

Classic G/B/B models target a bell curve (e.g., 20/60/20) with the hero tier capturing the majority. Exercise 1 produced a barbell: 59% T1, 9% T2, 33% T3. T2 is a "no man's land."

*Assessment*: The barbell describes the **current state under the old model**, not a prediction of the future state. It is the symptom of Problem 2 ("per-module pricing does not support natural expansion or tier logic"). Under a-la-carte pricing, there was no structural middle — customers either stayed on iPad or went to full stack. The new T2 is designed to create the bell curve landing zone that doesn't exist today.

The bell curve should emerge from three sources:
1. **T1 upgrades**: ~19 behaviorally-Commerce-Active T1 accounts are the immediate pipeline
2. **New customers**: Prospects *without* an existing B2B commerce site who are ready to launch digital ordering and buyer self-serve for the first time are natural T2 buyers — SuperCat gives them a vertically integrated commerce layer alongside catalog and rep tools without requiring a separate platform. (Prospects who *already* operate a B2B site are more likely T1 buyers adding catalog/iPad capabilities alongside their existing commerce infrastructure; rip-and-replace of an incumbent B2B platform is rare in observed prospect behavior.)
3. **T3 right-sizing**: Some current T3 accounts (particularly the 14 with Portal but no Cart) may be better served at T2 if their Portal use is primarily buyer self-serve rather than analytics (see below)

*Monitoring*: The speed at which the barbell resolves to a bell curve is a key leading indicator for whether T2 is priced and positioned correctly. If T2 remains at <15% of accounts after 12 months of new-customer acquisition, the tier fence or pricing needs revisiting.

**Concern 2: T3 support capacity (34 accounts with premium commitments)**

T3 promises priority support SLA, dedicated CSM, and executive business reviews. At 34 accounts, this is a substantial delivery commitment that may exceed current support capacity.

*Mitigating factors*:
1. **T3 population may shrink.** If the Sales Portal decomposition (Option A) resolves — and some of the 14 Portal-but-no-Cart accounts are found to primarily use buyer self-serve rather than analytics — they could migrate to T2 instead of T3. This could reduce T3 to 20–25 accounts, closer to the original M1 Platform-Embedded count of 20.
2. **"Dedicated CSM" does not require 1:1 staffing.** A named CSM with a book of 10–15 T3 accounts is standard in vertical SaaS. At 20–25 T3 accounts, that's 2 CSMs; at 34, that's 3.
3. **Support tiers within T3 can be graduated.** Executive business reviews could be quarterly for top-revenue T3 accounts and semi-annual for others. Priority SLA is primarily a process change (faster response target), not a dedicated headcount.

*Resolution path*: This is a Workstream C (Operational Readiness) deliverable. The question "can we deliver T3-level support to N accounts?" must be answered with a concrete capacity assessment before T3 pricing is finalized. If the answer is "not at 34, but yes at 20–25," that feeds back into the portal decomposition decision and may tighten the T2→T3 fence.

*Dependency resolved*: The Sales Portal decomposition is now stamped (D-003e, 2026-02-25). Option A (Buyer Self-Serve in T2, Sales Intelligence in T3) confirmed by Sales + CTO. Under Option A, Portal-but-no-Cart accounts that primarily use buyer self-serve (order tracking, invoices) rather than analytics are T2 candidates — potentially reducing T3 from 34 to 20–25. Workstream C should assess which of the 14 Portal-but-no-Cart accounts are analytics-active vs. self-serve-only to finalize the T3 population.

#### Exercise 2: Competitive Price Benchmarking — COMPLETE (2026-02-25)

Full analysis: `11_synthesis/2026-02-25__competitive_price_benchmarking__d004a_exercise2__v1.md`

Mapped preliminary price ranges against direct competitors with freshly validated pricing (Feb 2026). All competitor pricing was re-confirmed via web research; data freshness documented in the analysis appendix.

##### Competitive Pricing Summary (validated Feb 2026)

**Direct Competitors**

| Vendor | Tier | Platform Fee | Setup Fee | Users | Value Metric |
|---|---|---:|---:|---|---|
| **AmpTab** | Starter | $500/mo | $5,000 | **Unlimited** | Platform tier |
| **AmpTab** | Advanced | $1,000/mo | $10,000 | **Unlimited** | Platform tier |
| **AmpTab** | Pro | $3,000/mo | $30,000 | **Unlimited** | Platform tier |
| **Pepperi** | Pro | $500/mo | — | $48/user/mo | Platform + per-user |
| **Pepperi** | Corporate | $1,500/mo | — | $78/user/mo | Platform + per-user |
| **Pepperi** | Ultimate | Custom | — | $128/user/mo | Platform + per-user |
| **WizCommerce** | — | ~$500–1,000/mo (est.) | Low/none | Unknown | Quote-only |
| **MarketTime** | — | Quote-only | — | Unknown | Network/quote |
| **RepZio** | Rep App | $25/user/mo | — | Per-user | Pure per-user |
| **RepZio** | B2B Direct | $300/mo | — | N/A | Platform |

**Adjacent Competitors**

| Vendor | Tier | Price | Users | Notes |
|---|---|---:|---|---|
| **Candid Wholesale** | Pro | $179–219/mo | 1 | Up to $1.5M order volume |
| **Candid Wholesale** | Complete | $599–719/mo | 5 | Up to $5M order volume |
| **Onsight** | Business | $65/user/mo | Per-user | iPad sales app (horizontal) |
| **Geckoboard** | Core–Pro | $175–319/mo | 25–50 viewers | Sales dashboards only |
| **Equals** | CRM–GTM | $699–1,899/mo | — | Sales analytics only |

##### Tier-by-Tier Competitive Mapping

**T1: Catalog Essentials — SuperCat range: $695–$795/mo**

| Competitor | Equivalent | Total at 15 users | vs. SuperCat T1 |
|---|---|---:|---|
| **AmpTab Starter** | iOS app + buyers portal + unlimited SKUs + basic reporting | **$500/mo** | SuperCat is 39–59% more |
| **Pepperi Pro** | Web + mobile apps + barcode + multiple price lists | **$1,220/mo** | SuperCat is 35–43% less |
| **RepZio** | iOS app + offline + inventory + reports (no online catalog) | **$375/mo** | SuperCat is 85–112% more |
| **Onsight Business** | iPad sales app only (horizontal, no online catalog) | **$975/mo** | SuperCat is 19–29% less |

Competitive position: SuperCat T1 sits between AmpTab Starter ($500) and Pepperi Pro ($1,220). AmpTab gap ($195–295/mo premium) is justified by Online Product Catalog inclusion in T1 (AmpTab Starter's "buyers portal" is basic), vertical specialization in furniture/lighting, and AmpTab's $5K setup fee amortization ($417/mo → effective AmpTab Y1 = $917/mo).

**T2: Commerce Professional — SuperCat range: $1,195–$1,395/mo**

| Competitor | Equivalent | Total at 25 users | vs. SuperCat T2 |
|---|---|---:|---|
| **AmpTab Advanced** | Starter + website + CRM/ERP + credit card + CPQ + advanced reporting | **$1,000/mo** | SuperCat is 20–40% more |
| **Pepperi Corporate** | Multi-storefront + multi-language/currency + trade promos | **$3,450/mo** | SuperCat is 60–65% less |
| **WizCommerce** | WizOrder + WizShop (estimated) | **~$1,000/mo** | Roughly comparable |
| **RepZio + B2B Direct** | Rep app + storefront | **$925/mo** | SuperCat is 29–51% more |

Competitive position: The hero tier sits in the competitive sweet spot between AmpTab Advanced ($1,000) and Pepperi Corporate ($3,450). Key differentiator: SuperCat's T2 includes Order & Invoice Tracking (buyer self-serve) — AmpTab gates equivalent capability at Pro ($3,000). This is the strongest competitive narrative. CPQ is now included in T2 (previously a $195/mo add-on), making the comparison cleaner: SuperCat T2 ($1,295, CPQ included) vs. AmpTab Advanced ($1,000, CPQ included). The $295 gap is justified by Order & Invoice Tracking and further narrowed by AmpTab's $10K setup ($833/mo amortized → effective AmpTab Y1 = $1,833/mo).

**T3: Commerce Enterprise — SuperCat range: $1,995–$2,495/mo** (shifted up from Exercise 1's $1,795–$2,195)

| Competitor | Equivalent | Total at 50 users | vs. SuperCat T3 |
|---|---|---:|---|
| **AmpTab Pro** | Advanced + custom website + data exports + analytics + AI + territory mapping | **$3,000/mo** | SuperCat is 17–33% less |
| **Pepperi Ultimate** | Full enterprise suite | **$6,400+/mo** | SuperCat is 61–69% less |
| **Equals GTM** | Sales analytics only (no commerce) | **$1,899/mo** | Analytics-only benchmark |

Competitive position: Significant headroom. AmpTab Pro at $3,000 sets the ceiling; even at $2,495 (top of range), SuperCat is $505/mo cheaper. AmpTab Pro includes capabilities SuperCat doesn't offer (AI merchandising, custom website, kiosks, retailer data feeds), but AmpTab's $30K setup fee ($2,500/mo amortized → effective AmpTab Y1 = $5,500/mo) is a substantial barrier. The upward shift from Exercise 1 is directly supported by this headroom.

##### Normalized Total Cost of Ownership (at typical team sizes)

| Team Size | AmpTab | SuperCat (mid) | Pepperi | RepZio |
|---|---:|---:|---:|---:|
| **15 users (T1)** | $500 | **$745** | $1,220 | $375 |
| **25 users (T2)** | $1,000 | **$1,295** | $3,450 | $925 |
| **50 users (T3)** | $3,000 | **$2,245** | $6,400+ | $1,550 |
| **100 users (T3)** | $3,000 | **$3,245*** | $12,800+ | $2,800 |

*\*50 additional users at ~$20/user effective rate. Per-user crossover with AmpTab Pro occurs at ~100 users — applies to <10% of accounts.*

**Key insight**: SuperCat is competitive at every tier and team size. The per-user model creates a crossover point at ~100 users where SuperCat total cost approaches AmpTab Pro — but this affects very few accounts, and the per-user revenue ($34,653/mo, 23% of MRR) is too valuable to abandon.

##### Setup Fee Amortization (Y1 effective monthly cost)

| | Monthly | Setup | Y1 Effective |
|---|---:|---:|---:|
| **AmpTab Starter** | $500 | $5,000 | **$917** |
| **AmpTab Advanced** | $1,000 | $10,000 | **$1,833** |
| **AmpTab Pro** | $3,000 | $30,000 | **$5,500** |
| **SuperCat T1 (mid)** | $745 | ~$3,750 | **$1,058** |
| **SuperCat T2 (mid)** | $1,295 | ~$10,000 | **$2,128** |
| **SuperCat T3 (mid)** | $2,245 | ~$22,500 | **$4,120** |

When setup fees are amortized, SuperCat's Y1 effective cost is within 15% of AmpTab at every tier — a much tighter competitive picture than monthly sticker prices alone suggest.

##### Competitive Positioning: Strengths & Vulnerabilities

**Where SuperCat wins:**

| Advantage | vs. AmpTab | vs. Pepperi | vs. WizCommerce | vs. RepZio |
|---|---|---|---|---|
| **Vertical depth** (furniture/lighting) | Comparable | SC wins | SC wins | SC wins |
| **CPQ / Configurable products** | AmpTab has it at Advanced | Not mentioned | Not available | Basic only |
| **Order & Invoice Tracking in T2** | AmpTab gates at Pro ($3K) | Available | Unknown | Basic |
| **Price transparency** | Both transparent | Both transparent | Quote-only (SC wins) | Both transparent |
| **Expansion economics** | SC captures user growth | Both capture | Unknown | SC broader platform |

**Where SuperCat is vulnerable:**

| Vulnerability | Competitor | Mitigation |
|---|---|---|
| **Unlimited users** | AmpTab (all tiers) | TCO narrative; user charges fund product investment |
| **AI capabilities** | WizCommerce (Kai, AI search) | Product roadmap — outside pricing scope |
| **Implementation speed** | WizCommerce (<30 days) | Depth and quality for complex data (furniture/lighting) |
| **Network effects** | MarketTime (300K buyers) | Different value prop — platform vs. marketplace |
| **Enterprise breadth** | Pepperi (multi-language, DSD) | Vertical focus, not horizontal enterprise |

##### The "Unlimited Users" Response Narrative

AmpTab's most potent competitive message. SuperCat's four-part response:

1. **"Unlimited users" is priced into the platform fee.** AmpTab Starter at $500 with unlimited users vs. SuperCat T1 at $695–795 with 10 included — AmpTab is effectively charging a higher platform fee that bundles user costs. For accounts with <10 users, SuperCat is the better deal.
2. **SuperCat's model rewards right-sizing.** A 10-user team shouldn't subsidize a 200-user deployment. Included base (10/15/40) covers the baseline team at each maturity stage, with transparent graduated expansion pricing.
3. **User charges are the expansion engine.** 23% of SuperCat's MRR ($416K/yr) comes from user expansion. Eliminating this would require raising platform fees ~30% — making SuperCat less competitive at entry points.
4. **The real comparison is total cost.** At 50 users, SuperCat T3 ($2,245) is still cheaper than AmpTab Pro ($3,000). Unlimited-users only matters if comparing sticker prices, not total cost of ownership.

##### Competitive Response Playbook (draft)

| Competitor | When encountered | Key message | Proof point |
|---|---|---|---|
| **AmpTab** | Most common | "Comparable features, lower total cost at scale, vertical depth for furniture/lighting" | Y1 TCO comparison including setup fees |
| **AmpTab "unlimited users"** | If raised | "Our included base covers your team. You pay for growth, not phantom seats. Compare total cost, not sticker price." | Total cost at actual team size |
| **Pepperi** | Enterprise deals | "Same capabilities at 60% less. Pepperi charges $48–128/user — our included base + expansion rate is dramatically more affordable." | 25-user Pepperi Corporate = $3,450 vs. SuperCat T2 = $1,295 |
| **WizCommerce** | AI-forward prospects | "AI is a feature, not a platform. We run your commerce operation end-to-end including configurable products." | CPQ capability gap; implementation depth |
| **RepZio** | Price-sensitive | "RepZio is a rep tool, not a commerce platform. No online catalog, no buyer self-serve, no analytics." | Feature gap comparison |
| **"We can build it"** | Enterprise | "Total build cost exceeds 5 years of SuperCat. You're buying ongoing product investment, not a one-time build." | Implementation complexity + ongoing maintenance |

##### Price Range Refinement

Overlaying competitive benchmarks on Exercise 1's revealed WTP ranges:

**T1: Catalog Essentials**

| Anchor | Value |
|---|---:|
| Exercise 1 revealed median | $725 |
| Exercise 1 range | $695–$795 |
| AmpTab Starter (sticker) | $500 |
| AmpTab Starter Y1 effective | $917 |
| Pepperi Pro (15 users) | $1,220 |

Refined range: **$695–$795** (unchanged). Sweet spot between AmpTab Starter Y1 effective ($917) and Pepperi Pro ($1,220). Below $695 sacrifices revenue without gaining competitive position; above $795 widens the AmpTab sticker gap uncomfortably.

**T2: Commerce Professional**

| Anchor | Value |
|---|---:|
| Exercise 1 revealed median | $1,414 |
| Exercise 1 range | $1,195–$1,395 |
| AmpTab Advanced (sticker) | $1,000 |
| AmpTab Advanced Y1 effective | $1,833 |
| Pepperi Corporate (25 users) | $3,450 |

Refined range: **$1,195–$1,395** (unchanged). At $1,195, only $195/mo more than AmpTab Advanced — justified by Order & Invoice Tracking (AmpTab gates at $3K). At $1,395, still well below AmpTab Y1 effective ($1,833). With CPQ now included in T2 (per 2026-03-11 revision), the comparison is apples-to-apples: SuperCat T2 ($1,295) vs. AmpTab Advanced ($1,000) — both include CPQ. The $295 gap is justified by Order & Invoice Tracking and further narrowed by AmpTab's $10K setup.

**T3: Commerce Enterprise**

| Anchor | Value |
|---|---:|
| Exercise 1 revealed median | $1,670 |
| Exercise 1 range | $1,795–$2,195 |
| AmpTab Pro (sticker) | $3,000 |
| AmpTab Pro Y1 effective | $5,500 |
| Pepperi Ultimate (50 users) | $6,400+ |

Refined range: **$1,995–$2,495** (shifted up from $1,795–$2,195). Competitive headroom justifies the uplift: even at $2,495, SuperCat is 17% below AmpTab Pro. This widens the T3/T2 ratio from ~1.3x to ~1.6x at midpoints, directly addressing the Exercise 1 concern about insufficient tier differentiation. The "more value at comparable cost" migration narrative holds — current T3 accounts pay a median of $1,670 but gain 8+ new capabilities.

##### Combined Price Ranges (Exercise 1 + Exercise 2)

| Tier | Exercise 1 (WTP) | Exercise 2 (Competitive) | **Combined** | Rationale |
|---|---:|---:|---:|---|
| **T1** | $695–$795 | $695–$795 | **$695–$795** | Anchored to current book ($725). Competitive with AmpTab Y1 effective. |
| **T2** | $1,195–$1,395 | $1,195–$1,395 | **$1,195–$1,395** | Hero tier priced for adoption. $195–395 premium to AmpTab Advanced is defensible. |
| **T3** | $1,795–$2,195 | $1,995–$2,495 | **$1,995–$2,495** | Competitive headroom justifies upward shift. 17–33% below AmpTab Pro. |

##### Tier Ratios at Midpoints

| Ratio | Exercise 1 Only | Combined | G/B/B Best Practice |
|---|:---:|:---:|:---:|
| T2/T1 | 1.7x | **1.7x** | 1.5–2.0x |
| T3/T2 | 1.4x | **1.7x** | 1.5–2.5x |
| T3/T1 | 2.7x | **3.0x** | 2.5–3.5x |

The combined ranges produce tier ratios squarely within the G/B/B best-practice range. The T3/T2 improvement (from 1.4x to 1.7x) directly addresses the Exercise 1 concern about insufficient differentiation.

---

### D-004a: Tier Price Points — STAMPED 2026-02-25

**T1: $749/mo | T2: $1,295/mo | T3: $2,295/mo**

Approved by CEO. Full migration model: `03_data/tier_price_recommendation.py`

#### Price Points & Rationale

| Tier | Price | Current Book | Delta | Rationale |
|---|---:|---:|---:|---|
| **T1 — Catalog Essentials** | **$749** | $725 | +$24 (+3%) | $24 above current book. Online Catalog now included (was $295/mo add-on). Competitive with AmpTab Starter Y1 effective ($917). |
| **T2 — Commerce Professional** | **$1,295** | $1,315 | -$20 (-2%) | Midpoint of range. Below revealed median ($1,414) — priced for adoption as the hero tier. Order & Invoice Tracking included; AmpTab gates equivalent at Pro ($3,000). |
| **T3 — Commerce Enterprise** | **$2,295** | $1,710 | +$585 (+34%) | Above mid-range. 23% below AmpTab Pro ($3,000). Sales Intelligence + priority SLA + dedicated CSM + 40 included users justify uplift. |

#### Tier Ratios

| Ratio | Value | Best Practice |
|---|:---:|:---:|
| T2/T1 | **1.73x** | 1.5–2.0x |
| T3/T2 | **1.77x** | 1.5–2.5x |
| T3/T1 | **3.06x** | 2.5–3.5x |

#### Revenue Impact (install base)

| Metric | Current | New | Delta |
|---|---:|---:|---:|
| Total MRR | $148,598 | $178,978 | **+$30,380 (+20.4%)** |
| Total ARR | $1,783,181 | $2,147,736 | **+$364,555** |

> **Revised 2026-04-15 (v5)**: v1 total was $165,040 (+11.1%). v2 corrected three data errors (+$3,625/mo). v3 corrected product audit findings (+$2,018/mo). v4 tightened included-user allocation from 15/25/50 to 10/15/40 (+$9,790/mo). v5 removed brand charges from the default migration path (-$1,495/mo) — brand pricing (D-004c) is consolidation-only (Path B). Net v1→v5 improvement: +$13,938/mo.

Full account-by-account model: `03_data/2026-04-15__migration_revenue_model__v5.md`
Canonical account export: `03_data/extracts/2026-04-15__migration_table__v5.csv` (104 accounts × 31 columns)
Entity migration view: `03_data/extracts/2026-04-15__entity_migration_table__v1.csv` (11 entities × 22 columns)

##### Migration Model Methodology (v5)

The migration model maps every current account to future-state pricing using mechanical tier assignment (portal → T3, cart/CPQ/CC → T2, else → T1), applies stamped pricing components (tier base + graduated user charges), and classifies the resulting delta by its primary driver. Brand charges are excluded from the default path — brand pricing is consolidation-only (D-004c, Path B).

Six key methodological choices distinguish v5:

1. **Decomposed source data.** Uses `actual_platform_fee` and `actual_user_charges` from the Angie-audited v3 master table, not the `mrr_platform` column (which bundled user charges into platform fees for some accounts).

2. **Brand dimension.** Reads `n_sites` from the v3 master and applies per-brand fees (D-004c) for multi-site accounts.

3. **Modeled users.** For accounts where the current platform fee bundles a user provision (e.g., Progress Lighting's $2,100 includes 80 users), uses the contractual user count (`modeled_users=80`) rather than the billboard snapshot (`billable_users=3`). The `assumptions` column documents every such judgment.

4. **CPQ/CC as tier-driving features (v3).** Product audit confirmed CPQ and CC are T2+ capabilities, not T1 add-ons. Six accounts moved from T1 to T2 via CPQ, one via CC. Stack labels now explicitly include CPQ, CC, and Flipbook. Addon charges eliminated (CPQ/CC included in T2+).

5. **Tightened included-user allocation (v4).** Per-tier sensitivity sweep revealed the v3 allocation of 15/25/50 was suboptimal — T2 at 25 users captured only $983/mo from 4 accounts (75% had all users free). v4 tightens to T1: 10, T2: 15, T3: 40. Supported by `2026-04-15__tier_pricing_stress_test__v1.md` (5-scenario comparison) and `2026-04-15__included_user_sensitivity__v1.md` (granular per-tier sweep with marginal revenue curves).

6. **Brand charges removed from default path (v5).** D-004c stress test concluded brand pricing is consolidation-only. The multi-org discount is sunset at the account level (Path B). Brand pricing at 90% of natural tier ($674/$1,166/$2,066) is available as a reactive entity-level consolidation option — modeled in `entity_migration_table.py`. Only 1 account affected (Wildwood/Chelsea House, -$1,495).

##### Migration Revenue Drivers

Every account is classified by the primary mechanism behind its price change. This is the analytical lens for understanding *why* the migration produces ~$30k/mo in lift — and where the structural costs are.

| Driver | Accounts | Δ MRR | Avg/Acct | What it means |
|---|---:|---:|---:|---|
| `user_rate_normalization` | 46 | **+$15,290** | +$332 | Legacy $15–$20/user moving to graduated $25/$22/$20/$18. Largest driver. |
| `discount_correction` | 33 | **+$14,502** | +$439 | Legacy base/module discounts being normalized to book. |
| `multi_org_retirement` | 9 | +$3,213 | +$357 | 10% multi-org discount being eliminated. Concentrated in entity accounts. |
| `at_book_tier_shift` | 6 | +$239 | +$40 | Accounts already at/near book rate. $725→$749 produces a small, zero-friction increase. |
| `user_count_variance` | 2 | **-$941** | -$471 | Current MRR reflects averaged billing; new pricing uses a snapshot. |
| `module_compression` | 8 | **-$1,923** | -$240 | Tier absorbs formerly separate modules (Catalog $295, Closed $100). By design — the structural cost of packaging simplification. |

**Strategic read:** The gross lift is +$33,244/mo from user rate normalization + discount correction + multi-org retirement. The structural cost is -$2,864/mo from module compression + user count variance. The net +$30,380/mo reflects the difference. Multi-org retirement (+$3,213) is a distinct driver — it represents the sunset of the 10% entity-level discount. Brand pricing at 90% is available as a reactive entity-level lever but does NOT reduce these account-level deltas on the default path.

> **Revised 2026-04-15 (v5)**: v4 showed `brand_captured` as a secondary driver for multi-site accounts — removed in v5 because brand charges are consolidation-only. Wildwood/Chelsea House reclassified from user_rate_normalization to user_count_variance (delta flipped from +20% to -24% after brand charge removal).

##### Risk-Adjusted Scenarios (migration-induced churn)

| Scenario | Accounts Lost | Net MRR | Net ARR | vs Current |
|---|---:|---:|---:|---:|
| Conservative | 8 | $156,576 | $1,878,912 | **+5.4%** |
| Expected | 4 | $167,230 | $2,006,760 | **+12.5%** |
| Optimistic | 1 | $175,863 | $2,110,356 | **+18.3%** |
| No churn + all 12 rollups consolidate | 0 | $176,850 | $2,122,200 | **+19.0%** |

Churn rates by risk cohort: 0% for all decrease/flat accounts. 2%/1%/0% for flat, 5%/2%/1% for modest, 10%/5%/2% for moderate, 15%/8%/3% for significant (conservative/expected/optimistic). Churn removes the highest-MRR accounts first within each cohort (worst-case assumption).

Even in the conservative scenario (8 accounts lost), the migration is MRR-positive (+$7,978/mo). The expected scenario delivers +$18,632/mo (+$224k/yr) from install-base migration alone. The no-churn baseline ($178,978) with full entity consolidation ($176,850) retains 93% of the refresh delta.

> **Revised 2026-04-15 (v5)**: v5 is modestly below v4 across all scenarios (-$410 to -$1,495) due to Wildwood brand charge removal. Added entity consolidation overlay row — if all 12 rollup entities consolidate (worst case), $2,128/mo leaks and 93% of the delta is retained.

##### Decrease Account Policy (Workstream D Input)

10 accounts (10% of base) would see a price decrease under raw tier pricing, totaling -$2,864/mo (-$34,368/yr). Whether to pass through reductions or hold at current rate is a **Workstream D decision**.

| Category | Accounts | MRR Erosion | Nature | Workstream D Lever |
|---|---:|---:|---|---|
| Module compression | 8 | -$1,923 | By design — tier absorbs legacy modules | Floor pricing holds these at current |
| User count variance | 2 | -$941 | Methodology artifact (snapshot vs average) | Trailing 6-month average resolves |

> **Revised 2026-04-15 (v5)**: v5 adds Wildwood/Chelsea House to the decrease cohort (-$817, -24%) because its $1,495 T3 brand charge was removed from the default path (brand pricing is consolidation-only). Total decrease accounts: 22 (v1) → 20 (v2) → 16 (v3) → 9 (v4) → 10 (v5). The v5 increase is a policy change, not a pricing error.

Floor variant analysis saved separately — see `03_data/migration_revenue_model__floor_variant.py`.

#### Migration Risk Profile

| Bucket | Accounts | % | Assessment |
|---|---:|---:|---|
| Decrease (>10%) | 5 | 5% | Module compression + brand charge removal (Wildwood) — Workstream D policy |
| Decrease (0–10%) | 5 | 5% | Near-parity; zero-friction migration |
| Flat (0–10%) | 16 | 15% | No conversation needed |
| Modest (10–20%) | 21 | 20% | "You gain 6–8 new capabilities for $100–200/mo more" |
| Moderate (20–30%) | 21 | 20% | Requires value narrative; manageable. 13 of 21 are T3 accounts from 50→40 tightening. |
| Significant (>30%) | 36 | 35% | Legacy discounts + CPQ/CC tier corrections + user tightening — migration sequencing, not pricing |

> **Revised 2026-04-15 (v5)**: Decrease cohort: 22 (v1) → 20 (v2) → 16 (v3) → 9 (v4) → 10 (v5). Wildwood enters >10% Decrease from Moderate (brand charge removed, -24%). Moderate decreases by 1 (22→21). All other cohorts unchanged. Total decrease MRR: -$6,526 → -$3,509 → -$3,065 → -$2,047 → -$2,864.

26% of accounts see a decrease or <10% increase — zero-friction migration. 46% see ≤20% increase. The 36 accounts with >30% increase include multi-org entities (Godinger, HVLG, WAC, Generation Brands) and accounts with deep legacy discounts — these require entity-level conversations and the four-wave migration approach. See barbell analysis in migration revenue model v5.

##### Migration Narratives by Risk Cohort

| Cohort | Accounts | Core Narrative | Conversation Approach |
|---|---:|---|---|
| Decrease (>10%) | 5 | "You save money and get more capabilities." | Retention win. Workstream D decides whether to pass through or hold. Wildwood is a policy-driven decrease (brand charges removed). |
| Decrease (0–10%) | 5 | "Your price stays roughly the same, with new features included." | Straightforward. Near-parity accounts. |
| Flat (0–10%) | 16 | "Modest adjustment with 6–8 new capabilities." | Lead with platform value expansion. |
| Modest (10–20%) | 21 | "$100–200/mo more for a significantly expanded platform." | Standard migration. Value narrative required but not contentious. |
| Moderate (20–30%) | 21 | "Account-owner-led conversation required." | 13 of 21 are T3 accounts from 50→40 user tightening — conversation is about 10 fewer included users. Remaining 8 are discount correction and user rate normalization. |
| Significant (>30%) | 36 | "High-touch migration — entity-level or executive conversation." | Four-wave approach. 5 accounts with >100% increase are phased-increase candidates (50% year 1, full year 2). 11 new v4 entrants are T1 accounts with $75–$125/mo incremental user charges — straightforward value narrative. |

#### Multi-Org Entity View — Path B (Consolidation-Only Brand Pricing)

v5 implements **Path B**: the multi-org discount is sunset at the account level. Each account pays full tier + users on the default migration path. Brand pricing at 90% of natural tier is available as a **reactive entity-level consolidation option** — not proactively applied. This creates two migration scenarios for multi-org entities.

##### All Rollup Entities with Consolidation Option (12 entities, 30 accounts)

All 12 rollup entities have a consolidation option — each could consolidate to 1 platform + N-1 brands at 90% of natural tier. 5 of 12 also have a multi-org discount being retired.

| Entity | Brands | Multi-Org | Current | Default (v5) | Δ Default | Consol | Saving |
|---|---:|---:|---:|---:|---:|---:|---:|
| Gabriella White | 4 | 10% | $9,156 | $11,287 | +23% | $10,600 | $687 (6.1%) |
| Generation Brands | 3 | 22.5% | $3,955 | $5,701 | +44% | $5,551 | $150 (2.6%) |
| Interlude Home | 2 | — | $3,572 | $4,590 | +28% | $4,361 | $229 (5.0%) |
| Abaline | 2 | — | $3,414 | $3,815 | +12% | $3,686 | $129 (3.4%) |
| WAC | 2 | 10% | $3,311 | $4,414 | +33% | $4,339 | $75 (1.7%) |
| Theodore Alexander | 2 | — | $3,193 | $3,590 | +12% | $3,461 | $129 (3.6%) |
| Baker Interiors | 3 | 10% | $3,015 | $3,663 | +22% | $3,513 | $150 (4.1%) |
| Coleto Brands | 2 | — | $2,880 | $3,408 | +18% | $3,333 | $75 (2.2%) |
| Jonathan Charles | 2 | — | $2,808 | $3,590 | +28% | $3,461 | $129 (3.6%) |
| Godinger Silver Art | 4 | — | $1,862 | $3,897 | +109% | $3,672 | $225 (5.8%) |
| Century Furniture | 2 | 10% | $1,305 | $1,498 | +15% | $1,423 | $75 (5.0%) |
| HVLG | 2 | — | $816 | $2,646 | +224% | $2,571 | $75 (2.8%) |
| **TOTAL** | **30** | | **$39,288** | **$52,099** | **+33%** | **$49,971** | **$2,128 (4.1%)** |

Consolidation saves $2,128/mo total across all 12 entities — 7.0% of the v5 refresh delta. Even if all 12 entities consolidate, **93% of the delta is retained.** Per-entity savings range from 1.7% to 6.1% — all well within the 10% multi-org ceiling.

##### Standalone Multi-Org Accounts (6 accounts, no consolidation option)

| Account | Multi-Org | Current | Default (v5) | Δ | Risk | Driver |
|---|---:|---:|---:|---:|---|---|
| RENWIL | 22% | $2,114 | $2,721 | +$606 (+29%) | Moderate | user_rate_normalization |
| Donald Choi Canada | 22% | $1,836 | $1,295 | -$542 (-30%) | Decrease | module_compression |
| Maxim Lighting | 10% | $1,603 | $2,135 | +$532 (+33%) | Significant | multi_org_retirement |
| Tomlinson Companies | 20% | $1,120 | $749 | -$371 (-33%) | Decrease | module_compression |
| EGLO Canada | 10% | $652 | $999 | +$347 (+53%) | Significant | multi_org_retirement |
| Visual Comfort Europe | 10% | $652 | $874 | +$222 (+34%) | Significant | multi_org_retirement |

These accounts receive multi-org discount but have no sibling brands to consolidate with. The discount is retired with no replacement mechanism.

> **Revised 2026-04-15 (v5)**: Multi-org entity view fully restructured for Path B. All 12 rollup entities now shown with consolidation economics — not just the 5 with multi-org discounts. 5 of 12 have multi-org discount being retired; the other 7 have no legacy discount but still have the consolidation option available reactively. 6 standalone multi-org accounts have discount retirement but no consolidation option. Full entity migration table: `03_data/extracts/2026-04-15__entity_migration_table__v1.csv`.

#### Migration Pacing

Migration window: Q3 2026 (50% migrated) → Q4 2026 (80%) → Q5 2027 (100%). Revised from Q3=80%/Q4=100% to reflect the four-wave migration approach recommended by the barbell analysis. Q1 and Q2 are pre-migration (current pricing, background churn only). Quarterly background churn: 0.53% (from 97.9% annual retention).

Migration-only quarterly bridge (expected scenario):

| Quarter | MRR | ARR Run Rate | vs Baseline |
|---|---:|---:|---:|
| Q0 (Mar 2026) | $148,598 | $1,783,181 | baseline |
| Q1 (Jun 2026) | $147,811 | $1,773,730 | -$788 |
| Q2 (Sep 2026) | $147,027 | $1,764,329 | -$1,571 |
| Q3 (Dec 2026) | $155,941 | $1,871,296 | +$7,343 |
| Q4 (Mar 2027) | $160,997 | $1,931,966 | +$12,399 |
| Q5 (Jun 2027) | $164,050 | $1,968,600 | +$15,452 |

Year-end 2026 ARR run rate (migration only): ~$1.87M.

> **Revised 2026-04-15 (v5)**: v4 bridge was modestly higher due to Wildwood brand charge. v5 removes brand charges from default path — impact is -$1,495/mo phased through the migration window. All other dynamics unchanged.

---

#### Comprehensive Revenue Impact (migration + new logos + expansion)

Full model: `03_data/2026-04-15__revenue_impact_model__v5.md`
Migration narrative: `03_data/2026-04-15__migration_revenue_model__v5.md`

The comprehensive model layers four components on the migration baseline. This is the full forward-looking revenue projection under the new pricing architecture.

| Component | Mechanism | Revenue Character |
|---|---|---|
| **Install-base migration** | 104 accounts repriced to new tiers | One-time lift, then decays with background churn |
| **New logo acquisition** | New customers at new tier pricing | Recurring quarterly additions |
| **User expansion** | Organic growth in billable users | Automatic — no sales effort; compounds quarterly |
| **Tier upgrades** | T1→T2 and T2→T3 conversions | Expansion revenue from existing accounts |

Brand expansion and integration hosting are excluded (Workstream D).

##### Assumptions (Expected Scenario)

| Parameter | Value | Rationale |
|---|---|---|
| New logos / quarter | 3 (12/yr) | Matches 2023-2025 observed pace |
| New logo tier mix | 65% T1 / 20% T2 / 15% T3 | Shift toward T2 as hero tier |
| T1→T2 upgrades / quarter | 2 | From ~19 behaviorally Commerce-Active T1 accounts |
| T2→T3 upgrades / quarter | 0.5 | Rarer; ~1 every two quarters |
| Quarterly user growth | 2% | Modest organic growth; no sales effort required |
| Migration-induced churn | 3 accounts | Risk-cohort-based (see migration model) |

**New logos:** Recent pace (2023-2025) is ~12/year. Conservative (8/yr) assumes slight decline; optimistic (16/yr) assumes acceleration from improved pricing clarity and sales enablement. Tier mix shift toward T2 is the primary ARPU lever — every new logo at T2 vs T1 adds $546/mo in recurring revenue.

**Tier upgrades:** ~19 current accounts are behaviorally Commerce-Active (using Cart/Portal features) but modularly T1 — they're *doing* commerce without *paying for* it. This is the T1→T2 conversion pipeline. Expected assumes converting 2/quarter, which adds ~$600/mo per conversion.

**User growth:** 2%/quarter organic growth reflects natural team expansion at customer accounts. Revenue materializes automatically through graduated excess-user billing — no sales motion required.

##### Year-End ARR Run Rates (All Scenarios)

| Metric | Current | Conservative | Expected | Optimistic |
|---|---:|---:|---:|---:|
| Year-end 2026 ARR | $1,783,181 | $1,889,088 | **$2,005,932** | $2,174,036 |
| Year-end 2027 ARR | $1,783,181 | $1,998,014 | **$2,252,497** | $2,617,938 |
| Δ ARR (vs current) | — | +$215k (+12.0%) | **+$469k (+26.3%)** | +$835k (+46.8%) |

> **Revised 2026-04-15 (v5)**: Comprehensive revenue impact model now uses v5 migration baseline ($178,978 no-churn). v5 expected year-end 2027 ARR: **$2,252,497** — a +$58K improvement over v3's $2,194,457. The v5 migration baseline is $8,295/mo stronger than v3 ($9,790 from user tightening, -$1,495 from brand charge removal).

##### Revenue Components at Q7 (Expected)

| Component | MRR | % | ARR | Growth Character |
|---|---:|---:|---:|---|
| Install-base (migrated) | $162,847 | 87% | $1,954,168 | Decaying (bg churn erodes ~$870/mo) |
| New logos (cumulative) | $16,016 | 9% | $192,192 | Accumulating (+$2,793/quarter net of churn) |
| Tier upgrades | $5,905 | 3% | $70,855 | Accumulating (+$857/quarter net of churn) |
| User expansion | $3,279 | 2% | $39,348 | Compounding (grows with installed base) |
| **Total** | **$188,047** | **100%** | **$2,256,563** | |

##### Key Dynamics

1. **Migration dominates near-term.** 87% of Q7 MRR in expected scenario. Getting migration sequencing, Workstream D policy decisions, and entity-level conversations right matters more than any other single lever. The v5 barbell analysis (57 accounts with >20% increases) demands careful four-wave sequencing. For the 5 multi-org rollup entities, the entity migration table provides consolidation economics as a reactive conversation tool.

2. **New logo tier mix is the primary ARPU lever.** T1 starting ARPU ($749) is simplified but comparable to legacy. T2 ($1,295) and T3 ($2,295) are meaningfully higher than the old stacked-module equivalent. Shifting acquisition toward T2 as the "hero tier" is the single largest new-logo ARPU lever.

3. **T2 is now a real install-base tier.** v3 moved T2 from 9 to 16 accounts via CPQ/CC corrections. v4's tighter user allocation (25→15) doubled T2's user revenue from $983 to $2,134/mo and increased T2's delta from +$1,935 to +$3,086. The upgrade pipeline (behaviorally Commerce-Active T1 accounts) reduced from ~19 to ~12, but is replenished by new T1 logos.

4. **User expansion compounds passively.** 2%/quarter organic growth materializes automatically through graduated excess-user billing with no sales effort. By Q7, this contributes $4,166/mo — small in isolation but permanently accretive.

5. **Conservative now exceeds $2M ARR by year-end 2027.** Even with 8 new logos/year, 1 upgrade/quarter, 1% user growth, and 8 migration-induced churns, the model reaches **$2.0M ARR** by year-end 2027 (+$215k vs current).

6. **Upside optionality excluded.** Brand expansion, integration hosting, and floor pricing policy are additional revenue streams addressed in Workstream D. Each represents incremental ARR not captured in these projections.

#### Positioning Choices

**T1 at $749 (not $725 or $795)**: $725 would signal "no change" and miss the Online Catalog inclusion value narrative. $795 widens the AmpTab sticker gap uncomfortably. $749 is "just above book" — signals value without triggering resistance.

**T2 at $1,295 (not $1,195 or $1,395)**: T2 is the hero tier, priced for adoption. Below the revealed median ($1,414) means most current T2-equivalent accounts pay *less* than today. T2 shows -7% on the 9 legacy accounts — acceptable because T2 should capture the majority of new customers.

**T3 at $2,295 (not $1,995 or $2,495)**: $1,995 makes the median T3 account decrease (-8%) — too generous. $2,495 pushes the median to +16% — defensible but harder across 34 accounts with concurrent support commitments. $2,295 lands a balanced position. With the revised 40 included users (tightened from 50 in v4), the median T3 account sees a moderate increase — manageable given the 8+ new capabilities included.

---

### D-004b: User Expansion Pricing — STAMPED 2026-02-25

Full analysis: `11_synthesis/2026-02-25__user_discount_curve__d004b__v1.md`

#### Included-User Allocations — Revised to 10/15/40

The original M3 allocations (15/25/50) were validated in D-004b against v1 tier assignments (T1: 61, T2: 9, T3: 34). The v3 product audit moved 7 accounts from T1 to T2 via CPQ/CC, fundamentally changing the T2 composition. A per-tier sensitivity sweep (`2026-04-15__included_user_sensitivity__v1.md`) revealed the allocations needed tightening. **Revised allocation: 10/15/40.**

| Tier | Original | Revised | Median Users | % Expanding | User MRR Captured | v3→v4 Δ |
|---|---:|---:|---:|---:|---:|---:|
| T1 | 15 | **10** | 24 | 78% (42/54) | ~$25.8K/mo | +$4,210 |
| T2 | 25 | **15** | 16 | 50% (8/16) | ~$2.1K/mo | +$1,151 |
| T3 | 50 | **40** | 50 | 65% (22/34) | ~$11.9K/mo | +$4,429 |

**T1 at 10** (was 15): The marginal $/user-dropped curve accelerates below 15 — each user removed is worth $898/user (12→10) vs $744/user (18→15). Captures 78% of T1 accounts for expansion (vs 65% at 15). The 11 additional accounts in the Sig>30% band are rate-architecture-correction accounts with the clearest migration narrative.

**T2 at 15** (was 25): The headline finding. 75% of T2 accounts had ≤25 users — the v3 allocation generated just $983/mo from only 4 accounts. At 15u, 50% pay and user revenue doubles to $2,134/mo. The marginal curve has a clear inflection at 15 ($96/user above, $153+/user below). Risk delta: only 3 accounts worsen. This is effectively risk-free revenue.

**T3 at 40** (was 50): Captures 65% of T3 accounts (vs 47%). The Sig>30% count stays flat at 2 and decrease accounts drop to zero. The T3 value proposition is deep feature access — user expansion at the margin, not the core. $456/user-dropped with no incremental risk.

**Supporting analysis:** `2026-04-15__tier_pricing_stress_test__v1.md` validated that the user lever is more risk-efficient than the price lever ($191/worsened-account for users vs $222 for price). `2026-04-15__included_user_sensitivity__v1.md` provides the full per-tier marginal revenue curves and "knee in the curve" analysis.

#### Discount Curve — Proposed

Step-declining rate, **uniform across tiers** (tier differentiation handled by included-user allocation, not per-user rate):

| Excess Users | Rate/User/Mo | Book Discount | Monthly Example |
|---|---:|---:|---|
| 1–10 | **$25** | 0% | 5 excess = $125/mo |
| 11–25 | **$22** | 12% | 20 excess = $250 + $220 = $470/mo |
| 26–50 | **$20** | 20% | 40 excess = $250 + $330 + $300 = $880/mo |
| 51+ | **$18** | 28% | 75 excess = $250 + $330 + $500 + $450 = $1,530/mo |

**Design rationale:**

1. **First 10 at book ($25)**: No discount for small overages. A 5-user overage at $125/mo is psychologically trivial relative to a $749+ platform fee. Preserves rate integrity.
2. **11–25 at $22**: First volume break. Formalizes the negotiated discount that most mid-size accounts have already achieved. Average effective rate for a 20-user overage = $23.50.
3. **26–50 at $20**: Matches the revealed effective rate across the install base. Removes negotiation friction — the published rate is what accounts have historically been paying.
4. **51+ at $18**: Deep discount for the largest teams (5–10 accounts). Even at 100 excess users, SuperCat T3 total ($2,295 + $1,530 = $3,825) approaches but does not dramatically exceed AmpTab Pro ($3,000). The Y1 setup-fee-adjusted comparison remains favorable.
5. **Graduated/marginal rates (not flat-rate-at-total)**: Each tranche is billed at its own rate — the $22 rate applies only to users 11–25, not retroactively to users 1–10. This is a deliberate structural choice with three consequences: (a) **No cliff effect** — adding user #11 does not retroactively reduce the per-user cost of users 1–10, so SuperCat never loses revenue from volume growth; (b) **Strictly increasing cost curve** — there is no scenario where adding more users lowers the total bill, eliminating perverse incentives to over-provision; (c) **Transparent volume reward** — customers see exactly where each dollar goes and how additional volume earns a better marginal rate, which is more defensible in enterprise procurement conversations than an opaque "you get $20/user because you have 30" flat rate. The monthly examples in the table above reflect graduated billing (e.g., 20 excess = $250 + $220 = $470, not 20 × $22 = $440).

**Alternatives rejected:**

- **Tier-differentiated rates** (higher at T1, lower at T3): +~$2K/mo marginal revenue, but introduces three rate cards, complicates invoicing, and creates a confusing "my users got cheaper when I upgraded" experience. Tier differentiation belongs in the included base, not the marginal rate.
- **Block pricing** (buy blocks of 5/10/25/50): Stress-tested in depth (2026-01-28). Blocks map elegantly to the step-declining curve but are rejected for this vertical because: (1) block ceilings create friction when adding users — a go-to-market tool should never gate a rep's access behind an admin purchasing decision; (2) seasonal sales forces (common in wholesale/B2B) would need to buy and drop blocks as they scale for market months, making blocks cumbersome on any cadence shorter than annual; (3) "paying for unused seats" in partially filled blocks conflicts with competitive conditioning and customer expectations. The committed floor + arrears overage model (see billing mechanics stress test above) captures the predictability benefits of blocks without these drawbacks.

#### Competitive Positioning

| Volume | SuperCat | RepZio | Pepperi Pro | Onsight | Market Avg |
|---|---:|---:|---:|---:|---:|
| 1–10 excess | **$25** | $25 | $48 | $65 | $40–50 |
| 11–25 | **$22** | $25 | $48 | $65 | $40–50 |
| 26–50 | **$20** | $25 | $48 | $65 | $40–50 |
| 51+ | **$18** | $25 | $48 | $65 | $40–50 |

SuperCat is at or below RepZio at every volume level, and 50–72% below the market average. The highest marginal rate ($25 for first 10) is 48% below Pepperi Pro ($48) — a powerful competitive message.

#### Revenue Impact (at stamped tier prices $749/$1,295/$2,295, tightened allocation 10/15/40)

| Component | Current | New (v5) | Delta |
|---|---:|---:|---:|
| Platform MRR | $113,945 | $139,196 (78%) | +$25,251 (+22%) |
| User MRR | $34,653 | $39,782 (22%) | +$5,129 (+15%) |
| Brand MRR (default path) | — | $0 (0%) | — |
| **Total MRR** | **$148,598** | **$178,978** | **+$30,380 (+20.4%)** |
| **Total ARR** | **$1,783,181** | **$2,147,736** | **+$364,555** |

> **Revised 2026-04-15 (v5)**: Brand MRR is $0 on the default migration path — brand pricing (D-004c) is consolidation-only (Path B). Revenue mix is 78/22 (platform/users) — a clean two-component model on the default path. The v4 allocation of 10/15/40 restores user MRR to 22% of the mix (close to the current 23%), preserving the expansion mechanic that drives NRR.

#### Open Items

| Item | Status | Notes |
|---|---|---|
| Billing mechanics (arrears vs. committed) | **Deferred — see stress test below** | Committed floor model validated as superior; deferred to subsequent pricing iteration to limit migration scope |
| Rate card publication | Open | Published builds trust; unpublished preserves negotiation flexibility |
| Upgrade user-count recalculation | Recommended: yes | Expanding included base on tier upgrade creates immediate relief — makes upgrades feel rewarding |

#### Billing Mechanics Stress Test (2026-01-28)

**Context**: D-000a Problem 1 identifies arrears billing as harmful to both SuperCat (impaired cash flow predictability) and customers (unpredictable costs). D-004b stamped the pricing (rate curve) but left billing mechanics open.

**Models evaluated:**

| Model | Description | Verdict |
|---|---|---|
| **A: Arrears** (status quo) | Count at month-end, bill exact actuals | Retains all current problems but zero migration complexity |
| **B: Committed Floor + Arrears Overage** | Customer commits to a user floor (trough); floor billed at committed rate; users above floor billed at rack rate in arrears; floor ratchets up only | **Best fit for seasonal vertical SaaS** — handles seasonality naturally, zero growth friction, revenue-identical to pure arrears |
| **C: User Blocks** | Buy fixed-size blocks (10/15/25/50 users) mapped to the step-declining curve | **Rejected** — block ceilings create friction when adding users mid-season; seasonal buy/drop cycle is cumbersome; "paying for unused seats" conflicts with competitive conditioning |
| **D: Committed Count** | Commit to exact additional user count annually with true-up | Strongest predictability but weakest seasonality handling; enterprise-oriented, may feel heavy for SMB segment |

**Key finding — SuperCat already operates Model B for annual arrangements:**

Existing annual contract user billing (from current service agreements):
- Base package: 25 users included in annual platform licensing fee
- Customer declares estimated total monthly active users at contract signing
- Annual fee includes prepaid additional users at $25/user/month for declared amount above base
- Quarterly reconciliation: average of prior quarter's monthly active users [(M1 + M2 + M3) ÷ 3]
- Overage: $30/user/month for each user above declared estimate (20% premium over committed rate)

This is precisely the Committed Floor + Arrears Overage model — with the "declared estimate" as the floor, $25 as the committed rate, $30 as the overage rate (20% premium), and quarterly averaging to smooth seasonality.

**Install base modeling** (floor at 80% of current excess): ~80% of user MRR ($22.8K of $28.5K/mo) becomes predictable; 20% remains variable overage. Total revenue is identical to pure arrears — the mechanic change does not leave money on the table.

**Decision: Defer to subsequent pricing iteration.**

Rationale: This iteration already touches tier structure, tier pricing, user rates, brand pricing (entirely new concept), à la carte modules, annual vs. monthly, and discounting guardrails. Adding a billing mechanics change (requiring billing system updates, sales training, customer communications) increases execution risk for a marginal gain. The step-declining curve is intentionally designed to support either arrears or committed floor billing — the architecture accommodates transition without structural changes.

**Guard rails for future iteration:**
1. The step-declining curve ($25/$22/$20/$18) is confirmed to work as either a per-user arrears rate or a committed floor rate structure.
2. The existing annual arrangement billing model (declared estimate + quarterly reconciliation + overage premium) provides a proven template for the committed floor transition.
3. D-004e (annual vs. monthly pricing) can offer voluntary annual user count commitments as a predictability option for customers who proactively want it — serving as a soft pilot.
4. When billing mechanics transition occurs, the overage premium (currently 20% / $30 vs. $25) should be recalibrated against the new step-declining curve rates.

---

### D-004c: Per-Brand Pricing — STAMPED (v2) 2026-02-25

**Natural-tier per-brand pricing at 90% of book (10% discount): $674 / $1,166 / $2,066 per additional brand. 1 brand included per tier (all tiers). Consolidation-only — not applied on default migration path (Path B).**

> **Revision history**: v1 (flawed) proposed $295/mo flat with 1/3/5 included brands — would wipe out 93% of refresh delta. v2 corrected with tier-scaled rates ($495/$895/$1,495) at ~66% of governing tier and 1-brand allocation. v4 stress test (2026-04-15) revealed two structural flaws in v2: the governing tier rule punishes 4 of 12 mixed-tier entities and produces outsized savings for T3-heavy entities. **v4/v5 revision:** natural-tier pricing at 90% of book ($674/$1,166/$2,066) — each brand priced at a 10% discount from its own tier, directly mirroring the legacy multi-org discount being retired. **v5 policy decision (Path B):** brand pricing is reactive/consolidation-only. Not applied on the default account-level migration path. Multi-org discount is sunset at the account level. Brand pricing is available as an entity-level consolidation lever for all 12 rollup entities (5 of which also have a multi-org discount being retired). Full analysis: `03_data/2026-04-15__brand_pricing_stress_test__v1.md`.

#### Foundational Reframe: Brands Are Business Units

The v1 error was treating brands as a catalog configuration ($295 add-on anchored to the Online Catalog module price). A brand on SuperCat is a **business unit** that consumes: its own product catalog (data, media, sync), separate customer/dealer relationships, separate order flows, separate reporting, and often separate sales teams. It shares admin infrastructure with the primary brand but drives full platform value.

**Revealed per-brand value** across the 12 multi-instance entities ranges from **$408 to $2,289/mo**. The v1 rate of $295 was below the floor of observed willingness-to-pay. Every entity currently pays more per brand than v1 proposed to charge.

#### Per-Brand Rate Structure

| Tier | Platform Price | Brand Rate (v2) | Brand Rate (proposed) | % of Tier | Rationale |
|---|---:|---:|---:|---:|---|
| **T1** Catalog Essentials | $749/mo | $495/mo | **$674/mo** | 90% | 10% discount from tier — mirrors the legacy multi-org discount, applied per-brand |
| **T2** Commerce Professional | $1,295/mo | $895/mo | **$1,166/mo** | 90% | Same principle — each brand priced at its natural tier with a 10% shared-infrastructure discount |
| **T3** Commerce Enterprise | $2,295/mo | $1,495/mo | **$2,066/mo** | 90% | Same principle — a T3 brand is an enterprise operation, 10% discount |

> **Stress test revision (2026-04-15):** Rates revised from ~66% governing-tier to **90% natural-tier (10% discount from book)**. The governing tier rule (all brands priced at the highest tier in the entity) is retired in favor of natural-tier pricing (each brand priced for the capabilities it actually consumes). The 10% discount directly replaces the legacy 10% multi-org discount. See `03_data/2026-04-15__brand_pricing_stress_test__v1.md`.

Rates are tier-scaled because the value delivered per brand depends on the capabilities enabled. Each brand is priced at 90% of its natural tier — a 10% discount that mirrors the legacy multi-org discount being retired. The narrative: "We're retiring the entity-level discount. Each additional brand on a consolidated instance receives a 10% discount from its tier price."

Production rounding: $674/$1,166/$2,066 are exact 90%. May round to $675/$1,165/$2,065 (nearest $5) or $675/$1,170/$2,070.

#### Included Brand Allocation: 1 Per Tier (All Tiers)

**Revised from 1/3/5.** Three reasons:

1. **Eliminates implicit giveaway.** At $1,495/brand, T3's old 5-brand allocation implicitly bundled $5,980 of brand value — making a 5-brand T3 identical in price to a 1-brand T3 despite 5× the platform value consumed.
2. **Closes rate card arbitrage.** Under v1 (1/3/5), Gabriella White (4 brands, T3) would pay $0 in brand charges because 4 ≤ 5 included. Under v2 (1/1/1), GW pays 3 × $1,495 = $4,485 in brand charges.
3. **Clean separation of value dimensions.** Tiers differentiate on features and included users. Brands are a separate axis. The vast majority of customers (74 of 104) are single-brand — the included allocation is irrelevant to them.

#### Multi-Brand Landscape and Impact

12 of 86 entities (14%) operate multiple brands across 2–4 separate instances. These 30 accounts represent 26% of total MRR ($39,288/mo).

| Entity | Brands | Mixed? | Current MRR | Non-consol | Consol (proposed) | Δ vs Current | Consol Savings |
|---|---:|---|---:|---:|---:|---:|---:|
| Gabriella White | 4 | No | $9,156 | $11,287 | $10,600 | +$1,444 (+16%) | $687 (6.1%) |
| Generation Brands | 3 | No | $3,955 | $5,701 | $5,551 | +$1,596 (+40%) | $150 (2.6%) |
| Interlude Home | 2 | No | $3,572 | $4,590 | $4,361 | +$788 (+22%) | $229 (5.0%) |
| Abaline | 2 | YES | $3,414 | $3,815 | $3,686 | +$272 (+8%) | $129 (3.4%) |
| WAC | 2 | No | $3,311 | $4,414 | $4,339 | +$1,028 (+31%) | $75 (1.7%) |
| Theodore Alexander | 2 | YES | $3,193 | $3,590 | $3,461 | +$268 (+8%) | $129 (3.6%) |
| Baker Interiors Group | 3 | YES | $3,015 | $3,663 | $3,513 | +$498 (+17%) | $150 (4.1%) |
| Coleto Brands | 2 | No | $2,880 | $3,408 | $3,333 | +$453 (+16%) | $75 (2.2%) |
| Jonathan Charles | 2 | YES | $2,808 | $3,590 | $3,461 | +$653 (+23%) | $129 (3.6%) |
| Godinger Silver Art | 4 | No | $1,862 | $3,897 | $3,672 | +$1,810 (+97%) | $225 (5.8%) |
| Century Furniture | 2 | No | $1,305 | $1,498 | $1,423 | +$118 (+9%) | $75 (5.0%) |
| HVLG | 2 | No | $816 | $2,646 | $2,571 | +$1,755 (+215%) | $75 (2.8%) |
| **TOTAL** | **30** | | **$39,288** | **$52,099** | **$49,971** | **+$10,683 (+27%)** | **$2,128 (4.1%)** |

> **Revised 2026-04-15 (v4 stress test)**: Table reflects the proposed model: natural-tier brand pricing at 90% of book (10% discount) + per-brand included users (no pooling). Key changes from prior version:
> - **Governing tier retired**: Brand rates are no longer forced to the highest tier in the entity. Each brand is priced at 90% of its own natural tier — a 10% discount that directly mirrors the legacy multi-org discount being retired.
> - **Per-brand included users**: Each brand carries its own tier's included-user allocation, consistent with how multi-instance entities operate today. No pooling assumption or overlap estimate needed.
> - **All 4 mixed-tier penalties eliminated**: Abaline, Theodore Alexander, Baker Interiors, and Jonathan Charles all show modest savings (3-4%) instead of consolidation penalties.
> - **Consolidation savings tightened**: All 12 entities fall within a 2-6% range — well within the 10% multi-org discount ceiling. No entity exceeds the ceiling.
> - **Refresh delta retained**: **93%** under the proposed model (up from 86% under Gov@66%).

*Non-consolidated is the default migration path — each instance priced independently at its natural tier. Consolidated uses natural-tier brand rates at 90% of book (10% discount) with per-brand included-user allocations (consistent with how multi-instance entities operate today — each brand carries its own included users, no pooling).*

**Key structural property**: Even in the worst case (all 12 entities consolidate), revenue grows +27% above current. Consolidation savings range from 2% to 6% — all well within the legacy 10% multi-org discount level. Zero entities are punished for consolidating. Zero entities exceed the 10% ceiling.

**Multi-org sunset alignment**: The 10% brand discount directly mirrors the legacy 10% multi-org discount. The multi-org discount can be retired cleanly: "We're retiring the entity-level discount. Each additional brand on a consolidated instance receives a 10% discount from its tier price." No entity receives a more generous consolidation benefit than the legacy discount provided.

**User pooling as targeted migration lever (optional)**: User pooling (where brands share a single included-user allocation with an assumed deduplication) was explored as an alternative. If offered universally, the incremental revenue exposure is ~$369/mo (~$4,400/yr) — negligible. Pooling benefits T1-heavy entities (Generation Brands, WAC) but actually costs T3-heavy entities more. This is a Workstream D migration policy decision — could be offered selectively as an account-level negotiation tool.

**Consolidation not incentivized (Path B)**: Brand pricing is reactive/consolidation-only — not applied on the default migration path. All 12 rollup entities (30 accounts) have a consolidation option available. Consolidation modestly reduces sticker shock (e.g., GW +23%→+16%, Jonathan Charles +28%→+23%, HVLG +224%→+215%) but is not designed to be compelling. Per-entity savings range from 1.7% to 6.1% — insufficient to justify operational effort. The 6 standalone multi-org accounts have no consolidation option — their discount is simply retired.

**Brand count relies on the deployment-based definition.** 5 of 12 entities have ambiguous classifications where channel variants share a brand name (e.g., Summer Classics Wholesale / Contract / Retail). Under the tightened deployment-based definition, each separate catalog instance with its own buyer base counts as a brand — so GW = 4 brands, not 2. Under the prior marketing-based definition, customers could argue as few as 2, creating $89,580/yr of aggregate dispute surface. See brand definition in D-003c above and enforcement guidelines (Workstream D, pending).

#### Gabriella White Detail

GW is the largest entity at 4 brands (all T3) and the critical stress test:

| Scenario | Platform | Brands | Users | Total | vs Current |
|---|---:|---:|---:|---:|---:|
| Current (4 separate instances) | (blended) | — | — | $9,156 | — |
| v5 Default (each priced independently, no brand charges) | $9,180 | $0 | $2,107 | $11,287 | +23% |
| v5 Consolidated — **Nat@90%** (per-brand, reactive) | $2,295 | $6,198 | $2,107 | $10,600 | +16% |
| **v1 flawed** consolidated | $2,295 | $0 | $2,862 | $5,157 | **-44%** |

> **Revised 2026-04-15 (v5)**: Under Path B, GW's default migration is $11,287/mo (+23%) — no brand charges. If GW elects to consolidate, brand pricing at 90% of natural tier applies: $10,600/mo (+16%), saving $687/mo (6.1%). Consolidation is reactive — GW would only see this option if they request it. The saving ($687/mo) is comparable to the legacy 10% multi-org discount (~$916/mo) they currently receive.

Compare to v1 which would have dropped GW to $5,157/mo (-44%).

#### Revenue Impact

**Default migration (v5)** — brand charges are $0 on the default path:

| Component | Current | New (v5) | Delta |
|---|---:|---:|---:|
| Platform (tiers) | (blended) | $139,196 | — |
| Users (D-004b, 10/15/40) | (blended) | $39,782 | — |
| Brands (D-004c, default) | $0 | $0 | — |
| **Total MRR** | **$148,598** | **$178,978** | **+$30,380 (+20.4%)** |
| **Total ARR** | **$1,783,181** | **$2,147,736** | **+$364,555** |

**Worst case** (all 12 rollup entities consolidate):

| Component | Current | New (v5) | Delta |
|---|---:|---:|---:|
| Default migration | $148,598 | $178,978 | +$30,380 |
| Consolidation adjustment (12 rollup entities, Nat@90%, per-brand) | — | — | -$2,128 |
| **Total MRR** | **$148,598** | **$176,850** | **+$28,252 (+19.0%)** |
| **Total ARR** | **$1,783,181** | **$2,122,200** | **+$339,019** |

**93% of the v5 refresh delta is retained** even if all 12 rollup entities consolidate. Compare to v1 which retained only 7%.

> **Revised 2026-04-15 (v5)**: v5 implements Path B — brand charges removed from default path. All 12 rollup entities (30 accounts) have a consolidation option. Total consolidation leakage if all 12 consolidate: $2,128/mo (7.0% of v5 delta). Of these, 5 entities have multi-org discount being retired ($1,137/mo consolidation saving); 7 entities have no legacy discount ($991/mo saving). Per-entity savings range from 1.7% to 6.1% — all within the 10% ceiling.

#### v2 vs v1 Comparison

| Metric | v1 (Flawed) | v2 (Revised) |
|---|---:|---:|
| Brand revenue (worst-case consol) | $3,245/mo | $15,910/mo |
| Consolidation leakage | -$16,187/mo | -$3,522/mo |
| Worst-case total ARR | $1,797,936 | $1,949,916 |
| Refresh delta retained | 7% | 80% |
| GW consolidated | $5,157/mo (-44%) | $9,642/mo (+5%) |
| Revenue protection vs v1 | — | **+$151,980/yr** |

---

### D-004d: À La Carte Premium Schedule — STAMPED 2026-02-25

**Three unpublished, response-only modules priced at 30–50% premium over implied tier cost.**

Full analysis: `11_synthesis/2026-02-25__a_la_carte_premium_schedule__d004d__v1.md`

#### Module Schedule

| Module | Price | Capabilities Included | Implied Tier Cost | Premium |
|---|---:|---|---:|---:|
| **B2B Commerce** | $795/mo | Full T2 increment: B2B Cart, Closed Site, self-service enrollment, contract pricing, gridview, address verification, Order & Invoice Tracking | $546 (T2−T1) | 46% |
| **Sales Intelligence** | $995/mo | T3 analytics cluster: dashboard, territory & performance views, reports & summaries, data export | ~$650 (65% of T3−T2) | 53% |
| **Premium Support** | $495/mo | Priority support SLA, dedicated CSM, executive business reviews | ~$350 (35% of T3−T2) | 41% |

#### Design Rationale

**Why three modules, not individual features**: Capabilities within each tier increment are architecturally and commercially coherent — Cart without Order Tracking is broken; analytics without export is crippled. Selling sub-clusters would create configuration complexity with no buyer benefit. Three modules cover the full tier-differentiation surface.

**Why SI at 53% (slightly above 30–50% ceiling)**: At 50% ($975), T2 + SI = $2,270 — $25 below T3, creating a rational path to skip T3 entirely. At 53% ($995), T2 + SI = $2,290 — essentially identical to T3 ($2,295). The premium is intentionally calibrated so the sales conversation is: *"For $5 more, T3 gives you priority support, a dedicated CSM, and executive reviews. T3 is the obvious choice."*

**Premium Support as Problem 5 lever**: Making priority support + CSM available à la carte at any tier creates the first monetization path for support (Problem 5). A high-touch T1 or T2 account can add Premium Support ($495/mo) without upgrading, generating revenue that offsets their disproportionate support consumption.

#### Tier-Push Economics

The schedule is designed so that any à la carte combination approximating a tier costs more than the tier itself:

| Configuration | Total | vs Equivalent Tier | Sales Narrative |
|---|---:|---:|---|
| T1 + Commerce | $1,544 | +$249 vs T2 (+19%) | "T2 is $249 cheaper AND includes CPQ, PCI, and 10 more users." |
| T1 + Commerce + SI | $2,539 | +$244 vs T3 (+11%) | "You need Commerce and Analytics — that IS T3, and T3 includes CPQ, PCI, CSM, and 35 more users." |
| T2 + SI | $2,290 | -$5 vs T3 (≈0%) | "For $5 more, T3 adds CSM and priority support." |
| T2 + SI + Support | $2,785 | +$490 vs T3 (+21%) | "T3 piecemeal costs 21% more than T3." |

**The only economically rational à la carte purchase** is **T1 + SI ($1,744)** — a prospect with established B2B ecommerce who needs catalog + analytics. No direct tier equivalent; sits between T2 and T3. This is the exact edge case D-003a designed for. No cannibalization: these prospects would not have bought T3 anyway.

> **Updated 2026-03-11**: With CPQ and PCI now included in T2/T3 (per D-003a v2), the tier-push narrative is even stronger. The B2B Commerce à la carte module does NOT include CPQ or PCI — those are separate T1-only à la carte items at $195/mo each. A T1 customer buying Commerce + CPQ + PCI à la carte = $1,185/mo; T2 at $1,295 includes all three plus 10 more users. The piecemeal path is only $110 cheaper but forfeits 10 users — a weak value proposition for the buyer.

#### Operational Guardrails

- **Unpublished**: Not on pricing page, not in public materials
- **Response-only**: Sales does not lead with à la carte; it responds to a specific objection about overlapping capabilities
- **Approval required**: À la carte deals require Sales leadership sign-off
- **Tier migration flag**: Any à la carte customer is flagged for tier migration review when usage evolves
- **Stacking**: À la carte modules stack with per-brand charges and (for T1 only) with CPQ/PCI à la carte options

---

### D-004e: Annual vs. Monthly Pricing — STAMPED 2026-03-11

**Annual and monthly are the same rate. No annual prepay discount.**

Annual commitment is a billing arrangement (committed term + simplified billing), not a pricing tier. There is no published or unpublished annual incentive.

#### Rationale

1. **Market signal**: Recent new logos are choosing annual contracts without requesting or expecting a discount. The market accepts annual commitment at SuperCat's ~$15k ACV as normal.

2. **Cannibalization risk**: The pricing refresh produces +$16,442/mo (+11.1%) in install-base MRR. An 8.3% annual discount (1 month free), if adopted by the majority of accounts during migration, would erode up to 84% of that gain — reducing the effective delta to ~$2,700/mo. The annual incentive would literally eat the pricing refresh it was designed to support.

3. **Seasonality is already solved**: The graduated user pricing curve (D-004b) handles seasonal user fluctuations within an annual framework. Users are billed on actual usage (committed floor + arrears overage for annual contracts), so seasonal spikes and drops are accommodated at the user line — the contract term doesn't need to absorb this.

4. **Legacy context**: The historical bias toward month-to-month was an internal decision to accommodate user seasonality, not a customer demand. With the user pricing mechanics now properly designed, this rationale no longer applies.

#### What Annual Means

| Dimension | Monthly | Annual |
|---|---|---|
| **Rate** | Published rack rate | Same published rack rate |
| **Term** | Month-to-month, 30-day notice | 12-month committed term |
| **Billing** | Monthly invoice | Annual invoice (or quarterly, per customer preference) |
| **Users** | Billed on actual monthly usage | Committed floor at contract signing; quarterly reconciliation; overage at rack rate |
| **Renewal** | Auto-renews monthly | Auto-renews annually at then-current rates |
| **Early termination** | 30-day notice | Remaining term due (standard SaaS) |

#### Migration Application

For install-base accounts migrating to new pricing, annual commitment is NOT paired with a subscription discount. If an account needs a migration incentive, the lever is onboarding/services flexibility (D-004f, Tier 1) — one-time cost concessions that don't erode recurring revenue.

---

### D-004f: Discounting Authority and Guardrails — STAMPED 2026-03-11

**Subscription rates are non-negotiable by default. Implementation and services costs are the primary negotiation surface.**

Discounting has very rarely been necessary in SuperCat's sales history. This policy preserves that discipline while giving Sales a defined toolkit for competitive situations.

#### Tier 1: Onboarding and Services Flexibility (primary lever — Sales discretion)

Sales may reduce or waive one-time fees without escalation:

| Concession | Value | When to Use |
|---|---:|---|
| Waive Guided onboarding | $2,500 | Competitive deal, strategic account |
| Reduce Comprehensive to Guided price | $2,500 | Large subscription commitment, annual term |
| Waive Comprehensive onboarding | $5,000 | Exceptional — T3 annual with strong strategic fit |
| Include Data Assessment | $1,500 | Sweetener for integration-heavy prospects |
| Include Certified Pipeline (Tier B) | $2,500 | Customer with integration need, subscription commitment |

Maximum one-time concession without escalation: **$5,000** (full Comprehensive waiver). Combinations exceeding $5,000 require CEO approval.

These concessions cost SuperCat $1,500–$2,000 in fully loaded labor — effectively a customer acquisition cost amortized over the subscription lifetime. They do not touch recurring subscription revenue.

#### Tier 2: Subscription Discounting (rare exception — CEO approval required)

| Guardrail | Detail |
|---|---|
| **Maximum discount** | 10% of monthly rack rate |
| **Approval** | CEO sign-off required — no exceptions |
| **Documentation** | Written rationale: why standard pricing + Tier 1 lever is insufficient |
| **Time limit** | First 12 months only; reverts to rack rate at renewal |
| **Scope** | Platform tier fee only — user rates, brand rates, and integration hosting are never discounted |
| **Frequency signal** | If >10% of new deals require Tier 2, the price card needs revisiting, not the discount policy |

#### What Sales Should Never Do

- Never discount to match a competitor's published rate — compete on value, not price
- Never discount user or brand expansion pricing — these are already volume-declining
- Never offer multi-year subscription discounts — revisit at scale
- Never discount integration hosting — it's already below market
- Never combine annual term with subscription discount without CEO approval

#### Philosophy

The pricing architecture is designed so that the *published rate is the rate*. Sales energy should be spent articulating value ("here's what you get at T2 that you don't have today") rather than negotiating price ("what if we took 15% off?"). When negotiation pressure arises, onboarding and services flexibility provides a meaningful concession ($1,500–$5,000) that closes deals without establishing a precedent that subscription rates are negotiable.

---

## Phase 2B Stress Tests

Cross-cutting validation exercises that test the pricing architecture against strategic assumptions and growth model integrity. These are not decision items — they validate that stamped decisions hold up under scrutiny.

### ST-001: Expansion White Space Cannibalization (2026-01-28)

**Question**: Does tier bundling (modules included in tiers instead of sold individually) cannibalize SuperCat's status-quo expansion white space? This matters because the 2026 growth model targets a rough 10/10/10 split (10% pricing refresh + 10% expansion + 10% new logos = 30% YoY), and expansion historically meant selling individual modules to existing customers.

**Verdict**: Tier bundling absorbs some expansion paths but the net effect is strongly positive. The expansion ceiling *increases* 64%, per-conversion value increases 2–5×, and two net-new expansion vectors (brand pricing, premium support) are created. The risk shifts from structural (insufficient white space) to execution (Sales learning tier upgrade conversations instead of module sales).

#### What Gets Cannibalized

Tier bundling absorbs three module-sale expansion paths:

| Cannibalized Path | Accounts | Old-Model MRR Potential | Mechanism |
|---|---:|---:|---|
| T1 gets Online Catalog free (bundled into T1) | 56 | $16,520/mo | 56 iPad-only accounts had no Catalog; it's now included in T1 |
| T3 gets Cart free (bundled into T3) | 14 | $4,130/mo | 14 Portal-only T3 accounts had no Cart; it's now included in T3 |
| T3 gets Catalog free (bundled into T3) | 0 | $0/mo | All T3 accounts already had Catalog |
| **Total cannibalized** | **70** | **$20,650/mo ($248K/yr)** | |

#### Why the Cannibalized White Space Was Low-Conversion

The $248K/yr figure overstates the real loss because this white space was aspirational, not productive:

- **Catalog for iPad-only accounts**: Only 5 of 61 T1 accounts (8%) have ever purchased Catalog as a standalone module despite it being available for years. An 8% attach rate over the product's lifetime means this was not an active expansion lever.
- **Cart for Portal-only T3 accounts**: 14 of 34 T3 accounts (41%) have Portal but not Cart. These accounts chose Portal for dealer/buyer access management without needing online ordering — Cart wasn't a natural upsell for this segment.

#### What Replaces It: Higher Per-Conversion Value

Every expansion motion is worth dramatically more under the tier model:

| Commercial Motion | Old Model (module sale) | New Model (tier upgrade) | Delta | Change |
|---|---:|---:|---:|---:|
| T1 customer adds Cart | $295/mo | $546/mo (T1→T2) | +$251 | **+85%** |
| T1 customer adds Portal | $295/mo | $1,546/mo (T1→T3) | +$1,251 | **+424%** |
| T1 customer adds Cart + Portal | $590/mo | $1,546/mo (T1→T3) | +$956 | **+162%** |
| T2 customer adds Portal | $295/mo | $1,000/mo (T2→T3) | +$705 | **+239%** |

The tier upgrade captures a full platform-level price step, not an incremental module fee. The commercial effort is comparable — the same conversations about digital selling maturity, buyer self-service, and analytics readiness — but each conversion generates 2–5× the revenue.

#### Cannibalized Accounts Still Generate More Revenue Under Tier Migration

The 14 T3-no-Cart accounts (the largest cannibalized segment by per-account impact) were individually verified. Every account sees a platform fee increase from tier migration that exceeds the $295/mo Cart module they would have bought:

| Account | Current Platform | New T3 Price | Platform Uplift | vs $295 Cart Sale |
|---|---:|---:|---:|---|
| Jonathan Charles Fine Furniture | $1,107 | $2,295 | +$1,188/mo | 4.0× the module sale |
| Sarreid, Ltd. | $1,370 | $2,295 | +$925/mo | 3.1× |
| Access Lighting | $1,515 | $2,295 | +$780/mo | 2.6× |
| Interlude Furniture | $1,540 | $2,295 | +$755/mo | 2.6× |
| Summer Classics (Wholesale) | $1,426 | $2,295 | +$869/mo | 2.9× |
| Universal Furniture | $1,020 | $2,295 | +$1,275/mo | 4.3× |
| Ciana Varaluz LLC | $725 | $2,295 | +$1,570/mo | 5.3× |
| *...7 others...* | *$1,515–$2,540* | *$2,295* | *+$290 to +$780/mo* | *1.0–2.6×* |
| **Total (14 accounts)** | | | **+$10,747/mo** | **2.6× the $4,130 Cart white space** |

Only one account (Crystorama, currently at $2,540) sees a decrease (-$245/mo). For this account, the "free" Cart at migration is a genuine value-add narrative: *"Your platform fee decreases slightly, and you gain online ordering capabilities."*

#### Expansion Ceiling Comparison: Old vs. New

| Expansion Vector | Old Model Ceiling | New Model Ceiling | Notes |
|---|---:|---:|---|
| Module sales (Cart, Portal, Catalog) | $59,295/mo | — | Absorbed into tier upgrades |
| **Cross-tier upgrades** (T1→T2, T2→T3) | — | **$42,306/mo** | 61 T1 × $546 + 9 T2 × $1,000 |
| User expansion | (same) | $28,496/mo | Preserved; growth-driven |
| Add-ons (CPQ, PCI) | $38,415/mo | $38,415/mo | Preserved; orthogonal to tiers |
| **Brand expansion** | — | **Uncapped** | Net-new vector ($495/$895/$1,495/brand) |
| **Premium Support** | — | **$51,480/mo** | Net-new vector ($495/mo × 104 accounts) |
| **Total ceiling** | **$97,710/mo** | **$160,697/mo+** | **+64% (excludes brand expansion)** |

The old model's expansion was structurally capped by the $295/module price point. The new model replaces $295 module sales with $546–$1,546 tier upgrades and adds two net-new vectors that didn't exist.

#### Impact on 10/10/10 Growth Model

Current ARR: $1,783,181. 30% YoY growth target: $534,954 delta, allocated 10/10/10.

| Growth Lever | Target (10%) | Actual/Projected | Status |
|---|---:|---:|---|
| **Pricing refresh** | $178,318 | $209,004 (11.7%) | Over-delivers by $31K |
| **Expansion** | $178,318 | See below | Ceiling dramatically expanded |
| **New logos** | $178,318 | Independent of pricing architecture | Unchanged |

**Blended expansion scenario** (same commercial effort, both models):

| Motion | Old Model Yield | New Model Yield |
|---|---:|---:|
| 5 module/tier upgrades from T1 | $17,700/yr (5 × $295 × 12) | $32,760/yr (5 × $546 × 12) |
| 2 module/tier upgrades from T2 | $7,080/yr (2 × $295 × 12) | $24,000/yr (2 × $1,000 × 12) |
| Organic user growth | $24,000/yr | $24,000/yr |
| Premium Support (5 accounts) | — | $29,700/yr |
| Add-ons (3 CPQ) | $7,020/yr | $7,020/yr |
| **Total** | **$55,800/yr (3.1%)** | **$117,480/yr (6.6%)** |

Same commercial effort yields **111% more expansion revenue** under the new model. The 6.6% is below the 10% target, but:

1. The scenario is conservative — 5 T1→T2 upgrades from 61 eligible accounts is an 8% conversion rate
2. Brand expansion revenue (net-new, hard to size pre-launch) is excluded
3. Organic user growth at $2K/mo is a conservative baseline
4. The pricing refresh over-delivery ($31K) partially compensates

To reach the full 10% expansion target, the new model requires approximately 8 T1→T2 upgrades (13% conversion), 3 T2→T3 upgrades, and modest contributions from premium support, user growth, and add-ons. The old model cannot reach 10% under any realistic assumption — its ceiling of $55.8K/yr at the same effort level is only 31% of the target.

#### Execution Risk: The Real Constraint

The structural finding is that tier bundling *enlarges* expansion capacity. The bottleneck is execution:

- **Commercial motion shift**: Sales is accustomed to pitching individual modules ("add Cart for $295/mo"). Under tiers, the conversation becomes tier upgrades ("upgrade to Commerce Professional for $546/mo more"). Same trigger (digital selling maturity), higher ask, different framing.
- **Enablement requirement**: Sales team needs to articulate the *value* of a tier (bundle of capabilities) rather than the *function* of a module (Cart does X). This is a Workstream A / 60-second test deliverable.
- **Timeline**: Module-sale muscle memory won't disappear overnight. Expect the first 2–3 quarters post-migration to run at the conservative scenario (6–7% expansion), with acceleration as tier upgrade conversations become natural.

This execution risk is addressed by Phase 2 Workstream A (Sales enablement, 60-second test) and Phase 4 (GTM readiness). It is not a pricing architecture problem.

---

## Migration Policy & Install Base Transition System

> **Status**: Framework codified from v5 migration analysis. Policy decisions marked as **DECIDED** or **OPEN (Workstream D)**. This section is the operating manual for the install-base migration — it translates the analytical work (v1–v5 migration models, entity migration table, brand pricing stress test) into executable policy.

> **Governing principle**: The migration is a one-time event that normalizes 104 accounts from legacy à la carte pricing to the stamped tier architecture. Every policy decision in this section should optimize for *completing the migration cleanly* — not for maximizing short-term revenue or minimizing short-term risk at the expense of architectural integrity.

---

### MP-001: Migration Scope and Completeness

**DECIDED.** All 104 accounts in the v5 migration table migrate to the new pricing architecture. There are no opt-outs, grandfather clauses, or permanent legacy holds. The goal is 100% migration by Q5 2027.

| Dimension | Policy |
|---|---|
| Scope | All 104 active accounts |
| Target completion | 100% by Q5 2027 (Jun 2027) |
| Pacing | Wave 1 (Q3 2026): 50% migrated / Wave 2 (Q4 2026): 80% / Wave 3 (Q5 2027): 100% |
| Opt-out | None. Legacy pricing is retired. |
| Grandfathering | None. All accounts move to stamped tier pricing. |

---

### MP-002: Tier Assignment Rules

**DECIDED.** Tier assignment is mechanical, based on product configuration. No subjective judgment, no negotiation surface.

| Signal | Tier | Price |
|---|---|---|
| `has_portal = True` | T3 — Commerce Enterprise | $2,295/mo |
| `has_cart = True` OR `has_cpq = True` OR `has_cc = True` | T2 — Commerce Professional | $1,295/mo |
| None of the above | T1 — Catalog Essentials | $749/mo |

Tier assignment determines: platform price, included-user allocation (10/15/40), and eligible brand rate (if consolidation applies). CPQ, CC, and PCI are included in T2+ — these features drive the tier minimum, not a separate charge.

**Edge case**: An account with CPQ but no Cart is still T2. The feature, not the module configuration, determines the tier.

---

### MP-003: Pricing Components on Default Migration Path

**DECIDED.** The default migration path has exactly two pricing components. Brand charges are excluded.

| Component | Rule | Source |
|---|---|---|
| **Tier base** | T1: $749 / T2: $1,295 / T3: $2,295 | D-004a |
| **Excess users** | Graduated: $25 (1-10) → $22 (11-25) → $20 (26-50) → $18 (51+) | D-004b |
| **Brands** | $0 on default path | D-004c / Path B |
| **Add-ons** | $0 (CPQ/CC/PCI included in T2+) | D-003a v2 |

`new_total_mrr = tier_base + graduated_user_charge(modeled_users - included_users)`

Included users: T1 = 10, T2 = 15, T3 = 40.

---

### MP-004: Risk Classification System

**DECIDED.** Every account is classified into one of six risk bands based on percentage change from current to new MRR. Risk bands drive migration wave assignment, conversation approach, and churn modeling.

| Band | Criteria | v5 Accounts | Conversation Intensity |
|---|---|---:|---|
| 1 — Decrease (>10%) | New < Current by >10% | 5 | Zero-friction. Policy decision on floor pricing. |
| 2 — Decrease (0-10%) | New < Current by 0-10% | 5 | Zero-friction. Near-parity. |
| 3 — Flat (0-10%) | New > Current by 0-10% | 16 | Standard email. |
| 4 — Modest (10-20%) | New > Current by 10-20% | 21 | Account-owner email + brief call. |
| 5 — Moderate (20-30%) | New > Current by 20-30% | 21 | Account-owner call with value narrative. |
| 6 — Significant (>30%) | New > Current by >30% | 36 | High-touch: account-owner + CS leadership. |

---

### MP-005: Migration Wave Assignment

**DECIDED.** Four-wave migration, sequenced by risk band. Lower-risk accounts migrate first to build institutional experience and create positive proof points before high-stakes conversations.

| Wave | Timing | Risk Bands | Accounts | MRR Coverage | Rationale |
|---|---|---|---:|---:|---|
| **1** | Q3 2026 (first half) | Bands 1-3 (Decrease + Flat) | 26 | $42,618 | Zero-friction. Builds momentum. Proves mechanics. |
| **2** | Q3 2026 (second half) | Band 4 (Modest) | 21 | $39,223 | Standard value narrative. "$100-200/mo more for expanded platform." |
| **3** | Q4 2026 | Band 5 (Moderate) | 21 | $45,942 | Account-owner conversations. 13 of 21 are T3 (10 fewer included users). |
| **4** | Q4 2026 – Q1 2027 | Band 6 (Significant) | 36 | $51,195 | High-touch. Entity conversations. Phased increases for >100%. |

Wave 1 and 2 together reach 50% of accounts by mid-Q3 2026. Waves 3-4 reach 80% by end Q4 2026. Stragglers and complex entity conversations complete by Q5 2027.

---

### MP-006: Migration Driver Taxonomy

**DECIDED.** Every account's price change is classified by a primary driver from the stamped taxonomy. This is the analytical backbone of the migration conversation — it answers *why* the price is changing and informs the narrative.

| Driver | Direction | Accounts | Δ MRR | Conversation Anchor |
|---|---|---:|---:|---|
| `user_rate_normalization` | ↑ | 46 | +$15,290 | "Your per-user rate moves from $15-20 to the graduated curve ($25/$22/$20/$18)." |
| `discount_correction` | ↑ | 33 | +$14,502 | "We're normalizing your platform to the published rate. Here's what you gain." |
| `multi_org_retirement` | ↑ | 9 | +$3,213 | "The entity-wide discount is being retired. Let's discuss your options." |
| `at_book_tier_shift` | ↑ | 6 | +$239 | "Minimal change — your rate moves from $725 to $749 with new capabilities." |
| `user_count_variance` | ↓ | 2 | -$941 | "Your new pricing is actually lower based on your current usage." |
| `module_compression` | ↓ | 8 | -$1,923 | "Your tier now includes modules you were paying separately for." |

**Secondary drivers** (noted in the `secondary_drivers` column) provide additional context but don't change the primary narrative. Common secondaries: `multi_org_retirement` (on accounts where discount correction is primary), `included_user_gain` (tier includes more users than current allocation).

---

### MP-007: Multi-Org Discount Retirement (Path B)

**DECIDED.** The legacy 10% multi-org discount is sunset at the account level. Each account pays full tier + users on the default migration path. Brand pricing at 90% of natural tier is available as a reactive, entity-level consolidation option — not proactively applied.

| Element | Policy |
|---|---|
| Default path | Multi-org discount retired. Account pays full tier + users. |
| Brand pricing | Consolidation-only. Not applied unless entity requests it. |
| Brand rates | 90% of natural tier: T1 $674 / T2 $1,166 / T3 $2,066 |
| Included users per brand | Per-brand allocation at natural tier (no pooling). |
| Who is affected | 5 rollup entities (14 accounts) with multi-org discount + 6 standalone accounts |
| Standalone multi-org | Discount retired with no replacement. No sibling brands to consolidate with. |

#### Entity Consolidation Economics (if requested)

| Entity | Brands | Default Δ | Consol Δ | Saving | Multi-Org? |
|---|---:|---:|---:|---:|---|
| Gabriella White | 4 | +23% | +16% | $687 (6.1%) | 10% |
| Interlude Home | 2 | +28% | +22% | $229 (5.0%) | — |
| Godinger Silver Art | 4 | +109% | +97% | $225 (5.8%) | — |
| Generation Brands | 3 | +44% | +40% | $150 (2.6%) | 22.5% |
| Baker Interiors | 3 | +22% | +17% | $150 (4.1%) | 10% |
| Abaline | 2 | +12% | +8% | $129 (3.4%) | — |
| Theodore Alexander | 2 | +12% | +8% | $129 (3.6%) | — |
| Jonathan Charles | 2 | +28% | +23% | $129 (3.6%) | — |
| Coleto Brands | 2 | +18% | +16% | $75 (2.2%) | — |
| WAC | 2 | +33% | +31% | $75 (1.7%) | 10% |
| Century Furniture | 2 | +15% | +9% | $75 (5.0%) | 10% |
| HVLG | 2 | +224% | +215% | $75 (2.8%) | — |
| **Total** | **30** | | | **$2,128 (4.1%)** | |

Worst-case consolidation leakage: $2,128/mo. 93% of v5 refresh delta retained.

---

### MP-008: Floor Pricing Policy for Decrease Accounts

**OPEN — Workstream D decision required.**

10 accounts (10% of base) see a price decrease under raw tier pricing, totaling -$2,864/mo (-$34,368/yr). The question: pass through the decrease or hold at current MRR?

| Option | Revenue Impact | Rationale | Risk |
|---|---|---|---|
| **A: Pass through** | -$2,864/mo | Price integrity. New pricing is the price. Decrease accounts are retention wins. | Leaves $34K/yr on the table. Sets precedent that prices can go down. |
| **B: Floor at current** | $0 erosion | No account pays less than today. Preserves every dollar of current MRR. | "My new price is lower but you're charging me the old price" — credibility risk if discovered. |
| **C: Floor with sunset** | -$2,864/mo at sunset | Floor at current for 12 months, then transition to true new pricing. | Complexity. Two pricing events per account. |

**Accounts affected:**

| Company | Tier | Current | New | Δ | Driver |
|---|---|---:|---:|---:|---|
| Wildwood/Chelsea House | T3 | $3,362 | $2,545 | -$817 | user_count_variance (brand charges removed) |
| Donald Choi Canada | T2 | $1,836 | $1,295 | -$542 | module_compression |
| Tomlinson Companies | T1 | $1,120 | $749 | -$371 | module_compression |
| Morgan Fabrics | T1 | $1,120 | $749 | -$371 | module_compression |
| Palecek | T1 | $3,251 | $2,963 | -$288 | module_compression |
| Yutzy Woodworking | T1 | $949 | $824 | -$125 | user_count_variance |
| Charleston Forge | T2 | $1,756 | $1,633 | -$123 | module_compression |
| Groupe Courchesne | T2 | $1,415 | $1,295 | -$120 | module_compression |
| Moda at Home | T2 | $1,387 | $1,295 | -$92 | module_compression |
| Kennedy International | T2 | $1,387 | $1,370 | -$17 | module_compression |

**Recommendation**: Option A (pass through). Module compression decreases are by design — the tier architecture absorbs legacy modules. These accounts gain capabilities they were paying separately for. Passing through the decrease is the clearest signal that the new pricing is fair and consistent. The $2,864/mo is a small structural cost of packaging simplification, and these accounts become retention proof points.

---

### MP-009: Phased Increase Policy for >100% Accounts

**OPEN — Workstream D decision required.**

5 accounts see increases exceeding 100%. These are the highest-risk migration conversations and may warrant a phased approach.

| Account | Tier | Current | New | Δ% | Driver | Entity |
|---|---|---:|---:|---:|---|---|
| Troy Lighting | T1 | $366 | $1,197 | +227% | discount_correction | HVLG |
| Hudson Valley Lighting | T1 | $450 | $1,449 | +222% | discount_correction | HVLG |
| Ricci Argentieri | T1 | $378 | $1,131 | +199% | discount_correction | Godinger |
| Studio Silversmiths | T1 | $375 | $899 | +140% | discount_correction | Godinger |
| Philip Whitney | T1 | $375 | $824 | +120% | discount_correction | Godinger |

All 5 are T1 accounts with deep legacy discounts (platform fees 50-75% below book). All are members of rollup entities (HVLG: 2 accounts, Godinger: 3 of 4 accounts).

| Option | Year 1 | Year 2 | Revenue Impact |
|---|---|---|---|
| **A: Full migration** | 100% of new price | — | Maximum revenue. Highest churn risk on 5 accounts. |
| **B: 50/100 phased** | 50% of increase | Full new price | Defers ~$1,900/mo for 12 months (~$23K). Halves sticker shock. |
| **C: 3-step (33/66/100)** | 33% of increase | 66% of increase, then 100% in Year 3 | Maximum softening. Most complex to administer. |

**Recommendation**: Option B (50/100). These are small-dollar accounts ($366-$450 current MRR) within entities that are already having high-touch conversations. The phased approach costs ~$23K in deferred revenue but significantly de-risks the two highest-risk entity conversations (HVLG at +224% and Godinger at +109%). Year 1 prices for phased accounts:

| Account | Year 1 (50%) | Year 2 (100%) |
|---|---:|---:|
| Troy Lighting | $782 | $1,197 |
| Hudson Valley Lighting | $949 | $1,449 |
| Ricci Argentieri | $755 | $1,131 |
| Studio Silversmiths | $637 | $899 |
| Philip Whitney | $600 | $824 |

---

### MP-010: Entity Migration Protocol

**DECIDED (framework) / OPEN (outreach mechanics).**

12 rollup entities (30 accounts) require entity-level migration conversations. 6 standalone multi-org accounts require individual conversations acknowledging the discount retirement.

#### Entity Conversation Tiers

| Tier | Entities | Criteria | Conversation Lead | Consolidation Posture |
|---|---|---|---|---|
| **Executive** | Godinger (+109%), HVLG (+224%) | Entity increase >50% | CS leadership + account-owner | Present consolidation economics if asked. Phased increases recommended. |
| **High-touch** | GW (+23%), Gen Brands (+44%), WAC (+33%), Baker (+22%), Interlude (+28%), Jonathan Charles (+28%) | Entity increase 20-50% | Account-owner with CS support | Mention consolidation option. Lead with value narrative. |
| **Standard** | Abaline (+12%), Theodore Alexander (+12%), Coleto (+18%), Century (+15%) | Entity increase <20% | Account-owner | Standard migration communication. Consolidation available if requested. |

#### Consolidation Outreach Protocol

**OPEN — Workstream D decision required.** The question: how proactive should we be in presenting the consolidation option?

| Option | Approach | Implication |
|---|---|---|
| **A: Fully reactive** | Never mention consolidation. Only discuss if entity raises it. | Minimizes consolidation uptake. Maximizes revenue. May frustrate entities that discover the option later. |
| **B: Informed consent** | Present both paths (default and consolidated) during entity conversations. Let them choose. | Transparent. Gives entities agency. May increase consolidation uptake to 2-3 of 12 entities. |
| **C: Multi-org entities only** | Present consolidation to the 5 entities with multi-org discount being retired (as a replacement mechanism). Reactive for other 7. | Targeted. Addresses the "what replaces my discount" question directly. |

**Recommendation**: Option C. The 5 multi-org entities will inevitably ask "what happens to my 10% discount?" — consolidation at 90% of natural tier is the prepared answer. For the other 7 entities, consolidation saves 2-6% with no legacy discount to replace; there's no natural trigger to raise it.

---

### MP-011: Billing Transition Mechanics

**OPEN — Workstream D decision required.**

| Decision | Options | Recommendation |
|---|---|---|
| **Effective date** | (A) Next renewal date, (B) Fixed cutover date per wave, (C) 30-day notice from communication | **B: Fixed cutover per wave.** Simplifies operations. All Wave 1 accounts transition on the same date. |
| **Annual contracts mid-term** | (A) Transition at renewal, (B) Transition immediately with pro-rata credit, (C) Transition immediately at blended rate for remainder | **A: Transition at renewal.** Respects contract terms. Annual accounts may slip to Wave 3-4 timing. |
| **Month-to-month accounts** | (A) 30-day notice, (B) 60-day notice, (C) Next billing cycle after notification | **A: 30-day notice.** Standard practice. Aligns with existing terms. |
| **Invoice format** | (A) Single line "Platform + Users", (B) Decomposed: tier base + user charges | **B: Decomposed.** Transparency. Customers see exactly what they pay for. Aligns with the graduated user curve being a feature, not a hidden mechanic. |

---

### MP-012: Communication Framework

**OPEN — Workstream D decision required (templates).** Framework established.

#### Per-Cohort Communication Approach

| Cohort | Channel | Timing | Content |
|---|---|---|---|
| Decrease (>10%) | Email + optional call | 30 days pre-transition | "Your new pricing is lower. Here's what's included in your tier." |
| Decrease (0-10%) | Email | 30 days pre-transition | "Your pricing is virtually unchanged, with new capabilities included." |
| Flat (0-10%) | Email | 30 days pre-transition | "Modest adjustment with significantly expanded platform." |
| Modest (10-20%) | Email + account-owner call | 45 days pre-transition | "$X/mo more for [list of new capabilities]. Here's the value breakdown." |
| Moderate (20-30%) | Account-owner call + follow-up email | 60 days pre-transition | Value narrative required. For T3 accounts: "10 fewer included users; additional at graduated rates." |
| Significant (>30%) | Account-owner + CS leadership call | 90 days pre-transition | Driver-specific narrative. Entity conversations. Phased increase offer (if applicable). |

#### Key Messaging Principles

1. **Lead with what they gain, not what changes.** Every tier includes capabilities that were previously separate charges or unavailable.
2. **Name the driver.** "Your rate is normalizing to the published price" (discount_correction) is more defensible than "your price is going up."
3. **Never apologize for the price.** The new pricing is fair, consistent, and competitive. Discounting was the anomaly.
4. **Entity conversations are singular.** All accounts within an entity are discussed in one conversation, even if they span multiple waves.

---

### MP-013: Exception and Escalation Protocol

**OPEN — Workstream D decision required (thresholds).** Framework established.

| Scenario | Authority | Documentation Required |
|---|---|---|
| Account requests delay (not objection to price) | Account-owner discretion, max 60 days | Email confirmation of new date |
| Account threatens churn (< $1,000 MRR) | Account-owner + CS manager | Written summary: account value, risk assessment, recommended action |
| Account threatens churn ($1,000-$3,000 MRR) | CS leadership approval | Formal escalation: account history, alternative scenarios, revenue at risk |
| Account threatens churn (> $3,000 MRR) | CEO involvement | Full briefing: entity context, migration economics, retention options |
| Request for phased increase (not pre-approved) | CS leadership approval | Justified by comparable precedent (>100% increase accounts) |
| Request for consolidation pricing | Account-owner presents entity migration table | Entity migration table provides the economics. No approval needed to present. |
| Request for discount beyond D-004f guardrails | CEO approval per D-004f | Per existing Tier 2 protocol |

**Hard rules (no exceptions):**
- Tier assignment is not negotiable. Product configuration determines tier.
- User rates are not negotiable. The graduated curve is the published rate.
- Brand rates are not negotiable. 90% of natural tier is the rate.
- No permanent legacy holds. Every account migrates.

---

### MP-014: Success Metrics and Tracking

**DECIDED (metrics) / OPEN (targets and reporting cadence).**

| Metric | Definition | v5 Baseline | Target |
|---|---|---:|---|
| **Migration completion %** | Accounts transitioned / 104 | 0% | 50% by Q3, 80% by Q4, 100% by Q5 |
| **Retained MRR** | Post-migration MRR / v5 projected MRR ($178,978) | — | >95% (expected scenario) |
| **Migration-induced churn** | Accounts lost specifically due to pricing migration | 0 | <4 (expected), <8 (conservative) |
| **Churn vs. modeled** | Actual churn by risk band vs. modeled rates | — | At or below modeled rates per band |
| **Consolidation uptake** | Entities that opt for consolidated pricing | 0 | Track, no target (consolidation is not incentivized) |
| **Floor pricing invocations** | Decrease accounts held at current vs. passed through | — | Per MP-008 decision |
| **Phased increase compliance** | Year 2 transitions for phased accounts | — | 100% (all phase to full price) |
| **Entity conversation completion** | 12 rollup entities + 6 standalone conversations completed | 0 | 100% before Wave 4 |
| **Average days to close** | Days from notification to confirmed acceptance per wave | — | <30 (Waves 1-2), <45 (Wave 3), <60 (Wave 4) |

---

### MP-015: Rollback and Recovery

**DECIDED (principle) / OPEN (mechanics).**

**Principle**: There is no systemic rollback. The migration is a one-way transition to the stamped pricing architecture. Individual account-level accommodations are handled through the escalation protocol (MP-013).

| Scenario | Response | Authority |
|---|---|---|
| Account migrated, objects to price | Escalation protocol (MP-013). No automatic rollback to legacy pricing. | Per escalation tier |
| Systemic issue discovered post-migration | Pause remaining waves. Assess and correct the issue. Migrated accounts stay on new pricing unless the issue materially misrepresents value. | CEO + Pricing Lead |
| Data quality issue on specific account | Correct the account-level data. Re-calculate using v5 methodology. Communicate corrected price. | Account-owner + Pricing Lead |
| Entity requests consolidation after migration | Process at any time. Entity migration table provides the economics. No timing constraint on consolidation requests. | Account-owner presents options |

---

### Migration Policy Decision Summary

| ID | Decision | Status | Owner |
|---|---|---|---|
| MP-001 | Scope: all 104 accounts, no opt-outs | **DECIDED** | — |
| MP-002 | Tier assignment: mechanical, product-based | **DECIDED** | — |
| MP-003 | Pricing: tier + users only (no brands on default) | **DECIDED** | — |
| MP-004 | Risk classification: 6-band system | **DECIDED** | — |
| MP-005 | Wave assignment: 4-wave, risk-sequenced | **DECIDED** | — |
| MP-006 | Driver taxonomy: 8 primary drivers | **DECIDED** | — |
| MP-007 | Multi-org retirement: Path B, consolidation-only | **DECIDED** | — |
| MP-008 | Floor pricing for decrease accounts | **OPEN** | Workstream D |
| MP-009 | Phased increases for >100% accounts | **OPEN** | Workstream D |
| MP-010 | Entity consolidation outreach protocol | **OPEN** | Workstream D |
| MP-011 | Billing transition mechanics | **OPEN** | Workstream D + Finance |
| MP-012 | Communication templates | **OPEN** | Workstream D + CS |
| MP-013 | Exception/escalation thresholds | **OPEN** | Workstream D + CEO |
| MP-014 | Success metric targets and reporting | **OPEN** | Workstream D + Finance |
| MP-015 | Rollback mechanics | **OPEN** | Workstream D + CEO |

**Canonical data sources for migration execution:**
- Account-level: `03_data/extracts/2026-04-15__migration_table__v5.csv` (104 accounts × 31 columns)
- Entity-level: `03_data/extracts/2026-04-15__entity_migration_table__v1.csv` (18 rows × 22 columns)
- Narrative: `03_data/2026-04-15__migration_revenue_model__v5.md`
- Revenue projection: `03_data/2026-04-15__revenue_impact_model__v5.md`

---

## Exploratory Phase Reference

The following artifacts from the exploratory phase (Oct 2025 – Feb 2026) informed the decisions above. They are reference material, not stamped decisions:

| Artifact | Location | Use |
|---|---|---|
| Validated account master v3 (104 accounts) | `03_data/extracts/2026-02-28__master_account_table__v3.csv` | Baseline economics, corrected discount analysis (post-Angie audit) |
| Entity master v3 (86 entities) | `03_data/extracts/2026-02-28__master_entity_table__v3.csv` | Parent-child rollups, entity-level view |
| Angie audit source (SSOT) | `03_data/extracts/2026-02-28__master_account__angie_audit__CANONICAL.csv` | CoS-audited line-by-line pricing with comments |
| Canonical customer data V2 | `03_data/extracts/2026-02-11__master_customer_data__v2__CANONICAL.csv` | Hand-audited MRR decomposition (superseded by Angie audit for discount analysis) |
| Three candidate architectures (A/B/C) | `11_synthesis/OUTLINE_PROPOSALS.md` | Reference for M3 packaging decisions |
| Team workshop synthesis | `11_synthesis/2026-02-06__team_workshop_pricing_synthesis__v1.md` | Value metric confirmation, packaging feedback |
| Option C reference + CEO recommendation | `11_synthesis/2026-02-05__option_c_comprehensive_reference__v1.md`, `CEO recommendation.md` | Exploratory pricing direction |
| Data integration commercialization | `11_synthesis/2026-02-06__data_integration_commercialization__v1.md` | Integration tiering reference |
| Project plan v1 (historical) | `11_synthesis/2026-02-11__pricing_refresh_project_plan__v1.md` | Phase 1 (M0–M3) sequential; Phase 2+ restructured as parallel workstreams (revised 2026-01-28). Superseded by v2. |
| Project plan v2 (current) | `11_synthesis/2026-03-11__pricing_refresh_project_plan__v2.md` | Complete rewrite reflecting 16 stamped decisions, compressed path to market (~6 months) |
| Product capability map (M3 input) | `11_synthesis/2026-01-28__product_capability_map__m3_input__v1.md` | Code/DB-verified feature inventory; 27 capabilities, gating mechanisms, adoption |
| Competitive packaging audit (M3 input) | `11_synthesis/2026-01-28__competitive_packaging_audit__m3_input__v1.md` | AmpTab, Pepperi, WizCommerce, MarketTime, RepZio analysis |
| Packaging architecture (M3 output) | `11_synthesis/2026-01-28__m3_packaging_architecture__v1.md` | Feature-Value Matrix, tier fences, expansion, implementation |
| Customer validation artifact v1 (Phase 2A — superseded) | `09_website/2026-01-28__pricing_validation_artifact__v1.md` | Original structure-only artifact; no prices. Superseded by v2. |
| Customer validation artifact v2 (Phase 2B — current) | `09_website/2026-01-28__pricing_validation_artifact__v2.md` | Updated with all stamped prices, rates, and corrected allocations (1/1/1 brands, Standard support for T2). Design team source document. |
| Platform narrative slide (sales collateral) | `09_website/supercat_platform_narrative_slide.html` | Single-screen dark-background slide for prospect screen-sharing. Three tiers, pricing, scaling, add-ons. |
| Comprehensive pricing page (web) | `09_website/supercat_pricing_page.html` | Full responsive pricing page: tier cards, feature comparison, scaling, add-ons, implementation, upgrade paths. |
| Install-base tier mapping & revealed WTP (Phase 2B, Exercise 1) | `11_synthesis/2026-02-25__install_base_tier_mapping_wtp__d004a_exercise1__v1.md` | Module-to-tier assignment, platform-only MRR distribution, migration risk tables, preliminary price ranges |
| Tier mapping analysis script | `03_data/tier_mapping_wtp_analysis.py` | Python script for tier assignment and WTP analysis; reproduces all Exercise 1 findings |
| Competitive price benchmarking (Phase 2B, Exercise 2) | `11_synthesis/2026-02-25__competitive_price_benchmarking__d004a_exercise2__v1.md` | Tier-by-tier competitive mapping, normalized TCO, combined price ranges, response playbook |
| User discount curve analysis (Phase 2B, D-004b) | `11_synthesis/2026-02-25__user_discount_curve__d004b__v1.md` | Included-user validation, discount curve design, revenue impact modeling |
| User discount curve analysis script | `03_data/user_discount_curve_analysis.py` | Python script for user distribution, curve modeling, and revenue projections |
| Tier price recommendation model (v1 — superseded) | `03_data/tier_price_recommendation.py` | Per-account migration impact at stamped prices, revenue projection, risk analysis. Superseded by migration revenue model. |
| Migration table v5 script (canonical) | `03_data/migration_table_v5.py` | Account-by-account migration: tightened users (10/15/40), brand charges removed from default path |
| Migration revenue model v5 summary (canonical) | `03_data/2026-04-15__migration_revenue_model__v5.md` | Consolidated narrative: barbell analysis, driver taxonomy, sensitivity, entity view, migration playbook |
| Migration table v5 export (canonical) | `03_data/extracts/2026-04-15__migration_table__v5.csv` | 104 accounts × 31 columns, brand charges $0 on default path |
| Entity migration table script (canonical) | `03_data/entity_migration_table.py` | Entity-level migration: 12 rollup entities + 6 standalone multi-org accounts |
| Entity migration table export (canonical) | `03_data/extracts/2026-04-15__entity_migration_table__v1.csv` | 11 entities × 22 columns, default vs consolidated paths |
| Migration table v4 (superseded) | `03_data/migration_table_v4_tightened_users.py` | v4 script — superseded by v5 (brand charges removed) |
| Migration revenue model v4 summary (superseded) | `03_data/2026-04-15__migration_revenue_model__v4.md` | v4 narrative — superseded by v5 |
| Migration table v4 export (superseded) | `03_data/extracts/2026-04-15__migration_table__v4_tightened_users.csv` | v4 export — superseded by v5 |
| Tier pricing stress test (supporting) | `03_data/tier_pricing_stress_test.py` | 5-scenario price/user comparison against v3 baseline |
| Tier pricing stress test summary (supporting) | `03_data/2026-04-15__tier_pricing_stress_test__v1.md` | Decision-ready scenario comparison: revenue lift vs risk composition |
| Included-user sensitivity sweep (supporting) | `03_data/included_user_sensitivity.py` | Per-tier granular sweep with marginal revenue curves |
| Included-user sensitivity summary (supporting) | `03_data/2026-04-15__included_user_sensitivity__v1.md` | Knee-in-curve analysis, recommended allocation (10/15/40) |
| Migration revenue model v3 (superseded) | `03_data/migration_table_v3.py` | v3 script — superseded by v4 (tightened users) |
| Migration revenue model v3 summary (superseded) | `03_data/2026-04-15__migration_revenue_model__v3.md` | v3 narrative — superseded by v4 |
| Migration table v3 export (superseded) | `03_data/extracts/2026-04-15__migration_table__v3.csv` | v3: 104 accounts × 31 columns — superseded by v4 |
| Migration revenue model v2 (superseded) | `03_data/migration_table_v2.py` | v2 script — superseded |
| Migration revenue model v2 summary (superseded) | `03_data/2026-03-28__migration_revenue_model__v2.md` | v2 narrative — superseded |
| Migration table v2 export (superseded) | `03_data/extracts/2026-03-28__migration_table__v2.csv` | v2 export — superseded |
| Migration table v2 companion (superseded) | `03_data/2026-03-28__migration_table__v2.md` | v2 table summary — superseded |
| Migration revenue model v1 (superseded) | `03_data/migration_revenue_model.py` | v1 script — superseded |
| Migration revenue model v1 summary (superseded) | `03_data/2026-03-11__migration_revenue_model__v1.md` | v1 narrative — superseded |
| Migration table v1 export (superseded) | `03_data/extracts/2026-03-11__migration_table__v1.csv` | v1 export — superseded |
| Migration model — floor variant (exploratory) | `03_data/migration_revenue_model__floor_variant.py` | Floor pricing policy analysis (Workstream D) |
| Revenue impact model v5 summary (canonical) | `03_data/2026-04-15__revenue_impact_model__v5.md` | v5 narrative: v5 migration baseline, entity consolidation overlay, 3-scenario projection |
| Revenue impact model v3 (superseded) | `03_data/revenue_impact_model_v3.py` | v3 script — superseded by v5 migration baseline |
| Revenue impact model v3 summary (superseded) | `03_data/2026-04-15__revenue_impact_model__v3.md` | v3 narrative — superseded by v5 |
| Revenue impact model v2 (superseded) | `03_data/revenue_impact_model_v2.py` | v2 script — superseded |
| Revenue impact model v2 summary (superseded) | `03_data/2026-03-28__revenue_impact_model__v2.md` | v2 narrative — superseded |
| Revenue impact model v1 (superseded) | `03_data/revenue_impact_model.py` | v1 script — superseded |
| Revenue impact model v1 summary (superseded) | `03_data/2026-03-11__revenue_impact_model__v1.md` | v1 narrative — superseded |
| Brand pricing analysis (v2 — value-based) | `11_synthesis/2026-02-25__brand_pricing_analysis__d004c__v2.md` | Revised brand pricing architecture, entity-by-entity impact, consolidation stress test |
| Brand pricing stress test (v4 rebased) | `03_data/2026-04-15__brand_pricing_stress_test__v1.md` | Comprehensive stress test: multi-org anchor, governing tier critique, natural-tier proposal, user pooling policy analysis. Proposed and stamped: Nat@90% + per-brand included, consolidation-only (Path B). |
| Brand pricing stress test script | `03_data/brand_pricing_stress_test.py` | Consolidation economics, incentive delta, rate sensitivity, compound risk, user pooling |
| À la carte premium schedule | `11_synthesis/2026-02-25__a_la_carte_premium_schedule__d004d__v1.md` | Module pricing, tier-push verification, operational guardrails |
| Brand pricing analysis script | `03_data/brand_pricing_analysis.py` | Updated to value-based model ($495/$895/$1,495, 1 included per tier) — v2-era inputs |
| Modular alternative analysis (exploratory) | `04_models/2026-01-30__modular_alternative__option_b.md` | Competitive roundup from exploratory phase |
