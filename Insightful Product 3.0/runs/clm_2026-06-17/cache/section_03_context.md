# Section 3 Context Bundle — Crystorama (clm)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=74342, portal_order_gmv=$40.3M |
| HAS_INVENTORY | True | inventory_count=1902 |
| HAS_SALES_DATA | True | sales_data_count=69099 |
| HAS_SALES_SECTION | True | qualifying_reps=5 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Catalog-Focused |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | crystorama_clm_ecat_online |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$40.3M > ecat_gmv=$551,721: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 5 | 5 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 100 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 165, Mixpanel total submit_order (Q-01): 2 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=90.0%, ambiguous_rate=0.0%, showroom_event_share=6.5% |
| USER_GROUP_JOIN_RATE | 90% | 90 of 100 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7% | showroom+admin share of matched events: 6.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Amit Sharma, Megan  Trosclair, HighPoint Showroom, Amit Sharma |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=-2685853 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2058 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=38 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Crystorama
- **Shortname**: clm
- **Org ID**: 64
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Crystorama (clm, org_id=64)
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

# Signal Rank — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Total signals fired**: 55 (P0: 43, P1: 12, P2: 0)
- **Org GMV**: $0.6M eCat LTM, $40.3M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders | P1 | §2 Accounts | 12.8 | $12,799,682 | 2.0 | 327,663,719 | POSITIVE |
| 2 | SIG-ANOMALY-02 | Stock Out — HAY-1417-AG (Hayes 50'' Aged Brass Linear Chandelier) $491,812 LTM, 0 available | P0 | §3 Product | 10.0 | $491,812 | 3.0 | 14,754,357 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — ADD-317-AG-CL (Addis 51.75'' Aged Brass Linear Chandeli) $296,813 LTM, 0 available | P0 | §3 Product | 10.0 | $296,813 | 3.0 | 8,904,385 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — SHY-10907-SG (Shyla 24'' Soft Gold Chandelier) $292,247 LTM, 0 available | P0 | §3 Product | 10.0 | $292,247 | 3.0 | 8,767,410 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — ARA-10269-MK-ST (Aragon 58.75'' LED Matte Black Chandelie) $265,753 LTM, 0 available | P0 | §3 Product | 10.0 | $265,753 | 3.0 | 7,972,595 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 505-MT (Broche 16'' Matte White Semi Flush Mount) $230,169 LTM, 0 available | P0 | §3 Product | 10.0 | $230,169 | 3.0 | 6,905,072 | RISK |
| 7 | SIG-MOM-01 | Account Acceleration — Melrose & Madison CANADA ONLY (AMZ) 2 consecutive QoQ acceleration quarters, $744,929 peak quarter (+87% QoQ) | P0 | §2 Accounts | 2.9 | $744,929 | 3.0 | 6,465,987 | POSITIVE |
| 8 | SIG-ANOMALY-02 | Stock Out — ADD-317-AG-AU (Addis 51.75'' Aged Brass Linear Chandeli) $207,763 LTM, 0 available | P0 | §3 Product | 10.0 | $207,763 | 3.0 | 6,232,876 | RISK |
| 9 | SIG-COMMERCE-01 | Capture Rate — eCat captures 1.4% of $40M total business; each +1pt = $403K | P0 | §4 Commerce | 4.9 | $403,000 | 3.0 | 5,962,242 | POSITIVE |
| 10 | SIG-ANOMALY-02 | Stock Out — ADD-317-AG-AM (Addis 51.75'' Aged Brass Linear Chandeli) $188,094 LTM, 0 available | P0 | §3 Product | 10.0 | $188,094 | 3.0 | 5,642,824 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — ARC-1919-GA-CL-MWP (Arcadia 46.25'' Antique Gold Chandelier) $180,660 LTM, 0 available | P0 | §3 Product | 10.0 | $180,660 | 3.0 | 5,419,812 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — HAY-1409-PN (Hayes 40.5'' Polished Nickel Chandelier) $177,252 LTM, 0 available | P0 | §3 Product | 10.0 | $177,252 | 3.0 | 5,317,566 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — ADD-308-AG-WH (Addis 22'' Aged Brass Chandelier) $136,285 LTM, 0 available | P0 | §3 Product | 10.0 | $136,285 | 3.0 | 4,088,544 | RISK |
| 14 | SIG-ANOMALY-03 | Competitive Displacement — Cozy Development total biz +560% but eCat -100% | P0 | §2 Accounts | 44.0 | $23,584 | 3.0 | 3,110,693 | RISK |
| 15 | SIG-MOM-01 | Account Acceleration — Crystorama Accm 2 consecutive QoQ acceleration quarters, $61,836 peak quarter (+432% QoQ) | P0 | §2 Accounts | 14.4 | $61,836 | 3.0 | 2,673,161 | POSITIVE |
| 16 | SIG-DECAY-04 | Spending Contraction — Home Depot-ASN -54.9% YoY ($464,924→$209,744), $255,180 gap | P0 | §2 Accounts | 2.7 | $255,180 | 3.0 | 2,101,404 | RISK |
| 17 | SIG-MOM-01 | Account Acceleration — ShadesofLight 2 consecutive QoQ acceleration quarters, $381,645 peak quarter (+54% QoQ) | P0 | §2 Accounts | 1.8 | $381,645 | 3.0 | 2,064,698 | POSITIVE |
| 18 | SIG-MOM-01 | Account Acceleration — US Electrical Services, Inc.LA 2 consecutive QoQ acceleration quarters, $40,215 peak quarter (+233% QoQ) | P0 | §2 Accounts | 7.8 | $40,215 | 3.0 | 937,814 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — BBC Lighting Company 2 consecutive QoQ acceleration quarters, $62,520 peak quarter (+137% QoQ) | P0 | §2 Accounts | 4.6 | $62,520 | 3.0 | 855,902 | POSITIVE |
| 20 | SIG-DECAY-04 | Spending Contraction — Lamps.com -49.9% YoY ($209,278→$104,924), $104,354 gap | P0 | §2 Accounts | 2.5 | $104,354 | 3.0 | 781,088 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 32 | 1 | 0 | 33 | |
| §3 Product Intelligence | 10 | 0 | 0 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 10 | 0 | 10 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Melrose & Madison CANADA ONLY (AMZ) 2 consecutive QoQ acceleration quarters, $744,929 peak quarter (+87% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 1.4% of $40M total business; each +1pt = $403K
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Crystorama Accm 2 consecutive QoQ acceleration quarters, $61,836 peak quarter (+432% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — HAY-1417-AG (Hayes 50'' Aged Brass Linear Chandelier) $491,812 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — ADD-317-AG-CL (Addis 51.75'' Aged Brass Linear Chandeli) $296,813 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — SHY-10907-SG (Shyla 24'' Soft Gold Chandelier) $292,247 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Crystorama (clm, org_id=64)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,898 | 0 | 0 | 100 |

### Q-37_results.md

# Q-37 Results — Crystorama (clm, org_id=64)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HAY-1417-AG | CAT1 | HAYES | Hayes 50'' Aged Brass Linear Chandelier | $491,812 | 352 | 0 | 0 | 0 | 2026-7-14 |
| ADD-317-AG-CL | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $296,813 | 258 | 0 | 0 | 0 | 2026-6-30 |
| SHY-10907-SG | CAT1 | SHYLA | Shyla 24'' Soft Gold Chandelier | $292,247 | 657 | 0 | 0 | 0 | 2026-6-23 |
| ARA-10269-MK-ST | CAT1 | COL127 | Aragon 58.75'' LED Matte Black Chandelier | $265,753 | 102 | 0 | 0 | 0 | 2026-8-18 |
| 505-MT | CAT2 | COL100 | Broche 16'' Matte White Semi Flush Mount | $230,169 | 969 | 0 | 0 | 0 | 2026-6-26 |
| ADD-317-AG-AU | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $207,763 | 183 | 0 | 0 | 0 | 2026-6-29 |
| ADD-317-AG-AM | CAT1 | ADDIS | Addis 51.75'' Aged Brass Linear Chandelier | $188,094 | 162 | 0 | 0 | 0 | 2026-8-6 |
| ARC-1919-GA-CL-MWP | CAT1 | COL70 | Arcadia 46.25'' Antique Gold Chandelier | $180,660 | 110 | 0 | 0 | 0 | 2026-7-27 |
| HAY-1409-PN | CAT1 | HAYES | Hayes 40.5'' Polished Nickel Chandelier | $177,252 | 87 | 0 | 0 | 0 | 2026-7-14 |
| ADD-308-AG-WH | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $136,285 | 234 | 0 | 0 | 0 | 2026-6-29 |
| ADD-308-AG-AM | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $119,540 | 210 | 0 | 0 | 0 | 2026-6-30 |
| ARA-10269-MK | CAT1 | COL127 | Aragon 60'' LED Matte Black Chandelier | $114,179 | 44 | 0 | 0 | 0 | 2026-8-18 |
| 2242-VG | CAT6 | COL9 | Libby Langdon Sylvan 15.5'' Vibrant Gold Sconce | $112,124 | 1,113 | 0 | 0 | 0 | 2026-6-26 |
| 4840-CT | CAT2 | JOSIE | Josie 20.5'' Champagne Green Tea Semi Flush Mount | $108,607 | 539 | 0 | 0 | 0 | 2026-7-20 |
| ADD-308-AG-CL | CAT1 | ADDIS | Addis 22'' Aged Brass Chandelier | $100,772 | 173 | 0 | 0 | 0 | 2026-8-17 |
| ARC-1909-GA-CL-MWP | CAT1 | COL70 | Arcadia 32.5'' Antique Gold Chandelier | $98,352 | 116 | 0 | 0 | 0 | 2026-6-29 |
| 4456-GA-CL-MWP | CAT1 | COL113 | Filmore 29'' Hand Cut Crystal Antique Gold Chandelier | $94,422 | 184 | 0 | 0 | 0 | 2026-7-14 |
| 573-OP-GA | CAT5 | COL100 | Broche 25'' Antique Gold Bathroom Vanity | $89,658 | 483 | 0 | 0 | 0 | 2026-6-26 |
| ADD-321-AG-WH | CAT2 | ADDIS | Addis 22.25'' Aged Brass Flush Mount | $80,523 | 110 | 0 | 0 | 0 | 2026-5-25 |
| 4457-GA-CL-MWP | CAT2 | COL113 | Filmore 19'' Hand Cut Crystal Antique Gold Semi Flush Mount | $71,181 | 249 | 0 | 0 | 0 | 2026-7-14 |

### Q-38a_results.md

# Q-38a Results — Crystorama (clm, org_id=64)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
|  | — | — | — | 2025-12-1 | 6,537 | 1,976 |
|  | — | — | — | 2026-1-1 | 16,551 | 5,900 |
|  | — | — | — | 2026-2-1 | 15,177 | 5,980 |
|  | — | — | — | 2026-3-1 | 16,961 | 6,817 |
|  | — | — | — | 2026-4-1 | 17,772 | 6,676 |
|  | — | — | — | 2026-5-1 | 15,339 | 6,796 |
|  | — | — | — | 2026-6-1 | 8,312 | 3,671 |
|  | — | — | — | 2080-3-1 | 2 | 1 |
|  | — | — | — | 2080-9-1 | 2 | 1 |
|  | — | — | — | 2140-1-1 | 2 | 1 |
|  | — | — | — | 2220-6-1 | 2 | 1 |
|  | — | — | — | 2870-1-1 | 2 | 1 |
|  | — | — | — | 6021-12-1 | 2 | 1 |
|  | — | — | — | 6949-11-1 | 9 | 1 |
|  | — | — | — | 7690-1-1 | 2 | 1 |
|  | — | — | — | 8022-4-1 | 3 | 1 |
|  | — | — | — | 9021-7-1 | 2 | 1 |
|  | — | — | — | 9201-2-1 | 12 | 1 |
|  | — | — | — | 9260-1-1 | 5 | 1 |
|  | — | — | — | 9380-1-1 | 2 | 1 |

### Q-39_category_results.md

# Q-39-cat Results — Crystorama (clm, org_id=64)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT1 | $39.6M | 79,995 | 781 | $50,760 |
| CAT6 | $9.7M | 96,890 | 423 | $22,955 |
| CAT2 | $9.6M | 40,002 | 335 | $28,599 |
| CAT3 | $4.5M | 21,489 | 144 | $30,948 |
| CAT5 | $1.7M | 10,141 | 63 | $27,628 |
| CAT4 | $1.2M | 7,464 | 75 | $16,467 |
| CAT7 | $180,922 | 831 | 30 | $6,031 |
| CAT8 | $138,129 | 842 | 8 | $17,266 |
| SHADE | $244 | 37 | 2 | $122 |

### Q-39_collection_results.md

# Q-39-col Results — Crystorama (clm, org_id=64)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| COL100 | $10.1M | 43,662 | 138 | $73,202 |
| ADDIS | $8.0M | 9,539 | 138 | $58,195 |
| HAYES | $3.5M | 5,409 | 24 | $147,084 |
| COL122 | $2.7M | 7,223 | 48 | $56,721 |
| COL1 | $2.6M | 16,748 | 46 | $56,764 |
| EMORY | $2.1M | 1,659 | 14 | $148,302 |
| COL43 | $1.7M | 9,616 | 41 | $42,646 |
| COL9 | $1.4M | 12,824 | 40 | $34,048 |
| COL111 | $1.4M | 3,437 | 83 | $16,380 |
| COL127 | $1.1M | 725 | 25 | $45,147 |
| COL92 | $1.0M | 3,051 | 10 | $101,617 |
| COL70 | $963,724 | 1,691 | 17 | $56,690 |
| RYLEE | $919,766 | 2,298 | 27 | $34,065 |
| SHYLA | $911,348 | 1,504 | 2 | $455,674 |
| COL104 | $893,842 | 2,295 | 61 | $14,653 |
| COL86 | $821,032 | 4,141 | 24 | $34,210 |
| LUNA | $736,814 | 1,088 | 11 | $66,983 |
| JAYNA | $692,344 | 2,298 | 7 | $98,906 |
| COL137 | $690,947 | 2,072 | 19 | $36,366 |
| ESME | $683,689 | 1,184 | 20 | $34,184 |
| COL105 | $555,864 | 3,866 | 39 | $14,253 |
| COL7 | $481,722 | 4,597 | 8 | $60,215 |
| COL11 | $452,499 | 2,768 | 19 | $23,816 |
| PALLA | $444,234 | 909 | 12 | $37,020 |
| COL39 | $416,052 | 4,634 | 9 | $46,228 |

### Q-42_results.md

# Q-42 Results — Crystorama (clm, org_id=64)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| TRUAX | 75 | $133,951 | 281 | $1,786 |
| COL9 | 205 | $109,529 | 424 | $534 |
| COL58 | 158 | $108,534 | 998 | $687 |
| RYLEE | 114 | $87,038 | 297 | $763 |
| COL11 | 112 | $67,497 | 367 | $603 |
| COL79 | 82 | $52,708 | 215 | $643 |
| COL83 | 43 | $42,109 | 93 | $979 |
| COL35 | 67 | $39,818 | 231 | $594 |
| COL149 | 7 | $7,253 | 13 | $1,036 |
| COL96 | 15 | $4,610 | 28 | $307 |
| COL87 | 17 | $4,229 | 30 | $249 |
| COL91 | 22 | $3,575 | 37 | $162 |
| COL80 | 2 | $324 | 3 | $162 |

### Q-59_results.md

# Q-59 Results — Crystorama (clm, org_id=64)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 4
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ITEM | BRI-3002X-GA | Brielle EX 2 Light Antique Gol d Sconce | Uncategorized | — | — | 19 | 1 | 89 | 1,691 | 3,560 | 1 |
| ITEM | 571-OP-SA | Broche 6.5'' Antique Silver Sconce | CAT6 | — | — | 3 | 1 | 114 | 342 | 9,560.02 | 31 |
| ITEM | 7001-OB | Langley 4.75'' Olde Brass Sconce | CAT6 | — | — | 1 | 1 | 190.40 | 190.40 | 8,839.18 | 8 |
| ORG_SUMMARY | — | — | — | 95.70 | 7,855 | — | — | — | — | — | — |

### Q-61_results.md

# Q-61 Results — Crystorama (clm, org_id=64)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2016-AG | Brian Patrick Flynn Truax 16'' Aged Brass Pendant | CAT3 | 19 | 56 | 19,716 | 29 | 349 |
| 608-GA | Rylee 18.75'' Antique Gold Chandelier | CAT1 | 19 | 36 | 16,998.17 | 28 | 499 |
| 2030-AG | Brian Patrick Flynn Truax 30'' Aged Brass Pendant | CAT3 | 8 | 16 | 16,814.70 | 8 | 1,099 |
| SOL-9326-EB | Solaris 22.5'' English Bronze Outdoor Chandelier | CAT4 | 8 | 54 | 14,349.01 | 42 | 299 |
| 2243-PN | Libby Langdon Sylvan 16'' Polished Nickel Semi Flush Mount | CAT2 | 24 | 48 | 8,802.88 | 47 | 199 |
| CAP-8501-MK-TG | Brian Patrick Flynn Capsule 6'' Matte Black + Textured Gold Outdoor Sconce | CAT4 | 14 | 66 | 6,983.46 | 34 | 99 |
| 600-GA | Rylee 12.5'' Antique Gold Flush Mount | CAT2 | 22 | 33 | 6,651.88 | 31 | 199 |
| 2249-PN | Libby Langdon Sylvan 42'' Polished Nickel Linear Chandelier | CAT1 | 9 | 14 | 6,434.61 | 14 | 499 |
| 8864-PN | Baxter 22'' Polished Nickel Chandelier | CAT1 | 9 | 13 | 6,067.84 | 9 | 499 |
| 2264-AG-LED | Libby Langdon Jennings 24'' Integrated LED Aged Brass Bathroom Vanity | CAT5 | 13 | 26 | 5,239.13 | 17 | 199 |
| 2244-PN_NOSHADE | Libby Langdon Sylvan 21.5'' Polished Nickel Chandelier | CAT1 | 9 | 15 | 4,642.36 | 11 | 324 |
| CAP-8500-MK-TG | Brian Patrick Flynn Capsule 8'' Matte Black + Textured Gold Outdoor Semi Flush Mount | CAT4 | 16 | 36 | 3,771.40 | 23 | 109 |
| 9590-MK | Brian Patrick Flynn Hulton 15'' Matte Black Flush Mount | CAT2 | 11 | 19 | 3,538.22 | 12 | 199 |
| 2243-PN_NOSHADE | Libby Langdon Sylvan 16'' Polished Nickel Semi Flush Mount | CAT2 | 8 | 19 | 3,483.40 | 15 | 199 |
| CAP-8509-MK-TG | Brian Patrick Flynn Capsule 12.25'' Matte Black + Textured Gold Outdoor Post | CAT4 | 5 | 22 | 2,890.60 | 13 | 149 |
| 9595-MK | Brian Patrick Flynn Hulton 25'' Matte Black Chandelier | CAT1 | 6 | 7 | 2,603.42 | 6 | 374 |
| 8867-PN | Baxter 31.5'' Polished Nickel Chandelier | CAT1 | 5 | 6 | 2,584.40 | 6 | 497 |
| CAP-8503-MK-TG | Brian Patrick Flynn Capsule 12'' Matte Black + Textured Gold Outdoor Flush Mount | CAT4 | 12 | 26 | 2,388.07 | 24 | 109 |
| 2249-PN_NOSHADE | Libby Langdon Sylvan 42'' Polished Nickel Linear Chandelier | CAT1 | 4 | 5 | 2,295.40 | 5 | 499 |
| CAP-8506-MK-TG | Brian Patrick Flynn Capsule 12.25'' Matte Black + Textured Gold Outdoor Pendant | CAT4 | 8 | 11 | 2,208.27 | 8 | 199 |
| 2264-PN-LED | Libby Langdon Jennings 24'' Integrated LED Polished Nickel Bathroom Vanity | CAT5 | 9 | 12 | 2,191.24 | 9 | 199 |
| 9224-OS | Solaris 17'' Olde Silver Chandelier | CAT1 | 10 | 12 | 1,877.82 | 12 | 174 |
| 9224-EB | Solaris 17'' English Bronze Chandelier | CAT1 | 9 | 11 | 1,703.29 | 10 | 174 |
| 2247-PN_NOSHADE | Libby Langdon Sylvan 22.5'' Polished Nickel Chandelier | CAT1 | 4 | 6 | 1,566.08 | 6 | 297 |
| 9597-MK | Brian Patrick Flynn Hulton 21'' Matte Black Chandelier | CAT1 | 2 | 13 | 1,327 | 3 | 367 |
| SOL-9325-EB | Solaris 12'' English Bronze Outdoor Chandelier | CAT4 | 5 | 8 | 1,106.64 | 8 | 159 |
| 2245-PN_NOSHADE | Libby Langdon Sylvan 16'' Polished Nickel Chandelier | CAT1 | 2 | 3 | 801 | 2 | 267 |
| 783-CH-CL-MWP | Archer 11.5'' Hand Cut Crystal Polished Chrome Semi Flush Mount | CAT2 | 5 | 7 | 643.60 | 7 | 97 |
| 5534-WW-CL-S | Welton 11'' Swarovski Strass Crystal Wet White Chandelier | CAT1 | 1 | 1 | 547 | 1 | 547 |
| 5534-EB-CL-S | Welton 11'' Swarovski Strass Crystal English Bronze Chandelier | CAT1 | 1 | 1 | 547 | 1 | 547 |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HAY-1417-AG | Hayes 50'' Aged Brass Linear Chandelier | HAYES | 491,811.89 | 352 | — | 2026-7-14 | [{'customer': 'Build Drop Ship EDI', 'revenue': 30598.76}, {'customer': 'Elements', 'revenue': 28042.46}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 27794.75}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 20355.47}, {'customer': 'Lighting First - Bonita', 'revenue': 16689.5}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 13546.9}, {'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 13071.6}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 11858.25}, {'customer': 'Lighting, Inc', 'revenue': 11332.8}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 11146.85}, {'customer': 'Cleveland Lighting', 'revenue': 9174.2}, {'customer': 'Valley Light Gallery', 'revenue': 8544.6}, {'customer': 'Lightstyle of Orlando', 'revenue': 7454.28}, {'customer': "Horton's Home Lighting", 'revenue': 7310.25}, {'customer': 'Anthology Lighting', 'revenue': 6296.0}, {'customer': 'Universal Lights, Inc.', 'revenue': 6084.07}, {'customer': 'Lightology, LLC.com', 'revenue': 6072.14}, {'customer': 'Lighting By Fox, LLC', 'revenue': 5991.07}, {'customer': 'Litemode Limited', 'revenue': 5941.17}, {'customer': 'Dolan NW LLC', 'revenue': 5756.4}, {'customer': 'Progressive Lighting', 'revenue': 5576.4}, {'customer': 'Ellen Lighting & Hardware', 'revenue': 5322.64}, {'customer': 'Naples Lighting and Fan Depot', 'revenue': 4685.07}, {'customer': 'R. Bdelaa Lighting', 'revenue': 4597.0}, {'customer': 'Lighting Efx', 'revenue': 4573.14}, {'customer': 'Xpress Lighting of Texas', 'revenue': 4485.07}, {'customer': 'Metro Showroom West County', 'revenue': 4317.3}, {'customer': 'LDB Holdings, LLC', 'revenue': 3997.4}, {'customer': 'Lando Lighting', 'revenue': 3997.4}, {'customer': 'Home Lighting of Frazer', 'revenue': 3747.5}, {'customer': 'Reflections L+M', 'revenue': 3198.0}, {'customer': 'Muller Lighting Gallery', 'revenue': 3198.0}, {'customer': 'Aladdin Lighting & Supply, Inc', 'revenue': 3198.0}, {'customer': 'Lighting Etc', 'revenue': 3098.0}, {'customer': 'Passion Lighting', 'revenue': 3098.0}, {'customer': 'Continental Lighting Corp.', 'revenue': 3098.0}, {'customer': 'Dominion Electric', 'revenue': 3098.0}, {'customer': 'Nth Degree Home LLC', 'revenue': 3086.07}, {'customer': 'Haus Appeal LLC', 'revenue': 3006.12}, {'customer': 'Lightopia, LLC.', 'revenue': 3006.12}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 2998.0}, {'customer': 'Decorating Solutions by Sara', 'revenue': 2998.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 2998.0}, {'customer': 'Light Gallery Plus', 'revenue': 2998.0}, {'customer': 'Lighting First Ft. Myers', 'revenue': 2986.07}, {'customer': 'Mayson Enterprise dba Aura Lighting', 'revenue': 2974.14}, {'customer': "Graham's Living", 'revenue': 2881.14}, {'customer': 'Nova Lighting', 'revenue': 2881.14}, {'customer': 'E&L LIghting', 'revenue': 2848.1}, {'customer': 'Capitol Lighting-ASN', 'revenue': 2838.31}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 2788.2}, {'customer': 'Wilson Lighting of Naples', 'revenue': 2788.2}, {'customer': 'Foundrylighting.com', 'revenue': 2788.14}, {'customer': 'Southern Lights', 'revenue': 2788.14}, {'customer': 'Shades of Light', 'revenue': 2698.2}, {'customer': 'Crystorama Accm', 'revenue': 2698.2}, {'customer': 'Exclusive Lighting', 'revenue': 2548.3}, {'customer': 'ABC Creations', 'revenue': 2298.5}, {'customer': 'Royal Chic Design', 'revenue': 1999.0}, {'customer': 'Spark Lighting', 'revenue': 1874.0}, {'customer': 'Greer Lighting Center', 'revenue': 1873.75}, {'customer': 'Zimmerman Interiors', 'revenue': 1839.0}, {'customer': 'Pinnacle Design Consumer', 'revenue': 1839.0}, {'customer': 'Luminaires Repentigny Inc', 'revenue': 1759.0}, {'customer': 'Union Lighting & Home', 'revenue': 1724.0}, {'customer': 'O&I Design Group, LLC DBA The Elements', 'revenue': 1724.0}, {'customer': 'DDC Design', 'revenue': 1679.22}, {'customer': 'Littman Bros Lighting', 'revenue': 1599.0}, {'customer': 'Lightology, LLC-1', 'revenue': 1599.0}, {'customer': 'Aura Interiors Inc', 'revenue': 1599.0}, {'customer': 'Floral and Designs', 'revenue': 1599.0}, {'customer': 'Brothers Lighting &Fan Gallery', 'revenue': 1599.0}, {'customer': 'Morrison Supply Company,Midlan', 'revenue': 1599.0}, {'customer': 'Idlewood Electric Supply', 'revenue': 1599.0}, {'customer': 'Hye Lighting', 'revenue': 1599.0}, {'customer': 'Franklin Lighting', 'revenue': 1599.0}, {'customer': 'LyteWorks', 'revenue': 1599.0}, {'customer': "Garbe's Lighting and Hardware", 'revenue': 1599.0}, {'customer': 'Dulles Electric Supply', 'revenue': 1599.0}, {'customer': 'Save More Lighting, LTD', 'revenue': 1599.0}, {'customer': 'Armstrong Supply Co.', 'revenue': 1599.0}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 1599.0}, {'customer': 'IBS Lighting', 'revenue': 1599.0}, {'customer': 'Denali Lighting', 'revenue': 1599.0}, {'customer': 'M&M Lighting Co', 'revenue': 1599.0}, {'customer': 'At Home LLC DBA Home Lighting', 'revenue': 1599.0}, {'customer': 'Light Bulbs Etc (Montclair)', 'revenue': 1519.05}, {'customer': 'The Lighting Corner', 'revenue': 1499.0}, {'customer': 'PC Building Materials', 'revenue': 1499.0}, {'customer': 'Luminous Trends Inc DBA Modern Luxury by LT)', 'revenue': 1499.0}, {'customer': 'CES Aquisition LLC', 'revenue': 1499.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 1499.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 1499.0}, {'customer': 'Schwartz Design Showroom', 'revenue': 1499.0}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 1499.0}, {'customer': 'Fan & Lighting World', 'revenue': 1499.0}, {'customer': 'GW Lighting & Home Decor', 'revenue': 1499.0}, {'customer': 'House of Lights, Inc.', 'revenue': 1499.0}, {'customer': 'Naples Lamp Shop', 'revenue': 1499.0}, {'customer': 'Bolgiano Custom Homes&Interior', 'revenue': 1499.0}, {'customer': 'Bulbo', 'revenue': 1499.0}, {'customer': 'Maple Ridge Lighting Inc.', 'revenue': 1499.0}, {'customer': 'The Fixture Exchange', 'revenue': 1499.0}, {'customer': 'Lee Douglas Interiors, Inc.', 'revenue': 1499.0}, {'customer': 'Nimbus Nine Inc.', 'revenue': 1499.0}, {'customer': 'DuPage Lighting Inc.', 'revenue': 1487.07}, {'customer': 'Premier Bath Lighting&Hardware', 'revenue': 1487.07}, {'customer': 'Jones Group Interiors, Inc.', 'revenue': 1487.07}, {'customer': 'Robinson Lighting Centre', 'revenue': 1487.07}, {'customer': 'Georgia Lighting', 'revenue': 1487.07}, {'customer': 'Marx Fireplace and Lighting', 'revenue': 1487.07}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 1487.07}, {'customer': 'Lighting Direct NJ LLC', 'revenue': 1487.07}, {'customer': 'Accent Lighting, Inc.', 'revenue': 1487.07}, {'customer': 'Modern Lighting', 'revenue': 1487.07}, {'customer': "Efird's Interiors, Inc.", 'revenue': 1439.1}, {'customer': 'Luxury Lighting', 'revenue': 1439.1}, {'customer': 'C E Tang Yuk and Co Ltd', 'revenue': 1394.07}, {'customer': 'ABC Lighting Inc', 'revenue': 1394.07}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 1394.07}, {'customer': 'ArtGlass Canada Inc DBA Casa Di Luce', 'revenue': 1394.07}, {'customer': 'The Lighthouse', 'revenue': 1394.07}, {'customer': 'Beautiful Lights', 'revenue': 1349.1}, {'customer': 'Union Lighting & Furnishings', 'revenue': 1279.2}, {'customer': 'Montreal Luminaire', 'revenue': 1231.3}, {'customer': 'Erika Ward Interiors', 'revenue': 1214.19}, {'customer': 'RAINBOW LIGHTING INC', 'revenue': 1199.2}, {'customer': 'Hall Electric Co, Inc', 'revenue': 1119.3}, {'customer': 'Lyons Electrical Supply Co.', 'revenue': 1049.3}, {'customer': 'Illuminations', 'revenue': 899.4}, {'customer': 'Galleria Lighting  E MAIL', 'revenue': 799.5}, {'customer': 'Light Lab Design', 'revenue': 768.1}, {'customer': 'Prima Lighting', 'revenue': 749.5}, {'customer': 'First Coast Lighting & Fans', 'revenue': 0.0}, {'customer': 'Mars Electric Co.', 'revenue': 0.0}, {'customer': 'Ponton Interiors', 'revenue': 0.0}, {'customer': 'Light Point', 'revenue': 0.0}, {'customer': 'First Fruit Collection', 'revenue': 0.0}] | [{'item': 'HAY-1402-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 102}, {'item': 'HAY-1401-AG', 'desc': "Hayes 8'' Aged Brass Chandelier", 'available': 75}, {'item': 'HAY-1402-AG', 'desc': "Hayes 7.5'' Aged Brass Sconce", 'available': 61}, {'item': 'HAY-1411-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 39}, {'item': 'HAY-1401-PN', 'desc': "Hayes 8'' Polished Nickel Chandelier", 'available': 33}, {'item': 'HAY-1400-AG', 'desc': "Hayes 16'' Aged Brass Flush Mount", 'available': 30}, {'item': 'HAY-1409-AG', 'desc': "Hayes 40.5'' Aged Brass Chandelier", 'available': 29}, {'item': 'HAY-1407-PN', 'desc': "Hayes 28'' Polished Nickel Chandelier", 'available': 28}, {'item': 'HAY-1407-AG', 'desc': "Hayes 28'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1405-AG', 'desc': "Hayes 22'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1403-AG', 'desc': "Hayes 18'' Aged Brass Flush Mount", 'available': 24}, {'item': 'HAY-1403-PN', 'desc': "Hayes 18'' Polished Nickel Flush Mount", 'available': 17}, {'item': 'HAY-1413-PN', 'desc': "Hayes 23.5'' Polished Nickel Bathroom Vanity", 'available': 12}, {'item': 'HAY-1405-PN', 'desc': "Hayes 22'' Polished Nickel Chandelier", 'available': 12}, {'item': 'HAY-1400-PN', 'desc': "Hayes 16'' Polished Nickel Flush Mount", 'available': 10}, {'item': 'HAY-1415-PN', 'desc': "Hayes 31.5'' Polished Nickel Bathroom Vanity", 'available': 9}, {'item': 'HAY-1417-PN', 'desc': "Hayes 50'' Polished Nickel Linear Chandelier", 'available': 8}, {'item': 'HAY-1415-AG', 'desc': "Hayes 31.5'' Aged Brass Bathroom Vanity", 'available': 8}, {'item': 'HAY-1413-AG', 'desc': "Hayes 23.5'' Aged Brass Bathroom Vanity", 'available': 6}, {'item': 'HAY-1419-AG', 'desc': "Hayes 24'' Aged Brass Chandelier", 'available': 1}] |
| ADD-317-AG-CL | Addis 51.75'' Aged Brass Linear Chandelier | ADDIS | 296,812.82 | 258 | — | 2026-6-30 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 22170.22}, {'customer': 'Elements', 'revenue': 18638.9}, {'customer': 'Build Drop Ship EDI', 'revenue': 17236.85}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 15421.0}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 10155.6}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 8954.38}, {'customer': 'Idlewood Electric Supply', 'revenue': 6826.14}, {'customer': 'Reflections L+M', 'revenue': 6388.1}, {'customer': 'Dominion Electric', 'revenue': 5854.07}, {'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 5710.5}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 5500.76}, {'customer': "Graham's Living", 'revenue': 4832.28}, {'customer': 'Loudoun Interiors LLC', 'revenue': 4088.64}, {'customer': 'Daniel House Club', 'revenue': 3747.0}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 3747.0}, {'customer': 'IBS Lighting', 'revenue': 3747.0}, {'customer': 'Lights Unlimited', 'revenue': 3697.0}, {'customer': 'CAI Designs', 'revenue': 3597.0}, {'customer': 'Lighting Studio', 'revenue': 3597.0}, {'customer': 'Aladdin Lighting & Supply, Inc', 'revenue': 3575.64}, {'customer': 'Lights on Design', 'revenue': 3425.64}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 3147.3}, {'customer': "Elaine Everett's Lighting", 'revenue': 2987.4}, {'customer': 'Union Lighting & Furnishings', 'revenue': 2877.6}, {'customer': 'Joseph Moretti Design', 'revenue': 2748.0}, {'customer': 'Lightology, LLC.com', 'revenue': 2598.0}, {'customer': 'Cregger Company, LLC', 'revenue': 2598.0}, {'customer': 'Light Lab Design', 'revenue': 2598.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 2448.0}, {'customer': 'The Brecher Company', 'revenue': 2448.0}, {'customer': 'Littman Bros Lighting', 'revenue': 2448.0}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 2416.14}, {'customer': 'First Coast Lighting & Fans', 'revenue': 2367.57}, {'customer': 'Shades of Light', 'revenue': 2338.2}, {'customer': 'Foundrylighting.com', 'revenue': 2321.07}, {'customer': 'Wilson Fans And Lighting', 'revenue': 2203.2}, {'customer': 'Light Gallery Plus', 'revenue': 2198.0}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 2104.38}, {'customer': 'Lightopia, LLC.', 'revenue': 2090.64}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 1897.47}, {'customer': 'Shelby Mae Interiors', 'revenue': 1651.6}, {'customer': 'COLLECTED DESIGN LLC', 'revenue': 1608.6}, {'customer': 'Alison Friedricks Interior', 'revenue': 1494.0}, {'customer': 'Chroma Home, LLC', 'revenue': 1374.0}, {'customer': 'Union Lighting & Home', 'revenue': 1328.97}, {'customer': 'Carpet Palace Bethesda DBA Designer Workshop', 'revenue': 1322.0}, {'customer': 'Anderson Design Studio', 'revenue': 1321.0}, {'customer': 'Bright Ideas LED', 'revenue': 1316.93}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 1299.0}, {'customer': 'Hye Lighting', 'revenue': 1299.0}, {'customer': 'Fan & Lighting World', 'revenue': 1299.0}, {'customer': 'Passion Lighting', 'revenue': 1299.0}, {'customer': 'M&M Lighting Co', 'revenue': 1299.0}, {'customer': 'Mayson Enterprise dba Aura Lighting', 'revenue': 1299.0}, {'customer': 'Coley Electric & Plumbing Sup', 'revenue': 1299.0}, {'customer': 'Complete Lighting of Tampa,Inc', 'revenue': 1299.0}, {'customer': 'The Shallotte Electric Store', 'revenue': 1299.0}, {'customer': 'Lighting First Ft. Myers', 'revenue': 1299.0}, {'customer': 'Revival Lighting', 'revenue': 1299.0}, {'customer': 'Posh HB LLC DBA Posh Home and Bath', 'revenue': 1299.0}, {'customer': 'Kendall Electric', 'revenue': 1299.0}, {'customer': 'Aura Interiors Inc', 'revenue': 1299.0}, {'customer': 'The Jarrell Company', 'revenue': 1299.0}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 1299.0}, {'customer': 'At Home LLC DBA Home Lighting', 'revenue': 1299.0}, {'customer': 'Styled Interiors', 'revenue': 1236.6}, {'customer': 'Lighting Direct NJ LLC', 'revenue': 1235.89}, {'customer': 'Lighting First - Bonita', 'revenue': 1208.07}, {'customer': 'Southern Lights', 'revenue': 1208.07}, {'customer': 'Capitol Lighting Gallery', 'revenue': 1208.07}, {'customer': 'Valencia Lighting & Design', 'revenue': 1208.07}, {'customer': 'Kitchen Concepts & Designs, LL', 'revenue': 1208.07}, {'customer': 'Light Art of Durango', 'revenue': 1208.07}, {'customer': 'Christies Lighting Gallery,LLC', 'revenue': 1208.07}, {'customer': 'Robinson Lighting Centre', 'revenue': 1208.07}, {'customer': 'Progressive Lighting', 'revenue': 1169.1}, {'customer': 'Capitol Lighting-ASN', 'revenue': 1169.1}, {'customer': 'Metro Showroom West County', 'revenue': 1169.1}, {'customer': 'Dolan NW LLC', 'revenue': 1169.1}, {'customer': 'Electric Supply Lighting', 'revenue': 1149.0}, {'customer': 'Urban Lights', 'revenue': 1149.0}, {'customer': 'Bee Ridge Lighting & Design', 'revenue': 1149.0}, {'customer': 'Capital Electric', 'revenue': 1149.0}, {'customer': 'The Lighting Hut by Wilson', 'revenue': 1149.0}, {'customer': 'Pine Lighting', 'revenue': 1149.0}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 1149.0}, {'customer': 'Davids Furniture Ltd.', 'revenue': 1149.0}, {'customer': 'Safavieh Outlet', 'revenue': 1149.0}, {'customer': 'One Stop Lighting', 'revenue': 1149.0}, {'customer': 'Elan Studio Lighting', 'revenue': 1149.0}, {'customer': 'Kim E Courtney Interiors', 'revenue': 1149.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1149.0}, {'customer': 'CES Aquisition LLC', 'revenue': 1149.0}, {'customer': 'Georgia Lighting', 'revenue': 1149.0}, {'customer': 'Capital City Lighting', 'revenue': 1149.0}, {'customer': 'BBC Lighting Company', 'revenue': 1149.0}, {'customer': 'Stokes Lighting Center', 'revenue': 1149.0}, {'customer': 'Sun Lighting', 'revenue': 1149.0}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 1149.0}, {'customer': 'Lighting First Naples', 'revenue': 1149.0}, {'customer': 'ABC Lighting Inc', 'revenue': 1149.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 1099.0}, {'customer': 'Dement Lighting', 'revenue': 1099.0}, {'customer': 'The Design Firm. Inc.', 'revenue': 1099.0}, {'customer': 'Cleveland Lighting', 'revenue': 1091.55}, {'customer': 'Amber Dawn Designs', 'revenue': 1070.01}, {'customer': '2514004  Ontario Inc O/A iLITE', 'revenue': 1068.57}, {'customer': 'Pine Tree Lighting', 'revenue': 1068.57}, {'customer': 'Elume Distinctive Lighting**', 'revenue': 1068.57}, {'customer': 'Lighting Superstore', 'revenue': 1068.57}, {'customer': 'Porter Lighting Sales, Inc.', 'revenue': 1039.2}, {'customer': 'Lofings Lighting Inc', 'revenue': 1022.07}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 1022.07}, {'customer': 'Luxury Lighting', 'revenue': 659.4}, {'customer': 'Shades of Light', 'revenue': 0.0}, {'customer': 'Lighting, Inc', 'revenue': 0.0}, {'customer': 'Galleria Lighting  E MAIL', 'revenue': 0.0}, {'customer': 'Light Bulbs Unlimited', 'revenue': 0.0}, {'customer': 'Tec of North Little Rock', 'revenue': 0.0}, {'customer': 'Moreau Enterprises/Aggieland', 'revenue': 0.0}, {'customer': 'Winsupply Owensboro KY Co', 'revenue': 0.0}, {'customer': 'McLoughlan Supplies Limited', 'revenue': 0.0}, {'customer': 'Lighting Connection', 'revenue': 0.0}, {'customer': 'Prima Lighting', 'revenue': 0.0}, {'customer': 'Naples Lamp Shop', 'revenue': 0.0}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': "Hinkley's Lighting Factory", 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
| SHY-10907-SG | Shyla 24'' Soft Gold Chandelier | SHYLA | 292,247.01 | 657 | — | 2026-6-23 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 22511.75}, {'customer': 'Build Drop Ship EDI', 'revenue': 21032.63}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 19488.29}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 12424.76}, {'customer': 'Lightopia, LLC.', 'revenue': 10343.07}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 9050.66}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 8043.93}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 6700.5}, {'customer': 'Decorative Lighting Inc', 'revenue': 6505.21}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 5743.49}, {'customer': 'Lighting First - Bonita', 'revenue': 4922.49}, {'customer': 'Melrose & Madison (AMZ)', 'revenue': 4891.63}, {'customer': 'Union Lighting & Home', 'revenue': 4700.7}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 4696.0}, {'customer': 'Lightology, LLC.com', 'revenue': 4039.5}, {'customer': 'One Kings Lane.com-ASN', 'revenue': 3910.5}, {'customer': "Graham's Living", 'revenue': 3903.21}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 3761.07}, {'customer': 'Foundrylighting.com', 'revenue': 3428.5}, {'customer': 'Southern Lights', 'revenue': 3426.28}, {'customer': 'Lights Unlimited', 'revenue': 2945.0}, {'customer': 'Lighting First Naples', 'revenue': 2499.78}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 2494.13}, {'customer': 'First Coast Lighting & Fans', 'revenue': 2316.5}, {'customer': 'Montreal Luminaire', 'revenue': 2088.0}, {'customer': 'Progressive Lighting', 'revenue': 2069.1}, {'customer': 'Decorum', 'revenue': 1810.71}, {'customer': 'Dominion Electric', 'revenue': 1800.0}, {'customer': 'Brothers Lighting &Fan Gallery', 'revenue': 1638.07}, {'customer': 'M&M Lighting Co', 'revenue': 1638.07}, {'customer': 'Vida Events & Design LLC', 'revenue': 1610.0}, {'customer': 'Union Lighting & Home', 'revenue': 1531.71}, {'customer': 'Daniel House Club', 'revenue': 1497.0}, {'customer': "Montgomery's Furniture", 'revenue': 1497.0}, {'customer': 'Nova Lighting', 'revenue': 1497.0}, {'customer': 'Lifestyles Stores, Inc', 'revenue': 1497.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 1448.0}, {'customer': 'Grand Rapids Lighting', 'revenue': 1448.0}, {'customer': 'Kathy Kuo Home', 'revenue': 1432.12}, {'customer': 'Low Country Lighting Studio', 'revenue': 1399.0}, {'customer': 'Home Depot-ASN', 'revenue': 1350.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 1347.3}, {'customer': 'Lights of Oconee', 'revenue': 1332.57}, {'customer': 'Dolan NW LLC', 'revenue': 1303.2}, {'customer': 'Metro Showroom West County', 'revenue': 1215.0}, {'customer': 'Union Lighting & Furnishings', 'revenue': 1158.4}, {'customer': 'Kristen Morrison Interiors', 'revenue': 1148.0}, {'customer': 'Elements', 'revenue': 1003.62}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 998.0}, {'customer': 'Mathes of Alabama Electric Supply Co., Inc.', 'revenue': 998.0}, {'customer': 'The Lighting Marketplace DBA Fixture Farm', 'revenue': 998.0}, {'customer': 'Sundial Home Products LLC', 'revenue': 998.0}, {'customer': 'City Plumbing & Electric', 'revenue': 998.0}, {'customer': 'Cape Electrical Sup(Southfork)', 'revenue': 998.0}, {'customer': 'Lighting Etc.', 'revenue': 998.0}, {'customer': 'Lighting Connection', 'revenue': 998.0}, {'customer': 'Luxur Lighting', 'revenue': 949.0}, {'customer': 'JCM Lighting and Design, DBA The Local Lighting Shop', 'revenue': 949.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 949.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 928.14}, {'customer': 'Candelabra Light & Design.com DBA Meadow Blu', 'revenue': 917.5}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 900.0}, {'customer': 'Frooogal -DBA  France & Son', 'revenue': 900.0}, {'customer': 'Avenue Lighting & Design', 'revenue': 899.1}, {'customer': 'Lamps.com', 'revenue': 883.02}, {'customer': 'Paradise Lighting', 'revenue': 880.02}, {'customer': 'Beautiful Lights', 'revenue': 869.07}, {'customer': 'Classic Lighting & Design, Inc', 'revenue': 868.5}, {'customer': "Efird's Interiors, Inc.", 'revenue': 854.1}, {'customer': 'Brandywine Lighting Gallery', 'revenue': 837.0}, {'customer': 'Capital Electric', 'revenue': 814.0}, {'customer': "Mahlander's Appliance Lighting", 'revenue': 814.0}, {'customer': 'The Lighting Studio', 'revenue': 814.0}, {'customer': 'Winsupply Owensboro KY Co', 'revenue': 814.0}, {'customer': 'Lighting By Design - Dec Den', 'revenue': 769.0}, {'customer': 'Lando Lighting', 'revenue': 769.0}, {'customer': 'Accent Lighting, Inc.', 'revenue': 748.5}, {'customer': 'Hye Lighting', 'revenue': 720.0}, {'customer': 'Light Bulbs Etc (Montclair)', 'revenue': 699.05}, {'customer': 'Prima Lighting', 'revenue': 675.0}, {'customer': 'Redefined Lighting, LLC', 'revenue': 624.0}, {'customer': 'Monet Design', 'revenue': 574.0}, {'customer': 'The Beach Home, LLC', 'revenue': 574.0}, {'customer': 'Brick House Designs', 'revenue': 574.0}, {'customer': 'Crampton Lighting Design, Inc.', 'revenue': 574.0}, {'customer': 'Asburys Furnishings & Design', 'revenue': 574.0}, {'customer': 'Crimson Design Group', 'revenue': 574.0}, {'customer': 'Kelly Lord Designs', 'revenue': 574.0}, {'customer': 'Oak Highland Design dba Dec De', 'revenue': 563.0}, {'customer': 'Abode Made LLC', 'revenue': 563.0}, {'customer': 'JMH Designs', 'revenue': 563.0}, {'customer': 'CasaBella', 'revenue': 563.0}, {'customer': 'KV Design Co', 'revenue': 563.0}, {'customer': 'Mckenzie Baker Interiors', 'revenue': 563.0}, {'customer': 'Techtron Products, Inc', 'revenue': 563.0}, {'customer': 'West Coast Cabinets', 'revenue': 563.0}, {'customer': 'Inside Source LLC', 'revenue': 519.01}, {'customer': 'Carlyle Design Studio', 'revenue': 518.0}, {'customer': 'J and G Central Coast Interiors DBA Chic Interiors', 'revenue': 518.0}, {'customer': 'Serenity Design', 'revenue': 518.0}, {'customer': 'Kelley Elizabeth Interiors', 'revenue': 518.0}, {'customer': 'Cozy Development', 'revenue': 518.0}, {'customer': 'The Ervin Group', 'revenue': 518.0}, {'customer': 'Rast Road LLC DBA Emily Wood Design Co.', 'revenue': 518.0}, {'customer': 'Craven Gardner Design & Build', 'revenue': 518.0}, {'customer': 'Coastline Copper DBA The Henry Haus', 'revenue': 518.0}, {'customer': 'Lighting World Decorator', 'revenue': 499.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 499.0}, {'customer': 'Cregger Company, LLC', 'revenue': 499.0}, {'customer': 'IBS Lighting', 'revenue': 499.0}, {'customer': 'Burgess Lighting', 'revenue': 499.0}, {'customer': 'Creative Interiors, LTD', 'revenue': 499.0}, {'customer': 'Raymond Desteiger, Inc.', 'revenue': 499.0}, {'customer': 'Shannon Terry Interiors', 'revenue': 499.0}, {'customer': 'Light Bulbs, Etc. (Orange)', 'revenue': 499.0}, {'customer': 'Design Trade Service', 'revenue': 499.0}, {'customer': 'Chroma Home, LLC', 'revenue': 499.0}, {'customer': 'Light Idaho, LLC DBA Wolfe Lighting Twin Falls', 'revenue': 499.0}, {'customer': 'Lumi Lighting & Home Design', 'revenue': 499.0}, {'customer': 'The Jarrell Company', 'revenue': 499.0}, {'customer': 'Fort Worth Lighting', 'revenue': 499.0}, {'customer': 'Masterpiece Lighting Inc', 'revenue': 499.0}, {'customer': 'Magnolia Lighting & Electric', 'revenue': 499.0}, {'customer': 'Sun Lighting', 'revenue': 499.0}, {'customer': 'The Shallotte Electric Store', 'revenue': 499.0}, {'customer': 'Wasatch Lighting, Inc', 'revenue': 499.0}, {'customer': 'Littman Bros Lighting', 'revenue': 499.0}, {'customer': 'Construction Resources Company LLC', 'revenue': 499.0}, {'customer': 'Electrimat', 'revenue': 495.0}, {'customer': 'S. Mahoney Designs LLC DBA Mahoney Design Studio', 'revenue': 478.55}, {'customer': 'Haus Appeal LLC', 'revenue': 474.05}, {'customer': 'Litemode Limited', 'revenue': 464.07}, {'customer': 'Minnesota Lighting Fireplace', 'revenue': 464.07}, {'customer': "Hinkley's Lighting Factory", 'revenue': 464.07}, {'customer': 'Cleveland Lighting', 'revenue': 464.07}, {'customer': 'Broadway Showroom', 'revenue': 464.07}, {'customer': 'Energy Plus', 'revenue': 450.0}, {'customer': 'Thompson Supply Co.', 'revenue': 450.0}, {'customer': 'SideDoor', 'revenue': 450.0}, {'customer': 'CAI Designs', 'revenue': 450.0}, {'customer': 'Pelican Equipment Rentals, Inc', 'revenue': 450.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 450.0}, {'customer': 'Good Friend Electric', 'revenue': 450.0}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 450.0}, {'customer': 'Reflections L+M', 'revenue': 450.0}, {'customer': 'Best Lighting', 'revenue': 450.0}, {'customer': 'Crystorama Accm', 'revenue': 450.0}, {'customer': 'Warshauer Electric', 'revenue': 450.0}, {'customer': 'LJP dba Southside Lighting', 'revenue': 450.0}, {'customer': 'BBC Lighting Company', 'revenue': 450.0}, {'customer': 'Prosource , LLC', 'revenue': 450.0}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 450.0}, {'customer': 'Standard Electric', 'revenue': 450.0}, {'customer': 'Briggs Inc of Omaha', 'revenue': 450.0}, {'customer': 'Ricks Lighting and Supply', 'revenue': 450.0}, {'customer': 'Rittenhouse Electric Supply Co', 'revenue': 450.0}, {'customer': 'Coley Electric & Plumbing Sup', 'revenue': 450.0}, {'customer': 'Net Retailers dba Luxe Decor', 'revenue': 450.0}, {'customer': 'Lighting Connection', 'revenue': 450.0}, {'customer': 'Signature Lighting and Fans', 'revenue': 450.0}, {'customer': 'Nantucket Lightshop', 'revenue': 450.0}, {'customer': 'The Saltbox', 'revenue': 450.0}, {'customer': 'SKD Studios', 'revenue': 450.0}, {'customer': "Wilkinson's House of Lights", 'revenue': 450.0}, {'customer': 'Manasquan Lighting', 'revenue': 450.0}, {'customer': 'Overstock.com, Inc-Auto EDI', 'revenue': 450.0}, {'customer': 'Fanwerks & Lighting Inc', 'revenue': 450.0}, {'customer': 'Broad Street Interiors', 'revenue': 450.0}, {'customer': 'Urban Lights', 'revenue': 450.0}, {'customer': 'Fifth and College Tile and Design Co.', 'revenue': 450.0}, {'customer': 'Gallery South Inc', 'revenue': 450.0}, {'customer': 'Flemington Lighting & Fan', 'revenue': 450.0}, {'customer': 'Madison Lighting', 'revenue': 450.0}, {'customer': 'J & B Supply Inc.', 'revenue': 450.0}, {'customer': 'Joseph Electric Company', 'revenue': 450.0}, {'customer': "Horton's Home Lighting", 'revenue': 427.5}, {'customer': 'Mars Electric Co.', 'revenue': 418.5}, {'customer': 'The Lighting Design Co.', 'revenue': 418.5}, {'customer': 'Lighting First Ft. Myers', 'revenue': 418.5}, {'customer': 'LDB Holdings, LLC', 'revenue': 405.0}, {'customer': 'Wilson Lighting - St Louis', 'revenue': 405.0}, {'customer': 'Brandino Brass Co', 'revenue': 405.0}, {'customer': 'Lighting, Inc', 'revenue': 405.0}, {'customer': 'Wilson Fans And Lighting', 'revenue': 405.0}, {'customer': 'Precision Diamante', 'revenue': 382.5}, {'customer': 'Live Edge USA DBA Brick Mill', 'revenue': 349.3}, {'customer': 'Hampton Home Dinettes', 'revenue': 349.3}, {'customer': 'Richards Lighting', 'revenue': 349.3}, {'customer': 'Made New Interiors and Decor, LLC', 'revenue': 349.3}, {'customer': 'The Electrical &Plumbing Store', 'revenue': 315.0}, {'customer': 'Designer Blvd, LLC', 'revenue': 315.0}, {'customer': 'Interior Design House', 'revenue': 315.0}, {'customer': 'Plumb Supply Co', 'revenue': 299.4}, {'customer': "Graham's Lighting", 'revenue': 249.5}, {'customer': '43rd Street Lighting, Inc.', 'revenue': 225.0}, {'customer': 'One Stop Lighting', 'revenue': 225.0}, {'customer': 'Lighting Emporium', 'revenue': 225.0}, {'customer': 'Lighting Aura', 'revenue': 225.0}, {'customer': 'Bird Stairs', 'revenue': 0.0}, {'customer': 'Julie Bova Interior Design', 'revenue': 0.0}, {'customer': 'Carrington Lighting', 'revenue': 0.0}] | [{'item': 'SHY-10909-SG', 'desc': "Shyla 32'' Soft Gold Chandelier", 'available': 44}] |
| ARA-10269-MK-ST | Aragon 58.75'' LED Matte Black Chandelier | COL127 | 265,753.16 | 102 | — | 2026-8-18 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 21074.15}, {'customer': 'Capital Electric', 'revenue': 19662.0}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 15561.77}, {'customer': 'Lightology, LLC.com', 'revenue': 11387.71}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 11270.93}, {'customer': 'Elements', 'revenue': 9959.3}, {'customer': 'Passion Lighting', 'revenue': 9947.0}, {'customer': 'Build Drop Ship EDI', 'revenue': 9086.56}, {'customer': 'IBS Lighting', 'revenue': 8805.91}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 8547.0}, {'customer': 'Dolan NW LLC', 'revenue': 7602.3}, {'customer': 'North Coast Lighting', 'revenue': 7275.0}, {'customer': "Graham's Living", 'revenue': 6975.0}, {'customer': 'Construction Resources Company LLC', 'revenue': 5698.0}, {'customer': 'Urban Lights', 'revenue': 5648.0}, {'customer': 'Yellow Pine LLC', 'revenue': 5299.0}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 5077.52}, {'customer': 'Hobrecht Lighting Co., Inc.', 'revenue': 5000.0}, {'customer': 'CoCo Curtain Studio', 'revenue': 5000.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 3749.5}, {'customer': 'Swine Design LLC', 'revenue': 3366.79}, {'customer': 'Lee Douglas Interiors, Inc.', 'revenue': 3277.0}, {'customer': 'Designs with you in Mind', 'revenue': 3222.98}, {'customer': 'Inside Source LLC', 'revenue': 3124.0}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 3020.18}, {'customer': 'Crystorama Accm', 'revenue': 2995.0}, {'customer': 'Light Idaho, LLC DBA Wolfe Lighting Twin Falls', 'revenue': 2895.05}, {'customer': 'CES Aquisition LLC', 'revenue': 2849.0}, {'customer': 'Northern Lighting', 'revenue': 2849.0}, {'customer': 'M&M Lighting Co', 'revenue': 2849.0}, {'customer': 'Jerome Lessard Design', 'revenue': 2812.32}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 2799.0}, {'customer': 'Luminous Trends Inc DBA Modern Luxury by LT)', 'revenue': 2799.0}, {'customer': 'Royce Collection Inc.', 'revenue': 2799.0}, {'customer': 'LJP dba Southside Lighting', 'revenue': 2799.0}, {'customer': 'Nimbus Nine Inc.', 'revenue': 2749.0}, {'customer': 'Vogue Lighting', 'revenue': 2749.0}, {'customer': 'Lights Unlimited', 'revenue': 2749.0}, {'customer': 'Lighting Innovation', 'revenue': 2671.92}, {'customer': 'Imagine More', 'revenue': 2603.07}, {'customer': "Mahlander's Appliance Lighting", 'revenue': 2500.0}, {'customer': 'Dominion Electric', 'revenue': 2500.0}, {'customer': 'The Lighting Design Co.', 'revenue': 2500.0}, {'customer': 'Lighting, Inc', 'revenue': 2474.1}, {'customer': 'Wilson Fans And Lighting', 'revenue': 2474.1}, {'customer': 'Christies Lighting Gallery,LLC', 'revenue': 2325.0}, {'customer': 'Krell Lighting & Electric Supp', 'revenue': 2250.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 2250.0}, {'customer': 'Lightopia, LLC.', 'revenue': 2250.0}, {'customer': 'Robert Sales Inc #109', 'revenue': 1875.0}, {'customer': 'Hajoca Corporation', 'revenue': 1750.0}, {'customer': 'Accent Lighting Galleries', 'revenue': 0.0}, {'customer': 'Brad Ramsey Interiors', 'revenue': 0.0}] | [{'item': 'ARA-10261-SB-ST', 'desc': "Aragon 4.5'' LED Soft Brass Sconce", 'available': 85}, {'item': 'ARA-10261-MK-ST', 'desc': "Aragon 4.5'' LED Matte Black Sconce", 'available': 70}, {'item': 'ARA-10261-MK', 'desc': "Aragon 4.5'' LED Matte Black Sconce", 'available': 63}, {'item': 'ARA-10261-SB', 'desc': "Aragon 4.5'' LED Soft Brass Sconce", 'available': 51}, {'item': 'ARA-10266-MK', 'desc': "Aragon 48'' LED Matte Black Chandelier", 'available': 44}, {'item': 'ARA-10267-MK-ST', 'desc': "Aragon 56'' LED Matte Black Linear Chandelier", 'available': 43}, {'item': 'ARA-10266-MK-ST', 'desc': "Aragon 46.75'' LED Matte Black Chandelier", 'available': 37}, {'item': 'ARA-10266-SB-ST', 'desc': "Aragon 46.75'' LED Soft Brass Chandelier", 'available': 32}, {'item': 'ARA-10267-SB-ST', 'desc': "Aragon 56'' LED Soft Brass Linear Chandelier", 'available': 28}, {'item': 'ARA-10267-SB', 'desc': "Aragon 56'' LED Soft Brass Linear Chandelier", 'available': 23}, {'item': 'ARA-10265-MK-ST', 'desc': "Aragon 34.75'' LED Matte Black Chandelier", 'available': 22}, {'item': 'ARA-10266-SB', 'desc': "Aragon 48'' LED Soft Brass Chandelier", 'available': 18}, {'item': 'ARA-10265-SB-ST', 'desc': "Aragon 34.75'' LED Soft Brass Chandelier", 'available': 17}, {'item': 'ARA-10265-MK', 'desc': "Aragon 36'' LED Matte Black Chandelier", 'available': 14}, {'item': 'ARA-10267-MK', 'desc': "Aragon 56'' LED Matte Black Linear Chandelier", 'available': 13}, {'item': 'ARA-10265-SB', 'desc': "Aragon 36'' LED Soft Brass Chandelier", 'available': 11}, {'item': 'ARA-10268-SB', 'desc': "Aragon 48'' LED Soft Brass Chandelier", 'available': 3}, {'item': 'ARA-10264-SB-ST', 'desc': "Aragon 22.75'' LED Soft Brass Chandelier", 'available': 3}, {'item': 'ARA-10268-SB-ST', 'desc': "Aragon 46.75'' LED Soft Brass Chandelier", 'available': 3}, {'item': 'ARA-10269-SB', 'desc': "Aragon 60'' LED Soft Brass Chandelier", 'available': 2}, {'item': 'ARA-10269-SB-ST', 'desc': "Aragon 58.75'' LED Soft Brass Chandelier", 'available': 2}] |
| 505-MT | Broche 16'' Matte White Semi Flush Mount | COL100 | 230,169.06 | 971 | — | 2026-6-26 | [{'customer': 'Melrose & Madison (AMZ)', 'revenue': 39184.64}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 25107.36}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 23650.0}, {'customer': 'Shades of Light', 'revenue': 17460.0}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 16329.25}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 16039.95}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 10662.5}, {'customer': 'Build Drop Ship EDI', 'revenue': 8137.5}, {'customer': 'Houzz.com-Auto EDI', 'revenue': 5987.5}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 5563.72}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 4050.0}, {'customer': 'Foundrylighting.com', 'revenue': 3162.5}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 2250.0}, {'customer': 'Lightology, LLC.com', 'revenue': 1930.0}, {'customer': 'Lighting Etc.', 'revenue': 1750.0}, {'customer': 'Lamps.com', 'revenue': 1627.5}, {'customer': 'Lightopia, LLC.', 'revenue': 1622.5}, {'customer': 'Interior Design House', 'revenue': 1500.0}, {'customer': 'Overstock.com, Inc-Auto EDI', 'revenue': 1250.0}, {'customer': "Fleming's of Cohasset, Inc.", 'revenue': 1250.0}, {'customer': 'Tout Le Monde Interiors LLC', 'revenue': 1152.0}, {'customer': 'Kendall Electric', 'revenue': 1000.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1000.0}, {'customer': 'Continental Lighting Corp.', 'revenue': 1000.0}, {'customer': "Horton's Home Lighting", 'revenue': 950.0}, {'customer': 'Cates Lighting at Elements', 'revenue': 750.0}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 750.0}, {'customer': 'Manasquan Lighting', 'revenue': 750.0}, {'customer': 'Wostbrock Home', 'revenue': 750.0}, {'customer': 'Ocean Pacific Lighting', 'revenue': 750.0}, {'customer': 'Brooke & Lou', 'revenue': 750.0}, {'customer': 'Wilson Fans And Lighting', 'revenue': 675.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 675.0}, {'customer': 'RAINBOW LIGHTING INC', 'revenue': 600.0}, {'customer': 'Voss Designs', 'revenue': 576.0}, {'customer': 'Union Lighting & Home', 'revenue': 511.5}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 500.0}, {'customer': 'Dominion Electric', 'revenue': 500.0}, {'customer': 'Home Lighting of Frazer', 'revenue': 500.0}, {'customer': 'Gross Lighting & Home', 'revenue': 500.0}, {'customer': 'James and Company Ltd.', 'revenue': 500.0}, {'customer': 'Candelabra Light & Design.com DBA Meadow Blu', 'revenue': 500.0}, {'customer': 'Southern Lights', 'revenue': 482.5}, {'customer': 'Paramont-Evergreen Oak Inc.', 'revenue': 482.5}, {'customer': 'Raymond Desteiger, Inc.', 'revenue': 475.0}, {'customer': 'Fan & Lighting World', 'revenue': 475.0}, {'customer': 'Shop Freely LLC.com', 'revenue': 470.0}, {'customer': 'Del Mar Designs.com', 'revenue': 470.0}, {'customer': 'M&M Lighting Co', 'revenue': 465.0}, {'customer': '1 800 MY LAMPS.com', 'revenue': 465.0}, {'customer': 'Wilson Lighting - St Louis', 'revenue': 450.0}, {'customer': 'Progressive Lighting', 'revenue': 450.0}, {'customer': '2514004  Ontario Inc O/A iLITE', 'revenue': 429.29}, {'customer': 'Wage Lighting & Design', 'revenue': 425.0}, {'customer': 'Tide & Table', 'revenue': 400.0}, {'customer': 'Naples Lamp Shop', 'revenue': 375.0}, {'customer': 'Kate.H.Design', 'revenue': 313.0}, {'customer': 'Westend Interiors', 'revenue': 313.0}, {'customer': 'Stewart Design Group', 'revenue': 313.0}, {'customer': 'Moss Aaron', 'revenue': 313.0}, {'customer': 'Dianne Davant and Associates', 'revenue': 313.0}, {'customer': 'Fashion Light Center, LLC', 'revenue': 300.0}, {'customer': 'Koval Building & Plumbing Supply Co.', 'revenue': 288.0}, {'customer': 'Ashley Wells Design', 'revenue': 288.0}, {'customer': 'The Beach Home, LLC', 'revenue': 288.0}, {'customer': 'Blufish Designs', 'revenue': 288.0}, {'customer': 'Annie Baker Design', 'revenue': 288.0}, {'customer': 'River City Lighting', 'revenue': 266.05}, {'customer': 'Lighting By Fox, LLC', 'revenue': 250.0}, {'customer': 'Neenas Lighting', 'revenue': 250.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 250.0}, {'customer': 'Desert Lighting Solutions', 'revenue': 250.0}, {'customer': 'The Light House of Lewes', 'revenue': 250.0}, {'customer': 'Pine Lighting', 'revenue': 250.0}, {'customer': 'Scott Electric', 'revenue': 250.0}, {'customer': 'Decorum', 'revenue': 250.0}, {'customer': 'CoCo Curtain Studio', 'revenue': 250.0}, {'customer': 'Bayside Electric Supply', 'revenue': 250.0}, {'customer': 'Cregger Company, LLC', 'revenue': 250.0}, {'customer': 'Erwin Development, DBA The Lighting Studio', 'revenue': 250.0}, {'customer': 'Cayce Mill Supply Co.', 'revenue': 250.0}, {'customer': 'City Lights', 'revenue': 250.0}, {'customer': 'Coastal Lighting and Supply', 'revenue': 250.0}, {'customer': 'Illuminate Lighting Design, Formerly 17-90 Lighting Inc.', 'revenue': 250.0}, {'customer': 'U.S. 31 Supply Inc', 'revenue': 250.0}, {'customer': 'Rite Rug Co', 'revenue': 250.0}, {'customer': 'CES Aquisition LLC', 'revenue': 250.0}, {'customer': 'Pelican Equipment Rentals, Inc', 'revenue': 250.0}, {'customer': 'Logan Square DBA Studio 41', 'revenue': 250.0}, {'customer': 'Greer Lighting Center', 'revenue': 250.0}, {'customer': 'PAYNES GRAY', 'revenue': 250.0}, {'customer': 'Dulles Electric Supply', 'revenue': 250.0}, {'customer': 'Elektra Lights and Fans', 'revenue': 250.0}, {'customer': 'El Design', 'revenue': 250.0}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 250.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 250.0}, {'customer': 'King Electric Company Inc.', 'revenue': 250.0}, {'customer': 'Lighting & Lamps', 'revenue': 250.0}, {'customer': 'Biggins Lighting & Electric Su', 'revenue': 250.0}, {'customer': 'Lighting Emporium', 'revenue': 250.0}, {'customer': 'Lighting Showcase', 'revenue': 250.0}, {'customer': 'Alex Dee Home Accessories &Ltg', 'revenue': 250.0}, {'customer': 'Magnolia Lighting & Electric', 'revenue': 250.0}, {'customer': 'Premier Bath Lighting&Hardware', 'revenue': 250.0}, {'customer': 'Rittenhouse Electric Supply Co', 'revenue': 250.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 250.0}, {'customer': 'The Light Center', 'revenue': 250.0}, {'customer': 'The Light Post', 'revenue': 250.0}, {'customer': 'Lighting By Lavonne', 'revenue': 250.0}, {'customer': 'Cleveland Lighting', 'revenue': 250.0}, {'customer': 'Just Lights', 'revenue': 250.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 250.0}, {'customer': 'Retail Convergence.com, LP ASN (Rue La La)', 'revenue': 250.0}, {'customer': 'Inline Electric Supply', 'revenue': 250.0}, {'customer': 'Standard Electric', 'revenue': 250.0}, {'customer': 'Urban Lights', 'revenue': 250.0}, {'customer': 'North Coast Lighting', 'revenue': 242.5}, {'customer': 'Georgia Lighting', 'revenue': 232.5}, {'customer': 'Mayson Enterprise dba Aura Lighting', 'revenue': 232.5}, {'customer': "Graham's Living", 'revenue': 232.5}, {'customer': 'Galaxie Lighting', 'revenue': 232.5}, {'customer': 'Robinson Lighting Centre', 'revenue': 232.5}, {'customer': 'Littman Bros Lighting.com', 'revenue': 232.5}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 232.5}, {'customer': 'Haus Appeal LLC', 'revenue': 232.5}, {'customer': 'Tidewater Lighting & Design', 'revenue': 232.5}, {'customer': 'Aladdin Lighting & Supply, Inc', 'revenue': 232.5}, {'customer': 'Wilson Lighting of Naples', 'revenue': 225.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 225.0}, {'customer': "Efird's Interiors, Inc.", 'revenue': 225.0}, {'customer': 'RLA Lighting', 'revenue': 200.0}, {'customer': 'Made New Interiors and Decor, LLC', 'revenue': 175.0}, {'customer': 'Harbour Lighting LLC', 'revenue': 175.0}, {'customer': 'Prima Lighting', 'revenue': 125.0}, {'customer': 'The Glow Works Inc', 'revenue': 125.0}, {'customer': 'The Electrical &Plumbing Store', 'revenue': 86.8}, {'customer': 'Rhobin Delacruz Designs', 'revenue': 0.0}, {'customer': 'The Newburyport Lighting Co', 'revenue': 0.0}, {'customer': 'Haven and Dwell', 'revenue': 0.0}] | [{'item': '531-GA', 'desc': "Broche 6'' Antique Gold Sconce", 'available': 581}, {'item': '501-GA', 'desc': "Broche 8.5'' Antique Gold Sconce", 'available': 372}, {'item': '531-MT', 'desc': "Broche 6'' Matte White Sconce", 'available': 236}, {'item': '505-GA', 'desc': "Broche 16'' Antique Gold Semi Flush Mount", 'available': 212}, {'item': '531-SA', 'desc': "Broche 6'' Antique Silver Sconce", 'available': 210}, {'item': '517-GA_CEILING', 'desc': "Broche 24.5'' Antique Gold Semi Flush Mount", 'available': 203}, {'item': '517-GA', 'desc': "Broche 24.5'' Antique Gold Chandelier", 'available': 202}, {'item': '533-GA', 'desc': "Broche 27'' Antique Gold Chandelier", 'available': 172}, {'item': '519-GA_CEILING', 'desc': "Broche 30'' Antique Gold Semi Flush Mount", 'available': 150}, {'item': '519-GA', 'desc': "Broche 30'' Antique Gold Chandelier", 'available': 147}, {'item': '507-GA', 'desc': "Broche 24'' Antique Gold Semi Flush Mount", 'available': 142}, {'item': '566-MT', 'desc': "Broche 23'' Matte White Chandelier", 'available': 120}, {'item': '513-GA', 'desc': "Broche 14'' Antique Gold Chandelier", 'available': 113}, {'item': '513-GA_CEILING', 'desc': "Broche 14'' Antique Gold Semi Flush Mount", 'available': 113}, {'item': '534-MT', 'desc': "Broche 28'' Matte White Chandelier", 'available': 105}, {'item': '500W-MT', 'desc': "Broche 11'' Matte White Sconce", 'available': 100}, {'item': '500-MT', 'desc': "Broche 11'' Matte White Flush Mount", 'available': 100}, {'item': '510-GA', 'desc': "Broche 16'' Antique Gold Flush Mount", 'available': 95}, {'item': '514-GA', 'desc': "Broche 11'' Antique Gold Chandelier", 'available': 92}, {'item': '561-GA', 'desc': "Broche 8.25'' Antique Gold Sconce", 'available': 92}, {'item': '562-GA', 'desc': "Broche 12'' Antique Gold Sconce", 'available': 87}, {'item': '566-CT', 'desc': "Broche 23'' Champagne Green Tea Chandelier", 'available': 83}, {'item': '568-GA', 'desc': "Broche 32'' Antique Gold Chandelier", 'available': 83}, {'item': '566-GA', 'desc': "Broche 23'' Antique Gold Chandelier", 'available': 82}, {'item': '562-MT', 'desc': "Broche 12'' Matte White Sconce", 'available': 74}, {'item': '501-SA', 'desc': "Broche 8.5'' Antique Silver Sconce", 'available': 70}, {'item': '517-MT_CEILING', 'desc': "Broche 24.5'' Matte White Semi Flush Mount", 'available': 70}, {'item': '517-MT', 'desc': "Broche 24.5'' Matte White Chandelier", 'available': 70}, {'item': '537-GA', 'desc': "Broche 53.5'' Antique Gold Linear Chandelier", 'available': 69}, {'item': '531-OP-MT', 'desc': "Broche 6'' Matte White Sconce", 'available': 64}, {'item': '511-MT', 'desc': "Broche 8'' Matte White Sconce", 'available': 56}, {'item': 'BRH-M520-GA', 'desc': "Broche 20'' Antique Gold Mirror", 'available': 56}, {'item': '510-MT', 'desc': "Broche 16'' Matte White Flush Mount", 'available': 55}, {'item': '517-SA_CEILING', 'desc': "Broche 24.5'' Antique Silver Semi Flush Mount", 'available': 54}, {'item': '516-GA', 'desc': "Broche 16'' Antique Gold Chandelier", 'available': 54}, {'item': '517-SA', 'desc': "Broche 24.5'' Antique Silver Chandelier", 'available': 54}, {'item': '564-GA', 'desc': "Broche 18'' Antique Gold Pendant", 'available': 52}, {'item': '531-OP-SA', 'desc': "Broche 6'' Antique Silver Sconce", 'available': 50}, {'item': '501-EB', 'desc': "Broche 8.5'' English Bronze Sconce", 'available': 49}, {'item': '518-SA', 'desc': "Broche 24'' Antique Silver Chandelier", 'available': 48}, {'item': '560-GA', 'desc': "Broche 20.75'' Antique Gold Semi Flush Mount", 'available': 48}, {'item': '518-GA', 'desc': "Broche 24'' Antique Gold Chandelier", 'available': 48}, {'item': '573-OP-SA', 'desc': "Broche 25'' Antique Silver Bathroom Vanity", 'available': 47}, {'item': '500W-GA', 'desc': "Broche 11'' Antique Gold Sconce", 'available': 46}, {'item': '500-GA', 'desc': "Broche 11'' Antique Gold Flush Mount", 'available': 46}, {'item': '505-SA', 'desc': "Broche 16'' Antique Silver Semi Flush Mount", 'available': 44}, {'item': 'BRH-M520-MT', 'desc': "Broche 20'' Matte White Mirror", 'available': 42}, {'item': '504-EB-GA', 'desc': "Broche 16'' English Bronze + Antique Gold Chandelier", 'available': 41}, {'item': '503-GA-SA', 'desc': "Broche 18'' Antique Gold + Antique Silver Bathroom Vanity", 'available': 41}, {'item': '533-MT', 'desc': "Broche 27'' Matte White Chandelier", 'available': 40}, {'item': 'BRH-M520-SA', 'desc': "Broche 20'' Antique Silver Mirror", 'available': 40}, {'item': '571-OP-MT', 'desc': "Broche 6.5'' Matte White Sconce", 'available': 38}, {'item': '511-SA', 'desc': "Broche 8'' Antique Silver Sconce", 'available': 37}, {'item': '534-GA', 'desc': "Broche 28'' Antique Gold Chandelier", 'available': 35}, {'item': 'BRH-M530-GA', 'desc': "Broche 30'' Antique Gold Mirror", 'available': 33}, {'item': '533-SA', 'desc': "Broche 27'' Antique Silver Chandelier", 'available': 30}, {'item': '506-EB-GA', 'desc': "Broche 21'' English Bronze + Antique Gold Chandelier", 'available': 29}, {'item': 'BRH-M524-MT', 'desc': "Broche 24'' Matte White Mirror", 'available': 29}, {'item': '571-OP-GA', 'desc': "Broche 6.5'' Antique Gold Sconce", 'available': 28}, {'item': 'BRH-M530-SA', 'desc': "Broche 30'' Antique Silver Mirror", 'available': 27}, {'item': '566-SA', 'desc': "Broche 23'' Antique Silver Chandelier", 'available': 26}, {'item': 'BRH-M524-GA', 'desc': "Broche 24'' Antique Gold Mirror", 'available': 25}, {'item': '561-MT', 'desc': "Broche 8.25'' Matte White Sconce", 'available': 24}, {'item': '561-SA', 'desc': "Broche 8.25'' Antique Silver Sconce", 'available': 24}, {'item': '565-MT_CEILING', 'desc': "Broche 9'' Matte White Semi Flush Mount", 'available': 23}, {'item': '535-MT', 'desc': "Broche 18'' LED Matte White Chandelier", 'available': 23}, {'item': '535-MT_CEILING', 'desc': "Broche 18'' LED Matte White Semi Flush Mount", 'available': 23}, {'item': '515-GA', 'desc': "Broche 29'' Antique Gold Chandelier", 'available': 22}, {'item': '565-MT', 'desc': "Broche 9'' Matte White Chandelier", 'available': 22}, {'item': 'BRH-M530-MT', 'desc': "Broche 30'' Matte White Mirror", 'available': 22}, {'item': '537-SA', 'desc': "Broche 53.5'' Antique Silver Linear Chandelier", 'available': 22}, {'item': '501-MT', 'desc': "Broche 8.5'' Matte White Sconce", 'available': 21}, {'item': '560-MT', 'desc': "Broche 20.75'' Matte White Semi Flush Mount", 'available': 20}, {'item': '534-SA', 'desc': "Broche 28'' Antique Silver Chandelier", 'available': 20}, {'item': '507-SA', 'desc': "Broche 24'' Antique Silver Semi Flush Mount", 'available': 18}, {'item': '519-SA', 'desc': "Broche 30'' Antique Silver Chandelier", 'available': 18}, {'item': '562-SA', 'desc': "Broche 12'' Antique Silver Sconce", 'available': 18}, {'item': '519-SA_CEILING', 'desc': "Broche 30'' Antique Silver Semi Flush Mount", 'available': 17}, {'item': '535-SA', 'desc': "Broche 18'' LED Antique Silver Chandelier", 'available': 16}, {'item': 'BRH-M524-SA', 'desc': "Broche 24'' Antique Silver Mirror", 'available': 16}, {'item': '513-SA', 'desc': "Broche 14'' Antique Silver Chandelier", 'available': 16}, {'item': '535-SA_CEILING', 'desc': "Broche 18'' LED Antique Silver Semi Flush Mount", 'available': 16}, {'item': '569-MT', 'desc': "Broche 42'' Matte White Chandelier", 'available': 15}, {'item': '513-SA_CEILING', 'desc': "Broche 14'' Antique Silver Semi Flush Mount", 'available': 15}, {'item': '508-GA-SA', 'desc': "Broche 31'' Antique Gold + Antique Silver Bathroom Vanity", 'available': 15}, {'item': '569-GA', 'desc': "Broche 42'' Antique Gold Chandelier", 'available': 14}, {'item': '515-SA', 'desc': "Broche 29'' Antique Silver Chandelier", 'available': 13}, {'item': '567-MT', 'desc': "Broche 50.5'' Matte White Linear Chandelier", 'available': 12}, {'item': '536-GA', 'desc': "Broche 24'' Antique Gold Chandelier", 'available': 12}, {'item': '536-GA_CEILING', 'desc': "Broche 24'' Antique Gold Semi Flush Mount", 'available': 12}, {'item': '568-MT', 'desc': "Broche 32'' Matte White Chandelier", 'available': 11}, {'item': '500-SA', 'desc': "Broche 11'' Antique Silver Flush Mount", 'available': 11}, {'item': '511-GA', 'desc': "Broche 8'' Antique Gold Sconce", 'available': 11}, {'item': '561-CT', 'desc': "Broche 8.25'' Champagne Green Tea Sconce", 'available': 11}, {'item': 'BRH-M546-SA', 'desc': "Broche 46.75'' Antique Silver Mirror", 'available': 9}, {'item': '533-CT', 'desc': "Broche 27'' Champagne Green Tea Chandelier", 'available': 9}, {'item': '500W-SA', 'desc': "Broche 11'' Antique Silver Sconce", 'available': 9}, {'item': '564-MT', 'desc': "Broche 18'' Matte White Pendant", 'available': 8}, {'item': '536-MT', 'desc': "Broche 24'' Matte White Chandelier", 'available': 8}, {'item': 'BRH-M546-MT', 'desc': "Broche 46.75'' Matte White Mirror", 'available': 8}, {'item': '536-MT_CEILING', 'desc': "Broche 24'' Matte White Semi Flush Mount", 'available': 8}, {'item': '538-MT', 'desc': "Broche 33.5'' Matte White Chandelier", 'available': 6}, {'item': '538-SA_CEILING', 'desc': "Broche 33.5'' Antique Silver Semi Flush Mount", 'available': 6}, {'item': '538-MT_CEILING', 'desc': "Broche 33.5'' Matte White Semi Flush Mount", 'available': 6}, {'item': 'BRH-M546-GA', 'desc': "Broche 46.75'' Antique Gold Mirror", 'available': 6}, {'item': '569-SA', 'desc': "Broche 42'' Antique Silver Chandelier", 'available': 6}, {'item': '537-MT', 'desc': "Broche 53.5'' Matte White Linear Chandelier", 'available': 5}, {'item': '535-GA', 'desc': "Broche 18'' LED Antique Gold Chandelier", 'available': 5}, {'item': '565-SA_CEILING', 'desc': "Broche 9'' Antique Silver Semi Flush Mount", 'available': 5}, {'item': '538-SA', 'desc': "Broche 33.5'' Antique Silver Chandelier", 'available': 5}, {'item': '519-MT_CEILING', 'desc': "Broche 30'' Matte White Semi Flush Mount", 'available': 5}, {'item': '504-MT', 'desc': "Broche 16'' Matte White Chandelier", 'available': 4}, {'item': '536-SA', 'desc': "Broche 24'' Antique Silver Chandelier", 'available': 3}, {'item': '506-MT', 'desc': "Broche 21'' Matte White Chandelier", 'available': 3}, {'item': '538-GA', 'desc': "Broche 33.5'' Antique Gold Chandelier", 'available': 3}, {'item': '538-GA_CEILING', 'desc': "Broche 33.5'' Antique Gold Semi Flush Mount", 'available': 3}, {'item': '565-GA_CEILING', 'desc': "Broche 9'' Antique Gold Semi Flush Mount", 'available': 3}, {'item': '536-SA_CEILING', 'desc': "Broche 24'' Antique Silver Semi Flush Mount", 'available': 3}, {'item': '565-SA', 'desc': "Broche 9'' Antique Silver Chandelier", 'available': 2}, {'item': '568-SA', 'desc': "Broche 32'' Antique Silver Chandelier", 'available': 2}, {'item': '535-GA_CEILING', 'desc': "Broche 18'' LED Antique Gold Semi Flush Mount", 'available': 2}, {'item': '519-MT', 'desc': "Broche 30'' Matte White Chandelier", 'available': 1}] |
| ADD-317-AG-AU | Addis 51.75'' Aged Brass Linear Chandelier | ADDIS | 207,762.55 | 183 | — | 2026-6-29 | [{'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 14843.0}, {'customer': 'Shades of Light', 'revenue': 11291.1}, {'customer': 'Light Lab Design', 'revenue': 9220.05}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 8826.24}, {'customer': 'Lighting, Inc', 'revenue': 6409.5}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 6112.84}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 4996.0}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 4955.21}, {'customer': 'Georgia Lighting', 'revenue': 4171.5}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 4114.89}, {'customer': 'Union Lighting & Furnishings', 'revenue': 3916.8}, {'customer': 'Reflections L+M', 'revenue': 3747.0}, {'customer': "Graham's Living", 'revenue': 3624.21}, {'customer': 'Lighting Superstore', 'revenue': 3597.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 3507.3}, {'customer': "Hinkley's Lighting Factory", 'revenue': 3484.71}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 3147.48}, {'customer': 'Lando Lighting', 'revenue': 3107.4}, {'customer': 'Urban Lights', 'revenue': 2598.0}, {'customer': "Elaine Everett's Lighting", 'revenue': 2448.0}, {'customer': 'Light Source Lighting', 'revenue': 2448.0}, {'customer': 'Lights Unlimited', 'revenue': 2448.0}, {'customer': 'Build Drop Ship EDI', 'revenue': 2438.84}, {'customer': 'Foundrylighting.com', 'revenue': 2367.57}, {'customer': 'Butler Electric Supply', 'revenue': 2325.6}, {'customer': 'IB Lighting Supply', 'revenue': 2298.0}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 2217.57}, {'customer': 'First Coast Lighting & Fans', 'revenue': 2217.57}, {'customer': 'Universal Lights, Inc.', 'revenue': 2208.3}, {'customer': 'Elements', 'revenue': 1794.03}, {'customer': 'Y Factor Studio, LLC', 'revenue': 1624.0}, {'customer': 'The Lighting Marketplace DBA Fixture Farm', 'revenue': 1494.0}, {'customer': 'The Lighting Shoppe', 'revenue': 1425.15}, {'customer': 'Holland Custom Designs', 'revenue': 1374.0}, {'customer': 'Li Luxe', 'revenue': 1335.0}, {'customer': 'Her Home Design Boutique', 'revenue': 1322.0}, {'customer': 'Farrell Architecture', 'revenue': 1321.0}, {'customer': 'Houston LIght Bulb CO', 'revenue': 1299.0}, {'customer': 'M&M Lighting Co', 'revenue': 1299.0}, {'customer': 'Daniel House Club', 'revenue': 1299.0}, {'customer': 'Lighting By Fox, LLC', 'revenue': 1299.0}, {'customer': 'Hampton Home Dinettes', 'revenue': 1299.0}, {'customer': 'Accent Lighting Galleries', 'revenue': 1299.0}, {'customer': 'Wiseway Supply', 'revenue': 1299.0}, {'customer': 'The Jarrell Company', 'revenue': 1299.0}, {'customer': 'Posh HB LLC DBA Posh Home and Bath', 'revenue': 1299.0}, {'customer': 'Lighting World Decorator', 'revenue': 1299.0}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 1299.0}, {'customer': 'Cates Lighting at Elements', 'revenue': 1299.0}, {'customer': 'Design Lighting Sales, Ltd.', 'revenue': 1299.0}, {'customer': 'Idlewood Electric Supply', 'revenue': 1299.0}, {'customer': 'Front Street Lighting', 'revenue': 1299.0}, {'customer': 'House of Lights Inc', 'revenue': 1208.07}, {'customer': 'Illuminating Expressions', 'revenue': 1208.07}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 1208.07}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 1208.07}, {'customer': 'Gross Lighting & Home', 'revenue': 1208.07}, {'customer': 'The Brecher Company', 'revenue': 1208.07}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 1208.07}, {'customer': 'Lightstyle of Orlando', 'revenue': 1208.07}, {'customer': 'Wilson Lighting of Naples', 'revenue': 1169.1}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 1169.1}, {'customer': 'The Lighting Design Co.', 'revenue': 1149.0}, {'customer': 'Kirby Risk Corporation', 'revenue': 1149.0}, {'customer': 'Anthology Lighting', 'revenue': 1149.0}, {'customer': 'Brand Lighting Corporation', 'revenue': 1149.0}, {'customer': 'Paramont-Evergreen Oak Inc.', 'revenue': 1149.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 1149.0}, {'customer': 'Dominion Electric', 'revenue': 1149.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1149.0}, {'customer': 'LyteWorks', 'revenue': 1149.0}, {'customer': 'Lightopia, LLC.', 'revenue': 1149.0}, {'customer': 'Lighting By Design', 'revenue': 1149.0}, {'customer': 'Fan & Lighting World', 'revenue': 1149.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 1149.0}, {'customer': 'Lighting Solutions', 'revenue': 1099.0}, {'customer': 'White House Furniture Inc.', 'revenue': 1099.0}, {'customer': 'The Light House', 'revenue': 1099.0}, {'customer': 'Northwest Interiors', 'revenue': 1099.0}, {'customer': '43rd Street Lighting, Inc.', 'revenue': 1068.57}, {'customer': 'One Stop Lighting', 'revenue': 1068.57}, {'customer': 'Curb Ease, LLC dba Fixture This', 'revenue': 1068.57}, {'customer': "Graham's Lighting", 'revenue': 1068.57}, {'customer': 'House of Carpets, Inc.', 'revenue': 1068.57}, {'customer': 'Watts Current Inc.', 'revenue': 1068.57}, {'customer': "Mahlander's Appliance Lighting", 'revenue': 1068.57}, {'customer': 'The Light Brothers', 'revenue': 1068.57}, {'customer': 'Krell Lighting & Electric Supp', 'revenue': 1034.1}, {'customer': 'Progressive Lighting', 'revenue': 1034.1}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 1034.1}, {'customer': 'Sun Lighting', 'revenue': 1034.1}, {'customer': 'Premier Lighting', 'revenue': 1022.07}, {'customer': 'LDB Holdings, LLC', 'revenue': 989.1}, {'customer': 'Marx Fireplace and Lighting', 'revenue': 779.4}, {'customer': 'ABC Creations', 'revenue': 689.4}, {'customer': 'Plumb Supply Co', 'revenue': 0.0}, {'customer': 'Lightology, LLC.com', 'revenue': 0.0}, {'customer': 'Shades of Light', 'revenue': 0.0}, {'customer': 'Dolan NW LLC', 'revenue': 0.0}, {'customer': 'Lighting By Design - Dec Den', 'revenue': 0.0}, {'customer': 'Garden of the Gods Lighting', 'revenue': 0.0}, {'customer': 'Hye Lighting', 'revenue': 0.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 0.0}, {'customer': 'Teela Bennett Design', 'revenue': 0.0}, {'customer': 'Elektra Lights and Fans', 'revenue': 0.0}, {'customer': 'Lighting First - Bonita', 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
| ADD-317-AG-AM | Addis 51.75'' Aged Brass Linear Chandelier | ADDIS | 188,094.15 | 162 | — | 2026-8-6 | [{'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 12506.66}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 11995.83}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 9823.16}, {'customer': 'Build Drop Ship EDI', 'revenue': 8961.06}, {'customer': 'Foundrylighting.com', 'revenue': 7333.14}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 5806.53}, {'customer': "Hinkley's Lighting Factory", 'revenue': 5458.74}, {'customer': 'Shades of Light', 'revenue': 5440.5}, {'customer': 'Daniel House Club', 'revenue': 5046.0}, {'customer': 'Lightopia, LLC.', 'revenue': 4890.12}, {'customer': 'Lightology, LLC.com', 'revenue': 4805.07}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 4015.31}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 3897.0}, {'customer': 'Hudson Parc Lighting and Design', 'revenue': 2357.07}, {'customer': 'CES Aquisition LLC', 'revenue': 2298.0}, {'customer': 'Imagine More', 'revenue': 2276.64}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 2203.2}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 1911.89}, {'customer': 'Union Lighting & Furnishings', 'revenue': 1838.4}, {'customer': 'Elements', 'revenue': 1713.6}, {'customer': 'Freestyle Interiors', 'revenue': 1624.0}, {'customer': 'Luxe Living Interiors', 'revenue': 1494.0}, {'customer': 'Roz Murphy Design', 'revenue': 1436.0}, {'customer': 'The Sitting Room', 'revenue': 1436.0}, {'customer': 'Tiffany Skilling Interiors', 'revenue': 1322.0}, {'customer': 'J&L Interiors', 'revenue': 1321.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 1299.0}, {'customer': 'Lifestyles Stores, Inc', 'revenue': 1299.0}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 1299.0}, {'customer': 'Gateway Lighting & Design', 'revenue': 1299.0}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 1299.0}, {'customer': 'Urban Lights', 'revenue': 1299.0}, {'customer': 'Robinson Lighting Centre', 'revenue': 1299.0}, {'customer': 'Hall Electric Co, Inc', 'revenue': 1299.0}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 1299.0}, {'customer': 'Lighting Getz DBA Hello Lighting', 'revenue': 1299.0}, {'customer': 'Norwood Furniture Sales', 'revenue': 1299.0}, {'customer': 'Chroma Home, LLC', 'revenue': 1299.0}, {'customer': 'PAYNES GRAY', 'revenue': 1299.0}, {'customer': 'The Jarrell Company', 'revenue': 1299.0}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 1299.0}, {'customer': 'Lucia Lighting', 'revenue': 1299.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 1299.0}, {'customer': 'Littman Bros Lighting', 'revenue': 1299.0}, {'customer': 'Overstock.com, Inc-Auto EDI', 'revenue': 1299.0}, {'customer': 'Kathy Kuo Home', 'revenue': 1214.56}, {'customer': 'Mountain Lighting & Dsgn Ctr', 'revenue': 1208.07}, {'customer': 'The Saltbox', 'revenue': 1208.07}, {'customer': 'Lights on Design', 'revenue': 1208.07}, {'customer': 'Lightstyle of Orlando', 'revenue': 1208.07}, {'customer': 'First Coast Lighting & Fans', 'revenue': 1208.07}, {'customer': 'Pine Lighting', 'revenue': 1195.08}, {'customer': 'Progressive Lighting', 'revenue': 1169.1}, {'customer': 'Royal Lighting', 'revenue': 1169.1}, {'customer': 'Metro Showroom West County', 'revenue': 1169.1}, {'customer': 'Wilson Fans And Lighting', 'revenue': 1169.1}, {'customer': 'Capitol Lighting-ASN', 'revenue': 1169.1}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1149.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 1149.0}, {'customer': 'JCM Lighting and Design, DBA The Local Lighting Shop', 'revenue': 1149.0}, {'customer': 'Southern Lights', 'revenue': 1149.0}, {'customer': 'Gerrie Electric', 'revenue': 1149.0}, {'customer': "Wilkinson's House of Lights", 'revenue': 1149.0}, {'customer': 'Dominion Electric', 'revenue': 1149.0}, {'customer': 'Coast Lighting', 'revenue': 1149.0}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 1149.0}, {'customer': 'Lighting By Fox, LLC', 'revenue': 1149.0}, {'customer': 'North Valley Fans and Blinds', 'revenue': 1149.0}, {'customer': 'ARC DEST/ FOUNDRY NY', 'revenue': 1149.0}, {'customer': 'Ellen Lighting & Hardware', 'revenue': 1149.0}, {'customer': 'Furniture Land South', 'revenue': 1149.0}, {'customer': 'Rite Rug Co', 'revenue': 1149.0}, {'customer': 'Northeast Electrical formerly Rockingham Electrical Supply', 'revenue': 1149.0}, {'customer': 'William Hart Designs, LLC', 'revenue': 1149.0}, {'customer': 'R. Bdelaa Lighting', 'revenue': 1149.0}, {'customer': 'Newton Electrical Company', 'revenue': 1099.0}, {'customer': 'Lighting By Design - Exton PA', 'revenue': 1099.0}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 1068.57}, {'customer': 'Wyckoff Lighting', 'revenue': 1068.57}, {'customer': 'Posh Lighting', 'revenue': 1068.57}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 1068.57}, {'customer': 'Reflections L+M', 'revenue': 1034.1}, {'customer': 'Prima Lighting', 'revenue': 1034.1}, {'customer': 'Lamps.com', 'revenue': 1023.17}, {'customer': 'Kaleidoscope', 'revenue': 1022.07}, {'customer': "Graham's Living", 'revenue': 1022.07}, {'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 919.2}, {'customer': 'Courtesy Lighting', 'revenue': 824.25}, {'customer': 'M&M Lighting Co', 'revenue': 649.5}, {'customer': 'Moreau Enterprises/Aggieland', 'revenue': 649.5}, {'customer': 'Hye Lighting', 'revenue': 574.5}, {'customer': 'Nova Lighting', 'revenue': 0.0}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 0.0}, {'customer': 'Shades of Light', 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
| ARC-1919-GA-CL-MWP | Arcadia 46.25'' Antique Gold Chandelier | COL70 | 180,660.39 | 110 | — | 2026-7-27 | [{'customer': 'Progressive Lighting', 'revenue': 18694.8}, {'customer': 'Build Drop Ship EDI', 'revenue': 13864.72}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 13063.83}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 11829.35}, {'customer': 'Connecticut Lighting Center', 'revenue': 11322.9}, {'customer': 'Georgia Lighting', 'revenue': 9626.97}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 7104.64}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 6050.52}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 5249.07}, {'customer': 'TRI-Supply LLC', 'revenue': 5193.0}, {'customer': 'Elements', 'revenue': 4746.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 3444.0}, {'customer': 'Notoco-Baton Rouge', 'revenue': 3390.0}, {'customer': 'The Brecher Company', 'revenue': 3325.35}, {'customer': 'House of Carpets, Inc.', 'revenue': 3274.5}, {'customer': 'The Parker Company', 'revenue': 2187.0}, {'customer': 'FS DESIGN  GROUP', 'revenue': 2012.0}, {'customer': 'J&L Interiors', 'revenue': 2012.0}, {'customer': 'Foundrylighting.com', 'revenue': 1999.0}, {'customer': 'M&M Lighting Co', 'revenue': 1999.0}, {'customer': 'Retail Convergence.com, LP ASN (Rue La La)', 'revenue': 1999.0}, {'customer': 'One Stop Lighting', 'revenue': 1999.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 1999.0}, {'customer': 'O&I Design Group, LLC DBA The Elements', 'revenue': 1949.0}, {'customer': 'Lighting, Inc', 'revenue': 1799.1}, {'customer': 'Lighting Superstore', 'revenue': 1749.0}, {'customer': 'PC Building Materials', 'revenue': 1749.0}, {'customer': 'Universal Lights, Inc.', 'revenue': 1749.0}, {'customer': 'Elan Studio Lighting', 'revenue': 1749.0}, {'customer': 'Broad Street Interiors', 'revenue': 1749.0}, {'customer': 'Home Depot-ASN', 'revenue': 1695.0}, {'customer': 'Posh Places', 'revenue': 1695.0}, {'customer': 'Net Retailers dba Luxe Decor', 'revenue': 1695.0}, {'customer': 'Coastal Lighting Supply', 'revenue': 1695.0}, {'customer': 'Armstrong Supply Co.', 'revenue': 1695.0}, {'customer': 'Royce Collection Inc.', 'revenue': 1695.0}, {'customer': 'Farreys Wholesale', 'revenue': 1695.0}, {'customer': 'Magnolia Lighting & Electric', 'revenue': 1695.0}, {'customer': 'Lighting Efx', 'revenue': 1626.57}, {'customer': 'Lightology, LLC.com', 'revenue': 1626.57}, {'customer': "Graham's Living", 'revenue': 1576.35}, {'customer': 'Quinn Wholesale dba Lamp Outlet', 'revenue': 1576.35}, {'customer': 'Rittenhouse Electric Supply Co', 'revenue': 1576.35}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 1576.35}, {'customer': 'We Got Lites, Inc.', 'revenue': 1576.35}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 1576.35}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 1574.1}, {'customer': 'The Lighting Warehouse', 'revenue': 1525.5}, {'customer': 'Lighting & Lamps', 'revenue': 1224.3}, {'customer': 'Wage Lighting & Design', 'revenue': 1186.5}, {'customer': 'Plumbing Overstock, LLC', 'revenue': 0.0}] | [{'item': 'ARC-1900-SA-CL-MWP', 'desc': "Arcadia 15'' Antique Silver Semi Flush Mount", 'available': 42}, {'item': 'ARC-1900-GA-CL-MWP', 'desc': "Arcadia 15'' Antique Gold Semi Flush Mount", 'available': 24}, {'item': 'ARC-1909-SA-CL-MWP', 'desc': "Arcadia 32.5'' Antique Silver Chandelier", 'available': 21}, {'item': 'ARC-1917-SA-CL-MWP', 'desc': "Arcadia 24'' Antique Silver Chandelier", 'available': 19}, {'item': 'ARC-1908-SA-CL-MWP', 'desc': "Arcadia 26.75'' Antique Silver Chandelier", 'available': 17}, {'item': 'ARC-1902-GA-CL-MWP', 'desc': "Arcadia 11.25'' Antique Gold Sconce", 'available': 17}, {'item': 'ARC-1905-SA-CL-MWP', 'desc': "Arcadia 23.5'' Antique Silver Chandelier", 'available': 17}, {'item': 'ARC-1917-GA-CL-MWP', 'desc': "Arcadia 24'' Antique Gold Chandelier", 'available': 16}, {'item': 'ARC-1902-SA-CL-MWP', 'desc': "Arcadia 11.25'' Antique Silver Sconce", 'available': 15}, {'item': 'ARC-1905-GA-CL-MWP', 'desc': "Arcadia 23.5'' Antique Gold Chandelier", 'available': 12}, {'item': 'ARC-1907-SA-CL-MWP', 'desc': "Arcadia 18'' Antique Silver Chandelier", 'available': 12}, {'item': 'ARC-1929-GA-CL-MWP', 'desc': "Arcadia 61'' Antique Gold Chandelier", 'available': 11}, {'item': 'ARC-1908-GA-CL-MWP', 'desc': "Arcadia 26.75'' Antique Gold Chandelier", 'available': 9}, {'item': 'ARC-1929-SA-CL-MWP', 'desc': "Arcadia 61'' Antique Silver Chandelier", 'available': 7}, {'item': 'ARC-1919-SA-CL-MWP', 'desc': "Arcadia 46.25'' Antique Silver Chandelier", 'available': 5}] |
| HAY-1409-PN | Hayes 40.5'' Polished Nickel Chandelier | HAYES | 177,252.20 | 87 | — | 2026-7-14 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 16207.38}, {'customer': 'Build Drop Ship EDI', 'revenue': 15702.51}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 15493.0}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 7404.17}, {'customer': 'Anthology Lighting', 'revenue': 6247.0}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 6166.47}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 5932.16}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 5775.06}, {'customer': 'Lighting, Inc', 'revenue': 5397.3}, {'customer': 'Midwest Lighting Solutions', 'revenue': 4598.0}, {'customer': 'Cleveland Lighting', 'revenue': 4135.55}, {'customer': 'Lighting First - Bonita', 'revenue': 4090.57}, {'customer': 'Fan & Lighting World', 'revenue': 3998.0}, {'customer': 'Robinson Lighting Centre', 'revenue': 3998.0}, {'customer': 'Wilson Lighting of Naples', 'revenue': 3598.2}, {'customer': 'Elements', 'revenue': 3370.4}, {'customer': 'Beckland Creations LLC', 'revenue': 2889.32}, {'customer': 'LF Design', 'revenue': 2499.0}, {'customer': 'Earth and Images', 'revenue': 2499.0}, {'customer': 'Denali Lighting', 'revenue': 2299.0}, {'customer': 'CAI Designs', 'revenue': 2299.0}, {'customer': 'Franklin Lighting', 'revenue': 2299.0}, {'customer': 'Gallery of Lighting', 'revenue': 2299.0}, {'customer': 'Lucia Lighting', 'revenue': 2299.0}, {'customer': 'Acker Bryant Design', 'revenue': 2299.0}, {'customer': 'The Lighting Shoppe', 'revenue': 2249.0}, {'customer': 'Tazz Lighting, Inc.', 'revenue': 2249.0}, {'customer': 'Endacott Lighting', 'revenue': 2249.0}, {'customer': 'Hobrecht Lighting Co., Inc.', 'revenue': 2249.0}, {'customer': 'Universal Lamps', 'revenue': 2249.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 2249.0}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 2133.86}, {'customer': 'Lightology, LLC.com', 'revenue': 2091.57}, {'customer': 'Littman Bros Lighting', 'revenue': 2091.57}, {'customer': 'Fort Worth Lighting', 'revenue': 2091.57}, {'customer': 'W.T. Lighting', 'revenue': 2069.1}, {'customer': 'The Lighting Warehouse', 'revenue': 2024.1}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 1999.0}, {'customer': 'Beautiful Things', 'revenue': 1999.0}, {'customer': 'ARC DEST/ FOUNDRY NY', 'revenue': 1999.0}, {'customer': 'Village Lighting & Supply, Inc', 'revenue': 1859.07}, {'customer': "Hinkley's Lighting Factory", 'revenue': 1859.07}, {'customer': 'Shades of Light', 'revenue': 1799.1}, {'customer': 'Progressive Lighting', 'revenue': 1799.1}, {'customer': 'Metro Showroom West County', 'revenue': 1799.1}, {'customer': 'Lando Lighting', 'revenue': 1199.4}, {'customer': 'Naples Lamp Shop', 'revenue': 1149.5}, {'customer': 'Lowes Companies , Inc', 'revenue': 0.0}] | [{'item': 'HAY-1402-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 102}, {'item': 'HAY-1401-AG', 'desc': "Hayes 8'' Aged Brass Chandelier", 'available': 75}, {'item': 'HAY-1402-AG', 'desc': "Hayes 7.5'' Aged Brass Sconce", 'available': 61}, {'item': 'HAY-1411-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 39}, {'item': 'HAY-1401-PN', 'desc': "Hayes 8'' Polished Nickel Chandelier", 'available': 33}, {'item': 'HAY-1400-AG', 'desc': "Hayes 16'' Aged Brass Flush Mount", 'available': 30}, {'item': 'HAY-1409-AG', 'desc': "Hayes 40.5'' Aged Brass Chandelier", 'available': 29}, {'item': 'HAY-1407-PN', 'desc': "Hayes 28'' Polished Nickel Chandelier", 'available': 28}, {'item': 'HAY-1407-AG', 'desc': "Hayes 28'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1405-AG', 'desc': "Hayes 22'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1403-AG', 'desc': "Hayes 18'' Aged Brass Flush Mount", 'available': 24}, {'item': 'HAY-1403-PN', 'desc': "Hayes 18'' Polished Nickel Flush Mount", 'available': 17}, {'item': 'HAY-1413-PN', 'desc': "Hayes 23.5'' Polished Nickel Bathroom Vanity", 'available': 12}, {'item': 'HAY-1405-PN', 'desc': "Hayes 22'' Polished Nickel Chandelier", 'available': 12}, {'item': 'HAY-1400-PN', 'desc': "Hayes 16'' Polished Nickel Flush Mount", 'available': 10}, {'item': 'HAY-1415-PN', 'desc': "Hayes 31.5'' Polished Nickel Bathroom Vanity", 'available': 9}, {'item': 'HAY-1417-PN', 'desc': "Hayes 50'' Polished Nickel Linear Chandelier", 'available': 8}, {'item': 'HAY-1415-AG', 'desc': "Hayes 31.5'' Aged Brass Bathroom Vanity", 'available': 8}, {'item': 'HAY-1413-AG', 'desc': "Hayes 23.5'' Aged Brass Bathroom Vanity", 'available': 6}, {'item': 'HAY-1419-AG', 'desc': "Hayes 24'' Aged Brass Chandelier", 'available': 1}] |
| ADD-308-AG-WH | Addis 22'' Aged Brass Chandelier | ADDIS | 136,284.81 | 234 | — | 2026-6-29 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 11495.62}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 8489.15}, {'customer': 'Build Drop Ship EDI', 'revenue': 7613.91}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 6932.23}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 6072.26}, {'customer': 'Lightstyle of Orlando', 'revenue': 4642.56}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 3966.07}, {'customer': 'Haus Appeal LLC', 'revenue': 3554.38}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 3144.96}, {'customer': 'Dominion Electric', 'revenue': 2969.87}, {'customer': 'Idlewood Electric Supply', 'revenue': 2450.57}, {'customer': 'LDB Holdings, LLC', 'revenue': 2396.0}, {'customer': 'Lightopia, LLC.', 'revenue': 2310.87}, {'customer': 'Melrose & Madison (AMZ)', 'revenue': 2161.99}, {'customer': 'Newton Electrical Company', 'revenue': 2097.0}, {'customer': 'B.A. Robinson Co. Ltd.', 'revenue': 1947.0}, {'customer': 'IBS Lighting', 'revenue': 1897.0}, {'customer': 'Lightology, LLC.com', 'revenue': 1847.0}, {'customer': 'PC Building Materials', 'revenue': 1847.0}, {'customer': "Horton's Home Lighting", 'revenue': 1802.15}, {'customer': 'The Lighting Design Co.', 'revenue': 1801.57}, {'customer': 'BBC Lighting Company', 'revenue': 1797.0}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 1662.3}, {'customer': 'Union Lighting & Home', 'revenue': 1326.87}, {'customer': 'Xpress Lighting of Texas', 'revenue': 1298.0}, {'customer': 'Cleveland Lighting', 'revenue': 1265.55}, {'customer': 'Texas Bright Ideas', 'revenue': 1252.57}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 1248.0}, {'customer': 'Cates Lighting at Elements', 'revenue': 1248.0}, {'customer': 'Pine Tree Lighting', 'revenue': 1248.0}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 1248.0}, {'customer': 'Montreal Luminaire', 'revenue': 1225.74}, {'customer': 'Christies Lighting Gallery,LLC', 'revenue': 1207.14}, {'customer': 'Jackson Lighting', 'revenue': 1207.14}, {'customer': 'Valencia Lighting & Design', 'revenue': 1202.57}, {'customer': 'Lights of Oconee', 'revenue': 1202.57}, {'customer': 'Dement Lighting', 'revenue': 1198.0}, {'customer': "Efird's Interiors, Inc.", 'revenue': 1123.2}, {'customer': 'Connecticut Lighting Center', 'revenue': 1123.2}, {'customer': 'Stokes Lighting Center', 'revenue': 1018.3}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 948.5}, {'customer': 'Elements', 'revenue': 873.6}, {'customer': 'Great Neighborhood Homes', 'revenue': 749.0}, {'customer': 'Jill Heaton Interiors', 'revenue': 747.0}, {'customer': 'J. Adams Interiors', 'revenue': 747.0}, {'customer': 'Loudoun Interiors LLC', 'revenue': 747.0}, {'customer': 'Winsupply Owensboro KY Co', 'revenue': 649.0}, {'customer': 'Ocean Pacific Lighting', 'revenue': 649.0}, {'customer': 'White Star Supply LLC', 'revenue': 649.0}, {'customer': 'Hubbard Kitchen & BathShowroom', 'revenue': 649.0}, {'customer': 'Hydrologic Distribution Co.', 'revenue': 649.0}, {'customer': 'Light Bulbs, Etc. (Orange)', 'revenue': 649.0}, {'customer': 'Wiseway Supply', 'revenue': 649.0}, {'customer': 'Uncommon Living Inc.', 'revenue': 649.0}, {'customer': 'Lighting Etc.', 'revenue': 649.0}, {'customer': 'Modern Lighting', 'revenue': 649.0}, {'customer': 'Paradise Lighting', 'revenue': 649.0}, {'customer': 'Kathy Kuo Home', 'revenue': 606.81}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 603.57}, {'customer': 'Littman Bros Lighting', 'revenue': 603.57}, {'customer': 'JCM Lighting and Design, DBA The Local Lighting Shop', 'revenue': 603.57}, {'customer': 'Lowes Companies , Inc', 'revenue': 599.0}, {'customer': 'Hajoca Corporation', 'revenue': 599.0}, {'customer': 'Elan Studio Lighting', 'revenue': 599.0}, {'customer': 'Hobrecht Lighting Co., Inc.', 'revenue': 599.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 599.0}, {'customer': 'Design Trade Service', 'revenue': 599.0}, {'customer': 'Frank Souder Designs', 'revenue': 599.0}, {'customer': 'River Cities Lighting', 'revenue': 599.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 599.0}, {'customer': 'M&M Lighting Co', 'revenue': 599.0}, {'customer': 'William Hart Designs, LLC', 'revenue': 599.0}, {'customer': 'Coley Electric & Plumbing Sup', 'revenue': 599.0}, {'customer': 'Legacy Lighting', 'revenue': 599.0}, {'customer': 'Decorum', 'revenue': 599.0}, {'customer': 'Net Retailers dba Luxe Decor', 'revenue': 599.0}, {'customer': 'Kendall Electric', 'revenue': 599.0}, {'customer': 'The Brecher Company', 'revenue': 599.0}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 599.0}, {'customer': 'Lee Supply Corporate', 'revenue': 599.0}, {'customer': 'Metro Showroom West County', 'revenue': 584.1}, {'customer': 'Progressive Lighting', 'revenue': 584.1}, {'customer': 'Rensen House Lights', 'revenue': 557.07}, {'customer': 'CAI Designs', 'revenue': 557.07}, {'customer': 'Litemode Limited', 'revenue': 557.07}, {'customer': 'Foundrylighting.com', 'revenue': 557.07}, {'customer': 'Dolan NW LLC', 'revenue': 539.1}, {'customer': 'Prima Lighting', 'revenue': 539.1}, {'customer': 'Union Lighting & Furnishings', 'revenue': 519.2}, {'customer': 'Gerrie Electric', 'revenue': 0.0}, {'customer': 'KLS dba Spectrum Lighting', 'revenue': 0.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 0.0}, {'customer': 'The Lighting Warehouse', 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 5534-EB-CL-S | Welton 11'' Swarovski Strass Crystal English Bronze Chandelier | COL149 | 2 | 1,641 | [{'customer_code': '25207', 'customer_name': 'Melrose & Madison (AMZ)', 'collection_revenue': 59289.27}, {'customer_code': '463', 'customer_name': 'Lamps Plus.com-Auto ASN', 'collection_revenue': 15921.63}] |
| 5534-WW-CL-S | Welton 11'' Swarovski Strass Crystal Wet White Chandelier | COL149 | 2 | 1,094 | [{'customer_code': '25207', 'customer_name': 'Melrose & Madison (AMZ)', 'collection_revenue': 59289.27}, {'customer_code': '463', 'customer_name': 'Lamps Plus.com-Auto ASN', 'collection_revenue': 15921.63}] |
| 6050-PN | Brian Patrick Flynn Hurley 11.75'' Polished Nickel Flush Mount | COL80 | 2 | 323.92 | — |
| 6623-CH-CL-S | Othello 14'' Swarovski Strass Crystal Polished Chrome Chandelier | COL96 | 2 | 2,198 | [{'customer_code': '463', 'customer_name': 'Lamps Plus.com-Auto ASN', 'collection_revenue': 58984.88}, {'customer_code': '7044', 'customer_name': 'Wayfair.com-Auto EDI', 'collection_revenue': 22897.09}, {'customer_code': '4723', 'customer_name': 'Belami.com (1 Stop) - ASN', 'collection_revenue': 19813.62}, {'customer_code': '7342', 'customer_name': 'Build Drop Ship EDI', 'collection_revenue': 18370.19}] |
| 6625-CH-CL-S | Othello 24'' Swarovski Strass Crystal Polished Chrome Chandelier | COL96 | 0 | 0 | [{'customer_code': '463', 'customer_name': 'Lamps Plus.com-Auto ASN', 'collection_revenue': 58984.88}, {'customer_code': '7044', 'customer_name': 'Wayfair.com-Auto EDI', 'collection_revenue': 22897.09}, {'customer_code': '4723', 'customer_name': 'Belami.com (1 Stop) - ASN', 'collection_revenue': 19813.62}, {'customer_code': '7342', 'customer_name': 'Build Drop Ship EDI', 'collection_revenue': 18370.19}, {'customer_code': '7127', 'customer_name': 'Lighting New York-Auto EDI', 'collection_revenue': 14475.73}] |
| 6822-CH-CL-S | Othello 14'' Swarovski Strass Crystal Polished Chrome Sconce | COL96 | 0 | 0 | [{'customer_code': '463', 'customer_name': 'Lamps Plus.com-Auto ASN', 'collection_revenue': 58984.88}, {'customer_code': '7044', 'customer_name': 'Wayfair.com-Auto EDI', 'collection_revenue': 22897.09}, {'customer_code': '4723', 'customer_name': 'Belami.com (1 Stop) - ASN', 'collection_revenue': 19813.62}, {'customer_code': '7342', 'customer_name': 'Build Drop Ship EDI', 'collection_revenue': 18370.19}, {'customer_code': '7127', 'customer_name': 'Lighting New York-Auto EDI', 'collection_revenue': 14475.73}] |
