# Section 3 Context Bundle — Ratana International Ltd. (ril)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Ratana International Ltd. (ril, org_id=245)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=1738, portal_order_gmv=$17.2M |
| HAS_INVENTORY | True | inventory_count=1514 |
| HAS_SALES_DATA | True | sales_data_count=24377 |
| HAS_SALES_SECTION | True | qualifying_reps=13 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | ratana_ril |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | FAIL | erp_gmv=$17.2M > ecat_gmv=$17.6M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 13 | 13 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 71 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1256, Mixpanel total submit_order (Q-01): 1973 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=77.5%, ambiguous_rate=76.4%, showroom_event_share=11.9% |
| USER_GROUP_JOIN_RATE | 77% | 55 of 71 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 12% | showroom+admin share of matched events: 11.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Winnie Ng |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=43 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=612 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=447 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Ratana International Ltd.
- **Shortname**: ril
- **Org ID**: 245
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS

## Section Confidence

# Section Confidence Tiers — Ratana International Ltd. (ril, org_id=245)
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

# Signal Rank — Ratana International Ltd. (ril, org_id=245)
- **Run date**: 2026-06-17
- **Total signals fired**: 66 (P0: 47, P1: 13, P2: 6)
- **Org GMV**: $17.6M eCat LTM, $17.2M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $4.7M total business | P1 | §5 Team | 23.3 | $4,660,027 | 2.0 | 217,158,516 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — UM00705BLK/C/DSC co-purchase pattern across 45 customers | P0 | §2/§3 | 4.5 | $20,580,100 | 2.0 | 185,220,898 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $4.3M+ total business, zero eCat orders | P1 | §2 Accounts | 4.3 | $4,286,761 | 2.0 | 36,752,640 | POSITIVE |
| 4 | SIG-MOM-01 | Account Acceleration — Isidore Landscapes Inc. 3 consecutive QoQ acceleration quarters, $199,696 peak quarter (+867% QoQ) | P0 | §2 Accounts | 28.9 | $199,696 | 3.0 | 17,305,657 | POSITIVE |
| 5 | SIG-ANOMALY-03 | Competitive Displacement — Evercare Contract Furnishings Inc. total biz +202% but eCat -14% | P0 | §2 Accounts | 14.4 | $292,762 | 3.0 | 12,664,878 | RISK |
| 6 | SIG-DECAY-01 | Reorder Decay — Kimpton Hotel Monaco Seattle 56.5x normal gap (113d vs 2d avg) | P0 | §2 Accounts | 56.5 | $65,100 | 3.0 | 11,034,450 | RISK |
| 7 | SIG-DECAY-01 | Reorder Decay — The Interior Design Group Inc 13.1x normal gap (208d vs 15d avg) | P0 | §2 Accounts | 13.1 | $268,331 | 3.0 | 10,545,408 | RISK |
| 8 | SIG-ANOMALY-03 | Competitive Displacement — Cash Account (US$) total biz +167% but eCat -49% | P0 | §2 Accounts | 14.4 | $241,135 | 3.0 | 10,383,263 | RISK |
| 9 | SIG-MOM-01 | Account Acceleration — Patio Options 3 consecutive QoQ acceleration quarters, $116,057 peak quarter (+852% QoQ) | P0 | §2 Accounts | 28.4 | $116,057 | 3.0 | 9,889,244 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — Les Fabrication Dor-val Ltee 3 consecutive QoQ acceleration quarters, $220,484 peak quarter (+390% QoQ) | P0 | §2 Accounts | 13.0 | $220,484 | 3.0 | 8,601,084 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — FN54401ASG (Lucia Club Chair) $285,951 LTM, 0 available | P0 | §3 Product | 10.0 | $285,951 | 3.0 | 8,578,530 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — UM00705BLK/C (7.5' Fiberglass Umbrella,38mm 2 Poles W/) $281,054 LTM, 0 available | P0 | §3 Product | 10.0 | $281,054 | 3.0 | 8,431,620 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — FN63020BLK (Toscana Lounger) $269,492 LTM, 0 available | P0 | §3 Product | 10.0 | $269,492 | 3.0 | 8,084,760 | RISK |
| 14 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 48% of eCat GMV | P1 | §4 Commerce | 1.2 | $3,065,209 | 2.0 | 7,381,866 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — FN61385LAG (Poinciana Highback Chair) $215,990 LTM, 0 available | P0 | §3 Product | 10.0 | $215,990 | 3.0 | 6,479,700 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — UM00605-55 (Umbrella Base, Steel, Square, 120lbs) $209,535 LTM, 0 available | P0 | §3 Product | 10.0 | $209,535 | 3.0 | 6,286,050 | RISK |
| 17 | SIG-MOM-01 | Account Acceleration — Timmermans Landscaping 2 consecutive QoQ acceleration quarters, $116,895 peak quarter (+485% QoQ) | P0 | §2 Accounts | 16.2 | $116,895 | 3.0 | 5,669,425 | POSITIVE |
| 18 | SIG-ANOMALY-02 | Stock Out — CU54401 (Lucia Club Chair Cushion) $184,283 LTM, 0 available | P0 | §3 Product | 10.0 | $184,283 | 3.0 | 5,528,490 | RISK |
| 19 | SIG-ANOMALY-02 | Stock Out — CU55001 (Copacabana Club Chair Cushion) $178,063 LTM, 0 available | P0 | §3 Product | 10.0 | $178,063 | 3.0 | 5,341,890 | RISK |
| 20 | SIG-ANOMALY-02 | Stock Out — FN61788WTR (Biltmore Swivel Recliner) $174,052 LTM, 0 available | P0 | §3 Product | 10.0 | $174,052 | 3.0 | 5,221,560 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 26 | 1 | 0 | 27 | |
| §3 Product Intelligence | 20 | 0 | 0 | 20 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 2 | 0 | 2 | |
| §6 Platform Context | 0 | 9 | 6 | 15 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $4.7M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — UM00705BLK/C/DSC co-purchase pattern across 45 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $4.3M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Isidore Landscapes Inc. 3 consecutive QoQ acceleration quarters, $199,696 peak quarter (+867% QoQ)
5. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — Evercare Contract Furnishings Inc. total biz +202% but eCat -14%
6. **[RISK]** SIG-DECAY-01: Reorder Decay — Kimpton Hotel Monaco Seattle 56.5x normal gap (113d vs 2d avg)
7. **[RISK]** SIG-DECAY-01: Reorder Decay — The Interior Design Group Inc 13.1x normal gap (208d vs 15d avg)

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,529 | 27 | 0 | 98.20 |

### Q-37_results.md

# Q-37 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FN54401ASG | CAT3 | LUCIA | Lucia Club Chair | $285,951 | 518 | 0 | 11 | 9 | — |
| UM00705BLK/C | CAT32 | COL73 | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | $281,054 | 889 | 0 | 7 | 95 | — |
| FN63020BLK | CAT16 | COL110 | Toscana Lounger | $269,492 | 647 | 0 | 40 | 37 | — |
| FN61385LAG | CAT27 | COL82 | Poinciana Highback Chair | $215,990 | 314 | 0 | 43 | 47 | — |
| UM00605-55 | CAT32 | COL197 | Umbrella Base, Steel, Square, 120lbs | $209,535 | 407 | 0 | 30 | 21 | 2026-6-5 |
| CU54401 | CAT33 | COL203 | Lucia Club Chair Cushion | $184,283 | 957 | 0 | 0 | 77 | — |
| CU55001 | CAT33 | COL204 | Copacabana Club Chair Cushion | $178,063 | 772 | 0 | 2 | 83 | — |
| FN61788WTR | CAT22 | COL87 | Biltmore Swivel Recliner | $174,052 | 196 | 0 | 3 | 0 | — |
| UM01009BLK/C | CAT32 | COL73 | 10' Sq Cantilever Umbrella w/Canopy&Base | $169,959 | 149 | 0 | 0 | 13 | — |
| FN54420ASG | CAT16 | LUCIA | Lucia Lounger | $165,018 | 203 | 0 | 0 | 0 | — |
| FN57001ASG | CAT3 | COL61 | Element 5.0 Club Chair | $163,081 | 279 | 0 | 1 | 14 | — |
| FN65520BLK | CAT16 | COL145 | Avenue Lounger | $159,588 | 236 | 0 | 13 | 10 | 2026-6-30 |
| CU61301 | CAT33 | COL217 | Poinciana Club Chair Cushion | $152,554 | 637 | 0 | 0 | 8 | — |
| FN57003ASG | SOFA | COL61 | Element 5.0 2.5-seater Sofa | $135,573 | 135 | 0 | 2 | 0 | — |
| FN54403ASG | SOFA | LUCIA | Lucia Sofa | $132,614 | 131 | 0 | 7 | 4 | — |
| FN61790WTR-RUB | CAT10 | COL87 | Biltmore Swivel Gliding Club | $131,032 | 221 | 0 | 5 | 142 | 2026-6-16 |
| CU54403 | CAT33 | COL203 | Lucia Sofa Cushion | $127,402 | 248 | 0 | 0 | 26 | — |
| FN50063ASG | TABLE | COL43 | Limo 84inx42in Rect Dining Table W/uh | $125,576 | 180 | 0 | 7 | 11 | — |
| FN65520WHT | CAT16 | COL145 | Avenue Lounger | $124,576 | 185 | 0 | 0 | 7 | 2026-6-30 |
| UM00907BRZ/C | CAT32 | COL73 | 9' Alum W/fiberglass Ribs,pulley,2 Poles W/canopy | $121,687 | 333 | 0 | 0 | 31 | — |

### Q-38a_results.md

# Q-38a Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 479
- **Run date**: 2026-06-17


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
|  | — | — | — | 2025-12-1 | 429 | 14 |
|  | — | — | — | 2026-1-1 | 2,777 | 86 |
|  | — | — | — | 2026-2-1 | 3,467 | 96 |
|  | — | — | — | 2026-3-1 | 3,253 | 111 |
|  | — | — | — | 2026-4-1 | 9,020 | 223 |
|  | — | — | — | 2026-5-1 | 6,673 | 340 |
|  | — | — | — | 2026-6-1 | 5,128.50 | 377 |
| CAT/CT2025-2026 | — | — | — | 2026-1-1 | 95 | 5 |
| CAT/CT2025-2026 | — | — | — | 2026-3-1 | 1 | 1 |
| CAT/CT2025-2026 | — | — | — | 2026-4-1 | 1 | 1 |
| CAT/CT2025-2026 | — | — | — | 2026-5-1 | 2 | 2 |
| CAT/MN2025-2026 | — | — | — | 2026-2-1 | 20 | 1 |
| CAT/MN2025-2026 | — | — | — | 2026-3-1 | 83 | 2 |
| CAT/MN2025-2026 | — | — | — | 2026-5-1 | 68 | 2 |
| CAT/MN2025-2026 | — | — | — | 2026-6-1 | 144 | 2 |
| CAT/OD2025-2026 | — | — | — | 2026-1-1 | 16 | 2 |
| CAT/OD2025-2026 | — | — | — | 2026-3-1 | 1 | 1 |
| CAT/OD2025-2026 | — | — | — | 2026-5-1 | 1 | 1 |
| CAT/ODSUPP25-26 | — | — | — | 2026-1-1 | 1 | 1 |
| CAT/ODSUPP25-26 | — | — | — | 2026-3-1 | 1 | 1 |
| CAT/TER2021-2022 | — | — | — | 2026-4-1 | 1 | 1 |
| CU10516/3B | — | — | — | 2026-6-1 | 2 | 1 |
| CU10516/O | — | — | — | 2026-5-1 | 2 | 2 |
| CU10516/O | — | — | — | 2026-6-1 | 2 | 1 |
| CU12701 | — | — | — | 2026-1-1 | 75 | 1 |
| CU12701 | — | — | — | 2026-5-1 | 2 | 1 |
| CU12701 | — | — | — | 2026-6-1 | 16 | 7 |
| CU12702 | — | — | — | 2026-6-1 | 1 | 1 |
| CU15501/5A | — | — | — | 2026-5-1 | 4 | 2 |
| CU15501/5D | — | — | — | 2026-3-1 | 12 | 1 |
| CU15501/5D | — | — | — | 2026-5-1 | 2 | 1 |
| CU15501/5E | — | — | — | 2026-3-1 | 4 | 2 |
| CU15501/5E | — | — | — | 2026-5-1 | 1 | 1 |
| CU15501/5G | — | — | — | 2026-6-1 | 2 | 1 |
| CU15501/5G/SL | — | — | — | 2026-6-1 | 1 | 1 |
| CU15501/5G/SR | — | — | — | 2026-6-1 | 1 | 1 |
| CU15501/5N | — | — | — | 2026-6-1 | 2 | 1 |
| CU15501/O | — | — | — | 2026-3-1 | 1 | 1 |
| CU15501/O | — | — | — | 2026-6-1 | 4 | 2 |
| CU15501F/O | — | — | — | 2026-3-1 | 1 | 1 |
| CU15502/5D | — | — | — | 2026-5-1 | 2 | 1 |
| CU15502/5E | — | — | — | 2026-3-1 | 8 | 2 |
| CU15502/5E | — | — | — | 2026-4-1 | 6 | 1 |
| CU15502/5E | — | — | — | 2026-5-1 | 2 | 1 |
| CU15502/5N | — | — | — | 2026-6-1 | 2 | 1 |
| CU15502/O | — | — | — | 2026-3-1 | 1 | 1 |
| CU15502/O | — | — | — | 2026-6-1 | 1 | 1 |
| CU15502F/O | — | — | — | 2026-3-1 | 1 | 1 |
| CU15502G/OB | — | — | — | 2026-3-1 | 1 | 1 |
| CU15503/5A | — | — | — | 2026-5-1 | 2 | 2 |

*(Truncated: showing top 50 of 479 rows. Full data in cache file.)*

### Q-39_category_results.md

# Q-39-cat Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 35
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT33 | $6.4M | 39,248 | 290 | $22,190 |
| CAT3 | $3.7M | 6,952 | 49 | $75,914 |
| CAT2 | $3.6M | 17,835 | 71 | $50,853 |
| SOFA | $2.6M | 2,661 | 42 | $62,212 |
| CAT16 | $2.4M | 5,114 | 34 | $70,413 |
| CAT1 | $2.2M | 11,997 | 65 | $33,704 |
| CAT17 | $2.0M | 3,251 | 92 | $21,393 |
| TABLE | $1.8M | 2,897 | 66 | $26,656 |
| CAT25 | $1.3M | 2,073 | 23 | $55,277 |
| CAT32 | $1.1M | 2,849 | 19 | $59,826 |
| CAT4 | $833,102 | 1,094 | 24 | $34,713 |
| CAT20 | $794,519 | 2,219 | 36 | $22,070 |
| CAT14 | $792,796 | 3,156 | 35 | $22,651 |
| CAT6 | $765,835 | 3,498 | 39 | $19,637 |
| CAT11 | $715,811 | 3,306 | 87 | $8,228 |
| CAT10 | $686,217 | 1,126 | 12 | $57,185 |
| CAT5 | $629,943 | 1,803 | 50 | $12,599 |
| CAT22 | $611,998 | 682 | 10 | $61,200 |
| CAT12 | $525,876 | 2,595 | 66 | $7,968 |
| CAT13 | $414,173 | 1,690 | 23 | $18,008 |
| STOOL | $359,071 | 1,307 | 17 | $21,122 |
| CAT24 | $320,843 | 6,659 | 39 | $8,227 |
| CAT27 | $256,395 | 365 | 4 | $64,099 |
| CAT15 | $217,361 | 1,034 | 21 | $10,351 |
| CAT7 | $213,706 | 984 | 40 | $5,343 |
| CAT26 | $184,592 | 111 | 5 | $36,918 |
| BENCH | $139,020 | 273 | 9 | $15,447 |
| CAT9 | $79,619 | 198 | 6 | $13,270 |
| CAT19 | $60,970 | 113 | 11 | $5,543 |
| CAT21 | $53,187 | 59 | 1 | $53,187 |
| CAT8 | $48,795 | 41 | 1 | $48,795 |
| CAT18 | $47,686 | 79 | 10 | $4,769 |
| CAT28 | $31,250 | 143 | 4 | $7,812 |
| CAT29 | $13,160 | 284 | 34 | $387 |
| CAT30 | $7,868 | 208 | 2 | $3,934 |

### Q-39_collection_results.md

# Q-39-col Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| LUCIA | $2.1M | 4,674 | 47 | $43,806 |
| COL87 | $1.7M | 2,832 | 36 | $46,365 |
| COL61 | $1.5M | 2,633 | 43 | $34,514 |
| COL82 | $1.1M | 1,910 | 15 | $71,498 |
| COL142 | $937,718 | 1,563 | 25 | $37,509 |
| COL63 | $856,079 | 2,188 | 20 | $42,804 |
| COL76 | $852,765 | 1,462 | 15 | $56,851 |
| COL52 | $812,094 | 2,008 | 13 | $62,469 |
| COL73 | $771,235 | 1,684 | 12 | $64,270 |
| COL110 | $771,169 | 1,970 | 6 | $128,528 |
| COL203 | $713,694 | 4,507 | 19 | $37,563 |
| COL68 | $691,950 | 1,317 | 16 | $43,247 |
| DIVA | $687,383 | 2,006 | 16 | $42,961 |
| RIA | $669,895 | 3,807 | 9 | $74,433 |
| COL46 | $661,673 | 981 | 14 | $47,262 |
| COL208 | $651,815 | 2,590 | 13 | $50,140 |
| COL29 | $592,739 | 2,324 | 8 | $74,092 |
| COL191 | $586,929 | 1,103 | 16 | $36,683 |
| COL34 | $522,659 | 2,391 | 10 | $52,266 |
| COL75 | $521,548 | 1,071 | 32 | $16,298 |
| CUBO | $502,663 | 1,051 | 23 | $21,855 |
| COL85 | $478,598 | 950 | 11 | $43,509 |
| COL204 | $466,614 | 1,891 | 9 | $51,846 |
| COL217 | $464,266 | 1,968 | 13 | $35,713 |
| COL22 | $461,723 | 1,415 | 16 | $28,858 |

### Q-42_results.md

# Q-42 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-59_results.md

# Q-59 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ITEM | FN61790WTR-RUB | Biltmore Swivel Gliding Club | CAT10 | — | — | 28 | 4 | 660.97 | 18,507.16 | 122,837.72 | 24 |
| ITEM | UM01006SIL/C | 10'sq Cantilever Alum Umbrella,canopy&granite Base | CAT32 | — | — | 3 | 1 | 2,586.41 | 7,759.23 | 14,226.41 | 2 |
| ITEM | FN61720WTR-RUB | Biltmore Adjustable Lounger (W/wheels) | CAT16 | — | — | 12 | 1 | 552.06 | 6,624.72 | 36,613.38 | 9 |
| ITEM | FN61788WTR-RUB | Biltmore Swivel Recliner | CAT22 | — | — | 6 | 3 | 1,024 | 6,144 | 42,603.20 | 14 |
| ITEM | FN64912WTR-RUB | Cabo San Lucas Dining Arm Chair | CAT2 | — | — | 8 | 1 | 540.88 | 4,327.04 | 76,240.86 | 4 |
| ITEM | FN61705RUB | Biltmore End Table | CAT6 | — | — | 13 | 2 | 236.55 | 3,075.09 | 16,171.99 | 15 |
| ITEM | FN54402PRL | Lucia Love Seat | CAT4 | — | — | 4 | 1 | 636 | 2,544 | 9,698.69 | 3 |
| ITEM | FN61790PEW-OGY | Biltmore Swivel Gliding Club | CAT10 | — | — | 4 | 1 | 617.70 | 2,470.80 | 19,232.46 | 7 |
| ITEM | FN57001ASG | Element 5.0 Club Chair | CAT3 | — | — | 4 | 1 | 607.94 | 2,431.76 | 26,224.68 | 12 |
| ITEM | DSC | Tariff Prepaid | Uncategorized | — | — | 2,285.57 | 7 | 1 | 2,285.57 | 880,700.85 | 353 |
| ITEM | FN66301STN-DIV | Hamptons Club Chair | CAT3 | — | — | 4 | 1 | 527.13 | 2,108.52 | 49,727.50 | 10 |
| ITEM | FN57005CEM | Element 5.0 40in Sq C/t W/alum Top CEM, Base ASG | CAT5 | — | — | 4 | 1 | 498.62 | 1,994.48 | 13,348.80 | 5 |
| ITEM | FN23037 | Palm Harbor Deck Box W/wheels & Handle | CAT8 | — | — | 2 | 1 | 975.69 | 1,951.38 | 15,481.91 | 8 |
| ITEM | FN71290WTR | Coral Gables Swivel Gliding Club | CAT10 | — | — | 3 | 1 | 612.48 | 1,837.44 | 35,122.85 | 15 |
| ITEM | FN54403ASG | Lucia Sofa | SOFA | — | — | 2 | 1 | 843 | 1,686 | 25,020.36 | 10 |
| ITEM | FN71288WTR | Coral Gables Swivel Recliner | CAT22 | — | — | 2 | 1 | 761.11 | 1,522.22 | 66,430.44 | 17 |

### Q-61_results.md

(not present — file does not exist or is empty)

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FN54401ASG | Lucia Club Chair | LUCIA | 285,951 | 518 | 9 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 42560.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 22194.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 11466.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 11401.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 10033.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 9541.0}, {'customer': 'Northwest Trends', 'revenue': 8961.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 8779.0}, {'customer': 'Leap Hospitality', 'revenue': 8551.0}, {'customer': 'Furniture Solutions Group', 'revenue': 8551.0}, {'customer': 'Patio & Home Direct', 'revenue': 7526.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 7409.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 6841.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 6786.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 5497.0}, {'customer': 'Direct Supply Inc.', 'revenue': 4902.0}, {'customer': 'Atmosphere Commercial Interiors', 'revenue': 4560.0}, {'customer': 'Robson Design Group', 'revenue': 4560.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 4560.0}, {'customer': 'Keca International', 'revenue': 4498.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 4012.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 3998.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 3762.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 3675.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 3234.0}, {'customer': 'Net Retailers LLC', 'revenue': 3009.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 2940.0}, {'customer': 'Patio Productions', 'revenue': 2769.0}, {'customer': 'Garden Architecture & Design', 'revenue': 2646.0}, {'customer': 'Image Urbaine', 'revenue': 2646.0}, {'customer': 'DGA Interiors', 'revenue': 2508.0}, {'customer': 'Hue Design LLC', 'revenue': 2508.0}, {'customer': 'MOI Inc.', 'revenue': 2508.0}, {'customer': 'AJ Designs', 'revenue': 2508.0}, {'customer': 'Touchmark, LLC', 'revenue': 2508.0}, {'customer': 'B H Allen Building Centre', 'revenue': 2505.0}, {'customer': 'Source', 'revenue': 2280.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 2280.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 2117.0}, {'customer': 'Patio Comfort', 'revenue': 1676.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1633.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1588.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 1459.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 1322.0}, {'customer': 'Lawai Beach Resort', 'revenue': 1254.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 1176.0}, {'customer': 'GST Interiors, LLC', 'revenue': 1140.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 1140.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1140.0}, {'customer': 'Jori Interiors', 'revenue': 1140.0}, {'customer': 'Commonwealth Design Group', 'revenue': 1140.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 1140.0}, {'customer': 'Country Furniture', 'revenue': 1058.0}, {'customer': "Bishop's Casual Living", 'revenue': 1058.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 1058.0}, {'customer': "Today's Patio", 'revenue': 1003.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 1002.0}, {'customer': 'Ifurnish Co.', 'revenue': 912.0}, {'customer': 'Main Street Furniture', 'revenue': 912.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 882.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 882.0}, {'customer': 'Abacus Furniture', 'revenue': 882.0}, {'customer': 'Sunset Home and Patio', 'revenue': 775.0}, {'customer': 'FirstService Residential-Austin', 'revenue': 627.0}, {'customer': 'Coombs Furniture', 'revenue': 588.0}, {'customer': 'Piscine Hippocampe', 'revenue': 588.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 529.0}, {'customer': 'Real Patio Living Llc', 'revenue': 502.0}, {'customer': 'Industrial Revolution', 'revenue': 500.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 500.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 441.0}, {'customer': 'Morinville Home Hardware', 'revenue': 441.0}, {'customer': 'Christy Sports, LLC', 'revenue': 274.0}, {'customer': 'Pangaea Patio', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}] | [{'item': 'FN54411OGY', 'desc': 'Lucia Dining Side Chair', 'available': 94}, {'item': 'FN54411ASG', 'desc': 'Lucia Dining Side Chair', 'available': 89}, {'item': 'FN54441OGY', 'desc': 'Lucia Bar Chair', 'available': 44}, {'item': 'FN54412OGY', 'desc': 'Lucia Dining Arm Chair', 'available': 43}, {'item': 'FN54453ASG-V', 'desc': 'Lucia Curved Corner', 'available': 31}, {'item': 'FN54402OGY', 'desc': 'Lucia Love Seat', 'available': 30}, {'item': 'FN54440OGY', 'desc': 'Lucia Counter Chair', 'available': 30}, {'item': 'FN54458PRL', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 29}, {'item': 'FN54453OGY-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 28}, {'item': 'FN54453OGY-V', 'desc': 'Lucia Curved Corner', 'available': 25}, {'item': 'FN54453ASG-R', 'desc': 'Lucia Wedge Right Arm', 'available': 25}, {'item': 'FN54452OGY-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 25}, {'item': 'FN54452OGY-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 25}, {'item': 'FN54404PRL', 'desc': 'Lucia Coffee Table', 'available': 24}, {'item': 'FN54453ASG-L', 'desc': 'Lucia Wedge Left Arm', 'available': 22}, {'item': 'FN54404ASG', 'desc': 'Lucia Coffee Table', 'available': 17}, {'item': 'FN54420OGY', 'desc': 'Lucia Lounger', 'available': 15}, {'item': 'FN54452ASG-C', 'desc': 'Lucia Wedge Corner', 'available': 14}, {'item': 'FN54416OGY', 'desc': 'Lucia Ottoman', 'available': 14}, {'item': 'FN54403PRL', 'desc': 'Lucia Sofa', 'available': 13}, {'item': 'FN54452ASG-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 12}, {'item': 'FN54452ASG-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 12}, {'item': 'FN54416ASG', 'desc': 'Lucia Ottoman', 'available': 12}, {'item': 'FN54458ASG', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 11}, {'item': 'FN54405PEY-OGY', 'desc': 'Lucia Sintered Stone End Table (KD)', 'available': 10}, {'item': 'FN54457ASG', 'desc': 'Lucia Sectional 40in Round Coffee Table/ottoman', 'available': 8}, {'item': 'FN54453ASG-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 8}, {'item': 'FN54468PRL', 'desc': 'Lucia Swivel Rocker', 'available': 6}, {'item': 'FN54404PEY-OGY', 'desc': 'Lucia Sintered Stone Coffee Table (KD)', 'available': 6}, {'item': 'FN54468OGY', 'desc': 'Lucia Swivel Rocker', 'available': 4}, {'item': 'FN54441ASG', 'desc': 'Lucia Bar Chair', 'available': 4}, {'item': 'FN54440ASG', 'desc': 'Lucia Counter Chair', 'available': 4}, {'item': 'FN54412ASG', 'desc': 'Lucia Dining Arm Chair', 'available': 4}, {'item': 'FN54405PRL', 'desc': 'Lucia End Table', 'available': 2}, {'item': 'FN54405ASG', 'desc': 'Lucia End Table', 'available': 1}] |
| UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | COL73 | 281,054 | 889 | 95 | — | [{'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 21142.0}, {'customer': 'Hilton Supply MGM, LLC C/O The Gettys Group', 'revenue': 17662.0}, {'customer': 'Dalfen Sales Agency Inc', 'revenue': 14631.0}, {'customer': 'Carver & Associates', 'revenue': 11227.0}, {'customer': 'Hilton Supply Mgm. c/o HPD Hotel Procurement&Servi', 'revenue': 10036.0}, {'customer': 'Hilton Supply Management', 'revenue': 9100.0}, {'customer': 'Elite Contract Furniture Ltd', 'revenue': 8671.0}, {'customer': 'Dauntless Development', 'revenue': 8451.0}, {'customer': 'Hilton Supply Mgm LLC c/oInterMountain Renovations', 'revenue': 8420.0}, {'customer': 'Haylie Read Design, LLC', 'revenue': 7736.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 7605.0}, {'customer': "Les Plantes D'interieur Veronneau", 'revenue': 7239.0}, {'customer': 'Watermark Beach Resort', 'revenue': 5400.0}, {'customer': 'Adria International Inc', 'revenue': 5256.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 4753.0}, {'customer': 'The Vancouver Club', 'revenue': 4400.0}, {'customer': 'Synergy Design & Procurement LLC', 'revenue': 4125.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 4097.0}, {'customer': 'Evercare Contract Furnishings Inc.', 'revenue': 3673.0}, {'customer': 'Industrial Revolution', 'revenue': 3665.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 3430.0}, {'customer': 'Source', 'revenue': 3248.0}, {'customer': 'InnVest Hotels Limited', 'revenue': 3080.0}, {'customer': 'Fairmont Tremblant', 'revenue': 2695.0}, {'customer': 'Country Furniture', 'revenue': 2617.0}, {'customer': 'MBF Interior Design LLC', 'revenue': 2495.0}, {'customer': 'Redwood Construction', 'revenue': 2488.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 2448.0}, {'customer': 'The Interior Design Group Inc', 'revenue': 2400.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 2334.0}, {'customer': 'Walteriors Design LLC', 'revenue': 2183.0}, {'customer': 'Muse Design Inc', 'revenue': 2098.0}, {'customer': 'Broadmoor Golf Club', 'revenue': 1979.0}, {'customer': 'Northland Properties Corporation', 'revenue': 1955.0}, {'customer': 'The Westin Tampa Waterside', 'revenue': 1950.0}, {'customer': 'Keca International', 'revenue': 1904.0}, {'customer': 'His Chattanooga c/o The Stroud Group', 'revenue': 1871.0}, {'customer': 'Harbaugh Construction LLC', 'revenue': 1786.0}, {'customer': 'ACL Design Build Solutions', 'revenue': 1733.0}, {'customer': 'Pacific Arbour Seven Residences Ltd.', 'revenue': 1601.0}, {'customer': 'Bobby Design Inc.', 'revenue': 1600.0}, {'customer': 'FFE Solutions LLC', 'revenue': 1559.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 1559.0}, {'customer': 'GP Builders, Inc.', 'revenue': 1559.0}, {'customer': 'Summit Hotel Properties', 'revenue': 1555.0}, {'customer': 'Wawanesa Insurance', 'revenue': 1540.0}, {'customer': "Salty's Beach House", 'revenue': 1540.0}, {'customer': 'US Hospitality Group', 'revenue': 1503.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 1474.0}, {'customer': 'Zenn Investing', 'revenue': 1404.0}, {'customer': 'POI Business Interiors LP', 'revenue': 1280.0}, {'customer': 'GHG SB Goleta LLC c/o Project Dynamics Inc(agent)', 'revenue': 1247.0}, {'customer': 'Hampton Inn & Suites Hurricane WV', 'revenue': 1247.0}, {'customer': 'Hampton Inn & Suites Hemet CA', 'revenue': 1247.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 1247.0}, {'customer': 'National Hospitality Management', 'revenue': 1247.0}, {'customer': 'Hampton Inn Winston Salem NC c/o Carolina Hosp', 'revenue': 1247.0}, {'customer': 'Isidore Landscapes Inc.', 'revenue': 1155.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 1134.0}, {'customer': 'HI Cleveland II, LLC c/o The Stroud Group', 'revenue': 1134.0}, {'customer': 'Gatsby Apartments', 'revenue': 1131.0}, {'customer': 'Hilton Seattle Airport & Conference Center', 'revenue': 1053.0}, {'customer': 'Lux Hospitality & Senior Living', 'revenue': 1018.0}, {'customer': 'Marriott International, Inc.', 'revenue': 978.0}, {'customer': 'Image Business Interiors', 'revenue': 975.0}, {'customer': 'Carolina Hospitality Corp', 'revenue': 936.0}, {'customer': 'Carolina Hotel Investors Crabtree, LLC', 'revenue': 936.0}, {'customer': 'Opus Industries LLC', 'revenue': 936.0}, {'customer': 'Hampton Inn Suites-Roseburg OR c/o Dwelling(Agent)', 'revenue': 936.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 936.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 936.0}, {'customer': 'Property c/o Jerry Osborne & Asso, Inc.', 'revenue': 936.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 935.0}, {'customer': 'Metzger, Inc.', 'revenue': 851.0}, {'customer': '1000 100th Avenue L.P. (Lux Apartments)', 'revenue': 848.0}, {'customer': 'New Athens Creek', 'revenue': 800.0}, {'customer': 'Atmosphere Interiors', 'revenue': 770.0}, {'customer': 'AJ Designs', 'revenue': 672.0}, {'customer': 'Mckenzie Design LLC', 'revenue': 652.0}, {'customer': 'Sandman Signature Dallas Las Colinas Hotel &Suites', 'revenue': 652.0}, {'customer': 'Whistler & Blackcomb Mountain Resorts Ltd', 'revenue': 640.0}, {'customer': 'Schoolcraft Hospitality Llc', 'revenue': 624.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 624.0}, {'customer': 'Carbondale Hotels LLC', 'revenue': 624.0}, {'customer': 'ZMC Hotels, Llc', 'revenue': 624.0}, {'customer': 'Hampton Inn & Suites', 'revenue': 624.0}, {'customer': 'Brier Properties LLC', 'revenue': 624.0}, {'customer': 'Matteo Middletown Llc', 'revenue': 624.0}, {'customer': 'Olympia Equity Investors XIII, Llc c/o The Gettys', 'revenue': 624.0}, {'customer': 'M4 Orlando Llc c/o Beyer Brown (agent)', 'revenue': 624.0}, {'customer': 'Kernersville Hotels, LLC c/o Craver & Asso(agent)', 'revenue': 624.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 624.0}, {'customer': 'Western International c/o PMI L.P. (as agent)', 'revenue': 624.0}, {'customer': 'MHH Lenox 445 Operating, LLC C/O HPG International', 'revenue': 624.0}, {'customer': 'HC Kitsap, LLC', 'revenue': 624.0}, {'customer': 'Odyssey Propco VII, LLC c/o Aintree, LLC(agent)', 'revenue': 624.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 624.0}, {'customer': 'Spectrum Hospitality Management, LLC', 'revenue': 624.0}, {'customer': 'College Station Lodging Partners LP', 'revenue': 624.0}, {'customer': 'Furniture Solutions Group', 'revenue': 622.0}, {'customer': 'Spark Studio + Source LLC', 'revenue': 600.0}, {'customer': 'SAK Harbor LLC c/o Sourcing Advisors', 'revenue': 595.0}, {'customer': 'P&C Hotel LLC c/o ACC Design Inc(agent)', 'revenue': 567.0}, {'customer': 'D Hospitality Design LLC', 'revenue': 567.0}, {'customer': 'Town Creek Plaza', 'revenue': 567.0}, {'customer': 'AK Design Group, LLC', 'revenue': 567.0}, {'customer': 'Arveaux Interiors', 'revenue': 566.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 556.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 554.0}, {'customer': 'EPS7516 Bordeaux c/o Rancho Management', 'revenue': 385.0}, {'customer': 'Terra Verde', 'revenue': 340.0}, {'customer': 'Hampton Inn - Dyersburg, TN c/o Hersha Purchasing', 'revenue': 312.0}, {'customer': 'Champion Supply LLC', 'revenue': 312.0}, {'customer': 'Washington Hotels, LLC', 'revenue': 312.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 308.0}, {'customer': "Beck's Home & Heating", 'revenue': 308.0}, {'customer': 'Cash Account', 'revenue': 308.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 308.0}, {'customer': 'Snowhite Hospitality, LLC dba/Design Environments', 'revenue': 284.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 284.0}, {'customer': 'Laporte Hotel Suites, LLC dba/Hampton Inn', 'revenue': 284.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 284.0}, {'customer': 'FiveWest Interiors', 'revenue': 283.0}, {'customer': 'Club Piscines Sherbrooke', 'revenue': 160.0}, {'customer': 'ADS Hospitality LLC', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Hampton Inn & Suites Rocky Hill CT', 'revenue': 0.0}, {'customer': 'Northwest Trends', 'revenue': 0.0}, {'customer': 'Rama Tika Management LLC', 'revenue': 0.0}, {'customer': 'Curve Hospitality', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}, {'customer': 'Opportunity Lodging Three,LLC c/o Layman Hosp', 'revenue': 0.0}, {'customer': 'Era Living LLC', 'revenue': 0.0}, {'customer': 'Woodstock Hospitality Group', 'revenue': 0.0}, {'customer': 'Valiant Products Corportion', 'revenue': 0.0}, {'customer': 'Hampton Inn - Philadelphia Airport', 'revenue': 0.0}, {'customer': '3000 Vine LLC', 'revenue': 0.0}, {'customer': 'Home2 Suites Taylor', 'revenue': 0.0}, {'customer': "Anthony's Restaurants", 'revenue': 0.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 0.0}] | [{'item': 'UM01010SLV-CCL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Cloud canopy", 'available': 10}, {'item': 'UM01010SLV-CBL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Black canopy", 'available': 9}, {'item': 'UM01004SLV/C', 'desc': "10' Sq Deluxe Alum Umbrella, 48mm Pole W/canopy", 'available': 8}, {'item': 'UM00906BRZ/C', 'desc': "9' Alum W/fiber Ribs,crank Lift,collar Tilt,canopy", 'available': 6}, {'item': 'UM00909POLE-BRZ', 'desc': '45in Bar Bottom Pole for UM00906BRZ/C', 'available': 5}] |
| FN63020BLK | Toscana Lounger | COL110 | 269,492 | 647 | 37 | — | [{'customer': 'Studio Dwell', 'revenue': 26977.0}, {'customer': 'Haylie Read Design, LLC', 'revenue': 24902.0}, {'customer': 'Redwood Construction', 'revenue': 16435.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 14607.0}, {'customer': 'Carver & Associates', 'revenue': 12118.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 10559.0}, {'customer': 'Germain Lariviere (1970) Ltee.', 'revenue': 10295.0}, {'customer': 'Patio Options', 'revenue': 9131.0}, {'customer': 'Fairmont Tremblant', 'revenue': 7701.0}, {'customer': 'Sanctuary Home & Patio', 'revenue': 7668.0}, {'customer': 'Hilton Supply Management', 'revenue': 5935.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 5853.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 5633.0}, {'customer': "Hayward's Of Santa Barbara Inc.", 'revenue': 3851.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 3652.0}, {'customer': 'Zenn Investing', 'revenue': 3652.0}, {'customer': 'FFE Solutions LLC', 'revenue': 3652.0}, {'customer': 'GHG SB Goleta LLC c/o Project Dynamics Inc(agent)', 'revenue': 3652.0}, {'customer': 'Jennings Furniture & Design', 'revenue': 3520.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 3320.0}, {'customer': 'Bobby Design Inc.', 'revenue': 3300.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 3188.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2739.0}, {'customer': 'Opus Industries LLC', 'revenue': 2739.0}, {'customer': 'Hampton Inn & Suites Crawfordsville IN', 'revenue': 2739.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 2573.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 2490.0}, {'customer': 'D Hospitality Design LLC', 'revenue': 2490.0}, {'customer': 'Metzger, Inc.', 'revenue': 2490.0}, {'customer': 'Destiny Builders', 'revenue': 2490.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 2283.0}, {'customer': 'Northland Properties Corporation', 'revenue': 2200.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 2075.0}, {'customer': 'Southport Outdoor Living', 'revenue': 1980.0}, {'customer': 'Carbondale Hotels LLC', 'revenue': 1826.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 1826.0}, {'customer': 'R.R. Williams & Associates', 'revenue': 1826.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 1826.0}, {'customer': 'PSM Hospitality', 'revenue': 1826.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 1826.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 1826.0}, {'customer': 'Uniik Design Solutions', 'revenue': 1826.0}, {'customer': 'Oyen Flowers & Giftware', 'revenue': 1760.0}, {'customer': 'Meubles Duboise', 'revenue': 1672.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 1660.0}, {'customer': 'Magers Lodgings', 'revenue': 1660.0}, {'customer': 'Hospitality Designs', 'revenue': 1660.0}, {'customer': 'HCW', 'revenue': 1660.0}, {'customer': 'Lifestyles By Design, Llc.', 'revenue': 1660.0}, {'customer': 'Timmermans Landscaping', 'revenue': 1650.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1584.0}, {'customer': 'Garden Architecture & Design', 'revenue': 1489.0}, {'customer': 'Porch & Patio/casual Living', 'revenue': 1461.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 1408.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 1370.0}, {'customer': 'Muse Design Inc', 'revenue': 1370.0}, {'customer': 'Hampton Inn Bennington', 'revenue': 1370.0}, {'customer': 'Dunsire Asset Mgm USA Inc', 'revenue': 913.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 913.0}, {'customer': 'US Hospitality Group', 'revenue': 913.0}, {'customer': 'Mark Bombara Interior Design', 'revenue': 913.0}, {'customer': 'Meubles Poisson Ltée', 'revenue': 880.0}, {'customer': 'Robert Leduc', 'revenue': 880.0}, {'customer': 'Hotel Rehabs', 'revenue': 830.0}, {'customer': 'Billy Milner Design', 'revenue': 830.0}, {'customer': "S'tattic Design", 'revenue': 830.0}, {'customer': 'Country Furniture', 'revenue': 792.0}, {'customer': 'Decked Out Home & Patio', 'revenue': 792.0}, {'customer': 'OutBack Patio Furnishings', 'revenue': 621.0}, {'customer': 'Littman Bros Energy Supplies, Inc', 'revenue': 584.0}, {'customer': 'Entreprises H.P. Carignan Inc(mq034', 'revenue': 440.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 396.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 396.0}, {'customer': 'Club Piscines Sherbrooke', 'revenue': 220.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 219.0}, {'customer': 'Gooch Design Studio LLC', 'revenue': 199.0}, {'customer': 'Office Revolution LLC', 'revenue': 0.0}, {'customer': 'Elder And Ash, LLC', 'revenue': 0.0}, {'customer': 'Level 3 Design Group', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Polygon Interior Design Ltd.', 'revenue': 0.0}, {'customer': 'Hampton Inn & Suites Ada OK', 'revenue': 0.0}, {'customer': 'Hampton Inn & Suites Rocky Hill CT', 'revenue': 0.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 0.0}] | [{'item': 'FN63005BLK', 'desc': 'Toscana Side Table', 'available': 57}, {'item': 'FN63005GRY', 'desc': 'Toscana Side Table', 'available': 55}, {'item': 'FN63005WHT', 'desc': 'Toscana Side Table', 'available': 39}, {'item': 'FN63020GRY', 'desc': 'Toscana Lounger', 'available': 39}, {'item': 'FN63020WHT', 'desc': 'Toscana Lounger', 'available': 27}] |
| FN61385LAG | Poinciana Highback Chair | COL82 | 215,990 | 314 | 47 | — | [{'customer': 'Hilton Supply Management', 'revenue': 19272.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 17955.0}, {'customer': 'RLJ HS Seattle Lynnwood, LLC', 'revenue': 13300.0}, {'customer': 'Granite State Contract Furnishings', 'revenue': 9510.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 8778.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 8512.0}, {'customer': 'Creo Hospitality LLC', 'revenue': 8246.0}, {'customer': 'Christina River Exchange', 'revenue': 7229.0}, {'customer': 'Carver & Associates', 'revenue': 6916.0}, {'customer': 'PHG Jackson II, LLC c/o Carver & Asso (Atlanta)', 'revenue': 6650.0}, {'customer': 'Curve Hospitality', 'revenue': 5852.0}, {'customer': 'Studio Dwell', 'revenue': 5852.0}, {'customer': 'Homewood Suites By Hilton Covington', 'revenue': 5852.0}, {'customer': 'West Coast Lodging c/o Throughline by IIG (agent)', 'revenue': 5320.0}, {'customer': 'Country Furniture', 'revenue': 5299.0}, {'customer': 'Tharaldson Hospitality Development, LLC', 'revenue': 5121.0}, {'customer': 'Picerne Development Corp', 'revenue': 3990.0}, {'customer': 'Homewood Suites Orlando Airport', 'revenue': 3990.0}, {'customer': 'Renascent Hospitality', 'revenue': 3189.0}, {'customer': 'BPR Goldsboro, LLC c/o Carver and Asso(Atlanta)', 'revenue': 2926.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 2926.0}, {'customer': 'Farrell Flynne LLC', 'revenue': 2926.0}, {'customer': 'Sourcing Advisors LLC c/o Sourcing Advisor', 'revenue': 2926.0}, {'customer': 'LOF2 Tyler Golden TRS, LLC c/o DeBlauw Purchasing', 'revenue': 2926.0}, {'customer': 'Parks Hospitality Group', 'revenue': 2926.0}, {'customer': 'B&T Arizona Hotels III, LLC c/o PMI', 'revenue': 2926.0}, {'customer': 'Lajoie Purchasing Associates', 'revenue': 2926.0}, {'customer': 'MCR Allen Tenant, LLC c/o Onyx Contract SVC', 'revenue': 2926.0}, {'customer': 'Hospitality Depot', 'revenue': 2660.0}, {'customer': 'Larkin Family Properties Inc c/o Benjamin West', 'revenue': 2660.0}, {'customer': 'Marriott International, Inc.', 'revenue': 2660.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 2660.0}, {'customer': 'Buffalo-Alafaya Asso. LLC dba Homewood Suites', 'revenue': 2660.0}, {'customer': 'Dwellings, Llc', 'revenue': 2660.0}, {'customer': 'HSI Design Group', 'revenue': 2660.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2660.0}, {'customer': 'Eastwood Hospitality Group Llc', 'revenue': 1463.0}, {'customer': 'Zachary Park Hotel QOZB c/o Benjamin West(agent)', 'revenue': 1463.0}, {'customer': 'Lita Dirks & Co, Llc', 'revenue': 1463.0}, {'customer': 'Design and Construction, Llc c/o The Gettys Group', 'revenue': 1463.0}, {'customer': 'TPI Hospitality', 'revenue': 1463.0}, {'customer': 'Metzger, Inc.', 'revenue': 1463.0}, {'customer': 'Homewood Suites By Hilton Boston', 'revenue': 1463.0}, {'customer': 'IBee Design Studio LLC', 'revenue': 1330.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 1330.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1170.0}, {'customer': 'Jack Wills Companies', 'revenue': 1064.0}, {'customer': 'Studio 4d', 'revenue': 665.0}, {'customer': 'Can-Tario Brick & Stone', 'revenue': 626.0}, {'customer': 'Whitney Evans Ltd', 'revenue': 585.0}, {'customer': 'Creative Living', 'revenue': 532.0}, {'customer': 'Tru Contract Interiors', 'revenue': 0.0}, {'customer': 'Summit Hotel Properties', 'revenue': 0.0}, {'customer': 'Homewood Suites-Liverpool, NY c/o HPD(as agent)', 'revenue': 0.0}, {'customer': 'BPR Properties c/o Carver and Asso, Atlanta(agent)', 'revenue': 0.0}, {'customer': 'JSM Procurement LLC', 'revenue': 0.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 0.0}] | [{'item': 'FN61312LAG', 'desc': 'Poinciana Dining Arm Chair', 'available': 199}, {'item': 'FN61311LAG', 'desc': 'Poinciana Dining Side Chair', 'available': 160}, {'item': 'FN61353LAG-C', 'desc': 'Poinciana Chair (w/o Arm)', 'available': 72}, {'item': 'FN61352LAG-R', 'desc': 'Poinciana 2-Seater Right Arm', 'available': 57}, {'item': 'FN61353LAG-V', 'desc': 'Poinciana Curved Corner', 'available': 55}, {'item': 'FN61352LAG-L', 'desc': 'Poinciana 2-Seater Left Arm', 'available': 52}, {'item': 'FN61301LAG', 'desc': 'Poinciana Club Chair', 'available': 44}, {'item': 'FN61341LAG', 'desc': 'Poinciana Bar Chair', 'available': 23}, {'item': 'FN61368LAG', 'desc': 'Poinciana Swivel Rocker', 'available': 22}, {'item': 'FN61316ASG', 'desc': 'Poinciana Ottoman', 'available': 14}, {'item': 'FN61303LAG', 'desc': 'Poinciana Sofa', 'available': 14}, {'item': 'FN61304ASG', 'desc': 'Poinciana Coffee Table', 'available': 11}, {'item': 'FN61340LAG', 'desc': 'Poinciana Counter Chair', 'available': 10}, {'item': 'FN61305ASG', 'desc': 'Poinciana End Table', 'available': 5}] |
| UM00605-55 | Umbrella Base, Steel, Square, 120lbs | COL197 | 209,535 | 407 | 21 | 2026-6-5 | [{'customer': 'Hilton Supply MGM, LLC C/O The Gettys Group', 'revenue': 28435.0}, {'customer': 'Carver & Associates', 'revenue': 18025.0}, {'customer': 'Hilton Supply Mgm. c/o HPD Hotel Procurement&Servi', 'revenue': 13013.0}, {'customer': 'Hilton Supply Management', 'revenue': 11663.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 6992.0}, {'customer': 'Hilton Supply Mgm LLC c/oInterMountain Renovations', 'revenue': 6651.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 5832.0}, {'customer': 'Era Living LLC', 'revenue': 5049.0}, {'customer': 'Interior Solutions', 'revenue': 4488.0}, {'customer': 'Synergy Design & Procurement LLC', 'revenue': 4065.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 3968.0}, {'customer': 'Hampton Inn Phoenix/Anthem', 'revenue': 3856.0}, {'customer': 'Walteriors Design LLC', 'revenue': 3711.0}, {'customer': 'Muse Design Inc', 'revenue': 3566.0}, {'customer': 'PHG Ashburn LLC', 'revenue': 3181.0}, {'customer': 'His Chattanooga c/o The Stroud Group', 'revenue': 3181.0}, {'customer': 'Urban Design Studio', 'revenue': 3060.0}, {'customer': 'Harbaugh Construction LLC', 'revenue': 3036.0}, {'customer': 'FFE Solutions LLC', 'revenue': 2651.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2651.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 2651.0}, {'customer': 'US Hospitality Group', 'revenue': 2554.0}, {'customer': 'Bobby Design Inc.', 'revenue': 2520.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 2506.0}, {'customer': 'GHG SB Goleta LLC c/o Project Dynamics Inc(agent)', 'revenue': 2121.0}, {'customer': 'National Hospitality Management', 'revenue': 2121.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 2121.0}, {'customer': 'Hampton Inn Winston Salem NC c/o Carolina Hosp', 'revenue': 2121.0}, {'customer': "Leadon (St. John's) Operations LP", 'revenue': 2016.0}, {'customer': 'HI Cleveland II, LLC c/o The Stroud Group', 'revenue': 1928.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 1928.0}, {'customer': 'The Vancouver Club', 'revenue': 1890.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1683.0}, {'customer': 'Hampton Inn Suites-Roseburg OR c/o Dwelling(Agent)', 'revenue': 1590.0}, {'customer': 'Opus Industries LLC', 'revenue': 1590.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 1590.0}, {'customer': 'Hampton Inn & Suites Hurricane WV', 'revenue': 1590.0}, {'customer': 'Property c/o Jerry Osborne & Asso, Inc.', 'revenue': 1590.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 1590.0}, {'customer': 'Carolina Hospitality Corp', 'revenue': 1590.0}, {'customer': 'Metzger, Inc.', 'revenue': 1446.0}, {'customer': 'Atmosphere Interiors', 'revenue': 1260.0}, {'customer': 'College Station Lodging Partners LP', 'revenue': 1060.0}, {'customer': 'Hampton Inn & Suites', 'revenue': 1060.0}, {'customer': 'Brier Properties LLC', 'revenue': 1060.0}, {'customer': 'Matteo Middletown Llc', 'revenue': 1060.0}, {'customer': 'ZMC Hotels, Llc', 'revenue': 1060.0}, {'customer': 'M4 Orlando Llc c/o Beyer Brown (agent)', 'revenue': 1060.0}, {'customer': 'Town Creek Plaza', 'revenue': 1060.0}, {'customer': 'Olympia Equity Investors XIII, Llc c/o The Gettys', 'revenue': 1060.0}, {'customer': 'Kernersville Hotels, LLC c/o Craver & Asso(agent)', 'revenue': 1060.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 1060.0}, {'customer': 'AK Design Group, LLC', 'revenue': 1060.0}, {'customer': 'MHH Lenox 445 Operating, LLC C/O HPG International', 'revenue': 1060.0}, {'customer': 'Odyssey Propco VII, LLC c/o Aintree, LLC(agent)', 'revenue': 1060.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 1060.0}, {'customer': 'HC Kitsap, LLC', 'revenue': 1060.0}, {'customer': 'Spectrum Hospitality Management, LLC', 'revenue': 1060.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 1060.0}, {'customer': 'Schoolcraft Hospitality Llc', 'revenue': 1060.0}, {'customer': 'Carbondale Hotels LLC', 'revenue': 1060.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 1020.0}, {'customer': 'Dauntless Development', 'revenue': 1020.0}, {'customer': 'D Hospitality Design LLC', 'revenue': 964.0}, {'customer': 'P&C Hotel LLC c/o ACC Design Inc(agent)', 'revenue': 964.0}, {'customer': 'Spark Studio + Source LLC', 'revenue': 964.0}, {'customer': 'Insideout Home & Patio (Burlington)', 'revenue': 807.0}, {'customer': 'Hampton Inn - Dyersburg, TN c/o Hersha Purchasing', 'revenue': 530.0}, {'customer': 'Washington Hotels, LLC', 'revenue': 530.0}, {'customer': 'Laporte Hotel Suites, LLC dba/Hampton Inn', 'revenue': 530.0}, {'customer': 'Champion Supply LLC', 'revenue': 530.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 482.0}, {'customer': 'SAK Harbor LLC c/o Sourcing Advisors', 'revenue': 482.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 482.0}, {'customer': 'Snowhite Hospitality, LLC dba/Design Environments', 'revenue': 482.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 269.0}, {'customer': 'Dynamik Interiors', 'revenue': 269.0}, {'customer': 'Opportunity Lodging Three,LLC c/o Layman Hosp', 'revenue': 0.0}, {'customer': 'Valiant Products Corportion', 'revenue': 0.0}, {'customer': 'Woodstock Hospitality Group', 'revenue': 0.0}, {'customer': 'Northwest Trends', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 0.0}, {'customer': 'Rama Tika Management LLC', 'revenue': 0.0}, {'customer': 'Hampton Inn - Philadelphia Airport', 'revenue': 0.0}, {'customer': 'ADS Hospitality LLC', 'revenue': 0.0}, {'customer': 'Curve Hospitality', 'revenue': 0.0}] | [{'item': 'UM00606BRZ', 'desc': 'Umbrella Base W Dual Purpose Stem, Cast Iron,50lbs', 'available': 56}, {'item': 'UM00606ADD-ON', 'desc': 'Umbrella Base Add-on Weight, Cast Iron, 30lbs', 'available': 32}, {'item': 'UM00609BLK', 'desc': 'Umbrella Base w/Casters, Steel, 120lbs', 'available': 16}, {'item': 'UM00605-32', 'desc': 'Umbrella Base W Dual Purpose Stem, Steel, 70lbs', 'available': 13}, {'item': 'UM00610SGR', 'desc': 'Base for UM01010, Galvan. Steel w/ Lid, 415lbs', 'available': 9}, {'item': 'UM00612', 'desc': 'In-Ground Mount Kit for UM01010', 'available': 5}, {'item': 'UM00611', 'desc': 'Concrete Mount Kit for UM01010', 'available': 4}] |
| CU54401 | Lucia Club Chair Cushion | COL203 | 184,283 | 957 | 77 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 16892.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 8091.0}, {'customer': 'City of Yorba Linda', 'revenue': 7549.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 7350.0}, {'customer': 'Wegman Design Group', 'revenue': 6935.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 5455.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 5267.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 5100.0}, {'customer': 'Lanai Resorts LLC dba Pulama Lanai', 'revenue': 5100.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 4900.0}, {'customer': 'IDM Development, LLC', 'revenue': 4480.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 4440.0}, {'customer': 'Northwest Trends', 'revenue': 3900.0}, {'customer': 'Leap Hospitality', 'revenue': 3825.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 3593.0}, {'customer': 'Furniture Solutions Group', 'revenue': 3526.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 3368.0}, {'customer': 'Country Furniture', 'revenue': 3125.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 2851.0}, {'customer': 'Keca International', 'revenue': 2634.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 2619.0}, {'customer': 'Patio & Home Direct', 'revenue': 2608.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 2520.0}, {'customer': 'Bobby Design Inc.', 'revenue': 2384.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 2360.0}, {'customer': 'DGA Interiors', 'revenue': 2259.0}, {'customer': 'Touchmark, LLC', 'revenue': 2157.0}, {'customer': 'Direct Supply Inc.', 'revenue': 1940.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 1913.0}, {'customer': 'Atmosphere Commercial Interiors', 'revenue': 1840.0}, {'customer': 'Christy Sports, LLC', 'revenue': 1754.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1679.0}, {'customer': '1000 100th Avenue L.P. (Lux Apartments)', 'revenue': 1610.0}, {'customer': 'AJ Designs', 'revenue': 1598.0}, {'customer': 'The Childs Dreyfus Group', 'revenue': 1557.0}, {'customer': 'Real Patio Living Llc', 'revenue': 1456.0}, {'customer': 'B H Allen Building Centre', 'revenue': 1445.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 1411.0}, {'customer': 'Robson Design Group', 'revenue': 1240.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 1130.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 1107.0}, {'customer': 'Net Retailers LLC', 'revenue': 1103.0}, {'customer': 'We are Sparrow Studio', 'revenue': 1098.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1056.0}, {'customer': 'Studio Dwell', 'revenue': 1049.0}, {'customer': 'Design Collaborative, Inc.', 'revenue': 1020.0}, {'customer': 'Pabor Designs Purchasing Service Inc.', 'revenue': 1020.0}, {'customer': 'MOI Inc.', 'revenue': 1020.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 973.0}, {'customer': 'Hue Design LLC', 'revenue': 920.0}, {'customer': 'Source', 'revenue': 920.0}, {'customer': "Today's Patio", 'revenue': 892.0}, {'customer': 'Image Urbaine', 'revenue': 880.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 878.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 858.0}, {'customer': 'Patio Productions', 'revenue': 816.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 778.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 778.0}, {'customer': 'CMS Commercial Furniture', 'revenue': 755.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 731.0}, {'customer': 'Patio Comfort', 'revenue': 725.0}, {'customer': 'Garden Architecture & Design', 'revenue': 635.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 620.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 590.0}, {'customer': 'Lawai Beach Resort', 'revenue': 589.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 579.0}, {'customer': 'Model Home Interiors Inc', 'revenue': 576.0}, {'customer': 'Sonoma Backyard', 'revenue': 541.0}, {'customer': 'Piscine Hippocampe', 'revenue': 535.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 525.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 518.0}, {'customer': 'Zachary Park Hotel QOZB c/o Benjamin West(agent)', 'revenue': 510.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 497.0}, {'customer': 'InnVest Hotels Limited', 'revenue': 477.0}, {'customer': 'Office Revolution LLC', 'revenue': 460.0}, {'customer': 'Bridget Bohacz & Associates Inc', 'revenue': 460.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 460.0}, {'customer': 'Jori Interiors', 'revenue': 460.0}, {'customer': "Bishop's Casual Living", 'revenue': 435.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 420.0}, {'customer': 'GST Interiors, LLC', 'revenue': 415.0}, {'customer': 'Commonwealth Design Group', 'revenue': 410.0}, {'customer': 'Office Concepts Ltd', 'revenue': 389.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 360.0}, {'customer': '4C Group', 'revenue': 360.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 351.0}, {'customer': "Mio's Furniture Fashions", 'revenue': 331.0}, {'customer': 'Main Street Furniture', 'revenue': 328.0}, {'customer': 'Ifurnish Co.', 'revenue': 328.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 328.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 324.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 316.0}, {'customer': 'Sunset Home and Patio', 'revenue': 313.0}, {'customer': 'Veranda Home & Garden Collection', 'revenue': 313.0}, {'customer': 'Aqua Fire Leisure', 'revenue': 311.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 294.0}, {'customer': "Sherri's Living Large", 'revenue': 280.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 259.0}, {'customer': 'D.L. Shury Developments Ltd', 'revenue': 258.0}, {'customer': 'Abacus Furniture', 'revenue': 256.0}, {'customer': 'The Design Resource Group, Inc.', 'revenue': 245.0}, {'customer': 'Beachcomber Hot Tubs & Outdoor Living', 'revenue': 245.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 196.0}, {'customer': 'Coombs Furniture', 'revenue': 184.0}, {'customer': 'Farris Design Studio', 'revenue': 173.0}, {'customer': 'Canadian Home Leisure', 'revenue': 166.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 164.0}, {'customer': 'Emigh Ace Hardware', 'revenue': 156.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 156.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 156.0}, {'customer': 'Crystalview', 'revenue': 147.0}, {'customer': 'Rattan Wicker & Cane', 'revenue': 144.0}, {'customer': 'Industrial Revolution', 'revenue': 122.0}, {'customer': 'Morinville Home Hardware', 'revenue': 117.0}, {'customer': 'All Backyard Fun', 'revenue': 69.0}, {'customer': 'FirstService Residential-Austin', 'revenue': 62.0}, {'customer': 'Georgia Patio Inc', 'revenue': 53.0}, {'customer': 'Elders Ace', 'revenue': 53.0}, {'customer': "Schneiderman's Furniture, Inc.", 'revenue': 26.0}, {'customer': 'Americasmart Real Estate LLC', 'revenue': 0.0}, {'customer': 'Pangaea Patio', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}, {'customer': 'Drew Ruesch Interiors', 'revenue': 0.0}] | [{'item': 'CU54458', 'desc': 'Lucia Swivel Rocking Arm Chair Cushion (w/button)', 'available': 2}] |
| CU55001 | Copacabana Club Chair Cushion | COL204 | 178,063 | 772 | 83 | — | [{'customer': 'Country Furniture', 'revenue': 8880.0}, {'customer': 'Hilton Supply Management', 'revenue': 7800.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 4680.0}, {'customer': 'US Hospitality Group', 'revenue': 4680.0}, {'customer': 'Elland Property Development Limited', 'revenue': 4160.0}, {'customer': 'Into The Garden, Inc.', 'revenue': 4043.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 3900.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 3888.0}, {'customer': '1001 Canal LLC', 'revenue': 3720.0}, {'customer': 'Carver & Associates', 'revenue': 3640.0}, {'customer': 'PCH Hotels & Resort-Shoals c/oPurchasing Dimension', 'revenue': 3380.0}, {'customer': 'Net Retailers LLC', 'revenue': 3360.0}, {'customer': 'Blu Salmon, LLC', 'revenue': 3290.0}, {'customer': 'Muse Design Inc', 'revenue': 3120.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 3085.0}, {'customer': 'Brier Properties LLC', 'revenue': 2600.0}, {'customer': 'Kristin Martin Design', 'revenue': 2473.0}, {'customer': 'Carolina Hotel Investors Crabtree, LLC', 'revenue': 2414.0}, {'customer': 'Touchmark c/o Source', 'revenue': 2413.0}, {'customer': "Bishop's Casual Living", 'revenue': 2297.0}, {'customer': 'Furniture Solutions Group', 'revenue': 2280.0}, {'customer': 'Zachary Park Hotel QOZB c/o Benjamin West(agent)', 'revenue': 2280.0}, {'customer': 'Littman Bros Energy Supplies, Inc', 'revenue': 2106.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 2080.0}, {'customer': 'River Ridge Renovations LLC', 'revenue': 2080.0}, {'customer': 'Hampton Inn Detroit/Southgate', 'revenue': 2080.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2080.0}, {'customer': 'Keaton Interiors', 'revenue': 1960.0}, {'customer': 'Tarrison Products Ltd.', 'revenue': 1880.0}, {'customer': 'CIM Group c/o The Stroud Group', 'revenue': 1880.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 1863.0}, {'customer': 'B2 Design Co.', 'revenue': 1830.0}, {'customer': 'The Thrash Group c/o J Desterbecq & Associates', 'revenue': 1744.0}, {'customer': 'Thiel and Thiel, Inc', 'revenue': 1680.0}, {'customer': 'Patio & Home Direct', 'revenue': 1666.0}, {'customer': 'His Chattanooga c/o The Stroud Group', 'revenue': 1560.0}, {'customer': 'RK Hospitality Design', 'revenue': 1560.0}, {'customer': 'EAS Investment Enterprises Inc.', 'revenue': 1560.0}, {'customer': 'Hampton Inn & Suites Knightdale', 'revenue': 1560.0}, {'customer': 'Complete Office LLC', 'revenue': 1560.0}, {'customer': 'ZMC Hotels, Llc', 'revenue': 1560.0}, {'customer': 'Streetlights Residential', 'revenue': 1410.0}, {'customer': 'Trio, Inc.', 'revenue': 1307.0}, {'customer': 'Urban Shore Interior Design', 'revenue': 1182.0}, {'customer': 'One World Design Source', 'revenue': 1140.0}, {'customer': 'One10', 'revenue': 1140.0}, {'customer': 'Fourth Avenue Seattle Hotel LLC dba/Kimpton Monaco', 'revenue': 1107.0}, {'customer': 'Zenn Investing', 'revenue': 1082.0}, {'customer': 'Hampton Inn Suites-Roseburg OR c/o Dwelling(Agent)', 'revenue': 1040.0}, {'customer': 'JPH Procurement', 'revenue': 1040.0}, {'customer': 'Curve Hospitality', 'revenue': 1040.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 1040.0}, {'customer': 'Destiny Builders', 'revenue': 1040.0}, {'customer': 'Metzger, Inc.', 'revenue': 1040.0}, {'customer': 'HIS Hamilton Place c/o The Stroud Group', 'revenue': 1040.0}, {'customer': 'Property c/o Jerry Osborne & Asso, Inc.', 'revenue': 1040.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 1040.0}, {'customer': 'Uniik Design Solutions', 'revenue': 1040.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 1040.0}, {'customer': 'Pinnacle South LLC', 'revenue': 1040.0}, {'customer': 'Model Home Interiors Inc', 'revenue': 1008.0}, {'customer': 'Williams Olander Interior Design', 'revenue': 1007.0}, {'customer': 'Sunset Home and Patio', 'revenue': 984.0}, {'customer': 'The Childs Dreyfus Group', 'revenue': 982.0}, {'customer': 'Wegman Design Group', 'revenue': 940.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 914.0}, {'customer': 'Zauner Manhattan Design', 'revenue': 907.0}, {'customer': "Today's Patio", 'revenue': 885.0}, {'customer': 'Starland Property Co, LLC', 'revenue': 885.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 848.0}, {'customer': 'Le Reve Design & Associates', 'revenue': 840.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 835.0}, {'customer': 'Dexter Hotel Group LLC c/o First Call Hosp(agent)', 'revenue': 780.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 692.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 672.0}, {'customer': 'CO-OP At Home', 'revenue': 634.0}, {'customer': 'J. Davenport Associates', 'revenue': 553.0}, {'customer': 'Patio Productions', 'revenue': 526.0}, {'customer': 'Source', 'revenue': 520.0}, {'customer': 'Hampton Inn Phoenix/Anthem', 'revenue': 520.0}, {'customer': 'Hilton Garden Inn - Las Vegas Strip South', 'revenue': 520.0}, {'customer': 'Hampton Inn & Suites Hemet CA', 'revenue': 520.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 520.0}, {'customer': 'Olympia Equity Investors XIII, Llc c/o The Gettys', 'revenue': 520.0}, {'customer': 'Hotel Rehabs', 'revenue': 520.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 520.0}, {'customer': 'Harbaugh Construction LLC', 'revenue': 520.0}, {'customer': 'Town Creek Plaza', 'revenue': 520.0}, {'customer': 'Laporte Hotel Suites, LLC dba/Hampton Inn', 'revenue': 520.0}, {'customer': 'Schoolcraft Hospitality Llc', 'revenue': 520.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 520.0}, {'customer': 'Hampton Inn - Dyersburg, TN c/o Hersha Purchasing', 'revenue': 520.0}, {'customer': 'HI Cleveland II, LLC c/o The Stroud Group', 'revenue': 520.0}, {'customer': 'HC Kitsap, LLC', 'revenue': 520.0}, {'customer': 'SAK Harbor LLC c/o Sourcing Advisors', 'revenue': 520.0}, {'customer': 'Hampton Inn Waynesburg c/o Too Tall Trading Post', 'revenue': 520.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 520.0}, {'customer': 'Kernersville Hotels, LLC c/o Craver & Asso(agent)', 'revenue': 520.0}, {'customer': 'Dalfen Sales Agency Inc', 'revenue': 520.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 520.0}, {'customer': 'FFE Solutions LLC', 'revenue': 520.0}, {'customer': 'Design Environments', 'revenue': 520.0}, {'customer': 'Odyssey Propco VII, LLC c/o Aintree, LLC(agent)', 'revenue': 520.0}, {'customer': 'Wichita Falls Lodging, LP', 'revenue': 520.0}, {'customer': 'Walteriors Design LLC', 'revenue': 520.0}, {'customer': 'Pam Ellis & Associates, Inc.', 'revenue': 520.0}, {'customer': 'P&C Hotel LLC c/o ACC Design Inc(agent)', 'revenue': 520.0}, {'customer': 'Champion Supply LLC', 'revenue': 520.0}, {'customer': 'Hampton Inn & Suites Swansboro, NC', 'revenue': 520.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 508.0}, {'customer': 'Workshop Studio', 'revenue': 503.0}, {'customer': 'Reusch Interior Design', 'revenue': 503.0}, {'customer': 'GC Waikiki Hotel OpCo LLC c/o Level 3 Design Group', 'revenue': 500.0}, {'customer': 'Morinville Home Hardware', 'revenue': 489.0}, {'customer': 'Catalyst Interiors Inc.', 'revenue': 470.0}, {'customer': 'California Contract & Home Inc', 'revenue': 470.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 432.0}, {'customer': 'Tarson Supply Corp.', 'revenue': 416.0}, {'customer': 'Coombs Furniture', 'revenue': 403.0}, {'customer': 'Shop the Studio at Design Mart', 'revenue': 376.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 376.0}, {'customer': 'Forest Glade Fireplaces', 'revenue': 376.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 376.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 363.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 342.0}, {'customer': 'Luxe Furniture Company', 'revenue': 327.0}, {'customer': 'Paradise Pools (Enterprises) Ltd', 'revenue': 305.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 269.0}, {'customer': 'Spark Studio + Source LLC', 'revenue': 260.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 260.0}, {'customer': 'Terra Verde', 'revenue': 188.0}, {'customer': 'Parco Piscines & Spas Ltee (mq018)', 'revenue': 188.0}, {'customer': 'Piscine Hippocampe', 'revenue': 188.0}, {'customer': 'Centre Massicotte Inc.', 'revenue': 179.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 163.0}, {'customer': 'Hospitality Media Group LLC', 'revenue': 151.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 150.0}, {'customer': 'Hampton Inn Greenville, NC c/o Linked Hospitality', 'revenue': 0.0}, {'customer': 'Valiant Products Corportion', 'revenue': 0.0}, {'customer': 'Hampton Inn Camden c/o Linked Hospitality (Agent)', 'revenue': 0.0}, {'customer': 'Hampton Inn Edenton', 'revenue': 0.0}, {'customer': 'Level 3 Design Group', 'revenue': 0.0}, {'customer': 'Pangaea Patio', 'revenue': 0.0}, {'customer': 'Tharaldson Hospitality Development, LLC', 'revenue': 0.0}, {'customer': 'Polygon Interior Design Ltd.', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Rama Tika Management LLC', 'revenue': 0.0}, {'customer': 'ADS Hospitality LLC', 'revenue': 0.0}, {'customer': 'Legacy Hotels c/o Carver and Asso, Atlanta (agent)', 'revenue': 0.0}, {'customer': 'NSK Design Group', 'revenue': 0.0}] | — |
| FN61788WTR | Biltmore Swivel Recliner | COL87 | 174,052 | 196 | 0 | — | [{'customer': 'Offenbachers Home Escapes', 'revenue': 11339.0}, {'customer': 'Sunnyland Furniture', 'revenue': 9601.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 8128.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 7487.0}, {'customer': 'Patio Style', 'revenue': 6694.0}, {'customer': 'ZLM Enterprises', 'revenue': 6499.0}, {'customer': 'Sequoia Outback', 'revenue': 6477.0}, {'customer': 'Stauffers of Kissel Hill', 'revenue': 6213.0}, {'customer': 'Into The Garden, Inc.', 'revenue': 5801.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 5680.0}, {'customer': 'OutBack Patio Furnishings', 'revenue': 5099.0}, {'customer': 'Busch Fireplace', 'revenue': 4824.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 4416.0}, {'customer': 'Club Piscines Granby', 'revenue': 4352.0}, {'customer': 'Furniture Source International', 'revenue': 4100.0}, {'customer': 'Luxe Furniture Company', 'revenue': 4097.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 4001.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 3840.0}, {'customer': 'Georgia Patio Inc', 'revenue': 3730.0}, {'customer': 'Opdyke Furniture Inc', 'revenue': 3728.0}, {'customer': 'Greater Southern Home Recreation', 'revenue': 3400.0}, {'customer': 'High End Patio Furniture', 'revenue': 3400.0}, {'customer': 'Treescapes - The Outdoor Living Center', 'revenue': 3300.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 3010.0}, {'customer': 'Patio Productions', 'revenue': 2900.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 2880.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 2640.0}, {'customer': "Al's Garden Center& Greenhouses, LLC", 'revenue': 2200.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 2200.0}, {'customer': 'Hollywood Pool & Spa, Inc.', 'revenue': 2000.0}, {'customer': 'Beaver Bark & Rock', 'revenue': 2000.0}, {'customer': 'Veranda Home & Garden Collection', 'revenue': 1920.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 1920.0}, {'customer': 'Littman Bros Energy Supplies, Inc', 'revenue': 1862.0}, {'customer': 'The Collective Outdoors', 'revenue': 1840.0}, {'customer': 'Corner Collection', 'revenue': 1720.0}, {'customer': 'Custom Fireplace Patio and BBQ', 'revenue': 1700.0}, {'customer': "Bowman's Stove & Patio Inc.", 'revenue': 1600.0}, {'customer': 'Watsons Fire Place & Patio', 'revenue': 1600.0}, {'customer': 'Woodburners, Inc.', 'revenue': 1600.0}, {'customer': 'Sunshine Nursery + Greenhouse', 'revenue': 1280.0}, {'customer': 'Hive Design LLC', 'revenue': 1250.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 1152.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1152.0}, {'customer': 'Elegant Outdoor Living', 'revenue': 1000.0}, {'customer': 'Philadelphia Botanical Products', 'revenue': 1000.0}, {'customer': 'Camrose Home Hardware and Building Center', 'revenue': 960.0}, {'customer': 'East Texas Brick', 'revenue': 920.0}, {'customer': 'Spas of Colorado, Inc', 'revenue': 850.0}, {'customer': 'Daylight Home & Gardens', 'revenue': 850.0}, {'customer': 'Arkansas Furniture', 'revenue': 850.0}, {'customer': 'All Seasons Living', 'revenue': 495.0}, {'customer': 'Home And Patio', 'revenue': 495.0}] | [{'item': 'FN61711WTR', 'desc': 'Biltmore Dining Side Chair', 'available': 52}, {'item': 'FN61711PEW-OGY', 'desc': 'Biltmore Dining Side Chair', 'available': 38}, {'item': 'FN61712PEW-OGY', 'desc': 'Biltmore Dining Arm Chair', 'available': 26}, {'item': 'FN61704OGY', 'desc': 'Biltmore Coffee Table', 'available': 24}, {'item': 'FN61716PEW-OGY', 'desc': 'Biltmore Ottoman', 'available': 23}, {'item': 'FN61706PEY-OGY', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 23}, {'item': 'FN61712WTR', 'desc': 'Biltmore Dining Arm Chair', 'available': 19}, {'item': 'FN61704RUB', 'desc': 'Biltmore Coffee Table', 'available': 16}, {'item': 'FN61788PEW-OGY', 'desc': 'Biltmore Swivel Recliner', 'available': 15}, {'item': 'FN61704PEY-OGY', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 12}, {'item': 'FN61703PEW-OGY', 'desc': 'Biltmore Sofa', 'available': 10}, {'item': 'FN61704WLT-RUB', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 7}, {'item': 'FN61701WTR', 'desc': 'Biltmore Club Chair', 'available': 7}, {'item': 'FN61702WTR', 'desc': 'Biltmore Love Seat', 'available': 7}, {'item': 'FN61703WTR', 'desc': 'Biltmore Sofa', 'available': 7}, {'item': 'FN61704HGA', 'desc': 'Biltmore Coffee Table', 'available': 5}, {'item': 'FN61705PEY-OGY', 'desc': 'Biltmore Sintered Stone End Table', 'available': 4}, {'item': 'FN61703WTR-RUB', 'desc': 'Biltmore Sofa', 'available': 2}, {'item': 'FN61706WLT-RUB', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 1}] |
| UM01009BLK/C | 10' Sq Cantilever Umbrella w/Canopy&Base | COL73 | 169,959 | 149 | 13 | — | [{'customer': 'Vancouver Sofa & Patio', 'revenue': 42717.0}, {'customer': 'Patio & Home Direct', 'revenue': 13575.0}, {'customer': 'Country Furniture', 'revenue': 12491.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 11408.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 8730.0}, {'customer': 'St. Lawrence Pools', 'revenue': 7167.0}, {'customer': 'Innovations paysagées Ladouceur', 'revenue': 6273.0}, {'customer': 'Okanagan Home Center', 'revenue': 5796.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 5269.0}, {'customer': 'Garden Architecture & Design', 'revenue': 4568.0}, {'customer': 'CO-OP At Home', 'revenue': 3749.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 3638.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 3566.0}, {'customer': 'Cozy Stylish Chic', 'revenue': 2537.0}, {'customer': 'Janelle Interiors', 'revenue': 2450.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 2402.0}, {'customer': 'Design Therapy Inc', 'revenue': 2166.0}, {'customer': 'PHG Ashburn LLC', 'revenue': 1871.0}, {'customer': 'Image Urbaine', 'revenue': 1686.0}, {'customer': 'Stacey White Design', 'revenue': 1686.0}, {'customer': 'Homey Home', 'revenue': 1550.0}, {'customer': 'Cash Account (c$)', 'revenue': 1349.0}, {'customer': 'Terra Verde', 'revenue': 1349.0}, {'customer': 'Parco Piscines & Spas Ltee (mq018)', 'revenue': 1349.0}, {'customer': 'Joanna Branzell Interior Design', 'revenue': 1325.0}, {'customer': 'Coombs Furniture', 'revenue': 1320.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 1320.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 1281.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 1269.0}, {'customer': 'Cash Account', 'revenue': 1269.0}, {'customer': "Voth's Brandsource Home Furnishings", 'revenue': 1269.0}, {'customer': 'Hilltop Interiors', 'revenue': 1240.0}, {'customer': "Piscines CM Val D'or Inc (mq002)", 'revenue': 1240.0}, {'customer': 'Club Piscines Granby', 'revenue': 1190.0}, {'customer': 'O.M. Design Group', 'revenue': 1187.0}, {'customer': 'The Art of Room Design', 'revenue': 1187.0}, {'customer': 'Meubles Duboise', 'revenue': 1178.0}, {'customer': 'Maud Home', 'revenue': 1116.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1116.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 1056.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 1054.0}, {'customer': 'Design One Stevens Interiors', 'revenue': 0.0}, {'customer': 'Studio B Design Group', 'revenue': 0.0}, {'customer': 'Curve Interiors', 'revenue': 0.0}] | [{'item': 'UM01010SLV-CCL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Cloud canopy", 'available': 10}, {'item': 'UM01010SLV-CBL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Black canopy", 'available': 9}, {'item': 'UM01004SLV/C', 'desc': "10' Sq Deluxe Alum Umbrella, 48mm Pole W/canopy", 'available': 8}, {'item': 'UM00906BRZ/C', 'desc': "9' Alum W/fiber Ribs,crank Lift,collar Tilt,canopy", 'available': 6}, {'item': 'UM00909POLE-BRZ', 'desc': '45in Bar Bottom Pole for UM00906BRZ/C', 'available': 5}] |
| FN54420ASG | Lucia Lounger | LUCIA | 165,018 | 203 | 0 | — | [{'customer': 'Palmetto Bluff Club LLC', 'revenue': 83497.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 10031.0}, {'customer': 'Source', 'revenue': 9901.0}, {'customer': 'Patio & Home Direct', 'revenue': 6888.0}, {'customer': 'Image Urbaine', 'revenue': 3690.0}, {'customer': 'Furniture Solutions Group', 'revenue': 3630.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 3300.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 3280.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 3075.0}, {'customer': 'Macarthur Enterprises Ltd', 'revenue': 3075.0}, {'customer': 'Crystalview', 'revenue': 2952.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 2788.0}, {'customer': 'Meubles Poisson Ltée', 'revenue': 2460.0}, {'customer': 'Cash Account', 'revenue': 2460.0}, {'customer': 'Garden Architecture & Design', 'revenue': 2460.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 2132.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 2112.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 1980.0}, {'customer': 'Joanna Branzell Interior Design', 'revenue': 1650.0}, {'customer': 'Maritime Hospitality (Danja Inc)', 'revenue': 1640.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1476.0}, {'customer': "Mio's Furniture Fashions", 'revenue': 1394.0}, {'customer': 'Patio Productions', 'revenue': 1336.0}, {'customer': 'B H Allen Building Centre', 'revenue': 1312.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1230.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 1188.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 738.0}, {'customer': 'Net Retailers LLC', 'revenue': 726.0}, {'customer': 'Can-Tario Brick & Stone', 'revenue': 697.0}, {'customer': 'Ifurnish Co.', 'revenue': 660.0}, {'customer': 'Christy Sports, LLC', 'revenue': 653.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 607.0}] | [{'item': 'FN54411OGY', 'desc': 'Lucia Dining Side Chair', 'available': 94}, {'item': 'FN54411ASG', 'desc': 'Lucia Dining Side Chair', 'available': 89}, {'item': 'FN54441OGY', 'desc': 'Lucia Bar Chair', 'available': 44}, {'item': 'FN54412OGY', 'desc': 'Lucia Dining Arm Chair', 'available': 43}, {'item': 'FN54453ASG-V', 'desc': 'Lucia Curved Corner', 'available': 31}, {'item': 'FN54402OGY', 'desc': 'Lucia Love Seat', 'available': 30}, {'item': 'FN54440OGY', 'desc': 'Lucia Counter Chair', 'available': 30}, {'item': 'FN54458PRL', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 29}, {'item': 'FN54453OGY-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 28}, {'item': 'FN54453OGY-V', 'desc': 'Lucia Curved Corner', 'available': 25}, {'item': 'FN54453ASG-R', 'desc': 'Lucia Wedge Right Arm', 'available': 25}, {'item': 'FN54452OGY-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 25}, {'item': 'FN54452OGY-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 25}, {'item': 'FN54404PRL', 'desc': 'Lucia Coffee Table', 'available': 24}, {'item': 'FN54453ASG-L', 'desc': 'Lucia Wedge Left Arm', 'available': 22}, {'item': 'FN54404ASG', 'desc': 'Lucia Coffee Table', 'available': 17}, {'item': 'FN54420OGY', 'desc': 'Lucia Lounger', 'available': 15}, {'item': 'FN54452ASG-C', 'desc': 'Lucia Wedge Corner', 'available': 14}, {'item': 'FN54416OGY', 'desc': 'Lucia Ottoman', 'available': 14}, {'item': 'FN54403PRL', 'desc': 'Lucia Sofa', 'available': 13}, {'item': 'FN54452ASG-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 12}, {'item': 'FN54452ASG-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 12}, {'item': 'FN54416ASG', 'desc': 'Lucia Ottoman', 'available': 12}, {'item': 'FN54458ASG', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 11}, {'item': 'FN54405PEY-OGY', 'desc': 'Lucia Sintered Stone End Table (KD)', 'available': 10}, {'item': 'FN54457ASG', 'desc': 'Lucia Sectional 40in Round Coffee Table/ottoman', 'available': 8}, {'item': 'FN54453ASG-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 8}, {'item': 'FN54468PRL', 'desc': 'Lucia Swivel Rocker', 'available': 6}, {'item': 'FN54404PEY-OGY', 'desc': 'Lucia Sintered Stone Coffee Table (KD)', 'available': 6}, {'item': 'FN54468OGY', 'desc': 'Lucia Swivel Rocker', 'available': 4}, {'item': 'FN54441ASG', 'desc': 'Lucia Bar Chair', 'available': 4}, {'item': 'FN54440ASG', 'desc': 'Lucia Counter Chair', 'available': 4}, {'item': 'FN54412ASG', 'desc': 'Lucia Dining Arm Chair', 'available': 4}, {'item': 'FN54405PRL', 'desc': 'Lucia End Table', 'available': 2}, {'item': 'FN54405ASG', 'desc': 'Lucia End Table', 'available': 1}] |
| FN57001ASG | Element 5.0 Club Chair | COL61 | 163,081 | 279 | 14 | — | [{'customer': 'Bobby Design Inc.', 'revenue': 17572.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 11495.0}, {'customer': 'Dave Bang Associates Inc.', 'revenue': 11181.0}, {'customer': 'Thiel and Thiel, Inc', 'revenue': 9681.0}, {'customer': 'Net Retailers LLC', 'revenue': 7985.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 7720.0}, {'customer': 'Isidore Landscapes Inc.', 'revenue': 7601.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 6566.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 5654.0}, {'customer': 'Westin Kierland Resort & Spa', 'revenue': 5324.0}, {'customer': 'Royal Kona Resort', 'revenue': 4840.0}, {'customer': 'The Design Resource Group, Inc.', 'revenue': 4840.0}, {'customer': "Bishop's Casual Living", 'revenue': 3830.0}, {'customer': 'Houston Landscapes Ltd.', 'revenue': 3648.0}, {'customer': 'Studio Dwell', 'revenue': 3630.0}, {'customer': 'Patio & Home Direct', 'revenue': 3587.0}, {'customer': 'Luxe Furniture Company', 'revenue': 3174.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 2797.0}, {'customer': 'Kerry Imagine Designs Llc', 'revenue': 2662.0}, {'customer': 'Adria International Inc', 'revenue': 2584.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2462.0}, {'customer': 'Timmermans Landscaping', 'revenue': 2280.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 2189.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 2189.0}, {'customer': 'Country Furniture', 'revenue': 2189.0}, {'customer': 'Room By Room', 'revenue': 1824.0}, {'customer': 'Ifurnish Co.', 'revenue': 1802.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1549.0}, {'customer': 'Aava Whistler Hotel', 'revenue': 1520.0}, {'customer': 'Sun Gallery Patio Furniture Ltd.', 'revenue': 1368.0}, {'customer': 'Distrist Hubert Inc', 'revenue': 1368.0}, {'customer': "Today's Patio", 'revenue': 1300.0}, {'customer': 'Rethink Interiors&lifestyles', 'revenue': 1210.0}, {'customer': 'O.M. Design Group', 'revenue': 1210.0}, {'customer': 'IDM Development, LLC', 'revenue': 1210.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 1098.0}, {'customer': 'Heritage Office Furnishings Ltd.', 'revenue': 1094.0}, {'customer': 'All Backyard Fun', 'revenue': 1065.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 1065.0}, {'customer': 'Club Piscine (Terrebonne)', 'revenue': 1034.0}, {'customer': 'East Texas Brick', 'revenue': 871.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 775.0}, {'customer': 'Morinville Home Hardware', 'revenue': 760.0}, {'customer': 'The Collaborative Design Studio Inc', 'revenue': 760.0}, {'customer': 'Solutions Business Interiors', 'revenue': 760.0}, {'customer': 'Monticello Homes', 'revenue': 666.0}, {'customer': 'Bridge Interiors Furniture', 'revenue': 608.0}, {'customer': 'Patio Style', 'revenue': 484.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 0.0}, {'customer': 'Furniture Solutions Group', 'revenue': 0.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 0.0}] | [{'item': 'FN57011TWH', 'desc': 'Element 5.0 Dining Side Chair', 'available': 52}, {'item': 'FN57068OGY', 'desc': 'Element 5.0 Swivel Rocker', 'available': 39}, {'item': 'FN57068ASG', 'desc': 'Element 5.0 Swivel Rocker', 'available': 32}, {'item': 'FN57012TWH', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 31}, {'item': 'FN57005TWH', 'desc': 'Element 5.0 40in Sq C/T w/alum', 'available': 30}, {'item': 'FN57001OGY', 'desc': 'Element 5.0 Club Chair', 'available': 29}, {'item': 'FN57003OGY', 'desc': 'Element 5.0 2.5-seater Sofa', 'available': 28}, {'item': 'FN57016OGY', 'desc': 'Element 5.0 Ottoman', 'available': 25}, {'item': 'FN57016TWH', 'desc': 'Element 5.0 Ottoman', 'available': 17}, {'item': 'FN57005PEY-OGY', 'desc': 'Element 5.0 40in Square Sintered Stone Coffee Tabl', 'available': 17}, {'item': 'FN57052OGY-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 12}, {'item': 'FN57004TWH', 'desc': 'Element 5.0 Rect C/T w/alum', 'available': 12}, {'item': 'FN57052OGY-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 12}, {'item': 'FN57019ASG', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 11}, {'item': 'FN57021OGY', 'desc': 'Element 5.0 Double Chaise Lounger (New structure)', 'available': 11}, {'item': 'FN57068TWH', 'desc': 'Element 5.0 Swivel Rocker', 'available': 10}, {'item': 'FN57053OGY-N', 'desc': 'Element 5.0 Corner', 'available': 9}, {'item': 'FN57006PEY-OGY', 'desc': 'Element 5.0 Sintered Stone Side Table', 'available': 9}, {'item': 'FN57053OGY-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 8}, {'item': 'FN57004PEY-OGY', 'desc': 'Element 5.0 Rect Sintered Stone Coffee Table', 'available': 8}, {'item': 'FN57019OGY', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 7}, {'item': 'FN57012ASG', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 7}, {'item': 'FN57003TWH', 'desc': 'Element 5.0 2.5-Seater Sofa', 'available': 6}, {'item': 'FN57022WHT', 'desc': 'Element 5.0 Double Chaise Lounger', 'available': 5}, {'item': 'FN57052ASG-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 5}, {'item': 'FN57052TWH-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 4}, {'item': 'FN57053ASG-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57006CEM', 'desc': 'Element 5.0 Side Table W/alum Top CEM, Base ASG', 'available': 3}, {'item': 'FN57053TWH-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57053TWH-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 2}, {'item': 'FN57052ASG-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 2}, {'item': 'FN57052TWH-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 2}, {'item': 'FN57053ASG-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 1}, {'item': 'FN57011ASG', 'desc': 'Element 5.0 Dining Side Chair', 'available': 1}, {'item': 'FN57001TWH', 'desc': 'Element 5.0 Club Chair', 'available': 1}] |
| FN65520BLK | Avenue Lounger | COL145 | 159,588 | 236 | 10 | 2026-6-30 | [{'customer': 'Victory Furniture LLC.', 'revenue': 27717.0}, {'customer': 'Ellie Aiello Interiors', 'revenue': 22332.0}, {'customer': 'Two Fifty Master LLC c/o The Gettys Group', 'revenue': 15247.0}, {'customer': 'Streetlights Residential', 'revenue': 13301.0}, {'customer': 'Country Furniture', 'revenue': 11340.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 5670.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 5319.0}, {'customer': 'Sanctuary Home & Patio', 'revenue': 4928.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 4200.0}, {'customer': 'All American Pool & Patio', 'revenue': 3696.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 3500.0}, {'customer': "Bishop's Casual Living", 'revenue': 3150.0}, {'customer': 'Southport Outdoor Living', 'revenue': 3150.0}, {'customer': 'Contract Furniture Solutions', 'revenue': 2800.0}, {'customer': 'Piscine Hippocampe', 'revenue': 2800.0}, {'customer': 'Wade Gordon Hairdressing Academy', 'revenue': 2800.0}, {'customer': 'Light House Co.', 'revenue': 2800.0}, {'customer': 'Royal Bay Ryder Village LP', 'revenue': 2625.0}, {'customer': 'The Patio Place USA, Inc', 'revenue': 2464.0}, {'customer': 'Garden Architecture & Design', 'revenue': 2369.0}, {'customer': 'Waterleaf Interiors /DOS Amigas Designs Inc', 'revenue': 2310.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 2100.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 1890.0}, {'customer': 'Furniture Source International', 'revenue': 1792.0}, {'customer': 'Northland Properties Corporation', 'revenue': 1750.0}, {'customer': 'Studio Dwell', 'revenue': 1540.0}, {'customer': 'Patio Options', 'revenue': 1540.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 1190.0}, {'customer': 'The Patio', 'revenue': 952.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 700.0}, {'customer': 'Crystalview', 'revenue': 630.0}, {'customer': 'Daylight Home & Gardens', 'revenue': 616.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 370.0}, {'customer': 'Arveaux Interiors', 'revenue': 0.0}, {'customer': 'Luxe Furniture Company', 'revenue': 0.0}] | [{'item': 'FN65505WHT', 'desc': 'Avenue Side Table', 'available': 27}, {'item': 'FN65505BLK', 'desc': 'Avenue Side Table', 'available': 24}] |
| CU61301 | Poinciana Club Chair Cushion | COL217 | 152,554 | 637 | 8 | — | [{'customer': 'Elland Property Development Limited', 'revenue': 75066.0}, {'customer': 'JW Marriott Desert Ridge Resort and Spa', 'revenue': 19197.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 5763.0}, {'customer': 'KB Patio', 'revenue': 3492.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 3166.0}, {'customer': 'Luxe Furniture Company', 'revenue': 3116.0}, {'customer': 'CIB c/o Benjamin West (as agent)', 'revenue': 2588.0}, {'customer': 'J. Davenport Associates', 'revenue': 2560.0}, {'customer': 'Two Fifty Master LLC c/o The Gettys Group', 'revenue': 2205.0}, {'customer': 'Wegman Design Group', 'revenue': 2094.0}, {'customer': 'Keaton Interiors', 'revenue': 2038.0}, {'customer': 'Bluegreen Vacation Unlimited c/o Beyer Brown(agent', 'revenue': 1960.0}, {'customer': 'Hilton Supply Management', 'revenue': 1859.0}, {'customer': 'Creative License International, LLC', 'revenue': 1760.0}, {'customer': 'The Haus of Alchemy', 'revenue': 1620.0}, {'customer': 'GCC Procurement, LLC', 'revenue': 1593.0}, {'customer': 'Kathy Andrews Interiors, Inc.', 'revenue': 1581.0}, {'customer': 'Eatz Hospitality/Del Boca Brickell LP', 'revenue': 1425.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 1340.0}, {'customer': 'Patio Productions', 'revenue': 1101.0}, {'customer': 'Contract Furniture Solutions', 'revenue': 1080.0}, {'customer': 'Pixel Design Co.', 'revenue': 1080.0}, {'customer': 'Vicki Crew Interiors', 'revenue': 1000.0}, {'customer': 'The Art of Room Design', 'revenue': 980.0}, {'customer': 'Bobby Design Inc.', 'revenue': 950.0}, {'customer': 'Zauner Manhattan Design', 'revenue': 950.0}, {'customer': 'Net Retailers LLC', 'revenue': 758.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 740.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 700.0}, {'customer': 'Trio, Inc.', 'revenue': 675.0}, {'customer': 'Club Design Group, Inc.', 'revenue': 630.0}, {'customer': 'Lita Dirks & Co, Llc', 'revenue': 625.0}, {'customer': 'Country Furniture', 'revenue': 603.0}, {'customer': 'Alison Knapp Interior Design', 'revenue': 588.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 528.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 420.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 396.0}, {'customer': 'Elegant Outdoor Living', 'revenue': 392.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 392.0}, {'customer': 'S. Setlakwe Ltee', 'revenue': 392.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 352.0}, {'customer': 'Tri Supply Company', 'revenue': 352.0}, {'customer': 'Garden Architecture & Design', 'revenue': 332.0}, {'customer': 'Southport Outdoor Living', 'revenue': 315.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 311.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 282.0}, {'customer': 'Woodmill of Muskoka Inc', 'revenue': 282.0}, {'customer': 'The Patio Place USA, Inc', 'revenue': 216.0}, {'customer': 'Modern Living London', 'revenue': 173.0}, {'customer': 'Okanagan Home Center', 'revenue': 161.0}, {'customer': 'Les Jardins', 'revenue': 157.0}, {'customer': 'Real Patio Living Llc', 'revenue': 118.0}, {'customer': 'Cash Account', 'revenue': 100.0}, {'customer': 'Focus Design Interiors', 'revenue': 0.0}] | [{'item': 'CU61311', 'desc': 'Poinciana Dining Side Cushion (with button)', 'available': 2}] |
| FN57003ASG | Element 5.0 2.5-seater Sofa | COL61 | 135,573 | 135 | 0 | — | [{'customer': 'Tru Contract Interiors', 'revenue': 13343.0}, {'customer': 'Houston Landscapes Ltd.', 'revenue': 7783.0}, {'customer': 'Dave Bang Associates Inc.', 'revenue': 6838.0}, {'customer': 'Net Retailers LLC', 'revenue': 5860.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 5614.0}, {'customer': 'Country Furniture', 'revenue': 5004.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 4504.0}, {'customer': 'Royal Kona Resort', 'revenue': 4440.0}, {'customer': 'Bobby Design Inc.', 'revenue': 4170.0}, {'customer': 'Timmermans Landscaping', 'revenue': 4170.0}, {'customer': "Bishop's Casual Living", 'revenue': 4003.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 4003.0}, {'customer': 'Home And Patio', 'revenue': 3907.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 3552.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 3002.0}, {'customer': 'Patio & Home Direct', 'revenue': 3002.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 3002.0}, {'customer': 'Keca International', 'revenue': 2835.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2835.0}, {'customer': 'West One Design Inc.', 'revenue': 2780.0}, {'customer': 'Give Back Contracting', 'revenue': 2780.0}, {'customer': 'Sun Gallery Patio Furniture Ltd.', 'revenue': 2502.0}, {'customer': 'Haylie Read Design, LLC', 'revenue': 2220.0}, {'customer': 'Complete Office LLC', 'revenue': 2220.0}, {'customer': 'The Design Resource Group, Inc.', 'revenue': 2220.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 2007.0}, {'customer': 'Industrial Revolution', 'revenue': 1890.0}, {'customer': 'The Patio', 'revenue': 1731.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 1687.0}, {'customer': 'Distrist Hubert Inc', 'revenue': 1668.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1421.0}, {'customer': "Today's Patio", 'revenue': 1319.0}, {'customer': 'Sandman Signature Dallas Las Colinas Hotel &Suites', 'revenue': 1221.0}, {'customer': 'Trio, Inc.', 'revenue': 1221.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 1112.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1110.0}, {'customer': 'Rethink Interiors&lifestyles', 'revenue': 1110.0}, {'customer': 'Studio Dwell', 'revenue': 1110.0}, {'customer': 'Joanna Branzell Interior Design', 'revenue': 1110.0}, {'customer': 'Crystalview', 'revenue': 1001.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 977.0}, {'customer': 'Luxe Furniture Company', 'revenue': 967.0}, {'customer': 'Patio Style', 'revenue': 888.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 888.0}, {'customer': 'Innovative Designs & Mfg. Inc.', 'revenue': 888.0}, {'customer': 'Designers Resource Collection', 'revenue': 879.0}, {'customer': 'Ifurnish Co.', 'revenue': 830.0}, {'customer': 'East Texas Brick', 'revenue': 799.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 710.0}, {'customer': 'Patio Fireside Specialist Inc(sales Rep)', 'revenue': 440.0}] | [{'item': 'FN57011TWH', 'desc': 'Element 5.0 Dining Side Chair', 'available': 52}, {'item': 'FN57068OGY', 'desc': 'Element 5.0 Swivel Rocker', 'available': 39}, {'item': 'FN57068ASG', 'desc': 'Element 5.0 Swivel Rocker', 'available': 32}, {'item': 'FN57012TWH', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 31}, {'item': 'FN57005TWH', 'desc': 'Element 5.0 40in Sq C/T w/alum', 'available': 30}, {'item': 'FN57001OGY', 'desc': 'Element 5.0 Club Chair', 'available': 29}, {'item': 'FN57003OGY', 'desc': 'Element 5.0 2.5-seater Sofa', 'available': 28}, {'item': 'FN57016OGY', 'desc': 'Element 5.0 Ottoman', 'available': 25}, {'item': 'FN57016TWH', 'desc': 'Element 5.0 Ottoman', 'available': 17}, {'item': 'FN57005PEY-OGY', 'desc': 'Element 5.0 40in Square Sintered Stone Coffee Tabl', 'available': 17}, {'item': 'FN57052OGY-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 12}, {'item': 'FN57004TWH', 'desc': 'Element 5.0 Rect C/T w/alum', 'available': 12}, {'item': 'FN57052OGY-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 12}, {'item': 'FN57019ASG', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 11}, {'item': 'FN57021OGY', 'desc': 'Element 5.0 Double Chaise Lounger (New structure)', 'available': 11}, {'item': 'FN57068TWH', 'desc': 'Element 5.0 Swivel Rocker', 'available': 10}, {'item': 'FN57053OGY-N', 'desc': 'Element 5.0 Corner', 'available': 9}, {'item': 'FN57006PEY-OGY', 'desc': 'Element 5.0 Sintered Stone Side Table', 'available': 9}, {'item': 'FN57053OGY-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 8}, {'item': 'FN57004PEY-OGY', 'desc': 'Element 5.0 Rect Sintered Stone Coffee Table', 'available': 8}, {'item': 'FN57019OGY', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 7}, {'item': 'FN57012ASG', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 7}, {'item': 'FN57003TWH', 'desc': 'Element 5.0 2.5-Seater Sofa', 'available': 6}, {'item': 'FN57022WHT', 'desc': 'Element 5.0 Double Chaise Lounger', 'available': 5}, {'item': 'FN57052ASG-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 5}, {'item': 'FN57052TWH-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 4}, {'item': 'FN57053ASG-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57006CEM', 'desc': 'Element 5.0 Side Table W/alum Top CEM, Base ASG', 'available': 3}, {'item': 'FN57053TWH-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57053TWH-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 2}, {'item': 'FN57052ASG-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 2}, {'item': 'FN57052TWH-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 2}, {'item': 'FN57053ASG-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 1}, {'item': 'FN57011ASG', 'desc': 'Element 5.0 Dining Side Chair', 'available': 1}, {'item': 'FN57001TWH', 'desc': 'Element 5.0 Club Chair', 'available': 1}] |
| FN54403ASG | Lucia Sofa | LUCIA | 132,614 | 131 | 4 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 12365.0}, {'customer': 'Northwest Trends', 'revenue': 9856.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 7615.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 5168.0}, {'customer': 'Patio & Home Direct', 'revenue': 5058.0}, {'customer': 'Hue Design LLC', 'revenue': 4599.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 4327.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 4215.0}, {'customer': 'B H Allen Building Centre', 'revenue': 3878.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 3285.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 2866.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 2810.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2641.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 2409.0}, {'customer': 'Studio B Design Group', 'revenue': 2409.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 2409.0}, {'customer': 'Furniture Solutions Group', 'revenue': 2409.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 2409.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 2190.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 2023.0}, {'customer': 'Country Furniture', 'revenue': 2023.0}, {'customer': "Today's Patio", 'revenue': 1927.0}, {'customer': 'Crystalview', 'revenue': 1855.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1752.0}, {'customer': 'Abacus Furniture', 'revenue': 1686.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 1612.0}, {'customer': 'Cincinnati Pool & Patio', 'revenue': 1402.0}, {'customer': 'MOI Inc.', 'revenue': 1205.0}, {'customer': 'VAI Resort, LLC', 'revenue': 1205.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 1205.0}, {'customer': 'DGA Interiors', 'revenue': 1205.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 1205.0}, {'customer': 'Direct Supply Inc.', 'revenue': 1205.0}, {'customer': 'Entreprises H.P. Carignan Inc(mq034', 'revenue': 1124.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 1095.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 1095.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 1095.0}, {'customer': 'Kevin Roberts Interiors', 'revenue': 1095.0}, {'customer': 'Commonwealth Design Group', 'revenue': 1095.0}, {'customer': 'GST Interiors, LLC', 'revenue': 1095.0}, {'customer': 'Patio Comfort', 'revenue': 1068.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1012.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 1012.0}, {'customer': 'St. Lawrence Pools', 'revenue': 1012.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 1012.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1012.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 1012.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1012.0}, {'customer': 'Rattan Wicker & Cane', 'revenue': 964.0}, {'customer': 'Net Retailers LLC', 'revenue': 964.0}, {'customer': 'Industrial Revolution', 'revenue': 955.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 955.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 955.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 887.0}, {'customer': 'All Backyard Fun', 'revenue': 876.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 876.0}, {'customer': 'Main Street Furniture', 'revenue': 876.0}, {'customer': 'C.S. Wo & Sons, Ltd', 'revenue': 876.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 843.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 806.0}, {'customer': 'Patio Productions', 'revenue': 806.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 701.0}, {'customer': 'Mike Moser Studio', 'revenue': 0.0}] | [{'item': 'FN54411OGY', 'desc': 'Lucia Dining Side Chair', 'available': 94}, {'item': 'FN54411ASG', 'desc': 'Lucia Dining Side Chair', 'available': 89}, {'item': 'FN54441OGY', 'desc': 'Lucia Bar Chair', 'available': 44}, {'item': 'FN54412OGY', 'desc': 'Lucia Dining Arm Chair', 'available': 43}, {'item': 'FN54453ASG-V', 'desc': 'Lucia Curved Corner', 'available': 31}, {'item': 'FN54402OGY', 'desc': 'Lucia Love Seat', 'available': 30}, {'item': 'FN54440OGY', 'desc': 'Lucia Counter Chair', 'available': 30}, {'item': 'FN54458PRL', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 29}, {'item': 'FN54453OGY-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 28}, {'item': 'FN54453OGY-V', 'desc': 'Lucia Curved Corner', 'available': 25}, {'item': 'FN54453ASG-R', 'desc': 'Lucia Wedge Right Arm', 'available': 25}, {'item': 'FN54452OGY-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 25}, {'item': 'FN54452OGY-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 25}, {'item': 'FN54404PRL', 'desc': 'Lucia Coffee Table', 'available': 24}, {'item': 'FN54453ASG-L', 'desc': 'Lucia Wedge Left Arm', 'available': 22}, {'item': 'FN54404ASG', 'desc': 'Lucia Coffee Table', 'available': 17}, {'item': 'FN54420OGY', 'desc': 'Lucia Lounger', 'available': 15}, {'item': 'FN54452ASG-C', 'desc': 'Lucia Wedge Corner', 'available': 14}, {'item': 'FN54416OGY', 'desc': 'Lucia Ottoman', 'available': 14}, {'item': 'FN54403PRL', 'desc': 'Lucia Sofa', 'available': 13}, {'item': 'FN54452ASG-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 12}, {'item': 'FN54452ASG-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 12}, {'item': 'FN54416ASG', 'desc': 'Lucia Ottoman', 'available': 12}, {'item': 'FN54458ASG', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 11}, {'item': 'FN54405PEY-OGY', 'desc': 'Lucia Sintered Stone End Table (KD)', 'available': 10}, {'item': 'FN54457ASG', 'desc': 'Lucia Sectional 40in Round Coffee Table/ottoman', 'available': 8}, {'item': 'FN54453ASG-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 8}, {'item': 'FN54468PRL', 'desc': 'Lucia Swivel Rocker', 'available': 6}, {'item': 'FN54404PEY-OGY', 'desc': 'Lucia Sintered Stone Coffee Table (KD)', 'available': 6}, {'item': 'FN54468OGY', 'desc': 'Lucia Swivel Rocker', 'available': 4}, {'item': 'FN54441ASG', 'desc': 'Lucia Bar Chair', 'available': 4}, {'item': 'FN54440ASG', 'desc': 'Lucia Counter Chair', 'available': 4}, {'item': 'FN54412ASG', 'desc': 'Lucia Dining Arm Chair', 'available': 4}, {'item': 'FN54405PRL', 'desc': 'Lucia End Table', 'available': 2}, {'item': 'FN54405ASG', 'desc': 'Lucia End Table', 'available': 1}] |
| FN61790WTR-RUB | Biltmore Swivel Gliding Club | COL87 | 131,032 | 221 | 142 | 2026-6-16 | [{'customer': 'Sunnyland Furniture', 'revenue': 18727.0}, {'customer': 'Into The Garden, Inc.', 'revenue': 18672.0}, {'customer': 'Jack Wills Companies', 'revenue': 10846.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 9299.0}, {'customer': 'Tri Supply Company', 'revenue': 8787.0}, {'customer': 'Home And Patio', 'revenue': 7397.0}, {'customer': 'Georgia Patio Inc', 'revenue': 7000.0}, {'customer': 'If Walls Could Talk', 'revenue': 6865.0}, {'customer': 'OutBack Patio Furnishings', 'revenue': 5285.0}, {'customer': "Bowman's Stove & Patio Inc.", 'revenue': 3707.0}, {'customer': 'Casual Living Outfitters Llc', 'revenue': 3295.0}, {'customer': 'Sabine Pools Llc', 'revenue': 3295.0}, {'customer': 'Treescapes - The Outdoor Living Center', 'revenue': 2745.0}, {'customer': 'Luxe Furniture Company', 'revenue': 2663.0}, {'customer': 'Balboa Company', 'revenue': 2471.0}, {'customer': 'Backyard Adventures Of Iowa', 'revenue': 2333.0}, {'customer': "Al's Garden Center& Greenhouses, LLC", 'revenue': 2197.0}, {'customer': 'Corner Collection', 'revenue': 2197.0}, {'customer': "Callaway's Yard & Garden", 'revenue': 1688.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 1581.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1498.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1414.0}, {'customer': 'Zing Quality Furniture Inc', 'revenue': 1373.0}, {'customer': 'Sunset Home and Patio', 'revenue': 1373.0}, {'customer': 'Busch Fireplace', 'revenue': 1236.0}, {'customer': 'Pangaea Patio', 'revenue': 1235.0}, {'customer': 'Philadelphia Botanical Products', 'revenue': 1167.0}, {'customer': 'Patio Style', 'revenue': 686.0}, {'customer': 'Casual Marketplace, Inc.', 'revenue': 0.0}, {'customer': 'Mt.Lake Pool and Patio', 'revenue': 0.0}, {'customer': 'Net Retailers LLC', 'revenue': 0.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 0.0}, {'customer': 'ZLM Enterprises', 'revenue': 0.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 0.0}, {'customer': 'Cape Leisure, Inc.', 'revenue': 0.0}] | [{'item': 'FN61711WTR', 'desc': 'Biltmore Dining Side Chair', 'available': 52}, {'item': 'FN61711PEW-OGY', 'desc': 'Biltmore Dining Side Chair', 'available': 38}, {'item': 'FN61712PEW-OGY', 'desc': 'Biltmore Dining Arm Chair', 'available': 26}, {'item': 'FN61704OGY', 'desc': 'Biltmore Coffee Table', 'available': 24}, {'item': 'FN61716PEW-OGY', 'desc': 'Biltmore Ottoman', 'available': 23}, {'item': 'FN61706PEY-OGY', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 23}, {'item': 'FN61712WTR', 'desc': 'Biltmore Dining Arm Chair', 'available': 19}, {'item': 'FN61704RUB', 'desc': 'Biltmore Coffee Table', 'available': 16}, {'item': 'FN61788PEW-OGY', 'desc': 'Biltmore Swivel Recliner', 'available': 15}, {'item': 'FN61704PEY-OGY', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 12}, {'item': 'FN61703PEW-OGY', 'desc': 'Biltmore Sofa', 'available': 10}, {'item': 'FN61704WLT-RUB', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 7}, {'item': 'FN61701WTR', 'desc': 'Biltmore Club Chair', 'available': 7}, {'item': 'FN61702WTR', 'desc': 'Biltmore Love Seat', 'available': 7}, {'item': 'FN61703WTR', 'desc': 'Biltmore Sofa', 'available': 7}, {'item': 'FN61704HGA', 'desc': 'Biltmore Coffee Table', 'available': 5}, {'item': 'FN61705PEY-OGY', 'desc': 'Biltmore Sintered Stone End Table', 'available': 4}, {'item': 'FN61703WTR-RUB', 'desc': 'Biltmore Sofa', 'available': 2}, {'item': 'FN61706WLT-RUB', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 1}] |
| CU54403 | Lucia Sofa Cushion | COL203 | 127,402 | 248 | 26 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 8133.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 6839.0}, {'customer': 'Northwest Trends', 'revenue': 6599.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 6554.0}, {'customer': 'Country Furniture', 'revenue': 4699.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 4329.0}, {'customer': 'B H Allen Building Centre', 'revenue': 3858.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 3750.0}, {'customer': 'Patio & Home Direct', 'revenue': 3162.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 2783.0}, {'customer': 'DGA Interiors', 'revenue': 2504.0}, {'customer': 'Hue Design LLC', 'revenue': 2310.0}, {'customer': 'Bobby Design Inc.', 'revenue': 2144.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 2067.0}, {'customer': 'We are Sparrow Studio', 'revenue': 1975.0}, {'customer': 'Garden Architecture & Design', 'revenue': 1865.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 1770.0}, {'customer': 'Crystalview', 'revenue': 1727.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 1665.0}, {'customer': 'Touchmark, LLC', 'revenue': 1617.0}, {'customer': 'Wegman Design Group', 'revenue': 1498.0}, {'customer': 'CMS Commercial Furniture', 'revenue': 1487.0}, {'customer': 'Studio 4d', 'revenue': 1467.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 1455.0}, {'customer': 'Direct Supply Inc.', 'revenue': 1455.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 1395.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 1370.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 1282.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 1230.0}, {'customer': 'Studio B Design Group', 'revenue': 1230.0}, {'customer': 'Furniture Solutions Group', 'revenue': 1230.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 1167.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 1131.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1104.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1100.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 1080.0}, {'customer': 'Rattan Wicker & Cane', 'revenue': 959.0}, {'customer': "Bishop's Casual Living", 'revenue': 948.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 940.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 937.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 936.0}, {'customer': 'Sunset Home and Patio', 'revenue': 933.0}, {'customer': 'Patio Productions', 'revenue': 924.0}, {'customer': 'Keca International', 'revenue': 895.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 895.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 877.0}, {'customer': 'Model Home Interiors Inc', 'revenue': 864.0}, {'customer': "Today's Patio", 'revenue': 864.0}, {'customer': 'IDM Development, LLC', 'revenue': 840.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 836.0}, {'customer': 'Cincinnati Pool & Patio', 'revenue': 787.0}, {'customer': 'Abacus Furniture', 'revenue': 768.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 766.0}, {'customer': 'MOI Inc.', 'revenue': 765.0}, {'customer': 'Design Collaborative, Inc.', 'revenue': 765.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 719.0}, {'customer': 'InnVest Hotels Limited', 'revenue': 715.0}, {'customer': 'Kevin Roberts Interiors', 'revenue': 690.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 690.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 690.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 658.0}, {'customer': 'Shop the Studio at Design Mart', 'revenue': 647.0}, {'customer': 'VAI Resort, LLC', 'revenue': 615.0}, {'customer': 'Commonwealth Design Group', 'revenue': 615.0}, {'customer': 'All Backyard Fun', 'revenue': 552.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 540.0}, {'customer': 'Office Revolution LLC', 'revenue': 540.0}, {'customer': 'C.S. Wo & Sons, Ltd', 'revenue': 537.0}, {'customer': 'Piscine Hippocampe', 'revenue': 527.0}, {'customer': 'GST Interiors, LLC', 'revenue': 521.0}, {'customer': "Mio's Furniture Fashions", 'revenue': 497.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 497.0}, {'customer': 'Entreprises H.P. Carignan Inc(mq034', 'revenue': 492.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 492.0}, {'customer': 'Main Street Furniture', 'revenue': 492.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 485.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 469.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 467.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 465.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 453.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 443.0}, {'customer': 'East Texas Brick', 'revenue': 443.0}, {'customer': 'Net Retailers LLC', 'revenue': 432.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 429.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 418.0}, {'customer': 'Veranda Home & Garden Collection', 'revenue': 418.0}, {'customer': 'Patio Comfort', 'revenue': 410.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 397.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 394.0}, {'customer': 'St. Lawrence Pools', 'revenue': 389.0}, {'customer': "Sherri's Living Large", 'revenue': 389.0}, {'customer': 'Beachcomber Hot Tubs & Outdoor Living', 'revenue': 367.0}, {'customer': 'Industrial Revolution', 'revenue': 367.0}, {'customer': 'Real Patio Living Llc', 'revenue': 353.0}, {'customer': 'Georgia Patio Inc', 'revenue': 158.0}, {'customer': 'Americasmart Real Estate LLC', 'revenue': 0.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 0.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 0.0}, {'customer': 'Drew Ruesch Interiors', 'revenue': 0.0}, {'customer': 'Mike Moser Studio', 'revenue': 0.0}] | [{'item': 'CU54458', 'desc': 'Lucia Swivel Rocking Arm Chair Cushion (w/button)', 'available': 2}] |
| FN50063ASG | Limo 84inx42in Rect Dining Table W/uh | COL43 | 125,576 | 180 | 11 | — | [{'customer': 'Studio Dwell', 'revenue': 11241.0}, {'customer': 'Heritage Office Furnishings Ltd.', 'revenue': 8250.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 6799.0}, {'customer': 'Hilton Supply Management', 'revenue': 5198.0}, {'customer': 'Lifestyles By Design, Llc.', 'revenue': 4530.0}, {'customer': 'City of Yorba Linda', 'revenue': 4483.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 3202.0}, {'customer': 'Sonoma Backyard', 'revenue': 3080.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 2450.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 2443.0}, {'customer': 'Net Retailers LLC', 'revenue': 2390.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 2250.0}, {'customer': 'B H Allen Building Centre', 'revenue': 2250.0}, {'customer': 'West Coast Lodging c/o Throughline by IIG (agent)', 'revenue': 2228.0}, {'customer': 'Buffalo-Alafaya Asso. LLC dba Homewood Suites', 'revenue': 2228.0}, {'customer': 'Club Piscine (Terrebonne)', 'revenue': 2125.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2125.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 2098.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1945.0}, {'customer': 'Complete Office LLC', 'revenue': 1800.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 1684.0}, {'customer': 'Homewood Suites By Hilton Covington', 'revenue': 1634.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 1634.0}, {'customer': 'Tharaldson Hospitality Development, LLC', 'revenue': 1634.0}, {'customer': 'Christina River Exchange', 'revenue': 1614.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 1584.0}, {'customer': 'Country Furniture', 'revenue': 1500.0}, {'customer': 'Homewood Mt Pleasant C/O Linked Hospitality', 'revenue': 1485.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 1436.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 1417.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 1358.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 1358.0}, {'customer': 'Hue Design LLC', 'revenue': 1358.0}, {'customer': 'Cash Account', 'revenue': 1250.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1250.0}, {'customer': 'Patio Productions', 'revenue': 1195.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1195.0}, {'customer': 'Bobby Design Inc.', 'revenue': 1042.0}, {'customer': 'Isidore Landscapes Inc.', 'revenue': 1042.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 833.0}, {'customer': 'MV Design Studio', 'revenue': 817.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 817.0}, {'customer': 'Synergy Design & Procurement LLC', 'revenue': 817.0}, {'customer': 'Island Hospitality Management Inc', 'revenue': 817.0}, {'customer': 'Homewood Suites By Hilton Boston', 'revenue': 817.0}, {'customer': 'Design and Construction, Llc c/o The Gettys Group', 'revenue': 817.0}, {'customer': 'DCG Development c/o ACC Design, Inc (Agent)', 'revenue': 817.0}, {'customer': 'Curve Hospitality', 'revenue': 817.0}, {'customer': 'Sourcing Advisors LLC c/o Sourcing Advisor', 'revenue': 817.0}, {'customer': 'Germain Lariviere (1970) Ltee.', 'revenue': 792.0}, {'customer': 'Luxe Furniture Company', 'revenue': 773.0}, {'customer': 'Crystalview', 'revenue': 750.0}, {'customer': "Sherri's Living Large", 'revenue': 750.0}, {'customer': 'Design Therapy Inc', 'revenue': 750.0}, {'customer': 'Patio & Home Direct', 'revenue': 750.0}, {'customer': "Bishop's Casual Living", 'revenue': 750.0}, {'customer': 'Decked Out Home & Patio', 'revenue': 750.0}, {'customer': 'Kathy Andrews Interiors, Inc.', 'revenue': 747.0}, {'customer': 'Studio 4d', 'revenue': 747.0}, {'customer': 'HSI Design Group', 'revenue': 743.0}, {'customer': 'PHG Jackson II, LLC c/o Carver & Asso (Atlanta)', 'revenue': 743.0}, {'customer': 'Dwellings, Llc', 'revenue': 743.0}, {'customer': 'GP Builders, Inc.', 'revenue': 743.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 720.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 708.0}, {'customer': 'Beachcomber Hot Tubs & Outdoor Living', 'revenue': 708.0}, {'customer': 'Kora Home Artistry', 'revenue': 679.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 667.0}, {'customer': 'All American Pool & Patio', 'revenue': 598.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 598.0}, {'customer': 'The Patio Place Inc', 'revenue': 598.0}, {'customer': 'Home Stuff Interiors, Inc', 'revenue': 543.0}, {'customer': 'Canadian Home Leisure', 'revenue': 417.0}, {'customer': "Bowman's Stove & Patio Inc.", 'revenue': 324.0}, {'customer': "Hayward's Of Santa Barbara Inc.", 'revenue': 269.0}, {'customer': 'Sequoia Outback', 'revenue': 245.0}, {'customer': 'BPR Properties c/o Carver and Asso, Atlanta(agent)', 'revenue': 0.0}, {'customer': 'JSM Procurement LLC', 'revenue': 0.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 0.0}, {'customer': 'Carver & Associates', 'revenue': 0.0}, {'customer': 'Homewood Suites-Liverpool, NY c/o HPD(as agent)', 'revenue': 0.0}] | [{'item': 'FN50042TAU', 'desc': 'Limo 30inx60in Rect Counter Table W/uh (HGI)', 'available': 31}, {'item': 'FN50042TWH', 'desc': 'Limo 30inx60in Rect Counter Table W/uh', 'available': 22}, {'item': 'FN50042ASG', 'desc': 'Limo 30inx60in Rect Counter Table W/uh', 'available': 18}, {'item': 'FN50032TWH', 'desc': 'Limo 60in Sq Dining Table W/uh', 'available': 17}, {'item': 'FN50033TWH', 'desc': 'Limo 30inx60in Rect Bar Table W/uh', 'available': 16}, {'item': 'FN50047TWH', 'desc': 'Limo Bench', 'available': 13}, {'item': 'FN50047TWH-L', 'desc': 'Limo Bench (long)', 'available': 13}, {'item': 'FN50036TWH', 'desc': 'Limo 43in Sq Dining Table W/uh', 'available': 11}, {'item': 'FN50063TWH', 'desc': 'Limo 84inx42in Rect Dining Table W/uh', 'available': 8}, {'item': 'FN50047ASG', 'desc': 'Limo Bench', 'available': 6}, {'item': 'FN50066TWH', 'desc': 'Limo 103inx43in Rect Dining Table w/UH', 'available': 4}, {'item': 'FN50047ASG-L', 'desc': 'Limo Bench (long)', 'available': 1}] |
| FN65520WHT | Avenue Lounger | COL145 | 124,576 | 185 | 7 | 2026-6-30 | [{'customer': 'Ellie Aiello Interiors', 'revenue': 23102.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 14167.0}, {'customer': 'The Childs Dreyfus Group', 'revenue': 12601.0}, {'customer': 'Richland Bldg. Partners,LLC c/o The Gettys(agent)', 'revenue': 10781.0}, {'customer': 'Group 4 Design, Inc.', 'revenue': 9801.0}, {'customer': 'Net Retailers LLC', 'revenue': 8007.0}, {'customer': 'Kerry Imagine Designs Llc', 'revenue': 6160.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 3920.0}, {'customer': 'Canadian Resort Hotels Ltd Partner.c/o Sue Dulmage', 'revenue': 3500.0}, {'customer': 'The Patio Place USA, Inc', 'revenue': 3102.0}, {'customer': 'Outdoor Living LLC', 'revenue': 2688.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 2520.0}, {'customer': 'Country Furniture', 'revenue': 2520.0}, {'customer': 'Zing Quality Furniture Inc', 'revenue': 2464.0}, {'customer': 'All American Pool & Patio', 'revenue': 2464.0}, {'customer': 'MTN Mod LLC', 'revenue': 2464.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 2380.0}, {'customer': 'Southport Outdoor Living', 'revenue': 2100.0}, {'customer': 'Treasure Chest LLC', 'revenue': 1540.0}, {'customer': 'Distinctive Designs by Bambi', 'revenue': 1400.0}, {'customer': 'Light House Co.', 'revenue': 1400.0}, {'customer': 'B H Allen Building Centre', 'revenue': 1260.0}, {'customer': 'Keca International', 'revenue': 1190.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 1120.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 665.0}, {'customer': 'Crystalview', 'revenue': 630.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 630.0}] | [{'item': 'FN65505WHT', 'desc': 'Avenue Side Table', 'available': 27}, {'item': 'FN65505BLK', 'desc': 'Avenue Side Table', 'available': 24}] |
| UM00907BRZ/C | 9' Alum W/fiberglass Ribs,pulley,2 Poles W/canopy | COL73 | 121,687 | 333 | 31 | — | [{'customer': 'Le Chateau Montebello, Evergrande Hotel Hold', 'revenue': 26102.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 14405.0}, {'customer': 'Embarc Members Association', 'revenue': 11230.0}, {'customer': 'Urban Design Studio', 'revenue': 8392.0}, {'customer': 'Interior Motives', 'revenue': 7122.0}, {'customer': 'Shaughnessy Golf And Country Club', 'revenue': 4976.0}, {'customer': 'Country Furniture', 'revenue': 4190.0}, {'customer': 'Williams Group', 'revenue': 3749.0}, {'customer': 'Elite Contract Furniture Ltd', 'revenue': 3553.0}, {'customer': "Les Plantes D'interieur Veronneau", 'revenue': 3480.0}, {'customer': 'Hampton Inn Phoenix/Anthem', 'revenue': 3450.0}, {'customer': 'Northwest Trends', 'revenue': 3345.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 3303.0}, {'customer': 'Evercare Contract Furnishings Inc.', 'revenue': 3215.0}, {'customer': 'Era Living LLC', 'revenue': 3209.0}, {'customer': 'Terminal City Club', 'revenue': 3045.0}, {'customer': 'Embarc Members Association', 'revenue': 2610.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 2117.0}, {'customer': 'Kerry Imagine Designs Llc', 'revenue': 1783.0}, {'customer': 'Hue Design LLC', 'revenue': 1586.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1550.0}, {'customer': 'Harris Furniture & Antiques Inc.', 'revenue': 1044.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 690.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 690.0}, {'customer': 'Homey Home', 'revenue': 435.0}, {'customer': 'Cardinal Design and Procurement', 'revenue': 385.0}, {'customer': 'Atmosphere Commercial Interiors', 'revenue': 345.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 331.0}, {'customer': 'Patio & Home Direct', 'revenue': 326.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 323.0}, {'customer': 'Starland Property Co, LLC', 'revenue': 300.0}, {'customer': 'Club Piscines Sherbrooke', 'revenue': 206.0}, {'customer': 'Intown Ace Hardware', 'revenue': 200.0}, {'customer': 'Montage Hotels & Resorts', 'revenue': 0.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}] | [{'item': 'UM01010SLV-CCL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Cloud canopy", 'available': 10}, {'item': 'UM01010SLV-CBL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Black canopy", 'available': 9}, {'item': 'UM01004SLV/C', 'desc': "10' Sq Deluxe Alum Umbrella, 48mm Pole W/canopy", 'available': 8}, {'item': 'UM00906BRZ/C', 'desc': "9' Alum W/fiber Ribs,crank Lift,collar Tilt,canopy", 'available': 6}, {'item': 'UM00909POLE-BRZ', 'desc': '45in Bar Bottom Pole for UM00906BRZ/C', 'available': 5}] |

### Q-ORG-NEWITEM_results.md

(not present — file does not exist or is empty)
