# Section 2 Context Bundle — Kalco Lighting / Allegri Crystal (kal)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | True | recurring_services contains B2B Cart: True |
| HAS_PORTAL_ORDERS | True | portal_order_count=10066, portal_order_gmv=$11.7M |
| HAS_INVENTORY | True | inventory_count=2267 |
| HAS_SALES_DATA | True | sales_data_count=50129 |
| HAS_SALES_SECTION | True | qualifying_reps=6 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$11.7M > ecat_gmv=$2.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 6 | 6 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 79 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 197, Mixpanel total submit_order (Q-01): 266 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=78.5%, ambiguous_rate=0.0%, showroom_event_share=13.8% |
| USER_GROUP_JOIN_RATE | 78% | 62 of 79 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 14% | showroom+admin share of matched events: 13.8% |
| ADMIN_REPS_IN_LEADERBOARD | True | 3 admin/showroom users in leaderboard: Bob Ross, Claudia Carrillo, Snehal Shah |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=42 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=818 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=400 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=49 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Kalco Lighting / Allegri Crystal
- **Shortname**: kal
- **Org ID**: 146
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Kalco Lighting / Allegri Crystal (kal, org_id=146)
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

# Signal Rank — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Run date**: 2026-06-17
- **Total signals fired**: 53 (P0: 38, P1: 13, P2: 2)
- **Org GMV**: $2.6M eCat LTM, $11.7M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $6.3M total business | P1 | §5 Team | 31.5 | $6,290,391 | 2.0 | 395,690,189 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — 505840OL/505851OL co-purchase pattern across 37 customers | P0 | §2/§3 | 3.7 | $9,098,327 | 2.0 | 67,327,623 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 14 non-enterprise accounts with $3.0M+ total business, zero eCat orders | P1 | §2 Accounts | 3.0 | $2,958,738 | 2.0 | 17,508,261 | POSITIVE |
| 4 | SIG-ANOMALY-02 | Stock Out — 519275WB (Flint 5 Light Multi-Drop Pendant) $583,128 LTM, 0 available | P0 | §3 Product | 10.0 | $583,128 | 3.0 | 17,493,825 | RISK |
| 5 | SIG-MOM-01 | Account Acceleration — CLIVE DANIEL HOME 2 consecutive QoQ acceleration quarters, $258,074 peak quarter (+597% QoQ) | P0 | §2 Accounts | 19.9 | $258,074 | 3.0 | 15,401,841 | POSITIVE |
| 6 | SIG-DECAY-04 | Spending Contraction — DOLAN NORTHWEST LLC  PORTLAND -77.1% YoY ($520,864→$119,130), $401,733 gap | P0 | §2 Accounts | 3.9 | $401,733 | 3.0 | 4,646,047 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 515155OL (Samal 21 Inch Pendant) $124,925 LTM, 0 available | P0 | §3 Product | 10.0 | $124,925 | 3.0 | 3,747,747 | RISK |
| 8 | SIG-MOM-01 | Account Acceleration — LUX LIGHTING LTD 2 consecutive QoQ acceleration quarters, $56,060 peak quarter (+651% QoQ) | P0 | §2 Accounts | 21.7 | $56,060 | 3.0 | 3,647,231 | POSITIVE |
| 9 | SIG-MOM-01 | Account Acceleration — Lighting Design Center 2 consecutive QoQ acceleration quarters, $48,568 peak quarter (+693% QoQ) | P0 | §2 Accounts | 23.1 | $48,568 | 3.0 | 3,367,705 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — VALLEY LGT GALLERY 3 consecutive QoQ acceleration quarters, $83,209 peak quarter (+331% QoQ) | P0 | §2 Accounts | 11.0 | $83,209 | 3.0 | 2,756,711 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — 030257-038 (Glacier 60 Inch LED Round Pendant) $90,966 LTM, 0 available | P0 | §3 Product | 10.0 | $90,966 | 3.0 | 2,728,986 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 519221WB (Flint 1 Light Led  Convertible Wall Scon) $86,699 LTM, 0 available | P0 | §3 Product | 10.0 | $86,699 | 3.0 | 2,600,974 | RISK |
| 13 | SIG-MOM-01 | Account Acceleration — SUNBELT FANS & LTG LAUREL 3 consecutive QoQ acceleration quarters, $29,018 peak quarter (+671% QoQ) | P0 | §2 Accounts | 22.4 | $29,018 | 3.0 | 1,946,261 | POSITIVE |
| 14 | SIG-ANOMALY-02 | Stock Out — 505820OL (Roxy 2 Light ADA Sconce) $63,294 LTM, 0 available | P0 | §3 Product | 10.0 | $63,294 | 3.0 | 1,898,819 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — 519276WB (Flint 3 Light Full Canopy Pendant) $61,716 LTM, 0 available | P0 | §3 Product | 10.0 | $61,716 | 3.0 | 1,851,473 | RISK |
| 16 | SIG-DECAY-01 | Reorder Decay — SPACIAL EFX 3.7x normal gap (111d vs 30d avg) | P0 | §2 Accounts | 3.7 | $152,319 | 3.0 | 1,690,741 | RISK |
| 17 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 61% of eCat GMV | P1 | §4 Commerce | 1.5 | $528,750 | 2.0 | 1,611,251 | RISK |
| 18 | SIG-DECAY-04 | Spending Contraction — SHADES OF LIGHT -50.9% YoY ($401,435→$197,145), $204,290 gap | P0 | §2 Accounts | 2.5 | $204,290 | 3.0 | 1,559,754 | RISK |
| 19 | SIG-COMMERCE-01 | Capture Rate — eCat captures 22.2% of $12M total business; each +1pt = $117K | P0 | §4 Commerce | 3.9 | $117,000 | 3.0 | 1,365,000 | POSITIVE |
| 20 | SIG-ANOMALY-02 | Stock Out — 520555OL (Crescent 6 Light Pendant) $45,102 LTM, 0 available | P0 | §3 Product | 10.0 | $45,102 | 3.0 | 1,353,064 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 29 | 1 | 0 | 30 | |
| §3 Product Intelligence | 8 | 0 | 1 | 9 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 10 | 1 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 5 reps at 0% eCat capture on $6.3M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 505840OL/505851OL co-purchase pattern across 37 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 14 non-enterprise accounts with $3.0M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — CLIVE DANIEL HOME 2 consecutive QoQ acceleration quarters, $258,074 peak quarter (+597% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 519275WB (Flint 5 Light Multi-Drop Pendant) $583,128 LTM, 0 available
6. **[RISK]** SIG-DECAY-04: Spending Contraction — DOLAN NORTHWEST LLC  PORTLAND -77.1% YoY ($520,864→$119,130), $401,733 gap
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 515155OL (Samal 21 Inch Pendant) $124,925 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | LUX LIGHTING LTD | 2 | DECAY-04, MOM-01 | $96,505 |
| 2 | DESIGNER LIGHTING & FAN | 2 | ANOMALY-03, MOM-01 | $55,467 |
| 3 | SPACIAL EFX | 1 | DECAY-01 | $152,319 |
| 4 | DOLAN NORTHWEST LLC  PORTLAND | 1 | DECAY-04 | $401,733 |
| 5 | SHADES OF LIGHT | 1 | DECAY-04 | $204,290 |
| 6 | LAMPS PLUS | 1 | DECAY-04 | $117,394 |
| 7 | LIGHTING NEW YORK (INTERNET) | 1 | DECAY-04 | $112,365 |
| 8 | LIGHTING WORLD DECORATOR | 1 | DECAY-04 | $35,553 |
| 9 | CAPITOL LIGHTING--E. HANOVER | 1 | DECAY-04 | $34,536 |
| 10 | LIGHTSTYLE OF ORLANDO | 1 | DECAY-04 | $30,601 |

### Q-12_results.md

# Q-12 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 2,245 | 408 | 87 | 58 | 10 |

### Q-14_results.md

# Q-14 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 17
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 0000053 | SPACIAL EFX | 11 | $152,319 | 2025-10-25 20:17:11 | 2026-02-25 20:43:20 | 12.30 |
| 0005517 | LBX LIGHTING INC | 7 | $90,995 | 2025-06-19 15:39:42 | 2025-10-16 19:34:20 | 19.90 |
| 0010023 | FEI  FERGUSON MAIN ACCOUNT | 6 | $95,890 | 2025-06-27 20:38:05 | 2026-02-11 14:05:43 | 45.70 |
| 0001015 | LIGHTING INC | 6 | $105,057 | 2025-06-27 12:35:19 | 2026-03-11 14:04:06 | 51.40 |
| 0010939 | D+D HOME INTERIORS | 4 | $8,446 | 2025-07-07 19:01:12 | 2026-06-09 21:28:14 | 112.40 |
| 0010424 | LIGHT & DAY LLC | 4 | $25,334 | 2025-09-23 11:24:23 | 2025-10-25 20:51:00 | 10.80 |
| 0011284 | AMY LYNN INTERIORS LLC | 4 | $7,081 | 2025-09-15 19:05:21 | 2026-05-26 16:46:27 | 84.30 |
| 0006139 | WATSON & CO. | 4 | $4,012 | 2025-10-17 20:05:10 | 2026-01-29 18:22:58 | 34.60 |
| 0010157 | J DOUGLAS DESIGN | 4 | $6,887 | 2025-07-29 19:38:57 | 2025-12-03 17:14:16 | 42.30 |
| 0010118 | GEORGIAN LIGHTING GALERY INC | 4 | $8,604 | 2025-08-17 15:40:38 | 2026-06-09 17:15:15 | 98.70 |
| 0006205 | KASA INTERIORS JUAN CARLOS IBA | 3 | $17,799 | 2025-07-27 19:44:52 | 2025-07-29 19:21:44 | 1 |
| 0000060 | MCCARTY SALES & ASSOCIATES | 3 | $1,324 | 2025-09-05 15:00:00 | 2026-03-06 21:13:31 | 91.10 |
| 0002241 | PARK LIGHTING | 3 | $17,913 | 2025-06-20 13:22:21 | 2026-01-09 17:06:08 | 101.60 |
| 0003285 | LIGHTSTYLE OF ORLANDO | 3 | $2,554 | 2025-07-23 18:44:23 | 2025-07-23 18:47:33 | 0 |
| 0000011 | KIRK MARSHALL SALES | 3 | $1,599 | 2025-10-03 17:25:06 | 2026-02-11 15:12:13 | 65.50 |
| 0010803 | ROCKING MOUNTAIN DESIGN | 3 | $2,378 | 2025-08-12 18:39:15 | 2026-01-14 17:29:28 | 77.50 |
| 0011052 | HOWARTH HADDOCK DESIGN LLP | 3 | $1,958 | 2026-02-10 20:23:19 | 2026-04-28 16:17:27 | 38.40 |

### Q-14b_results.md

# Q-14b Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 0005575 | CAPITOL LIGHTING / 1-800LIGHTI | 550 | 0.90 | 1.40 | 1.56 | $181,361 |
| 0002855 | BEAUTIFUL THINGS LIGHTING | 60 | 7.80 | 12.10 | 1.55 | $74,004 |
| 0003476 | LUX LIGHTING LTD | 9 | 29.20 | 96 | 3.29 | $70,219 |
| 0006064 | LIGHTOPIA, LLC | 162 | 2.80 | 5 | 1.79 | $68,180 |
| 0002233 | FRANKLIN LIGHTING INC | 65 | 7 | 11.10 | 1.59 | $57,896 |
| 0005517 | LBX LIGHTING INC | 25 | 15.10 | 41 | 2.72 | $49,183 |
| 0010671 | BISONOFFICE LLC | 150 | 2.70 | 7.90 | 2.93 | $45,883 |
| 0005391 | NAPLES LIGHTING & FAN DEPOT | 47 | 9.70 | 16.80 | 1.73 | $42,657 |
| 0002608 | LIGHTING SUPERSTORE | 48 | 8.70 | 14.50 | 1.67 | $37,417 |
| 0001422 | LIGHTING EMPORIUM | 34 | 12.40 | 22.60 | 1.82 | $36,123 |
| 0001859 | RAY ELECTRIC | 61 | 6.40 | 23.90 | 3.73 | $32,065 |
| 0005675 | EUROPEAN CUSTOM LIGHTING | 10 | 36.90 | 98.50 | 2.67 | $31,617 |
| 0010457 | IB LIGHTING SUPPLY | 22 | 20.10 | 32.80 | 1.63 | $30,266 |
| 0011196 | TRADITION DE FRANCE | 5 | 27.30 | 164.50 | 6.03 | $29,445 |
| 0002301 | LIGHTING FIRST | 34 | 12.90 | 21 | 1.63 | $29,288 |

### Q-17_results.md

# Q-17 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 0000053 | SPACIAL EFX | MD | 2026-02-25 20:43:20 | 11 | $152,319 |
| 0001015 | LIGHTING INC | TX | 2026-03-11 14:04:06 | 6 | $105,057 |
| 0010023 | FEI  FERGUSON MAIN ACCOUNT | VA | 2026-02-11 14:05:43 | 6 | $95,890 |
| 0005517 | LBX LIGHTING INC | TX | 2025-10-16 19:34:20 | 7 | $90,995 |
| 0000967 | VALLEY LGT GALLERY | AZ | 2026-01-19 12:46:45 | 1 | $84,489 |
| 0003476 | LUX LIGHTING LTD | GA | 2025-12-17 22:24:01 | 2 | $67,288 |
| 0001580 | HERMITAGE ELECTRIC SUPPLY | TN | 2025-10-15 18:47:51 | 2 | $45,214 |
| 0006114 | VP SUPPLY CORP | NY | 2025-08-25 22:08:15 | 2 | $44,820 |
| 0000831 | CAROL'S LIGHTING | TX | 2026-01-27 15:33:14 | 1 | $32,526 |
| 0006119 | LUXURY FURNITURE INC. DBA VENICASA | FL | 2025-06-26 15:40:19 | 1 | $31,412 |
| 0010424 | LIGHT & DAY LLC | MD | 2025-10-25 20:51:00 | 4 | $25,334 |
| 0002274 | CAPITOL LIGHTING BOCA RATON | FL | 2025-06-26 16:12:47 | 1 | $25,108 |
| 0005299 | RBDELAA LIGHTING | NY | 2026-01-12 17:42:31 | 1 | $23,495 |
| 0006162 | SOVEREIGN INTERIORS PTY. LTD. | QU | 2025-09-17 05:27:51 | 2 | $23,208 |
| 0002052 | CARRINGTON LIGHTING | AB | 2026-01-11 14:45:05 | 2 | $20,421 |
| 0005489 | FISCHER-GAMBINO | LA | 2026-01-13 13:26:44 | 1 | $19,792 |
| 0010820 | HAJOCA CORPORATION | MA | 2026-01-12 20:27:05 | 1 | $18,911 |
| 0002241 | PARK LIGHTING | AB | 2026-01-09 17:06:08 | 3 | $17,913 |
| 0006205 | KASA INTERIORS JUAN CARLOS IBA | MX | 2025-07-29 19:21:44 | 3 | $17,799 |
| 0002745 | HOME LIGHTING OF PA | PA | 2025-11-04 15:54:23 | 1 | $16,832 |
| 0001228 | M & M LIGHTING LP | TX | 2026-02-04 05:36:59 | 1 | $15,572 |
| 0002067 | PINE GROVE ELEC'L SPL INC | LA | 2026-01-10 21:53:56 | 1 | $15,452 |
| 0005679 | PINE LIGHTING LTD | BC | 2026-01-10 03:18:45 | 1 | $14,474 |
| 0011196 | TRADITION DE FRANCE | VA | 2026-03-16 22:31:38 | 2 | $14,435 |
| 0006136 | LAMP SHOP OF NAPLES COMPANY | FL | 2025-06-26 15:41:34 | 1 | $13,862 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 0000053 | SPACIAL EFX | MD | $152,319 | 2026-02-25 20:43:20 | 111 |
| 0001015 | LIGHTING INC | TX | $105,057 | 2026-03-11 14:04:06 | 97 |
| 0010023 | FEI  FERGUSON MAIN ACCOUNT | VA | $95,890 | 2026-02-11 14:05:43 | 125 |
| 0005517 | LBX LIGHTING INC | TX | $90,995 | 2025-10-16 19:34:20 | 243 |
| 0000967 | VALLEY LGT GALLERY | AZ | $84,489 | 2026-01-19 12:46:45 | 148 |
| 0003476 | LUX LIGHTING LTD | GA | $67,288 | 2025-12-17 22:24:01 | 181 |
| 0001580 | HERMITAGE ELECTRIC SUPPLY | TN | $45,214 | 2025-10-15 18:47:51 | 244 |
| 0006114 | VP SUPPLY CORP | NY | $44,820 | 2025-08-25 22:08:15 | 295 |
| 0000831 | CAROL'S LIGHTING | TX | $32,526 | 2026-01-27 15:33:14 | 140 |
| 0006119 | LUXURY FURNITURE INC. DBA VENICASA | FL | $31,412 | 2025-06-26 15:40:19 | 355 |
| 0010424 | LIGHT & DAY LLC | MD | $25,334 | 2025-10-25 20:51:00 | 234 |
| 0002274 | CAPITOL LIGHTING BOCA RATON | FL | $25,108 | 2025-06-26 16:12:47 | 355 |
| 0005299 | RBDELAA LIGHTING | NY | $23,495 | 2026-01-12 17:42:31 | 155 |
| 0006162 | SOVEREIGN INTERIORS PTY. LTD. | QU | $23,208 | 2025-09-17 05:27:51 | 273 |
| 0002052 | CARRINGTON LIGHTING | AB | $20,421 | 2026-01-11 14:45:05 | 156 |
| 0005489 | FISCHER-GAMBINO | LA | $19,792 | 2026-01-13 13:26:44 | 154 |
| 0010820 | HAJOCA CORPORATION | MA | $18,911 | 2026-01-12 20:27:05 | 155 |
| 0002241 | PARK LIGHTING | AB | $17,913 | 2026-01-09 17:06:08 | 158 |
| 0006205 | KASA INTERIORS JUAN CARLOS IBA | MX | $17,799 | 2025-07-29 19:21:44 | 322 |
| 0002745 | HOME LIGHTING OF PA | PA | $16,832 | 2025-11-04 15:54:23 | 224 |

### Q-40_results.md

# Q-40 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| TX | 10 | 24 | $289,135 |
| MD | 3 | 17 | $178,577 |
| FL | 10 | 14 | $113,146 |
| VA | 2 | 8 | $110,325 |
| GA | 7 | 14 | $95,972 |
| AZ | 2 | 2 | $90,759 |
| NY | 4 | 5 | $73,527 |
| AB | 4 | 7 | $58,136 |
| TN | 3 | 4 | $51,979 |
| LA | 3 | 3 | $39,548 |
| UT | 4 | 6 | $33,530 |
| MA | 2 | 5 | $25,992 |
| QU | 1 | 2 | $23,208 |
| PA | 2 | 2 | $19,040 |
| MX | 1 | 3 | $17,799 |
| CA | 3 | 4 | $17,426 |
| BC | 1 | 1 | $14,474 |
| NJ | 2 | 2 | $11,731 |
| NC | 2 | 2 | $9,934 |
| SC | 2 | 3 | $8,674 |

### Q-41_results.md

# Q-41 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 19
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 3 |
| 2025-04-01 | Rep-Acquired (iPad) | 2 |
| 2025-06-01 | Rep-Acquired (iPad) | 8 |
| 2025-07-01 | Rep-Acquired (iPad) | 2 |
| 2025-08-01 | eCat Online-Acquired (self-serve) | 1 |
| 2025-09-01 | Rep-Acquired (iPad) | 3 |
| 2025-10-01 | Rep-Acquired (iPad) | 2 |
| 2025-11-01 | eCat Online-Acquired (self-serve) | 2 |
| 2025-12-01 | Rep-Acquired (iPad) | 1 |
| 2025-12-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 8 |
| 2026-02-01 | Rep-Acquired (iPad) | 3 |
| 2026-02-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-03-01 | Rep-Acquired (iPad) | 1 |
| 2026-03-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-04-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-05-01 | Rep-Acquired (iPad) | 1 |
| 2026-05-01 | eCat Online-Acquired (self-serve) | 1 |
| 2026-06-01 | eCat Online-Acquired (self-serve) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Scott Fellner | 4 |
| Kirk Marshall | 4 |
| Jenifer McCarty | 4 |
| Claudia Carrillo | 2 |
| Cheryl LaRosa | 2 |
| Lindsey Olsen | 2 |
| Robert Parker | 2 |
| Shawna Meshwork | 2 |
| Rob Azimi | 1 |
| Snehal Shah | 1 |
| Tom Wright | 1 |
| Albert Maldonado | 1 |
| Zachary Rapp | 1 |
| Alton Mckey | 1 |
| Amin Khan | 1 |
| DBA Associates | 1 |
| Doeren Sales | 1 |
| Jason Steele | 1 |
| Keya Mistry | 1 |
| Riki Lent | 1 |

### Q-52_results.md

# Q-52 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0010023 | FEI  FERGUSON MAIN ACCOUNT | VA | 590 | $652,848 | 6 | $95,890 | 14.70 |
| 0003937 | LUMENS LIGHT & LIVING | CA | 699 | $523,844 | 0 | $0 | 0 |
| 0004575 | BUILD.COM | CA | 692 | $448,622 | 0 | $0 | 0 |
| 0004961 | LIGHTING NEW YORK (INTERNET) | PA | 511 | $377,166 | 0 | $0 | 0 |
| 0010558 | CLIVE DANIEL HOME | FL | 29 | $329,862 | 0 | $0 | 0 |
| 0001416 | LAMPS PLUS | CA | 468 | $303,121 | 0 | $0 | 0 |
| 0005456 | WAYFAIR LLC | MA | 541 | $282,361 | 0 | $0 | 0 |
| 0005685 | LIGHTOLOGY LLC | IL | 219 | $245,901 | 0 | $0 | 0 |
| 0003299 | SHADES OF LIGHT | VA | 79 | $197,145 | 0 | $0 | 0 |
| 0005575 | CAPITOL LIGHTING / 1-800LIGHTI | FL | 340 | $181,361 | 0 | $0 | 0 |
| 0010336 | LIGHT LAB DESIGN | NY | 11 | $174,788 | 0 | $0 | 0 |
| 0002274 | CAPITOL LIGHTING BOCA RATON | FL | 116 | $167,213 | 1 | $25,108 | 15 |
| 0005789 | DESIGNER LIGHTING & FAN/DECOR | NJ | 194 | $164,144 | 0 | $0 | 0 |
| 0001551 | PROGRESSIVE LIGHTING | GA | 125 | $144,782 | 0 | $0 | 0 |
| 0000967 | VALLEY LGT GALLERY | AZ | 45 | $121,050 | 1 | $84,489 | 69.80 |
| 0002321 | DOLAN NORTHWEST LLC  PORTLAND | OR | 56 | $119,130 | 0 | $0 | 0 |
| 0001139 | SOUTHERN LIGHTING INC | MN | 67 | $114,274 | 0 | $0 | 0 |
| 0003006 | LIGHTING WORLD DECORATOR | NY | 115 | $99,822 | 0 | $0 | 0 |
| 0005130 | 1-800-MY-LAMPS | CA | 114 | $99,329 | 0 | $0 | 0 |
| 0011388 | GRUPO INMOBILIARIO SUSTAIN | NL | 3 | $95,469 | 0 | $0 | 0 |
| 0002825 | RAINBOW LIGHTING II LLC | NY | 35 | $86,506 | 0 | $0 | 0 |
| 0004803 | BELAMI, INC / 1STOP LIGHTING | CA | 134 | $84,106 | 0 | $0 | 0 |
| 0004913 | WES ULMO INTERIOR DESIGN | LA | 8 | $83,626 | 0 | $0 | 0 |
| 0001015 | LIGHTING INC | TX | 39 | $74,506 | 6 | $105,057 | 141 |
| 0001802 | HINKLEY'S LTG FACTORY | AZ | 36 | $74,391 | 1 | $6,270 | 8.40 |
| 0000053 | SPACIAL EFX | MD | 12 | $74,289 | 11 | $152,319 | 205 |
| 0002855 | BEAUTIFUL THINGS LIGHTING | FL | 40 | $74,004 | 1 | $11,875 | 16 |
| 0003476 | LUX LIGHTING LTD | GA | 4 | $70,219 | 2 | $67,288 | 95.80 |
| 0006064 | LIGHTOPIA, LLC | CA | 97 | $68,180 | 0 | $0 | 0 |
| 0003014 | Lighting Design Center | NV | 25 | $66,796 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 0003937 | LUMENS LIGHT & LIVING | CA | 699 | $523,844 |
| 0004575 | BUILD.COM | CA | 692 | $448,622 |
| 0004961 | LIGHTING NEW YORK (INTERNET) | PA | 511 | $377,166 |
| 0001416 | LAMPS PLUS | CA | 468 | $303,121 |
| 0005456 | WAYFAIR LLC | MA | 541 | $282,361 |
| 0005685 | LIGHTOLOGY LLC | IL | 219 | $245,901 |
| 0005575 | CAPITOL LIGHTING / 1-800LIGHTI | FL | 340 | $181,361 |
| 0002321 | DOLAN NORTHWEST LLC  PORTLAND | OR | 56 | $119,130 |
| 0005130 | 1-800-MY-LAMPS | CA | 114 | $99,329 |
| 0011388 | GRUPO INMOBILIARIO SUSTAIN | NL | 3 | $95,469 |
| 0004803 | BELAMI, INC / 1STOP LIGHTING | CA | 134 | $84,106 |
| 0004913 | WES ULMO INTERIOR DESIGN | LA | 8 | $83,626 |
| 0010278 | LIGHTING FACTORY OUTLET | NV | 12 | $64,176 |
| 0011345 | LINDSEY GLASS | CA | 3 | $50,526 |
| 0010671 | BISONOFFICE LLC | IL | 98 | $45,883 |
| 0010507 | MI CASA LIGHTING AND FAN | CA | 28 | $45,415 |
| 0011088 | REFLECTIONS L+M | NJ | 8 | $41,846 |
| 0005580 | LIGHTING FIRST - BONITA | FL | 29 | $41,698 |
| 0003388 | COLONIAL ELECTRIC SUPPLY | PA | 35 | $37,458 |
| 0002608 | LIGHTING SUPERSTORE | NJ | 32 | $37,417 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA | 85 | 2,586 | $2.1M | 3 | 4 | $17,426 | 0.80 |
| FL | 108 | 1,249 | $1.7M | 10 | 14 | $113,146 | 6.60 |
| VA | 17 | 734 | $960,618 | 2 | 8 | $110,325 | 11.50 |
| NY | 38 | 346 | $740,221 | 4 | 5 | $73,527 | 9.90 |
| TX | 84 | 442 | $631,308 | 10 | 24 | $289,135 | 45.80 |
| PA | 20 | 597 | $492,412 | 2 | 2 | $19,040 | 3.90 |
| IL | 27 | 500 | $488,182 | 1 | 2 | $988 | 0.20 |
| NJ | 32 | 428 | $462,901 | 2 | 2 | $11,731 | 2.50 |
| GA | 20 | 242 | $351,045 | 7 | 14 | $95,972 | 27.30 |
| MA | 12 | 642 | $336,062 | 2 | 5 | $25,992 | 7.70 |
| AZ | 14 | 148 | $320,556 | 2 | 2 | $90,759 | 28.30 |
| LA | 16 | 89 | $244,632 | 3 | 3 | $39,548 | 16.20 |
| MI | 19 | 166 | $225,132 | 0 | 0 | $0 | 0 |
| NV | 23 | 101 | $217,629 | 0 | 0 | $0 | 0 |
| MN | 9 | 129 | $195,594 | 2 | 2 | $4,736 | 2.40 |
| OR | 5 | 119 | $163,685 | 0 | 0 | $0 | 0 |
| OH | 29 | 135 | $137,483 | 3 | 3 | $6,316 | 4.60 |
| CO | 15 | 113 | $135,604 | 1 | 4 | $4,012 | 3 |
| OK | 9 | 116 | $134,438 | 0 | 0 | $0 | 0 |
| NC | 18 | 125 | $124,414 | 2 | 2 | $9,934 | 8 |

### Q-57_results.md

# Q-57 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

# Q-66 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-66 — Buyer-Within-Account Intelligence
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | new_buyers | existing_buyers | new_buyer_orders | new_buyer_revenue | earliest_new_buyer |
| --- | --- | --- | --- | --- | --- |
| STUDIO 41 | 1 | 0 | 1 | 13,720 | 2026-6-3 |
| COBURN SUPPLY COMPANY | 1 | 0 | 1 | 12,151 | 2026-4-16 |
| BAR 19 TWELVE | 1 | 0 | 1 | 11,047 | 2026-4-28 |
| DEMUTH DESIGNS | 1 | 0 | 2 | 5,922 | 2026-4-17 |
| INSTINCTIVE INTERIORS | 1 | 0 | 2 | 4,934 | 2026-6-10 |
| FOLEY + STINNETE INTERIOR DESI | 1 | 0 | 1 | 4,418 | 2026-6-3 |
| STUDIO B DESIGNS | 1 | 0 | 1 | 4,270 | 2026-4-28 |
| STATEMENT OF STYLE CORPORATION | 1 | 0 | 1 | 4,185 | 2026-4-14 |
| ILLUMINATIONS LIGHTING | 1 | 0 | 1 | 3,624 | 2026-4-29 |
| BERKELEY LIGHTING COMPANY | 1 | 0 | 4 | 3,523 | 2026-5-14 |
| TCOLE.DESIGN | 1 | 0 | 2 | 3,068.70 | 2026-4-28 |
| GROSS ELECTRIC | 1 | 0 | 1 | 2,667 | 2026-4-22 |
| SWITCHED ON DESIGN | 1 | 0 | 1 | 2,209 | 2026-6-16 |
| C NORMAN DESIGNS | 1 | 0 | 1 | 2,208 | 2026-5-26 |
| TREEHOUSE COFFEE & WINE | 1 | 0 | 1 | 2,208 | 2026-6-15 |
| MABRY DESIGN LLC | 1 | 0 | 1 | 2,144 | 2026-4-2 |
| SPK LIGHTING | 1 | 0 | 1 | 2,120 | 2026-4-21 |
| SBS DESIGNS | 1 | 0 | 1 | 1,841 | 2026-4-29 |
| DESIGN SQUARED | 1 | 0 | 1 | 1,841 | 2026-6-9 |
| AGAPE DESIGN GROUP | 1 | 0 | 1 | 1,841 | 2026-4-14 |

### Q-67_results.md

# Q-67 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FL | $562,777 | $787,720 | 40 | 93 | 89 | 4 | 385 |
| TX | $434,453 | $270,384 | -37.80 | 67 | 73 | -6 | 231 |
| NY | $267,122 | $238,444 | -10.70 | 34 | 39 | -5 | 126 |
| CA | $287,788 | $188,196 | -34.60 | 56 | 56 | 0 | 214 |
| AZ | $110,001 | $180,778 | 64.30 | 26 | 23 | 3 | 81 |
| LA | $63,122 | $110,742 | 75.40 | 14 | 12 | 2 | 25 |
| NJ | $141,766 | $101,247 | -28.60 | 37 | 37 | 0 | 106 |
| VA | $130,182 | $87,810 | -32.50 | 18 | 24 | -6 | 58 |
| NV | $39,997 | $81,912 | 104.80 | 16 | 15 | 1 | 43 |
| GA | $95,418 | $80,022 | -16.10 | 27 | 30 | -3 | 81 |
| IL | $73,685 | $74,274 | 0.80 | 27 | 31 | -4 | 80 |
| MN | $59,847 | $69,233 | 15.70 | 16 | 16 | 0 | 57 |
| SC | $93,975 | $66,319 | -29.40 | 27 | 23 | 4 | 47 |
| NC | $52,752 | $65,909 | 24.90 | 25 | 28 | -3 | 92 |
| CO | $55,734 | $55,183 | -1 | 20 | 25 | -5 | 57 |
| TN | $69,641 | $51,616 | -25.90 | 17 | 19 | -2 | 52 |
| UT | $45,431 | $47,466 | 4.50 | 18 | 15 | 3 | 39 |
| MI | $86,946 | $45,914 | -47.20 | 24 | 22 | 2 | 48 |
| OH | $32,903 | $44,334 | 34.70 | 25 | 25 | 0 | 50 |
| PA | $47,222 | $43,110 | -8.70 | 20 | 26 | -6 | 54 |
| MO | $36,752 | $37,193 | 1.20 | 14 | 13 | 1 | 35 |
| OK | $63,863 | $35,798 | -43.90 | 14 | 13 | 1 | 38 |
| AR | $19,581 | $34,268 | 75 | 9 | 6 | 3 | 14 |
| KY | $28,613 | $33,306 | 16.40 | 17 | 12 | 5 | 32 |
| IN | $41,949 | $31,505 | -24.90 | 18 | 18 | 0 | 36 |

### Q-68_results.md

# Q-68 Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| LANDO LIGHTING INC | ON | $11,290 | $869,121 | $857,831 | 1.30 | 2 |
| LUX LIGHTING LTD | NY | $74,049 | $393,072 | $319,023 | 18.80 | 5 |
| WIND CREEK BETHLEHEM, LLC | Unknown | $17,544 | $319,869 | $302,325 | 5.50 | 5 |
| DOLAN NORTHWEST, LLC- PORTLAND | WY | $118,842 | $379,042 | $260,200 | 31.40 | 13 |
| INTERIORS BY STEVEN G | FL | $1,415 | $255,711 | $254,296 | 0.60 | 2 |
| LBX LIGHTING INC. | TX | $72,094 | $279,715 | $207,621 | 25.80 | 7 |
| KALCO LIGHTING SHOWROOM\D | TX | $16,848 | $179,573 | $162,725 | 9.40 | 1 |
| HERALD WHOLESALE | NV | $19,101 | $174,398 | $155,297 | 11 | 11 |
| SUSAN SEMMELMANN INTERIORS | TX | $25,644 | $179,772 | $154,128 | 14.30 | 9 |
| ASHJIAN LIGHTING | CA | $11,400 | $160,977 | $149,577 | 7.10 | 5 |
| DESIGNERS RESOURCE COLLECTION | VA | $1,049 | $135,588 | $134,539 | 0.80 | 2 |
| POWER DESIGN RESOURCES | NC | $3,788 | $132,970 | $129,182 | 2.80 | 2 |
| BEAUTIFUL THINGS LIGHTING | TX | $86,806 | $203,629 | $116,823 | 42.60 | 13 |
| LIGHTING FIRST - BONITA | WI | $43,240 | $155,341 | $112,101 | 27.80 | 12 |
| CASA BELLA DESIGN & CONSTRUCTI | TX | $7,644 | $114,246 | $106,602 | 6.70 | 2 |
| LIGHTSTYLE OF TAMPA BAY | OR | $59,553 | $163,927 | $104,374 | 36.30 | 13 |
| DULLES ELECTRIC & SUPPLYf | VA | $10,761 | $113,854 | $103,093 | 9.50 | 8 |
| HINKLEY'S LTG FACTORY | WI | $93,157 | $195,304 | $102,147 | 47.70 | 13 |
| FORT WORTH LIGHTING | TX | $24,900 | $123,915 | $99,015 | 20.10 | 12 |
| URBAN LIGHTS | WY | $46,874 | $140,810 | $93,936 | 33.30 | 13 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| customer_num | customer_name | state | ltm_orders | ltm_gmv | last_order | days_since_last | avg_days_between | decay_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0000053 | SPACIAL EFX | MD | 11 | $152,319 | 2026-02-25 20:43:20 | 111 | 30.30 | 3.70 |

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 14
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0003937 | LUMENS LIGHT & LIVING | 519273WB | FLINT 3 LT MULTI DROP PENDANT | 72 | 6.80 | 54 | 7.90 | 44,668.40 | DECAY_DETECTED |
| 0003120 | LUXURY DESIGN BROOKLYN | 046261-073-FR001 | CADERE ISLAND LIGHT | 13 | 30.20 | 76 | 2.50 | 53,172 | SLOWING |
| 0003937 | LUMENS LIGHT & LIVING | 519671STB | VERDE 6LT CHANDELIER | 23 | 19.50 | 96 | 4.90 | 24,825 | DECAY_DETECTED |
| 0005456 | WAYFAIR LLC | 519275WB | FLINT 5 LT MULTI DROP | 18 | 20.40 | 125 | 6.10 | 18,686.40 | DECAY_DETECTED |
| 0010023 | FEI  FERGUSON MAIN ACCOUNT | 037661-038-FR001 | Estrella 42 Inch Island | 7 | 30 | 243 | 8.10 | 6,865.43 | DECAY_DETECTED |
| 0005685 | LIGHTOLOGY LLC | 519671STB | VERDE 6LT CHANDELIER | 6 | 45.70 | 195 | 4.30 | 11,543 | DECAY_DETECTED |
| 0004961 | LIGHTING NEW YORK (INTERNET) | 519671STB | VERDE 6LT CHANDELIER | 14 | 28.60 | 121 | 4.20 | 10,800.95 | DECAY_DETECTED |
| 0005789 | DESIGNER LIGHTING & FAN/DECOR | 505851OL | Roxy 27 Inch Pendant | 15 | 25.50 | 107 | 4.20 | 8,907 | DECAY_DETECTED |
| 0003937 | LUMENS LIGHT & LIVING | 405520BSG | Ashland Small Wall Sconce | 5 | 56.40 | 201 | 3.60 | 6,612.40 | DECAY_DETECTED |
| 0003937 | LUMENS LIGHT & LIVING | 030231-052 | Glacier 18 in LED ADA Bath | 5 | 56.60 | 258 | 4.60 | 5,118.30 | DECAY_DETECTED |
| 0010023 | FEI  FERGUSON MAIN ACCOUNT | 519671STB | VERDE 6LT CHANDELIER | 15 | 30.70 | 84 | 2.70 | 7,940.20 | SLOWING |
| 0002321 | DOLAN NORTHWEST LLC  PORTLAND | MODD-24IN-WALLSCONCE | CUSTOM 24 INCH ALABASTER WALL | 5 | 45.20 | 181 | 4 | 5,265 | DECAY_DETECTED |
| 0005456 | WAYFAIR LLC | 037656-038-FR001 | Estrella 32 Inch Pendant | 9 | 37.90 | 118 | 3.10 | 5,864.70 | DECAY_DETECTED |
| 0001416 | LAMPS PLUS | 506271MGM | Stuyvesant 12 Light Chandelier | 13 | 33.50 | 86 | 2.60 | 5,173.40 | SLOWING |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 50
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0005685 | LIGHTOLOGY LLC | 245,900.74 | 505840OL | Roxy 17 Inch Semi Flush Mount | 505851OL | Roxy 27 Inch Pendant | 37 |
| 0002274 | CAPITOL LIGHTING BOCA RATON | 167,212.99 | 505851OL | Roxy 27 Inch Pendant | 505840OL | Roxy 17 Inch Semi Flush Mount | 37 |
| 0001551 | PROGRESSIVE LIGHTING | 144,782.17 | 505840OL | Roxy 17 Inch Semi Flush Mount | 505851OL | Roxy 27 Inch Pendant | 37 |
| 0001802 | HINKLEY'S LTG FACTORY | 74,390.60 | 505851OL | Roxy 27 Inch Pendant | 505840OL | Roxy 17 Inch Semi Flush Mount | 37 |
| 0002855 | BEAUTIFUL THINGS LIGHTING | 74,003.99 | 505851OL | Roxy 27 Inch Pendant | 505840OL | Roxy 17 Inch Semi Flush Mount | 37 |
| 0006064 | LIGHTOPIA, LLC | 68,180.07 | 505840OL | Roxy 17 Inch Semi Flush Mount | 505851OL | Roxy 27 Inch Pendant | 37 |
| 0002131 | ELEMENTS AT HOME | 59,754.55 | 505840OL | Roxy 17 Inch Semi Flush Mount | 505851OL | Roxy 27 Inch Pendant | 37 |
| 0006119 | LUXURY FURNITURE INC. DBA VENICASA | 57,906.33 | 505840OL | Roxy 17 Inch Semi Flush Mount | 505851OL | Roxy 27 Inch Pendant | 37 |
| 0002233 | FRANKLIN LIGHTING INC | 57,895.82 | 505851OL | Roxy 27 Inch Pendant | 505840OL | Roxy 17 Inch Semi Flush Mount | 37 |
| 0001416 | LAMPS PLUS | 303,121.43 | 505840OL | Roxy 17 Inch Semi Flush Mount | 515045OL | Maurelle 17 Inch Semi Flush | 36 |
| 0001416 | LAMPS PLUS | 303,121.43 | 519273WB | Flint 3 Light Multi-Drop Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 36 |
| 0005685 | LIGHTOLOGY LLC | 245,900.74 | 505840OL | Roxy 17 Inch Semi Flush Mount | 515045OL | Maurelle 17 Inch Semi Flush | 36 |
| 0000967 | VALLEY LGT GALLERY | 121,049.50 | 515045OL | Maurelle 17 Inch Semi Flush | 505840OL | Roxy 17 Inch Semi Flush Mount | 36 |
| 0000967 | VALLEY LGT GALLERY | 121,049.50 | 519275WB | Flint 5 Light Multi-Drop Pendant | 519273WB | Flint 3 Light Multi-Drop Pendant | 36 |
| 0002321 | DOLAN NORTHWEST LLC  PORTLAND | 119,130.35 | 519273WB | Flint 3 Light Multi-Drop Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 36 |
| 0003006 | LIGHTING WORLD DECORATOR | 99,822.19 | 519275WB | Flint 5 Light Multi-Drop Pendant | 519273WB | Flint 3 Light Multi-Drop Pendant | 36 |
| 0001015 | LIGHTING INC | 74,505.95 | 505840OL | Roxy 17 Inch Semi Flush Mount | 515045OL | Maurelle 17 Inch Semi Flush | 36 |
| 0001802 | HINKLEY'S LTG FACTORY | 74,390.60 | 519273WB | Flint 3 Light Multi-Drop Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 36 |
| 0001802 | HINKLEY'S LTG FACTORY | 74,390.60 | 515045OL | Maurelle 17 Inch Semi Flush | 505840OL | Roxy 17 Inch Semi Flush Mount | 36 |
| 0002855 | BEAUTIFUL THINGS LIGHTING | 74,003.99 | 519273WB | Flint 3 Light Multi-Drop Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 36 |
| 0002351 | CAPITOL LIGHTING--E. HANOVER | 65,675.56 | 505840OL | Roxy 17 Inch Semi Flush Mount | 515045OL | Maurelle 17 Inch Semi Flush | 36 |
| 0001414 | HYE LIGHTING CO INC | 64,665.45 | 519275WB | Flint 5 Light Multi-Drop Pendant | 519273WB | Flint 3 Light Multi-Drop Pendant | 36 |
| 0003120 | LUXURY DESIGN BROOKLYN | 62,953.67 | 519275WB | Flint 5 Light Multi-Drop Pendant | 519273WB | Flint 3 Light Multi-Drop Pendant | 36 |
| 0003971 | METRO ELECTRIC | 59,107.05 | 519273WB | Flint 3 Light Multi-Drop Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 36 |
| 0006119 | LUXURY FURNITURE INC. DBA VENICASA | 57,906.33 | 505840OL | Roxy 17 Inch Semi Flush Mount | 515045OL | Maurelle 17 Inch Semi Flush | 36 |
| 0000525 | GARBE INDUSTRIES INC  TU | 52,937.25 | 515045OL | Maurelle 17 Inch Semi Flush | 505840OL | Roxy 17 Inch Semi Flush Mount | 36 |
| 0005388 | URBAN LIGHTS | 47,060.45 | 505840OL | Roxy 17 Inch Semi Flush Mount | 515045OL | Maurelle 17 Inch Semi Flush | 36 |
| 0010507 | MI CASA LIGHTING AND FAN | 45,415.29 | 519275WB | Flint 5 Light Multi-Drop Pendant | 519273WB | Flint 3 Light Multi-Drop Pendant | 36 |
| 0002790 | IDLEWOOD ELECTRIC SUPPLY | 44,287.58 | 519273WB | Flint 3 Light Multi-Drop Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 36 |
| 0001416 | LAMPS PLUS | 303,121.43 | 519221WB | Flint 1 Light Led  Convertible Wall Sconce/Mini Pendant | 519275WB | Flint 5 Light Multi-Drop Pendant | 29 |

*(Truncated: showing top 30 of 50 rows. Full data in cache file.)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0002321 | DOLAN NORTHWEST LLC  PORTLAND | OR | 119,130.35 | 520,863.77 | -77.10 | 0 | 0 | — | CONTRACTING |
| 0003299 | SHADES OF LIGHT | VA | 197,145.37 | 401,435.34 | -50.90 | 0 | 0 | — | CONTRACTING |
| 0001416 | LAMPS PLUS | CA | 303,121.43 | 420,515.55 | -27.90 | 0 | 0 | — | CONTRACTING |
| 0004961 | LIGHTING NEW YORK (INTERNET) | PA | 377,165.72 | 489,530.50 | -23 | 0 | 0 | — | CONTRACTING |
| 0003476 | LUX LIGHTING LTD | GA | 70,218.70 | 166,723.70 | -57.90 | 67,288 | 213,289.40 | -68.50 | CONTRACTING |
| 0010583 | NEIMAN MARCUS | TX | 25,293.60 | 104,646 | -75.80 | 0 | 0 | — | CONTRACTING |
| 0005789 | DESIGNER LIGHTING & FAN/DECOR | NJ | 164,144.31 | 103,817.39 | 58.10 | 0 | 20,658 | -100 | COMPETITIVE_DISPLACEMENT |
| 0005517 | LBX LIGHTING INC | TX | 49,183.30 | 108,114.65 | -54.50 | 90,995.30 | 17,493.60 | 420.20 | CONTRACTING |
| 0001859 | RAY ELECTRIC | MI | 32,064.97 | 90,361.54 | -64.50 | 0 | 0 | — | CONTRACTING |
| 0005675 | EUROPEAN CUSTOM LIGHTING | TX | 31,616.85 | 75,130.23 | -57.90 | 0 | 0 | — | CONTRACTING |
| 0003006 | LIGHTING WORLD DECORATOR | NY | 99,822.19 | 135,375.23 | -26.30 | 0 | 8,737.50 | -100 | CONTRACTING |
| 0002351 | CAPITOL LIGHTING--E. HANOVER | NJ | 65,675.56 | 100,211.54 | -34.50 | 0 | 0 | — | CONTRACTING |
| 0003285 | LIGHTSTYLE OF ORLANDO | FL | 55,327.64 | 85,928.28 | -35.60 | 2,554.50 | 0 | — | CONTRACTING |
| 0003971 | METRO ELECTRIC | MO | 59,107.05 | 30,828.38 | 91.70 | 0 | 16,888 | -100 | COMPETITIVE_DISPLACEMENT |
| 0003388 | COLONIAL ELECTRIC SUPPLY | PA | 37,457.82 | 65,664.10 | -43 | 0 | 0 | — | CONTRACTING |
| 0010671 | BISONOFFICE LLC | IL | 45,882.80 | 72,461.77 | -36.70 | 0 | 0 | — | CONTRACTING |
| 0005753 | LIGHT BULBS UNLIMITED BOCA RA | FL | 32,083.52 | 55,702.12 | -42.40 | 4,087 | 0 | — | CONTRACTING |
| 0002233 | FRANKLIN LIGHTING INC | FL | 57,895.82 | 80,358.01 | -28 | 10,957 | 0 | — | CONTRACTING |
| 0004686 | FORT WORTH LIGHTING | TX | 25,186.10 | 47,364.40 | -46.80 | 0 | 0 | — | CONTRACTING |
| 0006064 | LIGHTOPIA, LLC | CA | 68,180.07 | 89,883.22 | -24.10 | 0 | 0 | — | CONTRACTING |
| 0002825 | RAINBOW LIGHTING II LLC | NY | 86,505.65 | 67,582.62 | 28 | 0 | 8,852.60 | -100 | COMPETITIVE_DISPLACEMENT |
| 0002958 | UNIVERSAL LIGHTS | TX | 31,640.80 | 49,246.83 | -35.80 | 0 | 12,227 | -100 | CONTRACTING |
| 0003483 | THE LIGHT HOUSE | CA | 35,788.10 | 20,251.80 | 76.70 | 0 | 8,109 | -100 | COMPETITIVE_DISPLACEMENT |
| 0001308 | BRECHERS COMPANY | KY | 35,585.99 | 48,487.62 | -26.60 | 0 | 0 | — | CONTRACTING |
| 0002186 | KENDALL ELECTRIC INC | MI | 37,417.32 | 24,581.71 | 52.20 | 0 | 18,970 | -100 | COMPETITIVE_DISPLACEMENT |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 0010558 | CLIVE DANIEL HOME | 2 | 258,073.75 | 596.80 | [{'quarter': '2025-07-01', 'revenue': 19501.0, 'qoq_pct': -22.9}, {'quarter': '2025-10-01', 'revenue': 11949.0, 'qoq_pct': -38.7}, {'quarter': '2026-01-01', 'revenue': 37039.3, 'qoq_pct': 210.0}, {'quarter': '2026-04-01', 'revenue': 258073.75, 'qoq_pct': 596.8}] |
| 0010336 | LIGHT LAB DESIGN | 2 | 135,692 | 4,527 | [{'quarter': '2025-07-01', 'revenue': 2932.6, 'qoq_pct': 372.4}, {'quarter': '2026-01-01', 'revenue': 135692.0, 'qoq_pct': 4527.0}, {'quarter': '2026-04-01', 'revenue': 36163.88, 'qoq_pct': -73.3}] |
| 0000967 | VALLEY LGT GALLERY | 3 | 83,208.90 | 331.30 | [{'quarter': '2025-07-01', 'revenue': 6491.5, 'qoq_pct': -52.7}, {'quarter': '2025-10-01', 'revenue': 11020.9, 'qoq_pct': 69.8}, {'quarter': '2026-01-01', 'revenue': 19290.5, 'qoq_pct': 75.0}, {'quarter': '2026-04-01', 'revenue': 83208.9, 'qoq_pct': 331.3}] |
| 0003476 | LUX LIGHTING LTD | 2 | 56,059.50 | 650.60 | [{'quarter': '2025-07-01', 'revenue': 56059.5, 'qoq_pct': 650.6}, {'quarter': '2025-10-01', 'revenue': 9403.2, 'qoq_pct': -83.2}, {'quarter': '2026-01-01', 'revenue': 1924.0, 'qoq_pct': -79.5}, {'quarter': '2026-04-01', 'revenue': 2832.0, 'qoq_pct': 47.2}] |
| 0005789 | DESIGNER LIGHTING & FAN/DECOR | 2 | 55,467.17 | 43 | [{'quarter': '2025-07-01', 'revenue': 32041.03, 'qoq_pct': 43.0}, {'quarter': '2025-10-01', 'revenue': 43716.3, 'qoq_pct': 36.4}, {'quarter': '2026-01-01', 'revenue': 55467.17, 'qoq_pct': 26.9}, {'quarter': '2026-04-01', 'revenue': 31917.99, 'qoq_pct': -42.5}] |
| 0003014 | Lighting Design Center | 2 | 48,568 | 693.40 | [{'quarter': '2025-07-01', 'revenue': 7618.0, 'qoq_pct': -67.1}, {'quarter': '2025-10-01', 'revenue': 4488.9, 'qoq_pct': -41.1}, {'quarter': '2026-01-01', 'revenue': 6121.5, 'qoq_pct': 36.4}, {'quarter': '2026-04-01', 'revenue': 48568.0, 'qoq_pct': 693.4}] |
| 0005299 | RBDELAA LIGHTING | 2 | 39,116.50 | 1,225.70 | [{'quarter': '2025-07-01', 'revenue': 7022.44, 'qoq_pct': 297.0}, {'quarter': '2025-10-01', 'revenue': 2950.64, 'qoq_pct': -58.0}, {'quarter': '2026-01-01', 'revenue': 39116.5, 'qoq_pct': 1225.7}] |
| 0004803 | BELAMI, INC / 1STOP LIGHTING | 2 | 37,731.84 | 252.60 | [{'quarter': '2025-07-01', 'revenue': 37731.84, 'qoq_pct': 182.2}, {'quarter': '2025-10-01', 'revenue': 12135.67, 'qoq_pct': -67.8}, {'quarter': '2026-01-01', 'revenue': 6660.41, 'qoq_pct': -45.1}, {'quarter': '2026-04-01', 'revenue': 23486.61, 'qoq_pct': 252.6}] |
| 0002825 | RAINBOW LIGHTING II LLC | 2 | 33,084.11 | 1,117.80 | [{'quarter': '2025-07-01', 'revenue': 33084.11, 'qoq_pct': 1117.8}, {'quarter': '2025-10-01', 'revenue': 16017.84, 'qoq_pct': -51.6}, {'quarter': '2026-01-01', 'revenue': 11512.3, 'qoq_pct': -28.1}, {'quarter': '2026-04-01', 'revenue': 24731.4, 'qoq_pct': 114.8}] |
| 0000525 | GARBE INDUSTRIES INC  TU | 2 | 29,724 | 199.50 | [{'quarter': '2025-07-01', 'revenue': 10740.0, 'qoq_pct': 87.0}, {'quarter': '2025-10-01', 'revenue': 9926.0, 'qoq_pct': -7.6}, {'quarter': '2026-01-01', 'revenue': 29724.0, 'qoq_pct': 199.5}, {'quarter': '2026-04-01', 'revenue': 2547.25, 'qoq_pct': -91.4}] |
| 0002661 | SUNBELT FANS & LTG LAUREL | 3 | 29,018.36 | 670.70 | [{'quarter': '2025-07-01', 'revenue': 2290.38, 'qoq_pct': 200.0}, {'quarter': '2025-10-01', 'revenue': 17652.42, 'qoq_pct': 670.7}, {'quarter': '2026-01-01', 'revenue': 29018.36, 'qoq_pct': 64.4}, {'quarter': '2026-04-01', 'revenue': 594.0, 'qoq_pct': -98.0}] |
| 0001015 | LIGHTING INC | 4 | 26,856.90 | 79.90 | [{'quarter': '2025-07-01', 'revenue': 11270.4, 'qoq_pct': 79.9}, {'quarter': '2025-10-01', 'revenue': 15760.0, 'qoq_pct': 39.8}, {'quarter': '2026-01-01', 'revenue': 20618.65, 'qoq_pct': 30.8}, {'quarter': '2026-04-01', 'revenue': 26856.9, 'qoq_pct': 30.3}] |
| 0002855 | BEAUTIFUL THINGS LIGHTING | 2 | 26,247.80 | 50.70 | [{'quarter': '2025-07-01', 'revenue': 26247.8, 'qoq_pct': 50.7}, {'quarter': '2025-10-01', 'revenue': 14872.99, 'qoq_pct': -43.3}, {'quarter': '2026-01-01', 'revenue': 22056.95, 'qoq_pct': 48.3}, {'quarter': '2026-04-01', 'revenue': 6971.15, 'qoq_pct': -68.4}] |
| 0001414 | HYE LIGHTING CO INC | 2 | 24,677.40 | 83.10 | [{'quarter': '2025-07-01', 'revenue': 15535.45, 'qoq_pct': 40.2}, {'quarter': '2025-10-01', 'revenue': 13474.7, 'qoq_pct': -13.3}, {'quarter': '2026-01-01', 'revenue': 24677.4, 'qoq_pct': 83.1}, {'quarter': '2026-04-01', 'revenue': 9359.85, 'qoq_pct': -62.1}] |
| 0010671 | BISONOFFICE LLC | 2 | 23,417.39 | 209.40 | [{'quarter': '2025-07-01', 'revenue': 12795.82, 'qoq_pct': 209.4}, {'quarter': '2025-10-01', 'revenue': 23417.39, 'qoq_pct': 83.0}, {'quarter': '2026-01-01', 'revenue': 6443.32, 'qoq_pct': -72.5}, {'quarter': '2026-04-01', 'revenue': 2539.0, 'qoq_pct': -60.6}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Kalco Lighting / Allegri Crystal (kal, org_id=146)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 8
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 519275WB | Flint 5 Light Multi-Drop Pendant | FLINT | 583,127.50 | 515 | — | 2026-6-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 100065.55}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 75687.42}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 64745.71}, {'customer': 'BUILD.COM', 'revenue': 32335.17}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 28304.4}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 21462.92}, {'customer': 'WAYFAIR LLC', 'revenue': 21028.11}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 15856.57}, {'customer': 'SUN LIGHTING', 'revenue': 13280.4}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 11728.44}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 9742.62}, {'customer': 'CITY LIGHTS', 'revenue': 7456.5}, {'customer': 'PINE TREE LIGHTING', 'revenue': 6426.94}, {'customer': '1-800-MY-LAMPS', 'revenue': 4469.14}, {'customer': 'DULLES ELECTRIC & SUPPLY', 'revenue': 4408.97}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 4252.84}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 4028.1}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 3934.35}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 3915.9}, {'customer': 'LIGHTING ETC', 'revenue': 3872.0}, {'customer': 'NEIMAN MARCUS', 'revenue': 3747.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 3372.3}, {'customer': 'DOLAN NORTHWEST LLC  PORTLAND', 'revenue': 3372.3}, {'customer': 'MANHATTAN LIGHTS INC', 'revenue': 3095.14}, {'customer': 'UNIVERSAL LAMP', 'revenue': 3095.14}, {'customer': 'PLUMBING DISTRIBUTORS  INC', 'revenue': 3095.14}, {'customer': 'KRELL LIGHTING', 'revenue': 3037.32}, {'customer': 'Lighting Design Center', 'revenue': 2832.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 2790.0}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 2748.0}, {'customer': 'LUXUR LIGHTING', 'revenue': 2748.0}, {'customer': 'DESIGNERS RESOURCE COLLECTION', 'revenue': 2747.8}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 2665.0}, {'customer': 'NOVA LIGHTING', 'revenue': 2610.6}, {'customer': 'HERALD WHOLESALE', 'revenue': 2498.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 2498.0}, {'customer': 'EAGLE LIGHTING DISTRIBUTORS', 'revenue': 2498.0}, {'customer': 'LAMPS EXPO/LAMPCLICK.COM', 'revenue': 2498.0}, {'customer': 'GEORGIA LIGHTING', 'revenue': 2466.03}, {'customer': 'WILSON LIGHTING- NAPLES', 'revenue': 2248.2}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 2061.0}, {'customer': 'CAPITOL LIGHTING PARAMUS', 'revenue': 1967.25}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 1967.25}, {'customer': 'URBAN LIGHTS', 'revenue': 1957.0}, {'customer': 'R&F LIGHTING & SUPPLIES', 'revenue': 1896.32}, {'customer': 'TEXAS BRIGHT IDEAS INC', 'revenue': 1628.4}, {'customer': 'GEORGIAN LIGHTING GALERY INC', 'revenue': 1621.32}, {'customer': 'REFLECTIONS L+M', 'revenue': 1621.32}, {'customer': 'SUPREME LTG & ELEC', 'revenue': 1621.32}, {'customer': 'NORTHERN LIGHTING WESTERV', 'revenue': 1621.32}, {'customer': 'EFIRDS INTERIORS', 'revenue': 1621.32}, {'customer': "AARON'S SUPPLY  INC", 'revenue': 1621.32}, {'customer': 'KING ELECTRIC COMPANY INC', 'revenue': 1621.32}, {'customer': 'B A ROBINSON COMPANY LTD CALG', 'revenue': 1621.2}, {'customer': 'THE JARRELL COMPANY', 'revenue': 1580.1}, {'customer': 'FUSION LIGHT AND DESIGN LLC', 'revenue': 1580.1}, {'customer': 'IBS LIGHTING LTD.', 'revenue': 1580.1}, {'customer': 'ILLUMINATIONS MC ALLEN', 'revenue': 1580.1}, {'customer': 'CED / GLACIER STATE ELECTRIC', 'revenue': 1580.1}, {'customer': 'LIGHTING INC', 'revenue': 1511.4}, {'customer': 'RITTENHOUSE ELECTRIC', 'revenue': 1473.82}, {'customer': 'FANWORLD', 'revenue': 1473.82}, {'customer': 'WINSUPPLY HENDERSONVILLE', 'revenue': 1473.82}, {'customer': 'WOLBERG ELECTRICAL SUPPLY', 'revenue': 1473.82}, {'customer': 'LIGHT LAB DESIGN', 'revenue': 1473.82}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 1473.82}, {'customer': 'FOUNDRY  ARC DISTRIBUTION', 'revenue': 1473.82}, {'customer': 'CORDREY COLLECTION', 'revenue': 1436.35}, {'customer': 'PREMIER LIGHTING', 'revenue': 1436.35}, {'customer': 'LIGHTING ZONE', 'revenue': 1436.35}, {'customer': 'HALL ELECTRIC COMPANY', 'revenue': 1416.0}, {'customer': 'LIGHTING BY FOX LLC', 'revenue': 1416.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 1374.0}, {'customer': 'HOMIER LUMINAIRE INC.', 'revenue': 1374.0}, {'customer': 'LUXURY DESIGN BROOKLYN', 'revenue': 1374.0}, {'customer': 'CONSUMERS LIGHTING AND LAMPS L', 'revenue': 1374.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 1374.0}, {'customer': 'WALNUT CREEK LIGHTING', 'revenue': 1374.0}, {'customer': 'LIGHT BULBS UNLIMITED BOCA RA', 'revenue': 1374.0}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 1374.0}, {'customer': 'LEEWAL LLC', 'revenue': 1374.0}, {'customer': 'BISONOFFICE LLC', 'revenue': 1374.0}, {'customer': 'DEMENT LIGHTING', 'revenue': 1374.0}, {'customer': 'INDIANA LIGHTING CENTER', 'revenue': 1374.0}, {'customer': 'LIGHTING SUPERSTORE', 'revenue': 1374.0}, {'customer': 'RAY ELECTRIC', 'revenue': 1345.2}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 1332.78}, {'customer': 'LIGHTING INSTYLE', 'revenue': 1311.45}, {'customer': 'ACCENT LTG GALLERIES', 'revenue': 1249.0}, {'customer': 'ONE STOP LIGHTING', 'revenue': 1249.0}, {'customer': 'SHOPFREELY.COM', 'revenue': 1249.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 1249.0}, {'customer': 'WOLSELEY CANADA  INC', 'revenue': 1249.0}, {'customer': 'A A PORTER LTG CO (DO NOT CONTACT)', 'revenue': 1249.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 1249.0}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 1124.1}, {'customer': 'BELL & MCCOY COMPANIES', 'revenue': 1124.1}, {'customer': 'LIGHTSTYLES', 'revenue': 1099.2}, {'customer': 'CAPITOL LIGHTING--EATONTOWN', 'revenue': 1030.5}, {'customer': 'LIGHTING WAREHOUSE', 'revenue': 961.8}, {'customer': 'INFO LIGHTING, INC.', 'revenue': 811.85}, {'customer': 'HERMITAGE ELECTRIC SUPPLY', 'revenue': 687.0}, {'customer': 'LEE SUPPLY CORP', 'revenue': 624.5}, {'customer': 'WASATCH LIGHTING', 'revenue': 624.5}, {'customer': 'DHILLON LIGHTING', 'revenue': 624.5}, {'customer': 'MST LIGHTING INC.', 'revenue': 421.02}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 187.35}, {'customer': 'SCOUT LIGHTING', 'revenue': 0.1}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'LUXURY LIGHTING GROUP', 'revenue': 0.0}, {'customer': 'LIGHT & DAY LLC', 'revenue': 0.0}, {'customer': 'MI CASA LIGHTING AND FAN', 'revenue': 0.0}, {'customer': 'PARK LIGHTING', 'revenue': 0.0}, {'customer': 'RAINBOW LIGHTING INC /NBROOK', 'revenue': 0.0}, {'customer': 'EISENREICH INTERIORS', 'revenue': 0.0}, {'customer': 'EMMY COUTURE DESIGNS', 'revenue': 0.0}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 0.0}, {'customer': 'GINA IRELAND INTERIORS', 'revenue': 0.0}, {'customer': 'BUSTED 2 BANGIN', 'revenue': 0.0}, {'customer': 'ARYA GROUP INC', 'revenue': 0.0}, {'customer': 'KITCHEN SOCIETY', 'revenue': 0.0}, {'customer': 'I.D. HOME LOGISTICS INC', 'revenue': 0.0}, {'customer': 'B PILA DESIGN STUDIO', 'revenue': 0.0}, {'customer': 'TEELA BENNETT DESIGN', 'revenue': 0.0}, {'customer': 'JGIB INTERIORS', 'revenue': 0.0}, {'customer': 'AURORA LIGHTING & DESIGN', 'revenue': 0.0}, {'customer': 'DESIGN HUTCH', 'revenue': 0.0}, {'customer': 'EL DESIGN', 'revenue': 0.0}, {'customer': 'STEPHANIE ERVIN INTERIORS', 'revenue': 0.0}, {'customer': 'CARISA INTERIOR DESIGN', 'revenue': 0.0}, {'customer': 'COAST LIGHTING', 'revenue': 0.0}, {'customer': 'UNCOMMON ROSE DESIGNS', 'revenue': 0.0}, {'customer': 'THE VIBE INTERIORS', 'revenue': 0.0}, {'customer': 'PFH DESIGNS LLC', 'revenue': 0.0}, {'customer': 'JAQUELINE DOWNS INTERIOR DESIGN', 'revenue': 0.0}, {'customer': 'DESIGN SQUARED', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 0.0}, {'customer': 'BEND LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 0.0}, {'customer': 'PINE LIGHTING LTD', 'revenue': 0.0}, {'customer': 'LIGHTING BY LAVONNE  LLC', 'revenue': 0.0}, {'customer': 'BALTIMORE DESIGN CENTER', 'revenue': 0.0}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 0.0}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 0.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 0.0}, {'customer': 'P&F LITES ECT. LLC', 'revenue': 0.0}, {'customer': 'UNIVERSAL LIGHTS', 'revenue': 0.0}, {'customer': 'WATSON & CO.', 'revenue': 0.0}, {'customer': 'ALLOWAY LIGHTING COMPANY', 'revenue': 0.0}, {'customer': 'BEAUTIFUL LIGHTS LLC', 'revenue': 0.0}, {'customer': 'CENTRAL BULB INC', 'revenue': 0.0}, {'customer': 'FIXTURE EXCHANGE, THE', 'revenue': 0.0}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 0.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'ROYCE COLLECTION INC', 'revenue': 0.0}, {'customer': 'EXCEL LIGHTING & ELECTRICAL', 'revenue': 0.0}, {'customer': 'UNION ELECTRIC LIGHTING - TORO', 'revenue': 0.0}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 0.0}, {'customer': 'JL DESIGNS', 'revenue': 0.0}, {'customer': 'BRADLEY ADCOCK DESIGNS INC', 'revenue': 0.0}, {'customer': 'BLISS LINENS WORLD LP', 'revenue': 0.0}, {'customer': 'WHITE ROOM DESIGN LLC', 'revenue': 0.0}, {'customer': 'CHRISTINE VROOM INTERIORS', 'revenue': 0.0}, {'customer': 'LIGHTING SOLUTIONS & DESIGN', 'revenue': 0.0}, {'customer': 'PATTERSON HOMES', 'revenue': 0.0}, {'customer': 'ALADDIN LIGHTING AND SUPPLY INC.', 'revenue': 0.0}, {'customer': 'ANDERSON DESIGN STUDIO, LLC', 'revenue': 0.0}, {'customer': 'NYE DESIGN LLC', 'revenue': 0.0}, {'customer': 'BAYLEE DEYON DESIGN LLC', 'revenue': 0.0}, {'customer': 'FONDE INTERIORS', 'revenue': 0.0}, {'customer': 'LAURA KEHOE DESIGN', 'revenue': 0.0}, {'customer': 'CLASSIC IMPORTS & DESIGN LLC', 'revenue': 0.0}, {'customer': 'LIGHT CENTER', 'revenue': 0.0}, {'customer': "MONTGOMERY'S", 'revenue': 0.0}, {'customer': 'SHARED TREASURES', 'revenue': 0.0}, {'customer': 'LJR DESIGN', 'revenue': 0.0}, {'customer': 'CRESPO DESIGN GROUP', 'revenue': 0.0}, {'customer': 'AWARD INTERIORS', 'revenue': 0.0}, {'customer': 'AUDREY CAMPBELL DESIGN', 'revenue': 0.0}, {'customer': 'BYBRITT DESIGN', 'revenue': 0.0}, {'customer': 'TRACI CONNELL INTERIORS', 'revenue': 0.0}, {'customer': 'HAMILTON INTERIORS', 'revenue': 0.0}, {'customer': 'AGAPE DESIGN GROUP', 'revenue': 0.0}, {'customer': 'ARTISTIC ELEMENTS', 'revenue': -1768.82}] | [{'item': '519273WB', 'desc': 'Flint 3 Light Multi-Drop Pendant', 'available': 45}] |
| 515155OL | Samal 21 Inch Pendant | SAMAL | 124,924.90 | 260 | — | 2026-6-28 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 8853.33}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 8239.6}, {'customer': 'SHADES OF LIGHT', 'revenue': 8078.46}, {'customer': "PINE GROVE ELEC'L SPL INC", 'revenue': 6807.15}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 6050.7}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 6045.5}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 5304.97}, {'customer': 'CREGGER COMPANY  INC', 'revenue': 5138.88}, {'customer': 'LOWCOUNTRY LIGHTING STUDIO LLC', 'revenue': 3371.52}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 3367.75}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 3145.05}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 2859.45}, {'customer': 'PARK LIGHTING', 'revenue': 2687.4}, {'customer': 'FUSION LIGHT AND DESIGN LLC', 'revenue': 2610.55}, {'customer': "BUTLER'S ELECTRIC", 'revenue': 2249.62}, {'customer': 'BRECHERS COMPANY', 'revenue': 2246.8}, {'customer': 'BEE RIDGE LIGHTING DESIGN', 'revenue': 1865.58}, {'customer': 'BLACK WHALE LIGHTING', 'revenue': 1832.33}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 1762.95}, {'customer': 'CAROLINA LANTERNS & ACCS', 'revenue': 1730.08}, {'customer': 'REVIVAL LIGHTING', 'revenue': 1707.75}, {'customer': 'COASTAL LTG SUPPLY/WILMIN', 'revenue': 1695.66}, {'customer': 'HOBRECHT LIGHTING CO INC', 'revenue': 1652.55}, {'customer': 'MAPLE RIDGE LIGHTING, INC. dba', 'revenue': 1652.55}, {'customer': 'GARBE INDUSTRIES INC  TU', 'revenue': 1630.45}, {'customer': 'SISTER LIGHTING dba', 'revenue': 1572.85}, {'customer': 'SUN LIGHTING', 'revenue': 1501.95}, {'customer': 'BEAUTIFUL THINGS LIGHTING', 'revenue': 1501.95}, {'customer': 'WATTS CURRENT', 'revenue': 1437.0}, {'customer': 'PLUMBING DISTRIBUTORS  INC', 'revenue': 1332.64}, {'customer': 'LIGHT BY ALEXANDRIA', 'revenue': 1187.08}, {'customer': 'ULTRA DESIGN CENTER LLC', 'revenue': 1101.7}, {'customer': 'HYDROLOGIC CORPORATE', 'revenue': 1054.0}, {'customer': 'BUILD.COM', 'revenue': 1016.5}, {'customer': 'BISONOFFICE LLC', 'revenue': 1006.0}, {'customer': 'WAYFAIR LLC', 'revenue': 1001.3}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 952.09}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 862.2}, {'customer': 'M & M LIGHTING LP', 'revenue': 782.5}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 766.5}, {'customer': 'OLD WORLD STONE IMPORTS', 'revenue': 661.25}, {'customer': 'STOKES ELECTRIC', 'revenue': 640.74}, {'customer': 'FOREST HILL LIGHTING', 'revenue': 621.86}, {'customer': "RICHARD'S LIGHTING", 'revenue': 621.86}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 621.86}, {'customer': 'LIFESTYLES STORES INC', 'revenue': 606.05}, {'customer': 'LIGHT CENTER', 'revenue': 606.05}, {'customer': 'ONE SIDE DOOR', 'revenue': 565.22}, {'customer': "AARON'S SUPPLY  INC", 'revenue': 565.22}, {'customer': 'CAMINITI ASSOCIATE  INC  ILL', 'revenue': 565.22}, {'customer': 'CARRINGTON LIGHTING', 'revenue': 553.35}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 543.0}, {'customer': 'FIRST COAST LIGHTING AND FAN', 'revenue': 543.0}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 542.81}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 527.0}, {'customer': 'SUNBELT FANS & LTG LAUREL', 'revenue': 527.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 527.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 511.19}, {'customer': 'KALCO MARKETING CRM', 'revenue': 479.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 479.0}, {'customer': 'COAST LIGHTING', 'revenue': 479.0}, {'customer': "CAROL'S LIGHTING", 'revenue': 479.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 479.0}, {'customer': 'RIVERSIDE LIGHTING', 'revenue': 479.0}, {'customer': 'NOVA LIGHTING', 'revenue': 474.3}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 443.07}, {'customer': 'VP SUPPLY CORP', 'revenue': 342.55}, {'customer': 'LEE SUPPLY CORP', 'revenue': 239.5}, {'customer': 'EUROPEAN CUSTOM LIGHTING', 'revenue': 239.5}, {'customer': 'ROBINSON LIGHTING LTD / PLYMOU', 'revenue': 217.2}, {'customer': 'PURPOSE INTERIORS', 'revenue': 82.21}, {'customer': 'AURORA LIGHTING & DESIGN', 'revenue': 0.0}, {'customer': 'LESSMAN ELECTRIC SUPPLY CO. INC.', 'revenue': 0.0}, {'customer': 'LINDSEY GLASS', 'revenue': 0.0}, {'customer': 'KALCO LIGHTING SHOWROOM\\D', 'revenue': 0.0}, {'customer': 'BERKELEY LIGHTING COMPANY', 'revenue': 0.0}, {'customer': 'LIGHT HOUSE  THE   HARLINGEN', 'revenue': 0.0}, {'customer': 'WILSON COMPANY-KANSAS', 'revenue': 0.0}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 0.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 0.0}, {'customer': 'RE-LIGHTING INC', 'revenue': 0.0}, {'customer': 'SUPREME LTG & ELEC', 'revenue': 0.0}, {'customer': 'LIGHT INNOVATIONS', 'revenue': 0.0}, {'customer': 'SUPER LITE LIGHTING LTD', 'revenue': 0.0}, {'customer': 'SOUTH DADE LIGHTING INC\\M', 'revenue': 0.0}, {'customer': 'ROCKINGHAM ELEC. SUPPLY', 'revenue': 0.0}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 0.0}, {'customer': 'BRAND LIGHTING', 'revenue': 0.0}, {'customer': 'HOUSE OF LIGHTS INC', 'revenue': 0.0}, {'customer': 'CONNECTICUT LTG CENTER', 'revenue': 0.0}, {'customer': 'DULLES ELECTRIC & SUPPLY', 'revenue': 0.0}, {'customer': 'SALTBOX THE', 'revenue': 0.0}, {'customer': 'AVON CLOCK & LIGHTING', 'revenue': 0.0}, {'customer': 'CARAVELLE LIGHTING INC', 'revenue': 0.0}, {'customer': 'LIGHTHOUSE INC THE', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST', 'revenue': 0.0}, {'customer': 'EFIRDS INTERIORS', 'revenue': 0.0}, {'customer': 'RENSENHOUSE OF LIGHTS', 'revenue': 0.0}, {'customer': 'WILSON LIGHTING- NAPLES', 'revenue': 0.0}, {'customer': "HORTON'S OF LA GRANGE", 'revenue': 0.0}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': "ARMSTRONG'S SUPPLY CO., INC.", 'revenue': 0.0}, {'customer': 'BESCO ELECTRIC SUPPLY CO', 'revenue': 0.0}, {'customer': 'MCLAREN LIGHTING', 'revenue': 0.0}, {'customer': 'KILOHANA LIGHTING/LIHUE', 'revenue': 0.0}, {'customer': 'HOUSE OF LAMPS & SHADES', 'revenue': 0.0}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 0.0}, {'customer': 'COLONIAL ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'WISEWAY SUPPLY INC', 'revenue': 0.0}, {'customer': 'METRO ELECTRIC', 'revenue': 0.0}, {'customer': 'LIGHTSTYLES', 'revenue': 0.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 0.0}, {'customer': 'FIXTURE THIS INC', 'revenue': 0.0}, {'customer': 'FILAMENT LIGHTING', 'revenue': 0.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 0.0}, {'customer': 'LIGHTING BY FOX LLC', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'LBX LIGHTING INC', 'revenue': 0.0}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 0.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 0.0}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 0.0}, {'customer': 'PINE LIGHTING LTD', 'revenue': 0.0}, {'customer': 'NORTHWEST ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 0.0}, {'customer': 'MAGNOLIA LIGHTING, INC.', 'revenue': 0.0}, {'customer': 'PIONEER LIGHTING  INC', 'revenue': 0.0}, {'customer': 'CONSTRUCTION RESOURCES COMPANY LLC', 'revenue': 0.0}, {'customer': 'LIGHTS & MORE / TAMPA', 'revenue': 0.0}, {'customer': 'CATES LIGHTING AT ELEMENTS OF', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST / FT. MYERS', 'revenue': 0.0}, {'customer': 'FORESIGHT LIGHTING (DO NOT USE)', 'revenue': 0.0}, {'customer': 'LIGHTING FACTORY OUTLET', 'revenue': 0.0}, {'customer': 'INSIDE OUT LIGHTING & DECOR', 'revenue': 0.0}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 0.0}, {'customer': 'QUINN WHOLESALE DBA', 'revenue': 0.0}, {'customer': 'CRIMSON DESIGN GROUP', 'revenue': 0.0}, {'customer': '18 SETENTA GALLERIA', 'revenue': 0.0}, {'customer': 'GARBES LIGHTING', 'revenue': 0.0}, {'customer': 'LEEWAL LLC', 'revenue': 0.0}, {'customer': 'GW KEETER LIGHTING&HOME DECOR', 'revenue': 0.0}, {'customer': 'DE LAVENNE DESIGN', 'revenue': 0.0}, {'customer': 'SAVE MORE PLUMBING & LIGHTING', 'revenue': 0.0}, {'customer': 'INSPIRED INTERIORS', 'revenue': 0.0}, {'customer': 'BEAUTIFUL INTERIORS DESIGN GROUP', 'revenue': 0.0}, {'customer': 'EAST INDIES TRADING DBA WEST HOME COLLECTION', 'revenue': 0.0}] | [{'item': '515145OL', 'desc': 'Samal 21 in Pendant', 'available': 26}, {'item': '515141OL', 'desc': 'Samal 12 in Flush Mount', 'available': 20}, {'item': '515156OL', 'desc': 'Samal 25 Inch Pendant', 'available': 12}] |
| 030257-038 | Glacier 60 Inch LED Round Pendant | COL185 | 90,966.21 | 29 | — | 2026-7-7 | [{'customer': 'LIGHTING INC', 'revenue': 15980.9}, {'customer': 'B. COLLECTIVE CO.', 'revenue': 12235.0}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 7680.8}, {'customer': 'DOLAN NORTHWEST LLC  PORTLAND', 'revenue': 6881.4}, {'customer': 'FANWERKS & LIGHTING INC (HOLD)', 'revenue': 4206.0}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 4206.0}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 4206.0}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 3995.7}, {'customer': 'EFIRDS INTERIORS', 'revenue': 3823.0}, {'customer': 'VENICE LIGHTING COMPANY', 'revenue': 3823.0}, {'customer': 'CLIVE DANIEL HOME', 'revenue': 3823.0}, {'customer': 'COAST LIGHTING', 'revenue': 3823.0}, {'customer': 'ELEGANTE INTERIORS & DESIGN LLC', 'revenue': 3823.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 3708.31}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 3685.1}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 3154.5}, {'customer': 'LBX LIGHTING INC', 'revenue': 1911.5}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 0.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'ONE STOP LIGHTING', 'revenue': 0.0}, {'customer': 'TEXAS BRIGHT IDEAS INC', 'revenue': 0.0}, {'customer': 'HERALD WHOLESALE', 'revenue': 0.0}, {'customer': 'FIXTURE EXCHANGE, THE', 'revenue': 0.0}, {'customer': 'BEAUTIFUL THINGS LIGHTING', 'revenue': 0.0}, {'customer': 'QUALITY LIGHTING/DELRAY', 'revenue': 0.0}, {'customer': 'UNIVERSAL LIGHTS', 'revenue': 0.0}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': 'YALE ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'THE LIGHT HOUSE', 'revenue': 0.0}, {'customer': 'LIGHTING PALACE/BROOKLYN', 'revenue': 0.0}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 0.0}, {'customer': 'TALLAHASSEE LIGHTING FAN', 'revenue': 0.0}, {'customer': 'BUILD.COM', 'revenue': 0.0}, {'customer': 'DESERT LIGHTING SOLUTIONS', 'revenue': 0.0}, {'customer': 'MATCHEZ INTERNATIONALDBA', 'revenue': 0.0}, {'customer': 'BEBBER PROPERTIES INC dba', 'revenue': 0.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 0.0}, {'customer': 'AREZZO DESIGN GROUP', 'revenue': 0.0}, {'customer': 'EUROPEAN CUSTOM LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 0.0}, {'customer': 'LIGHTING BOUTIQUE LLC', 'revenue': 0.0}, {'customer': 'CASA BELLA DESIGN & CONSTRUCTI', 'revenue': 0.0}, {'customer': 'LIGHT BULBS UNLIMITED BOCA RA', 'revenue': 0.0}, {'customer': 'LUMINOUS TRENDS DBA MODERN LUXURY', 'revenue': 0.0}, {'customer': 'NORTHWEST ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'ELECTRIC OUTLET INC', 'revenue': 0.0}, {'customer': 'CONSUMERS LIGHTING AND LAMPS L', 'revenue': 0.0}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 0.0}, {'customer': 'DESIGN HOUSE  INC  THE', 'revenue': 0.0}, {'customer': 'PARADISE LIGHTING', 'revenue': 0.0}, {'customer': 'LAMP SHOP OF NAPLES COMPANY', 'revenue': 0.0}, {'customer': 'LE GROUPE MULTI LUMINAIRE', 'revenue': 0.0}, {'customer': "SCHOENER'S INTERIORS  LLC", 'revenue': 0.0}, {'customer': 'FARADGI DESIGNS INC DBA CHIC H', 'revenue': 0.0}, {'customer': 'CORNELSON DECORATING INC', 'revenue': 0.0}, {'customer': 'ROYCE COLLECTION INC', 'revenue': 0.0}, {'customer': 'EXCEL LIGHTING & ELECTRICAL', 'revenue': 0.0}, {'customer': 'MID VALLEY LIGHTING INC.', 'revenue': 0.0}, {'customer': 'BILL RAY & ASSOCIATES', 'revenue': 0.0}, {'customer': 'FLA LIGHTING  INC', 'revenue': 0.0}, {'customer': 'CORDREY COLLECTION', 'revenue': 0.0}, {'customer': 'LUXE LIFESTYLES NYC', 'revenue': 0.0}, {'customer': 'PATTI DUPREE FURNITURE', 'revenue': 0.0}, {'customer': 'ARTISTIC ELEMENTS', 'revenue': 0.0}, {'customer': "LANDRY'S DEVELOPMENT INC", 'revenue': 0.0}, {'customer': 'ILLUMINA LLC', 'revenue': 0.0}, {'customer': 'DIVINE INTERIORS', 'revenue': 0.0}, {'customer': 'NEIMAN MARCUS', 'revenue': 0.0}, {'customer': 'INTERNATIONAL DESIGN SOURCE', 'revenue': 0.0}, {'customer': 'BISONOFFICE LLC', 'revenue': 0.0}, {'customer': 'LIGHT UP YOUR LIFE', 'revenue': 0.0}, {'customer': 'DECOR HOME CENTER', 'revenue': 0.0}, {'customer': 'DMS SALES INC.', 'revenue': 0.0}, {'customer': 'WHITE ROOM DESIGN LLC', 'revenue': 0.0}, {'customer': 'LIGHTING SOLUTIONS & DESIGN', 'revenue': 0.0}, {'customer': 'INTERIOR OBSESSION', 'revenue': 0.0}, {'customer': 'LEVEL DECORATIONS INC.', 'revenue': 0.0}, {'customer': 'Cash Customer', 'revenue': 0.0}, {'customer': 'KALCO NON A/R CASH', 'revenue': 0.0}, {'customer': 'GARBE INDUSTRIES INC  TU', 'revenue': 0.0}, {'customer': 'WILSON COMPANY-KANSAS', 'revenue': 0.0}, {'customer': "CAROL'S LIGHTING", 'revenue': 0.0}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 0.0}, {'customer': 'LANDO LIGHTING INC', 'revenue': 0.0}, {'customer': 'LAMPS PLUS', 'revenue': 0.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING ETC', 'revenue': 0.0}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 0.0}, {'customer': 'NORTHERN LIGHTING WESTERV', 'revenue': 0.0}, {'customer': 'ASHJIAN LIGHTING', 'revenue': 0.0}, {'customer': 'SUN LIGHTING', 'revenue': 0.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 0.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 0.0}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 0.0}, {'customer': 'FANWORLD', 'revenue': 0.0}] | [{'item': '030220-010', 'desc': 'Glacier LED ADA Wall Sconce', 'available': 27}, {'item': '030220-184', 'desc': 'Glacier 12-in (8-watt) LED Black Nickel Wall Sconce', 'available': 25}, {'item': '030250-184', 'desc': 'Glacier 42-in (40-watt) LED Black Nickel Wave Linear Chandelier', 'available': 19}, {'item': '030210-184', 'desc': 'Glacier 10-in (26-watt) LED Black Nickel Chandelier', 'available': 19}, {'item': '030260-184', 'desc': 'Glacier 48-in (108-watt) LED Black Nickel Linear Chandelier', 'available': 18}, {'item': '030258-184', 'desc': 'Glacier 60-in (60-watt) LED Black Nickel Wave Linear Chandelier', 'available': 16}, {'item': '030250-038', 'desc': 'Glacier 42 Inch LED Wave Island', 'available': 14}, {'item': '030233-038', 'desc': 'Glacier 32 Inch LED ADA Bath', 'available': 13}, {'item': '030258-038', 'desc': 'Glacier 60 Inch LED Wave Island', 'available': 13}, {'item': '030253-010', 'desc': 'Glacier 20 Inch LED Round Pendant', 'available': 12}, {'item': '030231-038', 'desc': 'Glacier 18 Inch LED ADA Bath', 'available': 12}, {'item': '030255-184', 'desc': 'Glacier 32-in (94-watt) LED Black Nickel Chandelier', 'available': 9}, {'item': '030230-010', 'desc': 'Glacier 12 Inch LED ADA Bath', 'available': 9}, {'item': '030260-038', 'desc': 'Glacier 48 Inch LED Island', 'available': 9}, {'item': '030255-010', 'desc': 'Glacier 32 Inch Round LED Pendant', 'available': 8}, {'item': '030252-038', 'desc': 'Glacier 36 Inch LED Rectangular Island', 'available': 8}, {'item': '030253-184', 'desc': 'Glacier 20-in (58-watt) LED Black Nickel Chandelier', 'available': 7}, {'item': '030251-038', 'desc': 'Glacier 26 Inch Rectangular LE', 'available': 7}, {'item': '030259-010', 'desc': 'Glacier 36 Inch Extra Large LED Foyer', 'available': 6}, {'item': '030256-038', 'desc': 'Glacier 25 + 32 Inch 2 Tier LED Round Pendant', 'available': 6}, {'item': '030234-010', 'desc': 'Glacier 38 Inch LED ADA Bath', 'available': 6}, {'item': '030257-010', 'desc': 'Glacier 60 Inch LED Round Pendant', 'available': 6}, {'item': '030210-038', 'desc': 'Glacier 10 Inch LED Mini Pendant', 'available': 3}, {'item': '030254-038', 'desc': 'Glacier 25 Inch LED Round Pendant', 'available': 2}, {'item': '030232-010', 'desc': 'Glacier 24 Inch LED ADA Bath', 'available': 1}] |
| 519221WB | Flint 1 Light Led  Convertible Wall Sconce/Mini Pendant | FLINT | 86,699.12 | 351 | — | 2026-6-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 10564.65}, {'customer': 'WAYFAIR LLC', 'revenue': 8597.07}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 7852.77}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 7113.22}, {'customer': 'VALLEY LGT GALLERY', 'revenue': 4819.14}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 4335.5}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 3506.4}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 2585.4}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 2308.9}, {'customer': 'BUILD.COM', 'revenue': 2022.02}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 1992.0}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 1832.54}, {'customer': 'ROBINSON LIGHTING LTD / PLYMOU', 'revenue': 1415.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 1303.9}, {'customer': 'LAMPS PLUS', 'revenue': 1212.3}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 1167.24}, {'customer': 'SUN LIGHTING', 'revenue': 1128.2}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 1035.84}, {'customer': 'ATELIER MAISON & CO', 'revenue': 1020.58}, {'customer': 'LIGHTING SUPERSTORE', 'revenue': 986.14}, {'customer': 'LEE SUPPLY CORP', 'revenue': 961.14}, {'customer': "BUTLER'S ELECTRIC", 'revenue': 945.44}, {'customer': 'PREMIER LIGHTING', 'revenue': 945.3}, {'customer': 'WASATCH LIGHTING', 'revenue': 797.0}, {'customer': 'NOVA LIGHTING', 'revenue': 790.35}, {'customer': 'GEORGIA LIGHTING', 'revenue': 749.49}, {'customer': 'INSIDE SOURCE', 'revenue': 650.9}, {'customer': 'FUSION LIGHT AND DESIGN LLC', 'revenue': 630.2}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 630.2}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 616.5}, {'customer': 'LIGHTING INC', 'revenue': 602.8}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 572.7}, {'customer': 'THE LIGHT HOUSE', 'revenue': 572.7}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 566.0}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 564.1}, {'customer': 'LIGHT LAB DESIGN', 'revenue': 557.76}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 549.02}, {'customer': 'INDIANA LIGHTING CENTER', 'revenue': 548.0}, {'customer': 'HAUS APPEAL LLC', 'revenue': 548.0}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 516.48}, {'customer': 'LIGHTING ETC', 'revenue': 498.0}, {'customer': 'LIGHTING FIRST / FT. MYERS', 'revenue': 498.0}, {'customer': 'NEIMAN MARCUS', 'revenue': 498.0}, {'customer': 'LIGHTING WAREHOUSE', 'revenue': 424.7}, {'customer': 'CAPITOL LIGHTING PARAMUS', 'revenue': 373.5}, {'customer': 'GROSS LIGHTING & HOME', 'revenue': 333.94}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 333.94}, {'customer': 'INLINE ELECTRIC SUPPLY CO', 'revenue': 333.94}, {'customer': 'KRELL LIGHTING', 'revenue': 293.82}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 286.35}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 283.0}, {'customer': 'LUXUR LIGHTING', 'revenue': 274.0}, {'customer': 'THE JARRELL COMPANY', 'revenue': 274.0}, {'customer': 'DEMENT LIGHTING', 'revenue': 274.0}, {'customer': 'RIVERSIDE LIGHTING', 'revenue': 249.0}, {'customer': 'RAY ELECTRIC', 'revenue': 236.55}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 205.5}, {'customer': 'GROSS ELECTRIC', 'revenue': 161.85}, {'customer': 'COBURN SUPPLY COMPANY', 'revenue': 141.5}, {'customer': 'MINNESOTA LIGHTING, FIREPLACE', 'revenue': 137.0}, {'customer': 'MI CASA LIGHTING AND FAN', 'revenue': 137.0}, {'customer': 'DHILLON LIGHTING', 'revenue': 124.5}, {'customer': 'DEKKER LIGHTING', 'revenue': 124.5}, {'customer': 'LEILI DESIGN STUDIO', 'revenue': 44.82}, {'customer': 'J H LARSON COMPANY', 'revenue': 44.82}, {'customer': 'MST LIGHTING INC.', 'revenue': 0.0}, {'customer': 'LIGHTING FACTORY OUTLET', 'revenue': 0.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 0.0}, {'customer': 'MAPLE RIDGE LIGHTING, INC. dba', 'revenue': 0.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 0.0}, {'customer': 'JACKSON LIGHTING SUPPLY', 'revenue': 0.0}, {'customer': 'UNIVERSAL LAMP', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 0.0}, {'customer': 'ARYA GROUP INC', 'revenue': 0.0}, {'customer': 'KITCHEN SOCIETY', 'revenue': 0.0}, {'customer': 'SABRINA ROSE INTERIORS', 'revenue': 0.0}, {'customer': 'MORGANTE WILSON ARCHITECTS', 'revenue': 0.0}, {'customer': 'TREVOR CAMERON DESIGNS', 'revenue': 0.0}, {'customer': 'LAMB HOME DESIGN', 'revenue': 0.0}, {'customer': 'IMPERIO HOME', 'revenue': 0.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 0.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 0.0}, {'customer': 'BIANCA SPINAZZOLA', 'revenue': 0.0}, {'customer': 'CARIBE SALES AGENCIES, INC.', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'ASHJIAN LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 0.0}, {'customer': 'CENTRAL BULB INC', 'revenue': 0.0}] | [{'item': '519273WB', 'desc': 'Flint 3 Light Multi-Drop Pendant', 'available': 45}] |
| 505820OL | Roxy 2 Light ADA Sconce | ROXY | 63,293.97 | 566 | — | 2026-6-28 | [{'customer': 'SHADES OF LIGHT', 'revenue': 18087.32}, {'customer': 'WAYFAIR LLC', 'revenue': 5692.92}, {'customer': 'BUILD.COM', 'revenue': 4009.0}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 2846.01}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 2672.2}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 2330.16}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 2279.16}, {'customer': 'BISONOFFICE LLC', 'revenue': 2104.8}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 1395.2}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 1303.4}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 1113.6}, {'customer': 'ELEMENTS AT HOME', 'revenue': 1008.0}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 881.6}, {'customer': 'HOUZZ SHOP LLC', 'revenue': 851.2}, {'customer': 'TALLAHASSEE LIGHTING FAN', 'revenue': 822.96}, {'customer': 'LIGHTING ETC', 'revenue': 672.0}, {'customer': 'CONNECTICUT LTG CENTER', 'revenue': 672.0}, {'customer': "HORTON'S OF LA GRANGE", 'revenue': 634.4}, {'customer': 'HAUS APPEAL LLC', 'revenue': 627.2}, {'customer': 'HOME LIGHTING OF PA', 'revenue': 604.16}, {'customer': 'CAPITOL LIGHTING--E. HANOVER', 'revenue': 596.0}, {'customer': 'SUN LIGHTING', 'revenue': 570.4}, {'customer': 'SHALLOTTE ELECTRIC STORES', 'revenue': 556.96}, {'customer': 'SISTER LIGHTING dba', 'revenue': 512.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 505.12}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 496.0}, {'customer': 'LAMPS EXPO/LAMPCLICK.COM', 'revenue': 448.0}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 448.0}, {'customer': 'CREGGER COMPANY  INC', 'revenue': 438.96}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 428.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 380.0}, {'customer': 'TIDEWATER LIGHTING AND DESIGN', 'revenue': 357.32}, {'customer': 'VENICE LIGHTING COMPANY', 'revenue': 336.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 325.92}, {'customer': 'STOKES ELECTRIC', 'revenue': 302.08}, {'customer': 'MANASQUAN LIGHTING', 'revenue': 292.64}, {'customer': 'SALTBOX THE', 'revenue': 292.64}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 285.2}, {'customer': 'CRESCENT LIGHITNG SUPPLY', 'revenue': 285.2}, {'customer': 'CAMINITI ASSOCIATE  INC  ILL', 'revenue': 285.2}, {'customer': 'LIFESTYLES STORES INC', 'revenue': 285.2}, {'customer': 'FRANKLIN LIGHTING INC', 'revenue': 264.32}, {'customer': 'CHARLES RINEK', 'revenue': 264.32}, {'customer': 'N&S ELECTRIC SUPPLY  INC', 'revenue': 264.32}, {'customer': 'LIGHTING FIRST - BONITA', 'revenue': 264.32}, {'customer': 'IMAGINE MORE SERVICES CORP.', 'revenue': 257.6}, {'customer': 'READ LIGHTING', 'revenue': 256.0}, {'customer': 'BRECHERS COMPANY', 'revenue': 248.0}, {'customer': 'PINE LIGHTING LTD', 'revenue': 240.8}, {'customer': 'LIGHT GALLERY PLUS', 'revenue': 240.8}, {'customer': 'ALL PHASE/TRAVERSE CITY', 'revenue': 224.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 224.0}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 224.0}, {'customer': '123STORES INC', 'revenue': 207.2}, {'customer': 'LAMPS PLUS', 'revenue': 201.6}, {'customer': 'LANDO LIGHTING INC', 'revenue': 201.6}, {'customer': 'M & M LIGHTING LP', 'revenue': 192.0}, {'customer': 'DEKKER LIGHTING', 'revenue': 132.16}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 128.0}, {'customer': 'CLEVELAND LIGHTING CENTER LTD', 'revenue': 124.0}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 100.8}, {'customer': 'KALCO NON A/R CASH', 'revenue': 0.0}, {'customer': 'SHOWCASE LIGHTING / LAREDO', 'revenue': 0.0}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 0.0}, {'customer': 'PHILLIPS LIGHTING & HOME', 'revenue': 0.0}, {'customer': 'LIGHTS N SUCH', 'revenue': 0.0}, {'customer': 'LIGHTING INC', 'revenue': 0.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 0.0}, {'customer': 'UNIVERSAL LAMP', 'revenue': 0.0}, {'customer': 'LIGHTHOUSE (THE)', 'revenue': 0.0}, {'customer': 'RAY ELECTRIC', 'revenue': 0.0}, {'customer': 'ASHJIAN LIGHTING', 'revenue': 0.0}, {'customer': 'DE LIGHT VILLE INC', 'revenue': 0.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 0.0}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 0.0}, {'customer': 'HOUSE OF LIGHTS INC', 'revenue': 0.0}, {'customer': 'LIGHTING EFX INC', 'revenue': 0.0}, {'customer': 'LIGHTSTYLES INC', 'revenue': 0.0}, {'customer': 'DIAL ELECTRIC SUPPLY CO.', 'revenue': 0.0}, {'customer': 'RENSENHOUSE OF LIGHTS', 'revenue': 0.0}, {'customer': 'BURR RIDGE LIGHTING & DESIGN C', 'revenue': 0.0}, {'customer': 'WILSON LIGHTING CO., INC / N.', 'revenue': 0.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 0.0}, {'customer': 'KILOHANA LIGHTING/LIHUE', 'revenue': 0.0}, {'customer': 'OCEAN PACIFIC LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 0.0}, {'customer': 'LIGHTSTYLES', 'revenue': 0.0}, {'customer': 'WALNUT CREEK LIGHTING', 'revenue': 0.0}, {'customer': 'CAROLINA LANTERNS & ACCS', 'revenue': 0.0}, {'customer': "CHRISTIE'S LTG GALLERY", 'revenue': 0.0}, {'customer': 'LEGEND LIGHTING INC.', 'revenue': 0.0}, {'customer': 'STRAIT FLOORS  INC', 'revenue': 0.0}, {'customer': 'NORTHWEST ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'MILLION DECOR DESIGN, INC.', 'revenue': 0.0}, {'customer': 'BAYSIDE ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'OLD NORTH STATE IMPORTS  LLC', 'revenue': 0.0}, {'customer': 'THE PORCH SWING STORE', 'revenue': 0.0}, {'customer': 'KALCO SHOWROOM ACCOUNT', 'revenue': 0.0}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 0.0}, {'customer': 'INSIDE OUT LIVING SPACES', 'revenue': 0.0}, {'customer': 'FEIFERS', 'revenue': 0.0}, {'customer': 'HEDGEAPPLE INC', 'revenue': 0.0}, {'customer': 'JONATHONS COASTAL LIVING', 'revenue': 0.0}, {'customer': 'INSIDE OUT LIGHTING & DECOR', 'revenue': 0.0}, {'customer': 'DEL MAR DESIGNS', 'revenue': 0.0}, {'customer': 'AFP 104 CORP', 'revenue': 0.0}, {'customer': 'DAWN PATTERSON INTERIORS', 'revenue': 0.0}, {'customer': 'INSPIRED INTERIORS', 'revenue': 0.0}, {'customer': 'LINDSEY GLASS', 'revenue': 0.0}, {'customer': 'GALAXIE LIGHTING', 'revenue': 0.0}] | [{'item': '505851OL', 'desc': 'Roxy 27 Inch Pendant', 'available': 115}, {'item': '505840OL', 'desc': 'Roxy 17 Inch Semi Flush Mount', 'available': 76}, {'item': '505860OL', 'desc': 'Roxy 42 Inch Island Light', 'available': 38}, {'item': '505891OL', 'desc': 'Roxy 1 Light Table Lamp', 'available': 32}, {'item': '505852OL', 'desc': 'Roxy 33 Inch Pendant', 'available': 21}, {'item': '505850OL', 'desc': 'Roxy 2 Tier Foyer', 'available': 11}] |
| 519276WB | Flint 3 Light Full Canopy Pendant | COL429 | 61,715.78 | 95 | — | 2026-6-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 18724.89}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 7973.63}, {'customer': 'DANIEL HOUSE CLUB', 'revenue': 5592.0}, {'customer': 'RAINBOW LIGHTING II LLC', 'revenue': 3271.7}, {'customer': 'BUILD.COM', 'revenue': 2058.65}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 1972.48}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 1688.2}, {'customer': 'LIGHT BULBS UNLIMITED BOCA RA', 'revenue': 1634.74}, {'customer': 'WILSON LIGHTING- NAPLES', 'revenue': 1384.2}, {'customer': 'WILSON COMPANY-KANSAS', 'revenue': 1384.2}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 1153.5}, {'customer': 'LEE SUPPLY CORP', 'revenue': 1072.27}, {'customer': 'ATELIER MAISON & CO', 'revenue': 999.7}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': 907.42}, {'customer': 'KRELL LIGHTING', 'revenue': 907.42}, {'customer': 'SUBURBAN WHOLESALE LTG', 'revenue': 907.42}, {'customer': 'SUNBELT FANS & LTG LAUREL', 'revenue': 907.42}, {'customer': 'CAMINITI ASSOCIATES INC. / SCO', 'revenue': 884.35}, {'customer': 'DESIGNER LIGHTING & FAN/DECOR', 'revenue': 772.39}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 769.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 769.0}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 769.0}, {'customer': 'DEL MAR DESIGNS', 'revenue': 730.55}, {'customer': 'LAMPS PLUS', 'revenue': 713.7}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 692.1}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 576.75}, {'customer': 'IB LIGHTING SUPPLY', 'revenue': 576.75}, {'customer': 'DEMENT LIGHTING', 'revenue': 454.35}, {'customer': 'WILSON 6 ENTERPRISE', 'revenue': 384.5}, {'customer': 'LIGHTING SPECIALISTS', 'revenue': 384.5}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 349.5}, {'customer': 'M & M LIGHTING LP', 'revenue': 349.5}, {'customer': '31 DESIGNS', 'revenue': 0.0}, {'customer': 'WOLBERG ELECTRICAL SUPPLY', 'revenue': 0.0}, {'customer': 'KTR ASSOCIATES [INACTIVE]', 'revenue': 0.0}, {'customer': 'WAYFAIR LLC', 'revenue': 0.0}, {'customer': 'GOING GROUP  LLC  THE', 'revenue': 0.0}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 0.0}, {'customer': 'FORESIGHT LIGHTING (DO NOT USE)', 'revenue': 0.0}, {'customer': 'LEGACY LIGHTING, LLC.', 'revenue': 0.0}, {'customer': 'SAVE MORE PLUMBING & LIGHTING', 'revenue': 0.0}, {'customer': "WILKINSON'S HOUSE OF LTS", 'revenue': 0.0}, {'customer': 'IMPERIO HOME', 'revenue': 0.0}, {'customer': 'NOVA LIGHTING', 'revenue': 0.0}, {'customer': 'GUIDED HOME DESIGN', 'revenue': 0.0}, {'customer': 'EFIRDS INTERIORS', 'revenue': 0.0}] | — |
| 520555OL | Crescent 6 Light Pendant | COL435 | 45,102.15 | 100 | — | 2026-6-28 | [{'customer': 'LIGHTING FIRST - BONITA', 'revenue': 5050.48}, {'customer': 'BUILD.COM', 'revenue': 3834.6}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 3509.73}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 3176.46}, {'customer': 'LIGHTING FIRST', 'revenue': 2314.6}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 2268.57}, {'customer': 'ROBINSON LIGHTING LTD.', 'revenue': 1531.4}, {'customer': 'PROGRESSIVE LIGHTING', 'revenue': 1379.7}, {'customer': 'RENSENHOUSE OF LIGHTS', 'revenue': 1277.57}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 1172.5}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 1032.0}, {'customer': 'CONNECTICUT LTG CENTER', 'revenue': 1013.16}, {'customer': "CAROL'S LIGHTING", 'revenue': 985.0}, {'customer': 'WAYFAIR LLC', 'revenue': 928.8}, {'customer': 'SISTER LIGHTING dba', 'revenue': 790.0}, {'customer': 'OLD WORLD STONE IMPORTS', 'revenue': 734.85}, {'customer': 'NORTHERN LIGHTING WESTERV', 'revenue': 608.88}, {'customer': 'KING ELECTRIC COMPANY INC', 'revenue': 608.88}, {'customer': 'BLACK WHALE LIGHTING', 'revenue': 593.4}, {'customer': 'DOMINION ELECTRIC SUPPLY DBA BORDER STATES', 'revenue': 562.85}, {'customer': 'CREGGER COMPANY  INC', 'revenue': 553.42}, {'customer': 'COLEY ELECTRIC AND PLUMBING', 'revenue': 553.42}, {'customer': 'LIGHTING SUPERSTORE', 'revenue': 553.42}, {'customer': 'INDIANA LIGHTING CENTER', 'revenue': 553.42}, {'customer': 'BRIGHT IDEAS LIGHTING & MORE', 'revenue': 539.35}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 539.35}, {'customer': 'THE JARRELL COMPANY', 'revenue': 516.0}, {'customer': 'WALNUT CREEK LIGHTING', 'revenue': 516.0}, {'customer': 'MARS ELECTRIC COMPANY', 'revenue': 516.0}, {'customer': 'BEAUTIFUL THINGS LIGHTING', 'revenue': 505.4}, {'customer': 'RAY ELECTRIC', 'revenue': 490.2}, {'customer': 'MONTREAL LIGHTING & HARDWARE,', 'revenue': 469.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 469.0}, {'customer': 'CAPITAL ELECTRIC', 'revenue': 469.0}, {'customer': 'ROBINSON LIGHTING LTD / PLYMOU', 'revenue': 469.0}, {'customer': '1-800-MY-LAMPS', 'revenue': 469.0}, {'customer': 'BELAMI, INC / 1STOP LIGHTING', 'revenue': 454.93}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 445.55}, {'customer': 'LEEWAL LLC', 'revenue': 438.6}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 387.0}, {'customer': 'CAPITOL LIGHTING BOCA RATON', 'revenue': 387.0}, {'customer': 'VILLAGE LIGHTING', 'revenue': 328.3}, {'customer': 'PHILLIPS LIGHTING & HOME', 'revenue': 309.6}, {'customer': 'HYDROLOGIC CORPORATE', 'revenue': 234.5}, {'customer': "CHRISTIE'S LTG GALLERY", 'revenue': 234.5}, {'customer': 'CARRINGTON LIGHTING', 'revenue': 234.5}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 93.8}, {'customer': 'LAMP SHOP OF NAPLES COMPANY', 'revenue': 0.0}, {'customer': 'LIGHTING FIRST / FT. MYERS', 'revenue': 0.0}, {'customer': 'ALLOWAY LIGHTING COMPANY', 'revenue': 0.0}, {'customer': 'CENTRAL BULB INC', 'revenue': 0.0}, {'customer': 'LUMINOSA LIGHT DESIGN', 'revenue': 0.0}, {'customer': 'INTERIOR WORKS', 'revenue': 0.0}, {'customer': 'J H LARSON COMPANY', 'revenue': 0.0}, {'customer': 'URBAN LIGHTS', 'revenue': 0.0}, {'customer': 'SHALLOTTE ELECTRIC STORES', 'revenue': 0.0}, {'customer': 'BYG INC.', 'revenue': 0.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 0.0}, {'customer': 'PARK LIGHTING', 'revenue': 0.0}, {'customer': 'ILLUMINATIONS MC ALLEN', 'revenue': 0.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'TURN-ON LIGHTING', 'revenue': 0.0}, {'customer': 'LIGHTTRENDS.COM', 'revenue': 0.0}, {'customer': 'EAST INDIES TRADING DBA WEST HOME COLLECTION', 'revenue': 0.0}, {'customer': 'GRAHAMS LIGHTING INC FRANKLI', 'revenue': -0.54}] | [{'item': '520541OL', 'desc': 'Crescent 4 Light Flush Mount', 'available': 24}, {'item': '520521OL', 'desc': 'Crescent 3 Light Ada Wall Sconce', 'available': 15}, {'item': '520561OL', 'desc': 'Crescent 5 Light Island', 'available': 7}] |
| 509952WB | Lavo 39 Inch Round LED Pendant | LAVO | 43,929.98 | 54 | — | 2026-7-12 | [{'customer': 'LUMENS LIGHT & LIVING', 'revenue': 12714.54}, {'customer': 'ILLUMINATIONS LIGHTING', 'revenue': 3624.0}, {'customer': 'SOUTHERN LIGHTING INC', 'revenue': 2883.05}, {'customer': 'NORTH COAST ELECTRIC', 'revenue': 2661.0}, {'customer': 'LIGHTOPIA, LLC', 'revenue': 1952.0}, {'customer': 'MUSKA LIGHTING CENTER', 'revenue': 1952.0}, {'customer': 'CAPITOL LIGHTING / 1-800LIGHTI', 'revenue': 1530.3}, {'customer': 'GRANITE CITY ELECTRIC', 'revenue': 1224.66}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 1151.68}, {'customer': 'INLINE ELECTRIC SUPPLY CO', 'revenue': 1151.68}, {'customer': 'NAPLES LIGHTING & FAN DEPOT', 'revenue': 1046.66}, {'customer': 'FANWORLD', 'revenue': 1020.05}, {'customer': 'COAST LIGHTING', 'revenue': 1006.0}, {'customer': 'PINE TREE LIGHTING', 'revenue': 976.0}, {'customer': "HINKLEY'S LTG FACTORY", 'revenue': 976.0}, {'customer': 'KALCO MARKETING CRM', 'revenue': 976.0}, {'customer': 'LIGHTING DESIGN COMPANY', 'revenue': 976.0}, {'customer': 'FEI  FERGUSON MAIN ACCOUNT', 'revenue': 975.7}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 927.2}, {'customer': 'LAMPS PLUS', 'revenue': 905.4}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 887.0}, {'customer': 'URBAN LIGHTS', 'revenue': 887.0}, {'customer': 'LITTMAN BROTHERS BROTHERS', 'revenue': 878.4}, {'customer': 'SUNBELT FANS & LTG LAUREL', 'revenue': 488.0}, {'customer': "RICHARD'S LIGHTING", 'revenue': 159.66}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': 'UNION ELECTRIC LIGHTING - TORO', 'revenue': 0.0}, {'customer': 'LIGHTING NEW YORK (INTERNET)', 'revenue': 0.0}, {'customer': 'LIGHTING WAREHOUSE', 'revenue': 0.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 0.0}, {'customer': 'CAMINITI ASSOCIATE  INC  ILL', 'revenue': 0.0}, {'customer': 'LBX LIGHTING INC', 'revenue': 0.0}, {'customer': 'PARK LIGHTING', 'revenue': 0.0}, {'customer': 'KEIDEL SUPPLY CO. INC.', 'revenue': 0.0}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 0.0}, {'customer': 'INSPIRED LIVING STORES', 'revenue': 0.0}, {'customer': 'AZTEC LIGHTING INC', 'revenue': 0.0}, {'customer': 'STATELY LLC', 'revenue': 0.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 0.0}, {'customer': 'LIGHTING FACTORY OUTLET', 'revenue': 0.0}, {'customer': 'STYLEUP CORPORATION', 'revenue': 0.0}, {'customer': 'SUN LIGHTING', 'revenue': 0.0}, {'customer': 'SEMCO ELECTRIC', 'revenue': 0.0}, {'customer': 'SUPPLY HOLDING', 'revenue': 0.0}, {'customer': 'ONE SOURCE LIGHTING', 'revenue': 0.0}, {'customer': 'ILC STUDIOS', 'revenue': 0.0}, {'customer': 'AARON THOMAS INTERIORS', 'revenue': 0.0}, {'customer': 'I.D. HOME LOGISTICS INC', 'revenue': 0.0}, {'customer': 'SCOUT LIGHTING', 'revenue': 0.0}, {'customer': 'ALDER AND TWEED DESIGN CO.', 'revenue': 0.0}, {'customer': 'LIGHTING SOLUTIONS & DESIGN', 'revenue': 0.0}, {'customer': 'A A PORTER LTG CO (DO NOT CONTACT)', 'revenue': 0.0}] | [{'item': '509921WB', 'desc': 'Lavo LED ADA Wall Sconce', 'available': 25}, {'item': '509950WB', 'desc': 'Lavo 28 Inch Round LED Pendant', 'available': 13}] |
