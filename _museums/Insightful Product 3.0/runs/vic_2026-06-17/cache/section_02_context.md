# Section 2 Context Bundle — Vaxcel International Corporation (vic)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Vaxcel International Corporation (vic, org_id=176)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=52093, portal_order_gmv=$9.5M |
| HAS_INVENTORY | True | inventory_count=1190 |
| HAS_SALES_DATA | True | sales_data_count=198255 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=0 engagement_reps=10 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Catalog-Focused |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | vaxcel_international_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$9.5M > ecat_gmv=$28,345: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 0 | 0 |
| ENGAGEMENT_REP_COUNT | 10 | engagement_reps=10 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 32 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 93, Mixpanel total submit_order (Q-01): 1 |
| USER_GROUP_SPLIT_AVAILABLE | True | join_rate=96.9%, ambiguous_rate=0.0%, showroom_event_share=28.5% |
| USER_GROUP_JOIN_RATE | 97% | 31 of 32 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 29% | showroom+admin share of matched events: 28.5% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=6 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=476 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 7d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=115 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Vaxcel International Corporation
- **Shortname**: vic
- **Org ID**: 176
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Vaxcel International Corporation (vic, org_id=176)
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

# Signal Rank — Vaxcel International Corporation (vic, org_id=176)
- **Run date**: 2026-06-17
- **Total signals fired**: 23 (P0: 8, P1: 14, P2: 1)
- **Org GMV**: $0.0M eCat LTM, $9.5M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-01 | Next Best Product — C0281/C0280 co-purchase pattern across 26 customers | P0 | §2/§3 | 2.6 | $45,579,720 | 2.0 | 237,014,546 | POSITIVE |
| 2 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.1M+ total business, zero eCat orders | P1 | §2 Accounts | 8.1 | $8,135,489 | 2.0 | 132,372,363 | POSITIVE |
| 3 | SIG-DECAY-04 | Spending Contraction — Menards DC DIST #3039 -78.4% YoY ($300,730→$65,047), $235,683 gap | P0 | §2 Accounts | 3.9 | $235,683 | 3.0 | 2,771,632 | RISK |
| 4 | SIG-MOM-01 | Account Acceleration — Ace Hardware Corporation 2 consecutive QoQ acceleration quarters, $53,900 peak quarter (+439% QoQ) | P0 | §2 Accounts | 14.6 | $53,900 | 3.0 | 2,364,589 | POSITIVE |
| 5 | SIG-DECAY-04 | Spending Contraction — HomeDepot.com -24.9% YoY ($1,587,995→$1,191,892), $396,103 gap | P0 | §2 Accounts | 1.2 | $396,103 | 3.0 | 1,479,443 | RISK |
| 6 | SIG-COMMERCE-01 | Capture Rate — eCat captures 0.3% of $10M total business; each +1pt = $95K | P0 | §4 Commerce | 5.0 | $95,000 | 3.0 | 1,420,748 | POSITIVE |
| 7 | SIG-MOM-01 | Account Acceleration — Walmart.com 2 consecutive QoQ acceleration quarters, $19,549 peak quarter (+96% QoQ) | P0 | §2 Accounts | 3.2 | $19,549 | 3.0 | 188,258 | POSITIVE |
| 8 | SIG-OPP-04 | New Item Adoption Gap — 30 new items with $0 platform orders | P2 | §3 Product | 3.0 | $50,000 | 1.0 | 150,000 | POSITIVE |
| 9 | SIG-DECAY-04 | Spending Contraction — Belami, Inc. -25.1% YoY ($140,796→$105,442), $35,354 gap | P0 | §2 Accounts | 1.3 | $35,354 | 3.0 | 133,107 | RISK |
| 10 | SIG-DECAY-04 | Spending Contraction — Lighting New York -25.5% YoY ($93,402→$69,539), $23,864 gap | P0 | §2 Accounts | 1.3 | $23,864 | 3.0 | 91,279 | RISK |
| 11 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 59% of eCat GMV | P1 | §4 Commerce | 1.5 | $16,302 | 2.0 | 48,114 | RISK |
| 12 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — riser_prices last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — placement_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — options last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — option_groups last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — matrix_options last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — kit_items last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 7 | 1 | 0 | 8 | |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 12 | 0 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — C0281/C0280 co-purchase pattern across 26 customers
2. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.1M+ total business, zero eCat orders
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Ace Hardware Corporation 2 consecutive QoQ acceleration quarters, $53,900 peak quarter (+439% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 0.3% of $10M total business; each +1pt = $95K
5. **[RISK]** SIG-DECAY-04: Spending Contraction — Menards DC DIST #3039 -78.4% YoY ($300,730→$65,047), $235,683 gap
6. **[RISK]** SIG-DECAY-04: Spending Contraction — HomeDepot.com -24.9% YoY ($1,587,995→$1,191,892), $396,103 gap
7. **[RISK]** SIG-DECAY-04: Spending Contraction — Belami, Inc. -25.1% YoY ($140,796→$105,442), $35,354 gap

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Vaxcel International Corporation (vic, org_id=176)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | HomeDepot.com | 1 | DECAY-04 | $396,103 |
| 2 | Menards DC DIST #3039 | 1 | DECAY-04 | $235,683 |
| 3 | Belami, Inc. | 1 | DECAY-04 | $35,354 |
| 4 | Lighting New York | 1 | DECAY-04 | $23,864 |
| 5 | C0281 | 1 | OPP-01 | $45,579,720 |
| 6 | 20 accounts | 1 | OPP-02 | $8,135,489 |
| 7 | Ace Hardware Corporation | 1 | MOM-01 | $53,900 |
| 8 | Walmart.com | 1 | MOM-01 | $19,549 |

### Q-12_results.md

# Q-12 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 1,496 | 52 | 19 | 14 | 12 |

### Q-14_results.md

# Q-14 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| C01404 | Champlain Valley Electric Supply | 15 | $4,853 | 2025-08-12 17:28:18 | 2026-05-29 18:51:17 | 20.70 |
| C00567 | U.S. 31 Supply, Inc. | 14 | $2,459 | 2025-07-16 19:57:03 | 2026-05-29 19:15:14 | 24.40 |
| C00803 | Colorado Interiors Ltd | 12 | $2,988 | 2025-06-18 04:55:46 | 2026-04-27 18:48:32 | 28.50 |
| C00373 | Fan Lady and Lighting | 10 | $1,230 | 2025-06-18 19:58:33 | 2026-04-29 18:47:26 | 35 |
| C00783 | Unique Lighting & Home Decor | 7 | $2,727 | 2025-08-05 20:13:00 | 2026-03-28 17:53:40 | 39.20 |
| C01009 | Rangeley Lakes Builders Supply | 6 | $2,011 | 2025-11-11 21:07:57 | 2026-04-17 21:35:39 | 31.40 |
| C00206 | Kenyon Noble Lumber Co | 5 | $3,275 | 2025-10-29 17:06:40 | 2026-05-19 14:58:35 | 50.50 |
| C00894 | Ruby & Quiri, Inc. | 4 | $1,048 | 2025-07-01 20:18:19 | 2026-04-08 16:38:16 | 93.60 |
| C00767 | Avfco Wholesale Supply Co., Inc. | 4 | $2,011 | 2025-10-20 12:52:44 | 2026-04-16 19:34:00 | 59.40 |
| C01849 | Black Dog Design House | 4 | $1,959 | 2025-08-21 15:50:57 | 2026-06-09 17:21:49 | 97.40 |

### Q-14b_results.md

# Q-14b Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| C00371 | Menards DC DIST #3039 | 27 | 16.20 | 26.30 | 1.62 | $65,047 |
| C01061 | The Light Center | 24 | 17.90 | 30.80 | 1.72 | $33,331 |
| C00989 | CED Consolidated Electrical Distributors | 94 | 4.60 | 7.10 | 1.54 | $25,116 |
| C01582 | We Got Lites, Inc. | 117 | 3.90 | 6.10 | 1.56 | $20,470 |
| C01613 | Houzz Inc | 286 | 1.40 | 7.20 | 5.14 | $17,899 |
| C02157 | House-Hasson Hardware Company | 33 | 10 | 23.20 | 2.32 | $16,362 |
| C01931 | OJ Commerce, LLC | 228 | 2 | 3.80 | 1.90 | $14,627 |
| C00825 | Stokes Electric Company | 72 | 6.20 | 12.60 | 2.03 | $14,584 |
| C00980 | Christie's Lighting Gallery, LLC | 29 | 14.90 | 30.30 | 2.03 | $13,507 |
| C02010 | Vaasuhomes | 134 | 3.20 | 7.10 | 2.22 | $10,181 |
| C01142 | Progressive Lighting | 97 | 4.70 | 8 | 1.70 | $9,051 |
| C00934 | Wolfe Lighting & Accents | 45 | 9.40 | 15.60 | 1.66 | $8,732 |
| C00643 | Lighting Originals | 51 | 7.10 | 20.80 | 2.93 | $8,347 |
| C00726 | Lamps Plus, Inc. | 30 | 12.60 | 27 | 2.14 | $8,298 |
| C00554 | The Lighting Shoppe Inc | 51 | 3.50 | 5.80 | 1.66 | $8,060 |

### Q-17_results.md

# Q-17 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| C01534 | Rocky Mountain Design Interiors | MT | 2026-01-07 23:51:13 | 2 | $803 |
| C01242 | Interior Design Studio | MN | 2025-07-15 17:48:42 | 1 | $501 |
| C00625 | Bradley Interiors | MN | 2025-08-13 20:29:24 | 1 | $351 |
| C02148 | The Furniture Doctor Inc | NY | 2025-08-08 14:12:16 | 2 | $304 |
| C00900 | Village Lighting & Supply, Inc. | OH | 2026-01-16 18:51:55 | 1 | $198 |
| C01480 | Sound Interiors | ON | 2025-07-25 17:13:35 | 1 | $180 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| C01534 | Rocky Mountain Design Interiors | MT | $803 | 2026-01-07 23:51:13 | 160 |
| C01242 | Interior Design Studio | MN | $501 | 2025-07-15 17:48:42 | 337 |
| C00625 | Bradley Interiors | MN | $351 | 2025-08-13 20:29:24 | 308 |
| C02148 | The Furniture Doctor Inc | NY | $304 | 2025-08-08 14:12:16 | 313 |
| C00900 | Village Lighting & Supply, Inc. | OH | $198 | 2026-01-16 18:51:55 | 152 |
| C01480 | Sound Interiors | ON | $180 | 2025-07-25 17:13:35 | 327 |

### Q-40_results.md

# Q-40 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 12
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| MT | 3 | 14 | $6,805 |
| NY | 4 | 23 | $6,715 |
| CO | 1 | 12 | $2,988 |
| IN | 1 | 14 | $2,459 |
| ME | 1 | 6 | $2,011 |
| WI | 1 | 4 | $2,011 |
| GA | 1 | 4 | $1,959 |
| FL | 1 | 10 | $1,230 |
| MN | 2 | 2 | $852 |
| NE | 1 | 1 | $482 |
| OH | 1 | 1 | $198 |
| ON | 1 | 1 | $180 |

### Q-41_results.md

# Q-41 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-04-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-06-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-07-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-09-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-10-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-11-01 | eCat Online-Acquired (self-serve) | 2 |
| 2026-01-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-52_results.md

# Q-52 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01026 | Wayfair LLC | — | 12,750 | $1.8M | 0 | $0 | 0 |
| C01103 | HomeDepot.com | — | 8,935 | $1.2M | 0 | $0 | 0 |
| C00977 | Build.com | — | 6,057 | $1.1M | 0 | $0 | 0 |
| C00490 | Lowes.com US | — | 8,408 | $1.1M | 0 | $0 | 0 |
| C02057 | Amazon- Direct | — | 3,349 | $725,201 | 0 | $0 | 0 |
| C00113 | Orgill | — | 112 | $487,400 | 0 | $0 | 0 |
| C00835 | Ferguson Enterprises Corporate | — | 1,285 | $313,061 | 0 | $0 | 0 |
| C01378 | Black Forest Decor | — | 1,225 | $238,592 | 0 | $0 | 0 |
| C01469 | Designer Lighting & Fan | — | 929 | $188,153 | 0 | $0 | 0 |
| C01914 | Bed Bath & Beyond | — | 1,276 | $182,093 | 0 | $0 | 0 |
| C02160 | Ace International | — | 2 | $112,106 | 0 | $0 | 0 |
| C01825 | Ace Hardware Corporation | — | 170 | $107,453 | 0 | $0 | 0 |
| C01919 | Belami, Inc. | — | 608 | $105,442 | 0 | $0 | 0 |
| C02159 | Target Plus | — | 402 | $81,350 | 0 | $0 | 0 |
| C02156 | Cimarron Lumber & Supply Company | — | 176 | $75,940 | 0 | $0 | 0 |
| C01958 | Lighting New York | — | 383 | $69,539 | 0 | $0 | 0 |
| C01314 | Dolan Northwest, LLC Corp. | — | 341 | $67,201 | 0 | $0 | 0 |
| C00710 | Nebraska Furniture Mart, Inc. | — | 38 | $65,199 | 0 | $0 | 0 |
| C00371 | Menards DC DIST #3039 | — | 19 | $65,047 | 0 | $0 | 0 |
| C02117 | Walmart.com | — | 302 | $51,712 | 0 | $0 | 0 |
| C01368 | Imagine More, LLC | — | 21 | $35,992 | 0 | $0 | 0 |
| C01061 | The Light Center | — | 14 | $33,331 | 0 | $0 | 0 |
| C00402 | Homestyles-Coeur d'Alene | — | 38 | $33,197 | 0 | $0 | 0 |
| C00153 | Kohl's | — | 132 | $28,563 | 0 | $0 | 0 |
| C01031 | Cast Antlers | — | 86 | $27,403 | 0 | $0 | 0 |
| C00746 | The Cabin Place | — | 108 | $27,396 | 0 | $0 | 0 |
| C00282 | Light Source Lighting | — | 166 | $25,365 | 0 | $0 | 0 |
| C00989 | CED Consolidated Electrical Distributors | — | 59 | $25,116 | 1 | $760 | 3 |
| C01566 | Sonepar USA | — | 44 | $24,446 | 0 | $0 | 0 |
| C00369 | Shades of Light | — | 61 | $23,561 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| C01026 | Wayfair LLC | — | 12,750 | $1.8M |
| C01103 | HomeDepot.com | — | 8,935 | $1.2M |
| C00977 | Build.com | — | 6,057 | $1.1M |
| C00490 | Lowes.com US | — | 8,408 | $1.1M |
| C02057 | Amazon- Direct | — | 3,349 | $725,201 |
| C00113 | Orgill | — | 112 | $487,400 |
| C00835 | Ferguson Enterprises Corporate | — | 1,285 | $313,061 |
| C01378 | Black Forest Decor | — | 1,225 | $238,592 |
| C01469 | Designer Lighting & Fan | — | 929 | $188,153 |
| C01914 | Bed Bath & Beyond | — | 1,276 | $182,093 |
| C02160 | Ace International | — | 2 | $112,106 |
| C01825 | Ace Hardware Corporation | — | 170 | $107,453 |
| C01919 | Belami, Inc. | — | 608 | $105,442 |
| C02159 | Target Plus | — | 402 | $81,350 |
| C02156 | Cimarron Lumber & Supply Company | — | 176 | $75,940 |
| C01958 | Lighting New York | — | 383 | $69,539 |
| C01314 | Dolan Northwest, LLC Corp. | — | 341 | $67,201 |
| C00710 | Nebraska Furniture Mart, Inc. | — | 38 | $65,199 |
| C00371 | Menards DC DIST #3039 | — | 19 | $65,047 |
| C02117 | Walmart.com | — | 302 | $51,712 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 12
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CO | 0 | 0 | $0 | 1 | 12 | $2,988 | — |
| FL | 0 | 0 | $0 | 1 | 10 | $1,230 | — |
| GA | 0 | 0 | $0 | 1 | 4 | $1,959 | — |
| IN | 0 | 0 | $0 | 1 | 14 | $2,459 | — |
| ME | 0 | 0 | $0 | 1 | 6 | $2,011 | — |
| MN | 0 | 0 | $0 | 2 | 2 | $852 | — |
| MT | 0 | 0 | $0 | 3 | 14 | $6,805 | — |
| NE | 0 | 0 | $0 | 1 | 1 | $482 | — |
| NY | 0 | 0 | $0 | 4 | 23 | $6,715 | — |
| OH | 0 | 0 | $0 | 1 | 1 | $198 | — |
| ON | 0 | 0 | $0 | 1 | 1 | $180 | — |
| WI | 0 | 0 | $0 | 1 | 4 | $2,011 | — |

### Q-57_results.md

# Q-57 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA | $151,459 | $184,169 | 21.60 | 47 | 49 | -2 | 1,169 |
| TX | $132,972 | $168,039 | 26.40 | 48 | 39 | 9 | 869 |
| FL | $157,509 | $149,562 | -5 | 52 | 50 | 2 | 872 |
| NY | $86,736 | $127,471 | 47 | 47 | 42 | 5 | 825 |
| Unknown | $65,521 | $114,808 | 75.20 | 11 | 8 | 3 | 25 |
| CO | $72,140 | $111,619 | 54.70 | 36 | 37 | -1 | 400 |
| NC | $84,426 | $100,856 | 19.50 | 34 | 29 | 5 | 596 |
| PA | $77,640 | $93,649 | 20.60 | 38 | 36 | 2 | 572 |
| NJ | $48,404 | $88,200 | 82.20 | 24 | 28 | -4 | 677 |
| MA | $58,857 | $81,357 | 38.20 | 25 | 21 | 4 | 531 |
| TN | $64,514 | $75,556 | 17.10 | 30 | 28 | 2 | 433 |
| MI | $45,210 | $70,875 | 56.80 | 31 | 26 | 5 | 466 |
| IL | $59,263 | $69,792 | 17.80 | 39 | 27 | 12 | 492 |
| WI | $46,337 | $69,300 | 49.60 | 30 | 24 | 6 | 340 |
| VA | $59,139 | $68,979 | 16.60 | 33 | 25 | 8 | 454 |
| OH | $43,756 | $67,480 | 54.20 | 33 | 30 | 3 | 451 |
| MN | $49,318 | $64,833 | 31.50 | 28 | 29 | -1 | 369 |
| GA | $55,408 | $63,250 | 14.20 | 40 | 35 | 5 | 413 |
| WA | $54,248 | $56,312 | 3.80 | 29 | 25 | 4 | 394 |
| OR | $45,225 | $51,575 | 14 | 25 | 18 | 7 | 295 |
| SC | $34,895 | $45,551 | 30.50 | 29 | 23 | 6 | 289 |
| AZ | $32,671 | $42,882 | 31.30 | 29 | 26 | 3 | 242 |
| ID | $28,988 | $39,715 | 37 | 22 | 19 | 3 | 158 |
| MO | $32,079 | $38,571 | 20.20 | 24 | 30 | -6 | 247 |
| MD | $29,637 | $38,287 | 29.20 | 20 | 19 | 1 | 262 |

### Q-68_results.md

# Q-68 Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| Menards DC DIST #3039 | WI | $65,047 | $302,510 | $237,463 | 21.50 | 12 |
| Stokes Electric Company | TN | $14,932 | $40,572 | $25,640 | 36.80 | 11 |
| Lighting First | WI | $10,043 | $34,322 | $24,279 | 29.30 | 13 |
| Sun Lighting, Inc. | AZ | $4,917 | $19,513 | $14,596 | 25.20 | 6 |
| Premier Lighting | CA | $7,245 | $21,643 | $14,398 | 33.50 | 4 |
| Shades of Light | WI | $37,995 | $52,228 | $14,233 | 72.70 | 13 |
| EP Lighting LLC | TX | $8,143 | $21,047 | $12,904 | 38.70 | 7 |
| Lights and More, Inc. | SC | $5,184 | $13,739 | $8,555 | 37.70 | 7 |
| United Electrical Supply Co., Inc. | NE | $2,348 | $10,040 | $7,692 | 23.40 | 6 |
| Berkshire Lighting Galleries | NY | $4,614 | $12,140 | $7,526 | 38 | 6 |
| Hummel Brothers | PA | $1,765 | $9,107 | $7,341 | 19.40 | 9 |
| Wabash Electric Supply, Inc. | MI | $1,184 | $7,837 | $6,654 | 15.10 | 5 |
| The Light Depot | MN | $7,882 | $14,495 | $6,613 | 54.40 | 9 |
| Hearth & Home | AR | $2,597 | $8,825 | $6,228 | 29.40 | 5 |
| Lightstyle | NC | $3,263 | $9,232 | $5,969 | 35.30 | 12 |
| Geller Lighting Supply Co, Inc | VA | $2,780 | $8,537 | $5,757 | 32.60 | 3 |
| American Lighting & Design | GA | $1,305 | $6,653 | $5,348 | 19.60 | 4 |
| Graybar Electric Company, Inc. | SC | $1,091 | $6,207 | $5,116 | 17.60 | 5 |
| Lighting Concepts LLC | GA | $1,715 | $6,571 | $4,856 | 26.10 | 4 |
| Western Slope Electric Supply, Inc. | CO | $2,988 | $7,680 | $4,692 | 38.90 | 8 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01103 | HomeDepot.com | T0697 | 11.75-in. 2 Light Outdoor Motion Sensor Security Flood Light Bronze 240 Degrees | 145 | 2.10 | 239 | 113.80 | 8,609.50 | DECAY_DETECTED |
| C01026 | Wayfair LLC | F0097 | Curtiss 52-in. Ceiling Fan Satin Brass | 198 | 2.60 | 21 | 8.10 | 43,996.41 | DECAY_DETECTED |
| C01026 | Wayfair LLC | CO-OWD050TB | Chiasso 5-in Outdoor Wall Light Textured Black | 71 | 4.20 | 240 | 57.10 | 5,625.31 | DECAY_DETECTED |
| C01026 | Wayfair LLC | F0120 | Wedgewood 60-in. LED Ceiling Fan | 241 | 2.20 | 8 | 3.60 | 63,268.52 | DECAY_DETECTED |
| C01103 | HomeDepot.com | T0696 | 11.75-in. 2 Light Outdoor Motion Sensor Security Flood Light White 240 Deg. | 160 | 2.80 | 99 | 35.40 | 5,602.60 | DECAY_DETECTED |
| C01026 | Wayfair LLC | T0368 | Dorado 12-in Outdoor Wall Light Dark Bronze and Light Gold | 231 | 2.30 | 15 | 6.50 | 24,073.41 | DECAY_DETECTED |
| C01026 | Wayfair LLC | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 260 | 2.10 | 8 | 3.80 | 30,487.77 | DECAY_DETECTED |
| C00490 | Lowes.com US | P0357 | Beloit 9-in. Mini Pendant Matte Black | 172 | 3.10 | 14 | 4.50 | 25,400.15 | DECAY_DETECTED |
| C01026 | Wayfair LLC | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 195 | 2.70 | 13 | 4.80 | 23,432.18 | DECAY_DETECTED |
| C01026 | Wayfair LLC | C0261 | Huntley 12-in. Semi-Flush Ceiling Light White Glass Natural Brass | 230 | 2.30 | 12 | 5.20 | 18,771.04 | DECAY_DETECTED |
| C00977 | Build.com | P0176 | Milano 4.75-in Mini Pendant Marble Swirl Glass Satin Nickel | 158 | 3.30 | 22 | 6.70 | 13,327.18 | DECAY_DETECTED |
| C00490 | Lowes.com US | T0596 | Yosemite Dualux 7-in. Outdoor Motion Sensor Wall Light Burnished Bronze | 28 | 11.50 | 141 | 12.30 | 6,897 | DECAY_DETECTED |
| C01026 | Wayfair LLC | T0572 | Dorado 18 in. W Outdoor Wall Light Dark Bronze with Light Gold | 149 | 3.50 | 13 | 3.70 | 22,357.13 | DECAY_DETECTED |
| C01026 | Wayfair LLC | PD35459BN | Monrovia 11.25-in Pendant Brushed Nickel | 237 | 2.30 | 10 | 4.30 | 18,981.31 | DECAY_DETECTED |
| C00977 | Build.com | W0309 | Vilo 1L Vanity Golden Brass | 131 | 4 | 13 | 3.30 | 22,125.93 | DECAY_DETECTED |
| C01026 | Wayfair LLC | P0177 | Milano 4.75-in Mini Pendant Smoky Fire Glass Oil Rubbed Bronze | 183 | 2.90 | 11 | 3.80 | 18,069.74 | DECAY_DETECTED |
| C01026 | Wayfair LLC | T0197 | Outland 9.75-in Outdoor Wall Light Aged Iron and Light Gold | 125 | 4.10 | 34 | 8.30 | 8,082.51 | DECAY_DETECTED |
| C01026 | Wayfair LLC | CH35405RBZ/B | Monrovia 5L Chandelier Royal Bronze | 150 | 3.50 | 10 | 2.90 | 22,947.75 | SLOWING |
| C01103 | HomeDepot.com | P0176 | Milano 4.75-in Mini Pendant Marble Swirl Glass Satin Nickel | 221 | 2.40 | 7 | 2.90 | 19,630.92 | SLOWING |
| C00490 | Lowes.com US | T0695 | 11.75-in. 2 Light Outdoor Motion Sensor Security Flood Light Bronze 180 Deg. | 231 | 2.30 | 7 | 3 | 18,073 | DECAY_DETECTED |
| C01026 | Wayfair LLC | W0515 | Northbrook 24-in. W 3 Light Vanity Matte Black | 76 | 3.70 | 20 | 5.40 | 9,823 | DECAY_DETECTED |
| C01026 | Wayfair LLC | F0124 | Barnes 54-in Ceiling Fan Matte | 65 | 7.30 | 36 | 4.90 | 10,207.11 | DECAY_DETECTED |
| C01026 | Wayfair LLC | OW21861TB | Chatham 6.5-in Outdoor Wall Light Textured Black | 165 | 3.10 | 12 | 3.90 | 12,948.90 | DECAY_DETECTED |
| C01026 | Wayfair LLC | T0775 | Cottage Grove 9-in. W Outdoor Wall Light Matte Black | 108 | 4.90 | 14 | 2.90 | 17,482.16 | SLOWING |
| C00490 | Lowes.com US | P0243 | Huntley 12-in Pendant Milk Glass Oil Rubbed Bronze | 90 | 5.80 | 20 | 3.40 | 14,434.45 | DECAY_DETECTED |
| C01026 | Wayfair LLC | T0652 | Chiasso 2 Light 20-in.H Outdoor Wall Light Textured Black | 84 | 6.20 | 26 | 4.20 | 11,843.70 | DECAY_DETECTED |
| C02057 | Amazon- Direct | C0316 | Orleans 15-in. W Flush Mount Navy Blue and Matte Gold | 92 | 5.60 | 18 | 3.20 | 15,315.25 | DECAY_DETECTED |
| C01026 | Wayfair LLC | OW21861BBZ | Chatham 6.5-in Outdoor Wall Light Burnished Bronze | 121 | 4.20 | 24 | 5.70 | 8,582.30 | DECAY_DETECTED |
| C01103 | HomeDepot.com | P0173 | Milano 4.75-in Mini Pendant Toffee Swirl Glass Oil Rubbed Bronze | 83 | 6.10 | 34 | 5.60 | 8,348.50 | DECAY_DETECTED |
| C01026 | Wayfair LLC | C0312 | Eastgate 8.75-in. Semi-Flush Ceiling Light Matte Black | 212 | 2.50 | 10 | 4 | 10,664.31 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 50
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C01026 | Wayfair LLC | 1,753,066.17 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 26 |
| C02117 | Walmart.com | 51,711.70 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0281 | Burnaby 16-in Semi-Flush Mount Black | 26 |
| C00402 | Homestyles-Coeur d'Alene | 33,196.58 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 26 |
| C00989 | CED Consolidated Electrical Distributors | 25,115.75 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 26 |
| C01076 | Lighting Star | 21,670 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 26 |
| C01076 | Lighting Star | 21,670 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 26 |
| C01090 | Urban Lights | 20,051.02 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0281 | Burnaby 16-in Semi-Flush Mount Black | 26 |
| C00772 | InLine Electric Supply Co., Inc. | 18,396.60 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 26 |
| C01613 | Houzz Inc | 17,899 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0281 | Burnaby 16-in Semi-Flush Mount Black | 26 |
| C01613 | Houzz Inc | 17,899 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0281 | Burnaby 16-in Semi-Flush Mount Black | 26 |
| C00389 | The Lighting Design Company | 16,577.10 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0281 | Burnaby 16-in Semi-Flush Mount Black | 26 |
| C00389 | The Lighting Design Company | 16,577.10 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0281 | Burnaby 16-in Semi-Flush Mount Black | 26 |
| C01355 | Fusion Lighting and Design | 13,841.50 | C0281 | Burnaby 16-in Semi-Flush Mount Black | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 26 |
| C01026 | Wayfair LLC | 1,753,066.17 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 25 |
| C02117 | Walmart.com | 51,711.70 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 25 |
| C00402 | Homestyles-Coeur d'Alene | 33,196.58 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 25 |
| C00989 | CED Consolidated Electrical Distributors | 25,115.75 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 25 |
| C01090 | Urban Lights | 20,051.02 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 25 |
| C00772 | InLine Electric Supply Co., Inc. | 18,396.60 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | 25 |
| C01355 | Fusion Lighting and Design | 13,841.50 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 25 |
| C01026 | Wayfair LLC | 1,753,066.17 | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 24 |
| C01914 | Bed Bath & Beyond | 182,093.19 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 24 |
| C02159 | Target Plus | 81,350.07 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 24 |
| C00402 | Homestyles-Coeur d'Alene | 33,196.58 | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 24 |
| C00153 | Kohl's | 28,563.37 | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 24 |
| C01582 | We Got Lites, Inc. | 20,469.50 | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 24 |
| C01355 | Fusion Lighting and Design | 13,841.50 | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | C0280 | Burnaby 16-in Semi-Flush Mount Matte Brass | 24 |
| C01914 | Bed Bath & Beyond | 182,093.19 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 22 |
| C02159 | Target Plus | 81,350.07 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 22 |
| C02117 | Walmart.com | 51,711.70 | C0258 | Burnaby 20.5-in. 4 Light Semi-Flush Black | C0112 | Burnaby 20.5-in Semi Flush Ceiling Light Matte Brass | 22 |

*(Truncated: showing top 30 of 50 rows. Full data in cache file.)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C01103 | HomeDepot.com | — | 1,191,892.29 | 1,587,994.89 | -24.90 | 0 | 0 | — | CONTRACTING |
| C00371 | Menards DC DIST #3039 | — | 65,047 | 300,729.98 | -78.40 | 0 | 0 | — | CONTRACTING |
| C01919 | Belami, Inc. | — | 105,442.23 | 140,795.97 | -25.10 | 0 | 0 | — | CONTRACTING |
| C01958 | Lighting New York | — | 69,538.68 | 93,402.38 | -25.50 | 0 | 0 | — | CONTRACTING |
| C01031 | Cast Antlers | — | 27,402.98 | 36,555.03 | -25 | 0 | 0 | — | CONTRACTING |
| C00746 | The Cabin Place | — | 27,396 | 34,470.67 | -20.50 | 0 | 0 | — | CONTRACTING |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| C00113 | Orgill | 2 | 226,617.84 | 2,415.70 | [{'quarter': '2025-07-01', 'revenue': 112914.1, 'qoq_pct': 2415.7}, {'quarter': '2025-10-01', 'revenue': 226617.84, 'qoq_pct': 100.7}, {'quarter': '2026-01-01', 'revenue': 82970.46, 'qoq_pct': -63.4}, {'quarter': '2026-04-01', 'revenue': 64253.65, 'qoq_pct': -22.6}] |
| C01825 | Ace Hardware Corporation | 2 | 53,899.90 | 438.70 | [{'quarter': '2025-07-01', 'revenue': 53899.9, 'qoq_pct': 438.7}, {'quarter': '2025-10-01', 'revenue': 15154.34, 'qoq_pct': -71.9}, {'quarter': '2026-01-01', 'revenue': 25701.25, 'qoq_pct': 69.6}, {'quarter': '2026-04-01', 'revenue': 10835.1, 'qoq_pct': -57.8}] |
| C02159 | Target Plus | 2 | 38,974.97 | 1,095.30 | [{'quarter': '2025-07-01', 'revenue': 13262.57, 'qoq_pct': 1095.3}, {'quarter': '2025-10-01', 'revenue': 13525.73, 'qoq_pct': 2.0}, {'quarter': '2026-01-01', 'revenue': 15088.83, 'qoq_pct': 11.6}, {'quarter': '2026-04-01', 'revenue': 38974.97, 'qoq_pct': 158.3}] |
| C01061 | The Light Center | 2 | 31,168 | 2,243.50 | [{'quarter': '2025-07-01', 'revenue': 1330.0, 'qoq_pct': -26.1}, {'quarter': '2025-10-01', 'revenue': 31168.0, 'qoq_pct': 2243.5}, {'quarter': '2026-01-01', 'revenue': 298.0, 'qoq_pct': -99.0}, {'quarter': '2026-04-01', 'revenue': 535.0, 'qoq_pct': 79.5}] |
| C02117 | Walmart.com | 2 | 19,549.14 | 96.30 | [{'quarter': '2025-07-01', 'revenue': 8902.56, 'qoq_pct': -18.6}, {'quarter': '2025-10-01', 'revenue': 11919.86, 'qoq_pct': 33.9}, {'quarter': '2026-01-01', 'revenue': 9960.55, 'qoq_pct': -16.4}, {'quarter': '2026-04-01', 'revenue': 19549.14, 'qoq_pct': 96.3}] |
| C01368 | Imagine More, LLC | 2 | 19,405.80 | 1,048.10 | [{'quarter': '2025-07-01', 'revenue': 1012.5, 'qoq_pct': -22.9}, {'quarter': '2025-10-01', 'revenue': 1690.2, 'qoq_pct': 66.9}, {'quarter': '2026-01-01', 'revenue': 19405.8, 'qoq_pct': 1048.1}, {'quarter': '2026-04-01', 'revenue': 13883.4, 'qoq_pct': -28.5}] |
| C01076 | Lighting Star | 2 | 9,225.50 | 598.10 | [{'quarter': '2025-07-01', 'revenue': 3479.0, 'qoq_pct': 598.1}, {'quarter': '2025-10-01', 'revenue': 9225.5, 'qoq_pct': 165.2}, {'quarter': '2026-01-01', 'revenue': 4984.0, 'qoq_pct': -46.0}, {'quarter': '2026-04-01', 'revenue': 3981.5, 'qoq_pct': -20.1}] |
| C00989 | CED Consolidated Electrical Distributors | 2 | 8,960.40 | 106.70 | [{'quarter': '2025-07-01', 'revenue': 8960.4, 'qoq_pct': 88.4}, {'quarter': '2025-10-01', 'revenue': 3264.3, 'qoq_pct': -63.6}, {'quarter': '2026-01-01', 'revenue': 6747.27, 'qoq_pct': 106.7}, {'quarter': '2026-04-01', 'revenue': 4550.78, 'qoq_pct': -32.6}] |
| C00282 | Light Source Lighting | 2 | 8,926.64 | 57.70 | [{'quarter': '2025-07-01', 'revenue': 8926.64, 'qoq_pct': 32.8}, {'quarter': '2025-10-01', 'revenue': 5261.17, 'qoq_pct': -41.1}, {'quarter': '2026-01-01', 'revenue': 4018.85, 'qoq_pct': -23.6}, {'quarter': '2026-04-01', 'revenue': 6337.18, 'qoq_pct': 57.7}] |
| C02157 | House-Hasson Hardware Company | 2 | 8,019.27 | 805.80 | [{'quarter': '2025-07-01', 'revenue': 8019.27, 'qoq_pct': 652.0}, {'quarter': '2025-10-01', 'revenue': 667.5, 'qoq_pct': -91.7}, {'quarter': '2026-01-01', 'revenue': 6046.0, 'qoq_pct': 805.8}, {'quarter': '2026-04-01', 'revenue': 1180.38, 'qoq_pct': -80.5}] |
| C00873 | Royaume Luminaire Lanaudiere | 2 | 7,726.55 | 282.50 | [{'quarter': '2025-07-01', 'revenue': 1367.0, 'qoq_pct': 26.7}, {'quarter': '2025-10-01', 'revenue': 2020.0, 'qoq_pct': 47.8}, {'quarter': '2026-01-01', 'revenue': 7726.55, 'qoq_pct': 282.5}, {'quarter': '2026-04-01', 'revenue': 1188.0, 'qoq_pct': -84.6}] |
| C00252 | Crescent Lighting Supply, Inc. | 2 | 7,562.97 | 59.90 | [{'quarter': '2025-07-01', 'revenue': 3607.65, 'qoq_pct': 8.1}, {'quarter': '2025-10-01', 'revenue': 5769.45, 'qoq_pct': 59.9}, {'quarter': '2026-01-01', 'revenue': 7562.97, 'qoq_pct': 31.1}, {'quarter': '2026-04-01', 'revenue': 5136.59, 'qoq_pct': -32.1}] |
| C00726 | Lamps Plus, Inc. | 2 | 6,311.98 | 917.20 | [{'quarter': '2025-07-01', 'revenue': 6311.98, 'qoq_pct': 917.2}, {'quarter': '2025-10-01', 'revenue': 307.75, 'qoq_pct': -95.1}, {'quarter': '2026-01-01', 'revenue': 1251.91, 'qoq_pct': 306.8}, {'quarter': '2026-04-01', 'revenue': 413.25, 'qoq_pct': -67.0}] |
| C01718 | Cregger Company, Inc. | 3 | 6,130.60 | 331.90 | [{'quarter': '2025-07-01', 'revenue': 6130.6, 'qoq_pct': 331.9}, {'quarter': '2025-10-01', 'revenue': 424.0, 'qoq_pct': -93.1}, {'quarter': '2026-01-01', 'revenue': 1747.6, 'qoq_pct': 312.2}, {'quarter': '2026-04-01', 'revenue': 3936.7, 'qoq_pct': 125.3}] |
| C00980 | Christie's Lighting Gallery, LLC | 2 | 5,796 | 1,143.20 | [{'quarter': '2025-07-01', 'revenue': 5749.2, 'qoq_pct': 130.3}, {'quarter': '2025-10-01', 'revenue': 466.2, 'qoq_pct': -91.9}, {'quarter': '2026-01-01', 'revenue': 5796.0, 'qoq_pct': 1143.2}, {'quarter': '2026-04-01', 'revenue': 1495.8, 'qoq_pct': -74.2}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Vaxcel International Corporation (vic, org_id=176)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*
