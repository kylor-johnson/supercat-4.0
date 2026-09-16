# Section 3 Context Bundle — Savoy House Lighting (shl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=209029, portal_order_gmv=$50.0M |
| HAS_INVENTORY | True | inventory_count=3139 |
| HAS_SALES_DATA | True | sales_data_count=140638 |
| HAS_SALES_SECTION | True | mode=orders order_reps=18 engagement_reps=0 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | shl_ecat_online |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$50.0M > ecat_gmv=$3.4M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 18 | 18 |
| ENGAGEMENT_REP_COUNT | 0 |  |
| SALES_SECTION_MODE | orders | orders |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 84 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 653, Mixpanel total submit_order (Q-01): 543 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=89.3%, ambiguous_rate=6.7%, showroom_event_share=0.6% |
| USER_GROUP_JOIN_RATE | 89% | 75 of 84 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 1% | showroom+admin share of matched events: 0.6% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Jessica Romero |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1139 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=827 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Savoy House Lighting
- **Shortname**: shl
- **Org ID**: 41
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | False |
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
| §3 Customer | STRONG | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | STRONG | See Derived Gate 6 §5 formula |

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

# Signal Rank — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Total signals fired**: 59 (P0: 45, P1: 13, P2: 1)
- **Org GMV**: $3.4M eCat LTM, $50.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders | P1 | §2 Accounts | 8.3 | $8,268,334 | 2.0 | 136,730,694 | POSITIVE |
| 2 | SIG-ANOMALY-02 | Stock Out — 9-302-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $507,979 LTM, 0 available | P0 | §3 Product | 10.0 | $507,979 | 3.0 | 15,239,379 | RISK |
| 3 | SIG-MOM-01 | Account Acceleration — Shades Of Light 2 consecutive QoQ acceleration quarters, $867,672 peak quarter (+119% QoQ) | P0 | §2 Accounts | 4.0 | $867,672 | 3.0 | 10,333,979 | POSITIVE |
| 4 | SIG-ANOMALY-02 | Stock Out — 1-2221-6-322 (Salerno 6-Light Chandelier in Warm Brass) $303,275 LTM, 0 available | P0 | §3 Product | 10.0 | $303,275 | 3.0 | 9,098,262 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 7-1804-4-322 (Crawford 4-Light Pendant in Warm Brass) $286,652 LTM, 0 available | P0 | §3 Product | 10.0 | $286,652 | 3.0 | 8,599,568 | RISK |
| 6 | SIG-DECAY-04 | Spending Contraction — Shades Of Light -40.8% YoY ($2,915,999→$1,725,093), $1,190,906 gap | P0 | §2 Accounts | 2.0 | $1,190,906 | 3.0 | 7,288,344 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 7-1774-6-320 (Ashburn 6-Light Pendant in Warm Brass an) $233,394 LTM, 0 available | P0 | §3 Product | 10.0 | $233,394 | 3.0 | 7,001,821 | RISK |
| 8 | SIG-COMMERCE-01 | Capture Rate — eCat captures 6.8% of $50M total business; each +1pt = $500K | P0 | §4 Commerce | 4.7 | $500,000 | 3.0 | 6,990,000 | POSITIVE |
| 9 | SIG-DECAY-04 | Spending Contraction — Lighting Connection Lp -64.0% YoY ($926,397→$333,632), $592,765 gap | P0 | §2 Accounts | 3.2 | $592,765 | 3.0 | 5,690,545 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 1-312-15-322 (Middleton 15-Light Chandelier in Warm Br) $188,670 LTM, 0 available | P0 | §3 Product | 10.0 | $188,670 | 3.0 | 5,660,094 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 9-303-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $186,435 LTM, 0 available | P0 | §3 Product | 10.0 | $186,435 | 3.0 | 5,593,063 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — M60008NB (2-Light Ceiling Light in Natural Brass) $163,303 LTM, 0 available | P0 | §3 Product | 10.0 | $163,303 | 3.0 | 4,899,087 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 9-7144-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $162,681 LTM, 0 available | P0 | §3 Product | 10.0 | $162,681 | 3.0 | 4,880,422 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 7-2918-1-156 (Alta 1-Light Pendant in Concrete and Bra) $147,450 LTM, 0 available | P0 | §3 Product | 10.0 | $147,450 | 3.0 | 4,423,505 | RISK |
| 15 | SIG-ANOMALY-03 | Competitive Displacement — Sunbelt /Mississippi total biz +39% but eCat -83% | P0 | §2 Accounts | 8.1 | $97,748 | 3.0 | 2,387,015 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — Capital Electric 2 consecutive QoQ acceleration quarters, $43,171 peak quarter (+378% QoQ) | P0 | §2 Accounts | 12.6 | $43,171 | 3.0 | 1,631,423 | POSITIVE |
| 17 | SIG-DECAY-01 | Reorder Decay — Dement Lighting 7.8x normal gap (321d vs 41d avg) | P0 | §2 Accounts | 7.8 | $58,302 | 3.0 | 1,364,267 | RISK |
| 18 | SIG-MOM-01 | Account Acceleration — BELAMI 2 consecutive QoQ acceleration quarters, $271,678 peak quarter (+48% QoQ) | P0 | §2 Accounts | 1.6 | $271,678 | 3.0 | 1,312,206 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — St Louis Metro Electric 2 consecutive QoQ acceleration quarters, $69,827 peak quarter (+175% QoQ) | P0 | §2 Accounts | 5.8 | $69,827 | 3.0 | 1,221,975 | POSITIVE |
| 20 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 48% of eCat GMV | P1 | §4 Commerce | 1.2 | $410,802 | 2.0 | 995,505 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 35 | 1 | 0 | 36 | |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 0 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Shades Of Light 2 consecutive QoQ acceleration quarters, $867,672 peak quarter (+119% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 6.8% of $50M total business; each +1pt = $500K
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Capital Electric 2 consecutive QoQ acceleration quarters, $43,171 peak quarter (+378% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 9-302-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $507,979 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 1-2221-6-322 (Salerno 6-Light Chandelier in Warm Brass) $303,275 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 7-1804-4-322 (Crawford 4-Light Pendant in Warm Brass) $286,652 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 4,984 | 56 | 5 | 98.90 |

### Q-37_results.md

# Q-37 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9-302-1-322 | SCONC | MONRO | Monroe 1-Light Wall Sconce in Warm Brass | $514,623 | 11,980 | 0 | 0 | 0 | 2026-07-03 |
| 1-2221-6-322 | CHAND | SALER | Salerno 6-Light Chandelier in Warm Brass | $305,959 | 1,664 | 0 | 0 | 0 | 2026-06-27 |
| 7-1804-4-322 | PENDA | CRAWF | Crawford 4-Light Pendant in Warm Brass | $287,877 | 1,367 | 0 | 0 | 0 | 2026-07-11 |
| 7-1774-6-320 | PENDA | ASHBU | Ashburn 6-Light Pendant in Warm Brass and Rope | $234,942 | 559 | 0 | 0 | 0 | 2026-07-16 |
| 1-312-15-322 | CHAND | MIDDL | Middleton 15-Light Chandelier in Warm Brass | $189,678 | 218 | 0 | 0 | 0 | 2026-07-03 |
| 9-303-1-322 | SCONC | MONRO | Monroe 1-Light Wall Sconce in Warm Brass | $188,185 | 3,131 | 0 | 0 | 0 | 2026-07-03 |
| 1-1852-10-89 | DISCO | DISCO | Hudson 10-Light Oval Chandelier in Matte Black | $170,084 | 226 | 0 | 0 | 0 | — |
| M60008NB | SEMI | MSEMI | 2-Light Ceiling Light in Natural Brass | $165,810 | 3,051 | 0 | 0 | 0 | 2026-07-03 |
| 8-4030-3-11 | BATH | OCTAV | Octave 3-Light Bathroom Vanity Light in Polished Chrome | $165,184 | 2,241 | 0 | 0 | 0 | 2026-06-27 |
| 9-7144-1-322 | SCONC | MONRO | Monroe 1-Light Wall Sconce in Warm Brass | $162,822 | 2,785 | 0 | 0 | 0 | 2026-06-27 |
| 7-2918-1-156 | PENDA | ALTA | Alta 1-Light Pendant in Concrete and Brass | $154,818 | 514 | 0 | 0 | 0 | 2026-06-27 |
| 6-133-16-322 | FLUSH | WATKI | Watkins 3-Light Ceiling Light in Warm Brass | $150,402 | 1,733 | 0 | 0 | 0 | 2026-07-03 |
| 9-302-1-109 | SCONC | MONRO | Monroe 1-Light Wall Sconce in Polished Nickel | $132,728 | 1,987 | 0 | 0 | 0 | 2026-08-04 |
| 8-2988-3-322 | BATH | BLAIR | Blair 3-Light Bathroom Vanity Light in Warm Brass | $131,399 | 1,803 | 0 | 0 | 0 | 2026-07-24 |
| 1-1846-4-127 | CHAND | LIVOR | Livorno 4-Light Chandelier in Noble Brass | $128,788 | 405 | 0 | 0 | 0 | 2026-07-10 |
| 7-1850-8-89 | DISCO | DISCO | Hudson 8-Light Pendant in Matte Black | $126,001 | 215 | 0 | 0 | 0 | — |
| 7-1851-12-89 | DISCO | DISCO | Hudson 12-Light Pendant in Matte Black | $122,510 | 184 | 0 | 0 | 0 | — |
| 8-4030-4-322 | BATH | OCTAV | Octave 4-Light Bathroom Vanity Light in Warm Brass | $117,702 | 1,383 | 0 | 0 | 0 | 2026-06-27 |
| 28-FD-690-322 | DISCO | DISCO | Gideon 4-Light LED Fan D'Lier in Warm Brass | $115,154 | 146 | 0 | 0 | 0 | — |
| 26-FD-7806-143 | FANDL | SHEFF | Sheffield 6-Light LED Fan D'Lier in Matte Black with Warm Brass Accents | $112,402 | 300 | 0 | 0 | 0 | — |

### Q-38a_results.md

# Q-38a Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-39_category_results.md

# Q-39-cat Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 33
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| PENDA | $18.4M | 123,619 | 487 | $37,688 |
| CHAND | $15.6M | 62,366 | 414 | $37,681 |
| BATH | $14.0M | 178,097 | 537 | $26,074 |
| SCONC | $9.0M | 151,863 | 462 | $19,522 |
| SEMI | $6.1M | 72,497 | 159 | $38,312 |
| LINEA | $5.0M | 13,975 | 89 | $55,935 |
| FANDL | $4.1M | 11,075 | 52 | $79,272 |
| DISCO | $4.0M | 29,717 | 627 | $6,333 |
| LACEI | $3.6M | 642,228 | 28 | $129,349 |
| OUTWA | $3.0M | 40,106 | 141 | $21,297 |
| FLUSH | $2.5M | 50,760 | 64 | $39,423 |
| LAUND | $1.6M | 61,104 | 23 | $67,686 |
| FAN | $1.5M | 10,500 | 43 | $33,977 |
| LAEXT | $1.0M | 52,407 | 22 | $46,227 |
| MIRRO | $597,936 | 2,550 | 21 | $28,473 |
| MINIP | $452,323 | 7,069 | 28 | $16,154 |
| OUTCH | $319,336 | 1,146 | 5 | $63,867 |
| CONVE | $297,014 | 1,904 | 25 | $11,881 |
| OUTPE | $276,128 | 1,721 | 27 | $10,227 |
| LAMPS | $212,916 | 1,453 | 33 | $6,452 |
| RECHA | $200,272 | 2,742 | 10 | $20,027 |
| OUTCE | $157,963 | 2,970 | 6 | $26,327 |
| OUTPO | $145,735 | 922 | 24 | $6,072 |
| DOWNR | $91,697 | 5,048 | 141 | $650 |
| MINIC | $62,425 | 212 | 1 | $62,425 |
| EXTEN | $53,486 | 5,696 | 49 | $1,092 |
| BULBS | $43,043 | 29,456 | 8 | $5,380 |
| GLASS | $37,699 | 8,905 | 4 | $9,425 |
| CONTR | $35,730 | 1,527 | 13 | $2,748 |
| PARTS | $31,756 | 3,965 | 63 | $504 |
| LABAT | $23,585 | 484 | 25 | $943 |
| LIGHT | $19,298 | 384 | 7 | $2,757 |
| SLOPE | $3,452 | 231 | 13 | $266 |

### Q-39_collection_results.md

# Q-39-col Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| MCHAN | $4.1M | 34,264 | 131 | $31,551 |
| DISCO | $4.0M | 29,717 | 627 | $6,333 |
| MPEND | $3.7M | 40,534 | 135 | $27,529 |
| MBATH | $3.4M | 51,502 | 121 | $27,699 |
| OCTAV | $3.1M | 42,480 | 64 | $48,076 |
| LADIS | $3.0M | 525,573 | 22 | $137,050 |
| CALHO | $2.8M | 36,375 | 27 | $102,846 |
| MSEMI | $2.6M | 43,974 | 81 | $32,076 |
| MSCON | $2.4M | 49,879 | 162 | $14,960 |
| TOWNS | $2.0M | 10,032 | 24 | $82,969 |
| ORLEA | $2.0M | 1,876 | 6 | $327,071 |
| MCEIL | $1.5M | 11,730 | 49 | $30,698 |
| MONRO | $1.4M | 26,628 | 15 | $95,888 |
| MFLUS | $1.3M | 32,592 | 23 | $58,590 |
| LAUN5 | $1.2M | 41,179 | 9 | $133,770 |
| BOA | $1.2M | 2,022 | 5 | $238,791 |
| MIDDL | $906,897 | 1,909 | 10 | $90,690 |
| SANTIA | $888,845 | 1,404 | 4 | $222,211 |
| LAFLO | $864,177 | 45,984 | 9 | $96,020 |
| GENRY | $858,903 | 4,113 | 21 | $40,900 |
| ALDEN | $772,834 | 7,388 | 8 | $96,604 |
| STOC1 | $761,894 | 2,096 | 2 | $380,947 |
| SALER | $729,844 | 4,324 | 4 | $182,461 |
| ASHE | $696,590 | 5,060 | 4 | $174,148 |
| CAMER | $684,807 | 12,047 | 9 | $76,090 |

### Q-42_results.md

# Q-42 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 199
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| MATIS | 344 | $280,197 | 598 | $815 |
| DARIE | 971 | $268,098 | 1,929 | $276 |
| ORLEA | 148 | $221,084 | 235 | $1,494 |
| MRXBE | 334 | $199,234 | 1,091 | $597 |
| ALTA | 196 | $183,395 | 665 | $936 |
| BLAIR | 819 | $166,717 | 1,937 | $204 |
| MAYNA | 310 | $130,025 | 947 | $419 |
| LAFL3 | 244 | $127,350 | 5,532 | $522 |
| HOLTO | 675 | $119,947 | 1,815 | $178 |
| EDGEM | 437 | $118,409 | 1,302 | $271 |
| MARBE | 73 | $109,765 | 117 | $1,504 |
| MRXON | 244 | $108,178 | 607 | $443 |
| MRXPA | 314 | $101,790 | 715 | $324 |
| RIVAG | 171 | $96,112 | 579 | $562 |
| ORIAN | 189 | $87,333 | 315 | $462 |
| AQUIT | 96 | $85,968 | 166 | $896 |
| SHERR | 212 | $85,086 | 751 | $401 |
| ONCE | 73 | $81,147 | 99 | $1,112 |
| THAYE | 213 | $76,555 | 596 | $359 |
| RYDER | 397 | $74,116 | 2,212 | $187 |
| ANTOL | 117 | $73,669 | 158 | $630 |
| REILI | 136 | $69,900 | 277 | $514 |
| MRXCO | 178 | $64,705 | 357 | $364 |
| MANSE | 218 | $59,075 | 284 | $271 |
| OCTAV | 364 | $58,897 | 630 | $162 |
| ELSIE | 273 | $58,846 | 406 | $216 |
| WILLO | 168 | $53,980 | 370 | $321 |
| CHAUN | 205 | $49,524 | 512 | $242 |
| MOLLY | 209 | $47,485 | 850 | $227 |
| CHAML | 137 | $46,929 | 249 | $343 |
| BALFO | 203 | $46,607 | 316 | $230 |
| LANCA | 206 | $46,212 | 355 | $224 |
| EMERY | 206 | $45,661 | 532 | $222 |
| IRINA | 60 | $44,675 | 97 | $745 |
| LABUL | 55 | $42,481 | 29,549 | $772 |
| SANCT | 111 | $42,395 | 178 | $382 |
| LOMBA | 130 | $41,966 | 223 | $323 |
| SILAS | 124 | $41,923 | 611 | $338 |
| PALMA | 52 | $39,719 | 126 | $764 |
| BARRO | 357 | $39,106 | 766 | $110 |
| LINCO | 86 | $38,211 | 146 | $444 |
| MELIA | 54 | $36,440 | 71 | $675 |
| ASHLA | 172 | $36,227 | 298 | $211 |
| PASTI | 85 | $35,651 | 163 | $419 |
| CORA | 100 | $34,946 | 577 | $349 |
| CATAL | 51 | $34,487 | 104 | $676 |
| DOVER | 212 | $32,214 | 459 | $152 |
| MELSA | 132 | $31,753 | 301 | $241 |
| ARAGO | 79 | $30,526 | 105 | $386 |
| MAE | 84 | $30,402 | 622 | $362 |
| HILLB | 173 | $28,779 | 264 | $166 |
| LOTO | 42 | $27,755 | 53 | $661 |
| MONTR | 95 | $26,857 | 185 | $283 |
| TARTI | 74 | $26,421 | 257 | $357 |
| CONRA | 102 | $26,131 | 171 | $256 |
| ALLST | 75 | $24,673 | 112 | $329 |
| CABOT | 68 | $24,250 | 134 | $357 |
| GROTT | 140 | $24,217 | 300 | $173 |
| ASHBY | 56 | $23,585 | 128 | $421 |
| SILEN | 81 | $23,283 | 122 | $287 |
| PROTE | 37 | $23,051 | 94 | $623 |
| LEANN | 52 | $23,002 | 54 | $442 |
| HARDI | 67 | $22,427 | 119 | $335 |
| BARTL | 82 | $21,555 | 163 | $263 |
| DISCO | 81 | $21,486 | 112 | $265 |
| PIERC | 156 | $21,258 | 316 | $136 |
| MARIQ | 92 | $20,790 | 181 | $226 |
| EMMA | 36 | $19,525 | 238 | $542 |
| BAILE | 56 | $18,935 | 76 | $338 |
| BALTH | 56 | $18,895 | 216 | $337 |
| JUDI | 36 | $18,884 | 40 | $525 |
| HADLE | 66 | $18,215 | 141 | $276 |
| ABBOT | 40 | $18,054 | 72 | $451 |
| JENNI | 82 | $17,949 | 119 | $219 |
| HARPE | 93 | $16,807 | 150 | $181 |
| HERRO | 116 | $16,732 | 175 | $144 |
| LAKEL | 75 | $16,415 | 366 | $219 |
| PARSO | 41 | $16,191 | 157 | $395 |
| BRUMF | 70 | $16,096 | 145 | $230 |
| NOAH | 59 | $15,989 | 110 | $271 |
| REDFI | 244 | $15,942 | 550 | $65 |
| FARRE | 57 | $15,921 | 71 | $279 |
| LILLY | 33 | $15,604 | 29 | $473 |
| TREMO | 65 | $15,515 | 86 | $239 |
| ABELI | 54 | $15,304 | 99 | $283 |
| PALIS | 57 | $14,904 | 98 | $261 |
| SANGE | 23 | $14,893 | 25 | $648 |
| LINEL | 55 | $14,861 | 134 | $270 |
| COVEN | 127 | $14,633 | 131 | $115 |
| HEARS | 31 | $14,584 | 42 | $470 |
| MARSE | 58 | $13,584 | 123 | $234 |
| DUFFI | 23 | $13,498 | 62 | $587 |
| JAMSE | 70 | $13,061 | 170 | $187 |
| BEALE | 121 | $11,973 | 244 | $99 |
| GARDN | 56 | $11,636 | 90 | $208 |
| KOHLM | 43 | $11,566 | 55 | $269 |
| BANCR | 82 | $11,518 | 137 | $140 |
| MINET | 46 | $10,159 | 60 | $221 |
| CRESC | 38 | $9,976 | 23 | $263 |
| MCKEY | 35 | $9,962 | 96 | $285 |
| PAYNE | 68 | $9,172 | 126 | $135 |
| AGAVE | 77 | $9,073 | 119 | $118 |
| ANDOV | 13 | $8,881 | 26 | $683 |
| BALSA | 70 | $8,683 | 138 | $124 |
| DANA | 47 | $8,363 | 75 | $178 |
| CONSU | 159 | $8,272 | 281 | $52 |
| DAKOA | 33 | $7,898 | 74 | $239 |
| LIVIN | 37 | $7,648 | 51 | $207 |
| MERCE | 56 | $7,533 | 91 | $135 |
| DUNHA | 36 | $7,436 | 65 | $207 |
| LEEDS | 33 | $6,552 | 46 | $199 |
| BRENT | 75 | $6,527 | 80 | $87 |
| PELHA | 25 | $6,249 | 12 | $250 |
| BELLE | 32 | $6,162 | 44 | $193 |
| JEANE | 22 | $5,878 | 12 | $267 |
| WEHUN | 56 | $5,856 | 92 | $105 |
| COLLI | 37 | $5,506 | 41 | $149 |
| MIRAM | 21 | $5,250 | 39 | $250 |
| LEHIG | 17 | $5,126 | 24 | $302 |
| JADE | 58 | $4,913 | 137 | $85 |
| HADDI | 11 | $4,862 | 24 | $442 |
| CHEST | 27 | $4,570 | 16 | $169 |
| TRTON | 20 | $4,484 | 40 | $224 |
| NORWI | 26 | $4,462 | 34 | $172 |
| KIRKW | 21 | $4,403 | 38 | $210 |
| JAMES | 22 | $4,333 | 51 | $197 |
| MELBO | 64 | $4,087 | 91 | $64 |
| AMAND | 8 | $4,002 | 31 | $500 |
| PREST | 50 | $3,845 | 74 | $77 |
| CINDY | 25 | $3,668 | 60 | $147 |
| CORAL | 21 | $3,665 | 28 | $175 |
| WESTO | 18 | $3,624 | 10 | $201 |
| ASHTO | 90 | $2,983 | 45 | $33 |
| REDDI | 25 | $2,865 | 12 | $115 |
| HEARN | 84 | $2,840 | 46 | $34 |
| ERIE | 32 | $2,684 | 45 | $84 |
| CASTE | 116 | $2,641 | 136 | $23 |
| ETERE | 3 | $2,604 | 4 | $868 |
| DOTHA | 14 | $2,365 | 19 | $169 |
| LEIDE | 10 | $2,333 | 14 | $233 |
| BEAUM | 38 | $1,854 | 58 | $49 |
| BARTO | 15 | $1,830 | 26 | $122 |
| PARKE | 29 | $1,828 | 21 | $63 |
| KELLE | 44 | $1,766 | 19 | $40 |
| MALIN | 5 | $1,630 | 3 | $326 |
| JACOB | 41 | $1,514 | 10 | $37 |
| PENNY | 12 | $1,465 | 18 | $122 |
| LANET | 7 | $1,176 | 12 | $168 |
| JEAN | 32 | $1,003 | 93 | $31 |
| ADRIA | 5 | $892 | 6 | $178 |
| KEMP | 35 | $772 | 45 | $22 |
| DENIS | 3 | $746 | 6 | $249 |
| LADIS | 9 | $683 | 58 | $76 |
| FIXTU | 41 | $653 | 54 | $16 |
| CORIN | 27 | $342 | 7 | $13 |
| SENTE | 6 | $136 | 1 | $23 |
| PIERS | 18 | $22 | 6 | $1 |
| MUNREL | 19 | $0 | 0 | $0 |
| CONST | 9 | $0 | 0 | $0 |
| JASPE | 13 | $0 | 0 | $0 |
| CELIN | 15 | $0 | 0 | $0 |
| CDUNREL | 22 | $0 | 0 | $0 |
| ESPAC | 13 | $0 | 0 | $0 |
| SOFIA | 7 | $0 | 0 | $0 |
| SOMBR | 25 | $0 | 0 | $0 |
| SUNREL | 95 | $0 | 0 | $0 |
| TIEBR | 3 | $0 | 0 | $0 |
| LASKA | 30 | $-6 | 30 | $-0 |
| LADI5 | 9 | $-46 | 126 | $-5 |
| PHARR | 20 | $-64 | 0 | $-3 |
| LINDE | 25 | $-99 | 0 | $-4 |
| AMIEN | 44 | $-316 | 0 | $-7 |
| FLORS | 19 | $-481 | 0 | $-25 |
| BRADF | 37 | $-824 | 1 | $-22 |
| DAVEN | 117 | $-987 | 40 | $-8 |
| HUTCH | 8 | $-1,420 | 19 | $-177 |
| BALDW | 404 | $-1,968 | 335 | $-5 |
| CANTE | 13 | $-1,984 | 0 | $-153 |
| SALFO | 34 | $-2,164 | 0 | $-64 |
| DERBY | 27 | $-2,200 | 39 | $-81 |
| CASTR | 44 | $-2,831 | 0 | $-64 |
| TURIN | 50 | $-3,972 | 0 | $-79 |
| ROSA | 168 | $-4,427 | 264 | $-26 |
| BUTLE | 78 | $-4,505 | 0 | $-58 |
| LACON | 191 | $-5,011 | 378 | $-26 |
| PHARO | 53 | $-6,106 | 0 | $-115 |
| JARRE | 163 | $-6,118 | 238 | $-38 |
| ARCHE | 23 | $-6,152 | 0 | $-267 |
| LUNAR | 28 | $-7,213 | 13 | $-258 |
| RORY | 27 | $-8,320 | 59 | $-308 |
| LACOL | 98 | $-8,670 | 161 | $-88 |
| LELAN | 33 | $-10,613 | 23 | $-322 |
| COLOG | 18 | $-11,394 | 0 | $-633 |
| WILKE | 152 | $-14,469 | 0 | $-95 |
| COPPE | 60 | $-15,444 | 0 | $-257 |
| SEBRI | 44 | $-18,675 | 67 | $-424 |
| HANLE | 55 | $-19,267 | 83 | $-350 |
| GAIA | 89 | $-21,872 | 0 | $-246 |
| FLORE | 146 | $-40,598 | 146 | $-278 |

### Q-59_results.md

# Q-59 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORG_SUMMARY | — | — | — | 95.80 | 36,203 | — | — | — | — | — | — |

### Q-61_results.md

# Q-61 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7-2918-1-156 | Alta 1-Light Pendant in Concrete and Brass | PENDA | 88 | 274 | 106,583.36 | 253 | 407 |
| 7-2333-6-60 | Orleans 6-Light Pendant in Distressed Gold | PENDA | 42 | 61 | 75,555.90 | 59 | 1,253 |
| 6-9311-4-322 | Maynard 4-Light Ceiling Light in Warm Brass | FLUSH | 104 | 362 | 64,717.43 | 341 | 191 |
| 7-3091-6-339 | Davenport 6-Light Pendant in Antique Patina | PENDA | 67 | 95 | 63,676.62 | 83 | 679 |
| 2-1225-30X36 | Beckett LED Rectangle Frontlit and Backlit Mirror | MIRRO | 62 | 327 | 59,339.31 | 138 | 219 |
| 40-FD-8302-322 | Gaia 4-Light Fan D'Lier in Warm Brass by Breegan Jane | FANDL | 48 | 76 | 57,843.39 | 66 | 759 |
| 2-1226-48X32 | Beckett LED Rectangle Frontlit and Backlit Mirror | MIRRO | 57 | 266 | 57,387.30 | 122 | 255 |
| 6-4187-4-322 | Edgemont 4-Light Ceiling Light in Warm Brass | FLUSH | 110 | 332 | 55,115.97 | 241 | 170 |
| 1-7935-18-322 | Matisse 18-Light Chandelier in Warm Brass | CHAND | 60 | 79 | 53,291.96 | 88 | 682 |
| 2-1224-24X32 | Beckett LED Rectangle Frontlit and Backlit Mirror | MIRRO | 63 | 306 | 50,643.10 | 149 | 185 |
| 6-7163-6-322 | Elsie 6-Light Convertible Semi-Flush or Pendant in Warm Brass by Breegan Jane | CONVE | 86 | 155 | 49,483.28 | 144 | 319 |
| 7-7162-6-322 | Elsie 6-Light Pendant in Warm Brass by Breegan Jane | PENDA | 83 | 156 | 48,017.44 | 158 | 323 |
| 1-9855-8-328 | Once 8-Light Chandelier in Spun Gold by Breegan Jane | CHAND | 34 | 39 | 45,729.48 | 46 | 1,219 |
| 26-FD-775-322 | Mansell 4-Light Fan D'Lier in Warm Brass | FANDL | 59 | 158 | 44,188.66 | 162 | 299 |
| 7-2333-6-50 | Orleans 6-Light Pendant in Black Cashmere | PENDA | 31 | 36 | 43,788.44 | 40 | 1,253 |
| 2-1228-24X36 | Beckett Led Oval Frontlit and Backlit Mirror | MIRRO | 43 | 112 | 40,450.37 | 80 | 399 |
| 6-4187-4-89 | Edgemont 4-Light Ceiling Light in Matte Black | FLUSH | 99 | 239 | 39,471.35 | 211 | 170 |
| 4-FLOOD-A2-3CCT-BK | LED 3CCT Double Flood Light in Black | LAEXT | 49 | 1,718 | 38,506.31 | 147 | 26 |
| 1-7935-18-89 | Matisse 18-Light Chandelier in Matte Black | CHAND | 46 | 57 | 38,076.06 | 61 | 682 |
| 5-806-DS-273 | Ryder 1-Light Outdoor Wall Lantern in Atlas Bronze | OUTWA | 67 | 474 | 36,862.30 | 181 | 83 |
| 1-1487-9-15 | Salford 9-Light Chandelier in Mediterranean Bronze by Dann Foley | CHAND | 34 | 45 | 36,699.83 | 41 | 829 |
| 1-4528-14-221 | Marbella 14-Light Chandelier in Gold Shimmer by Breegan Jane | CHAND | 22 | 27 | 36,303.59 | 29 | 1,481 |
| 1-7934-16-322 | Matisse 16-Light Chandelier in Warm Brass | CHAND | 44 | 57 | 33,889.79 | 58 | 609 |
| 7-3092-8-339 | Davenport 8-Light Pendant in Antique Patina | PENDA | 30 | 38 | 33,496.74 | 35 | 899 |
| 3-1018-4-322 | Darien 4-Light Pendant in Warm Brass | PENDA | 50 | 105 | 32,629.32 | 91 | 316 |
| 1-1456-9-340 | Phong 9-Light Chandelier in Blanco | DISCO | 38 | 46 | 32,377.68 | 46 | 699 |
| 6-5564-1-322 | Sherrer 1-Light Ceiling Light in Warm Brass | SEMI | 54 | 217 | 32,356.07 | 182 | 157 |
| 7-2747-4-322 | Aquitane 4-Light Pendant in Warm Brass | PENDA | 25 | 42 | 31,831.44 | 45 | 803 |
| 1-1488-10-15 | Sanger 10-Light Chandelier in Mediterranean Bronze by Dann Foley | CHAND | 23 | 35 | 31,465 | 35 | 899 |
| 30-FD-435-322 | Castra LED Fan D'Lier in Warm Brass | FANDL | 37 | 44 | 30,735.03 | 41 | 699 |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9-302-1-322 | Monroe 1-Light Wall Sconce in Warm Brass | MONRO | 507,979.29 | 12,007 | — | 2026-07-03 | [{'customer': 'WAYFAIR LLC', 'revenue': 247432.54}, {'customer': 'FERGUSON', 'revenue': 32228.05}, {'customer': 'BUILD.COM', 'revenue': 28473.72}, {'customer': 'LAMPS PLUS INC', 'revenue': 15649.13}, {'customer': 'Inline Electric Supply', 'revenue': 9731.0}, {'customer': 'The Home Depot', 'revenue': 9438.54}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 7998.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 7932.75}, {'customer': 'Lighting World', 'revenue': 5065.81}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 4941.87}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 4602.0}, {'customer': 'LIGHTING BY JARED', 'revenue': 3360.62}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 3323.84}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 3145.57}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 3114.5}, {'customer': 'Sunbelt / Louisiana', 'revenue': 3040.6}, {'customer': 'Lighting Design Company', 'revenue': 2996.0}, {'customer': 'Lifestyles Store Inc', 'revenue': 2966.59}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 2817.0}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 2709.7}, {'customer': "Richard's Lighting", 'revenue': 2252.7}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2109.0}, {'customer': 'Masterpiece Lighting (GA)', 'revenue': 2009.0}, {'customer': 'BELAMI ECommerce', 'revenue': 1955.93}, {'customer': 'Light N Leisure Inc', 'revenue': 1932.0}, {'customer': "Seth's Lighting & Assoc. Inc", 'revenue': 1758.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 1731.96}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 1695.0}, {'customer': "Joseph's Electrical Center", 'revenue': 1690.64}, {'customer': 'M & M Lighting, L.P.', 'revenue': 1642.0}, {'customer': "LOWE'S", 'revenue': 1536.7}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 1528.0}, {'customer': 'Butler Lighting of High Point', 'revenue': 1503.14}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 1500.0}, {'customer': 'The Brecher Co, Inc', 'revenue': 1454.69}, {'customer': 'Lightology', 'revenue': 1404.16}, {'customer': '!! Maison Olive Inc.', 'revenue': 1350.94}, {'customer': 'The Electrical & Plumbing Store', 'revenue': 1320.0}, {'customer': 'Cregger Co LLC', 'revenue': 1313.64}, {'customer': 'HOUZZ SHOP', 'revenue': 1261.52}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 1260.0}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 1230.0}, {'customer': 'Northside Lighting & Fan dba Premier Lighting', 'revenue': 1224.23}, {'customer': 'Pace Lighting Inc', 'revenue': 1147.95}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 1120.44}, {'customer': 'Lights Unlimited', 'revenue': 1115.24}, {'customer': 'Elektra Lights & Fans Inc', 'revenue': 1080.0}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 1074.78}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 1063.77}, {'customer': 'Stokes Electric Company', 'revenue': 1020.0}, {'customer': 'Lighting Emporium Inc', 'revenue': 994.5}, {'customer': 'Rensen House of Lights', 'revenue': 955.63}, {'customer': "Hinkley's Lighting Factory", 'revenue': 934.3}, {'customer': 'Greer Lighting Center LLC', 'revenue': 906.7}, {'customer': 'Cleveland Lighting Center', 'revenue': 900.0}, {'customer': 'The Light House Gallery (MO)', 'revenue': 886.7}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 870.0}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 860.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 840.0}, {'customer': 'Universal Lighting Corp (Ont)', 'revenue': 836.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 830.0}, {'customer': 'Denney Electric Supply (Ambler, PA)', 'revenue': 825.0}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 824.85}, {'customer': 'Wilson Lighting', 'revenue': 817.0}, {'customer': 'K B L Design Center', 'revenue': 809.8}, {'customer': 'Bayside Electric Supply Co', 'revenue': 789.0}, {'customer': 'Lamps.com, Inc', 'revenue': 777.24}, {'customer': 'Capitol Lighting Gallery', 'revenue': 767.2}, {'customer': 'Hagens Lighting', 'revenue': 765.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 720.0}, {'customer': 'Deco Luminaire Quebec', 'revenue': 709.5}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 690.0}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 684.0}, {'customer': 'Union Lighting (Montreal)', 'revenue': 663.3}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': 661.1}, {'customer': 'Wiseway Supply', 'revenue': 652.0}, {'customer': 'Mathes of Alabama Elec. Supply', 'revenue': 652.0}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 648.1}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 644.52}, {'customer': '!! Applico, LLC', 'revenue': 644.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (PARAMUS)', 'revenue': 641.25}, {'customer': "Victor's Lighting", 'revenue': 623.92}, {'customer': 'Fort Worth Lighting', 'revenue': 596.0}, {'customer': 'Dement Lighting', 'revenue': 592.35}, {'customer': 'Design Superstore / Designco', 'revenue': 585.0}, {'customer': 'St Louis Metro Electric', 'revenue': 577.63}, {'customer': 'Parrish Family Enterprises dba American Lighting and Design', 'revenue': 574.38}, {'customer': 'Net Retailers, LLC', 'revenue': 562.77}, {'customer': 'LIGHTING CONCEPTS, LLC (GA)', 'revenue': 540.0}, {'customer': 'ULTRA DESIGN CENTER, LLC', 'revenue': 530.25}, {'customer': 'Bee Ridge Lighting & Design', 'revenue': 522.09}, {'customer': 'Asburys Design', 'revenue': 518.14}, {'customer': 'Gorman Brothers Appliance', 'revenue': 510.0}, {'customer': 'Lighting by Design (Exton, PA)', 'revenue': 509.0}, {'customer': 'OSMOND DESIGNS INC.', 'revenue': 507.29}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB)', 'revenue': 503.8}, {'customer': 'King Electric Company Inc', 'revenue': 499.86}, {'customer': 'Distinctive Lighting Concepts', 'revenue': 495.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 495.0}, {'customer': 'Union Lighting & Furnishings (Toronto)', 'revenue': 495.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 450.0}, {'customer': 'Elan Studio Lighting', 'revenue': 450.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 450.0}, {'customer': 'Southern Electric & Plumbing Supply', 'revenue': 441.71}, {'customer': 'Wilson Lighting of Naples Inc', 'revenue': 432.0}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 427.5}, {'customer': 'Idlewood Electric Supply', 'revenue': 427.2}, {'customer': 'VP Supply', 'revenue': 426.0}, {'customer': "Armstrong's Supply Co Inc", 'revenue': 412.0}, {'customer': 'Anzalone Electric', 'revenue': 405.0}, {'customer': 'F.W. Webb Company', 'revenue': 401.49}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 396.0}, {'customer': 'Multi-Luminaire (Granby)', 'revenue': 396.0}, {'customer': 'Lighting Connection LLC (TX) : Lighting Connection DFW', 'revenue': 387.25}, {'customer': 'Lighting Etc dba Lighting Unlimited (FL)', 'revenue': 385.76}, {'customer': 'Echelon Interiors', 'revenue': 384.7}, {'customer': "Scottie's Interiors", 'revenue': 382.82}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 378.75}, {'customer': 'ABC Lighting', 'revenue': 375.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 363.0}, {'customer': 'Living Lighting # 28 (Ottawa)', 'revenue': 363.0}, {'customer': 'Coley Electric & Plumbing Supply (Jesup)', 'revenue': 360.0}, {'customer': 'Sweet Home Design Company', 'revenue': 360.0}, {'customer': 'Schaedler Yesco Dist', 'revenue': 360.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 360.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 360.0}, {'customer': 'Coley Electric & Plumbing (Douglas)', 'revenue': 360.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 360.0}, {'customer': 'Colonial Electric Supply Co', 'revenue': 360.0}, {'customer': 'Lumen Nation LLC', 'revenue': 355.0}, {'customer': 'Flinz Holdings LLC', 'revenue': 355.0}, {'customer': 'Elements', 'revenue': 354.57}, {'customer': "Wilkinson's House of Lighting", 'revenue': 342.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 322.0}, {'customer': 'Gross Lighting & Home : Indiana Lighting Center', 'revenue': 322.0}, {'customer': 'Homestyles', 'revenue': 322.0}, {'customer': 'Denali Lighting LLC', 'revenue': 300.0}, {'customer': 'Lights of Oconee', 'revenue': 300.0}, {'customer': "Coburn Supply Company dba Coburn's : Spring Hill Lighting db", 'revenue': 300.0}, {'customer': 'Elaine Everetts Lighting', 'revenue': 300.0}, {'customer': 'Milliken Investments dba Shallotte Electric Stores', 'revenue': 300.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 300.0}, {'customer': 'Austell Lighting', 'revenue': 300.0}, {'customer': 'Multi-Luminaire (Pointe Claire)', 'revenue': 297.0}, {'customer': 'Royaume Luminaire', 'revenue': 297.0}, {'customer': 'Concept Luminaire M.B. Inc', 'revenue': 297.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 294.0}, {'customer': '!! Starlight Lighting', 'revenue': 291.89}, {'customer': 'Uncommon Living fka Lighting Unlimited (MS)', 'revenue': 286.46}, {'customer': 'Cape Electrical Supply', 'revenue': 283.48}, {'customer': 'House of Carpets', 'revenue': 272.35}, {'customer': 'Mainland Lighting Warehouse', 'revenue': 272.05}, {'customer': 'Locke Supply', 'revenue': 270.0}, {'customer': 'Southern Lights', 'revenue': 270.0}, {'customer': 'Wage Lighting & Design', 'revenue': 270.0}, {'customer': 'Wiseway Supply : Wiseway Supply Loveland', 'revenue': 270.0}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 270.0}, {'customer': 'Light and Day', 'revenue': 270.0}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 267.75}, {'customer': 'Chateau Lighting', 'revenue': 263.23}, {'customer': 'Beautiful Things, Inc', 'revenue': 255.6}, {'customer': 'First Coast Lighting & Fans', 'revenue': 254.2}, {'customer': 'Deco Luminaire Terrebonne', 'revenue': 247.5}, {'customer': 'Richardson Lighting', 'revenue': 247.5}, {'customer': 'Coco & Dash', 'revenue': 241.54}, {'customer': 'DISCOUNT PLUMBING & ELECTRIC', 'revenue': 240.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 237.6}, {'customer': '!! Bluetree Corporation', 'revenue': 227.09}, {'customer': 'Northwest Electrical Supply', 'revenue': 225.0}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 222.75}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (BOCA RATON)', 'revenue': 219.0}, {'customer': 'Southern Pipe & Supply (LA)', 'revenue': 217.0}, {'customer': 'Statewide Lighting (NV)', 'revenue': 213.0}, {'customer': 'Bright Ideas Lighting & More (Bridgeport)', 'revenue': 211.4}, {'customer': 'Brite Electric Supply Inc', 'revenue': 205.66}, {'customer': 'Hardwood Floors & More', 'revenue': 202.82}, {'customer': 'City Lightz London', 'revenue': 198.0}, {'customer': 'Paradise Lighting', 'revenue': 198.0}, {'customer': 'Signature Lighting & Fans dba Whitfield Lighting and Furnitu', 'revenue': 198.0}, {'customer': 'McLaren Electric', 'revenue': 198.0}, {'customer': 'John Ward Ace Hardware', 'revenue': 192.58}, {'customer': 'Illuminating Expressions (Evansville)', 'revenue': 191.71}, {'customer': 'Cajun Electric & Lighting', 'revenue': 191.41}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 189.57}, {'customer': 'Lighting Connection LLC (TX) : Lighting Connection (Dropship', 'revenue': 186.62}, {'customer': 'James Ashjian Lighting', 'revenue': 180.0}, {'customer': 'Palmer Electric Co dba Showcase Lighting (FL)', 'revenue': 180.0}, {'customer': 'Gem Electric Supply', 'revenue': 180.0}, {'customer': 'LDB Holdings LLC dba CW Floors and Lighting', 'revenue': 180.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 180.0}, {'customer': "Designer's Mart", 'revenue': 180.0}, {'customer': 'United Electric Supply (NE)', 'revenue': 180.0}, {'customer': 'Bright Ideas (Rochester)', 'revenue': 180.0}, {'customer': 'Mancini Fine Lighting, Inc dba Fine Lighting and Lighting De', 'revenue': 180.0}, {'customer': 'B.E.S. Lighting Center', 'revenue': 180.0}, {'customer': 'Decorative Lighting, Inc', 'revenue': 180.0}, {'customer': 'House of Lights of Sanford Inc', 'revenue': 180.0}, {'customer': 'Ray Mart Inc dba Tri-Supply', 'revenue': 180.0}, {'customer': 'Your Lighting Source, LLC', 'revenue': 180.0}, {'customer': 'American Lighting Inc', 'revenue': 180.0}, {'customer': 'GW Keeter Lighting', 'revenue': 180.0}, {'customer': 'Hubbard Supplyhouse', 'revenue': 180.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba E.D Supply Co', 'revenue': 180.0}, {'customer': 'Prima Lighting Inc', 'revenue': 178.2}, {'customer': 'Pine Lighting', 'revenue': 174.8}, {'customer': 'Multi-Luminaire Gatineau', 'revenue': 165.0}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 165.0}, {'customer': 'Muskoka Lighting & Electric', 'revenue': 165.0}, {'customer': 'J.D. Lighting', 'revenue': 165.0}, {'customer': 'Scout & Nimble', 'revenue': 164.12}, {'customer': 'Chester Lighting : Doylestown Electric', 'revenue': 161.21}, {'customer': 'SBS Electric & Lighting', 'revenue': 160.89}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 158.4}, {'customer': 'Lighting Instyle', 'revenue': 154.08}, {'customer': 'Wolberg Electrical Supply Co', 'revenue': 150.0}, {'customer': 'Premier Bath, Lighting (MI)', 'revenue': 150.0}, {'customer': 'Kendall Electric Inc', 'revenue': 150.0}, {'customer': 'Dickman Supply', 'revenue': 150.0}, {'customer': 'Hall Electric Co Inc', 'revenue': 150.0}, {'customer': '!! Duncan Corporation dba Better Living', 'revenue': 150.0}, {'customer': 'Flambeaux Gas & Electric Lights', 'revenue': 150.0}, {'customer': 'Gadsden Lighting Showroom Inc', 'revenue': 150.0}, {'customer': 'The Jarrell Company', 'revenue': 150.0}, {'customer': 'White Star Supply LLC', 'revenue': 150.0}, {'customer': 'Fixture This', 'revenue': 150.0}, {'customer': 'Coast Lighting', 'revenue': 150.0}, {'customer': "Garbe's Lighting & Hardware LLC", 'revenue': 150.0}, {'customer': 'Team Electric Supply, LLC', 'revenue': 150.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 150.0}, {'customer': 'Fusion Light and Design', 'revenue': 150.0}, {'customer': 'Lighting EFX', 'revenue': 143.74}, {'customer': 'Menards, Inc', 'revenue': 142.5}, {'customer': 'Chester Lighting', 'revenue': 142.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 131.48}, {'customer': 'Lamp Warehouse dba Lighting Expo', 'revenue': 116.2}, {'customer': 'Lonestar Lighting & Technology', 'revenue': 105.66}, {'customer': 'Vermont Lighting', 'revenue': 90.7}, {'customer': 'DuPage Lighting', 'revenue': 90.0}, {'customer': 'Konstantin Gut dba Elegant Lighting (MA)', 'revenue': 90.0}, {'customer': 'The Focal Point SWLA LLC', 'revenue': 75.0}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 71.0}, {'customer': 'Fashion Light Center', 'revenue': 71.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 63.8}, {'customer': 'Hortons of LaGrange', 'revenue': 55.92}, {'customer': "Isabelle's Lighting", 'revenue': 41.65}, {'customer': 'The Lighting Corner', 'revenue': 9.9}, {'customer': 'Candlelight Light & Log', 'revenue': 0.0}, {'customer': 'J & B Supply Inc / JBS', 'revenue': 0.0}, {'customer': '!! Pelleco Home Design', 'revenue': 0.0}, {'customer': 'Littman Bros Energy Supplies', 'revenue': -58.09}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': -90.48}, {'customer': 'Muska Lighting', 'revenue': -91.4}, {'customer': 'Lighting Incorporated', 'revenue': -199.4}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': -671.13}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': -1072.9}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': -4460.5}] | [{'item': '9-302-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 144}, {'item': '9-303-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 139}, {'item': '9-7144-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 119}, {'item': '9-303-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 92}, {'item': '9-7144-1-44', 'desc': 'Monroe 1-Light Wall Sconce in Classic Bronze', 'available': 64}, {'item': '9-7144-1-109', 'desc': 'Monroe 1-Light Wall Sconce in Polished Nickel', 'available': 61}] |
| 1-2221-6-322 | Salerno 6-Light Chandelier in Warm Brass | SALER | 303,275.41 | 1,667 | — | 2026-06-27 | [{'customer': 'WAYFAIR LLC', 'revenue': 89502.86}, {'customer': 'Shades of Light', 'revenue': 48033.19}, {'customer': 'FERGUSON', 'revenue': 23608.18}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 11128.5}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 7085.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 6939.75}, {'customer': 'BUILD.COM', 'revenue': 6329.68}, {'customer': 'BELAMI ECommerce', 'revenue': 5561.89}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 5176.46}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 4657.77}, {'customer': 'LAMPS PLUS INC', 'revenue': 4652.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 3645.68}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 3514.9}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 3491.5}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 3142.88}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 3133.25}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 2750.0}, {'customer': 'Lighting World', 'revenue': 2716.74}, {'customer': 'The Home Depot', 'revenue': 2688.23}, {'customer': 'Inline Electric Supply', 'revenue': 2687.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2511.0}, {'customer': 'LIGHTING BY JARED', 'revenue': 2425.33}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 2364.05}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 2058.7}, {'customer': 'St Louis Metro Electric', 'revenue': 2025.88}, {'customer': 'Sunbelt / Louisiana', 'revenue': 1945.62}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 1809.9}, {'customer': 'Lighting Design Company', 'revenue': 1651.4}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 1594.0}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 1439.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 1375.0}, {'customer': '!! Reflections L&M', 'revenue': 1374.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 1274.9}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 1221.0}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 1166.84}, {'customer': 'Lightology', 'revenue': 1155.21}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 1131.05}, {'customer': "Wilkinson's House of Lighting", 'revenue': 891.0}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 890.23}, {'customer': 'HOUZZ SHOP', 'revenue': 874.49}, {'customer': "LOWE'S", 'revenue': 832.88}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 825.0}, {'customer': 'Lights Unlimited', 'revenue': 805.6}, {'customer': "Richard's Lighting", 'revenue': 803.7}, {'customer': 'Lighting Emporium Inc', 'revenue': 785.5}, {'customer': 'Pine Tree Lighting dba Pine Tree Furniture', 'revenue': 779.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 687.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 618.75}, {'customer': 'LJP Enterprises, Inc. dba Southside Lighting Gallery', 'revenue': 618.3}, {'customer': 'House of Carpets', 'revenue': 563.6}, {'customer': 'All About Lights Inc', 'revenue': 559.4}, {'customer': 'Austell Lighting', 'revenue': 550.0}, {'customer': 'Village 1, LLC dba Village Home Stores', 'revenue': 550.0}, {'customer': 'Lighting Design Center (Las Vegas)', 'revenue': 550.0}, {'customer': 'AT HOME LLC dba HOME LIGHTING', 'revenue': 548.95}, {'customer': 'Team Electric Supply, LLC', 'revenue': 504.0}, {'customer': 'Accent Lighting (OR)', 'revenue': 504.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 495.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 488.0}, {'customer': 'Re-Lighting Inc', 'revenue': 486.2}, {'customer': 'Uncommon Living fka Lighting Unlimited (MS)', 'revenue': 458.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 458.0}, {'customer': 'IBS Lighting LLC', 'revenue': 458.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 450.01}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 439.68}, {'customer': 'Ocean Pacific Lighting Inc', 'revenue': 428.24}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 406.7}, {'customer': 'Connecticut Lighting Center', 'revenue': 403.2}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 385.83}, {'customer': 'Urban Rustic Living', 'revenue': 375.62}, {'customer': 'Rexel USA, Inc. : Mayer Electric Gulfport MS', 'revenue': 343.75}, {'customer': 'Signature Lighting & Fans dba Whitfield Lighting and Furnitu', 'revenue': 302.5}, {'customer': 'Pine Lighting', 'revenue': 302.5}, {'customer': 'Royaume Luminaire', 'revenue': 302.5}, {'customer': 'Net Retailers, LLC', 'revenue': 297.45}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 296.46}, {'customer': 'Asburys Design', 'revenue': 295.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 275.0}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 275.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 275.0}, {'customer': 'The Jarrell Company', 'revenue': 275.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 275.0}, {'customer': "Randolph's Door & Lighting dba RDHS Inc", 'revenue': 275.0}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 275.0}, {'customer': 'Plyler Supply Co. Inc DBA The Lighting Loft', 'revenue': 275.0}, {'customer': 'US Electrical Services, Inc DBA Yale Electric Supply', 'revenue': 275.0}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 275.0}, {'customer': 'First Coast Lighting & Fans', 'revenue': 275.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 275.0}, {'customer': 'Stokes Electric Company', 'revenue': 275.0}, {'customer': 'Elaine Everetts Lighting', 'revenue': 275.0}, {'customer': 'GW Keeter Lighting', 'revenue': 275.0}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 275.0}, {'customer': 'Home Front Design', 'revenue': 275.0}, {'customer': 'Pace Lighting Inc', 'revenue': 275.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Owensboro KY', 'revenue': 275.0}, {'customer': '!! Source & Co.', 'revenue': 265.07}, {'customer': 'Cape Electrical Supply', 'revenue': 258.5}, {'customer': 'Veradyne Unlimited', 'revenue': 258.46}, {'customer': 'Melody Lighting, Inc', 'revenue': 257.06}, {'customer': 'City Lightz London', 'revenue': 251.9}, {'customer': 'King Electric Company Inc', 'revenue': 246.73}, {'customer': 'Lyteworks', 'revenue': 235.76}, {'customer': 'ZenSupply Inc', 'revenue': 233.87}, {'customer': 'Van Stavern Interiors Inc', 'revenue': 233.5}, {'customer': 'Flinz Holdings LLC', 'revenue': 229.0}, {'customer': '!! WT Lighting', 'revenue': 229.0}, {'customer': 'Endacott Lighting DBA S&S Edison', 'revenue': 229.0}, {'customer': 'Illuminating Expressions (Evansville)', 'revenue': 229.0}, {'customer': 'SOUTHWEST PLUMBING SUPPLY', 'revenue': 229.0}, {'customer': 'North Coast Lighting, LLC (SE)', 'revenue': 229.0}, {'customer': 'Design Superstore / Designco', 'revenue': 229.0}, {'customer': 'Cayce Mill Supply Co', 'revenue': 229.0}, {'customer': 'Bright Ideas Lighting & More (Bridgeport)', 'revenue': 229.0}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 229.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 229.0}, {'customer': 'LIGHTING CONCEPTS, LLC (GA)', 'revenue': 229.0}, {'customer': 'Lampworks dba Lamp & Shadework', 'revenue': 229.0}, {'customer': 'White Star Supply LLC', 'revenue': 229.0}, {'customer': 'Kendall Electric Inc', 'revenue': 229.0}, {'customer': '!! Davis Lighting', 'revenue': 226.65}, {'customer': 'Enterprise Wholesale, Inc', 'revenue': 225.24}, {'customer': 'Menards, Inc', 'revenue': 217.55}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Teche Electric Supply', 'revenue': 213.0}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 213.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 213.0}, {'customer': '!! Applico, LLC', 'revenue': 213.0}, {'customer': 'Grand Rapids Lighting', 'revenue': 213.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Cookeville TN', 'revenue': 213.0}, {'customer': 'The Broadway Showroom dba Bliss Lighting', 'revenue': 213.0}, {'customer': 'Lumen Nation LLC', 'revenue': 213.0}, {'customer': 'WOLFE LIGHTING & ACCENTS : WOLFE LIGHTING & ACCENTS (TWIN FA', 'revenue': 213.0}, {'customer': 'Lighting Incorporated', 'revenue': 213.0}, {'customer': 'Bright City Lights', 'revenue': 213.0}, {'customer': 'Fort Worth Lighting', 'revenue': 213.0}, {'customer': 'Butler Lighting of High Point', 'revenue': 213.0}, {'customer': 'Lighting Instyle', 'revenue': 208.75}, {'customer': 'Lifestyles Store Inc', 'revenue': 194.65}, {'customer': 'Hagens Lighting', 'revenue': 191.8}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 183.2}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': 176.0}, {'customer': 'Galleria Lighting Inc.', 'revenue': 82.5}, {'customer': 'The Lighting Corner', 'revenue': 0.0}, {'customer': 'Light Gallery Plus', 'revenue': 0.0}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 0.0}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB)', 'revenue': -229.16}, {'customer': 'Rensen House of Lights', 'revenue': -2454.0}] | [{'item': '1-2221-6-109', 'desc': 'Salerno 6-Light Chandelier in Polished Nickel', 'available': 110}, {'item': '1-2221-6-83', 'desc': 'Salerno 6-Light Chandelier in Bisque White', 'available': 46}, {'item': '1-2221-6-89', 'desc': 'Salerno 6-Light Chandelier in Matte Black', 'available': 24}] |
| 7-1804-4-322 | Crawford 4-Light Pendant in Warm Brass | CRAWF | 286,652.26 | 1,374 | — | 2026-07-11 | [{'customer': 'FERGUSON', 'revenue': 73131.19}, {'customer': 'BUILD.COM', 'revenue': 42229.85}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 15666.75}, {'customer': 'BELAMI ECommerce', 'revenue': 10084.8}, {'customer': 'WAYFAIR LLC', 'revenue': 8312.05}, {'customer': 'First Coast Lighting & Fans', 'revenue': 6403.7}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 5824.1}, {'customer': 'Sunbelt / Louisiana', 'revenue': 5583.0}, {'customer': 'Lighting World', 'revenue': 5556.75}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 5501.95}, {'customer': 'The Home Depot', 'revenue': 5473.69}, {'customer': 'LIGHTING BY JARED', 'revenue': 4535.94}, {'customer': 'St Louis Metro Electric', 'revenue': 4250.0}, {'customer': 'LAMPS PLUS INC', 'revenue': 4223.74}, {'customer': "Richard's Lighting", 'revenue': 3865.62}, {'customer': 'Lifestyles Store Inc', 'revenue': 3028.92}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 3019.62}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 2681.4}, {'customer': 'Muska Lighting', 'revenue': 2540.1}, {'customer': 'Union Lighting (Montreal)', 'revenue': 2124.4}, {'customer': 'Lighting Incorporated', 'revenue': 1986.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 1948.56}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 1834.44}, {'customer': 'Lamps.com, Inc', 'revenue': 1785.54}, {'customer': "LOWE'S", 'revenue': 1730.21}, {'customer': 'Wiseway Supply', 'revenue': 1576.0}, {'customer': 'Lighting Design Company', 'revenue': 1564.5}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting : DesignDir', 'revenue': 1391.6}, {'customer': 'Inline Electric Supply', 'revenue': 1390.0}, {'customer': 'Hudson Parc Lighting & Design', 'revenue': 1272.0}, {'customer': 'Cambridge Interiors dba Inspired Interiors', 'revenue': 1232.8}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 1206.3}, {'customer': "Wilkinson's House of Lighting", 'revenue': 1206.0}, {'customer': 'Flambeaux Gas & Electric Lights', 'revenue': 1206.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 1160.0}, {'customer': 'Denali Lighting LLC', 'revenue': 1147.34}, {'customer': 'IB Lighting Supply', 'revenue': 1112.0}, {'customer': 'Lights Unlimited', 'revenue': 1112.0}, {'customer': 'Bayside Electric Supply Co', 'revenue': 1020.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 1020.0}, {'customer': 'Wilson Lighting of Naples Inc', 'revenue': 1017.25}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 994.0}, {'customer': 'Illuminations', 'revenue': 992.2}, {'customer': 'Menards, Inc', 'revenue': 969.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 950.4}, {'customer': 'VALENCIA LIGHTING & DESIGN', 'revenue': 928.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 928.0}, {'customer': 'Elektra Lights & Fans Inc', 'revenue': 834.0}, {'customer': 'American Lighting Inc', 'revenue': 834.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 834.0}, {'customer': 'The Light House (AL)', 'revenue': 834.0}, {'customer': 'Liza Joyner Designs Ryser', 'revenue': 834.0}, {'customer': 'Timberlake Lighting of Lynchburg', 'revenue': 834.0}, {'customer': 'Lightology', 'revenue': 832.64}, {'customer': 'Wholesale Lighting Inc (FL)', 'revenue': 750.6}, {'customer': 'New Age Interiors', 'revenue': 745.98}, {'customer': 'Passion Lighting DBA Cannon & Crossbow', 'revenue': 742.0}, {'customer': 'Legend Lighting', 'revenue': 696.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Daphne AL', 'revenue': 696.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba Billows Electric', 'revenue': 657.0}, {'customer': "Isabelle's Lighting", 'revenue': 643.86}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (BOCA RATON)', 'revenue': 625.5}, {'customer': 'Rainbow Lighting (NY)', 'revenue': 624.15}, {'customer': 'Unique Lighting Inc', 'revenue': 611.6}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 600.23}, {'customer': 'Southern Pipe & Supply (GA)', 'revenue': 598.46}, {'customer': 'Caminiti Associates Inc dba CAI Designs', 'revenue': 595.08}, {'customer': 'Net Retailers, LLC', 'revenue': 594.72}, {'customer': 'The Lighting Gallery (Huntington Station)', 'revenue': 591.3}, {'customer': 'ShellKat LLC dba Aldridge Appliance', 'revenue': 580.0}, {'customer': "Butler's Electric (Myrtle Beach)", 'revenue': 576.55}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 556.0}, {'customer': 'Lighting Resource Studio', 'revenue': 556.0}, {'customer': 'Home & Light Valdosta', 'revenue': 556.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 556.0}, {'customer': 'F.W. Webb Company', 'revenue': 556.0}, {'customer': 'Fort Worth Lighting', 'revenue': 556.0}, {'customer': 'Torrington Supply dba Torrco', 'revenue': 556.0}, {'customer': 'Lightstyles by Light Bulbs Etc (Orange) (BMD)', 'revenue': 556.0}, {'customer': 'Lighting Emporium Inc', 'revenue': 556.0}, {'customer': 'Queen City Stone dba Queen City Studio', 'revenue': 556.0}, {'customer': 'Hagens Lighting', 'revenue': 556.0}, {'customer': 'Winsupply Elizabethtown : Winsupply dba Bowling Green WLC 14', 'revenue': 556.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 556.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 545.0}, {'customer': 'Cregger Co LLC', 'revenue': 527.76}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (PARAMUS)', 'revenue': 522.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 510.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': 510.0}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 500.6}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 493.74}, {'customer': 'The Lamp and Lighthouse (TN)', 'revenue': 470.69}, {'customer': 'Locke Supply', 'revenue': 464.0}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 464.0}, {'customer': "Garbe's Lighting & Hardware LLC", 'revenue': 464.0}, {'customer': 'The Light House Gallery (MO)', 'revenue': 464.0}, {'customer': 'BEAUTIFUL LIGHTS LLC', 'revenue': 461.56}, {'customer': 'Capitol Lighting Gallery', 'revenue': 444.8}, {'customer': 'BBC Lighting & Supply', 'revenue': 438.0}, {'customer': 'White Star Supply LLC', 'revenue': 438.0}, {'customer': "!! Amber's Lighting", 'revenue': 438.0}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 432.5}, {'customer': 'Cleveland Lighting Center', 'revenue': 372.3}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 359.16}, {'customer': 'Dhillon Lighting Inc (Edmonton) : Dhillon Lighting Manitoba', 'revenue': 350.71}, {'customer': 'Dhillon Lighting Inc (Edmonton)', 'revenue': 340.23}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 328.5}, {'customer': 'Cardinal Lights Corp DBA Manasquan Lighting', 'revenue': 296.34}, {'customer': 'The Lighting Marketplace DBA FixtureFarm', 'revenue': 293.04}, {'customer': 'Gross Lighting & Home', 'revenue': 278.0}, {'customer': 'Hortons of LaGrange', 'revenue': 278.0}, {'customer': 'Construction Resources Co LLC dba CR Lighting', 'revenue': 278.0}, {'customer': 'Home Lighting Inc. (PA)', 'revenue': 278.0}, {'customer': 'Asburys Design', 'revenue': 246.21}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 245.0}, {'customer': 'SBS Electric & Lighting', 'revenue': 243.17}, {'customer': '!! Savoy House Cash Sales', 'revenue': 242.0}, {'customer': 'Morrison Supply Co (Lubbock) : Morrison Supply Co (Abilene)', 'revenue': 232.0}, {'customer': 'House of Lights of Sanford Inc', 'revenue': 232.0}, {'customer': 'Sanders Supply Inc', 'revenue': 232.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 219.0}, {'customer': 'Denney Electric Supply (Ambler, PA)', 'revenue': 219.0}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 199.2}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 197.1}, {'customer': 'Kendall Electric Inc', 'revenue': 195.88}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 181.19}, {'customer': 'Sonepar dba Capital Electric', 'revenue': 109.5}, {'customer': 'Kay Electric Supply Co. Inc', 'revenue': 93.2}, {'customer': 'Fixture This', 'revenue': 38.5}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba All Phase Pet', 'revenue': 0.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 0.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 0.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 0.0}, {'customer': 'Elliott Electric Supply Inc', 'revenue': 0.0}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 0.0}, {'customer': 'State Electric Supply', 'revenue': 0.0}, {'customer': 'Stokes Electric Company', 'revenue': 0.0}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 0.0}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': 0.0}, {'customer': 'Lighting and Design by J & K Electric', 'revenue': 0.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 0.0}, {'customer': 'Lamp Shop of Naples Co', 'revenue': 0.0}, {'customer': 'Valley Supply Co', 'revenue': 0.0}, {'customer': '!! Lando Lighting', 'revenue': -90.42}, {'customer': 'The Lamp Outlet : Quinn Wholesale LLC dba Quintessential Lig', 'revenue': -113.1}, {'customer': 'Lighting EFX', 'revenue': -1021.48}] | [{'item': '6-1802-3-SN', 'desc': 'Crawford 3-Light Ceiling Light in Satin Nickel', 'available': 87}, {'item': '7-1803-3-SN', 'desc': 'Crawford 3-Light Pendant in Satin Nickel', 'available': 85}, {'item': '9-1801-1-89', 'desc': 'Crawford 1-Light Wall Sconce in Matte Black', 'available': 66}, {'item': '7-1803-3-89', 'desc': 'Crawford 3-Light Pendant in Matte Black', 'available': 55}, {'item': '9-1801-1-SN', 'desc': 'Crawford 1-Light Wall Sconce in Satin Nickel', 'available': 53}, {'item': '7-1804-4-89', 'desc': 'Crawford 4-Light Pendant in Matte Black', 'available': 52}, {'item': '6-1802-3-322', 'desc': 'Crawford 3-Light Ceiling Light in Warm Brass', 'available': 44}, {'item': '7-1804-4-SN', 'desc': 'Crawford 4-Light Pendant in Satin Nickel', 'available': 36}, {'item': '7-1803-3-322', 'desc': 'Crawford 3-Light Pendant in Warm Brass', 'available': 27}, {'item': '9-1801-1-322', 'desc': 'Crawford 1-Light Wall Sconce in Warm Brass', 'available': 17}] |
| 7-1774-6-320 | Ashburn 6-Light Pendant in Warm Brass and Rope | ASHBU | 233,394.02 | 560 | — | 2026-07-16 | [{'customer': 'WAYFAIR LLC', 'revenue': 44777.92}, {'customer': 'BUILD.COM', 'revenue': 19259.91}, {'customer': 'FERGUSON', 'revenue': 12385.36}, {'customer': 'LAMPS PLUS INC', 'revenue': 11522.02}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 11159.65}, {'customer': 'First Coast Lighting & Fans', 'revenue': 8348.7}, {'customer': 'Muska Lighting', 'revenue': 7390.4}, {'customer': 'BELAMI ECommerce', 'revenue': 5428.55}, {'customer': 'Lighting World', 'revenue': 4508.2}, {'customer': '!! U.S. Electrical Services Inc. dba Wiedenbach Brown', 'revenue': 3992.0}, {'customer': 'M & M Lighting, L.P.', 'revenue': 3326.0}, {'customer': 'The Lighting Corner', 'revenue': 3069.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 2913.75}, {'customer': 'Lightology', 'revenue': 2872.96}, {'customer': 'Lighting Design Company', 'revenue': 2762.1}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 2387.6}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 2283.78}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 1944.58}, {'customer': 'LIGHTING BY JARED', 'revenue': 1906.62}, {'customer': 'Hye Lighting Co', 'revenue': 1804.37}, {'customer': 'Destin Lighting', 'revenue': 1696.95}, {'customer': '!! Lando Lighting', 'revenue': 1686.52}, {'customer': 'Florida Lighting dba Lighting Depot dba Fla Lighting Inc', 'revenue': 1672.51}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 1587.0}, {'customer': '!! Modern Komfort Furnishings Inc.', 'revenue': 1560.4}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 1557.0}, {'customer': 'The Lamp Outlet : Quinn Wholesale LLC dba Quintessential Lig', 'revenue': 1419.8}, {'customer': 'Lamps.com, Inc', 'revenue': 1392.08}, {'customer': 'Inline Electric Supply', 'revenue': 1270.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 1270.0}, {'customer': 'Southern Lights', 'revenue': 1270.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 1247.4}, {'customer': 'Capitol Lighting Gallery', 'revenue': 1233.0}, {'customer': 'Echelon Interiors', 'revenue': 1204.15}, {'customer': 'Southern Interiors & Lighting (Warner Robins)', 'revenue': 1164.0}, {'customer': 'Walnut Creek Lighting', 'revenue': 1164.0}, {'customer': 'Rainbow Lighting (NY)', 'revenue': 1143.0}, {'customer': 'Light N Leisure Inc', 'revenue': 1058.0}, {'customer': 'LJP Enterprises, Inc. dba Southside Lighting Gallery', 'revenue': 1058.0}, {'customer': 'Design Superstore / Designco', 'revenue': 1058.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 1047.75}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 1028.0}, {'customer': 'Lighting Incorporated', 'revenue': 1009.25}, {'customer': 'Hubbard Supplyhouse', 'revenue': 1007.0}, {'customer': 'St Louis Metro Electric', 'revenue': 1006.36}, {'customer': 'Southern Lighting Gallery (Augusta) : Southern Lighting Gall', 'revenue': 948.1}, {'customer': 'Dement Lighting', 'revenue': 928.4}, {'customer': 'Lifestyles Store Inc', 'revenue': 899.3}, {'customer': 'Light and Day', 'revenue': 843.7}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 793.5}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (BOCA RATON)', 'revenue': 793.5}, {'customer': 'Royaume Luminaire', 'revenue': 698.5}, {'customer': 'LIGHTSHINE INC DBA URBAN LIGHTS', 'revenue': 694.18}, {'customer': 'The Lighting Showroom, Inc (CA)', 'revenue': 689.06}, {'customer': "Hinkley's Lighting Factory", 'revenue': 678.6}, {'customer': 'Eagle Lighting', 'revenue': 675.65}, {'customer': 'Lighting by Lavonne, LLC', 'revenue': 635.0}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 635.0}, {'customer': 'Gross Lighting & Home', 'revenue': 635.0}, {'customer': 'Greer Lighting Center LLC', 'revenue': 635.0}, {'customer': 'VP Supply', 'revenue': 635.0}, {'customer': 'Home & Light Valdosta', 'revenue': 635.0}, {'customer': 'Passion Lighting DBA Cannon & Crossbow', 'revenue': 635.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 635.0}, {'customer': 'Lighting Palace Design Center', 'revenue': 635.0}, {'customer': 'Paramont- EO, Inc', 'revenue': 635.0}, {'customer': "Wilkinson's House of Lighting", 'revenue': 635.0}, {'customer': 'Coley Electric & Plumbing (Douglas)', 'revenue': 635.0}, {'customer': 'Lighting by Design LLC (Maryland)', 'revenue': 635.0}, {'customer': 'Aztec Lighting', 'revenue': 635.0}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 635.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 635.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 635.0}, {'customer': "Butler's Electric (Myrtle Beach)", 'revenue': 635.0}, {'customer': 'Mayson Enterprises dba Aura Lighting', 'revenue': 635.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Teche Electric Supply', 'revenue': 635.0}, {'customer': 'Sun Lighting (Tempe)', 'revenue': 635.0}, {'customer': 'Milliken Investments dba Shallotte Electric Stores', 'revenue': 635.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 614.0}, {'customer': 'City Lights (San Francisco)', 'revenue': 595.73}, {'customer': 'Richardson Lighting', 'revenue': 581.9}, {'customer': "Don's Light House LTD", 'revenue': 581.9}, {'customer': 'Consumers Lighting and Lamps', 'revenue': 574.95}, {'customer': 'Expressions Home Lighting', 'revenue': 571.5}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 558.8}, {'customer': 'Paradise Lighting', 'revenue': 548.9}, {'customer': 'Litemode Limited', 'revenue': 548.9}, {'customer': 'Queen City Stone dba Queen City Studio', 'revenue': 529.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 529.0}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 529.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba Billows Electric', 'revenue': 529.0}, {'customer': 'Lighting by Design (Exton, PA)', 'revenue': 529.0}, {'customer': 'Lamp Shop of Naples Co', 'revenue': 529.0}, {'customer': 'Accent Lighting (OR)', 'revenue': 529.0}, {'customer': "Christie's Lighting Gallery", 'revenue': 529.0}, {'customer': 'Front Street Lighting', 'revenue': 529.0}, {'customer': 'RDIC LLC dba Russell Home Decor / Russell Lands', 'revenue': 529.0}, {'customer': 'Fort Worth Lighting', 'revenue': 529.0}, {'customer': 'Legacy Lighting, LLC', 'revenue': 529.0}, {'customer': 'Timberlake Lighting of Lynchburg', 'revenue': 529.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 529.0}, {'customer': 'Bayside Electric Supply Co', 'revenue': 529.0}, {'customer': 'Lumber One Home Center', 'revenue': 529.0}, {'customer': 'Alice Stillabower Design', 'revenue': 529.0}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 529.0}, {'customer': 'Lighting Solutions Design (Owensboro)', 'revenue': 529.0}, {'customer': 'Cardinal Lights Corp DBA Manasquan Lighting', 'revenue': 529.0}, {'customer': "Richard's Lighting", 'revenue': 512.5}, {'customer': 'Lights Unlimited', 'revenue': 508.0}, {'customer': 'Idlewood Electric Supply', 'revenue': 508.0}, {'customer': 'Wilson Lighting of Naples Inc', 'revenue': 508.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 508.0}, {'customer': 'F.W. Webb Company', 'revenue': 507.84}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 499.0}, {'customer': 'Rite Rug DBA Capital Lighting', 'revenue': 499.0}, {'customer': 'Home Lighting Inc. (PA)', 'revenue': 499.0}, {'customer': 'IM Lighting', 'revenue': 499.0}, {'customer': 'Ellen Lighting and Hardware', 'revenue': 499.0}, {'customer': 'The Lighting Gallery (Huntington Station)', 'revenue': 476.1}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 465.58}, {'customer': 'Lyteworks', 'revenue': 460.35}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 449.1}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 439.12}, {'customer': "LOWE'S", 'revenue': 424.15}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 423.2}, {'customer': 'Connecticut Lighting Center', 'revenue': 423.2}, {'customer': 'Lighting Instyle', 'revenue': 416.8}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 412.74}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 342.8}, {'customer': 'Euroluce dba Home Lighting', 'revenue': 326.42}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': 99.9}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 12.7}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': -95.22}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': -102.97}, {'customer': 'Lighting Zone, Inc', 'revenue': -1350.0}] | [{'item': '3-1773-6-320', 'desc': 'Ashburn 6-Light Pendant in Warm Brass and Rope', 'available': 21}] |
| 1-312-15-322 | Middleton 15-Light Chandelier in Warm Brass | MIDDL | 188,669.81 | 218 | — | 2026-07-03 | [{'customer': 'WAYFAIR LLC', 'revenue': 19380.81}, {'customer': 'FERGUSON', 'revenue': 13821.8}, {'customer': 'Inline Electric Supply', 'revenue': 9599.0}, {'customer': 'Lights Unlimited', 'revenue': 6408.0}, {'customer': 'LAMPS PLUS INC', 'revenue': 5464.05}, {'customer': 'BELAMI ECommerce', 'revenue': 4723.35}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 4700.8}, {'customer': 'Lighting Design Company', 'revenue': 4411.0}, {'customer': "LOWE'S", 'revenue': 4150.04}, {'customer': 'First Coast Lighting & Fans', 'revenue': 3884.0}, {'customer': 'BUILD.COM', 'revenue': 3858.01}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': 3728.0}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 3591.24}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 3435.0}, {'customer': 'Palmer Electric Co dba Showcase Lighting (FL)', 'revenue': 3373.18}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 3301.0}, {'customer': 'The Brecher Co, Inc', 'revenue': 3154.4}, {'customer': 'IM Lighting', 'revenue': 3136.1}, {'customer': 'The Factory', 'revenue': 3052.0}, {'customer': 'Galleria Lighting Inc.', 'revenue': 3004.7}, {'customer': 'Home & Light Valdosta', 'revenue': 2913.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 2796.0}, {'customer': 'Lighting World', 'revenue': 2485.6}, {'customer': 'Farvahar Inc Dba Posh Lighting', 'revenue': 2389.59}, {'customer': 'Lighting Incorporated', 'revenue': 2378.75}, {'customer': 'F.W. Webb Company', 'revenue': 2352.31}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 2136.0}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 2136.0}, {'customer': 'Paulus Enterprises dba James & Co Lighting', 'revenue': 2136.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2081.0}, {'customer': 'Hortons of LaGrange', 'revenue': 1902.96}, {'customer': 'OSMOND DESIGNS INC.', 'revenue': 1747.5}, {'customer': 'Lamp Warehouse dba Lighting Expo', 'revenue': 1708.8}, {'customer': 'Aggieland Lighting', 'revenue': 1695.5}, {'customer': 'Lamps.com, Inc', 'revenue': 1670.12}, {'customer': 'Echelon Interiors', 'revenue': 1350.78}, {'customer': 'Southern Pipe & Supply (GA)', 'revenue': 1296.31}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 1281.5}, {'customer': '!! Gagnun Interior Concept Studio Inc DBA Boutique Intempore', 'revenue': 1281.5}, {'customer': 'The Electrical & Plumbing Store : Electrical & Plumbing Stor', 'revenue': 1281.5}, {'customer': 'Royal Lighting (Canada) dba Royal Lighting Limited Partnersh', 'revenue': 1281.5}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 1281.5}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba Billows Electric', 'revenue': 1165.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 1165.0}, {'customer': 'Stokes Electric Company', 'revenue': 1165.0}, {'customer': 'Muska Lighting', 'revenue': 1165.0}, {'customer': 'Paramont- EO, Inc', 'revenue': 1165.0}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 1165.0}, {'customer': 'Hagens Lighting', 'revenue': 1165.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 1165.0}, {'customer': 'Bright Ideas (Rochester)', 'revenue': 1165.0}, {'customer': 'Scott Electric Co', 'revenue': 1165.0}, {'customer': 'VALENCIA LIGHTING & DESIGN', 'revenue': 1165.0}, {'customer': "Seth's Lighting & Assoc. Inc", 'revenue': 1165.0}, {'customer': 'Design Superstore / Designco', 'revenue': 1165.0}, {'customer': 'Home Lighting Inc. (PA)', 'revenue': 1165.0}, {'customer': '!! Lighting Connections LLC', 'revenue': 1165.0}, {'customer': 'Dhillon Lighting Inc (Edmonton)', 'revenue': 1132.45}, {'customer': 'Elm Ridge Lighting & Interior', 'revenue': 1068.1}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 1068.1}, {'customer': 'St Louis Metro Electric', 'revenue': 1025.2}, {'customer': '!! CFSI Interiors Limited DBA Taylor Flooring', 'revenue': 1007.6}, {'customer': 'Asburys Design', 'revenue': 971.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 971.0}, {'customer': 'Ray Mart Inc dba Tri-Supply', 'revenue': 971.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 971.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 961.29}, {'customer': "Isabelle's Lighting", 'revenue': 932.16}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 916.62}, {'customer': "Designer's Mart", 'revenue': 916.0}, {'customer': 'Hi-Light Decorating', 'revenue': 916.0}, {'customer': 'Legend Lighting', 'revenue': 916.0}, {'customer': 'Timberlake Lighting of Lynchburg', 'revenue': 916.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 873.75}, {'customer': 'Mainland Lighting Warehouse', 'revenue': 753.41}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 745.6}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 687.0}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 627.33}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 545.0}, {'customer': 'Wilson 6 Enterprises Inc. DBA: Mountain Lighting & Design', 'revenue': 458.0}, {'customer': 'LIGHTING BY JARED', 'revenue': 93.2}, {'customer': 'Winsupply Elizabethtown : Winsupply dba Bowling Green WLC 14', 'revenue': 0.0}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': -373.7}, {'customer': 'Accent Lighting (KS)', 'revenue': -634.5}] | [{'item': '1-308-8-44', 'desc': 'Middleton 8-Light Chandelier in Classic Bronze', 'available': 65}, {'item': '1-308-8-322', 'desc': 'Middleton 8-Light Chandelier in Warm Brass', 'available': 62}, {'item': '1-308-8-89', 'desc': 'Middleton 8-Light Chandelier in Matte Black', 'available': 62}, {'item': '1-307-6-322', 'desc': 'Middleton 6-Light Chandelier in Warm Brass', 'available': 48}, {'item': '1-307-6-89', 'desc': 'Middleton 6-Light Chandelier in Matte Black', 'available': 43}, {'item': '1-308-8-SN', 'desc': 'Middleton 8-Light Chandelier in Satin Nickel', 'available': 41}, {'item': '1-312-15-89', 'desc': 'Middleton 15-Light Chandelier in Matte Black', 'available': 32}, {'item': '1-310-10-322', 'desc': 'Middleton 10-Light Chandelier in Warm Brass', 'available': 31}, {'item': '1-310-10-89', 'desc': 'Middleton 10-Light Chandelier in Matte Black', 'available': 28}] |
| 9-303-1-322 | Monroe 1-Light Wall Sconce in Warm Brass | MONRO | 186,435.44 | 3,151 | — | 2026-07-03 | [{'customer': 'WAYFAIR LLC', 'revenue': 38090.31}, {'customer': 'BUILD.COM', 'revenue': 17884.75}, {'customer': 'FERGUSON', 'revenue': 14022.57}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 10339.0}, {'customer': 'Gadsden Lighting Showroom Inc', 'revenue': 6027.24}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 5788.58}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 4748.25}, {'customer': 'Inline Electric Supply', 'revenue': 4490.0}, {'customer': 'LAMPS PLUS INC', 'revenue': 4126.3}, {'customer': 'Shades of Light', 'revenue': 3441.69}, {'customer': 'Sunbelt / Louisiana', 'revenue': 3306.5}, {'customer': "Richard's Lighting", 'revenue': 2877.57}, {'customer': 'Lifestyles Store Inc', 'revenue': 2796.0}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 2733.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 2544.1}, {'customer': 'BELAMI ECommerce', 'revenue': 2033.39}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 1886.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 1841.0}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 1748.0}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 1629.06}, {'customer': 'LIGHTING BY JARED', 'revenue': 1499.54}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 1432.44}, {'customer': "Wilkinson's House of Lighting", 'revenue': 1386.4}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 1185.0}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 1114.0}, {'customer': 'The Lighting Gallery (Huntington Station)', 'revenue': 1066.0}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 1056.3}, {'customer': 'Lighting World', 'revenue': 948.8}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 945.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 884.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 882.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 859.12}, {'customer': 'Gross Lighting & Home : Indiana Lighting Center', 'revenue': 857.0}, {'customer': 'Illuminate Lighting', 'revenue': 834.0}, {'customer': 'Lights Unlimited', 'revenue': 819.4}, {'customer': 'Western Chandelier Co', 'revenue': 793.45}, {'customer': 'Kendall Electric Inc', 'revenue': 784.0}, {'customer': 'Parrish Family Enterprises dba American Lighting and Design', 'revenue': 780.81}, {'customer': 'Lighting Design Company', 'revenue': 717.3}, {'customer': 'Net Retailers, LLC', 'revenue': 709.35}, {'customer': 'Ocean Pacific Lighting Inc', 'revenue': 705.54}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 622.0}, {'customer': 'Richardson Lighting', 'revenue': 616.39}, {'customer': 'Stokes Electric Company', 'revenue': 616.0}, {'customer': 'Chester Lighting : Doylestown Electric', 'revenue': 592.97}, {'customer': 'The Brecher Co, Inc', 'revenue': 588.31}, {'customer': 'IBS Lighting LLC', 'revenue': 588.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 588.0}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 576.4}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 575.0}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 574.0}, {'customer': 'Design Superstore / Designco', 'revenue': 574.0}, {'customer': 'House of Carpets', 'revenue': 563.05}, {'customer': 'Hudson Parc Lighting & Design', 'revenue': 556.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 530.6}, {'customer': 'J.D. Lighting', 'revenue': 503.8}, {'customer': 'St Louis Metro Electric', 'revenue': 482.24}, {'customer': 'McManus Company', 'revenue': 474.0}, {'customer': 'Dement Lighting', 'revenue': 469.2}, {'customer': 'LDB Holdings LLC dba CW Floors and Lighting', 'revenue': 458.0}, {'customer': 'Lightology', 'revenue': 453.36}, {'customer': 'Lighting Emporium Inc', 'revenue': 445.6}, {'customer': 'Southern Pipe & Supply (GA)', 'revenue': 435.62}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 431.2}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 431.2}, {'customer': 'The Electrical & Plumbing Store : Electrical & Plumbing Stor', 'revenue': 431.2}, {'customer': 'Laura of Pembroke', 'revenue': 416.74}, {'customer': 'HOUZZ SHOP', 'revenue': 416.22}, {'customer': 'Multi-Luminaire Gatineau : Multi-Luminaire (Ottawa)', 'revenue': 411.4}, {'customer': 'Elan Studio Lighting', 'revenue': 410.0}, {'customer': 'Flinz Holdings LLC', 'revenue': 410.0}, {'customer': 'Denali Lighting LLC', 'revenue': 404.83}, {'customer': 'Locke Supply', 'revenue': 392.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 392.0}, {'customer': 'Construction Resources Co LLC dba CR Lighting', 'revenue': 392.0}, {'customer': 'Virginia-Carolina Lighting Inc dba Coastal Lighting & Supply', 'revenue': 392.0}, {'customer': '!! U.S. Electrical Services Inc. dba Wiedenbach Brown', 'revenue': 385.0}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 385.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 375.08}, {'customer': 'F.W. Webb Company', 'revenue': 360.6}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 360.0}, {'customer': 'KLS LLC dba Spectrum Lighting', 'revenue': 360.0}, {'customer': 'American Lighting Inc', 'revenue': 360.0}, {'customer': "Isabelle's Lighting", 'revenue': 353.44}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 352.88}, {'customer': 'Queen City Stone dba Queen City Studio', 'revenue': 345.31}, {'customer': 'Lighting Instyle', 'revenue': 344.56}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 344.4}, {'customer': 'Denney Electric Supply (Ambler, PA)', 'revenue': 328.0}, {'customer': 'The Lighting Corner', 'revenue': 328.0}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 328.0}, {'customer': 'Meuth Wallpaper dba Sugar Bakers', 'revenue': 323.4}, {'customer': 'Lights of Oconee', 'revenue': 318.0}, {'customer': 'Paulus Enterprises dba James & Co Lighting', 'revenue': 318.0}, {'customer': 'Accent Lighting (KS)', 'revenue': 313.6}, {'customer': '!! Carly Blalock Interiors', 'revenue': 311.85}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Teche Electric Supply', 'revenue': 308.0}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 296.8}, {'customer': 'Team Electric Supply, LLC', 'revenue': 294.0}, {'customer': "LOWE'S", 'revenue': 289.94}, {'customer': "Christie's Lighting Gallery", 'revenue': 289.51}, {'customer': 'Gateway Lighting & Design Inc', 'revenue': 280.5}, {'customer': 'The Finishing Touch', 'revenue': 269.37}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 264.55}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 262.3}, {'customer': 'Home & Light Valdosta', 'revenue': 256.67}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 246.65}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba North Coast Light', 'revenue': 246.0}, {'customer': '!! Ana Cole Interiors Ltd', 'revenue': 245.0}, {'customer': 'Lighting Incorporated', 'revenue': 231.0}, {'customer': 'Rite Rug DBA Capital Lighting', 'revenue': 231.0}, {'customer': 'Hortons of LaGrange', 'revenue': 231.0}, {'customer': 'Pineridge Hollow/Corp 3641015', 'revenue': 215.6}, {'customer': 'Royal Lighting (Canada) dba Royal Lighting Limited Partnersh', 'revenue': 215.6}, {'customer': 'Cregger Co LLC', 'revenue': 212.43}, {'customer': 'The Lighthouse (ME)', 'revenue': 208.32}, {'customer': 'Southern Pipe & Supply (LA)', 'revenue': 207.89}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 196.0}, {'customer': 'Anzalone Electric', 'revenue': 196.0}, {'customer': 'The Jarrell Company', 'revenue': 196.0}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': 196.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 196.0}, {'customer': 'Southern Interiors & Lighting (Warner Robins)', 'revenue': 196.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 194.04}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 184.5}, {'customer': 'Aiken Lighting', 'revenue': 183.25}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 180.4}, {'customer': 'Cayce Mill Supply Co', 'revenue': 177.62}, {'customer': 'Wilson 6 Enterprises Inc. DBA: Mountain Lighting & Design', 'revenue': 176.4}, {'customer': 'Pine Lighting', 'revenue': 175.48}, {'customer': 'Lamps.com, Inc', 'revenue': 167.69}, {'customer': 'The Home Depot', 'revenue': 166.76}, {'customer': 'Sun Lighting (Tempe)', 'revenue': 164.0}, {'customer': 'Mathes of Alabama Elec. Supply', 'revenue': 164.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 164.0}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 164.0}, {'customer': 'Premier Bath, Lighting (MI)', 'revenue': 164.0}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 164.0}, {'customer': 'White Star Supply LLC', 'revenue': 164.0}, {'customer': 'Ellen Lighting and Hardware', 'revenue': 154.0}, {'customer': 'Colonial Electric Supply Co', 'revenue': 154.0}, {'customer': 'Lighting EFX', 'revenue': 152.19}, {'customer': 'IM Lighting', 'revenue': 146.8}, {'customer': 'Butler Lighting of High Point', 'revenue': 146.3}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 144.32}, {'customer': 'First Coast Lighting & Fans', 'revenue': 138.6}, {'customer': 'Idlewood Electric Supply', 'revenue': 131.2}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 131.2}, {'customer': 'Light Gallery Plus', 'revenue': 98.0}, {'customer': 'Pine Tree Lighting dba Pine Tree Furniture', 'revenue': 98.0}, {'customer': 'Lighting South LLC', 'revenue': 92.0}, {'customer': 'BGZA, INC. dba BG Design Center', 'revenue': 89.57}, {'customer': 'Southern Lighting (Chattanooga)', 'revenue': 82.0}, {'customer': 'Coco & Dash', 'revenue': 82.0}, {'customer': "Victor's Lighting", 'revenue': 80.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting : DesignDir', 'revenue': 78.4}, {'customer': 'DISCOUNT PLUMBING & ELECTRIC', 'revenue': 77.0}, {'customer': '!! Gagnun Interior Concept Studio Inc DBA Boutique Intempore', 'revenue': 75.79}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 73.29}, {'customer': 'Light Brite Distributing Inc.', 'revenue': 7.33}, {'customer': 'Wiseway Supply', 'revenue': 0.0}, {'customer': '!! Lando Lighting', 'revenue': 0.0}, {'customer': 'Danielhouse Studios, Inc', 'revenue': 0.0}, {'customer': 'Littman Bros Energy Supplies', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': -115.9}, {'customer': 'J & B Supply Inc / JBS', 'revenue': -154.0}, {'customer': 'M & M Lighting, L.P.', 'revenue': -366.93}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': -1113.2}] | [{'item': '9-302-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 144}, {'item': '9-303-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 139}, {'item': '9-7144-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 119}, {'item': '9-303-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 92}, {'item': '9-7144-1-44', 'desc': 'Monroe 1-Light Wall Sconce in Classic Bronze', 'available': 64}, {'item': '9-7144-1-109', 'desc': 'Monroe 1-Light Wall Sconce in Polished Nickel', 'available': 61}] |
| M60008NB | 2-Light Ceiling Light in Natural Brass | MSEMI | 163,302.89 | 3,063 | — | 2026-07-03 | [{'customer': 'The Home Depot', 'revenue': 34605.62}, {'customer': 'BUILD.COM', 'revenue': 29943.33}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 16677.31}, {'customer': 'WAYFAIR LLC', 'revenue': 13475.54}, {'customer': 'FERGUSON', 'revenue': 5868.75}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 4592.8}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 4535.79}, {'customer': 'Menards, Inc', 'revenue': 3286.19}, {'customer': 'Inline Electric Supply', 'revenue': 2354.0}, {'customer': "Richard's Lighting", 'revenue': 2329.95}, {'customer': 'HOUZZ SHOP', 'revenue': 2328.0}, {'customer': '!! Newburyport Lighting', 'revenue': 1980.85}, {'customer': 'Save More Plumbing & Lighting', 'revenue': 1351.2}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 1350.89}, {'customer': 'Connecticut Lighting Center', 'revenue': 1258.2}, {'customer': 'KIE SUPPLY INC', 'revenue': 1223.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 1108.0}, {'customer': 'Hortons of LaGrange', 'revenue': 1092.72}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 1089.7}, {'customer': 'LAMPS PLUS INC', 'revenue': 1063.7}, {'customer': 'Lights Unlimited', 'revenue': 928.2}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 873.0}, {'customer': 'PC Building Materials Inc', 'revenue': 873.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 868.72}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 803.63}, {'customer': 'Kendall Electric Inc', 'revenue': 733.0}, {'customer': 'Home & Light Valdosta', 'revenue': 684.0}, {'customer': 'The Glow Works, Inc', 'revenue': 674.9}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 673.92}, {'customer': 'Grand Rapids Lighting', 'revenue': 669.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 627.0}, {'customer': 'House of Lights (Mayfield Heights)', 'revenue': 608.0}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 583.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 568.7}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 559.68}, {'customer': 'Masterpiece Lighting (GA)', 'revenue': 548.83}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 523.93}, {'customer': 'Canadian Heritage Designs Ltd. DBA CF Interiors', 'revenue': 516.25}, {'customer': 'Elektra Lights & Fans Inc', 'revenue': 504.0}, {'customer': 'Lamps.com, Inc', 'revenue': 503.5}, {'customer': "LOWE'S", 'revenue': 488.23}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 480.0}, {'customer': 'WAI Products LTD DBA Kohara + Co', 'revenue': 479.96}, {'customer': "Seth's Lighting & Assoc. Inc", 'revenue': 456.0}, {'customer': 'American Lighting Inc', 'revenue': 454.0}, {'customer': 'Net Retailers, LLC', 'revenue': 449.18}, {'customer': 'All About Lights Inc', 'revenue': 441.0}, {'customer': 'Crown Electrical Supply', 'revenue': 405.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 379.2}, {'customer': 'Lamps Expo', 'revenue': 358.39}, {'customer': 'Pine Lighting', 'revenue': 346.76}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB)', 'revenue': 344.08}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 341.0}, {'customer': 'Lighting by Design LLC (Maryland)', 'revenue': 337.0}, {'customer': 'Lighting Design Company', 'revenue': 332.8}, {'customer': '!! Maison Olive Inc.', 'revenue': 321.83}, {'customer': 'Southern Lights', 'revenue': 317.52}, {'customer': 'The Lighting Shoppe Inc.', 'revenue': 314.11}, {'customer': 'Lighting by Lavonne, LLC', 'revenue': 311.0}, {'customer': 'Homestyles', 'revenue': 304.0}, {'customer': 'Design Lighting Sales', 'revenue': 303.16}, {'customer': 'The Brecher Co, Inc', 'revenue': 303.0}, {'customer': 'J.D. Lighting', 'revenue': 300.96}, {'customer': 'Lighting Reflects Design', 'revenue': 277.2}, {'customer': 'Western Chandelier Co', 'revenue': 275.8}, {'customer': 'Danielhouse Studios, Inc', 'revenue': 274.22}, {'customer': 'Elan Studio Lighting', 'revenue': 265.0}, {'customer': '!! CFSI Interiors Limited DBA Taylor Flooring', 'revenue': 259.6}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 249.8}, {'customer': 'Capital City Design Center', 'revenue': 248.0}, {'customer': 'Lifestyles Store Inc', 'revenue': 236.3}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 228.0}, {'customer': 'Premier Bath, Lighting (MI)', 'revenue': 228.0}, {'customer': 'Lighting Instyle', 'revenue': 228.0}, {'customer': 'LJP Enterprises, Inc. dba Southside Lighting Gallery', 'revenue': 228.0}, {'customer': 'Accent Lighting (KS)', 'revenue': 227.9}, {'customer': 'JW Bird and Company Ltd DBA Bird Stairs', 'revenue': 222.2}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 220.88}, {'customer': 'Cleveland Lighting Center', 'revenue': 215.0}, {'customer': 'Team Electric Supply, LLC', 'revenue': 215.0}, {'customer': 'The Lighting Corner', 'revenue': 202.0}, {'customer': 'St Louis Metro Electric', 'revenue': 202.0}, {'customer': 'The Factory', 'revenue': 194.0}, {'customer': 'Madison Lighting', 'revenue': 189.0}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 182.85}, {'customer': 'Chez-Del Interiors', 'revenue': 179.9}, {'customer': 'The Plywood Store, Inc. DBA Burlington Carpet One', 'revenue': 177.8}, {'customer': 'Deco Luminaire Terrebonne', 'revenue': 169.47}, {'customer': 'Multi-Luminaire (Laval)', 'revenue': 167.2}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 167.2}, {'customer': 'Prima Lighting Inc', 'revenue': 157.08}, {'customer': 'ZenSupply Inc', 'revenue': 152.65}, {'customer': 'Litecraft Lighting Inc', 'revenue': 152.0}, {'customer': "Coburn Supply Company dba Coburn's : Spring Hill Lighting db", 'revenue': 152.0}, {'customer': 'Gross Lighting & Home', 'revenue': 152.0}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': 152.0}, {'customer': 'Gross Lighting & Home : Indiana Lighting Center', 'revenue': 152.0}, {'customer': 'Home Front Design', 'revenue': 152.0}, {'customer': 'Radue Homes dba Inspired Spaces', 'revenue': 152.0}, {'customer': '!! Duncan Corporation dba Better Living', 'revenue': 148.0}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 133.33}, {'customer': 'Legend Lighting', 'revenue': 126.0}, {'customer': 'Illuminations, Inc. (NE)', 'revenue': 126.0}, {'customer': 'Lighting Plus (MS)', 'revenue': 126.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 126.0}, {'customer': 'Litehouse, Inc dba The Lite House Inc', 'revenue': 126.0}, {'customer': 'Anzalone Electric', 'revenue': 122.0}, {'customer': 'Southern Lighting (Chattanooga)', 'revenue': 122.0}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 122.0}, {'customer': 'Light Brite Distributing Inc.', 'revenue': 122.0}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 118.0}, {'customer': '!! Coastal Lighting Studio (SC)', 'revenue': 109.85}, {'customer': 'Pace Lighting Inc', 'revenue': 108.95}, {'customer': 'LIGHTING BY JARED', 'revenue': 107.86}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 90.1}, {'customer': 'Deco Luminaire Quebec', 'revenue': 83.6}, {'customer': 'Multi-Luminaire Gatineau', 'revenue': 83.6}, {'customer': 'ABC Creations, LLC', 'revenue': 82.5}, {'customer': 'Custom Lighting, Inc', 'revenue': 82.34}, {'customer': 'Just Lights', 'revenue': 81.39}, {'customer': 'Fogg Family Enterprises Inc', 'revenue': 77.95}, {'customer': 'Pine Tree Lighting dba Pine Tree Furniture', 'revenue': 76.0}, {'customer': 'Cregger Co LLC', 'revenue': 76.0}, {'customer': 'Fort Worth Lighting', 'revenue': 76.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 76.0}, {'customer': 'Be the Light Designs LLC', 'revenue': 76.0}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 76.0}, {'customer': 'Plank and Tile', 'revenue': 76.0}, {'customer': 'Logan Electric Company Inc', 'revenue': 76.0}, {'customer': 'Butler Lighting of High Point', 'revenue': 76.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 76.0}, {'customer': 'Elliott Electric Supply Inc', 'revenue': 73.24}, {'customer': 'Lighting South LLC', 'revenue': 69.3}, {'customer': 'Essence Lighting and Design', 'revenue': 69.3}, {'customer': 'Multi-Luminaire (Pointe Claire)', 'revenue': 69.3}, {'customer': 'Union Lighting (Montreal)', 'revenue': 69.3}, {'customer': 'Universal Lighting Corp (Ont)', 'revenue': 69.3}, {'customer': 'Townsquare Flooring and Design', 'revenue': 68.43}, {'customer': 'Beautiful Things, Inc', 'revenue': 63.34}, {'customer': 'Beals Lighting Gallery', 'revenue': 63.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 63.0}, {'customer': 'VP Supply', 'revenue': 63.0}, {'customer': 'Elite Lighting Innovations', 'revenue': 63.0}, {'customer': 'Wiseway Supply', 'revenue': 63.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 63.0}, {'customer': 'House of Lights of Sanford Inc', 'revenue': 63.0}, {'customer': 'BELAMI ECommerce', 'revenue': 63.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 63.0}, {'customer': 'Lighting Studio (NJ)', 'revenue': 63.0}, {'customer': 'Locke Supply', 'revenue': 63.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 61.0}, {'customer': 'BBC Lighting & Supply', 'revenue': 59.0}, {'customer': "Progressive Lighting, Inc. DBA Caroline's Interiors", 'revenue': 59.0}, {'customer': 'Bright City Lights', 'revenue': 59.0}, {'customer': 'Lighting EFX', 'revenue': 59.0}, {'customer': 'Ocean Pacific Lighting Inc', 'revenue': 58.91}, {'customer': 'Sunbelt / Louisiana', 'revenue': 56.7}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 51.66}, {'customer': 'Idlewood Electric Supply', 'revenue': 50.4}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 49.4}, {'customer': 'McLaren Electric', 'revenue': 38.72}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 37.76}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 19.18}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 8.5}, {'customer': 'Lightology', 'revenue': 0.0}, {'customer': 'Paramont- EO, Inc', 'revenue': -21.2}, {'customer': 'House of Carpets', 'revenue': -21.9}, {'customer': 'Chateau Lighting', 'revenue': -86.46}, {'customer': '!! Proper Goods Inc', 'revenue': -90.99}, {'customer': 'Galleria Lighting Inc.', 'revenue': -323.3}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': -716.1}, {'customer': 'City Lightz', 'revenue': -1247.4}] | [{'item': 'M60004NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 417}, {'item': 'M60054NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 292}, {'item': 'M60054MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 228}, {'item': 'M60011MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 208}, {'item': 'M60017ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 198}, {'item': 'M60068ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 194}, {'item': 'M60010ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 190}, {'item': 'M60017NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 185}, {'item': 'M60061MBK', 'desc': '4-Light Ceiling Light in Matte Black', 'available': 184}, {'item': 'M60074NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 183}, {'item': 'M60068PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 175}, {'item': 'M60056BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 173}, {'item': 'M60068NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 170}, {'item': 'M60074MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 165}, {'item': 'M60011ORBNB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze with Natural Brass', 'available': 164}, {'item': 'M60069ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 164}, {'item': 'M60055ORB', 'desc': '3-Light Convertible Semi-Flush or Pendant in Oil Rubbed Bronze', 'available': 164}, {'item': 'M60016MBK', 'desc': '2-Light Ceiling Light in Matte Black', 'available': 157}, {'item': 'M60056NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 155}, {'item': 'M60015NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 139}, {'item': 'M60070ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 123}, {'item': 'M60071MBKNB', 'desc': '1-Light Ceiling Light in Matte Black with Natural Brass', 'available': 121}, {'item': 'M60061NB', 'desc': '4-Light Ceiling Light in Natural Brass', 'available': 120}, {'item': 'M60018NB', 'desc': '3-Light Ceiling Light in Natural Brass', 'available': 118}, {'item': 'M60055NB', 'desc': '3-Light Convertible Semi-Flush or Pendant in Natural Brass', 'available': 117}, {'item': 'M60028DW', 'desc': '2-Light Ceiling Light in Distressed Wood', 'available': 115}, {'item': 'M60008ORB', 'desc': '2-Light Ceiling Light in Oil Rubbed Bronze', 'available': 113}, {'item': 'M60017PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 110}, {'item': 'M60061BN', 'desc': '4-Light Ceiling Light in Brushed Nickel', 'available': 104}, {'item': 'M60069NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 104}, {'item': 'M60017MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 91}, {'item': 'M60076NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 88}, {'item': 'M60061PN', 'desc': '4-Light Ceiling Light in Polished Nickel', 'available': 88}, {'item': 'M60080NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 87}, {'item': 'M60077MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 82}, {'item': 'M60064PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 80}, {'item': 'M60016NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 80}, {'item': 'M60011BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 80}, {'item': 'M60076MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 76}, {'item': 'M60016ORB', 'desc': '2-Light Ceiling Light in Oil Rubbed Bronze', 'available': 76}, {'item': 'M60070PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 76}, {'item': 'M60017BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 68}, {'item': 'M60010NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 65}, {'item': 'M60021NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 64}, {'item': 'M60078MBKNB', 'desc': '1-Light Ceiling Light in Matte Black and Natural Brass', 'available': 63}, {'item': 'M60055PN', 'desc': '3-Light Convertible Semi-Flush or Pendant in Polished Nickel', 'available': 63}, {'item': 'M60008MBK', 'desc': '2-Light Ceiling Light in Matte Black', 'available': 61}, {'item': 'M60038OG', 'desc': '3-Light Ceiling Light in Antique Gold', 'available': 57}, {'item': 'M60079MBKNB', 'desc': '3-Light Ceiling Light in Matte Black with Natural Brass', 'available': 57}, {'item': 'M60071NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 56}, {'item': 'M60076BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 54}, {'item': 'M60077NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 50}, {'item': 'M60077BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 50}, {'item': 'M60010MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 48}, {'item': 'M60056ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 42}, {'item': 'M60072MBKNB', 'desc': '3-Light Ceiling Light in Matte Black and Natural Brass', 'available': 37}, {'item': 'M60011NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 37}, {'item': 'M60008BN', 'desc': '2-Light Ceiling Light in Brushed Nickel', 'available': 36}, {'item': 'M60010BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 32}, {'item': 'M60020NB', 'desc': '3-Light Ceiling Light in Natural Brass', 'available': 31}, {'item': 'M60054CH', 'desc': '1-Light Ceiling Light in Chrome', 'available': 28}, {'item': 'M60020CBZ', 'desc': '3-Light Ceiling Light in Classic Bronze', 'available': 28}, {'item': 'M60055MBK', 'desc': '3-Light Convertible Semi-Flush or Pendant in Matte Black', 'available': 26}, {'item': 'M60015PN', 'desc': '2-Light Ceiling Light in Polished Nickel', 'available': 22}, {'item': 'M60078WHNB', 'desc': '1-Light Ceiling Light in White and Natural Brass', 'available': 21}, {'item': 'M60015ORB', 'desc': '2-Light Ceiling Light in Oil Rubbed Bronze', 'available': 15}, {'item': 'M60070NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 14}, {'item': 'M60072WHNB', 'desc': '3-Light Ceiling Light in White and Natural Brass', 'available': 10}, {'item': 'M60002-97', 'desc': '3-Light Ceiling Light in Natural Wood with Rope', 'available': 8}] |
| 9-7144-1-322 | Monroe 1-Light Wall Sconce in Warm Brass | MONRO | 162,680.72 | 2,784 | — | 2026-06-27 | [{'customer': 'WAYFAIR LLC', 'revenue': 79500.33}, {'customer': 'LAMPS PLUS INC', 'revenue': 6747.17}, {'customer': 'BUILD.COM', 'revenue': 5788.63}, {'customer': 'FERGUSON', 'revenue': 5171.54}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 4955.5}, {'customer': 'The Home Depot', 'revenue': 4659.83}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 4186.5}, {'customer': 'Shades of Light', 'revenue': 3851.0}, {'customer': 'Inline Electric Supply', 'revenue': 3030.0}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 1868.3}, {'customer': 'Lighting World', 'revenue': 1775.73}, {'customer': 'Multi-Luminaire Gatineau : Multi-Luminaire (Ottawa)', 'revenue': 1754.5}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 1613.65}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 1430.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 1374.64}, {'customer': 'Aggieland Lighting', 'revenue': 1281.75}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 1248.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 1201.76}, {'customer': 'Lamps.com, Inc', 'revenue': 1170.47}, {'customer': 'LIGHTING BY JARED', 'revenue': 1168.84}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 1098.73}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 1083.03}, {'customer': 'BELAMI ECommerce', 'revenue': 981.79}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 816.0}, {'customer': 'Lighting Design Company', 'revenue': 785.7}, {'customer': 'American Lighting Inc', 'revenue': 770.0}, {'customer': 'Sunbelt / Louisiana', 'revenue': 714.4}, {'customer': 'Lightology', 'revenue': 707.44}, {'customer': 'Lifestyles Store Inc', 'revenue': 707.27}, {'customer': 'Lighting Superstore', 'revenue': 702.93}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 659.5}, {'customer': 'Fusion Light and Design', 'revenue': 587.5}, {'customer': 'Rite Rug DBA Capital Lighting', 'revenue': 552.0}, {'customer': 'Lampworks dba Lamp & Shadework', 'revenue': 552.0}, {'customer': 'Lighting Incorporated', 'revenue': 550.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 542.0}, {'customer': 'Cape Electrical Supply', 'revenue': 540.96}, {'customer': 'Capitol Lighting Gallery', 'revenue': 536.0}, {'customer': 'Gateway Lighting & Design Inc', 'revenue': 472.61}, {'customer': 'Menards, Inc', 'revenue': 471.2}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 440.0}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 440.0}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 440.0}, {'customer': "Hinkley's Lighting Factory", 'revenue': 420.2}, {'customer': 'The Lighting Studio of 30A (Santa Rosa Beach)', 'revenue': 419.8}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 404.8}, {'customer': 'Union Lighting & Furnishings (Toronto)', 'revenue': 397.71}, {'customer': 'Wilson 6 Enterprises Inc. DBA: Mountain Lighting & Design', 'revenue': 396.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 385.6}, {'customer': 'Wiseway Supply', 'revenue': 385.0}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 385.0}, {'customer': 'Elaine Everetts Lighting', 'revenue': 368.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 368.0}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 339.68}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (PARAMUS)', 'revenue': 303.0}, {'customer': 'The Light Source', 'revenue': 276.0}, {'customer': 'City Lights (San Francisco)', 'revenue': 276.0}, {'customer': 'Lights Unlimited', 'revenue': 264.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 261.0}, {'customer': 'King Electric Company Inc', 'revenue': 244.7}, {'customer': 'Valley Supply Co', 'revenue': 237.89}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 231.0}, {'customer': 'Flinz Holdings LLC', 'revenue': 230.0}, {'customer': 'Illuminations, Inc. (NE)', 'revenue': 220.0}, {'customer': 'Sonepar dba Capital Electric', 'revenue': 220.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 220.0}, {'customer': 'Coley Electric & Plumbing (Douglas)', 'revenue': 220.0}, {'customer': 'Central Plumbing & Electric', 'revenue': 220.0}, {'customer': 'James Ashjian Lighting', 'revenue': 220.0}, {'customer': 'Muska Lighting', 'revenue': 220.0}, {'customer': 'Chester Lighting', 'revenue': 220.0}, {'customer': 'Sweet Home Design Company', 'revenue': 220.0}, {'customer': 'IBS Lighting LLC', 'revenue': 220.0}, {'customer': 'Kansas Lighting', 'revenue': 220.0}, {'customer': 'Front Street Lighting', 'revenue': 206.4}, {'customer': 'Hye Lighting Co', 'revenue': 198.0}, {'customer': 'Guildwood', 'revenue': 191.4}, {'customer': 'Union Lighting (Montreal)', 'revenue': 191.4}, {'customer': 'J.D. Lighting', 'revenue': 191.4}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 184.0}, {'customer': 'SOUTHWEST PLUMBING SUPPLY', 'revenue': 184.0}, {'customer': 'Kendall Electric Inc', 'revenue': 184.0}, {'customer': 'Hill Country Lighting Center', 'revenue': 184.0}, {'customer': 'Lights of Oconee', 'revenue': 184.0}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 184.0}, {'customer': 'Drew Designs, LLC dba Western Montana Lighting', 'revenue': 184.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 176.64}, {'customer': 'First Coast Lighting & Fans', 'revenue': 174.0}, {'customer': 'United Electric Supply (NE)', 'revenue': 174.0}, {'customer': 'Illuminate Lighting', 'revenue': 174.0}, {'customer': 'Beautiful Things, Inc', 'revenue': 170.4}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 156.4}, {'customer': 'Idlewood Electric Supply', 'revenue': 154.0}, {'customer': 'Pace Lighting Inc', 'revenue': 146.45}, {'customer': '!! Lando Lighting', 'revenue': 145.2}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 139.82}, {'customer': '!! Source & Co.', 'revenue': 139.52}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (STUART)', 'revenue': 138.0}, {'customer': 'Home & Light Valdosta', 'revenue': 123.3}, {'customer': 'Southern Electric & Plumbing Supply', 'revenue': 122.11}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 101.2}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 92.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 87.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 87.0}, {'customer': 'Beals Lighting Gallery', 'revenue': 74.5}, {'customer': 'The Brecher Co, Inc', 'revenue': 36.9}, {'customer': "LOWE'S", 'revenue': 0.0}, {'customer': 'Electric Outlet (LIGHTING BY FRAN)', 'revenue': 0.0}, {'customer': 'Small Town Home Decor LLC', 'revenue': 0.0}, {'customer': 'Mahlanders, Inc', 'revenue': 0.0}, {'customer': 'Dement Lighting', 'revenue': 0.0}, {'customer': 'Western Chandelier Co', 'revenue': -69.9}, {'customer': 'Stokes Electric Company', 'revenue': -71.0}] | [{'item': '9-302-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 144}, {'item': '9-303-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 139}, {'item': '9-7144-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 119}, {'item': '9-303-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 92}, {'item': '9-7144-1-44', 'desc': 'Monroe 1-Light Wall Sconce in Classic Bronze', 'available': 64}, {'item': '9-7144-1-109', 'desc': 'Monroe 1-Light Wall Sconce in Polished Nickel', 'available': 61}] |
| 7-2918-1-156 | Alta 1-Light Pendant in Concrete and Brass | ALTA | 147,450.18 | 537 | — | 2026-06-27 | [{'customer': 'FERGUSON', 'revenue': 12341.14}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 8575.49}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 8444.25}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 7733.0}, {'customer': 'BUILD.COM', 'revenue': 7081.8}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 5456.19}, {'customer': 'Lighting Design Company', 'revenue': 4511.3}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 3939.76}, {'customer': 'WAYFAIR LLC', 'revenue': 3824.25}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 3589.69}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 3198.61}, {'customer': 'Nebraska Furniture Mart, Inc', 'revenue': 3174.1}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2739.9}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 2606.45}, {'customer': 'Lighting Incorporated', 'revenue': 2387.5}, {'customer': '!! The Lifestyled Company LLC', 'revenue': 2360.73}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 2321.4}, {'customer': 'LIGHTING BY JARED', 'revenue': 2262.92}, {'customer': 'Fort Worth Lighting', 'revenue': 2224.6}, {'customer': 'Inline Electric Supply', 'revenue': 2000.5}, {'customer': "Wilkinson's House of Lighting", 'revenue': 1855.9}, {'customer': 'Lighting World', 'revenue': 1790.82}, {'customer': 'Small Town Home Decor LLC', 'revenue': 1718.0}, {'customer': 'Sunbelt / Louisiana', 'revenue': 1694.6}, {'customer': 'Lumen Nation LLC', 'revenue': 1628.0}, {'customer': 'Lifestyles Store Inc', 'revenue': 1536.18}, {'customer': '!! Gagnun Interior Concept Studio Inc DBA Boutique Intempore', 'revenue': 1471.91}, {'customer': 'The Lighting Corner', 'revenue': 1447.0}, {'customer': 'Hagens Lighting', 'revenue': 1390.5}, {'customer': 'The Brecher Co, Inc', 'revenue': 1281.3}, {'customer': 'Illuminations', 'revenue': 1254.7}, {'customer': 'Lightology', 'revenue': 1204.72}, {'customer': 'Passion Lighting DBA Cannon & Crossbow', 'revenue': 1186.5}, {'customer': 'Hall Electric Co Inc', 'revenue': 1153.0}, {'customer': 'Village 1, LLC dba Village Home Stores', 'revenue': 1153.0}, {'customer': 'Union Lighting (Montreal)', 'revenue': 1119.25}, {'customer': "Garbe's Lighting & Hardware LLC", 'revenue': 1085.0}, {'customer': 'BELAMI ECommerce', 'revenue': 1059.37}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 983.5}, {'customer': 'LAMPS PLUS INC', 'revenue': 977.29}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 973.67}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 917.4}, {'customer': 'Muskoka Lighting & Electric', 'revenue': 895.4}, {'customer': 'Urban Rustic Living', 'revenue': 895.4}, {'customer': 'Team Electric Supply, LLC', 'revenue': 847.5}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 814.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 814.0}, {'customer': 'WASATCH LIGHTING INC', 'revenue': 814.0}, {'customer': 'Uncommon Living fka Lighting Unlimited (MS)', 'revenue': 814.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 814.0}, {'customer': 'LIGHTSHINE INC DBA URBAN LIGHTS', 'revenue': 814.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 814.0}, {'customer': 'Kendall Electric Inc', 'revenue': 814.0}, {'customer': 'Aggieland Lighting', 'revenue': 802.25}, {'customer': 'The Light House Gallery (MO)', 'revenue': 773.3}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 746.0}, {'customer': 'Gorman Brothers Appliance', 'revenue': 746.0}, {'customer': '!! Simply Floors and Lights dba Fielden Ventures LLC', 'revenue': 745.8}, {'customer': 'Janbar Electric Ltd', 'revenue': 745.8}, {'customer': 'Muska Lighting', 'revenue': 678.0}, {'customer': 'Home & Light Valdosta', 'revenue': 678.0}, {'customer': 'The Finishing Touch', 'revenue': 678.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 678.0}, {'customer': 'Elan Studio Lighting', 'revenue': 678.0}, {'customer': 'Hudson Parc Lighting & Design', 'revenue': 634.13}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 621.61}, {'customer': 'Wiseway Supply', 'revenue': 576.5}, {'customer': 'TURN ON LIGHTING, INC.', 'revenue': 576.5}, {'customer': 'Royaume Luminaire', 'revenue': 563.2}, {'customer': 'J.D. Lighting', 'revenue': 447.7}, {'customer': 'Dhillon Lighting Inc (Edmonton) : Dhillon Lighting Manitoba', 'revenue': 447.7}, {'customer': 'JW Bird and Company Ltd DBA Bird Stairs', 'revenue': 447.7}, {'customer': '!! Lando Lighting', 'revenue': 447.7}, {'customer': '17-90 Lighting dba Illuminate Maine', 'revenue': 407.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Owensboro KY', 'revenue': 407.0}, {'customer': 'BIGGINS LIGHTING', 'revenue': 407.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba All Phase Tra', 'revenue': 407.0}, {'customer': 'Sun Lighting (Tempe)', 'revenue': 407.0}, {'customer': 'Lighting South LLC', 'revenue': 407.0}, {'customer': 'IMAGINE MORE SERVICE CORP.', 'revenue': 407.0}, {'customer': 'IBS Lighting LLC', 'revenue': 407.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 407.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 407.0}, {'customer': 'Fusion Light and Design', 'revenue': 407.0}, {'customer': 'Cleveland Lighting Center', 'revenue': 407.0}, {'customer': 'Lighting EFX', 'revenue': 378.51}, {'customer': 'Dement Lighting', 'revenue': 376.6}, {'customer': 'Maple Ridge Lighting Inc', 'revenue': 372.9}, {'customer': 'Essence Lighting and Design', 'revenue': 372.9}, {'customer': 'Idlewood Electric Supply', 'revenue': 366.3}, {'customer': 'First Coast Lighting & Fans', 'revenue': 366.3}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 345.95}, {'customer': 'Hill Country Lighting Center', 'revenue': 339.0}, {'customer': 'Showcase Lighting by 3-G LTD (TX)', 'revenue': 339.0}, {'customer': 'Lights of Oconee', 'revenue': 339.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 339.0}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 339.0}, {'customer': 'N S Electric Supply', 'revenue': 339.0}, {'customer': 'Royaume Luminaire Sherbrooke', 'revenue': 326.7}, {'customer': 'Lighting Reflects Design', 'revenue': 309.24}, {'customer': 'The Home Depot', 'revenue': 297.8}, {'customer': 'Deco Luminaire Brossard Dix 30', 'revenue': 261.25}, {'customer': 'Pine Lighting', 'revenue': 255.42}, {'customer': 'Young & Co', 'revenue': 254.25}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 244.24}, {'customer': 'Nestie Inc. fka Grand Lighting (CAN)', 'revenue': 223.85}, {'customer': 'Luminous Trends Inc DBA Modern Luxury by LT', 'revenue': 203.5}, {'customer': 'Royaume Luminaire-J.D. Inc', 'revenue': 186.45}, {'customer': 'Plank and Tile', 'revenue': 169.5}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba All Phase Pet', 'revenue': 169.5}, {'customer': 'KIE SUPPLY INC', 'revenue': 169.5}, {'customer': 'Lighting World Inc (Omaha)', 'revenue': 166.2}, {'customer': 'Mainland Lighting Warehouse', 'revenue': 140.8}, {'customer': 'James Ashjian Lighting', 'revenue': 135.6}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 124.79}, {'customer': 'Sweet Home Design Company', 'revenue': 83.4}, {'customer': 'The Lamp and Lighthouse (TN)', 'revenue': 50.99}, {'customer': "Hinkley's Lighting Factory", 'revenue': 30.45}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 0.0}, {'customer': 'Net Retailers, LLC', 'revenue': 0.0}, {'customer': 'SOUTHWEST PLUMBING SUPPLY', 'revenue': 0.0}, {'customer': 'Feldman Brothers Electrical Supply Co.', 'revenue': 0.0}, {'customer': 'Southern Lights', 'revenue': 0.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 0.0}, {'customer': 'Winsupply Elizabethtown : Winsupply dba Bowling Green WLC 14', 'revenue': 0.0}, {'customer': 'Lighting Emporium Inc', 'revenue': 0.0}, {'customer': "LOWE'S", 'revenue': 0.0}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': 0.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 0.0}, {'customer': 'U.S.31 Supply Inc', 'revenue': 0.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': -81.4}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': -120.07}, {'customer': 'Lighting by Lavonne, LLC', 'revenue': -165.0}, {'customer': 'Lumenco Inc (CIMPEXCO)', 'revenue': -179.08}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': -210.0}, {'customer': 'Multi-Luminaire Gatineau', 'revenue': -223.3}, {'customer': 'Illuminate Lighting', 'revenue': -324.5}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': -366.4}, {'customer': 'The Broadway Showroom dba Bliss Lighting', 'revenue': -423.0}, {'customer': 'Mahlanders, Inc', 'revenue': -488.64}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': -544.5}, {'customer': 'The Focal Point SWLA LLC', 'revenue': -623.5}, {'customer': 'Lights Unlimited', 'revenue': -716.4}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA)', 'revenue': -1265.5}, {'customer': 'The Lighting Shoppe Inc.', 'revenue': -1636.8}] | — |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 28-FD-485-109 | Archer LED Fan D'Lier in Polished Nickel | ARCHE | 1 | 0 | — |
| 1-3606-5-89 | Bancroft 5-Light Chandelier in Matte Black | BANCR | 2 | 1,288.50 | — |
| 11-CD04RC-BK | Molly 1-Light Rechargeable Table Lamp in Black | CDUNREL | 0 | 0 | — |
| 11-CD04RC-LBL | Molly 1-Light Rechargeable Table Lamp in Light Blue | CDUNREL | 0 | 0 | — |
| 11-CD04RC-PK | Molly 1-Light Rechargeable Table Lamp in Pink | CDUNREL | 0 | 0 | — |
| 11-CD22RC | Conrad 1-Light Rechargeable Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD23RC-BK | Sally 1-Light Rechargeable Table Lamp in Black | CDUNREL | 0 | 0 | — |
| 11-CD23RC-BL | Sally 1-Light Rechargeable Table Lamp in Blue | CDUNREL | 0 | 0 | — |
| 11-CD24RC | Shelly 1-Light Rechargeable Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD25RC | Hazel 1-Light Rechargeable Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD26RC | Posey 1-Light Rechargeable Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD27 | Eleanor 1-Light Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD28 | Amelia 1-Light Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD29 | Penelope 1-Light Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD30 | Josephine 1-Light Table Lamp | CDUNREL | 0 | 0 | — |
| 11-CD31-BK | Albert 1-Light Table Lamp in Black | CDUNREL | 0 | 0 | — |
| 11-CD31-HB | Albert 1-Light Table Lamp in Honey Brown | CDUNREL | 0 | 0 | — |
| 11-CD32-BK | Max 1-Light Table Lamp in Black | CDUNREL | 0 | 0 | — |
| 11-CD32-HB | Max 1-Light Table Lamp in Honey Brown | CDUNREL | 0 | 0 | — |
| 11-CD33-HBBK | Oliver 1-Light Table Lamp in Honey Brown and Black | CDUNREL | 0 | 0 | — |
| 11-CD33-HBBR | Oliver 1-Light Table Lamp in Honey Brown and Brown | CDUNREL | 0 | 0 | — |
| 11-CD34-BL | Viola 1-Light Table Lamp in Blue | CDUNREL | 0 | 0 | — |
| 11-CD34-WH | Viola 1-Light Table Lamp in White | CDUNREL | 0 | 0 | — |
| 11-CD36 | Betty 1-Light Table Lamp | CDUNREL | 0 | 0 | — |
| 6-3364-4-11 | Coral 4-Light Semi-Flush in Chrome | CORAL | 2 | 383.76 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
