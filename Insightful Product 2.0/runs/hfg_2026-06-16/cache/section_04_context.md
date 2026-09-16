# Section 4 Context Bundle — Hubbardton Forge (hfg)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=22104, portal_order_gmv=$42.2M |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | True | sales_data_count=44934 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | hubbardton_forge_hfg_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$42.2M > ecat_gmv=$16.8M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 137 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1871, Mixpanel total submit_order (Q-01): 3113 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.1%, ambiguous_rate=88.1%, showroom_event_share=3.5% |
| USER_GROUP_JOIN_RATE | 86% | 118 of 137 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Shannon Rose, Retha Boles |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=47 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2590 |
| INVENTORY_FRESH | False | inventories last_updated 300d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=57 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Hubbardton Forge
- **Shortname**: hfg
- **Org ID**: 165
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | True |
| HAS_PORTAL_ORDERS | True |
| HAS_INVENTORY | False |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | False |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | FULL | See Derived Gate 6 §2 formula |
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

# Q-07 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-07 — Catalog Completeness Score
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| visibility | total_products | missing_images | missing_price | completeness_pct |
| --- | --- | --- | --- | --- |
| visible | 1,082 | 48 | 0 | 95.60 |

### Q-37_results.md

(not present — file does not exist or is empty)

### Q-38a_results.md

# Q-38a Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-38a — Product Velocity Trend
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 6227
- **Run date**: 2026-06-16


| item_code | item_description | category_code | collection_code | month | quantity_ordered | order_count |
| --- | --- | --- | --- | --- | --- | --- |
|  | — | — | — | 2025-12-01 | 22 | 3 |
|  | — | — | — | 2026-01-01 | 113 | 14 |
|  | — | — | — | 2026-02-01 | 176 | 33 |
|  | — | — | — | 2026-03-01 | 300 | 23 |
|  | — | — | — | 2026-04-01 | 103 | 8 |
|  | — | — | — | 2026-05-01 | 159 | 10 |
|  | — | — | — | 2026-06-01 | 14 | 8 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2025-12-01 | 1 | 2 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2026-01-01 | 8 | 8 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2026-02-01 | 4 | 4 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2026-03-01 | 7 | 7 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2026-04-01 | 6 | 6 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2026-05-01 | 9 | 9 |
| 101160 | Simple Sweep 6-Arm Chandelier | CAT7 | COL11 | 2026-06-01 | 5 | 5 |
| 101261 | Aegis 5-Arm Chandelier | CAT7 | AEGIS | 2025-12-01 | 1 | 1 |
| 101261 | Aegis 5-Arm Chandelier | CAT7 | AEGIS | 2026-03-01 | 2 | 2 |
| 101261 | Aegis 5-Arm Chandelier | CAT7 | AEGIS | 2026-05-01 | 2 | 2 |
| 101261 | Aegis 5-Arm Chandelier | CAT7 | AEGIS | 2026-06-01 | 1 | 1 |
| 101309 | — | — | — | 2026-03-01 | 1 | 1 |
| 101315 | Tura 4-Light Small Chandelier | CAT7 | TURA | 2026-01-01 | 1 | 1 |
| 101315 | Tura 4-Light Small Chandelier | CAT7 | TURA | 2026-02-01 | 4 | 3 |
| 101315 | Tura 4-Light Small Chandelier | CAT7 | TURA | 2026-03-01 | 2 | 2 |
| 101315 | Tura 4-Light Small Chandelier | CAT7 | TURA | 2026-05-01 | 4 | 4 |
| 101315 | Tura 4-Light Small Chandelier | CAT7 | TURA | 2026-06-01 | 1 | 1 |
| 101316 | Tura 4-Light Medium Chandelier | CAT7 | TURA | 2026-01-01 | 1 | 1 |
| 101316 | Tura 4-Light Medium Chandelier | CAT7 | TURA | 2026-02-01 | 1 | 1 |
| 101316 | Tura 4-Light Medium Chandelier | CAT7 | TURA | 2026-05-01 | 3 | 3 |
| 101317 | Tura 8-Light Large Chandelier | CAT7 | TURA | 2026-01-01 | 1 | 1 |
| 101317 | Tura 8-Light Large Chandelier | CAT7 | TURA | 2026-02-01 | 1 | 1 |
| 101317 | Tura 8-Light Large Chandelier | CAT7 | TURA | 2026-03-01 | 3 | 3 |
| 101317 | Tura 8-Light Large Chandelier | CAT7 | TURA | 2026-04-01 | 4 | 4 |
| 101317 | Tura 8-Light Large Chandelier | CAT7 | TURA | 2026-05-01 | 2 | 2 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2025-12-01 | 3 | 3 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2026-01-01 | 3 | 3 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2026-02-01 | 5 | 5 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2026-03-01 | 4 | 3 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2026-04-01 | 1 | 1 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2026-05-01 | 4 | 3 |
| 101320 | Parasol 7-Light Chandelier | CAT7 | COL36 | 2026-06-01 | 2 | 2 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | COL84 | 2026-01-01 | 22 | 20 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | COL84 | 2026-02-01 | 13 | 13 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | COL84 | 2026-03-01 | 20 | 21 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | COL84 | 2026-04-01 | 13 | 6 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | COL84 | 2026-05-01 | 10 | 10 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | COL84 | 2026-06-01 | 4 | 4 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | COL84 | 2026-01-01 | 6 | 6 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | COL84 | 2026-02-01 | 12 | 12 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | COL84 | 2026-03-01 | 13 | 11 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | COL84 | 2026-04-01 | 10 | 10 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | COL84 | 2026-05-01 | 9 | 8 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | COL84 | 2026-06-01 | 7 | 7 |
| 101441 | Sweeping Taper 3-Arm Chandelier | CAT7 | COL1 | 2026-01-01 | 2 | 2 |
| 101441 | Sweeping Taper 3-Arm Chandelier | CAT7 | COL1 | 2026-02-01 | 3 | 3 |
| 101441 | Sweeping Taper 3-Arm Chandelier | CAT7 | COL1 | 2026-03-01 | 1 | 1 |
| 101441 | Sweeping Taper 3-Arm Chandelier | CAT7 | COL1 | 2026-06-01 | 1 | 1 |
| 101445 | Sweeping Taper 5-Arm Chandelier | CAT7 | COL1 | 2026-01-01 | 7 | 4 |
| 101445 | Sweeping Taper 5-Arm Chandelier | CAT7 | COL1 | 2026-03-01 | 1 | 1 |
| 101445 | Sweeping Taper 5-Arm Chandelier | CAT7 | COL1 | 2026-05-01 | 2 | 2 |
| 101445 | Sweeping Taper 5-Arm Chandelier | CAT7 | COL1 | 2026-06-01 | 1 | 1 |
| 101473 | — | — | — | 2026-05-01 | 1 | 1 |
| 101620 | — | — | — | 2026-01-01 | 1 | 1 |
| 101700 | Lilium 4-Light Chandelier | CAT7 | COL40 | 2025-12-01 | 2 | 1 |
| 101700 | Lilium 4-Light Chandelier | CAT7 | COL40 | 2026-01-01 | 2 | 2 |
| 101700 | Lilium 4-Light Chandelier | CAT7 | COL40 | 2026-02-01 | 0 | 1 |
| 101700 | Lilium 4-Light Chandelier | CAT7 | COL40 | 2026-03-01 | 4 | 3 |
| 101700 | Lilium 4-Light Chandelier | CAT7 | COL40 | 2026-04-01 | 2 | 2 |
| 101700 | Lilium 4-Light Chandelier | CAT7 | COL40 | 2026-05-01 | 1 | 1 |
| 101702 | Lilium 6-Light Chandelier | CAT7 | COL40 | 2026-01-01 | 3 | 3 |
| 101702 | Lilium 6-Light Chandelier | CAT7 | COL40 | 2026-02-01 | 3 | 4 |
| 101702 | Lilium 6-Light Chandelier | CAT7 | COL40 | 2026-03-01 | 5 | 5 |
| 101702 | Lilium 6-Light Chandelier | CAT7 | COL40 | 2026-04-01 | 2 | 2 |
| 101702 | Lilium 6-Light Chandelier | CAT7 | COL40 | 2026-05-01 | 2 | 2 |
| 101706 | Lilium 12-Light Chandelier | CAT7 | COL40 | 2026-02-01 | 1 | 1 |
| 101706 | Lilium 12-Light Chandelier | CAT7 | COL40 | 2026-03-01 | 4 | 3 |
| 101706 | Lilium 12-Light Chandelier | CAT7 | COL40 | 2026-04-01 | 2 | 2 |
| 101706 | Lilium 12-Light Chandelier | CAT7 | COL40 | 2026-06-01 | 1 | 1 |
| 103033 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2025-12-01 | 1 | 1 |
| 103033 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-01-01 | 1 | 1 |
| 103033 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-03-01 | 1 | 1 |
| 103033 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-04-01 | 1 | 1 |
| 103033 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-05-01 | 4 | 4 |
| 103033 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-06-01 | 1 | 1 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2025-12-01 | 3 | 4 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-01-01 | 6 | 6 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-02-01 | 10 | 10 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-03-01 | 4 | 4 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-04-01 | 8 | 5 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-05-01 | 10 | 10 |
| 103040 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-06-01 | 2 | 2 |
| 103043 | Flora 6 Arm Chandelier | CAT7 | FLORA | 2026-02-01 | 3 | 2 |
| 103043 | Flora 6 Arm Chandelier | CAT7 | FLORA | 2026-03-01 | 2 | 2 |
| 103045 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-01-01 | 5 | 3 |
| 103045 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-02-01 | 1 | 1 |
| 103045 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-03-01 | 2 | 2 |
| 103045 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-04-01 | 1 | 1 |
| 103045 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-05-01 | 2 | 2 |
| 103045 | Flora 5-Arm Chandelier | CAT7 | FLORA | 2026-06-01 | 1 | 1 |
| 103047 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-03-01 | 7 | 5 |
| 103047 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-04-01 | 4 | 3 |
| 103047 | Flora 3-Arm Chandelier | CAT7 | FLORA | 2026-05-01 | 4 | 4 |
| 103049 | Flora 7-Arm Chandelier | CAT7 | FLORA | 2026-01-01 | 1 | 1 |
| 103049 | Flora 7-Arm Chandelier | CAT7 | FLORA | 2026-02-01 | 3 | 3 |
| 103049 | Flora 7-Arm Chandelier | CAT7 | FLORA | 2026-03-01 | 3 | 3 |
| 103049 | Flora 7-Arm Chandelier | CAT7 | FLORA | 2026-05-01 | 2 | 2 |
| 103052 | — | — | — | 2026-03-01 | 2 | 2 |
| 103052 | — | — | — | 2026-04-01 | 2 | 2 |
| 103063 | — | — | — | 2026-01-01 | 1 | 1 |
| 103285 | — | — | — | 2026-01-01 | 1 | 1 |
| 103290 | New Town 10-Arm Chandelier | CAT7 | COL4 | 2025-12-01 | 1 | 1 |
| 103290 | New Town 10-Arm Chandelier | CAT7 | COL4 | 2026-01-01 | 2 | 2 |
| 103290 | New Town 10-Arm Chandelier | CAT7 | COL4 | 2026-02-01 | 3 | 2 |
| 103290 | New Town 10-Arm Chandelier | CAT7 | COL4 | 2026-04-01 | 1 | 1 |
| 104060 | Bow Tall Mini Pendant | CAT13 | BOW | 2026-01-01 | 1 | 1 |
| 104060 | Bow Tall Mini Pendant | CAT13 | BOW | 2026-02-01 | 6 | 2 |
| 104060 | Bow Tall Mini Pendant | CAT13 | BOW | 2026-03-01 | 7 | 3 |
| 104060 | Bow Tall Mini Pendant | CAT13 | BOW | 2026-05-01 | 3 | 2 |
| 104060 | Bow Tall Mini Pendant | CAT13 | BOW | 2026-06-01 | 3 | 1 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2025-12-01 | 2 | 1 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2026-01-01 | 15 | 11 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2026-02-01 | 4 | 4 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2026-03-01 | 5 | 5 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2026-04-01 | 4 | 3 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2026-05-01 | 1 | 1 |
| 104070 | Saratoga Small Pendant | CAT1 | COL5 | 2026-06-01 | 2 | 2 |
| 104072 | Saratoga Large Pendant | CAT1 | COL5 | 2026-01-01 | 4 | 4 |
| 104072 | Saratoga Large Pendant | CAT1 | COL5 | 2026-02-01 | 10 | 8 |
| 104072 | Saratoga Large Pendant | CAT1 | COL5 | 2026-03-01 | 4 | 3 |
| 104072 | Saratoga Large Pendant | CAT1 | COL5 | 2026-04-01 | 7 | 6 |
| 104072 | Saratoga Large Pendant | CAT1 | COL5 | 2026-05-01 | 5 | 4 |
| 104072 | Saratoga Large Pendant | CAT1 | COL5 | 2026-06-01 | 2 | 2 |
| 104106 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2025-12-01 | 1 | 1 |
| 104106 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-01-01 | 2 | 2 |
| 104106 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-02-01 | 2 | 2 |
| 104106 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-04-01 | 1 | 1 |
| 104106 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-05-01 | 3 | 3 |
| 104116 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-01-01 | 1 | 1 |
| 104116 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-02-01 | 1 | 1 |
| 104116 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-04-01 | 2 | 2 |
| 104116 | Oval Ribbon 6-Arm Chandelier | CAT7 | COL6 | 2026-05-01 | 3 | 2 |
| 104201 | Cirque Small Chandelier | CAT7 | COL32 | 2026-01-01 | 9 | 7 |
| 104201 | Cirque Small Chandelier | CAT7 | COL32 | 2026-02-01 | 11 | 5 |
| 104201 | Cirque Small Chandelier | CAT7 | COL32 | 2026-03-01 | 12 | 9 |
| 104201 | Cirque Small Chandelier | CAT7 | COL32 | 2026-04-01 | 1 | 1 |
| 104201 | Cirque Small Chandelier | CAT7 | COL32 | 2026-05-01 | 5 | 4 |
| 104201 | Cirque Small Chandelier | CAT7 | COL32 | 2026-06-01 | 4 | 4 |
| 104203 | Cirque Large Chandelier | CAT7 | COL32 | 2025-12-01 | 1 | 1 |
| 104203 | Cirque Large Chandelier | CAT7 | COL32 | 2026-01-01 | 6 | 7 |
| 104203 | Cirque Large Chandelier | CAT7 | COL32 | 2026-02-01 | 4 | 3 |
| 104203 | Cirque Large Chandelier | CAT7 | COL32 | 2026-03-01 | 3 | 3 |
| 104203 | Cirque Large Chandelier | CAT7 | COL32 | 2026-05-01 | 1 | 1 |
| 104203 | Cirque Large Chandelier | CAT7 | COL32 | 2026-06-01 | 3 | 2 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2025-12-01 | 1 | 1 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2026-01-01 | 7 | 8 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2026-02-01 | 13 | 12 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2026-03-01 | 6 | 6 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2026-04-01 | 7 | 7 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2026-05-01 | 7 | 5 |
| 104205 | Double Cirque Chandelier | CAT7 | COL32 | 2026-06-01 | 1 | 1 |
| 104230 | Loop Pendant | CAT7 | LOOP | 2025-12-01 | 2 | 2 |
| 104230 | Loop Pendant | CAT7 | LOOP | 2026-01-01 | 3 | 3 |
| 104230 | Loop Pendant | CAT7 | LOOP | 2026-02-01 | 1 | 2 |
| 104230 | Loop Pendant | CAT7 | LOOP | 2026-03-01 | 1 | 1 |
| 104230 | Loop Pendant | CAT7 | LOOP | 2026-04-01 | 1 | 1 |
| 104230 | Loop Pendant | CAT7 | LOOP | 2026-05-01 | 1 | 2 |
| 104250 | Bow Pendant | CAT1 | BOW | 2025-12-01 | 2 | 2 |
| 104250 | Bow Pendant | CAT1 | BOW | 2026-01-01 | 3 | 3 |
| 104250 | Bow Pendant | CAT1 | BOW | 2026-02-01 | 13 | 6 |
| 104250 | Bow Pendant | CAT1 | BOW | 2026-03-01 | 6 | 5 |
| 104250 | Bow Pendant | CAT1 | BOW | 2026-04-01 | 2 | 2 |
| 104250 | Bow Pendant | CAT1 | BOW | 2026-05-01 | 4 | 4 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2025-12-01 | 6 | 5 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2026-01-01 | 3 | 3 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2026-02-01 | 3 | 3 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2026-03-01 | 2 | 2 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2026-04-01 | 7 | 7 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2026-05-01 | 5 | 4 |
| 104255 | Bow Large Pendant | CAT1 | BOW | 2026-06-01 | 3 | 3 |
| 104260 | Bow Tall Pendant | CAT1 | BOW | 2025-12-01 | 1 | 1 |
| 104260 | Bow Tall Pendant | CAT1 | BOW | 2026-01-01 | 1 | 1 |
| 104260 | Bow Tall Pendant | CAT1 | BOW | 2026-02-01 | 1 | 1 |
| 104260 | Bow Tall Pendant | CAT1 | BOW | 2026-03-01 | 3 | 4 |
| 104260 | Bow Tall Pendant | CAT1 | BOW | 2026-06-01 | 2 | 1 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2025-12-01 | 4 | 4 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2026-01-01 | 10 | 9 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2026-02-01 | 6 | 6 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2026-03-01 | 8 | 8 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2026-04-01 | 9 | 9 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2026-05-01 | 12 | 12 |
| 104350 | Dahlia Chandelier | CAT7 | COL13 | 2026-06-01 | 6 | 4 |
| 104355 | Dahlia Large Chandelier | CAT1 | COL13 | 2025-12-01 | 1 | 1 |
| 104355 | Dahlia Large Chandelier | CAT1 | COL13 | 2026-01-01 | 2 | 2 |
| 104355 | Dahlia Large Chandelier | CAT1 | COL13 | 2026-02-01 | 3 | 3 |
| 104355 | Dahlia Large Chandelier | CAT1 | COL13 | 2026-03-01 | 3 | 3 |
| 104355 | Dahlia Large Chandelier | CAT1 | COL13 | 2026-05-01 | 5 | 6 |
| 104355 | Dahlia Large Chandelier | CAT1 | COL13 | 2026-06-01 | 3 | 3 |
| 104360 | Apothecary Circular Chandelier | CAT7 | COL34 | 2025-12-01 | 1 | 1 |
| 104360 | Apothecary Circular Chandelier | CAT7 | COL34 | 2026-01-01 | 1 | 1 |
| 104360 | Apothecary Circular Chandelier | CAT7 | COL34 | 2026-02-01 | 3 | 3 |
| 104360 | Apothecary Circular Chandelier | CAT7 | COL34 | 2026-03-01 | 1 | 1 |
| 104360 | Apothecary Circular Chandelier | CAT7 | COL34 | 2026-05-01 | 1 | 1 |
| 105020 | Gatsby Chandelier | CAT7 | COL35 | 2026-03-01 | 1 | 1 |
| 105020 | Gatsby Chandelier | CAT7 | COL35 | 2026-05-01 | 1 | 1 |
| 105021 | Gatsby 8-Light Chandelier | CAT7 | COL35 | 2026-04-01 | 2 | 2 |
| 105021 | Gatsby 8-Light Chandelier | CAT7 | COL35 | 2026-06-01 | 1 | 1 |
| 105040 | Banded Ring Chandelier | CAT7 | COL16 | 2026-01-01 | 1 | 1 |
| 105040 | Banded Ring Chandelier | CAT7 | COL16 | 2026-03-01 | 2 | 2 |
| 105040 | Banded Ring Chandelier | CAT7 | COL16 | 2026-04-01 | 1 | 1 |
| 105040 | Banded Ring Chandelier | CAT7 | COL16 | 2026-05-01 | 4 | 3 |
| 105040 | Banded Ring Chandelier | CAT7 | COL16 | 2026-06-01 | 4 | 2 |
| 105045 | Vela 5-Arm Chandelier | CAT7 | VELA | 2025-12-01 | 2 | 2 |
| 105045 | Vela 5-Arm Chandelier | CAT7 | VELA | 2026-02-01 | 3 | 2 |
| 105045 | Vela 5-Arm Chandelier | CAT7 | VELA | 2026-03-01 | 2 | 2 |
| 105045 | Vela 5-Arm Chandelier | CAT7 | VELA | 2026-04-01 | 1 | 1 |
| 105045 | Vela 5-Arm Chandelier | CAT7 | VELA | 2026-05-01 | 1 | 1 |
| 105045 | Vela 5-Arm Chandelier | CAT7 | VELA | 2026-06-01 | 3 | 3 |
| 105050 | Grace 8-Arm Chandelier | CAT7 | GRACE | 2026-01-01 | 3 | 3 |
| 105050 | Grace 8-Arm Chandelier | CAT7 | GRACE | 2026-02-01 | 2 | 2 |
| 105050 | Grace 8-Arm Chandelier | CAT7 | GRACE | 2026-03-01 | 2 | 2 |
| 105050 | Grace 8-Arm Chandelier | CAT7 | GRACE | 2026-04-01 | 6 | 6 |
| 105050 | Grace 8-Arm Chandelier | CAT7 | GRACE | 2026-05-01 | 2 | 2 |
| 105055 | — | — | — | 2026-01-01 | 1 | 1 |
| 105055 | — | — | — | 2026-02-01 | 1 | 1 |
| 106030 | Lisse 10-Arm Chandelier | CAT7 | LISSE | 2025-12-01 | 1 | 1 |
| 106030 | Lisse 10-Arm Chandelier | CAT7 | LISSE | 2026-01-01 | 1 | 1 |
| 106030 | Lisse 10-Arm Chandelier | CAT7 | LISSE | 2026-02-01 | 3 | 3 |
| 106030 | Lisse 10-Arm Chandelier | CAT7 | LISSE | 2026-03-01 | 2 | 2 |
| 106030 | Lisse 10-Arm Chandelier | CAT7 | LISSE | 2026-04-01 | 5 | 4 |
| 106030 | Lisse 10-Arm Chandelier | CAT7 | LISSE | 2026-05-01 | 5 | 4 |
| 121059 | Callisto Semi-Flush | CAT2 | COL82 | 2026-01-01 | 3 | 2 |
| 121059 | Callisto Semi-Flush | CAT2 | COL82 | 2026-02-01 | 3 | 3 |
| 121059 | Callisto Semi-Flush | CAT2 | COL82 | 2026-03-01 | 1 | 1 |
| 121059 | Callisto Semi-Flush | CAT2 | COL82 | 2026-05-01 | 1 | 1 |
| 121059 | Callisto Semi-Flush | CAT2 | COL82 | 2026-06-01 | 1 | 1 |
| 121140 | Bow Semi-Flush | CAT2 | BOW | 2026-01-01 | 5 | 3 |
| 121140 | Bow Semi-Flush | CAT2 | BOW | 2026-03-01 | 5 | 3 |
| 121140 | Bow Semi-Flush | CAT2 | BOW | 2026-04-01 | 5 | 2 |
| 121140 | Bow Semi-Flush | CAT2 | BOW | 2026-06-01 | 2 | 2 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2025-12-01 | 2 | 2 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2026-01-01 | 1 | 1 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2026-02-01 | 3 | 3 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2026-03-01 | 5 | 2 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2026-04-01 | 4 | 4 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2026-05-01 | 4 | 2 |
| 121142 | Bow Medium Semi-Flush | CAT2 | BOW | 2026-06-01 | 9 | 2 |
| 121145 | Bow Large Semi-Flush | CAT2 | BOW | 2025-12-01 | 2 | 2 |
| 121145 | Bow Large Semi-Flush | CAT2 | BOW | 2026-01-01 | 3 | 3 |
| 121145 | Bow Large Semi-Flush | CAT2 | BOW | 2026-02-01 | 7 | 6 |
| 121145 | Bow Large Semi-Flush | CAT2 | BOW | 2026-03-01 | 8 | 7 |
| 121145 | Bow Large Semi-Flush | CAT2 | BOW | 2026-05-01 | 4 | 3 |
| 121145 | Bow Large Semi-Flush | CAT2 | BOW | 2026-06-01 | 11 | 4 |
| 121320 | Parasol 7-Light Semi-Flush | CAT2 | COL36 | 2025-12-01 | 1 | 1 |
| 121320 | Parasol 7-Light Semi-Flush | CAT2 | COL36 | 2026-01-01 | 1 | 1 |
| 121320 | Parasol 7-Light Semi-Flush | CAT2 | COL36 | 2026-02-01 | 2 | 2 |
| 121320 | Parasol 7-Light Semi-Flush | CAT2 | COL36 | 2026-04-01 | 2 | 2 |
| 121320 | Parasol 7-Light Semi-Flush | CAT2 | COL36 | 2026-05-01 | 2 | 2 |
| 121320 | Parasol 7-Light Semi-Flush | CAT2 | COL36 | 2026-06-01 | 2 | 2 |
| 121370 | Ume 4-Light Semi-Flush | CAT2 | UME | 2025-12-01 | 2 | 2 |
| 121370 | Ume 4-Light Semi-Flush | CAT2 | UME | 2026-01-01 | 4 | 3 |
| 121370 | Ume 4-Light Semi-Flush | CAT2 | UME | 2026-02-01 | 1 | 1 |
| 121370 | Ume 4-Light Semi-Flush | CAT2 | UME | 2026-03-01 | 3 | 2 |
| 121370 | Ume 4-Light Semi-Flush | CAT2 | UME | 2026-04-01 | 2 | 2 |
| 121370 | Ume 4-Light Semi-Flush | CAT2 | UME | 2026-05-01 | 4 | 4 |
| 121372 | Ume 1-Light Semi-Flush | CAT2 | UME | 2025-12-01 | 1 | 1 |
| 121372 | Ume 1-Light Semi-Flush | CAT2 | UME | 2026-01-01 | 3 | 2 |
| 121372 | Ume 1-Light Semi-Flush | CAT2 | UME | 2026-02-01 | 3 | 3 |
| 121372 | Ume 1-Light Semi-Flush | CAT2 | UME | 2026-03-01 | 1 | 1 |
| 121372 | Ume 1-Light Semi-Flush | CAT2 | UME | 2026-04-01 | 1 | 1 |
| 121373 | Ume 3-Light Semi-Flush | CAT2 | UME | 2026-01-01 | 1 | 1 |
| 121373 | Ume 3-Light Semi-Flush | CAT2 | UME | 2026-02-01 | 2 | 2 |
| 121373 | Ume 3-Light Semi-Flush | CAT2 | UME | 2026-03-01 | 2 | 2 |
| 121373 | Ume 3-Light Semi-Flush | CAT2 | UME | 2026-04-01 | 2 | 2 |
| 121373 | Ume 3-Light Semi-Flush | CAT2 | UME | 2026-05-01 | 0 | 1 |
| 121374 | Brooklyn 3-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-01-01 | 5 | 4 |
| 121374 | Brooklyn 3-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-02-01 | 3 | 3 |
| 121374 | Brooklyn 3-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-03-01 | 6 | 5 |
| 121374 | Brooklyn 3-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-04-01 | 2 | 2 |
| 121374 | Brooklyn 3-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-05-01 | 2 | 2 |
| 121376 | Brooklyn 4-Light Double Shade Semi-Flush | CAT2 | COL2 | 2025-12-01 | 1 | 1 |
| 121376 | Brooklyn 4-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-01-01 | 3 | 2 |
| 121376 | Brooklyn 4-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-03-01 | 3 | 2 |
| 121376 | Brooklyn 4-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-05-01 | 2 | 2 |
| 121376 | Brooklyn 4-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-06-01 | 1 | 1 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2025-12-01 | 1 | 1 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-01-01 | 4 | 4 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-02-01 | 1 | 1 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-03-01 | 7 | 4 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-04-01 | 3 | 3 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-05-01 | 3 | 2 |
| 121377 | Brooklyn 1-Light Double Shade Semi-Flush | CAT2 | COL2 | 2026-06-01 | 3 | 3 |
| 121380 | Atlas Semi-Flush | CAT2 | ATLAS | 2026-02-01 | 2 | 2 |
| 121380 | Atlas Semi-Flush | CAT2 | ATLAS | 2026-03-01 | 4 | 3 |
| 121380 | Atlas Semi-Flush | CAT2 | ATLAS | 2026-04-01 | 3 | 2 |
| 121500 | Astra Semi-Flush | CAT2 | ASTRA | 2025-12-01 | 1 | 1 |
| 121500 | Astra Semi-Flush | CAT2 | ASTRA | 2026-01-01 | 2 | 2 |
| 121500 | Astra Semi-Flush | CAT2 | ASTRA | 2026-03-01 | 2 | 2 |
| 121500 | Astra Semi-Flush | CAT2 | ASTRA | 2026-04-01 | 5 | 3 |
| 121500 | Astra Semi-Flush | CAT2 | ASTRA | 2026-05-01 | 7 | 2 |
| 121500 | Astra Semi-Flush | CAT2 | ASTRA | 2026-06-01 | 1 | 1 |
| 121620 | — | — | — | 2026-01-01 | 4 | 1 |
| 121620 | — | — | — | 2026-03-01 | 1 | 1 |
| 122110 | Yoki 3-Light Semi-Flush | CAT2 | YOKI | 2026-03-01 | 3 | 3 |
| 122111 | Nova Small LED Flush Mount | CAT2 | NOVA | 2026-01-01 | 14 | 12 |
| 122111 | Nova Small LED Flush Mount | CAT2 | NOVA | 2026-02-01 | 18 | 13 |
| 122111 | Nova Small LED Flush Mount | CAT2 | NOVA | 2026-03-01 | 4 | 1 |
| 122111 | Nova Small LED Flush Mount | CAT2 | NOVA | 2026-04-01 | 11 | 8 |
| 122111 | Nova Small LED Flush Mount | CAT2 | NOVA | 2026-05-01 | 14 | 8 |
| 122111 | Nova Small LED Flush Mount | CAT2 | NOVA | 2026-06-01 | 6 | 6 |
| 122112 | Nova Large LED Flush Mount | CAT2 | NOVA | 2026-01-01 | 3 | 2 |
| 122112 | Nova Large LED Flush Mount | CAT2 | NOVA | 2026-02-01 | 4 | 4 |
| 122112 | Nova Large LED Flush Mount | CAT2 | NOVA | 2026-04-01 | 3 | 3 |
| 122112 | Nova Large LED Flush Mount | CAT2 | NOVA | 2026-06-01 | 1 | 1 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2025-12-01 | 1 | 1 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2026-01-01 | 6 | 7 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2026-02-01 | 5 | 5 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2026-03-01 | 6 | 5 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2026-04-01 | 11 | 9 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2026-05-01 | 10 | 8 |
| 123305 | Kirigami Semi-Flush | CAT2 | COL8 | 2026-06-01 | 2 | 2 |
| 123705 | Steppe Small Semi-Flush | CAT2 | COL9 | 2025-12-01 | 1 | 1 |
| 123705 | Steppe Small Semi-Flush | CAT2 | COL9 | 2026-01-01 | 8 | 6 |
| 123705 | Steppe Small Semi-Flush | CAT2 | COL9 | 2026-02-01 | 6 | 3 |
| 123705 | Steppe Small Semi-Flush | CAT2 | COL9 | 2026-03-01 | 7 | 6 |
| 123705 | Steppe Small Semi-Flush | CAT2 | COL9 | 2026-04-01 | 1 | 1 |
| 123705 | Steppe Small Semi-Flush | CAT2 | COL9 | 2026-05-01 | 0 | 1 |
| 123715 | Steppe Large Semi-Flush | CAT2 | COL9 | 2026-01-01 | 1 | 1 |
| 123715 | Steppe Large Semi-Flush | CAT2 | COL9 | 2026-02-01 | 1 | 1 |
| 123715 | Steppe Large Semi-Flush | CAT2 | COL9 | 2026-03-01 | 2 | 2 |
| 123715 | Steppe Large Semi-Flush | CAT2 | COL9 | 2026-04-01 | 6 | 4 |
| 123715 | Steppe Large Semi-Flush | CAT2 | COL9 | 2026-05-01 | 1 | 2 |
| 123775 | Exos Round Semi-Flush | CAT2 | COL39 | 2025-12-01 | 3 | 2 |
| 123775 | Exos Round Semi-Flush | CAT2 | COL39 | 2026-01-01 | 7 | 2 |
| 123775 | Exos Round Semi-Flush | CAT2 | COL39 | 2026-02-01 | 6 | 3 |
| 123775 | Exos Round Semi-Flush | CAT2 | COL39 | 2026-03-01 | 5 | 4 |
| 123775 | Exos Round Semi-Flush | CAT2 | COL39 | 2026-04-01 | 1 | 1 |
| 124251 | Moonband Semi-Flush | CAT2 | COL10 | 2026-01-01 | 1 | 2 |
| 124251 | Moonband Semi-Flush | CAT2 | COL10 | 2026-02-01 | 5 | 3 |
| 124251 | Moonband Semi-Flush | CAT2 | COL10 | 2026-03-01 | 7 | 3 |
| 124251 | Moonband Semi-Flush | CAT2 | COL10 | 2026-04-01 | 4 | 3 |
| 124251 | Moonband Semi-Flush | CAT2 | COL10 | 2026-05-01 | 2 | 2 |
| 124251 | Moonband Semi-Flush | CAT2 | COL10 | 2026-06-01 | 2 | 1 |
| 124252 | Moonband Large Semi-Flush | CAT2 | COL10 | 2026-01-01 | 2 | 2 |
| 124252 | Moonband Large Semi-Flush | CAT2 | COL10 | 2026-02-01 | 9 | 5 |
| 124252 | Moonband Large Semi-Flush | CAT2 | COL10 | 2026-03-01 | 4 | 3 |
| 124252 | Moonband Large Semi-Flush | CAT2 | COL10 | 2026-04-01 | 6 | 1 |
| 124252 | Moonband Large Semi-Flush | CAT2 | COL10 | 2026-05-01 | 2 | 2 |
| 124252 | Moonband Large Semi-Flush | CAT2 | COL10 | 2026-06-01 | 3 | 1 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2025-12-01 | 0 | 1 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2026-01-01 | 9 | 6 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2026-02-01 | 1 | 1 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2026-03-01 | 9 | 8 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2026-04-01 | 8 | 5 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2026-05-01 | 4 | 4 |
| 124302 | Plain Small Semi-Flush | CAT2 | COL11 | 2026-06-01 | 1 | 1 |
| 124304 | Plain Large Semi-Flush | CAT2 | COL11 | 2025-12-01 | 4 | 3 |
| 124304 | Plain Large Semi-Flush | CAT2 | COL11 | 2026-01-01 | 1 | 2 |
| 124304 | Plain Large Semi-Flush | CAT2 | COL11 | 2026-02-01 | 6 | 5 |
| 124304 | Plain Large Semi-Flush | CAT2 | COL11 | 2026-03-01 | 4 | 4 |
| 124304 | Plain Large Semi-Flush | CAT2 | COL11 | 2026-04-01 | 7 | 6 |
| 124304 | Plain Large Semi-Flush | CAT2 | COL11 | 2026-05-01 | 5 | 5 |
| 124341 | Mackintosh Semi-Flush | CAT2 | COL12 | 2026-01-01 | 4 | 4 |
| 124341 | Mackintosh Semi-Flush | CAT2 | COL12 | 2026-02-01 | 4 | 5 |
| 124341 | Mackintosh Semi-Flush | CAT2 | COL12 | 2026-03-01 | 4 | 4 |
| 124341 | Mackintosh Semi-Flush | CAT2 | COL12 | 2026-05-01 | 2 | 2 |
| 124341 | Mackintosh Semi-Flush | CAT2 | COL12 | 2026-06-01 | 2 | 2 |
| 124350 | Dahlia Semi-Flush | CAT2 | COL13 | 2025-12-01 | 1 | 1 |
| 124350 | Dahlia Semi-Flush | CAT2 | COL13 | 2026-01-01 | 0 | 1 |
| 124350 | Dahlia Semi-Flush | CAT2 | COL13 | 2026-03-01 | 1 | 1 |
| 124350 | Dahlia Semi-Flush | CAT2 | COL13 | 2026-04-01 | 2 | 2 |
| 124350 | Dahlia Semi-Flush | CAT2 | COL13 | 2026-06-01 | 1 | 1 |
| 124352 | Dahlia Medium Semi-Flush | CAT2 | COL13 | 2025-12-01 | 2 | 1 |
| 124352 | Dahlia Medium Semi-Flush | CAT2 | COL13 | 2026-02-01 | 1 | 1 |
| 124352 | Dahlia Medium Semi-Flush | CAT2 | COL13 | 2026-06-01 | 2 | 2 |
| 124362 | Mobius 12-Light Semi-Flush | CAT2 | COL14 | 2026-01-01 | 3 | 3 |
| 124362 | Mobius 12-Light Semi-Flush | CAT2 | COL14 | 2026-02-01 | 4 | 4 |
| 124362 | Mobius 12-Light Semi-Flush | CAT2 | COL14 | 2026-03-01 | 1 | 1 |
| 124362 | Mobius 12-Light Semi-Flush | CAT2 | COL14 | 2026-05-01 | 2 | 2 |
| 124362 | Mobius 12-Light Semi-Flush | CAT2 | COL14 | 2026-06-01 | 1 | 1 |
| 124394 | Banded Semi-Flush | CAT2 | COL16 | 2026-01-01 | 3 | 3 |
| 124394 | Banded Semi-Flush | CAT2 | COL16 | 2026-02-01 | 2 | 2 |
| 124394 | Banded Semi-Flush | CAT2 | COL16 | 2026-03-01 | 7 | 4 |
| 124394 | Banded Semi-Flush | CAT2 | COL16 | 2026-04-01 | 3 | 3 |
| 124394 | Banded Semi-Flush | CAT2 | COL16 | 2026-05-01 | 2 | 2 |
| 124402 | Presidio Tryne Flush Mount | CAT2 | TRYNE | 2025-12-01 | 2 | 1 |
| 124402 | Presidio Tryne Flush Mount | CAT2 | TRYNE | 2026-01-01 | 4 | 2 |
| 124402 | Presidio Tryne Flush Mount | CAT2 | TRYNE | 2026-02-01 | 1 | 1 |
| 124402 | Presidio Tryne Flush Mount | CAT2 | TRYNE | 2026-03-01 | 11 | 6 |
| 124402 | Presidio Tryne Flush Mount | CAT2 | TRYNE | 2026-04-01 | 5 | 5 |
| 124402 | Presidio Tryne Flush Mount | CAT2 | TRYNE | 2026-05-01 | 4 | 4 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2025-12-01 | 2 | 2 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2026-01-01 | 12 | 12 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2026-02-01 | 8 | 8 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2026-03-01 | 20 | 13 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2026-04-01 | 13 | 10 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2026-05-01 | 7 | 7 |
| 124412 | Presidio Tryne Small Semi-Flush | CAT2 | TRYNE | 2026-06-01 | 7 | 6 |
| 124422 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2025-12-01 | 1 | 1 |
| 124422 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-01-01 | 2 | 2 |
| 124422 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-02-01 | 5 | 3 |
| 124422 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-03-01 | 4 | 4 |
| 124422 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-04-01 | 3 | 4 |
| 124422 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-05-01 | 3 | 3 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2025-12-01 | 2 | 1 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-01-01 | 1 | 1 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-02-01 | 10 | 9 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-03-01 | 7 | 7 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-04-01 | 1 | 1 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-05-01 | 9 | 7 |
| 124432 | Presidio Tryne Semi-Flush | CAT2 | TRYNE | 2026-06-01 | 4 | 4 |
| 124442 | Presidio Tryne Large Semi-Flush | CAT2 | TRYNE | 2026-01-01 | 5 | 5 |
| 124442 | Presidio Tryne Large Semi-Flush | CAT2 | TRYNE | 2026-02-01 | 2 | 1 |
| 124442 | Presidio Tryne Large Semi-Flush | CAT2 | TRYNE | 2026-03-01 | 4 | 4 |
| 124442 | Presidio Tryne Large Semi-Flush | CAT2 | TRYNE | 2026-04-01 | 2 | 2 |
| 124442 | Presidio Tryne Large Semi-Flush | CAT2 | TRYNE | 2026-05-01 | 1 | 1 |
| 124550 | Compass Flush Mount | CAT2 | COL17 | 2026-01-01 | 2 | 2 |
| 124550 | Compass Flush Mount | CAT2 | COL17 | 2026-02-01 | 1 | 1 |
| 124550 | Compass Flush Mount | CAT2 | COL17 | 2026-03-01 | 2 | 2 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2025-12-01 | 3 | 3 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2026-01-01 | 2 | 2 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2026-02-01 | 3 | 3 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2026-03-01 | 3 | 3 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2026-04-01 | 2 | 2 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2026-05-01 | 4 | 3 |
| 124555 | Compass Small Semi-Flush | CAT2 | COL17 | 2026-06-01 | 2 | 2 |
| 124560 | Compass Large Semi-Flush | CAT2 | COL17 | 2025-12-01 | 2 | 2 |
| 124560 | Compass Large Semi-Flush | CAT2 | COL17 | 2026-01-01 | 11 | 2 |
| 124560 | Compass Large Semi-Flush | CAT2 | COL17 | 2026-02-01 | 3 | 3 |
| 124560 | Compass Large Semi-Flush | CAT2 | COL17 | 2026-03-01 | 3 | 2 |
| 124560 | Compass Large Semi-Flush | CAT2 | COL17 | 2026-05-01 | 5 | 3 |
| 124710 | Antasia Semi-Flush | CAT2 | COL18 | 2026-01-01 | 5 | 3 |
| 124710 | Antasia Semi-Flush | CAT2 | COL18 | 2026-02-01 | 1 | 1 |
| 124710 | Antasia Semi-Flush | CAT2 | COL18 | 2026-03-01 | 6 | 4 |
| 124710 | Antasia Semi-Flush | CAT2 | COL18 | 2026-04-01 | 2 | 2 |
| 124710 | Antasia Semi-Flush | CAT2 | COL18 | 2026-05-01 | 1 | 1 |
| 124910 | Twilight Flush Mount | CAT2 | COL19 | 2026-01-01 | 4 | 2 |
| 124910 | Twilight Flush Mount | CAT2 | COL19 | 2026-02-01 | 6 | 1 |
| 124910 | Twilight Flush Mount | CAT2 | COL19 | 2026-03-01 | 47 | 4 |
| 124910 | Twilight Flush Mount | CAT2 | COL19 | 2026-04-01 | 15 | 3 |
| 124910 | Twilight Flush Mount | CAT2 | COL19 | 2026-06-01 | 4 | 3 |
| 126400 | Axis Flush Mount | CAT2 | AXIS | 2026-01-01 | 10 | 9 |
| 126400 | Axis Flush Mount | CAT2 | AXIS | 2026-02-01 | 11 | 9 |
| 126400 | Axis Flush Mount | CAT2 | AXIS | 2026-03-01 | 3 | 2 |
| 126400 | Axis Flush Mount | CAT2 | AXIS | 2026-04-01 | 6 | 3 |
| 126400 | Axis Flush Mount | CAT2 | AXIS | 2026-05-01 | 8 | 4 |
| 126400 | Axis Flush Mount | CAT2 | AXIS | 2026-06-01 | 2 | 2 |
| 126401 | Axis Flush Mount | CAT2 | AXIS | 2026-03-01 | 1 | 1 |
| 126401 | Axis Flush Mount | CAT2 | AXIS | 2026-04-01 | 2 | 2 |
| 126401 | Axis Flush Mount | CAT2 | AXIS | 2026-06-01 | 1 | 1 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2025-12-01 | 2 | 1 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2026-01-01 | 3 | 3 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2026-02-01 | 16 | 2 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2026-03-01 | 4 | 3 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2026-04-01 | 7 | 6 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2026-05-01 | 4 | 4 |
| 126403 | Axis Semi-Flush | CAT2 | AXIS | 2026-06-01 | 9 | 4 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2025-12-01 | 3 | 1 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-01-01 | 18 | 12 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-02-01 | 6 | 5 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-03-01 | 7 | 7 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-04-01 | 7 | 3 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-05-01 | 8 | 5 |
| 126501 | Exos Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-06-01 | 1 | 1 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2025-12-01 | 7 | 5 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2026-01-01 | 18 | 16 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2026-02-01 | 22 | 9 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2026-03-01 | 12 | 8 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2026-04-01 | 20 | 11 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2026-05-01 | 25 | 19 |
| 126503 | Exos Double Shade Semi-Flush | CAT2 | EXOS | 2026-06-01 | 4 | 3 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2025-12-01 | 3 | 3 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-01-01 | 6 | 6 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-02-01 | 5 | 5 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-03-01 | 16 | 10 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-04-01 | 4 | 4 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-05-01 | 9 | 5 |
| 126505 | Exos Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-06-01 | 4 | 4 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2025-12-01 | 4 | 2 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-01-01 | 1 | 1 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-02-01 | 1 | 1 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-03-01 | 2 | 2 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-04-01 | 1 | 1 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-05-01 | 4 | 1 |
| 126507 | Exos Square Small Double Shade Semi-Flush | CAT2 | EXOS | 2026-06-01 | 1 | 1 |
| 126510 | Exos Square Double Shade Semi-Flush | CAT2 | EXOS | 2025-12-01 | 2 | 1 |
| 126510 | Exos Square Double Shade Semi-Flush | CAT2 | EXOS | 2026-01-01 | 4 | 3 |
| 126510 | Exos Square Double Shade Semi-Flush | CAT2 | EXOS | 2026-02-01 | 3 | 3 |
| 126510 | Exos Square Double Shade Semi-Flush | CAT2 | EXOS | 2026-03-01 | 4 | 4 |
| 126510 | Exos Square Double Shade Semi-Flush | CAT2 | EXOS | 2026-04-01 | 2 | 2 |
| 126510 | Exos Square Double Shade Semi-Flush | CAT2 | EXOS | 2026-05-01 | 7 | 5 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2025-12-01 | 2 | 2 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-01-01 | 1 | 1 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-02-01 | 3 | 3 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-03-01 | 5 | 5 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-04-01 | 7 | 5 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-05-01 | 1 | 1 |
| 126513 | Exos Square Large Double Shade Semi-Flush | CAT2 | EXOS | 2026-06-01 | 1 | 1 |
| 126601 | Wren Flush Mount | CAT2 | WREN | 2025-12-01 | 1 | 1 |
| 126601 | Wren Flush Mount | CAT2 | WREN | 2026-01-01 | 9 | 1 |
| 126601 | Wren Flush Mount | CAT2 | WREN | 2026-02-01 | 5 | 3 |
| 126601 | Wren Flush Mount | CAT2 | WREN | 2026-03-01 | 19 | 4 |
| 126601 | Wren Flush Mount | CAT2 | WREN | 2026-04-01 | 1 | 1 |
| 126601 | Wren Flush Mount | CAT2 | WREN | 2026-05-01 | 17 | 4 |
| 126620 | Bento Semi-Flush | CAT2 | BENTO | 2026-01-01 | 1 | 1 |
| 126620 | Bento Semi-Flush | CAT2 | BENTO | 2026-02-01 | 1 | 1 |
| 126620 | Bento Semi-Flush | CAT2 | BENTO | 2026-03-01 | 1 | 1 |
| 126620 | Bento Semi-Flush | CAT2 | BENTO | 2026-04-01 | 5 | 5 |
| 126620 | Bento Semi-Flush | CAT2 | BENTO | 2026-05-01 | 1 | 1 |
| 126620 | Bento Semi-Flush | CAT2 | BENTO | 2026-06-01 | 2 | 2 |
| 126709 | Forged Leaves Flush Mount | CAT2 | LEAF | 2026-01-01 | 6 | 3 |
| 126709 | Forged Leaves Flush Mount | CAT2 | LEAF | 2026-02-01 | 5 | 4 |
| 126709 | Forged Leaves Flush Mount | CAT2 | LEAF | 2026-03-01 | 3 | 3 |
| 126709 | Forged Leaves Flush Mount | CAT2 | LEAF | 2026-04-01 | 10 | 6 |
| 126709 | Forged Leaves Flush Mount | CAT2 | LEAF | 2026-05-01 | 5 | 2 |
| 126712 | Forged Leaves Semi-Flush | CAT2 | LEAF | 2025-12-01 | 0 | 1 |
| 126712 | Forged Leaves Semi-Flush | CAT2 | LEAF | 2026-01-01 | 4 | 4 |
| 126712 | Forged Leaves Semi-Flush | CAT2 | LEAF | 2026-02-01 | 1 | 1 |
| 126712 | Forged Leaves Semi-Flush | CAT2 | LEAF | 2026-03-01 | 4 | 3 |
| 126712 | Forged Leaves Semi-Flush | CAT2 | LEAF | 2026-04-01 | 4 | 3 |
| 126712 | Forged Leaves Semi-Flush | CAT2 | LEAF | 2026-05-01 | 1 | 1 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2025-12-01 | 1 | 1 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2026-01-01 | 4 | 2 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2026-02-01 | 6 | 6 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2026-03-01 | 9 | 5 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2026-04-01 | 1 | 1 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2026-05-01 | 3 | 3 |
| 126732 | Forged Leaves Large Semi-Flush | CAT2 | LEAF | 2026-06-01 | 2 | 2 |
| 126737 | Oceanus Semi-flush | CAT2 | COL21 | 2026-01-01 | 4 | 3 |
| 126737 | Oceanus Semi-flush | CAT2 | COL21 | 2026-02-01 | 5 | 3 |
| 126737 | Oceanus Semi-flush | CAT2 | COL21 | 2026-03-01 | 1 | 1 |
| 126737 | Oceanus Semi-flush | CAT2 | COL21 | 2026-04-01 | 1 | 1 |
| 126737 | Oceanus Semi-flush | CAT2 | COL21 | 2026-05-01 | 1 | 2 |
| 126737 | Oceanus Semi-flush | CAT2 | COL21 | 2026-06-01 | 2 | 2 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2025-12-01 | 3 | 2 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2026-01-01 | 5 | 5 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2026-02-01 | 4 | 2 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2026-03-01 | 18 | 9 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2026-04-01 | 11 | 7 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2026-05-01 | 7 | 3 |
| 126740 | Flora Flush Mount | CAT2 | FLORA | 2026-06-01 | 2 | 1 |
| 126742 | Flora LED Flush Mount | CAT2 | FLORA | 2025-12-01 | 1 | 1 |
| 126742 | Flora LED Flush Mount | CAT2 | FLORA | 2026-01-01 | 1 | 1 |
| 126742 | Flora LED Flush Mount | CAT2 | FLORA | 2026-03-01 | 2 | 2 |
| 126742 | Flora LED Flush Mount | CAT2 | FLORA | 2026-05-01 | 1 | 1 |
| 126745 | Metra Flush Mount | CAT2 | METRA | 2025-12-01 | 1 | 1 |
| 126745 | Metra Flush Mount | CAT2 | METRA | 2026-01-01 | 7 | 6 |
| 126745 | Metra Flush Mount | CAT2 | METRA | 2026-02-01 | 4 | 3 |
| 126745 | Metra Flush Mount | CAT2 | METRA | 2026-03-01 | 5 | 4 |
| 126745 | Metra Flush Mount | CAT2 | METRA | 2026-04-01 | 5 | 4 |
| 126745 | Metra Flush Mount | CAT2 | METRA | 2026-06-01 | 1 | 1 |
| 126747 | Metra LED Flush Mount | CAT2 | METRA | 2026-02-01 | 4 | 3 |
| 126747 | Metra LED Flush Mount | CAT2 | METRA | 2026-04-01 | 1 | 1 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2025-12-01 | 1 | 1 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2026-01-01 | 1 | 1 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2026-02-01 | 5 | 3 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2026-03-01 | 3 | 2 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2026-04-01 | 5 | 5 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2026-05-01 | 9 | 2 |
| 126751 | Impressions Large Semi-Flush | CAT2 | COL22 | 2026-06-01 | 2 | 2 |
| 126753 | Impressions Semi-Flush | CAT2 | COL22 | 2026-01-01 | 1 | 1 |
| 126753 | Impressions Semi-Flush | CAT2 | COL22 | 2026-02-01 | 1 | 1 |
| 126753 | Impressions Semi-Flush | CAT2 | COL22 | 2026-05-01 | 1 | 1 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2025-12-01 | 2 | 1 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2026-01-01 | 2 | 2 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2026-02-01 | 1 | 1 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2026-03-01 | 3 | 3 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2026-04-01 | 2 | 2 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2026-05-01 | 6 | 4 |
| 126803 | Disq LED Semi-Flush | CAT2 | DISQ | 2026-06-01 | 1 | 1 |
| 126805 | Disq Large LED Semi-Flush | CAT2 | DISQ | 2025-12-01 | 1 | 1 |
| 126805 | Disq Large LED Semi-Flush | CAT2 | DISQ | 2026-01-01 | 2 | 2 |
| 126805 | Disq Large LED Semi-Flush | CAT2 | DISQ | 2026-02-01 | 18 | 2 |
| 126805 | Disq Large LED Semi-Flush | CAT2 | DISQ | 2026-04-01 | 2 | 2 |
| 126805 | Disq Large LED Semi-Flush | CAT2 | DISQ | 2026-05-01 | 2 | 2 |
| 126805 | Disq Large LED Semi-Flush | CAT2 | DISQ | 2026-06-01 | 1 | 1 |
| 127660 | Brindille Semi-Flush | CAT2 | COL24 | 2026-01-01 | 5 | 4 |
| 127660 | Brindille Semi-Flush | CAT2 | COL24 | 2026-02-01 | 1 | 1 |
| 127660 | Brindille Semi-Flush | CAT2 | COL24 | 2026-03-01 | 6 | 4 |
| 127660 | Brindille Semi-Flush | CAT2 | COL24 | 2026-04-01 | 4 | 4 |
| 127660 | Brindille Semi-Flush | CAT2 | COL24 | 2026-05-01 | 6 | 5 |
| 127660 | Brindille Semi-Flush | CAT2 | COL24 | 2026-06-01 | 2 | 2 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2025-12-01 | 1 | 1 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2026-01-01 | 4 | 3 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2026-02-01 | 2 | 2 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2026-03-01 | 4 | 5 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2026-04-01 | 3 | 3 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2026-05-01 | 1 | 1 |
| 128712 | Corona Semi-Flush | CAT2 | COL26 | 2026-06-01 | 2 | 2 |
| 128715 | Sprig Semi-Flush | CAT2 | SPRIG | 2025-12-01 | 3 | 3 |
| 128715 | Sprig Semi-Flush | CAT2 | SPRIG | 2026-01-01 | 3 | 3 |
| 128715 | Sprig Semi-Flush | CAT2 | SPRIG | 2026-03-01 | 7 | 6 |
| 128715 | Sprig Semi-Flush | CAT2 | SPRIG | 2026-04-01 | 4 | 4 |
| 128715 | Sprig Semi-Flush | CAT2 | SPRIG | 2026-05-01 | 2 | 1 |
| 128715 | Sprig Semi-Flush | CAT2 | SPRIG | 2026-06-01 | 2 | 2 |
| 128716 | Sprig 6-Light Semi-Flush | CAT2 | SPRIG | 2025-12-01 | 1 | 1 |
| 128716 | Sprig 6-Light Semi-Flush | CAT2 | SPRIG | 2026-01-01 | 1 | 1 |
| 128716 | Sprig 6-Light Semi-Flush | CAT2 | SPRIG | 2026-02-01 | 2 | 2 |
| 128716 | Sprig 6-Light Semi-Flush | CAT2 | SPRIG | 2026-03-01 | 1 | 1 |
| 128716 | Sprig 6-Light Semi-Flush | CAT2 | SPRIG | 2026-05-01 | 1 | 1 |
| 128720 | Nest Semi-Flush | CAT2 | NEST | 2025-12-01 | 1 | 1 |
| 128720 | Nest Semi-Flush | CAT2 | NEST | 2026-01-01 | 1 | 1 |
| 128720 | Nest Semi-Flush | CAT2 | NEST | 2026-02-01 | 2 | 2 |
| 128720 | Nest Semi-Flush | CAT2 | NEST | 2026-04-01 | 2 | 2 |
| 128720 | Nest Semi-Flush | CAT2 | NEST | 2026-05-01 | 2 | 2 |
| 131001 | Muse LED Pendant | CAT1 | MUSE | 2026-01-01 | 9 | 7 |
| 131001 | Muse LED Pendant | CAT1 | MUSE | 2026-02-01 | 16 | 15 |
| 131001 | Muse LED Pendant | CAT1 | MUSE | 2026-03-01 | 5 | 5 |
| 131001 | Muse LED Pendant | CAT1 | MUSE | 2026-04-01 | 3 | 3 |
| 131001 | Muse LED Pendant | CAT1 | MUSE | 2026-05-01 | 3 | 3 |
| 131001 | Muse LED Pendant | CAT1 | MUSE | 2026-06-01 | 4 | 3 |
| 131002 | Muse LED Large Pendant | CAT1 | MUSE | 2026-01-01 | 8 | 7 |
| 131002 | Muse LED Large Pendant | CAT1 | MUSE | 2026-02-01 | 5 | 5 |
| 131002 | Muse LED Large Pendant | CAT1 | MUSE | 2026-03-01 | 3 | 3 |
| 131002 | Muse LED Large Pendant | CAT1 | MUSE | 2026-04-01 | 1 | 1 |
| 131002 | Muse LED Large Pendant | CAT1 | MUSE | 2026-05-01 | 6 | 6 |
| 131002 | Muse LED Large Pendant | CAT1 | MUSE | 2026-06-01 | 3 | 3 |
| 131003 | Sora Pendant | CAT1 | SORA | 2026-01-01 | 5 | 5 |
| 131003 | Sora Pendant | CAT1 | SORA | 2026-02-01 | 1 | 1 |
| 131003 | Sora Pendant | CAT1 | SORA | 2026-03-01 | 7 | 4 |
| 131003 | Sora Pendant | CAT1 | SORA | 2026-04-01 | 7 | 5 |
| 131003 | Sora Pendant | CAT1 | SORA | 2026-06-01 | 2 | 1 |
| 131008 | Bellis 6-Arm 12-Light Round Chandelier | CAT1 | COL87 | 2026-01-01 | 4 | 4 |
| 131008 | Bellis 6-Arm 12-Light Round Chandelier | CAT1 | COL87 | 2026-02-01 | 6 | 5 |
| 131008 | Bellis 6-Arm 12-Light Round Chandelier | CAT1 | COL87 | 2026-04-01 | 1 | 1 |
| 131008 | Bellis 6-Arm 12-Light Round Chandelier | CAT1 | COL87 | 2026-05-01 | 2 | 2 |
| 131008 | Bellis 6-Arm 12-Light Round Chandelier | CAT1 | COL87 | 2026-06-01 | 4 | 3 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | COL87 | 2026-01-01 | 7 | 7 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | COL87 | 2026-02-01 | 5 | 5 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | COL87 | 2026-03-01 | 4 | 4 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | COL87 | 2026-04-01 | 2 | 3 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | COL87 | 2026-05-01 | 3 | 4 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | COL87 | 2026-06-01 | 2 | 1 |
| 131010 | Vertex Large Pendant/Semi-Flush | CAT1 | COL47 | 2026-03-01 | 1 | 1 |
| 131040 | Derby Small LED Pendant | CAT1 | DERBY | 2025-12-01 | 3 | 1 |
| 131040 | Derby Small LED Pendant | CAT1 | DERBY | 2026-01-01 | 3 | 2 |
| 131040 | Derby Small LED Pendant | CAT1 | DERBY | 2026-02-01 | 3 | 2 |
| 131040 | Derby Small LED Pendant | CAT1 | DERBY | 2026-04-01 | 6 | 3 |
| 131040 | Derby Small LED Pendant | CAT1 | DERBY | 2026-05-01 | 4 | 3 |
| 131040 | Derby Small LED Pendant | CAT1 | DERBY | 2026-06-01 | 2 | 1 |
| 131042 | Derby Large LED Pendant | CAT1 | DERBY | 2026-03-01 | 2 | 1 |
| 131042 | Derby Large LED Pendant | CAT1 | DERBY | 2026-05-01 | 3 | 1 |
| 131043 | Derby Linear 4-Light LED Pendant | CAT1 | DERBY | 2025-12-01 | 1 | 1 |
| 131043 | Derby Linear 4-Light LED Pendant | CAT1 | DERBY | 2026-01-01 | 1 | 1 |
| 131043 | Derby Linear 4-Light LED Pendant | CAT1 | DERBY | 2026-02-01 | 6 | 3 |
| 131043 | Derby Linear 4-Light LED Pendant | CAT1 | DERBY | 2026-03-01 | 1 | 1 |
| 131043 | Derby Linear 4-Light LED Pendant | CAT1 | DERBY | 2026-04-01 | 1 | 1 |
| 131043 | Derby Linear 4-Light LED Pendant | CAT1 | DERBY | 2026-05-01 | 1 | 1 |
| 131046 | Derby Linear 5-Light LED Pendant | CAT1 | DERBY | 2026-01-01 | 2 | 2 |
| 131046 | Derby Linear 5-Light LED Pendant | CAT1 | DERBY | 2026-02-01 | 1 | 1 |
| 131046 | Derby Linear 5-Light LED Pendant | CAT1 | DERBY | 2026-04-01 | 6 | 5 |
| 131046 | Derby Linear 5-Light LED Pendant | CAT1 | DERBY | 2026-05-01 | 4 | 4 |
| 131053 | York Linear 5-Light LED Pendant | CAT1 | YORK | 2026-01-01 | 2 | 2 |
| 131053 | York Linear 5-Light LED Pendant | CAT1 | YORK | 2026-03-01 | 2 | 2 |
| 131053 | York Linear 5-Light LED Pendant | CAT1 | YORK | 2026-04-01 | 1 | 1 |
| 131055 | Passage 3-Light Pendant | CAT1 | COL43 | 2025-12-01 | 1 | 1 |
| 131055 | Passage 3-Light Pendant | CAT1 | COL43 | 2026-01-01 | 2 | 2 |
| 131055 | Passage 3-Light Pendant | CAT1 | COL43 | 2026-02-01 | 1 | 1 |
| 131055 | Passage 3-Light Pendant | CAT1 | COL43 | 2026-03-01 | 2 | 2 |
| 131055 | Passage 3-Light Pendant | CAT1 | COL43 | 2026-05-01 | 1 | 1 |
| 131055 | Passage 3-Light Pendant | CAT1 | COL43 | 2026-06-01 | 1 | 1 |
| 131059 | Callisto 7-Light Pendant | CAT1 | COL82 | 2026-01-01 | 1 | 1 |
| 131059 | Callisto 7-Light Pendant | CAT1 | COL82 | 2026-03-01 | 0 | 1 |
| 131059 | Callisto 7-Light Pendant | CAT1 | COL82 | 2026-04-01 | 6 | 1 |
| 131059 | Callisto 7-Light Pendant | CAT1 | COL82 | 2026-05-01 | 1 | 1 |
| 131060 | Arc 4-Light Semi-Flush/Pendant | CAT1 | ARC | 2026-01-01 | 2 | 1 |
| 131060 | Arc 4-Light Semi-Flush/Pendant | CAT1 | ARC | 2026-02-01 | 2 | 2 |
| 131060 | Arc 4-Light Semi-Flush/Pendant | CAT1 | ARC | 2026-03-01 | 5 | 3 |
| 131060 | Arc 4-Light Semi-Flush/Pendant | CAT1 | ARC | 2026-04-01 | 1 | 1 |
| 131060 | Arc 4-Light Semi-Flush/Pendant | CAT1 | ARC | 2026-05-01 | 3 | 4 |
| 131061 | Gatsby 4-Light Semi-Flush/Pendant | CAT1 | COL35 | 2026-02-01 | 1 | 1 |
| 131061 | Gatsby 4-Light Semi-Flush/Pendant | CAT1 | COL35 | 2026-05-01 | 8 | 3 |
| 131061 | Gatsby 4-Light Semi-Flush/Pendant | CAT1 | COL35 | 2026-06-01 | 3 | 1 |
| 131062 | Eos Semi-Flush/Pendant | CAT1 | EOS | 2026-01-01 | 2 | 2 |
| 131062 | Eos Semi-Flush/Pendant | CAT1 | EOS | 2026-05-01 | 4 | 3 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2025-12-01 | 3 | 1 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2026-01-01 | 11 | 4 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2026-02-01 | 10 | 6 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2026-03-01 | 6 | 3 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2026-04-01 | 5 | 2 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2026-05-01 | 13 | 6 |
| 131065 | Caliper Pendant | CAT1 | COL41 | 2026-06-01 | 2 | 1 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2025-12-01 | 5 | 2 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2026-01-01 | 1 | 1 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2026-02-01 | 13 | 6 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2026-03-01 | 13 | 6 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2026-04-01 | 11 | 6 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2026-05-01 | 7 | 3 |
| 131066 | Caliper Large Pendant | CAT1 | COL41 | 2026-06-01 | 3 | 1 |
| 131067 | Gatsby 9-Light Ring Pendant | CAT1 | COL35 | 2026-01-01 | 1 | 1 |
| 131068 | Brooklyn 9-Light Double Shade Ring Pendant | CAT1 | COL2 | 2026-01-01 | 1 | 1 |
| 131068 | Brooklyn 9-Light Double Shade Ring Pendant | CAT1 | COL2 | 2026-02-01 | 3 | 3 |
| 131068 | Brooklyn 9-Light Double Shade Ring Pendant | CAT1 | COL2 | 2026-03-01 | 1 | 1 |
| 131068 | Brooklyn 9-Light Double Shade Ring Pendant | CAT1 | COL2 | 2026-04-01 | 3 | 2 |
| 131068 | Brooklyn 9-Light Double Shade Ring Pendant | CAT1 | COL2 | 2026-05-01 | 1 | 1 |
| 131069 | Ume 9-Light Ring Pendant | CAT1 | UME | 2026-01-01 | 1 | 1 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2025-12-01 | 1 | 1 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2026-01-01 | 8 | 5 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2026-02-01 | 7 | 5 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2026-03-01 | 3 | 2 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2026-04-01 | 8 | 3 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2026-05-01 | 5 | 4 |
| 131070 | Triomphe 4-Light Pendant | CAT1 | COL83 | 2026-06-01 | 7 | 3 |
| 131071 | Triomphe 8-Light Pendant | CAT1 | COL83 | 2025-12-01 | 1 | 1 |
| 131071 | Triomphe 8-Light Pendant | CAT1 | COL83 | 2026-02-01 | 2 | 2 |
| 131071 | Triomphe 8-Light Pendant | CAT1 | COL83 | 2026-03-01 | 2 | 2 |
| 131071 | Triomphe 8-Light Pendant | CAT1 | COL83 | 2026-05-01 | 1 | 1 |
| 131071 | Triomphe 8-Light Pendant | CAT1 | COL83 | 2026-06-01 | 1 | 1 |
| 131075 | Triomphe 9-Light Linear Pendant | CAT1 | COL83 | 2026-02-01 | 2 | 2 |
| 131075 | Triomphe 9-Light Linear Pendant | CAT1 | COL83 | 2026-03-01 | 2 | 2 |
| 131075 | Triomphe 9-Light Linear Pendant | CAT1 | COL83 | 2026-04-01 | 3 | 3 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2025-12-01 | 1 | 1 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2026-01-01 | 2 | 3 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2026-02-01 | 3 | 3 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2026-03-01 | 1 | 1 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2026-04-01 | 3 | 3 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2026-05-01 | 2 | 2 |
| 131080 | Passage 8-Light Pendant | CAT1 | COL43 | 2026-06-01 | 1 | 1 |
| 131081 | Passage 5-Light Circular Pendant | CAT1 | COL43 | 2026-01-01 | 1 | 1 |
| 131081 | Passage 5-Light Circular Pendant | CAT1 | COL43 | 2026-02-01 | 2 | 2 |
| 131081 | Passage 5-Light Circular Pendant | CAT1 | COL43 | 2026-03-01 | 2 | 2 |
| 131081 | Passage 5-Light Circular Pendant | CAT1 | COL43 | 2026-04-01 | 2 | 2 |
| 131081 | Passage 5-Light Circular Pendant | CAT1 | COL43 | 2026-05-01 | 2 | 2 |
| 131085 | Optic 8-Light Oval Pendant | CAT1 | OPTIC | 2025-12-01 | 2 | 2 |
| 131085 | Optic 8-Light Oval Pendant | CAT1 | OPTIC | 2026-02-01 | 1 | 1 |
| 131085 | Optic 8-Light Oval Pendant | CAT1 | OPTIC | 2026-05-01 | 1 | 1 |
| 131085 | Optic 8-Light Oval Pendant | CAT1 | OPTIC | 2026-06-01 | 1 | 1 |
| 131087 | Brindille 8-Light Linear Pendant | CAT1 | COL24 | 2026-01-01 | 1 | 1 |
| 131095 | Tura 7-Light Seeded Glass Pendant | CAT1 | TURA | 2025-12-01 | 2 | 2 |
| 131095 | Tura 7-Light Seeded Glass Pendant | CAT1 | TURA | 2026-05-01 | 1 | 1 |
| 131096 | — | — | — | 2025-12-01 | 1 | 1 |
| 131096 | — | — | — | 2026-02-01 | 2 | 2 |
| 131096 | — | — | — | 2026-03-01 | 2 | 2 |
| 131097 | Pangea 6-Light Linear Pendant | CAT1 | COL77 | 2026-02-01 | 3 | 3 |
| 131097 | Pangea 6-Light Linear Pendant | CAT1 | COL77 | 2026-05-01 | 3 | 3 |
| 131098 | Mika 10-Light Pendant | CAT1 | MIKA | 2026-03-01 | 1 | 1 |
| 131099 | Riza 9-Light Pendant | CAT1 | RIZA | 2026-03-01 | 1 | 1 |
| 131099 | Riza 9-Light Pendant | CAT1 | RIZA | 2026-04-01 | 1 | 1 |
| 131100 | Link 9-Light Blown Glass Pendant | CAT1 | LINK | 2026-01-01 | 1 | 1 |
| 131100 | Link 9-Light Blown Glass Pendant | CAT1 | LINK | 2026-04-01 | 1 | 1 |
| 131100 | Link 9-Light Blown Glass Pendant | CAT1 | LINK | 2026-05-01 | 1 | 1 |
| 131101 | Luma 9-Light Crystal Pendant | CAT1 | LUMA | 2026-01-01 | 2 | 2 |
| 131101 | Luma 9-Light Crystal Pendant | CAT1 | LUMA | 2026-02-01 | 1 | 1 |
| 131101 | Luma 9-Light Crystal Pendant | CAT1 | LUMA | 2026-04-01 | 6 | 7 |
| 131101 | Luma 9-Light Crystal Pendant | CAT1 | LUMA | 2026-05-01 | 1 | 1 |
| 131102 | Mobius 9-Light Pendant | CAT1 | COL14 | 2026-01-01 | 1 | 1 |
| 131103 | Ume 9-Light Pendant | CAT1 | UME | 2026-01-01 | 3 | 3 |
| 131103 | Ume 9-Light Pendant | CAT1 | UME | 2026-02-01 | 1 | 1 |
| 131103 | Ume 9-Light Pendant | CAT1 | UME | 2026-03-01 | 1 | 1 |
| 131103 | Ume 9-Light Pendant | CAT1 | UME | 2026-04-01 | 1 | 1 |
| 131104 | Exos Glass 9-Light Pendant | CAT1 | COL39 | 2026-01-01 | 1 | 1 |
| 131104 | Exos Glass 9-Light Pendant | CAT1 | COL39 | 2026-05-01 | 2 | 2 |
| 131105 | Brooklyn 9-Light Double Shade Pendant | CAT1 | COL2 | 2026-05-01 | 2 | 2 |
| 131105 | Brooklyn 9-Light Double Shade Pendant | CAT1 | COL2 | 2026-06-01 | 1 | 1 |
| 131107 | Tura 9-Light Seeded Glass Pendant | CAT1 | TURA | 2026-01-01 | 1 | 1 |
| 131107 | Tura 9-Light Seeded Glass Pendant | CAT1 | TURA | 2026-02-01 | 1 | 1 |
| 131107 | Tura 9-Light Seeded Glass Pendant | CAT1 | TURA | 2026-04-01 | 1 | 1 |
| 131107 | Tura 9-Light Seeded Glass Pendant | CAT1 | TURA | 2026-05-01 | 1 | 1 |
| 131108 | Link 9-Light Clear Glass Pendant | CAT1 | LINK | 2026-01-01 | 1 | 1 |
| 131109 | — | — | — | 2026-01-01 | 1 | 1 |
| 131120 | Link 5-Light Blown Glass Pendant | CAT1 | LINK | 2025-12-01 | 1 | 1 |
| 131120 | Link 5-Light Blown Glass Pendant | CAT1 | LINK | 2026-06-01 | 1 | 1 |
| 131121 | Luma 5-Light Pendant | CAT1 | LUMA | 2025-12-01 | 2 | 1 |
| 131121 | Luma 5-Light Pendant | CAT1 | LUMA | 2026-01-01 | 3 | 2 |
| 131121 | Luma 5-Light Pendant | CAT1 | LUMA | 2026-02-01 | 3 | 3 |
| 131121 | Luma 5-Light Pendant | CAT1 | LUMA | 2026-05-01 | 1 | 1 |
| 131121 | Luma 5-Light Pendant | CAT1 | LUMA | 2026-06-01 | 2 | 2 |
| 131122 | Mobius 5-Light Pendant | CAT1 | COL14 | 2026-01-01 | 1 | 1 |
| 131122 | Mobius 5-Light Pendant | CAT1 | COL14 | 2026-03-01 | 2 | 2 |
| 131123 | Ume 5-Light Pendant | CAT1 | UME | 2025-12-01 | 2 | 2 |
| 131123 | Ume 5-Light Pendant | CAT1 | UME | 2026-01-01 | 1 | 1 |
| 131123 | Ume 5-Light Pendant | CAT1 | UME | 2026-02-01 | 2 | 1 |
| 131123 | Ume 5-Light Pendant | CAT1 | UME | 2026-03-01 | 2 | 3 |
| 131123 | Ume 5-Light Pendant | CAT1 | UME | 2026-05-01 | 1 | 1 |
| 131124 | Exos Glass 5-Light Pendant | CAT1 | COL39 | 2025-12-01 | 1 | 1 |
| 131124 | Exos Glass 5-Light Pendant | CAT1 | COL39 | 2026-01-01 | 2 | 1 |
| 131124 | Exos Glass 5-Light Pendant | CAT1 | COL39 | 2026-02-01 | 4 | 4 |
| 131124 | Exos Glass 5-Light Pendant | CAT1 | COL39 | 2026-03-01 | 3 | 3 |
| 131124 | Exos Glass 5-Light Pendant | CAT1 | COL39 | 2026-05-01 | 2 | 2 |
| 131124 | Exos Glass 5-Light Pendant | CAT1 | COL39 | 2026-06-01 | 1 | 1 |
| 131125 | Brooklyn 5-Light Double Shade Pendant | CAT1 | COL2 | 2026-01-01 | 1 | 1 |
| 131125 | Brooklyn 5-Light Double Shade Pendant | CAT1 | COL2 | 2026-05-01 | 1 | 1 |
| 131125 | Brooklyn 5-Light Double Shade Pendant | CAT1 | COL2 | 2026-06-01 | 3 | 2 |
| 131126 | Tura 5-Light Seeded Glass Pendant | CAT1 | TURA | 2026-05-01 | 2 | 2 |
| 131127 | Link 5-Light Clear Glass Pendant | CAT1 | LINK | 2026-02-01 | 1 | 1 |
| 131127 | Link 5-Light Clear Glass Pendant | CAT1 | LINK | 2026-06-01 | 2 | 1 |
| 131128 | — | — | — | 2026-05-01 | 1 | 1 |
| 131129 | Riza 5-Light Pendant | CAT1 | RIZA | 2026-04-01 | 1 | 1 |
| 131129 | Riza 5-Light Pendant | CAT1 | RIZA | 2026-05-01 | 2 | 2 |
| 131130 | Fritz Globe 10-Light Pendant | CAT1 | FRITZ | 2026-02-01 | 1 | 1 |
| 131130 | Fritz Globe 10-Light Pendant | CAT1 | FRITZ | 2026-03-01 | 1 | 1 |
| 131131 | Fritz Globe 5-Light Pendant | CAT1 | FRITZ | 2026-02-01 | 2 | 2 |
| 131131 | Fritz Globe 5-Light Pendant | CAT1 | FRITZ | 2026-05-01 | 1 | 1 |
| 131131 | Fritz Globe 5-Light Pendant | CAT1 | FRITZ | 2026-06-01 | 2 | 1 |
| 131137 | Chrysalis 5-Light Small Crystal Pendant | CAT1 | COL86 | 2025-12-01 | 2 | 1 |
| 131137 | Chrysalis 5-Light Small Crystal Pendant | CAT1 | COL86 | 2026-01-01 | 1 | 1 |
| 131137 | Chrysalis 5-Light Small Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 3 | 1 |
| 131137 | Chrysalis 5-Light Small Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 2 | 1 |
| 131137 | Chrysalis 5-Light Small Crystal Pendant | CAT1 | COL86 | 2026-06-01 | 1 | 1 |
| 131138 | Chrysalis 5-Light Large Crystal Pendant | CAT1 | COL86 | 2025-12-01 | 1 | 1 |
| 131138 | Chrysalis 5-Light Large Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 3 | 4 |
| 131138 | Chrysalis 5-Light Large Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 1 | 1 |
| 131138 | Chrysalis 5-Light Large Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 1 | 1 |
| 131138 | Chrysalis 5-Light Large Crystal Pendant | CAT1 | COL86 | 2026-05-01 | 2 | 1 |
| 131139 | Chrysalis 5-Light Mixed Crystal Pendant | CAT1 | COL86 | 2025-12-01 | 1 | 1 |
| 131139 | Chrysalis 5-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-01-01 | 1 | 1 |
| 131139 | Chrysalis 5-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 3 | 3 |
| 131139 | Chrysalis 5-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 1 | 1 |
| 131139 | Chrysalis 5-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 9 | 5 |
| 131139 | Chrysalis 5-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-05-01 | 9 | 7 |
| 131140 | Chrysalis 9-Light Small Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 1 | 1 |
| 131140 | Chrysalis 9-Light Small Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 1 | 1 |
| 131141 | Chrysalis 9-Light Large Crystal Pendant | CAT1 | COL86 | 2025-12-01 | 1 | 1 |
| 131141 | Chrysalis 9-Light Large Crystal Pendant | CAT1 | COL86 | 2026-01-01 | 3 | 2 |
| 131141 | Chrysalis 9-Light Large Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 2 | 2 |
| 131141 | Chrysalis 9-Light Large Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 1 | 1 |
| 131141 | Chrysalis 9-Light Large Crystal Pendant | CAT1 | COL86 | 2026-05-01 | 3 | 3 |
| 131141 | Chrysalis 9-Light Large Crystal Pendant | CAT1 | COL86 | 2026-06-01 | 1 | 1 |
| 131142 | Chrysalis 9-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-01-01 | 4 | 3 |
| 131142 | Chrysalis 9-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 1 | 1 |
| 131142 | Chrysalis 9-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 1 | 1 |
| 131142 | Chrysalis 9-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 3 | 3 |
| 131142 | Chrysalis 9-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-05-01 | 1 | 1 |
| 131142 | Chrysalis 9-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-06-01 | 1 | 1 |
| 131143 | Chrysalis 10-Light Small Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 2 | 2 |
| 131143 | Chrysalis 10-Light Small Crystal Pendant | CAT1 | COL86 | 2026-05-01 | 1 | 1 |
| 131144 | Chrysalis 10-Light Large Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 1 | 1 |
| 131144 | Chrysalis 10-Light Large Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 2 | 4 |
| 131144 | Chrysalis 10-Light Large Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 4 | 1 |
| 131145 | Chrysalis 10-Light Mixed Crystal Pendant | CAT1 | COL86 | 2025-12-01 | 1 | 1 |
| 131145 | Chrysalis 10-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-01-01 | 1 | 1 |
| 131145 | Chrysalis 10-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-02-01 | 2 | 2 |
| 131145 | Chrysalis 10-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-03-01 | 1 | 1 |
| 131145 | Chrysalis 10-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-04-01 | 1 | 1 |
| 131145 | Chrysalis 10-Light Mixed Crystal Pendant | CAT1 | COL86 | 2026-05-01 | 3 | 3 |
| 131146 | Clouds 5-Light Pendant | CAT1 | COL79 | 2026-01-01 | 2 | 2 |
| 131146 | Clouds 5-Light Pendant | CAT1 | COL79 | 2026-02-01 | 4 | 3 |
| 131146 | Clouds 5-Light Pendant | CAT1 | COL79 | 2026-03-01 | 7 | 6 |
| 131146 | Clouds 5-Light Pendant | CAT1 | COL79 | 2026-04-01 | 2 | 2 |
| 131146 | Clouds 5-Light Pendant | CAT1 | COL79 | 2026-05-01 | 2 | 2 |
| 131146 | Clouds 5-Light Pendant | CAT1 | COL79 | 2026-06-01 | 2 | 2 |
| 131147 | Clouds 9-Light Pendant | CAT1 | COL79 | 2025-12-01 | 3 | 3 |
| 131147 | Clouds 9-Light Pendant | CAT1 | COL79 | 2026-01-01 | 6 | 6 |
| 131147 | Clouds 9-Light Pendant | CAT1 | COL79 | 2026-03-01 | 1 | 1 |
| 131147 | Clouds 9-Light Pendant | CAT1 | COL79 | 2026-04-01 | 2 | 2 |
| 131147 | Clouds 9-Light Pendant | CAT1 | COL79 | 2026-05-01 | 1 | 1 |
| 131148 | Clouds 10-Light Pendant | CAT1 | COL79 | 2025-12-01 | 1 | 1 |
| 131148 | Clouds 10-Light Pendant | CAT1 | COL79 | 2026-01-01 | 3 | 3 |
| 131148 | Clouds 10-Light Pendant | CAT1 | COL79 | 2026-02-01 | 2 | 2 |
| 131148 | Clouds 10-Light Pendant | CAT1 | COL79 | 2026-03-01 | 2 | 2 |
| 131148 | Clouds 10-Light Pendant | CAT1 | COL79 | 2026-05-01 | 1 | 2 |
| 131148 | Clouds 10-Light Pendant | CAT1 | COL79 | 2026-06-01 | 1 | 1 |
| 131149 | Link 10-Light Clear Glass Mobile Pendant | CAT1 | LINK | 2026-05-01 | 1 | 1 |
| 131150 | Link 10-Light Blown Glass Mobile Pendant | CAT1 | LINK | 2026-02-01 | 2 | 2 |
| 131151 | Fritz Globe 10-Light Mobile Pendant | CAT1 | FRITZ | 2025-12-01 | 1 | 1 |
| 131151 | Fritz Globe 10-Light Mobile Pendant | CAT1 | FRITZ | 2026-02-01 | 3 | 3 |
| 131151 | Fritz Globe 10-Light Mobile Pendant | CAT1 | FRITZ | 2026-04-01 | 1 | 1 |
| 131152 | Mobius 10-Light Mobile Pendant | CAT1 | COL14 | 2026-04-01 | 1 | 1 |
| 131152 | Mobius 10-Light Mobile Pendant | CAT1 | COL14 | 2026-05-01 | 1 | 1 |
| 131153 | Ume 10-Light Mobile Pendant | CAT1 | UME | 2025-12-01 | 1 | 1 |
| 131153 | Ume 10-Light Mobile Pendant | CAT1 | UME | 2026-02-01 | 1 | 1 |
| 131153 | Ume 10-Light Mobile Pendant | CAT1 | UME | 2026-03-01 | 1 | 1 |
| 131154 | Exos 10-Light Mobile Pendant | CAT1 | EXOS | 2025-12-01 | 2 | 2 |
| 131154 | Exos 10-Light Mobile Pendant | CAT1 | EXOS | 2026-03-01 | 1 | 1 |
| 131155 | Brooklyn 10-Light Double Shade Mobile Pendant | CAT1 | COL2 | 2026-01-01 | 4 | 4 |
| 131155 | Brooklyn 10-Light Double Shade Mobile Pendant | CAT1 | COL2 | 2026-03-01 | 3 | 2 |
| 131155 | Brooklyn 10-Light Double Shade Mobile Pendant | CAT1 | COL2 | 2026-04-01 | 1 | 1 |
| 131155 | Brooklyn 10-Light Double Shade Mobile Pendant | CAT1 | COL2 | 2026-05-01 | 1 | 1 |
| 131155 | Brooklyn 10-Light Double Shade Mobile Pendant | CAT1 | COL2 | 2026-06-01 | 1 | 1 |
| 131156 | Tura 10-Light Seeded Glass Mobile Pendant | CAT1 | TURA | 2025-12-01 | 1 | 1 |
| 131156 | Tura 10-Light Seeded Glass Mobile Pendant | CAT1 | TURA | 2026-02-01 | 1 | 1 |
| 131156 | Tura 10-Light Seeded Glass Mobile Pendant | CAT1 | TURA | 2026-06-01 | 1 | 1 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2025-12-01 | 4 | 3 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2026-01-01 | 1 | 1 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2026-02-01 | 4 | 4 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2026-03-01 | 6 | 5 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2026-04-01 | 5 | 4 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2026-05-01 | 4 | 4 |
| 131157 | Clouds 10-Light Mobile Pendant | CAT1 | COL79 | 2026-06-01 | 1 | 1 |
| 131158 | Riza 10-Light Mobile Pendant | CAT1 | RIZA | 2026-01-01 | 1 | 1 |
| 131158 | Riza 10-Light Mobile Pendant | CAT1 | RIZA | 2026-02-01 | 1 | 1 |
| 131158 | Riza 10-Light Mobile Pendant | CAT1 | RIZA | 2026-03-01 | 1 | 1 |
| 131159 | Chrysalis 10-Light Small Crystal Mobile Pendant | CAT1 | COL86 | 2026-01-01 | 1 | 1 |
| 131159 | Chrysalis 10-Light Small Crystal Mobile Pendant | CAT1 | COL86 | 2026-02-01 | 1 | 1 |
| 131159 | Chrysalis 10-Light Small Crystal Mobile Pendant | CAT1 | COL86 | 2026-04-01 | 4 | 4 |
| 131159 | Chrysalis 10-Light Small Crystal Mobile Pendant | CAT1 | COL86 | 2026-06-01 | 1 | 1 |
| 131160 | Tura 10-Light Frosted Glass Mobile Pendant | CAT1 | TURA | 2025-12-01 | 1 | 1 |
| 131160 | Tura 10-Light Frosted Glass Mobile Pendant | CAT1 | TURA | 2026-03-01 | 2 | 2 |
| 131161 | Lyric 5-Light Round Pendant | CAT1 | LYRIC | 2026-01-01 | 10 | 9 |
| 131161 | Lyric 5-Light Round Pendant | CAT1 | LYRIC | 2026-02-01 | 11 | 11 |
| 131161 | Lyric 5-Light Round Pendant | CAT1 | LYRIC | 2026-03-01 | 7 | 7 |
| 131161 | Lyric 5-Light Round Pendant | CAT1 | LYRIC | 2026-04-01 | 2 | 2 |
| 131161 | Lyric 5-Light Round Pendant | CAT1 | LYRIC | 2026-05-01 | 3 | 3 |
| 131162 | Lyric 7-Light Linear Pendant | CAT1 | LYRIC | 2026-01-01 | 6 | 6 |
| 131162 | Lyric 7-Light Linear Pendant | CAT1 | LYRIC | 2026-03-01 | 4 | 5 |
| 131162 | Lyric 7-Light Linear Pendant | CAT1 | LYRIC | 2026-04-01 | 4 | 3 |
| 131162 | Lyric 7-Light Linear Pendant | CAT1 | LYRIC | 2026-05-01 | 1 | 1 |
| 131163 | Lilium 5-Light Round Pendant | CAT1 | COL40 | 2026-01-01 | 1 | 1 |
| 131163 | Lilium 5-Light Round Pendant | CAT1 | COL40 | 2026-02-01 | 1 | 1 |
| 131163 | Lilium 5-Light Round Pendant | CAT1 | COL40 | 2026-03-01 | 3 | 3 |
| 131163 | Lilium 5-Light Round Pendant | CAT1 | COL40 | 2026-05-01 | 2 | 2 |
| 131164 | Lilium 9-Light Round Pendant | CAT1 | COL40 | 2026-01-01 | 1 | 1 |
| 131164 | Lilium 9-Light Round Pendant | CAT1 | COL40 | 2026-04-01 | 3 | 3 |
| 131164 | Lilium 9-Light Round Pendant | CAT1 | COL40 | 2026-05-01 | 1 | 1 |
| 131165 | Lilium 10-Light Linear Pendant | CAT1 | COL40 | 2026-02-01 | 3 | 3 |
| 131165 | Lilium 10-Light Linear Pendant | CAT1 | COL40 | 2026-03-01 | 2 | 2 |
| 131165 | Lilium 10-Light Linear Pendant | CAT1 | COL40 | 2026-05-01 | 3 | 3 |
| 131165 | Lilium 10-Light Linear Pendant | CAT1 | COL40 | 2026-06-01 | 1 | 1 |
| 131166 | Lilium 10-Light Mobile Pendant | CAT1 | COL40 | 2026-06-01 | 1 | 1 |
| 131200 | Link 10-Light Blown Glass Pendant | CAT1 | LINK | 2026-01-01 | 1 | 1 |
| 131200 | Link 10-Light Blown Glass Pendant | CAT1 | LINK | 2026-03-01 | 1 | 1 |
| 131200 | Link 10-Light Blown Glass Pendant | CAT1 | LINK | 2026-04-01 | 2 | 2 |
| 131200 | Link 10-Light Blown Glass Pendant | CAT1 | LINK | 2026-06-01 | 1 | 1 |
| 131201 | Luma 10-Light Crystal Pendant | CAT1 | LUMA | 2026-01-01 | 2 | 2 |
| 131201 | Luma 10-Light Crystal Pendant | CAT1 | LUMA | 2026-02-01 | 1 | 1 |
| 131201 | Luma 10-Light Crystal Pendant | CAT1 | LUMA | 2026-03-01 | 3 | 4 |
| 131201 | Luma 10-Light Crystal Pendant | CAT1 | LUMA | 2026-05-01 | 1 | 1 |
| 131202 | Mobius 10-Light Pendant | CAT1 | COL14 | 2026-05-01 | 1 | 1 |
| 131203 | Ume 10-Light Pendant | CAT1 | UME | 2026-01-01 | 1 | 1 |
| 131203 | Ume 10-Light Pendant | CAT1 | UME | 2026-03-01 | 1 | 1 |
| 131204 | Exos Glass 10-Light Pendant | CAT1 | COL39 | 2025-12-01 | 3 | 3 |
| 131204 | Exos Glass 10-Light Pendant | CAT1 | COL39 | 2026-04-01 | 1 | 1 |
| 131205 | Brooklyn 10-Light Double Shade Pendant | CAT1 | COL2 | 2026-03-01 | 1 | 1 |
| 131205 | Brooklyn 10-Light Double Shade Pendant | CAT1 | COL2 | 2026-06-01 | 3 | 2 |
| 131207 | Link 10-Light Clear Glass Pendant | CAT1 | LINK | 2025-12-01 | 1 | 1 |
| 131207 | Link 10-Light Clear Glass Pendant | CAT1 | LINK | 2026-03-01 | 1 | 1 |
| 131207 | Link 10-Light Clear Glass Pendant | CAT1 | LINK | 2026-04-01 | 1 | 1 |
| 131207 | Link 10-Light Clear Glass Pendant | CAT1 | LINK | 2026-05-01 | 1 | 1 |
| 131208 | Riza 10-Light Pendant | CAT1 | RIZA | 2026-01-01 | 1 | 1 |
| 131310 | Arc Lantern | CAT1 | ARC | 2025-12-01 | 6 | 4 |
| 131310 | Arc Lantern | CAT1 | ARC | 2026-01-01 | 20 | 13 |
| 131310 | Arc Lantern | CAT1 | ARC | 2026-02-01 | 16 | 11 |
| 131310 | Arc Lantern | CAT1 | ARC | 2026-03-01 | 18 | 13 |
| 131310 | Arc Lantern | CAT1 | ARC | 2026-04-01 | 13 | 7 |
| 131310 | Arc Lantern | CAT1 | ARC | 2026-05-01 | 16 | 13 |
| 131310 | Arc Lantern | CAT1 | ARC | 2026-06-01 | 5 | 3 |
| 131311 | Arc Linear Pendant | CAT1 | ARC | 2026-01-01 | 1 | 1 |
| 131311 | Arc Linear Pendant | CAT1 | ARC | 2026-02-01 | 2 | 2 |
| 131311 | Arc Linear Pendant | CAT1 | ARC | 2026-04-01 | 1 | 1 |
| 131311 | Arc Linear Pendant | CAT1 | ARC | 2026-05-01 | 4 | 4 |
| 131312 | Arc 8-Light Pendant | CAT1 | ARC | 2026-01-01 | 1 | 1 |
| 131312 | Arc 8-Light Pendant | CAT1 | ARC | 2026-02-01 | 3 | 3 |
| 131312 | Arc 8-Light Pendant | CAT1 | ARC | 2026-04-01 | 4 | 2 |
| 131312 | Arc 8-Light Pendant | CAT1 | ARC | 2026-05-01 | 1 | 1 |
| 131312 | Arc 8-Light Pendant | CAT1 | ARC | 2026-06-01 | 1 | 1 |
| 131313 | Arc 8-Light Tall Pendant | CAT1 | ARC | 2026-01-01 | 2 | 1 |
| 131313 | Arc 8-Light Tall Pendant | CAT1 | ARC | 2026-03-01 | 1 | 1 |
| 131313 | Arc 8-Light Tall Pendant | CAT1 | ARC | 2026-04-01 | 3 | 1 |
| 131313 | Arc 8-Light Tall Pendant | CAT1 | ARC | 2026-05-01 | 2 | 2 |
| 131313 | Arc 8-Light Tall Pendant | CAT1 | ARC | 2026-06-01 | 3 | 2 |
| 131321 | Luma 12-Light Starburst Pendant | CAT1 | LUMA | 2026-01-01 | 1 | 1 |
| 131410 | Flight 10-Light Small Pendant | CAT1 | COL81 | 2025-12-01 | 3 | 3 |
| 131410 | Flight 10-Light Small Pendant | CAT1 | COL81 | 2026-01-01 | 2 | 2 |
| 131410 | Flight 10-Light Small Pendant | CAT1 | COL81 | 2026-02-01 | 4 | 4 |
| 131410 | Flight 10-Light Small Pendant | CAT1 | COL81 | 2026-03-01 | 3 | 3 |
| 131410 | Flight 10-Light Small Pendant | CAT1 | COL81 | 2026-04-01 | 7 | 6 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2025-12-01 | 6 | 6 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2026-01-01 | 7 | 7 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2026-02-01 | 9 | 9 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2026-03-01 | 9 | 10 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2026-04-01 | 13 | 13 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2026-05-01 | 5 | 5 |
| 131412 | Flight 10-Light Pendant | CAT1 | COL81 | 2026-06-01 | 2 | 2 |
| 131500 | Astra Orb Small Pendant | CAT1 | ASTRA | 2025-12-01 | 6 | 3 |
| 131500 | Astra Orb Small Pendant | CAT1 | ASTRA | 2026-01-01 | 4 | 3 |
| 131500 | Astra Orb Small Pendant | CAT1 | ASTRA | 2026-02-01 | 7 | 4 |
| 131500 | Astra Orb Small Pendant | CAT1 | ASTRA | 2026-03-01 | 3 | 2 |
| 131500 | Astra Orb Small Pendant | CAT1 | ASTRA | 2026-04-01 | 2 | 2 |
| 131500 | Astra Orb Small Pendant | CAT1 | ASTRA | 2026-05-01 | 1 | 1 |
| 131503 | Astra Orb Large Pendant | CAT1 | ASTRA | 2025-12-01 | 1 | 1 |
| 131503 | Astra Orb Large Pendant | CAT1 | ASTRA | 2026-02-01 | 2 | 2 |
| 131503 | Astra Orb Large Pendant | CAT1 | ASTRA | 2026-03-01 | 1 | 1 |
| 131503 | Astra Orb Large Pendant | CAT1 | ASTRA | 2026-06-01 | 1 | 1 |
| 131525 | — | — | — | 2026-01-01 | 1 | 1 |
| 131540 | Cypress 5-Light Pendant | CAT1 | COL103 | 2026-02-01 | 2 | 2 |
| 131540 | Cypress 5-Light Pendant | CAT1 | COL103 | 2026-03-01 | 3 | 3 |
| 131540 | Cypress 5-Light Pendant | CAT1 | COL103 | 2026-06-01 | 1 | 1 |
| 131550 | Geo 4-Light Pendant | CAT1 | GEO | 2026-02-01 | 3 | 1 |
| 131550 | Geo 4-Light Pendant | CAT1 | GEO | 2026-03-01 | 8 | 3 |
| 131552 | Geo 6-Light Pendant | CAT1 | GEO | 2026-01-01 | 1 | 1 |
| 131552 | Geo 6-Light Pendant | CAT1 | GEO | 2026-02-01 | 1 | 1 |
| 131552 | Geo 6-Light Pendant | CAT1 | GEO | 2026-04-01 | 1 | 1 |
| 131552 | Geo 6-Light Pendant | CAT1 | GEO | 2026-05-01 | 1 | 1 |
| 131590 | Griffin Starburst Pendant | CAT1 | COL42 | 2025-12-01 | 2 | 2 |
| 131590 | Griffin Starburst Pendant | CAT1 | COL42 | 2026-01-01 | 1 | 1 |
| 131590 | Griffin Starburst Pendant | CAT1 | COL42 | 2026-03-01 | 2 | 2 |
| 131590 | Griffin Starburst Pendant | CAT1 | COL42 | 2026-05-01 | 1 | 1 |
| 131602 | Olympus Orb Pendant | CAT1 | COL7 | 2026-05-01 | 2 | 2 |
| 131606 | Olympus Vertical Pendant | CAT1 | COL7 | 2025-12-01 | 2 | 1 |
| 131606 | Olympus Vertical Pendant | CAT1 | COL7 | 2026-01-01 | 1 | 1 |
| 131606 | Olympus Vertical Pendant | CAT1 | COL7 | 2026-03-01 | 3 | 1 |
| 131610 | Ume Vertical Pendant | CAT1 | UME | 2025-12-01 | 4 | 2 |
| 131610 | Ume Vertical Pendant | CAT1 | UME | 2026-02-01 | 3 | 2 |
| 131610 | Ume Vertical Pendant | CAT1 | UME | 2026-03-01 | 6 | 3 |
| 131610 | Ume Vertical Pendant | CAT1 | UME | 2026-04-01 | 4 | 3 |
| 131610 | Ume Vertical Pendant | CAT1 | UME | 2026-05-01 | 3 | 2 |
| 131610 | Ume Vertical Pendant | CAT1 | UME | 2026-06-01 | 4 | 3 |
| 131611 | Brooklyn 4-Light Double Shade Vertical Pendant | CAT1 | COL2 | 2026-02-01 | 1 | 1 |
| 131611 | Brooklyn 4-Light Double Shade Vertical Pendant | CAT1 | COL2 | 2026-04-01 | 1 | 1 |
| 131611 | Brooklyn 4-Light Double Shade Vertical Pendant | CAT1 | COL2 | 2026-05-01 | 1 | 1 |
| 131612 | Gatsby 4-Light Vertical Pendant | CAT1 | COL35 | 2025-12-01 | 1 | 1 |
| 131612 | Gatsby 4-Light Vertical Pendant | CAT1 | COL35 | 2026-02-01 | 1 | 1 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | COL149 | 2026-01-01 | 5 | 5 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | COL149 | 2026-02-01 | 2 | 2 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | COL149 | 2026-03-01 | 1 | 1 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | COL149 | 2026-04-01 | 3 | 3 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | COL149 | 2026-05-01 | 2 | 2 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | COL149 | 2026-06-01 | 5 | 4 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | COL149 | 2026-01-01 | 7 | 7 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | COL149 | 2026-02-01 | 6 | 6 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | COL149 | 2026-03-01 | 12 | 9 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | COL149 | 2026-04-01 | 4 | 4 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | COL149 | 2026-05-01 | 2 | 2 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | COL149 | 2026-06-01 | 1 | 1 |
| 131623 | Truss 6-Arm Linear Chandelier | CAT1 | TRUSS | 2026-01-01 | 10 | 10 |
| 131623 | Truss 6-Arm Linear Chandelier | CAT1 | TRUSS | 2026-02-01 | 9 | 9 |
| 131623 | Truss 6-Arm Linear Chandelier | CAT1 | TRUSS | 2026-03-01 | 4 | 4 |
| 131623 | Truss 6-Arm Linear Chandelier | CAT1 | TRUSS | 2026-04-01 | 1 | 1 |
| 131623 | Truss 6-Arm Linear Chandelier | CAT1 | TRUSS | 2026-05-01 | 3 | 3 |
| 131624 | Truss 7-Arm Round Chandelier | CAT1 | TRUSS | 2026-01-01 | 2 | 2 |
| 131624 | Truss 7-Arm Round Chandelier | CAT1 | TRUSS | 2026-02-01 | 3 | 3 |
| 131624 | Truss 7-Arm Round Chandelier | CAT1 | TRUSS | 2026-03-01 | 1 | 1 |
| 131624 | Truss 7-Arm Round Chandelier | CAT1 | TRUSS | 2026-05-01 | 3 | 3 |
| 132043 | Summit Lantern | CAT1 | COL44 | 2025-12-01 | 1 | 1 |
| 132043 | Summit Lantern | CAT1 | COL44 | 2026-01-01 | 1 | 1 |
| 132043 | Summit Lantern | CAT1 | COL44 | 2026-02-01 | 1 | 1 |
| 132043 | Summit Lantern | CAT1 | COL44 | 2026-03-01 | 2 | 2 |
| 132043 | Summit Lantern | CAT1 | COL44 | 2026-04-01 | 3 | 1 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2025-12-01 | 1 | 1 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2026-01-01 | 2 | 2 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2026-02-01 | 2 | 2 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2026-03-01 | 11 | 5 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2026-04-01 | 1 | 1 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2026-05-01 | 7 | 8 |
| 132045 | Summit 8-Light Pendant | CAT1 | COL44 | 2026-06-01 | 4 | 4 |
| 132047 | Summit 12-Light Pendant | CAT1 | COL44 | 2026-01-01 | 7 | 2 |
| 132047 | Summit 12-Light Pendant | CAT1 | COL44 | 2026-02-01 | 2 | 2 |
| 132047 | Summit 12-Light Pendant | CAT1 | COL44 | 2026-03-01 | 2 | 2 |
| 132047 | Summit 12-Light Pendant | CAT1 | COL44 | 2026-04-01 | 1 | 1 |
| 132047 | Summit 12-Light Pendant | CAT1 | COL44 | 2026-05-01 | 1 | 2 |
| 132047 | Summit 12-Light Pendant | CAT1 | COL44 | 2026-06-01 | 1 | 1 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2025-12-01 | 11 | 10 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2026-01-01 | 31 | 31 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2026-02-01 | 25 | 23 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2026-03-01 | 26 | 24 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2026-04-01 | 15 | 15 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2026-05-01 | 46 | 22 |
| 132117 | Zen Pendant | CAT1 | ZEN | 2026-06-01 | 7 | 6 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2025-12-01 | 3 | 3 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2026-01-01 | 3 | 3 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2026-02-01 | 1 | 1 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2026-03-01 | 5 | 5 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2026-04-01 | 3 | 3 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2026-05-01 | 5 | 5 |
| 132160 | Waves Pendant | CAT1 | WAVES | 2026-06-01 | 5 | 5 |
| 132161 | Crest 6-Light Circular Pendant | CAT1 | CREST | 2026-01-01 | 2 | 2 |
| 132161 | Crest 6-Light Circular Pendant | CAT1 | CREST | 2026-02-01 | 4 | 4 |
| 132161 | Crest 6-Light Circular Pendant | CAT1 | CREST | 2026-03-01 | 2 | 2 |
| 132161 | Crest 6-Light Circular Pendant | CAT1 | CREST | 2026-04-01 | 3 | 3 |
| 132161 | Crest 6-Light Circular Pendant | CAT1 | CREST | 2026-05-01 | 1 | 1 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2025-12-01 | 5 | 5 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2026-01-01 | 2 | 2 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2026-02-01 | 5 | 5 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2026-03-01 | 5 | 6 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2026-04-01 | 11 | 12 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2026-05-01 | 6 | 6 |
| 133303 | Kirigami 3-Light Pendant | CAT1 | COL8 | 2026-06-01 | 4 | 4 |
| 133305 | Kirigami 4-Light Pendant | CAT1 | COL8 | 2026-01-01 | 1 | 1 |
| 133305 | Kirigami 4-Light Pendant | CAT1 | COL8 | 2026-02-01 | 3 | 4 |
| 133305 | Kirigami 4-Light Pendant | CAT1 | COL8 | 2026-03-01 | 1 | 1 |
| 133305 | Kirigami 4-Light Pendant | CAT1 | COL8 | 2026-04-01 | 3 | 3 |
| 133305 | Kirigami 4-Light Pendant | CAT1 | COL8 | 2026-05-01 | 2 | 1 |
| 133305 | Kirigami 4-Light Pendant | CAT1 | COL8 | 2026-06-01 | 1 | 1 |
| 134070 | Saratoga Oval Pendant | CAT1 | COL5 | 2025-12-01 | 2 | 2 |
| 134070 | Saratoga Oval Pendant | CAT1 | COL5 | 2026-01-01 | 9 | 6 |
| 134070 | Saratoga Oval Pendant | CAT1 | COL5 | 2026-02-01 | 4 | 4 |
| 134070 | Saratoga Oval Pendant | CAT1 | COL5 | 2026-03-01 | 8 | 8 |
| 134070 | Saratoga Oval Pendant | CAT1 | COL5 | 2026-04-01 | 3 | 3 |
| 134070 | Saratoga Oval Pendant | CAT1 | COL5 | 2026-05-01 | 8 | 6 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2025-12-01 | 6 | 5 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2026-01-01 | 5 | 5 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2026-02-01 | 6 | 6 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2026-03-01 | 5 | 5 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2026-04-01 | 4 | 4 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2026-05-01 | 2 | 3 |
| 134325 | Mackintosh Pendant | CAT1 | COL12 | 2026-06-01 | 3 | 3 |
| 134328 | Mackintosh Large Pendant | CAT1 | COL12 | 2025-12-01 | 1 | 1 |
| 134328 | Mackintosh Large Pendant | CAT1 | COL12 | 2026-01-01 | 1 | 1 |
| 134328 | Mackintosh Large Pendant | CAT1 | COL12 | 2026-02-01 | 6 | 7 |
| 134328 | Mackintosh Large Pendant | CAT1 | COL12 | 2026-03-01 | 6 | 6 |
| 134328 | Mackintosh Large Pendant | CAT1 | COL12 | 2026-04-01 | 5 | 5 |
| 134328 | Mackintosh Large Pendant | CAT1 | COL12 | 2026-05-01 | 4 | 4 |
| 134405 | Otto Sphere Pendant | CAT1 | OTTO | 2026-01-01 | 6 | 3 |
| 134405 | Otto Sphere Pendant | CAT1 | OTTO | 2026-05-01 | 6 | 4 |
| 134405 | Otto Sphere Pendant | CAT1 | OTTO | 2026-06-01 | 3 | 1 |
| 134409 | Otto Sphere 5-Light Pendant | CAT1 | OTTO | 2025-12-01 | 1 | 1 |
| 134409 | Otto Sphere 5-Light Pendant | CAT1 | OTTO | 2026-02-01 | 1 | 1 |
| 134409 | Otto Sphere 5-Light Pendant | CAT1 | OTTO | 2026-03-01 | 1 | 1 |
| 134409 | Otto Sphere 5-Light Pendant | CAT1 | OTTO | 2026-04-01 | 1 | 1 |
| 134409 | Otto Sphere 5-Light Pendant | CAT1 | OTTO | 2026-06-01 | 1 | 1 |
| 134410 | Sfera 6-Light Pendant | CAT1 | SFERA | 2026-02-01 | 2 | 1 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2025-12-01 | 10 | 5 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2026-01-01 | 13 | 8 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2026-02-01 | 9 | 7 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2026-03-01 | 14 | 10 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2026-04-01 | 19 | 13 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2026-05-01 | 23 | 14 |
| 134501 | Mobius Small Pendant | CAT1 | COL14 | 2026-06-01 | 12 | 6 |
| 134502 | Summit Pendant | CAT1 | COL44 | 2026-01-01 | 3 | 1 |
| 134502 | Summit Pendant | CAT1 | COL44 | 2026-02-01 | 7 | 4 |
| 134502 | Summit Pendant | CAT1 | COL44 | 2026-03-01 | 11 | 5 |
| 134502 | Summit Pendant | CAT1 | COL44 | 2026-04-01 | 10 | 4 |
| 134502 | Summit Pendant | CAT1 | COL44 | 2026-05-01 | 2 | 1 |
| 134502 | Summit Pendant | CAT1 | COL44 | 2026-06-01 | 3 | 1 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2025-12-01 | 1 | 1 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2026-01-01 | 11 | 11 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2026-02-01 | 9 | 9 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2026-03-01 | 16 | 15 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2026-04-01 | 9 | 8 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2026-05-01 | 15 | 12 |
| 134503 | Mobius Large Pendant | CAT1 | COL14 | 2026-06-01 | 6 | 5 |
| 134505 | Mobius Tall Pendant | CAT1 | COL14 | 2026-01-01 | 4 | 2 |
| 134505 | Mobius Tall Pendant | CAT1 | COL14 | 2026-02-01 | 7 | 5 |
| 134505 | Mobius Tall Pendant | CAT1 | COL14 | 2026-03-01 | 1 | 1 |
| 134505 | Mobius Tall Pendant | CAT1 | COL14 | 2026-04-01 | 3 | 1 |
| 134505 | Mobius Tall Pendant | CAT1 | COL14 | 2026-05-01 | 4 | 2 |
| 134505 | Mobius Tall Pendant | CAT1 | COL14 | 2026-06-01 | 2 | 1 |
| 134506 | Mobius 16-Light Orb Pendant | CAT1 | COL14 | 2025-12-01 | 1 | 1 |
| 134506 | Mobius 16-Light Orb Pendant | CAT1 | COL14 | 2026-02-01 | 2 | 2 |
| 134506 | Mobius 16-Light Orb Pendant | CAT1 | COL14 | 2026-04-01 | 1 | 1 |
| 134506 | Mobius 16-Light Orb Pendant | CAT1 | COL14 | 2026-05-01 | 1 | 1 |
| 134506 | Mobius 16-Light Orb Pendant | CAT1 | COL14 | 2026-06-01 | 2 | 2 |
| 134510 | Mobius 12-Light Pendant | CAT1 | COL14 | 2026-01-01 | 3 | 3 |
| 134510 | Mobius 12-Light Pendant | CAT1 | COL14 | 2026-02-01 | 4 | 4 |
| 134510 | Mobius 12-Light Pendant | CAT1 | COL14 | 2026-03-01 | 1 | 1 |
| 134510 | Mobius 12-Light Pendant | CAT1 | COL14 | 2026-04-01 | 2 | 2 |
| 134510 | Mobius 12-Light Pendant | CAT1 | COL14 | 2026-05-01 | 1 | 2 |
| 134510 | Mobius 12-Light Pendant | CAT1 | COL14 | 2026-06-01 | 2 | 2 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2025-12-01 | 11 | 4 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2026-01-01 | 10 | 5 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2026-02-01 | 10 | 5 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2026-03-01 | 3 | 3 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2026-04-01 | 6 | 3 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2026-05-01 | 10 | 5 |
| 134550 | Henry Medium Steel Shade Pendant | CAT1 | HENRY | 2026-06-01 | 3 | 1 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2025-12-01 | 5 | 3 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2026-01-01 | 5 | 4 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2026-02-01 | 13 | 6 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2026-03-01 | 7 | 4 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2026-04-01 | 8 | 3 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2026-05-01 | 8 | 3 |
| 134553 | Henry Medium Glass Shade Pendant | CAT1 | HENRY | 2026-06-01 | 11 | 5 |
| 135001 | Quill LED Pendant | CAT1 | QUILL | 2026-02-01 | 14 | 1 |
| 135001 | Quill LED Pendant | CAT1 | QUILL | 2026-03-01 | 5 | 3 |
| 135001 | Quill LED Pendant | CAT1 | QUILL | 2026-04-01 | 1 | 1 |
| 135001 | Quill LED Pendant | CAT1 | QUILL | 2026-05-01 | 1 | 1 |
| 135003 | Quill LED Pendant | CAT1 | QUILL | 2025-12-01 | 1 | 1 |
| 135003 | Quill LED Pendant | CAT1 | QUILL | 2026-02-01 | 1 | 1 |
| 135003 | Quill LED Pendant | CAT1 | QUILL | 2026-04-01 | 1 | 1 |
| 135003 | Quill LED Pendant | CAT1 | QUILL | 2026-05-01 | 1 | 1 |
| 135006 | — | — | — | 2026-03-01 | 2 | 1 |
| 135008 | — | — | — | 2026-02-01 | 1 | 1 |
| 135008 | — | — | — | 2026-03-01 | 1 | 1 |
| 136340 | Henry Pendant | CAT1 | HENRY | 2026-01-01 | 4 | 3 |
| 136340 | Henry Pendant | CAT1 | HENRY | 2026-03-01 | 18 | 7 |
| 136340 | Henry Pendant | CAT1 | HENRY | 2026-04-01 | 2 | 1 |
| 136340 | Henry Pendant | CAT1 | HENRY | 2026-05-01 | 2 | 2 |
| 136350 | Willow 6-Light Small Chandelier | CAT1 | COL28 | 2025-12-01 | 1 | 1 |
| 136350 | Willow 6-Light Small Chandelier | CAT1 | COL28 | 2026-01-01 | 2 | 2 |
| 136350 | Willow 6-Light Small Chandelier | CAT1 | COL28 | 2026-03-01 | 3 | 3 |
| 136350 | Willow 6-Light Small Chandelier | CAT1 | COL28 | 2026-05-01 | 2 | 2 |
| 136352 | Willow 6-Light Large Chandelier | CAT1 | COL28 | 2025-12-01 | 1 | 1 |
| 136352 | Willow 6-Light Large Chandelier | CAT1 | COL28 | 2026-01-01 | 1 | 1 |
| 136352 | Willow 6-Light Large Chandelier | CAT1 | COL28 | 2026-02-01 | 2 | 2 |
| 136352 | Willow 6-Light Large Chandelier | CAT1 | COL28 | 2026-03-01 | 1 | 1 |
| 136352 | Willow 6-Light Large Chandelier | CAT1 | COL28 | 2026-05-01 | 1 | 1 |
| 136357 | Ume 6-Light Large Pendant | CAT1 | UME | 2025-12-01 | 2 | 2 |
| 136357 | Ume 6-Light Large Pendant | CAT1 | UME | 2026-01-01 | 5 | 2 |
| 136357 | Ume 6-Light Large Pendant | CAT1 | UME | 2026-02-01 | 2 | 2 |
| 136357 | Ume 6-Light Large Pendant | CAT1 | UME | 2026-03-01 | 2 | 2 |
| 136357 | Ume 6-Light Large Pendant | CAT1 | UME | 2026-04-01 | 1 | 1 |
| 136357 | Ume 6-Light Large Pendant | CAT1 | UME | 2026-05-01 | 1 | 1 |
| 136385 | — | — | — | 2026-05-01 | 1 | 1 |
| 136390 | Etch Pendant | CAT1 | ETCH | 2025-12-01 | 1 | 1 |
| 136390 | Etch Pendant | CAT1 | ETCH | 2026-02-01 | 3 | 3 |
| 136390 | Etch Pendant | CAT1 | ETCH | 2026-03-01 | 4 | 3 |
| 136390 | Etch Pendant | CAT1 | ETCH | 2026-04-01 | 3 | 3 |
| 136390 | Etch Pendant | CAT1 | ETCH | 2026-05-01 | 5 | 4 |
| 136420 | Sprig Pendant | CAT1 | SPRIG | 2025-12-01 | 2 | 2 |
| 136420 | Sprig Pendant | CAT1 | SPRIG | 2026-02-01 | 8 | 5 |
| 136420 | Sprig Pendant | CAT1 | SPRIG | 2026-03-01 | 4 | 4 |
| 136420 | Sprig Pendant | CAT1 | SPRIG | 2026-04-01 | 7 | 5 |
| 136420 | Sprig Pendant | CAT1 | SPRIG | 2026-05-01 | 4 | 4 |
| 136420 | Sprig Pendant | CAT1 | SPRIG | 2026-06-01 | 4 | 3 |
| 136421 | Sprig Circular Pendant | CAT1 | SPRIG | 2026-02-01 | 4 | 3 |
| 136421 | Sprig Circular Pendant | CAT1 | SPRIG | 2026-03-01 | 4 | 4 |
| 136421 | Sprig Circular Pendant | CAT1 | SPRIG | 2026-04-01 | 1 | 1 |
| 136421 | Sprig Circular Pendant | CAT1 | SPRIG | 2026-05-01 | 2 | 2 |
| 136500 | Corona Small Pendant | CAT1 | COL26 | 2026-01-01 | 2 | 2 |
| 136500 | Corona Small Pendant | CAT1 | COL26 | 2026-02-01 | 2 | 3 |
| 136500 | Corona Small Pendant | CAT1 | COL26 | 2026-03-01 | 0 | 1 |
| 136500 | Corona Small Pendant | CAT1 | COL26 | 2026-04-01 | 4 | 3 |
| 136500 | Corona Small Pendant | CAT1 | COL26 | 2026-05-01 | 5 | 4 |
| 136500 | Corona Small Pendant | CAT1 | COL26 | 2026-06-01 | 1 | 1 |
| 136501 | Corona Pendant | CAT1 | COL26 | 2026-01-01 | 2 | 2 |
| 136501 | Corona Pendant | CAT1 | COL26 | 2026-02-01 | 1 | 1 |
| 136501 | Corona Pendant | CAT1 | COL26 | 2026-03-01 | 3 | 3 |
| 136501 | Corona Pendant | CAT1 | COL26 | 2026-04-01 | 3 | 4 |
| 136501 | Corona Pendant | CAT1 | COL26 | 2026-05-01 | 1 | 1 |
| 136501 | Corona Pendant | CAT1 | COL26 | 2026-06-01 | 2 | 2 |
| 136502 | Corona Brass Accent Pendant | CAT1 | COL26 | 2026-01-01 | 1 | 1 |
| 136502 | Corona Brass Accent Pendant | CAT1 | COL26 | 2026-02-01 | 2 | 2 |
| 136502 | Corona Brass Accent Pendant | CAT1 | COL26 | 2026-04-01 | 1 | 1 |
| 136502 | Corona Brass Accent Pendant | CAT1 | COL26 | 2026-05-01 | 2 | 2 |
| 136502 | Corona Brass Accent Pendant | CAT1 | COL26 | 2026-06-01 | 3 | 3 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2025-12-01 | 1 | 1 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2026-01-01 | 6 | 6 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2026-02-01 | 6 | 5 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2026-03-01 | 2 | 2 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2026-04-01 | 6 | 6 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2026-05-01 | 2 | 2 |
| 136505 | Corona Large Pendant | CAT1 | COL26 | 2026-06-01 | 3 | 3 |
| 136520 | Flux LED Pendant | CAT1 | FLUX | 2025-12-01 | 1 | 1 |
| 136520 | Flux LED Pendant | CAT1 | FLUX | 2026-01-01 | 1 | 1 |
| 136520 | Flux LED Pendant | CAT1 | FLUX | 2026-04-01 | 3 | 2 |
| 136520 | Flux LED Pendant | CAT1 | FLUX | 2026-05-01 | 1 | 1 |
| 136525 | Flux Large LED Pendant | CAT1 | FLUX | 2026-01-01 | 2 | 2 |
| 136525 | Flux Large LED Pendant | CAT1 | FLUX | 2026-02-01 | 2 | 2 |
| 136525 | Flux Large LED Pendant | CAT1 | FLUX | 2026-03-01 | 1 | 1 |
| 136525 | Flux Large LED Pendant | CAT1 | FLUX | 2026-05-01 | 1 | 1 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2025-12-01 | 2 | 1 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2026-01-01 | 1 | 1 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2026-02-01 | 2 | 2 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2026-03-01 | 2 | 2 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2026-04-01 | 5 | 4 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2026-05-01 | 1 | 1 |
| 136560 | Kiwi Pendant | CAT1 | KIWI | 2026-06-01 | 1 | 1 |
| 136570 | More Cowbell LED Pendant | CAT1 | COL52 | 2026-01-01 | 2 | 2 |
| 136570 | More Cowbell LED Pendant | CAT1 | COL52 | 2026-02-01 | 2 | 1 |
| 136570 | More Cowbell LED Pendant | CAT1 | COL52 | 2026-03-01 | 2 | 2 |
| 136570 | More Cowbell LED Pendant | CAT1 | COL52 | 2026-05-01 | 3 | 3 |
| 136605 | — | — | — | 2026-03-01 | 1 | 1 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2025-12-01 | 2 | 1 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2026-01-01 | 2 | 2 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2026-02-01 | 3 | 3 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2026-03-01 | 3 | 2 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2026-04-01 | 1 | 1 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2026-05-01 | 4 | 3 |
| 136753 | Impressions Pendant | CAT1 | COL22 | 2026-06-01 | 2 | 2 |
| 137462 | Atlas Large Pendant | CAT1 | ATLAS | 2025-12-01 | 4 | 1 |
| 137462 | Atlas Large Pendant | CAT1 | ATLAS | 2026-01-01 | 5 | 3 |
| 137462 | Atlas Large Pendant | CAT1 | ATLAS | 2026-03-01 | 7 | 2 |
| 137462 | Atlas Large Pendant | CAT1 | ATLAS | 2026-04-01 | 7 | 2 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2025-12-01 | 2 | 2 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2026-01-01 | 9 | 9 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2026-02-01 | 4 | 4 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2026-03-01 | 7 | 7 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2026-04-01 | 8 | 8 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2026-05-01 | 6 | 6 |
| 137525 | Arc Ellipse 5-Light Pendant | CAT1 | COL48 | 2026-06-01 | 4 | 4 |
| 137531 | — | — | — | 2026-01-01 | 1 | 1 |
| 137585 | Glissade LED Pendant | CAT1 | COL106 | 2026-02-01 | 1 | 1 |
| 137585 | Glissade LED Pendant | CAT1 | COL106 | 2026-05-01 | 1 | 1 |
| 137585 | Glissade LED Pendant | CAT1 | COL106 | 2026-06-01 | 3 | 1 |
| 137586 | Glissade Large LED Pendant | CAT1 | COL106 | 2026-01-01 | 1 | 1 |
| 137586 | Glissade Large LED Pendant | CAT1 | COL106 | 2026-02-01 | 2 | 2 |
| 137586 | Glissade Large LED Pendant | CAT1 | COL106 | 2026-03-01 | 1 | 1 |
| 137586 | Glissade Large LED Pendant | CAT1 | COL106 | 2026-06-01 | 1 | 1 |
| 137587 | Glissade Double Large LED Pendant | CAT1 | COL106 | 2026-01-01 | 1 | 1 |
| 137587 | Glissade Double Large LED Pendant | CAT1 | COL106 | 2026-05-01 | 2 | 2 |
| 137655 | Moreau Pendant | CAT1 | COL50 | 2025-12-01 | 2 | 2 |
| 137655 | Moreau Pendant | CAT1 | COL50 | 2026-01-01 | 3 | 3 |
| 137655 | Moreau Pendant | CAT1 | COL50 | 2026-02-01 | 2 | 3 |
| 137655 | Moreau Pendant | CAT1 | COL50 | 2026-03-01 | 3 | 3 |
| 137655 | Moreau Pendant | CAT1 | COL50 | 2026-04-01 | 3 | 3 |
| 137655 | Moreau Pendant | CAT1 | COL50 | 2026-05-01 | 1 | 1 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2025-12-01 | 0 | 1 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2026-01-01 | 8 | 8 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2026-02-01 | 7 | 7 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2026-03-01 | 11 | 10 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2026-04-01 | 5 | 5 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2026-05-01 | 10 | 10 |
| 137660 | Brindille Pendant | CAT1 | COL24 | 2026-06-01 | 2 | 2 |
| 137665 | Brindille Drum Shade Pendant | CAT1 | COL24 | 2025-12-01 | 1 | 1 |
| 137665 | Brindille Drum Shade Pendant | CAT1 | COL24 | 2026-01-01 | 0 | 1 |
| 137665 | Brindille Drum Shade Pendant | CAT1 | COL24 | 2026-02-01 | 7 | 7 |
| 137665 | Brindille Drum Shade Pendant | CAT1 | COL24 | 2026-03-01 | 4 | 4 |
| 137665 | Brindille Drum Shade Pendant | CAT1 | COL24 | 2026-04-01 | 3 | 3 |
| 137665 | Brindille Drum Shade Pendant | CAT1 | COL24 | 2026-05-01 | 3 | 4 |
| 137670 | Cavaletti Pendant | CAT1 | COL51 | 2025-12-01 | 2 | 2 |
| 137670 | Cavaletti Pendant | CAT1 | COL51 | 2026-01-01 | 2 | 2 |
| 137670 | Cavaletti Pendant | CAT1 | COL51 | 2026-02-01 | 2 | 2 |
| 137670 | Cavaletti Pendant | CAT1 | COL51 | 2026-03-01 | 5 | 5 |
| 137670 | Cavaletti Pendant | CAT1 | COL51 | 2026-04-01 | 3 | 3 |
| 137670 | Cavaletti Pendant | CAT1 | COL51 | 2026-05-01 | 4 | 4 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2025-12-01 | 1 | 1 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2026-01-01 | 1 | 1 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2026-02-01 | 2 | 2 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2026-03-01 | 2 | 2 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2026-04-01 | 1 | 1 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2026-05-01 | 2 | 2 |
| 137675 | Oceanus Pendant | CAT1 | COL21 | 2026-06-01 | 1 | 1 |
| 137680 | — | — | — | 2026-05-01 | 1 | 1 |
| 137687 | Folio LED Pendant | CAT1 | FOLIO | 2026-01-01 | 1 | 1 |
| 137687 | Folio LED Pendant | CAT1 | FOLIO | 2026-02-01 | 1 | 1 |
| 137687 | Folio LED Pendant | CAT1 | FOLIO | 2026-04-01 | 3 | 3 |
| 137687 | Folio LED Pendant | CAT1 | FOLIO | 2026-05-01 | 2 | 2 |
| 137687 | Folio LED Pendant | CAT1 | FOLIO | 2026-06-01 | 1 | 1 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2025-12-01 | 2 | 2 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2026-01-01 | 5 | 5 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2026-02-01 | 2 | 2 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2026-03-01 | 1 | 1 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2026-04-01 | 1 | 1 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2026-05-01 | 3 | 2 |
| 137689 | Folio Large LED Pendant | CAT1 | FOLIO | 2026-06-01 | 2 | 2 |
| 137720 | — | — | — | 2026-03-01 | 2 | 1 |
| 137725 | Erlenmeyer 5-Light Pendant | CAT1 | COL25 | 2025-12-01 | 1 | 1 |
| 137725 | Erlenmeyer 5-Light Pendant | CAT1 | COL25 | 2026-01-01 | 2 | 2 |
| 137725 | Erlenmeyer 5-Light Pendant | CAT1 | COL25 | 2026-02-01 | 3 | 3 |
| 137725 | Erlenmeyer 5-Light Pendant | CAT1 | COL25 | 2026-03-01 | 1 | 1 |
| 137725 | Erlenmeyer 5-Light Pendant | CAT1 | COL25 | 2026-04-01 | 1 | 1 |
| 137730 | Venn Pendant | CAT1 | VENN | 2025-12-01 | 6 | 2 |
| 137730 | Venn Pendant | CAT1 | VENN | 2026-01-01 | 3 | 2 |
| 137730 | Venn Pendant | CAT1 | VENN | 2026-02-01 | 15 | 7 |
| 137730 | Venn Pendant | CAT1 | VENN | 2026-03-01 | 11 | 6 |
| 137730 | Venn Pendant | CAT1 | VENN | 2026-04-01 | 9 | 4 |
| 137730 | Venn Pendant | CAT1 | VENN | 2026-05-01 | 9 | 5 |
| 137730 | Venn Pendant | CAT1 | VENN | 2026-06-01 | 2 | 1 |
| 137750 | Griffin Pendant | CAT1 | COL42 | 2026-01-01 | 1 | 1 |
| 137750 | Griffin Pendant | CAT1 | COL42 | 2026-02-01 | 1 | 1 |
| 137750 | Griffin Pendant | CAT1 | COL42 | 2026-04-01 | 1 | 1 |
| 137750 | Griffin Pendant | CAT1 | COL42 | 2026-05-01 | 1 | 1 |
| 137810 | Apothecary Pendant | CAT1 | COL34 | 2026-01-01 | 4 | 4 |
| 137810 | Apothecary Pendant | CAT1 | COL34 | 2026-02-01 | 2 | 2 |
| 137810 | Apothecary Pendant | CAT1 | COL34 | 2026-03-01 | 2 | 2 |
| 137820 | Graffiti Pendant | CAT1 | COL54 | 2025-12-01 | 1 | 1 |
| 137820 | Graffiti Pendant | CAT1 | COL54 | 2026-01-01 | 4 | 4 |
| 137820 | Graffiti Pendant | CAT1 | COL54 | 2026-02-01 | 6 | 6 |
| 137820 | Graffiti Pendant | CAT1 | COL54 | 2026-03-01 | 5 | 5 |
| 137820 | Graffiti Pendant | CAT1 | COL54 | 2026-04-01 | 2 | 2 |
| 137820 | Graffiti Pendant | CAT1 | COL54 | 2026-05-01 | 7 | 7 |
| 137840 | Nola Pendant | CAT1 | NOLA | 2025-12-01 | 1 | 1 |
| 137840 | Nola Pendant | CAT1 | NOLA | 2026-01-01 | 2 | 2 |
| 137840 | Nola Pendant | CAT1 | NOLA | 2026-03-01 | 2 | 2 |
| 137840 | Nola Pendant | CAT1 | NOLA | 2026-04-01 | 1 | 1 |
| 137840 | Nola Pendant | CAT1 | NOLA | 2026-05-01 | 2 | 2 |
| 137855 | Nest Pendant | CAT1 | NEST | 2025-12-01 | 3 | 2 |
| 137855 | Nest Pendant | CAT1 | NEST | 2026-01-01 | 2 | 2 |
| 137855 | Nest Pendant | CAT1 | NEST | 2026-02-01 | 6 | 5 |
| 137855 | Nest Pendant | CAT1 | NEST | 2026-03-01 | 4 | 4 |
| 137855 | Nest Pendant | CAT1 | NEST | 2026-04-01 | 2 | 2 |
| 137855 | Nest Pendant | CAT1 | NEST | 2026-05-01 | 8 | 8 |
| 137865 | Aerial Pendant | CAT1 | COL55 | 2026-01-01 | 1 | 1 |
| 137865 | Aerial Pendant | CAT1 | COL55 | 2026-04-01 | 1 | 1 |
| 137865 | Aerial Pendant | CAT1 | COL55 | 2026-06-01 | 1 | 1 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2025-12-01 | 2 | 2 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2026-01-01 | 2 | 2 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2026-02-01 | 12 | 4 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2026-03-01 | 2 | 2 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2026-04-01 | 1 | 1 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2026-05-01 | 2 | 2 |
| 138552 | Ondrian Pendant | CAT1 | COL56 | 2026-06-01 | 1 | 1 |
| 138573 | Vine Pendant | CAT1 | VINE | 2025-12-01 | 1 | 1 |
| 138573 | Vine Pendant | CAT1 | VINE | 2026-01-01 | 1 | 1 |
| 138573 | Vine Pendant | CAT1 | VINE | 2026-02-01 | 1 | 1 |
| 138573 | Vine Pendant | CAT1 | VINE | 2026-03-01 | 2 | 2 |
| 138573 | Vine Pendant | CAT1 | VINE | 2026-04-01 | 1 | 1 |
| 138573 | Vine Pendant | CAT1 | VINE | 2026-05-01 | 1 | 1 |
| 138585 | Aura Pendant | CAT1 | AURA | 2025-12-01 | 1 | 1 |
| 138585 | Aura Pendant | CAT1 | AURA | 2026-01-01 | 1 | 1 |
| 138585 | Aura Pendant | CAT1 | AURA | 2026-04-01 | 1 | 1 |
| 138585 | Aura Pendant | CAT1 | AURA | 2026-05-01 | 1 | 1 |
| 138588 | Aura Glass Pendant | CAT1 | AURA | 2025-12-01 | 3 | 2 |
| 138588 | Aura Glass Pendant | CAT1 | AURA | 2026-01-01 | 9 | 2 |
| 138588 | Aura Glass Pendant | CAT1 | AURA | 2026-02-01 | 5 | 1 |
| 138588 | Aura Glass Pendant | CAT1 | AURA | 2026-03-01 | 5 | 4 |
| 138588 | Aura Glass Pendant | CAT1 | AURA | 2026-04-01 | 5 | 5 |
| 138589 | Aura Large LED Pendant | CAT1 | AURA | 2026-01-01 | 2 | 1 |
| 138589 | Aura Large LED Pendant | CAT1 | AURA | 2026-02-01 | 4 | 4 |
| 138589 | Aura Large LED Pendant | CAT1 | AURA | 2026-03-01 | 3 | 2 |
| 138650 | — | — | — | 2026-01-01 | 1 | 1 |
| 138650 | — | — | — | 2026-02-01 | 11 | 1 |
| 138920 | Celesse Pendant | CAT1 | COL57 | 2026-01-01 | 1 | 1 |
| 138920 | Celesse Pendant | CAT1 | COL57 | 2026-02-01 | 1 | 1 |
| 138920 | Celesse Pendant | CAT1 | COL57 | 2026-04-01 | 1 | 1 |
| 138940 | Portico Pendant | CAT1 | COL128 | 2026-01-01 | 1 | 1 |
| 138940 | Portico Pendant | CAT1 | COL128 | 2026-02-01 | 1 | 1 |
| 138940 | Portico Pendant | CAT1 | COL128 | 2026-05-01 | 1 | 1 |
| 139050 | Abacus 5-Light LED Pendant | CAT1 | COL60 | 2025-12-01 | 1 | 1 |
| 139050 | Abacus 5-Light LED Pendant | CAT1 | COL60 | 2026-04-01 | 2 | 2 |
| 139050 | Abacus 5-Light LED Pendant | CAT1 | COL60 | 2026-05-01 | 1 | 1 |
| 139051 | Abacus 10-Light Square LED Pendant | CAT1 | COL60 | 2026-01-01 | 2 | 2 |
| 139051 | Abacus 10-Light Square LED Pendant | CAT1 | COL60 | 2026-02-01 | 1 | 1 |
| 139051 | Abacus 10-Light Square LED Pendant | CAT1 | COL60 | 2026-03-01 | 2 | 2 |
| 139051 | Abacus 10-Light Square LED Pendant | CAT1 | COL60 | 2026-04-01 | 2 | 2 |
| 139051 | Abacus 10-Light Square LED Pendant | CAT1 | COL60 | 2026-05-01 | 3 | 3 |
| 139051 | Abacus 10-Light Square LED Pendant | CAT1 | COL60 | 2026-06-01 | 1 | 1 |
| 139052 | Abacus 4-Light Round LED Pendant | CAT1 | COL60 | 2025-12-01 | 1 | 1 |
| 139052 | Abacus 4-Light Round LED Pendant | CAT1 | COL60 | 2026-01-01 | 1 | 1 |
| 139052 | Abacus 4-Light Round LED Pendant | CAT1 | COL60 | 2026-02-01 | 1 | 1 |
| 139052 | Abacus 4-Light Round LED Pendant | CAT1 | COL60 | 2026-03-01 | 2 | 2 |
| 139052 | Abacus 4-Light Round LED Pendant | CAT1 | COL60 | 2026-05-01 | 1 | 1 |
| 139054 | Abacus 7-Light Double Linear LED Pendant | CAT1 | COL60 | 2026-02-01 | 1 | 1 |
| 139054 | Abacus 7-Light Double Linear LED Pendant | CAT1 | COL60 | 2026-03-01 | 2 | 1 |
| 139054 | Abacus 7-Light Double Linear LED Pendant | CAT1 | COL60 | 2026-04-01 | 5 | 4 |
| 139055 | Abacus 6-Light LED Pendant | CAT1 | COL60 | 2026-01-01 | 1 | 1 |
| 139056 | Gatsby 9-Light LED Pendant | CAT1 | COL35 | 2026-02-01 | 1 | 1 |
| 139056 | Gatsby 9-Light LED Pendant | CAT1 | COL35 | 2026-03-01 | 1 | 1 |
| 139057 | Abacus 9-Light LED Pendant | CAT1 | COL60 | 2026-06-01 | 1 | 1 |
| 139058 | Gatsby 3-Light LED Pendant | CAT1 | COL35 | 2026-03-01 | 2 | 1 |
| 139059 | Abacus 3-Light LED Pendant | CAT1 | COL60 | 2026-02-01 | 2 | 2 |
| 139059 | Abacus 3-Light LED Pendant | CAT1 | COL60 | 2026-03-01 | 2 | 1 |
| 139059 | Abacus 3-Light LED Pendant | CAT1 | COL60 | 2026-04-01 | 1 | 1 |
| 139059 | Abacus 3-Light LED Pendant | CAT1 | COL60 | 2026-05-01 | 1 | 1 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2025-12-01 | 2 | 2 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2026-01-01 | 7 | 6 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2026-02-01 | 4 | 4 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2026-03-01 | 6 | 6 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2026-04-01 | 6 | 6 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2026-05-01 | 7 | 6 |
| 139201 | Slide Pendant | CAT1 | SLIDE | 2026-06-01 | 4 | 4 |
| 139202 | — | — | — | 2026-03-01 | 1 | 1 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2025-12-01 | 1 | 1 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2026-01-01 | 3 | 3 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2026-02-01 | 8 | 8 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2026-03-01 | 6 | 6 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2026-04-01 | 6 | 6 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2026-05-01 | 4 | 4 |
| 139203 | Slide XL 6-Light Pendant | CAT1 | SLIDE | 2026-06-01 | 5 | 4 |
| 139208 | Glacier 3-Light Pendant | CAT1 | COL49 | 2026-02-01 | 1 | 1 |
| 139208 | Glacier 3-Light Pendant | CAT1 | COL49 | 2026-06-01 | 1 | 1 |
| 139209 | Glacier XL 6-Light Pendant | CAT1 | COL49 | 2026-01-01 | 1 | 1 |
| 139209 | Glacier XL 6-Light Pendant | CAT1 | COL49 | 2026-04-01 | 1 | 1 |
| 139209 | Glacier XL 6-Light Pendant | CAT1 | COL49 | 2026-06-01 | 2 | 2 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2025-12-01 | 8 | 3 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2026-01-01 | 6 | 4 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2026-02-01 | 12 | 7 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2026-03-01 | 7 | 6 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2026-04-01 | 10 | 6 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2026-05-01 | 13 | 7 |
| 139450 | Hibiscus Small Pendant | CAT1 | COL61 | 2026-06-01 | 1 | 1 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2025-12-01 | 8 | 4 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2026-01-01 | 16 | 12 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2026-02-01 | 12 | 10 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2026-03-01 | 17 | 14 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2026-04-01 | 10 | 9 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2026-05-01 | 12 | 7 |
| 139455 | Hibiscus Large Pendant | CAT1 | COL61 | 2026-06-01 | 5 | 4 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2025-12-01 | 1 | 1 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2026-01-01 | 2 | 2 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2026-02-01 | 3 | 3 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2026-03-01 | 5 | 3 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2026-04-01 | 3 | 2 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2026-05-01 | 4 | 3 |
| 139460 | Hana Small Pendant | CAT1 | HANA | 2026-06-01 | 1 | 1 |
| 139465 | Hana Large Pendant | CAT1 | HANA | 2026-01-01 | 5 | 4 |
| 139465 | Hana Large Pendant | CAT1 | HANA | 2026-02-01 | 1 | 1 |
| 139465 | Hana Large Pendant | CAT1 | HANA | 2026-03-01 | 1 | 1 |
| 139590 | Exos Small Single Shade Pendant | CAT1 | EXOS | 2025-12-01 | 2 | 1 |
| 139590 | Exos Small Single Shade Pendant | CAT1 | EXOS | 2026-02-01 | 13 | 4 |
| 139590 | Exos Small Single Shade Pendant | CAT1 | EXOS | 2026-03-01 | 10 | 4 |
| 139590 | Exos Small Single Shade Pendant | CAT1 | EXOS | 2026-04-01 | 4 | 2 |
| 139590 | Exos Small Single Shade Pendant | CAT1 | EXOS | 2026-05-01 | 4 | 2 |
| 139600 | Exos Single Shade Pendant | CAT1 | EXOS | 2026-02-01 | 7 | 3 |
| 139600 | Exos Single Shade Pendant | CAT1 | EXOS | 2026-03-01 | 3 | 1 |
| 139600 | Exos Single Shade Pendant | CAT1 | EXOS | 2026-04-01 | 3 | 2 |
| 139600 | Exos Single Shade Pendant | CAT1 | EXOS | 2026-06-01 | 2 | 1 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2025-12-01 | 1 | 1 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2026-01-01 | 4 | 2 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2026-02-01 | 6 | 6 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2026-03-01 | 8 | 6 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2026-04-01 | 3 | 3 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2026-05-01 | 2 | 1 |
| 139602 | Exos Small Double Shade Pendant | CAT1 | EXOS | 2026-06-01 | 1 | 1 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2025-12-01 | 3 | 3 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2026-01-01 | 19 | 14 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2026-02-01 | 11 | 10 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2026-03-01 | 5 | 5 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2026-04-01 | 8 | 8 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2026-05-01 | 16 | 14 |
| 139605 | Exos Double Shade Pendant | CAT1 | EXOS | 2026-06-01 | 22 | 9 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2025-12-01 | 5 | 5 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2026-01-01 | 6 | 5 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2026-02-01 | 12 | 12 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2026-03-01 | 15 | 13 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2026-04-01 | 12 | 11 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2026-05-01 | 11 | 9 |
| 139610 | Exos Large Double Shade Pendant | CAT1 | EXOS | 2026-06-01 | 5 | 5 |
| 139630 | Exos Square Double Shade Pendant | CAT1 | EXOS | 2026-01-01 | 3 | 2 |
| 139630 | Exos Square Double Shade Pendant | CAT1 | EXOS | 2026-02-01 | 1 | 1 |
| 139630 | Exos Square Double Shade Pendant | CAT1 | EXOS | 2026-04-01 | 5 | 2 |
| 139630 | Exos Square Double Shade Pendant | CAT1 | EXOS | 2026-06-01 | 1 | 1 |
| 139635 | Exos Square Large Double Shade Pendant | CAT1 | EXOS | 2026-01-01 | 2 | 3 |
| 139635 | Exos Square Large Double Shade Pendant | CAT1 | EXOS | 2026-02-01 | 5 | 4 |
| 139635 | Exos Square Large Double Shade Pendant | CAT1 | EXOS | 2026-03-01 | 4 | 2 |
| 139635 | Exos Square Large Double Shade Pendant | CAT1 | EXOS | 2026-04-01 | 2 | 1 |
| 139635 | Exos Square Large Double Shade Pendant | CAT1 | EXOS | 2026-05-01 | 1 | 1 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2025-12-01 | 3 | 3 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2026-01-01 | 8 | 8 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2026-02-01 | 12 | 12 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2026-03-01 | 15 | 14 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2026-04-01 | 13 | 12 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2026-05-01 | 8 | 8 |
| 139640 | Exos Rectangular Pendant | CAT1 | EXOS | 2026-06-01 | 2 | 2 |
| 139652 | Hildene Large LED Pendant | CAT1 | COL62 | 2026-01-01 | 2 | 1 |
| 139652 | Hildene Large LED Pendant | CAT1 | COL62 | 2026-02-01 | 4 | 2 |
| 139652 | Hildene Large LED Pendant | CAT1 | COL62 | 2026-03-01 | 3 | 3 |
| 139653 | Hildene Circular LED Pendant | CAT1 | COL62 | 2026-01-01 | 3 | 1 |
| 139653 | Hildene Circular LED Pendant | CAT1 | COL62 | 2026-02-01 | 1 | 1 |
| 139653 | Hildene Circular LED Pendant | CAT1 | COL62 | 2026-03-01 | 6 | 1 |
| 139655 | Gossamer Large LED Pendant | CAT1 | COL63 | 2026-03-01 | 1 | 1 |
| 139655 | Gossamer Large LED Pendant | CAT1 | COL63 | 2026-04-01 | 1 | 1 |
| 139656 | Gossamer Circular LED Pendant | CAT1 | COL63 | 2026-01-01 | 1 | 1 |
| 139656 | Gossamer Circular LED Pendant | CAT1 | COL63 | 2026-03-01 | 1 | 1 |
| 139656 | Gossamer Circular LED Pendant | CAT1 | COL63 | 2026-04-01 | 1 | 1 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2025-12-01 | 1 | 1 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2026-01-01 | 4 | 4 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2026-02-01 | 3 | 3 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2026-03-01 | 3 | 3 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2026-04-01 | 6 | 6 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2026-05-01 | 3 | 3 |
| 139660 | Vitre Circular LED Pendant | CAT1 | VITRE | 2026-06-01 | 5 | 4 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2025-12-01 | 7 | 7 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2026-01-01 | 6 | 6 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2026-02-01 | 9 | 8 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2026-03-01 | 4 | 5 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2026-04-01 | 11 | 10 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2026-05-01 | 4 | 4 |
| 139661 | Vitre Large Linear LED Pendant | CAT1 | VITRE | 2026-06-01 | 5 | 5 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2025-12-01 | 2 | 2 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2026-01-01 | 15 | 15 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2026-02-01 | 8 | 8 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2026-03-01 | 6 | 6 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2026-04-01 | 10 | 8 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2026-05-01 | 4 | 5 |
| 139665 | Ardesia Circular LED Pendant | CAT1 | COL64 | 2026-06-01 | 5 | 5 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2025-12-01 | 6 | 6 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2026-01-01 | 8 | 8 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2026-02-01 | 8 | 9 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2026-03-01 | 18 | 15 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2026-04-01 | 8 | 7 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2026-05-01 | 10 | 10 |
| 139666 | Ardesia Linear LED Pendant | CAT1 | COL64 | 2026-06-01 | 7 | 7 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2025-12-01 | 4 | 4 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2026-01-01 | 7 | 6 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2026-02-01 | 8 | 8 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2026-03-01 | 12 | 11 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2026-04-01 | 10 | 11 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2026-05-01 | 11 | 10 |
| 139667 | Volterra Linear LED Pendant | CAT1 | COL102 | 2026-06-01 | 3 | 3 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2025-12-01 | 3 | 2 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2026-01-01 | 9 | 5 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2026-02-01 | 2 | 2 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2026-03-01 | 3 | 4 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2026-04-01 | 3 | 3 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2026-05-01 | 5 | 6 |
| 139668 | Volterra Circular LED Pendant | CAT1 | COL102 | 2026-06-01 | 3 | 3 |
| 139710 | Disq LED Pendant | CAT1 | DISQ | 2025-12-01 | 1 | 1 |
| 139710 | Disq LED Pendant | CAT1 | DISQ | 2026-04-01 | 2 | 1 |
| 139713 | Disq Large LED Pendant | CAT1 | DISQ | 2026-02-01 | 3 | 3 |
| 139713 | Disq Large LED Pendant | CAT1 | DISQ | 2026-03-01 | 2 | 1 |
| 139713 | Disq Large LED Pendant | CAT1 | DISQ | 2026-04-01 | 1 | 1 |
| 139713 | Disq Large LED Pendant | CAT1 | DISQ | 2026-05-01 | 2 | 2 |
| 139718 | Planar Small LED Pendant | CAT1 | COL65 | 2026-01-01 | 2 | 2 |
| 139718 | Planar Small LED Pendant | CAT1 | COL65 | 2026-02-01 | 9 | 6 |
| 139718 | Planar Small LED Pendant | CAT1 | COL65 | 2026-03-01 | 6 | 3 |
| 139718 | Planar Small LED Pendant | CAT1 | COL65 | 2026-04-01 | 3 | 3 |
| 139718 | Planar Small LED Pendant | CAT1 | COL65 | 2026-05-01 | 2 | 1 |
| 139718 | Planar Small LED Pendant | CAT1 | COL65 | 2026-06-01 | 1 | 1 |
| 139720 | Planar Large LED Pendant | CAT1 | COL65 | 2025-12-01 | 3 | 3 |
| 139720 | Planar Large LED Pendant | CAT1 | COL65 | 2026-01-01 | 1 | 1 |
| 139720 | Planar Large LED Pendant | CAT1 | COL65 | 2026-02-01 | 4 | 4 |
| 139720 | Planar Large LED Pendant | CAT1 | COL65 | 2026-03-01 | 2 | 2 |
| 139720 | Planar Large LED Pendant | CAT1 | COL65 | 2026-04-01 | 2 | 2 |
| 139720 | Planar Large LED Pendant | CAT1 | COL65 | 2026-05-01 | 1 | 1 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2025-12-01 | 1 | 1 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2026-01-01 | 8 | 8 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2026-02-01 | 7 | 7 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2026-03-01 | 4 | 4 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2026-04-01 | 4 | 3 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2026-05-01 | 8 | 8 |
| 139721 | Planar LED Pendant with Accent | CAT1 | COL65 | 2026-06-01 | 7 | 6 |
| 139725 | — | — | — | 2026-01-01 | 2 | 2 |
| 139726 | Cityscape Large LED Pendant | CAT1 | COL66 | 2026-01-01 | 9 | 9 |
| 139726 | Cityscape Large LED Pendant | CAT1 | COL66 | 2026-02-01 | 9 | 10 |
| 139726 | Cityscape Large LED Pendant | CAT1 | COL66 | 2026-03-01 | 3 | 3 |
| 139726 | Cityscape Large LED Pendant | CAT1 | COL66 | 2026-04-01 | 4 | 4 |
| 139726 | Cityscape Large LED Pendant | CAT1 | COL66 | 2026-05-01 | 7 | 7 |
| 139726 | Cityscape Large LED Pendant | CAT1 | COL66 | 2026-06-01 | 2 | 2 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2025-12-01 | 3 | 3 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2026-01-01 | 12 | 9 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2026-02-01 | 7 | 7 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2026-03-01 | 5 | 5 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2026-04-01 | 7 | 7 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2026-05-01 | 7 | 6 |
| 139727 | Landscape LED Pendant | CAT1 | COL67 | 2026-06-01 | 3 | 3 |
| 139730 | Switchback LED Pendant | CAT1 | COL68 | 2026-01-01 | 2 | 2 |
| 139730 | Switchback LED Pendant | CAT1 | COL68 | 2026-02-01 | 2 | 2 |
| 139730 | Switchback LED Pendant | CAT1 | COL68 | 2026-04-01 | 3 | 2 |
| 139730 | Switchback LED Pendant | CAT1 | COL68 | 2026-05-01 | 1 | 1 |
| 139738 | Solitude Large LED Pendant | CAT1 | COL69 | 2026-01-01 | 3 | 3 |
| 139738 | Solitude Large LED Pendant | CAT1 | COL69 | 2026-02-01 | 5 | 5 |
| 139738 | Solitude Large LED Pendant | CAT1 | COL69 | 2026-03-01 | 3 | 3 |
| 139738 | Solitude Large LED Pendant | CAT1 | COL69 | 2026-04-01 | 3 | 4 |
| 139738 | Solitude Large LED Pendant | CAT1 | COL69 | 2026-05-01 | 1 | 1 |
| 139738 | Solitude Large LED Pendant | CAT1 | COL69 | 2026-06-01 | 1 | 1 |
| 139752 | Spring LED Pendant | CAT1 | COL70 | 2025-12-01 | 1 | 1 |
| 139752 | Spring LED Pendant | CAT1 | COL70 | 2026-01-01 | 1 | 1 |
| 139752 | Spring LED Pendant | CAT1 | COL70 | 2026-02-01 | 1 | 1 |
| 139754 | Summer LED Pendant | CAT1 | COL70 | 2026-03-01 | 1 | 2 |
| 139756 | Autumn LED Pendant | CAT1 | COL70 | 2026-01-01 | 1 | 1 |
| 139756 | Autumn LED Pendant | CAT1 | COL70 | 2026-04-01 | 2 | 2 |
| 139756 | Autumn LED Pendant | CAT1 | COL70 | 2026-05-01 | 1 | 1 |
| 139772 | Anemone Circular LED Pendant | CAT1 | COL71 | 2026-01-01 | 1 | 1 |
| 139772 | Anemone Circular LED Pendant | CAT1 | COL71 | 2026-02-01 | 3 | 2 |
| 139772 | Anemone Circular LED Pendant | CAT1 | COL71 | 2026-03-01 | 2 | 2 |
| 139772 | Anemone Circular LED Pendant | CAT1 | COL71 | 2026-04-01 | 4 | 2 |
| 139778 | Cascade LED Pendant | CAT1 | COL72 | 2025-12-01 | 1 | 1 |
| 139778 | Cascade LED Pendant | CAT1 | COL72 | 2026-02-01 | 1 | 1 |
| 139778 | Cascade LED Pendant | CAT1 | COL72 | 2026-03-01 | 1 | 2 |
| 139778 | Cascade LED Pendant | CAT1 | COL72 | 2026-05-01 | 1 | 1 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2025-12-01 | 4 | 4 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2026-01-01 | 4 | 4 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2026-02-01 | 4 | 4 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2026-03-01 | 4 | 4 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2026-04-01 | 4 | 4 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2026-05-01 | 6 | 6 |
| 139780 | Solstice LED Pendant | CAT1 | COL73 | 2026-06-01 | 4 | 3 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2025-12-01 | 3 | 3 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2026-01-01 | 4 | 4 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2026-02-01 | 1 | 1 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2026-03-01 | 1 | 1 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2026-04-01 | 3 | 2 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2026-05-01 | 1 | 1 |
| 139782 | Solstice LED Tiered Pendant | CAT1 | COL73 | 2026-06-01 | 1 | 1 |
| 139812 | Lily LED Pendant | CAT1 | LILY | 2025-12-01 | 1 | 1 |
| 139812 | Lily LED Pendant | CAT1 | LILY | 2026-01-01 | 1 | 1 |
| 139812 | Lily LED Pendant | CAT1 | LILY | 2026-02-01 | 2 | 2 |
| 139812 | Lily LED Pendant | CAT1 | LILY | 2026-03-01 | 2 | 2 |
| 139812 | Lily LED Pendant | CAT1 | LILY | 2026-05-01 | 5 | 5 |
| 139812 | Lily LED Pendant | CAT1 | LILY | 2026-06-01 | 1 | 1 |
| 139813 | Belladonna LED Pendant | CAT1 | COL76 | 2026-01-01 | 5 | 4 |
| 139813 | Belladonna LED Pendant | CAT1 | COL76 | 2026-02-01 | 3 | 3 |
| 139813 | Belladonna LED Pendant | CAT1 | COL76 | 2026-06-01 | 3 | 1 |
| 139825 | Sling Pendant | CAT1 | SLING | 2025-12-01 | 1 | 1 |
| 139825 | Sling Pendant | CAT1 | SLING | 2026-01-01 | 7 | 2 |
| 139825 | Sling Pendant | CAT1 | SLING | 2026-04-01 | 3 | 1 |
| 139825 | Sling Pendant | CAT1 | SLING | 2026-05-01 | 2 | 2 |
| 139825 | Sling Pendant | CAT1 | SLING | 2026-06-01 | 1 | 1 |
| 139833 | Zephyr LED Pendant | CAT1 | COL78 | 2026-01-01 | 6 | 5 |
| 139833 | Zephyr LED Pendant | CAT1 | COL78 | 2026-02-01 | 4 | 4 |
| 139833 | Zephyr LED Pendant | CAT1 | COL78 | 2026-03-01 | 8 | 7 |
| 139833 | Zephyr LED Pendant | CAT1 | COL78 | 2026-04-01 | 5 | 4 |
| 139833 | Zephyr LED Pendant | CAT1 | COL78 | 2026-06-01 | 1 | 1 |
| 139845 | Mobius LED Mini Pendant | CAT13 | COL14 | 2026-01-01 | 3 | 1 |
| 139845 | Mobius LED Mini Pendant | CAT13 | COL14 | 2026-02-01 | 2 | 1 |
| 139845 | Mobius LED Mini Pendant | CAT13 | COL14 | 2026-03-01 | 1 | 1 |
| 139845 | Mobius LED Mini Pendant | CAT13 | COL14 | 2026-04-01 | 3 | 2 |
| 139845 | Mobius LED Mini Pendant | CAT13 | COL14 | 2026-06-01 | 2 | 1 |
| 139860 | Trove LED Pendant | CAT1 | TROVE | 2026-01-01 | 1 | 1 |
| 139860 | Trove LED Pendant | CAT1 | TROVE | 2026-02-01 | 1 | 1 |
| 139860 | Trove LED Pendant | CAT1 | TROVE | 2026-03-01 | 3 | 3 |
| 139860 | Trove LED Pendant | CAT1 | TROVE | 2026-04-01 | 2 | 2 |
| 139860 | Trove LED Pendant | CAT1 | TROVE | 2026-06-01 | 2 | 2 |
| 139861 | Trove LED Circular Pendant | CAT1 | TROVE | 2026-01-01 | 2 | 2 |
| 139861 | Trove LED Circular Pendant | CAT1 | TROVE | 2026-02-01 | 5 | 3 |
| 139861 | Trove LED Circular Pendant | CAT1 | TROVE | 2026-03-01 | 1 | 1 |
| 139861 | Trove LED Circular Pendant | CAT1 | TROVE | 2026-04-01 | 2 | 2 |
| 139901 | Tenon LED Pendant | CAT1 | TENON | 2025-12-01 | 1 | 1 |
| 139901 | Tenon LED Pendant | CAT1 | TENON | 2026-02-01 | 3 | 3 |
| 139901 | Tenon LED Pendant | CAT1 | TENON | 2026-04-01 | 1 | 1 |
| 139901 | Tenon LED Pendant | CAT1 | TENON | 2026-05-01 | 2 | 2 |
| 139901 | Tenon LED Pendant | CAT1 | TENON | 2026-06-01 | 0 | 1 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2025-12-01 | 2 | 2 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2026-01-01 | 1 | 1 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2026-02-01 | 2 | 2 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2026-03-01 | 6 | 6 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2026-04-01 | 2 | 2 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2026-05-01 | 3 | 3 |
| 139905 | Crossing Waves LED Pendant | CAT1 | COL80 | 2026-06-01 | 3 | 3 |
| 139910 | Cityscape Circular LED Pendant | CAT1 | COL66 | 2026-01-01 | 4 | 2 |
| 139910 | Cityscape Circular LED Pendant | CAT1 | COL66 | 2026-03-01 | 1 | 1 |
| 139910 | Cityscape Circular LED Pendant | CAT1 | COL66 | 2026-05-01 | 1 | 1 |
| 139910 | Cityscape Circular LED Pendant | CAT1 | COL66 | 2026-06-01 | 1 | 1 |
| 139915 | Solitude Circular LED Pendant | CAT1 | COL69 | 2025-12-01 | 2 | 2 |
| 139915 | Solitude Circular LED Pendant | CAT1 | COL69 | 2026-01-01 | 1 | 1 |
| 139915 | Solitude Circular LED Pendant | CAT1 | COL69 | 2026-02-01 | 4 | 4 |
| 139915 | Solitude Circular LED Pendant | CAT1 | COL69 | 2026-03-01 | 2 | 3 |
| 139915 | Solitude Circular LED Pendant | CAT1 | COL69 | 2026-04-01 | 1 | 3 |
| 139915 | Solitude Circular LED Pendant | CAT1 | COL69 | 2026-06-01 | 1 | 1 |
| 139920 | Plank LED Pendant | CAT1 | PLANK | 2025-12-01 | 1 | 1 |
| 139920 | Plank LED Pendant | CAT1 | PLANK | 2026-01-01 | 1 | 1 |
| 139920 | Plank LED Pendant | CAT1 | PLANK | 2026-02-01 | 2 | 2 |
| 139920 | Plank LED Pendant | CAT1 | PLANK | 2026-03-01 | 2 | 2 |
| 139920 | Plank LED Pendant | CAT1 | PLANK | 2026-04-01 | 2 | 2 |
| 139970 | Cairn Mini Pendant | CAT1 | CAIRN | 2026-01-01 | 7 | 5 |
| 139970 | Cairn Mini Pendant | CAT1 | CAIRN | 2026-02-01 | 10 | 6 |
| 139970 | Cairn Mini Pendant | CAT1 | CAIRN | 2026-03-01 | 13 | 10 |
| 139970 | Cairn Mini Pendant | CAT1 | CAIRN | 2026-04-01 | 13 | 5 |
| 139970 | Cairn Mini Pendant | CAT1 | CAIRN | 2026-05-01 | 13 | 10 |
| 139970 | Cairn Mini Pendant | CAT1 | CAIRN | 2026-06-01 | 8 | 4 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2025-12-01 | 6 | 3 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2026-01-01 | 17 | 8 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2026-02-01 | 17 | 12 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2026-03-01 | 21 | 13 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2026-04-01 | 19 | 10 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2026-05-01 | 18 | 12 |
| 139973 | Cairn Large Mini Pendant | CAT1 | CAIRN | 2026-06-01 | 3 | 2 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2025-12-01 | 4 | 4 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2026-01-01 | 5 | 5 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2026-02-01 | 4 | 4 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2026-03-01 | 5 | 5 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2026-04-01 | 1 | 2 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2026-05-01 | 5 | 5 |
| 139975 | Cairn Linear LED Pendant | CAT1 | CAIRN | 2026-06-01 | 2 | 2 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2025-12-01 | 2 | 1 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2026-01-01 | 11 | 9 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2026-02-01 | 8 | 8 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2026-03-01 | 6 | 5 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2026-04-01 | 1 | 2 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2026-05-01 | 9 | 9 |
| 139980 | Riverbed LED Pendant | CAT1 | COL91 | 2026-06-01 | 3 | 3 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2025-12-01 | 1 | 1 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2026-01-01 | 2 | 2 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2026-02-01 | 4 | 4 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2026-03-01 | 4 | 4 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2026-04-01 | 3 | 3 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2026-05-01 | 6 | 6 |
| 139982 | Riverbed Circular LED Pendant | CAT1 | COL91 | 2026-06-01 | 3 | 3 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2025-12-01 | 2 | 2 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2026-01-01 | 1 | 1 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2026-02-01 | 4 | 4 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2026-03-01 | 1 | 1 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2026-04-01 | 3 | 4 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2026-05-01 | 1 | 1 |
| 13CNMULT31 | 3-Light Linear Canopy | CAT1 | COL96 | 2026-06-01 | 2 | 2 |
| 13CNMULT32 | 3-Light Round Canopy | CAT1 | COL96 | 2026-01-01 | 3 | 3 |
| 13CNMULT32 | 3-Light Round Canopy | CAT1 | COL96 | 2026-02-01 | 6 | 6 |
| 13CNMULT32 | 3-Light Round Canopy | CAT1 | COL96 | 2026-03-01 | 1 | 2 |
| 13CNMULT32 | 3-Light Round Canopy | CAT1 | COL96 | 2026-04-01 | 6 | 5 |
| 13CNMULT32 | 3-Light Round Canopy | CAT1 | COL96 | 2026-05-01 | 2 | 2 |
| 13CNMULT32 | 3-Light Round Canopy | CAT1 | COL96 | 2026-06-01 | 1 | 1 |
| 144710 | Antasia Pendant | CAT1 | COL18 | 2025-12-01 | 1 | 1 |
| 144710 | Antasia Pendant | CAT1 | COL18 | 2026-01-01 | 3 | 3 |
| 144710 | Antasia Pendant | CAT1 | COL18 | 2026-03-01 | 1 | 1 |
| 144710 | Antasia Pendant | CAT1 | COL18 | 2026-04-01 | 4 | 2 |
| 144710 | Antasia Pendant | CAT1 | COL18 | 2026-05-01 | 3 | 3 |
| 151030 | — | — | — | 2026-04-01 | 1 | 1 |
| 151060 | Cowbell LED Mini Pendant | CAT13 | COL52 | 2026-01-01 | 1 | 1 |
| 151060 | Cowbell LED Mini Pendant | CAT13 | COL52 | 2026-03-01 | 11 | 2 |
| 151060 | Cowbell LED Mini Pendant | CAT13 | COL52 | 2026-04-01 | 2 | 2 |
| 151060 | Cowbell LED Mini Pendant | CAT13 | COL52 | 2026-05-01 | 6 | 2 |
| 151060 | Cowbell LED Mini Pendant | CAT13 | COL52 | 2026-06-01 | 6 | 2 |
| 161040 | Link Clear Glass Mini Pendant | CAT13 | LINK | 2026-01-01 | 10 | 3 |
| 161040 | Link Clear Glass Mini Pendant | CAT13 | LINK | 2026-03-01 | 6 | 2 |
| 161040 | Link Clear Glass Mini Pendant | CAT13 | LINK | 2026-04-01 | 9 | 2 |
| 161040 | Link Clear Glass Mini Pendant | CAT13 | LINK | 2026-05-01 | 8 | 3 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2025-12-01 | 3 | 2 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2026-01-01 | 2 | 1 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2026-02-01 | 5 | 2 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2026-03-01 | 6 | 2 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2026-04-01 | 4 | 2 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2026-05-01 | 2 | 1 |
| 161042 | Link Blown Glass Mini Pendant | CAT13 | LINK | 2026-06-01 | 7 | 2 |
| 161060 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-02-01 | 3 | 1 |
| 161060 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-03-01 | 3 | 1 |
| 161065 | Erlenmeyer Large Mini Pendant | CAT13 | COL25 | 2026-03-01 | 3 | 1 |
| 161180 | Exos Glass Mini Pendant | CAT13 | COL39 | 2025-12-01 | 2 | 2 |
| 161180 | Exos Glass Mini Pendant | CAT13 | COL39 | 2026-01-01 | 2 | 2 |
| 161180 | Exos Glass Mini Pendant | CAT13 | COL39 | 2026-02-01 | 7 | 3 |
| 161180 | Exos Glass Mini Pendant | CAT13 | COL39 | 2026-03-01 | 8 | 3 |
| 161180 | Exos Glass Mini Pendant | CAT13 | COL39 | 2026-04-01 | 6 | 3 |
| 161180 | Exos Glass Mini Pendant | CAT13 | COL39 | 2026-05-01 | 2 | 1 |
| 161181 | Mobius Mini Pendant | CAT13 | COL14 | 2026-01-01 | 10 | 2 |
| 161181 | Mobius Mini Pendant | CAT13 | COL14 | 2026-02-01 | 1 | 1 |
| 161181 | Mobius Mini Pendant | CAT13 | COL14 | 2026-03-01 | 2 | 1 |
| 161181 | Mobius Mini Pendant | CAT13 | COL14 | 2026-04-01 | 2 | 1 |
| 161182 | Ume Mini Pendant | CAT13 | UME | 2026-01-01 | 5 | 2 |
| 161182 | Ume Mini Pendant | CAT13 | UME | 2026-02-01 | 4 | 2 |
| 161182 | Ume Mini Pendant | CAT13 | UME | 2026-03-01 | 2 | 1 |
| 161182 | Ume Mini Pendant | CAT13 | UME | 2026-04-01 | 6 | 3 |
| 161182 | Ume Mini Pendant | CAT13 | UME | 2026-05-01 | 2 | 1 |
| 161183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2025-12-01 | 2 | 1 |
| 161183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-03-01 | 6 | 2 |
| 161183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-04-01 | 9 | 5 |
| 161183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-05-01 | 7 | 2 |
| 161183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-06-01 | 2 | 1 |
| 161184 | Tura Seeded Glass Mini Pendant | CAT13 | TURA | 2026-01-01 | 0 | 1 |
| 161184 | Tura Seeded Glass Mini Pendant | CAT13 | TURA | 2026-02-01 | 3 | 1 |
| 161184 | Tura Seeded Glass Mini Pendant | CAT13 | TURA | 2026-03-01 | 4 | 3 |
| 161184 | Tura Seeded Glass Mini Pendant | CAT13 | TURA | 2026-04-01 | 1 | 1 |
| 161184 | Tura Seeded Glass Mini Pendant | CAT13 | TURA | 2026-05-01 | 9 | 4 |
| 161184 | Tura Seeded Glass Mini Pendant | CAT13 | TURA | 2026-06-01 | 2 | 2 |
| 161185 | — | — | — | 2025-12-01 | 2 | 1 |
| 161185 | — | — | — | 2026-02-01 | 3 | 1 |
| 161185 | — | — | — | 2026-03-01 | 3 | 2 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2025-12-01 | 4 | 2 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2026-01-01 | 3 | 1 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2026-02-01 | 2 | 2 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2026-03-01 | 1 | 1 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2026-04-01 | 4 | 1 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2026-05-01 | 4 | 2 |
| 161186 | Riza Mini Pendant | CAT13 | RIZA | 2026-06-01 | 7 | 4 |
| 161187 | Fritz Globe 1-Light Mini Pendant | CAT13 | FRITZ | 2026-01-01 | 1 | 1 |
| 161187 | Fritz Globe 1-Light Mini Pendant | CAT13 | FRITZ | 2026-03-01 | 2 | 1 |
| 161187 | Fritz Globe 1-Light Mini Pendant | CAT13 | FRITZ | 2026-05-01 | 2 | 1 |
| 161188 | Chrysalis 1-Light Small Pendant | CAT13 | COL86 | 2025-12-01 | 5 | 3 |
| 161188 | Chrysalis 1-Light Small Pendant | CAT13 | COL86 | 2026-01-01 | 4 | 3 |
| 161188 | Chrysalis 1-Light Small Pendant | CAT13 | COL86 | 2026-03-01 | 3 | 4 |
| 161188 | Chrysalis 1-Light Small Pendant | CAT13 | COL86 | 2026-04-01 | 9 | 3 |
| 161188 | Chrysalis 1-Light Small Pendant | CAT13 | COL86 | 2026-05-01 | 11 | 5 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2025-12-01 | 1 | 1 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2026-01-01 | 8 | 4 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2026-02-01 | 10 | 5 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2026-03-01 | 10 | 6 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2026-04-01 | 17 | 8 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2026-05-01 | 11 | 6 |
| 161189 | Chrysalis 1-Light Large Pendant | CAT13 | COL86 | 2026-06-01 | 9 | 2 |
| 161190 | Clouds Mini Pendant | CAT13 | COL79 | 2025-12-01 | 4 | 2 |
| 161190 | Clouds Mini Pendant | CAT13 | COL79 | 2026-02-01 | 5 | 2 |
| 161190 | Clouds Mini Pendant | CAT13 | COL79 | 2026-03-01 | 5 | 3 |
| 161190 | Clouds Mini Pendant | CAT13 | COL79 | 2026-05-01 | 11 | 6 |
| 161191 | Lyric 1-Light Pendant | CAT13 | LYRIC | 2026-01-01 | 11 | 9 |
| 161191 | Lyric 1-Light Pendant | CAT13 | LYRIC | 2026-02-01 | 16 | 16 |
| 161191 | Lyric 1-Light Pendant | CAT13 | LYRIC | 2026-03-01 | 16 | 11 |
| 161191 | Lyric 1-Light Pendant | CAT13 | LYRIC | 2026-04-01 | 9 | 5 |
| 161191 | Lyric 1-Light Pendant | CAT13 | LYRIC | 2026-05-01 | 14 | 9 |
| 161191 | Lyric 1-Light Pendant | CAT13 | LYRIC | 2026-06-01 | 8 | 3 |
| 161192 | Lilium Mini Pendant | CAT13 | COL40 | 2026-01-01 | 1 | 1 |
| 161192 | Lilium Mini Pendant | CAT13 | COL40 | 2026-02-01 | 28 | 9 |
| 161192 | Lilium Mini Pendant | CAT13 | COL40 | 2026-03-01 | 4 | 2 |
| 161192 | Lilium Mini Pendant | CAT13 | COL40 | 2026-04-01 | 5 | 2 |
| 161192 | Lilium Mini Pendant | CAT13 | COL40 | 2026-05-01 | 7 | 3 |
| 161305 | Otto Sphere Mini Pendant | CAT13 | OTTO | 2026-01-01 | 5 | 3 |
| 161305 | Otto Sphere Mini Pendant | CAT13 | OTTO | 2026-02-01 | 3 | 1 |
| 161305 | Otto Sphere Mini Pendant | CAT13 | OTTO | 2026-03-01 | 3 | 3 |
| 161305 | Otto Sphere Mini Pendant | CAT13 | OTTO | 2026-04-01 | 1 | 1 |
| 161305 | Otto Sphere Mini Pendant | CAT13 | OTTO | 2026-05-01 | 11 | 4 |
| 161305 | Otto Sphere Mini Pendant | CAT13 | OTTO | 2026-06-01 | 1 | 1 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2025-12-01 | 6 | 4 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2026-01-01 | 12 | 6 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2026-02-01 | 18 | 6 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2026-03-01 | 23 | 7 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2026-04-01 | 14 | 6 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2026-05-01 | 22 | 10 |
| 161321 | Luma Mini Pendant | CAT13 | LUMA | 2026-06-01 | 5 | 3 |
| 181061 | Gatsby 1-Light Mini Pendant | CAT13 | COL35 | 2025-12-01 | 2 | 1 |
| 181061 | Gatsby 1-Light Mini Pendant | CAT13 | COL35 | 2026-01-01 | 7 | 4 |
| 181061 | Gatsby 1-Light Mini Pendant | CAT13 | COL35 | 2026-02-01 | 4 | 3 |
| 181061 | Gatsby 1-Light Mini Pendant | CAT13 | COL35 | 2026-05-01 | 2 | 1 |
| 181070 | Mika 2-Light Pendant | CAT13 | MIKA | 2026-03-01 | 3 | 1 |
| 181070 | Mika 2-Light Pendant | CAT13 | MIKA | 2026-04-01 | 7 | 3 |
| 181070 | Mika 2-Light Pendant | CAT13 | MIKA | 2026-05-01 | 3 | 2 |
| 181070 | Mika 2-Light Pendant | CAT13 | MIKA | 2026-06-01 | 2 | 1 |
| 181072 | Pangea 1-Light Pendant | CAT13 | COL77 | 2025-12-01 | 3 | 1 |
| 181072 | Pangea 1-Light Pendant | CAT13 | COL77 | 2026-01-01 | 2 | 1 |
| 181072 | Pangea 1-Light Pendant | CAT13 | COL77 | 2026-03-01 | 5 | 3 |
| 181072 | Pangea 1-Light Pendant | CAT13 | COL77 | 2026-06-01 | 6 | 2 |
| 181183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2025-12-01 | 4 | 2 |
| 181183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-02-01 | 6 | 3 |
| 181183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-03-01 | 7 | 3 |
| 181183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-04-01 | 9 | 5 |
| 181183 | Brooklyn Double Shade Mini Pendant | CAT13 | COL2 | 2026-05-01 | 2 | 2 |
| 181184 | Brooklyn Double Shade Art Glass Mini Pendant | CAT13 | COL2 | 2026-03-01 | 10 | 1 |
| 181540 | Cypress 1-Light Pendant | CAT13 | COL103 | 2026-01-01 | 2 | 1 |
| 181540 | Cypress 1-Light Pendant | CAT13 | COL103 | 2026-02-01 | 12 | 3 |
| 181540 | Cypress 1-Light Pendant | CAT13 | COL103 | 2026-03-01 | 11 | 5 |
| 181540 | Cypress 1-Light Pendant | CAT13 | COL103 | 2026-04-01 | 14 | 6 |
| 181540 | Cypress 1-Light Pendant | CAT13 | COL103 | 2026-05-01 | 10 | 5 |
| 181540 | Cypress 1-Light Pendant | CAT13 | COL103 | 2026-06-01 | 4 | 3 |
| 181542 | — | — | — | 2026-05-01 | 0 | 1 |
| 181601 | Kora Mini Pendant | CAT13 | KORA | 2026-01-01 | 8 | 6 |
| 181601 | Kora Mini Pendant | CAT13 | KORA | 2026-02-01 | 17 | 7 |
| 181601 | Kora Mini Pendant | CAT13 | KORA | 2026-03-01 | 1 | 1 |
| 181601 | Kora Mini Pendant | CAT13 | KORA | 2026-04-01 | 2 | 1 |
| 181601 | Kora Mini Pendant | CAT13 | KORA | 2026-05-01 | 12 | 5 |
| 181601 | Kora Mini Pendant | CAT13 | KORA | 2026-06-01 | 6 | 2 |
| 181602 | Kora Pendant | CAT13 | KORA | 2026-01-01 | 1 | 1 |
| 181602 | Kora Pendant | CAT13 | KORA | 2026-02-01 | 2 | 2 |
| 181602 | Kora Pendant | CAT13 | KORA | 2026-03-01 | 1 | 1 |
| 181602 | Kora Pendant | CAT13 | KORA | 2026-04-01 | 5 | 3 |
| 181602 | Kora Pendant | CAT13 | KORA | 2026-06-01 | 3 | 1 |
| 181603 | Trilogy Mini Pendant | CAT13 | COL150 | 2026-01-01 | 10 | 8 |
| 181603 | Trilogy Mini Pendant | CAT13 | COL150 | 2026-02-01 | 17 | 14 |
| 181603 | Trilogy Mini Pendant | CAT13 | COL150 | 2026-03-01 | 10 | 5 |
| 181603 | Trilogy Mini Pendant | CAT13 | COL150 | 2026-04-01 | 4 | 2 |
| 181603 | Trilogy Mini Pendant | CAT13 | COL150 | 2026-05-01 | 6 | 4 |
| 181603 | Trilogy Mini Pendant | CAT13 | COL150 | 2026-06-01 | 5 | 2 |
| 181604 | Spire Mini Pendant | CAT13 | SPIRE | 2026-01-01 | 6 | 6 |
| 181604 | Spire Mini Pendant | CAT13 | SPIRE | 2026-02-01 | 4 | 4 |
| 181604 | Spire Mini Pendant | CAT13 | SPIRE | 2026-03-01 | 3 | 3 |
| 181604 | Spire Mini Pendant | CAT13 | SPIRE | 2026-04-01 | 3 | 1 |
| 181604 | Spire Mini Pendant | CAT13 | SPIRE | 2026-05-01 | 3 | 1 |
| 181604 | Spire Mini Pendant | CAT13 | SPIRE | 2026-06-01 | 11 | 5 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2025-12-01 | 6 | 3 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2026-01-01 | 10 | 5 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2026-02-01 | 4 | 2 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2026-03-01 | 7 | 3 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2026-04-01 | 4 | 2 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2026-05-01 | 6 | 4 |
| 182640 | Trumpet Mini Pendant | CAT13 | COL89 | 2026-06-01 | 4 | 2 |
| 182660 | Twining Leaf Mini Pendant | CAT13 | LEAF | 2026-01-01 | 1 | 1 |
| 182660 | Twining Leaf Mini Pendant | CAT13 | LEAF | 2026-03-01 | 4 | 2 |
| 182660 | Twining Leaf Mini Pendant | CAT13 | LEAF | 2026-04-01 | 2 | 1 |
| 182660 | Twining Leaf Mini Pendant | CAT13 | LEAF | 2026-05-01 | 9 | 3 |
| 182660 | Twining Leaf Mini Pendant | CAT13 | LEAF | 2026-06-01 | 1 | 1 |
| 183030 | Flora Down Light Mini Pendant | CAT13 | FLORA | 2025-12-01 | 5 | 2 |
| 183030 | Flora Down Light Mini Pendant | CAT13 | FLORA | 2026-01-01 | 14 | 3 |
| 183030 | Flora Down Light Mini Pendant | CAT13 | FLORA | 2026-02-01 | 6 | 2 |
| 183030 | Flora Down Light Mini Pendant | CAT13 | FLORA | 2026-03-01 | 11 | 4 |
| 183030 | Flora Down Light Mini Pendant | CAT13 | FLORA | 2026-04-01 | 7 | 3 |
| 183030 | Flora Down Light Mini Pendant | CAT13 | FLORA | 2026-05-01 | 3 | 2 |
| 183050 | Flora Up Light Mini Pendant | CAT13 | FLORA | 2026-01-01 | 3 | 2 |
| 183050 | Flora Up Light Mini Pendant | CAT13 | FLORA | 2026-03-01 | 3 | 2 |
| 183050 | Flora Up Light Mini Pendant | CAT13 | FLORA | 2026-04-01 | 6 | 1 |
| 183050 | Flora Up Light Mini Pendant | CAT13 | FLORA | 2026-05-01 | 11 | 5 |
| 183550 | Paralline Mini Pendant | CAT13 | COL90 | 2026-01-01 | 4 | 3 |
| 183550 | Paralline Mini Pendant | CAT13 | COL90 | 2026-02-01 | 6 | 3 |
| 183550 | Paralline Mini Pendant | CAT13 | COL90 | 2026-05-01 | 3 | 2 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2025-12-01 | 10 | 4 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2026-01-01 | 4 | 2 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2026-02-01 | 8 | 6 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2026-03-01 | 4 | 3 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2026-04-01 | 7 | 3 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2026-05-01 | 4 | 2 |
| 184250 | Henry Mini Pendant | CAT13 | HENRY | 2026-06-01 | 3 | 2 |
| 184251 | Henry with Chamfer Pendant | CAT13 | HENRY | 2026-02-01 | 1 | 1 |
| 184251 | Henry with Chamfer Pendant | CAT13 | HENRY | 2026-03-01 | 2 | 1 |
| 184251 | Henry with Chamfer Pendant | CAT13 | HENRY | 2026-04-01 | 3 | 2 |
| 184253 | Henry Mini Pendant | CAT13 | HENRY | 2025-12-01 | 2 | 1 |
| 184253 | Henry Mini Pendant | CAT13 | HENRY | 2026-01-01 | 9 | 3 |
| 184253 | Henry Mini Pendant | CAT13 | HENRY | 2026-02-01 | 15 | 6 |
| 184253 | Henry Mini Pendant | CAT13 | HENRY | 2026-03-01 | 11 | 4 |
| 184253 | Henry Mini Pendant | CAT13 | HENRY | 2026-04-01 | 3 | 2 |
| 184253 | Henry Mini Pendant | CAT13 | HENRY | 2026-05-01 | 11 | 5 |
| 184350 | Dahlia Mini Pendant | CAT13 | COL13 | 2026-01-01 | 3 | 3 |
| 184350 | Dahlia Mini Pendant | CAT13 | COL13 | 2026-02-01 | 3 | 3 |
| 184350 | Dahlia Mini Pendant | CAT13 | COL13 | 2026-03-01 | 4 | 4 |
| 184350 | Dahlia Mini Pendant | CAT13 | COL13 | 2026-04-01 | 1 | 1 |
| 184350 | Dahlia Mini Pendant | CAT13 | COL13 | 2026-05-01 | 1 | 1 |
| 184350 | Dahlia Mini Pendant | CAT13 | COL13 | 2026-06-01 | 3 | 3 |
| 184500 | Mobius Steel Shade Mini Pendant | CAT13 | COL14 | 2026-01-01 | 8 | 4 |
| 184500 | Mobius Steel Shade Mini Pendant | CAT13 | COL14 | 2026-02-01 | 1 | 1 |
| 184500 | Mobius Steel Shade Mini Pendant | CAT13 | COL14 | 2026-03-01 | 2 | 1 |
| 184500 | Mobius Steel Shade Mini Pendant | CAT13 | COL14 | 2026-05-01 | 4 | 2 |
| 184500 | Mobius Steel Shade Mini Pendant | CAT13 | COL14 | 2026-06-01 | 2 | 1 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2025-12-01 | 2 | 1 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2026-01-01 | 6 | 3 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2026-02-01 | 3 | 2 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2026-03-01 | 15 | 10 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2026-04-01 | 12 | 6 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2026-05-01 | 3 | 1 |
| 184530 | Mobius Mini Pendant | CAT13 | COL14 | 2026-06-01 | 2 | 1 |
| 184930 | Staccato Mini Pendant | CAT13 | COL85 | 2025-12-01 | 3 | 1 |
| 184930 | Staccato Mini Pendant | CAT13 | COL85 | 2026-03-01 | 11 | 6 |
| 184930 | Staccato Mini Pendant | CAT13 | COL85 | 2026-04-01 | 5 | 2 |
| 184970 | Staccato Large Mini Pendant | CAT13 | COL85 | 2025-12-01 | 3 | 2 |
| 184970 | Staccato Large Mini Pendant | CAT13 | COL85 | 2026-01-01 | 12 | 6 |
| 184970 | Staccato Large Mini Pendant | CAT13 | COL85 | 2026-02-01 | 8 | 4 |
| 184970 | Staccato Large Mini Pendant | CAT13 | COL85 | 2026-03-01 | 15 | 6 |
| 184970 | Staccato Large Mini Pendant | CAT13 | COL85 | 2026-05-01 | 14 | 7 |
| 184970 | Staccato Large Mini Pendant | CAT13 | COL85 | 2026-06-01 | 1 | 1 |
| 185400 | Fullered Impressions Mini Pendant | CAT13 | COL29 | 2026-01-01 | 6 | 3 |
| 185400 | Fullered Impressions Mini Pendant | CAT13 | COL29 | 2026-02-01 | 10 | 5 |
| 185400 | Fullered Impressions Mini Pendant | CAT13 | COL29 | 2026-03-01 | 12 | 5 |
| 185400 | Fullered Impressions Mini Pendant | CAT13 | COL29 | 2026-04-01 | 3 | 1 |
| 185400 | Fullered Impressions Mini Pendant | CAT13 | COL29 | 2026-05-01 | 3 | 2 |
| 186400 | Axis Mini Pendant | CAT13 | AXIS | 2025-12-01 | 4 | 1 |
| 186400 | Axis Mini Pendant | CAT13 | AXIS | 2026-01-01 | 1 | 1 |
| 186400 | Axis Mini Pendant | CAT13 | AXIS | 2026-02-01 | 3 | 2 |
| 186400 | Axis Mini Pendant | CAT13 | AXIS | 2026-03-01 | 11 | 4 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2025-12-01 | 1 | 1 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2026-01-01 | 1 | 1 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2026-02-01 | 3 | 1 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2026-03-01 | 9 | 4 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2026-04-01 | 7 | 4 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2026-05-01 | 1 | 1 |
| 186500 | Corona Mini Pendant | CAT13 | COL26 | 2026-06-01 | 2 | 1 |
| 186530 | Corona Large Mini Pendant | CAT13 | COL26 | 2026-01-01 | 2 | 2 |
| 186530 | Corona Large Mini Pendant | CAT13 | COL26 | 2026-02-01 | 7 | 4 |
| 186530 | Corona Large Mini Pendant | CAT13 | COL26 | 2026-03-01 | 9 | 4 |
| 186530 | Corona Large Mini Pendant | CAT13 | COL26 | 2026-04-01 | 0 | 1 |
| 186530 | Corona Large Mini Pendant | CAT13 | COL26 | 2026-05-01 | 5 | 3 |
| 186530 | Corona Large Mini Pendant | CAT13 | COL26 | 2026-06-01 | 4 | 3 |
| 186600 | Wren Mini Pendant | CAT13 | WREN | 2025-12-01 | 3 | 1 |
| 186600 | Wren Mini Pendant | CAT13 | WREN | 2026-03-01 | 1 | 1 |
| 186600 | Wren Mini Pendant | CAT13 | WREN | 2026-04-01 | 4 | 1 |
| 186600 | Wren Mini Pendant | CAT13 | WREN | 2026-05-01 | 7 | 2 |
| 186600 | Wren Mini Pendant | CAT13 | WREN | 2026-06-01 | 3 | 1 |
| 186670 | Brindille Mini Pendant | CAT13 | COL24 | 2025-12-01 | 3 | 1 |
| 186670 | Brindille Mini Pendant | CAT13 | COL24 | 2026-01-01 | 5 | 3 |
| 186670 | Brindille Mini Pendant | CAT13 | COL24 | 2026-02-01 | 4 | 2 |
| 186670 | Brindille Mini Pendant | CAT13 | COL24 | 2026-04-01 | 2 | 2 |
| 186670 | Brindille Mini Pendant | CAT13 | COL24 | 2026-05-01 | 4 | 1 |
| 186670 | Brindille Mini Pendant | CAT13 | COL24 | 2026-06-01 | 2 | 1 |
| 187000 | — | — | — | 2026-01-01 | 6 | 1 |
| 187100 | Erlenmeyer Small Mini Pendant | CAT13 | COL25 | 2025-12-01 | 2 | 1 |
| 187100 | Erlenmeyer Small Mini Pendant | CAT13 | COL25 | 2026-02-01 | 6 | 2 |
| 187100 | Erlenmeyer Small Mini Pendant | CAT13 | COL25 | 2026-03-01 | 11 | 2 |
| 187100 | Erlenmeyer Small Mini Pendant | CAT13 | COL25 | 2026-05-01 | 18 | 4 |
| 187100 | Erlenmeyer Small Mini Pendant | CAT13 | COL25 | 2026-06-01 | 2 | 1 |
| 187150 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-01-01 | 3 | 3 |
| 187150 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-02-01 | 4 | 2 |
| 187150 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-03-01 | 3 | 2 |
| 187150 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-04-01 | 6 | 2 |
| 187150 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-05-01 | 6 | 2 |
| 187150 | Erlenmeyer Mini Pendant | CAT13 | COL25 | 2026-06-01 | 2 | 1 |
| 187200 | Erlenmeyer Large Mini Pendant | CAT13 | COL25 | 2026-01-01 | 4 | 2 |
| 187200 | Erlenmeyer Large Mini Pendant | CAT13 | COL25 | 2026-05-01 | 1 | 1 |
| 187200 | Erlenmeyer Large Mini Pendant | CAT13 | COL25 | 2026-06-01 | 3 | 1 |
| 187250 | Apparatus Mini Pendant | CAT13 | COL92 | 2025-12-01 | 5 | 1 |
| 187250 | Apparatus Mini Pendant | CAT13 | COL92 | 2026-01-01 | 2 | 1 |
| 187250 | Apparatus Mini Pendant | CAT13 | COL92 | 2026-02-01 | 1 | 1 |
| 187250 | Apparatus Mini Pendant | CAT13 | COL92 | 2026-03-01 | 2 | 1 |
| 187250 | Apparatus Mini Pendant | CAT13 | COL92 | 2026-04-01 | 1 | 1 |
| 187300 | Cuff Small Mini Pendant | CAT13 | CUFF | 2025-12-01 | 3 | 1 |
| 187300 | Cuff Small Mini Pendant | CAT13 | CUFF | 2026-02-01 | 5 | 2 |
| 187300 | Cuff Small Mini Pendant | CAT13 | CUFF | 2026-03-01 | 2 | 1 |
| 187300 | Cuff Small Mini Pendant | CAT13 | CUFF | 2026-04-01 | 3 | 1 |
| 187300 | Cuff Small Mini Pendant | CAT13 | CUFF | 2026-05-01 | 3 | 1 |
| 187300 | Cuff Small Mini Pendant | CAT13 | CUFF | 2026-06-01 | 2 | 1 |
| 187330 | Cuff Mini Pendant | CAT13 | CUFF | 2026-01-01 | 5 | 2 |
| 187330 | Cuff Mini Pendant | CAT13 | CUFF | 2026-02-01 | 4 | 2 |
| 187330 | Cuff Mini Pendant | CAT13 | CUFF | 2026-03-01 | 8 | 4 |
| 187330 | Cuff Mini Pendant | CAT13 | CUFF | 2026-04-01 | 1 | 1 |
| 187330 | Cuff Mini Pendant | CAT13 | CUFF | 2026-05-01 | 2 | 1 |
| 187330 | Cuff Mini Pendant | CAT13 | CUFF | 2026-06-01 | 5 | 3 |
| 187340 | Cuff Large Mini Pendant | CAT13 | CUFF | 2026-01-01 | 2 | 1 |
| 187340 | Cuff Large Mini Pendant | CAT13 | CUFF | 2026-02-01 | 4 | 3 |
| 187340 | Cuff Large Mini Pendant | CAT13 | CUFF | 2026-03-01 | 2 | 1 |
| 187340 | Cuff Large Mini Pendant | CAT13 | CUFF | 2026-04-01 | 3 | 1 |
| 187340 | Cuff Large Mini Pendant | CAT13 | CUFF | 2026-06-01 | 4 | 1 |
| 187420 | — | — | — | 2026-02-01 | 3 | 1 |
| 187440 | Rhythm Mini Pendant | CAT13 | COL45 | 2025-12-01 | 3 | 1 |
| 187440 | Rhythm Mini Pendant | CAT13 | COL45 | 2026-01-01 | 3 | 1 |
| 187440 | Rhythm Mini Pendant | CAT13 | COL45 | 2026-02-01 | 7 | 2 |
| 187440 | Rhythm Mini Pendant | CAT13 | COL45 | 2026-03-01 | 3 | 1 |
| 187440 | Rhythm Mini Pendant | CAT13 | COL45 | 2026-05-01 | 2 | 2 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2025-12-01 | 8 | 2 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2026-01-01 | 7 | 3 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2026-02-01 | 5 | 2 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2026-03-01 | 9 | 5 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2026-04-01 | 7 | 3 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2026-05-01 | 11 | 5 |
| 187460 | Atlas Pendant | CAT13 | ATLAS | 2026-06-01 | 2 | 1 |
| 187462 | Atlas Small Pendant | CAT13 | ATLAS | 2025-12-01 | 10 | 1 |
| 187462 | Atlas Small Pendant | CAT13 | ATLAS | 2026-01-01 | 6 | 2 |
| 187462 | Atlas Small Pendant | CAT13 | ATLAS | 2026-03-01 | 3 | 1 |
| 187462 | Atlas Small Pendant | CAT13 | ATLAS | 2026-04-01 | 3 | 1 |
| 187462 | Atlas Small Pendant | CAT13 | ATLAS | 2026-05-01 | 2 | 1 |
| 187465 | Dane Lantern | CAT13 | DANE | 2026-02-01 | 1 | 1 |
| 187465 | Dane Lantern | CAT13 | DANE | 2026-04-01 | 2 | 1 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2025-12-01 | 13 | 6 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2026-01-01 | 40 | 17 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2026-02-01 | 48 | 25 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2026-03-01 | 52 | 23 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2026-04-01 | 16 | 10 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2026-05-01 | 29 | 13 |
| 187468 | Vaso Pendant | CAT13 | VASO | 2026-06-01 | 4 | 2 |
| 187510 | — | — | — | 2026-03-01 | 2 | 1 |
| 187520 | Apothecary Mini Pendant | CAT13 | COL34 | 2026-02-01 | 1 | 1 |
| 187520 | Apothecary Mini Pendant | CAT13 | COL34 | 2026-03-01 | 3 | 2 |
| 187520 | Apothecary Mini Pendant | CAT13 | COL34 | 2026-04-01 | 2 | 1 |
| 187520 | Apothecary Mini Pendant | CAT13 | COL34 | 2026-05-01 | 3 | 2 |
| 187650 | Exos Small Mini Pendant | CAT13 | COL39 | 2026-01-01 | 2 | 1 |
| 187650 | Exos Small Mini Pendant | CAT13 | COL39 | 2026-02-01 | 6 | 2 |
| 187650 | Exos Small Mini Pendant | CAT13 | COL39 | 2026-03-01 | 11 | 4 |
| 187650 | Exos Small Mini Pendant | CAT13 | COL39 | 2026-04-01 | 4 | 1 |
| 187650 | Exos Small Mini Pendant | CAT13 | COL39 | 2026-05-01 | 5 | 2 |
| 187650 | Exos Small Mini Pendant | CAT13 | COL39 | 2026-06-01 | 1 | 1 |
| 187660 | Exos Large Mini Pendant | CAT13 | COL39 | 2026-01-01 | 8 | 4 |
| 187660 | Exos Large Mini Pendant | CAT13 | COL39 | 2026-02-01 | 10 | 5 |
| 187660 | Exos Large Mini Pendant | CAT13 | COL39 | 2026-03-01 | 8 | 5 |
| 187660 | Exos Large Mini Pendant | CAT13 | COL39 | 2026-04-01 | 8 | 3 |
| 187660 | Exos Large Mini Pendant | CAT13 | COL39 | 2026-05-01 | 4 | 2 |
| 187910 | Airis Small Mini Pendant | CAT13 | AIRIS | 2026-02-01 | 7 | 2 |
| 187910 | Airis Small Mini Pendant | CAT13 | AIRIS | 2026-05-01 | 7 | 3 |
| 187910 | Airis Small Mini Pendant | CAT13 | AIRIS | 2026-06-01 | 2 | 1 |
| 187930 | Airis Medium Mini Pendant | CAT13 | AIRIS | 2026-02-01 | 4 | 1 |
| 187930 | Airis Medium Mini Pendant | CAT13 | AIRIS | 2026-05-01 | 5 | 2 |
| 188100 | Exos Delta Mini Pendant | CAT13 | COL39 | 2026-02-01 | 2 | 1 |
| 188100 | Exos Delta Mini Pendant | CAT13 | COL39 | 2026-03-01 | 2 | 1 |
| 188100 | Exos Delta Mini Pendant | CAT13 | COL39 | 2026-06-01 | 1 | 1 |
| 188200 | Arc Ellipse Mini Pendant | CAT13 | COL48 | 2025-12-01 | 4 | 1 |
| 188200 | Arc Ellipse Mini Pendant | CAT13 | COL48 | 2026-02-01 | 3 | 1 |
| 188200 | Arc Ellipse Mini Pendant | CAT13 | COL48 | 2026-03-01 | 2 | 1 |
| 188200 | Arc Ellipse Mini Pendant | CAT13 | COL48 | 2026-04-01 | 1 | 1 |
| 188200 | Arc Ellipse Mini Pendant | CAT13 | COL48 | 2026-05-01 | 5 | 4 |
| 188200 | Arc Ellipse Mini Pendant | CAT13 | COL48 | 2026-06-01 | 5 | 2 |
| 188250 | Arc Ellipse Large Mini Pendant | CAT13 | COL48 | 2025-12-01 | 3 | 1 |
| 188250 | Arc Ellipse Large Mini Pendant | CAT13 | COL48 | 2026-03-01 | 7 | 4 |
| 188250 | Arc Ellipse Large Mini Pendant | CAT13 | COL48 | 2026-04-01 | 4 | 3 |
| 188250 | Arc Ellipse Large Mini Pendant | CAT13 | COL48 | 2026-05-01 | 6 | 2 |
| 188600 | Simple Mini Pendant | CAT13 | COL11 | 2026-01-01 | 0 | 1 |
| 188600 | Simple Mini Pendant | CAT13 | COL11 | 2026-02-01 | 14 | 4 |
| 188600 | Simple Mini Pendant | CAT13 | COL11 | 2026-03-01 | 6 | 2 |
| 188600 | Simple Mini Pendant | CAT13 | COL11 | 2026-05-01 | 2 | 2 |
| 188600 | Simple Mini Pendant | CAT13 | COL11 | 2026-06-01 | 6 | 2 |
| 188750 | Folio Mini Pendant | CAT13 | FOLIO | 2026-02-01 | 10 | 5 |
| 188750 | Folio Mini Pendant | CAT13 | FOLIO | 2026-03-01 | 3 | 1 |
| 188750 | Folio Mini Pendant | CAT13 | FOLIO | 2026-04-01 | 6 | 2 |
| 188750 | Folio Mini Pendant | CAT13 | FOLIO | 2026-06-01 | 5 | 3 |
| 188770 | Pental Mini Pendant | CAT13 | COL93 | 2025-12-01 | 3 | 1 |
| 188770 | Pental Mini Pendant | CAT13 | COL93 | 2026-02-01 | 1 | 1 |
| 188770 | Pental Mini Pendant | CAT13 | COL93 | 2026-03-01 | 7 | 5 |
| 188770 | Pental Mini Pendant | CAT13 | COL93 | 2026-04-01 | 2 | 1 |
| 188770 | Pental Mini Pendant | CAT13 | COL93 | 2026-05-01 | 12 | 4 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2025-12-01 | 6 | 2 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2026-01-01 | 2 | 2 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2026-02-01 | 12 | 5 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2026-03-01 | 5 | 2 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2026-04-01 | 2 | 1 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2026-05-01 | 10 | 3 |
| 188900 | Fritz Mini Pendant | CAT13 | FRITZ | 2026-06-01 | 10 | 4 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2025-12-01 | 8 | 4 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2026-01-01 | 6 | 5 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2026-02-01 | 26 | 13 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2026-03-01 | 13 | 7 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2026-04-01 | 13 | 6 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2026-05-01 | 19 | 8 |
| 188902 | Fritz Large Pendant | CAT13 | FRITZ | 2026-06-01 | 13 | 5 |
| 192043 | Lisse 20-Arm Chandelier | CAT14 | LISSE | 2026-01-01 | 1 | 1 |
| 192043 | Lisse 20-Arm Chandelier | CAT14 | LISSE | 2026-02-01 | 1 | 1 |
| 192043 | Lisse 20-Arm Chandelier | CAT14 | LISSE | 2026-04-01 | 1 | 1 |
| 192043 | Lisse 20-Arm Chandelier | CAT14 | LISSE | 2026-05-01 | 2 | 2 |
| 192043 | Lisse 20-Arm Chandelier | CAT14 | LISSE | 2026-06-01 | 2 | 2 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2025-12-01 | 3 | 2 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2026-01-01 | 5 | 5 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2026-02-01 | 4 | 3 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2026-03-01 | 3 | 3 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2026-04-01 | 10 | 10 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2026-05-01 | 5 | 3 |
| 194248 | Double Cirque Large Scale Chandelier | CAT14 | COL32 | 2026-06-01 | 5 | 2 |
| 194431 | Presidio Tryne Large Scale Pendant | CAT14 | TRYNE | 2026-01-01 | 1 | 1 |
| 194531 | Compass Large Scale Pendant | CAT14 | COL17 | 2025-12-01 | 2 | 2 |
| 194531 | Compass Large Scale Pendant | CAT14 | COL17 | 2026-02-01 | 2 | 2 |
| 194531 | Compass Large Scale Pendant | CAT14 | COL17 | 2026-03-01 | 2 | 2 |
| 194531 | Compass Large Scale Pendant | CAT14 | COL17 | 2026-05-01 | 1 | 1 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2025-12-01 | 3 | 3 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-01-01 | 2 | 2 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-02-01 | 2 | 2 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-03-01 | 2 | 2 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-04-01 | 6 | 2 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-05-01 | 3 | 3 |
| 194630 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-06-01 | 4 | 4 |
| 194636 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-01-01 | 2 | 2 |
| 194636 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-02-01 | 1 | 1 |
| 194636 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-03-01 | 2 | 2 |
| 194636 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-04-01 | 1 | 1 |
| 194636 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-05-01 | 5 | 3 |
| 194642 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-02-01 | 17 | 6 |
| 194642 | Exos Double Shade Large Scale Pendant | CAT14 | EXOS | 2026-04-01 | 1 | 1 |
| 194648 | — | — | — | 2026-04-01 | 1 | 1 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2025-12-01 | 5 | 2 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2026-01-01 | 7 | 3 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2026-02-01 | 19 | 8 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2026-03-01 | 7 | 4 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2026-04-01 | 26 | 4 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2026-05-01 | 12 | 3 |
| 201030 | Derby LED Sconce | CAT15 | DERBY | 2026-06-01 | 5 | 3 |
| 201057 | Callisto 3-Light Bath Sconce | CAT15 | COL82 | 2025-12-01 | 1 | 1 |
| 201057 | Callisto 3-Light Bath Sconce | CAT15 | COL82 | 2026-01-01 | 2 | 2 |
| 201057 | Callisto 3-Light Bath Sconce | CAT15 | COL82 | 2026-02-01 | 6 | 5 |
| 201057 | Callisto 3-Light Bath Sconce | CAT15 | COL82 | 2026-03-01 | 6 | 4 |
| 201057 | Callisto 3-Light Bath Sconce | CAT15 | COL82 | 2026-04-01 | 5 | 5 |
| 201057 | Callisto 3-Light Bath Sconce | CAT15 | COL82 | 2026-05-01 | 6 | 4 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2025-12-01 | 2 | 1 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2026-01-01 | 2 | 1 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2026-02-01 | 3 | 2 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2026-03-01 | 11 | 5 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2026-04-01 | 1 | 1 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2026-05-01 | 4 | 3 |
| 201059 | Callisto 1-Light Sconce | CAT15 | COL82 | 2026-06-01 | 2 | 1 |
| 201060 | Mika 3-Light Large Sconce/Semi-Flush | CAT15 | MIKA | 2026-01-01 | 7 | 3 |
| 201060 | Mika 3-Light Large Sconce/Semi-Flush | CAT15 | MIKA | 2026-02-01 | 2 | 1 |
| 201060 | Mika 3-Light Large Sconce/Semi-Flush | CAT15 | MIKA | 2026-03-01 | 1 | 1 |
| 201060 | Mika 3-Light Large Sconce/Semi-Flush | CAT15 | MIKA | 2026-04-01 | 1 | 1 |
| 201060 | Mika 3-Light Large Sconce/Semi-Flush | CAT15 | MIKA | 2026-05-01 | 1 | 1 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2025-12-01 | 8 | 1 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2026-01-01 | 5 | 4 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2026-02-01 | 5 | 4 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2026-03-01 | 8 | 4 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2026-04-01 | 5 | 1 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2026-05-01 | 8 | 3 |
| 201061 | Pangea 1-Light Sconce | CAT15 | COL77 | 2026-06-01 | 3 | 2 |
| 201062 | Crest 1-Light Sconce | CAT15 | CREST | 2026-01-01 | 2 | 1 |
| 201062 | Crest 1-Light Sconce | CAT15 | CREST | 2026-03-01 | 2 | 1 |
| 201062 | Crest 1-Light Sconce | CAT15 | CREST | 2026-05-01 | 2 | 1 |
| 201064 | Muse Sconce/Semi-Flush | CAT15 | MUSE | 2026-01-01 | 6 | 6 |
| 201064 | Muse Sconce/Semi-Flush | CAT15 | MUSE | 2026-02-01 | 5 | 5 |
| 201064 | Muse Sconce/Semi-Flush | CAT15 | MUSE | 2026-03-01 | 6 | 7 |
| 201064 | Muse Sconce/Semi-Flush | CAT15 | MUSE | 2026-04-01 | 5 | 5 |
| 201064 | Muse Sconce/Semi-Flush | CAT15 | MUSE | 2026-05-01 | 10 | 5 |
| 201065 | Shield Small Sconce | CAT15 | COL3 | 2026-01-01 | 11 | 10 |
| 201065 | Shield Small Sconce | CAT15 | COL3 | 2026-02-01 | 26 | 18 |
| 201065 | Shield Small Sconce | CAT15 | COL3 | 2026-03-01 | 30 | 20 |
| 201065 | Shield Small Sconce | CAT15 | COL3 | 2026-04-01 | 31 | 18 |
| 201065 | Shield Small Sconce | CAT15 | COL3 | 2026-05-01 | 23 | 13 |
| 201065 | Shield Small Sconce | CAT15 | COL3 | 2026-06-01 | 21 | 9 |
| 201066 | Lilium 1-Light Sconce | CAT15 | COL40 | 2026-01-01 | 1 | 1 |
| 201066 | Lilium 1-Light Sconce | CAT15 | COL40 | 2026-02-01 | 1 | 1 |
| 201066 | Lilium 1-Light Sconce | CAT15 | COL40 | 2026-05-01 | 1 | 1 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2025-12-01 | 2 | 1 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2026-01-01 | 7 | 6 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2026-02-01 | 10 | 6 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2026-03-01 | 7 | 6 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2026-04-01 | 6 | 4 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2026-05-01 | 14 | 6 |
| 201067 | Shield Large Sconce | CAT15 | COL3 | 2026-06-01 | 4 | 2 |
| 201070 | Triomphe 1-Light Sconce | CAT15 | COL83 | 2026-01-01 | 4 | 3 |
| 201070 | Triomphe 1-Light Sconce | CAT15 | COL83 | 2026-02-01 | 8 | 2 |
| 201070 | Triomphe 1-Light Sconce | CAT15 | COL83 | 2026-03-01 | 1 | 1 |
| 201070 | Triomphe 1-Light Sconce | CAT15 | COL83 | 2026-04-01 | 8 | 2 |
| 201070 | Triomphe 1-Light Sconce | CAT15 | COL83 | 2026-06-01 | 2 | 1 |
| 201080 | Passage 1-Light Sconce | CAT15 | COL43 | 2026-01-01 | 8 | 4 |
| 201080 | Passage 1-Light Sconce | CAT15 | COL43 | 2026-03-01 | 4 | 2 |
| 201080 | Passage 1-Light Sconce | CAT15 | COL43 | 2026-04-01 | 2 | 1 |
| 201080 | Passage 1-Light Sconce | CAT15 | COL43 | 2026-05-01 | 10 | 4 |
| 201080 | Passage 1-Light Sconce | CAT15 | COL43 | 2026-06-01 | 4 | 1 |
| 201082 | Truss 1-Light Sconce | CAT15 | TRUSS | 2026-01-01 | 4 | 4 |
| 201082 | Truss 1-Light Sconce | CAT15 | TRUSS | 2026-02-01 | 15 | 9 |
| 201082 | Truss 1-Light Sconce | CAT15 | TRUSS | 2026-03-01 | 19 | 6 |
| 201082 | Truss 1-Light Sconce | CAT15 | TRUSS | 2026-04-01 | 3 | 2 |
| 201082 | Truss 1-Light Sconce | CAT15 | TRUSS | 2026-05-01 | 4 | 3 |
| 201082 | Truss 1-Light Sconce | CAT15 | TRUSS | 2026-06-01 | 7 | 3 |
| 201083 | Windsor 1-Light Sconce | CAT15 | COL149 | 2026-01-01 | 6 | 6 |
| 201083 | Windsor 1-Light Sconce | CAT15 | COL149 | 2026-02-01 | 10 | 3 |
| 201083 | Windsor 1-Light Sconce | CAT15 | COL149 | 2026-03-01 | 6 | 5 |
| 201083 | Windsor 1-Light Sconce | CAT15 | COL149 | 2026-04-01 | 4 | 3 |
| 201083 | Windsor 1-Light Sconce | CAT15 | COL149 | 2026-05-01 | 11 | 4 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | FOCAL | 2026-01-01 | 4 | 4 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | FOCAL | 2026-02-01 | 7 | 3 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | FOCAL | 2026-03-01 | 5 | 2 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | FOCAL | 2026-04-01 | 3 | 3 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | FOCAL | 2026-05-01 | 8 | 4 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | FOCAL | 2026-06-01 | 2 | 2 |
| 201086 | Focal Small Sconce/Flush Mount | CAT15 | FOCAL | 2026-01-01 | 7 | 6 |
| 201086 | Focal Small Sconce/Flush Mount | CAT15 | FOCAL | 2026-02-01 | 8 | 7 |
| 201086 | Focal Small Sconce/Flush Mount | CAT15 | FOCAL | 2026-03-01 | 3 | 2 |
| 201086 | Focal Small Sconce/Flush Mount | CAT15 | FOCAL | 2026-04-01 | 6 | 2 |
| 201086 | Focal Small Sconce/Flush Mount | CAT15 | FOCAL | 2026-05-01 | 5 | 2 |
| 201086 | Focal Small Sconce/Flush Mount | CAT15 | FOCAL | 2026-06-01 | 1 | 1 |
| 201309 | Parasol Sconce | CAT15 | COL36 | 2026-01-01 | 6 | 4 |
| 201309 | Parasol Sconce | CAT15 | COL36 | 2026-02-01 | 16 | 9 |
| 201309 | Parasol Sconce | CAT15 | COL36 | 2026-03-01 | 13 | 4 |
| 201309 | Parasol Sconce | CAT15 | COL36 | 2026-04-01 | 1 | 1 |
| 201309 | Parasol Sconce | CAT15 | COL36 | 2026-05-01 | 3 | 2 |
| 201310 | Arc Large 1-Light Bath Sconce | CAT15 | ARC | 2026-01-01 | 11 | 2 |
| 201310 | Arc Large 1-Light Bath Sconce | CAT15 | ARC | 2026-02-01 | 8 | 3 |
| 201310 | Arc Large 1-Light Bath Sconce | CAT15 | ARC | 2026-04-01 | 19 | 7 |
| 201310 | Arc Large 1-Light Bath Sconce | CAT15 | ARC | 2026-05-01 | 7 | 4 |
| 201310 | Arc Large 1-Light Bath Sconce | CAT15 | ARC | 2026-06-01 | 7 | 2 |
| 201311 | Arc Small 1-Light Bath Sconce | CAT15 | ARC | 2026-01-01 | 11 | 4 |
| 201311 | Arc Small 1-Light Bath Sconce | CAT15 | ARC | 2026-02-01 | 13 | 6 |
| 201311 | Arc Small 1-Light Bath Sconce | CAT15 | ARC | 2026-03-01 | 9 | 5 |
| 201311 | Arc Small 1-Light Bath Sconce | CAT15 | ARC | 2026-04-01 | 6 | 4 |
| 201311 | Arc Small 1-Light Bath Sconce | CAT15 | ARC | 2026-05-01 | 5 | 3 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2025-12-01 | 3 | 2 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2026-01-01 | 7 | 5 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2026-02-01 | 19 | 10 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2026-03-01 | 19 | 13 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2026-04-01 | 10 | 10 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2026-05-01 | 24 | 11 |
| 201312 | Arc 3-Light Bath Sconce | CAT15 | ARC | 2026-06-01 | 5 | 5 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2025-12-01 | 3 | 2 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2026-01-01 | 4 | 3 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2026-02-01 | 2 | 1 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2026-03-01 | 14 | 8 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2026-04-01 | 11 | 8 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2026-05-01 | 4 | 3 |
| 201313 | Arc 5-Light Bath Sconce | CAT15 | ARC | 2026-06-01 | 3 | 2 |
| 201320 | Gatsby 1-Light Bath Sconce | CAT15 | COL35 | 2025-12-01 | 5 | 1 |
| 201320 | Gatsby 1-Light Bath Sconce | CAT15 | COL35 | 2026-01-01 | 6 | 2 |
| 201320 | Gatsby 1-Light Bath Sconce | CAT15 | COL35 | 2026-02-01 | 6 | 3 |
| 201320 | Gatsby 1-Light Bath Sconce | CAT15 | COL35 | 2026-03-01 | 2 | 1 |
| 201320 | Gatsby 1-Light Bath Sconce | CAT15 | COL35 | 2026-04-01 | 6 | 3 |
| 201320 | Gatsby 1-Light Bath Sconce | CAT15 | COL35 | 2026-05-01 | 5 | 3 |
| 201322 | Gatsby 3-Light Bath Sconce | CAT15 | COL35 | 2025-12-01 | 1 | 1 |
| 201322 | Gatsby 3-Light Bath Sconce | CAT15 | COL35 | 2026-01-01 | 1 | 1 |
| 201322 | Gatsby 3-Light Bath Sconce | CAT15 | COL35 | 2026-03-01 | 2 | 3 |
| 201322 | Gatsby 3-Light Bath Sconce | CAT15 | COL35 | 2026-04-01 | 3 | 1 |
| 201322 | Gatsby 3-Light Bath Sconce | CAT15 | COL35 | 2026-05-01 | 2 | 1 |
| 201323 | Gatsby 5-Light Bath Sconce | CAT15 | COL35 | 2026-02-01 | 2 | 1 |
| 201323 | Gatsby 5-Light Bath Sconce | CAT15 | COL35 | 2026-05-01 | 2 | 2 |
| 201323 | Gatsby 5-Light Bath Sconce | CAT15 | COL35 | 2026-06-01 | 3 | 2 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2025-12-01 | 2 | 1 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2026-01-01 | 18 | 6 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2026-02-01 | 12 | 7 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2026-03-01 | 12 | 7 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2026-04-01 | 25 | 12 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2026-05-01 | 15 | 8 |
| 201330 | Eos 1-Light Bath Sconce | CAT15 | EOS | 2026-06-01 | 20 | 4 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2025-12-01 | 2 | 2 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2026-01-01 | 5 | 4 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2026-02-01 | 5 | 4 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2026-03-01 | 4 | 4 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2026-04-01 | 7 | 6 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2026-05-01 | 3 | 3 |
| 201332 | Eos 3-Light Bath Sconce | CAT15 | EOS | 2026-06-01 | 5 | 3 |
| 201333 | Eos 5-Light Bath Sconce | CAT15 | EOS | 2026-01-01 | 3 | 2 |
| 201333 | Eos 5-Light Bath Sconce | CAT15 | EOS | 2026-02-01 | 5 | 2 |
| 201333 | Eos 5-Light Bath Sconce | CAT15 | EOS | 2026-03-01 | 11 | 8 |
| 201333 | Eos 5-Light Bath Sconce | CAT15 | EOS | 2026-04-01 | 2 | 2 |
| 201333 | Eos 5-Light Bath Sconce | CAT15 | EOS | 2026-05-01 | 3 | 2 |
| 201333 | Eos 5-Light Bath Sconce | CAT15 | EOS | 2026-06-01 | 3 | 2 |
| 201340 | Ume 1-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-01-01 | 2 | 1 |
| 201340 | Ume 1-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-02-01 | 2 | 3 |
| 201340 | Ume 1-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-03-01 | 5 | 3 |
| 201340 | Ume 1-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-05-01 | 1 | 1 |
| 201342 | Ume 3-Light Curved Arm Bath Sconce | CAT15 | UME | 2025-12-01 | 2 | 2 |
| 201342 | Ume 3-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-01-01 | 1 | 1 |
| 201342 | Ume 3-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-02-01 | 7 | 6 |
| 201342 | Ume 3-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-03-01 | 6 | 5 |
| 201342 | Ume 3-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-04-01 | 5 | 4 |
| 201342 | Ume 3-Light Curved Arm Bath Sconce | CAT15 | UME | 2026-05-01 | 4 | 4 |
| 201344 | Bow 1-Light Bath Sconce | CAT15 | BOW | 2026-01-01 | 2 | 1 |
| 201344 | Bow 1-Light Bath Sconce | CAT15 | BOW | 2026-02-01 | 3 | 1 |
| 201344 | Bow 1-Light Bath Sconce | CAT15 | BOW | 2026-03-01 | 1 | 1 |
| 201344 | Bow 1-Light Bath Sconce | CAT15 | BOW | 2026-04-01 | 6 | 3 |
| 201344 | Bow 1-Light Bath Sconce | CAT15 | BOW | 2026-05-01 | 2 | 1 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2025-12-01 | 8 | 2 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2026-01-01 | 7 | 4 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2026-02-01 | 5 | 3 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2026-03-01 | 8 | 5 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2026-04-01 | 4 | 2 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2026-05-01 | 3 | 3 |
| 201346 | Bow 2-Light Bath Sconce | CAT15 | BOW | 2026-06-01 | 0 | 1 |
| 201350 | Lapas 1-Light Bath Sconce | CAT15 | LAPAS | 2026-01-01 | 3 | 2 |
| 201350 | Lapas 1-Light Bath Sconce | CAT15 | LAPAS | 2026-02-01 | 14 | 7 |
| 201350 | Lapas 1-Light Bath Sconce | CAT15 | LAPAS | 2026-03-01 | 2 | 1 |
| 201350 | Lapas 1-Light Bath Sconce | CAT15 | LAPAS | 2026-04-01 | 3 | 2 |
| 201350 | Lapas 1-Light Bath Sconce | CAT15 | LAPAS | 2026-05-01 | 2 | 2 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2025-12-01 | 2 | 1 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2026-01-01 | 7 | 6 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2026-02-01 | 15 | 11 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2026-03-01 | 7 | 6 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2026-04-01 | 3 | 2 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2026-05-01 | 9 | 6 |
| 201352 | Lapas 3-Light Bath Sconce | CAT15 | LAPAS | 2026-06-01 | 5 | 3 |
| 201353 | Riza Sconce | CAT15 | RIZA | 2026-04-01 | 2 | 1 |
| 201353 | Riza Sconce | CAT15 | RIZA | 2026-05-01 | 1 | 1 |
| 201355 | Prisma 1-Light Bath Sconce | CAT15 | COL94 | 2026-05-01 | 2 | 1 |
| 201357 | Prisma 3-Light Bath Sconce | CAT15 | COL94 | 2026-01-01 | 2 | 1 |
| 201357 | Prisma 3-Light Bath Sconce | CAT15 | COL94 | 2026-02-01 | 2 | 2 |
| 201357 | Prisma 3-Light Bath Sconce | CAT15 | COL94 | 2026-03-01 | 2 | 2 |
| 201360 | — | — | — | 2026-01-01 | 1 | 1 |
| 201360 | — | — | — | 2026-03-01 | 1 | 1 |
| 201360 | — | — | — | 2026-04-01 | 2 | 2 |
| 201361 | — | — | — | 2026-03-01 | 1 | 1 |
| 201371 | Ume 1-Light Long-Arm Sconce | CAT15 | UME | 2026-01-01 | 4 | 2 |
| 201372 | Brooklyn 1-Light Single Shade Bath Sconce | CAT15 | COL2 | 2025-12-01 | 4 | 2 |
| 201372 | Brooklyn 1-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-01-01 | 3 | 1 |
| 201372 | Brooklyn 1-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-03-01 | 3 | 1 |
| 201373 | Brooklyn 3-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-01-01 | 1 | 1 |
| 201373 | Brooklyn 3-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-02-01 | 1 | 1 |
| 201373 | Brooklyn 3-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-03-01 | 1 | 1 |
| 201373 | Brooklyn 3-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-04-01 | 1 | 1 |
| 201373 | Brooklyn 3-Light Single Shade Bath Sconce | CAT15 | COL2 | 2026-05-01 | 2 | 1 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2025-12-01 | 1 | 1 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-01-01 | 5 | 3 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-02-01 | 6 | 3 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-03-01 | 17 | 8 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-04-01 | 9 | 4 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-05-01 | 6 | 4 |
| 201374 | Brooklyn 1-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-06-01 | 5 | 3 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2025-12-01 | 4 | 3 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-01-01 | 6 | 5 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-02-01 | 10 | 8 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-03-01 | 11 | 10 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-04-01 | 11 | 11 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-05-01 | 8 | 6 |
| 201375 | Brooklyn 3-Light Double Shade Bath Sconce | CAT15 | COL2 | 2026-06-01 | 5 | 4 |
| 201376 | Brooklyn 1-Light Single Shade Long-Arm Sconce | CAT15 | COL2 | 2025-12-01 | 1 | 1 |
| 201376 | Brooklyn 1-Light Single Shade Long-Arm Sconce | CAT15 | COL2 | 2026-01-01 | 4 | 2 |
| 201376 | Brooklyn 1-Light Single Shade Long-Arm Sconce | CAT15 | COL2 | 2026-02-01 | 3 | 1 |
| 201376 | Brooklyn 1-Light Single Shade Long-Arm Sconce | CAT15 | COL2 | 2026-03-01 | 1 | 1 |
| 201376 | Brooklyn 1-Light Single Shade Long-Arm Sconce | CAT15 | COL2 | 2026-05-01 | 4 | 2 |
| 201376 | Brooklyn 1-Light Single Shade Long-Arm Sconce | CAT15 | COL2 | 2026-06-01 | 2 | 2 |
| 201377 | Brooklyn 1-Light Double Shade Long-Arm Sconce | CAT15 | COL2 | 2026-01-01 | 8 | 4 |
| 201377 | Brooklyn 1-Light Double Shade Long-Arm Sconce | CAT15 | COL2 | 2026-03-01 | 7 | 2 |
| 201377 | Brooklyn 1-Light Double Shade Long-Arm Sconce | CAT15 | COL2 | 2026-04-01 | 8 | 2 |
| 201377 | Brooklyn 1-Light Double Shade Long-Arm Sconce | CAT15 | COL2 | 2026-05-01 | 2 | 2 |
| 201378 | Brooklyn 3-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-01-01 | 2 | 1 |
| 201378 | Brooklyn 3-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-02-01 | 5 | 1 |
| 201378 | Brooklyn 3-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-03-01 | 2 | 2 |
| 201378 | Brooklyn 3-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-04-01 | 3 | 2 |
| 201378 | Brooklyn 3-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-05-01 | 1 | 1 |
| 201378 | Brooklyn 3-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-06-01 | 2 | 1 |
| 201379 | Brooklyn 5-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-03-01 | 1 | 1 |
| 201379 | Brooklyn 5-Light Straight Double Shade Bath Sconce | CAT15 | COL2 | 2026-04-01 | 1 | 1 |
| 201380 | Passage LED Bath Bar | CAT15 | COL43 | 2026-02-01 | 1 | 1 |
| 201380 | Passage LED Bath Bar | CAT15 | COL43 | 2026-03-01 | 3 | 2 |
| 201380 | Passage LED Bath Bar | CAT15 | COL43 | 2026-04-01 | 2 | 1 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2025-12-01 | 4 | 2 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2026-01-01 | 4 | 2 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2026-02-01 | 11 | 4 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2026-03-01 | 11 | 6 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2026-04-01 | 20 | 11 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2026-05-01 | 8 | 5 |
| 201390 | Luma Sconce | CAT15 | LUMA | 2026-06-01 | 3 | 1 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2025-12-01 | 3 | 2 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2026-01-01 | 10 | 3 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2026-02-01 | 2 | 1 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2026-03-01 | 10 | 6 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2026-04-01 | 2 | 1 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2026-05-01 | 2 | 1 |
| 201391 | Mobius Sconce | CAT15 | COL14 | 2026-06-01 | 3 | 1 |
| 201392 | Link Blown Glass Sconce | CAT15 | LINK | 2025-12-01 | 3 | 1 |
| 201392 | Link Blown Glass Sconce | CAT15 | LINK | 2026-01-01 | 5 | 3 |
| 201392 | Link Blown Glass Sconce | CAT15 | LINK | 2026-04-01 | 4 | 2 |
| 201392 | Link Blown Glass Sconce | CAT15 | LINK | 2026-06-01 | 4 | 2 |
| 201393 | Tura Seeded Glass Sconce | CAT15 | TURA | 2026-05-01 | 1 | 1 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2025-12-01 | 4 | 2 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2026-01-01 | 6 | 3 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2026-02-01 | 10 | 5 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2026-03-01 | 7 | 4 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2026-04-01 | 16 | 6 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2026-05-01 | 6 | 2 |
| 201394 | Exos Glass Mini Sconce | CAT15 | COL39 | 2026-06-01 | 7 | 3 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2025-12-01 | 2 | 1 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2026-01-01 | 4 | 3 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2026-02-01 | 9 | 4 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2026-03-01 | 2 | 1 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2026-04-01 | 9 | 2 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2026-05-01 | 33 | 8 |
| 201395 | Link Clear Glass Sconce | CAT15 | LINK | 2026-06-01 | 6 | 3 |
| 201397 | Chrysalis Small Sconce | CAT15 | COL86 | 2026-01-01 | 2 | 1 |
| 201397 | Chrysalis Small Sconce | CAT15 | COL86 | 2026-03-01 | 2 | 1 |
| 201397 | Chrysalis Small Sconce | CAT15 | COL86 | 2026-05-01 | 4 | 2 |
| 201397 | Chrysalis Small Sconce | CAT15 | COL86 | 2026-06-01 | 2 | 1 |
| 201398 | Chrysalis Large Sconce | CAT15 | COL86 | 2026-01-01 | 4 | 2 |
| 201398 | Chrysalis Large Sconce | CAT15 | COL86 | 2026-02-01 | 4 | 1 |
| 201398 | Chrysalis Large Sconce | CAT15 | COL86 | 2026-04-01 | 8 | 4 |
| 201398 | Chrysalis Large Sconce | CAT15 | COL86 | 2026-05-01 | 4 | 2 |
| 201398 | Chrysalis Large Sconce | CAT15 | COL86 | 2026-06-01 | 2 | 1 |
| 201399 | Clouds Sconce | CAT15 | COL79 | 2026-01-01 | 3 | 2 |
| 201399 | Clouds Sconce | CAT15 | COL79 | 2026-02-01 | 3 | 2 |
| 201399 | Clouds Sconce | CAT15 | COL79 | 2026-03-01 | 6 | 2 |
| 201399 | Clouds Sconce | CAT15 | COL79 | 2026-04-01 | 4 | 2 |
| 201399 | Clouds Sconce | CAT15 | COL79 | 2026-05-01 | 1 | 1 |
| 201399 | Clouds Sconce | CAT15 | COL79 | 2026-06-01 | 10 | 6 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2025-12-01 | 2 | 1 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2026-01-01 | 2 | 1 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2026-02-01 | 1 | 1 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2026-03-01 | 2 | 1 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2026-04-01 | 0 | 1 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2026-05-01 | 4 | 2 |
| 201500 | Astra Sconce | CAT15 | ASTRA | 2026-06-01 | 1 | 1 |
| 201550 | Geo Sconce | CAT15 | GEO | 2026-02-01 | 2 | 1 |
| 201550 | Geo Sconce | CAT15 | GEO | 2026-03-01 | 2 | 1 |
| 201700 | Lilium Sconce | CAT15 | COL40 | 2026-02-01 | 2 | 1 |
| 201700 | Lilium Sconce | CAT15 | COL40 | 2026-03-01 | 1 | 1 |
| 201700 | Lilium Sconce | CAT15 | COL40 | 2026-04-01 | 2 | 1 |
| 201700 | Lilium Sconce | CAT15 | COL40 | 2026-06-01 | 3 | 2 |
| 202010 | — | — | — | 2026-02-01 | 1 | 1 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2025-12-01 | 2 | 1 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2026-01-01 | 5 | 4 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2026-02-01 | 4 | 2 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2026-03-01 | 10 | 6 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2026-04-01 | 5 | 1 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2026-05-01 | 3 | 2 |
| 202015 | Trove LED Sconce | CAT15 | TROVE | 2026-06-01 | 7 | 3 |
| 202025 | Solstice Sconce | CAT15 | COL73 | 2026-01-01 | 2 | 2 |
| 202025 | Solstice Sconce | CAT15 | COL73 | 2026-02-01 | 8 | 4 |
| 202025 | Solstice Sconce | CAT15 | COL73 | 2026-03-01 | 7 | 3 |
| 202025 | Solstice Sconce | CAT15 | COL73 | 2026-04-01 | 6 | 4 |
| 202025 | Solstice Sconce | CAT15 | COL73 | 2026-05-01 | 20 | 4 |
| 202025 | Solstice Sconce | CAT15 | COL73 | 2026-06-01 | 7 | 3 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2025-12-01 | 8 | 3 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2026-01-01 | 3 | 2 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2026-02-01 | 7 | 3 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2026-03-01 | 9 | 3 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2026-04-01 | 6 | 2 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2026-05-01 | 9 | 4 |
| 202045 | Summit Sconce | CAT15 | COL44 | 2026-06-01 | 6 | 2 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2025-12-01 | 14 | 7 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2026-01-01 | 2 | 2 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2026-02-01 | 14 | 8 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2026-03-01 | 8 | 3 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2026-04-01 | 7 | 5 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2026-05-01 | 4 | 4 |
| 202117 | Zen Sconce | CAT15 | ZEN | 2026-06-01 | 4 | 2 |
| 202221 | Glissade LED Bath Sconce | CAT15 | COL106 | 2026-01-01 | 2 | 2 |
| 202221 | Glissade LED Bath Sconce | CAT15 | COL106 | 2026-02-01 | 4 | 4 |
| 202221 | Glissade LED Bath Sconce | CAT15 | COL106 | 2026-03-01 | 2 | 2 |
| 202221 | Glissade LED Bath Sconce | CAT15 | COL106 | 2026-05-01 | 3 | 2 |
| 202221 | Glissade LED Bath Sconce | CAT15 | COL106 | 2026-06-01 | 5 | 2 |
| 202222 | Glissade LED Bath Bar | CAT15 | COL106 | 2025-12-01 | 3 | 2 |
| 202222 | Glissade LED Bath Bar | CAT15 | COL106 | 2026-01-01 | 8 | 2 |
| 202222 | Glissade LED Bath Bar | CAT15 | COL106 | 2026-02-01 | 2 | 1 |
| 202222 | Glissade LED Bath Bar | CAT15 | COL106 | 2026-03-01 | 3 | 2 |
| 202222 | Glissade LED Bath Bar | CAT15 | COL106 | 2026-05-01 | 14 | 7 |
| 202225 | Draped Glass LED Bath Bar | CAT15 | COL23 | 2025-12-01 | 1 | 1 |
| 202225 | Draped Glass LED Bath Bar | CAT15 | COL23 | 2026-01-01 | 3 | 3 |
| 202225 | Draped Glass LED Bath Bar | CAT15 | COL23 | 2026-02-01 | 3 | 2 |
| 202225 | Draped Glass LED Bath Bar | CAT15 | COL23 | 2026-03-01 | 6 | 3 |
| 202225 | Draped Glass LED Bath Bar | CAT15 | COL23 | 2026-06-01 | 5 | 3 |
| 203030 | Flora Sconce | CAT15 | FLORA | 2026-01-01 | 5 | 3 |
| 203030 | Flora Sconce | CAT15 | FLORA | 2026-02-01 | 4 | 2 |
| 203030 | Flora Sconce | CAT15 | FLORA | 2026-03-01 | 1 | 1 |
| 203030 | Flora Sconce | CAT15 | FLORA | 2026-04-01 | 3 | 2 |
| 203030 | Flora Sconce | CAT15 | FLORA | 2026-05-01 | 1 | 1 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2025-12-01 | 4 | 2 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2026-01-01 | 24 | 9 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2026-02-01 | 10 | 5 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2026-03-01 | 2 | 1 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2026-04-01 | 12 | 7 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2026-05-01 | 4 | 3 |
| 203035 | Flora Sconce | CAT15 | FLORA | 2026-06-01 | 2 | 1 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2025-12-01 | 2 | 1 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2026-01-01 | 15 | 5 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2026-02-01 | 7 | 4 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2026-03-01 | 29 | 5 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2026-04-01 | 4 | 1 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2026-05-01 | 8 | 5 |
| 203050 | Lisse 1-Light Sconce | CAT15 | LISSE | 2026-06-01 | 5 | 2 |
| 203053 | Lisse 2-Light Sconce | CAT15 | LISSE | 2025-12-01 | 4 | 3 |
| 203053 | Lisse 2-Light Sconce | CAT15 | LISSE | 2026-01-01 | 8 | 4 |
| 203053 | Lisse 2-Light Sconce | CAT15 | LISSE | 2026-02-01 | 20 | 5 |
| 203053 | Lisse 2-Light Sconce | CAT15 | LISSE | 2026-03-01 | 25 | 10 |
| 203053 | Lisse 2-Light Sconce | CAT15 | LISSE | 2026-04-01 | 6 | 4 |
| 203053 | Lisse 2-Light Sconce | CAT15 | LISSE | 2026-05-01 | 14 | 5 |
| 203300 | Apothecary Sconce | CAT15 | COL34 | 2025-12-01 | 1 | 1 |
| 203300 | Apothecary Sconce | CAT15 | COL34 | 2026-01-01 | 4 | 2 |
| 203300 | Apothecary Sconce | CAT15 | COL34 | 2026-02-01 | 2 | 1 |
| 203325 | Kiwi Sconce | CAT15 | KIWI | 2026-03-01 | 2 | 1 |
| 203330 | Vela Sconce | CAT15 | VELA | 2025-12-01 | 24 | 6 |
| 203330 | Vela Sconce | CAT15 | VELA | 2026-01-01 | 16 | 10 |
| 203330 | Vela Sconce | CAT15 | VELA | 2026-02-01 | 36 | 13 |
| 203330 | Vela Sconce | CAT15 | VELA | 2026-03-01 | 143 | 8 |
| 203330 | Vela Sconce | CAT15 | VELA | 2026-04-01 | 10 | 4 |
| 203330 | Vela Sconce | CAT15 | VELA | 2026-05-01 | 28 | 11 |
| 203330 | Vela Sconce | CAT15 | VELA | 2026-06-01 | 16 | 4 |
| 203335 | Luma Sconce | CAT15 | LUMA | 2026-02-01 | 2 | 1 |
| 203335 | Luma Sconce | CAT15 | LUMA | 2026-03-01 | 0 | 1 |
| 203335 | Luma Sconce | CAT15 | LUMA | 2026-04-01 | 8 | 3 |
| 204070 | Saratoga Sconce | CAT15 | COL5 | 2026-01-01 | 4 | 1 |
| 204070 | Saratoga Sconce | CAT15 | COL5 | 2026-02-01 | 2 | 1 |
| 204070 | Saratoga Sconce | CAT15 | COL5 | 2026-03-01 | 5 | 3 |
| 204070 | Saratoga Sconce | CAT15 | COL5 | 2026-04-01 | 24 | 3 |
| 204070 | Saratoga Sconce | CAT15 | COL5 | 2026-05-01 | 3 | 2 |
| 204070 | Saratoga Sconce | CAT15 | COL5 | 2026-06-01 | 4 | 2 |
| 204072 | Caribou 1-Light Sconce | CAT15 | COL84 | 2026-01-01 | 3 | 2 |
| 204072 | Caribou 1-Light Sconce | CAT15 | COL84 | 2026-02-01 | 3 | 3 |
| 204072 | Caribou 1-Light Sconce | CAT15 | COL84 | 2026-03-01 | 16 | 11 |
| 204072 | Caribou 1-Light Sconce | CAT15 | COL84 | 2026-04-01 | 4 | 2 |
| 204072 | Caribou 1-Light Sconce | CAT15 | COL84 | 2026-05-01 | 3 | 2 |
| 204072 | Caribou 1-Light Sconce | CAT15 | COL84 | 2026-06-01 | 3 | 2 |
| 204073 | Bellis 2-Light Sconce | CAT15 | COL87 | 2026-01-01 | 9 | 8 |
| 204073 | Bellis 2-Light Sconce | CAT15 | COL87 | 2026-02-01 | 23 | 13 |
| 204073 | Bellis 2-Light Sconce | CAT15 | COL87 | 2026-03-01 | 22 | 9 |
| 204073 | Bellis 2-Light Sconce | CAT15 | COL87 | 2026-04-01 | 8 | 5 |
| 204073 | Bellis 2-Light Sconce | CAT15 | COL87 | 2026-05-01 | 11 | 4 |
| 204073 | Bellis 2-Light Sconce | CAT15 | COL87 | 2026-06-01 | 4 | 2 |
| 204074 | Lyric 1-LIght Sconce | CAT15 | LYRIC | 2026-01-01 | 2 | 2 |
| 204074 | Lyric 1-LIght Sconce | CAT15 | LYRIC | 2026-02-01 | 4 | 2 |
| 204074 | Lyric 1-LIght Sconce | CAT15 | LYRIC | 2026-03-01 | 7 | 3 |
| 204210 | Simple Lines Sconce | CAT15 | COL11 | 2025-12-01 | 2 | 1 |
| 204210 | Simple Lines Sconce | CAT15 | COL11 | 2026-01-01 | 3 | 2 |
| 204210 | Simple Lines Sconce | CAT15 | COL11 | 2026-02-01 | 4 | 2 |
| 204210 | Simple Lines Sconce | CAT15 | COL11 | 2026-03-01 | 11 | 5 |
| 204210 | Simple Lines Sconce | CAT15 | COL11 | 2026-04-01 | 6 | 3 |
| 204210 | Simple Lines Sconce | CAT15 | COL11 | 2026-05-01 | 3 | 1 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2025-12-01 | 7 | 2 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2026-01-01 | 3 | 2 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2026-02-01 | 4 | 2 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2026-03-01 | 8 | 5 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2026-04-01 | 13 | 6 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2026-05-01 | 15 | 7 |
| 204213 | Simple Lines Sconce | CAT15 | COL11 | 2026-06-01 | 3 | 2 |
| 204250 | New Town Sconce | CAT15 | COL4 | 2026-01-01 | 1 | 1 |
| 204250 | New Town Sconce | CAT15 | COL4 | 2026-02-01 | 2 | 2 |
| 204250 | New Town Sconce | CAT15 | COL4 | 2026-03-01 | 6 | 6 |
| 204250 | New Town Sconce | CAT15 | COL4 | 2026-04-01 | 6 | 2 |
| 204250 | New Town Sconce | CAT15 | COL4 | 2026-05-01 | 36 | 5 |
| 204250 | New Town Sconce | CAT15 | COL4 | 2026-06-01 | 6 | 1 |
| 204255 | New Town Large Sconce | CAT15 | COL4 | 2025-12-01 | 4 | 2 |
| 204255 | New Town Large Sconce | CAT15 | COL4 | 2026-01-01 | 10 | 5 |
| 204255 | New Town Large Sconce | CAT15 | COL4 | 2026-02-01 | 15 | 6 |
| 204255 | New Town Large Sconce | CAT15 | COL4 | 2026-03-01 | 4 | 2 |
| 204255 | New Town Large Sconce | CAT15 | COL4 | 2026-05-01 | 9 | 5 |
| 204255 | New Town Large Sconce | CAT15 | COL4 | 2026-06-01 | 2 | 1 |
| 204260 | New Town Sconce | CAT15 | COL4 | 2026-04-01 | 1 | 1 |
| 204260 | New Town Sconce | CAT15 | COL4 | 2026-05-01 | 1 | 2 |
| 204260 | New Town Sconce | CAT15 | COL4 | 2026-06-01 | 6 | 2 |
| 204320 | Echo Sconce | CAT15 | ECHO | 2025-12-01 | 2 | 1 |
| 204320 | Echo Sconce | CAT15 | ECHO | 2026-01-01 | 2 | 1 |
| 204320 | Echo Sconce | CAT15 | ECHO | 2026-02-01 | 2 | 1 |
| 204320 | Echo Sconce | CAT15 | ECHO | 2026-03-01 | 2 | 1 |
| 204320 | Echo Sconce | CAT15 | ECHO | 2026-04-01 | 4 | 2 |
| 204320 | Echo Sconce | CAT15 | ECHO | 2026-05-01 | 2 | 1 |
| 204420 | Portico 1-Light Sconce | CAT15 | COL128 | 2026-01-01 | 6 | 1 |
| 204420 | Portico 1-Light Sconce | CAT15 | COL128 | 2026-03-01 | 2 | 1 |
| 204420 | Portico 1-Light Sconce | CAT15 | COL128 | 2026-04-01 | 4 | 1 |
| 204420 | Portico 1-Light Sconce | CAT15 | COL128 | 2026-06-01 | 1 | 1 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2025-12-01 | 3 | 3 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2026-01-01 | 14 | 7 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2026-02-01 | 18 | 5 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2026-03-01 | 6 | 4 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2026-04-01 | 13 | 8 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2026-05-01 | 11 | 4 |
| 204526 | Sweeping Taper Sconce | CAT15 | COL1 | 2026-06-01 | 6 | 3 |
| 204529 | Sweeping Taper ADA Sconce | CAT15 | COL1 | 2026-01-01 | 4 | 2 |
| 204529 | Sweeping Taper ADA Sconce | CAT15 | COL1 | 2026-02-01 | 3 | 2 |
| 204529 | Sweeping Taper ADA Sconce | CAT15 | COL1 | 2026-03-01 | 2 | 1 |
| 204529 | Sweeping Taper ADA Sconce | CAT15 | COL1 | 2026-04-01 | 7 | 2 |
| 204529 | Sweeping Taper ADA Sconce | CAT15 | COL1 | 2026-05-01 | 2 | 1 |
| 204531 | Scroll Sconce | CAT15 | COL97 | 2026-01-01 | 6 | 4 |
| 204531 | Scroll Sconce | CAT15 | COL97 | 2026-02-01 | 6 | 3 |
| 204531 | Scroll Sconce | CAT15 | COL97 | 2026-03-01 | 2 | 1 |
| 204531 | Scroll Sconce | CAT15 | COL97 | 2026-04-01 | 4 | 2 |
| 204670 | Formae Contemporary 1-Light Sconce | CAT15 | COL98 | 2025-12-01 | 5 | 2 |
| 204670 | Formae Contemporary 1-Light Sconce | CAT15 | COL98 | 2026-01-01 | 4 | 3 |
| 204670 | Formae Contemporary 1-Light Sconce | CAT15 | COL98 | 2026-02-01 | 2 | 1 |
| 204670 | Formae Contemporary 1-Light Sconce | CAT15 | COL98 | 2026-04-01 | 4 | 1 |
| 204670 | Formae Contemporary 1-Light Sconce | CAT15 | COL98 | 2026-05-01 | 4 | 2 |
| 204670 | Formae Contemporary 1-Light Sconce | CAT15 | COL98 | 2026-06-01 | 2 | 1 |
| 204672 | Formae Contemporary 2-Light Sconce | CAT15 | COL98 | 2025-12-01 | 8 | 2 |
| 204672 | Formae Contemporary 2-Light Sconce | CAT15 | COL98 | 2026-03-01 | 4 | 1 |
| 204672 | Formae Contemporary 2-Light Sconce | CAT15 | COL98 | 2026-05-01 | 4 | 1 |
| 204672 | Formae Contemporary 2-Light Sconce | CAT15 | COL98 | 2026-06-01 | 2 | 1 |
| 204710 | Antasia Single Glass 1-Light Sconce | CAT15 | COL18 | 2025-12-01 | 2 | 1 |
| 204710 | Antasia Single Glass 1-Light Sconce | CAT15 | COL18 | 2026-01-01 | 6 | 1 |
| 204710 | Antasia Single Glass 1-Light Sconce | CAT15 | COL18 | 2026-02-01 | 8 | 4 |
| 204710 | Antasia Single Glass 1-Light Sconce | CAT15 | COL18 | 2026-04-01 | 4 | 1 |
| 204710 | Antasia Single Glass 1-Light Sconce | CAT15 | COL18 | 2026-05-01 | 5 | 3 |
| 204710 | Antasia Single Glass 1-Light Sconce | CAT15 | COL18 | 2026-06-01 | 7 | 1 |
| 204712 | Antasia Double Glass 1-Light Sconce | CAT15 | COL18 | 2026-01-01 | 3 | 2 |
| 204712 | Antasia Double Glass 1-Light Sconce | CAT15 | COL18 | 2026-02-01 | 6 | 3 |
| 204712 | Antasia Double Glass 1-Light Sconce | CAT15 | COL18 | 2026-03-01 | 6 | 2 |
| 204712 | Antasia Double Glass 1-Light Sconce | CAT15 | COL18 | 2026-04-01 | 2 | 1 |
| 204712 | Antasia Double Glass 1-Light Sconce | CAT15 | COL18 | 2026-05-01 | 3 | 1 |
| 204750 | Mediki Sconce | CAT15 | COL99 | 2026-01-01 | 2 | 1 |
| 204750 | Mediki Sconce | CAT15 | COL99 | 2026-02-01 | 4 | 1 |
| 204750 | Mediki Sconce | CAT15 | COL99 | 2026-05-01 | 9 | 2 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2025-12-01 | 3 | 1 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2026-01-01 | 4 | 2 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2026-02-01 | 4 | 2 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2026-03-01 | 19 | 8 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2026-04-01 | 9 | 3 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2026-05-01 | 3 | 3 |
| 204790 | Dune Sconce | CAT15 | DUNE | 2026-06-01 | 5 | 2 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2025-12-01 | 9 | 3 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2026-01-01 | 6 | 2 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2026-02-01 | 21 | 6 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2026-03-01 | 19 | 8 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2026-04-01 | 32 | 10 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2026-05-01 | 12 | 5 |
| 204795 | Dune Large Sconce | CAT15 | DUNE | 2026-06-01 | 6 | 3 |
| 204810 | Beacon Hall Oval Drum Shade Sconce | CAT15 | COL31 | 2026-01-01 | 6 | 3 |
| 204810 | Beacon Hall Oval Drum Shade Sconce | CAT15 | COL31 | 2026-03-01 | 2 | 1 |
| 204810 | Beacon Hall Oval Drum Shade Sconce | CAT15 | COL31 | 2026-04-01 | 3 | 2 |
| 204810 | Beacon Hall Oval Drum Shade Sconce | CAT15 | COL31 | 2026-05-01 | 6 | 3 |
| 204810 | Beacon Hall Oval Drum Shade Sconce | CAT15 | COL31 | 2026-06-01 | 2 | 1 |
| 204820 | Beacon Hall Ellipse Glass Sconce | CAT15 | COL31 | 2026-01-01 | 15 | 6 |
| 204820 | Beacon Hall Ellipse Glass Sconce | CAT15 | COL31 | 2026-02-01 | 1 | 1 |
| 204820 | Beacon Hall Ellipse Glass Sconce | CAT15 | COL31 | 2026-03-01 | 7 | 3 |
| 204820 | Beacon Hall Ellipse Glass Sconce | CAT15 | COL31 | 2026-04-01 | 4 | 1 |
| 204820 | Beacon Hall Ellipse Glass Sconce | CAT15 | COL31 | 2026-05-01 | 7 | 3 |
| 204825 | Beacon Hall Half Cone Glass Sconce | CAT15 | COL31 | 2025-12-01 | 2 | 1 |
| 204825 | Beacon Hall Half Cone Glass Sconce | CAT15 | COL31 | 2026-02-01 | 4 | 2 |
| 204825 | Beacon Hall Half Cone Glass Sconce | CAT15 | COL31 | 2026-03-01 | 9 | 3 |
| 204825 | Beacon Hall Half Cone Glass Sconce | CAT15 | COL31 | 2026-05-01 | 1 | 1 |
| 204826 | Beacon Hall Half Drum Shade Sconce | CAT15 | COL31 | 2025-12-01 | 3 | 2 |
| 204826 | Beacon Hall Half Drum Shade Sconce | CAT15 | COL31 | 2026-01-01 | 2 | 1 |
| 204826 | Beacon Hall Half Drum Shade Sconce | CAT15 | COL31 | 2026-02-01 | 4 | 1 |
| 204826 | Beacon Hall Half Drum Shade Sconce | CAT15 | COL31 | 2026-03-01 | 8 | 4 |
| 204826 | Beacon Hall Half Drum Shade Sconce | CAT15 | COL31 | 2026-05-01 | 4 | 2 |
| 204826 | Beacon Hall Half Drum Shade Sconce | CAT15 | COL31 | 2026-06-01 | 9 | 1 |
| 205122 | Forged Leaf Sconce | CAT15 | LEAF | 2026-01-01 | 1 | 1 |
| 205122 | Forged Leaf Sconce | CAT15 | LEAF | 2026-02-01 | 8 | 5 |
| 205122 | Forged Leaf Sconce | CAT15 | LEAF | 2026-03-01 | 13 | 5 |
| 205122 | Forged Leaf Sconce | CAT15 | LEAF | 2026-04-01 | 2 | 1 |
| 205122 | Forged Leaf Sconce | CAT15 | LEAF | 2026-05-01 | 5 | 3 |
| 205401 | Twine Sconce | CAT15 | TWINE | 2026-01-01 | 2 | 2 |
| 205401 | Twine Sconce | CAT15 | TWINE | 2026-02-01 | 5 | 2 |
| 205401 | Twine Sconce | CAT15 | TWINE | 2026-03-01 | 9 | 4 |
| 205401 | Twine Sconce | CAT15 | TWINE | 2026-04-01 | 9 | 2 |
| 205401 | Twine Sconce | CAT15 | TWINE | 2026-06-01 | 6 | 2 |
| 205420 | Alison's Leaves Sconce | CAT15 | COL100 | 2025-12-01 | 4 | 2 |
| 205420 | Alison's Leaves Sconce | CAT15 | COL100 | 2026-01-01 | 3 | 2 |
| 205420 | Alison's Leaves Sconce | CAT15 | COL100 | 2026-02-01 | 1 | 1 |
| 205420 | Alison's Leaves Sconce | CAT15 | COL100 | 2026-03-01 | 5 | 2 |
| 205420 | Alison's Leaves Sconce | CAT15 | COL100 | 2026-04-01 | 15 | 4 |
| 205420 | Alison's Leaves Sconce | CAT15 | COL100 | 2026-05-01 | 8 | 4 |
| 205440 | Rhapsody LED Sconce | CAT15 | COL101 | 2026-03-01 | 3 | 1 |
| 205440 | Rhapsody LED Sconce | CAT15 | COL101 | 2026-04-01 | 2 | 1 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2025-12-01 | 4 | 2 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2026-01-01 | 7 | 3 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2026-02-01 | 10 | 4 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2026-03-01 | 16 | 7 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2026-04-01 | 15 | 7 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2026-05-01 | 16 | 7 |
| 205770 | Forged Leaf and Stem Sconce | CAT15 | LEAF | 2026-06-01 | 4 | 2 |
| 205812 | Banded Sconce | CAT15 | COL16 | 2025-12-01 | 1 | 2 |
| 205812 | Banded Sconce | CAT15 | COL16 | 2026-01-01 | 24 | 8 |
| 205812 | Banded Sconce | CAT15 | COL16 | 2026-02-01 | 1 | 1 |
| 205812 | Banded Sconce | CAT15 | COL16 | 2026-03-01 | 8 | 3 |
| 205812 | Banded Sconce | CAT15 | COL16 | 2026-04-01 | 12 | 3 |
| 205812 | Banded Sconce | CAT15 | COL16 | 2026-05-01 | 2 | 1 |
| 205814 | Torch Indoor Sconce | CAT15 | TORCH | 2026-01-01 | 6 | 2 |
| 205814 | Torch Indoor Sconce | CAT15 | TORCH | 2026-02-01 | 2 | 1 |
| 205814 | Torch Indoor Sconce | CAT15 | TORCH | 2026-03-01 | 5 | 1 |
| 205814 | Torch Indoor Sconce | CAT15 | TORCH | 2026-04-01 | 3 | 1 |
| 205814 | Torch Indoor Sconce | CAT15 | TORCH | 2026-05-01 | 2 | 1 |
| 205892 | Banded with Bar Sconce | CAT15 | COL16 | 2026-01-01 | 7 | 2 |
| 205892 | Banded with Bar Sconce | CAT15 | COL16 | 2026-02-01 | 1 | 2 |
| 205892 | Banded with Bar Sconce | CAT15 | COL16 | 2026-03-01 | 1 | 1 |
| 205892 | Banded with Bar Sconce | CAT15 | COL16 | 2026-04-01 | 1 | 1 |
| 205892 | Banded with Bar Sconce | CAT15 | COL16 | 2026-05-01 | 1 | 1 |
| 205894 | — | — | — | 2026-04-01 | 1 | 1 |
| 205910 | Extended Bars Sconce | CAT15 | COL16 | 2025-12-01 | 1 | 1 |
| 205910 | Extended Bars Sconce | CAT15 | COL16 | 2026-01-01 | 5 | 3 |
| 205910 | Extended Bars Sconce | CAT15 | COL16 | 2026-02-01 | 2 | 1 |
| 205910 | Extended Bars Sconce | CAT15 | COL16 | 2026-03-01 | 2 | 1 |
| 205950 | Bento Sconce | CAT15 | BENTO | 2025-12-01 | 4 | 1 |
| 205950 | Bento Sconce | CAT15 | BENTO | 2026-01-01 | 6 | 2 |
| 205950 | Bento Sconce | CAT15 | BENTO | 2026-02-01 | 6 | 2 |
| 205950 | Bento Sconce | CAT15 | BENTO | 2026-03-01 | 3 | 2 |
| 205950 | Bento Sconce | CAT15 | BENTO | 2026-04-01 | 10 | 3 |
| 205956 | Bento Large LED Sconce | CAT15 | BENTO | 2026-01-01 | 6 | 1 |
| 205956 | Bento Large LED Sconce | CAT15 | BENTO | 2026-02-01 | 12 | 2 |
| 205956 | Bento Large LED Sconce | CAT15 | BENTO | 2026-03-01 | 3 | 2 |
| 205956 | Bento Large LED Sconce | CAT15 | BENTO | 2026-04-01 | 20 | 4 |
| 205956 | Bento Large LED Sconce | CAT15 | BENTO | 2026-05-01 | 2 | 2 |
| 205956 | Bento Large LED Sconce | CAT15 | BENTO | 2026-06-01 | 3 | 1 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2025-12-01 | 3 | 2 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2026-01-01 | 2 | 1 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2026-02-01 | 3 | 3 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2026-03-01 | 4 | 4 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2026-04-01 | 1 | 1 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2026-05-01 | 4 | 3 |
| 206050 | Sprig Sconce | CAT15 | SPRIG | 2026-06-01 | 1 | 1 |
| 206101 | Flux Sconce | CAT15 | FLUX | 2025-12-01 | 4 | 2 |
| 206101 | Flux Sconce | CAT15 | FLUX | 2026-01-01 | 1 | 1 |
| 206101 | Flux Sconce | CAT15 | FLUX | 2026-02-01 | 2 | 1 |
| 206101 | Flux Sconce | CAT15 | FLUX | 2026-03-01 | 2 | 1 |
| 206120 | Folio Sconce | CAT15 | FOLIO | 2026-01-01 | 11 | 5 |
| 206120 | Folio Sconce | CAT15 | FOLIO | 2026-02-01 | 2 | 1 |
| 206120 | Folio Sconce | CAT15 | FOLIO | 2026-03-01 | 4 | 2 |
| 206120 | Folio Sconce | CAT15 | FOLIO | 2026-04-01 | 4 | 1 |
| 206120 | Folio Sconce | CAT15 | FOLIO | 2026-05-01 | 4 | 2 |
| 206120 | Folio Sconce | CAT15 | FOLIO | 2026-06-01 | 1 | 1 |
| 206251 | Banded Wall Torch Sconce | CAT15 | COL16 | 2026-01-01 | 13 | 6 |
| 206251 | Banded Wall Torch Sconce | CAT15 | COL16 | 2026-02-01 | 2 | 1 |
| 206251 | Banded Wall Torch Sconce | CAT15 | COL16 | 2026-03-01 | 5 | 3 |
| 206251 | Banded Wall Torch Sconce | CAT15 | COL16 | 2026-04-01 | 5 | 3 |
| 206251 | Banded Wall Torch Sconce | CAT15 | COL16 | 2026-05-01 | 2 | 2 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2025-12-01 | 2 | 1 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2026-01-01 | 3 | 2 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2026-02-01 | 10 | 5 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2026-03-01 | 10 | 5 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2026-04-01 | 11 | 4 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2026-05-01 | 5 | 3 |
| 206301 | Ondrian 1-Light Sconce | CAT15 | COL56 | 2026-06-01 | 6 | 3 |
| 206350 | Cosmo Sconce | CAT15 | COSMO | 2026-01-01 | 1 | 1 |
| 206350 | Cosmo Sconce | CAT15 | COSMO | 2026-05-01 | 2 | 1 |
| 206350 | Cosmo Sconce | CAT15 | COSMO | 2026-06-01 | 2 | 1 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2025-12-01 | 6 | 3 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2026-01-01 | 5 | 4 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2026-02-01 | 5 | 4 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2026-03-01 | 0 | 1 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2026-04-01 | 2 | 2 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2026-05-01 | 2 | 2 |
| 206401 | Axis Sconce | CAT15 | AXIS | 2026-06-01 | 2 | 2 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2025-12-01 | 4 | 4 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2026-01-01 | 3 | 2 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2026-02-01 | 3 | 3 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2026-03-01 | 2 | 1 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2026-04-01 | 5 | 4 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2026-05-01 | 5 | 5 |
| 206410 | Axis Large Sconce | CAT15 | AXIS | 2026-06-01 | 1 | 1 |
| 206440 | Double Axis Small Sconce | CAT15 | AXIS | 2026-01-01 | 2 | 1 |
| 206440 | Double Axis Small Sconce | CAT15 | AXIS | 2026-02-01 | 9 | 2 |
| 206450 | Airis Small Sconce | CAT15 | AIRIS | 2026-02-01 | 2 | 1 |
| 206450 | Airis Small Sconce | CAT15 | AIRIS | 2026-03-01 | 5 | 3 |
| 206450 | Airis Small Sconce | CAT15 | AIRIS | 2026-05-01 | 0 | 1 |
| 206455 | Airis Sconce | CAT15 | AIRIS | 2025-12-01 | 10 | 2 |
| 206455 | Airis Sconce | CAT15 | AIRIS | 2026-02-01 | 6 | 2 |
| 206455 | Airis Sconce | CAT15 | AIRIS | 2026-03-01 | 3 | 1 |
| 206455 | Airis Sconce | CAT15 | AIRIS | 2026-04-01 | 3 | 1 |
| 206501 | Corona Sconce | CAT15 | COL26 | 2025-12-01 | 2 | 1 |
| 206501 | Corona Sconce | CAT15 | COL26 | 2026-01-01 | 4 | 2 |
| 206501 | Corona Sconce | CAT15 | COL26 | 2026-02-01 | 3 | 2 |
| 206501 | Corona Sconce | CAT15 | COL26 | 2026-03-01 | 12 | 4 |
| 206501 | Corona Sconce | CAT15 | COL26 | 2026-05-01 | 2 | 1 |
| 206501 | Corona Sconce | CAT15 | COL26 | 2026-06-01 | 4 | 1 |
| 206503 | Corona Large Sconce | CAT15 | COL26 | 2026-01-01 | 2 | 1 |
| 206551 | Suspended Half Cone Sconce | CAT15 | COL104 | 2026-01-01 | 6 | 3 |
| 206551 | Suspended Half Cone Sconce | CAT15 | COL104 | 2026-02-01 | 1 | 1 |
| 206551 | Suspended Half Cone Sconce | CAT15 | COL104 | 2026-03-01 | 3 | 2 |
| 206551 | Suspended Half Cone Sconce | CAT15 | COL104 | 2026-04-01 | 2 | 1 |
| 206551 | Suspended Half Cone Sconce | CAT15 | COL104 | 2026-05-01 | 4 | 2 |
| 206551 | Suspended Half Cone Sconce | CAT15 | COL104 | 2026-06-01 | 2 | 1 |
| 206563 | Half Cone Sconce | CAT15 | COL104 | 2025-12-01 | 1 | 1 |
| 206563 | Half Cone Sconce | CAT15 | COL104 | 2026-01-01 | 11 | 4 |
| 206563 | Half Cone Sconce | CAT15 | COL104 | 2026-02-01 | 4 | 1 |
| 206563 | Half Cone Sconce | CAT15 | COL104 | 2026-03-01 | 12 | 3 |
| 206563 | Half Cone Sconce | CAT15 | COL104 | 2026-04-01 | 10 | 3 |
| 206563 | Half Cone Sconce | CAT15 | COL104 | 2026-05-01 | 6 | 3 |
| 206601 | Wren 1-Light Sconce | CAT15 | WREN | 2026-01-01 | 6 | 2 |
| 206601 | Wren 1-Light Sconce | CAT15 | WREN | 2026-02-01 | 2 | 2 |
| 206601 | Wren 1-Light Sconce | CAT15 | WREN | 2026-03-01 | 4 | 2 |
| 206601 | Wren 1-Light Sconce | CAT15 | WREN | 2026-04-01 | 8 | 3 |
| 206601 | Wren 1-Light Sconce | CAT15 | WREN | 2026-05-01 | 5 | 3 |
| 206601 | Wren 1-Light Sconce | CAT15 | WREN | 2026-06-01 | 3 | 2 |
| 206603 | Wren 3-Light Sconce | CAT15 | WREN | 2026-02-01 | 1 | 1 |
| 206603 | Wren 3-Light Sconce | CAT15 | WREN | 2026-03-01 | 1 | 1 |
| 206603 | Wren 3-Light Sconce | CAT15 | WREN | 2026-05-01 | 1 | 1 |
| 206729 | Forged Vertical Bar Sconce | CAT15 | COL105 | 2026-01-01 | 3 | 1 |
| 206729 | Forged Vertical Bar Sconce | CAT15 | COL105 | 2026-02-01 | 3 | 1 |
| 206729 | Forged Vertical Bar Sconce | CAT15 | COL105 | 2026-03-01 | 9 | 5 |
| 206729 | Forged Vertical Bar Sconce | CAT15 | COL105 | 2026-04-01 | 2 | 1 |
| 206729 | Forged Vertical Bar Sconce | CAT15 | COL105 | 2026-05-01 | 5 | 3 |
| 206730 | Forged Vertical Bar Large Sconce | CAT15 | COL105 | 2026-01-01 | 7 | 4 |
| 206730 | Forged Vertical Bar Large Sconce | CAT15 | COL105 | 2026-02-01 | 6 | 3 |
| 206730 | Forged Vertical Bar Large Sconce | CAT15 | COL105 | 2026-03-01 | 2 | 1 |
| 206730 | Forged Vertical Bar Large Sconce | CAT15 | COL105 | 2026-04-01 | 9 | 5 |
| 206730 | Forged Vertical Bar Large Sconce | CAT15 | COL105 | 2026-05-01 | 1 | 1 |
| 206740 | Forged Vertical Bars Sconce | CAT15 | COL105 | 2026-02-01 | 9 | 5 |
| 206740 | Forged Vertical Bars Sconce | CAT15 | COL105 | 2026-03-01 | 5 | 3 |
| 206740 | Forged Vertical Bars Sconce | CAT15 | COL105 | 2026-04-01 | 1 | 1 |
| 206740 | Forged Vertical Bars Sconce | CAT15 | COL105 | 2026-05-01 | 10 | 2 |
| 207370 | Oval Impressions Sconce | CAT15 | COL22 | 2025-12-01 | 4 | 2 |
| 207370 | Oval Impressions Sconce | CAT15 | COL22 | 2026-01-01 | 8 | 5 |
| 207370 | Oval Impressions Sconce | CAT15 | COL22 | 2026-02-01 | 6 | 3 |
| 207370 | Oval Impressions Sconce | CAT15 | COL22 | 2026-03-01 | 4 | 2 |
| 207370 | Oval Impressions Sconce | CAT15 | COL22 | 2026-04-01 | 1 | 1 |
| 207370 | Oval Impressions Sconce | CAT15 | COL22 | 2026-05-01 | 7 | 3 |
| 207420 | Cirque Sconce | CAT15 | COL32 | 2026-01-01 | 9 | 4 |
| 207420 | Cirque Sconce | CAT15 | COL32 | 2026-02-01 | 2 | 1 |
| 207420 | Cirque Sconce | CAT15 | COL32 | 2026-03-01 | 2 | 1 |
| 207420 | Cirque Sconce | CAT15 | COL32 | 2026-04-01 | 2 | 1 |
| 207521 | Arc Ellipse 1-Light Sconce | CAT15 | COL48 | 2026-01-01 | 4 | 1 |
| 207521 | Arc Ellipse 1-Light Sconce | CAT15 | COL48 | 2026-03-01 | 6 | 3 |
| 207521 | Arc Ellipse 1-Light Sconce | CAT15 | COL48 | 2026-04-01 | 16 | 1 |
| 207521 | Arc Ellipse 1-Light Sconce | CAT15 | COL48 | 2026-05-01 | 3 | 2 |
| 207522 | Arc Ellipse 2-Light Sconce | CAT15 | COL48 | 2025-12-01 | 1 | 1 |
| 207522 | Arc Ellipse 2-Light Sconce | CAT15 | COL48 | 2026-01-01 | 3 | 3 |
| 207522 | Arc Ellipse 2-Light Sconce | CAT15 | COL48 | 2026-02-01 | 4 | 3 |
| 207522 | Arc Ellipse 2-Light Sconce | CAT15 | COL48 | 2026-03-01 | 3 | 2 |
| 207522 | Arc Ellipse 2-Light Sconce | CAT15 | COL48 | 2026-04-01 | 3 | 3 |
| 207522 | Arc Ellipse 2-Light Sconce | CAT15 | COL48 | 2026-06-01 | 2 | 1 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2025-12-01 | 2 | 1 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2026-01-01 | 6 | 3 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2026-02-01 | 7 | 5 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2026-03-01 | 6 | 4 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2026-04-01 | 2 | 1 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2026-05-01 | 3 | 3 |
| 207523 | Arc Ellipse 3-Light Sconce | CAT15 | COL48 | 2026-06-01 | 2 | 2 |
| 207525 | Arc Ellipse 5-Light Sconce | CAT15 | COL48 | 2025-12-01 | 1 | 1 |
| 207525 | Arc Ellipse 5-Light Sconce | CAT15 | COL48 | 2026-01-01 | 2 | 1 |
| 207525 | Arc Ellipse 5-Light Sconce | CAT15 | COL48 | 2026-02-01 | 2 | 2 |
| 207525 | Arc Ellipse 5-Light Sconce | CAT15 | COL48 | 2026-03-01 | 4 | 3 |
| 207525 | Arc Ellipse 5-Light Sconce | CAT15 | COL48 | 2026-04-01 | 2 | 2 |
| 207525 | Arc Ellipse 5-Light Sconce | CAT15 | COL48 | 2026-05-01 | 1 | 1 |
| 207640 | Arbo Sconce | CAT15 | ARBO | 2025-12-01 | 4 | 2 |
| 207640 | Arbo Sconce | CAT15 | ARBO | 2026-01-01 | 0 | 1 |
| 207640 | Arbo Sconce | CAT15 | ARBO | 2026-02-01 | 5 | 3 |
| 207640 | Arbo Sconce | CAT15 | ARBO | 2026-03-01 | 5 | 3 |
| 207640 | Arbo Sconce | CAT15 | ARBO | 2026-04-01 | 2 | 1 |
| 207660 | Brindille Sconce | CAT15 | COL24 | 2026-01-01 | 3 | 2 |
| 207660 | Brindille Sconce | CAT15 | COL24 | 2026-02-01 | 2 | 2 |
| 207660 | Brindille Sconce | CAT15 | COL24 | 2026-03-01 | 3 | 2 |
| 207660 | Brindille Sconce | CAT15 | COL24 | 2026-05-01 | 2 | 1 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2025-12-01 | 2 | 1 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2026-01-01 | 20 | 2 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2026-02-01 | 2 | 1 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2026-03-01 | 7 | 5 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2026-04-01 | 8 | 4 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2026-05-01 | 15 | 9 |
| 207670 | Brindille Sconce | CAT15 | COL24 | 2026-06-01 | 4 | 1 |
| 207675 | Cavaletti Sconce | CAT15 | COL51 | 2026-02-01 | 1 | 1 |
| 207675 | Cavaletti Sconce | CAT15 | COL51 | 2026-03-01 | 1 | 2 |
| 207675 | Cavaletti Sconce | CAT15 | COL51 | 2026-04-01 | 6 | 2 |
| 207675 | Cavaletti Sconce | CAT15 | COL51 | 2026-05-01 | 5 | 2 |
| 207680 | Exos Rectangular Sconce | CAT15 | EXOS | 2025-12-01 | 3 | 2 |
| 207680 | Exos Rectangular Sconce | CAT15 | EXOS | 2026-01-01 | 2 | 1 |
| 207680 | Exos Rectangular Sconce | CAT15 | EXOS | 2026-02-01 | 3 | 1 |
| 207680 | Exos Rectangular Sconce | CAT15 | EXOS | 2026-04-01 | 1 | 1 |
| 207680 | Exos Rectangular Sconce | CAT15 | EXOS | 2026-05-01 | 2 | 1 |
| 207693 | Oceanus 1-Light Sconce | CAT15 | COL21 | 2026-01-01 | 4 | 1 |
| 207693 | Oceanus 1-Light Sconce | CAT15 | COL21 | 2026-03-01 | 5 | 2 |
| 207693 | Oceanus 1-Light Sconce | CAT15 | COL21 | 2026-04-01 | 2 | 1 |
| 207693 | Oceanus 1-Light Sconce | CAT15 | COL21 | 2026-05-01 | 1 | 1 |
| 207693 | Oceanus 1-Light Sconce | CAT15 | COL21 | 2026-06-01 | 4 | 2 |
| 207695 | Oceanus 2-Light Sconce | CAT15 | COL21 | 2025-12-01 | 2 | 1 |
| 207695 | Oceanus 2-Light Sconce | CAT15 | COL21 | 2026-03-01 | 3 | 2 |
| 207695 | Oceanus 2-Light Sconce | CAT15 | COL21 | 2026-04-01 | 4 | 1 |
| 207695 | Oceanus 2-Light Sconce | CAT15 | COL21 | 2026-05-01 | 2 | 1 |
| 207697 | Oceanus 3-Light Sconce | CAT15 | COL21 | 2026-01-01 | 2 | 2 |
| 207697 | Oceanus 3-Light Sconce | CAT15 | COL21 | 2026-02-01 | 1 | 1 |
| 207697 | Oceanus 3-Light Sconce | CAT15 | COL21 | 2026-04-01 | 1 | 1 |
| 207697 | Oceanus 3-Light Sconce | CAT15 | COL21 | 2026-05-01 | 2 | 1 |
| 207710 | Erlenmeyer Sconce | CAT15 | COL25 | 2025-12-01 | 4 | 1 |
| 207710 | Erlenmeyer Sconce | CAT15 | COL25 | 2026-01-01 | 5 | 3 |
| 207710 | Erlenmeyer Sconce | CAT15 | COL25 | 2026-02-01 | 4 | 2 |
| 207710 | Erlenmeyer Sconce | CAT15 | COL25 | 2026-03-01 | 16 | 3 |
| 207710 | Erlenmeyer Sconce | CAT15 | COL25 | 2026-04-01 | 4 | 2 |
| 207710 | Erlenmeyer Sconce | CAT15 | COL25 | 2026-05-01 | 2 | 1 |
| 207720 | Erlenmeyer ADA Sconce | CAT15 | COL25 | 2025-12-01 | 5 | 3 |
| 207720 | Erlenmeyer ADA Sconce | CAT15 | COL25 | 2026-01-01 | 6 | 2 |
| 207720 | Erlenmeyer ADA Sconce | CAT15 | COL25 | 2026-02-01 | 2 | 1 |
| 207720 | Erlenmeyer ADA Sconce | CAT15 | COL25 | 2026-03-01 | 7 | 2 |
| 207720 | Erlenmeyer ADA Sconce | CAT15 | COL25 | 2026-04-01 | 10 | 2 |
| 207720 | Erlenmeyer ADA Sconce | CAT15 | COL25 | 2026-05-01 | 10 | 5 |
| 207765 | Ethos Large LED Sconce | CAT15 | ETHOS | 2025-12-01 | 2 | 1 |
| 207765 | Ethos Large LED Sconce | CAT15 | ETHOS | 2026-02-01 | 2 | 1 |
| 207765 | Ethos Large LED Sconce | CAT15 | ETHOS | 2026-03-01 | 1 | 1 |
| 207765 | Ethos Large LED Sconce | CAT15 | ETHOS | 2026-04-01 | 4 | 1 |
| 207765 | Ethos Large LED Sconce | CAT15 | ETHOS | 2026-05-01 | 2 | 1 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2025-12-01 | 2 | 1 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2026-01-01 | 4 | 2 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2026-02-01 | 12 | 4 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2026-03-01 | 5 | 3 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2026-04-01 | 5 | 3 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2026-05-01 | 8 | 2 |
| 207801 | Ondrian 2-Light Sconce | CAT15 | COL56 | 2026-06-01 | 2 | 1 |
| 207821 | Kakomi 1-Light Sconce | CAT15 | COL107 | 2026-01-01 | 1 | 1 |
| 207821 | Kakomi 1-Light Sconce | CAT15 | COL107 | 2026-02-01 | 3 | 1 |
| 207821 | Kakomi 1-Light Sconce | CAT15 | COL107 | 2026-03-01 | 3 | 1 |
| 207831 | Kakomi 1-Light Sconce | CAT15 | COL107 | 2026-04-01 | 8 | 1 |
| 207831 | Kakomi 1-Light Sconce | CAT15 | COL107 | 2026-05-01 | 2 | 1 |
| 207833 | Kakomi 3-Light Sconce | CAT15 | COL107 | 2025-12-01 | 4 | 1 |
| 207833 | Kakomi 3-Light Sconce | CAT15 | COL107 | 2026-01-01 | 0 | 1 |
| 207833 | Kakomi 3-Light Sconce | CAT15 | COL107 | 2026-02-01 | 1 | 1 |
| 207833 | Kakomi 3-Light Sconce | CAT15 | COL107 | 2026-03-01 | 3 | 3 |
| 207833 | Kakomi 3-Light Sconce | CAT15 | COL107 | 2026-04-01 | 1 | 1 |
| 207833 | Kakomi 3-Light Sconce | CAT15 | COL107 | 2026-06-01 | 1 | 1 |
| 207843 | Impressions 3-Light Sconce | CAT15 | COL22 | 2026-01-01 | 5 | 3 |
| 207843 | Impressions 3-Light Sconce | CAT15 | COL22 | 2026-02-01 | 1 | 1 |
| 207843 | Impressions 3-Light Sconce | CAT15 | COL22 | 2026-03-01 | 2 | 2 |
| 207843 | Impressions 3-Light Sconce | CAT15 | COL22 | 2026-04-01 | 1 | 1 |
| 207843 | Impressions 3-Light Sconce | CAT15 | COL22 | 2026-05-01 | 2 | 1 |
| 207858 | After Hours Sconce | CAT15 | COL108 | 2026-01-01 | 7 | 3 |
| 207858 | After Hours Sconce | CAT15 | COL108 | 2026-02-01 | 6 | 4 |
| 207858 | After Hours Sconce | CAT15 | COL108 | 2026-03-01 | 10 | 3 |
| 207858 | After Hours Sconce | CAT15 | COL108 | 2026-04-01 | 9 | 4 |
| 207858 | After Hours Sconce | CAT15 | COL108 | 2026-05-01 | 5 | 2 |
| 207901 | Otto Sconce | CAT15 | OTTO | 2026-02-01 | 4 | 3 |
| 207901 | Otto Sconce | CAT15 | OTTO | 2026-03-01 | 6 | 2 |
| 207901 | Otto Sconce | CAT15 | OTTO | 2026-04-01 | 2 | 1 |
| 207901 | Otto Sconce | CAT15 | OTTO | 2026-05-01 | 4 | 2 |
| 207901 | Otto Sconce | CAT15 | OTTO | 2026-06-01 | 1 | 1 |
| 207903 | Otto Sphere Sconce | CAT15 | OTTO | 2026-01-01 | 1 | 1 |
| 207903 | Otto Sphere Sconce | CAT15 | OTTO | 2026-02-01 | 6 | 3 |
| 207903 | Otto Sphere Sconce | CAT15 | OTTO | 2026-03-01 | 7 | 2 |
| 207910 | — | — | — | 2026-03-01 | 1 | 1 |
| 207915 | — | — | — | 2025-12-01 | 4 | 1 |
| 207918 | Solitude LED Sconce | CAT15 | COL69 | 2026-02-01 | 5 | 3 |
| 207918 | Solitude LED Sconce | CAT15 | COL69 | 2026-05-01 | 1 | 1 |
| 208903 | Fritz Globe Sconce | CAT15 | FRITZ | 2026-01-01 | 2 | 1 |
| 208903 | Fritz Globe Sconce | CAT15 | FRITZ | 2026-03-01 | 2 | 1 |
| 208903 | Fritz Globe Sconce | CAT15 | FRITZ | 2026-04-01 | 4 | 1 |
| 209105 | Libra LED Sconce | CAT15 | LIBRA | 2025-12-01 | 10 | 1 |
| 209105 | Libra LED Sconce | CAT15 | LIBRA | 2026-01-01 | 1 | 1 |
| 209105 | Libra LED Sconce | CAT15 | LIBRA | 2026-02-01 | 1 | 1 |
| 209105 | Libra LED Sconce | CAT15 | LIBRA | 2026-03-01 | 1 | 1 |
| 209105 | Libra LED Sconce | CAT15 | LIBRA | 2026-06-01 | 2 | 1 |
| 209120 | Willow Sconce | CAT15 | COL28 | 2026-01-01 | 2 | 1 |
| 209120 | Willow Sconce | CAT15 | COL28 | 2026-02-01 | 2 | 1 |
| 209120 | Willow Sconce | CAT15 | COL28 | 2026-04-01 | 6 | 3 |
| 209120 | Willow Sconce | CAT15 | COL28 | 2026-05-01 | 5 | 3 |
| 209120 | Willow Sconce | CAT15 | COL28 | 2026-06-01 | 5 | 3 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2025-12-01 | 12 | 6 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2026-01-01 | 13 | 7 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2026-02-01 | 11 | 5 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2026-03-01 | 24 | 13 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2026-04-01 | 10 | 5 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2026-05-01 | 16 | 8 |
| 209250 | Simple Swing Arm Sconce | CAT15 | COL11 | 2026-06-01 | 4 | 2 |
| 209320 | Henry Sconce | CAT15 | HENRY | 2025-12-01 | 4 | 2 |
| 209320 | Henry Sconce | CAT15 | HENRY | 2026-01-01 | 7 | 4 |
| 209320 | Henry Sconce | CAT15 | HENRY | 2026-02-01 | 2 | 1 |
| 209320 | Henry Sconce | CAT15 | HENRY | 2026-03-01 | 17 | 7 |
| 209320 | Henry Sconce | CAT15 | HENRY | 2026-05-01 | 2 | 2 |
| 209320 | Henry Sconce | CAT15 | HENRY | 2026-06-01 | 4 | 2 |
| 209321 | Henry Large Metal Shade Sconce | CAT15 | HENRY | 2026-02-01 | 1 | 1 |
| 209321 | Henry Large Metal Shade Sconce | CAT15 | HENRY | 2026-03-01 | 3 | 2 |
| 209321 | Henry Large Metal Shade Sconce | CAT15 | HENRY | 2026-04-01 | 2 | 1 |
| 209322 | Henry Large Glass Shade Sconce | CAT15 | HENRY | 2025-12-01 | 4 | 1 |
| 209322 | Henry Large Glass Shade Sconce | CAT15 | HENRY | 2026-02-01 | 1 | 1 |
| 209322 | Henry Large Glass Shade Sconce | CAT15 | HENRY | 2026-03-01 | 5 | 3 |
| 209322 | Henry Large Glass Shade Sconce | CAT15 | HENRY | 2026-04-01 | 2 | 1 |
| 209322 | Henry Large Glass Shade Sconce | CAT15 | HENRY | 2026-05-01 | 2 | 2 |
| 209323 | Henry Small Metal Shade Sconce | CAT15 | HENRY | 2026-01-01 | 1 | 1 |
| 209323 | Henry Small Metal Shade Sconce | CAT15 | HENRY | 2026-02-01 | 5 | 4 |
| 209323 | Henry Small Metal Shade Sconce | CAT15 | HENRY | 2026-04-01 | 3 | 1 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2025-12-01 | 2 | 1 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2026-01-01 | 1 | 1 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2026-02-01 | 3 | 2 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2026-03-01 | 1 | 1 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2026-04-01 | 6 | 3 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2026-05-01 | 3 | 3 |
| 209324 | Henry Small Glass Shade Sconce | CAT15 | HENRY | 2026-06-01 | 2 | 1 |
| 209325 | Henry Swing Arm Metal Shade Sconce | CAT15 | HENRY | 2025-12-01 | 2 | 1 |
| 209325 | Henry Swing Arm Metal Shade Sconce | CAT15 | HENRY | 2026-01-01 | 1 | 1 |
| 209325 | Henry Swing Arm Metal Shade Sconce | CAT15 | HENRY | 2026-02-01 | 3 | 2 |
| 209325 | Henry Swing Arm Metal Shade Sconce | CAT15 | HENRY | 2026-03-01 | 5 | 3 |
| 209326 | Henry Swing Arm Glass Shade Sconce | CAT15 | HENRY | 2026-01-01 | 3 | 2 |
| 209326 | Henry Swing Arm Glass Shade Sconce | CAT15 | HENRY | 2026-02-01 | 5 | 2 |
| 209326 | Henry Swing Arm Glass Shade Sconce | CAT15 | HENRY | 2026-03-01 | 1 | 1 |
| 209326 | Henry Swing Arm Glass Shade Sconce | CAT15 | HENRY | 2026-04-01 | 3 | 2 |
| 209326 | Henry Swing Arm Glass Shade Sconce | CAT15 | HENRY | 2026-05-01 | 4 | 3 |
| 209335 | — | — | — | 2026-01-01 | 4 | 2 |
| 209335 | — | — | — | 2026-02-01 | 1 | 1 |
| 209335 | — | — | — | 2026-03-01 | 5 | 2 |
| 209335 | — | — | — | 2026-06-01 | 5 | 2 |
| 209336 | — | — | — | 2026-01-01 | 4 | 1 |
| 209336 | — | — | — | 2026-03-01 | 1 | 1 |
| 209980 | Riverbed LED Sconce | CAT15 | COL91 | 2026-01-01 | 13 | 6 |
| 209980 | Riverbed LED Sconce | CAT15 | COL91 | 2026-02-01 | 5 | 5 |
| 209980 | Riverbed LED Sconce | CAT15 | COL91 | 2026-03-01 | 7 | 5 |
| 209980 | Riverbed LED Sconce | CAT15 | COL91 | 2026-04-01 | 28 | 8 |
| 209980 | Riverbed LED Sconce | CAT15 | COL91 | 2026-05-01 | 22 | 4 |
| 209980 | Riverbed LED Sconce | CAT15 | COL91 | 2026-06-01 | 12 | 2 |
| 212034 | Brindille 4-Light Large Sconce/Semi-Flush | CAT15 | COL24 | 2026-03-01 | 1 | 1 |
| 212034 | Brindille 4-Light Large Sconce/Semi-Flush | CAT15 | COL24 | 2026-05-01 | 1 | 1 |
| 213310 | Oculus Sconce/Flush Mount | CAT15 | COL111 | 2025-12-01 | 5 | 1 |
| 213310 | Oculus Sconce/Flush Mount | CAT15 | COL111 | 2026-01-01 | 9 | 2 |
| 213310 | Oculus Sconce/Flush Mount | CAT15 | COL111 | 2026-05-01 | 6 | 1 |
| 217185 | Forged Vertical Bar Sconce - Steel Backplate | CAT15 | COL105 | 2026-02-01 | 4 | 2 |
| 217185 | Forged Vertical Bar Sconce - Steel Backplate | CAT15 | COL105 | 2026-03-01 | 5 | 2 |
| 217185 | Forged Vertical Bar Sconce - Steel Backplate | CAT15 | COL105 | 2026-04-01 | 5 | 1 |
| 217185 | Forged Vertical Bar Sconce - Steel Backplate | CAT15 | COL105 | 2026-05-01 | 4 | 2 |
| 217185 | Forged Vertical Bar Sconce - Steel Backplate | CAT15 | COL105 | 2026-06-01 | 2 | 1 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2025-12-01 | 4 | 2 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2026-01-01 | 6 | 3 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2026-02-01 | 5 | 3 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2026-03-01 | 3 | 2 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2026-04-01 | 9 | 3 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2026-05-01 | 7 | 3 |
| 217186 | Forged Vertical Bar Sconce - Cherry or Copper B... | CAT15 | COL105 | 2026-06-01 | 10 | 2 |
| 217310 | Planar LED Sconce | CAT15 | COL65 | 2026-01-01 | 1 | 1 |
| 217310 | Planar LED Sconce | CAT15 | COL65 | 2026-02-01 | 7 | 2 |
| 217310 | Planar LED Sconce | CAT15 | COL65 | 2026-03-01 | 1 | 1 |
| 217310 | Planar LED Sconce | CAT15 | COL65 | 2026-05-01 | 2 | 2 |
| 217510 | Aperture Sconce | CAT15 | COL113 | 2025-12-01 | 8 | 1 |
| 217510 | Aperture Sconce | CAT15 | COL113 | 2026-01-01 | 3 | 2 |
| 217510 | Aperture Sconce | CAT15 | COL113 | 2026-03-01 | 2 | 1 |
| 217510 | Aperture Sconce | CAT15 | COL113 | 2026-04-01 | 3 | 2 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2025-12-01 | 2 | 1 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2026-01-01 | 22 | 4 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2026-02-01 | 4 | 2 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2026-03-01 | 2 | 1 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2026-04-01 | 10 | 3 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2026-05-01 | 28 | 1 |
| 217520 | Aperture Vertical Sconce | CAT15 | COL113 | 2026-06-01 | 2 | 1 |
| 217635 | Gallery Sconce | CAT15 | COL114 | 2025-12-01 | 4 | 2 |
| 217635 | Gallery Sconce | CAT15 | COL114 | 2026-01-01 | 12 | 4 |
| 217635 | Gallery Sconce | CAT15 | COL114 | 2026-02-01 | 4 | 2 |
| 217635 | Gallery Sconce | CAT15 | COL114 | 2026-03-01 | 14 | 3 |
| 217635 | Gallery Sconce | CAT15 | COL114 | 2026-04-01 | 6 | 1 |
| 217635 | Gallery Sconce | CAT15 | COL114 | 2026-05-01 | 4 | 2 |
| 217640 | Gallery Sconce | CAT15 | COL114 | 2026-01-01 | 5 | 3 |
| 217640 | Gallery Sconce | CAT15 | COL114 | 2026-02-01 | 1 | 1 |
| 217640 | Gallery Sconce | CAT15 | COL114 | 2026-03-01 | 3 | 2 |
| 217640 | Gallery Sconce | CAT15 | COL114 | 2026-06-01 | 2 | 1 |
| 217650 | Gallery Small Sconce | CAT15 | COL114 | 2025-12-01 | 9 | 2 |
| 217650 | Gallery Small Sconce | CAT15 | COL114 | 2026-02-01 | 3 | 3 |
| 217650 | Gallery Small Sconce | CAT15 | COL114 | 2026-03-01 | 6 | 2 |
| 217650 | Gallery Small Sconce | CAT15 | COL114 | 2026-04-01 | 7 | 1 |
| 217650 | Gallery Small Sconce | CAT15 | COL114 | 2026-05-01 | 4 | 2 |
| 217650 | Gallery Small Sconce | CAT15 | COL114 | 2026-06-01 | 10 | 1 |
| 217652 | Gallery LED Sconce | CAT15 | COL114 | 2025-12-01 | 2 | 1 |
| 217652 | Gallery LED Sconce | CAT15 | COL114 | 2026-01-01 | 5 | 2 |
| 217652 | Gallery LED Sconce | CAT15 | COL114 | 2026-02-01 | 2 | 1 |
| 217652 | Gallery LED Sconce | CAT15 | COL114 | 2026-05-01 | 12 | 2 |
| 217654 | Gallery Medium LED Sconce | CAT15 | COL114 | 2026-01-01 | 6 | 1 |
| 217654 | Gallery Medium LED Sconce | CAT15 | COL114 | 2026-03-01 | 4 | 1 |
| 217654 | Gallery Medium LED Sconce | CAT15 | COL114 | 2026-04-01 | 3 | 2 |
| 217654 | Gallery Medium LED Sconce | CAT15 | COL114 | 2026-05-01 | 13 | 3 |
| 217654 | Gallery Medium LED Sconce | CAT15 | COL114 | 2026-06-01 | 2 | 1 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2025-12-01 | 2 | 1 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2026-01-01 | 1 | 1 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2026-02-01 | 11 | 4 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2026-03-01 | 12 | 4 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2026-04-01 | 2 | 2 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2026-05-01 | 3 | 2 |
| 217656 | Gallery Large LED Sconce | CAT15 | COL114 | 2026-06-01 | 2 | 1 |
| 22043 | — | — | — | 2025-12-01 | 1 | 1 |
| 22043 | — | — | — | 2026-01-01 | 2 | 2 |
| 22043 | — | — | — | 2026-02-01 | 2 | 2 |
| 22043 | — | — | — | 2026-03-01 | 1 | 1 |
| 22043 | — | — | — | 2026-04-01 | 1 | 1 |
| 22043 | — | — | — | 2026-05-01 | 2 | 2 |
| 22051 | — | — | — | 2026-01-01 | 1 | 1 |
| 22052 | — | — | — | 2026-01-01 | 1 | 1 |
| 22052 | — | — | — | 2026-04-01 | 1 | 1 |
| 22054 | — | — | — | 2026-02-01 | 1 | 1 |
| 22054 | — | — | — | 2026-03-01 | 1 | 1 |
| 22058 | — | — | — | 2026-01-01 | 1 | 1 |
| 232665 | Stasis Floor Lamp | CAT9 | COL115 | 2025-12-01 | 1 | 1 |
| 232665 | Stasis Floor Lamp | CAT9 | COL115 | 2026-01-01 | 1 | 1 |
| 232665 | Stasis Floor Lamp | CAT9 | COL115 | 2026-02-01 | 3 | 3 |
| 232665 | Stasis Floor Lamp | CAT9 | COL115 | 2026-03-01 | 2 | 2 |
| 232665 | Stasis Floor Lamp | CAT9 | COL115 | 2026-05-01 | 2 | 2 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2025-12-01 | 1 | 1 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2026-01-01 | 3 | 2 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2026-02-01 | 3 | 3 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2026-03-01 | 4 | 4 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2026-04-01 | 3 | 3 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2026-05-01 | 4 | 4 |
| 232666 | Stasis Floor Lamp | CAT9 | COL115 | 2026-06-01 | 1 | 1 |
| 232686 | Almost Infinity Floor Lamp | CAT9 | COL116 | 2025-12-01 | 3 | 3 |
| 232686 | Almost Infinity Floor Lamp | CAT9 | COL116 | 2026-01-01 | 5 | 5 |
| 232686 | Almost Infinity Floor Lamp | CAT9 | COL116 | 2026-02-01 | 8 | 7 |
| 232686 | Almost Infinity Floor Lamp | CAT9 | COL116 | 2026-03-01 | 4 | 4 |
| 232686 | Almost Infinity Floor Lamp | CAT9 | COL116 | 2026-04-01 | 5 | 5 |
| 232686 | Almost Infinity Floor Lamp | CAT9 | COL116 | 2026-06-01 | 3 | 3 |
| 232720 | Contemporary Formae Floor Lamp | CAT9 | COL98 | 2026-01-01 | 1 | 1 |
| 232720 | Contemporary Formae Floor Lamp | CAT9 | COL98 | 2026-02-01 | 2 | 2 |
| 232805 | — | — | — | 2026-05-01 | 2 | 1 |
| 232810 | Antasia Floor Lamp | CAT9 | COL18 | 2025-12-01 | 2 | 2 |
| 232810 | Antasia Floor Lamp | CAT9 | COL18 | 2026-01-01 | 3 | 3 |
| 232810 | Antasia Floor Lamp | CAT9 | COL18 | 2026-02-01 | 1 | 1 |
| 232810 | Antasia Floor Lamp | CAT9 | COL18 | 2026-03-01 | 2 | 2 |
| 232810 | Antasia Floor Lamp | CAT9 | COL18 | 2026-05-01 | 1 | 1 |
| 232810 | Antasia Floor Lamp | CAT9 | COL18 | 2026-06-01 | 1 | 1 |
| 232850 | Facet Floor Lamp | CAT9 | FACET | 2026-01-01 | 2 | 2 |
| 232850 | Facet Floor Lamp | CAT9 | FACET | 2026-02-01 | 3 | 2 |
| 232850 | Facet Floor Lamp | CAT9 | FACET | 2026-03-01 | 3 | 3 |
| 232850 | Facet Floor Lamp | CAT9 | FACET | 2026-04-01 | 2 | 2 |
| 232850 | Facet Floor Lamp | CAT9 | FACET | 2026-05-01 | 2 | 2 |
| 232860 | Reach Floor Lamp | CAT9 | REACH | 2025-12-01 | 1 | 1 |
| 232860 | Reach Floor Lamp | CAT9 | REACH | 2026-01-01 | 2 | 2 |
| 232860 | Reach Floor Lamp | CAT9 | REACH | 2026-02-01 | 3 | 2 |
| 232860 | Reach Floor Lamp | CAT9 | REACH | 2026-03-01 | 4 | 4 |
| 232860 | Reach Floor Lamp | CAT9 | REACH | 2026-04-01 | 1 | 1 |
| 232860 | Reach Floor Lamp | CAT9 | REACH | 2026-05-01 | 2 | 2 |
| 233070 | Moreau Floor Lamp | CAT9 | COL50 | 2026-02-01 | 5 | 5 |
| 233070 | Moreau Floor Lamp | CAT9 | COL50 | 2026-03-01 | 1 | 1 |
| 233070 | Moreau Floor Lamp | CAT9 | COL50 | 2026-05-01 | 1 | 1 |
| 234505 | Mobius Arc Floor Lamp | CAT9 | COL14 | 2025-12-01 | 2 | 1 |
| 234505 | Mobius Arc Floor Lamp | CAT9 | COL14 | 2026-01-01 | 2 | 2 |
| 234505 | Mobius Arc Floor Lamp | CAT9 | COL14 | 2026-02-01 | 4 | 4 |
| 234505 | Mobius Arc Floor Lamp | CAT9 | COL14 | 2026-03-01 | 1 | 1 |
| 234505 | Mobius Arc Floor Lamp | CAT9 | COL14 | 2026-05-01 | 1 | 1 |
| 234505 | Mobius Arc Floor Lamp | CAT9 | COL14 | 2026-06-01 | 2 | 2 |
| 234510 | — | — | — | 2026-02-01 | 1 | 1 |
| 234901 | Rook Floor Lamp | CAT9 | ROOK | 2026-02-01 | 1 | 1 |
| 234901 | Rook Floor Lamp | CAT9 | ROOK | 2026-03-01 | 2 | 2 |
| 234901 | Rook Floor Lamp | CAT9 | ROOK | 2026-05-01 | 1 | 1 |
| 234901 | Rook Floor Lamp | CAT9 | ROOK | 2026-06-01 | 1 | 1 |
| 234903 | Rook Twin Floor Lamp | CAT9 | ROOK | 2026-01-01 | 1 | 1 |
| 234903 | Rook Twin Floor Lamp | CAT9 | ROOK | 2026-02-01 | 1 | 1 |
| 234903 | Rook Twin Floor Lamp | CAT9 | ROOK | 2026-03-01 | 1 | 1 |
| 234903 | Rook Twin Floor Lamp | CAT9 | ROOK | 2026-05-01 | 2 | 2 |
| 234903 | Rook Twin Floor Lamp | CAT9 | ROOK | 2026-06-01 | 1 | 1 |
| 237660 | Brindille Floor Lamp | CAT9 | COL24 | 2026-05-01 | 1 | 1 |
| 237670 | Cavaletti Floor Lamp | CAT9 | COL51 | 2025-12-01 | 1 | 1 |
| 237670 | Cavaletti Floor Lamp | CAT9 | COL51 | 2026-01-01 | 2 | 2 |
| 237670 | Cavaletti Floor Lamp | CAT9 | COL51 | 2026-02-01 | 1 | 1 |
| 237670 | Cavaletti Floor Lamp | CAT9 | COL51 | 2026-03-01 | 3 | 2 |
| 237670 | Cavaletti Floor Lamp | CAT9 | COL51 | 2026-04-01 | 1 | 1 |
| 237670 | Cavaletti Floor Lamp | CAT9 | COL51 | 2026-06-01 | 2 | 1 |
| 237681 | Sway Floor Lamp | CAT9 | SWAY | 2025-12-01 | 4 | 4 |
| 237681 | Sway Floor Lamp | CAT9 | SWAY | 2026-01-01 | 6 | 6 |
| 237681 | Sway Floor Lamp | CAT9 | SWAY | 2026-02-01 | 10 | 9 |
| 237681 | Sway Floor Lamp | CAT9 | SWAY | 2026-03-01 | 5 | 1 |
| 237681 | Sway Floor Lamp | CAT9 | SWAY | 2026-04-01 | 1 | 1 |
| 237681 | Sway Floor Lamp | CAT9 | SWAY | 2026-05-01 | 1 | 1 |
| 241100 | Pulse Floor Lamp | CAT9 | PULSE | 2026-02-01 | 1 | 1 |
| 241100 | Pulse Floor Lamp | CAT9 | PULSE | 2026-03-01 | 1 | 1 |
| 241101 | Chrysalis Torchiere | CAT16 | COL86 | 2025-12-01 | 1 | 1 |
| 241101 | Chrysalis Torchiere | CAT16 | COL86 | 2026-01-01 | 3 | 3 |
| 241101 | Chrysalis Torchiere | CAT16 | COL86 | 2026-02-01 | 1 | 1 |
| 241101 | Chrysalis Torchiere | CAT16 | COL86 | 2026-04-01 | 2 | 2 |
| 241102 | Tryst Floor Lamp | CAT9 | TRYST | 2026-01-01 | 4 | 3 |
| 241102 | Tryst Floor Lamp | CAT9 | TRYST | 2026-05-01 | 2 | 2 |
| 241103 | Vertex Floor Lamp | CAT9 | COL47 | 2026-02-01 | 1 | 1 |
| 241103 | Vertex Floor Lamp | CAT9 | COL47 | 2026-04-01 | 1 | 1 |
| 241103 | Vertex Floor Lamp | CAT9 | COL47 | 2026-05-01 | 1 | 1 |
| 241104 | Quill Torchiere | CAT16 | QUILL | 2026-02-01 | 1 | 1 |
| 241104 | Quill Torchiere | CAT16 | QUILL | 2026-03-01 | 1 | 1 |
| 241104 | Quill Torchiere | CAT16 | QUILL | 2026-04-01 | 2 | 2 |
| 241104 | Quill Torchiere | CAT16 | QUILL | 2026-05-01 | 2 | 2 |
| 241105 | Aerial Torchiere | CAT16 | COL55 | 2025-12-01 | 4 | 4 |
| 241105 | Aerial Torchiere | CAT16 | COL55 | 2026-01-01 | 6 | 6 |
| 241105 | Aerial Torchiere | CAT16 | COL55 | 2026-02-01 | 2 | 2 |
| 241105 | Aerial Torchiere | CAT16 | COL55 | 2026-03-01 | 8 | 8 |
| 241105 | Aerial Torchiere | CAT16 | COL55 | 2026-04-01 | 1 | 1 |
| 241105 | Aerial Torchiere | CAT16 | COL55 | 2026-05-01 | 1 | 1 |
| 241108 | Glissade LED Arc Floor Lamp | CAT9 | COL106 | 2026-01-01 | 1 | 1 |
| 241108 | Glissade LED Arc Floor Lamp | CAT9 | COL106 | 2026-02-01 | 1 | 1 |
| 241108 | Glissade LED Arc Floor Lamp | CAT9 | COL106 | 2026-03-01 | 1 | 1 |
| 241108 | Glissade LED Arc Floor Lamp | CAT9 | COL106 | 2026-04-01 | 1 | 1 |
| 241108 | Glissade LED Arc Floor Lamp | CAT9 | COL106 | 2026-05-01 | 2 | 2 |
| 241108 | Glissade LED Arc Floor Lamp | CAT9 | COL106 | 2026-06-01 | 1 | 1 |
| 241109 | Pangea Torchiere | CAT16 | COL77 | 2026-01-01 | 1 | 1 |
| 241109 | Pangea Torchiere | CAT16 | COL77 | 2026-02-01 | 1 | 1 |
| 241109 | Pangea Torchiere | CAT16 | COL77 | 2026-03-01 | 1 | 1 |
| 241109 | Pangea Torchiere | CAT16 | COL77 | 2026-05-01 | 1 | 1 |
| 241109 | Pangea Torchiere | CAT16 | COL77 | 2026-06-01 | 1 | 1 |
| 241200 | Cairn Floor Lamp | CAT9 | CAIRN | 2026-01-01 | 1 | 1 |
| 241200 | Cairn Floor Lamp | CAT9 | CAIRN | 2026-02-01 | 4 | 4 |
| 241200 | Cairn Floor Lamp | CAT9 | CAIRN | 2026-03-01 | 2 | 2 |
| 241200 | Cairn Floor Lamp | CAT9 | CAIRN | 2026-04-01 | 1 | 1 |
| 241201 | Shield Short Floor Lamp | CAT9 | COL3 | 2026-01-01 | 1 | 1 |
| 241201 | Shield Short Floor Lamp | CAT9 | COL3 | 2026-02-01 | 1 | 1 |
| 241201 | Shield Short Floor Lamp | CAT9 | COL3 | 2026-03-01 | 1 | 1 |
| 241201 | Shield Short Floor Lamp | CAT9 | COL3 | 2026-04-01 | 2 | 2 |
| 241201 | Shield Short Floor Lamp | CAT9 | COL3 | 2026-05-01 | 1 | 1 |
| 241201 | Shield Short Floor Lamp | CAT9 | COL3 | 2026-06-01 | 1 | 1 |
| 241202 | Shield Medium Floor Lamp | CAT9 | COL3 | 2026-01-01 | 7 | 5 |
| 241202 | Shield Medium Floor Lamp | CAT9 | COL3 | 2026-02-01 | 5 | 5 |
| 241202 | Shield Medium Floor Lamp | CAT9 | COL3 | 2026-05-01 | 2 | 1 |
| 241203 | Shield Tall Floor Lamp | CAT9 | COL3 | 2026-01-01 | 5 | 4 |
| 241203 | Shield Tall Floor Lamp | CAT9 | COL3 | 2026-02-01 | 4 | 4 |
| 241203 | Shield Tall Floor Lamp | CAT9 | COL3 | 2026-03-01 | 5 | 5 |
| 241203 | Shield Tall Floor Lamp | CAT9 | COL3 | 2026-04-01 | 2 | 2 |
| 241203 | Shield Tall Floor Lamp | CAT9 | COL3 | 2026-05-01 | 2 | 2 |
| 241203 | Shield Tall Floor Lamp | CAT9 | COL3 | 2026-06-01 | 3 | 3 |
| 241204 | Lattice Torchiere | CAT16 | COL15 | 2026-01-01 | 5 | 5 |
| 241204 | Lattice Torchiere | CAT16 | COL15 | 2026-02-01 | 6 | 4 |
| 241204 | Lattice Torchiere | CAT16 | COL15 | 2026-03-01 | 1 | 1 |
| 241204 | Lattice Torchiere | CAT16 | COL15 | 2026-04-01 | 2 | 2 |
| 241204 | Lattice Torchiere | CAT16 | COL15 | 2026-05-01 | 1 | 1 |
| 241205 | Fracture Lamp | CAT9 | COL33 | 2026-01-01 | 1 | 1 |
| 241205 | Fracture Lamp | CAT9 | COL33 | 2026-02-01 | 5 | 5 |
| 241205 | Fracture Lamp | CAT9 | COL33 | 2026-03-01 | 1 | 1 |
| 241205 | Fracture Lamp | CAT9 | COL33 | 2026-04-01 | 2 | 2 |
| 241205 | Fracture Lamp | CAT9 | COL33 | 2026-05-01 | 1 | 1 |
| 241952 | Metamorphic Contemporary Floor Lamp | CAT9 | COL117 | 2025-12-01 | 2 | 2 |
| 241952 | Metamorphic Contemporary Floor Lamp | CAT9 | COL117 | 2026-01-01 | 2 | 2 |
| 241952 | Metamorphic Contemporary Floor Lamp | CAT9 | COL117 | 2026-02-01 | 2 | 2 |
| 241952 | Metamorphic Contemporary Floor Lamp | CAT9 | COL117 | 2026-03-01 | 2 | 2 |
| 241952 | Metamorphic Contemporary Floor Lamp | CAT9 | COL117 | 2026-04-01 | 1 | 1 |
| 241952 | Metamorphic Contemporary Floor Lamp | CAT9 | COL117 | 2026-05-01 | 2 | 2 |
| 242050 | — | — | — | 2025-12-01 | 1 | 1 |
| 242051 | — | — | — | 2026-02-01 | 1 | 1 |
| 242051 | — | — | — | 2026-05-01 | 1 | 1 |
| 242161 | Twist Basket Floor Lamp | CAT9 | COL38 | 2025-12-01 | 2 | 1 |
| 242161 | Twist Basket Floor Lamp | CAT9 | COL38 | 2026-01-01 | 3 | 3 |
| 242161 | Twist Basket Floor Lamp | CAT9 | COL38 | 2026-02-01 | 3 | 2 |
| 242161 | Twist Basket Floor Lamp | CAT9 | COL38 | 2026-03-01 | 5 | 5 |
| 242161 | Twist Basket Floor Lamp | CAT9 | COL38 | 2026-05-01 | 3 | 3 |
| 242210 | Pluto Floor Lamp | CAT9 | PLUTO | 2025-12-01 | 2 | 2 |
| 242210 | Pluto Floor Lamp | CAT9 | PLUTO | 2026-01-01 | 1 | 1 |
| 242210 | Pluto Floor Lamp | CAT9 | PLUTO | 2026-02-01 | 1 | 1 |
| 242210 | Pluto Floor Lamp | CAT9 | PLUTO | 2026-03-01 | 1 | 1 |
| 242210 | Pluto Floor Lamp | CAT9 | PLUTO | 2026-04-01 | 2 | 1 |
| 242210 | Pluto Floor Lamp | CAT9 | PLUTO | 2026-05-01 | 1 | 1 |
| 242215 | Henry Floor Lamp | CAT9 | HENRY | 2025-12-01 | 4 | 4 |
| 242215 | Henry Floor Lamp | CAT9 | HENRY | 2026-01-01 | 7 | 6 |
| 242215 | Henry Floor Lamp | CAT9 | HENRY | 2026-02-01 | 2 | 3 |
| 242215 | Henry Floor Lamp | CAT9 | HENRY | 2026-03-01 | 2 | 2 |
| 242215 | Henry Floor Lamp | CAT9 | HENRY | 2026-04-01 | 1 | 1 |
| 242215 | Henry Floor Lamp | CAT9 | HENRY | 2026-05-01 | 2 | 2 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2025-12-01 | 1 | 1 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2026-01-01 | 2 | 2 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2026-02-01 | 1 | 1 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2026-03-01 | 3 | 3 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2026-04-01 | 4 | 3 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2026-05-01 | 4 | 4 |
| 246761 | Forged Leaves and Vase Floor Lamp | CAT9 | LEAF | 2026-06-01 | 1 | 1 |
| 248416 | Metra Twin Tall Floor Lamp | CAT9 | METRA | 2025-12-01 | 1 | 1 |
| 248416 | Metra Twin Tall Floor Lamp | CAT9 | METRA | 2026-01-01 | 1 | 1 |
| 248416 | Metra Twin Tall Floor Lamp | CAT9 | METRA | 2026-02-01 | 3 | 3 |
| 248416 | Metra Twin Tall Floor Lamp | CAT9 | METRA | 2026-03-01 | 2 | 2 |
| 248416 | Metra Twin Tall Floor Lamp | CAT9 | METRA | 2026-05-01 | 2 | 2 |
| 248421 | Metra Double Floor Lamp | CAT9 | METRA | 2026-01-01 | 5 | 5 |
| 248421 | Metra Double Floor Lamp | CAT9 | METRA | 2026-02-01 | 2 | 2 |
| 248421 | Metra Double Floor Lamp | CAT9 | METRA | 2026-04-01 | 1 | 1 |
| 248421 | Metra Double Floor Lamp | CAT9 | METRA | 2026-05-01 | 1 | 1 |
| 248421 | Metra Double Floor Lamp | CAT9 | METRA | 2026-06-01 | 3 | 3 |
| 249642 | Taper Torchiere | CAT16 | TAPER | 2026-01-01 | 6 | 4 |
| 249642 | Taper Torchiere | CAT16 | TAPER | 2026-02-01 | 10 | 7 |
| 249642 | Taper Torchiere | CAT16 | TAPER | 2026-03-01 | 7 | 7 |
| 249642 | Taper Torchiere | CAT16 | TAPER | 2026-04-01 | 4 | 4 |
| 249642 | Taper Torchiere | CAT16 | TAPER | 2026-05-01 | 2 | 2 |
| 249642 | Taper Torchiere | CAT16 | TAPER | 2026-06-01 | 2 | 2 |
| 251092 | — | — | — | 2026-02-01 | 2 | 1 |
| 251092 | — | — | — | 2026-03-01 | 8 | 2 |
| 251099 | — | — | — | 2026-02-01 | 1 | 1 |
| 251099 | — | — | — | 2026-04-01 | 1 | 1 |
| 251195 | — | — | — | 2026-03-01 | 1 | 1 |
| 251295 | — | — | — | 2026-01-01 | 2 | 1 |
| 251295 | — | — | — | 2026-03-01 | 4 | 1 |
| 251348 | — | — | — | 2026-01-01 | 1 | 1 |
| 251348 | — | — | — | 2026-05-01 | 2 | 2 |
| 251494 | — | — | — | 2026-01-01 | 4 | 1 |
| 251494 | — | — | — | 2026-02-01 | 2 | 2 |
| 251494 | — | — | — | 2026-03-01 | 3 | 3 |
| 251494 | — | — | — | 2026-04-01 | 1 | 1 |
| 251494 | — | — | — | 2026-05-01 | 3 | 1 |
| 251505 | — | — | — | 2026-03-01 | 1 | 1 |
| 251505 | — | — | — | 2026-04-01 | 1 | 1 |
| 251511 | — | — | — | 2026-03-01 | 1 | 1 |
| 251555 | — | — | — | 2026-01-01 | 1 | 1 |
| 251555 | — | — | — | 2026-02-01 | 1 | 1 |
| 251555 | — | — | — | 2026-03-01 | 2 | 1 |
| 251555 | — | — | — | 2026-06-01 | 2 | 2 |
| 251590 | — | — | — | 2025-12-01 | 1 | 1 |
| 251590 | — | — | — | 2026-01-01 | 1 | 1 |
| 251590 | — | — | — | 2026-02-01 | 1 | 1 |
| 251590 | — | — | — | 2026-03-01 | 1 | 1 |
| 251590 | — | — | — | 2026-05-01 | 5 | 3 |
| 251590 | — | — | — | 2026-06-01 | 1 | 1 |
| 251594 | — | — | — | 2026-02-01 | 2 | 1 |
| 251594 | — | — | — | 2026-03-01 | 1 | 1 |
| 251605 | — | — | — | 2026-01-01 | 1 | 1 |
| 251605 | — | — | — | 2026-02-01 | 1 | 1 |
| 251605 | — | — | — | 2026-05-01 | 1 | 1 |
| 251605 | — | — | — | 2026-06-01 | 1 | 1 |
| 251606 | — | — | — | 2026-03-01 | 1 | 1 |
| 251606 | — | — | — | 2026-05-01 | 2 | 2 |
| 251606 | — | — | — | 2026-06-01 | 2 | 1 |
| 251655 | — | — | — | 2026-01-01 | 1 | 1 |
| 251655 | — | — | — | 2026-03-01 | 1 | 1 |
| 251692 | — | — | — | 2025-12-01 | 2 | 1 |
| 251695 | — | — | — | 2025-12-01 | 1 | 1 |
| 251695 | — | — | — | 2026-01-01 | 6 | 5 |
| 251695 | — | — | — | 2026-02-01 | 2 | 2 |
| 251695 | — | — | — | 2026-03-01 | 2 | 2 |
| 251695 | — | — | — | 2026-04-01 | 2 | 2 |
| 251695 | — | — | — | 2026-05-01 | 2 | 2 |
| 251695 | — | — | — | 2026-06-01 | 2 | 2 |
| 251755 | — | — | — | 2026-01-01 | 2 | 2 |
| 251755 | — | — | — | 2026-02-01 | 3 | 3 |
| 251755 | — | — | — | 2026-05-01 | 1 | 1 |
| 251755 | — | — | — | 2026-06-01 | 2 | 2 |
| 251794 | — | — | — | 2026-06-01 | 2 | 2 |
| 251795 | — | — | — | 2026-01-01 | 2 | 1 |
| 251810 | — | — | — | 2026-01-01 | 1 | 1 |
| 251810 | — | — | — | 2026-02-01 | 1 | 1 |
| 251810 | — | — | — | 2026-05-01 | 1 | 1 |
| 251815 | — | — | — | 2026-01-01 | 2 | 1 |
| 251815 | — | — | — | 2026-03-01 | 1 | 1 |
| 251894 | — | — | — | 2025-12-01 | 1 | 1 |
| 251894 | — | — | — | 2026-02-01 | 1 | 1 |
| 251899 | — | — | — | 2025-12-01 | 4 | 1 |
| 251899 | — | — | — | 2026-02-01 | 2 | 2 |
| 251899 | — | — | — | 2026-04-01 | 2 | 2 |
| 251899 | — | — | — | 2026-05-01 | 2 | 2 |
| 251899 | — | — | — | 2026-06-01 | 1 | 1 |
| 251914 | — | — | — | 2026-02-01 | 2 | 2 |
| 251995 | — | — | — | 2026-01-01 | 1 | 1 |
| 251995 | — | — | — | 2026-02-01 | 1 | 1 |
| 251995 | — | — | — | 2026-04-01 | 1 | 1 |
| 251995 | — | — | — | 2026-05-01 | 1 | 1 |
| 252010 | — | — | — | 2026-01-01 | 2 | 2 |
| 252010 | — | — | — | 2026-02-01 | 1 | 1 |
| 252010 | — | — | — | 2026-03-01 | 1 | 1 |
| 252010 | — | — | — | 2026-04-01 | 2 | 2 |
| 252010 | — | — | — | 2026-05-01 | 2 | 2 |
| 252011 | — | — | — | 2025-12-01 | 1 | 1 |
| 252011 | — | — | — | 2026-02-01 | 2 | 1 |
| 252011 | — | — | — | 2026-04-01 | 1 | 1 |
| 252012 | — | — | — | 2025-12-01 | 1 | 1 |
| 252012 | — | — | — | 2026-02-01 | 1 | 1 |
| 252012 | — | — | — | 2026-05-01 | 1 | 1 |
| 252012 | — | — | — | 2026-06-01 | 1 | 1 |
| 252023R | — | — | — | 2026-04-01 | 1 | 1 |
| 252155 | — | — | — | 2025-12-01 | 1 | 1 |
| 252155 | — | — | — | 2026-04-01 | 2 | 2 |
| 252155 | — | — | — | 2026-05-01 | 1 | 1 |
| 252201 | — | — | — | 2025-12-01 | 1 | 1 |
| 252201 | — | — | — | 2026-03-01 | 1 | 1 |
| 252201 | — | — | — | 2026-06-01 | 1 | 1 |
| 252202 | — | — | — | 2026-03-01 | 1 | 1 |
| 252290 | — | — | — | 2025-12-01 | 2 | 2 |
| 252290 | — | — | — | 2026-01-01 | 4 | 4 |
| 252290 | — | — | — | 2026-04-01 | 2 | 2 |
| 252290 | — | — | — | 2026-05-01 | 2 | 2 |
| 252290 | — | — | — | 2026-06-01 | 1 | 1 |
| 252302 | — | — | — | 2025-12-01 | 1 | 1 |
| 252302 | — | — | — | 2026-01-01 | 1 | 1 |
| 252302 | — | — | — | 2026-06-01 | 1 | 1 |
| 252312 | — | — | — | 2026-06-01 | 1 | 1 |
| 252401 | — | — | — | 2025-12-01 | 1 | 1 |
| 252401 | — | — | — | 2026-03-01 | 1 | 1 |
| 252811 | — | — | — | 2026-01-01 | 1 | 1 |
| 252811 | — | — | — | 2026-06-01 | 1 | 1 |
| 252812 | — | — | — | 2025-12-01 | 1 | 1 |
| 252812 | — | — | — | 2026-01-01 | 1 | 1 |
| 252812 | — | — | — | 2026-02-01 | 1 | 1 |
| 252812 | — | — | — | 2026-04-01 | 2 | 2 |
| 252899 | — | — | — | 2026-01-01 | 4 | 4 |
| 252899 | — | — | — | 2026-02-01 | 1 | 1 |
| 252899 | — | — | — | 2026-05-01 | 1 | 1 |
| 252899 | — | — | — | 2026-06-01 | 1 | 1 |
| 253699 | — | — | — | 2026-02-01 | 1 | 1 |
| 254207 | — | — | — | 2026-05-01 | 1 | 1 |
| 254279 | — | — | — | 2026-03-01 | 1 | 1 |
| 254298 | — | — | — | 2025-12-01 | 1 | 1 |
| 254298 | — | — | — | 2026-01-01 | 1 | 1 |
| 254298 | — | — | — | 2026-02-01 | 3 | 3 |
| 254298 | — | — | — | 2026-03-01 | 3 | 3 |
| 254298 | — | — | — | 2026-04-01 | 2 | 2 |
| 254298 | — | — | — | 2026-05-01 | 3 | 3 |
| 254299 | — | — | — | 2026-02-01 | 1 | 1 |
| 254299 | — | — | — | 2026-04-01 | 1 | 1 |
| 254299 | — | — | — | 2026-05-01 | 1 | 1 |
| 254602 | — | — | — | 2026-02-01 | 1 | 1 |
| 254602 | — | — | — | 2026-04-01 | 3 | 3 |
| 254602 | — | — | — | 2026-05-01 | 1 | 1 |
| 254602 | — | — | — | 2026-06-01 | 1 | 1 |
| 254608R | — | — | — | 2026-03-01 | 1 | 1 |
| 262072 | — | — | — | 2026-01-01 | 1 | 1 |
| 262072 | — | — | — | 2026-04-01 | 1 | 1 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2025-12-01 | 1 | 1 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2026-01-01 | 9 | 6 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2026-02-01 | 4 | 3 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2026-03-01 | 3 | 2 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2026-04-01 | 4 | 3 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2026-05-01 | 1 | 1 |
| 265001 | Twist Basket Table Lamp | CAT5 | COL38 | 2026-06-01 | 2 | 3 |
| 266760 | Forged Leaves and Vase Table Lamp | CAT5 | LEAF | 2025-12-01 | 3 | 3 |
| 266760 | Forged Leaves and Vase Table Lamp | CAT5 | LEAF | 2026-01-01 | 2 | 2 |
| 266760 | Forged Leaves and Vase Table Lamp | CAT5 | LEAF | 2026-02-01 | 3 | 2 |
| 266760 | Forged Leaves and Vase Table Lamp | CAT5 | LEAF | 2026-03-01 | 2 | 2 |
| 266760 | Forged Leaves and Vase Table Lamp | CAT5 | LEAF | 2026-05-01 | 1 | 1 |
| 266760 | Forged Leaves and Vase Table Lamp | CAT5 | LEAF | 2026-06-01 | 2 | 1 |
| 266792 | Forged Leaves Table Lamp | CAT5 | LEAF | 2026-01-01 | 1 | 1 |
| 266792 | Forged Leaves Table Lamp | CAT5 | LEAF | 2026-02-01 | 3 | 3 |
| 266792 | Forged Leaves Table Lamp | CAT5 | LEAF | 2026-03-01 | 2 | 2 |
| 266792 | Forged Leaves Table Lamp | CAT5 | LEAF | 2026-04-01 | 4 | 3 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2025-12-01 | 3 | 2 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2026-01-01 | 2 | 2 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2026-02-01 | 3 | 2 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2026-03-01 | 5 | 4 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2026-04-01 | 4 | 2 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2026-05-01 | 1 | 1 |
| 268421 | Metra Double Table Lamp | CAT5 | METRA | 2026-06-01 | 1 | 1 |
| 268422 | — | — | — | 2026-03-01 | 2 | 1 |
| 269411 | — | — | — | 2026-03-01 | 1 | 1 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2025-12-01 | 2 | 1 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2026-01-01 | 7 | 4 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2026-02-01 | 2 | 2 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2026-03-01 | 3 | 2 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2026-04-01 | 3 | 2 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2026-05-01 | 2 | 1 |
| 271200 | Cairn Table Lamp | CAT5 | CAIRN | 2026-06-01 | 1 | 1 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2025-12-01 | 1 | 1 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2026-01-01 | 3 | 3 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2026-02-01 | 6 | 5 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2026-03-01 | 2 | 2 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2026-04-01 | 2 | 2 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2026-05-01 | 0 | 1 |
| 271201 | Horizon Console Lamp | CAT5 | COL37 | 2026-06-01 | 1 | 1 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2025-12-01 | 6 | 4 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2026-01-01 | 13 | 8 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2026-02-01 | 9 | 7 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2026-03-01 | 4 | 4 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2026-04-01 | 4 | 4 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2026-05-01 | 2 | 3 |
| 271202 | Horizon Table Lamp | CAT5 | COL37 | 2026-06-01 | 2 | 1 |
| 272102 | Pression Table Lamp | CAT5 | COL53 | 2026-04-01 | 2 | 1 |
| 272102 | Pression Table Lamp | CAT5 | COL53 | 2026-06-01 | 2 | 1 |
| 272103 | Pangea Dome Table Lamp | CAT5 | COL77 | 2026-02-01 | 1 | 1 |
| 272103 | Pangea Dome Table Lamp | CAT5 | COL77 | 2026-06-01 | 1 | 1 |
| 272104 | Dahlia Cylindrical Table Lamp | CAT5 | COL13 | 2026-01-01 | 2 | 1 |
| 272105 | Dahlia Table Lamp | CAT5 | COL13 | 2026-01-01 | 1 | 1 |
| 272105 | Dahlia Table Lamp | CAT5 | COL13 | 2026-02-01 | 1 | 1 |
| 272106 | Blossom Mini Table Lamp | CAT5 | COL109 | 2026-01-01 | 2 | 2 |
| 272106 | Blossom Mini Table Lamp | CAT5 | COL109 | 2026-02-01 | 2 | 2 |
| 272106 | Blossom Mini Table Lamp | CAT5 | COL109 | 2026-03-01 | 7 | 2 |
| 272107 | Pangea Mini Table Lamp | CAT5 | COL77 | 2026-03-01 | 1 | 1 |
| 272110 | Yoki Table Lamp | CAT5 | YOKI | 2026-01-01 | 2 | 2 |
| 272110 | Yoki Table Lamp | CAT5 | YOKI | 2026-03-01 | 2 | 2 |
| 272110 | Yoki Table Lamp | CAT5 | YOKI | 2026-04-01 | 1 | 1 |
| 272110 | Yoki Table Lamp | CAT5 | YOKI | 2026-05-01 | 1 | 1 |
| 272110 | Yoki Table Lamp | CAT5 | YOKI | 2026-06-01 | 3 | 1 |
| 272111 | Crest Table Lamp | CAT5 | CREST | 2026-01-01 | 3 | 2 |
| 272111 | Crest Table Lamp | CAT5 | CREST | 2026-02-01 | 2 | 2 |
| 272111 | Crest Table Lamp | CAT5 | CREST | 2026-04-01 | 2 | 1 |
| 272111 | Crest Table Lamp | CAT5 | CREST | 2026-05-01 | 4 | 3 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2025-12-01 | 4 | 2 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2026-01-01 | 4 | 3 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2026-02-01 | 3 | 2 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2026-03-01 | 3 | 2 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2026-04-01 | 0 | 1 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2026-05-01 | 3 | 2 |
| 272112 | Rivulet Table Lamp | CAT5 | COL59 | 2026-06-01 | 1 | 1 |
| 272115 | Cambrian Table Lamp | CAT5 | COL75 | 2026-01-01 | 2 | 1 |
| 272115 | Cambrian Table Lamp | CAT5 | COL75 | 2026-02-01 | 1 | 1 |
| 272115 | Cambrian Table Lamp | CAT5 | COL75 | 2026-03-01 | 1 | 1 |
| 272116 | — | — | — | 2025-12-01 | 1 | 1 |
| 272117 | Zen Table Lamp | CAT5 | ZEN | 2026-01-01 | 1 | 1 |
| 272117 | Zen Table Lamp | CAT5 | ZEN | 2026-03-01 | 2 | 2 |
| 272117 | Zen Table Lamp | CAT5 | ZEN | 2026-04-01 | 1 | 1 |
| 272117 | Zen Table Lamp | CAT5 | ZEN | 2026-05-01 | 1 | 1 |
| 272120 | Pangea Tall Table Lamp | CAT5 | COL77 | 2026-02-01 | 1 | 1 |
| 272121 | Cypress Table Lamp | CAT5 | COL103 | 2026-01-01 | 3 | 2 |
| 272121 | Cypress Table Lamp | CAT5 | COL103 | 2026-04-01 | 2 | 1 |
| 272121 | Cypress Table Lamp | CAT5 | COL103 | 2026-06-01 | 3 | 3 |
| 272122 | Volterra Table Lamp | CAT5 | COL102 | 2026-01-01 | 2 | 1 |
| 272122 | Volterra Table Lamp | CAT5 | COL102 | 2026-04-01 | 2 | 1 |
| 272122 | Volterra Table Lamp | CAT5 | COL102 | 2026-06-01 | 4 | 2 |
| 272123 | Glissade LED Table Lamp | CAT5 | COL106 | 2026-03-01 | 1 | 1 |
| 272123 | Glissade LED Table Lamp | CAT5 | COL106 | 2026-05-01 | 3 | 2 |
| 272125 | Spire Table Lamp | CAT5 | SPIRE | 2025-12-01 | 4 | 2 |
| 272125 | Spire Table Lamp | CAT5 | SPIRE | 2026-02-01 | 1 | 1 |
| 272125 | Spire Table Lamp | CAT5 | SPIRE | 2026-03-01 | 3 | 2 |
| 272125 | Spire Table Lamp | CAT5 | SPIRE | 2026-04-01 | 2 | 1 |
| 272127 | Union Table Lamp | CAT5 | UNION | 2025-12-01 | 6 | 3 |
| 272127 | Union Table Lamp | CAT5 | UNION | 2026-01-01 | 3 | 2 |
| 272127 | Union Table Lamp | CAT5 | UNION | 2026-03-01 | 2 | 2 |
| 272127 | Union Table Lamp | CAT5 | UNION | 2026-06-01 | 1 | 1 |
| 272665 | Stasis Table Lamp | CAT5 | COL115 | 2026-01-01 | 1 | 1 |
| 272665 | Stasis Table Lamp | CAT5 | COL115 | 2026-02-01 | 3 | 3 |
| 272665 | Stasis Table Lamp | CAT5 | COL115 | 2026-03-01 | 1 | 1 |
| 272665 | Stasis Table Lamp | CAT5 | COL115 | 2026-04-01 | 1 | 1 |
| 272665 | Stasis Table Lamp | CAT5 | COL115 | 2026-05-01 | 2 | 2 |
| 272665 | Stasis Table Lamp | CAT5 | COL115 | 2026-06-01 | 3 | 2 |
| 272666 | Stasis Table Lamp | CAT5 | COL115 | 2025-12-01 | 1 | 1 |
| 272666 | Stasis Table Lamp | CAT5 | COL115 | 2026-02-01 | 1 | 1 |
| 272666 | Stasis Table Lamp | CAT5 | COL115 | 2026-03-01 | 4 | 3 |
| 272666 | Stasis Table Lamp | CAT5 | COL115 | 2026-04-01 | 2 | 1 |
| 272666 | Stasis Table Lamp | CAT5 | COL115 | 2026-05-01 | 4 | 3 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2025-12-01 | 1 | 1 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2026-01-01 | 4 | 5 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2026-02-01 | 2 | 2 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2026-03-01 | 8 | 7 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2026-04-01 | 7 | 6 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2026-05-01 | 8 | 5 |
| 272674 | Fullered Impressions Table Lamp | CAT5 | COL29 | 2026-06-01 | 1 | 1 |
| 272678 | Fullered Impressions Large Table Lamp | CAT5 | COL29 | 2025-12-01 | 2 | 1 |
| 272678 | Fullered Impressions Large Table Lamp | CAT5 | COL29 | 2026-01-01 | 5 | 3 |
| 272678 | Fullered Impressions Large Table Lamp | CAT5 | COL29 | 2026-02-01 | 4 | 4 |
| 272678 | Fullered Impressions Large Table Lamp | CAT5 | COL29 | 2026-03-01 | 2 | 2 |
| 272678 | Fullered Impressions Large Table Lamp | CAT5 | COL29 | 2026-04-01 | 5 | 4 |
| 272678 | Fullered Impressions Large Table Lamp | CAT5 | COL29 | 2026-05-01 | 4 | 3 |
| 272686 | Almost Infinity Table Lamp | CAT5 | COL116 | 2026-01-01 | 5 | 5 |
| 272686 | Almost Infinity Table Lamp | CAT5 | COL116 | 2026-02-01 | 3 | 3 |
| 272686 | Almost Infinity Table Lamp | CAT5 | COL116 | 2026-03-01 | 3 | 2 |
| 272686 | Almost Infinity Table Lamp | CAT5 | COL116 | 2026-04-01 | 2 | 1 |
| 272686 | Almost Infinity Table Lamp | CAT5 | COL116 | 2026-05-01 | 1 | 1 |
| 272686 | Almost Infinity Table Lamp | CAT5 | COL116 | 2026-06-01 | 1 | 1 |
| 272687 | Almost Infinity Tall Table Lamp | CAT5 | COL116 | 2026-01-01 | 4 | 3 |
| 272687 | Almost Infinity Tall Table Lamp | CAT5 | COL116 | 2026-02-01 | 5 | 4 |
| 272687 | Almost Infinity Tall Table Lamp | CAT5 | COL116 | 2026-03-01 | 5 | 3 |
| 272687 | Almost Infinity Tall Table Lamp | CAT5 | COL116 | 2026-05-01 | 2 | 1 |
| 272800 | Antasia Table Lamp | CAT5 | COL18 | 2026-01-01 | 3 | 2 |
| 272800 | Antasia Table Lamp | CAT5 | COL18 | 2026-02-01 | 4 | 4 |
| 272800 | Antasia Table Lamp | CAT5 | COL18 | 2026-03-01 | 4 | 3 |
| 272800 | Antasia Table Lamp | CAT5 | COL18 | 2026-04-01 | 6 | 3 |
| 272800 | Antasia Table Lamp | CAT5 | COL18 | 2026-05-01 | 4 | 3 |
| 272800 | Antasia Table Lamp | CAT5 | COL18 | 2026-06-01 | 3 | 3 |
| 272815 | Antasia Table Lamp | CAT5 | COL18 | 2025-12-01 | 2 | 1 |
| 272815 | Antasia Table Lamp | CAT5 | COL18 | 2026-02-01 | 2 | 2 |
| 272815 | Antasia Table Lamp | CAT5 | COL18 | 2026-06-01 | 1 | 1 |
| 272840 | Henry Table Lamp | CAT5 | HENRY | 2025-12-01 | 1 | 1 |
| 272840 | Henry Table Lamp | CAT5 | HENRY | 2026-01-01 | 3 | 2 |
| 272840 | Henry Table Lamp | CAT5 | HENRY | 2026-03-01 | 2 | 2 |
| 272840 | Henry Table Lamp | CAT5 | HENRY | 2026-04-01 | 3 | 2 |
| 272840 | Henry Table Lamp | CAT5 | HENRY | 2026-05-01 | 2 | 1 |
| 272850 | Facet Table Lamp | CAT5 | FACET | 2026-02-01 | 1 | 1 |
| 272850 | Facet Table Lamp | CAT5 | FACET | 2026-03-01 | 2 | 1 |
| 272860 | Reach Table Lamp | CAT5 | REACH | 2025-12-01 | 1 | 1 |
| 272860 | Reach Table Lamp | CAT5 | REACH | 2026-01-01 | 2 | 1 |
| 272860 | Reach Table Lamp | CAT5 | REACH | 2026-02-01 | 3 | 3 |
| 272860 | Reach Table Lamp | CAT5 | REACH | 2026-03-01 | 1 | 1 |
| 272860 | Reach Table Lamp | CAT5 | REACH | 2026-04-01 | 2 | 1 |
| 272860 | Reach Table Lamp | CAT5 | REACH | 2026-05-01 | 2 | 1 |
| 272880 | Encounter LED Table Lamp | CAT5 | COL118 | 2026-02-01 | 3 | 3 |
| 272880 | Encounter LED Table Lamp | CAT5 | COL118 | 2026-03-01 | 1 | 1 |
| 272880 | Encounter LED Table Lamp | CAT5 | COL118 | 2026-04-01 | 1 | 1 |
| 272880 | Encounter LED Table Lamp | CAT5 | COL118 | 2026-05-01 | 3 | 2 |
| 272880 | Encounter LED Table Lamp | CAT5 | COL118 | 2026-06-01 | 1 | 1 |
| 272920 | Folio Table Lamp | CAT5 | FOLIO | 2025-12-01 | 1 | 1 |
| 272920 | Folio Table Lamp | CAT5 | FOLIO | 2026-01-01 | 1 | 1 |
| 272920 | Folio Table Lamp | CAT5 | FOLIO | 2026-02-01 | 1 | 1 |
| 272920 | Folio Table Lamp | CAT5 | FOLIO | 2026-03-01 | 1 | 1 |
| 272920 | Folio Table Lamp | CAT5 | FOLIO | 2026-04-01 | 2 | 2 |
| 273030 | Gallery Spiral Table Lamp | CAT5 | COL114 | 2025-12-01 | 2 | 2 |
| 273030 | Gallery Spiral Table Lamp | CAT5 | COL114 | 2026-01-01 | 2 | 2 |
| 273030 | Gallery Spiral Table Lamp | CAT5 | COL114 | 2026-02-01 | 2 | 2 |
| 273030 | Gallery Spiral Table Lamp | CAT5 | COL114 | 2026-03-01 | 2 | 1 |
| 273030 | Gallery Spiral Table Lamp | CAT5 | COL114 | 2026-05-01 | 3 | 3 |
| 273030 | Gallery Spiral Table Lamp | CAT5 | COL114 | 2026-06-01 | 1 | 1 |
| 273050 | Gallery Twofold Table Lamp | CAT5 | COL114 | 2025-12-01 | 1 | 1 |
| 273050 | Gallery Twofold Table Lamp | CAT5 | COL114 | 2026-01-01 | 1 | 1 |
| 273050 | Gallery Twofold Table Lamp | CAT5 | COL114 | 2026-03-01 | 3 | 3 |
| 273050 | Gallery Twofold Table Lamp | CAT5 | COL114 | 2026-05-01 | 2 | 1 |
| 273077 | Moreau Tall Table Lamp | CAT5 | COL50 | 2026-01-01 | 1 | 1 |
| 273077 | Moreau Tall Table Lamp | CAT5 | COL50 | 2026-02-01 | 3 | 2 |
| 273077 | Moreau Tall Table Lamp | CAT5 | COL50 | 2026-03-01 | 1 | 1 |
| 273077 | Moreau Tall Table Lamp | CAT5 | COL50 | 2026-05-01 | 2 | 2 |
| 273085 | Lino Table Lamp | CAT5 | LINO | 2026-01-01 | 2 | 2 |
| 273085 | Lino Table Lamp | CAT5 | LINO | 2026-02-01 | 1 | 1 |
| 273085 | Lino Table Lamp | CAT5 | LINO | 2026-03-01 | 2 | 1 |
| 273085 | Lino Table Lamp | CAT5 | LINO | 2026-04-01 | 2 | 1 |
| 273085 | Lino Table Lamp | CAT5 | LINO | 2026-05-01 | 6 | 4 |
| 274120 | Pluto Table Lamp | CAT5 | PLUTO | 2025-12-01 | 1 | 1 |
| 274120 | Pluto Table Lamp | CAT5 | PLUTO | 2026-01-01 | 3 | 3 |
| 274120 | Pluto Table Lamp | CAT5 | PLUTO | 2026-02-01 | 2 | 2 |
| 274120 | Pluto Table Lamp | CAT5 | PLUTO | 2026-03-01 | 1 | 1 |
| 274120 | Pluto Table Lamp | CAT5 | PLUTO | 2026-05-01 | 6 | 4 |
| 277660 | Brindille Table Lamp | CAT5 | COL24 | 2026-01-01 | 2 | 2 |
| 277660 | Brindille Table Lamp | CAT5 | COL24 | 2026-02-01 | 6 | 6 |
| 277660 | Brindille Table Lamp | CAT5 | COL24 | 2026-03-01 | 1 | 1 |
| 277660 | Brindille Table Lamp | CAT5 | COL24 | 2026-05-01 | 2 | 2 |
| 277670 | Cavaletti Table Lamp | CAT5 | COL51 | 2026-01-01 | 1 | 1 |
| 277670 | Cavaletti Table Lamp | CAT5 | COL51 | 2026-02-01 | 1 | 1 |
| 277670 | Cavaletti Table Lamp | CAT5 | COL51 | 2026-03-01 | 1 | 1 |
| 277670 | Cavaletti Table Lamp | CAT5 | COL51 | 2026-05-01 | 2 | 2 |
| 277670 | Cavaletti Table Lamp | CAT5 | COL51 | 2026-06-01 | 2 | 2 |
| 277810 | Erlenmeyer Table Lamp | CAT5 | COL25 | 2026-02-01 | 1 | 1 |
| 289470 | Gatsby 5-Light Floor to Ceiling Plug-In LED Lamp | CAT1 | COL35 | 2026-01-01 | 1 | 1 |
| 289470 | Gatsby 5-Light Floor to Ceiling Plug-In LED Lamp | CAT1 | COL35 | 2026-05-01 | 1 | 1 |
| 289520 | Abacus 5-Light Floor to Ceiling Plug-In LED Lamp | CAT1 | COL60 | 2025-12-01 | 1 | 1 |
| 289520 | Abacus 5-Light Floor to Ceiling Plug-In LED Lamp | CAT1 | COL60 | 2026-02-01 | 2 | 1 |
| 289520 | Abacus 5-Light Floor to Ceiling Plug-In LED Lamp | CAT1 | COL60 | 2026-06-01 | 3 | 1 |
| 290198 | — | — | — | 2025-12-01 | 13 | 1 |
| 290198 | — | — | — | 2026-02-01 | 2 | 1 |
| 290202 | — | — | — | 2026-04-01 | 1 | 1 |
| 290209 | — | — | — | 2025-12-01 | 1 | 1 |
| 290213 | — | — | — | 2026-01-01 | 5 | 4 |
| 290213 | — | — | — | 2026-02-01 | 1 | 2 |
| 290213 | — | — | — | 2026-03-01 | 1 | 1 |
| 290213 | — | — | — | 2026-04-01 | 1 | 1 |
| 290213 | — | — | — | 2026-05-01 | 3 | 3 |
| 290213 | — | — | — | 2026-06-01 | 4 | 3 |
| 290236 | — | — | — | 2026-01-01 | 2 | 2 |
| 290236 | — | — | — | 2026-02-01 | 3 | 2 |
| 290236 | — | — | — | 2026-04-01 | 2 | 1 |
| 290236 | — | — | — | 2026-05-01 | 1 | 1 |
| 290240 | — | — | — | 2026-02-01 | 2 | 2 |
| 290240 | — | — | — | 2026-03-01 | 2 | 2 |
| 290241 | 0241 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 3 | 3 |
| 290241 | 0241 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 1 | 2 |
| 290241 | 0241 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 3 | 2 |
| 290241 | 0241 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 2 | 2 |
| 290241 | 0241 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 3 | 2 |
| 290241 | 0241 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 2 | 2 |
| 290242 | — | — | — | 2026-02-01 | 1 | 1 |
| 290242 | — | — | — | 2026-06-01 | 2 | 1 |
| 290243 | — | — | — | 2026-02-01 | 1 | 1 |
| 290244 | — | — | — | 2026-03-01 | 2 | 1 |
| 290244 | — | — | — | 2026-04-01 | 4 | 3 |
| 290244 | — | — | — | 2026-06-01 | 1 | 1 |
| 290245 | — | — | — | 2026-03-01 | 1 | 1 |
| 290245 | — | — | — | 2026-04-01 | 2 | 1 |
| 290246 | — | — | — | 2026-02-01 | 4 | 1 |
| 290246 | — | — | — | 2026-04-01 | 6 | 1 |
| 290246 | — | — | — | 2026-06-01 | 1 | 1 |
| 290254 | — | — | — | 2026-01-01 | 3 | 3 |
| 290254 | — | — | — | 2026-04-01 | 1 | 1 |
| 290261 | — | — | — | 2026-02-01 | 2 | 2 |
| 290261 | — | — | — | 2026-04-01 | 1 | 1 |
| 290264 | — | — | — | 2026-05-01 | 1 | 1 |
| 290266 | — | — | — | 2026-01-01 | 3 | 2 |
| 290266 | — | — | — | 2026-02-01 | 1 | 1 |
| 290266 | — | — | — | 2026-05-01 | 3 | 3 |
| 290268 | — | — | — | 2026-01-01 | 2 | 1 |
| 290268 | — | — | — | 2026-03-01 | 1 | 1 |
| 290268 | — | — | — | 2026-05-01 | 4 | 2 |
| 290268 | — | — | — | 2026-06-01 | 1 | 1 |
| 290271 | — | — | — | 2026-01-01 | 4 | 1 |
| 290271 | — | — | — | 2026-02-01 | 1 | 1 |
| 290271 | — | — | — | 2026-05-01 | 4 | 1 |
| 290272 | — | — | — | 2026-01-01 | 4 | 1 |
| 290272 | — | — | — | 2026-05-01 | 4 | 1 |
| 290275 | — | — | — | 2026-01-01 | 3 | 2 |
| 290275 | — | — | — | 2026-04-01 | 2 | 2 |
| 290275 | — | — | — | 2026-06-01 | 1 | 1 |
| 290278 | — | — | — | 2026-03-01 | 2 | 1 |
| 290279 | — | — | — | 2026-01-01 | 1 | 1 |
| 290282 | — | — | — | 2026-01-01 | 1 | 1 |
| 290282 | — | — | — | 2026-02-01 | 1 | 1 |
| 290282 | — | — | — | 2026-05-01 | 5 | 1 |
| 290283 | — | — | — | 2026-01-01 | 1 | 1 |
| 290283 | — | — | — | 2026-04-01 | 1 | 1 |
| 290283 | — | — | — | 2026-06-01 | 1 | 1 |
| 290287 | — | — | — | 2026-06-01 | 1 | 1 |
| 290289 | — | — | — | 2026-02-01 | 2 | 2 |
| 290289 | — | — | — | 2026-03-01 | 1 | 1 |
| 290289 | — | — | — | 2026-04-01 | 2 | 1 |
| 290289 | — | — | — | 2026-05-01 | 6 | 1 |
| 290289 | — | — | — | 2026-06-01 | 2 | 2 |
| 290301 | — | — | — | 2026-01-01 | 3 | 2 |
| 290301 | — | — | — | 2026-05-01 | 1 | 1 |
| 290302 | — | — | — | 2026-05-01 | 1 | 1 |
| 290303 | — | — | — | 2026-02-01 | 1 | 1 |
| 290303 | — | — | — | 2026-03-01 | 1 | 1 |
| 290303 | — | — | — | 2026-04-01 | 1 | 1 |
| 290303 | — | — | — | 2026-05-01 | 9 | 2 |
| 290305 | — | — | — | 2025-12-01 | 1 | 1 |
| 290305 | — | — | — | 2026-01-01 | 3 | 2 |
| 290307 | — | — | — | 2026-03-01 | 1 | 1 |
| 290312 | — | — | — | 2026-02-01 | 1 | 1 |
| 290313 | — | — | — | 2026-02-01 | 1 | 1 |
| 290313 | — | — | — | 2026-03-01 | 1 | 1 |
| 290313 | — | — | — | 2026-04-01 | 1 | 1 |
| 290313 | — | — | — | 2026-05-01 | 2 | 2 |
| 290314 | — | — | — | 2025-12-01 | 3 | 1 |
| 290314 | — | — | — | 2026-02-01 | 1 | 1 |
| 290314 | — | — | — | 2026-04-01 | 1 | 1 |
| 290319 | — | — | — | 2026-01-01 | 2 | 2 |
| 290319 | — | — | — | 2026-03-01 | 2 | 1 |
| 290319 | — | — | — | 2026-04-01 | 4 | 2 |
| 290319 | — | — | — | 2026-06-01 | 2 | 1 |
| 290324 | — | — | — | 2026-01-01 | 4 | 4 |
| 290328 | — | — | — | 2026-01-01 | 1 | 1 |
| 290328 | — | — | — | 2026-03-01 | 1 | 1 |
| 290328 | — | — | — | 2026-04-01 | 2 | 2 |
| 290328 | — | — | — | 2026-05-01 | 1 | 1 |
| 290328 | — | — | — | 2026-06-01 | 1 | 1 |
| 290330 | — | — | — | 2026-02-01 | 1 | 1 |
| 290331 | — | — | — | 2026-01-01 | 1 | 1 |
| 290332 | — | — | — | 2026-03-01 | 2 | 1 |
| 290332 | — | — | — | 2026-05-01 | 3 | 2 |
| 290333 | — | — | — | 2025-12-01 | 1 | 1 |
| 290333 | — | — | — | 2026-01-01 | 1 | 1 |
| 290333 | — | — | — | 2026-02-01 | 1 | 1 |
| 290333 | — | — | — | 2026-05-01 | 1 | 1 |
| 290340 | — | — | — | 2026-04-01 | 1 | 1 |
| 290343 | — | — | — | 2025-12-01 | 3 | 2 |
| 290343 | — | — | — | 2026-01-01 | 3 | 3 |
| 290343 | — | — | — | 2026-02-01 | 4 | 3 |
| 290343 | — | — | — | 2026-03-01 | 5 | 5 |
| 290343 | — | — | — | 2026-04-01 | 1 | 1 |
| 290343 | — | — | — | 2026-05-01 | 8 | 6 |
| 290346 | — | — | — | 2026-01-01 | 3 | 3 |
| 290347 | — | — | — | 2026-02-01 | 1 | 1 |
| 290347 | — | — | — | 2026-05-01 | 1 | 1 |
| 290349 | 0349 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 5 | 3 |
| 290349 | 0349 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 3 | 2 |
| 290349 | 0349 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 1 | 1 |
| 290349 | 0349 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 8 | 4 |
| 290350 | — | — | — | 2026-01-01 | 2 | 1 |
| 290350 | — | — | — | 2026-03-01 | 2 | 2 |
| 290351 | — | — | — | 2026-01-01 | 2 | 1 |
| 290351 | — | — | — | 2026-03-01 | 1 | 1 |
| 290351 | — | — | — | 2026-04-01 | 1 | 1 |
| 290351 | — | — | — | 2026-05-01 | 3 | 2 |
| 290352 | 0352 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 11 | 6 |
| 290352 | 0352 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 10 | 6 |
| 290352 | 0352 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 2 | 1 |
| 290352 | 0352 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 1 | 1 |
| 290352 | 0352 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 5 | 1 |
| 290352 | 0352 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 6 | 1 |
| 290354 | — | — | — | 2026-02-01 | 4 | 2 |
| 290355 | — | — | — | 2026-01-01 | 1 | 1 |
| 290361 | — | — | — | 2026-01-01 | 1 | 1 |
| 290361 | — | — | — | 2026-04-01 | 2 | 2 |
| 290361 | — | — | — | 2026-05-01 | 1 | 1 |
| 290366 | — | — | — | 2026-04-01 | 2 | 2 |
| 290377 | 0377 1pc Replacement Glass | GLASS | COL154 | 2025-12-01 | 2 | 2 |
| 290377 | 0377 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 11 | 3 |
| 290377 | 0377 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 6 | 4 |
| 290377 | 0377 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 2 | 2 |
| 290377 | 0377 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 1 | 1 |
| 290377 | 0377 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 11 | 6 |
| 290380 | 0065 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 4 | 4 |
| 290380 | 0065 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 2 | 1 |
| 290380 | 0065 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 3 | 3 |
| 290380 | 0065 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 9 | 2 |
| 290380 | 0065 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 9 | 4 |
| 290381 | 0066 1pc Replacement Glass | GLASS | COL154 | 2025-12-01 | 2 | 1 |
| 290381 | 0066 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 6 | 3 |
| 290381 | 0066 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 14 | 4 |
| 290381 | 0066 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 4 | 4 |
| 290381 | 0066 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 20 | 6 |
| 290381 | 0066 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 3 | 3 |
| 290384 | — | — | — | 2026-01-01 | 6 | 3 |
| 290384 | — | — | — | 2026-02-01 | 1 | 1 |
| 290384 | — | — | — | 2026-03-01 | 2 | 1 |
| 290384 | — | — | — | 2026-04-01 | 1 | 1 |
| 290384 | — | — | — | 2026-06-01 | 1 | 1 |
| 290386 | — | — | — | 2026-02-01 | 1 | 1 |
| 290387 | — | — | — | 2026-01-01 | 1 | 1 |
| 290389 | — | — | — | 2026-03-01 | 3 | 3 |
| 290389 | — | — | — | 2026-06-01 | 2 | 1 |
| 290391 | — | — | — | 2026-03-01 | 1 | 1 |
| 290392 | — | — | — | 2025-12-01 | 3 | 2 |
| 290392 | — | — | — | 2026-01-01 | 7 | 2 |
| 290392 | — | — | — | 2026-02-01 | 3 | 1 |
| 290392 | — | — | — | 2026-05-01 | 1 | 1 |
| 290397 | — | — | — | 2026-06-01 | 1 | 1 |
| 290398 | — | — | — | 2026-02-01 | 1 | 1 |
| 290420 | — | — | — | 2025-12-01 | 3 | 2 |
| 290420 | — | — | — | 2026-01-01 | 2 | 1 |
| 290420 | — | — | — | 2026-02-01 | 1 | 1 |
| 290420 | — | — | — | 2026-04-01 | 6 | 2 |
| 290420 | — | — | — | 2026-05-01 | 7 | 4 |
| 290425 | — | — | — | 2026-04-01 | 1 | 1 |
| 290426 | — | — | — | 2026-03-01 | 1 | 1 |
| 290434 | — | — | — | 2025-12-01 | 1 | 1 |
| 290434 | — | — | — | 2026-01-01 | 1 | 1 |
| 290434 | — | — | — | 2026-03-01 | 1 | 1 |
| 290434 | — | — | — | 2026-04-01 | 1 | 1 |
| 290434 | — | — | — | 2026-05-01 | 3 | 1 |
| 290435 | — | — | — | 2025-12-01 | 1 | 1 |
| 290435 | — | — | — | 2026-01-01 | 1 | 1 |
| 290435 | — | — | — | 2026-03-01 | 1 | 1 |
| 290435 | — | — | — | 2026-04-01 | 6 | 1 |
| 290435 | — | — | — | 2026-05-01 | 1 | 1 |
| 290436 | — | — | — | 2025-12-01 | 8 | 4 |
| 290436 | — | — | — | 2026-01-01 | 5 | 4 |
| 290436 | — | — | — | 2026-02-01 | 1 | 1 |
| 290436 | — | — | — | 2026-03-01 | 8 | 5 |
| 290436 | — | — | — | 2026-04-01 | 4 | 4 |
| 290436 | — | — | — | 2026-05-01 | 7 | 5 |
| 290436 | — | — | — | 2026-06-01 | 5 | 3 |
| 290441 | — | — | — | 2025-12-01 | 1 | 1 |
| 290441 | — | — | — | 2026-01-01 | 3 | 2 |
| 290441 | — | — | — | 2026-02-01 | 1 | 1 |
| 290441 | — | — | — | 2026-03-01 | 1 | 1 |
| 290441 | — | — | — | 2026-04-01 | 1 | 1 |
| 290442 | — | — | — | 2026-01-01 | 6 | 2 |
| 290442 | — | — | — | 2026-02-01 | 1 | 1 |
| 290442 | — | — | — | 2026-04-01 | 5 | 1 |
| 290442 | — | — | — | 2026-05-01 | 1 | 1 |
| 290444 | — | — | — | 2026-06-01 | 1 | 1 |
| 290447 | — | — | — | 2026-01-01 | 2 | 1 |
| 290447 | — | — | — | 2026-02-01 | 1 | 1 |
| 290447 | — | — | — | 2026-04-01 | 4 | 1 |
| 290447 | — | — | — | 2026-05-01 | 3 | 3 |
| 290448 | — | — | — | 2026-01-01 | 4 | 3 |
| 290448 | — | — | — | 2026-02-01 | 8 | 5 |
| 290448 | — | — | — | 2026-03-01 | 3 | 2 |
| 290448 | — | — | — | 2026-04-01 | 1 | 1 |
| 290448 | — | — | — | 2026-05-01 | 2 | 2 |
| 290448 | — | — | — | 2026-06-01 | 3 | 3 |
| 290462 | — | — | — | 2025-12-01 | 1 | 1 |
| 290462 | — | — | — | 2026-01-01 | 4 | 3 |
| 290462 | — | — | — | 2026-02-01 | 4 | 2 |
| 290462 | — | — | — | 2026-03-01 | 9 | 7 |
| 290462 | — | — | — | 2026-04-01 | 16 | 9 |
| 290462 | — | — | — | 2026-05-01 | 12 | 6 |
| 290462 | — | — | — | 2026-06-01 | 15 | 5 |
| 290467 | — | — | — | 2026-01-01 | 5 | 4 |
| 290467 | — | — | — | 2026-02-01 | 1 | 1 |
| 290467 | — | — | — | 2026-03-01 | 6 | 2 |
| 290467 | — | — | — | 2026-04-01 | 1 | 1 |
| 290467 | — | — | — | 2026-05-01 | 1 | 1 |
| 290469 | — | — | — | 2026-03-01 | 1 | 1 |
| 290469 | — | — | — | 2026-05-01 | 13 | 2 |
| 290470 | — | — | — | 2026-02-01 | 1 | 1 |
| 290470 | — | — | — | 2026-03-01 | 2 | 1 |
| 290470 | — | — | — | 2026-05-01 | 8 | 3 |
| 290474 | — | — | — | 2026-01-01 | 1 | 1 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2025-12-01 | 6 | 5 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 3 | 3 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 5 | 5 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 3 | 2 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 3 | 2 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 1 | 1 |
| 290475 | 0075 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 2 | 2 |
| 290480 | — | — | — | 2026-01-01 | 1 | 1 |
| 290480 | — | — | — | 2026-04-01 | 1 | 1 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2025-12-01 | 9 | 2 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2026-01-01 | 2 | 2 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2026-02-01 | 8 | 5 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2026-03-01 | 18 | 10 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2026-04-01 | 61 | 9 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2026-05-01 | 6 | 5 |
| 290481 | 0034 1pc Glass Replacement | GLASS | COL154 | 2026-06-01 | 16 | 5 |
| 290482 | — | — | — | 2026-02-01 | 1 | 1 |
| 290482 | — | — | — | 2026-05-01 | 1 | 1 |
| 290489 | — | — | — | 2026-03-01 | 1 | 1 |
| 290489 | — | — | — | 2026-05-01 | 2 | 1 |
| 290490 | — | — | — | 2026-04-01 | 1 | 1 |
| 290491 | — | — | — | 2026-03-01 | 1 | 1 |
| 290492 | — | — | — | 2026-02-01 | 1 | 1 |
| 290492 | — | — | — | 2026-05-01 | 2 | 1 |
| 290497 | — | — | — | 2026-04-01 | 2 | 2 |
| 290497 | — | — | — | 2026-05-01 | 1 | 1 |
| 290497 | — | — | — | 2026-06-01 | 1 | 1 |
| 290501 | — | — | — | 2026-05-01 | 1 | 1 |
| 290505 | — | — | — | 2026-03-01 | 1 | 1 |
| 290506 | — | — | — | 2025-12-01 | 1 | 1 |
| 290506 | — | — | — | 2026-01-01 | 1 | 1 |
| 290506 | — | — | — | 2026-04-01 | 1 | 1 |
| 290513 | — | — | — | 2025-12-01 | 2 | 2 |
| 290513 | — | — | — | 2026-01-01 | 17 | 12 |
| 290513 | — | — | — | 2026-02-01 | 9 | 5 |
| 290513 | — | — | — | 2026-03-01 | 11 | 4 |
| 290513 | — | — | — | 2026-04-01 | 4 | 3 |
| 290513 | — | — | — | 2026-05-01 | 6 | 5 |
| 290513 | — | — | — | 2026-06-01 | 4 | 3 |
| 290514 | — | — | — | 2026-01-01 | 7 | 1 |
| 290514 | — | — | — | 2026-02-01 | 1 | 1 |
| 290514 | — | — | — | 2026-03-01 | 1 | 1 |
| 290518 | — | — | — | 2026-01-01 | 5 | 2 |
| 290518 | — | — | — | 2026-02-01 | 7 | 4 |
| 290518 | — | — | — | 2026-03-01 | 1 | 1 |
| 290518 | — | — | — | 2026-04-01 | 1 | 1 |
| 290518 | — | — | — | 2026-05-01 | 1 | 1 |
| 290518 | — | — | — | 2026-06-01 | 1 | 1 |
| 290520 | — | — | — | 2026-01-01 | 4 | 3 |
| 290520 | — | — | — | 2026-03-01 | 3 | 2 |
| 290546 | — | — | — | 2026-01-01 | 1 | 1 |
| 290546 | — | — | — | 2026-02-01 | 5 | 2 |
| 290546 | — | — | — | 2026-03-01 | 1 | 1 |
| 290546 | — | — | — | 2026-04-01 | 1 | 1 |
| 290546 | — | — | — | 2026-05-01 | 5 | 2 |
| 290549 | — | — | — | 2026-01-01 | 5 | 1 |
| 290549 | — | — | — | 2026-02-01 | 4 | 1 |
| 290549 | — | — | — | 2026-05-01 | 1 | 1 |
| 290555 | — | — | — | 2025-12-01 | 1 | 1 |
| 290560 | — | — | — | 2026-03-01 | 2 | 2 |
| 290560 | — | — | — | 2026-04-01 | 3 | 2 |
| 290564 | — | — | — | 2026-03-01 | 7 | 1 |
| 290565 | — | — | — | 2026-01-01 | 1 | 1 |
| 290566 | — | — | — | 2026-03-01 | 2 | 1 |
| 290566 | — | — | — | 2026-06-01 | 1 | 1 |
| 290567 | — | — | — | 2025-12-01 | 1 | 1 |
| 290567 | — | — | — | 2026-01-01 | 1 | 1 |
| 290570 | — | — | — | 2025-12-01 | 1 | 1 |
| 290570 | — | — | — | 2026-01-01 | 1 | 1 |
| 290570 | — | — | — | 2026-03-01 | 1 | 1 |
| 290570 | — | — | — | 2026-04-01 | 6 | 1 |
| 290572 | — | — | — | 2026-01-01 | 1 | 1 |
| 290572 | — | — | — | 2026-03-01 | 1 | 1 |
| 290573 | — | — | — | 2026-02-01 | 2 | 2 |
| 290573 | — | — | — | 2026-04-01 | 1 | 1 |
| 290573 | — | — | — | 2026-06-01 | 2 | 2 |
| 290577 | — | — | — | 2026-05-01 | 1 | 1 |
| 290580 | — | — | — | 2026-03-01 | 1 | 1 |
| 290580 | — | — | — | 2026-04-01 | 1 | 1 |
| 290581 | 0037 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 8 | 5 |
| 290581 | 0037 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 8 | 5 |
| 290581 | 0037 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 7 | 6 |
| 290581 | 0037 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 5 | 4 |
| 290581 | 0037 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 14 | 10 |
| 290581 | 0037 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 12 | 6 |
| 290583 | — | — | — | 2026-02-01 | 2 | 2 |
| 290583 | — | — | — | 2026-04-01 | 1 | 1 |
| 290589 | 0169 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 6 | 3 |
| 290589 | 0169 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 2 | 1 |
| 290590 | — | — | — | 2026-02-01 | 1 | 1 |
| 290590 | — | — | — | 2026-04-01 | 2 | 1 |
| 290590 | — | — | — | 2026-05-01 | 2 | 1 |
| 290591 | — | — | — | 2025-12-01 | 2 | 1 |
| 290591 | — | — | — | 2026-01-01 | 2 | 2 |
| 290591 | — | — | — | 2026-02-01 | 6 | 3 |
| 290591 | — | — | — | 2026-03-01 | 1 | 1 |
| 290591 | — | — | — | 2026-04-01 | 3 | 3 |
| 290604 | — | — | — | 2026-02-01 | 5 | 2 |
| 290604 | — | — | — | 2026-03-01 | 1 | 1 |
| 290604 | — | — | — | 2026-05-01 | 1 | 1 |
| 290605 | — | — | — | 2026-02-01 | 1 | 1 |
| 290605 | — | — | — | 2026-03-01 | 2 | 2 |
| 290605 | — | — | — | 2026-04-01 | 4 | 3 |
| 290605 | — | — | — | 2026-05-01 | 8 | 4 |
| 290608 | — | — | — | 2026-04-01 | 1 | 1 |
| 290611 | 0611 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 11 | 5 |
| 290611 | 0611 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 2 | 2 |
| 290611 | 0611 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 11 | 5 |
| 290611 | 0611 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 8 | 3 |
| 290611 | 0611 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 3 | 3 |
| 290611 | 0611 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 9 | 2 |
| 290616 | — | — | — | 2026-03-01 | 1 | 1 |
| 290617 | — | — | — | 2026-02-01 | 1 | 1 |
| 290618 | — | — | — | 2026-04-01 | 10 | 1 |
| 290620 | — | — | — | 2026-04-01 | 3 | 2 |
| 290621 | — | — | — | 2026-01-01 | 1 | 1 |
| 290621 | — | — | — | 2026-02-01 | 4 | 2 |
| 290622 | — | — | — | 2026-04-01 | 1 | 1 |
| 290626 | — | — | — | 2025-12-01 | 1 | 1 |
| 290626 | — | — | — | 2026-02-01 | 2 | 1 |
| 290626 | — | — | — | 2026-05-01 | 3 | 2 |
| 290626 | — | — | — | 2026-06-01 | 1 | 1 |
| 290629 | — | — | — | 2026-01-01 | 16 | 3 |
| 290629 | — | — | — | 2026-02-01 | 1 | 1 |
| 290629 | — | — | — | 2026-04-01 | 5 | 2 |
| 290629 | — | — | — | 2026-05-01 | 5 | 3 |
| 290629 | — | — | — | 2026-06-01 | 3 | 2 |
| 290631 | — | — | — | 2025-12-01 | 1 | 1 |
| 290631 | — | — | — | 2026-01-01 | 12 | 1 |
| 290631 | — | — | — | 2026-04-01 | 1 | 1 |
| 290631 | — | — | — | 2026-05-01 | 4 | 2 |
| 290631 | — | — | — | 2026-06-01 | 1 | 1 |
| 290642 | — | — | — | 2025-12-01 | 1 | 1 |
| 290642 | — | — | — | 2026-01-01 | 10 | 6 |
| 290642 | — | — | — | 2026-02-01 | 7 | 4 |
| 290642 | — | — | — | 2026-04-01 | 6 | 4 |
| 290642 | — | — | — | 2026-05-01 | 4 | 4 |
| 290642 | — | — | — | 2026-06-01 | 2 | 2 |
| 290648 | — | — | — | 2026-01-01 | 3 | 2 |
| 290648 | — | — | — | 2026-03-01 | 4 | 1 |
| 290648 | — | — | — | 2026-04-01 | 1 | 1 |
| 290648 | — | — | — | 2026-05-01 | 6 | 3 |
| 290653 | — | — | — | 2026-04-01 | 1 | 1 |
| 290653 | — | — | — | 2026-05-01 | 1 | 1 |
| 290655 | — | — | — | 2026-03-01 | 1 | 1 |
| 290663 | — | — | — | 2026-01-01 | 1 | 1 |
| 290663 | — | — | — | 2026-04-01 | 1 | 1 |
| 290668 | — | — | — | 2025-12-01 | 40 | 1 |
| 290668 | — | — | — | 2026-03-01 | 3 | 2 |
| 290670 | — | — | — | 2026-03-01 | 2 | 1 |
| 290670 | — | — | — | 2026-04-01 | 1 | 1 |
| 290671 | — | — | — | 2026-05-01 | 8 | 3 |
| 290671 | — | — | — | 2026-06-01 | 1 | 1 |
| 290672 | — | — | — | 2026-05-01 | 1 | 1 |
| 290673 | — | — | — | 2026-02-01 | 2 | 1 |
| 290673 | — | — | — | 2026-03-01 | 1 | 1 |
| 290674 | — | — | — | 2026-01-01 | 1 | 1 |
| 290674 | — | — | — | 2026-03-01 | 2 | 2 |
| 290674 | — | — | — | 2026-05-01 | 3 | 2 |
| 290674 | — | — | — | 2026-06-01 | 1 | 1 |
| 290676 | — | — | — | 2026-01-01 | 1 | 1 |
| 290681 | — | — | — | 2026-02-01 | 2 | 2 |
| 290681 | — | — | — | 2026-03-01 | 3 | 1 |
| 290681 | — | — | — | 2026-04-01 | 3 | 3 |
| 290681 | — | — | — | 2026-05-01 | 3 | 3 |
| 290681 | — | — | — | 2026-06-01 | 4 | 2 |
| 290685 | — | — | — | 2026-02-01 | 1 | 1 |
| 290685 | — | — | — | 2026-06-01 | 1 | 1 |
| 290686 | — | — | — | 2025-12-01 | 1 | 1 |
| 290686 | — | — | — | 2026-04-01 | 1 | 1 |
| 290686 | — | — | — | 2026-05-01 | 3 | 1 |
| 290693 | — | — | — | 2025-12-01 | 1 | 1 |
| 290693 | — | — | — | 2026-01-01 | 3 | 1 |
| 290693 | — | — | — | 2026-02-01 | 1 | 1 |
| 290693 | — | — | — | 2026-03-01 | 2 | 2 |
| 290693 | — | — | — | 2026-04-01 | 3 | 2 |
| 290693 | — | — | — | 2026-05-01 | 1 | 1 |
| 290699 | — | — | — | 2025-12-01 | 1 | 1 |
| 290699 | — | — | — | 2026-01-01 | 1 | 1 |
| 290699 | — | — | — | 2026-06-01 | 1 | 1 |
| 290700 | — | — | — | 2026-02-01 | 3 | 3 |
| 290700 | — | — | — | 2026-03-01 | 1 | 1 |
| 290700 | — | — | — | 2026-04-01 | 1 | 1 |
| 290703 | — | — | — | 2026-01-01 | 1 | 1 |
| 290705 | — | — | — | 2026-01-01 | 3 | 3 |
| 290705 | — | — | — | 2026-05-01 | 1 | 1 |
| 290706 | — | — | — | 2026-01-01 | 5 | 4 |
| 290706 | — | — | — | 2026-02-01 | 6 | 4 |
| 290706 | — | — | — | 2026-03-01 | 2 | 2 |
| 290706 | — | — | — | 2026-04-01 | 4 | 4 |
| 290706 | — | — | — | 2026-05-01 | 7 | 2 |
| 290706 | — | — | — | 2026-06-01 | 1 | 1 |
| 290707 | — | — | — | 2026-01-01 | 2 | 1 |
| 290707 | — | — | — | 2026-02-01 | 5 | 3 |
| 290707 | — | — | — | 2026-03-01 | 3 | 2 |
| 290707 | — | — | — | 2026-04-01 | 1 | 1 |
| 290707 | — | — | — | 2026-05-01 | 6 | 4 |
| 290707 | — | — | — | 2026-06-01 | 1 | 1 |
| 290709 | — | — | — | 2026-06-01 | 2 | 1 |
| 290718 | — | — | — | 2026-04-01 | 1 | 1 |
| 290718 | — | — | — | 2026-06-01 | 2 | 1 |
| 290719 | — | — | — | 2025-12-01 | 2 | 1 |
| 290719 | — | — | — | 2026-01-01 | 4 | 4 |
| 290719 | — | — | — | 2026-02-01 | 1 | 1 |
| 290719 | — | — | — | 2026-04-01 | 1 | 1 |
| 290721 | — | — | — | 2026-05-01 | 1 | 1 |
| 290727 | — | — | — | 2026-01-01 | 1 | 1 |
| 290727 | — | — | — | 2026-03-01 | 1 | 1 |
| 290731 | — | — | — | 2026-02-01 | 3 | 3 |
| 290731 | — | — | — | 2026-04-01 | 1 | 1 |
| 290735 | — | — | — | 2026-05-01 | 1 | 1 |
| 290736 | — | — | — | 2026-03-01 | 1 | 1 |
| 290737 | — | — | — | 2026-03-01 | 2 | 2 |
| 290738 | — | — | — | 2026-03-01 | 1 | 1 |
| 290739 | — | — | — | 2026-02-01 | 1 | 1 |
| 290739 | — | — | — | 2026-03-01 | 1 | 1 |
| 290741 | — | — | — | 2026-01-01 | 2 | 1 |
| 290741 | — | — | — | 2026-02-01 | 1 | 1 |
| 290741 | — | — | — | 2026-03-01 | 2 | 2 |
| 290741 | — | — | — | 2026-06-01 | 2 | 1 |
| 290742 | — | — | — | 2026-02-01 | 5 | 1 |
| 290742 | — | — | — | 2026-04-01 | 1 | 1 |
| 290742 | — | — | — | 2026-05-01 | 1 | 1 |
| 290743 | — | — | — | 2026-05-01 | 3 | 3 |
| 290746 | — | — | — | 2025-12-01 | 1 | 1 |
| 290747 | — | — | — | 2026-01-01 | 2 | 2 |
| 290747 | — | — | — | 2026-02-01 | 1 | 1 |
| 290748 | — | — | — | 2026-02-01 | 1 | 1 |
| 290748 | — | — | — | 2026-04-01 | 1 | 1 |
| 290751 | — | — | — | 2026-03-01 | 2 | 1 |
| 290751 | — | — | — | 2026-05-01 | 1 | 1 |
| 290753 | — | — | — | 2026-01-01 | 1 | 1 |
| 290753 | — | — | — | 2026-04-01 | 1 | 1 |
| 290780 | — | — | — | 2025-12-01 | 1 | 1 |
| 290780 | — | — | — | 2026-01-01 | 1 | 1 |
| 290780 | — | — | — | 2026-03-01 | 1 | 1 |
| 290781 | — | — | — | 2026-05-01 | 2 | 1 |
| 290782 | — | — | — | 2025-12-01 | 1 | 1 |
| 290782 | — | — | — | 2026-03-01 | 3 | 2 |
| 290782 | — | — | — | 2026-04-01 | 1 | 1 |
| 290782 | — | — | — | 2026-05-01 | 1 | 1 |
| 290782 | — | — | — | 2026-06-01 | 1 | 1 |
| 290784 | — | — | — | 2026-01-01 | 1 | 1 |
| 290784 | — | — | — | 2026-04-01 | 1 | 1 |
| 290785 | — | — | — | 2026-02-01 | 1 | 1 |
| 290785 | — | — | — | 2026-06-01 | 2 | 2 |
| 290787 | — | — | — | 2025-12-01 | 1 | 1 |
| 290787 | — | — | — | 2026-05-01 | 1 | 1 |
| 290788 | — | — | — | 2026-02-01 | 1 | 1 |
| 290791 | — | — | — | 2026-01-01 | 1 | 1 |
| 290792 | — | — | — | 2026-04-01 | 1 | 1 |
| 290793 | — | — | — | 2026-01-01 | 1 | 1 |
| 290793 | — | — | — | 2026-03-01 | 1 | 1 |
| 290794 | — | — | — | 2026-04-01 | 1 | 1 |
| 290795 | — | — | — | 2025-12-01 | 1 | 1 |
| 290795 | — | — | — | 2026-03-01 | 3 | 2 |
| 290795 | — | — | — | 2026-05-01 | 1 | 1 |
| 290797 | — | — | — | 2026-01-01 | 3 | 2 |
| 290797 | — | — | — | 2026-02-01 | 1 | 1 |
| 290797 | — | — | — | 2026-04-01 | 2 | 2 |
| 290799 | — | — | — | 2025-12-01 | 1 | 1 |
| 290799 | — | — | — | 2026-01-01 | 6 | 3 |
| 290799 | — | — | — | 2026-02-01 | 1 | 1 |
| 290799 | — | — | — | 2026-03-01 | 2 | 2 |
| 290799 | — | — | — | 2026-04-01 | 1 | 1 |
| 290799 | — | — | — | 2026-05-01 | 2 | 2 |
| 290799 | — | — | — | 2026-06-01 | 2 | 2 |
| 290800 | — | — | — | 2026-04-01 | 1 | 1 |
| 290800 | — | — | — | 2026-05-01 | 1 | 1 |
| 290808 | — | — | — | 2026-02-01 | 1 | 1 |
| 290808 | — | — | — | 2026-04-01 | 1 | 1 |
| 290809-SE | — | — | — | 2026-04-01 | 2 | 1 |
| 290812 | — | — | — | 2026-05-01 | 1 | 1 |
| 290813-SE | — | — | — | 2026-04-01 | 1 | 1 |
| 290815 | — | — | — | 2026-01-01 | 1 | 2 |
| 290815 | — | — | — | 2026-04-01 | 3 | 2 |
| 290815 | — | — | — | 2026-06-01 | 1 | 1 |
| 290818 | — | — | — | 2025-12-01 | 1 | 1 |
| 290818 | — | — | — | 2026-01-01 | 1 | 1 |
| 290818 | — | — | — | 2026-03-01 | 1 | 1 |
| 290818 | — | — | — | 2026-04-01 | 10 | 1 |
| 290819 | — | — | — | 2026-02-01 | 3 | 1 |
| 290821 | — | — | — | 2025-12-01 | 9 | 3 |
| 290821 | — | — | — | 2026-01-01 | 5 | 2 |
| 290821 | — | — | — | 2026-03-01 | 14 | 4 |
| 290821 | — | — | — | 2026-04-01 | 3 | 2 |
| 290821 | — | — | — | 2026-05-01 | 2 | 2 |
| 290821 | — | — | — | 2026-06-01 | 3 | 2 |
| 290822 | — | — | — | 2025-12-01 | 3 | 2 |
| 290822 | — | — | — | 2026-01-01 | 14 | 3 |
| 290822 | — | — | — | 2026-02-01 | 2 | 1 |
| 290822 | — | — | — | 2026-03-01 | 2 | 2 |
| 290822 | — | — | — | 2026-04-01 | 12 | 3 |
| 290822 | — | — | — | 2026-05-01 | 13 | 2 |
| 290822 | — | — | — | 2026-06-01 | 10 | 1 |
| 290823 | — | — | — | 2025-12-01 | 4 | 3 |
| 290823 | — | — | — | 2026-02-01 | 3 | 2 |
| 290823 | — | — | — | 2026-03-01 | 9 | 3 |
| 290823 | — | — | — | 2026-04-01 | 4 | 3 |
| 290823 | — | — | — | 2026-05-01 | 1 | 1 |
| 290823 | — | — | — | 2026-06-01 | 1 | 1 |
| 290824 | — | — | — | 2026-03-01 | 4 | 2 |
| 290824 | — | — | — | 2026-05-01 | 4 | 2 |
| 290824 | — | — | — | 2026-06-01 | 1 | 1 |
| 290825 | — | — | — | 2025-12-01 | 2 | 1 |
| 290825 | — | — | — | 2026-03-01 | 1 | 1 |
| 290825 | — | — | — | 2026-04-01 | 1 | 1 |
| 290825 | — | — | — | 2026-05-01 | 1 | 1 |
| 290826 | — | — | — | 2026-01-01 | 1 | 1 |
| 290826 | — | — | — | 2026-04-01 | 1 | 1 |
| 290826 | — | — | — | 2026-06-01 | 1 | 1 |
| 290828 | — | — | — | 2025-12-01 | 1 | 1 |
| 290828 | — | — | — | 2026-03-01 | 1 | 1 |
| 290828 | — | — | — | 2026-06-01 | 1 | 1 |
| 290830 | — | — | — | 2025-12-01 | 1 | 1 |
| 290831 | — | — | — | 2026-04-01 | 1 | 1 |
| 290831 | — | — | — | 2026-05-01 | 1 | 1 |
| 290832 | — | — | — | 2026-04-01 | 1 | 1 |
| 290833 | — | — | — | 2025-12-01 | 1 | 1 |
| 290833 | — | — | — | 2026-01-01 | 2 | 2 |
| 290835 | — | — | — | 2026-03-01 | 1 | 1 |
| 290836 | — | — | — | 2026-02-01 | 1 | 1 |
| 290838 | — | — | — | 2026-01-01 | 3 | 1 |
| 290838 | — | — | — | 2026-02-01 | 2 | 2 |
| 290838 | — | — | — | 2026-05-01 | 2 | 1 |
| 290842 | — | — | — | 2026-05-01 | 2 | 1 |
| 290842 | — | — | — | 2026-06-01 | 1 | 1 |
| 290843 | — | — | — | 2026-05-01 | 7 | 4 |
| 290844 | — | — | — | 2026-01-01 | 2 | 2 |
| 290844 | — | — | — | 2026-04-01 | 1 | 1 |
| 290844 | — | — | — | 2026-05-01 | 11 | 4 |
| 290845 | — | — | — | 2026-01-01 | 2 | 2 |
| 290845 | — | — | — | 2026-05-01 | 12 | 4 |
| 290847 | — | — | — | 2025-12-01 | 1 | 1 |
| 290847 | — | — | — | 2026-04-01 | 1 | 1 |
| 290847 | — | — | — | 2026-05-01 | 4 | 2 |
| 290848 | — | — | — | 2025-12-01 | 1 | 1 |
| 290848 | — | — | — | 2026-02-01 | 5 | 1 |
| 290850 | — | — | — | 2026-05-01 | 3 | 1 |
| 290851 | — | — | — | 2026-04-01 | 1 | 1 |
| 290859 | — | — | — | 2026-02-01 | 1 | 1 |
| 290859 | — | — | — | 2026-04-01 | 1 | 1 |
| 290859 | — | — | — | 2026-06-01 | 1 | 1 |
| 290864 | — | — | — | 2026-03-01 | 1 | 1 |
| 290864 | — | — | — | 2026-05-01 | 12 | 1 |
| 290866 | — | — | — | 2026-04-01 | 2 | 1 |
| 290867 | — | — | — | 2026-04-01 | 1 | 1 |
| 290872 | — | — | — | 2026-04-01 | 1 | 1 |
| 290873 | — | — | — | 2026-04-01 | 1 | 1 |
| 290873 | — | — | — | 2026-05-01 | 4 | 1 |
| 290874 | — | — | — | 2026-05-01 | 0 | 1 |
| 290877 | — | — | — | 2026-04-01 | 1 | 1 |
| 290877 | — | — | — | 2026-06-01 | 1 | 1 |
| 290882 | — | — | — | 2026-04-01 | 1 | 1 |
| 290882 | — | — | — | 2026-05-01 | 2 | 2 |
| 290882 | — | — | — | 2026-06-01 | 2 | 1 |
| 290886 | — | — | — | 2026-01-01 | 2 | 1 |
| 290887 | — | — | — | 2026-01-01 | 2 | 1 |
| 290887 | — | — | — | 2026-03-01 | 7 | 2 |
| 290887 | — | — | — | 2026-04-01 | 2 | 1 |
| 290887 | — | — | — | 2026-05-01 | 2 | 2 |
| 290888 | — | — | — | 2026-04-01 | 1 | 1 |
| 290888 | — | — | — | 2026-05-01 | 1 | 1 |
| 290889 | — | — | — | 2026-02-01 | 1 | 1 |
| 290889 | — | — | — | 2026-04-01 | 6 | 6 |
| 290890 | 0084 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 4 | 3 |
| 290890 | 0084 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 2 | 1 |
| 290890 | 0084 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 3 | 2 |
| 290904 | — | — | — | 2026-02-01 | 5 | 2 |
| 290960 | — | — | — | 2026-04-01 | 1 | 1 |
| 290961 | — | — | — | 2026-02-01 | 1 | 1 |
| 290961 | — | — | — | 2026-03-01 | 1 | 1 |
| 290961 | — | — | — | 2026-04-01 | 4 | 2 |
| 290961 | — | — | — | 2026-05-01 | 1 | 1 |
| 291051 | — | — | — | 2026-01-01 | 5 | 3 |
| 291051 | — | — | — | 2026-02-01 | 2 | 2 |
| 291051 | — | — | — | 2026-05-01 | 1 | 1 |
| 291151 | — | — | — | 2026-03-01 | 2 | 1 |
| 291170 | — | — | — | 2026-05-01 | 1 | 1 |
| 291185 | — | — | — | 2026-01-01 | 1 | 1 |
| 291229 | — | — | — | 2026-03-01 | 4 | 1 |
| 291229 | — | — | — | 2026-05-01 | 1 | 1 |
| 291230 | — | — | — | 2026-01-01 | 1 | 1 |
| 291230 | — | — | — | 2026-02-01 | 3 | 1 |
| 291230 | — | — | — | 2026-04-01 | 3 | 3 |
| 291230 | — | — | — | 2026-06-01 | 1 | 1 |
| 291242 | — | — | — | 2026-03-01 | 3 | 3 |
| 291335 | — | — | — | 2026-01-01 | 1 | 1 |
| 291335 | — | — | — | 2026-03-01 | 1 | 1 |
| 291335 | — | — | — | 2026-04-01 | 1 | 1 |
| 291350 | — | — | — | 2026-01-01 | 1 | 1 |
| 291350 | — | — | — | 2026-03-01 | 1 | 1 |
| 291350 | — | — | — | 2026-04-01 | 2 | 2 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2025-12-01 | 1 | 1 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2026-01-01 | 5 | 5 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2026-02-01 | 1 | 1 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2026-03-01 | 3 | 3 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2026-04-01 | 3 | 3 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2026-05-01 | 3 | 2 |
| 291352 | 0048 1pc Replacement Glass | GLASS | COL154 | 2026-06-01 | 2 | 2 |
| 291607 | — | — | — | 2025-12-01 | 1 | 1 |
| 291650 | — | — | — | 2026-02-01 | 1 | 1 |
| 291652 | — | — | — | 2026-01-01 | 1 | 1 |
| 291652 | — | — | — | 2026-02-01 | 1 | 1 |
| 291652 | — | — | — | 2026-03-01 | 1 | 1 |
| 291652 | — | — | — | 2026-04-01 | 4 | 3 |
| 291660 | — | — | — | 2026-02-01 | 2 | 2 |
| 291870 | — | — | — | 2026-04-01 | 2 | 2 |
| 291870 | — | — | — | 2026-05-01 | 1 | 1 |
| 292021 | — | — | — | 2026-01-01 | 1 | 1 |
| 292021 | — | — | — | 2026-03-01 | 1 | 1 |
| 292021 | — | — | — | 2026-06-01 | 1 | 1 |
| 292058 | — | — | — | 2025-12-01 | 3 | 3 |
| 292058 | — | — | — | 2026-01-01 | 1 | 1 |
| 292058 | — | — | — | 2026-02-01 | 1 | 1 |
| 292058 | — | — | — | 2026-03-01 | 2 | 2 |
| 292058 | — | — | — | 2026-04-01 | 5 | 5 |
| 292058 | — | — | — | 2026-05-01 | 1 | 1 |
| 292208 | — | — | — | 2026-03-01 | 1 | 1 |
| 292208 | — | — | — | 2026-04-01 | 2 | 2 |
| 292208 | — | — | — | 2026-06-01 | 1 | 1 |
| 292450 | — | — | — | 2026-02-01 | 2 | 2 |
| 292451 | — | — | — | 2025-12-01 | 1 | 1 |
| 292451 | — | — | — | 2026-01-01 | 3 | 3 |
| 292451 | — | — | — | 2026-03-01 | 3 | 3 |
| 292451 | — | — | — | 2026-04-01 | 1 | 1 |
| 292451 | — | — | — | 2026-05-01 | 4 | 4 |
| 292451 | — | — | — | 2026-06-01 | 1 | 1 |
| 293011 | — | — | — | 2026-02-01 | 1 | 1 |
| 293011 | — | — | — | 2026-05-01 | 1 | 1 |
| 293059 | — | — | — | 2026-01-01 | 1 | 1 |
| 293059 | — | — | — | 2026-04-01 | 2 | 2 |
| 293813 | — | — | — | 2026-01-01 | 1 | 1 |
| 294074 | — | — | — | 2026-02-01 | 1 | 1 |
| 294074 | — | — | — | 2026-03-01 | 2 | 2 |
| 294074 | — | — | — | 2026-06-01 | 1 | 1 |
| 294091 | — | — | — | 2026-02-01 | 2 | 1 |
| 294099 | — | — | — | 2026-02-01 | 4 | 2 |
| 294099 | — | — | — | 2026-03-01 | 2 | 2 |
| 294099 | — | — | — | 2026-05-01 | 4 | 3 |
| 294107 | — | — | — | 2026-01-01 | 1 | 1 |
| 294107 | — | — | — | 2026-03-01 | 19 | 3 |
| 294113 | — | — | — | 2026-01-01 | 6 | 1 |
| 294113 | — | — | — | 2026-05-01 | 2 | 1 |
| 294124 | — | — | — | 2025-12-01 | 3 | 1 |
| 294124 | — | — | — | 2026-01-01 | 1 | 1 |
| 294124 | — | — | — | 2026-02-01 | 5 | 3 |
| 294124 | — | — | — | 2026-03-01 | 5 | 3 |
| 294124 | — | — | — | 2026-04-01 | 7 | 4 |
| 294124 | — | — | — | 2026-06-01 | 4 | 1 |
| 294175 | — | — | — | 2026-01-01 | 1 | 1 |
| 294175 | — | — | — | 2026-03-01 | 3 | 1 |
| 294175 | — | — | — | 2026-06-01 | 1 | 1 |
| 29417L | — | — | — | 2026-05-01 | 1 | 1 |
| 29417R | — | — | — | 2026-01-01 | 1 | 1 |
| 29417R | — | — | — | 2026-02-01 | 2 | 1 |
| 29417R | — | — | — | 2026-04-01 | 1 | 1 |
| 294222 | — | — | — | 2026-05-01 | 1 | 1 |
| 294223 | — | — | — | 2026-02-01 | 1 | 1 |
| 294223 | — | — | — | 2026-04-01 | 1 | 1 |
| 294223 | — | — | — | 2026-05-01 | 1 | 1 |
| 294223 | — | — | — | 2026-06-01 | 4 | 1 |
| 294336 | — | — | — | 2026-06-01 | 1 | 1 |
| 294357 | — | — | — | 2026-02-01 | 1 | 1 |
| 294357 | — | — | — | 2026-06-01 | 1 | 1 |
| 294364 | — | — | — | 2026-04-01 | 1 | 1 |
| 294663 | — | — | — | 2026-03-01 | 3 | 1 |
| 294663 | — | — | — | 2026-04-01 | 1 | 1 |
| 294673 | — | — | — | 2026-05-01 | 2 | 1 |
| 296103 | — | — | — | 2026-03-01 | 4 | 2 |
| 296103 | — | — | — | 2026-04-01 | 1 | 1 |
| 296123 | — | — | — | 2026-05-01 | 1 | 1 |
| 298520 | — | — | — | 2026-04-01 | 4 | 1 |
| 299121 | — | — | — | 2026-03-01 | 1 | 1 |
| 299121 | — | — | — | 2026-05-01 | 2 | 1 |
| 299751 | — | — | — | 2026-01-01 | 5 | 2 |
| 299751 | — | — | — | 2026-02-01 | 3 | 3 |
| 299751 | — | — | — | 2026-03-01 | 2 | 1 |
| 299751 | — | — | — | 2026-05-01 | 4 | 3 |
| 29A380 | — | — | — | 2025-12-01 | 2 | 2 |
| 29A380 | — | — | — | 2026-01-01 | 3 | 3 |
| 29A380 | — | — | — | 2026-02-01 | 2 | 3 |
| 29A380 | — | — | — | 2026-03-01 | 3 | 2 |
| 29A380 | — | — | — | 2026-04-01 | 3 | 3 |
| 29A380 | — | — | — | 2026-05-01 | 7 | 5 |
| 29A380 | — | — | — | 2026-06-01 | 2 | 2 |
| 29B280 | — | — | — | 2026-05-01 | 2 | 1 |
| 29B382 | — | — | — | 2026-02-01 | 1 | 1 |
| 29B382 | — | — | — | 2026-03-01 | 1 | 1 |
| 29B382 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R023 | — | — | — | 2026-01-01 | 7 | 4 |
| 29R023 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R023 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R035 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R035 | — | — | — | 2026-03-01 | 2 | 2 |
| 29R035 | — | — | — | 2026-04-01 | 5 | 2 |
| 29R070 | — | — | — | 2026-01-01 | 3 | 3 |
| 29R070 | — | — | — | 2026-02-01 | 2 | 2 |
| 29R070 | — | — | — | 2026-03-01 | 2 | 1 |
| 29R070 | — | — | — | 2026-04-01 | 5 | 2 |
| 29R080 | — | — | — | 2025-12-01 | 1 | 1 |
| 29R080 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R081 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R081 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R083 | — | — | — | 2026-01-01 | 6 | 1 |
| 29R084 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R084 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R084 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R086 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R095 | — | — | — | 2025-12-01 | 1 | 1 |
| 29R101 | — | — | — | 2026-01-01 | 4 | 3 |
| 29R101 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R101 | — | — | — | 2026-03-01 | 2 | 2 |
| 29R101 | — | — | — | 2026-04-01 | 3 | 3 |
| 29R101 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R101 | — | — | — | 2026-06-01 | 2 | 1 |
| 29R106 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R107 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R113 | — | — | — | 2026-01-01 | 3 | 2 |
| 29R113 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R113 | — | — | — | 2026-03-01 | 2 | 2 |
| 29R113 | — | — | — | 2026-04-01 | 3 | 2 |
| 29R113 | — | — | — | 2026-06-01 | 1 | 1 |
| 29R115 | — | — | — | 2026-06-01 | 1 | 1 |
| 29R116 | — | — | — | 2025-12-01 | 1 | 1 |
| 29R116 | — | — | — | 2026-06-01 | 6 | 1 |
| 29R120 | — | — | — | 2026-01-01 | 1 | 1 |
| 29R122 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R122 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R126 | — | — | — | 2026-01-01 | 2 | 2 |
| 29R134 | — | — | — | 2026-03-01 | 2 | 1 |
| 29R134 | — | — | — | 2026-05-01 | 2 | 1 |
| 29R135 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R135 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R136 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R136 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R148 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R149 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R150 | — | — | — | 2026-01-01 | 1 | 1 |
| 29R152 | — | — | — | 2026-03-01 | 1 | 1 |
| 29R153 | — | — | — | 2026-01-01 | 1 | 1 |
| 29R153 | — | — | — | 2026-04-01 | 1 | 1 |
| 29R153 | — | — | — | 2026-05-01 | 1 | 1 |
| 29R160 | — | — | — | 2026-06-01 | 1 | 1 |
| 29R163 | — | — | — | 2026-06-01 | 3 | 1 |
| 29R164 | — | — | — | 2026-03-01 | 1 | 1 |
| 29R164 | — | — | — | 2026-06-01 | 3 | 1 |
| 29R170 | — | — | — | 2025-12-01 | 1 | 1 |
| 29R170 | — | — | — | 2026-01-01 | 2 | 2 |
| 29R170 | — | — | — | 2026-02-01 | 1 | 1 |
| 29R170 | — | — | — | 2026-04-01 | 2 | 2 |
| 29R170 | — | — | — | 2026-06-01 | 1 | 1 |
| 29R171 | — | — | — | 2025-12-01 | 2 | 2 |
| 29R175 | — | — | — | 2026-01-01 | 1 | 1 |
| 29R175 | — | — | — | 2026-03-01 | 1 | 1 |
| 29R179 | — | — | — | 2026-03-01 | 1 | 1 |
| 29R179 | — | — | — | 2026-06-01 | 1 | 1 |
| 29R180 | — | — | — | 2026-03-01 | 1 | 1 |
| 29R471 | — | — | — | 2026-06-01 | 1 | 1 |
| 29R474 | — | — | — | 2026-01-01 | 1 | 1 |
| 29R475 | — | — | — | 2026-05-01 | 12 | 1 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2025-12-01 | 1 | 1 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2026-01-01 | 4 | 2 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2026-02-01 | 9 | 4 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2026-03-01 | 10 | 6 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2026-04-01 | 16 | 5 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2026-05-01 | 35 | 8 |
| 302021 | Cela Medium Outdoor Sconce | CAT6 | CELA | 2026-06-01 | 16 | 3 |
| 302023 | Cela Large Outdoor Sconce | CAT6 | CELA | 2026-01-01 | 1 | 1 |
| 302023 | Cela Large Outdoor Sconce | CAT6 | CELA | 2026-02-01 | 13 | 3 |
| 302023 | Cela Large Outdoor Sconce | CAT6 | CELA | 2026-03-01 | 20 | 6 |
| 302023 | Cela Large Outdoor Sconce | CAT6 | CELA | 2026-04-01 | 14 | 5 |
| 302023 | Cela Large Outdoor Sconce | CAT6 | CELA | 2026-05-01 | 3 | 2 |
| 302023 | Cela Large Outdoor Sconce | CAT6 | CELA | 2026-06-01 | 2 | 1 |
| 302024 | Linea Small Outdoor Sconce | CAT6 | LINEA | 2026-01-01 | 8 | 6 |
| 302024 | Linea Small Outdoor Sconce | CAT6 | LINEA | 2026-02-01 | 4 | 4 |
| 302024 | Linea Small Outdoor Sconce | CAT6 | LINEA | 2026-03-01 | 9 | 4 |
| 302024 | Linea Small Outdoor Sconce | CAT6 | LINEA | 2026-04-01 | 5 | 2 |
| 302024 | Linea Small Outdoor Sconce | CAT6 | LINEA | 2026-05-01 | 4 | 4 |
| 302025 | Linea Medium Outdoor Sconce | CAT6 | LINEA | 2026-01-01 | 4 | 3 |
| 302025 | Linea Medium Outdoor Sconce | CAT6 | LINEA | 2026-02-01 | 5 | 4 |
| 302025 | Linea Medium Outdoor Sconce | CAT6 | LINEA | 2026-03-01 | 14 | 4 |
| 302025 | Linea Medium Outdoor Sconce | CAT6 | LINEA | 2026-04-01 | 2 | 1 |
| 302025 | Linea Medium Outdoor Sconce | CAT6 | LINEA | 2026-05-01 | 4 | 3 |
| 302026 | Linea Large Outdoor Sconce | CAT6 | LINEA | 2026-03-01 | 26 | 2 |
| 302026 | Linea Large Outdoor Sconce | CAT6 | LINEA | 2026-04-01 | 2 | 1 |
| 302026 | Linea Large Outdoor Sconce | CAT6 | LINEA | 2026-05-01 | 3 | 2 |
| 302030 | Triomphe Small Outdoor Sconce | CAT6 | COL83 | 2025-12-01 | 8 | 1 |
| 302030 | Triomphe Small Outdoor Sconce | CAT6 | COL83 | 2026-01-01 | 13 | 6 |
| 302030 | Triomphe Small Outdoor Sconce | CAT6 | COL83 | 2026-02-01 | 1 | 1 |
| 302030 | Triomphe Small Outdoor Sconce | CAT6 | COL83 | 2026-03-01 | 11 | 5 |
| 302030 | Triomphe Small Outdoor Sconce | CAT6 | COL83 | 2026-04-01 | 31 | 3 |
| 302030 | Triomphe Small Outdoor Sconce | CAT6 | COL83 | 2026-05-01 | 3 | 2 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2025-12-01 | 14 | 1 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2026-01-01 | 23 | 3 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2026-02-01 | 9 | 4 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2026-03-01 | 16 | 2 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2026-04-01 | 10 | 2 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2026-05-01 | 8 | 3 |
| 302031 | Triomphe Medium Outdoor Sconce | CAT6 | COL83 | 2026-06-01 | 3 | 2 |
| 302032 | Triomphe Large Outdoor Sconce | CAT6 | COL83 | 2026-02-01 | 2 | 1 |
| 302032 | Triomphe Large Outdoor Sconce | CAT6 | COL83 | 2026-03-01 | 3 | 3 |
| 302032 | Triomphe Large Outdoor Sconce | CAT6 | COL83 | 2026-04-01 | 11 | 4 |
| 302032 | Triomphe Large Outdoor Sconce | CAT6 | COL83 | 2026-05-01 | 6 | 2 |
| 302032 | Triomphe Large Outdoor Sconce | CAT6 | COL83 | 2026-06-01 | 6 | 2 |
| 302034 | Element Small Outdoor Sconce | CAT6 | COL126 | 2025-12-01 | 10 | 1 |
| 302034 | Element Small Outdoor Sconce | CAT6 | COL126 | 2026-02-01 | 8 | 1 |
| 302034 | Element Small Outdoor Sconce | CAT6 | COL126 | 2026-03-01 | 7 | 3 |
| 302034 | Element Small Outdoor Sconce | CAT6 | COL126 | 2026-05-01 | 4 | 2 |
| 302034 | Element Small Outdoor Sconce | CAT6 | COL126 | 2026-06-01 | 1 | 1 |
| 302035 | Element Medium Outdoor Sconce | CAT6 | COL126 | 2025-12-01 | 4 | 1 |
| 302035 | Element Medium Outdoor Sconce | CAT6 | COL126 | 2026-01-01 | 2 | 2 |
| 302035 | Element Medium Outdoor Sconce | CAT6 | COL126 | 2026-02-01 | 4 | 3 |
| 302035 | Element Medium Outdoor Sconce | CAT6 | COL126 | 2026-03-01 | 0 | 1 |
| 302035 | Element Medium Outdoor Sconce | CAT6 | COL126 | 2026-04-01 | 11 | 3 |
| 302035 | Element Medium Outdoor Sconce | CAT6 | COL126 | 2026-05-01 | 7 | 3 |
| 302036 | Element Large Outdoor Sconce | CAT6 | COL126 | 2026-01-01 | 2 | 1 |
| 302036 | Element Large Outdoor Sconce | CAT6 | COL126 | 2026-03-01 | 9 | 1 |
| 302036 | Element Large Outdoor Sconce | CAT6 | COL126 | 2026-04-01 | 2 | 1 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2025-12-01 | 2 | 1 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2026-01-01 | 1 | 1 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2026-02-01 | 5 | 3 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2026-03-01 | 22 | 5 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2026-04-01 | 22 | 4 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2026-05-01 | 5 | 2 |
| 302038 | Revere Small Outdoor Sconce | CAT6 | COL134 | 2026-06-01 | 13 | 4 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2025-12-01 | 11 | 1 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2026-01-01 | 6 | 3 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2026-02-01 | 4 | 3 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2026-03-01 | 9 | 2 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2026-04-01 | 16 | 5 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2026-05-01 | 6 | 2 |
| 302039 | Revere Medium Outdoor Sconce | CAT6 | COL134 | 2026-06-01 | 23 | 1 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2025-12-01 | 4 | 1 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2026-01-01 | 10 | 2 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2026-02-01 | 6 | 3 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2026-03-01 | 11 | 4 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2026-04-01 | 2 | 2 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2026-05-01 | 4 | 2 |
| 302040 | Revere Large Outdoor Sconce | CAT6 | COL134 | 2026-06-01 | 5 | 3 |
| 302042 | Carbon Small Outdoor Sconce | CAT6 | COL135 | 2025-12-01 | 9 | 2 |
| 302042 | Carbon Small Outdoor Sconce | CAT6 | COL135 | 2026-02-01 | 5 | 3 |
| 302042 | Carbon Small Outdoor Sconce | CAT6 | COL135 | 2026-03-01 | 12 | 6 |
| 302042 | Carbon Small Outdoor Sconce | CAT6 | COL135 | 2026-04-01 | 10 | 5 |
| 302042 | Carbon Small Outdoor Sconce | CAT6 | COL135 | 2026-05-01 | 12 | 4 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2025-12-01 | 2 | 1 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2026-01-01 | 2 | 1 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2026-02-01 | 7 | 5 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2026-03-01 | 14 | 4 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2026-04-01 | 19 | 2 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2026-05-01 | 9 | 2 |
| 302043 | Carbon Medium Outdoor Sconce | CAT6 | COL135 | 2026-06-01 | 4 | 2 |
| 302044 | Carbon Large Outdoor Sconce | CAT6 | COL135 | 2025-12-01 | 2 | 1 |
| 302044 | Carbon Large Outdoor Sconce | CAT6 | COL135 | 2026-01-01 | 6 | 4 |
| 302044 | Carbon Large Outdoor Sconce | CAT6 | COL135 | 2026-02-01 | 10 | 5 |
| 302044 | Carbon Large Outdoor Sconce | CAT6 | COL135 | 2026-03-01 | 17 | 5 |
| 302044 | Carbon Large Outdoor Sconce | CAT6 | COL135 | 2026-04-01 | 1 | 1 |
| 302044 | Carbon Large Outdoor Sconce | CAT6 | COL135 | 2026-05-01 | 11 | 4 |
| 302045 | Summit Small Outdoor Sconce | CAT6 | COL44 | 2026-02-01 | 4 | 1 |
| 302046 | Summit Medium Outdoor Sconce | CAT6 | COL44 | 2026-01-01 | 1 | 1 |
| 302046 | Summit Medium Outdoor Sconce | CAT6 | COL44 | 2026-02-01 | 2 | 1 |
| 302046 | Summit Medium Outdoor Sconce | CAT6 | COL44 | 2026-03-01 | 2 | 1 |
| 302046 | Summit Medium Outdoor Sconce | CAT6 | COL44 | 2026-04-01 | 4 | 3 |
| 302047 | Summit Large Outdoor Sconce | CAT6 | COL44 | 2025-12-01 | 2 | 1 |
| 302047 | Summit Large Outdoor Sconce | CAT6 | COL44 | 2026-01-01 | 1 | 1 |
| 302047 | Summit Large Outdoor Sconce | CAT6 | COL44 | 2026-04-01 | 3 | 1 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | ARC | 2026-01-01 | 5 | 5 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | ARC | 2026-02-01 | 8 | 2 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | ARC | 2026-03-01 | 1 | 1 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | ARC | 2026-04-01 | 2 | 1 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | ARC | 2026-05-01 | 6 | 4 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | ARC | 2026-06-01 | 3 | 1 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | ARC | 2026-01-01 | 5 | 2 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | ARC | 2026-02-01 | 1 | 1 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | ARC | 2026-03-01 | 13 | 7 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | ARC | 2026-04-01 | 9 | 5 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | ARC | 2026-05-01 | 10 | 6 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | ARC | 2026-06-01 | 2 | 1 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | ARC | 2026-01-01 | 3 | 3 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | ARC | 2026-02-01 | 3 | 3 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | ARC | 2026-03-01 | 4 | 1 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | ARC | 2026-04-01 | 5 | 2 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | ARC | 2026-05-01 | 6 | 4 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | ARC | 2026-06-01 | 3 | 2 |
| 302052 | Stowe Small Outdoor Sconce | CAT6 | STOWE | 2026-01-01 | 9 | 7 |
| 302052 | Stowe Small Outdoor Sconce | CAT6 | STOWE | 2026-02-01 | 19 | 7 |
| 302052 | Stowe Small Outdoor Sconce | CAT6 | STOWE | 2026-03-01 | 11 | 9 |
| 302052 | Stowe Small Outdoor Sconce | CAT6 | STOWE | 2026-04-01 | 20 | 6 |
| 302052 | Stowe Small Outdoor Sconce | CAT6 | STOWE | 2026-05-01 | 17 | 5 |
| 302052 | Stowe Small Outdoor Sconce | CAT6 | STOWE | 2026-06-01 | 4 | 1 |
| 302053 | Stowe Medium Outdoor Sconce | CAT6 | STOWE | 2026-01-01 | 4 | 4 |
| 302053 | Stowe Medium Outdoor Sconce | CAT6 | STOWE | 2026-02-01 | 8 | 5 |
| 302053 | Stowe Medium Outdoor Sconce | CAT6 | STOWE | 2026-03-01 | 8 | 5 |
| 302053 | Stowe Medium Outdoor Sconce | CAT6 | STOWE | 2026-04-01 | 6 | 4 |
| 302053 | Stowe Medium Outdoor Sconce | CAT6 | STOWE | 2026-05-01 | 5 | 3 |
| 302053 | Stowe Medium Outdoor Sconce | CAT6 | STOWE | 2026-06-01 | 14 | 2 |
| 302054 | Stowe Large Outdoor Sconce | CAT6 | STOWE | 2026-03-01 | 5 | 3 |
| 302054 | Stowe Large Outdoor Sconce | CAT6 | STOWE | 2026-04-01 | 1 | 1 |
| 302054 | Stowe Large Outdoor Sconce | CAT6 | STOWE | 2026-06-01 | 4 | 1 |
| 302501 | Ursa Small LED Outdoor Sconce | CAT6 | URSA | 2025-12-01 | 3 | 1 |
| 302501 | Ursa Small LED Outdoor Sconce | CAT6 | URSA | 2026-01-01 | 3 | 1 |
| 302501 | Ursa Small LED Outdoor Sconce | CAT6 | URSA | 2026-02-01 | 7 | 3 |
| 302501 | Ursa Small LED Outdoor Sconce | CAT6 | URSA | 2026-03-01 | 2 | 2 |
| 302501 | Ursa Small LED Outdoor Sconce | CAT6 | URSA | 2026-04-01 | 13 | 3 |
| 302501 | Ursa Small LED Outdoor Sconce | CAT6 | URSA | 2026-05-01 | 8 | 2 |
| 302503 | Ursa Large LED Outdoor Sconce | CAT6 | URSA | 2026-01-01 | 18 | 3 |
| 302503 | Ursa Large LED Outdoor Sconce | CAT6 | URSA | 2026-03-01 | 13 | 6 |
| 302503 | Ursa Large LED Outdoor Sconce | CAT6 | URSA | 2026-04-01 | 21 | 3 |
| 302503 | Ursa Large LED Outdoor Sconce | CAT6 | URSA | 2026-05-01 | 5 | 3 |
| 302507 | Double-Large Ursa LED Outdoor Sconce | CAT6 | URSA | 2026-03-01 | 1 | 1 |
| 302507 | Double-Large Ursa LED Outdoor Sconce | CAT6 | URSA | 2026-04-01 | 4 | 3 |
| 302507 | Double-Large Ursa LED Outdoor Sconce | CAT6 | URSA | 2026-05-01 | 1 | 1 |
| 302507 | Double-Large Ursa LED Outdoor Sconce | CAT6 | URSA | 2026-06-01 | 1 | 1 |
| 302512 | — | — | — | 2026-03-01 | 2 | 1 |
| 302515 | Shard Small LED Outdoor Sconce | CAT6 | SHARD | 2026-01-01 | 1 | 1 |
| 302515 | Shard Small LED Outdoor Sconce | CAT6 | SHARD | 2026-02-01 | 2 | 1 |
| 302515 | Shard Small LED Outdoor Sconce | CAT6 | SHARD | 2026-03-01 | 4 | 2 |
| 302515 | Shard Small LED Outdoor Sconce | CAT6 | SHARD | 2026-04-01 | 3 | 1 |
| 302517 | Shard Large LED Outdoor Sconce | CAT6 | SHARD | 2025-12-01 | 2 | 1 |
| 302517 | Shard Large LED Outdoor Sconce | CAT6 | SHARD | 2026-01-01 | 5 | 3 |
| 302517 | Shard Large LED Outdoor Sconce | CAT6 | SHARD | 2026-02-01 | 10 | 3 |
| 302517 | Shard Large LED Outdoor Sconce | CAT6 | SHARD | 2026-03-01 | 12 | 3 |
| 302517 | Shard Large LED Outdoor Sconce | CAT6 | SHARD | 2026-04-01 | 4 | 2 |
| 302517 | Shard Large LED Outdoor Sconce | CAT6 | SHARD | 2026-05-01 | 5 | 2 |
| 302518 | Shard XL Outdoor Sconce | CAT6 | SHARD | 2026-02-01 | 2 | 1 |
| 302518 | Shard XL Outdoor Sconce | CAT6 | SHARD | 2026-04-01 | 1 | 1 |
| 302518 | Shard XL Outdoor Sconce | CAT6 | SHARD | 2026-05-01 | 1 | 1 |
| 302520 | Collage Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL119 | 2026-02-01 | 1 | 1 |
| 302523 | Collage Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL119 | 2026-01-01 | 2 | 1 |
| 302523 | Collage Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL119 | 2026-02-01 | 3 | 1 |
| 302523 | Collage Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL119 | 2026-03-01 | 1 | 1 |
| 302523 | Collage Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL119 | 2026-04-01 | 2 | 1 |
| 302523 | Collage Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL119 | 2026-05-01 | 3 | 2 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2025-12-01 | 2 | 2 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-01-01 | 2 | 1 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-02-01 | 4 | 1 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-03-01 | 2 | 1 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-04-01 | 7 | 3 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-05-01 | 4 | 1 |
| 302527 | Tress Small Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-06-01 | 1 | 1 |
| 302529 | Tress Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2025-12-01 | 2 | 1 |
| 302529 | Tress Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-01-01 | 8 | 4 |
| 302529 | Tress Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-03-01 | 1 | 1 |
| 302529 | Tress Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-04-01 | 19 | 3 |
| 302529 | Tress Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | TRESS | 2026-06-01 | 1 | 1 |
| 302531 | Rainfall LED Outdoor Sconce | CAT6 | COL120 | 2025-12-01 | 2 | 1 |
| 302531 | Rainfall LED Outdoor Sconce | CAT6 | COL120 | 2026-01-01 | 10 | 2 |
| 302531 | Rainfall LED Outdoor Sconce | CAT6 | COL120 | 2026-03-01 | 5 | 2 |
| 302531 | Rainfall LED Outdoor Sconce | CAT6 | COL120 | 2026-06-01 | 3 | 2 |
| 302533 | Rainfall Large LED Outdoor Sconce | CAT6 | COL120 | 2025-12-01 | 6 | 2 |
| 302533 | Rainfall Large LED Outdoor Sconce | CAT6 | COL120 | 2026-01-01 | 9 | 1 |
| 302533 | Rainfall Large LED Outdoor Sconce | CAT6 | COL120 | 2026-02-01 | 3 | 2 |
| 302533 | Rainfall Large LED Outdoor Sconce | CAT6 | COL120 | 2026-04-01 | 1 | 1 |
| 302533 | Rainfall Large LED Outdoor Sconce | CAT6 | COL120 | 2026-05-01 | 6 | 4 |
| 302533 | Rainfall Large LED Outdoor Sconce | CAT6 | COL120 | 2026-06-01 | 2 | 1 |
| 302551 | Fairwinds Outdoor Sconce | CAT6 | COL121 | 2025-12-01 | 8 | 4 |
| 302551 | Fairwinds Outdoor Sconce | CAT6 | COL121 | 2026-02-01 | 12 | 2 |
| 302551 | Fairwinds Outdoor Sconce | CAT6 | COL121 | 2026-06-01 | 4 | 2 |
| 302553 | Fairwinds Large Outdoor Sconce | CAT6 | COL121 | 2026-02-01 | 4 | 1 |
| 302553 | Fairwinds Large Outdoor Sconce | CAT6 | COL121 | 2026-05-01 | 1 | 1 |
| 302553 | Fairwinds Large Outdoor Sconce | CAT6 | COL121 | 2026-06-01 | 5 | 2 |
| 302555 | Alcove Small Outdoor Sconce | CAT6 | COL112 | 2026-01-01 | 5 | 4 |
| 302555 | Alcove Small Outdoor Sconce | CAT6 | COL112 | 2026-02-01 | 6 | 4 |
| 302555 | Alcove Small Outdoor Sconce | CAT6 | COL112 | 2026-03-01 | 3 | 2 |
| 302555 | Alcove Small Outdoor Sconce | CAT6 | COL112 | 2026-04-01 | 2 | 2 |
| 302555 | Alcove Small Outdoor Sconce | CAT6 | COL112 | 2026-05-01 | 2 | 1 |
| 302555 | Alcove Small Outdoor Sconce | CAT6 | COL112 | 2026-06-01 | 3 | 2 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2025-12-01 | 2 | 1 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2026-01-01 | 14 | 2 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2026-02-01 | 1 | 1 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2026-03-01 | 9 | 4 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2026-04-01 | 12 | 3 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2026-05-01 | 20 | 3 |
| 302556 | Alcove Medium Outdoor Sconce | CAT6 | COL112 | 2026-06-01 | 4 | 1 |
| 302557 | Alcove Large Outdoor Sconce | CAT6 | COL112 | 2026-01-01 | 9 | 5 |
| 302557 | Alcove Large Outdoor Sconce | CAT6 | COL112 | 2026-02-01 | 22 | 2 |
| 302557 | Alcove Large Outdoor Sconce | CAT6 | COL112 | 2026-03-01 | 17 | 2 |
| 302557 | Alcove Large Outdoor Sconce | CAT6 | COL112 | 2026-04-01 | 10 | 2 |
| 302557 | Alcove Large Outdoor Sconce | CAT6 | COL112 | 2026-05-01 | 5 | 2 |
| 302557 | Alcove Large Outdoor Sconce | CAT6 | COL112 | 2026-06-01 | 5 | 2 |
| 302560 | Edge Medium LED Outdoor Sconce | CAT6 | EDGE | 2026-01-01 | 6 | 1 |
| 302560 | Edge Medium LED Outdoor Sconce | CAT6 | EDGE | 2026-02-01 | 9 | 2 |
| 302560 | Edge Medium LED Outdoor Sconce | CAT6 | EDGE | 2026-04-01 | 12 | 2 |
| 302560 | Edge Medium LED Outdoor Sconce | CAT6 | EDGE | 2026-06-01 | 1 | 1 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2025-12-01 | 6 | 2 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2026-01-01 | 5 | 2 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2026-02-01 | 36 | 2 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2026-03-01 | 3 | 3 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2026-04-01 | 3 | 3 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2026-05-01 | 3 | 2 |
| 302563 | Edge Large LED Outdoor Sconce | CAT6 | EDGE | 2026-06-01 | 9 | 3 |
| 302581 | Tura Medium Outdoor Sconce | CAT6 | TURA | 2026-02-01 | 2 | 1 |
| 302583 | Tura Large Outdoor Sconce | CAT6 | TURA | 2026-03-01 | 1 | 1 |
| 302583 | Tura Large Outdoor Sconce | CAT6 | TURA | 2026-04-01 | 18 | 1 |
| 302600 | Shadow Box Small w/Slate Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 1 | 1 |
| 302600 | Shadow Box Small w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 5 | 1 |
| 302600 | Shadow Box Small w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 1 | 1 |
| 302601 | Shadow Box Small Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 3 | 2 |
| 302601 | Shadow Box Small Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 11 | 3 |
| 302601 | Shadow Box Small Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 7 | 1 |
| 302601 | Shadow Box Small Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 3 | 2 |
| 302601 | Shadow Box Small Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 2 | 1 |
| 302601 | Shadow Box Small Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 2 | 1 |
| 302602 | Shadow Box Medium w/Slate Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 5 | 1 |
| 302602 | Shadow Box Medium w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 7 | 1 |
| 302602 | Shadow Box Medium w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 2 | 1 |
| 302602 | Shadow Box Medium w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 2 | 1 |
| 302602 | Shadow Box Medium w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 2 | 2 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 14 | 2 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 3 | 1 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 2 | 2 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 1 | 1 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 1 | 1 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 4 | 1 |
| 302603 | Shadow Box Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 1 | 1 |
| 302604 | Shadow Box Large w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 10 | 1 |
| 302604 | Shadow Box Large w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 8 | 5 |
| 302604 | Shadow Box Large w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 15 | 4 |
| 302604 | Shadow Box Large w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 10 | 3 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 7 | 4 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 19 | 9 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 23 | 6 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 46 | 14 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 21 | 12 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 15 | 3 |
| 302605 | Shadow Box Large Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 3 | 1 |
| 302606 | Shadow Box Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 1 | 1 |
| 302606 | Shadow Box Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 8 | 2 |
| 302606 | Shadow Box Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 5 | 3 |
| 302606 | Shadow Box Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 8 | 4 |
| 302606 | Shadow Box Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 8 | 2 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 24 | 5 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 14 | 4 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 11 | 2 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 13 | 3 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 6 | 4 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 12 | 3 |
| 302607 | Shadow Box Tall Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 5 | 2 |
| 302608 | Shadow Box Extra Tall Sconce | CAT6 | COL122 | 2026-01-01 | 14 | 2 |
| 302608 | Shadow Box Extra Tall Sconce | CAT6 | COL122 | 2026-02-01 | 3 | 2 |
| 302608 | Shadow Box Extra Tall Sconce | CAT6 | COL122 | 2026-03-01 | 4 | 2 |
| 302608 | Shadow Box Extra Tall Sconce | CAT6 | COL122 | 2026-04-01 | 6 | 2 |
| 302608 | Shadow Box Extra Tall Sconce | CAT6 | COL122 | 2026-06-01 | 2 | 1 |
| 302609 | Shadow Box Extra Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 2 | 3 |
| 302609 | Shadow Box Extra Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 8 | 3 |
| 302609 | Shadow Box Extra Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 4 | 2 |
| 302609 | Shadow Box Extra Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 1 | 1 |
| 302609 | Shadow Box Extra Tall w/Slate Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 2 | 1 |
| 302620 | Refraction Outdoor Sconce | CAT6 | COL123 | 2026-02-01 | 2 | 1 |
| 302623 | Refraction Large Outdoor Sconce | CAT6 | COL123 | 2026-01-01 | 0 | 1 |
| 302623 | Refraction Large Outdoor Sconce | CAT6 | COL123 | 2026-03-01 | 5 | 2 |
| 302623 | Refraction Large Outdoor Sconce | CAT6 | COL123 | 2026-04-01 | 5 | 1 |
| 302623 | Refraction Large Outdoor Sconce | CAT6 | COL123 | 2026-05-01 | 4 | 1 |
| 302630 | Stratum Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL124 | 2026-04-01 | 2 | 1 |
| 302632 | Stratum Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL124 | 2025-12-01 | 2 | 1 |
| 302632 | Stratum Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL124 | 2026-01-01 | 8 | 3 |
| 302632 | Stratum Large Dark Sky Friendly LED Outdoor Sconce | CAT6 | COL124 | 2026-02-01 | 3 | 1 |
| 302641 | — | — | — | 2026-04-01 | 3 | 1 |
| 302643 | — | — | — | 2026-04-01 | 1 | 1 |
| 302651 | Stellar Small Outdoor Sconce | CAT6 | COL125 | 2026-02-01 | 9 | 3 |
| 302651 | Stellar Small Outdoor Sconce | CAT6 | COL125 | 2026-03-01 | 3 | 1 |
| 302651 | Stellar Small Outdoor Sconce | CAT6 | COL125 | 2026-04-01 | 2 | 2 |
| 302652 | Stellar Large Outdoor Sconce | CAT6 | COL125 | 2026-02-01 | 2 | 1 |
| 302652 | Stellar Large Outdoor Sconce | CAT6 | COL125 | 2026-03-01 | 1 | 1 |
| 302652 | Stellar Large Outdoor Sconce | CAT6 | COL125 | 2026-05-01 | 1 | 1 |
| 302653 | Stellar Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL125 | 2026-02-01 | 5 | 3 |
| 302654 | Stellar Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL125 | 2026-01-01 | 2 | 1 |
| 302660 | Shadow Box Small w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-01-01 | 2 | 2 |
| 302660 | Shadow Box Small w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-03-01 | 2 | 1 |
| 302660 | Shadow Box Small w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-04-01 | 2 | 1 |
| 302661 | Shadow Box Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 4 | 2 |
| 302661 | Shadow Box Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 3 | 2 |
| 302661 | Shadow Box Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 2 | 1 |
| 302661 | Shadow Box Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 6 | 1 |
| 302662 | Shadow Box Medium w/Slate Dark Sky Friendly Out... | CAT6 | COL122 | 2026-03-01 | 7 | 3 |
| 302662 | Shadow Box Medium w/Slate Dark Sky Friendly Out... | CAT6 | COL122 | 2026-06-01 | 2 | 1 |
| 302663 | Shadow Box Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 6 | 1 |
| 302663 | Shadow Box Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 5 | 1 |
| 302663 | Shadow Box Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 11 | 2 |
| 302663 | Shadow Box Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 4 | 2 |
| 302663 | Shadow Box Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 2 | 1 |
| 302664 | Shadow Box Large w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-01-01 | 23 | 4 |
| 302664 | Shadow Box Large w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-02-01 | 8 | 1 |
| 302664 | Shadow Box Large w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-03-01 | 7 | 3 |
| 302664 | Shadow Box Large w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-04-01 | 4 | 1 |
| 302664 | Shadow Box Large w/Slate Dark Sky Friendly Outd... | CAT6 | COL122 | 2026-05-01 | 3 | 2 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 1 | 1 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 5 | 2 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 24 | 7 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 7 | 5 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 16 | 4 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-05-01 | 12 | 1 |
| 302665 | Shadow Box Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 5 | 1 |
| 302666 | Shadow Box Tall w/Slate Dark Sky Friendly Outdo... | CAT6 | COL122 | 2026-01-01 | 9 | 3 |
| 302666 | Shadow Box Tall w/Slate Dark Sky Friendly Outdo... | CAT6 | COL122 | 2026-02-01 | 1 | 1 |
| 302666 | Shadow Box Tall w/Slate Dark Sky Friendly Outdo... | CAT6 | COL122 | 2026-03-01 | 17 | 4 |
| 302666 | Shadow Box Tall w/Slate Dark Sky Friendly Outdo... | CAT6 | COL122 | 2026-04-01 | 10 | 3 |
| 302666 | Shadow Box Tall w/Slate Dark Sky Friendly Outdo... | CAT6 | COL122 | 2026-05-01 | 4 | 2 |
| 302667 | Shadow Box Tall Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2025-12-01 | 2 | 1 |
| 302667 | Shadow Box Tall Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-01-01 | 2 | 1 |
| 302667 | Shadow Box Tall Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-02-01 | 8 | 4 |
| 302667 | Shadow Box Tall Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-03-01 | 16 | 3 |
| 302667 | Shadow Box Tall Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-04-01 | 4 | 2 |
| 302667 | Shadow Box Tall Dark Sky Friendly Outdoor Sconce | CAT6 | COL122 | 2026-06-01 | 9 | 1 |
| 302668 | Shadow Box Extra Tall Dark Sky Friendly Outdoor... | CAT6 | COL122 | 2025-12-01 | 1 | 1 |
| 302668 | Shadow Box Extra Tall Dark Sky Friendly Outdoor... | CAT6 | COL122 | 2026-02-01 | 3 | 2 |
| 302668 | Shadow Box Extra Tall Dark Sky Friendly Outdoor... | CAT6 | COL122 | 2026-04-01 | 10 | 2 |
| 302668 | Shadow Box Extra Tall Dark Sky Friendly Outdoor... | CAT6 | COL122 | 2026-05-01 | 2 | 1 |
| 302669 | Shadow Box Extra Tall w/Slate Dark Sky Friendly... | CAT6 | COL122 | 2026-01-01 | 6 | 2 |
| 302669 | Shadow Box Extra Tall w/Slate Dark Sky Friendly... | CAT6 | COL122 | 2026-03-01 | 1 | 1 |
| 302709 | Henry Small Glass Shade Outdoor Sconce | CAT6 | HENRY | 2025-12-01 | 2 | 1 |
| 302709 | Henry Small Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-01-01 | 0 | 1 |
| 302709 | Henry Small Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-02-01 | 3 | 3 |
| 302709 | Henry Small Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-04-01 | 10 | 3 |
| 302709 | Henry Small Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-06-01 | 2 | 2 |
| 302710 | Henry Small Outdoor Sconce | CAT6 | HENRY | 2026-01-01 | 5 | 4 |
| 302710 | Henry Small Outdoor Sconce | CAT6 | HENRY | 2026-02-01 | 1 | 1 |
| 302710 | Henry Small Outdoor Sconce | CAT6 | HENRY | 2026-03-01 | 30 | 10 |
| 302710 | Henry Small Outdoor Sconce | CAT6 | HENRY | 2026-04-01 | 23 | 6 |
| 302710 | Henry Small Outdoor Sconce | CAT6 | HENRY | 2026-05-01 | 12 | 5 |
| 302710 | Henry Small Outdoor Sconce | CAT6 | HENRY | 2026-06-01 | 5 | 3 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2025-12-01 | 11 | 2 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-01-01 | 12 | 7 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-02-01 | 17 | 8 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-03-01 | 30 | 9 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-04-01 | 17 | 6 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-05-01 | 20 | 4 |
| 302711 | Henry Small Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-06-01 | 13 | 3 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2025-12-01 | 8 | 2 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2026-01-01 | 3 | 3 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2026-02-01 | 10 | 6 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2026-03-01 | 58 | 16 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2026-04-01 | 11 | 6 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2026-05-01 | 18 | 8 |
| 302712 | Henry Large Outdoor Sconce | CAT6 | HENRY | 2026-06-01 | 7 | 3 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2025-12-01 | 32 | 7 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-01-01 | 44 | 13 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-02-01 | 20 | 9 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-03-01 | 10 | 6 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-04-01 | 16 | 9 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-05-01 | 20 | 7 |
| 302713 | Henry Large Dark Sky Friendly Outdoor Sconce | CAT6 | HENRY | 2026-06-01 | 12 | 7 |
| 302714 | Henry Large Glass Shade Outdoor Sconce | CAT6 | HENRY | 2025-12-01 | 1 | 1 |
| 302714 | Henry Large Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-01-01 | 1 | 1 |
| 302714 | Henry Large Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-02-01 | 2 | 1 |
| 302714 | Henry Large Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-03-01 | 5 | 2 |
| 302714 | Henry Large Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-04-01 | 6 | 1 |
| 302714 | Henry Large Glass Shade Outdoor Sconce | CAT6 | HENRY | 2026-05-01 | 2 | 1 |
| 303001 | Mason Small Outdoor Sconce | CAT6 | MASON | 2025-12-01 | 6 | 3 |
| 303001 | Mason Small Outdoor Sconce | CAT6 | MASON | 2026-01-01 | 3 | 2 |
| 303001 | Mason Small Outdoor Sconce | CAT6 | MASON | 2026-02-01 | 13 | 7 |
| 303001 | Mason Small Outdoor Sconce | CAT6 | MASON | 2026-03-01 | 4 | 2 |
| 303001 | Mason Small Outdoor Sconce | CAT6 | MASON | 2026-04-01 | 3 | 2 |
| 303001 | Mason Small Outdoor Sconce | CAT6 | MASON | 2026-05-01 | 10 | 4 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2025-12-01 | 18 | 5 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2026-01-01 | 22 | 12 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2026-02-01 | 39 | 10 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2026-03-01 | 29 | 9 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2026-04-01 | 13 | 7 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2026-05-01 | 35 | 13 |
| 303003 | Mason Outdoor Sconce | CAT6 | MASON | 2026-06-01 | 7 | 2 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2025-12-01 | 10 | 4 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2026-01-01 | 40 | 12 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2026-02-01 | 24 | 9 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2026-03-01 | 20 | 6 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2026-04-01 | 17 | 8 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2026-05-01 | 30 | 11 |
| 303005 | Mason Large Outdoor Sconce | CAT6 | MASON | 2026-06-01 | 1 | 1 |
| 303080 | Cavo Large Outdoor Wall Sconce | CAT6 | CAVO | 2026-01-01 | 1 | 1 |
| 303080 | Cavo Large Outdoor Wall Sconce | CAT6 | CAVO | 2026-02-01 | 3 | 2 |
| 303080 | Cavo Large Outdoor Wall Sconce | CAT6 | CAVO | 2026-03-01 | 4 | 2 |
| 303080 | Cavo Large Outdoor Wall Sconce | CAT6 | CAVO | 2026-05-01 | 5 | 1 |
| 303080 | Cavo Large Outdoor Wall Sconce | CAT6 | CAVO | 2026-06-01 | 2 | 1 |
| 303090 | Flux Dark Sky Friendly Outdoor Sconce | CAT6 | FLUX | 2025-12-01 | 1 | 1 |
| 303090 | Flux Dark Sky Friendly Outdoor Sconce | CAT6 | FLUX | 2026-01-01 | 5 | 4 |
| 303090 | Flux Dark Sky Friendly Outdoor Sconce | CAT6 | FLUX | 2026-02-01 | 6 | 3 |
| 303090 | Flux Dark Sky Friendly Outdoor Sconce | CAT6 | FLUX | 2026-03-01 | 6 | 4 |
| 303090 | Flux Dark Sky Friendly Outdoor Sconce | CAT6 | FLUX | 2026-04-01 | 17 | 3 |
| 303090 | Flux Dark Sky Friendly Outdoor Sconce | CAT6 | FLUX | 2026-05-01 | 24 | 5 |
| 304210 | — | — | — | 2026-05-01 | 1 | 1 |
| 304215 | Sea Coast Outdoor Sconce | CAT6 | COL127 | 2025-12-01 | 2 | 1 |
| 304215 | Sea Coast Outdoor Sconce | CAT6 | COL127 | 2026-01-01 | 4 | 1 |
| 304215 | Sea Coast Outdoor Sconce | CAT6 | COL127 | 2026-03-01 | 9 | 2 |
| 304215 | Sea Coast Outdoor Sconce | CAT6 | COL127 | 2026-04-01 | 14 | 5 |
| 304220 | Sea Coast Large Outdoor Sconce | CAT6 | COL127 | 2025-12-01 | 8 | 1 |
| 304220 | Sea Coast Large Outdoor Sconce | CAT6 | COL127 | 2026-03-01 | 10 | 4 |
| 304220 | Sea Coast Large Outdoor Sconce | CAT6 | COL127 | 2026-04-01 | 5 | 1 |
| 304220 | Sea Coast Large Outdoor Sconce | CAT6 | COL127 | 2026-05-01 | 2 | 1 |
| 304303 | — | — | — | 2026-04-01 | 1 | 1 |
| 304320 | Portico Small Outdoor Sconce | CAT6 | COL128 | 2026-01-01 | 5 | 2 |
| 304320 | Portico Small Outdoor Sconce | CAT6 | COL128 | 2026-02-01 | 2 | 1 |
| 304320 | Portico Small Outdoor Sconce | CAT6 | COL128 | 2026-03-01 | 5 | 3 |
| 304320 | Portico Small Outdoor Sconce | CAT6 | COL128 | 2026-04-01 | 12 | 3 |
| 304320 | Portico Small Outdoor Sconce | CAT6 | COL128 | 2026-05-01 | 1 | 1 |
| 304325 | Portico Outdoor Sconce | CAT6 | COL128 | 2026-01-01 | 10 | 3 |
| 304325 | Portico Outdoor Sconce | CAT6 | COL128 | 2026-02-01 | 5 | 1 |
| 304325 | Portico Outdoor Sconce | CAT6 | COL128 | 2026-03-01 | 1 | 1 |
| 304325 | Portico Outdoor Sconce | CAT6 | COL128 | 2026-05-01 | 2 | 1 |
| 304330 | Portico Large Outdoor Sconce | CAT6 | COL128 | 2026-01-01 | 5 | 2 |
| 304330 | Portico Large Outdoor Sconce | CAT6 | COL128 | 2026-02-01 | 2 | 1 |
| 304330 | Portico Large Outdoor Sconce | CAT6 | COL128 | 2026-03-01 | 7 | 2 |
| 304330 | Portico Large Outdoor Sconce | CAT6 | COL128 | 2026-04-01 | 2 | 1 |
| 304815 | Beacon Hall Outdoor Sconce | CAT6 | COL31 | 2026-01-01 | 0 | 1 |
| 304815 | Beacon Hall Outdoor Sconce | CAT6 | COL31 | 2026-02-01 | 2 | 1 |
| 304815 | Beacon Hall Outdoor Sconce | CAT6 | COL31 | 2026-03-01 | 8 | 1 |
| 304815 | Beacon Hall Outdoor Sconce | CAT6 | COL31 | 2026-04-01 | 4 | 1 |
| 304815 | Beacon Hall Outdoor Sconce | CAT6 | COL31 | 2026-05-01 | 2 | 2 |
| 304820 | Beacon Hall Large Outdoor Sconce | CAT6 | COL31 | 2026-03-01 | 6 | 1 |
| 304840 | Kingston Outdoor Medium Sconce | CAT6 | COL129 | 2026-01-01 | 1 | 1 |
| 304840 | Kingston Outdoor Medium Sconce | CAT6 | COL129 | 2026-02-01 | 5 | 1 |
| 304840 | Kingston Outdoor Medium Sconce | CAT6 | COL129 | 2026-03-01 | 10 | 3 |
| 304840 | Kingston Outdoor Medium Sconce | CAT6 | COL129 | 2026-05-01 | 9 | 2 |
| 304842 | Kingston Outdoor Large Sconce | CAT6 | COL129 | 2026-01-01 | 2 | 1 |
| 304842 | Kingston Outdoor Large Sconce | CAT6 | COL129 | 2026-02-01 | 7 | 2 |
| 304842 | Kingston Outdoor Large Sconce | CAT6 | COL129 | 2026-04-01 | 11 | 2 |
| 304852 | Polaris Outdoor Medium Sconce | CAT6 | COL130 | 2025-12-01 | 2 | 1 |
| 304852 | Polaris Outdoor Medium Sconce | CAT6 | COL130 | 2026-01-01 | 4 | 1 |
| 304852 | Polaris Outdoor Medium Sconce | CAT6 | COL130 | 2026-05-01 | 17 | 3 |
| 304852 | Polaris Outdoor Medium Sconce | CAT6 | COL130 | 2026-06-01 | 2 | 1 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2025-12-01 | 4 | 1 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2026-01-01 | 16 | 1 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2026-02-01 | 8 | 3 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2026-03-01 | 8 | 2 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2026-04-01 | 7 | 2 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2026-05-01 | 5 | 2 |
| 304854 | Polaris Outdoor Large Sconce | CAT6 | COL130 | 2026-06-01 | 2 | 1 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2025-12-01 | 2 | 2 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-01-01 | 5 | 3 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-02-01 | 7 | 4 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-03-01 | 17 | 7 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-04-01 | 17 | 5 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-05-01 | 29 | 7 |
| 304901 | Twilight Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-06-01 | 12 | 4 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2025-12-01 | 13 | 3 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-01-01 | 43 | 6 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-02-01 | 46 | 16 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-03-01 | 35 | 12 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-04-01 | 23 | 8 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-05-01 | 12 | 7 |
| 304903 | Twilight Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-06-01 | 12 | 3 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2025-12-01 | 10 | 2 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-01-01 | 6 | 2 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-02-01 | 11 | 3 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-03-01 | 15 | 2 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-04-01 | 9 | 5 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-05-01 | 6 | 3 |
| 304905 | Twilight Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL19 | 2026-06-01 | 2 | 2 |
| 305201 | Dorset Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-01-01 | 12 | 5 |
| 305201 | Dorset Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-02-01 | 7 | 2 |
| 305201 | Dorset Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-03-01 | 1 | 1 |
| 305201 | Dorset Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-04-01 | 6 | 2 |
| 305201 | Dorset Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-05-01 | 37 | 4 |
| 305201 | Dorset Small Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-06-01 | 1 | 1 |
| 305202 | Dorset Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-01-01 | 5 | 3 |
| 305202 | Dorset Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-02-01 | 6 | 3 |
| 305202 | Dorset Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-03-01 | 14 | 3 |
| 305202 | Dorset Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-04-01 | 7 | 3 |
| 305202 | Dorset Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-05-01 | 21 | 4 |
| 305202 | Dorset Medium Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-06-01 | 2 | 1 |
| 305203 | Dorset Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-01-01 | 3 | 2 |
| 305203 | Dorset Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-03-01 | 2 | 1 |
| 305203 | Dorset Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-04-01 | 7 | 4 |
| 305203 | Dorset Large Dark Sky Friendly Outdoor Sconce | CAT6 | COL95 | 2026-05-01 | 2 | 1 |
| 305211 | Davis Small Outdoor Sconce | CAT6 | DAVIS | 2026-01-01 | 2 | 2 |
| 305211 | Davis Small Outdoor Sconce | CAT6 | DAVIS | 2026-02-01 | 9 | 5 |
| 305211 | Davis Small Outdoor Sconce | CAT6 | DAVIS | 2026-03-01 | 2 | 1 |
| 305211 | Davis Small Outdoor Sconce | CAT6 | DAVIS | 2026-04-01 | 7 | 3 |
| 305211 | Davis Small Outdoor Sconce | CAT6 | DAVIS | 2026-05-01 | 3 | 1 |
| 305211 | Davis Small Outdoor Sconce | CAT6 | DAVIS | 2026-06-01 | 1 | 1 |
| 305212 | Davis Medium Outdoor Sconce | CAT6 | DAVIS | 2026-01-01 | 1 | 1 |
| 305212 | Davis Medium Outdoor Sconce | CAT6 | DAVIS | 2026-02-01 | 4 | 3 |
| 305212 | Davis Medium Outdoor Sconce | CAT6 | DAVIS | 2026-03-01 | 1 | 1 |
| 305212 | Davis Medium Outdoor Sconce | CAT6 | DAVIS | 2026-04-01 | 8 | 3 |
| 305212 | Davis Medium Outdoor Sconce | CAT6 | DAVIS | 2026-05-01 | 2 | 1 |
| 305212 | Davis Medium Outdoor Sconce | CAT6 | DAVIS | 2026-06-01 | 2 | 1 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2025-12-01 | 1 | 1 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2026-01-01 | 2 | 1 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2026-02-01 | 3 | 2 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2026-03-01 | 4 | 1 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2026-04-01 | 2 | 1 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2026-05-01 | 2 | 1 |
| 305213 | Davis Large Outdoor Sconce | CAT6 | DAVIS | 2026-06-01 | 1 | 1 |
| 305605 | Meridian Small Outdoor Sconce | CAT6 | COL131 | 2026-01-01 | 2 | 1 |
| 305605 | Meridian Small Outdoor Sconce | CAT6 | COL131 | 2026-03-01 | 10 | 4 |
| 305605 | Meridian Small Outdoor Sconce | CAT6 | COL131 | 2026-05-01 | 5 | 4 |
| 305605 | Meridian Small Outdoor Sconce | CAT6 | COL131 | 2026-06-01 | 2 | 2 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2025-12-01 | 1 | 1 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2026-01-01 | 11 | 1 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2026-02-01 | 16 | 6 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2026-03-01 | 3 | 2 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2026-04-01 | 21 | 4 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2026-05-01 | 14 | 4 |
| 305610 | Meridian Outdoor Sconce | CAT6 | COL131 | 2026-06-01 | 19 | 5 |
| 305615 | Meridian Large Outdoor Sconce | CAT6 | COL131 | 2025-12-01 | 5 | 1 |
| 305615 | Meridian Large Outdoor Sconce | CAT6 | COL131 | 2026-02-01 | 9 | 4 |
| 305615 | Meridian Large Outdoor Sconce | CAT6 | COL131 | 2026-03-01 | 2 | 2 |
| 305615 | Meridian Large Outdoor Sconce | CAT6 | COL131 | 2026-04-01 | 7 | 2 |
| 305615 | Meridian Large Outdoor Sconce | CAT6 | COL131 | 2026-05-01 | 16 | 5 |
| 305615 | Meridian Large Outdoor Sconce | CAT6 | COL131 | 2026-06-01 | 19 | 4 |
| 305650 | Province Outdoor Sconce | CAT6 | COL132 | 2025-12-01 | 2 | 1 |
| 305650 | Province Outdoor Sconce | CAT6 | COL132 | 2026-03-01 | 5 | 2 |
| 305650 | Province Outdoor Sconce | CAT6 | COL132 | 2026-04-01 | 3 | 1 |
| 305650 | Province Outdoor Sconce | CAT6 | COL132 | 2026-05-01 | 4 | 1 |
| 305655 | Province Large Outdoor Sconce | CAT6 | COL132 | 2026-01-01 | 19 | 1 |
| 305655 | Province Large Outdoor Sconce | CAT6 | COL132 | 2026-03-01 | 6 | 1 |
| 305655 | Province Large Outdoor Sconce | CAT6 | COL132 | 2026-05-01 | 2 | 1 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2025-12-01 | 5 | 3 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 9 | 8 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 4 | 3 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 19 | 9 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 28 | 9 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 35 | 6 |
| 305892 | Banded Small Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 12 | 4 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2025-12-01 | 16 | 5 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 18 | 10 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 14 | 7 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 40 | 11 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 17 | 6 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 35 | 13 |
| 305893 | Banded Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 9 | 4 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2025-12-01 | 2 | 1 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 22 | 9 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 140 | 5 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 26 | 7 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 15 | 6 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 38 | 8 |
| 305894 | Banded Large Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 11 | 3 |
| 305895 | Banded Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 6 | 2 |
| 305895 | Banded Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 1 | 1 |
| 305895 | Banded Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 8 | 3 |
| 305895 | Banded Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 2 | 1 |
| 305895 | Banded Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 4 | 1 |
| 305896 | Torch Small Outdoor Sconce | CAT6 | TORCH | 2025-12-01 | 8 | 3 |
| 305896 | Torch Small Outdoor Sconce | CAT6 | TORCH | 2026-02-01 | 4 | 2 |
| 305896 | Torch Small Outdoor Sconce | CAT6 | TORCH | 2026-03-01 | 17 | 4 |
| 305896 | Torch Small Outdoor Sconce | CAT6 | TORCH | 2026-05-01 | 3 | 1 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2025-12-01 | 0 | 1 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2026-01-01 | 14 | 2 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2026-02-01 | 2 | 1 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2026-03-01 | 10 | 2 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2026-04-01 | 2 | 1 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2026-05-01 | 21 | 4 |
| 305897 | Torch Outdoor Sconce | CAT6 | TORCH | 2026-06-01 | 2 | 1 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2025-12-01 | 14 | 3 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2026-01-01 | 8 | 3 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2026-02-01 | 1 | 1 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2026-03-01 | 48 | 10 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2026-04-01 | 3 | 2 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2026-05-01 | 5 | 3 |
| 305898 | Torch Large Outdoor Sconce | CAT6 | TORCH | 2026-06-01 | 5 | 2 |
| 305899 | Torch XL Outdoor Sconce | CAT6 | TORCH | 2025-12-01 | 11 | 1 |
| 305899 | Torch XL Outdoor Sconce | CAT6 | TORCH | 2026-01-01 | 1 | 1 |
| 305899 | Torch XL Outdoor Sconce | CAT6 | TORCH | 2026-03-01 | 4 | 2 |
| 305899 | Torch XL Outdoor Sconce | CAT6 | TORCH | 2026-04-01 | 1 | 1 |
| 305899 | Torch XL Outdoor Sconce | CAT6 | TORCH | 2026-05-01 | 6 | 1 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2025-12-01 | 3 | 2 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 6 | 2 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 7 | 5 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 22 | 4 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 9 | 2 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 4 | 1 |
| 305992 | Banded with Top Plate Small Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 10 | 2 |
| 305993 | Banded with Top Plate Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 12 | 3 |
| 305993 | Banded with Top Plate Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 27 | 8 |
| 305993 | Banded with Top Plate Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 24 | 9 |
| 305993 | Banded with Top Plate Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 12 | 7 |
| 305993 | Banded with Top Plate Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 14 | 5 |
| 305993 | Banded with Top Plate Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 10 | 5 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2025-12-01 | 2 | 1 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 1 | 1 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2026-02-01 | 1 | 1 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 6 | 2 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 5 | 2 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2026-05-01 | 4 | 3 |
| 305994 | Banded with Top Plate Large Outdoor Sconce | CAT6 | COL16 | 2026-06-01 | 5 | 2 |
| 305995 | Banded with Top Plate Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-01-01 | 0 | 1 |
| 305995 | Banded with Top Plate Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-03-01 | 7 | 2 |
| 305995 | Banded with Top Plate Extra Large Outdoor Sconce | CAT6 | COL16 | 2026-04-01 | 2 | 1 |
| 305996 | Torch Small Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-01-01 | 17 | 1 |
| 305996 | Torch Small Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-03-01 | 12 | 2 |
| 305996 | Torch Small Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-04-01 | 2 | 1 |
| 305996 | Torch Small Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-05-01 | 1 | 1 |
| 305997 | Torch with Top Plate Outdoor Sconce | CAT6 | TORCH | 2025-12-01 | 9 | 2 |
| 305997 | Torch with Top Plate Outdoor Sconce | CAT6 | TORCH | 2026-01-01 | 11 | 3 |
| 305997 | Torch with Top Plate Outdoor Sconce | CAT6 | TORCH | 2026-02-01 | 8 | 3 |
| 305997 | Torch with Top Plate Outdoor Sconce | CAT6 | TORCH | 2026-04-01 | 4 | 1 |
| 305997 | Torch with Top Plate Outdoor Sconce | CAT6 | TORCH | 2026-05-01 | 2 | 1 |
| 305997 | Torch with Top Plate Outdoor Sconce | CAT6 | TORCH | 2026-06-01 | 3 | 2 |
| 305998 | Torch with Top Plate Large Outdoor Sconce | CAT6 | TORCH | 2026-01-01 | 11 | 3 |
| 305998 | Torch with Top Plate Large Outdoor Sconce | CAT6 | TORCH | 2026-03-01 | 25 | 2 |
| 305998 | Torch with Top Plate Large Outdoor Sconce | CAT6 | TORCH | 2026-04-01 | 11 | 4 |
| 305998 | Torch with Top Plate Large Outdoor Sconce | CAT6 | TORCH | 2026-05-01 | 16 | 3 |
| 305998 | Torch with Top Plate Large Outdoor Sconce | CAT6 | TORCH | 2026-06-01 | 3 | 1 |
| 305999 | Torch XL Outdoor Sconce with Top Plate | CAT6 | TORCH | 2025-12-01 | 2 | 1 |
| 305999 | Torch XL Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-01-01 | 4 | 1 |
| 305999 | Torch XL Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-02-01 | 35 | 3 |
| 305999 | Torch XL Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-03-01 | 3 | 1 |
| 305999 | Torch XL Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-04-01 | 1 | 1 |
| 305999 | Torch XL Outdoor Sconce with Top Plate | CAT6 | TORCH | 2026-06-01 | 3 | 1 |
| 306006 | Tourou Small Outdoor Sconce | CAT6 | COL133 | 2025-12-01 | 2 | 1 |
| 306006 | Tourou Small Outdoor Sconce | CAT6 | COL133 | 2026-02-01 | 1 | 1 |
| 306006 | Tourou Small Outdoor Sconce | CAT6 | COL133 | 2026-03-01 | 3 | 1 |
| 306006 | Tourou Small Outdoor Sconce | CAT6 | COL133 | 2026-04-01 | 8 | 3 |
| 306006 | Tourou Small Outdoor Sconce | CAT6 | COL133 | 2026-05-01 | 3 | 2 |
| 306006 | Tourou Small Outdoor Sconce | CAT6 | COL133 | 2026-06-01 | 8 | 5 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2025-12-01 | 4 | 1 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2026-01-01 | 5 | 2 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2026-02-01 | 12 | 6 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2026-03-01 | 10 | 4 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2026-04-01 | 8 | 3 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2026-05-01 | 8 | 1 |
| 306007 | Tourou Outdoor Sconce | CAT6 | COL133 | 2026-06-01 | 27 | 5 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2025-12-01 | 6 | 2 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2026-01-01 | 1 | 1 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2026-02-01 | 1 | 1 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2026-03-01 | 15 | 6 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2026-04-01 | 17 | 5 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2026-05-01 | 28 | 4 |
| 306008 | Tourou Large Outdoor Sconce | CAT6 | COL133 | 2026-06-01 | 18 | 3 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2025-12-01 | 6 | 1 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2026-01-01 | 21 | 9 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2026-02-01 | 20 | 6 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2026-03-01 | 11 | 5 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2026-04-01 | 28 | 7 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2026-05-01 | 5 | 2 |
| 306401 | Axis Small Outdoor Sconce | CAT6 | AXIS | 2026-06-01 | 26 | 6 |
| 306403 | Axis Outdoor Sconce | CAT6 | AXIS | 2026-01-01 | 17 | 5 |
| 306403 | Axis Outdoor Sconce | CAT6 | AXIS | 2026-02-01 | 27 | 7 |
| 306403 | Axis Outdoor Sconce | CAT6 | AXIS | 2026-03-01 | 24 | 8 |
| 306403 | Axis Outdoor Sconce | CAT6 | AXIS | 2026-04-01 | 41 | 11 |
| 306403 | Axis Outdoor Sconce | CAT6 | AXIS | 2026-05-01 | 30 | 8 |
| 306403 | Axis Outdoor Sconce | CAT6 | AXIS | 2026-06-01 | 11 | 2 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2025-12-01 | 2 | 2 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2026-01-01 | 54 | 8 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2026-02-01 | 52 | 14 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2026-03-01 | 22 | 9 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2026-04-01 | 55 | 10 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2026-05-01 | 31 | 8 |
| 306405 | Axis Large Outdoor Sconce | CAT6 | AXIS | 2026-06-01 | 11 | 3 |
| 306415 | Double Axis Small LED Outdoor Sconce | CAT6 | AXIS | 2025-12-01 | 6 | 2 |
| 306415 | Double Axis Small LED Outdoor Sconce | CAT6 | AXIS | 2026-01-01 | 7 | 2 |
| 306415 | Double Axis Small LED Outdoor Sconce | CAT6 | AXIS | 2026-02-01 | 8 | 4 |
| 306415 | Double Axis Small LED Outdoor Sconce | CAT6 | AXIS | 2026-03-01 | 12 | 4 |
| 306415 | Double Axis Small LED Outdoor Sconce | CAT6 | AXIS | 2026-04-01 | 18 | 4 |
| 306415 | Double Axis Small LED Outdoor Sconce | CAT6 | AXIS | 2026-05-01 | 1 | 1 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2025-12-01 | 30 | 2 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2026-01-01 | 8 | 2 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2026-02-01 | 19 | 7 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2026-03-01 | 4 | 2 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2026-04-01 | 22 | 4 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2026-05-01 | 8 | 6 |
| 306420 | Double Axis LED Outdoor Sconce | CAT6 | AXIS | 2026-06-01 | 14 | 4 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2025-12-01 | 3 | 2 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2026-01-01 | 9 | 2 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2026-02-01 | 3 | 2 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2026-03-01 | 4 | 3 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2026-04-01 | 17 | 6 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2026-05-01 | 5 | 3 |
| 306425 | Double Axis Large LED Outdoor Sconce | CAT6 | AXIS | 2026-06-01 | 6 | 3 |
| 306453 | Fuse Outdoor Sconce | CAT6 | FUSE | 2025-12-01 | 2 | 1 |
| 306455 | Fuse Large Outdoor Sconce | CAT6 | FUSE | 2026-03-01 | 17 | 2 |
| 306455 | Fuse Large Outdoor Sconce | CAT6 | FUSE | 2026-04-01 | 26 | 2 |
| 306560 | — | — | — | 2026-02-01 | 1 | 1 |
| 306563 | Hood Dark Sky Outdoor Sconce | CAT6 | HOOD | 2025-12-01 | 4 | 2 |
| 306563 | Hood Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-01-01 | 6 | 1 |
| 306563 | Hood Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-02-01 | 4 | 3 |
| 306563 | Hood Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-03-01 | 8 | 7 |
| 306563 | Hood Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-04-01 | 19 | 3 |
| 306563 | Hood Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-05-01 | 17 | 5 |
| 306567 | Hood Large Dark Sky Outdoor Sconce | CAT6 | HOOD | 2025-12-01 | 2 | 2 |
| 306567 | Hood Large Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-01-01 | 5 | 2 |
| 306567 | Hood Large Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-02-01 | 1 | 1 |
| 306567 | Hood Large Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-03-01 | 2 | 1 |
| 306567 | Hood Large Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-05-01 | 9 | 2 |
| 306567 | Hood Large Dark Sky Outdoor Sconce | CAT6 | HOOD | 2026-06-01 | 2 | 1 |
| 306603 | — | — | — | 2026-05-01 | 1 | 1 |
| 307281 | Vertical Bar Fluted Glass Small Outdoor Sconce | CAT6 | COL105 | 2025-12-01 | 1 | 1 |
| 307281 | Vertical Bar Fluted Glass Small Outdoor Sconce | CAT6 | COL105 | 2026-02-01 | 4 | 3 |
| 307282 | Vertical Bar Fluted Glass Medium Outdoor Sconce | CAT6 | COL105 | 2025-12-01 | 9 | 2 |
| 307282 | Vertical Bar Fluted Glass Medium Outdoor Sconce | CAT6 | COL105 | 2026-02-01 | 4 | 1 |
| 307282 | Vertical Bar Fluted Glass Medium Outdoor Sconce | CAT6 | COL105 | 2026-04-01 | 6 | 1 |
| 307283 | Vertical Bar Fluted Glass Large Outdoor Sconce | CAT6 | COL105 | 2025-12-01 | 3 | 2 |
| 307283 | Vertical Bar Fluted Glass Large Outdoor Sconce | CAT6 | COL105 | 2026-02-01 | 1 | 1 |
| 307283 | Vertical Bar Fluted Glass Large Outdoor Sconce | CAT6 | COL105 | 2026-04-01 | 9 | 2 |
| 307283 | Vertical Bar Fluted Glass Large Outdoor Sconce | CAT6 | COL105 | 2026-05-01 | 4 | 2 |
| 307285 | Forged Vertical Bars Small Outdoor Sconce | CAT6 | COL105 | 2026-01-01 | 3 | 2 |
| 307285 | Forged Vertical Bars Small Outdoor Sconce | CAT6 | COL105 | 2026-02-01 | 1 | 1 |
| 307285 | Forged Vertical Bars Small Outdoor Sconce | CAT6 | COL105 | 2026-03-01 | 5 | 3 |
| 307285 | Forged Vertical Bars Small Outdoor Sconce | CAT6 | COL105 | 2026-05-01 | 16 | 6 |
| 307285 | Forged Vertical Bars Small Outdoor Sconce | CAT6 | COL105 | 2026-06-01 | 4 | 2 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2025-12-01 | 6 | 2 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2026-01-01 | 1 | 1 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2026-02-01 | 7 | 4 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2026-03-01 | 15 | 3 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2026-04-01 | 5 | 2 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2026-05-01 | 23 | 7 |
| 307286 | Forged Vertical Bars Outdoor Sconce | CAT6 | COL105 | 2026-06-01 | 5 | 2 |
| 307287 | Forged Vertical Bars Large Outdoor Sconce | CAT6 | COL105 | 2026-01-01 | 1 | 1 |
| 307287 | Forged Vertical Bars Large Outdoor Sconce | CAT6 | COL105 | 2026-02-01 | 12 | 3 |
| 307287 | Forged Vertical Bars Large Outdoor Sconce | CAT6 | COL105 | 2026-03-01 | 15 | 3 |
| 307287 | Forged Vertical Bars Large Outdoor Sconce | CAT6 | COL105 | 2026-04-01 | 5 | 1 |
| 307287 | Forged Vertical Bars Large Outdoor Sconce | CAT6 | COL105 | 2026-05-01 | 4 | 1 |
| 307287 | Forged Vertical Bars Large Outdoor Sconce | CAT6 | COL105 | 2026-06-01 | 5 | 3 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2025-12-01 | 6 | 1 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2026-01-01 | 7 | 3 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2026-02-01 | 2 | 1 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2026-03-01 | 5 | 2 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2026-04-01 | 13 | 2 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2026-05-01 | 5 | 2 |
| 307650 | Gallery Small Outdoor Sconce | CAT6 | COL114 | 2026-06-01 | 10 | 3 |
| 307651 | Gallery Outdoor Sconce | CAT6 | COL114 | 2025-12-01 | 11 | 3 |
| 307651 | Gallery Outdoor Sconce | CAT6 | COL114 | 2026-01-01 | 6 | 2 |
| 307651 | Gallery Outdoor Sconce | CAT6 | COL114 | 2026-02-01 | 7 | 4 |
| 307651 | Gallery Outdoor Sconce | CAT6 | COL114 | 2026-03-01 | 5 | 2 |
| 307651 | Gallery Outdoor Sconce | CAT6 | COL114 | 2026-05-01 | 6 | 1 |
| 307651 | Gallery Outdoor Sconce | CAT6 | COL114 | 2026-06-01 | 10 | 4 |
| 307653 | Gallery Large Outdoor Sconce | CAT6 | COL114 | 2025-12-01 | 6 | 2 |
| 307653 | Gallery Large Outdoor Sconce | CAT6 | COL114 | 2026-01-01 | 6 | 2 |
| 307653 | Gallery Large Outdoor Sconce | CAT6 | COL114 | 2026-02-01 | 6 | 2 |
| 307653 | Gallery Large Outdoor Sconce | CAT6 | COL114 | 2026-03-01 | 3 | 2 |
| 307653 | Gallery Large Outdoor Sconce | CAT6 | COL114 | 2026-05-01 | 19 | 6 |
| 307653 | Gallery Large Outdoor Sconce | CAT6 | COL114 | 2026-06-01 | 2 | 2 |
| 307710 | Erlenmeyer Small Outdoor Sconce | CAT6 | COL25 | 2026-01-01 | 2 | 1 |
| 307710 | Erlenmeyer Small Outdoor Sconce | CAT6 | COL25 | 2026-03-01 | 10 | 3 |
| 307710 | Erlenmeyer Small Outdoor Sconce | CAT6 | COL25 | 2026-04-01 | 8 | 3 |
| 307710 | Erlenmeyer Small Outdoor Sconce | CAT6 | COL25 | 2026-05-01 | 18 | 8 |
| 307710 | Erlenmeyer Small Outdoor Sconce | CAT6 | COL25 | 2026-06-01 | 4 | 2 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2025-12-01 | 1 | 1 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2026-01-01 | 2 | 2 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2026-02-01 | 10 | 7 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2026-03-01 | 18 | 5 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2026-04-01 | 31 | 8 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2026-05-01 | 56 | 14 |
| 307715 | Erlenmeyer Medium Outdoor Sconce | CAT6 | COL25 | 2026-06-01 | 12 | 5 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2025-12-01 | 2 | 1 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2026-01-01 | 22 | 3 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2026-02-01 | 8 | 4 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2026-03-01 | 29 | 5 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2026-04-01 | 11 | 5 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2026-05-01 | 8 | 4 |
| 307716 | Erlenmeyer Dark Sky Friendly Outdoor Sconce | CAT6 | COL25 | 2026-06-01 | 7 | 4 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2025-12-01 | 15 | 2 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2026-01-01 | 3 | 2 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2026-02-01 | 23 | 5 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2026-03-01 | 8 | 4 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2026-04-01 | 2 | 2 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2026-05-01 | 7 | 4 |
| 307720 | Erlenmeyer Large Outdoor Sconce | CAT6 | COL25 | 2026-06-01 | 1 | 1 |
| 307860 | After Hours Outdoor Sconce | CAT6 | COL108 | 2026-01-01 | 2 | 1 |
| 307860 | After Hours Outdoor Sconce | CAT6 | COL108 | 2026-02-01 | 14 | 2 |
| 307860 | After Hours Outdoor Sconce | CAT6 | COL108 | 2026-03-01 | 3 | 2 |
| 307860 | After Hours Outdoor Sconce | CAT6 | COL108 | 2026-04-01 | 6 | 2 |
| 307860 | After Hours Outdoor Sconce | CAT6 | COL108 | 2026-05-01 | 10 | 3 |
| 307860 | After Hours Outdoor Sconce | CAT6 | COL108 | 2026-06-01 | 7 | 1 |
| 307861 | After Hours Large Outdoor Sconce | CAT6 | COL108 | 2026-01-01 | 0 | 1 |
| 307861 | After Hours Large Outdoor Sconce | CAT6 | COL108 | 2026-02-01 | 4 | 1 |
| 307861 | After Hours Large Outdoor Sconce | CAT6 | COL108 | 2026-04-01 | 7 | 2 |
| 307861 | After Hours Large Outdoor Sconce | CAT6 | COL108 | 2026-05-01 | 2 | 1 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2025-12-01 | 38 | 5 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-01-01 | 23 | 6 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-02-01 | 23 | 5 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-03-01 | 22 | 6 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-04-01 | 29 | 9 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-05-01 | 28 | 12 |
| 307910 | Airis Small Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-06-01 | 11 | 3 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2025-12-01 | 5 | 2 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-01-01 | 43 | 13 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-02-01 | 42 | 11 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-03-01 | 41 | 11 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-04-01 | 19 | 9 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-05-01 | 12 | 4 |
| 307920 | Airis Medium Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-06-01 | 11 | 4 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2025-12-01 | 4 | 2 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-01-01 | 20 | 4 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-02-01 | 28 | 4 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-03-01 | 35 | 4 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-04-01 | 5 | 3 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-05-01 | 1 | 1 |
| 307930 | Airis Large Dark Sky Friendly Outdoor Sconce | CAT6 | AIRIS | 2026-06-01 | 13 | 2 |
| 335796 | Banded Outdoor Pier Mount | CAT6 | COL16 | 2026-01-01 | 2 | 1 |
| 335796 | Banded Outdoor Pier Mount | CAT6 | COL16 | 2026-02-01 | 3 | 2 |
| 335796 | Banded Outdoor Pier Mount | CAT6 | COL16 | 2026-03-01 | 2 | 2 |
| 335796 | Banded Outdoor Pier Mount | CAT6 | COL16 | 2026-05-01 | 9 | 3 |
| 342021 | Cela Outdoor Post Light | CAT6 | CELA | 2026-01-01 | 3 | 3 |
| 342021 | Cela Outdoor Post Light | CAT6 | CELA | 2026-02-01 | 3 | 2 |
| 342021 | Cela Outdoor Post Light | CAT6 | CELA | 2026-03-01 | 6 | 2 |
| 342021 | Cela Outdoor Post Light | CAT6 | CELA | 2026-04-01 | 10 | 2 |
| 342021 | Cela Outdoor Post Light | CAT6 | CELA | 2026-05-01 | 3 | 2 |
| 342025 | Alcove Outdoor Post Light | CAT6 | COL112 | 2026-01-01 | 1 | 1 |
| 342025 | Alcove Outdoor Post Light | CAT6 | COL112 | 2026-05-01 | 5 | 1 |
| 342026 | Linea Outdoor Lantern Post Light | CAT6 | LINEA | 2026-03-01 | 10 | 1 |
| 342030 | Triomphe Post Light | CAT6 | COL83 | 2025-12-01 | 2 | 1 |
| 342030 | Triomphe Post Light | CAT6 | COL83 | 2026-04-01 | 2 | 1 |
| 342031 | Stowe Outdoor Lantern Post Light | CAT6 | STOWE | 2026-01-01 | 2 | 2 |
| 342031 | Stowe Outdoor Lantern Post Light | CAT6 | STOWE | 2026-02-01 | 3 | 3 |
| 342031 | Stowe Outdoor Lantern Post Light | CAT6 | STOWE | 2026-05-01 | 22 | 3 |
| 342553 | Fairwinds Outdoor Post Light | CAT6 | COL121 | 2026-02-01 | 2 | 1 |
| 342553 | Fairwinds Outdoor Post Light | CAT6 | COL121 | 2026-06-01 | 1 | 1 |
| 342554 | Fairwinds Extra Large Outdoor Post Light | CAT6 | COL121 | 2025-12-01 | 8 | 1 |
| 342554 | Fairwinds Extra Large Outdoor Post Light | CAT6 | COL121 | 2026-02-01 | 6 | 2 |
| 342651 | Stellar Post Light | CAT6 | COL125 | 2026-02-01 | 5 | 3 |
| 342651 | Stellar Post Light | CAT6 | COL125 | 2026-04-01 | 2 | 1 |
| 342652 | Stellar Dark Sky Friendly Post Light | CAT6 | COL125 | 2026-03-01 | 2 | 2 |
| 344227 | Henry Outdoor Post Light | CAT6 | HENRY | 2025-12-01 | 2 | 1 |
| 344227 | Henry Outdoor Post Light | CAT6 | HENRY | 2026-02-01 | 4 | 2 |
| 344227 | Henry Outdoor Post Light | CAT6 | HENRY | 2026-03-01 | 6 | 4 |
| 344227 | Henry Outdoor Post Light | CAT6 | HENRY | 2026-04-01 | 1 | 1 |
| 344227 | Henry Outdoor Post Light | CAT6 | HENRY | 2026-05-01 | 5 | 2 |
| 344810 | Mason Post Light | CAT6 | MASON | 2026-02-01 | 2 | 2 |
| 344810 | Mason Post Light | CAT6 | MASON | 2026-03-01 | 8 | 2 |
| 344810 | Mason Post Light | CAT6 | MASON | 2026-04-01 | 1 | 1 |
| 344810 | Mason Post Light | CAT6 | MASON | 2026-05-01 | 12 | 2 |
| 344820 | Beacon Hall Outdoor Post Light | CAT6 | COL31 | 2025-12-01 | 3 | 2 |
| 344820 | Beacon Hall Outdoor Post Light | CAT6 | COL31 | 2026-02-01 | 1 | 1 |
| 344820 | Beacon Hall Outdoor Post Light | CAT6 | COL31 | 2026-03-01 | 10 | 3 |
| 344820 | Beacon Hall Outdoor Post Light | CAT6 | COL31 | 2026-04-01 | 4 | 1 |
| 344820 | Beacon Hall Outdoor Post Light | CAT6 | COL31 | 2026-06-01 | 1 | 1 |
| 344830 | Shadow Box Outdoor Post Light | CAT6 | COL122 | 2025-12-01 | 4 | 2 |
| 344830 | Shadow Box Outdoor Post Light | CAT6 | COL122 | 2026-01-01 | 17 | 3 |
| 344830 | Shadow Box Outdoor Post Light | CAT6 | COL122 | 2026-03-01 | 1 | 1 |
| 344830 | Shadow Box Outdoor Post Light | CAT6 | COL122 | 2026-04-01 | 18 | 10 |
| 344830 | Shadow Box Outdoor Post Light | CAT6 | COL122 | 2026-05-01 | 11 | 5 |
| 344830 | Shadow Box Outdoor Post Light | CAT6 | COL122 | 2026-06-01 | 11 | 3 |
| 344840 | Kingston Outdoor Post Light | CAT6 | COL129 | 2026-03-01 | 2 | 2 |
| 344840 | Kingston Outdoor Post Light | CAT6 | COL129 | 2026-05-01 | 1 | 1 |
| 344850 | Polaris Outdoor Post Light | CAT6 | COL130 | 2026-01-01 | 2 | 1 |
| 344850 | Polaris Outdoor Post Light | CAT6 | COL130 | 2026-02-01 | 2 | 1 |
| 344850 | Polaris Outdoor Post Light | CAT6 | COL130 | 2026-05-01 | 27 | 1 |
| 344850 | Polaris Outdoor Post Light | CAT6 | COL130 | 2026-06-01 | 1 | 1 |
| 345203 | Dorset Dark Sky Friendly Post Light | CAT6 | COL95 | 2025-12-01 | 2 | 1 |
| 345203 | Dorset Dark Sky Friendly Post Light | CAT6 | COL95 | 2026-02-01 | 1 | 1 |
| 345203 | Dorset Dark Sky Friendly Post Light | CAT6 | COL95 | 2026-04-01 | 1 | 1 |
| 345203 | Dorset Dark Sky Friendly Post Light | CAT6 | COL95 | 2026-05-01 | 9 | 2 |
| 345203 | Dorset Dark Sky Friendly Post Light | CAT6 | COL95 | 2026-06-01 | 2 | 1 |
| 345213 | Davis Post Light | CAT6 | DAVIS | 2026-04-01 | 1 | 1 |
| 345610 | Meridian Outdoor Post Light | CAT6 | COL131 | 2026-01-01 | 1 | 1 |
| 345610 | Meridian Outdoor Post Light | CAT6 | COL131 | 2026-02-01 | 3 | 1 |
| 345610 | Meridian Outdoor Post Light | CAT6 | COL131 | 2026-03-01 | 1 | 1 |
| 345610 | Meridian Outdoor Post Light | CAT6 | COL131 | 2026-04-01 | 5 | 3 |
| 345610 | Meridian Outdoor Post Light | CAT6 | COL131 | 2026-05-01 | 5 | 3 |
| 345610 | Meridian Outdoor Post Light | CAT6 | COL131 | 2026-06-01 | 2 | 1 |
| 345895 | Banded Outdoor Post Light | CAT6 | COL16 | 2025-12-01 | 5 | 2 |
| 345895 | Banded Outdoor Post Light | CAT6 | COL16 | 2026-01-01 | 7 | 1 |
| 345895 | Banded Outdoor Post Light | CAT6 | COL16 | 2026-03-01 | 2 | 2 |
| 345895 | Banded Outdoor Post Light | CAT6 | COL16 | 2026-04-01 | 1 | 1 |
| 345897 | Torch Outdoor Post Light | CAT6 | TORCH | 2026-01-01 | 1 | 1 |
| 346011 | Tourou Outdoor Post Light | CAT6 | COL133 | 2026-01-01 | 3 | 2 |
| 346011 | Tourou Outdoor Post Light | CAT6 | COL133 | 2026-02-01 | 1 | 1 |
| 346011 | Tourou Outdoor Post Light | CAT6 | COL133 | 2026-04-01 | 2 | 1 |
| 346011 | Tourou Outdoor Post Light | CAT6 | COL133 | 2026-06-01 | 2 | 1 |
| 346013 | Tourou Large Outdoor Post Light | CAT6 | COL133 | 2026-02-01 | 1 | 1 |
| 346013 | Tourou Large Outdoor Post Light | CAT6 | COL133 | 2026-03-01 | 3 | 2 |
| 346013 | Tourou Large Outdoor Post Light | CAT6 | COL133 | 2026-04-01 | 1 | 1 |
| 346013 | Tourou Large Outdoor Post Light | CAT6 | COL133 | 2026-05-01 | 1 | 1 |
| 346013 | Tourou Large Outdoor Post Light | CAT6 | COL133 | 2026-06-01 | 2 | 1 |
| 346410 | Axis Large Outdoor Post Light | CAT6 | AXIS | 2025-12-01 | 4 | 1 |
| 346410 | Axis Large Outdoor Post Light | CAT6 | AXIS | 2026-01-01 | 15 | 3 |
| 346410 | Axis Large Outdoor Post Light | CAT6 | AXIS | 2026-04-01 | 1 | 1 |
| 347288 | Forged Vertical Bars Outdoor Post Light | CAT6 | COL105 | 2026-03-01 | 4 | 2 |
| 347288 | Forged Vertical Bars Outdoor Post Light | CAT6 | COL105 | 2026-04-01 | 5 | 2 |
| 347288 | Forged Vertical Bars Outdoor Post Light | CAT6 | COL105 | 2026-05-01 | 1 | 1 |
| 347288 | Forged Vertical Bars Outdoor Post Light | CAT6 | COL105 | 2026-06-01 | 4 | 2 |
| 347295 | Erlenmeyer Outdoor Post Light | CAT6 | COL25 | 2026-02-01 | 3 | 2 |
| 347295 | Erlenmeyer Outdoor Post Light | CAT6 | COL25 | 2026-03-01 | 2 | 2 |
| 347295 | Erlenmeyer Outdoor Post Light | CAT6 | COL25 | 2026-04-01 | 1 | 1 |
| 352551 | Fairwinds Outdoor Semi-Flush | CAT6 | COL121 | 2025-12-01 | 2 | 1 |
| 352551 | Fairwinds Outdoor Semi-Flush | CAT6 | COL121 | 2026-05-01 | 1 | 1 |
| 352551 | Fairwinds Outdoor Semi-Flush | CAT6 | COL121 | 2026-06-01 | 3 | 2 |
| 356010 | Erlenmeyer Outdoor Pendant | CAT6 | COL25 | 2026-01-01 | 5 | 2 |
| 356010 | Erlenmeyer Outdoor Pendant | CAT6 | COL25 | 2026-02-01 | 4 | 2 |
| 356010 | Erlenmeyer Outdoor Pendant | CAT6 | COL25 | 2026-03-01 | 2 | 1 |
| 356010 | Erlenmeyer Outdoor Pendant | CAT6 | COL25 | 2026-05-01 | 1 | 1 |
| 356010 | Erlenmeyer Outdoor Pendant | CAT6 | COL25 | 2026-06-01 | 1 | 1 |
| 356015 | Erlenmeyer Outdoor Semi-Flush | CAT6 | COL25 | 2026-01-01 | 2 | 2 |
| 356015 | Erlenmeyer Outdoor Semi-Flush | CAT6 | COL25 | 2026-02-01 | 2 | 2 |
| 356015 | Erlenmeyer Outdoor Semi-Flush | CAT6 | COL25 | 2026-03-01 | 2 | 2 |
| 356015 | Erlenmeyer Outdoor Semi-Flush | CAT6 | COL25 | 2026-04-01 | 3 | 2 |
| 356015 | Erlenmeyer Outdoor Semi-Flush | CAT6 | COL25 | 2026-05-01 | 2 | 1 |
| 356840 | Kingston Outdoor Large Lantern | CAT6 | COL129 | 2026-01-01 | 4 | 3 |
| 356840 | Kingston Outdoor Large Lantern | CAT6 | COL129 | 2026-02-01 | 5 | 1 |
| 356840 | Kingston Outdoor Large Lantern | CAT6 | COL129 | 2026-03-01 | 0 | 1 |
| 362001 | — | — | — | 2026-01-01 | 1 | 1 |
| 362010 | Portico Drum Outdoor Pendant | CAT6 | COL128 | 2026-01-01 | 5 | 1 |
| 362010 | Portico Drum Outdoor Pendant | CAT6 | COL128 | 2026-02-01 | 2 | 1 |
| 362010 | Portico Drum Outdoor Pendant | CAT6 | COL128 | 2026-03-01 | 4 | 3 |
| 362010 | Portico Drum Outdoor Pendant | CAT6 | COL128 | 2026-04-01 | 1 | 1 |
| 362010 | Portico Drum Outdoor Pendant | CAT6 | COL128 | 2026-05-01 | 1 | 1 |
| 362015 | Divergence Outdoor Pendant | CAT6 | COL58 | 2026-03-01 | 2 | 2 |
| 362015 | Divergence Outdoor Pendant | CAT6 | COL58 | 2026-04-01 | 2 | 2 |
| 362015 | Divergence Outdoor Pendant | CAT6 | COL58 | 2026-06-01 | 4 | 3 |
| 362021 | Cela Medium Outdoor Lantern | CAT6 | CELA | 2026-03-01 | 3 | 2 |
| 362023 | Cela Large Outdoor Lantern | CAT6 | CELA | 2025-12-01 | 1 | 1 |
| 362023 | Cela Large Outdoor Lantern | CAT6 | CELA | 2026-01-01 | 5 | 3 |
| 362023 | Cela Large Outdoor Lantern | CAT6 | CELA | 2026-04-01 | 1 | 1 |
| 362023 | Cela Large Outdoor Lantern | CAT6 | CELA | 2026-05-01 | 4 | 4 |
| 362024 | Stowe Outdoor Lantern | CAT6 | STOWE | 2026-01-01 | 7 | 6 |
| 362024 | Stowe Outdoor Lantern | CAT6 | STOWE | 2026-02-01 | 4 | 4 |
| 362024 | Stowe Outdoor Lantern | CAT6 | STOWE | 2026-03-01 | 6 | 4 |
| 362024 | Stowe Outdoor Lantern | CAT6 | STOWE | 2026-04-01 | 1 | 1 |
| 362024 | Stowe Outdoor Lantern | CAT6 | STOWE | 2026-05-01 | 1 | 1 |
| 362025 | Stowe 4-Light Outdoor Pendant | CAT6 | STOWE | 2026-02-01 | 2 | 2 |
| 362025 | Stowe 4-Light Outdoor Pendant | CAT6 | STOWE | 2026-03-01 | 1 | 1 |
| 362555 | Alcove Outdoor Pendant | CAT6 | COL112 | 2026-01-01 | 5 | 5 |
| 362555 | Alcove Outdoor Pendant | CAT6 | COL112 | 2026-05-01 | 5 | 2 |
| 362651 | Stellar Large Outdoor Pendant/Semi-Flush | CAT6 | COL125 | 2025-12-01 | 2 | 2 |
| 362651 | Stellar Large Outdoor Pendant/Semi-Flush | CAT6 | COL125 | 2026-01-01 | 2 | 2 |
| 362651 | Stellar Large Outdoor Pendant/Semi-Flush | CAT6 | COL125 | 2026-02-01 | 4 | 4 |
| 362651 | Stellar Large Outdoor Pendant/Semi-Flush | CAT6 | COL125 | 2026-03-01 | 9 | 6 |
| 362651 | Stellar Large Outdoor Pendant/Semi-Flush | CAT6 | COL125 | 2026-04-01 | 7 | 7 |
| 362651 | Stellar Large Outdoor Pendant/Semi-Flush | CAT6 | COL125 | 2026-05-01 | 5 | 4 |
| 363001 | — | — | — | 2026-01-01 | 1 | 1 |
| 363001 | — | — | — | 2026-03-01 | 6 | 1 |
| 363003 | Mason Outdoor Ceiling Fixture | CAT6 | MASON | 2026-01-01 | 6 | 3 |
| 363003 | Mason Outdoor Ceiling Fixture | CAT6 | MASON | 2026-02-01 | 2 | 2 |
| 363003 | Mason Outdoor Ceiling Fixture | CAT6 | MASON | 2026-03-01 | 9 | 2 |
| 363003 | Mason Outdoor Ceiling Fixture | CAT6 | MASON | 2026-05-01 | 12 | 3 |
| 363005 | Mason Large Outdoor Ceiling Fixture | CAT6 | MASON | 2026-01-01 | 8 | 7 |
| 363005 | Mason Large Outdoor Ceiling Fixture | CAT6 | MASON | 2026-02-01 | 8 | 4 |
| 363005 | Mason Large Outdoor Ceiling Fixture | CAT6 | MASON | 2026-03-01 | 9 | 5 |
| 363005 | Mason Large Outdoor Ceiling Fixture | CAT6 | MASON | 2026-04-01 | 3 | 1 |
| 363005 | Mason Large Outdoor Ceiling Fixture | CAT6 | MASON | 2026-05-01 | 4 | 3 |
| 363005 | Mason Large Outdoor Ceiling Fixture | CAT6 | MASON | 2026-06-01 | 3 | 3 |
| 363008 | Henry Outdoor Pendant Medium | CAT6 | HENRY | 2025-12-01 | 8 | 1 |
| 363008 | Henry Outdoor Pendant Medium | CAT6 | HENRY | 2026-02-01 | 3 | 3 |
| 363008 | Henry Outdoor Pendant Medium | CAT6 | HENRY | 2026-03-01 | 4 | 3 |
| 363008 | Henry Outdoor Pendant Medium | CAT6 | HENRY | 2026-04-01 | 3 | 2 |
| 363008 | Henry Outdoor Pendant Medium | CAT6 | HENRY | 2026-05-01 | 5 | 2 |
| 363009 | Henry Outdoor Pendant with Glass Medium | CAT6 | HENRY | 2026-02-01 | 1 | 1 |
| 363009 | Henry Outdoor Pendant with Glass Medium | CAT6 | HENRY | 2026-03-01 | 2 | 1 |
| 363009 | Henry Outdoor Pendant with Glass Medium | CAT6 | HENRY | 2026-04-01 | 5 | 1 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2025-12-01 | 3 | 1 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2026-01-01 | 5 | 4 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2026-02-01 | 4 | 4 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2026-03-01 | 7 | 5 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2026-04-01 | 3 | 2 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2026-05-01 | 4 | 4 |
| 363010 | Henry Outdoor Pendant | CAT6 | HENRY | 2026-06-01 | 4 | 3 |
| 363017 | Linea Outdoor Lantern | CAT6 | LINEA | 2026-03-01 | 2 | 2 |
| 363017 | Linea Outdoor Lantern | CAT6 | LINEA | 2026-05-01 | 1 | 1 |
| 363017 | Linea Outdoor Lantern | CAT6 | LINEA | 2026-06-01 | 1 | 1 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2025-12-01 | 14 | 1 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2026-01-01 | 4 | 3 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2026-02-01 | 5 | 2 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2026-03-01 | 6 | 4 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2026-04-01 | 4 | 3 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2026-05-01 | 4 | 3 |
| 363100 | Shadow Box Small Outdoor Flush Mount | CAT6 | COL122 | 2026-06-01 | 13 | 1 |
| 363102 | Shadow Box Large Outdoor Flush Mount | CAT6 | COL122 | 2025-12-01 | 1 | 1 |
| 363102 | Shadow Box Large Outdoor Flush Mount | CAT6 | COL122 | 2026-02-01 | 6 | 4 |
| 363102 | Shadow Box Large Outdoor Flush Mount | CAT6 | COL122 | 2026-03-01 | 2 | 2 |
| 363102 | Shadow Box Large Outdoor Flush Mount | CAT6 | COL122 | 2026-04-01 | 2 | 3 |
| 363102 | Shadow Box Large Outdoor Flush Mount | CAT6 | COL122 | 2026-05-01 | 2 | 2 |
| 363102 | Shadow Box Large Outdoor Flush Mount | CAT6 | COL122 | 2026-06-01 | 4 | 1 |
| 364030 | Triomphe Outdoor Lantern | CAT6 | COL83 | 2026-01-01 | 5 | 4 |
| 364030 | Triomphe Outdoor Lantern | CAT6 | COL83 | 2026-02-01 | 6 | 4 |
| 364030 | Triomphe Outdoor Lantern | CAT6 | COL83 | 2026-03-01 | 3 | 2 |
| 364030 | Triomphe Outdoor Lantern | CAT6 | COL83 | 2026-04-01 | 27 | 7 |
| 364030 | Triomphe Outdoor Lantern | CAT6 | COL83 | 2026-05-01 | 12 | 6 |
| 364030 | Triomphe Outdoor Lantern | CAT6 | COL83 | 2026-06-01 | 4 | 4 |
| 364201 | Pomme Outdoor Pendant | CAT6 | POMME | 2026-01-01 | 1 | 1 |
| 364201 | Pomme Outdoor Pendant | CAT6 | POMME | 2026-04-01 | 4 | 4 |
| 364201 | Pomme Outdoor Pendant | CAT6 | POMME | 2026-05-01 | 1 | 1 |
| 364210 | Henry Outdoor 4-Light Pendant | CAT6 | HENRY | 2026-01-01 | 1 | 1 |
| 364210 | Henry Outdoor 4-Light Pendant | CAT6 | HENRY | 2026-02-01 | 1 | 1 |
| 364210 | Henry Outdoor 4-Light Pendant | CAT6 | HENRY | 2026-03-01 | 1 | 1 |
| 364210 | Henry Outdoor 4-Light Pendant | CAT6 | HENRY | 2026-04-01 | 3 | 2 |
| 364210 | Henry Outdoor 4-Light Pendant | CAT6 | HENRY | 2026-05-01 | 2 | 2 |
| 364210 | Henry Outdoor 4-Light Pendant | CAT6 | HENRY | 2026-06-01 | 1 | 1 |
| 364212 | Mason Outdoor 4-Light Pendant | CAT6 | MASON | 2025-12-01 | 2 | 1 |
| 364213 | Polaris Outdoor 4-Light Pendant | CAT6 | COL130 | 2025-12-01 | 2 | 2 |
| 364213 | Polaris Outdoor 4-Light Pendant | CAT6 | COL130 | 2026-01-01 | 2 | 2 |
| 364213 | Polaris Outdoor 4-Light Pendant | CAT6 | COL130 | 2026-02-01 | 4 | 4 |
| 364213 | Polaris Outdoor 4-Light Pendant | CAT6 | COL130 | 2026-03-01 | 1 | 1 |
| 364213 | Polaris Outdoor 4-Light Pendant | CAT6 | COL130 | 2026-04-01 | 3 | 4 |
| 364213 | Polaris Outdoor 4-Light Pendant | CAT6 | COL130 | 2026-06-01 | 2 | 2 |
| 364901 | Twilight Small Dark Sky Friendly Outdoor Semi-F... | CAT6 | COL19 | 2026-01-01 | 1 | 1 |
| 364901 | Twilight Small Dark Sky Friendly Outdoor Semi-F... | CAT6 | COL19 | 2026-02-01 | 10 | 2 |
| 364901 | Twilight Small Dark Sky Friendly Outdoor Semi-F... | CAT6 | COL19 | 2026-03-01 | 2 | 1 |
| 364901 | Twilight Small Dark Sky Friendly Outdoor Semi-F... | CAT6 | COL19 | 2026-06-01 | 1 | 1 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2025-12-01 | 8 | 3 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2026-01-01 | 17 | 4 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2026-02-01 | 9 | 4 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2026-03-01 | 9 | 4 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2026-04-01 | 1 | 1 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2026-05-01 | 20 | 6 |
| 364903 | Twilight Dark Sky Friendly Outdoor Semi-Flush | CAT6 | COL19 | 2026-06-01 | 6 | 2 |
| 365203 | Dorset Dark Sky Friendly Outdoor Lantern | CAT6 | COL95 | 2025-12-01 | 7 | 4 |
| 365203 | Dorset Dark Sky Friendly Outdoor Lantern | CAT6 | COL95 | 2026-01-01 | 2 | 2 |
| 365203 | Dorset Dark Sky Friendly Outdoor Lantern | CAT6 | COL95 | 2026-02-01 | 1 | 1 |
| 365203 | Dorset Dark Sky Friendly Outdoor Lantern | CAT6 | COL95 | 2026-03-01 | 3 | 3 |
| 365203 | Dorset Dark Sky Friendly Outdoor Lantern | CAT6 | COL95 | 2026-04-01 | 6 | 3 |
| 365203 | Dorset Dark Sky Friendly Outdoor Lantern | CAT6 | COL95 | 2026-05-01 | 2 | 2 |
| 365213 | Davis Outdoor Lantern | CAT6 | DAVIS | 2026-01-01 | 2 | 2 |
| 365213 | Davis Outdoor Lantern | CAT6 | DAVIS | 2026-03-01 | 2 | 2 |
| 365605 | Meridian Outdoor Semi-Flush | CAT6 | COL131 | 2026-02-01 | 1 | 1 |
| 365605 | Meridian Outdoor Semi-Flush | CAT6 | COL131 | 2026-03-01 | 1 | 1 |
| 365605 | Meridian Outdoor Semi-Flush | CAT6 | COL131 | 2026-04-01 | 4 | 2 |
| 365605 | Meridian Outdoor Semi-Flush | CAT6 | COL131 | 2026-05-01 | 6 | 5 |
| 365605 | Meridian Outdoor Semi-Flush | CAT6 | COL131 | 2026-06-01 | 1 | 1 |
| 365610 | Meridian Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-02-01 | 4 | 1 |
| 365610 | Meridian Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-03-01 | 3 | 3 |
| 365610 | Meridian Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-04-01 | 2 | 1 |
| 365610 | Meridian Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-05-01 | 1 | 2 |
| 365610 | Meridian Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-06-01 | 5 | 2 |
| 365615 | Meridian Large Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-02-01 | 3 | 3 |
| 365615 | Meridian Large Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-03-01 | 1 | 1 |
| 365615 | Meridian Large Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-04-01 | 4 | 3 |
| 365615 | Meridian Large Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-05-01 | 1 | 1 |
| 365615 | Meridian Large Outdoor Ceiling Fixture | CAT6 | COL131 | 2026-06-01 | 7 | 4 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2025-12-01 | 1 | 1 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2026-01-01 | 3 | 3 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2026-02-01 | 5 | 1 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2026-03-01 | 11 | 5 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2026-04-01 | 2 | 2 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2026-05-01 | 3 | 3 |
| 365650 | Province Outdoor Flush Mount | CAT6 | COL132 | 2026-06-01 | 10 | 5 |
| 365892 | — | — | — | 2026-04-01 | 1 | 1 |
| 365894 | Banded Large Outdoor Fixture | CAT6 | COL16 | 2025-12-01 | 1 | 1 |
| 365894 | Banded Large Outdoor Fixture | CAT6 | COL16 | 2026-02-01 | 2 | 2 |
| 365894 | Banded Large Outdoor Fixture | CAT6 | COL16 | 2026-03-01 | 4 | 4 |
| 365894 | Banded Large Outdoor Fixture | CAT6 | COL16 | 2026-04-01 | 1 | 1 |
| 365894 | Banded Large Outdoor Fixture | CAT6 | COL16 | 2026-05-01 | 1 | 1 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2025-12-01 | 4 | 2 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2026-01-01 | 3 | 3 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2026-02-01 | 1 | 1 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2026-03-01 | 4 | 4 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2026-04-01 | 7 | 6 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2026-05-01 | 1 | 1 |
| 366007 | Tourou Large Outdoor Ceiling Fixture | CAT6 | COL133 | 2026-06-01 | 1 | 1 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2025-12-01 | 7 | 2 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2026-01-01 | 5 | 2 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2026-02-01 | 5 | 4 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2026-03-01 | 3 | 2 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2026-04-01 | 1 | 1 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2026-05-01 | 3 | 3 |
| 369455 | Hibiscus Outdoor Pendant | CAT6 | COL61 | 2026-06-01 | 1 | 1 |
| 390006 | Pier Mount Outdoor | CAT6 | COL136 | 2026-02-01 | 1 | 1 |
| 390006 | Pier Mount Outdoor | CAT6 | COL136 | 2026-03-01 | 2 | 1 |
| 390006 | Pier Mount Outdoor | CAT6 | COL136 | 2026-04-01 | 2 | 1 |
| 390006 | Pier Mount Outdoor | CAT6 | COL136 | 2026-05-01 | 2 | 1 |
| 390011 | Pier Mount Outdoor | CAT6 | COL136 | 2025-12-01 | 8 | 3 |
| 390011 | Pier Mount Outdoor | CAT6 | COL136 | 2026-01-01 | 22 | 3 |
| 390011 | Pier Mount Outdoor | CAT6 | COL136 | 2026-03-01 | 8 | 4 |
| 390011 | Pier Mount Outdoor | CAT6 | COL136 | 2026-04-01 | 11 | 5 |
| 390011 | Pier Mount Outdoor | CAT6 | COL136 | 2026-05-01 | 20 | 4 |
| 390011 | Pier Mount Outdoor | CAT6 | COL136 | 2026-06-01 | 15 | 5 |
| 390013 | Pier Mount Outdoor | CAT6 | COL136 | 2025-12-01 | 0 | 1 |
| 390013 | Pier Mount Outdoor | CAT6 | COL136 | 2026-01-01 | 3 | 1 |
| 390013 | Pier Mount Outdoor | CAT6 | COL136 | 2026-02-01 | 2 | 1 |
| 390013 | Pier Mount Outdoor | CAT6 | COL136 | 2026-03-01 | 15 | 6 |
| 390013 | Pier Mount Outdoor | CAT6 | COL136 | 2026-04-01 | 4 | 1 |
| 390013 | Pier Mount Outdoor | CAT6 | COL136 | 2026-05-01 | 12 | 7 |
| 390019 | Cover Cap Outdoor | CAT6 | COL137 | 2026-01-01 | 2 | 1 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2025-12-01 | 6 | 2 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2026-01-01 | 38 | 8 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2026-02-01 | 12 | 5 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2026-03-01 | 2 | 2 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2026-04-01 | 13 | 7 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2026-05-01 | 47 | 9 |
| 390020 | Cover Cap Outdoor | CAT6 | COL137 | 2026-06-01 | 13 | 4 |
| 390025 | Cover Cap Outdoor | CAT6 | COL137 | 2025-12-01 | 5 | 3 |
| 390025 | Cover Cap Outdoor | CAT6 | COL137 | 2026-02-01 | 5 | 2 |
| 390025 | Cover Cap Outdoor | CAT6 | COL137 | 2026-03-01 | 8 | 3 |
| 390025 | Cover Cap Outdoor | CAT6 | COL137 | 2026-04-01 | 1 | 1 |
| 390025 | Cover Cap Outdoor | CAT6 | COL137 | 2026-05-01 | 9 | 3 |
| 390047 | Square Post Outdoor | CAT6 | COL30 | 2026-01-01 | 0 | 1 |
| 390047 | Square Post Outdoor | CAT6 | COL30 | 2026-04-01 | 1 | 1 |
| 390123 | Square Post Outdoor | CAT6 | COL30 | 2026-02-01 | 1 | 1 |
| 390123 | Square Post Outdoor | CAT6 | COL30 | 2026-03-01 | 1 | 1 |
| 390123 | Square Post Outdoor | CAT6 | COL30 | 2026-06-01 | 1 | 1 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2025-12-01 | 1 | 1 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2026-01-01 | 4 | 3 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2026-02-01 | 8 | 2 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2026-03-01 | 6 | 6 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2026-04-01 | 4 | 4 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2026-05-01 | 16 | 4 |
| 390171 | Square Outdoor Post | CAT6 | COL30 | 2026-06-01 | 3 | 2 |
| 390172 | 7' Square Outdoor Post | CAT6 | COL146 | 2025-12-01 | 1 | 1 |
| 390172 | 7' Square Outdoor Post | CAT6 | COL146 | 2026-02-01 | 2 | 1 |
| 390172 | 7' Square Outdoor Post | CAT6 | COL146 | 2026-05-01 | 1 | 1 |
| 390172 | 7' Square Outdoor Post | CAT6 | COL146 | 2026-06-01 | 1 | 1 |
| 390240 | 2.5" Square to 3" Round Post Adapter | CAT6 | COL146 | 2026-02-01 | 9 | 3 |
| 390240 | 2.5" Square to 3" Round Post Adapter | CAT6 | COL146 | 2026-03-01 | 1 | 1 |
| 390240 | 2.5" Square to 3" Round Post Adapter | CAT6 | COL146 | 2026-04-01 | 5 | 6 |
| 390240 | 2.5" Square to 3" Round Post Adapter | CAT6 | COL146 | 2026-05-01 | 8 | 4 |
| 390240 | 2.5" Square to 3" Round Post Adapter | CAT6 | COL146 | 2026-06-01 | 13 | 3 |
| 390271 | Round Outdoor Post | CAT6 | COL138 | 2025-12-01 | 7 | 3 |
| 390271 | Round Outdoor Post | CAT6 | COL138 | 2026-02-01 | 5 | 3 |
| 390271 | Round Outdoor Post | CAT6 | COL138 | 2026-03-01 | 12 | 3 |
| 390271 | Round Outdoor Post | CAT6 | COL138 | 2026-04-01 | 1 | 1 |
| 390271 | Round Outdoor Post | CAT6 | COL138 | 2026-05-01 | 6 | 2 |
| 390271 | Round Outdoor Post | CAT6 | COL138 | 2026-06-01 | 2 | 1 |
| 390272 | 7' Round Outdoor Post | CAT6 | COL146 | 2026-01-01 | 15 | 4 |
| 390272 | 7' Round Outdoor Post | CAT6 | COL146 | 2026-02-01 | 1 | 1 |
| 390272 | 7' Round Outdoor Post | CAT6 | COL146 | 2026-03-01 | 2 | 2 |
| 390272 | 7' Round Outdoor Post | CAT6 | COL146 | 2026-04-01 | 1 | 2 |
| 390272 | 7' Round Outdoor Post | CAT6 | COL146 | 2026-05-01 | 1 | 1 |
| 390272 | 7' Round Outdoor Post | CAT6 | COL146 | 2026-06-01 | 1 | 1 |
| 401213 | Lustra Flush Mount/Sconce | CAT2 | COL151 | 2026-01-01 | 3 | 2 |
| 401213 | Lustra Flush Mount/Sconce | CAT2 | COL151 | 2026-02-01 | 1 | 1 |
| 401213 | Lustra Flush Mount/Sconce | CAT2 | COL151 | 2026-04-01 | 1 | 1 |
| 401213 | Lustra Flush Mount/Sconce | CAT2 | COL151 | 2026-05-01 | 4 | 3 |
| 401234 | Fusion Semi-Flush | CAT2 | COL139 | 2026-01-01 | 1 | 1 |
| 401234 | Fusion Semi-Flush | CAT2 | COL139 | 2026-04-01 | 1 | 1 |
| 401310 | Brutus Pendant | CAT1 | COL140 | 2026-01-01 | 1 | 1 |
| 401310 | Brutus Pendant | CAT1 | COL140 | 2026-03-01 | 2 | 2 |
| 401310 | Brutus Pendant | CAT1 | COL140 | 2026-05-01 | 1 | 1 |
| 401311 | Brutus Large Pendant | CAT1 | COL140 | 2026-01-01 | 1 | 1 |
| 401311 | Brutus Large Pendant | CAT1 | COL140 | 2026-02-01 | 1 | 1 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2025-12-01 | 1 | 1 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2026-01-01 | 4 | 4 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2026-02-01 | 10 | 5 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2026-03-01 | 5 | 4 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2026-04-01 | 2 | 2 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2026-05-01 | 1 | 1 |
| 401315 | SNAPS Medium LED Pendant | CAT1 | SNAPS | 2026-06-01 | 2 | 2 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2025-12-01 | 1 | 1 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2026-01-01 | 2 | 2 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2026-02-01 | 3 | 3 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2026-03-01 | 6 | 7 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2026-04-01 | 4 | 4 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2026-05-01 | 1 | 1 |
| 401316 | SNAPS Large LED Pendant | CAT1 | SNAPS | 2026-06-01 | 3 | 3 |
| 401319 | Veneto 5-Light Linear Pendant | CAT1 | COL141 | 2025-12-01 | 1 | 1 |
| 401319 | Veneto 5-Light Linear Pendant | CAT1 | COL141 | 2026-01-01 | 1 | 1 |
| 401319 | Veneto 5-Light Linear Pendant | CAT1 | COL141 | 2026-02-01 | 1 | 1 |
| 401319 | Veneto 5-Light Linear Pendant | CAT1 | COL141 | 2026-03-01 | 2 | 2 |
| 401319 | Veneto 5-Light Linear Pendant | CAT1 | COL141 | 2026-05-01 | 1 | 1 |
| 401320 | Aspen Small LED Lantern | CAT1 | ASPEN | 2025-12-01 | 2 | 1 |
| 401320 | Aspen Small LED Lantern | CAT1 | ASPEN | 2026-01-01 | 2 | 2 |
| 401320 | Aspen Small LED Lantern | CAT1 | ASPEN | 2026-02-01 | 2 | 2 |
| 401320 | Aspen Small LED Lantern | CAT1 | ASPEN | 2026-03-01 | 3 | 3 |
| 401320 | Aspen Small LED Lantern | CAT1 | ASPEN | 2026-04-01 | 6 | 2 |
| 401320 | Aspen Small LED Lantern | CAT1 | ASPEN | 2026-06-01 | 1 | 1 |
| 401321 | Aspen Large LED Lantern | CAT1 | ASPEN | 2026-01-01 | 4 | 3 |
| 401321 | Aspen Large LED Lantern | CAT1 | ASPEN | 2026-02-01 | 12 | 9 |
| 401321 | Aspen Large LED Lantern | CAT1 | ASPEN | 2026-03-01 | 8 | 6 |
| 401321 | Aspen Large LED Lantern | CAT1 | ASPEN | 2026-04-01 | 9 | 4 |
| 401321 | Aspen Large LED Lantern | CAT1 | ASPEN | 2026-05-01 | 6 | 4 |
| 401322 | SNAPS Large LED Pendant w/Metal Cones | CAT1 | SNAPS | 2026-03-01 | 3 | 4 |
| 401326 | Coral LED Pendant | CAT1 | CORAL | 2026-01-01 | 4 | 4 |
| 401326 | Coral LED Pendant | CAT1 | CORAL | 2026-02-01 | 2 | 2 |
| 401326 | Coral LED Pendant | CAT1 | CORAL | 2026-03-01 | 1 | 1 |
| 401326 | Coral LED Pendant | CAT1 | CORAL | 2026-04-01 | 3 | 3 |
| 401326 | Coral LED Pendant | CAT1 | CORAL | 2026-05-01 | 3 | 2 |
| 401326 | Coral LED Pendant | CAT1 | CORAL | 2026-06-01 | 2 | 2 |
| 401328 | Fusion Large Pendant | CAT1 | COL139 | 2026-01-01 | 2 | 2 |
| 401328 | Fusion Large Pendant | CAT1 | COL139 | 2026-02-01 | 1 | 1 |
| 401328 | Fusion Large Pendant | CAT1 | COL139 | 2026-03-01 | 1 | 1 |
| 401330 | Coral LED Ring Pendant | CAT1 | CORAL | 2026-01-01 | 2 | 2 |
| 401330 | Coral LED Ring Pendant | CAT1 | CORAL | 2026-02-01 | 2 | 2 |
| 401330 | Coral LED Ring Pendant | CAT1 | CORAL | 2026-03-01 | 2 | 2 |
| 401330 | Coral LED Ring Pendant | CAT1 | CORAL | 2026-04-01 | 2 | 2 |
| 401330 | Coral LED Ring Pendant | CAT1 | CORAL | 2026-06-01 | 1 | 1 |
| 401347 | Fusion Pendant | CAT1 | COL139 | 2026-01-01 | 2 | 2 |
| 401347 | Fusion Pendant | CAT1 | COL139 | 2026-02-01 | 2 | 2 |
| 401347 | Fusion Pendant | CAT1 | COL139 | 2026-03-01 | 1 | 1 |
| 401347 | Fusion Pendant | CAT1 | COL139 | 2026-04-01 | 2 | 2 |
| 401349 | Stacks 6-Light LED Pendant | CAT1 | COL142 | 2026-01-01 | 1 | 1 |
| 401349 | Stacks 6-Light LED Pendant | CAT1 | COL142 | 2026-02-01 | 2 | 2 |
| 401349 | Stacks 6-Light LED Pendant | CAT1 | COL142 | 2026-03-01 | 1 | 1 |
| 401349 | Stacks 6-Light LED Pendant | CAT1 | COL142 | 2026-04-01 | 1 | 1 |
| 401358 | Fold LED Pendant | CAT1 | FOLD | 2026-01-01 | 1 | 1 |
| 401358 | Fold LED Pendant | CAT1 | FOLD | 2026-03-01 | 2 | 2 |
| 401358 | Fold LED Pendant | CAT1 | FOLD | 2026-05-01 | 1 | 1 |
| 401374 | Ingot LED Pendant | CAT1 | INGOT | 2026-01-01 | 1 | 1 |
| 401374 | Ingot LED Pendant | CAT1 | INGOT | 2026-02-01 | 1 | 1 |
| 401374 | Ingot LED Pendant | CAT1 | INGOT | 2026-03-01 | 2 | 2 |
| 401374 | Ingot LED Pendant | CAT1 | INGOT | 2026-05-01 | 2 | 1 |
| 401848 | SNAPS Single LED 45º Pendant w/Metal Cone | CAT13 | SNAPS | 2026-01-01 | 1 | 1 |
| 401848 | SNAPS Single LED 45º Pendant w/Metal Cone | CAT13 | SNAPS | 2026-02-01 | 1 | 1 |
| 401850 | SNAPS Small LED Pendant | CAT13 | SNAPS | 2026-01-01 | 1 | 1 |
| 401850 | SNAPS Small LED Pendant | CAT13 | SNAPS | 2026-03-01 | 5 | 3 |
| 401850 | SNAPS Small LED Pendant | CAT13 | SNAPS | 2026-05-01 | 9 | 3 |
| 401850 | SNAPS Small LED Pendant | CAT13 | SNAPS | 2026-06-01 | 4 | 1 |
| 401851 | Veneto 1-Light Pendant | CAT13 | COL141 | 2025-12-01 | 2 | 1 |
| 401851 | Veneto 1-Light Pendant | CAT13 | COL141 | 2026-01-01 | 1 | 1 |
| 401851 | Veneto 1-Light Pendant | CAT13 | COL141 | 2026-02-01 | 7 | 5 |
| 401851 | Veneto 1-Light Pendant | CAT13 | COL141 | 2026-03-01 | 11 | 5 |
| 401851 | Veneto 1-Light Pendant | CAT13 | COL141 | 2026-06-01 | 2 | 2 |
| 401854 | Stacks LED Pendant | CAT13 | COL142 | 2026-01-01 | 1 | 1 |
| 401854 | Stacks LED Pendant | CAT13 | COL142 | 2026-05-01 | 5 | 1 |
| 401854 | Stacks LED Pendant | CAT13 | COL142 | 2026-06-01 | 2 | 2 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2025-12-01 | 1 | 1 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2026-01-01 | 2 | 2 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2026-02-01 | 5 | 3 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2026-03-01 | 3 | 2 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2026-04-01 | 4 | 2 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2026-05-01 | 2 | 1 |
| 402030 | Veneto Sconce | CAT15 | COL141 | 2026-06-01 | 6 | 2 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2025-12-01 | 2 | 1 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2026-01-01 | 5 | 3 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2026-02-01 | 4 | 2 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2026-03-01 | 6 | 3 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2026-04-01 | 6 | 4 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2026-05-01 | 2 | 1 |
| 402031 | SNAPS LED Sconce | CAT15 | SNAPS | 2026-06-01 | 4 | 2 |
| 402032 | SNAPS 3-Light Sconce | CAT15 | SNAPS | 2026-01-01 | 3 | 3 |
| 402032 | SNAPS 3-Light Sconce | CAT15 | SNAPS | 2026-02-01 | 1 | 1 |
| 402032 | SNAPS 3-Light Sconce | CAT15 | SNAPS | 2026-03-01 | 2 | 2 |
| 402032 | SNAPS 3-Light Sconce | CAT15 | SNAPS | 2026-04-01 | 3 | 2 |
| 402032 | SNAPS 3-Light Sconce | CAT15 | SNAPS | 2026-06-01 | 7 | 2 |
| 402035 | Brutus Sconce | CAT15 | COL140 | 2026-03-01 | 1 | 1 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2025-12-01 | 2 | 1 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2026-01-01 | 35 | 9 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2026-02-01 | 11 | 9 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2026-03-01 | 5 | 4 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2026-04-01 | 4 | 2 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2026-05-01 | 2 | 3 |
| 402036 | Coral Sconce | CAT15 | CORAL | 2026-06-01 | 4 | 2 |
| 402040 | Lustra Sconce/Flush Mount | CAT15 | COL151 | 2026-01-01 | 8 | 8 |
| 402040 | Lustra Sconce/Flush Mount | CAT15 | COL151 | 2026-02-01 | 7 | 6 |
| 402040 | Lustra Sconce/Flush Mount | CAT15 | COL151 | 2026-03-01 | 2 | 2 |
| 402040 | Lustra Sconce/Flush Mount | CAT15 | COL151 | 2026-04-01 | 9 | 3 |
| 402040 | Lustra Sconce/Flush Mount | CAT15 | COL151 | 2026-05-01 | 4 | 2 |
| 402064 | Stacks LED Sconce | CAT15 | COL142 | 2026-02-01 | 2 | 2 |
| 402064 | Stacks LED Sconce | CAT15 | COL142 | 2026-03-01 | 1 | 1 |
| 402064 | Stacks LED Sconce | CAT15 | COL142 | 2026-05-01 | 3 | 2 |
| 402749 | Coral Table Lamp | CAT5 | CORAL | 2025-12-01 | 8 | 4 |
| 402749 | Coral Table Lamp | CAT5 | CORAL | 2026-01-01 | 3 | 2 |
| 402749 | Coral Table Lamp | CAT5 | CORAL | 2026-02-01 | 5 | 4 |
| 402749 | Coral Table Lamp | CAT5 | CORAL | 2026-03-01 | 1 | 1 |
| 402749 | Coral Table Lamp | CAT5 | CORAL | 2026-05-01 | 2 | 2 |
| 402801 | SNAPS Floor-to-Ceiling Plug-in LED Lamp | CAT1 | SNAPS | 2026-04-01 | 1 | 1 |
| 402801 | SNAPS Floor-to-Ceiling Plug-in LED Lamp | CAT1 | SNAPS | 2026-05-01 | 1 | 1 |
| 402801 | SNAPS Floor-to-Ceiling Plug-in LED Lamp | CAT1 | SNAPS | 2026-06-01 | 1 | 1 |
| 403016 | Fusion Small LED Sconce | CAT15 | COL139 | 2025-12-01 | 1 | 1 |
| 403016 | Fusion Small LED Sconce | CAT15 | COL139 | 2026-03-01 | 2 | 1 |
| 403046 | Procession Arch Small Outdoor Sconce | CAT6 | COL143 | 2026-01-01 | 6 | 1 |
| 403046 | Procession Arch Small Outdoor Sconce | CAT6 | COL143 | 2026-02-01 | 8 | 1 |
| 403046 | Procession Arch Small Outdoor Sconce | CAT6 | COL143 | 2026-04-01 | 1 | 1 |
| 403046 | Procession Arch Small Outdoor Sconce | CAT6 | COL143 | 2026-05-01 | 2 | 1 |
| 403052 | Procession Small Outdoor Sconce | CAT6 | COL143 | 2025-12-01 | 3 | 1 |
| 403052 | Procession Small Outdoor Sconce | CAT6 | COL143 | 2026-01-01 | 2 | 1 |
| 403052 | Procession Small Outdoor Sconce | CAT6 | COL143 | 2026-03-01 | 17 | 2 |
| 403052 | Procession Small Outdoor Sconce | CAT6 | COL143 | 2026-04-01 | 6 | 2 |
| 403052 | Procession Small Outdoor Sconce | CAT6 | COL143 | 2026-05-01 | 6 | 1 |
| 403061 | Procession Large Outdoor Sconce | CAT6 | COL143 | 2026-01-01 | 1 | 1 |
| 403061 | Procession Large Outdoor Sconce | CAT6 | COL143 | 2026-02-01 | 2 | 2 |
| 403061 | Procession Large Outdoor Sconce | CAT6 | COL143 | 2026-03-01 | 2 | 2 |
| 403061 | Procession Large Outdoor Sconce | CAT6 | COL143 | 2026-04-01 | 2 | 1 |
| 403061 | Procession Large Outdoor Sconce | CAT6 | COL143 | 2026-05-01 | 3 | 2 |
| 403061 | Procession Large Outdoor Sconce | CAT6 | COL143 | 2026-06-01 | 10 | 2 |
| 403082 | Fusion Large LED Sconce | CAT15 | COL139 | 2026-01-01 | 1 | 1 |
| 403082 | Fusion Large LED Sconce | CAT15 | COL139 | 2026-02-01 | 2 | 2 |
| 403082 | Fusion Large LED Sconce | CAT15 | COL139 | 2026-03-01 | 1 | 1 |
| 403082 | Fusion Large LED Sconce | CAT15 | COL139 | 2026-04-01 | 1 | 1 |
| 403087 | Procession Arch Large Outdoor Sconce | CAT6 | COL143 | 2025-12-01 | 2 | 1 |
| 403087 | Procession Arch Large Outdoor Sconce | CAT6 | COL143 | 2026-02-01 | 2 | 1 |
| 403087 | Procession Arch Large Outdoor Sconce | CAT6 | COL143 | 2026-03-01 | 2 | 1 |
| 403087 | Procession Arch Large Outdoor Sconce | CAT6 | COL143 | 2026-06-01 | 9 | 2 |
| 451971 | — | — | — | 2026-01-01 | 1 | 1 |
| 451987 | — | — | — | 2026-04-01 | 2 | 2 |
| 451987 | — | — | — | 2026-05-01 | 3 | 2 |
| 451990 | — | — | — | 2026-02-01 | 1 | 1 |
| 451990 | — | — | — | 2026-04-01 | 1 | 1 |
| 451990 | — | — | — | 2026-05-01 | 1 | 1 |
| 451992 | — | — | — | 2026-06-01 | 2 | 1 |
| 451995 | — | — | — | 2026-01-01 | 1 | 1 |
| 451997 | — | — | — | 2026-05-01 | 1 | 1 |
| 451999 | — | — | — | 2026-05-01 | 1 | 1 |
| 45859 | — | — | — | 2026-03-01 | 1 | 1 |
| 49911 | — | — | — | 2026-01-01 | 4 | 4 |
| 49911 | — | — | — | 2026-02-01 | 4 | 4 |
| 49911 | — | — | — | 2026-03-01 | 7 | 6 |
| 49911 | — | — | — | 2026-04-01 | 2 | 2 |
| 49911 | — | — | — | 2026-05-01 | 5 | 3 |
| 49911 | — | — | — | 2026-06-01 | 2 | 1 |
| 49912 | — | — | — | 2025-12-01 | 1 | 1 |
| 49912 | — | — | — | 2026-01-01 | 7 | 6 |
| 49912 | — | — | — | 2026-02-01 | 7 | 6 |
| 49912 | — | — | — | 2026-03-01 | 8 | 5 |
| 49912 | — | — | — | 2026-04-01 | 1 | 1 |
| 49912 | — | — | — | 2026-05-01 | 3 | 3 |
| 49912 | — | — | — | 2026-06-01 | 3 | 2 |
| 49913 | — | — | — | 2025-12-01 | 1 | 1 |
| 49913 | — | — | — | 2026-01-01 | 3 | 3 |
| 49913 | — | — | — | 2026-02-01 | 3 | 3 |
| 49913 | — | — | — | 2026-03-01 | 2 | 2 |
| 49913 | — | — | — | 2026-04-01 | 1 | 1 |
| 49913 | — | — | — | 2026-05-01 | 4 | 3 |
| 49913 | — | — | — | 2026-06-01 | 1 | 1 |
| 49914 | — | — | — | 2025-12-01 | 3 | 3 |
| 49914 | — | — | — | 2026-01-01 | 7 | 6 |
| 49914 | — | — | — | 2026-02-01 | 11 | 9 |
| 49914 | — | — | — | 2026-03-01 | 9 | 8 |
| 49914 | — | — | — | 2026-04-01 | 4 | 3 |
| 49914 | — | — | — | 2026-05-01 | 12 | 3 |
| 49914 | — | — | — | 2026-06-01 | 3 | 2 |
| 49915 | — | — | — | 2025-12-01 | 1 | 1 |
| 49915 | — | — | — | 2026-01-01 | 2 | 2 |
| 49915 | — | — | — | 2026-02-01 | 4 | 4 |
| 49915 | — | — | — | 2026-03-01 | 1 | 1 |
| 49915 | — | — | — | 2026-06-01 | 1 | 1 |
| 49916 | — | — | — | 2026-01-01 | 2 | 1 |
| 49916 | — | — | — | 2026-02-01 | 2 | 2 |
| 49916 | — | — | — | 2026-03-01 | 2 | 2 |
| 49916 | — | — | — | 2026-04-01 | 2 | 1 |
| 49916 | — | — | — | 2026-06-01 | 1 | 1 |
| 49917 | — | — | — | 2026-02-01 | 3 | 2 |
| 49917 | — | — | — | 2026-03-01 | 2 | 2 |
| 49917 | — | — | — | 2026-04-01 | 2 | 1 |
| 49917 | — | — | — | 2026-06-01 | 3 | 2 |
| 49918 | — | — | — | 2026-01-01 | 1 | 1 |
| 49918 | — | — | — | 2026-02-01 | 1 | 1 |
| 49918 | — | — | — | 2026-06-01 | 1 | 1 |
| 49919 | — | — | — | 2026-01-01 | 1 | 1 |
| 49919 | — | — | — | 2026-02-01 | 7 | 5 |
| 49919 | — | — | — | 2026-03-01 | 2 | 2 |
| 49919 | — | — | — | 2026-04-01 | 1 | 1 |
| 49919 | — | — | — | 2026-05-01 | 1 | 1 |
| 49919 | — | — | — | 2026-06-01 | 3 | 3 |
| 49920 | — | — | — | 2025-12-01 | 1 | 1 |
| 49920 | — | — | — | 2026-01-01 | 3 | 2 |
| 49920 | — | — | — | 2026-02-01 | 7 | 5 |
| 49920 | — | — | — | 2026-03-01 | 6 | 5 |
| 49920 | — | — | — | 2026-04-01 | 3 | 3 |
| 49920 | — | — | — | 2026-05-01 | 11 | 2 |
| 49921 | — | — | — | 2026-02-01 | 1 | 1 |
| 49921 | — | — | — | 2026-03-01 | 1 | 1 |
| 49921 | — | — | — | 2026-05-01 | 2 | 2 |
| 49922 | — | — | — | 2025-12-01 | 4 | 3 |
| 49922 | — | — | — | 2026-01-01 | 6 | 5 |
| 49922 | — | — | — | 2026-02-01 | 2 | 2 |
| 49922 | — | — | — | 2026-03-01 | 8 | 6 |
| 49922 | — | — | — | 2026-04-01 | 4 | 4 |
| 49922 | — | — | — | 2026-05-01 | 11 | 2 |
| 49922 | — | — | — | 2026-06-01 | 1 | 1 |
| 49932 | — | — | — | 2026-01-01 | 3 | 2 |
| 49932 | — | — | — | 2026-02-01 | 1 | 1 |
| 49932 | — | — | — | 2026-04-01 | 1 | 1 |
| 49932 | — | — | — | 2026-05-01 | 1 | 1 |
| 49932 | — | — | — | 2026-06-01 | 2 | 2 |
| 49933 | — | — | — | 2026-01-01 | 3 | 3 |
| 49933 | — | — | — | 2026-02-01 | 1 | 1 |
| 49933 | — | — | — | 2026-03-01 | 4 | 3 |
| 49933 | — | — | — | 2026-04-01 | 1 | 1 |
| 49933 | — | — | — | 2026-05-01 | 2 | 2 |
| 49933 | — | — | — | 2026-06-01 | 6 | 5 |
| 49934 | — | — | — | 2025-12-01 | 1 | 1 |
| 49934 | — | — | — | 2026-01-01 | 3 | 3 |
| 49934 | — | — | — | 2026-02-01 | 2 | 2 |
| 49934 | — | — | — | 2026-03-01 | 3 | 3 |
| 49934 | — | — | — | 2026-05-01 | 1 | 1 |
| 49934 | — | — | — | 2026-06-01 | 5 | 4 |
| 49941 | — | — | — | 2026-01-01 | 1 | 1 |
| 49941 | — | — | — | 2026-02-01 | 1 | 1 |
| 49941 | — | — | — | 2026-03-01 | 2 | 2 |
| 49941 | — | — | — | 2026-04-01 | 2 | 2 |
| 49941 | — | — | — | 2026-05-01 | 2 | 1 |
| 49941 | — | — | — | 2026-06-01 | 2 | 1 |
| 49942 | — | — | — | 2026-01-01 | 1 | 1 |
| 49942 | — | — | — | 2026-04-01 | 2 | 2 |
| 49942 | — | — | — | 2026-05-01 | 2 | 2 |
| 49942 | — | — | — | 2026-06-01 | 1 | 1 |
| 49943 | — | — | — | 2026-01-01 | 1 | 1 |
| 49943 | — | — | — | 2026-02-01 | 2 | 2 |
| 49943 | — | — | — | 2026-03-01 | 2 | 2 |
| 49943 | — | — | — | 2026-04-01 | 1 | 1 |
| 49943 | — | — | — | 2026-05-01 | 1 | 1 |
| 49943 | — | — | — | 2026-06-01 | 1 | 1 |
| 49951 | — | — | — | 2026-02-01 | 1 | 1 |
| 49952 | — | — | — | 2026-02-01 | 1 | 1 |
| 49953 | — | — | — | 2026-01-01 | 1 | 1 |
| 49953 | — | — | — | 2026-02-01 | 1 | 1 |
| 50511 | — | — | — | 2025-12-01 | 10 | 6 |
| 50511 | — | — | — | 2026-01-01 | 59 | 42 |
| 50511 | — | — | — | 2026-02-01 | 69 | 35 |
| 50511 | — | — | — | 2026-03-01 | 48 | 27 |
| 50511 | — | — | — | 2026-04-01 | 81 | 31 |
| 50511 | — | — | — | 2026-05-01 | 82 | 34 |
| 50511 | — | — | — | 2026-06-01 | 52 | 21 |
| 50536 | — | — | — | 2026-03-01 | 1 | 1 |
| 50536 | — | — | — | 2026-04-01 | 1 | 1 |
| 50537 | — | — | — | 2026-01-01 | 1 | 1 |
| 50537 | — | — | — | 2026-02-01 | 3 | 3 |
| 50537 | — | — | — | 2026-03-01 | 3 | 3 |
| 50537 | — | — | — | 2026-04-01 | 6 | 2 |
| 50537 | — | — | — | 2026-05-01 | 1 | 2 |
| 710004 | Beveled Oval Mirror | CAT17 | COL144 | 2026-01-01 | 2 | 2 |
| 710004 | Beveled Oval Mirror | CAT17 | COL144 | 2026-02-01 | 4 | 3 |
| 710004 | Beveled Oval Mirror | CAT17 | COL144 | 2026-03-01 | 3 | 3 |
| 710004 | Beveled Oval Mirror | CAT17 | COL144 | 2026-04-01 | 2 | 2 |
| 710004 | Beveled Oval Mirror | CAT17 | COL144 | 2026-05-01 | 8 | 6 |
| 710004 | Beveled Oval Mirror | CAT17 | COL144 | 2026-06-01 | 2 | 2 |
| 710014 | Beveled Oval Mirror with Leaf | CAT17 | COL144 | 2025-12-01 | 1 | 1 |
| 710014 | Beveled Oval Mirror with Leaf | CAT17 | COL144 | 2026-01-01 | 2 | 2 |
| 710014 | Beveled Oval Mirror with Leaf | CAT17 | COL144 | 2026-03-01 | 1 | 1 |
| 710014 | Beveled Oval Mirror with Leaf | CAT17 | COL144 | 2026-04-01 | 1 | 1 |
| 710014 | Beveled Oval Mirror with Leaf | CAT17 | COL144 | 2026-05-01 | 1 | 1 |
| 710014 | Beveled Oval Mirror with Leaf | CAT17 | COL144 | 2026-06-01 | 2 | 2 |
| 710116 | Metra Beveled Mirror | CAT17 | METRA | 2026-01-01 | 1 | 1 |
| 710116 | Metra Beveled Mirror | CAT17 | METRA | 2026-03-01 | 1 | 1 |
| 710116 | Metra Beveled Mirror | CAT17 | METRA | 2026-05-01 | 3 | 2 |
| 710118 | Metra Large Beveled Mirror | CAT17 | COL144 | 2026-01-01 | 1 | 1 |
| 710118 | Metra Large Beveled Mirror | CAT17 | COL144 | 2026-02-01 | 1 | 1 |
| 710118 | Metra Large Beveled Mirror | CAT17 | COL144 | 2026-03-01 | 5 | 4 |
| 710118 | Metra Large Beveled Mirror | CAT17 | COL144 | 2026-04-01 | 3 | 2 |
| 710118 | Metra Large Beveled Mirror | CAT17 | COL144 | 2026-05-01 | 3 | 2 |
| 714901 | Rook Beveled Mirror | CAT17 | ROOK | 2025-12-01 | 1 | 1 |
| 714901 | Rook Beveled Mirror | CAT17 | ROOK | 2026-01-01 | 2 | 2 |
| 714901 | Rook Beveled Mirror | CAT17 | ROOK | 2026-04-01 | 1 | 1 |
| 750102 | Wick Side Table | CAT17 | WICK | 2026-03-01 | 2 | 1 |
| 750102 | Wick Side Table | CAT17 | WICK | 2026-05-01 | 1 | 1 |
| 750104 | Wick 30" Console Table | CAT17 | WICK | 2025-12-01 | 2 | 2 |
| 750104 | Wick 30" Console Table | CAT17 | WICK | 2026-01-01 | 3 | 3 |
| 750104 | Wick 30" Console Table | CAT17 | WICK | 2026-02-01 | 2 | 2 |
| 750104 | Wick 30" Console Table | CAT17 | WICK | 2026-03-01 | 1 | 1 |
| 750104 | Wick 30" Console Table | CAT17 | WICK | 2026-05-01 | 2 | 3 |
| 750104 | Wick 30" Console Table | CAT17 | WICK | 2026-06-01 | 1 | 1 |
| 750106 | Wick 42" Console Table | CAT17 | WICK | 2026-05-01 | 3 | 2 |
| 750108 | Wick 60" Console Table | CAT17 | WICK | 2026-05-01 | 1 | 1 |
| 750111 | Brindille Wood Top Accent Table | CAT17 | COL24 | 2026-03-01 | 2 | 1 |
| 750112 | Brindille Console Table | CAT17 | COL24 | 2026-02-01 | 1 | 1 |
| 750113 | Brindille Wood Top Console Table | CAT17 | COL24 | 2026-02-01 | 1 | 1 |
| 750117 | — | — | — | 2025-12-01 | 1 | 1 |
| 750117 | — | — | — | 2026-05-01 | 1 | 1 |
| 750118 | Equus Console Table | CAT17 | EQUUS | 2026-02-01 | 1 | 1 |
| 750119 | — | — | — | 2025-12-01 | 1 | 1 |
| 750119 | — | — | — | 2026-01-01 | 1 | 1 |
| 750123 | Crux Coffee Table w/Wood Legs | CAT17 | CRUX | 2025-12-01 | 1 | 1 |
| 750127 | Cove Marble Top Console Table | CAT17 | COVE | 2026-02-01 | 1 | 1 |
| 750133 | Olympus Glass Top Accent Table | CAT17 | COL7 | 2026-03-01 | 2 | 1 |
| 750133 | Olympus Glass Top Accent Table | CAT17 | COL7 | 2026-05-01 | 1 | 1 |
| 750134 | Olympus Wood Top Accent Table | CAT17 | COL7 | 2026-03-01 | 2 | 1 |
| 857300 | — | — | — | 2025-12-01 | 2 | 2 |
| 857300 | — | — | — | 2026-01-01 | 4 | 3 |
| 857300 | — | — | — | 2026-02-01 | 4 | 4 |
| 857300 | — | — | — | 2026-03-01 | 5 | 5 |
| 857300 | — | — | — | 2026-04-01 | 2 | 2 |
| 857300 | — | — | — | 2026-05-01 | 3 | 3 |
| 857300 | — | — | — | 2026-06-01 | 1 | 1 |
| 859223 | — | — | — | 2026-01-01 | 1 | 1 |
| 859226 | — | — | — | 2026-06-01 | 1 | 1 |
| 890540 | — | — | — | 2025-12-01 | 7 | 2 |
| 890540 | — | — | — | 2026-01-01 | 12 | 7 |
| 890540 | — | — | — | 2026-02-01 | 48 | 13 |
| 890540 | — | — | — | 2026-03-01 | 56 | 29 |
| 890540 | — | — | — | 2026-04-01 | 14 | 5 |
| 890540 | — | — | — | 2026-05-01 | 42 | 9 |
| 890540 | — | — | — | 2026-06-01 | 18 | 4 |
| 890700 | Outdoor Post Display POP | CAT8 | COL145 | 2026-02-01 | 2 | 1 |
| 890700 | Outdoor Post Display POP | CAT8 | COL145 | 2026-03-01 | 1 | 1 |
| 890815 | Marketing Tool: 36" x 48" Sconce Board | CAT3 | COL20 | 2026-01-01 | 1 | 1 |
| 890815 | Marketing Tool: 36" x 48" Sconce Board | CAT3 | COL20 | 2026-03-01 | 4 | 1 |
| 890828 | Marketing Tool: Hubbardton Forge Warranty Logo ... | CAT3 | COL20 | 2026-01-01 | 2 | 1 |
| 890828 | Marketing Tool: Hubbardton Forge Warranty Logo ... | CAT3 | COL20 | 2026-02-01 | 6 | 3 |
| 890828 | Marketing Tool: Hubbardton Forge Warranty Logo ... | CAT3 | COL20 | 2026-05-01 | 2 | 1 |
| 890837 | Marketing Tool: 15" x 15" Hammer Graphic | CAT3 | COL20 | 2026-01-01 | 1 | 1 |
| 890837 | Marketing Tool: 15" x 15" Hammer Graphic | CAT3 | COL20 | 2026-03-01 | 1 | 1 |
| 890838 | Marketing Tool: 15" x 15" Fine Tuning Graphic | CAT3 | COL20 | 2026-01-01 | 1 | 1 |
| 890845 | Marketing Tool: 4" x 11", Hubbardton Forge, War... | CAT3 | COL20 | 2026-01-01 | 3 | 1 |
| 890845 | Marketing Tool: 4" x 11", Hubbardton Forge, War... | CAT3 | COL20 | 2026-05-01 | 1 | 1 |
| 890846 | Marketing Tool: 4" x 11", Hubbardton Forge, Out... | CAT3 | COL20 | 2026-05-01 | 1 | 1 |
| 890847 | Marketing Tool: Large Logo Vertical | CAT3 | COL20 | 2026-01-01 | 3 | 1 |
| 890847 | Marketing Tool: Large Logo Vertical | CAT3 | COL20 | 2026-02-01 | 1 | 1 |
| 890847 | Marketing Tool: Large Logo Vertical | CAT3 | COL20 | 2026-05-01 | 1 | 1 |
| 890848 | Marketing Tool: Large Logo Horizontal | CAT3 | COL20 | 2026-01-01 | 3 | 1 |
| 890848 | Marketing Tool: Large Logo Horizontal | CAT3 | COL20 | 2026-02-01 | 1 | 1 |
| 890848 | Marketing Tool: Large Logo Horizontal | CAT3 | COL20 | 2026-05-01 | 1 | 1 |
| 890851 | Marketing Tool: 15" x 15", Verbiage Panel | CAT3 | COL20 | 2026-01-01 | 3 | 1 |
| 890851 | Marketing Tool: 15" x 15", Verbiage Panel | CAT3 | COL20 | 2026-02-01 | 1 | 1 |
| 890851 | Marketing Tool: 15" x 15", Verbiage Panel | CAT3 | COL20 | 2026-03-01 | 1 | 1 |
| 890851 | Marketing Tool: 15" x 15", Verbiage Panel | CAT3 | COL20 | 2026-05-01 | 1 | 1 |
| 890854 | Marketing Tool: 15" x 15", Antasia Detail | CAT3 | COL20 | 2026-03-01 | 1 | 1 |
| 890857 | Marketing Tool: 15" x 15", Antasia II | CAT3 | COL20 | 2026-01-01 | 1 | 1 |
| 890868 | Marketing Tool: Map Wall Poster, 24" x 36" | CAT3 | COL20 | 2026-02-01 | 2 | 2 |
| 890870 | Marketing Tool: 8" x 12", Hubbardton Forge, Ext... | CAT3 | COL20 | 2026-01-01 | 4 | 2 |
| 890870 | Marketing Tool: 8" x 12", Hubbardton Forge, Ext... | CAT3 | COL20 | 2026-02-01 | 4 | 3 |
| 890870 | Marketing Tool: 8" x 12", Hubbardton Forge, Ext... | CAT3 | COL20 | 2026-03-01 | 1 | 1 |
| 890870 | Marketing Tool: 8" x 12", Hubbardton Forge, Ext... | CAT3 | COL20 | 2026-05-01 | 2 | 2 |
| 891026 | Snaps POP | CAT3 | COL20 | 2026-01-01 | 1 | 1 |
| 891026 | Snaps POP | CAT3 | COL20 | 2026-02-01 | 1 | 1 |
| 891026 | Snaps POP | CAT3 | COL20 | 2026-05-01 | 1 | 1 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2025-12-01 | 1 | 1 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2026-01-01 | 27 | 12 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2026-02-01 | 23 | 15 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2026-03-01 | 28 | 15 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2026-04-01 | 20 | 9 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2026-05-01 | 48 | 10 |
| 901010 | Standard Chain, 3' | CAT4 | COL146 | 2026-06-01 | 26 | 9 |
| 901015 | — | — | — | 2026-01-01 | 1 | 1 |
| 901015 | — | — | — | 2026-03-01 | 1 | 1 |
| 901015 | — | — | — | 2026-04-01 | 3 | 1 |
| 901020 | Heavy Chain, 3' | CAT4 | HEAVY | 2026-01-01 | 2 | 2 |
| 901020 | Heavy Chain, 3' | CAT4 | HEAVY | 2026-02-01 | 5 | 3 |
| 901020 | Heavy Chain, 3' | CAT4 | HEAVY | 2026-03-01 | 9 | 4 |
| 901020 | Heavy Chain, 3' | CAT4 | HEAVY | 2026-04-01 | 13 | 6 |
| 901020 | Heavy Chain, 3' | CAT4 | HEAVY | 2026-05-01 | 12 | 4 |
| 901020 | Heavy Chain, 3' | CAT4 | HEAVY | 2026-06-01 | 15 | 7 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2025-12-01 | 2 | 1 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2026-01-01 | 5 | 3 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2026-02-01 | 25 | 1 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2026-03-01 | 6 | 2 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2026-04-01 | 20 | 2 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2026-05-01 | 2 | 1 |
| 901030 | 5 Gauge Chain, 1' | CAT4 | COL152 | 2026-06-01 | 7 | 2 |
| 901039 | 8 Gauge Chain, 1' | CAT4 | COL152 | 2026-01-01 | 1 | 1 |
| 901039 | 8 Gauge Chain, 1' | CAT4 | COL152 | 2026-05-01 | 3 | 1 |
| 901039 | 8 Gauge Chain, 1' | CAT4 | COL152 | 2026-06-01 | 2 | 1 |
| 901040 | 7 Gauge Chain, 1' | CAT4 | COL152 | 2026-01-01 | 32 | 3 |
| 901040 | 7 Gauge Chain, 1' | CAT4 | COL152 | 2026-02-01 | 16 | 2 |
| 901040 | 7 Gauge Chain, 1' | CAT4 | COL152 | 2026-05-01 | 30 | 1 |
| 901040 | 7 Gauge Chain, 1' | CAT4 | COL152 | 2026-06-01 | 7 | 4 |
| 901041 | 7 Gauge Chain, 3' | CAT4 | COL152 | 2026-01-01 | 3 | 3 |
| 901041 | 7 Gauge Chain, 3' | CAT4 | COL152 | 2026-02-01 | 21 | 9 |
| 901041 | 7 Gauge Chain, 3' | CAT4 | COL152 | 2026-03-01 | 10 | 7 |
| 901041 | 7 Gauge Chain, 3' | CAT4 | COL152 | 2026-04-01 | 27 | 8 |
| 901041 | 7 Gauge Chain, 3' | CAT4 | COL152 | 2026-05-01 | 19 | 5 |
| 901041 | 7 Gauge Chain, 3' | CAT4 | COL152 | 2026-06-01 | 5 | 2 |
| 901050 | — | — | — | 2026-01-01 | 1 | 1 |
| 901110 | — | — | — | 2026-03-01 | 1 | 1 |
| 901111 | — | — | — | 2026-03-01 | 2 | 2 |
| 901111 | — | — | — | 2026-04-01 | 1 | 1 |
| 901162 | — | — | — | 2026-01-01 | 1 | 1 |
| 901525 | — | — | — | 2026-01-01 | 1 | 1 |
| 901610 | — | — | — | 2025-12-01 | 1 | 1 |
| 901620 | — | — | — | 2026-01-01 | 1 | 1 |
| 901620 | — | — | — | 2026-05-01 | 1 | 1 |
| 901646 | — | — | — | 2026-05-01 | 1 | 1 |
| 901647 | — | — | — | 2026-03-01 | 1 | 1 |
| 901652 | — | — | — | 2026-03-01 | 1 | 1 |
| 901657 | — | — | — | 2026-02-01 | 1 | 1 |
| 901661 | — | — | — | 2026-02-01 | 1 | 1 |
| 901663 | — | — | — | 2026-02-01 | 2 | 2 |
| 901663 | — | — | — | 2026-03-01 | 2 | 1 |
| 901663 | — | — | — | 2026-04-01 | 3 | 2 |
| 901663 | — | — | — | 2026-05-01 | 3 | 1 |
| 901664 | — | — | — | 2025-12-01 | 1 | 1 |
| 901664 | — | — | — | 2026-01-01 | 2 | 2 |
| 901664 | — | — | — | 2026-04-01 | 2 | 1 |
| 901664 | — | — | — | 2026-05-01 | 4 | 2 |
| 901667 | — | — | — | 2025-12-01 | 1 | 1 |
| 901667 | — | — | — | 2026-02-01 | 3 | 2 |
| 901667 | — | — | — | 2026-04-01 | 4 | 3 |
| 901670 | — | — | — | 2026-01-01 | 1 | 1 |
| 902010 | — | — | — | 2026-03-01 | 1 | 1 |
| 902010 | — | — | — | 2026-04-01 | 1 | 1 |
| 902010 | — | — | — | 2026-06-01 | 1 | 1 |
| 902210 | — | — | — | 2026-03-01 | 12 | 1 |
| 902310 | — | — | — | 2025-12-01 | 1 | 1 |
| 902310 | — | — | — | 2026-01-01 | 4 | 2 |
| 902310 | — | — | — | 2026-03-01 | 3 | 3 |
| 902310 | — | — | — | 2026-04-01 | 1 | 1 |
| 902310 | — | — | — | 2026-05-01 | 2 | 2 |
| 902323 | Glass Sample | CAT8 | GLASS | 2025-12-01 | 1 | 1 |
| 902323 | Glass Sample | CAT8 | GLASS | 2026-01-01 | 5 | 4 |
| 902323 | Glass Sample | CAT8 | GLASS | 2026-02-01 | 3 | 2 |
| 902323 | Glass Sample | CAT8 | GLASS | 2026-03-01 | 2 | 2 |
| 902323 | Glass Sample | CAT8 | GLASS | 2026-04-01 | 2 | 2 |
| 902323 | Glass Sample | CAT8 | GLASS | 2026-05-01 | 2 | 2 |
| 902325 | Wood Sample | CAT8 | WOOD | 2026-01-01 | 1 | 1 |
| 902325 | Wood Sample | CAT8 | WOOD | 2026-02-01 | 3 | 1 |
| 902326 | Leather Sample | CAT8 | COL147 | 2026-01-01 | 3 | 1 |
| 902326 | Leather Sample | CAT8 | COL147 | 2026-02-01 | 3 | 2 |
| 902326 | Leather Sample | CAT8 | COL147 | 2026-03-01 | 4 | 3 |
| 902326 | Leather Sample | CAT8 | COL147 | 2026-04-01 | 5 | 2 |
| 902326 | Leather Sample | CAT8 | COL147 | 2026-05-01 | 5 | 2 |
| 902326 | Leather Sample | CAT8 | COL147 | 2026-06-01 | 4 | 1 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2025-12-01 | 11 | 7 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2026-01-01 | 39 | 17 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2026-02-01 | 55 | 19 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2026-03-01 | 52 | 26 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2026-04-01 | 27 | 14 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2026-05-01 | 50 | 15 |
| 902327 | Metal Finish Sample | CAT8 | METAL | 2026-06-01 | 22 | 8 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2025-12-01 | 1 | 1 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2026-01-01 | 9 | 5 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2026-02-01 | 4 | 3 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2026-03-01 | 7 | 4 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2026-04-01 | 2 | 2 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2026-05-01 | 4 | 2 |
| 902328 | Fabric Shade Sample | CAT8 | COL148 | 2026-06-01 | 13 | 5 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2025-12-01 | 10 | 6 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2026-01-01 | 65 | 44 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2026-02-01 | 72 | 38 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2026-03-01 | 49 | 28 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2026-04-01 | 81 | 31 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2026-05-01 | 82 | 34 |
| 902329 | Metal Finish Samples Ring | CAT8 | METAL | 2026-06-01 | 52 | 21 |
| 902410 | — | — | — | 2026-03-01 | 1 | 1 |
| 902410 | — | — | — | 2026-04-01 | 6 | 1 |
| 902412 | — | — | — | 2026-03-01 | 1 | 1 |
| 902412 | — | — | — | 2026-04-01 | 6 | 1 |
| 902420 | — | — | — | 2026-03-01 | 3 | 3 |
| 902420 | — | — | — | 2026-04-01 | 6 | 1 |
| 902440 | — | — | — | 2026-04-01 | 6 | 1 |
| 902626 | — | — | — | 2025-12-01 | 3 | 1 |
| 902710 | — | — | — | 2026-01-01 | 2 | 2 |
| 902710 | — | — | — | 2026-02-01 | 5 | 5 |
| 902710 | — | — | — | 2026-03-01 | 3 | 3 |
| 902710 | — | — | — | 2026-04-01 | 2 | 2 |
| 902710 | — | — | — | 2026-05-01 | 3 | 3 |
| 902720 | — | — | — | 2026-01-01 | 1 | 1 |
| 902720 | — | — | — | 2026-02-01 | 1 | 1 |
| 902720 | — | — | — | 2026-03-01 | 1 | 1 |
| 902720 | — | — | — | 2026-05-01 | 1 | 1 |
| 902730 | — | — | — | 2026-03-01 | 1 | 1 |
| 902730 | — | — | — | 2026-04-01 | 1 | 1 |
| 902730 | — | — | — | 2026-05-01 | 1 | 1 |
| 902821 | SNAPS Additional 3-Light LED Module 24" Extensi... | CAT4 | SNAPS | 2026-01-01 | 1 | 1 |
| 902821 | SNAPS Additional 3-Light LED Module 24" Extensi... | CAT4 | SNAPS | 2026-02-01 | 2 | 2 |
| 902821 | SNAPS Additional 3-Light LED Module 24" Extensi... | CAT4 | SNAPS | 2026-04-01 | 2 | 2 |
| 902822 | — | — | — | 2026-03-01 | 2 | 1 |
| 902860 | — | — | — | 2026-03-01 | 2 | 1 |
| 905207 | — | — | — | 2025-12-01 | 1 | 1 |
| 905207 | — | — | — | 2026-01-01 | 1 | 1 |
| 905207 | — | — | — | 2026-02-01 | 1 | 1 |
| 905207 | — | — | — | 2026-03-01 | 7 | 1 |
| 905207 | — | — | — | 2026-04-01 | 23 | 4 |
| 905207 | — | — | — | 2026-05-01 | 6 | 1 |
| 905210 | — | — | — | 2026-06-01 | 1 | 1 |
| 905212 | — | — | — | 2026-03-01 | 4 | 1 |
| 905212 | — | — | — | 2026-04-01 | 31 | 2 |
| 905215 | — | — | — | 2025-12-01 | 1 | 1 |
| 905215 | — | — | — | 2026-01-01 | 2 | 2 |
| 905228 | — | — | — | 2026-04-01 | 1 | 1 |
| 905228 | — | — | — | 2026-06-01 | 1 | 1 |
| 905229 | — | — | — | 2026-03-01 | 1 | 1 |
| 905229 | — | — | — | 2026-04-01 | 3 | 2 |
| 905230 | — | — | — | 2025-12-01 | 1 | 1 |
| 905230 | — | — | — | 2026-01-01 | 10 | 2 |
| 905230 | — | — | — | 2026-03-01 | 6 | 2 |
| 905230 | — | — | — | 2026-04-01 | 6 | 3 |
| 905233 | — | — | — | 2025-12-01 | 2 | 1 |
| 905233 | — | — | — | 2026-03-01 | 1 | 1 |
| 905234 | — | — | — | 2025-12-01 | 4 | 1 |
| 905234 | — | — | — | 2026-02-01 | 9 | 2 |
| 905235 | — | — | — | 2026-01-01 | 1 | 1 |
| 905235 | — | — | — | 2026-02-01 | 2 | 2 |
| 905236 | — | — | — | 2025-12-01 | 6 | 1 |
| 905236 | — | — | — | 2026-01-01 | 5 | 1 |
| 905236 | — | — | — | 2026-02-01 | 6 | 4 |
| 905236 | — | — | — | 2026-03-01 | 1 | 1 |
| 905236 | — | — | — | 2026-04-01 | 1 | 1 |
| 905236 | — | — | — | 2026-05-01 | 1 | 1 |
| 905237 | — | — | — | 2026-01-01 | 6 | 3 |
| 905237 | — | — | — | 2026-02-01 | 1 | 1 |
| 905237 | — | — | — | 2026-03-01 | 3 | 1 |
| 905240 | — | — | — | 2026-02-01 | 2 | 1 |
| 905241 | — | — | — | 2026-06-01 | 1 | 1 |
| 905242 | — | — | — | 2026-03-01 | 1 | 1 |
| 905247 | — | — | — | 2026-01-01 | 2 | 1 |
| 905247 | — | — | — | 2026-03-01 | 2 | 2 |
| 905247 | — | — | — | 2026-04-01 | 3 | 2 |
| 905248 | — | — | — | 2026-03-01 | 1 | 1 |
| 905252 | — | — | — | 2026-03-01 | 1 | 1 |
| 905253 | — | — | — | 2026-06-01 | 1 | 1 |
| 905257 | — | — | — | 2026-01-01 | 1 | 1 |
| 905258 | — | — | — | 2026-01-01 | 1 | 1 |
| 905258 | — | — | — | 2026-02-01 | 1 | 1 |
| 905258 | — | — | — | 2026-03-01 | 2 | 2 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2025-12-01 | 25 | 9 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2026-01-01 | 46 | 19 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2026-02-01 | 90 | 34 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2026-03-01 | 103 | 30 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2026-04-01 | 80 | 30 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2026-05-01 | 68 | 28 |
| 905657 | 3-Piece Stem Kit, 11.5mm Diameter | CAT4 | COL153 | 2026-06-01 | 31 | 12 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2025-12-01 | 18 | 6 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-01-01 | 18 | 8 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-02-01 | 23 | 11 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-03-01 | 28 | 11 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-04-01 | 14 | 8 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-05-01 | 18 | 8 |
| 905659 | 3-Piece Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-06-01 | 2 | 2 |
| 905662 | 3-Piece Stem Kit, 19mm Diameter | CAT4 | COL153 | 2025-12-01 | 2 | 1 |
| 905662 | 3-Piece Stem Kit, 19mm Diameter | CAT4 | COL153 | 2026-02-01 | 7 | 3 |
| 905662 | 3-Piece Stem Kit, 19mm Diameter | CAT4 | COL153 | 2026-03-01 | 5 | 1 |
| 905662 | 3-Piece Stem Kit, 19mm Diameter | CAT4 | COL153 | 2026-05-01 | 6 | 2 |
| 905662 | 3-Piece Stem Kit, 19mm Diameter | CAT4 | COL153 | 2026-06-01 | 7 | 4 |
| 905663 | — | — | — | 2026-01-01 | 9 | 1 |
| 905669 | — | — | — | 2026-04-01 | 1 | 1 |
| 905670 | — | — | — | 2026-06-01 | 1 | 1 |
| 905672 | — | — | — | 2025-12-01 | 1 | 1 |
| 905672 | — | — | — | 2026-01-01 | 2 | 1 |
| 905672 | — | — | — | 2026-05-01 | 1 | 1 |
| 905676 | — | — | — | 2026-06-01 | 1 | 1 |
| 905679 | — | — | — | 2025-12-01 | 9 | 1 |
| 905680 | — | — | — | 2026-04-01 | 15 | 1 |
| 905680 | — | — | — | 2026-05-01 | 1 | 1 |
| 905681 | — | — | — | 2025-12-01 | 2 | 2 |
| 905681 | — | — | — | 2026-01-01 | 8 | 2 |
| 905681 | — | — | — | 2026-02-01 | 2 | 2 |
| 905681 | — | — | — | 2026-03-01 | 1 | 1 |
| 905681 | — | — | — | 2026-05-01 | 8 | 2 |
| 905681 | — | — | — | 2026-06-01 | 1 | 1 |
| 905682 | — | — | — | 2025-12-01 | 21 | 3 |
| 905682 | — | — | — | 2026-01-01 | 3 | 2 |
| 905682 | — | — | — | 2026-02-01 | 1 | 1 |
| 905682 | — | — | — | 2026-03-01 | 3 | 2 |
| 905682 | — | — | — | 2026-05-01 | 5 | 1 |
| 905682 | — | — | — | 2026-06-01 | 3 | 2 |
| 905686 | — | — | — | 2026-03-01 | 1 | 1 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2025-12-01 | 3 | 2 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-01-01 | 10 | 5 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-02-01 | 7 | 4 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-03-01 | 23 | 6 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-04-01 | 4 | 3 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-05-01 | 1 | 1 |
| 905689 | 3-Piece Outdoor Stem Kit, 16mm Diameter | CAT4 | COL153 | 2026-06-01 | 1 | 1 |
| 905695 | — | — | — | 2026-02-01 | 2 | 1 |
| 905695 | — | — | — | 2026-04-01 | 1 | 1 |
| 905696 | — | — | — | 2025-12-01 | 1 | 1 |
| 905696 | — | — | — | 2026-01-01 | 1 | 1 |
| 905696 | — | — | — | 2026-03-01 | 2 | 2 |
| 905696 | — | — | — | 2026-04-01 | 1 | 1 |
| 905696 | — | — | — | 2026-05-01 | 2 | 1 |
| 905697 | — | — | — | 2025-12-01 | 2 | 1 |
| 905697 | — | — | — | 2026-04-01 | 1 | 1 |
| 905697 | — | — | — | 2026-06-01 | 4 | 1 |
| 905699 | — | — | — | 2026-01-01 | 4 | 2 |
| 905699 | — | — | — | 2026-02-01 | 2 | 2 |
| 905699 | — | — | — | 2026-04-01 | 12 | 1 |
| 905699 | — | — | — | 2026-05-01 | 13 | 2 |
| 905700 | SNAPS 24" Extension Strap | CAT4 | SNAPS | 2026-01-01 | 2 | 1 |
| 905700 | SNAPS 24" Extension Strap | CAT4 | SNAPS | 2026-03-01 | 2 | 1 |
| 905700 | SNAPS 24" Extension Strap | CAT4 | SNAPS | 2026-04-01 | 2 | 2 |
| 905701 | SNAPS Additional LED Module with 24" Extension ... | CAT4 | SNAPS | 2026-01-01 | 3 | 2 |
| 905701 | SNAPS Additional LED Module with 24" Extension ... | CAT4 | SNAPS | 2026-02-01 | 2 | 1 |
| 905701 | SNAPS Additional LED Module with 24" Extension ... | CAT4 | SNAPS | 2026-03-01 | 6 | 3 |
| 905701 | SNAPS Additional LED Module with 24" Extension ... | CAT4 | SNAPS | 2026-04-01 | 6 | 4 |
| 905701 | SNAPS Additional LED Module with 24" Extension ... | CAT4 | SNAPS | 2026-05-01 | 5 | 4 |
| 905703 | — | — | — | 2026-05-01 | 1 | 1 |
| 905705 | — | — | — | 2026-01-01 | 1 | 1 |
| 905706 | — | — | — | 2025-12-01 | 1 | 1 |
| 905706 | — | — | — | 2026-02-01 | 2 | 1 |
| 905707 | — | — | — | 2025-12-01 | 1 | 1 |
| 905707 | — | — | — | 2026-02-01 | 1 | 1 |
| 905707 | — | — | — | 2026-04-01 | 2 | 2 |
| 905707 | — | — | — | 2026-05-01 | 1 | 1 |
| 905707 | — | — | — | 2026-06-01 | 1 | 1 |
| 905708 | — | — | — | 2026-01-01 | 2 | 1 |
| 905708 | — | — | — | 2026-02-01 | 1 | 1 |
| 905708 | — | — | — | 2026-03-01 | 1 | 1 |
| 905713 | SNAPS Additional LED Module with 72" Extension ... | CAT4 | SNAPS | 2025-12-01 | 2 | 1 |
| 905713 | SNAPS Additional LED Module with 72" Extension ... | CAT4 | SNAPS | 2026-01-01 | 1 | 1 |
| 905713 | SNAPS Additional LED Module with 72" Extension ... | CAT4 | SNAPS | 2026-02-01 | 1 | 1 |
| 905713 | SNAPS Additional LED Module with 72" Extension ... | CAT4 | SNAPS | 2026-03-01 | 2 | 1 |
| 905713 | SNAPS Additional LED Module with 72" Extension ... | CAT4 | SNAPS | 2026-04-01 | 4 | 2 |
| 905713 | SNAPS Additional LED Module with 72" Extension ... | CAT4 | SNAPS | 2026-05-01 | 8 | 2 |
| 905718 | Lilium Chain, 3' | CAT4 | COL152 | 2026-02-01 | 1 | 1 |
| 905718 | Lilium Chain, 3' | CAT4 | COL152 | 2026-03-01 | 1 | 1 |
| 905718 | Lilium Chain, 3' | CAT4 | COL152 | 2026-06-01 | 2 | 1 |
| 905719 | — | — | — | 2025-12-01 | 1 | 1 |
| 905720 | — | — | — | 2026-01-01 | 1 | 1 |
| 905722 | — | — | — | 2026-03-01 | 1 | 1 |
| 905723 | — | — | — | 2026-05-01 | 1 | 1 |
| 905723 | — | — | — | 2026-06-01 | 1 | 1 |
| 905724 | — | — | — | 2026-04-01 | 4 | 3 |
| 905724 | — | — | — | 2026-05-01 | 2 | 2 |
| 905725 | — | — | — | 2026-03-01 | 2 | 1 |
| 905725 | — | — | — | 2026-04-01 | 0 | 1 |
| 905725 | — | — | — | 2026-05-01 | 4 | 2 |
| 905725 | — | — | — | 2026-06-01 | 10 | 4 |
| 905726 | — | — | — | 2026-04-01 | 10 | 4 |
| 905726 | — | — | — | 2026-05-01 | 5 | 3 |
| 905726 | — | — | — | 2026-06-01 | 4 | 2 |
| 905727 | — | — | — | 2026-04-01 | 2 | 1 |
| 905727 | — | — | — | 2026-05-01 | 2 | 2 |
| 905727 | — | — | — | 2026-06-01 | 1 | 1 |
| 905729 | — | — | — | 2026-04-01 | 7 | 3 |
| 905729 | — | — | — | 2026-05-01 | 2 | 2 |
| 905729 | — | — | — | 2026-06-01 | 2 | 1 |
| 905730 | — | — | — | 2026-04-01 | 1 | 1 |
| 905731 | — | — | — | 2026-04-01 | 2 | 2 |
| 905741 | — | — | — | 2026-04-01 | 2 | 1 |
| 905744 | — | — | — | 2026-04-01 | 2 | 1 |
| 905744 | — | — | — | 2026-05-01 | 3 | 2 |
| 905744 | — | — | — | 2026-06-01 | 3 | 1 |
| 9BPAINT | — | — | — | 2026-06-01 | 1 | 1 |
| 9C25PACK | — | — | — | 2026-01-01 | 1 | 1 |
| 9C25PACK | — | — | — | 2026-03-01 | 4 | 1 |
| 9C25PACK | — | — | — | 2026-05-01 | 2 | 2 |
| 9C29PACK | — | — | — | 2025-12-01 | 3 | 3 |
| 9C29PACK | — | — | — | 2026-01-01 | 4 | 4 |
| 9C29PACK | — | — | — | 2026-02-01 | 6 | 4 |
| 9C29PACK | — | — | — | 2026-03-01 | 16 | 8 |
| 9C29PACK | — | — | — | 2026-04-01 | 6 | 5 |
| 9C29PACK | — | — | — | 2026-05-01 | 3 | 3 |
| 9C29PACK | — | — | — | 2026-06-01 | 3 | 2 |
| 9CUSTOM | — | — | — | 2025-12-01 | 19 | 13 |
| 9CUSTOM | — | — | — | 2026-01-01 | 63 | 26 |
| 9CUSTOM | — | — | — | 2026-02-01 | 52 | 35 |
| 9CUSTOM | — | — | — | 2026-03-01 | 44 | 25 |
| 9CUSTOM | — | — | — | 2026-04-01 | 30 | 24 |
| 9CUSTOM | — | — | — | 2026-05-01 | 54 | 23 |
| 9CUSTOM | — | — | — | 2026-06-01 | 20 | 12 |
| 9N00145716-1-05 | — | — | — | 2026-06-01 | 1 | 1 |
| 9N00145716-2-05 | — | — | — | 2026-06-01 | 1 | 1 |
| 9N00145922 | — | — | — | 2025-12-01 | 14 | 4 |
| 9N00146745 | — | — | — | 2025-12-01 | 1 | 1 |
| 9N00147387-4 | — | — | — | 2026-04-01 | 1 | 1 |
| C201059 | — | — | — | 2026-03-01 | 211 | 1 |
| C306401 | — | — | — | 2026-05-01 | 40 | 1 |

### Q-39_category_results.md

# Q-39-cat Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-39-cat — Line Analysis by Category
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 15
- **Run date**: 2026-06-16


| category_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| CAT1 | $29.4M | 17,518 | 275 | $106,826 |
| CAT6 | $22.5M | 38,289 | 240 | $93,619 |
| CAT15 | $8.3M | 20,960 | 189 | $43,931 |
| CAT13 | $4.2M | 9,494 | 79 | $53,118 |
| CAT2 | $3.7M | 6,436 | 70 | $52,359 |
| CAT7 | $2.4M | 2,200 | 34 | $71,741 |
| CAT14 | $1.4M | 433 | 7 | $194,015 |
| CAT9 | $1.0M | 1,178 | 33 | $30,997 |
| CAT5 | $973,358 | 1,895 | 49 | $19,864 |
| CAT16 | $290,276 | 289 | 6 | $48,379 |
| CAT17 | $286,653 | 313 | 23 | $12,463 |
| CAT4 | $194,105 | 3,805 | 16 | $12,132 |
| GLASS | $111,910 | 1,589 | 13 | $8,608 |
| CAT3 | $7,004 | 10 | 2 | $3,502 |
| CAT8 | $3,956 | 209 | 7 | $565 |

### Q-39_collection_results.md

# Q-39-col Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-39-col — Line Analysis by Collection
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| collection_code | total_erp_sales | total_qty | item_count | sales_per_item |
| --- | --- | --- | --- | --- |
| AXIS | $3.3M | 4,269 | 14 | $237,132 |
| COL122 | $2.9M | 3,938 | 23 | $125,621 |
| EXOS | $2.5M | 2,916 | 19 | $130,500 |
| HENRY | $2.3M | 4,350 | 26 | $86,567 |
| COL64 | $1.5M | 487 | 2 | $759,947 |
| COL102 | $1.4M | 500 | 4 | $361,223 |
| COL86 | $1.4M | 1,232 | 15 | $92,439 |
| COL114 | $1.4M | 1,579 | 11 | $124,421 |
| MASON | $1.3M | 1,905 | 7 | $184,177 |
| COL16 | $1.2M | 3,615 | 17 | $72,601 |
| COL25 | $1.1M | 2,757 | 18 | $63,179 |
| AIRIS | $1.1M | 2,508 | 7 | $160,666 |
| ARC | $1.1M | 1,809 | 12 | $89,471 |
| VITRE | $1.0M | 325 | 2 | $522,729 |
| COL32 | $1.0M | 725 | 5 | $207,814 |
| COL14 | $862,775 | 1,551 | 16 | $53,923 |
| CAIRN | $825,939 | 743 | 5 | $165,188 |
| COL60 | $789,146 | 283 | 8 | $98,643 |
| SNAPS | $788,422 | 510 | 13 | $60,648 |
| LUMA | $783,779 | 798 | 7 | $111,968 |
| COL66 | $763,051 | 224 | 2 | $381,526 |
| TORCH | $741,352 | 1,539 | 10 | $74,135 |
| COL26 | $737,479 | 666 | 9 | $81,942 |
| COL19 | $730,387 | 2,032 | 6 | $121,731 |
| COL24 | $703,287 | 891 | 16 | $43,955 |

### Q-42_results.md

# Q-42 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-42 — New Item Performance
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 22
- **Run date**: 2026-06-16


| collection_code | new_item_count | total_erp_sales | total_qty_sold | sales_per_new_item |
| --- | --- | --- | --- | --- |
| COL84 | 114 | $174,793 | 134 | $1,533 |
| LYRIC | 86 | $142,295 | 119 | $1,655 |
| COL149 | 62 | $107,113 | 75 | $1,728 |
| COL87 | 72 | $81,515 | 99 | $1,132 |
| COL3 | 91 | $75,484 | 133 | $829 |
| MUSE | 75 | $52,916 | 81 | $706 |
| LINEA | 37 | $49,932 | 95 | $1,350 |
| COL139 | 7 | $49,894 | 7 | $7,128 |
| ARC | 43 | $41,556 | 77 | $966 |
| STOWE | 75 | $41,234 | 111 | $550 |
| TRUSS | 57 | $37,069 | 75 | $650 |
| COL40 | 37 | $35,941 | 62 | $971 |
| NOVA | 43 | $26,713 | 65 | $621 |
| CORAL | 8 | $24,780 | 7 | $3,098 |
| FOCAL | 30 | $21,079 | 47 | $703 |
| KORA | 28 | $17,183 | 43 | $614 |
| COL150 | 28 | $12,124 | 40 | $433 |
| COL151 | 23 | $11,640 | 26 | $506 |
| SORA | 14 | $7,688 | 20 | $549 |
| SPIRE | 17 | $7,407 | 22 | $436 |
| SNAPS | 6 | $4,250 | 6 | $708 |
| NP | 1 | $0 | 0 | $0 |

### Q-59_results.md

# Q-59 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-59 — Fill Rate & Backorder Revenue Impact
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| row_type | item_number | item_description | category | fill_rate_pct | total_unfilled | qty_backordered | affected_customers | avg_unit_price | backorder_exposure | annual_revenue | annual_buyers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ORG_SUMMARY | — | — | — | 83.90 | 10,510 | — | — | — | — | — | — |

### Q-61_results.md

# Q-61 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-61 — New Introduction Adoption Gap
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 30
- **Run date**: 2026-06-16


| item_number | description | category | buyers | qty_ordered | revenue | orders | list_price |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 181601 | Kora Mini Pendant | CAT13 | 0 | 0 | 0 | 0 | 925 |
| 201085 | Focal Large Sconce/Flush Mount | CAT15 | 0 | 0 | 0 | 0 | 1,300 |
| 302049 | Arc Large Outdoor Sconce | CAT6 | 0 | 0 | 0 | 0 | 1,200 |
| 401330 | Coral LED Ring Pendant | CAT1 | 0 | 0 | 0 | 0 | 14,750 |
| 302048 | Arc Small Outdoor Sconce | CAT6 | 0 | 0 | 0 | 0 | 875 |
| 302050 | Arc Tall Outdoor Sconce | CAT6 | 0 | 0 | 0 | 0 | 2,225 |
| 201082 | Truss 1-Light Sconce | CAT15 | 0 | 0 | 0 | 0 | 625 |
| 204072 | Caribou 1-Light Sconce | CAT15 | 0 | 0 | 0 | 0 | 850 |
| 201083 | Windsor 1-Light Sconce | CAT15 | 0 | 0 | 0 | 0 | 625 |
| 122112 | Nova Large LED Flush Mount | CAT2 | 0 | 0 | 0 | 0 | 1,725 |
| 101325 | Caribou 5-Light Chandelier | CAT7 | 0 | 0 | 0 | 0 | 4,150 |
| 101326 | Caribou 9-Light Tiered Chandelier | CAT7 | 0 | 0 | 0 | 0 | 7,375 |
| 122111 | Nova Small LED Flush Mount | CAT2 | 0 | 0 | 0 | 0 | 1,000 |
| 131001 | Muse LED Pendant | CAT1 | 0 | 0 | 0 | 0 | 2,125 |
| 131002 | Muse LED Large Pendant | CAT1 | 0 | 0 | 0 | 0 | 2,475 |
| 131003 | Sora Pendant | CAT1 | 0 | 0 | 0 | 0 | 1,125 |
| 131008 | Bellis 6-Arm 12-Light Round Chandelier | CAT1 | 0 | 0 | 0 | 0 | 5,625 |
| 131009 | Bellis 6-Arm 12-Light Oval Chandelier | CAT1 | 0 | 0 | 0 | 0 | 5,875 |
| 131161 | Lyric 5-Light Round Pendant | CAT1 | 0 | 0 | 0 | 0 | 6,125 |
| 131162 | Lyric 7-Light Linear Pendant | CAT1 | 0 | 0 | 0 | 0 | 10,375 |
| 131163 | Lilium 5-Light Round Pendant | CAT1 | 0 | 0 | 0 | 0 | 2,900 |
| 131164 | Lilium 9-Light Round Pendant | CAT1 | 0 | 0 | 0 | 0 | 5,250 |
| 131165 | Lilium 10-Light Linear Pendant | CAT1 | 0 | 0 | 0 | 0 | 5,725 |
| 131166 | Lilium 10-Light Mobile Pendant | CAT1 | 0 | 0 | 0 | 0 | 5,725 |
| 131621 | Windsor 16-Light Chandelier | CAT1 | 0 | 0 | 0 | 0 | 9,875 |
| 131622 | Windsor 12-Light Chandelier | CAT1 | 0 | 0 | 0 | 0 | 6,375 |
| 131623 | Truss 6-Arm Linear Chandelier | CAT1 | 0 | 0 | 0 | 0 | 3,000 |
| 161191 | Lyric 1-Light Pendant | CAT13 | 0 | 0 | 0 | 0 | 1,300 |
| 181602 | Kora Pendant | CAT13 | 0 | 0 | 0 | 0 | 1,450 |
| 181603 | Trilogy Mini Pendant | CAT13 | 0 | 0 | 0 | 0 | 1,125 |
