# Section 2 Context Bundle — Maxim Lighting (mli)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Maxim Lighting  (mli, org_id=137)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=6490 |
| HAS_SALES_DATA | True | sales_data_count=189283 |
| HAS_SALES_SECTION | True | mode=engagement order_reps=1 engagement_reps=68 (threshold: >=5) |
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
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 1 | 1 |
| ENGAGEMENT_REP_COUNT | 68 | engagement_reps=68 (>= 50 selling-activity events, 12mo) |
| SALES_SECTION_MODE | engagement | engagement |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 91, Mixpanel total submit_order (Q-01): 102 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=82.4%, ambiguous_rate=0.0%, showroom_event_share=4.9% |
| USER_GROUP_JOIN_RATE | 82% | 75 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 5% | showroom+admin share of matched events: 4.9% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Nathen Bliss |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=210 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Maxim Lighting 
- **Shortname**: mli
- **Org ID**: 137
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — Maxim Lighting  (mli, org_id=137)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| PORTAL_ORDERS_FRESH | False |
| HAS_PORTAL_ORDERS | False |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | PARTIAL | See Derived Gate 6 §5 formula |

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

# Signal Rank — Maxim Lighting  (mli, org_id=137)
- **Run date**: 2026-06-17
- **Total signals fired**: 22 (P0: 9, P1: 10, P2: 3)
- **Org GMV**: $0.0M eCat LTM, $0.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-ANOMALY-02 | Stock Out — 57664WTBK (Trim 11" RD LED Flush Mount 3000K) $282,149 LTM, 0 available | P0 | §3 Product | 10.0 | $282,149 | 3.0 | 8,464,477 | RISK |
| 2 | SIG-ANOMALY-02 | Stock Out — 10283SWBK (Lateral 3-Light Bath Vanity) $229,831 LTM, 0 available | P0 | §3 Product | 10.0 | $229,831 | 3.0 | 6,894,921 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — 52102SN (Rail 24" LED Bath Vanity) $228,969 LTM, 0 available | P0 | §3 Product | 10.0 | $228,969 | 3.0 | 6,869,072 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — 57933WTWT (Diverse 13" LED Flush Mount 3000K) $132,528 LTM, 0 available | P0 | §3 Product | 10.0 | $132,528 | 3.0 | 3,975,831 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 88707BK (Falcon Pull Chain 52" In/Outdoor Fan w L) $117,033 LTM, 0 available | P0 | §3 Product | 10.0 | $117,033 | 3.0 | 3,510,997 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 88708SN (Falcon AC Damp 52" In/Out Fan w LED Ligh) $101,340 LTM, 0 available | P0 | §3 Product | 10.0 | $101,340 | 3.0 | 3,040,211 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 61018GS (Odeon 8-Light WiFi-enabled LED Fandeligh) $100,438 LTM, 0 available | P0 | §3 Product | 10.0 | $100,438 | 3.0 | 3,013,150 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 12262CDBK (Acadia 2-Light Bath Vanity) $98,559 LTM, 0 available | P0 | §3 Product | 10.0 | $98,559 | 3.0 | 2,956,773 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — E25052-CHK (Souffle 8.5" 1-Light Pendant) $98,083 LTM, 0 available | P0 | §3 Product | 10.0 | $98,083 | 3.0 | 2,942,491 | RISK |
| 10 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 66% of eCat GMV | P1 | §4 Commerce | 1.6 | $307,432 | 2.0 | 1,013,488 | RISK |
| 11 | SIG-OPP-04 | New Item Adoption Gap — 22 new items with $0 platform orders | P2 | §3 Product | 2.2 | $50,000 | 1.0 | 110,000 | POSITIVE |
| 12 | SIG-RISK-03 | Data Staleness — contract_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 13 | SIG-RISK-03 | Data Staleness — kit_items last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 14 | SIG-RISK-03 | Data Staleness — matrix_options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 15 | SIG-RISK-03 | Data Staleness — option_groups last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 16 | SIG-RISK-03 | Data Staleness — options last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 17 | SIG-RISK-03 | Data Staleness — commitment_reports last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 18 | SIG-RISK-03 | Data Staleness — riser_prices last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 19 | SIG-RISK-03 | Data Staleness — customer_payment_informations last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |
| 20 | SIG-RISK-03 | Data Staleness — sales_quotas last updated 313d ago | P1 | §6 Platform | 3.5 | $1 | 2.0 | 7 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 0 | 1 | 0 | 1 | |
| §6 Platform Context | 0 | 9 | 2 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 22 new items with $0 platform orders
2. **[RISK]** SIG-ANOMALY-02: Stock Out — 57664WTBK (Trim 11" RD LED Flush Mount 3000K) $282,149 LTM, 0 available
3. **[RISK]** SIG-ANOMALY-02: Stock Out — 10283SWBK (Lateral 3-Light Bath Vanity) $229,831 LTM, 0 available
4. **[RISK]** SIG-ANOMALY-02: Stock Out — 52102SN (Rail 24" LED Bath Vanity) $228,969 LTM, 0 available
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 57933WTWT (Diverse 13" LED Flush Mount 3000K) $132,528 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 88707BK (Falcon Pull Chain 52" In/Outdoor Fan w L) $117,033 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 88708SN (Falcon AC Damp 52" In/Out Fan w LED Ligh) $101,340 LTM, 0 available

**Balance check**: 1 positive (slots 1-1), 6 risk (slots 2-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Maxim Lighting  (mli, org_id=137)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |

### Q-12_results.md

# Q-12 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 9,352 | 136 | 65 | 62 | 5 |

### Q-14_results.md

# Q-14 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 4
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 43RSAI-DROP | 43RD STREET LIGHTING, INC. | 5 | $18,387 | 2026-01-08 18:42:35 | 2026-01-08 21:50:50 | 0 |
| CARCA2- | CARTWRIGHT LIGHTING | 3 | $30,356 | 2026-01-09 22:23:25 | 2026-01-11 18:13:21 | 0.90 |
| COAPORTI- | COASTAL LIGHTING LLC. | 3 | $36,975 | 2026-01-11 15:33:55 | 2026-01-12 15:29:34 | 0.50 |
| RAYBEAUM- | RAY MART INC. | 3 | $61,066 | 2026-01-10 21:28:08 | 2026-01-14 03:17:04 | 1.60 |

### Q-14b_results.md

(not present — file does not exist or is empty)

### Q-17_results.md

# Q-17 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| LIGHOU-AUSTIN | LIGHTING, INC. OFFICE-AUSTIN | TX | 2026-01-14 03:15:00 | 2 | $99,353 |
| HAJLAFAY-MOOCOL | MOORE SUPPLY 705-COLLEGE STATION,TX | TX | 2026-01-11 17:41:26 | 2 | $67,054 |
| RAYBEAUM- | RAY MART INC. | TX | 2026-01-14 03:17:04 | 3 | $61,066 |
| FERHAM-FE2775 | FERGUSON-CONROE, TX | TX | 2026-01-14 00:34:59 | 1 | $42,984 |
| COAPORTI- | COASTAL LIGHTING LLC. | TX | 2026-01-12 15:29:34 | 3 | $36,975 |
| CARCA2- | CARTWRIGHT LIGHTING | AB | 2026-01-11 18:13:21 | 3 | $30,356 |
| Z9274000- | SURFSIDE CASUAL CORPORATION | NJ | 2026-01-13 20:25:03 | 1 | $26,021 |
| 43RSAI-DROP | 43RD STREET LIGHTING, INC. | MN | 2026-01-08 21:50:50 | 5 | $18,387 |
| DENAMB- | DENNEY ELECTRIC SUPPLY | PA | 2026-01-13 20:31:12 | 1 | $14,638 |
| SHARIC- | SHADES OF LIGHT LLC | VA | 2026-01-13 16:57:11 | 1 | $13,907 |
| FORFOR- | FORT WORTH LIGHTING | TX | 2026-01-13 23:12:55 | 1 | $13,216 |
| DULSTE- | DULLES ELECTRIC & SUPPLY | VA | 2026-01-11 16:12:42 | 1 | $11,505 |
| ROBWINNI-ROBWI2 | ROBINSON LIGHTING-WINNIPEG | MB | 2026-01-10 15:21:51 | 1 | $10,818 |
| LIGFREDE- | LIGHT & DAY | MD | 2026-01-14 14:25:01 | 2 | $10,032 |
| LEEINDIA-LEEDAY | LEE SUPPLY CORP.-DAYTON, OH | OH | 2026-01-10 16:19:28 | 1 | $9,971 |
| FERHAM-FEI230 | FERGUSON-OKLAHOMA, OK | OK | 2026-01-13 23:14:10 | 1 | $9,726 |
| CARHUM- | CAROL'S LIGHTING & FAN SHOP | TX | 2026-01-14 00:22:13 | 1 | $8,108 |
| SUPWINNI- | SUPERLITE | MB | 2026-01-12 18:50:24 | 1 | $8,031 |
| HUNOKL-SHIP | HUNZICKER BROTHERS INC | OK | 2026-01-13 23:16:15 | 1 | $7,531 |
| N&SHUN- | N&S ELECTRIC SUPPLY & LIGHTING | NY | 2025-12-23 14:26:17 | 1 | $7,465 |
| SHOLAR- | SHOWCASE LIGHTING BY 3-G, LTD | TX | 2026-01-11 16:55:12 | 2 | $7,314 |
| LITVAU- | LITEMODE LIMITED | ON | 2026-01-21 01:23:05 | 1 | $7,292 |
| HILKER- | HILL COUNTRY LIGHTING CENTER | TX | 2026-01-13 20:06:29 | 1 | $7,114 |
| CHLNORWA- | CHLOE WINSTON LIGHTING DESIGN LLC. | CT | 2026-01-10 18:42:25 | 2 | $6,206 |
| LIGLEW- | LIGHT HOUSE OF LEWES | DE | 2026-01-13 20:24:08 | 1 | $5,834 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| LIGHOU-AUSTIN | LIGHTING, INC. OFFICE-AUSTIN | TX | $99,353 | 2026-01-14 03:15:00 | 154 |
| HAJLAFAY-MOOCOL | MOORE SUPPLY 705-COLLEGE STATION,TX | TX | $67,054 | 2026-01-11 17:41:26 | 156 |
| RAYBEAUM- | RAY MART INC. | TX | $61,066 | 2026-01-14 03:17:04 | 154 |
| FERHAM-FE2775 | FERGUSON-CONROE, TX | TX | $42,984 | 2026-01-14 00:34:59 | 154 |
| COAPORTI- | COASTAL LIGHTING LLC. | TX | $36,975 | 2026-01-12 15:29:34 | 155 |
| CARCA2- | CARTWRIGHT LIGHTING | AB | $30,356 | 2026-01-11 18:13:21 | 156 |
| Z9274000- | SURFSIDE CASUAL CORPORATION | NJ | $26,021 | 2026-01-13 20:25:03 | 154 |
| 43RSAI-DROP | 43RD STREET LIGHTING, INC. | MN | $18,387 | 2026-01-08 21:50:50 | 159 |
| DENAMB- | DENNEY ELECTRIC SUPPLY | PA | $14,638 | 2026-01-13 20:31:12 | 154 |
| SHARIC- | SHADES OF LIGHT LLC | VA | $13,907 | 2026-01-13 16:57:11 | 154 |
| FORFOR- | FORT WORTH LIGHTING | TX | $13,216 | 2026-01-13 23:12:55 | 154 |
| DULSTE- | DULLES ELECTRIC & SUPPLY | VA | $11,505 | 2026-01-11 16:12:42 | 156 |
| ROBWINNI-ROBWI2 | ROBINSON LIGHTING-WINNIPEG | MB | $10,818 | 2026-01-10 15:21:51 | 157 |
| LIGFREDE- | LIGHT & DAY | MD | $10,032 | 2026-01-14 14:25:01 | 153 |
| LEEINDIA-LEEDAY | LEE SUPPLY CORP.-DAYTON, OH | OH | $9,971 | 2026-01-10 16:19:28 | 157 |
| FERHAM-FEI230 | FERGUSON-OKLAHOMA, OK | OK | $9,726 | 2026-01-13 23:14:10 | 154 |
| CARHUM- | CAROL'S LIGHTING & FAN SHOP | TX | $8,108 | 2026-01-14 00:22:13 | 154 |
| SUPWINNI- | SUPERLITE | MB | $8,031 | 2026-01-12 18:50:24 | 155 |
| HUNOKL-SHIP | HUNZICKER BROTHERS INC | OK | $7,531 | 2026-01-13 23:16:15 | 154 |
| N&SHUN- | N&S ELECTRIC SUPPLY & LIGHTING | NY | $7,465 | 2025-12-23 14:26:17 | 175 |

### Q-40_results.md

# Q-40 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| TX | 20 | 28 | $380,933 |
| VA | 5 | 5 | $38,478 |
| AB | 1 | 3 | $30,356 |
| NJ | 2 | 2 | $29,234 |
| NY | 6 | 7 | $24,831 |
| MB | 3 | 3 | $23,898 |
| OK | 4 | 4 | $23,241 |
| PA | 4 | 5 | $20,974 |
| MN | 1 | 5 | $18,387 |
| ON | 3 | 4 | $14,661 |
| CT | 3 | 4 | $14,551 |
| MD | 1 | 2 | $10,032 |
| OH | 1 | 1 | $9,971 |
| DE | 1 | 1 | $5,834 |
| IL | 1 | 2 | $5,462 |
| MA | 1 | 1 | $4,721 |
| KS | 1 | 1 | $4,392 |
| BC | 1 | 1 | $3,674 |
| FL | 1 | 1 | $3,470 |
| CA | 1 | 1 | $3,457 |

### Q-41_results.md

# Q-41 Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 8
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-04-01 | Rep-Acquired (iPad) | 2 |
| 2025-06-01 | Rep-Acquired (iPad) | 2 |
| 2025-08-01 | Rep-Acquired (iPad) | 2 |
| 2025-12-01 | Rep-Acquired (iPad) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 52 |
| 2026-02-01 | Rep-Acquired (iPad) | 1 |
| 2026-03-01 | Rep-Acquired (iPad) | 2 |
| 2026-05-01 | Rep-Acquired (iPad) | 2 |

### Q-41_rep_results.md

# Q-41-rep Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 24
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Newell King | 7 |
| Alex Miranda | 6 |
| Todd Pawlowski | 6 |
| Mike Elford | 5 |
| John Boyd | 5 |
| Nathen Bliss | 4 |
| Brian Walter | 4 |
| Jeff Izower | 4 |
| Peter Saiolla | 3 |
| Tim Gietz | 3 |
| Kristen Cavanagh | 2 |
| Rob Antonecchia | 2 |
| Scott Fellner | 2 |
| Paul Mackey | 1 |
| Peter Scalia | 1 |
| Susan Collins | 1 |
| Tim Green | 1 |
| Allison Murillo | 1 |
| Karl Prekaski | 1 |
| Troy  Kaup | 1 |
| Kirk Johnson | 1 |
| Howell Turner | 1 |
| Brad Krieger | 1 |
| Ashlyn Elliot | 1 |

### Q-52_results.md

(not present — file does not exist or is empty)

### Q-53_results.md

(not present — file does not exist or is empty)

### Q-54_results.md

(not present — file does not exist or is empty)

### Q-57_results.md

(not present — file does not exist or is empty)

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

(not present — file does not exist or is empty)

### Q-68_results.md

(not present — file does not exist or is empty)

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

(not present — file does not exist or is empty)

### Q-ORG-NBP_results.md

(not present — file does not exist or is empty)

### Q-ORG-CONTRACTION_results.md

(not present — file does not exist or is empty)

### Q-ORG-VELOCITY_results.md

(not present — file does not exist or is empty)

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Maxim Lighting  (mli, org_id=137)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 57664WTBK | Trim 11" RD LED Flush Mount 3000K | TRIM | 282,149.23 | 8,348 | — | 2026-06-26 | [{'customer': 'US ELECTRICAL SERVICES INC(USESI)', 'revenue': 72898.3}, {'customer': 'CAPITOL LIGHTING', 'revenue': 22635.2}, {'customer': 'FERGUSON-PERRIS, CA', 'revenue': 21425.75}, {'customer': 'HANSEN LIGHTING, INC.-LINDON, UT', 'revenue': 21232.5}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 10924.55}, {'customer': 'SHADES OF LIGHT LLC', 'revenue': 10613.36}, {'customer': 'SEATTLE LIGHTING-SEATTLE', 'revenue': 8777.47}, {'customer': 'PACIFIC LAMP & SUPPLY CO.', 'revenue': 6536.0}, {'customer': 'WAYFAIR LLC', 'revenue': 6033.9}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 6014.84}, {'customer': 'THE LIGHTING DESIGN-LAYTON, UT', 'revenue': 5733.3}, {'customer': 'FERGUSON-NAMPA, ID', 'revenue': 5159.17}, {'customer': 'LEGACY LIGHTING LLC', 'revenue': 4621.25}, {'customer': "FERGUSON-COEUR D'ALENE, ID", 'revenue': 4462.76}, {'customer': 'LIGHTWISE-BOLIVAR, MO', 'revenue': 4263.9}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 3564.05}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 3182.27}, {'customer': 'FERGUSON-NEW HUDSON, MI', 'revenue': 2937.4}, {'customer': 'JOSS AND MAIN-BOSTON', 'revenue': 2882.31}, {'customer': 'FERGUSON-FRONT ROYAL, VA', 'revenue': 2614.4}, {'customer': 'FERGUSON-ADDISON, IL', 'revenue': 2614.4}, {'customer': 'FERGUSON-PORTLAND, OR', 'revenue': 1952.0}, {'customer': 'FERGUSON-STOCKTON, CA', 'revenue': 1904.75}, {'customer': 'MAXWELL LIGHTING & ENERGY', 'revenue': 1832.5}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 1815.3}, {'customer': 'FERGUSON-MANCHESTER, NH', 'revenue': 1808.8}, {'customer': 'INDEPENDENT ELECTRIC-MANCHESTER, NH', 'revenue': 1747.5}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 1581.6}, {'customer': 'THE LIGHTING DESIGN, LLC', 'revenue': 1449.8}, {'customer': 'BUILDERS ELECTRIC INC.,CORP OF WY', 'revenue': 1372.0}, {'customer': 'CED - KENT, WA', 'revenue': 1333.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 1199.0}, {'customer': 'MAIN ELECTRIC SUPPLY CO.', 'revenue': 1073.0}, {'customer': 'LAMPS PLUS', 'revenue': 1032.72}, {'customer': 'LIGHTOLOGY', 'revenue': 795.68}, {'customer': 'LOWES COMPANIES', 'revenue': 785.4}, {'customer': 'HI-LIGHT LIGHTING', 'revenue': 774.0}, {'customer': 'ELLEN LIGHTING & HARDWARE-SUGARLAND', 'revenue': 774.0}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 774.0}, {'customer': 'PARAMONT-EO, INC.-NEW LENOX, IL', 'revenue': 633.0}, {'customer': 'WALTERS WHOLESALE ELECTRIC', 'revenue': 598.75}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 598.56}, {'customer': 'FERGUSON-RICHMOND, VA', 'revenue': 568.1}, {'customer': 'FERGUSON-FORT PAYNE, AL', 'revenue': 531.05}, {'customer': "FERGUSON-O'FALLON, MO", 'revenue': 526.3}, {'customer': 'POWER DESIGN RESOURCES', 'revenue': 516.0}, {'customer': 'CED-DALLAS, TX', 'revenue': 516.0}, {'customer': 'WAYFAIR LLC-CRANBURY, NJ', 'revenue': 511.22}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 500.6}, {'customer': 'FERGUSON-GRIMES, IA', 'revenue': 490.2}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 483.55}, {'customer': 'FERGUSON-FREDERICKSBURG, VA', 'revenue': 482.6}, {'customer': 'NORTHEAST ELECTRICAL-HAVERHILL, MA', 'revenue': 473.0}, {'customer': 'HAUS APPEAL LLC', 'revenue': 464.4}, {'customer': 'HOME LIGHTING', 'revenue': 450.1}, {'customer': 'FERGUSON-LEBANON, TN', 'revenue': 449.35}, {'customer': 'LIGHTS UNLIMITED  INC.-WAKE FOREST', 'revenue': 430.0}, {'customer': 'E.B. LIGHTING & SUPPLIES, INC.', 'revenue': 430.0}, {'customer': 'WAYFAIR LLC-LANCASTER, TX', 'revenue': 426.91}, {'customer': 'WAYFAIR LLC-PERRIS, CA', 'revenue': 421.09}, {'customer': 'LAMPS PLUS', 'revenue': 407.1}, {'customer': 'DU PAGE LIGHTING', 'revenue': 371.0}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 359.0}, {'customer': 'ELEKTRA LIGHTS & FANS, INC.', 'revenue': 355.5}, {'customer': 'KENDALL ELECTRIC-GRAND RAPIDS, MI', 'revenue': 344.0}, {'customer': 'THE LIGHTING CORNER', 'revenue': 344.0}, {'customer': 'WILSON LIGHTING', 'revenue': 344.0}, {'customer': 'URBAN LIGHTS-DENVER, CO', 'revenue': 339.5}, {'customer': 'FERGUSON-AURORA, CO', 'revenue': 319.2}, {'customer': 'ULTRA DESIGN CENTER', 'revenue': 301.0}, {'customer': 'LEE SUPPLY CORP.-NEW ALBANY, IN', 'revenue': 301.0}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 301.0}, {'customer': 'WAYFAIR LLC-MCDONOUGH, GA', 'revenue': 293.88}, {'customer': 'ELECTRICAL WHOLESALE-IDAHO FALLS,ID', 'revenue': 270.0}, {'customer': 'URBAN LIGHTS', 'revenue': 267.3}, {'customer': 'THE FAN CONNECTION', 'revenue': 258.0}, {'customer': 'MICHAELS ELECTRICAL SUPPLY', 'revenue': 258.0}, {'customer': 'W.T. LIGHTING-ROCHESTER', 'revenue': 258.0}, {'customer': 'FERGUSON-EAST SYRACUSE, NY', 'revenue': 245.1}, {'customer': 'FERGUSON-WILLIAMSBURG, VA', 'revenue': 245.1}, {'customer': 'ROCKINGHAM ELECTRICAL-NEWINGTON', 'revenue': 244.79}, {'customer': 'KBL DESIGN CENTER, INC.', 'revenue': 233.7}, {'customer': 'JONES LIGHTING SPECIALISTS', 'revenue': 227.9}, {'customer': 'FERGUSON-FRANKLIN, NC', 'revenue': 222.3}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 221.4}, {'customer': 'B.E.S. LIGHTING CENTER', 'revenue': 215.0}, {'customer': 'CAPE ELECTRIC SUPPLY', 'revenue': 215.0}, {'customer': 'SYNERGY LIGHT STUDIO', 'revenue': 215.0}, {'customer': 'DHILLON LIGHTING INC.-WINNIPEG, MB', 'revenue': 215.0}, {'customer': 'PARAMONT-EO INC.-CHICAGO', 'revenue': 215.0}, {'customer': 'FERGUSON-ALPHARETTA, GA', 'revenue': 204.25}, {'customer': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'revenue': 204.25}, {'customer': 'THE LIGHTING SHOPPE', 'revenue': 204.25}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 204.25}, {'customer': 'LEE SUPPLY CORP.', 'revenue': 195.65}, {'customer': 'FLEX DISTRIBUTION C/O CAPSTONE LTG', 'revenue': 195.0}, {'customer': 'BRIGHTER HOMES LIGHTING-EUGENE', 'revenue': 190.94}, {'customer': 'CITY ELECTRIC SUPPLY-PASADENA, CA', 'revenue': 189.2}, {'customer': 'FERGUSON-LEWISVILLE, TX', 'revenue': 185.25}, {'customer': 'FERGUSON-CHARLOTTESVILLE, VA', 'revenue': 185.25}, {'customer': 'ULTRA LIGHTING-MISSISSAUGA', 'revenue': 172.0}, {'customer': 'STARLIGHT LIGHTING CENTRE', 'revenue': 172.0}, {'customer': 'KENNEWICK IND/DBA KIE SUPPLY', 'revenue': 172.0}, {'customer': 'LIGHTOPIA', 'revenue': 168.0}, {'customer': 'R. WILSON CO. INC.-LENEXA, KS', 'revenue': 163.4}, {'customer': 'FERGUSON-FARGO, ND', 'revenue': 163.4}, {'customer': 'FERGUSON-COLUMBUS, OH', 'revenue': 159.6}, {'customer': 'PLATT ELECTRIC-MOUNTLAKE TERRACE,WA', 'revenue': 156.0}, {'customer': 'LIGHTING, INC. OFFICE-HOUSTON', 'revenue': 140.4}, {'customer': 'KENDALL ELECTRIC, INC.-COLUMBUS, OH', 'revenue': 129.0}, {'customer': 'GALAXY LIGHTING', 'revenue': 129.0}, {'customer': 'JUST LIGHTS INC.', 'revenue': 129.0}, {'customer': 'KNOXVILLE NOLAND CO.-KNOXVILLE, TN', 'revenue': 129.0}, {'customer': 'DHILLON LIGHTING CALGARY LTD.', 'revenue': 129.0}, {'customer': 'TIMBERLAKE LIGHTING OF LYNCHBURG', 'revenue': 129.0}, {'customer': 'YALE ELECTRIC-LANCASTER, PA', 'revenue': 129.0}, {'customer': 'WAREHOUSE-LIGHTING.COM', 'revenue': 129.0}, {'customer': 'COLONIAL ELECTRIC-PHILADELPHIA, PA', 'revenue': 129.0}, {'customer': 'HERITAGE INTERIORS & DESIGN', 'revenue': 129.0}, {'customer': 'PLATT ELECTRIC-KENT, WA', 'revenue': 129.0}, {'customer': 'FERGUSON-SAN ANTONIO, TX', 'revenue': 122.55}, {'customer': 'FERGUSON-BATON ROUGE, LA', 'revenue': 122.55}, {'customer': 'FERGUSON-VISTA, CA', 'revenue': 122.55}, {'customer': 'LAMPS.COM', 'revenue': 122.55}, {'customer': 'FERGUSON-COLUMBIA, SC', 'revenue': 122.55}, {'customer': 'FERGUSON-GOLDEN VALLEY, MN', 'revenue': 122.55}, {'customer': 'FERGUSON-HOLLY SPRINGS, NC', 'revenue': 122.55}, {'customer': 'FERGUSON-LEXINGTON, KY', 'revenue': 118.75}, {'customer': 'COLONIAL LIGHTING-DECATUR, GA', 'revenue': 117.0}, {'customer': 'INCOLIGHT GROUP LLC.', 'revenue': 117.0}, {'customer': '43RD STREET LIGHTING, INC.', 'revenue': 117.0}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 116.1}, {'customer': 'FERGUSON-MEMPHIS, TN', 'revenue': 114.95}, {'customer': 'FERGUSON-CORPUS CHRISTI, TX', 'revenue': 111.15}, {'customer': 'WAYFAIR LLC-PORT WENTWORTH, GA', 'revenue': 109.65}, {'customer': 'PLATT ELECTRIC SUPPLY', 'revenue': 108.0}, {'customer': 'CRESCENT LIGHTING-SPOKANE VALLEY,WA', 'revenue': 104.91}, {'customer': 'NORTH COAST LIGHTING-PORTLAND, OR', 'revenue': 95.91}, {'customer': 'BRIGHT IDEAS INC.', 'revenue': 86.0}, {'customer': 'PINE TREE LIGHTING-LAKE ORION', 'revenue': 86.0}, {'customer': 'LEE SUPPLY CORP.-DAYTON, OH', 'revenue': 86.0}, {'customer': 'TRI-SUPPLY-AUSTIN, TX', 'revenue': 86.0}, {'customer': 'LEE SUPPLY CORP.-CARMEL', 'revenue': 86.0}, {'customer': 'STATE ELECTRIC-CHRISTIANSBURG, VA', 'revenue': 86.0}, {'customer': 'LIGHT BRITE DISTRIBUTING-TRENTON', 'revenue': 82.0}, {'customer': 'CASA DI LUCE', 'revenue': 82.0}, {'customer': 'PREMIER LIGHTING-PHOENIX, AZ', 'revenue': 81.7}, {'customer': 'FERGUSON-TAUNTON, MA', 'revenue': 81.7}, {'customer': 'FERGUSON ENTERPRISES-LEWISTON,ID', 'revenue': 81.7}, {'customer': 'FERGUSON-LANSING, MI', 'revenue': 81.7}, {'customer': 'KENDALL ELECTRIC-FORT WAYNE, IN', 'revenue': 78.0}, {'customer': 'CABINET & LIGHTING SUPPLY', 'revenue': 78.0}, {'customer': 'FERGUSON-BROOKSHIRE, TX', 'revenue': 77.9}, {'customer': 'LIGHTING, INC. OFFICE-AUSTIN', 'revenue': 77.4}, {'customer': 'WILLCALL FOR LIGHT CONCERN', 'revenue': 75.66}, {'customer': 'FERGUSON-SUMNER, WA', 'revenue': 66.94}, {'customer': 'MV BY DESIGN', 'revenue': 54.0}, {'customer': 'CITY LIGHTS', 'revenue': 43.0}, {'customer': 'RAINBOW LIGHTING', 'revenue': 43.0}, {'customer': 'SHEPARD LIGHTING', 'revenue': 43.0}, {'customer': 'CASA DI LUCE', 'revenue': 43.0}, {'customer': 'LIGHTING BY LDI', 'revenue': 43.0}, {'customer': 'THE LIGHT CENTER', 'revenue': 43.0}, {'customer': 'MAIN ELECTRIC SUPPLY-SAN DIEGO, CA', 'revenue': 42.9}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 42.75}, {'customer': 'FERGUSON - SOUTH BEND, IN', 'revenue': 40.85}, {'customer': 'FERGUSON-JACKSON, WY', 'revenue': 40.85}, {'customer': 'FERGUSON-ROANOKE, VA', 'revenue': 40.85}, {'customer': 'SUN LIGHTING', 'revenue': 40.85}, {'customer': 'FERGUSON-NORFOLK, VA', 'revenue': 40.85}, {'customer': 'FERGUSON- CHANDLER,AZ', 'revenue': 40.85}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 40.85}, {'customer': 'ROBINSON LIGHTING', 'revenue': 40.85}, {'customer': 'FERGUSON-SEATTLE, WA', 'revenue': 40.85}, {'customer': 'FERGUSON-GRAND PRAIRIE, TX', 'revenue': 40.85}, {'customer': 'FERGUSON-JOHNSON CITY, TN', 'revenue': 40.85}, {'customer': 'FERGUSON-WEST ALLIS, WI', 'revenue': 40.85}, {'customer': 'LIGHT BULBS ETC.', 'revenue': 40.85}, {'customer': 'FERGUSON-HUDSON, WI', 'revenue': 40.85}, {'customer': 'FERGUSON-ROUND ROCK, TX', 'revenue': 40.85}, {'customer': 'FERGUSON-ST. GEORGE, UT', 'revenue': 40.85}, {'customer': 'UNION LIGHTING', 'revenue': 40.85}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 39.0}, {'customer': 'MARX FIREPLACES & LIGHTING', 'revenue': 39.0}, {'customer': 'GROVER ELECTRIC-MEDFORD, OR', 'revenue': 39.0}, {'customer': 'MCLAREN LIGHTING', 'revenue': 39.0}, {'customer': 'FANCO - LAS VEGAS, NV', 'revenue': 39.0}, {'customer': 'LA LUZ LIGHTING LLC.', 'revenue': 39.0}, {'customer': 'METRO ELECTRIC SUPPLY-BRENTWOOD, MO', 'revenue': 38.7}, {'customer': 'PINE LIGHTING-KELOWNA', 'revenue': 38.7}, {'customer': 'WAYFAIR LLC -PERIGOLD', 'revenue': 36.55}, {'customer': 'CRESCENT LIGHTING SUPPLY-OLYMPIA,WA', 'revenue': 34.97}, {'customer': 'CRESCENT LIGHTING-BURLINGTON, WA', 'revenue': 34.97}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY', 'revenue': 34.95}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 32.95}, {'customer': 'URBAN LIGHTS', 'revenue': 31.55}, {'customer': 'ALL CITY LIGHTING & SUPPLIES INC.', 'revenue': 30.95}, {'customer': 'CAPITAL ELECTRIC-UPPER MARLBORO, MD', 'revenue': 30.1}, {'customer': 'WASATCH LIGHTING', 'revenue': 21.5}, {'customer': 'LIGHTS ON DESIGN, INC.', 'revenue': 19.5}, {'customer': 'CASA DI LUCE', 'revenue': 5.0}, {'customer': 'TURN ON LIGHTING', 'revenue': 0.0}] | [{'item': '57660WTWT', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 8984}, {'item': '57662WTWT', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 4604}, {'item': '57664WTSN', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 2689}, {'item': '57662WTBK', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 2103}, {'item': '57670WTBK', 'desc': 'Trim 16" RD LED Flush Mount 3000K', 'available': 1859}, {'item': '57663WTBK', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 1763}, {'item': '57664WTWT', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 1585}, {'item': '57663WTSN', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 1092}, {'item': '57662WTSN', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 989}, {'item': '57668WTWT', 'desc': 'Trim 8.5" SQ LED Flush Mount 3000K', 'available': 943}, {'item': '57667WTWT', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 900}, {'item': '57660WTSN', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 615}, {'item': '57668WTSN', 'desc': 'Trim 8.5" SQ LED Flush Mount 3000K', 'available': 585}, {'item': '57663WTWT', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 574}, {'item': '57670WTSN', 'desc': 'Trim 16" RD LED Flush Mount 3000K', 'available': 479}, {'item': '57675WTWT', 'desc': 'Trim 15.5" SQ LED Flush Mount 3000K', 'available': 325}, {'item': '57664WTPC', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 311}, {'item': '57663WTPC', 'desc': 'Trim 9" RD LED Flush Mount 3000K', 'available': 309}, {'item': '57669WTWT', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 265}, {'item': '57668WTBK', 'desc': 'Trim 8.5" SQ LED Flush Mount 3000K', 'available': 259}, {'item': '57667WTBK', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 258}, {'item': '57660WTSBR', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 251}, {'item': '57675WTBK', 'desc': 'Trim 15.5" SQ LED Flush Mount 3000K', 'available': 235}, {'item': '57665WTWT', 'desc': 'Trim 4.5" SQ LED Flush Mount 3000K', 'available': 232}, {'item': '57890WT', 'desc': 'Empty EM Shell for 7" Round Trim', 'available': 222}, {'item': '57669WTSN', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 211}, {'item': '57664WTSBR', 'desc': 'Trim 11" RD LED Flush Mount 3000K', 'available': 205}, {'item': '57662WTPC', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 196}, {'item': '57669WTBK', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 189}, {'item': '57670WTSBR', 'desc': 'Trim 16" RD LED Flush Mount 3000K', 'available': 173}, {'item': '57662WTSBR', 'desc': 'Trim 7" RD LED Flush Mount 3000K', 'available': 163}, {'item': '57600PC', 'desc': 'Pendant Conversion Kit for Trim 5766x - Chrome', 'available': 162}, {'item': '57665WTSN', 'desc': 'Trim 4.5" SQ LED Flush Mount 3000K', 'available': 155}, {'item': '57660WTPC', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 133}, {'item': '57665WTBK', 'desc': 'Trim 4.5" SQ LED Flush Mount 3000K', 'available': 127}, {'item': '57669WTPC', 'desc': 'Trim 10.5" SQ LED Flush Mount 3000K', 'available': 97}, {'item': '57660WTBK', 'desc': 'Trim 5" RD LED Flush Mount 3000K', 'available': 91}, {'item': '57675WTSN', 'desc': 'Trim 15.5" SQ LED Flush Mount 3000K', 'available': 86}, {'item': '57667WTSN', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 50}, {'item': '57667WTPC', 'desc': 'Trim 6.5" SQ LED Flush Mount 3000K', 'available': 8}] |
| 10283SWBK | Lateral 3-Light Bath Vanity | COL56 | 229,830.69 | 5,905 | — | 2026-06-29 | [{'customer': 'US ELECTRICAL SERVICES INC(USESI)', 'revenue': 31576.3}, {'customer': 'AVID LIGHTING, LLC', 'revenue': 25884.0}, {'customer': 'MAIN ELECTRIC SUPPLY CO.', 'revenue': 14269.2}, {'customer': 'CED-UPPER MARLBORO, MD', 'revenue': 11814.25}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 11728.2}, {'customer': 'CARRINGTON LIGHTING.COM', 'revenue': 10738.75}, {'customer': 'THE LIGHTING DESIGN, LLC', 'revenue': 10094.7}, {'customer': 'CBMC LIGHTING SOLUTIONS', 'revenue': 9534.45}, {'customer': 'CBMC LIGHTING SOLUTION-INDIANAPOLIS', 'revenue': 8095.4}, {'customer': 'DOMINION ELECTRIC SUPPLY, INC.', 'revenue': 7984.75}, {'customer': 'PEAK LIGHTING BULBS & BALLASTS,LLC', 'revenue': 7350.0}, {'customer': "DESIGNER'S MART", 'revenue': 5944.15}, {'customer': 'LIFESTYLES-TULSA', 'revenue': 5601.8}, {'customer': 'LIFESTYLES', 'revenue': 5374.7}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY-BARRINGTON', 'revenue': 5181.25}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 4721.25}, {'customer': 'CBMC LIGHTING SOLUTIONS', 'revenue': 4655.7}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 4419.05}, {'customer': 'ROBINSON LIGHTING-WINNIPEG', 'revenue': 3305.7}, {'customer': 'AZTEC LIGHTING', 'revenue': 3020.05}, {'customer': 'IBS LIGHTING, LTD. LLC', 'revenue': 2787.15}, {'customer': 'ILLUMINATE LIGHTING-LISBON, IA', 'revenue': 2695.0}, {'customer': 'STEADFAST LIGHTING LLC', 'revenue': 2548.0}, {'customer': 'IBS LIGHTING, LTD.-THE COLONY, TX', 'revenue': 2463.9}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 2450.0}, {'customer': 'TEXAS FLOOR SOURCE', 'revenue': 1987.2}, {'customer': 'ALL-PHASE ELECTRIC-GRAND JUNCTION', 'revenue': 1764.0}, {'customer': 'THE LIGHTING DESIGN-LAYTON, UT', 'revenue': 1745.7}, {'customer': 'ELECTRICAL PLUMBING STORE', 'revenue': 1568.0}, {'customer': 'SIGNATURE LIGHTING & FANS', 'revenue': 1422.5}, {'customer': 'REXEL USA, INC.-TEMPLE, TX', 'revenue': 882.0}, {'customer': 'PINE TREE LIGHTING-LAKE ORION', 'revenue': 796.95}, {'customer': 'FERGUSON-CELINA, OH', 'revenue': 698.25}, {'customer': 'LONG LIGHTING STUDIO INC.', 'revenue': 686.0}, {'customer': 'ROBINSON LIGHTING', 'revenue': 629.6}, {'customer': 'FRANKLIN BUILDING SUPPLY-POCATELLO', 'revenue': 584.25}, {'customer': 'TURNEY LIGHTING & ELECTRIC', 'revenue': 510.25}, {'customer': 'ALL-PHASE ELECTRIC-BLOOMINGTON, IN', 'revenue': 449.82}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 441.0}, {'customer': 'HAUS APPEAL LLC', 'revenue': 441.0}, {'customer': 'R. WILSON CO. INC.-LENEXA, KS', 'revenue': 418.95}, {'customer': 'LIGHTING, INC. OFFICE-HOUSTON', 'revenue': 407.05}, {'customer': 'WEL-LIT HOMES-OGDEN', 'revenue': 379.5}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 379.5}, {'customer': 'NORTH COAST LIGHTING-PORTLAND, OR', 'revenue': 366.93}, {'customer': 'GRAYBAR ELECTRIC-CHARLOTTE, NC', 'revenue': 343.0}, {'customer': 'METRO ELECTRIC SUPPLY-BRENTWOOD, MO', 'revenue': 308.7}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 294.0}, {'customer': 'FANDANGO LIGHTS & DECOR', 'revenue': 294.0}, {'customer': 'UNITED ELECTRIC SUPPLY CO', 'revenue': 245.7}, {'customer': 'TECHTRON PRODUCTS, INC.', 'revenue': 245.0}, {'customer': 'LAMPS PLUS', 'revenue': 244.02}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 203.85}, {'customer': 'DAKOTA WHOLESALE-SIOUX FALLS, SD', 'revenue': 203.01}, {'customer': 'GRAHAM LIGHTING-MEMPHIS', 'revenue': 196.0}, {'customer': 'MEDINA LIGHTING, INC.', 'revenue': 196.0}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 196.0}, {'customer': 'E. SAM JONES DISTRIBUTOR,', 'revenue': 196.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 196.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 184.75}, {'customer': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'revenue': 179.75}, {'customer': 'NORTH COAST LIGHTING-BILLINGS, MT', 'revenue': 163.08}, {'customer': 'BONAIRE LIGHTING SOLUTIONS', 'revenue': 162.85}, {'customer': 'THE LIGHTING CORNER', 'revenue': 159.8}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 147.0}, {'customer': 'NORTHERN LIGHTS & ACCENTS', 'revenue': 147.0}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 147.0}, {'customer': 'SEATTLE LIGHTING-SEATTLE', 'revenue': 147.0}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 147.0}, {'customer': 'SUMMIT ELECTRIC SUPPLY-PHOENIX, AZ', 'revenue': 147.0}, {'customer': 'BULB LIGHTING & DESIGN', 'revenue': 147.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 147.0}, {'customer': 'MULTI LUMINAIRE LAVAL', 'revenue': 139.65}, {'customer': 'GROVER ELECTRIC -BOISE', 'revenue': 125.31}, {'customer': 'CAPITAL CITY DESIGN CENTER, INC.', 'revenue': 125.01}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 124.95}, {'customer': 'MATHES ELECTRIC OF FORT WALTON', 'revenue': 124.71}, {'customer': 'ROBINSON LIGHTING-KELOWNA', 'revenue': 116.85}, {'customer': 'IMAGINE MORE', 'revenue': 104.85}, {'customer': 'SOUTH DADE LIGHTING INC.-MIAMI', 'revenue': 98.0}, {'customer': 'KANSAS LIGHTING DISTRICT-WICHITA', 'revenue': 98.0}, {'customer': 'THE LIGHTING CONNECTION', 'revenue': 98.0}, {'customer': 'LIVIO DESIGNS, LLC-LACOMBE, LA', 'revenue': 98.0}, {'customer': 'EAST COAST LUMBER BUILDING SUPPLY', 'revenue': 98.0}, {'customer': 'KENNEWICK IND/DBA KIE SUPPLY', 'revenue': 98.0}, {'customer': 'ABBEVILLE ELECTRIC SUPPLY INC.', 'revenue': 98.0}, {'customer': 'LITECRAFT LIGHTING-AUGUSTA, GA', 'revenue': 98.0}, {'customer': 'KENYON NOBLE LUMBER-BOZEMAN, MT', 'revenue': 98.0}, {'customer': 'KBL DESIGN CENTER, INC.', 'revenue': 93.1}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 88.2}, {'customer': 'WEL-LIT HOMES', 'revenue': 75.9}, {'customer': 'MAIN ELECTRIC SUPPLY-VENTURA, CA', 'revenue': 75.9}, {'customer': 'WAYFAIR LLC', 'revenue': 73.5}, {'customer': 'SUBURBAN WHOLESALE LIGHTING', 'revenue': 71.9}, {'customer': 'PLANK & TILE', 'revenue': 69.9}, {'customer': 'W.T. LIGHTING-ROCHESTER', 'revenue': 49.0}, {'customer': 'LYONS ELECTRIC SUPPLY', 'revenue': 49.0}, {'customer': 'THE HOME CENTER, INC', 'revenue': 49.0}, {'customer': 'THE OLDE PARSONAGE', 'revenue': 49.0}, {'customer': 'BRIGGS INC.', 'revenue': 49.0}, {'customer': 'GLOBE LIGHTING CO.-HAPPY VALLEY', 'revenue': 49.0}, {'customer': 'FIXTURE THIS INC.', 'revenue': 49.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 49.0}, {'customer': 'SIOUX FALLS LIGHTHOUSE', 'revenue': 49.0}, {'customer': 'ELITE LIGHTING INNOVATIONS', 'revenue': 49.0}, {'customer': 'E.G. PENNER BUILDING-STEINBACH', 'revenue': 49.0}, {'customer': 'VP SUPPLY CORPORATION-ROCHESTER', 'revenue': 49.0}, {'customer': "HAGEN'S LIGHTING", 'revenue': 49.0}, {'customer': 'ILLUMINATE LIGHTING', 'revenue': 49.0}, {'customer': 'HODGSON LIGHT & LOG', 'revenue': 49.0}, {'customer': 'LITEMODE LIMITED', 'revenue': 49.0}, {'customer': 'MULTI LUMINAIRE LEVIS', 'revenue': 46.55}, {'customer': 'FERGUSON-COLUMBIA, MO', 'revenue': 46.55}, {'customer': 'THE LIGHTING SHOPPE-WAREHOUSE', 'revenue': 46.55}, {'customer': 'LIGHTOLOGY', 'revenue': 45.33}, {'customer': 'GROVER ELECTRIC -NAMPA', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-GRANTS PASS, OR', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-KLAMATH FALLS, OR', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-TWIN FALLS', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC-MEDFORD, OR', 'revenue': 41.77}, {'customer': 'GROVER ELECTRIC & PLUMBING INC.', 'revenue': 41.77}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 38.95}, {'customer': 'KENDALL ELECTRIC-GRAND RAPIDS, MI', 'revenue': 37.95}, {'customer': 'MASTRO ELECTRIC SUPPLY CO.', 'revenue': 34.3}, {'customer': 'HABITECH SYSTEMS-ORMOND BEACH, FL', 'revenue': 24.5}] | [{'item': '10283CLSN', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 744}, {'item': '10282CLSN', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 734}, {'item': '10283SWSN', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 676}, {'item': '10284SWBK', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 422}, {'item': '10283CLBK', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 400}, {'item': '10281CLSN', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 400}, {'item': '10284CLBK', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 398}, {'item': '10282SWSN', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 389}, {'item': '10284CLSN', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 371}, {'item': '90281CLSN', 'desc': 'Lateral Mini Pendant', 'available': 245}, {'item': '90281SWSN', 'desc': 'Lateral Mini Pendant', 'available': 228}, {'item': '10283SWSBR', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 203}, {'item': '10282SWBK', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 199}, {'item': '10282CLBK', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 186}, {'item': '10286SWBK', 'desc': 'Lateral 5-Light Chandelier', 'available': 184}, {'item': '10285CLSN', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 170}, {'item': '90281CLBK', 'desc': 'Lateral Mini Pendant', 'available': 166}, {'item': '10282SWSBR', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 157}, {'item': '10284SWSBR', 'desc': 'Lateral 4-Light Bath Vanity', 'available': 157}, {'item': '90281SWBK', 'desc': 'Lateral Mini Pendant', 'available': 152}, {'item': '10286SWSN', 'desc': 'Lateral 5-Light Chandelier', 'available': 125}, {'item': '10285SWSN', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 92}, {'item': '90281CLSBR', 'desc': 'Lateral Mini Pendant', 'available': 90}, {'item': '10285CLBK', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 71}, {'item': '10287CLSN', 'desc': 'Lateral 3-Light Chandelier', 'available': 50}, {'item': '10281CLSBR', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 49}, {'item': '10285SWSBR', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 47}, {'item': '10282CLSBR', 'desc': 'Lateral 2-Light Bath Vanity', 'available': 47}, {'item': '10281SWBK', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 46}, {'item': '10283CLSBR', 'desc': 'Lateral 3-Light Bath Vanity', 'available': 46}, {'item': '10286CLSN', 'desc': 'Lateral 5-Light Chandelier', 'available': 45}, {'item': '10287CLBK', 'desc': 'Lateral 3-Light Chandelier', 'available': 43}, {'item': '10287SWSN', 'desc': 'Lateral 3-Light Chandelier', 'available': 43}, {'item': '10288CLSN', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 42}, {'item': '10287SWBK', 'desc': 'Lateral 3-Light Chandelier', 'available': 38}, {'item': '10286CLSBR', 'desc': 'Lateral 5-Light Chandelier', 'available': 34}, {'item': '10287CLSBR', 'desc': 'Lateral 3-Light Chandelier', 'available': 34}, {'item': '10287SWSBR', 'desc': 'Lateral 3-Light Chandelier', 'available': 33}, {'item': '10286CLBK', 'desc': 'Lateral 5-Light Chandelier', 'available': 31}, {'item': '10288CLBK', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 28}, {'item': '10285SWBK', 'desc': 'Lateral 5-Light Bath Vanity', 'available': 24}, {'item': '10288CLSBR', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 24}, {'item': '90281SWSBR', 'desc': 'Lateral Mini Pendant', 'available': 23}, {'item': '10286SWSBR', 'desc': 'Lateral 5-Light Chandelier', 'available': 15}, {'item': '10288SWSBR', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 10}, {'item': '10288SWBK', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 7}, {'item': '10288SWSN', 'desc': 'Lateral 4-Light Linear Pendant', 'available': 6}, {'item': '10281SWSBR', 'desc': 'Lateral 1-Light Bath Vanity', 'available': 3}] |
| 52102SN | Rail 24" LED Bath Vanity | RAIL | 228,969.07 | 5,666 | — | 2026-07-06 | [{'customer': 'J6 ENTERPRISES, LLC', 'revenue': 17801.45}, {'customer': 'LIGHTOLOGY', 'revenue': 15338.7}, {'customer': 'FERGUSON-CELINA, OH', 'revenue': 14683.2}, {'customer': 'GRAYBAR ELECTRIC CO.-SEATTLE, WA', 'revenue': 13892.45}, {'customer': 'REGENCY LIGHTING-KENNESAW, GA', 'revenue': 12493.26}, {'customer': 'FERGUSON-COXSACKIE, NY', 'revenue': 8740.0}, {'customer': 'WIEDENBACH-BROWN-USESI', 'revenue': 8458.0}, {'customer': 'FERGUSON-FRONT ROYAL, VA', 'revenue': 8171.9}, {'customer': 'LIGHTWISE-BOLIVAR, MO', 'revenue': 7479.3}, {'customer': 'ALL COUNTY ELECTRIC SUPPLY', 'revenue': 6578.0}, {'customer': 'FERGUSON-GRAND PRAIRIE, TX', 'revenue': 6555.0}, {'customer': 'FERGUSON-FORT PAYNE, AL', 'revenue': 6456.2}, {'customer': 'FERGUSON-RICHLAND, WA', 'revenue': 5549.9}, {'customer': 'FERGUSON-STOCKTON, CA', 'revenue': 5506.2}, {'customer': 'SEATTLE LIGHTING-SEATTLE', 'revenue': 5462.0}, {'customer': 'THE LIGHTING DESIGN-LAYTON, UT', 'revenue': 5362.5}, {'customer': 'VALUE LIGHTING-CARROLLTON, TX', 'revenue': 5332.0}, {'customer': 'CENTRAL ELECTRIC SUPPLY', 'revenue': 5135.25}, {'customer': 'FERGUSON-FROSTPROOF, FL', 'revenue': 4588.5}, {'customer': 'APCO, INC.', 'revenue': 3560.0}, {'customer': 'FERGUSON-WATERLOO, IA', 'revenue': 3539.7}, {'customer': 'FERGUSON- CHANDLER,AZ', 'revenue': 2927.9}, {'customer': 'VERMONT LIGHTING COMPANY', 'revenue': 2898.0}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 2890.0}, {'customer': 'FERGUSON-PERRIS, CA', 'revenue': 2753.1}, {'customer': 'LIGHT CONCERN', 'revenue': 2721.55}, {'customer': 'THE BRECHER CO.-LOUISVILLE', 'revenue': 2488.2}, {'customer': 'FERGUSON-BROOKSHIRE, TX', 'revenue': 2403.5}, {'customer': 'FERGUSON-KINGS MOUNTAIN, NC', 'revenue': 2272.4}, {'customer': 'MARCHAND ELECTRIC', 'revenue': 2254.0}, {'customer': 'FERGUSON-AURORA, CO', 'revenue': 2185.0}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 2022.25}, {'customer': 'WAREHOUSE-LIGHTING.COM', 'revenue': 1926.0}, {'customer': 'CED-BREMERTON, WA', 'revenue': 1840.0}, {'customer': 'FLUSHING LIGHTING FIXTURE CO.', 'revenue': 1798.0}, {'customer': 'WOLFE LIGHTING & ACCENTS', 'revenue': 1773.6}, {'customer': 'ELECTRICAL WHOLESALE DISTRIBUTORS', 'revenue': 1773.6}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 1334.0}, {'customer': 'FERGUSON-LEBANON, TN', 'revenue': 1311.0}, {'customer': 'NORTH COAST LIGHTING', 'revenue': 1294.92}, {'customer': 'FERGUSON-SECAUCUS, NJ', 'revenue': 1223.6}, {'customer': 'DECO LUMINAIRE', 'revenue': 1153.35}, {'customer': 'LOGIQ MODERN SUPPLY', 'revenue': 1035.0}, {'customer': 'DECOR LIGHTING-AUBURN', 'revenue': 1032.0}, {'customer': 'BAY LIGHTING', 'revenue': 920.0}, {'customer': 'RAINBOW LIGHTING', 'revenue': 557.4}, {'customer': 'FELDMAN BROTHERS ELECTRICAL', 'revenue': 552.0}, {'customer': 'M & M LIGHTING-HOUSTON', 'revenue': 552.0}, {'customer': 'CED-TWIN STATE-WILLISTON, VT', 'revenue': 552.0}, {'customer': 'OCEAN PACIFIC LIGHTING INC.', 'revenue': 552.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 480.6}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 441.15}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 414.0}, {'customer': 'AZTEC LIGHTING', 'revenue': 374.5}, {'customer': 'FERGUSON-SAN ANTONIO, TX', 'revenue': 349.6}, {'customer': 'PREMIER LIGHTING-PHOENIX, AZ', 'revenue': 349.6}, {'customer': 'WAYFAIR LLC', 'revenue': 322.8}, {'customer': 'LOWES COMPANIES', 'revenue': 278.18}, {'customer': 'VALUE LIGHTING, INC.', 'revenue': 276.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 234.9}, {'customer': 'THE OLDE PARSONAGE', 'revenue': 221.0}, {'customer': 'CED-EVERETT, WA', 'revenue': 215.0}, {'customer': 'LIGHTSTYLE', 'revenue': 215.0}, {'customer': 'LAMPS PLUS', 'revenue': 214.9}, {'customer': 'LUMINAIRE EXPERT', 'revenue': 209.7}, {'customer': 'WILLCALL FOR LIGHT CONCERN', 'revenue': 206.7}, {'customer': 'LONESTAR ELECTRIC-GRAND PRAIRIE, TX', 'revenue': 186.5}, {'customer': 'CONCEPT LUMINAIRE, INC.', 'revenue': 174.75}, {'customer': 'DECOR LIGHTING', 'revenue': 172.0}, {'customer': 'CLEVELAND LIGHTING ONE', 'revenue': 167.32}, {'customer': 'CARRINGTON LIGHTING.COM', 'revenue': 152.2}, {'customer': 'ELLIOTT ELECTRIC SUPPLY', 'revenue': 138.0}, {'customer': 'SOLTERRA LIGHTING', 'revenue': 138.0}, {'customer': 'CRESCENT LIGHTING SUPPLY-OLYMPIA,WA', 'revenue': 138.0}, {'customer': 'BUILDERS LIGHTING-BOISE', 'revenue': 138.0}, {'customer': 'BUILDER FINISH PRODUCTS', 'revenue': 129.0}, {'customer': 'PACE LIGHTING', 'revenue': 129.0}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 123.4}, {'customer': 'FERGUSON-SUMNER, WA', 'revenue': 110.91}, {'customer': "GARBE'S LIGHTING & HARDWARE", 'revenue': 104.85}, {'customer': 'WILLCALL FOR LIGHTSTYLES', 'revenue': 104.82}, {'customer': 'GROSS LIGHTING-TOLEDO, OH', 'revenue': 92.0}, {'customer': 'HOME CONCEPT', 'revenue': 92.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 92.0}, {'customer': "STAFFORD'S LIGHTING CO.,INC", 'revenue': 92.0}, {'customer': 'CONTINENTAL LIGHTING', 'revenue': 92.0}, {'customer': 'CENTRAL BUILDERS SUPPLY COURTENAY', 'revenue': 92.0}, {'customer': 'MUSKA LIGHTING CENTER-ROSEVILLE, MN', 'revenue': 92.0}, {'customer': 'STATEWIDE LIGHTING  INC.', 'revenue': 87.4}, {'customer': 'FERGUSON-LUBBOCK, TX', 'revenue': 87.4}, {'customer': 'FERGUSON-CALEDONIA, MI', 'revenue': 87.4}, {'customer': 'FERGUSON-HOLLY SPRINGS, NC', 'revenue': 87.4}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 87.4}, {'customer': 'LIGHTSTYLE OF TAMPA BAY', 'revenue': 82.8}, {'customer': 'FERGUSON-CLEVELAND, TN', 'revenue': 81.7}, {'customer': 'ALAMEDA ELECTRICAL DISTRIBUTORS', 'revenue': 73.1}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 71.94}, {'customer': 'BOUTIQUE LUMINAIRE PLUS-GRANBY', 'revenue': 69.9}, {'customer': 'TAZZ LIGHTING, INC.', 'revenue': 46.0}, {'customer': 'THE LIGHTING CORNER', 'revenue': 46.0}, {'customer': 'DHILLON LIGHTING INC.', 'revenue': 46.0}, {'customer': 'QED/GALLERIA LIGHTING-AURORA, CO', 'revenue': 46.0}, {'customer': 'STATE ELECTRIC-HUNTINGTON, WV', 'revenue': 46.0}, {'customer': 'RAINBOW LIGHTING', 'revenue': 46.0}, {'customer': 'COLONIAL ELECTRIC SUPPLY', 'revenue': 46.0}, {'customer': 'COAST LIGHTING', 'revenue': 46.0}, {'customer': 'CITY LIGHTS', 'revenue': 46.0}, {'customer': "AARON'S SUPPLY INC.-LITTLE RIVER", 'revenue': 46.0}, {'customer': 'CASA DI LUCE', 'revenue': 46.0}, {'customer': 'INLINE ELECTRIC SUPPLY-AUBURN', 'revenue': 46.0}, {'customer': 'LIGHTSTYLES', 'revenue': 43.7}, {'customer': 'PLUMBING DISTRIBUTORS-EATONTON', 'revenue': 43.0}, {'customer': 'HARDWOOD SPECIALTIES, INC.', 'revenue': 43.0}, {'customer': 'REDEFINED LIGHTING LLC.', 'revenue': 34.97}, {'customer': 'DECO LUMINAIRE', 'revenue': 34.95}, {'customer': 'LUPARELLO & SONS LIGHTING CORP.', 'revenue': 32.95}, {'customer': 'ROYAUME LUMINAIRE JD INC', 'revenue': 18.4}, {'customer': 'ROYAUME DU LUMINAIRE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE DRUMMONDVILE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE LANAUDIERE', 'revenue': 18.4}, {'customer': 'LUMINAIRES & CIE', 'revenue': 18.4}, {'customer': 'ROYAUME LUMINAIRE BEAUPORT', 'revenue': 18.4}, {'customer': 'ECLAIRAGE RAYMOND INC.', 'revenue': 5.0}, {'customer': 'WA BRAGG-EVANS, GA', 'revenue': 0.0}] | [{'item': '52102BK', 'desc': 'Rail 24" LED Bath Vanity', 'available': 2493}, {'item': '52102PC', 'desc': 'Rail 24" LED Bath Vanity', 'available': 1278}, {'item': '52103SN', 'desc': 'Rail 30" LED Bath Vanity', 'available': 796}, {'item': '52100PC', 'desc': 'Rail 18" LED Bath Vanity', 'available': 547}, {'item': '52104SN', 'desc': 'Rail 36" LED Bath Vanity', 'available': 310}, {'item': '52104PC', 'desc': 'Rail 36" LED Bath Vanity', 'available': 264}, {'item': '52104BK', 'desc': 'Rail 36" LED Bath Vanity', 'available': 215}, {'item': '52100SN', 'desc': 'Rail 18" LED Bath Vanity', 'available': 201}, {'item': '52100BK', 'desc': 'Rail 18" LED Bath Vanity', 'available': 198}, {'item': '52103PC', 'desc': 'Rail 30" LED Bath Vanity', 'available': 168}, {'item': '52105SN', 'desc': 'Rail 48" LED Bath Vanity', 'available': 83}, {'item': '52132SN', 'desc': 'Rail 24" LED Bath Bar CCT Select', 'available': 66}, {'item': '52105PC', 'desc': 'Rail 48" LED Bath Vanity', 'available': 36}, {'item': '52103BK', 'desc': 'Rail 30" LED Bath Vanity', 'available': 9}, {'item': '52105BK', 'desc': 'Rail 48" LED Bath Vanity', 'available': 1}] |
| 57933WTWT | Diverse 13" LED Flush Mount 3000K | COL7 | 132,527.70 | 6,314 | — | 2026-06-26 | [{'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 58452.85}, {'customer': 'LIFESTYLES', 'revenue': 10014.1}, {'customer': 'REXEL USA, INC.-TEMPLE, TX', 'revenue': 8000.0}, {'customer': 'FERGUSON-OMAHA, NE', 'revenue': 6277.5}, {'customer': 'TRINITY WHOLESALE DIST-NEW HAVEN', 'revenue': 6264.05}, {'customer': 'LIGHTING ETC, INC', 'revenue': 5266.92}, {'customer': 'GEORGIA LIGHTING', 'revenue': 4788.0}, {'customer': 'REID LIGHTING CO. INC.', 'revenue': 3925.8}, {'customer': 'LEGACY LIGHTING LLC', 'revenue': 3791.95}, {'customer': 'FERGUSON-LINCOLN, NE', 'revenue': 3123.6}, {'customer': 'THE LIGHTING DESIGN, LLC', 'revenue': 2431.28}, {'customer': 'AVID LIGHTING, LLC', 'revenue': 2041.26}, {'customer': 'FERGUSON-OKLAHOMA CITY, OK', 'revenue': 1830.4}, {'customer': 'CLEVELAND LIGHTING ONE', 'revenue': 1487.12}, {'customer': 'FERGUSON-OKLAHOMA, OK', 'revenue': 1482.0}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 1240.2}, {'customer': 'KENNEWICK IND/DBA KIE SUPPLY', 'revenue': 1164.41}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 1082.0}, {'customer': 'CITY ELECTRIC SUPPLY-GARDEN CITY,GA', 'revenue': 1037.5}, {'customer': "WILKINSON'S HOUSE OF LIGHTING", 'revenue': 884.0}, {'customer': 'COLONIAL LIGHTING-DECATUR, GA', 'revenue': 786.25}, {'customer': 'WINSUPPLY OF N ST. GEORGE UT CO.', 'revenue': 780.0}, {'customer': "HAGEN'S LIGHTING-TYLER", 'revenue': 754.0}, {'customer': 'LITECRAFT LIGHTING-AUGUSTA, GA', 'revenue': 553.5}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 520.0}, {'customer': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'revenue': 500.4}, {'customer': 'CITY ELECTRIC SUPPLY-STATESBORO, GA', 'revenue': 498.0}, {'customer': 'FERGUSON-NEW HUDSON, MI', 'revenue': 496.65}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 439.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 436.8}, {'customer': 'LIGHT WORKS', 'revenue': 312.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 260.0}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 221.35}, {'customer': 'HILL COUNTRY LIGHTING CENTER', 'revenue': 130.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 117.0}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 104.0}, {'customer': 'ECHO GROUP INC.-DES MOINES, IA', 'revenue': 104.0}, {'customer': 'COBURN SUPPLY COMPANY-MOBILE, AL', 'revenue': 104.0}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 101.25}, {'customer': 'GROSS LIGHTING-INDIANAPOLIS,IN', 'revenue': 78.0}, {'customer': "FERGUSON-O'FALLON, MO", 'revenue': 74.1}, {'customer': 'FERGUSON-TULSA, OK', 'revenue': 74.1}, {'customer': 'LIGHTING SOUTH, LLC-FAIRLAWN, OH', 'revenue': 65.85}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 65.85}, {'customer': 'PLUMBING DISTRIBUTORS-ALPHARETTA', 'revenue': 52.0}, {'customer': 'PLUMBING DISTRIBUTORS-EATONTON', 'revenue': 52.0}, {'customer': 'WILSON LIGHTING', 'revenue': 52.0}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 49.4}, {'customer': 'LAMPS PLUS', 'revenue': 43.16}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 26.0}, {'customer': 'MEDINA LIGHTING, INC.', 'revenue': 25.0}, {'customer': 'DENALI LIGHTING LLC', 'revenue': 25.0}, {'customer': 'FERGUSON-FRESNO, CA', 'revenue': 22.15}, {'customer': 'ELECTRICAL WHOLESALE DISTRIBUTORS', 'revenue': 19.95}] | [{'item': '87411WTWT', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 25682}, {'item': '87645WTWT', 'desc': 'Diverse 7.5" LED Flush Mount - 5CCT', 'available': 24210}, {'item': '87643WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 13554}, {'item': '57633WTWT', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 8871}, {'item': '57413WTWT', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 7411}, {'item': '87415WTWT', 'desc': 'Diverse 6" LED Flush Mount 5CCT', 'available': 5998}, {'item': '87642WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 2700K', 'available': 4195}, {'item': '87643WTBZ', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 3750}, {'item': '57641WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 2700K', 'available': 2541}, {'item': '57613WTSN', 'desc': 'Diverse 7.5" LED Flush Mount 3000K Non-T24', 'available': 1527}, {'item': '87643WTSN', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 1523}, {'item': '57933WTBK', 'desc': 'Diverse 13" LED Flush Mount 3000K', 'available': 858}, {'item': '57631WTWT', 'desc': 'Diverse 6.25" LED Flush Mount 2700K', 'available': 647}, {'item': '57935WTWT', 'desc': 'Diverse 13" LED Flush Mount 5CCT', 'available': 637}, {'item': '57414WTWT', 'desc': 'Diverse 6" LED Flush Mount 4000K', 'available': 630}, {'item': '57913WTBZ', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 465}, {'item': '57853WTWT', 'desc': 'Diverse 9" LED Flush Mount 4000K', 'available': 451}, {'item': '87643WTBK', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 430}, {'item': '57413WTBK', 'desc': 'Diverse 6" LED Flush Mount 3000K', 'available': 373}, {'item': '57647WTSN', 'desc': 'Diverse 7.5" LED Flush Mount 3000K', 'available': 352}, {'item': '57412WTWT', 'desc': 'Diverse 6" LED Flush Mount 2700K', 'available': 257}, {'item': '57935WTSN', 'desc': 'Diverse 13" LED Flush Mount 5CCT', 'available': 231}, {'item': '57932WTWT', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 219}, {'item': '57931WTBK', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 197}, {'item': '57923WTBK', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 194}, {'item': '57856WTWT', 'desc': 'Diverse 11" LED Flush Mount 2700K', 'available': 162}, {'item': '57858WTWT', 'desc': 'Diverse 11" LED Flush Mount 4000K', 'available': 150}, {'item': '57933WTSN', 'desc': 'Diverse 13" LED Flush Mount 3000K', 'available': 136}, {'item': '57861WTWT', 'desc': 'Diverse 13" LED Flush Mount 2700K', 'available': 135}, {'item': '57932WTBK', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 128}, {'item': '57933WTBZ', 'desc': 'Diverse 13" LED Flush Mount 3000K', 'available': 117}, {'item': '57925WTWT', 'desc': 'Diverse 11" LED Flush Mount 5CCT', 'available': 101}, {'item': '57925WTSN', 'desc': 'Diverse 11" LED Flush Mount 5CCT', 'available': 96}, {'item': '57915WTSN', 'desc': 'Diverse 9" LED Flush Mount 5CCT', 'available': 90}, {'item': '57923WTSN', 'desc': 'Diverse 11" LED Flush Mount 3000K', 'available': 86}, {'item': '57913WTSN', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 83}, {'item': '57863WTWT', 'desc': 'Diverse 13" LED Flush Mount 4000K', 'available': 49}, {'item': '57855WTWT', 'desc': 'Diverse 11" LED Flush Mount 3000K Non-T24', 'available': 48}, {'item': '57855WTSN', 'desc': 'Diverse 11" LED Flush Mount 3000K Non-T24', 'available': 48}, {'item': '87644WTWT', 'desc': 'Diverse 7.5" LED Flush Mount 4000K', 'available': 32}, {'item': '57851WTWT', 'desc': 'Diverse 9" LED Flush Mount 2700K', 'available': 20}, {'item': '57855WTBK', 'desc': 'Diverse 11" LED Flush Mount 3000K Non-T24', 'available': 2}, {'item': '57913WTBK', 'desc': 'Diverse 9" LED Flush Mount 3000K', 'available': 2}] |
| 88707BK | Falcon Pull Chain 52" In/Outdoor Fan w LED Light | COL196 | 117,033.23 | 1,107 | — | — | [{'customer': 'ALL-PHASE ELECTRIC (CED)-INDY, IN', 'revenue': 69363.43}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 29290.8}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 3449.55}, {'customer': 'BARROW LIGHTING SUPPLY', 'revenue': 3078.6}, {'customer': 'ILLUMINATE LIGHTING-LISBON, IA', 'revenue': 2186.8}, {'customer': 'THE LOCAL LIGHTING SHOP', 'revenue': 1595.3}, {'customer': 'LONESTAR ELECTRIC SUPPLY', 'revenue': 852.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 852.0}, {'customer': 'CAPITAL ELECTRIC-UPPER MARLBORO, MD', 'revenue': 852.0}, {'customer': 'SUMMIT ELECTRIC SUPPLY-PHOENIX, AZ', 'revenue': 675.0}, {'customer': 'TEAM ELECTRIC SUPPLY', 'revenue': 568.0}, {'customer': 'ELLIOTT ELECTRIC SUPPLY-SPRINGDALE', 'revenue': 540.0}, {'customer': 'PLUMBING DISTRIBUTORS-LAWRENCEVILLE', 'revenue': 540.0}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 344.85}, {'customer': 'DANLAR, INC.-USESI', 'revenue': 284.0}, {'customer': 'CLINE-HOLDER ELECTRIC SUPPLY', 'revenue': 284.0}, {'customer': 'HOME & LIGHT VALDOSTA', 'revenue': 270.5}, {'customer': 'LIGHT BRITE DISTRIBUTING-TRENTON', 'revenue': 261.09}, {'customer': 'CED ALL-PHASE ELECTRIC SUPPLY', 'revenue': 205.9}, {'customer': 'LEE SUPPLY CORP.-DAYTON, OH', 'revenue': 142.0}, {'customer': 'LIGHT & DAY', 'revenue': 142.0}, {'customer': 'LEE SUPPLY CORP.- FORT WAYNE, IN', 'revenue': 142.0}, {'customer': 'KNOXVILLE NOLAND CO.-KNOXVILLE, TN', 'revenue': 142.0}, {'customer': 'PLUMBING DISTRIBUTORS-ALPHARETTA', 'revenue': 135.0}, {'customer': 'BUILDERS LIGHTING & DESIGN, INC', 'revenue': 135.0}, {'customer': 'LAMPS.COM', 'revenue': 134.9}, {'customer': 'PARK LIGHTING', 'revenue': 121.5}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 120.7}, {'customer': 'LAMPS PLUS', 'revenue': 117.86}, {'customer': 'WALTERS WHOLESALE ELECTRIC-BREA', 'revenue': 106.5}, {'customer': 'SHOOK ELECTRICAL SUPPLY-CONYERS, GA', 'revenue': 99.95}, {'customer': 'ELFORD TEIBER & COMPANY', 'revenue': 0.0}] | [{'item': '88707SN', 'desc': 'Falcon Pull Chain 52" In/Outdoor Fan w LED Light', 'available': 636}] |
| 88708SN | Falcon AC Damp 52" In/Out Fan w LED Light Kit | COL198 | 101,340.37 | 771 | — | 2026-06-26 | [{'customer': 'MAYER ELECTRIC SUPPLY-GREENSBORO,NC', 'revenue': 91906.42}, {'customer': 'KING ELECTRIC CO.', 'revenue': 3598.5}, {'customer': 'HUNZICKER BROTHERS INC', 'revenue': 1395.0}, {'customer': 'DON DALTON COMPANY', 'revenue': 1059.5}, {'customer': 'KING ELECTRIC CO. INC.-BURLINGTON', 'revenue': 839.65}, {'customer': 'NORTHSIDE WAREHOUSE-TUCSON, AZ', 'revenue': 438.9}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 412.18}, {'customer': 'PARAMONT-EO INC.-CHICAGO', 'revenue': 308.0}, {'customer': 'LAMPS PLUS', 'revenue': 245.68}, {'customer': 'LONESTAR ELECTRIC SUPPLY-MANOR, TX', 'revenue': 154.0}, {'customer': 'THE LOCAL LIGHTING SHOP', 'revenue': 154.0}, {'customer': 'CRESCENT LIGHTING SUPPLY-OLYMPIA,WA', 'revenue': 154.0}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 146.3}, {'customer': 'UNION LIGHTING', 'revenue': 146.3}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 130.9}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 129.09}, {'customer': 'IMAGINE MORE', 'revenue': 121.95}] | — |
| 61018GS | Odeon 8-Light WiFi-enabled LED Fandelight | ODEON | 100,438.34 | 82 | — | 2026-06-19 | [{'customer': 'SHALLOTTE ELECTRIC & PLUMBING', 'revenue': 5396.0}, {'customer': 'VALLEY LIGHT GALLERY', 'revenue': 3642.3}, {'customer': 'LAMPS PLUS', 'revenue': 3156.66}, {'customer': 'LOWES COMPANIES', 'revenue': 3039.66}, {'customer': 'PREMIER LIGHTING', 'revenue': 2698.0}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 2347.26}, {'customer': 'GALLERIA LIGHTING', 'revenue': 2345.84}, {'customer': 'WAYFAIR LLC', 'revenue': 2178.64}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 1349.0}, {'customer': 'UNIVERSAL LIGHTS  INC.', 'revenue': 1349.0}, {'customer': 'ATLANTA CEILING FANS', 'revenue': 1349.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 1349.0}, {'customer': 'BULB BIN INC.', 'revenue': 1349.0}, {'customer': 'CAPE ELECTRIC-CAPE GIRARDEAU, MO', 'revenue': 1349.0}, {'customer': "CHRISTIE'S LIGHTING GALLERY", 'revenue': 1349.0}, {'customer': "BRADY'S DESIGN CENTER-LAWTON, OK", 'revenue': 1349.0}, {'customer': 'COMPLETE LIGHTING OF TAMPA', 'revenue': 1349.0}, {'customer': 'GLOBE LIGHTING COMPANY-PORTLAND', 'revenue': 1349.0}, {'customer': 'GRAND RAPIDS LIGHTING CENTER', 'revenue': 1349.0}, {'customer': 'GROSS LIGHTING-INDIANAPOLIS,IN', 'revenue': 1349.0}, {'customer': 'HERALD WHOLESALE  INC.', 'revenue': 1349.0}, {'customer': 'INLINE ELECTRIC SUPPLY-CHATTANOOGA', 'revenue': 1349.0}, {'customer': 'INLINE ELECTRIC SUPPLY-HUNTSVILLE', 'revenue': 1349.0}, {'customer': 'KENDALL ELECTRIC-FORT WAYNE, IN', 'revenue': 1349.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 1349.0}, {'customer': 'LIFESTYLES', 'revenue': 1349.0}, {'customer': 'LIGHTING STAR', 'revenue': 1349.0}, {'customer': 'LIGHTING ETC, INC', 'revenue': 1349.0}, {'customer': 'LYONS ELECTRIC SUPPLY', 'revenue': 1349.0}, {'customer': 'LYTEWORKS, INC.', 'revenue': 1349.0}, {'customer': 'MANTECA LIGHTING', 'revenue': 1349.0}, {'customer': 'MAYSON ENTERPRISE', 'revenue': 1349.0}, {'customer': 'PACE LIGHTING, INC.', 'revenue': 1349.0}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 1349.0}, {'customer': 'SISTERS LIGHTING', 'revenue': 1349.0}, {'customer': 'URBAN LIGHTS-DENVER, CO', 'revenue': 1349.0}, {'customer': 'VERSALLIES', 'revenue': 1349.0}, {'customer': 'VILLAGE HOME STORES, INC.', 'revenue': 1349.0}, {'customer': 'WEST COAST CABINETS CLOSETS & FLOOR', 'revenue': 1349.0}, {'customer': 'J&G ELECTRIC', 'revenue': 1349.0}, {'customer': 'UNION LIGHTING', 'revenue': 1281.55}, {'customer': 'BEAUTIFUL THINGS', 'revenue': 1281.55}, {'customer': 'IDLEWOOD ELECTRIC SUPPLY INC.', 'revenue': 1281.55}, {'customer': 'LBU LIGHTING PORT ST. LUCIE', 'revenue': 1281.55}, {'customer': 'FERGUSON-SHARONVILLE, OH', 'revenue': 1281.55}, {'customer': 'LIGHTING FIRST', 'revenue': 1281.55}, {'customer': 'LBU LIGHTING PINECREST', 'revenue': 1281.55}, {'customer': 'FERGUSON-ALPHARETTA, GA', 'revenue': 1281.55}, {'customer': 'FERGUSON-ROUND ROCK, TX', 'revenue': 1281.55}, {'customer': 'CLEVELAND LIGHTING ONE', 'revenue': 1268.06}, {'customer': 'LIGHTOLOGY', 'revenue': 1247.83}, {'customer': 'LIGHTSTYLE OF TAMPA BAY', 'revenue': 1214.1}, {'customer': 'LIGHT SOURCE LIGHTING', 'revenue': 1214.1}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 1214.1}, {'customer': 'FRANKLIN LIGHTING', 'revenue': 1214.1}, {'customer': 'LIGHTING, INC. OFFICE-HOUSTON', 'revenue': 1214.1}, {'customer': 'LIGHTING, INC. OFFICE-SAN ANTONIO', 'revenue': 1214.1}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 1214.1}, {'customer': "AARON'S SUPPLY INC.-LITTLE RIVER", 'revenue': 1199.09}, {'customer': 'HOBRECHT LIGHTING', 'revenue': 1199.09}, {'customer': 'NAPLES LIGHTING & FAN DEPOT INC.', 'revenue': 1199.09}, {'customer': 'PROGRESSIVE LIGHTING-ROSWELL, GA', 'revenue': 1187.12}, {'customer': 'GALLERIA LIGHTING', 'revenue': 1146.75}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 1146.65}, {'customer': 'LAMPS PLUS', 'revenue': 1119.67}, {'customer': 'CAPITOL LIGHTING-BOCA RATON', 'revenue': 1079.2}, {'customer': 'LIGHTING WORLD-STATEN ISLAND, NY', 'revenue': 640.78}, {'customer': 'LITTMAN BROTHERS', 'revenue': 0.0}, {'customer': 'MI CASA LIGHTING', 'revenue': 0.0}] | [{'item': '21866BCBK', 'desc': 'Odeon 6-Light Chandelier', 'available': 27}, {'item': '21869BCGS', 'desc': 'Odeon 10-Light Chandelier', 'available': 23}, {'item': '21866BCGS', 'desc': 'Odeon 6-Light Chandelier', 'available': 21}, {'item': '21869BCBK', 'desc': 'Odeon 10-Light Chandelier', 'available': 16}, {'item': '61018BK', 'desc': 'Odeon 8-Light WiFi-enabled LED Fandelight', 'available': 15}] |
| 12262CDBK | Acadia 2-Light Bath Vanity | COL8 | 98,559.11 | 3,377 | — | 2026-06-29 | [{'customer': 'HUBBARD PIPE & SUPPLY-CHARLOTTE, NC', 'revenue': 12415.68}, {'customer': 'CED-ALSTON ELECTRIC SUPPLY PC#5889', 'revenue': 8876.8}, {'customer': 'HUBBARD PIPE & SUPPLY-FAYETTEVILLE', 'revenue': 8478.3}, {'customer': 'COLONIAL LIGHTING-DECATUR, GA', 'revenue': 6259.75}, {'customer': 'COBURN SUPPLY COMPANY-MOBILE, AL', 'revenue': 4355.18}, {'customer': 'INLINE ELECTRIC SUPPLY-HUNTSVILLE', 'revenue': 3800.38}, {'customer': 'LONESTAR ELECTRIC SUPPLY-MANOR, TX', 'revenue': 3522.98}, {'customer': 'NORTH COAST LIGHTING-AUBURN, WA', 'revenue': 3297.0}, {'customer': 'WA BRAGG-WARNER ROBINS', 'revenue': 3134.62}, {'customer': 'PLUMBING DISTRIBUTORS-LAWRENCEVILLE', 'revenue': 2995.92}, {'customer': 'FERGUSON-LEBANON, TN', 'revenue': 2812.0}, {'customer': 'PDI-COVINGTON DC', 'revenue': 2385.64}, {'customer': 'HUBBARD PIPE & SUPPLY-WILMINGTON', 'revenue': 2299.2}, {'customer': 'PLUMBING DISTRIBUTORS-WOODSTOCK', 'revenue': 2286.94}, {'customer': 'HUBBARD PIPE & SUPPLY-GARNER, NC', 'revenue': 2239.2}, {'customer': 'ALL-PHASE ELECTRIC-GULFPORT, MS', 'revenue': 1914.06}, {'customer': 'RICHARDS LIGHTING', 'revenue': 1773.99}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 1741.96}, {'customer': 'INLINE ELECTRIC SUPPLY-PELHAM', 'revenue': 1692.14}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 1498.7}, {'customer': 'FROMM ELECTRIC', 'revenue': 1298.5}, {'customer': 'NORTH COAST LIGHTING-PORTLAND, OR', 'revenue': 1120.98}, {'customer': 'FERGUSON-GREENVILLE, SC', 'revenue': 1007.68}, {'customer': 'FERGUSON-RICHMOND, VA', 'revenue': 999.2}, {'customer': 'MATHES OF ALABAMA-DAPHNE', 'revenue': 998.64}, {'customer': 'HEARTH AND HOME, INC.', 'revenue': 898.5}, {'customer': 'THE HOME CENTER, INC', 'revenue': 875.3}, {'customer': 'AMERICAN LIGHTING', 'revenue': 873.1}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 723.75}, {'customer': 'ACTIVE ELECTRICAL SUPPLY CO.', 'revenue': 680.0}, {'customer': 'STOKES LIGHTING CENTER-KNOXVILLE', 'revenue': 599.0}, {'customer': 'COFFMAN HOME DECOR-ELKTON', 'revenue': 575.1}, {'customer': 'PLUMBING DISTRIBUTORS-MCDONOUGH', 'revenue': 554.8}, {'customer': 'LIGHTING CONCEPTS, LLC', 'revenue': 520.0}, {'customer': 'LEE SUPPLY CORP.', 'revenue': 459.84}, {'customer': 'TURNEY LIGHTING & ELECTRIC', 'revenue': 383.4}, {'customer': 'FERGUSON-LOUISVILLE, KY', 'revenue': 380.0}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 360.0}, {'customer': 'FERGUSON-INDIANAPOLIS, IN', 'revenue': 344.88}, {'customer': "SETH'S LIGHTING", 'revenue': 340.45}, {'customer': 'TALLAHASSEE LIGHTING & DECOR', 'revenue': 320.0}, {'customer': 'CAPITAL CITY DESIGN CENTER, INC.', 'revenue': 319.5}, {'customer': 'CAPITAL ELECTRIC-UPPER MARLBORO, MD', 'revenue': 280.0}, {'customer': 'KBL DESIGN CENTER, INC.', 'revenue': 266.0}, {'customer': 'SIGNATURE LIGHTING & FANS', 'revenue': 240.0}, {'customer': 'THE OLDE PARSONAGE', 'revenue': 240.0}, {'customer': 'AMERICAN LIGHTING-JOHNSON CITY', 'revenue': 204.42}, {'customer': 'FRANKLIN LIGHTING CENTER', 'revenue': 200.0}, {'customer': 'DEALERS LIGHTING-BRYAN, TX', 'revenue': 191.7}, {'customer': 'ROBINSON LIGHTING-PLYMOUTH, MN', 'revenue': 190.0}, {'customer': 'AMAZON PRIME ORDERS', 'revenue': 180.0}, {'customer': 'PLANK & TILE', 'revenue': 173.7}, {'customer': 'WINSUPPLY HENDERSONVILLE TN CO.', 'revenue': 160.0}, {'customer': 'YALE ELECTRIC-LANCASTER, PA', 'revenue': 160.0}, {'customer': 'MADISON LIGHTING LTD', 'revenue': 123.45}, {'customer': 'CROWN ELECTRIC SUPPLY-ONTARIO', 'revenue': 120.0}, {'customer': 'CITY ELECTRIC SUPPLY-YOUNG HARRIS', 'revenue': 120.0}, {'customer': 'THE BETTER LIVING STORE', 'revenue': 120.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 120.0}, {'customer': 'CARRINGTON LIGHTING.COM', 'revenue': 120.0}, {'customer': 'PC BUILDING MATERIALS, INC.', 'revenue': 120.0}, {'customer': 'FERGUSON-AURORA, CO', 'revenue': 114.0}, {'customer': 'TRINITY WHOLESALE DIST-NEW HAVEN', 'revenue': 103.9}, {'customer': 'LAMPS PLUS', 'revenue': 99.6}, {'customer': 'HANSEN LIGHTING, INC.-LINDON, UT', 'revenue': 98.85}, {'customer': 'BONAIRE LIGHTING SOLUTIONS', 'revenue': 95.85}, {'customer': 'LIGHTING ETC, INC', 'revenue': 88.05}, {'customer': 'BRIGHT CITY LIGHTS', 'revenue': 80.0}, {'customer': 'SPECTRUM LIGHTING', 'revenue': 80.0}, {'customer': 'MAGNOLIA LIGHTING-HERNANDO', 'revenue': 80.0}, {'customer': 'COASTAL LIGHTING LLC.', 'revenue': 80.0}, {'customer': 'J.D. LIGHTING', 'revenue': 80.0}, {'customer': 'PALMER ELECTRIC COMPANY', 'revenue': 76.14}, {'customer': 'FERGUSON-LUBBOCK, TX', 'revenue': 76.0}, {'customer': 'FERGUSON-MIDLOTHIAN, VA', 'revenue': 76.0}, {'customer': 'FERGUSON-BLACKSBURG, VA', 'revenue': 76.0}, {'customer': 'ONE SOURCE LIGHTING', 'revenue': 74.34}, {'customer': 'CITY LIGHTZ', 'revenue': 74.0}, {'customer': 'PROGRESSIVE LIGHTING-CHARLOTTE, NC', 'revenue': 70.4}, {'customer': 'PROGRESSIVE LIGHTING-ROSWELL, GA', 'revenue': 70.4}, {'customer': 'FERGUSON-METAIRIE, LA', 'revenue': 69.95}, {'customer': 'REXEL USA, INC.-ORLANDO, FL', 'revenue': 67.9}, {'customer': 'A&A LIGHTING LLC', 'revenue': 59.9}, {'customer': 'INLINE ELECTRIC SUPPLY-MONTGOMERY', 'revenue': 55.48}, {'customer': 'EAST COAST LUMBER BUILDING SUPPLY', 'revenue': 40.0}, {'customer': 'MAYER ELECTRIC SUPPLY-DOTHAN, AL', 'revenue': 40.0}, {'customer': 'MINNESOTA LTG. FIREPLACE & FLOORING', 'revenue': 40.0}, {'customer': 'GATEWAY LIGHTING & DESIGN INC.', 'revenue': 40.0}, {'customer': 'BOWLING GREEN WINLECTRIC CO.', 'revenue': 40.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 40.0}, {'customer': 'ALL-PHASE ELECTRIC-GRAND JUNCTION', 'revenue': 40.0}, {'customer': 'GRAHAM LIGHTING-MEMPHIS', 'revenue': 40.0}, {'customer': 'FERGUSON-PENSACOLA, FL', 'revenue': 38.0}, {'customer': 'MULTI LUMINAIRE', 'revenue': 38.0}, {'customer': 'THE LIGHTING SHOPPE', 'revenue': 38.0}, {'customer': 'FERGUSON-KNOXVILLE, TN', 'revenue': 38.0}, {'customer': 'RAY LIGHTING CENTER', 'revenue': 38.0}, {'customer': 'FERGUSON-TULSA, OK', 'revenue': 38.0}, {'customer': 'SUNBELT FANS & LIGHTING-LAFAYETTE', 'revenue': 38.0}, {'customer': 'UNION LIGHTING', 'revenue': 38.0}, {'customer': 'FERGUSON-MANDEVILLE, LA', 'revenue': 38.0}, {'customer': 'CONNECTICUT LIGHTING CENTE', 'revenue': 34.0}, {'customer': 'HOMESTYLES LIGHTING', 'revenue': 33.97}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 31.95}, {'customer': 'ALLOWAY LIGHTING', 'revenue': 30.95}, {'customer': 'THE LOCAL LIGHTING SHOP', 'revenue': 30.95}, {'customer': "DESIGNER'S MART", 'revenue': 30.85}, {'customer': 'SHOWCASE LIGHTING BY 3-G, LTD', 'revenue': 29.95}, {'customer': 'LOWES COMPANIES', 'revenue': 28.92}, {'customer': 'RITE RUG CO.-COLUMBUS, OH', 'revenue': 28.74}, {'customer': 'INLINE ELECTRIC SUPPLY-CLEVELAND,TN', 'revenue': 27.74}, {'customer': 'DANLAR, INC.-USESI-TUCKER, GA', 'revenue': 0.0}, {'customer': 'PLUMBING DISTRIBUTORS-SPARTANBURG', 'revenue': 0.0}] | [{'item': '12263CDSN', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 925}, {'item': '12263CDHR', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 796}, {'item': '12263CDBK', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 743}, {'item': '91260CDBK', 'desc': 'Acadia 1-Light Pendant', 'available': 364}, {'item': '12262CDSN', 'desc': 'Acadia 2-Light Bath Vanity', 'available': 360}, {'item': '12271CDBK', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 278}, {'item': '12273CDHR', 'desc': 'Acadia 3-Light Pendant', 'available': 222}, {'item': '12266CDBK', 'desc': 'Acadia 5-Light Chandelier', 'available': 201}, {'item': '12264CDSN', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 171}, {'item': '12273CDBK', 'desc': 'Acadia 3-Light Pendant', 'available': 164}, {'item': '12266CDHR', 'desc': 'Acadia 5-Light Chandelier', 'available': 117}, {'item': '91260CDNAB', 'desc': 'Acadia 1-Light Pendant', 'available': 99}, {'item': '91260CDHR', 'desc': 'Acadia 1-Light Pendant', 'available': 97}, {'item': '12264CDHR', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 96}, {'item': '12277CDSN', 'desc': 'Acadia 9-Light Chandelier', 'available': 85}, {'item': '12261CDBK', 'desc': 'Acadia 1-Light Wall Sconce', 'available': 78}, {'item': '12273CDNAB', 'desc': 'Acadia 3-Light Pendant', 'available': 75}, {'item': '12270CDNAB', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 75}, {'item': '12268CDNAB', 'desc': 'Acadia 8-Light Chandelier', 'available': 75}, {'item': '12261CDNAB', 'desc': 'Acadia 1-Light Wall Sconce', 'available': 75}, {'item': '12260CDNAB', 'desc': 'Acadia 3-Light Semi-Flush Mount/Chandelier', 'available': 75}, {'item': '12264CDNAB', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 73}, {'item': '12266CDSN', 'desc': 'Acadia 5-Light Chandelier', 'available': 73}, {'item': '12266CDNAB', 'desc': 'Acadia 5-Light Chandelier', 'available': 73}, {'item': '12277CDNAB', 'desc': 'Acadia 9-Light Chandelier', 'available': 72}, {'item': '12262CDNAB', 'desc': 'Acadia 2-Light Bath Vanity', 'available': 70}, {'item': '12271CDNAB', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 69}, {'item': '12263CDNAB', 'desc': 'Acadia 3-Light Bath Vanity', 'available': 59}, {'item': '12264CDBK', 'desc': 'Acadia 4-Light Bath Vanity', 'available': 58}, {'item': '12260CDSN', 'desc': 'Acadia 3-Light Semi-Flush Mount/Chandelier', 'available': 47}, {'item': '12271CDSN', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 36}, {'item': '12270CDSN', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 35}, {'item': '12270CDBK', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 35}, {'item': '12277CDBK', 'desc': 'Acadia 9-Light Chandelier', 'available': 30}, {'item': '12262CDHR', 'desc': 'Acadia 2-Light Bath Vanity', 'available': 28}, {'item': '12260CDBK', 'desc': 'Acadia 3-Light Semi-Flush Mount/Chandelier', 'available': 24}, {'item': '12268CDBK', 'desc': 'Acadia 8-Light Chandelier', 'available': 11}, {'item': '12270CDHR', 'desc': 'Acadia 1-Light Semi-Flush Mount', 'available': 10}, {'item': '12268CDSN', 'desc': 'Acadia 8-Light Chandelier', 'available': 9}, {'item': '12273CDSN', 'desc': 'Acadia 3-Light Pendant', 'available': 8}, {'item': '12268CDHR', 'desc': 'Acadia 8-Light Chandelier', 'available': 3}, {'item': '12271CDHR', 'desc': 'Acadia 3-Light Semi-Flush Mount', 'available': 3}] |
| E25052-CHK | Souffle 8.5" 1-Light Pendant | COL287 | 98,083.03 | 1,746 | — | 2026-06-19 | [{'customer': 'LUMISOLUTION INC.', 'revenue': 35421.58}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 14163.8}, {'customer': 'SOUTHERN LIGHTS,INC', 'revenue': 13087.61}, {'customer': 'LIGHTOLOGY', 'revenue': 5235.45}, {'customer': 'LUMENS LIGHT & LIVING', 'revenue': 4285.7}, {'customer': 'WAYFAIR LLC', 'revenue': 2091.96}, {'customer': 'TRANSIT LUMINAIRES', 'revenue': 1985.5}, {'customer': 'FUSION LIGHT & DESIGN', 'revenue': 1518.0}, {'customer': 'ESPACE LUMI DECOR INC.', 'revenue': 1382.0}, {'customer': 'JOSS AND MAIN-BOSTON', 'revenue': 1108.2}, {'customer': 'NORTHGLENN WINLECTRIC CO.', 'revenue': 990.0}, {'customer': 'DECO LUMINAIRE', 'revenue': 920.75}, {'customer': 'LUMINAIRES & CIE', 'revenue': 824.1}, {'customer': 'CASA DI LUCE', 'revenue': 770.1}, {'customer': 'NORBURN  LIGHTING & BATH-BURNABY', 'revenue': 671.5}, {'customer': 'PARK LIGHTING', 'revenue': 642.6}, {'customer': 'LAMPS PLUS', 'revenue': 592.04}, {'customer': 'CONCEPT LUMINAIRE, INC.', 'revenue': 568.3}, {'customer': 'LIGHTING ETC, INC', 'revenue': 528.0}, {'customer': 'UNION LIGHTING', 'revenue': 493.8}, {'customer': 'DECO LUMINAIRE', 'revenue': 473.4}, {'customer': 'DECO LUMINAIRE TERREBONNE', 'revenue': 454.55}, {'customer': 'POWER SHINE LIGHTING-BROOKLYN, NY', 'revenue': 446.0}, {'customer': 'CASA DI LUCE', 'revenue': 396.0}, {'customer': 'CRESCENT LIGHTING SUPPLY INC.', 'revenue': 384.0}, {'customer': 'LUMINAIRE REPENTIGNY', 'revenue': 381.5}, {'customer': 'LUMINAIRE ALDER INC.', 'revenue': 363.65}, {'customer': 'CITY LIGHTS', 'revenue': 330.0}, {'customer': 'MULTI LUMINAIRE', 'revenue': 318.5}, {'customer': 'LAMPS PLUS', 'revenue': 304.92}, {'customer': 'LAMPS.COM', 'revenue': 302.1}, {'customer': 'ROBINSON LIGHTING-WINNIPEG', 'revenue': 297.0}, {'customer': 'BOUTIQUE LUMINAIRE PLUS-GRANBY', 'revenue': 235.6}, {'customer': 'REXEL USA, INC. #989035', 'revenue': 232.5}, {'customer': 'LTG PROJECTS', 'revenue': 217.8}, {'customer': 'ROYAUME LUMINAIRE LANAUDIERE', 'revenue': 214.5}, {'customer': 'ROYAUME LUMINAIRE BEAUPORT', 'revenue': 203.1}, {'customer': 'ULTRA LIGHTING-MISSISSAUGA', 'revenue': 198.0}, {'customer': 'ELECTRIMAT-SAINT HUBERT, QC', 'revenue': 198.0}, {'customer': 'ECLAIRAGE RAYMOND INC.', 'revenue': 195.8}, {'customer': 'DULLES ELECTRIC & SUPPLY', 'revenue': 188.1}, {'customer': 'MULTI LUMINAIRE-QUEBEC', 'revenue': 188.1}, {'customer': 'THE LIGHT HOUSE', 'revenue': 186.0}, {'customer': 'ELM RIDGE LIGHTING & INTERIORS INC.', 'revenue': 178.2}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 178.2}, {'customer': 'SHADES OF LIGHT LLC', 'revenue': 176.88}, {'customer': 'ROBINSON LIGHTING-KELOWNA', 'revenue': 171.0}, {'customer': 'EDGES ELECTRICAL GROUP-SAN JOSE', 'revenue': 165.0}, {'customer': 'REDEFINED LIGHTING LLC.', 'revenue': 164.85}, {'customer': 'ECLAIRAGE ETC.', 'revenue': 155.85}, {'customer': "BEAULIEU DECOR D'ASTOUS ET FRERES", 'revenue': 146.85}, {'customer': 'LUMINAIRE EXPERT', 'revenue': 146.85}, {'customer': 'ROBINSON LIGHTING & BATH', 'revenue': 132.0}, {'customer': 'HYE LIGHTING', 'revenue': 132.0}, {'customer': 'PINE TREE LIGHTING-LAKE ORION', 'revenue': 132.0}, {'customer': 'RICHARDSON LIGHTING', 'revenue': 132.0}, {'customer': 'GADSDEN LIGHTING SHOWROOM INC.', 'revenue': 132.0}, {'customer': 'SYNERGY LIGHT STUDIO', 'revenue': 132.0}, {'customer': 'SUPERLITE', 'revenue': 132.0}, {'customer': 'LIGHTOPIA', 'revenue': 132.0}, {'customer': 'THE LIGHTING SHOPPE', 'revenue': 125.4}, {'customer': 'DHILLON LIGHTING CALGARY LTD.', 'revenue': 124.0}, {'customer': 'DESIGNER LIGHTING & FAN CENTER', 'revenue': 124.0}, {'customer': 'KENDALL ELECTRIC-FORT WAYNE, IN', 'revenue': 124.0}, {'customer': 'CARTWRIGHT LIGHTING', 'revenue': 118.8}, {'customer': 'ROYAUME LUMINAIRE-SAINT JULIE', 'revenue': 117.8}, {'customer': 'LIGHTING BY JARED, INC.', 'revenue': 114.84}, {'customer': 'THE LIGHTING WAREHOUSE', 'revenue': 111.6}, {'customer': 'LUMINAIRE NAPERT-ST. MARIE', 'revenue': 103.9}, {'customer': 'JANCO ELECTRIQUE', 'revenue': 103.9}, {'customer': 'STRUKTURA DESIGN INC.', 'revenue': 97.9}, {'customer': 'MASTERPIECE DISTRICT-ATLANTA', 'revenue': 92.4}, {'customer': 'ROYAUME DU LUMINAIRE', 'revenue': 82.5}, {'customer': 'UNION LIGHTING & FURNISHINGS', 'revenue': 62.7}, {'customer': 'ROYAUME LUMINAIRE DRUMMONDVILE', 'revenue': 26.4}, {'customer': 'PINE LIGHTING', 'revenue': 23.1}] | [{'item': 'E25050-CHK', 'desc': 'Souffle 10" LED Flush Mount', 'available': 817}, {'item': 'E25051-CHK', 'desc': 'Souffle 14" LED Flush Mount', 'available': 536}, {'item': 'E25050-TRC', 'desc': 'Souffle 10" LED Flush Mount', 'available': 318}, {'item': 'E25058-CHK', 'desc': 'Souffle 18" LED Flush Mount', 'available': 195}, {'item': 'E25058-TRC', 'desc': 'Souffle 18" LED Flush Mount', 'available': 168}, {'item': 'E25058-GY', 'desc': 'Souffle 18" LED Flush Mount', 'available': 143}, {'item': 'E25051-TRC', 'desc': 'Souffle 14" LED Flush Mount', 'available': 109}, {'item': 'E25059-TRC', 'desc': 'Souffle 22" LED Flush Mount', 'available': 88}, {'item': 'E25050-GY', 'desc': 'Souffle 10" LED Flush Mount', 'available': 88}, {'item': 'E25059-GY', 'desc': 'Souffle 22" LED Flush Mount', 'available': 86}, {'item': 'E25051-GY', 'desc': 'Souffle 14" LED Flush Mount', 'available': 57}, {'item': 'E25052-GY', 'desc': 'Souffle 8.5" 1-Light Pendant', 'available': 32}] |
