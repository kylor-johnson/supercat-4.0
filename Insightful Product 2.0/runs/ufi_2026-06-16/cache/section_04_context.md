# Section 4 Context Bundle — Universal Furniture (ufi)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=60988, portal_order_gmv=$137.9M |
| HAS_INVENTORY | True | inventory_count=2148 |
| HAS_SALES_DATA | True | sales_data_count=104838 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | ufi_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$137.9M > ecat_gmv=$13.4M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 103 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 2131, Mixpanel total submit_order (Q-01): 3593 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=82.5%, ambiguous_rate=15.3%, showroom_event_share=14.7% |
| USER_GROUP_JOIN_RATE | 83% | 85 of 103 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 15% | showroom+admin share of matched events: 14.7% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=4382 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | True | commitment_reports_count=4255 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Universal Furniture
- **Shortname**: ufi
- **Org ID**: 18
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16

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

## Section Guide — section_04_product.md

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

## Shared Rules

# Shared Rules — All Section Agents
> **v1.1** — updated 2026-06-16. Scoped forbidden-phrase canonical claim, confidence footer scope.

> **Note:** This file is a runtime guide consumed by section-building agents. The
> canonical rule definitions live in [`GUARDRAILS.md`](../../../GUARDRAILS.md). If
> this file and `GUARDRAILS.md` conflict, `GUARDRAILS.md` wins.

## A. Semantic Guardrails

| Term | Correct Meaning | Never Use For |
|------|----------------|--------------|
| `orders` | eCat-originated orders only | ERP or total-business data |
| `order_source = 'ipad'` | Rep-submitted iPad orders | Online or self-service orders |
| `order_source = 'server'` | eCat Online / B2B Cart buyer self-service | Rep orders |
| `portal_orders` | ERP-synced all-channel total business | Buyer activity, "portal ordering," self-service |
| `Sales Portal` | Internal BI dashboard for client team | A buyer-facing ordering channel |
| `self-service` | B2B Cart / eCat Online only | Sales Portal, portal_orders |
| Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | Internal classification only — never in external output | Every section including Peer Benchmarking — in §7, use plain-language cohort framing derived from `peer_group_id_effective` |
| Health score | Never in Phase 1 external report | Any external output |
| `benchmark_confidence` | Internal rendering signal only — governs section inclusion and phrasing | Never as a visible label in client output |
| `peer_group_level` | Internal gating signal only | Never in client output (not even paraphrased as "tier 1/2/3") |
| `peer_group_n` | Internal calibration signal — governs framing strength | Never as a raw count in client-facing output. Use to calibrate plain-language phrasing only. |

## B. Hard Rules

Invariant. No exception, no workaround, no soft reference:

1. Never surface health score, health band, or health classification in any external output
2. Never surface VM-27, VM-28, VM-29, VM-36, VM-48 content externally
3. If `has_clicky = false`, the Demand Signal Intelligence section does not exist. No placeholder. No mention of Clicky anywhere.
4. `portal_orders` is never buyer activity. Never "portal ordering adoption."
5. Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) are internal classification terms and must never appear anywhere in the external report — including the Peer Benchmarking section. In §7, describe the peer group using plain-language framing derived from `peer_group_id_effective` (e.g., "Lighting manufacturers on the same platform bundle") — not the raw label or segment classification terms.
6. Executive Summary is always written last
7. Every metric must include a time qualifier (e.g., "trailing 12 months," "last 90 days")
8. Every projection must be hedged with appropriate language ("potential," "estimated," "projected," "roughly," "could," "up to") in client-facing HTML. The literal tags `[HYPOTHETICAL]` and `[ESTIMATED]` are **internal pipeline markers only** — they appear in `cache/` highlight files and priority action candidates so validators and the Stage 4 assembler can track projections, but they must **never appear as visible text in HTML fragments**. If the literal string `[HYPOTHETICAL]` or `[ESTIMATED]` appears in a fragment, it is a rendering defect.
9. Every extrapolation must be hedged with appropriate language in client-facing HTML (same rule as #8 — see above).
10. Do not improvise around missing data — mark as N/A or omit per blueprint rules
11. `benchmark_confidence`, `peer_group_level`, and `peer_group_n` are internal signals only. Never expose these as labels in client-facing HTML — not in prose, callouts, section headers, or footnotes. Use them to calibrate plain-language benchmark framing only.

## C. Forbidden Phrases

> **Runtime copy of the canonical list in GUARDRAILS.md §4.** The post-build check in `qa/eval/check_static.sh` mirrors this list. If you add or remove a forbidden phrase, update GUARDRAILS.md first, then this file and the shell script.

Never in client-facing HTML:

- "health score" / "health scores"
- "portal orders" / "portal ordering" as buyer activity or entity label
- "net-new customers"
- "ERP" in any client-facing text — use "total business," "all-channel sales," "your business system," "your account base"
- "Mixpanel" — use "platform engagement data" or "engagement events"
- "Clicky" — never in delivered HTML
- Segment labels: "Platform-Embedded", "Commerce-Active", "Catalog-Focused"
- Internal identifiers: VM codes, query IDs, table names, column names, org IDs, dataset paths
- "bounce_rate"
- `order_source = 'ipad'` and similar code literals in client-facing prose
- "benchmark_confidence", "peer_group_level", "peer_group_n" as labels
- Literal `[HYPOTHETICAL]` or `[ESTIMATED]` tags — these are internal pipeline markers and must never appear in client-facing HTML

## D. Universal Formatting Rules

- Every metric has a time qualifier (Hard Rule #7)
- Projections use hedging language in HTML; `[HYPOTHETICAL]` tags in cache/highlights only — never in fragments (Hard Rule #8)
- Extrapolations use hedging language in HTML; `[ESTIMATED]` tags in cache/highlights only — never in fragments (Hard Rule #9)
- Dollar formatting: `$X,XXX` or `$X.XM`
- Do not improvise around missing data (Hard Rule #10)
- Every subsection ends with a "What this tells you" close (1–3 sentences, actionable implication)
- One `what-this-means` per subsection. Do not add a second section-level `what-this-means` after the last subsection's close.
- Coaching Opportunities & Selling Archetypes (§2.3) is the one exception to the `what-this-means` rule: coaching cards are self-contained action items and do NOT end with a `what-this-means` block.
- Do not surface operational exclusion methodology, showroom scan details, qualifying threshold explanations, or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference an exclusion count (e.g., "1 showroom excluded") but not the methodology.

## E. Fragment Contract

Every section agent produces an HTML fragment in this exact wrapper:

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div>
      <h2 class="section-title"><span class="section-num">§{{N}}</span> {{SECTION_TITLE}}</h2>
      <div class="section-sub">{{KEY_STATS_ONE_LINE}}</div>
      <div class="section-contents">{{SUBSECTION_LIST_MIDDOT_SEPARATED}}</div>
    </div>
    <span class="expand-hint">&#9662; Click to expand</span>
  </summary>
  <section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">
    {{SUBSECTION_CONTENT}}
  </section>
</details>
```

**Section IDs (locked):** `§2=sales`, `§3=customers`, `§4=product`, `§5=commerce`, `§6=portal`, `§7=peer`, `§8=platform`

**Fragment rules:**
- Starts with `<details`, ends with `</details>` — nothing before or after
- No `<html>`, `<head>`, `<body>`, or `<style>` tags
- No HTML comments (`<!-- -->`)
- `section-contents`: every rendered subsection name, separated by ` · ` (`&middot;`) — must reflect ONLY subsections that actually appear in the fragment (not skipped subsections)
- `section-sub`: data-dense one-liner, not a generic description
- Every subsection: `<div class="subsection">` with `<div class="subsection-title">` as first child
- Every subsection ends with `<div class="what-this-means">` (exception: §2.3 Coaching Opportunities & Selling Archetypes — coaching cards are self-contained and omit what-this-means per Section D above)
- **Structural self-check before saving**: count of `what-this-means` divs must equal count of `subsection` divs minus any coaching-card subsections. If you have more `what-this-means` than subsections, you have a duplicate — remove it. If fewer, a subsection is missing its close.

## F. CSS Class Quick-Reference

From `authority/html_report_template.html` (aligned with gold reference `clm_2026-04-14`). Use these class names exactly.

| Class | Renders |
|-------|---------|
| `.subsection` | Subsection container (24px top margin) |
| `.subsection-title` | Bold 15px subsection heading |
| `.what-this-means` | Amber left-bordered panel box for actionable close |
| `.metrics-grid` | Auto-fill responsive grid of metric cards |
| `.metric-card` | Panel-bg rounded card for a single metric |
| `.metric-val` | Bold 24px metric number |
| `.metric-label` | Mono 9px uppercase muted label |
| `.metric-note` | 11px muted annotation; variants `.ok` / `.warn` / `.danger` |
| `.callout` + `.callout-title` | Rounded box with left border accent; 600-weight 13px title |
| `.callout.insight` | Panel bg + amber left border |
| `.callout.alert` | Danger-bg + red left border (use instead of `.callout.warning`) |
| `.callout.opportunity` | Ok-bg + green left border (use instead of `.callout.action`) |
| `.badge` | Inline mono 10px uppercase pill |
| `.badge.ok` / `.badge.warn` / `.badge.danger` / `.badge.info` / `.badge.muted` | Status pills (dot notation — space-separated classes) |
| `.coaching-card` | White card with warn-colored 3px top border |
| `.coaching-header` / `.coaching-name` | Flex header row; bold 15px name |
| `.coaching-body` / `.coaching-action` / `.coaching-impact` | 13px body; medium-weight action; mono green impact pill |
| `.prose` | 13.5px secondary-color paragraph with 16px bottom margin |
| `<details>` (inner) | Panel-bg summary with arrow and click-to-expand pattern |
| `.row-highlight` | Table row with green (`--ok-bg`) emphasis |
| `.section-num` | Mono 11px muted section number prefix (e.g., §2) |
| `.peer-hero` | Panel-bg flex container for hero benchmark stat |
| `.peer-hero-pctile` | 13px mono pill badge; `.above` (green) / `.below` (red) / `.on-par` (muted) |
| `.peer-metric-row` | 3-column grid row for benchmark breakdown |
| `.peer-metric-title` | 12px metric name |
| `.peer-range-bar` / `.peer-range-marker` | 6px bar with positioned dot; `.above` / `.below` / `.on-par` |
| `.quartile-pill` / `.peer-quartile-pill` | 9px mono uppercase pill; `.q4` (green) / `.q3` (blue) / `.q2` (amber) / `.q1` (red) |
| `.priorities` / `.priority` | Grid container; 3-column card (badge / title+desc / impact) |
| `.priority-badge` | Mono 9px urgency pill; `.high` (red) / `.medium` (amber) / `.low` (muted) |
| `.priority-title` / `.priority-desc` / `.priority-impact` | Bold 14px title; 13px desc; mono 11px muted impact |
| `.highlights` | Counter-numbered list (amber-circled counters, light bottom borders) |
| `.top-performer-list` | Container for top-performer behavioral pattern rows (§7.4) |
| `.top-performer-row` | Flex row: icon + text, bottom-bordered |
| `.top-performer-icon` | 26px accent-glow rounded icon cell (use Unicode arrows/symbols) |
| `.top-performer-text` | 13px secondary prose with bold strong elements |
| `.data-confidence` | Info-bg panel at bottom of section body, 12px muted text, info left-border |
| `.data-confidence.limited` | Warn-bg variant with warn left-border (staleness/quality issues) |
| `.data-confidence-label` | Mono 9px uppercase badge prefix (tier label) |
| `.data-confidence-action` | 12px medium-weight text for "what would complete this" line |

## G. Highlight Candidate Format

Each section agent outputs `cache/section_NN_highlights.md` alongside its fragment.

```markdown
# §N Section Title — Highlight Candidates

1. **Bold headline** — one sentence of context with data. [→ §section-id]
2. **Bold headline** — one sentence of context with data. [→ §section-id]

## Priority Action Candidate
- **URGENCY**: Action statement with quantified impact [HYPOTHETICAL]. [→ §section-id]
```

**Note:** `[HYPOTHETICAL]` tags in highlight/priority candidates are correct — these are internal cache files consumed by the Stage 4 assembler, not client-facing HTML. The assembler strips or replaces tags with hedging language when building the Executive Summary.

**Rules:**
- 2–4 highlight candidates per section, ranked by signal strength
- Each: **bold headline**, one sentence of context, section link
- 0–1 priority action candidates per section with urgency level
- Stage 4 assembler selects top 5–6 highlights and 2–4 priority actions from all candidates
- Section agents do not write the Executive Summary — they only propose candidates

**Anti-repetition rule:** Executive summary highlights must NOT be repeated verbatim as section-level introductory callouts. A stat may appear in both the executive summary and a section, but the section must present the underlying data table — the `what-this-means` box must add **new interpretation** beyond what the executive summary already stated. If the `what-this-means` text could be copy-pasted into the executive summary without losing meaning, it is restating, not interpreting. The reader already read the table; the `what-this-means` job is to tell them what it MEANS, not what it SAYS.

## H. Display Limits

- Maximum 15 rows displayed per table. Default visible rows: 5. If showing top 10, show 5 visible + remaining 5 in a collapsed `<details>` element. Section-specific display limits in individual section guides take precedence over these defaults.
- Do not dump all cache file rows into tables. The section guide specifies how many to show per subsection.

## I. Progressive Disclosure — Subsection Collapse

- Subsections marked `[COLLAPSE]` in their section guide are wrapped in an inner `<details>` element within the parent section body (inside the outer `<details class="section-collapse">`).
- Collapsed subsections still appear in the `section-contents` middot list.
- When the user opens the parent section, `[COLLAPSE]` subsections remain closed until individually expanded.

## J. Data Confidence Framework

The Data Confidence Framework provides deterministic, per-section disclosure about what data sources are present, their freshness, and what additional data would make the picture more complete. It is formula-driven — no judgment calls, no improvisation.

### J.1 Tier Definitions

| Tier | Condition | Visual Treatment | Footer Rendered? |
|------|-----------|-----------------|-----------------|
| FULL | All primary + enrichment sources present and fresh (≤30 days) | `.data-confidence` footer | Yes — positive-tone data provenance |
| STRONG | Primary sources present; enrichment source stale (31-180d) or one source missing | `.data-confidence` footer | Yes — with source list |
| PARTIAL | Core eCat data only; ERP context unavailable | `.data-confidence` footer + "what would complete this" | Yes — with action |
| LIMITED | Core data stale (>180d) or known quality issues | `.data-confidence.limited` footer with staleness callout | Yes — with warn styling |

### J.2 Rendering Rules

1. **FULL** — render a `.data-confidence` footer with label `FULL PICTURE` and a positive-tone data sources summary listing what went into the analysis. No "To see X, do Y" action prompt — just a clean statement of what's there. **Position: bottom** of the section (after all subsections).
2. **STRONG / PARTIAL** — render a `.data-confidence` footer with a data sources summary AND an action prompt explaining what additional data would complete the picture. **Position: top** of the section (immediately after the key metrics row, before the first subsection). The reader sees upfront that data is incomplete before investing attention in the analysis.

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

All four tiers use this structure. `{{TIER_LABEL}}` is one of: `FULL PICTURE` / `STRONG VIEW` / `PARTIAL VIEW` / `LIMITED VIEW`.

3. **LIMITED** — same structure but with the `.limited` modifier:

```html
<div class="data-confidence limited">
  <span class="data-confidence-label">LIMITED VIEW</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

4. The confidence footer is part of the section fragment. The assembler pastes it verbatim — it does not modify, strip, or relocate it.
5. Never use "ERP" in any confidence footer text — this is client-facing. Use "your business system," "total business," or "all-channel" per Section C.
6. Confidence tier labels (`FULL PICTURE`, etc.) must not appear anywhere else in the report — they are reserved for this footer.

### J.3 Locked Template Strings

Section builders use these exact strings based on their section ID and tier. Do not paraphrase, shorten, or editorialize.

**§2 Sales Team:**
- `§2-FULL`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users), all-channel order data with rep attribution. Complete data for this section."
- `§2-FULL-NO-ERP`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users). Complete eCat data for this section."
- `§2-PARTIAL`: "Data sources: eCat iPad orders. To see behavioral analytics and selling archetypes, ensure reps are using the eCat iPad app. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-STRONG`: "Data sources: eCat iPad orders, platform behavioral analytics. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-ADMIN-DISCLOSURE`: "Note: This section includes ordering activity from users assigned to internal or administrative roles in your platform configuration. Their activity reflects real orders but may include test or operational transactions."

The `§2-ADMIN-DISCLOSURE` template is an **additive append** — it is rendered as a second line inside the same `.data-confidence` div when `ADMIN_REPS_IN_LEADERBOARD = true`, regardless of tier. At FULL tier, append the disclosure as a `<br>` line inside the FULL PICTURE footer. At STRONG/PARTIAL, append as a `<br>` line inside the existing footer.

Use `§2-FULL` when `PORTAL_REP_DATA_PRESENT = true`. Use `§2-FULL-NO-ERP` when `PORTAL_REP_DATA_PRESENT = false` (eCat + Mixpanel data present, but no all-channel rep attribution).

**§3 Customer:**
- `§3-FULL`: "Data sources: eCat order history, account records ({{CUSTOMER_COUNT}} accounts), all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§3-PARTIAL`: "Data sources: eCat order history, account records. To see customer-level penetration of your total business and identify high-value unactivated accounts, sync order data via your business system."
- `§3-STRONG`: "Data sources: eCat order history, account records, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current total-business context."

**§4 Product:**
- `§4-FULL`: "Data sources: Product catalog ({{PRODUCT_COUNT}} items), inventory data, sales history. Complete data for this section."
- `§4-PARTIAL`: "Data sources: Product catalog. To see inventory status and sales performance by category, import inventory and sales history data."
- `§4-STRONG`: "Data sources: Product catalog, {{SOURCES_PRESENT}}. {{STALE_SOURCE}} was last updated {{STALE_DATE}} — refresh for current analysis."

**§5 Commerce:**
- `§5-FULL`: "Data sources: eCat orders, all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§5-PARTIAL`: "Data sources: eCat orders by channel and type. To see eCat's share of your total business and per-customer penetration, sync order data via your business system."
- `§5-STRONG`: "Data sources: eCat orders, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current context."

### J.4 Template Variable Resolution

- `{{LAST_PORTAL_ORDER_DATE}}` — from the ERP enrichment preflight (`most_recent_erp_order`), formatted as "Month DD, YYYY"
- `{{SOURCES_PRESENT}}` — comma-separated list of present sources (e.g., "inventory data, sales history")
- `{{STALE_SOURCE}}` — the specific source that is stale (e.g., "Inventory data", "Sales history")
- `{{STALE_DATE}}` — from Q-08 data_versions, formatted as "Month DD, YYYY"
- `{{MIXPANEL_USER_COUNT}}` — from `gate_flags.md` evidence for `MIXPANEL_USER_DATA_PRESENT` (the row count from Q-01 Step 1). If unavailable, omit the parenthetical from the FULL template and just say "platform behavioral analytics".
- `{{CUSTOMER_COUNT}}` — from `gate_flags.md` evidence for customer base count (Q-10 or equivalent). If unavailable, omit the parenthetical from the FULL template.
- `{{PRODUCT_COUNT}}` — from `gate_flags.md` evidence for product count (Q-08 catalog count). If unavailable, omit the parenthetical from the FULL template.

If a template variable cannot be resolved (source missing), use the PARTIAL template instead — never render a STRONG or FULL template with unresolved variables. For FULL templates, the parenthetical counts (`{{MIXPANEL_USER_COUNT}}`, `{{CUSTOMER_COUNT}}`, `{{PRODUCT_COUNT}}`) are the only exception — those may be gracefully omitted while keeping the FULL template.

### J.4b PARTIAL-Tier "What You'd See" Teaser

When a subsection is gated out due to missing data (e.g., `HAS_PORTAL_ORDERS = false` suppresses capture rate), section builders at PARTIAL or LIMITED tier MAY include a single `.callout.opportunity` teaser at the point where the gated subsection would appear. This makes the data-enrichment value proposition concrete without being salesy.

**Template:**

```html
<div class="callout opportunity">
  <div class="callout-title">What this section would show with connected data</div>
  <p>{{TEASER_TEXT}}</p>
</div>
```

**Per-section teaser text (use verbatim or adapt to context):**

- **§2 (rep capture):** "If total-business order data with rep attribution were connected, this section would show each rep's capture rate — what percentage of their territory's full revenue flows through the platform. Clients with this data typically discover a 5–30× spread across their team."
- **§3 (customer penetration):** "If total-business order data were connected, this section would show which of your highest-value accounts have never placed a platform order — and the combined revenue they represent through other channels."
- **§5 (capture rate):** "If total-business order data were connected, this section would show your platform capture rate — how much of your full revenue flows through the platform. Clients with this data typically discover 70–90% of their business is invisible to their digital ordering tools."

**Rules:**
- Maximum ONE teaser per section (not per gated subsection)
- Only at PARTIAL or LIMITED tier — never at STRONG or FULL
- Never in §6, §7, or §8 (no confidence framework)
- The teaser replaces the gated subsection's slot — do not leave a gap AND show a teaser

### J.5 Section Builder Contract

Each section builder that has a confidence tier (§2, §3, §4, §5):

1. Reads its tier from `cache/section_confidence.md` (e.g., `SECTION_CONFIDENCE_3`)
2. If tier is FULL — selects the matching `§X-FULL` template from J.3, resolves variables, and places the `.data-confidence` div with label `FULL PICTURE` as the **last element** in the section fragment (after all subsections)
3. If tier is STRONG or PARTIAL — selects the matching template from §J.3, resolves variables, and places the `.data-confidence` div **immediately after the key metrics row, before the first subsection**
4. If tier is LIMITED — uses the `.data-confidence.limited` variant with warn styling, positioned at the **top** (same as STRONG/PARTIAL)
5. Every section fragment for §2–§5 MUST contain exactly one `.data-confidence` footer. §6, §7, and §8 do not have confidence tiers and omit the footer

## Cache Data

### Q-07_results.md

# Q-07 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 2,154 | 0 | 2,154 | 0 |

### Q-37_results.md

# Q-37 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-37 — Inventory × Sales Intelligence (OOS Top Sellers)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| item_code | category_code | collection_code | item_description | total_erp_invoiced | total_qty_sold | qty_available | qty_on_hand | qty_on_backorder | next_scheduled_receipt_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U097523 | UP022 | U097 | Walter Swivel Chair - Special Order | $1.2M | 1,295 | 0 | 0 | 0 | — |
| 071040 | BR040 | 071 | Drawer Dresser | $1.2M | 1,315 | 0 | 0 | 0 | — |
| 071355 | BR062 | 071 | Nightstand | $1.2M | 2,508 | 0 | 0 | 0 | — |
| U330350 | BR062 | U330 | Weekender Nightstand | $1.1M | 3,192 | 0 | 0 | 0 | — |
| U330D365 | BR098 | U330 | Bimini Chest | $1.1M | 1,919 | 0 | 0 | 0 | — |
| 997503 | UP022 | 997 | Burke Chair - Special Order | $962,893 | 1,204 | 0 | 0 | 0 | — |
| U181320B | BR005 | U181 | Daybreak Bed King | $954,829 | 850 | 0 | 0 | 0 | — |
| U365966 | HE031 | U365 | Cosmo Credenza | $888,892 | 279 | 0 | 0 | 0 | — |
| U352E964 | HE031 | U352 | Lumi Credenza | $888,060 | 763 | 0 | 0 | 0 | — |
| U428A050 | BR040 | U428 | Carmen Dresser | $872,373 | 953 | 0 | 0 | 0 | — |
| U352040 | BR040 | U352 | Walker Drawer Dresser | $871,370 | 1,073 | 0 | 0 | 0 | — |
| U181310CF-B | BR005 | U181 | Daybreak Bed -Special Order | $852,447 | 455 | 0 | 0 | 0 | — |
| U301350 | BR062 | U301 | Presley Nightstand | $839,681 | 2,478 | 0 | 0 | 0 | — |
| U195210CF-B | BR005 | U195 | Restore Bed -Special Order | $757,745 | 380 | 0 | 0 | 0 | — |
| U064523 | UP022 | U064 | Hudson Skirted Recliner -Special Order | $739,796 | 489 | 0 | 0 | 0 | — |
| U428050 | BR040 | U428 | Carmen Dresser | $720,217 | 765 | 0 | 0 | 0 | — |
| U330175 | BR028 | U330 | Weekender Chest | $698,360 | 796 | 0 | 0 | 0 | — |
| U330A355 | BR062 | U330 | Turo Nightstand | $692,358 | 1,881 | 0 | 0 | 0 | — |
| U330160 | BR016 | U330 | Weekender Utility Cabinet | $674,517 | 647 | 0 | 0 | 0 | — |
| U225A050 | BR040 | U225 | Vista Drawer Dresser | $650,923 | 576 | 0 | 0 | 0 | — |

### Q-38a_results.md

# Q-38a Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-39_category_results.md

# Q-39-cat Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 46
- **Run date**: 2026-06-16


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| BR005 | $24.2M | 23,528 | 170 | $142,609 |
| BR062 | $23.2M | 53,310 | 84 | $275,943 |
| BR040 | $19.8M | 22,605 | 50 | $396,276 |
| DR023 | $17.4M | 73,325 | 80 | $217,030 |
| UP022 | $16.4M | 19,819 | 144 | $113,863 |
| DR079 | $8.9M | 10,512 | 60 | $148,607 |
| HE031 | $8.7M | 6,770 | 28 | $309,021 |
| UP074 | $8.0M | 5,907 | 69 | $115,235 |
| AT053 | $6.5M | 19,757 | 101 | $64,839 |
| AT075 | $6.4M | 8,570 | 49 | $131,385 |
| DR018 | $5.9M | 5,171 | 29 | $203,986 |
| AT030 | $5.9M | 10,021 | 56 | $104,855 |
| BR028 | $4.1M | 4,637 | 16 | $256,672 |
| BR016 | $3.0M | 2,510 | 10 | $299,835 |
| DR029 | $3.0M | 2,460 | 16 | $184,419 |
| BR098 | $2.5M | 4,240 | 10 | $253,550 |
| DR099 | $2.3M | 6,861 | 15 | $156,190 |
| MO074 | $2.0M | 1,446 | 8 | $255,090 |
| BR010 | $1.9M | 5,039 | 19 | $100,848 |
| UP058 | $1.7M | 1,217 | 29 | $59,501 |
| BR060 | $1.6M | 5,000 | 35 | $46,258 |
| MO022 | $1.5M | 1,858 | 16 | $93,935 |
| AT103 | $1.3M | 3,268 | 14 | $93,409 |
| DR143 | $1.3M | 2,068 | 9 | $143,522 |
| UP065 | $1.2M | 2,721 | 42 | $28,239 |
| AT034 | $1.1M | 1,542 | 7 | $156,892 |
| AT137 | $976,460 | 1,093 | 10 | $97,646 |
| UP117 | $959,895 | 313 | 16 | $59,993 |
| AT028 | $761,166 | 1,014 | 10 | $76,117 |
| OD022 | $526,891 | 654 | 9 | $58,543 |
| UP107 | $374,250 | 4,328 | 8 | $46,781 |
| OD082 | $371,955 | 453 | 2 | $185,978 |
| OD074 | $369,068 | 190 | 6 | $61,511 |
| OD053 | $350,757 | 1,645 | 5 | $70,151 |
| UP093 | $319,429 | 318 | 17 | $18,790 |
| AT145 | $270,436 | 586 | 3 | $90,145 |
| MO058 | $251,054 | 301 | 3 | $83,685 |
| OD030 | $235,059 | 525 | 2 | $117,529 |
| OD002 | $172,724 | 691 | 10 | $17,272 |
| UP010 | $122,390 | 176 | 3 | $40,797 |
| MO117 | $107,772 | 38 | 1 | $107,772 |
| OD072 | $95,591 | 288 | 2 | $47,796 |
| OD065 | $58,371 | 174 | 6 | $9,729 |
| MO061 | $47,339 | 423 | 1 | $47,339 |
| BR061 | $15,940 | 134 | 10 | $1,594 |
| OD131 | $9,692 | 88 | 4 | $2,423 |

### Q-39_collection_results.md

# Q-39-col Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| U330 | $20.8M | 41,931 | 62 | $336,092 |
| U428 | $14.3M | 27,356 | 52 | $274,204 |
| U352 | $13.3M | 25,982 | 56 | $237,433 |
| U470 | $8.8M | 13,199 | 69 | $127,588 |
| U533 | $8.3M | 16,930 | 87 | $95,589 |
| U301 | $8.1M | 14,112 | 32 | $252,006 |
| U365 | $7.8M | 9,560 | 39 | $198,859 |
| U400 | $7.7M | 12,700 | 59 | $129,746 |
| U462 | $6.8M | 13,044 | 65 | $105,025 |
| U181 | $6.8M | 11,570 | 26 | $260,821 |
| 956 | $6.7M | 11,842 | 17 | $395,550 |
| 833 | $6.7M | 11,951 | 32 | $208,077 |
| U225 | $6.3M | 18,403 | 15 | $418,045 |
| U508 | $4.5M | 8,214 | 38 | $118,346 |
| 071 | $4.5M | 6,348 | 8 | $556,885 |
| U064 | $3.1M | 2,439 | 29 | $106,567 |
| 643 | $3.0M | 4,906 | 13 | $229,877 |
| U195 | $2.0M | 1,742 | 9 | $218,327 |
| U290 | $1.7M | 1,491 | 8 | $217,425 |
| U033 | $1.7M | 4,125 | 12 | $139,773 |
| U550 | $1.6M | 3,392 | 72 | $22,418 |
| U390 | $1.4M | 1,089 | 18 | $79,483 |
| U097 | $1.3M | 1,426 | 4 | $336,237 |
| U012 | $1.3M | 3,799 | 24 | $54,990 |
| 997 | $1.3M | 1,665 | 4 | $316,937 |

### Q-42_results.md

# Q-42 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-59_results.md

# Q-59 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORG_SUMMARY | — | — | — | 86.50 | 35,228 | — | — | — | — | — | — |

### Q-61_results.md

(not present — file does not exist or is empty)
