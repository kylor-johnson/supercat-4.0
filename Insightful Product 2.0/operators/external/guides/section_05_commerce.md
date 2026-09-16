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
