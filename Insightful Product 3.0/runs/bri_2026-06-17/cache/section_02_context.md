# Section 2 Context Bundle — Bulbrite (bri)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Bulbrite (bri, org_id=222)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=117632, portal_order_gmv=$19.0M |
| HAS_INVENTORY | True | inventory_count=895 |
| HAS_SALES_DATA | True | sales_data_count=45296 |
| HAS_SALES_SECTION | True | qualifying_reps=5 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | N/A |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$19.0M > ecat_gmv=$3.5M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 5 | 5 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 107 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3137, Mixpanel total submit_order (Q-01): 435 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.2%, ambiguous_rate=1.0%, showroom_event_share=2.0% |
| USER_GROUP_JOIN_RATE | 97% | 104 of 107 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 2% | showroom+admin share of matched events: 2.0% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1309 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=179 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Bulbrite
- **Shortname**: bri
- **Org ID**: 222
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Bulbrite (bri, org_id=222)
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

# Signal Rank — Bulbrite (bri, org_id=222)
- **Run date**: 2026-06-17
- **Total signals fired**: 48 (P0: 38, P1: 10, P2: 0)
- **Org GMV**: $3.5M eCat LTM, $19.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $5.4M+ total business, zero eCat orders | P1 | §2 Accounts | 5.4 | $5,411,901 | 2.0 | 58,577,345 | POSITIVE |
| 2 | SIG-ANOMALY-02 | Stock Out — 773166 (LED14REC/5/6/930/WHRD/D) $792,072 LTM, 0 available | P0 | §3 Product | 10.0 | $792,072 | 3.0 | 23,762,164 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 774239 (LED9A19/P60W/930/J/D/1P) $254,415 LTM, 0 available | P0 | §3 Product | 10.0 | $254,415 | 3.0 | 7,632,456 | RISK |
| 4 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 70% of eCat GMV | P1 | §4 Commerce | 1.8 | $1,380,801 | 2.0 | 4,844,634 | RISK |
| 5 | SIG-DECAY-04 | Spending Contraction — LUMENS LIGHT & LIVING *** -52.7% YoY ($841,148→$397,623), $443,525 gap | P0 | §2 Accounts | 2.6 | $443,525 | 3.0 | 3,506,064 | RISK |
| 6 | SIG-DECAY-04 | Spending Contraction — PROGRESSIVE -71.3% YoY ($394,531→$113,256), $281,274 gap | P0 | §2 Accounts | 3.6 | $281,274 | 3.0 | 3,008,231 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 136019 (NOS60-1910) $79,784 LTM, 0 available | P0 | §3 Product | 10.0 | $79,784 | 3.0 | 2,393,506 | RISK |
| 8 | SIG-COMMERCE-01 | Capture Rate — eCat captures 18.4% of $19M total business; each +1pt = $190K | P0 | §4 Commerce | 4.1 | $190,000 | 3.0 | 2,325,000 | POSITIVE |
| 9 | SIG-ANOMALY-02 | Stock Out — 776724 (LED4T8/30K/FIL/3) $74,388 LTM, 0 available | P0 | §3 Product | 10.0 | $74,388 | 3.0 | 2,231,643 | RISK |
| 10 | SIG-MOM-01 | Account Acceleration — CAPITOL LIGHTING - NJ location 2 consecutive QoQ acceleration quarters, $81,900 peak quarter (+229% QoQ) | P0 | §2 Accounts | 7.6 | $81,900 | 3.0 | 1,872,227 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — 712160 (60A19HM) $61,566 LTM, 0 available | P0 | §3 Product | 10.0 | $61,566 | 3.0 | 1,846,975 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 776869 (LED8A19/30K/FIL/M/3) $60,846 LTM, 0 available | P0 | §3 Product | 10.0 | $60,846 | 3.0 | 1,825,385 | RISK |
| 13 | SIG-MOM-01 | Account Acceleration — SHADES OF LIGHT 3 consecutive QoQ acceleration quarters, $65,471 peak quarter (+134% QoQ) | P0 | §2 Accounts | 4.5 | $65,471 | 3.0 | 875,342 | POSITIVE |
| 14 | SIG-DECAY-04 | Spending Contraction — M & M LIGHTING-HOUSTON ** -44.9% YoY ($263,767→$145,327), $118,440 gap | P0 | §2 Accounts | 2.2 | $118,440 | 3.0 | 797,691 | RISK |
| 15 | SIG-DECAY-04 | Spending Contraction — WAYFAIR, LLC -CASTLEGATE -31.6% YoY ($524,671→$358,953), $165,717 gap | P0 | §2 Accounts | 1.6 | $165,717 | 3.0 | 785,501 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — PROJECT LIGHTING CO INC/CED *** 2 consecutive QoQ acceleration quarters, $45,282 peak quarter (+164% QoQ) | P0 | §2 Accounts | 5.5 | $45,282 | 3.0 | 743,525 | POSITIVE |
| 17 | SIG-MOM-01 | Account Acceleration — CED - National Accounts 3 consecutive QoQ acceleration quarters, $19,621 peak quarter (+321% QoQ) | P0 | §2 Accounts | 10.7 | $19,621 | 3.0 | 629,644 | POSITIVE |
| 18 | SIG-MOM-01 | Account Acceleration — STEWART LIGHTING 2 consecutive QoQ acceleration quarters, $25,398 peak quarter (+235% QoQ) | P0 | §2 Accounts | 7.8 | $25,398 | 3.0 | 597,876 | POSITIVE |
| 19 | SIG-DECAY-04 | Spending Contraction — LIGHTING DESIGN LLC -27.4% YoY ($480,966→$349,365), $131,601 gap | P0 | §2 Accounts | 1.4 | $131,601 | 3.0 | 540,881 | RISK |
| 20 | SIG-MOM-01 | Account Acceleration — LOWES COMPANY, INC. 2 consecutive QoQ acceleration quarters, $68,616 peak quarter (+72% QoQ) | P0 | §2 Accounts | 2.4 | $68,616 | 3.0 | 494,037 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 31 | 1 | 0 | 32 | |
| §3 Product Intelligence | 6 | 0 | 0 | 6 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 8 | 0 | 8 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $5.4M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 18.4% of $19M total business; each +1pt = $190K
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — CAPITOL LIGHTING - NJ location 2 consecutive QoQ acceleration quarters, $81,900 peak quarter (+229% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — SHADES OF LIGHT 3 consecutive QoQ acceleration quarters, $65,471 peak quarter (+134% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 773166 (LED14REC/5/6/930/WHRD/D) $792,072 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 774239 (LED9A19/P60W/930/J/D/1P) $254,415 LTM, 0 available
7. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 70% of eCat GMV

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Bulbrite (bri, org_id=222)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | SHADES OF LIGHT | 2 | DECAY-04, MOM-01 | $65,471 |
| 2 | JAMES & COMPANY LIGHTING | 2 | DECAY-04, MOM-01 | $38,048 |
| 3 | LUMENS LIGHT & LIVING *** | 1 | DECAY-04 | $443,525 |
| 4 | PROGRESSIVE | 1 | DECAY-04 | $281,274 |
| 5 | WAYFAIR, LLC -CASTLEGATE | 1 | DECAY-04 | $165,717 |
| 6 | LIGHTING DESIGN LLC | 1 | DECAY-04 | $131,601 |
| 7 | M & M LIGHTING-HOUSTON ** | 1 | DECAY-04 | $118,440 |
| 8 | WAYFAIR, LLC *** | 1 | DECAY-04 | $77,182 |
| 9 | Low Country Lighting Inc | 1 | DECAY-04 | $71,842 |
| 10 | COFFMAN HOME DECOR | 1 | DECAY-04 | $67,329 |

### Q-12_results.md

# Q-12 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 3,226 | 430 | 334 | 261 | 211 |

### Q-14_results.md

# Q-14 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 025958 | BULBS.COM | 295 | $476,032 | 2025-06-17 14:54:20 | 2026-06-16 16:33:38 | 1.20 |
| 125750 | LIGHTING GETZ CORP. *** | 118 | $11,272 | 2025-06-18 15:19:34 | 2026-03-09 15:55:57 | 2.30 |
| 056100 | EXWAY ELECTRIC SUPPLY CO | 84 | $81,510 | 2025-09-30 21:23:41 | 2026-06-16 20:47:58 | 3.10 |
| 064505 | Francis King | 68 | $4,081 | 2025-06-17 18:25:20 | 2026-06-04 20:11:52 | 5.30 |
| 027000 | JUST BULBS THE LIGHT BULB STORE | 55 | $28,464 | 2025-06-30 18:02:25 | 2026-06-16 20:18:40 | 6.50 |
| 160655 | Parallax Industries Inc. dba Square Deal Shop | 48 | $602,055 | 2025-07-01 16:00:42 | 2026-06-03 17:14:08 | 7.20 |
| 073090 | GRAND BRASS LAMP PARTS INC | 45 | $48,003 | 2025-06-18 12:02:19 | 2026-06-11 17:33:39 | 8.10 |
| 130645 | MADISON LIGHTING | 44 | $55,551 | 2025-06-18 15:50:35 | 2026-06-10 16:22:47 | 8.30 |
| 121155 | KLS LLC dba SPECTRUM LIGHTING ** | 41 | $47,629 | 2025-06-24 12:15:35 | 2026-03-09 12:54:39 | 6.50 |
| 127320 | Lumber One Home Center - Little Rock Inc | 40 | $90,182 | 2025-06-20 20:54:22 | 2026-06-09 17:01:41 | 9.10 |
| 090206 | Illuminating Design LLC | 40 | $2,665 | 2025-06-24 19:19:42 | 2026-01-02 17:05:00 | 4.90 |
| 194927 | SOUTHERN LIGHTS, INC. ** | 40 | $62,498 | 2025-06-20 15:42:00 | 2026-03-05 21:54:56 | 6.60 |
| 025160 | BRIGHT IDEAS | 38 | $55,484 | 2025-06-18 14:36:55 | 2026-06-10 15:17:01 | 9.60 |
| 130800 | FOGG LIGHTING | 38 | $10,572 | 2025-06-19 19:32:57 | 2026-06-12 17:46:14 | 9.70 |
| 080980 | HARRY HORN INC | 37 | $6,960 | 2025-06-24 16:31:12 | 2026-06-04 14:15:26 | 9.60 |
| 233295 | WILSON LIGHTING OF NAPLES | 36 | $36,823 | 2025-06-27 15:08:34 | 2026-05-28 19:00:49 | 9.60 |
| 085025 | HUNZICKER BROS** | 35 | $55,269 | 2025-06-17 18:59:45 | 2026-03-02 19:16:06 | 7.60 |
| 073080 | GRAHAM'S LIGHTING FIXTURES, INC. | 32 | $46,735 | 2025-06-20 18:16:52 | 2026-04-24 21:20:57 | 9.90 |
| 011908 | ACCENT LIGHTING INC | 31 | $2,335 | 2025-06-18 16:11:19 | 2026-06-10 16:20:37 | 11.90 |
| 090395 | ILLUMINATIONS | 31 | $94,560 | 2025-06-20 04:09:10 | 2026-06-03 22:07:38 | 11.60 |

### Q-14b_results.md

# Q-14b Results — Bulbrite (bri, org_id=222)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 163820 | PROGRESSIVE | 123 | 3.90 | 5.90 | 1.51 | $113,256 |
| 024508 | BRAND NAME LIGHTING | 94 | 4.30 | 14.60 | 3.40 | $107,488 |
| 233295 | WILSON LIGHTING OF NAPLES | 64 | 6.70 | 13.80 | 2.06 | $70,184 |
| 016970 | 1800LIGHTING.COM ** | 2,231 | 0.20 | 0.30 | 1.50 | $65,329 |
| 061942 | FERGUSON-TX 1563,66,64,2751,2812 | 81 | 4.70 | 9.60 | 2.04 | $64,112 |
| 101255 | JAMES & COMPANY LIGHTING | 25 | 15.40 | 59.70 | 3.88 | $56,646 |
| 073080 | GRAHAM'S LIGHTING FIXTURES, INC. | 61 | 6.90 | 14.40 | 2.09 | $49,837 |
| 183569 | ROBINSON LIGHTING-Winnepeg, MB | 23 | 16.90 | 48 | 2.84 | $47,217 |
| 110710 | KENNEDY-WEBSTER ELECTRIC CO | 35 | 13.10 | 20.10 | 1.53 | $46,594 |
| 124961 | LIGHTING CONNECTION | 25 | 15.90 | 28.40 | 1.79 | $45,986 |
| 135218 | Metro Appliance and More | 24 | 19.10 | 29.50 | 1.54 | $44,541 |
| 063455 | STEWART LIGHTING | 25 | 15.30 | 61.30 | 4.01 | $41,416 |
| 123100 | LIGHT ROOM LLC | 594 | 0.70 | 1.10 | 1.57 | $38,826 |
| 051230 | Decora Lighting Corp | 42 | 9.90 | 16.80 | 1.70 | $38,247 |
| 083333 | HOMESTYLES | 23 | 17.70 | 40.80 | 2.31 | $37,901 |

### Q-17_results.md

# Q-17 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 163305 | PRECISION LIGHTING & TRANSFORMER, INC. (aka) PLT | TX | 2025-09-02 18:41:35 | 25 | $61,581 |
| 163845 | PROJECT LIGHTING CO INC/CED | TX | 2026-02-25 19:32:02 | 10 | $41,780 |
| 051230 | Decora Lighting Corp | NJ | 2026-02-24 17:14:39 | 17 | $29,005 |
| 183569 | ROBINSON LIGHTING-Winnepeg, MB | MB | 2025-12-22 20:34:30 | 8 | $22,010 |
| 203801 | Tulsa Winnelson | OK | 2025-12-17 20:44:10 | 2 | $15,870 |
| 011455 | A-1 LED, LLC | AR | 2025-09-12 16:13:41 | 3 | $8,610 |
| 232150 | WHISKERTIN, LLC | OH | 2026-01-30 01:07:02 | 3 | $5,512 |
| 202120 | VINTAGE | OH | 2026-03-10 21:17:27 | 6 | $5,335 |
| 030398 | CFA TRADING | NJ | 2026-01-27 20:30:40 | 1 | $4,190 |
| 163200 | PRACTICAL PROPS | CA | 2026-02-04 23:33:21 | 5 | $3,716 |
| 197600 | STEADFAST LIGHTING | AR | 2026-01-27 16:28:06 | 3 | $3,465 |
| 060100 | F & M ELECTRIC SUPPLY CO | CT | 2026-02-19 12:46:27 | 2 | $3,279 |
| 101915 | JELLIOTT LIGHTS | MI | 2026-01-14 20:03:12 | 6 | $3,068 |
| 063100 | Shades & Lamps of Fletcher | NC | 2025-09-30 20:52:10 | 2 | $2,683 |
| 090206 | Illuminating Design LLC | NJ | 2026-01-02 17:05:00 | 40 | $2,665 |
| 032323 | CED dba ALL-PHASE ELECTRIC PETOSKEY | MI | 2026-03-10 19:50:19 | 2 | $2,143 |
| 030975 | CAPITAL LIGHTING FIXTURE COMPANY | GA | 2025-12-03 00:22:07 | 1 | $2,065 |
| 080900 | HAROLDS LAMPS & SHADES | WA | 2026-02-25 21:59:20 | 7 | $1,650 |
| 021000 | BARBIZON ELECTRIC CO., INC. | NY | 2026-01-08 17:24:16 | 2 | $1,630 |
| 100955 | JACKSON MOORE LIGHTING | WY | 2026-03-02 22:45:28 | 5 | $1,542 |
| 142648 | NOLAND - KNOXVILLE TN | TN | 2025-08-21 18:39:44 | 2 | $1,501 |
| 024498 | LYTEWORKS INC | FL | 2025-07-15 16:34:12 | 2 | $1,500 |
| 065070 | F.W. WEBB COMPANY - NY | NY | 2025-10-15 13:38:19 | 2 | $1,411 |
| 196705 | Staggs Carpets & Interiors, Inc. | MS | 2025-11-18 15:40:31 | 1 | $1,381 |
| 131920 | MARCH INDUSTRIES INC. | IL | 2025-06-27 13:27:54 | 1 | $1,358 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Bulbrite (bri, org_id=222)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 163305 | PRECISION LIGHTING & TRANSFORMER, INC. (aka) PLT | TX | $61,581 | 2025-09-02 18:41:35 | 287 |
| 163845 | PROJECT LIGHTING CO INC/CED | TX | $41,780 | 2026-02-25 19:32:02 | 111 |
| 051230 | Decora Lighting Corp | NJ | $29,005 | 2026-02-24 17:14:39 | 112 |
| 183569 | ROBINSON LIGHTING-Winnepeg, MB | MB | $22,010 | 2025-12-22 20:34:30 | 176 |
| 203801 | Tulsa Winnelson | OK | $15,870 | 2025-12-17 20:44:10 | 181 |
| 199005 | SUNLAN LIGHTING INC | OR | $13,300 | 2026-03-17 20:36:54 | 91 |
| 011455 | A-1 LED, LLC | AR | $8,610 | 2025-09-12 16:13:41 | 277 |
| 232150 | WHISKERTIN, LLC | OH | $5,512 | 2026-01-30 01:07:02 | 138 |
| 202120 | VINTAGE | OH | $5,335 | 2026-03-10 21:17:27 | 98 |
| 030398 | CFA TRADING | NJ | $4,190 | 2026-01-27 20:30:40 | 140 |
| 163200 | PRACTICAL PROPS | CA | $3,716 | 2026-02-04 23:33:21 | 132 |
| 197600 | STEADFAST LIGHTING | AR | $3,465 | 2026-01-27 16:28:06 | 140 |
| 060100 | F & M ELECTRIC SUPPLY CO | CT | $3,279 | 2026-02-19 12:46:27 | 117 |
| 101915 | JELLIOTT LIGHTS | MI | $3,068 | 2026-01-14 20:03:12 | 153 |
| 063100 | Shades & Lamps of Fletcher | NC | $2,683 | 2025-09-30 20:52:10 | 259 |
| 090206 | Illuminating Design LLC | NJ | $2,665 | 2026-01-02 17:05:00 | 165 |
| 032323 | CED dba ALL-PHASE ELECTRIC PETOSKEY | MI | $2,143 | 2026-03-10 19:50:19 | 98 |
| 030975 | CAPITAL LIGHTING FIXTURE COMPANY | GA | $2,065 | 2025-12-03 00:22:07 | 196 |
| 080900 | HAROLDS LAMPS & SHADES | WA | $1,650 | 2026-02-25 21:59:20 | 111 |
| 021000 | BARBIZON ELECTRIC CO., INC. | NY | $1,630 | 2026-01-08 17:24:16 | 159 |

### Q-40_results.md

# Q-40 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| UT | 3 | 59 | $623,192 |
| MA | 20 | 420 | $513,889 |
| TX | 20 | 203 | $333,494 |
| AR | 12 | 120 | $239,104 |
| NY | 41 | 452 | $231,299 |
| OK | 9 | 110 | $227,167 |
| MI | 7 | 135 | $194,007 |
| MN | 9 | 181 | $169,188 |
| TN | 10 | 80 | $146,110 |
| IA | 4 | 88 | $86,036 |
| FL | 14 | 129 | $84,246 |
| WI | 5 | 77 | $64,078 |
| NJ | 19 | 148 | $58,097 |
| CT | 5 | 56 | $52,659 |
| * | 7 | 43 | $50,972 |
| CA | 23 | 116 | $48,525 |
| PA | 15 | 125 | $43,621 |
| VA | 6 | 46 | $36,885 |
| GA | 10 | 35 | $35,838 |
| CO | 7 | 49 | $33,227 |

### Q-41_results.md

# Q-41 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 27
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 1 |
| 2025-03-01 | eCat Online-Acquired (self-serve) | 7 |
| 2025-04-01 | Rep-Acquired (iPad) | 1 |
| 2025-04-01 | eCat Online-Acquired (self-serve) | 12 |
| 2025-05-01 | eCat Online-Acquired (self-serve) | 11 |
| 2025-06-01 | eCat Online-Acquired (self-serve) | 7 |
| 2025-07-01 | eCat Online-Acquired (self-serve) | 7 |
| 2025-08-01 | Rep-Acquired (iPad) | 5 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 8 |
| 2025-09-01 | Rep-Acquired (iPad) | 3 |
| 2025-09-01 | eCat Online-Acquired (self-serve) | 9 |
| 2025-10-01 | Rep-Acquired (iPad) | 2 |
| 2025-10-01 | eCat Online-Acquired (self-serve) | 7 |
| 2025-11-01 | Rep-Acquired (iPad) | 1 |
| 2025-11-01 | eCat Online-Acquired (self-serve) | 4 |
| 2025-12-01 | Rep-Acquired (iPad) | 1 |
| 2025-12-01 | eCat Online-Acquired (self-serve) | 7 |
| 2026-01-01 | Rep-Acquired (iPad) | 2 |
| 2026-01-01 | eCat Online-Acquired (self-serve) | 9 |
| 2026-02-01 | Rep-Acquired (iPad) | 2 |
| 2026-02-01 | eCat Online-Acquired (self-serve) | 5 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 3 |
| 2026-04-01 | Rep-Acquired (iPad) | 1 |
| 2026-04-01 | eCat Online-Acquired (self-serve) | 5 |
| 2026-05-01 | Rep-Acquired (iPad) | 1 |
| 2026-05-01 | eCat Online-Acquired (self-serve) | 6 |
| 2026-06-01 | eCat Online-Acquired (self-serve) | 5 |

### Q-41_rep_results.md

# Q-41-rep Results — Bulbrite (bri, org_id=222)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Jason Burns | 7 |
| Pat Debarber | 2 |
| Pepper Carlson | 2 |
| Dave Kapalka | 2 |
| Vincent Ingato | 2 |
| Melissa Schultheis | 1 |
| Ruben Vargas | 1 |
| Shelly Orban | 1 |
| Kevin Gannon | 1 |
| Beth Peel | 1 |
| Bill Bondy | 1 |
| Jon McMahan | 1 |
| Aaron Moscowicz | 1 |

### Q-52_results.md

# Q-52 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 083172 | THE HOME DEPOT | — | 15,063 | $573,354 | 0 | $0 | 0 |
| 090043 | IBS Lighting | — | 75 | $475,133 | 0 | $0 | 0 |
| 161335 | PDI- PLUMBING DISTRIBUTORS INC. (PDI) *** | — | 163 | $474,138 | 0 | $0 | 0 |
| 160655 | Parallax Industries Inc. dba Square Deal Shop | — | 65 | $467,595 | 48 | $602,055 | 128.80 |
| 025958 | BULBS.COM | — | 306 | $466,223 | 295 | $476,032 | 102.10 |
| 163134 | WILLIAMS-SONOMA INC (PB-DS) | — | 13,208 | $387,069 | 0 | $0 | 0 |
| 128413 | LONESTAR ELECTRIC - AUSTIN, Houston | — | 206 | $384,582 | 0 | $0 | 0 |
| 163305 | PRECISION LIGHTING & TRANSFORMER, INC. (aka) PLT | — | 116 | $359,848 | 25 | $61,581 | 17.10 |
| 038017 | WAYFAIR, LLC -CASTLEGATE | — | 14,483 | $358,953 | 0 | $0 | 0 |
| 125240 | LIGHTING DESIGN LLC | — | 91 | $349,365 | 0 | $0 | 0 |
| 163136 | WILLIAMS-SONOMA INC  (WE-DS) | — | 16,995 | $332,320 | 0 | $0 | 0 |
| 128745 | LUMENS LIGHT & LIVING *** | — | 9,519 | $316,104 | 0 | $0 | 0 |
| 080488 | HANSEN LIGHTING INC. | — | 64 | $268,788 | 0 | $0 | 0 |
| 030398 | CFA TRADING | — | 59 | $247,146 | 1 | $4,190 | 1.70 |
| 080488 | NOVA LIGHTING INC. | — | 41 | $227,553 | 0 | $0 | 0 |
| 025720 | BUILD.COM | — | 4,345 | $201,433 | 0 | $0 | 0 |
| 062374 | Winsupply C Houston Co. | — | 14 | $201,123 | 0 | $0 | 0 |
| 128610 | LOWES COMPANY, INC. | — | 4,825 | $198,195 | 0 | $0 | 0 |
| 038019 | WAYFAIR, LLC *** | — | 6,113 | $186,249 | 0 | $0 | 0 |
| 182800 | REAL LIGHTING INC. | — | 270 | $184,511 | 0 | $0 | 0 |
| 161335 | PDI- PLUMBING DISTRIBUTORS INC. (PDI) | — | 59 | $171,017 | 0 | $0 | 0 |
| 070565 | GADSDEN LIGHTING SHOWROOM INC | — | 43 | $169,727 | 0 | $0 | 0 |
| 074020 | GREER LIGHTING CENTER, LLC | — | 28 | $157,495 | 0 | $0 | 0 |
| 192650 | SHADES OF LIGHT | — | 44 | $152,930 | 0 | $0 | 0 |
| 060501 | LIGHTING FIRST | — | 182 | $148,621 | 0 | $0 | 0 |
| 220210 | SERVICE LIGHTING (MN) *** | — | 173 | $138,396 | 0 | $0 | 0 |
| 127927 | LITECRAFT LIGHTING INC | — | 42 | $135,525 | 0 | $0 | 0 |
| 031105 | CAPITOL LIGHTING - FL location *** | — | 136 | $134,537 | 0 | $0 | 0 |
| 031099 | CAPITOL LIGHTING - NJ location | — | 235 | $129,717 | 0 | $0 | 0 |
| 163823 | PROGRESSIVE LIGHTING INC dba LEE LIGHTING(TX) | — | 43 | $127,164 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 083172 | THE HOME DEPOT | — | 15,063 | $573,354 |
| 090043 | IBS Lighting | — | 75 | $475,133 |
| 163134 | WILLIAMS-SONOMA INC (PB-DS) | — | 13,208 | $387,069 |
| 128413 | LONESTAR ELECTRIC - AUSTIN, Houston | — | 206 | $384,582 |
| 038017 | WAYFAIR, LLC -CASTLEGATE | — | 14,483 | $358,953 |
| 125240 | LIGHTING DESIGN LLC | — | 91 | $349,365 |
| 163136 | WILLIAMS-SONOMA INC  (WE-DS) | — | 16,995 | $332,320 |
| 128745 | LUMENS LIGHT & LIVING *** | — | 9,519 | $316,104 |
| 080488 | HANSEN LIGHTING INC. | — | 64 | $268,788 |
| 080488 | NOVA LIGHTING INC. | — | 41 | $227,553 |
| 025720 | BUILD.COM | — | 4,345 | $201,433 |
| 062374 | Winsupply C Houston Co. | — | 14 | $201,123 |
| 128610 | LOWES COMPANY, INC. | — | 4,825 | $198,195 |
| 038019 | WAYFAIR, LLC *** | — | 6,113 | $186,249 |
| 182800 | REAL LIGHTING INC. | — | 270 | $184,511 |
| 070565 | GADSDEN LIGHTING SHOWROOM INC | — | 43 | $169,727 |
| 074020 | GREER LIGHTING CENTER, LLC | — | 28 | $157,495 |
| 192650 | SHADES OF LIGHT | — | 44 | $152,930 |
| 060501 | LIGHTING FIRST | — | 182 | $148,621 |
| 220210 | SERVICE LIGHTING (MN) *** | — | 173 | $138,396 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AR | 0 | 0 | $0 | 12 | 120 | $239,104 | — |
| AZ | 0 | 0 | $0 | 2 | 5 | $794 | — |
| CA | 0 | 0 | $0 | 23 | 116 | $48,525 | — |
| CO | 0 | 0 | $0 | 7 | 49 | $33,227 | — |
| CT | 0 | 0 | $0 | 5 | 56 | $52,659 | — |
| DC | 0 | 0 | $0 | 1 | 1 | $22 | — |
| FL | 0 | 0 | $0 | 14 | 129 | $84,246 | — |
| GA | 0 | 0 | $0 | 10 | 35 | $35,838 | — |
| HI | 0 | 0 | $0 | 3 | 3 | $603 | — |
| IA | 0 | 0 | $0 | 4 | 88 | $86,036 | — |
| ID | 0 | 0 | $0 | 1 | 5 | $1,320 | — |
| IL | 0 | 0 | $0 | 10 | 33 | $12,936 | — |
| IN | 0 | 0 | $0 | 2 | 13 | $4,972 | — |
| KS | 0 | 0 | $0 | 3 | 45 | $5,042 | — |
| KY | 0 | 0 | $0 | 2 | 7 | $3,827 | — |
| LA | 0 | 0 | $0 | 3 | 15 | $9,404 | — |
| MA | 0 | 0 | $0 | 20 | 420 | $513,889 | — |
| MB | 0 | 0 | $0 | 2 | 9 | $22,349 | — |
| MD | 0 | 0 | $0 | 7 | 42 | $14,262 | — |
| * | 0 | 0 | $0 | 7 | 43 | $50,972 | — |

### Q-57_results.md

# Q-57 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unknown | $4.4M | $4.6M | 4.60 | 828 | 805 | 23 | 28,059 |

### Q-68_results.md

# Q-68 Results — Bulbrite (bri, org_id=222)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| LUMENS LIGHT & LIVING *** | Unknown | $410,283 | $867,713 | $457,429 | 47.30 | 13 |
| PROGRESSIVE | Unknown | $125,218 | $463,676 | $338,458 | 27 | 13 |
| WAYFAIR, LLC -CASTLEGATE | Unknown | $376,963 | $529,961 | $152,998 | 71.10 | 12 |
| CRAWFORD ELECTRIC SUPPLY CO. | Unknown | $34,696 | $175,600 | $140,904 | 19.80 | 6 |
| LIGHTING DESIGN LLC | Unknown | $342,312 | $469,943 | $127,631 | 72.80 | 13 |
| M & M LIGHTING-HOUSTON ** | Unknown | $171,380 | $295,200 | $123,821 | 58.10 | 13 |
| CE TANG YUK & CO., LTD. ** | Unknown | $39,133 | $150,671 | $111,538 | 26 | 5 |
| Aztec Lighting | Unknown | $1,334 | $103,698 | $102,364 | 1.30 | 6 |
| SERVICE LIGHTING (MN) *** | Unknown | $208,422 | $303,485 | $95,063 | 68.70 | 13 |
| LIGHTING SPECIALISTS, INC | Unknown | $57,844 | $152,367 | $94,523 | 38 | 7 |
| BUILDERS LIGHTING & DESIGN INC *** | Unknown | $7,398 | $85,487 | $78,089 | 8.70 | 11 |
| COFFMAN HOME DECOR | Unknown | $71,927 | $147,660 | $75,732 | 48.70 | 12 |
| FORESIGHT LIGHTING | Unknown | $7,756 | $75,119 | $67,364 | 10.30 | 3 |
| Low Country Lighting Inc | Unknown | $127,281 | $190,569 | $63,288 | 66.80 | 13 |
| FERGUSON-SC,23,589,43,72 | Unknown | $3,332 | $65,064 | $61,732 | 5.10 | 12 |
| URBAN LIGHTS | Unknown | $15,189 | $76,269 | $61,080 | 19.90 | 13 |
| BBC LIGHTING & SUPPLY | Unknown | $2,519 | $63,362 | $60,843 | 4 | 10 |
| SHADES OF LIGHT | Unknown | $173,820 | $234,409 | $60,589 | 74.20 | 13 |
| URBAN AMBIANCE INC | Unknown | $28,075 | $86,801 | $58,726 | 32.30 | 4 |
| BRAND NAME LIGHTING | Unknown | $132,022 | $189,955 | $57,934 | 69.50 | 12 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Bulbrite (bri, org_id=222)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Bulbrite (bri, org_id=222)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Bulbrite (bri, org_id=222)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Bulbrite (bri, org_id=222)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 128745 | LUMENS LIGHT & LIVING *** | — | 397,623.40 | 841,148.26 | -52.70 | 0 | 0 | — | CONTRACTING |
| 163820 | PROGRESSIVE | — | 113,256.33 | 394,530.81 | -71.30 | 0 | 0 | — | CONTRACTING |
| 038017 | WAYFAIR, LLC -CASTLEGATE | — | 358,953.21 | 524,670.66 | -31.60 | 0 | 0 | — | CONTRACTING |
| 125240 | LIGHTING DESIGN LLC | — | 349,364.73 | 480,965.96 | -27.40 | 0 | 0 | — | CONTRACTING |
| 130075 | M & M LIGHTING-HOUSTON ** | — | 145,326.96 | 263,766.65 | -44.90 | 121,928.17 | 0 | — | CONTRACTING |
| 126740 | LIGHTING SPECIALISTS, INC | — | 35,878.81 | 143,845.52 | -75.10 | 0 | 0 | — | CONTRACTING |
| 037221 | CRAWFORD ELECTRIC SUPPLY CO. | — | 36,169.27 | 143,633.54 | -74.80 | 0 | 0 | — | CONTRACTING |
| 032190 | CE TANG YUK & CO., LTD. ** | — | 41,646.43 | 128,042.74 | -67.50 | 39,513.06 | 92,442.28 | -57.30 | CONTRACTING |
| 211850 | URBAN AMBIANCE INC | — | 30,053.90 | 114,581.42 | -73.80 | 0 | 0 | — | CONTRACTING |
| 038019 | WAYFAIR, LLC *** | — | 265,782.12 | 342,963.98 | -22.50 | 0 | 0 | — | CONTRACTING |
| 128603 | Low Country Lighting Inc | — | 120,719.94 | 192,561.93 | -37.30 | 0 | 0 | — | CONTRACTING |
| 034890 | COFFMAN HOME DECOR | — | 70,483.71 | 137,812.95 | -48.90 | 0 | 0 | — | CONTRACTING |
| 220210 | SERVICE LIGHTING (MN) *** | — | 194,252.78 | 257,977.32 | -24.70 | 0 | 0 | — | CONTRACTING |
| 192650 | SHADES OF LIGHT | — | 152,929.58 | 214,500.01 | -28.70 | 0 | 0 | — | CONTRACTING |
| 161335 | PDI- PLUMBING DISTRIBUTORS INC. (PDI) *** | — | 645,154.38 | 593,588.61 | 8.70 | 0 | 1,249.74 | -100 | COMPETITIVE_DISPLACEMENT |
| 076000 | GW KEETER LIGHTING & HOME | — | 30,611.33 | 68,617.15 | -55.40 | 32,444.06 | 27,780.38 | 16.80 | CONTRACTING |
| 024508 | BRAND NAME LIGHTING | — | 107,488.39 | 145,155.38 | -25.90 | 40,378.28 | 20,257.63 | 99.30 | CONTRACTING |
| 061942 | FERGUSON-TX 1563,66,64,2751,2812 | — | 64,112.45 | 100,333.89 | -36.10 | 0 | 0 | — | CONTRACTING |
| 101255 | JAMES & COMPANY LIGHTING | — | 56,646.38 | 90,696.75 | -37.50 | 0 | 0 | — | CONTRACTING |
| 121890 | LEGEND LIGHTING INC. | — | 50,181.58 | 82,732.34 | -39.30 | 0 | 0 | — | CONTRACTING |
| 190422 | CHL LIGHTING INC | — | 45,474.45 | 76,222.96 | -40.30 | 0 | 0 | — | CONTRACTING |
| 038018 | WAYFAIR B2B | — | 71,244.57 | 100,992.03 | -29.50 | 0 | 0 | — | CONTRACTING |
| 082725 | HOLDER ELECTRIC CO | — | 44,950.08 | 74,484.22 | -39.70 | 0 | 0 | — | CONTRACTING |
| 074216 | GROSS ELECTRIC, INC. | — | 62,123.55 | 88,040.46 | -29.40 | 0 | 0 | — | CONTRACTING |
| 130645 | MADISON LIGHTING | — | 61,473.59 | 87,034.66 | -29.40 | 55,550.53 | 83,692.49 | -33.60 | CONTRACTING |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Bulbrite (bri, org_id=222)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 031099 | CAPITOL LIGHTING - NJ location | 2 | 81,899.69 | 228.60 | [{'quarter': '2025-07-01', 'revenue': 81899.69, 'qoq_pct': 228.6}, {'quarter': '2025-10-01', 'revenue': 11290.55, 'qoq_pct': -86.2}, {'quarter': '2026-01-01', 'revenue': 17176.05, 'qoq_pct': 52.1}, {'quarter': '2026-04-01', 'revenue': 16457.56, 'qoq_pct': -4.2}] |
| 128610 | LOWES COMPANY, INC. | 2 | 68,616.22 | 72 | [{'quarter': '2025-07-01', 'revenue': 29326.09, 'qoq_pct': -33.0}, {'quarter': '2025-10-01', 'revenue': 50446.2, 'qoq_pct': 72.0}, {'quarter': '2026-01-01', 'revenue': 68616.22, 'qoq_pct': 36.0}, {'quarter': '2026-04-01', 'revenue': 45101.4, 'qoq_pct': -34.3}] |
| 192650 | SHADES OF LIGHT | 3 | 65,470.57 | 133.70 | [{'quarter': '2025-07-01', 'revenue': 9623.15, 'qoq_pct': -86.8}, {'quarter': '2025-10-01', 'revenue': 22485.63, 'qoq_pct': 133.7}, {'quarter': '2026-01-01', 'revenue': 35792.95, 'qoq_pct': 59.2}, {'quarter': '2026-04-01', 'revenue': 65470.57, 'qoq_pct': 82.9}] |
| 074020 | GREER LIGHTING CENTER, LLC | 2 | 59,214.23 | 41.40 | [{'quarter': '2025-07-01', 'revenue': 59214.23, 'qoq_pct': 40.4}, {'quarter': '2025-10-01', 'revenue': 35919.2, 'qoq_pct': -39.3}, {'quarter': '2026-01-01', 'revenue': 23831.44, 'qoq_pct': -33.7}, {'quarter': '2026-04-01', 'revenue': 33702.94, 'qoq_pct': 41.4}] |
| 163845 | PROJECT LIGHTING CO INC/CED *** | 2 | 45,281.66 | 164.20 | [{'quarter': '2025-07-01', 'revenue': 29977.37, 'qoq_pct': 39.0}, {'quarter': '2025-10-01', 'revenue': 17140.29, 'qoq_pct': -42.8}, {'quarter': '2026-01-01', 'revenue': 45281.66, 'qoq_pct': 164.2}, {'quarter': '2026-04-01', 'revenue': 29665.35, 'qoq_pct': -34.5}] |
| 101255 | JAMES & COMPANY LIGHTING | 2 | 38,048.10 | 72.40 | [{'quarter': '2025-07-01', 'revenue': 38048.1, 'qoq_pct': 72.4}, {'quarter': '2025-10-01', 'revenue': 13057.17, 'qoq_pct': -65.7}, {'quarter': '2026-01-01', 'revenue': 2147.06, 'qoq_pct': -83.6}, {'quarter': '2026-04-01', 'revenue': 3394.05, 'qoq_pct': 58.1}] |
| 201735 | THREE JORDANS INC dba FORT WORTH LIGHTING | 2 | 36,004.22 | 32.70 | [{'quarter': '2025-07-01', 'revenue': 36004.22, 'qoq_pct': 32.2}, {'quarter': '2025-10-01', 'revenue': 23879.76, 'qoq_pct': -33.7}, {'quarter': '2026-01-01', 'revenue': 31677.53, 'qoq_pct': 32.7}, {'quarter': '2026-04-01', 'revenue': 27563.86, 'qoq_pct': -13.0}] |
| 043724 | DIVISION CONSTRUCTION SUPPLY | 2 | 32,473.12 | 6,587.80 | [{'quarter': '2025-07-01', 'revenue': 5552.14, 'qoq_pct': 804.0}, {'quarter': '2025-10-01', 'revenue': 485.56, 'qoq_pct': -91.3}, {'quarter': '2026-01-01', 'revenue': 32473.12, 'qoq_pct': 6587.8}, {'quarter': '2026-04-01', 'revenue': 428.93, 'qoq_pct': -98.7}] |
| 201500 | TEXAS BRIGHT IDEAS INC | 2 | 27,082.95 | 5,476.30 | [{'quarter': '2025-07-01', 'revenue': 21661.71, 'qoq_pct': 5476.3}, {'quarter': '2025-10-01', 'revenue': 15116.65, 'qoq_pct': -30.2}, {'quarter': '2026-01-01', 'revenue': 27082.95, 'qoq_pct': 79.2}, {'quarter': '2026-04-01', 'revenue': 5689.26, 'qoq_pct': -79.0}] |
| 063455 | STEWART LIGHTING | 2 | 25,398.30 | 235.40 | [{'quarter': '2025-07-01', 'revenue': 4966.67, 'qoq_pct': -50.2}, {'quarter': '2025-10-01', 'revenue': 7571.77, 'qoq_pct': 52.5}, {'quarter': '2026-01-01', 'revenue': 25398.3, 'qoq_pct': 235.4}, {'quarter': '2026-04-01', 'revenue': 3062.48, 'qoq_pct': -87.9}] |
| 143305 | IMAGINE MORE SERVICE CORP | 2 | 24,992.99 | 55.80 | [{'quarter': '2025-07-01', 'revenue': 12769.02, 'qoq_pct': -23.9}, {'quarter': '2025-10-01', 'revenue': 11256.84, 'qoq_pct': -11.8}, {'quarter': '2026-01-01', 'revenue': 17541.76, 'qoq_pct': 55.8}, {'quarter': '2026-04-01', 'revenue': 24992.99, 'qoq_pct': 42.5}] |
| 034350 | Labtrb, Inc dba CITY LIGHTS | 2 | 23,829.14 | 150.10 | [{'quarter': '2025-07-01', 'revenue': 9526.5, 'qoq_pct': 113.1}, {'quarter': '2025-10-01', 'revenue': 23829.14, 'qoq_pct': 150.1}, {'quarter': '2026-01-01', 'revenue': 20138.41, 'qoq_pct': -15.5}, {'quarter': '2026-04-01', 'revenue': 10134.11, 'qoq_pct': -49.7}] |
| 025160 | BRIGHT IDEAS | 2 | 20,053.55 | 32.90 | [{'quarter': '2025-07-01', 'revenue': 15158.08, 'qoq_pct': 20.6}, {'quarter': '2025-10-01', 'revenue': 20053.55, 'qoq_pct': 32.3}, {'quarter': '2026-01-01', 'revenue': 9603.12, 'qoq_pct': -52.1}, {'quarter': '2026-04-01', 'revenue': 12759.33, 'qoq_pct': 32.9}] |
| 013957 | AMERICAN LIGHTING INC | 2 | 19,761.70 | 40.90 | [{'quarter': '2025-07-01', 'revenue': 14022.44, 'qoq_pct': -41.6}, {'quarter': '2025-10-01', 'revenue': 19761.7, 'qoq_pct': 40.9}, {'quarter': '2026-01-01', 'revenue': 14656.42, 'qoq_pct': -25.8}, {'quarter': '2026-04-01', 'revenue': 19592.06, 'qoq_pct': 33.7}] |
| 032191 | CED - National Accounts | 3 | 19,621.19 | 320.90 | [{'quarter': '2025-07-01', 'revenue': 2172.84, 'qoq_pct': 57.4}, {'quarter': '2025-10-01', 'revenue': 9145.81, 'qoq_pct': 320.9}, {'quarter': '2026-01-01', 'revenue': 19621.19, 'qoq_pct': 114.5}, {'quarter': '2026-04-01', 'revenue': 2530.01, 'qoq_pct': -87.1}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Bulbrite (bri, org_id=222)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 6
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 773166 | LED14REC/5/6/930/WHRD/D | LED | 792,072.12 | 149,051 | — | 2040-4-4 | [{'customer': 'M & M LIGHTING-HOUSTON', 'revenue': 229999.27}, {'customer': 'GREER LIGHTING CENTER, LLC', 'revenue': 135862.69}, {'customer': 'MacMillan Distributing Inc', 'revenue': 91760.87}, {'customer': 'LONESTAR ELECTRIC - AUSTIN, Houston', 'revenue': 83809.24}, {'customer': 'NOVA LIGHTING INC.', 'revenue': 45421.18}, {'customer': 'AMERICAN LIGHTING INC', 'revenue': 42408.85}, {'customer': 'LIGHTING CORNER', 'revenue': 38672.3}, {'customer': 'BEALS LIGHTING & DECORATING GALLERY', 'revenue': 26616.92}, {'customer': 'LIGHTING DESIGN LLC', 'revenue': 20735.18}, {'customer': 'SHOWCASE LIGHTING BY 3-G LTD', 'revenue': 17622.5}, {'customer': 'THREE JORDANS INC dba FORT WORTH LIGHTING', 'revenue': 13223.58}, {'customer': 'Parallax Industries Inc. dba Square Deal Shop', 'revenue': 10736.73}, {'customer': 'RADUE HOMES dba INSPIRED SPACES', 'revenue': 10359.72}, {'customer': 'IMAGINE MORE SERVICE CORP', 'revenue': 6876.98}, {'customer': 'PDI- PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 6566.34}, {'customer': 'PROGRESSIVE LIGHTING INC dba LEE LIGHTING(NC)', 'revenue': 2138.6}, {'customer': 'SERVICE LIGHTING (MN)', 'revenue': 1208.34}, {'customer': 'BRAND NAME LIGHTING', 'revenue': 1188.59}, {'customer': 'LIGHTING SPECIALISTS, INC - Nova lighting', 'revenue': 1031.93}, {'customer': 'REAL LIGHTING INC.', 'revenue': 1020.45}, {'customer': 'CRAWFORD ELECTRIC SUPPLY CO.', 'revenue': 757.69}, {'customer': 'PINE TREE LIGHTING', 'revenue': 501.39}, {'customer': 'CFA TRADING', 'revenue': 488.41}, {'customer': 'ARIZONA LIGHTING CO. OF YUMA, INC.', 'revenue': 431.64}, {'customer': 'CAPITOL LIGHTING - FL location', 'revenue': 313.38}, {'customer': 'CLS LEDSpot.,LLC', 'revenue': 261.92}, {'customer': 'LSC HOLDINGS INC, dba LIGHTING SUPPLY', 'revenue': 258.97}, {'customer': 'LIGHTING CONNECTION', 'revenue': 215.83}, {'customer': 'CAPITOL LIGHTING - NJ location', 'revenue': 189.67}, {'customer': '1800LIGHTING.COM', 'revenue': 163.9}, {'customer': 'HOUSE OF SHADES & LAMPS', 'revenue': 160.04}, {'customer': 'LIGHTING N BEYOND LLC', 'revenue': 147.69}, {'customer': 'ST JAMES LIGHTING LLC', 'revenue': 142.79}, {'customer': 'PROGRESSIVE', 'revenue': 137.39}, {'customer': 'DECORUM', 'revenue': 132.85}, {'customer': 'CED - National Accounts', 'revenue': 123.52}, {'customer': 'EXWAY ELECTRIC SUPPLY CO', 'revenue': 110.69}, {'customer': 'Inspired Interiors', 'revenue': 75.72}, {'customer': 'Hudson Parc Lighting and Design', 'revenue': 62.96}, {'customer': 'URBAN LIGHTS', 'revenue': 57.49}, {'customer': 'COBUR', 'revenue': 52.0}, {'customer': 'TRI-SUPPLY LLC', 'revenue': 38.0}, {'customer': 'CREGGER COMPANY, INC', 'revenue': 33.35}, {'customer': 'INCON INDUSTRIES', 'revenue': 28.5}, {'customer': 'GELLER LIGHTING SUPPLY', 'revenue': 25.32}, {'customer': 'LIGHTING GETZ CORP.', 'revenue': 10.81}, {'customer': 'Bulbrite Industries Inc', 'revenue': 7.45}, {'customer': 'LIGHT BULB DISTRICT, INC', 'revenue': 0.0}, {'customer': 'Bluecom, LLC DBA SupplyStop', 'revenue': 0.0}, {'customer': 'TRINITY SALES GROUP LLC', 'revenue': 0.0}, {'customer': 'LAMPS PLUS dba PACIFIC COAST LIGHTING', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'LIGHTING PLUS', 'revenue': 0.0}, {'customer': 'KTR ASSOCIATES', 'revenue': 0.0}, {'customer': 'LYTEWORKS INC', 'revenue': 0.0}, {'customer': 'UNBEATABLESALE.COM INC.', 'revenue': 0.0}, {'customer': 'London Lighting LLC', 'revenue': -6.48}, {'customer': 'HOLDER ELECTRIC CO', 'revenue': -37.22}, {'customer': 'SOUTHERN LIGHTING GALLERY', 'revenue': -73.81}] | [{'item': '774244', 'desc': 'LED8A19/B60W/830/1P', 'available': 242227}, {'item': '774263', 'desc': 'LED9A19/PF60W/930/D/2/1P', 'available': 171667}, {'item': '776214', 'desc': 'LED7A19/30K/FIL/D/B/2', 'available': 128216}, {'item': '776212', 'desc': 'LED7A19/27K/FIL/D/B/2', 'available': 85200}, {'item': '774243', 'desc': 'LED8A19/B60W/827/1P', 'available': 74194}, {'item': '774262', 'desc': 'LED9A19/PF60W/927/D/2/1P', 'available': 51010}, {'item': '774280', 'desc': 'LED9A19/P60W/927/J/D/2/1P', 'available': 47742}, {'item': '776756', 'desc': 'LED4B11/27K/FIL/4/JA8', 'available': 46077}, {'item': '776627', 'desc': 'LED5B11/30K/FIL/E12/3', 'available': 38110}, {'item': '776204', 'desc': 'LED5B11/30K/FIL/D/B/2', 'available': 36790}, {'item': '773117', 'desc': 'LED9REC/4/940/WHRD/D', 'available': 32447}, {'item': '776873', 'desc': 'LED4G16/27K/FIL/3', 'available': 31103}, {'item': '776626', 'desc': 'LED5B11/27K/FIL/E12/3', 'available': 30021}, {'item': '776216', 'desc': 'LED7A19/40K/FIL/D/B/2', 'available': 29245}, {'item': '776201', 'desc': 'LED4B11/30K/FIL/D/B/2', 'available': 24933}, {'item': '773231', 'desc': 'LED7JBOXDL/3/930/WHRD/D', 'available': 21266}, {'item': '776207', 'desc': 'LED5T9/30K/FIL/D/B/2', 'available': 21110}, {'item': '772870', 'desc': 'LED8BR30/827/D/4', 'available': 20542}, {'item': '776215', 'desc': 'LED7A19/30K/FIL/M/D/B/2', 'available': 20370}, {'item': '776200', 'desc': 'LED4B11/27K/FIL/D/B/2', 'available': 19940}, {'item': '776768', 'desc': 'LED8A19/30K/FIL/3/JA8', 'available': 19752}, {'item': '772857', 'desc': 'LED8BR30/830/D/5', 'available': 18274}, {'item': '773232', 'desc': 'LED7JBOXDL/3/940/WHRD/D', 'available': 17512}, {'item': '776774', 'desc': 'LED8A19/27K/FIL/3/JA8', 'available': 17363}, {'item': '773167', 'desc': 'LED14REC/5/6/940/WHRD/D', 'available': 16954}, {'item': '770579', 'desc': 'LED4G9/30K/120/D', 'available': 16521}, {'item': '776931', 'desc': 'LED5B11/40K/FIL/E12/3', 'available': 13584}, {'item': '776769', 'desc': 'LED8ST18/30K/FIL/3/JA8', 'available': 13486}, {'item': '776962', 'desc': 'LED4B11/50K/FIL/3', 'available': 13132}, {'item': '772253', 'desc': 'LED15PAR38/B-FL40/830/WD/2', 'available': 12921}, {'item': '776224', 'desc': 'LED7ST18/30K/FIL/D/B/2', 'available': 12603}, {'item': '776763', 'desc': 'LED4B11/30K/FIL/4/JA8', 'available': 11901}, {'item': '776987', 'desc': 'LED13ST18/50K/FIL/3', 'available': 11700}, {'item': '776985', 'desc': 'LED8ST18/50K/FIL/3', 'available': 11431}, {'item': '776937', 'desc': 'LED8A19/27K/FIL/M/4', 'available': 11147}, {'item': '774265', 'desc': 'LED9A19/PF60W/950/D/2/1P', 'available': 10427}, {'item': '774245', 'desc': 'LED8A19/B60W/840/1P', 'available': 10401}, {'item': '776964', 'desc': 'LED5B11/50K/FIL/3', 'available': 10398}, {'item': '776966', 'desc': 'LED6B11/50K/FIL/3', 'available': 10362}, {'item': '776684', 'desc': 'LED1S14/24K/FIL', 'available': 10279}, {'item': '776767', 'desc': 'LED8ST18/27K/FIL/3/JA8', 'available': 10262}, {'item': '774281', 'desc': 'LED9A19/P60W/930/J/D/2/1P', 'available': 10171}, {'item': '776685', 'desc': 'LED1S14/27K/FIL', 'available': 9202}, {'item': '773262', 'desc': 'LED14JBOXDL/6/940/WHRD/D', 'available': 8927}, {'item': '776859', 'desc': 'LED4CA10/27K/FIL/3', 'available': 8859}, {'item': '776791', 'desc': 'LED4T6/30K/FIL/3', 'available': 8768}, {'item': '776977', 'desc': 'LED8G25/40K/FIL/3/JA8', 'available': 8685}, {'item': '774232', 'desc': 'LED9A19/B60W/840/1P', 'available': 8516}, {'item': '776220', 'desc': 'LED7G25/30K/FIL/M/D/B/2', 'available': 8183}, {'item': '776935', 'desc': 'LED8ST18/40K/FIL/3/JA8', 'available': 8053}, {'item': '776930', 'desc': 'LED4B11/40K/FIL/3/JA8', 'available': 8002}, {'item': '776963', 'desc': 'LED4B11/50K/FIL/M/3', 'available': 7911}, {'item': '776965', 'desc': 'LED5B11/50K/FIL/M/3', 'available': 7867}, {'item': '776967', 'desc': 'LED6B11/50K/FIL/M/3', 'available': 7771}, {'item': '776979', 'desc': 'LED8G25/50K/FIL/3', 'available': 7734}, {'item': '776976', 'desc': 'LED5G25/30K/FIL/M/3', 'available': 7639}, {'item': '776968', 'desc': 'LED6B11/40K/FIL/M/3', 'available': 7585}, {'item': '776904', 'desc': 'LED2T6/21K/FIL-NOS/3', 'available': 7484}, {'item': '776974', 'desc': 'LED5G25/27K/FIL/M/3', 'available': 7448}, {'item': '772245', 'desc': 'LED10PAR30S/B-FL40/830/WD/2', 'available': 7170}, {'item': '772254', 'desc': 'LED15PAR38/B-FL40/840/WD/2', 'available': 7138}, {'item': '776958', 'desc': 'LED8A19/50K/FIL/3', 'available': 7119}, {'item': '774267', 'desc': 'LED11A19/PF75W/930/D/2/1P', 'available': 7093}, {'item': '776203', 'desc': 'LED5B11/27K/FIL/D/B/2', 'available': 7031}, {'item': '773165', 'desc': 'LED14REC/5/6/927/WHRD/D', 'available': 6752}, {'item': '770191', 'desc': 'LED/C9C', 'available': 6725}, {'item': '776973', 'desc': 'LED5G25/27K/FIL/3', 'available': 6691}, {'item': '776945', 'desc': 'LED5T9L/27K/11/FIL/4', 'available': 6516}, {'item': '776732', 'desc': 'LED5T9/30K/5/FIL/4/JA8', 'available': 6468}, {'item': '774248', 'desc': 'LED8A19/B60W/830/4P', 'available': 6392}, {'item': '770595', 'desc': 'LED4E12/27K/120/D', 'available': 6243}, {'item': '776781', 'desc': 'LED5T9/27K/5/FIL/F/3', 'available': 6238}, {'item': '776223', 'desc': 'LED7ST18/27K/FIL/D/B/2', 'available': 6173}, {'item': '776975', 'desc': 'LED5G25/30K/FIL/3', 'available': 6138}, {'item': '776593', 'desc': 'LED4C15/21K/FIL/SPUN/AMB', 'available': 5879}, {'item': '776991', 'desc': 'LED5T9/50K/5/FIL/3', 'available': 5805}, {'item': '776402', 'desc': 'LED5CA10/30K-18K/WMDM/FIL/M', 'available': 5760}, {'item': '776980', 'desc': 'LED8G25/50K/FIL/M/3', 'available': 5759}, {'item': '776936', 'desc': 'LED13ST18/40K/FIL/3/JA8', 'available': 5688}, {'item': '776969', 'desc': 'LED5CA10/27K/FIL/E26/3', 'available': 5619}, {'item': '776960', 'desc': 'LED14A19/50K/FIL/3', 'available': 5594}, {'item': '776978', 'desc': 'LED8G25/40K/FIL/M/3', 'available': 5589}, {'item': '773272', 'desc': 'LED18JBOXDL/8/940/WHRD/D', 'available': 5540}, {'item': '776405', 'desc': 'LED9ST18/30K-18K/WMDM/FIL/M', 'available': 5471}, {'item': '773260', 'desc': 'LED14JBOXDL/6/927/WHRD/D', 'available': 5418}, {'item': '776780', 'desc': 'LED4T6/27K/FIL/3', 'available': 5254}, {'item': '776949', 'desc': 'LED3T9/30K/7/FIL/4', 'available': 5211}, {'item': '776951', 'desc': 'LED2T6/27K/FIL/3', 'available': 5170}, {'item': '776952', 'desc': 'LED2T6/30K/FIL/4', 'available': 5158}, {'item': '776592', 'desc': 'LED4C15/27K/FIL/SPUN/SAT', 'available': 5154}, {'item': '772302', 'desc': 'LED15PAR38/FL40/930/WD/2', 'available': 5122}, {'item': '776581', 'desc': 'LED4F15/21K/FIESTA/AMB', 'available': 5089}, {'item': '773240', 'desc': 'LED9JBOXDL/4/927/WHRD/D', 'available': 4978}, {'item': '772877', 'desc': 'LED15BR40/830/D/4', 'available': 4964}, {'item': '776219', 'desc': 'LED7G25/30K/FIL/D/B/2', 'available': 4860}, {'item': '776953', 'desc': 'LED2A19/27K/FIL/M/3', 'available': 4834}, {'item': '773210', 'desc': 'LED9JBOXDL/4/827/WHRD/D', 'available': 4829}, {'item': '776914', 'desc': 'LED9A19/30K/FIL/4', 'available': 4825}, {'item': '776959', 'desc': 'LED8A19/50K/FIL/M/3', 'available': 4815}, {'item': '776872', 'desc': 'LED5A19/27K/FIL/3', 'available': 4807}, {'item': '776989', 'desc': 'LED5T9/40K/5/FIL/3/JA8', 'available': 4806}, {'item': '776205', 'desc': 'LED5B11/40K/FIL/D/B/2', 'available': 4740}, {'item': '776902', 'desc': 'LED4A19/21K/FIL-NOS/3', 'available': 4729}, {'item': '776749', 'desc': 'LED8G25/27K/FIL/4/JA8', 'available': 4726}, {'item': '776206', 'desc': 'LED5T9/27K/FIL/D/B/2', 'available': 4718}, {'item': '776840', 'desc': 'LED6G40/27K/FIL/HW/3', 'available': 4647}, {'item': '776836', 'desc': 'LED6G40/27K/FIL/HB/3', 'available': 4647}, {'item': '776837', 'desc': 'LED5A19/27K/FIL/HW/3', 'available': 4522}, {'item': '776862', 'desc': 'LED4B11/27K/FIL/E26/3', 'available': 4453}, {'item': '776731', 'desc': 'LED5T9/27K/5/FIL/4/JA8', 'available': 4452}, {'item': '776833', 'desc': 'LED5A19/27K/FIL/HB/3', 'available': 4382}, {'item': '776580', 'desc': 'LED4F15/27K/FIESTA/CLR', 'available': 4348}, {'item': '776719', 'desc': 'LED5T9L/21K/15/FIL-NOS/3', 'available': 4325}, {'item': '776225', 'desc': 'LED7ST18/40K/FIL/D/B/2', 'available': 4199}, {'item': '776906', 'desc': 'LED2G16/21K/FIL-NOS/3', 'available': 4189}, {'item': '773221', 'desc': 'LED14JBOXDL/6/830/WHRD/D', 'available': 4186}, {'item': '771109', 'desc': 'LED6PAR16GUFL40/50/930/J/D/2', 'available': 4184}, {'item': '771086', 'desc': 'LED6MR16FL40/50/930/J/D/5', 'available': 4165}, {'item': '772246', 'desc': 'LED10PAR30S/B-FL40/840/WD/2', 'available': 4155}, {'item': '772856', 'desc': 'LED8BR30/827/D/5', 'available': 4138}, {'item': '776925', 'desc': 'LED8A19/40K/FIL/3/JA8', 'available': 4089}, {'item': '772242', 'desc': 'LED7PAR20/B-FL40/830/WD/2', 'available': 4049}, {'item': '771088', 'desc': 'LED7MR16FL40/75/930/J/D/2', 'available': 3955}, {'item': '776839', 'desc': 'LED5G25/27K/FIL/HW/3', 'available': 3940}, {'item': '776970', 'desc': 'LED5CA10/27K/FIL/E26/M/3', 'available': 3938}, {'item': '776992', 'desc': 'LED5T9/50K/5/FIL/F/3', 'available': 3902}, {'item': '776217', 'desc': 'LED7G25/27K/FIL/D/B/2', 'available': 3894}, {'item': '776982', 'desc': 'LED8G40/40K/FIL/M/3', 'available': 3881}, {'item': '776990', 'desc': 'LED5T9/40K/5/FIL/F/3', 'available': 3854}, {'item': '776832', 'desc': 'LED7A15/30K/FIL/M/3', 'available': 3831}, {'item': '776838', 'desc': 'LED2G16/27K/FIL/HW/3', 'available': 3791}, {'item': '772243', 'desc': 'LED7PAR20/B-FL40/840/WD/2', 'available': 3727}, {'item': '776981', 'desc': 'LED8G40/40K/FIL/3', 'available': 3726}, {'item': '776988', 'desc': 'LED6B11/30K/FIL/M/3', 'available': 3692}, {'item': '773271', 'desc': 'LED18JBOXDL/8/930/WHRD/D', 'available': 3675}, {'item': '776404', 'desc': 'LED9G25/30K-18K/WMDM/FIL/M', 'available': 3629}, {'item': '776744', 'desc': 'LED4G16/30K/FIL/4/JA8', 'available': 3590}, {'item': '776995', 'desc': 'LED4T6/50K/FIL/3', 'available': 3553}, {'item': '776986', 'desc': 'LED6B11/27K/FIL/M/3', 'available': 3541}, {'item': '776864', 'desc': 'LED4CA10/30K/FIL/3', 'available': 3495}, {'item': '776913', 'desc': 'LED9A19/27K/FIL/4', 'available': 3479}, {'item': '776829', 'desc': 'LED7A15/27K/FIL/3', 'available': 3434}, {'item': '774269', 'desc': 'LED15A19/P100W/930/J/D/2/1P', 'available': 3381}, {'item': '776938', 'desc': 'LED2B11/27K/FIL/4', 'available': 3374}, {'item': '771085', 'desc': 'LED6MR16FL40/50/927/J/D/5', 'available': 3361}, {'item': '776514', 'desc': 'LED4A19/21K/FIL-NOS/CURV/LOOP', 'available': 3346}, {'item': '774264', 'desc': 'LED9A19/PF60W/940/D/2/1P', 'available': 3333}, {'item': '776835', 'desc': 'LED5G25/27K/FIL/HB/3', 'available': 3331}, {'item': '776221', 'desc': 'LED7G25/40K/FIL/D/B/2', 'available': 3310}, {'item': '776743', 'desc': 'LED4G16/27K/FIL/4/JA8', 'available': 3301}, {'item': '773222', 'desc': 'LED14JBOXDL/6/840/WHRD/D', 'available': 3290}, {'item': '770195', 'desc': 'LED/C9O', 'available': 3261}, {'item': '776834', 'desc': 'LED2G16/27K/FIL/HB/3', 'available': 3187}, {'item': '772764', 'desc': 'LED10PAR30S/FL40/827/WD/2', 'available': 3177}, {'item': '776943', 'desc': 'LED4G16/27K/FIL/M/4', 'available': 3159}, {'item': '776897', 'desc': 'LED8G40/27K/FIL/M/3', 'available': 3156}, {'item': '776726', 'desc': 'LED5T9/30K/7/FIL/F/3', 'available': 3100}, {'item': '774285', 'desc': 'LED5/9/14A19/PF100W/827/3WAY/1P', 'available': 3098}, {'item': '776725', 'desc': 'LED5T9/27K/7/FIL/F/3', 'available': 3091}, {'item': '776721', 'desc': 'LED5T9L/30K/15/FIL/3', 'available': 3090}, {'item': '776591', 'desc': 'LED4C11/21K/FIL/SPUN/AMB', 'available': 3057}, {'item': '770598', 'desc': 'LED3G9/30K/W/D', 'available': 3052}, {'item': '770591', 'desc': 'LED4G9/27K/120/F/D', 'available': 3031}, {'item': '772286', 'desc': 'LED10PAR30L/FL40/927/WD/2', 'available': 3030}, {'item': '776858', 'desc': 'LED2CA10/27K/FIL/E12/3', 'available': 3009}, {'item': '772861', 'desc': 'LED15BR40/830/D/5', 'available': 3005}, {'item': '772248', 'desc': 'LED10PAR30L/B-FL40/830/WD/2', 'available': 3002}, {'item': '772859', 'desc': 'LED11BR30/830/D/5', 'available': 3002}, {'item': '770614', 'desc': 'LED1/FEST/27K/24/2', 'available': 2986}, {'item': '776961', 'desc': 'LED14A19/50K/FIL/M/3', 'available': 2979}, {'item': '776773', 'desc': 'LED4B11/30K/FIL/M/3', 'available': 2935}, {'item': '776713', 'desc': 'LED5T9/21K/7/FIL-NOS/3', 'available': 2900}, {'item': '776321', 'desc': 'LED4C53/30K/FIL/GRAD/SMK', 'available': 2891}, {'item': '776825', 'desc': 'LED4A15/27K/FIL/E12/3', 'available': 2861}, {'item': '776933', 'desc': 'LED4B11/40K/FIL/M/3', 'available': 2849}, {'item': '776950', 'desc': 'LED2S14/27K/FIL/4', 'available': 2820}, {'item': '776594', 'desc': 'LED4T6SL/27K/FIL/3', 'available': 2783}, {'item': '776934', 'desc': 'LED5B11/40K/FIL/M/3', 'available': 2781}, {'item': '776928', 'desc': 'LED7A19/40K/FIL/M/3', 'available': 2759}, {'item': '774279', 'desc': 'LED15A19/P100W/930/GU24/J/D/1P', 'available': 2755}, {'item': '774266', 'desc': 'LED11A19/PF75W/927/D/2/1P', 'available': 2739}, {'item': '770171', 'desc': 'LED/C7C', 'available': 2738}, {'item': '770637', 'desc': 'LED6R7S/30K/S/D', 'available': 2731}, {'item': '774286', 'desc': 'LED5/9/14A19/PF100W/830/3WAY/1P', 'available': 2692}, {'item': '772265', 'desc': 'LED6PAR20/NFL25/930/WD/2', 'available': 2689}, {'item': '776929', 'desc': 'LED14A19/40K/FIL/M/3', 'available': 2653}, {'item': '776712', 'desc': 'LED4G16/30K/FIL/M/3', 'available': 2647}, {'item': '776917', 'desc': 'LED9A19/27K/FIL/M/4', 'available': 2622}, {'item': '776108', 'desc': 'LED4A19/GRN/FIL/D', 'available': 2607}, {'item': '773170', 'desc': 'LED9REC/4/927/WHRD-G/D', 'available': 2585}, {'item': '776742', 'desc': 'LED5CA10/30K/FIL/4/JA8', 'available': 2573}, {'item': '776521', 'desc': 'LED11A19/30K/FIL/3WAY', 'available': 2561}, {'item': '776926', 'desc': 'LED9A19/40K/FIL/3', 'available': 2538}, {'item': '776741', 'desc': 'LED5CA10/27K/FIL/4/JA8', 'available': 2528}, {'item': '770586', 'desc': 'LED2G4/27K/12', 'available': 2517}, {'item': '776151', 'desc': 'LED2S14/AMB/FIL/D', 'available': 2514}, {'item': '770596', 'desc': 'LED4E12/27K/120/F/D', 'available': 2498}, {'item': '776218', 'desc': 'LED7G25/27K/FIL/M/D/B/2', 'available': 2470}, {'item': '776208', 'desc': 'LED7A15/27K/FIL/D/B/2', 'available': 2445}, {'item': '773180', 'desc': 'LED14REC/5/6/927/WHRD-G/D', 'available': 2436}, {'item': '771087', 'desc': 'LED7MR16FL40/75/927/J/D/2', 'available': 2420}, {'item': '770580', 'desc': 'LED4G9/30K/120/F/D', 'available': 2389}, {'item': '773181', 'desc': 'LED14REC/5/6/930/WHRD-G/D', 'available': 2354}, {'item': '776106', 'desc': 'LED4A19/AMB/FIL/D', 'available': 2350}, {'item': '776110', 'desc': 'LED4A19/PNK/FIL/D', 'available': 2347}, {'item': '770583', 'desc': 'LED2WEDGE/30K/12', 'available': 2339}, {'item': '776994', 'desc': 'LED4T6/40K/FIL/M/3', 'available': 2339}, {'item': '770613', 'desc': 'LED1/FEST/30K/24/2', 'available': 2327}, {'item': '776954', 'desc': 'LED5A19/27K/FIL/M/3', 'available': 2326}, {'item': '773242', 'desc': 'LED9JBOXDL/4/940/WHRD/D', 'available': 2320}, {'item': '776516', 'desc': 'LED4G25/21K/FIL-NOS/CURV/SPIRAL', 'available': 2296}, {'item': '776909', 'desc': 'LED7ST18/21K/FIL-NOS/3', 'available': 2288}, {'item': '776927', 'desc': 'LED14A19/40K/FIL/3', 'available': 2255}, {'item': '770638', 'desc': 'LED10R7S/30K/L/D', 'available': 2251}, {'item': '776520', 'desc': 'LED11A19/27K/FIL/3WAY', 'available': 2237}, {'item': '776801', 'desc': 'LED5ST18/22K/FIL-NOS/3', 'available': 2232}, {'item': '776403', 'desc': 'LED5G16/30K-18K/WMDM/FIL/M', 'available': 2228}, {'item': '770626', 'desc': 'LED5GY6/30K/12', 'available': 2226}, {'item': '776922', 'desc': 'LED9A19/30K/FIL/M/4', 'available': 2220}, {'item': '776228', 'desc': 'LED7A19/40K/FIL/D/B/2/4P', 'available': 2211}, {'item': '776720', 'desc': 'LED5T9L/27K/15/FIL/3', 'available': 2200}, {'item': '773241', 'desc': 'LED9JBOXDL/4/930/WHRD/D', 'available': 2188}, {'item': '772261', 'desc': 'LED6PAR20/NFL25/927/WD/2', 'available': 2141}, {'item': '776213', 'desc': 'LED7A19/27K/FIL/M/D/B/2', 'available': 2116}, {'item': '776948', 'desc': 'LED3T9/27K/7/FIL/4', 'available': 2111}, {'item': '770648', 'desc': 'LED5G9/30K/120/D/2', 'available': 2066}, {'item': '776916', 'desc': 'LED14A19/30K/FIL/3', 'available': 2042}, {'item': '776918', 'desc': 'LED14A19/27K/FIL/M/3', 'available': 2031}, {'item': '770611', 'desc': 'LED1/FEST/30K/12/2', 'available': 2019}, {'item': '776231', 'desc': 'LED4B11/40K/FIL/D/B/2/6P', 'available': 2018}, {'item': '770196', 'desc': 'LED/C9P', 'available': 2015}, {'item': '772249', 'desc': 'LED10PAR30L/B-FL40/840/WD/2', 'available': 2010}, {'item': '770630', 'desc': 'LED5E11/30K/120/D', 'available': 1992}, {'item': '776972', 'desc': 'LED5CA10/30K/FIL/E26/M/3', 'available': 1971}, {'item': '776996', 'desc': 'LED4T6/50K/FIL/M/3', 'available': 1954}, {'item': '770619', 'desc': 'LED4DC/30K/D', 'available': 1947}, {'item': '776941', 'desc': 'LED5B11/30K/FIL/M/4', 'available': 1934}, {'item': '776932', 'desc': 'LED6B11/40K/FIL/3', 'available': 1928}, {'item': '776983', 'desc': 'LED8G40/50K/FIL/3', 'available': 1927}, {'item': '776824', 'desc': 'LED4ST15/30K/FIL/M/3', 'available': 1925}, {'item': '770597', 'desc': 'LED3G9/27K/W/D', 'available': 1912}, {'item': '776750', 'desc': 'LED8G25/30K/FIL/4/JA8', 'available': 1904}, {'item': '776984', 'desc': 'LED8G40/50K/FIL/M/3', 'available': 1894}, {'item': '776785', 'desc': 'LED1S14/27K/FIL/PL', 'available': 1892}, {'item': '770625', 'desc': 'LED5GY6/27K/12', 'available': 1885}, {'item': '772610', 'desc': 'LED18PAR38/FL40/927/J/WD', 'available': 1866}, {'item': '774246', 'desc': 'LED8A19/B60W/850/1P', 'available': 1866}, {'item': '776109', 'desc': 'LED4A19/BLU/FIL/D', 'available': 1856}, {'item': '770624', 'desc': 'LED4G4/30K/12', 'available': 1855}, {'item': '776322', 'desc': 'LED4C53/30K/FIL/GRAD/BLU', 'available': 1849}, {'item': '770577', 'desc': 'LED3G9/30K/120', 'available': 1842}, {'item': '776827', 'desc': 'LED4A15/27K/FIL/M/E12/3', 'available': 1838}, {'item': '772876', 'desc': 'LED15BR40/827/D/4', 'available': 1811}, {'item': '770622', 'desc': 'LED3G4/WA/27K/12', 'available': 1811}, {'item': '776942', 'desc': 'LED4CA10/27K/FIL/M/3', 'available': 1809}, {'item': '770650', 'desc': 'LED2G4/30K/W/D', 'available': 1802}, {'item': '770589', 'desc': 'LED3G9/27K/120', 'available': 1801}, {'item': '776971', 'desc': 'LED5CA10/30K/FIL/E26/3', 'available': 1798}, {'item': '776920', 'desc': 'LED6G40/27K/FIL/HM/3', 'available': 1783}, {'item': '770658', 'desc': 'LED4G9/30K/W/F/D', 'available': 1770}, {'item': '773171', 'desc': 'LED9REC/4/930/WHRD-G/D', 'available': 1761}, {'item': '773270', 'desc': 'LED18JBOXDL/8/927/WHRD/D', 'available': 1754}, {'item': '776993', 'desc': 'LED4T6/40K/FIL/3', 'available': 1628}, {'item': '773115', 'desc': 'LED9REC/4/927/WHRD/D', 'available': 1613}, {'item': '776878', 'desc': 'LED8G40/27K/FIL/3', 'available': 1606}, {'item': '776861', 'desc': 'LED4CA10/30K/FIL/M/3', 'available': 1560}, {'item': '776831', 'desc': 'LED7A15/27K/FIL/M/3', 'available': 1523}, {'item': '771105', 'desc': 'LED6PAR16FL40/50/830/D/5', 'available': 1516}, {'item': '770643', 'desc': 'LED6E12/30K/120/D', 'available': 1512}, {'item': '776899', 'desc': 'LED8G40/30K/FIL/M/3', 'available': 1511}, {'item': '776997', 'desc': 'LED4G40/30K/FIL/GRAD/SMK', 'available': 1508}, {'item': '776823', 'desc': 'LED4ST15/27K/FIL/M/3', 'available': 1502}, {'item': '776903', 'desc': 'LED2CA10/21K/FIL-NOS/3', 'available': 1501}, {'item': '772860', 'desc': 'LED15BR40/827/D/5', 'available': 1488}, {'item': '770645', 'desc': 'LED6G9/30K/120/D', 'available': 1483}, {'item': '772301', 'desc': 'LED15PAR38/NF25/930/WD/2', 'available': 1478}, {'item': '776105', 'desc': 'LED4A19/RED/FIL/D', 'available': 1475}, {'item': '770652', 'desc': 'LED2G4/30K/W/F/D', 'available': 1471}, {'item': '772855', 'desc': 'LED7BR20/830/D/5', 'available': 1471}, {'item': '776746', 'desc': 'LED13ST18/30K/FIL/3/JA8', 'available': 1470}, {'item': '773220', 'desc': 'LED14JBOXDL/6/827/WHRD/D', 'available': 1467}, {'item': '774249', 'desc': 'LED8A19/B60W/840/4P', 'available': 1454}, {'item': '771117', 'desc': 'LED6PAR16FL40/50/830/D/4', 'available': 1449}, {'item': '776946', 'desc': 'LED5T9L/30K/11/FIL/4', 'available': 1448}, {'item': '776722', 'desc': 'LED4T8/21K/FIL-NOS/3', 'available': 1443}, {'item': '776870', 'desc': 'LED5G25/27K/FIL/HM/3', 'available': 1423}, {'item': '776707', 'desc': 'LED5T9L/21K/11/FIL-NOS/3', 'available': 1422}, {'item': '776828', 'desc': 'LED4A15/30K/FIL/M/E12/3', 'available': 1417}, {'item': '776241', 'desc': 'LED7G25/40K/FIL/D/B/2/4P', 'available': 1417}, {'item': '770612', 'desc': 'LED1/FEST/27K/12/2', 'available': 1409}, {'item': '772768', 'desc': 'LED10PAR30S/FL40/830/WD/2', 'available': 1408}, {'item': '776915', 'desc': 'LED14A19/27K/FIL/3', 'available': 1385}, {'item': '776237', 'desc': 'LED5B11/27K/FIL/D/B/2/25P', 'available': 1385}, {'item': '776826', 'desc': 'LED4A15/30K/FIL/E12/3', 'available': 1384}, {'item': '776800', 'desc': 'LED5G25/22K/FIL-NOS/3', 'available': 1379}, {'item': '776944', 'desc': 'LED8G25/27K/FIL/M/3', 'available': 1362}, {'item': '776229', 'desc': 'LED4B11/27K/FIL/D/B/2/6P', 'available': 1362}, {'item': '773152', 'desc': 'LED20DL/9/927/WHRD/J/D', 'available': 1359}, {'item': '772502', 'desc': 'LED15PAR38/FL/YLW/D', 'available': 1353}, {'item': '776232', 'desc': 'LED5B11/27K/FIL/D/B/2/6P', 'available': 1338}, {'item': '770651', 'desc': 'LED2G4/27K/W/F/D', 'available': 1336}, {'item': '776234', 'desc': 'LED5B11/40K/FIL/D/B/2/6P', 'available': 1333}, {'item': '776401', 'desc': 'LED5B11/30K-18K/WMDM/FIL/M', 'available': 1330}, {'item': '770576', 'desc': 'LED4GY8/30K/120/D', 'available': 1322}, {'item': '776406', 'desc': 'LED4G40/30K-18K/WMDM/FIL/M', 'available': 1319}, {'item': '776939', 'desc': 'LED4B11/27K/FIL/M/3', 'available': 1318}, {'item': '776730', 'desc': 'LED4T6/30K/FIL/M/3', 'available': 1316}, {'item': '776235', 'desc': 'LED4B11/27K/FIL/D/B/2/25P', 'available': 1314}, {'item': '776734', 'desc': 'LED5B11/30K/FIL/E26/3', 'available': 1299}, {'item': '774247', 'desc': 'LED8A19/B60W/827/4P', 'available': 1299}, {'item': '770604', 'desc': 'LED/LI4T8/27K', 'available': 1285}, {'item': '772854', 'desc': 'LED7BR20/827/D/5', 'available': 1280}, {'item': '772505', 'desc': 'LED15PAR38/FL/PNK/D', 'available': 1268}, {'item': '776738', 'desc': 'LED6B11/30K/FIL/3', 'available': 1266}, {'item': '772503', 'desc': 'LED15PAR38/FL/GRN/D', 'available': 1261}, {'item': '776830', 'desc': 'LED7A15/30K/FIL/3', 'available': 1256}, {'item': '776740', 'desc': 'LED6CA10/30K/FIL/3', 'available': 1253}, {'item': '776919', 'desc': 'LED14A19/30K/FIL/M/3', 'available': 1248}, {'item': '770585', 'desc': 'LED4E12/30K/120/F/D', 'available': 1242}, {'item': '776787', 'desc': 'LED5CA10/27K/FIL/M/3', 'available': 1240}, {'item': '772290', 'desc': 'LED10PAR30L/FL40/930/WD/2', 'available': 1233}, {'item': '773146', 'desc': 'LED15DL/7/927/WHSQ/J/D', 'available': 1216}, {'item': '776595', 'desc': 'LED4T6SL/30K/FIL/3', 'available': 1216}, {'item': '772278', 'desc': 'LED10PAR30S/FL40/930/WD/2', 'available': 1207}, {'item': '776239', 'desc': 'LED7G25/27K/FIL/D/B/2/4P', 'available': 1201}, {'item': '776748', 'desc': 'LED13G25/30K/FIL/3/JA8', 'available': 1200}, {'item': '776238', 'desc': 'LED5B11/30K/FIL/D/B/2/25P', 'available': 1199}, {'item': '770593', 'desc': 'LED4E11/27K/120/F/D', 'available': 1195}, {'item': '770581', 'desc': 'LED4E11/30K/120/D', 'available': 1182}, {'item': '776921', 'desc': 'LED2G16/27K/FIL/HG/3', 'available': 1179}, {'item': '772274', 'desc': 'LED10PAR30S/FL40/927/WD/2', 'available': 1176}, {'item': '772500', 'desc': 'LED15PAR38/FL/RED/D', 'available': 1169}, {'item': '771108', 'desc': 'LED6PAR16GUFL40/50/927/J/D/2', 'available': 1165}, {'item': '776210', 'desc': 'LED7A15/30K/FIL/D/B/2', 'available': 1145}, {'item': '770623', 'desc': 'LED4G4/27K/12', 'available': 1136}, {'item': '776107', 'desc': 'LED4A19/YLW/FIL/D', 'available': 1135}, {'item': '772504', 'desc': 'LED15PAR38/FL/BLU/D', 'available': 1124}, {'item': '774240', 'desc': 'LED9A19/P60W/940/J/D/1P', 'available': 1123}, {'item': '776735', 'desc': 'LED5B11/27K/FIL/M/E26/3', 'available': 1120}, {'item': '776226', 'desc': 'LED7A19/27K/FIL/D/B/2/4P', 'available': 1113}, {'item': '772858', 'desc': 'LED11BR30/827/D/5', 'available': 1094}, {'item': '776306', 'desc': 'LED4OLIVE/22K/FIL', 'available': 1089}, {'item': '776747', 'desc': 'LED13G25/27K/FIL/3/JA8', 'available': 1071}, {'item': '770152', 'desc': 'LED/G14G', 'available': 1049}, {'item': '773125', 'desc': 'LED11JBOXDL/6/827/WHRD/D', 'available': 1038}, {'item': '776318', 'desc': 'LED4JEWEL/20K/FIL-NOS', 'available': 1037}, {'item': '774254', 'desc': 'LED9A19/PF60W/930/D/2/4P', 'available': 1035}, {'item': '772865', 'desc': 'LED7R20/830/D/4', 'available': 1013}, {'item': '772298', 'desc': 'LED15PAR38/FL40/927/WD/2', 'available': 994}, {'item': '774253', 'desc': 'LED9A19/PF60W/927/D/2/4P', 'available': 984}, {'item': '776153', 'desc': 'LED2S14/GRN/FIL/D', 'available': 983}, {'item': '774256', 'desc': 'LED9A19/PF60W/950/D/2/4P', 'available': 982}, {'item': '776209', 'desc': 'LED7A15/27K/FIL/M/D/B/2', 'available': 967}, {'item': '774250', 'desc': 'LED8A19/B60W/850/4P', 'available': 964}, {'item': '776792', 'desc': 'LED5T9/30K/5/FIL/F/3', 'available': 963}, {'item': '770594', 'desc': 'LED2WEDGE/27K/12', 'available': 961}, {'item': '774283', 'desc': 'LED9A19/P60W/927/GU24/J/D/2/1P', 'available': 958}, {'item': '776222', 'desc': 'LED7G25/40K/FIL/M/D/B/2', 'available': 941}, {'item': '776737', 'desc': 'LED6B11/27K/FIL/3', 'available': 939}, {'item': '776400', 'desc': 'LED9A19/30K-18K/WMDM/FIL/M', 'available': 930}, {'item': '770599', 'desc': 'LED4G9/27K/W/D', 'available': 929}, {'item': '776879', 'desc': 'LED8G40/30K/FIL/3', 'available': 928}, {'item': '772501', 'desc': 'LED15PAR38/FL/AMB/D', 'available': 917}, {'item': '770641', 'desc': 'LED6E11/30K/120/D', 'available': 905}, {'item': '770620', 'desc': 'LED4DC/27K/D', 'available': 888}, {'item': '776819', 'desc': 'LED5T14/27K/FIL/3', 'available': 884}, {'item': '776155', 'desc': 'LED2S14/PNK/FIL/D', 'available': 861}, {'item': '770616', 'desc': 'LED4GY6/27K/D/2', 'available': 860}, {'item': '770584', 'desc': 'LED4E12/30K/120/D', 'available': 849}, {'item': '770600', 'desc': 'LED4G9/30K/W/D', 'available': 848}, {'item': '770660', 'desc': 'LED3G9/30K/W/F/D', 'available': 837}, {'item': '776728', 'desc': 'LED5T9/30K/11/FIL/F/3', 'available': 834}, {'item': '770656', 'desc': 'LED2GY6/30K/12/W/F/D', 'available': 827}, {'item': '776924', 'desc': 'LED6G40/27K/FIL/HG/3', 'available': 826}, {'item': '776998', 'desc': 'LED4G40/30K/FIL/GRAD/BLU', 'available': 806}, {'item': '776739', 'desc': 'LED6CA10/27K/FIL/3', 'available': 799}, {'item': '776317', 'desc': 'LED4DROP/20K/FIL-NOS', 'available': 796}, {'item': '776243', 'desc': 'LED7ST18/30K/FIL/D/B/2/4P', 'available': 793}, {'item': '770632', 'desc': 'LED5E12/30K/120/D', 'available': 785}, {'item': '776515', 'desc': 'LED3ST18/21K/FIL-NOS/CURV/HAIRPIN', 'available': 780}, {'item': '772767', 'desc': 'LED10PAR30S/NF25/830/WD/2', 'available': 756}, {'item': '770629', 'desc': 'LED5E11/27K/120/D', 'available': 755}, {'item': '776771', 'desc': 'LED2G16/27K/FIL/HM/3', 'available': 755}, {'item': '776820', 'desc': 'LED5T14/30K/FIL/3', 'available': 735}, {'item': '776152', 'desc': 'LED2S14/YLW/FIL/D', 'available': 732}, {'item': '770649', 'desc': 'LED2G4/27K/W/D', 'available': 731}, {'item': '774251', 'desc': 'LED8A19/B60W/827/25P', 'available': 725}, {'item': '776101', 'desc': 'LED27T5/48/840/DIR', 'available': 723}, {'item': '770571', 'desc': 'LED2G4/30K/12', 'available': 715}, {'item': '776810', 'desc': 'LED8G25/30K/FIL/M/3', 'available': 714}, {'item': '776150', 'desc': 'LED2S14/RED/FIL/D', 'available': 688}, {'item': '774242', 'desc': 'LED9A19/P60W/930/GU24/J/D/1P', 'available': 679}, {'item': '770587', 'desc': 'LED3G4/27K/12', 'available': 664}, {'item': '772792', 'desc': 'LED15PAR38/FL40/830/WD/2', 'available': 662}, {'item': '770647', 'desc': 'LED5G9/27K/120/D/2', 'available': 655}, {'item': '770653', 'desc': 'LED2GY6/27K/12/W/D', 'available': 654}, {'item': '776706', 'desc': 'LED2G16/27K/FIL/3', 'available': 641}, {'item': '772775', 'desc': 'LED10PAR30L/NF25/827/WD/2', 'available': 641}, {'item': '776908', 'desc': 'LED3T9/21K/FIL-NOS/3', 'available': 638}, {'item': '776923', 'desc': 'LED4G25/27K/FIL/HG/3', 'available': 633}, {'item': '776230', 'desc': 'LED4B11/30K/FIL/D/B/2/6P', 'available': 631}, {'item': '776154', 'desc': 'LED2S14/BLU/FIL/D', 'available': 618}, {'item': '776005', 'desc': 'LED20T8/30K', 'available': 616}, {'item': '770590', 'desc': 'LED4G9/27K/120/D', 'available': 608}, {'item': '776242', 'desc': 'LED7ST18/27K/FIL/D/B/2/4P', 'available': 605}, {'item': '776822', 'desc': 'LED4ST15/30K/FIL/3', 'available': 599}, {'item': '770654', 'desc': 'LED2GY6/30K/12/W/D', 'available': 595}, {'item': '774258', 'desc': 'LED9A19/PF60W/930/D/2/25P', 'available': 567}, {'item': '776871', 'desc': 'LED2A19/27K/FIL/3', 'available': 561}, {'item': '776302', 'desc': 'LED4G63/22K/FIL', 'available': 559}, {'item': '776745', 'desc': 'LED13ST18/27K/FIL/3/JA8', 'available': 540}, {'item': '770631', 'desc': 'LED5E12/27K/120/D', 'available': 506}, {'item': '776854', 'desc': 'LED3T9/30K/FIL/3', 'available': 504}, {'item': '776940', 'desc': 'LED5B11/27K/FIL/M/4', 'available': 499}, {'item': '772262', 'desc': 'LED6PAR20/FL40/927/WD/2', 'available': 477}, {'item': '772779', 'desc': 'LED10PAR30L/NF25/830/WD/2', 'available': 469}, {'item': '770655', 'desc': 'LED2GY6/27K/12/W/F/D', 'available': 438}, {'item': '770621', 'desc': 'LED3G4/WA/30K/12', 'available': 434}, {'item': '770588', 'desc': 'LED4GY8/27K/120/D', 'available': 416}, {'item': '776211', 'desc': 'LED7A15/30K/FIL/M/D/B/2', 'available': 387}, {'item': '770194', 'desc': 'LED/C9G', 'available': 375}, {'item': '770618', 'desc': 'LED4SC/27K/12', 'available': 373}, {'item': '776233', 'desc': 'LED5B11/30K/FIL/D/B/2/6P', 'available': 369}, {'item': '770640', 'desc': 'LED6E11/27K/120/D', 'available': 367}, {'item': '776518', 'desc': 'LED4T14/21K/FIL-NOS/CURV/SPIRAL', 'available': 357}, {'item': '770644', 'desc': 'LED6G9/27K/120/D', 'available': 340}, {'item': '776679', 'desc': 'LED5A19/27K/FIL/HG/3', 'available': 328}, {'item': '776596', 'desc': 'LED4PRISM/30K/FIL/3', 'available': 296}, {'item': '772266', 'desc': 'LED6PAR20/FL40/930/WD/2', 'available': 276}, {'item': '776727', 'desc': 'LED5T9/27K/11/FIL/F/3', 'available': 269}, {'item': '772756', 'desc': 'LED7PAR20/FL40/830/WD/2', 'available': 265}, {'item': '773158', 'desc': 'LED20DL/9/927/WHSQ/J/D', 'available': 259}, {'item': '776821', 'desc': 'LED4ST15/27K/FIL/3', 'available': 258}, {'item': '776227', 'desc': 'LED7A19/30K/FIL/D/B/2/4P', 'available': 231}, {'item': '776240', 'desc': 'LED7G25/30K/FIL/D/B/2/4P', 'available': 197}, {'item': '776905', 'desc': 'LED4T14/21K/FIL-NOS/3', 'available': 190}, {'item': '774257', 'desc': 'LED9A19/PF60W/927/D/2/25P', 'available': 185}, {'item': '776788', 'desc': 'LED5CA10/30K/FIL/M/3', 'available': 179}, {'item': '776244', 'desc': 'LED7ST18/40K/FIL/D/B/2/4P', 'available': 155}, {'item': '774276', 'desc': 'LED15A19/P100W/927/J/D/1P', 'available': 150}, {'item': '776314', 'desc': 'LED4BT56/22K/FIL', 'available': 147}, {'item': '770659', 'desc': 'LED3G9/27K/W/F/D', 'available': 144}, {'item': '776736', 'desc': 'LED5B11/30K/FIL/M/E26/3', 'available': 140}, {'item': '770615', 'desc': 'LED4GY6/30K/D/2', 'available': 112}, {'item': '776305', 'desc': 'LED4DIA/22K/FIL', 'available': 86}, {'item': '772763', 'desc': 'LED10PAR30S/NF25/827/WD/2', 'available': 77}, {'item': '777801', 'desc': 'AC-CC-0002-00-S1', 'available': 74}, {'item': '777902', 'desc': 'SR111-18-36D-927-03', 'available': 68}, {'item': '776301', 'desc': 'LED4ET25/22K/FIL', 'available': 66}, {'item': '776304', 'desc': 'LED4BH/22K/FIL', 'available': 66}, {'item': '777252', 'desc': 'SP20-11-10D-927-03', 'available': 53}, {'item': '776300', 'desc': 'LED4PS52/22K/FIL', 'available': 51}, {'item': '777803', 'desc': 'AC-GC-2525-00-S1', 'available': 40}, {'item': '777809', 'desc': 'AC-FR-3636-00-S1', 'available': 35}, {'item': '777679', 'desc': 'SP38-14-60D-827-H1', 'available': 30}, {'item': '777823', 'desc': 'AC-E-GC-2525-00-S1', 'available': 25}, {'item': '772717', 'desc': 'LED7PAR20/NF25/840/WD', 'available': 23}, {'item': '771208', 'desc': 'LED6MR16FL35/50/830/D', 'available': 21}, {'item': '777766', 'desc': 'SP38-18-36D-930-03', 'available': 14}, {'item': '777700', 'desc': 'SP30L-18-09D-927-03', 'available': 12}, {'item': '777721', 'desc': 'SP30S-18-25D-927-03', 'available': 10}, {'item': '777681', 'desc': 'SP38-14-25D-830-H1', 'available': 10}, {'item': '774260', 'desc': 'LED11A19/PF75W/927/D/1P', 'available': 10}, {'item': '777661', 'desc': 'SP30L-14-25D-827-H1', 'available': 10}, {'item': '773230', 'desc': 'LED7JBOXDL/3/927/WHRD/D', 'available': 9}, {'item': '777827', 'desc': 'AC-E-GE-1036-00-S1', 'available': 9}, {'item': '776320', 'desc': 'LED4GLACIER/20K/FIL-NOS', 'available': 9}, {'item': '774252', 'desc': 'LED8A19/B60W/830/25P', 'available': 8}, {'item': '777707', 'desc': 'SP30L-18-60D-930-03', 'available': 6}, {'item': '777235', 'desc': 'SP20-11-36D-830-H1', 'available': 6}, {'item': '777764', 'desc': 'SP38-18-09D-930-03', 'available': 5}, {'item': '777579', 'desc': 'SM16GA-09-60D-930-03', 'available': 5}, {'item': '777046', 'desc': 'SM16-09-25D-827-H1', 'available': 4}, {'item': '777670', 'desc': 'SP30S-14-36D-827-H1', 'available': 4}, {'item': '777722', 'desc': 'SP30S-18-36D-927-03', 'available': 4}, {'item': '772776', 'desc': 'LED10PAR30L/FL40/827/WD/2', 'available': 3}, {'item': '777931', 'desc': 'SR111-12-25D-927-03', 'available': 3}, {'item': '777683', 'desc': 'SP38-14-60D-830-H1', 'available': 3}, {'item': '777532', 'desc': 'SM16GA-09-60D-827-H1', 'available': 3}, {'item': '777723', 'desc': 'SP30S-18-60D-927-03', 'available': 3}, {'item': '777660', 'desc': 'SP30L-14-09D-827-H1', 'available': 3}, {'item': '777760', 'desc': 'SP38-18-09D-927-03', 'available': 3}, {'item': '777253', 'desc': 'SP20-11-10D-930-03', 'available': 2}, {'item': '777265', 'desc': 'SP20-11-36D-930-03', 'available': 2}, {'item': '777576', 'desc': 'SM16GA-09-36D-927-03', 'available': 2}, {'item': '777726', 'desc': 'SP30S-18-36D-930-03', 'available': 2}, {'item': '777702', 'desc': 'SP30L-18-36D-927-03', 'available': 2}, {'item': '777814', 'desc': 'AC-E-AM-0020-00-S1', 'available': 2}, {'item': '777828', 'desc': 'AC-E-FR-3636-00-S1', 'available': 2}, {'item': '777059', 'desc': 'SM16-07-36D-930-03', 'available': 2}, {'item': '777821', 'desc': 'AC-E-CC-0002-00-S1', 'available': 1}, {'item': '777048', 'desc': 'SM16-09-25D-830-H1', 'available': 1}, {'item': '777767', 'desc': 'SP38-18-60D-930-03', 'available': 1}, {'item': '777802', 'desc': 'AC-CC-0003-00-S1', 'available': 1}, {'item': '777673', 'desc': 'SP30S-14-25D-830-H1', 'available': 1}, {'item': '777815', 'desc': 'AC-E-EN-0001-00-S1', 'available': 1}, {'item': '777259', 'desc': 'SP20-11-25D-930-03', 'available': 1}, {'item': '777521', 'desc': 'SM16GA-07-10D-830-H1', 'available': 1}, {'item': '777533', 'desc': 'SM16GA-09-60D-830-H1', 'available': 1}, {'item': '777832', 'desc': 'SR111-19-36DM-927/918-01', 'available': 1}, {'item': '777578', 'desc': 'SM16GA-09-60D-927-03', 'available': 1}, {'item': '777724', 'desc': 'SP30S-18-09D-930-03', 'available': 1}, {'item': '777900', 'desc': 'SR111-18-09D-927-03', 'available': 1}] |
| 774239 | LED9A19/P60W/930/J/D/1P | LED | 254,415.19 | 122,429 | — | — | [{'customer': 'LONESTAR ELECTRIC - AUSTIN, Houston', 'revenue': 65661.02}, {'customer': 'GRAND RAPIDS LIGHTING CENTER', 'revenue': 36166.45}, {'customer': 'PACIFIC BUILDERS HARDWARE & LIGHTING, INC.', 'revenue': 33813.15}, {'customer': 'PDI- PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 23832.91}, {'customer': 'CONNECTICUT LIGHTING CENTER', 'revenue': 17372.54}, {'customer': 'JAMES & COMPANY LIGHTING', 'revenue': 15948.25}, {'customer': 'LIGHTING UNLIMITED', 'revenue': 9474.87}, {'customer': 'PREMIER LIGHTING', 'revenue': 8985.6}, {'customer': 'BULBS.COM', 'revenue': 4216.05}, {'customer': 'BRIGHT IDEAS', 'revenue': 3969.04}, {'customer': 'GALLERIA LIGHTING', 'revenue': 3674.87}, {'customer': 'VALLEY LIGHT GALLERY', 'revenue': 3167.55}, {'customer': 'PEAK LIGHTING PRODUCTS INC', 'revenue': 2563.9}, {'customer': 'Southland Lighting LLC', 'revenue': 1998.02}, {'customer': 'PRECISION LIGHTING & TRANSFORMER, INC. (aka) PLT', 'revenue': 1972.64}, {'customer': 'LIGHTING FIRST', 'revenue': 1727.91}, {'customer': 'Glass Designs Lighting', 'revenue': 1679.46}, {'customer': 'CANDELA CORP', 'revenue': 1451.62}, {'customer': "MONTGOMERY'S FURNITURE GALLERY", 'revenue': 1342.1}, {'customer': 'ILLUMINATIONS', 'revenue': 1247.48}, {'customer': 'BAYSHORE SUPPLY & LIGHTS, SC', 'revenue': 1069.38}, {'customer': 'NOVA LIGHTING INC.', 'revenue': 794.42}, {'customer': 'KLS LLC dba SPECTRUM LIGHTING', 'revenue': 738.43}, {'customer': 'CORDAY LIGHTING', 'revenue': 709.08}, {'customer': 'CAPITOL LIGHTING - FL location', 'revenue': 648.11}, {'customer': 'CED - SANTA BARBARA, CA', 'revenue': 641.86}, {'customer': 'BUILDERS LIGHTING & DESIGN INC', 'revenue': 561.38}, {'customer': 'CABINET & LIGHTING SUPPLY', 'revenue': 552.75}, {'customer': 'LONESTAR ELECTRIC - DALLAS', 'revenue': 504.38}, {'customer': 'CAPITOL LIGHTING - NJ location', 'revenue': 476.45}, {'customer': 'WILSON LIGHTING OF NAPLES', 'revenue': 474.46}, {'customer': 'ACROPOLIS', 'revenue': 455.93}, {'customer': '1800LIGHTING.COM', 'revenue': 429.01}, {'customer': 'PACIFIC LIGHTING RESOURCES', 'revenue': 364.99}, {'customer': 'SERVICE LIGHTING (MN)', 'revenue': 321.52}, {'customer': 'BERNARD ELECTRIC SUPPLY CO', 'revenue': 312.18}, {'customer': 'SOLUTEX INC', 'revenue': 279.87}, {'customer': 'REAL LIGHTING INC.', 'revenue': 272.73}, {'customer': 'CAMINITI ASSOCIATES, INC dba CAIDESIGNS', 'revenue': 266.83}, {'customer': 'ENERGY PLUS WHOLESALE LIGHTING', 'revenue': 266.26}, {'customer': 'Vox Lumen, LLC', 'revenue': 258.73}, {'customer': 'MANHATTAN LIGHTS INC.', 'revenue': 252.66}, {'customer': 'Aggieland Lighting & Design', 'revenue': 236.49}, {'customer': 'FW WEBB COMPANY - BR70 Waterbury, CT', 'revenue': 194.0}, {'customer': 'MINNESOTA LIGHTING FIREPLACE &', 'revenue': 178.45}, {'customer': 'HOUSE OF SHADES & LAMPS', 'revenue': 176.03}, {'customer': 'PRESTIGE LIGHTING & DESIGN', 'revenue': 161.77}, {'customer': 'UNITED LIGHTING & SUPPLY', 'revenue': 158.16}, {'customer': 'MONTREAL LIGHTING & HARDWARE INC.', 'revenue': 152.28}, {'customer': 'LUXE LIGHT STUDIO dba KA MANAGEMENT', 'revenue': 133.75}, {'customer': 'CED dba ALL-PHASE ELECTRIC PETOSKEY', 'revenue': 126.61}, {'customer': 'EXWAY ELECTRIC SUPPLY CO', 'revenue': 123.59}, {'customer': 'LUMEN ILUMINACION, LTD.', 'revenue': 116.27}, {'customer': 'SMALL TOWN HOME & DECOR', 'revenue': 115.77}, {'customer': 'HOLDER ELECTRIC CO', 'revenue': 105.82}, {'customer': 'LIGHTING SPECIALISTS, INC - Nova lighting', 'revenue': 99.08}, {'customer': 'RABBIT CREEK DBA Visual Comfort', 'revenue': 88.64}, {'customer': 'LOFINGS LIGHTING, INC.', 'revenue': 84.87}, {'customer': 'First Choice Electrical Supply', 'revenue': 81.32}, {'customer': 'FW Webb Company - BR23 Needham, MA', 'revenue': 80.43}, {'customer': 'LIGHT HOUSE OF LEWES INC', 'revenue': 77.64}, {'customer': 'LYTEWORKS INC', 'revenue': 77.61}, {'customer': 'IMPALA INDUSTRIES, INC', 'revenue': 64.92}, {'customer': 'MAISON DU LUMINAIRE INC', 'revenue': 59.12}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 56.62}, {'customer': 'LAIDCO SALES INC', 'revenue': 54.9}, {'customer': 'Embellishments Gallerie', 'revenue': 51.54}, {'customer': 'The Jarrell Company', 'revenue': 51.07}, {'customer': 'DAN WEST INTERIOR DESIGN', 'revenue': 50.85}, {'customer': 'FOGG LIGHTING', 'revenue': 49.6}, {'customer': 'LIGHTING INNOVATION', 'revenue': 47.84}, {'customer': 'JELLIOTT LIGHTS', 'revenue': 39.1}, {'customer': 'FW Webb Company - BR128 Elmwood Park, NJ', 'revenue': 34.8}, {'customer': 'Lightbulb Wholesaler Inc.', 'revenue': 34.54}, {'customer': 'ALLIED WHOLESALE', 'revenue': 30.4}, {'customer': 'Gross Lighting & Home dba Indiana Lighting Center', 'revenue': 28.47}, {'customer': 'LIGHTING CONNECTION', 'revenue': 27.06}, {'customer': 'NEENAS DESIGN LIGHTING', 'revenue': 26.97}, {'customer': 'LIGHT (WOOLF LIGHTING)', 'revenue': 26.94}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 23.7}, {'customer': 'BRAND NAME LIGHTING', 'revenue': 23.51}, {'customer': 'MADISON LIGHTING', 'revenue': 20.83}, {'customer': 'VILLA LIGHTING SUPPLY INC', 'revenue': 20.54}, {'customer': 'VALET ENERGY LLC', 'revenue': 20.48}, {'customer': 'LIGHTING GETZ CORP.', 'revenue': 19.44}, {'customer': 'PALETTE STUDIOS INC', 'revenue': 18.37}, {'customer': 'HOMESTYLES', 'revenue': 18.08}, {'customer': 'INCON INDUSTRIES', 'revenue': 16.91}, {'customer': 'PIONEER LIGHTING INC', 'revenue': 14.43}, {'customer': 'CREATIVE LIGHTING DESIGNS & DECOR LLC', 'revenue': 11.61}, {'customer': 'PINE TREE LIGHTING', 'revenue': 5.73}, {'customer': 'LIGHTING EFX', 'revenue': 2.7}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'NORTHERN LIGHTS & ACCENTS', 'revenue': 0.0}, {'customer': 'YALE ELECTRIC c/o USESI', 'revenue': 0.0}, {'customer': 'Greyed Brindle Design', 'revenue': 0.0}, {'customer': 'Bulbrite Industries Inc', 'revenue': 0.0}, {'customer': 'ILUMILA S.A.', 'revenue': 0.0}, {'customer': 'RAGLighting, Inc.', 'revenue': 0.0}, {'customer': 'LIGHTING DESIGN LLC', 'revenue': 0.0}, {'customer': 'CHL LIGHTING INC', 'revenue': 0.0}, {'customer': 'SAPPHIRE MANUFACTURING INC.', 'revenue': 0.0}, {'customer': 'LIGHTING CORNER', 'revenue': 0.0}, {'customer': 'AC Electric & Custom Design Lighting', 'revenue': 0.0}, {'customer': 'CANAL BULBS AND PARTS INC', 'revenue': 0.0}, {'customer': 'TEC OF N LITTLE ROCK INC', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY (ECOMM)', 'revenue': 0.0}, {'customer': 'UNBEATABLESALE.COM INC.', 'revenue': 0.0}, {'customer': 'Gross Lighting & Home - OH', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'LIGHT BULB DISTRICT, INC', 'revenue': 0.0}, {'customer': '303 LIGHTING INC.', 'revenue': 0.0}, {'customer': 'DRETZKA AND ASSOCIATES, INC.', 'revenue': 0.0}, {'customer': 'ILLUMINATE', 'revenue': 0.0}, {'customer': 'IWORKS LLC', 'revenue': 0.0}, {'customer': 'WOLFERS LIGHTING INC', 'revenue': 0.0}, {'customer': 'DLC LIGHTING', 'revenue': -7.8}, {'customer': 'DUPAGE LIGHTING INC', 'revenue': -13.5}] | [{'item': '774244', 'desc': 'LED8A19/B60W/830/1P', 'available': 242227}, {'item': '774263', 'desc': 'LED9A19/PF60W/930/D/2/1P', 'available': 171667}, {'item': '776214', 'desc': 'LED7A19/30K/FIL/D/B/2', 'available': 128216}, {'item': '776212', 'desc': 'LED7A19/27K/FIL/D/B/2', 'available': 85200}, {'item': '774243', 'desc': 'LED8A19/B60W/827/1P', 'available': 74194}, {'item': '774262', 'desc': 'LED9A19/PF60W/927/D/2/1P', 'available': 51010}, {'item': '774280', 'desc': 'LED9A19/P60W/927/J/D/2/1P', 'available': 47742}, {'item': '776756', 'desc': 'LED4B11/27K/FIL/4/JA8', 'available': 46077}, {'item': '776627', 'desc': 'LED5B11/30K/FIL/E12/3', 'available': 38110}, {'item': '776204', 'desc': 'LED5B11/30K/FIL/D/B/2', 'available': 36790}, {'item': '773117', 'desc': 'LED9REC/4/940/WHRD/D', 'available': 32447}, {'item': '776873', 'desc': 'LED4G16/27K/FIL/3', 'available': 31103}, {'item': '776626', 'desc': 'LED5B11/27K/FIL/E12/3', 'available': 30021}, {'item': '776216', 'desc': 'LED7A19/40K/FIL/D/B/2', 'available': 29245}, {'item': '776201', 'desc': 'LED4B11/30K/FIL/D/B/2', 'available': 24933}, {'item': '773231', 'desc': 'LED7JBOXDL/3/930/WHRD/D', 'available': 21266}, {'item': '776207', 'desc': 'LED5T9/30K/FIL/D/B/2', 'available': 21110}, {'item': '772870', 'desc': 'LED8BR30/827/D/4', 'available': 20542}, {'item': '776215', 'desc': 'LED7A19/30K/FIL/M/D/B/2', 'available': 20370}, {'item': '776200', 'desc': 'LED4B11/27K/FIL/D/B/2', 'available': 19940}, {'item': '776768', 'desc': 'LED8A19/30K/FIL/3/JA8', 'available': 19752}, {'item': '772857', 'desc': 'LED8BR30/830/D/5', 'available': 18274}, {'item': '773232', 'desc': 'LED7JBOXDL/3/940/WHRD/D', 'available': 17512}, {'item': '776774', 'desc': 'LED8A19/27K/FIL/3/JA8', 'available': 17363}, {'item': '773167', 'desc': 'LED14REC/5/6/940/WHRD/D', 'available': 16954}, {'item': '770579', 'desc': 'LED4G9/30K/120/D', 'available': 16521}, {'item': '776931', 'desc': 'LED5B11/40K/FIL/E12/3', 'available': 13584}, {'item': '776769', 'desc': 'LED8ST18/30K/FIL/3/JA8', 'available': 13486}, {'item': '776962', 'desc': 'LED4B11/50K/FIL/3', 'available': 13132}, {'item': '772253', 'desc': 'LED15PAR38/B-FL40/830/WD/2', 'available': 12921}, {'item': '776224', 'desc': 'LED7ST18/30K/FIL/D/B/2', 'available': 12603}, {'item': '776763', 'desc': 'LED4B11/30K/FIL/4/JA8', 'available': 11901}, {'item': '776987', 'desc': 'LED13ST18/50K/FIL/3', 'available': 11700}, {'item': '776985', 'desc': 'LED8ST18/50K/FIL/3', 'available': 11431}, {'item': '776937', 'desc': 'LED8A19/27K/FIL/M/4', 'available': 11147}, {'item': '774265', 'desc': 'LED9A19/PF60W/950/D/2/1P', 'available': 10427}, {'item': '774245', 'desc': 'LED8A19/B60W/840/1P', 'available': 10401}, {'item': '776964', 'desc': 'LED5B11/50K/FIL/3', 'available': 10398}, {'item': '776966', 'desc': 'LED6B11/50K/FIL/3', 'available': 10362}, {'item': '776684', 'desc': 'LED1S14/24K/FIL', 'available': 10279}, {'item': '776767', 'desc': 'LED8ST18/27K/FIL/3/JA8', 'available': 10262}, {'item': '774281', 'desc': 'LED9A19/P60W/930/J/D/2/1P', 'available': 10171}, {'item': '776685', 'desc': 'LED1S14/27K/FIL', 'available': 9202}, {'item': '773262', 'desc': 'LED14JBOXDL/6/940/WHRD/D', 'available': 8927}, {'item': '776859', 'desc': 'LED4CA10/27K/FIL/3', 'available': 8859}, {'item': '776791', 'desc': 'LED4T6/30K/FIL/3', 'available': 8768}, {'item': '776977', 'desc': 'LED8G25/40K/FIL/3/JA8', 'available': 8685}, {'item': '774232', 'desc': 'LED9A19/B60W/840/1P', 'available': 8516}, {'item': '776220', 'desc': 'LED7G25/30K/FIL/M/D/B/2', 'available': 8183}, {'item': '776935', 'desc': 'LED8ST18/40K/FIL/3/JA8', 'available': 8053}, {'item': '776930', 'desc': 'LED4B11/40K/FIL/3/JA8', 'available': 8002}, {'item': '776963', 'desc': 'LED4B11/50K/FIL/M/3', 'available': 7911}, {'item': '776965', 'desc': 'LED5B11/50K/FIL/M/3', 'available': 7867}, {'item': '776967', 'desc': 'LED6B11/50K/FIL/M/3', 'available': 7771}, {'item': '776979', 'desc': 'LED8G25/50K/FIL/3', 'available': 7734}, {'item': '776976', 'desc': 'LED5G25/30K/FIL/M/3', 'available': 7639}, {'item': '776968', 'desc': 'LED6B11/40K/FIL/M/3', 'available': 7585}, {'item': '776904', 'desc': 'LED2T6/21K/FIL-NOS/3', 'available': 7484}, {'item': '776974', 'desc': 'LED5G25/27K/FIL/M/3', 'available': 7448}, {'item': '772245', 'desc': 'LED10PAR30S/B-FL40/830/WD/2', 'available': 7170}, {'item': '772254', 'desc': 'LED15PAR38/B-FL40/840/WD/2', 'available': 7138}, {'item': '776958', 'desc': 'LED8A19/50K/FIL/3', 'available': 7119}, {'item': '774267', 'desc': 'LED11A19/PF75W/930/D/2/1P', 'available': 7093}, {'item': '776203', 'desc': 'LED5B11/27K/FIL/D/B/2', 'available': 7031}, {'item': '773165', 'desc': 'LED14REC/5/6/927/WHRD/D', 'available': 6752}, {'item': '770191', 'desc': 'LED/C9C', 'available': 6725}, {'item': '776973', 'desc': 'LED5G25/27K/FIL/3', 'available': 6691}, {'item': '776945', 'desc': 'LED5T9L/27K/11/FIL/4', 'available': 6516}, {'item': '776732', 'desc': 'LED5T9/30K/5/FIL/4/JA8', 'available': 6468}, {'item': '774248', 'desc': 'LED8A19/B60W/830/4P', 'available': 6392}, {'item': '770595', 'desc': 'LED4E12/27K/120/D', 'available': 6243}, {'item': '776781', 'desc': 'LED5T9/27K/5/FIL/F/3', 'available': 6238}, {'item': '776223', 'desc': 'LED7ST18/27K/FIL/D/B/2', 'available': 6173}, {'item': '776975', 'desc': 'LED5G25/30K/FIL/3', 'available': 6138}, {'item': '776593', 'desc': 'LED4C15/21K/FIL/SPUN/AMB', 'available': 5879}, {'item': '776991', 'desc': 'LED5T9/50K/5/FIL/3', 'available': 5805}, {'item': '776402', 'desc': 'LED5CA10/30K-18K/WMDM/FIL/M', 'available': 5760}, {'item': '776980', 'desc': 'LED8G25/50K/FIL/M/3', 'available': 5759}, {'item': '776936', 'desc': 'LED13ST18/40K/FIL/3/JA8', 'available': 5688}, {'item': '776969', 'desc': 'LED5CA10/27K/FIL/E26/3', 'available': 5619}, {'item': '776960', 'desc': 'LED14A19/50K/FIL/3', 'available': 5594}, {'item': '776978', 'desc': 'LED8G25/40K/FIL/M/3', 'available': 5589}, {'item': '773272', 'desc': 'LED18JBOXDL/8/940/WHRD/D', 'available': 5540}, {'item': '776405', 'desc': 'LED9ST18/30K-18K/WMDM/FIL/M', 'available': 5471}, {'item': '773260', 'desc': 'LED14JBOXDL/6/927/WHRD/D', 'available': 5418}, {'item': '776780', 'desc': 'LED4T6/27K/FIL/3', 'available': 5254}, {'item': '776949', 'desc': 'LED3T9/30K/7/FIL/4', 'available': 5211}, {'item': '776951', 'desc': 'LED2T6/27K/FIL/3', 'available': 5170}, {'item': '776952', 'desc': 'LED2T6/30K/FIL/4', 'available': 5158}, {'item': '776592', 'desc': 'LED4C15/27K/FIL/SPUN/SAT', 'available': 5154}, {'item': '772302', 'desc': 'LED15PAR38/FL40/930/WD/2', 'available': 5122}, {'item': '776581', 'desc': 'LED4F15/21K/FIESTA/AMB', 'available': 5089}, {'item': '773240', 'desc': 'LED9JBOXDL/4/927/WHRD/D', 'available': 4978}, {'item': '772877', 'desc': 'LED15BR40/830/D/4', 'available': 4964}, {'item': '776219', 'desc': 'LED7G25/30K/FIL/D/B/2', 'available': 4860}, {'item': '776953', 'desc': 'LED2A19/27K/FIL/M/3', 'available': 4834}, {'item': '773210', 'desc': 'LED9JBOXDL/4/827/WHRD/D', 'available': 4829}, {'item': '776914', 'desc': 'LED9A19/30K/FIL/4', 'available': 4825}, {'item': '776959', 'desc': 'LED8A19/50K/FIL/M/3', 'available': 4815}, {'item': '776872', 'desc': 'LED5A19/27K/FIL/3', 'available': 4807}, {'item': '776989', 'desc': 'LED5T9/40K/5/FIL/3/JA8', 'available': 4806}, {'item': '776205', 'desc': 'LED5B11/40K/FIL/D/B/2', 'available': 4740}, {'item': '776902', 'desc': 'LED4A19/21K/FIL-NOS/3', 'available': 4729}, {'item': '776749', 'desc': 'LED8G25/27K/FIL/4/JA8', 'available': 4726}, {'item': '776206', 'desc': 'LED5T9/27K/FIL/D/B/2', 'available': 4718}, {'item': '776840', 'desc': 'LED6G40/27K/FIL/HW/3', 'available': 4647}, {'item': '776836', 'desc': 'LED6G40/27K/FIL/HB/3', 'available': 4647}, {'item': '776837', 'desc': 'LED5A19/27K/FIL/HW/3', 'available': 4522}, {'item': '776862', 'desc': 'LED4B11/27K/FIL/E26/3', 'available': 4453}, {'item': '776731', 'desc': 'LED5T9/27K/5/FIL/4/JA8', 'available': 4452}, {'item': '776833', 'desc': 'LED5A19/27K/FIL/HB/3', 'available': 4382}, {'item': '776580', 'desc': 'LED4F15/27K/FIESTA/CLR', 'available': 4348}, {'item': '776719', 'desc': 'LED5T9L/21K/15/FIL-NOS/3', 'available': 4325}, {'item': '776225', 'desc': 'LED7ST18/40K/FIL/D/B/2', 'available': 4199}, {'item': '776906', 'desc': 'LED2G16/21K/FIL-NOS/3', 'available': 4189}, {'item': '773221', 'desc': 'LED14JBOXDL/6/830/WHRD/D', 'available': 4186}, {'item': '771109', 'desc': 'LED6PAR16GUFL40/50/930/J/D/2', 'available': 4184}, {'item': '771086', 'desc': 'LED6MR16FL40/50/930/J/D/5', 'available': 4165}, {'item': '772246', 'desc': 'LED10PAR30S/B-FL40/840/WD/2', 'available': 4155}, {'item': '772856', 'desc': 'LED8BR30/827/D/5', 'available': 4138}, {'item': '776925', 'desc': 'LED8A19/40K/FIL/3/JA8', 'available': 4089}, {'item': '772242', 'desc': 'LED7PAR20/B-FL40/830/WD/2', 'available': 4049}, {'item': '771088', 'desc': 'LED7MR16FL40/75/930/J/D/2', 'available': 3955}, {'item': '776839', 'desc': 'LED5G25/27K/FIL/HW/3', 'available': 3940}, {'item': '776970', 'desc': 'LED5CA10/27K/FIL/E26/M/3', 'available': 3938}, {'item': '776992', 'desc': 'LED5T9/50K/5/FIL/F/3', 'available': 3902}, {'item': '776217', 'desc': 'LED7G25/27K/FIL/D/B/2', 'available': 3894}, {'item': '776982', 'desc': 'LED8G40/40K/FIL/M/3', 'available': 3881}, {'item': '776990', 'desc': 'LED5T9/40K/5/FIL/F/3', 'available': 3854}, {'item': '776832', 'desc': 'LED7A15/30K/FIL/M/3', 'available': 3831}, {'item': '776838', 'desc': 'LED2G16/27K/FIL/HW/3', 'available': 3791}, {'item': '772243', 'desc': 'LED7PAR20/B-FL40/840/WD/2', 'available': 3727}, {'item': '776981', 'desc': 'LED8G40/40K/FIL/3', 'available': 3726}, {'item': '776988', 'desc': 'LED6B11/30K/FIL/M/3', 'available': 3692}, {'item': '773271', 'desc': 'LED18JBOXDL/8/930/WHRD/D', 'available': 3675}, {'item': '776404', 'desc': 'LED9G25/30K-18K/WMDM/FIL/M', 'available': 3629}, {'item': '776744', 'desc': 'LED4G16/30K/FIL/4/JA8', 'available': 3590}, {'item': '776995', 'desc': 'LED4T6/50K/FIL/3', 'available': 3553}, {'item': '776986', 'desc': 'LED6B11/27K/FIL/M/3', 'available': 3541}, {'item': '776864', 'desc': 'LED4CA10/30K/FIL/3', 'available': 3495}, {'item': '776913', 'desc': 'LED9A19/27K/FIL/4', 'available': 3479}, {'item': '776829', 'desc': 'LED7A15/27K/FIL/3', 'available': 3434}, {'item': '774269', 'desc': 'LED15A19/P100W/930/J/D/2/1P', 'available': 3381}, {'item': '776938', 'desc': 'LED2B11/27K/FIL/4', 'available': 3374}, {'item': '771085', 'desc': 'LED6MR16FL40/50/927/J/D/5', 'available': 3361}, {'item': '776514', 'desc': 'LED4A19/21K/FIL-NOS/CURV/LOOP', 'available': 3346}, {'item': '774264', 'desc': 'LED9A19/PF60W/940/D/2/1P', 'available': 3333}, {'item': '776835', 'desc': 'LED5G25/27K/FIL/HB/3', 'available': 3331}, {'item': '776221', 'desc': 'LED7G25/40K/FIL/D/B/2', 'available': 3310}, {'item': '776743', 'desc': 'LED4G16/27K/FIL/4/JA8', 'available': 3301}, {'item': '773222', 'desc': 'LED14JBOXDL/6/840/WHRD/D', 'available': 3290}, {'item': '770195', 'desc': 'LED/C9O', 'available': 3261}, {'item': '776834', 'desc': 'LED2G16/27K/FIL/HB/3', 'available': 3187}, {'item': '772764', 'desc': 'LED10PAR30S/FL40/827/WD/2', 'available': 3177}, {'item': '776943', 'desc': 'LED4G16/27K/FIL/M/4', 'available': 3159}, {'item': '776897', 'desc': 'LED8G40/27K/FIL/M/3', 'available': 3156}, {'item': '776726', 'desc': 'LED5T9/30K/7/FIL/F/3', 'available': 3100}, {'item': '774285', 'desc': 'LED5/9/14A19/PF100W/827/3WAY/1P', 'available': 3098}, {'item': '776725', 'desc': 'LED5T9/27K/7/FIL/F/3', 'available': 3091}, {'item': '776721', 'desc': 'LED5T9L/30K/15/FIL/3', 'available': 3090}, {'item': '776591', 'desc': 'LED4C11/21K/FIL/SPUN/AMB', 'available': 3057}, {'item': '770598', 'desc': 'LED3G9/30K/W/D', 'available': 3052}, {'item': '770591', 'desc': 'LED4G9/27K/120/F/D', 'available': 3031}, {'item': '772286', 'desc': 'LED10PAR30L/FL40/927/WD/2', 'available': 3030}, {'item': '776858', 'desc': 'LED2CA10/27K/FIL/E12/3', 'available': 3009}, {'item': '772861', 'desc': 'LED15BR40/830/D/5', 'available': 3005}, {'item': '772248', 'desc': 'LED10PAR30L/B-FL40/830/WD/2', 'available': 3002}, {'item': '772859', 'desc': 'LED11BR30/830/D/5', 'available': 3002}, {'item': '770614', 'desc': 'LED1/FEST/27K/24/2', 'available': 2986}, {'item': '776961', 'desc': 'LED14A19/50K/FIL/M/3', 'available': 2979}, {'item': '776773', 'desc': 'LED4B11/30K/FIL/M/3', 'available': 2935}, {'item': '776713', 'desc': 'LED5T9/21K/7/FIL-NOS/3', 'available': 2900}, {'item': '776321', 'desc': 'LED4C53/30K/FIL/GRAD/SMK', 'available': 2891}, {'item': '776825', 'desc': 'LED4A15/27K/FIL/E12/3', 'available': 2861}, {'item': '776933', 'desc': 'LED4B11/40K/FIL/M/3', 'available': 2849}, {'item': '776950', 'desc': 'LED2S14/27K/FIL/4', 'available': 2820}, {'item': '776594', 'desc': 'LED4T6SL/27K/FIL/3', 'available': 2783}, {'item': '776934', 'desc': 'LED5B11/40K/FIL/M/3', 'available': 2781}, {'item': '776928', 'desc': 'LED7A19/40K/FIL/M/3', 'available': 2759}, {'item': '774279', 'desc': 'LED15A19/P100W/930/GU24/J/D/1P', 'available': 2755}, {'item': '774266', 'desc': 'LED11A19/PF75W/927/D/2/1P', 'available': 2739}, {'item': '770171', 'desc': 'LED/C7C', 'available': 2738}, {'item': '770637', 'desc': 'LED6R7S/30K/S/D', 'available': 2731}, {'item': '774286', 'desc': 'LED5/9/14A19/PF100W/830/3WAY/1P', 'available': 2692}, {'item': '772265', 'desc': 'LED6PAR20/NFL25/930/WD/2', 'available': 2689}, {'item': '776929', 'desc': 'LED14A19/40K/FIL/M/3', 'available': 2653}, {'item': '776712', 'desc': 'LED4G16/30K/FIL/M/3', 'available': 2647}, {'item': '776917', 'desc': 'LED9A19/27K/FIL/M/4', 'available': 2622}, {'item': '776108', 'desc': 'LED4A19/GRN/FIL/D', 'available': 2607}, {'item': '773170', 'desc': 'LED9REC/4/927/WHRD-G/D', 'available': 2585}, {'item': '776742', 'desc': 'LED5CA10/30K/FIL/4/JA8', 'available': 2573}, {'item': '776521', 'desc': 'LED11A19/30K/FIL/3WAY', 'available': 2561}, {'item': '776926', 'desc': 'LED9A19/40K/FIL/3', 'available': 2538}, {'item': '776741', 'desc': 'LED5CA10/27K/FIL/4/JA8', 'available': 2528}, {'item': '770586', 'desc': 'LED2G4/27K/12', 'available': 2517}, {'item': '776151', 'desc': 'LED2S14/AMB/FIL/D', 'available': 2514}, {'item': '770596', 'desc': 'LED4E12/27K/120/F/D', 'available': 2498}, {'item': '776218', 'desc': 'LED7G25/27K/FIL/M/D/B/2', 'available': 2470}, {'item': '776208', 'desc': 'LED7A15/27K/FIL/D/B/2', 'available': 2445}, {'item': '773180', 'desc': 'LED14REC/5/6/927/WHRD-G/D', 'available': 2436}, {'item': '771087', 'desc': 'LED7MR16FL40/75/927/J/D/2', 'available': 2420}, {'item': '770580', 'desc': 'LED4G9/30K/120/F/D', 'available': 2389}, {'item': '773181', 'desc': 'LED14REC/5/6/930/WHRD-G/D', 'available': 2354}, {'item': '776106', 'desc': 'LED4A19/AMB/FIL/D', 'available': 2350}, {'item': '776110', 'desc': 'LED4A19/PNK/FIL/D', 'available': 2347}, {'item': '770583', 'desc': 'LED2WEDGE/30K/12', 'available': 2339}, {'item': '776994', 'desc': 'LED4T6/40K/FIL/M/3', 'available': 2339}, {'item': '770613', 'desc': 'LED1/FEST/30K/24/2', 'available': 2327}, {'item': '776954', 'desc': 'LED5A19/27K/FIL/M/3', 'available': 2326}, {'item': '773242', 'desc': 'LED9JBOXDL/4/940/WHRD/D', 'available': 2320}, {'item': '776516', 'desc': 'LED4G25/21K/FIL-NOS/CURV/SPIRAL', 'available': 2296}, {'item': '776909', 'desc': 'LED7ST18/21K/FIL-NOS/3', 'available': 2288}, {'item': '776927', 'desc': 'LED14A19/40K/FIL/3', 'available': 2255}, {'item': '770638', 'desc': 'LED10R7S/30K/L/D', 'available': 2251}, {'item': '776520', 'desc': 'LED11A19/27K/FIL/3WAY', 'available': 2237}, {'item': '776801', 'desc': 'LED5ST18/22K/FIL-NOS/3', 'available': 2232}, {'item': '776403', 'desc': 'LED5G16/30K-18K/WMDM/FIL/M', 'available': 2228}, {'item': '770626', 'desc': 'LED5GY6/30K/12', 'available': 2226}, {'item': '776922', 'desc': 'LED9A19/30K/FIL/M/4', 'available': 2220}, {'item': '776228', 'desc': 'LED7A19/40K/FIL/D/B/2/4P', 'available': 2211}, {'item': '776720', 'desc': 'LED5T9L/27K/15/FIL/3', 'available': 2200}, {'item': '773241', 'desc': 'LED9JBOXDL/4/930/WHRD/D', 'available': 2188}, {'item': '772261', 'desc': 'LED6PAR20/NFL25/927/WD/2', 'available': 2141}, {'item': '776213', 'desc': 'LED7A19/27K/FIL/M/D/B/2', 'available': 2116}, {'item': '776948', 'desc': 'LED3T9/27K/7/FIL/4', 'available': 2111}, {'item': '770648', 'desc': 'LED5G9/30K/120/D/2', 'available': 2066}, {'item': '776916', 'desc': 'LED14A19/30K/FIL/3', 'available': 2042}, {'item': '776918', 'desc': 'LED14A19/27K/FIL/M/3', 'available': 2031}, {'item': '770611', 'desc': 'LED1/FEST/30K/12/2', 'available': 2019}, {'item': '776231', 'desc': 'LED4B11/40K/FIL/D/B/2/6P', 'available': 2018}, {'item': '770196', 'desc': 'LED/C9P', 'available': 2015}, {'item': '772249', 'desc': 'LED10PAR30L/B-FL40/840/WD/2', 'available': 2010}, {'item': '770630', 'desc': 'LED5E11/30K/120/D', 'available': 1992}, {'item': '776972', 'desc': 'LED5CA10/30K/FIL/E26/M/3', 'available': 1971}, {'item': '776996', 'desc': 'LED4T6/50K/FIL/M/3', 'available': 1954}, {'item': '770619', 'desc': 'LED4DC/30K/D', 'available': 1947}, {'item': '776941', 'desc': 'LED5B11/30K/FIL/M/4', 'available': 1934}, {'item': '776932', 'desc': 'LED6B11/40K/FIL/3', 'available': 1928}, {'item': '776983', 'desc': 'LED8G40/50K/FIL/3', 'available': 1927}, {'item': '776824', 'desc': 'LED4ST15/30K/FIL/M/3', 'available': 1925}, {'item': '770597', 'desc': 'LED3G9/27K/W/D', 'available': 1912}, {'item': '776750', 'desc': 'LED8G25/30K/FIL/4/JA8', 'available': 1904}, {'item': '776984', 'desc': 'LED8G40/50K/FIL/M/3', 'available': 1894}, {'item': '776785', 'desc': 'LED1S14/27K/FIL/PL', 'available': 1892}, {'item': '770625', 'desc': 'LED5GY6/27K/12', 'available': 1885}, {'item': '772610', 'desc': 'LED18PAR38/FL40/927/J/WD', 'available': 1866}, {'item': '774246', 'desc': 'LED8A19/B60W/850/1P', 'available': 1866}, {'item': '776109', 'desc': 'LED4A19/BLU/FIL/D', 'available': 1856}, {'item': '770624', 'desc': 'LED4G4/30K/12', 'available': 1855}, {'item': '776322', 'desc': 'LED4C53/30K/FIL/GRAD/BLU', 'available': 1849}, {'item': '770577', 'desc': 'LED3G9/30K/120', 'available': 1842}, {'item': '776827', 'desc': 'LED4A15/27K/FIL/M/E12/3', 'available': 1838}, {'item': '772876', 'desc': 'LED15BR40/827/D/4', 'available': 1811}, {'item': '770622', 'desc': 'LED3G4/WA/27K/12', 'available': 1811}, {'item': '776942', 'desc': 'LED4CA10/27K/FIL/M/3', 'available': 1809}, {'item': '770650', 'desc': 'LED2G4/30K/W/D', 'available': 1802}, {'item': '770589', 'desc': 'LED3G9/27K/120', 'available': 1801}, {'item': '776971', 'desc': 'LED5CA10/30K/FIL/E26/3', 'available': 1798}, {'item': '776920', 'desc': 'LED6G40/27K/FIL/HM/3', 'available': 1783}, {'item': '770658', 'desc': 'LED4G9/30K/W/F/D', 'available': 1770}, {'item': '773171', 'desc': 'LED9REC/4/930/WHRD-G/D', 'available': 1761}, {'item': '773270', 'desc': 'LED18JBOXDL/8/927/WHRD/D', 'available': 1754}, {'item': '776993', 'desc': 'LED4T6/40K/FIL/3', 'available': 1628}, {'item': '773115', 'desc': 'LED9REC/4/927/WHRD/D', 'available': 1613}, {'item': '776878', 'desc': 'LED8G40/27K/FIL/3', 'available': 1606}, {'item': '776861', 'desc': 'LED4CA10/30K/FIL/M/3', 'available': 1560}, {'item': '776831', 'desc': 'LED7A15/27K/FIL/M/3', 'available': 1523}, {'item': '771105', 'desc': 'LED6PAR16FL40/50/830/D/5', 'available': 1516}, {'item': '770643', 'desc': 'LED6E12/30K/120/D', 'available': 1512}, {'item': '776899', 'desc': 'LED8G40/30K/FIL/M/3', 'available': 1511}, {'item': '776997', 'desc': 'LED4G40/30K/FIL/GRAD/SMK', 'available': 1508}, {'item': '776823', 'desc': 'LED4ST15/27K/FIL/M/3', 'available': 1502}, {'item': '776903', 'desc': 'LED2CA10/21K/FIL-NOS/3', 'available': 1501}, {'item': '772860', 'desc': 'LED15BR40/827/D/5', 'available': 1488}, {'item': '770645', 'desc': 'LED6G9/30K/120/D', 'available': 1483}, {'item': '772301', 'desc': 'LED15PAR38/NF25/930/WD/2', 'available': 1478}, {'item': '776105', 'desc': 'LED4A19/RED/FIL/D', 'available': 1475}, {'item': '770652', 'desc': 'LED2G4/30K/W/F/D', 'available': 1471}, {'item': '772855', 'desc': 'LED7BR20/830/D/5', 'available': 1471}, {'item': '776746', 'desc': 'LED13ST18/30K/FIL/3/JA8', 'available': 1470}, {'item': '773220', 'desc': 'LED14JBOXDL/6/827/WHRD/D', 'available': 1467}, {'item': '774249', 'desc': 'LED8A19/B60W/840/4P', 'available': 1454}, {'item': '771117', 'desc': 'LED6PAR16FL40/50/830/D/4', 'available': 1449}, {'item': '776946', 'desc': 'LED5T9L/30K/11/FIL/4', 'available': 1448}, {'item': '776722', 'desc': 'LED4T8/21K/FIL-NOS/3', 'available': 1443}, {'item': '776870', 'desc': 'LED5G25/27K/FIL/HM/3', 'available': 1423}, {'item': '776707', 'desc': 'LED5T9L/21K/11/FIL-NOS/3', 'available': 1422}, {'item': '776828', 'desc': 'LED4A15/30K/FIL/M/E12/3', 'available': 1417}, {'item': '776241', 'desc': 'LED7G25/40K/FIL/D/B/2/4P', 'available': 1417}, {'item': '770612', 'desc': 'LED1/FEST/27K/12/2', 'available': 1409}, {'item': '772768', 'desc': 'LED10PAR30S/FL40/830/WD/2', 'available': 1408}, {'item': '776915', 'desc': 'LED14A19/27K/FIL/3', 'available': 1385}, {'item': '776237', 'desc': 'LED5B11/27K/FIL/D/B/2/25P', 'available': 1385}, {'item': '776826', 'desc': 'LED4A15/30K/FIL/E12/3', 'available': 1384}, {'item': '776800', 'desc': 'LED5G25/22K/FIL-NOS/3', 'available': 1379}, {'item': '776944', 'desc': 'LED8G25/27K/FIL/M/3', 'available': 1362}, {'item': '776229', 'desc': 'LED4B11/27K/FIL/D/B/2/6P', 'available': 1362}, {'item': '773152', 'desc': 'LED20DL/9/927/WHRD/J/D', 'available': 1359}, {'item': '772502', 'desc': 'LED15PAR38/FL/YLW/D', 'available': 1353}, {'item': '776232', 'desc': 'LED5B11/27K/FIL/D/B/2/6P', 'available': 1338}, {'item': '770651', 'desc': 'LED2G4/27K/W/F/D', 'available': 1336}, {'item': '776234', 'desc': 'LED5B11/40K/FIL/D/B/2/6P', 'available': 1333}, {'item': '776401', 'desc': 'LED5B11/30K-18K/WMDM/FIL/M', 'available': 1330}, {'item': '770576', 'desc': 'LED4GY8/30K/120/D', 'available': 1322}, {'item': '776406', 'desc': 'LED4G40/30K-18K/WMDM/FIL/M', 'available': 1319}, {'item': '776939', 'desc': 'LED4B11/27K/FIL/M/3', 'available': 1318}, {'item': '776730', 'desc': 'LED4T6/30K/FIL/M/3', 'available': 1316}, {'item': '776235', 'desc': 'LED4B11/27K/FIL/D/B/2/25P', 'available': 1314}, {'item': '776734', 'desc': 'LED5B11/30K/FIL/E26/3', 'available': 1299}, {'item': '774247', 'desc': 'LED8A19/B60W/827/4P', 'available': 1299}, {'item': '770604', 'desc': 'LED/LI4T8/27K', 'available': 1285}, {'item': '772854', 'desc': 'LED7BR20/827/D/5', 'available': 1280}, {'item': '772505', 'desc': 'LED15PAR38/FL/PNK/D', 'available': 1268}, {'item': '776738', 'desc': 'LED6B11/30K/FIL/3', 'available': 1266}, {'item': '772503', 'desc': 'LED15PAR38/FL/GRN/D', 'available': 1261}, {'item': '776830', 'desc': 'LED7A15/30K/FIL/3', 'available': 1256}, {'item': '776740', 'desc': 'LED6CA10/30K/FIL/3', 'available': 1253}, {'item': '776919', 'desc': 'LED14A19/30K/FIL/M/3', 'available': 1248}, {'item': '770585', 'desc': 'LED4E12/30K/120/F/D', 'available': 1242}, {'item': '776787', 'desc': 'LED5CA10/27K/FIL/M/3', 'available': 1240}, {'item': '772290', 'desc': 'LED10PAR30L/FL40/930/WD/2', 'available': 1233}, {'item': '773146', 'desc': 'LED15DL/7/927/WHSQ/J/D', 'available': 1216}, {'item': '776595', 'desc': 'LED4T6SL/30K/FIL/3', 'available': 1216}, {'item': '772278', 'desc': 'LED10PAR30S/FL40/930/WD/2', 'available': 1207}, {'item': '776239', 'desc': 'LED7G25/27K/FIL/D/B/2/4P', 'available': 1201}, {'item': '776748', 'desc': 'LED13G25/30K/FIL/3/JA8', 'available': 1200}, {'item': '776238', 'desc': 'LED5B11/30K/FIL/D/B/2/25P', 'available': 1199}, {'item': '770593', 'desc': 'LED4E11/27K/120/F/D', 'available': 1195}, {'item': '770581', 'desc': 'LED4E11/30K/120/D', 'available': 1182}, {'item': '776921', 'desc': 'LED2G16/27K/FIL/HG/3', 'available': 1179}, {'item': '772274', 'desc': 'LED10PAR30S/FL40/927/WD/2', 'available': 1176}, {'item': '772500', 'desc': 'LED15PAR38/FL/RED/D', 'available': 1169}, {'item': '771108', 'desc': 'LED6PAR16GUFL40/50/927/J/D/2', 'available': 1165}, {'item': '776210', 'desc': 'LED7A15/30K/FIL/D/B/2', 'available': 1145}, {'item': '770623', 'desc': 'LED4G4/27K/12', 'available': 1136}, {'item': '776107', 'desc': 'LED4A19/YLW/FIL/D', 'available': 1135}, {'item': '772504', 'desc': 'LED15PAR38/FL/BLU/D', 'available': 1124}, {'item': '774240', 'desc': 'LED9A19/P60W/940/J/D/1P', 'available': 1123}, {'item': '776735', 'desc': 'LED5B11/27K/FIL/M/E26/3', 'available': 1120}, {'item': '776226', 'desc': 'LED7A19/27K/FIL/D/B/2/4P', 'available': 1113}, {'item': '772858', 'desc': 'LED11BR30/827/D/5', 'available': 1094}, {'item': '776306', 'desc': 'LED4OLIVE/22K/FIL', 'available': 1089}, {'item': '776747', 'desc': 'LED13G25/27K/FIL/3/JA8', 'available': 1071}, {'item': '770152', 'desc': 'LED/G14G', 'available': 1049}, {'item': '773125', 'desc': 'LED11JBOXDL/6/827/WHRD/D', 'available': 1038}, {'item': '776318', 'desc': 'LED4JEWEL/20K/FIL-NOS', 'available': 1037}, {'item': '774254', 'desc': 'LED9A19/PF60W/930/D/2/4P', 'available': 1035}, {'item': '772865', 'desc': 'LED7R20/830/D/4', 'available': 1013}, {'item': '772298', 'desc': 'LED15PAR38/FL40/927/WD/2', 'available': 994}, {'item': '774253', 'desc': 'LED9A19/PF60W/927/D/2/4P', 'available': 984}, {'item': '776153', 'desc': 'LED2S14/GRN/FIL/D', 'available': 983}, {'item': '774256', 'desc': 'LED9A19/PF60W/950/D/2/4P', 'available': 982}, {'item': '776209', 'desc': 'LED7A15/27K/FIL/M/D/B/2', 'available': 967}, {'item': '774250', 'desc': 'LED8A19/B60W/850/4P', 'available': 964}, {'item': '776792', 'desc': 'LED5T9/30K/5/FIL/F/3', 'available': 963}, {'item': '770594', 'desc': 'LED2WEDGE/27K/12', 'available': 961}, {'item': '774283', 'desc': 'LED9A19/P60W/927/GU24/J/D/2/1P', 'available': 958}, {'item': '776222', 'desc': 'LED7G25/40K/FIL/M/D/B/2', 'available': 941}, {'item': '776737', 'desc': 'LED6B11/27K/FIL/3', 'available': 939}, {'item': '776400', 'desc': 'LED9A19/30K-18K/WMDM/FIL/M', 'available': 930}, {'item': '770599', 'desc': 'LED4G9/27K/W/D', 'available': 929}, {'item': '776879', 'desc': 'LED8G40/30K/FIL/3', 'available': 928}, {'item': '772501', 'desc': 'LED15PAR38/FL/AMB/D', 'available': 917}, {'item': '770641', 'desc': 'LED6E11/30K/120/D', 'available': 905}, {'item': '770620', 'desc': 'LED4DC/27K/D', 'available': 888}, {'item': '776819', 'desc': 'LED5T14/27K/FIL/3', 'available': 884}, {'item': '776155', 'desc': 'LED2S14/PNK/FIL/D', 'available': 861}, {'item': '770616', 'desc': 'LED4GY6/27K/D/2', 'available': 860}, {'item': '770584', 'desc': 'LED4E12/30K/120/D', 'available': 849}, {'item': '770600', 'desc': 'LED4G9/30K/W/D', 'available': 848}, {'item': '770660', 'desc': 'LED3G9/30K/W/F/D', 'available': 837}, {'item': '776728', 'desc': 'LED5T9/30K/11/FIL/F/3', 'available': 834}, {'item': '770656', 'desc': 'LED2GY6/30K/12/W/F/D', 'available': 827}, {'item': '776924', 'desc': 'LED6G40/27K/FIL/HG/3', 'available': 826}, {'item': '776998', 'desc': 'LED4G40/30K/FIL/GRAD/BLU', 'available': 806}, {'item': '776739', 'desc': 'LED6CA10/27K/FIL/3', 'available': 799}, {'item': '776317', 'desc': 'LED4DROP/20K/FIL-NOS', 'available': 796}, {'item': '776243', 'desc': 'LED7ST18/30K/FIL/D/B/2/4P', 'available': 793}, {'item': '770632', 'desc': 'LED5E12/30K/120/D', 'available': 785}, {'item': '776515', 'desc': 'LED3ST18/21K/FIL-NOS/CURV/HAIRPIN', 'available': 780}, {'item': '772767', 'desc': 'LED10PAR30S/NF25/830/WD/2', 'available': 756}, {'item': '770629', 'desc': 'LED5E11/27K/120/D', 'available': 755}, {'item': '776771', 'desc': 'LED2G16/27K/FIL/HM/3', 'available': 755}, {'item': '776820', 'desc': 'LED5T14/30K/FIL/3', 'available': 735}, {'item': '776152', 'desc': 'LED2S14/YLW/FIL/D', 'available': 732}, {'item': '770649', 'desc': 'LED2G4/27K/W/D', 'available': 731}, {'item': '774251', 'desc': 'LED8A19/B60W/827/25P', 'available': 725}, {'item': '776101', 'desc': 'LED27T5/48/840/DIR', 'available': 723}, {'item': '770571', 'desc': 'LED2G4/30K/12', 'available': 715}, {'item': '776810', 'desc': 'LED8G25/30K/FIL/M/3', 'available': 714}, {'item': '776150', 'desc': 'LED2S14/RED/FIL/D', 'available': 688}, {'item': '774242', 'desc': 'LED9A19/P60W/930/GU24/J/D/1P', 'available': 679}, {'item': '770587', 'desc': 'LED3G4/27K/12', 'available': 664}, {'item': '772792', 'desc': 'LED15PAR38/FL40/830/WD/2', 'available': 662}, {'item': '770647', 'desc': 'LED5G9/27K/120/D/2', 'available': 655}, {'item': '770653', 'desc': 'LED2GY6/27K/12/W/D', 'available': 654}, {'item': '776706', 'desc': 'LED2G16/27K/FIL/3', 'available': 641}, {'item': '772775', 'desc': 'LED10PAR30L/NF25/827/WD/2', 'available': 641}, {'item': '776908', 'desc': 'LED3T9/21K/FIL-NOS/3', 'available': 638}, {'item': '776923', 'desc': 'LED4G25/27K/FIL/HG/3', 'available': 633}, {'item': '776230', 'desc': 'LED4B11/30K/FIL/D/B/2/6P', 'available': 631}, {'item': '776154', 'desc': 'LED2S14/BLU/FIL/D', 'available': 618}, {'item': '776005', 'desc': 'LED20T8/30K', 'available': 616}, {'item': '770590', 'desc': 'LED4G9/27K/120/D', 'available': 608}, {'item': '776242', 'desc': 'LED7ST18/27K/FIL/D/B/2/4P', 'available': 605}, {'item': '776822', 'desc': 'LED4ST15/30K/FIL/3', 'available': 599}, {'item': '770654', 'desc': 'LED2GY6/30K/12/W/D', 'available': 595}, {'item': '774258', 'desc': 'LED9A19/PF60W/930/D/2/25P', 'available': 567}, {'item': '776871', 'desc': 'LED2A19/27K/FIL/3', 'available': 561}, {'item': '776302', 'desc': 'LED4G63/22K/FIL', 'available': 559}, {'item': '776745', 'desc': 'LED13ST18/27K/FIL/3/JA8', 'available': 540}, {'item': '770631', 'desc': 'LED5E12/27K/120/D', 'available': 506}, {'item': '776854', 'desc': 'LED3T9/30K/FIL/3', 'available': 504}, {'item': '776940', 'desc': 'LED5B11/27K/FIL/M/4', 'available': 499}, {'item': '772262', 'desc': 'LED6PAR20/FL40/927/WD/2', 'available': 477}, {'item': '772779', 'desc': 'LED10PAR30L/NF25/830/WD/2', 'available': 469}, {'item': '770655', 'desc': 'LED2GY6/27K/12/W/F/D', 'available': 438}, {'item': '770621', 'desc': 'LED3G4/WA/30K/12', 'available': 434}, {'item': '770588', 'desc': 'LED4GY8/27K/120/D', 'available': 416}, {'item': '776211', 'desc': 'LED7A15/30K/FIL/M/D/B/2', 'available': 387}, {'item': '770194', 'desc': 'LED/C9G', 'available': 375}, {'item': '770618', 'desc': 'LED4SC/27K/12', 'available': 373}, {'item': '776233', 'desc': 'LED5B11/30K/FIL/D/B/2/6P', 'available': 369}, {'item': '770640', 'desc': 'LED6E11/27K/120/D', 'available': 367}, {'item': '776518', 'desc': 'LED4T14/21K/FIL-NOS/CURV/SPIRAL', 'available': 357}, {'item': '770644', 'desc': 'LED6G9/27K/120/D', 'available': 340}, {'item': '776679', 'desc': 'LED5A19/27K/FIL/HG/3', 'available': 328}, {'item': '776596', 'desc': 'LED4PRISM/30K/FIL/3', 'available': 296}, {'item': '772266', 'desc': 'LED6PAR20/FL40/930/WD/2', 'available': 276}, {'item': '776727', 'desc': 'LED5T9/27K/11/FIL/F/3', 'available': 269}, {'item': '772756', 'desc': 'LED7PAR20/FL40/830/WD/2', 'available': 265}, {'item': '773158', 'desc': 'LED20DL/9/927/WHSQ/J/D', 'available': 259}, {'item': '776821', 'desc': 'LED4ST15/27K/FIL/3', 'available': 258}, {'item': '776227', 'desc': 'LED7A19/30K/FIL/D/B/2/4P', 'available': 231}, {'item': '776240', 'desc': 'LED7G25/30K/FIL/D/B/2/4P', 'available': 197}, {'item': '776905', 'desc': 'LED4T14/21K/FIL-NOS/3', 'available': 190}, {'item': '774257', 'desc': 'LED9A19/PF60W/927/D/2/25P', 'available': 185}, {'item': '776788', 'desc': 'LED5CA10/30K/FIL/M/3', 'available': 179}, {'item': '776244', 'desc': 'LED7ST18/40K/FIL/D/B/2/4P', 'available': 155}, {'item': '774276', 'desc': 'LED15A19/P100W/927/J/D/1P', 'available': 150}, {'item': '776314', 'desc': 'LED4BT56/22K/FIL', 'available': 147}, {'item': '770659', 'desc': 'LED3G9/27K/W/F/D', 'available': 144}, {'item': '776736', 'desc': 'LED5B11/30K/FIL/M/E26/3', 'available': 140}, {'item': '770615', 'desc': 'LED4GY6/30K/D/2', 'available': 112}, {'item': '776305', 'desc': 'LED4DIA/22K/FIL', 'available': 86}, {'item': '772763', 'desc': 'LED10PAR30S/NF25/827/WD/2', 'available': 77}, {'item': '777801', 'desc': 'AC-CC-0002-00-S1', 'available': 74}, {'item': '777902', 'desc': 'SR111-18-36D-927-03', 'available': 68}, {'item': '776301', 'desc': 'LED4ET25/22K/FIL', 'available': 66}, {'item': '776304', 'desc': 'LED4BH/22K/FIL', 'available': 66}, {'item': '777252', 'desc': 'SP20-11-10D-927-03', 'available': 53}, {'item': '776300', 'desc': 'LED4PS52/22K/FIL', 'available': 51}, {'item': '777803', 'desc': 'AC-GC-2525-00-S1', 'available': 40}, {'item': '777809', 'desc': 'AC-FR-3636-00-S1', 'available': 35}, {'item': '777679', 'desc': 'SP38-14-60D-827-H1', 'available': 30}, {'item': '777823', 'desc': 'AC-E-GC-2525-00-S1', 'available': 25}, {'item': '772717', 'desc': 'LED7PAR20/NF25/840/WD', 'available': 23}, {'item': '771208', 'desc': 'LED6MR16FL35/50/830/D', 'available': 21}, {'item': '777766', 'desc': 'SP38-18-36D-930-03', 'available': 14}, {'item': '777700', 'desc': 'SP30L-18-09D-927-03', 'available': 12}, {'item': '777721', 'desc': 'SP30S-18-25D-927-03', 'available': 10}, {'item': '777681', 'desc': 'SP38-14-25D-830-H1', 'available': 10}, {'item': '774260', 'desc': 'LED11A19/PF75W/927/D/1P', 'available': 10}, {'item': '777661', 'desc': 'SP30L-14-25D-827-H1', 'available': 10}, {'item': '773230', 'desc': 'LED7JBOXDL/3/927/WHRD/D', 'available': 9}, {'item': '777827', 'desc': 'AC-E-GE-1036-00-S1', 'available': 9}, {'item': '776320', 'desc': 'LED4GLACIER/20K/FIL-NOS', 'available': 9}, {'item': '774252', 'desc': 'LED8A19/B60W/830/25P', 'available': 8}, {'item': '777707', 'desc': 'SP30L-18-60D-930-03', 'available': 6}, {'item': '777235', 'desc': 'SP20-11-36D-830-H1', 'available': 6}, {'item': '777764', 'desc': 'SP38-18-09D-930-03', 'available': 5}, {'item': '777579', 'desc': 'SM16GA-09-60D-930-03', 'available': 5}, {'item': '777046', 'desc': 'SM16-09-25D-827-H1', 'available': 4}, {'item': '777670', 'desc': 'SP30S-14-36D-827-H1', 'available': 4}, {'item': '777722', 'desc': 'SP30S-18-36D-927-03', 'available': 4}, {'item': '772776', 'desc': 'LED10PAR30L/FL40/827/WD/2', 'available': 3}, {'item': '777931', 'desc': 'SR111-12-25D-927-03', 'available': 3}, {'item': '777683', 'desc': 'SP38-14-60D-830-H1', 'available': 3}, {'item': '777532', 'desc': 'SM16GA-09-60D-827-H1', 'available': 3}, {'item': '777723', 'desc': 'SP30S-18-60D-927-03', 'available': 3}, {'item': '777660', 'desc': 'SP30L-14-09D-827-H1', 'available': 3}, {'item': '777760', 'desc': 'SP38-18-09D-927-03', 'available': 3}, {'item': '777253', 'desc': 'SP20-11-10D-930-03', 'available': 2}, {'item': '777265', 'desc': 'SP20-11-36D-930-03', 'available': 2}, {'item': '777576', 'desc': 'SM16GA-09-36D-927-03', 'available': 2}, {'item': '777726', 'desc': 'SP30S-18-36D-930-03', 'available': 2}, {'item': '777702', 'desc': 'SP30L-18-36D-927-03', 'available': 2}, {'item': '777814', 'desc': 'AC-E-AM-0020-00-S1', 'available': 2}, {'item': '777828', 'desc': 'AC-E-FR-3636-00-S1', 'available': 2}, {'item': '777059', 'desc': 'SM16-07-36D-930-03', 'available': 2}, {'item': '777821', 'desc': 'AC-E-CC-0002-00-S1', 'available': 1}, {'item': '777048', 'desc': 'SM16-09-25D-830-H1', 'available': 1}, {'item': '777767', 'desc': 'SP38-18-60D-930-03', 'available': 1}, {'item': '777802', 'desc': 'AC-CC-0003-00-S1', 'available': 1}, {'item': '777673', 'desc': 'SP30S-14-25D-830-H1', 'available': 1}, {'item': '777815', 'desc': 'AC-E-EN-0001-00-S1', 'available': 1}, {'item': '777259', 'desc': 'SP20-11-25D-930-03', 'available': 1}, {'item': '777521', 'desc': 'SM16GA-07-10D-830-H1', 'available': 1}, {'item': '777533', 'desc': 'SM16GA-09-60D-830-H1', 'available': 1}, {'item': '777832', 'desc': 'SR111-19-36DM-927/918-01', 'available': 1}, {'item': '777578', 'desc': 'SM16GA-09-60D-927-03', 'available': 1}, {'item': '777724', 'desc': 'SP30S-18-09D-930-03', 'available': 1}, {'item': '777900', 'desc': 'SR111-18-09D-927-03', 'available': 1}] |
| 136019 | NOS60-1910 | COL1 | 79,783.55 | 19,522 | — | 2026-6-19 | [{'customer': 'Parallax Industries Inc. dba Square Deal Shop', 'revenue': 14591.74}, {'customer': 'CFA TRADING', 'revenue': 12265.9}, {'customer': 'Bulbrite Industries Inc', 'revenue': 5316.2}, {'customer': 'BULBS.COM', 'revenue': 5096.79}, {'customer': 'VILLA LIGHTING SUPPLY INC', 'revenue': 3292.22}, {'customer': 'JOHN POMP GLASS', 'revenue': 2392.3}, {'customer': 'SUNLAN LIGHTING INC', 'revenue': 2385.59}, {'customer': 'MP III LTD', 'revenue': 2287.98}, {'customer': 'REAL LIGHTING INC.', 'revenue': 1839.36}, {'customer': 'Paluska Group, LLC', 'revenue': 1720.1}, {'customer': 'LSC HOLDINGS INC, dba LIGHTING SUPPLY', 'revenue': 1531.59}, {'customer': 'SERVICE LIGHTING (MN)', 'revenue': 1330.76}, {'customer': '1800LIGHTING.COM', 'revenue': 1318.95}, {'customer': 'SPECTRO LIGHTING GROUP', 'revenue': 1254.03}, {'customer': 'EXWAY ELECTRIC SUPPLY CO', 'revenue': 1194.65}, {'customer': 'LIGHTING GETZ CORP.', 'revenue': 1188.26}, {'customer': 'V de V', 'revenue': 1125.5}, {'customer': 'CANAL BULBS AND PARTS INC', 'revenue': 1020.12}, {'customer': 'New Age America Inc.', 'revenue': 973.1}, {'customer': 'NEW BULBS WORLD', 'revenue': 812.66}, {'customer': 'GRAND BRASS LAMP PARTS INC', 'revenue': 790.94}, {'customer': 'GROSS ELECTRIC, INC.', 'revenue': 778.98}, {'customer': 'WATTS UP LIGHTING', 'revenue': 733.57}, {'customer': 'JUST BULBS THE LIGHT BULB STORE', 'revenue': 720.52}, {'customer': 'LIGHT BULBS & MORE INC', 'revenue': 699.96}, {'customer': 'Decora Lighting Corp', 'revenue': 653.41}, {'customer': 'CHLOE WINSTON LIGHTING DESIGN, LLC', 'revenue': 573.4}, {'customer': 'RIVERSIDE LIGHTING INC', 'revenue': 555.68}, {'customer': 'BULBTRONICS INC', 'revenue': 486.0}, {'customer': 'VALLEY LIGHT GALLERY', 'revenue': 485.46}, {'customer': 'VOSS LIGHTING', 'revenue': 483.33}, {'customer': 'LIGHT SOURCE', 'revenue': 383.1}, {'customer': 'NANTUCKET LIGHTSHOP', 'revenue': 380.43}, {'customer': 'LIGHT BULBS UNLIMITED-WINTER PARK', 'revenue': 364.86}, {'customer': 'Bulbs NYC Inc', 'revenue': 321.83}, {'customer': 'CHL LIGHTING INC', 'revenue': 314.35}, {'customer': 'NEWTON ELECTRICAL SUPPLY', 'revenue': 309.99}, {'customer': 'ZONE MAISON', 'revenue': 309.35}, {'customer': 'LIGHT (WOOLF LIGHTING)', 'revenue': 302.83}, {'customer': 'PRACTICAL PROPS', 'revenue': 245.48}, {'customer': 'Wilson 6 Enterprises  Inc. DBA Mountain Lighting and Design', 'revenue': 235.94}, {'customer': 'PDI- PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 233.13}, {'customer': 'FASHION LIGHT CENTER', 'revenue': 223.68}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 221.15}, {'customer': 'MADISON LIGHTING', 'revenue': 213.34}, {'customer': 'ELLIOTT ELECTRIC SUPPLY', 'revenue': 209.94}, {'customer': 'HUNZICKER BROS', 'revenue': 200.49}, {'customer': 'LIGHT BULBS UNLIMITED -SAND LAKE', 'revenue': 189.08}, {'customer': 'FSG', 'revenue': 186.72}, {'customer': 'M & M LIGHTING-HOUSTON', 'revenue': 184.93}, {'customer': 'CED dba ALL PHASE ELECTRIC - ENFIELD, CT', 'revenue': 173.25}, {'customer': 'G & G ELECTRIC SUPPLY', 'revenue': 171.07}, {'customer': 'CANDELA CORP', 'revenue': 170.1}, {'customer': 'MANASQUAN LIGHTING', 'revenue': 166.06}, {'customer': 'BRAND NAME LIGHTING', 'revenue': 163.07}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 153.37}, {'customer': 'LRS ALL BUILDING SUPPLIES LLC', 'revenue': 153.12}, {'customer': 'BARBIZON ELECTRIC CO., INC.', 'revenue': 145.8}, {'customer': 'GREER LIGHTING CENTER, LLC', 'revenue': 139.53}, {'customer': 'E. SAM JONES DISTRIBUTOR, INC.', 'revenue': 137.96}, {'customer': 'PDI- (TN) PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 126.37}, {'customer': 'NEWBURYPORT LIGHTING CO', 'revenue': 125.28}, {'customer': 'CREGGER COMPANY, INC', 'revenue': 117.74}, {'customer': 'Gross Lighting & Home - Howell, MI', 'revenue': 113.81}, {'customer': 'REXEL CLS HARTFORD,CT', 'revenue': 111.23}, {'customer': 'CED dba ALL-PHASE ELECTRIC PETOSKEY', 'revenue': 109.83}, {'customer': 'MSP LIGHTING PRODUCTS', 'revenue': 103.04}, {'customer': 'MILE HIGH LIGHTING INC.', 'revenue': 100.66}, {'customer': '31 WESTGATE', 'revenue': 85.61}, {'customer': 'LAMP LIGHTERS INC', 'revenue': 83.81}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 82.54}, {'customer': 'VILLAGE LIGHTING & SUPPLY', 'revenue': 82.25}, {'customer': 'FW WEBB COMPANY - BR68 Concord NH', 'revenue': 81.44}, {'customer': 'COLONIAL ELECTRIC - PA', 'revenue': 79.03}, {'customer': 'The Jarrell Company', 'revenue': 78.35}, {'customer': 'H&S FURNITURE', 'revenue': 77.72}, {'customer': 'VAIL LIGHTS INC', 'revenue': 74.11}, {'customer': 'Gross Lighting & Home - Elk Rapids, MI', 'revenue': 70.97}, {'customer': 'A & M ILLUMINATION INC dba Forest Hill Lighting', 'revenue': 66.78}, {'customer': 'COMMERCE CODEWORKS, INC. dba BULBCONNECTION.COM', 'revenue': 63.69}, {'customer': 'GELLER LIGHTING SUPPLY', 'revenue': 63.6}, {'customer': 'BUILDERS LIGHTING & DESIGN INC', 'revenue': 62.13}, {'customer': 'CONTINENTAL LIGHTING CORP', 'revenue': 61.2}, {'customer': 'DENNEY ELECTRIC SUPPLY', 'revenue': 60.47}, {'customer': 'GRAND RAPIDS LIGHTING CENTER', 'revenue': 59.48}, {'customer': 'OLDE MILL HOUSE SHOPPES INC', 'revenue': 59.23}, {'customer': 'THREE JORDANS INC dba FORT WORTH LIGHTING', 'revenue': 57.47}, {'customer': 'THE LIGHTING STUDIO, LLC', 'revenue': 56.46}, {'customer': 'Gross Lighting & Home - OH', 'revenue': 56.23}, {'customer': 'KANSAS LIGHTING DIST., INC', 'revenue': 52.69}, {'customer': 'LYTEWORKS INC', 'revenue': 51.53}, {'customer': 'READ LIGHTING', 'revenue': 48.41}, {'customer': 'CRESCENT LIGHTING SUPPLY INC', 'revenue': 47.63}, {'customer': 'DULLES ELECTRIC', 'revenue': 46.61}, {'customer': 'COMMERCIAL LIGHTING SUPPLY, INC.', 'revenue': 44.13}, {'customer': 'LIGHT BULBS UNLIMITED - PINE CREST', 'revenue': 43.72}, {'customer': 'CATOCTIN LIGHTING SERVICES, INC.', 'revenue': 43.09}, {'customer': 'ANCELRAN INC dba MUSKA LIGHTING CENTER', 'revenue': 41.91}, {'customer': 'Lightbulb Wholesaler Inc.', 'revenue': 41.8}, {'customer': 'B. KEITH CONTROLS, INC.', 'revenue': 41.28}, {'customer': 'DENNEY ELECTRIC SUPPLY', 'revenue': 38.72}, {'customer': 'LIGHTING LOFT', 'revenue': 35.71}, {'customer': 'Tallahassee Lighting', 'revenue': 35.52}, {'customer': 'BURNS ELECTRIC INC', 'revenue': 33.02}, {'customer': 'HOMIER LUMINAIRE INC', 'revenue': 32.11}, {'customer': 'INCON INDUSTRIES', 'revenue': 32.1}, {'customer': 'Light by Alexandria Electric', 'revenue': 29.95}, {'customer': 'RITTENHOUSE ELECTRIC SUPPLY CO', 'revenue': 24.66}, {'customer': 'LIGHTING ZONE INC', 'revenue': 22.11}, {'customer': 'CONNECTICUT LIGHTING CENTER', 'revenue': 20.79}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 16.25}, {'customer': 'LUXE LIGHTING CO. LLC', 'revenue': 15.98}, {'customer': 'METRO ELECTRIC', 'revenue': 14.75}, {'customer': 'Jeanne Rapone Designs, LLC dba Centerline Design', 'revenue': 13.58}, {'customer': 'BAUDANZA ELECTRIC CO INC', 'revenue': 11.9}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 9.71}, {'customer': 'SUNBELT LIGHTING LLC', 'revenue': 8.35}, {'customer': 'HARRY HORN INC', 'revenue': 7.28}, {'customer': 'ACCENT LIGHTING GALLERIES, LLC', 'revenue': 5.17}, {'customer': 'KLS LLC dba SPECTRUM LIGHTING', 'revenue': 4.96}, {'customer': 'WILLIAMS-SONOMA INC (PB-DC)', 'revenue': 0.0}, {'customer': 'LIGHTING N BEYOND LLC', 'revenue': 0.0}, {'customer': 'LIGHT BULBS UNLIMITED-FORT LAUDERDALE', 'revenue': 0.0}, {'customer': 'FOGG LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING INSTYLE', 'revenue': 0.0}, {'customer': 'MASTERPIECE LIGHTING', 'revenue': 0.0}, {'customer': 'McNALLY ELECTRIC', 'revenue': 0.0}, {'customer': 'MILLEN HARDWARE STORE', 'revenue': 0.0}, {'customer': 'MNH Inc', 'revenue': 0.0}, {'customer': 'LADCOS WASHINGTON PARK DESIGN CENTER', 'revenue': 0.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 0.0}, {'customer': 'JONES LIGHTING SPECIALISTS', 'revenue': 0.0}, {'customer': 'J.H. LARSON COMPANY', 'revenue': 0.0}, {'customer': 'LIGHTING EFX', 'revenue': 0.0}, {'customer': 'LIGHTING SUPPLY GUY INC', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'HOLDER ELECTRIC CO', 'revenue': 0.0}, {'customer': '17-90 LIGHTING', 'revenue': 0.0}, {'customer': 'SPECIALTY LIGHTING & BULBS', 'revenue': 0.0}, {'customer': 'Bluecom, LLC DBA SupplyStop', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY (ECOMM)', 'revenue': 0.0}, {'customer': 'CONSERVA ELECTRIC SUPPLY, INC', 'revenue': 0.0}, {'customer': 'UNBEATABLESALE.COM INC.', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'BARN LIGHT ELECTRIC COMPANY LLC', 'revenue': 0.0}, {'customer': 'F.K.G. INC dba THE LIGHT HOUSE', 'revenue': 0.0}, {'customer': 'E.S.C. LTD.', 'revenue': 0.0}, {'customer': 'ATLAS ELECTRIC SUPPLIES', 'revenue': -5.4}] | [{'item': '393002', 'desc': '25G25WH2', 'available': 26409}, {'item': '403307', 'desc': '7.5CFC/15/3', 'available': 23423}, {'item': '134018', 'desc': 'NOS40-1890', 'available': 22003}, {'item': '144015', 'desc': '40G25/ICE', 'available': 19416}, {'item': '134019', 'desc': 'NOS40-1910', 'available': 15465}, {'item': '707503', 'desc': '9T6.5C', 'available': 13861}, {'item': '706114', 'desc': '25T7/DC', 'available': 12280}, {'item': '708115', 'desc': '15T4/130V', 'available': 11586}, {'item': '706110', 'desc': '15T7/DC', 'available': 11492}, {'item': '144026', 'desc': '40G16/MAR/E12', 'available': 10727}, {'item': '707502', 'desc': '9T6.5C/DC', 'available': 9792}, {'item': '144024', 'desc': '25G16/MAR/E12', 'available': 9230}, {'item': '144025', 'desc': '40G25/MAR', 'available': 9059}, {'item': '132510', 'desc': 'NOS25ST15/SQ/E12', 'available': 8523}, {'item': '702007', 'desc': '7.5S11W', 'available': 8422}, {'item': '301040', 'desc': '40G12CL', 'available': 7416}, {'item': '381125', 'desc': 'B25G16CL', 'available': 7403}, {'item': '784160', 'desc': 'B60T10C', 'available': 4798}, {'item': '784025', 'desc': 'B25T10F', 'available': 4784}, {'item': '705140', 'desc': '40T8C', 'available': 4674}, {'item': '340040', 'desc': '40G30WH', 'available': 4547}, {'item': '414025', 'desc': '25CTD/C/2', 'available': 4247}, {'item': '705175', 'desc': '75T8C', 'available': 3869}, {'item': '430040', 'desc': '40C11S', 'available': 3797}, {'item': '104140', 'desc': '40A15C', 'available': 3542}, {'item': '712424', 'desc': '40G25HG', 'available': 3401}, {'item': '136020', 'desc': 'NOS60-VICTOR', 'available': 3390}, {'item': '411006', 'desc': 'SF/6S6', 'available': 3375}, {'item': '403140', 'desc': '40CFC/25/3', 'available': 3211}, {'item': '411007', 'desc': 'SF/7.5S11', 'available': 3179}, {'item': '101025', 'desc': '25A/CL', 'available': 3140}, {'item': '493125', 'desc': '25CFC/25/2', 'available': 3063}, {'item': '400425', 'desc': '25CTC/E14', 'available': 2841}, {'item': '712416', 'desc': '60A19HG', 'available': 2818}, {'item': '134008', 'desc': 'NOS40T9/L', 'available': 2777}, {'item': '108040', 'desc': '40A15/TF', 'available': 2763}, {'item': '351025', 'desc': '25G40CL', 'available': 2640}, {'item': '701511', 'desc': '11S14TPU', 'available': 2610}, {'item': '701611', 'desc': '11S14TPK', 'available': 2601}, {'item': '350100', 'desc': '100G40WH', 'available': 2531}, {'item': '342040', 'desc': 'NOS40G30', 'available': 2434}, {'item': '701311', 'desc': '11S14TB', 'available': 2404}, {'item': '495040', 'desc': '40ETC/2', 'available': 2199}, {'item': '134020', 'desc': 'NOS40-VICTOR', 'available': 2119}, {'item': '133009', 'desc': 'NOS30T9', 'available': 2104}, {'item': '701811', 'desc': '11S14TY', 'available': 2081}, {'item': '702107', 'desc': '7.5S11C', 'available': 2071}, {'item': '351100', 'desc': '100G40CL', 'available': 2064}, {'item': '411003', 'desc': 'SF/F3CTC', 'available': 2033}, {'item': '430025', 'desc': '25C11S', 'available': 1999}, {'item': '100025', 'desc': '25A', 'available': 1985}, {'item': '709607', 'desc': '7C7P', 'available': 1970}, {'item': '132506', 'desc': 'NOS25T6/SQ/E12', 'available': 1946}, {'item': '137501', 'desc': 'NOS60-WB', 'available': 1940}, {'item': '311015', 'desc': '15G16CL3', 'available': 1914}, {'item': '712351', 'desc': '100G40HM', 'available': 1873}, {'item': '134015', 'desc': 'NOS40T14/SQ', 'available': 1807}, {'item': '420225', 'desc': '25F10A', 'available': 1704}, {'item': '784140', 'desc': 'B40T10C', 'available': 1696}, {'item': '400115', 'desc': '15CTC/25/3', 'available': 1628}, {'item': '351060', 'desc': '60G40CL', 'available': 1515}, {'item': '704025', 'desc': '25T10F', 'available': 1479}, {'item': '311225', 'desc': '25G16ECL', 'available': 1448}, {'item': '489025', 'desc': 'B25EFF', 'available': 1439}, {'item': '400025', 'desc': '25CTC/32/3', 'available': 1414}, {'item': '701211', 'desc': '11S14TA', 'available': 1359}, {'item': '351040', 'desc': '40G40CL', 'available': 1292}, {'item': '712312', 'desc': '25G16HM', 'available': 1285}, {'item': '134014', 'desc': 'NOS40T14', 'available': 1274}, {'item': '132507', 'desc': '25T6/SQ/E12', 'available': 1147}, {'item': '350150', 'desc': '150G40WH', 'available': 1136}, {'item': '704125', 'desc': '25T10C', 'available': 1120}, {'item': '707501', 'desc': '9T6.5C/N', 'available': 1096}, {'item': '431040', 'desc': '40C15S', 'available': 1080}, {'item': '391115', 'desc': '15G16CL2', 'available': 1000}, {'item': '712314', 'desc': '40G16HM', 'available': 965}, {'item': '110025', 'desc': '25A19F/12', 'available': 951}, {'item': '393004', 'desc': '40G25WH2', 'available': 946}, {'item': '493115', 'desc': '15CFC/25/2', 'available': 917}, {'item': '712110', 'desc': '100A21HM', 'available': 910}, {'item': '712336', 'desc': '60G25HM', 'available': 898}, {'item': '708106', 'desc': '6T4/130V', 'available': 893}, {'item': '701711', 'desc': '11S14TR', 'available': 866}, {'item': '350040', 'desc': '40G40WH', 'available': 824}, {'item': '490025', 'desc': '25CTC/32/2', 'available': 810}, {'item': '330025', 'desc': '25G25WH3', 'available': 804}, {'item': '490125', 'desc': '25CTC/25/2', 'available': 788}, {'item': '712331', 'desc': '100G25HM', 'available': 787}, {'item': '400125', 'desc': '25CTC/25/3', 'available': 762}, {'item': '403040', 'desc': '40CFC/32/3', 'available': 732}, {'item': '421025', 'desc': '25F15WH', 'available': 702}, {'item': '784060', 'desc': 'B60T10F', 'available': 700}, {'item': '705040', 'desc': '40T8F', 'available': 681}, {'item': '701411', 'desc': '11S14TG', 'available': 675}, {'item': '144016', 'desc': '40G16/ICE/E12', 'available': 616}, {'item': '480140', 'desc': 'B40PRISM', 'available': 604}, {'item': '350025', 'desc': '25G40WH', 'available': 575}, {'item': '704340', 'desc': '40T10C/HO', 'available': 550}, {'item': '420215', 'desc': '15F10A', 'available': 513}, {'item': '300010', 'desc': '10G12WH', 'available': 476}, {'item': '403025', 'desc': '25CFC/32/3', 'available': 470}, {'item': '707115', 'desc': '15T6', 'available': 454}, {'item': '431025', 'desc': '25C15S', 'available': 428}, {'item': '706115', 'desc': '15T7', 'available': 419}, {'item': '421225', 'desc': '25F15A', 'available': 393}, {'item': '408040', 'desc': '40EFC/3', 'available': 370}, {'item': '712356', 'desc': '60G40HM', 'available': 344}, {'item': '705075', 'desc': '75T8F', 'available': 174}, {'item': '493025', 'desc': '25CFC/32/2', 'available': 162}, {'item': '784115', 'desc': 'B15T10C', 'available': 150}, {'item': '300025', 'desc': '25G12WH', 'available': 127}, {'item': '132520', 'desc': 'NOS25-VICTOR', 'available': 124}, {'item': '137701', 'desc': 'NOS60-DIAMOND', 'available': 123}, {'item': '393102', 'desc': '25G25CL2', 'available': 102}, {'item': '137601', 'desc': 'NOS60-BH', 'available': 85}, {'item': '712334', 'desc': '40G25HM', 'available': 75}, {'item': '137401', 'desc': 'NOS60-GLOBE', 'available': 43}, {'item': '701111', 'desc': '11S14C', 'available': 40}, {'item': '701911', 'desc': '11S14F', 'available': 24}, {'item': '137101', 'desc': 'NOS60-PS', 'available': 22}, {'item': '330040', 'desc': '40G25WH3', 'available': 19}, {'item': '701011', 'desc': '11S14W', 'available': 15}, {'item': '137301', 'desc': 'NOS60-ET', 'available': 10}] |
| 776724 | LED4T8/30K/FIL/3 | LED | 74,388.09 | 18,170 | — | 2026-6-19 | [{'customer': 'NOVA LIGHTING INC.', 'revenue': 11824.72}, {'customer': 'BLUEBIRD LIGHTING LLC', 'revenue': 5274.22}, {'customer': 'WILSON FANS & LIGHTING', 'revenue': 3295.99}, {'customer': 'CREGGER COMPANY, INC', 'revenue': 3124.0}, {'customer': 'LIGHTING INC', 'revenue': 2404.39}, {'customer': 'Better Designed Lighting', 'revenue': 2269.49}, {'customer': 'WILSON LIGHTING OF NAPLES', 'revenue': 2139.98}, {'customer': 'CAPITOL LIGHTING - FL location', 'revenue': 2084.13}, {'customer': 'CAPITOL LIGHTING - NJ location', 'revenue': 2022.77}, {'customer': 'ELEMENTS-DISTINCTIVE LIGHTING & HOME FURNISHINGS', 'revenue': 1797.83}, {'customer': 'REAL LIGHTING INC.', 'revenue': 1608.47}, {'customer': 'BORDER STATES ELEC SUPPLY (West Coast)', 'revenue': 1109.17}, {'customer': 'THREE JORDANS INC dba FORT WORTH LIGHTING', 'revenue': 993.43}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 887.33}, {'customer': 'LIGHTING SPECIALISTS, INC - Nova lighting', 'revenue': 870.72}, {'customer': 'CONNECTICUT LIGHTING CENTER', 'revenue': 870.44}, {'customer': 'BEAUTIFUL THINGS', 'revenue': 859.52}, {'customer': 'HOBRECHT LIGHTING CO., INC.', 'revenue': 856.94}, {'customer': 'LDB HOLDINGS, LLC dba CW FLOORS AND LIGHTING', 'revenue': 776.93}, {'customer': 'VALLEY LIGHT GALLERY', 'revenue': 764.91}, {'customer': 'LIGHT BULBS ETC', 'revenue': 754.24}, {'customer': 'SOUTHERN LIGHTING GALLERY', 'revenue': 748.66}, {'customer': 'LIGHT & DAY LLC', 'revenue': 740.04}, {'customer': 'PROGRESSIVE', 'revenue': 650.7}, {'customer': 'CE TANG YUK & CO., LTD.', 'revenue': 641.45}, {'customer': '1800LIGHTING.COM', 'revenue': 628.93}, {'customer': 'LONESTAR ELECTRIC - AUSTIN, Houston', 'revenue': 617.33}, {'customer': 'LIGHTING DESIGN LLC', 'revenue': 612.14}, {'customer': 'CED dba ALL-PHASE ELECTRIC PETOSKEY', 'revenue': 587.62}, {'customer': 'SOUTHERN LIGHTS, INC.', 'revenue': 570.71}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 558.59}, {'customer': 'WASATCH LIGHTING INC', 'revenue': 523.96}, {'customer': 'TEXAS BRIGHT IDEAS INC', 'revenue': 498.04}, {'customer': 'AMERICAN LIGHTING INC', 'revenue': 489.84}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 486.57}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 460.42}, {'customer': 'CANDELA CORP', 'revenue': 453.77}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 450.84}, {'customer': 'EXWAY ELECTRIC SUPPLY CO', 'revenue': 444.06}, {'customer': 'PDI- PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 443.98}, {'customer': 'LIGHT BULBS UNLIMITED-PORT ST LUCIE', 'revenue': 432.18}, {'customer': 'LYTEWORKS INC', 'revenue': 404.87}, {'customer': 'CAROLINA LANTERNS', 'revenue': 402.17}, {'customer': 'HOLDER ELECTRIC CO', 'revenue': 394.96}, {'customer': 'GRAND RAPIDS LIGHTING CENTER', 'revenue': 390.65}, {'customer': 'PASSION LIGHTING', 'revenue': 386.6}, {'customer': 'LIGHT HOUSE OF LEWES INC', 'revenue': 380.03}, {'customer': 'INTEGRIS SOLUTIONS dba GSCS, LLC.', 'revenue': 359.85}, {'customer': 'CONTINENTAL LIGHTING CORP', 'revenue': 328.28}, {'customer': 'LIGHT BULBS UNLIMITED-NAPLES', 'revenue': 324.68}, {'customer': 'SERVICE LIGHTING (MN)', 'revenue': 322.56}, {'customer': 'DEALERS ELECTRIC SUPPLY-WACO', 'revenue': 310.13}, {'customer': 'DIAL ELECTRIC SUPPLY CO', 'revenue': 291.24}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 286.36}, {'customer': 'EFIRDS INTERIORS, INC.', 'revenue': 284.04}, {'customer': 'PDI- (TN) PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 267.66}, {'customer': 'PROGRESSIVE LIGHTING INC dba LEE LIGHTING(NC)', 'revenue': 264.69}, {'customer': "MAHLANDER'S APPLIANCE AND LIGHTING", 'revenue': 260.77}, {'customer': 'COMPLETE LIGHTING OF TAMPA, INC.', 'revenue': 257.5}, {'customer': 'ILLUMINATIONS LIGHTING', 'revenue': 254.63}, {'customer': 'PROGRESSIVE LIGHTING INC dba LEE LIGHTING(TX)', 'revenue': 253.98}, {'customer': 'CAPITAL ELECTRIC - NC/SC', 'revenue': 239.91}, {'customer': 'CHRISTIES LIGHTING GALLERY, LLC', 'revenue': 236.83}, {'customer': 'LIGHTING SUPER STORE', 'revenue': 236.54}, {'customer': 'CLINE-HOLDER ELECTRIC SUPPLY, INC.', 'revenue': 229.17}, {'customer': 'JAMES ASHJIAN LIGHTING & HOME', 'revenue': 225.68}, {'customer': 'SMALL TOWN HOME & DECOR', 'revenue': 222.2}, {'customer': 'CAROLS LIGHTING & FAN SHOP', 'revenue': 220.23}, {'customer': 'HYDROLOGIC DISTRIBUTION COMPANY', 'revenue': 211.23}, {'customer': 'RITTENHOUSE ELECTRIC SUPPLY CO', 'revenue': 202.11}, {'customer': 'SCHAEDLER YESCO DISTRIBUTION', 'revenue': 198.09}, {'customer': 'LUMENAREA', 'revenue': 180.22}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 172.61}, {'customer': 'A & E BOWERY LIGHTING INC.', 'revenue': 171.73}, {'customer': 'LAMP & SHADE WORKS', 'revenue': 165.2}, {'customer': 'LIGHTING BY FOX', 'revenue': 161.92}, {'customer': 'The Jarrell Company', 'revenue': 159.19}, {'customer': 'AVENUE LIGHTING & DESIGN', 'revenue': 157.53}, {'customer': 'LIGHTING CORNER', 'revenue': 155.87}, {'customer': 'LIGHTING & BULBS UNLIMITED', 'revenue': 155.55}, {'customer': 'VILLAGE LIGHTING & SUPPLY', 'revenue': 155.33}, {'customer': 'SIOUX EMPIRE LIGHTING, INC', 'revenue': 155.28}, {'customer': 'LSC HOLDINGS INC, dba LIGHTING SUPPLY', 'revenue': 147.1}, {'customer': 'HAMBUCHEN ELECTRIC CO., INC.', 'revenue': 144.52}, {'customer': 'JOSEPHS ELECTRICAL CENTER', 'revenue': 138.73}, {'customer': 'IM LIGHTING LLC', 'revenue': 138.37}, {'customer': 'PEMBA LIGHTING & AUTOMATION', 'revenue': 136.96}, {'customer': 'NORTHERN CONSTRUCTION LLC dba UNIQUE DESIGN', 'revenue': 136.09}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 133.0}, {'customer': 'VAIL LIGHTS INC', 'revenue': 130.37}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 125.34}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 124.81}, {'customer': 'HOUSE OF LAMPS & SHADES', 'revenue': 122.19}, {'customer': "BRUNO'S HARDWARE, INC.", 'revenue': 121.74}, {'customer': 'Bulbs NYC Inc', 'revenue': 115.59}, {'customer': 'ILLUMINATIONS', 'revenue': 112.16}, {'customer': 'FOX HOME CENTER', 'revenue': 109.85}, {'customer': 'Inspired Interiors', 'revenue': 107.62}, {'customer': 'CHL LIGHTING INC', 'revenue': 107.23}, {'customer': 'ELUME DISTINCTIVE LIGHTING', 'revenue': 105.67}, {'customer': 'LIGHT BULBS ETC-LIGHTSTYLES', 'revenue': 105.53}, {'customer': 'GARDEN OF THE GODS LIGHTING', 'revenue': 104.56}, {'customer': 'WOLBERG ELECTRICAL SUPPLY CO', 'revenue': 102.06}, {'customer': 'KRELL LIGHTING', 'revenue': 99.51}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 97.0}, {'customer': 'DOLAN NW LLC DBA MELETIO COMPANY', 'revenue': 94.96}, {'customer': 'TIMELESS DESIGNS LP', 'revenue': 94.91}, {'customer': 'URBAN LIGHTS', 'revenue': 94.3}, {'customer': 'Tareli Inc dba Mi Casa Lighting & Fans', 'revenue': 93.3}, {'customer': 'HOMESTYLES', 'revenue': 90.1}, {'customer': 'INCON INDUSTRIES', 'revenue': 89.42}, {'customer': 'IMAGINE MORE SERVICE CORP', 'revenue': 87.83}, {'customer': 'IBS Lighting', 'revenue': 85.69}, {'customer': 'JUST LIGHTS', 'revenue': 85.11}, {'customer': 'COOKS LIGHTING & FLOORING', 'revenue': 84.65}, {'customer': 'MODERN LIGHTING', 'revenue': 84.54}, {'customer': 'BRIGHT IDEAS', 'revenue': 79.31}, {'customer': 'ACCENT LIGHTING INC', 'revenue': 75.44}, {'customer': 'RM COOPER LIGHTING ETC', 'revenue': 75.42}, {'customer': 'HOUSE ELECTRIC, LLC', 'revenue': 72.56}, {'customer': 'RAYMOND DeSTEIGER INC', 'revenue': 72.37}, {'customer': 'MORSCO -TX area', 'revenue': 72.13}, {'customer': 'SUNBELT LIGHTING LLC', 'revenue': 67.45}, {'customer': 'Georgia Lighting', 'revenue': 65.07}, {'customer': 'LIGHT BULBS UNLIMITED-WEST PALM BEACH', 'revenue': 64.76}, {'customer': 'JACOBSON ELECTRIC SERVICE INC', 'revenue': 59.77}, {'customer': 'Aggieland Lighting & Design', 'revenue': 56.79}, {'customer': 'Light by Alexandria Electric', 'revenue': 54.97}, {'customer': 'KLS LLC dba SPECTRUM LIGHTING', 'revenue': 54.58}, {'customer': 'VALLEY LIGHTING INC', 'revenue': 53.67}, {'customer': 'COAST LIGHTING', 'revenue': 52.87}, {'customer': 'SOUTHLAND PLUMBING SUPPLY', 'revenue': 52.13}, {'customer': 'COLEY ELECTRIC SUPPLY, INC.', 'revenue': 51.69}, {'customer': 'AURA LIGHTING', 'revenue': 51.46}, {'customer': 'Lightbulb Wholesaler Inc.', 'revenue': 51.3}, {'customer': 'HAGENS LIGHTING', 'revenue': 51.2}, {'customer': 'LIGHTING UNLIMITED', 'revenue': 50.12}, {'customer': 'Tallahassee Lighting', 'revenue': 49.59}, {'customer': 'FASHION LIGHT CENTER', 'revenue': 49.5}, {'customer': 'COFFMAN HOME DECOR', 'revenue': 48.92}, {'customer': 'LIGHT (WOOLF LIGHTING)', 'revenue': 47.89}, {'customer': 'NORTHERN LIGHTING, INC.', 'revenue': 47.58}, {'customer': 'LUMEN ILUMINACION, LTD.', 'revenue': 46.61}, {'customer': 'LIGHTING SOUTH LLC', 'revenue': 45.95}, {'customer': 'JUST BULBS THE LIGHT BULB STORE', 'revenue': 45.89}, {'customer': 'COMMERCE CODEWORKS, INC. dba BULBCONNECTION.COM', 'revenue': 44.06}, {'customer': 'Gross Lighting & Home - Howell, MI', 'revenue': 43.93}, {'customer': 'LIGHTHOUSE SUPPLY CO', 'revenue': 42.7}, {'customer': 'Ruby and Company', 'revenue': 41.89}, {'customer': 'Living Lighting #53', 'revenue': 40.59}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 40.19}, {'customer': 'CHARLESTON LIGHTING & INT.', 'revenue': 38.36}, {'customer': 'MEDINA LIGHTING', 'revenue': 34.46}, {'customer': 'HAJOCA CORP -TX, FL, LA', 'revenue': 33.45}, {'customer': 'BUILDERS LIGHTING & DESIGN INC', 'revenue': 32.57}, {'customer': 'CRESCENT LIGHTING SUPPLY INC', 'revenue': 32.33}, {'customer': 'LIGHTING GETZ CORP.', 'revenue': 31.84}, {'customer': 'LIGHT BARN', 'revenue': 31.55}, {'customer': 'METRO ELECTRIC', 'revenue': 31.12}, {'customer': 'J.H. LARSON COMPANY', 'revenue': 29.44}, {'customer': 'SPRINGFIELD ELECTRIC COMPANY,LLC DBA ECHO ELECTRIC', 'revenue': 29.06}, {'customer': 'CONNECTICUT LIGHTING CENTER-Dropship', 'revenue': 27.39}, {'customer': 'DOLAN NW LLC - DBA SEATTLE LIGHTING', 'revenue': 26.76}, {'customer': 'MASTERPIECE LIGHTING', 'revenue': 26.76}, {'customer': 'STOKES ELECTRIC COMPANY', 'revenue': 25.7}, {'customer': 'FW WEBB COMPANY - BR68 Concord NH', 'revenue': 24.78}, {'customer': 'Gross Lighting & Home - OH', 'revenue': 23.25}, {'customer': 'HARBOUR LIGHTING', 'revenue': 19.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 18.39}, {'customer': 'GREER LIGHTING CENTER, LLC', 'revenue': 18.25}, {'customer': 'MADISON LIGHTING', 'revenue': 17.57}, {'customer': 'ILLUMINATE', 'revenue': 17.19}, {'customer': 'NEWTON ELECTRICAL SUPPLY', 'revenue': 10.71}, {'customer': 'LIGHTING CONNECTION - BUDA', 'revenue': 10.49}, {'customer': 'LIGHTING UNLIMITED dba LIGHTING ETC', 'revenue': 10.22}, {'customer': 'GROSS ELECTRIC, INC.', 'revenue': 9.44}, {'customer': 'F.K.G. INC dba THE LIGHT HOUSE', 'revenue': 9.12}, {'customer': 'FW Webb Company - BR151 Middlebury VT', 'revenue': 8.95}, {'customer': 'EDWARD JOY LIGHTING & ELECTRIC SUPPLY', 'revenue': 8.85}, {'customer': 'Lowcountry Lighting Studio', 'revenue': 7.77}, {'customer': 'LIGHT BULBS UNLIMITED-WINTER PARK', 'revenue': 4.64}, {'customer': 'Staggs Carpets & Interiors, Inc.', 'revenue': 0.0}, {'customer': 'HOUSE OF SHADES & LAMPS', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY (ECOMM)', 'revenue': 0.0}, {'customer': "GRAHAM'S LIGHTING FIXTURES, INC.", 'revenue': 0.0}, {'customer': 'UNIVERSAL LIGHTS', 'revenue': 0.0}, {'customer': 'URBAN AMBIANCE INC', 'revenue': 0.0}, {'customer': 'FUSION LIGHT & DESIGN', 'revenue': 0.0}, {'customer': 'FRANKLIN LIGHTING', 'revenue': 0.0}, {'customer': 'FW WEBB COMPANY - ME', 'revenue': 0.0}, {'customer': 'Wes Ulmo Interior Design', 'revenue': 0.0}, {'customer': 'DOMINION ELECTRIC SUPPLY, a Division of Border States - VA,', 'revenue': 0.0}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 0.0}, {'customer': 'CAMPBELL LAMP SUPPLY', 'revenue': 0.0}, {'customer': 'BURNS ELECTRIC INC', 'revenue': 0.0}, {'customer': 'WOLFERS LIGHTING INC', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'NOLAND - KNOXVILLE TN', 'revenue': 0.0}, {'customer': 'ACE PLUMBING HEATING & ELECTRICAL', 'revenue': 0.0}, {'customer': 'N & S ELECTRIC SUPPLY CO', 'revenue': 0.0}, {'customer': 'MINNESOTA LIGHTING FIREPLACE &', 'revenue': 0.0}, {'customer': 'P&F Lites Etcetera, LLC', 'revenue': 0.0}, {'customer': 'Southeast Electric & Plumbing', 'revenue': 0.0}, {'customer': 'MAISON DU LUMINAIRE INC', 'revenue': 0.0}, {'customer': 'PRESTIGE LIGHTING & DESIGN', 'revenue': 0.0}, {'customer': 'LIGHTS OF OCONEE', 'revenue': 0.0}, {'customer': 'Lighting Star DBA 1-800Mylamps', 'revenue': 0.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 0.0}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 0.0}, {'customer': 'Reclaimed Warehouse', 'revenue': 0.0}, {'customer': 'RITE RUG CO. dba Capital Lighting', 'revenue': 0.0}, {'customer': 'LIGHT BULBS UNLIMITED- BOCA RATON', 'revenue': 0.0}, {'customer': 'ROBINSON LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHT BULBS UNLIMITED - PINE CREST', 'revenue': 0.0}, {'customer': 'KENYON NOBLE LUMBER COMPANY', 'revenue': 0.0}, {'customer': 'KAELINS, INC. dba ALCOTT & BENTLEY', 'revenue': 0.0}, {'customer': 'HUBBARDTON FORGE', 'revenue': 0.0}, {'customer': 'SPRINGHAUS', 'revenue': 0.0}, {'customer': 'Bulbrite Industries Inc', 'revenue': 0.0}] | [{'item': '774244', 'desc': 'LED8A19/B60W/830/1P', 'available': 242227}, {'item': '774263', 'desc': 'LED9A19/PF60W/930/D/2/1P', 'available': 171667}, {'item': '776214', 'desc': 'LED7A19/30K/FIL/D/B/2', 'available': 128216}, {'item': '776212', 'desc': 'LED7A19/27K/FIL/D/B/2', 'available': 85200}, {'item': '774243', 'desc': 'LED8A19/B60W/827/1P', 'available': 74194}, {'item': '774262', 'desc': 'LED9A19/PF60W/927/D/2/1P', 'available': 51010}, {'item': '774280', 'desc': 'LED9A19/P60W/927/J/D/2/1P', 'available': 47742}, {'item': '776756', 'desc': 'LED4B11/27K/FIL/4/JA8', 'available': 46077}, {'item': '776627', 'desc': 'LED5B11/30K/FIL/E12/3', 'available': 38110}, {'item': '776204', 'desc': 'LED5B11/30K/FIL/D/B/2', 'available': 36790}, {'item': '773117', 'desc': 'LED9REC/4/940/WHRD/D', 'available': 32447}, {'item': '776873', 'desc': 'LED4G16/27K/FIL/3', 'available': 31103}, {'item': '776626', 'desc': 'LED5B11/27K/FIL/E12/3', 'available': 30021}, {'item': '776216', 'desc': 'LED7A19/40K/FIL/D/B/2', 'available': 29245}, {'item': '776201', 'desc': 'LED4B11/30K/FIL/D/B/2', 'available': 24933}, {'item': '773231', 'desc': 'LED7JBOXDL/3/930/WHRD/D', 'available': 21266}, {'item': '776207', 'desc': 'LED5T9/30K/FIL/D/B/2', 'available': 21110}, {'item': '772870', 'desc': 'LED8BR30/827/D/4', 'available': 20542}, {'item': '776215', 'desc': 'LED7A19/30K/FIL/M/D/B/2', 'available': 20370}, {'item': '776200', 'desc': 'LED4B11/27K/FIL/D/B/2', 'available': 19940}, {'item': '776768', 'desc': 'LED8A19/30K/FIL/3/JA8', 'available': 19752}, {'item': '772857', 'desc': 'LED8BR30/830/D/5', 'available': 18274}, {'item': '773232', 'desc': 'LED7JBOXDL/3/940/WHRD/D', 'available': 17512}, {'item': '776774', 'desc': 'LED8A19/27K/FIL/3/JA8', 'available': 17363}, {'item': '773167', 'desc': 'LED14REC/5/6/940/WHRD/D', 'available': 16954}, {'item': '770579', 'desc': 'LED4G9/30K/120/D', 'available': 16521}, {'item': '776931', 'desc': 'LED5B11/40K/FIL/E12/3', 'available': 13584}, {'item': '776769', 'desc': 'LED8ST18/30K/FIL/3/JA8', 'available': 13486}, {'item': '776962', 'desc': 'LED4B11/50K/FIL/3', 'available': 13132}, {'item': '772253', 'desc': 'LED15PAR38/B-FL40/830/WD/2', 'available': 12921}, {'item': '776224', 'desc': 'LED7ST18/30K/FIL/D/B/2', 'available': 12603}, {'item': '776763', 'desc': 'LED4B11/30K/FIL/4/JA8', 'available': 11901}, {'item': '776987', 'desc': 'LED13ST18/50K/FIL/3', 'available': 11700}, {'item': '776985', 'desc': 'LED8ST18/50K/FIL/3', 'available': 11431}, {'item': '776937', 'desc': 'LED8A19/27K/FIL/M/4', 'available': 11147}, {'item': '774265', 'desc': 'LED9A19/PF60W/950/D/2/1P', 'available': 10427}, {'item': '774245', 'desc': 'LED8A19/B60W/840/1P', 'available': 10401}, {'item': '776964', 'desc': 'LED5B11/50K/FIL/3', 'available': 10398}, {'item': '776966', 'desc': 'LED6B11/50K/FIL/3', 'available': 10362}, {'item': '776684', 'desc': 'LED1S14/24K/FIL', 'available': 10279}, {'item': '776767', 'desc': 'LED8ST18/27K/FIL/3/JA8', 'available': 10262}, {'item': '774281', 'desc': 'LED9A19/P60W/930/J/D/2/1P', 'available': 10171}, {'item': '776685', 'desc': 'LED1S14/27K/FIL', 'available': 9202}, {'item': '773262', 'desc': 'LED14JBOXDL/6/940/WHRD/D', 'available': 8927}, {'item': '776859', 'desc': 'LED4CA10/27K/FIL/3', 'available': 8859}, {'item': '776791', 'desc': 'LED4T6/30K/FIL/3', 'available': 8768}, {'item': '776977', 'desc': 'LED8G25/40K/FIL/3/JA8', 'available': 8685}, {'item': '774232', 'desc': 'LED9A19/B60W/840/1P', 'available': 8516}, {'item': '776220', 'desc': 'LED7G25/30K/FIL/M/D/B/2', 'available': 8183}, {'item': '776935', 'desc': 'LED8ST18/40K/FIL/3/JA8', 'available': 8053}, {'item': '776930', 'desc': 'LED4B11/40K/FIL/3/JA8', 'available': 8002}, {'item': '776963', 'desc': 'LED4B11/50K/FIL/M/3', 'available': 7911}, {'item': '776965', 'desc': 'LED5B11/50K/FIL/M/3', 'available': 7867}, {'item': '776967', 'desc': 'LED6B11/50K/FIL/M/3', 'available': 7771}, {'item': '776979', 'desc': 'LED8G25/50K/FIL/3', 'available': 7734}, {'item': '776976', 'desc': 'LED5G25/30K/FIL/M/3', 'available': 7639}, {'item': '776968', 'desc': 'LED6B11/40K/FIL/M/3', 'available': 7585}, {'item': '776904', 'desc': 'LED2T6/21K/FIL-NOS/3', 'available': 7484}, {'item': '776974', 'desc': 'LED5G25/27K/FIL/M/3', 'available': 7448}, {'item': '772245', 'desc': 'LED10PAR30S/B-FL40/830/WD/2', 'available': 7170}, {'item': '772254', 'desc': 'LED15PAR38/B-FL40/840/WD/2', 'available': 7138}, {'item': '776958', 'desc': 'LED8A19/50K/FIL/3', 'available': 7119}, {'item': '774267', 'desc': 'LED11A19/PF75W/930/D/2/1P', 'available': 7093}, {'item': '776203', 'desc': 'LED5B11/27K/FIL/D/B/2', 'available': 7031}, {'item': '773165', 'desc': 'LED14REC/5/6/927/WHRD/D', 'available': 6752}, {'item': '770191', 'desc': 'LED/C9C', 'available': 6725}, {'item': '776973', 'desc': 'LED5G25/27K/FIL/3', 'available': 6691}, {'item': '776945', 'desc': 'LED5T9L/27K/11/FIL/4', 'available': 6516}, {'item': '776732', 'desc': 'LED5T9/30K/5/FIL/4/JA8', 'available': 6468}, {'item': '774248', 'desc': 'LED8A19/B60W/830/4P', 'available': 6392}, {'item': '770595', 'desc': 'LED4E12/27K/120/D', 'available': 6243}, {'item': '776781', 'desc': 'LED5T9/27K/5/FIL/F/3', 'available': 6238}, {'item': '776223', 'desc': 'LED7ST18/27K/FIL/D/B/2', 'available': 6173}, {'item': '776975', 'desc': 'LED5G25/30K/FIL/3', 'available': 6138}, {'item': '776593', 'desc': 'LED4C15/21K/FIL/SPUN/AMB', 'available': 5879}, {'item': '776991', 'desc': 'LED5T9/50K/5/FIL/3', 'available': 5805}, {'item': '776402', 'desc': 'LED5CA10/30K-18K/WMDM/FIL/M', 'available': 5760}, {'item': '776980', 'desc': 'LED8G25/50K/FIL/M/3', 'available': 5759}, {'item': '776936', 'desc': 'LED13ST18/40K/FIL/3/JA8', 'available': 5688}, {'item': '776969', 'desc': 'LED5CA10/27K/FIL/E26/3', 'available': 5619}, {'item': '776960', 'desc': 'LED14A19/50K/FIL/3', 'available': 5594}, {'item': '776978', 'desc': 'LED8G25/40K/FIL/M/3', 'available': 5589}, {'item': '773272', 'desc': 'LED18JBOXDL/8/940/WHRD/D', 'available': 5540}, {'item': '776405', 'desc': 'LED9ST18/30K-18K/WMDM/FIL/M', 'available': 5471}, {'item': '773260', 'desc': 'LED14JBOXDL/6/927/WHRD/D', 'available': 5418}, {'item': '776780', 'desc': 'LED4T6/27K/FIL/3', 'available': 5254}, {'item': '776949', 'desc': 'LED3T9/30K/7/FIL/4', 'available': 5211}, {'item': '776951', 'desc': 'LED2T6/27K/FIL/3', 'available': 5170}, {'item': '776952', 'desc': 'LED2T6/30K/FIL/4', 'available': 5158}, {'item': '776592', 'desc': 'LED4C15/27K/FIL/SPUN/SAT', 'available': 5154}, {'item': '772302', 'desc': 'LED15PAR38/FL40/930/WD/2', 'available': 5122}, {'item': '776581', 'desc': 'LED4F15/21K/FIESTA/AMB', 'available': 5089}, {'item': '773240', 'desc': 'LED9JBOXDL/4/927/WHRD/D', 'available': 4978}, {'item': '772877', 'desc': 'LED15BR40/830/D/4', 'available': 4964}, {'item': '776219', 'desc': 'LED7G25/30K/FIL/D/B/2', 'available': 4860}, {'item': '776953', 'desc': 'LED2A19/27K/FIL/M/3', 'available': 4834}, {'item': '773210', 'desc': 'LED9JBOXDL/4/827/WHRD/D', 'available': 4829}, {'item': '776914', 'desc': 'LED9A19/30K/FIL/4', 'available': 4825}, {'item': '776959', 'desc': 'LED8A19/50K/FIL/M/3', 'available': 4815}, {'item': '776872', 'desc': 'LED5A19/27K/FIL/3', 'available': 4807}, {'item': '776989', 'desc': 'LED5T9/40K/5/FIL/3/JA8', 'available': 4806}, {'item': '776205', 'desc': 'LED5B11/40K/FIL/D/B/2', 'available': 4740}, {'item': '776902', 'desc': 'LED4A19/21K/FIL-NOS/3', 'available': 4729}, {'item': '776749', 'desc': 'LED8G25/27K/FIL/4/JA8', 'available': 4726}, {'item': '776206', 'desc': 'LED5T9/27K/FIL/D/B/2', 'available': 4718}, {'item': '776840', 'desc': 'LED6G40/27K/FIL/HW/3', 'available': 4647}, {'item': '776836', 'desc': 'LED6G40/27K/FIL/HB/3', 'available': 4647}, {'item': '776837', 'desc': 'LED5A19/27K/FIL/HW/3', 'available': 4522}, {'item': '776862', 'desc': 'LED4B11/27K/FIL/E26/3', 'available': 4453}, {'item': '776731', 'desc': 'LED5T9/27K/5/FIL/4/JA8', 'available': 4452}, {'item': '776833', 'desc': 'LED5A19/27K/FIL/HB/3', 'available': 4382}, {'item': '776580', 'desc': 'LED4F15/27K/FIESTA/CLR', 'available': 4348}, {'item': '776719', 'desc': 'LED5T9L/21K/15/FIL-NOS/3', 'available': 4325}, {'item': '776225', 'desc': 'LED7ST18/40K/FIL/D/B/2', 'available': 4199}, {'item': '776906', 'desc': 'LED2G16/21K/FIL-NOS/3', 'available': 4189}, {'item': '773221', 'desc': 'LED14JBOXDL/6/830/WHRD/D', 'available': 4186}, {'item': '771109', 'desc': 'LED6PAR16GUFL40/50/930/J/D/2', 'available': 4184}, {'item': '771086', 'desc': 'LED6MR16FL40/50/930/J/D/5', 'available': 4165}, {'item': '772246', 'desc': 'LED10PAR30S/B-FL40/840/WD/2', 'available': 4155}, {'item': '772856', 'desc': 'LED8BR30/827/D/5', 'available': 4138}, {'item': '776925', 'desc': 'LED8A19/40K/FIL/3/JA8', 'available': 4089}, {'item': '772242', 'desc': 'LED7PAR20/B-FL40/830/WD/2', 'available': 4049}, {'item': '771088', 'desc': 'LED7MR16FL40/75/930/J/D/2', 'available': 3955}, {'item': '776839', 'desc': 'LED5G25/27K/FIL/HW/3', 'available': 3940}, {'item': '776970', 'desc': 'LED5CA10/27K/FIL/E26/M/3', 'available': 3938}, {'item': '776992', 'desc': 'LED5T9/50K/5/FIL/F/3', 'available': 3902}, {'item': '776217', 'desc': 'LED7G25/27K/FIL/D/B/2', 'available': 3894}, {'item': '776982', 'desc': 'LED8G40/40K/FIL/M/3', 'available': 3881}, {'item': '776990', 'desc': 'LED5T9/40K/5/FIL/F/3', 'available': 3854}, {'item': '776832', 'desc': 'LED7A15/30K/FIL/M/3', 'available': 3831}, {'item': '776838', 'desc': 'LED2G16/27K/FIL/HW/3', 'available': 3791}, {'item': '772243', 'desc': 'LED7PAR20/B-FL40/840/WD/2', 'available': 3727}, {'item': '776981', 'desc': 'LED8G40/40K/FIL/3', 'available': 3726}, {'item': '776988', 'desc': 'LED6B11/30K/FIL/M/3', 'available': 3692}, {'item': '773271', 'desc': 'LED18JBOXDL/8/930/WHRD/D', 'available': 3675}, {'item': '776404', 'desc': 'LED9G25/30K-18K/WMDM/FIL/M', 'available': 3629}, {'item': '776744', 'desc': 'LED4G16/30K/FIL/4/JA8', 'available': 3590}, {'item': '776995', 'desc': 'LED4T6/50K/FIL/3', 'available': 3553}, {'item': '776986', 'desc': 'LED6B11/27K/FIL/M/3', 'available': 3541}, {'item': '776864', 'desc': 'LED4CA10/30K/FIL/3', 'available': 3495}, {'item': '776913', 'desc': 'LED9A19/27K/FIL/4', 'available': 3479}, {'item': '776829', 'desc': 'LED7A15/27K/FIL/3', 'available': 3434}, {'item': '774269', 'desc': 'LED15A19/P100W/930/J/D/2/1P', 'available': 3381}, {'item': '776938', 'desc': 'LED2B11/27K/FIL/4', 'available': 3374}, {'item': '771085', 'desc': 'LED6MR16FL40/50/927/J/D/5', 'available': 3361}, {'item': '776514', 'desc': 'LED4A19/21K/FIL-NOS/CURV/LOOP', 'available': 3346}, {'item': '774264', 'desc': 'LED9A19/PF60W/940/D/2/1P', 'available': 3333}, {'item': '776835', 'desc': 'LED5G25/27K/FIL/HB/3', 'available': 3331}, {'item': '776221', 'desc': 'LED7G25/40K/FIL/D/B/2', 'available': 3310}, {'item': '776743', 'desc': 'LED4G16/27K/FIL/4/JA8', 'available': 3301}, {'item': '773222', 'desc': 'LED14JBOXDL/6/840/WHRD/D', 'available': 3290}, {'item': '770195', 'desc': 'LED/C9O', 'available': 3261}, {'item': '776834', 'desc': 'LED2G16/27K/FIL/HB/3', 'available': 3187}, {'item': '772764', 'desc': 'LED10PAR30S/FL40/827/WD/2', 'available': 3177}, {'item': '776943', 'desc': 'LED4G16/27K/FIL/M/4', 'available': 3159}, {'item': '776897', 'desc': 'LED8G40/27K/FIL/M/3', 'available': 3156}, {'item': '776726', 'desc': 'LED5T9/30K/7/FIL/F/3', 'available': 3100}, {'item': '774285', 'desc': 'LED5/9/14A19/PF100W/827/3WAY/1P', 'available': 3098}, {'item': '776725', 'desc': 'LED5T9/27K/7/FIL/F/3', 'available': 3091}, {'item': '776721', 'desc': 'LED5T9L/30K/15/FIL/3', 'available': 3090}, {'item': '776591', 'desc': 'LED4C11/21K/FIL/SPUN/AMB', 'available': 3057}, {'item': '770598', 'desc': 'LED3G9/30K/W/D', 'available': 3052}, {'item': '770591', 'desc': 'LED4G9/27K/120/F/D', 'available': 3031}, {'item': '772286', 'desc': 'LED10PAR30L/FL40/927/WD/2', 'available': 3030}, {'item': '776858', 'desc': 'LED2CA10/27K/FIL/E12/3', 'available': 3009}, {'item': '772861', 'desc': 'LED15BR40/830/D/5', 'available': 3005}, {'item': '772248', 'desc': 'LED10PAR30L/B-FL40/830/WD/2', 'available': 3002}, {'item': '772859', 'desc': 'LED11BR30/830/D/5', 'available': 3002}, {'item': '770614', 'desc': 'LED1/FEST/27K/24/2', 'available': 2986}, {'item': '776961', 'desc': 'LED14A19/50K/FIL/M/3', 'available': 2979}, {'item': '776773', 'desc': 'LED4B11/30K/FIL/M/3', 'available': 2935}, {'item': '776713', 'desc': 'LED5T9/21K/7/FIL-NOS/3', 'available': 2900}, {'item': '776321', 'desc': 'LED4C53/30K/FIL/GRAD/SMK', 'available': 2891}, {'item': '776825', 'desc': 'LED4A15/27K/FIL/E12/3', 'available': 2861}, {'item': '776933', 'desc': 'LED4B11/40K/FIL/M/3', 'available': 2849}, {'item': '776950', 'desc': 'LED2S14/27K/FIL/4', 'available': 2820}, {'item': '776594', 'desc': 'LED4T6SL/27K/FIL/3', 'available': 2783}, {'item': '776934', 'desc': 'LED5B11/40K/FIL/M/3', 'available': 2781}, {'item': '776928', 'desc': 'LED7A19/40K/FIL/M/3', 'available': 2759}, {'item': '774279', 'desc': 'LED15A19/P100W/930/GU24/J/D/1P', 'available': 2755}, {'item': '774266', 'desc': 'LED11A19/PF75W/927/D/2/1P', 'available': 2739}, {'item': '770171', 'desc': 'LED/C7C', 'available': 2738}, {'item': '770637', 'desc': 'LED6R7S/30K/S/D', 'available': 2731}, {'item': '774286', 'desc': 'LED5/9/14A19/PF100W/830/3WAY/1P', 'available': 2692}, {'item': '772265', 'desc': 'LED6PAR20/NFL25/930/WD/2', 'available': 2689}, {'item': '776929', 'desc': 'LED14A19/40K/FIL/M/3', 'available': 2653}, {'item': '776712', 'desc': 'LED4G16/30K/FIL/M/3', 'available': 2647}, {'item': '776917', 'desc': 'LED9A19/27K/FIL/M/4', 'available': 2622}, {'item': '776108', 'desc': 'LED4A19/GRN/FIL/D', 'available': 2607}, {'item': '773170', 'desc': 'LED9REC/4/927/WHRD-G/D', 'available': 2585}, {'item': '776742', 'desc': 'LED5CA10/30K/FIL/4/JA8', 'available': 2573}, {'item': '776521', 'desc': 'LED11A19/30K/FIL/3WAY', 'available': 2561}, {'item': '776926', 'desc': 'LED9A19/40K/FIL/3', 'available': 2538}, {'item': '776741', 'desc': 'LED5CA10/27K/FIL/4/JA8', 'available': 2528}, {'item': '770586', 'desc': 'LED2G4/27K/12', 'available': 2517}, {'item': '776151', 'desc': 'LED2S14/AMB/FIL/D', 'available': 2514}, {'item': '770596', 'desc': 'LED4E12/27K/120/F/D', 'available': 2498}, {'item': '776218', 'desc': 'LED7G25/27K/FIL/M/D/B/2', 'available': 2470}, {'item': '776208', 'desc': 'LED7A15/27K/FIL/D/B/2', 'available': 2445}, {'item': '773180', 'desc': 'LED14REC/5/6/927/WHRD-G/D', 'available': 2436}, {'item': '771087', 'desc': 'LED7MR16FL40/75/927/J/D/2', 'available': 2420}, {'item': '770580', 'desc': 'LED4G9/30K/120/F/D', 'available': 2389}, {'item': '773181', 'desc': 'LED14REC/5/6/930/WHRD-G/D', 'available': 2354}, {'item': '776106', 'desc': 'LED4A19/AMB/FIL/D', 'available': 2350}, {'item': '776110', 'desc': 'LED4A19/PNK/FIL/D', 'available': 2347}, {'item': '770583', 'desc': 'LED2WEDGE/30K/12', 'available': 2339}, {'item': '776994', 'desc': 'LED4T6/40K/FIL/M/3', 'available': 2339}, {'item': '770613', 'desc': 'LED1/FEST/30K/24/2', 'available': 2327}, {'item': '776954', 'desc': 'LED5A19/27K/FIL/M/3', 'available': 2326}, {'item': '773242', 'desc': 'LED9JBOXDL/4/940/WHRD/D', 'available': 2320}, {'item': '776516', 'desc': 'LED4G25/21K/FIL-NOS/CURV/SPIRAL', 'available': 2296}, {'item': '776909', 'desc': 'LED7ST18/21K/FIL-NOS/3', 'available': 2288}, {'item': '776927', 'desc': 'LED14A19/40K/FIL/3', 'available': 2255}, {'item': '770638', 'desc': 'LED10R7S/30K/L/D', 'available': 2251}, {'item': '776520', 'desc': 'LED11A19/27K/FIL/3WAY', 'available': 2237}, {'item': '776801', 'desc': 'LED5ST18/22K/FIL-NOS/3', 'available': 2232}, {'item': '776403', 'desc': 'LED5G16/30K-18K/WMDM/FIL/M', 'available': 2228}, {'item': '770626', 'desc': 'LED5GY6/30K/12', 'available': 2226}, {'item': '776922', 'desc': 'LED9A19/30K/FIL/M/4', 'available': 2220}, {'item': '776228', 'desc': 'LED7A19/40K/FIL/D/B/2/4P', 'available': 2211}, {'item': '776720', 'desc': 'LED5T9L/27K/15/FIL/3', 'available': 2200}, {'item': '773241', 'desc': 'LED9JBOXDL/4/930/WHRD/D', 'available': 2188}, {'item': '772261', 'desc': 'LED6PAR20/NFL25/927/WD/2', 'available': 2141}, {'item': '776213', 'desc': 'LED7A19/27K/FIL/M/D/B/2', 'available': 2116}, {'item': '776948', 'desc': 'LED3T9/27K/7/FIL/4', 'available': 2111}, {'item': '770648', 'desc': 'LED5G9/30K/120/D/2', 'available': 2066}, {'item': '776916', 'desc': 'LED14A19/30K/FIL/3', 'available': 2042}, {'item': '776918', 'desc': 'LED14A19/27K/FIL/M/3', 'available': 2031}, {'item': '770611', 'desc': 'LED1/FEST/30K/12/2', 'available': 2019}, {'item': '776231', 'desc': 'LED4B11/40K/FIL/D/B/2/6P', 'available': 2018}, {'item': '770196', 'desc': 'LED/C9P', 'available': 2015}, {'item': '772249', 'desc': 'LED10PAR30L/B-FL40/840/WD/2', 'available': 2010}, {'item': '770630', 'desc': 'LED5E11/30K/120/D', 'available': 1992}, {'item': '776972', 'desc': 'LED5CA10/30K/FIL/E26/M/3', 'available': 1971}, {'item': '776996', 'desc': 'LED4T6/50K/FIL/M/3', 'available': 1954}, {'item': '770619', 'desc': 'LED4DC/30K/D', 'available': 1947}, {'item': '776941', 'desc': 'LED5B11/30K/FIL/M/4', 'available': 1934}, {'item': '776932', 'desc': 'LED6B11/40K/FIL/3', 'available': 1928}, {'item': '776983', 'desc': 'LED8G40/50K/FIL/3', 'available': 1927}, {'item': '776824', 'desc': 'LED4ST15/30K/FIL/M/3', 'available': 1925}, {'item': '770597', 'desc': 'LED3G9/27K/W/D', 'available': 1912}, {'item': '776750', 'desc': 'LED8G25/30K/FIL/4/JA8', 'available': 1904}, {'item': '776984', 'desc': 'LED8G40/50K/FIL/M/3', 'available': 1894}, {'item': '776785', 'desc': 'LED1S14/27K/FIL/PL', 'available': 1892}, {'item': '770625', 'desc': 'LED5GY6/27K/12', 'available': 1885}, {'item': '772610', 'desc': 'LED18PAR38/FL40/927/J/WD', 'available': 1866}, {'item': '774246', 'desc': 'LED8A19/B60W/850/1P', 'available': 1866}, {'item': '776109', 'desc': 'LED4A19/BLU/FIL/D', 'available': 1856}, {'item': '770624', 'desc': 'LED4G4/30K/12', 'available': 1855}, {'item': '776322', 'desc': 'LED4C53/30K/FIL/GRAD/BLU', 'available': 1849}, {'item': '770577', 'desc': 'LED3G9/30K/120', 'available': 1842}, {'item': '776827', 'desc': 'LED4A15/27K/FIL/M/E12/3', 'available': 1838}, {'item': '772876', 'desc': 'LED15BR40/827/D/4', 'available': 1811}, {'item': '770622', 'desc': 'LED3G4/WA/27K/12', 'available': 1811}, {'item': '776942', 'desc': 'LED4CA10/27K/FIL/M/3', 'available': 1809}, {'item': '770650', 'desc': 'LED2G4/30K/W/D', 'available': 1802}, {'item': '770589', 'desc': 'LED3G9/27K/120', 'available': 1801}, {'item': '776971', 'desc': 'LED5CA10/30K/FIL/E26/3', 'available': 1798}, {'item': '776920', 'desc': 'LED6G40/27K/FIL/HM/3', 'available': 1783}, {'item': '770658', 'desc': 'LED4G9/30K/W/F/D', 'available': 1770}, {'item': '773171', 'desc': 'LED9REC/4/930/WHRD-G/D', 'available': 1761}, {'item': '773270', 'desc': 'LED18JBOXDL/8/927/WHRD/D', 'available': 1754}, {'item': '776993', 'desc': 'LED4T6/40K/FIL/3', 'available': 1628}, {'item': '773115', 'desc': 'LED9REC/4/927/WHRD/D', 'available': 1613}, {'item': '776878', 'desc': 'LED8G40/27K/FIL/3', 'available': 1606}, {'item': '776861', 'desc': 'LED4CA10/30K/FIL/M/3', 'available': 1560}, {'item': '776831', 'desc': 'LED7A15/27K/FIL/M/3', 'available': 1523}, {'item': '771105', 'desc': 'LED6PAR16FL40/50/830/D/5', 'available': 1516}, {'item': '770643', 'desc': 'LED6E12/30K/120/D', 'available': 1512}, {'item': '776899', 'desc': 'LED8G40/30K/FIL/M/3', 'available': 1511}, {'item': '776997', 'desc': 'LED4G40/30K/FIL/GRAD/SMK', 'available': 1508}, {'item': '776823', 'desc': 'LED4ST15/27K/FIL/M/3', 'available': 1502}, {'item': '776903', 'desc': 'LED2CA10/21K/FIL-NOS/3', 'available': 1501}, {'item': '772860', 'desc': 'LED15BR40/827/D/5', 'available': 1488}, {'item': '770645', 'desc': 'LED6G9/30K/120/D', 'available': 1483}, {'item': '772301', 'desc': 'LED15PAR38/NF25/930/WD/2', 'available': 1478}, {'item': '776105', 'desc': 'LED4A19/RED/FIL/D', 'available': 1475}, {'item': '770652', 'desc': 'LED2G4/30K/W/F/D', 'available': 1471}, {'item': '772855', 'desc': 'LED7BR20/830/D/5', 'available': 1471}, {'item': '776746', 'desc': 'LED13ST18/30K/FIL/3/JA8', 'available': 1470}, {'item': '773220', 'desc': 'LED14JBOXDL/6/827/WHRD/D', 'available': 1467}, {'item': '774249', 'desc': 'LED8A19/B60W/840/4P', 'available': 1454}, {'item': '771117', 'desc': 'LED6PAR16FL40/50/830/D/4', 'available': 1449}, {'item': '776946', 'desc': 'LED5T9L/30K/11/FIL/4', 'available': 1448}, {'item': '776722', 'desc': 'LED4T8/21K/FIL-NOS/3', 'available': 1443}, {'item': '776870', 'desc': 'LED5G25/27K/FIL/HM/3', 'available': 1423}, {'item': '776707', 'desc': 'LED5T9L/21K/11/FIL-NOS/3', 'available': 1422}, {'item': '776828', 'desc': 'LED4A15/30K/FIL/M/E12/3', 'available': 1417}, {'item': '776241', 'desc': 'LED7G25/40K/FIL/D/B/2/4P', 'available': 1417}, {'item': '770612', 'desc': 'LED1/FEST/27K/12/2', 'available': 1409}, {'item': '772768', 'desc': 'LED10PAR30S/FL40/830/WD/2', 'available': 1408}, {'item': '776915', 'desc': 'LED14A19/27K/FIL/3', 'available': 1385}, {'item': '776237', 'desc': 'LED5B11/27K/FIL/D/B/2/25P', 'available': 1385}, {'item': '776826', 'desc': 'LED4A15/30K/FIL/E12/3', 'available': 1384}, {'item': '776800', 'desc': 'LED5G25/22K/FIL-NOS/3', 'available': 1379}, {'item': '776944', 'desc': 'LED8G25/27K/FIL/M/3', 'available': 1362}, {'item': '776229', 'desc': 'LED4B11/27K/FIL/D/B/2/6P', 'available': 1362}, {'item': '773152', 'desc': 'LED20DL/9/927/WHRD/J/D', 'available': 1359}, {'item': '772502', 'desc': 'LED15PAR38/FL/YLW/D', 'available': 1353}, {'item': '776232', 'desc': 'LED5B11/27K/FIL/D/B/2/6P', 'available': 1338}, {'item': '770651', 'desc': 'LED2G4/27K/W/F/D', 'available': 1336}, {'item': '776234', 'desc': 'LED5B11/40K/FIL/D/B/2/6P', 'available': 1333}, {'item': '776401', 'desc': 'LED5B11/30K-18K/WMDM/FIL/M', 'available': 1330}, {'item': '770576', 'desc': 'LED4GY8/30K/120/D', 'available': 1322}, {'item': '776406', 'desc': 'LED4G40/30K-18K/WMDM/FIL/M', 'available': 1319}, {'item': '776939', 'desc': 'LED4B11/27K/FIL/M/3', 'available': 1318}, {'item': '776730', 'desc': 'LED4T6/30K/FIL/M/3', 'available': 1316}, {'item': '776235', 'desc': 'LED4B11/27K/FIL/D/B/2/25P', 'available': 1314}, {'item': '776734', 'desc': 'LED5B11/30K/FIL/E26/3', 'available': 1299}, {'item': '774247', 'desc': 'LED8A19/B60W/827/4P', 'available': 1299}, {'item': '770604', 'desc': 'LED/LI4T8/27K', 'available': 1285}, {'item': '772854', 'desc': 'LED7BR20/827/D/5', 'available': 1280}, {'item': '772505', 'desc': 'LED15PAR38/FL/PNK/D', 'available': 1268}, {'item': '776738', 'desc': 'LED6B11/30K/FIL/3', 'available': 1266}, {'item': '772503', 'desc': 'LED15PAR38/FL/GRN/D', 'available': 1261}, {'item': '776830', 'desc': 'LED7A15/30K/FIL/3', 'available': 1256}, {'item': '776740', 'desc': 'LED6CA10/30K/FIL/3', 'available': 1253}, {'item': '776919', 'desc': 'LED14A19/30K/FIL/M/3', 'available': 1248}, {'item': '770585', 'desc': 'LED4E12/30K/120/F/D', 'available': 1242}, {'item': '776787', 'desc': 'LED5CA10/27K/FIL/M/3', 'available': 1240}, {'item': '772290', 'desc': 'LED10PAR30L/FL40/930/WD/2', 'available': 1233}, {'item': '773146', 'desc': 'LED15DL/7/927/WHSQ/J/D', 'available': 1216}, {'item': '776595', 'desc': 'LED4T6SL/30K/FIL/3', 'available': 1216}, {'item': '772278', 'desc': 'LED10PAR30S/FL40/930/WD/2', 'available': 1207}, {'item': '776239', 'desc': 'LED7G25/27K/FIL/D/B/2/4P', 'available': 1201}, {'item': '776748', 'desc': 'LED13G25/30K/FIL/3/JA8', 'available': 1200}, {'item': '776238', 'desc': 'LED5B11/30K/FIL/D/B/2/25P', 'available': 1199}, {'item': '770593', 'desc': 'LED4E11/27K/120/F/D', 'available': 1195}, {'item': '770581', 'desc': 'LED4E11/30K/120/D', 'available': 1182}, {'item': '776921', 'desc': 'LED2G16/27K/FIL/HG/3', 'available': 1179}, {'item': '772274', 'desc': 'LED10PAR30S/FL40/927/WD/2', 'available': 1176}, {'item': '772500', 'desc': 'LED15PAR38/FL/RED/D', 'available': 1169}, {'item': '771108', 'desc': 'LED6PAR16GUFL40/50/927/J/D/2', 'available': 1165}, {'item': '776210', 'desc': 'LED7A15/30K/FIL/D/B/2', 'available': 1145}, {'item': '770623', 'desc': 'LED4G4/27K/12', 'available': 1136}, {'item': '776107', 'desc': 'LED4A19/YLW/FIL/D', 'available': 1135}, {'item': '772504', 'desc': 'LED15PAR38/FL/BLU/D', 'available': 1124}, {'item': '774240', 'desc': 'LED9A19/P60W/940/J/D/1P', 'available': 1123}, {'item': '776735', 'desc': 'LED5B11/27K/FIL/M/E26/3', 'available': 1120}, {'item': '776226', 'desc': 'LED7A19/27K/FIL/D/B/2/4P', 'available': 1113}, {'item': '772858', 'desc': 'LED11BR30/827/D/5', 'available': 1094}, {'item': '776306', 'desc': 'LED4OLIVE/22K/FIL', 'available': 1089}, {'item': '776747', 'desc': 'LED13G25/27K/FIL/3/JA8', 'available': 1071}, {'item': '770152', 'desc': 'LED/G14G', 'available': 1049}, {'item': '773125', 'desc': 'LED11JBOXDL/6/827/WHRD/D', 'available': 1038}, {'item': '776318', 'desc': 'LED4JEWEL/20K/FIL-NOS', 'available': 1037}, {'item': '774254', 'desc': 'LED9A19/PF60W/930/D/2/4P', 'available': 1035}, {'item': '772865', 'desc': 'LED7R20/830/D/4', 'available': 1013}, {'item': '772298', 'desc': 'LED15PAR38/FL40/927/WD/2', 'available': 994}, {'item': '774253', 'desc': 'LED9A19/PF60W/927/D/2/4P', 'available': 984}, {'item': '776153', 'desc': 'LED2S14/GRN/FIL/D', 'available': 983}, {'item': '774256', 'desc': 'LED9A19/PF60W/950/D/2/4P', 'available': 982}, {'item': '776209', 'desc': 'LED7A15/27K/FIL/M/D/B/2', 'available': 967}, {'item': '774250', 'desc': 'LED8A19/B60W/850/4P', 'available': 964}, {'item': '776792', 'desc': 'LED5T9/30K/5/FIL/F/3', 'available': 963}, {'item': '770594', 'desc': 'LED2WEDGE/27K/12', 'available': 961}, {'item': '774283', 'desc': 'LED9A19/P60W/927/GU24/J/D/2/1P', 'available': 958}, {'item': '776222', 'desc': 'LED7G25/40K/FIL/M/D/B/2', 'available': 941}, {'item': '776737', 'desc': 'LED6B11/27K/FIL/3', 'available': 939}, {'item': '776400', 'desc': 'LED9A19/30K-18K/WMDM/FIL/M', 'available': 930}, {'item': '770599', 'desc': 'LED4G9/27K/W/D', 'available': 929}, {'item': '776879', 'desc': 'LED8G40/30K/FIL/3', 'available': 928}, {'item': '772501', 'desc': 'LED15PAR38/FL/AMB/D', 'available': 917}, {'item': '770641', 'desc': 'LED6E11/30K/120/D', 'available': 905}, {'item': '770620', 'desc': 'LED4DC/27K/D', 'available': 888}, {'item': '776819', 'desc': 'LED5T14/27K/FIL/3', 'available': 884}, {'item': '776155', 'desc': 'LED2S14/PNK/FIL/D', 'available': 861}, {'item': '770616', 'desc': 'LED4GY6/27K/D/2', 'available': 860}, {'item': '770584', 'desc': 'LED4E12/30K/120/D', 'available': 849}, {'item': '770600', 'desc': 'LED4G9/30K/W/D', 'available': 848}, {'item': '770660', 'desc': 'LED3G9/30K/W/F/D', 'available': 837}, {'item': '776728', 'desc': 'LED5T9/30K/11/FIL/F/3', 'available': 834}, {'item': '770656', 'desc': 'LED2GY6/30K/12/W/F/D', 'available': 827}, {'item': '776924', 'desc': 'LED6G40/27K/FIL/HG/3', 'available': 826}, {'item': '776998', 'desc': 'LED4G40/30K/FIL/GRAD/BLU', 'available': 806}, {'item': '776739', 'desc': 'LED6CA10/27K/FIL/3', 'available': 799}, {'item': '776317', 'desc': 'LED4DROP/20K/FIL-NOS', 'available': 796}, {'item': '776243', 'desc': 'LED7ST18/30K/FIL/D/B/2/4P', 'available': 793}, {'item': '770632', 'desc': 'LED5E12/30K/120/D', 'available': 785}, {'item': '776515', 'desc': 'LED3ST18/21K/FIL-NOS/CURV/HAIRPIN', 'available': 780}, {'item': '772767', 'desc': 'LED10PAR30S/NF25/830/WD/2', 'available': 756}, {'item': '770629', 'desc': 'LED5E11/27K/120/D', 'available': 755}, {'item': '776771', 'desc': 'LED2G16/27K/FIL/HM/3', 'available': 755}, {'item': '776820', 'desc': 'LED5T14/30K/FIL/3', 'available': 735}, {'item': '776152', 'desc': 'LED2S14/YLW/FIL/D', 'available': 732}, {'item': '770649', 'desc': 'LED2G4/27K/W/D', 'available': 731}, {'item': '774251', 'desc': 'LED8A19/B60W/827/25P', 'available': 725}, {'item': '776101', 'desc': 'LED27T5/48/840/DIR', 'available': 723}, {'item': '770571', 'desc': 'LED2G4/30K/12', 'available': 715}, {'item': '776810', 'desc': 'LED8G25/30K/FIL/M/3', 'available': 714}, {'item': '776150', 'desc': 'LED2S14/RED/FIL/D', 'available': 688}, {'item': '774242', 'desc': 'LED9A19/P60W/930/GU24/J/D/1P', 'available': 679}, {'item': '770587', 'desc': 'LED3G4/27K/12', 'available': 664}, {'item': '772792', 'desc': 'LED15PAR38/FL40/830/WD/2', 'available': 662}, {'item': '770647', 'desc': 'LED5G9/27K/120/D/2', 'available': 655}, {'item': '770653', 'desc': 'LED2GY6/27K/12/W/D', 'available': 654}, {'item': '776706', 'desc': 'LED2G16/27K/FIL/3', 'available': 641}, {'item': '772775', 'desc': 'LED10PAR30L/NF25/827/WD/2', 'available': 641}, {'item': '776908', 'desc': 'LED3T9/21K/FIL-NOS/3', 'available': 638}, {'item': '776923', 'desc': 'LED4G25/27K/FIL/HG/3', 'available': 633}, {'item': '776230', 'desc': 'LED4B11/30K/FIL/D/B/2/6P', 'available': 631}, {'item': '776154', 'desc': 'LED2S14/BLU/FIL/D', 'available': 618}, {'item': '776005', 'desc': 'LED20T8/30K', 'available': 616}, {'item': '770590', 'desc': 'LED4G9/27K/120/D', 'available': 608}, {'item': '776242', 'desc': 'LED7ST18/27K/FIL/D/B/2/4P', 'available': 605}, {'item': '776822', 'desc': 'LED4ST15/30K/FIL/3', 'available': 599}, {'item': '770654', 'desc': 'LED2GY6/30K/12/W/D', 'available': 595}, {'item': '774258', 'desc': 'LED9A19/PF60W/930/D/2/25P', 'available': 567}, {'item': '776871', 'desc': 'LED2A19/27K/FIL/3', 'available': 561}, {'item': '776302', 'desc': 'LED4G63/22K/FIL', 'available': 559}, {'item': '776745', 'desc': 'LED13ST18/27K/FIL/3/JA8', 'available': 540}, {'item': '770631', 'desc': 'LED5E12/27K/120/D', 'available': 506}, {'item': '776854', 'desc': 'LED3T9/30K/FIL/3', 'available': 504}, {'item': '776940', 'desc': 'LED5B11/27K/FIL/M/4', 'available': 499}, {'item': '772262', 'desc': 'LED6PAR20/FL40/927/WD/2', 'available': 477}, {'item': '772779', 'desc': 'LED10PAR30L/NF25/830/WD/2', 'available': 469}, {'item': '770655', 'desc': 'LED2GY6/27K/12/W/F/D', 'available': 438}, {'item': '770621', 'desc': 'LED3G4/WA/30K/12', 'available': 434}, {'item': '770588', 'desc': 'LED4GY8/27K/120/D', 'available': 416}, {'item': '776211', 'desc': 'LED7A15/30K/FIL/M/D/B/2', 'available': 387}, {'item': '770194', 'desc': 'LED/C9G', 'available': 375}, {'item': '770618', 'desc': 'LED4SC/27K/12', 'available': 373}, {'item': '776233', 'desc': 'LED5B11/30K/FIL/D/B/2/6P', 'available': 369}, {'item': '770640', 'desc': 'LED6E11/27K/120/D', 'available': 367}, {'item': '776518', 'desc': 'LED4T14/21K/FIL-NOS/CURV/SPIRAL', 'available': 357}, {'item': '770644', 'desc': 'LED6G9/27K/120/D', 'available': 340}, {'item': '776679', 'desc': 'LED5A19/27K/FIL/HG/3', 'available': 328}, {'item': '776596', 'desc': 'LED4PRISM/30K/FIL/3', 'available': 296}, {'item': '772266', 'desc': 'LED6PAR20/FL40/930/WD/2', 'available': 276}, {'item': '776727', 'desc': 'LED5T9/27K/11/FIL/F/3', 'available': 269}, {'item': '772756', 'desc': 'LED7PAR20/FL40/830/WD/2', 'available': 265}, {'item': '773158', 'desc': 'LED20DL/9/927/WHSQ/J/D', 'available': 259}, {'item': '776821', 'desc': 'LED4ST15/27K/FIL/3', 'available': 258}, {'item': '776227', 'desc': 'LED7A19/30K/FIL/D/B/2/4P', 'available': 231}, {'item': '776240', 'desc': 'LED7G25/30K/FIL/D/B/2/4P', 'available': 197}, {'item': '776905', 'desc': 'LED4T14/21K/FIL-NOS/3', 'available': 190}, {'item': '774257', 'desc': 'LED9A19/PF60W/927/D/2/25P', 'available': 185}, {'item': '776788', 'desc': 'LED5CA10/30K/FIL/M/3', 'available': 179}, {'item': '776244', 'desc': 'LED7ST18/40K/FIL/D/B/2/4P', 'available': 155}, {'item': '774276', 'desc': 'LED15A19/P100W/927/J/D/1P', 'available': 150}, {'item': '776314', 'desc': 'LED4BT56/22K/FIL', 'available': 147}, {'item': '770659', 'desc': 'LED3G9/27K/W/F/D', 'available': 144}, {'item': '776736', 'desc': 'LED5B11/30K/FIL/M/E26/3', 'available': 140}, {'item': '770615', 'desc': 'LED4GY6/30K/D/2', 'available': 112}, {'item': '776305', 'desc': 'LED4DIA/22K/FIL', 'available': 86}, {'item': '772763', 'desc': 'LED10PAR30S/NF25/827/WD/2', 'available': 77}, {'item': '777801', 'desc': 'AC-CC-0002-00-S1', 'available': 74}, {'item': '777902', 'desc': 'SR111-18-36D-927-03', 'available': 68}, {'item': '776301', 'desc': 'LED4ET25/22K/FIL', 'available': 66}, {'item': '776304', 'desc': 'LED4BH/22K/FIL', 'available': 66}, {'item': '777252', 'desc': 'SP20-11-10D-927-03', 'available': 53}, {'item': '776300', 'desc': 'LED4PS52/22K/FIL', 'available': 51}, {'item': '777803', 'desc': 'AC-GC-2525-00-S1', 'available': 40}, {'item': '777809', 'desc': 'AC-FR-3636-00-S1', 'available': 35}, {'item': '777679', 'desc': 'SP38-14-60D-827-H1', 'available': 30}, {'item': '777823', 'desc': 'AC-E-GC-2525-00-S1', 'available': 25}, {'item': '772717', 'desc': 'LED7PAR20/NF25/840/WD', 'available': 23}, {'item': '771208', 'desc': 'LED6MR16FL35/50/830/D', 'available': 21}, {'item': '777766', 'desc': 'SP38-18-36D-930-03', 'available': 14}, {'item': '777700', 'desc': 'SP30L-18-09D-927-03', 'available': 12}, {'item': '777721', 'desc': 'SP30S-18-25D-927-03', 'available': 10}, {'item': '777681', 'desc': 'SP38-14-25D-830-H1', 'available': 10}, {'item': '774260', 'desc': 'LED11A19/PF75W/927/D/1P', 'available': 10}, {'item': '777661', 'desc': 'SP30L-14-25D-827-H1', 'available': 10}, {'item': '773230', 'desc': 'LED7JBOXDL/3/927/WHRD/D', 'available': 9}, {'item': '777827', 'desc': 'AC-E-GE-1036-00-S1', 'available': 9}, {'item': '776320', 'desc': 'LED4GLACIER/20K/FIL-NOS', 'available': 9}, {'item': '774252', 'desc': 'LED8A19/B60W/830/25P', 'available': 8}, {'item': '777707', 'desc': 'SP30L-18-60D-930-03', 'available': 6}, {'item': '777235', 'desc': 'SP20-11-36D-830-H1', 'available': 6}, {'item': '777764', 'desc': 'SP38-18-09D-930-03', 'available': 5}, {'item': '777579', 'desc': 'SM16GA-09-60D-930-03', 'available': 5}, {'item': '777046', 'desc': 'SM16-09-25D-827-H1', 'available': 4}, {'item': '777670', 'desc': 'SP30S-14-36D-827-H1', 'available': 4}, {'item': '777722', 'desc': 'SP30S-18-36D-927-03', 'available': 4}, {'item': '772776', 'desc': 'LED10PAR30L/FL40/827/WD/2', 'available': 3}, {'item': '777931', 'desc': 'SR111-12-25D-927-03', 'available': 3}, {'item': '777683', 'desc': 'SP38-14-60D-830-H1', 'available': 3}, {'item': '777532', 'desc': 'SM16GA-09-60D-827-H1', 'available': 3}, {'item': '777723', 'desc': 'SP30S-18-60D-927-03', 'available': 3}, {'item': '777660', 'desc': 'SP30L-14-09D-827-H1', 'available': 3}, {'item': '777760', 'desc': 'SP38-18-09D-927-03', 'available': 3}, {'item': '777253', 'desc': 'SP20-11-10D-930-03', 'available': 2}, {'item': '777265', 'desc': 'SP20-11-36D-930-03', 'available': 2}, {'item': '777576', 'desc': 'SM16GA-09-36D-927-03', 'available': 2}, {'item': '777726', 'desc': 'SP30S-18-36D-930-03', 'available': 2}, {'item': '777702', 'desc': 'SP30L-18-36D-927-03', 'available': 2}, {'item': '777814', 'desc': 'AC-E-AM-0020-00-S1', 'available': 2}, {'item': '777828', 'desc': 'AC-E-FR-3636-00-S1', 'available': 2}, {'item': '777059', 'desc': 'SM16-07-36D-930-03', 'available': 2}, {'item': '777821', 'desc': 'AC-E-CC-0002-00-S1', 'available': 1}, {'item': '777048', 'desc': 'SM16-09-25D-830-H1', 'available': 1}, {'item': '777767', 'desc': 'SP38-18-60D-930-03', 'available': 1}, {'item': '777802', 'desc': 'AC-CC-0003-00-S1', 'available': 1}, {'item': '777673', 'desc': 'SP30S-14-25D-830-H1', 'available': 1}, {'item': '777815', 'desc': 'AC-E-EN-0001-00-S1', 'available': 1}, {'item': '777259', 'desc': 'SP20-11-25D-930-03', 'available': 1}, {'item': '777521', 'desc': 'SM16GA-07-10D-830-H1', 'available': 1}, {'item': '777533', 'desc': 'SM16GA-09-60D-830-H1', 'available': 1}, {'item': '777832', 'desc': 'SR111-19-36DM-927/918-01', 'available': 1}, {'item': '777578', 'desc': 'SM16GA-09-60D-927-03', 'available': 1}, {'item': '777724', 'desc': 'SP30S-18-09D-930-03', 'available': 1}, {'item': '777900', 'desc': 'SR111-18-09D-927-03', 'available': 1}] |
| 712160 | 60A19HM | COL1 | 61,565.82 | 27,011 | — | 2026-7-10 | [{'customer': 'LIGHTING N BEYOND LLC', 'revenue': 23646.81}, {'customer': 'CFA TRADING', 'revenue': 11927.34}, {'customer': 'Parallax Industries Inc. dba Square Deal Shop', 'revenue': 7716.86}, {'customer': 'LIGHTING GETZ CORP.', 'revenue': 3627.88}, {'customer': 'The Urban Electric Company', 'revenue': 3373.31}, {'customer': 'BULBS.COM', 'revenue': 2362.26}, {'customer': 'Decora Lighting Corp', 'revenue': 1377.37}, {'customer': 'EXWAY ELECTRIC SUPPLY CO', 'revenue': 962.06}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 924.83}, {'customer': 'New Age America Inc.', 'revenue': 879.51}, {'customer': 'SERVICE LIGHTING (MN)', 'revenue': 722.39}, {'customer': 'LSC HOLDINGS INC, dba LIGHTING SUPPLY', 'revenue': 485.97}, {'customer': 'REXEL CLS HARTFORD,CT', 'revenue': 456.74}, {'customer': 'Bulbs NYC Inc', 'revenue': 422.25}, {'customer': 'GRAND BRASS LAMP PARTS INC', 'revenue': 332.68}, {'customer': 'ROYAL LIGHTING', 'revenue': 287.87}, {'customer': 'MP III LTD', 'revenue': 278.89}, {'customer': 'BULBTRONICS INC', 'revenue': 186.4}, {'customer': 'REAL LIGHTING INC.', 'revenue': 183.58}, {'customer': 'LIGHT BULBS & MORE INC', 'revenue': 157.42}, {'customer': 'SUNLAN LIGHTING INC', 'revenue': 151.37}, {'customer': 'ATR LIGHTING ENTERPRISES INC', 'revenue': 148.6}, {'customer': 'NEW BULBS WORLD', 'revenue': 110.75}, {'customer': 'LIGHT BULBS UNLIMITED', 'revenue': 106.39}, {'customer': 'CANAL BULBS AND PARTS INC', 'revenue': 104.96}, {'customer': 'JUST BULBS THE LIGHT BULB STORE', 'revenue': 93.59}, {'customer': 'HOUSE OF ASIA', 'revenue': 75.66}, {'customer': 'BRAND NAME LIGHTING', 'revenue': 60.35}, {'customer': 'LIGHT SOURCE', 'revenue': 52.98}, {'customer': 'Lightbulb Wholesaler Inc.', 'revenue': 45.58}, {'customer': 'G & G ELECTRIC SUPPLY', 'revenue': 44.38}, {'customer': 'Alton Hardgoods Company LLC', 'revenue': 43.99}, {'customer': 'WATTSAVER LIGHTING PRODUCTS', 'revenue': 43.0}, {'customer': 'INCON INDUSTRIES', 'revenue': 40.05}, {'customer': 'COLUMBIA OMNI CORP', 'revenue': 36.6}, {'customer': 'HD Supply', 'revenue': 25.25}, {'customer': 'EUROLITE INC', 'revenue': 20.47}, {'customer': 'FLEMINGS', 'revenue': 19.76}, {'customer': 'RITTENHOUSE ELECTRIC SUPPLY CO', 'revenue': 17.14}, {'customer': 'Light by Alexandria Electric', 'revenue': 16.06}, {'customer': 'LIGHTOLOGY (ECOMM)', 'revenue': 0.0}, {'customer': '1800LIGHTING.COM', 'revenue': 0.0}, {'customer': 'ADAMS PARNELL AGENCY dba LIGHTING VIRGINIA', 'revenue': 0.0}, {'customer': 'PORT LIGHTING SYSTEMS', 'revenue': 0.0}, {'customer': 'DEL MAR DESIGNS', 'revenue': 0.0}, {'customer': 'MAIN ELECTRIC SUPPLY CO INC', 'revenue': 0.0}, {'customer': 'MNH Inc', 'revenue': 0.0}, {'customer': 'CONSERVA ELECTRIC SUPPLY, INC', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 0.0}, {'customer': 'RIVERSIDE LIGHTING INC', 'revenue': 0.0}, {'customer': 'Bluecom, LLC DBA SupplyStop', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 0.0}, {'customer': 'GOODBULB LLC', 'revenue': 0.0}, {'customer': 'BARN LIGHT ELECTRIC COMPANY LLC', 'revenue': 0.0}, {'customer': 'Bulbrite Industries Inc', 'revenue': -3.53}] | [{'item': '393002', 'desc': '25G25WH2', 'available': 26409}, {'item': '403307', 'desc': '7.5CFC/15/3', 'available': 23423}, {'item': '134018', 'desc': 'NOS40-1890', 'available': 22003}, {'item': '144015', 'desc': '40G25/ICE', 'available': 19416}, {'item': '134019', 'desc': 'NOS40-1910', 'available': 15465}, {'item': '707503', 'desc': '9T6.5C', 'available': 13861}, {'item': '706114', 'desc': '25T7/DC', 'available': 12280}, {'item': '708115', 'desc': '15T4/130V', 'available': 11586}, {'item': '706110', 'desc': '15T7/DC', 'available': 11492}, {'item': '144026', 'desc': '40G16/MAR/E12', 'available': 10727}, {'item': '707502', 'desc': '9T6.5C/DC', 'available': 9792}, {'item': '144024', 'desc': '25G16/MAR/E12', 'available': 9230}, {'item': '144025', 'desc': '40G25/MAR', 'available': 9059}, {'item': '132510', 'desc': 'NOS25ST15/SQ/E12', 'available': 8523}, {'item': '702007', 'desc': '7.5S11W', 'available': 8422}, {'item': '301040', 'desc': '40G12CL', 'available': 7416}, {'item': '381125', 'desc': 'B25G16CL', 'available': 7403}, {'item': '784160', 'desc': 'B60T10C', 'available': 4798}, {'item': '784025', 'desc': 'B25T10F', 'available': 4784}, {'item': '705140', 'desc': '40T8C', 'available': 4674}, {'item': '340040', 'desc': '40G30WH', 'available': 4547}, {'item': '414025', 'desc': '25CTD/C/2', 'available': 4247}, {'item': '705175', 'desc': '75T8C', 'available': 3869}, {'item': '430040', 'desc': '40C11S', 'available': 3797}, {'item': '104140', 'desc': '40A15C', 'available': 3542}, {'item': '712424', 'desc': '40G25HG', 'available': 3401}, {'item': '136020', 'desc': 'NOS60-VICTOR', 'available': 3390}, {'item': '411006', 'desc': 'SF/6S6', 'available': 3375}, {'item': '403140', 'desc': '40CFC/25/3', 'available': 3211}, {'item': '411007', 'desc': 'SF/7.5S11', 'available': 3179}, {'item': '101025', 'desc': '25A/CL', 'available': 3140}, {'item': '493125', 'desc': '25CFC/25/2', 'available': 3063}, {'item': '400425', 'desc': '25CTC/E14', 'available': 2841}, {'item': '712416', 'desc': '60A19HG', 'available': 2818}, {'item': '134008', 'desc': 'NOS40T9/L', 'available': 2777}, {'item': '108040', 'desc': '40A15/TF', 'available': 2763}, {'item': '351025', 'desc': '25G40CL', 'available': 2640}, {'item': '701511', 'desc': '11S14TPU', 'available': 2610}, {'item': '701611', 'desc': '11S14TPK', 'available': 2601}, {'item': '350100', 'desc': '100G40WH', 'available': 2531}, {'item': '342040', 'desc': 'NOS40G30', 'available': 2434}, {'item': '701311', 'desc': '11S14TB', 'available': 2404}, {'item': '495040', 'desc': '40ETC/2', 'available': 2199}, {'item': '134020', 'desc': 'NOS40-VICTOR', 'available': 2119}, {'item': '133009', 'desc': 'NOS30T9', 'available': 2104}, {'item': '701811', 'desc': '11S14TY', 'available': 2081}, {'item': '702107', 'desc': '7.5S11C', 'available': 2071}, {'item': '351100', 'desc': '100G40CL', 'available': 2064}, {'item': '411003', 'desc': 'SF/F3CTC', 'available': 2033}, {'item': '430025', 'desc': '25C11S', 'available': 1999}, {'item': '100025', 'desc': '25A', 'available': 1985}, {'item': '709607', 'desc': '7C7P', 'available': 1970}, {'item': '132506', 'desc': 'NOS25T6/SQ/E12', 'available': 1946}, {'item': '137501', 'desc': 'NOS60-WB', 'available': 1940}, {'item': '311015', 'desc': '15G16CL3', 'available': 1914}, {'item': '712351', 'desc': '100G40HM', 'available': 1873}, {'item': '134015', 'desc': 'NOS40T14/SQ', 'available': 1807}, {'item': '420225', 'desc': '25F10A', 'available': 1704}, {'item': '784140', 'desc': 'B40T10C', 'available': 1696}, {'item': '400115', 'desc': '15CTC/25/3', 'available': 1628}, {'item': '351060', 'desc': '60G40CL', 'available': 1515}, {'item': '704025', 'desc': '25T10F', 'available': 1479}, {'item': '311225', 'desc': '25G16ECL', 'available': 1448}, {'item': '489025', 'desc': 'B25EFF', 'available': 1439}, {'item': '400025', 'desc': '25CTC/32/3', 'available': 1414}, {'item': '701211', 'desc': '11S14TA', 'available': 1359}, {'item': '351040', 'desc': '40G40CL', 'available': 1292}, {'item': '712312', 'desc': '25G16HM', 'available': 1285}, {'item': '134014', 'desc': 'NOS40T14', 'available': 1274}, {'item': '132507', 'desc': '25T6/SQ/E12', 'available': 1147}, {'item': '350150', 'desc': '150G40WH', 'available': 1136}, {'item': '704125', 'desc': '25T10C', 'available': 1120}, {'item': '707501', 'desc': '9T6.5C/N', 'available': 1096}, {'item': '431040', 'desc': '40C15S', 'available': 1080}, {'item': '391115', 'desc': '15G16CL2', 'available': 1000}, {'item': '712314', 'desc': '40G16HM', 'available': 965}, {'item': '110025', 'desc': '25A19F/12', 'available': 951}, {'item': '393004', 'desc': '40G25WH2', 'available': 946}, {'item': '493115', 'desc': '15CFC/25/2', 'available': 917}, {'item': '712110', 'desc': '100A21HM', 'available': 910}, {'item': '712336', 'desc': '60G25HM', 'available': 898}, {'item': '708106', 'desc': '6T4/130V', 'available': 893}, {'item': '701711', 'desc': '11S14TR', 'available': 866}, {'item': '350040', 'desc': '40G40WH', 'available': 824}, {'item': '490025', 'desc': '25CTC/32/2', 'available': 810}, {'item': '330025', 'desc': '25G25WH3', 'available': 804}, {'item': '490125', 'desc': '25CTC/25/2', 'available': 788}, {'item': '712331', 'desc': '100G25HM', 'available': 787}, {'item': '400125', 'desc': '25CTC/25/3', 'available': 762}, {'item': '403040', 'desc': '40CFC/32/3', 'available': 732}, {'item': '421025', 'desc': '25F15WH', 'available': 702}, {'item': '784060', 'desc': 'B60T10F', 'available': 700}, {'item': '705040', 'desc': '40T8F', 'available': 681}, {'item': '701411', 'desc': '11S14TG', 'available': 675}, {'item': '144016', 'desc': '40G16/ICE/E12', 'available': 616}, {'item': '480140', 'desc': 'B40PRISM', 'available': 604}, {'item': '350025', 'desc': '25G40WH', 'available': 575}, {'item': '704340', 'desc': '40T10C/HO', 'available': 550}, {'item': '420215', 'desc': '15F10A', 'available': 513}, {'item': '300010', 'desc': '10G12WH', 'available': 476}, {'item': '403025', 'desc': '25CFC/32/3', 'available': 470}, {'item': '707115', 'desc': '15T6', 'available': 454}, {'item': '431025', 'desc': '25C15S', 'available': 428}, {'item': '706115', 'desc': '15T7', 'available': 419}, {'item': '421225', 'desc': '25F15A', 'available': 393}, {'item': '408040', 'desc': '40EFC/3', 'available': 370}, {'item': '712356', 'desc': '60G40HM', 'available': 344}, {'item': '705075', 'desc': '75T8F', 'available': 174}, {'item': '493025', 'desc': '25CFC/32/2', 'available': 162}, {'item': '784115', 'desc': 'B15T10C', 'available': 150}, {'item': '300025', 'desc': '25G12WH', 'available': 127}, {'item': '132520', 'desc': 'NOS25-VICTOR', 'available': 124}, {'item': '137701', 'desc': 'NOS60-DIAMOND', 'available': 123}, {'item': '393102', 'desc': '25G25CL2', 'available': 102}, {'item': '137601', 'desc': 'NOS60-BH', 'available': 85}, {'item': '712334', 'desc': '40G25HM', 'available': 75}, {'item': '137401', 'desc': 'NOS60-GLOBE', 'available': 43}, {'item': '701111', 'desc': '11S14C', 'available': 40}, {'item': '701911', 'desc': '11S14F', 'available': 24}, {'item': '137101', 'desc': 'NOS60-PS', 'available': 22}, {'item': '330040', 'desc': '40G25WH3', 'available': 19}, {'item': '701011', 'desc': '11S14W', 'available': 15}, {'item': '137301', 'desc': 'NOS60-ET', 'available': 10}] |
| 776869 | LED8A19/30K/FIL/M/3 | LED | 60,846.17 | 10,159 | — | 2026-6-19 | [{'customer': 'KENDALL ELECTRIC INC', 'revenue': 17465.12}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 5289.01}, {'customer': 'CONNECTICUT LIGHTING CENTER', 'revenue': 3441.67}, {'customer': 'SERVICE LIGHTING (MN)', 'revenue': 3281.74}, {'customer': 'KLS LLC dba SPECTRUM LIGHTING', 'revenue': 2807.13}, {'customer': 'CAROLINA LANTERNS', 'revenue': 2720.49}, {'customer': 'LUMENAREA', 'revenue': 2560.32}, {'customer': 'CAPITOL LIGHTING - NJ location', 'revenue': 2118.04}, {'customer': 'SOUTHERN LIGHTS, INC.', 'revenue': 2112.63}, {'customer': 'CAPITOL LIGHTING - FL location', 'revenue': 1788.12}, {'customer': 'HARRY HORN INC', 'revenue': 1628.45}, {'customer': 'VALLEY LIGHT GALLERY', 'revenue': 993.52}, {'customer': 'GROSS ELECTRIC, INC.', 'revenue': 980.02}, {'customer': 'CED dba ALL-PHASE ELECTRIC PETOSKEY', 'revenue': 975.1}, {'customer': 'Gross Lighting & Home - Howell, MI', 'revenue': 697.01}, {'customer': '1800LIGHTING.COM', 'revenue': 695.46}, {'customer': 'DOLAN NW LLC - DBA SEATTLE LIGHTING', 'revenue': 685.52}, {'customer': 'Light by Alexandria Electric', 'revenue': 645.53}, {'customer': 'Gross Lighting & Home - Indianapolis, IN', 'revenue': 635.1}, {'customer': 'WARSHAUER ELECTRIC', 'revenue': 551.43}, {'customer': 'LIGHTING SOUTH LLC', 'revenue': 546.69}, {'customer': 'EXWAY ELECTRIC SUPPLY CO', 'revenue': 521.15}, {'customer': 'LIGHT & DAY LLC', 'revenue': 460.54}, {'customer': 'DOLAN NW LLC -DBA GLOBE LIGHTING', 'revenue': 451.73}, {'customer': 'LYTEWORKS INC', 'revenue': 451.67}, {'customer': 'IMAGINE MORE SERVICE CORP', 'revenue': 412.98}, {'customer': 'Lighting first', 'revenue': 382.41}, {'customer': 'Vox Lumen, LLC', 'revenue': 320.98}, {'customer': 'NEENAS DESIGN LIGHTING', 'revenue': 297.39}, {'customer': 'CHRISTIES LIGHTING GALLERY, LLC', 'revenue': 287.81}, {'customer': 'PDI- PLUMBING DISTRIBUTORS INC. (PDI)', 'revenue': 279.13}, {'customer': 'REAL LIGHTING INC.', 'revenue': 278.53}, {'customer': 'DOMINION ELECTRIC SUPPLY, a Division of Border States - VA,', 'revenue': 270.34}, {'customer': 'EDWARD JOY LIGHTING & ELECTRIC SUPPLY', 'revenue': 268.37}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 232.71}, {'customer': 'CRYSTAL LAKE LIGHTING', 'revenue': 219.96}, {'customer': 'NAPLES LAMP SHOP', 'revenue': 215.23}, {'customer': 'MONTREAL LIGHTING & HARDWARE INC.', 'revenue': 193.86}, {'customer': 'LIGHT HOUSE OF LEWES INC', 'revenue': 191.83}, {'customer': 'FW Webb Company - BR9 South Portland, ME', 'revenue': 182.83}, {'customer': 'LIGHT BULBS UNLIMITED-FORT LAUDERDALE', 'revenue': 163.44}, {'customer': 'LIGHTING SPECIALISTS, INC - Nova lighting', 'revenue': 160.86}, {'customer': 'LAMPS.COM INC', 'revenue': 144.9}, {'customer': 'LIGHTING UNLIMITED', 'revenue': 143.39}, {'customer': 'Adam Amrani Consulting', 'revenue': 140.92}, {'customer': 'VALET ENERGY LLC', 'revenue': 115.55}, {'customer': 'NOVA LIGHTING INC.', 'revenue': 113.71}, {'customer': 'CHL LIGHTING INC', 'revenue': 80.73}, {'customer': 'LUMEN NATION', 'revenue': 77.53}, {'customer': 'ROBINSON LIGHTING-Winnepeg, MB', 'revenue': 73.1}, {'customer': 'NEWTON ELECTRICAL SUPPLY', 'revenue': 72.99}, {'customer': 'BRIGHT IDEAS', 'revenue': 70.45}, {'customer': 'The Jarrell Company', 'revenue': 70.44}, {'customer': 'ILLUMINATE', 'revenue': 69.76}, {'customer': 'Modern Luxury by LT', 'revenue': 69.63}, {'customer': 'VILLA LIGHTING SUPPLY INC', 'revenue': 60.65}, {'customer': 'MOON LIGHTING LLC', 'revenue': 56.87}, {'customer': 'JT Roselle Lighting & Supply, Inc.', 'revenue': 55.1}, {'customer': 'CREATIVE LIGHTING DESIGNS & DECOR LLC', 'revenue': 54.21}, {'customer': 'LIGHT UP YOUR LIFE INC', 'revenue': 52.16}, {'customer': 'Francis King', 'revenue': 51.6}, {'customer': 'LIGHTING GETZ CORP.', 'revenue': 49.68}, {'customer': 'DECOR LIGHTING CORP - DESIGNER', 'revenue': 47.74}, {'customer': 'First Supply LLC', 'revenue': 43.3}, {'customer': 'Samco Lighting', 'revenue': 39.98}, {'customer': 'HOMESTYLES', 'revenue': 34.45}, {'customer': 'LIGHTING CORNER', 'revenue': 33.69}, {'customer': 'Everlights, Inc.', 'revenue': 28.4}, {'customer': 'MADISON LIGHTING', 'revenue': 25.83}, {'customer': 'Design House', 'revenue': 24.56}, {'customer': 'ILLUMINATIONS LIGHTING', 'revenue': 22.35}, {'customer': 'HOLDER ELECTRIC CO', 'revenue': 21.08}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 17.15}, {'customer': 'FW WEBB COMPANY - BR107 Madison, NJ', 'revenue': 16.25}, {'customer': 'DULLES ELECTRIC', 'revenue': 7.54}, {'customer': 'WILSON LIGHTING OF NAPLES', 'revenue': 0.0}, {'customer': 'NEEDHAM DECORATIVE HARDWARE', 'revenue': 0.0}, {'customer': 'PACIFIC LIGHTING RESOURCES', 'revenue': 0.0}, {'customer': 'LEGEND LIGHTING INC.', 'revenue': 0.0}, {'customer': 'QED, INC.', 'revenue': 0.0}, {'customer': 'J KNOX DESIGNS, LLC', 'revenue': 0.0}, {'customer': 'HUBBARDTON FORGE', 'revenue': 0.0}, {'customer': 'ROBINSON LIGHTING - PLYMOUTH', 'revenue': 0.0}, {'customer': 'HINSDALE LIGHTING', 'revenue': 0.0}, {'customer': 'Bulbrite Industries Inc', 'revenue': 0.0}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 0.0}, {'customer': 'CREATIVE LIGHTING', 'revenue': 0.0}, {'customer': '17-90 LIGHTING', 'revenue': 0.0}, {'customer': 'CITY LIGHTING PRODUCTS CO', 'revenue': 0.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY (ECOMM)', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'AMERICAN LIGHTING INC', 'revenue': 0.0}, {'customer': 'AM/PM LIGHTING', 'revenue': 0.0}, {'customer': 'VARALUZ', 'revenue': 0.0}, {'customer': 'NO LIMIT LIGHTING SALES', 'revenue': 0.0}, {'customer': 'BC LIGHTING GROUP', 'revenue': 0.0}, {'customer': 'FOGG LIGHTING', 'revenue': -1.37}] | [{'item': '774244', 'desc': 'LED8A19/B60W/830/1P', 'available': 242227}, {'item': '774263', 'desc': 'LED9A19/PF60W/930/D/2/1P', 'available': 171667}, {'item': '776214', 'desc': 'LED7A19/30K/FIL/D/B/2', 'available': 128216}, {'item': '776212', 'desc': 'LED7A19/27K/FIL/D/B/2', 'available': 85200}, {'item': '774243', 'desc': 'LED8A19/B60W/827/1P', 'available': 74194}, {'item': '774262', 'desc': 'LED9A19/PF60W/927/D/2/1P', 'available': 51010}, {'item': '774280', 'desc': 'LED9A19/P60W/927/J/D/2/1P', 'available': 47742}, {'item': '776756', 'desc': 'LED4B11/27K/FIL/4/JA8', 'available': 46077}, {'item': '776627', 'desc': 'LED5B11/30K/FIL/E12/3', 'available': 38110}, {'item': '776204', 'desc': 'LED5B11/30K/FIL/D/B/2', 'available': 36790}, {'item': '773117', 'desc': 'LED9REC/4/940/WHRD/D', 'available': 32447}, {'item': '776873', 'desc': 'LED4G16/27K/FIL/3', 'available': 31103}, {'item': '776626', 'desc': 'LED5B11/27K/FIL/E12/3', 'available': 30021}, {'item': '776216', 'desc': 'LED7A19/40K/FIL/D/B/2', 'available': 29245}, {'item': '776201', 'desc': 'LED4B11/30K/FIL/D/B/2', 'available': 24933}, {'item': '773231', 'desc': 'LED7JBOXDL/3/930/WHRD/D', 'available': 21266}, {'item': '776207', 'desc': 'LED5T9/30K/FIL/D/B/2', 'available': 21110}, {'item': '772870', 'desc': 'LED8BR30/827/D/4', 'available': 20542}, {'item': '776215', 'desc': 'LED7A19/30K/FIL/M/D/B/2', 'available': 20370}, {'item': '776200', 'desc': 'LED4B11/27K/FIL/D/B/2', 'available': 19940}, {'item': '776768', 'desc': 'LED8A19/30K/FIL/3/JA8', 'available': 19752}, {'item': '772857', 'desc': 'LED8BR30/830/D/5', 'available': 18274}, {'item': '773232', 'desc': 'LED7JBOXDL/3/940/WHRD/D', 'available': 17512}, {'item': '776774', 'desc': 'LED8A19/27K/FIL/3/JA8', 'available': 17363}, {'item': '773167', 'desc': 'LED14REC/5/6/940/WHRD/D', 'available': 16954}, {'item': '770579', 'desc': 'LED4G9/30K/120/D', 'available': 16521}, {'item': '776931', 'desc': 'LED5B11/40K/FIL/E12/3', 'available': 13584}, {'item': '776769', 'desc': 'LED8ST18/30K/FIL/3/JA8', 'available': 13486}, {'item': '776962', 'desc': 'LED4B11/50K/FIL/3', 'available': 13132}, {'item': '772253', 'desc': 'LED15PAR38/B-FL40/830/WD/2', 'available': 12921}, {'item': '776224', 'desc': 'LED7ST18/30K/FIL/D/B/2', 'available': 12603}, {'item': '776763', 'desc': 'LED4B11/30K/FIL/4/JA8', 'available': 11901}, {'item': '776987', 'desc': 'LED13ST18/50K/FIL/3', 'available': 11700}, {'item': '776985', 'desc': 'LED8ST18/50K/FIL/3', 'available': 11431}, {'item': '776937', 'desc': 'LED8A19/27K/FIL/M/4', 'available': 11147}, {'item': '774265', 'desc': 'LED9A19/PF60W/950/D/2/1P', 'available': 10427}, {'item': '774245', 'desc': 'LED8A19/B60W/840/1P', 'available': 10401}, {'item': '776964', 'desc': 'LED5B11/50K/FIL/3', 'available': 10398}, {'item': '776966', 'desc': 'LED6B11/50K/FIL/3', 'available': 10362}, {'item': '776684', 'desc': 'LED1S14/24K/FIL', 'available': 10279}, {'item': '776767', 'desc': 'LED8ST18/27K/FIL/3/JA8', 'available': 10262}, {'item': '774281', 'desc': 'LED9A19/P60W/930/J/D/2/1P', 'available': 10171}, {'item': '776685', 'desc': 'LED1S14/27K/FIL', 'available': 9202}, {'item': '773262', 'desc': 'LED14JBOXDL/6/940/WHRD/D', 'available': 8927}, {'item': '776859', 'desc': 'LED4CA10/27K/FIL/3', 'available': 8859}, {'item': '776791', 'desc': 'LED4T6/30K/FIL/3', 'available': 8768}, {'item': '776977', 'desc': 'LED8G25/40K/FIL/3/JA8', 'available': 8685}, {'item': '774232', 'desc': 'LED9A19/B60W/840/1P', 'available': 8516}, {'item': '776220', 'desc': 'LED7G25/30K/FIL/M/D/B/2', 'available': 8183}, {'item': '776935', 'desc': 'LED8ST18/40K/FIL/3/JA8', 'available': 8053}, {'item': '776930', 'desc': 'LED4B11/40K/FIL/3/JA8', 'available': 8002}, {'item': '776963', 'desc': 'LED4B11/50K/FIL/M/3', 'available': 7911}, {'item': '776965', 'desc': 'LED5B11/50K/FIL/M/3', 'available': 7867}, {'item': '776967', 'desc': 'LED6B11/50K/FIL/M/3', 'available': 7771}, {'item': '776979', 'desc': 'LED8G25/50K/FIL/3', 'available': 7734}, {'item': '776976', 'desc': 'LED5G25/30K/FIL/M/3', 'available': 7639}, {'item': '776968', 'desc': 'LED6B11/40K/FIL/M/3', 'available': 7585}, {'item': '776904', 'desc': 'LED2T6/21K/FIL-NOS/3', 'available': 7484}, {'item': '776974', 'desc': 'LED5G25/27K/FIL/M/3', 'available': 7448}, {'item': '772245', 'desc': 'LED10PAR30S/B-FL40/830/WD/2', 'available': 7170}, {'item': '772254', 'desc': 'LED15PAR38/B-FL40/840/WD/2', 'available': 7138}, {'item': '776958', 'desc': 'LED8A19/50K/FIL/3', 'available': 7119}, {'item': '774267', 'desc': 'LED11A19/PF75W/930/D/2/1P', 'available': 7093}, {'item': '776203', 'desc': 'LED5B11/27K/FIL/D/B/2', 'available': 7031}, {'item': '773165', 'desc': 'LED14REC/5/6/927/WHRD/D', 'available': 6752}, {'item': '770191', 'desc': 'LED/C9C', 'available': 6725}, {'item': '776973', 'desc': 'LED5G25/27K/FIL/3', 'available': 6691}, {'item': '776945', 'desc': 'LED5T9L/27K/11/FIL/4', 'available': 6516}, {'item': '776732', 'desc': 'LED5T9/30K/5/FIL/4/JA8', 'available': 6468}, {'item': '774248', 'desc': 'LED8A19/B60W/830/4P', 'available': 6392}, {'item': '770595', 'desc': 'LED4E12/27K/120/D', 'available': 6243}, {'item': '776781', 'desc': 'LED5T9/27K/5/FIL/F/3', 'available': 6238}, {'item': '776223', 'desc': 'LED7ST18/27K/FIL/D/B/2', 'available': 6173}, {'item': '776975', 'desc': 'LED5G25/30K/FIL/3', 'available': 6138}, {'item': '776593', 'desc': 'LED4C15/21K/FIL/SPUN/AMB', 'available': 5879}, {'item': '776991', 'desc': 'LED5T9/50K/5/FIL/3', 'available': 5805}, {'item': '776402', 'desc': 'LED5CA10/30K-18K/WMDM/FIL/M', 'available': 5760}, {'item': '776980', 'desc': 'LED8G25/50K/FIL/M/3', 'available': 5759}, {'item': '776936', 'desc': 'LED13ST18/40K/FIL/3/JA8', 'available': 5688}, {'item': '776969', 'desc': 'LED5CA10/27K/FIL/E26/3', 'available': 5619}, {'item': '776960', 'desc': 'LED14A19/50K/FIL/3', 'available': 5594}, {'item': '776978', 'desc': 'LED8G25/40K/FIL/M/3', 'available': 5589}, {'item': '773272', 'desc': 'LED18JBOXDL/8/940/WHRD/D', 'available': 5540}, {'item': '776405', 'desc': 'LED9ST18/30K-18K/WMDM/FIL/M', 'available': 5471}, {'item': '773260', 'desc': 'LED14JBOXDL/6/927/WHRD/D', 'available': 5418}, {'item': '776780', 'desc': 'LED4T6/27K/FIL/3', 'available': 5254}, {'item': '776949', 'desc': 'LED3T9/30K/7/FIL/4', 'available': 5211}, {'item': '776951', 'desc': 'LED2T6/27K/FIL/3', 'available': 5170}, {'item': '776952', 'desc': 'LED2T6/30K/FIL/4', 'available': 5158}, {'item': '776592', 'desc': 'LED4C15/27K/FIL/SPUN/SAT', 'available': 5154}, {'item': '772302', 'desc': 'LED15PAR38/FL40/930/WD/2', 'available': 5122}, {'item': '776581', 'desc': 'LED4F15/21K/FIESTA/AMB', 'available': 5089}, {'item': '773240', 'desc': 'LED9JBOXDL/4/927/WHRD/D', 'available': 4978}, {'item': '772877', 'desc': 'LED15BR40/830/D/4', 'available': 4964}, {'item': '776219', 'desc': 'LED7G25/30K/FIL/D/B/2', 'available': 4860}, {'item': '776953', 'desc': 'LED2A19/27K/FIL/M/3', 'available': 4834}, {'item': '773210', 'desc': 'LED9JBOXDL/4/827/WHRD/D', 'available': 4829}, {'item': '776914', 'desc': 'LED9A19/30K/FIL/4', 'available': 4825}, {'item': '776959', 'desc': 'LED8A19/50K/FIL/M/3', 'available': 4815}, {'item': '776872', 'desc': 'LED5A19/27K/FIL/3', 'available': 4807}, {'item': '776989', 'desc': 'LED5T9/40K/5/FIL/3/JA8', 'available': 4806}, {'item': '776205', 'desc': 'LED5B11/40K/FIL/D/B/2', 'available': 4740}, {'item': '776902', 'desc': 'LED4A19/21K/FIL-NOS/3', 'available': 4729}, {'item': '776749', 'desc': 'LED8G25/27K/FIL/4/JA8', 'available': 4726}, {'item': '776206', 'desc': 'LED5T9/27K/FIL/D/B/2', 'available': 4718}, {'item': '776840', 'desc': 'LED6G40/27K/FIL/HW/3', 'available': 4647}, {'item': '776836', 'desc': 'LED6G40/27K/FIL/HB/3', 'available': 4647}, {'item': '776837', 'desc': 'LED5A19/27K/FIL/HW/3', 'available': 4522}, {'item': '776862', 'desc': 'LED4B11/27K/FIL/E26/3', 'available': 4453}, {'item': '776731', 'desc': 'LED5T9/27K/5/FIL/4/JA8', 'available': 4452}, {'item': '776833', 'desc': 'LED5A19/27K/FIL/HB/3', 'available': 4382}, {'item': '776580', 'desc': 'LED4F15/27K/FIESTA/CLR', 'available': 4348}, {'item': '776719', 'desc': 'LED5T9L/21K/15/FIL-NOS/3', 'available': 4325}, {'item': '776225', 'desc': 'LED7ST18/40K/FIL/D/B/2', 'available': 4199}, {'item': '776906', 'desc': 'LED2G16/21K/FIL-NOS/3', 'available': 4189}, {'item': '773221', 'desc': 'LED14JBOXDL/6/830/WHRD/D', 'available': 4186}, {'item': '771109', 'desc': 'LED6PAR16GUFL40/50/930/J/D/2', 'available': 4184}, {'item': '771086', 'desc': 'LED6MR16FL40/50/930/J/D/5', 'available': 4165}, {'item': '772246', 'desc': 'LED10PAR30S/B-FL40/840/WD/2', 'available': 4155}, {'item': '772856', 'desc': 'LED8BR30/827/D/5', 'available': 4138}, {'item': '776925', 'desc': 'LED8A19/40K/FIL/3/JA8', 'available': 4089}, {'item': '772242', 'desc': 'LED7PAR20/B-FL40/830/WD/2', 'available': 4049}, {'item': '771088', 'desc': 'LED7MR16FL40/75/930/J/D/2', 'available': 3955}, {'item': '776839', 'desc': 'LED5G25/27K/FIL/HW/3', 'available': 3940}, {'item': '776970', 'desc': 'LED5CA10/27K/FIL/E26/M/3', 'available': 3938}, {'item': '776992', 'desc': 'LED5T9/50K/5/FIL/F/3', 'available': 3902}, {'item': '776217', 'desc': 'LED7G25/27K/FIL/D/B/2', 'available': 3894}, {'item': '776982', 'desc': 'LED8G40/40K/FIL/M/3', 'available': 3881}, {'item': '776990', 'desc': 'LED5T9/40K/5/FIL/F/3', 'available': 3854}, {'item': '776832', 'desc': 'LED7A15/30K/FIL/M/3', 'available': 3831}, {'item': '776838', 'desc': 'LED2G16/27K/FIL/HW/3', 'available': 3791}, {'item': '772243', 'desc': 'LED7PAR20/B-FL40/840/WD/2', 'available': 3727}, {'item': '776981', 'desc': 'LED8G40/40K/FIL/3', 'available': 3726}, {'item': '776988', 'desc': 'LED6B11/30K/FIL/M/3', 'available': 3692}, {'item': '773271', 'desc': 'LED18JBOXDL/8/930/WHRD/D', 'available': 3675}, {'item': '776404', 'desc': 'LED9G25/30K-18K/WMDM/FIL/M', 'available': 3629}, {'item': '776744', 'desc': 'LED4G16/30K/FIL/4/JA8', 'available': 3590}, {'item': '776995', 'desc': 'LED4T6/50K/FIL/3', 'available': 3553}, {'item': '776986', 'desc': 'LED6B11/27K/FIL/M/3', 'available': 3541}, {'item': '776864', 'desc': 'LED4CA10/30K/FIL/3', 'available': 3495}, {'item': '776913', 'desc': 'LED9A19/27K/FIL/4', 'available': 3479}, {'item': '776829', 'desc': 'LED7A15/27K/FIL/3', 'available': 3434}, {'item': '774269', 'desc': 'LED15A19/P100W/930/J/D/2/1P', 'available': 3381}, {'item': '776938', 'desc': 'LED2B11/27K/FIL/4', 'available': 3374}, {'item': '771085', 'desc': 'LED6MR16FL40/50/927/J/D/5', 'available': 3361}, {'item': '776514', 'desc': 'LED4A19/21K/FIL-NOS/CURV/LOOP', 'available': 3346}, {'item': '774264', 'desc': 'LED9A19/PF60W/940/D/2/1P', 'available': 3333}, {'item': '776835', 'desc': 'LED5G25/27K/FIL/HB/3', 'available': 3331}, {'item': '776221', 'desc': 'LED7G25/40K/FIL/D/B/2', 'available': 3310}, {'item': '776743', 'desc': 'LED4G16/27K/FIL/4/JA8', 'available': 3301}, {'item': '773222', 'desc': 'LED14JBOXDL/6/840/WHRD/D', 'available': 3290}, {'item': '770195', 'desc': 'LED/C9O', 'available': 3261}, {'item': '776834', 'desc': 'LED2G16/27K/FIL/HB/3', 'available': 3187}, {'item': '772764', 'desc': 'LED10PAR30S/FL40/827/WD/2', 'available': 3177}, {'item': '776943', 'desc': 'LED4G16/27K/FIL/M/4', 'available': 3159}, {'item': '776897', 'desc': 'LED8G40/27K/FIL/M/3', 'available': 3156}, {'item': '776726', 'desc': 'LED5T9/30K/7/FIL/F/3', 'available': 3100}, {'item': '774285', 'desc': 'LED5/9/14A19/PF100W/827/3WAY/1P', 'available': 3098}, {'item': '776725', 'desc': 'LED5T9/27K/7/FIL/F/3', 'available': 3091}, {'item': '776721', 'desc': 'LED5T9L/30K/15/FIL/3', 'available': 3090}, {'item': '776591', 'desc': 'LED4C11/21K/FIL/SPUN/AMB', 'available': 3057}, {'item': '770598', 'desc': 'LED3G9/30K/W/D', 'available': 3052}, {'item': '770591', 'desc': 'LED4G9/27K/120/F/D', 'available': 3031}, {'item': '772286', 'desc': 'LED10PAR30L/FL40/927/WD/2', 'available': 3030}, {'item': '776858', 'desc': 'LED2CA10/27K/FIL/E12/3', 'available': 3009}, {'item': '772861', 'desc': 'LED15BR40/830/D/5', 'available': 3005}, {'item': '772248', 'desc': 'LED10PAR30L/B-FL40/830/WD/2', 'available': 3002}, {'item': '772859', 'desc': 'LED11BR30/830/D/5', 'available': 3002}, {'item': '770614', 'desc': 'LED1/FEST/27K/24/2', 'available': 2986}, {'item': '776961', 'desc': 'LED14A19/50K/FIL/M/3', 'available': 2979}, {'item': '776773', 'desc': 'LED4B11/30K/FIL/M/3', 'available': 2935}, {'item': '776713', 'desc': 'LED5T9/21K/7/FIL-NOS/3', 'available': 2900}, {'item': '776321', 'desc': 'LED4C53/30K/FIL/GRAD/SMK', 'available': 2891}, {'item': '776825', 'desc': 'LED4A15/27K/FIL/E12/3', 'available': 2861}, {'item': '776933', 'desc': 'LED4B11/40K/FIL/M/3', 'available': 2849}, {'item': '776950', 'desc': 'LED2S14/27K/FIL/4', 'available': 2820}, {'item': '776594', 'desc': 'LED4T6SL/27K/FIL/3', 'available': 2783}, {'item': '776934', 'desc': 'LED5B11/40K/FIL/M/3', 'available': 2781}, {'item': '776928', 'desc': 'LED7A19/40K/FIL/M/3', 'available': 2759}, {'item': '774279', 'desc': 'LED15A19/P100W/930/GU24/J/D/1P', 'available': 2755}, {'item': '774266', 'desc': 'LED11A19/PF75W/927/D/2/1P', 'available': 2739}, {'item': '770171', 'desc': 'LED/C7C', 'available': 2738}, {'item': '770637', 'desc': 'LED6R7S/30K/S/D', 'available': 2731}, {'item': '774286', 'desc': 'LED5/9/14A19/PF100W/830/3WAY/1P', 'available': 2692}, {'item': '772265', 'desc': 'LED6PAR20/NFL25/930/WD/2', 'available': 2689}, {'item': '776929', 'desc': 'LED14A19/40K/FIL/M/3', 'available': 2653}, {'item': '776712', 'desc': 'LED4G16/30K/FIL/M/3', 'available': 2647}, {'item': '776917', 'desc': 'LED9A19/27K/FIL/M/4', 'available': 2622}, {'item': '776108', 'desc': 'LED4A19/GRN/FIL/D', 'available': 2607}, {'item': '773170', 'desc': 'LED9REC/4/927/WHRD-G/D', 'available': 2585}, {'item': '776742', 'desc': 'LED5CA10/30K/FIL/4/JA8', 'available': 2573}, {'item': '776521', 'desc': 'LED11A19/30K/FIL/3WAY', 'available': 2561}, {'item': '776926', 'desc': 'LED9A19/40K/FIL/3', 'available': 2538}, {'item': '776741', 'desc': 'LED5CA10/27K/FIL/4/JA8', 'available': 2528}, {'item': '770586', 'desc': 'LED2G4/27K/12', 'available': 2517}, {'item': '776151', 'desc': 'LED2S14/AMB/FIL/D', 'available': 2514}, {'item': '770596', 'desc': 'LED4E12/27K/120/F/D', 'available': 2498}, {'item': '776218', 'desc': 'LED7G25/27K/FIL/M/D/B/2', 'available': 2470}, {'item': '776208', 'desc': 'LED7A15/27K/FIL/D/B/2', 'available': 2445}, {'item': '773180', 'desc': 'LED14REC/5/6/927/WHRD-G/D', 'available': 2436}, {'item': '771087', 'desc': 'LED7MR16FL40/75/927/J/D/2', 'available': 2420}, {'item': '770580', 'desc': 'LED4G9/30K/120/F/D', 'available': 2389}, {'item': '773181', 'desc': 'LED14REC/5/6/930/WHRD-G/D', 'available': 2354}, {'item': '776106', 'desc': 'LED4A19/AMB/FIL/D', 'available': 2350}, {'item': '776110', 'desc': 'LED4A19/PNK/FIL/D', 'available': 2347}, {'item': '770583', 'desc': 'LED2WEDGE/30K/12', 'available': 2339}, {'item': '776994', 'desc': 'LED4T6/40K/FIL/M/3', 'available': 2339}, {'item': '770613', 'desc': 'LED1/FEST/30K/24/2', 'available': 2327}, {'item': '776954', 'desc': 'LED5A19/27K/FIL/M/3', 'available': 2326}, {'item': '773242', 'desc': 'LED9JBOXDL/4/940/WHRD/D', 'available': 2320}, {'item': '776516', 'desc': 'LED4G25/21K/FIL-NOS/CURV/SPIRAL', 'available': 2296}, {'item': '776909', 'desc': 'LED7ST18/21K/FIL-NOS/3', 'available': 2288}, {'item': '776927', 'desc': 'LED14A19/40K/FIL/3', 'available': 2255}, {'item': '770638', 'desc': 'LED10R7S/30K/L/D', 'available': 2251}, {'item': '776520', 'desc': 'LED11A19/27K/FIL/3WAY', 'available': 2237}, {'item': '776801', 'desc': 'LED5ST18/22K/FIL-NOS/3', 'available': 2232}, {'item': '776403', 'desc': 'LED5G16/30K-18K/WMDM/FIL/M', 'available': 2228}, {'item': '770626', 'desc': 'LED5GY6/30K/12', 'available': 2226}, {'item': '776922', 'desc': 'LED9A19/30K/FIL/M/4', 'available': 2220}, {'item': '776228', 'desc': 'LED7A19/40K/FIL/D/B/2/4P', 'available': 2211}, {'item': '776720', 'desc': 'LED5T9L/27K/15/FIL/3', 'available': 2200}, {'item': '773241', 'desc': 'LED9JBOXDL/4/930/WHRD/D', 'available': 2188}, {'item': '772261', 'desc': 'LED6PAR20/NFL25/927/WD/2', 'available': 2141}, {'item': '776213', 'desc': 'LED7A19/27K/FIL/M/D/B/2', 'available': 2116}, {'item': '776948', 'desc': 'LED3T9/27K/7/FIL/4', 'available': 2111}, {'item': '770648', 'desc': 'LED5G9/30K/120/D/2', 'available': 2066}, {'item': '776916', 'desc': 'LED14A19/30K/FIL/3', 'available': 2042}, {'item': '776918', 'desc': 'LED14A19/27K/FIL/M/3', 'available': 2031}, {'item': '770611', 'desc': 'LED1/FEST/30K/12/2', 'available': 2019}, {'item': '776231', 'desc': 'LED4B11/40K/FIL/D/B/2/6P', 'available': 2018}, {'item': '770196', 'desc': 'LED/C9P', 'available': 2015}, {'item': '772249', 'desc': 'LED10PAR30L/B-FL40/840/WD/2', 'available': 2010}, {'item': '770630', 'desc': 'LED5E11/30K/120/D', 'available': 1992}, {'item': '776972', 'desc': 'LED5CA10/30K/FIL/E26/M/3', 'available': 1971}, {'item': '776996', 'desc': 'LED4T6/50K/FIL/M/3', 'available': 1954}, {'item': '770619', 'desc': 'LED4DC/30K/D', 'available': 1947}, {'item': '776941', 'desc': 'LED5B11/30K/FIL/M/4', 'available': 1934}, {'item': '776932', 'desc': 'LED6B11/40K/FIL/3', 'available': 1928}, {'item': '776983', 'desc': 'LED8G40/50K/FIL/3', 'available': 1927}, {'item': '776824', 'desc': 'LED4ST15/30K/FIL/M/3', 'available': 1925}, {'item': '770597', 'desc': 'LED3G9/27K/W/D', 'available': 1912}, {'item': '776750', 'desc': 'LED8G25/30K/FIL/4/JA8', 'available': 1904}, {'item': '776984', 'desc': 'LED8G40/50K/FIL/M/3', 'available': 1894}, {'item': '776785', 'desc': 'LED1S14/27K/FIL/PL', 'available': 1892}, {'item': '770625', 'desc': 'LED5GY6/27K/12', 'available': 1885}, {'item': '772610', 'desc': 'LED18PAR38/FL40/927/J/WD', 'available': 1866}, {'item': '774246', 'desc': 'LED8A19/B60W/850/1P', 'available': 1866}, {'item': '776109', 'desc': 'LED4A19/BLU/FIL/D', 'available': 1856}, {'item': '770624', 'desc': 'LED4G4/30K/12', 'available': 1855}, {'item': '776322', 'desc': 'LED4C53/30K/FIL/GRAD/BLU', 'available': 1849}, {'item': '770577', 'desc': 'LED3G9/30K/120', 'available': 1842}, {'item': '776827', 'desc': 'LED4A15/27K/FIL/M/E12/3', 'available': 1838}, {'item': '772876', 'desc': 'LED15BR40/827/D/4', 'available': 1811}, {'item': '770622', 'desc': 'LED3G4/WA/27K/12', 'available': 1811}, {'item': '776942', 'desc': 'LED4CA10/27K/FIL/M/3', 'available': 1809}, {'item': '770650', 'desc': 'LED2G4/30K/W/D', 'available': 1802}, {'item': '770589', 'desc': 'LED3G9/27K/120', 'available': 1801}, {'item': '776971', 'desc': 'LED5CA10/30K/FIL/E26/3', 'available': 1798}, {'item': '776920', 'desc': 'LED6G40/27K/FIL/HM/3', 'available': 1783}, {'item': '770658', 'desc': 'LED4G9/30K/W/F/D', 'available': 1770}, {'item': '773171', 'desc': 'LED9REC/4/930/WHRD-G/D', 'available': 1761}, {'item': '773270', 'desc': 'LED18JBOXDL/8/927/WHRD/D', 'available': 1754}, {'item': '776993', 'desc': 'LED4T6/40K/FIL/3', 'available': 1628}, {'item': '773115', 'desc': 'LED9REC/4/927/WHRD/D', 'available': 1613}, {'item': '776878', 'desc': 'LED8G40/27K/FIL/3', 'available': 1606}, {'item': '776861', 'desc': 'LED4CA10/30K/FIL/M/3', 'available': 1560}, {'item': '776831', 'desc': 'LED7A15/27K/FIL/M/3', 'available': 1523}, {'item': '771105', 'desc': 'LED6PAR16FL40/50/830/D/5', 'available': 1516}, {'item': '770643', 'desc': 'LED6E12/30K/120/D', 'available': 1512}, {'item': '776899', 'desc': 'LED8G40/30K/FIL/M/3', 'available': 1511}, {'item': '776997', 'desc': 'LED4G40/30K/FIL/GRAD/SMK', 'available': 1508}, {'item': '776823', 'desc': 'LED4ST15/27K/FIL/M/3', 'available': 1502}, {'item': '776903', 'desc': 'LED2CA10/21K/FIL-NOS/3', 'available': 1501}, {'item': '772860', 'desc': 'LED15BR40/827/D/5', 'available': 1488}, {'item': '770645', 'desc': 'LED6G9/30K/120/D', 'available': 1483}, {'item': '772301', 'desc': 'LED15PAR38/NF25/930/WD/2', 'available': 1478}, {'item': '776105', 'desc': 'LED4A19/RED/FIL/D', 'available': 1475}, {'item': '770652', 'desc': 'LED2G4/30K/W/F/D', 'available': 1471}, {'item': '772855', 'desc': 'LED7BR20/830/D/5', 'available': 1471}, {'item': '776746', 'desc': 'LED13ST18/30K/FIL/3/JA8', 'available': 1470}, {'item': '773220', 'desc': 'LED14JBOXDL/6/827/WHRD/D', 'available': 1467}, {'item': '774249', 'desc': 'LED8A19/B60W/840/4P', 'available': 1454}, {'item': '771117', 'desc': 'LED6PAR16FL40/50/830/D/4', 'available': 1449}, {'item': '776946', 'desc': 'LED5T9L/30K/11/FIL/4', 'available': 1448}, {'item': '776722', 'desc': 'LED4T8/21K/FIL-NOS/3', 'available': 1443}, {'item': '776870', 'desc': 'LED5G25/27K/FIL/HM/3', 'available': 1423}, {'item': '776707', 'desc': 'LED5T9L/21K/11/FIL-NOS/3', 'available': 1422}, {'item': '776828', 'desc': 'LED4A15/30K/FIL/M/E12/3', 'available': 1417}, {'item': '776241', 'desc': 'LED7G25/40K/FIL/D/B/2/4P', 'available': 1417}, {'item': '770612', 'desc': 'LED1/FEST/27K/12/2', 'available': 1409}, {'item': '772768', 'desc': 'LED10PAR30S/FL40/830/WD/2', 'available': 1408}, {'item': '776915', 'desc': 'LED14A19/27K/FIL/3', 'available': 1385}, {'item': '776237', 'desc': 'LED5B11/27K/FIL/D/B/2/25P', 'available': 1385}, {'item': '776826', 'desc': 'LED4A15/30K/FIL/E12/3', 'available': 1384}, {'item': '776800', 'desc': 'LED5G25/22K/FIL-NOS/3', 'available': 1379}, {'item': '776944', 'desc': 'LED8G25/27K/FIL/M/3', 'available': 1362}, {'item': '776229', 'desc': 'LED4B11/27K/FIL/D/B/2/6P', 'available': 1362}, {'item': '773152', 'desc': 'LED20DL/9/927/WHRD/J/D', 'available': 1359}, {'item': '772502', 'desc': 'LED15PAR38/FL/YLW/D', 'available': 1353}, {'item': '776232', 'desc': 'LED5B11/27K/FIL/D/B/2/6P', 'available': 1338}, {'item': '770651', 'desc': 'LED2G4/27K/W/F/D', 'available': 1336}, {'item': '776234', 'desc': 'LED5B11/40K/FIL/D/B/2/6P', 'available': 1333}, {'item': '776401', 'desc': 'LED5B11/30K-18K/WMDM/FIL/M', 'available': 1330}, {'item': '770576', 'desc': 'LED4GY8/30K/120/D', 'available': 1322}, {'item': '776406', 'desc': 'LED4G40/30K-18K/WMDM/FIL/M', 'available': 1319}, {'item': '776939', 'desc': 'LED4B11/27K/FIL/M/3', 'available': 1318}, {'item': '776730', 'desc': 'LED4T6/30K/FIL/M/3', 'available': 1316}, {'item': '776235', 'desc': 'LED4B11/27K/FIL/D/B/2/25P', 'available': 1314}, {'item': '776734', 'desc': 'LED5B11/30K/FIL/E26/3', 'available': 1299}, {'item': '774247', 'desc': 'LED8A19/B60W/827/4P', 'available': 1299}, {'item': '770604', 'desc': 'LED/LI4T8/27K', 'available': 1285}, {'item': '772854', 'desc': 'LED7BR20/827/D/5', 'available': 1280}, {'item': '772505', 'desc': 'LED15PAR38/FL/PNK/D', 'available': 1268}, {'item': '776738', 'desc': 'LED6B11/30K/FIL/3', 'available': 1266}, {'item': '772503', 'desc': 'LED15PAR38/FL/GRN/D', 'available': 1261}, {'item': '776830', 'desc': 'LED7A15/30K/FIL/3', 'available': 1256}, {'item': '776740', 'desc': 'LED6CA10/30K/FIL/3', 'available': 1253}, {'item': '776919', 'desc': 'LED14A19/30K/FIL/M/3', 'available': 1248}, {'item': '770585', 'desc': 'LED4E12/30K/120/F/D', 'available': 1242}, {'item': '776787', 'desc': 'LED5CA10/27K/FIL/M/3', 'available': 1240}, {'item': '772290', 'desc': 'LED10PAR30L/FL40/930/WD/2', 'available': 1233}, {'item': '773146', 'desc': 'LED15DL/7/927/WHSQ/J/D', 'available': 1216}, {'item': '776595', 'desc': 'LED4T6SL/30K/FIL/3', 'available': 1216}, {'item': '772278', 'desc': 'LED10PAR30S/FL40/930/WD/2', 'available': 1207}, {'item': '776239', 'desc': 'LED7G25/27K/FIL/D/B/2/4P', 'available': 1201}, {'item': '776748', 'desc': 'LED13G25/30K/FIL/3/JA8', 'available': 1200}, {'item': '776238', 'desc': 'LED5B11/30K/FIL/D/B/2/25P', 'available': 1199}, {'item': '770593', 'desc': 'LED4E11/27K/120/F/D', 'available': 1195}, {'item': '770581', 'desc': 'LED4E11/30K/120/D', 'available': 1182}, {'item': '776921', 'desc': 'LED2G16/27K/FIL/HG/3', 'available': 1179}, {'item': '772274', 'desc': 'LED10PAR30S/FL40/927/WD/2', 'available': 1176}, {'item': '772500', 'desc': 'LED15PAR38/FL/RED/D', 'available': 1169}, {'item': '771108', 'desc': 'LED6PAR16GUFL40/50/927/J/D/2', 'available': 1165}, {'item': '776210', 'desc': 'LED7A15/30K/FIL/D/B/2', 'available': 1145}, {'item': '770623', 'desc': 'LED4G4/27K/12', 'available': 1136}, {'item': '776107', 'desc': 'LED4A19/YLW/FIL/D', 'available': 1135}, {'item': '772504', 'desc': 'LED15PAR38/FL/BLU/D', 'available': 1124}, {'item': '774240', 'desc': 'LED9A19/P60W/940/J/D/1P', 'available': 1123}, {'item': '776735', 'desc': 'LED5B11/27K/FIL/M/E26/3', 'available': 1120}, {'item': '776226', 'desc': 'LED7A19/27K/FIL/D/B/2/4P', 'available': 1113}, {'item': '772858', 'desc': 'LED11BR30/827/D/5', 'available': 1094}, {'item': '776306', 'desc': 'LED4OLIVE/22K/FIL', 'available': 1089}, {'item': '776747', 'desc': 'LED13G25/27K/FIL/3/JA8', 'available': 1071}, {'item': '770152', 'desc': 'LED/G14G', 'available': 1049}, {'item': '773125', 'desc': 'LED11JBOXDL/6/827/WHRD/D', 'available': 1038}, {'item': '776318', 'desc': 'LED4JEWEL/20K/FIL-NOS', 'available': 1037}, {'item': '774254', 'desc': 'LED9A19/PF60W/930/D/2/4P', 'available': 1035}, {'item': '772865', 'desc': 'LED7R20/830/D/4', 'available': 1013}, {'item': '772298', 'desc': 'LED15PAR38/FL40/927/WD/2', 'available': 994}, {'item': '774253', 'desc': 'LED9A19/PF60W/927/D/2/4P', 'available': 984}, {'item': '776153', 'desc': 'LED2S14/GRN/FIL/D', 'available': 983}, {'item': '774256', 'desc': 'LED9A19/PF60W/950/D/2/4P', 'available': 982}, {'item': '776209', 'desc': 'LED7A15/27K/FIL/M/D/B/2', 'available': 967}, {'item': '774250', 'desc': 'LED8A19/B60W/850/4P', 'available': 964}, {'item': '776792', 'desc': 'LED5T9/30K/5/FIL/F/3', 'available': 963}, {'item': '770594', 'desc': 'LED2WEDGE/27K/12', 'available': 961}, {'item': '774283', 'desc': 'LED9A19/P60W/927/GU24/J/D/2/1P', 'available': 958}, {'item': '776222', 'desc': 'LED7G25/40K/FIL/M/D/B/2', 'available': 941}, {'item': '776737', 'desc': 'LED6B11/27K/FIL/3', 'available': 939}, {'item': '776400', 'desc': 'LED9A19/30K-18K/WMDM/FIL/M', 'available': 930}, {'item': '770599', 'desc': 'LED4G9/27K/W/D', 'available': 929}, {'item': '776879', 'desc': 'LED8G40/30K/FIL/3', 'available': 928}, {'item': '772501', 'desc': 'LED15PAR38/FL/AMB/D', 'available': 917}, {'item': '770641', 'desc': 'LED6E11/30K/120/D', 'available': 905}, {'item': '770620', 'desc': 'LED4DC/27K/D', 'available': 888}, {'item': '776819', 'desc': 'LED5T14/27K/FIL/3', 'available': 884}, {'item': '776155', 'desc': 'LED2S14/PNK/FIL/D', 'available': 861}, {'item': '770616', 'desc': 'LED4GY6/27K/D/2', 'available': 860}, {'item': '770584', 'desc': 'LED4E12/30K/120/D', 'available': 849}, {'item': '770600', 'desc': 'LED4G9/30K/W/D', 'available': 848}, {'item': '770660', 'desc': 'LED3G9/30K/W/F/D', 'available': 837}, {'item': '776728', 'desc': 'LED5T9/30K/11/FIL/F/3', 'available': 834}, {'item': '770656', 'desc': 'LED2GY6/30K/12/W/F/D', 'available': 827}, {'item': '776924', 'desc': 'LED6G40/27K/FIL/HG/3', 'available': 826}, {'item': '776998', 'desc': 'LED4G40/30K/FIL/GRAD/BLU', 'available': 806}, {'item': '776739', 'desc': 'LED6CA10/27K/FIL/3', 'available': 799}, {'item': '776317', 'desc': 'LED4DROP/20K/FIL-NOS', 'available': 796}, {'item': '776243', 'desc': 'LED7ST18/30K/FIL/D/B/2/4P', 'available': 793}, {'item': '770632', 'desc': 'LED5E12/30K/120/D', 'available': 785}, {'item': '776515', 'desc': 'LED3ST18/21K/FIL-NOS/CURV/HAIRPIN', 'available': 780}, {'item': '772767', 'desc': 'LED10PAR30S/NF25/830/WD/2', 'available': 756}, {'item': '770629', 'desc': 'LED5E11/27K/120/D', 'available': 755}, {'item': '776771', 'desc': 'LED2G16/27K/FIL/HM/3', 'available': 755}, {'item': '776820', 'desc': 'LED5T14/30K/FIL/3', 'available': 735}, {'item': '776152', 'desc': 'LED2S14/YLW/FIL/D', 'available': 732}, {'item': '770649', 'desc': 'LED2G4/27K/W/D', 'available': 731}, {'item': '774251', 'desc': 'LED8A19/B60W/827/25P', 'available': 725}, {'item': '776101', 'desc': 'LED27T5/48/840/DIR', 'available': 723}, {'item': '770571', 'desc': 'LED2G4/30K/12', 'available': 715}, {'item': '776810', 'desc': 'LED8G25/30K/FIL/M/3', 'available': 714}, {'item': '776150', 'desc': 'LED2S14/RED/FIL/D', 'available': 688}, {'item': '774242', 'desc': 'LED9A19/P60W/930/GU24/J/D/1P', 'available': 679}, {'item': '770587', 'desc': 'LED3G4/27K/12', 'available': 664}, {'item': '772792', 'desc': 'LED15PAR38/FL40/830/WD/2', 'available': 662}, {'item': '770647', 'desc': 'LED5G9/27K/120/D/2', 'available': 655}, {'item': '770653', 'desc': 'LED2GY6/27K/12/W/D', 'available': 654}, {'item': '776706', 'desc': 'LED2G16/27K/FIL/3', 'available': 641}, {'item': '772775', 'desc': 'LED10PAR30L/NF25/827/WD/2', 'available': 641}, {'item': '776908', 'desc': 'LED3T9/21K/FIL-NOS/3', 'available': 638}, {'item': '776923', 'desc': 'LED4G25/27K/FIL/HG/3', 'available': 633}, {'item': '776230', 'desc': 'LED4B11/30K/FIL/D/B/2/6P', 'available': 631}, {'item': '776154', 'desc': 'LED2S14/BLU/FIL/D', 'available': 618}, {'item': '776005', 'desc': 'LED20T8/30K', 'available': 616}, {'item': '770590', 'desc': 'LED4G9/27K/120/D', 'available': 608}, {'item': '776242', 'desc': 'LED7ST18/27K/FIL/D/B/2/4P', 'available': 605}, {'item': '776822', 'desc': 'LED4ST15/30K/FIL/3', 'available': 599}, {'item': '770654', 'desc': 'LED2GY6/30K/12/W/D', 'available': 595}, {'item': '774258', 'desc': 'LED9A19/PF60W/930/D/2/25P', 'available': 567}, {'item': '776871', 'desc': 'LED2A19/27K/FIL/3', 'available': 561}, {'item': '776302', 'desc': 'LED4G63/22K/FIL', 'available': 559}, {'item': '776745', 'desc': 'LED13ST18/27K/FIL/3/JA8', 'available': 540}, {'item': '770631', 'desc': 'LED5E12/27K/120/D', 'available': 506}, {'item': '776854', 'desc': 'LED3T9/30K/FIL/3', 'available': 504}, {'item': '776940', 'desc': 'LED5B11/27K/FIL/M/4', 'available': 499}, {'item': '772262', 'desc': 'LED6PAR20/FL40/927/WD/2', 'available': 477}, {'item': '772779', 'desc': 'LED10PAR30L/NF25/830/WD/2', 'available': 469}, {'item': '770655', 'desc': 'LED2GY6/27K/12/W/F/D', 'available': 438}, {'item': '770621', 'desc': 'LED3G4/WA/30K/12', 'available': 434}, {'item': '770588', 'desc': 'LED4GY8/27K/120/D', 'available': 416}, {'item': '776211', 'desc': 'LED7A15/30K/FIL/M/D/B/2', 'available': 387}, {'item': '770194', 'desc': 'LED/C9G', 'available': 375}, {'item': '770618', 'desc': 'LED4SC/27K/12', 'available': 373}, {'item': '776233', 'desc': 'LED5B11/30K/FIL/D/B/2/6P', 'available': 369}, {'item': '770640', 'desc': 'LED6E11/27K/120/D', 'available': 367}, {'item': '776518', 'desc': 'LED4T14/21K/FIL-NOS/CURV/SPIRAL', 'available': 357}, {'item': '770644', 'desc': 'LED6G9/27K/120/D', 'available': 340}, {'item': '776679', 'desc': 'LED5A19/27K/FIL/HG/3', 'available': 328}, {'item': '776596', 'desc': 'LED4PRISM/30K/FIL/3', 'available': 296}, {'item': '772266', 'desc': 'LED6PAR20/FL40/930/WD/2', 'available': 276}, {'item': '776727', 'desc': 'LED5T9/27K/11/FIL/F/3', 'available': 269}, {'item': '772756', 'desc': 'LED7PAR20/FL40/830/WD/2', 'available': 265}, {'item': '773158', 'desc': 'LED20DL/9/927/WHSQ/J/D', 'available': 259}, {'item': '776821', 'desc': 'LED4ST15/27K/FIL/3', 'available': 258}, {'item': '776227', 'desc': 'LED7A19/30K/FIL/D/B/2/4P', 'available': 231}, {'item': '776240', 'desc': 'LED7G25/30K/FIL/D/B/2/4P', 'available': 197}, {'item': '776905', 'desc': 'LED4T14/21K/FIL-NOS/3', 'available': 190}, {'item': '774257', 'desc': 'LED9A19/PF60W/927/D/2/25P', 'available': 185}, {'item': '776788', 'desc': 'LED5CA10/30K/FIL/M/3', 'available': 179}, {'item': '776244', 'desc': 'LED7ST18/40K/FIL/D/B/2/4P', 'available': 155}, {'item': '774276', 'desc': 'LED15A19/P100W/927/J/D/1P', 'available': 150}, {'item': '776314', 'desc': 'LED4BT56/22K/FIL', 'available': 147}, {'item': '770659', 'desc': 'LED3G9/27K/W/F/D', 'available': 144}, {'item': '776736', 'desc': 'LED5B11/30K/FIL/M/E26/3', 'available': 140}, {'item': '770615', 'desc': 'LED4GY6/30K/D/2', 'available': 112}, {'item': '776305', 'desc': 'LED4DIA/22K/FIL', 'available': 86}, {'item': '772763', 'desc': 'LED10PAR30S/NF25/827/WD/2', 'available': 77}, {'item': '777801', 'desc': 'AC-CC-0002-00-S1', 'available': 74}, {'item': '777902', 'desc': 'SR111-18-36D-927-03', 'available': 68}, {'item': '776301', 'desc': 'LED4ET25/22K/FIL', 'available': 66}, {'item': '776304', 'desc': 'LED4BH/22K/FIL', 'available': 66}, {'item': '777252', 'desc': 'SP20-11-10D-927-03', 'available': 53}, {'item': '776300', 'desc': 'LED4PS52/22K/FIL', 'available': 51}, {'item': '777803', 'desc': 'AC-GC-2525-00-S1', 'available': 40}, {'item': '777809', 'desc': 'AC-FR-3636-00-S1', 'available': 35}, {'item': '777679', 'desc': 'SP38-14-60D-827-H1', 'available': 30}, {'item': '777823', 'desc': 'AC-E-GC-2525-00-S1', 'available': 25}, {'item': '772717', 'desc': 'LED7PAR20/NF25/840/WD', 'available': 23}, {'item': '771208', 'desc': 'LED6MR16FL35/50/830/D', 'available': 21}, {'item': '777766', 'desc': 'SP38-18-36D-930-03', 'available': 14}, {'item': '777700', 'desc': 'SP30L-18-09D-927-03', 'available': 12}, {'item': '777721', 'desc': 'SP30S-18-25D-927-03', 'available': 10}, {'item': '777681', 'desc': 'SP38-14-25D-830-H1', 'available': 10}, {'item': '774260', 'desc': 'LED11A19/PF75W/927/D/1P', 'available': 10}, {'item': '777661', 'desc': 'SP30L-14-25D-827-H1', 'available': 10}, {'item': '773230', 'desc': 'LED7JBOXDL/3/927/WHRD/D', 'available': 9}, {'item': '777827', 'desc': 'AC-E-GE-1036-00-S1', 'available': 9}, {'item': '776320', 'desc': 'LED4GLACIER/20K/FIL-NOS', 'available': 9}, {'item': '774252', 'desc': 'LED8A19/B60W/830/25P', 'available': 8}, {'item': '777707', 'desc': 'SP30L-18-60D-930-03', 'available': 6}, {'item': '777235', 'desc': 'SP20-11-36D-830-H1', 'available': 6}, {'item': '777764', 'desc': 'SP38-18-09D-930-03', 'available': 5}, {'item': '777579', 'desc': 'SM16GA-09-60D-930-03', 'available': 5}, {'item': '777046', 'desc': 'SM16-09-25D-827-H1', 'available': 4}, {'item': '777670', 'desc': 'SP30S-14-36D-827-H1', 'available': 4}, {'item': '777722', 'desc': 'SP30S-18-36D-927-03', 'available': 4}, {'item': '772776', 'desc': 'LED10PAR30L/FL40/827/WD/2', 'available': 3}, {'item': '777931', 'desc': 'SR111-12-25D-927-03', 'available': 3}, {'item': '777683', 'desc': 'SP38-14-60D-830-H1', 'available': 3}, {'item': '777532', 'desc': 'SM16GA-09-60D-827-H1', 'available': 3}, {'item': '777723', 'desc': 'SP30S-18-60D-927-03', 'available': 3}, {'item': '777660', 'desc': 'SP30L-14-09D-827-H1', 'available': 3}, {'item': '777760', 'desc': 'SP38-18-09D-927-03', 'available': 3}, {'item': '777253', 'desc': 'SP20-11-10D-930-03', 'available': 2}, {'item': '777265', 'desc': 'SP20-11-36D-930-03', 'available': 2}, {'item': '777576', 'desc': 'SM16GA-09-36D-927-03', 'available': 2}, {'item': '777726', 'desc': 'SP30S-18-36D-930-03', 'available': 2}, {'item': '777702', 'desc': 'SP30L-18-36D-927-03', 'available': 2}, {'item': '777814', 'desc': 'AC-E-AM-0020-00-S1', 'available': 2}, {'item': '777828', 'desc': 'AC-E-FR-3636-00-S1', 'available': 2}, {'item': '777059', 'desc': 'SM16-07-36D-930-03', 'available': 2}, {'item': '777821', 'desc': 'AC-E-CC-0002-00-S1', 'available': 1}, {'item': '777048', 'desc': 'SM16-09-25D-830-H1', 'available': 1}, {'item': '777767', 'desc': 'SP38-18-60D-930-03', 'available': 1}, {'item': '777802', 'desc': 'AC-CC-0003-00-S1', 'available': 1}, {'item': '777673', 'desc': 'SP30S-14-25D-830-H1', 'available': 1}, {'item': '777815', 'desc': 'AC-E-EN-0001-00-S1', 'available': 1}, {'item': '777259', 'desc': 'SP20-11-25D-930-03', 'available': 1}, {'item': '777521', 'desc': 'SM16GA-07-10D-830-H1', 'available': 1}, {'item': '777533', 'desc': 'SM16GA-09-60D-830-H1', 'available': 1}, {'item': '777832', 'desc': 'SR111-19-36DM-927/918-01', 'available': 1}, {'item': '777578', 'desc': 'SM16GA-09-60D-927-03', 'available': 1}, {'item': '777724', 'desc': 'SP30S-18-09D-930-03', 'available': 1}, {'item': '777900', 'desc': 'SR111-18-09D-927-03', 'available': 1}] |
