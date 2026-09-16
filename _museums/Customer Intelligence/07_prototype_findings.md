# Customer Intelligence Brief — Prototype Findings

> **Date**: 2026-06-15
> **Briefs Built**: 7 customers across 3 clients
> **Data Sources**: Postgres (portal_orders, portal_invoices, portal_invoice_items, customers, products, taxonomies, inventories, commitment_reports, placement_reports, orders, rma_requests, shipping_locations) + BigQuery (mixpanel.events)

---

## Executive Summary

We built 7 real Customer Intelligence Briefs using live production data across 3 clients representing different industries, customer types, and data richness levels. **The concept works.** Every brief produced genuinely actionable insights that a sales rep couldn't get from any other source — and several uncovered findings that the manufacturer themselves likely doesn't know about their own customers.

The strongest signals came from:
1. **Category-level YoY analysis** — every brief surfaced a clear story (Star Furniture's motion collapse, Capitol Lighting's furniture retreat, Kristen Finney's indoor expansion)
2. **Inventory cross-reference** — flagging zero-stock on a customer's top-selling items is immediately actionable
3. **Wallet share** — knowing you're 89% of Nebraska or 39% of Virginia reframes the entire conversation
4. **Rep engagement contrast** — the Kristen Finney vs. Ashley Gilbreath comparison is the single most compelling slide in the entire prototype set

---

## Briefs Built

| # | Client | Customer | Code | Type | LTM Revenue | YoY | Key Story |
|---|--------|----------|------|------|-------------|-----|-----------|
| 1 | UFI | Baer's Furniture | 3002 | Top | $5.23M | +25.8% | Accelerating giant, stale placements, zero eCat |
| 2 | UFI | Nebraska Furniture Mart | 1709 | Growth | $1.89M | +192.7% | Explosive growth, 89% of NE, Modern Sable-Desert anchor |
| 3 | UFI | Star Furniture | 1386 | Declining | $971K | -39.3% | Motion upholstery collapsed -79%, dining growing |
| 4 | CCI | Ferguson Enterprises | FER ENT | Top | $1.32M | +87.0% | Breakout dealer, 39% of VA, wall sconces +225% |
| 5 | CCI | Capitol Lighting Boca | CL BOCA | Declining | $950K | -6.2% | Pulling back from furniture, lighting core stable |
| 6 | SC | Kristen Finney | 1213728 | High-Engagement | $690K combined | +814% | Power user, 3 reps, eCat explosion |
| 7 | SC | Ashley Gilbreath | 1223388 | Declining | $79K | -45.0% | 5-month blackout, zero eCat, abandoned by rep |

---

## What Works (Sections That Produced Real Value)

### Tier 1 — Home Runs

**Category Breakdown with YoY (CQ-02)**
The single most consistently valuable section. Every brief told a clear story:
- Star Furniture: Motion upholstery collapsed from $636K → $149K, but dining chairs grew +78%. Without this view, the rep would only know "they're buying less" — not WHERE the loss is concentrated.
- Capitol Lighting: Tables -53%, Mirrors -64%, Cabinets -82% — they're retreating from non-lighting. Pendants +37% — lighting core is growing.
- Ferguson: Wall Sconces +225% — a new buying pattern the rep should lean into.

**Inventory Cross-Reference on Top SKUs (CQ-03)**
Found stock-out risks on high-velocity items in every brief:
- Baer's: 6 of top 15 items at zero inventory (Weekender Nightstand = 427 units/year, zero stock)
- Nebraska: Sable Nightstand (#2 at $106K) down to 28 units
- CCI: Nottaway Grande Bronze/Gold both at zero; Malvasia Sconce at zero

This is money on the table. If a rep shows up knowing "your best-seller is out of stock and here's when it's back," that's a different conversation.

**Wallet Share (CQ-22)**
Reframes every account relationship:
- Nebraska: 89% of all NE revenue — they ARE the Nebraska business
- Ferguson: 39% of VA — anchor account, 6.4x larger than #2
- Capitol Lighting: Still #1 in FL despite the decline, 3.5x #2
- Kristen Finney: 7% of all TN revenue, 22x the average customer

**Rep Engagement Contrast (CQ-13 — SC only)**
The Kristen Finney vs. Ashley Gilbreath comparison is the prototype's best showcase:
- Kristen: 359 Mixpanel events, 3 reps, 25 eCat orders, $571K eCat GMV
- Ashley: 71 events from ONE rep in a 10-day window, then a 5-month blackout
- Same org, same price level, vastly different outcomes. This is the insight that makes a VP of Sales write a check.

### Tier 2 — Consistently Useful

**Spend Trajectory (CQ-10)**
Quarterly trend tables clearly show inflection points:
- Nebraska's Apr 2025 jump from ~$100K to $320K/quarter
- Star Furniture's declining staircase pattern
- Kristen Finney's record Q2 2026 ($107K)

**Monthly Seasonality (CQ-08)**
Revealed actionable timing patterns:
- Baer's peaks in September and March (market cycle alignment)
- Kristen Finney is a burst buyer (Feb-May, then quiet)
- Ashley Gilbreath's historical Q2 peak is missing entirely in 2026

**Channel Mix (CQ-12)**
Immediately tells you how the customer operates:
- EDI-dominant (Ferguson 92%, Capitol 93%, Star 85%) = programmatic/automated
- Rep-driven (Kristen 98%) = high-touch relationship
- Customer-direct (Ashley 100%) = unmanaged self-service

**Account Lifecycle Stage (CQ-23)**
The growing/stable/declining/dormant classification worked well as a framing device, though it's more valuable as a label than as a section — it should go in the header, not as a standalone section.

### Tier 3 — Situationally Valuable

**Market Commitments (CQ-17)**
Only available for UFI (the only org with commitment_reports). When present, highly valuable:
- Baer's APR2026 commitment dropped from 112 items to 23 — is this a signal?
- Star Furniture: Consistent 18-24 items per market despite revenue decline — still engaged
- Nebraska: Commitments growing (3→11→24→45→25) — mirrors revenue trajectory

**Collection Mix (CQ-04)**
Useful for broad-assortment buyers (Baer's buys 10+ collections) but less interesting for concentrated buyers. Works best as a complement to category breakdown.

**Showroom Placements (CQ-18)**
The data itself was universally stale (all records from 2019-2020), but that staleness is itself an insight — it flags "nobody has audited the floor in 6 years" which is an action item.

---

## What Falls Flat (Sections That Need Rework)

### Buyer Intelligence (CQ-14)
**Status: Mostly empty.** Buyer name is unpopulated for 6 of 7 customers. The only useful data was in SC where channel mix showed REP vs CUSTOMER ordering — but buyer_name itself was blank everywhere. For EDI/portal-heavy accounts, buyer attribution doesn't flow through the order data.

**Recommendation**: Demote to conditional rendering. Only show when buyer_name has > 1 distinct value with meaningful data. Replace with "Ordering Pattern" section that uses channel mix + order origin to characterize the buying behavior instead.

### Returns / RMA (CQ-16)
**Status: Zero data for all 7 customers.** No RMA requests found for any customer across all 3 clients. Either returns are rare in furniture/lighting, or RMA tracking is underutilized by these orgs.

**Recommendation**: Keep gated — only render when data exists. Don't remove the query; it will matter for orgs that use RMA tracking. But don't include an empty "No returns found" section in the brief.

### eCat Orders for Large Retailers (CQ-01 eCat portion)
**Status: Zero or negligible for 5 of 7 customers.** Baer's, Nebraska, Star, Ferguson, Capitol Lighting — none use the eCat iPad app for ordering. They're EDI/portal accounts. The eCat penetration metric is only relevant for designer-segment accounts (SC).

**Recommendation**: Conditional rendering. If eCat orders = 0 for both LTM and prior, collapse this section to a single note ("Account does not use eCat iPad — orders via [channel]") rather than showing a table full of zeros.

### Rep Engagement for Non-SC Orgs (CQ-13)
**Status: No customer-level data for UFI or CCI.** Mixpanel events either don't carry `selected_bill_to_code` for these orgs, or reps aren't selecting customers before taking actions. CCI only showed `api_access` events (system-level, not rep-level).

**Recommendation**: This section is transformational for SC but invisible for UFI/CCI. Gate on whether the org's Mixpanel data actually has `selected_bill_to_code` populated. For orgs without it, skip entirely rather than showing "No data available."

### Same-Store Comps (CQ-21)
**Status: Not tested — ship-to data was sparse in portal_orders.** Baer's returned empty ship-to results despite having 39 ship-to locations in the customer record. The ship-to fields may not be reliably populated in portal_orders.

**Recommendation**: Test further. If ship-to data isn't populated in portal_orders, try joining through `shipping_locations` table or using `portal_order_items` ship-to fields instead.

### Next Best Product (CQ-06) / Cross-Sell (CQ-19) / Reorder Decay (CQ-09)
**Status: Not run in prototypes** — these are computationally expensive queries that were deprioritized to focus on the core sections. The queries are written but unvalidated.

**Recommendation**: Validate in a follow-up session. These represent the "advanced insights" tier and should be tested on a customer with rich purchase history (Baer's or Ferguson would be ideal candidates).

---

## Data Quality Issues

### Product Categorization Gaps
**Severity: Medium.** "Uncategorized" was the #1 category for Baer's (24.9% of spend) and appeared in other briefs. Products missing `category_code` in the product catalog fall into this bucket. This limits the category-level analysis that is otherwise the brief's strongest section.

**Impact**: Understates category trends. If 25% of spend is uncategorized, the category breakdown is telling an incomplete story.

**Fix**: Org-level data quality — encourage clients to assign categories to all products. Could also build a "categorization coverage" metric into the org-level report.

### Collection Taxonomy Mapping
**Severity: Low-Medium.** CCI's collection data was 85-88% "Core / Unassigned" — their product catalog doesn't heavily use the collection taxonomy. SC had similar gaps with SCH-prefix items not mapped to collections.

**Impact**: Collection mix section is less useful for these orgs. Category breakdown is more reliable.

### Stale Placement Data
**Severity: Medium.** Every placement record across all UFI customers was from 2019-2020 (2,300-2,800 days old). CCI's placement data was more current.

**Impact**: Placement sections show historical state, not current floor presence. The staleness itself is valuable to flag, but the data can't be used for "current placements" claims.

### Commitment Report Items (jsonb parsing)
**Severity: Low.** Commitment items are stored as jsonb arrays. We retrieved counts but didn't parse individual item numbers for conversion rate analysis (CQ-17 Step 2). This would be the next step to answer "what did they commit to vs. what did they actually buy?"

---

## Refined Section Design (v2)

Based on the prototype findings, here's the recommended brief structure:

### Always-On Sections
1. **Header** — Name, code, location, price level, territory, ship-to count, lifecycle stage badge, last order recency
2. **Account at a Glance** — Total business LTM vs. prior, YoY change. eCat metrics only if > 0. Days since last order as a risk signal.
3. **Purchase DNA — Categories** — Category breakdown with YoY. The single most valuable section.
4. **Purchase DNA — Top Items** — Top 10-15 SKUs with inventory status flags. Stock-out alerts called out separately.
5. **Spend Trajectory** — Quarterly trend with QoQ changes. Visual sparkline ideal.
6. **Buying Rhythm** — Orders/month, days between, active months. Monthly seasonality pattern.
7. **Channel Mix** — How they order (EDI/portal/eCat/OCC).
8. **Wallet Share** — vs. same-state cohort avg and max. Rank within state.
9. **Lifecycle Assessment** — Stage classification + narrative summary.

### Conditional Sections (render only when data exists)
10. **Market Commitments** — Gate: commitment_reports > 0. Show history + commitment-to-conversion analysis.
11. **Showroom Placements** — Gate: placement_reports > 0. Flag staleness if > 1 year old.
12. **Rep Engagement** — Gate: Mixpanel events with selected_bill_to_code > 0. Event mix + rep breakdown + handoff detection.
13. **Buyer Intelligence** — Gate: > 1 distinct buyer_name with revenue. Otherwise skip.
14. **Returns** — Gate: rma_requests > 0. Otherwise skip.
15. **Collection Mix** — Gate: < 50% "Uncategorized/Core". Otherwise fold into category section.

### Summary Section (always-on)
16. **Strategic Summary** — 3-5 bullet narrative: strengths, risks, opportunities, rep talking points.

### Advanced Insights (future tier)
17. **Reorder Decay Detection** — Per-SKU velocity tracking
18. **Next Best Product** — Purchase sequence analysis
19. **Cross-Sell Opportunity** — Category gap vs. cohort
20. **Category Share Evolution** — Mix shift analysis

---

## What Makes This Product Monetizable

After building 7 real briefs, the value proposition is clear:

**For the manufacturer (our client)**:
- No one else can produce this. The data lives in SuperCat's systems — our client's ERP doesn't have cross-referenced eCat/Mixpanel/portal/commitment data in one view.
- The category-level YoY analysis alone is worth the subscription. Star Furniture's motion collapse (-79%, $557K lost) is the kind of insight that triggers a VP of Sales call.
- Inventory cross-referencing (top items at zero stock) is operational intelligence that prevents lost sales.

**For the sales rep**:
- Walk into every meeting with complete account knowledge.
- Know what the customer buys, when they buy it, what's growing, what's declining, what's in stock, and whether they're ahead or behind their commitment.
- The wallet share framing transforms the conversation from "how do I sell more" to "here's where you stand relative to similar accounts."

**What makes it better than a spreadsheet**:
- YoY trending, lifecycle classification, and cohort comparison are computed insights, not raw data.
- Conditional rendering means the brief adapts to what's relevant — a designer account gets rep engagement data while a big-box retailer gets commitment/placement analysis.
- The "Uncategorized" finding is itself a product feedback loop — it tells our client where their data is incomplete.

**Pricing signal**: This is a per-customer, per-quarter deliverable. At 50-100 key accounts per manufacturer, this is a $5-10K/year add-on that pays for itself if it saves one relationship or identifies one at-risk account.

---

## Next Steps

1. **Validate advanced queries** (CQ-06, CQ-09, CQ-19, CQ-20) on Baer's and Ferguson
2. **Build the brief generator** — parameterized prompt that takes (org_id, customer_code) and produces a complete brief
3. **Test commitment-to-conversion analysis** — parse jsonb items from commitment_reports, cross-reference against post-commitment portal_order_items
4. **Explore ship-to level analysis** — investigate why portal_orders ship-to fields were empty for UFI
5. **Design the delivery format** — PDF vs. markdown vs. interactive dashboard
6. **Pilot with one client** — UFI is the obvious candidate (richest data, commitment + placement, large account base)
