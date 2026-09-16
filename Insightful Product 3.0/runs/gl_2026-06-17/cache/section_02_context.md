# Section 2 Context Bundle — Golden Lighting (gl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=6096, portal_order_gmv=$2.6M |
| HAS_INVENTORY | True | inventory_count=3058 |
| HAS_SALES_DATA | True | sales_data_count=36842 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=28 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$2.6M > ecat_gmv=$131,176: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 28 | engagement_reps=28 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 51 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 240, Mixpanel total submit_order (Q-01): 59 |
| USER_GROUP_SPLIT_AVAILABLE | True | join_rate=98.0%, ambiguous_rate=0.0%, showroom_event_share=13.9% |
| USER_GROUP_JOIN_RATE | 98% | 50 of 51 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 14% | showroom+admin share of matched events: 13.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Sholeh Duncan, Sholeh Duncan |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=2 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=905 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=856 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Golden Lighting
- **Shortname**: gl
- **Org ID**: 187
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Golden Lighting (gl, org_id=187)
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

# Signal Rank — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Total signals fired**: 35 (P0: 20, P1: 10, P2: 5)
- **Org GMV**: $0.1M eCat LTM, $2.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 9903-24 MG (Ziva by Golden Lighting Autumn Twilight ) $79,468 LTM, 0 available | P0 | §3 Product | 10.0 | $79,468 | 3.0 | 2,384,038 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 3118-L BLK-SD (Yep by Golden Lighting Hines 1-light 14i) $74,996 LTM, 0 available | P0 | §3 Product | 10.0 | $74,996 | 3.0 | 2,249,878 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 9903-12 MG (Ziva by Golden Lighting Autumn Twilight ) $67,163 LTM, 0 available | P0 | §3 Product | 10.0 | $67,163 | 3.0 | 2,014,876 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 7312-L BP (Golden Lighting Bartlett 2-light Pendant) $58,825 LTM, 0 available | P0 | §3 Product | 10.0 | $58,825 | 3.0 | 1,764,763 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 6805-6 BLK-NR (Golden Lighting Everly 6-light Chandelie) $42,401 LTM, 0 available | P0 | §3 Product | 10.0 | $42,401 | 3.0 | 1,272,043 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 9903-6 MG (Ziva by Golden Lighting Autumn Twilight ) $41,930 LTM, 0 available | P0 | §3 Product | 10.0 | $41,930 | 3.0 | 1,257,908 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 6937-M BLK-NR (Golden Lighting Valentina 1-light Pendan) $41,561 LTM, 0 available | P0 | §3 Product | 10.0 | $41,561 | 3.0 | 1,246,826 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 1270-13 BLK (Wry Lighting Morgon 2-light 13" Flush Mo) $41,544 LTM, 0 available | P0 | §3 Product | 10.0 | $41,544 | 3.0 | 1,246,329 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 6950-L MBS (Golden Lighting Shepard 1-light Pendant ) $34,834 LTM, 0 available | P0 | §3 Product | 10.0 | $34,834 | 3.0 | 1,045,015 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 7312-L CP (Golden Lighting Bartlett 2-light Pendant) $32,869 LTM, 0 available | P0 | §3 Product | 10.0 | $32,869 | 3.0 | 986,058 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 6070-LP BLK-BLK (Golden Lighting Tribeca 5-light Island L) $32,606 LTM, 0 available | P0 | §3 Product | 10.0 | $32,606 | 3.0 | 978,173 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 1017-69 BLK (Golden Lighting Alastair 15-light 2-tier) $28,315 LTM, 0 available | P0 | §3 Product | 10.0 | $28,315 | 3.0 | 849,450 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 1017-96 BLK (Golden Lighting Alastair 15-light 2-tier) $28,248 LTM, 0 available | P0 | §3 Product | 10.0 | $28,248 | 3.0 | 847,438 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 3118-L PW-SD (Yep by Golden Lighting Hines 1-light 14i) $27,819 LTM, 0 available | P0 | §3 Product | 10.0 | $27,819 | 3.0 | 834,563 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — 8001-BA3 BLK-SD (Golden Lighting Parrish 3-light Vanity i) $25,628 LTM, 0 available | P0 | §3 Product | 10.0 | $25,628 | 3.0 | 768,844 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — 3118-L RBZ-SD (Yep by Golden Lighting Hines 1-light 14i) $25,317 LTM, 0 available | P0 | §3 Product | 10.0 | $25,317 | 3.0 | 759,502 | RISK |
| 17 | SIG-OPP-01 | Next Best Product — 3164-FM BCB-HWG/3164-FM BLK-HWG co-purchase pattern across 10 customers | P0 | §2/§3 | 1.0 | $293,278 | 2.0 | 586,555 | POSITIVE |
| 18 | SIG-COMMERCE-01 | Capture Rate — eCat captures 5.0% of $3M total business; each +1pt = $26K | P0 | §4 Commerce | 4.7 | $26,000 | 3.0 | 370,324 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — THE LIGHTING DESIGN CO. 2 consecutive QoQ acceleration quarters, $11,875 peak quarter (+191% QoQ) | P0 | §2 Accounts | 6.4 | $11,875 | 3.0 | 226,694 | POSITIVE |
| 20 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 3 | 0 | 0 | 3 | |
| §3 Product Intelligence | 16 | 0 | 1 | 17 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 9 | 4 | 13 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 3164-FM BCB-HWG/3164-FM BLK-HWG co-purchase pattern across 10 customers
2. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 5.0% of $3M total business; each +1pt = $26K
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — THE LIGHTING DESIGN CO. 2 consecutive QoQ acceleration quarters, $11,875 peak quarter (+191% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 9903-24 MG (Ziva by Golden Lighting Autumn Twilight ) $79,468 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 3118-L BLK-SD (Yep by Golden Lighting Hines 1-light 14i) $74,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 9903-12 MG (Ziva by Golden Lighting Autumn Twilight ) $67,163 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Golden Lighting (gl, org_id=187)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | 3164-FM BCB-HWG | 1 | OPP-01 | $293,278 |
| 2 | THE LIGHTING DESIGN CO. | 1 | MOM-01 | $11,875 |
| 3 | THE WELL APPOINTED HOUSE | 1 | MOM-01 | $10,754 |

### Q-12_results.md

# Q-12 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 2,340 | 189 | 71 | 47 | 23 |

### Q-14_results.md

# Q-14 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 195600 | ELEGANT LIGHTING /WEST SPRINGFIELD | 22 | $8,053 | 2025-06-26 21:39:48 | 2026-06-16 21:31:16 | 16.90 |
| 060301 | FIXTURE THIS | 19 | $5,147 | 2025-06-26 19:24:48 | 2026-05-11 17:34:56 | 17.70 |
| 014201 | VERMONT LIGHTING DBA THE LIGHTING HOUSE | 17 | $6,387 | 2025-07-09 17:14:00 | 2026-04-08 12:48:02 | 17.10 |
| 221900 | VILLAGE LIGHTING AND SUPPLY/ LORAIN | 12 | $5,164 | 2025-08-08 14:31:25 | 2026-06-08 17:07:40 | 27.60 |
| 210200 | US 31 SUPPLY | 12 | $2,758 | 2025-11-04 21:37:55 | 2026-06-10 18:05:29 | 19.80 |
| 085700 | HOUSTON LIGHTBULB & LIGHTING / HOUSTON | 10 | $3,470 | 2025-06-25 16:39:06 | 2026-06-16 20:57:17 | 39.60 |
| 083850 | Home And Light Valdosta | 10 | $3,299 | 2025-11-21 16:33:14 | 2026-06-05 19:03:03 | 21.80 |
| 063000 | Fogg Lighting | 9 | $3,014 | 2025-06-25 19:31:21 | 2026-05-08 17:24:26 | 39.60 |
| 035900 | Cline-Holder Electric Supply, Inc / Elizabethton | 8 | $2,156 | 2025-06-19 17:43:32 | 2026-05-04 14:57:28 | 45.60 |
| 193350 | STAGGS CARPETS & INTERIORS dba STAGGS INTERIORS | 8 | $2,478 | 2025-06-25 21:21:46 | 2026-05-07 16:59:01 | 45.10 |
| 191700 | SOUTHERN LIGHTS/BURNSVILLE | 6 | $5,042 | 2025-08-28 18:57:42 | 2025-12-31 18:40:11 | 25 |
| 135650 | MJG INTERIORS | 6 | $1,766 | 2025-07-10 13:36:43 | 2025-10-13 12:33:25 | 19 |
| 011950 | AUSTELL LIGHTING | 5 | $1,241 | 2025-09-23 14:29:32 | 2026-04-09 18:41:42 | 49.50 |
| 100000 | JULIAN DESIGNS | 5 | $3,504 | 2026-01-21 21:27:58 | 2026-05-11 18:11:18 | 27.50 |
| 150890 | O'CONNOR HOME DESIGN LLC | 5 | $1,238 | 2025-10-09 15:52:57 | 2026-06-03 14:20:34 | 59.20 |
| 061705 | TANSON BOUTIQUE LLC | 4 | $6,854 | 2026-03-09 16:49:51 | 2026-04-22 13:39:55 | 14.60 |
| 012700 | ANNE THOMPSON & ASSOCIATES INC | 4 | $1,280 | 2025-06-27 15:49:57 | 2026-03-10 12:11:49 | 85.30 |
| 111460 | CJ LIGHTING AND FANS | 4 | $1,387 | 2025-12-04 18:40:08 | 2026-05-01 22:26:20 | 49.40 |
| 111360 | Kenyon Noble Lumber Company | 3 | $1,151 | 2026-03-10 16:42:31 | 2026-05-11 18:20:55 | 31 |
| 033890 | COTTAGE INSPIRED LLC | 3 | $824 | 2025-08-14 17:31:36 | 2026-02-17 20:10:38 | 93.60 |

### Q-14b_results.md

# Q-14b Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 044100 | DOLAN NORTHWEST LLC | 71 | 1.80 | 4.10 | 2.28 | $23,544 |
| 084000 | HOBRECHT LIGHTING | 8 | 5 | 33.70 | 6.74 | $13,723 |
| 062100 | FRONT STREET LIGHTING | 12 | 11.70 | 19.60 | 1.68 | $12,538 |
| 123500 | LIGHTING INCORPORATED | 23 | 7.10 | 11.10 | 1.56 | $11,788 |
| 070350 | GADSDEN LIGHTING SHOWROOM | 12 | 8 | 21.40 | 2.68 | $11,602 |
| 123035 | THE LITE COMPANY | 5 | 9 | 31 | 3.44 | $11,404 |
| 081100 | GALLERY OF LIGHTING | 33 | 4.40 | 7.60 | 1.73 | $11,308 |
| 192800 | SHALLOTTE ELECTRIC | 26 | 5.10 | 11.10 | 2.18 | $10,937 |
| 194100 | STEADFAST LIGHTING | 14 | 9 | 17.30 | 1.92 | $10,802 |
| 125202 | LIGHTING FIRST/ FORT MYERS | 20 | 7.80 | 11.70 | 1.50 | $10,257 |
| 081300 | HOME LIGHTING/FRAZER | 21 | 5.40 | 13.80 | 2.56 | $10,256 |
| 123039 | LIFESTYLES STORES | 24 | 4.10 | 11.10 | 2.71 | $9,650 |
| 195600 | ELEGANT LIGHTING | 17 | 9.60 | 14.70 | 1.53 | $8,517 |
| 085600 | IDAHO DREAMING | 11 | 11.70 | 21.30 | 1.82 | $8,359 |
| 073402 | GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC | 14 | 8.60 | 16.30 | 1.90 | $7,805 |

### Q-17_results.md

# Q-17 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 180700 | ROYAUME LUMINAIRE/ TERREBONNE | QC | 2026-01-13 00:10:28 | 1 | $5,793 |
| 123230 | LIGHT LAB DESIGN LLC | NY | 2026-01-12 20:15:19 | 1 | $5,775 |
| 191700 | SOUTHERN LIGHTS/BURNSVILLE | MN | 2025-12-31 18:40:11 | 6 | $5,042 |
| 222700 | Valley Electric Supply / Ansonia | CT | 2025-06-19 23:30:13 | 2 | $4,350 |
| 065600 | FIRST COAST LIGHTING AND FANS, LLC | FL | 2026-01-12 16:02:38 | 1 | $4,200 |
| 180702 | ROYAUME LUMINAIRE/ BEAUPORT | QC | 2026-01-13 00:07:45 | 1 | $3,943 |
| 100800 | ECLECTIC INTERIORS INC. dba JILL HERTZ INTERIOR DESIGN / MEM | TN | 2026-02-23 21:45:04 | 2 | $3,030 |
| 022500 | BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH | SC | 2025-06-20 15:06:51 | 1 | $2,660 |
| 123027 | LUXURY DESIGN / LD INC. | NY | 2025-12-31 21:18:26 | 2 | $2,409 |
| 231050 | WELL DRESSED HOME DESIGNS | FL | 2025-12-12 15:21:27 | 2 | $2,283 |
| 080400 | HOUSE OF LAMPS & SHADES | FL | 2026-01-26 20:17:44 | 1 | $2,200 |
| 032550 | CHRISTY BROWN INTERIOR DESIGN LLC | MD | 2026-02-18 02:44:21 | 1 | $1,980 |
| 135650 | MJG INTERIORS | VT | 2025-10-13 12:33:25 | 6 | $1,766 |
| 232400 | Wholesale Lighting / Daytona | FL | 2026-01-26 15:21:30 | 1 | $1,465 |
| 012700 | ANNE THOMPSON & ASSOCIATES INC | FL | 2026-03-10 12:11:49 | 4 | $1,280 |
| 039700 | COASTAL LIGHTING SUPPLY/ WILMINGTON | NC | 2026-01-10 23:10:21 | 1 | $1,210 |
| 043300 | Dupage Lighting Inc. | IL | 2025-09-22 16:43:13 | 3 | $1,200 |
| 150875 | OCEANSIDE LIGHTING AND FAN | CA | 2025-11-24 17:37:47 | 2 | $836 |
| 033890 | COTTAGE INSPIRED LLC | TX | 2026-02-17 20:10:38 | 3 | $824 |
| 041550 | Design A La Mode Inc | WI | 2025-09-05 15:41:10 | 3 | $809 |
| 137120 | MILA LEE DESIGN LLC dba DIANE BISHOP INTERIORS | PA | 2026-03-03 16:23:07 | 1 | $696 |
| 141300 | PROGRESSIVE LIGHTING, INC | AL | 2025-08-28 14:15:03 | 1 | $645 |
| 160700 | PRESTIGE LIGHTING/ LANSING | IL | 2025-09-05 16:07:23 | 1 | $635 |
| 123338 | LOUISANA HOME CENTER | LA | 2026-03-05 14:37:18 | 3 | $614 |
| 014000 | AZTEC LIGHTING INC. | AZ | 2025-07-16 21:31:02 | 2 | $595 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 180700 | ROYAUME LUMINAIRE/ TERREBONNE | QC | $5,793 | 2026-01-13 00:10:28 | 155 |
| 123230 | LIGHT LAB DESIGN LLC | NY | $5,775 | 2026-01-12 20:15:19 | 155 |
| 191700 | SOUTHERN LIGHTS/BURNSVILLE | MN | $5,042 | 2025-12-31 18:40:11 | 167 |
| 234805 | WILLIAMS ELECTRIC SUPPLY | TN | $4,662 | 2026-03-17 17:04:33 | 91 |
| 222700 | Valley Electric Supply / Ansonia | CT | $4,350 | 2025-06-19 23:30:13 | 362 |
| 065600 | FIRST COAST LIGHTING AND FANS, LLC | FL | $4,200 | 2026-01-12 16:02:38 | 155 |
| 180702 | ROYAUME LUMINAIRE/ BEAUPORT | QC | $3,943 | 2026-01-13 00:07:45 | 155 |
| 100800 | ECLECTIC INTERIORS INC. dba JILL HERTZ INTERIOR DESIGN / MEM | TN | $3,030 | 2026-02-23 21:45:04 | 113 |
| 022500 | BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH | SC | $2,660 | 2025-06-20 15:06:51 | 361 |
| 123027 | LUXURY DESIGN / LD INC. | NY | $2,409 | 2025-12-31 21:18:26 | 167 |
| 231050 | WELL DRESSED HOME DESIGNS | FL | $2,283 | 2025-12-12 15:21:27 | 186 |
| 080400 | HOUSE OF LAMPS & SHADES | FL | $2,200 | 2026-01-26 20:17:44 | 141 |
| 032550 | CHRISTY BROWN INTERIOR DESIGN LLC | MD | $1,980 | 2026-02-18 02:44:21 | 119 |
| 135650 | MJG INTERIORS | VT | $1,766 | 2025-10-13 12:33:25 | 246 |
| 232400 | Wholesale Lighting / Daytona | FL | $1,465 | 2026-01-26 15:21:30 | 141 |
| 012700 | ANNE THOMPSON & ASSOCIATES INC | FL | $1,280 | 2026-03-10 12:11:49 | 98 |
| 039700 | COASTAL LIGHTING SUPPLY/ WILMINGTON | NC | $1,210 | 2026-01-10 23:10:21 | 157 |
| 043300 | Dupage Lighting Inc. | IL | $1,200 | 2025-09-22 16:43:13 | 267 |
| 150875 | OCEANSIDE LIGHTING AND FAN | CA | $836 | 2025-11-24 17:37:47 | 204 |
| 033890 | COTTAGE INSPIRED LLC | TX | $824 | 2026-02-17 20:10:38 | 119 |

### Q-40_results.md

# Q-40 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| FL | 8 | 12 | $12,315 |
| TX | 6 | 35 | $10,709 |
| QC | 2 | 2 | $9,736 |
| NY | 3 | 4 | $8,604 |
| MN | 2 | 11 | $8,546 |
| VT | 3 | 24 | $8,285 |
| MA | 1 | 22 | $8,053 |
| TN | 2 | 4 | $7,692 |
| KS | 1 | 4 | $6,854 |
| OH | 2 | 13 | $5,425 |
| CT | 2 | 5 | $4,850 |
| CA | 4 | 5 | $4,159 |
| GA | 2 | 11 | $3,409 |
| ME | 1 | 9 | $3,014 |
| IN | 1 | 12 | $2,758 |
| SC | 1 | 1 | $2,660 |
| MS | 2 | 9 | $2,574 |
| AL | 4 | 8 | $2,334 |
| VA | 1 | 8 | $2,156 |
| IL | 3 | 5 | $2,000 |

### Q-41_results.md

# Q-41 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 18
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | eCat Online-Acquired (self-serve) | 9 |
| 2025-04-01 | eCat Online-Acquired (self-serve) | 6 |
| 2025-05-01 | eCat Online-Acquired (self-serve) | 11 |
| 2025-06-01 | Rep-Acquired (iPad) | 1 |
| 2025-06-01 | eCat Online-Acquired (self-serve) | 4 |
| 2025-07-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 3 |
| 2025-09-01 | eCat Online-Acquired (self-serve) | 3 |
| 2025-10-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-11-01 | eCat Online-Acquired (self-serve) | 3 |
| 2025-12-01 | Rep-Acquired (iPad) | 1 |
| 2025-12-01 | eCat Online-Acquired (self-serve) | 4 |
| 2026-01-01 | Rep-Acquired (iPad) | 3 |
| 2026-01-01 | eCat Online-Acquired (self-serve) | 2 |
| 2026-02-01 | eCat Online-Acquired (self-serve) | 3 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 3 |
| 2026-04-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-05-01 | eCat Online-Acquired (self-serve) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 5
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Corinne Noreyko | 1 |
| JC Gonzalez | 1 |
| Laura Ford | 1 |
| Melissa Schultheis | 1 |
| Sholeh Duncan | 1 |

### Q-52_results.md

# Q-52 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 501950 | ENTERPRISE LIGHTING | — | 3 | $44,822 | 0 | $0 | 0 |
| 160000 | PACE LIGHTING | — | 24 | $38,438 | 0 | $0 | 0 |
| 191700 | SOUTHERN LIGHTS | — | 39 | $34,739 | 6 | $5,042 | 14.50 |
| 092803 | INLINE ELECTRIC SUPPLY | — | 28 | $32,528 | 0 | $0 | 0 |
| 060050 | FROMM ELECTRIC SUPPLY CORP | — | 2 | $29,990 | 0 | $0 | 0 |
| 092805 | INLINE ELECTRIC SUPPLY | — | 24 | $29,396 | 0 | $0 | 0 |
| 139000 | NORTHERN LIGHTING / WESTERVILLE | — | 38 | $29,328 | 0 | $0 | 0 |
| 063400 | FORT WORTH LIGHTING | — | 26 | $29,269 | 0 | $0 | 0 |
| 030600 | CRESCENT LIGHTING SUPPLY | — | 40 | $27,456 | 0 | $0 | 0 |
| 021400 | BBC LIGHTING & SUPPLY | — | 26 | $25,970 | 0 | $0 | 0 |
| 020900 | BROTHERS LIGHTING AND FAN GALLERY | — | 38 | $23,950 | 0 | $0 | 0 |
| 123023 | THE LIGHTING DESIGN CO. | — | 76 | $23,747 | 0 | $0 | 0 |
| 044100 | DOLAN NORTHWEST LLC | — | 72 | $23,544 | 0 | $0 | 0 |
| 038700 | COLONIAL ELECTRIC SUPPLY | — | 27 | $21,902 | 0 | $0 | 0 |
| 231058 | THE WELL APPOINTED HOUSE | — | 70 | $19,787 | 0 | $0 | 0 |
| 180210 | Rite Rug Co | — | 26 | $18,849 | 0 | $0 | 0 |
| 060628 | FERGUSON #1455/ CARSON | — | 15 | $18,536 | 0 | $0 | 0 |
| 123350 | THE LIGHTING CORNER INC | — | 27 | $18,127 | 0 | $0 | 0 |
| 022700 | BRECHER LIGHTING | — | 27 | $16,940 | 0 | $0 | 0 |
| 081500 | HANSEN LIGHTING INC | — | 20 | $16,129 | 0 | $0 | 0 |
| 021300 | BRIGHT IDEAS OF ROCHESTER | — | 28 | $15,973 | 0 | $0 | 0 |
| 051700 | LIGHTING BY DESIGN/ APPLETON | — | 29 | $15,763 | 0 | $0 | 0 |
| 083801 | ARCH STREET LIGHTING | — | 3 | $15,537 | 0 | $0 | 0 |
| 100600 | JUST LIGHTS | — | 30 | $15,534 | 0 | $0 | 0 |
| 233801 | KENDALL ELECTRIC INC | — | 31 | $15,044 | 0 | $0 | 0 |
| 234805 | WILLIAMS ELECTRIC SUPPLY | — | 3 | $14,691 | 2 | $4,662 | 31.70 |
| 135200 | METRO ELECTRIC SUPPLY | — | 55 | $14,505 | 0 | $0 | 0 |
| 233198 | WOLFE LIGHTING IDAHO FALLS | — | 16 | $14,423 | 0 | $0 | 0 |
| 212300 | URBAN LIGHTS | — | 43 | $14,412 | 0 | $0 | 0 |
| 065600 | FIRST COAST LIGHTING AND FANS, LLC | — | 23 | $14,108 | 1 | $4,200 | 29.80 |

### Q-53_results.md

# Q-53 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 501950 | ENTERPRISE LIGHTING | — | 3 | $44,822 |
| 160000 | PACE LIGHTING | — | 24 | $38,438 |
| 092803 | INLINE ELECTRIC SUPPLY | — | 28 | $32,528 |
| 060050 | FROMM ELECTRIC SUPPLY CORP | — | 2 | $29,990 |
| 092805 | INLINE ELECTRIC SUPPLY | — | 24 | $29,396 |
| 139000 | NORTHERN LIGHTING / WESTERVILLE | — | 38 | $29,328 |
| 063400 | FORT WORTH LIGHTING | — | 26 | $29,269 |
| 030600 | CRESCENT LIGHTING SUPPLY | — | 40 | $27,456 |
| 021400 | BBC LIGHTING & SUPPLY | — | 26 | $25,970 |
| 123023 | THE LIGHTING DESIGN CO. | — | 76 | $23,747 |
| 044100 | DOLAN NORTHWEST LLC | — | 72 | $23,544 |
| 038700 | COLONIAL ELECTRIC SUPPLY | — | 27 | $21,902 |
| 231058 | THE WELL APPOINTED HOUSE | — | 70 | $19,787 |
| 180210 | Rite Rug Co | — | 26 | $18,849 |
| 060628 | FERGUSON #1455/ CARSON | — | 15 | $18,536 |
| 123350 | THE LIGHTING CORNER INC | — | 27 | $18,127 |
| 081500 | HANSEN LIGHTING INC | — | 20 | $16,129 |
| 021300 | BRIGHT IDEAS OF ROCHESTER | — | 28 | $15,973 |
| 051700 | LIGHTING BY DESIGN/ APPLETON | — | 29 | $15,763 |
| 083801 | ARCH STREET LIGHTING | — | 3 | $15,537 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AL | 0 | 0 | $0 | 4 | 8 | $2,334 | — |
| AR | 0 | 0 | $0 | 1 | 2 | $836 | — |
| AZ | 0 | 0 | $0 | 1 | 2 | $595 | — |
| BC | 0 | 0 | $0 | 1 | 1 | $312 | — |
| CA | 0 | 0 | $0 | 4 | 5 | $4,159 | — |
| CT | 0 | 0 | $0 | 2 | 5 | $4,850 | — |
| FL | 0 | 0 | $0 | 8 | 12 | $12,315 | — |
| GA | 0 | 0 | $0 | 2 | 11 | $3,409 | — |
| ID | 0 | 0 | $0 | 1 | 1 | $330 | — |
| IL | 0 | 0 | $0 | 3 | 5 | $2,000 | — |
| IN | 0 | 0 | $0 | 1 | 12 | $2,758 | — |
| KS | 0 | 0 | $0 | 1 | 4 | $6,854 | — |
| LA | 0 | 0 | $0 | 3 | 5 | $1,331 | — |
| MA | 0 | 0 | $0 | 1 | 22 | $8,053 | — |
| MD | 0 | 0 | $0 | 1 | 1 | $1,980 | — |
| ME | 0 | 0 | $0 | 1 | 9 | $3,014 | — |
| MN | 0 | 0 | $0 | 2 | 11 | $8,546 | — |
| MO | 0 | 0 | $0 | 1 | 4 | $1,387 | — |
| MS | 0 | 0 | $0 | 2 | 9 | $2,574 | — |
| MT | 0 | 0 | $0 | 1 | 3 | $1,151 | — |

### Q-57_results.md

# Q-57 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unknown | $960,610 | $1.0M | 4.20 | 680 | 655 | 25 | 2,491 |

### Q-68_results.md

# Q-68 Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 030600 | CRESCENT LIGHTING SUPPLY/KIRKLAND | 3306-BA3 BLK-BLK | 3-Light Vanity Light | 5 | 25 | 69 | 2.80 | 6,765 | SLOWING |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 12
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 139000 | NORTHERN LIGHTING / WESTERVILLE | 29,327.75 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |
| 063400 | FORT WORTH LIGHTING | 29,269 | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 10 |
| 123023 | THE LIGHTING DESIGN CO. | 23,747 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |
| 123350 | THE LIGHTING CORNER INC | 18,127 | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 10 |
| 081500 | HANSEN LIGHTING INC | 16,129 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |
| 051700 | LIGHTING BY DESIGN/ APPLETON | 15,763 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |
| 233198 | WOLFE LIGHTING IDAHO FALLS | 14,423 | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 10 |
| 138800 | MUSKA LIGHTING CENTER | 13,538 | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 10 |
| 062100 | FRONT STREET LIGHTING | 12,538 | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 10 |
| 143300 | NOTOCO INDUSTRIES, LLC | 12,140 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |
| 124400 | LIGHTS UNLIMITED INC | 11,462.50 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |
| 081100 | GALLERY OF LIGHTING | 11,308 | 3164-FM BCB-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Brushed Champagne Brass | 3164-FM BLK-HWG | Yep by Golden Lighting Aenon 3-light Flush Mount in Matte Black | 10 |

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 123023 | THE LIGHTING DESIGN CO. | 2 | 11,875 | 190.90 | [{'quarter': '2025-10-01', 'revenue': 3037.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 8835.0, 'qoq_pct': 190.9}, {'quarter': '2026-04-01', 'revenue': 11875.0, 'qoq_pct': 34.4}] |
| 231058 | THE WELL APPOINTED HOUSE | 2 | 10,753.70 | 105.20 | [{'quarter': '2025-10-01', 'revenue': 3791.98, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 5240.86, 'qoq_pct': 38.2}, {'quarter': '2026-04-01', 'revenue': 10753.7, 'qoq_pct': 105.2}] |
| 060640 | FERGUSON ENTERPRISES / CHANTILLY #001 | 2 | 9,143.50 | 625.70 | [{'quarter': '2025-10-01', 'revenue': 605.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1260.0, 'qoq_pct': 108.3}, {'quarter': '2026-04-01', 'revenue': 9143.5, 'qoq_pct': 625.7}] |
| 180500 | RENSEN HOUSE OF LIGHTS | 2 | 6,767.53 | 58.80 | [{'quarter': '2025-10-01', 'revenue': 2792.05, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 4260.75, 'qoq_pct': 52.6}, {'quarter': '2026-04-01', 'revenue': 6767.53, 'qoq_pct': 58.8}] |
| 070350 | GADSDEN LIGHTING SHOWROOM | 2 | 6,283 | 107.30 | [{'quarter': '2025-10-01', 'revenue': 2288.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 3031.0, 'qoq_pct': 32.5}, {'quarter': '2026-04-01', 'revenue': 6283.0, 'qoq_pct': 107.3}] |
| 081100 | GALLERY OF LIGHTING | 2 | 5,273 | 50 | [{'quarter': '2025-10-01', 'revenue': 2414.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 3621.0, 'qoq_pct': 50.0}, {'quarter': '2026-04-01', 'revenue': 5273.0, 'qoq_pct': 45.6}] |
| 132700 | MOUNTAIN LIGHTING | 2 | 5,219 | 235.40 | [{'quarter': '2025-10-01', 'revenue': 707.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 2371.0, 'qoq_pct': 235.4}, {'quarter': '2026-04-01', 'revenue': 5219.0, 'qoq_pct': 120.1}] |
| 125001 | LIGHTSTYLES | 2 | 4,778 | 60.50 | [{'quarter': '2025-10-01', 'revenue': 2131.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 3420.0, 'qoq_pct': 60.5}, {'quarter': '2026-04-01', 'revenue': 4778.0, 'qoq_pct': 39.7}] |
| 062000 | EFIRD'S INTERIORS, INC. | 2 | 4,225.92 | 103.30 | [{'quarter': '2025-10-01', 'revenue': 1368.03, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 2078.55, 'qoq_pct': 51.9}, {'quarter': '2026-04-01', 'revenue': 4225.92, 'qoq_pct': 103.3}] |
| 185700 | RICHARDS LIGHTING | 2 | 3,990 | 148.80 | [{'quarter': '2025-10-01', 'revenue': 678.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1687.0, 'qoq_pct': 148.8}, {'quarter': '2026-04-01', 'revenue': 3990.0, 'qoq_pct': 136.5}] |
| 0606740 | FERGUSON ENTERPRISES | 2 | 3,709 | 128.50 | [{'quarter': '2025-10-01', 'revenue': 1139.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1623.0, 'qoq_pct': 42.5}, {'quarter': '2026-04-01', 'revenue': 3709.0, 'qoq_pct': 128.5}] |
| 194800 | STOKES ELECTRIC CO | 2 | 3,682 | 142.90 | [{'quarter': '2025-10-01', 'revenue': 1045.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1516.0, 'qoq_pct': 45.1}, {'quarter': '2026-04-01', 'revenue': 3682.0, 'qoq_pct': 142.9}] |
| 180300 | RAYMOND DE STEIGER | 2 | 3,475 | 151.80 | [{'quarter': '2025-10-01', 'revenue': 590.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1380.0, 'qoq_pct': 133.9}, {'quarter': '2026-04-01', 'revenue': 3475.0, 'qoq_pct': 151.8}] |
| 044200 | DISTINCTIVE LIGHTING/BOZEMAN | 2 | 3,343 | 68.40 | [{'quarter': '2025-10-01', 'revenue': 1416.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1985.0, 'qoq_pct': 40.2}, {'quarter': '2026-04-01', 'revenue': 3343.0, 'qoq_pct': 68.4}] |
| 024900 | BRIGHTER HOMES LIGHTING | 2 | 3,080 | 287.50 | [{'quarter': '2025-10-01', 'revenue': 440.0, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 1705.0, 'qoq_pct': 287.5}, {'quarter': '2026-04-01', 'revenue': 3080.0, 'qoq_pct': 80.6}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Golden Lighting (gl, org_id=187)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9903-24 MG | Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Mystic Gold | 9903 | 79,467.93 | 24 | — | 2026-10-04 | [{'customer': 'INLINE ELECTRIC #11 / ATHENS', 'revenue': 11248.5}, {'customer': 'MAPLE RIDGE LIGHTING', 'revenue': 7678.8}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 3749.5}, {'customer': 'BOWLING GREEN WINLECTRIC', 'revenue': 3199.5}, {'customer': 'CAPE ELECTRICAL SUPPLY / CAPE GIRARDEAU', 'revenue': 3199.5}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 3199.5}, {'customer': 'ELLEN LIGHTING/ STAFFORD', 'revenue': 3199.5}, {'customer': 'ELUME DISTINCTIVE LIGHTING', 'revenue': 3199.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 3199.5}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 3199.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 3199.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 3199.5}, {'customer': 'KENDALL ELECTRIC', 'revenue': 3199.5}, {'customer': 'LIGHTING EXPO / FREEHOLD', 'revenue': 3199.5}, {'customer': 'LIGHTING AND BULBS UNLIMITED', 'revenue': 3199.5}, {'customer': 'LISA PLATT DESIGNS', 'revenue': 3199.5}, {'customer': 'TEXAS BRIGHT IDEAS/ HARKER HEIGHTS', 'revenue': 3199.5}, {'customer': 'ARIZONA LIGHTING / MESA', 'revenue': 3199.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 3199.5}, {'customer': None, 'revenue': 3199.5}, {'customer': 'LINDAS DESIGN dba CASA DE DECOR', 'revenue': 2399.63}] | [{'item': '9903-WSC MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 2-light Wall Sconce in Mystic Gold', 'available': 34}, {'item': '9903-6 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Black Iron', 'available': 24}, {'item': '9903-24 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Black Iron', 'available': 10}, {'item': '9903-18 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Black Iron', 'available': 7}, {'item': '9903-18 MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Mystic Gold', 'available': 5}, {'item': '9903-12 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Black Iron', 'available': 2}] |
| 3118-L BLK-SD | Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Seeded Glass | 3118 | 74,995.93 | 818 | — | 2026-08-06 | [{'customer': None, 'revenue': 11688.75}, {'customer': 'VILLA LIGHTING', 'revenue': 11225.89}, {'customer': 'STEADFAST LIGHTING - SPRINGDALE, AR', 'revenue': 4885.51}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 2569.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 2493.75}, {'customer': 'Southside Lighting Gallery', 'revenue': 2314.02}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 2216.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 2014.89}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 1437.43}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 1379.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 1137.0}, {'customer': 'KINGSTON LIGHTING AKA MCCAFFERTY NEIL B ELECTRIC COMPANY LTD', 'revenue': 1070.73}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 814.76}, {'customer': 'JUST LIGHTS  INC', 'revenue': 675.5}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 661.5}, {'customer': 'COSHOCTON LUMBER COMPANY', 'revenue': 567.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 557.0}, {'customer': 'Better Living Store', 'revenue': 537.0}, {'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 513.26}, {'customer': 'BUTLER LIGHTING/HIGH POINT', 'revenue': 462.5}, {'customer': 'ELEKTRA LIGHTS & FANS', 'revenue': 462.5}, {'customer': 'FERGUSON ENTERPRISES / 2715/ 226/ 228 / OMAHA', 'revenue': 462.5}, {'customer': 'THE LIGHTING SHOPPE/ CAMBRIDGE', 'revenue': 447.76}, {'customer': 'FERGUSON ENTERPRISES #118/ MURFREESBORO', 'revenue': 398.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 398.0}, {'customer': 'Ferguson Enterprises #3131/ St. George', 'revenue': 391.0}, {'customer': 'FERGUSON #2657 / BOWLING GREEN', 'revenue': 384.0}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 378.0}, {'customer': 'Ferguson Enterprises #951 / #952 Indianapolis', 'revenue': 378.0}, {'customer': 'ONE SOURCE LIGHTING / BILLINGS', 'revenue': 377.0}, {'customer': 'LIGHTING UNLIMITED/ COLUMBUS', 'revenue': 370.0}, {'customer': None, 'revenue': 370.0}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 368.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 368.0}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 367.0}, {'customer': 'GEORGIAN LIGHTING GALLERY INC', 'revenue': 358.0}, {'customer': 'Plumbing Distributors Inc / Lawrenceville', 'revenue': 328.26}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 312.18}, {'customer': 'KBL DESIGN CENTER INC/ PEORIA', 'revenue': 298.5}, {'customer': 'N.E.O. ELECTRICAL SUPPLY COMPANY', 'revenue': 298.5}, {'customer': 'PIONEER LIGHTING INC.', 'revenue': 298.5}, {'customer': 'ILLUMINATIONS/McALLEN', 'revenue': 298.5}, {'customer': 'LIGHT BRITE/ TRENTON', 'revenue': 298.5}, {'customer': 'Ferguson Enterprises / Corpus Christi', 'revenue': 283.5}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 277.5}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 277.5}, {'customer': 'US 31 SUPPLY', 'revenue': 277.5}, {'customer': 'US ELECTRICAL SERVICES DBA YALE ELECTRIC SUPPLY / WEST CHEST', 'revenue': 277.5}, {'customer': 'LDB HOLDINGS LLC, dba CW FLOORS & LIGHTING / DENTON', 'revenue': 277.5}, {'customer': 'KENDALL ELECTRIC INC / FORT WAYNE', 'revenue': 277.5}, {'customer': 'FAN AND LIGHTING WORLD/ BOYNTON BEACH', 'revenue': 277.5}, {'customer': "HAGEN'S LIGHTING", 'revenue': 277.5}, {'customer': 'Echo Group Inc dba Echo Lighting Gallery', 'revenue': 277.5}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 277.5}, {'customer': 'VILLAGE MAYTAG DBA VILLAGE HOME STORES', 'revenue': 273.63}, {'customer': 'METRO APPLIANCES & MORE/OKL CITY', 'revenue': 273.5}, {'customer': 'AL ENTERPRISES dba VALUE LIGHTING, INC. / CARROLLTON', 'revenue': 268.5}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 268.5}, {'customer': 'CANDLELIGHT LIGHT & LOG/ SAGINAW', 'revenue': 268.5}, {'customer': 'LIGHTING ETC / N RICHLAND HILLS', 'revenue': 268.5}, {'customer': 'BLACK DIAMOND ACQUISITIONS  dba ALLOWAY LIGHTING CO', 'revenue': 268.5}, {'customer': 'PROGRESSIVE LIGHTING, INC', 'revenue': 268.5}, {'customer': 'LEBANON ELECTRIC SUPPLY, INC', 'revenue': 233.75}, {'customer': 'LIGHT SYSTEMS, INC.', 'revenue': 223.89}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 223.89}, {'customer': 'ROB AND NITA YOUNG LLC dba YOUNG & CO', 'revenue': 199.0}, {'customer': 'BILLOWS ELECTRIC SUPPLY/ BERLIN', 'revenue': 199.0}, {'customer': 'DEKKER LIGHTING', 'revenue': 199.0}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 199.0}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 199.0}, {'customer': 'FIXTURE THIS', 'revenue': 199.0}, {'customer': 'FERGUSON ENTERPRISES / SACRAMENTO #686', 'revenue': 199.0}, {'customer': 'FERGUSON ENTERPRISES / LOUISVILLE #185 #1168', 'revenue': 199.0}, {'customer': 'FANGIO / THE  FACTORY LIGHTING / FURNITURE / PATIO', 'revenue': 199.0}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 199.0}, {'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 199.0}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 199.0}, {'customer': 'KENDALL ELECTRIC / GRAND RAPIDS', 'revenue': 199.0}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 199.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 199.0}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 199.0}, {'customer': 'LIGHT SOURCE LIGHTING/ PLAINFIELD', 'revenue': 199.0}, {'customer': 'PACE LIGHTING', 'revenue': 199.0}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 199.0}, {'customer': 'SIERRA PLUMBING SUPPLY', 'revenue': 199.0}, {'customer': 'SHALLOTTE ELECTRIC', 'revenue': 199.0}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 199.0}, {'customer': 'WILSON LIGHTING/ CLAYTON', 'revenue': 199.0}, {'customer': 'DESIGNER LIGHTING & FAN / SHOWROOM', 'revenue': 189.0}, {'customer': 'WOLBERG ELECTRICAL SUPPLY/ SCHENECTADY/ALBANY WAREHOUSE', 'revenue': 189.0}, {'customer': 'The Lite House / Columbia', 'revenue': 189.0}, {'customer': 'SCOTTIES INTERIORS', 'revenue': 189.0}, {'customer': 'Raymond De Steiger/ Ray Lighting Center', 'revenue': 189.0}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 189.0}, {'customer': 'FERGUSON ENTERPRISES #1550/ ADDISON IL', 'revenue': 189.0}, {'customer': 'Kitchens & Bath By Briggs / Omaha', 'revenue': 185.0}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 185.0}, {'customer': 'House of Lights / Mayfield HTS', 'revenue': 185.0}, {'customer': 'THE PLUMBING WAREHOUSE - LCR / SHREVEPORT', 'revenue': 185.0}, {'customer': 'WINSUPPLY COOKEVILLE TN CO', 'revenue': 185.0}, {'customer': 'FERGUSON ENTERPRISES / BROOKSHIRE 2812', 'revenue': 185.0}, {'customer': 'FERGUSON ENTERPRISES / #12 NORFOLK', 'revenue': 185.0}, {'customer': 'FERGUSON ENTERPRISES #499/ CHARLOTTESVILLE', 'revenue': 185.0}, {'customer': 'ELLIOTT ELECTRIC SUPPLY / NACOGDOCHES', 'revenue': 185.0}, {'customer': 'Be The Light Designs LLC', 'revenue': 185.0}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 185.0}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 185.0}, {'customer': 'METRO ELECTRIC SUPPLY/ ST LOUIS/ BRENTWOOD', 'revenue': 179.56}, {'customer': 'FERGUSON ENTERPRISES #1196 / FRANKLIN MA', 'revenue': 179.0}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 179.0}, {'customer': 'PROSOURCE SUPPLY / EASLEY', 'revenue': 179.0}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 179.0}, {'customer': 'E S LIGHTING', 'revenue': 179.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 179.0}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 179.0}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 179.0}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 179.0}, {'customer': 'PROGRESSIVE LIGHTING INC #07 / LEE LIGHTING / DULUTH', 'revenue': 149.26}, {'customer': 'LIGHTING WORLD / STATEN ISLAND SHOWROOM', 'revenue': 99.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 99.5}, {'customer': None, 'revenue': 99.5}, {'customer': 'Distinctive Lighting / Bozeman', 'revenue': 99.5}, {'customer': 'BOWLING GREEN WINLECTRIC', 'revenue': 99.5}, {'customer': 'Stokes Electrical Supply Co, Inc.', 'revenue': 99.5}, {'customer': None, 'revenue': 99.5}, {'customer': 'WHS WHOLESALE dba COURTESY ELECTRIC WHOLESALE', 'revenue': 94.5}, {'customer': 'Trinity Home Center', 'revenue': 94.5}, {'customer': 'KIRBY RISK CORP/ LAFAYETTE', 'revenue': 92.5}, {'customer': 'PROGRESSIVE LIGHTING INC #05 / LEE LIGHTING / ROSWELL', 'revenue': 92.5}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': 92.5}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 74.63}, {'customer': 'SCHAEDLER YESCO/ HARRISBURG', 'revenue': 74.63}, {'customer': 'FERGUSON ENTERPRISES #43/ GREENVILLE SC', 'revenue': 47.25}, {'customer': 'PREMIER LIGHTING/ BAKERSFIELD', 'revenue': 46.25}] | [{'item': '3118-M1L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Opal Glass', 'available': 558}, {'item': '3118-M1L RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Seeded Glass', 'available': 144}, {'item': '3118-2SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 106}, {'item': '3118-M1L PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Seeded Glass', 'available': 105}, {'item': '3118-BA2 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Seeded Glass', 'available': 105}, {'item': '3118-BA3 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-BA3 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-L BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Opal Glass', 'available': 59}, {'item': '3118-BA2 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-2SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Opal Glass', 'available': 56}, {'item': '3118-BA3 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Opal Glass', 'available': 55}, {'item': '3118-BA3 CH-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Opal Glass', 'available': 55}, {'item': '3118-3SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 CH-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Chrome and Opal Glass', 'available': 54}, {'item': '3118-BA2 CH-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Opal Glass', 'available': 52}, {'item': '3118-BA2 PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Pewter', 'available': 42}, {'item': '3118-2SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Pewter', 'available': 42}, {'item': '3118-L BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Clear Glass', 'available': 32}, {'item': '3118-1SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-BA1 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-2SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 29}, {'item': '3118-BA2 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Seeded Glass', 'available': 29}, {'item': '3118-L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Chrome and Seeded Glass', 'available': 28}, {'item': '3118-SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 28}, {'item': '3118-SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 28}, {'item': '3118-3SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 27}, {'item': '3118-4SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Semi-Flush Mount in Matte Black', 'available': 26}, {'item': '3118-BA3 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Opal Glass', 'available': 26}, {'item': '3118-BA4 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Seeded Glass', 'available': 26}, {'item': '3118-BA4 CH-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Opal Glass', 'available': 24}, {'item': '3118-BA4 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA3 PW-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Pewter and Opal Glass', 'available': 23}, {'item': '3118-SF14 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14 in Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA4 PW-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Seeded Glass', 'available': 21}, {'item': '3118-BA3 BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Clear Glass', 'available': 21}, {'item': '3118-M1L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Opal Glass', 'available': 20}, {'item': '3118-BA4 CH-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Seeded Glass', 'available': 19}, {'item': '3118-BA4 PW-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Opal Glass', 'available': 19}, {'item': '3118-BA4 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Opal Glass', 'available': 18}, {'item': '3118-BA1 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA1 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA2 BCB-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Opal Glass', 'available': 13}, {'item': '3118-BA4 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Opal Glass', 'available': 12}, {'item': '3118-M1L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Chrome and Seeded Glass', 'available': 11}, {'item': '3118-1SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Pewter', 'available': 9}, {'item': '3118-BA1 PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Seeded Glass', 'available': 9}, {'item': '3118-BA1 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-3SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Chrome', 'available': 6}, {'item': '3118-BA3 CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Seeded Glass', 'available': 6}, {'item': '3118-1SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 5}, {'item': '3118-2SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Chrome', 'available': 2}, {'item': '3118-BA2 CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Seeded Glass', 'available': 2}, {'item': '3118-L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Opal Glass', 'available': 1}, {'item': '3118-SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 1}, {'item': '3118-2SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 1}, {'item': '3118-BA2 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Opal Glass', 'available': 1}] |
| 9903-12 MG | Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Mystic Gold | 9903 | 67,162.55 | 65 | — | 2026-10-04 | [{'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 4085.65}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 3268.5}, {'customer': 'ROYCE COLLECTION / REDFORD', 'revenue': 2339.0}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 2179.0}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ IRVING', 'revenue': 2179.0}, {'customer': 'JACOBSON ELECTRIC', 'revenue': 1634.25}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 1634.25}, {'customer': 'DREAM HOUSE FURNISHINGS', 'revenue': 1499.4}, {'customer': 'TARELI INC dba MI CASA LIGHTING & FANS', 'revenue': 1249.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 1249.5}, {'customer': 'Hortons Home Lighting / LaGrange', 'revenue': 1249.5}, {'customer': 'THE PLUMBING WAREHOUSE - LCR / SHREVEPORT', 'revenue': 1249.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 1249.5}, {'customer': 'SOURCE LIGHTING / KALISPELL', 'revenue': 1249.5}, {'customer': 'SUN LIGHTING INC/ TEMPE', 'revenue': 1249.5}, {'customer': 'DESIGNER LIGHTING & FAN / SHOWROOM', 'revenue': 1249.5}, {'customer': 'DESIGN LIGHTING/ SURREY', 'revenue': 1225.69}, {'customer': 'WHS WHOLESALE dba COURTESY ELECTRIC WHOLESALE', 'revenue': 1124.55}, {'customer': 'LIGHTING RESOURCE STUDIO', 'revenue': 1089.5}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 1089.5}, {'customer': 'LISA PLATT DESIGNS', 'revenue': 1089.5}, {'customer': 'LINDAS DESIGN dba CASA DE DECOR', 'revenue': 1089.5}, {'customer': 'Luxur Lighting / Cedar City', 'revenue': 1089.5}, {'customer': None, 'revenue': 1089.5}, {'customer': 'AMERICAN LIGHTING / JOHNSON CITY', 'revenue': 1089.5}, {'customer': None, 'revenue': 1089.5}, {'customer': 'CAPITOL LIGHTING/ HANOVER', 'revenue': 1089.5}, {'customer': 'DULLES ELECTRIC SUPPLY CORP / STERLING', 'revenue': 1089.5}, {'customer': 'DRIFTWOOD GALLERIES', 'revenue': 1089.5}, {'customer': 'EP LIGHTING LLC', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES #48/ WILMINGTON NC', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES #13/ KNOXVILLE', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES / BROOKSHIRE 2812', 'revenue': 1089.5}, {'customer': 'FERGUSON ENTERPRISES / #2790 PITTSBURGH', 'revenue': 1089.5}, {'customer': 'Georgia Lighting', 'revenue': 1089.5}, {'customer': 'PREMIER BATH LIGHTING & HARDWARE dba HERALD WHOLESALE', 'revenue': 1089.5}, {'customer': 'HOBRECHT LIGHTING', 'revenue': 1089.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 1089.5}, {'customer': 'KENDALL ELECTRIC', 'revenue': 1089.5}, {'customer': 'THE LITE COMPANY', 'revenue': 1089.5}, {'customer': 'PINE GROVE LIGHTING & ELECTRICAL SUPPLY', 'revenue': 1089.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 1089.5}, {'customer': 'RICHARDS LIGHTING/ HUNTSVILLE', 'revenue': 1089.5}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 1089.5}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 1013.24}, {'customer': 'LIGHTING FIRST/ NAPLES', 'revenue': 937.13}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 817.13}, {'customer': 'US 31 SUPPLY', 'revenue': 817.13}, {'customer': 'BRECHER LIGHTING / LEXINGTON', 'revenue': 817.13}, {'customer': 'AURORA LIGHTING COMPANY', 'revenue': 544.75}, {'customer': 'WAGE LIGHTING & DESIGN', 'revenue': 544.75}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 544.75}, {'customer': 'CAPITAL ELECTRIC / WILMINGTON', 'revenue': 544.75}] | [{'item': '9903-WSC MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 2-light Wall Sconce in Mystic Gold', 'available': 34}, {'item': '9903-6 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Black Iron', 'available': 24}, {'item': '9903-24 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Black Iron', 'available': 10}, {'item': '9903-18 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Black Iron', 'available': 7}, {'item': '9903-18 MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Mystic Gold', 'available': 5}, {'item': '9903-12 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Black Iron', 'available': 2}] |
| 7312-L BP | Golden Lighting Bartlett 2-light Pendant in Black Patina | 7312 | 58,825.44 | 617 | — | 2026-08-06 | [{'customer': None, 'revenue': 38360.05}, {'customer': 'WHITE STAR SUPPLY LLC / BRUNSWICK 2', 'revenue': 1776.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 1567.6}, {'customer': 'METRO APPLIANCES & MORE/OKL CITY', 'revenue': 1406.76}, {'customer': 'ROBINSON LIGHTING/ KELOWNA', 'revenue': 984.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': 886.28}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 783.76}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 746.5}, {'customer': 'TIDEWATER LIGHTING & DESIGN LLC', 'revenue': 627.0}, {'customer': 'SUNBELT LIGHTING LLC/ HATTIESBURG', 'revenue': 522.5}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 518.5}, {'customer': 'The Lighting Design Co / Layton', 'revenue': 422.0}, {'customer': 'KING ELECTRIC', 'revenue': 418.0}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 414.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 365.76}, {'customer': "HENSON'S CARPET ONE", 'revenue': 365.76}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 328.5}, {'customer': 'PSJM dba STERLING CARPET ONE / GRAND FORKS', 'revenue': 313.5}, {'customer': 'SUNBELT LIGHTING LLC / BILOXI', 'revenue': 313.5}, {'customer': 'IBS LIGHTING, LTD / THE COLONY', 'revenue': 313.5}, {'customer': None, 'revenue': 313.5}, {'customer': 'RACHELS LIGHTING / PANAMA CITY', 'revenue': 313.5}, {'customer': 'KIE SUPPLY CORP/ KENNEWICK', 'revenue': 311.5}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 311.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 307.5}, {'customer': 'CAPPADONNA OF AZ', 'revenue': 307.5}, {'customer': 'CAPITAL ELECTRIC SUPPLY / NORTH CHARLESTON', 'revenue': 235.14}, {'customer': 'HERMITAGE', 'revenue': 219.0}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 219.0}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 211.0}, {'customer': None, 'revenue': 209.0}, {'customer': 'ELLIOTT ELECTRIC SUPPLY / NACOGDOCHES', 'revenue': 209.0}, {'customer': 'Lyteworks', 'revenue': 209.0}, {'customer': 'The Lite House / Columbia', 'revenue': 209.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 209.0}, {'customer': 'CHAMPLAIN VALLEY ELECTRIC SUPPLY COMPANY, INC.', 'revenue': 209.0}, {'customer': 'LUMENAREA', 'revenue': 209.0}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 209.0}, {'customer': 'OAK HEART INTERIORS LLC', 'revenue': 209.0}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 209.0}, {'customer': 'LIGHTING INCORPORATED / AUSTIN, TX', 'revenue': 207.0}, {'customer': 'LIGHTING WORLD / STATEN ISLAND SHOWROOM', 'revenue': 205.0}, {'customer': 'CREGGER COMPANY / WEST COLUMBIA', 'revenue': 205.0}, {'customer': 'SUNBELT LIGHTING LLC / MADISON', 'revenue': 205.0}, {'customer': 'PLUMBING DISTRIBUTORS INC/ MCDONOUGH', 'revenue': 156.76}, {'customer': 'Lights on Banks', 'revenue': 123.19}, {'customer': 'MAPLE RIDGE LIGHTING', 'revenue': 123.0}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 105.5}, {'customer': 'APPLICO, LLC/ TUSCALOOSA', 'revenue': 104.5}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 104.5}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 104.5}, {'customer': 'CAPITAL ELECTRIC / BLUFFTON', 'revenue': 104.5}, {'customer': 'Brandon Lighting / MS', 'revenue': 104.5}, {'customer': 'Better Living Store', 'revenue': 104.5}, {'customer': 'AMERICAN LIGHTING / KNOXVILLE', 'revenue': 104.5}, {'customer': 'HINSDALE LIGHTING / WESTMONT', 'revenue': 104.5}, {'customer': "HAGEN'S LIGHTING", 'revenue': 102.5}, {'customer': 'SUNBELT LIGHTING LLC / LAFAYETTE', 'revenue': 102.5}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 102.5}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 78.38}] | [{'item': '7312-SF BP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Black Patina', 'available': 59}, {'item': '7312-S CP', 'desc': 'Golden Lighting Bartlett 1-light Pendant in Copper Patina', 'available': 52}, {'item': '7312-BA1 BP', 'desc': 'Golden Lighting Bartlett 1-light Vanity in Black Patina', 'available': 33}, {'item': '7312-SF FW', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in French White', 'available': 30}, {'item': '7312-SF CP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Copper Patina', 'available': 27}, {'item': '7312-BA1 FW', 'desc': 'Golden Lighting Bartlett 1-light Vanity in French White', 'available': 19}, {'item': '7312-FM CP', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in Copper Patina', 'available': 15}, {'item': '7312-L FW', 'desc': 'Golden Lighting Bartlett 2-light Pendant in French White', 'available': 11}, {'item': '7312-1W CP', 'desc': 'Golden Lighting Bartlett 1-light Wall Sconce in Copper Patina', 'available': 10}, {'item': '7312-FM FW', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in French White', 'available': 5}, {'item': '7312-BA3 FW', 'desc': 'Golden Lighting Bartlett 3-light Vanity in French White', 'available': 5}, {'item': '7312-BA2 FW', 'desc': 'Golden Lighting Bartlett 2-light Vanity in French White', 'available': 5}, {'item': '7312-BA3 CP', 'desc': 'Golden Lighting Bartlett 3-light Vanity in Copper Patina', 'available': 4}, {'item': '7312-FM16 BP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Black Patina', 'available': 3}, {'item': '7312-FM16 FW', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in French White', 'available': 3}, {'item': '7312-S FW', 'desc': 'Golden Lighting Bartlett 1-light Pendant in French White', 'available': 3}, {'item': '7312-BA2 BP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Black Patina', 'available': 2}, {'item': '7312-BA2 CP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Copper Patina', 'available': 2}, {'item': '7312-FM16 CP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Copper Patina', 'available': 1}] |
| 6805-6 BLK-NR | Golden Lighting Everly 6-light Chandelier in Matte Black and Natural Rattan shade | 6805 | 42,401.43 | 173 | — | 2026-07-13 | [{'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 2021.0}, {'customer': 'BEE RIDGE LIGHTING & DESIGN', 'revenue': 1791.5}, {'customer': 'LIGHTING & DESIGN BY J&K ELECTRIC SUPPLY CO', 'revenue': 1763.5}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 1716.23}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 1702.5}, {'customer': 'PC BUILDING MATERIALS dba PC HOME CENTER', 'revenue': 1575.0}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 1543.25}, {'customer': 'COASTAL LIGHTING SUPPLY/ WILMINGTON', 'revenue': 1468.0}, {'customer': 'THE LIGHTING STUDIO / SENOIA', 'revenue': 1312.5}, {'customer': 'ELEGANT LIGHTING /WEST SPRINGFIELD', 'revenue': 1027.0}, {'customer': 'ROB AND NITA YOUNG LLC dba YOUNG & CO', 'revenue': 1022.0}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 787.5}, {'customer': 'FERGUSON ENTERPRISES / RICHMOND 5', 'revenue': 787.5}, {'customer': 'Light Store USA', 'revenue': 764.5}, {'customer': 'DECORATIVE LIGHTING, INC.', 'revenue': 759.5}, {'customer': 'LIGHTING FIRST/ NAPLES', 'revenue': 738.26}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 736.5}, {'customer': 'LIGHTING CONCEPTS & DESIGN', 'revenue': 656.25}, {'customer': 'IMAGINE MORE SERVICE / NORTHERN LIGHTS', 'revenue': 525.0}, {'customer': 'Southern Lighting Gallery/ Augusta', 'revenue': 525.0}, {'customer': 'BRECHER LIGHTING / LOUISVILLE', 'revenue': 479.0}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 479.0}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 472.16}, {'customer': 'DESIGN LIGHTING/ SURREY', 'revenue': 315.0}, {'customer': 'ROYAUME LUMINAIRE/ SHERBROOKE', 'revenue': 295.32}, {'customer': 'Lights on Banks', 'revenue': 295.31}, {'customer': 'ROYAUME LUMINAIRE/ TERREBONNE', 'revenue': 291.36}, {'customer': 'JUST LIGHTS  INC', 'revenue': 262.5}, {'customer': 'BILLOWS ELECTRIC SUPPLY/ BERLIN', 'revenue': 262.5}, {'customer': 'CHICOINE INTERIORS', 'revenue': 262.5}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 262.5}, {'customer': 'CREATIVE LIGHTING/ ST. PAUL', 'revenue': 262.5}, {'customer': 'CREGGER COMPANY / WEST COLUMBIA', 'revenue': 262.5}, {'customer': 'Coffman Home Decor LLC', 'revenue': 262.5}, {'customer': 'COLONIAL ELECTRIC SUPPLY COMPANY / KING OF PRUSSIA', 'revenue': 262.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 262.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 262.5}, {'customer': 'EAST VALLEY FANS & BLINDS / MESA', 'revenue': 262.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 262.5}, {'customer': 'FLA LIGHTING INC. dba LIGHTING DEPOT', 'revenue': 262.5}, {'customer': 'FERGUSON ENTERPRISES #196/ TAMPA', 'revenue': 262.5}, {'customer': 'Ferguson Enterprises #1869 / Round Rock', 'revenue': 262.5}, {'customer': 'FLINZ HOLDINGS LLC dba THE GALLERY OF LIGHTS / LONGVIEW', 'revenue': 262.5}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 262.5}, {'customer': 'GREENBRIER LIGHTING/ CHESAPEAKE', 'revenue': 262.5}, {'customer': 'GREENBRIER LIGHTING dba GREENBRIER LIGHTING AT HILLTOP', 'revenue': 262.5}, {'customer': 'HILL COUNTRY HOME CENTER LLC / KERRVILLE', 'revenue': 262.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 262.5}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 262.5}, {'customer': 'KING ELECTRIC', 'revenue': 262.5}, {'customer': 'Lyteworks', 'revenue': 262.5}, {'customer': 'Lighting by Design / Exton', 'revenue': 262.5}, {'customer': 'LIGHTING UNLIMITED LLC dba LIGHTING ETC  / PANAMA CITY BEACH', 'revenue': 262.5}, {'customer': 'THE LIGHT CENTER/ FORT COLLINS', 'revenue': 262.5}, {'customer': 'LOWCOUNTRY LIGHTING STUDIO', 'revenue': 262.5}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 262.5}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 262.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 262.5}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ CHARLOTTE', 'revenue': 262.5}, {'customer': 'PREMIERE LIGHTING GALLERY/ BEAVERCREEK', 'revenue': 262.5}, {'customer': 'PINE GROVE LIGHTING & ELECTRICAL SUPPLY', 'revenue': 262.5}, {'customer': 'RANDOLPH LIGHTING', 'revenue': 262.5}, {'customer': 'TEXAS BRIGHT IDEAS/ GEORGETOWN', 'revenue': 262.5}, {'customer': 'REXEL USA/TECHE ELECTRIC/ LAFAYETTE', 'revenue': 262.5}, {'customer': 'LIGHTING FIRST OF FLORIDA/ BONITA SPG', 'revenue': 249.38}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 244.13}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 244.13}, {'customer': 'HOME LIGHTING/ MALVERN', 'revenue': 239.5}, {'customer': 'MOUNTAINLAND SUPPLY / OREM', 'revenue': 239.5}, {'customer': 'US 31 SUPPLY', 'revenue': 239.5}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 239.5}, {'customer': 'FERGUSON ENTERPRISES #1196 / FRANKLIN MA', 'revenue': 239.5}, {'customer': 'DULLES ELECTRIC SUPPLY CORP / STERLING', 'revenue': 239.5}, {'customer': 'BIGGINS LIGHTING', 'revenue': 239.5}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 239.5}, {'customer': 'The Lite House / Columbia', 'revenue': 239.5}, {'customer': 'SCOTTIES INTERIORS', 'revenue': 239.5}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 234.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 234.5}, {'customer': 'Filament, Inc / St Louis Park', 'revenue': 234.5}, {'customer': 'LEE SUPPLY CORP / INDIANAPOLIS', 'revenue': 234.5}, {'customer': "HILL'S LIGHTING/ BONITA SPRINGS", 'revenue': 234.5}, {'customer': 'CLEVELAND LIGHTING / LYNDHURST', 'revenue': 234.5}, {'customer': 'BURGESS LIGHTING / FORRESTVILLE', 'revenue': 234.5}, {'customer': 'Heritage Lighting', 'revenue': 234.5}, {'customer': 'ONE STOP LIGHTING / THOUSAND OAKS', 'revenue': 234.5}, {'customer': 'Bayside Electric Supply', 'revenue': 234.5}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 234.5}, {'customer': 'CRESCENT LIGHTING SUPPLY/KIRKLAND', 'revenue': 234.5}, {'customer': 'ILLUMINATING EXPRESSIONS / EVANSVILLE IN', 'revenue': 234.5}, {'customer': 'ROYAUME LUMINAIRE/ SAINTE-JULIE', 'revenue': 143.7}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 143.7}, {'customer': 'ABC CREATIONS, LLC  / LAREDO', 'revenue': 131.25}, {'customer': 'COLEY ELECTRIC/DOUGLAS', 'revenue': 119.75}, {'customer': 'Southern Lighting LLC', 'revenue': 119.75}] | [{'item': '6805-6SF BLK-MBR', 'desc': 'Golden Lighting Everly 6-light Semi-Flush Mount in Matte Black and Modern Black Rattan shade', 'available': 217}, {'item': '6805-6 BLK-MBR', 'desc': 'Golden Lighting Everly 6-light Chandelier in Matte Black and Modern Black Rattan shade', 'available': 158}, {'item': '6805-4 BLK-NR', 'desc': 'Golden Lighting Everly 4-light Pendant in Matte Black and Natural Rattan shade', 'available': 57}, {'item': '6805-4SF BLK-NR', 'desc': 'Golden Lighting Everly 4-light Semi-Flush Mount in Matte Black and Natural Rattan shade', 'available': 57}, {'item': '6805-4 BLK-MBR', 'desc': 'Golden Lighting Everly 4-light Pendant in Matte Black and Modern Black Rattan shade', 'available': 19}, {'item': '6805-4SF BLK-MBR', 'desc': 'Golden Lighting Everly 4-light Semi-Flush Mount in Matte Black and Modern Black Rattan shade', 'available': 19}] |
| 9903-6 MG | Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Mystic Gold | 9903 | 41,930.25 | 67 | — | 2026-07-20 | [{'customer': 'Concept Lighting Group / Oakville', 'revenue': 1621.69}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 1569.38}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 1395.0}, {'customer': 'TAP LIGHTING', 'revenue': 1395.0}, {'customer': 'LIGHTING AND BULBS UNLIMITED', 'revenue': 1395.0}, {'customer': 'SPOTLIGHT DESIGN CENTER', 'revenue': 1395.0}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 1297.36}, {'customer': 'THE LITE COMPANY', 'revenue': 1272.63}, {'customer': 'FINISHING TOUCHES', 'revenue': 1220.63}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 1116.0}, {'customer': 'BURGESS LIGHTING / FORRESTVILLE', 'revenue': 1046.26}, {'customer': 'THE LIGHTING WAREHOUSE/ RICHMOND', 'revenue': 899.4}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 871.88}, {'customer': 'KINGSTON LIGHTING AKA MCCAFFERTY NEIL B ELECTRIC COMPANY LTD', 'revenue': 784.69}, {'customer': 'Light Store USA', 'revenue': 749.5}, {'customer': None, 'revenue': 749.5}, {'customer': 'SHALLOTTE ELECTRIC', 'revenue': 749.5}, {'customer': 'WILSON LIGHTING/ OVERLAND PARK', 'revenue': 697.5}, {'customer': 'FERGUSON ENTERPRISES #13/ KNOXVILLE', 'revenue': 697.5}, {'customer': 'FERGUSON ENTERPRISES #107 / ALPHARETTA', 'revenue': 697.5}, {'customer': 'FERGUSON ENTERPRISES / BROOKSHIRE 2812', 'revenue': 697.5}, {'customer': 'HARRY HORN INC dba Arch Street Lighting', 'revenue': 697.5}, {'customer': 'INLINE ELECTRIC/ PELHAM', 'revenue': 697.5}, {'customer': 'LAMPS EXPO / LOS ANGELES', 'revenue': 697.5}, {'customer': 'LIGHTING EXPO / FREEHOLD', 'revenue': 697.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 697.5}, {'customer': 'LIGHTING PLUS / HOUSTON', 'revenue': 697.5}, {'customer': 'LIGHTING FIRST/ FORT MYERS', 'revenue': 697.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 697.5}, {'customer': 'PASSION LIGHTING', 'revenue': 697.5}, {'customer': 'PEMBA LIGHTING', 'revenue': 697.5}, {'customer': 'ROYCE COLLECTION / REDFORD', 'revenue': 697.5}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 697.5}, {'customer': 'UNIVERSAL LIGHTS/ STAFFORD', 'revenue': 697.5}, {'customer': 'WILSON LIGHTING OF NAPLES', 'revenue': 697.5}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 648.68}, {'customer': 'SISTERS LIGHTING dba ANTHOLOGY LIGHTING / TEXAS', 'revenue': 558.0}, {'customer': 'EUROPA INTERIORS AND GIFTS LLC', 'revenue': 558.0}, {'customer': 'LIGHTING FIRST OF FLORIDA/ BONITA SPG', 'revenue': 558.0}, {'customer': 'INTERSTATE SUPPLY, INC. / LAKE CITY', 'revenue': 558.0}, {'customer': 'Distinctive Lighting / Bozeman', 'revenue': 558.0}, {'customer': 'EDWARD JOY ELECTRIC, LLC', 'revenue': 558.0}, {'customer': 'Dupage Lighting Inc.', 'revenue': 558.0}, {'customer': 'FERGUSON ENTERPRISE #3031/ SPOKANE WA', 'revenue': 558.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 523.13}, {'customer': 'JUST LIGHTS  INC', 'revenue': 523.13}, {'customer': 'ONE STOP LIGHTING / THOUSAND OAKS', 'revenue': 523.13}, {'customer': 'HELEN PITEO INTERIORS LLC.', 'revenue': 523.13}, {'customer': 'KRELL LIGHTING', 'revenue': 523.13}, {'customer': 'Light N Leisure', 'revenue': 374.75}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 348.75}, {'customer': 'ELEKTRA LIGHTS & FANS', 'revenue': 348.75}, {'customer': 'JACOBSON ELECTRIC', 'revenue': 348.75}, {'customer': 'BURNS ELECTRIC INC', 'revenue': 348.75}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 348.75}] | [{'item': '9903-WSC MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 2-light Wall Sconce in Mystic Gold', 'available': 34}, {'item': '9903-6 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 6-light Chandelier in Black Iron', 'available': 24}, {'item': '9903-24 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 24-light Chandelier in Black Iron', 'available': 10}, {'item': '9903-18 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Black Iron', 'available': 7}, {'item': '9903-18 MG', 'desc': 'Ziva by Golden Lighting Autumn Twilight 18-light Chandelier in Mystic Gold', 'available': 5}, {'item': '9903-12 BI', 'desc': 'Ziva by Golden Lighting Autumn Twilight 12-light Chandelier in Black Iron', 'available': 2}] |
| 6937-M BLK-NR | Golden Lighting Valentina 1-light Pendant in Matte Black | 6937 | 41,560.87 | 545 | — | 2026-07-13 | [{'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 17315.1}, {'customer': 'ONE SOURCE LIGHTING / BILLINGS', 'revenue': 3349.5}, {'customer': 'MATHES OF ALABAMA ELECTRIC SUPPLY CO., INC.', 'revenue': 1880.0}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 1108.0}, {'customer': 'FERGUSON ENTERPRISES #0088  / TULSA', 'revenue': 715.5}, {'customer': None, 'revenue': 643.95}, {'customer': 'FERGUSON ENTERPRISES #230/ OKLAHOMA CITY', 'revenue': 636.0}, {'customer': 'PRESTIGE LIGHTING AND DESIGN', 'revenue': 567.0}, {'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 420.5}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 407.5}, {'customer': 'FERGUSON ENTERPRISES #1020 / WEST ALLIS', 'revenue': 395.5}, {'customer': 'HYE LIGHTING CO.', 'revenue': 387.5}, {'customer': 'STEADFAST LIGHTING - SPRINGDALE, AR', 'revenue': 326.0}, {'customer': 'Lighting Emporium / Springdale', 'revenue': 318.0}, {'customer': 'APPLICO, LLC/ TUSCALOOSA', 'revenue': 318.0}, {'customer': 'WHITE STAR SUPPLY LLC / WAYCROSS 1', 'revenue': 310.0}, {'customer': 'WHITE STAR SUPPLY LLC / BRUNSWICK 2', 'revenue': 289.2}, {'customer': 'DECO LUMINAIRE INC. / TERREBONNE', 'revenue': 285.19}, {'customer': 'Lyteworks', 'revenue': 283.5}, {'customer': 'RANDOLPH LIGHTING', 'revenue': 283.5}, {'customer': 'FERGUSON ENTERPRISES #499/ CHARLOTTESVILLE', 'revenue': 283.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 255.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 244.5}, {'customer': 'RICHARDS LIGHTING/ HUNTSVILLE', 'revenue': 244.5}, {'customer': 'ONE STOP LIGHTING / THOUSAND OAKS', 'revenue': 244.5}, {'customer': 'FERGUSON ENTERPRISES #253/ PENSACOLA', 'revenue': 244.5}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 240.5}, {'customer': 'FERGUSON ENTERPRISE #3031/ SPOKANE WA', 'revenue': 238.5}, {'customer': 'FERGUSON / COLUMBUS OH 1589 2828', 'revenue': 238.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 238.5}, {'customer': 'NOVA LIGHTING dba HANSEN LIGHTING INC', 'revenue': 238.5}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 238.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 238.5}, {'customer': 'DOMINION ELECTRIC SUPPLY/ CHANTILLY', 'revenue': 238.5}, {'customer': 'LIGHTING CONCEPTS & DESIGN', 'revenue': 238.5}, {'customer': 'VENICE LIGHTING COMPANY/ NOKOMIS', 'revenue': 232.5}, {'customer': 'METRO APPLIANCES & MORE/OKL CITY', 'revenue': 232.5}, {'customer': 'UNIQUE LIGHTING/ SASKATOON', 'revenue': 212.62}, {'customer': 'ROBINSON LIGHTING/ KELOWNA', 'revenue': 212.62}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 198.75}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 195.75}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 189.0}, {'customer': 'HELSEL-JEPPERSON', 'revenue': 189.0}, {'customer': 'Illuminations Lighting Inc dba Illimunations', 'revenue': 189.0}, {'customer': 'Ferguson Enterprises #476 / Valleyview OH', 'revenue': 189.0}, {'customer': 'NORTH COAST ELECTRIC / KENT / AUBURN', 'revenue': 189.0}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 189.0}, {'customer': 'FLINZ HOLDINGS LLC dba THE GALLERY OF LIGHTS / LONGVIEW', 'revenue': 170.1}, {'customer': 'GREER LIGHTING CENTER', 'revenue': 163.0}, {'customer': "HILL'S LIGHTING/ BONITA SPRINGS", 'revenue': 163.0}, {'customer': 'FERGUSON ENTERPRISES #2635 / ENGLEWOOD', 'revenue': 163.0}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 163.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 159.0}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES /DES MOINES #522 / CLIVE#226', 'revenue': 159.0}, {'customer': 'Ferguson Enterprises #52/ Orlando', 'revenue': 159.0}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 159.0}, {'customer': 'LIGHTING CONNECTION / BUDA', 'revenue': 159.0}, {'customer': 'ARIZONA LIGHTING COMPANY/ YUMA', 'revenue': 159.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 159.0}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES / HOLLY SPRINGS 1723', 'revenue': 159.0}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 159.0}, {'customer': 'TOUCH OF CLASS', 'revenue': 159.0}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 155.0}, {'customer': 'AMERICAN LIGHTING / KNOXVILLE', 'revenue': 155.0}, {'customer': 'BLYTHE INTERIORS', 'revenue': 155.0}, {'customer': 'RACHELS LIGHTING / PANAMA CITY', 'revenue': 155.0}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 155.0}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 147.88}, {'customer': 'Royaume Luminaire / St. Basile', 'revenue': 127.14}, {'customer': 'SAVE MORE LIGHTING LTD', 'revenue': 97.8}, {'customer': 'Mountainhigh Designs Inc', 'revenue': 94.5}, {'customer': 'EAST VALLEY FANS & BLINDS / MESA', 'revenue': 94.5}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 93.62}, {'customer': 'ROYAUME LUMINAIRE/ SAINTE-JULIE', 'revenue': 93.62}, {'customer': 'ROYAUME LUMINAIRE/ TERREBONNE', 'revenue': 93.62}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 81.5}, {'customer': 'JUST LIGHTS  INC', 'revenue': 81.5}, {'customer': 'FERGUSON ENTERPRISES #3055 / IDAHO FALLS', 'revenue': 81.5}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 79.5}, {'customer': 'FLA LIGHTING INC. dba LIGHTING DEPOT', 'revenue': 79.5}, {'customer': 'FERGUSON ENTERPRISES #454/ SAN ANTONIO', 'revenue': 79.5}, {'customer': 'FUSION LIGHT AND DESIGN dba IMAGE COMPLETE', 'revenue': 77.5}, {'customer': 'CED dba ALL-PHASE ELECTRIC', 'revenue': 77.5}, {'customer': None, 'revenue': 77.5}, {'customer': 'ROYAUME LUMINAIRE/ DRUMMONDVILLE', 'revenue': 44.72}, {'customer': 'ROYAUME LUMINAIRE/ TROIS RIVIERES', 'revenue': 44.72}, {'customer': 'ROYAUME LUMINAIRE/ SHERBROOKE', 'revenue': 44.72}, {'customer': 'SANDERS LIGHTING CO', 'revenue': 39.75}] | [{'item': '6937-4P BLK-NR', 'desc': 'Golden Lighting Valentina 4-light Pendant in Matte Black and Natural Raphia Rope shade', 'available': 1}] |
| 1270-13 BLK | Wry Lighting Morgon 2-light 13" Flush Mount in Matte Black and Opal Glass | 1270 | 41,544.30 | 1,010 | — | 2026-07-20 | [{'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 13507.0}, {'customer': 'AMC LIGHTING & DECOR/ RALEIGH', 'revenue': 5487.8}, {'customer': 'CLW', 'revenue': 2917.36}, {'customer': 'MCI INC dba  MCI LIGHTING ONE / WAITE PARK', 'revenue': 2719.5}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 2358.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 1444.5}, {'customer': 'EP LIGHTING LLC', 'revenue': 1190.0}, {'customer': 'VALLEY LIGHTS INC / FARGO', 'revenue': 1189.5}, {'customer': 'MCNALLY ELECTRIC', 'revenue': 870.0}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 825.5}, {'customer': 'FERGUSON ENTERPRISES / HOLLY SPRINGS 1723', 'revenue': 765.0}, {'customer': 'FERGUSON ENTERPRISES #16/ GREENSBORO', 'revenue': 722.5}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 554.5}, {'customer': 'FERGUSON ENTERPRISES #1550/ ADDISON IL', 'revenue': 445.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 437.0}, {'customer': 'URBAN LIGHTS', 'revenue': 425.0}, {'customer': 'METRO ELECTRIC SUPPLY/ ST LOUIS/ BRENTWOOD', 'revenue': 365.0}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 344.0}, {'customer': 'PRESTIGE LIGHTING/ LANSING', 'revenue': 343.1}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 301.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 285.0}, {'customer': 'INSIDE SOURCE, LLC/ FRISCO', 'revenue': 273.0}, {'customer': 'FERGUSON ENTERPRISES #34/ CHARLOTTE', 'revenue': 255.0}, {'customer': 'STARLIGHT LIGHTING CENTRE - DROP SHIP (US)', 'revenue': 222.5}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 222.5}, {'customer': 'GALAXIE LIGHTING dba LIGHTINGUTAH.COM', 'revenue': 222.5}, {'customer': 'LIGHT SOURCE LIGHTING/ PLAINFIELD', 'revenue': 218.5}, {'customer': 'JUST LIGHTS  INC', 'revenue': 216.5}, {'customer': 'BLANCS DE BLANCS 2021 INC', 'revenue': 185.23}, {'customer': 'CRESCENT LIGHTING SUPPLY/KIRKLAND', 'revenue': 178.0}, {'customer': 'FERGUSON ENTERPRISES #215 / LENEXA', 'revenue': 178.0}, {'customer': 'FERGUSON ENTERPRISES #2009-#1657 / GOLDEN VALLEY', 'revenue': 178.0}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 170.0}, {'customer': 'At Home Lighting / Home Lighting / Colorado Springs', 'revenue': 170.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 170.0}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 133.5}, {'customer': 'FERGUSON ENTERPRISES / 1599 2820 PITTSBURGH', 'revenue': 89.0}, {'customer': 'CREATIVE LIGHTING/ ST. PAUL', 'revenue': 89.0}, {'customer': 'CLEVELAND LIGHTING / LYNDHURST', 'revenue': 85.0}, {'customer': 'MADISON CREEK FURNISHINGS /  MISSOULA', 'revenue': 85.0}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 85.0}, {'customer': 'ADVANCE ELECTRIC INC/ GAYLORD', 'revenue': 85.0}, {'customer': 'SIGNATURE LIGHTING AND FANS', 'revenue': 51.0}, {'customer': 'THE ELECTRICAL & PLUMBING STORE / GLOUCESTER', 'revenue': 47.81}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 44.5}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 44.5}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 44.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 44.5}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 44.5}, {'customer': 'Raymond De Steiger/ Ray Lighting Center', 'revenue': 44.5}, {'customer': 'STUDIO H2O / PSC DISTRIBUTION / IOWA CITY', 'revenue': 42.5}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 42.5}, {'customer': 'Better Living Store', 'revenue': 42.5}, {'customer': 'BRIGHT IDEAS DBA HALEY LIGHTING', 'revenue': 42.5}] | [{'item': '1270-13 CH', 'desc': 'Wry Lighting Morgon 2-light Flush Mount in Chrome', 'available': 95}, {'item': '1270-09 BLK', 'desc': 'Wry Lighting Morgon 1-light Flush Mount in Matte Black', 'available': 57}, {'item': '1270-09 PW', 'desc': 'Wry Lighting Morgon 1-light Flush Mount in Pewter', 'available': 22}, {'item': '1270-11 PW', 'desc': 'Wry Lighting Morgon 2-light 11" Flush Mount in Pewter and Opal Glass', 'available': 20}] |
| 6950-L MBS | Golden Lighting Shepard 1-light Pendant in Modern Brass and Modern Brass shade | 6950 | 34,833.82 | 285 | — | 2026-07-20 | [{'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 1361.5}, {'customer': 'BRECHER LIGHTING / LOUISVILLE', 'revenue': 1311.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 1017.0}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 980.0}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 922.5}, {'customer': 'BRAZORIA COUNTY LIGHTING INC', 'revenue': 901.5}, {'customer': 'Springfield Electric Supply / Champaign', 'revenue': 871.5}, {'customer': 'RECLAIMED WAREHOUSE', 'revenue': 742.0}, {'customer': 'FERGUSON ENTERPRISES #61 EULESS & #66 LEWISVILLE', 'revenue': 687.5}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 687.5}, {'customer': 'PREMIER LIGHTING/ BAKERSFIELD', 'revenue': 679.5}, {'customer': 'LAMPS EXPO / LOS ANGELES', 'revenue': 647.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY / BARRINGTON', 'revenue': 612.5}, {'customer': 'RIVER CITIES LIGHTING', 'revenue': 550.0}, {'customer': 'The Lite House / Columbia', 'revenue': 520.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 518.0}, {'customer': 'FERGUSON ENTERPRISES / CHANTILLY #001', 'revenue': 504.0}, {'customer': 'SANDERS LIGHTING CO', 'revenue': 504.0}, {'customer': 'FERGUSON ENTERPRISES / RICHMOND 5', 'revenue': 497.0}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 490.0}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 443.25}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 435.75}, {'customer': "CAROL'S LIGHTING & FAN SHOP/ HUMBLE", 'revenue': 412.5}, {'customer': 'JOHN WARD INTERIORS AND GIFTS', 'revenue': 404.5}, {'customer': 'FERGUSON ENTERPRISES #1550/ ADDISON IL', 'revenue': 388.5}, {'customer': 'BRIGHT CITY LIGHTS', 'revenue': 388.5}, {'customer': 'BLACK DIAMOND ACQUISITIONS  dba ALLOWAY LIGHTING CO', 'revenue': 388.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 388.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 388.5}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 381.5}, {'customer': 'VILLAGE MAYTAG DBA VILLAGE HOME STORES', 'revenue': 374.5}, {'customer': 'NOVA LIGHTING dba HANSEN LIGHTING INC', 'revenue': 367.5}, {'customer': 'Hortons Home Lighting / LaGrange', 'revenue': 367.5}, {'customer': 'Bayside Electric Supply', 'revenue': 367.5}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 367.5}, {'customer': 'REXEL USA/TECHE ELECTRIC/ LAFAYETTE', 'revenue': 367.5}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 320.25}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 309.75}, {'customer': 'HOBRECHT LIGHTING', 'revenue': 275.0}, {'customer': None, 'revenue': 275.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': 275.0}, {'customer': 'BIGGINS LIGHTING', 'revenue': 275.0}, {'customer': 'LIGHTS OF OCONEE', 'revenue': 275.0}, {'customer': 'MAGNOLIA LIGHTING', 'revenue': 275.0}, {'customer': 'WASATCH LIGHTING INC', 'revenue': 275.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 275.0}, {'customer': 'TURN ON LIGHTING / RIO RANCHO', 'revenue': 259.0}, {'customer': 'COBURN SUPPLY COMPANY INC / #3 LAKE CHARLES', 'revenue': 259.0}, {'customer': 'FERGUSON ENTERPRISES / #12 NORFOLK', 'revenue': 259.0}, {'customer': 'MCMANUS COMPANY', 'revenue': 259.0}, {'customer': 'NORTH COAST LIGHTING, LLC', 'revenue': 259.0}, {'customer': 'MARTINEZ PROPERTY GROUP LLC DBA ONE SOURCE LIGHTING', 'revenue': 259.0}, {'customer': 'Stokes Electrical Supply Co, Inc.', 'revenue': 259.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 252.0}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 245.0}, {'customer': 'SISTERS LIGHTING dba ANTHOLOGY LIGHTING / TEXAS', 'revenue': 245.0}, {'customer': 'LIGHTING SPECIALISTS / MIDVALE', 'revenue': 245.0}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 245.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 245.0}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 245.0}, {'customer': 'SUNBELT LIGHTING LLC / LAFAYETTE', 'revenue': 245.0}, {'customer': 'Ferguson Enterprises #1869 / Round Rock', 'revenue': 245.0}, {'customer': 'FERGUSON ENTERPRISES #118/ MURFREESBORO', 'revenue': 245.0}, {'customer': 'PROSOURCE SUPPLY / EASLEY', 'revenue': 245.0}, {'customer': 'FERGUSON ENTERPRISES / POMONA 603', 'revenue': 245.0}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 245.0}, {'customer': 'Legacy Lighting, LLC', 'revenue': 245.0}, {'customer': 'INLINE ELECTRIC #11 / ATHENS', 'revenue': 245.0}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 232.76}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 190.75}, {'customer': 'AUSTELL LIGHTING', 'revenue': 183.75}, {'customer': 'SAVE MORE LIGHTING LTD', 'revenue': 155.4}, {'customer': 'Mountainhigh Designs Inc', 'revenue': 155.4}, {'customer': 'SIGNATURE LIGHTING AND FANS', 'revenue': 137.81}, {'customer': 'WILSON LIGHTING/ OVERLAND PARK', 'revenue': 137.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 137.5}, {'customer': 'GREENBRIER LIGHTING AT HILLTOP DBA CJ & H LIGHTING INC', 'revenue': 137.5}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 137.5}, {'customer': 'NORTHERN LIGHTS UNLIMITED/ BELVIDERE', 'revenue': 137.5}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 129.5}, {'customer': 'WT LIGHTING', 'revenue': 129.5}, {'customer': 'THE PLUMBING WAREHOUSE - LCR / LAFAYETTE', 'revenue': 129.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 129.5}, {'customer': 'Ferguson Enterprises #540 / Baton Rouge', 'revenue': 129.5}, {'customer': 'TEAM ELECTRIC SUPPLY', 'revenue': 129.5}, {'customer': 'SMALL TOWN HOME & DECOR', 'revenue': 129.5}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 129.5}, {'customer': 'CREATIVE LIGHTING/ ST. PAUL', 'revenue': 129.5}, {'customer': 'HOME LIGHTING/ MALVERN', 'revenue': 129.5}, {'customer': 'WOLFE LIGHTING & ACCENTS / REXBURG', 'revenue': 129.5}, {'customer': 'STUDIO H2O / PSC DISTRIBUTION / IOWA CITY', 'revenue': 122.5}, {'customer': 'Ferguson Enterprises #52/ Orlando', 'revenue': 122.5}, {'customer': 'MATHES OF ALABAMA ELECTRIC SUPPLY CO., INC.', 'revenue': 122.5}, {'customer': 'ARMITAGE INTERIORS', 'revenue': 122.5}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 122.5}, {'customer': 'RANDOLPH LIGHTING', 'revenue': 122.5}, {'customer': 'BES LIGHTING/ RAPID CITY', 'revenue': 122.5}, {'customer': 'FINISHING TOUCHES', 'revenue': 122.5}, {'customer': 'ROYAUME LUMINAIRE/ TROIS RIVIERES', 'revenue': 77.7}, {'customer': 'TWIN BRIDGE LIGHTING', 'revenue': 72.84}, {'customer': 'STAGGS CARPETS & INTERIORS dba STAGGS INTERIORS', 'revenue': 68.91}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 68.75}, {'customer': 'LUMINAIRES LTD / WILLMAR', 'revenue': 68.75}, {'customer': None, 'revenue': 68.75}, {'customer': 'INLINE ELECTRIC / CHATTANOOGA #12', 'revenue': 68.75}, {'customer': 'CLIFTON AND COMPANY', 'revenue': 64.75}, {'customer': 'COLEY ELECTRIC/DOUGLAS', 'revenue': 64.75}, {'customer': "NANCY B'S HOUSE OF LIGHTS LLC / CHARLOTTESVILLE", 'revenue': 64.75}, {'customer': 'DEKKER LIGHTING', 'revenue': 64.75}, {'customer': 'MAYER ELECTRIC SUPPLY/ PELHAM', 'revenue': 64.75}, {'customer': 'VALENCIA LIGHTING & DESIGN / SANTA CLARITA', 'revenue': 61.25}, {'customer': 'PROSOURCE / GREENVILLE', 'revenue': 61.25}, {'customer': 'BURR RIDGE LIGHTING', 'revenue': 61.25}, {'customer': 'ILLUMINATE LIGHTING', 'revenue': 61.25}, {'customer': 'Coffman Home Decor LLC', 'revenue': 61.25}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 0.0}] | [{'item': '6950-1W MBS-WHT', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Matte White shade', 'available': 56}, {'item': '6950-1W MBS-BLK', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Matte Black shade', 'available': 56}, {'item': '6950-BA2 MBS-BLK', 'desc': 'Golden Lighting Shepard 2-light Vanity in Modern Brass and Matte Black shade', 'available': 39}, {'item': '6950-BA2 MBS-WHT', 'desc': 'Golden Lighting Shepard 2-light Vanity in Modern Brass and Matte White shade', 'available': 38}, {'item': '6950-FM MBS-WHT', 'desc': 'Golden Lighting Shepard 3-light Flush Mount in Modern Brass and Matte White shade', 'available': 38}, {'item': '6950-1W MBS-RC', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Russet Clay shade', 'available': 37}, {'item': '6950-L MBS-WHT', 'desc': 'Golden Lighting Shepard 1-light Pendant in Modern Brass and Matte White shade', 'available': 36}, {'item': '6950-L MBS-RC', 'desc': 'Golden Lighting Shepard 1-light Pendant in Modern Brass and Russet Clay shade', 'available': 34}, {'item': '6950-FM MBS-RC', 'desc': 'Golden Lighting Shepard 3-light Flush Mount in Modern Brass and Russet Clay shade', 'available': 32}, {'item': '6950-BA3 MBS-MBS', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Modern Brass shade', 'available': 24}, {'item': '6950-BA2 MBS-RC', 'desc': 'Golden Lighting Shepard 2-light Vanity in Modern Brass and Russet Clay shade', 'available': 19}, {'item': '6950-FM MBS-BLK', 'desc': 'Golden Lighting Shepard 3-light Flush Mount in Modern Brass and Matte Black shade', 'available': 13}, {'item': '6950-1W MBS-MBS', 'desc': 'Golden Lighting Shepard 1-light Wall Sconce in Modern Brass and Modern Brass shade', 'available': 9}, {'item': '6950-L MBS-BLK', 'desc': 'Golden Lighting Shepard 1-light Pendant in Modern Brass and Matte Black shade', 'available': 7}, {'item': '6950-BA3 MBS-WHT', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Matte White shade', 'available': 4}, {'item': '6950-BA3 MBS-BLK', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Matte Black shade', 'available': 3}, {'item': '6950-BA3 MBS-RC', 'desc': 'Golden Lighting Shepard 3-light Vanity in Modern Brass and Russet Clay shade', 'available': 3}] |
| 7312-L CP | Golden Lighting Bartlett 2-light Pendant in Copper Patina | 7312 | 32,868.59 | 307 | — | 2026-07-20 | [{'customer': None, 'revenue': 15327.3}, {'customer': 'CITY LIGHTZ / ST CATHARINES', 'revenue': 2463.8}, {'customer': 'Gem Sales & Marketing / Joe Miotto', 'revenue': 1971.0}, {'customer': 'LIGHTING WORLD / STATEN ISLAND SHOWROOM', 'revenue': 1505.0}, {'customer': 'TEXAS BRIGHT IDEAS/ GEORGETOWN', 'revenue': 1290.0}, {'customer': 'THE ELECTRICAL & PLUMBING STORE / GLOUCESTER', 'revenue': 1075.52}, {'customer': 'Georgia Lighting', 'revenue': 541.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 444.0}, {'customer': 'NOVA LIGHTING dba HANSEN LIGHTING INC', 'revenue': 438.0}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 337.5}, {'customer': 'BRIGHT CITY LIGHTS', 'revenue': 337.5}, {'customer': 'Brandon Lighting / MS', 'revenue': 337.5}, {'customer': 'J & B SUPPLY INC / FORT SMITH', 'revenue': 337.5}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 337.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 328.5}, {'customer': 'CHAMPLAIN VALLEY ELECTRIC SUPPLY COMPANY, INC.', 'revenue': 328.5}, {'customer': None, 'revenue': 328.5}, {'customer': 'FERGUSON ENTERPRISES / #1334 JACKSONVILLE', 'revenue': 322.5}, {'customer': 'Capitol Lighting Gallery / Raleigh', 'revenue': 313.89}, {'customer': 'KINGSTON LIGHTING AKA MCCAFFERTY NEIL B ELECTRIC COMPANY LTD', 'revenue': 270.0}, {'customer': 'RICHARDSON LIGHTING/ SASKATOON', 'revenue': 246.38}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 246.38}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 225.0}, {'customer': 'SOUTHERN LIGHTING/WARNER ROBINS', 'revenue': 225.0}, {'customer': None, 'revenue': 225.0}, {'customer': None, 'revenue': 219.0}, {'customer': 'Cline-Holder Electric Supply, Inc / Elizabethton', 'revenue': 219.0}, {'customer': 'FERGUSON ENTERPRISES / #0245 / AUSTIN', 'revenue': 219.0}, {'customer': 'MCNALLY ELECTRIC', 'revenue': 219.0}, {'customer': 'PROGRESSIVE LIGHTING INC #05 / LEE LIGHTING / ROSWELL', 'revenue': 219.0}, {'customer': 'RIVER CITIES LIGHTING', 'revenue': 219.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 219.0}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 215.0}, {'customer': 'ELLEN LIGHTING/ STAFFORD', 'revenue': 215.0}, {'customer': 'ADVANCE ELECTRIC INC/ GAYLORD', 'revenue': 215.0}, {'customer': 'MAPLE RIDGE LIGHTING', 'revenue': 123.19}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 112.5}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 112.5}, {'customer': 'URBAN LIGHTS', 'revenue': 112.5}, {'customer': 'Home And Light Valdosta', 'revenue': 109.5}, {'customer': 'The Cabinet Corner, Inc', 'revenue': 107.5}, {'customer': 'RACHELS LIGHTING / PANAMA CITY', 'revenue': 107.5}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 102.13}] | [{'item': '7312-SF BP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Black Patina', 'available': 59}, {'item': '7312-S CP', 'desc': 'Golden Lighting Bartlett 1-light Pendant in Copper Patina', 'available': 52}, {'item': '7312-BA1 BP', 'desc': 'Golden Lighting Bartlett 1-light Vanity in Black Patina', 'available': 33}, {'item': '7312-SF FW', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in French White', 'available': 30}, {'item': '7312-SF CP', 'desc': 'Golden Lighting Bartlett 2-light Semi-Flush Mount in Copper Patina', 'available': 27}, {'item': '7312-BA1 FW', 'desc': 'Golden Lighting Bartlett 1-light Vanity in French White', 'available': 19}, {'item': '7312-FM CP', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in Copper Patina', 'available': 15}, {'item': '7312-L FW', 'desc': 'Golden Lighting Bartlett 2-light Pendant in French White', 'available': 11}, {'item': '7312-1W CP', 'desc': 'Golden Lighting Bartlett 1-light Wall Sconce in Copper Patina', 'available': 10}, {'item': '7312-FM FW', 'desc': 'Golden Lighting Bartlett 2-light Flush Mount in French White', 'available': 5}, {'item': '7312-BA3 FW', 'desc': 'Golden Lighting Bartlett 3-light Vanity in French White', 'available': 5}, {'item': '7312-BA2 FW', 'desc': 'Golden Lighting Bartlett 2-light Vanity in French White', 'available': 5}, {'item': '7312-BA3 CP', 'desc': 'Golden Lighting Bartlett 3-light Vanity in Copper Patina', 'available': 4}, {'item': '7312-FM16 BP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Black Patina', 'available': 3}, {'item': '7312-FM16 FW', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in French White', 'available': 3}, {'item': '7312-S FW', 'desc': 'Golden Lighting Bartlett 1-light Pendant in French White', 'available': 3}, {'item': '7312-BA2 BP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Black Patina', 'available': 2}, {'item': '7312-BA2 CP', 'desc': 'Golden Lighting Bartlett 2-light Vanity in Copper Patina', 'available': 2}, {'item': '7312-FM16 CP', 'desc': 'Golden Lighting Bartlett 3-light Flush Mount in Copper Patina', 'available': 1}] |
| 6070-LP BLK-BLK | Golden Lighting Tribeca 5-light Island Light in Matte Black | 6070 | 32,605.78 | 165 | — | 2026-08-06 | [{'customer': 'JUST LIGHTS  INC', 'revenue': 2382.0}, {'customer': 'FERGUSON ENTERPRISES / 2715/ 226/ 228 / OMAHA', 'revenue': 1767.5}, {'customer': 'Sunbelt Lighting LLC / Baton Rouge', 'revenue': 1529.0}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 1484.61}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 1153.0}, {'customer': 'ILLUMINATING EXPRESSIONS / EVANSVILLE IN', 'revenue': 838.0}, {'customer': 'MID-COUNTY LIGHTING SHOWROOM & ELECTRICAL SUPPLIES', 'revenue': 794.0}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 764.0}, {'customer': 'ILLUMINATIONS/ LINCOLN', 'revenue': 764.0}, {'customer': 'MAHLANDERS INC / SIOUX FALLS', 'revenue': 751.55}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 682.32}, {'customer': "PREMIER LIGHTING/ LEE'S SUMMIT", 'revenue': 628.5}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 606.5}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 606.5}, {'customer': 'BRIGHT IDEAS DBA HALEY LIGHTING', 'revenue': 598.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 584.5}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 584.5}, {'customer': 'WILSON LIGHTING/ OVERLAND PARK', 'revenue': 576.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 562.5}, {'customer': 'SIGNATURE LIGHTING AND FANS', 'revenue': 471.38}, {'customer': 'FERGUSON ENTERPRISES #1117/ SPRINGDALE', 'revenue': 419.0}, {'customer': 'ILLUMINATE LIGHTING', 'revenue': 397.0}, {'customer': 'PARAMONT-EO/ NEW LENOX', 'revenue': 397.0}, {'customer': 'DEALERS ELECTRICAL SUPPLY / GREENVILLE', 'revenue': 389.0}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 382.0}, {'customer': 'The Lighting Design Co / Layton', 'revenue': 382.0}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 382.0}, {'customer': 'LIGHTING ETC / N RICHLAND HILLS', 'revenue': 375.0}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 375.0}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 375.0}, {'customer': 'BRECHER LIGHTING / LEXINGTON', 'revenue': 375.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 375.0}, {'customer': 'SUPER-LITE LIGHTING LTD', 'revenue': 235.69}, {'customer': 'TWIN BRIDGE LIGHTING', 'revenue': 235.69}, {'customer': 'THE ELECTRICAL & PLUMBING STORE / GLOUCESTER', 'revenue': 210.94}, {'customer': 'RICHARDSON LIGHTING/ REGINA', 'revenue': 210.94}, {'customer': 'PACE LIGHTING', 'revenue': 209.5}, {'customer': 'COURT STREET LIGHTING', 'revenue': 209.5}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 209.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 209.5}, {'customer': 'KING ELECTRIC', 'revenue': 209.5}, {'customer': 'LIGHTING WORLD INC/OMAHA', 'revenue': 209.5}, {'customer': 'LIGHT BRITE/ TRENTON', 'revenue': 209.5}, {'customer': 'Luxur Lighting / Cedar City', 'revenue': 209.5}, {'customer': 'NORTHERN LIGHTS & FANS / LAS VEGAS', 'revenue': 209.5}, {'customer': 'TEXAS BRIGHT IDEAS/ GEORGETOWN', 'revenue': 209.5}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 209.5}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 199.03}, {'customer': 'COLONIAL ELECTRIC SUPPLY COMPANY / KING OF PRUSSIA', 'revenue': 194.5}, {'customer': 'CLEVELAND LIGHTING / LYNDHURST', 'revenue': 194.5}, {'customer': 'CARAVELLE LIGHTING', 'revenue': 194.5}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 194.5}, {'customer': 'VILLAGE LIGHTING AND SUPPLY/ LORAIN', 'revenue': 194.5}, {'customer': 'MARTINEZ PROPERTY GROUP LLC DBA ONE SOURCE LIGHTING', 'revenue': 194.5}, {'customer': 'BRIGHT IDEAS dba THE LAMP SHOP', 'revenue': 194.5}, {'customer': 'FERGUSON ENTERPRISE #3031/ SPOKANE WA', 'revenue': 194.5}, {'customer': 'HOME LIGHTING/ MALVERN', 'revenue': 194.5}, {'customer': 'KENDALL ELECTRIC / GRAND RAPIDS', 'revenue': 194.5}, {'customer': 'FERGUSON ENTERPRISES #43/ GREENVILLE SC', 'revenue': 194.5}, {'customer': 'WT LIGHTING', 'revenue': 194.5}, {'customer': 'Home And Light Valdosta', 'revenue': 194.5}, {'customer': 'Heritage Lighting', 'revenue': 187.5}, {'customer': 'Tuthill Lighting Design', 'revenue': 187.5}, {'customer': 'BRICK + LINEN', 'revenue': 187.5}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 187.5}, {'customer': 'House of Lights / Mayfield HTS', 'revenue': 187.5}, {'customer': 'MAYNARDS ELECTRIC / ROCHESTER', 'revenue': 187.5}, {'customer': 'NAPLES BULB INC/ LIGHT BULBS UNLIMITED', 'revenue': 187.5}, {'customer': 'Georgia Lighting', 'revenue': 187.5}, {'customer': 'MINNESOTA LIGHTING', 'revenue': 187.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 187.5}, {'customer': 'FERGUSON ENTERPRISES #216/ WICHITA', 'revenue': 187.5}, {'customer': 'EAST VALLEY FANS & BLINDS / MESA', 'revenue': 187.5}, {'customer': 'ANZALONE ELECTRIC INC.', 'revenue': 187.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 187.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 187.5}, {'customer': 'DESIGNERS MART / EL PASO', 'revenue': 187.5}, {'customer': 'TEXAS BRIGHT IDEAS/ HARKER HEIGHTS', 'revenue': 187.5}, {'customer': 'REXEL USA/TECHE ELECTRIC/ LAFAYETTE', 'revenue': 187.5}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 187.5}, {'customer': 'LIGHTING SHOWROOM', 'revenue': 187.5}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 178.13}] | [{'item': '6070-SF BLK-BLK', 'desc': 'Golden Lighting Tribeca 4-light Semi-Flush Mount in Matte Black', 'available': 361}, {'item': '6070-FM BLK-BLK', 'desc': 'Golden Lighting Tribeca 2-light Flush Mount in Matte Black', 'available': 224}, {'item': '6070-BA3 BLK-BLK', 'desc': 'Golden Lighting Tribeca 3-light Vanity in Matte Black', 'available': 116}, {'item': '6070-9 BLK-BLK', 'desc': 'Golden Lighting Tribeca 9-light Chandelier in Matte Black', 'available': 24}, {'item': '6070-4 BLK-BLK', 'desc': 'Golden Lighting Tribeca 4-light Pendant in Matte Black', 'available': 20}, {'item': '6070-4 BLK-PW', 'desc': 'Golden Lighting Tribeca 4-light Pendant in Matte Black and Pewter Accents', 'available': 17}, {'item': '6070-FM BLK-PW', 'desc': 'Golden Lighting Tribeca 2-light Flush Mount in Matte Black and Pewter Accents', 'available': 9}, {'item': '6070-1SF PW-PW', 'desc': 'Golden Lighting Tribeca 1-light Semi-Flush Mount in Pewter', 'available': 8}, {'item': '6070-BA2 BLK-BLK', 'desc': 'Golden Lighting Tribeca 2-light Vanity in Matte Black', 'available': 3}] |
| 1017-69 BLK | Golden Lighting Alastair 15-light 2-tier Chandelier (6+9) Matte Black | 1017 | 28,315 | 85 | — | 2026-07-20 | [{'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 1639.5}, {'customer': None, 'revenue': 1093.5}, {'customer': 'GW KEETER LIGHTING & HOME/ BENTON', 'revenue': 958.5}, {'customer': 'PIONEER LIGHTING INC.', 'revenue': 729.0}, {'customer': 'ASBURYS INC', 'revenue': 729.0}, {'customer': 'TOUCH OF CLASS', 'revenue': 729.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 684.0}, {'customer': 'URBAN LIGHTS', 'revenue': 684.0}, {'customer': 'KENDALL ELECTRIC INC / FORT WAYNE', 'revenue': 684.0}, {'customer': 'FERGUSON #2657 / BOWLING GREEN', 'revenue': 639.0}, {'customer': 'FERGUSON ENTERPRISES #13/ KNOXVILLE', 'revenue': 639.0}, {'customer': 'WOLBERG ELECTRICAL SUPPLY / SARATOGA SPRINGS', 'revenue': 639.0}, {'customer': 'ELEKTRA LIGHTS & FANS', 'revenue': 636.0}, {'customer': 'FERGUSON ENTERPRISES #484/ ODESSA TX', 'revenue': 636.0}, {'customer': 'Cline-Holder Electric Supply, Inc / Elizabethton', 'revenue': 633.0}, {'customer': 'AURA INTERIORS INC', 'revenue': 410.06}, {'customer': 'C & M DESIGNS LLC DBA THE MINT JULEP', 'revenue': 383.4}, {'customer': 'HOME LIGHTING CANADA', 'revenue': 383.4}, {'customer': 'FIELDEN VENTURES, LLC dba SIMPLY FLOORS AND LIGHTS', 'revenue': 364.5}, {'customer': None, 'revenue': 364.5}, {'customer': "CAROL'S LIGHTING & FAN SHOP/ HUMBLE", 'revenue': 364.5}, {'customer': 'DOLAN NORTHWEST LLC/ SEATTLE LIGHTING/ SEATTLE', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES NASHVILLE/LEBANON #20/#452', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES #3093/ FARGO', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES / RICHMOND 5', 'revenue': 364.5}, {'customer': 'Ferguson Enterprises / CLARKSVILLE 3699', 'revenue': 364.5}, {'customer': 'Home And Light Valdosta', 'revenue': 364.5}, {'customer': 'JUST LIGHTS  INC', 'revenue': 364.5}, {'customer': 'LIGHTING WORLD INC/OMAHA', 'revenue': 364.5}, {'customer': None, 'revenue': 364.5}, {'customer': 'MASTERS LIGHTING, INC.', 'revenue': 364.5}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ CHARLOTTE', 'revenue': 364.5}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 364.5}, {'customer': 'The Watt House LLC', 'revenue': 364.5}, {'customer': 'FERGUSON ENTERPRISES #36 / GREENVILLE', 'revenue': 319.5}, {'customer': 'US ELECTRICAL SERVICES dba YALE ELECTRIC SUPPLY/ LANCASTER', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES / FORT PAYNE 533', 'revenue': 319.5}, {'customer': 'Ferguson Enterprises / GRAND RAPIDS 945', 'revenue': 319.5}, {'customer': 'At Home Lighting / Home Lighting / Colorado Springs', 'revenue': 319.5}, {'customer': 'Ferguson Enterprises #541 Sharonville', 'revenue': 319.5}, {'customer': 'GATEWAY LIGHTING & DESIGN', 'revenue': 319.5}, {'customer': 'HOME LIGHTING & SUPPLY INC', 'revenue': 319.5}, {'customer': 'ILLUMINATIONS/McALLEN', 'revenue': 319.5}, {'customer': 'INLINE ELECTRIC/ AUBURN', 'revenue': 319.5}, {'customer': 'INLINE ELECTRIC / CHATTANOOGA #12', 'revenue': 319.5}, {'customer': 'TECHTRON PRODUCTS INC', 'revenue': 319.5}, {'customer': 'FERGUSON / COLUMBUS OH 1589 2828', 'revenue': 319.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 319.5}, {'customer': 'LIGHTING CONCEPTS / VALDOSTA', 'revenue': 319.5}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 319.5}, {'customer': 'CRESCENT LIGHTING SUPPLY/KIRKLAND', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES #75/ FOREST', 'revenue': 319.5}, {'customer': 'MANTECA LIGHTING', 'revenue': 319.5}, {'customer': 'VOWELL AND SONS INC.', 'revenue': 319.5}, {'customer': 'PROGRESSIVE LIGHTING, INC', 'revenue': 319.5}, {'customer': 'ARIZONA LIGHTING COMPANY/ YUMA', 'revenue': 319.5}, {'customer': 'PACE LIGHTING', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES /DES MOINES #522 / CLIVE#226', 'revenue': 319.5}, {'customer': 'FERGUSON ENTERPRISES #1020 / WEST ALLIS', 'revenue': 319.5}, {'customer': "HAGEN'S LIGHTING", 'revenue': 316.5}, {'customer': 'FERGUSON ENTERPRISES #1130/ PHARR', 'revenue': 316.5}, {'customer': 'FERGUSON ENTERPRISES #34/ CHARLOTTE', 'revenue': 316.5}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 297.14}, {'customer': "MCGILL'S FURNITURE", 'revenue': 159.75}, {'customer': 'COLEY ELECTRIC/DOUGLAS', 'revenue': 159.75}] | [{'item': '1017-9 BLK', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte Black', 'available': 136}, {'item': '1017-3 BLK', 'desc': 'Golden Lighting Alastair 3-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-6 BLK', 'desc': 'Golden Lighting Alastair 6-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-9 WHT', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte White', 'available': 28}, {'item': '1017-39 BLK', 'desc': 'Golden Lighting Alastair 12-light Chandelier in Matte Black', 'available': 18}] |
| 1017-96 BLK | Golden Lighting Alastair 15-light 2-tier Chandelier (9+6) in Matte Black | 1017 | 28,247.94 | 92 | — | 2026-07-20 | [{'customer': 'Plumbing Distributors Inc / Lawrenceville', 'revenue': 1146.0}, {'customer': 'SOUTHERN LIGHTS/BURNSVILLE', 'revenue': 953.5}, {'customer': 'FERGUSON ENTERPRISES #215 / LENEXA', 'revenue': 920.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 859.5}, {'customer': 'TECHTRON PRODUCTS INC', 'revenue': 859.5}, {'customer': 'RECLAIMED WAREHOUSE', 'revenue': 695.0}, {'customer': 'Southern Lighting LLC', 'revenue': 695.0}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 674.0}, {'customer': 'AMERICAN LIGHTING / JOHNSON CITY', 'revenue': 653.0}, {'customer': 'SHANOR ELECTRIC SUPPLIES LLC / ORCHARD PARK', 'revenue': 634.0}, {'customer': 'DECORATIVE LIGHTING, INC.', 'revenue': 634.0}, {'customer': 'PARAMONT-EO/ NEW LENOX', 'revenue': 573.0}, {'customer': 'AURA INTERIORS INC', 'revenue': 391.8}, {'customer': 'FANGIO / THE  FACTORY LIGHTING / FURNITURE / PATIO', 'revenue': 347.5}, {'customer': 'Brandon Lighting / MS', 'revenue': 347.5}, {'customer': 'PEAK LIGHTING', 'revenue': 347.5}, {'customer': 'URBAN LIGHTS', 'revenue': 347.5}, {'customer': 'Southside Lighting Gallery', 'revenue': 347.5}, {'customer': 'ONE SOURCE LIGHTING / BILLINGS', 'revenue': 347.5}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 347.5}, {'customer': 'CAPPADONNA OF AZ', 'revenue': 347.5}, {'customer': 'Dupage Lighting Inc.', 'revenue': 347.5}, {'customer': 'GROVE SUPPLY INC / PHILADELPHIA', 'revenue': 347.5}, {'customer': 'Ferguson Enterprises #52/ Orlando', 'revenue': 347.5}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY/HIGHLAND PARK', 'revenue': 347.5}, {'customer': 'FERGUSON ENTERPRISES #57/ OCALA', 'revenue': 347.5}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 347.5}, {'customer': 'STARLIGHT LIGHTING CENTRE', 'revenue': 343.8}, {'customer': 'AMERICAN LIGHTING / KNOXVILLE', 'revenue': 326.5}, {'customer': None, 'revenue': 326.5}, {'customer': 'LITE ART BY CAI DESIGNS', 'revenue': 326.5}, {'customer': 'AMERICAN LIGHTING / KINGSPORT', 'revenue': 326.5}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 326.5}, {'customer': 'Hortons Home Lighting / LaGrange', 'revenue': 326.5}, {'customer': 'Southern Lighting Gallery/ Augusta', 'revenue': 326.5}, {'customer': 'AUSTELL LIGHTING', 'revenue': 326.5}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 326.5}, {'customer': 'Lighting Emporium / Springdale', 'revenue': 326.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 326.5}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 319.5}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 319.5}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 286.5}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 286.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 286.5}, {'customer': 'Robinson Lighting Winnipeg - Cartier Lighting / Plymouth', 'revenue': 286.5}, {'customer': 'DEMENT LIGHTING/ LUBBOCK', 'revenue': 286.5}, {'customer': 'DEALERS ELECTRICAL SUPPLY/BRYAN', 'revenue': 286.5}, {'customer': 'FERGUSON ENTERPRISES #483/ AMARILLO TX', 'revenue': 286.5}, {'customer': 'FERGUSON ENTERPRISES #2009-#1657 / GOLDEN VALLEY', 'revenue': 286.5}, {'customer': 'Ferguson Enterprises #951 / #952 Indianapolis', 'revenue': 286.5}, {'customer': 'FERGUSON ENTERPRISES / BRYAN 1563', 'revenue': 286.5}, {'customer': None, 'revenue': 286.5}, {'customer': None, 'revenue': 286.5}, {'customer': 'GOOD FRIEND ELECTRIC', 'revenue': 286.5}, {'customer': 'GALAXIE LIGHTING dba LIGHTINGUTAH.COM', 'revenue': 286.5}, {'customer': 'IMAGINE MORE SERVICE / NORTHERN LIGHTS', 'revenue': 286.5}, {'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 286.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 286.5}, {'customer': 'LUMINAIRES LTD / WILLMAR', 'revenue': 286.5}, {'customer': 'LIGHTING INCORPORATED / HOUSTON, TX', 'revenue': 286.5}, {'customer': 'MAYER ELECTRIC SUPPLY / DOTHAN #172500', 'revenue': 286.5}, {'customer': 'PLUMBING DISTRIBUTORS INC/ WOODSTOCK', 'revenue': 286.5}, {'customer': 'PLUMBING DISTRIBUTORS INC / #021 NASHVILLE', 'revenue': 286.5}, {'customer': 'Raymond De Steiger/ Ray Lighting Center', 'revenue': 286.5}, {'customer': 'SIOUX FALLS LIGHTHOUSE, LLC', 'revenue': 286.5}, {'customer': 'TRI-SUPPLY CO / CONROE', 'revenue': 286.5}, {'customer': 'DANLAR INC dba LADE-DANLAR / TUCKER', 'revenue': 286.5}, {'customer': 'The Watt House LLC', 'revenue': 286.5}, {'customer': 'Wilson Lighting Co / Winston Salem', 'revenue': 286.5}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 286.5}, {'customer': "GRAHAM'S LIGHTING / FRANKLIN", 'revenue': 272.18}, {'customer': 'ROYAUME LUMINAIRE/ SHERBROOKE', 'revenue': 179.72}, {'customer': 'ROYAUME LUMINAIRE/ BEAUPORT', 'revenue': 179.72}, {'customer': 'ROYAUME LUMINAIRE/ TERREBONNE', 'revenue': 179.72}] | [{'item': '1017-9 BLK', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte Black', 'available': 136}, {'item': '1017-3 BLK', 'desc': 'Golden Lighting Alastair 3-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-6 BLK', 'desc': 'Golden Lighting Alastair 6-light Chandelier in Matte Black', 'available': 31}, {'item': '1017-9 WHT', 'desc': 'Golden Lighting Alastair 9-light Chandelier in Matte White', 'available': 28}, {'item': '1017-39 BLK', 'desc': 'Golden Lighting Alastair 12-light Chandelier in Matte Black', 'available': 18}] |
| 3118-L PW-SD | Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Seeded Glass | 3118 | 27,818.76 | 298 | — | 2026-07-13 | [{'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 7545.31}, {'customer': None, 'revenue': 5526.95}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 2163.0}, {'customer': 'Southside Lighting Gallery', 'revenue': 2028.0}, {'customer': 'RIVER CITY LIGHTING', 'revenue': 1380.0}, {'customer': "Gerhard's Kitchen & Bath / First Supply LLC", 'revenue': 731.5}, {'customer': 'BUTLER LIGHTING/HIGH POINT', 'revenue': 563.0}, {'customer': 'ILLUMINATIONS/McALLEN', 'revenue': 555.0}, {'customer': "BUTLER'S ELECTRIC SUPPLY / MYRTLE BEACH", 'revenue': 468.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 368.0}, {'customer': 'Ferguson Enterprises #1599  / Cranberry Township', 'revenue': 313.5}, {'customer': "CAROL'S LIGHTING & FAN SHOP/ HUMBLE", 'revenue': 313.5}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 283.5}, {'customer': 'CAPITAL ELECTRIC / BLUFFTON', 'revenue': 277.5}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 268.5}, {'customer': 'LIGHTING FIRST OF FLORIDA/ BONITA SPG', 'revenue': 268.5}, {'customer': 'PREMIER LIGHTING/ BAKERSFIELD', 'revenue': 255.25}, {'customer': 'THE BROADWAY SHOWROOM', 'revenue': 209.0}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 209.0}, {'customer': 'INLINE ELECTRIC / HUNTSVILLE', 'revenue': 209.0}, {'customer': None, 'revenue': 209.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 209.0}, {'customer': 'MCFREDERICKS INC / THE OLDE PARSONAGE', 'revenue': 209.0}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 209.0}, {'customer': 'HUDSON PARC LIGHTING AND DESIGN', 'revenue': 189.0}, {'customer': 'LIGHTS UNLIMITED  INC.', 'revenue': 189.0}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 189.0}, {'customer': 'MATHES OF ALABAMA ELECTRIC SUPPLY CO., INC.', 'revenue': 189.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 185.0}, {'customer': 'LIGHTING PLUS / HOUSTON', 'revenue': 185.0}, {'customer': 'IBS LIGHTING, LTD / THE COLONY', 'revenue': 185.0}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 185.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 179.0}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 179.0}, {'customer': 'FARMVILLE WHOLESALE ELECTRIC', 'revenue': 138.75}, {'customer': 'SUNBELT LIGHTING LLC / FLOWOOD', 'revenue': 104.5}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 104.5}, {'customer': 'MAYER ELECTRIC SUPPLY / DOTHAN #172500', 'revenue': 94.5}, {'customer': 'Trinity Home Center', 'revenue': 94.5}, {'customer': 'THE LIGHTING DESIGN CO. / Draper, UT', 'revenue': 94.5}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 94.5}, {'customer': 'BRECHER LIGHTING / LOUISVILLE', 'revenue': 94.5}, {'customer': 'DOLAN NORTHWEST LLC / GLOBE LIGHTING / PORTLAND', 'revenue': 94.5}, {'customer': 'MAYER ELECTRIC SUPPLY/ BIRMINGHAM #200', 'revenue': 92.5}, {'customer': 'LIGHTSTYLES / COSTA MESA / LUXE HOME STUDIO', 'revenue': 92.5}, {'customer': 'LIGHTSTYLES  / ORANGE / RIVERSIDE', 'revenue': 92.5}] | [{'item': '3118-M1L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Opal Glass', 'available': 558}, {'item': '3118-M1L RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Seeded Glass', 'available': 144}, {'item': '3118-2SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 106}, {'item': '3118-M1L PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Seeded Glass', 'available': 105}, {'item': '3118-BA2 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Seeded Glass', 'available': 105}, {'item': '3118-BA3 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-BA3 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-L BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Opal Glass', 'available': 59}, {'item': '3118-BA2 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-2SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Opal Glass', 'available': 56}, {'item': '3118-BA3 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Opal Glass', 'available': 55}, {'item': '3118-BA3 CH-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Opal Glass', 'available': 55}, {'item': '3118-3SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 CH-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Chrome and Opal Glass', 'available': 54}, {'item': '3118-BA2 CH-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Opal Glass', 'available': 52}, {'item': '3118-BA2 PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Pewter', 'available': 42}, {'item': '3118-2SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Pewter', 'available': 42}, {'item': '3118-L BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Clear Glass', 'available': 32}, {'item': '3118-1SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-BA1 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-2SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 29}, {'item': '3118-BA2 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Seeded Glass', 'available': 29}, {'item': '3118-L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Chrome and Seeded Glass', 'available': 28}, {'item': '3118-SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 28}, {'item': '3118-SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 28}, {'item': '3118-3SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 27}, {'item': '3118-4SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Semi-Flush Mount in Matte Black', 'available': 26}, {'item': '3118-BA3 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Opal Glass', 'available': 26}, {'item': '3118-BA4 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Seeded Glass', 'available': 26}, {'item': '3118-BA4 CH-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Opal Glass', 'available': 24}, {'item': '3118-BA4 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA3 PW-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Pewter and Opal Glass', 'available': 23}, {'item': '3118-SF14 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14 in Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA4 PW-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Seeded Glass', 'available': 21}, {'item': '3118-BA3 BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Clear Glass', 'available': 21}, {'item': '3118-M1L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Opal Glass', 'available': 20}, {'item': '3118-BA4 CH-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Seeded Glass', 'available': 19}, {'item': '3118-BA4 PW-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Opal Glass', 'available': 19}, {'item': '3118-BA4 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Opal Glass', 'available': 18}, {'item': '3118-BA1 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA1 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA2 BCB-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Opal Glass', 'available': 13}, {'item': '3118-BA4 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Opal Glass', 'available': 12}, {'item': '3118-M1L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Chrome and Seeded Glass', 'available': 11}, {'item': '3118-1SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Pewter', 'available': 9}, {'item': '3118-BA1 PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Seeded Glass', 'available': 9}, {'item': '3118-BA1 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-3SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Chrome', 'available': 6}, {'item': '3118-BA3 CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Seeded Glass', 'available': 6}, {'item': '3118-1SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 5}, {'item': '3118-2SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Chrome', 'available': 2}, {'item': '3118-BA2 CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Seeded Glass', 'available': 2}, {'item': '3118-L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Opal Glass', 'available': 1}, {'item': '3118-SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 1}, {'item': '3118-2SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 1}, {'item': '3118-BA2 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Opal Glass', 'available': 1}] |
| 8001-BA3 BLK-SD | Golden Lighting Parrish 3-light Vanity in Matte Black | 8001 | 25,628.13 | 346 | — | 2026-08-20 | [{'customer': 'ELLEN LIGHTING/ STAFFORD', 'revenue': 14063.55}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 833.0}, {'customer': 'FIRST COAST LIGHTING AND FANS, LLC', 'revenue': 678.83}, {'customer': 'HELSEL-JEPPERSON', 'revenue': 651.0}, {'customer': 'STEADFAST LIGHTING - SPRINGDALE, AR', 'revenue': 567.0}, {'customer': 'Home And Light Valdosta', 'revenue': 540.6}, {'customer': 'ANCELRAN, INC. dba MUSKA LIGHTING CENTER, INC.', 'revenue': 477.0}, {'customer': 'Plumbing Distributors Inc / Lawrenceville', 'revenue': 427.5}, {'customer': 'PIONEER LIGHTING INC.', 'revenue': 318.0}, {'customer': 'The Watt House LLC', 'revenue': 318.0}, {'customer': 'Robinson Lighting Winnipeg - Cartier Lighting / Plymouth', 'revenue': 318.0}, {'customer': 'FIXTURE THIS', 'revenue': 318.0}, {'customer': 'DECORATIVE LIGHTING, INC.', 'revenue': 298.15}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 286.2}, {'customer': 'COASTAL LIGHTING SUPPLY/ WILMINGTON', 'revenue': 283.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 278.26}, {'customer': 'LIGHTING CONCEPTS / VALDOSTA', 'revenue': 262.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 238.52}, {'customer': 'SUNBELT LIGHTING LLC #9 / BATESVILLE', 'revenue': 238.5}, {'customer': 'LISA LYNN DESIGNS / LOUISVILLE', 'revenue': 238.5}, {'customer': 'XPRESS LIGHTING OF TEXAS', 'revenue': 234.63}, {'customer': 'STAGGS CARPETS & INTERIORS dba STAGGS INTERIORS', 'revenue': 190.8}, {'customer': 'FERGUSON ENTERPRISES #107 / ALPHARETTA', 'revenue': 189.0}, {'customer': 'LIGHT SYSTEMS, INC.', 'revenue': 178.89}, {'customer': 'LIGHTING BY LAVONNE LLC', 'revenue': 178.89}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 175.0}, {'customer': 'Stokes Electrical Supply Co, Inc.', 'revenue': 175.0}, {'customer': 'SHALLOTTE ELECTRIC', 'revenue': 175.0}, {'customer': 'ROB AND NITA YOUNG LLC dba YOUNG & CO', 'revenue': 159.0}, {'customer': None, 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES / #2790 PITTSBURGH', 'revenue': 159.0}, {'customer': '43RD STREET LIGHTING INC', 'revenue': 159.0}, {'customer': 'HOMESTYLES dba IDAHO DREAMING LLC / DALTON', 'revenue': 159.0}, {'customer': 'LEE SUPPLY CORP / INDIANAPOLIS', 'revenue': 159.0}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 159.0}, {'customer': 'PROGRESSIVE LIGHTING, INC', 'revenue': 159.0}, {'customer': 'PROGRESSIVE LIGHTING INC/ LEE LIGHTING/ CHARLOTTE', 'revenue': 159.0}, {'customer': 'TEXAS BRIGHT IDEAS/ HARKER HEIGHTS', 'revenue': 159.0}, {'customer': 'SUNBELT LIGHTING LLC / BILOXI', 'revenue': 159.0}, {'customer': 'FERGUSON ENTERPRISES #215 / LENEXA', 'revenue': 127.2}, {'customer': 'ACCENT LIGHTING/ WICHITA', 'revenue': 119.26}, {'customer': 'KANSAS LIGHTING', 'revenue': 79.5}, {'customer': 'MINNESOTA LIGHTING', 'revenue': 79.5}, {'customer': 'Trinity Home Center', 'revenue': 79.5}, {'customer': 'NORTH COAST ELECTRIC / KENT / AUBURN', 'revenue': 79.5}, {'customer': 'THE LIGHTING STUDIO / SENOIA', 'revenue': 79.5}, {'customer': 'Valley Electric Supply / Ansonia', 'revenue': 63.6}, {'customer': 'CJ LIGHTING AND FANS', 'revenue': 39.75}] | [{'item': '8001-9 BLK-SD', 'desc': 'Golden Lighting Parrish 9-light Chandelier in Matte Black', 'available': 110}, {'item': '8001-BA2 BLK-SD', 'desc': 'Golden Lighting Parrish 2-light Vanity in Matte Black', 'available': 108}, {'item': '8001-BA2 RBZ-SD', 'desc': 'Golden Lighting Parrish 2-light Vanity in Rubbed Bronze', 'available': 29}, {'item': '8001-BA3 PW-SD', 'desc': 'Golden Lighting Parrish 3-light Vanity in Pewter', 'available': 18}] |
| 3118-L RBZ-SD | Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Seeded Glass | 3118 | 25,316.74 | 285 | — | 2026-07-13 | [{'customer': None, 'revenue': 6201.3}, {'customer': 'BROTHERS LIGHTING AND FAN GALLERY', 'revenue': 772.87}, {'customer': 'MAYER ELECTRIC SUPPLY/ BIRMINGHAM #200', 'revenue': 716.0}, {'customer': 'MOUNTAIN LIGHTING & DESIGN', 'revenue': 661.5}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 650.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 650.5}, {'customer': 'NORTHERN LIGHTING / WESTERVILLE', 'revenue': 557.0}, {'customer': 'THE LIGHTING CORNER INC / GRANDVILLE', 'revenue': 542.0}, {'customer': 'FERGUSON ENTERPRISES / #12 NORFOLK', 'revenue': 537.0}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 447.5}, {'customer': 'TURNEY LIGHTING & ELECTRIC / SAN ANTONIO', 'revenue': 390.0}, {'customer': 'THE LIGHTING GALLERY/LANCASTER', 'revenue': 390.0}, {'customer': 'BUTLER LIGHTING/HIGH POINT', 'revenue': 384.0}, {'customer': 'KENDALL ELECTRIC INC / FORT WAYNE', 'revenue': 374.0}, {'customer': 'LIGHTING AND LAMP / PELHAM', 'revenue': 358.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 358.0}, {'customer': 'LIGHTING UNLIMITED/ COLUMBUS', 'revenue': 358.0}, {'customer': "CLT LIGHTING, LLC dba EFIRD'S INTERIORS, INC.", 'revenue': 332.96}, {'customer': 'DESIGN LIGHTING/ SURREY', 'revenue': 322.2}, {'customer': 'SUPER-LITE LIGHTING LTD', 'revenue': 302.07}, {'customer': 'GREER LIGHTING CENTER', 'revenue': 292.5}, {'customer': 'FERGUSON ENTERPRISES / MANCHESTER 3356', 'revenue': 292.5}, {'customer': 'GW KEETER LIGHTING & HOME/ BENTON', 'revenue': 292.5}, {'customer': 'Lifestyles Stores Inc / Edmond', 'revenue': 292.5}, {'customer': 'The Glows Works Inc dba The Lighting Gallery', 'revenue': 292.5}, {'customer': 'FERGUSON ENTERPRISES/ #190 SPRING', 'revenue': 292.5}, {'customer': 'PREMIER LIGHTING/ PHOENIX', 'revenue': 283.5}, {'customer': 'Southside Lighting Gallery', 'revenue': 268.5}, {'customer': 'Cregger Lighting Branch 11 / Bluffton', 'revenue': 268.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 268.5}, {'customer': 'FERGUSON ENTERPRISES #8/ ROANOKE', 'revenue': 268.5}, {'customer': 'FERGUSON ENTERPRISES #48/ WILMINGTON NC', 'revenue': 268.5}, {'customer': 'GALLERY OF LIGHTING /HOLDER ELECTRIC/GREENVILLE', 'revenue': 268.5}, {'customer': 'LIFESTYLES STORES INC/ TULSA', 'revenue': 268.5}, {'customer': 'THE LAMPLIGHTER/ SPECTRUM LIGHTING', 'revenue': 268.5}, {'customer': 'RITE RUG DBA CAPITAL LIGHTING', 'revenue': 268.5}, {'customer': 'At Home Lighting / Home Lighting / Colorado Springs', 'revenue': 268.5}, {'customer': 'SUN LIGHTING INC/ TEMPE', 'revenue': 268.5}, {'customer': 'THE SALT BOX LIGHTING/ DEPERE', 'revenue': 268.5}, {'customer': 'LIGHTSTYLE OF TAMPA BAY', 'revenue': 255.09}, {'customer': 'THE BULB BIN  INC', 'revenue': 195.0}, {'customer': 'PACE LIGHTING', 'revenue': 195.0}, {'customer': 'PLUMBING DISTRIBUTORS INC / ALPHARETTA', 'revenue': 195.0}, {'customer': 'PRESTIGE LIGHTING AND DESIGN', 'revenue': 195.0}, {'customer': 'COASTAL LIGHTING SUPPLY/ WILMINGTON', 'revenue': 189.0}, {'customer': 'LIGHTING ETC / N RICHLAND HILLS', 'revenue': 189.0}, {'customer': 'HUDSON PARC LIGHTING AND DESIGN', 'revenue': 189.0}, {'customer': 'LIGHTING INCORPORATED / SAN ANTONIO', 'revenue': 187.0}, {'customer': 'INLINE ELECTRIC / CHATTANOOGA #12', 'revenue': 179.0}, {'customer': 'KRELL LIGHTING', 'revenue': 179.0}, {'customer': 'Tri-Supply Co / Beaumont', 'revenue': 179.0}, {'customer': 'HILL COUNTRY HOME CENTER LLC / KERRVILLE', 'revenue': 179.0}, {'customer': 'CAPITAL ELECTRIC / BLUFFTON', 'revenue': 179.0}, {'customer': None, 'revenue': 179.0}, {'customer': 'Fogg Lighting', 'revenue': 179.0}, {'customer': 'FERGUSON ENTERPRISES / #1334 JACKSONVILLE', 'revenue': 179.0}, {'customer': 'FERGUSON ENTERPRISES #78/ EVANSVILLE', 'revenue': 179.0}, {'customer': 'STOKES ELECTRIC CO / KNOXVILLE', 'revenue': 179.0}, {'customer': 'JUST LIGHTS  INC', 'revenue': 179.0}, {'customer': 'Sunbelt Lighting LLC / Baton Rouge', 'revenue': 97.5}, {'customer': 'CED dba NOTOCO INDUSTRIES', 'revenue': 97.5}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 97.5}, {'customer': 'DULLES ELECTRIC SUPPLY CORP / STERLING', 'revenue': 97.5}, {'customer': 'IMAGINE MORE SERVICE / NORTHERN LIGHTS', 'revenue': 97.5}, {'customer': 'PLAZA ELECTRIC', 'revenue': 97.5}, {'customer': 'BEST LIGHTING & ACCESSORIES / GLADSTONE', 'revenue': 94.5}, {'customer': 'INLINE ELECTRIC/ AUBURN', 'revenue': 89.5}, {'customer': 'PEAK LIGHTING', 'revenue': 89.5}, {'customer': 'Wholesale Lighting / Daytona', 'revenue': 89.5}, {'customer': 'LEBANON ELECTRIC SUPPLY, INC', 'revenue': 44.75}, {'customer': 'INLINE ELECTRIC #11 / ATHENS', 'revenue': 0.0}] | [{'item': '3118-M1L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Opal Glass', 'available': 558}, {'item': '3118-M1L RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Rubbed Bronze and Seeded Glass', 'available': 144}, {'item': '3118-2SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 106}, {'item': '3118-M1L PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Seeded Glass', 'available': 105}, {'item': '3118-BA2 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Seeded Glass', 'available': 105}, {'item': '3118-BA3 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 86}, {'item': '3118-3SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-BA3 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Seeded Glass', 'available': 64}, {'item': '3118-L BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Opal Glass', 'available': 59}, {'item': '3118-BA2 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-2SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 57}, {'item': '3118-L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Pewter and Opal Glass', 'available': 56}, {'item': '3118-BA3 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Opal Glass', 'available': 55}, {'item': '3118-BA3 CH-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Opal Glass', 'available': 55}, {'item': '3118-3SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 55}, {'item': '3118-BA1 CH-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Chrome and Opal Glass', 'available': 54}, {'item': '3118-BA2 CH-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Opal Glass', 'available': 52}, {'item': '3118-BA2 PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Pewter', 'available': 42}, {'item': '3118-2SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Pewter', 'available': 42}, {'item': '3118-L BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Matte Black and Clear Glass', 'available': 32}, {'item': '3118-1SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-BA1 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Opal Glass', 'available': 32}, {'item': '3118-2SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 29}, {'item': '3118-BA2 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Seeded Glass', 'available': 29}, {'item': '3118-L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Chrome and Seeded Glass', 'available': 28}, {'item': '3118-SF RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Opal Glass', 'available': 28}, {'item': '3118-SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Seeded Glass', 'available': 28}, {'item': '3118-3SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 27}, {'item': '3118-4SF BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Semi-Flush Mount in Matte Black', 'available': 26}, {'item': '3118-BA3 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Opal Glass', 'available': 26}, {'item': '3118-BA4 BLK-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Seeded Glass', 'available': 26}, {'item': '3118-BA4 CH-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Opal Glass', 'available': 24}, {'item': '3118-BA4 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA3 PW-OP', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Pewter and Opal Glass', 'available': 23}, {'item': '3118-SF14 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 14 in Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 23}, {'item': '3118-BA4 PW-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Seeded Glass', 'available': 21}, {'item': '3118-BA3 BLK-CLR', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Matte Black and Clear Glass', 'available': 21}, {'item': '3118-M1L PW-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Pewter and Opal Glass', 'available': 20}, {'item': '3118-BA4 CH-SD', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Chrome and Seeded Glass', 'available': 19}, {'item': '3118-BA4 PW-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Pewter and Opal Glass', 'available': 19}, {'item': '3118-BA4 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Matte Black and Opal Glass', 'available': 18}, {'item': '3118-BA1 BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BCB-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Brushed Champagne Brass', 'available': 15}, {'item': '3118-1SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA1 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Matte Black and Opal Glass', 'available': 14}, {'item': '3118-BA2 BCB-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Brushed Champagne Brass and Opal Glass', 'available': 13}, {'item': '3118-BA4 RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 4-light Vanity in Rubbed Bronze and Opal Glass', 'available': 12}, {'item': '3118-M1L CH-SD', 'desc': 'Yep by Golden Lighting Hines 1-light 7in Pendant in Chrome and Seeded Glass', 'available': 11}, {'item': '3118-1SF PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Pewter', 'available': 9}, {'item': '3118-BA1 PW-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Pewter and Seeded Glass', 'available': 9}, {'item': '3118-BA1 RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Vanity in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-3SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Semi-Flush Mount in Chrome', 'available': 6}, {'item': '3118-BA3 CH-SD', 'desc': 'Yep by Golden Lighting Hines 3-light Vanity in Chrome and Seeded Glass', 'available': 6}, {'item': '3118-1SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Adjustable Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 6}, {'item': '3118-SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 5}, {'item': '3118-2SF CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Chrome', 'available': 2}, {'item': '3118-BA2 CH-SD', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Chrome and Seeded Glass', 'available': 2}, {'item': '3118-L RBZ-OP', 'desc': 'Yep by Golden Lighting Hines 1-light 14in Pendant in Rubbed Bronze and Opal Glass', 'available': 1}, {'item': '3118-SF RBZ-SD', 'desc': 'Yep by Golden Lighting Hines 1-light Semi-Flush Mount in Rubbed Bronze and Seeded Glass', 'available': 1}, {'item': '3118-2SF BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Semi-Flush Mount in Matte Black and Opal Glass', 'available': 1}, {'item': '3118-BA2 BLK-OP', 'desc': 'Yep by Golden Lighting Hines 2-light Vanity in Matte Black and Opal Glass', 'available': 1}] |
