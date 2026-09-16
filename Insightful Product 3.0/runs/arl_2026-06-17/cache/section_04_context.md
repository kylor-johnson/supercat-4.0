# Section 4 Context Bundle — Arabela Lighting (arl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Arabela Lighting (arl, org_id=269)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=77 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=4 engagement_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Catalog-Focused |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 4 | 4 |
| ENGAGEMENT_REP_COUNT | 17 | engagement_reps=17 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 64 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | True | Postgres LTM orders: 314, Mixpanel total submit_order (Q-01): 0 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=89.1%, ambiguous_rate=0.0%, showroom_event_share=46.9% |
| USER_GROUP_JOIN_RATE | 89% | 57 of 64 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 47% | showroom+admin share of matched events: 46.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 3 admin/showroom users in leaderboard: Lee Nemeth, Nadia Quintero, Sophia Wang |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | False | inventories last_updated 188d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | False | customers last_updated 85d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=196 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | LIMITED | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Arabela Lighting
- **Shortname**: arl
- **Org ID**: 269
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Arabela Lighting (arl, org_id=269)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| PORTAL_ORDERS_FRESH | False |
| HAS_PORTAL_ORDERS | False |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | False |
| INVENTORY_FRESH | False |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | False |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | LIMITED | See Derived Gate 6 §4 formula |
| §5 Commerce | PARTIAL | See Derived Gate 6 §5 formula |

## Section Guide — section_04_commerce.md

# Section Guide: Commerce Patterns
> **v3.0** — signal-first architecture. Only non-obvious patterns a client can't see in their own systems.

## Section Identity

- **id**: `commerce`
- **title**: Commerce Patterns
- **section number**: 4
- **include when**: `signal_rank.md` shows ≥ 1 P0/P1 signal with `Section Home = Commerce Patterns`, OR at least 3 of the 12 subsections below pass their individual gates
- **skip when**: 0 relevant P0/P1 signals AND fewer than 3 subsections have data

## Query Inputs

Read these cache files:

- `cache/signal_rank.md` — ranked signal manifest
- `cache/Q-13_results.md` — Customer concentration risk (top-buyer eCat GMV share)
- `cache/Q-18_results.md` — eCat order trend, channel breakdown, and rep-level performance
- `cache/Q-19_results.md` — Order channel mix (iPad vs eCat Online vs other)
- `cache/Q-20_results.md` — Order type breakdown (Confirmed, Quote, etc.)
- `cache/Q-21_results.md` — Order type & workflow distribution
- `cache/Q-41_results.md` — New eCat buyer acquisition trend
- `cache/Q-45_results.md` — eCat capture rate
- `cache/Q-52_results.md` — eCat penetration of total business by customer (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 4 Top Buyers table MUST include enrichment columns)
- `cache/Q-55_results.md` — Category-level competitive displacement (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains displacement rows, subsection 9 MUST be rendered)
- `cache/Q-56_results.md` — Per-rep capture rate trend (conditional: render Part B of subsection 9 if `PORTAL_REP_DATA_PRESENT = true` AND data rows show declining reps)
- `cache/Q-58_results.md` — Market commitment conversion (**MANDATORY when gate met**: if `HAS_COMMITMENT_DATA = true` AND this file contains data rows, subsection 11 MUST be rendered)
- `cache/Q-58b_results.md` — Uncommitted market items in stock (conditional: render Part B of subsection 11 if `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND data rows exist)
- `cache/Q-60_results.md` — Price erosion / trade-down detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains data rows, subsection 10 MUST be rendered)
- `cache/Q-69_results.md` — Order timing distribution (reserved for future use)
- `cache/Q-ORG-VELOCITY_results.md` — Account velocity patterns
- `cache/gate_flags.md` — data availability gates
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_4` tier

## CRITICAL REQUIREMENTS — Read Before Building

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **Q-52 MANDATORY ENRICHMENT**: If `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `Q-52_results.md` has data rows, the Top Buyers table (subsection 4) MUST include "Total Business" and "eCat Share" columns.
2. **HAS_PORTAL_ORDERS GATE**: If `HAS_PORTAL_ORDERS = false`, subsections 1 (Part B of eCat Capture Rate), 3 (Channel Migration share-of-total overlay), 9 (Competitive Displacement), and 10 (Price Erosion) are ALL skipped. Do not mention total business anywhere.
3. **Q-55 COMPETITIVE DISPLACEMENT**: If `HAS_PORTAL_ORDERS = true` AND `Q-55_results.md` has rows where total grew but eCat share shrank, subsection 9 MUST be rendered. MANDATORY.
4. **Q-60 PRICE EROSION**: If `HAS_PORTAL_ORDERS = true` AND `Q-60_results.md` has data rows, subsection 10 MUST be rendered. MANDATORY.
5. **Q-58 MARKET ATTRIBUTION**: If `HAS_COMMITMENT_DATA = true` AND `Q-58_results.md` has data rows, subsection 11 MUST be rendered. MANDATORY.
6. **Q-58b IN-STOCK ITEMS**: If `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND `Q-58b_results.md` has data rows, subsection 11 Part B MUST be rendered.
7. **CONFIDENCE HEADER**: Every §4 fragment MUST contain a confidence header **at the top of the section** (immediately after the header metrics, before any subsection content). This is NOT optional — if the confidence header is missing, the fragment is defective. Read `SECTION_CONFIDENCE_4` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags.

---

## PRE-BUILD GATE CHECK

> Follow `section_shared_contract.md` §1 for the gate check process.

| Flag | Used by |
|------|---------|
| `HAS_PORTAL_ORDERS` | Subsections 1 (Part B), 3 (share overlay), 9, 10 |
| `HAS_CART` | Subsection 3 (channel breakdown) |
| `HAS_COMMITMENT_DATA` | Subsection 11 |
| `HAS_INVENTORY` | Subsection 11 (Part B) |
| `VM45_RENDER` | Subsection 1 (capture rate denominator validity) |
| `PORTAL_CUSTOMER_DATA_PRESENT` | Subsection 4 (Q-52 enrichment) |
| `PORTAL_REP_DATA_PRESENT` | Subsection 9 (Part B) |

---

## Fragment Structure

Uses the standard `<details class="section-collapse">` wrapper per shared_rules.md Section E.

```
Section ID: commerce
Section Number: §4
```

---

## Guiding Principle

**Our value = cross-system patterns only our data position enables.** If a client could pull this from their own dashboard, don't show it. Every subsection must reveal something that requires cross-referencing eCat behavioral data, multi-source order data, or platform-specific intelligence.

---

## Content Blocks (render in NARRATIVE ARC order — each is independently gated)

**Rendering order within this section (strength → intelligence → opportunity → risk):**
1. Digital Ordering Share (STRENGTH — what share you've won)
2. eCat Order Trend (STRENGTH — the growth trajectory)
4. Top Buyers & Concentration (INTELLIGENCE — who's buying)
6. Order Type & Workflow (INTELLIGENCE — how they're buying)
3. Channel Migration (INTELLIGENCE — where they're buying)
11. Market Commitment Attribution (OPPORTUNITY — pipeline conversion)
5. Quote Economics (OPPORTUNITY — conversion upside)
8. AOV Spread by Rep (OPPORTUNITY — coaching upside)
12. First-Time Buyer Acquisition (INTELLIGENCE — pipeline health)
7. Seasonal Timing (INTELLIGENCE — timing patterns)
9. Competitive Displacement (RISK — render late)
10. Price Erosion (RISK — render last)

### 1. Digital Ordering Share (conditional)

**Gate**: `HAS_PORTAL_ORDERS = true` (from gate_flags) AND gate_flags shows commerce data sufficient for capture rate computation.

What share of total business flows through eCat, trending over time.

```html
<div class="subsection">
  <div class="subsection-title">Digital Ordering Share</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val">{{CAPTURE_PCT}}%</div>
      <div class="metric-label">Share of Orders Through eCat</div>
      <div class="metric-note">Trailing 12 months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">{{CLASSIFICATION}}</div>
      <div class="metric-label">Adoption Stage</div>
      <div class="metric-note">{{CLASSIFICATION_DEFINITION}}</div>
    </div>
  </div>
```

**Classification tiers** (render as `.badge` with color):
- **Dominant** (> 60%): `.badge.ok` — "More than 60% of total business flows through eCat"
- **Significant** (30–60%): `.badge.ok` — "eCat handles 30–60% of total business"
- **Emerging** (10–30%): `.badge.warn` — "eCat is established but handles under 30% of orders"
- **Early** (< 10%): `.badge.danger` — "Less than 10% of total business flows through eCat"

If quarterly trend data available, show the trajectory: QoQ capture rate change. Use `.callout.insight` if the trend is meaningful (> 2pp change QoQ).

If `VM45_RENDER = false` (denominator gate failed): render total business context only with a metrics grid showing all-channel business volume. Do NOT attempt an ordering share calculation without a valid denominator. Add a single prose line: "Digital ordering share analysis requires consistent data between eCat and total-business records — this will be available when data synchronization is validated."

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CAPTURE_RATE_IMPLICATION}}. {{TREND_IMPLICATION}}. {{If early/emerging: "Moving from X% to Y% capture would add an estimated $Z in orders placed through eCat — the customers already exist, the ordering behavior just needs to shift."}}
  </div>
</div>
```

**Data source**: `Q-45_results.md`, `Q-16_results.md`

**Claim rules**: Frame the gap as opportunity, not failure. If the share is low (< 15%), frame as runway with a dollar-equivalent projection (hedged). If high (> 30%), celebrate eCat adoption. Always hedge projections with "estimated," "approximately," or "potential." Never say "platform capture rate" in client-facing text — say "digital ordering share" or "share of orders through eCat."

---

### 2. eCat Order Trend (always)

**Gate**: Always render Part A. Part B conditional on `HAS_PORTAL_ORDERS = true`.

**Data source**: `Q-18_results.md`

**Part A** (always): eCat order trend — eCat-originated orders only. Show monthly or quarterly volume over time.

```html
<div class="subsection">
  <div class="subsection-title">eCat Order Trend</div>
  <table>
    <tr><th>Period</th><th>eCat Orders</th><th>eCat GMV</th><th>Avg Order Value</th></tr>
    {{ROWS — one per month/quarter, chronological}}
  </table>
```

**Part B** (only if `HAS_PORTAL_ORDERS = true`): Add eCat share of total business trend alongside Part A. Extend the table with additional columns:

```html
  <table>
    <tr><th>Period</th><th>eCat Orders</th><th>eCat GMV</th><th>Total Business</th><th>eCat Share</th><th>Avg Order Value</th></tr>
    {{ROWS — one per month/quarter, chronological, with total business and share columns}}
  </table>
```

**What-this-means guidance**: Frame like an analyst comparing seasonality to growth. Highlight peak months, note partial-period artifacts, and contextualize whether the trend is stable, accelerating, or cyclical. Example: "eCat ordering peaked in [month] with consistent monthly volume of X–Y orders. The partial-month dip at period boundaries reflects data truncation, not declining demand."

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{TREND_NARRATIVE — contextualize whether volume is stable, accelerating, seasonal, or cyclical. Highlight the peak period and note any partial-period artifacts at data boundaries.}}
  </div>
</div>
```

**Claim rules**: Never attribute a partial-period drop to declining demand without explicit evidence. Always note when the first or last period in the range is truncated. If Part B is present, frame the eCat share trajectory — is it growing, flat, or declining relative to total business?

---

### 3. Channel Migration / Channel Breakdown (conditional)

**Gate**: `order_origin` or `order_source` populated across orders, with at least 2 distinct channels AND 6+ months of history. If `HAS_CART = true`, render iPad vs eCat Online channel split from Q-18 data.

**Data source**: `Q-18_results.md`, `Q-19_results.md`

Shifts between iPad / eCat Online / other channels over time.

```html
<div class="subsection">
  <div class="subsection-title">Channel Migration</div>
  <table>
    <tr><th>Channel</th><th>Prior Period GMV</th><th>Current Period GMV</th><th>Share Change</th><th>Order Count Change</th></tr>
    {{ROWS — one per channel}}
  </table>
```

Key question to answer: Is self-service (eCat Online) growing relative to rep-mediated (iPad)? Frame the shift narrative:

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CHANNEL_SHIFT_NARRATIVE — e.g., "Self-service ordering grew from X% to Y% of platform volume. Your buyers are increasingly comfortable ordering without rep involvement — protect this by ensuring the online catalog and pricing are current."}}
  </div>
</div>
```

**Channel attribution statement** (required when `HAS_CART = true`): "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." Do not use code literals like `order_source = 'ipad'` in client-facing prose.

**What-this-means guidance**: Frame the channel mix as adoption signal. If one channel dominates, explain what that implies about buyer behavior. Example: "100% iPad ordering reflects a rep-driven sales model. Activating eCat Online would add a self-service channel for reorders and lower-touch accounts without displacing rep relationships."

**Claim rules**: Never use "portal ordering" — say "self-service ordering" or "eCat Online." Frame channel shifts as adoption evolution, not channel conflict.

---

### 4. Top Buyers & Concentration (always)

**Gate**: Always render. Q-52 enrichment is MANDATORY when `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-52_results.md` exists with data rows.

**Data source**: `Q-13_results.md`, `Q-52_results.md` (when gate met)

Show top 10 buyers by eCat GMV with these exact columns:

| Column | Content |
|--------|---------|
| Customer | Buyer name |
| Orders | eCat order count |
| GMV | eCat GMV |
| % of eCat GMV | Buyer's share of total eCat GMV |

```html
<div class="subsection">
  <div class="subsection-title">Top Buyers & Concentration</div>
```

Include a concentration callout if top-5 buyers exceed 25% of total eCat GMV:

```html
  <div class="callout insight">
    <div class="callout-title">Revenue Concentration</div>
    <p>Your top 5 eCat buyers account for {{TOP5_PCT}}% of total platform GMV (${{TOP5_GMV}} of ${{TOTAL_GMV}}). {{CONCENTRATION_IMPLICATION}}.</p>
  </div>
```

```html
  <table>
    <tr><th>Customer</th><th>Orders</th><th>GMV</th><th>% of eCat GMV</th></tr>
    {{ROWS — top 10 by GMV, sorted descending}}
  </table>
```

**MANDATORY ENRICHMENT** (when `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-52_results.md` exists with data rows): You MUST add two columns to the table using `cache/Q-52_results.md` data joined on customer identifier — "Total Business" (all-channel GMV) and "eCat Share" (`ecat_gmv / total_business_gmv × 100`). When `PORTAL_CUSTOMER_DATA_PRESENT = false` OR the file is absent OR it contains zero rows, render the Q-13-only table unchanged — do not add empty columns or placeholders.

Enriched table header when Q-52 is available:

```html
  <table>
    <tr><th>Customer</th><th>Orders</th><th>GMV</th><th>% of eCat GMV</th><th>Total Business</th><th>eCat Share</th></tr>
    {{ROWS — top 10 by GMV, sorted descending, with total business and penetration columns from Q-52}}
  </table>
```

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CONCENTRATION_NARRATIVE — assess concentration risk like a portfolio analyst. Low concentration = stability but broad-based growth needed. High concentration = key-account dependency risk. When enrichment is present, highlight penetration gaps: "Your largest eCat buyer generates $X on the platform but $Y in total business — there's headroom to capture more of their spend digitally."}}
  </div>
</div>
```

**Claim rules**: Never expose internal customer identifiers (`customer_bill_to_number`, etc.). Use buyer names only. Frame concentration as portfolio risk analysis. When enrichment is present, frame penetration gaps as growth opportunity.

---

### 5. Quote Economics (conditional)

**Gate**: `Q-20_results.md` or `Q-45_results.md` shows Quote-type orders AND Confirmed-type orders with sufficient volume (10+ quotes).

**Data source**: `Q-20_results.md`, `Q-45_results.md`

The spread between Quote AOV and Confirmed AOV, and the dollar opportunity if conversion improved.

```html
<div class="subsection">
  <div class="subsection-title">Quote Economics</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val">${{QUOTE_AOV}}</div>
      <div class="metric-label">Avg Quote Value</div>
      <div class="metric-note">{{QUOTE_COUNT}} quotes, trailing 12 months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${{CONFIRMED_AOV}}</div>
      <div class="metric-label">Avg Confirmed Order Value</div>
      <div class="metric-note">{{CONFIRMED_COUNT}} orders, trailing 12 months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${{SPREAD}}</div>
      <div class="metric-label">AOV Spread</div>
      <div class="metric-note">Quotes {{HIGHER_OR_LOWER}} than confirmed</div>
    </div>
  </div>
  <p class="prose">If quote-to-confirmed conversion improved by 10 percentage points, that's an estimated ${{INCREMENTAL}} in incremental annual revenue.</p>
  <div class="what-this-means">
    <strong>Action:</strong> {{QUOTE_ECONOMICS_IMPLICATION — e.g., "Quotes are 40% larger than confirmed orders on average, which means your highest-value opportunities are the ones most likely to stall. Focus rep follow-up on quotes > $X to capture the top of the pipeline."}}
  </div>
</div>
```

Hedge the 10pp improvement projection with "estimated" language.

**Claim rules**: Always hedge conversion improvement projections. Never promise specific ROI — use "estimated," "potential," "approximately."

---

### 6. Order Type & Workflow (always)

**Gate**: Always render. Build from `Q-21_results.md`.

**Data source**: `Q-21_results.md`

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

```html
<div class="subsection">
  <div class="subsection-title">Order Type & Workflow</div>
  <div class="callout insight">
    <div class="callout-title">Quote Premium</div>
    <p>Your quote orders average ${{QUOTE_AOV}} — {{MULTIPLIER}}x the standard confirmed order value (${{CONFIRMED_AOV}}). Increasing quote-to-confirmed conversion is your highest-leverage volume opportunity.</p>
  </div>
  <details>
    <summary>View order type breakdown</summary>
    <table>
      <tr><th>Order Type</th><th>Orders</th><th>Share</th><th>Avg Order Value</th></tr>
      {{ROWS — one per order type, sorted by order count descending}}
    </table>
  </details>
```

- If HFC (Hold for Confirmation) orders exist, note in prose that the approval workflow serves compliance or high-value transaction governance.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{ORDER_TYPE_IMPLICATION — Focus on the actionable insight from the type distribution, not the distribution itself. Example: "The Nx AOV premium on quotes means each converted quote is worth N standard orders. If even X% more quotes converted to confirmed, that would add $Y in platform GMV." Do not restate "96% of your orders are confirmed" — the reader can see that in the collapsed table.}}
  </div>
</div>
```

**Claim rules**: Lead with the non-obvious insight (quote premium multiplier), not the obvious (order type distribution). Hedge conversion improvement estimates. Never expose internal order type codes.

---

### 7. Seasonal Timing (conditional)

**Gate**: 12+ months of order data available (check Q-21 for monthly time series spanning at least 12 months).

**Data source**: `Q-21_results.md`

Monthly revenue pattern with peak identification.

```html
<div class="subsection">
  <div class="subsection-title">Ordering Seasonality</div>
  <table>
    <tr><th>Month</th><th>Avg Monthly Revenue</th><th>% of Annual</th><th>Relative Intensity</th></tr>
    {{12 ROWS — one per month, averaged across available years}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> Your ordering peaks in {{PEAK_MONTHS}} — align inventory builds, rep outreach campaigns, and new product launches to lead these peaks by 4–6 weeks. {{TROUGH_INSIGHT — e.g., "The Q3 trough (July–August) may be an opportunity for targeted promotions to flatten the curve."}}
  </div>
</div>
```

"Relative Intensity" column: show as a visual indicator. Use `.badge.ok` for peak months (> 10% of annual), `.badge.muted` for average months, `.badge.warn` for trough months (< 6% of annual). `[COLLAPSE]`

**Claim rules**: Frame troughs as promotional opportunities, not failures. Never attribute seasonality to a single cause without evidence.

---

### 8. AOV Spread by Rep (conditional)

**Gate**: `Q-18_results.md` shows rep-level AOV data AND the spread between highest and lowest active rep AOV is > 2x.

**SKIP if spread ≤ 2x.** A small spread is normal and not actionable.

**Data source**: `Q-18_results.md`

```html
<div class="subsection">
  <div class="subsection-title">Average Order Value Spread by Rep</div>
  <div class="callout insight">
    <div class="callout-title">{{SPREAD_RATIO}}x AOV gap across your team</div>
    <p>Your highest-AOV rep averages ${{HIGH_AOV}} per order. Your lowest: ${{LOW_AOV}}. If the bottom quartile matched the median (${{MEDIAN_AOV}}), that's an estimated ${{UPSIDE}} in incremental annual revenue.</p>
  </div>
  <table>
    <tr><th>Rep</th><th>Orders (LTM)</th><th>GMV (LTM)</th><th>AOV</th><th>vs Median</th></tr>
    {{ROWS — sorted by AOV desc, top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> A large AOV spread usually means reps are selling into different customer segments, or some reps are better at bundling and upselling. Investigate whether low-AOV reps are serving smaller accounts (normal) or leaving money on the table with the same customers (coachable).
  </div>
</div>
```

"vs Median" column: `.badge.ok` if above median, `.badge.warn` if below. Show as percentage above/below.

**Claim rules**: Frame AOV gaps as coaching opportunity, not rep failure. Always acknowledge that customer mix may explain differences.

---

### 9. Competitive Displacement Signals (conditional) — MANDATORY WHEN GATE MET

**Gate**: `HAS_PORTAL_ORDERS = true` — if false, skip this entire subsection silently.

**MANDATORY RENDER**: If `cache/Q-55_results.md` exists AND contains data rows showing at least one category where `total_growth_pct > 0` AND `ecat_share_change_ppts < 0`, this subsection MUST appear. If no category meets the displacement criteria (total grew but eCat share shrank), skip silently — no false alarm.

**Data sources**: `cache/Q-55_results.md` (category displacement), `cache/Q-56_results.md` (rep capture trend)

**Part A — Category Displacement (Q-55):**

Open with a `.callout.insight` (NOT `.callout.alert`) titled "Channel Share Opportunity". Frame as recapturable revenue, not loss.

```html
<div class="subsection">
  <div class="subsection-title">Channel Share Opportunity</div>
  <div class="callout insight">
    <div class="callout-title">Platform Share Gap in Growing Categories</div>
    <p>In {{COUNT}} categories, total business grew while platform share declined — an estimated ${{DISPLACED_TOTAL}} in additional platform revenue is available if channel share is recovered.</p>
  </div>
  <table>
    <tr>
      <th>Category</th>
      <th>Total Business (Current Qtr)</th>
      <th>Total Growth</th>
      <th>Platform Share (Prior)</th>
      <th>Platform Share (Current)</th>
      <th>Share Change</th>
      <th>Est. Displaced</th>
    </tr>
    {{ROWS — categories where total_growth_pct > 0 AND ecat_share_change_ppts < 0}}
  </table>
```

Render table with categories that show displacement (where `total_growth_pct > 0` AND `ecat_share_change_ppts < 0`):

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

```html
  <h4>Rep Capture Rate Trend</h4>
  <table>
    <tr>
      <th>Rep</th>
      <th>Total Business (Current)</th>
      <th>Prior Capture %</th>
      <th>Current Capture %</th>
      <th>Change</th>
    </tr>
    {{ROWS — reps where capture_change_ppts < 0, sorted by current_total_gmv desc, top 5 visible}}
  </table>
```

Show only reps where `capture_change_ppts < 0` (declining), sorted by `current_total_gmv` descending. Top 5 visible, remaining in `<details>`. If no reps show decline, omit Part B silently.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{DISPLACEMENT_NARRATIVE — investigative, not accusatory. Example: "In X categories, total business grew while your platform share declined. This pattern may reflect buyers shifting to alternative ordering channels, seasonal procurement timing, or competitive displacement — it warrants rep-level follow-up to understand the root cause." For Part B: "These reps manage growing accounts but are capturing less of that growth on the platform — a focused enablement conversation could recapture share."}}
  </div>
</div>
```

**Claim rules**: "Total business in [Category] grew X%, but your platform captured Y fewer percentage points of that growth — an estimated $Z shifted to other channels." ALWAYS hedge: "estimated," "may have shifted," "suggests." Never say definitively "lost to competitors" — could be channel shift, timing, or seasonal patterns. Frame rep-level data as coaching opportunity, not failure. Never use "ERP," "portal_orders," or "portal ordering." Use "total business" and "all-channel."

---

### 10. Price Erosion / Trade-Down Detection (conditional) — MANDATORY WHEN GATE MET

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `cache/Q-60_results.md` has data rows.

**Data source**: `cache/Q-60_results.md` (deduplicated rows — one row per account showing QoQ avg unit price decline ≥ 4%)

**Rendering**: Open with a `.callout.insight` (NOT `.callout.warn`) titled "Product Mix Shift" — frame as an investigative finding, not an alarm.

```html
<div class="subsection">
  <div class="subsection-title">Product Mix & Pricing Trends</div>
  <div class="callout insight">
    <div class="callout-title">Product Mix Shift</div>
    <p>{{COUNT}} accounts show declining average unit prices quarter-over-quarter — combined current-quarter business: ${{COMBINED_GMV}}. This may indicate competitive pressure, shifting buyer mix, or product substitution.</p>
  </div>
  <table>
    <tr>
      <th>Account</th>
      <th>Prior Avg Price</th>
      <th>Current Avg Price</th>
      <th>Change</th>
      <th>Current Quarter GMV</th>
      <th>Orders</th>
    </tr>
    {{ROWS — sorted by current_quarter_gmv desc, top 5 visible, rest in <details>}}
  </table>
```

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| Prior Avg Price | `prior_avg_price` formatted as currency |
| Current Avg Price | `current_avg_price` formatted as currency |
| Change | `price_change_pct` with `.badge.danger` styling (all values are negative — use badge for visual urgency) |
| Current Quarter GMV | `current_quarter_gmv` formatted as currency |
| Orders | `current_orders` |

After the table, add a `.callout.insight` titled "Investigative Context":

```html
  <div class="callout insight">
    <div class="callout-title">Investigative Context</div>
    <p>Declining unit prices may reflect several dynamics: competitive pricing pressure driving buyers to request discounts, a natural shift toward lower-priced product tiers, changing buyer mix within an account, or seasonal promotional activity. These patterns warrant individual account review — they are signals to investigate, not conclusions to act on.</p>
  </div>
  <div class="what-this-means">
    <strong>Action:</strong> {{PRICE_EROSION_NARRATIVE — investigative, measured, multi-causal. Example: "X accounts are trending toward lower unit prices. This could reflect competitive pricing pressure, a shift toward different product tiers, or evolving buyer preferences within these accounts. The pattern is worth a focused conversation — particularly for accounts where current-quarter volume remains strong, suggesting the relationship is active but the product mix is shifting."}}
  </div>
</div>
```

**Tone**: Investigative, not alarmist. The `.badge.danger` on percentage declines provides visual urgency but the prose must remain measured and multi-causal. Never say "price erosion alert" in a way that implies the client is failing — frame as "pattern worth understanding."

**Part B — Category-Level Pricing Trends (render when Q-60 gate met AND category/collection data available from Q-39)**

This provides the diagnostic the user actually needs: are prices going up while units drop? Is volume loss in specific categories masking overall AOV changes?

**Data source**: Derive from `Q-60_results.md` aggregated by category, cross-referenced with `Q-39_results.md` for category-level unit volume.

```html
  <h4>Category-Level AOV Trends</h4>
  <div class="callout insight">
    <div class="callout-title">Price vs. Volume by Category</div>
    <p>{{DIAGNOSTIC_HEADLINE — e.g., "Your average selling price for Pendants increased 8% while units sold dropped 12%. In Chandeliers, both price and volume grew. The category-level view reveals whether AOV changes reflect intentional pricing strategy or demand erosion."}}</p>
  </div>
  <table>
    <tr>
      <th>Category</th>
      <th>Prior Avg Unit Price</th>
      <th>Current Avg Unit Price</th>
      <th>Price Change</th>
      <th>Prior Units</th>
      <th>Current Units</th>
      <th>Unit Change</th>
      <th>Diagnosis</th>
    </tr>
    {{ROWS — categories with meaningful price OR volume shifts, sorted by revenue impact desc}}
  </table>
```

**Diagnosis column** (computed per category):
| Pattern | Diagnosis | Badge |
|---------|-----------|-------|
| Price ↑, Units ↑ | "Healthy growth" | `.badge.ok` |
| Price ↑, Units ↓ | "Price sensitivity — may be losing volume to pricing" | `.badge.warn` |
| Price ↓, Units ↑ | "Volume play — lower prices driving adoption" | `.badge.muted` |
| Price ↓, Units ↓ | "Category contraction — investigate competitive pressure" | `.badge.danger` |
| Price flat, Units ↓ | "Demand erosion — not a price issue" | `.badge.warn` |

Only show categories where EITHER price change > 5% OR unit change > 10% — minor fluctuations are noise.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CATEGORY_PRICING_NARRATIVE — specific to org. Example: "Your Pendants category shows classic price sensitivity: an 8% price increase correlated with a 12% unit drop, netting a 5% revenue decline. Meanwhile, Bath Lighting grew both price (+3%) and volume (+18%) — suggesting strong market fit. The categories showing 'price sensitivity' are where competitor pricing comparisons would be most valuable."}}
  </div>
```

**When category data is insufficient**: If Q-39 doesn't have enough granularity to break pricing trends by category, omit Part B silently — the account-level view (Part A) still renders.

**Claim rules**: Always hedge — "correlated with" not "caused by." Frame price sensitivity as a hypothesis requiring investigation. Never definitively state "you raised prices too high" — say "the price increase correlated with volume loss in this category." Always hedge: "may reflect," "suggests," "warrants investigation."

---

### 11. Market Commitment Attribution (conditional) — MANDATORY WHEN GATE MET

**Gate**: `HAS_COMMITMENT_DATA = true` (read from `gate_flags.md`) — if false, skip this entire subsection silently.

**MANDATORY RENDER**: If `cache/Q-58_results.md` exists AND contains data rows, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-58_results.md`, `cache/Q-58b_results.md`

**Rendering**: Open with a `.callout.insight` block titled "Market Commitment Conversion" with a summary computed from the most recent market row: "At [market_code], your accounts committed to X items. Within 90 days, Y% converted to orders — Z items remain unrealized."

```html
<div class="subsection">
  <div class="subsection-title">Market Commitment Attribution</div>
  <div class="callout insight">
    <div class="callout-title">Market Commitment Conversion</div>
    <p>At {{MOST_RECENT_MARKET}}, your accounts committed to {{TOTAL_COMMITTED}} items. Within 90 days, {{CONVERSION_PCT}}% converted to orders — {{UNREALIZED}} items remain unrealized.</p>
  </div>
  <table>
    <tr>
      <th>Market</th>
      <th>Date</th>
      <th>Customers</th>
      <th>Items Committed</th>
      <th>Items Converted</th>
      <th>Conversion Rate</th>
      <th>Unrealized Items</th>
    </tr>
    {{ROWS — all market rows, typically 2–6}}
  </table>
```

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

After the table, include a `.callout.insight` summary:

```html
  <div class="callout insight">
    <div class="callout-title">Unrealized Pipeline</div>
    <p>Across all markets, {{TOTAL_UNREALIZED}} total items remain committed-but-not-ordered. These represent buying intent that was expressed but not yet fulfilled — ideal targets for rep follow-up.</p>
  </div>
```

**Part B — In-Stock Actionable Items (Q-58b)**

**Gate**: Render ONLY if `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND `cache/Q-58b_results.md` has data rows.

**Data source**: `cache/Q-58b_results.md`

**Rendering**: After the market conversion table, add a `.callout.opportunity` block titled "Immediate Action: Committed Items Currently In Stock". Open with: "These items were committed at market, never ordered, and are sitting in your warehouse right now — the shortest path from intent to revenue."

```html
  <div class="callout opportunity">
    <div class="callout-title">Immediate Action: Committed Items Currently In Stock</div>
    <p>These items were committed at market, never ordered, and are sitting in your warehouse right now — the shortest path from intent to revenue.</p>
  </div>
  <table>
    <tr>
      <th>Item</th>
      <th>Market</th>
      <th>Accounts</th>
      <th>Committed Qty</th>
      <th>In Stock</th>
      <th>Stock Value</th>
    </tr>
    {{ROWS — all in-stock actionable items}}
  </table>
  <p class="prose">Total actionable value: ${{TOTAL_STOCK_VALUE}} across {{ITEM_COUNT}} items.</p>
```

| Column | Content |
|--------|---------|
| Item | `item_description` (fall back to `item_number` if blank) |
| Market | `market_code` formatted as readable name |
| Accounts | `customers_committed` |
| Committed Qty | `total_committed_qty` |
| In Stock | `current_stock` |
| Stock Value | `stock_value` formatted as currency |

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{MARKET_COMMITMENT_NARRATIVE — Frame market conversion as pipeline visibility. Example: "Market commitments represent explicit buying intent captured at the point of enthusiasm. The X% conversion rate means Y items still have unrealized demand — these are warm leads that require re-engagement, not cold outreach." For Part B, emphasize zero-friction: "These items are already in your warehouse with committed buyers — they represent revenue waiting to be invoiced."}}
  </div>
</div>
```

**Claim rules**: Never expose `item_number` as raw internal code — use `item_description` in prose. Frame as the lowest-friction opportunity available. Never use "ERP." Use `.callout.opportunity` (green border) for Part B — NOT `.callout.success`.

---

### 12. First-Time Buyer Acquisition Trend (conditional)

**Gate**: `Q-41_results.md` has monthly new buyer counts spanning 6+ months.

**Data source**: `Q-41_results.md`

New eCat buyers per month with NAMED accounts and their growth trajectories. Aggregate counts alone are vanity metrics — the intelligence value is WHO the new buyers are and what they became.

**⚠ CRITICAL FRAMING**: "2-8 new buyers per month" without naming them is NOT intelligence. Every new buyer acquisition section MUST include named accounts showing their trajectory from first order to current state. If Q-41 includes account-level detail, use it. If it only has aggregates, supplement with data from Q-12 or Q-ORG-VELOCITY to identify specific accounts that first ordered within the reporting window and show their growth arc.

```html
<div class="subsection">
  <div class="subsection-title">New Buyer Acquisition & Growth</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val">{{AVG_MONTHLY_NEW_BUYERS}}</div>
      <div class="metric-label">Avg New Buyers / Month</div>
      <div class="metric-note">Trailing {{N}} months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">{{TREND_DIRECTION}}</div>
      <div class="metric-label">Acquisition Trend</div>
      <div class="metric-note {{ok_or_warn}}>{{FIRST_HALF_VS_SECOND_HALF}}</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${{TOP_NEW_BUYER_GMV}}</div>
      <div class="metric-label">Best New Buyer (LTM)</div>
      <div class="metric-note">{{TOP_NEW_BUYER_NAME}}</div>
    </div>
  </div>
```

**Named Account Trajectories (MANDATORY when data available)**:

Show the top 5 new buyers by current LTM revenue with their growth trajectory from first order:

```html
  <div class="callout insight">
    <div class="callout-title">New Buyer Growth Stories</div>
    <p>Your strongest recent acquisitions aren't just new — they're growing. {{TOP_BUYER_NAME}} started with ${{FIRST_ORDER}} and has grown to ${{CURRENT_LTM}} in {{MONTHS}} months. These trajectories prove your acquisition funnel produces real, growing relationships.</p>
  </div>
  <table>
    <tr><th>Account</th><th>First Order</th><th>First Order Value</th><th>Current LTM Revenue</th><th>Growth</th><th>Orders (LTM)</th></tr>
    {{ROWS — top 5 new buyers by current LTM revenue, showing trajectory}}
  </table>
```

"Growth" column: Show as multiplier if meaningful (e.g., "12x first order") with `.badge.ok`. If account has only 1-2 orders, show "Early" with `.badge.muted`.

If declining (second-half average < first-half average by > 25%):

```html
  <div class="callout alert">
    <div class="callout-title">Acquisition Rate Declining</div>
    <p>New buyer acquisition dropped from {{FIRST_HALF_AVG}} per month ({{FIRST_HALF_PERIOD}}) to {{SECOND_HALF_AVG}} per month ({{SECOND_HALF_PERIOD}}). At this rate, natural attrition may outpace new buyer onboarding.</p>
  </div>
```

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{ACQUISITION_NARRATIVE — MUST reference specific named accounts. Example: "Your acquisition funnel is producing winners: Graham's Lighting went from $53K first quarter to $100K LTM, and Royaume grew to $72K from a standing start. But the acquisition rate is declining — you're getting fewer shots on goal each month. The question isn't whether your new buyers grow (they do), it's whether you're finding enough of them."}}
  </div>
</div>
```

**Claim rules**: Frame declining acquisition as pipeline risk, not operational failure. Hedge attrition projections. ALWAYS name specific accounts — aggregate counts without names are filler, not intelligence. If account-level trajectory data is unavailable, state it explicitly: "Account-level trajectory data would show which new buyers are growing fastest — request customer-level first-order dates for the next cycle."

---

## Section-Level What-This-Means (MANDATORY)

After all subsections, one `.what-this-means` for the entire section. Max 3 sentences:

1. The most important commerce pattern insight (capture rate trajectory, channel shift, displacement signal, or AOV opportunity)
2. The dollar implication of the pattern continuing
3. (Optional) What additional data would enable (e.g., order_origin for precise channel attribution)

---

## Data Confidence Header (MANDATORY — ALWAYS AT TOP)

**⚠ ENFORCEMENT: If this header is missing from the rendered section, the fragment is DEFECTIVE. Do NOT skip it under any circumstances.**

> Follow `section_shared_contract.md` §2 for the confidence header process.

**Template selection** for `SECTION_CONFIDENCE_4`:

| Tier value | Template | Label |
|---|---|---|
| `FULL` | `§4-FULL` | `FULL PICTURE` |
| `STRONG` | `§4-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§4-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§4-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

**Variable resolution**: `{{LAST_PORTAL_ORDER_DATE}}` from enrichment preflight in `gate_flags.md`. If it can't be resolved for FULL or STRONG, fall back to `§4-PARTIAL`.

---

## Highlight File Output

> Follow `section_shared_contract.md` §4 for the highlight file format.

Save `cache/section_04_highlights.md` with 2–4 candidates from the strongest commerce signals. Deep-link: `[→ §commerce]`.

---

## Section-Specific Rules

**If `HAS_PORTAL_ORDERS = false`**: Commerce Patterns shows eCat-only data. Do not mention total business or all-channel anywhere in this section. Subsections 1 (Part B of Capture Rate), 9 (Competitive Displacement), and 10 (Price Erosion) are all skipped. Channel Migration (subsection 3) renders eCat channel split only without share-of-total overlay.

**Channel attribution statement** (required in section body when `HAS_CART = true`): "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." Do not use code literals like `order_source = 'ipad'` in client-facing prose.

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Rep-level performance, coaching, or behavioral analysis → belongs in §5 Team Intelligence
2. Customer activation, dormancy, or buyer-level analysis → belongs in §2 Account Intelligence
3. Product catalog health, inventory status, or sales-line analysis → belongs in §3 Product Intelligence
4. Portal traffic or geographic demand → belongs in Demand Signal Intelligence
5. ~~Peer benchmarking or cohort comparisons~~ → **EXCLUDED from all reports** (data unreliable)
6. Platform feature utilization or data freshness → belongs in Platform & Feature
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md)

Read: `GUARDRAILS.md` for the full query ownership table and rule set.

---

## Conditional Subsection Checklist

| # | Subsection | Gate Condition | Action When Met | Action When Not Met |
|---|-----------|----------------|-----------------|---------------------|
| 1 | Digital Ordering Share | `HAS_PORTAL_ORDERS = true` | Render ordering share metrics + classification badge | Skip silently |
| 1+ | Ordering Share (VM45) | `VM45_RENDER = true` | Include ordering share calculation | Render total business context only (no share) |
| 2A | eCat Order Trend | Always | Render eCat-only trend table | — |
| 2B | eCat Share of Total Trend | `HAS_PORTAL_ORDERS = true` | Add total business + share columns to trend | Skip Part B silently |
| 3 | Channel Migration / Breakdown | `HAS_CART = true` OR 2+ channels with 6+ months | Render channel split table | Skip silently |
| 4 | Top Buyers (base) | Always | Render Q-13 top-10 table | — |
| 4+ | Top Buyers enrichment | `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-52` has rows | Add "Total Business" + "eCat Share" columns | Render Q-13-only table |
| 5 | Quote Economics | 10+ quotes + confirmed orders exist | Render quote vs confirmed AOV spread | Skip silently |
| 6 | Order Type & Workflow | Always | Render quote premium callout + collapsed type table | — |
| 7 | Seasonal Timing | 12+ months of monthly data | Render seasonality table with intensity badges. `[COLLAPSE]` | Skip silently |
| 8 | AOV Spread by Rep | Spread > 2x between highest and lowest rep AOV | Render AOV spread callout + rep table | Skip silently (spread ≤ 2x is normal) |
| 9A | Category Displacement | `HAS_PORTAL_ORDERS = true` + `Q-55` has displacement rows | Render `.callout.insight` + displacement table. **MANDATORY.** | Skip silently |
| 9B | Rep Capture Trend | `PORTAL_REP_DATA_PRESENT = true` + `Q-56` has declining reps | Render rep decline table | Skip Part B silently |
| 10 | Price Erosion | `HAS_PORTAL_ORDERS = true` + `Q-60` has rows | Render `.callout.insight` + accounts table + `.callout.insight`. **MANDATORY.** | Skip silently |
| 11 | Market Commitment | `HAS_COMMITMENT_DATA = true` + `Q-58` has rows | Render market conversion table. **MANDATORY.** | Skip silently |
| 11B | In-Stock Actionable | `HAS_COMMITMENT_DATA = true` + `HAS_INVENTORY = true` + `Q-58b` has rows | Render `.callout.opportunity` + in-stock table | Skip Part B silently |
| 12 | First-Time Buyer Acquisition | 6+ months of monthly new buyer data | Render acquisition trend. Decline flagged if > 25% drop. `[COLLAPSE]` | Skip silently |

## TARGET STRUCTURE — Gold Standard (MATCH THIS MARKUP EXACTLY)

This is the corresponding section from the canonical reference report. It is the source of truth for HTML structure: tag nesting, class names, column headers, subsection order, which subsections carry a `what-this-means` block, and the `<thead>`/`<tbody>`/`row-highlight` patterns. The data values below are illustrative — replace them with this client's data — but reproduce the STRUCTURE exactly. Where this target and the prose guide disagree on markup, THIS WINS.

```html
<details class="section-collapse" id="commerce">
  <summary>
    <div class="section-title">Commerce Patterns</div>
    <div class="section-sub">$8.6M eCat sales LTM &middot; 23.1% digital ordering share &middot; channel and seasonal analysis</div>
    <div class="section-contents">Digital share trajectory, channel split, quote conversion, seasonal timing, AOV analysis</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section">

    <div class="data-confidence">
      <span class="data-confidence-label">Full Picture</span>
      Commerce analysis draws from eCat order data (iPad + Online), all-channel invoices, quote/cart activity from app behavioral data, and inventory availability feeds.
    </div><div class="subsection">
      <div class="subsection-title">Digital Ordering Share Trajectory</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">Current Share (LTM)</div>
          <div class="metric-value">23.1%</div>
          <div class="metric-note ok">+2.4 pts this quarter</div>
        </div>
        <div class="metric">
          <div class="metric-label">Prior Year Share</div>
          <div class="metric-value">19.2%</div>
          <div class="metric-note">+3.9 pts YoY gain</div>
        </div>
        <div class="metric">
          <div class="metric-label">eCat Sales LTM</div>
          <div class="metric-value">$8.6M</div>
          <div class="metric-note ok">+17.4% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">All-Channel LTM</div>
          <div class="metric-value">$37.2M</div>
          <div class="metric-note ok">+9.1% YoY</div>
        </div>
      </div>
      <table>
        <thead>
          <tr><th>Quarter</th><th>eCat Sales</th><th>All-Channel</th><th>Digital Share</th><th>QoQ Change</th></tr>
        </thead>
        <tbody>
          <tr><td>Q3 2025 (Jul&ndash;Sep)</td><td>$1,920,000</td><td>$8,840,000</td><td>21.7%</td><td>+1.1 pts</td></tr>
          <tr><td>Q4 2025 (Oct&ndash;Dec)</td><td>$2,280,000</td><td>$9,620,000</td><td>23.7%</td><td>+2.0 pts</td></tr>
          <tr><td>Q1 2026 (Jan&ndash;Mar)</td><td>$2,040,000</td><td>$9,180,000</td><td>22.2%</td><td>&minus;1.5 pts</td></tr>
          <tr class="row-highlight"><td>Q2 2026 (Apr&ndash;May, partial)</td><td>$1,560,000</td><td>$6,340,000</td><td>24.6%</td><td class="metric-note ok">+2.4 pts</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Digital ordering share dipped in Q1 2026 (seasonal pattern &mdash; reps prioritize in-person at spring markets) but rebounded strongly in Q2 to a new high of 24.6%. At this trajectory, you&rsquo;ll cross 25% by end of Q3. Each additional percentage point represents $372K in orders shifting to trackable, reportable digital channels.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Channel Split: iPad vs eCat Online</div>
      <div class="callout insight">
        <div class="callout-title">Channel Behavior Differences</div>
        <p>iPad and Online serve different roles in your selling process. iPad drives larger project orders through presentations; Online handles quick reorders and after-hours purchasing.</p>
        <ul>
          <li><strong>iPad:</strong> 58% of eCat revenue ($4.99M LTM), AOV of $1,842, typically placed during or after client meetings</li>
          <li><strong>Online:</strong> 42% of eCat revenue ($3.61M LTM), AOV of $694, 38% placed outside business hours (evenings/weekends)</li>
          <li><strong>Overlap:</strong> 62% of buyers who use both channels have higher LTM revenue than single-channel buyers ($4,200 vs $2,100 avg per account)</li>
        </ul>
      </div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">iPad Revenue</div>
          <div class="metric-value">$4.99M</div>
          <div class="metric-note ok">+14.2% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Online Revenue</div>
          <div class="metric-value">$3.61M</div>
          <div class="metric-note ok">+22.1% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">iPad AOV</div>
          <div class="metric-value">$1,842</div>
          <div class="metric-note">2.7x Online</div>
        </div>
        <div class="metric">
          <div class="metric-label">Online AOV</div>
          <div class="metric-value">$694</div>
          <div class="metric-note ok">+8.3% YoY</div>
        </div>
      </div>
      <div class="what-this-means">
        <strong>Action:</strong> Online is growing faster (+22.1% vs +14.2%) and capturing after-hours orders your reps can&rsquo;t. Encourage accounts like Lakeside Living (6 locations, frequent small reorders) to use Online for replenishment while keeping iPad for project presentations. Dual-channel accounts spend 2x more than single-channel.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Quote-to-Order Conversion</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">Quotes Created (LTM)</div>
          <div class="metric-value">2,847</div>
          <div class="metric-note">Avg $2,140 per quote</div>
        </div>
        <div class="metric">
          <div class="metric-label">Converted to Orders</div>
          <div class="metric-value">1,624</div>
          <div class="metric-note">57.0% conversion</div>
        </div>
        <div class="metric">
          <div class="metric-label">Abandoned Value</div>
          <div class="metric-value">$2.62M</div>
          <div class="metric-note warn">1,223 unconverted quotes</div>
        </div>
        <div class="metric">
          <div class="metric-label">Avg Days to Convert</div>
          <div class="metric-value">8.4 days</div>
          <div class="metric-note">Median: 4 days</div>
        </div>
      </div>
      <table>
        <thead>
          <tr><th>Conversion Window</th><th>Orders</th><th>Share</th><th>Avg Value</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td>Same day</td><td>486</td><td>29.9%</td><td>$1,420</td></tr>
          <tr><td>1&ndash;3 days</td><td>524</td><td>32.3%</td><td>$1,890</td></tr>
          <tr><td>4&ndash;7 days</td><td>318</td><td>19.6%</td><td>$2,640</td></tr>
          <tr><td>8&ndash;14 days</td><td>198</td><td>12.2%</td><td>$3,180</td></tr>
          <tr><td>15&ndash;30 days</td><td>98</td><td>6.0%</td><td>$3,860</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Quotes that convert after 7+ days are your largest deals ($3,180&ndash;$3,860 avg), suggesting project-based buyers need approval cycles. Set up automated quote-reminder notifications at day 7 and day 14 for quotes over $2,000 &mdash; even converting 10% of abandoned high-value quotes would recover an estimated $180K annually.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Seasonal Timing Intelligence</div>
      <table>
        <thead>
          <tr><th>Period</th><th>eCat Sales</th><th>Index vs Avg</th><th>Key Driver</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td><strong>Oct&ndash;Nov (Post-High Point)</strong></td><td>$1,680,000</td><td>142</td><td>Market follow-up orders + Q4 project specs</td></tr>
          <tr class="row-highlight"><td><strong>Apr&ndash;May (Post-Spring Market)</strong></td><td>$1,560,000</td><td>132</td><td>New collection launches + renovation season</td></tr>
          <tr><td>Jan&ndash;Feb</td><td>$1,140,000</td><td>96</td><td>Year-start budgets, slower pace</td></tr>
          <tr><td>Jun&ndash;Jul</td><td>$980,000</td><td>83</td><td>Summer slowdown, design vacations</td></tr>
          <tr class="row-warn"><td><strong>Aug&ndash;Sep (Pre-Market)</strong></td><td>$860,000</td><td>73</td><td>Buyers hold orders awaiting new products at Market</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> The August&ndash;September pre-Market dip costs you roughly $520K vs. average months. Consider a &ldquo;Pre-Market Preview&rdquo; program: give top 20 accounts early access to 3&ndash;5 new items in August, capturing orders before the buying freeze. Coastal Design Partners and Pacific Rim Hospitality both responded within 48 hours to your last early-access offer.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Average Order Value Trends</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">Overall AOV (LTM)</div>
          <div class="metric-value">$1,186</div>
          <div class="metric-note ok">+6.8% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">iPad AOV</div>
          <div class="metric-value">$1,842</div>
          <div class="metric-note ok">+9.2% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Online AOV</div>
          <div class="metric-value">$694</div>
          <div class="metric-note ok">+8.3% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Hospitality AOV</div>
          <div class="metric-value">$2,640</div>
          <div class="metric-note">2.2x overall avg</div>
        </div>
      </div>
      <div class="what-this-means">
        <strong>Action:</strong> Hospitality accounts order at 2.2x your average AOV ($2,640 vs $1,186). With Heritage Hospitality and Pinnacle Hotel Group both at risk from the Aurora Sconce stockout, protecting hospitality AOV is the single highest-leverage inventory decision on the table right now.
      </div>
    </div>

    <div class="callout note" style="margin-top:16px;">
      <div class="callout-title">With Connected Data</div>
      Connecting your shipping/fulfillment data would let us measure fill rate by SKU and territory, showing where backorders cause the most downstream revenue loss and whether expedited shipping correlates with higher reorder rates.
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

## E. Semantic Rules (Locked)

1. `portal_orders` = "total business across all channels" / "orders synced from
   your ERP". **Never** "portal ordering" or "buyer self-service."
2. If `has_clicky = false`, the Portal/Demand section **does not exist**. Do not
   reference it in any other section.
3. Health score is **INTERNAL only** — never appears in external report output.
4. Segment labels (`Platform-Embedded`, `Commerce-Active`, `Catalog-Focused`)
   **NEVER** appear in external output.
5. **Peer benchmarking is EXCLUDED entirely.** Do not reference peer comparisons,
   quartile positioning, peer medians, or cohort benchmarks in any section.
   The peer data is unreliable. If a signal or subsection references peer
   comparison, skip that comparison silently.
6. Benchmark metadata (`benchmark_confidence`, `peer_group_level`,
   `peer_group_n`) are **banned from all output** — neither internal nor external.

---


## Cache Data

### signal_rank.md

# Signal Rank — Arabela Lighting (arl, org_id=269)
- **Run date**: 2026-06-17
- **Total signals fired**: 17 (P0: 2, P1: 13, P2: 2)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 50% of eCat GMV | P1 | §4 Commerce | 1.3 | $119,437 | 2.0 | 298,945 | RISK |
| 2 | SIG-DECAY-01 | Reorder Decay — Beautiful Things Lighting & Accessories 3.0x normal gap (55d vs 18d avg) | P0 | §2 Accounts | 3.0 | $18,963 | 3.0 | 170,667 | RISK |
| 3 | SIG-DECAY-01 | Reorder Decay — WAYFAIR 4.6x normal gap (79d vs 17d avg) | P0 | §2 Accounts | 4.6 | $11,650 | 3.0 | 160,770 | RISK |
| 4 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 5 | SIG-RISK-03 | Data Staleness — customer_favorites last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 6 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 7 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 8 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 9 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 10 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 11 | SIG-RISK-03 | Data Staleness — placement_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — inventories last updated 188d ago | P1 | §6 Platform | 2.1 | $1 | 2.0 | 4 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — portal_orders last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — portal_invoices last updated 96d ago | P2 | §6 Platform | 1.1 | $1 | 2.0 | 2 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 2 | 0 | 0 | 2 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 12 | 2 | 14 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 50% of eCat GMV
2. **[RISK]** SIG-DECAY-01: Reorder Decay — Beautiful Things Lighting & Accessories 3.0x normal gap (55d vs 18d avg)
3. **[RISK]** SIG-DECAY-01: Reorder Decay — WAYFAIR 4.6x normal gap (79d vs 17d avg)
4. **[RISK]** SIG-RISK-03: Data Staleness — contract_prices last updated 313d ago
5. **[RISK]** SIG-RISK-03: Data Staleness — customer_favorites last updated 313d ago
6. **[RISK]** SIG-RISK-03: Data Staleness — kit_items last updated 313d ago
7. **[RISK]** SIG-RISK-03: Data Staleness — matrix_options last updated 313d ago

**Balance check**: 0 positive (slots 1-0), 7 risk (slots 1-7). Finding #1 is RISK. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### Q-13_results.md

# Q-13 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-13 — Customer Concentration Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | orders | gmv | pct_of_ecat_gmv |
| --- | --- | --- | --- | --- |
| LIGH77087 | Lighting Inc | 23 | $33,541 | $8 |
| LUX30096 | Lux Lighting | 1 | $25,691 | $6 |
| LIG34134 | Lighting First | 15 | $24,244 | $6 |
| BEAT33065 | Beautiful Things Lighting & Accessories | 8 | $18,963 | $5 |
| Lux | Lux Lighting | 1 | $16,998 | $4 |
| Georgia | Georgia Lighting | 13 | $16,607 | $4 |
| ILLU78504 | Illuminations | 7 | $14,536 | $4 |
| FALW33436 | Fan & Lighting World | 13 | $13,597 | $3 |
| PYKY11108 | PYRAMID CREATIVE SUPPLIES | 1 | $13,540 | $3 |
| Mews | MEWS | 1 | $11,978 | $3 |
| WAYF02116 | WAYFAIR | 12 | $11,650 | $3 |
| LYTE34208 | Lyteworks | 8 | $11,373 | $3 |
| TRI76504 | TRI-SUPPLY | 2 | $9,108 | $2 |
| HORB95821 | Hobrecht Lighting Co. Inc | 6 | $8,386 | $2 |
| UEM6M1Y3 | Union Electric Lighting Co | 2 | $8,380 | $2 |

### Q-16_results.md

(not present — file does not exist or is empty)

### Q-18_partA_results.md

# Q-18-A Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-18-A — eCat Order Velocity — Part A
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| month | total_ecat_orders | ipad_orders | ecat_online_orders | ecat_gmv | ecat_aov |
| --- | --- | --- | --- | --- | --- |
| 2026-6-1 | 26 | 26 | 0 | $33,903 | $1,304 |
| 2026-5-1 | 34 | 34 | 0 | $40,397 | $1,188 |
| 2026-4-1 | 45 | 45 | 0 | $72,976 | $1,622 |
| 2026-3-1 | 34 | 34 | 0 | $53,717 | $1,580 |
| 2026-2-1 | 39 | 39 | 0 | $82,471 | $2,115 |
| 2026-1-1 | 41 | 41 | 0 | $175,680 | $4,285 |
| 2025-12-1 | 22 | 22 | 0 | $41,118 | $1,869 |
| 2025-11-1 | 22 | 22 | 0 | $25,356 | $1,153 |
| 2025-10-1 | 16 | 16 | 0 | $19,120 | $1,195 |
| 2025-9-1 | 10 | 10 | 0 | $15,298 | $1,530 |
| 2025-8-1 | 14 | 14 | 0 | $59,208 | $4,229 |
| 2025-7-1 | 5 | 5 | 0 | $6,599 | $1,320 |
| 2025-6-1 | 5 | 5 | 0 | $36,532 | $7,306 |

### Q-18_partB_results.md

(not present — file does not exist or is empty)

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-19_results.md

(not present — file does not exist or is empty)

### Q-20_results.md

# Q-20 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-20 — eCat AOV Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 4
- **Run date**: 2026-06-17


| dimension | order_count | avg_order_value | total_ecat_gmv |
| --- | --- | --- | --- |
| All eCat Orders | 313 | $2,116 | $662,375 |
| iPad Orders | 313 | $2,116 | $662,375 |
| eCat Online Orders | 0 | — | — |
| Quote Orders | 0 | — | — |

### Q-21_results.md

# Q-21 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-21 — eCat Order Type & Workflow Analysis
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 3
- **Run date**: 2026-06-17


| order_type | orders | pct | gmv | avg_value |
| --- | --- | --- | --- | --- |
| Confirmed | 301 | 96.20 | $566,095 | 1,880.71 |
| HFC | 7 | 2.20 | $74,223 | 10,603.29 |
| Canceled | 5 | 1.60 | $22,057 | 4,411.40 |

### Q-41_results.md

# Q-41 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-06-01 | Rep-Acquired (iPad) | 3 |
| 2025-07-01 | Rep-Acquired (iPad) | 2 |
| 2025-08-01 | Rep-Acquired (iPad) | 3 |
| 2025-09-01 | Rep-Acquired (iPad) | 7 |
| 2025-10-01 | Rep-Acquired (iPad) | 7 |
| 2025-11-01 | Rep-Acquired (iPad) | 4 |
| 2025-12-01 | Rep-Acquired (iPad) | 2 |
| 2026-01-01 | Rep-Acquired (iPad) | 7 |
| 2026-02-01 | Rep-Acquired (iPad) | 7 |
| 2026-03-01 | Rep-Acquired (iPad) | 8 |
| 2026-04-01 | Rep-Acquired (iPad) | 14 |
| 2026-05-01 | Rep-Acquired (iPad) | 7 |
| 2026-06-01 | Rep-Acquired (iPad) | 4 |

### Q-45_results.md

(not present — file does not exist or is empty)

### Q-52_results.md

(not present — file does not exist or is empty)

### Q-55_results.md

(not present — file does not exist or is empty)

### Q-56_results.md

(not present — file does not exist or is empty)

### Q-58_results.md

(not present — file does not exist or is empty)

### Q-58b_results.md

(not present — file does not exist or is empty)

### Q-60_results.md

(not present — file does not exist or is empty)

### Q-69_results.md

# Q-69 Results — Arabela Lighting (arl, org_id=269)
- **Query**: Q-69 — Order Timing Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-VELOCITY_results.md

(not present — file does not exist or is empty)
