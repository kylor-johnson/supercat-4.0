# Section 3 Context Bundle — Vaxcel International Corporation (vic)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Vaxcel International Corporation (vic, org_id=176)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=52093, portal_order_gmv=$9.5M |
| HAS_INVENTORY | True | inventory_count=1190 |
| HAS_SALES_DATA | True | sales_data_count=198255 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=0 engagement_reps=10 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Catalog-Focused |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | vaxcel_international_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$9.5M > ecat_gmv=$28,345: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 0 | 0 |
| ENGAGEMENT_REP_COUNT | 10 | engagement_reps=10 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 32 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 93, Mixpanel total submit_order (Q-01): 1 |
| USER_GROUP_SPLIT_AVAILABLE | True | join_rate=96.9%, ambiguous_rate=0.0%, showroom_event_share=28.5% |
| USER_GROUP_JOIN_RATE | 97% | 31 of 32 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 29% | showroom+admin share of matched events: 28.5% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=6 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=476 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 7d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=115 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Vaxcel International Corporation
- **Shortname**: vic
- **Org ID**: 176
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Vaxcel International Corporation (vic, org_id=176)
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

# Signal Rank — Vaxcel International Corporation (vic, org_id=176)
- **Run date**: 2026-06-17
- **Total signals fired**: 23 (P0: 8, P1: 14, P2: 1)
- **Org GMV**: $0.0M eCat LTM, $9.5M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-01 | Next Best Product — C0281/C0280 co-purchase pattern across 26 customers | P0 | §2/§3 | 2.6 | $45,579,720 | 2.0 | 237,014,546 | POSITIVE |
| 2 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.1M+ total business, zero eCat orders | P1 | §2 Accounts | 8.1 | $8,135,489 | 2.0 | 132,372,363 | POSITIVE |
| 3 | SIG-DECAY-04 | Spending Contraction — Menards DC DIST #3039 -78.4% YoY ($300,730→$65,047), $235,683 gap | P0 | §2 Accounts | 3.9 | $235,683 | 3.0 | 2,771,632 | RISK |
| 4 | SIG-MOM-01 | Account Acceleration — Ace Hardware Corporation 2 consecutive QoQ acceleration quarters, $53,900 peak quarter (+439% QoQ) | P0 | §2 Accounts | 14.6 | $53,900 | 3.0 | 2,364,589 | POSITIVE |
| 5 | SIG-DECAY-04 | Spending Contraction — HomeDepot.com -24.9% YoY ($1,587,995→$1,191,892), $396,103 gap | P0 | §2 Accounts | 1.2 | $396,103 | 3.0 | 1,479,443 | RISK |
| 6 | SIG-COMMERCE-01 | Capture Rate — eCat captures 0.3% of $10M total business; each +1pt = $95K | P0 | §4 Commerce | 5.0 | $95,000 | 3.0 | 1,420,748 | POSITIVE |
| 7 | SIG-MOM-01 | Account Acceleration — Walmart.com 2 consecutive QoQ acceleration quarters, $19,549 peak quarter (+96% QoQ) | P0 | §2 Accounts | 3.2 | $19,549 | 3.0 | 188,258 | POSITIVE |
| 8 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |
| 9 | SIG-DECAY-04 | Spending Contraction — Belami, Inc. -25.1% YoY ($140,796→$105,442), $35,354 gap | P0 | §2 Accounts | 1.3 | $35,354 | 3.0 | 133,107 | RISK |
| 10 | SIG-DECAY-04 | Spending Contraction — Lighting New York -25.5% YoY ($93,402→$69,539), $23,864 gap | P0 | §2 Accounts | 1.3 | $23,864 | 3.0 | 91,279 | RISK |
| 11 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 59% of eCat GMV | P1 | §4 Commerce | 1.5 | $16,302 | 2.0 | 48,114 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — riser_prices last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — placement_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — options last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — option_groups last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — matrix_options last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — kit_items last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 7 | 1 | 0 | 8 | |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 12 | 0 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — C0281/C0280 co-purchase pattern across 26 customers
2. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.1M+ total business, zero eCat orders
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Ace Hardware Corporation 2 consecutive QoQ acceleration quarters, $53,900 peak quarter (+439% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 0.3% of $10M total business; each +1pt = $95K
5. **[RISK]** SIG-DECAY-04: Spending Contraction — Menards DC DIST #3039 -78.4% YoY ($300,730→$65,047), $235,683 gap
6. **[RISK]** SIG-DECAY-04: Spending Contraction — HomeDepot.com -24.9% YoY ($1,587,995→$1,191,892), $396,103 gap
7. **[RISK]** SIG-DECAY-04: Spending Contraction — Belami, Inc. -25.1% YoY ($140,796→$105,442), $35,354 gap

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,112 | 0 | 1,112 | 0 |

### Q-37_results.md

# Q-37 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0307 | — | — | — | $153,895 | 828 | 0 | 0 | 0 | — |
| P0341 | — | — | — | $101,711 | 544 | 0 | 0 | 0 | — |
| P0187 | — | — | — | $77,064 | 432 | 0 | 0 | 0 | — |
| PD35413BN | — | — | — | $62,402 | 435 | 0 | 0 | 0 | — |
| C0238 | — | — | — | $56,865 | 248 | 0 | 0 | 0 | — |
| C0222 | — | — | — | $46,163 | 231 | 0 | 0 | 0 | — |
| W0378 | — | — | — | $43,910 | 411 | 0 | 0 | 0 | — |
| C0164 | — | — | — | $40,481 | 535 | 0 | 0 | 0 | — |
| P0343 | — | — | — | $32,030 | 176 | 0 | 0 | 0 | — |
| P0344 | — | — | — | $31,940 | 109 | 0 | 0 | 0 | — |
| CF35417RBZ/B | CAT3 | COL19 | Monrovia 17-in Semi Flush Ceiling Light or Pendant (Dual Mount) Royal Bronze | $30,846 | 437 | 0 | 0 | 0 | 2026-6-19 |
| W0266 | — | — | — | $30,497 | 933 | 0 | 0 | 0 | — |
| P0228 | — | — | — | $30,216 | 208 | 0 | 0 | 0 | — |
| W0350 | — | — | — | $29,286 | 850 | 0 | 0 | 0 | — |
| LK33012WP-C | — | — | — | $28,304 | 449 | 0 | 0 | 0 | — |
| P0238 | — | — | — | $24,165 | 189 | 0 | 0 | 0 | — |
| W0351 | — | — | — | $23,014 | 239 | 0 | 0 | 0 | — |
| C0162 | — | — | — | $22,441 | 194 | 0 | 0 | 0 | — |
| H0268 | — | — | — | $21,850 | 85 | 0 | 0 | 0 | — |
| T0652 | OW | CHIA | Chiasso 2 Light 20-in.H Outdoor Wall Light Textured Black | $20,340 | 885 | 0 | 0 | 0 | 2026-8-5 |

### Q-38a_results.md

# Q-38a Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-39_category_results.md

# Q-39-cat Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 23
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| OW | $2.6M | 109,595 | 167 | $15,716 |
| CL | $2.6M | 17,611 | 46 | $56,202 |
| BL | $2.5M | 47,225 | 138 | $18,280 |
| CAT3 | $2.1M | 22,267 | 63 | $32,696 |
| P | $1.0M | 12,770 | 62 | $16,591 |
| C | $968,145 | 5,882 | 44 | $22,003 |
| OMS | $935,463 | 21,872 | 53 | $17,650 |
| CAT2 | $698,017 | 30,184 | 51 | $13,687 |
| LC | $697,747 | 2,809 | 17 | $41,044 |
| CAT4 | $643,931 | 9,435 | 41 | $15,706 |
| WL | $598,740 | 19,051 | 62 | $9,657 |
| OC | $444,878 | 9,468 | 20 | $22,244 |
| CLK | $264,608 | 2,862 | 8 | $33,076 |
| OD | $161,442 | 4,698 | 13 | $12,419 |
| DL | $140,095 | 2,124 | 5 | $28,019 |
| OP | $121,565 | 2,708 | 7 | $17,366 |
| CAT7 | $91,088 | 978 | 5 | $18,218 |
| OS | $86,813 | 5,339 | 28 | $3,100 |
| MC | $75,610 | 529 | 3 | $25,203 |
| SWL | $42,109 | 831 | 1 | $42,109 |
| CAT8 | $3,587 | 938 | 4 | $897 |
| CAT11 | $3,025 | 658 | 3 | $1,008 |
| CAT5 | $2,100 | 62 | 7 | $300 |

### Q-39_collection_results.md

# Q-39-col Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| BURN | $1.2M | 9,781 | 9 | $134,388 |
| DOR | $888,189 | 30,127 | 15 | $59,213 |
| COL29 | $651,477 | 14,289 | 27 | $24,129 |
| ELS | $565,693 | 3,838 | 10 | $56,569 |
| AKR | $558,523 | 10,383 | 12 | $46,544 |
| BARN | $504,899 | 3,632 | 2 | $252,449 |
| COL12 | $457,539 | 6,348 | 13 | $35,195 |
| CHIA | $437,018 | 25,227 | 17 | $25,707 |
| BOZ | $425,377 | 6,744 | 9 | $47,264 |
| COL19 | $420,524 | 5,537 | 15 | $28,035 |
| COL14 | $412,536 | 19,992 | 17 | $24,267 |
| COL79 | $367,332 | 2,795 | 6 | $61,222 |
| COL66 | $366,946 | 1,121 | 2 | $183,473 |
| COL13 | $338,480 | 3,843 | 9 | $37,609 |
| COL15 | $335,895 | 7,837 | 13 | $25,838 |
| CUR | $329,620 | 2,128 | 2 | $164,810 |
| COL72 | $296,208 | 1,816 | 2 | $148,104 |
| BRY | $242,087 | 3,787 | 9 | $26,899 |
| VINE | $232,196 | 3,372 | 8 | $29,024 |
| EUC | $226,373 | 882 | 2 | $113,187 |
| CHAT | $216,382 | 8,532 | 9 | $24,042 |
| ORBIT | $215,741 | 2,381 | 7 | $30,820 |
| VILO | $203,278 | 9,186 | 7 | $29,040 |
| BEL | $198,540 | 3,002 | 4 | $49,635 |
| COL35 | $197,935 | 2,120 | 6 | $32,989 |

### Q-42_results.md

# Q-42 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 48
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| BELO | 1 | $0 | 0 | $0 |
| BOZ | 1 | $0 | 0 | $0 |
| BUR | 1 | $0 | 0 | $0 |
| CARY | 1 | $0 | 0 | $0 |
| CHIA | 3 | $0 | 0 | $0 |
| COL106 | 2 | $0 | 0 | $0 |
| COL108 | 1 | $0 | 0 | $0 |
| COL111 | 3 | $0 | 0 | $0 |
| COL121 | 2 | $0 | 0 | $0 |
| COL13 | 1 | $0 | 0 | $0 |
| COL137 | 13 | $0 | 0 | $0 |
| COL14 | 2 | $0 | 0 | $0 |
| COL142 | 1 | $0 | 0 | $0 |
| COL148 | 3 | $0 | 0 | $0 |
| COL153 | 2 | $0 | 0 | $0 |
| COL154 | 4 | $0 | 0 | $0 |
| COL157 | 2 | $0 | 0 | $0 |
| COL159 | 2 | $0 | 0 | $0 |
| COL160 | 2 | $0 | 0 | $0 |
| COL165 | 1 | $0 | 0 | $0 |
| COL173 | 1 | $0 | 0 | $0 |
| COL182 | 1 | $0 | 0 | $0 |
| COL19 | 2 | $0 | 0 | $0 |
| COL203 | 1 | $0 | 0 | $0 |
| COL213 | 1 | $0 | 0 | $0 |
| COL214 | 3 | $0 | 0 | $0 |
| COL218 | 5 | $0 | 0 | $0 |
| COL221 | 2 | $0 | 0 | $0 |
| COL223 | 5 | $0 | 0 | $0 |
| COL225 | 2 | $0 | 0 | $0 |
| COL240 | 5 | $0 | 0 | $0 |
| COL281 | 1 | $0 | 0 | $0 |
| COL282 | 1 | $0 | 0 | $0 |
| COL283 | 1 | $0 | 0 | $0 |
| COL285 | 1 | $0 | 0 | $0 |
| COL286 | 1 | $0 | 0 | $0 |
| COL287 | 3 | $0 | 0 | $0 |
| COL30 | 2 | $0 | 0 | $0 |
| COL56 | 2 | $0 | 0 | $0 |
| COL96 | 1 | $0 | 0 | $0 |
| DAY | 1 | $0 | 0 | $0 |
| DRAKE | 1 | $0 | 0 | $0 |
| EST | 13 | $0 | 0 | $0 |
| GRANT | 1 | $0 | 0 | $0 |
| KENT | 2 | $0 | 0 | $0 |
| NILES | 2 | $0 | 0 | $0 |
| RAD | 4 | $0 | 0 | $0 |
| SMITH | 2 | $0 | 0 | $0 |

### Q-59_results.md

# Q-59 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORG_SUMMARY | — | — | — | 100 | 0 | — | — | — | — | — | — |

### Q-61_results.md

# Q-61 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0449 | Lincoln 12.75-in. W 1 Light Pendant Matte Black | P | 16 | 144 | 15,414.79 | 78 | — |
| P0448 | Lincoln 12.75-in. W 1 Light Pendant Muted Brass | P | 18 | 134 | 15,287.38 | 81 | — |
| P0453 | Eastgate 12-in. W 1 Light Pendant Matte Black | P | 12 | 123 | 7,001.76 | 56 | — |
| C0350 | Eastgate 12-in. W Semi-Flush Mount Ceiling Light Matte Black | CAT3 | 13 | 158 | 6,712.54 | 96 | — |
| C0349 | Eastgate 12-in. W Semi-Flush Mount Ceiling Light Antique Gold | CAT3 | 16 | 135 | 6,267.40 | 86 | — |
| F0135 | Niles 60-in. LED Ceiling Fan Satin Brass | CL | 6 | 29 | 5,490.31 | 21 | — |
| P0452 | Eastgate 12-in. W 1 Light Pendant Antique Gold | P | 13 | 92 | 4,997.91 | 46 | — |
| F0133 | Wedgewood 60-in. LED Ceiling Fan Satin Brass with Dark Elm Blades | CL | 6 | 19 | 4,461.42 | 14 | — |
| C0342 | Northgate LED 13-in. W Flush Mount Matte Black and Satin Gold | CAT4 | 10 | 74 | 3,782.88 | 23 | — |
| T0820 | Smith 8.5-in. W Outdoor Motion Sensor Wall Light Textured Black | OMS | 7 | 69 | 3,564.20 | 23 | — |
| C0348 | Armitage 32-in. W 5 Light Semi-Flush Muted Brass | CAT3 | 9 | 17 | 3,544.89 | 14 | — |
| F0137 | Maplewood 52-in. LED Ceiling Fan Matte White | CL | 6 | 25 | 3,287.61 | 14 | — |
| H0319 | Monrovia 26-in. W 5 Light Chandelier Oil Rubbed Bronze | C | 4 | 17 | 2,990 | 17 | — |
| C0346 | Shelby 9.25-in. W 1 Light Semi-Flush Mount Matte Black | CAT3 | 8 | 59 | 2,906.30 | 34 | — |
| F0141 | Niles 60-in. LED Ceiling Fan Black | CL | 2 | 15 | 2,829.12 | 11 | — |
| P0446 | Kent 11.75-in. W 1 Light Pendant Muted Brass | P | 8 | 22 | 2,757.65 | 11 | — |
| W0558 | Eastgate 15-in. W 2 Light Vanity Antique Gold | BL | 8 | 50 | 2,671.71 | 39 | — |
| P0450 | Milano 4.75-in W 1 Light Mini Pendant Alabaster Glass Satin Nickel | CAT2 | 9 | 54 | 2,657.97 | 27 | — |
| C0345 | Beloit 12-in. W 1 Light Semi-Flush Mount Matte Black | CAT3 | 9 | 37 | 2,593.98 | 29 | — |
| F0147 | Wedgewood 60-in. LED Ceiling Fan Satin Brass with Light Oak Blades | CL | 5 | 11 | 2,548.89 | 10 | — |
| W0560 | Eastgate 23-in. W 3 Light Vanity Antique Gold | BL | 8 | 31 | 2,455.54 | 24 | — |
| P0341R | Estelle 26.75 in. 6 Light Orb Pendant Natural Brass and Matte Black | P | 3 | 9 | 2,336.88 | 4 | — |
| P0451 | Milano 4.75-in W 1 Light Mini Pendant Alabaster Glass Muted Brass | CAT2 | 6 | 35 | 2,198.65 | 18 | — |
| T0818 | Cottage Grove 10.5-in. W 3 Light Outdoor Wall Light Matte Black | OW | 3 | 16 | 2,117.66 | 6 | — |
| F0146 | Cary 56-in. LED Ceiling Fan Matte Black and Satin Brass | CL | 3 | 14 | 1,983.68 | 9 | — |
| P0426R | Avalon 27.25-in. 6 Light LED Pendant Muted Brass | P | 4 | 17 | 1,895.40 | 9 | — |
| F0140 | Ruston 60-in. LED Ceiling Fan Matte Black | CL | 5 | 13 | 1,876.29 | 9 | — |
| W0561 | Eastgate 23-in. W 3 Light Vanity Matte Black | BL | 6 | 21 | 1,398.57 | 18 | — |
| F0134 | Wedgewood 60-in. LED Ceiling Fan Satin Nickel with Natural Walnut Blades | CL | 3 | 6 | 1,272.40 | 4 | — |
| W0559 | Eastgate 15-in. W 2 Light Vanity Matte Black | BL | 7 | 26 | 1,190.26 | 19 | — |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| C0345 | Beloit 12-in. W 1 Light Semi-Flush Mount Matte Black | BELO | 0 | 0 | [{'customer_code': 'C00490', 'customer_name': 'Lowes.com US', 'collection_revenue': 36693.27}, {'customer_code': 'C01026', 'customer_name': 'Wayfair LLC', 'collection_revenue': 14929.27}, {'customer_code': 'C00977', 'customer_name': 'Build.com', 'collection_revenue': 14518.4}] |
| PD55724BBZ | Bozeman 24-in Pendant Burnished Bronze | BOZ | 0 | 0 | [{'customer_code': 'C01378', 'customer_name': 'Black Forest Decor', 'collection_revenue': 107470.38}, {'customer_code': 'C00490', 'customer_name': 'Lowes.com US', 'collection_revenue': 43596.44}, {'customer_code': 'C01914', 'customer_name': 'Bed Bath & Beyond', 'collection_revenue': 34925.21}, {'customer_code': 'C01387', 'customer_name': 'Haus Appeal, LLC', 'collection_revenue': 31711.2}, {'customer_code': 'C01129', 'customer_name': 'Rugs & Lighting Imports', 'collection_revenue': 26013.72}, {'customer_code': 'C01469', 'customer_name': 'Designer Lighting & Fan', 'collection_revenue': 25364.48}, {'customer_code': 'C00977', 'customer_name': 'Build.com', 'collection_revenue': 20002.48}, {'customer_code': 'C01031', 'customer_name': 'Cast Antlers', 'collection_revenue': 13308.87}, {'customer_code': 'C00256', 'customer_name': 'Cape Electrical Supply', 'collection_revenue': 10915.94}] |
| P0365R | Burien 18-in. 4 Light Pendant Black and Washed Ash | BUR | 0 | 0 | — |
| F0146 | Cary 56-in. LED Ceiling Fan Matte Black and Satin Brass | CARY | 0 | 0 | — |
| T0798 | Chiasso 13.25-in. H Outdoor 2-Light Wall Light Dusk to Dawn  with GFCI Outlet Textured Black | CHIA | 0 | 0 | [{'customer_code': 'C01026', 'customer_name': 'Wayfair LLC', 'collection_revenue': 297819.68}, {'customer_code': 'C00977', 'customer_name': 'Build.com', 'collection_revenue': 31985.78}, {'customer_code': 'C00490', 'customer_name': 'Lowes.com US', 'collection_revenue': 22080.9}, {'customer_code': 'C01387', 'customer_name': 'Haus Appeal, LLC', 'collection_revenue': 15747.83}, {'customer_code': 'C00447', 'customer_name': 'Bellacor', 'collection_revenue': 10000.19}] |
| T0821 | Chiasso 11.25-in.H LED Outdoor Wall Light Matte Black | CHIA | 0 | 0 | [{'customer_code': 'C01026', 'customer_name': 'Wayfair LLC', 'collection_revenue': 297819.68}, {'customer_code': 'C00977', 'customer_name': 'Build.com', 'collection_revenue': 31985.78}, {'customer_code': 'C00490', 'customer_name': 'Lowes.com US', 'collection_revenue': 22080.9}, {'customer_code': 'C01387', 'customer_name': 'Haus Appeal, LLC', 'collection_revenue': 15747.83}, {'customer_code': 'C00447', 'customer_name': 'Bellacor', 'collection_revenue': 10000.19}] |
| T0822 | Chiasso 11.25-in.H LED Outdoor Wall Light Deep Bronze | CHIA | 0 | 0 | [{'customer_code': 'C01026', 'customer_name': 'Wayfair LLC', 'collection_revenue': 297819.68}, {'customer_code': 'C00977', 'customer_name': 'Build.com', 'collection_revenue': 31985.78}, {'customer_code': 'C00490', 'customer_name': 'Lowes.com US', 'collection_revenue': 22080.9}, {'customer_code': 'C01387', 'customer_name': 'Haus Appeal, LLC', 'collection_revenue': 15747.83}, {'customer_code': 'C00447', 'customer_name': 'Bellacor', 'collection_revenue': 10000.19}] |
| W0562 | Bosworth 22-in. W 3 Light Vanity Muted Brass | COL106 | 0 | 0 | — |
| W0563 | Bosworth 22-in. W 3 Light Vanity Matte Black | COL106 | 0 | 0 | — |
| H0266R | Glencoe 28-in. 6 Light Chandelier Matte Black | COL108 | 0 | 0 | — |
| W0401R | Galena 1 Light Vanity Matte Black and Satin Nickel | COL111 | 0 | 0 | — |
| W0402R | Galena 2 Light Vanity Matte Black and Satin Nickel | COL111 | 0 | 0 | — |
| W0403R | Galena 3 Light Vanity Matte Black and Satin Nickel | COL111 | 0 | 0 | — |
| F0136 | Maplewood 52-in. LED Ceiling Fan Matte Black | COL121 | 0 | 0 | — |
| F0137 | Maplewood 52-in. LED Ceiling Fan Matte White | COL121 | 0 | 0 | — |
| PD55624BBZ | Yellowstone 24-in Moose Pendant Burnished Bronze | COL13 | 0 | 0 | [{'customer_code': 'C01378', 'customer_name': 'Black Forest Decor', 'collection_revenue': 77398.05}, {'customer_code': 'C01914', 'customer_name': 'Bed Bath & Beyond', 'collection_revenue': 28794.7}, {'customer_code': 'C00490', 'customer_name': 'Lowes.com US', 'collection_revenue': 27685.02}, {'customer_code': 'C01469', 'customer_name': 'Designer Lighting & Fan', 'collection_revenue': 22900.53}, {'customer_code': 'C00977', 'customer_name': 'Build.com', 'collection_revenue': 16402.91}, {'customer_code': 'C01387', 'customer_name': 'Haus Appeal, LLC', 'collection_revenue': 13392.49}, {'customer_code': 'C01026', 'customer_name': 'Wayfair LLC', 'collection_revenue': 12237.23}] |
| C0349 | Eastgate 12-in. W Semi-Flush Mount Ceiling Light Antique Gold | COL137 | 0 | 0 | — |
| C0350 | Eastgate 12-in. W Semi-Flush Mount Ceiling Light Matte Black | COL137 | 0 | 0 | — |
| C0351 | Eastgate 8.75-in. W Semi-Flush Ceiling Light Satin Nickel | COL137 | 0 | 0 | — |
| C0352 | Eastgate 12-in. W Semi-Flush Ceiling Light Satin Nickel | COL137 | 0 | 0 | — |
| P0452 | Eastgate 12-in. W 1 Light Pendant Antique Gold | COL137 | 0 | 0 | — |
| P0453 | Eastgate 12-in. W 1 Light Pendant Matte Black | COL137 | 0 | 0 | — |
| P0459 | Eastgate 12-in. W 1 Light Pendant Satin Nickel | COL137 | 0 | 0 | — |
| W0558 | Eastgate 15-in. W 2 Light Vanity Antique Gold | COL137 | 0 | 0 | — |
| W0559 | Eastgate 15-in. W 2 Light Vanity Matte Black | COL137 | 0 | 0 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
