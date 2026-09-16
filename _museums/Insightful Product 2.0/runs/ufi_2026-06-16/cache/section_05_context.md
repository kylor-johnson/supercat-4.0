# Section 5 Context Bundle — Universal Furniture (ufi)
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

## Section Guide — section_05_commerce.md

# Section Guide: §5 — Commerce Analytics
> **v2.0** — hardened 2026-06-16 (CCI v3 run). Last updated: 2026-06-16.

## Section Identity
- **id**: `commerce`
- **title**: Commerce Analytics
- **section number**: 5
- **include when**: Always
- **skip when**: Never — this section is always rendered

## Query Inputs

Read these cache files:
- `cache/Q-13_results.md` — Customer concentration risk (top-buyer eCat GMV share)
- `cache/Q-16_results.md` — All-channel total business visibility
- `cache/Q-18_results.md` — eCat order trend and channel breakdown
- `cache/Q-20_results.md` — AOV by order segment
- `cache/Q-21_results.md` — Order type & workflow
- `cache/Q-45_results.md` — eCat capture rate
- `cache/gate_flags.md` — for `HAS_CART`, `HAS_PORTAL_ORDERS`, `VM45_RENDER`, `PORTAL_CUSTOMER_DATA_PRESENT`
- `cache/Q-52_results.md` — eCat penetration of total business by customer (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 4 Top Buyers table MUST include enrichment columns)
- `cache/Q-55_results.md` — Category-level competitive displacement (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains displacement rows, subsection 8 Part A MUST be rendered)
- `cache/Q-56_results.md` — Per-rep capture rate trend (conditional: render Part B of subsection 8 if `PORTAL_REP_DATA_PRESENT = true` AND data rows show declining reps)
- `cache/Q-58_results.md` — Market commitment conversion (**MANDATORY when gate met**: if `HAS_COMMITMENT_DATA = true` AND this file contains data rows, subsection 9 MUST be rendered)
- `cache/Q-58b_results.md` — Uncommitted market items in stock (conditional: render Part B of subsection 9 if `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND data rows exist)
- `cache/Q-60_results.md` — Price erosion / trade-down detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains data rows, subsection 9 MUST be rendered)
- `cache/Q-69_results.md` — Order timing distribution (conditional: new query, render subsection 10 if data rows exist)
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_5` tier

## CRITICAL REQUIREMENTS — Read Before Building

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **Q-52 MANDATORY ENRICHMENT**: If `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `Q-52_results.md` has data rows, the Top Buyers table (subsection 4) MUST include "Total Business" and "eCat Share" columns.
2. **HAS_PORTAL_ORDERS GATE**: If `HAS_PORTAL_ORDERS = false`, subsections 1B, 6, and 7 are ALL skipped. Do not mention ERP or total business anywhere.
3. **VM45_RENDER GATE**: If `VM45_RENDER = false`, subsection 6 renders total business context only (no capture rate). If `HAS_PORTAL_ORDERS = false`, subsection 6 is skipped entirely.
4. **Q-55 COMPETITIVE DISPLACEMENT**: If `HAS_PORTAL_ORDERS = true` AND `Q-55_results.md` has rows where total grew but eCat share shrank, subsection 7 MUST be rendered.
5. **Q-58 MARKET ATTRIBUTION**: If `HAS_COMMITMENT_DATA = true` AND `Q-58_results.md` has data rows, subsection 8 MUST be rendered.
6. **Q-58b IN-STOCK ITEMS**: If `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND `Q-58b_results.md` has data rows, subsection 8 Part B MUST be rendered.
7. **Q-60 PRICE EROSION**: If `HAS_PORTAL_ORDERS = true` AND `Q-60_results.md` has data rows, subsection 9 MUST be rendered.
8. **CONFIDENCE FOOTER**: Every §5 fragment MUST contain a confidence footer. Read `SECTION_CONFIDENCE_5` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags. Position: FULL=bottom, STRONG/PARTIAL/LIMITED=top (after metrics, before first subsection).
9. **VERIFICATION**: After building, run through the Conditional Subsection Checklist at the bottom of this guide. Fix any failures before saving.

---

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. eCat Order Trend (Q-18)

**Part A** (always): eCat order trend — eCat-originated orders only.

**Part B** (only if `HAS_PORTAL_ORDERS = true`): Add eCat share of total business trend alongside Part A.

**What-this-means guidance**: Frame like an analyst comparing seasonality to growth. Highlight peak months, note partial-period artifacts, and contextualize whether the trend is stable, accelerating, or cyclical. Example: "eCat ordering peaked in [month] with consistent monthly volume of X–Y orders. The partial-month dip at period boundaries reflects data truncation, not declining demand."

### 2. AOV by Order Segment (Q-20)

Build from `Q-20_results.md`. Surface average order value broken down by order segment.

**What-this-means guidance**: Identify the premium segments and frame the AOV gap as opportunity. Example: "Quote orders average $X — more than Nx the standard order value. This premium reflects project-based complexity. Increasing quote-to-confirmed conversion could significantly lift platform GMV."

### 3. eCat Ordering Channel Breakdown (Q-18)

**Gate**: `HAS_CART = true`

Build from Q-18 data. Show iPad vs. eCat Online channel split.

**What-this-means guidance**: Frame the channel mix as adoption signal. If one channel dominates, explain what that implies about buyer behavior. Example: "100% iPad ordering reflects a rep-driven sales model. Activating eCat Online would add a self-service channel for reorders and lower-touch accounts without displacing rep relationships."

### 4. Top Buyers & Concentration (Q-13)

Build from `Q-13_results.md`. Show top 10 buyers by eCat GMV with these exact columns:

| Column | Content |
|--------|---------|
| Customer | Buyer name |
| Orders | eCat order count |
| GMV | eCat GMV |
| % of eCat GMV | Buyer's share of total eCat GMV |

Include a concentration callout if top-5 buyers exceed 25% of total eCat GMV.

**MANDATORY ENRICHMENT** (when `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-52_results.md` exists with data rows): You MUST add two columns to the table using `cache/Q-52_results.md` data joined on customer identifier — "Total Business" (all-channel GMV) and "eCat Share" (`ecat_gmv / total_business_gmv × 100`). When `PORTAL_CUSTOMER_DATA_PRESENT = false` OR the file is absent OR it contains zero rows, render the Q-13-only table unchanged — do not add empty columns or placeholders.

**What-this-means guidance**: Assess concentration risk like a portfolio analyst. Low concentration = stability but broad-based growth needed. High concentration = key-account dependency risk. When enrichment is present, highlight penetration gaps: "Your largest eCat buyer generates $X on the platform but $Y in total business — there's headroom to capture more of their spend digitally."

### 5. Order Type & Workflow (Q-21)

Build from `Q-21_results.md`.

**Framing principle**: Lead with the quote premium insight — the AOV difference between quote orders and confirmed orders. The full type distribution table is supporting detail, not the headline. Most clients already know their team places confirmed orders; what they don't know is the dollar multiplier on quotes.

**Required content:**
- `.callout.insight` leading with the quote premium: "Your quote orders average $X — Nx the standard confirmed order value ($Y). Increasing quote-to-confirmed conversion is your highest-leverage volume opportunity." If no quote orders exist, lead with the dominant workflow pattern instead.
- Full order type distribution table inside a collapsed `<details>` block with summary "View order type breakdown":

| Column | Content |
|--------|---------|
| Order Type | Type name (Confirmed, Quote, HFC, etc.) |
| Orders | Count |
| Share | Percentage of total orders |
| Avg Order Value | AOV for that type |

- If HFC (Hold for Confirmation) orders exist, note in prose that the approval workflow serves compliance or high-value transaction governance.

**What-this-means guidance**: Focus on the actionable insight from the type distribution, not the distribution itself. Example: "The Nx AOV premium on quotes means each converted quote is worth N standard orders. If even X% more quotes converted to confirmed, that would add $Y in platform GMV." Do not restate "96% of your orders are confirmed" — the reader can see that in the collapsed table.

### 6. Channel Mix & Capture Rate (Q-16, Q-45)

**Gate**: `HAS_PORTAL_ORDERS = true` — if false, skip this entire subsection silently.

Build from `Q-16_results.md` and `Q-45_results.md`. This subsection states total business ONCE and immediately pivots to the capture rate story. No separate "Total Business Context" preamble.

**Never use "ERP" in the rendered HTML** — say "total business," "all-channel sales," or "your business system."

**Required content:**
- Metrics grid: Total all-channel business (trailing 12 months), eCat GMV, eCat capture rate (GMV-based). Include order-based capture rate as a secondary metric if meaningfully different from GMV-based.
- Prose paragraph: state total business as context, then pivot immediately to what the capture rate means. Frame the gap as opportunity, not failure. Example: "Your total business across all channels reached $87M over the trailing 12 months. eCat captured $8.6M — a 9.8% share by GMV. Even a modest increase to 15% would represent approximately $4.5M in additional platform-attributed revenue annually."
- If `VM45_RENDER = false` (denominator gate failed): render total business context only with a metrics grid showing all-channel business volume. Do NOT attempt a capture rate without a valid denominator. Add a single prose line: "Capture rate analysis requires a consistent denominator between platform and total-business data — this will be available when data synchronization is validated."
- If capture rate is low (<15%), frame as runway with a dollar-equivalent projection (hedged): "significant headroom remains — each percentage point of capture represents approximately $X in additional platform GMV."
- If capture rate is high (>30%), frame as platform maturity and celebrate the achievement.

**What-this-means guidance**: Frame capture rate as the single most important adoption metric. Do not restate the numbers — explain what the gap is worth in dollars and what would move the needle. Example: "The X% gap between your current capture rate and the top-quartile benchmark represents $Y in annual platform GMV — achievable through activation of dormant accounts and deeper rep adoption."

### 7. Competitive Displacement Signals (Q-55, Q-56)

**Gate**: `HAS_PORTAL_ORDERS = true` — if false, skip this entire subsection silently.

**MANDATORY RENDER**: If `cache/Q-55_results.md` exists AND contains data rows showing at least one category where `total_growth_pct > 0` AND `ecat_share_change_ppts < 0`, this subsection MUST appear. If no category meets the displacement criteria (total grew but eCat share shrank), skip silently — no false alarm.

**Data sources**: `cache/Q-55_results.md` (category displacement), `cache/Q-56_results.md` (rep capture trend)

**Rendering**:

**Part A — Category Displacement (Q-55):**

Open with a `.callout.alert` titled "Competitive Displacement Detected" if any categories show displacement. The callout should state: "In X categories, total business grew while your platform share declined — an estimated $Y may have shifted to other sources."

Then render a table with categories that show displacement (where `total_growth_pct > 0` AND `ecat_share_change_ppts < 0`):

| Column | Content |
|--------|---------|
| Category | Product category name |
| Total Business (Current Qtr) | `current_total_gmv` |
| Total Growth | `total_growth_pct` with `.badge.ok` |
| Platform Share (Prior) | `prior_ecat_share_pct` |
| Platform Share (Current) | `current_ecat_share_pct` |
| Share Change | `ecat_share_change_ppts` with `.badge.danger` (negative = red) |
| Est. Displaced | Calculated: `(prior_ecat_share_pct/100 × current_total_gmv) - current_ecat_gmv` |

Show all displacement categories (typically 3–8). If more than 5, collapse remaining in `<details>`.

**Part B — Rep Capture Rate Trend (Q-56, conditional):**

If `cache/Q-56_results.md` exists AND contains data rows AND `PORTAL_REP_DATA_PRESENT = true`, render a supplementary table showing reps whose capture rate declined:

| Column | Content |
|--------|---------|
| Rep | Rep name (never expose internal identifiers) |
| Total Business (Current) | `current_total_gmv` |
| Prior Capture % | `prior_capture_pct` |
| Current Capture % | `current_capture_pct` |
| Change | `capture_change_ppts` with badge (`.badge.danger` if ≤ -5, `.badge.warn` if -5 to 0) |

Show only reps where `capture_change_ppts < 0` (declining), sorted by `current_total_gmv` descending. Top 5 visible, remaining in `<details>`. If no reps show decline, omit Part B silently.

**Claim rules**: "Total business in [Category] grew X%, but your platform captured Y fewer percentage points of that growth — an estimated $Z shifted to other channels." ALWAYS hedge: "estimated," "may have shifted," "suggests." Never say definitively "lost to competitors" — could be channel shift, timing, or seasonal patterns. Frame rep-level data as coaching opportunity, not failure. Never use "ERP" or "portal_orders" or "portal_order_items." Use "total business" and "all-channel."

**What-this-means guidance**: Frame displacement as investigative signal, not accusation. Example: "In X categories, total business grew while your platform share declined. This pattern may reflect buyers shifting to alternative ordering channels, seasonal procurement timing, or competitive displacement — it warrants rep-level follow-up to understand the root cause." For Part B, frame as coaching: "These reps manage growing accounts but are capturing less of that growth on the platform — a focused enablement conversation could recapture share."

### 8. Market Commitment Attribution (Q-58)

**Gate**: `HAS_COMMITMENT_DATA = true` (read from `gate_flags.md`) — if false, skip this entire subsection silently.

**MANDATORY RENDER**: If `cache/Q-58_results.md` exists AND contains data rows, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-58_results.md`

**Rendering**: Open with a `.callout.insight` block titled "Market Commitment Conversion" with a summary computed from the most recent market row: "At [market_code], your accounts committed to X items. Within 90 days, Y% converted to orders — Z items remain unrealized."

Then render a table with all market rows (typically 2–6 markets):

| Column | Content |
|--------|---------|
| Market | `market_code` (e.g., "High Point April 2026") — format nicely from code |
| Date | `market_start_date` formatted as month/year |
| Customers | `customers_committing` |
| Items Committed | `total_committed_items` |
| Items Converted | `items_converted` |
| Conversion Rate | `item_conversion_pct` with `.badge.ok` if ≥ 70%, `.badge.warn` if 40–69%, `.badge.danger` if < 40% |
| Unrealized Items | `unrealized_items` — committed items with zero follow-through |

Show all market rows (no collapse unless > 6 rows).

After the table, include a `.callout.insight` summary: "Across all markets, X total items remain uncommitted-to-ordered. These represent buying intent that was expressed but not yet fulfilled — ideal targets for rep follow-up."

**Part B — In-Stock Actionable Items (Q-58b)**

**Gate**: Render ONLY if `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND `cache/Q-58b_results.md` has data rows.

**Data source**: `cache/Q-58b_results.md`

**Rendering**: After the market conversion table, add a `.callout.opportunity` block titled "Immediate Action: Committed Items Currently In Stock". Open with: "These items were committed at market, never ordered, and are sitting in your warehouse right now — the shortest path from intent to revenue."

Then render a table:

| Column | Content |
|--------|---------|
| Item | `item_description` (fall back to `item_number` if blank) |
| Market | `market_code` formatted as readable name |
| Accounts | `customers_committed` |
| Committed Qty | `total_committed_qty` |
| In Stock | `current_stock` |
| Stock Value | `stock_value` formatted as currency |

After the table: "Total actionable value: $X across Y items. These are sitting in your warehouse right now — the shortest path from intent to revenue."

**Claim rules**: Never expose `item_number` as raw internal code. Use `item_description` in prose. Frame as the lowest-friction opportunity available. Never use "ERP."

**What-this-means guidance (subsection 9 overall)**: Frame market conversion as pipeline visibility. Example: "Market commitments represent explicit buying intent captured at the point of enthusiasm. The X% conversion rate means Y items still have unrealized demand — these are warm leads that require re-engagement, not cold outreach." For Part B, emphasize zero-friction: "These items are already in your warehouse with committed buyers — they represent revenue waiting to be invoiced."

---

### 9. Price Erosion / Trade-Down Detection (Q-60)

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `cache/Q-60_results.md` has data rows.

**Data source**: `cache/Q-60_results.md` (20 deduplicated rows in CCI v3 — one row per account showing QoQ avg unit price decline ≥ 4%)

**Rendering**: Open with a `.callout.warn` titled "Pricing Shift Detected" with a summary: "X accounts show declining average unit prices quarter-over-quarter — combined current-quarter business: $Y. This may indicate competitive pressure, shifting buyer mix, or product substitution."

Then render a table of top accounts (sorted by `current_quarter_gmv` descending). Show top 5 visible, remaining in `<details>`:

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| Prior Avg Price | `prior_avg_price` formatted as currency |
| Current Avg Price | `current_avg_price` formatted as currency |
| Change | `price_change_pct` with `.badge.danger` styling (all values are negative — use badge for visual urgency) |
| Current Quarter GMV | `current_quarter_gmv` formatted as currency |
| Orders | `current_orders` |

After the table, add a `.callout.insight` titled "Investigative Context": "Declining unit prices may reflect several dynamics: competitive pricing pressure driving buyers to request discounts, a natural shift toward lower-priced product tiers, changing buyer mix within an account, or seasonal promotional activity. These patterns warrant individual account review — they are signals to investigate, not conclusions to act on."

**Tone**: Investigative, not alarmist. The `.badge.danger` on percentage declines provides visual urgency but the prose must remain measured and multi-causal. Never say "price erosion alert" in a way that implies the client is failing — frame as "pattern worth understanding."

**Claim rules**: Always hedge — "may indicate competitive pressure, shifting buyer mix, or product substitution." Never assert a single cause. Never say "losing to competitors" or "trading down" definitively — use "trending toward lower price points" or "average unit price declining." Never expose `customer_bill_to_number` or any internal identifier. Never use "ERP" — use "your order history" or "all-channel data."

**What-this-means guidance**: Frame as investigative opportunity, not alarm. Example: "X accounts are trending toward lower unit prices. This could reflect competitive pricing pressure, a shift toward different product tiers, or evolving buyer preferences within these accounts. The pattern is worth a focused conversation — particularly for accounts where current-quarter volume remains strong, suggesting the relationship is active but the product mix is shifting."

### 10. Order Timing Patterns (Q-69) `[COLLAPSE]`

**Gate**: Render ONLY if `cache/Q-69_results.md` exists AND contains data rows.

**Data source**: `cache/Q-69_results.md`

**Status**: New query — requires integration into `data_gather.py` before this subsection will render.

**Rendering**: Open with a `.callout.insight` identifying the peak and gap pattern: "X% of your orders are placed Monday–Wednesday, with Friday accounting for only Y% of weekly volume. Your peak selling hour is Z:00, suggesting [pattern]."

Then render a compact day-of-week summary table:

| Column | Content |
|--------|---------|
| Day | Day of week |
| Orders | Order count |
| Share | Percentage of weekly total |
| GMV | Total GMV for that day |
| Avg Order | Average order value |

After the table, add a what-this-means close framing timing gaps as scheduling opportunities: "If your team added consistent Friday selling activity, matching even half of your Tuesday volume, that could represent $X in additional weekly GMV." Use hedging language.

**Claim rules**: Frame gaps as scheduling opportunities, not rep failures. Never expose raw timestamps. Use "your team's selling patterns" not "order submission times."

## Section-Specific Rules

**VM-45 denominator gate**: The section agent reads `VM45_RENDER` from `gate_flags.md`. Stage 1 pre-computes the two-gate validity check (Gate 1: `portal_orders_gmv > ecat_gmv`; Gate 2: `ecat_gmv >= 5% of portal_orders_gmv`). If `VM45_RENDER = false`, skip subsection 6 silently (Channel Mix & Capture Rate renders total business context only). Do not re-derive the gate. Do not render a fallback capture rate without a valid denominator.

**If `HAS_PORTAL_ORDERS = false`**: Commerce Analytics shows eCat-only data. Do not mention ERP, total business, or `portal_orders` at all in this section. Subsections 1 Part B, 6, and 7 are all skipped.

**Channel attribution statement** (required in section body when `HAS_CART = true`): "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." Do not use code literals like `order_source = 'ipad'` in client-facing prose.

## Data Confidence Footer

**You MUST render this footer.** Follow the numbered steps below exactly. Do NOT skip or reorder them.

**STEP 1 — Read the tier (MANDATORY).** Open `cache/section_confidence.md` and read the EXACT value of `SECTION_CONFIDENCE_5`. It is one of: `FULL`, `STRONG`, `PARTIAL`, `LIMITED`. **Use THIS value. Do NOT infer or recompute the tier from gate flags — the data gathering script already computed it.**

**STEP 2 — Select the template** matching the tier from STEP 1:

| STEP 1 value | Template | Label |
|---|---|---|
| `FULL` | `§5-FULL` | `FULL PICTURE` |
| `STRONG` | `§5-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§5-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§5-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

Resolve template variables: `{{LAST_PORTAL_ORDER_DATE}}` from enrichment preflight in `gate_flags.md`. If it can't be resolved for FULL or STRONG, fall back to `§5-PARTIAL`.

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

If STEP 1 value is `LIMITED`, use `<div class="data-confidence limited">` instead.

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Rep-level performance, coaching, or behavioral analysis → belongs in §2 Sales Team Performance
2. Customer activation, dormancy, or buyer-level analysis → belongs in §3 Customer & Buyer Intelligence
3. Product catalog health, inventory status, or sales-line analysis → belongs in §4 Product & Inventory
4. Portal traffic, Clicky analytics, or geographic demand → belongs in §6 Demand Signal Intelligence
5. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
6. Platform feature utilization or data freshness → belongs in §8 Platform & Feature
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Conditional Subsection Checklist (verify before saving fragment)

Before writing `fragments/section_05.html`, confirm each item. Every checked box must be TRUE for the fragment to ship.

| # | Subsection | Gate Condition | Action When Met | Action When Not Met |
|---|-----------|----------------|-----------------|---------------------|
| 1A | eCat Order Trend | Always | Render eCat-only trend table | — |
| 1B | eCat Share of Total | `HAS_PORTAL_ORDERS = true` | Add total business columns to trend | Skip Part B silently |
| 2 | AOV by Segment | Always | Render segment AOV table | — |
| 3 | Channel Breakdown | `HAS_CART = true` | Render iPad vs Online split | Skip silently |
| 4 | Top Buyers (base) | Always | Render Q-13 top-10 table | — |
| 4+ | Top Buyers enrichment | `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-52` has rows | Add "Total Business" + "eCat Share" columns | Render Q-13-only table |
| 5 | Order Type & Workflow | Always | Render quote premium callout + collapsed type table | — |
| 6 | Channel Mix & Capture Rate | `HAS_PORTAL_ORDERS = true` | Render total business + capture rate (if VM45_RENDER=true) | Skip silently |
| 7A | Category Displacement | `HAS_PORTAL_ORDERS = true` + `Q-55` has displacement rows | Render displacement table + alert callout | Skip silently |
| 7B | Rep Capture Trend | `PORTAL_REP_DATA_PRESENT = true` + `Q-56` has declining reps | Render rep decline table | Skip Part B silently |
| 8 | Market Commitment | `HAS_COMMITMENT_DATA = true` + `Q-58` has rows | Render market conversion table | Skip silently |
| 8B | In-Stock Actionable | `HAS_COMMITMENT_DATA = true` + `HAS_INVENTORY = true` + `Q-58b` has rows | Render `.callout.opportunity` + in-stock table | Skip Part B silently |
| 9 | Price Erosion | `HAS_PORTAL_ORDERS = true` + `Q-60` has rows | Render `.callout.warn` + accounts table + `.callout.insight` | Skip silently |
| 10 | Order Timing Patterns | `Q-69` has rows (new query) | Render day-of-week table inside `[COLLAPSE]` | Skip silently |

**Final checks:**

- [ ] Every rendered subsection ends with a `<div class="what-this-means">` block (analyst-quality, actionable)
- [ ] `HAS_PORTAL_ORDERS = false` → subsections 1B, 6, 7, 9 all skipped, no "total business" mentions anywhere
- [ ] No "ERP," "Mixpanel," health scores, segment labels, or internal identifiers in rendered HTML
- [ ] `portal_orders` is referenced only as "total business" — never "portal ordering" or "buyer self-service"
- [ ] Q-60 prose is investigative (hedged, multi-causal) — `.badge.danger` on numbers only
- [ ] Q-58b uses `.callout.opportunity` (green border) — NOT `.callout.success`
- [ ] Confidence footer present and matches `SECTION_CONFIDENCE_5` tier (rendered at ALL tiers including FULL)
- [ ] `section-contents` middot list reflects ONLY subsections actually rendered (not skipped ones)

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

### Q-13_results.md

# Q-13 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-13 — Customer Concentration Risk
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 15
- **Run date**: 2026-06-16


| customer_num | bill_to_company_name | orders | gmv | pct_of_ecat_gmv |
| --- | --- | --- | --- | --- |
| 6759 | WICHITA FURNITURE INC | 34 | $429,630 | $4 |
| 1770 | MISKELLYS FURNITURE WAREHOUSE INC | 25 | $429,495 | $4 |
| 23269 | ENCORE RESALES INC | 39 | $261,420 | $2 |
| 23649 | CREATIVE CONCEPTS OF BETHANY | 8 | $221,929 | $2 |
| 15688 | TOUCH OF BRASS | 20 | $195,555 | $2 |
| 2444 | FURNITURE WAREHOUSE SALES | 7 | $172,610 | $2 |
| 36893 | CREATIVE DISPLAYS AND DESIGNS INC | 17 | $167,690 | $2 |
| 44863 | COMPASS INTERIORS LLC | 7 | $164,325 | $1 |
| 54584 | SEAWAH FURNITURE AND DESIGN LLC | 5 | $153,505 | $1 |
| 20449 | LYNCH APPLIANCE CENTER INC | 12 | $153,190 | $1 |
| 42741 | COASTAL INTERIORS INC | 4 | $147,410 | $1 |
| 2922 | BIRMINGHAM WHOLESALE FURNITURE | 8 | $137,320 | $1 |
| 27506 | MARATHON FURNISHINGS INC | 9 | $134,388 | $1 |
| 90418 | UNCLAIMED FURNITURE OF THE UPSTATE | 6 | $124,560 | $1 |
| 1816 | MAYNARDS HOME FURNISHINGS | 10 | $123,026 | $1 |

### Q-16_results.md

# Q-16 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-16 — ERP Total Business Visibility
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-18_partA_results.md

# Q-18-A Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-18-A — eCat Order Velocity — Part A
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 13
- **Run date**: 2026-06-16


| month | total_ecat_orders | ipad_orders | ecat_online_orders | ecat_gmv | ecat_aov |
| --- | --- | --- | --- | --- | --- |
| 2026-6-1 | 90 | 90 | 0 | $646,432 | $7,183 |
| 2026-5-1 | 220 | 220 | 0 | $1.6M | $7,412 |
| 2026-4-1 | 248 | 248 | 0 | $1.7M | $7,016 |
| 2026-3-1 | 180 | 180 | 0 | $1.0M | $5,629 |
| 2026-2-1 | 147 | 147 | 0 | $1.2M | $7,934 |
| 2026-1-1 | 158 | 158 | 0 | $989,308 | $6,261 |
| 2025-12-1 | 174 | 174 | 0 | $878,662 | $5,050 |
| 2025-11-1 | 174 | 174 | 0 | $1.1M | $6,506 |
| 2025-10-1 | 201 | 201 | 0 | $1.5M | $7,344 |
| 2025-9-1 | 156 | 156 | 0 | $876,752 | $5,620 |
| 2025-8-1 | 160 | 160 | 0 | $1.0M | $6,299 |
| 2025-7-1 | 158 | 158 | 0 | $633,771 | $4,011 |
| 2025-6-1 | 62 | 62 | 0 | $234,093 | $3,776 |

### Q-18_partB_results.md

# Q-18-B Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-18-B — eCat Order Velocity — Part B (ERP)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 13
- **Run date**: 2026-06-16


| month | total_erp_orders | total_erp_gmv |
| --- | --- | --- |
| 2026-6-1 | 2,397 | $5.2M |
| 2026-5-1 | 5,506 | $13.0M |
| 2026-4-1 | 5,217 | $12.9M |
| 2026-3-1 | 5,160 | $12.0M |
| 2026-2-1 | 4,648 | $11.8M |
| 2026-1-1 | 4,618 | $10.7M |
| 2025-12-1 | 4,576 | $10.4M |
| 2025-11-1 | 4,863 | $11.9M |
| 2025-10-1 | 5,613 | $12.6M |
| 2025-9-1 | 5,847 | $12.5M |
| 2025-8-1 | 5,017 | $10.2M |
| 2025-7-1 | 5,082 | $9.9M |
| 2025-6-1 | 2,206 | $4.3M |

### Q-20_results.md

# Q-20 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-20 — eCat AOV Analysis
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 4
- **Run date**: 2026-06-16


| dimension | order_count | avg_order_value | total_ecat_gmv |
| --- | --- | --- | --- |
| Quote Orders | 18 | $14,472 | $260,493 |
| All eCat Orders | 2,128 | $6,309 | $13.4M |
| iPad Orders | 2,128 | $6,309 | $13.4M |
| eCat Online Orders | 0 | — | — |

### Q-21_results.md

# Q-21 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-21 — eCat Order Type & Workflow Analysis
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 3
- **Run date**: 2026-06-16


| order_type | orders | pct | gmv | avg_value |
| --- | --- | --- | --- | --- |
| Confirmed | 2,108 | 99.10 | $13.1M | 6,230.41 |
| Quote | 18 | 0.80 | $260,493 | 14,471.85 |
| HFC | 2 | 0.10 | $31,070 | 15,535 |

### Q-45_results.md

# Q-45 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-45 — eCat Capture Rate vs. Total Business
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| ecat_order_count | erp_order_count | ecat_order_capture_pct | ecat_gmv | erp_gmv | ecat_gmv_capture_pct | ecat_posture |
| --- | --- | --- | --- | --- | --- | --- |
| 2,128 | 60,750 | 3.50 | $13.4M | $137.4M | 9.80 | Enablement-heavy; eCat captures little of total volume |

### Q-52_results.md

# Q-52 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-55_results.md

# Q-55 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-55 — Category-Level Competitive Displacement
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-56_results.md

(not present — file does not exist or is empty)

### Q-58_results.md

# Q-58 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-58 — Market Commitment Conversion
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 4
- **Run date**: 2026-06-16


| market_code | market_start_date | market_end_date | customers_committing | total_committed_items | total_committed_qty | items_converted | item_conversion_pct | total_ordered_qty | qty_conversion_pct | unrealized_items |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| APR2026 | 2026-4-24 | 2026-5-8 | 114 | 161 | 13,750 | 91 | 56.50 | 1,734 | 12.60 | 70 |
| OCT2025 | 2025-10-23 | 2025-11-6 | 180 | 234 | 22,801 | 102 | 43.60 | 15,665 | 68.70 | 132 |
| APR2025 | 2025-4-27 | 2025-5-6 | 178 | 189 | 9,835 | 146 | 77.20 | 7,841 | 79.70 | 43 |
| OCT2024 | 2024-10-23 | 2024-11-5 | 130 | 196 | 5,584 | 114 | 58.20 | 4,003 | 71.70 | 82 |

### Q-58b_results.md

# Q-58b Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-58b — Uncommitted Market Items In Stock
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-60_results.md

# Q-60 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-60 — Price Erosion / Trade-Down Detection
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| customer_bill_to_name | prior_avg_price | current_avg_price | price_change_pct | current_quarter_gmv | prior_quarter_gmv | current_orders | current_line_items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WAYFAIR LLC | 597.93 | 559.40 | -6.40 | $2.4M | $1.8M | 2,993 | 3,876 |
| CITY FURNITURE INC | 622.99 | 415.81 | -33.30 | $1.7M | $2.6M | 31 | 1,758 |
| STEWARTS SLEEP CTR/MATTER BROTHERS | 541.41 | 494.19 | -8.70 | $1.1M | $1.2M | 81 | 550 |
| HAVERTY FURNITURE COMPANIES INC | 347.50 | 315.26 | -9.30 | $625,120 | $295,745 | 14 | 117 |
| NEBRASKA FURNITURE MART | 566 | 498.87 | -11.90 | $512,147 | $462,043 | 126 | 350 |
| ROBB & STUCKY INTERNATIONAL INC | 747.39 | 717.35 | -4 | $320,530 | $400,193 | 111 | 165 |
| BLANDFORD HOMES LLC | 1,122.65 | 739.66 | -34.10 | $283,192 | $26,983 | 32 | 328 |
| GREEN FRONT FURNITURE | 766.51 | 669.55 | -12.60 | $252,079 | $90,883 | 55 | 208 |
| AFA STORES | 792.50 | 754.28 | -4.80 | $222,996 | $330,857 | 238 | 268 |
| HUDSONS FURNITURE | 567.49 | 476.70 | -16 | $200,529 | $169,759 | 38 | 249 |
| COMPASS INTERIORS LLC | 839.08 | 710.28 | -15.30 | $150,678 | $56,610 | 35 | 162 |
| THE PULTE GROUP | 845.56 | 762.20 | -9.90 | $150,030 | $249,350 | 69 | 153 |
| BRIGAN INC | 481.05 | 418.33 | -13 | $139,533 | $113,068 | 44 | 331 |
| CREATIVE CONCEPTS OF BETHANY | 539.03 | 484.36 | -10.10 | $137,728 | $131,512 | 40 | 198 |
| CLIVE DANIEL HOME | 737.03 | 651.87 | -11.60 | $112,737 | $100,392 | 79 | 118 |
| BISON COMMERCE LLC | 400.05 | 371.41 | -7.20 | $111,619 | $77,802 | 191 | 196 |
| MGL PARTNERS LLC | 666.54 | 637.55 | -4.30 | $109,212 | $92,272 | 63 | 141 |
| KOPER FURNITURE INC | 792.50 | 198.99 | -74.90 | $108,780 | $134,865 | 5 | 82 |
| WICHITA FURNITURE INC | 858.80 | 742.58 | -13.50 | $106,172 | $142,080 | 30 | 106 |
| BACON'S FURNITURE GALLERIES | 666.18 | 614.24 | -7.80 | $95,300 | $85,184 | 37 | 109 |

### Q-69_results.md

(not present — file does not exist or is empty)
