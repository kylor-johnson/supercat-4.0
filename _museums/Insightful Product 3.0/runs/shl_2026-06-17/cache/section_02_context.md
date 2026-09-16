# Section 2 Context Bundle — Savoy House Lighting (shl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=209029, portal_order_gmv=$50.0M |
| HAS_INVENTORY | True | inventory_count=3139 |
| HAS_SALES_DATA | True | sales_data_count=140638 |
| HAS_SALES_SECTION | True | mode=orders order_reps=18 engagement_reps=0 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | shl_ecat_online |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$50.0M > ecat_gmv=$3.4M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 18 | 18 |
| ENGAGEMENT_REP_COUNT | 0 |  |
| SALES_SECTION_MODE | orders | orders |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 84 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 653, Mixpanel total submit_order (Q-01): 543 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=89.3%, ambiguous_rate=6.7%, showroom_event_share=0.6% |
| USER_GROUP_JOIN_RATE | 89% | 75 of 84 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 1% | showroom+admin share of matched events: 0.6% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Jessica Romero |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1139 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=827 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Savoy House Lighting
- **Shortname**: shl
- **Org ID**: 41
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | True |
| PORTAL_ORDERS_FRESH | False |
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
| §3 Customer | STRONG | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | STRONG | See Derived Gate 6 §5 formula |

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

# Signal Rank — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Total signals fired**: 59 (P0: 45, P1: 13, P2: 1)
- **Org GMV**: $3.4M eCat LTM, $50.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders | P1 | §2 Accounts | 8.3 | $8,268,334 | 2.0 | 136,730,694 | POSITIVE |
| 2 | SIG-ANOMALY-02 | Stock Out — 9-302-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $507,979 LTM, 0 available | P0 | §3 Product | 10.0 | $507,979 | 3.0 | 15,239,379 | RISK |
| 3 | SIG-MOM-01 | Account Acceleration — Shades Of Light 2 consecutive QoQ acceleration quarters, $867,672 peak quarter (+119% QoQ) | P0 | §2 Accounts | 4.0 | $867,672 | 3.0 | 10,333,979 | POSITIVE |
| 4 | SIG-ANOMALY-02 | Stock Out — 1-2221-6-322 (Salerno 6-Light Chandelier in Warm Brass) $303,275 LTM, 0 available | P0 | §3 Product | 10.0 | $303,275 | 3.0 | 9,098,262 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 7-1804-4-322 (Crawford 4-Light Pendant in Warm Brass) $286,652 LTM, 0 available | P0 | §3 Product | 10.0 | $286,652 | 3.0 | 8,599,568 | RISK |
| 6 | SIG-DECAY-04 | Spending Contraction — Shades Of Light -40.8% YoY ($2,915,999→$1,725,093), $1,190,906 gap | P0 | §2 Accounts | 2.0 | $1,190,906 | 3.0 | 7,288,344 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 7-1774-6-320 (Ashburn 6-Light Pendant in Warm Brass an) $233,394 LTM, 0 available | P0 | §3 Product | 10.0 | $233,394 | 3.0 | 7,001,821 | RISK |
| 8 | SIG-COMMERCE-01 | Capture Rate — eCat captures 6.8% of $50M total business; each +1pt = $500K | P0 | §4 Commerce | 4.7 | $500,000 | 3.0 | 6,990,000 | POSITIVE |
| 9 | SIG-DECAY-04 | Spending Contraction — Lighting Connection Lp -64.0% YoY ($926,397→$333,632), $592,765 gap | P0 | §2 Accounts | 3.2 | $592,765 | 3.0 | 5,690,545 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 1-312-15-322 (Middleton 15-Light Chandelier in Warm Br) $188,670 LTM, 0 available | P0 | §3 Product | 10.0 | $188,670 | 3.0 | 5,660,094 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 9-303-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $186,435 LTM, 0 available | P0 | §3 Product | 10.0 | $186,435 | 3.0 | 5,593,063 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — M60008NB (2-Light Ceiling Light in Natural Brass) $163,303 LTM, 0 available | P0 | §3 Product | 10.0 | $163,303 | 3.0 | 4,899,087 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 9-7144-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $162,681 LTM, 0 available | P0 | §3 Product | 10.0 | $162,681 | 3.0 | 4,880,422 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 7-2918-1-156 (Alta 1-Light Pendant in Concrete and Bra) $147,450 LTM, 0 available | P0 | §3 Product | 10.0 | $147,450 | 3.0 | 4,423,505 | RISK |
| 15 | SIG-ANOMALY-03 | Competitive Displacement — Sunbelt /Mississippi total biz +39% but eCat -83% | P0 | §2 Accounts | 8.1 | $97,748 | 3.0 | 2,387,015 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — Capital Electric 2 consecutive QoQ acceleration quarters, $43,171 peak quarter (+378% QoQ) | P0 | §2 Accounts | 12.6 | $43,171 | 3.0 | 1,631,423 | POSITIVE |
| 17 | SIG-DECAY-01 | Reorder Decay — Dement Lighting 7.8x normal gap (321d vs 41d avg) | P0 | §2 Accounts | 7.8 | $58,302 | 3.0 | 1,364,267 | RISK |
| 18 | SIG-MOM-01 | Account Acceleration — BELAMI 2 consecutive QoQ acceleration quarters, $271,678 peak quarter (+48% QoQ) | P0 | §2 Accounts | 1.6 | $271,678 | 3.0 | 1,312,206 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — St Louis Metro Electric 2 consecutive QoQ acceleration quarters, $69,827 peak quarter (+175% QoQ) | P0 | §2 Accounts | 5.8 | $69,827 | 3.0 | 1,221,975 | POSITIVE |
| 20 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 48% of eCat GMV | P1 | §4 Commerce | 1.2 | $410,802 | 2.0 | 995,505 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 35 | 1 | 0 | 36 | |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 0 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Shades Of Light 2 consecutive QoQ acceleration quarters, $867,672 peak quarter (+119% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 6.8% of $50M total business; each +1pt = $500K
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Capital Electric 2 consecutive QoQ acceleration quarters, $43,171 peak quarter (+378% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 9-302-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $507,979 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 1-2221-6-322 (Salerno 6-Light Chandelier in Warm Brass) $303,275 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 7-1804-4-322 (Crawford 4-Light Pendant in Warm Brass) $286,652 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | Dement Lighting | 2 | DECAY-01, MOM-01 | $58,302 |
| 2 | Shades Of Light | 2 | DECAY-04, MOM-01 | $1,190,906 |
| 3 | Hermitage Lighting Gallery | 2 | DECAY-04, MOM-01 | $63,423 |
| 4 | Elements | 2 | ANOMALY-03, MOM-01 | $29,405 |
| 5 | Lighting Connection Lp | 1 | DECAY-04 | $592,765 |
| 6 | Plumbing Distributors Inc dba PDI | 1 | DECAY-04 | $69,493 |
| 7 | Lamps.com | 1 | DECAY-04 | $60,628 |
| 8 | Graham's Lighting Inc | 1 | DECAY-04 | $58,661 |
| 9 | The Brecher Co., Inc | 1 | DECAY-04 | $58,283 |
| 10 | Aztec Lighting Inc. | 1 | DECAY-04 | $54,924 |

### Q-12_results.md

# Q-12 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 1,353 | 958 | 320 | 264 | 48 |

### Q-14_results.md

# Q-14 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 71568 | Asburys Design | 26 | $12,309 | 2025-07-15 18:47:03 | 2026-06-02 14:43:25 | 12.90 |
| 70599 | The Light Brothers | 18 | $4,795 | 2025-07-28 20:19:47 | 2026-05-30 21:07:48 | 18 |
| 72417 | Weathered Finishes LLC DBA Nouvelle Lighting | 14 | $5,142 | 2025-09-18 22:33:11 | 2026-05-30 20:00:12 | 19.50 |
| 71943 | Your Lighting Source, LLC | 11 | $2,215 | 2025-08-11 13:54:00 | 2026-06-15 13:50:25 | 30.80 |
| 71003 | Virginia-Carolina Lighting Inc dba Coastal Lighting & Supply | 11 | $7,960 | 2025-07-15 17:34:22 | 2026-06-02 12:08:25 | 32.20 |
| 71582 | Meuth Wallpaper dba Sugar Bakers | 9 | $6,021 | 2025-09-04 21:13:10 | 2026-06-08 16:25:54 | 34.60 |
| 70764 | Sunbelt / Louisiana | 7 | $106,339 | 2025-06-18 19:26:59 | 2026-01-10 19:18:33 | 34.30 |
| 71824 | MADISON CREEK FURNISHINGS & DESIGN | 7 | $5,258 | 2025-07-15 20:02:18 | 2025-09-11 16:02:33 | 9.60 |
| 72544 | Shelly Orr Interiors | 7 | $12,330 | 2025-07-11 17:45:41 | 2025-11-10 17:37:51 | 20.30 |
| 72193 | Liza Joyner Designs Ryser | 7 | $2,199 | 2025-06-27 12:48:54 | 2026-06-16 19:22:18 | 59 |
| 72126 | FISHTRAP CREEK LIGHTING LLC | 6 | $1,121 | 2025-08-08 18:24:37 | 2026-02-25 17:36:31 | 40.20 |
| 70642 | Rainbow Lighting (NY) | 6 | $3,746 | 2025-11-24 16:43:24 | 2026-01-13 13:55:32 | 10 |
| 70276 | Dement Lighting | 6 | $58,302 | 2025-06-20 18:17:31 | 2025-07-31 21:00:41 | 8.20 |
| 70523 | J.F. LIGHTING & DESIGN INC. | 6 | $1,702 | 2025-07-14 19:01:53 | 2026-04-14 23:40:17 | 54.80 |
| 72544 | !! Shelly Orr Interiors | 6 | $3,859 | 2026-03-18 16:36:58 | 2026-05-11 21:56:52 | 10.80 |
| 72093 | FIRST & MAIN DESIGN MARKET | 5 | $3,054 | 2025-09-18 22:07:43 | 2026-02-06 22:44:56 | 35.30 |
| 72170 | FERGUSON | 5 | $79,680 | 2026-01-12 15:25:15 | 2026-01-13 18:54:50 | 0.30 |
| 72180 | Studio Trimble, Inc | 5 | $6,829 | 2025-07-30 16:56:05 | 2026-05-04 14:14:19 | 69.50 |
| 72450 | Tuthill Lighting Design, Inc | 5 | $891 | 2025-07-11 20:31:39 | 2025-08-23 18:18:02 | 10.70 |
| 71279 | Lightstyles by Light Bulbs Etc (Orange) : Lightstyles by Lig | 5 | $17,780 | 2025-06-19 16:50:48 | 2025-06-20 19:32:29 | 0.30 |

### Q-14b_results.md

# Q-14b Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 71234 | LUMENS LIGHT & LIVING | 6 | 0.30 | 0.50 | 1.67 | $795,170 |
| 70227 | Lighting World (Showroom) | 3,451 | 0.10 | 0.20 | 2 | $492,707 |
| 70427 | DOLAN NW/SEATLE/GLOBE | 10 | 0.30 | 1 | 3.33 | $452,670 |
| 71345 | Amc Lighting & Decor Inc. | 220 | 2.10 | 3.40 | 1.62 | $209,167 |
| 72355 | MENARDS, INC | 1,829 | 0.30 | 0.50 | 1.67 | $182,684 |
| 71428 | Home Depot - Canada | 2,522 | 0.20 | 0.30 | 1.50 | $132,523 |
| 70114 | Hermitage Lighting Gallery | 129 | 3.60 | 5.50 | 1.53 | $122,694 |
| 70802 | *HAGENS LIGHTING | 10 | 1 | 2.70 | 2.70 | $103,490 |
| 71766 | Imagine More Service Corp. | 183 | 2.60 | 3.90 | 1.50 | $96,051 |
| 70192 | Ray Electric-Sterling Hts | 465 | 1 | 1.70 | 1.70 | $88,427 |
| 72125 | Tri Supply Conroe | 295 | 1.60 | 2.40 | 1.50 | $83,510 |
| 71404 | Lamps.com | 837 | 0.50 | 1.20 | 2.40 | $81,750 |
| 71868 | Montreal Lighting & Hardware | 261 | 1.80 | 3 | 1.67 | $78,733 |
| 71715 | Gross Electric | 156 | 2.40 | 4.50 | 1.88 | $64,982 |
| 71354 | At Home, LLC. | 126 | 3.20 | 9.20 | 2.88 | $59,597 |

### Q-17_results.md

# Q-17 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 70764 | Sunbelt / Louisiana | MS | 2026-01-10 19:18:33 | 7 | $106,339 |
| 70242 | Valley Light Gallery (AZ) | AZ | 2026-01-11 15:10:14 | 3 | $91,476 |
| 72170 | FERGUSON | VA | 2026-01-13 18:54:50 | 5 | $79,680 |
| 70410 | Shades of Light | VA | 2026-01-10 23:17:09 | 3 | $75,005 |
| 70276 | Dement Lighting | TX | 2025-07-31 21:00:41 | 6 | $58,302 |
| 70137 | The Electric Connection ( TEC Electric) | AR | 2026-01-10 17:36:49 | 1 | $53,703 |
| 70598 | Lighting Incorporated | TX | 2026-01-10 22:52:54 | 3 | $49,163 |
| 70204 | Northside Lighting & Fan dba Premier Lighting | AZ | 2026-01-10 15:52:18 | 4 | $48,602 |
| 71995 | Design Superstore / Designco | TX | 2026-01-12 18:49:56 | 2 | $47,430 |
| 70899 | Royaume Luminaire | QC | 2026-01-10 19:01:46 | 1 | $41,820 |
| 70595 | Coley Electric & Plumbing (Douglas) | GA | 2026-01-11 20:35:27 | 1 | $41,528 |
| 72561 | Cambridge Interiors dba Inspired Interiors | TX | 2026-01-11 16:54:37 | 3 | $41,311 |
| 72089 | Coburn Supply Company dba Coburn's | TX | 2026-01-11 22:52:03 | 2 | $40,062 |
| 72235 | Deco Luminaire Brossard Dix 30 | QC | 2026-01-10 21:15:57 | 2 | $36,700 |
| 71996 | Vermont Lighting | VT | 2026-01-11 21:23:33 | 3 | $36,480 |
| 72565 | Aura Interiors Inc (CAN) | BC | 2026-01-10 18:34:38 | 2 | $35,765 |
| 70415 | Pine Grove Electric Supply Co | LA | 2026-01-10 21:06:00 | 2 | $34,126 |
| 70291 | Garbe's Lighting & Hardware LLC | OK | 2026-01-10 18:10:05 | 3 | $33,936 |
| 70593 | DULLES ELECTRIC AND SUPPLY | VA | 2026-01-12 19:28:37 | 2 | $32,984 |
| 72240 | !! Main Place Lighting | TX | 2026-01-10 15:49:28 | 2 | $32,554 |
| 72283 | Dhillon Lighting (Calgary - Gurpreet) | AB | 2026-01-11 18:34:03 | 2 | $32,160 |
| 71885 | Royaume Luminaire-J.D. Inc | QC | 2026-01-10 19:04:53 | 3 | $31,366 |
| 72271 | The Jarrell Company | TX | 2026-01-13 15:15:06 | 2 | $29,527 |
| 70222 | Hunzicker Lighting Gallery | OK | 2026-01-11 23:09:26 | 2 | $27,362 |
| 71089 | Winsupply Elizabethtown : Winsupply Owensboro KY | OH | 2026-01-11 16:44:21 | 1 | $25,906 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 70764 | Sunbelt / Louisiana | MS | $106,339 | 2026-01-10 19:18:33 | 158 |
| 70242 | Valley Light Gallery (AZ) | AZ | $91,476 | 2026-01-11 15:10:14 | 158 |
| 72170 | FERGUSON | VA | $79,680 | 2026-01-13 18:54:50 | 155 |
| 70410 | Shades of Light | VA | $75,005 | 2026-01-10 23:17:09 | 158 |
| 70276 | Dement Lighting | TX | $58,302 | 2025-07-31 21:00:41 | 321 |
| 70137 | The Electric Connection ( TEC Electric) | AR | $53,703 | 2026-01-10 17:36:49 | 158 |
| 70598 | Lighting Incorporated | TX | $49,163 | 2026-01-10 22:52:54 | 158 |
| 70204 | Northside Lighting & Fan dba Premier Lighting | AZ | $48,602 | 2026-01-10 15:52:18 | 159 |
| 71995 | Design Superstore / Designco | TX | $47,430 | 2026-01-12 18:49:56 | 156 |
| 70899 | Royaume Luminaire | QC | $41,820 | 2026-01-10 19:01:46 | 158 |
| 70595 | Coley Electric & Plumbing (Douglas) | GA | $41,528 | 2026-01-11 20:35:27 | 157 |
| 72561 | Cambridge Interiors dba Inspired Interiors | TX | $41,311 | 2026-01-11 16:54:37 | 157 |
| 72089 | Coburn Supply Company dba Coburn's | TX | $40,062 | 2026-01-11 22:52:03 | 157 |
| 72235 | Deco Luminaire Brossard Dix 30 | QC | $36,700 | 2026-01-10 21:15:57 | 158 |
| 71996 | Vermont Lighting | VT | $36,480 | 2026-01-11 21:23:33 | 157 |
| 72565 | Aura Interiors Inc (CAN) | BC | $35,765 | 2026-01-10 18:34:38 | 158 |
| 70415 | Pine Grove Electric Supply Co | LA | $34,126 | 2026-01-10 21:06:00 | 158 |
| 70291 | Garbe's Lighting & Hardware LLC | OK | $33,936 | 2026-01-10 18:10:05 | 158 |
| 70593 | DULLES ELECTRIC AND SUPPLY | VA | $32,984 | 2026-01-12 19:28:37 | 156 |
| 72240 | !! Main Place Lighting | TX | $32,554 | 2026-01-10 15:49:28 | 159 |

### Q-40_results.md

# Q-40 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| TX | 34 | 70 | $562,190 |
| VA | 7 | 25 | $209,029 |
| FL | 21 | 31 | $207,302 |
| QC | 12 | 15 | $182,144 |
| AZ | 7 | 28 | $169,942 |
| GA | 14 | 46 | $154,430 |
| MS | 3 | 12 | $142,820 |
| LA | 11 | 17 | $140,661 |
| CA | 24 | 40 | $97,083 |
| AL | 10 | 26 | $88,631 |
| BC | 5 | 8 | $74,952 |
| OH | 13 | 20 | $72,039 |
| OK | 3 | 6 | $71,156 |
| AR | 3 | 3 | $67,657 |
| TN | 7 | 10 | $63,518 |
| SC | 8 | 17 | $60,013 |
| MI | 8 | 11 | $59,330 |
| CT | 9 | 31 | $56,842 |
| ON | 7 | 8 | $50,307 |
| AB | 3 | 4 | $49,790 |

### Q-41_results.md

# Q-41 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 17
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-06-01 | Rep-Acquired (iPad) | 11 |
| 2025-06-01 | eCat Online-Acquired (self-serve) | 3 |
| 2025-07-01 | eCat Online-Acquired (self-serve) | 12 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 7 |
| 2025-09-01 | eCat Online-Acquired (self-serve) | 7 |
| 2025-10-01 | eCat Online-Acquired (self-serve) | 4 |
| 2025-11-01 | eCat Online-Acquired (self-serve) | 5 |
| 2025-12-01 | eCat Online-Acquired (self-serve) | 3 |
| 2026-01-01 | Rep-Acquired (iPad) | 21 |
| 2026-01-01 | eCat Online-Acquired (self-serve) | 4 |
| 2026-02-01 | eCat Online-Acquired (self-serve) | 7 |
| 2026-03-01 | Rep-Acquired (iPad) | 1 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 8 |
| 2026-04-01 | Rep-Acquired (iPad) | 1 |
| 2026-04-01 | eCat Online-Acquired (self-serve) | 7 |
| 2026-05-01 | eCat Online-Acquired (self-serve) | 2 |
| 2026-06-01 | eCat Online-Acquired (self-serve) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 22
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Dakota Duffield | 4 |
| Todd Tuchfarber | 3 |
| Jessica Romero | 3 |
| Adams Smith | 2 |
| Jerry Sharp | 2 |
| Julie Gannon | 2 |
| Keeley - Luxeco  Jackson | 2 |
| Lisa Belesky | 2 |
| Brad Dobson | 1 |
| Shelly Meshwork | 1 |
| Kathy Phelps | 1 |
| Brad Buntz | 1 |
| Kevin Blackley | 1 |
| Kevin Gannon | 1 |
| Kris Roach | 1 |
| Wayne Falk | 1 |
| Mary McKey | 1 |
| Matt Rowland | 1 |
| Chris Collier | 1 |
| Customer Support | 1 |
| Cheryl LaRosa | 1 |
| Rob Azimi | 1 |

### Q-52_results.md

# Q-52 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 71200 | WAYFAIR LLC | MA | 83,971 | $7.0M | 0 | $0 | 0 |
| 72170 | FERGUSON | VA | 6,358 | $2.7M | 5 | $79,680 | 3 |
| 70839 | BUILD.COM | CA | 12,715 | $2.5M | 0 | $0 | 0 |
| 70410 | Shades Of Light | VA | 599 | $1.7M | 3 | $75,005 | 4.30 |
| 71410 | The Home Depot | GA | 22,806 | $1.5M | 0 | $0 | 0 |
| 71199 | LAMPS PLUS INC | CA | 6,848 | $1.4M | 0 | $0 | 0 |
| 71366 | LIGHTING BY JARED | PA | 4,804 | $906,444 | 0 | $0 | 0 |
| 71273 | BELAMI | CA | 3,533 | $826,957 | 0 | $0 | 0 |
| 71234 | 71234 | CA | 4,249 | $795,255 | 0 | $0 | 0 |
| 70513 | Lifestyles Stores, Inc. - Edmo | OK | 374 | $793,951 | 0 | $0 | 0 |
| 71059 | CAPITOL LTG 1800LIGHTING.COM | FL | 4,217 | $791,453 | 0 | $0 | 0 |
| 71651 | Im Lighting Limited Liability | TX | 151 | $494,937 | 0 | $0 | 0 |
| 70227 | Lighting World (Showroom) | NY | 1,950 | $492,809 | 1 | $12,162 | 2.50 |
| 72008 | HOME GOODS | CT | 25 | $491,968 | 0 | $0 | 0 |
| 70764 | Sunbelt/ Louisiana | MS | 481 | $457,020 | 7 | $106,339 | 23.30 |
| 70427 | Dolan Nw/Seatle/Globe | OR | 616 | $452,723 | 1 | $1,926 | 0.40 |
| 70172 | Inline Electric Supply | AL | 455 | $410,380 | 2 | $20,862 | 5.10 |
| 70448 | Lighting Design Company | UT | 495 | $356,733 | 0 | $0 | 0 |
| 70853 | Sunbelt /Mississippi | MS | 417 | $356,728 | 2 | $13,257 | 3.70 |
| 72372 | LOWE'S COMPANIES INC | NC | 3,812 | $350,459 | 0 | $0 | 0 |
| 71187 | Lighting Connection Lp | TX | 101 | $333,632 | 0 | $0 | 0 |
| 71777 | Nova Lighting | UT | 165 | $331,199 | 0 | $0 | 0 |
| 70228 | Lighting World - FBA | NY | 1,178 | $315,997 | 0 | $0 | 0 |
| 70952 | Graham's Lighting Fixtures Inc | TN | 171 | $307,292 | 1 | $20,114 | 6.50 |
| 70359 | Palmer Electric Company | FL | 185 | $292,213 | 0 | $0 | 0 |
| 70590 | Gadsden Lighting Showroom Inc | AL | 106 | $277,603 | 1 | $8,826 | 3.20 |
| 70212 | Stokes Electric Company | TN | 229 | $276,772 | 0 | $0 | 0 |
| 70598 | Lighting Incorporated | TX | 404 | $259,083 | 3 | $49,163 | 19 |
| 71498 | Fort Worth Lighting | TX | 194 | $253,575 | 1 | $17,045 | 6.70 |
| 70135 | Southern Lighting Gallery Inc | GA | 206 | $251,976 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 71410 | The Home Depot | GA | 22,806 | $1.5M |
| 71199 | LAMPS PLUS INC | CA | 6,848 | $1.4M |
| 71273 | BELAMI | CA | 3,533 | $826,957 |
| 71059 | CAPITOL LTG 1800LIGHTING.COM | FL | 4,217 | $791,453 |
| 71651 | Im Lighting Limited Liability | TX | 151 | $494,937 |
| 72008 | HOME GOODS | CT | 25 | $491,968 |
| 72372 | LOWE'S COMPANIES INC | NC | 3,812 | $350,459 |
| 71187 | Lighting Connection Lp | TX | 101 | $333,632 |
| 70228 | Lighting World - FBA | NY | 1,178 | $315,997 |
| 72225 | 2641426 Ont Inc DBA Lighthouse Cabinetry | ON | 1,386 | $241,771 |
| 71587 | Lightology | IL | 770 | $205,717 |
| 72081 | Litecraft Lighting Inc | GA | 218 | $203,967 |
| 72355 | MENARDS, INC | WI | 1,144 | $182,684 |
| 72686 | Shades Of Light | VA | 11 | $173,946 |
| 71593 | Haus Appeal LLC | MA | 1,240 | $152,429 |
| 70786 | Aztec Lighting Inc. | AZ | 64 | $144,280 |
| 71428 | Home Depot - Canada | GA | 1,424 | $132,523 |
| 71855 | LIGHTOPIA  LLC | CA | 644 | $126,893 |
| 70459 | Northern Lighting, Inc. | OH | 109 | $116,971 |
| 71404 | Lamps.com | PA | 531 | $81,750 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MA | 29 | 86,146 | $7.5M | 4 | 6 | $13,160 | 0.20 |
| CA | 89 | 29,937 | $6.4M | 24 | 40 | $97,083 | 1.50 |
| VA | 18 | 7,439 | $4.7M | 7 | 25 | $209,029 | 4.50 |
| TX | 88 | 5,187 | $3.4M | 34 | 70 | $562,190 | 16.40 |
| GA | 48 | 26,804 | $3.2M | 14 | 46 | $154,430 | 4.80 |
| FL | 90 | 9,122 | $3.0M | 21 | 31 | $207,302 | 6.80 |
| PA | 31 | 6,219 | $1.4M | 6 | 6 | $19,989 | 1.50 |
| NY | 55 | 4,298 | $1.4M | 12 | 22 | $49,252 | 3.60 |
| TN | 26 | 1,148 | $1.2M | 7 | 10 | $63,518 | 5.50 |
| NC | 31 | 5,057 | $1.1M | 7 | 11 | $48,205 | 4.30 |
| MS | 9 | 1,142 | $1.1M | 3 | 12 | $142,820 | 12.90 |
| UT | 13 | 1,151 | $1.1M | 1 | 1 | $1,363 | 0.10 |
| OK | 8 | 728 | $1.1M | 3 | 6 | $71,156 | 6.70 |
| AL | 21 | 1,127 | $1.1M | 10 | 26 | $88,631 | 8.30 |
| IL | 33 | 2,397 | $899,658 | 7 | 27 | $44,490 | 4.90 |
| CT | 17 | 1,016 | $856,544 | 9 | 31 | $56,842 | 6.60 |
| ON | 54 | 2,533 | $817,801 | 7 | 8 | $50,307 | 6.20 |
| OH | 52 | 1,414 | $803,948 | 13 | 20 | $72,039 | 9 |
| OR | 11 | 1,360 | $786,808 | 3 | 4 | $4,028 | 0.50 |
| LA | 27 | 825 | $576,060 | 11 | 17 | $140,661 | 24.40 |

### Q-57_results.md

# Q-57 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TX | $1.6M | $1.4M | -13.50 | 126 | 125 | 1 | 4,127 |
| FL | $1.0M | $891,698 | -14.80 | 120 | 124 | -4 | 3,517 |
| VA | $1.0M | $775,649 | -23.70 | 46 | 42 | 4 | 1,500 |
| TN | $668,596 | $653,964 | -2.20 | 57 | 65 | -8 | 1,747 |
| GA | $694,915 | $641,850 | -7.60 | 74 | 73 | 1 | 2,453 |
| NC | $545,644 | $576,417 | 5.60 | 65 | 64 | 1 | 2,164 |
| CA | $538,694 | $553,487 | 2.70 | 85 | 96 | -11 | 3,574 |
| NY | $393,391 | $452,756 | 15.10 | 73 | 79 | -6 | 2,189 |
| AL | $320,030 | $441,662 | 38 | 50 | 48 | 2 | 930 |
| LA | $368,510 | $412,808 | 12 | 50 | 42 | 8 | 778 |
| OK | $386,924 | $391,579 | 1.20 | 27 | 31 | -4 | 561 |
| NJ | $339,606 | $372,161 | 9.60 | 60 | 61 | -1 | 2,696 |
| OH | $336,148 | $349,766 | 4.10 | 66 | 66 | 0 | 1,351 |
| IL | $383,442 | $335,304 | -12.60 | 59 | 58 | 1 | 1,883 |
| ON | $280,873 | $334,939 | 19.20 | 60 | 51 | 9 | 1,030 |
| UT | $335,455 | $332,859 | -0.80 | 35 | 36 | -1 | 665 |
| SC | $404,558 | $300,833 | -25.60 | 57 | 63 | -6 | 1,271 |
| AZ | $306,386 | $293,756 | -4.10 | 48 | 42 | 6 | 877 |
| KY | $243,964 | $267,622 | 9.70 | 41 | 43 | -2 | 762 |
| PA | $234,670 | $257,859 | 9.90 | 63 | 57 | 6 | 1,583 |
| MS | $201,688 | $243,534 | 20.70 | 30 | 27 | 3 | 419 |
| MI | $227,656 | $240,412 | 5.60 | 49 | 46 | 3 | 1,197 |
| MN | $166,697 | $225,937 | 35.50 | 35 | 37 | -2 | 873 |
| MA | $180,625 | $207,866 | 15.10 | 51 | 48 | 3 | 1,533 |
| MO | $206,300 | $192,022 | -6.90 | 37 | 41 | -4 | 759 |

### Q-68_results.md

# Q-68 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| Lighting Connection Lp | TX | $369,850 | $822,450 | $452,599 | 45 | 13 |
| Foresight Lighting | UT | $58,743 | $250,151 | $191,408 | 23.50 | 5 |
| Lighting Specialists | Unknown | $44,440 | $122,269 | $77,829 | 36.30 | 6 |
| Qed Inc. DBA Galleria Lighting | MN | $43,170 | $95,985 | $52,814 | 45 | 13 |
| Designer's Mart | TX | $57,159 | $105,546 | $48,387 | 54.20 | 13 |
| Rdhs Inc DBA Randolph Door & Lighting | TX | $16,037 | $55,662 | $39,624 | 28.80 | 11 |
| Garbe Industries Inc. | OK | $61,793 | $101,094 | $39,301 | 61.10 | 13 |
| Euroluce DBA Home Lighting | ON | $31,702 | $70,264 | $38,562 | 45.10 | 13 |
| Lando Lighting | ON | $35,565 | $68,313 | $32,748 | 52.10 | 5 |
| Austell Lighting | TN | $8,236 | $39,265 | $31,029 | 21 | 6 |
| Lbx Lighting | TX | $30,593 | $61,184 | $30,590 | 50 | 9 |
| Pine Lighting | BC | $54,631 | $84,582 | $29,951 | 64.60 | 13 |
| At Home, LLC. | CO | $72,617 | $102,365 | $29,748 | 70.90 | 12 |
| The Finishing Touch | OK | $36,473 | $65,473 | $29,000 | 55.70 | 13 |
| Elliott Electric Supply Inc. | TX | $5,572 | $34,249 | $28,677 | 16.30 | 9 |
| Quintessential Lighting | AR | $37,637 | $65,008 | $27,372 | 57.90 | 13 |
| Valencia Lighting | CA | $11,606 | $36,239 | $24,633 | 32 | 12 |
| Christie's Lighting Gallery | SC | $21,122 | $45,706 | $24,584 | 46.20 | 13 |
| Gorman Brothers Appliance & Lighting | LA | $20,923 | $44,758 | $23,835 | 46.70 | 12 |
| Magnolia Electric Supply Co, Inc | MS | $24,695 | $45,798 | $21,103 | 53.90 | 5 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| customer_num | customer_name | state | ltm_orders | ltm_gmv | last_order | days_since_last | avg_days_between | decay_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 70276 | Dement Lighting | TX | 6 | $58,302 | 2025-07-31 21:00:41 | 321 | 41 | 7.80 |

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 71200 | WAYFAIR LLC | 1-3060-6-60 | *LQ* Claiborne 6 LT Chandelier in Avalite (LP) | 59 | 6.80 | 134 | 19.70 | 17,821.02 | DECAY_DETECTED |
| 70952 | Graham's Lighting Fixtures Inc | 6-2000-7-WH | LED Disc Light in White | 35 | 13.30 | 57 | 4.30 | 69,460.75 | DECAY_DETECTED |
| 71345 | Amc Lighting & Decor Inc. | 6-3333-12-WH | 12" ROUND LED FLUSH | 46 | 9.80 | 93 | 9.50 | 28,744.50 | DECAY_DETECTED |
| 70227 | Lighting World (Showroom) | 1-1738-5-320 | Ashe 5 LT Oval Chandelier in Warm Brass and Rope | 28 | 8.10 | 255 | 31.50 | 7,431.80 | DECAY_DETECTED |
| 71651 | Im Lighting Limited Liability | 5-258-13 | Monte Grande 1 LT Outdoor Wall Lantern in English Bronze | 30 | 13.30 | 135 | 10.20 | 20,795.52 | DECAY_DETECTED |
| 72170 | FERGUSON | M2018BNRV | 52" 2 LT Ceiling Fan in Brushed Nickel *USE 52-ECM-5RV-SN FIRST | 15 | 13.90 | 51 | 3.70 | 53,190 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | M10078MBK | 4 LT Linear Chandelier in Matte Black *M20 | 369 | 1.50 | 7 | 4.70 | 38,834.39 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 8-2988-3-322 | Blair 3 LT Bathroom Vanity Light in Warm Brass | 322 | 1.70 | 9 | 5.30 | 32,130.34 | DECAY_DETECTED |
| 71273 | BELAMI | 39-FD-125-54 | Stockholm 6 LT Fan D'Lier in  Gold Patina | 97 | 5 | 56 | 11.20 | 15,184 | DECAY_DETECTED |
| 72170 | FERGUSON | 5-3045-72 | Exterior Collections 1 LT Outdoor Wall Lantern in Rustic Bronze | 43 | 10.20 | 51 | 5 | 31,402.80 | DECAY_DETECTED |
| 71345 | Amc Lighting & Decor Inc. | 6-2000-7-WH | LED Disc Light in White | 64 | 8.10 | 23 | 2.80 | 55,094.04 | SLOWING |
| 71187 | Lighting Connection Lp | 8-4030-4-322 | Octave 4 LT Bathroom Vanity Light in Warm Brass | 34 | 13.40 | 70 | 5.20 | 29,205.86 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 35-328-FD-13 | *LQ* Brisa 8 LT Fan D'Lier in English Bronze (LP) | 47 | 8.40 | 112 | 13.30 | 11,195.96 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | M90088MBKNB | 2 LT Wall Sconce in Matte Black with Natural Brass *M23 | 120 | 3.90 | 70 | 17.90 | 7,675.41 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 6-4035-3-BK | Octave 3 LT Ceiling Light in Black | 211 | 2.50 | 26 | 10.40 | 11,582.42 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 1-990-8-41 | Burgess 8 LT Linear Chandelier in Durango | 121 | 4.10 | 31 | 7.60 | 14,038.70 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 1-3961-6-322 | Ashbury 6 LT Chandelier in Warm Brass | 25 | 5.10 | 86 | 16.90 | 6,081.64 | DECAY_DETECTED |
| 71345 | Amc Lighting & Decor Inc. | M80044NB | 3 LT Bathroom Vanity Light in Natural Brass | 22 | 12.70 | 136 | 10.70 | 9,364.42 | DECAY_DETECTED |
| 71651 | Im Lighting Limited Liability | 5-3045-72 | Exterior Collections 1 LT Outdoor Wall Lantern in Rustic Bronze | 42 | 12 | 44 | 3.70 | 25,982.58 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 3-7701-5-89 | Benson 5 LT Pendant in Matte Black | 185 | 2.90 | 14 | 4.80 | 17,504.84 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 9-1826-1-320 | Ashe 1 LT Wall Sconce in Warm Brass and Rope | 99 | 4.90 | 44 | 9 | 8,836.65 | DECAY_DETECTED |
| 70410 | Shades Of Light | 9-996-1-109 | Willmar 1 LT Wall Sconce in Polished Nickel | 20 | 20.10 | 90 | 4.50 | 17,710 | DECAY_DETECTED |
| 70839 | BUILD.COM | 1-3720-6-89 | Boca 6 LT Chandelier in Matte Black | 30 | 13.20 | 148 | 11.20 | 6,954.78 | DECAY_DETECTED |
| 71651 | Im Lighting Limited Liability | M50053RB | 1 LT Outdoor Wall Lantern in Rustic Bronze | 43 | 11.40 | 44 | 3.90 | 19,733.79 | DECAY_DETECTED |
| 70359 | Palmer Electric Company | 7-9006-3-89 | Akron 3 LT Pendant in Matte Black | 39 | 12.40 | 49 | 4 | 17,999.30 | DECAY_DETECTED |
| 71651 | Im Lighting Limited Liability | 6-780-13-BK | 2 LT Ceiling Light in Matte Black | 37 | 13.30 | 37 | 2.80 | 25,386.60 | SLOWING |
| 71200 | WAYFAIR LLC | M100122NB | 2 LT Linear Chandelier in Natural Brass | 144 | 3.60 | 29 | 8.10 | 8,692.12 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | M7029NB | 4 LT Pendant in Natural Brass | 130 | 4.10 | 17 | 4.10 | 16,670.26 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 9-2542-1-109 | Cameron 1 LT Wall Sconce in Polished Nickel | 241 | 2.20 | 14 | 6.40 | 10,842.31 | DECAY_DETECTED |
| 71200 | WAYFAIR LLC | 7-1040-3-BK | Penrose 3 LT Pendant in Black | 237 | 2.20 | 9 | 4.10 | 16,551.71 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 70410 | Shades Of Light | VA | 1,725,093.39 | 2,915,999.22 | -40.80 | 75,005 | 31,766 | 136.10 | CONTRACTING |
| 71187 | Lighting Connection Lp | TX | 333,631.59 | 926,396.67 | -64 | 0 | 0 | — | CONTRACTING |
| 72170 | FERGUSON | VA | 2,691,390.24 | 2,428,548.17 | 10.80 | 79,680.50 | 94,089 | -15.30 | COMPETITIVE_DISPLACEMENT |
| 72149 | Foresight Lighting | UT | 45,070.74 | 251,892.20 | -82.10 | 0 | 0 | — | CONTRACTING |
| 70513 | Lifestyles Stores, Inc. - Edmo | OK | 793,951.31 | 640,562.57 | 23.90 | 0 | 19,452 | -100 | COMPETITIVE_DISPLACEMENT |
| 71850 | HOUZZ SHOP LLC | CA | 29,517.62 | 148,919.68 | -80.20 | 0 | 0 | — | CONTRACTING |
| 70853 | Sunbelt /Mississippi | MS | 356,379.46 | 257,029.65 | 38.70 | 13,257 | 80,056 | -83.40 | COMPETITIVE_DISPLACEMENT |
| 72397 | Plumbing Distributors Inc dba PDI | GA | 86,932.42 | 156,425.05 | -44.40 | 23,338 | 19,069 | 22.40 | CONTRACTING |
| 71780 | Lighting Specialists | UT | 35,521.29 | 103,350.44 | -65.60 | 0 | 0 | — | CONTRACTING |
| 70114 | Hermitage Lighting Gallery | TN | 122,693.92 | 186,117.05 | -34.10 | 6,872 | 668.80 | 927.50 | CONTRACTING |
| 70659 | Designer's Mart | TX | 42,739.20 | 104,944.80 | -59.30 | 18,218.50 | 13,515 | 34.80 | CONTRACTING |
| 71404 | Lamps.com | PA | 81,750.43 | 142,378.39 | -42.60 | 0 | 0 | — | CONTRACTING |
| 70973 | Graham's Lighting Inc | TN | 120,291.57 | 178,952.50 | -32.80 | 0 | 0 | — | CONTRACTING |
| 71447 | The Brecher Co., Inc | KY | 161,902.28 | 220,185.02 | -26.50 | 7,658 | 12,724 | -39.80 | CONTRACTING |
| 70122 | Qed Inc. DBA Galleria Lighting | CO | 39,021.16 | 96,952.96 | -59.80 | 0 | 0 | — | CONTRACTING |
| 70745 | Connecticut Lighting Center | CT | 247,930.50 | 190,201.70 | 30.40 | 21,135.10 | 34,609 | -38.90 | COMPETITIVE_DISPLACEMENT |
| 70786 | Aztec Lighting Inc. | AZ | 144,217.22 | 199,140.98 | -27.60 | 0 | 0 | — | CONTRACTING |
| 70063 | Lights Unlimited | NC | 137,531.80 | 181,511.16 | -24.20 | 7,289 | 0 | — | CONTRACTING |
| 71868 | Montreal Lighting & Hardware | QC | 78,733.26 | 119,432.98 | -34.10 | 0 | 0 | — | CONTRACTING |
| 70642 | Rainbow Lighting | NY | 55,674 | 96,332.90 | -42.20 | 3,746.50 | 5,590.20 | -33 | CONTRACTING |
| 70531 | Southern Lighting Gallery, LLC dba Charleston Lighting | SC | 129,787.47 | 167,450.50 | -22.50 | 0 | 0 | — | CONTRACTING |
| 70949 | Kendall Electric | MI | 71,526.50 | 108,908.08 | -34.30 | 21,456 | 13,293 | 61.40 | CONTRACTING |
| 71428 | Home Depot - Canada | GA | 132,523.09 | 168,119.48 | -21.20 | 0 | 0 | — | CONTRACTING |
| 70291 | Garbe Industries Inc. | OK | 51,946.31 | 87,028.10 | -40.30 | 33,936 | 17,947 | 89.10 | CONTRACTING |
| 70154 | Elements | NY | 94,630.57 | 60,195.92 | 57.20 | 6,088 | 6,873 | -11.40 | COMPETITIVE_DISPLACEMENT |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 70410 | Shades Of Light | 2 | 867,672.44 | 119.10 | [{'quarter': '2025-07-01', 'revenue': 187359.18, 'qoq_pct': -84.7}, {'quarter': '2025-10-01', 'revenue': 410558.55, 'qoq_pct': 119.1}, {'quarter': '2026-01-01', 'revenue': 867672.44, 'qoq_pct': 111.3}, {'quarter': '2026-04-01', 'revenue': 231209.65, 'qoq_pct': -73.4}] |
| 71273 | BELAMI | 2 | 271,678.33 | 48.30 | [{'quarter': '2025-07-01', 'revenue': 271678.33, 'qoq_pct': 48.3}, {'quarter': '2025-10-01', 'revenue': 169654.44, 'qoq_pct': -37.6}, {'quarter': '2026-01-01', 'revenue': 155456.43, 'qoq_pct': -8.4}, {'quarter': '2026-04-01', 'revenue': 204702.56, 'qoq_pct': 31.7}] |
| 70952 | Graham's Lighting Fixtures Inc | 2 | 102,951.26 | 39.60 | [{'quarter': '2025-07-01', 'revenue': 53272.84, 'qoq_pct': -27.2}, {'quarter': '2025-10-01', 'revenue': 71916.97, 'qoq_pct': 35.0}, {'quarter': '2026-01-01', 'revenue': 73752.71, 'qoq_pct': 2.6}, {'quarter': '2026-04-01', 'revenue': 102951.26, 'qoq_pct': 39.6}] |
| 70344 | Magnolia Lighting, Inc | 2 | 73,911.23 | 87.50 | [{'quarter': '2025-07-01', 'revenue': 43190.63, 'qoq_pct': -38.0}, {'quarter': '2025-10-01', 'revenue': 65379.6, 'qoq_pct': 51.4}, {'quarter': '2026-01-01', 'revenue': 39417.0, 'qoq_pct': -39.7}, {'quarter': '2026-04-01', 'revenue': 73911.23, 'qoq_pct': 87.5}] |
| 70865 | St Louis Metro Electric | 2 | 69,827.16 | 175 | [{'quarter': '2025-07-01', 'revenue': 37927.54, 'qoq_pct': 32.6}, {'quarter': '2025-10-01', 'revenue': 25394.16, 'qoq_pct': -33.0}, {'quarter': '2026-01-01', 'revenue': 69827.16, 'qoq_pct': 175.0}, {'quarter': '2026-04-01', 'revenue': 42889.44, 'qoq_pct': -38.6}] |
| 70629 | CAPITOL LIGHTING (BOCA RATON) | 2 | 59,193 | 74.10 | [{'quarter': '2025-07-01', 'revenue': 28891.75, 'qoq_pct': -31.8}, {'quarter': '2025-10-01', 'revenue': 24488.81, 'qoq_pct': -15.2}, {'quarter': '2026-01-01', 'revenue': 34007.27, 'qoq_pct': 38.9}, {'quarter': '2026-04-01', 'revenue': 59193.0, 'qoq_pct': 74.1}] |
| 70222 | Hunzicker Lighting Gallery | 2 | 57,381.46 | 105 | [{'quarter': '2025-07-01', 'revenue': 45461.93, 'qoq_pct': 105.0}, {'quarter': '2025-10-01', 'revenue': 33165.86, 'qoq_pct': -27.0}, {'quarter': '2026-01-01', 'revenue': 57381.46, 'qoq_pct': 73.0}, {'quarter': '2026-04-01', 'revenue': 27584.26, 'qoq_pct': -51.9}] |
| 70114 | Hermitage Lighting Gallery | 2 | 55,976.73 | 102 | [{'quarter': '2025-07-01', 'revenue': 55976.73, 'qoq_pct': 102.0}, {'quarter': '2025-10-01', 'revenue': 21879.4, 'qoq_pct': -60.9}, {'quarter': '2026-01-01', 'revenue': 32005.25, 'qoq_pct': 46.3}, {'quarter': '2026-04-01', 'revenue': 12430.24, 'qoq_pct': -61.2}] |
| 71766 | Imagine More Service Corp. | 2 | 52,406.29 | 101.50 | [{'quarter': '2025-07-01', 'revenue': 52406.29, 'qoq_pct': 101.5}, {'quarter': '2025-10-01', 'revenue': 13780.17, 'qoq_pct': -73.7}, {'quarter': '2026-01-01', 'revenue': 18806.79, 'qoq_pct': 36.5}, {'quarter': '2026-04-01', 'revenue': 6524.58, 'qoq_pct': -65.3}] |
| 71448 | Light | 2 | 48,929 | 1,407 | [{'quarter': '2025-07-01', 'revenue': 981.08, 'qoq_pct': -73.2}, {'quarter': '2025-10-01', 'revenue': 2798.8, 'qoq_pct': 185.3}, {'quarter': '2026-01-01', 'revenue': 3246.78, 'qoq_pct': 16.0}, {'quarter': '2026-04-01', 'revenue': 48929.0, 'qoq_pct': 1407.0}] |
| 70633 | Bbc Lighting & Supply | 2 | 43,527.63 | 103.40 | [{'quarter': '2025-07-01', 'revenue': 43527.63, 'qoq_pct': 103.4}, {'quarter': '2025-10-01', 'revenue': 28948.0, 'qoq_pct': -33.5}, {'quarter': '2026-01-01', 'revenue': 38219.24, 'qoq_pct': 32.0}, {'quarter': '2026-04-01', 'revenue': 29245.24, 'qoq_pct': -23.5}] |
| 71158 | Capital Electric | 2 | 43,170.75 | 377.90 | [{'quarter': '2025-07-01', 'revenue': 43170.75, 'qoq_pct': 377.9}, {'quarter': '2025-10-01', 'revenue': 8194.0, 'qoq_pct': -81.0}, {'quarter': '2026-01-01', 'revenue': 15337.5, 'qoq_pct': 87.2}, {'quarter': '2026-04-01', 'revenue': 12918.0, 'qoq_pct': -15.8}] |
| 70350 | Gallery Of Lighting (Holder) | 2 | 38,315.22 | 116.70 | [{'quarter': '2025-07-01', 'revenue': 12404.06, 'qoq_pct': -3.3}, {'quarter': '2025-10-01', 'revenue': 17677.8, 'qoq_pct': 42.5}, {'quarter': '2026-01-01', 'revenue': 38315.22, 'qoq_pct': 116.7}, {'quarter': '2026-04-01', 'revenue': 14748.92, 'qoq_pct': -61.5}] |
| 70276 | Dement Lighting | 2 | 36,187.80 | 114.20 | [{'quarter': '2025-07-01', 'revenue': 36187.8, 'qoq_pct': 40.4}, {'quarter': '2025-10-01', 'revenue': 16709.2, 'qoq_pct': -53.8}, {'quarter': '2026-01-01', 'revenue': 35786.01, 'qoq_pct': 114.2}, {'quarter': '2026-04-01', 'revenue': 11696.69, 'qoq_pct': -67.3}] |
| 70154 | Elements | 2 | 29,405.45 | 62.70 | [{'quarter': '2025-07-01', 'revenue': 20885.35, 'qoq_pct': 62.7}, {'quarter': '2025-10-01', 'revenue': 29405.45, 'qoq_pct': 40.8}, {'quarter': '2026-01-01', 'revenue': 20134.19, 'qoq_pct': -31.5}, {'quarter': '2026-04-01', 'revenue': 23775.25, 'qoq_pct': 18.1}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 9-302-1-322 | Monroe 1-Light Wall Sconce in Warm Brass | MONRO | 507,979.29 | 12,007 | — | 2026-07-03 | [{'customer': 'WAYFAIR LLC', 'revenue': 247432.54}, {'customer': 'FERGUSON', 'revenue': 32228.05}, {'customer': 'BUILD.COM', 'revenue': 28473.72}, {'customer': 'LAMPS PLUS INC', 'revenue': 15649.13}, {'customer': 'Inline Electric Supply', 'revenue': 9731.0}, {'customer': 'The Home Depot', 'revenue': 9438.54}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 7998.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 7932.75}, {'customer': 'Lighting World', 'revenue': 5065.81}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 4941.87}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 4602.0}, {'customer': 'LIGHTING BY JARED', 'revenue': 3360.62}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 3323.84}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 3145.57}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 3114.5}, {'customer': 'Sunbelt / Louisiana', 'revenue': 3040.6}, {'customer': 'Lighting Design Company', 'revenue': 2996.0}, {'customer': 'Lifestyles Store Inc', 'revenue': 2966.59}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 2817.0}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 2709.7}, {'customer': "Richard's Lighting", 'revenue': 2252.7}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2109.0}, {'customer': 'Masterpiece Lighting (GA)', 'revenue': 2009.0}, {'customer': 'BELAMI ECommerce', 'revenue': 1955.93}, {'customer': 'Light N Leisure Inc', 'revenue': 1932.0}, {'customer': "Seth's Lighting & Assoc. Inc", 'revenue': 1758.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 1731.96}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 1695.0}, {'customer': "Joseph's Electrical Center", 'revenue': 1690.64}, {'customer': 'M & M Lighting, L.P.', 'revenue': 1642.0}, {'customer': "LOWE'S", 'revenue': 1536.7}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 1528.0}, {'customer': 'Butler Lighting of High Point', 'revenue': 1503.14}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 1500.0}, {'customer': 'The Brecher Co, Inc', 'revenue': 1454.69}, {'customer': 'Lightology', 'revenue': 1404.16}, {'customer': '!! Maison Olive Inc.', 'revenue': 1350.94}, {'customer': 'The Electrical & Plumbing Store', 'revenue': 1320.0}, {'customer': 'Cregger Co LLC', 'revenue': 1313.64}, {'customer': 'HOUZZ SHOP', 'revenue': 1261.52}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 1260.0}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 1230.0}, {'customer': 'Northside Lighting & Fan dba Premier Lighting', 'revenue': 1224.23}, {'customer': 'Pace Lighting Inc', 'revenue': 1147.95}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 1120.44}, {'customer': 'Lights Unlimited', 'revenue': 1115.24}, {'customer': 'Elektra Lights & Fans Inc', 'revenue': 1080.0}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 1074.78}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 1063.77}, {'customer': 'Stokes Electric Company', 'revenue': 1020.0}, {'customer': 'Lighting Emporium Inc', 'revenue': 994.5}, {'customer': 'Rensen House of Lights', 'revenue': 955.63}, {'customer': "Hinkley's Lighting Factory", 'revenue': 934.3}, {'customer': 'Greer Lighting Center LLC', 'revenue': 906.7}, {'customer': 'Cleveland Lighting Center', 'revenue': 900.0}, {'customer': 'The Light House Gallery (MO)', 'revenue': 886.7}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 870.0}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 860.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 840.0}, {'customer': 'Universal Lighting Corp (Ont)', 'revenue': 836.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 830.0}, {'customer': 'Denney Electric Supply (Ambler, PA)', 'revenue': 825.0}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 824.85}, {'customer': 'Wilson Lighting', 'revenue': 817.0}, {'customer': 'K B L Design Center', 'revenue': 809.8}, {'customer': 'Bayside Electric Supply Co', 'revenue': 789.0}, {'customer': 'Lamps.com, Inc', 'revenue': 777.24}, {'customer': 'Capitol Lighting Gallery', 'revenue': 767.2}, {'customer': 'Hagens Lighting', 'revenue': 765.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 720.0}, {'customer': 'Deco Luminaire Quebec', 'revenue': 709.5}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 690.0}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 684.0}, {'customer': 'Union Lighting (Montreal)', 'revenue': 663.3}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': 661.1}, {'customer': 'Wiseway Supply', 'revenue': 652.0}, {'customer': 'Mathes of Alabama Elec. Supply', 'revenue': 652.0}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 648.1}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 644.52}, {'customer': '!! Applico, LLC', 'revenue': 644.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (PARAMUS)', 'revenue': 641.25}, {'customer': "Victor's Lighting", 'revenue': 623.92}, {'customer': 'Fort Worth Lighting', 'revenue': 596.0}, {'customer': 'Dement Lighting', 'revenue': 592.35}, {'customer': 'Design Superstore / Designco', 'revenue': 585.0}, {'customer': 'St Louis Metro Electric', 'revenue': 577.63}, {'customer': 'Parrish Family Enterprises dba American Lighting and Design', 'revenue': 574.38}, {'customer': 'Net Retailers, LLC', 'revenue': 562.77}, {'customer': 'LIGHTING CONCEPTS, LLC (GA)', 'revenue': 540.0}, {'customer': 'ULTRA DESIGN CENTER, LLC', 'revenue': 530.25}, {'customer': 'Bee Ridge Lighting & Design', 'revenue': 522.09}, {'customer': 'Asburys Design', 'revenue': 518.14}, {'customer': 'Gorman Brothers Appliance', 'revenue': 510.0}, {'customer': 'Lighting by Design (Exton, PA)', 'revenue': 509.0}, {'customer': 'OSMOND DESIGNS INC.', 'revenue': 507.29}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB)', 'revenue': 503.8}, {'customer': 'King Electric Company Inc', 'revenue': 499.86}, {'customer': 'Distinctive Lighting Concepts', 'revenue': 495.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 495.0}, {'customer': 'Union Lighting & Furnishings (Toronto)', 'revenue': 495.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 450.0}, {'customer': 'Elan Studio Lighting', 'revenue': 450.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 450.0}, {'customer': 'Southern Electric & Plumbing Supply', 'revenue': 441.71}, {'customer': 'Wilson Lighting of Naples Inc', 'revenue': 432.0}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 427.5}, {'customer': 'Idlewood Electric Supply', 'revenue': 427.2}, {'customer': 'VP Supply', 'revenue': 426.0}, {'customer': "Armstrong's Supply Co Inc", 'revenue': 412.0}, {'customer': 'Anzalone Electric', 'revenue': 405.0}, {'customer': 'F.W. Webb Company', 'revenue': 401.49}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 396.0}, {'customer': 'Multi-Luminaire (Granby)', 'revenue': 396.0}, {'customer': 'Lighting Connection LLC (TX) : Lighting Connection DFW', 'revenue': 387.25}, {'customer': 'Lighting Etc dba Lighting Unlimited (FL)', 'revenue': 385.76}, {'customer': 'Echelon Interiors', 'revenue': 384.7}, {'customer': "Scottie's Interiors", 'revenue': 382.82}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 378.75}, {'customer': 'ABC Lighting', 'revenue': 375.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 363.0}, {'customer': 'Living Lighting # 28 (Ottawa)', 'revenue': 363.0}, {'customer': 'Coley Electric & Plumbing Supply (Jesup)', 'revenue': 360.0}, {'customer': 'Sweet Home Design Company', 'revenue': 360.0}, {'customer': 'Schaedler Yesco Dist', 'revenue': 360.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 360.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 360.0}, {'customer': 'Coley Electric & Plumbing (Douglas)', 'revenue': 360.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 360.0}, {'customer': 'Colonial Electric Supply Co', 'revenue': 360.0}, {'customer': 'Lumen Nation LLC', 'revenue': 355.0}, {'customer': 'Flinz Holdings LLC', 'revenue': 355.0}, {'customer': 'Elements', 'revenue': 354.57}, {'customer': "Wilkinson's House of Lighting", 'revenue': 342.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 322.0}, {'customer': 'Gross Lighting & Home : Indiana Lighting Center', 'revenue': 322.0}, {'customer': 'Homestyles', 'revenue': 322.0}, {'customer': 'Denali Lighting LLC', 'revenue': 300.0}, {'customer': 'Lights of Oconee', 'revenue': 300.0}, {'customer': "Coburn Supply Company dba Coburn's : Spring Hill Lighting db", 'revenue': 300.0}, {'customer': 'Elaine Everetts Lighting', 'revenue': 300.0}, {'customer': 'Milliken Investments dba Shallotte Electric Stores', 'revenue': 300.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 300.0}, {'customer': 'Austell Lighting', 'revenue': 300.0}, {'customer': 'Multi-Luminaire (Pointe Claire)', 'revenue': 297.0}, {'customer': 'Royaume Luminaire', 'revenue': 297.0}, {'customer': 'Concept Luminaire M.B. Inc', 'revenue': 297.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 294.0}, {'customer': '!! Starlight Lighting', 'revenue': 291.89}, {'customer': 'Uncommon Living fka Lighting Unlimited (MS)', 'revenue': 286.46}, {'customer': 'Cape Electrical Supply', 'revenue': 283.48}, {'customer': 'House of Carpets', 'revenue': 272.35}, {'customer': 'Mainland Lighting Warehouse', 'revenue': 272.05}, {'customer': 'Locke Supply', 'revenue': 270.0}, {'customer': 'Southern Lights', 'revenue': 270.0}, {'customer': 'Wage Lighting & Design', 'revenue': 270.0}, {'customer': 'Wiseway Supply : Wiseway Supply Loveland', 'revenue': 270.0}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 270.0}, {'customer': 'Light and Day', 'revenue': 270.0}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 267.75}, {'customer': 'Chateau Lighting', 'revenue': 263.23}, {'customer': 'Beautiful Things, Inc', 'revenue': 255.6}, {'customer': 'First Coast Lighting & Fans', 'revenue': 254.2}, {'customer': 'Deco Luminaire Terrebonne', 'revenue': 247.5}, {'customer': 'Richardson Lighting', 'revenue': 247.5}, {'customer': 'Coco & Dash', 'revenue': 241.54}, {'customer': 'DISCOUNT PLUMBING & ELECTRIC', 'revenue': 240.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 237.6}, {'customer': '!! Bluetree Corporation', 'revenue': 227.09}, {'customer': 'Northwest Electrical Supply', 'revenue': 225.0}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 222.75}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (BOCA RATON)', 'revenue': 219.0}, {'customer': 'Southern Pipe & Supply (LA)', 'revenue': 217.0}, {'customer': 'Statewide Lighting (NV)', 'revenue': 213.0}, {'customer': 'Bright Ideas Lighting & More (Bridgeport)', 'revenue': 211.4}, {'customer': 'Brite Electric Supply Inc', 'revenue': 205.66}, {'customer': 'Hardwood Floors & More', 'revenue': 202.82}, {'customer': 'City Lightz London', 'revenue': 198.0}, {'customer': 'Paradise Lighting', 'revenue': 198.0}, {'customer': 'Signature Lighting & Fans dba Whitfield Lighting and Furnitu', 'revenue': 198.0}, {'customer': 'McLaren Electric', 'revenue': 198.0}, {'customer': 'John Ward Ace Hardware', 'revenue': 192.58}, {'customer': 'Illuminating Expressions (Evansville)', 'revenue': 191.71}, {'customer': 'Cajun Electric & Lighting', 'revenue': 191.41}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 189.57}, {'customer': 'Lighting Connection LLC (TX) : Lighting Connection (Dropship', 'revenue': 186.62}, {'customer': 'James Ashjian Lighting', 'revenue': 180.0}, {'customer': 'Palmer Electric Co dba Showcase Lighting (FL)', 'revenue': 180.0}, {'customer': 'Gem Electric Supply', 'revenue': 180.0}, {'customer': 'LDB Holdings LLC dba CW Floors and Lighting', 'revenue': 180.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 180.0}, {'customer': "Designer's Mart", 'revenue': 180.0}, {'customer': 'United Electric Supply (NE)', 'revenue': 180.0}, {'customer': 'Bright Ideas (Rochester)', 'revenue': 180.0}, {'customer': 'Mancini Fine Lighting, Inc dba Fine Lighting and Lighting De', 'revenue': 180.0}, {'customer': 'B.E.S. Lighting Center', 'revenue': 180.0}, {'customer': 'Decorative Lighting, Inc', 'revenue': 180.0}, {'customer': 'House of Lights of Sanford Inc', 'revenue': 180.0}, {'customer': 'Ray Mart Inc dba Tri-Supply', 'revenue': 180.0}, {'customer': 'Your Lighting Source, LLC', 'revenue': 180.0}, {'customer': 'American Lighting Inc', 'revenue': 180.0}, {'customer': 'GW Keeter Lighting', 'revenue': 180.0}, {'customer': 'Hubbard Supplyhouse', 'revenue': 180.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba E.D Supply Co', 'revenue': 180.0}, {'customer': 'Prima Lighting Inc', 'revenue': 178.2}, {'customer': 'Pine Lighting', 'revenue': 174.8}, {'customer': 'Multi-Luminaire Gatineau', 'revenue': 165.0}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 165.0}, {'customer': 'Muskoka Lighting & Electric', 'revenue': 165.0}, {'customer': 'J.D. Lighting', 'revenue': 165.0}, {'customer': 'Scout & Nimble', 'revenue': 164.12}, {'customer': 'Chester Lighting : Doylestown Electric', 'revenue': 161.21}, {'customer': 'SBS Electric & Lighting', 'revenue': 160.89}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 158.4}, {'customer': 'Lighting Instyle', 'revenue': 154.08}, {'customer': 'Wolberg Electrical Supply Co', 'revenue': 150.0}, {'customer': 'Premier Bath, Lighting (MI)', 'revenue': 150.0}, {'customer': 'Kendall Electric Inc', 'revenue': 150.0}, {'customer': 'Dickman Supply', 'revenue': 150.0}, {'customer': 'Hall Electric Co Inc', 'revenue': 150.0}, {'customer': '!! Duncan Corporation dba Better Living', 'revenue': 150.0}, {'customer': 'Flambeaux Gas & Electric Lights', 'revenue': 150.0}, {'customer': 'Gadsden Lighting Showroom Inc', 'revenue': 150.0}, {'customer': 'The Jarrell Company', 'revenue': 150.0}, {'customer': 'White Star Supply LLC', 'revenue': 150.0}, {'customer': 'Fixture This', 'revenue': 150.0}, {'customer': 'Coast Lighting', 'revenue': 150.0}, {'customer': "Garbe's Lighting & Hardware LLC", 'revenue': 150.0}, {'customer': 'Team Electric Supply, LLC', 'revenue': 150.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 150.0}, {'customer': 'Fusion Light and Design', 'revenue': 150.0}, {'customer': 'Lighting EFX', 'revenue': 143.74}, {'customer': 'Menards, Inc', 'revenue': 142.5}, {'customer': 'Chester Lighting', 'revenue': 142.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 131.48}, {'customer': 'Lamp Warehouse dba Lighting Expo', 'revenue': 116.2}, {'customer': 'Lonestar Lighting & Technology', 'revenue': 105.66}, {'customer': 'Vermont Lighting', 'revenue': 90.7}, {'customer': 'DuPage Lighting', 'revenue': 90.0}, {'customer': 'Konstantin Gut dba Elegant Lighting (MA)', 'revenue': 90.0}, {'customer': 'The Focal Point SWLA LLC', 'revenue': 75.0}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 71.0}, {'customer': 'Fashion Light Center', 'revenue': 71.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 63.8}, {'customer': 'Hortons of LaGrange', 'revenue': 55.92}, {'customer': "Isabelle's Lighting", 'revenue': 41.65}, {'customer': 'The Lighting Corner', 'revenue': 9.9}, {'customer': 'Candlelight Light & Log', 'revenue': 0.0}, {'customer': 'J & B Supply Inc / JBS', 'revenue': 0.0}, {'customer': '!! Pelleco Home Design', 'revenue': 0.0}, {'customer': 'Littman Bros Energy Supplies', 'revenue': -58.09}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': -90.48}, {'customer': 'Muska Lighting', 'revenue': -91.4}, {'customer': 'Lighting Incorporated', 'revenue': -199.4}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': -671.13}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': -1072.9}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': -4460.5}] | [{'item': '9-302-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 144}, {'item': '9-303-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 139}, {'item': '9-7144-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 119}, {'item': '9-303-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 92}, {'item': '9-7144-1-44', 'desc': 'Monroe 1-Light Wall Sconce in Classic Bronze', 'available': 64}, {'item': '9-7144-1-109', 'desc': 'Monroe 1-Light Wall Sconce in Polished Nickel', 'available': 61}] |
| 1-2221-6-322 | Salerno 6-Light Chandelier in Warm Brass | SALER | 303,275.41 | 1,667 | — | 2026-06-27 | [{'customer': 'WAYFAIR LLC', 'revenue': 89502.86}, {'customer': 'Shades of Light', 'revenue': 48033.19}, {'customer': 'FERGUSON', 'revenue': 23608.18}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 11128.5}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 7085.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 6939.75}, {'customer': 'BUILD.COM', 'revenue': 6329.68}, {'customer': 'BELAMI ECommerce', 'revenue': 5561.89}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 5176.46}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 4657.77}, {'customer': 'LAMPS PLUS INC', 'revenue': 4652.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 3645.68}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 3514.9}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 3491.5}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 3142.88}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 3133.25}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 2750.0}, {'customer': 'Lighting World', 'revenue': 2716.74}, {'customer': 'The Home Depot', 'revenue': 2688.23}, {'customer': 'Inline Electric Supply', 'revenue': 2687.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2511.0}, {'customer': 'LIGHTING BY JARED', 'revenue': 2425.33}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 2364.05}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 2058.7}, {'customer': 'St Louis Metro Electric', 'revenue': 2025.88}, {'customer': 'Sunbelt / Louisiana', 'revenue': 1945.62}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 1809.9}, {'customer': 'Lighting Design Company', 'revenue': 1651.4}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 1594.0}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 1439.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 1375.0}, {'customer': '!! Reflections L&M', 'revenue': 1374.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 1274.9}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 1221.0}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 1166.84}, {'customer': 'Lightology', 'revenue': 1155.21}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 1131.05}, {'customer': "Wilkinson's House of Lighting", 'revenue': 891.0}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 890.23}, {'customer': 'HOUZZ SHOP', 'revenue': 874.49}, {'customer': "LOWE'S", 'revenue': 832.88}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 825.0}, {'customer': 'Lights Unlimited', 'revenue': 805.6}, {'customer': "Richard's Lighting", 'revenue': 803.7}, {'customer': 'Lighting Emporium Inc', 'revenue': 785.5}, {'customer': 'Pine Tree Lighting dba Pine Tree Furniture', 'revenue': 779.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 687.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 618.75}, {'customer': 'LJP Enterprises, Inc. dba Southside Lighting Gallery', 'revenue': 618.3}, {'customer': 'House of Carpets', 'revenue': 563.6}, {'customer': 'All About Lights Inc', 'revenue': 559.4}, {'customer': 'Austell Lighting', 'revenue': 550.0}, {'customer': 'Village 1, LLC dba Village Home Stores', 'revenue': 550.0}, {'customer': 'Lighting Design Center (Las Vegas)', 'revenue': 550.0}, {'customer': 'AT HOME LLC dba HOME LIGHTING', 'revenue': 548.95}, {'customer': 'Team Electric Supply, LLC', 'revenue': 504.0}, {'customer': 'Accent Lighting (OR)', 'revenue': 504.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 495.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 488.0}, {'customer': 'Re-Lighting Inc', 'revenue': 486.2}, {'customer': 'Uncommon Living fka Lighting Unlimited (MS)', 'revenue': 458.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 458.0}, {'customer': 'IBS Lighting LLC', 'revenue': 458.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 450.01}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 439.68}, {'customer': 'Ocean Pacific Lighting Inc', 'revenue': 428.24}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 406.7}, {'customer': 'Connecticut Lighting Center', 'revenue': 403.2}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 385.83}, {'customer': 'Urban Rustic Living', 'revenue': 375.62}, {'customer': 'Rexel USA, Inc. : Mayer Electric Gulfport MS', 'revenue': 343.75}, {'customer': 'Signature Lighting & Fans dba Whitfield Lighting and Furnitu', 'revenue': 302.5}, {'customer': 'Pine Lighting', 'revenue': 302.5}, {'customer': 'Royaume Luminaire', 'revenue': 302.5}, {'customer': 'Net Retailers, LLC', 'revenue': 297.45}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 296.46}, {'customer': 'Asburys Design', 'revenue': 295.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 275.0}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 275.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 275.0}, {'customer': 'The Jarrell Company', 'revenue': 275.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 275.0}, {'customer': "Randolph's Door & Lighting dba RDHS Inc", 'revenue': 275.0}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 275.0}, {'customer': 'Plyler Supply Co. Inc DBA The Lighting Loft', 'revenue': 275.0}, {'customer': 'US Electrical Services, Inc DBA Yale Electric Supply', 'revenue': 275.0}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 275.0}, {'customer': 'First Coast Lighting & Fans', 'revenue': 275.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 275.0}, {'customer': 'Stokes Electric Company', 'revenue': 275.0}, {'customer': 'Elaine Everetts Lighting', 'revenue': 275.0}, {'customer': 'GW Keeter Lighting', 'revenue': 275.0}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 275.0}, {'customer': 'Home Front Design', 'revenue': 275.0}, {'customer': 'Pace Lighting Inc', 'revenue': 275.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Owensboro KY', 'revenue': 275.0}, {'customer': '!! Source & Co.', 'revenue': 265.07}, {'customer': 'Cape Electrical Supply', 'revenue': 258.5}, {'customer': 'Veradyne Unlimited', 'revenue': 258.46}, {'customer': 'Melody Lighting, Inc', 'revenue': 257.06}, {'customer': 'City Lightz London', 'revenue': 251.9}, {'customer': 'King Electric Company Inc', 'revenue': 246.73}, {'customer': 'Lyteworks', 'revenue': 235.76}, {'customer': 'ZenSupply Inc', 'revenue': 233.87}, {'customer': 'Van Stavern Interiors Inc', 'revenue': 233.5}, {'customer': 'Flinz Holdings LLC', 'revenue': 229.0}, {'customer': '!! WT Lighting', 'revenue': 229.0}, {'customer': 'Endacott Lighting DBA S&S Edison', 'revenue': 229.0}, {'customer': 'Illuminating Expressions (Evansville)', 'revenue': 229.0}, {'customer': 'SOUTHWEST PLUMBING SUPPLY', 'revenue': 229.0}, {'customer': 'North Coast Lighting, LLC (SE)', 'revenue': 229.0}, {'customer': 'Design Superstore / Designco', 'revenue': 229.0}, {'customer': 'Cayce Mill Supply Co', 'revenue': 229.0}, {'customer': 'Bright Ideas Lighting & More (Bridgeport)', 'revenue': 229.0}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 229.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 229.0}, {'customer': 'LIGHTING CONCEPTS, LLC (GA)', 'revenue': 229.0}, {'customer': 'Lampworks dba Lamp & Shadework', 'revenue': 229.0}, {'customer': 'White Star Supply LLC', 'revenue': 229.0}, {'customer': 'Kendall Electric Inc', 'revenue': 229.0}, {'customer': '!! Davis Lighting', 'revenue': 226.65}, {'customer': 'Enterprise Wholesale, Inc', 'revenue': 225.24}, {'customer': 'Menards, Inc', 'revenue': 217.55}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Teche Electric Supply', 'revenue': 213.0}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 213.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 213.0}, {'customer': '!! Applico, LLC', 'revenue': 213.0}, {'customer': 'Grand Rapids Lighting', 'revenue': 213.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Cookeville TN', 'revenue': 213.0}, {'customer': 'The Broadway Showroom dba Bliss Lighting', 'revenue': 213.0}, {'customer': 'Lumen Nation LLC', 'revenue': 213.0}, {'customer': 'WOLFE LIGHTING & ACCENTS : WOLFE LIGHTING & ACCENTS (TWIN FA', 'revenue': 213.0}, {'customer': 'Lighting Incorporated', 'revenue': 213.0}, {'customer': 'Bright City Lights', 'revenue': 213.0}, {'customer': 'Fort Worth Lighting', 'revenue': 213.0}, {'customer': 'Butler Lighting of High Point', 'revenue': 213.0}, {'customer': 'Lighting Instyle', 'revenue': 208.75}, {'customer': 'Lifestyles Store Inc', 'revenue': 194.65}, {'customer': 'Hagens Lighting', 'revenue': 191.8}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 183.2}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': 176.0}, {'customer': 'Galleria Lighting Inc.', 'revenue': 82.5}, {'customer': 'The Lighting Corner', 'revenue': 0.0}, {'customer': 'Light Gallery Plus', 'revenue': 0.0}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 0.0}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB)', 'revenue': -229.16}, {'customer': 'Rensen House of Lights', 'revenue': -2454.0}] | [{'item': '1-2221-6-109', 'desc': 'Salerno 6-Light Chandelier in Polished Nickel', 'available': 110}, {'item': '1-2221-6-83', 'desc': 'Salerno 6-Light Chandelier in Bisque White', 'available': 46}, {'item': '1-2221-6-89', 'desc': 'Salerno 6-Light Chandelier in Matte Black', 'available': 24}] |
| 7-1804-4-322 | Crawford 4-Light Pendant in Warm Brass | CRAWF | 286,652.26 | 1,374 | — | 2026-07-11 | [{'customer': 'FERGUSON', 'revenue': 73131.19}, {'customer': 'BUILD.COM', 'revenue': 42229.85}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 15666.75}, {'customer': 'BELAMI ECommerce', 'revenue': 10084.8}, {'customer': 'WAYFAIR LLC', 'revenue': 8312.05}, {'customer': 'First Coast Lighting & Fans', 'revenue': 6403.7}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 5824.1}, {'customer': 'Sunbelt / Louisiana', 'revenue': 5583.0}, {'customer': 'Lighting World', 'revenue': 5556.75}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 5501.95}, {'customer': 'The Home Depot', 'revenue': 5473.69}, {'customer': 'LIGHTING BY JARED', 'revenue': 4535.94}, {'customer': 'St Louis Metro Electric', 'revenue': 4250.0}, {'customer': 'LAMPS PLUS INC', 'revenue': 4223.74}, {'customer': "Richard's Lighting", 'revenue': 3865.62}, {'customer': 'Lifestyles Store Inc', 'revenue': 3028.92}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 3019.62}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 2681.4}, {'customer': 'Muska Lighting', 'revenue': 2540.1}, {'customer': 'Union Lighting (Montreal)', 'revenue': 2124.4}, {'customer': 'Lighting Incorporated', 'revenue': 1986.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 1948.56}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 1834.44}, {'customer': 'Lamps.com, Inc', 'revenue': 1785.54}, {'customer': "LOWE'S", 'revenue': 1730.21}, {'customer': 'Wiseway Supply', 'revenue': 1576.0}, {'customer': 'Lighting Design Company', 'revenue': 1564.5}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting : DesignDir', 'revenue': 1391.6}, {'customer': 'Inline Electric Supply', 'revenue': 1390.0}, {'customer': 'Hudson Parc Lighting & Design', 'revenue': 1272.0}, {'customer': 'Cambridge Interiors dba Inspired Interiors', 'revenue': 1232.8}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 1206.3}, {'customer': "Wilkinson's House of Lighting", 'revenue': 1206.0}, {'customer': 'Flambeaux Gas & Electric Lights', 'revenue': 1206.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 1160.0}, {'customer': 'Denali Lighting LLC', 'revenue': 1147.34}, {'customer': 'IB Lighting Supply', 'revenue': 1112.0}, {'customer': 'Lights Unlimited', 'revenue': 1112.0}, {'customer': 'Bayside Electric Supply Co', 'revenue': 1020.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 1020.0}, {'customer': 'Wilson Lighting of Naples Inc', 'revenue': 1017.25}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 994.0}, {'customer': 'Illuminations', 'revenue': 992.2}, {'customer': 'Menards, Inc', 'revenue': 969.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 950.4}, {'customer': 'VALENCIA LIGHTING & DESIGN', 'revenue': 928.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 928.0}, {'customer': 'Elektra Lights & Fans Inc', 'revenue': 834.0}, {'customer': 'American Lighting Inc', 'revenue': 834.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 834.0}, {'customer': 'The Light House (AL)', 'revenue': 834.0}, {'customer': 'Liza Joyner Designs Ryser', 'revenue': 834.0}, {'customer': 'Timberlake Lighting of Lynchburg', 'revenue': 834.0}, {'customer': 'Lightology', 'revenue': 832.64}, {'customer': 'Wholesale Lighting Inc (FL)', 'revenue': 750.6}, {'customer': 'New Age Interiors', 'revenue': 745.98}, {'customer': 'Passion Lighting DBA Cannon & Crossbow', 'revenue': 742.0}, {'customer': 'Legend Lighting', 'revenue': 696.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Daphne AL', 'revenue': 696.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba Billows Electric', 'revenue': 657.0}, {'customer': "Isabelle's Lighting", 'revenue': 643.86}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (BOCA RATON)', 'revenue': 625.5}, {'customer': 'Rainbow Lighting (NY)', 'revenue': 624.15}, {'customer': 'Unique Lighting Inc', 'revenue': 611.6}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 600.23}, {'customer': 'Southern Pipe & Supply (GA)', 'revenue': 598.46}, {'customer': 'Caminiti Associates Inc dba CAI Designs', 'revenue': 595.08}, {'customer': 'Net Retailers, LLC', 'revenue': 594.72}, {'customer': 'The Lighting Gallery (Huntington Station)', 'revenue': 591.3}, {'customer': 'ShellKat LLC dba Aldridge Appliance', 'revenue': 580.0}, {'customer': "Butler's Electric (Myrtle Beach)", 'revenue': 576.55}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 556.0}, {'customer': 'Lighting Resource Studio', 'revenue': 556.0}, {'customer': 'Home & Light Valdosta', 'revenue': 556.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 556.0}, {'customer': 'F.W. Webb Company', 'revenue': 556.0}, {'customer': 'Fort Worth Lighting', 'revenue': 556.0}, {'customer': 'Torrington Supply dba Torrco', 'revenue': 556.0}, {'customer': 'Lightstyles by Light Bulbs Etc (Orange) (BMD)', 'revenue': 556.0}, {'customer': 'Lighting Emporium Inc', 'revenue': 556.0}, {'customer': 'Queen City Stone dba Queen City Studio', 'revenue': 556.0}, {'customer': 'Hagens Lighting', 'revenue': 556.0}, {'customer': 'Winsupply Elizabethtown : Winsupply dba Bowling Green WLC 14', 'revenue': 556.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 556.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 545.0}, {'customer': 'Cregger Co LLC', 'revenue': 527.76}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (PARAMUS)', 'revenue': 522.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 510.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': 510.0}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 500.6}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 493.74}, {'customer': 'The Lamp and Lighthouse (TN)', 'revenue': 470.69}, {'customer': 'Locke Supply', 'revenue': 464.0}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 464.0}, {'customer': "Garbe's Lighting & Hardware LLC", 'revenue': 464.0}, {'customer': 'The Light House Gallery (MO)', 'revenue': 464.0}, {'customer': 'BEAUTIFUL LIGHTS LLC', 'revenue': 461.56}, {'customer': 'Capitol Lighting Gallery', 'revenue': 444.8}, {'customer': 'BBC Lighting & Supply', 'revenue': 438.0}, {'customer': 'White Star Supply LLC', 'revenue': 438.0}, {'customer': "!! Amber's Lighting", 'revenue': 438.0}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 432.5}, {'customer': 'Cleveland Lighting Center', 'revenue': 372.3}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 359.16}, {'customer': 'Dhillon Lighting Inc (Edmonton) : Dhillon Lighting Manitoba', 'revenue': 350.71}, {'customer': 'Dhillon Lighting Inc (Edmonton)', 'revenue': 340.23}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 328.5}, {'customer': 'Cardinal Lights Corp DBA Manasquan Lighting', 'revenue': 296.34}, {'customer': 'The Lighting Marketplace DBA FixtureFarm', 'revenue': 293.04}, {'customer': 'Gross Lighting & Home', 'revenue': 278.0}, {'customer': 'Hortons of LaGrange', 'revenue': 278.0}, {'customer': 'Construction Resources Co LLC dba CR Lighting', 'revenue': 278.0}, {'customer': 'Home Lighting Inc. (PA)', 'revenue': 278.0}, {'customer': 'Asburys Design', 'revenue': 246.21}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 245.0}, {'customer': 'SBS Electric & Lighting', 'revenue': 243.17}, {'customer': '!! Savoy House Cash Sales', 'revenue': 242.0}, {'customer': 'Morrison Supply Co (Lubbock) : Morrison Supply Co (Abilene)', 'revenue': 232.0}, {'customer': 'House of Lights of Sanford Inc', 'revenue': 232.0}, {'customer': 'Sanders Supply Inc', 'revenue': 232.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 219.0}, {'customer': 'Denney Electric Supply (Ambler, PA)', 'revenue': 219.0}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 199.2}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 197.1}, {'customer': 'Kendall Electric Inc', 'revenue': 195.88}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 181.19}, {'customer': 'Sonepar dba Capital Electric', 'revenue': 109.5}, {'customer': 'Kay Electric Supply Co. Inc', 'revenue': 93.2}, {'customer': 'Fixture This', 'revenue': 38.5}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba All Phase Pet', 'revenue': 0.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 0.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 0.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 0.0}, {'customer': 'Elliott Electric Supply Inc', 'revenue': 0.0}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 0.0}, {'customer': 'State Electric Supply', 'revenue': 0.0}, {'customer': 'Stokes Electric Company', 'revenue': 0.0}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 0.0}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': 0.0}, {'customer': 'Lighting and Design by J & K Electric', 'revenue': 0.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 0.0}, {'customer': 'Lamp Shop of Naples Co', 'revenue': 0.0}, {'customer': 'Valley Supply Co', 'revenue': 0.0}, {'customer': '!! Lando Lighting', 'revenue': -90.42}, {'customer': 'The Lamp Outlet : Quinn Wholesale LLC dba Quintessential Lig', 'revenue': -113.1}, {'customer': 'Lighting EFX', 'revenue': -1021.48}] | [{'item': '6-1802-3-SN', 'desc': 'Crawford 3-Light Ceiling Light in Satin Nickel', 'available': 87}, {'item': '7-1803-3-SN', 'desc': 'Crawford 3-Light Pendant in Satin Nickel', 'available': 85}, {'item': '9-1801-1-89', 'desc': 'Crawford 1-Light Wall Sconce in Matte Black', 'available': 66}, {'item': '7-1803-3-89', 'desc': 'Crawford 3-Light Pendant in Matte Black', 'available': 55}, {'item': '9-1801-1-SN', 'desc': 'Crawford 1-Light Wall Sconce in Satin Nickel', 'available': 53}, {'item': '7-1804-4-89', 'desc': 'Crawford 4-Light Pendant in Matte Black', 'available': 52}, {'item': '6-1802-3-322', 'desc': 'Crawford 3-Light Ceiling Light in Warm Brass', 'available': 44}, {'item': '7-1804-4-SN', 'desc': 'Crawford 4-Light Pendant in Satin Nickel', 'available': 36}, {'item': '7-1803-3-322', 'desc': 'Crawford 3-Light Pendant in Warm Brass', 'available': 27}, {'item': '9-1801-1-322', 'desc': 'Crawford 1-Light Wall Sconce in Warm Brass', 'available': 17}] |
| 7-1774-6-320 | Ashburn 6-Light Pendant in Warm Brass and Rope | ASHBU | 233,394.02 | 560 | — | 2026-07-16 | [{'customer': 'WAYFAIR LLC', 'revenue': 44777.92}, {'customer': 'BUILD.COM', 'revenue': 19259.91}, {'customer': 'FERGUSON', 'revenue': 12385.36}, {'customer': 'LAMPS PLUS INC', 'revenue': 11522.02}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 11159.65}, {'customer': 'First Coast Lighting & Fans', 'revenue': 8348.7}, {'customer': 'Muska Lighting', 'revenue': 7390.4}, {'customer': 'BELAMI ECommerce', 'revenue': 5428.55}, {'customer': 'Lighting World', 'revenue': 4508.2}, {'customer': '!! U.S. Electrical Services Inc. dba Wiedenbach Brown', 'revenue': 3992.0}, {'customer': 'M & M Lighting, L.P.', 'revenue': 3326.0}, {'customer': 'The Lighting Corner', 'revenue': 3069.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 2913.75}, {'customer': 'Lightology', 'revenue': 2872.96}, {'customer': 'Lighting Design Company', 'revenue': 2762.1}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 2387.6}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 2283.78}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 1944.58}, {'customer': 'LIGHTING BY JARED', 'revenue': 1906.62}, {'customer': 'Hye Lighting Co', 'revenue': 1804.37}, {'customer': 'Destin Lighting', 'revenue': 1696.95}, {'customer': '!! Lando Lighting', 'revenue': 1686.52}, {'customer': 'Florida Lighting dba Lighting Depot dba Fla Lighting Inc', 'revenue': 1672.51}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 1587.0}, {'customer': '!! Modern Komfort Furnishings Inc.', 'revenue': 1560.4}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 1557.0}, {'customer': 'The Lamp Outlet : Quinn Wholesale LLC dba Quintessential Lig', 'revenue': 1419.8}, {'customer': 'Lamps.com, Inc', 'revenue': 1392.08}, {'customer': 'Inline Electric Supply', 'revenue': 1270.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 1270.0}, {'customer': 'Southern Lights', 'revenue': 1270.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 1247.4}, {'customer': 'Capitol Lighting Gallery', 'revenue': 1233.0}, {'customer': 'Echelon Interiors', 'revenue': 1204.15}, {'customer': 'Southern Interiors & Lighting (Warner Robins)', 'revenue': 1164.0}, {'customer': 'Walnut Creek Lighting', 'revenue': 1164.0}, {'customer': 'Rainbow Lighting (NY)', 'revenue': 1143.0}, {'customer': 'Light N Leisure Inc', 'revenue': 1058.0}, {'customer': 'LJP Enterprises, Inc. dba Southside Lighting Gallery', 'revenue': 1058.0}, {'customer': 'Design Superstore / Designco', 'revenue': 1058.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 1047.75}, {'customer': 'Winsupply Elizabethtown : Winsupply Hendersonville TN', 'revenue': 1028.0}, {'customer': 'Lighting Incorporated', 'revenue': 1009.25}, {'customer': 'Hubbard Supplyhouse', 'revenue': 1007.0}, {'customer': 'St Louis Metro Electric', 'revenue': 1006.36}, {'customer': 'Southern Lighting Gallery (Augusta) : Southern Lighting Gall', 'revenue': 948.1}, {'customer': 'Dement Lighting', 'revenue': 928.4}, {'customer': 'Lifestyles Store Inc', 'revenue': 899.3}, {'customer': 'Light and Day', 'revenue': 843.7}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 793.5}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (BOCA RATON)', 'revenue': 793.5}, {'customer': 'Royaume Luminaire', 'revenue': 698.5}, {'customer': 'LIGHTSHINE INC DBA URBAN LIGHTS', 'revenue': 694.18}, {'customer': 'The Lighting Showroom, Inc (CA)', 'revenue': 689.06}, {'customer': "Hinkley's Lighting Factory", 'revenue': 678.6}, {'customer': 'Eagle Lighting', 'revenue': 675.65}, {'customer': 'Lighting by Lavonne, LLC', 'revenue': 635.0}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 635.0}, {'customer': 'Gross Lighting & Home', 'revenue': 635.0}, {'customer': 'Greer Lighting Center LLC', 'revenue': 635.0}, {'customer': 'VP Supply', 'revenue': 635.0}, {'customer': 'Home & Light Valdosta', 'revenue': 635.0}, {'customer': 'Passion Lighting DBA Cannon & Crossbow', 'revenue': 635.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 635.0}, {'customer': 'Lighting Palace Design Center', 'revenue': 635.0}, {'customer': 'Paramont- EO, Inc', 'revenue': 635.0}, {'customer': "Wilkinson's House of Lighting", 'revenue': 635.0}, {'customer': 'Coley Electric & Plumbing (Douglas)', 'revenue': 635.0}, {'customer': 'Lighting by Design LLC (Maryland)', 'revenue': 635.0}, {'customer': 'Aztec Lighting', 'revenue': 635.0}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 635.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 635.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 635.0}, {'customer': "Butler's Electric (Myrtle Beach)", 'revenue': 635.0}, {'customer': 'Mayson Enterprises dba Aura Lighting', 'revenue': 635.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Teche Electric Supply', 'revenue': 635.0}, {'customer': 'Sun Lighting (Tempe)', 'revenue': 635.0}, {'customer': 'Milliken Investments dba Shallotte Electric Stores', 'revenue': 635.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 614.0}, {'customer': 'City Lights (San Francisco)', 'revenue': 595.73}, {'customer': 'Richardson Lighting', 'revenue': 581.9}, {'customer': "Don's Light House LTD", 'revenue': 581.9}, {'customer': 'Consumers Lighting and Lamps', 'revenue': 574.95}, {'customer': 'Expressions Home Lighting', 'revenue': 571.5}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 558.8}, {'customer': 'Paradise Lighting', 'revenue': 548.9}, {'customer': 'Litemode Limited', 'revenue': 548.9}, {'customer': 'Queen City Stone dba Queen City Studio', 'revenue': 529.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 529.0}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 529.0}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba Billows Electric', 'revenue': 529.0}, {'customer': 'Lighting by Design (Exton, PA)', 'revenue': 529.0}, {'customer': 'Lamp Shop of Naples Co', 'revenue': 529.0}, {'customer': 'Accent Lighting (OR)', 'revenue': 529.0}, {'customer': "Christie's Lighting Gallery", 'revenue': 529.0}, {'customer': 'Front Street Lighting', 'revenue': 529.0}, {'customer': 'RDIC LLC dba Russell Home Decor / Russell Lands', 'revenue': 529.0}, {'customer': 'Fort Worth Lighting', 'revenue': 529.0}, {'customer': 'Legacy Lighting, LLC', 'revenue': 529.0}, {'customer': 'Timberlake Lighting of Lynchburg', 'revenue': 529.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 529.0}, {'customer': 'Bayside Electric Supply Co', 'revenue': 529.0}, {'customer': 'Lumber One Home Center', 'revenue': 529.0}, {'customer': 'Alice Stillabower Design', 'revenue': 529.0}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 529.0}, {'customer': 'Lighting Solutions Design (Owensboro)', 'revenue': 529.0}, {'customer': 'Cardinal Lights Corp DBA Manasquan Lighting', 'revenue': 529.0}, {'customer': "Richard's Lighting", 'revenue': 512.5}, {'customer': 'Lights Unlimited', 'revenue': 508.0}, {'customer': 'Idlewood Electric Supply', 'revenue': 508.0}, {'customer': 'Wilson Lighting of Naples Inc', 'revenue': 508.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 508.0}, {'customer': 'F.W. Webb Company', 'revenue': 507.84}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 499.0}, {'customer': 'Rite Rug DBA Capital Lighting', 'revenue': 499.0}, {'customer': 'Home Lighting Inc. (PA)', 'revenue': 499.0}, {'customer': 'IM Lighting', 'revenue': 499.0}, {'customer': 'Ellen Lighting and Hardware', 'revenue': 499.0}, {'customer': 'The Lighting Gallery (Huntington Station)', 'revenue': 476.1}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 465.58}, {'customer': 'Lyteworks', 'revenue': 460.35}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 449.1}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 439.12}, {'customer': "LOWE'S", 'revenue': 424.15}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 423.2}, {'customer': 'Connecticut Lighting Center', 'revenue': 423.2}, {'customer': 'Lighting Instyle', 'revenue': 416.8}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 412.74}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 342.8}, {'customer': 'Euroluce dba Home Lighting', 'revenue': 326.42}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': 99.9}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 12.7}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': -95.22}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': -102.97}, {'customer': 'Lighting Zone, Inc', 'revenue': -1350.0}] | [{'item': '3-1773-6-320', 'desc': 'Ashburn 6-Light Pendant in Warm Brass and Rope', 'available': 21}] |
| 1-312-15-322 | Middleton 15-Light Chandelier in Warm Brass | MIDDL | 188,669.81 | 218 | — | 2026-07-03 | [{'customer': 'WAYFAIR LLC', 'revenue': 19380.81}, {'customer': 'FERGUSON', 'revenue': 13821.8}, {'customer': 'Inline Electric Supply', 'revenue': 9599.0}, {'customer': 'Lights Unlimited', 'revenue': 6408.0}, {'customer': 'LAMPS PLUS INC', 'revenue': 5464.05}, {'customer': 'BELAMI ECommerce', 'revenue': 4723.35}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 4700.8}, {'customer': 'Lighting Design Company', 'revenue': 4411.0}, {'customer': "LOWE'S", 'revenue': 4150.04}, {'customer': 'First Coast Lighting & Fans', 'revenue': 3884.0}, {'customer': 'BUILD.COM', 'revenue': 3858.01}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': 3728.0}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 3591.24}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 3435.0}, {'customer': 'Palmer Electric Co dba Showcase Lighting (FL)', 'revenue': 3373.18}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 3301.0}, {'customer': 'The Brecher Co, Inc', 'revenue': 3154.4}, {'customer': 'IM Lighting', 'revenue': 3136.1}, {'customer': 'The Factory', 'revenue': 3052.0}, {'customer': 'Galleria Lighting Inc.', 'revenue': 3004.7}, {'customer': 'Home & Light Valdosta', 'revenue': 2913.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 2796.0}, {'customer': 'Lighting World', 'revenue': 2485.6}, {'customer': 'Farvahar Inc Dba Posh Lighting', 'revenue': 2389.59}, {'customer': 'Lighting Incorporated', 'revenue': 2378.75}, {'customer': 'F.W. Webb Company', 'revenue': 2352.31}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 2136.0}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 2136.0}, {'customer': 'Paulus Enterprises dba James & Co Lighting', 'revenue': 2136.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2081.0}, {'customer': 'Hortons of LaGrange', 'revenue': 1902.96}, {'customer': 'OSMOND DESIGNS INC.', 'revenue': 1747.5}, {'customer': 'Lamp Warehouse dba Lighting Expo', 'revenue': 1708.8}, {'customer': 'Aggieland Lighting', 'revenue': 1695.5}, {'customer': 'Lamps.com, Inc', 'revenue': 1670.12}, {'customer': 'Echelon Interiors', 'revenue': 1350.78}, {'customer': 'Southern Pipe & Supply (GA)', 'revenue': 1296.31}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 1281.5}, {'customer': '!! Gagnun Interior Concept Studio Inc DBA Boutique Intempore', 'revenue': 1281.5}, {'customer': 'The Electrical & Plumbing Store : Electrical & Plumbing Stor', 'revenue': 1281.5}, {'customer': 'Royal Lighting (Canada) dba Royal Lighting Limited Partnersh', 'revenue': 1281.5}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 1281.5}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba Billows Electric', 'revenue': 1165.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 1165.0}, {'customer': 'Stokes Electric Company', 'revenue': 1165.0}, {'customer': 'Muska Lighting', 'revenue': 1165.0}, {'customer': 'Paramont- EO, Inc', 'revenue': 1165.0}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 1165.0}, {'customer': 'Hagens Lighting', 'revenue': 1165.0}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 1165.0}, {'customer': 'Bright Ideas (Rochester)', 'revenue': 1165.0}, {'customer': 'Scott Electric Co', 'revenue': 1165.0}, {'customer': 'VALENCIA LIGHTING & DESIGN', 'revenue': 1165.0}, {'customer': "Seth's Lighting & Assoc. Inc", 'revenue': 1165.0}, {'customer': 'Design Superstore / Designco', 'revenue': 1165.0}, {'customer': 'Home Lighting Inc. (PA)', 'revenue': 1165.0}, {'customer': '!! Lighting Connections LLC', 'revenue': 1165.0}, {'customer': 'Dhillon Lighting Inc (Edmonton)', 'revenue': 1132.45}, {'customer': 'Elm Ridge Lighting & Interior', 'revenue': 1068.1}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 1068.1}, {'customer': 'St Louis Metro Electric', 'revenue': 1025.2}, {'customer': '!! CFSI Interiors Limited DBA Taylor Flooring', 'revenue': 1007.6}, {'customer': 'Asburys Design', 'revenue': 971.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 971.0}, {'customer': 'Ray Mart Inc dba Tri-Supply', 'revenue': 971.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 971.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 961.29}, {'customer': "Isabelle's Lighting", 'revenue': 932.16}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 916.62}, {'customer': "Designer's Mart", 'revenue': 916.0}, {'customer': 'Hi-Light Decorating', 'revenue': 916.0}, {'customer': 'Legend Lighting', 'revenue': 916.0}, {'customer': 'Timberlake Lighting of Lynchburg', 'revenue': 916.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 873.75}, {'customer': 'Mainland Lighting Warehouse', 'revenue': 753.41}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 745.6}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 687.0}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 627.33}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 545.0}, {'customer': 'Wilson 6 Enterprises Inc. DBA: Mountain Lighting & Design', 'revenue': 458.0}, {'customer': 'LIGHTING BY JARED', 'revenue': 93.2}, {'customer': 'Winsupply Elizabethtown : Winsupply dba Bowling Green WLC 14', 'revenue': 0.0}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': -373.7}, {'customer': 'Accent Lighting (KS)', 'revenue': -634.5}] | [{'item': '1-308-8-44', 'desc': 'Middleton 8-Light Chandelier in Classic Bronze', 'available': 65}, {'item': '1-308-8-322', 'desc': 'Middleton 8-Light Chandelier in Warm Brass', 'available': 62}, {'item': '1-308-8-89', 'desc': 'Middleton 8-Light Chandelier in Matte Black', 'available': 62}, {'item': '1-307-6-322', 'desc': 'Middleton 6-Light Chandelier in Warm Brass', 'available': 48}, {'item': '1-307-6-89', 'desc': 'Middleton 6-Light Chandelier in Matte Black', 'available': 43}, {'item': '1-308-8-SN', 'desc': 'Middleton 8-Light Chandelier in Satin Nickel', 'available': 41}, {'item': '1-312-15-89', 'desc': 'Middleton 15-Light Chandelier in Matte Black', 'available': 32}, {'item': '1-310-10-322', 'desc': 'Middleton 10-Light Chandelier in Warm Brass', 'available': 31}, {'item': '1-310-10-89', 'desc': 'Middleton 10-Light Chandelier in Matte Black', 'available': 28}] |
| 9-303-1-322 | Monroe 1-Light Wall Sconce in Warm Brass | MONRO | 186,435.44 | 3,151 | — | 2026-07-03 | [{'customer': 'WAYFAIR LLC', 'revenue': 38090.31}, {'customer': 'BUILD.COM', 'revenue': 17884.75}, {'customer': 'FERGUSON', 'revenue': 14022.57}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 10339.0}, {'customer': 'Gadsden Lighting Showroom Inc', 'revenue': 6027.24}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 5788.58}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 4748.25}, {'customer': 'Inline Electric Supply', 'revenue': 4490.0}, {'customer': 'LAMPS PLUS INC', 'revenue': 4126.3}, {'customer': 'Shades of Light', 'revenue': 3441.69}, {'customer': 'Sunbelt / Louisiana', 'revenue': 3306.5}, {'customer': "Richard's Lighting", 'revenue': 2877.57}, {'customer': 'Lifestyles Store Inc', 'revenue': 2796.0}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 2733.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 2544.1}, {'customer': 'BELAMI ECommerce', 'revenue': 2033.39}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 1886.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 1841.0}, {'customer': 'Dealers Electrical Sys. Co (Bryan)', 'revenue': 1748.0}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 1629.06}, {'customer': 'LIGHTING BY JARED', 'revenue': 1499.54}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 1432.44}, {'customer': "Wilkinson's House of Lighting", 'revenue': 1386.4}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 1185.0}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 1114.0}, {'customer': 'The Lighting Gallery (Huntington Station)', 'revenue': 1066.0}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 1056.3}, {'customer': 'Lighting World', 'revenue': 948.8}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 945.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 884.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 882.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 859.12}, {'customer': 'Gross Lighting & Home : Indiana Lighting Center', 'revenue': 857.0}, {'customer': 'Illuminate Lighting', 'revenue': 834.0}, {'customer': 'Lights Unlimited', 'revenue': 819.4}, {'customer': 'Western Chandelier Co', 'revenue': 793.45}, {'customer': 'Kendall Electric Inc', 'revenue': 784.0}, {'customer': 'Parrish Family Enterprises dba American Lighting and Design', 'revenue': 780.81}, {'customer': 'Lighting Design Company', 'revenue': 717.3}, {'customer': 'Net Retailers, LLC', 'revenue': 709.35}, {'customer': 'Ocean Pacific Lighting Inc', 'revenue': 705.54}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 622.0}, {'customer': 'Richardson Lighting', 'revenue': 616.39}, {'customer': 'Stokes Electric Company', 'revenue': 616.0}, {'customer': 'Chester Lighting : Doylestown Electric', 'revenue': 592.97}, {'customer': 'The Brecher Co, Inc', 'revenue': 588.31}, {'customer': 'IBS Lighting LLC', 'revenue': 588.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 588.0}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 576.4}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 575.0}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 574.0}, {'customer': 'Design Superstore / Designco', 'revenue': 574.0}, {'customer': 'House of Carpets', 'revenue': 563.05}, {'customer': 'Hudson Parc Lighting & Design', 'revenue': 556.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 530.6}, {'customer': 'J.D. Lighting', 'revenue': 503.8}, {'customer': 'St Louis Metro Electric', 'revenue': 482.24}, {'customer': 'McManus Company', 'revenue': 474.0}, {'customer': 'Dement Lighting', 'revenue': 469.2}, {'customer': 'LDB Holdings LLC dba CW Floors and Lighting', 'revenue': 458.0}, {'customer': 'Lightology', 'revenue': 453.36}, {'customer': 'Lighting Emporium Inc', 'revenue': 445.6}, {'customer': 'Southern Pipe & Supply (GA)', 'revenue': 435.62}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 431.2}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 431.2}, {'customer': 'The Electrical & Plumbing Store : Electrical & Plumbing Stor', 'revenue': 431.2}, {'customer': 'Laura of Pembroke', 'revenue': 416.74}, {'customer': 'HOUZZ SHOP', 'revenue': 416.22}, {'customer': 'Multi-Luminaire Gatineau : Multi-Luminaire (Ottawa)', 'revenue': 411.4}, {'customer': 'Elan Studio Lighting', 'revenue': 410.0}, {'customer': 'Flinz Holdings LLC', 'revenue': 410.0}, {'customer': 'Denali Lighting LLC', 'revenue': 404.83}, {'customer': 'Locke Supply', 'revenue': 392.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 392.0}, {'customer': 'Construction Resources Co LLC dba CR Lighting', 'revenue': 392.0}, {'customer': 'Virginia-Carolina Lighting Inc dba Coastal Lighting & Supply', 'revenue': 392.0}, {'customer': '!! U.S. Electrical Services Inc. dba Wiedenbach Brown', 'revenue': 385.0}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 385.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 375.08}, {'customer': 'F.W. Webb Company', 'revenue': 360.6}, {'customer': 'CES Acquisition dba Cardello Lighting & Electric Supply', 'revenue': 360.0}, {'customer': 'KLS LLC dba Spectrum Lighting', 'revenue': 360.0}, {'customer': 'American Lighting Inc', 'revenue': 360.0}, {'customer': "Isabelle's Lighting", 'revenue': 353.44}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 352.88}, {'customer': 'Queen City Stone dba Queen City Studio', 'revenue': 345.31}, {'customer': 'Lighting Instyle', 'revenue': 344.56}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 344.4}, {'customer': 'Denney Electric Supply (Ambler, PA)', 'revenue': 328.0}, {'customer': 'The Lighting Corner', 'revenue': 328.0}, {'customer': 'Sisters Lighting DBA Anthology Lighting', 'revenue': 328.0}, {'customer': 'Meuth Wallpaper dba Sugar Bakers', 'revenue': 323.4}, {'customer': 'Lights of Oconee', 'revenue': 318.0}, {'customer': 'Paulus Enterprises dba James & Co Lighting', 'revenue': 318.0}, {'customer': 'Accent Lighting (KS)', 'revenue': 313.6}, {'customer': '!! Carly Blalock Interiors', 'revenue': 311.85}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Teche Electric Supply', 'revenue': 308.0}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 296.8}, {'customer': 'Team Electric Supply, LLC', 'revenue': 294.0}, {'customer': "LOWE'S", 'revenue': 289.94}, {'customer': "Christie's Lighting Gallery", 'revenue': 289.51}, {'customer': 'Gateway Lighting & Design Inc', 'revenue': 280.5}, {'customer': 'The Finishing Touch', 'revenue': 269.37}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 264.55}, {'customer': 'Gallery of Lighting (Holder Electric)', 'revenue': 262.3}, {'customer': 'Home & Light Valdosta', 'revenue': 256.67}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 246.65}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba North Coast Light', 'revenue': 246.0}, {'customer': '!! Ana Cole Interiors Ltd', 'revenue': 245.0}, {'customer': 'Lighting Incorporated', 'revenue': 231.0}, {'customer': 'Rite Rug DBA Capital Lighting', 'revenue': 231.0}, {'customer': 'Hortons of LaGrange', 'revenue': 231.0}, {'customer': 'Pineridge Hollow/Corp 3641015', 'revenue': 215.6}, {'customer': 'Royal Lighting (Canada) dba Royal Lighting Limited Partnersh', 'revenue': 215.6}, {'customer': 'Cregger Co LLC', 'revenue': 212.43}, {'customer': 'The Lighthouse (ME)', 'revenue': 208.32}, {'customer': 'Southern Pipe & Supply (LA)', 'revenue': 207.89}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 196.0}, {'customer': 'Anzalone Electric', 'revenue': 196.0}, {'customer': 'The Jarrell Company', 'revenue': 196.0}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': 196.0}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 196.0}, {'customer': 'Southern Interiors & Lighting (Warner Robins)', 'revenue': 196.0}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 194.04}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (HANOVER)', 'revenue': 184.5}, {'customer': 'Aiken Lighting', 'revenue': 183.25}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 180.4}, {'customer': 'Cayce Mill Supply Co', 'revenue': 177.62}, {'customer': 'Wilson 6 Enterprises Inc. DBA: Mountain Lighting & Design', 'revenue': 176.4}, {'customer': 'Pine Lighting', 'revenue': 175.48}, {'customer': 'Lamps.com, Inc', 'revenue': 167.69}, {'customer': 'The Home Depot', 'revenue': 166.76}, {'customer': 'Sun Lighting (Tempe)', 'revenue': 164.0}, {'customer': 'Mathes of Alabama Elec. Supply', 'revenue': 164.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 164.0}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 164.0}, {'customer': 'Premier Bath, Lighting (MI)', 'revenue': 164.0}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 164.0}, {'customer': 'White Star Supply LLC', 'revenue': 164.0}, {'customer': 'Ellen Lighting and Hardware', 'revenue': 154.0}, {'customer': 'Colonial Electric Supply Co', 'revenue': 154.0}, {'customer': 'Lighting EFX', 'revenue': 152.19}, {'customer': 'IM Lighting', 'revenue': 146.8}, {'customer': 'Butler Lighting of High Point', 'revenue': 146.3}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 144.32}, {'customer': 'First Coast Lighting & Fans', 'revenue': 138.6}, {'customer': 'Idlewood Electric Supply', 'revenue': 131.2}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting', 'revenue': 131.2}, {'customer': 'Light Gallery Plus', 'revenue': 98.0}, {'customer': 'Pine Tree Lighting dba Pine Tree Furniture', 'revenue': 98.0}, {'customer': 'Lighting South LLC', 'revenue': 92.0}, {'customer': 'BGZA, INC. dba BG Design Center', 'revenue': 89.57}, {'customer': 'Southern Lighting (Chattanooga)', 'revenue': 82.0}, {'customer': 'Coco & Dash', 'revenue': 82.0}, {'customer': "Victor's Lighting", 'revenue': 80.0}, {'customer': 'Raymond Desteiger Inc dba Design Direct Lighting : DesignDir', 'revenue': 78.4}, {'customer': 'DISCOUNT PLUMBING & ELECTRIC', 'revenue': 77.0}, {'customer': '!! Gagnun Interior Concept Studio Inc DBA Boutique Intempore', 'revenue': 75.79}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 73.29}, {'customer': 'Light Brite Distributing Inc.', 'revenue': 7.33}, {'customer': 'Wiseway Supply', 'revenue': 0.0}, {'customer': '!! Lando Lighting', 'revenue': 0.0}, {'customer': 'Danielhouse Studios, Inc', 'revenue': 0.0}, {'customer': 'Littman Bros Energy Supplies', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting : Light S', 'revenue': -115.9}, {'customer': 'J & B Supply Inc / JBS', 'revenue': -154.0}, {'customer': 'M & M Lighting, L.P.', 'revenue': -366.93}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': -1113.2}] | [{'item': '9-302-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 144}, {'item': '9-303-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 139}, {'item': '9-7144-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 119}, {'item': '9-303-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 92}, {'item': '9-7144-1-44', 'desc': 'Monroe 1-Light Wall Sconce in Classic Bronze', 'available': 64}, {'item': '9-7144-1-109', 'desc': 'Monroe 1-Light Wall Sconce in Polished Nickel', 'available': 61}] |
| M60008NB | 2-Light Ceiling Light in Natural Brass | MSEMI | 163,302.89 | 3,063 | — | 2026-07-03 | [{'customer': 'The Home Depot', 'revenue': 34605.62}, {'customer': 'BUILD.COM', 'revenue': 29943.33}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 16677.31}, {'customer': 'WAYFAIR LLC', 'revenue': 13475.54}, {'customer': 'FERGUSON', 'revenue': 5868.75}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 4592.8}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 4535.79}, {'customer': 'Menards, Inc', 'revenue': 3286.19}, {'customer': 'Inline Electric Supply', 'revenue': 2354.0}, {'customer': "Richard's Lighting", 'revenue': 2329.95}, {'customer': 'HOUZZ SHOP', 'revenue': 2328.0}, {'customer': '!! Newburyport Lighting', 'revenue': 1980.85}, {'customer': 'Save More Plumbing & Lighting', 'revenue': 1351.2}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 1350.89}, {'customer': 'Connecticut Lighting Center', 'revenue': 1258.2}, {'customer': 'KIE SUPPLY INC', 'revenue': 1223.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 1108.0}, {'customer': 'Hortons of LaGrange', 'revenue': 1092.72}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 1089.7}, {'customer': 'LAMPS PLUS INC', 'revenue': 1063.7}, {'customer': 'Lights Unlimited', 'revenue': 928.2}, {'customer': 'Crescent Lighting Supply Inc (WA)', 'revenue': 873.0}, {'customer': 'PC Building Materials Inc', 'revenue': 873.0}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 868.72}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 803.63}, {'customer': 'Kendall Electric Inc', 'revenue': 733.0}, {'customer': 'Home & Light Valdosta', 'revenue': 684.0}, {'customer': 'The Glow Works, Inc', 'revenue': 674.9}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 673.92}, {'customer': 'Grand Rapids Lighting', 'revenue': 669.0}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 627.0}, {'customer': 'House of Lights (Mayfield Heights)', 'revenue': 608.0}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 583.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 568.7}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 559.68}, {'customer': 'Masterpiece Lighting (GA)', 'revenue': 548.83}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 523.93}, {'customer': 'Canadian Heritage Designs Ltd. DBA CF Interiors', 'revenue': 516.25}, {'customer': 'Elektra Lights & Fans Inc', 'revenue': 504.0}, {'customer': 'Lamps.com, Inc', 'revenue': 503.5}, {'customer': "LOWE'S", 'revenue': 488.23}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 480.0}, {'customer': 'WAI Products LTD DBA Kohara + Co', 'revenue': 479.96}, {'customer': "Seth's Lighting & Assoc. Inc", 'revenue': 456.0}, {'customer': 'American Lighting Inc', 'revenue': 454.0}, {'customer': 'Net Retailers, LLC', 'revenue': 449.18}, {'customer': 'All About Lights Inc', 'revenue': 441.0}, {'customer': 'Crown Electrical Supply', 'revenue': 405.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 379.2}, {'customer': 'Lamps Expo', 'revenue': 358.39}, {'customer': 'Pine Lighting', 'revenue': 346.76}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB)', 'revenue': 344.08}, {'customer': 'Carolina Lanterns (Pelican Equip)', 'revenue': 341.0}, {'customer': 'Lighting by Design LLC (Maryland)', 'revenue': 337.0}, {'customer': 'Lighting Design Company', 'revenue': 332.8}, {'customer': '!! Maison Olive Inc.', 'revenue': 321.83}, {'customer': 'Southern Lights', 'revenue': 317.52}, {'customer': 'The Lighting Shoppe Inc.', 'revenue': 314.11}, {'customer': 'Lighting by Lavonne, LLC', 'revenue': 311.0}, {'customer': 'Homestyles', 'revenue': 304.0}, {'customer': 'Design Lighting Sales', 'revenue': 303.16}, {'customer': 'The Brecher Co, Inc', 'revenue': 303.0}, {'customer': 'J.D. Lighting', 'revenue': 300.96}, {'customer': 'Lighting Reflects Design', 'revenue': 277.2}, {'customer': 'Western Chandelier Co', 'revenue': 275.8}, {'customer': 'Danielhouse Studios, Inc', 'revenue': 274.22}, {'customer': 'Elan Studio Lighting', 'revenue': 265.0}, {'customer': '!! CFSI Interiors Limited DBA Taylor Flooring', 'revenue': 259.6}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 249.8}, {'customer': 'Capital City Design Center', 'revenue': 248.0}, {'customer': 'Lifestyles Store Inc', 'revenue': 236.3}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 228.0}, {'customer': 'Premier Bath, Lighting (MI)', 'revenue': 228.0}, {'customer': 'Lighting Instyle', 'revenue': 228.0}, {'customer': 'LJP Enterprises, Inc. dba Southside Lighting Gallery', 'revenue': 228.0}, {'customer': 'Accent Lighting (KS)', 'revenue': 227.9}, {'customer': 'JW Bird and Company Ltd DBA Bird Stairs', 'revenue': 222.2}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 220.88}, {'customer': 'Cleveland Lighting Center', 'revenue': 215.0}, {'customer': 'Team Electric Supply, LLC', 'revenue': 215.0}, {'customer': 'The Lighting Corner', 'revenue': 202.0}, {'customer': 'St Louis Metro Electric', 'revenue': 202.0}, {'customer': 'The Factory', 'revenue': 194.0}, {'customer': 'Madison Lighting', 'revenue': 189.0}, {'customer': 'Robinson Lighting Ltd (ROB) : B.A. Robinson  (ROB) (BRANDON,', 'revenue': 182.85}, {'customer': 'Chez-Del Interiors', 'revenue': 179.9}, {'customer': 'The Plywood Store, Inc. DBA Burlington Carpet One', 'revenue': 177.8}, {'customer': 'Deco Luminaire Terrebonne', 'revenue': 169.47}, {'customer': 'Multi-Luminaire (Laval)', 'revenue': 167.2}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 167.2}, {'customer': 'Prima Lighting Inc', 'revenue': 157.08}, {'customer': 'ZenSupply Inc', 'revenue': 152.65}, {'customer': 'Litecraft Lighting Inc', 'revenue': 152.0}, {'customer': "Coburn Supply Company dba Coburn's : Spring Hill Lighting db", 'revenue': 152.0}, {'customer': 'Gross Lighting & Home', 'revenue': 152.0}, {'customer': 'William L Hart Designs LLC DBA Hart Designs LLC', 'revenue': 152.0}, {'customer': 'Gross Lighting & Home : Indiana Lighting Center', 'revenue': 152.0}, {'customer': 'Home Front Design', 'revenue': 152.0}, {'customer': 'Radue Homes dba Inspired Spaces', 'revenue': 152.0}, {'customer': '!! Duncan Corporation dba Better Living', 'revenue': 148.0}, {'customer': '!! Premier Industries dba Premier Lighting & Hardware (KC-MO', 'revenue': 133.33}, {'customer': 'Legend Lighting', 'revenue': 126.0}, {'customer': 'Illuminations, Inc. (NE)', 'revenue': 126.0}, {'customer': 'Lighting Plus (MS)', 'revenue': 126.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 126.0}, {'customer': 'Litehouse, Inc dba The Lite House Inc', 'revenue': 126.0}, {'customer': 'Anzalone Electric', 'revenue': 122.0}, {'customer': 'Southern Lighting (Chattanooga)', 'revenue': 122.0}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 122.0}, {'customer': 'Light Brite Distributing Inc.', 'revenue': 122.0}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 118.0}, {'customer': '!! Coastal Lighting Studio (SC)', 'revenue': 109.85}, {'customer': 'Pace Lighting Inc', 'revenue': 108.95}, {'customer': 'LIGHTING BY JARED', 'revenue': 107.86}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 90.1}, {'customer': 'Deco Luminaire Quebec', 'revenue': 83.6}, {'customer': 'Multi-Luminaire Gatineau', 'revenue': 83.6}, {'customer': 'ABC Creations, LLC', 'revenue': 82.5}, {'customer': 'Custom Lighting, Inc', 'revenue': 82.34}, {'customer': 'Just Lights', 'revenue': 81.39}, {'customer': 'Fogg Family Enterprises Inc', 'revenue': 77.95}, {'customer': 'Pine Tree Lighting dba Pine Tree Furniture', 'revenue': 76.0}, {'customer': 'Cregger Co LLC', 'revenue': 76.0}, {'customer': 'Fort Worth Lighting', 'revenue': 76.0}, {'customer': 'Northern Lighting, Inc', 'revenue': 76.0}, {'customer': 'Be the Light Designs LLC', 'revenue': 76.0}, {'customer': 'Dominion Electric Supply Co, a Division of Border States', 'revenue': 76.0}, {'customer': 'Plank and Tile', 'revenue': 76.0}, {'customer': 'Logan Electric Company Inc', 'revenue': 76.0}, {'customer': 'Butler Lighting of High Point', 'revenue': 76.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 76.0}, {'customer': 'Elliott Electric Supply Inc', 'revenue': 73.24}, {'customer': 'Lighting South LLC', 'revenue': 69.3}, {'customer': 'Essence Lighting and Design', 'revenue': 69.3}, {'customer': 'Multi-Luminaire (Pointe Claire)', 'revenue': 69.3}, {'customer': 'Union Lighting (Montreal)', 'revenue': 69.3}, {'customer': 'Universal Lighting Corp (Ont)', 'revenue': 69.3}, {'customer': 'Townsquare Flooring and Design', 'revenue': 68.43}, {'customer': 'Beautiful Things, Inc', 'revenue': 63.34}, {'customer': 'Beals Lighting Gallery', 'revenue': 63.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 63.0}, {'customer': 'VP Supply', 'revenue': 63.0}, {'customer': 'Elite Lighting Innovations', 'revenue': 63.0}, {'customer': 'Wiseway Supply', 'revenue': 63.0}, {'customer': 'P&F Lites Etc, LLC / LITES ETCETERA, INC', 'revenue': 63.0}, {'customer': 'House of Lights of Sanford Inc', 'revenue': 63.0}, {'customer': 'BELAMI ECommerce', 'revenue': 63.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 63.0}, {'customer': 'Lighting Studio (NJ)', 'revenue': 63.0}, {'customer': 'Locke Supply', 'revenue': 63.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 61.0}, {'customer': 'BBC Lighting & Supply', 'revenue': 59.0}, {'customer': "Progressive Lighting, Inc. DBA Caroline's Interiors", 'revenue': 59.0}, {'customer': 'Bright City Lights', 'revenue': 59.0}, {'customer': 'Lighting EFX', 'revenue': 59.0}, {'customer': 'Ocean Pacific Lighting Inc', 'revenue': 58.91}, {'customer': 'Sunbelt / Louisiana', 'revenue': 56.7}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 51.66}, {'customer': 'Idlewood Electric Supply', 'revenue': 50.4}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 49.4}, {'customer': 'McLaren Electric', 'revenue': 38.72}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 37.76}, {'customer': 'Sonepar dba Capital Electric : Sonepar dba QED Galleria Ligh', 'revenue': 19.18}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 8.5}, {'customer': 'Lightology', 'revenue': 0.0}, {'customer': 'Paramont- EO, Inc', 'revenue': -21.2}, {'customer': 'House of Carpets', 'revenue': -21.9}, {'customer': 'Chateau Lighting', 'revenue': -86.46}, {'customer': '!! Proper Goods Inc', 'revenue': -90.99}, {'customer': 'Galleria Lighting Inc.', 'revenue': -323.3}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': -716.1}, {'customer': 'City Lightz', 'revenue': -1247.4}] | [{'item': 'M60004NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 417}, {'item': 'M60054NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 292}, {'item': 'M60054MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 228}, {'item': 'M60011MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 208}, {'item': 'M60017ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 198}, {'item': 'M60068ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 194}, {'item': 'M60010ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 190}, {'item': 'M60017NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 185}, {'item': 'M60061MBK', 'desc': '4-Light Ceiling Light in Matte Black', 'available': 184}, {'item': 'M60074NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 183}, {'item': 'M60068PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 175}, {'item': 'M60056BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 173}, {'item': 'M60068NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 170}, {'item': 'M60074MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 165}, {'item': 'M60011ORBNB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze with Natural Brass', 'available': 164}, {'item': 'M60069ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 164}, {'item': 'M60055ORB', 'desc': '3-Light Convertible Semi-Flush or Pendant in Oil Rubbed Bronze', 'available': 164}, {'item': 'M60016MBK', 'desc': '2-Light Ceiling Light in Matte Black', 'available': 157}, {'item': 'M60056NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 155}, {'item': 'M60015NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 139}, {'item': 'M60070ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 123}, {'item': 'M60071MBKNB', 'desc': '1-Light Ceiling Light in Matte Black with Natural Brass', 'available': 121}, {'item': 'M60061NB', 'desc': '4-Light Ceiling Light in Natural Brass', 'available': 120}, {'item': 'M60018NB', 'desc': '3-Light Ceiling Light in Natural Brass', 'available': 118}, {'item': 'M60055NB', 'desc': '3-Light Convertible Semi-Flush or Pendant in Natural Brass', 'available': 117}, {'item': 'M60028DW', 'desc': '2-Light Ceiling Light in Distressed Wood', 'available': 115}, {'item': 'M60008ORB', 'desc': '2-Light Ceiling Light in Oil Rubbed Bronze', 'available': 113}, {'item': 'M60017PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 110}, {'item': 'M60061BN', 'desc': '4-Light Ceiling Light in Brushed Nickel', 'available': 104}, {'item': 'M60069NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 104}, {'item': 'M60017MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 91}, {'item': 'M60076NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 88}, {'item': 'M60061PN', 'desc': '4-Light Ceiling Light in Polished Nickel', 'available': 88}, {'item': 'M60080NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 87}, {'item': 'M60077MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 82}, {'item': 'M60064PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 80}, {'item': 'M60016NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 80}, {'item': 'M60011BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 80}, {'item': 'M60076MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 76}, {'item': 'M60016ORB', 'desc': '2-Light Ceiling Light in Oil Rubbed Bronze', 'available': 76}, {'item': 'M60070PN', 'desc': '1-Light Ceiling Light in Polished Nickel', 'available': 76}, {'item': 'M60017BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 68}, {'item': 'M60010NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 65}, {'item': 'M60021NB', 'desc': '2-Light Ceiling Light in Natural Brass', 'available': 64}, {'item': 'M60078MBKNB', 'desc': '1-Light Ceiling Light in Matte Black and Natural Brass', 'available': 63}, {'item': 'M60055PN', 'desc': '3-Light Convertible Semi-Flush or Pendant in Polished Nickel', 'available': 63}, {'item': 'M60008MBK', 'desc': '2-Light Ceiling Light in Matte Black', 'available': 61}, {'item': 'M60038OG', 'desc': '3-Light Ceiling Light in Antique Gold', 'available': 57}, {'item': 'M60079MBKNB', 'desc': '3-Light Ceiling Light in Matte Black with Natural Brass', 'available': 57}, {'item': 'M60071NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 56}, {'item': 'M60076BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 54}, {'item': 'M60077NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 50}, {'item': 'M60077BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 50}, {'item': 'M60010MBK', 'desc': '1-Light Ceiling Light in Matte Black', 'available': 48}, {'item': 'M60056ORB', 'desc': '1-Light Ceiling Light in Oil Rubbed Bronze', 'available': 42}, {'item': 'M60072MBKNB', 'desc': '3-Light Ceiling Light in Matte Black and Natural Brass', 'available': 37}, {'item': 'M60011NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 37}, {'item': 'M60008BN', 'desc': '2-Light Ceiling Light in Brushed Nickel', 'available': 36}, {'item': 'M60010BN', 'desc': '1-Light Ceiling Light in Brushed Nickel', 'available': 32}, {'item': 'M60020NB', 'desc': '3-Light Ceiling Light in Natural Brass', 'available': 31}, {'item': 'M60054CH', 'desc': '1-Light Ceiling Light in Chrome', 'available': 28}, {'item': 'M60020CBZ', 'desc': '3-Light Ceiling Light in Classic Bronze', 'available': 28}, {'item': 'M60055MBK', 'desc': '3-Light Convertible Semi-Flush or Pendant in Matte Black', 'available': 26}, {'item': 'M60015PN', 'desc': '2-Light Ceiling Light in Polished Nickel', 'available': 22}, {'item': 'M60078WHNB', 'desc': '1-Light Ceiling Light in White and Natural Brass', 'available': 21}, {'item': 'M60015ORB', 'desc': '2-Light Ceiling Light in Oil Rubbed Bronze', 'available': 15}, {'item': 'M60070NB', 'desc': '1-Light Ceiling Light in Natural Brass', 'available': 14}, {'item': 'M60072WHNB', 'desc': '3-Light Ceiling Light in White and Natural Brass', 'available': 10}, {'item': 'M60002-97', 'desc': '3-Light Ceiling Light in Natural Wood with Rope', 'available': 8}] |
| 9-7144-1-322 | Monroe 1-Light Wall Sconce in Warm Brass | MONRO | 162,680.72 | 2,784 | — | 2026-06-27 | [{'customer': 'WAYFAIR LLC', 'revenue': 79500.33}, {'customer': 'LAMPS PLUS INC', 'revenue': 6747.17}, {'customer': 'BUILD.COM', 'revenue': 5788.63}, {'customer': 'FERGUSON', 'revenue': 5171.54}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 4955.5}, {'customer': 'The Home Depot', 'revenue': 4659.83}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 4186.5}, {'customer': 'Shades of Light', 'revenue': 3851.0}, {'customer': 'Inline Electric Supply', 'revenue': 3030.0}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 1868.3}, {'customer': 'Lighting World', 'revenue': 1775.73}, {'customer': 'Multi-Luminaire Gatineau : Multi-Luminaire (Ottawa)', 'revenue': 1754.5}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 1613.65}, {'customer': 'Mechanical-Electrical-Whole', 'revenue': 1430.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 1374.64}, {'customer': 'Aggieland Lighting', 'revenue': 1281.75}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 1248.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': 1201.76}, {'customer': 'Lamps.com, Inc', 'revenue': 1170.47}, {'customer': 'LIGHTING BY JARED', 'revenue': 1168.84}, {'customer': 'DULLES ELECTRIC AND SUPPLY', 'revenue': 1098.73}, {'customer': 'Del Mar Designs dba Del Mar Fans & Lighting', 'revenue': 1083.03}, {'customer': 'BELAMI ECommerce', 'revenue': 981.79}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': 816.0}, {'customer': 'Lighting Design Company', 'revenue': 785.7}, {'customer': 'American Lighting Inc', 'revenue': 770.0}, {'customer': 'Sunbelt / Louisiana', 'revenue': 714.4}, {'customer': 'Lightology', 'revenue': 707.44}, {'customer': 'Lifestyles Store Inc', 'revenue': 707.27}, {'customer': 'Lighting Superstore', 'revenue': 702.93}, {'customer': 'The Home Depot : Home Depot - Canada', 'revenue': 659.5}, {'customer': 'Fusion Light and Design', 'revenue': 587.5}, {'customer': 'Rite Rug DBA Capital Lighting', 'revenue': 552.0}, {'customer': 'Lampworks dba Lamp & Shadework', 'revenue': 552.0}, {'customer': 'Lighting Incorporated', 'revenue': 550.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED DBA: Notoco Indus', 'revenue': 542.0}, {'customer': 'Cape Electrical Supply', 'revenue': 540.96}, {'customer': 'Capitol Lighting Gallery', 'revenue': 536.0}, {'customer': 'Gateway Lighting & Design Inc', 'revenue': 472.61}, {'customer': 'Menards, Inc', 'revenue': 471.2}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 440.0}, {'customer': 'Sonepar dba Capital Electric : Echo Electric Supply dba Echo', 'revenue': 440.0}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 440.0}, {'customer': "Hinkley's Lighting Factory", 'revenue': 420.2}, {'customer': 'The Lighting Studio of 30A (Santa Rosa Beach)', 'revenue': 419.8}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 404.8}, {'customer': 'Union Lighting & Furnishings (Toronto)', 'revenue': 397.71}, {'customer': 'Wilson 6 Enterprises Inc. DBA: Mountain Lighting & Design', 'revenue': 396.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 385.6}, {'customer': 'Wiseway Supply', 'revenue': 385.0}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 385.0}, {'customer': 'Elaine Everetts Lighting', 'revenue': 368.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 368.0}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 339.68}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (PARAMUS)', 'revenue': 303.0}, {'customer': 'The Light Source', 'revenue': 276.0}, {'customer': 'City Lights (San Francisco)', 'revenue': 276.0}, {'customer': 'Lights Unlimited', 'revenue': 264.0}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 261.0}, {'customer': 'King Electric Company Inc', 'revenue': 244.7}, {'customer': 'Valley Supply Co', 'revenue': 237.89}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 231.0}, {'customer': 'Flinz Holdings LLC', 'revenue': 230.0}, {'customer': 'Illuminations, Inc. (NE)', 'revenue': 220.0}, {'customer': 'Sonepar dba Capital Electric', 'revenue': 220.0}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': 220.0}, {'customer': 'Coley Electric & Plumbing (Douglas)', 'revenue': 220.0}, {'customer': 'Central Plumbing & Electric', 'revenue': 220.0}, {'customer': 'James Ashjian Lighting', 'revenue': 220.0}, {'customer': 'Muska Lighting', 'revenue': 220.0}, {'customer': 'Chester Lighting', 'revenue': 220.0}, {'customer': 'Sweet Home Design Company', 'revenue': 220.0}, {'customer': 'IBS Lighting LLC', 'revenue': 220.0}, {'customer': 'Kansas Lighting', 'revenue': 220.0}, {'customer': 'Front Street Lighting', 'revenue': 206.4}, {'customer': 'Hye Lighting Co', 'revenue': 198.0}, {'customer': 'Guildwood', 'revenue': 191.4}, {'customer': 'Union Lighting (Montreal)', 'revenue': 191.4}, {'customer': 'J.D. Lighting', 'revenue': 191.4}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 184.0}, {'customer': 'SOUTHWEST PLUMBING SUPPLY', 'revenue': 184.0}, {'customer': 'Kendall Electric Inc', 'revenue': 184.0}, {'customer': 'Hill Country Lighting Center', 'revenue': 184.0}, {'customer': 'Lights of Oconee', 'revenue': 184.0}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': 184.0}, {'customer': 'Drew Designs, LLC dba Western Montana Lighting', 'revenue': 184.0}, {'customer': 'LIGHT SOURCE LIGHTING [EDI] dba Styles of Lighting', 'revenue': 176.64}, {'customer': 'First Coast Lighting & Fans', 'revenue': 174.0}, {'customer': 'United Electric Supply (NE)', 'revenue': 174.0}, {'customer': 'Illuminate Lighting', 'revenue': 174.0}, {'customer': 'Beautiful Things, Inc', 'revenue': 170.4}, {'customer': 'Southern Lighting Gallery (Augusta)', 'revenue': 156.4}, {'customer': 'Idlewood Electric Supply', 'revenue': 154.0}, {'customer': 'Pace Lighting Inc', 'revenue': 146.45}, {'customer': '!! Lando Lighting', 'revenue': 145.2}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': 139.82}, {'customer': '!! Source & Co.', 'revenue': 139.52}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM : CAPITOL LIGHTING (STUART)', 'revenue': 138.0}, {'customer': 'Home & Light Valdosta', 'revenue': 123.3}, {'customer': 'Southern Electric & Plumbing Supply', 'revenue': 122.11}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 101.2}, {'customer': "Coburn Supply Company dba Coburn's", 'revenue': 92.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 87.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 87.0}, {'customer': 'Beals Lighting Gallery', 'revenue': 74.5}, {'customer': 'The Brecher Co, Inc', 'revenue': 36.9}, {'customer': "LOWE'S", 'revenue': 0.0}, {'customer': 'Electric Outlet (LIGHTING BY FRAN)', 'revenue': 0.0}, {'customer': 'Small Town Home Decor LLC', 'revenue': 0.0}, {'customer': 'Mahlanders, Inc', 'revenue': 0.0}, {'customer': 'Dement Lighting', 'revenue': 0.0}, {'customer': 'Western Chandelier Co', 'revenue': -69.9}, {'customer': 'Stokes Electric Company', 'revenue': -71.0}] | [{'item': '9-302-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 144}, {'item': '9-303-1-89', 'desc': 'Monroe 1-Light Wall Sconce in Matte Black', 'available': 139}, {'item': '9-7144-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 119}, {'item': '9-303-1-SN', 'desc': 'Monroe 1-Light Wall Sconce in Satin Nickel', 'available': 92}, {'item': '9-7144-1-44', 'desc': 'Monroe 1-Light Wall Sconce in Classic Bronze', 'available': 64}, {'item': '9-7144-1-109', 'desc': 'Monroe 1-Light Wall Sconce in Polished Nickel', 'available': 61}] |
| 7-2918-1-156 | Alta 1-Light Pendant in Concrete and Brass | ALTA | 147,450.18 | 537 | — | 2026-06-27 | [{'customer': 'FERGUSON', 'revenue': 12341.14}, {'customer': 'LUMENS LIGHT & LIVING (Y DESIGN)', 'revenue': 8575.49}, {'customer': 'CAPITOL LTG 1800LIGHTING.COM', 'revenue': 8444.25}, {'customer': "Graham's Lighting Inc (Franklin)", 'revenue': 7733.0}, {'customer': 'BUILD.COM', 'revenue': 7081.8}, {'customer': 'Nova Lighting fka Hansen Lighting', 'revenue': 5456.19}, {'customer': 'Lighting Design Company', 'revenue': 4511.3}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry', 'revenue': 3939.76}, {'customer': 'WAYFAIR LLC', 'revenue': 3824.25}, {'customer': 'LIGHTOPIA  LLC', 'revenue': 3589.69}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 3198.61}, {'customer': 'Nebraska Furniture Mart, Inc', 'revenue': 3174.1}, {'customer': 'Pine Grove Electric Supply Co', 'revenue': 2739.9}, {'customer': 'Dhillon Lighting (Calgary - Gurpreet)', 'revenue': 2606.45}, {'customer': 'Lighting Incorporated', 'revenue': 2387.5}, {'customer': '!! The Lifestyled Company LLC', 'revenue': 2360.73}, {'customer': 'Lyteout dba Lightstyle of Orlando', 'revenue': 2321.4}, {'customer': 'LIGHTING BY JARED', 'revenue': 2262.92}, {'customer': 'Fort Worth Lighting', 'revenue': 2224.6}, {'customer': 'Inline Electric Supply', 'revenue': 2000.5}, {'customer': "Wilkinson's House of Lighting", 'revenue': 1855.9}, {'customer': 'Lighting World', 'revenue': 1790.82}, {'customer': 'Small Town Home Decor LLC', 'revenue': 1718.0}, {'customer': 'Sunbelt / Louisiana', 'revenue': 1694.6}, {'customer': 'Lumen Nation LLC', 'revenue': 1628.0}, {'customer': 'Lifestyles Store Inc', 'revenue': 1536.18}, {'customer': '!! Gagnun Interior Concept Studio Inc DBA Boutique Intempore', 'revenue': 1471.91}, {'customer': 'The Lighting Corner', 'revenue': 1447.0}, {'customer': 'Hagens Lighting', 'revenue': 1390.5}, {'customer': 'The Brecher Co, Inc', 'revenue': 1281.3}, {'customer': 'Illuminations', 'revenue': 1254.7}, {'customer': 'Lightology', 'revenue': 1204.72}, {'customer': 'Passion Lighting DBA Cannon & Crossbow', 'revenue': 1186.5}, {'customer': 'Hall Electric Co Inc', 'revenue': 1153.0}, {'customer': 'Village 1, LLC dba Village Home Stores', 'revenue': 1153.0}, {'customer': 'Union Lighting (Montreal)', 'revenue': 1119.25}, {'customer': "Garbe's Lighting & Hardware LLC", 'revenue': 1085.0}, {'customer': 'BELAMI ECommerce', 'revenue': 1059.37}, {'customer': 'Colonial Lighting LLC dba Georgia Lighting', 'revenue': 983.5}, {'customer': 'LAMPS PLUS INC', 'revenue': 977.29}, {'customer': 'Park Lighting and Furniture Ltd dba Cartwright Lighting & Fu', 'revenue': 973.67}, {'customer': 'Carrington Lighting dba Can-Kor', 'revenue': 917.4}, {'customer': 'Muskoka Lighting & Electric', 'revenue': 895.4}, {'customer': 'Urban Rustic Living', 'revenue': 895.4}, {'customer': 'Team Electric Supply, LLC', 'revenue': 847.5}, {'customer': 'Lowcountry Lighting Studio LLC', 'revenue': 814.0}, {'customer': 'Plumbing Distributors Inc dba PDI', 'revenue': 814.0}, {'customer': 'WASATCH LIGHTING INC', 'revenue': 814.0}, {'customer': 'Uncommon Living fka Lighting Unlimited (MS)', 'revenue': 814.0}, {'customer': 'ALLOWAY LIGHTING, LLC', 'revenue': 814.0}, {'customer': 'LIGHTSHINE INC DBA URBAN LIGHTS', 'revenue': 814.0}, {'customer': 'Bright Side Ptnrs dba Tallahassee Lighting', 'revenue': 814.0}, {'customer': 'Kendall Electric Inc', 'revenue': 814.0}, {'customer': 'Aggieland Lighting', 'revenue': 802.25}, {'customer': 'The Light House Gallery (MO)', 'revenue': 773.3}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 746.0}, {'customer': 'Gorman Brothers Appliance', 'revenue': 746.0}, {'customer': '!! Simply Floors and Lights dba Fielden Ventures LLC', 'revenue': 745.8}, {'customer': 'Janbar Electric Ltd', 'revenue': 745.8}, {'customer': 'Muska Lighting', 'revenue': 678.0}, {'customer': 'Home & Light Valdosta', 'revenue': 678.0}, {'customer': 'The Finishing Touch', 'revenue': 678.0}, {'customer': 'Magnolia Lighting, Inc', 'revenue': 678.0}, {'customer': 'Elan Studio Lighting', 'revenue': 678.0}, {'customer': 'Hudson Parc Lighting & Design', 'revenue': 634.13}, {'customer': 'Robinson Lighting Ltd (ROB) : Norburn Lighting & Bath Centre', 'revenue': 621.61}, {'customer': 'Wiseway Supply', 'revenue': 576.5}, {'customer': 'TURN ON LIGHTING, INC.', 'revenue': 576.5}, {'customer': 'Royaume Luminaire', 'revenue': 563.2}, {'customer': 'J.D. Lighting', 'revenue': 447.7}, {'customer': 'Dhillon Lighting Inc (Edmonton) : Dhillon Lighting Manitoba', 'revenue': 447.7}, {'customer': 'JW Bird and Company Ltd DBA Bird Stairs', 'revenue': 447.7}, {'customer': '!! Lando Lighting', 'revenue': 447.7}, {'customer': '17-90 Lighting dba Illuminate Maine', 'revenue': 407.0}, {'customer': 'Winsupply Elizabethtown : Winsupply Owensboro KY', 'revenue': 407.0}, {'customer': 'BIGGINS LIGHTING', 'revenue': 407.0}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba All Phase Tra', 'revenue': 407.0}, {'customer': 'Sun Lighting (Tempe)', 'revenue': 407.0}, {'customer': 'Lighting South LLC', 'revenue': 407.0}, {'customer': 'IMAGINE MORE SERVICE CORP.', 'revenue': 407.0}, {'customer': 'IBS Lighting LLC', 'revenue': 407.0}, {'customer': "Graham's Lighting Fixtures Inc (Memphis)", 'revenue': 407.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 407.0}, {'customer': 'Fusion Light and Design', 'revenue': 407.0}, {'customer': 'Cleveland Lighting Center', 'revenue': 407.0}, {'customer': 'Lighting EFX', 'revenue': 378.51}, {'customer': 'Dement Lighting', 'revenue': 376.6}, {'customer': 'Maple Ridge Lighting Inc', 'revenue': 372.9}, {'customer': 'Essence Lighting and Design', 'revenue': 372.9}, {'customer': 'Idlewood Electric Supply', 'revenue': 366.3}, {'customer': 'First Coast Lighting & Fans', 'revenue': 366.3}, {'customer': 'Dolan NW / Seattle / Globe', 'revenue': 345.95}, {'customer': 'Hill Country Lighting Center', 'revenue': 339.0}, {'customer': 'Showcase Lighting by 3-G LTD (TX)', 'revenue': 339.0}, {'customer': 'Lights of Oconee', 'revenue': 339.0}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA) : Hajoca d', 'revenue': 339.0}, {'customer': 'LBU Lighting DBA Boca Bulb Inc : LBU Lighting DBA Central Bu', 'revenue': 339.0}, {'customer': 'N S Electric Supply', 'revenue': 339.0}, {'customer': 'Royaume Luminaire Sherbrooke', 'revenue': 326.7}, {'customer': 'Lighting Reflects Design', 'revenue': 309.24}, {'customer': 'The Home Depot', 'revenue': 297.8}, {'customer': 'Deco Luminaire Brossard Dix 30', 'revenue': 261.25}, {'customer': 'Pine Lighting', 'revenue': 255.42}, {'customer': 'Young & Co', 'revenue': 254.25}, {'customer': 'Lighting World : Lighting World - FBA', 'revenue': 244.24}, {'customer': 'Nestie Inc. fka Grand Lighting (CAN)', 'revenue': 223.85}, {'customer': 'Luminous Trends Inc DBA Modern Luxury by LT', 'revenue': 203.5}, {'customer': 'Royaume Luminaire-J.D. Inc', 'revenue': 186.45}, {'customer': 'Plank and Tile', 'revenue': 169.5}, {'customer': 'CED dba Consolidated Electrical Dist : CED dba All Phase Pet', 'revenue': 169.5}, {'customer': 'KIE SUPPLY INC', 'revenue': 169.5}, {'customer': 'Lighting World Inc (Omaha)', 'revenue': 166.2}, {'customer': 'Mainland Lighting Warehouse', 'revenue': 140.8}, {'customer': 'James Ashjian Lighting', 'revenue': 135.6}, {'customer': 'Montreal Lighting & Hardware', 'revenue': 124.79}, {'customer': 'Sweet Home Design Company', 'revenue': 83.4}, {'customer': 'The Lamp and Lighthouse (TN)', 'revenue': 50.99}, {'customer': "Hinkley's Lighting Factory", 'revenue': 30.45}, {'customer': 'Nova Lighting fka Hansen Lighting : LIGHTING SPECIALISTS', 'revenue': 0.0}, {'customer': 'Net Retailers, LLC', 'revenue': 0.0}, {'customer': 'SOUTHWEST PLUMBING SUPPLY', 'revenue': 0.0}, {'customer': 'Feldman Brothers Electrical Supply Co.', 'revenue': 0.0}, {'customer': 'Southern Lights', 'revenue': 0.0}, {'customer': 'Wilson Lighting of Naples Inc : R. Wilson Lighting Company I', 'revenue': 0.0}, {'customer': 'Winsupply Elizabethtown : Winsupply dba Bowling Green WLC 14', 'revenue': 0.0}, {'customer': 'Lighting Emporium Inc', 'revenue': 0.0}, {'customer': "LOWE'S", 'revenue': 0.0}, {'customer': 'The Electric Connection ( TEC Electric)', 'revenue': 0.0}, {'customer': '2641426 Ont Inc dba Lighthouse Cabinetry : Lighthouse Cabine', 'revenue': 0.0}, {'customer': 'U.S.31 Supply Inc', 'revenue': 0.0}, {'customer': 'Haus Appeal dba Bliss Modern', 'revenue': -81.4}, {'customer': 'BELAMI ECommerce : BELAMI CANADA', 'revenue': -120.07}, {'customer': 'Lighting by Lavonne, LLC', 'revenue': -165.0}, {'customer': 'Lumenco Inc (CIMPEXCO)', 'revenue': -179.08}, {'customer': 'Rexel USA, Inc. : Rexel USA, Inc. dba Mayer Electric', 'revenue': -210.0}, {'customer': 'Multi-Luminaire Gatineau', 'revenue': -223.3}, {'customer': 'Illuminate Lighting', 'revenue': -324.5}, {'customer': 'Sunbelt / Louisiana : Sunbelt / Mississippi', 'revenue': -366.4}, {'customer': 'The Broadway Showroom dba Bliss Lighting', 'revenue': -423.0}, {'customer': 'Mahlanders, Inc', 'revenue': -488.64}, {'customer': 'The Salt Box Lighting Inc.', 'revenue': -544.5}, {'customer': 'The Focal Point SWLA LLC', 'revenue': -623.5}, {'customer': 'Lights Unlimited', 'revenue': -716.4}, {'customer': 'Hajoca dba The Plumbing Warehouse (Lafayette, LA)', 'revenue': -1265.5}, {'customer': 'The Lighting Shoppe Inc.', 'revenue': -1636.8}] | — |
