# Section 2 Context Bundle — Ratana International Ltd. (ril)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Ratana International Ltd. (ril, org_id=245)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=1738, portal_order_gmv=$17.2M |
| HAS_INVENTORY | True | inventory_count=1514 |
| HAS_SALES_DATA | True | sales_data_count=24377 |
| HAS_SALES_SECTION | True | qualifying_reps=13 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | ratana_ril |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | FAIL | erp_gmv=$17.2M > ecat_gmv=$17.6M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 13 | 13 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 71 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1256, Mixpanel total submit_order (Q-01): 1973 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=77.5%, ambiguous_rate=76.4%, showroom_event_share=11.9% |
| USER_GROUP_JOIN_RATE | 77% | 55 of 71 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 12% | showroom+admin share of matched events: 11.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Winnie Ng |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=43 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=612 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=447 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Ratana International Ltd.
- **Shortname**: ril
- **Org ID**: 245
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS

## Section Confidence

# Section Confidence Tiers — Ratana International Ltd. (ril, org_id=245)
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

# Signal Rank — Ratana International Ltd. (ril, org_id=245)
- **Run date**: 2026-06-17
- **Total signals fired**: 66 (P0: 47, P1: 13, P2: 6)
- **Org GMV**: $17.6M eCat LTM, $17.2M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $4.7M total business | P1 | §5 Team | 23.3 | $4,660,027 | 2.0 | 217,158,516 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — UM00705BLK/C/DSC co-purchase pattern across 45 customers | P0 | §2/§3 | 4.5 | $20,580,100 | 2.0 | 185,220,898 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $4.3M+ total business, zero eCat orders | P1 | §2 Accounts | 4.3 | $4,286,761 | 2.0 | 36,752,640 | POSITIVE |
| 4 | SIG-MOM-01 | Account Acceleration — Isidore Landscapes Inc. 3 consecutive QoQ acceleration quarters, $199,696 peak quarter (+867% QoQ) | P0 | §2 Accounts | 28.9 | $199,696 | 3.0 | 17,305,657 | POSITIVE |
| 5 | SIG-ANOMALY-03 | Competitive Displacement — Evercare Contract Furnishings Inc. total biz +202% but eCat -14% | P0 | §2 Accounts | 14.4 | $292,762 | 3.0 | 12,664,878 | RISK |
| 6 | SIG-DECAY-01 | Reorder Decay — Kimpton Hotel Monaco Seattle 56.5x normal gap (113d vs 2d avg) | P0 | §2 Accounts | 56.5 | $65,100 | 3.0 | 11,034,450 | RISK |
| 7 | SIG-DECAY-01 | Reorder Decay — The Interior Design Group Inc 13.1x normal gap (208d vs 15d avg) | P0 | §2 Accounts | 13.1 | $268,331 | 3.0 | 10,545,408 | RISK |
| 8 | SIG-ANOMALY-03 | Competitive Displacement — Cash Account (US$) total biz +167% but eCat -49% | P0 | §2 Accounts | 14.4 | $241,135 | 3.0 | 10,383,263 | RISK |
| 9 | SIG-MOM-01 | Account Acceleration — Patio Options 3 consecutive QoQ acceleration quarters, $116,057 peak quarter (+852% QoQ) | P0 | §2 Accounts | 28.4 | $116,057 | 3.0 | 9,889,244 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — Les Fabrication Dor-val Ltee 3 consecutive QoQ acceleration quarters, $220,484 peak quarter (+390% QoQ) | P0 | §2 Accounts | 13.0 | $220,484 | 3.0 | 8,601,084 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — FN54401ASG (Lucia Club Chair) $285,951 LTM, 0 available | P0 | §3 Product | 10.0 | $285,951 | 3.0 | 8,578,530 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — UM00705BLK/C (7.5' Fiberglass Umbrella,38mm 2 Poles W/) $281,054 LTM, 0 available | P0 | §3 Product | 10.0 | $281,054 | 3.0 | 8,431,620 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — FN63020BLK (Toscana Lounger) $269,492 LTM, 0 available | P0 | §3 Product | 10.0 | $269,492 | 3.0 | 8,084,760 | RISK |
| 14 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 48% of eCat GMV | P1 | §4 Commerce | 1.2 | $3,065,209 | 2.0 | 7,381,866 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — FN61385LAG (Poinciana Highback Chair) $215,990 LTM, 0 available | P0 | §3 Product | 10.0 | $215,990 | 3.0 | 6,479,700 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — UM00605-55 (Umbrella Base, Steel, Square, 120lbs) $209,535 LTM, 0 available | P0 | §3 Product | 10.0 | $209,535 | 3.0 | 6,286,050 | RISK |
| 17 | SIG-MOM-01 | Account Acceleration — Timmermans Landscaping 2 consecutive QoQ acceleration quarters, $116,895 peak quarter (+485% QoQ) | P0 | §2 Accounts | 16.2 | $116,895 | 3.0 | 5,669,425 | POSITIVE |
| 18 | SIG-ANOMALY-02 | Stock Out — CU54401 (Lucia Club Chair Cushion) $184,283 LTM, 0 available | P0 | §3 Product | 10.0 | $184,283 | 3.0 | 5,528,490 | RISK |
| 19 | SIG-ANOMALY-02 | Stock Out — CU55001 (Copacabana Club Chair Cushion) $178,063 LTM, 0 available | P0 | §3 Product | 10.0 | $178,063 | 3.0 | 5,341,890 | RISK |
| 20 | SIG-ANOMALY-02 | Stock Out — FN61788WTR (Biltmore Swivel Recliner) $174,052 LTM, 0 available | P0 | §3 Product | 10.0 | $174,052 | 3.0 | 5,221,560 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 26 | 1 | 0 | 27 | |
| §3 Product Intelligence | 20 | 0 | 0 | 20 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 2 | 0 | 2 | |
| §6 Platform Context | 0 | 9 | 6 | 15 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $4.7M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — UM00705BLK/C/DSC co-purchase pattern across 45 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $4.3M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Isidore Landscapes Inc. 3 consecutive QoQ acceleration quarters, $199,696 peak quarter (+867% QoQ)
5. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — Evercare Contract Furnishings Inc. total biz +202% but eCat -14%
6. **[RISK]** SIG-DECAY-01: Reorder Decay — Kimpton Hotel Monaco Seattle 56.5x normal gap (113d vs 2d avg)
7. **[RISK]** SIG-DECAY-01: Reorder Decay — The Interior Design Group Inc 13.1x normal gap (208d vs 15d avg)

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Ratana International Ltd. (ril, org_id=245)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | KM-Associates Inc (REP) | 2 | DECAY-04, MOM-01 | $74,313 |
| 2 | Clutch Procurement & Consulting, LLC | 2 | DECAY-04, MOM-01 | $65,407 |
| 3 | Kimpton Hotel Monaco Seattle | 1 | DECAY-01 | $65,100 |
| 4 | The Interior Design Group Inc | 1 | DECAY-01 | $268,331 |
| 5 | TKA+D Architecture + Design | 1 | DECAY-01 | $313,672 |
| 6 | The Hotel Design Group | 1 | DECAY-01 | $140,999 |
| 7 | InnSpace Projects LLP | 1 | DECAY-01 | $258,985 |
| 8 | Let It Grow Inc. | 1 | DECAY-01 | $166,632 |
| 9 | Tamarainc (Sales Rep) | 1 | DECAY-01 | $125,914 |
| 10 | Living Revolution | 1 | DECAY-01 | $58,615 |

### Q-12_results.md

# Q-12 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 4,423 | 422 | 310 | 199 | 132 |

### Q-14_results.md

# Q-14 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 86945 | Patio & Home Direct | 111 | $187,567 | 2025-08-01 17:10:25 | 2026-06-17 20:15:22 | 2.90 |
| 67167 | Les Fabrication Dor-val Ltee | 38 | $637,656 | 2025-07-04 16:41:53 | 2026-06-15 19:55:48 | 9.40 |
| 87855 | Timmermans Landscaping | 31 | $430,492 | 2025-07-21 17:53:43 | 2026-04-30 16:21:12 | 9.40 |
| 87413 | Bishop's Casual Living | 23 | $17,961 | 2025-07-30 20:15:25 | 2026-05-30 21:45:14 | 13.80 |
| 87554 | Contract Furniture Solutions | 21 | $539,681 | 2025-06-30 17:04:41 | 2026-06-12 21:55:32 | 17.40 |
| U1657H | Fowler & Moore, Inc. | 20 | $286,422 | 2026-03-02 14:51:07 | 2026-06-03 23:46:39 | 4.90 |
| U1274H | Studio 4d | 20 | $137,769 | 2025-07-11 17:32:16 | 2026-05-04 21:31:17 | 15.60 |
| 80000H | Cash Account (c$) | 19 | $509,062 | 2025-06-25 19:10:47 | 2026-06-16 21:48:36 | 19.80 |
| 57575 | Stevans Sales And Marketing Inc. | 19 | $288,069 | 2025-06-19 16:07:46 | 2026-06-04 19:55:44 | 19.50 |
| 87481 | Bobby Design Inc. | 18 | $327,451 | 2025-07-29 22:42:09 | 2026-06-10 19:42:44 | 18.60 |
| 87868 | CHIL Interior Design | 18 | $488,658 | 2025-07-24 22:04:29 | 2026-04-29 17:59:08 | 16.40 |
| U1043H | Aegis Senior Communities, Llc | 16 | $102,803 | 2025-07-16 21:45:37 | 2026-06-16 16:10:41 | 22.30 |
| 86307 | The Interior Design Group Inc | 16 | $268,331 | 2025-06-27 18:41:26 | 2025-11-20 22:47:06 | 9.70 |
| 87607 | Polygon Interior Design Ltd. | 16 | $141,211 | 2025-08-08 18:40:43 | 2026-05-28 21:46:23 | 19.50 |
| U1295H | Northwest Trends | 15 | $257,021 | 2025-07-22 22:47:50 | 2026-06-16 16:13:14 | 23.50 |
| 87834 | Isidore Landscapes Inc. | 14 | $330,063 | 2025-06-20 22:24:20 | 2026-06-15 20:31:56 | 27.70 |
| 57576A | Algonquin Resort LP o/a The Algonquin Resort | 11 | $890,152 | 2025-10-22 19:00:21 | 2026-06-02 17:41:10 | 22.30 |
| 87849 | Evercare Contract Furnishings Inc. | 11 | $115,938 | 2025-06-20 17:16:34 | 2026-06-15 22:59:58 | 36 |
| U1171H | Trio, Inc. | 11 | $52,468 | 2025-07-09 22:21:09 | 2026-04-23 21:12:45 | 28.80 |
| U1044H | Anthony's Restaurants | 10 | $263,026 | 2026-03-10 20:59:44 | 2026-05-05 05:12:58 | 6.10 |

### Q-14b_results.md

# Q-14b Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 11
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| U41413 | KB Patio | 8 | 13 | 50.20 | 3.86 | $228,136 |
| U4606H | The Design Resource Group, Inc. | 8 | 10.30 | 32.20 | 3.13 | $122,735 |
| U51031 | Linda Cezar (sales Rep) | 10 | 8.30 | 72 | 8.67 | $92,967 |
| U4044H | HDB Design Group, LLC. | 12 | 30.40 | 47 | 1.55 | $81,989 |
| U2005H | Direct Supply Inc. | 6 | 10 | 62.30 | 6.23 | $63,797 |
| 80000 | Cash Account | 6 | 35 | 74 | 2.11 | $46,547 |
| U1567H | Redwood Construction | 4 | 4 | 83.50 | 20.88 | $44,651 |
| U1690H | Joanna Branzell Interior Design | 4 | 41.50 | 168 | 4.05 | $37,233 |
| 87849 | Evercare Contract Furnishings Inc. | 5 | 29 | 129.70 | 4.47 | $34,354 |
| 15330 | ACL Design Build Solutions | 4 | 54 | 185.50 | 3.44 | $13,808 |
| 67223 | Restotrends Inc. | 4 | 46.50 | 194.50 | 4.18 | $13,543 |

### Q-17_results.md

# Q-17 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| U4148H | Saia Trim Group | MS | 2026-01-29 22:16:07 | 6 | $447,182 |
| 86307 | The Interior Design Group Inc | BC | 2025-11-20 22:47:06 | 16 | $268,331 |
| 87532 | Waterfront Hospitality Inc | BC | 2026-02-26 23:59:24 | 8 | $263,545 |
| U1548H | InnSpace Projects LLP | MT | 2025-12-19 17:38:18 | 9 | $258,985 |
| U3179H | Harp Team LLC(Rep) | NY | 2025-11-19 20:27:06 | 7 | $166,632 |
| 87895 | West One Design Inc. | BC | 2026-01-30 20:07:32 | 2 | $166,487 |
| U6052H | The Hotel Design Group | FL | 2026-02-17 18:18:45 | 5 | $140,999 |
| 67165 | Le Chateau Montebello, Evergrande Hotel Hold | QC | 2025-08-01 20:19:28 | 5 | $133,629 |
| U4875H | Casella Interiors | TN | 2026-01-27 18:52:01 | 3 | $129,162 |
| U1553H | Tamarainc (Sales Rep) | CA | 2026-01-23 18:19:59 | 7 | $125,914 |
| U2076H | Pure Workplace Solutions | MO | 2025-12-23 17:39:14 | 2 | $122,760 |
| U1816H | Meden Agan Studio | CA | 2025-08-27 18:16:32 | 4 | $118,367 |
| U3248H | Let It Grow Inc. | NJ | 2025-11-03 21:04:39 | 1 | $111,495 |
| U6012H | Sandman Signature Plano | TX | 2025-08-06 21:59:03 | 1 | $101,539 |
| 28112 | Contemporary Office Interiors Ltd | AB | 2026-02-24 23:39:16 | 2 | $99,670 |
| 67061 | Amenagement Et Design Sportscene inc. | QC | 2025-11-12 16:37:16 | 1 | $96,759 |
| 57576 | InnVest Hotels Limited | ON | 2025-08-15 17:10:22 | 2 | $85,642 |
| U31135 | Sequoia Outback | PA | 2025-08-27 21:54:32 | 3 | $81,128 |
| 57704 | The Chega Group | ON | 2026-03-13 15:39:21 | 3 | $79,866 |
| 57594 | Tarrison Products Ltd. | ON | 2025-08-22 16:26:16 | 1 | $77,192 |
| U4185H | Hilton Supply Management | VA | 2026-01-30 20:03:05 | 3 | $73,277 |
| U4870H | Prime Home Builders | FL | 2025-08-06 16:05:09 | 2 | $71,725 |
| U4911H | Lang & Schwander Hotel Interios | FL | 2026-02-18 19:58:13 | 1 | $69,957 |
| U1826H | Kimpton Hotel Monaco Seattle | WA | 2026-02-23 22:04:27 | 5 | $65,100 |
| U2261H | Living Revolution | IL | 2026-02-06 18:39:04 | 6 | $58,615 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| U4148H | Saia Trim Group | MS | $447,182 | 2026-01-29 22:16:07 | 138 |
| 86307 | The Interior Design Group Inc | BC | $268,331 | 2025-11-20 22:47:06 | 208 |
| 87532 | Waterfront Hospitality Inc | BC | $263,545 | 2026-02-26 23:59:24 | 110 |
| U1548H | InnSpace Projects LLP | MT | $258,985 | 2025-12-19 17:38:18 | 180 |
| U3179H | Harp Team LLC(Rep) | NY | $166,632 | 2025-11-19 20:27:06 | 210 |
| 87895 | West One Design Inc. | BC | $166,487 | 2026-01-30 20:07:32 | 138 |
| U6052H | The Hotel Design Group | FL | $140,999 | 2026-02-17 18:18:45 | 120 |
| 67165 | Le Chateau Montebello, Evergrande Hotel Hold | QC | $133,629 | 2025-08-01 20:19:28 | 320 |
| U4875H | Casella Interiors | TN | $129,162 | 2026-01-27 18:52:01 | 141 |
| U1553H | Tamarainc (Sales Rep) | CA | $125,914 | 2026-01-23 18:19:59 | 145 |
| U2076H | Pure Workplace Solutions | MO | $122,760 | 2025-12-23 17:39:14 | 176 |
| U1816H | Meden Agan Studio | CA | $118,367 | 2025-08-27 18:16:32 | 294 |
| U3248H | Let It Grow Inc. | NJ | $111,495 | 2025-11-03 21:04:39 | 225 |
| U6012H | Sandman Signature Plano | TX | $101,539 | 2025-08-06 21:59:03 | 314 |
| 28112 | Contemporary Office Interiors Ltd | AB | $99,670 | 2026-02-24 23:39:16 | 112 |
| 67061 | Amenagement Et Design Sportscene inc. | QC | $96,759 | 2025-11-12 16:37:16 | 217 |
| 57576 | InnVest Hotels Limited | ON | $85,642 | 2025-08-15 17:10:22 | 306 |
| U31135 | Sequoia Outback | PA | $81,128 | 2025-08-27 21:54:32 | 293 |
| 57704 | The Chega Group | ON | $79,866 | 2026-03-13 15:39:21 | 96 |
| 57594 | Tarrison Products Ltd. | ON | $77,192 | 2025-08-22 16:26:16 | 299 |

### Q-40_results.md

# Q-40 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| BC | 80 | 461 | $5.8M |
| ON | 16 | 70 | $1.7M |
| QC | 11 | 72 | $1.3M |
| CA | 35 | 113 | $1.1M |
| WA | 13 | 70 | $1.0M |
| FL | 22 | 52 | $771,885 |
| MS | 2 | 7 | $447,402 |
| AB | 14 | 43 | $418,622 |
| CO | 11 | 57 | $405,684 |
| NS | 3 | 10 | $404,310 |
| IL | 3 | 14 | $308,013 |
| MT | 3 | 14 | $296,351 |
| NY | 5 | 15 | $222,249 |
| NJ | 4 | 7 | $206,128 |
| OR | 9 | 22 | $204,002 |
| GA | 11 | 25 | $177,800 |
| PA | 5 | 7 | $168,078 |
| NV | 4 | 19 | $166,261 |
| TN | 3 | 7 | $147,763 |
| MO | 5 | 7 | $140,326 |

### Q-41_results.md

# Q-41 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 26
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 22 |
| 2025-04-01 | Rep-Acquired (iPad) | 40 |
| 2025-05-01 | Rep-Acquired (iPad) | 30 |
| 2025-05-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-06-01 | Rep-Acquired (iPad) | 22 |
| 2025-07-01 | Rep-Acquired (iPad) | 20 |
| 2025-07-01 | eCat Online-Acquired (self-serve) | 3 |
| 2025-08-01 | Rep-Acquired (iPad) | 14 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-09-01 | Rep-Acquired (iPad) | 23 |
| 2025-10-01 | Rep-Acquired (iPad) | 12 |
| 2025-10-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-11-01 | Rep-Acquired (iPad) | 10 |
| 2025-12-01 | Rep-Acquired (iPad) | 10 |
| 2025-12-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 14 |
| 2026-02-01 | Rep-Acquired (iPad) | 16 |
| 2026-02-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-03-01 | Rep-Acquired (iPad) | 19 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 3 |
| 2026-04-01 | Rep-Acquired (iPad) | 14 |
| 2026-04-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-05-01 | Rep-Acquired (iPad) | 16 |
| 2026-05-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-06-01 | Rep-Acquired (iPad) | 16 |
| 2026-06-01 | eCat Online-Acquired (self-serve) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Yash Roy | 140 |
| Allison Tsoi | 33 |
| Sheryl Madonna | 22 |
| Michele Gee | 12 |
| Meghan Crandall | 11 |
| Kim King | 10 |
| Bryan Gladstone | 8 |
| John Fangman | 8 |
| Sylvia Ou | 7 |
| Gayle Massey | 6 |
| Johnny  Hostetter | 6 |
| Rayna Huang  | 6 |
| Tamara Bartley | 5 |
| Michael Urkowitz | 4 |
| Steven McFarlain | 3 |
| Shelley Straughan | 3 |
| Winnie Ng | 3 |
| Jean Louis Jalbert | 2 |
| Jim Connell | 2 |
| Steve Aman | 2 |
| Ashley Larrick | 1 |
| Sondra Walbert | 1 |
| Elaine Voong | 1 |
| Desiree Gladstone | 1 |
| Joe Crandall | 1 |

### Q-52_results.md

# Q-52 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| U1090H | Starbucks Coffee | WA | 49 | $1.9M | 0 | $0 | 0 |
| 67167 | Les Fabrication Dor-val Ltee | QC | 20 | $457,336 | 38 | $637,656 | 139.40 |
| 87834 | Isidore Landscapes Inc. | BC | 11 | $358,446 | 14 | $330,063 | 92.10 |
| 80000H | Cash Account (c$) | BC | 12 | $310,462 | 19 | $509,062 | 164 |
| U3248H | Let It Grow Inc. | NJ | 2 | $302,771 | 1 | $111,495 | 36.80 |
| 87554 | Contract Furniture Solutions | BC | 16 | $247,856 | 21 | $539,681 | 217.70 |
| U4185H | Hilton Supply Management | VA | 16 | $234,259 | 3 | $73,277 | 31.30 |
| 87526 | Vancouver Sofa & Patio | BC | 65 | $230,498 | 0 | $0 | 0 |
| U41413 | KB Patio | FL | 9 | $228,136 | 0 | $0 | 0 |
| 87855 | Timmermans Landscaping | BC | 18 | $227,294 | 31 | $430,492 | 189.40 |
| U4612H | Wegman Design Group | FL | 7 | $218,941 | 0 | $0 | 0 |
| U4871H | Patio Options | NC | 18 | $216,218 | 0 | $0 | 0 |
| U5004H | Summa International | HI | 5 | $214,351 | 2 | $12,854 | 6 |
| U1295H | Northwest Trends | WA | 12 | $168,795 | 15 | $257,021 | 152.30 |
| U4875H | Casella Interiors | TN | 4 | $163,750 | 3 | $129,162 | 78.90 |
| 87868 | CHIL Interior Design | BC | 6 | $156,135 | 18 | $488,658 | 313 |
| U1027H | Urban Design Studio | NV | 23 | $150,055 | 10 | $80,312 | 53.50 |
| U6090H | The Villages | FL | 3 | $142,748 | 0 | $0 | 0 |
| U41309 | Sunnyland Furniture | TX | 9 | $139,735 | 0 | $0 | 0 |
| U2265H | Fairlawn Country Club | OH | 5 | $138,097 | 0 | $0 | 0 |
| 87532 | Waterfront Hospitality Inc | BC | 5 | $134,819 | 8 | $263,545 | 195.50 |
| U2126H | The Getty Group | IL | 5 | $127,951 | 7 | $160,167 | 125.20 |
| 85891 | Industrial Revolution | BC | 16 | $126,611 | 8 | $27,034 | 21.40 |
| 86307 | The Interior Design Group Inc | BC | 6 | $125,815 | 16 | $268,331 | 213.30 |
| 87268 | F.E.K. Enterprises Inc. | BC | 38 | $123,367 | 0 | $0 | 0 |
| U4606H | The Design Resource Group, Inc. | FL | 9 | $122,735 | 9 | $114,972 | 93.70 |
| U3258H | At Work Collaborative | MA | 6 | $121,409 | 6 | $109,058 | 89.80 |
| 67247 | Dalfen Sales Agency Inc | QC | 3 | $118,460 | 4 | $177,318 | 149.70 |
| 67259 | Image Urbaine | QC | 5 | $114,835 | 8 | $83,507 | 72.70 |
| U4579H | Great Wolf Resorts Holdings, Inc | WI | 1 | $108,152 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| U1090H | Starbucks Coffee | WA | 49 | $1.9M |
| 87526 | Vancouver Sofa & Patio | BC | 65 | $230,498 |
| U41413 | KB Patio | FL | 9 | $228,136 |
| U4612H | Wegman Design Group | FL | 7 | $218,941 |
| U4871H | Patio Options | NC | 18 | $216,218 |
| U6090H | The Villages | FL | 3 | $142,748 |
| U2265H | Fairlawn Country Club | OH | 5 | $138,097 |
| U4579H | Great Wolf Resorts Holdings, Inc | WI | 1 | $108,152 |
| 87818 | Foris Projects Inc | BC | 3 | $106,472 |
| 57680 | POI Business Interiors LP | ON | 2 | $104,065 |
| 35496 | Garden Architecture & Design | SK | 10 | $102,195 |
| 28115 | Beachcomber Hot Tubs & Outdoor Living | AB | 12 | $101,096 |
| U3190H | RD Jones | MD | 8 | $99,215 |
| U4329H | Purchasing Management International L.P | TX | 1 | $92,650 |
| U6059H | Tom Hoch Interior Designs Inc | OK | 1 | $92,253 |
| U41417 | Tri Supply Company | TX | 4 | $88,546 |
| U3274H | ADM Management NY Corp. | NY | 6 | $81,334 |
| U4148HA | Osage Casinos c/o Saia Trim Group (Agent) | BC | 1 | $80,122 |
| U5026H | Luana Hospitality Group | HI | 2 | $78,529 |
| U2289H | Interior Environments | MI | 2 | $77,494 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BC | 102 | 458 | $3.7M | 80 | 461 | $5.8M | 154.40 |
| WA | 12 | 84 | $2.3M | 13 | 70 | $1.0M | 43 |
| FL | 49 | 116 | $1.4M | 22 | 52 | $771,885 | 55.10 |
| QC | 26 | 74 | $1.0M | 11 | 72 | $1.3M | 124.20 |
| TX | 40 | 76 | $799,087 | 11 | 15 | $134,868 | 16.90 |
| CA | 50 | 100 | $596,475 | 35 | 113 | $1.1M | 185.60 |
| ON | 30 | 71 | $573,946 | 16 | 70 | $1.7M | 297.40 |
| HI | 11 | 29 | $533,901 | 7 | 19 | $106,238 | 19.90 |
| AB | 22 | 94 | $470,995 | 14 | 43 | $418,622 | 88.90 |
| IL | 20 | 58 | $441,316 | 3 | 14 | $308,013 | 69.80 |
| NJ | 3 | 8 | $338,652 | 4 | 7 | $206,128 | 60.90 |
| GA | 25 | 49 | $322,328 | 11 | 25 | $177,800 | 55.20 |
| PA | 18 | 53 | $300,565 | 5 | 7 | $168,078 | 55.90 |
| TN | 8 | 11 | $294,462 | 3 | 7 | $147,763 | 50.20 |
| NC | 8 | 38 | $288,190 | 0 | 0 | $0 | 0 |
| CO | 24 | 48 | $288,014 | 11 | 57 | $405,684 | 140.90 |
| NV | 6 | 30 | $273,247 | 4 | 19 | $166,261 | 60.80 |
| MD | 12 | 29 | $266,438 | 1 | 1 | $4,136 | 1.60 |
| VA | 4 | 24 | $262,877 | 1 | 3 | $73,277 | 27.90 |
| AZ | 21 | 26 | $231,365 | 9 | 12 | $121,716 | 52.60 |

### Q-57_results.md

# Q-57 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

# Q-66 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-66 — Buyer-Within-Account Intelligence
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | new_buyers | existing_buyers | new_buyer_orders | new_buyer_revenue | earliest_new_buyer |
| --- | --- | --- | --- | --- | --- |
| Northwest Trends | 1 | 0 | 12 | 155,948.29 | 2026-4-10 |
| Vancouver Sofa & Patio | 1 | 0 | 58 | 154,383.02 | 2026-3-25 |
| F.E.K. Enterprises Inc. | 1 | 0 | 38 | 117,492.56 | 2026-3-27 |
| Patio Options | 1 | 0 | 11 | 110,251.29 | 2026-3-23 |
| Image Urbaine | 1 | 0 | 4 | 105,069.29 | 2026-4-1 |
| Isidore Landscapes Inc. | 1 | 0 | 4 | 104,781.77 | 2026-3-20 |
| Tom Hoch Interior Designs Inc | 1 | 0 | 1 | 92,254.33 | 2026-6-1 |
| ADM Management NY Corp. | 1 | 0 | 6 | 81,333.59 | 2026-5-19 |
| Spirit Ridge Resort | 1 | 0 | 3 | 70,893.50 | 2026-4-15 |
| Peachtree Group | 1 | 0 | 1 | 69,207.07 | 2026-5-1 |
| Net Retailers LLC | 1 | 0 | 22 | 68,722.82 | 2026-5-4 |
| The Childs Dreyfus Group | 1 | 0 | 2 | 66,320.45 | 2026-4-22 |
| Maritime Hospitality (Danja Inc) | 1 | 0 | 1 | 60,851.86 | 2026-5-11 |
| Era Living LLC | 1 | 0 | 5 | 56,277.63 | 2026-4-7 |
| Midwest Commercial Interiors | 1 | 0 | 3 | 50,444.93 | 2026-4-24 |
| Benjamin West (as Agent) | 1 | 0 | 3 | 47,806.29 | 2026-3-30 |
| Fowler & Moore, Inc. | 1 | 0 | 6 | 47,738.46 | 2026-6-3 |
| Dalfen Sales Agency Inc | 1 | 0 | 2 | 47,722.65 | 2026-4-16 |
| Aqua Fire Leisure | 1 | 0 | 8 | 47,457.68 | 2026-3-24 |
| Wicker Land Patio - Victoria | 1 | 0 | 20 | 44,967.82 | 2026-5-1 |

### Q-67_results.md

# Q-67 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BC | $748,114 | $1.6M | 112.60 | 76 | 25 | 51 | 337 |
| CA | $263,320 | $1.1M | 335.60 | 37 | 16 | 21 | 93 |
| TN | $9,781 | $1.1M | 11,625.60 | 4 | 3 | 1 | 34 |
| QC | $50,362 | $470,640 | 834.50 | 17 | 5 | 12 | 45 |
| TX | $75,213 | $453,003 | 502.30 | 31 | 7 | 24 | 53 |
| FL | $491,250 | $258,400 | -47.40 | 26 | 32 | -6 | 46 |
| WA | $20,203 | $255,656 | 1,165.40 | 11 | 4 | 7 | 23 |
| AB | $69,336 | $239,274 | 245.10 | 13 | 6 | 7 | 72 |
| ON | $47,177 | $224,849 | 376.60 | 28 | 3 | 25 | 63 |
| OK | $93,534 | $200,206 | 114 | 6 | 2 | 4 | 9 |
| GA | $12,460 | $170,438 | 1,267.90 | 15 | 4 | 11 | 18 |
| OH | $15,303 | $135,857 | 787.80 | 5 | 2 | 3 | 8 |
| CO | $51,483 | $130,574 | 153.60 | 21 | 6 | 15 | 35 |
| IL | $34,992 | $126,544 | 261.60 | 11 | 3 | 8 | 15 |
| NC | $16,219 | $122,113 | 652.90 | 9 | 3 | 6 | 18 |
| AZ | $81,442 | $105,102 | 29.10 | 13 | 4 | 9 | 16 |
| NY | $25,063 | $102,197 | 307.80 | 7 | 3 | 4 | 13 |
| Unknown | $594,489 | $99,076 | -83.30 | 12 | 19 | -7 | 13 |
| UT | $28,258 | $74,929 | 165.20 | 8 | 3 | 5 | 11 |
| QU | $47,971 | $71,517 | 49.10 | 7 | 1 | 6 | 9 |
| NV | $64,534 | $62,181 | -3.60 | 6 | 3 | 3 | 10 |
| KS | $17,257 | $60,326 | 249.60 | 6 | 4 | 2 | 9 |
| MI | $22,595 | $40,376 | 78.70 | 7 | 3 | 4 | 8 |
| SK | $70,526 | $30,411 | -56.90 | 3 | 2 | 1 | 9 |
| VA | $119,828 | $23,046 | -80.80 | 6 | 5 | 1 | 11 |

### Q-68_results.md

# Q-68 Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| Trio, Inc. | Unknown | $5,406 | $352,642 | $347,235 | 1.50 | 2 |
| Ratana International Ltd | Unknown | $129,233 | $424,681 | $295,447 | 30.40 | 3 |
| Stevans Sales And Marketing Inc. | ON | $37,349 | $189,226 | $151,877 | 19.70 | 3 |
| HDB Design Group, LLC. | Unknown | $80,878 | $213,066 | $132,189 | 38 | 6 |
| KM-Associates Inc (REP) | FL | $47,235 | $170,506 | $123,271 | 27.70 | 5 |
| Clutch Procurement & Consulting, LLC | NC | $50,541 | $171,351 | $120,810 | 29.50 | 3 |
| Timmermans Landscaping | BC | $208,015 | $311,754 | $103,739 | 66.70 | 7 |
| Dalfen Sales Agency Inc | QC | $111,349 | $181,551 | $70,201 | 61.30 | 2 |
| Lang & Schwander Hotel Interios | FL | $82,164 | $115,342 | $33,178 | 71.20 | 4 |
| Cash Account (US$) | IL | $27,450 | $38,445 | $10,995 | 71.40 | 4 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| customer_num | customer_name | state | ltm_orders | ltm_gmv | last_order | days_since_last | avg_days_between | decay_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U1826H | Kimpton Hotel Monaco Seattle | WA | 5 | $65,100 | 2026-02-23 22:04:27 | 113 | 2 | 56.50 |
| 86307 | The Interior Design Group Inc | BC | 16 | $268,331 | 2025-11-20 22:47:06 | 208 | 15.90 | 13.10 |
| 87909 | TKA+D Architecture + Design | BC | 6 | $313,672 | 2026-03-20 21:31:12 | 88 | 20.50 | 4.30 |
| U6052H | The Hotel Design Group | FL | 5 | $140,999 | 2026-02-17 18:18:45 | 120 | 13.50 | 8.90 |
| U1548H | InnSpace Projects LLP | MT | 9 | $258,985 | 2025-12-19 17:38:18 | 180 | 52.80 | 3.40 |
| U3179H | Let It Grow Inc. | NY | 7 | $166,632 | 2025-11-19 20:27:06 | 210 | 51 | 4.10 |
| U1553H | Tamarainc (Sales Rep) | CA | 7 | $125,914 | 2026-01-23 18:19:59 | 145 | 32.20 | 4.50 |
| U2261H | Living Revolution | IL | 6 | $58,615 | 2026-02-06 18:39:04 | 131 | 36.50 | 3.60 |
| 57269 | Elite Contract Furniture Ltd | ON | 8 | $68,182 | 2026-04-10 20:43:04 | 67 | 26.70 | 2.50 |

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 50
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 67167 | Les Fabrication Dor-val Ltee | 457,335.55 | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | DSC | — | 45 |
| U3248H | Let It Grow Inc. | 302,771.18 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4185H | Hilton Supply Management | 234,258.66 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| 87526 | Vancouver Sofa & Patio | 230,497.78 | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | DSC | — | 45 |
| U41413 | KB Patio | 228,136.18 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4612H | Wegman Design Group | 218,940.91 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4871H | Patio Options | 216,218.09 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U5004H | Summa International | 214,351 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U3258H | At Work Collaborative | 180,187.49 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4875H | Casella Interiors | 163,749.73 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U1027H | Urban Design Studio | 150,055.44 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U6090H | The Villages | 142,748.34 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U41309 | Sunnyland Furniture | 139,735 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U2265H | Fairlawn Country Club | 138,096.63 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U2126H | The Getty Group | 127,951.06 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| 86307 | The Interior Design Group Inc | 125,814.84 | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | DSC | — | 45 |
| U4606H | The Design Resource Group, Inc. | 122,734.54 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4579H | Great Wolf Resorts Holdings, Inc | 108,152.39 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| 87909 | TKA+D Architecture + Design | 104,841.71 | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | DSC | — | 45 |
| U4148H | Saia Trim Group | 100,883.07 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U3190H | RD Jones | 99,215.47 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U51031 | Linda Cezar (sales Rep) | 92,966.55 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4329H | Purchasing Management International L.P | 92,650.24 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4911H | Lang & Schwander Hotel Interios | 90,026.13 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U41417 | Tri Supply Company | 88,546.25 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U3274H | ADM Management NY Corp. | 81,333.90 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U4148HA | Osage Casinos c/o Saia Trim Group (Agent) | 80,121.82 | DSC | — | UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | 45 |
| U3248H | Let It Grow Inc. | 302,771.18 | DSC | — | UM00605-55 | Umbrella Base, Steel, Square, 120lbs | 38 |
| U4185H | Hilton Supply Management | 234,258.66 | DSC | — | UM00605-55 | Umbrella Base, Steel, Square, 120lbs | 38 |
| U41413 | KB Patio | 228,136.18 | DSC | — | UM00605-55 | Umbrella Base, Steel, Square, 120lbs | 38 |

*(Truncated: showing top 30 of 50 rows. Full data in cache file.)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 18
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 57575 | Stevans Sales And Marketing Inc. | ON | 42,204.63 | 171,621.43 | -75.40 | 305,615.71 | 214,062.03 | 42.80 | CONTRACTING |
| U3179H | Harp Team LLC(Rep) | NY | 63,524.55 | 138,005.72 | -54 | 166,631.52 | 20,928.90 | 696.20 | CONTRACTING |
| U4195H | KM-Associates Inc (REP) | FL | 51,413.66 | 125,726.88 | -59.10 | 66,647.53 | 0 | — | CONTRACTING |
| U1518H | Clutch Procurement & Consulting, LLC | CO | 55,292.07 | 120,699.20 | -54.20 | 35,196.78 | 73,570.68 | -52.20 | CONTRACTING |
| U4044H | HDB Design Group, LLC. | FL | 81,989.26 | 131,473.36 | -37.60 | 50,660.58 | 85,085.48 | -40.50 | CONTRACTING |
| 87849 | Evercare Contract Furnishings Inc. | BC | 34,353.91 | 11,373.86 | 202 | 115,938.01 | 135,349.91 | -14.30 | COMPETITIVE_DISPLACEMENT |
| U8000H | Cash Account (US$) | BC | 29,996.68 | 11,247.20 | 166.70 | 57,544.48 | 111,999.43 | -48.60 | COMPETITIVE_DISPLACEMENT |
| USCTC | Ratana International Ltd | MI | 67,726.80 | 66,299.57 | 2.20 | 47,781.01 | 66,299.57 | -27.90 | COMPETITIVE_DISPLACEMENT |
| U3053H | Furniture Solutions Group | MD | 51,389.97 | 0 | — | 0 | 4,950.36 | -100 | COMPETITIVE_DISPLACEMENT |
| 84337 | Country Furniture | BC | 53,164.87 | 0 | — | 0 | 2,584.80 | -100 | COMPETITIVE_DISPLACEMENT |
| U1061H | Benjamin West (as Agent) | CO | 52,469.52 | 0 | — | 46,645.44 | 183,554.80 | -74.60 | COMPETITIVE_DISPLACEMENT |
| U41309 | Sunnyland Furniture | TX | 139,735 | 0 | — | 0 | 26,114.64 | -100 | COMPETITIVE_DISPLACEMENT |
| U4191H | Carver & Associates | GA | 69,792.57 | 0 | — | 0 | 477.54 | -100 | COMPETITIVE_DISPLACEMENT |
| 87793 | Northland Properties Corporation | BC | 32,686.93 | 0 | — | 32,743.50 | 50,604.21 | -35.30 | COMPETITIVE_DISPLACEMENT |
| U4250H | Eatz Hospitality/Del Boca Brickell LP | TX | 25,775.86 | 0 | — | 0 | 49,998.90 | -100 | COMPETITIVE_DISPLACEMENT |
| U4939H | R.R. Williams & Associates | TX | 27,769.31 | 0 | — | 0 | 9,592.64 | -100 | COMPETITIVE_DISPLACEMENT |
| 87268 | F.E.K. Enterprises Inc. | BC | 123,367.25 | 0 | — | 0 | 716.40 | -100 | COMPETITIVE_DISPLACEMENT |
| 85891 | Industrial Revolution | BC | 126,610.79 | 0 | — | 27,033.95 | 85,713.27 | -68.50 | COMPETITIVE_DISPLACEMENT |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 67167 | Les Fabrication Dor-val Ltee | 3 | 220,484.08 | 390.10 | [{'quarter': '2025-07-01', 'revenue': 220484.08, 'qoq_pct': 390.1}, {'quarter': '2025-10-01', 'revenue': 19514.1, 'qoq_pct': -91.1}, {'quarter': '2026-01-01', 'revenue': 48672.02, 'qoq_pct': 149.4}, {'quarter': '2026-04-01', 'revenue': 168665.35, 'qoq_pct': 246.5}] |
| 87834 | Isidore Landscapes Inc. | 3 | 199,696.02 | 866.60 | [{'quarter': '2025-07-01', 'revenue': 38773.79, 'qoq_pct': 866.6}, {'quarter': '2025-10-01', 'revenue': 199696.02, 'qoq_pct': 415.0}, {'quarter': '2026-01-01', 'revenue': 45146.4, 'qoq_pct': -77.4}, {'quarter': '2026-04-01', 'revenue': 74830.26, 'qoq_pct': 65.8}] |
| U5004H | Summa International | 2 | 198,106.91 | 1,478.70 | [{'quarter': '2025-10-01', 'revenue': 3694.99, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 12549.1, 'qoq_pct': 239.6}, {'quarter': '2026-04-01', 'revenue': 198106.91, 'qoq_pct': 1478.7}] |
| 87526 | Vancouver Sofa & Patio | 3 | 144,399.57 | 20,515.50 | [{'quarter': '2025-07-01', 'revenue': 64938.76, 'qoq_pct': 20515.5}, {'quarter': '2025-10-01', 'revenue': 3457.13, 'qoq_pct': -94.7}, {'quarter': '2026-01-01', 'revenue': 17702.32, 'qoq_pct': 412.1}, {'quarter': '2026-04-01', 'revenue': 144399.57, 'qoq_pct': 715.7}] |
| 87554 | Contract Furniture Solutions | 2 | 129,441.08 | 1,158.10 | [{'quarter': '2025-07-01', 'revenue': 6599.05, 'qoq_pct': -67.7}, {'quarter': '2025-10-01', 'revenue': 83021.88, 'qoq_pct': 1158.1}, {'quarter': '2026-01-01', 'revenue': 28794.41, 'qoq_pct': -65.3}, {'quarter': '2026-04-01', 'revenue': 129441.08, 'qoq_pct': 349.5}] |
| 87855 | Timmermans Landscaping | 2 | 116,895.36 | 485 | [{'quarter': '2025-10-01', 'revenue': 116895.36, 'qoq_pct': 485.0}, {'quarter': '2026-01-01', 'revenue': 31481.45, 'qoq_pct': -73.1}, {'quarter': '2026-04-01', 'revenue': 78917.37, 'qoq_pct': 150.7}] |
| U4871H | Patio Options | 3 | 116,057.32 | 852.10 | [{'quarter': '2025-07-01', 'revenue': 74122.76, 'qoq_pct': 596.8}, {'quarter': '2025-10-01', 'revenue': 3211.53, 'qoq_pct': -95.7}, {'quarter': '2026-01-01', 'revenue': 12189.13, 'qoq_pct': 279.5}, {'quarter': '2026-04-01', 'revenue': 116057.32, 'qoq_pct': 852.1}] |
| U4911H | Lang & Schwander Hotel Interios | 2 | 68,573.39 | 509.80 | [{'quarter': '2025-07-01', 'revenue': 10206.97, 'qoq_pct': 68.6}, {'quarter': '2025-10-01', 'revenue': 11245.77, 'qoq_pct': 10.2}, {'quarter': '2026-01-01', 'revenue': 68573.39, 'qoq_pct': 509.8}] |
| U4044H | HDB Design Group, LLC. | 2 | 57,129.30 | 9,866.80 | [{'quarter': '2025-07-01', 'revenue': 237.62, 'qoq_pct': -98.8}, {'quarter': '2026-01-01', 'revenue': 23683.08, 'qoq_pct': 9866.8}, {'quarter': '2026-04-01', 'revenue': 57129.3, 'qoq_pct': 141.2}] |
| U3069H | Hospitality Furnishings & Design Inc | 2 | 54,505.32 | 551.70 | [{'quarter': '2025-07-01', 'revenue': 2099.9, 'qoq_pct': None}, {'quarter': '2025-10-01', 'revenue': 13684.58, 'qoq_pct': 551.7}, {'quarter': '2026-01-01', 'revenue': 54505.32, 'qoq_pct': 298.3}, {'quarter': '2026-04-01', 'revenue': 8817.26, 'qoq_pct': -83.8}] |
| 80000 | Cash Account | 2 | 41,034.07 | 783.30 | [{'quarter': '2025-07-01', 'revenue': 867.23, 'qoq_pct': -53.5}, {'quarter': '2026-01-01', 'revenue': 4645.62, 'qoq_pct': 435.7}, {'quarter': '2026-04-01', 'revenue': 41034.07, 'qoq_pct': 783.3}] |
| U1518H | Clutch Procurement & Consulting, LLC | 2 | 35,452.24 | 205.70 | [{'quarter': '2025-07-01', 'revenue': 8243.59, 'qoq_pct': -68.9}, {'quarter': '2025-10-01', 'revenue': 11596.24, 'qoq_pct': 40.7}, {'quarter': '2026-01-01', 'revenue': 35452.24, 'qoq_pct': 205.7}] |
| U4195H | KM-Associates Inc (REP) | 2 | 25,653.17 | 348.30 | [{'quarter': '2025-10-01', 'revenue': 20037.84, 'qoq_pct': 234.9}, {'quarter': '2026-01-01', 'revenue': 5722.65, 'qoq_pct': -71.4}, {'quarter': '2026-04-01', 'revenue': 25653.17, 'qoq_pct': 348.3}] |
| U4333H | LG AS Manager LLC | 2 | 20,429.44 | 190.90 | [{'quarter': '2025-07-01', 'revenue': 3654.51, 'qoq_pct': None}, {'quarter': '2026-01-01', 'revenue': 7023.1, 'qoq_pct': 92.2}, {'quarter': '2026-04-01', 'revenue': 20429.44, 'qoq_pct': 190.9}] |
| U3217H | Dash Design | 2 | 12,948.37 | 805.20 | [{'quarter': '2025-10-01', 'revenue': 3954.08, 'qoq_pct': 805.2}, {'quarter': '2026-01-01', 'revenue': 12948.37, 'qoq_pct': 227.5}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Ratana International Ltd. (ril, org_id=245)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FN54401ASG | Lucia Club Chair | LUCIA | 285,951 | 518 | 9 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 42560.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 22194.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 11466.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 11401.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 10033.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 9541.0}, {'customer': 'Northwest Trends', 'revenue': 8961.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 8779.0}, {'customer': 'Leap Hospitality', 'revenue': 8551.0}, {'customer': 'Furniture Solutions Group', 'revenue': 8551.0}, {'customer': 'Patio & Home Direct', 'revenue': 7526.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 7409.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 6841.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 6786.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 5497.0}, {'customer': 'Direct Supply Inc.', 'revenue': 4902.0}, {'customer': 'Atmosphere Commercial Interiors', 'revenue': 4560.0}, {'customer': 'Robson Design Group', 'revenue': 4560.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 4560.0}, {'customer': 'Keca International', 'revenue': 4498.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 4012.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 3998.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 3762.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 3675.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 3234.0}, {'customer': 'Net Retailers LLC', 'revenue': 3009.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 2940.0}, {'customer': 'Patio Productions', 'revenue': 2769.0}, {'customer': 'Garden Architecture & Design', 'revenue': 2646.0}, {'customer': 'Image Urbaine', 'revenue': 2646.0}, {'customer': 'DGA Interiors', 'revenue': 2508.0}, {'customer': 'Hue Design LLC', 'revenue': 2508.0}, {'customer': 'MOI Inc.', 'revenue': 2508.0}, {'customer': 'AJ Designs', 'revenue': 2508.0}, {'customer': 'Touchmark, LLC', 'revenue': 2508.0}, {'customer': 'B H Allen Building Centre', 'revenue': 2505.0}, {'customer': 'Source', 'revenue': 2280.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 2280.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 2117.0}, {'customer': 'Patio Comfort', 'revenue': 1676.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1633.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1588.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 1459.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 1322.0}, {'customer': 'Lawai Beach Resort', 'revenue': 1254.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 1176.0}, {'customer': 'GST Interiors, LLC', 'revenue': 1140.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 1140.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1140.0}, {'customer': 'Jori Interiors', 'revenue': 1140.0}, {'customer': 'Commonwealth Design Group', 'revenue': 1140.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 1140.0}, {'customer': 'Country Furniture', 'revenue': 1058.0}, {'customer': "Bishop's Casual Living", 'revenue': 1058.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 1058.0}, {'customer': "Today's Patio", 'revenue': 1003.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 1002.0}, {'customer': 'Ifurnish Co.', 'revenue': 912.0}, {'customer': 'Main Street Furniture', 'revenue': 912.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 882.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 882.0}, {'customer': 'Abacus Furniture', 'revenue': 882.0}, {'customer': 'Sunset Home and Patio', 'revenue': 775.0}, {'customer': 'FirstService Residential-Austin', 'revenue': 627.0}, {'customer': 'Coombs Furniture', 'revenue': 588.0}, {'customer': 'Piscine Hippocampe', 'revenue': 588.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 529.0}, {'customer': 'Real Patio Living Llc', 'revenue': 502.0}, {'customer': 'Industrial Revolution', 'revenue': 500.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 500.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 441.0}, {'customer': 'Morinville Home Hardware', 'revenue': 441.0}, {'customer': 'Christy Sports, LLC', 'revenue': 274.0}, {'customer': 'Pangaea Patio', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}] | [{'item': 'FN54411OGY', 'desc': 'Lucia Dining Side Chair', 'available': 94}, {'item': 'FN54411ASG', 'desc': 'Lucia Dining Side Chair', 'available': 89}, {'item': 'FN54441OGY', 'desc': 'Lucia Bar Chair', 'available': 44}, {'item': 'FN54412OGY', 'desc': 'Lucia Dining Arm Chair', 'available': 43}, {'item': 'FN54453ASG-V', 'desc': 'Lucia Curved Corner', 'available': 31}, {'item': 'FN54402OGY', 'desc': 'Lucia Love Seat', 'available': 30}, {'item': 'FN54440OGY', 'desc': 'Lucia Counter Chair', 'available': 30}, {'item': 'FN54458PRL', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 29}, {'item': 'FN54453OGY-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 28}, {'item': 'FN54453OGY-V', 'desc': 'Lucia Curved Corner', 'available': 25}, {'item': 'FN54453ASG-R', 'desc': 'Lucia Wedge Right Arm', 'available': 25}, {'item': 'FN54452OGY-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 25}, {'item': 'FN54452OGY-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 25}, {'item': 'FN54404PRL', 'desc': 'Lucia Coffee Table', 'available': 24}, {'item': 'FN54453ASG-L', 'desc': 'Lucia Wedge Left Arm', 'available': 22}, {'item': 'FN54404ASG', 'desc': 'Lucia Coffee Table', 'available': 17}, {'item': 'FN54420OGY', 'desc': 'Lucia Lounger', 'available': 15}, {'item': 'FN54452ASG-C', 'desc': 'Lucia Wedge Corner', 'available': 14}, {'item': 'FN54416OGY', 'desc': 'Lucia Ottoman', 'available': 14}, {'item': 'FN54403PRL', 'desc': 'Lucia Sofa', 'available': 13}, {'item': 'FN54452ASG-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 12}, {'item': 'FN54452ASG-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 12}, {'item': 'FN54416ASG', 'desc': 'Lucia Ottoman', 'available': 12}, {'item': 'FN54458ASG', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 11}, {'item': 'FN54405PEY-OGY', 'desc': 'Lucia Sintered Stone End Table (KD)', 'available': 10}, {'item': 'FN54457ASG', 'desc': 'Lucia Sectional 40in Round Coffee Table/ottoman', 'available': 8}, {'item': 'FN54453ASG-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 8}, {'item': 'FN54468PRL', 'desc': 'Lucia Swivel Rocker', 'available': 6}, {'item': 'FN54404PEY-OGY', 'desc': 'Lucia Sintered Stone Coffee Table (KD)', 'available': 6}, {'item': 'FN54468OGY', 'desc': 'Lucia Swivel Rocker', 'available': 4}, {'item': 'FN54441ASG', 'desc': 'Lucia Bar Chair', 'available': 4}, {'item': 'FN54440ASG', 'desc': 'Lucia Counter Chair', 'available': 4}, {'item': 'FN54412ASG', 'desc': 'Lucia Dining Arm Chair', 'available': 4}, {'item': 'FN54405PRL', 'desc': 'Lucia End Table', 'available': 2}, {'item': 'FN54405ASG', 'desc': 'Lucia End Table', 'available': 1}] |
| UM00705BLK/C | 7.5' Fiberglass Umbrella,38mm 2 Poles W/canopy | COL73 | 281,054 | 889 | 95 | — | [{'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 21142.0}, {'customer': 'Hilton Supply MGM, LLC C/O The Gettys Group', 'revenue': 17662.0}, {'customer': 'Dalfen Sales Agency Inc', 'revenue': 14631.0}, {'customer': 'Carver & Associates', 'revenue': 11227.0}, {'customer': 'Hilton Supply Mgm. c/o HPD Hotel Procurement&Servi', 'revenue': 10036.0}, {'customer': 'Hilton Supply Management', 'revenue': 9100.0}, {'customer': 'Elite Contract Furniture Ltd', 'revenue': 8671.0}, {'customer': 'Dauntless Development', 'revenue': 8451.0}, {'customer': 'Hilton Supply Mgm LLC c/oInterMountain Renovations', 'revenue': 8420.0}, {'customer': 'Haylie Read Design, LLC', 'revenue': 7736.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 7605.0}, {'customer': "Les Plantes D'interieur Veronneau", 'revenue': 7239.0}, {'customer': 'Watermark Beach Resort', 'revenue': 5400.0}, {'customer': 'Adria International Inc', 'revenue': 5256.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 4753.0}, {'customer': 'The Vancouver Club', 'revenue': 4400.0}, {'customer': 'Synergy Design & Procurement LLC', 'revenue': 4125.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 4097.0}, {'customer': 'Evercare Contract Furnishings Inc.', 'revenue': 3673.0}, {'customer': 'Industrial Revolution', 'revenue': 3665.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 3430.0}, {'customer': 'Source', 'revenue': 3248.0}, {'customer': 'InnVest Hotels Limited', 'revenue': 3080.0}, {'customer': 'Fairmont Tremblant', 'revenue': 2695.0}, {'customer': 'Country Furniture', 'revenue': 2617.0}, {'customer': 'MBF Interior Design LLC', 'revenue': 2495.0}, {'customer': 'Redwood Construction', 'revenue': 2488.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 2448.0}, {'customer': 'The Interior Design Group Inc', 'revenue': 2400.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 2334.0}, {'customer': 'Walteriors Design LLC', 'revenue': 2183.0}, {'customer': 'Muse Design Inc', 'revenue': 2098.0}, {'customer': 'Broadmoor Golf Club', 'revenue': 1979.0}, {'customer': 'Northland Properties Corporation', 'revenue': 1955.0}, {'customer': 'The Westin Tampa Waterside', 'revenue': 1950.0}, {'customer': 'Keca International', 'revenue': 1904.0}, {'customer': 'His Chattanooga c/o The Stroud Group', 'revenue': 1871.0}, {'customer': 'Harbaugh Construction LLC', 'revenue': 1786.0}, {'customer': 'ACL Design Build Solutions', 'revenue': 1733.0}, {'customer': 'Pacific Arbour Seven Residences Ltd.', 'revenue': 1601.0}, {'customer': 'Bobby Design Inc.', 'revenue': 1600.0}, {'customer': 'FFE Solutions LLC', 'revenue': 1559.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 1559.0}, {'customer': 'GP Builders, Inc.', 'revenue': 1559.0}, {'customer': 'Summit Hotel Properties', 'revenue': 1555.0}, {'customer': 'Wawanesa Insurance', 'revenue': 1540.0}, {'customer': "Salty's Beach House", 'revenue': 1540.0}, {'customer': 'US Hospitality Group', 'revenue': 1503.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 1474.0}, {'customer': 'Zenn Investing', 'revenue': 1404.0}, {'customer': 'POI Business Interiors LP', 'revenue': 1280.0}, {'customer': 'GHG SB Goleta LLC c/o Project Dynamics Inc(agent)', 'revenue': 1247.0}, {'customer': 'Hampton Inn & Suites Hurricane WV', 'revenue': 1247.0}, {'customer': 'Hampton Inn & Suites Hemet CA', 'revenue': 1247.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 1247.0}, {'customer': 'National Hospitality Management', 'revenue': 1247.0}, {'customer': 'Hampton Inn Winston Salem NC c/o Carolina Hosp', 'revenue': 1247.0}, {'customer': 'Isidore Landscapes Inc.', 'revenue': 1155.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 1134.0}, {'customer': 'HI Cleveland II, LLC c/o The Stroud Group', 'revenue': 1134.0}, {'customer': 'Gatsby Apartments', 'revenue': 1131.0}, {'customer': 'Hilton Seattle Airport & Conference Center', 'revenue': 1053.0}, {'customer': 'Lux Hospitality & Senior Living', 'revenue': 1018.0}, {'customer': 'Marriott International, Inc.', 'revenue': 978.0}, {'customer': 'Image Business Interiors', 'revenue': 975.0}, {'customer': 'Carolina Hospitality Corp', 'revenue': 936.0}, {'customer': 'Carolina Hotel Investors Crabtree, LLC', 'revenue': 936.0}, {'customer': 'Opus Industries LLC', 'revenue': 936.0}, {'customer': 'Hampton Inn Suites-Roseburg OR c/o Dwelling(Agent)', 'revenue': 936.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 936.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 936.0}, {'customer': 'Property c/o Jerry Osborne & Asso, Inc.', 'revenue': 936.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 935.0}, {'customer': 'Metzger, Inc.', 'revenue': 851.0}, {'customer': '1000 100th Avenue L.P. (Lux Apartments)', 'revenue': 848.0}, {'customer': 'New Athens Creek', 'revenue': 800.0}, {'customer': 'Atmosphere Interiors', 'revenue': 770.0}, {'customer': 'AJ Designs', 'revenue': 672.0}, {'customer': 'Mckenzie Design LLC', 'revenue': 652.0}, {'customer': 'Sandman Signature Dallas Las Colinas Hotel &Suites', 'revenue': 652.0}, {'customer': 'Whistler & Blackcomb Mountain Resorts Ltd', 'revenue': 640.0}, {'customer': 'Schoolcraft Hospitality Llc', 'revenue': 624.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 624.0}, {'customer': 'Carbondale Hotels LLC', 'revenue': 624.0}, {'customer': 'ZMC Hotels, Llc', 'revenue': 624.0}, {'customer': 'Hampton Inn & Suites', 'revenue': 624.0}, {'customer': 'Brier Properties LLC', 'revenue': 624.0}, {'customer': 'Matteo Middletown Llc', 'revenue': 624.0}, {'customer': 'Olympia Equity Investors XIII, Llc c/o The Gettys', 'revenue': 624.0}, {'customer': 'M4 Orlando Llc c/o Beyer Brown (agent)', 'revenue': 624.0}, {'customer': 'Kernersville Hotels, LLC c/o Craver & Asso(agent)', 'revenue': 624.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 624.0}, {'customer': 'Western International c/o PMI L.P. (as agent)', 'revenue': 624.0}, {'customer': 'MHH Lenox 445 Operating, LLC C/O HPG International', 'revenue': 624.0}, {'customer': 'HC Kitsap, LLC', 'revenue': 624.0}, {'customer': 'Odyssey Propco VII, LLC c/o Aintree, LLC(agent)', 'revenue': 624.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 624.0}, {'customer': 'Spectrum Hospitality Management, LLC', 'revenue': 624.0}, {'customer': 'College Station Lodging Partners LP', 'revenue': 624.0}, {'customer': 'Furniture Solutions Group', 'revenue': 622.0}, {'customer': 'Spark Studio + Source LLC', 'revenue': 600.0}, {'customer': 'SAK Harbor LLC c/o Sourcing Advisors', 'revenue': 595.0}, {'customer': 'P&C Hotel LLC c/o ACC Design Inc(agent)', 'revenue': 567.0}, {'customer': 'D Hospitality Design LLC', 'revenue': 567.0}, {'customer': 'Town Creek Plaza', 'revenue': 567.0}, {'customer': 'AK Design Group, LLC', 'revenue': 567.0}, {'customer': 'Arveaux Interiors', 'revenue': 566.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 556.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 554.0}, {'customer': 'EPS7516 Bordeaux c/o Rancho Management', 'revenue': 385.0}, {'customer': 'Terra Verde', 'revenue': 340.0}, {'customer': 'Hampton Inn - Dyersburg, TN c/o Hersha Purchasing', 'revenue': 312.0}, {'customer': 'Champion Supply LLC', 'revenue': 312.0}, {'customer': 'Washington Hotels, LLC', 'revenue': 312.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 308.0}, {'customer': "Beck's Home & Heating", 'revenue': 308.0}, {'customer': 'Cash Account', 'revenue': 308.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 308.0}, {'customer': 'Snowhite Hospitality, LLC dba/Design Environments', 'revenue': 284.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 284.0}, {'customer': 'Laporte Hotel Suites, LLC dba/Hampton Inn', 'revenue': 284.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 284.0}, {'customer': 'FiveWest Interiors', 'revenue': 283.0}, {'customer': 'Club Piscines Sherbrooke', 'revenue': 160.0}, {'customer': 'ADS Hospitality LLC', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Hampton Inn & Suites Rocky Hill CT', 'revenue': 0.0}, {'customer': 'Northwest Trends', 'revenue': 0.0}, {'customer': 'Rama Tika Management LLC', 'revenue': 0.0}, {'customer': 'Curve Hospitality', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}, {'customer': 'Opportunity Lodging Three,LLC c/o Layman Hosp', 'revenue': 0.0}, {'customer': 'Era Living LLC', 'revenue': 0.0}, {'customer': 'Woodstock Hospitality Group', 'revenue': 0.0}, {'customer': 'Valiant Products Corportion', 'revenue': 0.0}, {'customer': 'Hampton Inn - Philadelphia Airport', 'revenue': 0.0}, {'customer': '3000 Vine LLC', 'revenue': 0.0}, {'customer': 'Home2 Suites Taylor', 'revenue': 0.0}, {'customer': "Anthony's Restaurants", 'revenue': 0.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 0.0}] | [{'item': 'UM01010SLV-CCL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Cloud canopy", 'available': 10}, {'item': 'UM01010SLV-CBL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Black canopy", 'available': 9}, {'item': 'UM01004SLV/C', 'desc': "10' Sq Deluxe Alum Umbrella, 48mm Pole W/canopy", 'available': 8}, {'item': 'UM00906BRZ/C', 'desc': "9' Alum W/fiber Ribs,crank Lift,collar Tilt,canopy", 'available': 6}, {'item': 'UM00909POLE-BRZ', 'desc': '45in Bar Bottom Pole for UM00906BRZ/C', 'available': 5}] |
| FN63020BLK | Toscana Lounger | COL110 | 269,492 | 647 | 37 | — | [{'customer': 'Studio Dwell', 'revenue': 26977.0}, {'customer': 'Haylie Read Design, LLC', 'revenue': 24902.0}, {'customer': 'Redwood Construction', 'revenue': 16435.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 14607.0}, {'customer': 'Carver & Associates', 'revenue': 12118.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 10559.0}, {'customer': 'Germain Lariviere (1970) Ltee.', 'revenue': 10295.0}, {'customer': 'Patio Options', 'revenue': 9131.0}, {'customer': 'Fairmont Tremblant', 'revenue': 7701.0}, {'customer': 'Sanctuary Home & Patio', 'revenue': 7668.0}, {'customer': 'Hilton Supply Management', 'revenue': 5935.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 5853.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 5633.0}, {'customer': "Hayward's Of Santa Barbara Inc.", 'revenue': 3851.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 3652.0}, {'customer': 'Zenn Investing', 'revenue': 3652.0}, {'customer': 'FFE Solutions LLC', 'revenue': 3652.0}, {'customer': 'GHG SB Goleta LLC c/o Project Dynamics Inc(agent)', 'revenue': 3652.0}, {'customer': 'Jennings Furniture & Design', 'revenue': 3520.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 3320.0}, {'customer': 'Bobby Design Inc.', 'revenue': 3300.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 3188.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2739.0}, {'customer': 'Opus Industries LLC', 'revenue': 2739.0}, {'customer': 'Hampton Inn & Suites Crawfordsville IN', 'revenue': 2739.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 2573.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 2490.0}, {'customer': 'D Hospitality Design LLC', 'revenue': 2490.0}, {'customer': 'Metzger, Inc.', 'revenue': 2490.0}, {'customer': 'Destiny Builders', 'revenue': 2490.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 2283.0}, {'customer': 'Northland Properties Corporation', 'revenue': 2200.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 2075.0}, {'customer': 'Southport Outdoor Living', 'revenue': 1980.0}, {'customer': 'Carbondale Hotels LLC', 'revenue': 1826.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 1826.0}, {'customer': 'R.R. Williams & Associates', 'revenue': 1826.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 1826.0}, {'customer': 'PSM Hospitality', 'revenue': 1826.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 1826.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 1826.0}, {'customer': 'Uniik Design Solutions', 'revenue': 1826.0}, {'customer': 'Oyen Flowers & Giftware', 'revenue': 1760.0}, {'customer': 'Meubles Duboise', 'revenue': 1672.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 1660.0}, {'customer': 'Magers Lodgings', 'revenue': 1660.0}, {'customer': 'Hospitality Designs', 'revenue': 1660.0}, {'customer': 'HCW', 'revenue': 1660.0}, {'customer': 'Lifestyles By Design, Llc.', 'revenue': 1660.0}, {'customer': 'Timmermans Landscaping', 'revenue': 1650.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1584.0}, {'customer': 'Garden Architecture & Design', 'revenue': 1489.0}, {'customer': 'Porch & Patio/casual Living', 'revenue': 1461.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 1408.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 1370.0}, {'customer': 'Muse Design Inc', 'revenue': 1370.0}, {'customer': 'Hampton Inn Bennington', 'revenue': 1370.0}, {'customer': 'Dunsire Asset Mgm USA Inc', 'revenue': 913.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 913.0}, {'customer': 'US Hospitality Group', 'revenue': 913.0}, {'customer': 'Mark Bombara Interior Design', 'revenue': 913.0}, {'customer': 'Meubles Poisson Ltée', 'revenue': 880.0}, {'customer': 'Robert Leduc', 'revenue': 880.0}, {'customer': 'Hotel Rehabs', 'revenue': 830.0}, {'customer': 'Billy Milner Design', 'revenue': 830.0}, {'customer': "S'tattic Design", 'revenue': 830.0}, {'customer': 'Country Furniture', 'revenue': 792.0}, {'customer': 'Decked Out Home & Patio', 'revenue': 792.0}, {'customer': 'OutBack Patio Furnishings', 'revenue': 621.0}, {'customer': 'Littman Bros Energy Supplies, Inc', 'revenue': 584.0}, {'customer': 'Entreprises H.P. Carignan Inc(mq034', 'revenue': 440.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 396.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 396.0}, {'customer': 'Club Piscines Sherbrooke', 'revenue': 220.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 219.0}, {'customer': 'Gooch Design Studio LLC', 'revenue': 199.0}, {'customer': 'Office Revolution LLC', 'revenue': 0.0}, {'customer': 'Elder And Ash, LLC', 'revenue': 0.0}, {'customer': 'Level 3 Design Group', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Polygon Interior Design Ltd.', 'revenue': 0.0}, {'customer': 'Hampton Inn & Suites Ada OK', 'revenue': 0.0}, {'customer': 'Hampton Inn & Suites Rocky Hill CT', 'revenue': 0.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 0.0}] | [{'item': 'FN63005BLK', 'desc': 'Toscana Side Table', 'available': 57}, {'item': 'FN63005GRY', 'desc': 'Toscana Side Table', 'available': 55}, {'item': 'FN63005WHT', 'desc': 'Toscana Side Table', 'available': 39}, {'item': 'FN63020GRY', 'desc': 'Toscana Lounger', 'available': 39}, {'item': 'FN63020WHT', 'desc': 'Toscana Lounger', 'available': 27}] |
| FN61385LAG | Poinciana Highback Chair | COL82 | 215,990 | 314 | 47 | — | [{'customer': 'Hilton Supply Management', 'revenue': 19272.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 17955.0}, {'customer': 'RLJ HS Seattle Lynnwood, LLC', 'revenue': 13300.0}, {'customer': 'Granite State Contract Furnishings', 'revenue': 9510.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 8778.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 8512.0}, {'customer': 'Creo Hospitality LLC', 'revenue': 8246.0}, {'customer': 'Christina River Exchange', 'revenue': 7229.0}, {'customer': 'Carver & Associates', 'revenue': 6916.0}, {'customer': 'PHG Jackson II, LLC c/o Carver & Asso (Atlanta)', 'revenue': 6650.0}, {'customer': 'Curve Hospitality', 'revenue': 5852.0}, {'customer': 'Studio Dwell', 'revenue': 5852.0}, {'customer': 'Homewood Suites By Hilton Covington', 'revenue': 5852.0}, {'customer': 'West Coast Lodging c/o Throughline by IIG (agent)', 'revenue': 5320.0}, {'customer': 'Country Furniture', 'revenue': 5299.0}, {'customer': 'Tharaldson Hospitality Development, LLC', 'revenue': 5121.0}, {'customer': 'Picerne Development Corp', 'revenue': 3990.0}, {'customer': 'Homewood Suites Orlando Airport', 'revenue': 3990.0}, {'customer': 'Renascent Hospitality', 'revenue': 3189.0}, {'customer': 'BPR Goldsboro, LLC c/o Carver and Asso(Atlanta)', 'revenue': 2926.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 2926.0}, {'customer': 'Farrell Flynne LLC', 'revenue': 2926.0}, {'customer': 'Sourcing Advisors LLC c/o Sourcing Advisor', 'revenue': 2926.0}, {'customer': 'LOF2 Tyler Golden TRS, LLC c/o DeBlauw Purchasing', 'revenue': 2926.0}, {'customer': 'Parks Hospitality Group', 'revenue': 2926.0}, {'customer': 'B&T Arizona Hotels III, LLC c/o PMI', 'revenue': 2926.0}, {'customer': 'Lajoie Purchasing Associates', 'revenue': 2926.0}, {'customer': 'MCR Allen Tenant, LLC c/o Onyx Contract SVC', 'revenue': 2926.0}, {'customer': 'Hospitality Depot', 'revenue': 2660.0}, {'customer': 'Larkin Family Properties Inc c/o Benjamin West', 'revenue': 2660.0}, {'customer': 'Marriott International, Inc.', 'revenue': 2660.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 2660.0}, {'customer': 'Buffalo-Alafaya Asso. LLC dba Homewood Suites', 'revenue': 2660.0}, {'customer': 'Dwellings, Llc', 'revenue': 2660.0}, {'customer': 'HSI Design Group', 'revenue': 2660.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2660.0}, {'customer': 'Eastwood Hospitality Group Llc', 'revenue': 1463.0}, {'customer': 'Zachary Park Hotel QOZB c/o Benjamin West(agent)', 'revenue': 1463.0}, {'customer': 'Lita Dirks & Co, Llc', 'revenue': 1463.0}, {'customer': 'Design and Construction, Llc c/o The Gettys Group', 'revenue': 1463.0}, {'customer': 'TPI Hospitality', 'revenue': 1463.0}, {'customer': 'Metzger, Inc.', 'revenue': 1463.0}, {'customer': 'Homewood Suites By Hilton Boston', 'revenue': 1463.0}, {'customer': 'IBee Design Studio LLC', 'revenue': 1330.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 1330.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1170.0}, {'customer': 'Jack Wills Companies', 'revenue': 1064.0}, {'customer': 'Studio 4d', 'revenue': 665.0}, {'customer': 'Can-Tario Brick & Stone', 'revenue': 626.0}, {'customer': 'Whitney Evans Ltd', 'revenue': 585.0}, {'customer': 'Creative Living', 'revenue': 532.0}, {'customer': 'Tru Contract Interiors', 'revenue': 0.0}, {'customer': 'Summit Hotel Properties', 'revenue': 0.0}, {'customer': 'Homewood Suites-Liverpool, NY c/o HPD(as agent)', 'revenue': 0.0}, {'customer': 'BPR Properties c/o Carver and Asso, Atlanta(agent)', 'revenue': 0.0}, {'customer': 'JSM Procurement LLC', 'revenue': 0.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 0.0}] | [{'item': 'FN61312LAG', 'desc': 'Poinciana Dining Arm Chair', 'available': 199}, {'item': 'FN61311LAG', 'desc': 'Poinciana Dining Side Chair', 'available': 160}, {'item': 'FN61353LAG-C', 'desc': 'Poinciana Chair (w/o Arm)', 'available': 72}, {'item': 'FN61352LAG-R', 'desc': 'Poinciana 2-Seater Right Arm', 'available': 57}, {'item': 'FN61353LAG-V', 'desc': 'Poinciana Curved Corner', 'available': 55}, {'item': 'FN61352LAG-L', 'desc': 'Poinciana 2-Seater Left Arm', 'available': 52}, {'item': 'FN61301LAG', 'desc': 'Poinciana Club Chair', 'available': 44}, {'item': 'FN61341LAG', 'desc': 'Poinciana Bar Chair', 'available': 23}, {'item': 'FN61368LAG', 'desc': 'Poinciana Swivel Rocker', 'available': 22}, {'item': 'FN61316ASG', 'desc': 'Poinciana Ottoman', 'available': 14}, {'item': 'FN61303LAG', 'desc': 'Poinciana Sofa', 'available': 14}, {'item': 'FN61304ASG', 'desc': 'Poinciana Coffee Table', 'available': 11}, {'item': 'FN61340LAG', 'desc': 'Poinciana Counter Chair', 'available': 10}, {'item': 'FN61305ASG', 'desc': 'Poinciana End Table', 'available': 5}] |
| UM00605-55 | Umbrella Base, Steel, Square, 120lbs | COL197 | 209,535 | 407 | 21 | 2026-6-5 | [{'customer': 'Hilton Supply MGM, LLC C/O The Gettys Group', 'revenue': 28435.0}, {'customer': 'Carver & Associates', 'revenue': 18025.0}, {'customer': 'Hilton Supply Mgm. c/o HPD Hotel Procurement&Servi', 'revenue': 13013.0}, {'customer': 'Hilton Supply Management', 'revenue': 11663.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 6992.0}, {'customer': 'Hilton Supply Mgm LLC c/oInterMountain Renovations', 'revenue': 6651.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 5832.0}, {'customer': 'Era Living LLC', 'revenue': 5049.0}, {'customer': 'Interior Solutions', 'revenue': 4488.0}, {'customer': 'Synergy Design & Procurement LLC', 'revenue': 4065.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 3968.0}, {'customer': 'Hampton Inn Phoenix/Anthem', 'revenue': 3856.0}, {'customer': 'Walteriors Design LLC', 'revenue': 3711.0}, {'customer': 'Muse Design Inc', 'revenue': 3566.0}, {'customer': 'PHG Ashburn LLC', 'revenue': 3181.0}, {'customer': 'His Chattanooga c/o The Stroud Group', 'revenue': 3181.0}, {'customer': 'Urban Design Studio', 'revenue': 3060.0}, {'customer': 'Harbaugh Construction LLC', 'revenue': 3036.0}, {'customer': 'FFE Solutions LLC', 'revenue': 2651.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2651.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 2651.0}, {'customer': 'US Hospitality Group', 'revenue': 2554.0}, {'customer': 'Bobby Design Inc.', 'revenue': 2520.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 2506.0}, {'customer': 'GHG SB Goleta LLC c/o Project Dynamics Inc(agent)', 'revenue': 2121.0}, {'customer': 'National Hospitality Management', 'revenue': 2121.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 2121.0}, {'customer': 'Hampton Inn Winston Salem NC c/o Carolina Hosp', 'revenue': 2121.0}, {'customer': "Leadon (St. John's) Operations LP", 'revenue': 2016.0}, {'customer': 'HI Cleveland II, LLC c/o The Stroud Group', 'revenue': 1928.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 1928.0}, {'customer': 'The Vancouver Club', 'revenue': 1890.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1683.0}, {'customer': 'Hampton Inn Suites-Roseburg OR c/o Dwelling(Agent)', 'revenue': 1590.0}, {'customer': 'Opus Industries LLC', 'revenue': 1590.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 1590.0}, {'customer': 'Hampton Inn & Suites Hurricane WV', 'revenue': 1590.0}, {'customer': 'Property c/o Jerry Osborne & Asso, Inc.', 'revenue': 1590.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 1590.0}, {'customer': 'Carolina Hospitality Corp', 'revenue': 1590.0}, {'customer': 'Metzger, Inc.', 'revenue': 1446.0}, {'customer': 'Atmosphere Interiors', 'revenue': 1260.0}, {'customer': 'College Station Lodging Partners LP', 'revenue': 1060.0}, {'customer': 'Hampton Inn & Suites', 'revenue': 1060.0}, {'customer': 'Brier Properties LLC', 'revenue': 1060.0}, {'customer': 'Matteo Middletown Llc', 'revenue': 1060.0}, {'customer': 'ZMC Hotels, Llc', 'revenue': 1060.0}, {'customer': 'M4 Orlando Llc c/o Beyer Brown (agent)', 'revenue': 1060.0}, {'customer': 'Town Creek Plaza', 'revenue': 1060.0}, {'customer': 'Olympia Equity Investors XIII, Llc c/o The Gettys', 'revenue': 1060.0}, {'customer': 'Kernersville Hotels, LLC c/o Craver & Asso(agent)', 'revenue': 1060.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 1060.0}, {'customer': 'AK Design Group, LLC', 'revenue': 1060.0}, {'customer': 'MHH Lenox 445 Operating, LLC C/O HPG International', 'revenue': 1060.0}, {'customer': 'Odyssey Propco VII, LLC c/o Aintree, LLC(agent)', 'revenue': 1060.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 1060.0}, {'customer': 'HC Kitsap, LLC', 'revenue': 1060.0}, {'customer': 'Spectrum Hospitality Management, LLC', 'revenue': 1060.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 1060.0}, {'customer': 'Schoolcraft Hospitality Llc', 'revenue': 1060.0}, {'customer': 'Carbondale Hotels LLC', 'revenue': 1060.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 1020.0}, {'customer': 'Dauntless Development', 'revenue': 1020.0}, {'customer': 'D Hospitality Design LLC', 'revenue': 964.0}, {'customer': 'P&C Hotel LLC c/o ACC Design Inc(agent)', 'revenue': 964.0}, {'customer': 'Spark Studio + Source LLC', 'revenue': 964.0}, {'customer': 'Insideout Home & Patio (Burlington)', 'revenue': 807.0}, {'customer': 'Hampton Inn - Dyersburg, TN c/o Hersha Purchasing', 'revenue': 530.0}, {'customer': 'Washington Hotels, LLC', 'revenue': 530.0}, {'customer': 'Laporte Hotel Suites, LLC dba/Hampton Inn', 'revenue': 530.0}, {'customer': 'Champion Supply LLC', 'revenue': 530.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 482.0}, {'customer': 'SAK Harbor LLC c/o Sourcing Advisors', 'revenue': 482.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 482.0}, {'customer': 'Snowhite Hospitality, LLC dba/Design Environments', 'revenue': 482.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 269.0}, {'customer': 'Dynamik Interiors', 'revenue': 269.0}, {'customer': 'Opportunity Lodging Three,LLC c/o Layman Hosp', 'revenue': 0.0}, {'customer': 'Valiant Products Corportion', 'revenue': 0.0}, {'customer': 'Woodstock Hospitality Group', 'revenue': 0.0}, {'customer': 'Northwest Trends', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 0.0}, {'customer': 'Rama Tika Management LLC', 'revenue': 0.0}, {'customer': 'Hampton Inn - Philadelphia Airport', 'revenue': 0.0}, {'customer': 'ADS Hospitality LLC', 'revenue': 0.0}, {'customer': 'Curve Hospitality', 'revenue': 0.0}] | [{'item': 'UM00606BRZ', 'desc': 'Umbrella Base W Dual Purpose Stem, Cast Iron,50lbs', 'available': 56}, {'item': 'UM00606ADD-ON', 'desc': 'Umbrella Base Add-on Weight, Cast Iron, 30lbs', 'available': 32}, {'item': 'UM00609BLK', 'desc': 'Umbrella Base w/Casters, Steel, 120lbs', 'available': 16}, {'item': 'UM00605-32', 'desc': 'Umbrella Base W Dual Purpose Stem, Steel, 70lbs', 'available': 13}, {'item': 'UM00610SGR', 'desc': 'Base for UM01010, Galvan. Steel w/ Lid, 415lbs', 'available': 9}, {'item': 'UM00612', 'desc': 'In-Ground Mount Kit for UM01010', 'available': 5}, {'item': 'UM00611', 'desc': 'Concrete Mount Kit for UM01010', 'available': 4}] |
| CU54401 | Lucia Club Chair Cushion | COL203 | 184,283 | 957 | 77 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 16892.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 8091.0}, {'customer': 'City of Yorba Linda', 'revenue': 7549.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 7350.0}, {'customer': 'Wegman Design Group', 'revenue': 6935.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 5455.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 5267.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 5100.0}, {'customer': 'Lanai Resorts LLC dba Pulama Lanai', 'revenue': 5100.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 4900.0}, {'customer': 'IDM Development, LLC', 'revenue': 4480.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 4440.0}, {'customer': 'Northwest Trends', 'revenue': 3900.0}, {'customer': 'Leap Hospitality', 'revenue': 3825.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 3593.0}, {'customer': 'Furniture Solutions Group', 'revenue': 3526.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 3368.0}, {'customer': 'Country Furniture', 'revenue': 3125.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 2851.0}, {'customer': 'Keca International', 'revenue': 2634.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 2619.0}, {'customer': 'Patio & Home Direct', 'revenue': 2608.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 2520.0}, {'customer': 'Bobby Design Inc.', 'revenue': 2384.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 2360.0}, {'customer': 'DGA Interiors', 'revenue': 2259.0}, {'customer': 'Touchmark, LLC', 'revenue': 2157.0}, {'customer': 'Direct Supply Inc.', 'revenue': 1940.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 1913.0}, {'customer': 'Atmosphere Commercial Interiors', 'revenue': 1840.0}, {'customer': 'Christy Sports, LLC', 'revenue': 1754.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1679.0}, {'customer': '1000 100th Avenue L.P. (Lux Apartments)', 'revenue': 1610.0}, {'customer': 'AJ Designs', 'revenue': 1598.0}, {'customer': 'The Childs Dreyfus Group', 'revenue': 1557.0}, {'customer': 'Real Patio Living Llc', 'revenue': 1456.0}, {'customer': 'B H Allen Building Centre', 'revenue': 1445.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 1411.0}, {'customer': 'Robson Design Group', 'revenue': 1240.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 1130.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 1107.0}, {'customer': 'Net Retailers LLC', 'revenue': 1103.0}, {'customer': 'We are Sparrow Studio', 'revenue': 1098.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1056.0}, {'customer': 'Studio Dwell', 'revenue': 1049.0}, {'customer': 'Design Collaborative, Inc.', 'revenue': 1020.0}, {'customer': 'Pabor Designs Purchasing Service Inc.', 'revenue': 1020.0}, {'customer': 'MOI Inc.', 'revenue': 1020.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 973.0}, {'customer': 'Hue Design LLC', 'revenue': 920.0}, {'customer': 'Source', 'revenue': 920.0}, {'customer': "Today's Patio", 'revenue': 892.0}, {'customer': 'Image Urbaine', 'revenue': 880.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 878.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 858.0}, {'customer': 'Patio Productions', 'revenue': 816.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 778.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 778.0}, {'customer': 'CMS Commercial Furniture', 'revenue': 755.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 731.0}, {'customer': 'Patio Comfort', 'revenue': 725.0}, {'customer': 'Garden Architecture & Design', 'revenue': 635.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 620.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 590.0}, {'customer': 'Lawai Beach Resort', 'revenue': 589.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 579.0}, {'customer': 'Model Home Interiors Inc', 'revenue': 576.0}, {'customer': 'Sonoma Backyard', 'revenue': 541.0}, {'customer': 'Piscine Hippocampe', 'revenue': 535.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 525.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 518.0}, {'customer': 'Zachary Park Hotel QOZB c/o Benjamin West(agent)', 'revenue': 510.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 497.0}, {'customer': 'InnVest Hotels Limited', 'revenue': 477.0}, {'customer': 'Office Revolution LLC', 'revenue': 460.0}, {'customer': 'Bridget Bohacz & Associates Inc', 'revenue': 460.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 460.0}, {'customer': 'Jori Interiors', 'revenue': 460.0}, {'customer': "Bishop's Casual Living", 'revenue': 435.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 420.0}, {'customer': 'GST Interiors, LLC', 'revenue': 415.0}, {'customer': 'Commonwealth Design Group', 'revenue': 410.0}, {'customer': 'Office Concepts Ltd', 'revenue': 389.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 360.0}, {'customer': '4C Group', 'revenue': 360.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 351.0}, {'customer': "Mio's Furniture Fashions", 'revenue': 331.0}, {'customer': 'Main Street Furniture', 'revenue': 328.0}, {'customer': 'Ifurnish Co.', 'revenue': 328.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 328.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 324.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 316.0}, {'customer': 'Sunset Home and Patio', 'revenue': 313.0}, {'customer': 'Veranda Home & Garden Collection', 'revenue': 313.0}, {'customer': 'Aqua Fire Leisure', 'revenue': 311.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 294.0}, {'customer': "Sherri's Living Large", 'revenue': 280.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 259.0}, {'customer': 'D.L. Shury Developments Ltd', 'revenue': 258.0}, {'customer': 'Abacus Furniture', 'revenue': 256.0}, {'customer': 'The Design Resource Group, Inc.', 'revenue': 245.0}, {'customer': 'Beachcomber Hot Tubs & Outdoor Living', 'revenue': 245.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 196.0}, {'customer': 'Coombs Furniture', 'revenue': 184.0}, {'customer': 'Farris Design Studio', 'revenue': 173.0}, {'customer': 'Canadian Home Leisure', 'revenue': 166.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 164.0}, {'customer': 'Emigh Ace Hardware', 'revenue': 156.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 156.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 156.0}, {'customer': 'Crystalview', 'revenue': 147.0}, {'customer': 'Rattan Wicker & Cane', 'revenue': 144.0}, {'customer': 'Industrial Revolution', 'revenue': 122.0}, {'customer': 'Morinville Home Hardware', 'revenue': 117.0}, {'customer': 'All Backyard Fun', 'revenue': 69.0}, {'customer': 'FirstService Residential-Austin', 'revenue': 62.0}, {'customer': 'Georgia Patio Inc', 'revenue': 53.0}, {'customer': 'Elders Ace', 'revenue': 53.0}, {'customer': "Schneiderman's Furniture, Inc.", 'revenue': 26.0}, {'customer': 'Americasmart Real Estate LLC', 'revenue': 0.0}, {'customer': 'Pangaea Patio', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}, {'customer': 'Drew Ruesch Interiors', 'revenue': 0.0}] | [{'item': 'CU54458', 'desc': 'Lucia Swivel Rocking Arm Chair Cushion (w/button)', 'available': 2}] |
| CU55001 | Copacabana Club Chair Cushion | COL204 | 178,063 | 772 | 83 | — | [{'customer': 'Country Furniture', 'revenue': 8880.0}, {'customer': 'Hilton Supply Management', 'revenue': 7800.0}, {'customer': 'HPD Hotel Procurement & Design Services', 'revenue': 4680.0}, {'customer': 'US Hospitality Group', 'revenue': 4680.0}, {'customer': 'Elland Property Development Limited', 'revenue': 4160.0}, {'customer': 'Into The Garden, Inc.', 'revenue': 4043.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 3900.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 3888.0}, {'customer': '1001 Canal LLC', 'revenue': 3720.0}, {'customer': 'Carver & Associates', 'revenue': 3640.0}, {'customer': 'PCH Hotels & Resort-Shoals c/oPurchasing Dimension', 'revenue': 3380.0}, {'customer': 'Net Retailers LLC', 'revenue': 3360.0}, {'customer': 'Blu Salmon, LLC', 'revenue': 3290.0}, {'customer': 'Muse Design Inc', 'revenue': 3120.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 3085.0}, {'customer': 'Brier Properties LLC', 'revenue': 2600.0}, {'customer': 'Kristin Martin Design', 'revenue': 2473.0}, {'customer': 'Carolina Hotel Investors Crabtree, LLC', 'revenue': 2414.0}, {'customer': 'Touchmark c/o Source', 'revenue': 2413.0}, {'customer': "Bishop's Casual Living", 'revenue': 2297.0}, {'customer': 'Furniture Solutions Group', 'revenue': 2280.0}, {'customer': 'Zachary Park Hotel QOZB c/o Benjamin West(agent)', 'revenue': 2280.0}, {'customer': 'Littman Bros Energy Supplies, Inc', 'revenue': 2106.0}, {'customer': 'Roadrunner Furnishings', 'revenue': 2080.0}, {'customer': 'River Ridge Renovations LLC', 'revenue': 2080.0}, {'customer': 'Hampton Inn Detroit/Southgate', 'revenue': 2080.0}, {'customer': 'GP Builders, Inc.', 'revenue': 2080.0}, {'customer': 'Keaton Interiors', 'revenue': 1960.0}, {'customer': 'Tarrison Products Ltd.', 'revenue': 1880.0}, {'customer': 'CIM Group c/o The Stroud Group', 'revenue': 1880.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 1863.0}, {'customer': 'B2 Design Co.', 'revenue': 1830.0}, {'customer': 'The Thrash Group c/o J Desterbecq & Associates', 'revenue': 1744.0}, {'customer': 'Thiel and Thiel, Inc', 'revenue': 1680.0}, {'customer': 'Patio & Home Direct', 'revenue': 1666.0}, {'customer': 'His Chattanooga c/o The Stroud Group', 'revenue': 1560.0}, {'customer': 'RK Hospitality Design', 'revenue': 1560.0}, {'customer': 'EAS Investment Enterprises Inc.', 'revenue': 1560.0}, {'customer': 'Hampton Inn & Suites Knightdale', 'revenue': 1560.0}, {'customer': 'Complete Office LLC', 'revenue': 1560.0}, {'customer': 'ZMC Hotels, Llc', 'revenue': 1560.0}, {'customer': 'Streetlights Residential', 'revenue': 1410.0}, {'customer': 'Trio, Inc.', 'revenue': 1307.0}, {'customer': 'Urban Shore Interior Design', 'revenue': 1182.0}, {'customer': 'One World Design Source', 'revenue': 1140.0}, {'customer': 'One10', 'revenue': 1140.0}, {'customer': 'Fourth Avenue Seattle Hotel LLC dba/Kimpton Monaco', 'revenue': 1107.0}, {'customer': 'Zenn Investing', 'revenue': 1082.0}, {'customer': 'Hampton Inn Suites-Roseburg OR c/o Dwelling(Agent)', 'revenue': 1040.0}, {'customer': 'JPH Procurement', 'revenue': 1040.0}, {'customer': 'Curve Hospitality', 'revenue': 1040.0}, {'customer': 'Stone Ridge Hospitality', 'revenue': 1040.0}, {'customer': 'Destiny Builders', 'revenue': 1040.0}, {'customer': 'Metzger, Inc.', 'revenue': 1040.0}, {'customer': 'HIS Hamilton Place c/o The Stroud Group', 'revenue': 1040.0}, {'customer': 'Property c/o Jerry Osborne & Asso, Inc.', 'revenue': 1040.0}, {'customer': 'Distinctive Hospitality Designs, LLC', 'revenue': 1040.0}, {'customer': 'Uniik Design Solutions', 'revenue': 1040.0}, {'customer': 'Hampton Inn Danville, KY', 'revenue': 1040.0}, {'customer': 'Pinnacle South LLC', 'revenue': 1040.0}, {'customer': 'Model Home Interiors Inc', 'revenue': 1008.0}, {'customer': 'Williams Olander Interior Design', 'revenue': 1007.0}, {'customer': 'Sunset Home and Patio', 'revenue': 984.0}, {'customer': 'The Childs Dreyfus Group', 'revenue': 982.0}, {'customer': 'Wegman Design Group', 'revenue': 940.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 914.0}, {'customer': 'Zauner Manhattan Design', 'revenue': 907.0}, {'customer': "Today's Patio", 'revenue': 885.0}, {'customer': 'Starland Property Co, LLC', 'revenue': 885.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 848.0}, {'customer': 'Le Reve Design & Associates', 'revenue': 840.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 835.0}, {'customer': 'Dexter Hotel Group LLC c/o First Call Hosp(agent)', 'revenue': 780.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 692.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 672.0}, {'customer': 'CO-OP At Home', 'revenue': 634.0}, {'customer': 'J. Davenport Associates', 'revenue': 553.0}, {'customer': 'Patio Productions', 'revenue': 526.0}, {'customer': 'Source', 'revenue': 520.0}, {'customer': 'Hampton Inn Phoenix/Anthem', 'revenue': 520.0}, {'customer': 'Hilton Garden Inn - Las Vegas Strip South', 'revenue': 520.0}, {'customer': 'Hampton Inn & Suites Hemet CA', 'revenue': 520.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 520.0}, {'customer': 'Olympia Equity Investors XIII, Llc c/o The Gettys', 'revenue': 520.0}, {'customer': 'Hotel Rehabs', 'revenue': 520.0}, {'customer': 'Patten Purchasing, LLC', 'revenue': 520.0}, {'customer': 'Harbaugh Construction LLC', 'revenue': 520.0}, {'customer': 'Town Creek Plaza', 'revenue': 520.0}, {'customer': 'Laporte Hotel Suites, LLC dba/Hampton Inn', 'revenue': 520.0}, {'customer': 'Schoolcraft Hospitality Llc', 'revenue': 520.0}, {'customer': 'Chelsea Hospitality Group', 'revenue': 520.0}, {'customer': 'Hampton Inn - Dyersburg, TN c/o Hersha Purchasing', 'revenue': 520.0}, {'customer': 'HI Cleveland II, LLC c/o The Stroud Group', 'revenue': 520.0}, {'customer': 'HC Kitsap, LLC', 'revenue': 520.0}, {'customer': 'SAK Harbor LLC c/o Sourcing Advisors', 'revenue': 520.0}, {'customer': 'Hampton Inn Waynesburg c/o Too Tall Trading Post', 'revenue': 520.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 520.0}, {'customer': 'Kernersville Hotels, LLC c/o Craver & Asso(agent)', 'revenue': 520.0}, {'customer': 'Dalfen Sales Agency Inc', 'revenue': 520.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 520.0}, {'customer': 'FFE Solutions LLC', 'revenue': 520.0}, {'customer': 'Design Environments', 'revenue': 520.0}, {'customer': 'Odyssey Propco VII, LLC c/o Aintree, LLC(agent)', 'revenue': 520.0}, {'customer': 'Wichita Falls Lodging, LP', 'revenue': 520.0}, {'customer': 'Walteriors Design LLC', 'revenue': 520.0}, {'customer': 'Pam Ellis & Associates, Inc.', 'revenue': 520.0}, {'customer': 'P&C Hotel LLC c/o ACC Design Inc(agent)', 'revenue': 520.0}, {'customer': 'Champion Supply LLC', 'revenue': 520.0}, {'customer': 'Hampton Inn & Suites Swansboro, NC', 'revenue': 520.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 508.0}, {'customer': 'Workshop Studio', 'revenue': 503.0}, {'customer': 'Reusch Interior Design', 'revenue': 503.0}, {'customer': 'GC Waikiki Hotel OpCo LLC c/o Level 3 Design Group', 'revenue': 500.0}, {'customer': 'Morinville Home Hardware', 'revenue': 489.0}, {'customer': 'Catalyst Interiors Inc.', 'revenue': 470.0}, {'customer': 'California Contract & Home Inc', 'revenue': 470.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 432.0}, {'customer': 'Tarson Supply Corp.', 'revenue': 416.0}, {'customer': 'Coombs Furniture', 'revenue': 403.0}, {'customer': 'Shop the Studio at Design Mart', 'revenue': 376.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 376.0}, {'customer': 'Forest Glade Fireplaces', 'revenue': 376.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 376.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 363.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 342.0}, {'customer': 'Luxe Furniture Company', 'revenue': 327.0}, {'customer': 'Paradise Pools (Enterprises) Ltd', 'revenue': 305.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 269.0}, {'customer': 'Spark Studio + Source LLC', 'revenue': 260.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 260.0}, {'customer': 'Terra Verde', 'revenue': 188.0}, {'customer': 'Parco Piscines & Spas Ltee (mq018)', 'revenue': 188.0}, {'customer': 'Piscine Hippocampe', 'revenue': 188.0}, {'customer': 'Centre Massicotte Inc.', 'revenue': 179.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 163.0}, {'customer': 'Hospitality Media Group LLC', 'revenue': 151.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 150.0}, {'customer': 'Hampton Inn Greenville, NC c/o Linked Hospitality', 'revenue': 0.0}, {'customer': 'Valiant Products Corportion', 'revenue': 0.0}, {'customer': 'Hampton Inn Camden c/o Linked Hospitality (Agent)', 'revenue': 0.0}, {'customer': 'Hampton Inn Edenton', 'revenue': 0.0}, {'customer': 'Level 3 Design Group', 'revenue': 0.0}, {'customer': 'Pangaea Patio', 'revenue': 0.0}, {'customer': 'Tharaldson Hospitality Development, LLC', 'revenue': 0.0}, {'customer': 'Polygon Interior Design Ltd.', 'revenue': 0.0}, {'customer': 'Hampton Inn Suites-Redmond, WA c/o Dwellings', 'revenue': 0.0}, {'customer': 'Rama Tika Management LLC', 'revenue': 0.0}, {'customer': 'ADS Hospitality LLC', 'revenue': 0.0}, {'customer': 'Legacy Hotels c/o Carver and Asso, Atlanta (agent)', 'revenue': 0.0}, {'customer': 'NSK Design Group', 'revenue': 0.0}] | — |
| FN61788WTR | Biltmore Swivel Recliner | COL87 | 174,052 | 196 | 0 | — | [{'customer': 'Offenbachers Home Escapes', 'revenue': 11339.0}, {'customer': 'Sunnyland Furniture', 'revenue': 9601.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 8128.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 7487.0}, {'customer': 'Patio Style', 'revenue': 6694.0}, {'customer': 'ZLM Enterprises', 'revenue': 6499.0}, {'customer': 'Sequoia Outback', 'revenue': 6477.0}, {'customer': 'Stauffers of Kissel Hill', 'revenue': 6213.0}, {'customer': 'Into The Garden, Inc.', 'revenue': 5801.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 5680.0}, {'customer': 'OutBack Patio Furnishings', 'revenue': 5099.0}, {'customer': 'Busch Fireplace', 'revenue': 4824.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 4416.0}, {'customer': 'Club Piscines Granby', 'revenue': 4352.0}, {'customer': 'Furniture Source International', 'revenue': 4100.0}, {'customer': 'Luxe Furniture Company', 'revenue': 4097.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 4001.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 3840.0}, {'customer': 'Georgia Patio Inc', 'revenue': 3730.0}, {'customer': 'Opdyke Furniture Inc', 'revenue': 3728.0}, {'customer': 'Greater Southern Home Recreation', 'revenue': 3400.0}, {'customer': 'High End Patio Furniture', 'revenue': 3400.0}, {'customer': 'Treescapes - The Outdoor Living Center', 'revenue': 3300.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 3010.0}, {'customer': 'Patio Productions', 'revenue': 2900.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 2880.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 2640.0}, {'customer': "Al's Garden Center& Greenhouses, LLC", 'revenue': 2200.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 2200.0}, {'customer': 'Hollywood Pool & Spa, Inc.', 'revenue': 2000.0}, {'customer': 'Beaver Bark & Rock', 'revenue': 2000.0}, {'customer': 'Veranda Home & Garden Collection', 'revenue': 1920.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 1920.0}, {'customer': 'Littman Bros Energy Supplies, Inc', 'revenue': 1862.0}, {'customer': 'The Collective Outdoors', 'revenue': 1840.0}, {'customer': 'Corner Collection', 'revenue': 1720.0}, {'customer': 'Custom Fireplace Patio and BBQ', 'revenue': 1700.0}, {'customer': "Bowman's Stove & Patio Inc.", 'revenue': 1600.0}, {'customer': 'Watsons Fire Place & Patio', 'revenue': 1600.0}, {'customer': 'Woodburners, Inc.', 'revenue': 1600.0}, {'customer': 'Sunshine Nursery + Greenhouse', 'revenue': 1280.0}, {'customer': 'Hive Design LLC', 'revenue': 1250.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 1152.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1152.0}, {'customer': 'Elegant Outdoor Living', 'revenue': 1000.0}, {'customer': 'Philadelphia Botanical Products', 'revenue': 1000.0}, {'customer': 'Camrose Home Hardware and Building Center', 'revenue': 960.0}, {'customer': 'East Texas Brick', 'revenue': 920.0}, {'customer': 'Spas of Colorado, Inc', 'revenue': 850.0}, {'customer': 'Daylight Home & Gardens', 'revenue': 850.0}, {'customer': 'Arkansas Furniture', 'revenue': 850.0}, {'customer': 'All Seasons Living', 'revenue': 495.0}, {'customer': 'Home And Patio', 'revenue': 495.0}] | [{'item': 'FN61711WTR', 'desc': 'Biltmore Dining Side Chair', 'available': 52}, {'item': 'FN61711PEW-OGY', 'desc': 'Biltmore Dining Side Chair', 'available': 38}, {'item': 'FN61712PEW-OGY', 'desc': 'Biltmore Dining Arm Chair', 'available': 26}, {'item': 'FN61704OGY', 'desc': 'Biltmore Coffee Table', 'available': 24}, {'item': 'FN61716PEW-OGY', 'desc': 'Biltmore Ottoman', 'available': 23}, {'item': 'FN61706PEY-OGY', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 23}, {'item': 'FN61712WTR', 'desc': 'Biltmore Dining Arm Chair', 'available': 19}, {'item': 'FN61704RUB', 'desc': 'Biltmore Coffee Table', 'available': 16}, {'item': 'FN61788PEW-OGY', 'desc': 'Biltmore Swivel Recliner', 'available': 15}, {'item': 'FN61704PEY-OGY', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 12}, {'item': 'FN61703PEW-OGY', 'desc': 'Biltmore Sofa', 'available': 10}, {'item': 'FN61704WLT-RUB', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 7}, {'item': 'FN61701WTR', 'desc': 'Biltmore Club Chair', 'available': 7}, {'item': 'FN61702WTR', 'desc': 'Biltmore Love Seat', 'available': 7}, {'item': 'FN61703WTR', 'desc': 'Biltmore Sofa', 'available': 7}, {'item': 'FN61704HGA', 'desc': 'Biltmore Coffee Table', 'available': 5}, {'item': 'FN61705PEY-OGY', 'desc': 'Biltmore Sintered Stone End Table', 'available': 4}, {'item': 'FN61703WTR-RUB', 'desc': 'Biltmore Sofa', 'available': 2}, {'item': 'FN61706WLT-RUB', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 1}] |
| UM01009BLK/C | 10' Sq Cantilever Umbrella w/Canopy&Base | COL73 | 169,959 | 149 | 13 | — | [{'customer': 'Vancouver Sofa & Patio', 'revenue': 42717.0}, {'customer': 'Patio & Home Direct', 'revenue': 13575.0}, {'customer': 'Country Furniture', 'revenue': 12491.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 11408.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 8730.0}, {'customer': 'St. Lawrence Pools', 'revenue': 7167.0}, {'customer': 'Innovations paysagées Ladouceur', 'revenue': 6273.0}, {'customer': 'Okanagan Home Center', 'revenue': 5796.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 5269.0}, {'customer': 'Garden Architecture & Design', 'revenue': 4568.0}, {'customer': 'CO-OP At Home', 'revenue': 3749.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 3638.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 3566.0}, {'customer': 'Cozy Stylish Chic', 'revenue': 2537.0}, {'customer': 'Janelle Interiors', 'revenue': 2450.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 2402.0}, {'customer': 'Design Therapy Inc', 'revenue': 2166.0}, {'customer': 'PHG Ashburn LLC', 'revenue': 1871.0}, {'customer': 'Image Urbaine', 'revenue': 1686.0}, {'customer': 'Stacey White Design', 'revenue': 1686.0}, {'customer': 'Homey Home', 'revenue': 1550.0}, {'customer': 'Cash Account (c$)', 'revenue': 1349.0}, {'customer': 'Terra Verde', 'revenue': 1349.0}, {'customer': 'Parco Piscines & Spas Ltee (mq018)', 'revenue': 1349.0}, {'customer': 'Joanna Branzell Interior Design', 'revenue': 1325.0}, {'customer': 'Coombs Furniture', 'revenue': 1320.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 1320.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 1281.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 1269.0}, {'customer': 'Cash Account', 'revenue': 1269.0}, {'customer': "Voth's Brandsource Home Furnishings", 'revenue': 1269.0}, {'customer': 'Hilltop Interiors', 'revenue': 1240.0}, {'customer': "Piscines CM Val D'or Inc (mq002)", 'revenue': 1240.0}, {'customer': 'Club Piscines Granby', 'revenue': 1190.0}, {'customer': 'O.M. Design Group', 'revenue': 1187.0}, {'customer': 'The Art of Room Design', 'revenue': 1187.0}, {'customer': 'Meubles Duboise', 'revenue': 1178.0}, {'customer': 'Maud Home', 'revenue': 1116.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1116.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 1056.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 1054.0}, {'customer': 'Design One Stevens Interiors', 'revenue': 0.0}, {'customer': 'Studio B Design Group', 'revenue': 0.0}, {'customer': 'Curve Interiors', 'revenue': 0.0}] | [{'item': 'UM01010SLV-CCL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Cloud canopy", 'available': 10}, {'item': 'UM01010SLV-CBL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Black canopy", 'available': 9}, {'item': 'UM01004SLV/C', 'desc': "10' Sq Deluxe Alum Umbrella, 48mm Pole W/canopy", 'available': 8}, {'item': 'UM00906BRZ/C', 'desc': "9' Alum W/fiber Ribs,crank Lift,collar Tilt,canopy", 'available': 6}, {'item': 'UM00909POLE-BRZ', 'desc': '45in Bar Bottom Pole for UM00906BRZ/C', 'available': 5}] |
| FN54420ASG | Lucia Lounger | LUCIA | 165,018 | 203 | 0 | — | [{'customer': 'Palmetto Bluff Club LLC', 'revenue': 83497.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 10031.0}, {'customer': 'Source', 'revenue': 9901.0}, {'customer': 'Patio & Home Direct', 'revenue': 6888.0}, {'customer': 'Image Urbaine', 'revenue': 3690.0}, {'customer': 'Furniture Solutions Group', 'revenue': 3630.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 3300.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 3280.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 3075.0}, {'customer': 'Macarthur Enterprises Ltd', 'revenue': 3075.0}, {'customer': 'Crystalview', 'revenue': 2952.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 2788.0}, {'customer': 'Meubles Poisson Ltée', 'revenue': 2460.0}, {'customer': 'Cash Account', 'revenue': 2460.0}, {'customer': 'Garden Architecture & Design', 'revenue': 2460.0}, {'customer': 'Parc Communities Management Ltd', 'revenue': 2132.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 2112.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 1980.0}, {'customer': 'Joanna Branzell Interior Design', 'revenue': 1650.0}, {'customer': 'Maritime Hospitality (Danja Inc)', 'revenue': 1640.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1476.0}, {'customer': "Mio's Furniture Fashions", 'revenue': 1394.0}, {'customer': 'Patio Productions', 'revenue': 1336.0}, {'customer': 'B H Allen Building Centre', 'revenue': 1312.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1230.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 1188.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 738.0}, {'customer': 'Net Retailers LLC', 'revenue': 726.0}, {'customer': 'Can-Tario Brick & Stone', 'revenue': 697.0}, {'customer': 'Ifurnish Co.', 'revenue': 660.0}, {'customer': 'Christy Sports, LLC', 'revenue': 653.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 607.0}] | [{'item': 'FN54411OGY', 'desc': 'Lucia Dining Side Chair', 'available': 94}, {'item': 'FN54411ASG', 'desc': 'Lucia Dining Side Chair', 'available': 89}, {'item': 'FN54441OGY', 'desc': 'Lucia Bar Chair', 'available': 44}, {'item': 'FN54412OGY', 'desc': 'Lucia Dining Arm Chair', 'available': 43}, {'item': 'FN54453ASG-V', 'desc': 'Lucia Curved Corner', 'available': 31}, {'item': 'FN54402OGY', 'desc': 'Lucia Love Seat', 'available': 30}, {'item': 'FN54440OGY', 'desc': 'Lucia Counter Chair', 'available': 30}, {'item': 'FN54458PRL', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 29}, {'item': 'FN54453OGY-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 28}, {'item': 'FN54453OGY-V', 'desc': 'Lucia Curved Corner', 'available': 25}, {'item': 'FN54453ASG-R', 'desc': 'Lucia Wedge Right Arm', 'available': 25}, {'item': 'FN54452OGY-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 25}, {'item': 'FN54452OGY-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 25}, {'item': 'FN54404PRL', 'desc': 'Lucia Coffee Table', 'available': 24}, {'item': 'FN54453ASG-L', 'desc': 'Lucia Wedge Left Arm', 'available': 22}, {'item': 'FN54404ASG', 'desc': 'Lucia Coffee Table', 'available': 17}, {'item': 'FN54420OGY', 'desc': 'Lucia Lounger', 'available': 15}, {'item': 'FN54452ASG-C', 'desc': 'Lucia Wedge Corner', 'available': 14}, {'item': 'FN54416OGY', 'desc': 'Lucia Ottoman', 'available': 14}, {'item': 'FN54403PRL', 'desc': 'Lucia Sofa', 'available': 13}, {'item': 'FN54452ASG-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 12}, {'item': 'FN54452ASG-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 12}, {'item': 'FN54416ASG', 'desc': 'Lucia Ottoman', 'available': 12}, {'item': 'FN54458ASG', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 11}, {'item': 'FN54405PEY-OGY', 'desc': 'Lucia Sintered Stone End Table (KD)', 'available': 10}, {'item': 'FN54457ASG', 'desc': 'Lucia Sectional 40in Round Coffee Table/ottoman', 'available': 8}, {'item': 'FN54453ASG-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 8}, {'item': 'FN54468PRL', 'desc': 'Lucia Swivel Rocker', 'available': 6}, {'item': 'FN54404PEY-OGY', 'desc': 'Lucia Sintered Stone Coffee Table (KD)', 'available': 6}, {'item': 'FN54468OGY', 'desc': 'Lucia Swivel Rocker', 'available': 4}, {'item': 'FN54441ASG', 'desc': 'Lucia Bar Chair', 'available': 4}, {'item': 'FN54440ASG', 'desc': 'Lucia Counter Chair', 'available': 4}, {'item': 'FN54412ASG', 'desc': 'Lucia Dining Arm Chair', 'available': 4}, {'item': 'FN54405PRL', 'desc': 'Lucia End Table', 'available': 2}, {'item': 'FN54405ASG', 'desc': 'Lucia End Table', 'available': 1}] |
| FN57001ASG | Element 5.0 Club Chair | COL61 | 163,081 | 279 | 14 | — | [{'customer': 'Bobby Design Inc.', 'revenue': 17572.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 11495.0}, {'customer': 'Dave Bang Associates Inc.', 'revenue': 11181.0}, {'customer': 'Thiel and Thiel, Inc', 'revenue': 9681.0}, {'customer': 'Net Retailers LLC', 'revenue': 7985.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 7720.0}, {'customer': 'Isidore Landscapes Inc.', 'revenue': 7601.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 6566.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 5654.0}, {'customer': 'Westin Kierland Resort & Spa', 'revenue': 5324.0}, {'customer': 'Royal Kona Resort', 'revenue': 4840.0}, {'customer': 'The Design Resource Group, Inc.', 'revenue': 4840.0}, {'customer': "Bishop's Casual Living", 'revenue': 3830.0}, {'customer': 'Houston Landscapes Ltd.', 'revenue': 3648.0}, {'customer': 'Studio Dwell', 'revenue': 3630.0}, {'customer': 'Patio & Home Direct', 'revenue': 3587.0}, {'customer': 'Luxe Furniture Company', 'revenue': 3174.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 2797.0}, {'customer': 'Kerry Imagine Designs Llc', 'revenue': 2662.0}, {'customer': 'Adria International Inc', 'revenue': 2584.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2462.0}, {'customer': 'Timmermans Landscaping', 'revenue': 2280.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 2189.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 2189.0}, {'customer': 'Country Furniture', 'revenue': 2189.0}, {'customer': 'Room By Room', 'revenue': 1824.0}, {'customer': 'Ifurnish Co.', 'revenue': 1802.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1549.0}, {'customer': 'Aava Whistler Hotel', 'revenue': 1520.0}, {'customer': 'Sun Gallery Patio Furniture Ltd.', 'revenue': 1368.0}, {'customer': 'Distrist Hubert Inc', 'revenue': 1368.0}, {'customer': "Today's Patio", 'revenue': 1300.0}, {'customer': 'Rethink Interiors&lifestyles', 'revenue': 1210.0}, {'customer': 'O.M. Design Group', 'revenue': 1210.0}, {'customer': 'IDM Development, LLC', 'revenue': 1210.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 1098.0}, {'customer': 'Heritage Office Furnishings Ltd.', 'revenue': 1094.0}, {'customer': 'All Backyard Fun', 'revenue': 1065.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 1065.0}, {'customer': 'Club Piscine (Terrebonne)', 'revenue': 1034.0}, {'customer': 'East Texas Brick', 'revenue': 871.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 775.0}, {'customer': 'Morinville Home Hardware', 'revenue': 760.0}, {'customer': 'The Collaborative Design Studio Inc', 'revenue': 760.0}, {'customer': 'Solutions Business Interiors', 'revenue': 760.0}, {'customer': 'Monticello Homes', 'revenue': 666.0}, {'customer': 'Bridge Interiors Furniture', 'revenue': 608.0}, {'customer': 'Patio Style', 'revenue': 484.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 0.0}, {'customer': 'Furniture Solutions Group', 'revenue': 0.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 0.0}] | [{'item': 'FN57011TWH', 'desc': 'Element 5.0 Dining Side Chair', 'available': 52}, {'item': 'FN57068OGY', 'desc': 'Element 5.0 Swivel Rocker', 'available': 39}, {'item': 'FN57068ASG', 'desc': 'Element 5.0 Swivel Rocker', 'available': 32}, {'item': 'FN57012TWH', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 31}, {'item': 'FN57005TWH', 'desc': 'Element 5.0 40in Sq C/T w/alum', 'available': 30}, {'item': 'FN57001OGY', 'desc': 'Element 5.0 Club Chair', 'available': 29}, {'item': 'FN57003OGY', 'desc': 'Element 5.0 2.5-seater Sofa', 'available': 28}, {'item': 'FN57016OGY', 'desc': 'Element 5.0 Ottoman', 'available': 25}, {'item': 'FN57016TWH', 'desc': 'Element 5.0 Ottoman', 'available': 17}, {'item': 'FN57005PEY-OGY', 'desc': 'Element 5.0 40in Square Sintered Stone Coffee Tabl', 'available': 17}, {'item': 'FN57052OGY-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 12}, {'item': 'FN57004TWH', 'desc': 'Element 5.0 Rect C/T w/alum', 'available': 12}, {'item': 'FN57052OGY-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 12}, {'item': 'FN57019ASG', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 11}, {'item': 'FN57021OGY', 'desc': 'Element 5.0 Double Chaise Lounger (New structure)', 'available': 11}, {'item': 'FN57068TWH', 'desc': 'Element 5.0 Swivel Rocker', 'available': 10}, {'item': 'FN57053OGY-N', 'desc': 'Element 5.0 Corner', 'available': 9}, {'item': 'FN57006PEY-OGY', 'desc': 'Element 5.0 Sintered Stone Side Table', 'available': 9}, {'item': 'FN57053OGY-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 8}, {'item': 'FN57004PEY-OGY', 'desc': 'Element 5.0 Rect Sintered Stone Coffee Table', 'available': 8}, {'item': 'FN57019OGY', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 7}, {'item': 'FN57012ASG', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 7}, {'item': 'FN57003TWH', 'desc': 'Element 5.0 2.5-Seater Sofa', 'available': 6}, {'item': 'FN57022WHT', 'desc': 'Element 5.0 Double Chaise Lounger', 'available': 5}, {'item': 'FN57052ASG-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 5}, {'item': 'FN57052TWH-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 4}, {'item': 'FN57053ASG-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57006CEM', 'desc': 'Element 5.0 Side Table W/alum Top CEM, Base ASG', 'available': 3}, {'item': 'FN57053TWH-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57053TWH-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 2}, {'item': 'FN57052ASG-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 2}, {'item': 'FN57052TWH-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 2}, {'item': 'FN57053ASG-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 1}, {'item': 'FN57011ASG', 'desc': 'Element 5.0 Dining Side Chair', 'available': 1}, {'item': 'FN57001TWH', 'desc': 'Element 5.0 Club Chair', 'available': 1}] |
| FN65520BLK | Avenue Lounger | COL145 | 159,588 | 236 | 10 | 2026-6-30 | [{'customer': 'Victory Furniture LLC.', 'revenue': 27717.0}, {'customer': 'Ellie Aiello Interiors', 'revenue': 22332.0}, {'customer': 'Two Fifty Master LLC c/o The Gettys Group', 'revenue': 15247.0}, {'customer': 'Streetlights Residential', 'revenue': 13301.0}, {'customer': 'Country Furniture', 'revenue': 11340.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 5670.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 5319.0}, {'customer': 'Sanctuary Home & Patio', 'revenue': 4928.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 4200.0}, {'customer': 'All American Pool & Patio', 'revenue': 3696.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 3500.0}, {'customer': "Bishop's Casual Living", 'revenue': 3150.0}, {'customer': 'Southport Outdoor Living', 'revenue': 3150.0}, {'customer': 'Contract Furniture Solutions', 'revenue': 2800.0}, {'customer': 'Piscine Hippocampe', 'revenue': 2800.0}, {'customer': 'Wade Gordon Hairdressing Academy', 'revenue': 2800.0}, {'customer': 'Light House Co.', 'revenue': 2800.0}, {'customer': 'Royal Bay Ryder Village LP', 'revenue': 2625.0}, {'customer': 'The Patio Place USA, Inc', 'revenue': 2464.0}, {'customer': 'Garden Architecture & Design', 'revenue': 2369.0}, {'customer': 'Waterleaf Interiors /DOS Amigas Designs Inc', 'revenue': 2310.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 2100.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 1890.0}, {'customer': 'Furniture Source International', 'revenue': 1792.0}, {'customer': 'Northland Properties Corporation', 'revenue': 1750.0}, {'customer': 'Studio Dwell', 'revenue': 1540.0}, {'customer': 'Patio Options', 'revenue': 1540.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 1190.0}, {'customer': 'The Patio', 'revenue': 952.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 700.0}, {'customer': 'Crystalview', 'revenue': 630.0}, {'customer': 'Daylight Home & Gardens', 'revenue': 616.0}, {'customer': 'Emerald Expositions, LLC', 'revenue': 370.0}, {'customer': 'Arveaux Interiors', 'revenue': 0.0}, {'customer': 'Luxe Furniture Company', 'revenue': 0.0}] | [{'item': 'FN65505WHT', 'desc': 'Avenue Side Table', 'available': 27}, {'item': 'FN65505BLK', 'desc': 'Avenue Side Table', 'available': 24}] |
| CU61301 | Poinciana Club Chair Cushion | COL217 | 152,554 | 637 | 8 | — | [{'customer': 'Elland Property Development Limited', 'revenue': 75066.0}, {'customer': 'JW Marriott Desert Ridge Resort and Spa', 'revenue': 19197.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 5763.0}, {'customer': 'KB Patio', 'revenue': 3492.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 3166.0}, {'customer': 'Luxe Furniture Company', 'revenue': 3116.0}, {'customer': 'CIB c/o Benjamin West (as agent)', 'revenue': 2588.0}, {'customer': 'J. Davenport Associates', 'revenue': 2560.0}, {'customer': 'Two Fifty Master LLC c/o The Gettys Group', 'revenue': 2205.0}, {'customer': 'Wegman Design Group', 'revenue': 2094.0}, {'customer': 'Keaton Interiors', 'revenue': 2038.0}, {'customer': 'Bluegreen Vacation Unlimited c/o Beyer Brown(agent', 'revenue': 1960.0}, {'customer': 'Hilton Supply Management', 'revenue': 1859.0}, {'customer': 'Creative License International, LLC', 'revenue': 1760.0}, {'customer': 'The Haus of Alchemy', 'revenue': 1620.0}, {'customer': 'GCC Procurement, LLC', 'revenue': 1593.0}, {'customer': 'Kathy Andrews Interiors, Inc.', 'revenue': 1581.0}, {'customer': 'Eatz Hospitality/Del Boca Brickell LP', 'revenue': 1425.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 1340.0}, {'customer': 'Patio Productions', 'revenue': 1101.0}, {'customer': 'Contract Furniture Solutions', 'revenue': 1080.0}, {'customer': 'Pixel Design Co.', 'revenue': 1080.0}, {'customer': 'Vicki Crew Interiors', 'revenue': 1000.0}, {'customer': 'The Art of Room Design', 'revenue': 980.0}, {'customer': 'Bobby Design Inc.', 'revenue': 950.0}, {'customer': 'Zauner Manhattan Design', 'revenue': 950.0}, {'customer': 'Net Retailers LLC', 'revenue': 758.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 740.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 700.0}, {'customer': 'Trio, Inc.', 'revenue': 675.0}, {'customer': 'Club Design Group, Inc.', 'revenue': 630.0}, {'customer': 'Lita Dirks & Co, Llc', 'revenue': 625.0}, {'customer': 'Country Furniture', 'revenue': 603.0}, {'customer': 'Alison Knapp Interior Design', 'revenue': 588.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 528.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 420.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 396.0}, {'customer': 'Elegant Outdoor Living', 'revenue': 392.0}, {'customer': 'Bow Valley Garden Centre', 'revenue': 392.0}, {'customer': 'S. Setlakwe Ltee', 'revenue': 392.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 352.0}, {'customer': 'Tri Supply Company', 'revenue': 352.0}, {'customer': 'Garden Architecture & Design', 'revenue': 332.0}, {'customer': 'Southport Outdoor Living', 'revenue': 315.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 311.0}, {'customer': 'Insideout Home & Patio (Toronto)', 'revenue': 282.0}, {'customer': 'Woodmill of Muskoka Inc', 'revenue': 282.0}, {'customer': 'The Patio Place USA, Inc', 'revenue': 216.0}, {'customer': 'Modern Living London', 'revenue': 173.0}, {'customer': 'Okanagan Home Center', 'revenue': 161.0}, {'customer': 'Les Jardins', 'revenue': 157.0}, {'customer': 'Real Patio Living Llc', 'revenue': 118.0}, {'customer': 'Cash Account', 'revenue': 100.0}, {'customer': 'Focus Design Interiors', 'revenue': 0.0}] | [{'item': 'CU61311', 'desc': 'Poinciana Dining Side Cushion (with button)', 'available': 2}] |
| FN57003ASG | Element 5.0 2.5-seater Sofa | COL61 | 135,573 | 135 | 0 | — | [{'customer': 'Tru Contract Interiors', 'revenue': 13343.0}, {'customer': 'Houston Landscapes Ltd.', 'revenue': 7783.0}, {'customer': 'Dave Bang Associates Inc.', 'revenue': 6838.0}, {'customer': 'Net Retailers LLC', 'revenue': 5860.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 5614.0}, {'customer': 'Country Furniture', 'revenue': 5004.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 4504.0}, {'customer': 'Royal Kona Resort', 'revenue': 4440.0}, {'customer': 'Bobby Design Inc.', 'revenue': 4170.0}, {'customer': 'Timmermans Landscaping', 'revenue': 4170.0}, {'customer': "Bishop's Casual Living", 'revenue': 4003.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 4003.0}, {'customer': 'Home And Patio', 'revenue': 3907.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 3552.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 3002.0}, {'customer': 'Patio & Home Direct', 'revenue': 3002.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 3002.0}, {'customer': 'Keca International', 'revenue': 2835.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2835.0}, {'customer': 'West One Design Inc.', 'revenue': 2780.0}, {'customer': 'Give Back Contracting', 'revenue': 2780.0}, {'customer': 'Sun Gallery Patio Furniture Ltd.', 'revenue': 2502.0}, {'customer': 'Haylie Read Design, LLC', 'revenue': 2220.0}, {'customer': 'Complete Office LLC', 'revenue': 2220.0}, {'customer': 'The Design Resource Group, Inc.', 'revenue': 2220.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 2007.0}, {'customer': 'Industrial Revolution', 'revenue': 1890.0}, {'customer': 'The Patio', 'revenue': 1731.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 1687.0}, {'customer': 'Distrist Hubert Inc', 'revenue': 1668.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1421.0}, {'customer': "Today's Patio", 'revenue': 1319.0}, {'customer': 'Sandman Signature Dallas Las Colinas Hotel &Suites', 'revenue': 1221.0}, {'customer': 'Trio, Inc.', 'revenue': 1221.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 1112.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1110.0}, {'customer': 'Rethink Interiors&lifestyles', 'revenue': 1110.0}, {'customer': 'Studio Dwell', 'revenue': 1110.0}, {'customer': 'Joanna Branzell Interior Design', 'revenue': 1110.0}, {'customer': 'Crystalview', 'revenue': 1001.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 977.0}, {'customer': 'Luxe Furniture Company', 'revenue': 967.0}, {'customer': 'Patio Style', 'revenue': 888.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 888.0}, {'customer': 'Innovative Designs & Mfg. Inc.', 'revenue': 888.0}, {'customer': 'Designers Resource Collection', 'revenue': 879.0}, {'customer': 'Ifurnish Co.', 'revenue': 830.0}, {'customer': 'East Texas Brick', 'revenue': 799.0}, {'customer': 'Davis Porch & Patio LLC. (CLOSED)', 'revenue': 710.0}, {'customer': 'Patio Fireside Specialist Inc(sales Rep)', 'revenue': 440.0}] | [{'item': 'FN57011TWH', 'desc': 'Element 5.0 Dining Side Chair', 'available': 52}, {'item': 'FN57068OGY', 'desc': 'Element 5.0 Swivel Rocker', 'available': 39}, {'item': 'FN57068ASG', 'desc': 'Element 5.0 Swivel Rocker', 'available': 32}, {'item': 'FN57012TWH', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 31}, {'item': 'FN57005TWH', 'desc': 'Element 5.0 40in Sq C/T w/alum', 'available': 30}, {'item': 'FN57001OGY', 'desc': 'Element 5.0 Club Chair', 'available': 29}, {'item': 'FN57003OGY', 'desc': 'Element 5.0 2.5-seater Sofa', 'available': 28}, {'item': 'FN57016OGY', 'desc': 'Element 5.0 Ottoman', 'available': 25}, {'item': 'FN57016TWH', 'desc': 'Element 5.0 Ottoman', 'available': 17}, {'item': 'FN57005PEY-OGY', 'desc': 'Element 5.0 40in Square Sintered Stone Coffee Tabl', 'available': 17}, {'item': 'FN57052OGY-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 12}, {'item': 'FN57004TWH', 'desc': 'Element 5.0 Rect C/T w/alum', 'available': 12}, {'item': 'FN57052OGY-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 12}, {'item': 'FN57019ASG', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 11}, {'item': 'FN57021OGY', 'desc': 'Element 5.0 Double Chaise Lounger (New structure)', 'available': 11}, {'item': 'FN57068TWH', 'desc': 'Element 5.0 Swivel Rocker', 'available': 10}, {'item': 'FN57053OGY-N', 'desc': 'Element 5.0 Corner', 'available': 9}, {'item': 'FN57006PEY-OGY', 'desc': 'Element 5.0 Sintered Stone Side Table', 'available': 9}, {'item': 'FN57053OGY-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 8}, {'item': 'FN57004PEY-OGY', 'desc': 'Element 5.0 Rect Sintered Stone Coffee Table', 'available': 8}, {'item': 'FN57019OGY', 'desc': 'Element 5.0 Lounger (New structure)', 'available': 7}, {'item': 'FN57012ASG', 'desc': 'Element 5.0 Dining Arm Chair', 'available': 7}, {'item': 'FN57003TWH', 'desc': 'Element 5.0 2.5-Seater Sofa', 'available': 6}, {'item': 'FN57022WHT', 'desc': 'Element 5.0 Double Chaise Lounger', 'available': 5}, {'item': 'FN57052ASG-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 5}, {'item': 'FN57052TWH-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 4}, {'item': 'FN57053ASG-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57006CEM', 'desc': 'Element 5.0 Side Table W/alum Top CEM, Base ASG', 'available': 3}, {'item': 'FN57053TWH-N', 'desc': 'Element 5.0 Corner', 'available': 3}, {'item': 'FN57053TWH-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 2}, {'item': 'FN57052ASG-L', 'desc': 'Element 5.0 2-seater Left Arm', 'available': 2}, {'item': 'FN57052TWH-R', 'desc': 'Element 5.0 2-seater Right Arm', 'available': 2}, {'item': 'FN57053ASG-C', 'desc': 'Element 5.0 Chair (w/o Arm)', 'available': 1}, {'item': 'FN57011ASG', 'desc': 'Element 5.0 Dining Side Chair', 'available': 1}, {'item': 'FN57001TWH', 'desc': 'Element 5.0 Club Chair', 'available': 1}] |
| FN54403ASG | Lucia Sofa | LUCIA | 132,614 | 131 | 4 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 12365.0}, {'customer': 'Northwest Trends', 'revenue': 9856.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 7615.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 5168.0}, {'customer': 'Patio & Home Direct', 'revenue': 5058.0}, {'customer': 'Hue Design LLC', 'revenue': 4599.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 4327.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 4215.0}, {'customer': 'B H Allen Building Centre', 'revenue': 3878.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 3285.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 2866.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 2810.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2641.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 2409.0}, {'customer': 'Studio B Design Group', 'revenue': 2409.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 2409.0}, {'customer': 'Furniture Solutions Group', 'revenue': 2409.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 2409.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 2190.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 2023.0}, {'customer': 'Country Furniture', 'revenue': 2023.0}, {'customer': "Today's Patio", 'revenue': 1927.0}, {'customer': 'Crystalview', 'revenue': 1855.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1752.0}, {'customer': 'Abacus Furniture', 'revenue': 1686.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 1612.0}, {'customer': 'Cincinnati Pool & Patio', 'revenue': 1402.0}, {'customer': 'MOI Inc.', 'revenue': 1205.0}, {'customer': 'VAI Resort, LLC', 'revenue': 1205.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 1205.0}, {'customer': 'DGA Interiors', 'revenue': 1205.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 1205.0}, {'customer': 'Direct Supply Inc.', 'revenue': 1205.0}, {'customer': 'Entreprises H.P. Carignan Inc(mq034', 'revenue': 1124.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 1095.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 1095.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 1095.0}, {'customer': 'Kevin Roberts Interiors', 'revenue': 1095.0}, {'customer': 'Commonwealth Design Group', 'revenue': 1095.0}, {'customer': 'GST Interiors, LLC', 'revenue': 1095.0}, {'customer': 'Patio Comfort', 'revenue': 1068.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1012.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 1012.0}, {'customer': 'St. Lawrence Pools', 'revenue': 1012.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 1012.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1012.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 1012.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1012.0}, {'customer': 'Rattan Wicker & Cane', 'revenue': 964.0}, {'customer': 'Net Retailers LLC', 'revenue': 964.0}, {'customer': 'Industrial Revolution', 'revenue': 955.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 955.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 955.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 887.0}, {'customer': 'All Backyard Fun', 'revenue': 876.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 876.0}, {'customer': 'Main Street Furniture', 'revenue': 876.0}, {'customer': 'C.S. Wo & Sons, Ltd', 'revenue': 876.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 843.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 806.0}, {'customer': 'Patio Productions', 'revenue': 806.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 701.0}, {'customer': 'Mike Moser Studio', 'revenue': 0.0}] | [{'item': 'FN54411OGY', 'desc': 'Lucia Dining Side Chair', 'available': 94}, {'item': 'FN54411ASG', 'desc': 'Lucia Dining Side Chair', 'available': 89}, {'item': 'FN54441OGY', 'desc': 'Lucia Bar Chair', 'available': 44}, {'item': 'FN54412OGY', 'desc': 'Lucia Dining Arm Chair', 'available': 43}, {'item': 'FN54453ASG-V', 'desc': 'Lucia Curved Corner', 'available': 31}, {'item': 'FN54402OGY', 'desc': 'Lucia Love Seat', 'available': 30}, {'item': 'FN54440OGY', 'desc': 'Lucia Counter Chair', 'available': 30}, {'item': 'FN54458PRL', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 29}, {'item': 'FN54453OGY-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 28}, {'item': 'FN54453OGY-V', 'desc': 'Lucia Curved Corner', 'available': 25}, {'item': 'FN54453ASG-R', 'desc': 'Lucia Wedge Right Arm', 'available': 25}, {'item': 'FN54452OGY-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 25}, {'item': 'FN54452OGY-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 25}, {'item': 'FN54404PRL', 'desc': 'Lucia Coffee Table', 'available': 24}, {'item': 'FN54453ASG-L', 'desc': 'Lucia Wedge Left Arm', 'available': 22}, {'item': 'FN54404ASG', 'desc': 'Lucia Coffee Table', 'available': 17}, {'item': 'FN54420OGY', 'desc': 'Lucia Lounger', 'available': 15}, {'item': 'FN54452ASG-C', 'desc': 'Lucia Wedge Corner', 'available': 14}, {'item': 'FN54416OGY', 'desc': 'Lucia Ottoman', 'available': 14}, {'item': 'FN54403PRL', 'desc': 'Lucia Sofa', 'available': 13}, {'item': 'FN54452ASG-R', 'desc': 'Lucia 2-seater Right Arm', 'available': 12}, {'item': 'FN54452ASG-L', 'desc': 'Lucia 2-seater Left Arm', 'available': 12}, {'item': 'FN54416ASG', 'desc': 'Lucia Ottoman', 'available': 12}, {'item': 'FN54458ASG', 'desc': 'Lucia Swivel Rocking Arm Chair', 'available': 11}, {'item': 'FN54405PEY-OGY', 'desc': 'Lucia Sintered Stone End Table (KD)', 'available': 10}, {'item': 'FN54457ASG', 'desc': 'Lucia Sectional 40in Round Coffee Table/ottoman', 'available': 8}, {'item': 'FN54453ASG-C', 'desc': 'Lucia Chair (w/o Arm)', 'available': 8}, {'item': 'FN54468PRL', 'desc': 'Lucia Swivel Rocker', 'available': 6}, {'item': 'FN54404PEY-OGY', 'desc': 'Lucia Sintered Stone Coffee Table (KD)', 'available': 6}, {'item': 'FN54468OGY', 'desc': 'Lucia Swivel Rocker', 'available': 4}, {'item': 'FN54441ASG', 'desc': 'Lucia Bar Chair', 'available': 4}, {'item': 'FN54440ASG', 'desc': 'Lucia Counter Chair', 'available': 4}, {'item': 'FN54412ASG', 'desc': 'Lucia Dining Arm Chair', 'available': 4}, {'item': 'FN54405PRL', 'desc': 'Lucia End Table', 'available': 2}, {'item': 'FN54405ASG', 'desc': 'Lucia End Table', 'available': 1}] |
| FN61790WTR-RUB | Biltmore Swivel Gliding Club | COL87 | 131,032 | 221 | 142 | 2026-6-16 | [{'customer': 'Sunnyland Furniture', 'revenue': 18727.0}, {'customer': 'Into The Garden, Inc.', 'revenue': 18672.0}, {'customer': 'Jack Wills Companies', 'revenue': 10846.0}, {'customer': 'The Fireplace & Patio Place', 'revenue': 9299.0}, {'customer': 'Tri Supply Company', 'revenue': 8787.0}, {'customer': 'Home And Patio', 'revenue': 7397.0}, {'customer': 'Georgia Patio Inc', 'revenue': 7000.0}, {'customer': 'If Walls Could Talk', 'revenue': 6865.0}, {'customer': 'OutBack Patio Furnishings', 'revenue': 5285.0}, {'customer': "Bowman's Stove & Patio Inc.", 'revenue': 3707.0}, {'customer': 'Casual Living Outfitters Llc', 'revenue': 3295.0}, {'customer': 'Sabine Pools Llc', 'revenue': 3295.0}, {'customer': 'Treescapes - The Outdoor Living Center', 'revenue': 2745.0}, {'customer': 'Luxe Furniture Company', 'revenue': 2663.0}, {'customer': 'Balboa Company', 'revenue': 2471.0}, {'customer': 'Backyard Adventures Of Iowa', 'revenue': 2333.0}, {'customer': "Al's Garden Center& Greenhouses, LLC", 'revenue': 2197.0}, {'customer': 'Corner Collection', 'revenue': 2197.0}, {'customer': "Callaway's Yard & Garden", 'revenue': 1688.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 1581.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 1498.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 1414.0}, {'customer': 'Zing Quality Furniture Inc', 'revenue': 1373.0}, {'customer': 'Sunset Home and Patio', 'revenue': 1373.0}, {'customer': 'Busch Fireplace', 'revenue': 1236.0}, {'customer': 'Pangaea Patio', 'revenue': 1235.0}, {'customer': 'Philadelphia Botanical Products', 'revenue': 1167.0}, {'customer': 'Patio Style', 'revenue': 686.0}, {'customer': 'Casual Marketplace, Inc.', 'revenue': 0.0}, {'customer': 'Mt.Lake Pool and Patio', 'revenue': 0.0}, {'customer': 'Net Retailers LLC', 'revenue': 0.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 0.0}, {'customer': 'ZLM Enterprises', 'revenue': 0.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 0.0}, {'customer': 'Cape Leisure, Inc.', 'revenue': 0.0}] | [{'item': 'FN61711WTR', 'desc': 'Biltmore Dining Side Chair', 'available': 52}, {'item': 'FN61711PEW-OGY', 'desc': 'Biltmore Dining Side Chair', 'available': 38}, {'item': 'FN61712PEW-OGY', 'desc': 'Biltmore Dining Arm Chair', 'available': 26}, {'item': 'FN61704OGY', 'desc': 'Biltmore Coffee Table', 'available': 24}, {'item': 'FN61716PEW-OGY', 'desc': 'Biltmore Ottoman', 'available': 23}, {'item': 'FN61706PEY-OGY', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 23}, {'item': 'FN61712WTR', 'desc': 'Biltmore Dining Arm Chair', 'available': 19}, {'item': 'FN61704RUB', 'desc': 'Biltmore Coffee Table', 'available': 16}, {'item': 'FN61788PEW-OGY', 'desc': 'Biltmore Swivel Recliner', 'available': 15}, {'item': 'FN61704PEY-OGY', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 12}, {'item': 'FN61703PEW-OGY', 'desc': 'Biltmore Sofa', 'available': 10}, {'item': 'FN61704WLT-RUB', 'desc': 'Biltmore Sintered Stone Coffee Table', 'available': 7}, {'item': 'FN61701WTR', 'desc': 'Biltmore Club Chair', 'available': 7}, {'item': 'FN61702WTR', 'desc': 'Biltmore Love Seat', 'available': 7}, {'item': 'FN61703WTR', 'desc': 'Biltmore Sofa', 'available': 7}, {'item': 'FN61704HGA', 'desc': 'Biltmore Coffee Table', 'available': 5}, {'item': 'FN61705PEY-OGY', 'desc': 'Biltmore Sintered Stone End Table', 'available': 4}, {'item': 'FN61703WTR-RUB', 'desc': 'Biltmore Sofa', 'available': 2}, {'item': 'FN61706WLT-RUB', 'desc': 'Biltmore 18in Square Sintered Stone Side Table', 'available': 1}] |
| CU54403 | Lucia Sofa Cushion | COL203 | 127,402 | 248 | 26 | — | [{'customer': 'ACL Design Build Solutions', 'revenue': 8133.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 6839.0}, {'customer': 'Northwest Trends', 'revenue': 6599.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 6554.0}, {'customer': 'Country Furniture', 'revenue': 4699.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 4329.0}, {'customer': 'B H Allen Building Centre', 'revenue': 3858.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 3750.0}, {'customer': 'Patio & Home Direct', 'revenue': 3162.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 2783.0}, {'customer': 'DGA Interiors', 'revenue': 2504.0}, {'customer': 'Hue Design LLC', 'revenue': 2310.0}, {'customer': 'Bobby Design Inc.', 'revenue': 2144.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 2067.0}, {'customer': 'We are Sparrow Studio', 'revenue': 1975.0}, {'customer': 'Garden Architecture & Design', 'revenue': 1865.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 1770.0}, {'customer': 'Crystalview', 'revenue': 1727.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 1665.0}, {'customer': 'Touchmark, LLC', 'revenue': 1617.0}, {'customer': 'Wegman Design Group', 'revenue': 1498.0}, {'customer': 'CMS Commercial Furniture', 'revenue': 1487.0}, {'customer': 'Studio 4d', 'revenue': 1467.0}, {'customer': 'HDB Design Group, LLC.', 'revenue': 1455.0}, {'customer': 'Direct Supply Inc.', 'revenue': 1455.0}, {'customer': 'Robert Trotman Interior Design Inc', 'revenue': 1395.0}, {'customer': 'Desert Point, LLC c/o Blu Canyon', 'revenue': 1370.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 1282.0}, {'customer': 'Clutch Procurement & Consulting, LLC', 'revenue': 1230.0}, {'customer': 'Studio B Design Group', 'revenue': 1230.0}, {'customer': 'Furniture Solutions Group', 'revenue': 1230.0}, {'customer': 'T. Moscone & Bros. Landscaping Ltd.', 'revenue': 1167.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 1131.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1104.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1100.0}, {'customer': 'Papago Golf Course c/o RealFood/Troon Golf', 'revenue': 1080.0}, {'customer': 'Rattan Wicker & Cane', 'revenue': 959.0}, {'customer': "Bishop's Casual Living", 'revenue': 948.0}, {'customer': 'Outdoor Rooms Without Walls', 'revenue': 940.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 937.0}, {'customer': 'STCH, LLC c/o Blu Canyon (as agent)', 'revenue': 936.0}, {'customer': 'Sunset Home and Patio', 'revenue': 933.0}, {'customer': 'Patio Productions', 'revenue': 924.0}, {'customer': 'Keca International', 'revenue': 895.0}, {'customer': 'Wicker Land Patio - Victoria', 'revenue': 895.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 877.0}, {'customer': 'Model Home Interiors Inc', 'revenue': 864.0}, {'customer': "Today's Patio", 'revenue': 864.0}, {'customer': 'IDM Development, LLC', 'revenue': 840.0}, {'customer': 'Guerard Furniture Co Ltd', 'revenue': 836.0}, {'customer': 'Cincinnati Pool & Patio', 'revenue': 787.0}, {'customer': 'Abacus Furniture', 'revenue': 768.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 766.0}, {'customer': 'MOI Inc.', 'revenue': 765.0}, {'customer': 'Design Collaborative, Inc.', 'revenue': 765.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 719.0}, {'customer': 'InnVest Hotels Limited', 'revenue': 715.0}, {'customer': 'Kevin Roberts Interiors', 'revenue': 690.0}, {'customer': 'InterMountain Renovations LLC', 'revenue': 690.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 690.0}, {'customer': 'Madeleine Design Group Inc.', 'revenue': 658.0}, {'customer': 'Shop the Studio at Design Mart', 'revenue': 647.0}, {'customer': 'VAI Resort, LLC', 'revenue': 615.0}, {'customer': 'Commonwealth Design Group', 'revenue': 615.0}, {'customer': 'All Backyard Fun', 'revenue': 552.0}, {'customer': 'Collective Design + Furnishings', 'revenue': 540.0}, {'customer': 'Office Revolution LLC', 'revenue': 540.0}, {'customer': 'C.S. Wo & Sons, Ltd', 'revenue': 537.0}, {'customer': 'Piscine Hippocampe', 'revenue': 527.0}, {'customer': 'GST Interiors, LLC', 'revenue': 521.0}, {'customer': "Mio's Furniture Fashions", 'revenue': 497.0}, {'customer': 'Wickertree Holdings Ltd. (Duncan)', 'revenue': 497.0}, {'customer': 'Entreprises H.P. Carignan Inc(mq034', 'revenue': 492.0}, {'customer': 'Charles Eisen & Associates', 'revenue': 492.0}, {'customer': 'Main Street Furniture', 'revenue': 492.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 485.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 469.0}, {'customer': 'Kootenai Moon Wicker & Rattan', 'revenue': 467.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 465.0}, {'customer': 'Metro Appliances (Tulsa)', 'revenue': 453.0}, {'customer': 'Powell River Building Supply Ltd', 'revenue': 443.0}, {'customer': 'East Texas Brick', 'revenue': 443.0}, {'customer': 'Net Retailers LLC', 'revenue': 432.0}, {'customer': 'Backyard Leisure (Beachcomber)', 'revenue': 429.0}, {'customer': 'Valley Ridge Furniture, Ltd', 'revenue': 418.0}, {'customer': 'Veranda Home & Garden Collection', 'revenue': 418.0}, {'customer': 'Patio Comfort', 'revenue': 410.0}, {'customer': 'Shop The Lake Inc.', 'revenue': 397.0}, {'customer': "Bobo's Mogul Mouse Ski & Patio", 'revenue': 394.0}, {'customer': 'St. Lawrence Pools', 'revenue': 389.0}, {'customer': "Sherri's Living Large", 'revenue': 389.0}, {'customer': 'Beachcomber Hot Tubs & Outdoor Living', 'revenue': 367.0}, {'customer': 'Industrial Revolution', 'revenue': 367.0}, {'customer': 'Real Patio Living Llc', 'revenue': 353.0}, {'customer': 'Georgia Patio Inc', 'revenue': 158.0}, {'customer': 'Americasmart Real Estate LLC', 'revenue': 0.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 0.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 0.0}, {'customer': 'Drew Ruesch Interiors', 'revenue': 0.0}, {'customer': 'Mike Moser Studio', 'revenue': 0.0}] | [{'item': 'CU54458', 'desc': 'Lucia Swivel Rocking Arm Chair Cushion (w/button)', 'available': 2}] |
| FN50063ASG | Limo 84inx42in Rect Dining Table W/uh | COL43 | 125,576 | 180 | 11 | — | [{'customer': 'Studio Dwell', 'revenue': 11241.0}, {'customer': 'Heritage Office Furnishings Ltd.', 'revenue': 8250.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 6799.0}, {'customer': 'Hilton Supply Management', 'revenue': 5198.0}, {'customer': 'Lifestyles By Design, Llc.', 'revenue': 4530.0}, {'customer': 'City of Yorba Linda', 'revenue': 4483.0}, {'customer': 'Innvision Hospitality, Inc', 'revenue': 3202.0}, {'customer': 'Sonoma Backyard', 'revenue': 3080.0}, {'customer': 'Hospitality Furnishings & Design Inc', 'revenue': 2450.0}, {'customer': "Selden's Designer Home Furnishings", 'revenue': 2443.0}, {'customer': 'Net Retailers LLC', 'revenue': 2390.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 2250.0}, {'customer': 'B H Allen Building Centre', 'revenue': 2250.0}, {'customer': 'West Coast Lodging c/o Throughline by IIG (agent)', 'revenue': 2228.0}, {'customer': 'Buffalo-Alafaya Asso. LLC dba Homewood Suites', 'revenue': 2228.0}, {'customer': 'Club Piscine (Terrebonne)', 'revenue': 2125.0}, {'customer': 'Wicker Land Patio (Calgary)', 'revenue': 2125.0}, {'customer': 'Beachcomber (Coquitlam)', 'revenue': 2098.0}, {'customer': 'Williams All Seasons Co.', 'revenue': 1945.0}, {'customer': 'Complete Office LLC', 'revenue': 1800.0}, {'customer': 'Florida Furniture and Patio LLC', 'revenue': 1684.0}, {'customer': 'Homewood Suites By Hilton Covington', 'revenue': 1634.0}, {'customer': 'JM Hospitality Solutions, LLC', 'revenue': 1634.0}, {'customer': 'Tharaldson Hospitality Development, LLC', 'revenue': 1634.0}, {'customer': 'Christina River Exchange', 'revenue': 1614.0}, {'customer': 'Club Piscine Quebec C.P.P.Q. Inc', 'revenue': 1584.0}, {'customer': 'Country Furniture', 'revenue': 1500.0}, {'customer': 'Homewood Mt Pleasant C/O Linked Hospitality', 'revenue': 1485.0}, {'customer': 'Insideout Home & Patio (Woodbridge)', 'revenue': 1436.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 1417.0}, {'customer': 'Studio Six 5, Inc.', 'revenue': 1358.0}, {'customer': 'Aegis Senior Communities, Llc', 'revenue': 1358.0}, {'customer': 'Hue Design LLC', 'revenue': 1358.0}, {'customer': 'Cash Account', 'revenue': 1250.0}, {'customer': 'Orangeville Furniture & Bedding Inc', 'revenue': 1250.0}, {'customer': 'Patio Productions', 'revenue': 1195.0}, {'customer': 'Authenteak Outdoor Living', 'revenue': 1195.0}, {'customer': 'Bobby Design Inc.', 'revenue': 1042.0}, {'customer': 'Isidore Landscapes Inc.', 'revenue': 1042.0}, {'customer': 'JML/Toiles GR Inc.', 'revenue': 833.0}, {'customer': 'MV Design Studio', 'revenue': 817.0}, {'customer': 'Furniture Industries, Inc.', 'revenue': 817.0}, {'customer': 'Synergy Design & Procurement LLC', 'revenue': 817.0}, {'customer': 'Island Hospitality Management Inc', 'revenue': 817.0}, {'customer': 'Homewood Suites By Hilton Boston', 'revenue': 817.0}, {'customer': 'Design and Construction, Llc c/o The Gettys Group', 'revenue': 817.0}, {'customer': 'DCG Development c/o ACC Design, Inc (Agent)', 'revenue': 817.0}, {'customer': 'Curve Hospitality', 'revenue': 817.0}, {'customer': 'Sourcing Advisors LLC c/o Sourcing Advisor', 'revenue': 817.0}, {'customer': 'Germain Lariviere (1970) Ltee.', 'revenue': 792.0}, {'customer': 'Luxe Furniture Company', 'revenue': 773.0}, {'customer': 'Crystalview', 'revenue': 750.0}, {'customer': "Sherri's Living Large", 'revenue': 750.0}, {'customer': 'Design Therapy Inc', 'revenue': 750.0}, {'customer': 'Patio & Home Direct', 'revenue': 750.0}, {'customer': "Bishop's Casual Living", 'revenue': 750.0}, {'customer': 'Decked Out Home & Patio', 'revenue': 750.0}, {'customer': 'Kathy Andrews Interiors, Inc.', 'revenue': 747.0}, {'customer': 'Studio 4d', 'revenue': 747.0}, {'customer': 'HSI Design Group', 'revenue': 743.0}, {'customer': 'PHG Jackson II, LLC c/o Carver & Asso (Atlanta)', 'revenue': 743.0}, {'customer': 'Dwellings, Llc', 'revenue': 743.0}, {'customer': 'GP Builders, Inc.', 'revenue': 743.0}, {'customer': 'Metro Appliances & More (lowell)', 'revenue': 720.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 708.0}, {'customer': 'Beachcomber Hot Tubs & Outdoor Living', 'revenue': 708.0}, {'customer': 'Kora Home Artistry', 'revenue': 679.0}, {'customer': 'The Fireplace Center & Patio Shop', 'revenue': 667.0}, {'customer': 'All American Pool & Patio', 'revenue': 598.0}, {'customer': 'Fruehaufs Patio & Garden', 'revenue': 598.0}, {'customer': 'The Patio Place Inc', 'revenue': 598.0}, {'customer': 'Home Stuff Interiors, Inc', 'revenue': 543.0}, {'customer': 'Canadian Home Leisure', 'revenue': 417.0}, {'customer': "Bowman's Stove & Patio Inc.", 'revenue': 324.0}, {'customer': "Hayward's Of Santa Barbara Inc.", 'revenue': 269.0}, {'customer': 'Sequoia Outback', 'revenue': 245.0}, {'customer': 'BPR Properties c/o Carver and Asso, Atlanta(agent)', 'revenue': 0.0}, {'customer': 'JSM Procurement LLC', 'revenue': 0.0}, {'customer': 'Powers Sourcing Inc', 'revenue': 0.0}, {'customer': 'Carver & Associates', 'revenue': 0.0}, {'customer': 'Homewood Suites-Liverpool, NY c/o HPD(as agent)', 'revenue': 0.0}] | [{'item': 'FN50042TAU', 'desc': 'Limo 30inx60in Rect Counter Table W/uh (HGI)', 'available': 31}, {'item': 'FN50042TWH', 'desc': 'Limo 30inx60in Rect Counter Table W/uh', 'available': 22}, {'item': 'FN50042ASG', 'desc': 'Limo 30inx60in Rect Counter Table W/uh', 'available': 18}, {'item': 'FN50032TWH', 'desc': 'Limo 60in Sq Dining Table W/uh', 'available': 17}, {'item': 'FN50033TWH', 'desc': 'Limo 30inx60in Rect Bar Table W/uh', 'available': 16}, {'item': 'FN50047TWH', 'desc': 'Limo Bench', 'available': 13}, {'item': 'FN50047TWH-L', 'desc': 'Limo Bench (long)', 'available': 13}, {'item': 'FN50036TWH', 'desc': 'Limo 43in Sq Dining Table W/uh', 'available': 11}, {'item': 'FN50063TWH', 'desc': 'Limo 84inx42in Rect Dining Table W/uh', 'available': 8}, {'item': 'FN50047ASG', 'desc': 'Limo Bench', 'available': 6}, {'item': 'FN50066TWH', 'desc': 'Limo 103inx43in Rect Dining Table w/UH', 'available': 4}, {'item': 'FN50047ASG-L', 'desc': 'Limo Bench (long)', 'available': 1}] |
| FN65520WHT | Avenue Lounger | COL145 | 124,576 | 185 | 7 | 2026-6-30 | [{'customer': 'Ellie Aiello Interiors', 'revenue': 23102.0}, {'customer': 'American Cruise Lines, Inc.', 'revenue': 14167.0}, {'customer': 'The Childs Dreyfus Group', 'revenue': 12601.0}, {'customer': 'Richland Bldg. Partners,LLC c/o The Gettys(agent)', 'revenue': 10781.0}, {'customer': 'Group 4 Design, Inc.', 'revenue': 9801.0}, {'customer': 'Net Retailers LLC', 'revenue': 8007.0}, {'customer': 'Kerry Imagine Designs Llc', 'revenue': 6160.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 3920.0}, {'customer': 'Canadian Resort Hotels Ltd Partner.c/o Sue Dulmage', 'revenue': 3500.0}, {'customer': 'The Patio Place USA, Inc', 'revenue': 3102.0}, {'customer': 'Outdoor Living LLC', 'revenue': 2688.0}, {'customer': 'F.E.K. Enterprises Inc.', 'revenue': 2520.0}, {'customer': 'Country Furniture', 'revenue': 2520.0}, {'customer': 'Zing Quality Furniture Inc', 'revenue': 2464.0}, {'customer': 'All American Pool & Patio', 'revenue': 2464.0}, {'customer': 'MTN Mod LLC', 'revenue': 2464.0}, {'customer': 'Wicker Land Patio (Kelowna)', 'revenue': 2380.0}, {'customer': 'Southport Outdoor Living', 'revenue': 2100.0}, {'customer': 'Treasure Chest LLC', 'revenue': 1540.0}, {'customer': 'Distinctive Designs by Bambi', 'revenue': 1400.0}, {'customer': 'Light House Co.', 'revenue': 1400.0}, {'customer': 'B H Allen Building Centre', 'revenue': 1260.0}, {'customer': 'Keca International', 'revenue': 1190.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 1120.0}, {'customer': 'Backyard Supplies Atlantic', 'revenue': 665.0}, {'customer': 'Crystalview', 'revenue': 630.0}, {'customer': 'Vancouver Sofa & Patio', 'revenue': 630.0}] | [{'item': 'FN65505WHT', 'desc': 'Avenue Side Table', 'available': 27}, {'item': 'FN65505BLK', 'desc': 'Avenue Side Table', 'available': 24}] |
| UM00907BRZ/C | 9' Alum W/fiberglass Ribs,pulley,2 Poles W/canopy | COL73 | 121,687 | 333 | 31 | — | [{'customer': 'Le Chateau Montebello, Evergrande Hotel Hold', 'revenue': 26102.0}, {'customer': 'Les Fabrication Dor-val Ltee', 'revenue': 14405.0}, {'customer': 'Embarc Members Association', 'revenue': 11230.0}, {'customer': 'Urban Design Studio', 'revenue': 8392.0}, {'customer': 'Interior Motives', 'revenue': 7122.0}, {'customer': 'Shaughnessy Golf And Country Club', 'revenue': 4976.0}, {'customer': 'Country Furniture', 'revenue': 4190.0}, {'customer': 'Williams Group', 'revenue': 3749.0}, {'customer': 'Elite Contract Furniture Ltd', 'revenue': 3553.0}, {'customer': "Les Plantes D'interieur Veronneau", 'revenue': 3480.0}, {'customer': 'Hampton Inn Phoenix/Anthem', 'revenue': 3450.0}, {'customer': 'Northwest Trends', 'revenue': 3345.0}, {'customer': 'Stevans Sales And Marketing Inc.', 'revenue': 3303.0}, {'customer': 'Evercare Contract Furnishings Inc.', 'revenue': 3215.0}, {'customer': 'Era Living LLC', 'revenue': 3209.0}, {'customer': 'Terminal City Club', 'revenue': 3045.0}, {'customer': 'Embarc Members Association', 'revenue': 2610.0}, {'customer': 'RTJ Coastal Living Inc', 'revenue': 2117.0}, {'customer': 'Kerry Imagine Designs Llc', 'revenue': 1783.0}, {'customer': 'Hue Design LLC', 'revenue': 1586.0}, {'customer': 'Sechrist Design Associates, Inc.', 'revenue': 1550.0}, {'customer': 'Harris Furniture & Antiques Inc.', 'revenue': 1044.0}, {'customer': 'Faulkner Design Group, Inc.', 'revenue': 690.0}, {'customer': 'Absolute Procurement Llc', 'revenue': 690.0}, {'customer': 'Homey Home', 'revenue': 435.0}, {'customer': 'Cardinal Design and Procurement', 'revenue': 385.0}, {'customer': 'Atmosphere Commercial Interiors', 'revenue': 345.0}, {'customer': 'Le Club Piscine Plus C.P.P.Q. (West Island) Inc', 'revenue': 331.0}, {'customer': 'Patio & Home Direct', 'revenue': 326.0}, {'customer': 'Casual Patio Of The Palm Beaches', 'revenue': 323.0}, {'customer': 'Starland Property Co, LLC', 'revenue': 300.0}, {'customer': 'Club Piscines Sherbrooke', 'revenue': 206.0}, {'customer': 'Intown Ace Hardware', 'revenue': 200.0}, {'customer': 'Montage Hotels & Resorts', 'revenue': 0.0}, {'customer': 'Bristal Design Group, Inc', 'revenue': 0.0}, {'customer': 'The University of British Columbia', 'revenue': 0.0}] | [{'item': 'UM01010SLV-CCL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Cloud canopy", 'available': 10}, {'item': 'UM01010SLV-CBL', 'desc': "10' Sq Cantilever Umbrella w/Canvas Black canopy", 'available': 9}, {'item': 'UM01004SLV/C', 'desc': "10' Sq Deluxe Alum Umbrella, 48mm Pole W/canopy", 'available': 8}, {'item': 'UM00906BRZ/C', 'desc': "9' Alum W/fiber Ribs,crank Lift,collar Tilt,canopy", 'available': 6}, {'item': 'UM00909POLE-BRZ', 'desc': '45in Bar Bottom Pole for UM00906BRZ/C', 'available': 5}] |
