# Section 3 Context Bundle — Maxim Lighting (mli)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Maxim Lighting  (mli, org_id=137)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=6490 |
| HAS_SALES_DATA | True | sales_data_count=189283 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=68 (threshold: >=5) |
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
| ENGAGEMENT_REP_COUNT | 68 | engagement_reps=68 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 91, Mixpanel total submit_order (Q-01): 102 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=82.4%, ambiguous_rate=0.0%, showroom_event_share=4.9% |
| USER_GROUP_JOIN_RATE | 82% | 75 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 5% | showroom+admin share of matched events: 4.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Nathen Bliss |

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
| HAS_NEW_ITEMS | True | new_item_count=210 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Maxim Lighting 
- **Shortname**: mli
- **Org ID**: 137
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Maxim Lighting  (mli, org_id=137)
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

# Signal Rank — Maxim Lighting  (mli, org_id=137)
- **Run date**: 2026-06-17
- **Total signals fired**: 22 (P0: 9, P1: 10, P2: 3)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 57664WTBK (Trim 11" RD LED Flush Mount 3000K) $282,149 LTM, 0 available | P0 | §3 Product | 10.0 | $282,149 | 3.0 | 8,464,477 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 10283SWBK (Lateral 3-Light Bath Vanity) $229,831 LTM, 0 available | P0 | §3 Product | 10.0 | $229,831 | 3.0 | 6,894,921 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 52102SN (Rail 24" LED Bath Vanity) $228,969 LTM, 0 available | P0 | §3 Product | 10.0 | $228,969 | 3.0 | 6,869,072 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 57933WTWT (Diverse 13" LED Flush Mount 3000K) $132,528 LTM, 0 available | P0 | §3 Product | 10.0 | $132,528 | 3.0 | 3,975,831 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 88707BK (Falcon Pull Chain 52" In/Outdoor Fan w L) $117,033 LTM, 0 available | P0 | §3 Product | 10.0 | $117,033 | 3.0 | 3,510,997 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 88708SN (Falcon AC Damp 52" In/Out Fan w LED Ligh) $101,340 LTM, 0 available | P0 | §3 Product | 10.0 | $101,340 | 3.0 | 3,040,211 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 61018GS (Odeon 8-Light WiFi-enabled LED Fandeligh) $100,438 LTM, 0 available | P0 | §3 Product | 10.0 | $100,438 | 3.0 | 3,013,150 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 12262CDBK (Acadia 2-Light Bath Vanity) $98,559 LTM, 0 available | P0 | §3 Product | 10.0 | $98,559 | 3.0 | 2,956,773 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — E25052-CHK (Souffle 8.5" 1-Light Pendant) $98,083 LTM, 0 available | P0 | §3 Product | 10.0 | $98,083 | 3.0 | 2,942,491 | RISK |
| 10 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 66% of eCat GMV | P1 | §4 Commerce | 1.6 | $307,432 | 2.0 | 1,013,488 | RISK |
| 11 | SIG-OPP-04 | New Item Adoption Gap — 22 new items with $0 platform orders | P2 | §3 Product | 2.2 | $50,000 | 1.0 | 110,000 | POSITIVE |
| 12 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 9 | 2 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 22 new items with $0 platform orders
2. **[RISK]** SIG-ANOMALY-02: Stock Out — 57664WTBK (Trim 11" RD LED Flush Mount 3000K) $282,149 LTM, 0 available
3. **[RISK]** SIG-ANOMALY-02: Stock Out — 10283SWBK (Lateral 3-Light Bath Vanity) $229,831 LTM, 0 available
4. **[RISK]** SIG-ANOMALY-02: Stock Out — 52102SN (Rail 24" LED Bath Vanity) $228,969 LTM, 0 available
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 57933WTWT (Diverse 13" LED Flush Mount 3000K) $132,528 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 88707BK (Falcon Pull Chain 52" In/Outdoor Fan w L) $117,033 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 88708SN (Falcon AC Damp 52" In/Out Fan w LED Ligh) $101,340 LTM, 0 available

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 11,183 | 3,825 | 0 | 65.80 |

### Q-37_results.md

# Q-37 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 87611WTWT | CAT2 | COL7 | Diverse 7.5" LED Flush Mount 3000K | $3.1M | 602,567 | 0 | 0 | 0 | — |
| 57692WTWT | CAT2 | CHIP | Chip 7" 15W RD LED Flush Mount | $804,389 | 71,229 | 0 | 0 | 0 | — |
| 57690WTWT | CAT2 | CHIP | Chip 5" 12W RD LED Flush Mount | $741,240 | 77,914 | 0 | 0 | 0 | — |
| 57664WTBK | CAT2 | TRIM | Trim 11" RD LED Flush Mount 3000K | $282,149 | 8,344 | 0 | 644 | 0 | 2026-06-26 |
| 57592WTWT | CAT2 | CHIP | Chip 7" 15W RD LED Flush Mount | $255,036 | 27,734 | 0 | 0 | 0 | — |
| 10283SWBK | CAT4 | COL56 | Lateral 3-Light Bath Vanity | $229,831 | 5,900 | 0 | 85 | 0 | 2026-06-29 |
| 52102SN | CAT4 | RAIL | Rail 24" LED Bath Vanity | $228,969 | 5,664 | 0 | 0 | 0 | 2026-07-06 |
| 57933WTWT | CAT2 | COL7 | Diverse 13" LED Flush Mount 3000K | $132,528 | 6,292 | 0 | 4,283 | 0 | 2026-06-26 |
| 88707BK | CAT17 | COL196 | Falcon Pull Chain 52" In/Outdoor Fan w LED Light | $117,033 | 1,106 | 0 | 505 | 0 | — |
| 88708SN | CAT17 | COL198 | Falcon AC Damp 52" In/Out Fan w LED Light Kit | $101,340 | 771 | 0 | 0 | 0 | 2026-06-26 |
| 61018GS | CAT29 | ODEON | Odeon 8-Light WiFi-enabled LED Fandelight | $100,438 | 79 | 0 | 21 | 0 | 2026-06-19 |
| 12262CDBK | CAT4 | COL8 | Acadia 2-Light Bath Vanity | $98,559 | 3,321 | 0 | 659 | 0 | 2026-06-29 |
| E25052-CHK | CAT7 | COL287 | Souffle 8.5" 1-Light Pendant | $98,083 | 1,745 | 0 | 0 | 0 | 2026-06-19 |
| 86212BK | CAT2 | STOUT | Stout RD 120-277V Indoor/Outdoor Flush Mount | $81,517 | 1,540 | 0 | 0 | 0 | 2026-07-06 |
| 57913WTWT | CAT2 | COL7 | Diverse 9" LED Flush Mount 3000K | $74,047 | 5,538 | 0 | 0 | 0 | 2026-07-19 |
| 57670WTWT | CAT2 | TRIM | Trim 16" RD LED Flush Mount 3000K | $64,415 | 997 | 0 | 0 | 0 | 2026-07-08 |
| 57597WTWT | CAT34 | COL202 | Chip 11" 26W RD LED Flush Mount - 5CCT | $61,024 | 1,873 | 0 | 115 | 0 | — |
| E25067-92BKGLD | CAT7 | SOJI | Soji 18" LED Pendant | $59,842 | 352 | 0 | 28 | 0 | 2026-06-26 |
| 39538CYBKGL | CAT8 | COL70 | Radiant 20-Light LED Chandelier | $59,726 | 44 | 0 | 3 | 0 | — |
| 38423CLNAB | CAT8 | JOLIE | Jolie 34" LED Pendant | $59,611 | 113 | 0 | 21 | 0 | — |

### Q-38a_results.md

(not present — file does not exist or is empty)

### Q-39_category_results.md

# Q-39-cat Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 55
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT2 | $16.4M | 1,264,635 | 635 | $25,757 |
| CAT5 | $11.9M | 192,874 | 738 | $16,070 |
| CAT4 | $10.3M | 215,709 | 760 | $13,507 |
| CAT7 | $6.8M | 58,313 | 682 | $9,947 |
| CAT13 | $4.7M | 12,082 | 345 | $13,690 |
| CAT6 | $3.1M | 46,431 | 579 | $5,354 |
| CAT17 | $2.7M | 21,073 | 100 | $27,148 |
| CAT8 | $2.4M | 8,761 | 220 | $10,744 |
| CAT11 | $2.1M | 7,790 | 188 | $11,151 |
| CAT3 | $1.2M | 11,535 | 119 | $10,191 |
| CAT26 | $1.2M | 15,592 | 96 | $12,451 |
| CAT14 | $1.1M | 26,343 | 122 | $9,232 |
| CAT22 | $959,285 | 28,901 | 53 | $18,100 |
| CAT34 | $920,041 | 34,212 | 105 | $8,762 |
| CAT24 | $571,258 | 6,394 | 63 | $9,068 |
| CAT19 | $508,187 | 1,302 | 56 | $9,075 |
| CAT44 | $391,814 | 1,117 | 61 | $6,423 |
| CAT29 | $389,804 | 430 | 19 | $20,516 |
| CAT15 | $389,662 | 1,416 | 74 | $5,266 |
| CAT33 | $389,496 | 3,670 | 56 | $6,955 |
| CAT9 | $266,435 | 4,272 | 22 | $12,111 |
| CAT23 | $252,122 | 1,035 | 36 | $7,003 |
| CAT25 | $232,988 | 1,917 | 27 | $8,629 |
| CAT31 | $227,808 | 4,689 | 40 | $5,695 |
| CAT35 | $162,463 | 6,462 | 54 | $3,009 |
| CAT38 | $143,005 | 985 | 17 | $8,412 |
| CAT55 | $134,005 | 1,093 | 9 | $14,889 |
| CAT52 | $123,607 | 3,127 | 55 | $2,247 |
| CAT12 | $115,767 | 1,004 | 21 | $5,513 |
| CAT48 | $97,422 | 231 | 17 | $5,731 |
| CAT32 | $77,879 | 10,771 | 56 | $1,391 |
| CAT21 | $72,625 | 154 | 15 | $4,842 |
| CAT27 | $65,669 | 1,097 | 16 | $4,104 |
| CAT43 | $58,221 | 658 | 7 | $8,317 |
| CAT28 | $39,856 | 5,300 | 47 | $848 |
| CAT36 | $39,022 | 62 | 12 | $3,252 |
| CAT20 | $36,915 | 223 | 17 | $2,171 |
| TRACK | $36,321 | 1,466 | 6 | $6,054 |
| CAT30 | $21,727 | 232 | 8 | $2,716 |
| CAT57 | $21,616 | 288 | 2 | $10,808 |
| CAT37 | $15,868 | 139 | 5 | $3,174 |
| CAT16 | $14,030 | 121 | 3 | $4,677 |
| CAT51 | $13,910 | 568 | 3 | $4,637 |
| CAT58 | $13,904 | 32 | 7 | $1,986 |
| CAT1 | $13,883 | 50 | 6 | $2,314 |
| CAT54 | $8,381 | 1,365 | 12 | $698 |
| CAT39 | $4,992 | 256 | 7 | $713 |
| CAT41 | $3,947 | 24 | 7 | $564 |
| CAT53 | $2,818 | 346 | 6 | $470 |
| CAT18 | $1,755 | 8 | 4 | $439 |
| CAT40 | $1,752 | 81 | 1 | $1,752 |
| DÉCOR | $1,575 | 9 | 2 | $788 |
| CAT46 | $969 | 11 | 1 | $969 |
| CAT59 | $750 | 1 | 1 | $750 |
| CAT60 | $19 | 3 | 1 | $19 |

### Q-39_collection_results.md

# Q-39-col Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| COL7 | $4.1M | 710,535 | 49 | $82,956 |
| SPEC | $3.2M | 64,260 | 27 | $120,155 |
| CHIP | $3.0M | 255,989 | 36 | $82,923 |
| TRIM | $2.1M | 69,923 | 42 | $48,956 |
| COL26 | $1.5M | 32,963 | 51 | $29,208 |
| WAFER | $1.4M | 55,310 | 50 | $27,636 |
| COL8 | $1.3M | 25,968 | 41 | $32,148 |
| RAIL | $986,399 | 25,213 | 16 | $61,650 |
| COL280 | $833,429 | 728 | 29 | $28,739 |
| COL313 | $819,832 | 13,723 | 23 | $35,645 |
| COL444 | $765,649 | 5,468 | 13 | $58,896 |
| COL34 | $733,228 | 17,921 | 31 | $23,653 |
| COL56 | $702,479 | 17,392 | 50 | $14,050 |
| DART | $667,708 | 12,174 | 38 | $17,571 |
| COL35 | $629,991 | 11,820 | 10 | $62,999 |
| PRIME | $616,297 | 5,552 | 68 | $9,063 |
| COL15 | $585,440 | 6,357 | 10 | $58,544 |
| COL25 | $574,768 | 29,211 | 25 | $22,991 |
| COL53 | $566,599 | 9,673 | 6 | $94,433 |
| TRIO | $528,099 | 4,562 | 7 | $75,443 |
| COL287 | $518,157 | 7,042 | 12 | $43,180 |
| SNUG | $511,137 | 64,752 | 7 | $73,020 |
| COL29 | $479,493 | 9,424 | 18 | $26,638 |
| MANTA | $479,254 | 1,281 | 17 | $28,191 |
| COL66 | $453,208 | 6,643 | 15 | $30,214 |

### Q-42_results.md

# Q-42 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 58
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| TRIM | 3,848 | $1.7M | 64,069 | $434 |
| COL8 | 2,992 | $886,832 | 20,081 | $296 |
| DART | 2,914 | $521,685 | 9,967 | $179 |
| TRIO | 103 | $198,384 | 1,790 | $1,926 |
| UNITY | 91 | $143,294 | 96 | $1,575 |
| COL629 | 300 | $115,163 | 1,549 | $384 |
| SPEC | 175 | $110,545 | 974 | $632 |
| COL533 | 118 | $100,261 | 138 | $850 |
| COL623 | 137 | $97,761 | 228 | $714 |
| COL12 | 308 | $94,103 | 576 | $306 |
| COL280 | 65 | $88,948 | 74 | $1,368 |
| AURA | 61 | $66,043 | 78 | $1,083 |
| COL596 | 98 | $64,717 | 162 | $660 |
| ABYSS | 115 | $57,562 | 402 | $501 |
| COL632 | 37 | $55,802 | 625 | $1,508 |
| COL9 | 141 | $47,273 | 224 | $335 |
| COL15 | 134 | $41,238 | 348 | $308 |
| COL18 | 203 | $39,805 | 1,032 | $196 |
| COL23 | 176 | $32,758 | 393 | $186 |
| LINK | 78 | $28,980 | 115 | $372 |
| COL2 | 90 | $26,991 | 286 | $300 |
| COL14 | 61 | $25,887 | 361 | $424 |
| COL630 | 36 | $20,254 | 45 | $563 |
| YOU | 12 | $19,385 | 15 | $1,615 |
| COL19 | 86 | $16,471 | 239 | $192 |
| COL590 | 74 | $13,870 | 146 | $187 |
| COL3 | 171 | $13,719 | 613 | $80 |
| COL620 | 37 | $12,900 | 112 | $349 |
| COL617 | 41 | $11,848 | 83 | $289 |
| COL627 | 19 | $9,053 | 20 | $476 |
| COL624 | 29 | $7,633 | 47 | $263 |
| COL626 | 11 | $6,255 | 13 | $569 |
| COL10 | 14 | $5,510 | 15 | $394 |
| COL22 | 27 | $5,028 | 48 | $186 |
| CHARM | 13 | $4,906 | 23 | $377 |
| COL622 | 12 | $4,876 | 16 | $406 |
| COL628 | 3 | $3,822 | 3 | $1,274 |
| ABODE | 23 | $3,731 | 35 | $162 |
| NOB | 16 | $3,319 | 26 | $207 |
| VISOR | 17 | $2,824 | 23 | $166 |
| ORSON | 8 | $1,769 | 13 | $221 |
| COL17 | 25 | $1,634 | 49 | $65 |
| COL20 | 12 | $1,555 | 19 | $130 |
| COL16 | 3 | $623 | 16 | $208 |
| COL1 | 8 | $427 | 9 | $53 |
| POD | 4 | $188 | 4 | $47 |
| COL631 | 2 | $84 | 1 | $42 |
| COL618 | 2 | $64 | 2 | $32 |
| PLANK | 2 | $0 | 0 | $0 |
| ION | 1 | $0 | 0 | $0 |
| COL601 | 1 | $0 | 0 | $0 |
| SPIRE | 2 | $0 | 0 | $0 |
| COL608 | 2 | $0 | 0 | $0 |
| COL616 | 1 | $0 | 0 | $0 |
| BULBS | 1 | $0 | 0 | $0 |
| COL621 | 1 | $0 | 0 | $0 |
| YORK | 2 | $0 | 0 | $0 |
| ARC | 1 | $0 | 0 | $0 |

### Q-59_results.md

(not present — file does not exist or is empty)

### Q-61_results.md

(not present — file does not exist or is empty)

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 57664WTBK | Trim 11" RD LED Flush Mount 3000K | TRIM | 282,149.23 | 8,348 | — | 2026-06-26 | [{'customer': 'US ELECTRICAL SERVICES INC(USESI)', 'revenue': 72898.3}, {'customer': 'CAPITOL LIGHTING', 'revenue': 22635.2}, {'customer': 'FERGUSON-PERRIS, CA', 'revenue': 21425.75}, {'customer': 'HANSEN LIGHTING, INC.-LINDON, UT', 'revenue': 21232.5}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 10924.55}, {'customer': 'SHADES OF LIGHT LLC', 'revenue': 10613.36}, {'customer': 'SEATTLE LIGHTING-SEATTLE', 'revenue': 8777.47}, {'customer': 'PACIFIC LAMP & SUPPLY CO.', 'revenue': 6536.0}, {'customer': 'WAYFAIR LLC', 'revenue': 6033.9}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 6014.84}, {'customer': 'THE LIGHTING DESIGN-LAYTON, UT', 'revenue': 5733.3}, {'customer': 'FERGUSON-NAMPA, ID', 'revenue': 5159.17}, {'customer': 'LEGACY LIGHTING LLC', 'revenue': 4621.25}, {'customer': "FERGUSON-COEUR D'ALENE, ID", 'revenue': 4462.76}, {'customer': 'LIGHTWISE-BOLIVAR, MO', 'revenue': 4263.9}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 3564.05}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 3182.27}, {'customer': 'FERGUSON-NEW HUDSON, MI', 'revenue': 2937.4}, {'customer': 'JOSS AND MAIN-BOSTON', 'revenue': 2882.31}, {'customer': 'FERGUSON-FRONT ROYAL, VA', 'revenue': 2614.4}, {'customer': 'FERGUSON-ADDISON, IL', 'revenue': 2614.4}, {'customer': 'FERGUSON-PORTLAND, OR', 'revenue': 1952.0}, {'customer': 'FERGUSON-STOCKTON, CA', 'revenue': 1904.75}, {'customer': 'MAXWELL LIGHTING & ENERGY', 'revenue': 1832.5}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 1815.3}, {'customer': 'FERGUSON-MANCHESTER, NH', 'revenue': 1808.8}, {'customer': 'INDEPENDENT ELECTRIC-MANCHESTER, NH', 'revenue': 1747.5}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 1581.6}, {'customer': 'THE LIGHTING DESIGN, LLC', 'revenue': 1449.8}, {'customer': 'BUILDERS ELECTRIC INC.,CORP OF WY', 'revenue': 1372.0}, {'customer': 'CED - KENT, WA', 'revenue': 1333.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 1199.0}, {'customer': 'MAIN ELECTRIC SUPPLY CO.', 'revenue': 1073.0}, {'customer': 'LAMPS PLUS', 'revenue': 1032.72}, {'customer': 'LIGHTOLOGY', 'revenue': 795.68}, {'customer': 'LOWES COMPANIES', 'revenue': 785.4}, {'customer': 'HI-LIGHT LIGHTING', 'revenue': 774.0}, {'customer': 'ELLEN LIGHTING & HARDWARE-SUGARLAND', 'revenue': 774.0}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 774.0}, {'customer': 'PARAMONT-EO, INC.-NEW LENOX, IL', 'revenue': 633.0}, {'customer': 'WALTERS WHOLESALE ELECTRIC', 'revenue': 598.75}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 598.56}, {'customer': 'FERGUSON-RICHMOND, VA', 'revenue': 568.1}, {'customer': 'FERGUSON-FORT PAYNE, AL', 'revenue': 531.05}, {'customer': "FERGUSON-O'FALLON, MO", 'revenue': 526.3}, {'customer': 'POWER DESIGN RESOURCES', 'revenue': 516.0}, {'customer': 'CED-DALLAS, TX', 'revenue': 516.0}, {'customer': 'WAYFAIR LLC-CRANBURY, NJ', 'revenue': 511.22}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 500.6}, {'customer': 'FERGUSON-GRIMES, IA', 'revenue': 490.2}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 483.55}, {'customer': 'FERGUSON-FREDERICKSBURG, VA', 'revenue': 482.6}, {'customer': 'NORTHEAST ELECTRICAL-HAVERHILL, MA', 'revenue': 473.0}, {'customer': 'HAUS APPEAL LLC', 'revenue': 464.4}, {'customer': 'HOME LIGHTING', 'revenue': 450.1}, {'customer': 'FERGUSON-LEBANON, TN', 'revenue': 449.35}, {'customer': 'LIGHTS UNLIMITED  INC.-WAKE FOREST', 'revenue': 430.0}, {'customer': 'E.B. LIGHTING & SUPPLIES, INC.', 'revenue': 430.0}, {'customer': 'WAYFAIR LLC-LANCASTER, TX', 'revenue': 426.91}, {'customer': 'WAYFAIR LLC-PERRIS, CA', 'revenue': 421.09}, {'customer': 'LAMPS PLUS', 'revenue': 407.1}, {'customer': 'DU PAGE LIGHTING', 'revenue': 371.0}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 359.0}, {'customer': 'ELEKTRA LIGHTS & FANS, INC.', 'revenue': 355.5}, {'customer': 'KENDALL ELECTRIC-GRAND RAPIDS, MI', 'revenue': 344.0}, {'customer': 'THE LIGHTING CORNER', 'revenue': 344.0}, {'customer': 'WILSON LIGHTING', 'revenue': 344.0}, {'customer': 'URBAN LIGHTS-DENVER, CO', 'revenue': 339.5}, {'customer': 'FERGUSON-AURORA, CO', 'revenue': 319.2}, {'customer': 'ULTRA DESIGN CENTER', 'revenue': 301.0}, {'customer': 'LEE SUPPLY CORP.-NEW ALBANY, IN', 'revenue': 301.0}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 301.0}, {'customer': 'WAYFAIR LLC-MCDONOUGH, GA', 'revenue': 293.88}, {'customer': 'ELECTRICAL WHOLESALE-IDAHO FALLS,ID', 'revenue': 270.0}, {'customer': 'URBAN LIGHTS', 'revenue': 267.3}, {'customer': 'THE FAN CONNECTION', 'revenue': 258.0}, {'customer': 'MICHAELS ELECTRICAL SUPPLY', 'revenue': 258.0}, {'customer': 'W.T. LIGHTING-ROCHESTER', 'revenue': 258.0}, {'customer': 'FERGUSON-EAST SYRACUSE, NY', 'revenue': 245.1}, {'customer': 'FERGUSON-WILLIAMSBURG, VA', 'revenue': 245.1}, {'customer': 'ROCKINGHAM ELECTRICAL-NEWINGTON', 'revenue': 244.79}, {'customer': 'KBL DESIGN CENTER, INC.', 'revenue': 233.7}, {'customer': 'JONES LIGHTING SPECIALISTS', 'revenue': 227.9}, {'customer': 'FERGUSON-FRANKLIN, NC', 'revenue': 222.3}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 221.4}, {'customer': 'B.E.S. LIGHTING CENTER', 'revenue': 215.0}, {'customer': 'CAPE ELECTRIC SUPPLY', 'revenue': 215.0}, {'customer': 'SYNERGY LIGHT STUDIO', 'revenue': 215.0}, {'customer': 'DHILLON LIGHTING INC.-WINNIPEG, MB', 'revenue': 215.0}, {'customer': 'PARAMONT-EO INC.-CHICAGO', 'revenue': 215.0}, {'customer': 'FERGUSON-ALPHARETTA, GA', 'revenue': 204.25}, {'customer': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'revenue': 204.25}, {'customer': 'THE LIGHTING SHOPPE', 'revenue': 204.25}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 204.25}, {'customer': 'LEE SUPPLY CORP.', 'revenue': 195.65}, {'customer': 'FLEX DISTRIBUTION C/O CAPSTONE LTG', 'revenue': 195.0}, {'customer': 'BRIGHTER HOMES LIGHTING-EUGENE', 'revenue': 190.94}, {'customer': 'CITY ELECTRIC SUPPLY-PASADENA, CA', 'revenue': 189.2}, {'customer': 'FERGUSON-LEWISVILLE, TX', 'revenue': 185.25}, {'customer': 'FERGUSON-CHARLOTTESVILLE, VA', 'revenue': 185.25}, {'customer': 'ULTRA LIGHTING-MISSISSAUGA', 'revenue': 172.0}, {'customer': 'STARLIGHT LIGHTING CENTRE', 'revenue': 172.0}, {'customer': 'KENNEWICK IND/DBA KIE SUPPLY', 'revenue': 172.0}, {'customer': 'LIGHTOPIA', 'revenue': 168.0}, {'customer': 'R. WILSON CO. INC.-LENEXA, KS', 'revenue': 163.4}, {'customer': 'FERGUSON-FARGO, ND', 'revenue': 163.4}, {'customer': 'FERGUSON-COLUMBUS, OH', 'revenue': 159.6}, {'customer': 'PLATT ELECTRIC-MOUNTLAKE TERRACE,WA', 'revenue': 156.0}, {'customer': 'LIGHTING, INC. OFFICE-HOUSTON', 'revenue': 140.4}, {'customer': 'KENDALL ELECTRIC, INC.-COLUMBUS, OH', 'revenue': 129.0}, {'customer': 'GALAXY LIGHTING', 'revenue': 129.0}, {'customer': 'JUST LIGHTS INC.', 'revenue': 129.0}, {'customer': 'KNOXVILLE NOLAND CO.-KNOXVILLE, TN', 'revenue': 129.0}, {'customer': 'DHILLON LIGHTING CALGARY LTD.', 'revenue': 129.0}, {'customer': 'TIMBERLAKE LIGHTING OF LYNCHBURG', 'revenue': 129.0}, {'customer': 'YALE ELECTRIC-LANCASTER, PA', 'revenue': 129.0}, {'customer': 'WAREHOUSE-LIGHTING.COM', 'revenue': 129.0}, {'customer': 'COLONIAL ELECTRIC-PHILADELPHIA, PA', 'revenue': 129.0}, {'customer': 'HERITAGE INTERIORS & DESIGN', 'revenue': 129.0}, {'customer': 'PLATT ELECTRIC-KENT, WA', 'revenue': 129.0}, {'customer': 'FERGUSON-SAN ANTONIO, TX', 'revenue': 122.55}, {'customer': 'FERGUSON-BATON ROUGE, LA', 'revenue': 122.55}, {'customer': 'FERGUSON-VISTA, CA', 'revenue': 122.55}, {'customer': 'LAMPS.COM', 'revenue': 122.55}, {'customer': 'FERGUSON-COLUMBIA, SC', 'revenue': 122.55}, {'customer': 'FERGUSON-GOLDEN VALLEY, MN', 'revenue': 122.55}, {'customer': 'FERGUSON-HOLLY SPRINGS, NC', 'revenue': 122.55}, {'customer': 'FERGUSON-LEXINGTON, KY', 'revenue': 118.75}, {'customer': 'COLONIAL LIGHTING-DECATUR, GA', 'revenue': 117.0}, {'customer': 'INCOLIGHT GROUP LLC.', 'revenue': 117.0}, {'customer': '43RD STREET LIGHTING, INC.', 'revenue': 117.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 116.1}, {'customer': 'FERGUSON-MEMPHIS, TN', 'revenue': 114.95}, {'customer': 'FERGUSON-CORPUS CHRISTI, TX', 'revenue': 111.15}, {'customer': 'WAYFAIR LLC-PORT WENTWORTH, GA', 'revenue': 109.65}, {'customer': 'PLATT ELECTRIC SUPPLY', 'revenue': 108.0}, {'customer': 'CRESCENT LIGHTING-SPOKANE VALLEY,WA', 'revenue': 104.91}, {'customer': 'NORTH COAST LIGHTING-PORTLAND, OR', 'revenue': 95.91}, {'customer': 'BRIGHT IDEAS INC.', 'revenue': 86.0}, {'customer': 'PINE TREE LIGHTING-LAKE ORION', 'revenue': 86.0}, {'customer': 'LEE SUPPLY CORP.-DAYTON, OH', 'revenue': 86.0}, {'customer': 'TRI-SUPPLY-AUSTIN, TX', 'revenue': 86.0}, {'customer': 'LEE SUPPLY CORP.-CARMEL', 'revenue': 86.0}, {'customer': 'STATE ELECTRIC-CHRISTIANSBURG, VA', 'revenue': 86.0}, {'customer': 'LIGHT BRITE DISTRIBUTING-TRENTON', 'revenue': 82.0}, {'customer': 'CASA DI LUCE', 'revenue': 82.0}, {'customer': 'PREMIER LIGHTING-PHOENIX, AZ', 'revenue': 81.7}, {'customer': 'FERGUSON-TAUNTON, MA', 'revenue': 81.7}, {'customer': 'FERGUSON ENTERPRISES-LEWISTON,ID', 'revenue': 81.7}, {'customer': 'FERGUSON-LANSING, MI', 'revenue': 81.7}, {'customer': 'KENDALL ELECTRIC-FORT WAYNE, IN', 'revenue': 78.0}, {'customer': 'CABINET & LIGHTING SUPPLY', 'revenue': 78.0}, {'customer': 'FERGUSON-BROOKSHIRE, TX', 'revenue': 77.9}, {'customer': 'LIGHTING, INC. OFFICE-AUSTIN', 'revenue': 77.4}, {'customer': 'WILLCALL FOR LIGHT CONCERN', 'revenue': 75.66}, {'customer': 'FERGUSON-SUMNER, WA', 'revenue': 66.94}, {'customer': 'MV BY DESIGN', 'revenue': 54.0}, {'customer': 'CITY LIGHTS', 'revenue': 43.0}, {'customer': 'RAINBOW LIGHTING', 'revenue': 43.0}, {'customer': 'SHEPARD LIGHTING', 'revenue': 43.0}, {'customer': 'CASA DI LUCE', 'revenue': 43.0}, {'customer': 'LIGHTING BY LDI', 'revenue': 43.0}, {'customer': 'THE LIGHT CENTER', 'revenue': 43.0}, {'customer': 'MAIN ELECTRIC SUPPLY-SAN DIEGO, CA', 'revenue': 42.9}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 42.75}, {'customer': 'FERGUSON - SOUTH BEND, IN', 'revenue': 40.85}, {'customer': 'FERGUSON-JACKSON, WY', 'revenue': 40.85}, {'customer': 'FERGUSON-ROANOKE, VA', 'revenue': 40.85}, {'customer': 'SUN LIGHTING', 'revenue': 40.85}, {'customer': 'FERGUSON-NORFOLK, VA', 'revenue': 40.85}, {'customer': 'FERGUSON- CHANDLER,AZ', 'revenue': 40.85}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 40.85}, {'customer': 'ROBINSON LIGHTING', 'revenue': 40.85}, {'customer': 'FERGUSON-SEATTLE, WA', 'revenue': 40.85}, {'customer': 'FERGUSON-GRAND PRAIRIE, TX', 'revenue': 40.85}, {'customer': 'FERGUSON-JOHNSON CITY, TN', 'revenue': 40.85}, {'customer': 'FERGUSON-WEST ALLIS, WI', 'revenue': 40.85}, {'customer': 'LIGHT BULBS ETC.', 'revenue': 40.85}, {'customer': 'FERGUSON-HUDSON, WI', 'revenue': 40.85}, {'customer': 'FERGUSON-ROUND ROCK, TX', 'revenue': 40.85}, {'customer': 'FERGUSON-ST. GEORGE, UT', 'revenue': 40.85}, {'customer': 'UNION LIGHTING', 'revenue': 40.85}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 39.0}, {'customer': 'MARX FIREPLACES & LIGHTING', 'revenue': 39.0}, {'customer': 'GROVER ELECTRIC-MEDFORD, OR', 'revenue': 39.0}, {'customer': 'MCLAREN LIGHTING', 'revenue': 39.0}, {'customer': 'FANCO - LAS VEGAS, NV', 'revenue': 39.0}, {'customer': 'LA LUZ LIGHTING LLC.', 'revenue': 39.0}, {'customer': 'METRO ELECTRIC SUPPLY-BRENTWOOD, MO', 'revenue': 38.7}, {'customer': 'PINE LIGHTING-KELOWNA', 'revenue': 38.7}, {'customer': 'WAYFAIR LLC -PERIGOLD', 'revenue': 36.55}, {'customer': 'CRESCENT LIGHTING SUPPLY-OLYMPIA,WA', 'revenue': 34.97}, {'customer': 'CRESCENT LIGHTING-BURLINGTON, WA', 'revenue': 34.97}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 34.95}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 32.95}, {'customer': 'URBAN LIGHTS', 'revenue': 31.55}, {'customer': 'ALL CITY LIGHTING & SUPPLIES INC.', 'revenue': 30.95}, {'customer': 'CAPITAL ELECTRIC-UPPER MARLBORO, MD', 'revenue': 30.1}, {'customer': 'WASATCH LIGHTING', 'revenue': 21.5}, {'customer': 'LIGHTS ON DESIGN, INC.', 'revenue': 19.5}, {'customer': 'CASA DI LUCE', 'revenue': 5.0}, {'customer': 'TURN ON LIGHTING', 'revenue': 0.0}] | [{'item': '57660WTWT', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 8984}, {'item': '57662WTWT', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 4604}, {'item': '57664WTSN', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 2689}, {'item': '57662WTBK', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 2103}, {'item': '57670WTBK', 'desc': 'Trim 16" RD LED Flush Mount 3000K', 'available': 1859}, {'item': '57663WTBK', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 1763}, {'item': '57664WTWT', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 1585}, {'item': '57663WTSN', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 1092}, {'item': '57662WTSN', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 989}, {'item': '57668WTWT', 'desc': 'Trim 8.5" SQ LED Flush Mount 3000K', 'available': 943}, {'item': '57667WTWT', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 900}, {'item': '57660WTSN', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 615}, {'item': '57668WTSN', 'desc': 'Trim 8.5" SQ LED Flush Mount 3000K', 'available': 585}, {'item': '57663WTWT', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 574}, {'item': '57670WTSN', 'desc': 'Trim 16" RD LED Flush Mount 3000K', 'available': 479}, {'item': '57675WTWT', 'desc': 'Trim 15.5" SQ LED Flush Mount 3000K', 'available': 325}, {'item': '57664WTPC', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 311}, {'item': '57663WTPC', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 309}, {'item': '57669WTWT', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 265}, {'item': '57668WTBK', 'desc': 'Trim 8.5" SQ LED Flush Mount 3000K', 'available': 259}, {'item': '57667WTBK', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 258}, {'item': '57660WTSBR', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 251}, {'item': '57675WTBK', 'desc': 'Trim 15.5" SQ LED Flush Mount 3000K', 'available': 235}, {'item': '57665WTWT', 'desc': 'Trim 4.5" SQ LED Flush Mount 3000K', 'available': 232}, {'item': '57890WT', 'desc': 'Empty EM Shell for 7" Round Trim', 'available': 222}, {'item': '57669WTSN', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 211}, {'item': '57664WTSBR', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 205}, {'item': '57662WTPC', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 196}, {'item': '57669WTBK', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 189}, {'item': '57670WTSBR', 'desc': 'Trim 16" RD LED Flush Mount 3000K', 'available': 173}, {'item': '57662WTSBR', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 163}, {'item': '57600PC', 'desc': 'Pendant Conversion Kit for Trim 5766x - Chrome', 'available': 162}, {'item': '57665WTSN', 'desc': 'Trim 4.5" SQ LED Flush Mount 3000K', 'available': 155}, {'item': '57660WTPC', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 133}, {'item': '57665WTBK', 'desc': 'Trim 4.5" SQ LED Flush Mount 3000K', 'available': 127}, {'item': '57669WTPC', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 97}, {'item': '57660WTBK', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 91}, {'item': '57675WTSN', 'desc': 'Trim 15.5" SQ LED Flush Mount 3000K', 'available': 86}, {'item': '57667WTSN', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 50}, {'item': '57667WTPC', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 8}] |
| 10283SWBK | Lateral 3-Light Bath Vanity | COL56 | 229,830.69 | 5,905 | — | 2026-06-29 | [{'customer': 'US ELECTRICAL SERVICES INC(USESI)', 'revenue': 31576.3}, {'customer': 'AVID LIGHTING, LLC', 'revenue': 25884.0}, {'customer': 'MAIN ELECTRIC SUPPLY CO.', 'revenue': 14269.2}, {'customer': 'CED-UPPER MARLBORO, MD', 'revenue': 11814.25}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 11728.2}, {'customer': 'CARRINGTON LIGHTING.COM', 'revenue': 10738.75}, {'customer': 'THE LIGHTING DESIGN, LLC', 'revenue': 10094.7}, {'customer': 'CBMC LIGHTING SOLUTIONS', 'revenue': 9534.45}, {'customer': 'CBMC LIGHTING SOLUTION-INDIANAPOLIS', 'revenue': 8095.4}, {'customer': 'DOMINION ELECTRIC SUPPLY, INC.', 'revenue': 7984.75}, {'customer': 'PEAK LIGHTING BULBS & BALLASTS,LLC', 'revenue': 7350.0}, {'customer': "DESIGNER'S MART", 'revenue': 5944.15}, {'customer': 'LIFESTYLES-TULSA', 'revenue': 5601.8}, {'customer': 'LIFESTYLES', 'revenue': 5374.7}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY-BARRINGTON', 'revenue': 5181.25}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 4721.25}, {'customer': 'CBMC LIGHTING SOLUTIONS', 'revenue': 4655.7}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 4419.05}, {'customer': 'ROBINSON LIGHTING-WINNIPEG', 'revenue': 3305.7}, {'customer': 'AZTEC LIGHTING', 'revenue': 3020.05}, {'customer': 'IBS LIGHTING, LTD. LLC', 'revenue': 2787.15}, {'customer': 'ILLUMINATE LIGHTING-LISBON, IA', 'revenue': 2695.0}, {'customer': 'STEADFAST LIGHTING LLC', 'revenue': 2548.0}, {'customer': 'IBS LIGHTING, LTD.-THE COLONY, TX', 'revenue': 2463.9}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 2450.0}, {'customer': 'TEXAS FLOOR SOURCE', 'revenue': 1987.2}, {'customer': 'ALL-PHASE ELECTRIC-GRAND JUNCTION', 'revenue': 1764.0}, {'customer': 'THE LIGHTING DESIGN-LAYTON, UT', 'revenue': 1745.7}, {'customer': 'ELECTRICAL PLUMBING STORE', 'revenue': 1568.0}, {'customer': 'SIGNATURE LIGHTING & FANS', 'revenue': 1422.5}, {'customer': 'REXEL USA, INC.-TEMPLE, TX', 'revenue': 882.0}, {'customer': 'PINE TREE LIGHTING-LAKE ORION', 'revenue': 796.95}, {'customer': 'FERGUSON-CELINA, OH', 'revenue': 698.25}, {'customer': 'LONG LIGHTING STUDIO INC.', 'revenue': 686.0}, {'customer': 'ROBINSON LIGHTING', 'revenue': 629.6}, {'customer': 'FRANKLIN BUILDING SUPPLY-POCATELLO', 'revenue': 584.25}, {'customer': 'TURNEY LIGHTING & ELECTRIC', 'revenue': 510.25}, {'customer': 'ALL-PHASE ELECTRIC-BLOOMINGTON, IN', 'revenue': 449.82}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 441.0}, {'customer': 'HAUS APPEAL LLC', 'revenue': 441.0}, {'customer': 'R. WILSON CO. INC.-LENEXA, KS', 'revenue': 418.95}, {'customer': 'LIGHTING, INC. OFFICE-HOUSTON', 'revenue': 407.05}, {'customer': 'WEL-LIT HOMES-OGDEN', 'revenue': 379.5}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 379.5}, {'customer': 'NORTH COAST LIGHTING-PORTLAND, OR', 'revenue': 366.93}, {'customer': 'GRAYBAR ELECTRIC-CHARLOTTE, NC', 'revenue': 343.0}, {'customer': 'METRO ELECTRIC SUPPLY-BRENTWOOD, MO', 'revenue': 308.7}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 294.0}, {'customer': 'FANDANGO LIGHTS & DECOR', 'revenue': 294.0}, {'customer': 'UNITED ELECTRIC SUPPLY CO', 'revenue': 245.7}, {'customer': 'TECHTRON PRODUCTS, INC.', 'revenue': 245.0}, {'customer': 'LAMPS PLUS', 'revenue': 244.02}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 203.85}, {'customer': 'DAKOTA WHOLESALE-SIOUX FALLS, SD', 'revenue': 203.01}, {'customer': 'GRAHAM LIGHTING-MEMPHIS', 'revenue': 196.0}, {'customer': 'MEDINA LIGHTING, INC.', 'revenue': 196.0}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 196.0}, {'customer': 'E. SAM JONES DISTRIBUTOR,', 'revenue': 196.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 196.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 184.75}, {'customer': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'revenue': 179.75}, {'customer': 'NORTH COAST LIGHTING-BILLINGS, MT', 'revenue': 163.08}, {'customer': 'BONAIRE LIGHTING SOLUTIONS', 'revenue': 162.85}, {'customer': 'THE LIGHTING CORNER', 'revenue': 159.8}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 147.0}, {'customer': 'NORTHERN LIGHTS & ACCENTS', 'revenue': 147.0}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 147.0}, {'customer': 'SEATTLE LIGHTING-SEATTLE', 'revenue': 147.0}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 147.0}, {'customer': 'SUMMIT ELECTRIC SUPPLY-PHOENIX, AZ', 'revenue': 147.0}, {'customer': 'BULB LIGHTING & DESIGN', 'revenue': 147.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 147.0}, {'customer': 'MULTI LUMINAIRE LAVAL', 'revenue': 139.65}, {'customer': 'GROVER ELECTRIC -BOISE', 'revenue': 125.31}, {'customer': 'CAPITAL CITY DESIGN CENTER, INC.', 'revenue': 125.01}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 124.95}, {'customer': 'MATHES ELECTRIC OF FORT WALTON', 'revenue': 124.71}, {'customer': 'ROBINSON LIGHTING-KELOWNA', 'revenue': 116.85}, {'customer': 'IMAGINE MORE', 'revenue': 104.85}, {'customer': 'SOUTH DADE LIGHTING INC.-MIAMI', 'revenue': 98.0}, {'customer': 'KANSAS LIGHTING DISTRICT-WICHITA', 'revenue': 98.0}, {'customer': 'THE LIGHTING CONNECTION', 'revenue': 98.0}, {'customer': 'LIVIO DESIGNS, LLC-LACOMBE, LA', 'revenue': 98.0}, {'customer': 'EAST COAST LUMBER BUILDING SUPPLY', 'revenue': 98.0}, {'customer': 'KENNEWICK IND/DBA KIE SUPPLY', 'revenue': 98.0}, {'customer': 'ABBEVILLE ELECTRIC SUPPLY INC.', 'revenue': 98.0}, {'customer': 'LITECRAFT LIGHTING-AUGUSTA, GA', 'revenue': 98.0}, {'customer': 'KENYON NOBLE LUMBER-BOZEMAN, MT', 'revenue': 98.0}, {'customer': 'KBL DESIGN CENTER, INC.', 'revenue': 93.1}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 88.2}, {'customer': 'WEL-LIT HOMES', 'revenue': 75.9}, {'customer': 'MAIN ELECTRIC SUPPLY-VENTURA, CA', 'revenue': 75.9}, {'customer': 'WAYFAIR LLC', 'revenue': 73.5}, {'customer': 'SUBURBAN WHOLESALE LIGHTING', 'revenue': 71.9}, {'customer': 'PLANK & TILE', 'revenue': 69.9}, {'customer': 'W.T. LIGHTING-ROCHESTER', 'revenue': 49.0}, {'customer': 'LYONS ELECTRIC SUPPLY', 'revenue': 49.0}, {'customer': 'THE HOME CENTER, INC', 'revenue': 49.0}, {'customer': 'THE OLDE PARSONAGE', 'revenue': 49.0}, {'customer': 'BRIGGS INC.', 'revenue': 49.0}, {'customer': 'GLOBE LIGHTING CO.-HAPPY VALLEY', 'revenue': 49.0}, {'customer': 'FIXTURE THIS INC.', 'revenue': 49.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 49.0}, {'customer': 'SIOUX FALLS LIGHTHOUSE', 'revenue': 49.0}, {'customer': 'ELITE LIGHTING INNOVATIONS', 'revenue': 49.0}, {'customer': 'E.G. PENNER BUILDING-STEINBACH', 'revenue': 49.0}, {'customer': 'VP SUPPLY CORPORATION-ROCHESTER', 'revenue': 49.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 49.0}, {'customer': 'ILLUMINATE LIGHTING', 'revenue': 49.0}, {'customer': 'HODGSON LIGHT & LOG', 'revenue': 49.0}, {'customer': 'LITEMODE LIMITED', 'revenue': 49.0}, {'customer': 'MULTI LUMINAIRE LEVIS', 'revenue': 46.55}, {'customer': 'FERGUSON-COLUMBIA, MO', 'revenue': 46.55}, {'customer': 'THE LIGHTING SHOPPE-WAREHOUSE', 'revenue': 46.55}, {'customer': 'LIGHTOLOGY', 'revenue': 45.33}, {'customer': 'GROVER ELECTRIC -NAMPA', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-GRANTS PASS, OR', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-KLAMATH FALLS, OR', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-TWIN FALLS', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-MEDFORD, OR', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC & PLUMBING INC.', 'revenue': 41.77}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 38.95}, {'customer': 'KENDALL ELECTRIC-GRAND RAPIDS, MI', 'revenue': 37.95}, {'customer': 'MASTRO ELECTRIC SUPPLY CO.', 'revenue': 34.3}, {'customer': 'HABITECH SYSTEMS-ORMOND BEACH, FL', 'revenue': 24.5}] | [{'item': '10283CLSN', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 744}, {'item': '10282CLSN', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 734}, {'item': '10283SWSN', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 676}, {'item': '10284SWBK', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 422}, {'item': '10283CLBK', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 400}, {'item': '10281CLSN', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 400}, {'item': '10284CLBK', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 398}, {'item': '10282SWSN', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 389}, {'item': '10284CLSN', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 371}, {'item': '90281CLSN', 'desc': 'Lateral Mini Pendant', 'available': 245}, {'item': '90281SWSN', 'desc': 'Lateral Mini Pendant', 'available': 228}, {'item': '10283SWSBR', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 203}, {'item': '10282SWBK', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 199}, {'item': '10282CLBK', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 186}, {'item': '10286SWBK', 'desc': 'Lateral 5-Light Chandelier', 'available': 184}, {'item': '10285CLSN', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 170}, {'item': '90281CLBK', 'desc': 'Lateral Mini Pendant', 'available': 166}, {'item': '10282SWSBR', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 157}, {'item': '10284SWSBR', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 157}, {'item': '90281SWBK', 'desc': 'Lateral Mini Pendant', 'available': 152}, {'item': '10286SWSN', 'desc': 'Lateral 5-Light Chandelier', 'available': 125}, {'item': '10285SWSN', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 92}, {'item': '90281CLSBR', 'desc': 'Lateral Mini Pendant', 'available': 90}, {'item': '10285CLBK', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 71}, {'item': '10287CLSN', 'desc': 'Lateral 3-Light Chandelier', 'available': 50}, {'item': '10281CLSBR', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 49}, {'item': '10285SWSBR', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 47}, {'item': '10282CLSBR', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 47}, {'item': '10281SWBK', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 46}, {'item': '10283CLSBR', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 46}, {'item': '10286CLSN', 'desc': 'Lateral 5-Light Chandelier', 'available': 45}, {'item': '10287CLBK', 'desc': 'Lateral 3-Light Chandelier', 'available': 43}, {'item': '10287SWSN', 'desc': 'Lateral 3-Light Chandelier', 'available': 43}, {'item': '10288CLSN', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 42}, {'item': '10287SWBK', 'desc': 'Lateral 3-Light Chandelier', 'available': 38}, {'item': '10286CLSBR', 'desc': 'Lateral 5-Light Chandelier', 'available': 34}, {'item': '10287CLSBR', 'desc': 'Lateral 3-Light Chandelier', 'available': 34}, {'item': '10287SWSBR', 'desc': 'Lateral 3-Light Chandelier', 'available': 33}, {'item': '10286CLBK', 'desc': 'Lateral 5-Light Chandelier', 'available': 31}, {'item': '10288CLBK', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 28}, {'item': '10285SWBK', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 24}, {'item': '10288CLSBR', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 24}, {'item': '90281SWSBR', 'desc': 'Lateral Mini Pendant', 'available': 23}, {'item': '10286SWSBR', 'desc': 'Lateral 5-Light Chandelier', 'available': 15}, {'item': '10288SWSBR', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 10}, {'item': '10288SWBK', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 7}, {'item': '10288SWSN', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 6}, {'item': '10281SWSBR', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 3}] |
| 52102SN | Rail 24" LED Bath Vanity | RAIL | 228,969.07 | 5,666 | — | 2026-07-06 | [{'customer': 'J6 ENTERPRISES, LLC', 'revenue': 17801.45}, {'customer': 'LIGHTOLOGY', 'revenue': 15338.7}, {'customer': 'FERGUSON-CELINA, OH', 'revenue': 14683.2}, {'customer': 'GRAYBAR ELECTRIC CO.-SEATTLE, WA', 'revenue': 13892.45}, {'customer': 'REGENCY LIGHTING-KENNESAW, GA', 'revenue': 12493.26}, {'customer': 'FERGUSON-COXSACKIE, NY', 'revenue': 8740.0}, {'customer': 'WIEDENBACH-BROWN-USESI', 'revenue': 8458.0}, {'customer': 'FERGUSON-FRONT ROYAL, VA', 'revenue': 8171.9}, {'customer': 'LIGHTWISE-BOLIVAR, MO', 'revenue': 7479.3}, {'customer': 'ALL COUNTY ELECTRIC SUPPLY', 'revenue': 6578.0}, {'customer': 'FERGUSON-GRAND PRAIRIE, TX', 'revenue': 6555.0}, {'customer': 'FERGUSON-FORT PAYNE, AL', 'revenue': 6456.2}, {'customer': 'FERGUSON-RICHLAND, WA', 'revenue': 5549.9}, {'customer': 'FERGUSON-STOCKTON, CA', 'revenue': 5506.2}, {'customer': 'SEATTLE LIGHTING-SEATTLE', 'revenue': 5462.0}, {'customer': 'THE LIGHTING DESIGN-LAYTON, UT', 'revenue': 5362.5}, {'customer': 'VALUE LIGHTING-CARROLLTON, TX', 'revenue': 5332.0}, {'customer': 'CENTRAL ELECTRIC SUPPLY', 'revenue': 5135.25}, {'customer': 'FERGUSON-FROSTPROOF, FL', 'revenue': 4588.5}, {'customer': 'APCO, INC.', 'revenue': 3560.0}, {'customer': 'FERGUSON-WATERLOO, IA', 'revenue': 3539.7}, {'customer': 'FERGUSON- CHANDLER,AZ', 'revenue': 2927.9}, {'customer': 'VERMONT LIGHTING COMPANY', 'revenue': 2898.0}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 2890.0}, {'customer': 'FERGUSON-PERRIS, CA', 'revenue': 2753.1}, {'customer': 'LIGHT CONCERN', 'revenue': 2721.55}, {'customer': 'THE BRECHER CO.-LOUISVILLE', 'revenue': 2488.2}, {'customer': 'FERGUSON-BROOKSHIRE, TX', 'revenue': 2403.5}, {'customer': 'FERGUSON-KINGS MOUNTAIN, NC', 'revenue': 2272.4}, {'customer': 'MARCHAND ELECTRIC', 'revenue': 2254.0}, {'customer': 'FERGUSON-AURORA, CO', 'revenue': 2185.0}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 2022.25}, {'customer': 'WAREHOUSE-LIGHTING.COM', 'revenue': 1926.0}, {'customer': 'CED-BREMERTON, WA', 'revenue': 1840.0}, {'customer': 'FLUSHING LIGHTING FIXTURE CO.', 'revenue': 1798.0}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 1773.6}, {'customer': 'ELECTRICAL WHOLESALE DISTRIBUTORS', 'revenue': 1773.6}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 1334.0}, {'customer': 'FERGUSON-LEBANON, TN', 'revenue': 1311.0}, {'customer': 'NORTH COAST LIGHTING', 'revenue': 1294.92}, {'customer': 'FERGUSON-SECAUCUS, NJ', 'revenue': 1223.6}, {'customer': 'DECO LUMINAIRE', 'revenue': 1153.35}, {'customer': 'LOGIQ MODERN SUPPLY', 'revenue': 1035.0}, {'customer': 'DECOR LIGHTING-AUBURN', 'revenue': 1032.0}, {'customer': 'BAY LIGHTING', 'revenue': 920.0}, {'customer': 'RAINBOW LIGHTING', 'revenue': 557.4}, {'customer': 'FELDMAN BROTHERS ELECTRICAL', 'revenue': 552.0}, {'customer': 'M & M LIGHTING-HOUSTON', 'revenue': 552.0}, {'customer': 'CED-TWIN STATE-WILLISTON, VT', 'revenue': 552.0}, {'customer': 'OCEAN PACIFIC LIGHTING INC.', 'revenue': 552.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 480.6}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 441.15}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 414.0}, {'customer': 'AZTEC LIGHTING', 'revenue': 374.5}, {'customer': 'FERGUSON-SAN ANTONIO, TX', 'revenue': 349.6}, {'customer': 'PREMIER LIGHTING-PHOENIX, AZ', 'revenue': 349.6}, {'customer': 'WAYFAIR LLC', 'revenue': 322.8}, {'customer': 'LOWES COMPANIES', 'revenue': 278.18}, {'customer': 'VALUE LIGHTING, INC.', 'revenue': 276.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 234.9}, {'customer': 'THE OLDE PARSONAGE', 'revenue': 221.0}, {'customer': 'CED-EVERETT, WA', 'revenue': 215.0}, {'customer': 'LIGHTSTYLE', 'revenue': 215.0}, {'customer': 'LAMPS PLUS', 'revenue': 214.9}, {'customer': 'LUMINAIRE EXPERT', 'revenue': 209.7}, {'customer': 'WILLCALL FOR LIGHT CONCERN', 'revenue': 206.7}, {'customer': 'LONESTAR ELECTRIC-GRAND PRAIRIE, TX', 'revenue': 186.5}, {'customer': 'CONCEPT LUMINAIRE, INC.', 'revenue': 174.75}, {'customer': 'DECOR LIGHTING', 'revenue': 172.0}, {'customer': 'CLEVELAND LIGHTING ONE', 'revenue': 167.32}, {'customer': 'CARRINGTON LIGHTING.COM', 'revenue': 152.2}, {'customer': 'ELLIOTT ELECTRIC SUPPLY', 'revenue': 138.0}, {'customer': 'SOLTERRA LIGHTING', 'revenue': 138.0}, {'customer': 'CRESCENT LIGHTING SUPPLY-OLYMPIA,WA', 'revenue': 138.0}, {'customer': 'BUILDERS LIGHTING-BOISE', 'revenue': 138.0}, {'customer': 'BUILDER FINISH PRODUCTS', 'revenue': 129.0}, {'customer': 'PACE LIGHTING', 'revenue': 129.0}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 123.4}, {'customer': 'FERGUSON-SUMNER, WA', 'revenue': 110.91}, {'customer': "GARBE'S LIGHTING & HARDWARE", 'revenue': 104.85}, {'customer': 'WILLCALL FOR LIGHTSTYLES', 'revenue': 104.82}, {'customer': 'GROSS LIGHTING-TOLEDO, OH', 'revenue': 92.0}, {'customer': 'HOME CONCEPT', 'revenue': 92.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 92.0}, {'customer': "STAFFORD'S LIGHTING CO.,INC", 'revenue': 92.0}, {'customer': 'CONTINENTAL LIGHTING', 'revenue': 92.0}, {'customer': 'CENTRAL BUILDERS SUPPLY COURTENAY', 'revenue': 92.0}, {'customer': 'MUSKA LIGHTING CENTER-ROSEVILLE, MN', 'revenue': 92.0}, {'customer': 'STATEWIDE LIGHTING  INC.', 'revenue': 87.4}, {'customer': 'FERGUSON-LUBBOCK, TX', 'revenue': 87.4}, {'customer': 'FERGUSON-CALEDONIA, MI', 'revenue': 87.4}, {'customer': 'FERGUSON-HOLLY SPRINGS, NC', 'revenue': 87.4}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 87.4}, {'customer': 'LIGHTSTYLE OF TAMPA BAY', 'revenue': 82.8}, {'customer': 'FERGUSON-CLEVELAND, TN', 'revenue': 81.7}, {'customer': 'ALAMEDA ELECTRICAL DISTRIBUTORS', 'revenue': 73.1}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 71.94}, {'customer': 'BOUTIQUE LUMINAIRE PLUS-GRANBY', 'revenue': 69.9}, {'customer': 'TAZZ LIGHTING, INC.', 'revenue': 46.0}, {'customer': 'THE LIGHTING CORNER', 'revenue': 46.0}, {'customer': 'DHILLON LIGHTING INC.', 'revenue': 46.0}, {'customer': 'QED/GALLERIA LIGHTING-AURORA, CO', 'revenue': 46.0}, {'customer': 'STATE ELECTRIC-HUNTINGTON, WV', 'revenue': 46.0}, {'customer': 'RAINBOW LIGHTING', 'revenue': 46.0}, {'customer': 'COLONIAL ELECTRIC SUPPLY', 'revenue': 46.0}, {'customer': 'COAST LIGHTING', 'revenue': 46.0}, {'customer': 'CITY LIGHTS', 'revenue': 46.0}, {'customer': "AARON'S SUPPLY INC.-LITTLE RIVER", 'revenue': 46.0}, {'customer': 'CASA DI LUCE', 'revenue': 46.0}, {'customer': 'INLINE ELECTRIC SUPPLY-AUBURN', 'revenue': 46.0}, {'customer': 'LIGHTSTYLES', 'revenue': 43.7}, {'customer': 'PLUMBING DISTRIBUTORS-EATONTON', 'revenue': 43.0}, {'customer': 'HARDWOOD SPECIALTIES, INC.', 'revenue': 43.0}, {'customer': 'REDEFINED LIGHTING LLC.', 'revenue': 34.97}, {'customer': 'DECO LUMINAIRE', 'revenue': 34.95}, {'customer': 'LUPARELLO & SONS LIGHTING CORP.', 'revenue': 32.95}, {'customer': 'ROYAUME LUMINAIRE JD INC', 'revenue': 18.4}, {'customer': 'ROYAUME DU LUMINAIRE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE DRUMMONDVILE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE LANAUDIERE', 'revenue': 18.4}, {'customer': 'LUMINAIRES & CIE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE BEAUPORT', 'revenue': 18.4}, {'customer': 'ECLAIRAGE RAYMOND INC.', 'revenue': 5.0}, {'customer': 'WA BRAGG-EVANS, GA', 'revenue': 0.0}] | [{'item': '52102BK', 'desc': 'Rail 24" LED Bath Vanity', 'available': 2493}, {'item': '52102PC', 'desc': 'Rail 24" LED Bath Vanity', 'available': 1278}, {'item': '52103SN', 'desc': 'Rail 30" LED Bath Vanity', 'available': 796}, {'item': '52100PC', 'desc': 'Rail 18" LED Bath Vanity', 'available': 547}, {'item': '52104SN', 'desc': 'Rail 36" LED Bath Vanity', 'available': 310}, {'item': '52104PC', 'desc': 'Rail 36" LED Bath Vanity', 'available': 264}, {'item': '52104BK', 'desc': 'Rail 36" LED Bath Vanity', 'available': 215}, {'item': '52100SN', 'desc': 'Rail 18" LED Bath Vanity', 'available': 201}, {'item': '52100BK', 'desc': 'Rail 18" LED Bath Vanity', 'available': 198}, {'item': '52103PC', 'desc': 'Rail 30" LED Bath Vanity', 'available': 168}, {'item': '52105SN', 'desc': 'Rail 48" LED Bath Vanity', 'available': 83}, {'item': '52132SN', 'desc': 'Rail 24" LED Bath Bar CCT Select', 'available': 66}, {'item': '52105PC', 'desc': 'Rail 48" LED Bath Vanity', 'available': 36}, {'item': '52103BK', 'desc': 'Rail 30" LED Bath Vanity', 'available': 9}, {'item': '52105BK', 'desc': 'Rail 48" LED Bath Vanity', 'available': 1}] |
| 57933WTWT | Diverse 13" LED Flush Mount 3000K | COL7 | 132,527.70 | 6,314 | — | 2026-06-26 | [{'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 58452.85}, {'customer': 'LIFESTYLES', 'revenue': 10014.1}, {'customer': 'REXEL USA, INC.-TEMPLE, TX', 'revenue': 8000.0}, {'customer': 'FERGUSON-OMAHA, NE', 'revenue': 6277.5}, {'customer': 'TRINITY WHOLESALE DIST-NEW HAVEN', 'revenue': 6264.05}, {'customer': 'LIGHTING ETC, INC', 'revenue': 5266.92}, {'customer': 'GEORGIA LIGHTING', 'revenue': 4788.0}, {'customer': 'REID LIGHTING CO. INC.', 'revenue': 3925.8}, {'customer': 'LEGACY LIGHTING LLC', 'revenue': 3791.95}, {'customer': 'FERGUSON-LINCOLN, NE', 'revenue': 3123.6}, {'customer': 'THE LIGHTING DESIGN, LLC', 'revenue': 2431.28}, {'customer': 'AVID LIGHTING, LLC', 'revenue': 2041.26}, {'customer': 'FERGUSON-OKLAHOMA CITY, OK', 'revenue': 1830.4}, {'customer': 'CLEVELAND LIGHTING ONE', 'revenue': 1487.12}, {'customer': 'FERGUSON-OKLAHOMA, OK', 'revenue': 1482.0}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 1240.2}, {'customer': 'KENNEWICK IND/DBA KIE SUPPLY', 'revenue': 1164.41}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 1082.0}, {'customer': 'CITY ELECTRIC SUPPLY-GARDEN CITY,GA', 'revenue': 1037.5}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 884.0}, {'customer': 'COLONIAL LIGHTING-DECATUR, GA', 'revenue': 786.25}, {'customer': 'WINSUPPLY OF N ST. GEORGE UT CO.', 'revenue': 780.0}, {'customer': "HAGEN'S LIGHTING-TYLER", 'revenue': 754.0}, {'customer': 'LITECRAFT LIGHTING-AUGUSTA, GA', 'revenue': 553.5}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 520.0}, {'customer': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'revenue': 500.4}, {'customer': 'CITY ELECTRIC SUPPLY-STATESBORO, GA', 'revenue': 498.0}, {'customer': 'FERGUSON-NEW HUDSON, MI', 'revenue': 496.65}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 439.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 436.8}, {'customer': 'LIGHT WORKS', 'revenue': 312.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 260.0}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 221.35}, {'customer': 'HILL COUNTRY LIGHTING CENTER', 'revenue': 130.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 117.0}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 104.0}, {'customer': 'ECHO GROUP INC.-DES MOINES, IA', 'revenue': 104.0}, {'customer': 'COBURN SUPPLY COMPANY-MOBILE, AL', 'revenue': 104.0}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 101.25}, {'customer': 'GROSS LIGHTING-INDIANAPOLIS,IN', 'revenue': 78.0}, {'customer': "FERGUSON-O'FALLON, MO", 'revenue': 74.1}, {'customer': 'FERGUSON-TULSA, OK', 'revenue': 74.1}, {'customer': 'LIGHTING SOUTH, LLC-FAIRLAWN, OH', 'revenue': 65.85}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 65.85}, {'customer': 'PLUMBING DISTRIBUTORS-ALPHARETTA', 'revenue': 52.0}, {'customer': 'PLUMBING DISTRIBUTORS-EATONTON', 'revenue': 52.0}, {'customer': 'WILSON LIGHTING', 'revenue': 52.0}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 49.4}, {'customer': 'LAMPS PLUS', 'revenue': 43.16}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 26.0}, {'customer': 'MEDINA LIGHTING, INC.', 'revenue': 25.0}, {'customer': 'DENALI LIGHTING LLC', 'revenue': 25.0}, {'customer': 'FERGUSON-FRESNO, CA', 'revenue': 22.15}, {'customer': 'ELECTRICAL WHOLESALE DISTRIBUTORS', 'revenue': 19.95}] | [{'item': '87411WTWT', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 25682}, {'item': '87645WTWT', 'desc': 'Diverse 7.5" LED Flush Mount - 5CCT', 'available': 24210}, {'item': '87643WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 13554}, {'item': '57633WTWT', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 8871}, {'item': '57413WTWT', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 7411}, {'item': '87415WTWT', 'desc': 'Diverse 6" LED Flush Mount 5CCT', 'available': 5998}, {'item': '87642WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 2700K', 'available': 4195}, {'item': '87643WTBZ', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 3750}, {'item': '57641WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 2700K', 'available': 2541}, {'item': '57613WTSN', 'desc': 'Diverse 7.5" LED Flush Mount 3000K Non-T24', 'available': 1527}, {'item': '87643WTSN', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 1523}, {'item': '57933WTBK', 'desc': 'Diverse 13" LED Flush Mount 3000K', 'available': 858}, {'item': '57631WTWT', 'desc': 'Diverse 6.25" LED Flush Mount 2700K', 'available': 647}, {'item': '57935WTWT', 'desc': 'Diverse 13" LED Flush Mount 5CCT', 'available': 637}, {'item': '57414WTWT', 'desc': 'Diverse 6" LED Flush Mount 4000K', 'available': 630}, {'item': '57913WTBZ', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 465}, {'item': '57853WTWT', 'desc': 'Diverse 9" LED Flush Mount 4000K', 'available': 451}, {'item': '87643WTBK', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 430}, {'item': '57413WTBK', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 373}, {'item': '57647WTSN', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 352}, {'item': '57412WTWT', 'desc': 'Diverse 6" LED Flush Mount 2700K', 'available': 257}, {'item': '57935WTSN', 'desc': 'Diverse 13" LED Flush Mount 5CCT', 'available': 231}, {'item': '57932WTWT', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 219}, {'item': '57931WTBK', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 197}, {'item': '57923WTBK', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 194}, {'item': '57856WTWT', 'desc': 'Diverse 11" LED Flush Mount 2700K', 'available': 162}, {'item': '57858WTWT', 'desc': 'Diverse 11" LED Flush Mount 4000K', 'available': 150}, {'item': '57933WTSN', 'desc': 'Diverse 13" LED Flush Mount 3000K', 'available': 136}, {'item': '57861WTWT', 'desc': 'Diverse 13" LED Flush Mount 2700K', 'available': 135}, {'item': '57932WTBK', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 128}, {'item': '57933WTBZ', 'desc': 'Diverse 13" LED Flush Mount 3000K', 'available': 117}, {'item': '57925WTWT', 'desc': 'Diverse 11" LED Flush Mount 5CCT', 'available': 101}, {'item': '57925WTSN', 'desc': 'Diverse 11" LED Flush Mount 5CCT', 'available': 96}, {'item': '57915WTSN', 'desc': 'Diverse 9" LED Flush Mount 5CCT', 'available': 90}, {'item': '57923WTSN', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 86}, {'item': '57913WTSN', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 83}, {'item': '57863WTWT', 'desc': 'Diverse 13" LED Flush Mount 4000K', 'available': 49}, {'item': '57855WTWT', 'desc': 'Diverse 11" LED Flush Mount 3000K Non-T24', 'available': 48}, {'item': '57855WTSN', 'desc': 'Diverse 11" LED Flush Mount 3000K Non-T24', 'available': 48}, {'item': '87644WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 4000K', 'available': 32}, {'item': '57851WTWT', 'desc': 'Diverse 9" LED Flush Mount 2700K', 'available': 20}, {'item': '57855WTBK', 'desc': 'Diverse 11" LED Flush Mount 3000K Non-T24', 'available': 2}, {'item': '57913WTBK', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 2}] |
| 88707BK | Falcon Pull Chain 52" In/Outdoor Fan w LED Light | COL196 | 117,033.23 | 1,107 | — | — | [{'customer': 'ALL-PHASE ELECTRIC (CED)-INDY, IN', 'revenue': 69363.43}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 29290.8}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 3449.55}, {'customer': 'BARROW LIGHTING SUPPLY', 'revenue': 3078.6}, {'customer': 'ILLUMINATE LIGHTING-LISBON, IA', 'revenue': 2186.8}, {'customer': 'THE LOCAL LIGHTING SHOP', 'revenue': 1595.3}, {'customer': 'LONESTAR ELECTRIC SUPPLY', 'revenue': 852.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 852.0}, {'customer': 'CAPITAL ELECTRIC-UPPER MARLBORO, MD', 'revenue': 852.0}, {'customer': 'SUMMIT ELECTRIC SUPPLY-PHOENIX, AZ', 'revenue': 675.0}, {'customer': 'TEAM ELECTRIC SUPPLY', 'revenue': 568.0}, {'customer': 'ELLIOTT ELECTRIC SUPPLY-SPRINGDALE', 'revenue': 540.0}, {'customer': 'PLUMBING DISTRIBUTORS-LAWRENCEVILLE', 'revenue': 540.0}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 344.85}, {'customer': 'DANLAR, INC.-USESI', 'revenue': 284.0}, {'customer': 'CLINE-HOLDER ELECTRIC SUPPLY', 'revenue': 284.0}, {'customer': 'HOME & LIGHT VALDOSTA', 'revenue': 270.5}, {'customer': 'LIGHT BRITE DISTRIBUTING-TRENTON', 'revenue': 261.09}, {'customer': 'CED ALL-PHASE ELECTRIC SUPPLY', 'revenue': 205.9}, {'customer': 'LEE SUPPLY CORP.-DAYTON, OH', 'revenue': 142.0}, {'customer': 'LIGHT & DAY', 'revenue': 142.0}, {'customer': 'LEE SUPPLY CORP.- FORT WAYNE, IN', 'revenue': 142.0}, {'customer': 'KNOXVILLE NOLAND CO.-KNOXVILLE, TN', 'revenue': 142.0}, {'customer': 'PLUMBING DISTRIBUTORS-ALPHARETTA', 'revenue': 135.0}, {'customer': 'BUILDERS LIGHTING & DESIGN, INC', 'revenue': 135.0}, {'customer': 'LAMPS.COM', 'revenue': 134.9}, {'customer': 'PARK LIGHTING', 'revenue': 121.5}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 120.7}, {'customer': 'LAMPS PLUS', 'revenue': 117.86}, {'customer': 'WALTERS WHOLESALE ELECTRIC-BREA', 'revenue': 106.5}, {'customer': 'SHOOK ELECTRICAL SUPPLY-CONYERS, GA', 'revenue': 99.95}, {'customer': 'ELFORD TEIBER & COMPANY', 'revenue': 0.0}] | [{'item': '88707SN', 'desc': 'Falcon Pull Chain 52" In/Outdoor Fan w LED Light', 'available': 636}] |
| 88708SN | Falcon AC Damp 52" In/Out Fan w LED Light Kit | COL198 | 101,340.37 | 771 | — | 2026-06-26 | [{'customer': 'MAYER ELECTRIC SUPPLY-GREENSBORO,NC', 'revenue': 91906.42}, {'customer': 'KING ELECTRIC CO.', 'revenue': 3598.5}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 1395.0}, {'customer': 'DON DALTON COMPANY', 'revenue': 1059.5}, {'customer': 'KING ELECTRIC CO. INC.-BURLINGTON', 'revenue': 839.65}, {'customer': 'NORTHSIDE WAREHOUSE-TUCSON, AZ', 'revenue': 438.9}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 412.18}, {'customer': 'PARAMONT-EO INC.-CHICAGO', 'revenue': 308.0}, {'customer': 'LAMPS PLUS', 'revenue': 245.68}, {'customer': 'LONESTAR ELECTRIC SUPPLY-MANOR, TX', 'revenue': 154.0}, {'customer': 'THE LOCAL LIGHTING SHOP', 'revenue': 154.0}, {'customer': 'CRESCENT LIGHTING SUPPLY-OLYMPIA,WA', 'revenue': 154.0}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 146.3}, {'customer': 'UNION LIGHTING', 'revenue': 146.3}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 130.9}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 129.09}, {'customer': 'IMAGINE MORE', 'revenue': 121.95}] | — |
| 61018GS | Odeon 8-Light WiFi-enabled LED Fandelight | ODEON | 100,438.34 | 82 | — | 2026-06-19 | [{'customer': 'SHALLOTTE ELECTRIC & PLUMBING', 'revenue': 5396.0}, {'customer': 'VALLEY LIGHT GALLERY', 'revenue': 3642.3}, {'customer': 'LAMPS PLUS', 'revenue': 3156.66}, {'customer': 'LOWES COMPANIES', 'revenue': 3039.66}, {'customer': 'PREMIER LIGHTING', 'revenue': 2698.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 2347.26}, {'customer': 'GALLERIA LIGHTING', 'revenue': 2345.84}, {'customer': 'WAYFAIR LLC', 'revenue': 2178.64}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 1349.0}, {'customer': 'UNIVERSAL LIGHTS  INC.', 'revenue': 1349.0}, {'customer': 'ATLANTA CEILING FANS', 'revenue': 1349.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 1349.0}, {'customer': 'BULB BIN INC.', 'revenue': 1349.0}, {'customer': 'CAPE ELECTRIC-CAPE GIRARDEAU, MO', 'revenue': 1349.0}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 1349.0}, {'customer': "BRADY'S DESIGN CENTER-LAWTON, OK", 'revenue': 1349.0}, {'customer': 'COMPLETE LIGHTING OF TAMPA', 'revenue': 1349.0}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 1349.0}, {'customer': 'GRAND RAPIDS LIGHTING CENTER', 'revenue': 1349.0}, {'customer': 'GROSS LIGHTING-INDIANAPOLIS,IN', 'revenue': 1349.0}, {'customer': 'HERALD WHOLESALE  INC.', 'revenue': 1349.0}, {'customer': 'INLINE ELECTRIC SUPPLY-CHATTANOOGA', 'revenue': 1349.0}, {'customer': 'INLINE ELECTRIC SUPPLY-HUNTSVILLE', 'revenue': 1349.0}, {'customer': 'KENDALL ELECTRIC-FORT WAYNE, IN', 'revenue': 1349.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 1349.0}, {'customer': 'LIFESTYLES', 'revenue': 1349.0}, {'customer': 'LIGHTING STAR', 'revenue': 1349.0}, {'customer': 'LIGHTING ETC, INC', 'revenue': 1349.0}, {'customer': 'LYONS ELECTRIC SUPPLY', 'revenue': 1349.0}, {'customer': 'LYTEWORKS, INC.', 'revenue': 1349.0}, {'customer': 'MANTECA LIGHTING', 'revenue': 1349.0}, {'customer': 'MAYSON ENTERPRISE', 'revenue': 1349.0}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 1349.0}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 1349.0}, {'customer': 'SISTERS LIGHTING', 'revenue': 1349.0}, {'customer': 'URBAN LIGHTS-DENVER, CO', 'revenue': 1349.0}, {'customer': 'VERSALLIES', 'revenue': 1349.0}, {'customer': 'VILLAGE HOME STORES, INC.', 'revenue': 1349.0}, {'customer': 'WEST COAST CABINETS CLOSETS & FLOOR', 'revenue': 1349.0}, {'customer': 'J&G ELECTRIC', 'revenue': 1349.0}, {'customer': 'UNION LIGHTING', 'revenue': 1281.55}, {'customer': 'BEAUTIFUL THINGS', 'revenue': 1281.55}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY INC.', 'revenue': 1281.55}, {'customer': 'LBU LIGHTING PORT ST. LUCIE', 'revenue': 1281.55}, {'customer': 'FERGUSON-SHARONVILLE, OH', 'revenue': 1281.55}, {'customer': 'LIGHTING FIRST', 'revenue': 1281.55}, {'customer': 'LBU LIGHTING PINECREST', 'revenue': 1281.55}, {'customer': 'FERGUSON-ALPHARETTA, GA', 'revenue': 1281.55}, {'customer': 'FERGUSON-ROUND ROCK, TX', 'revenue': 1281.55}, {'customer': 'CLEVELAND LIGHTING ONE', 'revenue': 1268.06}, {'customer': 'LIGHTOLOGY', 'revenue': 1247.83}, {'customer': 'LIGHTSTYLE OF TAMPA BAY', 'revenue': 1214.1}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 1214.1}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 1214.1}, {'customer': 'FRANKLIN LIGHTING', 'revenue': 1214.1}, {'customer': 'LIGHTING, INC. OFFICE-HOUSTON', 'revenue': 1214.1}, {'customer': 'LIGHTING, INC. OFFICE-SAN ANTONIO', 'revenue': 1214.1}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 1214.1}, {'customer': "AARON'S SUPPLY INC.-LITTLE RIVER", 'revenue': 1199.09}, {'customer': 'HOBRECHT LIGHTING', 'revenue': 1199.09}, {'customer': 'NAPLES LIGHTING & FAN DEPOT INC.', 'revenue': 1199.09}, {'customer': 'PROGRESSIVE LIGHTING-ROSWELL, GA', 'revenue': 1187.12}, {'customer': 'GALLERIA LIGHTING', 'revenue': 1146.75}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 1146.65}, {'customer': 'LAMPS PLUS', 'revenue': 1119.67}, {'customer': 'CAPITOL LIGHTING-BOCA RATON', 'revenue': 1079.2}, {'customer': 'LIGHTING WORLD-STATEN ISLAND, NY', 'revenue': 640.78}, {'customer': 'LITTMAN BROTHERS', 'revenue': 0.0}, {'customer': 'MI CASA LIGHTING', 'revenue': 0.0}] | [{'item': '21866BCBK', 'desc': 'Odeon 6-Light Chandelier', 'available': 27}, {'item': '21869BCGS', 'desc': 'Odeon 10-Light Chandelier', 'available': 23}, {'item': '21866BCGS', 'desc': 'Odeon 6-Light Chandelier', 'available': 21}, {'item': '21869BCBK', 'desc': 'Odeon 10-Light Chandelier', 'available': 16}, {'item': '61018BK', 'desc': 'Odeon 8-Light WiFi-enabled LED Fandelight', 'available': 15}] |
| 12262CDBK | Acadia 2-Light Bath Vanity | COL8 | 98,559.11 | 3,377 | — | 2026-06-29 | [{'customer': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'revenue': 12415.68}, {'customer': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'revenue': 8876.8}, {'customer': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'revenue': 8478.3}, {'customer': 'COLONIAL LIGHTING-DECATUR, GA', 'revenue': 6259.75}, {'customer': 'COBURN SUPPLY COMPANY-MOBILE, AL', 'revenue': 4355.18}, {'customer': 'INLINE ELECTRIC SUPPLY-HUNTSVILLE', 'revenue': 3800.38}, {'customer': 'LONESTAR ELECTRIC SUPPLY-MANOR, TX', 'revenue': 3522.98}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 3297.0}, {'customer': 'WA BRAGG-WARNER ROBINS', 'revenue': 3134.62}, {'customer': 'PLUMBING DISTRIBUTORS-LAWRENCEVILLE', 'revenue': 2995.92}, {'customer': 'FERGUSON-LEBANON, TN', 'revenue': 2812.0}, {'customer': 'PDI-COVINGTON DC', 'revenue': 2385.64}, {'customer': 'HUBBARD PIPE & SUPPLY-WILMINGTON', 'revenue': 2299.2}, {'customer': 'PLUMBING DISTRIBUTORS-WOODSTOCK', 'revenue': 2286.94}, {'customer': 'HUBBARD PIPE & SUPPLY-GARNER, NC', 'revenue': 2239.2}, {'customer': 'ALL-PHASE ELECTRIC-GULFPORT, MS', 'revenue': 1914.06}, {'customer': 'RICHARDS LIGHTING', 'revenue': 1773.99}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 1741.96}, {'customer': 'INLINE ELECTRIC SUPPLY-PELHAM', 'revenue': 1692.14}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 1498.7}, {'customer': 'FROMM ELECTRIC', 'revenue': 1298.5}, {'customer': 'NORTH COAST LIGHTING-PORTLAND, OR', 'revenue': 1120.98}, {'customer': 'FERGUSON-GREENVILLE, SC', 'revenue': 1007.68}, {'customer': 'FERGUSON-RICHMOND, VA', 'revenue': 999.2}, {'customer': 'MATHES OF ALABAMA-DAPHNE', 'revenue': 998.64}, {'customer': 'HEARTH AND HOME, INC.', 'revenue': 898.5}, {'customer': 'THE HOME CENTER, INC', 'revenue': 875.3}, {'customer': 'AMERICAN LIGHTING', 'revenue': 873.1}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 723.75}, {'customer': 'ACTIVE ELECTRICAL SUPPLY CO.', 'revenue': 680.0}, {'customer': 'STOKES LIGHTING CENTER-KNOXVILLE', 'revenue': 599.0}, {'customer': 'COFFMAN HOME DECOR-ELKTON', 'revenue': 575.1}, {'customer': 'PLUMBING DISTRIBUTORS-MCDONOUGH', 'revenue': 554.8}, {'customer': 'LIGHTING CONCEPTS, LLC', 'revenue': 520.0}, {'customer': 'LEE SUPPLY CORP.', 'revenue': 459.84}, {'customer': 'TURNEY LIGHTING & ELECTRIC', 'revenue': 383.4}, {'customer': 'FERGUSON-LOUISVILLE, KY', 'revenue': 380.0}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 360.0}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 344.88}, {'customer': "SETH'S LIGHTING", 'revenue': 340.45}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 320.0}, {'customer': 'CAPITAL CITY DESIGN CENTER, INC.', 'revenue': 319.5}, {'customer': 'CAPITAL ELECTRIC-UPPER MARLBORO, MD', 'revenue': 280.0}, {'customer': 'KBL DESIGN CENTER, INC.', 'revenue': 266.0}, {'customer': 'SIGNATURE LIGHTING & FANS', 'revenue': 240.0}, {'customer': 'THE OLDE PARSONAGE', 'revenue': 240.0}, {'customer': 'AMERICAN LIGHTING-JOHNSON CITY', 'revenue': 204.42}, {'customer': 'FRANKLIN LIGHTING CENTER', 'revenue': 200.0}, {'customer': 'DEALERS LIGHTING-BRYAN, TX', 'revenue': 191.7}, {'customer': 'ROBINSON LIGHTING-PLYMOUTH, MN', 'revenue': 190.0}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 180.0}, {'customer': 'PLANK & TILE', 'revenue': 173.7}, {'customer': 'WINSUPPLY HENDERSONVILLE TN CO.', 'revenue': 160.0}, {'customer': 'YALE ELECTRIC-LANCASTER, PA', 'revenue': 160.0}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 123.45}, {'customer': 'CROWN ELECTRIC SUPPLY-ONTARIO', 'revenue': 120.0}, {'customer': 'CITY ELECTRIC SUPPLY-YOUNG HARRIS', 'revenue': 120.0}, {'customer': 'THE BETTER LIVING STORE', 'revenue': 120.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 120.0}, {'customer': 'CARRINGTON LIGHTING.COM', 'revenue': 120.0}, {'customer': 'PC BUILDING MATERIALS, INC.', 'revenue': 120.0}, {'customer': 'FERGUSON-AURORA, CO', 'revenue': 114.0}, {'customer': 'TRINITY WHOLESALE DIST-NEW HAVEN', 'revenue': 103.9}, {'customer': 'LAMPS PLUS', 'revenue': 99.6}, {'customer': 'HANSEN LIGHTING, INC.-LINDON, UT', 'revenue': 98.85}, {'customer': 'BONAIRE LIGHTING SOLUTIONS', 'revenue': 95.85}, {'customer': 'LIGHTING ETC, INC', 'revenue': 88.05}, {'customer': 'BRIGHT CITY LIGHTS', 'revenue': 80.0}, {'customer': 'SPECTRUM LIGHTING', 'revenue': 80.0}, {'customer': 'MAGNOLIA LIGHTING-HERNANDO', 'revenue': 80.0}, {'customer': 'COASTAL LIGHTING LLC.', 'revenue': 80.0}, {'customer': 'J.D. LIGHTING', 'revenue': 80.0}, {'customer': 'PALMER ELECTRIC COMPANY', 'revenue': 76.14}, {'customer': 'FERGUSON-LUBBOCK, TX', 'revenue': 76.0}, {'customer': 'FERGUSON-MIDLOTHIAN, VA', 'revenue': 76.0}, {'customer': 'FERGUSON-BLACKSBURG, VA', 'revenue': 76.0}, {'customer': 'ONE SOURCE LIGHTING', 'revenue': 74.34}, {'customer': 'CITY LIGHTZ', 'revenue': 74.0}, {'customer': 'PROGRESSIVE LIGHTING-CHARLOTTE, NC', 'revenue': 70.4}, {'customer': 'PROGRESSIVE LIGHTING-ROSWELL, GA', 'revenue': 70.4}, {'customer': 'FERGUSON-METAIRIE, LA', 'revenue': 69.95}, {'customer': 'REXEL USA, INC.-ORLANDO, FL', 'revenue': 67.9}, {'customer': 'A&A LIGHTING LLC', 'revenue': 59.9}, {'customer': 'INLINE ELECTRIC SUPPLY-MONTGOMERY', 'revenue': 55.48}, {'customer': 'EAST COAST LUMBER BUILDING SUPPLY', 'revenue': 40.0}, {'customer': 'MAYER ELECTRIC SUPPLY-DOTHAN, AL', 'revenue': 40.0}, {'customer': 'MINNESOTA LTG. FIREPLACE & FLOORING', 'revenue': 40.0}, {'customer': 'GATEWAY LIGHTING & DESIGN INC.', 'revenue': 40.0}, {'customer': 'BOWLING GREEN WINLECTRIC CO.', 'revenue': 40.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 40.0}, {'customer': 'ALL-PHASE ELECTRIC-GRAND JUNCTION', 'revenue': 40.0}, {'customer': 'GRAHAM LIGHTING-MEMPHIS', 'revenue': 40.0}, {'customer': 'FERGUSON-PENSACOLA, FL', 'revenue': 38.0}, {'customer': 'MULTI LUMINAIRE', 'revenue': 38.0}, {'customer': 'THE LIGHTING SHOPPE', 'revenue': 38.0}, {'customer': 'FERGUSON-KNOXVILLE, TN', 'revenue': 38.0}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 38.0}, {'customer': 'FERGUSON-TULSA, OK', 'revenue': 38.0}, {'customer': 'SUNBELT FANS & LIGHTING-LAFAYETTE', 'revenue': 38.0}, {'customer': 'UNION LIGHTING', 'revenue': 38.0}, {'customer': 'FERGUSON-MANDEVILLE, LA', 'revenue': 38.0}, {'customer': 'CONNECTICUT LIGHTING CENTE', 'revenue': 34.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 33.97}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 31.95}, {'customer': 'ALLOWAY LIGHTING', 'revenue': 30.95}, {'customer': 'THE LOCAL LIGHTING SHOP', 'revenue': 30.95}, {'customer': "DESIGNER'S MART", 'revenue': 30.85}, {'customer': 'SHOWCASE LIGHTING BY 3-G, LTD', 'revenue': 29.95}, {'customer': 'LOWES COMPANIES', 'revenue': 28.92}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 28.74}, {'customer': 'INLINE ELECTRIC SUPPLY-CLEVELAND,TN', 'revenue': 27.74}, {'customer': 'DANLAR, INC.-USESI-TUCKER, GA', 'revenue': 0.0}, {'customer': 'PLUMBING DISTRIBUTORS-SPARTANBURG', 'revenue': 0.0}] | [{'item': '12263CDSN', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 925}, {'item': '12263CDHR', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 796}, {'item': '12263CDBK', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 743}, {'item': '91260CDBK', 'desc': 'Acadia 1-Light Pendant', 'available': 364}, {'item': '12262CDSN', 'desc': 'Acadia 2-Light Bath Vanity', 'available': 360}, {'item': '12271CDBK', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 278}, {'item': '12273CDHR', 'desc': 'Acadia 3-Light Pendant', 'available': 222}, {'item': '12266CDBK', 'desc': 'Acadia 5-Light Chandelier', 'available': 201}, {'item': '12264CDSN', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 171}, {'item': '12273CDBK', 'desc': 'Acadia 3-Light Pendant', 'available': 164}, {'item': '12266CDHR', 'desc': 'Acadia 5-Light Chandelier', 'available': 117}, {'item': '91260CDNAB', 'desc': 'Acadia 1-Light Pendant', 'available': 99}, {'item': '91260CDHR', 'desc': 'Acadia 1-Light Pendant', 'available': 97}, {'item': '12264CDHR', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 96}, {'item': '12277CDSN', 'desc': 'Acadia 9-Light Chandelier', 'available': 85}, {'item': '12261CDBK', 'desc': 'Acadia 1-Light Wall Sconce', 'available': 78}, {'item': '12273CDNAB', 'desc': 'Acadia 3-Light Pendant', 'available': 75}, {'item': '12270CDNAB', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 75}, {'item': '12268CDNAB', 'desc': 'Acadia 8-Light Chandelier', 'available': 75}, {'item': '12261CDNAB', 'desc': 'Acadia 1-Light Wall Sconce', 'available': 75}, {'item': '12260CDNAB', 'desc': 'Acadia 3-Light Semi-Flush Mount/Chandelier', 'available': 75}, {'item': '12264CDNAB', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 73}, {'item': '12266CDSN', 'desc': 'Acadia 5-Light Chandelier', 'available': 73}, {'item': '12266CDNAB', 'desc': 'Acadia 5-Light Chandelier', 'available': 73}, {'item': '12277CDNAB', 'desc': 'Acadia 9-Light Chandelier', 'available': 72}, {'item': '12262CDNAB', 'desc': 'Acadia 2-Light Bath Vanity', 'available': 70}, {'item': '12271CDNAB', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 69}, {'item': '12263CDNAB', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 59}, {'item': '12264CDBK', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 58}, {'item': '12260CDSN', 'desc': 'Acadia 3-Light Semi-Flush Mount/Chandelier', 'available': 47}, {'item': '12271CDSN', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 36}, {'item': '12270CDSN', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 35}, {'item': '12270CDBK', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 35}, {'item': '12277CDBK', 'desc': 'Acadia 9-Light Chandelier', 'available': 30}, {'item': '12262CDHR', 'desc': 'Acadia 2-Light Bath Vanity', 'available': 28}, {'item': '12260CDBK', 'desc': 'Acadia 3-Light Semi-Flush Mount/Chandelier', 'available': 24}, {'item': '12268CDBK', 'desc': 'Acadia 8-Light Chandelier', 'available': 11}, {'item': '12270CDHR', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 10}, {'item': '12268CDSN', 'desc': 'Acadia 8-Light Chandelier', 'available': 9}, {'item': '12273CDSN', 'desc': 'Acadia 3-Light Pendant', 'available': 8}, {'item': '12268CDHR', 'desc': 'Acadia 8-Light Chandelier', 'available': 3}, {'item': '12271CDHR', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 3}] |
| E25052-CHK | Souffle 8.5" 1-Light Pendant | COL287 | 98,083.03 | 1,746 | — | 2026-06-19 | [{'customer': 'LUMISOLUTION INC.', 'revenue': 35421.58}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 14163.8}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 13087.61}, {'customer': 'LIGHTOLOGY', 'revenue': 5235.45}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 4285.7}, {'customer': 'WAYFAIR LLC', 'revenue': 2091.96}, {'customer': 'TRANSIT LUMINAIRES', 'revenue': 1985.5}, {'customer': 'FUSION LIGHT & DESIGN', 'revenue': 1518.0}, {'customer': 'ESPACE LUMI DECOR INC.', 'revenue': 1382.0}, {'customer': 'JOSS AND MAIN-BOSTON', 'revenue': 1108.2}, {'customer': 'NORTHGLENN WINLECTRIC CO.', 'revenue': 990.0}, {'customer': 'DECO LUMINAIRE', 'revenue': 920.75}, {'customer': 'LUMINAIRES & CIE', 'revenue': 824.1}, {'customer': 'CASA DI LUCE', 'revenue': 770.1}, {'customer': 'NORBURN  LIGHTING & BATH-BURNABY', 'revenue': 671.5}, {'customer': 'PARK LIGHTING', 'revenue': 642.6}, {'customer': 'LAMPS PLUS', 'revenue': 592.04}, {'customer': 'CONCEPT LUMINAIRE, INC.', 'revenue': 568.3}, {'customer': 'LIGHTING ETC, INC', 'revenue': 528.0}, {'customer': 'UNION LIGHTING', 'revenue': 493.8}, {'customer': 'DECO LUMINAIRE', 'revenue': 473.4}, {'customer': 'DECO LUMINAIRE TERREBONNE', 'revenue': 454.55}, {'customer': 'POWER SHINE LIGHTING-BROOKLYN, NY', 'revenue': 446.0}, {'customer': 'CASA DI LUCE', 'revenue': 396.0}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 384.0}, {'customer': 'LUMINAIRE REPENTIGNY', 'revenue': 381.5}, {'customer': 'LUMINAIRE ALDER INC.', 'revenue': 363.65}, {'customer': 'CITY LIGHTS', 'revenue': 330.0}, {'customer': 'MULTI LUMINAIRE', 'revenue': 318.5}, {'customer': 'LAMPS PLUS', 'revenue': 304.92}, {'customer': 'LAMPS.COM', 'revenue': 302.1}, {'customer': 'ROBINSON LIGHTING-WINNIPEG', 'revenue': 297.0}, {'customer': 'BOUTIQUE LUMINAIRE PLUS-GRANBY', 'revenue': 235.6}, {'customer': 'REXEL USA, INC. #989035', 'revenue': 232.5}, {'customer': 'LTG PROJECTS', 'revenue': 217.8}, {'customer': 'ROYAUME LUMINAIRE LANAUDIERE', 'revenue': 214.5}, {'customer': 'ROYAUME LUMINAIRE BEAUPORT', 'revenue': 203.1}, {'customer': 'ULTRA LIGHTING-MISSISSAUGA', 'revenue': 198.0}, {'customer': 'ELECTRIMAT-SAINT HUBERT, QC', 'revenue': 198.0}, {'customer': 'ECLAIRAGE RAYMOND INC.', 'revenue': 195.8}, {'customer': 'DULLES ELECTRIC & SUPPLY', 'revenue': 188.1}, {'customer': 'MULTI LUMINAIRE-QUEBEC', 'revenue': 188.1}, {'customer': 'THE LIGHT HOUSE', 'revenue': 186.0}, {'customer': 'ELM RIDGE LIGHTING & INTERIORS INC.', 'revenue': 178.2}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 178.2}, {'customer': 'SHADES OF LIGHT LLC', 'revenue': 176.88}, {'customer': 'ROBINSON LIGHTING-KELOWNA', 'revenue': 171.0}, {'customer': 'EDGES ELECTRICAL GROUP-SAN JOSE', 'revenue': 165.0}, {'customer': 'REDEFINED LIGHTING LLC.', 'revenue': 164.85}, {'customer': 'ECLAIRAGE ETC.', 'revenue': 155.85}, {'customer': "BEAULIEU DECOR D'ASTOUS ET FRERES", 'revenue': 146.85}, {'customer': 'LUMINAIRE EXPERT', 'revenue': 146.85}, {'customer': 'ROBINSON LIGHTING & BATH', 'revenue': 132.0}, {'customer': 'HYE LIGHTING', 'revenue': 132.0}, {'customer': 'PINE TREE LIGHTING-LAKE ORION', 'revenue': 132.0}, {'customer': 'RICHARDSON LIGHTING', 'revenue': 132.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 132.0}, {'customer': 'SYNERGY LIGHT STUDIO', 'revenue': 132.0}, {'customer': 'SUPERLITE', 'revenue': 132.0}, {'customer': 'LIGHTOPIA', 'revenue': 132.0}, {'customer': 'THE LIGHTING SHOPPE', 'revenue': 125.4}, {'customer': 'DHILLON LIGHTING CALGARY LTD.', 'revenue': 124.0}, {'customer': 'DESIGNER LIGHTING & FAN CENTER', 'revenue': 124.0}, {'customer': 'KENDALL ELECTRIC-FORT WAYNE, IN', 'revenue': 124.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 118.8}, {'customer': 'ROYAUME LUMINAIRE-SAINT JULIE', 'revenue': 117.8}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 114.84}, {'customer': 'THE LIGHTING WAREHOUSE', 'revenue': 111.6}, {'customer': 'LUMINAIRE NAPERT-ST. MARIE', 'revenue': 103.9}, {'customer': 'JANCO ELECTRIQUE', 'revenue': 103.9}, {'customer': 'STRUKTURA DESIGN INC.', 'revenue': 97.9}, {'customer': 'MASTERPIECE DISTRICT-ATLANTA', 'revenue': 92.4}, {'customer': 'ROYAUME DU LUMINAIRE', 'revenue': 82.5}, {'customer': 'UNION LIGHTING & FURNISHINGS', 'revenue': 62.7}, {'customer': 'ROYAUME LUMINAIRE DRUMMONDVILE', 'revenue': 26.4}, {'customer': 'PINE LIGHTING', 'revenue': 23.1}] | [{'item': 'E25050-CHK', 'desc': 'Souffle 10" LED Flush Mount', 'available': 817}, {'item': 'E25051-CHK', 'desc': 'Souffle 14" LED Flush Mount', 'available': 536}, {'item': 'E25050-TRC', 'desc': 'Souffle 10" LED Flush Mount', 'available': 318}, {'item': 'E25058-CHK', 'desc': 'Souffle 18" LED Flush Mount', 'available': 195}, {'item': 'E25058-TRC', 'desc': 'Souffle 18" LED Flush Mount', 'available': 168}, {'item': 'E25058-GY', 'desc': 'Souffle 18" LED Flush Mount', 'available': 143}, {'item': 'E25051-TRC', 'desc': 'Souffle 14" LED Flush Mount', 'available': 109}, {'item': 'E25059-TRC', 'desc': 'Souffle 22" LED Flush Mount', 'available': 88}, {'item': 'E25050-GY', 'desc': 'Souffle 10" LED Flush Mount', 'available': 88}, {'item': 'E25059-GY', 'desc': 'Souffle 22" LED Flush Mount', 'available': 86}, {'item': 'E25051-GY', 'desc': 'Souffle 14" LED Flush Mount', 'available': 57}, {'item': 'E25052-GY', 'desc': 'Souffle 8.5" 1-Light Pendant', 'available': 32}] |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| E20246-BBK | Arc 1-Light LED Table Lamp | ARC | 0 | 0 | — |
| BL9E26FT120V30-ES | 9W Dimmable LED E26 FT 3000K | BULBS | 0 | 0 | — |
| 57686CLFTPC | Illuminaire II 4.5"SQ LED Flush Mount 3000K | COL17 | 2 | 47.66 | — |
| FRD0212SN | 12" Down Rod, 89909, 993069 | COL2 | 0 | 0 | [{'customer_code': 'HUBFAYET-HUBCHA', 'customer_name': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'collection_revenue': 33299.1}, {'customer_code': 'Z3697469-CITCO2', 'customer_name': 'CITY ELECTRIC SUPPLY-CONCORD, NC', 'collection_revenue': 30123.6}, {'customer_code': 'HUBFAYET-HUBFAY', 'customer_name': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'collection_revenue': 26366.48}, {'customer_code': 'STABUR-', 'customer_name': "STAFFORD'S LIGHTING CO.,INC", 'collection_revenue': 16423.6}, {'customer_code': 'WALSIG-SHIP', 'customer_name': 'WALTERS WHOLESALE ELECTRIC-BREA', 'collection_revenue': 16371.2}, {'customer_code': 'FERHAM-FE1723', 'customer_name': 'FERGUSON-HOLLY SPRINGS, NC', 'collection_revenue': 14249.85}, {'customer_code': 'Z4334631-', 'customer_name': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'collection_revenue': 10388.8}] |
| FRD0218SN | 18" Down Rod, 89909, 993069 | COL2 | 0 | 0 | [{'customer_code': 'HUBFAYET-HUBCHA', 'customer_name': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'collection_revenue': 33299.1}, {'customer_code': 'Z3697469-CITCO2', 'customer_name': 'CITY ELECTRIC SUPPLY-CONCORD, NC', 'collection_revenue': 30123.6}, {'customer_code': 'HUBFAYET-HUBFAY', 'customer_name': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'collection_revenue': 26366.48}, {'customer_code': 'STABUR-', 'customer_name': "STAFFORD'S LIGHTING CO.,INC", 'collection_revenue': 16423.6}, {'customer_code': 'WALSIG-SHIP', 'customer_name': 'WALTERS WHOLESALE ELECTRIC-BREA', 'collection_revenue': 16371.2}, {'customer_code': 'FERHAM-FE1723', 'customer_name': 'FERGUSON-HOLLY SPRINGS, NC', 'collection_revenue': 14249.85}, {'customer_code': 'Z4334631-', 'customer_name': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'collection_revenue': 10388.8}] |
| FRD0236SN | 36" Down Rod, 89909, 993069 | COL2 | 0 | 0 | [{'customer_code': 'HUBFAYET-HUBCHA', 'customer_name': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'collection_revenue': 33299.1}, {'customer_code': 'Z3697469-CITCO2', 'customer_name': 'CITY ELECTRIC SUPPLY-CONCORD, NC', 'collection_revenue': 30123.6}, {'customer_code': 'HUBFAYET-HUBFAY', 'customer_name': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'collection_revenue': 26366.48}, {'customer_code': 'STABUR-', 'customer_name': "STAFFORD'S LIGHTING CO.,INC", 'collection_revenue': 16423.6}, {'customer_code': 'WALSIG-SHIP', 'customer_name': 'WALTERS WHOLESALE ELECTRIC-BREA', 'collection_revenue': 16371.2}, {'customer_code': 'FERHAM-FE1723', 'customer_name': 'FERGUSON-HOLLY SPRINGS, NC', 'collection_revenue': 14249.85}, {'customer_code': 'Z4334631-', 'customer_name': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'collection_revenue': 10388.8}] |
| FRD0248SN | 48" Down Rod, 89909, 993069 | COL2 | 0 | 0 | [{'customer_code': 'HUBFAYET-HUBCHA', 'customer_name': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'collection_revenue': 33299.1}, {'customer_code': 'Z3697469-CITCO2', 'customer_name': 'CITY ELECTRIC SUPPLY-CONCORD, NC', 'collection_revenue': 30123.6}, {'customer_code': 'HUBFAYET-HUBFAY', 'customer_name': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'collection_revenue': 26366.48}, {'customer_code': 'STABUR-', 'customer_name': "STAFFORD'S LIGHTING CO.,INC", 'collection_revenue': 16423.6}, {'customer_code': 'WALSIG-SHIP', 'customer_name': 'WALTERS WHOLESALE ELECTRIC-BREA', 'collection_revenue': 16371.2}, {'customer_code': 'FERHAM-FE1723', 'customer_name': 'FERGUSON-HOLLY SPRINGS, NC', 'collection_revenue': 14249.85}, {'customer_code': 'Z4334631-', 'customer_name': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'collection_revenue': 10388.8}] |
| GLSFKT211SW | Glass for 89908, FKT211, SW | COL2 | 0 | 0 | [{'customer_code': 'HUBFAYET-HUBCHA', 'customer_name': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'collection_revenue': 33299.1}, {'customer_code': 'Z3697469-CITCO2', 'customer_name': 'CITY ELECTRIC SUPPLY-CONCORD, NC', 'collection_revenue': 30123.6}, {'customer_code': 'HUBFAYET-HUBFAY', 'customer_name': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'collection_revenue': 26366.48}, {'customer_code': 'STABUR-', 'customer_name': "STAFFORD'S LIGHTING CO.,INC", 'collection_revenue': 16423.6}, {'customer_code': 'WALSIG-SHIP', 'customer_name': 'WALTERS WHOLESALE ELECTRIC-BREA', 'collection_revenue': 16371.2}, {'customer_code': 'FERHAM-FE1723', 'customer_name': 'FERGUSON-HOLLY SPRINGS, NC', 'collection_revenue': 14249.85}, {'customer_code': 'Z4334631-', 'customer_name': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'collection_revenue': 10388.8}] |
| ESHD21441-MG | Steel & Alumninum Shade for E21441-2,4, 4.5"x3.25" | COL590 | 0 | 0 | — |
| E71019-PC | Carlo LED Coffee Table | COL601 | 0 | 0 | — |
| E24862-PC | Victory LED Pendant | COL608 | 0 | 0 | — |
| E71001-PC | Victory LED Accent Table | COL608 | 0 | 0 | — |
| E71007-PC | Trapezoid LED Accent Table | COL616 | 0 | 0 | — |
| E23172-BKWT | Orbital 2-Light LED Wall Sconce | COL618 | 2 | 64.06 | — |
| E24745-130MW | Circuit 5-Light LED Pendant | COL621 | 0 | 0 | — |
| E31245-20PC | Quartz 6-Light LED Pendant | COL623 | 1 | 716.68 | — |
| E31246-20PC | Quartz 9-Light LED Pendant | COL623 | 0 | 0 | — |
| E31248-20PC | Quartz 12-Light LED Pendant | COL623 | 1 | 1,189.33 | — |
| E35001-MW | iCorona Friends of Hue LED Flush Mount | COL626 | 2 | 873.25 | — |
| E20642-61BK | Intersect LED Flush Mount | COL631 | 1 | 83.63 | — |
| E20646-61BK | Intersect LED Flush Mount | COL631 | 0 | 0 | — |
| E20443-BKPC | Ion 7-Light LED Pendant | ION | 0 | 0 | — |
| 25244WWDAB | Plank 5-Light Bath Vanity | PLANK | 0 | 0 | — |
| 25246WWDAB | Plank 6-Light Pendant | PLANK | 0 | 0 | — |
| E20594-BKGLD | Spire Large LED Pendant | SPIRE | 0 | 0 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
