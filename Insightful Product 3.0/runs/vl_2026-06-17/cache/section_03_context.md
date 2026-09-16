# Section 3 Context Bundle — Ciana Varaluz LLC (vl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=2019, portal_order_gmv=$1.4M |
| HAS_INVENTORY | True | inventory_count=775 |
| HAS_SALES_DATA | True | sales_data_count=10634 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=3 engagement_reps=38 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | varaluz_vl_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$1.4M > ecat_gmv=$1.3M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 3 | 3 |
| ENGAGEMENT_REP_COUNT | 38 | engagement_reps=38 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 95 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 116, Mixpanel total submit_order (Q-01): 160 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=84.2%, ambiguous_rate=0.0%, showroom_event_share=100.0% |
| USER_GROUP_JOIN_RATE | 84% | 80 of 95 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 100% | showroom+admin share of matched events: 100.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 27 admin/showroom users in leaderboard: Angela Smith, CS3 Varaluz, CS4 Varaluz, CS5 Varaluz, CS6 Varaluz |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=36 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=640 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=283 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=480 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Ciana Varaluz LLC
- **Shortname**: vl
- **Org ID**: 147
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | True |
| HAS_PORTAL_ORDERS | True |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | FULL | See Derived Gate 6 §2 formula |
| §3 Customer | FULL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | FULL | See Derived Gate 6 §5 formula |

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

# Signal Rank — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17
- **Total signals fired**: 24 (P0: 11, P1: 12, P2: 1)
- **Org GMV**: $1.3M eCat LTM, $1.4M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 64% of eCat GMV | P1 | §4 Commerce | 1.6 | $419,032 | 2.0 | 1,331,132 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 297P25HG (Social Club 25 Light 5-Tier - Havana Gol) $30,355 LTM, 0 available | P0 | §3 Product | 10.0 | $30,355 | 3.0 | 910,660 | RISK |
| 3 | SIG-DECAY-03 | Rep Trajectory — John Howard orders -80.0% QoQ, $33,580 current 90d GMV | P1 | §5 Team | 3.2 | $134,320 | 2.0 | 859,648 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 4DMI0108 (Kye 22x40 Rounded Rectangular Wall Mirro) $23,748 LTM, 0 available | P0 | §3 Product | 10.0 | $23,748 | 3.0 | 712,432 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 376W02BN (Morgan 2 Light Sconce - Brushed Nickel) $21,664 LTM, 0 available | P0 | §3 Product | 10.0 | $21,664 | 3.0 | 649,908 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 309P03HG (Matrix 3 Light Pendant - Havana Gold) $19,915 LTM, 0 available | P0 | §3 Product | 10.0 | $19,915 | 3.0 | 597,451 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 380P05MBFG (Estela 5 Light Pendant - Matte Black/Fre) $15,067 LTM, 0 available | P0 | §3 Product | 10.0 | $15,067 | 3.0 | 452,009 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 348N06HG (Kato 6 Light Oval Pendant - Havana Gold) $13,334 LTM, 0 available | P0 | §3 Product | 10.0 | $13,334 | 3.0 | 400,025 | RISK |
| 9 | SIG-OPP-01 | Next Best Product — 557P08HG/561N06FG co-purchase pattern across 14 customers | P0 | §2/§3 | 1.4 | $135,185 | 2.0 | 378,517 | POSITIVE |
| 10 | SIG-ANOMALY-02 | Stock Out — 297P19HG (Social Club 19 Light 4-Tier - Havana Gol) $12,092 LTM, 0 available | P0 | §3 Product | 10.0 | $12,092 | 3.0 | 362,751 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 389P06MBHN (Blonde Moment 6 Light   Pendant - Matte ) $11,456 LTM, 0 available | P0 | §3 Product | 10.0 | $11,456 | 3.0 | 343,685 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 345C21CBHG (Windsor 21 Light 4-Tier Crystal Chandeli) $10,797 LTM, 0 available | P0 | §3 Product | 10.0 | $10,797 | 3.0 | 323,911 | RISK |
| 13 | SIG-OPP-04 | New Item Adoption Gap — 21 new items with $0 platform orders | P2 | §3 Product | 2.1 | $50,000 | 1.0 | 105,000 | POSITIVE |
| 14 | SIG-COMMERCE-01 | Capture Rate — eCat captures 92.9% of $1M total business; each +1pt = $14K | P0 | §4 Commerce | 0.4 | $14,000 | 3.0 | 15,000 | POSITIVE |
| 15 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — riser_prices last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — placement_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — options last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 1 | 0 | 0 | 1 | |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 0 | 10 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 557P08HG/561N06FG co-purchase pattern across 14 customers
2. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 21 new items with $0 platform orders
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 92.9% of $1M total business; each +1pt = $14K
4. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 64% of eCat GMV
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 297P25HG (Social Club 25 Light 5-Tier - Havana Gol) $30,355 LTM, 0 available
6. **[RISK]** SIG-DECAY-03: Rep Trajectory — John Howard orders -80.0% QoQ, $33,580 current 90d GMV
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 4DMI0108 (Kye 22x40 Rounded Rectangular Wall Mirro) $23,748 LTM, 0 available

**Balance check**: 3 positive (slots 1-3), 4 risk (slots 4-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 814 | 2 | 356 | 56.30 |

### Q-37_results.md

# Q-37 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 297P25HG | CAT3 | COL15 | Social Club 25 Light 5-Tier - Havana Gold | $30,355 | 12 | 0 | 0 | 0 | 2026-7-17 |
| 4DMI0108 | CAT11 | KYE | Kye 22x40 Rounded Rectangular Wall Mirror - Gold | $23,748 | 104 | 0 | 0 | 0 | 2026-6-24 |
| 376W02BN | CAT1 | COL6 | Morgan 2 Light Sconce - Brushed Nickel | $21,664 | 197 | 0 | 0 | 0 | 2026-10-16 |
| 309P03HG | CAT3 | COL1 | Matrix 3 Light Pendant - Havana Gold | $19,915 | 40 | 0 | 0 | 0 | 2026-6-26 |
| 380P05MBFG | CAT3 | COL62 | Estela 5 Light Pendant - Matte Black/French Gold | $15,067 | 19 | 0 | 0 | 0 | 2026-6-29 |
| 348N06HG | CAT3 | KATO | Kato 6 Light Oval Pendant - Havana Gold | $13,334 | 18 | 0 | 0 | 0 | 2026-7-31 |
| 297P19HG | CAT3 | COL15 | Social Club 19 Light 4-Tier - Havana Gold | $12,092 | 7 | 0 | 0 | 0 | 2026-6-26 |
| 389P06MBHN | CAT3 | COL67 | Blonde Moment 6 Light   Pendant - Matte Black/Honey/Medium Oak | $11,456 | 18 | 0 | 0 | 0 | 2026-7-30 |
| 345C21CBHG | CAT2 | COL7 | Windsor 21 Light 4-Tier Crystal Chandelier - Carbon/Havana Gold | $10,797 | 2 | 0 | 0 | 0 | 2026-7-17 |
| 434MI22CH | CAT11 | COL69 | Capsule 22x40 Mirror - Chrome | $9,975 | 45 | 0 | 0 | 0 | 2026-9-15 |
| 370B03HG | CAT5 | COL9 | Cosmos 3 Light Bath - Havana Gold | $8,029 | 24 | 0 | 0 | 0 | 2026-7-31 |
| 431MI24GO | CAT11 | COL68 | Carlton 24x50 Mirror - Gold | $7,686 | 23 | 0 | 0 | 0 | 2026-6-15 |
| 393C14MBFG | CAT2 | COL39 | Park Row 14 Light 2-Tier Chandelier - Matte Black/French Gold | $6,984 | 5 | 0 | 0 | 0 | 2026-7-31 |
| 247N04HO | CAT8 | FLOW | Flow 4 Light Oval Linear Pendant w/Fabric Shade - Hammered Ore | $6,578 | 10 | 0 | 0 | 0 | 2026-6-22 |
| 381N06MBAR | CAT8 | COL54 | Scribble 6 Light Linear Pendant - Matte Black/Artifact | $5,915 | 7 | 0 | 0 | 0 | 2026-7-31 |
| 434MI22GO | CAT11 | COL69 | Capsule 22x40 Mirror - Gold | $5,906 | 25 | 0 | 0 | 0 | 2026-9-15 |
| 500S03HGOB | CAT7 | COL55 | Ethereal Rose 3 Light Inverted Semi-Flush - Havana Gold Ombre | $5,893 | 17 | 0 | 0 | 0 | 2026-7-31 |
| 500C06HGOB | CAT2 | COL55 | Ethereal Rose 6 Light Chandelier - Havana Gold Ombre | $5,505 | 18 | 0 | 0 | 0 | 2025-12-6 |
| 240K01HO | CAT1 | FLOW | Flow 1 Light Left Sconce - Hammered Ore | $5,189 | 22 | 0 | 0 | 0 | 2026-10-9 |
| 311P16CB | CAT3 | COL18 | Orbital Large 16 Light Pendant - Carbon | $4,742 | 6 | 0 | 0 | 0 | 2026-7-31 |

### Q-38a_results.md

# Q-38a Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1358
- **Run date**: 2026-06-17


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
| 1070P01CH | Chroman Empire 1 Light 10 in Bell Pendant | CAT3 | COL21 | 2026-2-1 | 1 | 1 |
| 1070P01CH | Chroman Empire 1 Light 10 in Bell Pendant | CAT3 | COL21 | 2026-4-1 | 3 | 1 |
| 1070P01CH | Chroman Empire 1 Light 10 in Bell Pendant | CAT3 | COL21 | 2026-6-1 | 1 | 1 |
| 1070P01LCH | Chroman Empire 1 Light 16 in Dome Pendant | CAT3 | COL21 | 2026-4-1 | 2 | 1 |
| 1070P01LSG | Chroman Empire 1 Light 16 in Dome Pendant | CAT3 | COL21 | 2026-6-1 | 1 | 1 |
| 1070P01MCH | Chroman Empire 1 Light 10 in Dome Pendant | CAT3 | COL21 | 2026-2-1 | 1 | 1 |
| 1070P01MSG | Chroman Empire 1 Light 10 in Dome Pendant | CAT3 | COL21 | 2026-2-1 | 2 | 2 |
| 1070P03CH | Chroman Empire 3 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-2-1 | 2 | 1 |
| 1070P03SG | Chroman Empire 3 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-1-1 | 1 | 1 |
| 1070P03SG | Chroman Empire 3 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-2-1 | 4 | 2 |
| 1070P04CH | Chroman Empire 4 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-4-1 | 1 | 1 |
| 1070P04SG | Chroman Empire 4 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-1-1 | 1 | 1 |
| 1070P04SG | Chroman Empire 4 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-2-1 | 6 | 3 |
| 1070P04SG | Chroman Empire 4 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-5-1 | 1 | 1 |
| 1070P04SG | Chroman Empire 4 Light Tall Cylinder Pendant | CAT3 | COL21 | 2026-6-1 | 3 | 2 |
| 169M01AQ | Urchin 1 Light Mini Pendant - Aqua Velvet | CAT3 | COL19 | 2026-1-1 | 1 | 1 |
| 169M01AQ | Urchin 1 Light Mini Pendant - Aqua Velvet | CAT3 | COL19 | 2026-3-1 | 1 | 1 |
| 169M01AQ | Urchin 1 Light Mini Pendant - Aqua Velvet | CAT3 | COL19 | 2026-6-1 | 1 | 1 |
| 169M01BL | Urchin 1 Light Mini Pendant - Black | CAT6 | COL19 | 2026-1-1 | 4 | 1 |
| 169M01CH | Urchin 1 Light Mini Pendant - Painted Chrome | CAT6 | COL19 | 2026-2-1 | 1 | 1 |
| 169M01GO | Urchin 1 Light Mini Pendant - Gold | CAT6 | COL19 | 2026-5-1 | 2 | 1 |
| 169M01OR | Urchin 1 Light Mini Pendant - Electric Pumpkin | CAT6 | COL19 | 2026-3-1 | 8 | 3 |
| 169M01OR | Urchin 1 Light Mini Pendant - Electric Pumpkin | CAT6 | COL19 | 2026-6-1 | 3 | 2 |
| 169M01SAQ | Urchin 1 Light Uber Mini Pendant - Aqua Velvet | CAT6 | COL19 | 2026-2-1 | 3 | 1 |
| 169M01SAQ | Urchin 1 Light Uber Mini Pendant - Aqua Velvet | CAT6 | COL19 | 2026-3-1 | 1 | 1 |
| 169M01SAQ | Urchin 1 Light Uber Mini Pendant - Aqua Velvet | CAT6 | COL19 | 2026-5-1 | 1 | 1 |
| 169M01SBL | Urchin 1 Light Uber Mini Pendant - Black | CAT6 | COL19 | 2026-1-1 | 1 | 1 |
| 169M01SBL | Urchin 1 Light Uber Mini Pendant - Black | CAT6 | COL19 | 2026-3-1 | 1 | 1 |
| 169M01SGO | Urchin 1 Light Uber Mini Pendant - Gold | CAT6 | COL19 | 2026-1-1 | 1 | 1 |
| 169M01SOR | Urchin 1 Light Uber Mini Pendant - Electric Pumpkin | CAT6 | COL19 | 2026-2-1 | 2 | 1 |
| 169M01SOR | Urchin 1 Light Uber Mini Pendant - Electric Pumpkin | CAT6 | COL19 | 2026-3-1 | 7 | 1 |
| 169M01SOR | Urchin 1 Light Uber Mini Pendant - Electric Pumpkin | CAT6 | COL19 | 2026-5-1 | 1 | 1 |
| 169M01SWH | Urchin 1 Light Uber Mini Pendant - White | CAT6 | COL19 | 2026-1-1 | 6 | 2 |
| 169M01SYE | Urchin 1 Light Uber Mini Pendant - Un-Mellow Yellow | CAT6 | COL19 | 2026-3-1 | 1 | 1 |
| 169M01SYE | Urchin 1 Light Uber Mini Pendant - Un-Mellow Yellow | CAT6 | COL19 | 2026-5-1 | 1 | 1 |
| 169M01WH | Urchin 1 Light Mini Pendant - White | CAT6 | COL19 | 2026-1-1 | 2 | 2 |
| 169M01WH | Urchin 1 Light Mini Pendant - White | CAT6 | COL19 | 2026-3-1 | 2 | 2 |
| 169M01YE | Urchin 1 Light Mini Pendant - Un-Mellow Yellow | CAT6 | COL19 | 2025-12-1 | 2 | 1 |
| 169M01YE | Urchin 1 Light Mini Pendant - Un-Mellow Yellow | CAT6 | COL19 | 2026-2-1 | 2 | 1 |
| 169M01YE | Urchin 1 Light Mini Pendant - Un-Mellow Yellow | CAT6 | COL19 | 2026-3-1 | 1 | 1 |
| 169P01AQ | Urchin 1 Light Pendant - Aqua Velvet | CAT3 | COL19 | 2026-1-1 | 1 | 1 |
| 169P01AQ | Urchin 1 Light Pendant - Aqua Velvet | CAT3 | COL19 | 2026-3-1 | 1 | 1 |
| 169P01AQ | Urchin 1 Light Pendant - Aqua Velvet | CAT3 | COL19 | 2026-6-1 | 4 | 1 |
| 169P01BL | Urchin 1 Light Pendant - Black | CAT3 | COL19 | 2026-1-1 | 1 | 1 |
| 169P01CH | Urchin 1 Light Pendant - Painted Chrome | CAT3 | COL19 | 2026-1-1 | 1 | 1 |
| 169P01CH | Urchin 1 Light Pendant - Painted Chrome | CAT3 | COL19 | 2026-2-1 | 1 | 1 |
| 169P01GO | Urchin 1 Light Pendant - Gold | CAT3 | COL19 | 2026-2-1 | 2 | 1 |
| 169P01GO | Urchin 1 Light Pendant - Gold | CAT3 | COL19 | 2026-4-1 | 1 | 1 |
| 169P01OR | Urchin 1 Light Pendant - Electric Pumpkin | CAT3 | COL19 | 2026-3-1 | 5 | 1 |
| 169P01WH | Urchin 1 Light Pendant - White | CAT3 | COL19 | 2026-1-1 | 3 | 1 |

*(Truncated: showing top 50 of 1358 rows. Full data in cache file.)*

### Q-39_category_results.md

# Q-39-cat Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 14
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT3 | $1.1M | 1,911 | 190 | $5,906 |
| CAT2 | $829,246 | 538 | 70 | $11,846 |
| CAT11 | $336,188 | 1,433 | 69 | $4,872 |
| CAT8 | $326,249 | 304 | 28 | $11,652 |
| CAT1 | $276,356 | 1,562 | 100 | $2,764 |
| CAT5 | $124,020 | 589 | 42 | $2,953 |
| CAT7 | $85,379 | 179 | 25 | $3,415 |
| FOYER | $70,109 | 96 | 16 | $4,382 |
| CAT9 | $31,251 | 220 | 5 | $6,250 |
| CAT6 | $24,031 | 116 | 13 | $1,848 |
| CAT4 | $16,526 | 13 | 5 | $3,305 |
| CAT12 | $10,092 | 16 | 3 | $3,364 |
| CAT10 | $9,048 | 63 | 8 | $1,131 |
| CAT14 | $6,194 | 23 | 2 | $3,097 |

### Q-39_collection_results.md

# Q-39-col Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| COL1 | $731,799 | 625 | 36 | $20,328 |
| FLOW | $286,728 | 519 | 37 | $7,749 |
| COL7 | $151,465 | 172 | 23 | $6,585 |
| COL9 | $143,063 | 213 | 14 | $10,219 |
| KYE | $137,536 | 636 | 11 | $12,503 |
| BASK | $123,390 | 139 | 16 | $7,712 |
| KATO | $103,210 | 141 | 18 | $5,734 |
| COL2 | $91,617 | 254 | 16 | $5,726 |
| COL39 | $83,917 | 123 | 12 | $6,993 |
| COL95 | $77,125 | 125 | 18 | $4,285 |
| COL66 | $62,648 | 185 | 9 | $6,961 |
| COL6 | $61,353 | 458 | 15 | $4,090 |
| COL48 | $59,927 | 35 | 6 | $9,988 |
| COL18 | $57,507 | 90 | 17 | $3,383 |
| COL76 | $54,475 | 258 | 8 | $6,809 |
| COL8 | $54,056 | 127 | 18 | $3,003 |
| COL15 | $52,937 | 52 | 10 | $5,294 |
| COL13 | $51,538 | 42 | 5 | $10,308 |
| COL3 | $43,895 | 52 | 2 | $21,948 |
| COL14 | $41,377 | 72 | 7 | $5,911 |
| COL62 | $41,355 | 65 | 9 | $4,595 |
| COCO | $39,571 | 84 | 9 | $4,397 |
| COL19 | $38,102 | 162 | 22 | $1,732 |
| COL55 | $38,077 | 96 | 9 | $4,231 |
| COL97 | $33,525 | 281 | 7 | $4,789 |

### Q-42_results.md

# Q-42 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 64
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| COL3 | 55 | $43,357 | 56 | $788 |
| COL30 | 57 | $29,074 | 53 | $510 |
| COL25 | 29 | $25,153 | 39 | $867 |
| COL39 | 21 | $22,472 | 31 | $1,070 |
| COL21 | 128 | $21,801 | 151 | $170 |
| COL28 | 28 | $18,865 | 18 | $674 |
| COL1 | 9 | $15,782 | 12 | $1,754 |
| COL37 | 33 | $12,900 | 36 | $391 |
| COL46 | 27 | $8,579 | 32 | $318 |
| COL75 | 22 | $8,544 | 24 | $388 |
| COL77 | 46 | $8,399 | 50 | $183 |
| COL2 | 25 | $6,369 | 15 | $255 |
| COL24 | 13 | $6,088 | 16 | $468 |
| COL15 | 10 | $5,753 | 16 | $575 |
| COL26 | 13 | $5,135 | 14 | $395 |
| COL36 | 11 | $4,860 | 13 | $442 |
| COL38 | 18 | $4,428 | 7 | $246 |
| COL48 | 7 | $4,125 | 7 | $589 |
| COL35 | 10 | $4,096 | 10 | $410 |
| HOPE | 27 | $3,819 | 40 | $141 |
| COL22 | 13 | $2,577 | 8 | $198 |
| COL29 | 7 | $2,154 | 8 | $308 |
| COL27 | 4 | $840 | 2 | $210 |
| COL17 | 24 | $710 | 2 | $30 |
| COL19 | 10 | $548 | 3 | $55 |
| KYE | 4 | $456 | 2 | $114 |
| COL51 | 10 | $179 | 2 | $18 |
| COL72 | 8 | $140 | 1 | $17 |
| COL86 | 11 | $0 | 0 | $0 |
| COL87 | 26 | $0 | 0 | $0 |
| COL88 | 5 | $0 | 0 | $0 |
| COL89 | 3 | $0 | 0 | $0 |
| COL90 | 6 | $0 | 0 | $0 |
| COL91 | 3 | $0 | 0 | $0 |
| COL92 | 6 | $0 | 0 | $0 |
| COL93 | 1 | $0 | 0 | $0 |
| LILA | 1 | $0 | 0 | $0 |
| COL12 | 34 | $0 | 0 | $0 |
| COL16 | 1 | $0 | 0 | $0 |
| COL20 | 4 | $0 | 0 | $0 |
| COL23 | 21 | $0 | 0 | $0 |
| COL31 | 11 | $0 | 0 | $0 |
| COL32 | 3 | $0 | 0 | $0 |
| COL33 | 5 | $0 | 0 | $0 |
| COL34 | 43 | $0 | 0 | $0 |
| COL4 | 4 | $0 | 0 | $0 |
| COL40 | 14 | $0 | 0 | $0 |
| COL41 | 3 | $0 | 0 | $0 |
| COL42 | 6 | $0 | 0 | $0 |
| COL43 | 3 | $0 | 0 | $0 |
| COL44 | 2 | $0 | 0 | $0 |
| COL45 | 1 | $0 | 0 | $0 |
| COL5 | 38 | $0 | 0 | $0 |
| COL73 | 4 | $0 | 0 | $0 |
| COL74 | 22 | $0 | 0 | $0 |
| COL76 | 5 | $0 | 0 | $0 |
| COL78 | 2 | $0 | 0 | $0 |
| COL79 | 2 | $0 | 0 | $0 |
| COL80 | 3 | $0 | 0 | $0 |
| COL81 | 4 | $0 | 0 | $0 |
| COL82 | 3 | $0 | 0 | $0 |
| COL83 | 22 | $0 | 0 | $0 |
| COL84 | 3 | $0 | 0 | $0 |
| COL85 | 2 | $0 | 0 | $0 |

### Q-59_results.md

# Q-59 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ITEM | 590S12SG | Downpour 12 Light Dimmable Pendant | CAT3 | — | — | 432 | 26 | 1,382.70 | 597,326.40 | 39,483.45 | 26 |
| ITEM | 348MI33HG | Kato 33-in Round Mirror - Havana Gold | CAT11 | — | — | 1,980 | 41 | 248.86 | 492,746.76 | 12,447.54 | 41 |
| ITEM | 585P08PG | Golden Thicket 9 Light Dimmable Pendant | CAT3 | — | — | 400 | 22 | 830.27 | 332,108.80 | 22,259.35 | 22 |
| ITEM | 567P13MDBFG | Botanic Panic 13 Light Medium Pendant | CAT3 | — | — | 506 | 21 | 591.43 | 299,265.65 | 13,956.10 | 21 |
| ITEM | 567P13DBFG | Botanic Panic 13 Light Pendant | CAT3 | — | — | 168 | 12 | 694.75 | 116,718 | 9,726.50 | 12 |
| ITEM | 348MI33CB | Kato 33-in Round Mirror - Carbon | CAT11 | — | — | 325 | 25 | 257.34 | 83,636.28 | 7,111.82 | 26 |
| ITEM | 576C08BG | Rockford 8 Light Chandelier | CAT2 | — | — | 154 | 9 | 287.80 | 44,321.20 | 4,173.10 | 9 |
| ITEM | 562W02HG | Mojave 2 Light Sconce | CAT1 | — | — | 234 | 12 | 152.39 | 35,659.26 | 3,110.12 | 12 |
| ITEM | 570P06DBFG | Aristocrat 6 Light Pendant | CAT3 | — | — | 72 | 7 | 355.89 | 25,624.35 | 3,539.70 | 7 |
| ITEM | 393C14MBFG | Park Row 14 Light 2-Tier Chandelier - Matte Black/French Gold | CAT2 | — | — | 15 | 5 | 1,577.01 | 23,655.18 | 10,441.87 | 5 |
| ITEM | 434MI22GO | Capsule 22x40 Mirror - Gold | CAT11 | — | — | 117 | 11 | 197.26 | 23,079.33 | 10,077.96 | 13 |
| ITEM | 570W02DBFG | Aristocrat 2 Light Sconce | CAT1 | — | — | 280 | 13 | 82.06 | 22,976 | 1,759.10 | 13 |
| ITEM | 536M01ZNCBRZ | Brasserie 1 Light Mini Pendant - Blackened Zinc/Heritage Bronze | CAT3 | — | — | 168 | 9 | 134.75 | 22,638 | 2,116.62 | 11 |
| ITEM | 567W01DBFG | Botanic Panic 1 Light Wall or Ceiling Flush Mount | CAT14 | — | — | 171 | 6 | 131.72 | 22,524.88 | 2,502.77 | 6 |
| ITEM | 557W04HG | Aurora 4 Light Sconce | CAT1 | — | — | 126 | 11 | 161.30 | 20,323.35 | 4,206.05 | 11 |
| ITEM | 540P01ABLKBRZ | Mood Swings 1 Light Round Pendant - Heritage Black/Heritage Bronze | CAT3 | — | — | 40 | 5 | 479.75 | 19,190 | 4,301.75 | 7 |

### Q-61_results.md

# Q-61 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 590S12SG | Downpour 12 Light Dimmable Pendant | CAT3 | 26 | 28 | 39,483.45 | 26 | — |
| 561N06FG | High Tide 6 Light linear Pendant | CAT3 | 28 | 36 | 30,595.95 | 31 | — |
| 585P08PG | Golden Thicket 9 Light Dimmable Pendant | CAT3 | 22 | 26 | 22,259.35 | 24 | — |
| 561C08FG | High Tide 8 Light Pendant | CAT3 | 19 | 24 | 18,007.80 | 21 | — |
| 562P12HG | Mojave 12 Light Pendant | CAT3 | 8 | 12 | 15,326.35 | 9 | — |
| 557P08HG | Aurora 8 Light Pendant | CAT3 | 20 | 23 | 14,338.55 | 20 | — |
| 567P13MDBFG | Botanic Panic 13 Light Medium Pendant | CAT3 | 21 | 23 | 13,956.10 | 21 | — |
| 558C09FG | Petal Court 9 Light Chandelier | CAT2 | 12 | 17 | 13,385.60 | 15 | — |
| 557P14HG | Aurora 14 Light 2 Tier Pendant | CAT3 | 7 | 8 | 11,886.35 | 7 | — |
| 587C24SG | Ain't She Grand 24 Light Chandelier | CAT3 | 1 | 3 | 11,418.30 | 1 | — |
| 393C14MBFG | Park Row 14 Light 2-Tier Chandelier - Matte Black/French Gold | CAT2 | 5 | 7 | 10,441.87 | 5 | — |
| 567P13DBFG | Botanic Panic 13 Light Pendant | CAT3 | 12 | 14 | 9,726.50 | 12 | — |
| 393C18MBFG | Park Row 18 Light 3-Tier Chandelier - Matte Black/French Gold | CAT2 | 4 | 6 | 9,168.25 | 4 | — |
| 309N10HG | Matrix 10 Light Linear - Havana Gold | CAT4 | 6 | 6 | 8,511.05 | 6 | — |
| 558C12FG | Petal Court 9+3 Light Chandelier | CAT2 | 7 | 7 | 7,078 | 7 | — |
| 562P09HG | Mojave 9 Light Pendant | CAT3 | 8 | 8 | 6,118 | 8 | — |
| 557S04HG | Aurora 4 Light Convertible Semi Flush | CAT14 | 14 | 15 | 5,852.02 | 15 | — |
| 531P03SB | Mingle 3 Light Pendant - Satin Brass | CAT3 | 3 | 8 | 5,450.20 | 4 | — |
| 556P05BK | Panelist 5 Light Pendant | CAT3 | 7 | 10 | 5,275.76 | 8 | — |
| 558P09FG | Petal Court 9 Light Pendant | CAT3 | 3 | 5 | 4,688.25 | 4 | — |
| 551T01BRZ | Hope 1 Light Table Lamp - Malouf Foundation Partnership - Heritage Bronze | CAT10 | 27 | 46 | 4,282.16 | 27 | — |
| 557W04HG | Aurora 4 Light Sconce | CAT1 | 11 | 22 | 4,206.05 | 13 | — |
| 576C08BG | Rockford 8 Light Chandelier | CAT2 | 9 | 13 | 4,173.10 | 10 | — |
| 577C08SB | Brass Tax 8 Light Chandelier | CAT2 | 8 | 11 | 3,957 | 8 | — |
| 393W03MBFG | Park Row 3 Light Sconce - Matte Black/French Gold | CAT1 | 8 | 19 | 3,809.48 | 8 | — |
| 309N12HG | Matrix 12 Light Linear - Havana Gold | CAT4 | 1 | 3 | 3,779.10 | 1 | — |
| 557F09HG | Aurora 9 Light Pendant | CAT3 | 5 | 6 | 3,756.12 | 5 | — |
| 583N60SG | Double Standard 60 inch Dimmable LED Linear Pendant | CAT4 | 2 | 3 | 3,584.25 | 3 | — |
| 323P05OG | Cannery 5 Light Pendant - Ombre Galvanized Steel | CAT3 | 6 | 8 | 3,550.20 | 6 | — |
| 570P06DBFG | Aristocrat 6 Light Pendant | CAT3 | 7 | 9 | 3,539.70 | 7 | — |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 297P25HG | Social Club 25 Light 5-Tier - Havana Gold | COL15 | 30,355.33 | 12 | — | 2026-7-17 | [{'customer': 'Ferguson Enterprises', 'revenue': 7216.02}, {'customer': 'Epiphany', 'revenue': 6014.22}, {'customer': 'Illuminations - McAllen TX', 'revenue': 3921.75}, {'customer': 'CED dba Notoco Industries', 'revenue': 2954.5}, {'customer': 'Lee Supply', 'revenue': 2614.5}, {'customer': 'Carrington Lighting', 'revenue': 2614.5}, {'customer': 'Lightstyle of Orlando', 'revenue': 2614.5}, {'customer': 'Ferguson Enterprises', 'revenue': 2405.34}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Fort Worth Lighting', 'revenue': 0.0}, {'customer': "Graham's Lighting Franklin", 'revenue': 0.0}, {'customer': 'Home Lighting', 'revenue': 0.0}, {'customer': 'Hubbard Pipe & Supply, Inc', 'revenue': 0.0}, {'customer': 'American Lighting', 'revenue': 0.0}, {'customer': 'Kristi Hopper Designs', 'revenue': 0.0}, {'customer': 'Lando Lighting', 'revenue': 0.0}, {'customer': 'Lights Unlimited Of Garner', 'revenue': 0.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 0.0}, {'customer': 'LightStyles', 'revenue': 0.0}, {'customer': 'Littman Bros. Lighting', 'revenue': 0.0}, {'customer': 'M & M Lighting', 'revenue': 0.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 0.0}, {'customer': 'Michigan Chandelier', 'revenue': 0.0}, {'customer': 'Progressive Lighting', 'revenue': 0.0}, {'customer': 'Ray Mart Inc. dba Tri Supply Company', 'revenue': 0.0}, {'customer': 'Varaluz LLC', 'revenue': 0.0}, {'customer': 'We Got Lites, Inc.', 'revenue': 0.0}, {'customer': 'Wage Lighting', 'revenue': 0.0}, {'customer': 'Illuminations', 'revenue': 0.0}, {'customer': "Brecher's - Louisville", 'revenue': 0.0}, {'customer': "Cappadonna's", 'revenue': 0.0}, {'customer': 'Cleveland Lighting One', 'revenue': 0.0}, {'customer': 'Elan Studio Lighting', 'revenue': 0.0}, {'customer': 'Envy Interiors', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Distribution Center #320 Grand Prairie', 'revenue': 0.0}] | [{'item': '297B01HG', 'desc': 'Social Club 1 Light Bath - Havana Gold', 'available': 11}, {'item': '297B02HG', 'desc': 'Social Club 2 Light Bath - Havana Gold', 'available': 11}, {'item': '297B03HG', 'desc': 'Social Club 3 Light Bath - Havana Gold', 'available': 7}, {'item': '297P09HG', 'desc': 'Social Club 9 Light 2-Tier Crystal Pendant - Havana Gold', 'available': 7}, {'item': '297P15HG', 'desc': 'Social Club 15 Light 3-Tier Crystal Pendant - Havana Gold', 'available': 6}, {'item': '297B04HG', 'desc': 'Social Club 4 Light Bath - Havana Gold', 'available': 5}] |
| 4DMI0108 | Kye 22x40 Rounded Rectangular Wall Mirror - Gold | KYE | 23,747.72 | 104 | — | 2026-6-24 | [{'customer': 'Studio 41', 'revenue': 3697.12}, {'customer': 'Varaluz LLC', 'revenue': 3116.44}, {'customer': 'Southern Lights', 'revenue': 1975.5}, {'customer': 'Ferguson Enterprises', 'revenue': 1316.98}, {'customer': 'Hermitage Electric Supply', 'revenue': 1227.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 1112.5}, {'customer': 'Beautiful Lights', 'revenue': 998.0}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 735.84}, {'customer': 'BLUE SKY DESIGN OF NWF LLC', 'revenue': 726.54}, {'customer': 'Muska Lighting Center', 'revenue': 703.5}, {'customer': 'Ferguson Enterprises', 'revenue': 564.42}, {'customer': 'First Coast Lighting and Fans', 'revenue': 499.0}, {'customer': "Mahlander's", 'revenue': 499.0}, {'customer': 'Briggs Inc of Omaha', 'revenue': 499.0}, {'customer': "Amini's Galleria", 'revenue': 499.0}, {'customer': 'Alloway Lighting', 'revenue': 492.0}, {'customer': 'Cooks Lighting & Flooring', 'revenue': 409.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 409.0}, {'customer': 'Modern Lighting', 'revenue': 409.0}, {'customer': 'Ferguson Enterprises', 'revenue': 376.28}, {'customer': 'Ferguson Enterprises', 'revenue': 376.28}, {'customer': 'Phillips Lighting & Home, Inc.', 'revenue': 374.25}, {'customer': 'Ferguson Enterprises', 'revenue': 352.82}, {'customer': 'Fusion Light and Design', 'revenue': 260.05}, {'customer': 'Venturi Capital, Inc. DBA Design Superstore', 'revenue': 252.99}, {'customer': 'Maison Kitchen & Bath, LLC', 'revenue': 249.5}, {'customer': 'Ferguson Enterprises', 'revenue': 211.18}, {'customer': 'Posh Lighting', 'revenue': 204.5}, {'customer': 'BR6 - Wiseway Supply - Lexington', 'revenue': 204.5}, {'customer': 'Lumi Lighting & Home Design LLC', 'revenue': 204.5}, {'customer': 'Cleveland Lighting One', 'revenue': 204.5}, {'customer': 'Gross Electric - Toledo', 'revenue': 204.5}, {'customer': 'Shallotte Electric', 'revenue': 204.5}, {'customer': 'Ferguson Enterprises', 'revenue': 169.33}, {'customer': 'Ferguson Enterprises', 'revenue': 9.2}, {'customer': 'Paint Plus Lighting and Design', 'revenue': 0.0}, {'customer': 'Shoreline Property Group', 'revenue': 0.0}, {'customer': '43rd Street Lighting, Inc', 'revenue': 0.0}, {'customer': 'Spectrum Lighting', 'revenue': 0.0}, {'customer': 'Urban Lights', 'revenue': 0.0}, {'customer': 'VAMAC, Inc.', 'revenue': 0.0}, {'customer': 'Varaluz Friends and Family Orders', 'revenue': 0.0}, {'customer': 'Solas Lighting and Design', 'revenue': 0.0}, {'customer': 'Accent Lighting', 'revenue': 0.0}, {'customer': 'Accent Lighting', 'revenue': 0.0}, {'customer': 'All Phase Petoskey', 'revenue': 0.0}, {'customer': 'Black Whale Lighting', 'revenue': 0.0}, {'customer': 'Coventry Lighting Inc', 'revenue': 0.0}, {'customer': 'Dominion Electric Supply', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Focal Point Hardware', 'revenue': 0.0}, {'customer': 'Galleria Lighting', 'revenue': 0.0}, {'customer': 'Inside Source', 'revenue': 0.0}, {'customer': 'Kaelins, Inc.', 'revenue': 0.0}, {'customer': 'Lighting Star', 'revenue': 0.0}, {'customer': 'Lighting World Decorator', 'revenue': 0.0}, {'customer': 'Lighting One of Cincinnati', 'revenue': 0.0}, {'customer': 'LIGHTOPIA WAREHOUSE', 'revenue': 0.0}, {'customer': 'Lights On Banks', 'revenue': 0.0}, {'customer': 'Littman Bros. Lighting', 'revenue': 0.0}, {'customer': 'Lowcountry Lighting Studio', 'revenue': 0.0}, {'customer': 'M & M Glass LLC', 'revenue': 0.0}, {'customer': 'Madison Lighting, Ltd', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': "Montgomery's", 'revenue': 0.0}] | [{'item': '407A02BL', 'desc': 'Kye 24x30 Rectangular Rounded Wall Mirror - Black', 'available': 134}, {'item': '407A04BZ', 'desc': 'Kye 30x30 Rounded Square Wall Mirror - Bronze', 'available': 125}, {'item': '407A02BZ', 'desc': 'Kye 24x30 Rectangular Rounded Wall Mirror - Bronze', 'available': 123}, {'item': '407A06BL', 'desc': 'Kye 40x40 Rounded Square Wall Mirror - Black', 'available': 104}, {'item': '407A04BL', 'desc': 'Kye 30x30 Rounded Square Wall Mirror - Black', 'available': 76}, {'item': '4DMI0109', 'desc': 'Kye 22x40 Rounded Rectangular Wall Mirror - Polished Nickel', 'available': 70}, {'item': '407A02GO', 'desc': 'Kye 24x30 Rectangular Rounded Wall Mirror - Gold', 'available': 46}, {'item': '407A04GO', 'desc': 'Kye 30x30 Rounded Square Wall Mirror - Gold', 'available': 34}, {'item': '4DMI0107', 'desc': 'Kye 22x40 Rounded Rectangular Wall Mirror - Black', 'available': 33}, {'item': '407A06GO', 'desc': 'Kye 40x40 Rounded Square Wall Mirror - Gold', 'available': 2}, {'item': '407A02PN', 'desc': 'Kye 30x24 Rounded Rectangular Wall Mirror - Polished Nickel', 'available': 1}] |
| 376W02BN | Morgan 2 Light Sconce - Brushed Nickel | COL6 | 21,663.60 | 199 | — | 2026-10-16 | [{'customer': 'Wholesale Lighting', 'revenue': 16303.49}, {'customer': 'Luxury Design Inc.', 'revenue': 1716.08}, {'customer': 'Ferguson - Knoxville TN 391', 'revenue': 792.75}, {'customer': 'Elements', 'revenue': 466.2}, {'customer': 'Lighting Originals', 'revenue': 324.36}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 291.6}, {'customer': 'Alloway Lighting', 'revenue': 259.0}, {'customer': 'Muska Lighting Center', 'revenue': 259.0}, {'customer': 'Lighting First', 'revenue': 259.0}, {'customer': 'Urban Lights', 'revenue': 256.41}, {'customer': 'Progressive Lighting', 'revenue': 233.1}, {'customer': 'Peak Lighting', 'revenue': 198.0}, {'customer': 'Lamps Plus/Pacific Coast Lighting', 'revenue': 154.6}, {'customer': 'Lighting Instyle', 'revenue': 150.01}, {'customer': 'Varaluz LLC', 'revenue': 0.0}, {'customer': 'BR6 - Wiseway Supply - Lexington', 'revenue': 0.0}, {'customer': 'Bee Ridge Lighting', 'revenue': 0.0}, {'customer': 'Black Whale Lighting', 'revenue': 0.0}, {'customer': 'Ciana Varaluz Lighting', 'revenue': 0.0}, {'customer': 'Cleveland Lighting South', 'revenue': 0.0}, {'customer': 'Creative Lighting', 'revenue': 0.0}, {'customer': 'Dominion Electric Supply', 'revenue': 0.0}, {'customer': 'Elektra', 'revenue': 0.0}, {'customer': 'A&M Illumination DBA Forest Hill Lighting', 'revenue': 0.0}, {'customer': 'Light House Gallery', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': 'Northern Lighting Inc', 'revenue': 0.0}, {'customer': 'Patdo Electrical Supply Co., Inc.', 'revenue': 0.0}, {'customer': 'Tallahassee Lighting', 'revenue': 0.0}] | [{'item': '376W03BL', 'desc': 'Morgan 3 Light Sconce - Black', 'available': 111}, {'item': '376W03BN', 'desc': 'Morgan 3 Light Sconce - Brushed Nickel', 'available': 94}, {'item': '376W02BL', 'desc': 'Morgan 2 Light Sconce - Black', 'available': 71}, {'item': '376W03SB', 'desc': 'Morgan 3 Light Sconce - Satin Brass', 'available': 59}, {'item': '376B03BN', 'desc': 'Morgan 3 Light Bath - Brushed Nickel', 'available': 54}, {'item': '376B04BN', 'desc': 'Morgan 4 Light Bath - Brushed Nickel', 'available': 44}, {'item': '376B04BL', 'desc': 'Morgan 4 Light Bath - Black', 'available': 42}, {'item': '376B03BL', 'desc': 'Morgan 3 Light Bath - Black', 'available': 42}, {'item': '376W02SB', 'desc': 'Morgan 2 Light Sconce - Satin Brass', 'available': 41}, {'item': '376W01SB', 'desc': 'Morgan 1 Light Sconce - Satin Brass', 'available': 40}, {'item': '376B03SB', 'desc': 'Morgan 3 Light Bath - Satin Brass', 'available': 30}, {'item': '376B04SB', 'desc': 'Morgan 4 Light Bath - Satin Brass', 'available': 10}, {'item': '376W01BL', 'desc': 'Morgan 1 Light Sconce - Black', 'available': 10}] |
| 309P03HG | Matrix 3 Light Pendant - Havana Gold | COL1 | 19,915.02 | 40 | — | 2026-6-26 | [{'customer': 'Light Source Lighting', 'revenue': 3417.0}, {'customer': 'Beautiful Things Lighting', 'revenue': 2847.5}, {'customer': 'N&S Electric Supply', 'revenue': 1423.5}, {'customer': 'Ferguson Enterprises', 'revenue': 1309.62}, {'customer': 'Ferguson Enterprises', 'revenue': 1225.44}, {'customer': 'Ferguson Enterprises', 'revenue': 1098.9}, {'customer': 'Wholesale Lighting', 'revenue': 949.0}, {'customer': 'Ferguson Enterprises', 'revenue': 873.08}, {'customer': 'Fort Worth Lighting', 'revenue': 569.5}, {'customer': 'Fan & Lighting World', 'revenue': 541.02}, {'customer': 'Raymond de Steiger, Inc.', 'revenue': 508.24}, {'customer': 'LED Capstone LLC', 'revenue': 474.5}, {'customer': 'Southern Lights', 'revenue': 474.5}, {'customer': 'Spectrum Lighting', 'revenue': 474.5}, {'customer': 'Lights Unlimited Of Garner', 'revenue': 474.5}, {'customer': 'Ferguson Enterprises', 'revenue': 436.54}, {'customer': 'Ferguson Enterprises', 'revenue': 436.54}, {'customer': 'Ferguson Enterprises', 'revenue': 436.54}, {'customer': '1800Lighting - Capitol Lighting', 'revenue': 427.05}, {'customer': 'Lighting First', 'revenue': 427.05}, {'customer': 'Winnelson Hendersonville', 'revenue': 379.0}, {'customer': 'The Bulb Bin', 'revenue': 284.75}, {'customer': 'Ferguson Enterprises', 'revenue': 237.25}, {'customer': 'Ferguson Enterprises', 'revenue': 189.5}, {'customer': 'Illuminations', 'revenue': 0.0}, {'customer': 'Lighting Instyle', 'revenue': 0.0}, {'customer': 'Lamps Plus/Pacific Coast Lighting', 'revenue': 0.0}, {'customer': 'Lighting First', 'revenue': 0.0}, {'customer': 'Lighting Resource Studio', 'revenue': 0.0}, {'customer': 'Lighting Star', 'revenue': 0.0}, {'customer': 'Light Innovations', 'revenue': 0.0}, {'customer': 'Lighting Etc', 'revenue': 0.0}, {'customer': 'LIGHTOPIA WAREHOUSE', 'revenue': 0.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 0.0}, {'customer': 'Lights of Oconee', 'revenue': 0.0}, {'customer': 'Littman Bros. Lighting', 'revenue': 0.0}, {'customer': 'Lumber One Home Center', 'revenue': 0.0}, {'customer': 'Lumen Nation', 'revenue': 0.0}, {'customer': 'Madison Creek Furnishings and Design', 'revenue': 0.0}, {'customer': 'Mechanical Electrical Wholesale Supply, Inc.', 'revenue': 0.0}, {'customer': 'Modern Lighting', 'revenue': 0.0}, {'customer': 'Matchez International Inc dba Parkyn Design', 'revenue': 0.0}, {'customer': 'Pine Tree Lighting', 'revenue': 0.0}, {'customer': 'Progressive Lighting', 'revenue': 0.0}, {'customer': 'Rbdelaa Lighting', 'revenue': 0.0}, {'customer': 'Rensen House of Lights', 'revenue': 0.0}, {'customer': 'Royce Collection', 'revenue': 0.0}, {'customer': 'Signature Lighting and Fans', 'revenue': 0.0}, {'customer': 'Sunbelt Lighting LLC', 'revenue': 0.0}, {'customer': 'The Lighting Boutique', 'revenue': 0.0}, {'customer': "Eclairage Union Montreal-La Cie D'eclairage Union", 'revenue': 0.0}, {'customer': 'Universal Lamp', 'revenue': 0.0}, {'customer': 'Urban Lights', 'revenue': 0.0}, {'customer': 'Versallies', 'revenue': 0.0}, {'customer': 'ABC Creations LLC', 'revenue': 0.0}, {'customer': 'Elume Distinctive Lighting', 'revenue': 0.0}, {'customer': '1800Lighting - Capitol Lighting', 'revenue': 0.0}, {'customer': 'LBU Lighting', 'revenue': 0.0}, {'customer': 'CLIVE DANIEL HOME - WAREHOUSE', 'revenue': 0.0}, {'customer': 'Colonial Electric Supply Company. Inc', 'revenue': 0.0}, {'customer': 'Coventry Lighting Inc', 'revenue': 0.0}, {'customer': 'Cregger Company, Inc.', 'revenue': 0.0}, {'customer': 'Dement Lighting', 'revenue': 0.0}, {'customer': 'Designer Lighting and Fan Inc', 'revenue': 0.0}, {'customer': 'Epiphany', 'revenue': 0.0}, {'customer': 'Ethan and Associates', 'revenue': 0.0}, {'customer': 'Farmville Wholesale Electric Supply Co.', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'First Coast Lighting and Fans', 'revenue': 0.0}, {'customer': "Graham's Lighting Franklin", 'revenue': 0.0}] | [{'item': '309W02LHG', 'desc': 'Matrix 2 Light 2-Tier Sconce - Havana Gold', 'available': 30}, {'item': '309W02LMBFG', 'desc': 'Matrix 2 Light 2-Tier Sconce - Matte Black/French Gold', 'available': 29}, {'item': '309W02HG', 'desc': 'Matrix 2 Light Sconce - Havana Gold', 'available': 24}, {'item': '309P12HG', 'desc': 'Matrix 12 Light Pendant - Havana Gold', 'available': 23}, {'item': '309P10HG', 'desc': 'Matrix 10 Light Pendant - Havana Gold', 'available': 19}, {'item': '309P06HG', 'desc': 'Matrix 6 Light Pendant - Havana Gold', 'available': 17}, {'item': '309B03MBFG', 'desc': 'Matrix 3 Light Bath - Matte Black/French Gold', 'available': 17}, {'item': '309P09MBFG', 'desc': 'Matrix 9 Light Pendant - Matte Black/French Gold', 'available': 17}, {'item': '309C30HG', 'desc': 'Matrix 30Light 4-Tier Chandelier - Havana Gold', 'available': 14}, {'item': '309C19HG', 'desc': 'Matrix 18 Light 3-Tier Chandelier - Havana Gold', 'available': 13}, {'item': '309T03MBFG', 'desc': 'Matrix 3 Light Table Lamp - Matte Black/French Gold', 'available': 12}, {'item': '309N06HG', 'desc': 'Matrix 6 Light Linear - Havana Gold', 'available': 12}, {'item': '309N06MBFG', 'desc': 'Matrix 6 Light Linear Pendant - Matte Black/French Gold', 'available': 10}, {'item': '309W01MBFG', 'desc': 'Matrix 1 Light Sconce - Matte Black/French Gold', 'available': 10}, {'item': '309N08HG', 'desc': 'Matrix 8 Light Linear - Havana Gold', 'available': 10}, {'item': '309L06MBFG', 'desc': 'Matrix 6 Light Floor Lamp - Matte Black/French Gold', 'available': 10}, {'item': '309P03MBFG', 'desc': 'Matrix 3 Light Pendant - Matte Black/French Gold', 'available': 9}, {'item': '309C14MBFG', 'desc': 'Matrix 14 Light 2-Tier Chandelier - Matte Black/French Gold', 'available': 9}, {'item': '309N12MBFG', 'desc': 'Matrix 12 Light Linear - Matte Black & French Gold', 'available': 9}, {'item': '309P06MBFG', 'desc': 'Matrix 6 Light Pendant - Matte Black/French Gold', 'available': 9}, {'item': '309C19MBFG', 'desc': 'Matrix 18 Light 3-Tier Chandelier - Matte Black/French Gold', 'available': 9}, {'item': '309W01HG', 'desc': 'Matrix 1 Light Sconce - Havana Gold', 'available': 8}, {'item': '309C14HG', 'desc': 'Matrix 14 Light 2-Tier Chandelier - Havana Gold', 'available': 7}, {'item': '309N10MBFG', 'desc': 'Matrix 10 Light Linear - Matte Black & French Gold', 'available': 7}, {'item': '309L06HG', 'desc': 'Matrix 6 Light Floor Lamp - Havana Gold', 'available': 7}, {'item': '309P12MBFG', 'desc': 'Matrix 12 Light Pendant - Matte Black/French Gold', 'available': 7}, {'item': '309T03HG', 'desc': 'Matrix 3 Light Table Lamp - Havana Gold', 'available': 7}, {'item': '309P09HG', 'desc': 'Matrix 9 Light Pendant - Havana Gold', 'available': 6}, {'item': '309B03HG', 'desc': 'Matrix 3 Light Bath - Havana Gold', 'available': 6}, {'item': '309P10MBFG', 'desc': 'Matrix 10 Light Pendant - Matte Black/French Gold', 'available': 6}, {'item': '309N12HG', 'desc': 'Matrix 12 Light Linear - Havana Gold', 'available': 6}, {'item': '309N08MBFG', 'desc': 'Matrix 8 Light Linear Pendant - Matte Black/French Gold', 'available': 4}, {'item': '309N10HG', 'desc': 'Matrix 10 Light Linear - Havana Gold', 'available': 4}, {'item': '309B02HG', 'desc': 'Matrix 2 Light Bath - Havana Gold', 'available': 3}, {'item': '309C30MBFG', 'desc': 'Matrix 30Light 4-Tier Chandelier - Matte Black/French Gold', 'available': 3}, {'item': '309B02MBFG', 'desc': 'Matrix 2 Light Bath - Matte Black/French Gold', 'available': 2}] |
| 380P05MBFG | Estela 5 Light Pendant - Matte Black/French Gold | COL62 | 15,066.97 | 19 | — | 2026-6-29 | [{'customer': 'CARMEL COLOR HOUSE', 'revenue': 3233.39}, {'customer': 'Georgia Lighting', 'revenue': 2758.83}, {'customer': 'Wilson Lighting - Overland Park KS', 'revenue': 2293.5}, {'customer': 'Light Bulbs Etc. - Costa Mesa', 'revenue': 1824.5}, {'customer': 'Danielhouse Studios Inc', 'revenue': 764.5}, {'customer': 'BR6 - Wiseway Supply - Lexington', 'revenue': 764.5}, {'customer': 'City Lights', 'revenue': 764.5}, {'customer': 'Cleveland Lighting One', 'revenue': 764.5}, {'customer': 'Cleveland Lighting South', 'revenue': 764.5}, {'customer': 'BBC Lighting', 'revenue': 764.5}, {'customer': 'Naples Lighting and Fan Depot', 'revenue': 369.75}, {'customer': "Brecher's - Louisville", 'revenue': 0.0}] | [{'item': '380M01MBFG', 'desc': 'Estela 1 Light Mini Pendant - Matte Black/French Gold', 'available': 13}, {'item': '380MI30AMBFG', 'desc': 'Estela 30-in Round Wall Mirror - Matte Black/French Gold', 'available': 9}, {'item': '380W02MBFG', 'desc': 'Estela 2 Light Sconce - Matte Black/French Gold', 'available': 7}, {'item': '380N05MBFG', 'desc': 'Estela 5 Light Linear Pendant - Matte Black/French Gold', 'available': 6}, {'item': '380P03MBFG', 'desc': 'Estela 3 Light Convertible Pendant/Semi-Flush - Matte Black/French Gold', 'available': 6}, {'item': '380MI30BMBFG', 'desc': 'Estela 30x40 Rectangular Wall Mirror - Matte Black/French Gold', 'available': 5}, {'item': '380F06MBFG', 'desc': 'Estela 6 Light Foyer - Matte Black/French Gold', 'available': 4}, {'item': '380N06MBFG', 'desc': 'Estela 6 Light   Linear Pendant - Matte Black/French Gold', 'available': 1}] |
| 348N06HG | Kato 6 Light Oval Pendant - Havana Gold | KATO | 13,334.16 | 18 | — | 2026-7-31 | [{'customer': 'Lighting First', 'revenue': 2794.85}, {'customer': 'Lighting First', 'revenue': 2714.4}, {'customer': 'Light Source Lighting', 'revenue': 1641.16}, {'customer': 'Hills Lighting', 'revenue': 1609.0}, {'customer': 'Fort Worth Lighting', 'revenue': 904.5}, {'customer': 'CARMEL COLOR HOUSE', 'revenue': 884.95}, {'customer': 'The Nest DBA Cregger Company', 'revenue': 804.5}, {'customer': "Mahlander's", 'revenue': 804.5}, {'customer': 'Elements', 'revenue': 724.05}, {'customer': 'Lighting First', 'revenue': 452.25}, {'customer': 'Rensen House of Lights', 'revenue': 0.0}, {'customer': 'Rittenhouse Electric', 'revenue': 0.0}, {'customer': 'Riverside Lighting and Electric', 'revenue': 0.0}, {'customer': 'Salt Box', 'revenue': 0.0}, {'customer': 'Acropolis', 'revenue': 0.0}, {'customer': 'Sunbelt Lighting LLC', 'revenue': 0.0}, {'customer': 'Cartwright Lighting and Furniture Ltd.', 'revenue': 0.0}, {'customer': "Christie's Lighting Gallery", 'revenue': 0.0}, {'customer': 'CLIVE DANIEL HOME - WAREHOUSE', 'revenue': 0.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'The Light House of Lewes', 'revenue': 0.0}, {'customer': 'Lighting World Decorator', 'revenue': 0.0}, {'customer': 'Park Lighting', 'revenue': 0.0}, {'customer': 'Progressive Lighting', 'revenue': 0.0}] | [{'item': '348W02HG', 'desc': 'Kato 2 Light Wall Sconce - Havana Gold', 'available': 13}, {'item': '348P06CB', 'desc': 'Kato 6 Light Pendant - Carbon Black', 'available': 12}, {'item': '348P06HG', 'desc': 'Kato 6 Light Pendant - Havana Gold', 'available': 10}, {'item': '348W02CB', 'desc': 'Kato 2 Light Wall Sconce - Carbon Black', 'available': 10}, {'item': '348P04HG', 'desc': 'Kato 4 Light 3-Tier Pendant - Havana Gold', 'available': 9}, {'item': '348F16CB', 'desc': 'Kato 16 Light 3-Tier Foyer - Carbon', 'available': 9}, {'item': '348P05HG', 'desc': 'Kato 5 Light Pendant - Havana Gold', 'available': 6}, {'item': '348S05CB', 'desc': 'Kato 5 Light Convertible Semi-Flush/Pendant - Carbon', 'available': 5}, {'item': '348S06HG', 'desc': 'Kato 6 Light Convertible Semi-Flush/Pendant - Havana Gold', 'available': 5}, {'item': '348S06CB', 'desc': 'Kato 6 Light Convertible Semi-Flush/Pendant - Carbon', 'available': 5}, {'item': '348F16HG', 'desc': 'Kato 16 Light 3-Tier Foyer - Havana Gold', 'available': 4}, {'item': '348P05CB', 'desc': 'Kato 5 Light Pendant - Carbon Black', 'available': 2}, {'item': '348P04CB', 'desc': 'Kato 4 Light 3-Tier Pendant - Carbon Black', 'available': 1}, {'item': '348N06CB', 'desc': 'Kato 6 Light Oval Pendant - Carbon Black', 'available': 1}, {'item': '348S05HG', 'desc': 'Kato 5 Light Convertible Semi-Flush/Pendant - Havana Gold', 'available': 1}] |
| 297P19HG | Social Club 19 Light 4-Tier - Havana Gold | COL15 | 12,091.69 | 8 | — | 2026-6-26 | [{'customer': 'Hunzicker Brothers', 'revenue': 2094.5}, {'customer': 'Versallies', 'revenue': 1844.5}, {'customer': 'Cleveland Lighting One', 'revenue': 1844.5}, {'customer': 'Lighting Instyle', 'revenue': 1844.5}, {'customer': 'Lee Supply', 'revenue': 1844.5}, {'customer': 'Ferguson Enterprises', 'revenue': 1696.94}, {'customer': 'Ferguson Distribution Center #320 Grand Prairie', 'revenue': 922.25}, {'customer': 'Home Lighting', 'revenue': 0.0}, {'customer': 'Hubbard Pipe & Supply, Inc', 'revenue': 0.0}, {'customer': 'Illuminations - McAllen TX', 'revenue': 0.0}, {'customer': 'Lamps Plus/Pacific Coast Lighting', 'revenue': 0.0}, {'customer': 'Lampworks, Inc dba Lamp & Shade Works, Inc.', 'revenue': 0.0}, {'customer': 'Lando Lighting', 'revenue': 0.0}, {'customer': 'Lighting by Fox', 'revenue': 0.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 0.0}, {'customer': 'Luz Love', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': 'Michigan Chandelier', 'revenue': 0.0}, {'customer': 'Modern Lighting', 'revenue': 0.0}, {'customer': "Montgomery's", 'revenue': 0.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 0.0}, {'customer': 'Texas Lighting & More', 'revenue': 0.0}, {'customer': 'Varaluz LLC', 'revenue': 0.0}, {'customer': 'Northwest Interiors dba Champions Lighting', 'revenue': 0.0}, {'customer': 'Wendy Mayes Design', 'revenue': 0.0}, {'customer': 'Ciana Varaluz Lighting', 'revenue': 0.0}, {'customer': 'Coventry Lighting Inc', 'revenue': 0.0}, {'customer': 'Denali Lighting One', 'revenue': 0.0}, {'customer': 'Designer Lighting and Fan Inc', 'revenue': 0.0}, {'customer': 'Ethan and Associates', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}] | [{'item': '297B01HG', 'desc': 'Social Club 1 Light Bath - Havana Gold', 'available': 11}, {'item': '297B02HG', 'desc': 'Social Club 2 Light Bath - Havana Gold', 'available': 11}, {'item': '297B03HG', 'desc': 'Social Club 3 Light Bath - Havana Gold', 'available': 7}, {'item': '297P09HG', 'desc': 'Social Club 9 Light 2-Tier Crystal Pendant - Havana Gold', 'available': 7}, {'item': '297P15HG', 'desc': 'Social Club 15 Light 3-Tier Crystal Pendant - Havana Gold', 'available': 6}, {'item': '297B04HG', 'desc': 'Social Club 4 Light Bath - Havana Gold', 'available': 5}] |
| 389P06MBHN | Blonde Moment 6 Light   Pendant - Matte Black/Honey/Medium Oak | COL67 | 11,456.18 | 18 | — | 2026-7-30 | [{'customer': 'Lyteworks', 'revenue': 1708.5}, {'customer': 'PDI', 'revenue': 1139.0}, {'customer': 'IBS LIGHTING LTD', 'revenue': 829.19}, {'customer': 'The Light Center', 'revenue': 736.8}, {'customer': 'Lighting Star', 'revenue': 664.5}, {'customer': 'N&S Electric Supply', 'revenue': 664.5}, {'customer': 'Dulles Electric Supply Corp', 'revenue': 664.5}, {'customer': 'Kenneth Ludwig Chicago', 'revenue': 645.29}, {'customer': 'Urban Lights', 'revenue': 612.81}, {'customer': 'Ferguson - Knoxville TN 391', 'revenue': 611.34}, {'customer': 'Lighting Instyle', 'revenue': 569.5}, {'customer': 'The Nest DBA Cregger Company', 'revenue': 569.5}, {'customer': 'Greer Lighting Center, LLC', 'revenue': 569.5}, {'customer': "Hagen's Lighting", 'revenue': 569.5}, {'customer': 'Avid Lighting', 'revenue': 569.5}, {'customer': 'Cabinet & Lighting Supply', 'revenue': 332.25}, {'customer': 'Madison Creek Furnishings and Design', 'revenue': 0.0}, {'customer': 'Lighting First', 'revenue': 0.0}, {'customer': 'Lights and More', 'revenue': 0.0}, {'customer': 'Southern Lights', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'First Coast Lighting and Fans', 'revenue': 0.0}] | [{'item': '389W01MBHN', 'desc': 'Blonde Moment 1 Light   Sconce - Matte Black/Honey/Medium Oak', 'available': 14}, {'item': '389N05MBHN', 'desc': 'Blonde Moment 5 Light   Linear Pendant - Matte Black/Honey/Medium Oak', 'available': 10}, {'item': '389S03MBHN', 'desc': 'Blonde Moment 3 Light   Semi-Flush - Matte Black/Honey/Medium Oak', 'available': 4}] |
| 345C21CBHG | Windsor 21 Light 4-Tier Crystal Chandelier - Carbon/Havana Gold | COL7 | 10,797.04 | 2 | — | 2026-7-17 | [{'customer': 'Frost Interiors Inc', 'revenue': 5997.44}, {'customer': 'Texas Lighting & More', 'revenue': 4799.6}, {'customer': 'Colonial Electric Supply Company. Inc', 'revenue': 0.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 0.0}, {'customer': 'Illuminations - McAllen TX', 'revenue': 0.0}, {'customer': 'Lampworks, Inc dba Lamp & Shade Works, Inc.', 'revenue': 0.0}, {'customer': 'Lando Lighting', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': 'PDI', 'revenue': 0.0}, {'customer': 'Showcase Lighting by 3G', 'revenue': 0.0}, {'customer': 'Ray Mart Inc. dba Tri Supply Company', 'revenue': 0.0}, {'customer': 'Builder Specialties, Inc', 'revenue': 0.0}, {'customer': 'Turn On Lighting', 'revenue': 0.0}, {'customer': '1800Lighting - Capitol Lighting', 'revenue': 0.0}] | [{'item': '345W01CBHG', 'desc': 'Windsor 1 Light Crystal Sconce - Carbon/Havana Gold', 'available': 23}, {'item': '345W01FGMB', 'desc': 'Windsor 1 Light Crystal Sconce - French Gold/Matte Black', 'available': 19}, {'item': '345P04FGMB', 'desc': 'Windsor 4 Light Crystal Pendant - French Gold/Matte Black', 'available': 16}, {'item': '345W02SFGMB', 'desc': 'Windsor 2 Light Small Crystal Sconce - French Gold/Matte Black', 'available': 11}, {'item': '345C13CBHG', 'desc': 'Windsor 13 Light 3-Tier Crystal Chandelier - Carbon/Havana Gold', 'available': 11}, {'item': '345W02CBHG', 'desc': 'Windsor 2 Light Crystal Sconce/Bath - Carbon/Havana Gold', 'available': 10}, {'item': '345B03FGMB', 'desc': 'Windsor 3 Light Crystal Bath - French Gold/Matte Black', 'available': 10}, {'item': '345W02SCBHG', 'desc': 'Windsor 2 Light Crystal Sconce - Carbon/Havana Gold', 'available': 10}, {'item': '345P01CBHG', 'desc': 'Windsor 1 Light Crystal Pendant - Carbon/Havana Gold', 'available': 10}, {'item': '345P06CBHG', 'desc': 'Windsor 6 Light Crystal Pendant - Carbon/Havana Gold', 'available': 10}, {'item': '345C07CBHG', 'desc': 'Windsor 7 Light 2-Tier Crystal Chandelier - Carbon/Havana Gold', 'available': 9}, {'item': '345B04CBHG', 'desc': 'Windsor 4 Light Crystal Bath - Carbon/Havana Gold', 'available': 8}, {'item': '345B03CBHG', 'desc': 'Windsor 3 Light Crystal Bath - Carbon/Havana Gold', 'available': 7}, {'item': '345W02FGMB', 'desc': 'Windsor 2 Light Crystal Sconce - French Gold/Matte Black', 'available': 6}, {'item': '345P06FGMB', 'desc': 'Windsor 6 Light Crystal Pendant - French Gold/Matte Black', 'available': 6}, {'item': '345C07FGMB', 'desc': 'Windsor 7 Light 2-Tier Crystal Chandelier - French Gold/Matte Black', 'available': 6}, {'item': '345N08CBHG', 'desc': 'Windsor 8 Light Crystal Oval Linear Pendant - Carbon/Havana Gold', 'available': 5}, {'item': '345C13FGMB', 'desc': 'Windsor 13 Light 3-Tier Crystal Chandelier - French Gold/Matte Black', 'available': 5}, {'item': '345P01FGMB', 'desc': 'Windsor 1 Light Crystal Pendant - French Gold/Matte Black', 'available': 4}, {'item': '345N08FGMB', 'desc': 'Windsor 8 Light Oval Crystal Linear Pendant - French Gold/Matte Black', 'available': 4}, {'item': '345C21FGMB', 'desc': 'Windsor 21 Light 4-Tier Crystal Chandelier - French Gold/Matte Black', 'available': 3}, {'item': '345P04CBHG', 'desc': 'Windsor 4 Light Crystal Pendant - Carbon/Havana Gold', 'available': 1}] |
| 434MI22CH | Capsule 22x40 Mirror - Chrome | COL69 | 9,975.40 | 45 | — | 2026-9-15 | [{'customer': 'Cleveland Lighting One', 'revenue': 1975.5}, {'customer': 'Dominion Electric Supply', 'revenue': 1497.0}, {'customer': 'Lights of Oconee', 'revenue': 499.0}, {'customer': 'Fort Worth Lighting', 'revenue': 469.0}, {'customer': 'Ferguson ENTERPRISES', 'revenue': 459.08}, {'customer': 'Southern Lights', 'revenue': 439.0}, {'customer': 'The Light Center', 'revenue': 439.0}, {'customer': "Amini's Galleria", 'revenue': 439.0}, {'customer': 'Ferguson Enterprises', 'revenue': 403.88}, {'customer': 'Ferguson Enterprises', 'revenue': 403.88}, {'customer': 'Ferguson Enterprises', 'revenue': 403.88}, {'customer': 'Mars Electric Co.', 'revenue': 395.1}, {'customer': '43rd Street Lighting, Inc', 'revenue': 316.27}, {'customer': 'Dominion Electric Supply', 'revenue': 297.08}, {'customer': 'North Coast Lighting', 'revenue': 249.5}, {'customer': 'Ferguson Enterprises', 'revenue': 229.54}, {'customer': 'Pace Lighting Inc.', 'revenue': 219.5}, {'customer': 'Lighting Etc', 'revenue': 219.5}, {'customer': 'Maison Kitchen & Bath, LLC', 'revenue': 219.5}, {'customer': 'Ferguson Enterprises', 'revenue': 201.94}, {'customer': 'Ferguson Enterprises', 'revenue': 109.75}, {'customer': 'Ferguson Enterprises', 'revenue': 89.5}, {'customer': 'Modern Lighting', 'revenue': 0.0}, {'customer': 'The Nest DBA Cregger Company', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Black Whale Lighting', 'revenue': 0.0}, {'customer': 'Inline Lighting', 'revenue': 0.0}, {'customer': 'Lumber One Home Center', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Masterpiece Lighting - Atlanta', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}] | [{'item': '434MI24CH', 'desc': 'Capsule 24x60 Mirror - Chrome', 'available': 24}, {'item': '434MI24BL', 'desc': 'Capsule 24x60 Mirror - Black', 'available': 14}, {'item': '434MI22BL', 'desc': 'Capsule 22x40 Mirror - Black', 'available': 4}, {'item': '434MI24GO', 'desc': 'Capsule 24x60 Mirror - Gold', 'available': 1}] |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 309N10MBFG | Matrix 10 Light Linear - Matte Black & French Gold | COL1 | 1 | 3,095.10 | [{'customer_code': 'SuperWi', 'customer_name': 'Superlite Lighting', 'collection_revenue': 17898.0}, {'customer_code': 'Ferg#66', 'customer_name': 'Ferguson Enterprises', 'collection_revenue': 15587.87}, {'customer_code': 'FortWorth', 'customer_name': 'Fort Worth Lighting', 'collection_revenue': 14921.0}, {'customer_code': 'CapitalLTG', 'customer_name': 'Capital Lighting & Supply, LLC', 'collection_revenue': 14099.74}, {'customer_code': 'Ferg#320', 'customer_name': 'Ferguson Distribution Center #320 Grand Prairie', 'collection_revenue': 13528.6}, {'customer_code': 'LightSourceI', 'customer_name': 'Light Source Lighting', 'collection_revenue': 13502.99}, {'customer_code': 'Capitol700', 'customer_name': '1800Lighting - Capitol Lighting', 'collection_revenue': 11263.5}, {'customer_code': 'Georgia', 'customer_name': 'Georgia Lighting', 'collection_revenue': 10932.08}, {'customer_code': 'BdeVine', 'customer_name': 'B. de Vine Interiors', 'collection_revenue': 10866.14}, {'customer_code': 'IBS', 'customer_name': 'IBS Lighting', 'collection_revenue': 10832.54}] |
| 309N12HG | Matrix 12 Light Linear - Havana Gold | COL1 | 1 | 3,779.10 | [{'customer_code': 'SuperWi', 'customer_name': 'Superlite Lighting', 'collection_revenue': 17898.0}, {'customer_code': 'Ferg#66', 'customer_name': 'Ferguson Enterprises', 'collection_revenue': 15587.87}, {'customer_code': 'FortWorth', 'customer_name': 'Fort Worth Lighting', 'collection_revenue': 14921.0}, {'customer_code': 'CapitalLTG', 'customer_name': 'Capital Lighting & Supply, LLC', 'collection_revenue': 14099.74}, {'customer_code': 'Ferg#320', 'customer_name': 'Ferguson Distribution Center #320 Grand Prairie', 'collection_revenue': 13528.6}, {'customer_code': 'LightSourceI', 'customer_name': 'Light Source Lighting', 'collection_revenue': 13502.99}, {'customer_code': 'Capitol700', 'customer_name': '1800Lighting - Capitol Lighting', 'collection_revenue': 11263.5}, {'customer_code': 'Georgia', 'customer_name': 'Georgia Lighting', 'collection_revenue': 10932.08}, {'customer_code': 'BdeVine', 'customer_name': 'B. de Vine Interiors', 'collection_revenue': 10866.14}, {'customer_code': 'IBS', 'customer_name': 'IBS Lighting', 'collection_revenue': 10832.54}] |
| 309N12MBFG | Matrix 12 Light Linear - Matte Black & French Gold | COL1 | 1 | 1,049.75 | [{'customer_code': 'ValleyLightG', 'customer_name': 'Valley Light Gallery', 'collection_revenue': 26710.2}, {'customer_code': 'SuperWi', 'customer_name': 'Superlite Lighting', 'collection_revenue': 17898.0}, {'customer_code': 'Ferg#66', 'customer_name': 'Ferguson Enterprises', 'collection_revenue': 15587.87}, {'customer_code': 'FortWorth', 'customer_name': 'Fort Worth Lighting', 'collection_revenue': 14921.0}, {'customer_code': 'CapitalLTG', 'customer_name': 'Capital Lighting & Supply, LLC', 'collection_revenue': 14099.74}, {'customer_code': 'Ferg#320', 'customer_name': 'Ferguson Distribution Center #320 Grand Prairie', 'collection_revenue': 13528.6}, {'customer_code': 'LightSourceI', 'customer_name': 'Light Source Lighting', 'collection_revenue': 13502.99}, {'customer_code': 'Capitol700', 'customer_name': '1800Lighting - Capitol Lighting', 'collection_revenue': 11263.5}, {'customer_code': 'Georgia', 'customer_name': 'Georgia Lighting', 'collection_revenue': 10932.08}, {'customer_code': 'BdeVine', 'customer_name': 'B. de Vine Interiors', 'collection_revenue': 10866.14}, {'customer_code': 'IBS', 'customer_name': 'IBS Lighting', 'collection_revenue': 10832.54}] |
| 570P02DBFG | Aristocrat 2 Light Mini Pendant | COL12 | 1 | 0 | — |
| 297P15HG | Social Club 15 Light 3-Tier Crystal Pendant - Havana Gold | COL15 | 1 | 1,094.50 | — |
| 297W03HG | Social Club 3 Light 2-Tier Crystal Sconce - Havana Gold | COL15 | 2 | 538 | — |
| 428A01BZ | Cottage 30-in Round Mirror - Bronze | COL16 | 0 | 0 | — |
| 270C03BK | Barcelona 3 Light Chandelier - Brass Kisser | COL17 | 0 | 0 | — |
| 270C06BK | Barcelona 6 Light Chandelier - Brass Kisser | COL17 | 1 | 289.75 | — |
| 270C09BK | Barcelona 9 Light 2-Tier Chandelier - Brass Kisser | COL17 | 2 | 419.75 | — |
| 270C12BK | Barcelona 12 Light 3-Tier Chandelier - Brass Kisser | COL17 | 0 | 0 | — |
| 270K02BK | Barcelona 2 Light Sconce with Shade | COL17 | 0 | 0 | — |
| 270K02OX | Barcelona 2 Light Sconce with Shade | COL17 | 0 | 0 | — |
| 270K02TR | Barcelona 2 Light Sconce with Shade - Transcend Silver | COL17 | 0 | 0 | — |
| 270P04BK | Barcelona 3+1 Light Pendant | COL17 | 0 | 0 | — |
| 270P06OX | Barcelona 6 Light Pendant w/Shade | COL17 | 0 | 0 | — |
| 270P06TR | Barcelona 6 Light Pendant w/Shade | COL17 | 0 | 0 | — |
| 270P07BK | Barcelona 6+1 Light Pendant | COL17 | 0 | 0 | — |
| 270P09OX | Barcelona 9 Light Pendant w/Shade | COL17 | 0 | 0 | — |
| 270P09TR | Barcelona 9 Light Pendant w/Shade | COL17 | 0 | 0 | — |
| 270P15BK | Barcelona 15 Light Pendant w/Shade - Brass Kisser | COL17 | 0 | 0 | — |
| 270P15OX | Barcelona 15 Light Pendant w/Shade | COL17 | 0 | 0 | — |
| 270P15TR | Barcelona 15 Light Pendant w/Shade | COL17 | 0 | 0 | — |
| 270W02BK | Barcelona 2 Light Wall Sconce - Brass Kisser | COL17 | 0 | 0 | — |
| 569M01BL | Urchin 1 Light Cylinder Mini Pendant | COL19 | 0 | 0 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
