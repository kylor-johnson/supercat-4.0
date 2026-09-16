# Section 2 Context Bundle — Ciana Varaluz LLC (vl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=2019, portal_order_gmv=$1.4M |
| HAS_INVENTORY | True | inventory_count=775 |
| HAS_SALES_DATA | True | sales_data_count=10634 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=3 engagement_reps=38 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | varaluz_vl_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$1.4M > ecat_gmv=$1.3M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 3 | 3 |
| ENGAGEMENT_REP_COUNT | 38 | engagement_reps=38 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 95 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 116, Mixpanel total submit_order (Q-01): 160 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=84.2%, ambiguous_rate=0.0%, showroom_event_share=100.0% |
| USER_GROUP_JOIN_RATE | 84% | 80 of 95 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 100% | showroom+admin share of matched events: 100.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 27 admin/showroom users in leaderboard: Angela Smith, CS3 Varaluz, CS4 Varaluz, CS5 Varaluz, CS6 Varaluz |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=36 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=640 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=283 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=480 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Ciana Varaluz LLC
- **Shortname**: vl
- **Org ID**: 147
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
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
| §2 Sales Team | FULL | See Derived Gate 6 §2 formula |
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

# Signal Rank — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17
- **Total signals fired**: 24 (P0: 11, P1: 12, P2: 1)
- **Org GMV**: $1.3M eCat LTM, $1.4M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 64% of eCat GMV | P1 | §4 Commerce | 1.6 | $419,032 | 2.0 | 1,331,132 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 297P25HG (Social Club 25 Light 5-Tier - Havana Gol) $30,355 LTM, 0 available | P0 | §3 Product | 10.0 | $30,355 | 3.0 | 910,660 | RISK |
| 3 | SIG-DECAY-03 | Rep Trajectory — John Howard orders -80.0% QoQ, $33,580 current 90d GMV | P1 | §5 Team | 3.2 | $134,320 | 2.0 | 859,648 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 4DMI0108 (Kye 22x40 Rounded Rectangular Wall Mirro) $23,748 LTM, 0 available | P0 | §3 Product | 10.0 | $23,748 | 3.0 | 712,432 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 376W02BN (Morgan 2 Light Sconce - Brushed Nickel) $21,664 LTM, 0 available | P0 | §3 Product | 10.0 | $21,664 | 3.0 | 649,908 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 309P03HG (Matrix 3 Light Pendant - Havana Gold) $19,915 LTM, 0 available | P0 | §3 Product | 10.0 | $19,915 | 3.0 | 597,451 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 380P05MBFG (Estela 5 Light Pendant - Matte Black/Fre) $15,067 LTM, 0 available | P0 | §3 Product | 10.0 | $15,067 | 3.0 | 452,009 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 348N06HG (Kato 6 Light Oval Pendant - Havana Gold) $13,334 LTM, 0 available | P0 | §3 Product | 10.0 | $13,334 | 3.0 | 400,025 | RISK |
| 9 | SIG-OPP-01 | Next Best Product — 557P08HG/561N06FG co-purchase pattern across 14 customers | P0 | §2/§3 | 1.4 | $135,185 | 2.0 | 378,517 | POSITIVE |
| 10 | SIG-ANOMALY-02 | Stock Out — 297P19HG (Social Club 19 Light 4-Tier - Havana Gol) $12,092 LTM, 0 available | P0 | §3 Product | 10.0 | $12,092 | 3.0 | 362,751 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 389P06MBHN (Blonde Moment 6 Light   Pendant - Matte ) $11,456 LTM, 0 available | P0 | §3 Product | 10.0 | $11,456 | 3.0 | 343,685 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 345C21CBHG (Windsor 21 Light 4-Tier Crystal Chandeli) $10,797 LTM, 0 available | P0 | §3 Product | 10.0 | $10,797 | 3.0 | 323,911 | RISK |
| 13 | SIG-OPP-04 | New Item Adoption Gap — 21 new items with $0 platform orders | P2 | §3 Product | 2.1 | $50,000 | 1.0 | 105,000 | POSITIVE |
| 14 | SIG-COMMERCE-01 | Capture Rate — eCat captures 92.9% of $1M total business; each +1pt = $14K | P0 | §4 Commerce | 0.4 | $14,000 | 3.0 | 15,000 | POSITIVE |
| 15 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — riser_prices last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — placement_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — options last updated 301d ago | P1 | §6 Platform | 3.3 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 1 | 0 | 0 | 1 | |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 0 | 10 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 557P08HG/561N06FG co-purchase pattern across 14 customers
2. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 21 new items with $0 platform orders
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 92.9% of $1M total business; each +1pt = $14K
4. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 64% of eCat GMV
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 297P25HG (Social Club 25 Light 5-Tier - Havana Gol) $30,355 LTM, 0 available
6. **[RISK]** SIG-DECAY-03: Rep Trajectory — John Howard orders -80.0% QoQ, $33,580 current 90d GMV
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 4DMI0108 (Kye 22x40 Rounded Rectangular Wall Mirro) $23,748 LTM, 0 available

**Balance check**: 3 positive (slots 1-3), 4 risk (slots 4-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Ciana Varaluz LLC (vl, org_id=147)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | 557P08HG | 1 | OPP-01 | $135,185 |

### Q-12_results.md

# Q-12 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 1,851 | 245 | 66 | 56 | 5 |

### Q-14_results.md

# Q-14 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| Beauthings | Beautiful Things Lighting | 5 | $58,792 | 2025-09-18 12:49:57 | 2026-03-05 15:35:22 | 42 |
| ValleyLightG | Valley Light Gallery | 4 | $136,962 | 2025-09-24 19:14:58 | 2026-01-12 20:57:31 | 36.70 |
| Dulles | Dulles Electric Supply Corp | 3 | $33,254 | 2025-06-19 16:19:02 | 2026-01-12 22:01:24 | 103.60 |
| LBUFLWestPal | Light Bulbs Unlimited | 3 | $19,983 | 2025-11-07 19:30:24 | 2026-03-17 15:16:19 | 64.90 |
| LBX | LBX Lighting Inc. | 3 | $149,661 | 2025-06-20 18:12:23 | 2026-01-26 23:25:07 | 110.10 |
| SunLiTu | Sun Lighting | 3 | $32,209 | 2026-01-11 23:44:13 | 2026-01-23 22:45:19 | 6 |

### Q-14b_results.md

# Q-14b Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| SouLiBu | Southern Lights | 48 | 9 | 20.90 | 2.32 | $19,865 |
| ProgressTDC | Progressive Lighting : TDC | 17 | 20 | 46.90 | 2.35 | $11,373 |
| DanielH | Danielhouse Studios Inc | 23 | 11.70 | 23 | 1.97 | $10,401 |
| Led | LED Capstone Inc | 12 | 18 | 53.20 | 2.96 | $9,003 |
| LightINgStar | Lighting Star | 28 | 13.40 | 40.80 | 3.04 | $8,630 |
| ClevelandLtg | Cleveland Lighting One | 29 | 10.80 | 43.80 | 4.06 | $8,389 |
| LightINgWorl | Lighting World Decorator | 21 | 16.20 | 49 | 3.02 | $8,272 |
| WilsonKSOver | Wilson Lighting - Overland Park KS | 8 | 42.30 | 63.30 | 1.50 | $6,975 |
| FocalP | Focal Point Hardware | 13 | 12.70 | 29.70 | 2.34 | $6,952 |
| LightingEtcT | Lighting Etc | 7 | 14.30 | 80.30 | 5.62 | $6,548 |
| CapitalLTG | Capital Lighting & Supply, LLC | 6 | 37 | 100 | 2.70 | $6,102 |
| LTGDesignUTD | Lighting Design Company | 14 | 27.70 | 78 | 2.82 | $5,606 |
| ProgressRDC | Progressive Lighting : RDC Lee Lighting | 15 | 26.10 | 42.30 | 1.62 | $5,550 |
| RenHoLe | Rensen House of Lights | 15 | 25.10 | 60.30 | 2.40 | $5,138 |
| Capitol700 | 1800Lighting - Capitol Lighting : Capitol Lighting - Boca Raton FL | 14 | 23.90 | 53 | 2.22 | $5,115 |

### Q-17_results.md

# Q-17 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| LBX | LBX Lighting Inc. | TX | 2026-01-26 23:25:07 | 3 | $149,661 |
| ValleyLightG | Valley Light Gallery | AZ | 2026-01-12 20:57:31 | 4 | $136,962 |
| Beauthings | Beautiful Things Lighting | FL | 2026-03-05 15:35:22 | 5 | $58,792 |
| PDI | PDI | GA | 2026-01-11 20:31:27 | 1 | $37,768 |
| Ferg#191 | Ferguson Enterprises | VA | 2026-02-03 14:21:09 | 1 | $35,849 |
| Dulles | Dulles Electric Supply Corp | VA | 2026-01-12 22:01:24 | 3 | $33,254 |
| SunLiTu | Sun Lighting | AZ | 2026-01-23 22:45:19 | 3 | $32,209 |
| LBEMontclair | Lighting Instyle | CA | 2026-01-15 00:39:04 | 1 | $25,241 |
| PreLiAZ | Premier Lighting | AZ | 2026-01-10 20:49:29 | 1 | $24,803 |
| CityLightsCA | City Lights | CA | 2026-03-03 23:01:22 | 2 | $23,884 |
| HomElightPA | Home Lighting | PA | 2026-02-02 19:06:27 | 2 | $21,831 |
| Ellenlight | Ellen Lighting and Hardware | TX | 2026-01-13 22:32:44 | 1 | $20,404 |
| LBUFLWestPal | Light Bulbs Unlimited | FL | 2026-03-17 15:16:19 | 3 | $19,983 |
| HubbardWilmingt | Hubbard Pipe & Supply, Inc | NC | 2025-06-18 15:15:24 | 1 | $19,956 |
| BrookesON | Brookes On Main | TN | 2026-01-12 16:49:10 | 1 | $18,946 |
| LaCampana | La Campana Store | TX | 2026-01-10 21:06:00 | 2 | $17,581 |
| Hobrecht | Hobrecht Lighting | CA | 2026-01-30 01:09:25 | 2 | $17,533 |
| OneStTh | One Stop Lighting | CA | 2026-01-15 00:41:20 | 1 | $17,118 |
| Georgia | Georgia Lighting | GA | 2026-01-12 20:51:48 | 1 | $16,954 |
| PineGrove | Pine Grove Electrical Supply | LA | 2026-01-10 22:42:46 | 1 | $16,652 |
| RenHoLe | Rensen House of Lights | KS | 2026-01-12 00:25:39 | 2 | $14,354 |
| Progress06 | Progressive Lighting | GA | 2026-01-12 22:08:37 | 1 | $14,159 |
| UniversalLTS | Universal Lights, Inc | TX | 2026-01-29 21:10:03 | 1 | $12,452 |
| Anthology | Anthology Lighting | TX | 2026-01-30 16:30:37 | 1 | $12,409 |
| Pace | Pace Lighting Inc. | GA | 2026-01-12 18:34:56 | 1 | $10,735 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| LBX | LBX Lighting Inc. | TX | $149,661 | 2026-01-26 23:25:07 | 141 |
| ValleyLightG | Valley Light Gallery | AZ | $136,962 | 2026-01-12 20:57:31 | 155 |
| Beauthings | Beautiful Things Lighting | FL | $58,792 | 2026-03-05 15:35:22 | 104 |
| PDI | PDI | GA | $37,768 | 2026-01-11 20:31:27 | 156 |
| Ferg#191 | Ferguson Enterprises | VA | $35,849 | 2026-02-03 14:21:09 | 134 |
| Dulles | Dulles Electric Supply Corp | VA | $33,254 | 2026-01-12 22:01:24 | 155 |
| SunLiTu | Sun Lighting | AZ | $32,209 | 2026-01-23 22:45:19 | 144 |
| LBEMontclair | Lighting Instyle | CA | $25,241 | 2026-01-15 00:39:04 | 153 |
| PreLiAZ | Premier Lighting | AZ | $24,803 | 2026-01-10 20:49:29 | 157 |
| CityLightsCA | City Lights | CA | $23,884 | 2026-03-03 23:01:22 | 105 |
| HomElightPA | Home Lighting | PA | $21,831 | 2026-02-02 19:06:27 | 135 |
| Ellenlight | Ellen Lighting and Hardware | TX | $20,404 | 2026-01-13 22:32:44 | 154 |
| LBUFLWestPal | Light Bulbs Unlimited | FL | $19,983 | 2026-03-17 15:16:19 | 92 |
| HubbardWilmingt | Hubbard Pipe & Supply, Inc | NC | $19,956 | 2025-06-18 15:15:24 | 364 |
| BrookesON | Brookes On Main | TN | $18,946 | 2026-01-12 16:49:10 | 156 |
| LaCampana | La Campana Store | TX | $17,581 | 2026-01-10 21:06:00 | 157 |
| Hobrecht | Hobrecht Lighting | CA | $17,533 | 2026-01-30 01:09:25 | 138 |
| OneStTh | One Stop Lighting | CA | $17,118 | 2026-01-15 00:41:20 | 153 |
| Georgia | Georgia Lighting | GA | $16,954 | 2026-01-12 20:51:48 | 155 |
| PineGrove | Pine Grove Electrical Supply | LA | $16,652 | 2026-01-10 22:42:46 | 157 |

### Q-40_results.md

# Q-40 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| TX | 7 | 10 | $225,598 |
| AZ | 4 | 9 | $202,360 |
| FL | 12 | 19 | $149,250 |
| VA | 7 | 9 | $106,872 |
| CA | 8 | 10 | $101,109 |
| GA | 5 | 5 | $83,206 |
| NC | 3 | 3 | $23,710 |
| PA | 1 | 2 | $21,831 |
| TN | 1 | 1 | $18,946 |
| LA | 1 | 1 | $16,652 |
| MS | 2 | 2 | $15,730 |
| KS | 1 | 2 | $14,354 |
| IL | 2 | 3 | $14,330 |
| ON | 2 | 2 | $12,204 |
| NJ | 2 | 2 | $11,888 |
| NY | 1 | 1 | $8,608 |
| SC | 2 | 2 | $8,138 |
| AB | 1 | 1 | $7,666 |
| OH | 1 | 1 | $4,948 |
| CT | 1 | 1 | $4,163 |

### Q-41_results.md

# Q-41 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 1 |
| 2025-06-01 | Rep-Acquired (iPad) | 3 |
| 2025-08-01 | Rep-Acquired (iPad) | 2 |
| 2025-10-01 | Rep-Acquired (iPad) | 1 |
| 2025-11-01 | Rep-Acquired (iPad) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 10 |
| 2026-02-01 | Rep-Acquired (iPad) | 3 |
| 2026-03-01 | Rep-Acquired (iPad) | 4 |
| 2026-04-01 | Rep-Acquired (iPad) | 1 |
| 2026-06-01 | Rep-Acquired (iPad) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| John Howard | 10 |
| CS4 Varaluz | 2 |
| CS3 Varaluz | 2 |
| Mitchell Winston | 2 |
| Robert Parker | 2 |
| Dean Coxworth | 2 |
| Angie Schaefer | 1 |
| Scott Fellner | 1 |
| CS5 Varaluz | 1 |
| CS6 Varaluz | 1 |
| CS7 Varaluz | 1 |
| HP1 Varaluz | 1 |
| HP4 Varaluz | 1 |

### Q-52_results.md

# Q-52 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LightSourceI | Light Source Lighting | IL | 28 | $25,119 | 0 | $0 | 0 |
| Ferg#320 | Ferguson Enterprises : Ferguson Distribution Center - Grand Prairie | TX | 19 | $23,153 | 0 | $0 | 0 |
| SouLiBu | Southern Lights | MN | 29 | $19,865 | 0 | $0 | 0 |
| SuperWi | Superlite Lighting | MB | 3 | $18,522 | 0 | $0 | 0 |
| Georgia | Georgia Lighting | GA | 16 | $18,160 | 1 | $16,954 | 93.40 |
| FortWorth | Fort Worth Lighting | TX | 31 | $17,758 | 0 | $0 | 0 |
| MetroLTG | Metro Lighting | MO | 15 | $17,364 | 0 | $0 | 0 |
| WEgotlites | We Got Lites, Inc. | NY | 28 | $15,574 | 0 | $0 | 0 |
| ferg#452 | Ferguson Enterprises : Ferguson # 452 |  | 12 | $15,006 | 0 | $0 | 0 |
| VillaLtg | Villa Lighting | MO | 7 | $13,083 | 0 | $0 | 0 |
| SerenH | Serenhaus Studio | NC | 1 | $11,418 | 0 | $0 | 0 |
| ProgressTDC | Progressive Lighting : TDC | GA | 9 | $11,373 | 0 | $0 | 0 |
| Legacy | Legacy Lighting, LLC | GA | 2 | $11,240 | 0 | $0 | 0 |
| Hobrecht | Hobrecht Lighting | CA | 17 | $11,116 | 2 | $17,533 | 157.70 |
| DanielH | Danielhouse Studios Inc | OR | 21 | $10,401 | 0 | $0 | 0 |
| RepSouthernL | Southern Lighting Source | GA | 4 | $10,297 | 0 | $0 | 0 |
| BlackWhale | Black Whale Lighting | CA | 13 | $9,656 | 1 | $3,258 | 33.70 |
| Beauthings | Beautiful Things Lighting | FL | 13 | $9,408 | 5 | $58,792 | 625 |
| Capitol600 | 1800Lighting - Capitol Lighting : Capitol Lighting - Stuart FL | FL | 13 | $9,328 | 0 | $0 | 0 |
| LBEMontclair | Lighting Instyle | CA | 6 | $9,126 | 1 | $25,241 | 276.60 |
| Lgtngfirst | Lighting First | FL | 9 | $9,072 | 0 | $0 | 0 |
| Led | LED Capstone Inc | FL | 10 | $9,003 | 1 | $1,034 | 11.50 |
| LightINgStar | Lighting Star | CA | 18 | $8,630 | 0 | $0 | 0 |
| UrbanLights | Urban Lights | CO | 13 | $8,505 | 0 | $0 | 0 |
| Connecticut | Connecticut Lighting Center | CT | 26 | $8,485 | 1 | $4,163 | 49.10 |
| HinNePh | Hinkley's New State Lighting | AZ | 8 | $8,399 | 0 | $0 | 0 |
| ClevelandLtg | Cleveland Lighting One | OH | 14 | $8,389 | 0 | $0 | 0 |
| LightINgWorl | Lighting World Decorator | NY | 9 | $8,272 | 0 | $0 | 0 |
| Light&Day | Light & Day | MD | 11 | $7,909 | 0 | $0 | 0 |
| SUGARs | Sugar and Spice Photography | MN | 1 | $7,858 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| LightSourceI | Light Source Lighting | IL | 28 | $25,119 |
| Ferg#320 | Ferguson Enterprises : Ferguson Distribution Center - Grand Prairie | TX | 19 | $23,153 |
| FortWorth | Fort Worth Lighting | TX | 31 | $17,758 |
| WEgotlites | We Got Lites, Inc. | NY | 28 | $15,574 |
| ferg#452 | Ferguson Enterprises : Ferguson # 452 |  | 12 | $15,006 |
| VillaLtg | Villa Lighting | MO | 7 | $13,083 |
| SerenH | Serenhaus Studio | NC | 1 | $11,418 |
| ProgressTDC | Progressive Lighting : TDC | GA | 9 | $11,373 |
| Legacy | Legacy Lighting, LLC | GA | 2 | $11,240 |
| DanielH | Danielhouse Studios Inc | OR | 21 | $10,401 |
| RepSouthernL | Southern Lighting Source | GA | 4 | $10,297 |
| Capitol600 | 1800Lighting - Capitol Lighting : Capitol Lighting - Stuart FL | FL | 13 | $9,328 |
| Lgtngfirst | Lighting First | FL | 9 | $9,072 |
| LightINgStar | Lighting Star | CA | 18 | $8,630 |
| UrbanLights | Urban Lights | CO | 13 | $8,505 |
| HinNePh | Hinkley's New State Lighting | AZ | 8 | $8,399 |
| ClevelandLtg | Cleveland Lighting One | OH | 14 | $8,389 |
| SUGARs | Sugar and Spice Photography | MN | 1 | $7,858 |
| VisualComfort | Circa Lighting, LLC DBA Visual Comfort | GA | 4 | $7,752 |
| Coley | Coley Electric and Plumbing Supply Inc | GA | 2 | $7,147 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TX | 56 | 192 | $165,669 | 7 | 10 | $225,598 | 136.20 |
| FL | 63 | 204 | $152,574 | 12 | 19 | $149,250 | 97.80 |
| VA | 134 | 237 | $120,155 | 7 | 9 | $106,872 | 88.90 |
| GA | 27 | 105 | $110,642 | 5 | 5 | $83,206 | 75.20 |
| CA | 45 | 139 | $96,440 | 8 | 10 | $101,109 | 104.80 |
| NY | 16 | 91 | $52,351 | 1 | 1 | $8,608 | 16.40 |
| IL | 18 | 62 | $48,246 | 2 | 3 | $14,330 | 29.70 |
| MO | 12 | 40 | $43,761 | 0 | 0 | $0 | 0 |
| NC | 22 | 60 | $42,147 | 3 | 3 | $23,710 | 56.30 |
| MN | 8 | 52 | $36,689 | 0 | 0 | $0 | 0 |
| OH | 14 | 55 | $32,478 | 1 | 1 | $4,948 | 15.20 |
| AZ | 10 | 39 | $32,118 | 4 | 9 | $202,360 | 630.10 |
| CO | 12 | 51 | $30,610 | 0 | 0 | $0 | 0 |
| MB | 3 | 15 | $23,776 | 0 | 0 | $0 | 0 |
| KS | 5 | 26 | $23,114 | 1 | 2 | $14,354 | 62.10 |
| NV | 13 | 59 | $21,090 | 0 | 0 | $0 | 0 |
| OR | 8 | 33 | $19,951 | 0 | 0 | $0 | 0 |
| SC | 11 | 33 | $18,771 | 2 | 2 | $8,138 | 43.40 |
| WI | 8 | 33 | $18,515 | 0 | 0 | $0 | 0 |
| ON | 11 | 26 | $16,810 | 2 | 2 | $12,204 | 72.60 |

### Q-57_results.md

# Q-57 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

# Q-66 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-66 — Buyer-Within-Account Intelligence
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | new_buyers | existing_buyers | new_buyer_orders | new_buyer_revenue | earliest_new_buyer |
| --- | --- | --- | --- | --- | --- |
| Serenhaus Studio | 1 | 0 | 1 | 12,182.40 | 2026-5-1 |
| Environs Residential Design and Construction LLC | 1 | 0 | 1 | 10,294 | 2026-6-9 |
| Matchez International Inc dba Parkyn Design | 1 | 0 | 2 | 7,432 | 2026-4-22 |
| Ferguson Enterprises : Ferguson - Lincoln NE | 1 | 0 | 2 | 6,863.17 | 2026-3-23 |
| Lighting Instyle | 1 | 0 | 1 | 6,123 | 2026-5-28 |
| Lando Lighting | 1 | 0 | 1 | 5,759.50 | 2026-4-21 |
| Light Bulbs Unlimited - Naples | 1 | 0 | 3 | 5,636.50 | 2026-4-10 |
| Crest Lighting : Paramont EO - New Lenox | 1 | 0 | 3 | 5,361.50 | 2026-5-7 |
| Village Lighting and Supply, Inc. | 1 | 0 | 2 | 5,307.50 | 2026-6-5 |
| FanCo | 1 | 0 | 1 | 4,747 | 2026-5-19 |
| Starlight Lighting Centre | 1 | 0 | 1 | 4,619 | 2026-4-9 |
| Light Gallery Plus | 1 | 0 | 1 | 4,346.50 | 2026-5-19 |
| Light Bulbs Unlimited | 1 | 0 | 1 | 4,229.25 | 2026-3-24 |
| Wasatch Lighting | 1 | 0 | 2 | 4,201 | 2026-5-19 |
| L DAVIS DESIGN | 1 | 0 | 1 | 3,984.50 | 2026-3-24 |
| M & M Lighting | 1 | 0 | 1 | 3,339 | 2026-6-3 |
| Farrey's Wholesale Hardware Co | 1 | 0 | 1 | 3,339 | 2026-5-11 |
| Archetype Design Studio | 1 | 0 | 1 | 3,019.25 | 2026-3-25 |
| Leonor Interiors | 1 | 0 | 1 | 2,924.10 | 2026-5-4 |
| LUCE Lighting and Design, LLC | 1 | 0 | 1 | 2,881 | 2026-3-27 |

### Q-67_results.md

# Q-67 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FL | $104,141 | $77,939 | -25.20 | 43 | 39 | 4 | 78 |
| TX | $135,466 | $74,191 | -45.20 | 40 | 40 | 0 | 68 |
| CA | $53,130 | $52,209 | -1.70 | 27 | 20 | 7 | 36 |
| NC | $17,421 | $36,910 | 111.90 | 21 | 19 | 2 | 28 |
| GA | $37,049 | $27,760 | -25.10 | 14 | 11 | 3 | 22 |
| AZ | $78,111 | $16,668 | -78.70 | 10 | 8 | 2 | 19 |
| ON | $6,283 | $16,457 | 161.90 | 6 | 5 | 1 | 7 |
| CO | $17,830 | $14,186 | -20.40 | 11 | 12 | -1 | 18 |
| LA | $13,559 | $13,775 | 1.60 | 8 | 5 | 3 | 11 |
| OH | $8,334 | $12,912 | 54.90 | 7 | 7 | 0 | 10 |
| VA | $14,772 | $12,226 | -17.20 | 10 | 10 | 0 | 12 |
| NY | $18,075 | $11,842 | -34.50 | 12 | 8 | 4 | 16 |
| IL | $7,553 | $11,556 | 53 | 9 | 8 | 1 | 12 |
| PA | $10,703 | $11,542 | 7.80 | 9 | 9 | 0 | 13 |
| TN | $11,577 | $10,710 | -7.50 | 9 | 6 | 3 | 19 |
| MN | $17,818 | $8,565 | -51.90 | 10 | 7 | 3 | 22 |
| WI | $5,896 | $8,307 | 40.90 | 7 | 7 | 0 | 10 |
| MO | $36,750 | $6,986 | -81 | 8 | 12 | -4 | 12 |
| KS | $14,532 | $6,465 | -55.50 | 6 | 3 | 3 | 9 |
| AB | $10,334 | $5,371 | -48 | 2 | 2 | 0 | 5 |

### Q-68_results.md

# Q-68 Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| Varaluz LLC | 广东省 | $4,024 | $131,263 | $127,238 | 3.10 | 9 |
| Colonial Electric Supply Company. Inc | PA | $5,406 | $82,205 | $76,799 | 6.60 | 6 |
| Southern Lighting Source | GA | $10,297 | $65,615 | $55,318 | 15.70 | 4 |
| Lando Lighting | ON | $5,760 | $55,644 | $49,884 | 10.40 | 1 |
| Progressive Lighting : TDC | TX | $12,208 | $57,915 | $45,707 | 21.10 | 5 |
| Ferguson Enterprises : Ferguson - Knoxville TN | TN | $3,569 | $44,504 | $40,935 | 8 | 4 |
| Ethan and Associates | TX | $6,732 | $47,564 | $40,833 | 14.20 | 3 |
| Illuminations | OK | $2,183 | $39,434 | $37,251 | 5.50 | 4 |
| Muska Lighting Center | MN | $6,306 | $43,335 | $37,029 | 14.60 | 6 |
| Progressive Lighting : Progressive Lighting | GA | $3,469 | $40,462 | $36,993 | 8.60 | 2 |
| Lighting First | OH | $12,521 | $45,210 | $32,689 | 27.70 | 6 |
| Ellen Lighting and Hardware | TX | $12,989 | $44,518 | $31,528 | 29.20 | 3 |
| Old North State Imports | TN | $2,483 | $33,443 | $30,960 | 7.40 | 4 |
| Ferguson Enterprises : Ferguson - Tulsa OK | OK | $3,937 | $34,273 | $30,336 | 11.50 | 4 |
| Wiseway Supply | OH | $4,131 | $33,257 | $29,125 | 12.40 | 8 |
| Creggar Company, Inc. : Cregger Company, Inc | SC | $3,032 | $32,136 | $29,103 | 9.40 | 3 |
| Mahlander's | SD | $2,706 | $31,789 | $29,082 | 8.50 | 4 |
| Lumen Nation | VA | $1,088 | $29,984 | $28,896 | 3.60 | 2 |
| Ferguson Enterprises : Ferguson - Brookshire TX | TX | $1,390 | $28,004 | $26,615 | 5 | 4 |
| Progressive Lighting : RDC Lee Lighting | NC | $6,780 | $33,300 | $26,519 | 20.40 | 9 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 8
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BlackWhale | Black Whale Lighting | 9,656.04 | 557P08HG | Aurora 8 Light Pendant | 561N06FG | High Tide 6 Light linear Pendant | 14 |
| SceneOne | Scene One Interiors | 6,665.85 | 557P08HG | Aurora 8 Light Pendant | 561N06FG | High Tide 6 Light linear Pendant | 14 |
| Jarrell CO | The Jarrell Company | 6,502 | 561N06FG | High Tide 6 Light linear Pendant | 557P08HG | Aurora 8 Light Pendant | 14 |
| CapitalLTG | Capital Lighting & Supply, LLC | 6,101.75 | 561N06FG | High Tide 6 Light linear Pendant | 557P08HG | Aurora 8 Light Pendant | 14 |
| SunLiTe | Sun Lighting nka Sun Lighting Phoenix LLC | 6,021 | 557P08HG | Aurora 8 Light Pendant | 561N06FG | High Tide 6 Light linear Pendant | 14 |
| Ferg#320 | Ferguson Enterprises : Ferguson Distribution Center - Grand Prairie | 23,153.36 | 590S12SG | Downpour 12 Light Dimmable Pendant | 585P08PG | Golden Thicket 9 Light Dimmable Pendant | 11 |
| SunLiTe | Sun Lighting nka Sun Lighting Phoenix LLC | 6,021 | 590S12SG | Downpour 12 Light Dimmable Pendant | 585P08PG | Golden Thicket 9 Light Dimmable Pendant | 11 |
| Cartwright | Cartwright Lighting and Furniture Ltd. | 5,888.15 | 585P08PG | Golden Thicket 9 Light Dimmable Pendant | 590S12SG | Downpour 12 Light Dimmable Pendant | 11 |

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| ferg#452 | Ferguson Enterprises : Ferguson # 452 | 2 | 10,547.04 | 15,456.10 | [{'quarter': '2025-07-01', 'revenue': 67.8, 'qoq_pct': -94.9}, {'quarter': '2025-10-01', 'revenue': 10547.04, 'qoq_pct': 15456.1}, {'quarter': '2026-01-01', 'revenue': 1687.2, 'qoq_pct': -84.0}, {'quarter': '2026-04-01', 'revenue': 3629.86, 'qoq_pct': 115.1}] |
| LightSourceI | Light Source Lighting | 2 | 8,979.50 | 353.10 | [{'quarter': '2025-07-01', 'revenue': 1982.0, 'qoq_pct': 52.6}, {'quarter': '2025-10-01', 'revenue': 8979.5, 'qoq_pct': 353.1}, {'quarter': '2026-01-01', 'revenue': 7633.21, 'qoq_pct': -15.0}, {'quarter': '2026-04-01', 'revenue': 6269.0, 'qoq_pct': -17.9}] |
| ProgressTDC | Progressive Lighting : TDC | 2 | 8,672.60 | 547.50 | [{'quarter': '2025-07-01', 'revenue': 939.15, 'qoq_pct': -22.6}, {'quarter': '2025-10-01', 'revenue': 422.1, 'qoq_pct': -55.1}, {'quarter': '2026-01-01', 'revenue': 1339.5, 'qoq_pct': 217.3}, {'quarter': '2026-04-01', 'revenue': 8672.6, 'qoq_pct': 547.5}] |
| MetroLTG | Metro Lighting | 2 | 8,481.50 | 127.80 | [{'quarter': '2025-07-01', 'revenue': 2223.0, 'qoq_pct': -50.9}, {'quarter': '2025-10-01', 'revenue': 5064.0, 'qoq_pct': 127.8}, {'quarter': '2026-01-01', 'revenue': 8481.5, 'qoq_pct': 67.5}, {'quarter': '2026-04-01', 'revenue': 1596.0, 'qoq_pct': -81.2}] |
| WEgotlites | We Got Lites, Inc. | 2 | 6,366.50 | 970.70 | [{'quarter': '2025-07-01', 'revenue': 3610.3, 'qoq_pct': 409.9}, {'quarter': '2025-10-01', 'revenue': 594.6, 'qoq_pct': -83.5}, {'quarter': '2026-01-01', 'revenue': 6366.5, 'qoq_pct': 970.7}, {'quarter': '2026-04-01', 'revenue': 5003.0, 'qoq_pct': -21.4}] |
| BlackWhale | Black Whale Lighting | 3 | 5,825.24 | 513.50 | [{'quarter': '2025-07-01', 'revenue': 2199.15, 'qoq_pct': 158.2}, {'quarter': '2025-10-01', 'revenue': 682.12, 'qoq_pct': -69.0}, {'quarter': '2026-01-01', 'revenue': 949.53, 'qoq_pct': 39.2}, {'quarter': '2026-04-01', 'revenue': 5825.24, 'qoq_pct': 513.5}] |
| Beauthings | Beautiful Things Lighting | 2 | 5,706.25 | 315.50 | [{'quarter': '2025-07-01', 'revenue': 758.5, 'qoq_pct': -57.7}, {'quarter': '2025-10-01', 'revenue': 1569.5, 'qoq_pct': 106.9}, {'quarter': '2026-01-01', 'revenue': 1373.25, 'qoq_pct': -12.5}, {'quarter': '2026-04-01', 'revenue': 5706.25, 'qoq_pct': 315.5}] |
| VillaLtg | Villa Lighting | 2 | 5,125.50 | 100 | [{'quarter': '2025-07-01', 'revenue': 3027.0, 'qoq_pct': 100.0}, {'quarter': '2025-10-01', 'revenue': 4930.5, 'qoq_pct': 62.9}, {'quarter': '2026-01-01', 'revenue': 5125.5, 'qoq_pct': 4.0}] |
| HinNePh | Hinkley's New State Lighting | 2 | 5,112 | 246.60 | [{'quarter': '2025-07-01', 'revenue': 1369.0, 'qoq_pct': -64.0}, {'quarter': '2025-10-01', 'revenue': 429.5, 'qoq_pct': -68.6}, {'quarter': '2026-01-01', 'revenue': 1488.5, 'qoq_pct': 246.6}, {'quarter': '2026-04-01', 'revenue': 5112.0, 'qoq_pct': 243.4}] |
| FusionLGT | Fusion Light and Design | 2 | 4,504 | 493 | [{'quarter': '2025-10-01', 'revenue': 199.5, 'qoq_pct': -66.1}, {'quarter': '2026-01-01', 'revenue': 1183.0, 'qoq_pct': 493.0}, {'quarter': '2026-04-01', 'revenue': 4504.0, 'qoq_pct': 280.7}] |
| Ferg#34 | Ferguson Enterprises : Ferguson - Charlotte NC | 2 | 4,116.54 | 1,008.10 | [{'quarter': '2025-07-01', 'revenue': 284.74, 'qoq_pct': -29.5}, {'quarter': '2026-01-01', 'revenue': 3155.14, 'qoq_pct': 1008.1}, {'quarter': '2026-04-01', 'revenue': 4116.54, 'qoq_pct': 30.5}] |
| ColonialPAKi | Colonial Electric Supply Company. Inc | 2 | 3,800 | 428.50 | [{'quarter': '2025-10-01', 'revenue': 309.5, 'qoq_pct': -77.4}, {'quarter': '2026-01-01', 'revenue': 719.0, 'qoq_pct': 132.3}, {'quarter': '2026-04-01', 'revenue': 3800.0, 'qoq_pct': 428.5}] |
| Lgtngfirst | Lighting First | 2 | 3,661.60 | 278.30 | [{'quarter': '2025-07-01', 'revenue': 2739.0, 'qoq_pct': 278.3}, {'quarter': '2025-10-01', 'revenue': 1412.55, 'qoq_pct': -48.4}, {'quarter': '2026-01-01', 'revenue': 1259.25, 'qoq_pct': -10.9}, {'quarter': '2026-04-01', 'revenue': 3661.6, 'qoq_pct': 190.8}] |
| Connecticut | Connecticut Lighting Center | 2 | 3,558.36 | 239.20 | [{'quarter': '2025-07-01', 'revenue': 2036.83, 'qoq_pct': -32.3}, {'quarter': '2025-10-01', 'revenue': 3558.36, 'qoq_pct': 74.7}, {'quarter': '2026-01-01', 'revenue': 373.35, 'qoq_pct': -89.5}, {'quarter': '2026-04-01', 'revenue': 1266.52, 'qoq_pct': 239.2}] |
| LightBulbsNa | Light Bulbs Unlimited - Naples | 2 | 3,508.50 | 225.90 | [{'quarter': '2025-07-01', 'revenue': 1369.5, 'qoq_pct': 225.9}, {'quarter': '2026-04-01', 'revenue': 3508.5, 'qoq_pct': 156.2}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Ciana Varaluz LLC (vl, org_id=147)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 297P25HG | Social Club 25 Light 5-Tier - Havana Gold | COL15 | 30,355.33 | 12 | — | 2026-7-17 | [{'customer': 'Ferguson Enterprises', 'revenue': 7216.02}, {'customer': 'Epiphany', 'revenue': 6014.22}, {'customer': 'Illuminations - McAllen TX', 'revenue': 3921.75}, {'customer': 'CED dba Notoco Industries', 'revenue': 2954.5}, {'customer': 'Lee Supply', 'revenue': 2614.5}, {'customer': 'Carrington Lighting', 'revenue': 2614.5}, {'customer': 'Lightstyle of Orlando', 'revenue': 2614.5}, {'customer': 'Ferguson Enterprises', 'revenue': 2405.34}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Fort Worth Lighting', 'revenue': 0.0}, {'customer': "Graham's Lighting Franklin", 'revenue': 0.0}, {'customer': 'Home Lighting', 'revenue': 0.0}, {'customer': 'Hubbard Pipe & Supply, Inc', 'revenue': 0.0}, {'customer': 'American Lighting', 'revenue': 0.0}, {'customer': 'Kristi Hopper Designs', 'revenue': 0.0}, {'customer': 'Lando Lighting', 'revenue': 0.0}, {'customer': 'Lights Unlimited Of Garner', 'revenue': 0.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 0.0}, {'customer': 'LightStyles', 'revenue': 0.0}, {'customer': 'Littman Bros. Lighting', 'revenue': 0.0}, {'customer': 'M & M Lighting', 'revenue': 0.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 0.0}, {'customer': 'Michigan Chandelier', 'revenue': 0.0}, {'customer': 'Progressive Lighting', 'revenue': 0.0}, {'customer': 'Ray Mart Inc. dba Tri Supply Company', 'revenue': 0.0}, {'customer': 'Varaluz LLC', 'revenue': 0.0}, {'customer': 'We Got Lites, Inc.', 'revenue': 0.0}, {'customer': 'Wage Lighting', 'revenue': 0.0}, {'customer': 'Illuminations', 'revenue': 0.0}, {'customer': "Brecher's - Louisville", 'revenue': 0.0}, {'customer': "Cappadonna's", 'revenue': 0.0}, {'customer': 'Cleveland Lighting One', 'revenue': 0.0}, {'customer': 'Elan Studio Lighting', 'revenue': 0.0}, {'customer': 'Envy Interiors', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Distribution Center #320 Grand Prairie', 'revenue': 0.0}] | [{'item': '297B01HG', 'desc': 'Social Club 1 Light Bath - Havana Gold', 'available': 11}, {'item': '297B02HG', 'desc': 'Social Club 2 Light Bath - Havana Gold', 'available': 11}, {'item': '297B03HG', 'desc': 'Social Club 3 Light Bath - Havana Gold', 'available': 7}, {'item': '297P09HG', 'desc': 'Social Club 9 Light 2-Tier Crystal Pendant - Havana Gold', 'available': 7}, {'item': '297P15HG', 'desc': 'Social Club 15 Light 3-Tier Crystal Pendant - Havana Gold', 'available': 6}, {'item': '297B04HG', 'desc': 'Social Club 4 Light Bath - Havana Gold', 'available': 5}] |
| 4DMI0108 | Kye 22x40 Rounded Rectangular Wall Mirror - Gold | KYE | 23,747.72 | 104 | — | 2026-6-24 | [{'customer': 'Studio 41', 'revenue': 3697.12}, {'customer': 'Varaluz LLC', 'revenue': 3116.44}, {'customer': 'Southern Lights', 'revenue': 1975.5}, {'customer': 'Ferguson Enterprises', 'revenue': 1316.98}, {'customer': 'Hermitage Electric Supply', 'revenue': 1227.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 1112.5}, {'customer': 'Beautiful Lights', 'revenue': 998.0}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 735.84}, {'customer': 'BLUE SKY DESIGN OF NWF LLC', 'revenue': 726.54}, {'customer': 'Muska Lighting Center', 'revenue': 703.5}, {'customer': 'Ferguson Enterprises', 'revenue': 564.42}, {'customer': 'First Coast Lighting and Fans', 'revenue': 499.0}, {'customer': "Mahlander's", 'revenue': 499.0}, {'customer': 'Briggs Inc of Omaha', 'revenue': 499.0}, {'customer': "Amini's Galleria", 'revenue': 499.0}, {'customer': 'Alloway Lighting', 'revenue': 492.0}, {'customer': 'Cooks Lighting & Flooring', 'revenue': 409.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 409.0}, {'customer': 'Modern Lighting', 'revenue': 409.0}, {'customer': 'Ferguson Enterprises', 'revenue': 376.28}, {'customer': 'Ferguson Enterprises', 'revenue': 376.28}, {'customer': 'Phillips Lighting & Home, Inc.', 'revenue': 374.25}, {'customer': 'Ferguson Enterprises', 'revenue': 352.82}, {'customer': 'Fusion Light and Design', 'revenue': 260.05}, {'customer': 'Venturi Capital, Inc. DBA Design Superstore', 'revenue': 252.99}, {'customer': 'Maison Kitchen & Bath, LLC', 'revenue': 249.5}, {'customer': 'Ferguson Enterprises', 'revenue': 211.18}, {'customer': 'Posh Lighting', 'revenue': 204.5}, {'customer': 'BR6 - Wiseway Supply - Lexington', 'revenue': 204.5}, {'customer': 'Lumi Lighting & Home Design LLC', 'revenue': 204.5}, {'customer': 'Cleveland Lighting One', 'revenue': 204.5}, {'customer': 'Gross Electric - Toledo', 'revenue': 204.5}, {'customer': 'Shallotte Electric', 'revenue': 204.5}, {'customer': 'Ferguson Enterprises', 'revenue': 169.33}, {'customer': 'Ferguson Enterprises', 'revenue': 9.2}, {'customer': 'Paint Plus Lighting and Design', 'revenue': 0.0}, {'customer': 'Shoreline Property Group', 'revenue': 0.0}, {'customer': '43rd Street Lighting, Inc', 'revenue': 0.0}, {'customer': 'Spectrum Lighting', 'revenue': 0.0}, {'customer': 'Urban Lights', 'revenue': 0.0}, {'customer': 'VAMAC, Inc.', 'revenue': 0.0}, {'customer': 'Varaluz Friends and Family Orders', 'revenue': 0.0}, {'customer': 'Solas Lighting and Design', 'revenue': 0.0}, {'customer': 'Accent Lighting', 'revenue': 0.0}, {'customer': 'Accent Lighting', 'revenue': 0.0}, {'customer': 'All Phase Petoskey', 'revenue': 0.0}, {'customer': 'Black Whale Lighting', 'revenue': 0.0}, {'customer': 'Coventry Lighting Inc', 'revenue': 0.0}, {'customer': 'Dominion Electric Supply', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Focal Point Hardware', 'revenue': 0.0}, {'customer': 'Galleria Lighting', 'revenue': 0.0}, {'customer': 'Inside Source', 'revenue': 0.0}, {'customer': 'Kaelins, Inc.', 'revenue': 0.0}, {'customer': 'Lighting Star', 'revenue': 0.0}, {'customer': 'Lighting World Decorator', 'revenue': 0.0}, {'customer': 'Lighting One of Cincinnati', 'revenue': 0.0}, {'customer': 'LIGHTOPIA WAREHOUSE', 'revenue': 0.0}, {'customer': 'Lights On Banks', 'revenue': 0.0}, {'customer': 'Littman Bros. Lighting', 'revenue': 0.0}, {'customer': 'Lowcountry Lighting Studio', 'revenue': 0.0}, {'customer': 'M & M Glass LLC', 'revenue': 0.0}, {'customer': 'Madison Lighting, Ltd', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': "Montgomery's", 'revenue': 0.0}] | [{'item': '407A02BL', 'desc': 'Kye 24x30 Rectangular Rounded Wall Mirror - Black', 'available': 134}, {'item': '407A04BZ', 'desc': 'Kye 30x30 Rounded Square Wall Mirror - Bronze', 'available': 125}, {'item': '407A02BZ', 'desc': 'Kye 24x30 Rectangular Rounded Wall Mirror - Bronze', 'available': 123}, {'item': '407A06BL', 'desc': 'Kye 40x40 Rounded Square Wall Mirror - Black', 'available': 104}, {'item': '407A04BL', 'desc': 'Kye 30x30 Rounded Square Wall Mirror - Black', 'available': 76}, {'item': '4DMI0109', 'desc': 'Kye 22x40 Rounded Rectangular Wall Mirror - Polished Nickel', 'available': 70}, {'item': '407A02GO', 'desc': 'Kye 24x30 Rectangular Rounded Wall Mirror - Gold', 'available': 46}, {'item': '407A04GO', 'desc': 'Kye 30x30 Rounded Square Wall Mirror - Gold', 'available': 34}, {'item': '4DMI0107', 'desc': 'Kye 22x40 Rounded Rectangular Wall Mirror - Black', 'available': 33}, {'item': '407A06GO', 'desc': 'Kye 40x40 Rounded Square Wall Mirror - Gold', 'available': 2}, {'item': '407A02PN', 'desc': 'Kye 30x24 Rounded Rectangular Wall Mirror - Polished Nickel', 'available': 1}] |
| 376W02BN | Morgan 2 Light Sconce - Brushed Nickel | COL6 | 21,663.60 | 199 | — | 2026-10-16 | [{'customer': 'Wholesale Lighting', 'revenue': 16303.49}, {'customer': 'Luxury Design Inc.', 'revenue': 1716.08}, {'customer': 'Ferguson - Knoxville TN 391', 'revenue': 792.75}, {'customer': 'Elements', 'revenue': 466.2}, {'customer': 'Lighting Originals', 'revenue': 324.36}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 291.6}, {'customer': 'Alloway Lighting', 'revenue': 259.0}, {'customer': 'Muska Lighting Center', 'revenue': 259.0}, {'customer': 'Lighting First', 'revenue': 259.0}, {'customer': 'Urban Lights', 'revenue': 256.41}, {'customer': 'Progressive Lighting', 'revenue': 233.1}, {'customer': 'Peak Lighting', 'revenue': 198.0}, {'customer': 'Lamps Plus/Pacific Coast Lighting', 'revenue': 154.6}, {'customer': 'Lighting Instyle', 'revenue': 150.01}, {'customer': 'Varaluz LLC', 'revenue': 0.0}, {'customer': 'BR6 - Wiseway Supply - Lexington', 'revenue': 0.0}, {'customer': 'Bee Ridge Lighting', 'revenue': 0.0}, {'customer': 'Black Whale Lighting', 'revenue': 0.0}, {'customer': 'Ciana Varaluz Lighting', 'revenue': 0.0}, {'customer': 'Cleveland Lighting South', 'revenue': 0.0}, {'customer': 'Creative Lighting', 'revenue': 0.0}, {'customer': 'Dominion Electric Supply', 'revenue': 0.0}, {'customer': 'Elektra', 'revenue': 0.0}, {'customer': 'A&M Illumination DBA Forest Hill Lighting', 'revenue': 0.0}, {'customer': 'Light House Gallery', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': 'Northern Lighting Inc', 'revenue': 0.0}, {'customer': 'Patdo Electrical Supply Co., Inc.', 'revenue': 0.0}, {'customer': 'Tallahassee Lighting', 'revenue': 0.0}] | [{'item': '376W03BL', 'desc': 'Morgan 3 Light Sconce - Black', 'available': 111}, {'item': '376W03BN', 'desc': 'Morgan 3 Light Sconce - Brushed Nickel', 'available': 94}, {'item': '376W02BL', 'desc': 'Morgan 2 Light Sconce - Black', 'available': 71}, {'item': '376W03SB', 'desc': 'Morgan 3 Light Sconce - Satin Brass', 'available': 59}, {'item': '376B03BN', 'desc': 'Morgan 3 Light Bath - Brushed Nickel', 'available': 54}, {'item': '376B04BN', 'desc': 'Morgan 4 Light Bath - Brushed Nickel', 'available': 44}, {'item': '376B04BL', 'desc': 'Morgan 4 Light Bath - Black', 'available': 42}, {'item': '376B03BL', 'desc': 'Morgan 3 Light Bath - Black', 'available': 42}, {'item': '376W02SB', 'desc': 'Morgan 2 Light Sconce - Satin Brass', 'available': 41}, {'item': '376W01SB', 'desc': 'Morgan 1 Light Sconce - Satin Brass', 'available': 40}, {'item': '376B03SB', 'desc': 'Morgan 3 Light Bath - Satin Brass', 'available': 30}, {'item': '376B04SB', 'desc': 'Morgan 4 Light Bath - Satin Brass', 'available': 10}, {'item': '376W01BL', 'desc': 'Morgan 1 Light Sconce - Black', 'available': 10}] |
| 309P03HG | Matrix 3 Light Pendant - Havana Gold | COL1 | 19,915.02 | 40 | — | 2026-6-26 | [{'customer': 'Light Source Lighting', 'revenue': 3417.0}, {'customer': 'Beautiful Things Lighting', 'revenue': 2847.5}, {'customer': 'N&S Electric Supply', 'revenue': 1423.5}, {'customer': 'Ferguson Enterprises', 'revenue': 1309.62}, {'customer': 'Ferguson Enterprises', 'revenue': 1225.44}, {'customer': 'Ferguson Enterprises', 'revenue': 1098.9}, {'customer': 'Wholesale Lighting', 'revenue': 949.0}, {'customer': 'Ferguson Enterprises', 'revenue': 873.08}, {'customer': 'Fort Worth Lighting', 'revenue': 569.5}, {'customer': 'Fan & Lighting World', 'revenue': 541.02}, {'customer': 'Raymond de Steiger, Inc.', 'revenue': 508.24}, {'customer': 'LED Capstone LLC', 'revenue': 474.5}, {'customer': 'Southern Lights', 'revenue': 474.5}, {'customer': 'Spectrum Lighting', 'revenue': 474.5}, {'customer': 'Lights Unlimited Of Garner', 'revenue': 474.5}, {'customer': 'Ferguson Enterprises', 'revenue': 436.54}, {'customer': 'Ferguson Enterprises', 'revenue': 436.54}, {'customer': 'Ferguson Enterprises', 'revenue': 436.54}, {'customer': '1800Lighting - Capitol Lighting', 'revenue': 427.05}, {'customer': 'Lighting First', 'revenue': 427.05}, {'customer': 'Winnelson Hendersonville', 'revenue': 379.0}, {'customer': 'The Bulb Bin', 'revenue': 284.75}, {'customer': 'Ferguson Enterprises', 'revenue': 237.25}, {'customer': 'Ferguson Enterprises', 'revenue': 189.5}, {'customer': 'Illuminations', 'revenue': 0.0}, {'customer': 'Lighting Instyle', 'revenue': 0.0}, {'customer': 'Lamps Plus/Pacific Coast Lighting', 'revenue': 0.0}, {'customer': 'Lighting First', 'revenue': 0.0}, {'customer': 'Lighting Resource Studio', 'revenue': 0.0}, {'customer': 'Lighting Star', 'revenue': 0.0}, {'customer': 'Light Innovations', 'revenue': 0.0}, {'customer': 'Lighting Etc', 'revenue': 0.0}, {'customer': 'LIGHTOPIA WAREHOUSE', 'revenue': 0.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 0.0}, {'customer': 'Lights of Oconee', 'revenue': 0.0}, {'customer': 'Littman Bros. Lighting', 'revenue': 0.0}, {'customer': 'Lumber One Home Center', 'revenue': 0.0}, {'customer': 'Lumen Nation', 'revenue': 0.0}, {'customer': 'Madison Creek Furnishings and Design', 'revenue': 0.0}, {'customer': 'Mechanical Electrical Wholesale Supply, Inc.', 'revenue': 0.0}, {'customer': 'Modern Lighting', 'revenue': 0.0}, {'customer': 'Matchez International Inc dba Parkyn Design', 'revenue': 0.0}, {'customer': 'Pine Tree Lighting', 'revenue': 0.0}, {'customer': 'Progressive Lighting', 'revenue': 0.0}, {'customer': 'Rbdelaa Lighting', 'revenue': 0.0}, {'customer': 'Rensen House of Lights', 'revenue': 0.0}, {'customer': 'Royce Collection', 'revenue': 0.0}, {'customer': 'Signature Lighting and Fans', 'revenue': 0.0}, {'customer': 'Sunbelt Lighting LLC', 'revenue': 0.0}, {'customer': 'The Lighting Boutique', 'revenue': 0.0}, {'customer': "Eclairage Union Montreal-La Cie D'eclairage Union", 'revenue': 0.0}, {'customer': 'Universal Lamp', 'revenue': 0.0}, {'customer': 'Urban Lights', 'revenue': 0.0}, {'customer': 'Versallies', 'revenue': 0.0}, {'customer': 'ABC Creations LLC', 'revenue': 0.0}, {'customer': 'Elume Distinctive Lighting', 'revenue': 0.0}, {'customer': '1800Lighting - Capitol Lighting', 'revenue': 0.0}, {'customer': 'LBU Lighting', 'revenue': 0.0}, {'customer': 'CLIVE DANIEL HOME - WAREHOUSE', 'revenue': 0.0}, {'customer': 'Colonial Electric Supply Company. Inc', 'revenue': 0.0}, {'customer': 'Coventry Lighting Inc', 'revenue': 0.0}, {'customer': 'Cregger Company, Inc.', 'revenue': 0.0}, {'customer': 'Dement Lighting', 'revenue': 0.0}, {'customer': 'Designer Lighting and Fan Inc', 'revenue': 0.0}, {'customer': 'Epiphany', 'revenue': 0.0}, {'customer': 'Ethan and Associates', 'revenue': 0.0}, {'customer': 'Farmville Wholesale Electric Supply Co.', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'First Coast Lighting and Fans', 'revenue': 0.0}, {'customer': "Graham's Lighting Franklin", 'revenue': 0.0}] | [{'item': '309W02LHG', 'desc': 'Matrix 2 Light 2-Tier Sconce - Havana Gold', 'available': 30}, {'item': '309W02LMBFG', 'desc': 'Matrix 2 Light 2-Tier Sconce - Matte Black/French Gold', 'available': 29}, {'item': '309W02HG', 'desc': 'Matrix 2 Light Sconce - Havana Gold', 'available': 24}, {'item': '309P12HG', 'desc': 'Matrix 12 Light Pendant - Havana Gold', 'available': 23}, {'item': '309P10HG', 'desc': 'Matrix 10 Light Pendant - Havana Gold', 'available': 19}, {'item': '309P06HG', 'desc': 'Matrix 6 Light Pendant - Havana Gold', 'available': 17}, {'item': '309B03MBFG', 'desc': 'Matrix 3 Light Bath - Matte Black/French Gold', 'available': 17}, {'item': '309P09MBFG', 'desc': 'Matrix 9 Light Pendant - Matte Black/French Gold', 'available': 17}, {'item': '309C30HG', 'desc': 'Matrix 30Light 4-Tier Chandelier - Havana Gold', 'available': 14}, {'item': '309C19HG', 'desc': 'Matrix 18 Light 3-Tier Chandelier - Havana Gold', 'available': 13}, {'item': '309T03MBFG', 'desc': 'Matrix 3 Light Table Lamp - Matte Black/French Gold', 'available': 12}, {'item': '309N06HG', 'desc': 'Matrix 6 Light Linear - Havana Gold', 'available': 12}, {'item': '309N06MBFG', 'desc': 'Matrix 6 Light Linear Pendant - Matte Black/French Gold', 'available': 10}, {'item': '309W01MBFG', 'desc': 'Matrix 1 Light Sconce - Matte Black/French Gold', 'available': 10}, {'item': '309N08HG', 'desc': 'Matrix 8 Light Linear - Havana Gold', 'available': 10}, {'item': '309L06MBFG', 'desc': 'Matrix 6 Light Floor Lamp - Matte Black/French Gold', 'available': 10}, {'item': '309P03MBFG', 'desc': 'Matrix 3 Light Pendant - Matte Black/French Gold', 'available': 9}, {'item': '309C14MBFG', 'desc': 'Matrix 14 Light 2-Tier Chandelier - Matte Black/French Gold', 'available': 9}, {'item': '309N12MBFG', 'desc': 'Matrix 12 Light Linear - Matte Black & French Gold', 'available': 9}, {'item': '309P06MBFG', 'desc': 'Matrix 6 Light Pendant - Matte Black/French Gold', 'available': 9}, {'item': '309C19MBFG', 'desc': 'Matrix 18 Light 3-Tier Chandelier - Matte Black/French Gold', 'available': 9}, {'item': '309W01HG', 'desc': 'Matrix 1 Light Sconce - Havana Gold', 'available': 8}, {'item': '309C14HG', 'desc': 'Matrix 14 Light 2-Tier Chandelier - Havana Gold', 'available': 7}, {'item': '309N10MBFG', 'desc': 'Matrix 10 Light Linear - Matte Black & French Gold', 'available': 7}, {'item': '309L06HG', 'desc': 'Matrix 6 Light Floor Lamp - Havana Gold', 'available': 7}, {'item': '309P12MBFG', 'desc': 'Matrix 12 Light Pendant - Matte Black/French Gold', 'available': 7}, {'item': '309T03HG', 'desc': 'Matrix 3 Light Table Lamp - Havana Gold', 'available': 7}, {'item': '309P09HG', 'desc': 'Matrix 9 Light Pendant - Havana Gold', 'available': 6}, {'item': '309B03HG', 'desc': 'Matrix 3 Light Bath - Havana Gold', 'available': 6}, {'item': '309P10MBFG', 'desc': 'Matrix 10 Light Pendant - Matte Black/French Gold', 'available': 6}, {'item': '309N12HG', 'desc': 'Matrix 12 Light Linear - Havana Gold', 'available': 6}, {'item': '309N08MBFG', 'desc': 'Matrix 8 Light Linear Pendant - Matte Black/French Gold', 'available': 4}, {'item': '309N10HG', 'desc': 'Matrix 10 Light Linear - Havana Gold', 'available': 4}, {'item': '309B02HG', 'desc': 'Matrix 2 Light Bath - Havana Gold', 'available': 3}, {'item': '309C30MBFG', 'desc': 'Matrix 30Light 4-Tier Chandelier - Matte Black/French Gold', 'available': 3}, {'item': '309B02MBFG', 'desc': 'Matrix 2 Light Bath - Matte Black/French Gold', 'available': 2}] |
| 380P05MBFG | Estela 5 Light Pendant - Matte Black/French Gold | COL62 | 15,066.97 | 19 | — | 2026-6-29 | [{'customer': 'CARMEL COLOR HOUSE', 'revenue': 3233.39}, {'customer': 'Georgia Lighting', 'revenue': 2758.83}, {'customer': 'Wilson Lighting - Overland Park KS', 'revenue': 2293.5}, {'customer': 'Light Bulbs Etc. - Costa Mesa', 'revenue': 1824.5}, {'customer': 'Danielhouse Studios Inc', 'revenue': 764.5}, {'customer': 'BR6 - Wiseway Supply - Lexington', 'revenue': 764.5}, {'customer': 'City Lights', 'revenue': 764.5}, {'customer': 'Cleveland Lighting One', 'revenue': 764.5}, {'customer': 'Cleveland Lighting South', 'revenue': 764.5}, {'customer': 'BBC Lighting', 'revenue': 764.5}, {'customer': 'Naples Lighting and Fan Depot', 'revenue': 369.75}, {'customer': "Brecher's - Louisville", 'revenue': 0.0}] | [{'item': '380M01MBFG', 'desc': 'Estela 1 Light Mini Pendant - Matte Black/French Gold', 'available': 13}, {'item': '380MI30AMBFG', 'desc': 'Estela 30-in Round Wall Mirror - Matte Black/French Gold', 'available': 9}, {'item': '380W02MBFG', 'desc': 'Estela 2 Light Sconce - Matte Black/French Gold', 'available': 7}, {'item': '380N05MBFG', 'desc': 'Estela 5 Light Linear Pendant - Matte Black/French Gold', 'available': 6}, {'item': '380P03MBFG', 'desc': 'Estela 3 Light Convertible Pendant/Semi-Flush - Matte Black/French Gold', 'available': 6}, {'item': '380MI30BMBFG', 'desc': 'Estela 30x40 Rectangular Wall Mirror - Matte Black/French Gold', 'available': 5}, {'item': '380F06MBFG', 'desc': 'Estela 6 Light Foyer - Matte Black/French Gold', 'available': 4}, {'item': '380N06MBFG', 'desc': 'Estela 6 Light   Linear Pendant - Matte Black/French Gold', 'available': 1}] |
| 348N06HG | Kato 6 Light Oval Pendant - Havana Gold | KATO | 13,334.16 | 18 | — | 2026-7-31 | [{'customer': 'Lighting First', 'revenue': 2794.85}, {'customer': 'Lighting First', 'revenue': 2714.4}, {'customer': 'Light Source Lighting', 'revenue': 1641.16}, {'customer': 'Hills Lighting', 'revenue': 1609.0}, {'customer': 'Fort Worth Lighting', 'revenue': 904.5}, {'customer': 'CARMEL COLOR HOUSE', 'revenue': 884.95}, {'customer': 'The Nest DBA Cregger Company', 'revenue': 804.5}, {'customer': "Mahlander's", 'revenue': 804.5}, {'customer': 'Elements', 'revenue': 724.05}, {'customer': 'Lighting First', 'revenue': 452.25}, {'customer': 'Rensen House of Lights', 'revenue': 0.0}, {'customer': 'Rittenhouse Electric', 'revenue': 0.0}, {'customer': 'Riverside Lighting and Electric', 'revenue': 0.0}, {'customer': 'Salt Box', 'revenue': 0.0}, {'customer': 'Acropolis', 'revenue': 0.0}, {'customer': 'Sunbelt Lighting LLC', 'revenue': 0.0}, {'customer': 'Cartwright Lighting and Furniture Ltd.', 'revenue': 0.0}, {'customer': "Christie's Lighting Gallery", 'revenue': 0.0}, {'customer': 'CLIVE DANIEL HOME - WAREHOUSE', 'revenue': 0.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'The Light House of Lewes', 'revenue': 0.0}, {'customer': 'Lighting World Decorator', 'revenue': 0.0}, {'customer': 'Park Lighting', 'revenue': 0.0}, {'customer': 'Progressive Lighting', 'revenue': 0.0}] | [{'item': '348W02HG', 'desc': 'Kato 2 Light Wall Sconce - Havana Gold', 'available': 13}, {'item': '348P06CB', 'desc': 'Kato 6 Light Pendant - Carbon Black', 'available': 12}, {'item': '348P06HG', 'desc': 'Kato 6 Light Pendant - Havana Gold', 'available': 10}, {'item': '348W02CB', 'desc': 'Kato 2 Light Wall Sconce - Carbon Black', 'available': 10}, {'item': '348P04HG', 'desc': 'Kato 4 Light 3-Tier Pendant - Havana Gold', 'available': 9}, {'item': '348F16CB', 'desc': 'Kato 16 Light 3-Tier Foyer - Carbon', 'available': 9}, {'item': '348P05HG', 'desc': 'Kato 5 Light Pendant - Havana Gold', 'available': 6}, {'item': '348S05CB', 'desc': 'Kato 5 Light Convertible Semi-Flush/Pendant - Carbon', 'available': 5}, {'item': '348S06HG', 'desc': 'Kato 6 Light Convertible Semi-Flush/Pendant - Havana Gold', 'available': 5}, {'item': '348S06CB', 'desc': 'Kato 6 Light Convertible Semi-Flush/Pendant - Carbon', 'available': 5}, {'item': '348F16HG', 'desc': 'Kato 16 Light 3-Tier Foyer - Havana Gold', 'available': 4}, {'item': '348P05CB', 'desc': 'Kato 5 Light Pendant - Carbon Black', 'available': 2}, {'item': '348P04CB', 'desc': 'Kato 4 Light 3-Tier Pendant - Carbon Black', 'available': 1}, {'item': '348N06CB', 'desc': 'Kato 6 Light Oval Pendant - Carbon Black', 'available': 1}, {'item': '348S05HG', 'desc': 'Kato 5 Light Convertible Semi-Flush/Pendant - Havana Gold', 'available': 1}] |
| 297P19HG | Social Club 19 Light 4-Tier - Havana Gold | COL15 | 12,091.69 | 8 | — | 2026-6-26 | [{'customer': 'Hunzicker Brothers', 'revenue': 2094.5}, {'customer': 'Versallies', 'revenue': 1844.5}, {'customer': 'Cleveland Lighting One', 'revenue': 1844.5}, {'customer': 'Lighting Instyle', 'revenue': 1844.5}, {'customer': 'Lee Supply', 'revenue': 1844.5}, {'customer': 'Ferguson Enterprises', 'revenue': 1696.94}, {'customer': 'Ferguson Distribution Center #320 Grand Prairie', 'revenue': 922.25}, {'customer': 'Home Lighting', 'revenue': 0.0}, {'customer': 'Hubbard Pipe & Supply, Inc', 'revenue': 0.0}, {'customer': 'Illuminations - McAllen TX', 'revenue': 0.0}, {'customer': 'Lamps Plus/Pacific Coast Lighting', 'revenue': 0.0}, {'customer': 'Lampworks, Inc dba Lamp & Shade Works, Inc.', 'revenue': 0.0}, {'customer': 'Lando Lighting', 'revenue': 0.0}, {'customer': 'Lighting by Fox', 'revenue': 0.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 0.0}, {'customer': 'Luz Love', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': 'Michigan Chandelier', 'revenue': 0.0}, {'customer': 'Modern Lighting', 'revenue': 0.0}, {'customer': "Montgomery's", 'revenue': 0.0}, {'customer': 'Robinson Lighting - Winnipeg', 'revenue': 0.0}, {'customer': 'Texas Lighting & More', 'revenue': 0.0}, {'customer': 'Varaluz LLC', 'revenue': 0.0}, {'customer': 'Northwest Interiors dba Champions Lighting', 'revenue': 0.0}, {'customer': 'Wendy Mayes Design', 'revenue': 0.0}, {'customer': 'Ciana Varaluz Lighting', 'revenue': 0.0}, {'customer': 'Coventry Lighting Inc', 'revenue': 0.0}, {'customer': 'Denali Lighting One', 'revenue': 0.0}, {'customer': 'Designer Lighting and Fan Inc', 'revenue': 0.0}, {'customer': 'Ethan and Associates', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}] | [{'item': '297B01HG', 'desc': 'Social Club 1 Light Bath - Havana Gold', 'available': 11}, {'item': '297B02HG', 'desc': 'Social Club 2 Light Bath - Havana Gold', 'available': 11}, {'item': '297B03HG', 'desc': 'Social Club 3 Light Bath - Havana Gold', 'available': 7}, {'item': '297P09HG', 'desc': 'Social Club 9 Light 2-Tier Crystal Pendant - Havana Gold', 'available': 7}, {'item': '297P15HG', 'desc': 'Social Club 15 Light 3-Tier Crystal Pendant - Havana Gold', 'available': 6}, {'item': '297B04HG', 'desc': 'Social Club 4 Light Bath - Havana Gold', 'available': 5}] |
| 389P06MBHN | Blonde Moment 6 Light   Pendant - Matte Black/Honey/Medium Oak | COL67 | 11,456.18 | 18 | — | 2026-7-30 | [{'customer': 'Lyteworks', 'revenue': 1708.5}, {'customer': 'PDI', 'revenue': 1139.0}, {'customer': 'IBS LIGHTING LTD', 'revenue': 829.19}, {'customer': 'The Light Center', 'revenue': 736.8}, {'customer': 'Lighting Star', 'revenue': 664.5}, {'customer': 'N&S Electric Supply', 'revenue': 664.5}, {'customer': 'Dulles Electric Supply Corp', 'revenue': 664.5}, {'customer': 'Kenneth Ludwig Chicago', 'revenue': 645.29}, {'customer': 'Urban Lights', 'revenue': 612.81}, {'customer': 'Ferguson - Knoxville TN 391', 'revenue': 611.34}, {'customer': 'Lighting Instyle', 'revenue': 569.5}, {'customer': 'The Nest DBA Cregger Company', 'revenue': 569.5}, {'customer': 'Greer Lighting Center, LLC', 'revenue': 569.5}, {'customer': "Hagen's Lighting", 'revenue': 569.5}, {'customer': 'Avid Lighting', 'revenue': 569.5}, {'customer': 'Cabinet & Lighting Supply', 'revenue': 332.25}, {'customer': 'Madison Creek Furnishings and Design', 'revenue': 0.0}, {'customer': 'Lighting First', 'revenue': 0.0}, {'customer': 'Lights and More', 'revenue': 0.0}, {'customer': 'Southern Lights', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'First Coast Lighting and Fans', 'revenue': 0.0}] | [{'item': '389W01MBHN', 'desc': 'Blonde Moment 1 Light   Sconce - Matte Black/Honey/Medium Oak', 'available': 14}, {'item': '389N05MBHN', 'desc': 'Blonde Moment 5 Light   Linear Pendant - Matte Black/Honey/Medium Oak', 'available': 10}, {'item': '389S03MBHN', 'desc': 'Blonde Moment 3 Light   Semi-Flush - Matte Black/Honey/Medium Oak', 'available': 4}] |
| 345C21CBHG | Windsor 21 Light 4-Tier Crystal Chandelier - Carbon/Havana Gold | COL7 | 10,797.04 | 2 | — | 2026-7-17 | [{'customer': 'Frost Interiors Inc', 'revenue': 5997.44}, {'customer': 'Texas Lighting & More', 'revenue': 4799.6}, {'customer': 'Colonial Electric Supply Company. Inc', 'revenue': 0.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 0.0}, {'customer': 'Illuminations - McAllen TX', 'revenue': 0.0}, {'customer': 'Lampworks, Inc dba Lamp & Shade Works, Inc.', 'revenue': 0.0}, {'customer': 'Lando Lighting', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}, {'customer': 'PDI', 'revenue': 0.0}, {'customer': 'Showcase Lighting by 3G', 'revenue': 0.0}, {'customer': 'Ray Mart Inc. dba Tri Supply Company', 'revenue': 0.0}, {'customer': 'Builder Specialties, Inc', 'revenue': 0.0}, {'customer': 'Turn On Lighting', 'revenue': 0.0}, {'customer': '1800Lighting - Capitol Lighting', 'revenue': 0.0}] | [{'item': '345W01CBHG', 'desc': 'Windsor 1 Light Crystal Sconce - Carbon/Havana Gold', 'available': 23}, {'item': '345W01FGMB', 'desc': 'Windsor 1 Light Crystal Sconce - French Gold/Matte Black', 'available': 19}, {'item': '345P04FGMB', 'desc': 'Windsor 4 Light Crystal Pendant - French Gold/Matte Black', 'available': 16}, {'item': '345W02SFGMB', 'desc': 'Windsor 2 Light Small Crystal Sconce - French Gold/Matte Black', 'available': 11}, {'item': '345C13CBHG', 'desc': 'Windsor 13 Light 3-Tier Crystal Chandelier - Carbon/Havana Gold', 'available': 11}, {'item': '345W02CBHG', 'desc': 'Windsor 2 Light Crystal Sconce/Bath - Carbon/Havana Gold', 'available': 10}, {'item': '345B03FGMB', 'desc': 'Windsor 3 Light Crystal Bath - French Gold/Matte Black', 'available': 10}, {'item': '345W02SCBHG', 'desc': 'Windsor 2 Light Crystal Sconce - Carbon/Havana Gold', 'available': 10}, {'item': '345P01CBHG', 'desc': 'Windsor 1 Light Crystal Pendant - Carbon/Havana Gold', 'available': 10}, {'item': '345P06CBHG', 'desc': 'Windsor 6 Light Crystal Pendant - Carbon/Havana Gold', 'available': 10}, {'item': '345C07CBHG', 'desc': 'Windsor 7 Light 2-Tier Crystal Chandelier - Carbon/Havana Gold', 'available': 9}, {'item': '345B04CBHG', 'desc': 'Windsor 4 Light Crystal Bath - Carbon/Havana Gold', 'available': 8}, {'item': '345B03CBHG', 'desc': 'Windsor 3 Light Crystal Bath - Carbon/Havana Gold', 'available': 7}, {'item': '345W02FGMB', 'desc': 'Windsor 2 Light Crystal Sconce - French Gold/Matte Black', 'available': 6}, {'item': '345P06FGMB', 'desc': 'Windsor 6 Light Crystal Pendant - French Gold/Matte Black', 'available': 6}, {'item': '345C07FGMB', 'desc': 'Windsor 7 Light 2-Tier Crystal Chandelier - French Gold/Matte Black', 'available': 6}, {'item': '345N08CBHG', 'desc': 'Windsor 8 Light Crystal Oval Linear Pendant - Carbon/Havana Gold', 'available': 5}, {'item': '345C13FGMB', 'desc': 'Windsor 13 Light 3-Tier Crystal Chandelier - French Gold/Matte Black', 'available': 5}, {'item': '345P01FGMB', 'desc': 'Windsor 1 Light Crystal Pendant - French Gold/Matte Black', 'available': 4}, {'item': '345N08FGMB', 'desc': 'Windsor 8 Light Oval Crystal Linear Pendant - French Gold/Matte Black', 'available': 4}, {'item': '345C21FGMB', 'desc': 'Windsor 21 Light 4-Tier Crystal Chandelier - French Gold/Matte Black', 'available': 3}, {'item': '345P04CBHG', 'desc': 'Windsor 4 Light Crystal Pendant - Carbon/Havana Gold', 'available': 1}] |
| 434MI22CH | Capsule 22x40 Mirror - Chrome | COL69 | 9,975.40 | 45 | — | 2026-9-15 | [{'customer': 'Cleveland Lighting One', 'revenue': 1975.5}, {'customer': 'Dominion Electric Supply', 'revenue': 1497.0}, {'customer': 'Lights of Oconee', 'revenue': 499.0}, {'customer': 'Fort Worth Lighting', 'revenue': 469.0}, {'customer': 'Ferguson ENTERPRISES', 'revenue': 459.08}, {'customer': 'Southern Lights', 'revenue': 439.0}, {'customer': 'The Light Center', 'revenue': 439.0}, {'customer': "Amini's Galleria", 'revenue': 439.0}, {'customer': 'Ferguson Enterprises', 'revenue': 403.88}, {'customer': 'Ferguson Enterprises', 'revenue': 403.88}, {'customer': 'Ferguson Enterprises', 'revenue': 403.88}, {'customer': 'Mars Electric Co.', 'revenue': 395.1}, {'customer': '43rd Street Lighting, Inc', 'revenue': 316.27}, {'customer': 'Dominion Electric Supply', 'revenue': 297.08}, {'customer': 'North Coast Lighting', 'revenue': 249.5}, {'customer': 'Ferguson Enterprises', 'revenue': 229.54}, {'customer': 'Pace Lighting Inc.', 'revenue': 219.5}, {'customer': 'Lighting Etc', 'revenue': 219.5}, {'customer': 'Maison Kitchen & Bath, LLC', 'revenue': 219.5}, {'customer': 'Ferguson Enterprises', 'revenue': 201.94}, {'customer': 'Ferguson Enterprises', 'revenue': 109.75}, {'customer': 'Ferguson Enterprises', 'revenue': 89.5}, {'customer': 'Modern Lighting', 'revenue': 0.0}, {'customer': 'The Nest DBA Cregger Company', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Black Whale Lighting', 'revenue': 0.0}, {'customer': 'Inline Lighting', 'revenue': 0.0}, {'customer': 'Lumber One Home Center', 'revenue': 0.0}, {'customer': 'Ferguson Enterprises', 'revenue': 0.0}, {'customer': 'Masterpiece Lighting - Atlanta', 'revenue': 0.0}, {'customer': 'Metro Lighting', 'revenue': 0.0}] | [{'item': '434MI24CH', 'desc': 'Capsule 24x60 Mirror - Chrome', 'available': 24}, {'item': '434MI24BL', 'desc': 'Capsule 24x60 Mirror - Black', 'available': 14}, {'item': '434MI22BL', 'desc': 'Capsule 22x40 Mirror - Black', 'available': 4}, {'item': '434MI24GO', 'desc': 'Capsule 24x60 Mirror - Gold', 'available': 1}] |
