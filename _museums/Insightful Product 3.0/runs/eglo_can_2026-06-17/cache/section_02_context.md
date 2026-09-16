# Section 2 Context Bundle — EGLO Canada (eglo_can)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — EGLO Canada (eglo_can, org_id=232)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=1691 |
| HAS_SALES_DATA | True | sales_data_count=6618 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
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
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 17 | engagement_reps=17 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 26 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 43, Mixpanel total submit_order (Q-01): 130 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=73.1%, ambiguous_rate=73.7%, showroom_event_share=38.1% |
| USER_GROUP_JOIN_RATE | 73% | 19 of 26 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 38% | showroom+admin share of matched events: 38.1% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Karen Hoffman |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=495 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: EGLO Canada
- **Shortname**: eglo_can
- **Org ID**: 232
- **Bundle**: 4
- **Bundle label for report**: 4

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — EGLO Canada (eglo_can, org_id=232)
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
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | PARTIAL | See Derived Gate 6 §5 formula |

## Section Guide — section_02_accounts.md

# Section Guide: Account Intelligence
> **v3.0** — signal-first architecture. The core value section.

## Section Identity

- **id**: `accounts`
- **title**: Account Intelligence
- **section number**: 2
- **include when**: `signal_rank.md` shows ≥ 1 P0/P1 signal with `Section Home = Account Intelligence` OR its alternate include gates pass (activation funnel data exists with sufficient account count)
- **skip when**: 0 P0/P1 account-level signals fired AND alternate gates fail (fall back to Mode 2/3)

## Query Inputs

Read these cache files:

- `cache/signal_rank.md` — ranked signal manifest
- `cache/top_accounts.md` — top 10 accounts by signal density (produced by signal detection pass)
- `cache/Q-12_results.md` — Customer activation & network health
- `cache/Q-14_results.md` — Reorder velocity & early warning
- `cache/Q-14b_results.md` — Account velocity deceleration detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND data rows exist, subsection 8b MUST render)
- `cache/Q-17_results.md` — Dormant high-value accounts
- `cache/Q-40_results.md` — Geographic distribution
- `cache/Q-41_results.md` — New eCat buyer acquisition
- `cache/Q-52_results.md` — eCat penetration of total business by customer (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND data rows exist, subsection 3b MUST render)
- `cache/Q-53_results.md` — Unactivated high-value accounts
- `cache/Q-54_results.md` — Geographic total-business enrichment
- `cache/Q-57_results.md` — Cross-sell whitespace by category (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND data rows exist, subsection 9 MUST render)
- `cache/Q-66_results.md` — Buyer-within-account intelligence (conditional: render subsection 10 if `HAS_PORTAL_ORDERS = true` AND `HAS_BUYER_DATA = true` AND data rows exist)
- `cache/Q-67_results.md` — Geographic revenue displacement (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND data rows exist, subsection 11 MUST render)
- `cache/Q-68_results.md` — Spending Contraction Detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` AND data rows exist, subsection 12 MUST render)
- `cache/Q-ORG-DECAY_results.md` — Customer & item-level reorder decay
- `cache/Q-ORG-CONTRACTION_results.md` — Spending contraction & competitive displacement
- `cache/Q-ORG-VELOCITY_results.md` — Account acceleration detection
- `cache/Q-ORG-NBP_results.md` — Companion product opportunities (customers who buy X also buy Y)
- `cache/Q-ORG-STOCKOUT_results.md` — Stock-out cross-referenced with customer impact
- `cache/gate_flags.md` — data availability gates
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_2` tier

## PRE-BUILD GATE CHECK — Complete Before Writing Any HTML

> Follow `section_shared_contract.md` §1 for the gate check process.

| Cache File | Gate Condition | If gate met + data rows exist → | Subsection |
|---|---|---|---|
| `Q-52_results.md` | `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 3b (eCat Penetration) |
| `Q-14b_results.md` | `HAS_PORTAL_ORDERS = true` | **MUST render** | 8b (Deceleration Alert) |
| `Q-57_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 9 (Cross-Sell Whitespace) |
| `Q-67_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 11 (Geographic Trends) |
| `Q-68_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_CUSTOMER_DATA_PRESENT = true` | **MUST render** | 12 (Spending Contraction) |

## CRITICAL REQUIREMENTS

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **MANDATORY SUBSECTIONS**: Every row in the Pre-Build Gate Check table above where the gate is met AND the cache file has data rows MUST produce a rendered subsection. If you skip one, the fragment is defective.
2. **CONFIDENCE HEADER**: Every §2 fragment MUST contain a confidence header **at the top of the section** (immediately after the header metrics, before any subsection content). This is NOT optional — if the confidence header is missing, the fragment is defective. Read `SECTION_CONFIDENCE_2` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags.
3. **SIGNAL-FIRST ARCHITECTURE**: The mini-briefs (subsection 3) remain the core of this section. New subsections ADD depth after mini-briefs — they do not replace them.

---

## Fragment Structure

Uses the standard `<details class="section-collapse">` wrapper per shared_rules.md Section E.

```
Section ID: accounts
Section Number: §2
```

---

## Content Blocks (render in NARRATIVE ARC order below)

**Rendering order within this section (intelligence → opportunity → risk):**
1. Header Metrics (mandatory)
2. Data Confidence Header (MANDATORY — renders at TOP of section, immediately after metrics)
3. Top 10 Mini-Briefs (mandatory — internal arc: trajectory → NBP → decay → displacement)
3b. eCat Penetration (INTELLIGENCE)
11. Geographic Revenue Trends (INTELLIGENCE)
10. Buyer-Within-Account Intelligence (INTELLIGENCE)
9. Untapped Category Opportunities (OPPORTUNITY)
5. Unactivated High-Value Accounts (OPPORTUNITY)
6. Geographic Distribution (neutral)
8. Reorder Velocity & Early Warning (early warning)
4. Dormant High-Value Accounts (RISK)
7. Velocity Deceleration (RISK)
12. Spending Contraction (RISK — render last, collapsed)

### 1. Header Metrics (MANDATORY)

Four `.metric-card` items in a `.metrics-grid`:

| Metric | Source | Notes |
|--------|--------|-------|
| Total Accounts | Q-12 | All account records in system |
| Active Accounts (12mo) | Q-12 | Accounts with ≥ 1 order in trailing 12 months |
| Active Accounts (90d) | Q-12 | Accounts with ≥ 1 order in last 90 days |
| Avg LTM Revenue per Active Account | Computed | Total LTM GMV ÷ active (12mo) count |

Every metric-card includes a `.metric-note` with time qualifier.

### 2. Data Confidence Header (MANDATORY — ALWAYS AT TOP)

> Follow `section_shared_contract.md` §2 for the confidence header process.

Read `SECTION_CONFIDENCE_2` from `cache/section_confidence.md`.

| Tier | Template | Label |
|---|---|---|
| `FULL` | `§2-FULL` | `FULL PICTURE` |
| `STRONG` | `§2-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§2-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§2-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

Resolve template variables: `{{ACCOUNT_COUNT}}` from `gate_flags.md`, `{{LAST_PORTAL_ORDER_DATE}}` from enrichment preflight in `gate_flags.md`. If `{{ACCOUNT_COUNT}}` cannot be resolved, omit the parenthetical. If `{{LAST_PORTAL_ORDER_DATE}}` cannot be resolved for FULL or STRONG, fall back to `§2-PARTIAL`.

### 3. Top 10 Accounts by Signal Density (MANDATORY)

This is the core of the section. Source: `cache/top_accounts.md`.

**Top 5 accounts**: Fully rendered mini-briefs (see Mini-Brief Spec below).

**Accounts 6–10**: Rendered inside a collapsed `<details>` block:

```html
<details>
  <summary>Accounts 6–10 by signal density &#9662;</summary>
  {{MINI_BRIEFS_6_THROUGH_10}}
</details>
```

---

## Mini-Brief Spec (per account)

Each mini-brief renders as a `.subsection` with the account name as `.subsection-title`. Include ONLY the components where the relevant signal fired for this account. Skip components silently when their signal did not fire.

**RENDER ORDER within each mini-brief follows the narrative arc:**
1. Account Header (mandatory) — establishes the relationship
2. Spending Trajectory — if accelerating, this is the LEAD story (positive)
2b. Wallet Share & Category Whitespace — intelligence/opportunity (shows the full relationship)
3. Companion products — opportunity framing
4. Reorder Decay — risk (only after positive context)
5. Stock-Out Impact — operational risk
6. Competitive Displacement — strategic risk
7. Pre-Meeting Priority (mandatory) — action close

### A. Account Header (MANDATORY for every mini-brief)

```html
<div class="metrics-grid">
  <div class="metric-card">
    <div class="metric-val">{{CUSTOMER_NAME}}</div>
    <div class="metric-label">{{CITY}}, {{STATE}}</div>
  </div>
  <div class="metric-card">
    <div class="metric-val">{{LAST_ORDER_DATE}}</div>
    <div class="metric-label">Last Order</div>
    <div class="metric-note {{warn_if_stale}}">{{DAYS_SINCE}} days ago</div>
  </div>
  <div class="metric-card">
    <div class="metric-val">${{LTM_REVENUE}}</div>
    <div class="metric-label">LTM Revenue</div>
    <div class="metric-note {{ok_or_warn}}">{{YOY_CHANGE}}% YoY</div>
  </div>
  <div class="metric-card">
    <div class="metric-val"><span class="badge {{SCORE_BADGE_CLASS}}">{{ENGAGEMENT_SCORE}}</span></div>
    <div class="metric-label">Engagement Score</div>
    <div class="metric-note">{{SCORE_LABEL}}</div>
  </div>
</div>
```

Use `.metric-note.warn` if last order > 60 days. Use `.metric-note.danger` if > 120 days. YoY change: `.ok` if positive, `.warn` if -1% to -15%, `.danger` if < -15%.

**Engagement Score Computation** (per account):

A composite 0–100 score blending four dimensions. Compute for every mini-brief account:

| Dimension | Weight | Scoring (0–25 each) |
|-----------|--------|---------------------|
| **Recency** | 25% | 25 if last order ≤ 14 days. Linear decay: 25 × (1 - days_since/365). Floor at 0 if > 365 days. |
| **Frequency** | 25% | 25 if order count ≥ org's 90th percentile. Scale linearly from 0 (1 order) to 25 (90th pctile). |
| **Monetary** | 25% | 25 if LTM revenue ≥ org's 90th percentile. Scale linearly from 0 ($0) to 25 (90th pctile). |
| **Trajectory** | 25% | 25 if YoY growth > 50%. 20 if 20–50%. 15 if 0–20%. 10 if -10% to 0%. 5 if -25% to -10%. 0 if < -25%. |

`ENGAGEMENT_SCORE = Recency + Frequency + Monetary + Trajectory` (integer 0–100)

| Score Range | Badge Class | Label |
|-------------|-------------|-------|
| 80–100 | `.badge.ok` | Champion |
| 60–79 | `.badge.ok` | Strong |
| 40–59 | `.badge.muted` | Moderate |
| 20–39 | `.badge.warn` | Cooling |
| 0–19 | `.badge.danger` | At Risk |

**Purpose**: Gives the reader a single sortable number to prioritize accounts. A "Champion" with a decay signal is more urgent than an "At Risk" account that was always low-value. The score contextualizes the signals that follow.

**IMPORTANT**: "Engagement Score" is permitted — it is a composite behavioral metric, not a health score. Never call this a "health score" in client-facing text (banned per shared_rules.md).

### B. Spending Trajectory (conditional: Q-ORG-VELOCITY or Q-ORG-CONTRACTION data exists for this account)

QoQ revenue trend with inflection callout. **This renders FIRST after the header because acceleration is the strongest positive signal.**

```html
<div class="callout insight">
  <div class="callout-title">Spending Trajectory</div>
  <p>Quarterly trend: ${{Q-3}} → ${{Q-2}} → ${{Q-1}} → ${{Q-CURRENT}}</p>
  <p>{{INFLECTION_NARRATIVE}}</p>
</div>
```

`INFLECTION_NARRATIVE`: If accelerating (SIG-MOM-01), frame positively: "Accelerating at X% QoQ for N consecutive quarters — annualized run rate: $Y." If contracting (SIG-DECAY-04), frame constructively: "Total business contracted X% YoY ($PRIOR → $LTM) — a $GAP recovery opportunity if engagement momentum returns."

### B2. Wallet Share & Category Whitespace (conditional: `HAS_PORTAL_ORDERS = true` AND Q-52/Q-57 data exists for this account)

**Gate**: Only renders when portal_orders data is available for this specific account AND either (a) Q-52 shows total business context, or (b) Q-57 shows category gaps for this account.

This component answers: "How much of this account's total spend do we capture, and what categories are they NOT buying from us that similar accounts buy?"

```html
<div class="callout insight">
  <div class="callout-title">Wallet Position</div>
  <p><strong>Total relationship:</strong> ${{TOTAL_BUSINESS_GMV}} across all channels | <strong>eCat share:</strong> ${{ECAT_GMV}} ({{PENETRATION_PCT}}%)</p>
  {{IF category_gaps_exist:}}
  <p><strong>Category whitespace:</strong> This account buys in {{ACTIVE_CATEGORIES}} categories but has $0 in {{MISSING_CATEGORY_1}}{{IF more: ", {{MISSING_CATEGORY_2}}"}}, where similar accounts average ${{PEER_MEDIAN}} annually.</p>
  {{/IF}}
</div>
```

**Construction rules:**
- `TOTAL_BUSINESS_GMV`: From Q-52 data for this account (all-channel GMV)
- `ECAT_GMV`: eCat-originated GMV for this account
- `PENETRATION_PCT`: `ECAT_GMV / TOTAL_BUSINESS_GMV × 100`
- `MISSING_CATEGORY_1/2`: From Q-57 data filtered for this account — categories where this account has zero purchases but peer accounts (similar revenue, same region) actively buy. Show top 2 by peer median spend.
- `PEER_MEDIAN`: The median annual spend in that category across similar accounts

**Framing**: This is about the SIZE of the relationship and the SHAPE of what they buy vs. what they could buy. It turns a one-dimensional revenue number into a multi-dimensional opportunity map. "You know this account does $2.7M with you — but they buy nothing in Mirrors or Bath Lighting, where accounts their size typically do $150K."

**When Q-57 data is unavailable for this account**: Render only the wallet position line (total business + eCat share) without the category whitespace paragraph.

### C. Companion Products (conditional: SIG-OPP-01 data available for this account)

```html
<div class="callout opportunity">
  <div class="callout-title">Products Frequently Bought Together</div>
  <p><strong>{{N}}</strong> customers who buy <strong>{{ANCHOR_ITEM}}</strong> ({{ANCHOR_DESC}}) also buy <strong>{{SUGGESTED_ITEM}}</strong> ({{SUGGESTED_DESC}}) — this account hasn't.</p>
  <p>Estimated opportunity: ${{AVG_REVENUE}} based on {{N}}-customer purchase pattern.</p>
</div>
```

If multiple NBP signals fired for this account, show top 2 by estimated opportunity. Rest omitted.

### D. Reorder Decay (conditional: SIG-DECAY-01 or SIG-DECAY-02 fired for this account)

Use `.callout.insight` (NOT `.callout.alert`) — frame as early warning, not alarm.

```html
<div class="callout insight">
  <div class="callout-title">Reorder Pattern Change</div>
  <p><strong>Account-level:</strong> {{CURRENT_GAP}} days since last order — {{RATIO}}x their normal cadence (avg every {{AVG_INTERVAL}} days). Worth a check-in.</p>
  {{IF predicted_next_order_window available:}}
  <p><strong>Predicted next order window:</strong> Based on their historical cadence, this account's next order was expected around {{EXPECTED_DATE}} ({{DAYS_OVERDUE}} days ago). {{IF seasonal_pattern: "This account historically orders heaviest in {{PEAK_MONTHS}} — the window is {{closing/open}}."}} </p>
  {{/IF}}
  <p><strong>Item-level:</strong></p>
  <table>
    <tr><th>Item</th><th>Description</th><th>Reorder Cycles</th><th>Avg Interval</th><th>Current Gap</th><th>Ratio</th><th>LTM Revenue</th></tr>
    {{ROWS_FOR_ITEMS_WITH_DECAY}}
  </table>
  <p>Dollar exposure if pattern persists: ${{SUM_LTM_OF_DECAYED_ITEMS}} in items where reorder frequency has stretched.</p>
</div>
```

Only include item rows where SIG-DECAY-02 fired. If only SIG-DECAY-01 (account-level) fired, omit the item table and show only the account-level paragraph.

**Predicted Next Order Window** (render when sufficient history exists):
- Compute `expected_next_order_date = last_order_date + avg_interval`
- If `expected_next_order_date` is in the past, show how many days overdue: "Expected around [date] — now [N] days past their normal cadence."
- If `expected_next_order_date` is in the future, show as a deadline: "Based on pattern, next order expected around [date] — [N] days from now."
- **Seasonality enhancement**: If the account's order history shows clear seasonal peaks (>50% of annual volume concentrated in specific months from Q-21 data), add the seasonal context: "This account historically orders heaviest in January and October — you're now past their October window with no reorder." This turns a generic decay signal into a TICKING CLOCK.
- If insufficient history (< 5 reorder cycles), omit the predicted window silently.

### E. Stock-Out Impact (conditional: SIG-ANOMALY-02 fired for items this account buys)

```html
<div class="callout insight">
  <div class="callout-title">Fulfillment Gap</div>
  <table>
    <tr><th>Item</th><th>Description</th><th>LTM Revenue (this account)</th><th>Qty Available</th><th>Next Receipt</th></tr>
    {{ROWS}}
  </table>
  <p>{{N}} items this account orders are currently out of stock, representing ${{SUM}} in LTM revenue. Proactive communication about restock timing protects the relationship.</p>
</div>
```

### F. Competitive Displacement (conditional: SIG-ANOMALY-03 fired for this account)

```html
<div class="callout insight">
  <div class="callout-title">Channel Share Shift</div>
  <p>eCat orders: {{ECAT_YOY}}% (${{ECAT_PRIOR}} → ${{ECAT_LTM}})</p>
  <p>Total business: {{TOTAL_YOY}}% (${{TOTAL_PRIOR}} → ${{TOTAL_LTM}})</p>
  <p>This account's total business is {{growing/flat}} but a smaller share flows through the platform. Re-engaging them on eCat could recapture an estimated ~${{GAP}}.</p>
</div>
```

### G. Pre-Meeting Priority (MANDATORY for every mini-brief)

A single bold sentence at the bottom of each mini-brief. The single most important thing to do about this account.

```html
<p class="prose"><strong>Priority:</strong> {{ONE_SENTENCE_ACTION}}</p>
```

This must name a specific action (call, email, visit), a specific person if rep data available, and reference the highest-ranked signal for this account.

---

## Additional Subsections (after mini-briefs)

**Render order follows the narrative arc**: Intelligence → Opportunity → Risk.
Subsections are numbered for reference but render in the order below, not
numerically.

### 3b. eCat Penetration of Total Business per Customer (Q-52) — INTELLIGENCE

**MANDATORY RENDER**: If `cache/Q-52_results.md` exists AND contains data rows AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-52_results.md`

**Rendering**: Table with top 15 customers by total business GMV:

| Column | Content |
|--------|---------|
| Customer Name | Display name (never expose `customer_code`) |
| State | Customer state |
| Total Business Orders | All-channel order count |
| Total Business GMV | All-channel GMV |
| eCat Orders | eCat-originated order count |
| eCat GMV | eCat-originated GMV |
| eCat Penetration % | `ecat_gmv / total_business_gmv × 100` |

Highlight customers with eCat Penetration > 50% using `.row-highlight` class. Show top 5 visible; remaining in a collapsed `<details>` element.

```html
<div class="subsection">
  <div class="subsection-title">eCat Penetration of Total Business</div>
  <table>
    <tr><th>Customer</th><th>State</th><th>Total Orders</th><th>Total GMV</th><th>eCat Orders</th><th>eCat GMV</th><th>Penetration</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">{{PENETRATION_NARRATIVE}}</div>
</div>
```

**Framing principle**: The penetration spread tells a story about where eCat is winning and where it hasn't landed yet. The what-this-means should identify geographic or customer-segment patterns: "Your New York accounts average 45% eCat adoption while your California accounts average 8% — is that a territory coverage gap or a market difference?" Frame penetration as a winnable game: "Going from 8% to 20% in California alone would add an estimated $X in eCat orders."

**Claim rules**: Reference by `customer_name` only — never expose `customer_code`. "Your top account does $X in total business — Y% flows through eCat." Customers at 0% penetration are legitimate — they buy through other channels but haven't adopted eCat. Frame constructively as activation opportunity, not failure. Never use "ERP."

### 4. Dormant High-Value Accounts (conditional: SIG-RISK-02 signals exist) — RISK (render late)

Source: Q-17 filtered by SIG-RISK-02 threshold ($15K+ historical spend, 90+ days silent).

```html
<div class="subsection">
  <div class="subsection-title">Dormant High-Value Accounts</div>
  <table>
    <tr><th>Customer</th><th>State</th><th>Last Order</th><th>Historical GMV</th><th>Silence vs Normal</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">{{ACTION_IMPLICATIONS}}</div>
</div>
```

"Silence vs Normal" column: show current gap in days and the ratio to normal cadence (e.g., "244 days — 4.7x normal").

### 5. Unactivated High-Value Accounts (conditional: SIG-OPP-02 signals exist) — OPPORTUNITY

Source: Q-53 filtered by SIG-OPP-02 threshold ($50K+ total business, zero eCat).

```html
<div class="subsection">
  <div class="subsection-title">Unactivated High-Value Accounts</div>
  <table>
    <tr><th>Customer</th><th>State</th><th>Total Business GMV (LTM)</th><th>Total Orders</th><th>eCat Orders</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">{{ACTIVATION_OPPORTUNITY_NARRATIVE}}</div>
</div>
```

Frame as "These accounts represent $X in proven demand flowing through other channels. Zero customer acquisition cost — this is pure activation."

### 5b. Enterprise Channel Accounts (conditional: ENTERPRISE_CHANNEL exclusion set is non-empty) `[COLLAPSE]`

**Gate**: Render ONLY if the signal detection pass identified ≥ 1 account as `ENTERPRISE_CHANNEL` (LTM orders ≥ 500 AND 0 lifetime eCat AND org `HAS_CART = false`).

**Purpose**: These accounts (national retailers, big-box chains, marketplace platforms) were EXCLUDED from SIG-OPP-02 because they order via EDI/PO/marketplace — not candidates for iPad activation. This callout acknowledges their existence transparently rather than letting them silently disappear.

**Display**: `[COLLAPSE]` — informational, not actionable.

```html
<details class="subsection collapsed">
  <summary class="subsection-title">Enterprise Channel Accounts ({{N}} excluded from activation analysis) &#9662;</summary>
  <p class="prose">The following accounts are high-volume buyers (500+ orders/year) with zero eCat history. They order through enterprise channels (EDI, direct PO, or marketplace integration) and are not candidates for eCat iPad activation. They are excluded from the "Unactivated High-Value" analysis above.</p>
  <table>
    <tr><th>Account</th><th>State</th><th>Total Business GMV (LTM)</th><th>LTM Orders</th><th>Channel</th></tr>
    {{ROWS — all enterprise accounts, sorted by GMV descending}}
  </table>
  <p class="prose"><strong>Note:</strong> If any of these accounts should be considered for eCat activation (e.g., the relationship has changed or B2B Cart is being added), flag them for reclassification in the next report cycle.</p>
</details>
```

**Channel column**: Infer from order patterns — "EDI/Direct PO" for all (since we can't see the actual channel, the volume + zero eCat pattern implies non-eCat ordering). Do NOT speculate on specific channel names beyond this.

**Claim rules**: Frame neutrally — these are NOT failures or missed opportunities. "Enterprise channel accounts operate outside eCat by design." Never suggest these accounts are problems to solve.

### 6. Geographic Distribution (conditional: geographic concentration or gaps are interesting)

**SKIP if distribution is uniform.** Only render if one state/region accounts for > 30% of revenue OR a clear geographic cluster exists. This is a conditional subsection — do not force it.

If rendered: use a compact table (State, Accounts, LTM GMV, % of Total) with enrichment from Q-54 if available. Collapse after top 5 states.

### 7. Velocity Deceleration Alerts (conditional: SIG-DECAY-04 signals exist) — RISK (render late)

Source: Q-ORG-CONTRACTION filtered by SIG-DECAY-04 threshold (YoY decline > 20%, LTM > $50K).

```html
<div class="subsection">
  <div class="subsection-title">Accounts Contracting Year-Over-Year</div>
  <table>
    <tr><th>Customer</th><th>State</th><th>Prior Year GMV</th><th>LTM GMV</th><th>YoY Change</th><th>Dollar Decline</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">{{CONTRACTION_IMPLICATIONS}}</div>
</div>
```

YoY Change column: use `.badge.danger` for > 30% decline, `.badge.warn` for 20–30%.

### 8. Reorder Velocity & Early Warning (Q-14, Q-14b)

Build from `Q-14_results.md`. Surface reorder frequency patterns and flag accounts showing declining reorder velocity as early churn warnings.

**Gate**: Always render from Q-14. Q-14b enrichment is MANDATORY when its gate is met.

**Rendering**: Show top 5 high-frequency buyers and flagged decelerating accounts.

```html
<div class="subsection">
  <div class="subsection-title">Reorder Velocity & Early Warning</div>
  <table>
    <tr><th>Account</th><th>State</th><th>Orders (LTM)</th><th>Avg Interval (days)</th><th>LTM Revenue</th></tr>
    {{ROWS — top 5 high-frequency buyers}}
  </table>
</div>
```

**8b. Account Velocity Deceleration Alert (Q-14b)**

**MANDATORY RENDER**: If `cache/Q-14b_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` in `gate_flags.md`, this enrichment MUST be rendered as a second part within subsection 8. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-14b_results.md`

**Rendering**: After the Q-14 reorder frequency table, add a `.callout.alert` titled "Deceleration Alert" followed by a table:

| Column | Content |
|--------|---------|
| Account | Customer name (never expose `customer_bill_to_number`) |
| Historical Avg | Historical average order interval (days) |
| Recent Avg | Recent 6-month average order interval (days) |
| Deceleration | Ratio displayed as "X.Xx" (e.g., "1.8x") with `.badge.danger` if ≥2.0, `.badge.warn` if 1.5–1.99 |
| Annual Value | LTM all-channel GMV for this account |

Sort by annual GMV descending. Show top 5 visible; remaining in collapsed `<details>`.

```html
<div class="callout alert">
  <div class="callout-title">Deceleration Alert</div>
  <table>
    <tr><th>Account</th><th>Historical Avg</th><th>Recent Avg</th><th>Deceleration</th><th>Annual Value</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="callout-summary">X accounts show order frequency stretching beyond 1.5x their historical average. Combined annual value at risk: $Y.</div>
</div>
<div class="what-this-means">These accounts are ordering less frequently than their established pattern. If this trend continues, projected at-risk revenue is approximately $Z. Proactive outreach to understand the cause — whether it's seasonal, competitive, or operational — is the highest-leverage action for your team right now.</div>
```

**Claim rules**: "These accounts are ordering less frequently than their established pattern." Always hedge projections: "If this trend continues, projected at-risk revenue is approximately $Z." Use "all-channel order frequency" — never "portal orders" or "ERP." Reference accounts by name only.

### 9. Untapped Category Opportunities (Q-57) — OPPORTUNITY

**MANDATORY RENDER**: If `cache/Q-57_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or either gate is false.

**Data source**: `cache/Q-57_results.md`

**Rendering**: Open with a `.callout.insight` block titled "Untapped Category Opportunity" with a summary: "Your top accounts have zero purchases in X categories where similar accounts are actively buying. Estimated addressable whitespace: $Y." Compute X as count of distinct `missing_category` values; compute Y as sum of `addressable_gap` across all rows.

Then render a table with top 10 rows sorted by `peer_median_spend` descending:

| Column | Content |
|--------|---------|
| Customer | `customer_bill_to_name` (never expose `customer_bill_to_number`) |
| Missing Category | `missing_category` |
| Customer Annual GMV | `customer_annual_gmv` formatted as currency |
| Peer Median Spend | `peer_median_spend` — what similar accounts spend in this category |
| Peers Buying | Count of other accounts actively purchasing in this category |

Show top 5 visible; remaining in collapsed `<details>`.

```html
<div class="subsection">
  <div class="subsection-title">Untapped Category Opportunities</div>
  <div class="callout insight">
    <div class="callout-title">Untapped Category Opportunity</div>
    <p>Your top accounts have zero purchases in {{X}} categories where similar accounts are actively buying. Estimated addressable whitespace: ${{Y}}.</p>
  </div>
  <table>
    <tr><th>Customer</th><th>Missing Category</th><th>Annual GMV</th><th>Peer Median Spend</th><th>Peers Buying</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">These gaps represent product categories where your existing accounts are buying nothing — but similar accounts are actively purchasing. Each row is a specific conversation starter for your reps: "You buy heavily in Lighting but nothing in Mirrors — other accounts your size typically do both." This isn't a guarantee of captured revenue, but it identifies the lowest-friction expansion paths.</div>
</div>
```

**Claim rules**: Always use hedging language — "estimated addressable whitespace," "if adoption matched peer behavior," "opportunity, not certainty." Never guarantee dollar amounts are capturable. Use "similar accounts" not "peers" in client-facing text. Never expose `customer_bill_to_number`. Never use "ERP" — use "your account base" or "accounts in your system."

### 10. Buyer-Within-Account Intelligence (Q-66) — INTELLIGENCE

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `HAS_BUYER_DATA = true` AND `cache/Q-66_results.md` has data rows.

**Display**: Standalone (NOT collapsed). New decision-maker detection within existing accounts — a unique signal no other section provides.

**Data source**: `cache/Q-66_results.md`

**Rendering**: Open with a `.callout.insight` titled "New Decision-Maker Detection" summarizing: "X of your accounts show a new buyer placing orders in the last 90 days. The highest-impact: [top account] added a new contact who placed $Y in their first engagement. New decision-makers signal either internal expansion or a changing buying committee — both demand immediate rep attention."

Compute `X` as row count. Identify the top row by `new_buyer_revenue`.

Then render a table of accounts with new buyers (sorted by `new_buyer_revenue` descending):

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| New Buyers | `new_buyers` |
| Existing Buyers | `existing_buyers` |
| New Buyer Orders | `new_buyer_orders` |
| New Buyer Revenue | `new_buyer_revenue` formatted as currency |

Show top 5 visible; remaining in collapsed `<details>`.

```html
<div class="subsection">
  <div class="subsection-title">Buyer-Within-Account Intelligence</div>
  <div class="callout insight">
    <div class="callout-title">New Decision-Maker Detection</div>
    <p>{{X}} of your accounts show a new buyer placing orders in the last 90 days. The highest-impact: {{TOP_ACCOUNT}} added a new contact who placed ${{Y}} in their first engagement.</p>
  </div>
  <table>
    <tr><th>Account</th><th>New Buyers</th><th>Existing Buyers</th><th>New Buyer Orders</th><th>New Buyer Revenue</th></tr>
    {{ROWS — top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">A new name placing orders within an existing account is one of the clearest signals that your customer relationship is evolving — either the business is growing and bringing on additional buyers, or a new decision-maker has taken over the account. In both cases, your rep needs to know immediately. Proactive outreach to these contacts — while they're still forming vendor preferences — is the highest-ROI relationship action available.</div>
</div>
```

**Claim rules**: Never expose `buyer_name` or `customer_bill_to_number`. Use only account name. Frame as "new decision-maker detected" — expansion opportunity that demands immediate rep relationship-building. Never use "ERP." Never reveal internal buyer identifiers.

### 11. Geographic Revenue Trends (Q-67) — INTELLIGENCE

**MANDATORY RENDER**: If `cache/Q-67_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or either gate is false.

**Display**: Standalone (NOT collapsed). Quarter-over-quarter geographic shift analysis.

**Data source**: `cache/Q-67_results.md`

**Rendering**: This is a standalone geographic analysis subsection (separate from subsection 6's static distribution view). Open with a `.callout.insight` titled "Geographic Revenue Shifts" with a punchy data-driven headline. Build it dynamically:

1. Identify the state with the largest positive `gmv_change_pct` — this is the "breakout market."
2. Identify the state with the largest negative `gmv_change_pct` — this is the "contracting market."
3. Construct the headline: "[Breakout state full name] grew [X]% quarter-over-quarter ($[prior]→$[current]) while [contracting state full name] contracted [Y]%. Your reps added [N] net new customers in growing states — that's market share being won in real time."

Use full state names in the callout headline (Virginia, not VA). Table rows may use abbreviations.

Then render a table of states (top 15 by `current_gmv` descending):

| Column | Content |
|--------|---------|
| State | `state` (abbreviation acceptable in table) |
| Current Quarter | `current_gmv` formatted as currency |
| Prior Quarter | `prior_gmv` formatted as currency |
| QoQ Change | `gmv_change_pct` with `.badge.ok` if positive, `.badge.warn` if -1% to -10%, `.badge.danger` if < -10% |
| Customers | `current_customers` (show `customer_change` as +/- delta, e.g., "643 (+30)") |

Show top 10 visible; remaining in collapsed `<details>`.

```html
<div class="subsection">
  <div class="subsection-title">Geographic Revenue Trends</div>
  <div class="callout insight">
    <div class="callout-title">Geographic Revenue Shifts</div>
    <p>{{DYNAMIC_HEADLINE}}</p>
  </div>
  <table>
    <tr><th>State</th><th>Current Quarter</th><th>Prior Quarter</th><th>QoQ Change</th><th>Customers</th></tr>
    {{ROWS — top 10 visible, rest in <details>}}
  </table>
  <div class="what-this-means">Geography isn't static — it shifts quarter to quarter as reps win or lose momentum. States gaining both revenue and customers are proof of effective coverage; states losing revenue (especially while customer counts hold steady) may signal competitive displacement or shrinking wallet share. Use this as a territory-planning input: where you're growing, double down on coverage; where you're contracting, investigate whether you're losing deals or losing the relationship.</div>
</div>
```

**Claim rules**: Never attribute decline to a specific named competitor or specific cause — say "may indicate competitive pressure," "could signal a coverage gap," or "warrants investigation." Frame growing states as momentum to protect and declining states as requiring attention. Use full state names in headline callouts; abbreviations are acceptable in table cells. Never use internal field names. Never use "ERP."

### 12. Spending Contraction Detection (Q-68) `[COLLAPSE]` — RISK (render last)

**MANDATORY RENDER**: If `cache/Q-68_results.md` exists AND contains data rows AND `HAS_PORTAL_ORDERS = true` AND `PORTAL_CUSTOMER_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or either gate is false.

**Display**: `[COLLAPSE]` — useful directional insight but historical-peak comparisons are approximate. Collapse keeps the section scannable while making this available for detail-oriented readers.

**Data source**: `cache/Q-68_results.md`

**Methodology**: Compare each account's trailing-12-month spend to their own **historical peak spending period** (highest rolling 12-month total in their order history). This surfaces accounts with a demonstrated spending capacity that has contracted — accounts that HAVE spent more, not accounts that SHOULD spend more based on peers.

**Methodology explanation (MUST include in rendered output)**: Before the table, include a `.prose` paragraph:

> "We compare each account's trailing-12-month spend to their own historical peak — the highest rolling 12-month total in their order history. This surfaces accounts with a demonstrated spending capacity that has contracted. These are accounts that have spent more in the past, making re-engagement a recovery conversation rather than a cold growth pitch."

This explanation must appear every time this subsection renders — it is not optional.

**Rendering**: Open with a `.callout.insight` titled "Spending Contraction: Accounts Below Their Peak" summarizing: "X accounts are spending below their historical peak. The combined gap between current and peak spend represents $Y in demonstrated capacity that has not been recaptured."

Compute `X` as row count. Compute `Y` as sum of `gap_to_peak` across all rows.

Then render the methodology explanation `.prose` paragraph (above).

Then render a table of accounts with highest contraction (sorted by `gap_to_peak` descending):

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| State | `primary_state` |
| Current Annual Spend | `customer_spend` formatted as currency |
| Historical Peak Spend | `peak_spend` formatted as currency |
| Contraction | `gap_to_peak` formatted as currency with `.badge.warn` styling |
| Current vs Peak | `current_vs_peak_pct` displayed as percentage (e.g., "38% of peak") |

Show top 8 visible; remaining in collapsed `<details>`.

```html
<div class="subsection collapsed">
  <div class="subsection-title">Spending Contraction Detection</div>
  <div class="callout insight">
    <div class="callout-title">Spending Contraction: Accounts Below Their Peak</div>
    <p>{{X}} accounts are spending below their historical peak. The combined gap between current and peak spend represents ${{Y}} in demonstrated capacity that has not been recaptured.</p>
  </div>
  <p class="prose">We compare each account's trailing-12-month spend to their own historical peak — the highest rolling 12-month total in their order history. This surfaces accounts with a demonstrated spending capacity that has contracted. These are accounts that have spent more in the past, making re-engagement a recovery conversation rather than a cold growth pitch.</p>
  <table>
    <tr><th>Account</th><th>State</th><th>Current Annual Spend</th><th>Historical Peak</th><th>Contraction</th><th>Current vs Peak</th></tr>
    {{ROWS — top 8 visible, rest in <details>}}
  </table>
  <div class="what-this-means">These accounts have a demonstrated spending capacity that exceeds their current level — they've proven they can buy at their peak amount, and something changed. The contraction could reflect competitive displacement, changing business needs, relationship drift, or simply a market cycle. What makes these accounts high-value targets is that the rep conversation isn't "you should spend more" — it's "you used to spend $X, what changed?" That's a fundamentally different and more productive dialogue.</div>
</div>
```

**Claim rules**: Always use "demonstrated capacity," "historical peak," and "contraction" — not "should be spending" or "underperforming." Frame as recovery opportunity, not failure. Never expose internal identifiers. Never use "ERP."

---

## Section-Level What-This-Means (MANDATORY)

After all subsections, one `.what-this-means` div for the entire section:

- **Sentence 1**: The actionable takeaway (what to DO first)
- **Sentence 2**: The cost of inaction (what happens if nothing changes)
- **Sentence 3 (optional)**: What additional data would sharpen the picture

---

## Highlight File Output

> Follow `section_shared_contract.md` §4 for the highlight file format.

Save `cache/section_02_highlights.md` with 2–4 candidate highlights from the strongest account-level signals.

---

## Conditional Subsection Checklist

| # | Subsection | Gate(s) | Treatment | Mandatory? |
|---|-----------|---------|-----------|-----------|
| 1 | Header Metrics (Q-12) | Always | Standalone | Yes — always rendered |
| 2 | Data Confidence Header | Always | **ALWAYS at top** (after metrics, before first subsection) | Yes — always rendered |
| 3 | Top 10 Mini-Briefs | Always | Top 5 standalone, 6–10 collapsed | Yes — always rendered |
| 3b | eCat Penetration (Q-52) | `PORTAL_CUSTOMER_DATA_PRESENT = true` + data rows | Standalone | Yes when gate met |
| 4 | Dormant High-Value (Q-17) | SIG-RISK-02 signals exist | Standalone | Conditional |
| 5 | Unactivated High-Value (Q-53) | SIG-OPP-02 signals exist | Standalone | Conditional |
| 5b | Enterprise Channel Accounts | ENTERPRISE_CHANNEL set non-empty | **`[COLLAPSE]`** | Conditional |
| 6 | Geographic Distribution (Q-40/Q-54) | Notable non-uniform distribution | Standalone | Conditional |
| 7 | Velocity Deceleration (Q-ORG-CONTRACTION) | SIG-DECAY-04 signals exist | Standalone | Conditional |
| 8 | Reorder Velocity (Q-14/Q-14b) | Always (Q-14b enrichment conditional) | Standalone | Yes — always rendered |
| 9 | Untapped Category Opportunities (Q-57) | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` + data rows | Standalone | Yes when gate met |
| 10 | Buyer-Within-Account (Q-66) | `HAS_PORTAL_ORDERS` + `HAS_BUYER_DATA` + data rows | **Standalone** | Conditional |
| 11 | Geographic Revenue Trends (Q-67) | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` + data rows | **Standalone** | Yes when gate met |
| 12 | Spending Contraction (Q-68) | `HAS_PORTAL_ORDERS` + `PORTAL_CUSTOMER_DATA_PRESENT` + data rows | **`[COLLAPSE]`** | Yes when gate met |

## TARGET STRUCTURE — Gold Standard (MATCH THIS MARKUP EXACTLY)

This is the corresponding section from the canonical reference report. It is the source of truth for HTML structure: tag nesting, class names, column headers, subsection order, which subsections carry a `what-this-means` block, and the `<thead>`/`<tbody>`/`row-highlight` patterns. The data values below are illustrative — replace them with this client's data — but reproduce the STRUCTURE exactly. Where this target and the prose guide disagree on markup, THIS WINS.

```html
<details class="section-collapse" id="accounts">
  <summary>
    <div class="section-title">Account Intelligence</div>
    <div class="section-sub">1,847 active buyers &middot; 8,942 total accounts &middot; top accounts with actionable briefs</div>
    <div class="section-contents">Revenue snapshots, reorder velocity, companion products, stock-out impact, competitive displacement signals</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section">

    <div class="data-confidence">
      <span class="data-confidence-label">Full Picture</span>
      Account data includes eCat orders, all-channel invoices, inventory availability, and app usage patterns. Revenue figures combine both data sources for a complete view of each account&rsquo;s relationship.
    </div><div class="subsection">
      <div class="subsection-title">1. Heritage Hospitality Group</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">All-Channel LTM</div>
          <div class="metric-value">$1,204,000</div>
          <div class="metric-note warn">&minus;3.2% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">eCat Sales LTM</div>
          <div class="metric-value">$312,000</div>
          <div class="metric-note ok">+8.4% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Reorder Velocity</div>
          <div class="metric-value">68 days</div>
          <div class="metric-note danger">Was 42 days (slowed 38%)</div>
        </div>
        <div class="metric">
          <div class="metric-label">Top Category</div>
          <div class="metric-value">Pendants</div>
          <div class="metric-note">62% of their orders</div>
        </div>
      </div>
      <div class="sub-label">Companion Products Frequently Bought Together</div>
      <p class="prose">Heritage pairs <strong>Solstice Pendant</strong> with <strong>Aurora Sconce</strong> in 78% of their projects. They also bundle the <strong>Meridian Floor Lamp</strong> into lobby specifications.</p>
      <div class="callout insight">
        <div class="callout-title">Competitive Displacement Signal</div>
        <p>Heritage&rsquo;s reorder velocity slowed from 42 to 68 days despite stable all-channel revenue. Investigative hypotheses:</p>
        <ul>
          <li><strong>Project pipeline shift:</strong> Their 2026 renovation calendar shows 3 major projects pushed from Q1 to Q3 (confirmed via trade press)</li>
          <li><strong>Competitor trial:</strong> A regional lighting competitor (Luminar Studios) exhibited at the same BDNY booth as Heritage&rsquo;s procurement director in November 2025</li>
          <li><strong>Stock-out friction:</strong> The Aurora Sconce backorder since March directly impacts their most-ordered SKU &mdash; they may be sourcing alternatives</li>
        </ul>
      </div>
      <div class="sub-label">Pre-Meeting Priority</div>
      <p class="prose">Confirm Aurora Sconce restock date before next contact. Lead with the new Halo Chandelier (similar aesthetic, in-stock) as an alternative for their Q3 projects.</p>
    </div><div class="subsection">
      <div class="subsection-title">2. Coastal Design Partners</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">All-Channel LTM</div>
          <div class="metric-value">$892,000</div>
          <div class="metric-note ok">+14.6% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">eCat Sales LTM</div>
          <div class="metric-value">$478,000</div>
          <div class="metric-note ok">+28.3% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Reorder Velocity</div>
          <div class="metric-value">28 days</div>
          <div class="metric-note ok">Stable</div>
        </div>
        <div class="metric">
          <div class="metric-label">Digital Share</div>
          <div class="metric-value">53.6%</div>
          <div class="metric-note ok">Highest of top 10</div>
        </div>
      </div>
      <div class="sub-label">Companion Products Frequently Bought Together</div>
      <p class="prose">Coastal consistently orders the <strong>Meridian Floor Lamp</strong> + <strong>Driftwood Table Lamp</strong> as a paired set. Their average order includes 3.2 SKUs (vs. 2.1 company average).</p>
      <div class="sub-label">Pre-Meeting Priority</div>
      <p class="prose">Showcase the new Horizon Collection &mdash; their coastal aesthetic preferences align perfectly. Upsell opportunity: they haven&rsquo;t ordered outdoor fixtures yet, estimated $48K annual potential based on their project types.</p>
    </div><div class="subsection">
      <div class="subsection-title">3. Metro Contract Furnishings</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">All-Channel LTM</div>
          <div class="metric-value">$784,000</div>
          <div class="metric-note ok">+22.1% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">eCat Sales LTM</div>
          <div class="metric-value">$196,000</div>
          <div class="metric-note ok">+41.7% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Reorder Velocity</div>
          <div class="metric-value">35 days</div>
          <div class="metric-note ok">Accelerating (was 44)</div>
        </div>
        <div class="metric">
          <div class="metric-label">Top Category</div>
          <div class="metric-value">Task Lighting</div>
          <div class="metric-note">48% of orders</div>
        </div>
      </div>
      <div class="sub-label">Pre-Meeting Priority</div>
      <p class="prose">Metro&rsquo;s eCat adoption is growing fastest of any account (+41.7% YoY). Their rep James Whitfield should introduce the specification-builder feature &mdash; Metro&rsquo;s multi-unit projects would benefit from saved project templates.</p>
    </div><div class="subsection">
      <div class="subsection-title">4. Summit Interiors</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">All-Channel LTM</div>
          <div class="metric-value">$672,000</div>
          <div class="metric-note ok">+7.8% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">eCat Sales LTM</div>
          <div class="metric-value">$284,000</div>
          <div class="metric-note ok">+16.2% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Reorder Velocity</div>
          <div class="metric-value">31 days</div>
          <div class="metric-note ok">Consistent</div>
        </div>
        <div class="metric">
          <div class="metric-label">Top Category</div>
          <div class="metric-value">Chandeliers</div>
          <div class="metric-note">55% of orders</div>
        </div>
      </div>
      <div class="sub-label">Pre-Meeting Priority</div>
      <p class="prose">Summit is your highest-value chandelier buyer. They haven&rsquo;t seen the Halo Chandelier yet (launched after their last order). Given their project size ($18K avg order), a single conversion on Halo could be your largest single-SKU order this quarter.</p>
    </div><div class="subsection">
      <div class="subsection-title">5. Pinnacle Hotel Group</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">All-Channel LTM</div>
          <div class="metric-value">$618,000</div>
          <div class="metric-note warn">&minus;8.4% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">eCat Sales LTM</div>
          <div class="metric-value">$142,000</div>
          <div class="metric-note warn">&minus;12.1% YoY</div>
        </div>
        <div class="metric">
          <div class="metric-label">Reorder Velocity</div>
          <div class="metric-value">52 days</div>
          <div class="metric-note warn">Was 38 days</div>
        </div>
        <div class="metric">
          <div class="metric-label">Top Category</div>
          <div class="metric-value">Wall Sconces</div>
          <div class="metric-note">44% of orders</div>
        </div>
      </div>
      <div class="sub-label">Stock-Out Impact</div>
      <p class="prose">Pinnacle&rsquo;s primary SKU (Aurora Sconce) has been on backorder since March. Their last 3 quote requests went unfulfilled &mdash; estimated $38K in lost Q2 orders directly attributable to this stockout.</p>
      <div class="sub-label">Pre-Meeting Priority</div>
      <p class="prose">Urgent: provide a restock timeline or offer the Nova Sconce as an alternative before Pinnacle sources externally. Their procurement cycle for Q3 hotel renovations starts in 3 weeks.</p>
    </div><details>
      <summary>Accounts 6&ndash;10</summary>
      <div style="padding: 16px 0;">
        <div class="subsection">
          <div class="subsection-title">6. Lakeside Living Showrooms</div>
          <div class="metrics">
            <div class="metric"><div class="metric-label">All-Channel LTM</div><div class="metric-value">$542,000</div><div class="metric-note ok">+18.9% YoY</div></div>
            <div class="metric"><div class="metric-label">eCat Sales LTM</div><div class="metric-value">$298,000</div><div class="metric-note ok">+34.2% YoY</div></div>
            <div class="metric"><div class="metric-label">Reorder Velocity</div><div class="metric-value">21 days</div><div class="metric-note ok">Fastest account</div></div>
          </div>
          <p class="prose">Lakeside has the fastest reorder cadence in your book. They order small batches frequently for their 6 showroom locations. Their digital share (55%) is your highest. Opportunity: introduce them to the Multi-Ship feature to streamline their per-location ordering.</p>
        </div>

        <div class="subsection">
          <div class="subsection-title">7. Broadmoor Design Collective</div>
          <div class="metrics">
            <div class="metric"><div class="metric-label">All-Channel LTM</div><div class="metric-value">$498,000</div><div class="metric-note ok">+11.2% YoY</div></div>
            <div class="metric"><div class="metric-label">eCat Sales LTM</div><div class="metric-value">$186,000</div><div class="metric-note ok">+22.8% YoY</div></div>
            <div class="metric"><div class="metric-label">Reorder Velocity</div><div class="metric-value">38 days</div><div class="metric-note">Stable</div></div>
          </div>
          <p class="prose">Broadmoor&rsquo;s purchasing is consolidating onto eCat. They historically split orders across phone and email; now 37% digital. Their project pipeline for H2 2026 includes 2 boutique hotel renovations &mdash; estimated $120K incremental.</p>
        </div>

        <div class="subsection">
          <div class="subsection-title">8. Urban Loft Studios</div>
          <div class="metrics">
            <div class="metric"><div class="metric-label">All-Channel LTM</div><div class="metric-value">$463,000</div><div class="metric-note ok">+6.4% YoY</div></div>
            <div class="metric"><div class="metric-label">eCat Sales LTM</div><div class="metric-value">$224,000</div><div class="metric-note ok">+19.7% YoY</div></div>
            <div class="metric"><div class="metric-label">Reorder Velocity</div><div class="metric-value">33 days</div><div class="metric-note ok">Improving</div></div>
          </div>
          <p class="prose">Urban Loft buys almost exclusively from the Modern Collection. They haven&rsquo;t ordered any Traditional or Transitional styles. Good candidate for the new Fusion series (modern-traditional crossover).</p>
        </div>

        <div class="subsection">
          <div class="subsection-title">9. Hartwell &amp; Associates</div>
          <div class="metrics">
            <div class="metric"><div class="metric-label">All-Channel LTM</div><div class="metric-value">$421,000</div><div class="metric-note warn">&minus;14.8% YoY</div></div>
            <div class="metric"><div class="metric-label">eCat Sales LTM</div><div class="metric-value">$94,000</div><div class="metric-note warn">&minus;21.3% YoY</div></div>
            <div class="metric"><div class="metric-label">Reorder Velocity</div><div class="metric-value">64 days</div><div class="metric-note warn">Slowing</div></div>
          </div>
          <p class="prose">Hartwell is shrinking but not yet at competitive-displacement thresholds. Their purchasing manager retired in Q4 2025; the replacement may not be familiar with eCat. Schedule an introductory session with the new buyer.</p>
        </div>

        <div class="subsection">
          <div class="subsection-title">10. Pacific Rim Hospitality</div>
          <div class="metrics">
            <div class="metric"><div class="metric-label">All-Channel LTM</div><div class="metric-value">$394,000</div><div class="metric-note ok">+9.7% YoY</div></div>
            <div class="metric"><div class="metric-label">eCat Sales LTM</div><div class="metric-value">$168,000</div><div class="metric-note ok">+26.4% YoY</div></div>
            <div class="metric"><div class="metric-label">Reorder Velocity</div><div class="metric-value">29 days</div><div class="metric-note ok">Stable</div></div>
          </div>
          <p class="prose">Pacific Rim&rsquo;s eCat adoption is accelerating ahead of their overall growth. They respond well to new product notifications &mdash; they ordered the Halo Chandelier within 48 hours of it appearing in the catalog. Strong candidate for early access on future launches.</p>
        </div>
      </div>
    </details>

    <div class="what-this-means" style="margin-top:20px;">
      <strong>Action:</strong> Your top 10 accounts represent $6.49M in all-channel business. The two at-risk accounts (Heritage Hospitality, Pinnacle Hotel Group) share a common pain point: Aurora Sconce stockout. Resolving that single inventory issue protects an estimated $1.82M in annual revenue across both accounts.
    </div>

    <div class="callout note" style="margin-top:16px;">
      <div class="callout-title">With Connected Data</div>
      Integrating your CRM would add contact-level intelligence (who within each account is the eCat user vs. the decision-maker) and let us correlate trade show interactions with post-event order spikes.
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

## M. Competitive Hypothesis Requirement

When ANY account shows a year-over-year decline exceeding 25% AND the account's LTM revenue exceeds $50K, the report MUST include 2–3 investigative hypotheses explaining the decline. This applies in:
- Account mini-briefs (subsection F: Competitive Displacement)
- Velocity Deceleration subsection (section 2, subsection 7)
- Spending Contraction subsection (section 2, subsection 12)

### Rules

1. **We cannot see competitors.** Never state "they are buying from [competitor]" as fact. Always frame as hypothesis.
2. **Provide 2–3 plausible explanations**, ordered by likelihood based on available evidence:
   - Channel consolidation ("may have consolidated vendors or shifted to direct-import sourcing")
   - Competitive displacement ("a competitor may have captured this relationship with better pricing or service")
   - Internal change ("the account may have exited a market segment, lost a key project, or changed buying committee")
   - Pricing sensitivity ("if your prices increased, the volume drop may reflect a price elasticity response")
   - Seasonal/cyclical ("if this account is project-driven, the decline may reflect normal project completion rather than relationship loss")
3. **Always close with a specific investigative action**: "The rep assigned to this account should ask directly — a 63% decline is almost never accidental, and the cause determines the response."
4. **Acknowledge the limitation explicitly** when relevant: "We can see the decline but not the cause — here are the most likely explanations based on the pattern."

### Format

```html
<div class="callout insight">
  <div class="callout-title">Decline Investigation: {{ACCOUNT_NAME}}</div>
  <p><strong>The pattern:</strong> {{PRIOR_GMV}} → {{LTM_GMV}} ({{DECLINE_PCT}}% decline, ${{DOLLAR_DECLINE}} in lost annual volume)</p>
  <p><strong>Hypotheses:</strong></p>
  <ol>
    <li>{{HYPOTHESIS_1}}</li>
    <li>{{HYPOTHESIS_2}}</li>
    <li>{{HYPOTHESIS_3_IF_APPLICABLE}}</li>
  </ol>
  <p><strong>Next step:</strong> {{SPECIFIC_INVESTIGATIVE_ACTION}}</p>
</div>
```

### Threshold

Only render competitive hypotheses when BOTH conditions are met:
- YoY decline > 25%
- Account LTM revenue > $50K (or prior-year revenue > $50K if current is lower)

Below these thresholds, the standard what-this-means framing is sufficient.


## Cache Data

### signal_rank.md

# Signal Rank — EGLO Canada (eglo_can, org_id=232)
- **Run date**: can_2026-06-17
- **Total signals fired**: 26 (P0: 12, P1: 11, P2: 3)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 205989A (Trago 5 - 12" 5CCT LED Ceiling Light / P) $72,729 LTM, 0 available | P0 | §3 Product | 10.0 | $72,729 | 3.0 | 2,181,874 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 39267A (Climene - LED Pendant Light / LED Lumina) $25,446 LTM, 0 available | P0 | §3 Product | 10.0 | $25,446 | 3.0 | 763,388 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 205292A (Rafaelino - 1L Pendant Light / Luminaire) $22,094 LTM, 0 available | P0 | §3 Product | 10.0 | $22,094 | 3.0 | 662,809 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 390466A (Fruitera - 6L 3CCT LED Pendant Light / L) $21,901 LTM, 0 available | P0 | §3 Product | 10.0 | $21,901 | 3.0 | 657,026 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 205986A (Trago 5 - 9" 5CCT LED Ceiling Light / Pl) $18,183 LTM, 0 available | P0 | §3 Product | 10.0 | $18,183 | 3.0 | 545,492 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 205988A (Trago 5 - 7" 5CCT LED Ceiling Light / Pl) $13,266 LTM, 0 available | P0 | §3 Product | 10.0 | $13,266 | 3.0 | 397,989 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 206938A (Grazia - LED Linear Chandelier / Lustre ) $11,773 LTM, 0 available | P0 | §3 Product | 10.0 | $11,773 | 3.0 | 353,179 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 206937A (Grazia - LED Chandelier / Lustre DEL) $11,460 LTM, 0 available | P0 | §3 Product | 10.0 | $11,460 | 3.0 | 343,787 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 205131A (Troy 3 - 1L Pendant Light / Luminaire su) $10,553 LTM, 0 available | P0 | §3 Product | 10.0 | $10,553 | 3.0 | 316,577 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 85977A (Troy 3 - 1L Pendant Light / Luminaire su) $10,439 LTM, 0 available | P0 | §3 Product | 10.0 | $10,439 | 3.0 | 313,169 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 390342A (Dracera - 10L Linear LED Pendant / Lumin) $10,409 LTM, 0 available | P0 | §3 Product | 10.0 | $10,409 | 3.0 | 312,274 | RISK |
| 12 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 49% of eCat GMV | P1 | §4 Commerce | 1.2 | $126,661 | 2.0 | 308,350 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 200146A (Ascoli - 1L Exterior Wall Light / Murale) $10,250 LTM, 0 available | P0 | §3 Product | 10.0 | $10,250 | 3.0 | 307,515 | RISK |
| 14 | SIG-OPP-04 | New Item Adoption Gap — 7 new items with $0 platform orders | P2 | §3 Product | 0.7 | $50,000 | 1.0 | 35,000 | POSITIVE |
| 15 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 12 | 0 | 1 | 13 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 2 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 7 new items with $0 platform orders
2. **[RISK]** SIG-ANOMALY-02: Stock Out — 205989A (Trago 5 - 12" 5CCT LED Ceiling Light / P) $72,729 LTM, 0 available
3. **[RISK]** SIG-ANOMALY-02: Stock Out — 39267A (Climene - LED Pendant Light / LED Lumina) $25,446 LTM, 0 available
4. **[RISK]** SIG-ANOMALY-02: Stock Out — 205292A (Rafaelino - 1L Pendant Light / Luminaire) $22,094 LTM, 0 available
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 390466A (Fruitera - 6L 3CCT LED Pendant Light / L) $21,901 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 205986A (Trago 5 - 9" 5CCT LED Ceiling Light / Pl) $18,183 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 205988A (Trago 5 - 7" 5CCT LED Ceiling Light / Pl) $13,266 LTM, 0 available

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — EGLO Canada (eglo_can, org_id=232)
- **Run date**: can_2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |

### Q-12_results.md

# Q-12 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 787 | 73 | 37 | 31 | 2 |

### Q-14_results.md

# Q-14 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-14b_results.md

(not present — file does not exist or is empty)

### Q-17_results.md

# Q-17 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 0000820296 | Royaume Luminaire - St-Basile | QC | 2026-01-12 19:03:17 | 1 | $28,830 |
| 0000820298 | Royaume Luminaire - Terrebonne | QC | 2026-01-12 16:08:24 | 1 | $27,849 |
| 0000820295 | Royaume Luminaire - Sherbrooke | QC | 2026-01-12 16:57:07 | 1 | $24,914 |
| 0000820299 | Royaume Luminaire - Tr.Rivieres | QC | 2026-01-12 19:40:12 | 1 | $23,031 |
| 0000821644 | Dhillon Lighting - Calgary | AB | 2026-01-30 23:35:21 | 1 | $22,037 |
| 0000820274 | Royaume Luminaire - Drummond | QC | 2026-01-12 18:19:40 | 1 | $21,923 |
| 0000820297 | Royaume Luminaire - Ste Julie | QC | 2026-01-12 21:02:11 | 1 | $19,964 |
| 0000820273 | Royaume Luminaire - Beauport | QC | 2026-01-12 20:34:46 | 1 | $19,098 |
| 0000820270 | Living Lighting #8 Napean | ON | 2025-12-23 13:32:28 | 1 | $14,897 |
| 0000822002 | Edmonton Lighting & Decor Inc. | AB | 2026-01-30 22:48:14 | 1 | $13,106 |
| 0000820390 | Super Lite Lighting | MB | 2026-01-30 22:50:59 | 1 | $12,824 |
| 0000820282 | Luminaire Alder inc | QC | 2026-02-04 16:54:35 | 1 | $8,232 |
| 0000820363 | Signature Lighting and Fans | AB | 2026-01-30 22:50:06 | 2 | $7,905 |
| 0000822088 | Aura Interiors Inc. | BC | 2026-01-30 22:45:15 | 1 | $6,630 |
| 0000820524 | Paradise Lighting/ MaxTraders Inc | ON | 2026-01-30 15:16:13 | 1 | $6,198 |
| 0000820330 | Pine Lighting - Surrey | BC | 2026-01-30 22:49:08 | 1 | $5,642 |
| 0000820359 | The Lighting Warehouse | BC | 2026-01-30 22:51:46 | 1 | $5,526 |
| 0000820489 | Royaume Luminaire - Sorel-Tracy | QC | 2026-01-12 19:58:50 | 1 | $5,025 |
| 0000820555 | Maple Ridge Lighting Inc | BC | 2026-01-30 23:36:33 | 1 | $4,827 |
| 0000821021 | Twin Bridge Lighting | ON | 2026-02-10 10:20:28 | 2 | $4,716 |
| 0000821449 | Paradise Lighting - Burlington | ON | 2026-01-30 15:16:48 | 1 | $4,200 |
| 0000820339 | Carrington Lighting - North Store | AB | 2025-06-20 16:12:37 | 1 | $3,809 |
| 0000820289 | CDE - St Jerome | QC | 2025-08-13 18:06:09 | 1 | $3,701 |
| 0000820508 | Unique Lighting | SK | 2026-01-30 22:52:32 | 1 | $3,111 |
| 0000822166 | Royal Lighting | ON | 2026-02-14 19:44:28 | 2 | $2,868 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 0000820296 | Royaume Luminaire - St-Basile | QC | $28,830 | 2026-01-12 19:03:17 | 156 |
| 0000820298 | Royaume Luminaire - Terrebonne | QC | $27,849 | 2026-01-12 16:08:24 | 156 |
| 0000820295 | Royaume Luminaire - Sherbrooke | QC | $24,914 | 2026-01-12 16:57:07 | 156 |
| 0000820299 | Royaume Luminaire - Tr.Rivieres | QC | $23,031 | 2026-01-12 19:40:12 | 156 |
| 0000821644 | Dhillon Lighting - Calgary | AB | $22,037 | 2026-01-30 23:35:21 | 137 |
| 0000820274 | Royaume Luminaire - Drummond | QC | $21,923 | 2026-01-12 18:19:40 | 156 |
| 0000820297 | Royaume Luminaire - Ste Julie | QC | $19,964 | 2026-01-12 21:02:11 | 155 |
| 0000820273 | Royaume Luminaire - Beauport | QC | $19,098 | 2026-01-12 20:34:46 | 155 |
| 0000820270 | Living Lighting #8 Napean | ON | $14,897 | 2025-12-23 13:32:28 | 176 |
| 0000822002 | Edmonton Lighting & Decor Inc. | AB | $13,106 | 2026-01-30 22:48:14 | 137 |
| 0000820390 | Super Lite Lighting | MB | $12,824 | 2026-01-30 22:50:59 | 137 |
| 0000820282 | Luminaire Alder inc | QC | $8,232 | 2026-02-04 16:54:35 | 133 |
| 0000820363 | Signature Lighting and Fans | AB | $7,905 | 2026-01-30 22:50:06 | 137 |
| 0000822088 | Aura Interiors Inc. | BC | $6,630 | 2026-01-30 22:45:15 | 137 |
| 0000820524 | Paradise Lighting/ MaxTraders Inc | ON | $6,198 | 2026-01-30 15:16:13 | 138 |
| 0000820330 | Pine Lighting - Surrey | BC | $5,642 | 2026-01-30 22:49:08 | 137 |
| 0000820359 | The Lighting Warehouse | BC | $5,526 | 2026-01-30 22:51:46 | 137 |
| 0000820489 | Royaume Luminaire - Sorel-Tracy | QC | $5,025 | 2026-01-12 19:58:50 | 156 |
| 0000820555 | Maple Ridge Lighting Inc | BC | $4,827 | 2026-01-30 23:36:33 | 137 |
| 0000821021 | Twin Bridge Lighting | ON | $4,716 | 2026-02-10 10:20:28 | 127 |

### Q-40_results.md

# Q-40 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| QC | 12 | 12 | $193,560 |
| AB | 4 | 5 | $46,857 |
| ON | 14 | 16 | $44,939 |
| BC | 4 | 4 | $22,625 |
| MB | 1 | 1 | $12,824 |
| SK | 2 | 2 | $4,366 |

### Q-41_results.md

# Q-41 Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 2 |
| 2025-04-01 | Rep-Acquired (iPad) | 1 |
| 2025-05-01 | Rep-Acquired (iPad) | 1 |
| 2025-06-01 | Rep-Acquired (iPad) | 3 |
| 2025-08-01 | Rep-Acquired (iPad) | 1 |
| 2025-09-01 | Rep-Acquired (iPad) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 4 |
| 2026-02-01 | Rep-Acquired (iPad) | 1 |
| 2026-03-01 | Rep-Acquired (iPad) | 3 |
| 2026-05-01 | Rep-Acquired (iPad) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 8
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Kevin  Taylor | 4 |
| Samuel Demers | 4 |
| Brittney Hayes | 3 |
| Arienne Mulligan | 3 |
| Karen Hoffman | 1 |
| Gary Ellis | 1 |
| Adam Hayes | 1 |
| Matt Sullivan | 1 |

### Q-52_results.md

(not present — file does not exist or is empty)

### Q-53_results.md

(not present — file does not exist or is empty)

### Q-54_results.md

(not present — file does not exist or is empty)

### Q-57_results.md

(not present — file does not exist or is empty)

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

(not present — file does not exist or is empty)

### Q-68_results.md

(not present — file does not exist or is empty)

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

(not present — file does not exist or is empty)

### Q-ORG-NBP_results.md

(not present — file does not exist or is empty)

### Q-ORG-CONTRACTION_results.md

(not present — file does not exist or is empty)

### Q-ORG-VELOCITY_results.md

(not present — file does not exist or is empty)

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — EGLO Canada (eglo_can, org_id=232)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 205989A | Trago 5 - 12" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 12" | COL804 | 72,729.13 | 3,508 | — | — | [{'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 9858.0}, {'customer': 'Marchand Electric Co. Ltd.', 'revenue': 8051.76}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 6494.84}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 6494.58}, {'customer': 'Richardson Lighting - Regina', 'revenue': 6437.61}, {'customer': 'Éclairage M&M', 'revenue': 4692.0}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 4409.6}, {'customer': 'CDE - Laval', 'revenue': 4329.72}, {'customer': 'Electrimat Ltee', 'revenue': 3263.01}, {'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 3175.26}, {'customer': 'The Lighting Shoppe - London', 'revenue': 2862.0}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 2217.0}, {'customer': 'Chatelaine Lighting Supply Ltd', 'revenue': 1908.0}, {'customer': 'Royaume Luminaire - St-Basile', 'revenue': 1226.8}, {'customer': 'Living Lighting # 38 London', 'revenue': 1191.54}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 1154.64}, {'customer': 'City Electric Supply - Caledon', 'revenue': 1077.6}, {'customer': 'Lumen - Laval', 'revenue': 842.6}, {'customer': 'Lighting Reflects Design', 'revenue': 689.0}, {'customer': 'Total Lighting Sales', 'revenue': 569.7}, {'customer': 'Struktura Design & Architecture', 'revenue': 318.0}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 318.0}, {'customer': 'Preston Hardware', 'revenue': 318.0}, {'customer': 'Twin Bridge Lighting', 'revenue': 246.87}, {'customer': 'Guildwood Lighting & Fireside', 'revenue': 212.0}, {'customer': 'La Galerie du Tapis', 'revenue': 106.0}, {'customer': 'Guillevin International - Dartmouth', 'revenue': 79.5}, {'customer': 'Design Electrical', 'revenue': 53.0}, {'customer': 'Guillevin International - St-Leonard', 'revenue': 53.0}, {'customer': 'Park Lighting', 'revenue': 26.5}, {'customer': 'Lumisolution Inc.', 'revenue': 26.5}, {'customer': 'Deco Luminaire - Québec', 'revenue': 26.5}] | [{'item': '204072', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1737}, {'item': '203766', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 1284}, {'item': '203762', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 1247}, {'item': '203897', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1234}, {'item': '203899', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1115}, {'item': '203759', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 956}, {'item': '204074', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 690}, {'item': '203771', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 640}, {'item': '204945A', 'desc': 'Trago - 7" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 7" carré', 'available': 610}, {'item': '203764', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 552}, {'item': '204073', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 513}, {'item': '204947', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 512}, {'item': '204946', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 466}, {'item': '205987A', 'desc': 'Trago 5 - 5" 5CCT LED Ceiling Light / Plafonnier 5CCT DEL 5"', 'available': 385}, {'item': '203778', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 339}, {'item': '203763', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 331}, {'item': '203773', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 326}, {'item': '203775', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 276}, {'item': '203898', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 259}, {'item': '203768', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 255}, {'item': '203765', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 254}, {'item': '203678A', 'desc': 'Trago - 9" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 9" carré', 'available': 252}, {'item': '203776', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 183}, {'item': '203774', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 163}, {'item': '203901', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 161}, {'item': '203777', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 157}, {'item': '204075', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 106}, {'item': '203761', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 103}, {'item': '203679A', 'desc': 'Trago - 12" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 12" carré', 'available': 95}, {'item': '205495A', 'desc': 'Trago 2 - 16" 3 CCT LED Ceiling Light / Plafonnier DEL 3 CCT 16"', 'available': 6}] |
| 39267A | Climene - LED Pendant Light / LED Luminaire suspendu | COL242 | 25,446.25 | 200 | — | — | [{'customer': 'Multi Luminaire Gatineau', 'revenue': 23378.64}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 537.3}, {'customer': 'Deco Luminaire - Brossard', 'revenue': 405.96}, {'customer': 'Luminaires Repentigny', 'revenue': 270.64}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 159.2}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 153.23}, {'customer': 'Deco Luminaire - Québec', 'revenue': 135.32}, {'customer': 'Luminaire Expert R.T. Inc.', 'revenue': 135.32}, {'customer': 'Luminaires & Cie Inc', 'revenue': 135.32}, {'customer': 'Deco Luminaire - Terrebonne', 'revenue': 135.32}] | [{'item': '204376A', 'desc': 'Climene - LED Pendant Light / Luminaire suspendu DEL', 'available': 52}] |
| 205292A | Rafaelino - 1L Pendant Light / Luminaire suspendu 1L | COL751 | 22,093.63 | 313 | — | — | [{'customer': 'Eclairage Raymond inc', 'revenue': 10545.2}, {'customer': 'Multi Luminaire Granby', 'revenue': 3120.0}, {'customer': 'Eecol Electric Corp - Saskatoon', 'revenue': 1954.08}, {'customer': 'Richardson Lighting - Regina', 'revenue': 1752.0}, {'customer': 'Eurolite', 'revenue': 1530.0}, {'customer': 'Multi Luminaire Lévis', 'revenue': 884.0}, {'customer': 'Multi Luminaire Laval', 'revenue': 544.0}, {'customer': 'Guillevin International - Terrebonne', 'revenue': 412.0}, {'customer': 'Cartwright Lighting', 'revenue': 315.0}, {'customer': 'Franklin Empire - Mont-Royal', 'revenue': 315.0}, {'customer': 'Dhillon Lighting - Calgary', 'revenue': 290.0}, {'customer': 'Park Lighting', 'revenue': 239.4}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 192.95}] | [{'item': '206244A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 192}, {'item': '206243A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 162}, {'item': '205291A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 147}, {'item': '204324A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 107}, {'item': '205295A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 59}, {'item': '204325A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 28}, {'item': '206242A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 12}] |
| 390466A | Fruitera - 6L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 6L | COL300 | 21,900.86 | 40 | — | — | [{'customer': 'Alberta Lighting & Décor', 'revenue': 5100.63}, {'customer': 'Park Lighting', 'revenue': 3175.2}, {'customer': 'Multi Luminaire Laval', 'revenue': 3084.48}, {'customer': 'Union Lighting & Furnishings', 'revenue': 2113.02}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 1722.19}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 1458.7}, {'customer': 'Deco Luminaire - Terrebonne', 'revenue': 1209.6}, {'customer': 'Cartwright Lighting', 'revenue': 1058.4}, {'customer': 'Paradise Lighting - Burlington', 'revenue': 982.8}, {'customer': 'Edmonton Lighting & Decor Inc.', 'revenue': 680.4}, {'customer': 'Multi Luminaire Granby', 'revenue': 514.08}, {'customer': 'Luminaire Galarneau', 'revenue': 423.36}, {'customer': 'Paradise Lighting/ MaxTraders Inc', 'revenue': 378.0}] | [{'item': '390463A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 15}, {'item': '390467A', 'desc': 'Fruitera - 1L 3CCT LED Table Lamp / Lampe de table DEL 3CCT 1L', 'available': 13}, {'item': '390464A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 12}] |
| 205986A | Trago 5 - 9" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 9" | COL804 | 18,183.08 | 1,183 | — | — | [{'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 3280.0}, {'customer': 'Royaume Luminaire - Ste Julie', 'revenue': 3189.63}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 2551.71}, {'customer': 'Richardson Lighting - Regina', 'revenue': 2476.23}, {'customer': 'Éclairage M&M', 'revenue': 1968.0}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 1275.86}, {'customer': 'CDE - Laval', 'revenue': 671.52}, {'customer': 'Corlite Distributors Inc.', 'revenue': 590.4}, {'customer': 'City Electric Supply - Caledon', 'revenue': 469.84}, {'customer': 'Living Lighting # 38 London', 'revenue': 405.71}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 391.72}, {'customer': 'Marchand Electric Co. Ltd.', 'revenue': 265.81}, {'customer': 'The Lighting Shoppe - London', 'revenue': 221.4}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 167.88}, {'customer': 'Living Lighting #8 Napean', 'revenue': 107.62}, {'customer': 'Electrimat Ltee', 'revenue': 60.27}, {'customer': 'La Galerie du Tapis', 'revenue': 41.0}, {'customer': 'Total Lighting Sales', 'revenue': 27.98}, {'customer': 'Lumen - Laval', 'revenue': 20.5}] | [{'item': '204072', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1737}, {'item': '203766', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 1284}, {'item': '203762', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 1247}, {'item': '203897', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1234}, {'item': '203899', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1115}, {'item': '203759', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 956}, {'item': '204074', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 690}, {'item': '203771', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 640}, {'item': '204945A', 'desc': 'Trago - 7" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 7" carré', 'available': 610}, {'item': '203764', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 552}, {'item': '204073', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 513}, {'item': '204947', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 512}, {'item': '204946', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 466}, {'item': '205987A', 'desc': 'Trago 5 - 5" 5CCT LED Ceiling Light / Plafonnier 5CCT DEL 5"', 'available': 385}, {'item': '203778', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 339}, {'item': '203763', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 331}, {'item': '203773', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 326}, {'item': '203775', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 276}, {'item': '203898', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 259}, {'item': '203768', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 255}, {'item': '203765', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 254}, {'item': '203678A', 'desc': 'Trago - 9" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 9" carré', 'available': 252}, {'item': '203776', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 183}, {'item': '203774', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 163}, {'item': '203901', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 161}, {'item': '203777', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 157}, {'item': '204075', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 106}, {'item': '203761', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 103}, {'item': '203679A', 'desc': 'Trago - 12" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 12" carré', 'available': 95}, {'item': '205495A', 'desc': 'Trago 2 - 16" 3 CCT LED Ceiling Light / Plafonnier DEL 3 CCT 16"', 'available': 6}] |
| 205988A | Trago 5 - 7" 5CCT LED Ceiling Light / Plafonnier DEL 5CCT 7" | COL804 | 13,266.30 | 970 | — | — | [{'customer': 'JC Eclairage inc.', 'revenue': 5376.0}, {'customer': 'The Lighting Shoppe - London', 'revenue': 1555.2}, {'customer': 'Electrimat Ltee', 'revenue': 1508.24}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 959.2}, {'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 820.11}, {'customer': 'CDE - Laval', 'revenue': 575.52}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 480.0}, {'customer': 'Chatelaine Lighting Supply Ltd', 'revenue': 384.0}, {'customer': 'Richardson Lighting - Regina', 'revenue': 287.76}, {'customer': 'Living Lighting # 38 London', 'revenue': 215.82}, {'customer': 'Lighting Reflects Design', 'revenue': 192.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 191.84}, {'customer': 'DND Electrical & AV Inc', 'revenue': 172.8}, {'customer': 'City Electric Supply - Caledon', 'revenue': 143.88}, {'customer': 'Deco Luminaire - Terrebonne', 'revenue': 115.2}, {'customer': 'Design Electrical', 'revenue': 96.0}, {'customer': 'Total Lighting Sales', 'revenue': 83.93}, {'customer': 'Cimpexco Entreprise Import Export Inc', 'revenue': 76.8}, {'customer': 'Luminaires Repentigny', 'revenue': 16.0}, {'customer': 'Struktura Design & Architecture', 'revenue': 16.0}] | [{'item': '204072', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1737}, {'item': '203766', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 1284}, {'item': '203762', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 1247}, {'item': '203897', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1234}, {'item': '203899', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 1115}, {'item': '203759', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 956}, {'item': '204074', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 690}, {'item': '203771', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 640}, {'item': '204945A', 'desc': 'Trago - 7" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 7" carré', 'available': 610}, {'item': '203764', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 552}, {'item': '204073', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 513}, {'item': '204947', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 512}, {'item': '204946', 'desc': 'Trago - Trim 7" Square / Finition 7" carré', 'available': 466}, {'item': '205987A', 'desc': 'Trago 5 - 5" 5CCT LED Ceiling Light / Plafonnier 5CCT DEL 5"', 'available': 385}, {'item': '203778', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 339}, {'item': '203763', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 331}, {'item': '203773', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 326}, {'item': '203775', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 276}, {'item': '203898', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 259}, {'item': '203768', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 255}, {'item': '203765', 'desc': 'Trago - Trim 9" Round / Finition 9" rond', 'available': 254}, {'item': '203678A', 'desc': 'Trago - 9" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 9" carré', 'available': 252}, {'item': '203776', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 183}, {'item': '203774', 'desc': 'Trago - Trim 9" Square / Finition 9" carré', 'available': 163}, {'item': '203901', 'desc': 'Trago - Trim 5" Round / Finition 5" rond', 'available': 161}, {'item': '203777', 'desc': 'Trago - Trim 12" Square / Finition 12" carré', 'available': 157}, {'item': '204075', 'desc': 'Trago - Trim 12" Round / Finition 12" rond', 'available': 106}, {'item': '203761', 'desc': 'Trago - Trim 7" Round / Finition 7" rond', 'available': 103}, {'item': '203679A', 'desc': 'Trago - 12" Square 3000K LED Ceiling Light / Plafonnier DEL 3000K 12" carré', 'available': 95}, {'item': '205495A', 'desc': 'Trago 2 - 16" 3 CCT LED Ceiling Light / Plafonnier DEL 3 CCT 16"', 'available': 6}] |
| 206938A | Grazia - LED Linear Chandelier / Lustre linéair DEL | COL31 | 11,772.62 | 55 | — | — | [{'customer': 'Multi Luminaire Laval', 'revenue': 1522.85}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 1305.3}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 1200.12}, {'customer': 'Multi Luminaire Granby', 'revenue': 870.2}, {'customer': 'Dhillon Lighting - Edmonton', 'revenue': 637.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 624.6}, {'customer': 'Super Lite Lighting', 'revenue': 573.0}, {'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 558.86}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 558.86}, {'customer': 'Royaume Luminaire - Drummond', 'revenue': 558.86}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 558.86}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 555.2}, {'customer': 'Luminaire Alder inc', 'revenue': 488.96}, {'customer': 'Multi Luminaire Lévis', 'revenue': 435.1}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 435.1}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 291.2}, {'customer': 'C.E Tang Yuk & Co. Ltd', 'revenue': 225.55}, {'customer': 'Paradise Lighting/ MaxTraders Inc', 'revenue': 191.0}, {'customer': 'Cornwall Lighting & Electrical', 'revenue': 182.0}] | [{'item': '206939A', 'desc': 'Grazia - LED Convertible Pendant Light / Luminaire suspendu convertible DEL', 'available': 15}, {'item': '207774A', 'desc': 'Grazia - LED Chandelier / Lustre DEL', 'available': 15}, {'item': '207775A', 'desc': 'Grazia - LED Linear Chandelier / Lustre linéair DEL', 'available': 8}] |
| 206937A | Grazia - LED Chandelier / Lustre DEL | COL31 | 11,459.56 | 48 | — | — | [{'customer': 'Multi Luminaire Laval', 'revenue': 1753.77}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 1404.37}, {'customer': 'Multi Luminaire Granby', 'revenue': 936.26}, {'customer': 'Dhillon Lighting - Edmonton', 'revenue': 888.7}, {'customer': 'Luminaire Galarneau', 'revenue': 657.6}, {'customer': 'Super Lite Lighting', 'revenue': 616.5}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 601.3}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 598.4}, {'customer': 'Carrington Lighting - North Store', 'revenue': 534.3}, {'customer': 'Litemode Limited', 'revenue': 504.9}, {'customer': 'C.E Tang Yuk & Co. Ltd', 'revenue': 486.2}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 468.14}, {'customer': 'Multi Luminaire Lévis', 'revenue': 468.13}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 448.8}, {'customer': 'Dhillon Lighting - Calgary', 'revenue': 369.9}, {'customer': 'The Lighting Shoppe - London', 'revenue': 277.43}, {'customer': 'Sparkle Light', 'revenue': 239.36}, {'customer': 'Paradise Lighting - Burlington', 'revenue': 205.5}] | [{'item': '206939A', 'desc': 'Grazia - LED Convertible Pendant Light / Luminaire suspendu convertible DEL', 'available': 15}, {'item': '207774A', 'desc': 'Grazia - LED Chandelier / Lustre DEL', 'available': 15}, {'item': '207775A', 'desc': 'Grazia - LED Linear Chandelier / Lustre linéair DEL', 'available': 8}] |
| 205131A | Troy 3 - 1L Pendant Light / Luminaire suspendu 1L | COL809 | 10,552.56 | 299 | — | — | [{'customer': 'Richardson Lighting - Regina', 'revenue': 3214.4}, {'customer': 'Eecol Electric Corp - Saskatoon', 'revenue': 2570.4}, {'customer': 'Eurolite', 'revenue': 1927.8}, {'customer': 'Multi Luminaire Lévis', 'revenue': 999.6}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 806.4}, {'customer': '0797222 BC LTD DBA Elumea Lighting Co', 'revenue': 378.0}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 302.4}, {'customer': 'Electrical & Plumbing - Gloucester', 'revenue': 142.8}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 129.36}, {'customer': 'The Lighting Shoppe - London', 'revenue': 47.8}, {'customer': 'Luminaire Galarneau', 'revenue': 33.6}] | [{'item': '85979A', 'desc': 'Troy 3 - 1L Wall Light / Murale 1L', 'available': 82}, {'item': '85978A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 37}, {'item': '205132A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 24}, {'item': '85981A', 'desc': 'Troy 3 - 1L Table Lamp / Lampe de table 1L', 'available': 3}] |
| 85977A | Troy 3 - 1L Pendant Light / Luminaire suspendu 1L | COL809 | 10,438.96 | 502 | — | — | [{'customer': 'Multi Luminaire Gatineau', 'revenue': 6487.74}, {'customer': 'Luminaires & Cie Inc', 'revenue': 614.4}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 604.8}, {'customer': 'Lumen - Laval', 'revenue': 542.72}, {'customer': 'Luminaires Repentigny', 'revenue': 512.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 358.4}, {'customer': 'Multi Luminaire Lévis', 'revenue': 353.6}, {'customer': 'Unique Lighting', 'revenue': 345.6}, {'customer': 'Multi Luminaire Laval', 'revenue': 244.8}, {'customer': 'Multi Luminaire Granby', 'revenue': 81.6}, {'customer': 'Super Lite Lighting', 'revenue': 81.6}, {'customer': 'Sparkle Light', 'revenue': 51.2}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 51.2}, {'customer': 'Corlite Distributors Inc.', 'revenue': 33.6}, {'customer': 'Eclairage Raymond inc', 'revenue': 25.6}, {'customer': 'City Lightz - St Catharines', 'revenue': 25.6}, {'customer': 'The Lighting Gallery', 'revenue': 24.5}] | [{'item': '85979A', 'desc': 'Troy 3 - 1L Wall Light / Murale 1L', 'available': 82}, {'item': '85978A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 37}, {'item': '205132A', 'desc': 'Troy 3 - 3L Pendant Light / Luminaire suspendu 3L', 'available': 24}, {'item': '85981A', 'desc': 'Troy 3 - 1L Table Lamp / Lampe de table 1L', 'available': 3}] |
| 390342A | Dracera - 10L Linear LED Pendant / Luminaire suspendu DEL linéaire 10L | COL37 | 10,409.12 | 21 | — | — | [{'customer': 'Multi Luminaire Laval', 'revenue': 3905.92}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 2453.4}, {'customer': 'Eclairage Union Montreal - DROP SHIP', 'revenue': 661.2}, {'customer': 'Alberta Lighting & Décor', 'revenue': 646.2}, {'customer': 'Union Lighting & Furnishings', 'revenue': 610.3}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 574.4}, {'customer': 'Luminaires & Cie Inc', 'revenue': 574.4}, {'customer': 'Deco Luminaire - Brossard', 'revenue': 574.4}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 408.9}] | [{'item': '390411A', 'desc': 'Dracera - 7L LED Ceiling Light / Plafonnier 7L DEL', 'available': 18}, {'item': '205804A', 'desc': 'Dracera - 10L LED Ceiling Light / Plafonnier DEL 10L', 'available': 6}, {'item': '390343A', 'desc': 'Dracera - 17L LED Pendant Light / Luminaire suspendu DEL 17L', 'available': 5}, {'item': '390339A', 'desc': 'Dracera - 10L Round LED Pendant / Luminaire suspendu DEL rond 10L', 'available': 2}] |
| 200146A | Ascoli - 1L Exterior Wall Light / Murale extérieure 1L | COL192 | 10,250.50 | 251 | — | — | [{'customer': 'Eclairage Raymond inc', 'revenue': 7800.0}, {'customer': 'Corlite Distributors Inc.', 'revenue': 1320.0}, {'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 660.0}, {'customer': 'Avaled Corp', 'revenue': 343.0}, {'customer': 'Multi Luminaire Granby', 'revenue': 127.5}] | [{'item': '200022A', 'desc': 'Ascoli - 1L Exterior Wall Light / Murale extérieure 1L', 'available': 101}, {'item': '200147A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 96}, {'item': '200023A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 80}, {'item': '200029A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 24}, {'item': '90119A', 'desc': 'Ascoli - 1L Exterior Wall Light / Murale extérieure 1L', 'available': 16}, {'item': '90121A', 'desc': 'Ascoli - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 13}] |
| 200032A | Riga - 1L Exterior Wall Light / Murale extérieure 1L | RIGA | 9,219.60 | 362 | — | — | [{'customer': 'Éclairage M&M', 'revenue': 4524.0}, {'customer': 'Espace Lumi Decor Inc', 'revenue': 2262.0}, {'customer': 'Deco Luminaire - Québec', 'revenue': 962.0}, {'customer': 'CDE - Laval', 'revenue': 847.6}, {'customer': 'Georgian Design Centre', 'revenue': 260.0}, {'customer': 'Eclairage Raymond inc', 'revenue': 182.0}, {'customer': 'Luminaires Paul Gregoire inc', 'revenue': 78.0}, {'customer': 'Eclairage Moderne Saran', 'revenue': 52.0}, {'customer': 'Luminaires & Cie Inc', 'revenue': 52.0}] | [{'item': '200033A', 'desc': 'Riga - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 490}, {'item': '84002A', 'desc': 'Riga - 2L Exterior Wall Light / Murale extérieure 2L', 'available': 4}] |
| 390465A | Fruitera - 3L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 3L | COL300 | 7,631.44 | 29 | — | — | [{'customer': 'Paradise Lighting - Burlington', 'revenue': 1096.2}, {'customer': 'Park Lighting', 'revenue': 1058.4}, {'customer': 'Vancouver Lighting - Richmond', 'revenue': 982.8}, {'customer': 'The Lighting Warehouse', 'revenue': 850.5}, {'customer': 'Cartwright Lighting', 'revenue': 529.2}, {'customer': 'Royal Lighting', 'revenue': 491.4}, {'customer': 'Multi Luminaire Granby', 'revenue': 472.31}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 472.31}, {'customer': 'Lumisolution Inc.', 'revenue': 396.9}, {'customer': 'Carrington Lighting - North Store', 'revenue': 321.3}, {'customer': 'Luminaires & Cie Inc', 'revenue': 302.4}, {'customer': 'Multi Luminaire Laval', 'revenue': 257.04}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 211.68}, {'customer': 'Paradise Lighting/ MaxTraders Inc', 'revenue': 189.0}] | [{'item': '390463A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 15}, {'item': '390467A', 'desc': 'Fruitera - 1L 3CCT LED Table Lamp / Lampe de table DEL 3CCT 1L', 'available': 13}, {'item': '390464A', 'desc': 'Fruitera - 1L 3CCT LED Pendant Light / Luminaire suspendu DEL 3CCT 1L', 'available': 12}] |
| 94187A | Tarbes - 1L Pendant Light / Luminaire suspendu 1L | COL790 | 7,267.33 | 220 | — | — | [{'customer': 'CDE - Laval', 'revenue': 3999.0}, {'customer': 'Multi Luminaire Lévis', 'revenue': 1193.4}, {'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 614.25}, {'customer': 'Deco Luminaire - Québec', 'revenue': 252.0}, {'customer': 'Luminaires & Cie Inc', 'revenue': 216.0}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 209.23}, {'customer': 'Lumen - Laval', 'revenue': 189.0}, {'customer': 'Richardson Lighting - Saskatoon', 'revenue': 162.0}, {'customer': 'Lite It Up By Design Inc. - INACTIVE', 'revenue': 137.7}, {'customer': 'Unique Lighting', 'revenue': 121.5}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 108.0}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 34.65}, {'customer': 'Multi Luminaire Granby', 'revenue': 30.6}] | [{'item': '94188A', 'desc': 'Tarbes - 1L Pendant Light / Luminaire suspendu 1L', 'available': 74}, {'item': '94189A', 'desc': 'Tarbes - 3L Pendant Light / Luminaire suspendu 3L', 'available': 53}, {'item': '43004A', 'desc': 'Tarbes - 1L Ceiling Light / Plafonnier 1L', 'available': 21}, {'item': '94191A', 'desc': 'Tarbes - 3L Pendant Light / Luminaire suspendu 3L', 'available': 15}] |
| 202343A | Fondachelli - 1L Floor Lamp / Lampe de plancher 1L | COL271 | 6,840 | 171 | — | — | [{'customer': 'Winners Merchants International LP', 'revenue': 6840.0}] | — |
| 205293A | Rafaelino - 1L Pendant Light / Luminaire suspendu 1L | COL751 | 6,777.66 | 68 | — | — | [{'customer': 'Alberta Lighting & Décor', 'revenue': 2534.4}, {'customer': 'Sparkle Light', 'revenue': 950.4}, {'customer': 'Multi Luminaire Granby', 'revenue': 538.56}, {'customer': 'Multi Luminaire Gatineau', 'revenue': 526.21}, {'customer': 'Wesco Distribution - Toronto', 'revenue': 462.0}, {'customer': 'Park Lighting', 'revenue': 369.6}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 254.69}, {'customer': 'Luminaire Galarneau', 'revenue': 253.44}, {'customer': 'Living Lighting #8 Napean', 'revenue': 224.4}, {'customer': 'Luminaires & Cie Inc', 'revenue': 211.2}, {'customer': 'Multi Luminaire Lévis', 'revenue': 179.52}, {'customer': 'Dhillon Lighting - Calgary', 'revenue': 171.6}, {'customer': 'Royaume Luminaire - Drummond', 'revenue': 101.64}] | [{'item': '206244A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 192}, {'item': '206243A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 162}, {'item': '205291A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 147}, {'item': '204324A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 107}, {'item': '205295A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 59}, {'item': '204325A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 28}, {'item': '206242A', 'desc': 'Rafaelino - 1L Pendant Light / Luminaire suspendu 1L', 'available': 12}] |
| 207407A | Como - 1L Convertible Pendant Light / Luminaire suspendu convertible 1L | COMO | 6,762.66 | 40 | — | — | [{'customer': 'Mclaren Lighting - Victoria', 'revenue': 4443.75}, {'customer': 'Super Lite Lighting', 'revenue': 1007.25}, {'customer': 'Union Lighting & Furnishings', 'revenue': 400.53}, {'customer': 'Living Lighting #8 Napean', 'revenue': 319.81}, {'customer': 'CDE - Laval', 'revenue': 189.6}, {'customer': 'Park Lighting', 'revenue': 150.5}, {'customer': 'Concept Luminaire M.B inc', 'revenue': 132.72}, {'customer': 'Dhillon Lighting - Edmonton', 'revenue': 118.5}] | — |
| 92719A | Coretto - 1L Pendant Light / Luminaire suspendu 1L | COL247 | 6,687.59 | 109 | — | — | [{'customer': 'Agence For-Trem', 'revenue': None}, {'customer': 'Carrington Lighting - North Store', 'revenue': 4446.0}, {'customer': 'Multi Luminaire Granby', 'revenue': 2008.84}, {'customer': 'Dubo Electrique ltee - Montréal', 'revenue': 99.75}, {'customer': 'Deco Luminaire - Québec', 'revenue': 76.0}, {'customer': 'Park Lighting', 'revenue': 57.0}] | [{'item': '92716A', 'desc': 'Coretto - 1L Pendant Light / Luminaire suspendu 1L', 'available': 16}] |
| 206423A | Rondo - 1L Pendant Light / Luminaire suspendu 1L | COL765 | 6,412.84 | 206 | — | — | [{'customer': 'Royaume Luminaire - Sherbrooke', 'revenue': 2732.73}, {'customer': 'Royaume Luminaire - Beauport', 'revenue': 564.57}, {'customer': 'SaveMore Plumbing & Heating', 'revenue': 555.77}, {'customer': 'Luminaire P.M. Lemire', 'revenue': 533.05}, {'customer': 'Multi Luminaire Laval', 'revenue': 430.95}, {'customer': 'Royaume Luminaire - Terrebonne', 'revenue': 312.28}, {'customer': 'Luminaire Galarneau', 'revenue': 249.6}, {'customer': 'Royaume Luminaire - Tr.Rivieres', 'revenue': 240.24}, {'customer': 'Vancouver Lighting - Richmond', 'revenue': 187.2}, {'customer': 'Eclairage Quebec Corporation', 'revenue': 156.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 124.8}, {'customer': 'Luminaire Alder inc', 'revenue': 124.8}, {'customer': 'Multi Luminaire Granby', 'revenue': 99.45}, {'customer': 'The Lighting Shoppe - London', 'revenue': 70.2}, {'customer': 'Deco Luminaire - Québec', 'revenue': 31.2}] | [{'item': '206424A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 73}, {'item': '206421A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 61}, {'item': '206425A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 42}, {'item': '206432A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 34}, {'item': '206422A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 24}, {'item': '206428A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 18}, {'item': '206431A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 17}, {'item': '206429A', 'desc': 'Rondo - 1L Pendant Light / Luminaire suspendu 1L', 'available': 13}, {'item': '85264A', 'desc': 'Rondo - 1L Table Lamp / Lampe de table 1L', 'available': 12}, {'item': '204565A', 'desc': 'Rondo - 1L Table Lamp / Lampe de table 1L', 'available': 9}, {'item': '85265A', 'desc': 'Rondo - 1L Table Lamp / Lampe de table 1L', 'available': 8}] |
