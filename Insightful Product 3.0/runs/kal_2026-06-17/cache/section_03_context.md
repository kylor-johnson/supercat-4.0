# Section 3 Context Bundle — Kalco Lighting / Allegri Crystal (kal)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=10066, portal_order_gmv=$11.7M |
| HAS_INVENTORY | True | inventory_count=2267 |
| HAS_SALES_DATA | True | sales_data_count=50129 |
| HAS_SALES_SECTION | True | qualifying_reps=6 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$11.7M > ecat_gmv=$2.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 6 | 6 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 79 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 197, Mixpanel total submit_order (Q-01): 266 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=78.5%, ambiguous_rate=0.0%, showroom_event_share=13.8% |
| USER_GROUP_JOIN_RATE | 78% | 62 of 79 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 14% | showroom+admin share of matched events: 13.8% |
| ADMIN_REPS_IN_LEADERBOARD | True | 3 admin/showroom users in leaderboard: Bob Ross, Claudia Carrillo, Snehal Shah |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=42 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=818 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=400 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=49 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Kalco Lighting / Allegri Crystal
- **Shortname**: kal
- **Org ID**: 146
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Kalco Lighting / Allegri Crystal (kal, org_id=146)
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

# Signal Rank — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Run date**: 2026-06-17
- **Total signals fired**: 53 (P0: 38, P1: 13, P2: 2)
- **Org GMV**: $2.6M eCat LTM, $11.7M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $6.3M total business | P1 | §5 Team | 31.5 | $6,290,391 | 2.0 | 395,690,189 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — 505840OL/505851OL co-purchase pattern across 37 customers | P0 | §2/§3 | 3.7 | $9,098,327 | 2.0 | 67,327,623 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 14 non-enterprise accounts with $3.0M+ total business, zero eCat orders | P1 | §2 Accounts | 3.0 | $2,958,738 | 2.0 | 17,508,261 | POSITIVE |
| 4 | SIG-ANOMALY-02 | Stock Out — 519275WB (Flint 5 Light Multi-Drop Pendant) $583,128 LTM, 0 available | P0 | §3 Product | 10.0 | $583,128 | 3.0 | 17,493,825 | RISK |
| 5 | SIG-MOM-01 | Account Acceleration — CLIVE DANIEL HOME 2 consecutive QoQ acceleration quarters, $258,074 peak quarter (+597% QoQ) | P0 | §2 Accounts | 19.9 | $258,074 | 3.0 | 15,401,841 | POSITIVE |
| 6 | SIG-DECAY-04 | Spending Contraction — DOLAN NORTHWEST LLC  PORTLAND -77.1% YoY ($520,864→$119,130), $401,733 gap | P0 | §2 Accounts | 3.9 | $401,733 | 3.0 | 4,646,047 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 515155OL (Samal 21 Inch Pendant) $124,925 LTM, 0 available | P0 | §3 Product | 10.0 | $124,925 | 3.0 | 3,747,747 | RISK |
| 8 | SIG-MOM-01 | Account Acceleration — LUX LIGHTING LTD 2 consecutive QoQ acceleration quarters, $56,060 peak quarter (+651% QoQ) | P0 | §2 Accounts | 21.7 | $56,060 | 3.0 | 3,647,231 | POSITIVE |
| 9 | SIG-MOM-01 | Account Acceleration — Lighting Design Center 2 consecutive QoQ acceleration quarters, $48,568 peak quarter (+693% QoQ) | P0 | §2 Accounts | 23.1 | $48,568 | 3.0 | 3,367,705 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — VALLEY LGT GALLERY 3 consecutive QoQ acceleration quarters, $83,209 peak quarter (+331% QoQ) | P0 | §2 Accounts | 11.0 | $83,209 | 3.0 | 2,756,711 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — 030257-038 (Glacier 60 Inch LED Round Pendant) $90,966 LTM, 0 available | P0 | §3 Product | 10.0 | $90,966 | 3.0 | 2,728,986 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 519221WB (Flint 1 Light Led  Convertible Wall Scon) $86,699 LTM, 0 available | P0 | §3 Product | 10.0 | $86,699 | 3.0 | 2,600,974 | RISK |
| 13 | SIG-MOM-01 | Account Acceleration — SUNBELT FANS & LTG LAUREL 3 consecutive QoQ acceleration quarters, $29,018 peak quarter (+671% QoQ) | P0 | §2 Accounts | 22.4 | $29,018 | 3.0 | 1,946,261 | POSITIVE |
| 14 | SIG-ANOMALY-02 | Stock Out — 505820OL (Roxy 2 Light ADA Sconce) $63,294 LTM, 0 available | P0 | §3 Product | 10.0 | $63,294 | 3.0 | 1,898,819 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — 519276WB (Flint 3 Light Full Canopy Pendant) $61,716 LTM, 0 available | P0 | §3 Product | 10.0 | $61,716 | 3.0 | 1,851,473 | RISK |
| 16 | SIG-DECAY-01 | Reorder Decay — SPACIAL EFX 3.7x normal gap (111d vs 30d avg) | P0 | §2 Accounts | 3.7 | $152,319 | 3.0 | 1,690,741 | RISK |
| 17 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 61% of eCat GMV | P1 | §4 Commerce | 1.5 | $528,750 | 2.0 | 1,611,251 | RISK |
| 18 | SIG-DECAY-04 | Spending Contraction — SHADES OF LIGHT -50.9% YoY ($401,435→$197,145), $204,290 gap | P0 | §2 Accounts | 2.5 | $204,290 | 3.0 | 1,559,754 | RISK |
| 19 | SIG-COMMERCE-01 | Capture Rate — eCat captures 22.2% of $12M total business; each +1pt = $117K | P0 | §4 Commerce | 3.9 | $117,000 | 3.0 | 1,365,000 | POSITIVE |
| 20 | SIG-ANOMALY-02 | Stock Out — 520555OL (Crescent 6 Light Pendant) $45,102 LTM, 0 available | P0 | §3 Product | 10.0 | $45,102 | 3.0 | 1,353,064 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 29 | 1 | 0 | 30 | |
| §3 Product Intelligence | 8 | 0 | 1 | 9 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 1 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $6.3M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 505840OL/505851OL co-purchase pattern across 37 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 14 non-enterprise accounts with $3.0M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — CLIVE DANIEL HOME 2 consecutive QoQ acceleration quarters, $258,074 peak quarter (+597% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 519275WB (Flint 5 Light Multi-Drop Pendant) $583,128 LTM, 0 available
6. **[RISK]** SIG-DECAY-04: Spending Contraction — DOLAN NORTHWEST LLC  PORTLAND -77.1% YoY ($520,864→$119,130), $401,733 gap
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 515155OL (Samal 21 Inch Pendant) $124,925 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 2
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| hidden | 265 | 14 | 0 | 94.70 |
| visible | 2,268 | 179 | 0 | 92.10 |

### Q-37_results.md

# Q-37 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 519275WB | CAT1 | FLINT | Flint 5 Light Multi-Drop Pendant | $584,896 | 459 | 0 | 0 | 0 | 2026-06-12 |
| 515155OL | CAT1 | SAMAL | Samal 21 Inch Pendant | $124,925 | 252 | 0 | 0 | 0 | 2026-06-28 |
| 030257-038 | CAT1 | COL185 | Glacier 60 Inch LED Round Pendant | $90,966 | 24 | 0 | 0 | 0 | 2026-07-07 |
| 519221WB | CAT7 | FLINT | Flint 1 Light Led  Convertible Wall Sconce/Mini Pendant | $86,699 | 342 | 0 | 0 | 0 | 2026-06-12 |
| 505820OL | CAT12 | ROXY | Roxy 2 Light ADA Sconce | $63,294 | 563 | 0 | 0 | 0 | 2026-06-28 |
| 519276WB | CAT1 | COL429 | Flint 3 Light Full Canopy Pendant | $61,716 | 88 | 0 | 0 | 0 | 2026-06-12 |
| 520555OL | CAT1 | COL435 | Crescent 6 Light Pendant | $45,103 | 96 | 0 | 0 | 0 | 2026-06-28 |
| 509952WB | CAT1 | LAVO | Lavo 39 Inch Round LED Pendant | $43,930 | 47 | 0 | 0 | 0 | 2026-07-12 |
| 519277WB | CAT1 | COL429 | Flint 5 Light Full Canopy Pendant | $36,445 | 30 | 0 | 0 | 0 | 2026-06-12 |
| 041961-062-FR001 | CAT9 | TUBO | Tubo CCT LED Island Light | $35,784 | 38 | 0 | 0 | 0 | — |
| 523531TRB | CAT7 | COL448 | Gypsum Tubular LED Wall Sconce | $30,059 | 61 | 0 | 0 | 0 | 2026-07-12 |
| 030234-038 | CAT29 | COL185 | Glacier 38 Inch LED ADA Bath | $28,729 | 33 | 0 | 0 | 0 | 2026-07-07 |
| 525361MG | CAT9 | FLORA | Flora Island Light | $28,487 | 49 | 0 | 0 | 0 | 2026-06-28 |
| 512511WB | CAT5 | COL409 | Canterbury 10 Inch LED Mini Pendant | $23,664 | 36 | 0 | 0 | 0 | 2026-07-12 |
| 033970-044-FR001 | CAT2 | TAVO | Tavo 6 Light Chandelier | $19,529 | 20 | 0 | 0 | 0 | 2026-07-12 |
| 525321MG | CAT7 | FLORA | Flora Tall Wall Sconce | $18,945 | 121 | 0 | 0 | 0 | 2026-08-03 |
| 099021-063-FR001 | CAT7 | COL6 | Tappata 24" LED Outdoor Wall Sconce | $15,254 | 42 | 0 | 0 | 0 | 2026-07-12 |
| 040221-010-FR001 | CAT7 | COL456 | Piovere LED CCT Wall Sconce | $14,692 | 38 | 0 | 0 | 0 | — |
| 090321-052-FR001 | CAT7 | COL6 | Tenuta Esterno 20" Outdoor Wall Sconce | $14,337 | 25 | 0 | 0 | 0 | 2026-06-12 |
| 030256-010 | CAT1 | COL185 | Glacier 25 + 32 Inch 2 Tier LED Round Pendant | $14,025 | 5 | 0 | 0 | 0 | — |

### Q-38a_results.md

# Q-38a Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 3792
- **Run date**: 2026-06-17


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
| /C | — | — | — | 2025-12-01 | 0 | 3 |
| /C | — | — | — | 2026-01-01 | 0 | 16 |
| /C | — | — | — | 2026-02-01 | 0 | 8 |
| /C | — | — | — | 2026-03-01 | 0 | 10 |
| /C | — | — | — | 2026-04-01 | 0 | 13 |
| /C | — | — | — | 2026-05-01 | 0 | 13 |
| /C | — | — | — | 2026-06-01 | 0 | 1 |
| 012121-010-FR001 | Floridia 1 Light Wall Bracket | CAT7 | COL154 | 2026-02-01 | 2 | 1 |
| 012121-010-FR001 | Floridia 1 Light Wall Bracket | CAT7 | COL154 | 2026-03-01 | 4 | 1 |
| 012121-045-FR001 | Floridia 1 Light Wall Bracket | CAT7 | COL154 | 2026-01-01 | 2 | 1 |
| 012121-045-FR001 | Floridia 1 Light Wall Bracket | CAT7 | COL154 | 2026-03-01 | 2 | 1 |
| 012121-045-FR001 | Floridia 1 Light Wall Bracket | CAT7 | COL154 | 2026-05-01 | 2 | 1 |
| 012121-045-FR001 | Floridia 1 Light Wall Bracket | CAT7 | COL154 | 2026-06-01 | 6 | 1 |
| 012122-010-FR001 | Floridia 2 Light Wall Bracket | CAT7 | COL154 | 2026-01-01 | 2 | 1 |
| 012122-045-FR001 | Floridia 2 Light Wall Bracket | CAT7 | COL154 | 2025-12-01 | 3 | 1 |
| 012122-045-FR001 | Floridia 2 Light Wall Bracket | CAT7 | COL154 | 2026-01-01 | 5 | 2 |
| 012122-045-FR001 | Floridia 2 Light Wall Bracket | CAT7 | COL154 | 2026-02-01 | 1 | 1 |
| 012122-045-FR001 | Floridia 2 Light Wall Bracket | CAT7 | COL154 | 2026-03-01 | 2 | 1 |
| 012122-045-FR001 | Floridia 2 Light Wall Bracket | CAT7 | COL154 | 2026-04-01 | 2 | 1 |
| 012170-010-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-04-01 | 1 | 1 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2025-12-01 | 1 | 1 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-01-01 | 5 | 5 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-02-01 | 5 | 3 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-03-01 | 6 | 5 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-04-01 | 3 | 3 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-05-01 | 1 | 1 |
| 012170-045-FR001 | Floridia 5 Light Chandelier | CAT2 | COL154 | 2026-06-01 | 1 | 1 |
| 012171-010-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-02-01 | 1 | 1 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2025-12-01 | 4 | 4 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-01-01 | 8 | 7 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-02-01 | 6 | 6 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-03-01 | 6 | 6 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-04-01 | 4 | 4 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-05-01 | 4 | 4 |
| 012171-045-FR001 | Floridia 6 Light Chandelier | CAT2 | COL154 | 2026-06-01 | 6 | 5 |
| 012172-010-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-01-01 | 1 | 1 |
| 012172-010-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-03-01 | 3 | 2 |
| 012172-045-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2025-12-01 | 1 | 1 |
| 012172-045-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-01-01 | 2 | 2 |
| 012172-045-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-02-01 | 1 | 1 |
| 012172-045-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-03-01 | 2 | 2 |
| 012172-045-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-04-01 | 5 | 5 |
| 012172-045-FR001 | Floridia (6+3) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-05-01 | 2 | 2 |
| 012173-010-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-05-01 | 1 | 1 |
| 012173-045-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2025-12-01 | 1 | 1 |
| 012173-045-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-01-01 | 2 | 1 |
| 012173-045-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-02-01 | 1 | 1 |
| 012173-045-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-03-01 | 1 | 1 |
| 012173-045-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-04-01 | 3 | 3 |
| 012173-045-FR001 | Floridia (10+5) Light 2 Tier Chandelier | CAT2 | COL154 | 2026-05-01 | 2 | 2 |

*(Truncated: showing top 50 of 3792 rows. Full data in cache file.)*

### Q-39_category_results.md

# Q-39-cat Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 27
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT1 | $7.7M | 8,757 | 418 | $18,467 |
| CAT2 | $2.3M | 2,516 | 173 | $13,050 |
| CAT7 | $2.1M | 9,160 | 255 | $8,165 |
| CAT9 | $1.8M | 1,699 | 113 | $15,607 |
| CAT3 | $477,391 | 2,079 | 152 | $3,141 |
| CAT6 | $469,151 | 1,704 | 29 | $16,178 |
| CAT11 | $400,506 | 1,399 | 60 | $6,675 |
| CAT4 | $377,132 | 356 | 40 | $9,428 |
| CAT14 | $352,298 | 1,283 | 399 | $883 |
| CAT5 | $349,634 | 1,264 | 47 | $7,439 |
| CAT34 | $316,970 | 1,009 | 43 | $7,371 |
| CAT12 | $199,528 | 1,211 | 20 | $9,976 |
| CAT29 | $107,912 | 266 | 13 | $8,301 |
| CAT8 | $94,103 | 81 | 13 | $7,239 |
| CAT15 | $74,184 | 171 | 10 | $7,418 |
| CAT13 | $40,188 | 108 | 4 | $10,047 |
| CAT10 | $39,270 | 81 | 11 | $3,570 |
| CAT16 | $38,683 | 61 | 6 | $6,447 |
| CAT20 | $28,661 | 26 | 6 | $4,777 |
| CAT18 | $12,831 | 38 | 5 | $2,566 |
| CAT25 | $10,396 | 7 | 3 | $3,465 |
| CAT24 | $9,434 | 32 | 8 | $1,179 |
| CAT23 | $9,050 | 19 | 5 | $1,810 |
| CAT21 | $4,025 | 10 | 2 | $2,012 |
| TABLE | $3,268 | 4 | 4 | $817 |
| CAT22 | $2,439 | 2 | 1 | $2,439 |
| CAT17 | $951 | 6 | 2 | $475 |

### Q-39_collection_results.md

# Q-39-col Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| COL185 | $1.6M | 1,125 | 58 | $27,331 |
| FLINT | $1.0M | 1,254 | 3 | $337,771 |
| ROXY | $668,533 | 2,136 | 7 | $95,505 |
| COL253 | $643,343 | 805 | 5 | $128,669 |
| COL6 | $451,450 | 656 | 30 | $15,048 |
| COL392 | $446,652 | 528 | 6 | $74,442 |
| VERDE | $383,731 | 501 | 6 | $63,955 |
| COL420 | $332,757 | 833 | 6 | $55,460 |
| SAMAL | $323,353 | 594 | 4 | $80,838 |
| COL154 | $322,054 | 497 | 14 | $23,004 |
| LINA | $294,705 | 547 | 25 | $11,788 |
| COL21 | $276,910 | 201 | 16 | $17,307 |
| UROKO | $248,243 | 467 | 10 | $24,824 |
| COL19 | $234,803 | 193 | 14 | $16,772 |
| COL439 | $230,788 | 254 | 3 | $76,929 |
| PRADO | $213,629 | 457 | 8 | $26,704 |
| COL33 | $212,095 | 171 | 5 | $42,419 |
| COL457 | $208,106 | 201 | 6 | $34,684 |
| ALTA | $205,292 | 122 | 13 | $15,792 |
| COL355 | $200,147 | 606 | 5 | $40,029 |
| COL431 | $199,384 | 662 | 3 | $66,461 |
| COL177 | $192,021 | 95 | 10 | $19,202 |
| COL206 | $178,795 | 331 | 17 | $10,517 |
| LUCCA | $175,872 | 393 | 11 | $15,988 |
| COL169 | $165,346 | 830 | 10 | $16,535 |

### Q-42_results.md

# Q-42 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 135
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| COL439 | 95 | $230,788 | 265 | $2,429 |
| COL33 | 93 | $212,095 | 199 | $2,281 |
| COL457 | 127 | $208,106 | 226 | $1,639 |
| UROKO | 169 | $137,622 | 273 | $814 |
| FUJI | 72 | $126,114 | 91 | $1,752 |
| TINTA | 65 | $109,369 | 145 | $1,683 |
| COL253 | 56 | $108,111 | 58 | $1,931 |
| COL429 | 63 | $98,161 | 128 | $1,558 |
| TUBO | 50 | $76,071 | 108 | $1,521 |
| COL436 | 66 | $72,767 | 136 | $1,103 |
| FLORA | 111 | $66,762 | 365 | $601 |
| ROCHE | 27 | $53,521 | 39 | $1,982 |
| COL448 | 49 | $51,984 | 125 | $1,061 |
| ALTA | 29 | $45,676 | 29 | $1,575 |
| COL456 | 44 | $41,089 | 58 | $934 |
| COL28 | 59 | $41,067 | 91 | $696 |
| COL449 | 37 | $38,205 | 60 | $1,033 |
| PELT | 42 | $36,677 | 63 | $873 |
| COL470 | 49 | $36,628 | 76 | $748 |
| FIORE | 31 | $34,300 | 38 | $1,106 |
| SPAT | 39 | $27,787 | 93 | $712 |
| COL29 | 24 | $26,839 | 31 | $1,118 |
| PASSO | 25 | $25,551 | 30 | $1,022 |
| COL472 | 28 | $24,586 | 35 | $878 |
| COL469 | 40 | $24,438 | 122 | $611 |
| DAMA | 26 | $23,720 | 25 | $912 |
| COL359 | 50 | $22,893 | 52 | $458 |
| VERDE | 29 | $22,303 | 46 | $769 |
| COL471 | 54 | $21,314 | 75 | $395 |
| POPPY | 43 | $20,894 | 48 | $486 |
| COL490 | 18 | $20,480 | 17 | $1,138 |
| COL185 | 15 | $20,120 | 18 | $1,341 |
| COL454 | 25 | $19,672 | 20 | $787 |
| COL489 | 33 | $18,319 | 55 | $555 |
| COL465 | 26 | $17,512 | 35 | $674 |
| COL35 | 27 | $16,305 | 68 | $604 |
| BOLSA | 43 | $15,928 | 42 | $370 |
| COL473 | 24 | $14,917 | 39 | $622 |
| COL495 | 15 | $14,669 | 20 | $978 |
| ROMAN | 18 | $14,578 | 37 | $810 |
| FOLIA | 35 | $13,997 | 27 | $400 |
| SOGA | 27 | $13,810 | 36 | $511 |
| ONYX | 15 | $13,400 | 22 | $893 |
| COL40 | 7 | $13,169 | 10 | $1,881 |
| COL491 | 27 | $13,147 | 24 | $487 |
| SPIRA | 25 | $12,915 | 46 | $517 |
| COL466 | 29 | $12,856 | 38 | $443 |
| COL38 | 22 | $12,844 | 25 | $584 |
| COL230 | 20 | $12,757 | 19 | $638 |
| COL447 | 43 | $12,754 | 55 | $297 |
| CREST | 29 | $12,434 | 34 | $429 |
| COL5 | 5 | $12,098 | 7 | $2,420 |
| COL27 | 17 | $11,694 | 27 | $688 |
| MISTO | 14 | $11,407 | 17 | $815 |
| GISEL | 17 | $11,262 | 18 | $662 |
| COL441 | 21 | $11,075 | 16 | $527 |
| COL43 | 4 | $10,951 | 12 | $2,738 |
| REEF | 19 | $10,827 | 24 | $570 |
| COL34 | 9 | $10,436 | 15 | $1,160 |
| EDGY | 24 | $10,425 | 72 | $434 |
| COL498 | 14 | $10,310 | 16 | $736 |
| COL474 | 9 | $10,272 | 23 | $1,141 |
| GEO | 14 | $10,088 | 20 | $721 |
| CORAL | 12 | $10,081 | 19 | $840 |
| BLOOM | 16 | $9,891 | 20 | $618 |
| CORDA | 10 | $9,705 | 11 | $971 |
| LUMBA | 18 | $9,653 | 27 | $536 |
| COL36 | 2 | $9,499 | 2 | $4,749 |
| COL39 | 5 | $9,187 | 9 | $1,837 |
| MANTA | 9 | $8,743 | 14 | $971 |
| COL1 | 5 | $7,946 | 5 | $1,589 |
| CORNA | 4 | $7,753 | 3 | $1,938 |
| COL32 | 14 | $7,752 | 13 | $554 |
| COL6 | 23 | $7,629 | 30 | $332 |
| DUET | 25 | $7,435 | 72 | $297 |
| COL463 | 12 | $7,241 | 20 | $603 |
| AMOR | 15 | $7,192 | 14 | $479 |
| ROSE | 20 | $6,820 | 22 | $341 |
| COL440 | 19 | $6,679 | 11 | $352 |
| COL445 | 11 | $5,888 | 8 | $535 |
| COL443 | 36 | $5,515 | 27 | $153 |
| COL408 | 2 | $5,361 | 2 | $2,680 |
| COL44 | 11 | $5,283 | 23 | $480 |
| BLUSH | 11 | $5,129 | 19 | $466 |
| COL37 | 3 | $5,109 | 3 | $1,703 |
| COL42 | 9 | $5,020 | 26 | $558 |
| COL442 | 7 | $5,006 | 9 | $715 |
| COL488 | 10 | $4,875 | 11 | $488 |
| MARGE | 7 | $4,722 | 11 | $675 |
| COL503 | 4 | $4,608 | 3 | $1,152 |
| COL481 | 7 | $4,215 | 11 | $602 |
| ADORN | 7 | $3,999 | 2 | $571 |
| BELLA | 7 | $3,500 | 5 | $500 |
| FERN | 8 | $3,399 | 9 | $425 |
| COL497 | 15 | $3,315 | 6 | $221 |
| TEMPO | 6 | $3,298 | 4 | $550 |
| COL493 | 3 | $2,979 | 6 | $993 |
| COL444 | 14 | $2,962 | 12 | $212 |
| COL467 | 4 | $2,547 | 6 | $637 |
| ROXY | 24 | $2,501 | 10 | $104 |
| COL394 | 9 | $2,498 | 3 | $278 |
| LOOPS | 6 | $2,463 | 4 | $410 |
| COL4 | 11 | $2,460 | 10 | $224 |
| COL468 | 7 | $2,448 | 9 | $350 |
| COL30 | 7 | $2,398 | 9 | $343 |
| JEWEL | 8 | $2,335 | 12 | $292 |
| COL502 | 4 | $2,249 | 1 | $562 |
| DUO | 6 | $2,213 | 8 | $369 |
| COL486 | 8 | $2,116 | 12 | $264 |
| COL501 | 11 | $1,944 | 10 | $177 |
| COL487 | 5 | $1,838 | 6 | $368 |
| MODA | 8 | $1,610 | 2 | $201 |
| COL475 | 3 | $1,498 | 3 | $500 |
| COL373 | 12 | $1,311 | 5 | $109 |
| COL492 | 2 | $1,299 | 2 | $649 |
| COL374 | 8 | $1,199 | 11 | $150 |
| COL31 | 3 | $1,126 | 3 | $375 |
| COCCO | 11 | $1,008 | 6 | $92 |
| COL499 | 11 | $1,003 | 4 | $91 |
| ORE | 3 | $822 | 4 | $274 |
| COL45 | 5 | $774 | 5 | $155 |
| DELTA | 4 | $478 | 4 | $120 |
| TART | 2 | $400 | 2 | $200 |
| COL504 | 2 | $349 | 2 | $174 |
| COL482 | 6 | $295 | 5 | $49 |
| RIZO | 3 | $250 | 1 | $83 |
| COL446 | 2 | $174 | 2 | $87 |
| COL248 | 1 | $149 | 1 | $149 |
| COL462 | 1 | $74 | 1 | $74 |
| COL464 | 1 | $54 | 1 | $54 |
| COL455 | 1 | $0 | 0 | $0 |
| COL494 | 1 | $0 | 1 | $0 |
| COL500 | 5 | $0 | 0 | $0 |
| DOS | 9 | $0 | 0 | $0 |
| ORI | 1 | $0 | 0 | $0 |

### Q-59_results.md

# Q-59 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ITEM | 519275WB | Flint 5 Light Multi-Drop Pendant | CAT1 | — | — | 7 | 7 | 1,405.89 | 9,841.20 | 447,201.28 | 102 |
| ITEM | 526555BCG | Autumna 29.5-in 22 Light (40-watt) Brushed Champagne Gold Chandelier | CAT2 | — | — | 6 | 6 | 1,415.67 | 8,494 | 8,494 | 6 |
| ITEM | 527751VGB | Adorn 35.75-in 40 Light (40-watt) Vintage Brass Chandelier | CAT2 | — | — | 3 | 2 | 2,666 | 7,998 | 27,993 | 7 |
| ITEM | 524622PWB | Uroko Wall Sconce | CAT7 | — | — | 59 | 1 | 121.50 | 7,168.50 | 18,572.35 | 16 |
| ITEM | MODD-GL-BBGLASS-MD | CUSTOM GOLD LEAF BUBBLES GLASS | Uncategorized | — | — | 1 | 1 | 5,813 | 5,813 | 10,463 | 1 |
| ITEM | 519276WB | Flint 3 Light Full Canopy Pendant | CAT1 | — | — | 7 | 5 | 779.78 | 5,458.48 | 56,331.15 | 34 |
| ITEM | 528655RSG | Moda 32-in 12 Light (6-watt) Rustic Gold Chandelier | CAT2 | — | — | 3 | 3 | 1,499 | 4,497 | 4,497 | 3 |
| ITEM | 030257-038 | Glacier 60 Inch LED Round Pendant | CAT1 | — | — | 1 | 1 | 4,333 | 4,333 | 71,379.10 | 12 |
| ITEM | 524156RSG | Cirque Foyer Light | CAT4 | — | — | 3 | 3 | 1,441 | 4,323 | 25,657.75 | 17 |
| ITEM | 524922WB | Kiriko 28-in (12-watt) LED Winter Brass Wall Sconce | CAT7 | — | — | 8 | 6 | 486.69 | 3,893.50 | 3,893.50 | 6 |
| ITEM | 047361-038-FR001 | Farfalle 60.5-in 9 Light (40-watt) Brushed Champagne Gold Linear Pendant | CAT20 | — | — | 3 | 3 | 1,249 | 3,747 | 7,494 | 6 |
| ITEM | 047355-038-FR001 | Farfalle 28-in 18 Light (40-watt) Brushed Champagne Gold Chandelier | CAT2 | — | — | 2 | 2 | 1,799 | 3,598 | 3,598 | 2 |
| ITEM | 523455WB | Camellia 28In Pendant | CAT1 | — | — | 3 | 2 | 1,132.67 | 3,398 | 21,622.10 | 12 |
| ITEM | 528461RBG | Dos 48-in 6 Light (40-watt) Rustic Gold and Brushed Gold Linear Pendant | CAT20 | — | — | 6 | 6 | 549 | 3,294 | 3,294 | 6 |
| ITEM | 043162-010-FR001 | Dama 60In LED Chrome Island Light | CAT9 | — | — | 3 | 1 | 1,029 | 3,087 | 5,085 | 2 |
| ITEM | 524661PWB | Uroko 49.5-in 9 Light (40-watt) Polished Winter Brass Linear Pendant | CAT20 | — | — | 2 | 2 | 1,499 | 2,998 | 16,489 | 9 |

### Q-61_results.md

# Q-61 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 521158PAB | Sphere 36" Capiz Pendant | CAT1 | 17 | 34 | 47,489.80 | 31 | 1,416 |
| 046261-073-FR001 | CADERE ISLAND LIGHT | CAT9 | 5 | 20 | 44,156.10 | 8 | 2,265 |
| 046256-073-FR001 | CADERE 40 IN CHANDELIER | CAT2 | 10 | 14 | 41,425.40 | 12 | 2,832 |
| 524655BN | UROKO 28 IN PENDANT BN | CAT1 | 30 | 46 | 39,816.40 | 40 | 906 |
| 043672-044-GLMULTI | TINTA 2-TIER CHANDELIER | CAT2 | 9 | 11 | 39,032.90 | 11 | 3,398 |
| 040555-062-FR008 | Fuji Foyer Light | CAT4 | 4 | 4 | 38,592 | 4 | 8,497 |
| 040655-038-FR001 | Frangia 29" Pendant | CAT1 | 16 | 23 | 33,302.95 | 22 | 1,529 |
| 519276WB | Flint 3 Light Full Canopy Pendant | CAT1 | 22 | 44 | 33,107.35 | 33 | 793 |
| 524656BN | UROKO 34 IN PENDANT BN | CAT1 | 18 | 20 | 30,245.50 | 19 | 1,540 |
| 519671STB/MGNT | Verde 40-in 6 Light (40-watt) Satin Brass Chandelier | CAT2 | 15 | 18 | 28,363.10 | 18 | 1,649 |
| 521156PAB | Sphere 28" Capiz Pendant | CAT1 | 22 | 34 | 28,237.65 | 29 | 849 |
| 527751VGB | Adorn 35.75-in 40 Light (40-watt) Vintage Brass Chandelier | CAT2 | 7 | 8 | 27,993 | 8 | 3,999 |
| 040656-038-FR001 | Frangia 34" Pendant | CAT1 | 11 | 11 | 26,218.65 | 11 | 2,605 |
| 040561-062-FR008 | Fuji Island Light | CAT9 | 11 | 12 | 25,941.75 | 12 | 2,265 |
| 037657-038-FR001 | Estrella 48" Pendant | CAT1 | 7 | 9 | 22,641 | 9 | 2,549 |
| 046251-073-FR001 | CADERE FOYER LIGHT | CAT4 | 4 | 4 | 20,367.40 | 4 | 4,531 |
| 526855PABMG | Button 6 Lt Pendant | CAT1 | 16 | 25 | 18,652.80 | 25 | 772 |
| 046255-073-FR001 | CADERE 26 IN CHANDELIER | CAT2 | 11 | 12 | 18,002.20 | 11 | 1,416 |
| 523531TRB | Gypsum Tubular LED Wall Sconce | CAT7 | 10 | 29 | 17,617.90 | 14 | 623 |
| 041961-062-FR001 | Tubo CCT LED Island Light | CAT9 | 8 | 12 | 16,979.60 | 10 | 1,416 |
| 524156RSG | Cirque Foyer Light | CAT4 | 11 | 12 | 16,844.05 | 12 | 1,441 |
| 524661BN | Uroko 49.5-in 9 Light (40-watt) Black Nickel Linear Pendant | CAT20 | 9 | 11 | 16,789 | 10 | 1,499 |
| 524661PWB | Uroko 49.5-in 9 Light (40-watt) Polished Winter Brass Linear Pendant | CAT20 | 9 | 11 | 16,489 | 10 | 1,499 |
| 041931-062-FR001 | TUBO BATH LIGHT | CAT3 | 7 | 21 | 15,331.50 | 10 | 793 |
| 519277WB | Flint 5 Light Full Canopy Pendant | CAT1 | 6 | 11 | 15,091.10 | 11 | 1,450 |
| 525361MG | Flora Island Light | CAT9 | 11 | 21 | 14,934 | 16 | 736 |
| 523455WB | Camellia 28In Pendant | CAT1 | 8 | 10 | 14,366.50 | 10 | 1,699 |
| 527455OLW | Amor 36-in 8 Light (40-watt) Oxidized Gold Leaf And White Chandelier | CAT2 | 14 | 15 | 13,485 | 14 | 899 |
| 043670-044-GLMULTI | TINTA 6 LIGHT CHANDELIER | CAT2 | 7 | 10 | 13,457.40 | 9 | 1,472 |
| 528352WB | Bolsa 31-in 6 Light (40-watt) Winter Brass Chandelier | CAT2 | 5 | 7 | 12,993.50 | 7 | 1,999 |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 8
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 519275WB | Flint 5 Light Multi-Drop Pendant | FLINT | 583,127.50 | 515 | — | 2026-6-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 100065.55}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 75687.42}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 64745.71}, {'customer': 'BUILD.COM', 'revenue': 32335.17}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 28304.4}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 21462.92}, {'customer': 'WAYFAIR LLC', 'revenue': 21028.11}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 15856.57}, {'customer': 'SUN LIGHTING', 'revenue': 13280.4}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 11728.44}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 9742.62}, {'customer': 'CITY LIGHTS', 'revenue': 7456.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 6426.94}, {'customer': '1-800-MY-LAMPS', 'revenue': 4469.14}, {'customer': 'DULLES ELECTRIC & SUPPLY', 'revenue': 4408.97}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 4252.84}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 4028.1}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 3934.35}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 3915.9}, {'customer': 'LIGHTING ETC', 'revenue': 3872.0}, {'customer': 'NEIMAN MARCUS', 'revenue': 3747.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 3372.3}, {'customer': 'DOLAN NORTHWEST LLC  PORTLAND', 'revenue': 3372.3}, {'customer': 'MANHATTAN LIGHTS INC', 'revenue': 3095.14}, {'customer': 'UNIVERSAL LAMP', 'revenue': 3095.14}, {'customer': 'PLUMBING DISTRIBUTORS  INC', 'revenue': 3095.14}, {'customer': 'KRELL LIGHTING', 'revenue': 3037.32}, {'customer': 'Lighting Design Center', 'revenue': 2832.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 2790.0}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 2748.0}, {'customer': 'LUXUR LIGHTING', 'revenue': 2748.0}, {'customer': 'DESIGNERS RESOURCE COLLECTION', 'revenue': 2747.8}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 2665.0}, {'customer': 'NOVA LIGHTING', 'revenue': 2610.6}, {'customer': 'HERALD WHOLESALE', 'revenue': 2498.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 2498.0}, {'customer': 'EAGLE LIGHTING DISTRIBUTORS', 'revenue': 2498.0}, {'customer': 'LAMPS EXPO/LAMPCLICK.COM', 'revenue': 2498.0}, {'customer': 'GEORGIA LIGHTING', 'revenue': 2466.03}, {'customer': 'WILSON LIGHTING- NAPLES', 'revenue': 2248.2}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 2061.0}, {'customer': 'CAPITOL LIGHTING PARAMUS', 'revenue': 1967.25}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 1967.25}, {'customer': 'URBAN LIGHTS', 'revenue': 1957.0}, {'customer': 'R&F LIGHTING & SUPPLIES', 'revenue': 1896.32}, {'customer': 'TEXAS BRIGHT IDEAS INC', 'revenue': 1628.4}, {'customer': 'GEORGIAN LIGHTING GALERY INC', 'revenue': 1621.32}, {'customer': 'REFLECTIONS L+M', 'revenue': 1621.32}, {'customer': 'SUPREME LTG & ELEC', 'revenue': 1621.32}, {'customer': 'NORTHERN LIGHTING WESTERV', 'revenue': 1621.32}, {'customer': 'EFIRDS INTERIORS', 'revenue': 1621.32}, {'customer': "AARON'S SUPPLY  INC", 'revenue': 1621.32}, {'customer': 'KING ELECTRIC COMPANY INC', 'revenue': 1621.32}, {'customer': 'B A ROBINSON COMPANY LTD CALG', 'revenue': 1621.2}, {'customer': 'THE JARRELL COMPANY', 'revenue': 1580.1}, {'customer': 'FUSION LIGHT AND DESIGN LLC', 'revenue': 1580.1}, {'customer': 'IBS LIGHTING LTD.', 'revenue': 1580.1}, {'customer': 'ILLUMINATIONS MC ALLEN', 'revenue': 1580.1}, {'customer': 'CED / GLACIER STATE ELECTRIC', 'revenue': 1580.1}, {'customer': 'LIGHTING INC', 'revenue': 1511.4}, {'customer': 'RITTENHOUSE ELECTRIC', 'revenue': 1473.82}, {'customer': 'FANWORLD', 'revenue': 1473.82}, {'customer': 'WINSUPPLY HENDERSONVILLE', 'revenue': 1473.82}, {'customer': 'WOLBERG ELECTRICAL SUPPLY', 'revenue': 1473.82}, {'customer': 'LIGHT LAB DESIGN', 'revenue': 1473.82}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 1473.82}, {'customer': 'FOUNDRY  ARC DISTRIBUTION', 'revenue': 1473.82}, {'customer': 'CORDREY COLLECTION', 'revenue': 1436.35}, {'customer': 'PREMIER LIGHTING', 'revenue': 1436.35}, {'customer': 'LIGHTING ZONE', 'revenue': 1436.35}, {'customer': 'HALL ELECTRIC COMPANY', 'revenue': 1416.0}, {'customer': 'LIGHTING BY FOX LLC', 'revenue': 1416.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 1374.0}, {'customer': 'HOMIER LUMINAIRE INC.', 'revenue': 1374.0}, {'customer': 'LUXURY DESIGN BROOKLYN', 'revenue': 1374.0}, {'customer': 'CONSUMERS LIGHTING AND LAMPS L', 'revenue': 1374.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 1374.0}, {'customer': 'WALNUT CREEK LIGHTING', 'revenue': 1374.0}, {'customer': 'LIGHT BULBS UNLIMITED BOCA RA', 'revenue': 1374.0}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 1374.0}, {'customer': 'LEEWAL LLC', 'revenue': 1374.0}, {'customer': 'BISONOFFICE LLC', 'revenue': 1374.0}, {'customer': 'DEMENT LIGHTING', 'revenue': 1374.0}, {'customer': 'INDIANA LIGHTING CENTER', 'revenue': 1374.0}, {'customer': 'LIGHTING SUPERSTORE', 'revenue': 1374.0}, {'customer': 'RAY ELECTRIC', 'revenue': 1345.2}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 1332.78}, {'customer': 'LIGHTING INSTYLE', 'revenue': 1311.45}, {'customer': 'ACCENT LTG GALLERIES', 'revenue': 1249.0}, {'customer': 'ONE STOP LIGHTING', 'revenue': 1249.0}, {'customer': 'SHOPFREELY.COM', 'revenue': 1249.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 1249.0}, {'customer': 'WOLSELEY CANADA  INC', 'revenue': 1249.0}, {'customer': 'A A PORTER LTG CO (DO NOT CONTACT)', 'revenue': 1249.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 1249.0}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 1124.1}, {'customer': 'BELL & MCCOY COMPANIES', 'revenue': 1124.1}, {'customer': 'LIGHTSTYLES', 'revenue': 1099.2}, {'customer': 'CAPITOL LIGHTING--EATONTOWN', 'revenue': 1030.5}, {'customer': 'LIGHTING WAREHOUSE', 'revenue': 961.8}, {'customer': 'INFO LIGHTING, INC.', 'revenue': 811.85}, {'customer': 'HERMITAGE ELECTRIC SUPPLY', 'revenue': 687.0}, {'customer': 'LEE SUPPLY CORP', 'revenue': 624.5}, {'customer': 'WASATCH LIGHTING', 'revenue': 624.5}, {'customer': 'DHILLON LIGHTING', 'revenue': 624.5}, {'customer': 'MST LIGHTING INC.', 'revenue': 421.02}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 187.35}, {'customer': 'SCOUT LIGHTING', 'revenue': 0.1}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'LUXURY LIGHTING GROUP', 'revenue': 0.0}, {'customer': 'LIGHT & DAY LLC', 'revenue': 0.0}, {'customer': 'MI CASA LIGHTING AND FAN', 'revenue': 0.0}, {'customer': 'PARK LIGHTING', 'revenue': 0.0}, {'customer': 'RAINBOW LIGHTING INC /NBROOK', 'revenue': 0.0}, {'customer': 'EISENREICH INTERIORS', 'revenue': 0.0}, {'customer': 'EMMY COUTURE DESIGNS', 'revenue': 0.0}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 0.0}, {'customer': 'GINA IRELAND INTERIORS', 'revenue': 0.0}, {'customer': 'BUSTED 2 BANGIN', 'revenue': 0.0}, {'customer': 'ARYA GROUP INC', 'revenue': 0.0}, {'customer': 'KITCHEN SOCIETY', 'revenue': 0.0}, {'customer': 'I.D. HOME LOGISTICS INC', 'revenue': 0.0}, {'customer': 'B PILA DESIGN STUDIO', 'revenue': 0.0}, {'customer': 'TEELA BENNETT DESIGN', 'revenue': 0.0}, {'customer': 'JGIB INTERIORS', 'revenue': 0.0}, {'customer': 'AURORA LIGHTING & DESIGN', 'revenue': 0.0}, {'customer': 'DESIGN HUTCH', 'revenue': 0.0}, {'customer': 'EL DESIGN', 'revenue': 0.0}, {'customer': 'STEPHANIE ERVIN INTERIORS', 'revenue': 0.0}, {'customer': 'CARISA INTERIOR DESIGN', 'revenue': 0.0}, {'customer': 'COAST LIGHTING', 'revenue': 0.0}, {'customer': 'UNCOMMON ROSE DESIGNS', 'revenue': 0.0}, {'customer': 'THE VIBE INTERIORS', 'revenue': 0.0}, {'customer': 'PFH DESIGNS LLC', 'revenue': 0.0}, {'customer': 'JAQUELINE DOWNS INTERIOR DESIGN', 'revenue': 0.0}, {'customer': 'DESIGN SQUARED', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 0.0}, {'customer': 'BEND LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 0.0}, {'customer': 'PINE LIGHTING LTD', 'revenue': 0.0}, {'customer': 'LIGHTING BY LAVONNE  LLC', 'revenue': 0.0}, {'customer': 'BALTIMORE DESIGN CENTER', 'revenue': 0.0}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 0.0}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 0.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 0.0}, {'customer': 'P&F LITES ECT. LLC', 'revenue': 0.0}, {'customer': 'UNIVERSAL LIGHTS', 'revenue': 0.0}, {'customer': 'WATSON & CO.', 'revenue': 0.0}, {'customer': 'ALLOWAY LIGHTING COMPANY', 'revenue': 0.0}, {'customer': 'BEAUTIFUL LIGHTS LLC', 'revenue': 0.0}, {'customer': 'CENTRAL BULB INC', 'revenue': 0.0}, {'customer': 'FIXTURE EXCHANGE, THE', 'revenue': 0.0}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 0.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'ROYCE COLLECTION INC', 'revenue': 0.0}, {'customer': 'EXCEL LIGHTING & ELECTRICAL', 'revenue': 0.0}, {'customer': 'UNION ELECTRIC LIGHTING - TORO', 'revenue': 0.0}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 0.0}, {'customer': 'JL DESIGNS', 'revenue': 0.0}, {'customer': 'BRADLEY ADCOCK DESIGNS INC', 'revenue': 0.0}, {'customer': 'BLISS LINENS WORLD LP', 'revenue': 0.0}, {'customer': 'WHITE ROOM DESIGN LLC', 'revenue': 0.0}, {'customer': 'CHRISTINE VROOM INTERIORS', 'revenue': 0.0}, {'customer': 'LIGHTING SOLUTIONS & DESIGN', 'revenue': 0.0}, {'customer': 'PATTERSON HOMES', 'revenue': 0.0}, {'customer': 'ALADDIN LIGHTING AND SUPPLY INC.', 'revenue': 0.0}, {'customer': 'ANDERSON DESIGN STUDIO, LLC', 'revenue': 0.0}, {'customer': 'NYE DESIGN LLC', 'revenue': 0.0}, {'customer': 'BAYLEE DEYON DESIGN LLC', 'revenue': 0.0}, {'customer': 'FONDE INTERIORS', 'revenue': 0.0}, {'customer': 'LAURA KEHOE DESIGN', 'revenue': 0.0}, {'customer': 'CLASSIC IMPORTS & DESIGN LLC', 'revenue': 0.0}, {'customer': 'LIGHT CENTER', 'revenue': 0.0}, {'customer': "MONTGOMERY'S", 'revenue': 0.0}, {'customer': 'SHARED TREASURES', 'revenue': 0.0}, {'customer': 'LJR DESIGN', 'revenue': 0.0}, {'customer': 'CRESPO DESIGN GROUP', 'revenue': 0.0}, {'customer': 'AWARD INTERIORS', 'revenue': 0.0}, {'customer': 'AUDREY CAMPBELL DESIGN', 'revenue': 0.0}, {'customer': 'BYBRITT DESIGN', 'revenue': 0.0}, {'customer': 'TRACI CONNELL INTERIORS', 'revenue': 0.0}, {'customer': 'HAMILTON INTERIORS', 'revenue': 0.0}, {'customer': 'AGAPE DESIGN GROUP', 'revenue': 0.0}, {'customer': 'ARTISTIC ELEMENTS', 'revenue': -1768.82}] | [{'item': '519273WB', 'desc': 'Flint 3 Light Multi-Drop Pendant', 'available': 45}] |
| 515155OL | Samal 21 Inch Pendant | SAMAL | 124,924.90 | 260 | — | 2026-6-28 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 8853.33}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 8239.6}, {'customer': 'SHADES OF LIGHT', 'revenue': 8078.46}, {'customer': "PINE GROVE ELEC'L SPL INC", 'revenue': 6807.15}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 6050.7}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 6045.5}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 5304.97}, {'customer': 'CREGGER COMPANY  INC', 'revenue': 5138.88}, {'customer': 'LOWCOUNTRY LIGHTING STUDIO LLC', 'revenue': 3371.52}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 3367.75}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 3145.05}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 2859.45}, {'customer': 'PARK LIGHTING', 'revenue': 2687.4}, {'customer': 'FUSION LIGHT AND DESIGN LLC', 'revenue': 2610.55}, {'customer': "BUTLER'S ELECTRIC", 'revenue': 2249.62}, {'customer': 'BRECHERS COMPANY', 'revenue': 2246.8}, {'customer': 'BEE RIDGE LIGHTING DESIGN', 'revenue': 1865.58}, {'customer': 'BLACK WHALE LIGHTING', 'revenue': 1832.33}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 1762.95}, {'customer': 'CAROLINA LANTERNS & ACCS', 'revenue': 1730.08}, {'customer': 'REVIVAL LIGHTING', 'revenue': 1707.75}, {'customer': 'COASTAL LTG SUPPLY/WILMIN', 'revenue': 1695.66}, {'customer': 'HOBRECHT LIGHTING CO INC', 'revenue': 1652.55}, {'customer': 'MAPLE RIDGE LIGHTING, INC. dba', 'revenue': 1652.55}, {'customer': 'GARBE INDUSTRIES INC  TU', 'revenue': 1630.45}, {'customer': 'SISTER LIGHTING dba', 'revenue': 1572.85}, {'customer': 'SUN LIGHTING', 'revenue': 1501.95}, {'customer': 'BEAUTIFUL THINGS LIGHTING', 'revenue': 1501.95}, {'customer': 'WATTS CURRENT', 'revenue': 1437.0}, {'customer': 'PLUMBING DISTRIBUTORS  INC', 'revenue': 1332.64}, {'customer': 'LIGHT BY ALEXANDRIA', 'revenue': 1187.08}, {'customer': 'ULTRA DESIGN CENTER LLC', 'revenue': 1101.7}, {'customer': 'HYDROLOGIC CORPORATE', 'revenue': 1054.0}, {'customer': 'BUILD.COM', 'revenue': 1016.5}, {'customer': 'BISONOFFICE LLC', 'revenue': 1006.0}, {'customer': 'WAYFAIR LLC', 'revenue': 1001.3}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 952.09}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 862.2}, {'customer': 'M & M LIGHTING LP', 'revenue': 782.5}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 766.5}, {'customer': 'OLD WORLD STONE IMPORTS', 'revenue': 661.25}, {'customer': 'STOKES ELECTRIC', 'revenue': 640.74}, {'customer': 'FOREST HILL LIGHTING', 'revenue': 621.86}, {'customer': "RICHARD'S LIGHTING", 'revenue': 621.86}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 621.86}, {'customer': 'LIFESTYLES STORES INC', 'revenue': 606.05}, {'customer': 'LIGHT CENTER', 'revenue': 606.05}, {'customer': 'ONE SIDE DOOR', 'revenue': 565.22}, {'customer': "AARON'S SUPPLY  INC", 'revenue': 565.22}, {'customer': 'CAMINITI ASSOCIATE  INC  ILL', 'revenue': 565.22}, {'customer': 'CARRINGTON LIGHTING', 'revenue': 553.35}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 543.0}, {'customer': 'FIRST COAST LIGHTING AND FAN', 'revenue': 543.0}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 542.81}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 527.0}, {'customer': 'SUNBELT FANS & LTG LAUREL', 'revenue': 527.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 527.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 511.19}, {'customer': 'KALCO MARKETING CRM', 'revenue': 479.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 479.0}, {'customer': 'COAST LIGHTING', 'revenue': 479.0}, {'customer': "CAROL'S LIGHTING", 'revenue': 479.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 479.0}, {'customer': 'RIVERSIDE LIGHTING', 'revenue': 479.0}, {'customer': 'NOVA LIGHTING', 'revenue': 474.3}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 443.07}, {'customer': 'VP SUPPLY CORP', 'revenue': 342.55}, {'customer': 'LEE SUPPLY CORP', 'revenue': 239.5}, {'customer': 'EUROPEAN CUSTOM LIGHTING', 'revenue': 239.5}, {'customer': 'ROBINSON LIGHTING LTD / PLYMOU', 'revenue': 217.2}, {'customer': 'PURPOSE INTERIORS', 'revenue': 82.21}, {'customer': 'AURORA LIGHTING & DESIGN', 'revenue': 0.0}, {'customer': 'LESSMAN ELECTRIC SUPPLY CO. INC.', 'revenue': 0.0}, {'customer': 'LINDSEY GLASS', 'revenue': 0.0}, {'customer': 'KALCO LIGHTING SHOWROOM\\D', 'revenue': 0.0}, {'customer': 'BERKELEY LIGHTING COMPANY', 'revenue': 0.0}, {'customer': 'LIGHT HOUSE  THE   HARLINGEN', 'revenue': 0.0}, {'customer': 'WILSON COMPANY-KANSAS', 'revenue': 0.0}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 0.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 0.0}, {'customer': 'RE-LIGHTING INC', 'revenue': 0.0}, {'customer': 'SUPREME LTG & ELEC', 'revenue': 0.0}, {'customer': 'LIGHT INNOVATIONS', 'revenue': 0.0}, {'customer': 'SUPER LITE LIGHTING LTD', 'revenue': 0.0}, {'customer': 'SOUTH DADE LIGHTING INC\\M', 'revenue': 0.0}, {'customer': 'ROCKINGHAM ELEC. SUPPLY', 'revenue': 0.0}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 0.0}, {'customer': 'BRAND LIGHTING', 'revenue': 0.0}, {'customer': 'HOUSE OF LIGHTS INC', 'revenue': 0.0}, {'customer': 'CONNECTICUT LTG CENTER', 'revenue': 0.0}, {'customer': 'DULLES ELECTRIC & SUPPLY', 'revenue': 0.0}, {'customer': 'SALTBOX THE', 'revenue': 0.0}, {'customer': 'AVON CLOCK & LIGHTING', 'revenue': 0.0}, {'customer': 'CARAVELLE LIGHTING INC', 'revenue': 0.0}, {'customer': 'LIGHTHOUSE INC THE', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST', 'revenue': 0.0}, {'customer': 'EFIRDS INTERIORS', 'revenue': 0.0}, {'customer': 'RENSENHOUSE OF LIGHTS', 'revenue': 0.0}, {'customer': 'WILSON LIGHTING- NAPLES', 'revenue': 0.0}, {'customer': "HORTON'S OF LA GRANGE", 'revenue': 0.0}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': "ARMSTRONG'S SUPPLY CO., INC.", 'revenue': 0.0}, {'customer': 'BESCO ELECTRIC SUPPLY CO', 'revenue': 0.0}, {'customer': 'MCLAREN LIGHTING', 'revenue': 0.0}, {'customer': 'KILOHANA LIGHTING/LIHUE', 'revenue': 0.0}, {'customer': 'HOUSE OF LAMPS & SHADES', 'revenue': 0.0}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 0.0}, {'customer': 'COLONIAL ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'WISEWAY SUPPLY INC', 'revenue': 0.0}, {'customer': 'METRO ELECTRIC', 'revenue': 0.0}, {'customer': 'LIGHTSTYLES', 'revenue': 0.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 0.0}, {'customer': 'FIXTURE THIS INC', 'revenue': 0.0}, {'customer': 'FILAMENT LIGHTING', 'revenue': 0.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 0.0}, {'customer': 'LIGHTING BY FOX LLC', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'LBX LIGHTING INC', 'revenue': 0.0}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 0.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 0.0}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 0.0}, {'customer': 'PINE LIGHTING LTD', 'revenue': 0.0}, {'customer': 'NORTHWEST ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 0.0}, {'customer': 'MAGNOLIA LIGHTING, INC.', 'revenue': 0.0}, {'customer': 'PIONEER LIGHTING  INC', 'revenue': 0.0}, {'customer': 'CONSTRUCTION RESOURCES COMPANY LLC', 'revenue': 0.0}, {'customer': 'LIGHTS & MORE / TAMPA', 'revenue': 0.0}, {'customer': 'CATES LIGHTING AT ELEMENTS OF', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST / FT. MYERS', 'revenue': 0.0}, {'customer': 'FORESIGHT LIGHTING (DO NOT USE)', 'revenue': 0.0}, {'customer': 'LIGHTING FACTORY OUTLET', 'revenue': 0.0}, {'customer': 'INSIDE OUT LIGHTING & DECOR', 'revenue': 0.0}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 0.0}, {'customer': 'QUINN WHOLESALE DBA', 'revenue': 0.0}, {'customer': 'CRIMSON DESIGN GROUP', 'revenue': 0.0}, {'customer': '18 SETENTA GALLERIA', 'revenue': 0.0}, {'customer': 'GARBES LIGHTING', 'revenue': 0.0}, {'customer': 'LEEWAL LLC', 'revenue': 0.0}, {'customer': 'GW KEETER LIGHTING&HOME DECOR', 'revenue': 0.0}, {'customer': 'DE LAVENNE DESIGN', 'revenue': 0.0}, {'customer': 'SAVE MORE PLUMBING & LIGHTING', 'revenue': 0.0}, {'customer': 'INSPIRED INTERIORS', 'revenue': 0.0}, {'customer': 'BEAUTIFUL INTERIORS DESIGN GROUP', 'revenue': 0.0}, {'customer': 'EAST INDIES TRADING DBA WEST HOME COLLECTION', 'revenue': 0.0}] | [{'item': '515145OL', 'desc': 'Samal 21 in Pendant', 'available': 26}, {'item': '515141OL', 'desc': 'Samal 12 in Flush Mount', 'available': 20}, {'item': '515156OL', 'desc': 'Samal 25 Inch Pendant', 'available': 12}] |
| 030257-038 | Glacier 60 Inch LED Round Pendant | COL185 | 90,966.21 | 29 | — | 2026-7-7 | [{'customer': 'LIGHTING INC', 'revenue': 15980.9}, {'customer': 'B. COLLECTIVE CO.', 'revenue': 12235.0}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 7680.8}, {'customer': 'DOLAN NORTHWEST LLC  PORTLAND', 'revenue': 6881.4}, {'customer': 'FANWERKS & LIGHTING INC (HOLD)', 'revenue': 4206.0}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 4206.0}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 4206.0}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 3995.7}, {'customer': 'EFIRDS INTERIORS', 'revenue': 3823.0}, {'customer': 'VENICE LIGHTING COMPANY', 'revenue': 3823.0}, {'customer': 'CLIVE DANIEL HOME', 'revenue': 3823.0}, {'customer': 'COAST LIGHTING', 'revenue': 3823.0}, {'customer': 'ELEGANTE INTERIORS & DESIGN LLC', 'revenue': 3823.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 3708.31}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 3685.1}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 3154.5}, {'customer': 'LBX LIGHTING INC', 'revenue': 1911.5}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 0.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'ONE STOP LIGHTING', 'revenue': 0.0}, {'customer': 'TEXAS BRIGHT IDEAS INC', 'revenue': 0.0}, {'customer': 'HERALD WHOLESALE', 'revenue': 0.0}, {'customer': 'FIXTURE EXCHANGE, THE', 'revenue': 0.0}, {'customer': 'BEAUTIFUL THINGS LIGHTING', 'revenue': 0.0}, {'customer': 'QUALITY LIGHTING/DELRAY', 'revenue': 0.0}, {'customer': 'UNIVERSAL LIGHTS', 'revenue': 0.0}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': 'YALE ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'THE LIGHT HOUSE', 'revenue': 0.0}, {'customer': 'LIGHTING PALACE/BROOKLYN', 'revenue': 0.0}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 0.0}, {'customer': 'TALLAHASSEE LIGHTING FAN', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'DESERT LIGHTING SOLUTIONS', 'revenue': 0.0}, {'customer': 'MATCHEZ INTERNATIONALDBA', 'revenue': 0.0}, {'customer': 'BEBBER PROPERTIES INC dba', 'revenue': 0.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 0.0}, {'customer': 'AREZZO DESIGN GROUP', 'revenue': 0.0}, {'customer': 'EUROPEAN CUSTOM LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 0.0}, {'customer': 'LIGHTING BOUTIQUE LLC', 'revenue': 0.0}, {'customer': 'CASA BELLA DESIGN & CONSTRUCTI', 'revenue': 0.0}, {'customer': 'LIGHT BULBS UNLIMITED BOCA RA', 'revenue': 0.0}, {'customer': 'LUMINOUS TRENDS DBA MODERN LUXURY', 'revenue': 0.0}, {'customer': 'NORTHWEST ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'ELECTRIC OUTLET INC', 'revenue': 0.0}, {'customer': 'CONSUMERS LIGHTING AND LAMPS L', 'revenue': 0.0}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 0.0}, {'customer': 'DESIGN HOUSE  INC  THE', 'revenue': 0.0}, {'customer': 'PARADISE LIGHTING', 'revenue': 0.0}, {'customer': 'LAMP SHOP OF NAPLES COMPANY', 'revenue': 0.0}, {'customer': 'LE GROUPE MULTI LUMINAIRE', 'revenue': 0.0}, {'customer': "SCHOENER'S INTERIORS  LLC", 'revenue': 0.0}, {'customer': 'FARADGI DESIGNS INC DBA CHIC H', 'revenue': 0.0}, {'customer': 'CORNELSON DECORATING INC', 'revenue': 0.0}, {'customer': 'ROYCE COLLECTION INC', 'revenue': 0.0}, {'customer': 'EXCEL LIGHTING & ELECTRICAL', 'revenue': 0.0}, {'customer': 'MID VALLEY LIGHTING INC.', 'revenue': 0.0}, {'customer': 'BILL RAY & ASSOCIATES', 'revenue': 0.0}, {'customer': 'FLA LIGHTING  INC', 'revenue': 0.0}, {'customer': 'CORDREY COLLECTION', 'revenue': 0.0}, {'customer': 'LUXE LIFESTYLES NYC', 'revenue': 0.0}, {'customer': 'PATTI DUPREE FURNITURE', 'revenue': 0.0}, {'customer': 'ARTISTIC ELEMENTS', 'revenue': 0.0}, {'customer': "LANDRY'S DEVELOPMENT INC", 'revenue': 0.0}, {'customer': 'ILLUMINA LLC', 'revenue': 0.0}, {'customer': 'DIVINE INTERIORS', 'revenue': 0.0}, {'customer': 'NEIMAN MARCUS', 'revenue': 0.0}, {'customer': 'INTERNATIONAL DESIGN SOURCE', 'revenue': 0.0}, {'customer': 'BISONOFFICE LLC', 'revenue': 0.0}, {'customer': 'LIGHT UP YOUR LIFE', 'revenue': 0.0}, {'customer': 'DECOR HOME CENTER', 'revenue': 0.0}, {'customer': 'DMS SALES INC.', 'revenue': 0.0}, {'customer': 'WHITE ROOM DESIGN LLC', 'revenue': 0.0}, {'customer': 'LIGHTING SOLUTIONS & DESIGN', 'revenue': 0.0}, {'customer': 'INTERIOR OBSESSION', 'revenue': 0.0}, {'customer': 'LEVEL DECORATIONS INC.', 'revenue': 0.0}, {'customer': 'Cash Customer', 'revenue': 0.0}, {'customer': 'KALCO NON A/R CASH', 'revenue': 0.0}, {'customer': 'GARBE INDUSTRIES INC  TU', 'revenue': 0.0}, {'customer': 'WILSON COMPANY-KANSAS', 'revenue': 0.0}, {'customer': "CAROL'S LIGHTING", 'revenue': 0.0}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 0.0}, {'customer': 'LANDO LIGHTING INC', 'revenue': 0.0}, {'customer': 'LAMPS PLUS', 'revenue': 0.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING ETC', 'revenue': 0.0}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 0.0}, {'customer': 'NORTHERN LIGHTING WESTERV', 'revenue': 0.0}, {'customer': 'ASHJIAN LIGHTING', 'revenue': 0.0}, {'customer': 'SUN LIGHTING', 'revenue': 0.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 0.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 0.0}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 0.0}, {'customer': 'FANWORLD', 'revenue': 0.0}] | [{'item': '030220-010', 'desc': 'Glacier LED ADA Wall Sconce', 'available': 27}, {'item': '030220-184', 'desc': 'Glacier 12-in (8-watt) LED Black Nickel Wall Sconce', 'available': 25}, {'item': '030250-184', 'desc': 'Glacier 42-in (40-watt) LED Black Nickel Wave Linear Chandelier', 'available': 19}, {'item': '030210-184', 'desc': 'Glacier 10-in (26-watt) LED Black Nickel Chandelier', 'available': 19}, {'item': '030260-184', 'desc': 'Glacier 48-in (108-watt) LED Black Nickel Linear Chandelier', 'available': 18}, {'item': '030258-184', 'desc': 'Glacier 60-in (60-watt) LED Black Nickel Wave Linear Chandelier', 'available': 16}, {'item': '030250-038', 'desc': 'Glacier 42 Inch LED Wave Island', 'available': 14}, {'item': '030233-038', 'desc': 'Glacier 32 Inch LED ADA Bath', 'available': 13}, {'item': '030258-038', 'desc': 'Glacier 60 Inch LED Wave Island', 'available': 13}, {'item': '030253-010', 'desc': 'Glacier 20 Inch LED Round Pendant', 'available': 12}, {'item': '030231-038', 'desc': 'Glacier 18 Inch LED ADA Bath', 'available': 12}, {'item': '030255-184', 'desc': 'Glacier 32-in (94-watt) LED Black Nickel Chandelier', 'available': 9}, {'item': '030230-010', 'desc': 'Glacier 12 Inch LED ADA Bath', 'available': 9}, {'item': '030260-038', 'desc': 'Glacier 48 Inch LED Island', 'available': 9}, {'item': '030255-010', 'desc': 'Glacier 32 Inch Round LED Pendant', 'available': 8}, {'item': '030252-038', 'desc': 'Glacier 36 Inch LED Rectangular Island', 'available': 8}, {'item': '030253-184', 'desc': 'Glacier 20-in (58-watt) LED Black Nickel Chandelier', 'available': 7}, {'item': '030251-038', 'desc': 'Glacier 26 Inch Rectangular LE', 'available': 7}, {'item': '030259-010', 'desc': 'Glacier 36 Inch Extra Large LED Foyer', 'available': 6}, {'item': '030256-038', 'desc': 'Glacier 25 + 32 Inch 2 Tier LED Round Pendant', 'available': 6}, {'item': '030234-010', 'desc': 'Glacier 38 Inch LED ADA Bath', 'available': 6}, {'item': '030257-010', 'desc': 'Glacier 60 Inch LED Round Pendant', 'available': 6}, {'item': '030210-038', 'desc': 'Glacier 10 Inch LED Mini Pendant', 'available': 3}, {'item': '030254-038', 'desc': 'Glacier 25 Inch LED Round Pendant', 'available': 2}, {'item': '030232-010', 'desc': 'Glacier 24 Inch LED ADA Bath', 'available': 1}] |
| 519221WB | Flint 1 Light Led  Convertible Wall Sconce/Mini Pendant | FLINT | 86,699.12 | 351 | — | 2026-6-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 10564.65}, {'customer': 'WAYFAIR LLC', 'revenue': 8597.07}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 7852.77}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 7113.22}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 4819.14}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 4335.5}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 3506.4}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 2585.4}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 2308.9}, {'customer': 'BUILD.COM', 'revenue': 2022.02}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 1992.0}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 1832.54}, {'customer': 'ROBINSON LIGHTING LTD / PLYMOU', 'revenue': 1415.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 1303.9}, {'customer': 'LAMPS PLUS', 'revenue': 1212.3}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 1167.24}, {'customer': 'SUN LIGHTING', 'revenue': 1128.2}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 1035.84}, {'customer': 'ATELIER MAISON & CO', 'revenue': 1020.58}, {'customer': 'LIGHTING SUPERSTORE', 'revenue': 986.14}, {'customer': 'LEE SUPPLY CORP', 'revenue': 961.14}, {'customer': "BUTLER'S ELECTRIC", 'revenue': 945.44}, {'customer': 'PREMIER LIGHTING', 'revenue': 945.3}, {'customer': 'WASATCH LIGHTING', 'revenue': 797.0}, {'customer': 'NOVA LIGHTING', 'revenue': 790.35}, {'customer': 'GEORGIA LIGHTING', 'revenue': 749.49}, {'customer': 'INSIDE SOURCE', 'revenue': 650.9}, {'customer': 'FUSION LIGHT AND DESIGN LLC', 'revenue': 630.2}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 630.2}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 616.5}, {'customer': 'LIGHTING INC', 'revenue': 602.8}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 572.7}, {'customer': 'THE LIGHT HOUSE', 'revenue': 572.7}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 566.0}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 564.1}, {'customer': 'LIGHT LAB DESIGN', 'revenue': 557.76}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 549.02}, {'customer': 'INDIANA LIGHTING CENTER', 'revenue': 548.0}, {'customer': 'HAUS APPEAL LLC', 'revenue': 548.0}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 516.48}, {'customer': 'LIGHTING ETC', 'revenue': 498.0}, {'customer': 'LIGHTING FIRST / FT. MYERS', 'revenue': 498.0}, {'customer': 'NEIMAN MARCUS', 'revenue': 498.0}, {'customer': 'LIGHTING WAREHOUSE', 'revenue': 424.7}, {'customer': 'CAPITOL LIGHTING PARAMUS', 'revenue': 373.5}, {'customer': 'GROSS LIGHTING & HOME', 'revenue': 333.94}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 333.94}, {'customer': 'INLINE ELECTRIC SUPPLY CO', 'revenue': 333.94}, {'customer': 'KRELL LIGHTING', 'revenue': 293.82}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 286.35}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 283.0}, {'customer': 'LUXUR LIGHTING', 'revenue': 274.0}, {'customer': 'THE JARRELL COMPANY', 'revenue': 274.0}, {'customer': 'DEMENT LIGHTING', 'revenue': 274.0}, {'customer': 'RIVERSIDE LIGHTING', 'revenue': 249.0}, {'customer': 'RAY ELECTRIC', 'revenue': 236.55}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 205.5}, {'customer': 'GROSS ELECTRIC', 'revenue': 161.85}, {'customer': 'COBURN SUPPLY COMPANY', 'revenue': 141.5}, {'customer': 'MINNESOTA LIGHTING, FIREPLACE', 'revenue': 137.0}, {'customer': 'MI CASA LIGHTING AND FAN', 'revenue': 137.0}, {'customer': 'DHILLON LIGHTING', 'revenue': 124.5}, {'customer': 'DEKKER LIGHTING', 'revenue': 124.5}, {'customer': 'LEILI DESIGN STUDIO', 'revenue': 44.82}, {'customer': 'J H LARSON COMPANY', 'revenue': 44.82}, {'customer': 'MST LIGHTING INC.', 'revenue': 0.0}, {'customer': 'LIGHTING FACTORY OUTLET', 'revenue': 0.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 0.0}, {'customer': 'MAPLE RIDGE LIGHTING, INC. dba', 'revenue': 0.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 0.0}, {'customer': 'JACKSON LIGHTING SUPPLY', 'revenue': 0.0}, {'customer': 'UNIVERSAL LAMP', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 0.0}, {'customer': 'ARYA GROUP INC', 'revenue': 0.0}, {'customer': 'KITCHEN SOCIETY', 'revenue': 0.0}, {'customer': 'SABRINA ROSE INTERIORS', 'revenue': 0.0}, {'customer': 'MORGANTE WILSON ARCHITECTS', 'revenue': 0.0}, {'customer': 'TREVOR CAMERON DESIGNS', 'revenue': 0.0}, {'customer': 'LAMB HOME DESIGN', 'revenue': 0.0}, {'customer': 'IMPERIO HOME', 'revenue': 0.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 0.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 0.0}, {'customer': 'BIANCA SPINAZZOLA', 'revenue': 0.0}, {'customer': 'CARIBE SALES AGENCIES, INC.', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'ASHJIAN LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 0.0}, {'customer': 'CENTRAL BULB INC', 'revenue': 0.0}] | [{'item': '519273WB', 'desc': 'Flint 3 Light Multi-Drop Pendant', 'available': 45}] |
| 505820OL | Roxy 2 Light ADA Sconce | ROXY | 63,293.97 | 566 | — | 2026-6-28 | [{'customer': 'SHADES OF LIGHT', 'revenue': 18087.32}, {'customer': 'WAYFAIR LLC', 'revenue': 5692.92}, {'customer': 'BUILD.COM', 'revenue': 4009.0}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 2846.01}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 2672.2}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 2330.16}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 2279.16}, {'customer': 'BISONOFFICE LLC', 'revenue': 2104.8}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 1395.2}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 1303.4}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 1113.6}, {'customer': 'ELEMENTS AT HOME', 'revenue': 1008.0}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 881.6}, {'customer': 'HOUZZ SHOP LLC', 'revenue': 851.2}, {'customer': 'TALLAHASSEE LIGHTING FAN', 'revenue': 822.96}, {'customer': 'LIGHTING ETC', 'revenue': 672.0}, {'customer': 'CONNECTICUT LTG CENTER', 'revenue': 672.0}, {'customer': "HORTON'S OF LA GRANGE", 'revenue': 634.4}, {'customer': 'HAUS APPEAL LLC', 'revenue': 627.2}, {'customer': 'HOME LIGHTING OF PA', 'revenue': 604.16}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 596.0}, {'customer': 'SUN LIGHTING', 'revenue': 570.4}, {'customer': 'SHALLOTTE ELECTRIC STORES', 'revenue': 556.96}, {'customer': 'SISTER LIGHTING dba', 'revenue': 512.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 505.12}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 496.0}, {'customer': 'LAMPS EXPO/LAMPCLICK.COM', 'revenue': 448.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 448.0}, {'customer': 'CREGGER COMPANY  INC', 'revenue': 438.96}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 428.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 380.0}, {'customer': 'TIDEWATER LIGHTING AND DESIGN', 'revenue': 357.32}, {'customer': 'VENICE LIGHTING COMPANY', 'revenue': 336.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 325.92}, {'customer': 'STOKES ELECTRIC', 'revenue': 302.08}, {'customer': 'MANASQUAN LIGHTING', 'revenue': 292.64}, {'customer': 'SALTBOX THE', 'revenue': 292.64}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 285.2}, {'customer': 'CRESCENT LIGHITNG SUPPLY', 'revenue': 285.2}, {'customer': 'CAMINITI ASSOCIATE  INC  ILL', 'revenue': 285.2}, {'customer': 'LIFESTYLES STORES INC', 'revenue': 285.2}, {'customer': 'FRANKLIN LIGHTING INC', 'revenue': 264.32}, {'customer': 'CHARLES RINEK', 'revenue': 264.32}, {'customer': 'N&S ELECTRIC SUPPLY  INC', 'revenue': 264.32}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 264.32}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 257.6}, {'customer': 'READ LIGHTING', 'revenue': 256.0}, {'customer': 'BRECHERS COMPANY', 'revenue': 248.0}, {'customer': 'PINE LIGHTING LTD', 'revenue': 240.8}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 240.8}, {'customer': 'ALL PHASE/TRAVERSE CITY', 'revenue': 224.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 224.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 224.0}, {'customer': '123STORES INC', 'revenue': 207.2}, {'customer': 'LAMPS PLUS', 'revenue': 201.6}, {'customer': 'LANDO LIGHTING INC', 'revenue': 201.6}, {'customer': 'M & M LIGHTING LP', 'revenue': 192.0}, {'customer': 'DEKKER LIGHTING', 'revenue': 132.16}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 128.0}, {'customer': 'CLEVELAND LIGHTING CENTER LTD', 'revenue': 124.0}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 100.8}, {'customer': 'KALCO NON A/R CASH', 'revenue': 0.0}, {'customer': 'SHOWCASE LIGHTING / LAREDO', 'revenue': 0.0}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 0.0}, {'customer': 'PHILLIPS LIGHTING & HOME', 'revenue': 0.0}, {'customer': 'LIGHTS N SUCH', 'revenue': 0.0}, {'customer': 'LIGHTING INC', 'revenue': 0.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 0.0}, {'customer': 'UNIVERSAL LAMP', 'revenue': 0.0}, {'customer': 'LIGHTHOUSE (THE)', 'revenue': 0.0}, {'customer': 'RAY ELECTRIC', 'revenue': 0.0}, {'customer': 'ASHJIAN LIGHTING', 'revenue': 0.0}, {'customer': 'DE LIGHT VILLE INC', 'revenue': 0.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 0.0}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 0.0}, {'customer': 'HOUSE OF LIGHTS INC', 'revenue': 0.0}, {'customer': 'LIGHTING EFX INC', 'revenue': 0.0}, {'customer': 'LIGHTSTYLES INC', 'revenue': 0.0}, {'customer': 'DIAL ELECTRIC SUPPLY CO.', 'revenue': 0.0}, {'customer': 'RENSENHOUSE OF LIGHTS', 'revenue': 0.0}, {'customer': 'BURR RIDGE LIGHTING & DESIGN C', 'revenue': 0.0}, {'customer': 'WILSON LIGHTING CO., INC / N.', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 0.0}, {'customer': 'KILOHANA LIGHTING/LIHUE', 'revenue': 0.0}, {'customer': 'OCEAN PACIFIC LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 0.0}, {'customer': 'LIGHTSTYLES', 'revenue': 0.0}, {'customer': 'WALNUT CREEK LIGHTING', 'revenue': 0.0}, {'customer': 'CAROLINA LANTERNS & ACCS', 'revenue': 0.0}, {'customer': "CHRISTIE'S LTG GALLERY", 'revenue': 0.0}, {'customer': 'LEGEND LIGHTING INC.', 'revenue': 0.0}, {'customer': 'STRAIT FLOORS  INC', 'revenue': 0.0}, {'customer': 'NORTHWEST ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'MILLION DECOR DESIGN, INC.', 'revenue': 0.0}, {'customer': 'BAYSIDE ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'OLD NORTH STATE IMPORTS  LLC', 'revenue': 0.0}, {'customer': 'THE PORCH SWING STORE', 'revenue': 0.0}, {'customer': 'KALCO SHOWROOM ACCOUNT', 'revenue': 0.0}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 0.0}, {'customer': 'INSIDE OUT LIVING SPACES', 'revenue': 0.0}, {'customer': 'FEIFERS', 'revenue': 0.0}, {'customer': 'HEDGEAPPLE INC', 'revenue': 0.0}, {'customer': 'JONATHONS COASTAL LIVING', 'revenue': 0.0}, {'customer': 'INSIDE OUT LIGHTING & DECOR', 'revenue': 0.0}, {'customer': 'DEL MAR DESIGNS', 'revenue': 0.0}, {'customer': 'AFP 104 CORP', 'revenue': 0.0}, {'customer': 'DAWN PATTERSON INTERIORS', 'revenue': 0.0}, {'customer': 'INSPIRED INTERIORS', 'revenue': 0.0}, {'customer': 'LINDSEY GLASS', 'revenue': 0.0}, {'customer': 'GALAXIE LIGHTING', 'revenue': 0.0}] | [{'item': '505851OL', 'desc': 'Roxy 27 Inch Pendant', 'available': 115}, {'item': '505840OL', 'desc': 'Roxy 17 Inch Semi Flush Mount', 'available': 76}, {'item': '505860OL', 'desc': 'Roxy 42 Inch Island Light', 'available': 38}, {'item': '505891OL', 'desc': 'Roxy 1 Light Table Lamp', 'available': 32}, {'item': '505852OL', 'desc': 'Roxy 33 Inch Pendant', 'available': 21}, {'item': '505850OL', 'desc': 'Roxy 2 Tier Foyer', 'available': 11}] |
| 519276WB | Flint 3 Light Full Canopy Pendant | COL429 | 61,715.78 | 95 | — | 2026-6-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 18724.89}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 7973.63}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 5592.0}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 3271.7}, {'customer': 'BUILD.COM', 'revenue': 2058.65}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 1972.48}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 1688.2}, {'customer': 'LIGHT BULBS UNLIMITED BOCA RA', 'revenue': 1634.74}, {'customer': 'WILSON LIGHTING- NAPLES', 'revenue': 1384.2}, {'customer': 'WILSON COMPANY-KANSAS', 'revenue': 1384.2}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 1153.5}, {'customer': 'LEE SUPPLY CORP', 'revenue': 1072.27}, {'customer': 'ATELIER MAISON & CO', 'revenue': 999.7}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 907.42}, {'customer': 'KRELL LIGHTING', 'revenue': 907.42}, {'customer': 'SUBURBAN WHOLESALE LTG', 'revenue': 907.42}, {'customer': 'SUNBELT FANS & LTG LAUREL', 'revenue': 907.42}, {'customer': 'CAMINITI ASSOCIATES INC. / SCO', 'revenue': 884.35}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 772.39}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 769.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 769.0}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 769.0}, {'customer': 'DEL MAR DESIGNS', 'revenue': 730.55}, {'customer': 'LAMPS PLUS', 'revenue': 713.7}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 692.1}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 576.75}, {'customer': 'IB LIGHTING SUPPLY', 'revenue': 576.75}, {'customer': 'DEMENT LIGHTING', 'revenue': 454.35}, {'customer': 'WILSON 6 ENTERPRISE', 'revenue': 384.5}, {'customer': 'LIGHTING SPECIALISTS', 'revenue': 384.5}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 349.5}, {'customer': 'M & M LIGHTING LP', 'revenue': 349.5}, {'customer': '31 DESIGNS', 'revenue': 0.0}, {'customer': 'WOLBERG ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'KTR ASSOCIATES [INACTIVE]', 'revenue': 0.0}, {'customer': 'WAYFAIR LLC', 'revenue': 0.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 0.0}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 0.0}, {'customer': 'FORESIGHT LIGHTING (DO NOT USE)', 'revenue': 0.0}, {'customer': 'LEGACY LIGHTING, LLC.', 'revenue': 0.0}, {'customer': 'SAVE MORE PLUMBING & LIGHTING', 'revenue': 0.0}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 0.0}, {'customer': 'IMPERIO HOME', 'revenue': 0.0}, {'customer': 'NOVA LIGHTING', 'revenue': 0.0}, {'customer': 'GUIDED HOME DESIGN', 'revenue': 0.0}, {'customer': 'EFIRDS INTERIORS', 'revenue': 0.0}] | — |
| 520555OL | Crescent 6 Light Pendant | COL435 | 45,102.15 | 100 | — | 2026-6-28 | [{'customer': 'LIGHTING FIRST - BONITA', 'revenue': 5050.48}, {'customer': 'BUILD.COM', 'revenue': 3834.6}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 3509.73}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 3176.46}, {'customer': 'LIGHTING FIRST', 'revenue': 2314.6}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 2268.57}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 1531.4}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 1379.7}, {'customer': 'RENSENHOUSE OF LIGHTS', 'revenue': 1277.57}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 1172.5}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 1032.0}, {'customer': 'CONNECTICUT LTG CENTER', 'revenue': 1013.16}, {'customer': "CAROL'S LIGHTING", 'revenue': 985.0}, {'customer': 'WAYFAIR LLC', 'revenue': 928.8}, {'customer': 'SISTER LIGHTING dba', 'revenue': 790.0}, {'customer': 'OLD WORLD STONE IMPORTS', 'revenue': 734.85}, {'customer': 'NORTHERN LIGHTING WESTERV', 'revenue': 608.88}, {'customer': 'KING ELECTRIC COMPANY INC', 'revenue': 608.88}, {'customer': 'BLACK WHALE LIGHTING', 'revenue': 593.4}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 562.85}, {'customer': 'CREGGER COMPANY  INC', 'revenue': 553.42}, {'customer': 'COLEY ELECTRIC AND PLUMBING', 'revenue': 553.42}, {'customer': 'LIGHTING SUPERSTORE', 'revenue': 553.42}, {'customer': 'INDIANA LIGHTING CENTER', 'revenue': 553.42}, {'customer': 'BRIGHT IDEAS LIGHTING & MORE', 'revenue': 539.35}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 539.35}, {'customer': 'THE JARRELL COMPANY', 'revenue': 516.0}, {'customer': 'WALNUT CREEK LIGHTING', 'revenue': 516.0}, {'customer': 'MARS ELECTRIC COMPANY', 'revenue': 516.0}, {'customer': 'BEAUTIFUL THINGS LIGHTING', 'revenue': 505.4}, {'customer': 'RAY ELECTRIC', 'revenue': 490.2}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 469.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 469.0}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 469.0}, {'customer': 'ROBINSON LIGHTING LTD / PLYMOU', 'revenue': 469.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 469.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 454.93}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 445.55}, {'customer': 'LEEWAL LLC', 'revenue': 438.6}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 387.0}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 387.0}, {'customer': 'VILLAGE LIGHTING', 'revenue': 328.3}, {'customer': 'PHILLIPS LIGHTING & HOME', 'revenue': 309.6}, {'customer': 'HYDROLOGIC CORPORATE', 'revenue': 234.5}, {'customer': "CHRISTIE'S LTG GALLERY", 'revenue': 234.5}, {'customer': 'CARRINGTON LIGHTING', 'revenue': 234.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 93.8}, {'customer': 'LAMP SHOP OF NAPLES COMPANY', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST / FT. MYERS', 'revenue': 0.0}, {'customer': 'ALLOWAY LIGHTING COMPANY', 'revenue': 0.0}, {'customer': 'CENTRAL BULB INC', 'revenue': 0.0}, {'customer': 'LUMINOSA LIGHT DESIGN', 'revenue': 0.0}, {'customer': 'INTERIOR WORKS', 'revenue': 0.0}, {'customer': 'J H LARSON COMPANY', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'SHALLOTTE ELECTRIC STORES', 'revenue': 0.0}, {'customer': 'BYG INC.', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 0.0}, {'customer': 'PARK LIGHTING', 'revenue': 0.0}, {'customer': 'ILLUMINATIONS MC ALLEN', 'revenue': 0.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'TURN-ON LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTTRENDS.COM', 'revenue': 0.0}, {'customer': 'EAST INDIES TRADING DBA WEST HOME COLLECTION', 'revenue': 0.0}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': -0.54}] | [{'item': '520541OL', 'desc': 'Crescent 4 Light Flush Mount', 'available': 24}, {'item': '520521OL', 'desc': 'Crescent 3 Light Ada Wall Sconce', 'available': 15}, {'item': '520561OL', 'desc': 'Crescent 5 Light Island', 'available': 7}] |
| 509952WB | Lavo 39 Inch Round LED Pendant | LAVO | 43,929.98 | 54 | — | 2026-7-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 12714.54}, {'customer': 'ILLUMINATIONS LIGHTING', 'revenue': 3624.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 2883.05}, {'customer': 'NORTH COAST ELECTRIC', 'revenue': 2661.0}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 1952.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 1952.0}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 1530.3}, {'customer': 'GRANITE CITY ELECTRIC', 'revenue': 1224.66}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 1151.68}, {'customer': 'INLINE ELECTRIC SUPPLY CO', 'revenue': 1151.68}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 1046.66}, {'customer': 'FANWORLD', 'revenue': 1020.05}, {'customer': 'COAST LIGHTING', 'revenue': 1006.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 976.0}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 976.0}, {'customer': 'KALCO MARKETING CRM', 'revenue': 976.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 976.0}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 975.7}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 927.2}, {'customer': 'LAMPS PLUS', 'revenue': 905.4}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 887.0}, {'customer': 'URBAN LIGHTS', 'revenue': 887.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 878.4}, {'customer': 'SUNBELT FANS & LTG LAUREL', 'revenue': 488.0}, {'customer': "RICHARD'S LIGHTING", 'revenue': 159.66}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': 'UNION ELECTRIC LIGHTING - TORO', 'revenue': 0.0}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 0.0}, {'customer': 'LIGHTING WAREHOUSE', 'revenue': 0.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'CAMINITI ASSOCIATE  INC  ILL', 'revenue': 0.0}, {'customer': 'LBX LIGHTING INC', 'revenue': 0.0}, {'customer': 'PARK LIGHTING', 'revenue': 0.0}, {'customer': 'KEIDEL SUPPLY CO. INC.', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 0.0}, {'customer': 'INSPIRED LIVING STORES', 'revenue': 0.0}, {'customer': 'AZTEC LIGHTING INC', 'revenue': 0.0}, {'customer': 'STATELY LLC', 'revenue': 0.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 0.0}, {'customer': 'LIGHTING FACTORY OUTLET', 'revenue': 0.0}, {'customer': 'STYLEUP CORPORATION', 'revenue': 0.0}, {'customer': 'SUN LIGHTING', 'revenue': 0.0}, {'customer': 'SEMCO ELECTRIC', 'revenue': 0.0}, {'customer': 'SUPPLY HOLDING', 'revenue': 0.0}, {'customer': 'ONE SOURCE LIGHTING', 'revenue': 0.0}, {'customer': 'ILC STUDIOS', 'revenue': 0.0}, {'customer': 'AARON THOMAS INTERIORS', 'revenue': 0.0}, {'customer': 'I.D. HOME LOGISTICS INC', 'revenue': 0.0}, {'customer': 'SCOUT LIGHTING', 'revenue': 0.0}, {'customer': 'ALDER AND TWEED DESIGN CO.', 'revenue': 0.0}, {'customer': 'LIGHTING SOLUTIONS & DESIGN', 'revenue': 0.0}, {'customer': 'A A PORTER LTG CO (DO NOT CONTACT)', 'revenue': 0.0}] | [{'item': '509921WB', 'desc': 'Lavo LED ADA Wall Sconce', 'available': 25}, {'item': '509950WB', 'desc': 'Lavo 28 Inch Round LED Pendant', 'available': 13}] |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 037249-184-FR102 | Alta 3 Orb Pendant (18+26+36) | ALTA | 0 | 0 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14096.7}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 11198.0}] |
| 037250-010-FR001 | Alta 3 Orb Pendant (26+26+36) | ALTA | 1 | 0 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14096.7}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 11198.0}] |
| 037250-184-FR102 | Alta 3 Orb Pendant (26+26+36) | ALTA | 1 | 7,469.10 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 11198.0}] |
| 037251-184-FR102 | Alta 3 Orb Pendant (18+18+18) | ALTA | 0 | 0 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14096.7}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 11198.0}] |
| 037252-184-FR102 | Alta 3 Orb Pendant (26+26+26) | ALTA | 0 | 0 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14096.7}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 11198.0}] |
| 037253-184-FR102 | Alta 3 Orb Pendant (18+26+26) | ALTA | 1 | 11,198 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14096.7}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}] |
| 037254-184-FR102 | Alta 3 Orb Pendant (18+18+26) | ALTA | 0 | 0 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 16980.78}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14096.7}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 13049.55}, {'customer_code': '0001802', 'customer_name': "HINKLEY'S LTG FACTORY", 'collection_revenue': 11305.0}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 11198.0}] |
| 045321-003-FR1VR | Bella Wall Sconce | BELLA | 2 | 1,251.10 | — |
| 045351-003-FR1VR | Bella Foyer Light | BELLA | 0 | 0 | — |
| 045355-003-FR1VR | Bella 26 In Pendant | BELLA | 0 | 0 | — |
| 045356-003-FR1VR | Bella 32 In Pendant | BELLA | 0 | 0 | — |
| 045361-003-FR1VR | Bella Island Light | BELLA | 2 | 2,249 | — |
| 528311WBWT | Bolsa 6.5-in 1 Light (40-watt) Winter Brass Pendant | BOLSA | 0 | 0 | — |
| 528312WBWT | Bolsa 8-in 1 Light (40-watt) Winter Brass Pendant | BOLSA | 0 | 0 | — |
| 528352WBWT | Bolsa 31-in 6 Light (40-watt) Winter Brass Chandelier | BOLSA | 0 | 0 | — |
| 030210-184 | Glacier 10-in (26-watt) LED Black Nickel Chandelier | COL185 | 1 | 324.50 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 88651.47}, {'customer_code': '0001416', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 62287.97}, {'customer_code': '0004961', 'customer_name': 'LIGHTING NEW YORK (INTERNET)', 'collection_revenue': 59326.06}, {'customer_code': '0002274', 'customer_name': 'CAPITOL LIGHTING BOCA RATON', 'collection_revenue': 56668.17}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 50656.38}, {'customer_code': '0002233', 'customer_name': 'FRANKLIN LIGHTING INC', 'collection_revenue': 42986.62}, {'customer_code': '0001414', 'customer_name': 'HYE LIGHTING CO INC', 'collection_revenue': 41409.2}, {'customer_code': '0010558', 'customer_name': 'CLIVE DANIEL HOME', 'collection_revenue': 39004.1}, {'customer_code': '0010507', 'customer_name': 'MI CASA LIGHTING AND FAN', 'collection_revenue': 37060.62}, {'customer_code': '0005789', 'customer_name': 'DESIGNER LIGHTING & FAN/DECOR', 'collection_revenue': 33890.94}, {'customer_code': '0001332', 'customer_name': 'LYTEWORKS', 'collection_revenue': 33037.02}, {'customer_code': '0003937', 'customer_name': 'LUMENS LIGHT & LIVING', 'collection_revenue': 29634.71}, {'customer_code': '0003483', 'customer_name': 'THE LIGHT HOUSE', 'collection_revenue': 23608.85}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 23209.06}, {'customer_code': '0005456', 'customer_name': 'WAYFAIR LLC', 'collection_revenue': 22736.81}, {'customer_code': '0001015', 'customer_name': 'LIGHTING INC', 'collection_revenue': 22371.15}, {'customer_code': '0002958', 'customer_name': 'UNIVERSAL LIGHTS', 'collection_revenue': 21765.2}, {'customer_code': '0005391', 'customer_name': 'NAPLES LIGHTING & FAN DEPOT', 'collection_revenue': 19694.07}, {'customer_code': '0002190', 'customer_name': 'LITTMAN BROTHERS BROTHERS', 'collection_revenue': 19448.1}, {'customer_code': '0002855', 'customer_name': 'BEAUTIFUL THINGS LIGHTING', 'collection_revenue': 18885.26}, {'customer_code': '0005575', 'customer_name': 'CAPITOL LIGHTING / 1-800LIGHTI', 'collection_revenue': 17941.35}, {'customer_code': '0010583', 'customer_name': 'NEIMAN MARCUS', 'collection_revenue': 17543.8}, {'customer_code': '0003006', 'customer_name': 'LIGHTING WORLD DECORATOR', 'collection_revenue': 17480.59}, {'customer_code': '0003448', 'customer_name': 'LAMP & SHADE WORKS SEWELL', 'collection_revenue': 16824.0}, {'customer_code': '0002933', 'customer_name': 'WILSON LIGHTING- NAPLES', 'collection_revenue': 16210.62}, {'customer_code': '0003285', 'customer_name': 'LIGHTSTYLE OF ORLANDO', 'collection_revenue': 15016.0}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14244.3}, {'customer_code': '0002131', 'customer_name': 'ELEMENTS AT HOME', 'collection_revenue': 13784.4}, {'customer_code': '0005299', 'customer_name': 'RBDELAA LIGHTING', 'collection_revenue': 13768.5}, {'customer_code': '0002321', 'customer_name': 'DOLAN NORTHWEST LLC  PORTLAND', 'collection_revenue': 13740.4}, {'customer_code': '0010457', 'customer_name': 'IB LIGHTING SUPPLY', 'collection_revenue': 13545.85}, {'customer_code': '0003014', 'customer_name': 'Lighting Design Center', 'collection_revenue': 12898.0}, {'customer_code': '0005517', 'customer_name': 'LBX LIGHTING INC', 'collection_revenue': 12235.5}, {'customer_code': '0010745', 'customer_name': 'B. COLLECTIVE CO.', 'collection_revenue': 12235.0}, {'customer_code': '0004803', 'customer_name': 'BELAMI, INC / 1STOP LIGHTING', 'collection_revenue': 12142.46}, {'customer_code': '0010267', 'customer_name': 'WINSUPPLY OF ALBUQUERQUE', 'collection_revenue': 11838.4}, {'customer_code': '0010591', 'customer_name': 'LEEWAL LLC', 'collection_revenue': 11834.5}, {'customer_code': '0005461', 'customer_name': 'N&S ELECTRIC SUPPLY  INC', 'collection_revenue': 11815.0}, {'customer_code': '0010693', 'customer_name': 'SKLAR FURNISHINGS', 'collection_revenue': 11666.0}, {'customer_code': '0006064', 'customer_name': 'LIGHTOPIA, LLC', 'collection_revenue': 11400.5}, {'customer_code': '0010587', 'customer_name': 'WINSUPPLY HENDERSONVILLE', 'collection_revenue': 11366.5}, {'customer_code': '0002316', 'customer_name': 'HOUSE OF LIGHTS INC', 'collection_revenue': 11125.35}, {'customer_code': '0001859', 'customer_name': 'RAY ELECTRIC', 'collection_revenue': 10766.27}, {'customer_code': '0002608', 'customer_name': 'LIGHTING SUPERSTORE', 'collection_revenue': 10732.75}, {'customer_code': '0006041', 'customer_name': 'CONSUMERS LIGHTING AND LAMPS L', 'collection_revenue': 10700.76}, {'customer_code': '0001549', 'customer_name': 'SOUTH DADE LIGHTING INC\\M', 'collection_revenue': 10692.8}] |
| 030250-184 | Glacier 42-in (40-watt) LED Black Nickel Wave Linear Chandelier | COL185 | 1 | 949.50 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 88651.47}, {'customer_code': '0001416', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 62287.97}, {'customer_code': '0004961', 'customer_name': 'LIGHTING NEW YORK (INTERNET)', 'collection_revenue': 59326.06}, {'customer_code': '0002274', 'customer_name': 'CAPITOL LIGHTING BOCA RATON', 'collection_revenue': 56668.17}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 50656.38}, {'customer_code': '0002233', 'customer_name': 'FRANKLIN LIGHTING INC', 'collection_revenue': 42986.62}, {'customer_code': '0001414', 'customer_name': 'HYE LIGHTING CO INC', 'collection_revenue': 41409.2}, {'customer_code': '0010558', 'customer_name': 'CLIVE DANIEL HOME', 'collection_revenue': 39004.1}, {'customer_code': '0010507', 'customer_name': 'MI CASA LIGHTING AND FAN', 'collection_revenue': 37060.62}, {'customer_code': '0005789', 'customer_name': 'DESIGNER LIGHTING & FAN/DECOR', 'collection_revenue': 33890.94}, {'customer_code': '0001332', 'customer_name': 'LYTEWORKS', 'collection_revenue': 33037.02}, {'customer_code': '0003937', 'customer_name': 'LUMENS LIGHT & LIVING', 'collection_revenue': 29634.71}, {'customer_code': '0003483', 'customer_name': 'THE LIGHT HOUSE', 'collection_revenue': 23608.85}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 23209.06}, {'customer_code': '0005456', 'customer_name': 'WAYFAIR LLC', 'collection_revenue': 22736.81}, {'customer_code': '0001015', 'customer_name': 'LIGHTING INC', 'collection_revenue': 22371.15}, {'customer_code': '0002958', 'customer_name': 'UNIVERSAL LIGHTS', 'collection_revenue': 21765.2}, {'customer_code': '0005391', 'customer_name': 'NAPLES LIGHTING & FAN DEPOT', 'collection_revenue': 19694.07}, {'customer_code': '0002190', 'customer_name': 'LITTMAN BROTHERS BROTHERS', 'collection_revenue': 19448.1}, {'customer_code': '0002855', 'customer_name': 'BEAUTIFUL THINGS LIGHTING', 'collection_revenue': 18885.26}, {'customer_code': '0005575', 'customer_name': 'CAPITOL LIGHTING / 1-800LIGHTI', 'collection_revenue': 17941.35}, {'customer_code': '0010583', 'customer_name': 'NEIMAN MARCUS', 'collection_revenue': 17543.8}, {'customer_code': '0003006', 'customer_name': 'LIGHTING WORLD DECORATOR', 'collection_revenue': 17480.59}, {'customer_code': '0003448', 'customer_name': 'LAMP & SHADE WORKS SEWELL', 'collection_revenue': 16824.0}, {'customer_code': '0002933', 'customer_name': 'WILSON LIGHTING- NAPLES', 'collection_revenue': 16210.62}, {'customer_code': '0003285', 'customer_name': 'LIGHTSTYLE OF ORLANDO', 'collection_revenue': 15016.0}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14244.3}, {'customer_code': '0002131', 'customer_name': 'ELEMENTS AT HOME', 'collection_revenue': 13784.4}, {'customer_code': '0005299', 'customer_name': 'RBDELAA LIGHTING', 'collection_revenue': 13768.5}, {'customer_code': '0002321', 'customer_name': 'DOLAN NORTHWEST LLC  PORTLAND', 'collection_revenue': 13740.4}, {'customer_code': '0010457', 'customer_name': 'IB LIGHTING SUPPLY', 'collection_revenue': 13545.85}, {'customer_code': '0003014', 'customer_name': 'Lighting Design Center', 'collection_revenue': 12898.0}, {'customer_code': '0005517', 'customer_name': 'LBX LIGHTING INC', 'collection_revenue': 12235.5}, {'customer_code': '0010745', 'customer_name': 'B. COLLECTIVE CO.', 'collection_revenue': 12235.0}, {'customer_code': '0004803', 'customer_name': 'BELAMI, INC / 1STOP LIGHTING', 'collection_revenue': 12142.46}, {'customer_code': '0010267', 'customer_name': 'WINSUPPLY OF ALBUQUERQUE', 'collection_revenue': 11838.4}, {'customer_code': '0010591', 'customer_name': 'LEEWAL LLC', 'collection_revenue': 11834.5}, {'customer_code': '0005461', 'customer_name': 'N&S ELECTRIC SUPPLY  INC', 'collection_revenue': 11815.0}, {'customer_code': '0010693', 'customer_name': 'SKLAR FURNISHINGS', 'collection_revenue': 11666.0}, {'customer_code': '0001139', 'customer_name': 'SOUTHERN LIGHTING INC', 'collection_revenue': 11608.5}, {'customer_code': '0006064', 'customer_name': 'LIGHTOPIA, LLC', 'collection_revenue': 11400.5}, {'customer_code': '0010587', 'customer_name': 'WINSUPPLY HENDERSONVILLE', 'collection_revenue': 11366.5}, {'customer_code': '0002316', 'customer_name': 'HOUSE OF LIGHTS INC', 'collection_revenue': 11125.35}, {'customer_code': '0001859', 'customer_name': 'RAY ELECTRIC', 'collection_revenue': 10766.27}, {'customer_code': '0002608', 'customer_name': 'LIGHTING SUPERSTORE', 'collection_revenue': 10732.75}, {'customer_code': '0006041', 'customer_name': 'CONSUMERS LIGHTING AND LAMPS L', 'collection_revenue': 10700.76}, {'customer_code': '0001549', 'customer_name': 'SOUTH DADE LIGHTING INC\\M', 'collection_revenue': 10692.8}] |
| 030255-184 | Glacier 32-in (94-watt) LED Black Nickel Chandelier | COL185 | 2 | 5,098.50 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 88651.47}, {'customer_code': '0001416', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 62287.97}, {'customer_code': '0004961', 'customer_name': 'LIGHTING NEW YORK (INTERNET)', 'collection_revenue': 59326.06}, {'customer_code': '0002274', 'customer_name': 'CAPITOL LIGHTING BOCA RATON', 'collection_revenue': 56668.17}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 50656.38}, {'customer_code': '0002233', 'customer_name': 'FRANKLIN LIGHTING INC', 'collection_revenue': 42986.62}, {'customer_code': '0001414', 'customer_name': 'HYE LIGHTING CO INC', 'collection_revenue': 41409.2}, {'customer_code': '0010558', 'customer_name': 'CLIVE DANIEL HOME', 'collection_revenue': 39004.1}, {'customer_code': '0010507', 'customer_name': 'MI CASA LIGHTING AND FAN', 'collection_revenue': 37060.62}, {'customer_code': '0005789', 'customer_name': 'DESIGNER LIGHTING & FAN/DECOR', 'collection_revenue': 33890.94}, {'customer_code': '0001332', 'customer_name': 'LYTEWORKS', 'collection_revenue': 33037.02}, {'customer_code': '0003937', 'customer_name': 'LUMENS LIGHT & LIVING', 'collection_revenue': 29634.71}, {'customer_code': '0003483', 'customer_name': 'THE LIGHT HOUSE', 'collection_revenue': 23608.85}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 23209.06}, {'customer_code': '0005456', 'customer_name': 'WAYFAIR LLC', 'collection_revenue': 22736.81}, {'customer_code': '0001015', 'customer_name': 'LIGHTING INC', 'collection_revenue': 22371.15}, {'customer_code': '0002958', 'customer_name': 'UNIVERSAL LIGHTS', 'collection_revenue': 21765.2}, {'customer_code': '0005391', 'customer_name': 'NAPLES LIGHTING & FAN DEPOT', 'collection_revenue': 19694.07}, {'customer_code': '0002190', 'customer_name': 'LITTMAN BROTHERS BROTHERS', 'collection_revenue': 19448.1}, {'customer_code': '0002855', 'customer_name': 'BEAUTIFUL THINGS LIGHTING', 'collection_revenue': 18885.26}, {'customer_code': '0005575', 'customer_name': 'CAPITOL LIGHTING / 1-800LIGHTI', 'collection_revenue': 17941.35}, {'customer_code': '0010583', 'customer_name': 'NEIMAN MARCUS', 'collection_revenue': 17543.8}, {'customer_code': '0003006', 'customer_name': 'LIGHTING WORLD DECORATOR', 'collection_revenue': 17480.59}, {'customer_code': '0003448', 'customer_name': 'LAMP & SHADE WORKS SEWELL', 'collection_revenue': 16824.0}, {'customer_code': '0002933', 'customer_name': 'WILSON LIGHTING- NAPLES', 'collection_revenue': 16210.62}, {'customer_code': '0003285', 'customer_name': 'LIGHTSTYLE OF ORLANDO', 'collection_revenue': 15016.0}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14244.3}, {'customer_code': '0002131', 'customer_name': 'ELEMENTS AT HOME', 'collection_revenue': 13784.4}, {'customer_code': '0005299', 'customer_name': 'RBDELAA LIGHTING', 'collection_revenue': 13768.5}, {'customer_code': '0002321', 'customer_name': 'DOLAN NORTHWEST LLC  PORTLAND', 'collection_revenue': 13740.4}, {'customer_code': '0010457', 'customer_name': 'IB LIGHTING SUPPLY', 'collection_revenue': 13545.85}, {'customer_code': '0003014', 'customer_name': 'Lighting Design Center', 'collection_revenue': 12898.0}, {'customer_code': '0005517', 'customer_name': 'LBX LIGHTING INC', 'collection_revenue': 12235.5}, {'customer_code': '0010745', 'customer_name': 'B. COLLECTIVE CO.', 'collection_revenue': 12235.0}, {'customer_code': '0004803', 'customer_name': 'BELAMI, INC / 1STOP LIGHTING', 'collection_revenue': 12142.46}, {'customer_code': '0010267', 'customer_name': 'WINSUPPLY OF ALBUQUERQUE', 'collection_revenue': 11838.4}, {'customer_code': '0010591', 'customer_name': 'LEEWAL LLC', 'collection_revenue': 11834.5}, {'customer_code': '0005461', 'customer_name': 'N&S ELECTRIC SUPPLY  INC', 'collection_revenue': 11815.0}, {'customer_code': '0010693', 'customer_name': 'SKLAR FURNISHINGS', 'collection_revenue': 11666.0}, {'customer_code': '0001139', 'customer_name': 'SOUTHERN LIGHTING INC', 'collection_revenue': 11608.5}, {'customer_code': '0006064', 'customer_name': 'LIGHTOPIA, LLC', 'collection_revenue': 11400.5}, {'customer_code': '0002316', 'customer_name': 'HOUSE OF LIGHTS INC', 'collection_revenue': 11125.35}, {'customer_code': '0001859', 'customer_name': 'RAY ELECTRIC', 'collection_revenue': 10766.27}, {'customer_code': '0002608', 'customer_name': 'LIGHTING SUPERSTORE', 'collection_revenue': 10732.75}, {'customer_code': '0006041', 'customer_name': 'CONSUMERS LIGHTING AND LAMPS L', 'collection_revenue': 10700.76}, {'customer_code': '0001549', 'customer_name': 'SOUTH DADE LIGHTING INC\\M', 'collection_revenue': 10692.8}] |
| 030258-184 | Glacier 60-in (60-watt) LED Black Nickel Wave Linear Chandelier | COL185 | 2 | 5,747.70 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 88651.47}, {'customer_code': '0001416', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 62287.97}, {'customer_code': '0004961', 'customer_name': 'LIGHTING NEW YORK (INTERNET)', 'collection_revenue': 59326.06}, {'customer_code': '0002274', 'customer_name': 'CAPITOL LIGHTING BOCA RATON', 'collection_revenue': 56668.17}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 50656.38}, {'customer_code': '0002233', 'customer_name': 'FRANKLIN LIGHTING INC', 'collection_revenue': 42986.62}, {'customer_code': '0001414', 'customer_name': 'HYE LIGHTING CO INC', 'collection_revenue': 41409.2}, {'customer_code': '0010558', 'customer_name': 'CLIVE DANIEL HOME', 'collection_revenue': 39004.1}, {'customer_code': '0010507', 'customer_name': 'MI CASA LIGHTING AND FAN', 'collection_revenue': 37060.62}, {'customer_code': '0005789', 'customer_name': 'DESIGNER LIGHTING & FAN/DECOR', 'collection_revenue': 33890.94}, {'customer_code': '0001332', 'customer_name': 'LYTEWORKS', 'collection_revenue': 33037.02}, {'customer_code': '0003937', 'customer_name': 'LUMENS LIGHT & LIVING', 'collection_revenue': 29634.71}, {'customer_code': '0003483', 'customer_name': 'THE LIGHT HOUSE', 'collection_revenue': 23608.85}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 23209.06}, {'customer_code': '0005456', 'customer_name': 'WAYFAIR LLC', 'collection_revenue': 22736.81}, {'customer_code': '0001015', 'customer_name': 'LIGHTING INC', 'collection_revenue': 22371.15}, {'customer_code': '0002958', 'customer_name': 'UNIVERSAL LIGHTS', 'collection_revenue': 21765.2}, {'customer_code': '0005391', 'customer_name': 'NAPLES LIGHTING & FAN DEPOT', 'collection_revenue': 19694.07}, {'customer_code': '0002190', 'customer_name': 'LITTMAN BROTHERS BROTHERS', 'collection_revenue': 19448.1}, {'customer_code': '0002855', 'customer_name': 'BEAUTIFUL THINGS LIGHTING', 'collection_revenue': 18885.26}, {'customer_code': '0005575', 'customer_name': 'CAPITOL LIGHTING / 1-800LIGHTI', 'collection_revenue': 17941.35}, {'customer_code': '0010583', 'customer_name': 'NEIMAN MARCUS', 'collection_revenue': 17543.8}, {'customer_code': '0003006', 'customer_name': 'LIGHTING WORLD DECORATOR', 'collection_revenue': 17480.59}, {'customer_code': '0003448', 'customer_name': 'LAMP & SHADE WORKS SEWELL', 'collection_revenue': 16824.0}, {'customer_code': '0002933', 'customer_name': 'WILSON LIGHTING- NAPLES', 'collection_revenue': 16210.62}, {'customer_code': '0003285', 'customer_name': 'LIGHTSTYLE OF ORLANDO', 'collection_revenue': 15016.0}, {'customer_code': '0002131', 'customer_name': 'ELEMENTS AT HOME', 'collection_revenue': 13784.4}, {'customer_code': '0005299', 'customer_name': 'RBDELAA LIGHTING', 'collection_revenue': 13768.5}, {'customer_code': '0002321', 'customer_name': 'DOLAN NORTHWEST LLC  PORTLAND', 'collection_revenue': 13740.4}, {'customer_code': '0010457', 'customer_name': 'IB LIGHTING SUPPLY', 'collection_revenue': 13545.85}, {'customer_code': '0003014', 'customer_name': 'Lighting Design Center', 'collection_revenue': 12898.0}, {'customer_code': '0005517', 'customer_name': 'LBX LIGHTING INC', 'collection_revenue': 12235.5}, {'customer_code': '0010745', 'customer_name': 'B. COLLECTIVE CO.', 'collection_revenue': 12235.0}, {'customer_code': '0004803', 'customer_name': 'BELAMI, INC / 1STOP LIGHTING', 'collection_revenue': 12142.46}, {'customer_code': '0010267', 'customer_name': 'WINSUPPLY OF ALBUQUERQUE', 'collection_revenue': 11838.4}, {'customer_code': '0010591', 'customer_name': 'LEEWAL LLC', 'collection_revenue': 11834.5}, {'customer_code': '0005461', 'customer_name': 'N&S ELECTRIC SUPPLY  INC', 'collection_revenue': 11815.0}, {'customer_code': '0010693', 'customer_name': 'SKLAR FURNISHINGS', 'collection_revenue': 11666.0}, {'customer_code': '0001139', 'customer_name': 'SOUTHERN LIGHTING INC', 'collection_revenue': 11608.5}, {'customer_code': '0006064', 'customer_name': 'LIGHTOPIA, LLC', 'collection_revenue': 11400.5}, {'customer_code': '0010587', 'customer_name': 'WINSUPPLY HENDERSONVILLE', 'collection_revenue': 11366.5}, {'customer_code': '0002316', 'customer_name': 'HOUSE OF LIGHTS INC', 'collection_revenue': 11125.35}, {'customer_code': '0001859', 'customer_name': 'RAY ELECTRIC', 'collection_revenue': 10766.27}, {'customer_code': '0002608', 'customer_name': 'LIGHTING SUPERSTORE', 'collection_revenue': 10732.75}, {'customer_code': '0006041', 'customer_name': 'CONSUMERS LIGHTING AND LAMPS L', 'collection_revenue': 10700.76}, {'customer_code': '0001549', 'customer_name': 'SOUTH DADE LIGHTING INC\\M', 'collection_revenue': 10692.8}] |
| 030260-184 | Glacier 48-in (108-watt) LED Black Nickel Linear Chandelier | COL185 | 2 | 3,699 | [{'customer_code': '0010023', 'customer_name': 'FEI  FERGUSON MAIN ACCOUNT', 'collection_revenue': 88651.47}, {'customer_code': '0001416', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 62287.97}, {'customer_code': '0004961', 'customer_name': 'LIGHTING NEW YORK (INTERNET)', 'collection_revenue': 59326.06}, {'customer_code': '0002274', 'customer_name': 'CAPITOL LIGHTING BOCA RATON', 'collection_revenue': 56668.17}, {'customer_code': '0004575', 'customer_name': 'BUILD.COM', 'collection_revenue': 50656.38}, {'customer_code': '0002233', 'customer_name': 'FRANKLIN LIGHTING INC', 'collection_revenue': 42986.62}, {'customer_code': '0001414', 'customer_name': 'HYE LIGHTING CO INC', 'collection_revenue': 41409.2}, {'customer_code': '0010558', 'customer_name': 'CLIVE DANIEL HOME', 'collection_revenue': 39004.1}, {'customer_code': '0005789', 'customer_name': 'DESIGNER LIGHTING & FAN/DECOR', 'collection_revenue': 33890.94}, {'customer_code': '0001332', 'customer_name': 'LYTEWORKS', 'collection_revenue': 33037.02}, {'customer_code': '0003937', 'customer_name': 'LUMENS LIGHT & LIVING', 'collection_revenue': 29634.71}, {'customer_code': '0003483', 'customer_name': 'THE LIGHT HOUSE', 'collection_revenue': 23608.85}, {'customer_code': '0002266', 'customer_name': 'FANWORLD', 'collection_revenue': 23209.06}, {'customer_code': '0005456', 'customer_name': 'WAYFAIR LLC', 'collection_revenue': 22736.81}, {'customer_code': '0001015', 'customer_name': 'LIGHTING INC', 'collection_revenue': 22371.15}, {'customer_code': '0002958', 'customer_name': 'UNIVERSAL LIGHTS', 'collection_revenue': 21765.2}, {'customer_code': '0005391', 'customer_name': 'NAPLES LIGHTING & FAN DEPOT', 'collection_revenue': 19694.07}, {'customer_code': '0002190', 'customer_name': 'LITTMAN BROTHERS BROTHERS', 'collection_revenue': 19448.1}, {'customer_code': '0002855', 'customer_name': 'BEAUTIFUL THINGS LIGHTING', 'collection_revenue': 18885.26}, {'customer_code': '0005575', 'customer_name': 'CAPITOL LIGHTING / 1-800LIGHTI', 'collection_revenue': 17941.35}, {'customer_code': '0010583', 'customer_name': 'NEIMAN MARCUS', 'collection_revenue': 17543.8}, {'customer_code': '0003006', 'customer_name': 'LIGHTING WORLD DECORATOR', 'collection_revenue': 17480.59}, {'customer_code': '0003448', 'customer_name': 'LAMP & SHADE WORKS SEWELL', 'collection_revenue': 16824.0}, {'customer_code': '0002933', 'customer_name': 'WILSON LIGHTING- NAPLES', 'collection_revenue': 16210.62}, {'customer_code': '0003285', 'customer_name': 'LIGHTSTYLE OF ORLANDO', 'collection_revenue': 15016.0}, {'customer_code': '0000967', 'customer_name': 'VALLEY LGT GALLERY', 'collection_revenue': 14244.3}, {'customer_code': '0002131', 'customer_name': 'ELEMENTS AT HOME', 'collection_revenue': 13784.4}, {'customer_code': '0005299', 'customer_name': 'RBDELAA LIGHTING', 'collection_revenue': 13768.5}, {'customer_code': '0002321', 'customer_name': 'DOLAN NORTHWEST LLC  PORTLAND', 'collection_revenue': 13740.4}, {'customer_code': '0010457', 'customer_name': 'IB LIGHTING SUPPLY', 'collection_revenue': 13545.85}, {'customer_code': '0003014', 'customer_name': 'Lighting Design Center', 'collection_revenue': 12898.0}, {'customer_code': '0005517', 'customer_name': 'LBX LIGHTING INC', 'collection_revenue': 12235.5}, {'customer_code': '0010745', 'customer_name': 'B. COLLECTIVE CO.', 'collection_revenue': 12235.0}, {'customer_code': '0004803', 'customer_name': 'BELAMI, INC / 1STOP LIGHTING', 'collection_revenue': 12142.46}, {'customer_code': '0010267', 'customer_name': 'WINSUPPLY OF ALBUQUERQUE', 'collection_revenue': 11838.4}, {'customer_code': '0010591', 'customer_name': 'LEEWAL LLC', 'collection_revenue': 11834.5}, {'customer_code': '0005461', 'customer_name': 'N&S ELECTRIC SUPPLY  INC', 'collection_revenue': 11815.0}, {'customer_code': '0010693', 'customer_name': 'SKLAR FURNISHINGS', 'collection_revenue': 11666.0}, {'customer_code': '0001139', 'customer_name': 'SOUTHERN LIGHTING INC', 'collection_revenue': 11608.5}, {'customer_code': '0006064', 'customer_name': 'LIGHTOPIA, LLC', 'collection_revenue': 11400.5}, {'customer_code': '0010587', 'customer_name': 'WINSUPPLY HENDERSONVILLE', 'collection_revenue': 11366.5}, {'customer_code': '0002316', 'customer_name': 'HOUSE OF LIGHTS INC', 'collection_revenue': 11125.35}, {'customer_code': '0001859', 'customer_name': 'RAY ELECTRIC', 'collection_revenue': 10766.27}, {'customer_code': '0002608', 'customer_name': 'LIGHTING SUPERSTORE', 'collection_revenue': 10732.75}, {'customer_code': '0006041', 'customer_name': 'CONSUMERS LIGHTING AND LAMPS L', 'collection_revenue': 10700.76}, {'customer_code': '0001549', 'customer_name': 'SOUTH DADE LIGHTING INC\\M', 'collection_revenue': 10692.8}] |
| 040855-010-FR001 | FONTANA 61 IN PENDANT | COL230 | 1 | 4,374.50 | — |
| 037521-010-FR001 | NUVOLE WALL SCONCE | COL248 | 1 | 149.25 | — |
| 040056-010-FR001-RGBW | Lina Colorata 14" RGBW Pendant | COL27 | 0 | 0 | — |
| 040056-010-FR1AQCG | Lina Colorata 14" Pendant | COL27 | 0 | 0 | — |
| 040057-010-FR001-RGBW | Lina Colorata 18" RGBW Pendant | COL27 | 1 | 714.50 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
