# Section 3 Context Bundle — EGLO Canada (eglo_can)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — EGLO Canada (eglo_can, org_id=232)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=1691 |
| HAS_SALES_DATA | True | sales_data_count=6618 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 17 | engagement_reps=17 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 26 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 43, Mixpanel total submit_order (Q-01): 130 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=73.1%, ambiguous_rate=73.7%, showroom_event_share=38.1% |
| USER_GROUP_JOIN_RATE | 73% | 19 of 26 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 38% | showroom+admin share of matched events: 38.1% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Karen Hoffman |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=495 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: EGLO Canada
- **Shortname**: eglo_can
- **Org ID**: 232
- **Bundle**: 4
- **Bundle label for report**: 4

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — EGLO Canada (eglo_can, org_id=232)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| PORTAL_ORDERS_FRESH | False |
| HAS_PORTAL_ORDERS | False |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | PARTIAL | See Derived Gate 6 §5 formula |

## Section Guide — section_03_product.md

# Section Guide: Product Intelligence
> **v3.0** — signal-first architecture. Item-level intelligence, not category summaries.

## Section Identity

- **id**: `product`
- **title**: Product Intelligence
- **section number**: 3
- **include when**: `signal_rank.md` shows ≥ 1 P0/P1 signal with `Section Home = Product Intelligence` OR alternate data gate passes (`HAS_INVENTORY = true` AND `HAS_SALES_DATA = true`)
- **skip when**: < 1 P0/P1 product-level signal fired AND alternate data gate fails (neither `HAS_INVENTORY` nor `HAS_SALES_DATA` is true)

## Query Inputs

Read these cache files:

- `cache/signal_rank.md` — ranked signal manifest
- `cache/Q-07_results.md` — Catalog completeness
- `cache/Q-37_results.md` — Top items by revenue with inventory position
- `cache/Q-38a_results.md` — Item velocity trends
- `cache/Q-39_results.md` — Collection/category mix and YoY change
- `cache/Q-42_results.md` — New introduction performance (also provides total new-item count consumed by subsection 6)
- `cache/Q-59_results.md` — Fill rate & backorder revenue impact (**MANDATORY when gate met**)
- `cache/Q-61_results.md` — New introduction adoption gap — returns ONLY items with ≥1 buyer
- `cache/Q-ORG-GHOST_results.md` — Ghost SKU detection
- `cache/Q-ORG-STOCKOUT_results.md` — Stock-out impact with customer cross-reference
- `cache/Q-ORG-NEWITEM_results.md` — New item adoption gaps
- `cache/gate_flags.md` — for `HAS_SALES_DATA`, `HAS_INVENTORY`, `HAS_CART`, `HAS_PORTAL_ORDERS`, `HAS_NEW_ITEMS`
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_3` tier

---

## Fragment Structure

Uses the standard `<details class="section-collapse">` wrapper per shared_rules.md Section E.

```
Section ID: product
Section Number: §3
```

---

## PRE-BUILD GATE CHECK

> Follow `section_shared_contract.md` §1 for the gate check process.

| Subsection | Mandatory? | Gate | Action if gate met |
|---|---|---|---|
| 1. Fill Rate & Revenue Impact (Q-59) | **MANDATORY** | `HAS_PORTAL_ORDERS = true` AND `Q-59_results.md` has data rows | MUST render — omission is a defect |
| 6. New Introduction Performance + Adoption Gap (Q-42/Q-61) | **MANDATORY** when Q-61 gate met | `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND `Q-61_results.md` has data rows | MUST render full arc (Q-42 metrics + Q-61 table) |
| 8. Catalog Completeness (Q-07) | **MANDATORY** | Always | MUST render |

**CONFIDENCE HEADER**: Every §3 fragment MUST contain a confidence header **at the top of the section** (immediately after the header metrics, before any subsection content). This is NOT optional — if the confidence header is missing, the fragment is defective. Read `SECTION_CONFIDENCE_3` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags.

---

## Content Blocks (render in NARRATIVE ARC order)

**Rendering order within this section (strength → intelligence → opportunity → risk):**
3. Top Sellers & Inventory Position (STRENGTH — what's selling well)
7. What's Selling — Category & Collection (INTELLIGENCE — the full picture)
8. Catalog Completeness (INTELLIGENCE — operational health)
6. New Introduction Performance + Adoption Gap (INTELLIGENCE + OPPORTUNITY)
5. Velocity Signals (INTELLIGENCE — accelerating leads, decelerating follows)
1. Fill Rate & Revenue Impact (RISK — operational, render after positive context)
2. Ghost SKU Registry (RISK — catalog gap)
4. Stock-Out Impact Board (RISK — render late)

### 1. Fill Rate & Revenue Impact (Q-59)

**MANDATORY RENDER**: If `cache/Q-59_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

This is a P0-level insight. When fill rate is below 85%, it leads the section as the most urgent product signal.

**Data source**: `cache/Q-59_results.md`

**Rendering**:

**Part A — Org Fill Rate (from the `ORG_SUMMARY` row):**

Render a `.metrics-grid` with 2–3 metric cards:
- **Fill Rate**: `fill_rate_pct` displayed as `XX.X%` with badge:
  - `.badge.ok` if ≥ 95%
  - `.badge.warn` if 85–94.9%
  - `.badge.danger` if < 85%
- **Units Unfilled**: `total_unfilled` with label "Units not shipped (trailing 12 months)"

If fill rate < 85%, add a `.callout.alert`:

```html
<div class="subsection">
  <div class="subsection-title">Fill Rate & Revenue Impact</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-value">{{FILL_RATE_PCT}}% <span class="badge {{BADGE_CLASS}}">{{BADGE_LABEL}}</span></div>
      <div class="metric-label">Order Fulfillment Rate</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">{{UNITS_UNFILLED}}</div>
      <div class="metric-label">Units not shipped (trailing 12 months)</div>
    </div>
  </div>

  {{IF fill_rate < 85%:}}
  <div class="callout alert">
    <div class="callout-title">Fulfillment Below Target</div>
    <p>Your fill rate is {{GAP}} points below the 95% benchmark. At this level, roughly 1 in {{1/(1 - fill_rate)}} ordered units is not being shipped — that's a customer retention risk when buyers learn they can't rely on consistent fulfillment.</p>
  </div>
```

**Part B — Top Backordered Items (from `ITEM` rows):**

Render a table with these exact columns:

| Column | Content |
|--------|---------|
| Item | Item number + description (e.g., "AS41G — CopperSmith Adam Street Lantern") |
| Category | Product category |
| Qty Backordered | Units currently on backorder |
| Customers Affected | Distinct customers waiting |
| Avg Unit Price | Average unit price |
| Exposure | `backorder_exposure` formatted as dollars — units × price |
| Annual Revenue | Trailing 12-month revenue for this item |

Sort by exposure descending (already sorted in cache). Show top 5 visible; remaining in collapsed `<details>`.

```html
  <table>
    <tr>
      <th>Item</th><th>Category</th><th>Qty Backordered</th>
      <th>Customers Affected</th><th>Avg Unit Price</th>
      <th>Exposure</th><th>Annual Revenue</th>
    </tr>
    {{ROWS — sorted by exposure desc, top 5 visible, rest in <details>}}
  </table>

  <div class="callout alert">
    <div class="callout-title">Revenue at Risk from Fulfillment Gaps</div>
    <p>These {{N}} items represent ${{SUM_ANNUAL_REVENUE}} in annualized revenue across {{TOTAL_CUSTOMERS}} customers. Persistent backorders correlate with longer reorder intervals — addressing these stockouts could protect an estimated ${{PROJECTED_AT_RISK}} in annual business.</p>
  </div>

  <div class="what-this-means">
    <strong>Action:</strong> An {{FILL_RATE_PCT}}% fill rate means roughly 1 in {{RATIO}} ordered units is not being shipped. Persistent stockouts train buyers to look elsewhere — each unfulfilled order is an opportunity for a competitor to earn the next one. The items above represent your highest-exposure gaps; resolving the top 3 addresses the majority of at-risk revenue.
  </div>
</div>
```

**Claim rules**: "Your order fulfillment rate is X%." Use "fulfillment rate" or "fill rate" interchangeably. The causal link between backorders and reorder decay is always hedged. Never claim "you are losing $X" — say "projected at-risk revenue is estimated at $X if backorder patterns persist." Never use internal table names. Reference items by description, not bare item numbers.

### 2. Ghost SKU Registry (conditional: SIG-ANOMALY-01 fired)

**Gate**: `Q-ORG-GHOST_results.md` has data rows AND any ghost SKU with > $5K LTM revenue.

Every item invoiced with no catalog record. This is a P0 signal — if it fired, it leads after fill rate.

```html
<div class="subsection">
  <div class="subsection-title">Ghost SKU Registry</div>
  <div class="callout alert">
    <div class="callout-title">{{N}} items invoiced with no catalog record</div>
    <p>These items generated ${{TOTAL_REVENUE}} in the trailing 12 months but don't exist in your product catalog. Without a catalog record, reps can't verify stock, customers can't see images, and the item is invisible to your digital ordering tools.</p>
  </div>
  <table>
    <tr><th>Item Code</th><th>LTM Revenue</th><th>Units Sold</th><th>Customers Ordering</th></tr>
    {{ROWS — sorted by LTM revenue desc, top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> Each ghost SKU is a catalog gap — revenue is flowing for items your platform can't present, price, or track inventory for. Adding these items to your catalog takes minutes and immediately makes them orderable, searchable, and reportable. Start with the highest-revenue items.
  </div>
</div>
```

"Customers Ordering" column: list customer names (up to 3), with "+N more" if > 3.

### 3. Top Sellers & Inventory Position (Q-37)

**Gate**: `HAS_SALES_DATA = true` AND `HAS_INVENTORY = true` (both required)

**Data source**: `cache/Q-37_results.md`

Top-selling products with their current inventory status — the intersection of demand and supply. Surface proven sellers and flag inventory gaps before they become stockouts.

```html
<div class="subsection">
  <div class="subsection-title">Top Sellers & Inventory Position</div>
  <table>
    <tr>
      <th>Item</th><th>Category</th><th>LTM Revenue</th><th>Units Sold</th>
      <th>Qty Available</th><th>On Hand</th><th>Backorder</th><th>Next Receipt</th>
    </tr>
    {{ROWS — sorted by LTM revenue desc, top 10 visible, rest in <details>}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> These are your highest-revenue products and their current supply position. Items with strong sales and zero or low available inventory are your most urgent replenishment priorities — they have proven demand and an empty shelf. Items with healthy stock represent revenue you can reliably fulfill. Focus on any top seller where Qty Available is zero and Next Receipt is blank or more than 30 days out.
  </div>
</div>
```

**Column details:**
- "Item": Description with item code in parentheses (e.g., "CopperSmith Adam Street Lantern (AS41G)")
- "Qty Available": Render `0` with `.badge.danger`
- "Backorder": Render values > 0 with `.badge.warn`
- "Next Receipt": Date if available, "Unknown" with `.badge.warn` if not
- Top 10 visible, remaining in collapsed `<details>`

**`what-this-means` close**: Frame around revenue protection. These are proven sellers — quantify the cumulative LTM revenue of the top items shown. Call out any item with zero availability and no scheduled receipt date as the highest-risk gap. Tone: "Your best-sellers are generating demand you can't fill right now. The [item with no receipt date] has no restock scheduled — that's the most urgent gap."

### 4. Stock-Out Impact Board (conditional: SIG-ANOMALY-02 fired)

**Gate**: `Q-ORG-STOCKOUT_results.md` has data rows AND top-selling items at zero inventory.

Top items at zero stock cross-referenced with who buys them and what alternatives exist.

**⚠ STRATEGIC FRAMING MANDATE**: This subsection is NOT a warehouse report. A VP of Sales already knows what's out of stock — their ops team tells them daily. The intelligence value is:
1. **Which customers are impacted** (named, with dollar exposure per customer)
2. **What alternatives to recommend** (in-stock substitutes for proactive rep outreach)
3. **Revenue at risk per relationship** (not per SKU)

If customer impact data or alternatives cannot be populated, this subsection MUST still frame the stock-out through a customer-relationship lens. Never render a bare list of stocked-out items without customer context — that is an inventory report, not intelligence.

```html
<div class="subsection">
  <div class="subsection-title">Stock-Out Impact Board</div>
  <div class="callout alert">
    <div class="callout-title">{{N}} top-selling items at zero availability — {{TOTAL_CUSTOMERS}} customer relationships exposed</div>
    <p>These items generated ${{TOTAL_LTM_REVENUE}} in trailing-12-month revenue. The intelligence value isn't the stockout itself — it's knowing which customers to call TODAY with an alternative recommendation before they find one elsewhere.</p>
  </div>
  <table>
    <tr>
      <th>Item</th><th>Description</th><th>Collection</th>
      <th>LTM Revenue</th><th>Units Sold</th><th>Qty Available</th>
      <th>Next Receipt</th><th>Top Customers Impacted</th><th>Alternatives (in-stock)</th>
    </tr>
    {{ROWS — sorted by LTM revenue desc, top 5 visible, rest in <details>}}
  </table>

  <div class="callout opportunity">
    <div class="callout-title">Proactive Outreach Script</div>
    <p>For each stocked-out item above, your reps have a ready-made customer conversation: "I noticed [item] is temporarily out of stock and I know you've ordered it before. I wanted to let you know we have [alternative] available now, and I'll flag you for priority fulfillment when [item] restocks {{IF next_receipt_date: 'around [date]'}}." This protects the relationship and demonstrates attention.</p>
  </div>

  <div class="what-this-means">
    <strong>Action:</strong> These items are generating demand you can't fulfill — and {{TOTAL_CUSTOMERS}} customers are waiting. Each stocked-out SKU is an active revenue leak: customers who reorder these items regularly will either wait (losing urgency), find a substitute themselves (losing your margin control), or go to a competitor (losing the relationship). The customer names above are your Monday morning call list — proactive outreach with an alternative recommendation protects the relationship even when you can't fill the order.
  </div>
</div>
```

**Column details:**
- "Qty Available": Render `0` with `.badge.danger`
- "Next Receipt": Date if available, "Unknown" with `.badge.danger` if not (escalated from `.warn` — unknown restock on a top seller is a bigger problem)
- "Top Customers Impacted" (**MANDATORY — never leave blank**): Up to 3 customer names by LTM revenue for that item, with their individual LTM spend on the item. Format: "Customer A ($X), Customer B ($Y), Customer C ($Z)". If customer-level data is unavailable from the cache, state "Customer impact data unavailable — request customer-level order detail for next cycle" in a `.prose` note below the table.
- "Alternatives (in-stock)" (**MANDATORY — never leave blank**): Up to 3 items from the same collection with qty_available > 0. Show item code, description, qty available. If no alternatives exist, show "None in collection — cross-collection alternatives may be available" with `.badge.warn`. The absence of alternatives is itself intelligence: it means the rep's ONLY play is the restock timeline.

### 5. Velocity Signals (conditional: Q-38a has acceleration/deceleration data)

**Gate**: `Q-38a_results.md` has item-level velocity trends showing meaningful acceleration or deceleration. Proxy: `HAS_PORTAL_ORDERS = true` and ≥ 3 real products with velocity data after filtering fee items and freight charges.

Items with growing demand vs. fading demand, with customer attribution showing WHO is driving the change.

```html
<div class="subsection">
  <div class="subsection-title">Item Velocity Signals</div>

  <div class="callout opportunity">
    <div class="callout-title">Accelerating Items</div>
  </div>
  <table>
    <tr><th>Item</th><th>Description</th><th>Collection</th><th>QoQ Revenue Change</th><th>LTM Revenue</th><th>Top Customers Driving Growth</th></tr>
    {{TOP 5 ACCELERATING ITEMS}}
  </table>

  <div class="callout alert">
    <div class="callout-title">Decelerating Items</div>
  </div>
  <table>
    <tr><th>Item</th><th>Description</th><th>Collection</th><th>QoQ Revenue Change</th><th>LTM Revenue</th><th>Customers Pulling Back</th></tr>
    {{TOP 5 DECELERATING ITEMS}}
  </table>

  <div class="what-this-means">
    <strong>Action:</strong> Accelerating items represent demand to protect — ensure inventory and rep awareness. Decelerating items may signal product lifecycle maturity, competitive substitution, or changing customer preferences. The customer attribution tells you whether the shift is broad-based or driven by one or two accounts changing behavior.
  </div>
</div>
```

**Customer attribution columns:**
- "Top Customers Driving Growth": Up to 3 customers with the largest positive revenue change for that item, with dollar delta
- "Customers Pulling Back": Up to 3 customers with the largest negative revenue change, with dollar delta

QoQ Revenue Change: use `.badge.ok` for growth, `.badge.danger` for decline. Show as percentage and absolute dollars.

**Omission rule**: If after filtering fee items fewer than 3 real products remain with meaningful velocity data, omit this subsection silently.

### 6. New Introduction Performance (Q-42) + Adoption Gap (Q-61/Q-ORG-NEWITEM)

**Gate (Part A — Q-42)**: `HAS_SALES_DATA = true`
**Gate (Part B — Q-61)**: `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND `cache/Q-61_results.md` has data rows. **MANDATORY when gate met.**

**Data sources**:
- `cache/Q-42_results.md` — new introduction performance and total new-item count
- `cache/Q-61_results.md` — contains ONLY items with ≥1 buyer (the adopted items)
- `cache/Q-ORG-NEWITEM_results.md` — new item adoption gaps with customer cross-reference

**Narrative arc**: This subsection tells a complete story: how many new items launched → what revenue they generated → how broadly accounts adopted them → where the traction gap is → what to do about it.

**Part A — Launch Metrics (Q-42):**

Render a `.metrics-grid` with:
- **New Items**: total count of new introductions
- **Revenue Generated**: total revenue from new items (with time qualifier)

Follow with a brief prose note identifying any notable collection or category trends among new items. If any collection has multiple new items with zero sales, flag it as warranting attention.

**Part B — Adoption Gap (Q-61 + Q-ORG-NEWITEM):**

When Q-61 gate is met, derive key metrics (Q-61 returns only adopted items, so totals must be cross-referenced with Q-42):
- `total_new_items` = total new item count from Q-42
- `adopted_items` = row count of Q-61
- `adoption_rate` = `adopted_items / total_new_items` as percentage
- `zero_traction_count` = `total_new_items - adopted_items`
- `adopted_revenue` = sum of `revenue` column in Q-61

Open Part B with a `.callout.insight` titled "New Introduction Adoption" summarizing all five derived metrics in a single narrative sentence:

Example: "You launched 369 new items. 30 have been ordered by at least one account (8% adoption), generating $911K in trailing-12-month revenue. 339 items have zero traction."

Then render:

**(i) Top Performers** — from Q-61 rows, sorted by revenue descending (show top 5–8 visible; remaining in collapsed `<details>`):

| Column | Content |
|--------|---------|
| Item | `description` (fall back to `item_number` only if description is blank — never expose raw item codes as the primary identifier) |
| Category | `category` |
| Buyers | `buyers` |
| Qty Sold | `qty_ordered` |
| Revenue | `revenue` formatted as currency |
| List Price | `list_price` formatted as currency |

**(ii) Zero-Traction Callout** — Q-61 returns only adopted items, so individual zero-traction items are **not available** in the data. Render a `.callout.warn` (NOT a table) with:
- Title: "Zero-Traction New Items"
- Body: "`zero_traction_count` new items have zero orders in the trailing 12 months. These may need rep attention, merchandising updates, or pricing review. High-list-price items with no traction represent the largest opportunity cost."

**IMPORTANT**: Do NOT render an empty zero-traction `<table>` with an empty `<tbody>`. The count-based callout is the correct treatment when individual zero-traction rows are not in the query results.

**(iii) Customer Cross-Reference (Q-ORG-NEWITEM):**

When `Q-ORG-NEWITEM_results.md` has data rows, cross-reference new introductions with customers who buy heavily from the same collection but haven't tried the new items.

```html
  {{FOR EACH COLLECTION WITH UNADOPTED NEW ITEMS:}}
  <p class="prose"><strong>{{COLLECTION_NAME}}:</strong> {{M}} new items, $0 platform revenue. Customers who buy deeply in {{COLLECTION_NAME}} but haven't tried the new items:</p>
  <table>
    <tr><th>Customer</th><th>Collection Spend (LTM)</th><th>New Items Purchased</th></tr>
    {{ROWS — customers with high collection spend and 0 new item purchases}}
  </table>
```

Group by collection. Show up to 3 collections with the highest gap (most new items × most collection-active customers). Customers in each collection table: top 5 by collection spend, rest in `<details>`.

```html
<div class="subsection">
  <div class="subsection-title">New Introduction Performance & Adoption</div>

  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-value">{{TOTAL_NEW_ITEMS}}</div>
      <div class="metric-label">New Items Launched</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">${{NEW_ITEM_REVENUE}}</div>
      <div class="metric-label">Revenue from new items (trailing 12 months)</div>
    </div>
  </div>

  {{IF Q-61 gate met:}}
  <div class="callout insight">
    <div class="callout-title">New Introduction Adoption</div>
    <p>You launched {{TOTAL_NEW_ITEMS}} new items. {{ADOPTED_ITEMS}} have been ordered by at least one account ({{ADOPTION_RATE}}% adoption), generating ${{ADOPTED_REVENUE}} in trailing-12-month revenue. {{ZERO_TRACTION_COUNT}} items have zero traction.</p>
  </div>

  {{TOP PERFORMERS TABLE}}

  <div class="callout warn">
    <div class="callout-title">Zero-Traction New Items</div>
    <p>{{ZERO_TRACTION_COUNT}} new items have zero orders in the trailing 12 months. These may need rep attention, merchandising updates, or pricing review. High-list-price items with no traction represent the largest opportunity cost.</p>
  </div>

  {{COLLECTION CROSS-REFERENCE TABLES from Q-ORG-NEWITEM}}

  <div class="what-this-means">
    <strong>Action:</strong> An {{ADOPTION_RATE}}% adoption rate means {{ZERO_TRACTION_COUNT}} new items haven't reached a single buyer yet. The top performers prove the line has appeal — the gap is in awareness and rep activation. Focused training on new introductions and featured placement in rep-facing lists can close this gap. The customer cross-reference above shows your warmest leads — accounts already buying from the same collections who simply haven't been shown the new additions.
  </div>
</div>
```

**When Q-61 gate is NOT met** (Part A only renders): Make the `what-this-means` close self-contained — focus on revenue per new item, which collections are gaining traction, and whether launch velocity meets expectations.

**Claim rules**: "You launched X new items. Y have been purchased by at least one account." Never expose item_number if it contains internal codes — use description. Frame zero-traction items as opportunity, not failure: "may need attention" not "are failing."

### 7. What's Selling — Category & Collection Breakdown (Q-39)

**Gate**: `HAS_SALES_DATA = true`

**Data source**: `cache/Q-39_results.md` (which may produce separate category and collection result files)

The full category and collection performance view. Render as a **single subsection** — do not split into separate subsections for category and collection.

**Part A — Category Breakdown:**

Lead with a `.callout.insight` identifying the dominant category by sales share and any collections with outsized per-item performance.

Table columns:
- Category
- Qty Sold
- Sales
- Items
- Sales/Item

**Part B — Collection Breakdown (in collapsed `<details>`):**

Table columns:
- Collection
- Items
- Qty Sold
- Sales

**Part C — Significant Mix Shifts (conditional callout within this subsection):**

If `Q-39_results.md` shows categories or collections gaining or losing > 3 share points YoY, include a `.callout.insight` with the significant movers. This replaces the previous standalone Collection Mix Evolution subsection.

```html
<div class="subsection">
  <div class="subsection-title">What's Selling — Category & Collection Breakdown</div>

  <div class="callout insight">
    <div class="callout-title">{{DOMINANT_CATEGORY}} drives {{SHARE}}% of sales</div>
    <p>{{DOMINANT_CATEGORY}} accounts for {{SHARE}}% of total revenue across {{ITEM_COUNT}} items. {{COLLECTION_NOTE — e.g., "The Artisan collection stands out with $X per item, 2× the category average."}}</p>
  </div>

  <table>
    <tr><th>Category</th><th>Qty Sold</th><th>Sales</th><th>Items</th><th>Sales/Item</th></tr>
    {{CATEGORY ROWS — all categories, sorted by sales desc}}
  </table>

  <details class="table-collapse">
    <summary>Collection Breakdown ({{N}} collections)</summary>
    <table>
      <tr><th>Collection</th><th>Items</th><th>Qty Sold</th><th>Sales</th></tr>
      {{COLLECTION ROWS — sorted by sales desc}}
    </table>
  </details>

  {{IF any collection shifted > 3 share points YoY:}}
  <div class="callout insight">
    <div class="callout-title">Significant Category Movement</div>
    <p>{{N}} collections shifted more than 3 share points year-over-year:</p>
  </div>
  <table>
    <tr><th>Collection</th><th>Prior Share</th><th>Current Share</th><th>Change</th><th>Top Item Driving Change</th><th>Top Customer Driving Change</th></tr>
    {{ROWS — only collections with > 3pt shift, sorted by absolute change desc}}
  </table>

  <div class="what-this-means">
    <strong>Action:</strong> {{DOMINANT_CATEGORY}}'s concentration means your revenue is heavily dependent on one product category — that's both a strength (clear market fit) and a risk (limited diversification). Collections with high sales-per-item signal strong rep confidence and customer pull. Categories with low sales per item may need merchandising support or rep training. {{IF SHIFTS EXIST: "The year-over-year shifts aren't random — they reflect changing customer preferences, successful product introductions, or competitive pressure."}}
  </div>
</div>
```

"Change" column (if shifts rendered): `.badge.ok` for positive shifts, `.badge.danger` for negative. Show as "+X.Xpp" or "-X.Xpp" (percentage points).

### 8. Catalog Completeness (Q-07)

**Gate**: Always (all accounts with a product catalog)

**Data source**: `cache/Q-07_results.md`

```html
<div class="subsection">
  <div class="subsection-title">Catalog Completeness</div>
  <table>
    <tr><th>Visibility</th><th>Products</th><th>Missing Images</th><th>Missing Price</th><th>Complete %</th></tr>
    {{ROWS — Visible / Hidden}}
  </table>

  {{IF completeness < 90%:}}
  <div class="callout alert">
    <div class="callout-title">Catalog Below 90% Complete</div>
    <p>{{COUNT}} visible products are missing images or pricing. Incomplete products are products reps can't confidently present — that's potential revenue left on the table from items your team can't effectively sell.</p>
  </div>

  <div class="what-this-means">
    <strong>Action:</strong> {{IF completeness >= 95%: "Your catalog is in strong shape — reps have the images and pricing they need to sell confidently. Maintaining this standard protects your digital selling effectiveness."}} {{IF completeness < 95%: "{{COUNT}} visible items are missing images or pricing, which means reps may skip them in presentations — that's potential revenue left on the table from products your team can't effectively sell. Completing these records is the lowest-effort improvement available."}}
  </div>
</div>
```

**Cross-reference to other sections**: For operational catalog completeness recommendations (upload images, refresh pricing, close configuration gaps), reference the Platform section if it exists: "See Platform Health Check for specific catalog remediation actions." Do NOT include operational "upload X images" or "refresh Y price levels" recommendations in this subsection — those belong in platform-level operational guidance.

---

## Section-Level What-This-Means (MANDATORY)

After all subsections, one `.what-this-means` for the entire section. Max 3 sentences:

1. The most urgent product-level action (restock, catalog update, new item push, fill rate remediation)
2. The revenue at risk if nothing changes
3. (Optional) What additional data would enable (e.g., item-level time-series for demand prediction)

---

## Data Confidence Header (MANDATORY — ALWAYS AT TOP)

**⚠ ENFORCEMENT: If this header is missing from the rendered section, the fragment is DEFECTIVE. Do NOT skip it under any circumstances.**

> Follow `section_shared_contract.md` §2 for the confidence header process.

**Template selection** for `SECTION_CONFIDENCE_3`:

| Tier value | Template | Label |
|---|---|---|
| `FULL` | `§3-FULL` | `FULL PICTURE` |
| `STRONG` | `§3-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§3-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§3-STRONG` (with `.limited` class) | `LIMITED VIEW` |

**Variable resolution**: `{{PRODUCT_COUNT}}` from `gate_flags.md` (omit parenthetical if unavailable). For STRONG: resolve `{{SOURCES_PRESENT}}`, `{{STALE_SOURCE}}`, `{{STALE_DATE}}` from Q-08 if available. If STRONG variables can't be resolved, fall back to `§3-PARTIAL`.

---

## Highlight File Output

> Follow `section_shared_contract.md` §4 for the highlight file format.

Save `cache/section_03_highlights.md` with 2–4 candidates from the strongest product signals. Deep-link: `[→ §product]`.

---

## Conditional Subsection Checklist

| # | Subsection | Gate | Mandatory? | Verify |
|---|-----------|------|------------|--------|
| 1 | Fill Rate & Revenue Impact (Q-59) | `HAS_PORTAL_ORDERS = true` + Q-59 has data rows | **YES** | rendered / correctly skipped |
| 2 | Ghost SKU Registry (Q-ORG-GHOST) | SIG-ANOMALY-01 fired + ghost SKU with > $5K LTM revenue | No | rendered / correctly skipped |
| 3 | Top Sellers & Inventory Position (Q-37) | `HAS_SALES_DATA` AND `HAS_INVENTORY` both true | No | rendered / correctly skipped |
| 4 | Stock-Out Impact Board (Q-ORG-STOCKOUT) | SIG-ANOMALY-02 fired + top-selling items at zero inventory | No | rendered / correctly skipped |
| 5 | Velocity Signals (Q-38a) | `HAS_PORTAL_ORDERS = true` + ≥ 3 real products with velocity data | No | rendered / correctly skipped |
| 6 | New Introduction Performance + Adoption Gap (Q-42/Q-61/Q-ORG-NEWITEM) | Part A: `HAS_SALES_DATA = true`. Part B: `HAS_PORTAL_ORDERS` AND `HAS_NEW_ITEMS` both true + Q-61 has data rows | **Part B: YES** when gate met | rendered / correctly skipped |
| 7 | What's Selling — Category & Collection (Q-39) | `HAS_SALES_DATA = true` | No | rendered / correctly skipped |
| 8 | Catalog Completeness (Q-07) | Always | **YES** | rendered |

## TARGET STRUCTURE — Gold Standard (MATCH THIS MARKUP EXACTLY)

This is the corresponding section from the canonical reference report. It is the source of truth for HTML structure: tag nesting, class names, column headers, subsection order, which subsections carry a `what-this-means` block, and the `<thead>`/`<tbody>`/`row-highlight` patterns. The data values below are illustrative — replace them with this client's data — but reproduce the STRUCTURE exactly. Where this target and the prose guide disagree on markup, THIS WINS.

```html
<details class="section-collapse" id="product">
  <summary>
    <div class="section-title">Product Intelligence</div>
    <div class="section-sub">1,247 active SKUs &middot; velocity signals, stock-out impact, new item adoption, companion analysis</div>
    <div class="section-contents">Products missing from catalog, stock-out board, velocity trends, new item gaps, category breakdown</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section">

    <div class="data-confidence">
      <span class="data-confidence-label">Full Picture</span>
      Product analysis combines eCat catalog data (1,247 SKUs), order history (eCat + all-channel invoices), real-time inventory feed, and app browse/search behavioral data.
    </div><div class="subsection">
      <div class="subsection-title">Products You&rsquo;re Selling But Reps Can&rsquo;t Find in eCat</div>
      <div class="sub-label">These items show up on invoices (customers are buying them) but they&rsquo;re not in the eCat catalog. That means reps can&rsquo;t present, quote, or order them through the app &mdash; customers are calling or faxing these in directly.</div>
      <table>
        <thead>
          <tr><th>Item Code</th><th>Product</th><th>Revenue (Last 12 Mo)</th><th>Orders</th><th>Why It&rsquo;s Missing</th></tr>
        </thead>
        <tbody>
          <tr class="row-warn"><td><strong>CL-918-BRS</strong></td><td>Classic Lantern 918, Brass</td><td>$142,000</td><td>38</td><td>Removed from catalog but still orderable by phone</td></tr>
          <tr class="row-warn"><td><strong>VT-4200-NK</strong></td><td>Vintage Track 4200, Nickel</td><td>$87,000</td><td>24</td><td>Custom finish never added to catalog</td></tr>
          <tr><td><strong>SP-1100-MT</strong></td><td>Spotlight 1100, Matte</td><td>$64,000</td><td>19</td><td>New SKU waiting on catalog upload</td></tr>
          <tr><td><strong>FL-HR-OAK</strong></td><td>Heritage Floor Lamp, Oak</td><td>$52,000</td><td>14</td><td>Seasonal item pulled too early</td></tr>
          <tr><td><strong>WL-320-AB</strong></td><td>Wall Light 320, Antique Brass</td><td>$41,000</td><td>11</td><td>Finish variant missing from master data</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> These 5 products sold $386K last year, but your reps can&rsquo;t see them in the app. If you add just the top two (Classic Lantern 918 and Vintage Track 4200) to the catalog with images and pricing, that&rsquo;s $229K in proven demand that all 32 reps can immediately present and sell &mdash; instead of only the handful who know to call it in.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Stock-Out Impact Board</div>
      <div class="sub-label">Active backorders with estimated revenue impact</div>
      <table>
        <thead>
          <tr><th>SKU</th><th>Product</th><th>Backorder Since</th><th>Est. Lost Orders (QTD)</th><th>Affected Accounts</th><th>Status</th></tr>
        </thead>
        <tbody>
          <tr class="row-danger"><td><strong>SC-AUR-BRS</strong></td><td>Aurora Sconce, Brass</td><td>Mar 12, 2026</td><td>$74,000</td><td>Heritage, Pinnacle, 4 others</td><td><span class="badge danger">Critical</span></td></tr>
          <tr class="row-warn"><td><strong>TL-PRM-NK</strong></td><td>Prism Table Lamp, Nickel</td><td>Apr 28, 2026</td><td>$62,000</td><td>Metro Contract, Urban Loft, 3 others</td><td><span class="badge warn">High</span></td></tr>
          <tr class="row-warn"><td><strong>FL-MRD-BRS</strong></td><td>Meridian Floor Lamp, Brass</td><td>May 8, 2026</td><td>$50,000</td><td>Coastal Design, Lakeside, 2 others</td><td><span class="badge warn">High</span></td></tr>
        </tbody>
      </table>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">Total Est. Lost Revenue QTD</div>
          <div class="metric-value">$186,000</div>
          <div class="metric-note danger">3 SKUs affecting 15 accounts</div>
        </div>
        <div class="metric">
          <div class="metric-label">Avg Days on Backorder</div>
          <div class="metric-value">58 days</div>
          <div class="metric-note danger">Aurora at 97 days</div>
        </div>
      </div>
      <div class="what-this-means">
        <strong>Action:</strong> The Aurora Sconce alone accounts for 40% of your stock-out impact and is the primary SKU for Heritage Hospitality Group and Pinnacle Hotel Group (combined $1.82M accounts). Expediting this single restock or offering the Nova Sconce at match pricing protects those relationships through Q3 project cycles.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Velocity Signals</div>

      <div class="sub-label">Accelerating (ordered more frequently this quarter vs. prior)</div>
      <table>
        <thead>
          <tr><th>SKU</th><th>Product</th><th>Orders This Qtr</th><th>QoQ Change</th><th>Revenue LTM</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td>CH-HAL-GLD</td><td>Halo Chandelier, Gold</td><td>34</td><td class="metric-note ok">+186%</td><td>$148,000</td></tr>
          <tr class="row-highlight"><td>PD-SOL-MBK</td><td>Solstice Pendant, Matte Black</td><td>52</td><td class="metric-note ok">+44%</td><td>$284,000</td></tr>
          <tr><td>FL-MRD-NK</td><td>Meridian Floor Lamp, Nickel</td><td>41</td><td class="metric-note ok">+38%</td><td>$312,000</td></tr>
          <tr><td>TL-DFT-NAT</td><td>Driftwood Table Lamp, Natural</td><td>28</td><td class="metric-note ok">+31%</td><td>$168,000</td></tr>
          <tr><td>WL-NOV-CHR</td><td>Nova Wall Sconce, Chrome</td><td>22</td><td class="metric-note ok">+27%</td><td>$94,000</td></tr>
        </tbody>
      </table>

      <div class="sub-label" style="margin-top:16px;">Decelerating (ordered less frequently, declining momentum)</div>
      <table>
        <thead>
          <tr><th>SKU</th><th>Product</th><th>Orders This Qtr</th><th>QoQ Change</th><th>Revenue LTM</th></tr>
        </thead>
        <tbody>
          <tr class="row-warn"><td>CH-TRD-AB</td><td>Traditional Chandelier, Ant. Brass</td><td>8</td><td class="metric-note danger">&minus;42%</td><td>$186,000</td></tr>
          <tr class="row-warn"><td>FL-CLS-BRZ</td><td>Classic Floor Lamp, Bronze</td><td>11</td><td class="metric-note danger">&minus;34%</td><td>$142,000</td></tr>
          <tr><td>TL-VIN-COP</td><td>Vintage Table Lamp, Copper</td><td>6</td><td class="metric-note warn">&minus;28%</td><td>$78,000</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> The Halo Chandelier&rsquo;s 186% QoQ acceleration confirms your Modern Collection bet is paying off. Meanwhile, the Traditional Chandelier is declining 42% QoQ &mdash; consider repositioning it as a &ldquo;Heritage Classic&rdquo; at a promotional price for your traditional-focused accounts like Hartwell &amp; Associates ($421K LTM, 64% traditional mix).
      </div>
    </div><div class="subsection">
      <div class="subsection-title">New Item Adoption Gaps</div>
      <div class="sub-label">Items launched since January 2026</div>
      <table>
        <thead>
          <tr><th>SKU</th><th>Product</th><th>Launch Date</th><th>Revenue to Date</th><th>Unique Buyers</th><th>Adoption Rate</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td>CH-HAL-GLD</td><td>Halo Chandelier, Gold</td><td>Jan 15</td><td>$148,000</td><td>28</td><td><span class="badge ok">Strong</span></td></tr>
          <tr class="row-highlight"><td>PD-ZEN-WHT</td><td>Zen Pendant, White</td><td>Feb 1</td><td>$94,000</td><td>22</td><td><span class="badge ok">Strong</span></td></tr>
          <tr><td>FL-HRZ-TK</td><td>Horizon Floor Lamp, Teak</td><td>Mar 1</td><td>$72,000</td><td>16</td><td><span class="badge info">Moderate</span></td></tr>
          <tr><td>WL-FSN-GY</td><td>Fusion Wall Light, Grey</td><td>Mar 15</td><td>$58,000</td><td>14</td><td><span class="badge info">Moderate</span></td></tr>
          <tr><td>TL-LNR-BK</td><td>Linear Table Lamp, Black</td><td>Apr 1</td><td>$28,000</td><td>8</td><td><span class="badge warn">Below Target</span></td></tr>
          <tr class="row-warn"><td>SC-PRF-SLV</td><td>Profile Sconce, Silver</td><td>Apr 15</td><td>$12,000</td><td>4</td><td><span class="badge danger">Needs Attention</span></td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> The Profile Sconce has only 4 buyers after 2 months &mdash; it&rsquo;s not in any rep presentations yet. Push it into Rachel Simmons&rsquo; and Patricia Nakamura&rsquo;s rotation (they drive 34% of new-item first orders). If it still underperforms after 60 days of active selling, reassess positioning.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Category &amp; Collection Performance</div>
      <table>
        <thead>
          <tr><th>Collection</th><th>SKUs</th><th>eCat Sales LTM</th><th>Share</th><th>YoY Change</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td><strong>Modern</strong></td><td>312</td><td>$3,440,000</td><td>40.0%</td><td class="metric-note ok">+28.4%</td></tr>
          <tr><td><strong>Transitional</strong></td><td>418</td><td>$2,752,000</td><td>32.0%</td><td class="metric-note ok">+12.1%</td></tr>
          <tr><td><strong>Traditional</strong></td><td>298</td><td>$1,548,000</td><td>18.0%</td><td class="metric-note warn">&minus;8.6%</td></tr>
          <tr><td><strong>Outdoor</strong></td><td>124</td><td>$602,000</td><td>7.0%</td><td class="metric-note ok">+34.8%</td></tr>
          <tr><td><strong>Custom/Special</strong></td><td>95</td><td>$258,000</td><td>3.0%</td><td class="metric-note ok">+6.2%</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Modern is now your largest collection by revenue (40% share, +28.4% YoY) while Traditional declines. Don&rsquo;t abandon Traditional &mdash; accounts like Hartwell &amp; Associates and 42 other buyers still depend on it &mdash; but shift new product development investment toward Modern and Outdoor (your fastest growers at +28.4% and +34.8% respectively).
      </div>
    </div>

    <div class="callout note" style="margin-top:16px;">
      <div class="callout-title">With Connected Data</div>
      Connecting your product development calendar would let us correlate launch timing with adoption velocity &mdash; showing whether High Point Market proximity drives faster uptake vs. mid-cycle launches.
    </div>

  </div>
</details>
```

## Section Shared Contract

# Section Shared Contract — Insightful Product 3.0

> Referenced by all section guides (§1–§6). Contains processes that are identical
> across sections. Each section guide provides section-specific parameters;
> this file provides the canonical process. **Do not duplicate these processes
> in individual guides.**

---

## 1. Pre-Build Gate Check Process

Before generating any HTML for a section:

1. Open `cache/gate_flags.md` and `cache/section_confidence.md`.
2. For each row in the section guide's **PRE-BUILD GATE CHECK** table:
   - Check the gate condition against `gate_flags.md`.
   - Check whether the cache file exists AND contains data rows.
   - Record: subsection name, MANDATORY or CONDITIONAL, gate MET or NOT MET.
3. **Write down your list** of subsections that will render before proceeding.
   Use this list as a checklist while building the fragment.
4. Skipping a MANDATORY subsection when its gate is met = **defective fragment**.

---

## 2. Data Confidence Header (MANDATORY for §2–§5)

Every section fragment (§2 through §5) MUST include a data confidence header.
If this header is missing, the fragment is **DEFECTIVE**.

**STEP 1 — Read the tier.** Open `cache/section_confidence.md` and read the
EXACT value of `SECTION_CONFIDENCE_N` (where N is this section's number). The
value is one of: `FULL`, `STRONG`, `PARTIAL`, `LIMITED`. **Use THIS value.
Do NOT infer or recompute the tier from gate flags — the data gathering script
already computed it.**

**STEP 2 — Select the template** from the section guide's confidence header
table (each guide defines its own template IDs, variable sources, and fallback
rules).

**STEP 3 — Position the header:** ALWAYS immediately after the header metrics,
BEFORE the first subsection content. This applies to ALL tiers including FULL.

**STEP 4 — Build the HTML:**

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

If the tier is `LIMITED`, use `<div class="data-confidence limited">` instead.

§6 (Platform Context) does NOT use a confidence header.

---

## 3. Fragment Wrapper

Sections §2–§5 use the `<details class="section-collapse">` wrapper per
`shared_rules.md` Section C. Each section guide specifies its Section ID and
Section Number.

**CORRECT HTML structure** (match exactly — rendering breaks if elements are
outside `<summary>` or wrong tag types are used):

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div class="section-title">{{SECTION_TITLE}}</div>
    <div class="section-sub">{{ONE-LINE STATS}}</div>
    <div class="section-contents">{{SUBSECTION_NAMES joined by · middots}}</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section">
    {{ALL SECTION CONTENT HERE}}
  </div>
</details>
```

Rules:
- `section-title` MUST be a `<div>`, not a `<span>`.
- `section-sub`, `section-contents`, and `expand-hint` MUST be INSIDE `<summary>`.
- If ANY of these elements are placed outside `<summary>`, the collapsed state
  renders incorrectly (text visible when section is collapsed).
- `section-contents` lists ONLY subsections that actually rendered (not skipped).

§1 (Signal Summary) renders as an open `<div class="section">` — it does NOT use `<details>`.
§6 (Platform Context) renders as a collapsed `<details>` (user must click to expand).

---

## 4. Highlight File Output

After building each section fragment, save `cache/section_NN_highlights.md`
per `shared_rules.md` Section K:

- 2–4 candidate highlights from the section's strongest signals.
- Each: bold headline + one sentence context + dollar figure + `surprise_score`
  + `signal_id` + section deep-link (e.g., `[→ §accounts]`).
- 0–1 priority action candidates with urgency level.
- At least 1 highlight MUST be positive.

Exception: §1 (Signal Summary) does NOT produce a highlights file — it consumes
highlights from all other sections. §6 produces 1–2 highlights only when issues
are severe (>180d staleness).

---

## 5. Conditional Subsection Checklist Process

Before saving a section fragment, verify against the section guide's
**Conditional Subsection Checklist** table:

1. For each row: confirm the subsection was rendered if its gate was met, or
   correctly skipped if its gate was not met.
2. Confirm the `section-contents` middot list in the HTML matches ONLY the
   subsections that actually rendered (not skipped ones).
3. Confirm every rendered subsection (except those noted otherwise in the guide)
   ends with a `<div class="what-this-means">` block that:
   - Starts with `<strong>Action:</strong>`
   - Contains max 3 sentences total
   - Names a specific entity and action (not generic advice)
4. Confirm the section-level `.what-this-means` is present (max 3 sentences,
   starts with `<strong>Action:</strong>`)
   — except §1 and §6 which have different rules per their guides.

---

## 6. Forbidden Terms Verification

Before saving any fragment, verify NONE of the following appear in the HTML:

| Forbidden | Replacement |
|-----------|-------------|
| ERP | "total business", "all-channel orders", "orders synced from your systems" |
| Mixpanel | "app usage data", "engagement events" |
| Clicky | Do not reference — suppress data source |
| health score | Use "Engagement Score" (§2 only) or describe the pattern |
| Segment labels (Platform-Embedded, etc.) | Describe the behavior instead |
| Internal IDs (org_id, customer_code, query IDs) | Remove entirely |
| Literal `[HYPOTHETICAL]` or `[ESTIMATED]` in HTML | Use prose hedging ("estimated", "projected") |
| portal orders / portal ordering | "total business", "all-channel orders" |
| platform (standalone) | "eCat", "the app", "your digital catalog" |
| platform-attributed revenue | "orders placed through eCat", "eCat volume" |
| platform engagement | "app usage", "digital catalog activity" |

Also verify:
- Every dollar figure has a time qualifier.
- Every finding names a specific entity — no generic "your accounts."
- Tables: top 5 visible, remainder in `<details>` (unless spec says otherwise).


# Shared Rules (excerpt for this section)

## A0. Editorial Voice — The North Star

**This is an intelligence report, not a risk report.**

The reader should finish this report thinking: *"I didn't know that about my
business — I need to pay for this."* NOT: *"Everything is broken, I should
churn."*

### Narrative Arc (MANDATORY)

Every section, and the report as a whole, follows this arc:

1. **MOMENTUM** — What's working. Celebrate wins, name the reps/accounts/products
   driving growth. This is NOT filler — it's the credibility foundation. If the
   reader doesn't trust that you understand their business, they won't act on risks.
2. **INTELLIGENCE** — What's interesting. Data-dense tables, penetration views,
   category breakdowns, behavioral patterns — the stuff they can't get from their
   own ERP. This is the "holy shit, I didn't know that" layer.
3. **OPPORTUNITY** — What could be better. Cross-sell whitespace, activation
   targets, coaching upside, conversion improvements. Frame as growth, not repair.
4. **RISK** — What to watch. Decay signals, displacement, contraction. These
   come LAST and are contextualized within the positive narrative. A $50K decay
  signal is alarming in isolation but manageable when prefaced by "$8.6M in eCat
  sales driven by 37 active reps."

### Tone Rules

- **Lead with strength.** The first subsection in every section should be the
  most impressive finding — the thing that makes the client proud of their business.
- **Risk findings are always contextualized.** Never "you're losing $X" in
  isolation. Always "you drove $Y through the platform; $X of that is at risk
  from [specific pattern]."
- **Frame negatives as opportunities.** "6 accounts show eCat share declining
  while total business grows — re-engaging them through the platform could
  recapture an estimated $Z" beats "COMPETITIVE DISPLACEMENT DETECTED — $X
  shifting away."
- **Ban doom headlines.** The words "ALERT", "DETECTED", "WARNING" in callout
  titles are reserved for genuine P0 operational issues (stock-outs affecting
  top customers, data staleness). Behavioral patterns, pricing shifts, and
  channel migration use `.callout.insight` not `.callout.alert`.
- **Celebrate specific wins by name.** "[Rep] converts at 26.8% — the highest
  on your team." "[Account] grew from $824 to $78.9K in 4 quarters on the
  platform." These are the findings that make clients say "I need this."

### Report-Level Balance Test (run before finalizing)

Count the findings across the Signal Summary:
- **Minimum 3 of 7 findings must be positive** (momentum, opportunity, or
  intelligence). If fewer than 3 are positive, demote the weakest risk finding
  and promote the next-best positive finding.
- **The FIRST finding must be positive.** The reader's first impression sets the
  tone for the entire report. Lead with the win.
- **Priority Actions balance:** At least 1 of 4 priority actions must be a GROWTH
  action (not a "fix this" or "re-engage that"). E.g., "Expand [product line]
  into [N] accounts that buy similar categories — estimated $X addressable."

---

## A1. Client-Facing Language — Write for Sales Leaders, Not SaaS PMs

The audience is a VP of Sales or owner at a lighting, furniture, or home decor
manufacturer. They think in reps, dealers, showrooms, orders, and products —
not platform metrics. Every term in the left column is **banned from client-facing
HTML**. Use the right column instead.

| Banned (SaaS / tech) | Use instead |
|---|---|
| "platform capture rate" / "capture rate" | "digital ordering share" or "share of orders placed through eCat" |
| "Capture Rate Economics" | "Digital Ordering Opportunity" |
| "platform GMV" | "eCat sales" or "orders placed through eCat" |
| "platform-attributed revenue" | "orders placed through eCat" or "eCat volume" |
| "collaborative filtering" | Describe the behavior: "customers who buy X also buy Y" |
| "cross-sell engine" | "products your customers buy together" or "companion products" |
| "Next Best Product" (as a title) | "Products Frequently Bought Together" or "Companion Product Opportunities" |
| "activation" (for accounts) | "onboarding" or "getting them ordering through the app" |
| "signal density" | Never in client-facing text — internal only |
| "behavioral data reveals" | "your team's usage patterns show" |
| "platform engagement" | "app usage" or "digital catalog activity" |
| "[assumes behavioral change]" | "[estimated]" — or drop if "estimated" already appears in the sentence |
| `[eCat ONLY]` / `[ALL-CHANNEL]` inline with dollar figures | Move these labels to **column headers** or **metric card labels** instead. In prose, say "eCat orders" or "total business across all channels" — never bracket-tags mid-sentence. |
| "platform" (standalone, as in "the platform") | "eCat" or "the app" or "your digital catalog" |
| "addressable" (as in "addressable revenue") | "potential" or "available" |

**Terms that are fine** — standard business vocabulary a sales leader uses daily:
conversion rate, year-over-year, trailing 12 months, reorder velocity, AOV,
LTM, quarter-over-quarter, fill rate, pipeline, territory, funnel.

**Inline data tags**: The `[eCat ONLY]` and `[ALL-CHANNEL]` bracket tags must
NOT appear inline with dollar figures in prose or table cells. Instead:
- In **metric cards**: put the scope in `.metric-note` (e.g., "eCat orders only")
- In **table headers**: append scope (e.g., "GMV (eCat)" or "GMV (all channels)")
- In **prose**: write it out ("$8.6M in eCat orders" or "$88M across all channels")
- These bracket tags ARE used in the **appendix labeling convention** and in
  **guide-internal documentation** to mark which data source applies — that is
  fine. The prohibition applies to client-facing rendered HTML only.

---

## H. What-This-Means Blocks

End every **section** (not subsection) with a `.what-this-means` div. Subsections also get their own `.what-this-means` per section guide specs.

- **Max 3 sentences.**
- **First sentence:** the strength to protect or the opportunity to capture
  (what's WORKING and how to build on it).
- **Second sentence:** the specific action that unlocks the next level of
  performance (growth-framed, not risk-framed).
- **Third sentence (optional):** what additional data would enable (data extension
  opportunity) OR the cost of inaction (but ONLY after the positive framing).
- **Never restate the statistics.** The reader already saw the table.
- **Never lead with doom.** "Your 37-rep team drove $8.6M through the platform —
  coaching the bottom quartile to median would add an estimated $1.2M" beats
  "10 reps convert below 10% — $1.2M at risk if nothing changes."

### H1. Self-Check (MANDATORY before saving any fragment)

After writing EVERY `.what-this-means` block, apply this 3-question test:

1. **Restatement test**: Could this sentence be produced by reading the first row of the table above it? If yes → REWRITE. The reader already read the table — your job is interpretation, not narration.
2. **Action test**: Does this block tell the reader what to DO or what it MEANS for their business? If it only tells them what the data SAYS → REWRITE.
3. **Specificity test**: Does this block reference at least one specific entity (rep name, account name, dollar figure, percentage) from THIS org's data? If it could apply to any org → REWRITE.

**FAILING EXAMPLES** (any of these patterns = automatic rewrite):
- "Your top performer generates $765K in iPad orders across 131 customers." ← This literally reads the table back.
- "This table shows your top 10 reps by GMV." ← Narrates the obvious.
- "Your top accounts are driving the majority of your revenue." ← Generic, applies to every org.
- "These accounts show declining order patterns." ← Restates without interpreting WHY or WHAT TO DO.

**PASSING EXAMPLES**:
- "The $485K gap between #1 and #10 suggests significant room to elevate mid-tier reps through coaching on customer targeting — if your bottom 5 matched your #5's AOV, that's an estimated $290K in annual incremental revenue."
- "Your most active rep presented to 49 accounts but only 3.6% converted to orders — high effort, lower yield. Meanwhile, your most efficient closer converts at 26.8% with far fewer presentations, suggesting targeted demos outperform high-volume prospecting for your product category."
- "The 63.8% decline at Lighting Connection ($926K→$335K) warrants immediate investigation: at that velocity, this was likely a deliberate channel shift rather than gradual drift. Three hypotheses: (1) they consolidated vendors, (2) they're sourcing this category direct-import, or (3) a competitor captured the relationship."

---

## K. Highlight File Contract

After building each section fragment, output `cache/section_NN_highlights.md`:

- **2–4 candidate highlights** per section.
- Each highlight: one-line headline + dollar figure + `surprise_score` +
  `signal_id`.
- Signal Summary builder reads **ALL** highlight files and selects top 5–7 by
  `SIGNAL_RANK`, subject to the diversity constraint (max 4 from any one section).
- `[HYPOTHETICAL]` tags appear in highlight files only — never in final HTML
  fragment.

---


## Cache Data

### signal_rank.md

# Signal Rank — EGLO Canada (eglo_can, org_id=232)
- **Run date**: can_2026-06-17
- **Total signals fired**: 26 (P0: 12, P1: 11, P2: 3)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 205989A (Trago 5 - 12" 5CCT LED Ceiling Light / P) $72,729 LTM, 0 available | P0 | §3 Product | 10.0 | $72,729 | 3.0 | 2,181,874 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 39267A (Climene - LED Pendant Light / LED Lumina) $25,446 LTM, 0 available | P0 | §3 Product | 10.0 | $25,446 | 3.0 | 763,388 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 205292A (Rafaelino - 1L Pendant Light / Luminaire) $22,094 LTM, 0 available | P0 | §3 Product | 10.0 | $22,094 | 3.0 | 662,809 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 390466A (Fruitera - 6L 3CCT LED Pendant Light / L) $21,901 LTM, 0 available | P0 | §3 Product | 10.0 | $21,901 | 3.0 | 657,026 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 205986A (Trago 5 - 9" 5CCT LED Ceiling Light / Pl) $18,183 LTM, 0 available | P0 | §3 Product | 10.0 | $18,183 | 3.0 | 545,492 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 205988A (Trago 5 - 7" 5CCT LED Ceiling Light / Pl) $13,266 LTM, 0 available | P0 | §3 Product | 10.0 | $13,266 | 3.0 | 397,989 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 206938A (Grazia - LED Linear Chandelier / Lustre ) $11,773 LTM, 0 available | P0 | §3 Product | 10.0 | $11,773 | 3.0 | 353,179 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 206937A (Grazia - LED Chandelier / Lustre DEL) $11,460 LTM, 0 available | P0 | §3 Product | 10.0 | $11,460 | 3.0 | 343,787 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 205131A (Troy 3 - 1L Pendant Light / Luminaire su) $10,553 LTM, 0 available | P0 | §3 Product | 10.0 | $10,553 | 3.0 | 316,577 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 85977A (Troy 3 - 1L Pendant Light / Luminaire su) $10,439 LTM, 0 available | P0 | §3 Product | 10.0 | $10,439 | 3.0 | 313,169 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 390342A (Dracera - 10L Linear LED Pendant / Lumin) $10,409 LTM, 0 available | P0 | §3 Product | 10.0 | $10,409 | 3.0 | 312,274 | RISK |
| 12 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 49% of eCat GMV | P1 | §4 Commerce | 1.2 | $126,661 | 2.0 | 308,350 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 200146A (Ascoli - 1L Exterior Wall Light / Murale) $10,250 LTM, 0 available | P0 | §3 Product | 10.0 | $10,250 | 3.0 | 307,515 | RISK |
| 14 | SIG-OPP-04 | New Item Adoption Gap — 7 new items with $0 platform orders | P2 | §3 Product | 0.7 | $50,000 | 1.0 | 35,000 | POSITIVE |
| 15 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 12 | 0 | 1 | 13 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 2 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 7 new items with $0 platform orders
2. **[RISK]** SIG-ANOMALY-02: Stock Out — 205989A (Trago 5 - 12" 5CCT LED Ceiling Light / P) $72,729 LTM, 0 available
3. **[RISK]** SIG-ANOMALY-02: Stock Out — 39267A (Climene - LED Pendant Light / LED Lumina) $25,446 LTM, 0 available
4. **[RISK]** SIG-ANOMALY-02: Stock Out — 205292A (Rafaelino - 1L Pendant Light / Luminaire) $22,094 LTM, 0 available
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 390466A (Fruitera - 6L 3CCT LED Pendant Light / L) $21,901 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 205986A (Trago 5 - 9" 5CCT LED Ceiling Light / Pl) $18,183 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 205988A (Trago 5 - 7" 5CCT LED Ceiling Light / Pl) $13,266 LTM, 0 available

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,563 | 1 | 0 | 99.90 |

### Q-37_results.md

# Q-37 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 205989A | CAT1 | COL804 | Trago 5 - 12" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 12" | $72,729 | 3,508 | 0 | 0 | 0 | — |
| 39267A | CAT12 | COL242 | Climene - LED Pendant Light / LED Luminaire suspendu | $25,446 | 200 | 0 | 0 | 0 | — |
| 205292A | CAT12 | COL751 | Rafaelino - 1L Pendant Light / Luminaire suspendu 1L | $22,094 | 313 | 0 | 0 | 0 | — |
| 390466A | CAT12 | COL300 | Fruitera - 6L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 6L | $21,901 | 40 | 0 | 0 | 0 | — |
| 205986A | CAT1 | COL804 | Trago 5 - 9" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 9" | $18,183 | 1,183 | 0 | 0 | 0 | — |
| 205988A | CAT1 | COL804 | Trago 5 - 7" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 7" | $13,266 | 970 | 0 | 0 | 0 | — |
| 206938A | CAT27 | COL31 | Grazia - LED Linear Chandelier / Lustre linéair DEL | $11,773 | 55 | 0 | 0 | 0 | — |
| 206937A | CAT27 | COL31 | Grazia - LED Chandelier / Lustre DEL | $11,460 | 48 | 0 | 0 | 0 | — |
| 205131A | CAT12 | COL809 | Troy 3 - 1L Pendant Light / Luminaire suspendu 1L | $10,553 | 299 | 0 | 0 | 0 | — |
| 85977A | CAT12 | COL809 | Troy 3 - 1L Pendant Light / Luminaire suspendu 1L | $10,439 | 502 | 0 | 0 | 0 | — |
| 390342A | CAT12 | COL37 | Dracera - 10L Linear LED Pendant / Luminaire suspendu DEL linéaire 10L | $10,409 | 21 | 0 | 0 | 0 | — |
| 200146A | CAT7 | COL192 | Ascoli - 1L Exterior Wall Light / Murale extérieure 1L | $10,250 | 251 | 0 | 0 | 0 | — |
| 200032A | CAT7 | RIGA | Riga - 1L Exterior Wall Light / Murale extérieure 1L | $9,220 | 362 | 0 | 0 | 0 | — |
| 390465A | CAT12 | COL300 | Fruitera - 3L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 3L | $7,631 | 29 | 0 | 0 | 0 | — |
| 94187A | CAT12 | COL790 | Tarbes - 1L Pendant Light / Luminaire suspendu 1L | $7,267 | 220 | 0 | 0 | 0 | — |
| 202343A | CAT13 | COL271 | Fondachelli - 1L Floor Lamp / Lampe de plancher 1L | $6,840 | 171 | 0 | 0 | 0 | — |
| 205293A | CAT12 | COL751 | Rafaelino - 1L Pendant Light / Luminaire suspendu 1L | $6,778 | 68 | 0 | 0 | 0 | — |
| 207407A | CAT15 | COMO | Como - 1L Convertible Pendant Light / Luminaire suspendu convertible 1L | $6,763 | 40 | 0 | 0 | 0 | — |
| 92719A | CAT12 | COL247 | Coretto - 1L Pendant Light / Luminaire suspendu 1L | $6,688 | 108 | 0 | 0 | 0 | — |
| 206423A | CAT12 | COL765 | Rondo - 1L Pendant Light / Luminaire suspendu 1L | $6,413 | 206 | 0 | 0 | 0 | — |

### Q-38a_results.md

(not present — file does not exist or is empty)

### Q-39_category_results.md

# Q-39-cat Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 18
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT12 | $857,995 | 10,072 | 333 | $2,577 |
| CAT1 | $293,096 | 12,209 | 105 | $2,791 |
| CAT27 | $226,070 | 858 | 88 | $2,569 |
| CAT7 | $136,882 | 3,012 | 80 | $1,711 |
| CAT6 | $127,681 | 1,656 | 155 | $824 |
| CAT26 | $72,603 | 17,521 | 23 | $3,157 |
| CAT10 | $70,239 | 1,995 | 30 | $2,341 |
| CAT3 | $63,156 | 1,301 | 48 | $1,316 |
| CAT13 | $57,901 | 875 | 49 | $1,182 |
| CAT15 | $55,130 | 325 | 31 | $1,778 |
| CAT11 | $43,122 | 975 | 83 | $520 |
| CAT9 | $16,050 | 223 | 10 | $1,605 |
| CAT21 | $4,858 | 165 | 3 | $1,619 |
| TRIM | $4,174 | 1,240 | 14 | $298 |
| CAT16 | $3,896 | 36 | 6 | $649 |
| CAT25 | $1,582 | 11 | 3 | $527 |
| CAT14 | $486 | 4 | 1 | $486 |
| CAT23 | $21 | 5 | 2 | $10 |

### Q-39_collection_results.md

# Q-39-col Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| COL804 | $147,463 | 10,065 | 21 | $7,022 |
| COL751 | $101,460 | 1,198 | 12 | $8,455 |
| COL848 | $72,603 | 17,521 | 23 | $3,157 |
| COL803 | $51,053 | 879 | 17 | $3,003 |
| COL184 | $45,482 | 525 | 2 | $22,741 |
| COL216 | $45,453 | 1,298 | 10 | $4,545 |
| COL300 | $44,040 | 214 | 6 | $7,340 |
| COL192 | $42,826 | 1,003 | 7 | $6,118 |
| COL773 | $36,587 | 763 | 10 | $3,659 |
| COL809 | $36,482 | 1,047 | 6 | $6,080 |
| COL242 | $35,347 | 259 | 3 | $11,782 |
| COL37 | $35,290 | 74 | 6 | $5,882 |
| COL116 | $32,289 | 162 | 14 | $2,306 |
| COL31 | $30,638 | 132 | 5 | $6,128 |
| RIGA | $29,284 | 1,087 | 4 | $7,321 |
| COL765 | $27,255 | 724 | 16 | $1,703 |
| COL286 | $27,036 | 142 | 4 | $6,759 |
| COL284 | $26,953 | 206 | 11 | $2,450 |
| DOYLE | $25,636 | 164 | 8 | $3,204 |
| COL182 | $24,939 | 351 | 18 | $1,386 |
| COL131 | $22,529 | 103 | 12 | $1,877 |
| COL230 | $22,019 | 223 | 16 | $1,376 |
| COL747 | $21,766 | 618 | 9 | $2,418 |
| AVIV | $21,080 | 1,147 | 3 | $7,027 |
| COL1 | $20,417 | 383 | 23 | $888 |

### Q-42_results.md

# Q-42 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 73
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| COL300 | 110 | $44,040 | 215 | $400 |
| COL116 | 90 | $32,289 | 162 | $359 |
| COL31 | 64 | $30,638 | 132 | $479 |
| COL286 | 64 | $27,036 | 142 | $422 |
| COL284 | 96 | $26,953 | 206 | $281 |
| DOYLE | 80 | $25,636 | 164 | $320 |
| COL182 | 152 | $24,939 | 352 | $164 |
| COL131 | 70 | $22,529 | 103 | $322 |
| COL1 | 108 | $20,417 | 383 | $189 |
| COL82 | 121 | $18,811 | 266 | $155 |
| COL290 | 61 | $18,651 | 92 | $306 |
| ABBEY | 26 | $17,133 | 42 | $659 |
| COL4 | 40 | $16,720 | 76 | $418 |
| AYERS | 25 | $15,477 | 33 | $619 |
| COL280 | 37 | $13,373 | 64 | $361 |
| COL153 | 27 | $12,559 | 79 | $465 |
| COL283 | 33 | $10,880 | 46 | $330 |
| JULEP | 55 | $10,659 | 80 | $194 |
| COL291 | 32 | $10,330 | 37 | $323 |
| COL101 | 23 | $10,047 | 77 | $437 |
| CALLE | 27 | $9,495 | 40 | $352 |
| COL48 | 58 | $9,392 | 176 | $162 |
| COMO | 14 | $9,296 | 57 | $664 |
| AGATE | 21 | $9,110 | 38 | $434 |
| COL87 | 59 | $8,847 | 106 | $150 |
| COL112 | 23 | $8,627 | 33 | $375 |
| COL41 | 36 | $6,983 | 68 | $194 |
| COL293 | 31 | $6,812 | 60 | $220 |
| COL11 | 12 | $6,665 | 16 | $555 |
| COL303 | 37 | $6,556 | 173 | $177 |
| AVRIL | 18 | $6,268 | 27 | $348 |
| COL144 | 15 | $5,672 | 24 | $378 |
| COL58 | 8 | $5,592 | 8 | $699 |
| ALFIE | 15 | $5,491 | 43 | $366 |
| COL118 | 17 | $5,436 | 36 | $320 |
| COL84 | 22 | $5,432 | 59 | $247 |
| JACKS | 18 | $5,356 | 34 | $298 |
| COL281 | 18 | $4,369 | 22 | $243 |
| COL179 | 11 | $4,175 | 12 | $380 |
| COL7 | 23 | $3,595 | 71 | $156 |
| COL285 | 11 | $3,447 | 13 | $313 |
| COL149 | 22 | $3,355 | 58 | $152 |
| COL70 | 21 | $2,749 | 42 | $131 |
| COL287 | 8 | $2,381 | 14 | $298 |
| COL289 | 9 | $2,227 | 15 | $247 |
| COL164 | 12 | $1,967 | 25 | $164 |
| COL305 | 15 | $1,915 | 90 | $128 |
| COL49 | 7 | $1,763 | 11 | $252 |
| COL119 | 7 | $1,724 | 10 | $246 |
| BRERA | 7 | $1,608 | 14 | $230 |
| COL74 | 6 | $1,552 | 18 | $259 |
| COL47 | 5 | $1,516 | 5 | $303 |
| COL172 | 6 | $1,348 | 16 | $225 |
| COL306 | 11 | $1,166 | 37 | $106 |
| COL26 | 6 | $1,149 | 6 | $192 |
| COL76 | 14 | $1,106 | 10 | $79 |
| COL114 | 12 | $956 | 10 | $80 |
| COL146 | 10 | $912 | 7 | $91 |
| SEBIO | 8 | $887 | 21 | $111 |
| COL302 | 15 | $854 | 26 | $57 |
| COL8 | 2 | $835 | 6 | $417 |
| COL86 | 8 | $834 | 6 | $104 |
| BLAKE | 9 | $592 | 6 | $66 |
| COL138 | 8 | $587 | 5 | $73 |
| COL73 | 3 | $418 | 5 | $139 |
| COL33 | 6 | $403 | 2 | $67 |
| COL154 | 3 | $286 | 3 | $95 |
| COL171 | 3 | $237 | 4 | $79 |
| COL5 | 3 | $0 | 0 | $0 |
| COL39 | 5 | $0 | 0 | $0 |
| COL52 | 3 | $0 | 0 | $0 |
| COL307 | 2 | $0 | 0 | $0 |
| COL304 | 17 | $0 | 0 | $0 |

### Q-59_results.md

(not present — file does not exist or is empty)

### Q-61_results.md

(not present — file does not exist or is empty)

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 205989A | Trago 5 - 12" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 12" | COL804 | 72,729.13 | 3,508 | — | — | [{'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 9858.0}, {'customer': 'Marchand Electric Co. Ltd.', 'revenue': 8051.76}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 6494.84}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 6494.58}, {'customer': 'Richardson Lighting - Regina', 'revenue': 6437.61}, {'customer': 'Éclairage M&M', 'revenue': 4692.0}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 4409.6}, {'customer': 'CDE - Laval', 'revenue': 4329.72}, {'customer': 'Electrimat Ltee', 'revenue': 3263.01}, {'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 3175.26}, {'customer': 'The Lighting Shoppe - London', 'revenue': 2862.0}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 2217.0}, {'customer': 'Chatelaine Lighting Supply Ltd', 'revenue': 1908.0}, {'customer': 'Royaume Luminaire - St-Basile', 'revenue': 1226.8}, {'customer': 'Living Lighting # 38 London', 'revenue': 1191.54}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 1154.64}, {'customer': 'City Electric Supply - Caledon', 'revenue': 1077.6}, {'customer': 'Lumen - Laval', 'revenue': 842.6}, {'customer': 'Lighting Reflects Design', 'revenue': 689.0}, {'customer': 'Total Lighting Sales', 'revenue': 569.7}, {'customer': 'Struktura Design & Architecture', 'revenue': 318.0}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 318.0}, {'customer': 'Preston Hardware', 'revenue': 318.0}, {'customer': 'Twin Bridge Lighting', 'revenue': 246.87}, {'customer': 'Guildwood Lighting & Fireside', 'revenue': 212.0}, {'customer': 'La Galerie du Tapis', 'revenue': 106.0}, {'customer': 'Guillevin International - Dartmouth', 'revenue': 79.5}, {'customer': 'Design Electrical', 'revenue': 53.0}, {'customer': 'Guillevin International - St-Leonard', 'revenue': 53.0}, {'customer': 'Park Lighting', 'revenue': 26.5}, {'customer': 'Lumisolution Inc.', 'revenue': 26.5}, {'customer': 'Deco Luminaire - Québec', 'revenue': 26.5}] | [{'item': '204072', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1737}, {'item': '203766', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 1284}, {'item': '203762', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 1247}, {'item': '203897', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1234}, {'item': '203899', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1115}, {'item': '203759', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 956}, {'item': '204074', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 690}, {'item': '203771', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 640}, {'item': '204945A', 'desc': 'Trago - 7" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 7" carré', 'available': 610}, {'item': '203764', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 552}, {'item': '204073', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 513}, {'item': '204947', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 512}, {'item': '204946', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 466}, {'item': '205987A', 'desc': 'Trago 5 - 5" 5CCT LED Ceiling Light / Plafonnier 5CCT DEL 5"', 'available': 385}, {'item': '203778', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 339}, {'item': '203763', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 331}, {'item': '203773', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 326}, {'item': '203775', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 276}, {'item': '203898', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 259}, {'item': '203768', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 255}, {'item': '203765', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 254}, {'item': '203678A', 'desc': 'Trago - 9" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 9" carré', 'available': 252}, {'item': '203776', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 183}, {'item': '203774', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 163}, {'item': '203901', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 161}, {'item': '203777', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 157}, {'item': '204075', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 106}, {'item': '203761', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 103}, {'item': '203679A', 'desc': 'Trago - 12" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 12" carré', 'available': 95}, {'item': '205495A', 'desc': 'Trago 2 - 16" 3 CCT LED Ceiling Light / Plafonnier DEL 3 CCT 16"', 'available': 6}] |
| 39267A | Climene - LED Pendant Light / LED Luminaire suspendu | COL242 | 25,446.25 | 200 | — | — | [{'customer': 'Multi Luminaire Gatineau', 'revenue': 23378.64}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 537.3}, {'customer': 'Deco Luminaire - Brossard', 'revenue': 405.96}, {'customer': 'Luminaires Repentigny', 'revenue': 270.64}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 159.2}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 153.23}, {'customer': 'Deco Luminaire - Québec', 'revenue': 135.32}, {'customer': 'Luminaire Expert R.T. Inc.', 'revenue': 135.32}, {'customer': 'Luminaires & Cie Inc', 'revenue': 135.32}, {'customer': 'Deco Luminaire - Terrebonne', 'revenue': 135.32}] | [{'item': '204376A', 'desc': 'Climene - LED Pendant Light / Luminaire suspendu DEL', 'available': 52}] |
| 205292A | Rafaelino - 1L Pendant Light / Luminaire suspendu 1L | COL751 | 22,093.63 | 313 | — | — | [{'customer': 'Eclairage Raymond inc', 'revenue': 10545.2}, {'customer': 'Multi Luminaire Granby', 'revenue': 3120.0}, {'customer': 'Eecol Electric Corp - Saskatoon', 'revenue': 1954.08}, {'customer': 'Richardson Lighting - Regina', 'revenue': 1752.0}, {'customer': 'Eurolite', 'revenue': 1530.0}, {'customer': 'Multi Luminaire Lévis', 'revenue': 884.0}, {'customer': 'Multi Luminaire Laval', 'revenue': 544.0}, {'customer': 'Guillevin International - Terrebonne', 'revenue': 412.0}, {'customer': 'Cartwright Lighting', 'revenue': 315.0}, {'customer': 'Franklin Empire - Mont-Royal', 'revenue': 315.0}, {'customer': 'Dhillon Lighting - Calgary', 'revenue': 290.0}, {'customer': 'Park Lighting', 'revenue': 239.4}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 192.95}] | [{'item': '206244A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 192}, {'item': '206243A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 162}, {'item': '205291A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 147}, {'item': '204324A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 107}, {'item': '205295A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 59}, {'item': '204325A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 28}, {'item': '206242A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 12}] |
| 390466A | Fruitera - 6L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 6L | COL300 | 21,900.86 | 40 | — | — | [{'customer': 'Alberta Lighting & Décor', 'revenue': 5100.63}, {'customer': 'Park Lighting', 'revenue': 3175.2}, {'customer': 'Multi Luminaire Laval', 'revenue': 3084.48}, {'customer': 'Union Lighting & Furnishings', 'revenue': 2113.02}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 1722.19}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 1458.7}, {'customer': 'Deco Luminaire - Terrebonne', 'revenue': 1209.6}, {'customer': 'Cartwright Lighting', 'revenue': 1058.4}, {'customer': 'Paradise Lighting - Burlington', 'revenue': 982.8}, {'customer': 'Edmonton Lighting & Decor Inc.', 'revenue': 680.4}, {'customer': 'Multi Luminaire Granby', 'revenue': 514.08}, {'customer': 'Luminaire Galarneau', 'revenue': 423.36}, {'customer': 'Paradise Lighting/ MaxTraders Inc', 'revenue': 378.0}] | [{'item': '390463A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 15}, {'item': '390467A', 'desc': 'Fruitera - 1L 3CCT LED Table Lamp / Lampe de table DEL 3CCT 1L', 'available': 13}, {'item': '390464A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 12}] |
| 205986A | Trago 5 - 9" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 9" | COL804 | 18,183.08 | 1,183 | — | — | [{'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 3280.0}, {'customer': 'Royaume Luminaire - Ste Julie', 'revenue': 3189.63}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 2551.71}, {'customer': 'Richardson Lighting - Regina', 'revenue': 2476.23}, {'customer': 'Éclairage M&M', 'revenue': 1968.0}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 1275.86}, {'customer': 'CDE - Laval', 'revenue': 671.52}, {'customer': 'Corlite Distributors Inc.', 'revenue': 590.4}, {'customer': 'City Electric Supply - Caledon', 'revenue': 469.84}, {'customer': 'Living Lighting # 38 London', 'revenue': 405.71}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 391.72}, {'customer': 'Marchand Electric Co. Ltd.', 'revenue': 265.81}, {'customer': 'The Lighting Shoppe - London', 'revenue': 221.4}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 167.88}, {'customer': 'Living Lighting #8 Napean', 'revenue': 107.62}, {'customer': 'Electrimat Ltee', 'revenue': 60.27}, {'customer': 'La Galerie du Tapis', 'revenue': 41.0}, {'customer': 'Total Lighting Sales', 'revenue': 27.98}, {'customer': 'Lumen - Laval', 'revenue': 20.5}] | [{'item': '204072', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1737}, {'item': '203766', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 1284}, {'item': '203762', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 1247}, {'item': '203897', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1234}, {'item': '203899', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1115}, {'item': '203759', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 956}, {'item': '204074', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 690}, {'item': '203771', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 640}, {'item': '204945A', 'desc': 'Trago - 7" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 7" carré', 'available': 610}, {'item': '203764', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 552}, {'item': '204073', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 513}, {'item': '204947', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 512}, {'item': '204946', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 466}, {'item': '205987A', 'desc': 'Trago 5 - 5" 5CCT LED Ceiling Light / Plafonnier 5CCT DEL 5"', 'available': 385}, {'item': '203778', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 339}, {'item': '203763', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 331}, {'item': '203773', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 326}, {'item': '203775', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 276}, {'item': '203898', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 259}, {'item': '203768', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 255}, {'item': '203765', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 254}, {'item': '203678A', 'desc': 'Trago - 9" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 9" carré', 'available': 252}, {'item': '203776', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 183}, {'item': '203774', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 163}, {'item': '203901', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 161}, {'item': '203777', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 157}, {'item': '204075', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 106}, {'item': '203761', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 103}, {'item': '203679A', 'desc': 'Trago - 12" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 12" carré', 'available': 95}, {'item': '205495A', 'desc': 'Trago 2 - 16" 3 CCT LED Ceiling Light / Plafonnier DEL 3 CCT 16"', 'available': 6}] |
| 205988A | Trago 5 - 7" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 7" | COL804 | 13,266.30 | 970 | — | — | [{'customer': 'JC Eclairage inc.', 'revenue': 5376.0}, {'customer': 'The Lighting Shoppe - London', 'revenue': 1555.2}, {'customer': 'Electrimat Ltee', 'revenue': 1508.24}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 959.2}, {'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 820.11}, {'customer': 'CDE - Laval', 'revenue': 575.52}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 480.0}, {'customer': 'Chatelaine Lighting Supply Ltd', 'revenue': 384.0}, {'customer': 'Richardson Lighting - Regina', 'revenue': 287.76}, {'customer': 'Living Lighting # 38 London', 'revenue': 215.82}, {'customer': 'Lighting Reflects Design', 'revenue': 192.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 191.84}, {'customer': 'DND Electrical & AV Inc', 'revenue': 172.8}, {'customer': 'City Electric Supply - Caledon', 'revenue': 143.88}, {'customer': 'Deco Luminaire - Terrebonne', 'revenue': 115.2}, {'customer': 'Design Electrical', 'revenue': 96.0}, {'customer': 'Total Lighting Sales', 'revenue': 83.93}, {'customer': 'Cimpexco Entreprise Import Export Inc', 'revenue': 76.8}, {'customer': 'Luminaires Repentigny', 'revenue': 16.0}, {'customer': 'Struktura Design & Architecture', 'revenue': 16.0}] | [{'item': '204072', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1737}, {'item': '203766', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 1284}, {'item': '203762', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 1247}, {'item': '203897', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1234}, {'item': '203899', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1115}, {'item': '203759', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 956}, {'item': '204074', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 690}, {'item': '203771', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 640}, {'item': '204945A', 'desc': 'Trago - 7" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 7" carré', 'available': 610}, {'item': '203764', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 552}, {'item': '204073', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 513}, {'item': '204947', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 512}, {'item': '204946', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 466}, {'item': '205987A', 'desc': 'Trago 5 - 5" 5CCT LED Ceiling Light / Plafonnier 5CCT DEL 5"', 'available': 385}, {'item': '203778', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 339}, {'item': '203763', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 331}, {'item': '203773', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 326}, {'item': '203775', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 276}, {'item': '203898', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 259}, {'item': '203768', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 255}, {'item': '203765', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 254}, {'item': '203678A', 'desc': 'Trago - 9" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 9" carré', 'available': 252}, {'item': '203776', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 183}, {'item': '203774', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 163}, {'item': '203901', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 161}, {'item': '203777', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 157}, {'item': '204075', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 106}, {'item': '203761', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 103}, {'item': '203679A', 'desc': 'Trago - 12" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 12" carré', 'available': 95}, {'item': '205495A', 'desc': 'Trago 2 - 16" 3 CCT LED Ceiling Light / Plafonnier DEL 3 CCT 16"', 'available': 6}] |
| 206938A | Grazia - LED Linear Chandelier / Lustre linéair DEL | COL31 | 11,772.62 | 55 | — | — | [{'customer': 'Multi Luminaire Laval', 'revenue': 1522.85}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 1305.3}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 1200.12}, {'customer': 'Multi Luminaire Granby', 'revenue': 870.2}, {'customer': 'Dhillon Lighting - Edmonton', 'revenue': 637.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 624.6}, {'customer': 'Super Lite Lighting', 'revenue': 573.0}, {'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 558.86}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 558.86}, {'customer': 'Royaume Luminaire - Drummond', 'revenue': 558.86}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 558.86}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 555.2}, {'customer': 'Luminaire Alder inc', 'revenue': 488.96}, {'customer': 'Multi Luminaire Lévis', 'revenue': 435.1}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 435.1}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 291.2}, {'customer': 'C.E Tang Yuk & Co. Ltd', 'revenue': 225.55}, {'customer': 'Paradise Lighting/ MaxTraders Inc', 'revenue': 191.0}, {'customer': 'Cornwall Lighting & Electrical', 'revenue': 182.0}] | [{'item': '206939A', 'desc': 'Grazia - LED Convertible Pendant Light / Luminaire suspendu convertible DEL', 'available': 15}, {'item': '207774A', 'desc': 'Grazia - LED Chandelier / Lustre DEL', 'available': 15}, {'item': '207775A', 'desc': 'Grazia - LED Linear Chandelier / Lustre linéair DEL', 'available': 8}] |
| 206937A | Grazia - LED Chandelier / Lustre DEL | COL31 | 11,459.56 | 48 | — | — | [{'customer': 'Multi Luminaire Laval', 'revenue': 1753.77}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 1404.37}, {'customer': 'Multi Luminaire Granby', 'revenue': 936.26}, {'customer': 'Dhillon Lighting - Edmonton', 'revenue': 888.7}, {'customer': 'Luminaire Galarneau', 'revenue': 657.6}, {'customer': 'Super Lite Lighting', 'revenue': 616.5}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 601.3}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 598.4}, {'customer': 'Carrington Lighting - North Store', 'revenue': 534.3}, {'customer': 'Litemode Limited', 'revenue': 504.9}, {'customer': 'C.E Tang Yuk & Co. Ltd', 'revenue': 486.2}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 468.14}, {'customer': 'Multi Luminaire Lévis', 'revenue': 468.13}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 448.8}, {'customer': 'Dhillon Lighting - Calgary', 'revenue': 369.9}, {'customer': 'The Lighting Shoppe - London', 'revenue': 277.43}, {'customer': 'Sparkle Light', 'revenue': 239.36}, {'customer': 'Paradise Lighting - Burlington', 'revenue': 205.5}] | [{'item': '206939A', 'desc': 'Grazia - LED Convertible Pendant Light / Luminaire suspendu convertible DEL', 'available': 15}, {'item': '207774A', 'desc': 'Grazia - LED Chandelier / Lustre DEL', 'available': 15}, {'item': '207775A', 'desc': 'Grazia - LED Linear Chandelier / Lustre linéair DEL', 'available': 8}] |
| 205131A | Troy 3 - 1L Pendant Light / Luminaire suspendu 1L | COL809 | 10,552.56 | 299 | — | — | [{'customer': 'Richardson Lighting - Regina', 'revenue': 3214.4}, {'customer': 'Eecol Electric Corp - Saskatoon', 'revenue': 2570.4}, {'customer': 'Eurolite', 'revenue': 1927.8}, {'customer': 'Multi Luminaire Lévis', 'revenue': 999.6}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 806.4}, {'customer': '0797222 BC LTD DBA Elumea Lighting Co', 'revenue': 378.0}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 302.4}, {'customer': 'Electrical & Plumbing - Gloucester', 'revenue': 142.8}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 129.36}, {'customer': 'The Lighting Shoppe - London', 'revenue': 47.8}, {'customer': 'Luminaire Galarneau', 'revenue': 33.6}] | [{'item': '85979A', 'desc': 'Troy 3 - 1L Wall Light / Murale 1L', 'available': 82}, {'item': '85978A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 37}, {'item': '205132A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 24}, {'item': '85981A', 'desc': 'Troy 3 - 1L Table Lamp / Lampe de table 1L', 'available': 3}] |
| 85977A | Troy 3 - 1L Pendant Light / Luminaire suspendu 1L | COL809 | 10,438.96 | 502 | — | — | [{'customer': 'Multi Luminaire Gatineau', 'revenue': 6487.74}, {'customer': 'Luminaires & Cie Inc', 'revenue': 614.4}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 604.8}, {'customer': 'Lumen - Laval', 'revenue': 542.72}, {'customer': 'Luminaires Repentigny', 'revenue': 512.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 358.4}, {'customer': 'Multi Luminaire Lévis', 'revenue': 353.6}, {'customer': 'Unique Lighting', 'revenue': 345.6}, {'customer': 'Multi Luminaire Laval', 'revenue': 244.8}, {'customer': 'Multi Luminaire Granby', 'revenue': 81.6}, {'customer': 'Super Lite Lighting', 'revenue': 81.6}, {'customer': 'Sparkle Light', 'revenue': 51.2}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 51.2}, {'customer': 'Corlite Distributors Inc.', 'revenue': 33.6}, {'customer': 'Eclairage Raymond inc', 'revenue': 25.6}, {'customer': 'City Lightz - St Catharines', 'revenue': 25.6}, {'customer': 'The Lighting Gallery', 'revenue': 24.5}] | [{'item': '85979A', 'desc': 'Troy 3 - 1L Wall Light / Murale 1L', 'available': 82}, {'item': '85978A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 37}, {'item': '205132A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 24}, {'item': '85981A', 'desc': 'Troy 3 - 1L Table Lamp / Lampe de table 1L', 'available': 3}] |
| 390342A | Dracera - 10L Linear LED Pendant / Luminaire suspendu DEL linéaire 10L | COL37 | 10,409.12 | 21 | — | — | [{'customer': 'Multi Luminaire Laval', 'revenue': 3905.92}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 2453.4}, {'customer': 'Eclairage Union Montreal - DROP SHIP', 'revenue': 661.2}, {'customer': 'Alberta Lighting & Décor', 'revenue': 646.2}, {'customer': 'Union Lighting & Furnishings', 'revenue': 610.3}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 574.4}, {'customer': 'Luminaires & Cie Inc', 'revenue': 574.4}, {'customer': 'Deco Luminaire - Brossard', 'revenue': 574.4}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 408.9}] | [{'item': '390411A', 'desc': 'Dracera - 7L LED Ceiling Light / Plafonnier 7L DEL', 'available': 18}, {'item': '205804A', 'desc': 'Dracera - 10L LED Ceiling Light / Plafonnier DEL 10L', 'available': 6}, {'item': '390343A', 'desc': 'Dracera - 17L LED Pendant Light / Luminaire suspendu DEL 17L', 'available': 5}, {'item': '390339A', 'desc': 'Dracera - 10L Round LED Pendant / Luminaire suspendu DEL rond 10L', 'available': 2}] |
| 200146A | Ascoli - 1L Exterior Wall Light / Murale extérieure 1L | COL192 | 10,250.50 | 251 | — | — | [{'customer': 'Eclairage Raymond inc', 'revenue': 7800.0}, {'customer': 'Corlite Distributors Inc.', 'revenue': 1320.0}, {'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 660.0}, {'customer': 'Avaled Corp', 'revenue': 343.0}, {'customer': 'Multi Luminaire Granby', 'revenue': 127.5}] | [{'item': '200022A', 'desc': 'Ascoli - 1L Exterior Wall Light / Murale extérieure 1L', 'available': 101}, {'item': '200147A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 96}, {'item': '200023A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 80}, {'item': '200029A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 24}, {'item': '90119A', 'desc': 'Ascoli - 1L Exterior Wall Light / Murale extérieure 1L', 'available': 16}, {'item': '90121A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 13}] |
| 200032A | Riga - 1L Exterior Wall Light / Murale extérieure 1L | RIGA | 9,219.60 | 362 | — | — | [{'customer': 'Éclairage M&M', 'revenue': 4524.0}, {'customer': 'Espace Lumi Decor Inc', 'revenue': 2262.0}, {'customer': 'Deco Luminaire - Québec', 'revenue': 962.0}, {'customer': 'CDE - Laval', 'revenue': 847.6}, {'customer': 'Georgian Design Centre', 'revenue': 260.0}, {'customer': 'Eclairage Raymond inc', 'revenue': 182.0}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 78.0}, {'customer': 'Eclairage Moderne Saran', 'revenue': 52.0}, {'customer': 'Luminaires & Cie Inc', 'revenue': 52.0}] | [{'item': '200033A', 'desc': 'Riga - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 490}, {'item': '84002A', 'desc': 'Riga - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 4}] |
| 390465A | Fruitera - 3L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 3L | COL300 | 7,631.44 | 29 | — | — | [{'customer': 'Paradise Lighting - Burlington', 'revenue': 1096.2}, {'customer': 'Park Lighting', 'revenue': 1058.4}, {'customer': 'Vancouver Lighting - Richmond', 'revenue': 982.8}, {'customer': 'The Lighting Warehouse', 'revenue': 850.5}, {'customer': 'Cartwright Lighting', 'revenue': 529.2}, {'customer': 'Royal Lighting', 'revenue': 491.4}, {'customer': 'Multi Luminaire Granby', 'revenue': 472.31}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 472.31}, {'customer': 'Lumisolution Inc.', 'revenue': 396.9}, {'customer': 'Carrington Lighting - North Store', 'revenue': 321.3}, {'customer': 'Luminaires & Cie Inc', 'revenue': 302.4}, {'customer': 'Multi Luminaire Laval', 'revenue': 257.04}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 211.68}, {'customer': 'Paradise Lighting/ MaxTraders Inc', 'revenue': 189.0}] | [{'item': '390463A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 15}, {'item': '390467A', 'desc': 'Fruitera - 1L 3CCT LED Table Lamp / Lampe de table DEL 3CCT 1L', 'available': 13}, {'item': '390464A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 12}] |
| 94187A | Tarbes - 1L Pendant Light / Luminaire suspendu 1L | COL790 | 7,267.33 | 220 | — | — | [{'customer': 'CDE - Laval', 'revenue': 3999.0}, {'customer': 'Multi Luminaire Lévis', 'revenue': 1193.4}, {'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 614.25}, {'customer': 'Deco Luminaire - Québec', 'revenue': 252.0}, {'customer': 'Luminaires & Cie Inc', 'revenue': 216.0}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 209.23}, {'customer': 'Lumen - Laval', 'revenue': 189.0}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 162.0}, {'customer': 'Lite It Up By Design Inc. - INACTIVE', 'revenue': 137.7}, {'customer': 'Unique Lighting', 'revenue': 121.5}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 108.0}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 34.65}, {'customer': 'Multi Luminaire Granby', 'revenue': 30.6}] | [{'item': '94188A', 'desc': 'Tarbes - 1L Pendant Light / Luminaire suspendu 1L', 'available': 74}, {'item': '94189A', 'desc': 'Tarbes - 3L Pendant Light / Luminaire suspendu 3L', 'available': 53}, {'item': '43004A', 'desc': 'Tarbes - 1L Ceiling Light / Plafonnier 1L', 'available': 21}, {'item': '94191A', 'desc': 'Tarbes - 3L Pendant Light / Luminaire suspendu 3L', 'available': 15}] |
| 202343A | Fondachelli - 1L Floor Lamp / Lampe de plancher 1L | COL271 | 6,840 | 171 | — | — | [{'customer': 'Winners Merchants International LP', 'revenue': 6840.0}] | — |
| 205293A | Rafaelino - 1L Pendant Light / Luminaire suspendu 1L | COL751 | 6,777.66 | 68 | — | — | [{'customer': 'Alberta Lighting & Décor', 'revenue': 2534.4}, {'customer': 'Sparkle Light', 'revenue': 950.4}, {'customer': 'Multi Luminaire Granby', 'revenue': 538.56}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 526.21}, {'customer': 'Wesco Distribution - Toronto', 'revenue': 462.0}, {'customer': 'Park Lighting', 'revenue': 369.6}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 254.69}, {'customer': 'Luminaire Galarneau', 'revenue': 253.44}, {'customer': 'Living Lighting #8 Napean', 'revenue': 224.4}, {'customer': 'Luminaires & Cie Inc', 'revenue': 211.2}, {'customer': 'Multi Luminaire Lévis', 'revenue': 179.52}, {'customer': 'Dhillon Lighting - Calgary', 'revenue': 171.6}, {'customer': 'Royaume Luminaire - Drummond', 'revenue': 101.64}] | [{'item': '206244A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 192}, {'item': '206243A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 162}, {'item': '205291A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 147}, {'item': '204324A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 107}, {'item': '205295A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 59}, {'item': '204325A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 28}, {'item': '206242A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 12}] |
| 207407A | Como - 1L Convertible Pendant Light / Luminaire suspendu convertible 1L | COMO | 6,762.66 | 40 | — | — | [{'customer': 'Mclaren Lighting - Victoria', 'revenue': 4443.75}, {'customer': 'Super Lite Lighting', 'revenue': 1007.25}, {'customer': 'Union Lighting & Furnishings', 'revenue': 400.53}, {'customer': 'Living Lighting #8 Napean', 'revenue': 319.81}, {'customer': 'CDE - Laval', 'revenue': 189.6}, {'customer': 'Park Lighting', 'revenue': 150.5}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 132.72}, {'customer': 'Dhillon Lighting - Edmonton', 'revenue': 118.5}] | — |
| 92719A | Coretto - 1L Pendant Light / Luminaire suspendu 1L | COL247 | 6,687.59 | 109 | — | — | [{'customer': 'Agence For-Trem', 'revenue': None}, {'customer': 'Carrington Lighting - North Store', 'revenue': 4446.0}, {'customer': 'Multi Luminaire Granby', 'revenue': 2008.84}, {'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 99.75}, {'customer': 'Deco Luminaire - Québec', 'revenue': 76.0}, {'customer': 'Park Lighting', 'revenue': 57.0}] | [{'item': '92716A', 'desc': 'Coretto - 1L Pendant Light / Luminaire suspendu 1L', 'available': 16}] |
| 206423A | Rondo - 1L Pendant Light / Luminaire suspendu 1L | COL765 | 6,412.84 | 206 | — | — | [{'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 2732.73}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 564.57}, {'customer': 'SaveMore Plumbing & Heating', 'revenue': 555.77}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 533.05}, {'customer': 'Multi Luminaire Laval', 'revenue': 430.95}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 312.28}, {'customer': 'Luminaire Galarneau', 'revenue': 249.6}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 240.24}, {'customer': 'Vancouver Lighting - Richmond', 'revenue': 187.2}, {'customer': 'Eclairage Quebec Corporation', 'revenue': 156.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 124.8}, {'customer': 'Luminaire Alder inc', 'revenue': 124.8}, {'customer': 'Multi Luminaire Granby', 'revenue': 99.45}, {'customer': 'The Lighting Shoppe - London', 'revenue': 70.2}, {'customer': 'Deco Luminaire - Québec', 'revenue': 31.2}] | [{'item': '206424A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 73}, {'item': '206421A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 61}, {'item': '206425A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 42}, {'item': '206432A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 34}, {'item': '206422A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 24}, {'item': '206428A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 18}, {'item': '206431A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 17}, {'item': '206429A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 13}, {'item': '85264A', 'desc': 'Rondo - 1L Table Lamp / Lampe de table 1L', 'available': 12}, {'item': '204565A', 'desc': 'Rondo - 1L Table Lamp / Lampe de table 1L', 'available': 9}, {'item': '85265A', 'desc': 'Rondo - 1L Table Lamp / Lampe de table 1L', 'available': 8}] |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 207423A | Agate - 4L Pendant Light / Luminaire suspendu 4L | AGATE | 2 | 1,041.60 | — |
| 207424A | Agate - 3L Pendant Light / Luminaire suspendu 3L | AGATE | 2 | 621.60 | — |
| 207428A | Agate - 3L Pendant Light / Luminaire suspendu 3L | AGATE | 1 | 175.69 | — |
| 207429A | Agate - 4L Pendant Light / Luminaire suspendu 4L | AGATE | 1 | 1,441.80 | — |
| 207309A | Avril - 8L Chandelier / Lustre 8L | AVRIL | 2 | 1,586.40 | — |
| 207277A | Ayers - 1L 5CCT LED Linear Chandelier / Lustre linéair DEL 5CCT 1L | AYERS | 0 | 0 | — |
| 207278A | Ayers - 1L 5CCT LED Linear Chandelier / Lustre linéair DEL 5CCT 1L | AYERS | 2 | 350.48 | — |
| 207683A | Blake - 1L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 1L | BLAKE | 0 | 0 | — |
| 207684A | Blake - 2L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 2L | BLAKE | 1 | 71.68 | — |
| 207685A | Blake - 3L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 3L | BLAKE | 1 | 140 | — |
| 207686A | Blake - 4L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 4L | BLAKE | 0 | 0 | — |
| 207687A | Blake - 1L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 1L | BLAKE | 0 | 0 | — |
| 207688A | Blake - 2L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 2L | BLAKE | 2 | 268.80 | — |
| 207689A | Blake - 3L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 3L | BLAKE | 1 | 111.30 | — |
| 207691A | Blake - 4L 5CCT LED Vanity Light / Murale de salle de bain DEL 5CCT 4L | BLAKE | 0 | 0 | — |
| 207025A | Bedminster - 1L Vanity Light / Murale de salle de bain 1L | COL1 | 2 | 627.12 | — |
| 207027A | Bedminster - 1L Vanity Light / Murale de salle de bain 1L | COL1 | 2 | 592.08 | — |
| 207043A | Bedminster - 4L Vanity Light / Murale de salle de bain 4L | COL1 | 2 | 241.65 | — |
| 207044A | Bedminster - 4L Vanity Light / Murale de salle de bain 4L | COL1 | 0 | 0 | — |
| 207045A | Bedminster - 4L Vanity Light / Murale de salle de bain 4L | COL1 | 1 | 114.10 | — |
| 207046A | Bedminster - 4L Vanity Light / Murale de salle de bain 4L | COL1 | 1 | 195.60 | — |
| 207047A | Bedminster - 4L Vanity Light / Murale de salle de bain 4L | COL1 | 1 | 134.25 | — |
| 207048A | Bedminster - 4L Vanity Light / Murale de salle de bain 4L | COL1 | 1 | 221.68 | — |
| 207611A | Argyle - 5CCT LED Flush Mount / Plafonnier DEL 5CCT | COL101 | 2 | 406 | — |
| 207614A | Argyle - 5CCT LED Flush Mount / Plafonnier DEL 5CCT | COL101 | 1 | 92.80 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
