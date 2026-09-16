# Section 2 Context Bundle — Currey & Company (cci)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=57730, portal_order_gmv=$87.6M |
| HAS_INVENTORY | True | inventory_count=3443 |
| HAS_SALES_DATA | True | sales_data_count=110748 |
| HAS_SALES_SECTION | True | mode=orders order_reps=37 engagement_reps=0 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$87.6M > ecat_gmv=$8.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 37 | 37 |
| ENGAGEMENT_REP_COUNT | 0 |  |
| SALES_SECTION_MODE | orders | orders |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 76 rows |
| SHOWROOM_EXCLUSIONS | 3 | 3 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3985, Mixpanel total submit_order (Q-01): 6616 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.4%, ambiguous_rate=0.0%, showroom_event_share=8.5% |
| USER_GROUP_JOIN_RATE | 97% | 74 of 76 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 9% | showroom+admin share of matched events: 8.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Atlanta Showroom, CC Dallas Showroom, Highpoint Showroom, Allan Otto |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=2 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=53 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=7906 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=369 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=3184 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Currey & Company
- **Shortname**: cci
- **Org ID**: 161
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Currey & Company (cci, org_id=161)
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

# Signal Rank — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Total signals fired**: 56 (P0: 34, P1: 21, P2: 1)
- **Org GMV**: $8.6M eCat LTM, $87.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 8 reps at 0% eCat capture on $31.5M total business | P1 | §5 Team | 252.0 | $31,500,000 | 2.0 | 15,876,000,000 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — 9000-0135/9000-0143 co-purchase pattern across 77 customers | P0 | §2/§3 | 7.7 | $32,879,194 | 2.0 | 506,339,588 | POSITIVE |
| 3 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $13.9M+ total business, zero eCat orders | P1 | §2 Accounts | 13.9 | $13,861,823 | 2.0 | 384,300,274 | POSITIVE |
| 4 | SIG-COMMERCE-01 | Capture Rate — eCat captures 9.8% of $88M total business; each +1pt = $876K | P0 | §4 Commerce | 4.5 | $876,000 | 3.0 | 11,850,000 | POSITIVE |
| 5 | SIG-MOM-01 | Account Acceleration — LILLIAN JAMES DESIGN GROUP 4 consecutive QoQ acceleration quarters, $110,380 peak quarter (+934% QoQ) | P0 | §2 Accounts | 31.1 | $110,380 | 3.0 | 10,312,818 | POSITIVE |
| 6 | SIG-ANOMALY-03 | Competitive Displacement — DEFINED INTERIORS total biz +541% but eCat -100% | P0 | §2 Accounts | 42.7 | $57,855 | 3.0 | 7,413,567 | RISK |
| 7 | SIG-MOM-01 | Account Acceleration — BAY DESIGN 3 consecutive QoQ acceleration quarters, $78,913 peak quarter (+925% QoQ) | P0 | §2 Accounts | 30.8 | $78,913 | 3.0 | 7,298,634 | POSITIVE |
| 8 | SIG-MOM-01 | Account Acceleration — WILSON LIGHTING - OVERLAND PRK 2 consecutive QoQ acceleration quarters, $77,581 peak quarter (+616% QoQ) | P0 | §2 Accounts | 20.5 | $77,581 | 3.0 | 4,779,784 | POSITIVE |
| 9 | SIG-MOM-01 | Account Acceleration — WESTEND PROPERTIES LTD 2 consecutive QoQ acceleration quarters, $112,801 peak quarter (+404% QoQ) | P0 | §2 Accounts | 13.5 | $112,801 | 3.0 | 4,553,775 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration — CROMWELL AUSTRALIA PTY LTD 2 consecutive QoQ acceleration quarters, $100,868 peak quarter (+418% QoQ) | P0 | §2 Accounts | 13.9 | $100,868 | 3.0 | 4,218,293 | POSITIVE |
| 11 | SIG-DECAY-04 | Spending Contraction — BEYOND INC -77.4% YoY ($306,714→$69,264), $237,450 gap | P0 | §2 Accounts | 3.9 | $237,450 | 3.0 | 2,756,791 | RISK |
| 12 | SIG-DECAY-04 | Spending Contraction — DESIGNSOURCE INTERNATIONAL -70.8% YoY ($327,412→$95,532), $231,880 gap | P0 | §2 Accounts | 3.5 | $231,880 | 3.0 | 2,462,566 | RISK |
| 13 | SIG-MOM-01 | Account Acceleration — ROBB & STUCKY INTERNATIONAL 2 consecutive QoQ acceleration quarters, $96,623 peak quarter (+187% QoQ) | P0 | §2 Accounts | 6.2 | $96,623 | 3.0 | 1,806,850 | POSITIVE |
| 14 | SIG-DECAY-04 | Spending Contraction — LAMPS.COM -55.3% YoY ($324,958→$145,295), $179,663 gap | P0 | §2 Accounts | 2.8 | $179,663 | 3.0 | 1,490,306 | RISK |
| 15 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 53% of eCat GMV | P1 | §4 Commerce | 1.3 | $541,073 | 2.0 | 1,431,238 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — CAI DESIGNS 2 consecutive QoQ acceleration quarters, $133,301 peak quarter (+105% QoQ) | P0 | §2 Accounts | 3.5 | $133,301 | 3.0 | 1,394,326 | POSITIVE |
| 17 | SIG-MOM-01 | Account Acceleration — FURNITURELAND SOUTH 2 consecutive QoQ acceleration quarters, $139,458 peak quarter (+98% QoQ) | P0 | §2 Accounts | 3.3 | $139,458 | 3.0 | 1,363,902 | POSITIVE |
| 18 | SIG-ANOMALY-03 | Competitive Displacement — ROBB & STUCKY INTERNATIONAL total biz +55% but eCat -20% | P0 | §2 Accounts | 5.0 | $88,611 | 3.0 | 1,329,164 | RISK |
| 19 | SIG-DECAY-03 | Rep Trajectory — Rip Nance orders -37.9% QoQ, $105,764 current 90d GMV | P1 | §5 Team | 1.5 | $423,056 | 2.0 | 1,282,706 | RISK |
| 20 | SIG-DECAY-03 | Rep Trajectory — Atlanta Showroom orders -40.5% QoQ, $92,410 current 90d GMV | P1 | §5 Team | 1.6 | $369,640 | 2.0 | 1,197,634 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 33 | 1 | 0 | 34 | |
| §3 Product Intelligence | 0 | 0 | 1 | 1 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 8 | 0 | 8 | |
| §6 Platform Context | 0 | 11 | 0 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 8 reps at 0% eCat capture on $31.5M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 9000-0135/9000-0143 co-purchase pattern across 77 customers
3. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $13.9M+ total business, zero eCat orders
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 9.8% of $88M total business; each +1pt = $876K
5. **[RISK]** SIG-ANOMALY-03: Competitive Displacement — DEFINED INTERIORS total biz +541% but eCat -100%
6. **[RISK]** SIG-DECAY-04: Spending Contraction — BEYOND INC -77.4% YoY ($306,714→$69,264), $237,450 gap
7. **[RISK]** SIG-DECAY-04: Spending Contraction — DESIGNSOURCE INTERNATIONAL -70.8% YoY ($327,412→$95,532), $231,880 gap

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | FURNITURELAND SOUTH | 2 | DECAY-01, MOM-01 | $139,458 |
| 2 | ROBB & STUCKY INTERNATIONAL | 2 | ANOMALY-03, MOM-01 | $96,623 |
| 3 | TRIBUS DESIGN STUDIO | 1 | DECAY-01 | $94,994 |
| 4 | THE DECORATORS UNLIMITED | 1 | DECAY-01 | $33,119 |
| 5 | BLACK SHEEP INTERIORS | 1 | DECAY-01 | $25,383 |
| 6 | DESIGN SPECIFICATIONS, INC. | 1 | DECAY-01 | $31,485 |
| 7 | BEYOND INC | 1 | DECAY-04 | $237,450 |
| 8 | DESIGNSOURCE INTERNATIONAL | 1 | DECAY-04 | $231,880 |
| 9 | POTTERY BARN | 1 | DECAY-04 | $201,128 |
| 10 | LAMPS.COM | 1 | DECAY-04 | $179,663 |

### Q-12_results.md

# Q-12 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 38,964 | 3,926 | 1,710 | 1,050 | 685 |

### Q-14_results.md

# Q-14 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| BAER 2 | BAER' S FURNITURE COMPANY | 105 | $160,324 | 2025-07-31 23:45:25 | 2026-05-29 18:25:23 | 2.90 |
| CLIVE D | CLIVE DANIEL HOME | 52 | $74,459 | 2025-06-25 21:10:38 | 2026-06-17 15:33:51 | 7 |
| LIBUMC | LIGHTING IN STYLE | 50 | $39,988 | 2025-07-10 23:44:56 | 2026-06-16 16:18:04 | 7 |
| RS INTL | ROBB & STUCKY INTERNATIONAL | 50 | $94,796 | 2025-07-15 00:18:17 | 2026-06-12 22:32:47 | 6.80 |
| AWELL | A WELL DRESSED HOME | 41 | $50,689 | 2025-06-26 17:38:18 | 2026-06-05 21:34:28 | 8.60 |
| 0003564 | TRIBUS DESIGN STUDIO | 41 | $94,994 | 2025-07-02 13:45:32 | 2026-05-22 17:42:11 | 8.10 |
| VITOCH | VITOCH INTERIORS | 32 | $32,736 | 2025-06-19 19:06:17 | 2026-06-12 14:44:36 | 11.50 |
| ST LGT | METRO LIGHTING, ST LOUIS | 31 | $36,326 | 2025-07-25 17:35:07 | 2026-06-17 16:53:48 | 10.90 |
| NTDTX | NORTH TEXAS DESIGN GROUP | 31 | $50,140 | 2025-06-20 14:29:07 | 2026-06-08 20:14:26 | 11.80 |
| DEC UNL | THE DECORATORS UNLIMITED | 28 | $33,119 | 2025-06-25 18:35:36 | 2026-04-20 15:25:12 | 11.10 |
| DWS | DESIGN WORKS STUDIO, INC. NC | 28 | $29,292 | 2025-07-02 05:53:19 | 2026-06-09 20:49:29 | 12.70 |
| 0003330 | BUNNY WILLIAMS HOME | 26 | $37,492 | 2025-06-20 14:32:13 | 2026-06-16 18:14:24 | 14.40 |
| LYTE | LYTEWORKS | 24 | $28,628 | 2025-06-24 14:33:20 | 2026-06-09 22:11:02 | 15.20 |
| VOSSDES | VOSS DESIGNS | 22 | $32,484 | 2025-06-21 00:24:41 | 2026-06-17 21:21:15 | 17.20 |
| PULTE | PULTE INTERIORS | 21 | $27,514 | 2025-07-12 00:00:10 | 2026-06-01 21:26:03 | 16.20 |
| KCID | KELLY CARON DESIGNS | 21 | $31,100 | 2025-07-01 16:47:06 | 2026-05-25 16:38:02 | 16.40 |
| 0015859 | FIRST COAST LIGHTING AND FANS | 20 | $37,499 | 2025-07-01 15:01:05 | 2026-05-19 14:08:04 | 16.90 |
| 0014980 | NAPLES LIGHTING & FAN DEPOT | 20 | $22,736 | 2025-06-26 19:55:49 | 2026-06-12 00:10:24 | 18.40 |
| MEDER | BLACK SHEEP INTERIORS | 19 | $25,383 | 2025-06-30 15:05:03 | 2026-04-17 19:04:54 | 16.20 |
| CHD 3 | CUSTOM HOME DECORATING | 19 | $18,592 | 2025-07-28 19:47:44 | 2026-05-08 12:58:55 | 15.80 |

### Q-14b_results.md

# Q-14b Results — Currey & Company (cci, org_id=161)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| LIGHTOP | LIGHTOPIA | 594 | 0.80 | 1.20 | 1.50 | $363,315 |
| 0005698 | POTTERY BARN | 880 | 0.50 | 0.90 | 1.80 | $350,389 |
| GOFRAN | GOODFORM FRANCE AND SON | 280 | 1.60 | 2.70 | 1.69 | $204,921 |
| THE CAR | THE CARROLL COMPANIES | 8 | 40.70 | 77 | 1.89 | $155,686 |
| LAM CO | LAMPS.COM | 402 | 1.20 | 2 | 1.67 | $145,295 |
| AMBERIN | AMBER INTERIORS | 276 | 1.70 | 2.70 | 1.59 | $139,159 |
| 0017963 | LIV DESIGN PARTNERS | 15 | 17.60 | 30.10 | 1.71 | $133,850 |
| UNITED | DIRECTBUY OPERATIONS LLC | 119 | 3.80 | 6.20 | 1.63 | $124,349 |
| DESINTL | DESIGNSOURCE INTERNATIONAL | 43 | 10.80 | 16.50 | 1.53 | $95,532 |
| CORKYS | CORKY'S FOOTWEAR INC. | 11 | 7.80 | 34.50 | 4.42 | $88,403 |
| 0001338 | FISH OUT OF WATER DESIGNS | 5 | 11.70 | 174.50 | 14.91 | $85,015 |
| 0012008 | LIGHT HOUSE CO | 156 | 3 | 4.70 | 1.57 | $82,701 |
| 0010851 | STEVEN SHELL LIVING | 28 | 14 | 26.70 | 1.91 | $82,450 |
| ANT SAN | ANTHEM | 20 | 17.10 | 41.70 | 2.44 | $80,071 |
| JGASTON | JAN GASTON INTERIORS | 47 | 8.10 | 15.30 | 1.89 | $70,815 |

### Q-17_results.md

# Q-17 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | NC | 2026-02-20 01:33:15 | 10 | $105,944 |
| TAL | TALAMORE AT OAK TERRACE | PA | 2026-02-09 18:06:26 | 1 | $46,696 |
| 0021471 | FONDA LANDHOLDINGS AND DESIGN | WI | 2026-01-29 22:44:09 | 2 | $30,910 |
| 0021046 | Palette and Parlor | NC | 2025-09-06 20:09:50 | 1 | $28,897 |
| 0008629 | FLOOR CO LLC | MS | 2025-09-25 00:49:18 | 1 | $28,506 |
| 0011082 | INTERIOR MARKETING GROUP | NY | 2025-08-21 21:15:45 | 2 | $28,038 |
| 0009768 | NATHAN VANAGS DESIGN | FL | 2026-03-11 00:09:34 | 5 | $27,482 |
| CRE & D | CREATIVE INTERIORS AND DESIGN | WA | 2026-02-09 17:13:24 | 1 | $24,340 |
| 0006755 | SAVANNAH COLLEGE OF ART DESIGN | GA | 2025-10-06 17:23:06 | 3 | $22,627 |
| CORKYS | CORKY'S FOOTWEAR INC. | AR | 2025-10-15 15:50:22 | 1 | $20,616 |
| GRAC NC | GRACE DESIGN | NC | 2026-02-12 18:21:51 | 5 | $20,208 |
| JST NC | JST INTERIOR DESIGN | NC | 2025-11-21 20:58:46 | 1 | $19,625 |
| 0019845 | MIRROR LAKE INNN | NY | 2025-08-11 17:00:25 | 2 | $18,855 |
| WHIRLY | WHIRLYGIG DESIGNS | NC | 2025-08-15 16:59:53 | 3 | $17,833 |
| CFI | CAROLINA FURNITURE & INTERIORS | SC | 2025-06-25 23:13:06 | 1 | $16,944 |
| ELEKTRA | ELEKTRA LIGHTS & FANS, INC. | WI | 2026-02-25 21:52:05 | 2 | $16,682 |
| SCB | SAYBROOK HOME | CT | 2025-08-27 15:47:32 | 1 | $16,576 |
| 0005339 | BRITANY SIMON DESIGN | AZ | 2025-11-06 15:55:20 | 1 | $16,310 |
| 0005879 | REFLECTIONS L & M | NJ | 2025-09-17 13:43:17 | 5 | $16,264 |
| DCI 2 | COLLUM DESIGNS | TX | 2026-03-10 21:42:49 | 9 | $16,215 |
| WILSON3 | WILSON LIGHTING - ST. LOUIS | MO | 2026-01-20 17:53:27 | 11 | $15,462 |
| 0010671 | COTTAGE & LOFT INTERIORS | FL | 2026-03-16 16:48:50 | 2 | $15,102 |
| LIT DIR | LIGHTS DIRECT | MO | 2026-02-18 21:09:42 | 7 | $14,780 |
| 0005509 | CREATIVE TONIC | TX | 2025-11-19 20:59:43 | 4 | $14,754 |
| MGD | MICHELE GREEN DESIGN | CT | 2026-03-02 19:52:15 | 8 | $14,650 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Currey & Company (cci, org_id=161)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | NC | $105,944 | 2026-02-20 01:33:15 | 118 |
| TAL | TALAMORE AT OAK TERRACE | PA | $46,696 | 2026-02-09 18:06:26 | 128 |
| 0021471 | FONDA LANDHOLDINGS AND DESIGN | WI | $30,910 | 2026-01-29 22:44:09 | 139 |
| 0021046 | Palette and Parlor | NC | $28,897 | 2025-09-06 20:09:50 | 284 |
| 0008629 | FLOOR CO LLC | MS | $28,506 | 2025-09-25 00:49:18 | 266 |
| 0011082 | INTERIOR MARKETING GROUP | NY | $28,038 | 2025-08-21 21:15:45 | 300 |
| 0009768 | NATHAN VANAGS DESIGN | FL | $27,482 | 2026-03-11 00:09:34 | 99 |
| 0020371 | NATALIE CROSBY CONSULTING | GA | $25,176 | 2026-03-19 17:25:43 | 90 |
| CRE & D | CREATIVE INTERIORS AND DESIGN | WA | $24,340 | 2026-02-09 17:13:24 | 128 |
| 0006755 | SAVANNAH COLLEGE OF ART DESIGN | GA | $22,627 | 2025-10-06 17:23:06 | 254 |
| CORKYS | CORKY'S FOOTWEAR INC. | AR | $20,616 | 2025-10-15 15:50:22 | 245 |
| GRAC NC | GRACE DESIGN | NC | $20,208 | 2026-02-12 18:21:51 | 125 |
| JST NC | JST INTERIOR DESIGN | NC | $19,625 | 2025-11-21 20:58:46 | 208 |
| 0019845 | MIRROR LAKE INNN | NY | $18,855 | 2025-08-11 17:00:25 | 310 |
| WHIRLY | WHIRLYGIG DESIGNS | NC | $17,833 | 2025-08-15 16:59:53 | 306 |
| CFI | CAROLINA FURNITURE & INTERIORS | SC | $16,944 | 2025-06-25 23:13:06 | 357 |
| ELEKTRA | ELEKTRA LIGHTS & FANS, INC. | WI | $16,682 | 2026-02-25 21:52:05 | 112 |
| SCB | SAYBROOK HOME | CT | $16,576 | 2025-08-27 15:47:32 | 294 |
| 0005339 | BRITANY SIMON DESIGN | AZ | $16,310 | 2025-11-06 15:55:20 | 223 |
| 0005879 | REFLECTIONS L & M | NJ | $16,264 | 2025-09-17 13:43:17 | 273 |

### Q-40_results.md

# Q-40 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| FL | 221 | 812 | $1.6M |
| NC | 136 | 293 | $758,544 |
| TX | 179 | 370 | $653,024 |
| GA | 130 | 234 | $639,493 |
| SC | 74 | 265 | $522,530 |
| NY | 109 | 268 | $513,458 |
| AL | 79 | 150 | $385,175 |
| NJ | 76 | 177 | $347,808 |
| AZ | 73 | 162 | $332,369 |
| CA | 67 | 160 | $284,351 |
| PA | 43 | 99 | $235,094 |
| IL | 45 | 84 | $208,672 |
| TN | 39 | 67 | $153,383 |
| VA | 45 | 72 | $153,152 |
| MO | 21 | 84 | $144,469 |
| CT | 24 | 56 | $137,032 |
| MS | 25 | 54 | $135,547 |
| MA | 44 | 66 | $113,878 |
| KY | 16 | 45 | $104,464 |
| MD | 32 | 60 | $93,872 |

### Q-41_results.md

# Q-41 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 40 |
| 2025-04-01 | Rep-Acquired (iPad) | 75 |
| 2025-05-01 | Rep-Acquired (iPad) | 77 |
| 2025-06-01 | Rep-Acquired (iPad) | 58 |
| 2025-07-01 | Rep-Acquired (iPad) | 62 |
| 2025-08-01 | Rep-Acquired (iPad) | 84 |
| 2025-09-01 | Rep-Acquired (iPad) | 85 |
| 2025-10-01 | Rep-Acquired (iPad) | 66 |
| 2025-11-01 | Rep-Acquired (iPad) | 76 |
| 2025-12-01 | Rep-Acquired (iPad) | 63 |
| 2026-01-01 | Rep-Acquired (iPad) | 53 |
| 2026-02-01 | Rep-Acquired (iPad) | 81 |
| 2026-03-01 | Rep-Acquired (iPad) | 90 |
| 2026-04-01 | Rep-Acquired (iPad) | 75 |
| 2026-05-01 | Rep-Acquired (iPad) | 64 |
| 2026-06-01 | Rep-Acquired (iPad) | 60 |

### Q-41_rep_results.md

# Q-41-rep Results — Currey & Company (cci, org_id=161)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 43
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| CC Dallas Showroom | 149 |
| Stacie Baker | 105 |
| Shephalli Jain | 58 |
| Lesley Blair | 54 |
| Stacey Chiavetta | 51 |
| Stewart Haviland | 49 |
| Russ Jones | 48 |
| Joanie Martin | 46 |
| Atlanta Showroom | 46 |
| Rip Nance | 41 |
| Kinshasa Floyd | 39 |
| Jodie Veeder | 36 |
| Betty Robbins | 35 |
| Michael  Mosko | 31 |
| Mindy McEntire | 29 |
| Randy Gould | 28 |
| Margarethe Martin | 28 |
| Carrie Haymore | 27 |
| Rob Nance | 26 |
| Kristy Orison | 20 |
| Sandy Glosson | 20 |
| Nancy Hubbard | 16 |
| Tanner Gould | 14 |
| Brigette Fontenot | 14 |
| Deborah Wilson | 13 |
| Patty Miller | 12 |
| Mary Miller | 8 |
| Tim Shelton | 8 |
| Highpoint Showroom | 6 |
| Cindy Rogers | 6 |
| Carey Yount | 6 |
| Lee Kram | 6 |
| Natalie Murphy | 5 |
| Ornella Avakian | 5 |
| Kristin Ireland | 4 |
| Jess Remillard | 4 |
| Eliza Brantley | 3 |
| Penny Gould | 3 |
| Beth Cousins | 3 |
| Sandy Nakatsu | 3 |
| Alexsis Lopez | 2 |
| Nicole Casanova | 1 |
| Vivi Mira-Culmer | 1 |

### Q-52_results.md

# Q-52 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WAYFAIR | WAYFAIR | MA | 8,537 | $4.7M | 0 | $0 | 0 |
| BENNING | LUMENS | CA | 1,695 | $1.4M | 0 | $0 | 0 |
| FER ENT | FERGUSON ENTERPRISES | VA | 940 | $1.3M | 2 | $8,577 | 0.70 |
| IMPROV | FERGUSON HOME | CA | 1,241 | $1.1M | 0 | $0 | 0 |
| NY LITE | LIGHTING NEW YORK | PA | 1,363 | $1.0M | 0 | $0 | 0 |
| LAMPS + | LAMPS PLUS | CA | 1,519 | $978,616 | 0 | $0 | 0 |
| CL BOCA | CAPITOL LIGHTING - BOCA RATON | FL | 938 | $954,269 | 0 | $0 | 0 |
| FURLAND | FURNITURELAND SOUTH | NC | 312 | $427,003 | 10 | $105,944 | 24.80 |
| LGTOLGY | LIGHTOLOGY | IL | 373 | $394,641 | 0 | $0 | 0 |
| KAT KUO | KATHY KUO DESIGNS | NY | 569 | $371,303 | 0 | $0 | 0 |
| CAI | CAI DESIGNS | IL | 312 | $368,823 | 3 | $14,479 | 3.90 |
| LIGHTOP | LIGHTOPIA | CA | 408 | $363,315 | 0 | $0 | 0 |
| 0005698 | POTTERY BARN | MS | 464 | $350,389 | 0 | $0 | 0 |
| FOUNDRY | FOUNDRY LIGHTING | NY | 424 | $329,990 | 0 | $0 | 0 |
| 0011923 | LULU AND GEORGIA | CA | 639 | $327,172 | 0 | $0 | 0 |
| RS INTL | ROBB & STUCKY INTERNATIONAL | FL | 80 | $273,429 | 50 | $94,796 | 34.70 |
| BAER 2 | BAER' S FURNITURE COMPANY | FL | 200 | $266,319 | 105 | $160,324 | 60.20 |
| CROMWEL | CROMWELL AUSTRALIA PTY LTD | AU | 45 | $261,188 | 0 | $0 | 0 |
| CLIVE D | CLIVE DANIEL HOME | FL | 82 | $233,369 | 52 | $74,459 | 31.90 |
| THETREA | THE TREASURE CHEST | FL | 1 | $215,418 | 0 | $0 | 0 |
| SAFAVIE | SAFAVIEH HOME & CARPET | NY | 257 | $210,376 | 5 | $14,632 | 7 |
| GOFRAN | GOODFORM FRANCE AND SON | NY | 220 | $204,921 | 0 | $0 | 0 |
| 0010221 | IVY HOME | VA | 188 | $204,293 | 0 | $0 | 0 |
| 0009681 | DANIEL HOUSE CLUB | OR | 249 | $202,325 | 0 | $0 | 0 |
| WIL | WILSON LIGHTING OF NAPLES | FL | 80 | $181,716 | 6 | $37,270 | 20.50 |
| LGT INC | LIGHTING INC | TX | 60 | $180,273 | 1 | $308 | 0.20 |
| HAV 001 | HAVERTY'S FURNITURE COMPANIES | GA | 335 | $177,635 | 0 | $0 | 0 |
| SMITHE | W E SMITHE | IL | 125 | $174,220 | 2 | $3,402 | 2 |
| GLOBE | GLOBE LIGHTING | OR | 101 | $172,515 | 0 | $0 | 0 |
| WILSON | WILSON LIGHTING - OVERLAND PRK | KS | 58 | $170,625 | 1 | $1,996 | 1.20 |

### Q-53_results.md

# Q-53 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| WAYFAIR | WAYFAIR | MA | 8,537 | $4.7M |
| BENNING | LUMENS | CA | 1,695 | $1.4M |
| IMPROV | FERGUSON HOME | CA | 1,241 | $1.1M |
| NY LITE | LIGHTING NEW YORK | PA | 1,363 | $1.0M |
| LAMPS + | LAMPS PLUS | CA | 1,519 | $978,616 |
| CL BOCA | CAPITOL LIGHTING - BOCA RATON | FL | 938 | $954,269 |
| LGTOLGY | LIGHTOLOGY | IL | 373 | $394,641 |
| KAT KUO | KATHY KUO DESIGNS | NY | 569 | $371,303 |
| LIGHTOP | LIGHTOPIA | CA | 408 | $363,315 |
| 0005698 | POTTERY BARN | MS | 464 | $350,389 |
| FOUNDRY | FOUNDRY LIGHTING | NY | 424 | $329,990 |
| 0011923 | LULU AND GEORGIA | CA | 639 | $327,172 |
| CROMWEL | CROMWELL AUSTRALIA PTY LTD | AU | 45 | $261,188 |
| THETREA | THE TREASURE CHEST | FL | 1 | $215,418 |
| GOFRAN | GOODFORM FRANCE AND SON | NY | 220 | $204,921 |
| 0010221 | IVY HOME | VA | 188 | $204,293 |
| 0009681 | DANIEL HOUSE CLUB | OR | 249 | $202,325 |
| HAV 001 | HAVERTY'S FURNITURE COMPANIES | GA | 335 | $177,635 |
| GLOBE | GLOBE LIGHTING | OR | 101 | $172,515 |
| BCI LLC | BYRON CHANDLER INTERIORS, LLC | FL | 2 | $153,833 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FL | 819 | 5,153 | $11.2M | 221 | 812 | $1.6M | 14.30 |
| CA | 574 | 8,611 | $8.8M | 67 | 160 | $284,351 | 3.20 |
| GA | 527 | 3,336 | $6.1M | 130 | 234 | $639,493 | 10.50 |
| MA | 250 | 9,253 | $5.8M | 44 | 66 | $113,878 | 2 |
| TX | 778 | 2,800 | $5.4M | 179 | 370 | $653,024 | 12.10 |
| NC | 446 | 2,219 | $4.9M | 136 | 293 | $758,544 | 15.40 |
| NY | 359 | 2,732 | $3.6M | 109 | 268 | $513,458 | 14.30 |
| VA | 226 | 2,058 | $3.4M | 45 | 72 | $153,152 | 4.50 |
| SC | 291 | 1,574 | $3.0M | 74 | 265 | $522,530 | 17.50 |
| PA | 220 | 2,669 | $2.9M | 43 | 99 | $235,094 | 8 |
| IL | 180 | 1,997 | $2.7M | 45 | 84 | $208,672 | 7.80 |
| AL | 215 | 868 | $2.2M | 79 | 150 | $385,175 | 17.50 |
| TN | 278 | 1,064 | $2.2M | 39 | 67 | $153,383 | 7.10 |
| AZ | 201 | 706 | $1.8M | 73 | 162 | $332,369 | 18.80 |
| NJ | 245 | 978 | $1.8M | 76 | 177 | $347,808 | 19.80 |
| OH | 167 | 811 | $1.5M | 5 | 7 | $20,180 | 1.40 |
| UT | 117 | 893 | $1.3M | 11 | 24 | $39,073 | 2.90 |
| MS | 75 | 1,098 | $1.2M | 25 | 54 | $135,547 | 11.20 |
| LA | 103 | 495 | $1.1M | 12 | 17 | $50,185 | 4.50 |
| CO | 152 | 517 | $1.1M | 21 | 30 | $70,896 | 6.40 |

### Q-57_results.md

# Q-57 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

# Q-66 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-66 — Buyer-Within-Account Intelligence
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | new_buyers | existing_buyers | new_buyer_orders | new_buyer_revenue | earliest_new_buyer |
| --- | --- | --- | --- | --- | --- |
| THE TREASURE CHEST | 1 | 0 | 1 | 175,944 | 2026-4-28 |
| ALERIE GARRETT | 1 | 0 | 1 | 112,423.50 | 2026-4-28 |
| ALEM DICKEY DESIGNED INTERIORS | 2 | 1 | 2 | 103,875 | 2026-4-26 |
| LILLIAN JAMES DESIGN GROUP | 2 | 1 | 3 | 93,019.40 | 2026-4-26 |
| J PEACH INTERIORS | 2 | 0 | 2 | 92,834.70 | 2026-4-25 |
| COLEY ELECTRIC & PLUMBING SUPP | 1 | 12 | 1 | 87,606 | 2026-6-13 |
| CROMWELL AUSTRALIA PTY LTD | 1 | 0 | 2 | 87,586.55 | 2026-4-26 |
| THE CARROLL COMPANIES | 1 | 1 | 1 | 86,950 | 2026-4-27 |
| FISH OUT OF WATER DESIGNS | 1 | 0 | 2 | 85,015 | 2026-4-6 |
| BAYSIDE INTERIORS | 1 | 0 | 1 | 75,210 | 2026-4-25 |
| ROOM AT THE BEACH | 2 | 0 | 2 | 70,978 | 2026-4-27 |
| METRY INTERIORS DBA I.C. | 3 | 0 | 3 | 70,464 | 2026-4-26 |
| BAY DESIGN | 2 | 1 | 3 | 66,560 | 2026-5-27 |
| VINEYARD BUILDING | 1 | 12 | 1 | 65,856 | 2026-6-13 |
| DEFINED INTERIORS | 1 | 0 | 1 | 63,048 | 2026-4-26 |
| JOHN RUDOLPH DESIGNS | 1 | 0 | 2 | 58,516 | 2026-5-4 |
| THREAD DESIGN GROUP | 1 | 0 | 2 | 54,215 | 2026-4-26 |
| FEATHERS CUSTOM FURNITURE, INC | 1 | 2 | 2 | 53,338 | 2026-4-1 |
| ECLECTIC HOME | 3 | 0 | 4 | 48,436 | 2026-4-13 |
| PINEAPPLE PARK | 1 | 1 | 1 | 45,898 | 2026-4-24 |

### Q-67_results.md

# Q-67 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FL | $3.0M | $4.6M | 51.30 | 656 | 608 | 48 | 2,059 |
| GA | $1.6M | $2.5M | 51.50 | 315 | 312 | 3 | 1,467 |
| TX | $1.3M | $1.9M | 44.40 | 402 | 381 | 21 | 1,296 |
| NC | $1.1M | $1.8M | 67.30 | 345 | 267 | 78 | 920 |
| CA | $1.4M | $1.3M | -5.80 | 316 | 345 | -29 | 1,143 |
| NY | $571,662 | $942,113 | 64.80 | 220 | 183 | 37 | 716 |
| SC | $786,471 | $926,778 | 17.80 | 228 | 222 | 6 | 604 |
| TN | $475,054 | $789,040 | 66.10 | 194 | 152 | 42 | 479 |
| VA | $366,847 | $736,908 | 100.90 | 169 | 118 | 51 | 410 |
| AL | $593,375 | $657,198 | 10.80 | 148 | 135 | 13 | 325 |
| NJ | $405,861 | $634,158 | 56.30 | 157 | 136 | 21 | 460 |
| AZ | $520,042 | $611,572 | 17.60 | 113 | 130 | -17 | 312 |
| IL | $338,675 | $550,009 | 62.40 | 138 | 107 | 31 | 444 |
| PA | $356,855 | $501,553 | 40.50 | 142 | 137 | 5 | 370 |
| MA | $389,885 | $455,329 | 16.80 | 184 | 160 | 24 | 454 |
| OH | $317,937 | $431,765 | 35.80 | 128 | 105 | 23 | 290 |
| CO | $263,626 | $409,443 | 55.30 | 104 | 105 | -1 | 273 |
| MI | $243,238 | $342,419 | 40.80 | 86 | 75 | 11 | 246 |
| LA | $219,748 | $337,688 | 53.70 | 84 | 69 | 15 | 197 |
| IN | $181,228 | $308,536 | 70.20 | 65 | 60 | 5 | 159 |
| MD | $162,645 | $297,975 | 83.20 | 115 | 79 | 36 | 236 |
| KY | $180,278 | $288,478 | 60 | 64 | 47 | 17 | 132 |
| CT | $205,869 | $254,768 | 23.80 | 99 | 95 | 4 | 223 |
| UT | $396,425 | $252,973 | -36.20 | 83 | 80 | 3 | 179 |
| MO | $205,268 | $227,680 | 10.90 | 48 | 54 | -6 | 132 |

### Q-68_results.md

# Q-68 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| HG BUYING CORP | TX | $58,282 | $260,270 | $201,988 | 22.40 | 2 |
| DESIGNSOURCE INTERNATIONAL | Unknown | $137,465 | $312,994 | $175,529 | 43.90 | 10 |
| WALT DISNEY WORLD COMPANY | FL | $1,785 | $168,232 | $166,447 | 1.10 | 3 |
| HOLIDAY BEACH DECOR | PA | $14,827 | $132,412 | $117,585 | 11.20 | 5 |
| THE SHOWROOM AT FURNITURE ROW | CO | $16,008 | $131,337 | $115,329 | 12.20 | 3 |
| AMANDA OWENS DESIGN INC | GA | $7,518 | $114,044 | $106,526 | 6.60 | 4 |
| HAVERTY'S FURNITURE COMPANIES | VA | $192,875 | $296,619 | $103,744 | 65 | 13 |
| HOM FURNITURE, INC. | MN | $50,590 | $151,849 | $101,259 | 33.30 | 12 |
| SOURCE | NV | $19,542 | $118,583 | $99,041 | 16.50 | 7 |
| ROOM AT THE BEACH | CA | $96,580 | $192,027 | $95,447 | 50.30 | 10 |
| THE BRASS BED | AL | $26,668 | $115,297 | $88,629 | 23.10 | 2 |
| KRISTA WATTERWORTH DSGN STUDIO | FL | $37,491 | $125,876 | $88,384 | 29.80 | 9 |
| GREEN GATES MARKET | AL | $9,291 | $92,519 | $83,228 | 10 | 3 |
| CONSTRUCTION RESOURCES COMPANY | GA | $26,791 | $110,003 | $83,213 | 24.40 | 9 |
| JOSHUA G YOUNGNER INTERIORS | GA | $9,285 | $90,640 | $81,355 | 10.20 | 2 |
| A PROPER GARDEN | OH | $10,189 | $88,180 | $77,991 | 11.60 | 2 |
| TABLE AND CHAIR SHOP | FL | $17,552 | $95,219 | $77,667 | 18.40 | 7 |
| FERWERDA INTERIOR DESIGN | FL | $1,872 | $77,509 | $75,637 | 2.40 | 3 |
| CUVEE DESIGN & DEVELOPMENT | CO | $1,424 | $76,538 | $75,114 | 1.90 | 1 |
| LIFESTYLES STORES, INC. | OK | $28,687 | $102,468 | $73,781 | 28 | 11 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 5
- **Run date**: 2026-06-17


| customer_num | customer_name | state | ltm_orders | ltm_gmv | last_order | days_since_last | avg_days_between | decay_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | NC | 10 | $105,944 | 2026-02-20 01:33:15 | 118 | 33.70 | 3.50 |
| 0003564 | TRIBUS DESIGN STUDIO | SC | 41 | $94,994 | 2026-05-22 17:42:11 | 26 | 8.90 | 2.90 |
| DEC UNL | THE DECORATORS UNLIMITED | FL | 28 | $33,119 | 2026-04-20 15:25:12 | 58 | 12.60 | 4.60 |
| MEDER | BLACK SHEEP INTERIORS | GA | 19 | $25,383 | 2026-04-17 19:04:54 | 61 | 16.90 | 3.60 |
| DESSPEC | DESIGN SPECIFICATIONS, INC. | FL | 17 | $31,485 | 2026-04-09 17:56:06 | 69 | 26.90 | 2.60 |

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0011923 | LULU AND GEORGIA | 79000-0461-1LG | SERPENTINA BRASS CHANDELIER, C | 21 | 14.60 | 184 | 12.60 | 11,520 | DECAY_DETECTED |
| LAMPS + | LAMPS PLUS | 9881 | CRYSTAL LIGHTS LARGE GOLD CHAN | 20 | 22.30 | 101 | 4.50 | 27,262.72 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 9251 | BAYOU SEAGLASS PENDANT | 24 | 13.30 | 37 | 2.80 | 39,793.60 | SLOWING |
| WAYFAIR | WAYFAIR | 9000-0157 | AGAVE AMERICANA GOLD CHANDELIE | 8 | 30.90 | 174 | 5.60 | 16,800 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 4142 | AGORA CONSOLE TABLE | 8 | 29.50 | 232 | 7.90 | 9,990.20 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 6000-0218 | CAIT GREEN TABLE LAMP | 85 | 5.90 | 15 | 2.50 | 28,394.60 | SLOWING |
| WAYFAIR | WAYFAIR | 3252 | MOROMBE COCOA CREDENZA | 5 | 43.40 | 167 | 3.80 | 17,376.80 | DECAY_DETECTED |
| IMPROV | FERGUSON HOME | 9000-0750 | DAZE LARGE PENDANT | 26 | 17.30 | 71 | 4.10 | 15,377.24 | DECAY_DETECTED |
| AMBERIN | AMBER INTERIORS | 9873 | BRUSSELS BLACK CHANDELIER | 9 | 28 | 163 | 5.80 | 10,752 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 6000-0758 | MALVASIA BRASS DESK LAMP | 19 | 19.90 | 108 | 5.40 | 10,486.40 | DECAY_DETECTED |
| BENNING | LUMENS | 9000-0574 | DAZE MEDIUM PENDANT | 34 | 13.70 | 55 | 4 | 13,710.40 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 6000-0805 | PICCOLO BROWN MINI TABLE LAMP | 66 | 7.30 | 49 | 6.70 | 7,076 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 4000-0063 | PIAF GOLD DRINKS TABLE | 98 | 5.30 | 14 | 2.60 | 17,279 | SLOWING |
| 0009327 | MCGEE & CO | 9000-0008 | BASTIAN LARGE CHESTNUT LANTERN | 14 | 28.40 | 106 | 3.70 | 11,616 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 4189 | PASCAL BRASS ACCENT TABLE | 60 | 8.70 | 22 | 2.50 | 17,113.60 | SLOWING |
| WAYFAIR | WAYFAIR | 6000-0645 | LUCENT BLUE TABLE LAMP | 24 | 16 | 122 | 7.60 | 5,480.60 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 3000-0142 | EVIE SHAGREEN CREDENZA | 7 | 51 | 128 | 2.50 | 16,156.80 | SLOWING |
| NY LITE | LIGHTING NEW YORK | 9000-0818 | LUNARIA SMALL SILVER CHANDELIE | 19 | 23.20 | 93 | 4 | 9,576 | DECAY_DETECTED |
| LAM CO | LAMPS.COM | 9000-0135 | NOTTAWAY LARGE BRONZE CHANDELI | 11 | 27.30 | 199 | 7.30 | 5,152 | DECAY_DETECTED |
| 0005698 | POTTERY BARN | 9000-0757 | SAXON LARGE TAN CHANDELIER | 17 | 23.60 | 76 | 3.20 | 10,543.20 | DECAY_DETECTED |
| HAV 001 | HAVERTY'S FURNITURE COMPANIES | L090-0023 | AVERY CHANDELIER | 35 | 13.70 | 63 | 4.60 | 7,350 | DECAY_DETECTED |
| 0005698 | POTTERY BARN | 9000-0754 | SHIPWRIGHT CHANDELIER | 13 | 30.10 | 101 | 3.40 | 9,548.40 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 1200-0897 | RUE DE BAC LARGE BUTTERFLIES | 67 | 7.50 | 27 | 3.60 | 8,764.80 | DECAY_DETECTED |
| SHADES | SHADES OF LIGHT | 9000-0735 | ROUSHAM WHITE CHANDELIER | 5 | 46.40 | 254 | 5.50 | 5,700 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 9000-1168 | ARCHETYPE CHANDELIER | 11 | 36 | 101 | 2.80 | 10,751.20 | SLOWING |
| BENNING | LUMENS | 9857 | ADMIRAL PENDANT | 8 | 35.30 | 204 | 5.80 | 5,135.20 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 6000-0022 | LILOU GREEN TABLE LAMP | 38 | 13.20 | 36 | 2.70 | 9,568 | SLOWING |
| FOUNDRY | FOUNDRY LIGHTING | 5000-0064 | MALVASIA BRASS WALL SCONCE | 27 | 17.80 | 57 | 3.20 | 8,100 | DECAY_DETECTED |
| WAYFAIR | WAYFAIR | 9188 | SEAWARD LARGE WHITE CHANDELIER | 8 | 35.40 | 147 | 4.20 | 5,702.40 | DECAY_DETECTED |
| IMPROV | FERGUSON HOME | 9000-0655 | TIRRELL LARGE BLACK CHANDELIER | 6 | 49.70 | 201 | 4 | 5,688.60 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 50
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | 427,002.52 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| SAFAVIE | SAFAVIEH HOME & CARPET | 210,376.26 | 9000-0143 | Nottaway Small Bronze Chandelier | 9000-0135 | Nottaway Large Bronze Chandelier | 77 |
| GOFRAN | GOODFORM FRANCE AND SON | 204,921.44 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| 0003564 | TRIBUS DESIGN STUDIO | 151,892.32 | 9000-0143 | Nottaway Small Bronze Chandelier | 9000-0135 | Nottaway Large Bronze Chandelier | 77 |
| LLGA | LEGACY LIGHTING | 145,365.64 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| SHADES | SHADES OF LIGHT | 142,258.40 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| AMBERIN | AMBER INTERIORS | 139,159.47 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| NRIIL | LUXE DECOR | 137,206 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| 0004257 | HEDGEAPPLE | 131,097.31 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0143 | Nottaway Small Bronze Chandelier | 77 |
| LAMPS + | LAMPS PLUS | 978,615.75 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| FURLAND | FURNITURELAND SOUTH | 427,002.52 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| CROMWEL | CROMWELL AUSTRALIA PTY LTD | 261,187.92 | 9267 | Saxon Large Black Chandelier | 9000-0135 | Nottaway Large Bronze Chandelier | 63 |
| SAFAVIE | SAFAVIEH HOME & CARPET | 210,376.26 | 9267 | Saxon Large Black Chandelier | 9000-0135 | Nottaway Large Bronze Chandelier | 63 |
| 0010221 | IVY HOME | 204,293.28 | 9267 | Saxon Large Black Chandelier | 9000-0135 | Nottaway Large Bronze Chandelier | 63 |
| WILSON | WILSON LIGHTING - OVERLAND PRK | 170,624.61 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| GRAHAMS | GRAHAM'S LIGHTING - FRANKLIN | 166,765.80 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| 0009327 | MCGEE & CO | 158,025.14 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| LLGA | LEGACY LIGHTING | 145,365.64 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| LAM CO | LAMPS.COM | 145,295.24 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| SHADES | SHADES OF LIGHT | 142,258.40 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| VAL LIG | VALLEY LIGHT GALLERY | 128,761.49 | 9000-0135 | Nottaway Large Bronze Chandelier | 9267 | Saxon Large Black Chandelier | 63 |
| LAMPS + | LAMPS PLUS | 978,615.75 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0574 | Daze Medium Pendant | 54 |
| FURLAND | FURNITURELAND SOUTH | 427,002.52 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0574 | Daze Medium Pendant | 54 |
| 0005698 | POTTERY BARN | 350,389.38 | 9000-0574 | Daze Medium Pendant | 9000-0135 | Nottaway Large Bronze Chandelier | 54 |
| 0011923 | LULU AND GEORGIA | 327,171.61 | 9000-0574 | Daze Medium Pendant | 9000-0135 | Nottaway Large Bronze Chandelier | 54 |
| SAFAVIE | SAFAVIEH HOME & CARPET | 210,376.26 | 9000-0574 | Daze Medium Pendant | 9000-0135 | Nottaway Large Bronze Chandelier | 54 |
| 0010221 | IVY HOME | 204,293.28 | 9000-0574 | Daze Medium Pendant | 9000-0135 | Nottaway Large Bronze Chandelier | 54 |
| 0009681 | DANIEL HOUSE CLUB | 202,325.18 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0574 | Daze Medium Pendant | 54 |
| WILSON | WILSON LIGHTING - OVERLAND PRK | 170,624.61 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0574 | Daze Medium Pendant | 54 |
| DOM EL | DOMINION ELECTRIC | 169,812.73 | 9000-0135 | Nottaway Large Bronze Chandelier | 9000-0574 | Daze Medium Pendant | 54 |

*(Truncated: showing top 30 of 50 rows. Full data in cache file.)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0014861 | BEYOND INC | UT | 69,264.44 | 306,714.11 | -77.40 | 0 | 0 | — | CONTRACTING |
| DESINTL | DESIGNSOURCE INTERNATIONAL | NC | 95,532.35 | 327,412.39 | -70.80 | 0 | 0 | — | CONTRACTING |
| 0005698 | POTTERY BARN | MS | 350,389.38 | 551,517.55 | -36.50 | 0 | 0 | — | CONTRACTING |
| LAM CO | LAMPS.COM | PA | 145,295.24 | 324,958.42 | -55.30 | 0 | 0 | — | CONTRACTING |
| ACCOM | YVONNE WANG DESIGNS | WI | 191,914 | 329,295.60 | -41.70 | 0 | 0 | — | CONTRACTING |
| 0018034 | LILLIAN JAMES DESIGN GROUP | AZ | 128,001.74 | 572.30 | 22,266.20 | 0 | 485 | -100 | COMPETITIVE_DISPLACEMENT |
| HAV 001 | HAVERTY'S FURNITURE COMPANIES | GA | 177,634.98 | 288,085.88 | -38.30 | 0 | 0 | — | CONTRACTING |
| SMITHE | WALTER E SMITHE | IL | 192,366.14 | 290,692.28 | -33.80 | 3,402 | 0 | — | CONTRACTING |
| RS INTL | ROBB & STUCKY INTERNATIONAL | FL | 273,428.54 | 176,171.29 | 55.20 | 94,796.40 | 118,147.93 | -19.80 | COMPETITIVE_DISPLACEMENT |
| INTL DE | INTERNATIONAL DESIGN SOURCE | FL | 118,495.50 | 201,176.73 | -41.10 | 0 | 0 | — | CONTRACTING |
| WIL | WILSON LIGHTING OF NAPLES | FL | 181,715.63 | 255,788.60 | -29 | 37,269.60 | 22,523.17 | 65.50 | CONTRACTING |
| SHADES | SHADES OF LIGHT | VA | 142,258.40 | 213,485.39 | -33.40 | 0 | 0 | — | CONTRACTING |
| 0001316 | KRISTA WATTERWORTH DSGN STUDIO | FL | 43,979.49 | 115,002.24 | -61.80 | 36,793.96 | 48,311.97 | -23.80 | CONTRACTING |
| UN LITE | UNION LIGHTING | QC | 90,433.09 | 160,413.48 | -43.60 | 1,392 | 27,063.65 | -94.90 | CONTRACTING |
| DAVANT | DIANNE DAVANT INTERIORS | NC | 53,581.63 | 123,086.90 | -56.50 | 2,116.60 | 2,971.60 | -28.80 | CONTRACTING |
| HGB HOM | HG BUYING CORP | MA | 43,262.51 | 112,222 | -61.40 | 0 | 0 | — | CONTRACTING |
| MATTER | MATTER BROTHERS  FURNITURE | FL | 97,467.96 | 166,405.62 | -41.40 | 26,390.40 | 44,080 | -40.10 | CONTRACTING |
| 0019345 | LITTLE MOUNTAIN HOME | SC | 100,149.96 | 35,277.05 | 183.90 | 1,884 | 2,384 | -21 | COMPETITIVE_DISPLACEMENT |
| 0012926 | DEFINED INTERIORS | FL | 76,768.80 | 11,982.36 | 540.70 | 0 | 9,030 | -100 | COMPETITIVE_DISPLACEMENT |
| MCLAIN | KIM MCLAIN INTERIORS | LA | 95,053.49 | 156,882.73 | -39.40 | 0 | 7,206 | -100 | CONTRACTING |
| 0004292 | JMT INTERIORS | FL | 59,911.39 | 1,816.56 | 3,198.10 | 0 | 1,566 | -100 | COMPETITIVE_DISPLACEMENT |
| USA | US DEPARTMENT OF STATE*DNMS | VA | 37,510 | 94,895.99 | -60.50 | 0 | 0 | — | CONTRACTING |
| COL LGT | CONSTRUCTION RESOURCES COMPANY | GA | 29,127.34 | 85,178.78 | -65.80 | 0 | 8,733.60 | -100 | CONTRACTING |
| ZZACCOM | WATTS HUMPHREY | TX | 88,806.55 | 144,821.24 | -38.70 | 5,824 | 739.97 | 687.10 | CONTRACTING |
| THE BB | THE BRASS BED | AL | 26,555.56 | 82,279.52 | -67.70 | 22,876 | 10,896 | 109.90 | CONTRACTING |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| FURLAND | FURNITURELAND SOUTH | 2 | 139,458.28 | 97.80 | [{'quarter': '2025-07-01', 'revenue': 139458.28, 'qoq_pct': 70.2}, {'quarter': '2025-10-01', 'revenue': 52229.4, 'qoq_pct': -62.5}, {'quarter': '2026-01-01', 'revenue': 103300.04, 'qoq_pct': 97.8}, {'quarter': '2026-04-01', 'revenue': 126422.8, 'qoq_pct': 22.4}] |
| CAI | CAI DESIGNS | 2 | 133,300.78 | 104.60 | [{'quarter': '2025-07-01', 'revenue': 61333.09, 'qoq_pct': -44.0}, {'quarter': '2025-10-01', 'revenue': 103610.67, 'qoq_pct': 68.9}, {'quarter': '2026-01-01', 'revenue': 65149.39, 'qoq_pct': -37.1}, {'quarter': '2026-04-01', 'revenue': 133300.78, 'qoq_pct': 104.6}] |
| PARK CO | WESTEND PROPERTIES LTD | 2 | 112,800.97 | 403.70 | [{'quarter': '2025-07-01', 'revenue': 22666.97, 'qoq_pct': 184.2}, {'quarter': '2025-10-01', 'revenue': 22284.96, 'qoq_pct': -1.7}, {'quarter': '2026-01-01', 'revenue': 112245.56, 'qoq_pct': 403.7}, {'quarter': '2026-04-01', 'revenue': 112800.97, 'qoq_pct': 0.5}] |
| 0018034 | LILLIAN JAMES DESIGN GROUP | 4 | 110,380.16 | 934.30 | [{'quarter': '2025-07-01', 'revenue': 2329.32, 'qoq_pct': 307.0}, {'quarter': '2025-10-01', 'revenue': 4620.48, 'qoq_pct': 98.4}, {'quarter': '2026-01-01', 'revenue': 10671.78, 'qoq_pct': 131.0}, {'quarter': '2026-04-01', 'revenue': 110380.16, 'qoq_pct': 934.3}] |
| THE CAR | THE CARROLL COMPANIES | 2 | 107,670.30 | 43,496.50 | [{'quarter': '2025-10-01', 'revenue': 47768.25, 'qoq_pct': 1943.7}, {'quarter': '2026-01-01', 'revenue': 246.97, 'qoq_pct': -99.5}, {'quarter': '2026-04-01', 'revenue': 107670.3, 'qoq_pct': 43496.5}] |
| 0016744 | MELISSA FISCHER INTERIORS | 2 | 103,962.72 | 5,381 | [{'quarter': '2025-07-01', 'revenue': 103962.72, 'qoq_pct': 5381.0}, {'quarter': '2025-10-01', 'revenue': 1019.52, 'qoq_pct': -99.0}, {'quarter': '2026-01-01', 'revenue': 23477.28, 'qoq_pct': 2202.8}] |
| CROMWEL | CROMWELL AUSTRALIA PTY LTD | 2 | 100,867.84 | 418.20 | [{'quarter': '2025-07-01', 'revenue': 19463.64, 'qoq_pct': -79.4}, {'quarter': '2025-10-01', 'revenue': 100867.84, 'qoq_pct': 418.2}, {'quarter': '2026-01-01', 'revenue': 34355.42, 'qoq_pct': -65.9}, {'quarter': '2026-04-01', 'revenue': 96668.63, 'qoq_pct': 181.4}] |
| WYNNDES | WYNN DESIGN & DEVELOPMENT | 2 | 99,534 | 1,773.90 | [{'quarter': '2026-01-01', 'revenue': 19334.0, 'qoq_pct': 1773.9}, {'quarter': '2026-04-01', 'revenue': 99534.0, 'qoq_pct': 414.8}] |
| RS INTL | ROBB & STUCKY INTERNATIONAL | 2 | 96,623 | 187 | [{'quarter': '2025-07-01', 'revenue': 33671.0, 'qoq_pct': 109.2}, {'quarter': '2025-10-01', 'revenue': 96623.0, 'qoq_pct': 187.0}, {'quarter': '2026-01-01', 'revenue': 70869.38, 'qoq_pct': -26.7}, {'quarter': '2026-04-01', 'revenue': 72265.16, 'qoq_pct': 2.0}] |
| SAFAVIE | SAFAVIEH HOME & CARPET | 2 | 91,187.70 | 128.10 | [{'quarter': '2025-07-01', 'revenue': 19378.65, 'qoq_pct': -64.1}, {'quarter': '2025-10-01', 'revenue': 44200.87, 'qoq_pct': 128.1}, {'quarter': '2026-01-01', 'revenue': 54935.84, 'qoq_pct': 24.3}, {'quarter': '2026-04-01', 'revenue': 91187.7, 'qoq_pct': 66.0}] |
| BENWEST | RYMAN HOSPITALITY PROPERTIES, INC | 2 | 85,705.31 | 1,915.30 | [{'quarter': '2025-07-01', 'revenue': 4252.69, 'qoq_pct': 193.0}, {'quarter': '2025-10-01', 'revenue': 85705.31, 'qoq_pct': 1915.3}, {'quarter': '2026-01-01', 'revenue': 21507.3, 'qoq_pct': -74.9}, {'quarter': '2026-04-01', 'revenue': 12253.73, 'qoq_pct': -43.0}] |
| LEX FUR | LEXINGTON FURNITURE | 2 | 81,451.22 | 4,196 | [{'quarter': '2025-07-01', 'revenue': 81451.22, 'qoq_pct': 4196.0}, {'quarter': '2025-10-01', 'revenue': 1138.48, 'qoq_pct': -98.6}, {'quarter': '2026-01-01', 'revenue': 4448.0, 'qoq_pct': 290.7}] |
| HOS PUR | HOSPITALITY PURVEYORS LLC | 2 | 80,327.68 | 1,084.50 | [{'quarter': '2025-07-01', 'revenue': 14041.0, 'qoq_pct': -60.8}, {'quarter': '2025-10-01', 'revenue': 1363.0, 'qoq_pct': -90.3}, {'quarter': '2026-01-01', 'revenue': 16144.88, 'qoq_pct': 1084.5}, {'quarter': '2026-04-01', 'revenue': 80327.68, 'qoq_pct': 397.5}] |
| BAY DES | BAY DESIGN | 3 | 78,912.68 | 924.90 | [{'quarter': '2025-07-01', 'revenue': 824.0, 'qoq_pct': -72.7}, {'quarter': '2025-10-01', 'revenue': 8444.8, 'qoq_pct': 924.9}, {'quarter': '2026-01-01', 'revenue': 12753.4, 'qoq_pct': 51.0}, {'quarter': '2026-04-01', 'revenue': 78912.68, 'qoq_pct': 518.8}] |
| WILSON | WILSON LIGHTING - OVERLAND PRK | 2 | 77,581.30 | 616.10 | [{'quarter': '2025-07-01', 'revenue': 24936.53, 'qoq_pct': -11.3}, {'quarter': '2025-10-01', 'revenue': 39301.18, 'qoq_pct': 57.6}, {'quarter': '2026-01-01', 'revenue': 10833.32, 'qoq_pct': -72.4}, {'quarter': '2026-04-01', 'revenue': 77581.3, 'qoq_pct': 616.1}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Currey & Company (cci, org_id=161)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6000-1118 | Entasis Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "BLU D'OR INTERIORS", 'revenue': None}, {'customer': 'KENNEDY GALLERIES', 'revenue': None}, {'customer': 'PLUM & CRIMSON FINE INT. DSGN.', 'revenue': None}, {'customer': 'SHRAWDER RESTORATIONS', 'revenue': None}] | — |
| 6700-0031 | Navigation Brown Cordless Table Lamp | — | — | — | — | 2026-9-16 | [{'customer': 'TIKALOVA', 'revenue': None}, {'customer': 'SWANK DESIGN', 'revenue': None}, {'customer': 'WESTON LYONS DESIGN', 'revenue': None}, {'customer': 'DISTINCTIVE IMAGE', 'revenue': None}, {'customer': 'UP COUNTRY HOME', 'revenue': None}, {'customer': 'UNIVERSAL LAMP MFG.', 'revenue': None}] | — |
| 3000-0346 | Virtuosity Bar Cabinet | — | — | — | — | 2026-7-18 | [{'customer': 'HEARTH AND SOUL', 'revenue': None}, {'customer': 'KUDZU AND COMPANY', 'revenue': None}, {'customer': "O'SHEA AND CO", 'revenue': None}, {'customer': 'THE CHANDLERY', 'revenue': None}, {'customer': 'ACCESSORIES, ETC - SAVANNAH', 'revenue': None}] | — |
| 6000-1089 | Betel Nut White Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': 'EAST END INTERIORS', 'revenue': None}] | — |
| 6000-1115 | Dossier Desk Lamp | — | — | — | — | 2026-9-16 | [{'customer': "REID'S FINE FURNISHINGS", 'revenue': None}, {'customer': 'ACCOMMODATION ACCOUNT', 'revenue': None}] | — |
| 9000-0824 | Denison Medium White Lantern | — | — | — | — | 2026-12-15 | [{'customer': 'CAITLIN KAH INTERIORS', 'revenue': None}, {'customer': 'BEATA BUHL INTERIORS', 'revenue': None}] | — |
| 9742 | Longhope Rectangular Chandelier | — | — | — | — | 2026-12-15 | [{'customer': 'LUXE HOME COMPANY', 'revenue': None}] | — |
| 1200-1167 | Sylva Medium White Vase | — | — | — | — | 2026-8-17 | [{'customer': 'ACCENTS FOR LIVING', 'revenue': None}, {'customer': 'HOME OUTFITTERS', 'revenue': None}, {'customer': 'LADCO', 'revenue': None}, {'customer': 'VERDALEE', 'revenue': None}] | — |
| 6000-0612 | Sonoran Table Lamp | — | — | — | — | — | [{'customer': 'MCGEE & CO', 'revenue': None}] | — |
| 6700-0044 | Volley Brass Cordless Table Lamp | — | — | — | — | 2026-7-18 | [{'customer': 'PAMELA GAYLIN RYDER INTERIORS', 'revenue': None}] | — |
| 5000-0320 | Grigsby Double-Light Wall Sconce | — | — | — | — | 2026-12-15 | [{'customer': 'HOWARD HOUSE INTERIORS', 'revenue': None}, {'customer': 'HAUTE HOUSE INTERIORS', 'revenue': None}] | — |
| 9000-1484 | Faraday Chandelier | — | — | — | — | 2026-12-15 | [{'customer': 'DANA MCKENNA DESIGNS', 'revenue': None}, {'customer': 'STEVEN SHELL LIVING', 'revenue': None}, {'customer': 'INTERIOR MOTIVES', 'revenue': None}, {'customer': 'MILIEU AND YOU', 'revenue': None}, {'customer': 'ACCENTS FOR LIVING', 'revenue': None}, {'customer': 'BELLISSIMO', 'revenue': None}, {'customer': 'CARTER & COMPANY', 'revenue': None}, {'customer': 'GADSDEN LIGHTING SHOWROOM', 'revenue': None}] | — |
| 6000-1095 | Uroko Table Lamp | — | — | — | — | 2026-7-18 | [{'customer': 'J F FABRICS', 'revenue': None}, {'customer': 'LOST CREEK RANCH', 'revenue': None}, {'customer': 'MATTER BROTHERS  FURNITURE', 'revenue': None}] | — |
| 6700-0040 | Wander Antique Silver Cordless Table Lamp | BUNNY WILLIAMS | — | — | — | 2026-7-18 | [{'customer': 'AB HOME', 'revenue': None}, {'customer': 'THE CHANDLERY', 'revenue': None}] | [{'item': '5000-0188', 'desc': 'Bette Gold Wall Sconce', 'available': 111}, {'item': '9000-0186', 'desc': 'Bette Gold Chandelier', 'available': 85}, {'item': '9999-0024', 'desc': 'Biddulph Gold Semi-Flush Mount', 'available': 71}, {'item': '5000-0067', 'desc': 'Westley Wall Sconce', 'available': 42}, {'item': '6700-0034', 'desc': 'Valise Cordless Table Lamp', 'available': 41}, {'item': '5900-0047', 'desc': 'Warwick Tall Wall Sconce', 'available': 33}, {'item': '9000-0187', 'desc': 'Belle Gold Chandelier', 'available': 30}, {'item': '9000-0991', 'desc': 'Augustus Small Chandelier', 'available': 29}, {'item': '9000-1296', 'desc': 'Bradshaw Lantern', 'available': 26}, {'item': '5000-0283', 'desc': 'Bradshaw Wall Sconce', 'available': 22}, {'item': '5000-0072', 'desc': 'Wallis Wall Sconce', 'available': 18}, {'item': '9000-1295', 'desc': 'Bradshaw Chandelier', 'available': 16}, {'item': '9000-1217', 'desc': 'Wycombe Lantern', 'available': 15}, {'item': '9000-0775', 'desc': 'Bailey Black Chandelier', 'available': 15}, {'item': '9000-0776', 'desc': 'Bebe Chandelier', 'available': 11}, {'item': '5000-0187', 'desc': 'Warwick Wall Sconce', 'available': 10}, {'item': '9000-0181', 'desc': 'Berkeley Chandelier', 'available': 5}] |
| 6700-0029 | Springe Ivory Cordless Table Lamp | — | — | — | — | 2026-9-16 | [{'customer': 'FIVE WEST INTERIORS', 'revenue': None}, {'customer': 'HOLIDAY BEACH DECOR', 'revenue': None}, {'customer': "O'SHEA AND CO", 'revenue': None}, {'customer': 'DECORATIVE CIRCLE', 'revenue': None}, {'customer': 'GREEN FRONT FURNITURE', 'revenue': None}, {'customer': 'UP COUNTRY HOME', 'revenue': None}] | — |
| 4000-0285 | Spalzato Demi-Lune Console Table | — | — | — | — | 2026-8-17 | [{'customer': 'ACP HOME INTERIORS', 'revenue': None}, {'customer': 'BRUMBAUGHS', 'revenue': None}] | — |
| 6700-0025 | Odyssey Large Cordless Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "BLU D'OR INTERIORS", 'revenue': None}, {'customer': 'KUDZU AND COMPANY', 'revenue': None}, {'customer': 'BEARDEN DESIGN', 'revenue': None}, {'customer': 'BARCLAY BUTERA INC', 'revenue': None}, {'customer': 'FEATHERS CUSTOM FURNITURE, INC', 'revenue': None}, {'customer': 'HYDE PARK INTERIORS', 'revenue': None}, {'customer': 'KNIGHT CARR & COMPANY', 'revenue': None}, {'customer': 'UP COUNTRY HOME', 'revenue': None}] | — |
| 6000-1120 | Blanche Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "BRAGG'S OF HUNTSVILLE", 'revenue': None}, {'customer': 'EAST END INTERIORS', 'revenue': None}, {'customer': 'MATTER BROTHERS  FURNITURE', 'revenue': None}] | — |
| 6000-1100 | Pinion Table Lamp | — | — | — | — | 2026-7-18 | [{'customer': 'DESIGNING WOMEN, INC.- HICKORY', 'revenue': None}] | — |
| 6000-1122 | Heaven Table Lamp | — | — | — | — | 2026-12-15 | [{'customer': "GMJ dba ROOSTER'S NEST", 'revenue': None}, {'customer': "BAER' S FURNITURE COMPANY", 'revenue': None}, {'customer': 'THE QUIET MOOSE', 'revenue': None}, {'customer': 'SEDLAK INTERIORS', 'revenue': None}] | — |
