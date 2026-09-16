# Signal Catalog — Insightful Product 3.0

> **Status**: Active
> **Organizing principle**: Signals ranked by actionability and surprise value — not by domain.
> **Design source**: Customer Intelligence v4 pattern detection (validated across 40+ customer briefs)

---

## How This Catalog Works

Every signal is a **detectable pattern** in the data that produces a specific, actionable output. Unlike the 2.0 Value Moment system (which cataloged capabilities by domain), this catalog is organized by **what makes a client say "holy shit."**

Each signal has:

| Field | Purpose |
|-------|---------|
| **Detection** | Query ID + threshold that fires the signal |
| **Surprise Score** | Formula for how far from expected this finding is |
| **Dollar Impact** | How to compute the revenue at stake |
| **Output Format** | Exactly what the rendered finding looks like (item numbers, customer names, dollar figures) |
| **Priority Tier** | P0 = always surface if detected. P1 = surface if top 10. P2 = detail/collapsed. |
| **Section Home** | Which report section this signal renders in |
| **Data Gate** | What must be present for detection to run |

---

## Surprise Scoring Framework

Every detected signal is scored:

```
SIGNAL_RANK = surprise_score × dollar_impact × actionability_multiplier
```

| Component | Computation |
|-----------|-------------|
| `surprise_score` | How many multiples of expected (e.g., 56-day gap / 12-day avg = 4.7x). Minimum 1.0. |
| `dollar_impact` | LTM revenue of affected entity (item, customer, category). In dollars. |
| `actionability_multiplier` | Item-level + named customer + specific action = 3.0. Category-level = 2.0. "Consider doing X" = 1.0. |

Signals are ranked by SIGNAL_RANK. The top 5-7 become the Signal Summary. The rest populate their section homes.

---

## Category 1: Decay Signals

### SIG-DECAY-01: Customer Reorder Frequency Collapse

**Priority**: P0
**Section Home**: Account Intelligence
**Data Gate**: `portal_orders` OR `orders` with 6+ months history

**Detection**: For each of the org's top 50 accounts by LTM revenue, compute:
- Historical average days-between-orders (minimum 5 orders to qualify)
- Current gap (days since last order)
- Ratio: `current_gap / avg_days_between`

**Fires when**: Ratio > 2.5x AND account LTM revenue > $10K

**Surprise Score**: `current_gap / avg_days_between` (e.g., 56 days / 12 days = 4.7x)

**Dollar Impact**: Account's LTM revenue (total from all channels if portal_orders available, else eCat-only)

**Output Format**:
> **[CUSTOMER NAME] — reorder silence at [X]x normal cadence**
> Last ordered [DATE] ([N] days ago). Historical average: every [Y] days. At $[LTM_REVENUE] LTM, this account typically places [N] orders per month. The [Z]-day silence is [RATIO]x their normal rhythm.

**Query**: Q-ORG-DECAY

---

### SIG-DECAY-02: Item-Level Reorder Collapse (Per-Customer)

**Priority**: P0
**Section Home**: Account Intelligence (embedded in account mini-briefs)
**Data Gate**: `portal_order_items` OR `sales_data`

**Detection**: For each top-50 account, identify items with 5+ historical reorder cycles. Compute:
- Average interval between orders for that item at that customer
- Days since last order of that item
- Ratio: `latest_interval / avg_interval`

**Fires when**: Ratio > 3.0x AND item LTM revenue at this customer > $5K

**Surprise Score**: `latest_interval / avg_interval`

**Dollar Impact**: Item's LTM revenue at this customer

**Output Format**:
> **[ITEM_NUMBER] ([DESCRIPTION]) at [CUSTOMER]** — [N] reorder cycles, avg every [X] days, last ordered [Y] days ago ([RATIO]x normal). LTM revenue: $[Z].
> Status: DECAY_DETECTED / SLOWING

**Query**: Q-ORG-DECAY (item-level sub-query)

---

### SIG-DECAY-03: Rep Engagement Trajectory Decline

**Priority**: P1
**Section Home**: Team Intelligence
**Data Gate**: `orders` with 6+ months history, 5+ active reps

**Detection**: Compare each rep's order count in most recent 90 days vs. prior 90 days.

**Fires when**: Decline > 25% AND rep had 10+ orders in prior period AND rep LTM GMV > $50K

**Surprise Score**: `ABS(pct_decline) / 25` (normalized so 25% = 1.0, 50% = 2.0)

**Dollar Impact**: Rep's trailing 90-day GMV annualized

**Output Format**:
> **[REP NAME]** — orders declined [X]% quarter-over-quarter ([PRIOR] → [CURRENT]). Current 90-day GMV: $[Y]. If trajectory continues, annual impact: ~$[Z].

**Query**: Q-06 (from 2.0 library)

---

### SIG-DECAY-04: Spending Contraction Detection

**Priority**: P0
**Section Home**: Account Intelligence
**Data Gate**: `portal_orders` with 12+ months history

**Detection**: For each account with LTM revenue > $25K, compare LTM vs. prior-year total business GMV.

**Fires when**: YoY decline > 20% AND LTM revenue > $50K

**Surprise Score**: `ABS(yoy_pct_decline) / 20` (20% decline = 1.0, 40% = 2.0)

**Dollar Impact**: Absolute dollar decline (prior_gmv - ltm_gmv)

**Output Format**:
> **[CUSTOMER]** — total business declined [X]% ($[PRIOR] → $[LTM]). Revenue lost: $[GAP]. [Quarters showing decline pattern].

**Query**: Q-ORG-CONTRACTION

---

## Category 2: Anomaly Signals

### SIG-ANOMALY-01: Ghost SKU Detection

**Priority**: P0
**Section Home**: Product Intelligence
**Data Gate**: `sales_data` OR `portal_order_items`

**Detection**: Cross-reference all invoiced/ordered item codes against `products` table. Items with revenue but no catalog record = ghost SKUs.

**Fires when**: Any ghost SKU with > $5K LTM revenue exists

**Surprise Score**: 3.0 (fixed — ghost SKUs are always highly surprising)

**Dollar Impact**: Sum of revenue for each ghost SKU

**Output Format**:
> **GHOST SKU — [ITEM_CODE]** — $[REVENUE] invoiced LTM ([UNITS] units), no catalog record. Cannot verify stock status, description, or collection. Customers ordering: [LIST].

**Query**: Q-ORG-GHOST

---

### SIG-ANOMALY-02: Stock-Out on High-Demand Items

**Priority**: P0
**Section Home**: Product Intelligence
**Data Gate**: `inventories` + (`sales_data` OR `portal_order_items`)

**Detection**: Join top-50 items by LTM revenue to current inventory. Flag items where `qty_available = 0` AND LTM revenue > $10K.

**Fires when**: Top-selling item at zero stock

**Surprise Score**: `item_rank_position / 5` (top 5 items = 1.0–5.0x surprise for being stocked out)

**Dollar Impact**: Item's LTM revenue

**Output Format**:
> **STOCK OUT — [ITEM] ([DESCRIPTION])** — $[REVENUE] LTM, [UNITS] units sold, 0 available.
> Next receipt: [DATE] | On backorder: [QTY]
> Customers impacted: [TOP 5 CUSTOMERS BY REVENUE FOR THIS ITEM]
> Alternatives (same collection): [UP TO 3 ALTERNATIVES WITH AVAILABLE QTY]

**Query**: Q-ORG-STOCKOUT

---

### SIG-ANOMALY-03: Competitive Displacement (eCat Down, Total Business Up)

**Priority**: P0
**Section Home**: Account Intelligence
**Data Gate**: `orders` + `portal_orders` both with 12+ months

**Detection**: For each account with both data sources: compute eCat YoY% and total-business YoY%.

**Fires when**: eCat YoY < -10% AND total business YoY > +5% AND account LTM > $25K

**Surprise Score**: `ABS(ecat_yoy - total_biz_yoy) / 15` (15-point divergence = 1.0)

**Dollar Impact**: `account_ecat_gmv_prior × ABS(ecat_yoy_pct - total_biz_yoy_pct) / 100`

**Output Format**:
> **COMPETITIVE DISPLACEMENT — [CUSTOMER]**
> eCat orders: [X]% ($[PRIOR] → $[LTM])
> Total business: [Y]% ($[PRIOR] → $[LTM])
> Revenue shifting away from eCat: ~$[GAP]
> This customer is buying MORE overall but LESS through your platform.

**Query**: Q-ORG-CONTRACTION (dual-source variant)

---

## Category 3: Opportunity Signals

### SIG-OPP-01: Next Best Product (Collaborative Filtering)

**Priority**: P0
**Section Home**: Account Intelligence (per-account) + Product Intelligence (org-wide patterns)
**Data Gate**: `portal_order_items` OR `sales_data` (requires item-level transaction history across multiple customers)

**Detection**: For each top-50 account, identify their top 5 purchased items. For each anchor item, find what OTHER customers who buy that item also purchase within 90 days. Flag items the target account has never bought.

**Fires when**: 10+ other customers exhibit the same purchase pairing AND target account has $0 for the suggested item

**Surprise Score**: `co_purchase_customers / 10` (10 customers = 1.0, 30 = 3.0)

**Dollar Impact**: `co_purchase_customer_count × avg_revenue_per_purchase` (estimated addressable revenue)

**Output Format**:
> **[CUSTOMER]** buys [ANCHOR ITEM] ([DESCRIPTION]) — [N] other customers also buy **[SUGGESTED ITEM]** ([DESCRIPTION]) within 90 days. [CUSTOMER] has never purchased it.
> Estimated opportunity: $[AVG_REVENUE] based on [N]-customer purchase pattern.

**Query**: Q-ORG-NBP

---

### SIG-OPP-02: Unactivated High-Value Accounts

**Priority**: P1
**Section Home**: Account Intelligence
**Data Gate**: `portal_orders` + `orders` (need both to compare)

**Detection**: Accounts in `portal_orders` (total business) with $50K+ LTM revenue but ZERO lifetime eCat orders.

**Fires when**: Account total business > $50K AND eCat orders = 0 AND account is NOT classified as Enterprise Channel (see exclusion below)

**Enterprise Channel Exclusion**: An account is classified as "Enterprise Channel" and EXCLUDED from this signal when ALL of the following are true:
- Total business LTM orders >= 500 (high-volume automated/EDI ordering pattern)
- Zero lifetime eCat orders
- The org does NOT have B2B Cart enabled (`HAS_CART = false`)

These accounts (e.g., Home Depot, Wayfair, Lowe's, Crate & Barrel) order through EDI, direct PO, or marketplace integrations and are not candidates for eCat iPad activation. They are surfaced separately in a collapsed "Enterprise Channel Accounts" callout in Account Intelligence — not as platform activation opportunities.

**Surprise Score**: `total_business_gmv / 100000` (scaled — $100K account = 1.0, $500K = 5.0)

**Dollar Impact**: Total business GMV (represents addressable platform activation)

**Output Format**:
> **[CUSTOMER]** — $[TOTAL_GMV] in total annual business, zero platform orders ever.
> Location: [CITY, STATE] | Orders: [COUNT] via other channels
> If 10% shifted to platform: ~$[POTENTIAL]

**Query**: Q-53 (from 2.0 library, already exists)

---

### SIG-OPP-03: Cross-Sell Category Whitespace

**Priority**: P1
**Section Home**: Account Intelligence (per-account)
**Data Gate**: `portal_order_items` OR `sales_data`

**Detection**: For a target account, identify categories where similar-state or same-territory customers spend significantly but this account spends $0.

**Fires when**: Category gap > $2K AND 5+ peer customers purchase in that category

**Surprise Score**: `peer_count / 5` (5 peers = 1.0, 15 = 3.0)

**Dollar Impact**: Peer average spend in that category

**Output Format**:
> **[CUSTOMER]** has $0 in [CATEGORY] — [N] similar customers average $[AVG] in this category.
> Gap: $[AVG]. Top items purchased by peers: [ITEM1], [ITEM2], [ITEM3].

**Query**: Q-ORG-NBP (category-level variant) or Q-57 (from 2.0)

---

### SIG-OPP-04: New Item Adoption Gap

**Priority**: P2
**Section Home**: Product Intelligence
**Data Gate**: `products.new_item = true` + `sales_data` or `portal_order_items`

**Detection**: Items flagged `new_item = true` that have zero or near-zero sales across the customer base, OR specific high-value customers who should be buying them (based on collection affinity) but aren't.

**Fires when**: New items exist with $0 platform orders AND customers who buy heavily from the same collection haven't purchased

**Surprise Score**: `collection_revenue_at_customer / 50000` (high collection affinity = high surprise at non-adoption)

**Dollar Impact**: Estimated from peer adoption rates

**Output Format**:
> **[N] new introductions with $0 platform adoption** — [TOTAL AVAILABLE]. Customers who buy heavily from [COLLECTION] but haven't tried new items: [CUSTOMER LIST with collection spend].

**Query**: Q-ORG-NEWITEM

---

## Category 4: Momentum Signals

### SIG-MOM-01: Account Acceleration

**Priority**: P0
**Section Home**: Account Intelligence
**Data Gate**: `portal_orders` OR `orders` with 6+ months

**Detection**: Accounts with QoQ revenue growth > 30% sustained for 2+ quarters.

**Fires when**: QoQ growth > 30% for 2+ consecutive quarters AND current quarter GMV > $10K

**Surprise Score**: `qoq_growth_pct / 30` (30% = 1.0, 60% = 2.0)

**Dollar Impact**: Current quarter GMV annualized minus prior-year annual (the growth delta)

**Output Format**:
> **[CUSTOMER]** — accelerating at [X]% QoQ for [N] consecutive quarters.
> Trajectory: $[Q-3] → $[Q-2] → $[Q-1] → $[Q-CURRENT]
> Annualized run rate: $[RATE] (up from $[PRIOR_YEAR])

**Query**: Q-ORG-VELOCITY

---

### SIG-MOM-02: Category Breakout

**Priority**: P2
**Section Home**: Product Intelligence
**Data Gate**: `sales_data` OR `portal_order_items` with 12+ months

**Detection**: Categories with YoY growth > 50% AND absolute growth > $25K.

**Fires when**: Category grew 50%+ YoY AND added $25K+ in absolute revenue

**Surprise Score**: `yoy_growth_pct / 50` (50% = 1.0, 100% = 2.0)

**Dollar Impact**: Absolute revenue growth

**Output Format**:
> **[CATEGORY]** — breakout growth at +[X]% YoY ($[PRIOR] → $[LTM]).
> Top items driving growth: [ITEM1] (+$[X]), [ITEM2] (+$[Y])
> Customers driving growth: [CUSTOMER1] (+$[X]), [CUSTOMER2] (+$[Y])

**Query**: Q-39 (from 2.0 library)

---

### SIG-MOM-03: AOV Uptrend / Migration Signal

**Priority**: P2
**Section Home**: Account Intelligence or Commerce Patterns
**Data Gate**: `portal_orders` OR `orders` with 6+ months

**Detection**: Accounts where quarterly average unit price is trending upward consistently (3+ quarters of increase).

**Fires when**: 3+ consecutive quarters of AOV increase AND latest AOV > 1.2x oldest in series

**Surprise Score**: `latest_aov / baseline_aov` (1.5x = moderately surprising)

**Dollar Impact**: `(latest_aov - baseline_aov) × recent_quarter_order_count × 4` (annualized AOV uplift)

**Output Format**:
> **[CUSTOMER]** — trading upmarket. Avg unit price: $[BASELINE] → $[LATEST] over [N] quarters (+[X]%).
> This customer is choosing higher-value products over time.

**Query**: Q-ORG-PRICE-SHIFT

---

## Category 5: Risk Signals

### SIG-RISK-01: Customer Revenue Concentration

**Priority**: P1
**Section Home**: Commerce Patterns or Account Intelligence
**Data Gate**: `orders` OR `portal_orders`

**Detection**: Compute top-5 customer share of total eCat (or total business) GMV.

**Fires when**: Top 5 customers represent > 40% of total GMV OR single customer > 20%

**Surprise Score**: `top5_share / 40` (40% = 1.0, 60% = 1.5)

**Dollar Impact**: GMV attributed to the concentrated accounts (at-risk if any single account churns)

**Output Format**:
> **Revenue concentration**: Top 5 accounts generate [X]% of total platform GMV ($[AMOUNT] of $[TOTAL]).
> [CUSTOMER1]: $[GMV] ([Y]%) | [CUSTOMER2]: $[GMV] ([Y]%) | ...
> If [TOP CUSTOMER] went dormant, you'd lose [Z]% of platform revenue overnight.

**Query**: Q-13 (from 2.0 library)

---

### SIG-RISK-02: Dormant High-Value Accounts

**Priority**: P0
**Section Home**: Account Intelligence
**Data Gate**: `orders` with 12+ months history

**Detection**: Accounts that previously ordered via eCat (LTM-ago period has orders) with > $15K historical eCat spend and zero orders in last 90 days.

**Fires when**: Historical eCat spend > $15K AND last order > 90 days ago

**Surprise Score**: `historical_gmv / 25000` (normalized — $25K = 1.0, $100K = 4.0)

**Dollar Impact**: Historical eCat GMV (revenue at risk of permanent loss)

**Output Format**:
> **[CUSTOMER]** — $[HISTORICAL_GMV] in historical eCat spend, last ordered [DATE] ([N] days ago).
> Was ordering every [AVG_INTERVAL] days. Current silence: [CURRENT_GAP] days ([RATIO]x normal).
> Rep: [REP_NAME if available] | State: [STATE]

**Query**: Q-17 (from 2.0 library, enhanced with interval data)

---

### SIG-RISK-03: Data Staleness (Platform Health)

**Priority**: P2 (escalates to P1 if staleness > 180 days on core entities)
**Section Home**: Platform Context
**Data Gate**: `data_versions` table

**Detection**: Check last import timestamp for each entity type. Flag any entity > 90 days stale.

**Fires when**: Any entity > 90 days since last import

**Surprise Score**: `days_stale / 90` (90 days = 1.0, 180 = 2.0, 365 = 4.0)

**Dollar Impact**: Not directly computable — use `1.0` as placeholder multiplier. Escalate to P1 if products/inventory/customers are stale (these directly affect ordering).

**Output Format**:
> **[ENTITY]**: last updated [DATE] ([N] days ago) — [FRESH/MONITOR/STALE]

**Query**: Q-08 (from 2.0 library)

---

### SIG-RISK-04: Rep Concentration

**Priority**: P1
**Section Home**: Team Intelligence
**Data Gate**: `orders` with rep attribution, 5+ active reps

**Detection**: Compute top-3 rep share of total eCat GMV.

**Fires when**: Single rep > 30% of total GMV OR top 3 reps > 60%

**Surprise Score**: `top_rep_share / 30` (30% = 1.0, 50% = 1.67)

**Dollar Impact**: Top rep's GMV (at-risk amount if rep leaves)

**Output Format**:
> **[REP_NAME]** generates [X]% of all platform revenue ($[GMV] of $[TOTAL]).
> If this rep left or disengaged, [X]% of eCat volume is at immediate risk.
> Next closest rep: [REP2] at $[GMV2] ([Y]%).

**Query**: Q-18 Part A (from 2.0 library)

---

## Category 6: Behavioral Intelligence Signals

### SIG-BEH-01: Presentation-to-Close Conversion Gap

**Priority**: P1
**Section Home**: Team Intelligence
**Data Gate**: BigQuery Mixpanel behavioral data + `orders`

**Detection**: For reps with 50+ customer-facing presentations (email_item_info, create_pdf_catalog, share_my_list), compute orders / presentations ratio.

**Fires when**: Rep has 50+ presentations AND conversion rate < 10% AND other reps with similar presentation volume convert at 25%+

**Surprise Score**: `peer_avg_conversion / rep_conversion` (peer at 25%, rep at 5% = 5.0x)

**Dollar Impact**: `(peer_conversion - rep_conversion) × rep_presentations × rep_aov`

**Output Format**:
> **[REP_NAME]** — [N] presentations across [M] accounts but only [K] orders ([X]% conversion).
> Peer average: [Y]% from similar activity volume. If [REP] converted at even half the peer rate, that's ~$[UPSIDE] in incremental annual GMV.
> Coaching focus: Post-presentation follow-up and closing workflow.

**Query**: Q-01 + Q-18 (from 2.0 library, cross-referenced)

---

### SIG-BEH-02: High-Activity Zero-Output Users

**Priority**: P2
**Section Home**: Team Intelligence
**Data Gate**: BigQuery Mixpanel + `orders`

**Detection**: Users with high platform engagement (1000+ total events) but < 5 orders in 12 months.

**Fires when**: 1000+ events AND < 5 submitted orders AND user is assigned an ordering role

**Surprise Score**: `total_events / 1000` (1000 events = 1.0, 5000 = 5.0)

**Dollar Impact**: Estimated from peer productivity — `peer_avg_gmv_per_1000_events × user_events / 1000`

**Output Format**:
> **[USER_NAME]** — [N] platform events but only [K] orders. Using the platform heavily for browsing/presentation but not closing.
> Compare: Users with similar engagement average [M] orders.

**Query**: Q-01 (from 2.0 library)

---

## Category 7: Commerce Signals

### SIG-COMMERCE-01: Capture Rate with Per-Point Dollar Math

**Priority**: P0
**Section Home**: Commerce Patterns
**Data Gate**: `portal_orders` + `orders` both present with 12+ months

**Detection**: Compute eCat GMV as percentage of total business GMV. Calculate the dollar value of each +1 percentage point of capture.

**Fires when**: Both data sources present AND capture rate is computable

**Surprise Score**: `(100 - capture_pct) / 20` (lower capture = more surprising/valuable the per-point math is. 10% capture = 4.5, 40% = 3.0)

**Dollar Impact**: `total_business_gmv / 100` (the dollar value of one capture point)

**Output Format**:
> **eCat captures [X]% of $[TOTAL] total business** — each +1 percentage point = $[PER_POINT]. Path to [TARGET]% = ~$[UPSIDE] in additional platform GMV (May 2025–May 2026).

**Query**: Q-45 + Q-16

---

### SIG-COMMERCE-02: Quote AOV Spread and Conversion Opportunity

**Priority**: P1
**Section Home**: Commerce Patterns
**Data Gate**: `orders` with 10+ Quote-type orders in LTM

**Detection**: Compare average Quote order value to average Confirmed order value. Compute the dollar opportunity from a 10-percentage-point improvement in quote-to-confirmed conversion.

**Fires when**: Quote AOV > 3x Confirmed AOV AND 10+ quotes exist

**Surprise Score**: `quote_aov / confirmed_aov` (3x = 3.0, 4.3x = 4.3)

**Dollar Impact**: `quote_count × quote_aov × 0.10` (10% conversion improvement scenario)

**Output Format**:
> **Quotes average $[QUOTE_AOV] vs $[CONFIRMED_AOV] confirmed ([RATIO]x spread)** — [N] quotes totaling $[QUOTE_GMV] in the trailing 12 months. A 10-percentage-point conversion improvement = ~$[UPSIDE] in incremental annual revenue [HYPOTHETICAL].

**Query**: Q-20

---

### SIG-COMMERCE-03: New Buyer Acquisition Decline

**Priority**: P1
**Section Home**: Commerce Patterns
**Data Gate**: `orders` with 12+ months history

**Detection**: Compare average monthly new eCat buyers in most recent 6 months vs. prior 6 months.

**Fires when**: Decline > 25% AND prior period averaged 10+ new buyers/month

**Surprise Score**: `ABS(pct_decline) / 25` (25% = 1.0, 55% = 2.2)

**Dollar Impact**: `(prior_avg_monthly - recent_avg_monthly) × 12 × avg_first_year_revenue_per_new_buyer`

**Output Format**:
> **New eCat buyer acquisition down [X]%** — from ~[PRIOR]/month ([PERIOD1]) to ~[RECENT]/month ([PERIOD2]). At this rate, natural customer attrition may outpace new platform onboarding.

**Query**: Q-41

---

## Category 8: Product Commerce Signals

### SIG-PRODUCT-01: Velocity × Stockout Collision

**Priority**: P1
**Section Home**: Product Intelligence
**Data Gate**: `inventories` + (`sales_data` OR `portal_order_items`) with velocity trend data

**Detection**: Cross-reference items with accelerating demand (QoQ volume increase > 30%) against current inventory. Flag items where velocity is increasing AND qty_available = 0.

**Fires when**: Any item with > 30% QoQ volume acceleration is at zero stock

**Surprise Score**: `velocity_increase_pct / 30` (30% acceleration = 1.0, 150% = 5.0)

**Dollar Impact**: Item's LTM revenue (demand exists but cannot be fulfilled)

**Output Format**:
> **[ITEM] ([DESCRIPTION]) — demand accelerating +[X]% while stocked out.** $[LTM_REVENUE] LTM, [UNITS] units sold, 0 available. [N] customers impacted. Next receipt: [DATE].
> This item's demand is growing and cannot be met.

**Query**: Q-38a + Q-ORG-STOCKOUT

---

## Category 9: Team Commerce Signals

### SIG-TEAM-01: Rep/Agency Capture Rate Gap

**Priority**: P1
**Section Home**: Team Intelligence
**Data Gate**: `portal_orders` with rep attribution + `orders` with 5+ active reps

**Detection**: For each rep/agency with > $500K in total business, compute their eCat capture rate. Flag reps at 0% capture on large total business volumes.

**Fires when**: Any rep/agency has 0% eCat capture on > $500K total business OR spread between highest and lowest capture > 30 percentage points

**Surprise Score**: `zero_capture_rep_count × (total_business_at_zero / 1000000)` (scaled by millions at 0% capture)

**Dollar Impact**: Total business flowing through reps at 0% capture (addressable platform revenue)

**Output Format**:
> **[N] reps/agencies at 0% eCat capture on $[TOTAL] total business** — [TOP_REP] leads at [X]% capture; [N] others at 0% on $[AT_ZERO] combined. If the bottom [M] matched even half the median capture rate, that's ~$[UPSIDE] in platform GMV [HYPOTHETICAL].

**Query**: Q-51 + Q-18

---

### SIG-TEAM-02: Presentation-to-Close Conversion Spread

**Priority**: P1
**Section Home**: Team Intelligence
**Data Gate**: BigQuery Mixpanel + `orders`, 3+ reps with 50+ presentations

**Detection**: For reps with 50+ customer-facing presentations, compute presentation-to-order conversion rate. Measure the spread between highest and lowest converters.

**Fires when**: Spread between top and bottom converters > 25 percentage points AND bottom rep has > $25K in territory revenue

**Surprise Score**: `spread_pct / 25` (25pt spread = 1.0, 40pt = 1.6)

**Dollar Impact**: `bottom_rep_presentations × (top_rep_conversion - bottom_rep_conversion) × bottom_rep_aov`

**Output Format**:
> **[TOP_REP] converts at [X]% vs [BOTTOM_REP] at [Y]% — [SPREAD]pt gap on similar presentation volume.** If [BOTTOM_REP] closed at even half [TOP_REP]'s rate, that's ~$[UPSIDE] in incremental annual GMV. Coaching focus: post-presentation follow-up workflow.

**Query**: Q-63 + Q-01 + Q-18

---

## Signal Count Summary

| Category | Signals | P0 | P1 | P2 |
|----------|---------|----|----|-----|
| Decay | 4 | 2 | 1 | 1 |
| Anomaly | 3 | 3 | 0 | 0 |
| Opportunity | 4 | 1 | 2 | 1 |
| Momentum | 3 | 1 | 0 | 2 |
| Risk | 4 | 1 | 2 | 1 |
| Behavioral | 2 | 0 | 1 | 1 |
| Commerce | 3 | 1 | 2 | 0 |
| Product Commerce | 1 | 0 | 1 | 0 |
| Team Commerce | 2 | 0 | 2 | 0 |
| **Total** | **26** | **9** | **11** | **6** |

**P0 Balance**: 5 negative (Decay×2, Anomaly×3) + 1 neutral (Risk-02) + 3 positive (MOM-01, OPP-01, COMMERCE-01). This ensures the Signal Summary always has positive P0 signals to draw from.

---

## Signals That Require Extended Data (The "If You Gave Us X" Layer)

These signals cannot fire today but are documented for when the data becomes available:

| Signal | Required Data | What It Would Enable |
|--------|--------------|---------------------|
| SIG-EXT-01: Full time-series product velocity | `invoice_date` on `sales_data` | Per-item demand curves over time, seasonal demand prediction, VM-38b completion |
| SIG-EXT-02: Channel-attributed competitive loss | `order_origin` populated on `portal_orders` | "This customer shifted $X from eCat to phone orders" — precise channel displacement |
| SIG-EXT-03: Multi-account relationship intelligence | Customer group/parent linkage | Wayfair-across-2-codes → $6.99M combined relationship, not two $3M accounts |
| SIG-EXT-04: Quote pipeline aging | Commitment/quote data with dates | "This customer has $X in uncommitted quotes aging past 60 days" |
| SIG-EXT-05: Fill-rate-to-reorder correlation | `invoice_date` + enhanced backorder tracking | "$X in lost repeat business because of fulfillment failures on specific items" |
