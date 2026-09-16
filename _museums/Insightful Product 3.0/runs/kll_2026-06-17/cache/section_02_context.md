# Section 2 Context Bundle — Kuzco Lighting Inc. (kll)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Kuzco Lighting Inc. (kll, org_id=166)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=118487, portal_order_gmv=$90.5M |
| HAS_INVENTORY | True | inventory_count=6376 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=4 engagement_reps=72 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | kuzco_kll_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$90.5M > ecat_gmv=$922,177: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 4 | 4 |
| ENGAGEMENT_REP_COUNT | 72 | engagement_reps=72 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 118 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 300, Mixpanel total submit_order (Q-01): 258 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=66.1%, ambiguous_rate=0.0%, showroom_event_share=13.9% |
| USER_GROUP_JOIN_RATE | 66% | 78 of 118 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 14% | showroom+admin share of matched events: 13.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Katy TIPTON, Kuzco Showroom |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2373 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=556 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Kuzco Lighting Inc.
- **Shortname**: kll
- **Org ID**: 166
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Kuzco Lighting Inc. (kll, org_id=166)
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
| HAS_SALES_DATA | False |
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

# Signal Rank — Kuzco Lighting Inc. (kll, org_id=166)
- **Run date**: 2026-06-17
- **Total signals fired**: 47 (P0: 33, P1: 13, P2: 1)
- **Org GMV**: $0.9M eCat LTM, $90.5M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $25.7M+ total business, zero eCat orders | P1 | §2 Accounts | 25.7 | $25,690,379 | 2.0 | 1,319,991,146 | POSITIVE |
| 2 | SIG-MOM-01 | Account Acceleration — KUZCO LIGHTING LLC. 2 consecutive QoQ acceleration quarters, $534,486 peak quarter (+344% QoQ) | P0 | §2 Accounts | 11.5 | $534,486 | 3.0 | 18,364,947 | POSITIVE |
| 3 | SIG-ANOMALY-03 | Competitive Displacement — ECLAIRAGE UNION MONTREAL total biz +242% but eCat -100% | P0 | §2 Accounts | 22.8 | $244,995 | 3.0 | 16,742,991 | RISK |
| 4 | SIG-MOM-01 | Account Acceleration — CED MILPITAS- SAN FRANCISCO 2 consecutive QoQ acceleration quarters, $147,978 peak quarter (+922% QoQ) | P0 | §2 Accounts | 30.7 | $147,978 | 3.0 | 13,642,092 | POSITIVE |
| 5 | SIG-COMMERCE-01 | Capture Rate — eCat captures 1.0% of $90M total business; each +1pt = $905K | P0 | §4 Commerce | 4.9 | $905,000 | 3.0 | 13,436,673 | POSITIVE |
| 6 | SIG-ANOMALY-03 | Competitive Displacement — WOLSELEY CALGARY total biz +504% but eCat -100% | P0 | §2 Accounts | 40.3 | $106,230 | 3.0 | 12,836,887 | RISK |
| 7 | SIG-MOM-01 | Account Acceleration — KUZCO LIGHTING INC. 2 consecutive QoQ acceleration quarters, $184,058 peak quarter (+594% QoQ) | P0 | §2 Accounts | 19.8 | $184,058 | 3.0 | 10,933,073 | POSITIVE |
| 8 | SIG-MOM-01 | Account Acceleration — CITY LIGHTS LIGHTING SHOWROOM 2 consecutive QoQ acceleration quarters, $325,136 peak quarter (+276% QoQ) | P0 | §2 Accounts | 9.2 | $325,136 | 3.0 | 8,980,243 | POSITIVE |
| 9 | SIG-ANOMALY-03 | Competitive Displacement — BIRD STAIRS total biz +624% but eCat -100% | P0 | §2 Accounts | 48.3 | $53,142 | 3.0 | 7,694,904 | RISK |
| 10 | SIG-MOM-01 | Account Acceleration — SOUTH DADE LIGHTING 2 consecutive QoQ acceleration quarters, $226,013 peak quarter (+333% QoQ) | P0 | §2 Accounts | 11.1 | $226,013 | 3.0 | 7,519,461 | POSITIVE |
| 11 | SIG-MOM-01 | Account Acceleration — US ELECTRICAL SERVICES INC 2 consecutive QoQ acceleration quarters, $248,078 peak quarter (+197% QoQ) | P0 | §2 Accounts | 6.6 | $248,078 | 3.0 | 4,889,623 | POSITIVE |
| 12 | SIG-ANOMALY-03 | Competitive Displacement — DECO LUMINAIRE QUEBEC total biz +151% but eCat -74% | P0 | §2 Accounts | 15.0 | $79,744 | 3.0 | 3,594,872 | RISK |
| 13 | SIG-ANOMALY-03 | Competitive Displacement — M & M LIGHTING total biz +280% but eCat -100% | P0 | §2 Accounts | 25.3 | $34,720 | 3.0 | 2,640,098 | RISK |
| 14 | SIG-MOM-01 | Account Acceleration — VIKING ELECTRIC SUPPLY 2 consecutive QoQ acceleration quarters, $130,089 peak quarter (+160% QoQ) | P0 | §2 Accounts | 5.3 | $130,089 | 3.0 | 2,081,424 | POSITIVE |
| 15 | SIG-ANOMALY-03 | Competitive Displacement — LIGHTING DESIGN COMPANY total biz +168% but eCat -29% | P0 | §2 Accounts | 13.1 | $52,035 | 3.0 | 2,042,902 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — GRAYBAR ELECTRIC - NOGA 2 consecutive QoQ acceleration quarters, $313,471 peak quarter (+50% QoQ) | P0 | §2 Accounts | 1.7 | $313,471 | 3.0 | 1,579,892 | POSITIVE |
| 17 | SIG-DECAY-04 | Spending Contraction — FLUX LIGHTING -46.5% YoY ($390,259→$208,941), $181,319 gap | P0 | §2 Accounts | 2.3 | $181,319 | 3.0 | 1,264,697 | RISK |
| 18 | SIG-MOM-01 | Account Acceleration — NUVO SALES 3 consecutive QoQ acceleration quarters, $230,264 peak quarter (+55% QoQ) | P0 | §2 Accounts | 1.8 | $230,264 | 3.0 | 1,257,239 | POSITIVE |
| 19 | SIG-ANOMALY-03 | Competitive Displacement — PINE LIGHTING total biz +40% but eCat -100% | P0 | §2 Accounts | 9.3 | $39,598 | 3.0 | 1,109,532 | RISK |
| 20 | SIG-ANOMALY-03 | Competitive Displacement — DHILLON LIGHTING CALGARY total biz +115% but eCat -100% | P0 | §2 Accounts | 14.3 | $23,831 | 3.0 | 1,024,716 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 32 | 1 | 0 | 33 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 1 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $25.7M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — KUZCO LIGHTING LLC. 2 consecutive QoQ acceleration quarters, $534,486 peak quarter (+344% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — CED MILPITAS- SAN FRANCISCO 2 consecutive QoQ acceleration quarters, $147,978 peak quarter (+922% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 1.0% of $90M total business; each +1pt = $905K
5. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — ECLAIRAGE UNION MONTREAL total biz +242% but eCat -100%
6. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — WOLSELEY CALGARY total biz +504% but eCat -100%
7. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — BIRD STAIRS total biz +624% but eCat -100%

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Kuzco Lighting Inc. (kll, org_id=166)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | FLUX LIGHTING | 1 | DECAY-04 | $181,319 |
| 2 | SUPREME LIGHTING AND ELEC SUPPLIES | 1 | DECAY-04 | $70,292 |
| 3 | REXEL | 1 | DECAY-04 | $69,296 |
| 4 | KENDALL ELECTRIC INC. | 1 | DECAY-04 | $59,532 |
| 5 | BA ROBINSON CO LTD | 1 | ANOMALY-03 | $26,114 |
| 6 | ROBINSON LIGHTING LTD | 1 | ANOMALY-03 | $18,797 |
| 7 | DHILLON LIGHTING CALGARY | 1 | ANOMALY-03 | $23,831 |
| 8 | ECLAIRAGE UNION MONTREAL | 1 | ANOMALY-03 | $244,995 |
| 9 | MCLAREN LIGHTING | 1 | ANOMALY-03 | $17,077 |
| 10 | MONTREAL LIGHTING AND HARDWARE | 1 | ANOMALY-03 | $14,438 |

### Q-12_results.md

# Q-12 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 2,837 | 445 | 200 | 130 | 56 |

### Q-14_results.md

# Q-14 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 17
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| LLC-T00000694 | NAOMI PRATT DESIGN | 6 | $5,350 | 2026-01-13 21:04:53 | 2026-05-05 14:56:58 | 22.30 |
| INC-K0000068 | MULTI LUMINAIRE LAVAL | 5 | $7,403 | 2026-01-11 16:03:04 | 2026-02-06 18:37:06 | 6.50 |
| LLC-USACST319 | ITHACA LIGHTS DBA KORNERLOT DESIGN AND DEVELOPMENT LLC | 4 | $5,680 | 2025-07-31 15:12:20 | 2026-01-14 20:22:45 | 55.70 |
| LLC-K0002037 | ANZALONE ELECTRIC INC | 4 | $5,072 | 2025-09-10 17:07:26 | 2026-01-15 15:47:25 | 42.30 |
| LLC-K0002287 | WAGE LIGHTING AND DESIGN | 4 | $13,077 | 2025-12-11 20:44:04 | 2026-03-05 18:55:38 | 28 |
| LLC-K0002762 | KUZCO LIGHTING LLC - VEGAS | 4 | $33,688 | 2025-08-06 21:12:04 | 2026-01-10 19:58:50 | 52.30 |
| LLC-T00000186 | CRANDALL HAUS DBA QUEEN CITY DESIGN | 4 | $2,525 | 2026-03-12 19:56:13 | 2026-05-14 17:34:59 | 21 |
| LLC-T00000744 | ANDERSON DESIGN STUDIO | 4 | $4,288 | 2026-02-10 18:54:10 | 2026-03-19 20:47:59 | 12.40 |
| LLC-T00000817 | JAN ROBINSON INTERIORS | 4 | $980 | 2025-12-09 21:53:06 | 2026-06-17 18:28:40 | 63.30 |
| LLC-00000742 | HUE AND HEM | 3 | $5,636 | 2025-07-17 19:55:25 | 2025-08-15 21:48:16 | 14.50 |
| LLC-USACST257 | WATTSAVER LIGHTING PRODUCTS INC | 3 | $4,630 | 2025-09-11 18:44:06 | 2026-04-02 18:42:51 | 101.50 |
| LLC-00000796 | PLANET DESIGN HOME | 3 | $10,010 | 2025-08-18 21:06:18 | 2025-08-20 21:03:19 | 1 |
| LLC-00000694 | NAOMI PRATT DESIGN | 3 | $1,161 | 2025-08-21 02:06:52 | 2025-11-19 01:58:04 | 45 |
| LLC-T00001084 | INTERIOR DESIGN STUDIO | 3 | $1,688 | 2026-01-20 19:56:51 | 2026-06-11 18:39:58 | 71 |
| LLC-T00001162 | L DESIGN AND PRODUCTION LLC | 3 | $76,172 | 2026-01-06 02:57:10 | 2026-01-12 20:37:13 | 3.40 |
| LLC-T00001302 | SPK LIGHTING | 3 | $2,262 | 2026-04-02 21:05:39 | 2026-05-16 19:11:38 | 22 |
| LLC-T00000339 | TRISTAN GARY DESIGNS | 3 | $1,240 | 2026-01-02 20:46:33 | 2026-03-05 18:57:03 | 31 |

### Q-14b_results.md

# Q-14b Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| LLC-K0001648 | FACILITY SOLUTIONS GROUP-NY | 40 | 11 | 17.40 | 1.58 | $313,701 |
| LLC-T00000702 | LIGHTS.COM | 718 | 0.50 | 0.90 | 1.80 | $209,302 |
| LLC-K0002013 | HEIN ELECTRIC SUPPLY CO | 73 | 6.20 | 9.80 | 1.58 | $172,863 |
| INC-K0000330 | MERCURY LIGHTING LIMITED | 23 | 16.70 | 29.60 | 1.77 | $154,046 |
| INC-K0000133 | MULTI LUMINAIRE OTTAWA(DO NOT USE) | 128 | 3.20 | 8.30 | 2.59 | $136,725 |
| INC-T00000068 | Elumea Lighting Co | 53 | 4.80 | 7.30 | 1.52 | $115,011 |
| LLC-K0000315 | REXEL | 97 | 3.80 | 12.10 | 3.18 | $107,488 |
| LLC-K0004374 | LAPPIN ELECTRIC-WAUKESHA | 36 | 12.50 | 20 | 1.60 | $106,984 |
| LLC-K0002448 | LIGHTING INSTYLE (MONTCLAIR) | 172 | 2.50 | 4.80 | 1.92 | $97,587 |
| INC-K0001245 | LUMINAIRE EXPERT | 76 | 6 | 9.30 | 1.55 | $91,677 |
| INC-CANCST44 | GERRIE ELECTRIC BURLINGTON | 51 | 8.60 | 14.80 | 1.72 | $83,882 |
| LLC-T00000021 | THE JARRELL COMPANY | 113 | 3.50 | 7.90 | 2.26 | $80,882 |
| LLC-K0004176 | PEPCO/DBA ECHO ELETRIC | 19 | 15.10 | 51.80 | 3.43 | $74,901 |
| INC-T00000048 | Ideoli Group INC | 17 | 20.70 | 48.80 | 2.36 | $69,505 |
| INC-K0000028 | DUBO ELECTRIQUE LTEE | 105 | 4 | 8.80 | 2.20 | $66,281 |

### Q-17_results.md

# Q-17 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| LLC-T00001162 | L DESIGN AND PRODUCTION LLC | NJ | 2026-01-12 20:37:13 | 3 | $76,172 |
| LLC-K0004903 | SHADES OF LIGHT LLC | VA | 2025-06-18 20:14:42 | 1 | $69,624 |
| INC-K0000074 | NUVO SALES | BC | 2025-06-20 18:21:28 | 2 | $43,341 |
| INC-K0000089 | ROYAUME LUMINAIRE TROISRIVIERES | QC | 2026-01-12 21:54:20 | 2 | $36,110 |
| LLC-K0002762 | KUZCO LIGHTING LLC - VEGAS | NV | 2026-01-10 19:58:50 | 4 | $33,688 |
| LLC-K0004469 | C.E. TANG YUK CO. LTD | TT | 2026-01-11 18:15:09 | 1 | $31,614 |
| LLC-K0002065 | LIGHTING DESIGN COMPANY | UT | 2026-01-12 22:59:56 | 1 | $18,924 |
| INC-K0000081 | ROYAUME DRUMMONDVILLE | QC | 2026-01-15 13:56:05 | 2 | $16,769 |
| LLC-K0002564 | LAMP DESIGNS | PR | 2025-06-19 16:34:29 | 1 | $16,059 |
| LLC-K0002287 | WAGE LIGHTING AND DESIGN | PA | 2026-03-05 18:55:38 | 4 | $13,077 |
| INC-K0000097 | SIGNATURE LIGHTING AND FANS | AB | 2026-01-10 23:34:08 | 2 | $13,058 |
| LLC-K0002586 | KITCHEN BY DESIGN | IA | 2026-01-11 23:30:31 | 2 | $12,568 |
| LLC-K0002100 | XSS HOTELS | NH | 2026-02-05 15:34:03 | 1 | $11,970 |
| LLC-K0004445 | STUDIO WEST | CO | 2026-01-10 22:51:44 | 1 | $11,935 |
| LLC-T00001131 | WELLS DESIGN STUDIO | CO | 2026-01-23 20:37:34 | 1 | $11,443 |
| INC-K0000414 | DECO LUMINAIRE BROSSARD | QC | 2026-01-10 22:50:02 | 2 | $11,274 |
| INC-K0000016 | CARRINGTON LIGHTING | AB | 2025-06-20 15:51:51 | 1 | $11,265 |
| INC-K0000085 | ROYAUME LUMINAIRE TERREBONNE | QC | 2026-01-12 21:47:23 | 1 | $11,017 |
| LLC-K0004171 | GW LIGHTING & HOME DECOR | AR | 2026-01-13 15:39:08 | 2 | $10,669 |
| LLC-K0003728 | ELAN STUDIO LIGHTING | LA | 2026-01-11 18:41:54 | 1 | $9,650 |
| INC-K0001191 | DECO LUMINAIRE QUEBEC | QC | 2026-01-10 22:45:17 | 1 | $9,053 |
| LLC-USACST63 | GEORGIA LIGHTING (COLONIAL LIGHTING LLC) | GA | 2025-06-23 16:04:52 | 1 | $8,468 |
| LLC-K0004777 | PINE GROVE LIGHTING & ELECTRICAL SUPPLY | LA | 2026-01-10 14:29:35 | 1 | $8,126 |
| LLC-K0001209 | IMAGINE MORE LLC | CO | 2025-06-19 14:39:10 | 1 | $8,069 |
| INC-K0000068 | MULTI LUMINAIRE LAVAL | QC | 2026-02-06 18:37:06 | 5 | $7,403 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| LLC-T00001162 | L DESIGN AND PRODUCTION LLC | NJ | $76,172 | 2026-01-12 20:37:13 | 155 |
| LLC-K0004903 | SHADES OF LIGHT LLC | VA | $69,624 | 2025-06-18 20:14:42 | 364 |
| INC-K0000074 | NUVO SALES | BC | $43,341 | 2025-06-20 18:21:28 | 362 |
| INC-K0000089 | ROYAUME LUMINAIRE TROISRIVIERES | QC | $36,110 | 2026-01-12 21:54:20 | 155 |
| LLC-K0002762 | KUZCO LIGHTING LLC - VEGAS | NV | $33,688 | 2026-01-10 19:58:50 | 158 |
| LLC-K0004469 | C.E. TANG YUK CO. LTD | TT | $31,614 | 2026-01-11 18:15:09 | 157 |
| LLC-K0002065 | LIGHTING DESIGN COMPANY | UT | $18,924 | 2026-01-12 22:59:56 | 155 |
| LLC-T00000530 | BD INTERIORS AKA BARRETT DESIGN INC | CO | $16,877 | 2026-03-19 19:58:10 | 90 |
| INC-K0000081 | ROYAUME DRUMMONDVILLE | QC | $16,769 | 2026-01-15 13:56:05 | 153 |
| LLC-K0002564 | LAMP DESIGNS | PR | $16,059 | 2025-06-19 16:34:29 | 363 |
| LLC-K0002287 | WAGE LIGHTING AND DESIGN | PA | $13,077 | 2026-03-05 18:55:38 | 104 |
| INC-K0000097 | SIGNATURE LIGHTING AND FANS | AB | $13,058 | 2026-01-10 23:34:08 | 157 |
| LLC-K0002586 | KITCHEN BY DESIGN | IA | $12,568 | 2026-01-11 23:30:31 | 156 |
| LLC-K0002100 | XSS HOTELS | NH | $11,970 | 2026-02-05 15:34:03 | 132 |
| LLC-K0004445 | STUDIO WEST | CO | $11,935 | 2026-01-10 22:51:44 | 157 |
| LLC-T00001131 | WELLS DESIGN STUDIO | CO | $11,443 | 2026-01-23 20:37:34 | 144 |
| INC-K0000414 | DECO LUMINAIRE BROSSARD | QC | $11,274 | 2026-01-10 22:50:02 | 157 |
| INC-K0000016 | CARRINGTON LIGHTING | AB | $11,265 | 2025-06-20 15:51:51 | 362 |
| INC-K0000085 | ROYAUME LUMINAIRE TERREBONNE | QC | $11,017 | 2026-01-12 21:47:23 | 155 |
| LLC-K0004171 | GW LIGHTING & HOME DECOR | AR | $10,669 | 2026-01-13 15:39:08 | 155 |

### Q-40_results.md

# Q-40 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| QC | 16 | 24 | $121,875 |
| NJ | 2 | 4 | $76,373 |
| VA | 3 | 3 | $70,876 |
| CO | 4 | 4 | $48,324 |
| BC | 1 | 2 | $43,341 |
| CA | 14 | 18 | $43,069 |
| NV | 2 | 5 | $36,376 |
| TT | 1 | 1 | $31,614 |
| AB | 2 | 3 | $24,323 |
| LA | 4 | 4 | $23,758 |
| PR | 2 | 2 | $22,225 |
| PA | 6 | 11 | $21,574 |
| UT | 3 | 5 | $21,468 |
| TX | 9 | 11 | $21,357 |
| CT | 6 | 8 | $15,204 |
| NY | 7 | 14 | $15,110 |
| IA | 3 | 5 | $12,951 |
| NH | 1 | 1 | $11,970 |
| FL | 9 | 10 | $11,670 |
| GA | 2 | 3 | $10,694 |

### Q-41_results.md

# Q-41 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 28
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 1 |
| 2025-03-01 | eCat Online-Acquired (self-serve) | 2 |
| 2025-04-01 | Rep-Acquired (iPad) | 2 |
| 2025-05-01 | Rep-Acquired (iPad) | 1 |
| 2025-05-01 | eCat Online-Acquired (self-serve) | 5 |
| 2025-06-01 | Rep-Acquired (iPad) | 11 |
| 2025-06-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-07-01 | Rep-Acquired (iPad) | 2 |
| 2025-07-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-08-01 | Rep-Acquired (iPad) | 3 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 3 |
| 2025-09-01 | Rep-Acquired (iPad) | 4 |
| 2025-09-01 | eCat Online-Acquired (self-serve) | 13 |
| 2025-10-01 | eCat Online-Acquired (self-serve) | 16 |
| 2025-11-01 | Rep-Acquired (iPad) | 2 |
| 2025-11-01 | eCat Online-Acquired (self-serve) | 8 |
| 2025-12-01 | Rep-Acquired (iPad) | 2 |
| 2025-12-01 | eCat Online-Acquired (self-serve) | 8 |
| 2026-01-01 | Rep-Acquired (iPad) | 8 |
| 2026-01-01 | eCat Online-Acquired (self-serve) | 16 |
| 2026-02-01 | Rep-Acquired (iPad) | 3 |
| 2026-02-01 | eCat Online-Acquired (self-serve) | 8 |
| 2026-03-01 | Rep-Acquired (iPad) | 1 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 16 |
| 2026-04-01 | Rep-Acquired (iPad) | 1 |
| 2026-04-01 | eCat Online-Acquired (self-serve) | 12 |
| 2026-05-01 | eCat Online-Acquired (self-serve) | 14 |
| 2026-06-01 | eCat Online-Acquired (self-serve) | 7 |

### Q-41_rep_results.md

# Q-41-rep Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Katy TIPTON | 11 |
| Kuzco Showroom | 5 |
| Lisa Belesky | 5 |
| Callie Curtis | 3 |
| Chas Lassoff | 2 |
| Ken Grillo | 2 |
| Jenifer McCarty | 2 |
| Corinne Noreyko | 2 |
| Jason Burns | 2 |
| Mike Hemsarth | 1 |
| Customer Support | 1 |
| Gary Raileanu | 1 |
| Grillo Customer Service | 1 |
| Kevin Blackley | 1 |
| Kevin Gannon | 1 |
| Brittney Hayes | 1 |

### Q-52_results.md

# Q-52 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LLC-K0001921 | LUMENS LIGHT & LIVING | California | 11,761 | $3.9M | 0 | $0 | 0 |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | Virginia | 3,410 | $3.6M | 0 | $0 | 0 |
| LLC-USACST245 | WAYFAIR LLC DBA JOSS AND MAIN | Massachusetts | 14,987 | $3.1M | 0 | $0 | 0 |
| LLC-USACST97 | BUILD.COM INC | California | 7,134 | $2.4M | 0 | $0 | 0 |
| LLC-K0002236 | LIGHTOLOGY LLC | Illinois | 3,176 | $1.6M | 0 | $0 | 0 |
| INC-K0000011 | BA ROBINSON CO LTD | Manitoba | 579 | $1.3M | 0 | $0 | 0 |
| LLC-K0004603 | LAMPS PLUS INC | California | 4,422 | $1.1M | 0 | $0 | 0 |
| LLC-K0000729 | GRAYBAR ELECTRIC - NOGA | Missouri | 349 | $1.0M | 0 | $0 | 0 |
| INC-CANCST48 | LIGHTHOUSE CABINETRY DBA 2641426 ONTARIO INC | Ontario | 3,468 | $1.0M | 0 | $0 | 0 |
| INC-K0000075 | OCEAN PACIFIC LIGHTING | British Columbia | 584 | $1.0M | 0 | $0 | 0 |
| INC-K0000138 | ROBINSON LIGHTING LTD | Manitoba | 321 | $921,069 | 0 | $0 | 0 |
| INC-K0001977 | KUZCO LIGHTING LLC. | Nevada | 65 | $863,333 | 0 | $0 | 0 |
| INC-K0002626 | DHILLON LIGHTING CALGARY | Alberta | 132 | $801,279 | 0 | $0 | 0 |
| LLC-T00000223 | THE HOME DEPOT PRODUCT AUTHORITY LLC | Georgia | 2,866 | $757,612 | 0 | $0 | 0 |
| LLC-K0001858 | DOLAN NORTHWEST LLC | Oregon | 580 | $682,172 | 0 | $0 | 0 |
| INC-K0003136 | SALEX INC | Ontario | 172 | $634,854 | 0 | $0 | 0 |
| LLC-K0004619 | US ELECTRICAL SERVICES INC | Connecticut | 111 | $630,482 | 0 | $0 | 0 |
| INC-K0000059 | LUMINAIRES AND CIE | Quebec | 251 | $624,929 | 0 | $0 | 0 |
| LLC-T00000264 | HAUS APPEAL | Massachusetts | 2,942 | $611,591 | 0 | $0 | 0 |
| LLC-K0004701 | CAPITOL LIGHTING OF EAST HANOVER | Florida | 1,639 | $606,239 | 0 | $0 | 0 |
| LLC-USACST460 | WILLIAMS SONOMA INC | Mississippi | 3,100 | $605,819 | 0 | $0 | 0 |
| LLC-K0004903 | SHADES OF LIGHT LLC | Virginia | 270 | $603,356 | 1 | $69,624 | 11.50 |
| INC-K0000074 | NUVO SALES | British Columbia | 233 | $573,325 | 2 | $43,341 | 7.60 |
| INC-K0000068 | MULTI LUMINAIRE LAVAL | Quebec | 243 | $563,549 | 5 | $7,403 | 1.30 |
| INC-K0000030 | ECLAIRAGE UNION MONTREAL | Quebec | 1,118 | $554,985 | 0 | $0 | 0 |
| LLC-K0002209 | CITY LIGHTS LIGHTING SHOWROOM | California | 578 | $554,402 | 1 | $7,067 | 1.30 |
| INC-T00000061 | WAYFAIR - INC | Massachusetts | 2,498 | $553,517 | 0 | $0 | 0 |
| LLC-K0002019 | LIGHTOPIA | California | 1,755 | $551,490 | 0 | $0 | 0 |
| LLC-K0001156 | POWER DESIGN RESOURCES | Florida | 89 | $532,568 | 0 | $0 | 0 |
| INC-K0000097 | SIGNATURE LIGHTING AND FANS | Alberta | 77 | $510,765 | 2 | $13,058 | 2.60 |

### Q-53_results.md

# Q-53 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| LLC-K0001921 | LUMENS LIGHT & LIVING | California | 11,761 | $3.9M |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | Virginia | 3,410 | $3.6M |
| LLC-USACST245 | WAYFAIR LLC DBA JOSS AND MAIN | Massachusetts | 14,987 | $3.1M |
| LLC-USACST97 | BUILD.COM INC | California | 7,134 | $2.4M |
| LLC-K0002236 | LIGHTOLOGY LLC | Illinois | 3,176 | $1.6M |
| LLC-K0004603 | LAMPS PLUS INC | California | 4,422 | $1.1M |
| LLC-K0000729 | GRAYBAR ELECTRIC - NOGA | Missouri | 349 | $1.0M |
| INC-CANCST48 | LIGHTHOUSE CABINETRY DBA 2641426 ONTARIO INC | Ontario | 3,468 | $1.0M |
| INC-K0000075 | OCEAN PACIFIC LIGHTING | British Columbia | 584 | $1.0M |
| INC-K0001977 | KUZCO LIGHTING LLC. | Nevada | 65 | $863,333 |
| LLC-T00000223 | THE HOME DEPOT PRODUCT AUTHORITY LLC | Georgia | 2,866 | $757,612 |
| LLC-K0001858 | DOLAN NORTHWEST LLC | Oregon | 580 | $682,172 |
| INC-K0003136 | SALEX INC | Ontario | 172 | $634,854 |
| LLC-K0004619 | US ELECTRICAL SERVICES INC | Connecticut | 111 | $630,482 |
| INC-K0000059 | LUMINAIRES AND CIE | Quebec | 251 | $624,929 |
| LLC-T00000264 | HAUS APPEAL | Massachusetts | 2,942 | $611,591 |
| LLC-USACST460 | WILLIAMS SONOMA INC | Mississippi | 3,100 | $605,819 |
| INC-T00000061 | WAYFAIR - INC | Massachusetts | 2,498 | $553,517 |
| LLC-K0001156 | POWER DESIGN RESOURCES | Florida | 89 | $532,568 |
| LLC-K0003081 | LIGHTING BY JARED INC | Pennsylvania | 1,192 | $493,502 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| California | 262 | 29,502 | $12.7M | 1 | 1 | $1,251 | 0 |
| Ontario | 162 | 10,538 | $8.7M | 0 | 0 | $0 | 0 |
| Quebec | 93 | 6,155 | $5.9M | 0 | 0 | $0 | 0 |
| Florida | 196 | 5,076 | $5.7M | 0 | 0 | $0 | 0 |
| British Columbia | 62 | 2,923 | $5.4M | 0 | 0 | $0 | 0 |
| Massachusetts | 42 | 21,104 | $5.2M | 0 | 0 | $0 | 0 |
| Virginia | 21 | 4,100 | $4.5M | 0 | 0 | $0 | 0 |
| Texas | 158 | 3,115 | $4.3M | 0 | 0 | $0 | 0 |
| Illinois | 71 | 4,966 | $3.6M | 0 | 0 | $0 | 0 |
| New York | 149 | 3,012 | $3.4M | 0 | 0 | $0 | 0 |
| Alberta | 31 | 1,938 | $3.1M | 0 | 0 | $0 | 0 |
| Manitoba | 11 | 1,245 | $2.6M | 0 | 0 | $0 | 0 |
| Georgia | 70 | 3,972 | $2.3M | 1 | 1 | $496 | 0 |
| Missouri | 44 | 900 | $1.8M | 0 | 0 | $0 | 0 |
| Oregon | 22 | 959 | $1.6M | 0 | 0 | $0 | 0 |
| Pennsylvania | 43 | 2,244 | $1.5M | 0 | 0 | $0 | 0 |
| Nevada | 20 | 1,133 | $1.3M | 0 | 0 | $0 | 0 |
| Connecticut | 28 | 492 | $1.2M | 1 | 2 | $2,014 | 0.20 |
| New Jersey | 56 | 875 | $1.0M | 0 | 0 | $0 | 0 |
| Colorado | 60 | 981 | $1.0M | 0 | 0 | $0 | 0 |

### Q-57_results.md

# Q-57 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ontario | $1.8M | $2.3M | 22.60 | 155 | 149 | 6 | 2,974 |
| California | $1.7M | $2.0M | 19.50 | 215 | 222 | -7 | 3,411 |
| British Columbia | $1.4M | $1.9M | 38.30 | 84 | 80 | 4 | 1,388 |
| Florida | $1.4M | $1.7M | 17.30 | 233 | 222 | 11 | 2,215 |
| Texas | $1.6M | $1.6M | 0.30 | 182 | 173 | 9 | 2,261 |
| Quebec | $1.3M | $1.4M | 8.50 | 99 | 100 | -1 | 1,805 |
| New York | $849,185 | $993,830 | 17 | 156 | 143 | 13 | 1,814 |
| Alberta | $864,265 | $877,539 | 1.50 | 61 | 50 | 11 | 695 |
| Illinois | $755,231 | $765,367 | 1.30 | 98 | 95 | 3 | 1,303 |
| New Jersey | $516,463 | $644,883 | 24.90 | 108 | 97 | 11 | 924 |
| Virginia | $353,005 | $536,277 | 51.90 | 66 | 58 | 8 | 599 |
| Colorado | $440,602 | $485,699 | 10.20 | 94 | 78 | 16 | 865 |
| Wisconsin | $285,216 | $485,437 | 70.20 | 55 | 46 | 9 | 399 |
| Ohio | $296,168 | $484,185 | 63.50 | 77 | 73 | 4 | 525 |
| Georgia | $366,367 | $473,284 | 29.20 | 86 | 82 | 4 | 655 |
| Washington | $423,585 | $458,313 | 8.20 | 67 | 69 | -2 | 850 |
| Arizona | $552,752 | $431,350 | -22 | 88 | 78 | 10 | 637 |
| North Carolina | $406,085 | $417,428 | 2.80 | 85 | 83 | 2 | 768 |
| Connecticut | $243,990 | $382,398 | 56.70 | 64 | 52 | 12 | 352 |
| Massachusetts | $487,294 | $373,325 | -23.40 | 80 | 63 | 17 | 742 |
| Michigan | $246,941 | $370,996 | 50.20 | 65 | 58 | 7 | 574 |
| Minnesota | $183,600 | $351,895 | 91.70 | 53 | 43 | 10 | 481 |
| Manitoba | $208,112 | $330,584 | 58.80 | 22 | 21 | 1 | 182 |
| Tennessee | $228,678 | $312,300 | 36.60 | 59 | 59 | 0 | 520 |
| Nevada | $65,047 | $296,673 | 356.10 | 43 | 33 | 10 | 227 |

### Q-68_results.md

# Q-68 Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| ALUME WAREHOUSE (DO NOT USE) | Quebec | $13,548 | $352,298 | $338,749 | 3.80 | 6 |
| FLUX LIGHTING | Quebec | $196,314 | $377,005 | $180,691 | 52.10 | 13 |
| SUPREME LIGHTING AND ELEC SUPPLIES | Ontario | $162,257 | $269,974 | $107,717 | 60.10 | 13 |
| CABINET AND LIGHTING SUPPLY | Nevada | $41,773 | $139,676 | $97,903 | 29.90 | 13 |
| DUBO ELECTRIQUE LTEE | Quebec | $66,071 | $159,044 | $92,973 | 41.50 | 13 |
| PRESTIGE LIGHTING-BROOKLYN | New York | $123,777 | $215,449 | $91,672 | 57.50 | 13 |
| CED-MULTIFAMILY | Virginia | $26,382 | $109,917 | $83,535 | 24 | 11 |
| CED-DENVER | Colorado | $93,418 | $176,405 | $82,987 | 53 | 13 |
| AZTEC LIGHTING INC | Nevada | $25,924 | $104,895 | $78,972 | 24.70 | 11 |
| AREVCO LIGHTING | Quebec | $181,046 | $259,273 | $78,228 | 69.80 | 13 |
| MCNAUGHTON-MCKAY ELEC/DBA CANIFF | Ohio | $52,852 | $121,589 | $68,737 | 43.50 | 9 |
| CAPITAL TRISTATE | Virginia | $7,174 | $74,085 | $66,911 | 9.70 | 4 |
| ECLAIRAGE UNION LIGHTING USD | Quebec | $4,071 | $67,581 | $63,510 | 6 | 5 |
| ROYAUME LUMINAIRE SHERBROOKE | Quebec | $29,638 | $91,562 | $61,924 | 32.40 | 13 |
| Lighting Partners of CF | Georgia | $16,014 | $73,789 | $57,775 | 21.70 | 7 |
| HOSPITALITY LIGHTING MANAGEMENT | Texas | $6,255 | $60,455 | $54,200 | 10.30 | 5 |
| ROYAUME LUMINAIRE BEAUPORT | Quebec | $32,239 | $84,683 | $52,444 | 38.10 | 13 |
| COMMERCE LIGHTING SUPPLY INC | New York | $4,505 | $52,422 | $47,917 | 8.60 | 3 |
| S AND D LIGHTING GROUP II LTD | Prince Edward Island | $20,071 | $67,501 | $47,430 | 29.70 | 12 |
| NEEDHAM ELECTRIC/ DBA WESCO DIST | Massachusetts | $12,535 | $56,699 | $44,164 | 22.10 | 7 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | CH3128-BG/OP | BOLLA LED CHANDELIERS BRUSHED GOLD_OPAL GLASS KUZCO | 6 | 3.30 | 293 | 88.80 | 22,472.32 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | CH407342BGGO | FIORE SOCKET CHANDELIERS BRUSHED GOLD_GLOSSY OPAL GLASS ALORA MOOD | 7 | 2.90 | 293 | 101 | 7,676.76 | DECAY_DETECTED |
| INC-K0002946 | WESCO DISTRIBUTION CANADA LP | WS16806-BK | DORCHESTER LED WALL_VANITY BLACK KUZCO | 7 | 32 | 208 | 6.50 | 108,455.60 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | PD631920BGOP | BONDI SOCKET PENDANTS BRUSHED GOLD_OPAL GLASS ALORA MOOD | 8 | 8.40 | 246 | 29.30 | 22,719.06 | DECAY_DETECTED |
| LLC-USACST245 | WAYFAIR LLC DBA JOSS AND MAIN | PD546719AGWL | OLIVER SOCKET PENDANTS AGED GOLD_WHITE LINEN ALORA MOOD | 278 | 1.90 | 6 | 3.20 | 170,018.42 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | CH355632VBGO | WYNWOOD SOCKET CHANDELIERS VINTAGE BRASS_GLOSSY OPAL ALORA | 8 | 19.90 | 154 | 7.70 | 67,067.32 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | PD321716NB | MARNI LED PENDANTS NATURAL BRASS ALORA | 11 | 22.50 | 90 | 4 | 90,206 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | CH336830VB-UNV | ANDERS LED CHANDELIERS VINTAGE BRASS ALORA | 24 | 19.40 | 51 | 2.60 | 119,194.30 | SLOWING |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | CH346046VBAR-UNV | DAHLIA LED CHANDELIERS VINTAGE BRASS_ALABASTER ALORA | 12 | 26.20 | 125 | 4.80 | 63,020.74 | DECAY_DETECTED |
| LLC-T00000223 | THE HOME DEPOT PRODUCT AUTHORITY LLC | PD546719AGWL | OLIVER SOCKET PENDANTS AGED GOLD_WHITE LINEN ALORA MOOD | 40 | 7.10 | 194 | 27.30 | 10,590.45 | DECAY_DETECTED |
| LLC-K0001858 | DOLAN NORTHWEST LLC | ZVL47321-CH (2700K) | CUSTOM VL47321-CH W/ 2700K LED | 19 | 10.10 | 285 | 28.20 | 9,400.51 | DECAY_DETECTED |
| INC-K0001977 | KUZCO LIGHTING LLC. | CF96956-BG | HORIZON LED FAN BRUSHED GOLD KUZCO | 5 | 60 | 216 | 3.60 | 65,207.58 | DECAY_DETECTED |
| LLC-USACST460 | WILLIAMS SONOMA INC | WV323225VBAR | CAESAR LED WALL_VANITY VINTAGE BRASS_ALABASTER ALORA | 32 | 8.90 | 111 | 12.50 | 18,094.72 | DECAY_DETECTED |
| LLC-K0001921 | LUMENS LIGHT & LIVING | FM48618 | NP-FM48618-5CCT | 49 | 4.30 | 55 | 12.80 | 17,495.52 | DECAY_DETECTED |
| LLC-K0001921 | LUMENS LIGHT & LIVING | CH89854-BG/GO-UNV | AMARA LED CHANDELIERS BRUSHED GOLD_GLOSSY OPAL GLASS KUZCO | 77 | 5.40 | 23 | 4.30 | 42,238.71 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | LP317448VB-UNV | OF ARYAS LED PENDANTS VINTAGE BRASS ALORA | 13 | 26.90 | 85 | 3.20 | 50,792.50 | DECAY_DETECTED |
| LLC-USACST460 | WILLIAMS SONOMA INC | LP21647-WT-UNV | OF DAKOTA LINEAR PENDANT WALNUT KUZCO | 50 | 6.40 | 62 | 9.70 | 16,340.35 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | LP348241VBPG | WILLARD SOCKET LINEAR PENDANT VINTAGE BRASS_PRISMATIC GLASS ALORA | 8 | 19.90 | 154 | 7.70 | 16,605.60 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | PD331016MWVB | DORAL SOCKET PENDANTS MATTE WHITE_VINTAGE BRASS ALORA | 8 | 19.90 | 154 | 7.70 | 16,246.56 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | PD507216MBOP | HARPER SOCKET PENDANTS MATTE BLACK_OPAL MATTE GLASS ALORA MOOD | 13 | 18.20 | 154 | 8.50 | 13,927.12 | DECAY_DETECTED |
| INC-K0000011 | BA ROBINSON CO LTD | AT7935-BK | VESTA LED WALL_VANITY BLACK KUZCO | 23 | 16.30 | 156 | 9.60 | 11,212.46 | DECAY_DETECTED |
| LLC-K0001921 | LUMENS LIGHT & LIVING | LP10356-BN | VEGA LED LINEAR PENDANT BRUSHED NICKEL KUZCO | 43 | 10.10 | 86 | 8.50 | 11,398.50 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | PD11708-BK | MONAE LED PENDANTS BLACK KUZCO | 14 | 14.10 | 133 | 9.40 | 9,975.42 | DECAY_DETECTED |
| LLC-K0001921 | LUMENS LIGHT & LIVING | PD87760-WH-UNV-010 | OF CERCHIO LED PENDANTS WHITE KUZCO | 7 | 41.90 | 154 | 3.70 | 25,314.57 | DECAY_DETECTED |
| LLC-K0002019 | LIGHTOPIA | LP549448MBOP | CASSIA SOCKET PENDANTS MATTE BLACK_OPAL MATTE GLASS ALORA MOOD | 5 | 25.20 | 198 | 7.90 | 11,707.96 | DECAY_DETECTED |
| LLC-USACST245 | WAYFAIR LLC DBA JOSS AND MAIN | FM556016AG | BRISBANE SOCKET FLUSH MOUNT AGED GOLD ALORA MOOD | 201 | 2.60 | 9 | 3.50 | 23,675.78 | DECAY_DETECTED |
| LLC-K0001921 | LUMENS LIGHT & LIVING | WV323225PNAR | CAESAR LED WALL_VANITY POLISHED NICKEL_ALABASTER ALORA | 34 | 12.40 | 84 | 6.80 | 11,949.35 | DECAY_DETECTED |
| LLC-USACST97 | BUILD.COM INC | FM47707-WH-5CCT | MIO FLUSH MOUNT WHITE KUZCO | 9 | 29.90 | 179 | 6 | 12,492.06 | DECAY_DETECTED |
| LLC-K0002661 | FERGUSON ENTERPRISES INC-NEWPORT | LP21647-BW-UNV | OF DAKOTA LINEAR PENDANT BEECH WOOD KUZCO | 8 | 19.90 | 154 | 7.70 | 9,585.94 | DECAY_DETECTED |
| LLC-K0001921 | LUMENS LIGHT & LIVING | SF62014-BK/CP | TRINITY LED SEMI FLUSH MOUNT BLACK_COPPER KUZCO | 97 | 5.10 | 30 | 5.90 | 12,134.45 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| INC-K0000011 | BA ROBINSON CO LTD | Manitoba | 1,510,477.25 | 816,213.55 | 85.10 | 0 | 14,108 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000138 | ROBINSON LIGHTING LTD | Manitoba | 921,068.97 | 440,970.83 | 108.90 | 0 | 8,998 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0002626 | DHILLON LIGHTING CALGARY | Alberta | 801,279.31 | 372,649.62 | 115 | 0 | 11,084 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000030 | ECLAIRAGE UNION MONTREAL | Quebec | 554,985.15 | 162,400.23 | 241.70 | 0 | 71,699 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000063 | MCLAREN LIGHTING | British Columbia | 508,131.74 | 196,228.19 | 158.90 | 0 | 6,596 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0001117 | MONTREAL LIGHTING AND HARDWARE | Quebec | 391,008.69 | 180,781.55 | 116.30 | 0 | 6,675 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000066 | MULTI LUMINAIRE GATINEAU | Quebec | 310,149.95 | 120,110.46 | 158.20 | 2,891 | 6,774 | -57.30 | COMPETITIVE_DISPLACEMENT |
| INC-K0000147 | FLUX LIGHTING | Ontario | 208,940.65 | 390,259.17 | -46.50 | 0 | 0 | — | CONTRACTING |
| LLC-USACST296 | LONESTAR ELECTRIC SUPPLY DBA LONESTAR LIGHTING AND TECHNOLOGY | Texas | 267,548.63 | 114,632.12 | 133.40 | 0 | 850 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0001191 | DECO LUMINAIRE QUEBEC | Quebec | 191,530.27 | 76,299.93 | 151 | 9,053 | 35,379 | -74.40 | COMPETITIVE_DISPLACEMENT |
| INC-K0000146 | MAPLE RIDGE LIGHTING INC | British Columbia | 288,932.76 | 182,673.14 | 58.20 | 0 | 2,892 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0003049 | CARTWRIGHT LIGHTING LTD | Alberta | 206,871.34 | 105,965.22 | 95.20 | 0 | 2,230 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000135 | BIRD STAIRS | Nova Scotia | 113,769.90 | 15,714.03 | 624 | 0 | 7,340 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000513 | RICHARDSON LIGHTING REGINA | Saskatchewan | 148,570.17 | 53,265.70 | 178.90 | 0 | 5,559 | -100 | COMPETITIVE_DISPLACEMENT |
| LLC-K0002065 | LIGHTING DESIGN COMPANY | Utah | 150,445.31 | 56,196.60 | 167.70 | 18,924 | 26,508 | -28.60 | COMPETITIVE_DISPLACEMENT |
| INC-K0002727 | VIVA LIFESTYLES INC | Ontario | 154,855.83 | 61,275.43 | 152.70 | 0 | 2,029 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-CANCST101 | WOLSELEY CALGARY | Alberta | 99,794.62 | 16,517.34 | 504.20 | 0 | 17,582 | -100 | COMPETITIVE_DISPLACEMENT |
| LLC-K0004513 | MCNAUGHTON-MCKAY ELEC/DBA CANIFF | Michigan | 34,300.70 | 113,809.11 | -69.90 | 0 | 0 | — | CONTRACTING |
| LLC-K0000145 | M & M LIGHTING | Texas | 105,130.80 | 27,654 | 280.20 | 0 | 9,132 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0003324 | PINE LIGHTING | British Columbia | 252,022.85 | 179,856.26 | 40.10 | 0 | 28,264 | -100 | COMPETITIVE_DISPLACEMENT |
| INC-K0000095 | SUPREME LIGHTING AND ELEC SUPPLIES | Ontario | 179,044.59 | 249,336.91 | -28.20 | 0 | 0 | — | CONTRACTING |
| LLC-K0000315 | REXEL | Georgia | 107,488.25 | 176,784.44 | -39.20 | 0 | 0 | — | CONTRACTING |
| LLC-K0001975 | CABINET AND LIGHTING SUPPLY | Nevada | 41,101.93 | 109,861.60 | -62.60 | 0 | 15,201 | -100 | CONTRACTING |
| LLC-K0002669 | AZTEC LIGHTING INC | Arizona | 25,533.93 | 88,713.48 | -71.20 | 0 | 0 | — | CONTRACTING |
| LLC-K0001947 | KENDALL ELECTRIC INC. | Michigan | 106,301.24 | 165,833.26 | -35.90 | 0 | 0 | — | CONTRACTING |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Kuzco Lighting Inc. (kll, org_id=166)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| INC-K0001977 | KUZCO LIGHTING LLC. | 2 | 534,486.22 | 343.60 | [{'quarter': '2025-07-01', 'revenue': 534486.22, 'qoq_pct': 343.6}, {'quarter': '2025-10-01', 'revenue': 190654.07, 'qoq_pct': -64.3}, {'quarter': '2026-01-01', 'revenue': 48670.75, 'qoq_pct': -74.5}, {'quarter': '2026-04-01', 'revenue': 178782.95, 'qoq_pct': 267.3}] |
| LLC-K0002209 | CITY LIGHTS LIGHTING SHOWROOM | 2 | 325,135.52 | 276.20 | [{'quarter': '2025-07-01', 'revenue': 59012.1, 'qoq_pct': -13.8}, {'quarter': '2025-10-01', 'revenue': 86423.83, 'qoq_pct': 46.5}, {'quarter': '2026-01-01', 'revenue': 325135.52, 'qoq_pct': 276.2}, {'quarter': '2026-04-01', 'revenue': 66507.97, 'qoq_pct': -79.5}] |
| LLC-K0000729 | GRAYBAR ELECTRIC - NOGA | 2 | 313,470.68 | 50.40 | [{'quarter': '2025-07-01', 'revenue': 233434.61, 'qoq_pct': 15.9}, {'quarter': '2025-10-01', 'revenue': 313470.68, 'qoq_pct': 34.3}, {'quarter': '2026-01-01', 'revenue': 180122.41, 'qoq_pct': -42.5}, {'quarter': '2026-04-01', 'revenue': 270984.33, 'qoq_pct': 50.4}] |
| LLC-K0004619 | US ELECTRICAL SERVICES INC | 2 | 248,078.28 | 197.10 | [{'quarter': '2025-07-01', 'revenue': 167855.33, 'qoq_pct': 197.1}, {'quarter': '2025-10-01', 'revenue': 109103.63, 'qoq_pct': -35.0}, {'quarter': '2026-01-01', 'revenue': 248078.28, 'qoq_pct': 127.4}, {'quarter': '2026-04-01', 'revenue': 101833.8, 'qoq_pct': -59.0}] |
| INC-K0000074 | NUVO SALES | 3 | 230,263.61 | 54.60 | [{'quarter': '2025-07-01', 'revenue': 71221.93, 'qoq_pct': -45.4}, {'quarter': '2025-10-01', 'revenue': 110088.19, 'qoq_pct': 54.6}, {'quarter': '2026-01-01', 'revenue': 160503.32, 'qoq_pct': 45.8}, {'quarter': '2026-04-01', 'revenue': 230263.61, 'qoq_pct': 43.5}] |
| LLC-K0001941 | SOUTH DADE LIGHTING | 2 | 226,013.25 | 332.70 | [{'quarter': '2025-07-01', 'revenue': 226013.25, 'qoq_pct': 332.7}, {'quarter': '2025-10-01', 'revenue': 31756.1, 'qoq_pct': -85.9}, {'quarter': '2026-01-01', 'revenue': 47048.6, 'qoq_pct': 48.2}, {'quarter': '2026-04-01', 'revenue': 18531.4, 'qoq_pct': -60.6}] |
| LLC-K0001967 | KUZCO LIGHTING INC. | 2 | 184,058.46 | 594 | [{'quarter': '2025-07-01', 'revenue': 26522.16, 'qoq_pct': -69.9}, {'quarter': '2025-10-01', 'revenue': 184058.46, 'qoq_pct': 594.0}, {'quarter': '2026-01-01', 'revenue': 40387.77, 'qoq_pct': -78.1}, {'quarter': '2026-04-01', 'revenue': 139582.43, 'qoq_pct': 245.6}] |
| INC-K0003389 | NORTHLAND PROPERTIES | 2 | 179,944.82 | 1,710.30 | [{'quarter': '2025-07-01', 'revenue': 9940.14, 'qoq_pct': -51.2}, {'quarter': '2025-10-01', 'revenue': 179944.82, 'qoq_pct': 1710.3}, {'quarter': '2026-01-01', 'revenue': 54986.24, 'qoq_pct': -69.4}, {'quarter': '2026-04-01', 'revenue': 135932.27, 'qoq_pct': 147.2}] |
| LLC-K0001705 | TURTLE & HUGHES INC | 2 | 171,289.80 | 1,009.90 | [{'quarter': '2025-07-01', 'revenue': 51815.91, 'qoq_pct': 204.9}, {'quarter': '2025-10-01', 'revenue': 25978.0, 'qoq_pct': -49.9}, {'quarter': '2026-01-01', 'revenue': 15433.18, 'qoq_pct': -40.6}, {'quarter': '2026-04-01', 'revenue': 171289.8, 'qoq_pct': 1009.9}] |
| LLC-K0002750 | LIGHTSTYLE AUTOMATED SYSTEMS INC | 2 | 160,271.50 | 2,681.30 | [{'quarter': '2025-07-01', 'revenue': 949.0, 'qoq_pct': -86.0}, {'quarter': '2025-10-01', 'revenue': 5762.5, 'qoq_pct': 507.2}, {'quarter': '2026-01-01', 'revenue': 160271.5, 'qoq_pct': 2681.3}, {'quarter': '2026-04-01', 'revenue': 265.0, 'qoq_pct': -99.8}] |
| LLC-K0004679 | CED MILPITAS- SAN FRANCISCO | 2 | 147,978 | 921.90 | [{'quarter': '2025-07-01', 'revenue': 147978.0, 'qoq_pct': 921.9}, {'quarter': '2025-10-01', 'revenue': 9192.8, 'qoq_pct': -93.8}, {'quarter': '2026-01-01', 'revenue': 23269.1, 'qoq_pct': 153.1}, {'quarter': '2026-04-01', 'revenue': 25419.0, 'qoq_pct': 9.2}] |
| INC-K0000330 | MERCURY LIGHTING LIMITED | 2 | 145,518.87 | 5,156.20 | [{'quarter': '2025-07-01', 'revenue': 5758.94, 'qoq_pct': 212.2}, {'quarter': '2025-10-01', 'revenue': 0.0, 'qoq_pct': -100.0}, {'quarter': '2026-01-01', 'revenue': 2768.5, 'qoq_pct': None}, {'quarter': '2026-04-01', 'revenue': 145518.87, 'qoq_pct': 5156.2}] |
| LLC-K0002067 | REXEL INC | 3 | 141,148.47 | 1,681 | [{'quarter': '2025-07-01', 'revenue': 29330.24, 'qoq_pct': 1681.0}, {'quarter': '2025-10-01', 'revenue': 63484.06, 'qoq_pct': 116.4}, {'quarter': '2026-01-01', 'revenue': 125165.19, 'qoq_pct': 97.2}, {'quarter': '2026-04-01', 'revenue': 141148.47, 'qoq_pct': 12.8}] |
| LLC-K0000303 | MAYER ELECTRIC SUPPLY CO INC | 2 | 134,155.31 | 65.20 | [{'quarter': '2025-07-01', 'revenue': 91951.88, 'qoq_pct': 65.2}, {'quarter': '2025-10-01', 'revenue': 134155.31, 'qoq_pct': 45.9}, {'quarter': '2026-01-01', 'revenue': 90062.85, 'qoq_pct': -32.9}, {'quarter': '2026-04-01', 'revenue': 87621.73, 'qoq_pct': -2.7}] |
| LLC-K0002524 | VIKING ELECTRIC SUPPLY | 2 | 130,089 | 160 | [{'quarter': '2025-07-01', 'revenue': 43224.0, 'qoq_pct': 9.0}, {'quarter': '2025-10-01', 'revenue': 65363.1, 'qoq_pct': 51.2}, {'quarter': '2026-01-01', 'revenue': 50029.5, 'qoq_pct': -23.5}, {'quarter': '2026-04-01', 'revenue': 130089.0, 'qoq_pct': 160.0}] |

### Q-ORG-STOCKOUT_results.md

(not present — file does not exist or is empty)
