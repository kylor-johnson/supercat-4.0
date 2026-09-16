# Section 3 Context Bundle — Craftmade (clli)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=168198, portal_order_gmv=$47.7M |
| HAS_INVENTORY | True | inventory_count=2867 |
| HAS_SALES_DATA | True | sales_data_count=508787 |
| HAS_SALES_SECTION | True | qualifying_reps=9 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | clli_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$47.7M > ecat_gmv=$881,333: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 9 | 9 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 228, Mixpanel total submit_order (Q-01): 371 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=83.5%, ambiguous_rate=15.8%, showroom_event_share=7.3% |
| USER_GROUP_JOIN_RATE | 84% | 76 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7% | showroom+admin share of matched events: 7.3% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: David Raushchuber, Kevin Ailara, Andrew  Rivera, Shayna Petty |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1722 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=289 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Craftmade
- **Shortname**: clli
- **Org ID**: 149
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Craftmade (clli, org_id=149)
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

# Signal Rank — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Total signals fired**: 51 (P0: 36, P1: 13, P2: 2)
- **Org GMV**: $0.9M eCat LTM, $47.7M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders | P1 | §2 Accounts | 8.3 | $8,279,294 | 2.0 | 137,093,418 | POSITIVE |
| 2 | SIG-MOM-01 | Account Acceleration —  3 consecutive QoQ acceleration quarters, $622,312 peak quarter (+180% QoQ) | P0 | §2 Accounts | 6.0 | $622,312 | 3.0 | 11,195,390 | POSITIVE |
| 3 | SIG-DECAY-04 | Spending Contraction —  -89.7% YoY ($899,202→$92,187), $807,015 gap | P0 | §2 Accounts | 4.5 | $807,015 | 3.0 | 10,858,392 | RISK |
| 4 | SIG-DECAY-04 | Spending Contraction —  -59.2% YoY ($1,788,691→$729,998), $1,058,693 gap | P0 | §2 Accounts | 3.0 | $1,058,693 | 3.0 | 9,401,193 | RISK |
| 5 | SIG-DECAY-04 | Spending Contraction —  -78.3% YoY ($957,251→$208,171), $749,080 gap | P0 | §2 Accounts | 3.9 | $749,080 | 3.0 | 8,797,942 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available | P0 | §3 Product | 10.0 | $281,687 | 3.0 | 8,450,620 | RISK |
| 7 | SIG-DECAY-04 | Spending Contraction —  -61.5% YoY ($1,414,384→$545,054), $869,331 gap | P0 | §2 Accounts | 3.1 | $869,331 | 3.0 | 8,019,576 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available | P0 | §3 Product | 10.0 | $266,996 | 3.0 | 8,009,889 | RISK |
| 9 | SIG-COMMERCE-01 | Capture Rate — eCat captures 1.8% of $48M total business; each +1pt = $477K | P0 | §4 Commerce | 4.9 | $477,000 | 3.0 | 7,022,800 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $104,278 peak quarter (+594% QoQ) | P0 | §2 Accounts | 19.8 | $104,278 | 3.0 | 6,188,876 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available | P0 | §3 Product | 10.0 | $193,427 | 3.0 | 5,802,810 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 19624BNK3 (Drake 3 Light Vanity in Brushed Polished) $174,443 LTM, 0 available | P0 | §3 Product | 10.0 | $174,443 | 3.0 | 5,233,279 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — BSCB-B (Surface Mount Die-Cast Builder's Series ) $162,869 LTM, 0 available | P0 | §3 Product | 10.0 | $162,869 | 3.0 | 4,886,060 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — Z402-TB (2 Light Directional Bullet in Textured B) $146,102 LTM, 0 available | P0 | §3 Product | 10.0 | $146,102 | 3.0 | 4,383,061 | RISK |
| 15 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $83,118 peak quarter (+490% QoQ) | P0 | §2 Accounts | 16.3 | $83,118 | 3.0 | 4,073,595 | POSITIVE |
| 16 | SIG-ANOMALY-02 | Stock Out — PH-2BZ (2 Light PAR Holder in Bronze) $132,167 LTM, 0 available | P0 | §3 Product | 10.0 | $132,167 | 3.0 | 3,964,999 | RISK |
| 17 | SIG-DECAY-04 | Spending Contraction —  -33.2% YoY ($1,528,897→$1,021,173), $507,724 gap | P0 | §2 Accounts | 1.7 | $507,724 | 3.0 | 2,528,463 | RISK |
| 18 | SIG-DECAY-04 | Spending Contraction —  -59.4% YoY ($403,858→$164,014), $239,843 gap | P0 | §2 Accounts | 3.0 | $239,843 | 3.0 | 2,137,005 | RISK |
| 19 | SIG-DECAY-04 | Spending Contraction —  -55.6% YoY ($422,120→$187,615), $234,505 gap | P0 | §2 Accounts | 2.8 | $234,505 | 3.0 | 1,955,775 | RISK |
| 20 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $87,277 peak quarter (+164% QoQ) | P0 | §2 Accounts | 5.5 | $87,277 | 3.0 | 1,428,729 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 28 | 1 | 0 | 29 | |
| §3 Product Intelligence | 7 | 0 | 1 | 8 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 1 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration —  3 consecutive QoQ acceleration quarters, $622,312 peak quarter (+180% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 1.8% of $48M total business; each +1pt = $477K
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-07_results.md

# Q-07 Results — Craftmade (clli, org_id=149)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 2,969 | 190 | 0 | 93.60 |

### Q-37_results.md

# Q-37 Results — Craftmade (clli, org_id=149)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C102L | — | — | — | $1.2M | 122,956 | 0 | 0 | 0 | — |
| DCF52BNK5C1 | — | — | — | $1.2M | 23,078 | 0 | 0 | 0 | — |
| DCF52BNK5C3 | — | — | — | $832,395 | 16,396 | 0 | 0 | 0 | — |
| CON48BNK4C1-48BN | — | — | — | $584,108 | 10,359 | 0 | 0 | 0 | — |
| C201BN | — | — | — | $466,770 | 9,082 | 0 | 0 | 0 | — |
| CON48BNK4C1 | — | — | — | $466,593 | 8,082 | 0 | 0 | 0 | — |
| C52-KIT | — | — | — | $437,374 | 10,274 | 0 | 0 | 0 | — |
| K11311 | — | — | — | $421,821 | 1,839 | 0 | 0 | 0 | — |
| K11072 | — | — | — | $349,917 | 6,298 | 0 | 0 | 0 | — |
| TG52BNK3-WM6W | — | — | — | $338,100 | 3,689 | 0 | 0 | 0 | — |
| TEA52CH4-18W | — | — | — | $289,835 | 3,370 | 0 | 0 | 0 | — |
| BW414AG3 | CAT1 | COL53 | Bellows IV 14" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Aged Bronze Textured w/ Aged Bronze Blades; Not Light Kit Adaptable | $281,687 | 1,534 | 0 | 0 | 10 | 2026-07-20 |
| DCF52FBZ5C1 | — | — | — | $280,208 | 5,614 | 0 | 0 | 0 | — |
| DCF52FBZ5C3 | — | — | — | $274,563 | 5,632 | 0 | 0 | 0 | — |
| BW321AG3 | CAT1 | COL52 | Bellows III 18" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Aged Bronze Textured w/ Aged Bronze Blades; Not Light Kit Adaptable | $266,996 | 1,125 | 0 | 0 | 12 | 2026-07-20 |
| TFV70REC | — | — | — | $236,895 | 5,149 | 0 | 0 | 0 | — |
| ANI36BNK3 | — | — | — | $217,174 | 792 | 0 | 0 | 0 | — |
| UCI-2000 | — | — | — | $212,750 | 6,804 | 0 | 0 | 0 | — |
| K11291 | — | — | — | $200,937 | 1,256 | 0 | 0 | 0 | — |
| K11289 | — | — | — | $198,083 | 1,261 | 0 | 0 | 0 | — |

### Q-38a_results.md

# Q-38a Results — Craftmade (clli, org_id=149)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
|  | — | — | — | 2025-12-1 | 27,238 | 4,097 |
|  | — | — | — | 2026-1-1 | 82,664 | 12,302 |
|  | — | — | — | 2026-2-1 | 83,475 | 12,565 |
|  | — | — | — | 2026-3-1 | 90,685 | 14,382 |
|  | — | — | — | 2026-4-1 | 95,778 | 13,952 |
|  | — | — | — | 2026-5-1 | 97,315 | 13,883 |
|  | — | — | — | 2026-6-1 | 60,590 | 8,159 |

### Q-39_category_results.md

# Q-39-cat Results — Craftmade (clli, org_id=149)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 54
- **Run date**: 2026-06-17


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT24 | $11.3M | 111,383 | 110 | $102,921 |
| CAT9 | $6.0M | 119,223 | 150 | $39,735 |
| CAT1 | $2.8M | 15,864 | 22 | $128,639 |
| CAT26 | $2.8M | 65,999 | 97 | $28,550 |
| CAT13 | $2.1M | 15,054 | 109 | $19,650 |
| FOYER | $1.2M | 10,460 | 34 | $33,917 |
| CAT20 | $1.1M | 31,182 | 51 | $21,278 |
| CAT51 | $987,093 | 116,135 | 144 | $6,855 |
| CAT8 | $616,205 | 19,885 | 77 | $8,003 |
| CAT45 | $411,978 | 68,533 | 26 | $15,845 |
| CAT14 | $398,707 | 3,448 | 36 | $11,075 |
| CAT50 | $381,617 | 11,229 | 26 | $14,678 |
| CAT16 | $353,729 | 2,268 | 19 | $18,617 |
| CAT56 | $343,027 | 42,628 | 4 | $85,757 |
| CAT35 | $326,525 | 6,819 | 11 | $29,684 |
| CHIME | $325,865 | 13,905 | 10 | $32,586 |
| CAT18 | $319,108 | 5,241 | 14 | $22,793 |
| CAT5 | $318,381 | 6,797 | 20 | $15,919 |
| CAT17 | $281,775 | 4,664 | 17 | $16,575 |
| CAT10 | $257,126 | 5,450 | 20 | $12,856 |
| CAT48 | $255,873 | 10,620 | 14 | $18,277 |
| CAT42 | $231,198 | 23,844 | 11 | $21,018 |
| CAT37 | $185,073 | 9,260 | 2 | $92,536 |
| CAT62 | $171,032 | 116,957 | 3 | $57,011 |
| CAT29 | $164,824 | 12,132 | 16 | $10,302 |
| CAT49 | $154,928 | 13,264 | 3 | $51,643 |
| CAT30 | $154,226 | 3,891 | 35 | $4,406 |
| CAT28 | $143,147 | 2,590 | 23 | $6,224 |
| CAT21 | $134,927 | 632 | 5 | $26,985 |
| CAT52 | $117,227 | 33,089 | 5 | $23,445 |
| CAT34 | $68,110 | 1,366 | 8 | $8,514 |
| FLOOD | $68,012 | 1,710 | 2 | $34,006 |
| CAT32 | $58,850 | 185 | 2 | $29,425 |
| CAT44 | $57,718 | 560 | 1 | $57,718 |
| CAT22 | $54,228 | 2,018 | 17 | $3,190 |
| BULB | $49,036 | 15,243 | 7 | $7,005 |
| CAT53 | $43,698 | 1,447 | 4 | $10,925 |
| CAT66 | $35,362 | 663 | 1 | $35,362 |
| CAT40 | $31,858 | 2,614 | 6 | $5,310 |
| CAT65 | $28,158 | 303 | 1 | $28,158 |
| CAT39 | $27,649 | 3,440 | 2 | $13,824 |
| CAT31 | $24,334 | 246 | 1 | $24,334 |
| CAT55 | $23,123 | 2,414 | 18 | $1,285 |
| CAT61 | $20,108 | 1,136 | 1 | $20,108 |
| CAT2 | $18,755 | 543 | 3 | $6,252 |
| CAT64 | $18,148 | 1,220 | 2 | $9,074 |
| CAT38 | $16,271 | 2,218 | 1 | $16,271 |
| CAT27 | $14,792 | 286 | 1 | $14,792 |
| CAT23 | $13,945 | 239 | 1 | $13,945 |
| CAT60 | $8,207 | 8,440 | 1 | $8,207 |
| CAT58 | $3,109 | 1,654 | 5 | $622 |
| CAT57 | $2,698 | 426 | 10 | $270 |
| CAT7 | $748 | 255 | 5 | $150 |
| CAT11 | $13 | 1 | 1 | $13 |

### Q-39_collection_results.md

# Q-39-col Results — Craftmade (clli, org_id=149)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| COL234 | $2.9M | 60,566 | 48 | $61,336 |
| COL85 | $1.7M | 17,747 | 3 | $570,761 |
| TEANA | $1.4M | 13,647 | 5 | $282,627 |
| GRACE | $1.4M | 29,543 | 41 | $34,195 |
| COL159 | $1.1M | 10,742 | 5 | $216,063 |
| COL337 | $1.1M | 139,033 | 145 | $7,362 |
| COL89 | $896,322 | 3,721 | 3 | $298,774 |
| COL174 | $865,238 | 3,257 | 6 | $144,206 |
| DRAKE | $687,667 | 13,988 | 10 | $68,767 |
| FLYNT | $642,202 | 6,391 | 4 | $160,551 |
| ESSEX | $483,833 | 7,877 | 15 | $32,256 |
| COL114 | $474,952 | 6,189 | 4 | $118,738 |
| COL233 | $466,557 | 10,608 | 30 | $15,552 |
| COL162 | $457,606 | 2,979 | 3 | $152,535 |
| COL314 | $448,675 | 8,342 | 18 | $24,926 |
| ARIA | $446,771 | 7,783 | 5 | $89,354 |
| COL81 | $429,532 | 6,395 | 3 | $143,177 |
| COL53 | $417,818 | 2,321 | 2 | $208,909 |
| TYLER | $416,281 | 9,608 | 14 | $29,734 |
| COL230 | $386,706 | 8,729 | 25 | $15,468 |
| COL163 | $375,052 | 2,254 | 2 | $187,526 |
| COL38 | $364,358 | 1,267 | 1 | $364,358 |
| COL75 | $359,063 | 1,787 | 2 | $179,531 |
| COL88 | $359,029 | 1,941 | 2 | $179,515 |
| COL244 | $354,182 | 6,303 | 15 | $23,612 |

### Q-42_results.md

# Q-42 Results — Craftmade (clli, org_id=149)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 83
- **Run date**: 2026-06-17


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| ASTOR | 8 | $0 | 0 | $0 |
| BANKS | 4 | $0 | 0 | $0 |
| BLAKE | 4 | $0 | 0 | $0 |
| CAST | 1 | $0 | 0 | $0 |
| COL10 | 1 | $0 | 0 | $0 |
| COL100 | 20 | $0 | 0 | $0 |
| COL101 | 2 | $0 | 0 | $0 |
| COL109 | 2 | $0 | 0 | $0 |
| COL11 | 2 | $0 | 0 | $0 |
| COL134 | 4 | $0 | 0 | $0 |
| COL136 | 2 | $0 | 0 | $0 |
| COL148 | 4 | $0 | 0 | $0 |
| COL152 | 6 | $0 | 0 | $0 |
| COL167 | 2 | $0 | 0 | $0 |
| COL169 | 3 | $0 | 0 | $0 |
| COL212 | 2 | $0 | 0 | $0 |
| COL218 | 2 | $0 | 0 | $0 |
| COL219 | 8 | $0 | 0 | $0 |
| COL226 | 2 | $0 | 0 | $0 |
| COL248 | 2 | $0 | 0 | $0 |
| COL256 | 1 | $0 | 0 | $0 |
| COL262 | 2 | $0 | 0 | $0 |
| COL280 | 3 | $0 | 0 | $0 |
| COL287 | 1 | $0 | 0 | $0 |
| COL288 | 2 | $0 | 0 | $0 |
| COL298 | 3 | $0 | 0 | $0 |
| COL300 | 3 | $0 | 0 | $0 |
| COL301 | 2 | $0 | 0 | $0 |
| COL304 | 8 | $0 | 0 | $0 |
| COL305 | 1 | $0 | 0 | $0 |
| COL306 | 2 | $0 | 0 | $0 |
| COL31 | 2 | $0 | 0 | $0 |
| COL318 | 1 | $0 | 0 | $0 |
| COL326 | 2 | $0 | 0 | $0 |
| COL33 | 1 | $0 | 0 | $0 |
| COL338 | 8 | $0 | 0 | $0 |
| COL343 | 12 | $0 | 0 | $0 |
| COL370 | 1 | $0 | 0 | $0 |
| COL385 | 2 | $0 | 0 | $0 |
| COL39 | 3 | $0 | 0 | $0 |
| COL40 | 9 | $0 | 0 | $0 |
| COL400 | 4 | $0 | 0 | $0 |
| COL401 | 2 | $0 | 0 | $0 |
| COL403 | 3 | $0 | 0 | $0 |
| COL405 | 14 | $0 | 0 | $0 |
| COL406 | 18 | $0 | 0 | $0 |
| COL407 | 1 | $0 | 0 | $0 |
| COL408 | 2 | $0 | 0 | $0 |
| COL410 | 8 | $0 | 0 | $0 |
| COL411 | 3 | $0 | 0 | $0 |
| COL413 | 4 | $0 | 0 | $0 |
| COL414 | 3 | $0 | 0 | $0 |
| COL415 | 3 | $0 | 0 | $0 |
| COL416 | 4 | $0 | 0 | $0 |
| COL417 | 1 | $0 | 0 | $0 |
| COL418 | 1 | $0 | 0 | $0 |
| COL419 | 1 | $0 | 0 | $0 |
| COL420 | 1 | $0 | 0 | $0 |
| COL421 | 1 | $0 | 0 | $0 |
| COL422 | 1 | $0 | 0 | $0 |
| COL424 | 1 | $0 | 0 | $0 |
| COL425 | 4 | $0 | 0 | $0 |
| COL426 | 6 | $0 | 0 | $0 |
| COL427 | 2 | $0 | 0 | $0 |
| COL428 | 2 | $0 | 0 | $0 |
| COL57 | 1 | $0 | 0 | $0 |
| COL58 | 1 | $0 | 0 | $0 |
| COL61 | 3 | $0 | 0 | $0 |
| COL63 | 3 | $0 | 0 | $0 |
| COL79 | 4 | $0 | 0 | $0 |
| COL86 | 3 | $0 | 0 | $0 |
| COL92 | 2 | $0 | 0 | $0 |
| EOS | 2 | $0 | 0 | $0 |
| HARDY | 3 | $0 | 0 | $0 |
| KEEVA | 4 | $0 | 0 | $0 |
| KEIRA | 4 | $0 | 0 | $0 |
| MISHA | 1 | $0 | 0 | $0 |
| PALLO | 1 | $0 | 0 | $0 |
| PAM | 1 | $0 | 0 | $0 |
| RENS | 2 | $0 | 0 | $0 |
| YATES | 6 | $0 | 0 | $0 |
| ZANE | 6 | $0 | 0 | $0 |
| — | 2 | $0 | 0 | $0 |

### Q-59_results.md

# Q-59 Results — Craftmade (clli, org_id=149)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ITEM | ECF111BNK5-DWWLN-P48 | Pallet of (48) ECF Fans | Uncategorized | — | — | 95 | 4 | 3,398.97 | 322,901.89 | 423,846.72 | 6 |
| ITEM | MCY52BNK3 | McCoy 52" 3-Blade Ceiling Fan in Brushed Polished Nickel w/ Brushed Nickel Blades; Light Kit Included (optional) | CAT24 | — | — | 1,657 | 41 | 103.38 | 171,297.51 | 291,286.82 | 94 |
| ITEM | PHZ52FB3 | Phaze II 52" 3-Blade Ceiling Fan in Flat Black w/ Flat Black/Greywood Blades; Integrated Light Kit | CAT24 | — | — | 1,651 | 15 | 100.43 | 165,816.91 | 263,826.08 | 73 |
| ITEM | PHZ52FB4 | Phaze II 52" 4-Blade Ceiling Fan in Flat Blak w/ Flat Black/Greywood Blades; Integrated Light Kit | CAT24 | — | — | 1,572 | 16 | 101.15 | 159,002.70 | 332,505.54 | 50 |
| ITEM | MCY52W4 | McCoy 52" 4-Blade Ceiling Fan in White w/ White Blades; Light Kit Included (optional) | CAT24 | — | — | 1,362 | 34 | 110.94 | 151,105.93 | 203,696.59 | 72 |
| ITEM | MCY52W5 | McCoy 52" 5-Blade Ceiling Fan in White w/ White Blades; Light Kit Included (optional) | CAT24 | — | — | 1,313 | 35 | 114.06 | 149,755.68 | 276,026.51 | 98 |
| ITEM | EPHA52FB5 | Phaze Energy Star 5 52" 5-Blade Ceiling Fan in Flat Black w/ Flat Black/Greywood Blades; Integrated Light Kit | CAT24 | — | — | 1,209 | 4 | 115.97 | 140,207.73 | 303,991.65 | 15 |
| ITEM | MCY52W3 | McCoy 52" 3-Blade Celling Fan in White w/ White Blades; Light Kit Included (optional) | CAT24 | — | — | 1,143 | 39 | 104.54 | 119,490.27 | 395,089.89 | 131 |
| ITEM | CK1000-W | Builder Chime Kit in White | CAT11 | — | — | 7,358 | 36 | 14.80 | 108,930.27 | 1,796,611.40 | 227 |
| ITEM | P104FB5-52FBGW | Pro Plus 104 52" 5-Blade Ceiling Fan in Flat Black w/ Flat Black/Grey Wood Blades; Integrated Light Kit | CAT24 | — | — | 998 | 54 | 107.98 | 107,766.12 | 844,825.11 | 146 |
| ITEM | PHZ52FB5 | Phaze II 52" 5-Blade Ceiling Fan in Flat Black w/ Flat Black/Greywood Blades; Integrated Light Kit | CAT24 | — | — | 1,020 | 11 | 103.68 | 105,757.31 | 137,158.44 | 65 |
| ITEM | ZA4004-MN | Perimeter 1 Light Small Outdoor Wall Mount in Midnight | CAT26 | — | — | 2,124 | 13 | 47.93 | 101,803.98 | 97,727.71 | 40 |
| ITEM | CK1003-W | Builder Chime Kit in White | CAT11 | — | — | 3,820 | 34 | 26.57 | 101,508.35 | 689,608.14 | 77 |
| ITEM | Z422-MN-LED | 2 Light Outdoor LED Flood in Midnight | CAT40 | — | — | 4,695 | 76 | 19.52 | 91,666.79 | 304,016.95 | 136 |
| ITEM | P119BNK5-52DWGWN | Pro Plus 119 52" 5-Blade Ceiling Fan in Brushed Polished Nickel w/ Driftwood/Grey Walnut Blades; Light Kit Included (optional) | CAT24 | — | — | 786 | 13 | 109.69 | 86,215.29 | 168,286.37 | 31 |
| ITEM | PHZ52BNK5-BNGW | Phaze II 52" 5-Blade Ceiling Fan in Brushed Polished Nickel w/ Brushed Nickel/Greywood Blades; Integrated Light Kit | CAT24 | — | — | 794 | 9 | 106.48 | 84,544.24 | 231,046.64 | 30 |

### Q-61_results.md

# Q-61 Results — Craftmade (clli, org_id=149)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EMCY52BNK4-PC | Energy Star McCoy 52" 4-Blade Ceiling Fan in Brushed Polished Nickel w/ Brushed Nickel Blades; Light Kit Included (Optional) | CAT24 | 11 | 460 | 43,486.38 | 19 | 115 |
| ECF201FB5-FBGW | Eos 52" 5-Blade Clear 2 Light Bowl Ceiling Fan in Flat Black w/ Flat Black/Greywood Blades; Light Kit Included (Optional) | CAT24 | 12 | 306 | 27,037.08 | 47 | 97 |
| MIR2410RT-FB3C | Slim Lite 24" x 36" Rectangle Front/Back Lit LED Mirror, Dimmer, 3000-5000K, in Flat Black | CAT3 | 24 | 86 | 26,867.60 | 45 | 319 |
| MIR2409RT-W3C | Meredith 24" x 36" Rectangle Front/Back Lit LED Mirror, Dimmer, 3000-5000K, in White | CAT3 | 31 | 117 | 20,878.05 | 43 | 199 |
| MIR2413M-W3C | LED Cabinet Mirror | CAT3 | 16 | 41 | 19,182.10 | 28 | 499 |
| CHM52SB3 | Charming 52" 3-Blade Ceiling Fan in Satin Brass w/ White Blades; Light Kit Sold Separately | CAT24 | 36 | 148 | 17,255 | 76 | 119 |
| GTY52FB5 | Getaway 52" 5-Blade Outdoor Ceiling Fan in Walnut  Blades; Not Light Kit Adaptable | CAT1 | 29 | 75 | 17,030.48 | 46 | 229 |
| KLS52SB4 | Kelsey 52" 4-Blade Ceiling Fan in Satin Brass w/ Flat Black Blades; Integrated Light Kit | CAT24 | 38 | 128 | 16,512.70 | 72 | 139 |
| ZA8010-TB | Jordan 3 Light Outdoor Wall Lantern in Textured Black | CAT26 | 16 | 91 | 15,730.84 | 30 | 189 |
| RSL52SBW5 | Rosalie 52" 5-Blade Ceiling Fan in Satin Brass/White w/ White Blades; Integrated Light Kit | CAT24 | 38 | 100 | 15,613.80 | 78 | 159 |
| 61173-CPZ | Pleated 3 Light Island in Premium Bronze | CAT16 | 24 | 57 | 13,488.10 | 41 | 229 |
| FON65SBFB5 | Fonz 65" 5-Blade Ceiling Fan in Satin Brass w/ Flat Black Blades; Light Kit Included (Optional) | CAT24 | 19 | 48 | 12,643 | 34 | 269 |
| ECF119BNK5-DWWLN | Eos 52" 5-Blade Ceiling Fan in Brushed Polished Nickel w/ Driftwood/Walnut Blades; LED Pan Light Kit Included (Optional) | CAT24 | 20 | 123 | 11,157.30 | 35 | 95 |
| PHB52FB3 | Phoebe 52" 3-Blade Ceiling Fan in Flat Black w/ Flat Black Blades; Light Kit Sold Separately | CAT24 | 22 | 69 | 11,130 | 42 | 159 |
| ECF104SB5-BWNFB | Eos 52" 5-Blade Clear 4 Light Ceiling Fan in Satin Brass w/ Black Walnut/Flat Black Blades; Integrated Light Kit | CAT24 | 28 | 120 | 10,946.12 | 59 | 99 |
| PHB52W3 | Phoebe 52" 3-Blade Ceiling Fan in White w/ White Blades; Light Kit Sold Separately | CAT24 | 17 | 65 | 10,587 | 30 | 159 |
| EMCY52FB4-PC | Energy Star McCoy 52" 4-Blade Ceiling Fan in Flat Black w/ Flat Black Blades; Light Kit Included (Optional) | CAT24 | 11 | 98 | 9,881.42 | 21 | 115 |
| ZA7710-TB | Irving 2 Light Outdoor Wall Lantern in Textured Black | CAT26 | 23 | 90 | 9,777.30 | 46 | 109 |
| FRZ56SB3 | Frazier 52" 3-Blade Ceiling Fan in Satin Brass w/ Flat Black Blades; Light Kit Sold Separately | CAT24 | 16 | 51 | 9,384 | 28 | 184 |
| CZY52FB3 | Cozy 52" 3-Blade Ceiling Fan w/ Pull Chain in Flat Black w/ Flat Black Blades; Light Kit Included (Optional) | CAT24 | 20 | 104 | 9,213.31 | 47 | 95 |
| ZA8030-TB | Jordan 38" 4 Light Outdoor Wall Lantern in Textured Black | CAT26 | 8 | 36 | 9,023.95 | 16 | 269 |
| CHM52FB3 | Charming 52" 3-Blade Ceiling Fan in Flat Black w/ Flat Black Blades ; Light Kit Sold Separately | CAT24 | 18 | 80 | 8,865 | 38 | 115 |
| ZA7720-TB | Irving 3 Light Outdoor Wall Lantern in Textured Black | CAT26 | 9 | 38 | 8,702 | 17 | 229 |
| 61226-FB | Reflection 6 Light Chandelier in Flat Black | CAT13 | 18 | 42 | 8,649.55 | 28 | 199 |
| ZA8020-TB | Jordan 32.5" 4 Light Outdoor Wall Lantern in Textured Black | CAT26 | 10 | 34 | 8,221.20 | 17 | 249 |
| 61391W-SB | Keira 1 Light Pendant in Satin Brass (White Rope) | CAT14 | 23 | 53 | 8,105.60 | 34 | 149 |
| ECF52CBZ5-CBZWLN | Eos 52" 5-Blade Ceiling Fan in Classic Bronze w/ Classic Bronze/Walnut Blades; Light Kit Optional (Not Included) | CAT24 | 28 | 125 | 7,983.99 | 52 | 67 |
| 61226-CPZ | Reflection 6 Light Chandelier in Premium Bronze | CAT13 | 17 | 35 | 7,895.96 | 23 | 218 |
| ECF201SB5-BWNFB | Eos 52" 5-Blade Clear 2 Light Bowl Ceiling Fan in Satin Brass w/ Black Walnut/Flat Black Blades; Light Kit Included (Optional) | CAT24 | 17 | 85 | 7,560.26 | 39 | 99 |
| FRZ56FB3 | Frazier 56" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Flat Black w/ Flat Black Blades; Light Kit Sold Separately | CAT1 | 17 | 41 | 7,544 | 28 | 184 |

### Q-ORG-GHOST_results.md

# Q-ORG-GHOST Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-GHOST — Ghost SKU Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | customer_count | total_revenue | total_units | status |
| --- | --- | --- | --- | --- |
| C102L | 233 | 1,233,970.14 | 122,992 | GHOST — no catalog record |
| DCF52BNK5C1 | 93 | 1,166,094.82 | 23,091 | GHOST — no catalog record |
| DCF52BNK5C3 | 78 | 832,394.61 | 16,403 | GHOST — no catalog record |
| CON48BNK4C1-48BN | 26 | 584,108.44 | 10,362 | GHOST — no catalog record |
| C201BN | 128 | 466,770.34 | 9,093 | GHOST — no catalog record |
| CON48BNK4C1 | 91 | 466,592.65 | 8,088 | GHOST — no catalog record |
| C52-KIT | 294 | 437,374.22 | 10,344 | GHOST — no catalog record |
| K11311 | 1 | 421,821 | 1,840 | GHOST — no catalog record |
| K11072 | 2 | 349,917 | 6,301 | GHOST — no catalog record |
| TG52BNK3-WM6W | 1 | 338,100 | 3,689 | GHOST — no catalog record |
| TEA52CH4-18W | 1 | 289,835 | 3,370 | GHOST — no catalog record |
| DCF52FBZ5C1 | 88 | 280,207.66 | 5,618 | GHOST — no catalog record |
| DCF52FBZ5C3 | 76 | 274,563.15 | 5,635 | GHOST — no catalog record |
| TFV70REC | 91 | 236,895.39 | 5,162 | GHOST — no catalog record |
| ANI36BNK3 | 129 | 217,174.34 | 821 | GHOST — no catalog record |
| UCI-2000 | 422 | 212,749.54 | 7,857 | GHOST — no catalog record |
| K11291 | 43 | 200,937.39 | 1,256 | GHOST — no catalog record |
| K11289 | 34 | 198,082.66 | 1,262 | GHOST — no catalog record |
| K11080 | 4 | 186,464.80 | 3,214 | GHOST — no catalog record |
| WND78ESP6 | 85 | 185,847.22 | 453 | GHOST — no catalog record |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BW414AG3 | Bellows IV 14" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Aged Bronze Textured w/ Aged Bronze Blades; Not Light Kit Adaptable | COL53 | 281,687.35 | 1,562 | 10 | 2026-07-20 | [{'customer': '1STOPLIGHTING-I', 'revenue': 52219.38}, {'customer': 'FERGUSONHOME.COM', 'revenue': 27861.72}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 19799.79}, {'customer': 'DELMAR FANS', 'revenue': 12045.15}, {'customer': 'WAYFAIR LLC-I', 'revenue': 11717.96}, {'customer': 'LUMENS LIGHT + LIVING-I', 'revenue': 7606.36}, {'customer': 'LIGHTING INC.', 'revenue': 7605.0}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 7374.85}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 4563.0}, {'customer': 'LAMPS PLUS', 'revenue': 4212.0}, {'customer': 'JABEN HOLDINGS INC-I', 'revenue': 3861.0}, {'customer': 'ELLER ENTERPRISES', 'revenue': 3716.7}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 3705.0}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 3120.0}, {'customer': 'HOUZZ SHOP LLC', 'revenue': 3120.0}, {'customer': 'DESIGN LIGHTING GROUP LLC-C', 'revenue': 3120.0}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 2730.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 2593.5}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 2535.0}, {'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 2363.4}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 2340.0}, {'customer': 'TRI SUPPLY', 'revenue': 2340.0}, {'customer': 'PASSION LIGHTING', 'revenue': 2340.0}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 2340.0}, {'customer': "GRAHAM'S LIGHTING INC", 'revenue': 2145.0}, {'customer': 'VILLA LIGHTING SUPPLY INC', 'revenue': 1950.0}, {'customer': 'MASTERPIECE LIGHTING', 'revenue': 1950.0}, {'customer': 'NET RETAILERS LLC-CII ONLY', 'revenue': 1950.0}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 1766.7}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 1755.0}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 1755.0}, {'customer': 'CAPITOL LIGHTING', 'revenue': 1755.0}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 1725.75}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 1560.0}, {'customer': 'AA PORTER', 'revenue': 1560.0}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 1376.7}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 1365.0}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 1365.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 1335.75}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 1318.98}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 1269.45}, {'customer': 'GOING DECOR', 'revenue': 1170.0}, {'customer': 'VALUE LIGHTING INC', 'revenue': 1170.0}, {'customer': 'LOWE ELECTRIC SUPPLY CO', 'revenue': 1170.0}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 1170.0}, {'customer': 'A & W LIGHTING', 'revenue': 1170.0}, {'customer': 'SONEPAR-USA', 'revenue': 1170.0}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 1170.0}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 1038.9}, {'customer': 'MAYER ELECTRIC SUPPLY CO INC', 'revenue': 975.0}, {'customer': 'STATE ELECTRIC SUPPLY CO', 'revenue': 945.75}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 945.75}, {'customer': 'ATHENIA MASON SUPPLY WILMINGTO', 'revenue': 928.2}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 877.5}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 803.4}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 780.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 780.0}, {'customer': 'MADISON LIGHTING', 'revenue': 780.0}, {'customer': 'MANASQUAN LIGHTING', 'revenue': 780.0}, {'customer': 'LIGHTING INC', 'revenue': 780.0}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 780.0}, {'customer': 'GREER LIGHTING CENTER LLC', 'revenue': 780.0}, {'customer': 'AFFORDABLE LIGHTING', 'revenue': 780.0}, {'customer': 'LIGHTING ETC', 'revenue': 780.0}, {'customer': 'CAJUN ELECTRIC, LLC', 'revenue': 780.0}, {'customer': 'WILLIAM L HART DESIGNS LLC', 'revenue': 780.0}, {'customer': 'LEGACY LIGHTING LLC', 'revenue': 716.0}, {'customer': 'POWER DESIGN RESOURCES', 'revenue': 704.0}, {'customer': 'PROGRESSIVE LIGHTING-I', 'revenue': 702.0}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 686.4}, {'customer': 'RGM DISTRIBUTION INC-I', 'revenue': 620.1}, {'customer': 'PINE GROVE ELEC SPLY', 'revenue': 585.0}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 585.0}, {'customer': "RON'S LUMBER AND HOME CENTER", 'revenue': 585.0}, {'customer': 'AMERICAN LIGHTING', 'revenue': 585.0}, {'customer': 'MATHES OF ALABAMA', 'revenue': 585.0}, {'customer': 'THE LIGHTING STUDIO, LLC', 'revenue': 585.0}, {'customer': 'KEIDEL SUPPLY CO INC', 'revenue': 585.0}, {'customer': 'T J S SUPPLY CO', 'revenue': 585.0}, {'customer': 'LED CAPSTONE INC.', 'revenue': 585.0}, {'customer': 'FAN DIEGO INC', 'revenue': 569.0}, {'customer': 'DUNCAN LIGHTING & HOME-I', 'revenue': 555.75}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 549.9}, {'customer': 'CAPE ELECTRIC SUPPLY', 'revenue': 538.2}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 526.5}, {'customer': 'ARCADIAN LIGHTING INC-I', 'revenue': 526.5}, {'customer': 'HOUSE ACCOUNT', 'revenue': 427.34}, {'customer': 'MENARDS - CRAFTMADE', 'revenue': 407.32}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 390.0}, {'customer': 'JPR LIGHTING INC', 'revenue': 390.0}, {'customer': 'SOUTHERN LTG GALLERY', 'revenue': 390.0}, {'customer': "FARREY'S WHOLESALE HARDWARE", 'revenue': 390.0}, {'customer': 'ONE SOURCE LIGHTING', 'revenue': 390.0}, {'customer': 'BES LIGHTING & HOME', 'revenue': 390.0}, {'customer': 'BUILD IT FAB INC', 'revenue': 390.0}, {'customer': 'HALL ELECTRIC', 'revenue': 390.0}, {'customer': 'SHEALY ELECTRIC CO', 'revenue': 390.0}, {'customer': 'TEC OF JONESBORO INC', 'revenue': 390.0}, {'customer': 'TECHE ELECTRIC', 'revenue': 390.0}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 390.0}, {'customer': 'BETTER HOMES SUPPLY', 'revenue': 390.0}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 390.0}, {'customer': 'LIGHTING CORNER, THE', 'revenue': 390.0}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 390.0}, {'customer': 'HAYNEEDLE,INC-I', 'revenue': 390.0}, {'customer': 'LOW COUNTRY LIGHTING INC', 'revenue': 390.0}, {'customer': 'ZORO TOOLS, INC. DBA ZORO', 'revenue': 390.0}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 390.0}, {'customer': 'ECHO ELECTRIC SUPPLY', 'revenue': 390.0}, {'customer': None, 'revenue': 390.0}, {'customer': 'CR LIGHTING', 'revenue': 390.0}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 390.0}, {'customer': 'LIGHTING PLUS', 'revenue': 390.0}, {'customer': 'LIGHT HOUSE, THE', 'revenue': 390.0}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 390.0}, {'customer': 'MADDUX LIGHTING GALLERY& SUPPL', 'revenue': 390.0}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 390.0}, {'customer': "LYDIA'S", 'revenue': 390.0}, {'customer': 'LIGHT DEPOT LLC', 'revenue': 390.0}, {'customer': 'METRO LIGHTING', 'revenue': 370.5}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 351.0}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 351.0}, {'customer': 'RICHARDSON HOUSE OF FIXTURES', 'revenue': 214.5}, {'customer': 'UNION LUMINAIRES ET DECOR', 'revenue': 214.5}, {'customer': 'ROYAUME LUMINAIRE LANDAUDIERE', 'revenue': 214.5}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 206.7}, {'customer': 'FREY ELECTRIC INC', 'revenue': 195.0}, {'customer': 'FORD BOYD INTERIORS DBA VERVE', 'revenue': 195.0}, {'customer': 'DOMINION ELECTRIC SUPPLY CO', 'revenue': 195.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 195.0}, {'customer': 'IDAHO DREAMING', 'revenue': 195.0}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 195.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 195.0}, {'customer': 'WINSUPPLY INC', 'revenue': 195.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 195.0}, {'customer': 'WEST BROWARD BULB INC', 'revenue': 195.0}, {'customer': 'KENYON-NOBLE LUMBER CO', 'revenue': 195.0}, {'customer': 'JOHNSON BURKS SUPPLY COMPANY', 'revenue': 195.0}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 195.0}, {'customer': 'VILLAGE LIGHTING & SUPPLY INC', 'revenue': 195.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 195.0}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 195.0}, {'customer': 'NORTHWOOD LIGHTING', 'revenue': 195.0}, {'customer': 'M & M LIGHTING LP', 'revenue': 195.0}, {'customer': 'TEC OF NORTH LITTLE ROCK', 'revenue': 195.0}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 195.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 195.0}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 195.0}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 195.0}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 195.0}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 195.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 195.0}, {'customer': 'WILSON LIGHTING STL', 'revenue': 195.0}, {'customer': 'R WILSON INC', 'revenue': 195.0}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 195.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 195.0}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 195.0}, {'customer': 'COLEY ELECTRIC-WAYCROSS', 'revenue': 195.0}, {'customer': 'J. H. LARSON COMPANY', 'revenue': 195.0}, {'customer': 'LUMENAREA', 'revenue': 195.0}, {'customer': 'C.E.S. CO NC DIVISION', 'revenue': 195.0}, {'customer': 'C.E.D.', 'revenue': 195.0}, {'customer': 'USESI', 'revenue': 195.0}, {'customer': 'FILAMENT INC', 'revenue': 195.0}, {'customer': 'KINGS WAGON YARD', 'revenue': 195.0}, {'customer': 'LIGHTING ORIGINALS INC.', 'revenue': 193.05}, {'customer': 'ROYAUME LUMINAIRE STE JULIE', 'revenue': 171.6}, {'customer': 'FANS PLUS', 'revenue': 169.65}, {'customer': 'LOFINGS LIGHTING', 'revenue': 167.7}, {'customer': 'CUSTOMER SERVICE ELECTRIC SUPP', 'revenue': 156.0}, {'customer': 'Craftmade Warranty Account', 'revenue': 0.0}] | [{'item': 'BW414BNK3', 'desc': 'Bellows IV 14" 3-Blade Ceiling Fan in Brushed Polished Nickel w/ Brushed Polished Nickel Blades; Not Light Kit Adaptable', 'available': 110}] |
| BW321AG3 | Bellows III 18" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Aged Bronze Textured w/ Aged Bronze Blades; Not Light Kit Adaptable | COL52 | 266,996.31 | 1,143 | 12 | 2026-07-20 | [{'customer': '1STOPLIGHTING-I', 'revenue': 30920.77}, {'customer': 'WAYFAIR LLC-I', 'revenue': 26810.83}, {'customer': 'FERGUSONHOME.COM', 'revenue': 18009.6}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 12092.4}, {'customer': 'LAMPS PLUS', 'revenue': 7497.99}, {'customer': 'LUMENS LIGHT + LIVING-I', 'revenue': 6942.6}, {'customer': 'TECHE ELECTRIC', 'revenue': 6552.0}, {'customer': 'LIGHTING INC.', 'revenue': 6360.4}, {'customer': 'DELMAR FANS', 'revenue': 6350.4}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 6299.9}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 4929.35}, {'customer': 'SPECIALTY LIGHTING GROUP LLC', 'revenue': 4536.0}, {'customer': 'AA PORTER', 'revenue': 4536.0}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 4095.0}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 3742.2}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 3558.2}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 3528.0}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 3276.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3192.8}, {'customer': "GRAHAM'S LIGHTING INC", 'revenue': 3024.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 2802.2}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 2802.2}, {'customer': 'PARALLAX INDUSTRIES, INC.', 'revenue': 2797.2}, {'customer': 'ELLER ENTERPRISES', 'revenue': 2772.0}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 2764.0}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 2721.6}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 2520.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 2520.0}, {'customer': 'PASSION LIGHTING', 'revenue': 2016.0}, {'customer': 'LOWE ELECTRIC SUPPLY CO', 'revenue': 1764.0}, {'customer': "HAGEN'S", 'revenue': 1764.0}, {'customer': 'GOING DECOR', 'revenue': 1542.2}, {'customer': 'GALLERY OF LTG', 'revenue': 1512.0}, {'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 1512.0}, {'customer': 'ABC LIGHTING', 'revenue': 1512.0}, {'customer': 'M & M LIGHTING LP', 'revenue': 1512.0}, {'customer': 'DESIGN LIGHTING GROUP LLC-C', 'revenue': 1512.0}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 1499.4}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 1421.28}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 1260.0}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 1260.0}, {'customer': 'TEC OF JONESBORO INC', 'revenue': 1260.0}, {'customer': 'FAN DIEGO INC', 'revenue': 1199.5}, {'customer': 'METRO LIGHTING', 'revenue': 1134.0}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 1105.2}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 1008.0}, {'customer': "ARMSTRONG'S SUPPLY CO", 'revenue': 1008.0}, {'customer': "JOSEPH'S ELECTRICAL CENTER", 'revenue': 1008.0}, {'customer': 'LIGHTING SHOWROOM INC', 'revenue': 1008.0}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 1008.0}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 1008.0}, {'customer': 'LABELLE CABINETRY & LTG-', 'revenue': 1008.0}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 1008.0}, {'customer': 'SOUTHLAND PLUMBING SUPPLY INC', 'revenue': 1008.0}, {'customer': 'LIGHTS OF OCONEE LLC', 'revenue': 1008.0}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 937.44}, {'customer': 'JABEN HOLDINGS INC-I', 'revenue': 907.2}, {'customer': 'MULTI LUMINAIRE ST. HUBERT', 'revenue': 881.43}, {'customer': 'LIGHTSHINE INC', 'revenue': 771.1}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 756.0}, {'customer': "CAPPADONNA'S OF ARIZONA", 'revenue': 756.0}, {'customer': 'NORTHERN LIGHTS & FANS LLC', 'revenue': 756.0}, {'customer': 'MID-SOUTH LIGHTING', 'revenue': 756.0}, {'customer': "ISABELLE'S LIGHTING INC.", 'revenue': 756.0}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 756.0}, {'customer': 'GADSDEN LIGHTING', 'revenue': 756.0}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 756.0}, {'customer': 'C.E.S.TX DIV', 'revenue': 756.0}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 756.0}, {'customer': None, 'revenue': 756.0}, {'customer': 'SANDERS SUPPLY INC', 'revenue': 756.0}, {'customer': 'ELITEFIXTURES.COM-I', 'revenue': 756.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 756.0}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 756.0}, {'customer': 'GATEWAY LTG & DESIGN INC', 'revenue': 756.0}, {'customer': 'LIGHTING WORKS', 'revenue': 756.0}, {'customer': 'HARDWOOD FLOORS & MORE-CXT', 'revenue': 756.0}, {'customer': 'ELLEN LIGHTING & HARDWARE', 'revenue': 756.0}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 756.0}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 748.0}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 703.08}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 680.4}, {'customer': 'DORIAN DRAKE INTERNATIONAL INC', 'revenue': 642.6}, {'customer': 'BLACK DIAMOND ACQUISITIONS', 'revenue': 504.0}, {'customer': "LYDIA'S", 'revenue': 504.0}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 504.0}, {'customer': 'COLEY ELECTRIC-WAYCROSS', 'revenue': 504.0}, {'customer': 'HI-LIGHT DECORATING', 'revenue': 504.0}, {'customer': 'REVERE ELECTRIC SUPPLY', 'revenue': 504.0}, {'customer': 'UNIVERSAL LIGHTS INC', 'revenue': 504.0}, {'customer': 'LIGHTING & REFLECTIONS', 'revenue': 504.0}, {'customer': 'STEVENS LIGHTING FIXTURE CO', 'revenue': 504.0}, {'customer': 'GROSS LIGHTING & HOME', 'revenue': 504.0}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 504.0}, {'customer': 'COMPLETE LIGHTING OF TAMPA', 'revenue': 504.0}, {'customer': 'CAPISTRANO LIGHTING', 'revenue': 504.0}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 504.0}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 504.0}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 504.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 504.0}, {'customer': 'HOUSE OF LIGHTS OF SANFORD INC', 'revenue': 504.0}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 504.0}, {'customer': 'HOME LIGHTING & SUPPLY INC', 'revenue': 504.0}, {'customer': 'SOUTHSIDE LIGHTING GALLERY', 'revenue': 504.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 478.8}, {'customer': 'CAPE ELECTRIC SUPPLY', 'revenue': 463.68}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 443.52}, {'customer': 'PC HOME CENTER', 'revenue': 428.4}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 424.12}, {'customer': 'ELFORD/TEIBER', 'revenue': 403.2}, {'customer': 'HOUSE ACCOUNT', 'revenue': 376.0}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 277.2}, {'customer': 'LUMINAIRES PAUL GREGOIRE INC', 'revenue': 277.2}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 267.1}, {'customer': 'TLC LIGHTING ON, LLC', 'revenue': 252.0}, {'customer': 'SHEALY ELECTRIC CO', 'revenue': 252.0}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 252.0}, {'customer': "RICK'S LIGHTING & SUPPLIES INC", 'revenue': 252.0}, {'customer': 'WEST BROWARD BULB INC', 'revenue': 252.0}, {'customer': 'LIGHTING EFX INC', 'revenue': 252.0}, {'customer': 'LIGHTING PLUS INC', 'revenue': 252.0}, {'customer': 'C.A.I. DESIGNS', 'revenue': 252.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 252.0}, {'customer': 'CONSTANT ELECTRIC', 'revenue': 252.0}, {'customer': 'QUIGLEY LIGHTING CO', 'revenue': 252.0}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 252.0}, {'customer': '1-800 MY LAMPS-I', 'revenue': 252.0}, {'customer': 'PRESTIGE LIGHTING AND DESIGN L', 'revenue': 252.0}, {'customer': 'NORTH AND SOUTH SALES', 'revenue': 252.0}, {'customer': 'CAROLINA LANTERNS & LIGHTING', 'revenue': 252.0}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 252.0}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 252.0}, {'customer': 'CAROLINA SUPPLY HOUSE INC', 'revenue': 252.0}, {'customer': 'LITE HOUSE INC', 'revenue': 252.0}, {'customer': 'ARIZONA LIGHTING CO OF YUMA', 'revenue': 252.0}, {'customer': 'PREMIER BATH, LTG & HDW LLC', 'revenue': 252.0}, {'customer': 'BEAUTIFUL THINGS', 'revenue': 252.0}, {'customer': 'HENSONS CARPET ONE', 'revenue': 252.0}, {'customer': 'EAST VALLEY FANS & BLINDS', 'revenue': 252.0}, {'customer': 'CAJUN ELECTRIC, LLC', 'revenue': 252.0}, {'customer': 'EDWARD JOY LIGHTING & ELEC SUP', 'revenue': 239.4}, {'customer': 'RE-LIGHTING', 'revenue': 235.62}, {'customer': None, 'revenue': 226.8}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 226.8}, {'customer': 'PROGRESSIVE LIGHTING-I', 'revenue': 226.8}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 226.8}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 214.2}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 214.2}, {'customer': 'HOME LIGHTING', 'revenue': 0.0}, {'customer': 'ECHO ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'IMAGINE MORE SERVICE CORP.', 'revenue': 0.0}, {'customer': 'Craftmade Warranty Account', 'revenue': 0.0}] | — |
| 50504-FB | Bolden 4 Light Vanity in Flat Black | COL234 | 193,427.01 | 3,290 | 3 | 2026-06-30 | [{'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 25723.39}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 15830.26}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 10297.33}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 9329.35}, {'customer': 'FERGUSONHOME.COM', 'revenue': 7044.93}, {'customer': 'LUXUR LIGHTING', 'revenue': 5460.9}, {'customer': 'METRO LIGHTING', 'revenue': 5371.26}, {'customer': 'T J S SUPPLY CO', 'revenue': 5276.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 4473.58}, {'customer': 'WAYFAIR LLC-I', 'revenue': 4341.11}, {'customer': 'TRI SUPPLY', 'revenue': 3660.5}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 3560.84}, {'customer': 'PREMIER INDUSTRIES INC', 'revenue': 3108.18}, {'customer': 'HEARTH & HOME', 'revenue': 2877.25}, {'customer': 'LIGHTING INC.', 'revenue': 2838.0}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 2784.35}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 2744.75}, {'customer': 'RICHARDSON LIGHTING LTD', 'revenue': 2698.95}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 2298.54}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 2290.39}, {'customer': 'CLARKSVILLE LIGHTING', 'revenue': 2271.75}, {'customer': 'AMERICAN LIGHTING', 'revenue': 2271.75}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 2053.32}, {'customer': '1STOPLIGHTING-I', 'revenue': 1968.79}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 1775.5}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 1681.08}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 1645.0}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 1514.5}, {'customer': None, 'revenue': 1285.0}, {'customer': 'R.D.H.S.INC', 'revenue': 1172.0}, {'customer': 'PASSION LIGHTING', 'revenue': 1165.0}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 1139.36}, {'customer': 'COFFMAN HOME DECOR-', 'revenue': 1106.75}, {'customer': 'DUNCAN CORPORATION', 'revenue': 1100.34}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 1097.45}, {'customer': 'TLC LIGHTING ON, LLC', 'revenue': 1048.5}, {'customer': 'AT HOME, LLC DBA HOME LIGHTING', 'revenue': 1048.5}, {'customer': 'ENCORE FLOORING & BLDG PROD', 'revenue': 1048.5}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 1025.25}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 990.25}, {'customer': 'Q E D', 'revenue': 932.0}, {'customer': 'ILLUMINATIONS', 'revenue': 929.07}, {'customer': 'W T LIGHTING', 'revenue': 880.75}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 851.62}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 830.05}, {'customer': "HAGEN'S", 'revenue': 815.5}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 796.29}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 792.78}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 745.25}, {'customer': 'SMITHFIELD LIGHTING CENTER', 'revenue': 699.0}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 689.65}, {'customer': 'PC HOME CENTER', 'revenue': 647.75}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 644.25}, {'customer': 'PARALLAX INDUSTRIES, INC.', 'revenue': 616.51}, {'customer': "KELLY'S HOME CENTER", 'revenue': 613.8}, {'customer': 'PLATT ELECTRIC SUPPLY', 'revenue': 611.0}, {'customer': 'NOVA LIGHTING', 'revenue': 596.5}, {'customer': 'DELMAR FANS', 'revenue': 596.2}, {'customer': 'LITE HOUSE INC', 'revenue': 582.5}, {'customer': '43RD STREET LIGHTING', 'revenue': 582.5}, {'customer': 'C.E.S. CO NC DIVISION', 'revenue': 558.2}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 548.82}, {'customer': 'BRANDON LIGHTING INC', 'revenue': 545.25}, {'customer': 'LIGHTING & REFLECTIONS', 'revenue': 543.25}, {'customer': 'GOING DECOR', 'revenue': 542.0}, {'customer': 'BRAZORIA COUNTY LIGHTING', 'revenue': 542.0}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 527.75}, {'customer': 'COASTAL LIGHTING & SUPPLY INC', 'revenue': 524.25}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 524.25}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 505.61}, {'customer': None, 'revenue': 480.55}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 473.0}, {'customer': 'AA PORTER', 'revenue': 466.0}, {'customer': 'AMC LIGHTING & DECOR, INC.', 'revenue': 452.02}, {'customer': 'M.C.I. INC', 'revenue': 410.55}, {'customer': 'LOYDS ELECTRIC SUPPLY INC', 'revenue': 407.75}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 407.75}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 407.75}, {'customer': 'LUMEN NATION LLC', 'revenue': 406.5}, {'customer': "Dianna's Lighting Design & Con", 'revenue': 384.8}, {'customer': 'FLOOR BROKERS, THE', 'revenue': 359.0}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 353.0}, {'customer': 'KIRBY RISK SUPPLY CO INC', 'revenue': 349.5}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 349.5}, {'customer': 'HALL ELECTRIC', 'revenue': 349.5}, {'customer': 'RITE RUG CO.', 'revenue': 338.75}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 338.75}, {'customer': 'RIMROCK LIGHTING', 'revenue': 338.75}, {'customer': 'RE-LIGHTING', 'revenue': 332.02}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 328.59}, {'customer': 'KENYON-NOBLE LUMBER CO', 'revenue': 309.75}, {'customer': 'AMOS ELECTRIC SUPPLY COMPANY', 'revenue': 291.25}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 291.25}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 291.25}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 291.25}, {'customer': 'SUNDIAL LIGHTING LTD', 'revenue': 291.25}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 282.51}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 271.0}, {'customer': 'VILLAGE HOME STORES', 'revenue': 271.0}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 242.5}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 236.5}, {'customer': 'BETTER HOMES SUPPLY', 'revenue': 233.0}, {'customer': 'LIGHTING SPECIALTIES WAREHOUSE', 'revenue': 233.0}, {'customer': 'PARAMONT-EO INC', 'revenue': 233.0}, {'customer': 'COVERINGS LLC', 'revenue': 233.0}, {'customer': 'HERITAGE LIGHTING, LLC', 'revenue': 233.0}, {'customer': 'LIGHT HOUSE OF SUMTER, LLC', 'revenue': 226.59}, {'customer': 'ILLUMINATIONS INC', 'revenue': 206.78}, {'customer': 'ALPHA  SUPPLY CORP', 'revenue': 203.25}, {'customer': 'SOUTHSIDE LIGHTING GALLERY', 'revenue': 178.25}, {'customer': 'SIOUX EMPIRE LIGHTING', 'revenue': 178.25}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 178.25}, {'customer': 'PINE LIGHTING LTD', 'revenue': 178.25}, {'customer': None, 'revenue': 174.75}, {'customer': 'LIGHTING WORLD INC', 'revenue': 174.75}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 174.75}, {'customer': 'CENTURY LIGHTING CENTER', 'revenue': 174.75}, {'customer': 'GALAXIE LIGHTING INC', 'revenue': 174.75}, {'customer': 'MAYER ELECTRIC SUPPLY CO INC', 'revenue': 174.75}, {'customer': 'WINSUPPLY INC', 'revenue': 174.75}, {'customer': 'LIGHTSHINE INC', 'revenue': 174.75}, {'customer': 'GALLERIA LIGHTING', 'revenue': 174.75}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 174.75}, {'customer': 'EXPRESSIONS HOME LTG & DECOR', 'revenue': 174.75}, {'customer': 'TRINITY WHOLESALE DIST INC', 'revenue': 166.01}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 166.01}, {'customer': 'HARDWOOD FLOORS & MORE-CXT', 'revenue': 143.6}, {'customer': 'DESIGNER LIGHTING & FAN', 'revenue': 135.5}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 135.5}, {'customer': 'NORTHERN LIGHTS & FANS LLC', 'revenue': 135.5}, {'customer': 'KLS,LLC dba SPECTRUM LIGHTING', 'revenue': 135.5}, {'customer': "MAHLANDER'S", 'revenue': 135.5}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 135.5}, {'customer': 'FISHTRAP CREEK LIGHTING', 'revenue': 135.5}, {'customer': 'CAPITOL LIGHTING', 'revenue': 135.5}, {'customer': 'EDWARD JOY LIGHTING & ELEC SUP', 'revenue': 123.5}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 123.5}, {'customer': 'FARMVILLE WHOL ELEC SUPPLY CO', 'revenue': 120.0}, {'customer': 'BRITE WHOLESALE ELEC SUPPLY', 'revenue': 120.0}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 116.5}, {'customer': 'A & M ILLUMINATION', 'revenue': 116.5}, {'customer': 'GATEWAY LTG & DESIGN INC', 'revenue': 116.5}, {'customer': 'TECHE ELECTRIC', 'revenue': 116.5}, {'customer': 'FIXTURE THIS INC', 'revenue': 116.5}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 116.5}, {'customer': 'G & G ELECTRIC & PLUMBING', 'revenue': 116.5}, {'customer': 'THOMSON PREMIER LTG', 'revenue': 116.5}, {'customer': 'CHADWICK DESIGN', 'revenue': 116.5}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 116.5}, {'customer': 'SONEPAR-USA', 'revenue': 116.5}, {'customer': 'ACCENT LIGHTING INC', 'revenue': 116.5}, {'customer': 'R & R SUPPLY CO', 'revenue': 116.5}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 116.5}, {'customer': 'CITY LIGHTZ', 'revenue': 116.5}, {'customer': 'THE PLUMBING WAREHOUSE', 'revenue': 116.5}, {'customer': 'THE BUILDING CENTER, INC.', 'revenue': 116.5}, {'customer': 'USESI', 'revenue': 116.5}, {'customer': None, 'revenue': 116.5}, {'customer': 'LIGHTING ETC', 'revenue': 116.5}, {'customer': 'LEBANON ELECTRIC SUPPLY', 'revenue': 116.5}, {'customer': 'C.E.D.', 'revenue': 116.5}, {'customer': 'MOUNTAIN LIGHTING', 'revenue': 99.02}, {'customer': 'FACTORY LIGHTING OUTLET INC', 'revenue': 99.02}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 67.75}, {'customer': 'LIGHTS & MORE', 'revenue': 67.75}, {'customer': 'HOME LIGHTING', 'revenue': 67.75}, {'customer': 'ROYAL ENTERPRISES', 'revenue': 67.75}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 67.75}, {'customer': 'FELT LIGHTING CO', 'revenue': 67.75}, {'customer': 'DISPLAY MERCHANDISE-10', 'revenue': 67.75}, {'customer': 'MADISON LIGHTING', 'revenue': 67.75}, {'customer': 'FIRST SUPPLY LLC', 'revenue': 67.75}, {'customer': 'LOW ENERGY HOMES', 'revenue': 67.75}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 67.75}, {'customer': 'RADUE HOMES DBA INSPIRED SPACE', 'revenue': 67.75}, {'customer': 'THAXPACK, LLC DBA HOME LUXE', 'revenue': 67.75}, {'customer': 'LIGHTING SOUTH, LLC', 'revenue': 67.75}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 67.75}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 67.75}, {'customer': 'CAROLINA LTG GALLERY', 'revenue': 67.75}, {'customer': 'CARDELLO ELECTRIC SUPPLY CO.', 'revenue': 64.0}, {'customer': 'COVENTRY LIGHTING INC', 'revenue': 64.0}, {'customer': 'LIGHTING EFX INC', 'revenue': 61.75}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 61.75}, {'customer': 'CONNECTICUT LIGHTING CTR INC', 'revenue': 60.98}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 60.98}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 60.97}, {'customer': 'COASTAL LIGHTING SUPPLY CO INC', 'revenue': 58.25}, {'customer': 'TEC OF NORTH LITTLE ROCK', 'revenue': 58.25}, {'customer': 'HUNZICKER BROTHERS', 'revenue': 58.25}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 58.25}, {'customer': 'SOUTHEAST ELECTRIC & PLUMBING', 'revenue': 58.25}, {'customer': 'HENSONS CARPET ONE', 'revenue': 58.25}, {'customer': 'BEST LIGHTING AND ACCESSORIES', 'revenue': 58.25}, {'customer': 'LIGHTING CONCEPTS LLC', 'revenue': 58.25}, {'customer': 'DUNCAN LIGHTING & HOME-I', 'revenue': 58.25}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 58.25}, {'customer': 'IDAHO DREAMING', 'revenue': 58.25}, {'customer': 'LIGHT SYSTEMS INC', 'revenue': 58.25}, {'customer': 'HOBRECHT LIGHTING CO INC', 'revenue': 58.25}, {'customer': 'WOLFE LIGHTING & ACCENTS LLC', 'revenue': 58.25}, {'customer': 'ALL ABOUT LIGHTS', 'revenue': 58.25}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 58.25}, {'customer': 'WOLFF BROS. SUPPLY, INC', 'revenue': 58.25}, {'customer': 'SORLIEN ELECTRIC INC', 'revenue': 58.25}, {'customer': 'MID-SOUTH LIGHTING', 'revenue': 58.25}, {'customer': 'A & A LIGHTING, LLP', 'revenue': 58.25}, {'customer': 'ILLUMINATIONS OF THE TRIAD', 'revenue': 58.25}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 58.25}, {'customer': 'LIGHTING WORKS', 'revenue': 58.25}, {'customer': 'GRAND RAPIDS LIGHTING CTR INC', 'revenue': 58.25}, {'customer': 'HOME CENTER INC', 'revenue': 58.25}, {'customer': 'ROYAUME LUMINAIRE STE JULIE', 'revenue': 54.2}, {'customer': 'ROYAUME SOREL-TRACEY', 'revenue': 49.51}, {'customer': 'FURNITURE SHOWCASE', 'revenue': 0.0}] | [{'item': '50503-BNK-WG', 'desc': 'Bolden 3 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 1440}, {'item': '50502-FB', 'desc': 'Bolden 2 Light Vanity in Flat Black', 'available': 505}, {'item': '50504-BNK', 'desc': 'Bolden 4 Light Vanity in Brushed Polished Nickel', 'available': 490}, {'item': '50503-BNK', 'desc': 'Bolden 3 Light Vanity in Brushed Polished Nickel', 'available': 363}, {'item': '50503-SB', 'desc': 'Bolden 3 Light Vanity in Satin Brass', 'available': 323}, {'item': '50503-FB', 'desc': 'Bolden 3 Light Vanity in Flat Black', 'available': 302}, {'item': '50591-FB-WG', 'desc': 'Bolden 1 Light Mini Pendant in Flat Black (White Glass)', 'available': 261}, {'item': '50591-BNK', 'desc': 'Bolden 1 Light Mini Pendant in Brushed Polished Nickel', 'available': 232}, {'item': '50504-FB-WG', 'desc': 'Bolden 4 Light Vanity in Flat Black (White Glass)', 'available': 179}, {'item': '50503-FB-WG', 'desc': 'Bolden 3 Light Vanity in Flat Black (White Glass)', 'available': 178}, {'item': '50523-FB', 'desc': 'Bolden 3 Light Chandelier in Flat Black', 'available': 171}, {'item': '50502-FB-WG', 'desc': 'Bolden 2 Light Vanity in Flat Black (White Glass)', 'available': 157}, {'item': '50523-BNK', 'desc': 'Bolden 3 Light Chandelier in Brushed Polished Nickel', 'available': 147}, {'item': '50525-SB', 'desc': 'Bolden 5 Light Chandelier in Satin Brass', 'available': 142}, {'item': '50591-FB', 'desc': 'Bolden 1 Light Mini Pendant in Flat Black', 'available': 141}, {'item': '50524-SB', 'desc': 'Bolden 4 Light Chandelier in Satin Brass', 'available': 127}, {'item': '50525-BNK', 'desc': 'Bolden 5 Light Chandelier in Brushed Polished Nickel', 'available': 119}, {'item': '50523-BNK-WG', 'desc': 'Bolden 3 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 116}, {'item': '50552-FB', 'desc': 'Bolden 2 Light Convertible Semi Flush in Flat Black', 'available': 113}, {'item': '50525-FB', 'desc': 'Bolden 5 Light Chandelier in Flat Black', 'available': 112}, {'item': '50501-SB', 'desc': 'Bolden 1 Light Wall Sconce in Satin Brass', 'available': 108}, {'item': '50524-FB', 'desc': 'Bolden 4 Light Chandelier in Flat Black', 'available': 105}, {'item': '50552-FB-WG', 'desc': 'Bolden 2 Light Convertible Semi Flush in Flat Black (White Glass)', 'available': 103}, {'item': '50536-FB', 'desc': 'Bolden 6 Light Foyer in Flat Black', 'available': 98}, {'item': '50525-BNK-WG', 'desc': 'Bolden 5 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 90}, {'item': '50536-SB', 'desc': 'Bolden 6 Light Foyer in Satin Brass', 'available': 88}, {'item': '50591-SB', 'desc': 'Bolden 1 Light Mini Pendant in Satin Brass', 'available': 85}, {'item': '50502-SB', 'desc': 'Bolden 2 Light Vanity in Satin Brass', 'available': 81}, {'item': '50552-BNK-WG', 'desc': 'Bolden 2 Light Convertible Semi Flush in Brushed Polished Nickel (White Glass)', 'available': 80}, {'item': '50501-FB-WG', 'desc': 'Bolden 1 Light Vanity in Flat Black (White Glass)', 'available': 79}, {'item': '50552-BNK', 'desc': 'Bolden 2 Light Convertible Semi Flush in Brushed Polished Nickel', 'available': 76}, {'item': '50533-FB', 'desc': 'Bolden 3 Light Foyer in Flat Black', 'available': 75}, {'item': '50529-FB', 'desc': 'Bolden 9 Light Chandelier in Flat Black', 'available': 75}, {'item': '50536-BNK', 'desc': 'Bolden 6 Light Foyer in Brushed Polished Nickel', 'available': 65}, {'item': '50523-FB-WG', 'desc': 'Bolden 3 Light Chandelier in Flat Black (White Glass)', 'available': 60}, {'item': '50529-BNK', 'desc': 'Bolden 9 Light Chandelier in Brushed Polished Nickel', 'available': 59}, {'item': '50552-SB', 'desc': 'Bolden 2 Light Convertible Semiflush in Satin Brass', 'available': 51}, {'item': '50528-FB-WG', 'desc': 'Bolden 8 Light Chandelier in Flat Black (White Glass)', 'available': 51}, {'item': '50528-BNK-WG', 'desc': 'Bolden 8 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 50}, {'item': '50528-SB', 'desc': 'Bolden 8 Light Chandelier in Satin Brass', 'available': 50}, {'item': '50524-FB-WG', 'desc': 'Bolden 4 Light Chandelier in Flat Black (White Glass)', 'available': 48}, {'item': '50525-FB-WG', 'desc': 'Bolden 5 Light Chandelier in Flat Black (White Glass)', 'available': 45}, {'item': '50533-SB', 'desc': 'Bolden 3 Light Foyer in Satin Brass', 'available': 42}, {'item': '50502-BNK-WG', 'desc': 'Bolden 2 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 38}, {'item': '50533-BNK', 'desc': 'Bolden 3 Light Foyer in Brushed Polished Nickel', 'available': 34}, {'item': '50524-BNK', 'desc': 'Bolden 4 Light Chandelier in Brushed Polished Nickel', 'available': 28}, {'item': '50528-BNK', 'desc': 'Bolden 8 Light Chandelier in Brushed Polished Nickel', 'available': 26}, {'item': '50501-BNK', 'desc': 'Bolden 1 Light Vanity in Brushed Polished Nickel', 'available': 25}, {'item': '50529-BNK-WG', 'desc': 'Bolden 9 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 20}, {'item': '50504-BNK-WG', 'desc': 'Bolden 4 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 18}, {'item': '50591-BNK-WG', 'desc': 'Bolden 1 Light Mini Pendant in Brushed Polished Nickel (White Glass)', 'available': 17}, {'item': '50528-FB', 'desc': 'Bolden 8 Light Chandelier in Flat Black', 'available': 17}, {'item': '50523-SB', 'desc': 'Bolden 3 Light Chandelier in Satin Brass', 'available': 16}, {'item': '50529-SB', 'desc': 'Bolden 9 Light Chandelier in Satin Brass', 'available': 14}, {'item': '50502-BNK', 'desc': 'Bolden 2 Light Vanity in Brushed Polished Nickel', 'available': 12}, {'item': '50501-FB', 'desc': 'Bolden 1 Light Vanity in Flat Black', 'available': 11}, {'item': '50504-SB', 'desc': 'Bolden 4 Light Vanity in Satin Brass', 'available': 8}, {'item': '50529-FB-WG', 'desc': 'Bolden 9 Light Chandelier in Flat Black (White Glass)', 'available': 4}, {'item': '50501-BNK-WG', 'desc': 'Bolden 1 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 2}] |
| 19624BNK3 | Drake 3 Light Vanity in Brushed Polished Nickel | DRAKE | 174,442.62 | 3,817 | 2 | 2026-07-12 | [{'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 23098.7}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 19782.3}, {'customer': 'GREER LIGHTING CENTER LLC', 'revenue': 11565.6}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 9456.5}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 9183.54}, {'customer': 'HEARTH & HOME', 'revenue': 7068.0}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 5528.07}, {'customer': 'BAYSIDE ELECTRIC SUPPLY CO INC', 'revenue': 4702.1}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 4306.28}, {'customer': 'BEST LIGHTING AND ACCESSORIES', 'revenue': 4097.6}, {'customer': 'G & G ELECTRIC & PLUMBING', 'revenue': 3925.57}, {'customer': 'PREMIER LIGHTING LLC', 'revenue': 3911.93}, {'customer': 'HUNZICKER BROTHERS', 'revenue': 3269.0}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 3196.52}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3046.72}, {'customer': 'TRI SUPPLY', 'revenue': 2806.8}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 2745.84}, {'customer': 'METRO LIGHTING', 'revenue': 2519.4}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 2371.5}, {'customer': 'HALL ELECTRIC', 'revenue': 2079.5}, {'customer': 'PC HOME CENTER', 'revenue': 1614.99}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 1576.36}, {'customer': 'FERGUSONHOME.COM', 'revenue': 1451.27}, {'customer': 'ILLUMINATIONS INC', 'revenue': 1367.12}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 1208.09}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 1200.66}, {'customer': 'LUXUR LIGHTING', 'revenue': 1187.03}, {'customer': 'LIGHTING WORLD INC', 'revenue': 1162.5}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 1134.62}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 1121.6}, {'customer': 'BRANDON LIGHTING INC', 'revenue': 1117.89}, {'customer': 'WAYFAIR LLC-I', 'revenue': 955.19}, {'customer': 'LIGHTING ETC', 'revenue': 930.0}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 851.88}, {'customer': 'WOLFE LIGHTING & ACCENTS LLC', 'revenue': 837.0}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 795.18}, {'customer': 'CAPITAL CITY DESIGN CENTER', 'revenue': 697.5}, {'customer': 'ALL ABOUT LIGHTS', 'revenue': 687.62}, {'customer': '1STOPLIGHTING-I', 'revenue': 672.46}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 651.0}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 644.03}, {'customer': 'PASSION LIGHTING', 'revenue': 604.5}, {'customer': 'LIGHTING PLUS', 'revenue': 604.5}, {'customer': 'FIXTURE THIS INC', 'revenue': 604.5}, {'customer': 'CHADWELL SUPPLY INC', 'revenue': 528.0}, {'customer': 'GALLERY OF LTG', 'revenue': 517.1}, {'customer': 'STEINKAMP HOME CENTER', 'revenue': 511.5}, {'customer': 'HUMMELL BROTHERS ELEC SUPPLY', 'revenue': 471.0}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 465.0}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 457.15}, {'customer': 'DELMAR FANS', 'revenue': 428.4}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 421.3}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 418.5}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 418.5}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 418.5}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 416.21}, {'customer': 'TECHE ELECTRIC', 'revenue': 374.8}, {'customer': 'PREMIER INDUSTRIES INC', 'revenue': 372.0}, {'customer': 'RIMROCK LIGHTING', 'revenue': 367.5}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 348.75}, {'customer': 'COASTAL LIGHTING SUPPLY CO INC', 'revenue': 339.45}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 337.5}, {'customer': "HAGEN'S", 'revenue': 325.5}, {'customer': 'TIMELESS DESIGNS LP', 'revenue': 325.5}, {'customer': 'HOME LIGHTING & SUPPLY INC', 'revenue': 325.5}, {'customer': 'PARALLAX INDUSTRIES, INC.', 'revenue': 283.5}, {'customer': 'LIGHTING CONCEPTS LLC', 'revenue': 279.0}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 279.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 279.0}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 279.0}, {'customer': 'KLS,LLC dba SPECTRUM LIGHTING', 'revenue': 262.5}, {'customer': 'ROBINSON LIGHTING LTD', 'revenue': 236.25}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 232.5}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 232.5}, {'customer': None, 'revenue': 232.5}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 232.5}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 232.5}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 210.0}, {'customer': 'B & H ELECTRIC SUPPLY', 'revenue': 210.0}, {'customer': 'BRILLANT LIGHTING CENTER', 'revenue': 210.0}, {'customer': 'CITY LIGHTZ', 'revenue': 206.01}, {'customer': 'HERITAGE LIGHTING, LLC', 'revenue': 191.6}, {'customer': 'BRIGHT IDEAS LTG & MORE', 'revenue': 186.0}, {'customer': 'BENDER MANAGEMENT INC', 'revenue': 186.0}, {'customer': 'HOME LIGHTING', 'revenue': 186.0}, {'customer': 'SORLIEN ELECTRIC INC', 'revenue': 186.0}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 186.0}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 186.0}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 186.0}, {'customer': 'DUNCAN CORPORATION', 'revenue': 186.0}, {'customer': 'TKL SOLUTIONS INC', 'revenue': 179.03}, {'customer': 'LANTERN HOUSE INC', 'revenue': 162.75}, {'customer': 'FISHTRAP CREEK LIGHTING', 'revenue': 157.5}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 157.5}, {'customer': 'CAPITOL LIGHTING', 'revenue': 157.5}, {'customer': 'RADUE HOMES DBA INSPIRED SPACE', 'revenue': 157.5}, {'customer': 'VISIONS LTG & ACCESSORIES', 'revenue': 157.5}, {'customer': 'COCOON INTERIORS INC.', 'revenue': 157.5}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 145.5}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 142.3}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 141.76}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 141.75}, {'customer': 'MEDINA LIGHTING INC', 'revenue': 139.5}, {'customer': 'KAMLOOPS LAMPOST THE', 'revenue': 139.5}, {'customer': 'APPLICO APPLIANCE & LTG', 'revenue': 139.5}, {'customer': 'RAYMOND DESTEIGER INC', 'revenue': 139.5}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 139.5}, {'customer': 'LIGHTING INC.', 'revenue': 139.5}, {'customer': 'CHATELAINE LIGHTING SUPPLY LTD', 'revenue': 139.5}, {'customer': 'MOUNTAIN LIGHTING', 'revenue': 139.5}, {'customer': 'PINE STATE ELEC SUPPLY', 'revenue': 139.5}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 139.5}, {'customer': 'AT HOME, LLC DBA HOME LIGHTING', 'revenue': 139.5}, {'customer': 'LIGHTING EFX INC', 'revenue': 139.5}, {'customer': 'U.S. 31 SUPPLY INC', 'revenue': 132.53}, {'customer': 'HOUSE OF LIGHTS OF SANFORD INC', 'revenue': 129.75}, {'customer': 'BLACK DIAMOND ACQUISITIONS', 'revenue': 105.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 105.0}, {'customer': 'M.C.I. INC', 'revenue': 105.0}, {'customer': 'THE SALT BOX', 'revenue': 105.0}, {'customer': 'ROYAL ENTERPRISES', 'revenue': 105.0}, {'customer': 'BGZA INC', 'revenue': 105.0}, {'customer': 'LESSMAN ELECTRIC SUPPLY CO', 'revenue': 105.0}, {'customer': 'GARDEN OF THE GODS LIGHTING', 'revenue': 105.0}, {'customer': 'NORTHERN LGTS & FURNISHINGS', 'revenue': 105.0}, {'customer': 'HOUSE ACCOUNT', 'revenue': 97.7}, {'customer': 'LYONS ELECTRICAL', 'revenue': 95.8}, {'customer': 'FIRST SUPPLY LLC', 'revenue': 95.56}, {'customer': 'CMC SUPPLY, INC.', 'revenue': 93.0}, {'customer': 'HOME BUILDERS SUPPLY INC', 'revenue': 93.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 93.0}, {'customer': 'SUNDIAL LIGHTING LTD', 'revenue': 93.0}, {'customer': 'AMOS ELECTRIC SUPPLY COMPANY', 'revenue': 93.0}, {'customer': 'W T LIGHTING', 'revenue': 93.0}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 93.0}, {'customer': 'IDAHO DREAMING', 'revenue': 93.0}, {'customer': 'QUARLES SUPPLY CO INC', 'revenue': 93.0}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 93.0}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 86.49}, {'customer': 'PIONEER LIGHTING INC', 'revenue': 55.7}, {'customer': 'HOUSE OF LIGHTS OF CARY INC', 'revenue': 52.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 52.5}, {'customer': 'DISPLAY MERCHANDISE-10', 'revenue': 52.5}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 52.5}, {'customer': 'ELEMENTS OF DESIGN', 'revenue': 52.5}, {'customer': 'FLOOR BROKERS, THE', 'revenue': 52.5}, {'customer': "MAHLANDER'S", 'revenue': 52.5}, {'customer': 'PREMIER BATH, LTG & HDW LLC', 'revenue': 52.5}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 49.3}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 48.82}, {'customer': 'LIGHT HOUSE THE', 'revenue': 48.82}, {'customer': 'LIGHTING SHOPPE CHATHAM, LLC', 'revenue': 47.25}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 47.25}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 46.5}, {'customer': 'PARAMONT-EO INC', 'revenue': 46.5}, {'customer': 'BETTER HOMES SUPPLY', 'revenue': 46.5}, {'customer': 'STATEWIDE LIGHTING-RENO', 'revenue': 46.5}, {'customer': None, 'revenue': 46.5}, {'customer': 'ELECTRIC SUPPLY LIGHTING', 'revenue': 46.5}, {'customer': 'FANS & LIGHTING MINN. LLC', 'revenue': 46.5}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 46.5}, {'customer': 'STATE ELECTRIC SUPPLY CO', 'revenue': 46.5}, {'customer': 'LIGHTSHINE INC', 'revenue': 46.5}, {'customer': 'ONE SOURCE LIGHTING INC', 'revenue': 46.5}, {'customer': 'WOLBERG ELECTRIC SUPPLY CO', 'revenue': 46.5}, {'customer': 'COVERINGS LLC', 'revenue': 46.5}, {'customer': 'A & W LIGHTING', 'revenue': 46.5}, {'customer': 'HOUSE OF LIGHTS', 'revenue': 46.5}, {'customer': 'GROSS LIGHTING & HOME', 'revenue': 46.5}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 46.5}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 46.5}, {'customer': 'CR LIGHTING', 'revenue': 46.5}, {'customer': 'RE-LIGHTING', 'revenue': 46.5}, {'customer': 'WHOLESALE SUPPLY GROUP INC', 'revenue': 46.5}, {'customer': '43RD STREET LIGHTING', 'revenue': 46.5}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 46.5}, {'customer': 'PLYLER SUPPLY CO', 'revenue': 44.63}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 37.2}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 26.25}, {'customer': 'BULB BIN INC', 'revenue': 0.0}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 0.0}, {'customer': 'C.E.D.', 'revenue': 0.0}, {'customer': 'FURNITURE SHOWCASE', 'revenue': 0.0}, {'customer': 'J. H. LARSON COMPANY', 'revenue': 0.0}] | [{'item': '19616BNK2', 'desc': 'Drake 2 Light Vanity in Brushed Polished Nickel', 'available': 91}, {'item': '19606BNK1', 'desc': 'Drake 1 Light Wall Sconce in Brushed Polished Nickel', 'available': 78}, {'item': '19633FB4', 'desc': 'Drake 4 Light Vanity in Flat Black', 'available': 60}, {'item': '19606FB1', 'desc': 'Drake 1 Light Wall Sconce in Flat Black', 'available': 53}, {'item': '19633BNK4', 'desc': 'Drake 4 Light Vanity in Brushed Polished Nickel', 'available': 48}, {'item': '19624FB3', 'desc': 'Drake 3 Light Vanity in Flat Black', 'available': 46}, {'item': '19642FB5', 'desc': 'Drake 5 Light Vanity in Flat Black', 'available': 24}, {'item': '19642BNK5', 'desc': 'Drake 5 Light Vanity in Brushed Polished Nickel', 'available': 12}] |
| BSCB-B | Surface Mount Die-Cast Builder's Series LED Lighted Push Button in Matte Black | COL335 | 162,868.66 | 32,229 | 4,421 | 2026-09-20 | [{'customer': 'LIGHTING CONNECTION LLC', 'revenue': 34633.5}, {'customer': 'C.E.D.', 'revenue': 21288.7}, {'customer': 'STAR LIGHT DISTRIBUTION INC', 'revenue': 8690.4}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 8386.98}, {'customer': 'DELMAR FANS', 'revenue': 5430.85}, {'customer': 'CR LIGHTING', 'revenue': 4926.05}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3208.35}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 3155.59}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 3089.3}, {'customer': 'FERGUSONHOME.COM', 'revenue': 3030.5}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 2861.1}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 2739.05}, {'customer': 'LUMINAIRES PAUL GREGOIRE INC', 'revenue': 2668.8}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 2624.4}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 2426.7}, {'customer': 'R WILSON INC', 'revenue': 2118.2}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 2034.3}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 1806.73}, {'customer': 'DESIGNS BY ANN INC', 'revenue': 1637.4}, {'customer': 'ELLEN LIGHTING & HARDWARE', 'revenue': 1545.5}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 1504.75}, {'customer': "HAGEN'S", 'revenue': 1398.15}, {'customer': 'LIGHTING WORLD INC', 'revenue': 1364.75}, {'customer': 'HUNZICKER BROTHERS', 'revenue': 1300.5}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 1213.98}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 1160.8}, {'customer': 'ROYAUME LUMINAIRE LANDAUDIERE', 'revenue': 1108.5}, {'customer': 'KBL DESIGN CENTER', 'revenue': 938.25}, {'customer': 'LORD HENRY ENTERPRISES INC-I', 'revenue': 892.05}, {'customer': 'TEC OF NORTH LITTLE ROCK', 'revenue': 890.7}, {'customer': 'SHANOR ELECTRIC SUPPLY INC', 'revenue': 859.75}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 854.72}, {'customer': None, 'revenue': 845.79}, {'customer': 'OLYMPIA LIGHTING CENTER INC', 'revenue': 810.9}, {'customer': 'LUXUR LIGHTING', 'revenue': 742.8}, {'customer': 'METRO LIGHTING', 'revenue': 739.94}, {'customer': 'A & A LIGHTING, LLP', 'revenue': 719.55}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 708.25}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 694.3}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 690.8}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 653.9}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 630.9}, {'customer': 'LIGHTING INC.', 'revenue': 565.8}, {'customer': 'SONEPAR-USA', 'revenue': 560.6}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 560.05}, {'customer': 'HERITAGE LIGHTING, LLC', 'revenue': 558.0}, {'customer': 'HOME CENTER INC', 'revenue': 555.24}, {'customer': 'AMC LIGHTING & DECOR, INC.', 'revenue': 532.2}, {'customer': 'HENSONS CARPET ONE', 'revenue': 513.0}, {'customer': 'R.D.H.S.INC', 'revenue': 508.5}, {'customer': 'PINE GROVE ELEC SPLY', 'revenue': 494.05}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 471.3}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 462.25}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 430.05}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 412.86}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 402.85}, {'customer': 'PACE LIGHTING INC', 'revenue': 399.75}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 393.84}, {'customer': 'PARK LIGHTING', 'revenue': 379.53}, {'customer': 'ALL ABOUT LIGHTS', 'revenue': 373.2}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 364.0}, {'customer': 'DESIGN LIGHTING SALES LTD', 'revenue': 334.72}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 333.3}, {'customer': 'RITE RUG CO.', 'revenue': 330.7}, {'customer': 'SOUTHSIDE ELECTRIC', 'revenue': 321.1}, {'customer': 'DECO LUMINAIRE QUEBEC', 'revenue': 311.55}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 308.4}, {'customer': "GRAHAM'S LIGHTING INC", 'revenue': 306.4}, {'customer': 'T J S SUPPLY CO', 'revenue': 294.05}, {'customer': 'A & W LIGHTING', 'revenue': 291.6}, {'customer': 'MULTI LUMINAIRE ST. HUBERT', 'revenue': 291.6}, {'customer': 'BRANDON LIGHTING INC', 'revenue': 286.0}, {'customer': 'LITE HOUSE INC', 'revenue': 285.9}, {'customer': 'ROBINSON LIGHTING LTD', 'revenue': 272.21}, {'customer': 'BEAULIEU & LAMOUREUX INC', 'revenue': 270.9}, {'customer': 'CREATIVE LIGHTING, INC.', 'revenue': 264.0}, {'customer': 'GREER LIGHTING CENTER LLC', 'revenue': 257.2}, {'customer': 'LIGHTING GALLERY INC', 'revenue': 253.2}, {'customer': 'SUPER-LITE LIGHTING LTD-T', 'revenue': 251.7}, {'customer': 'CRESCENT LIGHTING SUPPLY INC', 'revenue': 240.9}, {'customer': 'CAJUN ELECTRIC, LLC', 'revenue': 236.6}, {'customer': 'DUNCAN CORPORATION', 'revenue': 227.75}, {'customer': 'GALLERY OF LTG', 'revenue': 218.1}, {'customer': 'IMAGINE MORE SERVICE CORP.', 'revenue': 206.15}, {'customer': 'SHOPFREELY.COM-I', 'revenue': 191.7}, {'customer': 'UNITED ELECTRIC SUPPLY', 'revenue': 181.9}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 178.8}, {'customer': 'GATEWAY LTG & DESIGN INC', 'revenue': 176.7}, {'customer': 'LIGHT CENTER, THE', 'revenue': 175.85}, {'customer': 'LOW COUNTRY LIGHTING INC', 'revenue': 170.0}, {'customer': 'ENCORE FLOORING & BLDG PROD', 'revenue': 165.3}, {'customer': 'THE LIGHTING GALLERY LLC', 'revenue': 159.64}, {'customer': 'LIGHTING GALLERY INC, THE', 'revenue': 154.8}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 149.4}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 145.8}, {'customer': 'RICHARDS LIGHTING', 'revenue': 144.95}, {'customer': 'AA PORTER', 'revenue': 140.9}, {'customer': 'HEARTH & HOME', 'revenue': 140.12}, {'customer': 'SHOWCASE LIGHTING BY 3-G LTD', 'revenue': 139.7}, {'customer': 'WISEWAY SUPPLY', 'revenue': 138.9}, {'customer': "LOWE'S CABINETS & LIGHTING GAL", 'revenue': 138.9}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 138.05}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 133.05}, {'customer': 'HALL ELECTRIC', 'revenue': 131.7}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 131.22}, {'customer': 'SCOTT ELECTRIC', 'revenue': 130.2}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 118.2}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 114.85}, {'customer': 'RACHELS LTG & HOME ACCESSORIES', 'revenue': 114.3}, {'customer': "EFIRD'S INTERIOR", 'revenue': 112.22}, {'customer': 'CROWN ELECTRIC SUPPLY CO', 'revenue': 109.15}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 107.4}, {'customer': 'LIGHTING SOLUTIONS DESIGN GALL', 'revenue': 105.9}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 102.85}, {'customer': 'LOGAN ELECTRIC COMPANY INC', 'revenue': 100.5}, {'customer': 'ECLAIRAGE MODERNE SARAN INC', 'revenue': 99.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 98.15}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 95.85}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 87.75}, {'customer': 'J & K ELECTRICAL SUPPLY CO INC', 'revenue': 87.04}, {'customer': 'CENTURY LIGHTING CENTER', 'revenue': 84.45}, {'customer': 'LESSMAN ELECTRIC SUPPLY CO', 'revenue': 79.8}, {'customer': None, 'revenue': 79.8}, {'customer': 'PINE TREE FURN & LIGHTING INC', 'revenue': 76.65}, {'customer': 'WILSON LIGHTING CO INC', 'revenue': 76.2}, {'customer': 'SHOALS LIGHTING', 'revenue': 76.2}, {'customer': '1STOPLIGHTING-I', 'revenue': 72.37}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 71.88}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 70.6}, {'customer': None, 'revenue': 69.85}, {'customer': 'LUMEN NATION LLC', 'revenue': 69.45}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 69.3}, {'customer': 'HUMMELL BROTHERS ELEC SUPPLY', 'revenue': 69.3}, {'customer': 'MAYER ELECTRIC SUPPLY CO INC', 'revenue': 68.75}, {'customer': 'COLEY ELECTRIC', 'revenue': 66.0}, {'customer': 'AIKEN ELECTRICAL  WHOLSALE INC', 'revenue': 66.0}, {'customer': 'CORNWALL LTG & ELEC CTR', 'revenue': 66.0}, {'customer': 'THE LIGHTING HUT INC', 'revenue': 66.0}, {'customer': 'BGZA INC', 'revenue': 59.6}, {'customer': 'ACCENT LIGHTING INC', 'revenue': 57.2}, {'customer': 'MCCAFFETY ELECTRIC CO INC', 'revenue': 55.25}, {'customer': 'BRUNEAU LUMINAIRE INC', 'revenue': 55.0}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 55.0}, {'customer': 'ROYAUME LUMINAIRE STE JULIE', 'revenue': 53.2}, {'customer': 'TRI SUPPLY', 'revenue': 52.55}, {'customer': 'PASSION LIGHTING', 'revenue': 52.05}, {'customer': 'SEQUEL ELECTRICAL SUPPLY, LLC', 'revenue': 52.0}, {'customer': 'LIGHTING PLUS', 'revenue': 52.0}, {'customer': 'BURGESS LIGHTING & DIST', 'revenue': 50.9}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 50.3}, {'customer': 'CMC SUPPLY, INC.', 'revenue': 49.7}, {'customer': 'TURN-ON LIGHTING', 'revenue': 48.8}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 46.55}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 44.0}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 41.95}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 41.6}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 41.6}, {'customer': 'LIGHTING ETC', 'revenue': 41.0}, {'customer': 'MURRAY SUPPLY/WHOLESALE ELEC', 'revenue': 39.9}, {'customer': 'COVENTRY LIGHTING INC', 'revenue': 39.9}, {'customer': 'LIGHTING CONCEPTS', 'revenue': 39.9}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 38.1}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 38.1}, {'customer': 'APPLICO APPLIANCE & LTG', 'revenue': 38.1}, {'customer': 'TIMELESS DESIGNS LP', 'revenue': 38.1}, {'customer': 'LIGHTING & REFLECTIONS', 'revenue': 38.1}, {'customer': 'ILLUMINATIONS OF THE TRIAD', 'revenue': 38.1}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 36.45}, {'customer': 'BRIGHT IDEAS LTG & MORE', 'revenue': 36.4}, {'customer': 'LUMINAIRE REPENTIGNY INC', 'revenue': 34.8}, {'customer': 'THOMSON PREMIER LTG', 'revenue': 33.9}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 33.25}, {'customer': 'BAYSIDE ELECTRIC SUPPLY CO INC', 'revenue': 33.25}, {'customer': 'CLASSIC LIGHTING & DESIGN INC', 'revenue': 33.0}, {'customer': 'RICHARDSON HOUSE OF FIXTURES', 'revenue': 33.0}, {'customer': 'DOMINION ELECTRIC SUPPLY CO', 'revenue': 33.0}, {'customer': 'HOUSE OF LIGHTS OF CARY INC', 'revenue': 32.1}, {'customer': "MIKE'S LIGHTING & ELECTRICAL", 'revenue': 31.75}, {'customer': 'LIGHT HOUSE', 'revenue': 31.2}, {'customer': 'LIGHT HOUSE OF SUMTER, LLC', 'revenue': 27.5}, {'customer': 'WILLIAM L HART DESIGNS LLC', 'revenue': 26.6}, {'customer': 'LIGHTSHINE INC', 'revenue': 26.6}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 26.6}, {'customer': 'UNIVERSITY LIGHTS-EJT', 'revenue': 26.6}, {'customer': 'TOPS ELECTRIC SUPPLY', 'revenue': 24.3}, {'customer': 'GORDON ELECTRIC SUPPLY', 'revenue': 22.0}, {'customer': 'LOFINGS LIGHTING', 'revenue': 22.0}, {'customer': 'FISHTRAP CREEK LIGHTING', 'revenue': 22.0}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 19.95}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 18.8}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 18.8}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 17.94}, {'customer': 'FARMVILLE WHOL ELEC SUPPLY CO', 'revenue': 16.75}, {'customer': 'DECORATIVE LIGHTING', 'revenue': 16.5}, {'customer': 'LIGHTS N SUCH INC', 'revenue': 16.5}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 13.3}, {'customer': 'DECO LUMINAIRE', 'revenue': 13.3}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 12.7}, {'customer': 'NACOGDOCHES HOME DESIGN CENTER', 'revenue': 12.7}, {'customer': 'LIGHTHOUSE DIST-DOORBELLSDIREC', 'revenue': 12.7}, {'customer': 'DUNCAN LIGHTING & HOME-I', 'revenue': 12.64}, {'customer': 'USESI', 'revenue': 12.15}, {'customer': 'JUST LIGHTS, INC.', 'revenue': 12.15}, {'customer': None, 'revenue': 11.0}, {'customer': 'LIGHT SYSTEMS INC', 'revenue': 11.0}, {'customer': 'TECHE ELECTRIC', 'revenue': 11.0}, {'customer': "JOSEPH'S ELECTRICAL CENTER", 'revenue': 11.0}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 10.4}, {'customer': 'THE BUILDING CENTER, INC.', 'revenue': 10.4}, {'customer': 'MADISON LIGHTING', 'revenue': 6.65}, {'customer': 'LIGHT WORKS OF STEAMBOAT', 'revenue': 6.65}, {'customer': 'CHRISTIES LTG GALLERY LLC', 'revenue': 6.65}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 6.65}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 6.65}, {'customer': 'TRINITY WHOLESALE DIST INC', 'revenue': 6.35}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 6.35}, {'customer': 'COASTAL LIGHTING, LLC', 'revenue': 6.35}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 6.35}, {'customer': 'ELECTRICAL & PLBG STORE', 'revenue': 6.32}, {'customer': 'LAMPS PLUS', 'revenue': 5.98}, {'customer': 'MILLIKEN HOME CENTER', 'revenue': 5.5}, {'customer': 'ELITEFIXTURES.COM-I', 'revenue': 5.5}, {'customer': 'LIGHTING SHOWCASE', 'revenue': 5.5}, {'customer': 'STEVENS LIGHTING FIXTURE CO', 'revenue': 5.5}, {'customer': 'THE PLUMBING WAREHOUSE', 'revenue': 5.5}, {'customer': 'HOBRECHT LIGHTING CO INC', 'revenue': 5.5}, {'customer': 'DECO LUMINAIRE-BROSSARD', 'revenue': 5.5}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 5.4}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 5.4}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 5.11}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 4.95}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 4.95}, {'customer': 'BLACK DIAMOND ACQUISITIONS', 'revenue': 0.0}, {'customer': 'Craftmade Warranty Account', 'revenue': 0.0}] | [{'item': 'BS6-W', 'desc': 'Surface Mount Rectangle Lighted Push Button in White', 'available': 145}] |
| Z402-TB | 2 Light Directional Bullet in Textured Black | CAST | 146,102.04 | 7,363 | 48 | 2026-09-25 | [{'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 23404.02}, {'customer': 'WAYFAIR LLC-I', 'revenue': 17110.4}, {'customer': 'FERGUSONHOME.COM', 'revenue': 16244.25}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 13228.5}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 12237.03}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 4445.46}, {'customer': 'METRO LIGHTING', 'revenue': 3371.01}, {'customer': 'CR LIGHTING', 'revenue': 3291.75}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3074.14}, {'customer': "HAGEN'S", 'revenue': 2752.75}, {'customer': 'DELMAR FANS', 'revenue': 2730.2}, {'customer': 'LIGHTING INC.', 'revenue': 1925.0}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 1815.63}, {'customer': 'BRAZORIA COUNTY LIGHTING', 'revenue': 1721.25}, {'customer': 'MARS ELECTRIC CO', 'revenue': 1673.75}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 1656.25}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 1564.99}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 1542.11}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 1501.5}, {'customer': 'AMERICAN LIGHTING', 'revenue': 1369.25}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 1289.75}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 1092.82}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 1078.0}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 1039.51}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 920.2}, {'customer': '1STOPLIGHTING-I', 'revenue': 828.45}, {'customer': 'LIGHTING EFX INC', 'revenue': 828.22}, {'customer': 'ROBINSON LIGHTING LTD', 'revenue': 765.2}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 755.03}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 698.0}, {'customer': 'NOVA LIGHTING', 'revenue': 672.3}, {'customer': 'MADISON LIGHTING', 'revenue': 658.75}, {'customer': 'THE PLUMBING WAREHOUSE', 'revenue': 654.5}, {'customer': 'THE SALT BOX', 'revenue': 636.0}, {'customer': 'LIGHTING ETC', 'revenue': 635.25}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 631.0}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 539.0}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 469.69}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 463.53}, {'customer': 'SOUTHSIDE LIGHTING GALLERY', 'revenue': 449.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 365.75}, {'customer': 'C.E.D.', 'revenue': 365.75}, {'customer': 'CRESCENT ELECTRIC SUPPLY CO', 'revenue': 361.25}, {'customer': 'SOUTHEAST ELECTRIC & PLUMBING', 'revenue': 336.9}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 326.08}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 309.25}, {'customer': None, 'revenue': 308.0}, {'customer': 'LIGHT CENTER, THE', 'revenue': 308.0}, {'customer': 'QUARLES SUPPLY CO INC', 'revenue': 299.33}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 288.75}, {'customer': 'LUXUR LIGHTING', 'revenue': 269.5}, {'customer': 'LIGHTING GALLERY', 'revenue': 255.0}, {'customer': 'M.C.I. INC', 'revenue': 255.0}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 252.16}, {'customer': 'LIGHTINGFRONT.COM-I', 'revenue': 233.75}, {'customer': 'GORDON ELECTRIC SUPPLY', 'revenue': 233.75}, {'customer': 'LIGHTING INC', 'revenue': 231.0}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 224.4}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 212.5}, {'customer': 'THE GALLERIES', 'revenue': 211.75}, {'customer': 'HENSONS CARPET ONE', 'revenue': 211.75}, {'customer': 'USESI', 'revenue': 192.5}, {'customer': 'DUNCAN CORPORATION', 'revenue': 192.5}, {'customer': 'DESIGNS BY ANN INC', 'revenue': 192.5}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 191.25}, {'customer': 'CAPITOL LIGHTING', 'revenue': 188.25}, {'customer': 'HAJOCA CORP', 'revenue': 170.0}, {'customer': 'TECHE ELECTRIC', 'revenue': 154.0}, {'customer': 'EDWARD JOY LIGHTING & ELEC SUP', 'revenue': 154.0}, {'customer': 'HALL ELECTRIC', 'revenue': 154.0}, {'customer': 'WOLFF BROS. SUPPLY, INC', 'revenue': 154.0}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 154.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 151.11}, {'customer': 'J. H. LARSON COMPANY', 'revenue': 148.75}, {'customer': 'FIVE OAK CONSTRUCTION', 'revenue': 148.75}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 148.0}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 138.34}, {'customer': 'CREATIVE LIGHTING', 'revenue': 134.75}, {'customer': 'KWK INVESTMENTS LLC', 'revenue': 134.75}, {'customer': 'WINSUPPLY INC', 'revenue': 134.75}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 133.91}, {'customer': 'THE LIGHTING GALLERY LLC', 'revenue': 129.83}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 129.75}, {'customer': 'FACILITY SOLUTIONS GROUP INC', 'revenue': 127.5}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 127.5}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 115.5}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 115.5}, {'customer': 'BRIDGE STREET ELECTRIC', 'revenue': 115.5}, {'customer': 'LITE HOUSE INC', 'revenue': 115.5}, {'customer': 'GOING DECOR', 'revenue': 106.25}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 99.0}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 96.25}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 96.25}, {'customer': 'PREMIER LIGHTING LLC', 'revenue': 96.25}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 96.25}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 96.25}, {'customer': 'LUMENAREA', 'revenue': 96.25}, {'customer': 'WOLBERG ELECTRIC SUPPLY CO', 'revenue': 96.25}, {'customer': 'FIXTURE THIS INC', 'revenue': 96.25}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 96.25}, {'customer': 'BGZA INC', 'revenue': 85.0}, {'customer': 'DOMINION ELECTRIC SUPPLY CO', 'revenue': 85.0}, {'customer': 'HEIGHTS LIGHTS & THINGS', 'revenue': 85.0}, {'customer': 'HAYNEEDLE,INC-I', 'revenue': 84.25}, {'customer': 'THE LAMP & LIGHTHOUSE', 'revenue': 83.5}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 78.25}, {'customer': 'LIGHTSHINE INC', 'revenue': 77.0}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 77.0}, {'customer': 'TRI SUPPLY', 'revenue': 77.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 77.0}, {'customer': 'LIGHT HOUSE', 'revenue': 77.0}, {'customer': 'VILLAGE LIGHTING & SUPPLY INC', 'revenue': 77.0}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 77.0}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 77.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 63.75}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 63.75}, {'customer': 'LOFINGS LIGHTING', 'revenue': 63.75}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 63.75}, {'customer': 'RIMROCK LIGHTING', 'revenue': 63.75}, {'customer': 'STEVENS LIGHTING FIXTURE CO', 'revenue': 63.75}, {'customer': 'BUILD IT FAB INC', 'revenue': 63.75}, {'customer': 'RITE RUG CO.', 'revenue': 63.75}, {'customer': 'LAMP SHOP/BRIGHT IDEAS, THE', 'revenue': 61.75}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 61.5}, {'customer': 'W T LIGHTING', 'revenue': 57.75}, {'customer': 'PRICE WHOLESALE LIGHTING', 'revenue': 57.75}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 57.75}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 57.75}, {'customer': 'MCMANUS LAMPLIGHTER', 'revenue': 57.75}, {'customer': 'THE BUILDING CENTER, INC.', 'revenue': 57.75}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 57.75}, {'customer': 'ILLUMINATIONS INC', 'revenue': 57.75}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 57.75}, {'customer': 'LUMEN NATION LLC', 'revenue': 42.5}, {'customer': 'LIGHTING PLUS INC', 'revenue': 42.5}, {'customer': 'CEILING FAN COMPANY INC', 'revenue': 42.5}, {'customer': 'KINGS WAGON YARD', 'revenue': 38.5}, {'customer': 'STEINKAMP HOME CENTER', 'revenue': 38.5}, {'customer': 'HEARTH & HOME', 'revenue': 38.5}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 38.5}, {'customer': 'Peak Lighting Bulbs & Ballast', 'revenue': 38.5}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 38.5}, {'customer': 'GALLERIA LIGHTING', 'revenue': 38.5}, {'customer': 'J & B SUPPLY INC', 'revenue': 38.5}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 38.5}, {'customer': 'COLEY ELECTRIC-WAYCROSS', 'revenue': 38.5}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 38.5}, {'customer': 'BIGGINS LIGHTING & ELECTRIC', 'revenue': 38.5}, {'customer': 'DUNAMIS INTERIORS INC-C', 'revenue': 21.25}, {'customer': 'SUN LIGHTING CO-TUCSON', 'revenue': 21.25}, {'customer': 'FAN DIEGO INC', 'revenue': 21.25}, {'customer': 'HARTVILLE HARDWARE', 'revenue': 21.25}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 21.25}, {'customer': 'CAROLINA LANTERNS & LIGHTING', 'revenue': 21.25}, {'customer': 'HOME CONCEPTS-I', 'revenue': 21.25}, {'customer': 'AMINIS HOME, RUG & GAME', 'revenue': 21.25}, {'customer': '43RD STREET LIGHTING', 'revenue': 20.5}, {'customer': 'HOME CENTER INC', 'revenue': 19.25}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 19.25}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 19.25}, {'customer': 'RADUE HOMES DBA INSPIRED SPACE', 'revenue': 19.25}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 19.25}, {'customer': 'DISPLAY MERCHANDISE-10', 'revenue': 19.25}, {'customer': 'ALL-LITE', 'revenue': 19.25}, {'customer': 'MOUNTAIN LIGHTING', 'revenue': 19.25}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 19.25}, {'customer': 'TURN-ON LIGHTING', 'revenue': 19.25}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 18.29}] | [{'item': 'Z103-TB', 'desc': "Contractor's 1 Light Small Outdoor Wall Mount in Textured Black", 'available': 442}, {'item': 'Z402-DTZ', 'desc': '2 Light Directional Bullet in Dark Textured Bronze', 'available': 365}, {'item': 'Z402-TW', 'desc': '2 Light Directional Bullet in Textured White', 'available': 275}, {'item': 'Z433-TB', 'desc': 'Bent Glass 3 Light Flushmount in Textured Black', 'available': 241}] |
| PH-2BZ | 2 Light PAR Holder in Bronze | COL346 | 132,166.63 | 17,134 | 68 | — | [{'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 25128.12}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 22121.7}, {'customer': 'SCARBORO LIGHTING', 'revenue': 11531.35}, {'customer': "HAGEN'S", 'revenue': 7663.2}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 6020.7}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 5404.8}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 4633.2}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 4424.8}, {'customer': 'ENTERPRISE WHOLESALE INC', 'revenue': 3607.2}, {'customer': 'R.D.H.S.INC', 'revenue': 2876.35}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 2454.9}, {'customer': 'GORMAN BROS', 'revenue': 2416.8}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 2364.0}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 2233.25}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 2204.4}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 1845.35}, {'customer': 'CLARKSVILLE LIGHTING', 'revenue': 1803.6}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 1665.03}, {'customer': 'ROYAL ENTERPRISES', 'revenue': 1618.75}, {'customer': 'APPLICO APPLIANCE & LTG', 'revenue': 1603.2}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 1402.8}, {'customer': 'THE LIGHTING GALLERY LLC', 'revenue': 1291.4}, {'customer': 'WOLFE LIGHTING & ACCENTS LLC', 'revenue': 1235.0}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 1227.6}, {'customer': 'LANTERN HOUSE INC', 'revenue': 1202.4}, {'customer': 'HAMBUCHEN LIGHTING CO', 'revenue': 840.0}, {'customer': 'FIXTURE THIS INC', 'revenue': 813.6}, {'customer': 'C.E.D.', 'revenue': 729.6}, {'customer': 'HALL ELECTRIC', 'revenue': 717.6}, {'customer': 'AMOS ELECTRIC SUPPLY COMPANY', 'revenue': 626.25}, {'customer': 'BRIGHT IDEAS LTG & MORE', 'revenue': 518.4}, {'customer': 'KWK INVESTMENTS LLC', 'revenue': 501.0}, {'customer': 'IBS LIGHTING LTD.', 'revenue': 501.0}, {'customer': 'TRI SUPPLY', 'revenue': 444.55}, {'customer': 'COASTAL LIGHTING, LLC', 'revenue': 430.86}, {'customer': 'FERGUSONHOME.COM', 'revenue': 428.79}, {'customer': 'TRINITY WHOLESALE DIST INC', 'revenue': 425.85}, {'customer': 'LIGHTING INC.', 'revenue': 416.7}, {'customer': 'LIGHTING CONCEPTS LLC', 'revenue': 400.8}, {'customer': 'AMERICAN LIGHTING', 'revenue': 308.95}, {'customer': 'LIGHTS OF OCONEE LLC', 'revenue': 275.55}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 233.8}, {'customer': 'LIGHTING ETC', 'revenue': 233.8}, {'customer': 'HOUSE OF LIGHTS OF CARY INC', 'revenue': 227.5}, {'customer': 'PRICE WHOLESALE LIGHTING', 'revenue': 212.4}, {'customer': 'FACTORY LIGHTING OUTLET INC', 'revenue': 212.1}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 210.0}, {'customer': 'LIGHT SYSTEMS INC', 'revenue': 199.95}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 189.12}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 188.4}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 184.7}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 168.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 167.0}, {'customer': 'CUSTOM LIGHTING INC', 'revenue': 135.2}, {'customer': 'BRAZORIA COUNTY LIGHTING', 'revenue': 131.25}, {'customer': 'BULB BIN INC', 'revenue': 116.9}, {'customer': 'HEIGHTS LIGHTS & THINGS', 'revenue': 105.0}, {'customer': 'J & B SUPPLY INC', 'revenue': 100.2}, {'customer': 'SEQUEL ELECTRICAL SUPPLY, LLC', 'revenue': 100.2}, {'customer': 'TLC LIGHTING ON, LLC', 'revenue': 100.2}, {'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 83.5}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 61.6}, {'customer': 'HAYNEEDLE,INC-I', 'revenue': 53.05}, {'customer': 'WAYFAIR LLC-I', 'revenue': 51.56}, {'customer': '1STOPLIGHTING-I', 'revenue': 47.61}, {'customer': 'KINGS WAGON YARD', 'revenue': 41.75}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 33.4}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 25.05}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 25.05}, {'customer': 'METRO LIGHTING', 'revenue': 25.05}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 16.7}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 16.7}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 15.75}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 15.2}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 15.2}, {'customer': 'KEITH EICHENBLATT', 'revenue': 14.0}, {'customer': 'FELT LIGHTING CO', 'revenue': 8.75}, {'customer': 'RITE RUG CO.', 'revenue': 8.75}, {'customer': 'FURNITURE SHOWCASE', 'revenue': 8.75}, {'customer': 'Peak Lighting Bulbs & Ballast', 'revenue': 8.35}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 8.14}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 7.6}] | — |

### Q-ORG-NEWITEM_results.md

# Q-ORG-NEWITEM Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-NEWITEM — New Item Adoption Gap Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | customers_purchased | total_revenue | should_buy_customers |
| --- | --- | --- | --- | --- | --- |
| 61925-FB | Astor 5 Light Chandelier in Flat Black | ASTOR | 0 | 0 | — |
| 61925-SB | Astor 5 Light Chandelier in Premium Bronze | ASTOR | 0 | 0 | — |
| 61926-FB | Astor 6 Light Chandelier in Flat Black | ASTOR | 0 | 0 | — |
| 61926-SB | Astor 6 Light Chandelier in Premium Bronze | ASTOR | 0 | 0 | — |
| 61929-FB | Astor 9 Light Chandelier in Flat Black | ASTOR | 0 | 0 | — |
| 61929-SB | Astor 9 Light Chandelier in Premium Bronze | ASTOR | 0 | 0 | — |
| 61961-FB | Astor 1 Light Wall Sconce in Flat Black | ASTOR | 0 | 0 | — |
| 61961-SB | Astor 1 Light Wall Sconce in Premium Bronze | ASTOR | 0 | 0 | — |
| 62096-FB | Banks 6 Light 24.5" Pendant in Flat Black | BANKS | 0 | 0 | — |
| 62096-SB | Banks 6 Light 24.5" Pendant in Satin Brass | BANKS | 0 | 0 | — |
| 62098-FB | Banks 8 Light 32.5" Pendant in Flat Black | BANKS | 0 | 0 | — |
| 62098-SB | Banks 8 Light 32.5" Pendant in Satin Brass | BANKS | 0 | 0 | — |
| 60924-FBSB | Blake 4 Light Chandelier in Flat Black/Satin Brass | BLAKE | 0 | 0 | — |
| 60926-FBSB | Blake 6 Light Chandelier in Flat Black/Satin Brass | BLAKE | 0 | 0 | — |
| 60961-FBSB | Blake 1 Light Wall Sconce in Flat Black/Satin Brass | BLAKE | 0 | 0 | — |
| 60991-FBSB | Blake 1 Light Pendant in Flat Black/Satin Brass | BLAKE | 0 | 0 | — |
| Z402-DTZ | 2 Light Directional Bullet in Dark Textured Bronze | CAST | 0 | 0 | [{'customer_code': '6050', 'customer_name': "LOWE'S CO.- SOS CRAFTMADE", 'collection_revenue': 44227.75}, {'customer_code': '10106', 'customer_name': 'LIFESTYLES  STORES INC', 'collection_revenue': 41088.55}, {'customer_code': '3919', 'customer_name': 'WAYFAIR LLC-I', 'collection_revenue': 38710.28}, {'customer_code': '9802', 'customer_name': 'FERGUSONHOME.COM', 'collection_revenue': 26951.72}, {'customer_code': '9800', 'customer_name': 'FERGUSON ENTERPRISES INC', 'collection_revenue': 20110.79}, {'customer_code': '40100', 'customer_name': 'DEMENT LIGHTING INC', 'collection_revenue': 14845.5}, {'customer_code': '50200', 'customer_name': "GRAHAM'S LIGHTING FIXTURES INC", 'collection_revenue': 13283.5}, {'customer_code': '18031', 'customer_name': 'T J S SUPPLY CO', 'collection_revenue': 10045.5}] |
| CHM52W3 | Charming 52" 3-Blade Ceiling Fan in White w/ White Blades; Light Kit Sold Separately | COL10 | 0 | 0 | — |
| 62301-CPZ | Pleated II 1 Light Wall Sconce in Premium Bronze (Cased White Glass) | COL100 | 0 | 0 | — |
| 62301-FB | Pleated II 1 Light Wall Sconce in Flat Black (Cased White Glass) | COL100 | 0 | 0 | — |
| 62302-CPZ | Pleated II 2 Light Vanity in Premium Bronze (Cased White Glass) | COL100 | 0 | 0 | — |
| 62302-FB | Pleated II 2 Light Vanity in Flat Black (Cased White Glass) | COL100 | 0 | 0 | — |
| 62303-CPZ | Pleated II 3 Light Vanity in Premium Bronze (Cased White Glass) | COL100 | 0 | 0 | — |
| 62303-FB | Pleated II 3 Light Vanity in Flat Black (Cased White Glass) | COL100 | 0 | 0 | — |
| 62304-CPZ | Pleated II 4 Light Vanity in Premium Bronze (Cased White Glass) | COL100 | 0 | 0 | — |

*(Truncated: showing top 25 of 30 rows. Full data in cache file.)*
