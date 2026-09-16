# Section 3 Context Bundle — Currey & Company (cci)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=57730, portal_order_gmv=$87.6M |
| HAS_INVENTORY | True | inventory_count=3443 |
| HAS_SALES_DATA | True | sales_data_count=110748 |
| HAS_SALES_SECTION | True | mode=orders order_reps=37 engagement_reps=0 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$87.6M > ecat_gmv=$8.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 37 | 37 |
| ENGAGEMENT_REP_COUNT | 0 |  |
| SALES_SECTION_MODE | orders | orders |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 76 rows |
| SHOWROOM_EXCLUSIONS | 3 | 3 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3985, Mixpanel total submit_order (Q-01): 6616 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.4%, ambiguous_rate=0.0%, showroom_event_share=8.5% |
| USER_GROUP_JOIN_RATE | 97% | 74 of 76 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 9% | showroom+admin share of matched events: 8.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Atlanta Showroom, CC Dallas Showroom, Highpoint Showroom, Allan Otto |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=2 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=53 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=7906 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=369 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=3184 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Currey & Company
- **Shortname**: cci
- **Org ID**: 161
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Currey & Company (cci, org_id=161)
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

# Signal Rank — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Total signals fired**: 56 (P0: 34, P1: 21, P2: 1)
- **Org GMV**: $8.6M eCat LTM, $87.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 8 reps at 0% eCat capture on $31.5M total business | P1 | §5 Team | 252.0 | $31,500,000 | 2.0 | 15,876,000,000 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — 9000-0135/9000-0143 co-purchase pattern across 77 customers | P0 | §2/§3 | 7.7 | $32,879,194 | 2.0 | 506,339,588 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $13.9M+ total business, zero eCat orders | P1 | §2 Accounts | 13.9 | $13,861,823 | 2.0 | 384,300,274 | POSITIVE |
| 4 | SIG-COMMERCE-01 | Capture Rate — eCat captures 9.8% of $88M total business; each +1pt = $876K | P0 | §4 Commerce | 4.5 | $876,000 | 3.0 | 11,850,000 | POSITIVE |
| 5 | SIG-MOM-01 | Account Acceleration — LILLIAN JAMES DESIGN GROUP 4 consecutive QoQ acceleration quarters, $110,380 peak quarter (+934% QoQ) | P0 | §2 Accounts | 31.1 | $110,380 | 3.0 | 10,312,818 | POSITIVE |
| 6 | SIG-ANOMALY-03 | Competitive Displacement — DEFINED INTERIORS total biz +541% but eCat -100% | P0 | §2 Accounts | 42.7 | $57,855 | 3.0 | 7,413,567 | RISK |
| 7 | SIG-MOM-01 | Account Acceleration — BAY DESIGN 3 consecutive QoQ acceleration quarters, $78,913 peak quarter (+925% QoQ) | P0 | §2 Accounts | 30.8 | $78,913 | 3.0 | 7,298,634 | POSITIVE |
| 8 | SIG-MOM-01 | Account Acceleration — WILSON LIGHTING - OVERLAND PRK 2 consecutive QoQ acceleration quarters, $77,581 peak quarter (+616% QoQ) | P0 | §2 Accounts | 20.5 | $77,581 | 3.0 | 4,779,784 | POSITIVE |
| 9 | SIG-MOM-01 | Account Acceleration — WESTEND PROPERTIES LTD 2 consecutive QoQ acceleration quarters, $112,801 peak quarter (+404% QoQ) | P0 | §2 Accounts | 13.5 | $112,801 | 3.0 | 4,553,775 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — CROMWELL AUSTRALIA PTY LTD 2 consecutive QoQ acceleration quarters, $100,868 peak quarter (+418% QoQ) | P0 | §2 Accounts | 13.9 | $100,868 | 3.0 | 4,218,293 | POSITIVE |
| 11 | SIG-DECAY-04 | Spending Contraction — BEYOND INC -77.4% YoY ($306,714→$69,264), $237,450 gap | P0 | §2 Accounts | 3.9 | $237,450 | 3.0 | 2,756,791 | RISK |
| 12 | SIG-DECAY-04 | Spending Contraction — DESIGNSOURCE INTERNATIONAL -70.8% YoY ($327,412→$95,532), $231,880 gap | P0 | §2 Accounts | 3.5 | $231,880 | 3.0 | 2,462,566 | RISK |
| 13 | SIG-MOM-01 | Account Acceleration — ROBB & STUCKY INTERNATIONAL 2 consecutive QoQ acceleration quarters, $96,623 peak quarter (+187% QoQ) | P0 | §2 Accounts | 6.2 | $96,623 | 3.0 | 1,806,850 | POSITIVE |
| 14 | SIG-DECAY-04 | Spending Contraction — LAMPS.COM -55.3% YoY ($324,958→$145,295), $179,663 gap | P0 | §2 Accounts | 2.8 | $179,663 | 3.0 | 1,490,306 | RISK |
| 15 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 53% of eCat GMV | P1 | §4 Commerce | 1.3 | $541,073 | 2.0 | 1,431,238 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — CAI DESIGNS 2 consecutive QoQ acceleration quarters, $133,301 peak quarter (+105% QoQ) | P0 | §2 Accounts | 3.5 | $133,301 | 3.0 | 1,394,326 | POSITIVE |
| 17 | SIG-MOM-01 | Account Acceleration — FURNITURELAND SOUTH 2 consecutive QoQ acceleration quarters, $139,458 peak quarter (+98% QoQ) | P0 | §2 Accounts | 3.3 | $139,458 | 3.0 | 1,363,902 | POSITIVE |
| 18 | SIG-ANOMALY-03 | Competitive Displacement — ROBB & STUCKY INTERNATIONAL total biz +55% but eCat -20% | P0 | §2 Accounts | 5.0 | $88,611 | 3.0 | 1,329,164 | RISK |
| 19 | SIG-DECAY-03 | Rep Trajectory — Rip Nance orders -37.9% QoQ, $105,764 current 90d GMV | P1 | §5 Team | 1.5 | $423,056 | 2.0 | 1,282,706 | RISK |
| 20 | SIG-DECAY-03 | Rep Trajectory — Atlanta Showroom orders -40.5% QoQ, $92,410 current 90d GMV | P1 | §5 Team | 1.6 | $369,640 | 2.0 | 1,197,634 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 33 | 1 | 0 | 34 | |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 8 | 0 | 8 | |
| §6 Platform Context | 0 | 11 | 0 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 8 reps at 0% eCat capture on $31.5M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 9000-0135/9000-0143 co-purchase pattern across 77 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $13.9M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 9.8% of $88M total business; each +1pt = $876K
5. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — DEFINED INTERIORS total biz +541% but eCat -100%
6. **[RISK]** SIG-DECAY-04: Spending Contraction — BEYOND INC -77.4% YoY ($306,714→$69,264), $237,450 gap
7. **[RISK]** SIG-DECAY-04: Spending Contraction — DESIGNSOURCE INTERNATIONAL -70.8% YoY ($327,412→$95,532), $231,880 gap

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 2
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| hidden | 2,736 | 277 | 2 | 89.90 |
| visible | 3,394 | 144 | 17 | 95.80 |

### Q-37_results.md

# Q-37 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9000-1130 | LIGCHANDELIER | — | Nottaway Grande Bronze Chandelier | $872,209 | 413 | 0 | 0 | 0 | 2026-7-18 |
| 9000-0438 | LIGCHANDELIER | AVIVA STANOFF | Forest Dawn Gold Chandelier | $872,115 | 201 | 0 | 0 | 0 | 2026-7-18 |
| 3000-0004 | FURCABINETS&C | — | Briallen Black Demi-Lune Cabinet | $608,552 | 321 | 0 | 0 | 0 | 2026-7-18 |
| 5000-0064 | LIGWALLSCONCE | BUNNY WILLIAMS | Malvasia Brass Wall Sconce | $526,416 | 1,642 | 0 | 0 | 0 | 2026-7-18 |
| 9000-1129 | LIGCHANDELIER | — | Nottaway Two-Tier Bronze Chandelier | $490,391 | 349 | 0 | 0 | 0 | 2026-7-18 |
| 4000-0118 | FURTABLES | — | Abu Gold Accent Table | $314,439 | 923 | 0 | 0 | 0 | 2026-8-17 |
| 9000-0901 | LIGMULTI-DROP | — | Lazio 36-Light Round Multi-Drop Pendant | $278,980 | 35 | 0 | 0 | 0 | — |
| 9000-1255 | LIGCHANDELIER | — | Nottaway Grande Gold Chandelier | $276,925 | 126 | 0 | 0 | 0 | 2026-8-17 |
| 9000-1234 | LIGCHANDELIER | — | Electra Chandelier | $274,995 | 196 | 0 | 0 | 0 | 2026-8-17 |
| 3000-0247 | FURCABINETS&C | — | Kallista Blue Credenza | $274,980 | 105 | 0 | 0 | 0 | 2026-7-18 |
| 3000-0142 | FURCABINETS&C | — | Evie Shagreen Credenza | $265,727 | 109 | 0 | 0 | 0 | 2026-8-17 |
| 3000-0280 | FURCABINETS&C | — | Briallen Blue Demi-Lune Cabinet | $264,966 | 143 | 0 | 0 | 0 | 2026-8-17 |
| 9000-1235 | LIGCHANDELIER | — | Electra Three-Tier Chandelier | $237,674 | 56 | 0 | 0 | 0 | 2026-12-15 |
| 8000-0071 | LIGFLOORLAMPS | — | Tropical Large Brass Floor Lamp | $226,379 | 164 | 0 | 0 | 0 | 2026-8-17 |
| 6000-0601 | LIGTABLELAMPS | — | Greenlea Gray Table Lamp | $220,405 | 846 | 0 | 0 | 0 | 2026-8-17 |
| 9000-1018 | LIGMULTI-DROP | — | Pathos 36-Light Round Multi-Drop Pendant | $215,227 | 49 | 0 | 0 | 0 | — |
| 6000-0218 | LIGTABLELAMPS | — | Cait Green Table Lamp | $211,793 | 782 | 0 | 0 | 0 | 2026-8-17 |
| 3000-0082 | FURCABINETS&C | — | Kallista Blue Cabinet | $211,040 | 95 | 0 | 0 | 0 | 2026-8-17 |
| 9000-0407 | LIGPENDANTS | — | Weybright Brass Pendant | $209,143 | 421 | 0 | 0 | 0 | 2026-8-17 |
| 3000-0141 | FURCHESTS&NIG | — | Evie Shagreen Chest | $203,859 | 132 | 0 | 0 | 0 | 2026-8-17 |

### Q-38a_results.md

# Q-38a Results — Currey & Company (cci, org_id=161)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16655
- **Run date**: 2026-06-17


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
| /M | — | — | — | 2026-03-01 | 0 | 2 |
| /M | — | — | — | 2026-04-01 | 0 | 2 |
| /M | — | — | — | 2026-05-01 | 0 | 1 |
| /MISC | — | — | — | 2026-03-01 | 0 | 1 |
| /MISC | — | — | — | 2026-05-01 | 0 | 1 |
| 0009-BEI | — | — | — | 2026-05-01 | 1 | 1 |
| 0020-OWH | — | — | — | 2026-02-01 | 2 | 2 |
| 0045-BEIS | — | — | — | 2026-01-01 | 1 | 1 |
| 0045-BEIS | — | — | — | 2026-05-01 | 1 | 1 |
| 0100-0006 | 8' Contemporary Gold Leaf Chain | LIGADDITIONAL | — | 2026-04-01 | 3 | 2 |
| 0100-0048 | 3' Painted Gesso Chain | LIGADDITIONAL | — | 2026-02-01 | 1 | 1 |
| 0100-0048 | 3' Painted Gesso Chain | LIGADDITIONAL | — | 2026-03-01 | 1 | 1 |
| 0100-0054 | 8' Satin Black Chain | LIGADDITIONAL | — | 2026-04-01 | 1 | 1 |
| 0100-0056 | 3' Antique Gold Leaf Chain | LIGADDITIONAL | — | 2026-01-01 | 1 | 1 |
| 0100-0059 | 6' Chinois Textured Black Chain | LIGADDITIONAL | — | 2026-03-01 | 1 | 1 |
| 0100-0061 | 6' Gold Leaf Chain | LIGADDITIONAL | — | 2026-06-01 | 1 | 1 |
| 0100-0066 | 8' Bronze Gold Chain | LIGADDITIONAL | — | 2026-01-01 | 1 | 1 |
| 0100-0066 | 8' Bronze Gold Chain | LIGADDITIONAL | — | 2026-05-01 | 1 | 1 |
| 0100-0069 | 3' Brass Chain | LIGADDITIONAL | — | 2026-02-01 | 2 | 2 |
| 0100-0069 | 3' Brass Chain | LIGADDITIONAL | — | 2026-03-01 | 7 | 4 |
| 0100-0069 | 3' Brass Chain | LIGADDITIONAL | — | 2026-04-01 | 4 | 4 |
| 0100-0069 | 3' Brass Chain | LIGADDITIONAL | — | 2026-05-01 | 3 | 3 |
| 0100-0069 | 3' Brass Chain | LIGADDITIONAL | — | 2026-06-01 | 2 | 1 |
| 0100-0070 | 8' Painted Gesso White Chain | LIGADDITIONAL | — | 2026-02-01 | 1 | 1 |
| 0100-0090 | 6' Vintage Brass Chain | LIGADDITIONAL | — | 2025-12-01 | 2 | 1 |
| 0100-0090 | 6' Vintage Brass Chain | LIGADDITIONAL | — | 2026-01-01 | 4 | 1 |
| 0100-0090 | 6' Vintage Brass Chain | LIGADDITIONAL | — | 2026-03-01 | 1 | 1 |
| 0100-0090 | 6' Vintage Brass Chain | LIGADDITIONAL | — | 2026-05-01 | 2 | 1 |
| 0100-0090 | 6' Vintage Brass Chain | LIGADDITIONAL | — | 2026-06-01 | 1 | 1 |
| 0100-0096 | 3' Antique Black Chain | LIGADDITIONAL | — | 2026-03-01 | 7 | 1 |
| 0100-0096 | 3' Antique Black Chain | LIGADDITIONAL | — | 2026-04-01 | 2 | 1 |
| 0100-0099 | 6' Washed Black Chain | LIGADDITIONAL | — | 2026-02-01 | 2 | 1 |
| 0100-0103 | 6' Antique Silver Leaf Chain | LIGADDITIONAL | — | 2026-02-01 | 2 | 1 |
| 0100-0103 | 6' Antique Silver Leaf Chain | LIGADDITIONAL | — | 2026-04-01 | 1 | 1 |
| 0100-0106 | 8' Khaki Chain | LIGADDITIONAL | — | 2026-01-01 | 1 | 1 |
| 0100-0106 | 8' Khaki Chain | LIGADDITIONAL | — | 2026-04-01 | 1 | 1 |
| 0100-0106 | 8' Khaki Chain | LIGADDITIONAL | — | 2026-05-01 | 1 | 1 |
| 0100-0106 | 8' Khaki Chain | LIGADDITIONAL | — | 2026-06-01 | 1 | 1 |
| 0100-0107 | 3' Light Mole Chain | LIGADDITIONAL | — | 2025-12-01 | 1 | 1 |
| 0100-0110 | 3' Rustic Bronze Chain | LIGADDITIONAL | — | 2026-03-01 | 1 | 1 |
| 0100-0110 | 3' Rustic Bronze Chain | LIGADDITIONAL | — | 2026-05-01 | 9 | 2 |
| 0100-0114 | 6' Antique Brass Chain | LIGADDITIONAL | — | 2025-12-01 | 1 | 1 |
| 0100-0114 | 6' Antique Brass Chain | LIGADDITIONAL | — | 2026-01-01 | 6 | 2 |
| 0100-0114 | 6' Antique Brass Chain | LIGADDITIONAL | — | 2026-02-01 | 2 | 2 |
| 0100-0114 | 6' Antique Brass Chain | LIGADDITIONAL | — | 2026-03-01 | 2 | 2 |
| 0100-0114 | 6' Antique Brass Chain | LIGADDITIONAL | — | 2026-04-01 | 1 | 1 |
| 0100-0114 | 6' Antique Brass Chain | LIGADDITIONAL | — | 2026-05-01 | 3 | 2 |
| 0100-0115 | 6' Antique Silver Leaf Chain | LIGADDITIONAL | — | 2026-02-01 | 1 | 1 |
| 0100-0117 | 6' Contemporary Silver Leaf Chain | LIGADDITIONAL | — | 2026-04-01 | 1 | 1 |
| 0100-0130 | 6' White Chain | LIGADDITIONAL | — | 2026-02-01 | 8 | 2 |

*(Truncated: showing top 50 of 16655 rows. Full data in cache file.)*

### Q-39_category_results.md

# Q-39-cat Results — Currey & Company (cci, org_id=161)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 37
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| LIGCHANDELIER | $55.1M | 53,085 | 485 | $113,582 |
| LIGTABLELAMPS | $15.0M | 49,495 | 313 | $48,081 |
| LIGWALLSCONCE | $11.8M | 33,887 | 261 | $45,137 |
| LIGPENDANTS | $10.0M | 17,785 | 124 | $80,949 |
| LIGMULTI-DROP | $5.9M | 5,188 | 227 | $26,171 |
| FURTABLES | $5.7M | 13,679 | 174 | $32,952 |
| LIGSEMI-FLUSH | $5.1M | 6,819 | 61 | $84,099 |
| LIGFLOORLAMPS | $4.8M | 8,217 | 78 | $61,771 |
| FURCABINETS&C | $3.6M | 1,609 | 21 | $171,690 |
| LIGLANTERNS | $2.9M | 3,273 | 41 | $71,324 |
| LIGFLUSHMOUNT | $2.8M | 5,145 | 35 | $80,906 |
| ACCMIRRORS | $2.7M | 3,863 | 59 | $46,000 |
| FURCHESTS&NIG | $2.2M | 1,720 | 22 | $100,991 |
| OUTSEATING | $2.0M | 1,832 | 18 | $110,113 |
| ACCOBJECTS&SC | $1.6M | 6,292 | 109 | $15,018 |
| ACCVASESJARS& | $1.4M | 6,654 | 142 | $9,965 |
| ACCBOXES&TRAY | $1.2M | 5,284 | 89 | $13,001 |
| FURDESKS&VANI | $926,360 | 544 | 12 | $77,197 |
| FURBATHVANITI | $806,019 | 315 | 20 | $40,301 |
| OUTTABLES | $501,696 | 874 | 16 | $31,356 |
| FURACCENTPIEC | $454,118 | 439 | 13 | $34,932 |
| FUROTTOMANS&B | $440,186 | 444 | 12 | $36,682 |
| FURACCENTCHAI | $408,197 | 355 | 14 | $29,157 |
| OUTPLANTERS | $351,257 | 675 | 27 | $13,010 |
| FURBAR&COUNTE | $319,879 | 329 | 7 | $45,697 |
| LIGADDITIONAL | $190,268 | 5,424 | 197 | $966 |
| OUTACCESSORIE | $144,103 | 305 | 7 | $20,586 |
| LIGBATHBARS | $82,921 | 75 | 3 | $27,640 |
| FURDININGCHAI | $59,302 | 77 | 1 | $59,302 |
| LIGLIGHTBULBS | $57,440 | 3,860 | 5 | $11,488 |
| LIGLAMPSHADES | $35,562 | 232 | 21 | $1,693 |
| FURHARDWARE | $28,499 | 176 | 3 | $9,500 |
| FURGLASSTOPS | $8,241 | 62 | 4 | $2,060 |
| LIGCORDLESSLI | $8,049 | 232 | 11 | $732 |
| LIGPICTURELIG | $3,485 | 9 | 1 | $3,485 |
| FURBATHVANITY | $3,394 | 50 | 3 | $1,131 |
| LIG | $216 | 12 | 1 | $216 |

### Q-39_collection_results.md

# Q-39-col Results — Currey & Company (cci, org_id=161)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 12
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| BUNNY WILLIAMS | $3.1M | 4,742 | 22 | $139,322 |
| AVIVA STANOFF | $2.6M | 1,031 | 11 | $238,501 |
| SUZANNE DUIN | $2.0M | 3,706 | 23 | $87,330 |
| MARJORIE SKOURAS | $1.9M | 1,571 | 29 | $65,064 |
| LILLIAN AUGUST | $618,133 | 815 | 6 | $103,022 |
| BARRY GORALNICK | $617,636 | 1,593 | 8 | $77,205 |
| HIROSHI KOSHITAKA | $564,836 | 385 | 7 | $80,691 |
| WINTERTHUR | $515,931 | 509 | 7 | $73,704 |
| JAMIE BECKWITH | $316,858 | 415 | 4 | $79,214 |
| PHYLLIS MORRIS | $234,870 | 221 | 2 | $117,435 |
| DENISE MCGAHA | $120,693 | 114 | 1 | $120,693 |
| SASHA BIKOFF | $89,161 | 81 | 1 | $89,161 |

### Q-42_results.md

# Q-42 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 2
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| — | 1,442 | $540,063 | 869 | $375 |
| BUNNY WILLIAMS | 11 | $2,042 | 7 | $186 |

### Q-59_results.md

# Q-59 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORG_SUMMARY | — | — | — | 81.70 | 27,584 | — | — | — | — | — | — |

### Q-61_results.md

# Q-61 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9000-1426 | Winterberry Chandelier | LIGCHANDELIER | 26 | 30 | 82,680 | 30 | 6,240 |
| 9000-1439 | Magnum Opus Medium Chandelier | LIGCHANDELIER | 22 | 24 | 79,581.25 | 24 | 7,490 |
| 9000-1430 | Oblivion Chandelier | LIGCHANDELIER | 47 | 48 | 74,617.20 | 47 | 3,240 |
| 9000-1475 | Glazen Tulpen Chandelier | LIGCHANDELIER | 22 | 24 | 54,091.60 | 23 | 4,990 |
| 9000-1440 | Crystal Bud Large Ring Chandelier | LIGCHANDELIER | 12 | 13 | 45,303.30 | 13 | 7,990 |
| 9000-1432 | Weston Oval Chandelier | LIGCHANDELIER | 23 | 25 | 41,700.80 | 25 | 3,890 |
| 9000-1438 | Leda Chandelier | LIGCHANDELIER | 14 | 14 | 40,688.80 | 14 | 7,240 |
| 9000-1437 | Odile Chandelier | LIGCHANDELIER | 11 | 13 | 40,402.20 | 12 | 6,990 |
| 3000-0339 | Evie Large Burl Credenza | FURCABINETS&C | 12 | 12 | 35,806.20 | 13 | 7,190 |
| 9000-1443 | Seaward Extra Large Chandelier | LIGCHANDELIER | 10 | 11 | 34,454 | 10 | 7,490 |
| 9000-1454 | Electra Oval Chandelier | LIGCHANDELIER | 9 | 9 | 30,259.60 | 9 | 7,490 |
| 3000-0346 | Virtuosity Bar Cabinet | FURACCENTPIEC | 11 | 11 | 28,527.80 | 11 | 5,740 |
| 9000-1479 | Volterra Three-Tier Chandelier | LIGCHANDELIER | 11 | 12 | 26,420.80 | 12 | 6,740 |
| 3000-0341 | Evie Burl Chest | FURCHESTS&NIG | 8 | 14 | 26,404 | 10 | 4,600 |
| 3000-0343 | Evie Burl Writing Desk | FURDESKS&VANI | 12 | 14 | 23,438.40 | 15 | 4,560 |
| 3000-0345 | Virtuosity Credenza | FURCABINETS&C | 5 | 5 | 22,906 | 5 | 8,810 |
| 6000-1108 | Kora Large Blue Table Lamp | LIGTABLELAMPS | 16 | 23 | 21,696 | 16 | 1,920 |
| 8000-0187 | Galuchat Green Hourglass Floor Lamp | LIGFLOORLAMPS | 28 | 35 | 21,023.90 | 31 | 1,490 |
| 2000-0052 | Dunmore Medium Bench | OUTSEATING | 6 | 7 | 20,784.75 | 7 | 7,490 |
| 9000-1463 | Woodcroft Chandelier | LIGCHANDELIER | 17 | 18 | 20,644.80 | 17 | 2,640 |
| 9000-1431 | Capheira Chandelier | LIGCHANDELIER | 7 | 12 | 20,384.60 | 12 | 4,490 |
| 9000-1469 | Mallow Empire Chandelier | LIGCHANDELIER | 11 | 13 | 19,672.40 | 13 | 3,740 |
| 4000-0269 | Toth C Table | FURTABLES | 35 | 49 | 19,507.95 | 43 | 990 |
| 6700-0037 | Daphne Green Cordless Table Lamp | LIGTABLELAMPS | 25 | 76 | 19,129.60 | 26 | 610 |
| 1000-0183 | Jericho Mirror | ACCMIRRORS | 19 | 29 | 18,385.98 | 28 | 1,590 |
| 9000-1467 | Mallow Medium Chandelier | LIGCHANDELIER | 14 | 14 | 18,204.40 | 14 | 2,840 |
| 9000-1459 | Whirlwind Medium Pink Chandelier | LIGCHANDELIER | 17 | 19 | 18,188.60 | 19 | 1,990 |
| 9000-1433 | Lunaria Gold Oval Chandelier | LIGCHANDELIER | 18 | 19 | 17,920.80 | 19 | 2,280 |
| 9500-0031 | Cabo Medium Outdoor Pendant | LIGPENDANTS | 10 | 15 | 16,264 | 10 | 2,140 |
| 6000-1096 | Tribute Table Lamp | LIGTABLELAMPS | 13 | 28 | 16,023 | 13 | 1,470 |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6000-1118 | Entasis Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "BLU D'OR INTERIORS", 'revenue': None}, {'customer': 'KENNEDY GALLERIES', 'revenue': None}, {'customer': 'PLUM & CRIMSON FINE INT. DSGN.', 'revenue': None}, {'customer': 'SHRAWDER RESTORATIONS', 'revenue': None}] | — |
| 6700-0031 | Navigation Brown Cordless Table Lamp | — | — | — | — | 2026-9-16 | [{'customer': 'TIKALOVA', 'revenue': None}, {'customer': 'SWANK DESIGN', 'revenue': None}, {'customer': 'WESTON LYONS DESIGN', 'revenue': None}, {'customer': 'DISTINCTIVE IMAGE', 'revenue': None}, {'customer': 'UP COUNTRY HOME', 'revenue': None}, {'customer': 'UNIVERSAL LAMP MFG.', 'revenue': None}] | — |
| 3000-0346 | Virtuosity Bar Cabinet | — | — | — | — | 2026-7-18 | [{'customer': 'HEARTH AND SOUL', 'revenue': None}, {'customer': 'KUDZU AND COMPANY', 'revenue': None}, {'customer': "O'SHEA AND CO", 'revenue': None}, {'customer': 'THE CHANDLERY', 'revenue': None}, {'customer': 'ACCESSORIES, ETC - SAVANNAH', 'revenue': None}] | — |
| 6000-1089 | Betel Nut White Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': 'EAST END INTERIORS', 'revenue': None}] | — |
| 6000-1115 | Dossier Desk Lamp | — | — | — | — | 2026-9-16 | [{'customer': "REID'S FINE FURNISHINGS", 'revenue': None}, {'customer': 'ACCOMMODATION ACCOUNT', 'revenue': None}] | — |
| 9000-0824 | Denison Medium White Lantern | — | — | — | — | 2026-12-15 | [{'customer': 'CAITLIN KAH INTERIORS', 'revenue': None}, {'customer': 'BEATA BUHL INTERIORS', 'revenue': None}] | — |
| 9742 | Longhope Rectangular Chandelier | — | — | — | — | 2026-12-15 | [{'customer': 'LUXE HOME COMPANY', 'revenue': None}] | — |
| 1200-1167 | Sylva Medium White Vase | — | — | — | — | 2026-8-17 | [{'customer': 'ACCENTS FOR LIVING', 'revenue': None}, {'customer': 'HOME OUTFITTERS', 'revenue': None}, {'customer': 'LADCO', 'revenue': None}, {'customer': 'VERDALEE', 'revenue': None}] | — |
| 6000-0612 | Sonoran Table Lamp | — | — | — | — | — | [{'customer': 'MCGEE & CO', 'revenue': None}] | — |
| 6700-0044 | Volley Brass Cordless Table Lamp | — | — | — | — | 2026-7-18 | [{'customer': 'PAMELA GAYLIN RYDER INTERIORS', 'revenue': None}] | — |
| 5000-0320 | Grigsby Double-Light Wall Sconce | — | — | — | — | 2026-12-15 | [{'customer': 'HOWARD HOUSE INTERIORS', 'revenue': None}, {'customer': 'HAUTE HOUSE INTERIORS', 'revenue': None}] | — |
| 9000-1484 | Faraday Chandelier | — | — | — | — | 2026-12-15 | [{'customer': 'DANA MCKENNA DESIGNS', 'revenue': None}, {'customer': 'STEVEN SHELL LIVING', 'revenue': None}, {'customer': 'INTERIOR MOTIVES', 'revenue': None}, {'customer': 'MILIEU AND YOU', 'revenue': None}, {'customer': 'ACCENTS FOR LIVING', 'revenue': None}, {'customer': 'BELLISSIMO', 'revenue': None}, {'customer': 'CARTER & COMPANY', 'revenue': None}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': None}] | — |
| 6000-1095 | Uroko Table Lamp | — | — | — | — | 2026-7-18 | [{'customer': 'J F FABRICS', 'revenue': None}, {'customer': 'LOST CREEK RANCH', 'revenue': None}, {'customer': 'MATTER BROTHERS  FURNITURE', 'revenue': None}] | — |
| 6700-0040 | Wander Antique Silver Cordless Table Lamp | BUNNY WILLIAMS | — | — | — | 2026-7-18 | [{'customer': 'AB HOME', 'revenue': None}, {'customer': 'THE CHANDLERY', 'revenue': None}] | [{'item': '5000-0188', 'desc': 'Bette Gold Wall Sconce', 'available': 111}, {'item': '9000-0186', 'desc': 'Bette Gold Chandelier', 'available': 85}, {'item': '9999-0024', 'desc': 'Biddulph Gold Semi-Flush Mount', 'available': 71}, {'item': '5000-0067', 'desc': 'Westley Wall Sconce', 'available': 42}, {'item': '6700-0034', 'desc': 'Valise Cordless Table Lamp', 'available': 41}, {'item': '5900-0047', 'desc': 'Warwick Tall Wall Sconce', 'available': 33}, {'item': '9000-0187', 'desc': 'Belle Gold Chandelier', 'available': 30}, {'item': '9000-0991', 'desc': 'Augustus Small Chandelier', 'available': 29}, {'item': '9000-1296', 'desc': 'Bradshaw Lantern', 'available': 26}, {'item': '5000-0283', 'desc': 'Bradshaw Wall Sconce', 'available': 22}, {'item': '5000-0072', 'desc': 'Wallis Wall Sconce', 'available': 18}, {'item': '9000-1295', 'desc': 'Bradshaw Chandelier', 'available': 16}, {'item': '9000-1217', 'desc': 'Wycombe Lantern', 'available': 15}, {'item': '9000-0775', 'desc': 'Bailey Black Chandelier', 'available': 15}, {'item': '9000-0776', 'desc': 'Bebe Chandelier', 'available': 11}, {'item': '5000-0187', 'desc': 'Warwick Wall Sconce', 'available': 10}, {'item': '9000-0181', 'desc': 'Berkeley Chandelier', 'available': 5}] |
| 6700-0029 | Springe Ivory Cordless Table Lamp | — | — | — | — | 2026-9-16 | [{'customer': 'FIVE WEST INTERIORS', 'revenue': None}, {'customer': 'HOLIDAY BEACH DECOR', 'revenue': None}, {'customer': "O'SHEA AND CO", 'revenue': None}, {'customer': 'DECORATIVE CIRCLE', 'revenue': None}, {'customer': 'GREEN FRONT FURNITURE', 'revenue': None}, {'customer': 'UP COUNTRY HOME', 'revenue': None}] | — |
| 4000-0285 | Spalzato Demi-Lune Console Table | — | — | — | — | 2026-8-17 | [{'customer': 'ACP HOME INTERIORS', 'revenue': None}, {'customer': 'BRUMBAUGHS', 'revenue': None}] | — |
| 6700-0025 | Odyssey Large Cordless Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "BLU D'OR INTERIORS", 'revenue': None}, {'customer': 'KUDZU AND COMPANY', 'revenue': None}, {'customer': 'BEARDEN DESIGN', 'revenue': None}, {'customer': 'BARCLAY BUTERA INC', 'revenue': None}, {'customer': 'FEATHERS CUSTOM FURNITURE, INC', 'revenue': None}, {'customer': 'HYDE PARK INTERIORS', 'revenue': None}, {'customer': 'KNIGHT CARR & COMPANY', 'revenue': None}, {'customer': 'UP COUNTRY HOME', 'revenue': None}] | — |
| 6000-1120 | Blanche Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "BRAGG'S OF HUNTSVILLE", 'revenue': None}, {'customer': 'EAST END INTERIORS', 'revenue': None}, {'customer': 'MATTER BROTHERS  FURNITURE', 'revenue': None}] | — |
| 6000-1100 | Pinion Table Lamp | — | — | — | — | 2026-7-18 | [{'customer': 'DESIGNING WOMEN, INC.- HICKORY', 'revenue': None}] | — |
| 6000-1122 | Heaven Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "GMJ dba ROOSTER'S NEST", 'revenue': None}, {'customer': "BAER' S FURNITURE COMPANY", 'revenue': None}, {'customer': 'THE QUIET MOOSE', 'revenue': None}, {'customer': 'SEDLAK INTERIORS', 'revenue': None}] | — |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 6700-0039 | Wander Antique Brass Cordless Table Lamp | BUNNY WILLIAMS | 1 | 0 | [{'customer_code': 'WAYFAIR', 'customer_name': 'WAYFAIR', 'collection_revenue': 210891.36}, {'customer_code': 'NY LITE', 'customer_name': 'LIGHTING NEW YORK', 'collection_revenue': 73557.4}, {'customer_code': 'CL BOCA', 'customer_name': 'CAPITOL LIGHTING - BOCA RATON', 'collection_revenue': 59972.0}, {'customer_code': '0003330', 'customer_name': 'BUNNY WILLIAMS HOME', 'collection_revenue': 52492.0}, {'customer_code': 'LAMPS +', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 51940.96}, {'customer_code': 'BENNING', 'customer_name': 'LUMENS', 'collection_revenue': 50884.8}, {'customer_code': 'IMPROV', 'customer_name': 'FERGUSON HOME', 'collection_revenue': 50473.61}, {'customer_code': '0019677', 'customer_name': 'DYKES FOOD SERVICE', 'collection_revenue': 42840.0}, {'customer_code': 'FOUNDRY', 'customer_name': 'FOUNDRY LIGHTING', 'collection_revenue': 37224.0}, {'customer_code': 'FER ENT', 'customer_name': 'FERGUSON ENTERPRISES', 'collection_revenue': 37145.0}, {'customer_code': 'LGTOLGY', 'customer_name': 'LIGHTOLOGY', 'collection_revenue': 24032.0}, {'customer_code': 'PBHLITE', 'customer_name': 'PACIFIC BUILDERS HARDWARE LIGHTING', 'collection_revenue': 23952.0}, {'customer_code': 'GOFRAN', 'customer_name': 'GOODFORM FRANCE AND SON', 'collection_revenue': 17300.0}, {'customer_code': 'VAL LIG', 'customer_name': 'VALLEY LIGHT GALLERY', 'collection_revenue': 16999.2}, {'customer_code': 'LIGHTOP', 'customer_name': 'LIGHTOPIA', 'collection_revenue': 16177.2}, {'customer_code': '0018961', 'customer_name': 'TAP 42', 'collection_revenue': 15708.0}, {'customer_code': 'CAI', 'customer_name': 'CAI DESIGNS', 'collection_revenue': 14806.8}, {'customer_code': 'SHADES', 'customer_name': 'SHADES OF LIGHT', 'collection_revenue': 12319.2}, {'customer_code': 'CLD SC', 'customer_name': 'CLASSIC LIGHTING & DESIGN', 'collection_revenue': 11124.5}, {'customer_code': 'GATEVA', 'customer_name': 'GATES INTERIORS, LLC', 'collection_revenue': 10976.0}, {'customer_code': 'PACE GA', 'customer_name': 'PACE LIGHTING', 'collection_revenue': 10867.24}, {'customer_code': 'PLUMDIS', 'customer_name': 'PDI', 'collection_revenue': 10750.2}, {'customer_code': 'BWINC', 'customer_name': 'WILLIAMS LAWRENCE', 'collection_revenue': 10350.0}, {'customer_code': 'HOANHA', 'customer_name': 'HOUSE OF ANTIQUE HARDWARE', 'collection_revenue': 10332.0}] |
| 6700-0040 | Wander Antique Silver Cordless Table Lamp | BUNNY WILLIAMS | 2 | 0 | [{'customer_code': 'WAYFAIR', 'customer_name': 'WAYFAIR', 'collection_revenue': 210891.36}, {'customer_code': 'NY LITE', 'customer_name': 'LIGHTING NEW YORK', 'collection_revenue': 73557.4}, {'customer_code': 'CL BOCA', 'customer_name': 'CAPITOL LIGHTING - BOCA RATON', 'collection_revenue': 59972.0}, {'customer_code': '0003330', 'customer_name': 'BUNNY WILLIAMS HOME', 'collection_revenue': 52492.0}, {'customer_code': 'LAMPS +', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 51940.96}, {'customer_code': 'BENNING', 'customer_name': 'LUMENS', 'collection_revenue': 50884.8}, {'customer_code': 'IMPROV', 'customer_name': 'FERGUSON HOME', 'collection_revenue': 50473.61}, {'customer_code': '0019677', 'customer_name': 'DYKES FOOD SERVICE', 'collection_revenue': 42840.0}, {'customer_code': 'FOUNDRY', 'customer_name': 'FOUNDRY LIGHTING', 'collection_revenue': 37224.0}, {'customer_code': 'FER ENT', 'customer_name': 'FERGUSON ENTERPRISES', 'collection_revenue': 37145.0}, {'customer_code': 'LGTOLGY', 'customer_name': 'LIGHTOLOGY', 'collection_revenue': 24032.0}, {'customer_code': 'PBHLITE', 'customer_name': 'PACIFIC BUILDERS HARDWARE LIGHTING', 'collection_revenue': 23952.0}, {'customer_code': 'GOFRAN', 'customer_name': 'GOODFORM FRANCE AND SON', 'collection_revenue': 17300.0}, {'customer_code': 'VAL LIG', 'customer_name': 'VALLEY LIGHT GALLERY', 'collection_revenue': 16999.2}, {'customer_code': 'LIGHTOP', 'customer_name': 'LIGHTOPIA', 'collection_revenue': 16177.2}, {'customer_code': '0018961', 'customer_name': 'TAP 42', 'collection_revenue': 15708.0}, {'customer_code': 'CAI', 'customer_name': 'CAI DESIGNS', 'collection_revenue': 14806.8}, {'customer_code': 'SHADES', 'customer_name': 'SHADES OF LIGHT', 'collection_revenue': 12319.2}, {'customer_code': 'CLD SC', 'customer_name': 'CLASSIC LIGHTING & DESIGN', 'collection_revenue': 11124.5}, {'customer_code': 'GATEVA', 'customer_name': 'GATES INTERIORS, LLC', 'collection_revenue': 10976.0}, {'customer_code': 'PACE GA', 'customer_name': 'PACE LIGHTING', 'collection_revenue': 10867.24}, {'customer_code': 'PLUMDIS', 'customer_name': 'PDI', 'collection_revenue': 10750.2}, {'customer_code': 'BWINC', 'customer_name': 'WILLIAMS LAWRENCE', 'collection_revenue': 10350.0}, {'customer_code': 'HOANHA', 'customer_name': 'HOUSE OF ANTIQUE HARDWARE', 'collection_revenue': 10332.0}] |
| 6700-0041 | Wander Brass Cordless Table Lamp | BUNNY WILLIAMS | 2 | 0 | [{'customer_code': 'WAYFAIR', 'customer_name': 'WAYFAIR', 'collection_revenue': 210891.36}, {'customer_code': 'NY LITE', 'customer_name': 'LIGHTING NEW YORK', 'collection_revenue': 73557.4}, {'customer_code': 'CL BOCA', 'customer_name': 'CAPITOL LIGHTING - BOCA RATON', 'collection_revenue': 59972.0}, {'customer_code': '0003330', 'customer_name': 'BUNNY WILLIAMS HOME', 'collection_revenue': 52492.0}, {'customer_code': 'LAMPS +', 'customer_name': 'LAMPS PLUS', 'collection_revenue': 51940.96}, {'customer_code': 'BENNING', 'customer_name': 'LUMENS', 'collection_revenue': 50884.8}, {'customer_code': 'IMPROV', 'customer_name': 'FERGUSON HOME', 'collection_revenue': 50473.61}, {'customer_code': '0019677', 'customer_name': 'DYKES FOOD SERVICE', 'collection_revenue': 42840.0}, {'customer_code': 'FOUNDRY', 'customer_name': 'FOUNDRY LIGHTING', 'collection_revenue': 37224.0}, {'customer_code': 'FER ENT', 'customer_name': 'FERGUSON ENTERPRISES', 'collection_revenue': 37145.0}, {'customer_code': 'LGTOLGY', 'customer_name': 'LIGHTOLOGY', 'collection_revenue': 24032.0}, {'customer_code': 'PBHLITE', 'customer_name': 'PACIFIC BUILDERS HARDWARE LIGHTING', 'collection_revenue': 23952.0}, {'customer_code': 'GOFRAN', 'customer_name': 'GOODFORM FRANCE AND SON', 'collection_revenue': 17300.0}, {'customer_code': 'VAL LIG', 'customer_name': 'VALLEY LIGHT GALLERY', 'collection_revenue': 16999.2}, {'customer_code': 'LIGHTOP', 'customer_name': 'LIGHTOPIA', 'collection_revenue': 16177.2}, {'customer_code': '0018961', 'customer_name': 'TAP 42', 'collection_revenue': 15708.0}, {'customer_code': 'CAI', 'customer_name': 'CAI DESIGNS', 'collection_revenue': 14806.8}, {'customer_code': 'SHADES', 'customer_name': 'SHADES OF LIGHT', 'collection_revenue': 12319.2}, {'customer_code': 'CLD SC', 'customer_name': 'CLASSIC LIGHTING & DESIGN', 'collection_revenue': 11124.5}, {'customer_code': 'GATEVA', 'customer_name': 'GATES INTERIORS, LLC', 'collection_revenue': 10976.0}, {'customer_code': 'PACE GA', 'customer_name': 'PACE LIGHTING', 'collection_revenue': 10867.24}, {'customer_code': 'PLUMDIS', 'customer_name': 'PDI', 'collection_revenue': 10750.2}, {'customer_code': 'BWINC', 'customer_name': 'WILLIAMS LAWRENCE', 'collection_revenue': 10350.0}, {'customer_code': 'HOANHA', 'customer_name': 'HOUSE OF ANTIQUE HARDWARE', 'collection_revenue': 10332.0}] |
| 1000-0174 | Tessellate Mirror | — | 1 | 687.80 | — |
| 1000-0177 | Cobbler Whitewash Mirror | — | 1 | 296 | — |
| 1000-0180 | Sentimental Mirror | — | 1 | 0 | — |
| 1000-0181 | Aegis Gold Mirror | — | 0 | 0 | — |
| 1000-0185 | Wolcott Mirror | — | 0 | 0 | — |
| 1000-0187 | Dunmore Arch Mirror | — | 1 | 0 | — |
| 1000-0188 | Deanna Ivory Raffia Rectangular Floor Mirror | — | 1 | 1,116 | — |
| 1000-0189 | Deanna Ivory Raffia Oval Mirror | — | 1 | 908.20 | — |
| 1000-0190 | Tessera Round Mirror | — | 0 | 0 | — |
| 1200-1084 | Hercules Head on Metal Stand | — | 1 | 1,096 | — |
| 1200-1085 | Delos Torso on Metal Stand | — | 1 | 1,421.20 | — |
| 1200-1086 | Cyprus Torso on Metal Stand | — | 0 | 0 | — |
| 1200-1087 | Phoenician Pillar with Capital | — | 0 | 0 | — |
| 1200-1088 | Phoenician Pillar | — | 0 | 0 | — |
| 1200-1090 | Ishtar Fragment on Metal Stand | — | 2 | 1,584 | — |
| 1200-1101 | Le Danseur Bronze | — | 0 | 0 | — |
| 1200-1103 | Hypnos Head on Metal Plinth | — | 0 | 0 | — |
| 1200-1104 | Ashanti Fertility Bronze | — | 0 | 0 | — |
| 1200-1107 | Sunken Boat Barnacle Object | — | 0 | 0 | — |
| 1200-1108 | Seadrift Medium White Vase | — | 2 | 592 | — |
| 1200-1109 | Seadrift Small White Vase | — | 2 | 392 | — |
| 1200-1110 | Bulwark the Bulldog Bronze | — | 0 | 0 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
