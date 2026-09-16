# Section 3 Context Bundle — Golden Lighting (gl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=6096, portal_order_gmv=$2.6M |
| HAS_INVENTORY | True | inventory_count=3058 |
| HAS_SALES_DATA | True | sales_data_count=36842 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=28 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$2.6M > ecat_gmv=$131,176: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 28 | engagement_reps=28 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 51 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 240, Mixpanel total submit_order (Q-01): 59 |
| USER_GROUP_SPLIT_AVAILABLE | True | join_rate=98.0%, ambiguous_rate=0.0%, showroom_event_share=13.9% |
| USER_GROUP_JOIN_RATE | 98% | 50 of 51 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 14% | showroom+admin share of matched events: 13.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Sholeh Duncan, Sholeh Duncan |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=2 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=905 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=856 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Golden Lighting
- **Shortname**: gl
- **Org ID**: 187
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
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
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
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

# Signal Rank — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Total signals fired**: 35 (P0: 20, P1: 10, P2: 5)
- **Org GMV**: $0.1M eCat LTM, $2.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 9903-24 MG (Ziva by Golden Lighting Autumn Twilight ) $79,468 LTM, 0 available | P0 | §3 Product | 10.0 | $79,468 | 3.0 | 2,384,038 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 3118-L BLK-SD (Yep by Golden Lighting Hines 1-light 14i) $74,996 LTM, 0 available | P0 | §3 Product | 10.0 | $74,996 | 3.0 | 2,249,878 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 9903-12 MG (Ziva by Golden Lighting Autumn Twilight ) $67,163 LTM, 0 available | P0 | §3 Product | 10.0 | $67,163 | 3.0 | 2,014,876 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 7312-L BP (Golden Lighting Bartlett 2-light Pendant) $58,825 LTM, 0 available | P0 | §3 Product | 10.0 | $58,825 | 3.0 | 1,764,763 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 6805-6 BLK-NR (Golden Lighting Everly 6-light Chandelie) $42,401 LTM, 0 available | P0 | §3 Product | 10.0 | $42,401 | 3.0 | 1,272,043 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 9903-6 MG (Ziva by Golden Lighting Autumn Twilight ) $41,930 LTM, 0 available | P0 | §3 Product | 10.0 | $41,930 | 3.0 | 1,257,908 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 6937-M BLK-NR (Golden Lighting Valentina 1-light Pendan) $41,561 LTM, 0 available | P0 | §3 Product | 10.0 | $41,561 | 3.0 | 1,246,826 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 1270-13 BLK (Wry Lighting Morgon 2-light 13" Flush Mo) $41,544 LTM, 0 available | P0 | §3 Product | 10.0 | $41,544 | 3.0 | 1,246,329 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 6950-L MBS (Golden Lighting Shepard 1-light Pendant ) $34,834 LTM, 0 available | P0 | §3 Product | 10.0 | $34,834 | 3.0 | 1,045,015 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 7312-L CP (Golden Lighting Bartlett 2-light Pendant) $32,869 LTM, 0 available | P0 | §3 Product | 10.0 | $32,869 | 3.0 | 986,058 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 6070-LP BLK-BLK (Golden Lighting Tribeca 5-light Island L) $32,606 LTM, 0 available | P0 | §3 Product | 10.0 | $32,606 | 3.0 | 978,173 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 1017-69 BLK (Golden Lighting Alastair 15-light 2-tier) $28,315 LTM, 0 available | P0 | §3 Product | 10.0 | $28,315 | 3.0 | 849,450 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 1017-96 BLK (Golden Lighting Alastair 15-light 2-tier) $28,248 LTM, 0 available | P0 | §3 Product | 10.0 | $28,248 | 3.0 | 847,438 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 3118-L PW-SD (Yep by Golden Lighting Hines 1-light 14i) $27,819 LTM, 0 available | P0 | §3 Product | 10.0 | $27,819 | 3.0 | 834,563 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — 8001-BA3 BLK-SD (Golden Lighting Parrish 3-light Vanity i) $25,628 LTM, 0 available | P0 | §3 Product | 10.0 | $25,628 | 3.0 | 768,844 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — 3118-L RBZ-SD (Yep by Golden Lighting Hines 1-light 14i) $25,317 LTM, 0 available | P0 | §3 Product | 10.0 | $25,317 | 3.0 | 759,502 | RISK |
| 17 | SIG-OPP-01 | Next Best Product — 3164-FM BCB-HWG/3164-FM BLK-HWG co-purchase pattern across 10 customers | P0 | §2/§3 | 1.0 | $293,278 | 2.0 | 586,555 | POSITIVE |
| 18 | SIG-COMMERCE-01 | Capture Rate — eCat captures 5.0% of $3M total business; each +1pt = $26K | P0 | §4 Commerce | 4.7 | $26,000 | 3.0 | 370,324 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — THE LIGHTING DESIGN CO. 2 consecutive QoQ acceleration quarters, $11,875 peak quarter (+191% QoQ) | P0 | §2 Accounts | 6.4 | $11,875 | 3.0 | 226,694 | POSITIVE |
| 20 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 3 | 0 | 0 | 3 | |
| §3 Product Intelligence | 16 | 0 | 1 | 17 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 9 | 4 | 13 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 3164-FM BCB-HWG/3164-FM BLK-HWG co-purchase pattern across 10 customers
2. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 5.0% of $3M total business; each +1pt = $26K
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — THE LIGHTING DESIGN CO. 2 consecutive QoQ acceleration quarters, $11,875 peak quarter (+191% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 9903-24 MG (Ziva by Golden Lighting Autumn Twilight ) $79,468 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 3118-L BLK-SD (Yep by Golden Lighting Hines 1-light 14i) $74,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 9903-12 MG (Ziva by Golden Lighting Autumn Twilight ) $67,163 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 3,131 | 23 | 0 | 99.30 |

### Q-37_results.md

# Q-37 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9903-24 MG | CHANDELIER | 9903 | Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Mystic Gold | $79,468 | 24 | 0 | 0 | 0 | 2026-10-04 |
| 3118-L BLK-SD | PENDANT | 3118 | Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Seeded Glass | $74,996 | 818 | 0 | 0 | 0 | 2026-08-06 |
| 9903-12 MG | CHANDELIER | 9903 | Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Mystic Gold | $67,163 | 65 | 0 | 0 | 0 | 2026-10-04 |
| 2073-LP GMT | — | — | — | $60,181 | 284 | 0 | 0 | 0 | — |
| 7312-L BP | PENDANT | 7312 | Golden Lighting Bartlett 2-light Pendant in Black Patina | $58,825 | 617 | 0 | 0 | 0 | 2026-08-06 |
| 6805-6 BLK-NR | CHANDELIER | 6805 | Golden Lighting Everly 6-light Chandelier in Matte Black and Natural Rattan shade | $42,401 | 173 | 0 | 0 | 0 | 2026-07-13 |
| 9903-6 MG | CHANDELIER | 9903 | Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Mystic Gold | $41,930 | 67 | 0 | 0 | 0 | 2026-07-20 |
| 6937-M BLK-NR | PENDANT | 6937 | Golden Lighting Valentina 1-light Pendant in Matte Black | $41,561 | 545 | 0 | 0 | 0 | 2026-07-13 |
| 1270-13 BLK | FLUSH MOUNT | 1270 | Wry Lighting Morgon 2-light 13" Flush Mount in Matte Black and Opal Glass | $41,544 | 1,010 | 0 | 0 | 0 | 2026-07-20 |
| 6950-L MBS | PENDANT | 6950 | Golden Lighting Shepard 1-light Pendant in Modern Brass and Modern Brass shade | $34,834 | 284 | 0 | 0 | 0 | 2026-07-20 |
| 1081-5P BLK-PSG | PENDANT | 1081 | Golden Lighting Rue 5-light Pendant in Matte Black and Rubbed Bronze shade | $33,235 | 172 | 0 | 0 | 0 | — |
| 7312-L CP | PENDANT | 7312 | Golden Lighting Bartlett 2-light Pendant in Copper Patina | $32,869 | 307 | 0 | 0 | 0 | 2026-07-20 |
| 6070-LP BLK-BLK | ISLAND LIGHT | 6070 | Golden Lighting Tribeca 5-light Island Light in Matte Black | $32,606 | 165 | 0 | 0 | 0 | 2026-08-06 |
| 1081-8P BLK-PSG | PENDANT | 1081 | Golden Lighting Rue 8-light Chandelier in Matte Black and Rubbed Bronze shade | $30,720 | 103 | 0 | 0 | 0 | — |
| 2073-6 BLK-CLR | CHANDELIER | 2073 | Golden Lighting Smyth 6-light Chandelier in Matte Black | $29,707 | 109 | 0 | 0 | 0 | — |
| 2073-4 GMT | — | — | — | $28,897 | 127 | 0 | 0 | 0 | — |
| 6070-BA3 BLK-PW | — | — | — | $28,497 | 325 | 0 | 0 | 0 | — |
| 1017-69 BLK | CHANDELIER | 1017 | Golden Lighting Alastair 15-light 2-tier Chandelier (6+9) Matte Black | $28,315 | 85 | 0 | 0 | 0 | 2026-07-20 |
| 1017-96 BLK | CHANDELIER | 1017 | Golden Lighting Alastair 15-light 2-tier Chandelier (9+6) in Matte Black | $28,248 | 92 | 0 | 0 | 0 | 2026-07-20 |
| 3118-L PW-SD | PENDANT | 3118 | Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Seeded Glass | $27,819 | 298 | 0 | 0 | 0 | 2026-07-13 |

### Q-38a_results.md

# Q-38a Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-39_category_results.md

# Q-39-cat Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 12
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| PENDANT | $3.1M | 35,420 | 294 | $10,695 |
| VANITY | $2.0M | 24,044 | 314 | $6,288 |
| CHANDELIER | $1.8M | 6,599 | 125 | $14,427 |
| FLUSH MOUNT | $1.3M | 23,781 | 168 | $7,976 |
| SEMI-FLUSH MOUNT | $815,996 | 8,902 | 165 | $4,945 |
| ISLAND LIGHT | $529,721 | 2,909 | 37 | $14,317 |
| WALL SCONCE | $275,916 | 6,136 | 101 | $2,732 |
| SWING ARM WALL LAMP | $111,678 | 1,749 | 42 | $2,659 |
| OUTDOOR WALL | $65,091 | 870 | 17 | $3,829 |
| OUTDOOR PENDANT | $40,136 | 302 | 6 | $6,689 |
| OUTDOOR CEILING | $36,540 | 395 | 13 | $2,811 |
| OUTDOOR POST | $5,425 | 50 | 6 | $904 |

### Q-39_collection_results.md

# Q-39-col Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| 3602 | $1.4M | 22,449 | 194 | $7,300 |
| 3306 | $745,285 | 10,982 | 155 | $4,808 |
| 3604 | $528,207 | 7,457 | 38 | $13,900 |
| 3118 | $486,769 | 6,060 | 69 | $7,055 |
| 9903 | $399,841 | 328 | 9 | $44,427 |
| 2073 | $356,931 | 2,458 | 26 | $13,728 |
| 6068 | $315,979 | 1,721 | 15 | $21,065 |
| 6070 | $278,587 | 2,869 | 17 | $16,387 |
| 7011 | $253,777 | 3,576 | 16 | $15,861 |
| 6956 | $226,616 | 3,187 | 23 | $9,853 |
| 7312 | $194,480 | 2,495 | 27 | $7,203 |
| 3167 | $184,836 | 1,294 | 25 | $7,393 |
| 1081 | $178,007 | 832 | 5 | $35,601 |
| 1094 | $166,780 | 1,517 | 10 | $16,678 |
| 1017 | $155,693 | 614 | 10 | $15,569 |
| 3164 | $154,014 | 1,559 | 14 | $11,001 |
| 4309 | $148,133 | 902 | 14 | $10,581 |
| 2072 | $145,440 | 1,351 | 10 | $14,544 |
| 6805 | $139,695 | 754 | 7 | $19,956 |
| 6933 | $135,087 | 991 | 5 | $27,017 |
| 1084 | $129,443 | 797 | 9 | $14,383 |
| 1019 | $118,831 | 557 | 7 | $16,976 |
| 0865 | $114,346 | 1,283 | 22 | $5,198 |
| 0806 | $110,741 | 1,251 | 8 | $13,843 |
| 0508 | $101,885 | 914 | 19 | $5,362 |

### Q-42_results.md

# Q-42 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 65
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| 0314 | 6 | $0 | 0 | $0 |
| 0804 | 6 | $0 | 0 | $0 |
| 0806 | 12 | $0 | 0 | $0 |
| 0809 | 10 | $0 | 0 | $0 |
| 0815 | 3 | $0 | 0 | $0 |
| 0838 | 1 | $0 | 0 | $0 |
| 0877 | 5 | $0 | 0 | $0 |
| 0883 | 7 | $0 | 0 | $0 |
| 0890 | 6 | $0 | 0 | $0 |
| 1067 | 2 | $0 | 0 | $0 |
| 1088 | 6 | $0 | 0 | $0 |
| 1094 | 2 | $0 | 0 | $0 |
| 1468 | 4 | $0 | 0 | $0 |
| 1555 | 2 | $0 | 0 | $0 |
| 1768 | 6 | $0 | 0 | $0 |
| 1816 | 5 | $0 | 0 | $0 |
| 2173 | 10 | $0 | 0 | $0 |
| 2253 | 4 | $0 | 0 | $0 |
| 2351 | 4 | $0 | 0 | $0 |
| 2419 | 8 | $0 | 0 | $0 |
| 3000 | 4 | $0 | 0 | $0 |
| 3094 | 18 | $0 | 0 | $0 |
| 3133 | 17 | $0 | 0 | $0 |
| 3160 | 5 | $0 | 0 | $0 |
| 3164 | 17 | $0 | 0 | $0 |
| 3306 | 60 | $0 | 0 | $0 |
| 3318 | 3 | $0 | 0 | $0 |
| 3602 | 323 | $0 | 0 | $0 |
| 3604 | 79 | $0 | 0 | $0 |
| 3610 | 6 | $0 | 0 | $0 |
| 3632 | 5 | $0 | 0 | $0 |
| 3882 | 9 | $0 | 0 | $0 |
| 3988 | 8 | $0 | 0 | $0 |
| 4017 | 3 | $0 | 0 | $0 |
| 4072 | 3 | $0 | 0 | $0 |
| 4285 | 3 | $0 | 0 | $0 |
| 4502 | 1 | $0 | 0 | $0 |
| 4503 | 6 | $0 | 0 | $0 |
| 4741 | 9 | $0 | 0 | $0 |
| 4962 | 2 | $0 | 0 | $0 |
| 4963 | 2 | $0 | 0 | $0 |
| 5028 | 5 | $0 | 0 | $0 |
| 5096 | 12 | $0 | 0 | $0 |
| 5460 | 24 | $0 | 0 | $0 |
| 5461 | 6 | $0 | 0 | $0 |
| 5462 | 3 | $0 | 0 | $0 |
| 5590 | 3 | $0 | 0 | $0 |
| 5623 | 4 | $0 | 0 | $0 |
| 6007 | 6 | $0 | 0 | $0 |
| 6068 | 6 | $0 | 0 | $0 |
| 6072 | 1 | $0 | 0 | $0 |
| 6300 | 2 | $0 | 0 | $0 |
| 6400 | 20 | $0 | 0 | $0 |
| 6802 | 5 | $0 | 0 | $0 |
| 6884 | 4 | $0 | 0 | $0 |
| 6950 | 15 | $0 | 0 | $0 |
| 6952 | 6 | $0 | 0 | $0 |
| 6954 | 4 | $0 | 0 | $0 |
| 7365 | 12 | $0 | 0 | $0 |
| 7916 | 6 | $0 | 0 | $0 |
| 8046 | 3 | $0 | 0 | $0 |
| 8801 | 1 | $0 | 0 | $0 |
| 9013 | 4 | $0 | 0 | $0 |
| 9518 | 8 | $0 | 0 | $0 |
| 9608 | 4 | $0 | 0 | $0 |

### Q-59_results.md

# Q-59 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORG_SUMMARY | — | — | — | 92.90 | 1,434 | — | — | — | — | — | — |

### Q-61_results.md

# Q-61 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3164-6 BCB-HWG | Yep by Golden Lighting Aenon 6-light Chandelier in Brushed Champagne Brass | CHANDELIER | 31 | 40 | 11,928.80 | 35 | 310 |
| 3164-3SF BCB-HWG | Yep by Golden Lighting Aenon 3-light Semi-Flush Mount in Brushed Champagne Brass | SEMI-FLUSH MOUNT | 32 | 36 | 7,186 | 33 | 200 |
| 3164-6 PW-HWG | Yep by Golden Lighting Aenon 6-light Chandelier in Pewter | CHANDELIER | 17 | 22 | 6,000 | 20 | 300 |
| 3164-3SF BLK-HWG | Yep by Golden Lighting Aenon 3-light Semi-Flush Mount in Matte Black | SEMI-FLUSH MOUNT | 19 | 26 | 4,957.10 | 20 | 190 |
| 3988-18 DWA | Golden Lighting Conique 2-light Pendant in Dark Walnut | PENDANT | 7 | 21 | 4,800 | 10 | 300 |
| 3164-3SF PW-HWG | Yep by Golden Lighting Aenon 3-light Semi-Flush Mount in Pewter | SEMI-FLUSH MOUNT | 13 | 25 | 4,750 | 16 | 190 |
| 3164-LP BCB-HWG | Yep by Golden Lighting Aenon 3-light Island Light in Brushed Champagne Brass | ISLAND LIGHT | 15 | 15 | 4,635 | 15 | 300 |
| 0838-8 VS | Golden Lighting Finley 8-light Chandelier in Vintage Sage | CHANDELIER | 6 | 10 | 4,466 | 10 | 440 |
| 3000-5P NB-MAW | Wry Lighting Weavelight 5-light Pendant in Natural Black | PENDANT | 15 | 18 | 4,068 | 15 | 226 |
| 6884-22 TQ | Ziva by Golden Lighting Corallo Integrated LED 22in Chandelier in Turquoise | CHANDELIER | 5 | 5 | 3,960 | 5 | 990 |
| 3882-39 RG BL-CL | Yep by Golden Lighting Colorella LED Wall Sconce in Rose Gold with Blue and Clear Glass | WALL SCONCE | 2 | 9 | 3,850 | 3 | 149 |
| 1468-L BCH | Ziva by Golden Lighting Aurora Integrated LED 71"H Pendant in Brushed Champagne | PENDANT | 1 | 1 | 3,850 | 1 | 3,850 |
| 1768-LP PS-HWG | Golden Lighting Ciara 6-light Island Light in Peruvian Silver | ISLAND LIGHT | 7 | 13 | 3,810 | 11 | 300 |
| 1768-LP BLK-HWG | Golden Lighting Ciara 6-light Island Light in Matte Black | ISLAND LIGHT | 13 | 14 | 3,606.40 | 14 | 280 |
| 6884-30 TQ | Ziva by Golden Lighting Corallo Integrated LED 30in Chandelier in Turquoise | CHANDELIER | 3 | 3 | 3,437.50 | 3 | 1,375 |
| 3164-6SF BCB-HWG | Yep by Golden Lighting Aenon 6-light Semi-Flush Mount in Brushed Champagne Brass | SEMI-FLUSH MOUNT | 10 | 11 | 3,394.50 | 11 | 310 |
| 5461-32-26-18 SSG | Golden Lighting Lucerna Integrated LED 3-tier Chandelier in Stainless Steel Gold | CHANDELIER | 2 | 2 | 3,300 | 2 | 1,650 |
| 0890-LP ABI | Golden Lighting Alcott 8-light Island Light in Antique Black Iron | ISLAND LIGHT | 9 | 10 | 3,281.85 | 10 | 330 |
| 5590-OWL36 BLK | Golden Lighting Rodara Integrated LED 36in Outdoor Wall in Matte Black | OUTDOOR WALL | 4 | 21 | 3,258.75 | 4 | 165 |
| 3164-3 BLK-HWG | Yep by Golden Lighting Aenon 3-light Chandelier in Matte Black | CHANDELIER | 14 | 17 | 3,230 | 15 | 190 |
| 6068-8 BCB | Golden Lighting Marco 8-light Chandelier in Brushed Champagne Brass | CHANDELIER | 7 | 8 | 3,080 | 8 | 385 |
| 1768-LP WG-HWG | Golden Lighting Ciara 6-light Island Light in White Gold | ISLAND LIGHT | 8 | 11 | 2,820 | 11 | 300 |
| 4072-OWL36 SNB | Golden Lighting Obsidian Integrated LED 35in Outdoor Wall in Sand Black | OUTDOOR WALL | 4 | 20 | 2,800 | 4 | 140 |
| 6884-30 CR | Ziva by Golden Lighting Corallo Integrated LED 30in Chandelier in Coral | CHANDELIER | 2 | 2 | 2,750 | 2 | 1,375 |
| 0804-6P ABI | Golden Lighting Abingdon 6-light Pendant in Antique Black Iron | PENDANT | 8 | 9 | 2,691 | 8 | 299 |
| 6954-BA2 BCB-OP | Golden Lighting Dorinda 2-light Vanity in Brushed Champagne Brass | VANITY | 17 | 26 | 2,667 | 19 | 105 |
| 4072-OWL24 SNB | Golden Lighting Obsidian Integrated LED 24in Outdoor Wall in Sand Black | OUTDOOR WALL | 6 | 24 | 2,640 | 6 | 110 |
| 3164-3 BCB-HWG | Yep by Golden Lighting Aenon 3-light Chandelier in Brushed Champagne Brass | CHANDELIER | 11 | 13 | 2,600 | 11 | 200 |
| 4017-17 SNY | Golden Lighting Tela Integrated LED 18in Pendant in Sand Yellow | PENDANT | 2 | 3 | 2,475 | 2 | 825 |
| 5460-59 SNB | Golden Lighting Veritas Integrated LED 59in Chandelier in Sand Black | CHANDELIER | 3 | 4 | 2,452.45 | 3 | 715 |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | customer_count | total_revenue | total_units | status |
| --- | --- | --- | --- | --- |
| 2073-LP GMT | 77 | 60,181.37 | 284 | GHOST — no catalog record |
| 6070-BA3 BLK-PW | 51 | 28,496.56 | 325 | GHOST — no catalog record |
| 1323-6 WG | 44 | 24,512.86 | 99 | GHOST — no catalog record |
| 6070-LP BLK-PW | 40 | 23,423.59 | 116 | GHOST — no catalog record |
| 1323-9 WG | 35 | 21,982.57 | 63 | GHOST — no catalog record |
| 4309-LP BLK-SD | 36 | 18,396.22 | 62 | GHOST — no catalog record |
| 4309-LP BLK-AB-SD | 39 | 18,316.88 | 65 | GHOST — no catalog record |
| 1993-5 PS | 39 | 18,312.48 | 58 | GHOST — no catalog record |
| 2073-LP WG-CLR | 50 | 17,612.45 | 85 | GHOST — no catalog record |
| 1096-M BLK-SD | 26 | 16,913.51 | 143 | GHOST — no catalog record |
| 6070-BA3 BLK-AB | 56 | 16,237.45 | 184 | GHOST — no catalog record |
| 9905-8P RBZ | 50 | 15,330.97 | 60 | GHOST — no catalog record |
| 3184-LP NB-RO | 49 | 15,152.49 | 66 | GHOST — no catalog record |
| 1323-3P WG | 47 | 15,048.74 | 99 | GHOST — no catalog record |
| 6070-SF BLK-PW | 61 | 14,665.28 | 143 | GHOST — no catalog record |
| 0511-BA3 BLK-CLR | 46 | 14,559.53 | 133 | GHOST — no catalog record |
| 6070-SF BLK-AB | 61 | 14,221.52 | 143 | GHOST — no catalog record |
| 4309-BA3 BLK-SD | 36 | 13,893.86 | 132 | GHOST — no catalog record |
| 3167-LP PW | 18 | 13,593.67 | 59 | GHOST — no catalog record |
| 2073-6 GMT | 30 | 13,355.41 | 47 | GHOST — no catalog record |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9903-24 MG | Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Mystic Gold | 9903 | 79,467.93 | 24 | — | 2026-10-04 | [{'customer': 'INLINE ELECTRIC #11 / ATHENS', 'revenue': 11248.5}, {'customer': 'MAPLE RIDGE LIGHTING', 'revenue': 7678.8}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 3749.5}, {'customer': 'BOWLING GREEN WINLECTRIC', 'revenue': 3199.5}, {'customer': 'CAPE ELECTRICAL SUPPLY / CAPE GIRARDEAU', 'revenue': 3199.5}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 3199.5}, {'customer': 'ELLEN LIGHTING/ STAFFORD', 'revenue': 3199.5}, {'customer': 'ELUME DISTINCTIVE LIGHTING', 'revenue': 3199.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 3199.5}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 3199.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 3199.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 3199.5}, {'customer': 'KENDALL ELECTRIC', 'revenue': 3199.5}, {'customer': 'LIGHTING EXPO / FREEHOLD', 'revenue': 3199.5}, {'customer': 'LIGHTING AND BULBS UNLIMITED', 'revenue': 3199.5}, {'customer': 'LISA PLATT DESIGNS', 'revenue': 3199.5}, {'customer': 'TEXAS BRIGHT IDEAS/ HARKER HEIGHTS', 'revenue': 3199.5}, {'customer': 'ARIZONA LIGHTING / MESA', 'revenue': 3199.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 3199.5}, {'customer': None, 'revenue': 3199.5}, {'customer': 'LINDAS DESIGN dba CASA DE DECOR', 'revenue': 2399.63}] | [{'item': '9903-WSC MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 2-light Wall Sconce in Mystic Gold', 'available': 34}, {'item': '9903-6 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Black Iron', 'available': 24}, {'item': '9903-24 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Black Iron', 'available': 10}, {'item': '9903-18 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Black Iron', 'available': 7}, {'item': '9903-18 MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Mystic Gold', 'available': 5}, {'item': '9903-12 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Black Iron', 'available': 2}] |
| 3118-L BLK-SD | Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Seeded Glass | 3118 | 74,995.93 | 818 | — | 2026-08-06 | [{'customer': None, 'revenue': 11688.75}, {'customer': 'VILLA LIGHTING', 'revenue': 11225.89}, {'customer': 'STEADFAST LIGHTING - SPRINGDALE, AR', 'revenue': 4885.51}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 2569.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 2493.75}, {'customer': 'Southside Lighting Gallery', 'revenue': 2314.02}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 2216.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 2014.89}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 1437.43}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 1379.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 1137.0}, {'customer': 'KINGSTON LIGHTING AKA MCCAFFERTY NEIL B ELECTRIC COMPANY LTD', 'revenue': 1070.73}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 814.76}, {'customer': 'JUST LIGHTS  INC', 'revenue': 675.5}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 661.5}, {'customer': 'COSHOCTON LUMBER COMPANY', 'revenue': 567.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 557.0}, {'customer': 'Better Living Store', 'revenue': 537.0}, {'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 513.26}, {'customer': 'BUTLER LIGHTING/HIGH POINT', 'revenue': 462.5}, {'customer': 'ELEKTRA LIGHTS & FANS', 'revenue': 462.5}, {'customer': 'FERGUSON ENTERPRISES / 2715/ 226/ 228 / OMAHA', 'revenue': 462.5}, {'customer': 'THE LIGHTING SHOPPE/ CAMBRIDGE', 'revenue': 447.76}, {'customer': 'FERGUSON ENTERPRISES #118/ MURFREESBORO', 'revenue': 398.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 398.0}, {'customer': 'Ferguson Enterprises #3131/ St. George', 'revenue': 391.0}, {'customer': 'FERGUSON #2657 / BOWLING GREEN', 'revenue': 384.0}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 378.0}, {'customer': 'Ferguson Enterprises #951 / #952 Indianapolis', 'revenue': 378.0}, {'customer': 'ONE SOURCE LIGHTING / BILLINGS', 'revenue': 377.0}, {'customer': 'LIGHTING UNLIMITED/ COLUMBUS', 'revenue': 370.0}, {'customer': None, 'revenue': 370.0}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 368.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 368.0}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 367.0}, {'customer': 'GEORGIAN LIGHTING GALLERY INC', 'revenue': 358.0}, {'customer': 'Plumbing Distributors Inc / Lawrenceville', 'revenue': 328.26}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 312.18}, {'customer': 'KBL DESIGN CENTER INC/ PEORIA', 'revenue': 298.5}, {'customer': 'N.E.O. ELECTRICAL SUPPLY COMPANY', 'revenue': 298.5}, {'customer': 'PIONEER LIGHTING INC.', 'revenue': 298.5}, {'customer': 'ILLUMINATIONS/McALLEN', 'revenue': 298.5}, {'customer': 'LIGHT BRITE/ TRENTON', 'revenue': 298.5}, {'customer': 'Ferguson Enterprises / Corpus Christi', 'revenue': 283.5}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 277.5}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 277.5}, {'customer': 'US 31 SUPPLY', 'revenue': 277.5}, {'customer': 'US ELECTRICAL SERVICES DBA YALE ELECTRIC SUPPLY / WEST CHEST', 'revenue': 277.5}, {'customer': 'LDB HOLDINGS LLC, dba CW FLOORS & LIGHTING / DENTON', 'revenue': 277.5}, {'customer': 'KENDALL ELECTRIC INC / FORT WAYNE', 'revenue': 277.5}, {'customer': 'FAN AND LIGHTING WORLD/ BOYNTON BEACH', 'revenue': 277.5}, {'customer': "HAGEN'S LIGHTING", 'revenue': 277.5}, {'customer': 'Echo Group Inc dba Echo Lighting Gallery', 'revenue': 277.5}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 277.5}, {'customer': 'VILLAGE MAYTAG DBA VILLAGE HOME STORES', 'revenue': 273.63}, {'customer': 'METRO APPLIANCES & MORE/OKL CITY', 'revenue': 273.5}, {'customer': 'AL ENTERPRISES dba VALUE LIGHTING, INC. / CARROLLTON', 'revenue': 268.5}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 268.5}, {'customer': 'CANDLELIGHT LIGHT & LOG/ SAGINAW', 'revenue': 268.5}, {'customer': 'LIGHTING ETC / N RICHLAND HILLS', 'revenue': 268.5}, {'customer': 'BLACK DIAMOND ACQUISITIONS  dba ALLOWAY LIGHTING CO', 'revenue': 268.5}, {'customer': 'PROGRESSIVE LIGHTING, INC', 'revenue': 268.5}, {'customer': 'LEBANON ELECTRIC SUPPLY, INC', 'revenue': 233.75}, {'customer': 'LIGHT SYSTEMS, INC.', 'revenue': 223.89}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 223.89}, {'customer': 'ROB AND NITA YOUNG LLC dba YOUNG & CO', 'revenue': 199.0}, {'customer': 'BILLOWS ELECTRIC SUPPLY/ BERLIN', 'revenue': 199.0}, {'customer': 'DEKKER LIGHTING', 'revenue': 199.0}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 199.0}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 199.0}, {'customer': 'FIXTURE THIS', 'revenue': 199.0}, {'customer': 'FERGUSON ENTERPRISES / SACRAMENTO #686', 'revenue': 199.0}, {'customer': 'FERGUSON ENTERPRISES / LOUISVILLE #185 #1168', 'revenue': 199.0}, {'customer': 'FANGIO / THE  FACTORY LIGHTING / FURNITURE / PATIO', 'revenue': 199.0}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 199.0}, {'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 199.0}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 199.0}, {'customer': 'KENDALL ELECTRIC / GRAND RAPIDS', 'revenue': 199.0}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 199.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 199.0}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 199.0}, {'customer': 'LIGHT SOURCE LIGHTING/ PLAINFIELD', 'revenue': 199.0}, {'customer': 'PACE LIGHTING', 'revenue': 199.0}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 199.0}, {'customer': 'SIERRA PLUMBING SUPPLY', 'revenue': 199.0}, {'customer': 'SHALLOTTE ELECTRIC', 'revenue': 199.0}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 199.0}, {'customer': 'WILSON LIGHTING/ CLAYTON', 'revenue': 199.0}, {'customer': 'DESIGNER LIGHTING & FAN / SHOWROOM', 'revenue': 189.0}, {'customer': 'WOLBERG ELECTRICAL SUPPLY/ SCHENECTADY/ALBANY WAREHOUSE', 'revenue': 189.0}, {'customer': 'The Lite House / Columbia', 'revenue': 189.0}, {'customer': 'SCOTTIES INTERIORS', 'revenue': 189.0}, {'customer': 'Raymond De Steiger/ Ray Lighting Center', 'revenue': 189.0}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 189.0}, {'customer': 'FERGUSON ENTERPRISES #1550/ ADDISON IL', 'revenue': 189.0}, {'customer': 'Kitchens & Bath By Briggs / Omaha', 'revenue': 185.0}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 185.0}, {'customer': 'House of Lights / Mayfield HTS', 'revenue': 185.0}, {'customer': 'THE PLUMBING WAREHOUSE - LCR / SHREVEPORT', 'revenue': 185.0}, {'customer': 'WINSUPPLY COOKEVILLE TN CO', 'revenue': 185.0}, {'customer': 'FERGUSON ENTERPRISES / BROOKSHIRE 2812', 'revenue': 185.0}, {'customer': 'FERGUSON ENTERPRISES / #12 NORFOLK', 'revenue': 185.0}, {'customer': 'FERGUSON ENTERPRISES #499/ CHARLOTTESVILLE', 'revenue': 185.0}, {'customer': 'ELLIOTT ELECTRIC SUPPLY / NACOGDOCHES', 'revenue': 185.0}, {'customer': 'Be The Light Designs LLC', 'revenue': 185.0}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 185.0}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 185.0}, {'customer': 'METRO ELECTRIC SUPPLY/ ST LOUIS/ BRENTWOOD', 'revenue': 179.56}, {'customer': 'FERGUSON ENTERPRISES #1196 / FRANKLIN MA', 'revenue': 179.0}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 179.0}, {'customer': 'PROSOURCE SUPPLY / EASLEY', 'revenue': 179.0}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 179.0}, {'customer': 'E S LIGHTING', 'revenue': 179.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 179.0}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 179.0}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 179.0}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 179.0}, {'customer': 'PROGRESSIVE LIGHTING INC #07 / LEE LIGHTING / DULUTH', 'revenue': 149.26}, {'customer': 'LIGHTING WORLD / STATEN ISLAND SHOWROOM', 'revenue': 99.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 99.5}, {'customer': None, 'revenue': 99.5}, {'customer': 'Distinctive Lighting / Bozeman', 'revenue': 99.5}, {'customer': 'BOWLING GREEN WINLECTRIC', 'revenue': 99.5}, {'customer': 'Stokes Electrical Supply Co, Inc.', 'revenue': 99.5}, {'customer': None, 'revenue': 99.5}, {'customer': 'WHS WHOLESALE dba COURTESY ELECTRIC WHOLESALE', 'revenue': 94.5}, {'customer': 'Trinity Home Center', 'revenue': 94.5}, {'customer': 'KIRBY RISK CORP/ LAFAYETTE', 'revenue': 92.5}, {'customer': 'PROGRESSIVE LIGHTING INC #05 / LEE LIGHTING / ROSWELL', 'revenue': 92.5}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': 92.5}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 74.63}, {'customer': 'SCHAEDLER YESCO/ HARRISBURG', 'revenue': 74.63}, {'customer': 'FERGUSON ENTERPRISES #43/ GREENVILLE SC', 'revenue': 47.25}, {'customer': 'PREMIER LIGHTING/ BAKERSFIELD', 'revenue': 46.25}] | [{'item': '3118-M1L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Opal Glass', 'available': 558}, {'item': '3118-M1L RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Seeded Glass', 'available': 144}, {'item': '3118-2SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 106}, {'item': '3118-M1L PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Seeded Glass', 'available': 105}, {'item': '3118-BA2 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Seeded Glass', 'available': 105}, {'item': '3118-BA3 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-BA3 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-L BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Opal Glass', 'available': 59}, {'item': '3118-BA2 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-2SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Opal Glass', 'available': 56}, {'item': '3118-BA3 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Opal Glass', 'available': 55}, {'item': '3118-BA3 CH-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Opal Glass', 'available': 55}, {'item': '3118-3SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 CH-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Chrome and Opal Glass', 'available': 54}, {'item': '3118-BA2 CH-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Opal Glass', 'available': 52}, {'item': '3118-BA2 PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Pewter', 'available': 42}, {'item': '3118-2SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Pewter', 'available': 42}, {'item': '3118-L BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Clear Glass', 'available': 32}, {'item': '3118-1SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-BA1 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-2SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 29}, {'item': '3118-BA2 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Seeded Glass', 'available': 29}, {'item': '3118-L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Chrome and Seeded Glass', 'available': 28}, {'item': '3118-SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 28}, {'item': '3118-SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 28}, {'item': '3118-3SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 27}, {'item': '3118-4SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Semi-Flush Mount in Matte Black', 'available': 26}, {'item': '3118-BA3 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Opal Glass', 'available': 26}, {'item': '3118-BA4 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Seeded Glass', 'available': 26}, {'item': '3118-BA4 CH-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Opal Glass', 'available': 24}, {'item': '3118-BA4 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA3 PW-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Pewter and Opal Glass', 'available': 23}, {'item': '3118-SF14 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14 in Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA4 PW-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Seeded Glass', 'available': 21}, {'item': '3118-BA3 BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Clear Glass', 'available': 21}, {'item': '3118-M1L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Opal Glass', 'available': 20}, {'item': '3118-BA4 CH-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Seeded Glass', 'available': 19}, {'item': '3118-BA4 PW-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Opal Glass', 'available': 19}, {'item': '3118-BA4 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Opal Glass', 'available': 18}, {'item': '3118-BA1 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA1 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA2 BCB-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Opal Glass', 'available': 13}, {'item': '3118-BA4 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Opal Glass', 'available': 12}, {'item': '3118-M1L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Chrome and Seeded Glass', 'available': 11}, {'item': '3118-1SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Pewter', 'available': 9}, {'item': '3118-BA1 PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Seeded Glass', 'available': 9}, {'item': '3118-BA1 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-3SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Chrome', 'available': 6}, {'item': '3118-BA3 CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Seeded Glass', 'available': 6}, {'item': '3118-1SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 5}, {'item': '3118-2SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Chrome', 'available': 2}, {'item': '3118-BA2 CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Seeded Glass', 'available': 2}, {'item': '3118-L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Opal Glass', 'available': 1}, {'item': '3118-SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 1}, {'item': '3118-2SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 1}, {'item': '3118-BA2 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Opal Glass', 'available': 1}] |
| 9903-12 MG | Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Mystic Gold | 9903 | 67,162.55 | 65 | — | 2026-10-04 | [{'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 4085.65}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 3268.5}, {'customer': 'ROYCE COLLECTION / REDFORD', 'revenue': 2339.0}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 2179.0}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ IRVING', 'revenue': 2179.0}, {'customer': 'JACOBSON ELECTRIC', 'revenue': 1634.25}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 1634.25}, {'customer': 'DREAM HOUSE FURNISHINGS', 'revenue': 1499.4}, {'customer': 'TARELI INC dba MI CASA LIGHTING & FANS', 'revenue': 1249.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 1249.5}, {'customer': 'Hortons Home Lighting / LaGrange', 'revenue': 1249.5}, {'customer': 'THE PLUMBING WAREHOUSE - LCR / SHREVEPORT', 'revenue': 1249.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 1249.5}, {'customer': 'SOURCE LIGHTING / KALISPELL', 'revenue': 1249.5}, {'customer': 'SUN LIGHTING INC/ TEMPE', 'revenue': 1249.5}, {'customer': 'DESIGNER LIGHTING & FAN / SHOWROOM', 'revenue': 1249.5}, {'customer': 'DESIGN LIGHTING/ SURREY', 'revenue': 1225.69}, {'customer': 'WHS WHOLESALE dba COURTESY ELECTRIC WHOLESALE', 'revenue': 1124.55}, {'customer': 'LIGHTING RESOURCE STUDIO', 'revenue': 1089.5}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 1089.5}, {'customer': 'LISA PLATT DESIGNS', 'revenue': 1089.5}, {'customer': 'LINDAS DESIGN dba CASA DE DECOR', 'revenue': 1089.5}, {'customer': 'Luxur Lighting / Cedar City', 'revenue': 1089.5}, {'customer': None, 'revenue': 1089.5}, {'customer': 'AMERICAN LIGHTING / JOHNSON CITY', 'revenue': 1089.5}, {'customer': None, 'revenue': 1089.5}, {'customer': 'CAPITOL LIGHTING/ HANOVER', 'revenue': 1089.5}, {'customer': 'DULLES ELECTRIC SUPPLY CORP / STERLING', 'revenue': 1089.5}, {'customer': 'DRIFTWOOD GALLERIES', 'revenue': 1089.5}, {'customer': 'EP LIGHTING LLC', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES #48/ WILMINGTON NC', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES #13/ KNOXVILLE', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES / BROOKSHIRE 2812', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES / #2790 PITTSBURGH', 'revenue': 1089.5}, {'customer': 'Georgia Lighting', 'revenue': 1089.5}, {'customer': 'PREMIER BATH LIGHTING & HARDWARE dba HERALD WHOLESALE', 'revenue': 1089.5}, {'customer': 'HOBRECHT LIGHTING', 'revenue': 1089.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 1089.5}, {'customer': 'KENDALL ELECTRIC', 'revenue': 1089.5}, {'customer': 'THE LITE COMPANY', 'revenue': 1089.5}, {'customer': 'PINE GROVE LIGHTING & ELECTRICAL SUPPLY', 'revenue': 1089.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 1089.5}, {'customer': 'RICHARDS LIGHTING/ HUNTSVILLE', 'revenue': 1089.5}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 1089.5}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 1013.24}, {'customer': 'LIGHTING FIRST/ NAPLES', 'revenue': 937.13}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 817.13}, {'customer': 'US 31 SUPPLY', 'revenue': 817.13}, {'customer': 'BRECHER LIGHTING / LEXINGTON', 'revenue': 817.13}, {'customer': 'AURORA LIGHTING COMPANY', 'revenue': 544.75}, {'customer': 'WAGE LIGHTING & DESIGN', 'revenue': 544.75}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 544.75}, {'customer': 'CAPITAL ELECTRIC / WILMINGTON', 'revenue': 544.75}] | [{'item': '9903-WSC MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 2-light Wall Sconce in Mystic Gold', 'available': 34}, {'item': '9903-6 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Black Iron', 'available': 24}, {'item': '9903-24 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Black Iron', 'available': 10}, {'item': '9903-18 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Black Iron', 'available': 7}, {'item': '9903-18 MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Mystic Gold', 'available': 5}, {'item': '9903-12 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Black Iron', 'available': 2}] |
| 7312-L BP | Golden Lighting Bartlett 2-light Pendant in Black Patina | 7312 | 58,825.44 | 617 | — | 2026-08-06 | [{'customer': None, 'revenue': 38360.05}, {'customer': 'WHITE STAR SUPPLY LLC / BRUNSWICK 2', 'revenue': 1776.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 1567.6}, {'customer': 'METRO APPLIANCES & MORE/OKL CITY', 'revenue': 1406.76}, {'customer': 'ROBINSON LIGHTING/ KELOWNA', 'revenue': 984.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': 886.28}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 783.76}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 746.5}, {'customer': 'TIDEWATER LIGHTING & DESIGN LLC', 'revenue': 627.0}, {'customer': 'SUNBELT LIGHTING LLC/ HATTIESBURG', 'revenue': 522.5}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 518.5}, {'customer': 'The Lighting Design Co / Layton', 'revenue': 422.0}, {'customer': 'KING ELECTRIC', 'revenue': 418.0}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 414.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 365.76}, {'customer': "HENSON'S CARPET ONE", 'revenue': 365.76}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 328.5}, {'customer': 'PSJM dba STERLING CARPET ONE / GRAND FORKS', 'revenue': 313.5}, {'customer': 'SUNBELT LIGHTING LLC / BILOXI', 'revenue': 313.5}, {'customer': 'IBS LIGHTING, LTD / THE COLONY', 'revenue': 313.5}, {'customer': None, 'revenue': 313.5}, {'customer': 'RACHELS LIGHTING / PANAMA CITY', 'revenue': 313.5}, {'customer': 'KIE SUPPLY CORP/ KENNEWICK', 'revenue': 311.5}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 311.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 307.5}, {'customer': 'CAPPADONNA OF AZ', 'revenue': 307.5}, {'customer': 'CAPITAL ELECTRIC SUPPLY / NORTH CHARLESTON', 'revenue': 235.14}, {'customer': 'HERMITAGE', 'revenue': 219.0}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 219.0}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 211.0}, {'customer': None, 'revenue': 209.0}, {'customer': 'ELLIOTT ELECTRIC SUPPLY / NACOGDOCHES', 'revenue': 209.0}, {'customer': 'Lyteworks', 'revenue': 209.0}, {'customer': 'The Lite House / Columbia', 'revenue': 209.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 209.0}, {'customer': 'CHAMPLAIN VALLEY ELECTRIC SUPPLY COMPANY, INC.', 'revenue': 209.0}, {'customer': 'LUMENAREA', 'revenue': 209.0}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 209.0}, {'customer': 'OAK HEART INTERIORS LLC', 'revenue': 209.0}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 209.0}, {'customer': 'LIGHTING INCORPORATED / AUSTIN, TX', 'revenue': 207.0}, {'customer': 'LIGHTING WORLD / STATEN ISLAND SHOWROOM', 'revenue': 205.0}, {'customer': 'CREGGER COMPANY / WEST COLUMBIA', 'revenue': 205.0}, {'customer': 'SUNBELT LIGHTING LLC / MADISON', 'revenue': 205.0}, {'customer': 'PLUMBING DISTRIBUTORS INC/ MCDONOUGH', 'revenue': 156.76}, {'customer': 'Lights on Banks', 'revenue': 123.19}, {'customer': 'MAPLE RIDGE LIGHTING', 'revenue': 123.0}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 105.5}, {'customer': 'APPLICO, LLC/ TUSCALOOSA', 'revenue': 104.5}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 104.5}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 104.5}, {'customer': 'CAPITAL ELECTRIC / BLUFFTON', 'revenue': 104.5}, {'customer': 'Brandon Lighting / MS', 'revenue': 104.5}, {'customer': 'Better Living Store', 'revenue': 104.5}, {'customer': 'AMERICAN LIGHTING / KNOXVILLE', 'revenue': 104.5}, {'customer': 'HINSDALE LIGHTING / WESTMONT', 'revenue': 104.5}, {'customer': "HAGEN'S LIGHTING", 'revenue': 102.5}, {'customer': 'SUNBELT LIGHTING LLC / LAFAYETTE', 'revenue': 102.5}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 102.5}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 78.38}] | [{'item': '7312-SF BP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Black Patina', 'available': 59}, {'item': '7312-S CP', 'desc': 'Golden Lighting Bartlett 1-light Pendant in Copper Patina', 'available': 52}, {'item': '7312-BA1 BP', 'desc': 'Golden Lighting Bartlett 1-light Vanity in Black Patina', 'available': 33}, {'item': '7312-SF FW', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in French White', 'available': 30}, {'item': '7312-SF CP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Copper Patina', 'available': 27}, {'item': '7312-BA1 FW', 'desc': 'Golden Lighting Bartlett 1-light Vanity in French White', 'available': 19}, {'item': '7312-FM CP', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in Copper Patina', 'available': 15}, {'item': '7312-L FW', 'desc': 'Golden Lighting Bartlett 2-light Pendant in French White', 'available': 11}, {'item': '7312-1W CP', 'desc': 'Golden Lighting Bartlett 1-light Wall Sconce in Copper Patina', 'available': 10}, {'item': '7312-FM FW', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in French White', 'available': 5}, {'item': '7312-BA3 FW', 'desc': 'Golden Lighting Bartlett 3-light Vanity in French White', 'available': 5}, {'item': '7312-BA2 FW', 'desc': 'Golden Lighting Bartlett 2-light Vanity in French White', 'available': 5}, {'item': '7312-BA3 CP', 'desc': 'Golden Lighting Bartlett 3-light Vanity in Copper Patina', 'available': 4}, {'item': '7312-FM16 BP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Black Patina', 'available': 3}, {'item': '7312-FM16 FW', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in French White', 'available': 3}, {'item': '7312-S FW', 'desc': 'Golden Lighting Bartlett 1-light Pendant in French White', 'available': 3}, {'item': '7312-BA2 BP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Black Patina', 'available': 2}, {'item': '7312-BA2 CP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Copper Patina', 'available': 2}, {'item': '7312-FM16 CP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Copper Patina', 'available': 1}] |
| 6805-6 BLK-NR | Golden Lighting Everly 6-light Chandelier in Matte Black and Natural Rattan shade | 6805 | 42,401.43 | 173 | — | 2026-07-13 | [{'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 2021.0}, {'customer': 'BEE RIDGE LIGHTING & DESIGN', 'revenue': 1791.5}, {'customer': 'LIGHTING & DESIGN BY J&K ELECTRIC SUPPLY CO', 'revenue': 1763.5}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 1716.23}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 1702.5}, {'customer': 'PC BUILDING MATERIALS dba PC HOME CENTER', 'revenue': 1575.0}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 1543.25}, {'customer': 'COASTAL LIGHTING SUPPLY/ WILMINGTON', 'revenue': 1468.0}, {'customer': 'THE LIGHTING STUDIO / SENOIA', 'revenue': 1312.5}, {'customer': 'ELEGANT LIGHTING /WEST SPRINGFIELD', 'revenue': 1027.0}, {'customer': 'ROB AND NITA YOUNG LLC dba YOUNG & CO', 'revenue': 1022.0}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 787.5}, {'customer': 'FERGUSON ENTERPRISES / RICHMOND 5', 'revenue': 787.5}, {'customer': 'Light Store USA', 'revenue': 764.5}, {'customer': 'DECORATIVE LIGHTING, INC.', 'revenue': 759.5}, {'customer': 'LIGHTING FIRST/ NAPLES', 'revenue': 738.26}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 736.5}, {'customer': 'LIGHTING CONCEPTS & DESIGN', 'revenue': 656.25}, {'customer': 'IMAGINE MORE SERVICE / NORTHERN LIGHTS', 'revenue': 525.0}, {'customer': 'Southern Lighting Gallery/ Augusta', 'revenue': 525.0}, {'customer': 'BRECHER LIGHTING / LOUISVILLE', 'revenue': 479.0}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 479.0}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 472.16}, {'customer': 'DESIGN LIGHTING/ SURREY', 'revenue': 315.0}, {'customer': 'ROYAUME LUMINAIRE/ SHERBROOKE', 'revenue': 295.32}, {'customer': 'Lights on Banks', 'revenue': 295.31}, {'customer': 'ROYAUME LUMINAIRE/ TERREBONNE', 'revenue': 291.36}, {'customer': 'JUST LIGHTS  INC', 'revenue': 262.5}, {'customer': 'BILLOWS ELECTRIC SUPPLY/ BERLIN', 'revenue': 262.5}, {'customer': 'CHICOINE INTERIORS', 'revenue': 262.5}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 262.5}, {'customer': 'CREATIVE LIGHTING/ ST. PAUL', 'revenue': 262.5}, {'customer': 'CREGGER COMPANY / WEST COLUMBIA', 'revenue': 262.5}, {'customer': 'Coffman Home Decor LLC', 'revenue': 262.5}, {'customer': 'COLONIAL ELECTRIC SUPPLY COMPANY / KING OF PRUSSIA', 'revenue': 262.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 262.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 262.5}, {'customer': 'EAST VALLEY FANS & BLINDS / MESA', 'revenue': 262.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 262.5}, {'customer': 'FLA LIGHTING INC. dba LIGHTING DEPOT', 'revenue': 262.5}, {'customer': 'FERGUSON ENTERPRISES #196/ TAMPA', 'revenue': 262.5}, {'customer': 'Ferguson Enterprises #1869 / Round Rock', 'revenue': 262.5}, {'customer': 'FLINZ HOLDINGS LLC dba THE GALLERY OF LIGHTS / LONGVIEW', 'revenue': 262.5}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 262.5}, {'customer': 'GREENBRIER LIGHTING/ CHESAPEAKE', 'revenue': 262.5}, {'customer': 'GREENBRIER LIGHTING dba GREENBRIER LIGHTING AT HILLTOP', 'revenue': 262.5}, {'customer': 'HILL COUNTRY HOME CENTER LLC / KERRVILLE', 'revenue': 262.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 262.5}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 262.5}, {'customer': 'KING ELECTRIC', 'revenue': 262.5}, {'customer': 'Lyteworks', 'revenue': 262.5}, {'customer': 'Lighting by Design / Exton', 'revenue': 262.5}, {'customer': 'LIGHTING UNLIMITED LLC dba LIGHTING ETC  / PANAMA CITY BEACH', 'revenue': 262.5}, {'customer': 'THE LIGHT CENTER/ FORT COLLINS', 'revenue': 262.5}, {'customer': 'LOWCOUNTRY LIGHTING STUDIO', 'revenue': 262.5}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 262.5}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 262.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 262.5}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ CHARLOTTE', 'revenue': 262.5}, {'customer': 'PREMIERE LIGHTING GALLERY/ BEAVERCREEK', 'revenue': 262.5}, {'customer': 'PINE GROVE LIGHTING & ELECTRICAL SUPPLY', 'revenue': 262.5}, {'customer': 'RANDOLPH LIGHTING', 'revenue': 262.5}, {'customer': 'TEXAS BRIGHT IDEAS/ GEORGETOWN', 'revenue': 262.5}, {'customer': 'REXEL USA/TECHE ELECTRIC/ LAFAYETTE', 'revenue': 262.5}, {'customer': 'LIGHTING FIRST OF FLORIDA/ BONITA SPG', 'revenue': 249.38}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 244.13}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 244.13}, {'customer': 'HOME LIGHTING/ MALVERN', 'revenue': 239.5}, {'customer': 'MOUNTAINLAND SUPPLY / OREM', 'revenue': 239.5}, {'customer': 'US 31 SUPPLY', 'revenue': 239.5}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 239.5}, {'customer': 'FERGUSON ENTERPRISES #1196 / FRANKLIN MA', 'revenue': 239.5}, {'customer': 'DULLES ELECTRIC SUPPLY CORP / STERLING', 'revenue': 239.5}, {'customer': 'BIGGINS LIGHTING', 'revenue': 239.5}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 239.5}, {'customer': 'The Lite House / Columbia', 'revenue': 239.5}, {'customer': 'SCOTTIES INTERIORS', 'revenue': 239.5}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 234.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 234.5}, {'customer': 'Filament, Inc / St Louis Park', 'revenue': 234.5}, {'customer': 'LEE SUPPLY CORP / INDIANAPOLIS', 'revenue': 234.5}, {'customer': "HILL'S LIGHTING/ BONITA SPRINGS", 'revenue': 234.5}, {'customer': 'CLEVELAND LIGHTING / LYNDHURST', 'revenue': 234.5}, {'customer': 'BURGESS LIGHTING / FORRESTVILLE', 'revenue': 234.5}, {'customer': 'Heritage Lighting', 'revenue': 234.5}, {'customer': 'ONE STOP LIGHTING / THOUSAND OAKS', 'revenue': 234.5}, {'customer': 'Bayside Electric Supply', 'revenue': 234.5}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 234.5}, {'customer': 'CRESCENT LIGHTING SUPPLY/KIRKLAND', 'revenue': 234.5}, {'customer': 'ILLUMINATING EXPRESSIONS / EVANSVILLE IN', 'revenue': 234.5}, {'customer': 'ROYAUME LUMINAIRE/ SAINTE-JULIE', 'revenue': 143.7}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 143.7}, {'customer': 'ABC CREATIONS, LLC  / LAREDO', 'revenue': 131.25}, {'customer': 'COLEY ELECTRIC/DOUGLAS', 'revenue': 119.75}, {'customer': 'Southern Lighting LLC', 'revenue': 119.75}] | [{'item': '6805-6SF BLK-MBR', 'desc': 'Golden Lighting Everly 6-light Semi-Flush Mount in Matte Black and Modern Black Rattan shade', 'available': 217}, {'item': '6805-6 BLK-MBR', 'desc': 'Golden Lighting Everly 6-light Chandelier in Matte Black and Modern Black Rattan shade', 'available': 158}, {'item': '6805-4 BLK-NR', 'desc': 'Golden Lighting Everly 4-light Pendant in Matte Black and Natural Rattan shade', 'available': 57}, {'item': '6805-4SF BLK-NR', 'desc': 'Golden Lighting Everly 4-light Semi-Flush Mount in Matte Black and Natural Rattan shade', 'available': 57}, {'item': '6805-4 BLK-MBR', 'desc': 'Golden Lighting Everly 4-light Pendant in Matte Black and Modern Black Rattan shade', 'available': 19}, {'item': '6805-4SF BLK-MBR', 'desc': 'Golden Lighting Everly 4-light Semi-Flush Mount in Matte Black and Modern Black Rattan shade', 'available': 19}] |
| 9903-6 MG | Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Mystic Gold | 9903 | 41,930.25 | 67 | — | 2026-07-20 | [{'customer': 'Concept Lighting Group / Oakville', 'revenue': 1621.69}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 1569.38}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 1395.0}, {'customer': 'TAP LIGHTING', 'revenue': 1395.0}, {'customer': 'LIGHTING AND BULBS UNLIMITED', 'revenue': 1395.0}, {'customer': 'SPOTLIGHT DESIGN CENTER', 'revenue': 1395.0}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 1297.36}, {'customer': 'THE LITE COMPANY', 'revenue': 1272.63}, {'customer': 'FINISHING TOUCHES', 'revenue': 1220.63}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 1116.0}, {'customer': 'BURGESS LIGHTING / FORRESTVILLE', 'revenue': 1046.26}, {'customer': 'THE LIGHTING WAREHOUSE/ RICHMOND', 'revenue': 899.4}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 871.88}, {'customer': 'KINGSTON LIGHTING AKA MCCAFFERTY NEIL B ELECTRIC COMPANY LTD', 'revenue': 784.69}, {'customer': 'Light Store USA', 'revenue': 749.5}, {'customer': None, 'revenue': 749.5}, {'customer': 'SHALLOTTE ELECTRIC', 'revenue': 749.5}, {'customer': 'WILSON LIGHTING/ OVERLAND PARK', 'revenue': 697.5}, {'customer': 'FERGUSON ENTERPRISES #13/ KNOXVILLE', 'revenue': 697.5}, {'customer': 'FERGUSON ENTERPRISES #107 / ALPHARETTA', 'revenue': 697.5}, {'customer': 'FERGUSON ENTERPRISES / BROOKSHIRE 2812', 'revenue': 697.5}, {'customer': 'HARRY HORN INC dba Arch Street Lighting', 'revenue': 697.5}, {'customer': 'INLINE ELECTRIC/ PELHAM', 'revenue': 697.5}, {'customer': 'LAMPS EXPO / LOS ANGELES', 'revenue': 697.5}, {'customer': 'LIGHTING EXPO / FREEHOLD', 'revenue': 697.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 697.5}, {'customer': 'LIGHTING PLUS / HOUSTON', 'revenue': 697.5}, {'customer': 'LIGHTING FIRST/ FORT MYERS', 'revenue': 697.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 697.5}, {'customer': 'PASSION LIGHTING', 'revenue': 697.5}, {'customer': 'PEMBA LIGHTING', 'revenue': 697.5}, {'customer': 'ROYCE COLLECTION / REDFORD', 'revenue': 697.5}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 697.5}, {'customer': 'UNIVERSAL LIGHTS/ STAFFORD', 'revenue': 697.5}, {'customer': 'WILSON LIGHTING OF NAPLES', 'revenue': 697.5}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 648.68}, {'customer': 'SISTERS LIGHTING dba ANTHOLOGY LIGHTING / TEXAS', 'revenue': 558.0}, {'customer': 'EUROPA INTERIORS AND GIFTS LLC', 'revenue': 558.0}, {'customer': 'LIGHTING FIRST OF FLORIDA/ BONITA SPG', 'revenue': 558.0}, {'customer': 'INTERSTATE SUPPLY, INC. / LAKE CITY', 'revenue': 558.0}, {'customer': 'Distinctive Lighting / Bozeman', 'revenue': 558.0}, {'customer': 'EDWARD JOY ELECTRIC, LLC', 'revenue': 558.0}, {'customer': 'Dupage Lighting Inc.', 'revenue': 558.0}, {'customer': 'FERGUSON ENTERPRISE #3031/ SPOKANE WA', 'revenue': 558.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 523.13}, {'customer': 'JUST LIGHTS  INC', 'revenue': 523.13}, {'customer': 'ONE STOP LIGHTING / THOUSAND OAKS', 'revenue': 523.13}, {'customer': 'HELEN PITEO INTERIORS LLC.', 'revenue': 523.13}, {'customer': 'KRELL LIGHTING', 'revenue': 523.13}, {'customer': 'Light N Leisure', 'revenue': 374.75}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 348.75}, {'customer': 'ELEKTRA LIGHTS & FANS', 'revenue': 348.75}, {'customer': 'JACOBSON ELECTRIC', 'revenue': 348.75}, {'customer': 'BURNS ELECTRIC INC', 'revenue': 348.75}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 348.75}] | [{'item': '9903-WSC MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 2-light Wall Sconce in Mystic Gold', 'available': 34}, {'item': '9903-6 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Black Iron', 'available': 24}, {'item': '9903-24 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Black Iron', 'available': 10}, {'item': '9903-18 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Black Iron', 'available': 7}, {'item': '9903-18 MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Mystic Gold', 'available': 5}, {'item': '9903-12 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Black Iron', 'available': 2}] |
| 6937-M BLK-NR | Golden Lighting Valentina 1-light Pendant in Matte Black | 6937 | 41,560.87 | 545 | — | 2026-07-13 | [{'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 17315.1}, {'customer': 'ONE SOURCE LIGHTING / BILLINGS', 'revenue': 3349.5}, {'customer': 'MATHES OF ALABAMA ELECTRIC SUPPLY CO., INC.', 'revenue': 1880.0}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 1108.0}, {'customer': 'FERGUSON ENTERPRISES #0088  / TULSA', 'revenue': 715.5}, {'customer': None, 'revenue': 643.95}, {'customer': 'FERGUSON ENTERPRISES #230/ OKLAHOMA CITY', 'revenue': 636.0}, {'customer': 'PRESTIGE LIGHTING AND DESIGN', 'revenue': 567.0}, {'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 420.5}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 407.5}, {'customer': 'FERGUSON ENTERPRISES #1020 / WEST ALLIS', 'revenue': 395.5}, {'customer': 'HYE LIGHTING CO.', 'revenue': 387.5}, {'customer': 'STEADFAST LIGHTING - SPRINGDALE, AR', 'revenue': 326.0}, {'customer': 'Lighting Emporium / Springdale', 'revenue': 318.0}, {'customer': 'APPLICO, LLC/ TUSCALOOSA', 'revenue': 318.0}, {'customer': 'WHITE STAR SUPPLY LLC / WAYCROSS 1', 'revenue': 310.0}, {'customer': 'WHITE STAR SUPPLY LLC / BRUNSWICK 2', 'revenue': 289.2}, {'customer': 'DECO LUMINAIRE INC. / TERREBONNE', 'revenue': 285.19}, {'customer': 'Lyteworks', 'revenue': 283.5}, {'customer': 'RANDOLPH LIGHTING', 'revenue': 283.5}, {'customer': 'FERGUSON ENTERPRISES #499/ CHARLOTTESVILLE', 'revenue': 283.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 255.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 244.5}, {'customer': 'RICHARDS LIGHTING/ HUNTSVILLE', 'revenue': 244.5}, {'customer': 'ONE STOP LIGHTING / THOUSAND OAKS', 'revenue': 244.5}, {'customer': 'FERGUSON ENTERPRISES #253/ PENSACOLA', 'revenue': 244.5}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 240.5}, {'customer': 'FERGUSON ENTERPRISE #3031/ SPOKANE WA', 'revenue': 238.5}, {'customer': 'FERGUSON / COLUMBUS OH 1589 2828', 'revenue': 238.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 238.5}, {'customer': 'NOVA LIGHTING dba HANSEN LIGHTING INC', 'revenue': 238.5}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 238.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 238.5}, {'customer': 'DOMINION ELECTRIC SUPPLY/ CHANTILLY', 'revenue': 238.5}, {'customer': 'LIGHTING CONCEPTS & DESIGN', 'revenue': 238.5}, {'customer': 'VENICE LIGHTING COMPANY/ NOKOMIS', 'revenue': 232.5}, {'customer': 'METRO APPLIANCES & MORE/OKL CITY', 'revenue': 232.5}, {'customer': 'UNIQUE LIGHTING/ SASKATOON', 'revenue': 212.62}, {'customer': 'ROBINSON LIGHTING/ KELOWNA', 'revenue': 212.62}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 198.75}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 195.75}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 189.0}, {'customer': 'HELSEL-JEPPERSON', 'revenue': 189.0}, {'customer': 'Illuminations Lighting Inc dba Illimunations', 'revenue': 189.0}, {'customer': 'Ferguson Enterprises #476 / Valleyview OH', 'revenue': 189.0}, {'customer': 'NORTH COAST ELECTRIC / KENT / AUBURN', 'revenue': 189.0}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 189.0}, {'customer': 'FLINZ HOLDINGS LLC dba THE GALLERY OF LIGHTS / LONGVIEW', 'revenue': 170.1}, {'customer': 'GREER LIGHTING CENTER', 'revenue': 163.0}, {'customer': "HILL'S LIGHTING/ BONITA SPRINGS", 'revenue': 163.0}, {'customer': 'FERGUSON ENTERPRISES #2635 / ENGLEWOOD', 'revenue': 163.0}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 163.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 159.0}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES /DES MOINES #522 / CLIVE#226', 'revenue': 159.0}, {'customer': 'Ferguson Enterprises #52/ Orlando', 'revenue': 159.0}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 159.0}, {'customer': 'LIGHTING CONNECTION / BUDA', 'revenue': 159.0}, {'customer': 'ARIZONA LIGHTING COMPANY/ YUMA', 'revenue': 159.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 159.0}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES / HOLLY SPRINGS 1723', 'revenue': 159.0}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 159.0}, {'customer': 'TOUCH OF CLASS', 'revenue': 159.0}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 155.0}, {'customer': 'AMERICAN LIGHTING / KNOXVILLE', 'revenue': 155.0}, {'customer': 'BLYTHE INTERIORS', 'revenue': 155.0}, {'customer': 'RACHELS LIGHTING / PANAMA CITY', 'revenue': 155.0}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 155.0}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 147.88}, {'customer': 'Royaume Luminaire / St. Basile', 'revenue': 127.14}, {'customer': 'SAVE MORE LIGHTING LTD', 'revenue': 97.8}, {'customer': 'Mountainhigh Designs Inc', 'revenue': 94.5}, {'customer': 'EAST VALLEY FANS & BLINDS / MESA', 'revenue': 94.5}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 93.62}, {'customer': 'ROYAUME LUMINAIRE/ SAINTE-JULIE', 'revenue': 93.62}, {'customer': 'ROYAUME LUMINAIRE/ TERREBONNE', 'revenue': 93.62}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 81.5}, {'customer': 'JUST LIGHTS  INC', 'revenue': 81.5}, {'customer': 'FERGUSON ENTERPRISES #3055 / IDAHO FALLS', 'revenue': 81.5}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 79.5}, {'customer': 'FLA LIGHTING INC. dba LIGHTING DEPOT', 'revenue': 79.5}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 79.5}, {'customer': 'FUSION LIGHT AND DESIGN dba IMAGE COMPLETE', 'revenue': 77.5}, {'customer': 'CED dba ALL-PHASE ELECTRIC', 'revenue': 77.5}, {'customer': None, 'revenue': 77.5}, {'customer': 'ROYAUME LUMINAIRE/ DRUMMONDVILLE', 'revenue': 44.72}, {'customer': 'ROYAUME LUMINAIRE/ TROIS RIVIERES', 'revenue': 44.72}, {'customer': 'ROYAUME LUMINAIRE/ SHERBROOKE', 'revenue': 44.72}, {'customer': 'SANDERS LIGHTING CO', 'revenue': 39.75}] | [{'item': '6937-4P BLK-NR', 'desc': 'Golden Lighting Valentina 4-light Pendant in Matte Black and Natural Raphia Rope shade', 'available': 1}] |
| 1270-13 BLK | Wry Lighting Morgon 2-light 13" Flush Mount in Matte Black and Opal Glass | 1270 | 41,544.30 | 1,010 | — | 2026-07-20 | [{'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 13507.0}, {'customer': 'AMC LIGHTING & DECOR/ RALEIGH', 'revenue': 5487.8}, {'customer': 'CLW', 'revenue': 2917.36}, {'customer': 'MCI INC dba  MCI LIGHTING ONE / WAITE PARK', 'revenue': 2719.5}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 2358.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 1444.5}, {'customer': 'EP LIGHTING LLC', 'revenue': 1190.0}, {'customer': 'VALLEY LIGHTS INC / FARGO', 'revenue': 1189.5}, {'customer': 'MCNALLY ELECTRIC', 'revenue': 870.0}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 825.5}, {'customer': 'FERGUSON ENTERPRISES / HOLLY SPRINGS 1723', 'revenue': 765.0}, {'customer': 'FERGUSON ENTERPRISES #16/ GREENSBORO', 'revenue': 722.5}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 554.5}, {'customer': 'FERGUSON ENTERPRISES #1550/ ADDISON IL', 'revenue': 445.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 437.0}, {'customer': 'URBAN LIGHTS', 'revenue': 425.0}, {'customer': 'METRO ELECTRIC SUPPLY/ ST LOUIS/ BRENTWOOD', 'revenue': 365.0}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 344.0}, {'customer': 'PRESTIGE LIGHTING/ LANSING', 'revenue': 343.1}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 301.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 285.0}, {'customer': 'INSIDE SOURCE, LLC/ FRISCO', 'revenue': 273.0}, {'customer': 'FERGUSON ENTERPRISES #34/ CHARLOTTE', 'revenue': 255.0}, {'customer': 'STARLIGHT LIGHTING CENTRE - DROP SHIP (US)', 'revenue': 222.5}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 222.5}, {'customer': 'GALAXIE LIGHTING dba LIGHTINGUTAH.COM', 'revenue': 222.5}, {'customer': 'LIGHT SOURCE LIGHTING/ PLAINFIELD', 'revenue': 218.5}, {'customer': 'JUST LIGHTS  INC', 'revenue': 216.5}, {'customer': 'BLANCS DE BLANCS 2021 INC', 'revenue': 185.23}, {'customer': 'CRESCENT LIGHTING SUPPLY/KIRKLAND', 'revenue': 178.0}, {'customer': 'FERGUSON ENTERPRISES #215 / LENEXA', 'revenue': 178.0}, {'customer': 'FERGUSON ENTERPRISES #2009-#1657 / GOLDEN VALLEY', 'revenue': 178.0}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 170.0}, {'customer': 'At Home Lighting / Home Lighting / Colorado Springs', 'revenue': 170.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 170.0}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 133.5}, {'customer': 'FERGUSON ENTERPRISES / 1599 2820 PITTSBURGH', 'revenue': 89.0}, {'customer': 'CREATIVE LIGHTING/ ST. PAUL', 'revenue': 89.0}, {'customer': 'CLEVELAND LIGHTING / LYNDHURST', 'revenue': 85.0}, {'customer': 'MADISON CREEK FURNISHINGS /  MISSOULA', 'revenue': 85.0}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 85.0}, {'customer': 'ADVANCE ELECTRIC INC/ GAYLORD', 'revenue': 85.0}, {'customer': 'SIGNATURE LIGHTING AND FANS', 'revenue': 51.0}, {'customer': 'THE ELECTRICAL & PLUMBING STORE / GLOUCESTER', 'revenue': 47.81}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 44.5}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 44.5}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 44.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 44.5}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 44.5}, {'customer': 'Raymond De Steiger/ Ray Lighting Center', 'revenue': 44.5}, {'customer': 'STUDIO H2O / PSC DISTRIBUTION / IOWA CITY', 'revenue': 42.5}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 42.5}, {'customer': 'Better Living Store', 'revenue': 42.5}, {'customer': 'BRIGHT IDEAS DBA HALEY LIGHTING', 'revenue': 42.5}] | [{'item': '1270-13 CH', 'desc': 'Wry Lighting Morgon 2-light Flush Mount in Chrome', 'available': 95}, {'item': '1270-09 BLK', 'desc': 'Wry Lighting Morgon 1-light Flush Mount in Matte Black', 'available': 57}, {'item': '1270-09 PW', 'desc': 'Wry Lighting Morgon 1-light Flush Mount in Pewter', 'available': 22}, {'item': '1270-11 PW', 'desc': 'Wry Lighting Morgon 2-light 11" Flush Mount in Pewter and Opal Glass', 'available': 20}] |
| 6950-L MBS | Golden Lighting Shepard 1-light Pendant in Modern Brass and Modern Brass shade | 6950 | 34,833.82 | 285 | — | 2026-07-20 | [{'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 1361.5}, {'customer': 'BRECHER LIGHTING / LOUISVILLE', 'revenue': 1311.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 1017.0}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 980.0}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 922.5}, {'customer': 'BRAZORIA COUNTY LIGHTING INC', 'revenue': 901.5}, {'customer': 'Springfield Electric Supply / Champaign', 'revenue': 871.5}, {'customer': 'RECLAIMED WAREHOUSE', 'revenue': 742.0}, {'customer': 'FERGUSON ENTERPRISES #61 EULESS & #66 LEWISVILLE', 'revenue': 687.5}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 687.5}, {'customer': 'PREMIER LIGHTING/ BAKERSFIELD', 'revenue': 679.5}, {'customer': 'LAMPS EXPO / LOS ANGELES', 'revenue': 647.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 612.5}, {'customer': 'RIVER CITIES LIGHTING', 'revenue': 550.0}, {'customer': 'The Lite House / Columbia', 'revenue': 520.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 518.0}, {'customer': 'FERGUSON ENTERPRISES / CHANTILLY #001', 'revenue': 504.0}, {'customer': 'SANDERS LIGHTING CO', 'revenue': 504.0}, {'customer': 'FERGUSON ENTERPRISES / RICHMOND 5', 'revenue': 497.0}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 490.0}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 443.25}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 435.75}, {'customer': "CAROL'S LIGHTING & FAN SHOP/ HUMBLE", 'revenue': 412.5}, {'customer': 'JOHN WARD INTERIORS AND GIFTS', 'revenue': 404.5}, {'customer': 'FERGUSON ENTERPRISES #1550/ ADDISON IL', 'revenue': 388.5}, {'customer': 'BRIGHT CITY LIGHTS', 'revenue': 388.5}, {'customer': 'BLACK DIAMOND ACQUISITIONS  dba ALLOWAY LIGHTING CO', 'revenue': 388.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 388.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 388.5}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 381.5}, {'customer': 'VILLAGE MAYTAG DBA VILLAGE HOME STORES', 'revenue': 374.5}, {'customer': 'NOVA LIGHTING dba HANSEN LIGHTING INC', 'revenue': 367.5}, {'customer': 'Hortons Home Lighting / LaGrange', 'revenue': 367.5}, {'customer': 'Bayside Electric Supply', 'revenue': 367.5}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 367.5}, {'customer': 'REXEL USA/TECHE ELECTRIC/ LAFAYETTE', 'revenue': 367.5}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 320.25}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 309.75}, {'customer': 'HOBRECHT LIGHTING', 'revenue': 275.0}, {'customer': None, 'revenue': 275.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': 275.0}, {'customer': 'BIGGINS LIGHTING', 'revenue': 275.0}, {'customer': 'LIGHTS OF OCONEE', 'revenue': 275.0}, {'customer': 'MAGNOLIA LIGHTING', 'revenue': 275.0}, {'customer': 'WASATCH LIGHTING INC', 'revenue': 275.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 275.0}, {'customer': 'TURN ON LIGHTING / RIO RANCHO', 'revenue': 259.0}, {'customer': 'COBURN SUPPLY COMPANY INC / #3 LAKE CHARLES', 'revenue': 259.0}, {'customer': 'FERGUSON ENTERPRISES / #12 NORFOLK', 'revenue': 259.0}, {'customer': 'MCMANUS COMPANY', 'revenue': 259.0}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 259.0}, {'customer': 'MARTINEZ PROPERTY GROUP LLC DBA ONE SOURCE LIGHTING', 'revenue': 259.0}, {'customer': 'Stokes Electrical Supply Co, Inc.', 'revenue': 259.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 252.0}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 245.0}, {'customer': 'SISTERS LIGHTING dba ANTHOLOGY LIGHTING / TEXAS', 'revenue': 245.0}, {'customer': 'LIGHTING SPECIALISTS / MIDVALE', 'revenue': 245.0}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 245.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 245.0}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 245.0}, {'customer': 'SUNBELT LIGHTING LLC / LAFAYETTE', 'revenue': 245.0}, {'customer': 'Ferguson Enterprises #1869 / Round Rock', 'revenue': 245.0}, {'customer': 'FERGUSON ENTERPRISES #118/ MURFREESBORO', 'revenue': 245.0}, {'customer': 'PROSOURCE SUPPLY / EASLEY', 'revenue': 245.0}, {'customer': 'FERGUSON ENTERPRISES / POMONA 603', 'revenue': 245.0}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 245.0}, {'customer': 'Legacy Lighting, LLC', 'revenue': 245.0}, {'customer': 'INLINE ELECTRIC #11 / ATHENS', 'revenue': 245.0}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 232.76}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 190.75}, {'customer': 'AUSTELL LIGHTING', 'revenue': 183.75}, {'customer': 'SAVE MORE LIGHTING LTD', 'revenue': 155.4}, {'customer': 'Mountainhigh Designs Inc', 'revenue': 155.4}, {'customer': 'SIGNATURE LIGHTING AND FANS', 'revenue': 137.81}, {'customer': 'WILSON LIGHTING/ OVERLAND PARK', 'revenue': 137.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 137.5}, {'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 137.5}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 137.5}, {'customer': 'NORTHERN LIGHTS UNLIMITED/ BELVIDERE', 'revenue': 137.5}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 129.5}, {'customer': 'WT LIGHTING', 'revenue': 129.5}, {'customer': 'THE PLUMBING WAREHOUSE - LCR / LAFAYETTE', 'revenue': 129.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 129.5}, {'customer': 'Ferguson Enterprises #540 / Baton Rouge', 'revenue': 129.5}, {'customer': 'TEAM ELECTRIC SUPPLY', 'revenue': 129.5}, {'customer': 'SMALL TOWN HOME & DECOR', 'revenue': 129.5}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 129.5}, {'customer': 'CREATIVE LIGHTING/ ST. PAUL', 'revenue': 129.5}, {'customer': 'HOME LIGHTING/ MALVERN', 'revenue': 129.5}, {'customer': 'WOLFE LIGHTING & ACCENTS / REXBURG', 'revenue': 129.5}, {'customer': 'STUDIO H2O / PSC DISTRIBUTION / IOWA CITY', 'revenue': 122.5}, {'customer': 'Ferguson Enterprises #52/ Orlando', 'revenue': 122.5}, {'customer': 'MATHES OF ALABAMA ELECTRIC SUPPLY CO., INC.', 'revenue': 122.5}, {'customer': 'ARMITAGE INTERIORS', 'revenue': 122.5}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 122.5}, {'customer': 'RANDOLPH LIGHTING', 'revenue': 122.5}, {'customer': 'BES LIGHTING/ RAPID CITY', 'revenue': 122.5}, {'customer': 'FINISHING TOUCHES', 'revenue': 122.5}, {'customer': 'ROYAUME LUMINAIRE/ TROIS RIVIERES', 'revenue': 77.7}, {'customer': 'TWIN BRIDGE LIGHTING', 'revenue': 72.84}, {'customer': 'STAGGS CARPETS & INTERIORS dba STAGGS INTERIORS', 'revenue': 68.91}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 68.75}, {'customer': 'LUMINAIRES LTD / WILLMAR', 'revenue': 68.75}, {'customer': None, 'revenue': 68.75}, {'customer': 'INLINE ELECTRIC / CHATTANOOGA #12', 'revenue': 68.75}, {'customer': 'CLIFTON AND COMPANY', 'revenue': 64.75}, {'customer': 'COLEY ELECTRIC/DOUGLAS', 'revenue': 64.75}, {'customer': "NANCY B'S HOUSE OF LIGHTS LLC / CHARLOTTESVILLE", 'revenue': 64.75}, {'customer': 'DEKKER LIGHTING', 'revenue': 64.75}, {'customer': 'MAYER ELECTRIC SUPPLY/ PELHAM', 'revenue': 64.75}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 61.25}, {'customer': 'PROSOURCE / GREENVILLE', 'revenue': 61.25}, {'customer': 'BURR RIDGE LIGHTING', 'revenue': 61.25}, {'customer': 'ILLUMINATE LIGHTING', 'revenue': 61.25}, {'customer': 'Coffman Home Decor LLC', 'revenue': 61.25}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 0.0}] | [{'item': '6950-1W MBS-WHT', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Matte White shade', 'available': 56}, {'item': '6950-1W MBS-BLK', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Matte Black shade', 'available': 56}, {'item': '6950-BA2 MBS-BLK', 'desc': 'Golden Lighting Shepard 2-light Vanity in Modern Brass and Matte Black shade', 'available': 39}, {'item': '6950-BA2 MBS-WHT', 'desc': 'Golden Lighting Shepard 2-light Vanity in Modern Brass and Matte White shade', 'available': 38}, {'item': '6950-FM MBS-WHT', 'desc': 'Golden Lighting Shepard 3-light Flush Mount in Modern Brass and Matte White shade', 'available': 38}, {'item': '6950-1W MBS-RC', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Russet Clay shade', 'available': 37}, {'item': '6950-L MBS-WHT', 'desc': 'Golden Lighting Shepard 1-light Pendant in Modern Brass and Matte White shade', 'available': 36}, {'item': '6950-L MBS-RC', 'desc': 'Golden Lighting Shepard 1-light Pendant in Modern Brass and Russet Clay shade', 'available': 34}, {'item': '6950-FM MBS-RC', 'desc': 'Golden Lighting Shepard 3-light Flush Mount in Modern Brass and Russet Clay shade', 'available': 32}, {'item': '6950-BA3 MBS-MBS', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Modern Brass shade', 'available': 24}, {'item': '6950-BA2 MBS-RC', 'desc': 'Golden Lighting Shepard 2-light Vanity in Modern Brass and Russet Clay shade', 'available': 19}, {'item': '6950-FM MBS-BLK', 'desc': 'Golden Lighting Shepard 3-light Flush Mount in Modern Brass and Matte Black shade', 'available': 13}, {'item': '6950-1W MBS-MBS', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Modern Brass shade', 'available': 9}, {'item': '6950-L MBS-BLK', 'desc': 'Golden Lighting Shepard 1-light Pendant in Modern Brass and Matte Black shade', 'available': 7}, {'item': '6950-BA3 MBS-WHT', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Matte White shade', 'available': 4}, {'item': '6950-BA3 MBS-BLK', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Matte Black shade', 'available': 3}, {'item': '6950-BA3 MBS-RC', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Russet Clay shade', 'available': 3}] |
| 7312-L CP | Golden Lighting Bartlett 2-light Pendant in Copper Patina | 7312 | 32,868.59 | 307 | — | 2026-07-20 | [{'customer': None, 'revenue': 15327.3}, {'customer': 'CITY LIGHTZ / ST CATHARINES', 'revenue': 2463.8}, {'customer': 'Gem Sales & Marketing / Joe Miotto', 'revenue': 1971.0}, {'customer': 'LIGHTING WORLD / STATEN ISLAND SHOWROOM', 'revenue': 1505.0}, {'customer': 'TEXAS BRIGHT IDEAS/ GEORGETOWN', 'revenue': 1290.0}, {'customer': 'THE ELECTRICAL & PLUMBING STORE / GLOUCESTER', 'revenue': 1075.52}, {'customer': 'Georgia Lighting', 'revenue': 541.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 444.0}, {'customer': 'NOVA LIGHTING dba HANSEN LIGHTING INC', 'revenue': 438.0}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 337.5}, {'customer': 'BRIGHT CITY LIGHTS', 'revenue': 337.5}, {'customer': 'Brandon Lighting / MS', 'revenue': 337.5}, {'customer': 'J & B SUPPLY INC / FORT SMITH', 'revenue': 337.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 337.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 328.5}, {'customer': 'CHAMPLAIN VALLEY ELECTRIC SUPPLY COMPANY, INC.', 'revenue': 328.5}, {'customer': None, 'revenue': 328.5}, {'customer': 'FERGUSON ENTERPRISES / #1334 JACKSONVILLE', 'revenue': 322.5}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 313.89}, {'customer': 'KINGSTON LIGHTING AKA MCCAFFERTY NEIL B ELECTRIC COMPANY LTD', 'revenue': 270.0}, {'customer': 'RICHARDSON LIGHTING/ SASKATOON', 'revenue': 246.38}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 246.38}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 225.0}, {'customer': 'SOUTHERN LIGHTING/WARNER ROBINS', 'revenue': 225.0}, {'customer': None, 'revenue': 225.0}, {'customer': None, 'revenue': 219.0}, {'customer': 'Cline-Holder Electric Supply, Inc / Elizabethton', 'revenue': 219.0}, {'customer': 'FERGUSON ENTERPRISES / #0245 / AUSTIN', 'revenue': 219.0}, {'customer': 'MCNALLY ELECTRIC', 'revenue': 219.0}, {'customer': 'PROGRESSIVE LIGHTING INC #05 / LEE LIGHTING / ROSWELL', 'revenue': 219.0}, {'customer': 'RIVER CITIES LIGHTING', 'revenue': 219.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 219.0}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 215.0}, {'customer': 'ELLEN LIGHTING/ STAFFORD', 'revenue': 215.0}, {'customer': 'ADVANCE ELECTRIC INC/ GAYLORD', 'revenue': 215.0}, {'customer': 'MAPLE RIDGE LIGHTING', 'revenue': 123.19}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 112.5}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 112.5}, {'customer': 'URBAN LIGHTS', 'revenue': 112.5}, {'customer': 'Home And Light Valdosta', 'revenue': 109.5}, {'customer': 'The Cabinet Corner, Inc', 'revenue': 107.5}, {'customer': 'RACHELS LIGHTING / PANAMA CITY', 'revenue': 107.5}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 102.13}] | [{'item': '7312-SF BP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Black Patina', 'available': 59}, {'item': '7312-S CP', 'desc': 'Golden Lighting Bartlett 1-light Pendant in Copper Patina', 'available': 52}, {'item': '7312-BA1 BP', 'desc': 'Golden Lighting Bartlett 1-light Vanity in Black Patina', 'available': 33}, {'item': '7312-SF FW', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in French White', 'available': 30}, {'item': '7312-SF CP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Copper Patina', 'available': 27}, {'item': '7312-BA1 FW', 'desc': 'Golden Lighting Bartlett 1-light Vanity in French White', 'available': 19}, {'item': '7312-FM CP', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in Copper Patina', 'available': 15}, {'item': '7312-L FW', 'desc': 'Golden Lighting Bartlett 2-light Pendant in French White', 'available': 11}, {'item': '7312-1W CP', 'desc': 'Golden Lighting Bartlett 1-light Wall Sconce in Copper Patina', 'available': 10}, {'item': '7312-FM FW', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in French White', 'available': 5}, {'item': '7312-BA3 FW', 'desc': 'Golden Lighting Bartlett 3-light Vanity in French White', 'available': 5}, {'item': '7312-BA2 FW', 'desc': 'Golden Lighting Bartlett 2-light Vanity in French White', 'available': 5}, {'item': '7312-BA3 CP', 'desc': 'Golden Lighting Bartlett 3-light Vanity in Copper Patina', 'available': 4}, {'item': '7312-FM16 BP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Black Patina', 'available': 3}, {'item': '7312-FM16 FW', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in French White', 'available': 3}, {'item': '7312-S FW', 'desc': 'Golden Lighting Bartlett 1-light Pendant in French White', 'available': 3}, {'item': '7312-BA2 BP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Black Patina', 'available': 2}, {'item': '7312-BA2 CP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Copper Patina', 'available': 2}, {'item': '7312-FM16 CP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Copper Patina', 'available': 1}] |
| 6070-LP BLK-BLK | Golden Lighting Tribeca 5-light Island Light in Matte Black | 6070 | 32,605.78 | 165 | — | 2026-08-06 | [{'customer': 'JUST LIGHTS  INC', 'revenue': 2382.0}, {'customer': 'FERGUSON ENTERPRISES / 2715/ 226/ 228 / OMAHA', 'revenue': 1767.5}, {'customer': 'Sunbelt Lighting LLC / Baton Rouge', 'revenue': 1529.0}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 1484.61}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 1153.0}, {'customer': 'ILLUMINATING EXPRESSIONS / EVANSVILLE IN', 'revenue': 838.0}, {'customer': 'MID-COUNTY LIGHTING SHOWROOM & ELECTRICAL SUPPLIES', 'revenue': 794.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 764.0}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 764.0}, {'customer': 'MAHLANDERS INC / SIOUX FALLS', 'revenue': 751.55}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 682.32}, {'customer': "PREMIER LIGHTING/ LEE'S SUMMIT", 'revenue': 628.5}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 606.5}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 606.5}, {'customer': 'BRIGHT IDEAS DBA HALEY LIGHTING', 'revenue': 598.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 584.5}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 584.5}, {'customer': 'WILSON LIGHTING/ OVERLAND PARK', 'revenue': 576.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 562.5}, {'customer': 'SIGNATURE LIGHTING AND FANS', 'revenue': 471.38}, {'customer': 'FERGUSON ENTERPRISES #1117/ SPRINGDALE', 'revenue': 419.0}, {'customer': 'ILLUMINATE LIGHTING', 'revenue': 397.0}, {'customer': 'PARAMONT-EO/ NEW LENOX', 'revenue': 397.0}, {'customer': 'DEALERS ELECTRICAL SUPPLY / GREENVILLE', 'revenue': 389.0}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 382.0}, {'customer': 'The Lighting Design Co / Layton', 'revenue': 382.0}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 382.0}, {'customer': 'LIGHTING ETC / N RICHLAND HILLS', 'revenue': 375.0}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 375.0}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 375.0}, {'customer': 'BRECHER LIGHTING / LEXINGTON', 'revenue': 375.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 375.0}, {'customer': 'SUPER-LITE LIGHTING LTD', 'revenue': 235.69}, {'customer': 'TWIN BRIDGE LIGHTING', 'revenue': 235.69}, {'customer': 'THE ELECTRICAL & PLUMBING STORE / GLOUCESTER', 'revenue': 210.94}, {'customer': 'RICHARDSON LIGHTING/ REGINA', 'revenue': 210.94}, {'customer': 'PACE LIGHTING', 'revenue': 209.5}, {'customer': 'COURT STREET LIGHTING', 'revenue': 209.5}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 209.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 209.5}, {'customer': 'KING ELECTRIC', 'revenue': 209.5}, {'customer': 'LIGHTING WORLD INC/OMAHA', 'revenue': 209.5}, {'customer': 'LIGHT BRITE/ TRENTON', 'revenue': 209.5}, {'customer': 'Luxur Lighting / Cedar City', 'revenue': 209.5}, {'customer': 'NORTHERN LIGHTS & FANS / LAS VEGAS', 'revenue': 209.5}, {'customer': 'TEXAS BRIGHT IDEAS/ GEORGETOWN', 'revenue': 209.5}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 209.5}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 199.03}, {'customer': 'COLONIAL ELECTRIC SUPPLY COMPANY / KING OF PRUSSIA', 'revenue': 194.5}, {'customer': 'CLEVELAND LIGHTING / LYNDHURST', 'revenue': 194.5}, {'customer': 'CARAVELLE LIGHTING', 'revenue': 194.5}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 194.5}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 194.5}, {'customer': 'MARTINEZ PROPERTY GROUP LLC DBA ONE SOURCE LIGHTING', 'revenue': 194.5}, {'customer': 'BRIGHT IDEAS dba THE LAMP SHOP', 'revenue': 194.5}, {'customer': 'FERGUSON ENTERPRISE #3031/ SPOKANE WA', 'revenue': 194.5}, {'customer': 'HOME LIGHTING/ MALVERN', 'revenue': 194.5}, {'customer': 'KENDALL ELECTRIC / GRAND RAPIDS', 'revenue': 194.5}, {'customer': 'FERGUSON ENTERPRISES #43/ GREENVILLE SC', 'revenue': 194.5}, {'customer': 'WT LIGHTING', 'revenue': 194.5}, {'customer': 'Home And Light Valdosta', 'revenue': 194.5}, {'customer': 'Heritage Lighting', 'revenue': 187.5}, {'customer': 'Tuthill Lighting Design', 'revenue': 187.5}, {'customer': 'BRICK + LINEN', 'revenue': 187.5}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 187.5}, {'customer': 'House of Lights / Mayfield HTS', 'revenue': 187.5}, {'customer': 'MAYNARDS ELECTRIC / ROCHESTER', 'revenue': 187.5}, {'customer': 'NAPLES BULB INC/ LIGHT BULBS UNLIMITED', 'revenue': 187.5}, {'customer': 'Georgia Lighting', 'revenue': 187.5}, {'customer': 'MINNESOTA LIGHTING', 'revenue': 187.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 187.5}, {'customer': 'FERGUSON ENTERPRISES #216/ WICHITA', 'revenue': 187.5}, {'customer': 'EAST VALLEY FANS & BLINDS / MESA', 'revenue': 187.5}, {'customer': 'ANZALONE ELECTRIC INC.', 'revenue': 187.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 187.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 187.5}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 187.5}, {'customer': 'TEXAS BRIGHT IDEAS/ HARKER HEIGHTS', 'revenue': 187.5}, {'customer': 'REXEL USA/TECHE ELECTRIC/ LAFAYETTE', 'revenue': 187.5}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 187.5}, {'customer': 'LIGHTING SHOWROOM', 'revenue': 187.5}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 178.13}] | [{'item': '6070-SF BLK-BLK', 'desc': 'Golden Lighting Tribeca 4-light Semi-Flush Mount in Matte Black', 'available': 361}, {'item': '6070-FM BLK-BLK', 'desc': 'Golden Lighting Tribeca 2-light Flush Mount in Matte Black', 'available': 224}, {'item': '6070-BA3 BLK-BLK', 'desc': 'Golden Lighting Tribeca 3-light Vanity in Matte Black', 'available': 116}, {'item': '6070-9 BLK-BLK', 'desc': 'Golden Lighting Tribeca 9-light Chandelier in Matte Black', 'available': 24}, {'item': '6070-4 BLK-BLK', 'desc': 'Golden Lighting Tribeca 4-light Pendant in Matte Black', 'available': 20}, {'item': '6070-4 BLK-PW', 'desc': 'Golden Lighting Tribeca 4-light Pendant in Matte Black and Pewter Accents', 'available': 17}, {'item': '6070-FM BLK-PW', 'desc': 'Golden Lighting Tribeca 2-light Flush Mount in Matte Black and Pewter Accents', 'available': 9}, {'item': '6070-1SF PW-PW', 'desc': 'Golden Lighting Tribeca 1-light Semi-Flush Mount in Pewter', 'available': 8}, {'item': '6070-BA2 BLK-BLK', 'desc': 'Golden Lighting Tribeca 2-light Vanity in Matte Black', 'available': 3}] |
| 1017-69 BLK | Golden Lighting Alastair 15-light 2-tier Chandelier (6+9) Matte Black | 1017 | 28,315 | 85 | — | 2026-07-20 | [{'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 1639.5}, {'customer': None, 'revenue': 1093.5}, {'customer': 'GW KEETER LIGHTING & HOME/ BENTON', 'revenue': 958.5}, {'customer': 'PIONEER LIGHTING INC.', 'revenue': 729.0}, {'customer': 'ASBURYS INC', 'revenue': 729.0}, {'customer': 'TOUCH OF CLASS', 'revenue': 729.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 684.0}, {'customer': 'URBAN LIGHTS', 'revenue': 684.0}, {'customer': 'KENDALL ELECTRIC INC / FORT WAYNE', 'revenue': 684.0}, {'customer': 'FERGUSON #2657 / BOWLING GREEN', 'revenue': 639.0}, {'customer': 'FERGUSON ENTERPRISES #13/ KNOXVILLE', 'revenue': 639.0}, {'customer': 'WOLBERG ELECTRICAL SUPPLY / SARATOGA SPRINGS', 'revenue': 639.0}, {'customer': 'ELEKTRA LIGHTS & FANS', 'revenue': 636.0}, {'customer': 'FERGUSON ENTERPRISES #484/ ODESSA TX', 'revenue': 636.0}, {'customer': 'Cline-Holder Electric Supply, Inc / Elizabethton', 'revenue': 633.0}, {'customer': 'AURA INTERIORS INC', 'revenue': 410.06}, {'customer': 'C & M DESIGNS LLC DBA THE MINT JULEP', 'revenue': 383.4}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 383.4}, {'customer': 'FIELDEN VENTURES, LLC dba SIMPLY FLOORS AND LIGHTS', 'revenue': 364.5}, {'customer': None, 'revenue': 364.5}, {'customer': "CAROL'S LIGHTING & FAN SHOP/ HUMBLE", 'revenue': 364.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES #3093/ FARGO', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES / RICHMOND 5', 'revenue': 364.5}, {'customer': 'Ferguson Enterprises / CLARKSVILLE 3699', 'revenue': 364.5}, {'customer': 'Home And Light Valdosta', 'revenue': 364.5}, {'customer': 'JUST LIGHTS  INC', 'revenue': 364.5}, {'customer': 'LIGHTING WORLD INC/OMAHA', 'revenue': 364.5}, {'customer': None, 'revenue': 364.5}, {'customer': 'MASTERS LIGHTING, INC.', 'revenue': 364.5}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ CHARLOTTE', 'revenue': 364.5}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 364.5}, {'customer': 'The Watt House LLC', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES #36 / GREENVILLE', 'revenue': 319.5}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES / FORT PAYNE 533', 'revenue': 319.5}, {'customer': 'Ferguson Enterprises / GRAND RAPIDS 945', 'revenue': 319.5}, {'customer': 'At Home Lighting / Home Lighting / Colorado Springs', 'revenue': 319.5}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 319.5}, {'customer': 'GATEWAY LIGHTING & DESIGN', 'revenue': 319.5}, {'customer': 'HOME LIGHTING & SUPPLY INC', 'revenue': 319.5}, {'customer': 'ILLUMINATIONS/McALLEN', 'revenue': 319.5}, {'customer': 'INLINE ELECTRIC/ AUBURN', 'revenue': 319.5}, {'customer': 'INLINE ELECTRIC / CHATTANOOGA #12', 'revenue': 319.5}, {'customer': 'TECHTRON PRODUCTS INC', 'revenue': 319.5}, {'customer': 'FERGUSON / COLUMBUS OH 1589 2828', 'revenue': 319.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 319.5}, {'customer': 'LIGHTING CONCEPTS / VALDOSTA', 'revenue': 319.5}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 319.5}, {'customer': 'CRESCENT LIGHTING SUPPLY/KIRKLAND', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES #75/ FOREST', 'revenue': 319.5}, {'customer': 'MANTECA LIGHTING', 'revenue': 319.5}, {'customer': 'VOWELL AND SONS INC.', 'revenue': 319.5}, {'customer': 'PROGRESSIVE LIGHTING, INC', 'revenue': 319.5}, {'customer': 'ARIZONA LIGHTING COMPANY/ YUMA', 'revenue': 319.5}, {'customer': 'PACE LIGHTING', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES /DES MOINES #522 / CLIVE#226', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES #1020 / WEST ALLIS', 'revenue': 319.5}, {'customer': "HAGEN'S LIGHTING", 'revenue': 316.5}, {'customer': 'FERGUSON ENTERPRISES #1130/ PHARR', 'revenue': 316.5}, {'customer': 'FERGUSON ENTERPRISES #34/ CHARLOTTE', 'revenue': 316.5}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 297.14}, {'customer': "MCGILL'S FURNITURE", 'revenue': 159.75}, {'customer': 'COLEY ELECTRIC/DOUGLAS', 'revenue': 159.75}] | [{'item': '1017-9 BLK', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte Black', 'available': 136}, {'item': '1017-3 BLK', 'desc': 'Golden Lighting Alastair 3-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-6 BLK', 'desc': 'Golden Lighting Alastair 6-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-9 WHT', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte White', 'available': 28}, {'item': '1017-39 BLK', 'desc': 'Golden Lighting Alastair 12-light Chandelier in Matte Black', 'available': 18}] |
| 1017-96 BLK | Golden Lighting Alastair 15-light 2-tier Chandelier (9+6) in Matte Black | 1017 | 28,247.94 | 92 | — | 2026-07-20 | [{'customer': 'Plumbing Distributors Inc / Lawrenceville', 'revenue': 1146.0}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 953.5}, {'customer': 'FERGUSON ENTERPRISES #215 / LENEXA', 'revenue': 920.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 859.5}, {'customer': 'TECHTRON PRODUCTS INC', 'revenue': 859.5}, {'customer': 'RECLAIMED WAREHOUSE', 'revenue': 695.0}, {'customer': 'Southern Lighting LLC', 'revenue': 695.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 674.0}, {'customer': 'AMERICAN LIGHTING / JOHNSON CITY', 'revenue': 653.0}, {'customer': 'SHANOR ELECTRIC SUPPLIES LLC / ORCHARD PARK', 'revenue': 634.0}, {'customer': 'DECORATIVE LIGHTING, INC.', 'revenue': 634.0}, {'customer': 'PARAMONT-EO/ NEW LENOX', 'revenue': 573.0}, {'customer': 'AURA INTERIORS INC', 'revenue': 391.8}, {'customer': 'FANGIO / THE  FACTORY LIGHTING / FURNITURE / PATIO', 'revenue': 347.5}, {'customer': 'Brandon Lighting / MS', 'revenue': 347.5}, {'customer': 'PEAK LIGHTING', 'revenue': 347.5}, {'customer': 'URBAN LIGHTS', 'revenue': 347.5}, {'customer': 'Southside Lighting Gallery', 'revenue': 347.5}, {'customer': 'ONE SOURCE LIGHTING / BILLINGS', 'revenue': 347.5}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 347.5}, {'customer': 'CAPPADONNA OF AZ', 'revenue': 347.5}, {'customer': 'Dupage Lighting Inc.', 'revenue': 347.5}, {'customer': 'GROVE SUPPLY INC / PHILADELPHIA', 'revenue': 347.5}, {'customer': 'Ferguson Enterprises #52/ Orlando', 'revenue': 347.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 347.5}, {'customer': 'FERGUSON ENTERPRISES #57/ OCALA', 'revenue': 347.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 347.5}, {'customer': 'STARLIGHT LIGHTING CENTRE', 'revenue': 343.8}, {'customer': 'AMERICAN LIGHTING / KNOXVILLE', 'revenue': 326.5}, {'customer': None, 'revenue': 326.5}, {'customer': 'LITE ART BY CAI DESIGNS', 'revenue': 326.5}, {'customer': 'AMERICAN LIGHTING / KINGSPORT', 'revenue': 326.5}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 326.5}, {'customer': 'Hortons Home Lighting / LaGrange', 'revenue': 326.5}, {'customer': 'Southern Lighting Gallery/ Augusta', 'revenue': 326.5}, {'customer': 'AUSTELL LIGHTING', 'revenue': 326.5}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 326.5}, {'customer': 'Lighting Emporium / Springdale', 'revenue': 326.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 326.5}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 319.5}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 319.5}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 286.5}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 286.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 286.5}, {'customer': 'Robinson Lighting Winnipeg - Cartier Lighting / Plymouth', 'revenue': 286.5}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 286.5}, {'customer': 'DEALERS ELECTRICAL SUPPLY/BRYAN', 'revenue': 286.5}, {'customer': 'FERGUSON ENTERPRISES #483/ AMARILLO TX', 'revenue': 286.5}, {'customer': 'FERGUSON ENTERPRISES #2009-#1657 / GOLDEN VALLEY', 'revenue': 286.5}, {'customer': 'Ferguson Enterprises #951 / #952 Indianapolis', 'revenue': 286.5}, {'customer': 'FERGUSON ENTERPRISES / BRYAN 1563', 'revenue': 286.5}, {'customer': None, 'revenue': 286.5}, {'customer': None, 'revenue': 286.5}, {'customer': 'GOOD FRIEND ELECTRIC', 'revenue': 286.5}, {'customer': 'GALAXIE LIGHTING dba LIGHTINGUTAH.COM', 'revenue': 286.5}, {'customer': 'IMAGINE MORE SERVICE / NORTHERN LIGHTS', 'revenue': 286.5}, {'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 286.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 286.5}, {'customer': 'LUMINAIRES LTD / WILLMAR', 'revenue': 286.5}, {'customer': 'LIGHTING INCORPORATED / HOUSTON, TX', 'revenue': 286.5}, {'customer': 'MAYER ELECTRIC SUPPLY / DOTHAN #172500', 'revenue': 286.5}, {'customer': 'PLUMBING DISTRIBUTORS INC/ WOODSTOCK', 'revenue': 286.5}, {'customer': 'PLUMBING DISTRIBUTORS INC / #021 NASHVILLE', 'revenue': 286.5}, {'customer': 'Raymond De Steiger/ Ray Lighting Center', 'revenue': 286.5}, {'customer': 'SIOUX FALLS LIGHTHOUSE, LLC', 'revenue': 286.5}, {'customer': 'TRI-SUPPLY CO / CONROE', 'revenue': 286.5}, {'customer': 'DANLAR INC dba LADE-DANLAR / TUCKER', 'revenue': 286.5}, {'customer': 'The Watt House LLC', 'revenue': 286.5}, {'customer': 'Wilson Lighting Co / Winston Salem', 'revenue': 286.5}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 286.5}, {'customer': "GRAHAM'S LIGHTING / FRANKLIN", 'revenue': 272.18}, {'customer': 'ROYAUME LUMINAIRE/ SHERBROOKE', 'revenue': 179.72}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 179.72}, {'customer': 'ROYAUME LUMINAIRE/ TERREBONNE', 'revenue': 179.72}] | [{'item': '1017-9 BLK', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte Black', 'available': 136}, {'item': '1017-3 BLK', 'desc': 'Golden Lighting Alastair 3-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-6 BLK', 'desc': 'Golden Lighting Alastair 6-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-9 WHT', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte White', 'available': 28}, {'item': '1017-39 BLK', 'desc': 'Golden Lighting Alastair 12-light Chandelier in Matte Black', 'available': 18}] |
| 3118-L PW-SD | Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Seeded Glass | 3118 | 27,818.76 | 298 | — | 2026-07-13 | [{'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 7545.31}, {'customer': None, 'revenue': 5526.95}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 2163.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 2028.0}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 1380.0}, {'customer': "Gerhard's Kitchen & Bath / First Supply LLC", 'revenue': 731.5}, {'customer': 'BUTLER LIGHTING/HIGH POINT', 'revenue': 563.0}, {'customer': 'ILLUMINATIONS/McALLEN', 'revenue': 555.0}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 468.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 368.0}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 313.5}, {'customer': "CAROL'S LIGHTING & FAN SHOP/ HUMBLE", 'revenue': 313.5}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 283.5}, {'customer': 'CAPITAL ELECTRIC / BLUFFTON', 'revenue': 277.5}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 268.5}, {'customer': 'LIGHTING FIRST OF FLORIDA/ BONITA SPG', 'revenue': 268.5}, {'customer': 'PREMIER LIGHTING/ BAKERSFIELD', 'revenue': 255.25}, {'customer': 'THE BROADWAY SHOWROOM', 'revenue': 209.0}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 209.0}, {'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 209.0}, {'customer': None, 'revenue': 209.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 209.0}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 209.0}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 209.0}, {'customer': 'HUDSON PARC LIGHTING AND DESIGN', 'revenue': 189.0}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 189.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 189.0}, {'customer': 'MATHES OF ALABAMA ELECTRIC SUPPLY CO., INC.', 'revenue': 189.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 185.0}, {'customer': 'LIGHTING PLUS / HOUSTON', 'revenue': 185.0}, {'customer': 'IBS LIGHTING, LTD / THE COLONY', 'revenue': 185.0}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 185.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 179.0}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 179.0}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 138.75}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 104.5}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 104.5}, {'customer': 'MAYER ELECTRIC SUPPLY / DOTHAN #172500', 'revenue': 94.5}, {'customer': 'Trinity Home Center', 'revenue': 94.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 94.5}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 94.5}, {'customer': 'BRECHER LIGHTING / LOUISVILLE', 'revenue': 94.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 94.5}, {'customer': 'MAYER ELECTRIC SUPPLY/ BIRMINGHAM #200', 'revenue': 92.5}, {'customer': 'LIGHTSTYLES / COSTA MESA / LUXE HOME STUDIO', 'revenue': 92.5}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 92.5}] | [{'item': '3118-M1L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Opal Glass', 'available': 558}, {'item': '3118-M1L RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Seeded Glass', 'available': 144}, {'item': '3118-2SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 106}, {'item': '3118-M1L PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Seeded Glass', 'available': 105}, {'item': '3118-BA2 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Seeded Glass', 'available': 105}, {'item': '3118-BA3 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-BA3 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-L BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Opal Glass', 'available': 59}, {'item': '3118-BA2 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-2SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Opal Glass', 'available': 56}, {'item': '3118-BA3 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Opal Glass', 'available': 55}, {'item': '3118-BA3 CH-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Opal Glass', 'available': 55}, {'item': '3118-3SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 CH-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Chrome and Opal Glass', 'available': 54}, {'item': '3118-BA2 CH-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Opal Glass', 'available': 52}, {'item': '3118-BA2 PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Pewter', 'available': 42}, {'item': '3118-2SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Pewter', 'available': 42}, {'item': '3118-L BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Clear Glass', 'available': 32}, {'item': '3118-1SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-BA1 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-2SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 29}, {'item': '3118-BA2 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Seeded Glass', 'available': 29}, {'item': '3118-L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Chrome and Seeded Glass', 'available': 28}, {'item': '3118-SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 28}, {'item': '3118-SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 28}, {'item': '3118-3SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 27}, {'item': '3118-4SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Semi-Flush Mount in Matte Black', 'available': 26}, {'item': '3118-BA3 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Opal Glass', 'available': 26}, {'item': '3118-BA4 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Seeded Glass', 'available': 26}, {'item': '3118-BA4 CH-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Opal Glass', 'available': 24}, {'item': '3118-BA4 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA3 PW-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Pewter and Opal Glass', 'available': 23}, {'item': '3118-SF14 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14 in Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA4 PW-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Seeded Glass', 'available': 21}, {'item': '3118-BA3 BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Clear Glass', 'available': 21}, {'item': '3118-M1L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Opal Glass', 'available': 20}, {'item': '3118-BA4 CH-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Seeded Glass', 'available': 19}, {'item': '3118-BA4 PW-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Opal Glass', 'available': 19}, {'item': '3118-BA4 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Opal Glass', 'available': 18}, {'item': '3118-BA1 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA1 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA2 BCB-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Opal Glass', 'available': 13}, {'item': '3118-BA4 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Opal Glass', 'available': 12}, {'item': '3118-M1L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Chrome and Seeded Glass', 'available': 11}, {'item': '3118-1SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Pewter', 'available': 9}, {'item': '3118-BA1 PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Seeded Glass', 'available': 9}, {'item': '3118-BA1 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-3SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Chrome', 'available': 6}, {'item': '3118-BA3 CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Seeded Glass', 'available': 6}, {'item': '3118-1SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 5}, {'item': '3118-2SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Chrome', 'available': 2}, {'item': '3118-BA2 CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Seeded Glass', 'available': 2}, {'item': '3118-L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Opal Glass', 'available': 1}, {'item': '3118-SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 1}, {'item': '3118-2SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 1}, {'item': '3118-BA2 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Opal Glass', 'available': 1}] |
| 8001-BA3 BLK-SD | Golden Lighting Parrish 3-light Vanity in Matte Black | 8001 | 25,628.13 | 346 | — | 2026-08-20 | [{'customer': 'ELLEN LIGHTING/ STAFFORD', 'revenue': 14063.55}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 833.0}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 678.83}, {'customer': 'HELSEL-JEPPERSON', 'revenue': 651.0}, {'customer': 'STEADFAST LIGHTING - SPRINGDALE, AR', 'revenue': 567.0}, {'customer': 'Home And Light Valdosta', 'revenue': 540.6}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 477.0}, {'customer': 'Plumbing Distributors Inc / Lawrenceville', 'revenue': 427.5}, {'customer': 'PIONEER LIGHTING INC.', 'revenue': 318.0}, {'customer': 'The Watt House LLC', 'revenue': 318.0}, {'customer': 'Robinson Lighting Winnipeg - Cartier Lighting / Plymouth', 'revenue': 318.0}, {'customer': 'FIXTURE THIS', 'revenue': 318.0}, {'customer': 'DECORATIVE LIGHTING, INC.', 'revenue': 298.15}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 286.2}, {'customer': 'COASTAL LIGHTING SUPPLY/ WILMINGTON', 'revenue': 283.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 278.26}, {'customer': 'LIGHTING CONCEPTS / VALDOSTA', 'revenue': 262.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 238.52}, {'customer': 'SUNBELT LIGHTING LLC #9 / BATESVILLE', 'revenue': 238.5}, {'customer': 'LISA LYNN DESIGNS / LOUISVILLE', 'revenue': 238.5}, {'customer': 'XPRESS LIGHTING OF TEXAS', 'revenue': 234.63}, {'customer': 'STAGGS CARPETS & INTERIORS dba STAGGS INTERIORS', 'revenue': 190.8}, {'customer': 'FERGUSON ENTERPRISES #107 / ALPHARETTA', 'revenue': 189.0}, {'customer': 'LIGHT SYSTEMS, INC.', 'revenue': 178.89}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 178.89}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 175.0}, {'customer': 'Stokes Electrical Supply Co, Inc.', 'revenue': 175.0}, {'customer': 'SHALLOTTE ELECTRIC', 'revenue': 175.0}, {'customer': 'ROB AND NITA YOUNG LLC dba YOUNG & CO', 'revenue': 159.0}, {'customer': None, 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES / #2790 PITTSBURGH', 'revenue': 159.0}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 159.0}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 159.0}, {'customer': 'LEE SUPPLY CORP / INDIANAPOLIS', 'revenue': 159.0}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 159.0}, {'customer': 'PROGRESSIVE LIGHTING, INC', 'revenue': 159.0}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ CHARLOTTE', 'revenue': 159.0}, {'customer': 'TEXAS BRIGHT IDEAS/ HARKER HEIGHTS', 'revenue': 159.0}, {'customer': 'SUNBELT LIGHTING LLC / BILOXI', 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES #215 / LENEXA', 'revenue': 127.2}, {'customer': 'ACCENT LIGHTING/ WICHITA', 'revenue': 119.26}, {'customer': 'KANSAS LIGHTING', 'revenue': 79.5}, {'customer': 'MINNESOTA LIGHTING', 'revenue': 79.5}, {'customer': 'Trinity Home Center', 'revenue': 79.5}, {'customer': 'NORTH COAST ELECTRIC / KENT / AUBURN', 'revenue': 79.5}, {'customer': 'THE LIGHTING STUDIO / SENOIA', 'revenue': 79.5}, {'customer': 'Valley Electric Supply / Ansonia', 'revenue': 63.6}, {'customer': 'CJ LIGHTING AND FANS', 'revenue': 39.75}] | [{'item': '8001-9 BLK-SD', 'desc': 'Golden Lighting Parrish 9-light Chandelier in Matte Black', 'available': 110}, {'item': '8001-BA2 BLK-SD', 'desc': 'Golden Lighting Parrish 2-light Vanity in Matte Black', 'available': 108}, {'item': '8001-BA2 RBZ-SD', 'desc': 'Golden Lighting Parrish 2-light Vanity in Rubbed Bronze', 'available': 29}, {'item': '8001-BA3 PW-SD', 'desc': 'Golden Lighting Parrish 3-light Vanity in Pewter', 'available': 18}] |
| 3118-L RBZ-SD | Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Seeded Glass | 3118 | 25,316.74 | 285 | — | 2026-07-13 | [{'customer': None, 'revenue': 6201.3}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 772.87}, {'customer': 'MAYER ELECTRIC SUPPLY/ BIRMINGHAM #200', 'revenue': 716.0}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 661.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 650.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 650.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 557.0}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 542.0}, {'customer': 'FERGUSON ENTERPRISES / #12 NORFOLK', 'revenue': 537.0}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 447.5}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 390.0}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 390.0}, {'customer': 'BUTLER LIGHTING/HIGH POINT', 'revenue': 384.0}, {'customer': 'KENDALL ELECTRIC INC / FORT WAYNE', 'revenue': 374.0}, {'customer': 'LIGHTING AND LAMP / PELHAM', 'revenue': 358.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 358.0}, {'customer': 'LIGHTING UNLIMITED/ COLUMBUS', 'revenue': 358.0}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 332.96}, {'customer': 'DESIGN LIGHTING/ SURREY', 'revenue': 322.2}, {'customer': 'SUPER-LITE LIGHTING LTD', 'revenue': 302.07}, {'customer': 'GREER LIGHTING CENTER', 'revenue': 292.5}, {'customer': 'FERGUSON ENTERPRISES / MANCHESTER 3356', 'revenue': 292.5}, {'customer': 'GW KEETER LIGHTING & HOME/ BENTON', 'revenue': 292.5}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 292.5}, {'customer': 'The Glows Works Inc dba The Lighting Gallery', 'revenue': 292.5}, {'customer': 'FERGUSON ENTERPRISES/ #190 SPRING', 'revenue': 292.5}, {'customer': 'PREMIER LIGHTING/ PHOENIX', 'revenue': 283.5}, {'customer': 'Southside Lighting Gallery', 'revenue': 268.5}, {'customer': 'Cregger Lighting Branch 11 / Bluffton', 'revenue': 268.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 268.5}, {'customer': 'FERGUSON ENTERPRISES #8/ ROANOKE', 'revenue': 268.5}, {'customer': 'FERGUSON ENTERPRISES #48/ WILMINGTON NC', 'revenue': 268.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 268.5}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 268.5}, {'customer': 'THE LAMPLIGHTER/ SPECTRUM LIGHTING', 'revenue': 268.5}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 268.5}, {'customer': 'At Home Lighting / Home Lighting / Colorado Springs', 'revenue': 268.5}, {'customer': 'SUN LIGHTING INC/ TEMPE', 'revenue': 268.5}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 268.5}, {'customer': 'LIGHTSTYLE OF TAMPA BAY', 'revenue': 255.09}, {'customer': 'THE BULB BIN  INC', 'revenue': 195.0}, {'customer': 'PACE LIGHTING', 'revenue': 195.0}, {'customer': 'PLUMBING DISTRIBUTORS INC / ALPHARETTA', 'revenue': 195.0}, {'customer': 'PRESTIGE LIGHTING AND DESIGN', 'revenue': 195.0}, {'customer': 'COASTAL LIGHTING SUPPLY/ WILMINGTON', 'revenue': 189.0}, {'customer': 'LIGHTING ETC / N RICHLAND HILLS', 'revenue': 189.0}, {'customer': 'HUDSON PARC LIGHTING AND DESIGN', 'revenue': 189.0}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 187.0}, {'customer': 'INLINE ELECTRIC / CHATTANOOGA #12', 'revenue': 179.0}, {'customer': 'KRELL LIGHTING', 'revenue': 179.0}, {'customer': 'Tri-Supply Co / Beaumont', 'revenue': 179.0}, {'customer': 'HILL COUNTRY HOME CENTER LLC / KERRVILLE', 'revenue': 179.0}, {'customer': 'CAPITAL ELECTRIC / BLUFFTON', 'revenue': 179.0}, {'customer': None, 'revenue': 179.0}, {'customer': 'Fogg Lighting', 'revenue': 179.0}, {'customer': 'FERGUSON ENTERPRISES / #1334 JACKSONVILLE', 'revenue': 179.0}, {'customer': 'FERGUSON ENTERPRISES #78/ EVANSVILLE', 'revenue': 179.0}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 179.0}, {'customer': 'JUST LIGHTS  INC', 'revenue': 179.0}, {'customer': 'Sunbelt Lighting LLC / Baton Rouge', 'revenue': 97.5}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 97.5}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 97.5}, {'customer': 'DULLES ELECTRIC SUPPLY CORP / STERLING', 'revenue': 97.5}, {'customer': 'IMAGINE MORE SERVICE / NORTHERN LIGHTS', 'revenue': 97.5}, {'customer': 'PLAZA ELECTRIC', 'revenue': 97.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 94.5}, {'customer': 'INLINE ELECTRIC/ AUBURN', 'revenue': 89.5}, {'customer': 'PEAK LIGHTING', 'revenue': 89.5}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 89.5}, {'customer': 'LEBANON ELECTRIC SUPPLY, INC', 'revenue': 44.75}, {'customer': 'INLINE ELECTRIC #11 / ATHENS', 'revenue': 0.0}] | [{'item': '3118-M1L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Opal Glass', 'available': 558}, {'item': '3118-M1L RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Seeded Glass', 'available': 144}, {'item': '3118-2SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 106}, {'item': '3118-M1L PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Seeded Glass', 'available': 105}, {'item': '3118-BA2 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Seeded Glass', 'available': 105}, {'item': '3118-BA3 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-BA3 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-L BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Opal Glass', 'available': 59}, {'item': '3118-BA2 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-2SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Opal Glass', 'available': 56}, {'item': '3118-BA3 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Opal Glass', 'available': 55}, {'item': '3118-BA3 CH-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Opal Glass', 'available': 55}, {'item': '3118-3SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 CH-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Chrome and Opal Glass', 'available': 54}, {'item': '3118-BA2 CH-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Opal Glass', 'available': 52}, {'item': '3118-BA2 PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Pewter', 'available': 42}, {'item': '3118-2SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Pewter', 'available': 42}, {'item': '3118-L BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Clear Glass', 'available': 32}, {'item': '3118-1SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-BA1 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-2SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 29}, {'item': '3118-BA2 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Seeded Glass', 'available': 29}, {'item': '3118-L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Chrome and Seeded Glass', 'available': 28}, {'item': '3118-SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 28}, {'item': '3118-SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 28}, {'item': '3118-3SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 27}, {'item': '3118-4SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Semi-Flush Mount in Matte Black', 'available': 26}, {'item': '3118-BA3 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Opal Glass', 'available': 26}, {'item': '3118-BA4 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Seeded Glass', 'available': 26}, {'item': '3118-BA4 CH-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Opal Glass', 'available': 24}, {'item': '3118-BA4 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA3 PW-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Pewter and Opal Glass', 'available': 23}, {'item': '3118-SF14 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14 in Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA4 PW-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Seeded Glass', 'available': 21}, {'item': '3118-BA3 BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Clear Glass', 'available': 21}, {'item': '3118-M1L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Opal Glass', 'available': 20}, {'item': '3118-BA4 CH-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Seeded Glass', 'available': 19}, {'item': '3118-BA4 PW-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Opal Glass', 'available': 19}, {'item': '3118-BA4 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Opal Glass', 'available': 18}, {'item': '3118-BA1 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA1 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA2 BCB-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Opal Glass', 'available': 13}, {'item': '3118-BA4 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Opal Glass', 'available': 12}, {'item': '3118-M1L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Chrome and Seeded Glass', 'available': 11}, {'item': '3118-1SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Pewter', 'available': 9}, {'item': '3118-BA1 PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Seeded Glass', 'available': 9}, {'item': '3118-BA1 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-3SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Chrome', 'available': 6}, {'item': '3118-BA3 CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Seeded Glass', 'available': 6}, {'item': '3118-1SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 5}, {'item': '3118-2SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Chrome', 'available': 2}, {'item': '3118-BA2 CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Seeded Glass', 'available': 2}, {'item': '3118-L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Opal Glass', 'available': 1}, {'item': '3118-SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 1}, {'item': '3118-2SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 1}, {'item': '3118-BA2 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Opal Glass', 'available': 1}] |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 0314-BA2 BCB-CLR | Golden Lighting Remy 2-light Vanity in Brushed Champagne Brass | 0314 | 0 | 0 | — |
| 0314-BA2 BLK-CLR | Golden Lighting Remy 2-light Vanity in Matte Black | 0314 | 0 | 0 | — |
| 0314-BA2 CH-CLR | Golden Lighting Remy 2-light Vanity in Chrome | 0314 | 0 | 0 | — |
| 0314-BA2 PW-CLR | Golden Lighting Remy 2-light Vanity in Pewter | 0314 | 0 | 0 | — |
| 0314-BA3 CH-CLR | Golden Lighting Remy 3-light Vanity in Chrome | 0314 | 0 | 0 | — |
| 0314-BA3 PW-CLR | Golden Lighting Remy 3-light Vanity in Pewter | 0314 | 0 | 0 | — |
| 0804-6P ABI | Golden Lighting Abingdon 6-light Pendant in Antique Black Iron | 0804 | 0 | 0 | — |
| 0804-6P AI | Golden Lighting Abingdon 6-light Pendant in Antique Ivory | 0804 | 0 | 0 | — |
| 0804-LP ABI | Golden Lighting Abingdon 8-light Island Light in Antique Black Iron | 0804 | 0 | 0 | — |
| 0804-LP AI | Golden Lighting Abingdon 8-light Island Light in Antique Ivory | 0804 | 0 | 0 | — |
| 0804-M2L ABI | Golden Lighting Abingdon 2-light Pendant in Antique Black Iron | 0804 | 0 | 0 | — |
| 0804-M2L AI | Golden Lighting Abingdon 2-light Pendant in Antique Ivory | 0804 | 0 | 0 | — |
| 0806-1W ABI-HWG | Golden Lighting Keating 1-light Wall Sconce in Antique Black Iron | 0806 | 0 | 0 | — |
| 0806-1W AI-HWG | Golden Lighting Keating 1-light Wall Sconce in Antique Ivory | 0806 | 0 | 0 | — |
| 0806-6 ABI-HWG | Golden Lighting Keating 6-light Chandelier in Antique Black Iron | 0806 | 0 | 0 | — |
| 0806-6 AI-HWG | Golden Lighting Keating 6-light Chandelier in Antique Ivory | 0806 | 0 | 0 | — |
| 0806-9 ABI-HWG | Golden Lighting Keating 9-light Chandelier in Antique Black Iron | 0806 | 0 | 0 | — |
| 0806-9 AI-HWG | Golden Lighting Keating 9-light Chandelier in Antique Ivory | 0806 | 0 | 0 | — |
| 0806-BA2 ABI-HWG | Golden Lighting Keating 2-light Vanity in Antique Black Iron | 0806 | 0 | 0 | — |
| 0806-BA2 AI-HWG | Golden Lighting Keating 2-light Vanity in Antique Ivory | 0806 | 0 | 0 | — |
| 0806-BA3 ABI-HWG | Golden Lighting Keating 3-light Vanity in Antique Black Iron | 0806 | 0 | 0 | — |
| 0806-BA3 AI-HWG | Golden Lighting Keating 3-light Vanity in Antique Ivory | 0806 | 0 | 0 | — |
| 0806-M1L ABI-HWG | Golden Lighting Keating 1-light Pendant in Antique Black Iron and Hammered Water Glass | 0806 | 0 | 0 | — |
| 0806-M1L AI-HWG | Golden Lighting Keating 1-light Pendant in Antique Ivory and Hammered Water Glass | 0806 | 0 | 0 | — |
| 0809-5P VG-AI | Golden Lighting Alison 5-light Pendant in Vintage Gold and Antique Ivory shade | 0809 | 0 | 0 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
