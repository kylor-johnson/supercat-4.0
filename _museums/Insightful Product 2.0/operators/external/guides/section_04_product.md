# Section Guide: §4 — Product & Inventory Intelligence
> **v2.0** — hardened 2026-06-16 (CCI v3 run). Last updated: 2026-06-16.

## Section Identity
- **id**: `product`
- **title**: Product & Inventory Intelligence
- **section number**: 4
- **include when**: `HAS_INVENTORY = true` OR `HAS_SALES_DATA = true`
- **skip when**: Neither `HAS_INVENTORY` nor `HAS_SALES_DATA` is true — omit silently, no note in delivered report

## Query Inputs

Read these cache files:
- `cache/Q-07_results.md` — Catalog completeness
- `cache/Q-37_results.md` — Top sellers currently out of stock
- `cache/Q-38a_results.md` — Product velocity trend
- `cache/Q-39_results.md` — Line analysis by category & collection
- `cache/Q-42_results.md` — New introduction performance (**also provides total new-item count** consumed by subsection 6)
- `cache/Q-59_results.md` — Fill rate & backorder revenue impact (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains data rows, subsection 1b MUST be rendered)
- `cache/Q-61_results.md` — New introduction adoption gap — **returns ONLY items with ≥1 buyer** (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND this file contains data rows, subsection 6 MUST be rendered)
- `cache/gate_flags.md` — for `HAS_SALES_DATA`, `HAS_INVENTORY`, `HAS_CART`, `HAS_PORTAL_ORDERS`, `HAS_NEW_ITEMS`
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_4` tier

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Top Sellers OOS (Q-37)

**Gate**: `HAS_SALES_DATA = true` AND `HAS_INVENTORY = true` (both required)

Build from `Q-37_results.md`. Surface top-selling products that are currently out of stock.

Render a table with columns: Item (description with item code), Category, All-Time Sales, Next Receipt. Show top 5 visible; remaining in collapsed `<details>`.

**`what-this-means` close**: Frame around revenue protection. These are proven sellers sitting at zero inventory — quantify the cumulative sales history of the top items shown. Call out any item with no scheduled receipt date as the highest-risk gap. Tone: "Your best-sellers are generating demand you can't fill right now. The [item with no receipt date] has no restock scheduled — that's the most urgent gap."

### 1b. Fill Rate & Revenue Impact (Q-59)

**MANDATORY RENDER**: If `cache/Q-59_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-59_results.md`

**Rendering**:

**Part A — Org Fill Rate (from the `ORG_SUMMARY` row):**

Render a `.metrics-grid` with 2–3 metric cards:
- **Fill Rate**: `fill_rate_pct` displayed as `XX.X%` with `.metric-note` contextualizing (e.g., `.ok` if ≥95%, `.warn` if 85–94.9%, `.danger` if <85%)
- **Units Unfilled**: `total_unfilled` with label "Units not shipped (trailing 12 months)"

If fill rate < 85%, add a `.callout.alert` titled "Fulfillment Below Target" noting the gap vs. the 95% benchmark and connecting to customer retention risk.

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

After the table, render a `.callout.alert` with title "Revenue at Risk from Fulfillment Gaps":
- Sum the `annual_revenue` column for the top 5 items: "These 5 items represent $X in annualized revenue across Y customers. Persistent backorders correlate with longer reorder intervals — addressing these stockouts could protect an estimated $Z in annual business."
- Tag the projected figure with hedging language ("estimated," "could," "projected").

**`what-this-means` close**: Translate fill rate into plain language — "An X% fill rate means roughly 1 in Y ordered units is not being shipped." Connect to customer experience: persistent stockouts train buyers to look elsewhere. Tone: a supply-chain analyst explaining the cost of gaps to a VP of Sales.

**Claim rules**: "Your order fulfillment rate is X%." Use "fulfillment rate" or "fill rate" interchangeably. The causal link between backorders and reorder decay is always hedged. Never claim "you are losing $X" — say "projected at-risk revenue is estimated at $X if backorder patterns persist." Never use "ERP" or "portal_order_items." Reference items by description, not bare item numbers.

### 2. New Introduction Performance (Q-42)

**Gate**: `HAS_SALES_DATA = true`

Build from `Q-42_results.md`. Surface performance of newly introduced products.

**Narrative role**: This subsection opens the new-introduction story arc. It answers "how many new items did you launch, and what revenue have they generated?" When subsection 6 (Q-61) also renders, these two subsections form a deliberate arc: **launch count → total revenue → adoption rate → traction gap → action**. Subsection 2 sets the stage; subsection 6 delivers the payoff.

Render a `.metrics-grid` with:
- **New Items**: total count of new introductions (this count is also used by subsection 6 to derive adoption rate)
- **Revenue Generated**: total revenue from new items (with time qualifier, e.g., "all-time" or "trailing 12 months")

Follow with a brief prose note identifying any notable collection or category trends among new items. If any collection has multiple new items with zero sales, flag it as warranting attention.

**`what-this-means` close**: When subsection 6 will also render (both Q-61 gates met), tee up the adoption question: "You launched X new items generating $Y. The next question is how broadly your accounts have adopted them — see below." When subsection 6 is NOT rendered (gate not met), make the close self-contained: focus on revenue per new item, which collections are gaining traction, and whether launch velocity meets expectations.

### 3. Product Velocity Trend (Q-38a)

**Gate**: `portal_order_items` confirmed present (check `gate_flags.md` — `HAS_PORTAL_ORDERS = true` is the proxy)

Build from `Q-38a_results.md`. Exclude fee items, freight charges, and non-product line items from the analysis (Stage 1 filters by matching to `products` table on `ecat_item_number`).

Render as a table with these exact columns:

| Column | Content |
|--------|---------|
| Direction | ▲ accelerating / ▼ declining |
| Item Code | Product item code |
| Category | From products table if available |
| Recent 90d | Order count or unit count for the recent 90-day window |
| Prior 90d | Order count or unit count for the prior 90-day window |
| Velocity Change | Percentage with Accelerating/Declining badge |

Show the top 3–5 accelerating and top 3–5 declining items by absolute velocity change. Follow with a prose note: accelerating items should be flagged for inventory replenishment before stockout; declining items may warrant clearance pricing or repositioning.

**Omission rule**: If after filtering fee items fewer than 3 real products remain with meaningful velocity data, omit this subsection silently.

**`what-this-means` close**: Frame as an early-warning system. Accelerating items need inventory protection now to avoid stockouts during the demand ramp; declining items need intervention before they become dead stock. Tone: "Velocity is the leading indicator — these trends tell you where to place your next inventory bet and where to cut losses early."

### 4. Catalog Completeness (Q-07)

**Gate**: Always (all accounts with a product catalog)

Build from `Q-07_results.md`. Render as a table with these exact columns:

| Column | Content |
|--------|---------|
| Visibility | Visible / Hidden |
| Products | Count of products |
| Missing Images | Count missing images |
| Missing Price | Count missing price |
| Complete % | Percentage of products that are complete |

Include a callout if completeness is below 90% or if more than 50 items need assets.

**Cross-reference to §8**: For operational catalog completeness recommendations (upload images, refresh pricing, close configuration gaps), reference the Platform section: "See §8 Platform Health Check for specific catalog remediation actions." Do NOT include operational "upload X images" or "refresh Y price levels" recommendations in this subsection — those belong in §8, which owns the operational catalog completeness recommendation.

**`what-this-means` close**: Connect catalog completeness to **sales performance impact** — incomplete products are products reps can't confidently show or sell. Quantify: "X visible items are missing images or pricing, which means reps may skip them in presentations — that's potential revenue left on the table from products your team can't effectively sell." If completeness is high (>95%), acknowledge it positively and note the sales enablement advantage. Tone: sales-impact framing, not operational checklist.

### 5. What's Selling (Q-39)

**Gate**: `HAS_SALES_DATA = true`

Build from `Q-39_results.md` (which may produce separate category and collection result files). Render as a **single subsection** titled "What's Selling" — do not split into separate subsections for category and collection.

Inside this one subsection, render two progressive-disclosure tables:

**(a) Category breakdown** with columns:
- Category
- Qty Sold
- Sales
- Items
- Sales/Item

**(b) Collection breakdown** (in collapsed `<details>`) with columns:
- Collection
- Items
- Qty Sold
- Sales

Lead with a `.callout.insight` identifying the dominant category by sales share and any collections with outsized per-item performance.

**`what-this-means` close**: Identify concentration risk and whitespace opportunity. Name the dominant category and its share of total sales. Highlight any collection with high per-item revenue as evidence of rep confidence and market fit. Flag categories with low sales per item as needing merchandising support or rep training. Tone: a portfolio manager identifying where to double down and where to investigate.

### 6. New Introduction Adoption Gap (Q-61 + Q-42)

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND `cache/Q-61_results.md` has data rows.

**Data sources**:
- `cache/Q-61_results.md` — contains **ONLY items with ≥1 buyer** (the adopted items)
- `cache/Q-42_results.md` — provides the **total new-item count** (needed to calculate adoption rate and zero-traction count)

**Narrative role**: This is the payoff of the story arc opened in subsection 2 (Q-42). Subsection 2 says "you launched X items generating $Y." This subsection answers "how many actually gained traction, and what does the gap look like?"

**Deriving key metrics** (critical — Q-61 returns only adopted items, so totals must be cross-referenced):
- `total_new_items` = total new item count from Q-42 (e.g., 369)
- `adopted_items` = row count of Q-61 (e.g., 30)
- `adoption_rate` = `adopted_items / total_new_items` as percentage (e.g., 8%)
- `zero_traction_count` = `total_new_items - adopted_items` (e.g., 339)
- `adopted_revenue` = sum of `revenue` column in Q-61

**Rendering**:

Open with a `.callout.insight` titled "New Introduction Adoption" summarizing all five derived metrics in a single narrative sentence:

Example: "You launched 369 new items. 30 have been ordered by at least one account (8% adoption), generating $911K in trailing-12-month revenue. 339 items have zero traction."

Then render:

**(a) Top Performers** — from Q-61 rows, sorted by revenue descending (show top 5–8 visible; remaining in collapsed `<details>`):

| Column | Content |
|--------|---------|
| Item | `description` (fall back to `item_number` only if description is blank — never expose raw item codes as the primary identifier) |
| Category | `category` |
| Buyers | `buyers` |
| Qty Sold | `qty_ordered` |
| Revenue | `revenue` formatted as currency |
| List Price | `list_price` formatted as currency |

**(b) Zero-Traction Callout** — Q-61 returns only adopted items, so individual zero-traction items are **not available** in the data. Render a `.callout.warn` (NOT a table) with:
- Title: "Zero-Traction New Items"
- Body: "`zero_traction_count` new items have zero orders in the trailing 12 months. These may need rep attention, merchandising updates, or pricing review. High-list-price items with no traction represent the largest opportunity cost."

**IMPORTANT**: Do NOT render an empty zero-traction `<table>` with an empty `<tbody>`. The count-based callout is the correct treatment when individual zero-traction rows are not in the query results. An empty table is a rendering defect.

**`what-this-means` close**: Frame as a launch effectiveness diagnostic. An adoption rate below ~25% means most new introductions haven't reached a single buyer — the gap is likely in awareness and rep activation, not product quality. Connect to actionable next steps: rep training on new items, featured placement in SmartLists, targeted merchandising. When adoption rate is healthy (>40%), acknowledge it and focus the close on scaling the top performers.

Example tone: "An 8% adoption rate means 339 new items haven't reached a single buyer yet. The top performers prove the line has appeal — the gap is in awareness and rep activation. Focused training on new introductions and featured placement in rep-facing lists can close this gap."

**Claim rules**: "You launched X new items. Y have been purchased by at least one account." Never expose item_number if it contains internal codes — use description. Frame zero-traction items as opportunity, not failure: "may need attention" not "are failing." Never use "ERP."

## Empty-Section Guard

After evaluating individual subsection gates, if zero subsections qualify for rendering, omit §4 entirely — do not render a section header or collapsible card with no content. The section-level gate (`HAS_INVENTORY = true` OR `HAS_SALES_DATA = true`) is a pre-filter; the final inclusion decision requires at least one subsection to be buildable from query results.

## Section-Specific Rules

- **VM-38b is `pending_engineering`** — do not attempt to run. Do not fabricate product velocity data from `sales_data` without an `invoice_date`.

## Data Confidence Footer

**You MUST render this footer.** Follow the numbered steps below exactly. Do NOT skip or reorder them.

**STEP 1 — Read the tier (MANDATORY).** Open `cache/section_confidence.md` and read the EXACT value of `SECTION_CONFIDENCE_4`. It is one of: `FULL`, `STRONG`, `PARTIAL`, `LIMITED`. **Use THIS value. Do NOT infer or recompute the tier from gate flags — the data gathering script already computed it.**

**STEP 2 — Select the template** matching the tier from STEP 1:

| STEP 1 value | Template | Label |
|---|---|---|
| `FULL` | `§4-FULL` | `FULL PICTURE` |
| `STRONG` | `§4-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§4-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§4-STRONG` (with `.limited` class) | `LIMITED VIEW` |

Resolve template variables: `{{PRODUCT_COUNT}}` from `gate_flags.md` (omit parenthetical if unavailable). For STRONG: resolve `{{SOURCES_PRESENT}}`, `{{STALE_SOURCE}}`, `{{STALE_DATE}}` from Q-08. If STRONG variables can't be resolved, fall back to `§4-PARTIAL`.

**STEP 3 — Position the footer:**
- If STEP 1 value is **FULL** → place the footer as the **last element** in the section fragment, after all subsection content.
- If STEP 1 value is **STRONG / PARTIAL / LIMITED** → place the footer **immediately after the key metrics row**, before the first subsection.

**STEP 4 — Build the HTML:**

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

If STEP 1 value is `LIMITED`, use `<div class="data-confidence limited">` instead. For LIMITED, use the:

```html
<div class="data-confidence limited">
  <span class="data-confidence-label">LIMITED VIEW</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Customer-level activation, penetration, or dormancy analysis → belongs in §3 Customer & Buyer Intelligence
2. Rep-level performance, coaching, or behavioral analysis → belongs in §2 Sales Team Performance
3. Order trends, channel mix, or capture rate → belongs in §5 Commerce Analytics
4. Portal traffic, Clicky analytics, or geographic demand → belongs in §6 Demand Signal Intelligence
5. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
6. Platform feature utilization or data freshness → belongs in §8 Platform & Feature
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Conditional Subsection Checklist (verify before saving fragment)

Before writing `fragments/section_04.html`, confirm every item:

| # | Subsection | Gate | Verify |
|---|-----------|------|--------|
| 1 | Top Sellers OOS (Q-37) | `HAS_SALES_DATA` AND `HAS_INVENTORY` both true | rendered / correctly skipped |
| 1b | Fill Rate & Revenue Impact (Q-59) | `HAS_PORTAL_ORDERS = true` + Q-59 has data rows | rendered / correctly skipped |
| 2 | New Introduction Performance (Q-42) | `HAS_SALES_DATA = true` | rendered / correctly skipped |
| 3 | Product Velocity Trend (Q-38a) | `HAS_PORTAL_ORDERS = true` + ≥3 real products with velocity data | rendered / correctly skipped |
| 4 | Catalog Completeness (Q-07) | Always | rendered |
| 5 | What's Selling (Q-39) | `HAS_SALES_DATA = true` | rendered / correctly skipped |
| 6 | New Introduction Adoption Gap (Q-61) | `HAS_PORTAL_ORDERS` AND `HAS_NEW_ITEMS` both true + Q-61 has data rows | rendered / correctly skipped |

**Structural checks (also verify before saving):**

| Check | Rule | Pass? |
|-------|------|-------|
| `what-this-means` count | Equals rendered subsection count | ☐ |
| Zero-traction rendering | Q-61 uses `.callout.warn` count — no empty `<table><tbody></tbody></table>` | ☐ |
| Q-42 → Q-61 narrative arc | Subsection 2 tees up subsection 6 when both render | ☐ |
| Forbidden phrases | No "ERP," no raw item codes as primary identifiers, no "Mixpanel," no segment labels | ☐ |
| Confidence footer | Present, matches `SECTION_CONFIDENCE_4` tier, template variables resolved | ☐ |
| Adoption metrics | `total_new_items` from Q-42, `adopted_items` from Q-61 row count, math correct | ☐ |
