# Section 2 Context Bundle — Hubbardton Forge (hfg)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=22112, portal_order_gmv=$42.2M |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | True | sales_data_count=44983 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | hubbardton_forge_hfg_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$42.2M > ecat_gmv=$16.8M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 137 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1873, Mixpanel total submit_order (Q-01): 3123 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.1%, ambiguous_rate=88.1%, showroom_event_share=3.5% |
| USER_GROUP_JOIN_RATE | 86% | 118 of 137 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Shannon Rose, Retha Boles |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=47 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2589 |
| INVENTORY_FRESH | False | inventories last_updated 300d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=57 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Hubbardton Forge
- **Shortname**: hfg
- **Org ID**: 165
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Hubbardton Forge (hfg, org_id=165)
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
| HAS_INVENTORY | False |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | False |
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

# Signal Rank — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Total signals fired**: 65 (P0: 47, P1: 18, P2: 0)
- **Org GMV**: $16.8M eCat LTM, $42.2M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep/Agency Capture Rate Gap — 16 reps at 0% eCat capture on $33.5M total business | P1 | §5 Team | 536.6 | $33,536,329 | 2.0 | 35,989,931,609 | POSITIVE |
| 2 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders | P1 | §2 Accounts | 12.8 | $12,843,857 | 2.0 | 329,929,325 | POSITIVE |
| 3 | SIG-OPP-01 | Next Best Product — 890540/890540-BINDER co-purchase pattern across 40 customers | P0 | §2/§3 | 4.0 | $25,823,289 | 2.0 | 206,586,310 | POSITIVE |
| 4 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 68% of eCat GMV | P1 | §4 Commerce | 1.7 | $5,984,145 | 2.0 | 20,334,605 | RISK |
| 5 | SIG-DECAY-03 | Rep Trajectory — Tony Minutelli orders -54.3% QoQ, $514,283 current 90d GMV | P1 | §5 Team | 2.2 | $2,057,132 | 2.0 | 8,936,181 | RISK |
| 6 | SIG-DECAY-01 | Reorder Decay — The Hotel Design Group 30.7x normal gap (307d vs 10d avg) | P0 | §2 Accounts | 30.7 | $73,912 | 3.0 | 6,807,295 | RISK |
| 7 | SIG-ANOMALY-03 | Competitive Displacement — HF Internal - Residential Accommodation total biz +396% but eCat -100% | P0 | §2 Accounts | 33.1 | $59,206 | 3.0 | 5,872,002 | RISK |
| 8 | SIG-DECAY-01 | Reorder Decay — Tode Rubenstein 4.1x normal gap (88d vs 21d avg) | P0 | §2 Accounts | 4.1 | $411,106 | 3.0 | 5,056,604 | RISK |
| 9 | SIG-DECAY-01 | Reorder Decay — ILC Studios 8.1x normal gap (313d vs 38d avg) | P0 | §2 Accounts | 8.1 | $159,187 | 3.0 | 3,868,244 | RISK |
| 10 | SIG-DECAY-01 | Reorder Decay — Beyer Brown 2.7x normal gap (123d vs 46d avg) | P0 | §2 Accounts | 2.7 | $470,819 | 3.0 | 3,813,634 | RISK |
| 11 | SIG-COMMERCE-01 | Capture Rate — eCat captures 39.8% of $42M total business; each +1pt = $422K | P0 | §4 Commerce | 3.0 | $422,000 | 3.0 | 3,810,000 | POSITIVE |
| 12 | SIG-MOM-01 | Account Acceleration — Decorators Unlimited Inc 2 consecutive QoQ acceleration quarters, $89,675 peak quarter (+350% QoQ) | P0 | §2 Accounts | 11.7 | $89,675 | 3.0 | 3,142,205 | POSITIVE |
| 13 | SIG-DECAY-03 | Rep Trajectory — Karen Clegg orders -32.7% QoQ, $280,300 current 90d GMV | P1 | §5 Team | 1.3 | $1,121,200 | 2.0 | 2,933,059 | RISK |
| 14 | SIG-DECAY-04 | Spending Contraction — Sun Lighting Tempe LLC. -78.4% YoY ($301,307→$65,086), $236,221 gap | P0 | §2 Accounts | 3.9 | $236,221 | 3.0 | 2,777,959 | RISK |
| 15 | SIG-MOM-01 | Account Acceleration — Fogg Lighting 2 consecutive QoQ acceleration quarters, $83,700 peak quarter (+237% QoQ) | P0 | §2 Accounts | 7.9 | $83,700 | 3.0 | 1,982,844 | POSITIVE |
| 16 | SIG-DECAY-03 | Rep Trajectory — Sherri Juhl orders -30.2% QoQ, $190,903 current 90d GMV | P1 | §5 Team | 1.2 | $763,612 | 2.0 | 1,844,887 | RISK |
| 17 | SIG-DECAY-01 | Reorder Decay — Value Lighting Inc. 3.5x normal gap (47d vs 13d avg) | P0 | §2 Accounts | 3.5 | $168,072 | 3.0 | 1,764,756 | RISK |
| 18 | SIG-MOM-01 | Account Acceleration — Clive Daniel Home 3 consecutive QoQ acceleration quarters, $108,698 peak quarter (+150% QoQ) | P0 | §2 Accounts | 5.0 | $108,698 | 3.0 | 1,627,215 | POSITIVE |
| 19 | SIG-DECAY-01 | Reorder Decay — Burk Design Group 11.5x normal gap (250d vs 21d avg) | P0 | §2 Accounts | 11.5 | $45,438 | 3.0 | 1,567,611 | RISK |
| 20 | SIG-DECAY-01 | Reorder Decay — Main Electric Supply Co. 3.0x normal gap (46d vs 15d avg) | P0 | §2 Accounts | 3.0 | $155,437 | 3.0 | 1,398,933 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 46 | 1 | 0 | 47 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 7 | 0 | 7 | |
| §6 Platform Context | 0 | 9 | 0 | 9 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep/Agency Capture Rate Gap — 16 reps at 0% eCat capture on $33.5M total business
2. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders
3. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 890540/890540-BINDER co-purchase pattern across 40 customers
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 39.8% of $42M total business; each +1pt = $422K
5. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 68% of eCat GMV
6. **[RISK]** SIG-DECAY-03: Rep Trajectory — Tony Minutelli orders -54.3% QoQ, $514,283 current 90d GMV
7. **[RISK]** SIG-DECAY-01: Reorder Decay — The Hotel Design Group 30.7x normal gap (307d vs 10d avg)

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | Graybar Electric | 2 | DECAY-01, DECAY-04 | $141,462 |
| 2 | Lighting Design Center | 2 | DECAY-04, MOM-01 | $96,977 |
| 3 | Fan & Lighting World | 2 | DECAY-04, MOM-01 | $55,441 |
| 4 | The Hotel Design Group | 1 | DECAY-01 | $73,912 |
| 5 | Tode Rubenstein | 1 | DECAY-01 | $411,106 |
| 6 | ILC Studios | 1 | DECAY-01 | $159,187 |
| 7 | Beyer Brown | 1 | DECAY-01 | $470,819 |
| 8 | Value Lighting Inc. | 1 | DECAY-01 | $168,072 |
| 9 | Burk Design Group | 1 | DECAY-01 | $45,438 |
| 10 | Main Electric Supply Co. | 1 | DECAY-01 | $155,437 |

### Q-12_results.md

# Q-12 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 9,026 | 1,359 | 496 | 327 | 191 |

### Q-14_results.md

# Q-14 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 13794 | Apex Lighting Solutions | 133 | $750,200 | 2025-06-17 17:24:31 | 2026-06-16 19:17:42 | 2.80 |
| 10972 | Power Design Resources, LLC | 62 | $759,245 | 2025-06-26 15:51:44 | 2026-06-05 14:40:39 | 5.60 |
| 16998 | Larrick Design Resources | 49 | $603,881 | 2025-07-08 18:16:31 | 2026-06-11 15:28:02 | 7 |
| 35347 | Integris Solutions | 39 | $331,587 | 2025-06-18 20:42:03 | 2026-06-09 16:45:56 | 9.40 |
| 10336 | CED | 36 | $125,334 | 2025-07-08 17:53:22 | 2026-06-16 18:11:45 | 9.80 |
| 13247 | Freestyle Interiors | 31 | $154,052 | 2025-07-01 20:47:31 | 2026-06-16 15:49:28 | 11.70 |
| 2465 | The Parker Company LLC | 28 | $3.4M | 2025-08-29 15:12:02 | 2026-06-15 20:19:29 | 10.70 |
| 35095 | Lonestar Electric Supply | 28 | $116,104 | 2025-06-30 16:22:59 | 2026-05-28 15:49:43 | 12.30 |
| 10468 | Main Electric Supply Co. | 27 | $155,437 | 2025-07-10 20:46:37 | 2026-05-01 14:25:58 | 11.30 |
| 11598 | Value Lighting Inc. | 25 | $168,072 | 2025-07-01 15:48:17 | 2026-04-30 16:23:19 | 12.60 |
| 13657 | Karen Clegg and Associates | 25 | $351,420 | 2025-08-13 22:02:30 | 2026-06-10 18:30:47 | 12.50 |
| 10110 | Rexel, Inc | 24 | $192,984 | 2025-07-25 13:40:43 | 2026-06-16 18:16:45 | 14.20 |
| 13841 | Legacy Lighting LLC | 23 | $202,594 | 2025-06-18 15:07:33 | 2026-06-04 15:05:30 | 16 |
| 39954 | Light and Living | 19 | $50,882 | 2025-06-24 10:48:31 | 2026-06-09 10:53:07 | 19.40 |
| 1326 | Graybar Electric | 19 | $141,462 | 2025-07-09 20:47:46 | 2026-04-24 16:33:23 | 16 |
| 12957 | Tode Rubenstein | 18 | $411,106 | 2025-07-22 17:08:11 | 2026-03-20 18:50:27 | 14.20 |
| 13205 | Beyer Brown | 15 | $470,819 | 2025-09-11 15:51:02 | 2026-02-13 22:07:07 | 11.10 |
| 38962 | Ion Lighting | 15 | $163,456 | 2025-10-23 15:41:03 | 2026-05-28 13:25:42 | 15.50 |
| 10367 | Walters Wholesale Electric Co. | 14 | $78,527 | 2025-07-03 14:54:40 | 2026-03-27 00:29:16 | 20.50 |
| 11839 | E Sam Jones Distributor Inc | 13 | $202,452 | 2025-07-21 16:15:55 | 2026-05-20 14:51:48 | 25.20 |

### Q-14b_results.md

# Q-14b Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 2055 | Lighting Design Center | 93 | 4.70 | 8.40 | 1.79 | $150,453 |
| 1255 | Berkeley Lighting Company | 60 | 7.70 | 11.70 | 1.52 | $112,716 |
| 13062 | North Coast Lighting Co | 103 | 4.30 | 8.50 | 1.98 | $106,204 |
| 26456 | Bridget Bohacz + Associates, Inc. | 6 | 26.70 | 92.70 | 3.47 | $94,380 |
| 11942 | Lighting EFX | 16 | 25.70 | 38.60 | 1.50 | $84,848 |
| 1787 | Wasatch Lighting | 45 | 10.60 | 16.10 | 1.52 | $83,806 |
| 1155 | Rockingham Electrical Supply | 81 | 5.70 | 9 | 1.58 | $76,379 |
| 1326 | Graybar Electric | 32 | 11.10 | 65.70 | 5.92 | $75,841 |
| 13247 | Freestyle Interiors | 41 | 10.90 | 19.70 | 1.81 | $71,462 |
| 32140 | Lesly Maxwell Interiors | 20 | 15.80 | 59.30 | 3.75 | $69,573 |
| 1886 | M&M Lighting | 36 | 12 | 22 | 1.83 | $65,792 |
| 10170 | Sun Lighting Tempe LLC. | 63 | 6.40 | 14.30 | 2.23 | $65,086 |
| 17236 | HF Internal - Residential Accommodation | 15 | 23.50 | 48.50 | 2.06 | $59,548 |
| 2044 | Lofings Lighting, Inc. | 51 | 7.90 | 14.40 | 1.82 | $58,854 |
| 2048 | Littman Bros. Lighting | 66 | 6.70 | 12.20 | 1.82 | $57,981 |

### Q-17_results.md

# Q-17 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 13205 | Beyer Brown | FL | 2026-02-13 22:07:07 | 15 | $470,819 |
| 43565 | ILC Studios | CO | 2025-08-07 17:02:10 | 5 | $159,187 |
| 39015 | PVG Interiors | CA | 2026-03-12 23:17:55 | 3 | $121,134 |
| 43070 | CHS Design Studio LLC | FL | 2026-01-26 14:25:12 | 5 | $118,754 |
| 37312 | LOGIQ Supply LLC | CO | 2026-02-27 23:32:57 | 6 | $104,962 |
| 39614 | Wesco Distribution | GA | 2026-02-10 16:36:24 | 1 | $93,852 |
| 22389 | The Hotel Design Group | FL | 2025-08-13 18:26:39 | 5 | $73,912 |
| 38168 | Thyme and Place Design | NJ | 2025-11-13 22:12:22 | 2 | $61,584 |
| 11029 | One Source Distributors | CA | 2025-12-03 21:26:00 | 9 | $61,084 |
| 40567 | Amy Storm & Co. | IL | 2025-07-02 18:42:44 | 2 | $53,330 |
| 27220 | Burk Design Group | CO | 2025-10-09 20:38:03 | 11 | $45,438 |
| 44172 | American First Builders | AZ | 2026-02-05 21:03:44 | 3 | $39,053 |
| 41725 | El Gee Lighting | FL | 2026-03-11 20:01:32 | 6 | $33,121 |
| 12805 | Innvision Hospitality, Inc | GA | 2025-10-22 19:16:43 | 3 | $32,920 |
| 29064 | EDGES | CA | 2026-03-05 19:02:12 | 9 | $29,512 |
| 29910 | SAS Interiors | CA | 2025-06-19 19:54:06 | 2 | $29,400 |
| 45304 | Impact Energy | CO | 2025-11-18 21:22:33 | 2 | $29,046 |
| 35769 | Elizabeth Robb Interiors | MT | 2026-01-21 21:55:07 | 1 | $28,988 |
| 45945 | Kelly Jahn Interior Architecture + Design | NY | 2025-12-05 21:00:06 | 2 | $24,148 |
| 37814 | Amber Hodgins Design | VT | 2026-03-03 21:44:09 | 2 | $23,612 |
| 43156 | City Electric Supply | TX | 2026-01-15 17:16:03 | 3 | $23,230 |
| 10717 | Elliott Electric Supply | TX | 2026-02-05 22:06:14 | 3 | $23,174 |
| 34381 | Florida Coach | FL | 2026-02-20 21:09:07 | 9 | $22,945 |
| 1572 | Kendall Lighting Center | MI | 2026-01-15 20:40:25 | 2 | $22,658 |
| 43125 | Sun Lighting Tucson | AZ | 2026-01-14 19:24:33 | 2 | $22,544 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 13205 | Beyer Brown | FL | $470,819 | 2026-02-13 22:07:07 | 123 |
| 43565 | ILC Studios | CO | $159,187 | 2025-08-07 17:02:10 | 313 |
| 39015 | PVG Interiors | CA | $121,134 | 2026-03-12 23:17:55 | 96 |
| 43070 | CHS Design Studio LLC | FL | $118,754 | 2026-01-26 14:25:12 | 141 |
| 37312 | LOGIQ Supply LLC | CO | $104,962 | 2026-02-27 23:32:57 | 109 |
| 39614 | Wesco Distribution | GA | $93,852 | 2026-02-10 16:36:24 | 126 |
| 22389 | The Hotel Design Group | FL | $73,912 | 2025-08-13 18:26:39 | 307 |
| 38168 | Thyme and Place Design | NJ | $61,584 | 2025-11-13 22:12:22 | 215 |
| 11029 | One Source Distributors | CA | $61,084 | 2025-12-03 21:26:00 | 195 |
| 40567 | Amy Storm & Co. | IL | $53,330 | 2025-07-02 18:42:44 | 349 |
| 27220 | Burk Design Group | CO | $45,438 | 2025-10-09 20:38:03 | 250 |
| 44172 | American First Builders | AZ | $39,053 | 2026-02-05 21:03:44 | 131 |
| 41725 | El Gee Lighting | FL | $33,121 | 2026-03-11 20:01:32 | 97 |
| 12805 | Innvision Hospitality, Inc | GA | $32,920 | 2025-10-22 19:16:43 | 237 |
| 29064 | EDGES | CA | $29,512 | 2026-03-05 19:02:12 | 103 |
| 29910 | SAS Interiors | CA | $29,400 | 2025-06-19 19:54:06 | 362 |
| 45304 | Impact Energy | CO | $29,046 | 2025-11-18 21:22:33 | 210 |
| 35769 | Elizabeth Robb Interiors | MT | $28,988 | 2026-01-21 21:55:07 | 146 |
| 13907 | Schreier Interiors | MN | $24,819 | 2026-03-18 11:35:33 | 90 |
| 45945 | Kelly Jahn Interior Architecture + Design | NY | $24,148 | 2025-12-05 21:00:06 | 193 |

### Q-40_results.md

# Q-40 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| FL | 47 | 271 | $6.2M |
| CA | 65 | 226 | $1.8M |
| CO | 46 | 215 | $1.5M |
| GA | 23 | 129 | $1.2M |
| TX | 22 | 157 | $994,897 |
| CT | 14 | 157 | $853,151 |
| AZ | 37 | 77 | $308,667 |
| MA | 37 | 79 | $272,758 |
| TN | 9 | 24 | $149,648 |
| MO | 1 | 19 | $141,462 |
| NY | 12 | 22 | $130,192 |
| IL | 11 | 14 | $129,096 |
| MT | 16 | 32 | $115,457 |
| VT | 17 | 27 | $111,929 |
| WA | 20 | 30 | $109,388 |
| KY | 3 | 5 | $88,255 |
| NJ | 7 | 8 | $86,216 |
| ME | 17 | 35 | $84,879 |
| NV | 10 | 15 | $65,747 |
| OR | 9 | 17 | $60,561 |

### Q-41_results.md

# Q-41 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 16
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 7 |
| 2025-04-01 | Rep-Acquired (iPad) | 30 |
| 2025-05-01 | Rep-Acquired (iPad) | 16 |
| 2025-06-01 | Rep-Acquired (iPad) | 16 |
| 2025-07-01 | Rep-Acquired (iPad) | 16 |
| 2025-08-01 | Rep-Acquired (iPad) | 10 |
| 2025-09-01 | Rep-Acquired (iPad) | 16 |
| 2025-10-01 | Rep-Acquired (iPad) | 20 |
| 2025-11-01 | Rep-Acquired (iPad) | 15 |
| 2025-12-01 | Rep-Acquired (iPad) | 13 |
| 2026-01-01 | Rep-Acquired (iPad) | 24 |
| 2026-02-01 | Rep-Acquired (iPad) | 18 |
| 2026-03-01 | Rep-Acquired (iPad) | 18 |
| 2026-04-01 | Rep-Acquired (iPad) | 21 |
| 2026-05-01 | Rep-Acquired (iPad) | 21 |
| 2026-06-01 | Rep-Acquired (iPad) | 5 |

### Q-41_rep_results.md

# Q-41-rep Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 37
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Dunn Lighting | 44 |
| Julie Gannon | 34 |
| Amy Matteson | 23 |
| Lynn  Ross | 17 |
| Brad Krieger | 17 |
| Randy Gould | 12 |
| Tanner Gould | 11 |
| Karen Clegg | 11 |
| Wayne Guthrie | 10 |
| Lisa Belesky | 9 |
| Tony Minutelli | 8 |
| Jenifer McCarty | 8 |
| Kevin Gannon | 7 |
| Tami Stauffacher | 7 |
| Sherri Juhl | 5 |
| Vincent Ingato | 5 |
| Grant Duguid | 5 |
| Lynn Ross | 3 |
| Martha Graham & Associates Office | 3 |
| Jeff Stander | 3 |
| Jeff Izower | 3 |
| Jim Hickey | 2 |
| Trip McKenzie | 2 |
| Stacey  Micheal | 2 |
| Brian Roche | 2 |
| Doug Glassman | 2 |
| Jessica - Ricci sales Mason | 1 |
| John Fangman | 1 |
| Jessica Mason | 1 |
| Allison Stauffacher | 1 |
| Larry Williams | 1 |
| Mickey McCarthy | 1 |
| Penny Gould | 1 |
| Geno Schwartz | 1 |
| Retha Boles | 1 |
| Shannon Rose | 1 |
| Chris Zaya | 1 |

### Q-52_results.md

# Q-52 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 13869 | Illuminating Expressions | NY | 12 | $2.7M | 0 | $0 | 0 |
| 11499 | Lumens, Inc. | CA | 2,038 | $2.4M | 0 | $0 | 0 |
| 1358 | Ferguson Enterprises | VA | 630 | $1.2M | 0 | $0 | 0 |
| 11878 | Build.com Inc | CA | 615 | $783,077 | 0 | $0 | 0 |
| 12180 | Wayfair, LLC | MA | 893 | $775,909 | 0 | $0 | 0 |
| 10505 | Handmade In Vermont.com | VT | 756 | $695,764 | 0 | $0 | 0 |
| 35639 | Shop Hubbardton Forge | VT | 498 | $656,180 | 0 | $0 | 0 |
| 1489 | AFJ Distribution Inc. | QC | 499 | $645,582 | 0 | $0 | 0 |
| 34918 | Lighting New York | PA | 657 | $632,467 | 0 | $0 | 0 |
| 10285 | Lightology LLC | IL | 433 | $619,930 | 0 | $0 | 0 |
| 2258 | Lamps Plus Centennial | CA | 669 | $556,067 | 0 | $0 | 0 |
| 11199 | Capitol Lighting | FL | 276 | $477,028 | 0 | $0 | 0 |
| 12445 | CAI Designs | IL | 178 | $405,033 | 0 | $0 | 0 |
| 42246 | 1800Lighting.com | NJ | 362 | $355,754 | 0 | $0 | 0 |
| 34218 | Clive Daniel Home | FL | 62 | $244,876 | 0 | $0 | 0 |
| 2332 | Hinkley's New State Lighting | AZ | 60 | $239,597 | 1 | $9,115 | 3.80 |
| 2241 | Nova Lighting | UT | 38 | $218,903 | 0 | $0 | 0 |
| 12056 | Urban Lights | CO | 104 | $213,161 | 0 | $0 | 0 |
| 11936 | Lighting First | FL | 87 | $209,528 | 0 | $0 | 0 |
| 1531 | Crescent Lighting Supply | WA | 115 | $206,165 | 3 | $7,634 | 3.70 |
| 2213 | Dolan Northwest, LLC | OR | 180 | $197,496 | 0 | $0 | 0 |
| 10698 | Ray Lighting Center | MI | 170 | $194,156 | 0 | $0 | 0 |
| 1547 | Southern Lights | MN | 77 | $173,064 | 0 | $0 | 0 |
| 1178 | Shanor Electric Supply Inc. | NY | 7 | $170,553 | 0 | $0 | 0 |
| 1857 | Wilson Fans & Lighting | FL | 51 | $169,421 | 0 | $0 | 0 |
| 11365 | Fogg Lighting | ME | 84 | $164,520 | 0 | $0 | 0 |
| 1716 | Valley Light Gallery | AZ | 46 | $163,808 | 0 | $0 | 0 |
| 2459 | QED, Inc | CO | 68 | $163,495 | 0 | $0 | 0 |
| 1905 | Gross Lighting + Home | OH | 72 | $153,002 | 0 | $0 | 0 |
| 2055 | Lighting Design Center | NV | 53 | $150,453 | 2 | $13,647 | 9.10 |

### Q-53_results.md

# Q-53 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 13869 | Illuminating Expressions | NY | 12 | $2.7M |
| 11499 | Lumens, Inc. | CA | 2,038 | $2.4M |
| 11878 | Build.com Inc | CA | 615 | $783,077 |
| 12180 | Wayfair, LLC | MA | 893 | $775,909 |
| 10505 | Handmade In Vermont.com | VT | 756 | $695,764 |
| 35639 | Shop Hubbardton Forge | VT | 498 | $656,180 |
| 1489 | AFJ Distribution Inc. | QC | 499 | $645,582 |
| 34918 | Lighting New York | PA | 657 | $632,467 |
| 10285 | Lightology LLC | IL | 433 | $619,930 |
| 2258 | Lamps Plus Centennial | CA | 669 | $556,067 |
| 12445 | CAI Designs | IL | 178 | $405,033 |
| 42246 | 1800Lighting.com | NJ | 362 | $355,754 |
| 34218 | Clive Daniel Home | FL | 62 | $244,876 |
| 2241 | Nova Lighting | UT | 38 | $218,903 |
| 12056 | Urban Lights | CO | 104 | $213,161 |
| 11936 | Lighting First | FL | 87 | $209,528 |
| 2213 | Dolan Northwest, LLC | OR | 180 | $197,496 |
| 10698 | Ray Lighting Center | MI | 170 | $194,156 |
| 1178 | Shanor Electric Supply Inc. | NY | 7 | $170,553 |
| 1857 | Wilson Fans & Lighting | FL | 51 | $169,421 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA | 270 | 5,056 | $7.0M | 65 | 226 | $1.8M | 26.50 |
| FL | 260 | 1,826 | $4.6M | 47 | 271 | $6.2M | 135.20 |
| NY | 179 | 837 | $4.5M | 12 | 22 | $130,192 | 2.90 |
| VT | 52 | 1,818 | $2.0M | 17 | 27 | $111,929 | 5.60 |
| CO | 118 | 819 | $1.9M | 46 | 215 | $1.5M | 75.80 |
| MA | 99 | 1,633 | $1.9M | 37 | 79 | $272,758 | 14.50 |
| IL | 58 | 894 | $1.5M | 11 | 14 | $129,096 | 8.40 |
| PA | 74 | 1,050 | $1.5M | 4 | 14 | $41,477 | 2.70 |
| VA | 42 | 804 | $1.5M | 2 | 2 | $4,231 | 0.30 |
| AZ | 92 | 463 | $1.3M | 37 | 77 | $308,667 | 23.20 |
| TX | 140 | 452 | $1.1M | 22 | 157 | $994,897 | 91.50 |
| NJ | 90 | 752 | $1.1M | 7 | 8 | $86,216 | 8 |
| UT | 57 | 210 | $916,673 | 4 | 6 | $16,214 | 1.80 |
| WA | 69 | 413 | $817,716 | 20 | 30 | $109,388 | 13.40 |
| NC | 94 | 419 | $800,418 | 3 | 6 | $19,318 | 2.40 |
| QC | 2 | 500 | $770,138 | 0 | 0 | $0 | 0 |
| MI | 40 | 400 | $653,924 | 3 | 4 | $45,030 | 6.90 |
| GA | 66 | 262 | $589,884 | 23 | 129 | $1.2M | 209.80 |
| OR | 39 | 357 | $589,268 | 9 | 17 | $60,561 | 10.30 |
| CT | 64 | 286 | $569,964 | 14 | 157 | $853,151 | 149.70 |

### Q-57_results.md

# Q-57 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Unknown | $10.4M | $9.4M | -9 | 1,242 | 1,207 | 35 | 5,417 |

### Q-68_results.md

# Q-68 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| AFJ Distribution Inc. | Unknown | $667,461 | $1.0M | $351,117 | 65.50 | 13 |
| Handmade In Vermont.com | Unknown | $715,140 | $1.1M | $350,718 | 67.10 | 13 |
| Sun Lighting Tempe LLC. | Unknown | $65,086 | $313,535 | $248,449 | 20.80 | 13 |
| Technology By Design | Unknown | $13,406 | $161,138 | $147,731 | 8.30 | 4 |
| Graybar Electric | Unknown | $81,797 | $218,058 | $136,260 | 37.50 | 6 |
| The Lighting Showroom, Inc | Unknown | $72,926 | $207,963 | $135,037 | 35.10 | 12 |
| Lighting Design Center | Unknown | $151,810 | $279,178 | $127,368 | 54.40 | 12 |
| Dolan Northwest, LLC | Unknown | $208,826 | $331,884 | $123,058 | 62.90 | 13 |
| Anixter Power Solutions LLC | Unknown | $11,576 | $131,607 | $120,031 | 8.80 | 6 |
| Sonepar/NE Electrical Dist. | Unknown | $11,497 | $123,514 | $112,016 | 9.30 | 5 |
| Dianne Davant & Associates | Unknown | $28,387 | $134,846 | $106,458 | 21.10 | 7 |
| American First Builders | Unknown | $44,099 | $141,990 | $97,891 | 31.10 | 5 |
| Lonestar Electric Supply | Unknown | $27,765 | $120,049 | $92,284 | 23.10 | 7 |
| Shepherd Electric Company | Unknown | $17,781 | $109,307 | $91,526 | 16.30 | 3 |
| HF Internal - Commercial Accomodation | Unknown | $54,636 | $144,850 | $90,214 | 37.70 | 13 |
| Urban Lights | Unknown | $231,306 | $320,127 | $88,821 | 72.30 | 13 |
| N & S Decor Fixture Co, Inc. | Unknown | $66,246 | $153,104 | $86,858 | 43.30 | 13 |
| Lumenarea.com | Unknown | $51,983 | $138,247 | $86,263 | 37.60 | 13 |
| E Sam Jones Distributor Inc | Unknown | $6,271 | $87,324 | $81,052 | 7.20 | 4 |
| Olivia's Home Furnishings | Unknown | $88,841 | $168,868 | $80,027 | 52.60 | 11 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| customer_num | customer_name | state | ltm_orders | ltm_gmv | last_order | days_since_last | avg_days_between | decay_ratio |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 22389 | The Hotel Design Group | FL | 5 | $73,912 | 2025-08-13 18:26:39 | 307 | 10 | 30.70 |
| 12957 | Tode Rubenstein | CA | 18 | $411,106 | 2026-03-20 18:50:27 | 88 | 21.30 | 4.10 |
| 43565 | ILC Studios | CO | 5 | $159,187 | 2025-08-07 17:02:10 | 313 | 38.50 | 8.10 |
| 13205 | Beyer Brown | FL | 15 | $470,819 | 2026-02-13 22:07:07 | 123 | 46.10 | 2.70 |
| 11598 | Value Lighting Inc. | GA | 25 | $168,072 | 2026-04-30 16:23:19 | 47 | 13.60 | 3.50 |
| 27220 | Burk Design Group | CO | 11 | $45,438 | 2025-10-09 20:38:03 | 250 | 21.70 | 11.50 |
| 10468 | Main Electric Supply Co. | CA | 27 | $155,437 | 2026-05-01 14:25:58 | 46 | 15.10 | 3 |
| 1326 | Graybar Electric | MO | 19 | $141,462 | 2026-04-24 16:33:23 | 53 | 17.60 | 3 |
| 43070 | CHS Design Studio LLC | FL | 5 | $118,754 | 2026-01-26 14:25:12 | 141 | 50 | 2.80 |
| 29064 | EDGES | CA | 9 | $29,512 | 2026-03-05 19:02:12 | 103 | 9.60 | 10.70 |
| 11029 | One Source Distributors | CA | 9 | $61,084 | 2025-12-03 21:26:00 | 195 | 38 | 5.10 |
| 10367 | Walters Wholesale Electric Co. | CA | 14 | $78,527 | 2026-03-27 00:29:16 | 82 | 21.50 | 3.80 |
| 34793 | Moxie Design Studio | CA | 12 | $69,648 | 2026-03-20 18:34:28 | 88 | 28.90 | 3 |

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 4
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11499 | Lumens, Inc. | 137660-SKT-MULT-05-SE4298 | 137660-SKT-MULT-05-SE4298     |Pendant: Brindille, Rect | 5 | 8 | 284 | 35.50 | 8,323 | DECAY_DETECTED |
| 11499 | Lumens, Inc. | 306405-SKT-14-ZM0333 | 306405-SKT-14-ZM0333           Outdoor: Axis, Lrg | 5 | 51 | 212 | 4.20 | 28,474 | DECAY_DETECTED |
| 11499 | Lumens, Inc. | 306403-SKT-80-ZM0332 | 306403-SKT-80-ZM0332           Outdoor: Axis, Med | 15 | 28.10 | 98 | 3.50 | 8,472 | DECAY_DETECTED |
| 11499 | Lumens, Inc. | 302713-SKT-80 | 302713-SKT-80                  Outdoor: Henry, Dark Sky, Medium | 6 | 40.70 | 128 | 3.10 | 8,504 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 50
- **Run date**: 2026-06-17


| customer_code | customer_name | customer_ltm | anchor_item | anchor_desc | suggested_item | suggested_desc | co_purchase_customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1489 | AFJ Distribution Inc. | 645,582.22 | 890540 | — | 890540-BINDER | — | 40 |
| 2213 | Dolan Northwest, LLC | 197,496.10 | 890540 | — | 890540-BINDER | — | 40 |
| 2459 | QED, Inc | 163,495.36 | 890540 | — | 890540-BINDER | — | 40 |
| 13689 | F.W. Webb Company | 134,456.19 | 890540 | — | 890540-BINDER | — | 40 |
| 12358 | Naples Lamp Shop | 131,414 | 890540 | — | 890540-BINDER | — | 40 |
| 1294 | Coast Lighting | 127,648.12 | 890540 | — | 890540-BINDER | — | 40 |
| 13869 | Illuminating Expressions | 2,692,148.54 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 11878 | Build.com Inc | 783,076.59 | 902329-CHIP-RING | — | 9MOD-A | — | 31 |
| 11878 | Build.com Inc | 783,076.59 | 50511 | — | 9MOD-A | — | 31 |
| 11878 | Build.com Inc | 783,076.59 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 12180 | Wayfair, LLC | 775,909.17 | 890540 | — | 902329-CHIP-RING | — | 31 |
| 10505 | Handmade In Vermont.com | 695,764.24 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 35639 | Shop Hubbardton Forge | 656,179.69 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 35639 | Shop Hubbardton Forge | 656,179.69 | 902329-CHIP-RING | — | 9MOD-A | — | 31 |
| 35639 | Shop Hubbardton Forge | 656,179.69 | 50511 | — | 9MOD-A | — | 31 |
| 34918 | Lighting New York | 632,467.05 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 10285 | Lightology LLC | 619,930.42 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 2258 | Lamps Plus Centennial | 556,066.60 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 11199 | Capitol Lighting | 477,028.45 | 9MOD-A | — | 50511 | — | 31 |
| 11199 | Capitol Lighting | 477,028.45 | 9MOD-A | — | 902329-CHIP-RING | — | 31 |
| 12445 | CAI Designs | 405,033.15 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 42246 | 1800Lighting.com | 355,754.20 | 50511 | — | 9MOD-A | — | 31 |
| 42246 | 1800Lighting.com | 355,754.20 | 902329-CHIP-RING | — | 9MOD-A | — | 31 |
| 42246 | 1800Lighting.com | 355,754.20 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 34218 | Clive Daniel Home | 244,876.50 | 902329-CHIP-RING | — | 890540 | — | 31 |
| 34218 | Clive Daniel Home | 244,876.50 | 902329-CHIP-RING | — | 9MOD-A | — | 31 |
| 34218 | Clive Daniel Home | 244,876.50 | 50511 | — | 9MOD-A | — | 31 |
| 2332 | Hinkley's New State Lighting | 239,596.62 | 9MOD-A | — | 902329-CHIP-RING | — | 31 |
| 2332 | Hinkley's New State Lighting | 239,596.62 | 9MOD-A | — | 50511 | — | 31 |
| 2241 | Nova Lighting | 218,903.24 | 9MOD-A | — | 50511 | — | 31 |

*(Truncated: showing top 30 of 50 rows. Full data in cache file.)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10170 | Sun Lighting Tempe LLC. | AZ | 65,086.20 | 301,307.20 | -78.40 | 9,219 | 8,337.50 | 10.60 | CONTRACTING |
| 10505 | Handmade In Vermont.com | VT | 695,764.24 | 924,230.24 | -24.70 | 0 | 0 | — | CONTRACTING |
| 1489 | AFJ Distribution Inc. | QC | 645,582.22 | 808,266.02 | -20.10 | 0 | 0 | — | CONTRACTING |
| 2213 | Dolan Northwest, LLC | OR | 197,496.10 | 318,501.26 | -38 | 0 | 0 | — | CONTRACTING |
| 1326 | Graybar Electric | MO | 75,841.38 | 186,714.50 | -59.40 | 141,461.60 | 165,940.70 | -14.80 | CONTRACTING |
| 2055 | Lighting Design Center | NV | 150,452.60 | 247,429.90 | -39.20 | 13,647 | 12,420 | 9.90 | CONTRACTING |
| 11894 | N & S Decor Fixture Co, Inc. | NY | 64,422.86 | 153,809 | -58.10 | 0 | 0 | — | CONTRACTING |
| 12056 | Urban Lights | CO | 213,161.02 | 295,341.08 | -27.80 | 0 | 0 | — | CONTRACTING |
| 2433 | The Lighting Showroom, Inc | CA | 65,641.30 | 139,928.72 | -53.10 | 0 | 10,131 | -100 | CONTRACTING |
| 1992 | Lighting Showroom LLC | NH | 81,125.33 | 145,255.60 | -44.10 | 0 | 1,400 | -100 | CONTRACTING |
| 13337 | Naples Lighting & Fan Depot | FL | 74,170 | 137,368 | -46 | 0 | 6,684 | -100 | CONTRACTING |
| 2103 | Lumenarea.com | CO | 50,816.42 | 109,029.62 | -53.40 | 0 | 0 | — | CONTRACTING |
| 12437 | Fan & Lighting World | FL | 138,187 | 193,627.58 | -28.60 | 0 | 0 | — | CONTRACTING |
| 35095 | Lonestar Electric Supply | TX | 27,765.40 | 83,167.60 | -66.60 | 116,103.80 | 317,301.60 | -63.40 | CONTRACTING |
| 1933 | Herald Wholesale | MI | 45,983.84 | 99,676 | -53.90 | 16,150 | 0 | — | CONTRACTING |
| 2459 | QED, Inc | CO | 163,495.36 | 112,207.96 | 45.70 | 0 | 6,164 | -100 | COMPETITIVE_DISPLACEMENT |
| 12036 | Fusion Light and Design | CO | 100,435 | 151,364.40 | -33.60 | 0 | 25,418 | -100 | CONTRACTING |
| 1572 | Kendall Lighting Center | MI | 76,489.86 | 124,332.50 | -38.50 | 22,657.50 | 46,866 | -51.70 | CONTRACTING |
| 10755 | LBU Lighting Boca Raton | FL | 54,496.05 | 102,064.20 | -46.60 | 0 | 0 | — | CONTRACTING |
| 17236 | HF Internal - Residential Accommodation | VT | 59,547.67 | 12,007.05 | 395.90 | 0 | 11,939 | -100 | COMPETITIVE_DISPLACEMENT |
| 10368 | Academy/Foundry LA | NY | 31,024.30 | 78,432 | -60.40 | 0 | 16,644.95 | -100 | CONTRACTING |
| 2367 | Marriott International Design | MD | 29,783 | 76,544.08 | -61.10 | 0 | 0 | — | CONTRACTING |
| 10317 | Beautiful Things Lighting | FL | 115,414.62 | 162,035.38 | -28.80 | 0 | 0 | — | CONTRACTING |
| 2048 | Littman Bros. Lighting | IL | 57,981.24 | 103,179 | -43.80 | 0 | 6,536.50 | -100 | CONTRACTING |
| 2057 | Lighting Inc | TX | 62,808.86 | 107,788.22 | -41.70 | 0 | 0 | — | CONTRACTING |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 13869 | Illuminating Expressions | 2 | 2,676,945.30 | 235,546.60 | [{'quarter': '2025-07-01', 'revenue': 1136.0, 'qoq_pct': -83.2}, {'quarter': '2025-10-01', 'revenue': 2676945.3, 'qoq_pct': 235546.6}, {'quarter': '2026-01-01', 'revenue': 3810.0, 'qoq_pct': -99.9}, {'quarter': '2026-04-01', 'revenue': 10257.24, 'qoq_pct': 169.2}] |
| 2258 | Lamps Plus Centennial | 2 | 169,902.10 | 45.30 | [{'quarter': '2025-07-01', 'revenue': 169902.1, 'qoq_pct': 40.9}, {'quarter': '2025-10-01', 'revenue': 159509.2, 'qoq_pct': -6.1}, {'quarter': '2026-01-01', 'revenue': 87409.96, 'qoq_pct': -45.2}, {'quarter': '2026-04-01', 'revenue': 126989.34, 'qoq_pct': 45.3}] |
| 1178 | Shanor Electric Supply Inc. | 3 | 165,861 | 5,477 | [{'quarter': '2025-07-01', 'revenue': 1718.0, 'qoq_pct': 48.6}, {'quarter': '2025-10-01', 'revenue': 2974.0, 'qoq_pct': 73.1}, {'quarter': '2026-01-01', 'revenue': 165861.0, 'qoq_pct': 5477.0}, {'quarter': '2026-04-01', 'revenue': 0.0, 'qoq_pct': -100.0}] |
| 34218 | Clive Daniel Home | 3 | 108,698.40 | 149.70 | [{'quarter': '2025-07-01', 'revenue': 64466.1, 'qoq_pct': 36.7}, {'quarter': '2025-10-01', 'revenue': 108698.4, 'qoq_pct': 68.6}, {'quarter': '2026-01-01', 'revenue': 19035.0, 'qoq_pct': -82.5}, {'quarter': '2026-04-01', 'revenue': 47521.0, 'qoq_pct': 149.7}] |
| 37085 | Decorators Unlimited Inc | 2 | 89,674.80 | 350.40 | [{'quarter': '2025-07-01', 'revenue': 89674.8, 'qoq_pct': 350.4}, {'quarter': '2025-10-01', 'revenue': 7924.8, 'qoq_pct': -91.2}, {'quarter': '2026-01-01', 'revenue': 12267.4, 'qoq_pct': 54.8}, {'quarter': '2026-04-01', 'revenue': 3468.0, 'qoq_pct': -71.7}] |
| 26456 | Bridget Bohacz + Associates, Inc. | 2 | 87,260.40 | 2,190.30 | [{'quarter': '2025-07-01', 'revenue': 87260.4, 'qoq_pct': 2190.3}, {'quarter': '2026-01-01', 'revenue': 2991.2, 'qoq_pct': -96.6}, {'quarter': '2026-04-01', 'revenue': 4128.4, 'qoq_pct': 38.0}] |
| 11365 | Fogg Lighting | 2 | 83,699.62 | 236.90 | [{'quarter': '2025-07-01', 'revenue': 18546.32, 'qoq_pct': -17.0}, {'quarter': '2025-10-01', 'revenue': 24842.24, 'qoq_pct': 33.9}, {'quarter': '2026-01-01', 'revenue': 83699.62, 'qoq_pct': 236.9}, {'quarter': '2026-04-01', 'revenue': 36456.0, 'qoq_pct': -56.4}] |
| 1531 | Crescent Lighting Supply | 2 | 71,526.10 | 83.40 | [{'quarter': '2025-07-01', 'revenue': 37958.0, 'qoq_pct': 60.1}, {'quarter': '2025-10-01', 'revenue': 69606.0, 'qoq_pct': 83.4}, {'quarter': '2026-01-01', 'revenue': 71526.1, 'qoq_pct': 2.8}, {'quarter': '2026-04-01', 'revenue': 27074.6, 'qoq_pct': -62.1}] |
| 10698 | Ray Lighting Center | 3 | 67,424 | 84 | [{'quarter': '2025-07-01', 'revenue': 27066.0, 'qoq_pct': 50.1}, {'quarter': '2025-10-01', 'revenue': 49814.0, 'qoq_pct': 84.0}, {'quarter': '2026-01-01', 'revenue': 67424.0, 'qoq_pct': 35.4}, {'quarter': '2026-04-01', 'revenue': 48088.0, 'qoq_pct': -28.7}] |
| 1716 | Valley Light Gallery | 3 | 62,692.64 | 116.70 | [{'quarter': '2025-07-01', 'revenue': 21265.0, 'qoq_pct': 84.6}, {'quarter': '2025-10-01', 'revenue': 46086.62, 'qoq_pct': 116.7}, {'quarter': '2026-01-01', 'revenue': 62692.64, 'qoq_pct': 36.0}, {'quarter': '2026-04-01', 'revenue': 33026.24, 'qoq_pct': -47.3}] |
| 13825 | Designers Resource Collection | 2 | 61,920 | 1,602.30 | [{'quarter': '2025-07-01', 'revenue': 1798.0, 'qoq_pct': 25.2}, {'quarter': '2025-10-01', 'revenue': 469.0, 'qoq_pct': -73.9}, {'quarter': '2026-01-01', 'revenue': 7984.0, 'qoq_pct': 1602.3}, {'quarter': '2026-04-01', 'revenue': 61920.0, 'qoq_pct': 675.6}] |
| 11951 | Inside Source | 2 | 58,647.56 | 71.20 | [{'quarter': '2025-07-01', 'revenue': 34264.72, 'qoq_pct': 38.1}, {'quarter': '2025-10-01', 'revenue': 58647.56, 'qoq_pct': 71.2}, {'quarter': '2026-01-01', 'revenue': 40158.0, 'qoq_pct': -31.5}, {'quarter': '2026-04-01', 'revenue': 5040.0, 'qoq_pct': -87.4}] |
| 13689 | F.W. Webb Company | 2 | 58,117.17 | 100.20 | [{'quarter': '2025-07-01', 'revenue': 58117.17, 'qoq_pct': 31.3}, {'quarter': '2025-10-01', 'revenue': 19806.82, 'qoq_pct': -65.9}, {'quarter': '2026-01-01', 'revenue': 39659.1, 'qoq_pct': 100.2}, {'quarter': '2026-04-01', 'revenue': 15867.1, 'qoq_pct': -60.0}] |
| 2055 | Lighting Design Center | 2 | 55,405 | 152.90 | [{'quarter': '2025-07-01', 'revenue': 55405.0, 'qoq_pct': 60.2}, {'quarter': '2025-10-01', 'revenue': 20228.6, 'qoq_pct': -63.5}, {'quarter': '2026-01-01', 'revenue': 51156.0, 'qoq_pct': 152.9}, {'quarter': '2026-04-01', 'revenue': 11656.0, 'qoq_pct': -77.2}] |
| 12437 | Fan & Lighting World | 2 | 53,030 | 242 | [{'quarter': '2025-07-01', 'revenue': 43642.0, 'qoq_pct': 71.6}, {'quarter': '2025-10-01', 'revenue': 15504.0, 'qoq_pct': -64.5}, {'quarter': '2026-01-01', 'revenue': 53030.0, 'qoq_pct': 242.0}, {'quarter': '2026-04-01', 'revenue': 26011.0, 'qoq_pct': -51.0}] |

### Q-ORG-STOCKOUT_results.md

(not present — file does not exist or is empty)
