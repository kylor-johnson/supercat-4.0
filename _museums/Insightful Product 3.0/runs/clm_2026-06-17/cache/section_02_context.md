# Section 2 Context Bundle — Crystorama (clm)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=74342, portal_order_gmv=$40.3M |
| HAS_INVENTORY | True | inventory_count=1902 |
| HAS_SALES_DATA | True | sales_data_count=69099 |
| HAS_SALES_SECTION | True | qualifying_reps=5 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Catalog-Focused |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | crystorama_clm_ecat_online |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$40.3M > ecat_gmv=$551,721: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 5 | 5 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 100 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 165, Mixpanel total submit_order (Q-01): 2 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=90.0%, ambiguous_rate=0.0%, showroom_event_share=6.5% |
| USER_GROUP_JOIN_RATE | 90% | 90 of 100 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7% | showroom+admin share of matched events: 6.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Amit Sharma, Megan  Trosclair, HighPoint Showroom, Amit Sharma |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=-2685853 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2058 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=38 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Crystorama
- **Shortname**: clm
- **Org ID**: 64
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Crystorama (clm, org_id=64)
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

# Signal Rank — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Total signals fired**: 55 (P0: 43, P1: 12, P2: 0)
- **Org GMV**: $0.6M eCat LTM, $40.3M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders | P1 | §2 Accounts | 12.8 | $12,799,682 | 2.0 | 327,663,719 | POSITIVE |
| 2 | SIG-ANOMALY-02 | Stock Out — HAY-1417-AG (Hayes 50'' Aged Brass Linear Chandelier) $491,812 LTM, 0 available | P0 | §3 Product | 10.0 | $491,812 | 3.0 | 14,754,357 | RISK |
| 3 | SIG-ANOMALY-02 | Stock Out — ADD-317-AG-CL (Addis 51.75'' Aged Brass Linear Chandeli) $296,813 LTM, 0 available | P0 | §3 Product | 10.0 | $296,813 | 3.0 | 8,904,385 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — SHY-10907-SG (Shyla 24'' Soft Gold Chandelier) $292,247 LTM, 0 available | P0 | §3 Product | 10.0 | $292,247 | 3.0 | 8,767,410 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — ARA-10269-MK-ST (Aragon 58.75'' LED Matte Black Chandelie) $265,753 LTM, 0 available | P0 | §3 Product | 10.0 | $265,753 | 3.0 | 7,972,595 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 505-MT (Broche 16'' Matte White Semi Flush Mount) $230,169 LTM, 0 available | P0 | §3 Product | 10.0 | $230,169 | 3.0 | 6,905,072 | RISK |
| 7 | SIG-MOM-01 | Account Acceleration — Melrose & Madison CANADA ONLY (AMZ) 2 consecutive QoQ acceleration quarters, $744,929 peak quarter (+87% QoQ) | P0 | §2 Accounts | 2.9 | $744,929 | 3.0 | 6,465,987 | POSITIVE |
| 8 | SIG-ANOMALY-02 | Stock Out — ADD-317-AG-AU (Addis 51.75'' Aged Brass Linear Chandeli) $207,763 LTM, 0 available | P0 | §3 Product | 10.0 | $207,763 | 3.0 | 6,232,876 | RISK |
| 9 | SIG-COMMERCE-01 | Capture Rate — eCat captures 1.4% of $40M total business; each +1pt = $403K | P0 | §4 Commerce | 4.9 | $403,000 | 3.0 | 5,962,242 | POSITIVE |
| 10 | SIG-ANOMALY-02 | Stock Out — ADD-317-AG-AM (Addis 51.75'' Aged Brass Linear Chandeli) $188,094 LTM, 0 available | P0 | §3 Product | 10.0 | $188,094 | 3.0 | 5,642,824 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — ARC-1919-GA-CL-MWP (Arcadia 46.25'' Antique Gold Chandelier) $180,660 LTM, 0 available | P0 | §3 Product | 10.0 | $180,660 | 3.0 | 5,419,812 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — HAY-1409-PN (Hayes 40.5'' Polished Nickel Chandelier) $177,252 LTM, 0 available | P0 | §3 Product | 10.0 | $177,252 | 3.0 | 5,317,566 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — ADD-308-AG-WH (Addis 22'' Aged Brass Chandelier) $136,285 LTM, 0 available | P0 | §3 Product | 10.0 | $136,285 | 3.0 | 4,088,544 | RISK |
| 14 | SIG-ANOMALY-03 | Competitive Displacement — Cozy Development total biz +560% but eCat -100% | P0 | §2 Accounts | 44.0 | $23,584 | 3.0 | 3,110,693 | RISK |
| 15 | SIG-MOM-01 | Account Acceleration — Crystorama Accm 2 consecutive QoQ acceleration quarters, $61,836 peak quarter (+432% QoQ) | P0 | §2 Accounts | 14.4 | $61,836 | 3.0 | 2,673,161 | POSITIVE |
| 16 | SIG-DECAY-04 | Spending Contraction — Home Depot-ASN -54.9% YoY ($464,924→$209,744), $255,180 gap | P0 | §2 Accounts | 2.7 | $255,180 | 3.0 | 2,101,404 | RISK |
| 17 | SIG-MOM-01 | Account Acceleration — ShadesofLight 2 consecutive QoQ acceleration quarters, $381,645 peak quarter (+54% QoQ) | P0 | §2 Accounts | 1.8 | $381,645 | 3.0 | 2,064,698 | POSITIVE |
| 18 | SIG-MOM-01 | Account Acceleration — US Electrical Services, Inc.LA 2 consecutive QoQ acceleration quarters, $40,215 peak quarter (+233% QoQ) | P0 | §2 Accounts | 7.8 | $40,215 | 3.0 | 937,814 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — BBC Lighting Company 2 consecutive QoQ acceleration quarters, $62,520 peak quarter (+137% QoQ) | P0 | §2 Accounts | 4.6 | $62,520 | 3.0 | 855,902 | POSITIVE |
| 20 | SIG-DECAY-04 | Spending Contraction — Lamps.com -49.9% YoY ($209,278→$104,924), $104,354 gap | P0 | §2 Accounts | 2.5 | $104,354 | 3.0 | 781,088 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 32 | 1 | 0 | 33 | |
| §3 Product Intelligence | 10 | 0 | 0 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 10 | 0 | 10 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Melrose & Madison CANADA ONLY (AMZ) 2 consecutive QoQ acceleration quarters, $744,929 peak quarter (+87% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 1.4% of $40M total business; each +1pt = $403K
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Crystorama Accm 2 consecutive QoQ acceleration quarters, $61,836 peak quarter (+432% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — HAY-1417-AG (Hayes 50'' Aged Brass Linear Chandelier) $491,812 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — ADD-317-AG-CL (Addis 51.75'' Aged Brass Linear Chandeli) $296,813 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — SHY-10907-SG (Shyla 24'' Soft Gold Chandelier) $292,247 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | Overstock.com, Inc-Auto EDI | 2 | DECAY-04, MOM-01 | $63,288 |
| 2 | Armstrong Supply Co. | 2 | ANOMALY-03, MOM-01 | $30,822 |
| 3 | Home Depot-ASN | 1 | DECAY-04 | $255,180 |
| 4 | Lamps.com | 1 | DECAY-04 | $104,354 |
| 5 | Wayfair Perigold-Auto EDI | 1 | DECAY-04 | $63,432 |
| 6 | Home Sense | 1 | DECAY-04 | $56,994 |
| 7 | WAYFAIR - Birch Lane-Auto EDI | 1 | DECAY-04 | $47,997 |
| 8 | Urban Lights | 1 | DECAY-04 | $43,601 |
| 9 | Wilson Lighting of Naples | 1 | DECAY-04 | $40,286 |
| 10 | WAYFAIR-Joss&Main.com-Auto EDI | 1 | DECAY-04 | $40,031 |

### Q-12_results.md

# Q-12 Results — Crystorama (clm, org_id=64)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 4,815 | 611 | 114 | 91 | 16 |

### Q-14_results.md

# Q-14 Results — Crystorama (clm, org_id=64)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 11
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 544 | Lightstyle of Orlando | 7 | $19,163 | 2025-06-24 20:33:31 | 2026-01-21 14:09:46 | 35.10 |
| 30825 | Austell Lighting | 6 | $4,200 | 2025-07-07 20:17:54 | 2026-02-19 20:29:14 | 45.40 |
| 8091 | Beautiful Lights | 6 | $8,680 | 2025-11-17 19:30:46 | 2026-05-21 15:39:33 | 37 |
| 682 | Richards Lighting | 4 | $14,828 | 2026-02-16 19:27:09 | 2026-02-16 19:34:56 | 0 |
| 30311 | Mathes of Alabama Electric Supply Co., Inc. | 4 | $7,867 | 2026-01-23 21:42:39 | 2026-01-23 21:49:07 | 0 |
| 24743 | Enterprise Wholesale & Floorin | 3 | $2,545 | 2025-12-12 17:40:06 | 2026-03-30 23:13:35 | 54.10 |
| 992 | Lighting World Decorator | 3 | $12,496 | 2025-11-17 16:03:35 | 2026-01-27 16:30:54 | 35.50 |
| 2562 | Wage Lighting & Design | 3 | $20,334 | 2026-01-11 17:23:36 | 2026-01-11 17:23:36 | 0 |
| 30223 | Poonams by Design, LLC | 3 | $1,624 | 2025-07-11 16:01:47 | 2025-10-03 14:57:08 | 42 |
| 30980 | Surf Electrical Services | 3 | $11,960 | 2026-01-12 19:12:58 | 2026-01-26 21:06:17 | 7 |
| 7428 | Royal Lighting | 3 | $5,094 | 2025-06-27 20:41:58 | 2026-02-10 14:42:29 | 113.90 |

### Q-14b_results.md

# Q-14b Results — Crystorama (clm, org_id=64)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 319 | Ferguson Entrprises #2828 | 46 | 0.10 | 0.30 | 3 | $1.9M |
| 319 | Ferguson Entrprise-#571 | 20 | 0.10 | 0.50 | 5 | $1.9M |
| 319 | Ferguson Enterprises #48 - Wil | 85 | 0.10 | 0.20 | 2 | $1.9M |
| 319 | Ferguson Entrprise-Hampton#228 | 29 | 0.10 | 0.30 | 3 | $1.9M |
| 319 | Ferguson Enterprises #243 | 10 | 0.40 | 1 | 2.50 | $1.9M |
| 319 | Ferguson Enterprises #361 - Ro | 16 | 0.10 | 0.30 | 3 | $1.9M |
| 319 | Ferguson Enterprises #2812 | 94 | 0.10 | 0.20 | 2 | $1.9M |
| 319 | Ferguson #1983 | 19 | 0.10 | 0.30 | 3 | $1.9M |
| 319 | Ferguson Enterprises #320 - So | 72 | 0.10 | 0.20 | 2 | $1.9M |
| 319 | Ferguson Enterprises #101 - We | 17 | 0.10 | 0.30 | 3 | $1.9M |
| 319 | Ferguson Enterprises #215 - Le | 44 | 0.10 | 0.30 | 3 | $1.9M |
| 319 | Ferguson Enterprises #1551 - D | 16 | 0.10 | 0.50 | 5 | $1.9M |
| 319 | Ferguson Enterprises #34 - Cha | 82 | 0.20 | 0.30 | 1.50 | $1.9M |
| 319 | Ferguson Enterprises #2540  - | 22 | 0.20 | 0.30 | 1.50 | $1.9M |
| 4723 | Belami.com (1 Stop) - ASN | 5,830 | 0.10 | 129.90 | 1,299 | $1.6M |

### Q-17_results.md

# Q-17 Results — Crystorama (clm, org_id=64)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 12677 | Cregger Company, LLC | SC | 2026-01-11 21:20:27 | 2 | $22,820 |
| 2599 | Wiseway Supply | KY | 2026-02-05 17:14:57 | 2 | $20,690 |
| 2562 | Wage Lighting & Design | PA | 2026-01-11 17:23:36 | 3 | $20,334 |
| 368 | Graham's Lighting | TN | 2026-01-12 17:48:27 | 1 | $19,460 |
| 544 | Lightstyle of Orlando | FL | 2026-01-21 14:09:46 | 7 | $19,163 |
| 5311 | Home Lighting of Frazer | PA | 2026-02-05 21:50:20 | 1 | $16,602 |
| 682 | Richards Lighting | AL | 2026-02-16 19:34:56 | 4 | $14,828 |
| 537 | Lighting, Inc | TX | 2025-07-24 19:20:22 | 1 | $14,278 |
| 992 | Lighting World Decorator | NY | 2026-01-27 16:30:54 | 3 | $12,496 |
| 30784 | HUGHES SUPPLY HAJOCA CORPORATION | LA | 2026-01-11 15:34:08 | 1 | $12,179 |
| 30980 | Surf Electrical Services | NJ | 2026-01-26 21:06:17 | 3 | $11,960 |
| 13073 | Anthology Lighting | TX | 2026-01-20 19:11:44 | 2 | $10,988 |
| 11546 | Schaedler Yesco Distribution | PA | 2026-01-12 15:39:09 | 2 | $10,656 |
| 25620 | Greer Lighting Center | SC | 2026-01-12 21:32:49 | 1 | $9,944 |
| 11452 | Christies Lighting Gallery,LLC | NC | 2026-01-11 17:10:15 | 1 | $9,467 |
| 876 | Wilson Fans And Lighting | KS | 2026-01-10 21:05:53 | 1 | $8,812 |
| 10458 | Winsupply Owensboro KY Co | OH | 2026-01-12 17:51:37 | 1 | $8,780 |
| 30324 | Staggs Carpets & Interiors Inc. | MS | 2026-01-22 21:11:33 | 1 | $8,464 |
| 24874 | Notoco-Baton Rouge | LA | 2026-02-27 18:15:45 | 1 | $8,232 |
| 30470 | Made New Interiors and Decor, LLC | NC | 2026-01-13 18:53:47 | 1 | $8,196 |
| 30311 | Mathes of Alabama Electric Supply Co., Inc. | AL | 2026-01-23 21:49:07 | 4 | $7,867 |
| 428 | Jacobson Electric Service | IL | 2026-01-12 19:36:07 | 2 | $7,338 |
| 31313 | Wilhouse Designs | AL | 2025-10-26 11:46:27 | 1 | $6,356 |
| 5113 | Billows Electric Supply Co. | NJ | 2026-02-27 20:18:01 | 2 | $6,215 |
| 30618 | Illuminating Design LLC DBA A&J Investments | NJ | 2026-01-19 15:05:09 | 1 | $6,202 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Crystorama (clm, org_id=64)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 12677 | Cregger Company, LLC | SC | $22,820 | 2026-01-11 21:20:27 | 156 |
| 2599 | Wiseway Supply | KY | $20,690 | 2026-02-05 17:14:57 | 132 |
| 2562 | Wage Lighting & Design | PA | $20,334 | 2026-01-11 17:23:36 | 157 |
| 368 | Graham's Lighting | TN | $19,460 | 2026-01-12 17:48:27 | 156 |
| 544 | Lightstyle of Orlando | FL | $19,163 | 2026-01-21 14:09:46 | 147 |
| 5311 | Home Lighting of Frazer | PA | $16,602 | 2026-02-05 21:50:20 | 131 |
| 682 | Richards Lighting | AL | $14,828 | 2026-02-16 19:34:56 | 121 |
| 537 | Lighting, Inc | TX | $14,278 | 2025-07-24 19:20:22 | 328 |
| 992 | Lighting World Decorator | NY | $12,496 | 2026-01-27 16:30:54 | 141 |
| 30784 | HUGHES SUPPLY HAJOCA CORPORATION | LA | $12,179 | 2026-01-11 15:34:08 | 157 |
| 30980 | Surf Electrical Services | NJ | $11,960 | 2026-01-26 21:06:17 | 141 |
| 13073 | Anthology Lighting | TX | $10,988 | 2026-01-20 19:11:44 | 148 |
| 11546 | Schaedler Yesco Distribution | PA | $10,656 | 2026-01-12 15:39:09 | 156 |
| 25620 | Greer Lighting Center | SC | $9,944 | 2026-01-12 21:32:49 | 155 |
| 11452 | Christies Lighting Gallery,LLC | NC | $9,467 | 2026-01-11 17:10:15 | 157 |
| 876 | Wilson Fans And Lighting | KS | $8,812 | 2026-01-10 21:05:53 | 157 |
| 10458 | Winsupply Owensboro KY Co | OH | $8,780 | 2026-01-12 17:51:37 | 156 |
| 30324 | Staggs Carpets & Interiors Inc. | MS | $8,464 | 2026-01-22 21:11:33 | 145 |
| 24874 | Notoco-Baton Rouge | LA | $8,232 | 2026-02-27 18:15:45 | 110 |
| 30470 | Made New Interiors and Decor, LLC | NC | $8,196 | 2026-01-13 18:53:47 | 155 |

### Q-40_results.md

# Q-40 Results — Crystorama (clm, org_id=64)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| LA | 13 | 13 | $56,434 |
| PA | 5 | 10 | $56,133 |
| AL | 12 | 27 | $45,496 |
| FL | 11 | 24 | $39,925 |
| SC | 4 | 5 | $39,550 |
| TX | 6 | 7 | $36,910 |
| GA | 9 | 9 | $36,398 |
| ON | 12 | 14 | $32,058 |
| NC | 5 | 5 | $28,787 |
| TN | 2 | 2 | $24,676 |
| NJ | 3 | 6 | $24,376 |
| KY | 1 | 2 | $20,690 |
| NY | 2 | 4 | $15,858 |
| IL | 3 | 4 | $14,214 |
| AB | 3 | 4 | $12,664 |
| MS | 2 | 2 | $12,396 |
| OH | 2 | 2 | $10,813 |
| AR | 4 | 4 | $10,101 |
| KS | 1 | 1 | $8,812 |
| CO | 3 | 6 | $7,019 |

### Q-41_results.md

# Q-41 Results — Crystorama (clm, org_id=64)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 13
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 2 |
| 2025-04-01 | Rep-Acquired (iPad) | 2 |
| 2025-05-01 | Rep-Acquired (iPad) | 2 |
| 2025-07-01 | Rep-Acquired (iPad) | 3 |
| 2025-08-01 | Rep-Acquired (iPad) | 1 |
| 2025-10-01 | Rep-Acquired (iPad) | 3 |
| 2025-11-01 | Rep-Acquired (iPad) | 3 |
| 2025-12-01 | Rep-Acquired (iPad) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 20 |
| 2026-02-01 | Rep-Acquired (iPad) | 8 |
| 2026-03-01 | Rep-Acquired (iPad) | 5 |
| 2026-04-01 | Rep-Acquired (iPad) | 1 |
| 2026-05-01 | Rep-Acquired (iPad) | 2 |

### Q-41_rep_results.md

# Q-41-rep Results — Crystorama (clm, org_id=64)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 23
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Katy McCully | 9 |
| Jeff Nicholson | 8 |
| Cindy Rogers | 4 |
| Zachary Rapp | 4 |
| Megan  Trosclair | 4 |
| Brad Dobson | 3 |
| Vince  Hall | 3 |
| Steve Linder | 2 |
| Kevin  Taylor | 2 |
| Matt Sullivan | 1 |
| Mike Hemsarth | 1 |
| Pauline Theos | 1 |
| Shelly Orban | 1 |
| Steve Jones | 1 |
| Kelly York | 1 |
| Chas Lassoff | 1 |
| Cindy Vackar | 1 |
| Eric Manzo | 1 |
| Forrest Denbow | 1 |
| Gary Ellis | 1 |
| HighPoint Showroom | 1 |
| Amy Matteson | 1 |
| Kristen Cavanagh | 1 |

### Q-52_results.md

# Q-52 Results — Crystorama (clm, org_id=64)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 463 | Lamps Plus.com-Auto ASN | CA | 8,352 | $2.6M | 0 | $0 | 0 |
| 7342 | Build Drop Ship EDI | CA | 5,442 | $2.2M | 0 | $0 | 0 |
| 7127 | Lighting New York-Auto EDI | PA | 4,245 | $2.0M | 0 | $0 | 0 |
| 4723 | Belami.com (1 Stop) - ASN | - null - | 4,129 | $1.6M | 0 | $0 | 0 |
| 11861 | Y Design/Lumens, Inc.com-ASN | CA | 3,130 | $1.3M | 0 | $0 | 0 |
| 704 | ShadesofLight | VA | 251 | $1.2M | 0 | $0 | 0 |
| 7044 | Wayfair.com-Auto EDI | MA | 3,719 | $896,751 | 0 | $0 | 0 |
| 9395 | Capitol Lighting-Dropship-ASN | FL | 1,529 | $679,474 | 0 | $0 | 0 |
| 12867 | Foundrylighting.com | NY | 1,827 | $633,580 | 0 | $0 | 0 |
| 24260 | Wayfair-B2B-Auto EDI | MA | 1,617 | $537,197 | 0 | $0 | 0 |
| 463 | Lamps Plus.com-Auto ASN B2B Orders | CA | 1,124 | $459,716 | 0 | $0 | 0 |
| 12052 | Haus Appeal LLC | MA | 1,436 | $368,525 | 0 | $0 | 0 |
| 11714 | Lightology, LLC.com | IL | 481 | $348,120 | 0 | $0 | 0 |
| 168 | Elements | NY | 401 | $324,032 | 0 | $0 | 0 |
| 12167 | Lightopia, LLC. | CA | 699 | $285,657 | 0 | $0 | 0 |
| 24817 | Lowes Companies , Inc | NC | 818 | $267,621 | 0 | $0 | 0 |
| 31018 | Ambient Lighting DBA Lights.com | NY | 716 | $260,972 | 0 | $0 | 0 |
| 723 | Southern Lights | MN | 149 | $252,257 | 0 | $0 | 0 |
| 12644 | Home Depot-ASN | GA | 695 | $209,744 | 0 | $0 | 0 |
| 7044 | Wayfair-B2B-Auto EDI | MA | 628 | $204,461 | 0 | $0 | 0 |
| 25207 | Melrose & Madison (AMZ) | TX | 428 | $195,638 | 0 | $0 | 0 |
| 53 | BBC Lighting Company | WI | 111 | $182,175 | 0 | $0 | 0 |
| 25207 | Melrose & Madison (AMZ) | FL | 411 | $173,268 | 0 | $0 | 0 |
| 319 | Ferguson Entrprises #452 | - null - | 130 | $164,386 | 0 | $0 | 0 |
| 1938 | Plumbing Distributors Inc. | GA | 152 | $157,423 | 0 | $0 | 0 |
| 414 | Idlewood Electric Supply | IL | 136 | $157,219 | 0 | $0 | 0 |
| 278 | Dominion Electric - Westfax | VA | 107 | $156,736 | 0 | $0 | 0 |
| 30862 | Daniel House Club | OR | 206 | $134,853 | 0 | $0 | 0 |
| 12764 | WAYFAIR - Birch Lane-Auto EDI | MA | 594 | $130,198 | 0 | $0 | 0 |
| 1628 | Crystorama Accm | NY | 779 | $126,900 | 0 | $0 | 0 |

### Q-53_results.md

# Q-53 Results — Crystorama (clm, org_id=64)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 7342 | Build Drop Ship EDI | CA | 5,442 | $2.2M |
| 7127 | Lighting New York-Auto EDI | PA | 4,245 | $2.0M |
| 4723 | Belami.com (1 Stop) - ASN | - null - | 4,129 | $1.6M |
| 11861 | Y Design/Lumens, Inc.com-ASN | CA | 3,130 | $1.3M |
| 7044 | Wayfair.com-Auto EDI | MA | 3,719 | $896,751 |
| 9395 | Capitol Lighting-Dropship-ASN | FL | 1,529 | $679,474 |
| 12867 | Foundrylighting.com | NY | 1,827 | $633,580 |
| 24260 | Wayfair-B2B-Auto EDI | MA | 1,617 | $537,197 |
| 12052 | Haus Appeal LLC | MA | 1,436 | $368,525 |
| 11714 | Lightology, LLC.com | IL | 481 | $348,120 |
| 168 | Elements | NY | 401 | $324,032 |
| 12167 | Lightopia, LLC. | CA | 699 | $285,657 |
| 24817 | Lowes Companies , Inc | NC | 818 | $267,621 |
| 31018 | Ambient Lighting DBA Lights.com | NY | 716 | $260,972 |
| 12644 | Home Depot-ASN | GA | 695 | $209,744 |
| 7044 | Wayfair-B2B-Auto EDI | MA | 628 | $204,461 |
| 25207 | Melrose & Madison (AMZ) | TX | 428 | $195,638 |
| 25207 | Melrose & Madison (AMZ) | FL | 411 | $173,268 |
| 1938 | Plumbing Distributors Inc. | GA | 152 | $157,423 |
| 414 | Idlewood Electric Supply | IL | 136 | $157,219 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Crystorama (clm, org_id=64)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CA | 122 | 20,270 | $7.7M | 0 | 0 | $0 | 0 |
| - null - | 12 | 6,933 | $3.5M | 0 | 0 | $0 | 0 |
| MA | 65 | 10,334 | $3.0M | 1 | 1 | $3,338 | 0.10 |
| FL | 186 | 4,068 | $2.8M | 11 | 24 | $39,925 | 1.40 |
| PA | 78 | 5,331 | $2.7M | 5 | 10 | $56,133 | 2.10 |
| NY | 124 | 5,286 | $2.5M | 2 | 4 | $15,858 | 0.60 |
| VA | 68 | 1,042 | $1.8M | 0 | 0 | $0 | 0 |
| TX | 134 | 2,053 | $1.8M | 6 | 7 | $36,910 | 2 |
| GA | 78 | 2,168 | $1.6M | 9 | 9 | $36,398 | 2.30 |
| IL | 67 | 1,804 | $1.4M | 3 | 4 | $14,214 | 1 |
| NC | 128 | 2,099 | $1.3M | 5 | 5 | $28,787 | 2.20 |
| NJ | 116 | 985 | $776,283 | 3 | 6 | $24,376 | 3.10 |
| OH | 73 | 804 | $678,216 | 2 | 2 | $10,813 | 1.60 |
| LA | 48 | 712 | $655,995 | 13 | 13 | $56,434 | 8.60 |
| SC | 75 | 795 | $641,398 | 4 | 5 | $39,550 | 6.20 |
| MI | 46 | 631 | $474,607 | 0 | 0 | $0 | 0 |
| TN | 53 | 523 | $456,922 | 2 | 2 | $24,676 | 5.40 |
| MN | 31 | 466 | $453,293 | 0 | 0 | $0 | 0 |
| WI | 16 | 369 | $410,251 | 0 | 0 | $0 | 0 |
| MO | 28 | 486 | $396,029 | 0 | 0 | $0 | 0 |

### Q-57_results.md

# Q-57 Results — Crystorama (clm, org_id=64)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Crystorama (clm, org_id=64)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TX | $913,537 | $1.1M | 17.50 | 140 | 131 | 9 | 1,755 |
| FL | $928,535 | $1.1M | 14.60 | 165 | 154 | 11 | 1,779 |
| NC | $541,566 | $705,964 | 30.40 | 120 | 120 | 0 | 1,110 |
| VA | $642,786 | $689,013 | 7.20 | 62 | 73 | -11 | 698 |
| CA | $481,315 | $623,644 | 29.60 | 99 | 93 | 6 | 1,367 |
| NY | $568,382 | $604,653 | 6.40 | 106 | 114 | -8 | 1,233 |
| GA | $488,543 | $512,217 | 4.80 | 85 | 82 | 3 | 930 |
| NJ | $432,308 | $495,827 | 14.70 | 104 | 104 | 0 | 937 |
| TN | $308,048 | $444,775 | 44.40 | 66 | 60 | 6 | 692 |
| IL | $396,481 | $405,142 | 2.20 | 73 | 81 | -8 | 772 |
| SC | $301,532 | $344,741 | 14.30 | 84 | 91 | -7 | 600 |
| PA | $288,968 | $340,109 | 17.70 | 84 | 74 | 10 | 695 |
| OH | $321,911 | $282,590 | -12.20 | 78 | 74 | 4 | 521 |
| MA | $207,555 | $274,358 | 32.20 | 77 | 67 | 10 | 649 |
| LA | $251,691 | $259,186 | 3 | 66 | 62 | 4 | 381 |
| MI | $214,731 | $228,967 | 6.60 | 60 | 57 | 3 | 478 |
| MN | $170,894 | $225,178 | 31.80 | 43 | 36 | 7 | 314 |
| MO | $171,432 | $181,318 | 5.80 | 41 | 45 | -4 | 293 |
| AL | $177,394 | $179,068 | 0.90 | 46 | 51 | -5 | 342 |
| WI | $164,798 | $176,361 | 7 | 36 | 40 | -4 | 264 |
| AZ | $141,339 | $164,259 | 16.20 | 40 | 51 | -11 | 304 |
| IN | $120,900 | $159,988 | 32.30 | 58 | 52 | 6 | 310 |
| KY | $141,974 | $151,947 | 7 | 35 | 47 | -12 | 283 |
| CT | $124,206 | $144,107 | 16 | 44 | 43 | 1 | 372 |
| CO | $143,599 | $139,868 | -2.60 | 43 | 51 | -8 | 275 |

### Q-68_results.md

# Q-68 Results — Crystorama (clm, org_id=64)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
| Shades of Light ** | VA | $10,294 | $48,273 | $37,979 | 21.30 | 3 |
| Light Bulbs Unlimited | MI | $39,695 | $73,456 | $33,761 | 54 | 12 |
| Illuminations Lighting Inc. | OK | $23,010 | $55,153 | $32,143 | 41.70 | 10 |
| ABC Creations | TX | $14,136 | $45,957 | $31,821 | 30.80 | 7 |
| Modern Lighting | CA | $9,990 | $41,560 | $31,570 | 24 | 11 |
| Lighting Resource Studio | MI | $8,177 | $38,393 | $30,216 | 21.30 | 10 |
| Cardello Electric Supply | WV | $80,817 | $109,790 | $28,973 | 73.60 | 13 |
| Indiana Lighting Center, Inc. | IN | $7,927 | $36,467 | $28,540 | 21.70 | 6 |
| Watts Current Inc. | ON | $11,684 | $38,986 | $27,302 | 30 | 8 |
| Morgan Stuart Logistics | NY | $29,694 | $53,873 | $24,179 | 55.10 | 10 |
| Union Lighting & Furnishings | ON | $63,901 | $87,405 | $23,503 | 73.10 | 13 |
| Elaine Everett's Lighting | TX | $34,339 | $57,525 | $23,186 | 59.70 | 13 |
| Nova Lighting | UT | $5,344 | $26,696 | $21,352 | 20 | 7 |
| Curb Ease, LLC dba Fixture This | TX | $20,022 | $40,843 | $20,821 | 49 | 13 |
| Texture BR, LLC | MS | $9,877 | $30,606 | $20,729 | 32.30 | 7 |
| LyteWorks | MD | $29,886 | $49,611 | $19,724 | 60.20 | 12 |
| Custom Lighting | IL | $15,905 | $34,798 | $18,893 | 45.70 | 8 |
| Lando Lighting | ON | $11,617 | $30,099 | $18,482 | 38.60 | 5 |
| Interiors By Sabrina | NY | $1,946 | $20,386 | $18,440 | 9.50 | 1 |
| Royce Collection Inc. | MI | $43,201 | $61,069 | $17,868 | 70.70 | 8 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 22285 | Wayfair Perigold-Auto EDI | 517-GA_CEILING | Broche 6 Light Antique Gold Semi Flush Mount | 66 | 6 | 149 | 24.80 | 14,909.67 | DECAY_DETECTED |
| 12052 | Haus Appeal LLC | 531-GA | Broche 6'' Antique Gold Sconce | 110 | 4 | 78 | 19.50 | 18,418.95 | DECAY_DETECTED |
| 24260 | Wayfair-B2B-Auto EDI | 517-GA_CEILING | Broche 6 Light Antique Gold Semi Flush Mount | 57 | 5.70 | 218 | 38.20 | 8,958.60 | DECAY_DETECTED |
| 25207 | Melrose & Madison (AMZ) | 710-OB-CL-I | Waltham 2 Light Clear Italian Crystal Olde Brass Flush Mount | 144 | 3.50 | 35 | 10 | 21,216.51 | DECAY_DETECTED |
| 12167 | Lightopia, LLC. | 533-CT | Broche 6 Light Champagne Green Tea Chandelier | 25 | 9.30 | 244 | 26.20 | 7,240.49 | DECAY_DETECTED |
| 704 | ShadesofLight | 531-SA | Broche 6'' Antique Silver Sconce | 17 | 11.80 | 316 | 26.80 | 6,593.40 | DECAY_DETECTED |
| 12764 | WAYFAIR - Birch Lane-Auto EDI | 712-OB-CL-I | Waltham 3 Light Clear Italian Crystal Olde Brass Flush Mount | 47 | 9.10 | 104 | 11.40 | 11,218.95 | DECAY_DETECTED |
| 24260 | Wayfair-B2B-Auto EDI | ADD-300-AG-AM_CEILING | Addis 4 Light Aged Brass Semi Flush Mount | 35 | 11.80 | 108 | 9.20 | 13,173.66 | DECAY_DETECTED |
| 4723 | Belami.com (1 Stop) - ASN | 517-GA_CEILING | Broche 6 Light Antique Gold Semi Flush Mount | 88 | 5.90 | 19 | 3.20 | 29,335.86 | DECAY_DETECTED |
| 11861 | Y Design/Lumens, Inc.com-ASN | 531-GA | Broche 6'' Antique Gold Sconce | 124 | 4.20 | 21 | 5 | 18,245.70 | DECAY_DETECTED |
| 463 | LampsPlus#63 | 3025-EB-CL-MWP | Butler 5 Light Hand Cut Crystal English Bronze Chandelier | 55 | 7.70 | 87 | 11.30 | 7,049.60 | DECAY_DETECTED |
| 7342 | Build Drop Ship EDI | HAY-1407-AG | Hayes 28'' Aged Brass Chandelier | 24 | 18 | 95 | 5.30 | 14,865.12 | DECAY_DETECTED |
| 12052 | Haus Appeal LLC | XAV-B9315-VG-BL | Xavier 5 Light Vibrant Gold + Blue Chandelier | 29 | 10.90 | 166 | 15.20 | 5,149.32 | DECAY_DETECTED |
| 24260 | Wayfair-B2B-Auto EDI | XAV-B8301-VG | Xavier 12'' Vibrant Gold Pendant | 43 | 9.80 | 105 | 10.70 | 6,415.40 | DECAY_DETECTED |
| 12052 | Haus Appeal LLC | 566-CT | Broche 5 Light Champagne Green Tea Chandelier | 11 | 11.40 | 133 | 11.70 | 5,739.85 | DECAY_DETECTED |
| 25207 | Melrose & Madison CANADA ONLY (AMZ) | 7404-BU | Norwalk 4 Light Bronze Umber Mini Chandelier | 64 | 7.80 | 43 | 5.50 | 12,129.18 | DECAY_DETECTED |
| 11861 | Y Design/Lumens, Inc.com-ASN | ADD-317-AG-CL | Addis 51.75'' Aged Brass Linear Chandelier | 9 | 27.70 | 160 | 5.80 | 11,106.45 | DECAY_DETECTED |
| 704 | ShadesofLight | FUL-905-PN | Fulton 3 Light Polished Nickel Semi Flush Mount | 5 | 53.20 | 233 | 4.40 | 14,580 | DECAY_DETECTED |
| 24260 | Wayfair-B2B-Auto EDI | 501-GA | Broche 8.5'' Antique Gold Sconce | 45 | 9.80 | 104 | 10.60 | 5,987.34 | DECAY_DETECTED |
| 22285 | Wayfair Perigold-Auto EDI | 519-GA_CEILING | Broche 8 Light Antique Gold Semi Flush Mount | 20 | 19.10 | 163 | 8.50 | 6,920.10 | DECAY_DETECTED |
| 319 | Ferguson Entrprises #452 | ARC-1917-GA-CL-MWP | Arcadia 24'' Antique Gold Chandelier | 5 | 10.40 | 104 | 10 | 5,878.02 | DECAY_DETECTED |
| 12167 | Lightopia, LLC. | 568-GA | Broche 6 Light Antique Gold Chandelier | 37 | 11.20 | 75 | 6.70 | 8,737.86 | DECAY_DETECTED |
| 4723 | Belami.com (1 Stop) - ASN | 505-MT | Broche 4 Light Matte White Semi Flush Mount | 76 | 6.40 | 22 | 3.40 | 16,510 | DECAY_DETECTED |
| 463 | LampsPlus#61 | HAY-1407-PN | Hayes 28'' Polished Nickel Chandelier | 26 | 16.30 | 62 | 3.80 | 14,585.40 | DECAY_DETECTED |
| 47 | Progressive Lighting Inc. | ZAN-9006-SG | Zanzibar 6 Light Soft Gold Pendant | 17 | 22.20 | 139 | 6.30 | 8,579.70 | DECAY_DETECTED |
| 24260 | Wayfair-B2B-Auto EDI | 566-MT | Broche 5 Light Matte White Chandelier | 24 | 14.80 | 103 | 7 | 7,216.48 | DECAY_DETECTED |
| 7342 | Build Drop Ship EDI | 7409-BU | Norwalk 9 Light Bronze Umber Chandelier | 16 | 17.60 | 119 | 6.80 | 7,051.17 | DECAY_DETECTED |
| 7127 | Lighting New York-Auto EDI | 517-GA_CEILING | Broche 6 Light Antique Gold Semi Flush Mount | 40 | 12 | 50 | 4.20 | 11,220.76 | DECAY_DETECTED |
| 24260 | Wayfair-B2B-Auto EDI | 531-GA | Broche 6'' Antique Gold Sconce | 34 | 11.70 | 104 | 8.90 | 5,252.55 | DECAY_DETECTED |
| 7342 | Build Drop Ship EDI | HAY-1417-AG | Hayes 50'' Aged Brass Linear Chandelier | 11 | 31.20 | 107 | 3.40 | 13,383.63 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 12644 | Home Depot-ASN | GA | 209,744.48 | 464,924.09 | -54.90 | 0 | 0 | — | CONTRACTING |
| 319 | Karl'sAppliance#2690 | VA | 1,859,096.79 | 1,666,226.20 | 11.60 | 0 | 23,326 | -100 | COMPETITIVE_DISPLACEMENT |
| 10231 | Lamps.com | PA | 104,923.88 | 209,277.67 | -49.90 | 0 | 0 | — | CONTRACTING |
| 22285 | Wayfair Perigold-Auto EDI | MA | 98,776.37 | 162,207.95 | -39.10 | 0 | 0 | — | CONTRACTING |
| 9522 | Overstock.com, Inc-Auto EDI | UT | 106,832 | 170,120 | -37.20 | 0 | 0 | — | CONTRACTING |
| 24539 | Home Sense | ON | 77,178 | 134,172 | -42.50 | 0 | 0 | — | CONTRACTING |
| 12764 | WAYFAIR - Birch Lane-Auto EDI | MA | 130,198.45 | 178,195.85 | -26.90 | 0 | 0 | — | CONTRACTING |
| 10009 | Urban Lights | CO | 98,714.68 | 142,315.30 | -30.60 | 0 | 0 | — | CONTRACTING |
| 30651 | Cozy Development | SC | 51,342.18 | 7,785.06 | 559.50 | 0 | 3,576 | -100 | COMPETITIVE_DISPLACEMENT |
| 1774 | Wilson Lighting of Naples | FL | 68,311.20 | 108,596.93 | -37.10 | 0 | 0 | — | CONTRACTING |
| 11836 | WAYFAIR-Joss&Main.com-Auto EDI | MA | 83,657.83 | 123,688.83 | -32.40 | 0 | 0 | — | CONTRACTING |
| 11879 | Light Bulbs Unlimited | FL | 39,522.77 | 78,464.41 | -49.60 | 0 | 0 | — | CONTRACTING |
| 2140 | Armstrong Supply Co. | LA | 56,719.06 | 20,221.47 | 180.50 | 0 | 3,157 | -100 | COMPETITIVE_DISPLACEMENT |
| 9784 | Lighting By Fox, LLC | IL | 27,446.27 | 57,238.90 | -52 | 0 | 0 | — | CONTRACTING |
| 25145 | Cardello Electric Supply | PA | 75,222.21 | 102,144.50 | -26.40 | 0 | 0 | — | CONTRACTING |
| 825 | Union Lighting & Furnishings | ON | 60,313.40 | 86,526.90 | -30.30 | 0 | 8,065.10 | -100 | CONTRACTING |
| 4720 | Fan & Lighting World | FL | 38,790.71 | 60,508.15 | -35.90 | 0 | 0 | — | CONTRACTING |
| 12777 | Elaine Everett's Lighting | TX | 32,960.07 | 53,890.34 | -38.80 | 0 | 0 | — | CONTRACTING |
| 304 | Paramont-Evergreen Oak Inc. | IL | 57,971.06 | 78,168.59 | -25.80 | 0 | 0 | — | CONTRACTING |
| 6732 | LyteWorks | FL | 29,536.82 | 49,542.01 | -40.40 | 0 | 0 | — | CONTRACTING |
| 576 | Mayer-Erie PA | OR | 67,440 | 49,306 | 36.80 | 0 | 198 | -100 | COMPETITIVE_DISPLACEMENT |
| 159 | Butlers Lighting of Greensboro | SC | 51,037.67 | 69,109.39 | -26.10 | 0 | 0 | — | CONTRACTING |
| 1014 | LONE OAK - SOUTHFORK LIGHTING | MO | 29,695.84 | 47,740.75 | -37.80 | 0 | 0 | — | CONTRACTING |
| 754 | Sun Lighting | AZ | 36,323 | 54,217.88 | -33 | 0 | 0 | — | CONTRACTING |
| 30519 | City Plumbing & Electric | GA | 53,665.70 | 38,172.84 | 40.60 | 0 | 14,984.20 | -100 | COMPETITIVE_DISPLACEMENT |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 25207 | Melrose & Madison CANADA ONLY (AMZ) | 2 | 744,929.33 | 86.80 | [{'quarter': '2025-07-01', 'revenue': 224033.92, 'qoq_pct': 1.4}, {'quarter': '2025-10-01', 'revenue': 258744.44, 'qoq_pct': 15.5}, {'quarter': '2026-01-01', 'revenue': 483313.85, 'qoq_pct': 86.8}, {'quarter': '2026-04-01', 'revenue': 744929.33, 'qoq_pct': 54.1}] |
| 704 | ShadesofLight | 2 | 381,644.68 | 54.10 | [{'quarter': '2025-07-01', 'revenue': 173211.1, 'qoq_pct': -71.4}, {'quarter': '2025-10-01', 'revenue': 247650.4, 'qoq_pct': 43.0}, {'quarter': '2026-01-01', 'revenue': 381644.68, 'qoq_pct': 54.1}, {'quarter': '2026-04-01', 'revenue': 338009.64, 'qoq_pct': -11.4}] |
| 12167 | Lightopia, LLC. | 2 | 94,643.94 | 41.60 | [{'quarter': '2025-07-01', 'revenue': 94643.94, 'qoq_pct': 32.5}, {'quarter': '2025-10-01', 'revenue': 55585.42, 'qoq_pct': -41.3}, {'quarter': '2026-01-01', 'revenue': 78711.79, 'qoq_pct': 41.6}, {'quarter': '2026-04-01', 'revenue': 48307.9, 'qoq_pct': -38.6}] |
| 53 | BBC Lighting Company | 2 | 62,520.23 | 136.90 | [{'quarter': '2025-07-01', 'revenue': 62520.23, 'qoq_pct': 136.9}, {'quarter': '2025-10-01', 'revenue': 30166.89, 'qoq_pct': -51.7}, {'quarter': '2026-01-01', 'revenue': 54580.4, 'qoq_pct': 80.9}, {'quarter': '2026-04-01', 'revenue': 31757.13, 'qoq_pct': -41.8}] |
| 1628 | Crystorama Accm | 2 | 61,835.79 | 432.30 | [{'quarter': '2025-07-01', 'revenue': 7596.63, 'qoq_pct': -67.0}, {'quarter': '2025-10-01', 'revenue': 40440.0, 'qoq_pct': 432.3}, {'quarter': '2026-01-01', 'revenue': 13910.32, 'qoq_pct': -65.6}, {'quarter': '2026-04-01', 'revenue': 61835.79, 'qoq_pct': 344.5}] |
| 559 | M&M Lighting Co | 2 | 42,793.54 | 100 | [{'quarter': '2025-07-01', 'revenue': 13714.17, 'qoq_pct': -38.2}, {'quarter': '2025-10-01', 'revenue': 20900.99, 'qoq_pct': 52.4}, {'quarter': '2026-01-01', 'revenue': 21393.93, 'qoq_pct': 2.4}, {'quarter': '2026-04-01', 'revenue': 42793.54, 'qoq_pct': 100.0}] |
| 876 | Wilson Fans And Lighting - KS | 2 | 41,502.20 | 102.50 | [{'quarter': '2025-07-01', 'revenue': 20773.9, 'qoq_pct': -44.7}, {'quarter': '2025-10-01', 'revenue': 41502.2, 'qoq_pct': 99.8}, {'quarter': '2026-01-01', 'revenue': 19919.3, 'qoq_pct': -52.0}, {'quarter': '2026-04-01', 'revenue': 40338.75, 'qoq_pct': 102.5}] |
| 9329 | US Electrical Services, Inc.LA | 2 | 40,215 | 233.20 | [{'quarter': '2025-07-01', 'revenue': 40215.0, 'qoq_pct': 233.2}, {'quarter': '2025-10-01', 'revenue': 2955.0, 'qoq_pct': -92.7}, {'quarter': '2026-01-01', 'revenue': 8878.0, 'qoq_pct': 200.4}, {'quarter': '2026-04-01', 'revenue': 3132.0, 'qoq_pct': -64.7}] |
| 21252 | Kathy Kuo Home | 3 | 37,323.37 | 2,179.50 | [{'quarter': '2025-07-01', 'revenue': 697.0, 'qoq_pct': 511.4}, {'quarter': '2025-10-01', 'revenue': 15887.84, 'qoq_pct': 2179.5}, {'quarter': '2026-01-01', 'revenue': 28963.21, 'qoq_pct': 82.3}, {'quarter': '2026-04-01', 'revenue': 37323.37, 'qoq_pct': 28.9}] |
| 31171 | Hospitality Lighting Management | 2 | 37,045 | 164.60 | [{'quarter': '2025-10-01', 'revenue': 37045.0, 'qoq_pct': 120.6}, {'quarter': '2026-01-01', 'revenue': 374.0, 'qoq_pct': -99.0}, {'quarter': '2026-04-01', 'revenue': 989.52, 'qoq_pct': 164.6}] |
| 9522 | Overstock.com, Inc-Auto EDI | 2 | 37,019 | 94.10 | [{'quarter': '2025-07-01', 'revenue': 12437.0, 'qoq_pct': -48.9}, {'quarter': '2025-10-01', 'revenue': 24135.0, 'qoq_pct': 94.1}, {'quarter': '2026-01-01', 'revenue': 31454.0, 'qoq_pct': 30.3}, {'quarter': '2026-04-01', 'revenue': 37019.0, 'qoq_pct': 17.7}] |
| 5595 | Hinkley's Lighting Factory | 2 | 31,970.41 | 128.30 | [{'quarter': '2025-07-01', 'revenue': 21688.17, 'qoq_pct': 31.5}, {'quarter': '2025-10-01', 'revenue': 14002.69, 'qoq_pct': -35.4}, {'quarter': '2026-01-01', 'revenue': 31970.41, 'qoq_pct': 128.3}, {'quarter': '2026-04-01', 'revenue': 8094.2, 'qoq_pct': -74.7}] |
| 563 | Magnolia Lighting & Electric | 2 | 31,778.95 | 73.40 | [{'quarter': '2025-07-01', 'revenue': 22003.08, 'qoq_pct': -29.8}, {'quarter': '2025-10-01', 'revenue': 31778.95, 'qoq_pct': 44.4}, {'quarter': '2026-01-01', 'revenue': 17201.89, 'qoq_pct': -45.9}, {'quarter': '2026-04-01', 'revenue': 29832.09, 'qoq_pct': 73.4}] |
| 2140 | Armstrong Supply Co. | 2 | 30,822.31 | 204.40 | [{'quarter': '2025-07-01', 'revenue': 10125.0, 'qoq_pct': 88.1}, {'quarter': '2025-10-01', 'revenue': 30822.31, 'qoq_pct': 204.4}, {'quarter': '2026-01-01', 'revenue': 14927.75, 'qoq_pct': -51.6}, {'quarter': '2026-04-01', 'revenue': 645.0, 'qoq_pct': -95.7}] |
| 5369 | Passion Lighting | 2 | 30,331.91 | 181.40 | [{'quarter': '2025-07-01', 'revenue': 30331.91, 'qoq_pct': 181.4}, {'quarter': '2025-10-01', 'revenue': 11413.0, 'qoq_pct': -62.4}, {'quarter': '2026-01-01', 'revenue': 18961.0, 'qoq_pct': 66.1}, {'quarter': '2026-04-01', 'revenue': 16090.44, 'qoq_pct': -15.1}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Crystorama (clm, org_id=64)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HAY-1417-AG | Hayes 50'' Aged Brass Linear Chandelier | HAYES | 491,811.89 | 352 | — | 2026-7-14 | [{'customer': 'Build Drop Ship EDI', 'revenue': 30598.76}, {'customer': 'Elements', 'revenue': 28042.46}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 27794.75}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 20355.47}, {'customer': 'Lighting First - Bonita', 'revenue': 16689.5}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 13546.9}, {'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 13071.6}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 11858.25}, {'customer': 'Lighting, Inc', 'revenue': 11332.8}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 11146.85}, {'customer': 'Cleveland Lighting', 'revenue': 9174.2}, {'customer': 'Valley Light Gallery', 'revenue': 8544.6}, {'customer': 'Lightstyle of Orlando', 'revenue': 7454.28}, {'customer': "Horton's Home Lighting", 'revenue': 7310.25}, {'customer': 'Anthology Lighting', 'revenue': 6296.0}, {'customer': 'Universal Lights, Inc.', 'revenue': 6084.07}, {'customer': 'Lightology, LLC.com', 'revenue': 6072.14}, {'customer': 'Lighting By Fox, LLC', 'revenue': 5991.07}, {'customer': 'Litemode Limited', 'revenue': 5941.17}, {'customer': 'Dolan NW LLC', 'revenue': 5756.4}, {'customer': 'Progressive Lighting', 'revenue': 5576.4}, {'customer': 'Ellen Lighting & Hardware', 'revenue': 5322.64}, {'customer': 'Naples Lighting and Fan Depot', 'revenue': 4685.07}, {'customer': 'R. Bdelaa Lighting', 'revenue': 4597.0}, {'customer': 'Lighting Efx', 'revenue': 4573.14}, {'customer': 'Xpress Lighting of Texas', 'revenue': 4485.07}, {'customer': 'Metro Showroom West County', 'revenue': 4317.3}, {'customer': 'LDB Holdings, LLC', 'revenue': 3997.4}, {'customer': 'Lando Lighting', 'revenue': 3997.4}, {'customer': 'Home Lighting of Frazer', 'revenue': 3747.5}, {'customer': 'Reflections L+M', 'revenue': 3198.0}, {'customer': 'Muller Lighting Gallery', 'revenue': 3198.0}, {'customer': 'Aladdin Lighting & Supply, Inc', 'revenue': 3198.0}, {'customer': 'Lighting Etc', 'revenue': 3098.0}, {'customer': 'Passion Lighting', 'revenue': 3098.0}, {'customer': 'Continental Lighting Corp.', 'revenue': 3098.0}, {'customer': 'Dominion Electric', 'revenue': 3098.0}, {'customer': 'Nth Degree Home LLC', 'revenue': 3086.07}, {'customer': 'Haus Appeal LLC', 'revenue': 3006.12}, {'customer': 'Lightopia, LLC.', 'revenue': 3006.12}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 2998.0}, {'customer': 'Decorating Solutions by Sara', 'revenue': 2998.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 2998.0}, {'customer': 'Light Gallery Plus', 'revenue': 2998.0}, {'customer': 'Lighting First Ft. Myers', 'revenue': 2986.07}, {'customer': 'Mayson Enterprise dba Aura Lighting', 'revenue': 2974.14}, {'customer': "Graham's Living", 'revenue': 2881.14}, {'customer': 'Nova Lighting', 'revenue': 2881.14}, {'customer': 'E&L LIghting', 'revenue': 2848.1}, {'customer': 'Capitol Lighting-ASN', 'revenue': 2838.31}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 2788.2}, {'customer': 'Wilson Lighting of Naples', 'revenue': 2788.2}, {'customer': 'Foundrylighting.com', 'revenue': 2788.14}, {'customer': 'Southern Lights', 'revenue': 2788.14}, {'customer': 'Shades of Light', 'revenue': 2698.2}, {'customer': 'Crystorama Accm', 'revenue': 2698.2}, {'customer': 'Exclusive Lighting', 'revenue': 2548.3}, {'customer': 'ABC Creations', 'revenue': 2298.5}, {'customer': 'Royal Chic Design', 'revenue': 1999.0}, {'customer': 'Spark Lighting', 'revenue': 1874.0}, {'customer': 'Greer Lighting Center', 'revenue': 1873.75}, {'customer': 'Zimmerman Interiors', 'revenue': 1839.0}, {'customer': 'Pinnacle Design Consumer', 'revenue': 1839.0}, {'customer': 'Luminaires Repentigny Inc', 'revenue': 1759.0}, {'customer': 'Union Lighting & Home', 'revenue': 1724.0}, {'customer': 'O&I Design Group, LLC DBA The Elements', 'revenue': 1724.0}, {'customer': 'DDC Design', 'revenue': 1679.22}, {'customer': 'Littman Bros Lighting', 'revenue': 1599.0}, {'customer': 'Lightology, LLC-1', 'revenue': 1599.0}, {'customer': 'Aura Interiors Inc', 'revenue': 1599.0}, {'customer': 'Floral and Designs', 'revenue': 1599.0}, {'customer': 'Brothers Lighting &Fan Gallery', 'revenue': 1599.0}, {'customer': 'Morrison Supply Company,Midlan', 'revenue': 1599.0}, {'customer': 'Idlewood Electric Supply', 'revenue': 1599.0}, {'customer': 'Hye Lighting', 'revenue': 1599.0}, {'customer': 'Franklin Lighting', 'revenue': 1599.0}, {'customer': 'LyteWorks', 'revenue': 1599.0}, {'customer': "Garbe's Lighting and Hardware", 'revenue': 1599.0}, {'customer': 'Dulles Electric Supply', 'revenue': 1599.0}, {'customer': 'Save More Lighting, LTD', 'revenue': 1599.0}, {'customer': 'Armstrong Supply Co.', 'revenue': 1599.0}, {'customer': 'Hunzicker Lighting Gallery', 'revenue': 1599.0}, {'customer': 'IBS Lighting', 'revenue': 1599.0}, {'customer': 'Denali Lighting', 'revenue': 1599.0}, {'customer': 'M&M Lighting Co', 'revenue': 1599.0}, {'customer': 'At Home LLC DBA Home Lighting', 'revenue': 1599.0}, {'customer': 'Light Bulbs Etc (Montclair)', 'revenue': 1519.05}, {'customer': 'The Lighting Corner', 'revenue': 1499.0}, {'customer': 'PC Building Materials', 'revenue': 1499.0}, {'customer': 'Luminous Trends Inc DBA Modern Luxury by LT)', 'revenue': 1499.0}, {'customer': 'CES Aquisition LLC', 'revenue': 1499.0}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 1499.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 1499.0}, {'customer': 'Schwartz Design Showroom', 'revenue': 1499.0}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 1499.0}, {'customer': 'Fan & Lighting World', 'revenue': 1499.0}, {'customer': 'GW Lighting & Home Decor', 'revenue': 1499.0}, {'customer': 'House of Lights, Inc.', 'revenue': 1499.0}, {'customer': 'Naples Lamp Shop', 'revenue': 1499.0}, {'customer': 'Bolgiano Custom Homes&Interior', 'revenue': 1499.0}, {'customer': 'Bulbo', 'revenue': 1499.0}, {'customer': 'Maple Ridge Lighting Inc.', 'revenue': 1499.0}, {'customer': 'The Fixture Exchange', 'revenue': 1499.0}, {'customer': 'Lee Douglas Interiors, Inc.', 'revenue': 1499.0}, {'customer': 'Nimbus Nine Inc.', 'revenue': 1499.0}, {'customer': 'DuPage Lighting Inc.', 'revenue': 1487.07}, {'customer': 'Premier Bath Lighting&Hardware', 'revenue': 1487.07}, {'customer': 'Jones Group Interiors, Inc.', 'revenue': 1487.07}, {'customer': 'Robinson Lighting Centre', 'revenue': 1487.07}, {'customer': 'Georgia Lighting', 'revenue': 1487.07}, {'customer': 'Marx Fireplace and Lighting', 'revenue': 1487.07}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 1487.07}, {'customer': 'Lighting Direct NJ LLC', 'revenue': 1487.07}, {'customer': 'Accent Lighting, Inc.', 'revenue': 1487.07}, {'customer': 'Modern Lighting', 'revenue': 1487.07}, {'customer': "Efird's Interiors, Inc.", 'revenue': 1439.1}, {'customer': 'Luxury Lighting', 'revenue': 1439.1}, {'customer': 'C E Tang Yuk and Co Ltd', 'revenue': 1394.07}, {'customer': 'ABC Lighting Inc', 'revenue': 1394.07}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 1394.07}, {'customer': 'ArtGlass Canada Inc DBA Casa Di Luce', 'revenue': 1394.07}, {'customer': 'The Lighthouse', 'revenue': 1394.07}, {'customer': 'Beautiful Lights', 'revenue': 1349.1}, {'customer': 'Union Lighting & Furnishings', 'revenue': 1279.2}, {'customer': 'Montreal Luminaire', 'revenue': 1231.3}, {'customer': 'Erika Ward Interiors', 'revenue': 1214.19}, {'customer': 'RAINBOW LIGHTING INC', 'revenue': 1199.2}, {'customer': 'Hall Electric Co, Inc', 'revenue': 1119.3}, {'customer': 'Lyons Electrical Supply Co.', 'revenue': 1049.3}, {'customer': 'Illuminations', 'revenue': 899.4}, {'customer': 'Galleria Lighting  E MAIL', 'revenue': 799.5}, {'customer': 'Light Lab Design', 'revenue': 768.1}, {'customer': 'Prima Lighting', 'revenue': 749.5}, {'customer': 'First Coast Lighting & Fans', 'revenue': 0.0}, {'customer': 'Mars Electric Co.', 'revenue': 0.0}, {'customer': 'Ponton Interiors', 'revenue': 0.0}, {'customer': 'Light Point', 'revenue': 0.0}, {'customer': 'First Fruit Collection', 'revenue': 0.0}] | [{'item': 'HAY-1402-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 102}, {'item': 'HAY-1401-AG', 'desc': "Hayes 8'' Aged Brass Chandelier", 'available': 75}, {'item': 'HAY-1402-AG', 'desc': "Hayes 7.5'' Aged Brass Sconce", 'available': 61}, {'item': 'HAY-1411-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 39}, {'item': 'HAY-1401-PN', 'desc': "Hayes 8'' Polished Nickel Chandelier", 'available': 33}, {'item': 'HAY-1400-AG', 'desc': "Hayes 16'' Aged Brass Flush Mount", 'available': 30}, {'item': 'HAY-1409-AG', 'desc': "Hayes 40.5'' Aged Brass Chandelier", 'available': 29}, {'item': 'HAY-1407-PN', 'desc': "Hayes 28'' Polished Nickel Chandelier", 'available': 28}, {'item': 'HAY-1407-AG', 'desc': "Hayes 28'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1405-AG', 'desc': "Hayes 22'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1403-AG', 'desc': "Hayes 18'' Aged Brass Flush Mount", 'available': 24}, {'item': 'HAY-1403-PN', 'desc': "Hayes 18'' Polished Nickel Flush Mount", 'available': 17}, {'item': 'HAY-1413-PN', 'desc': "Hayes 23.5'' Polished Nickel Bathroom Vanity", 'available': 12}, {'item': 'HAY-1405-PN', 'desc': "Hayes 22'' Polished Nickel Chandelier", 'available': 12}, {'item': 'HAY-1400-PN', 'desc': "Hayes 16'' Polished Nickel Flush Mount", 'available': 10}, {'item': 'HAY-1415-PN', 'desc': "Hayes 31.5'' Polished Nickel Bathroom Vanity", 'available': 9}, {'item': 'HAY-1417-PN', 'desc': "Hayes 50'' Polished Nickel Linear Chandelier", 'available': 8}, {'item': 'HAY-1415-AG', 'desc': "Hayes 31.5'' Aged Brass Bathroom Vanity", 'available': 8}, {'item': 'HAY-1413-AG', 'desc': "Hayes 23.5'' Aged Brass Bathroom Vanity", 'available': 6}, {'item': 'HAY-1419-AG', 'desc': "Hayes 24'' Aged Brass Chandelier", 'available': 1}] |
| ADD-317-AG-CL | Addis 51.75'' Aged Brass Linear Chandelier | ADDIS | 296,812.82 | 258 | — | 2026-6-30 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 22170.22}, {'customer': 'Elements', 'revenue': 18638.9}, {'customer': 'Build Drop Ship EDI', 'revenue': 17236.85}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 15421.0}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 10155.6}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 8954.38}, {'customer': 'Idlewood Electric Supply', 'revenue': 6826.14}, {'customer': 'Reflections L+M', 'revenue': 6388.1}, {'customer': 'Dominion Electric', 'revenue': 5854.07}, {'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 5710.5}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 5500.76}, {'customer': "Graham's Living", 'revenue': 4832.28}, {'customer': 'Loudoun Interiors LLC', 'revenue': 4088.64}, {'customer': 'Daniel House Club', 'revenue': 3747.0}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 3747.0}, {'customer': 'IBS Lighting', 'revenue': 3747.0}, {'customer': 'Lights Unlimited', 'revenue': 3697.0}, {'customer': 'CAI Designs', 'revenue': 3597.0}, {'customer': 'Lighting Studio', 'revenue': 3597.0}, {'customer': 'Aladdin Lighting & Supply, Inc', 'revenue': 3575.64}, {'customer': 'Lights on Design', 'revenue': 3425.64}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 3147.3}, {'customer': "Elaine Everett's Lighting", 'revenue': 2987.4}, {'customer': 'Union Lighting & Furnishings', 'revenue': 2877.6}, {'customer': 'Joseph Moretti Design', 'revenue': 2748.0}, {'customer': 'Lightology, LLC.com', 'revenue': 2598.0}, {'customer': 'Cregger Company, LLC', 'revenue': 2598.0}, {'customer': 'Light Lab Design', 'revenue': 2598.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 2448.0}, {'customer': 'The Brecher Company', 'revenue': 2448.0}, {'customer': 'Littman Bros Lighting', 'revenue': 2448.0}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 2416.14}, {'customer': 'First Coast Lighting & Fans', 'revenue': 2367.57}, {'customer': 'Shades of Light', 'revenue': 2338.2}, {'customer': 'Foundrylighting.com', 'revenue': 2321.07}, {'customer': 'Wilson Fans And Lighting', 'revenue': 2203.2}, {'customer': 'Light Gallery Plus', 'revenue': 2198.0}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 2104.38}, {'customer': 'Lightopia, LLC.', 'revenue': 2090.64}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 1897.47}, {'customer': 'Shelby Mae Interiors', 'revenue': 1651.6}, {'customer': 'COLLECTED DESIGN LLC', 'revenue': 1608.6}, {'customer': 'Alison Friedricks Interior', 'revenue': 1494.0}, {'customer': 'Chroma Home, LLC', 'revenue': 1374.0}, {'customer': 'Union Lighting & Home', 'revenue': 1328.97}, {'customer': 'Carpet Palace Bethesda DBA Designer Workshop', 'revenue': 1322.0}, {'customer': 'Anderson Design Studio', 'revenue': 1321.0}, {'customer': 'Bright Ideas LED', 'revenue': 1316.93}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 1299.0}, {'customer': 'Hye Lighting', 'revenue': 1299.0}, {'customer': 'Fan & Lighting World', 'revenue': 1299.0}, {'customer': 'Passion Lighting', 'revenue': 1299.0}, {'customer': 'M&M Lighting Co', 'revenue': 1299.0}, {'customer': 'Mayson Enterprise dba Aura Lighting', 'revenue': 1299.0}, {'customer': 'Coley Electric & Plumbing Sup', 'revenue': 1299.0}, {'customer': 'Complete Lighting of Tampa,Inc', 'revenue': 1299.0}, {'customer': 'The Shallotte Electric Store', 'revenue': 1299.0}, {'customer': 'Lighting First Ft. Myers', 'revenue': 1299.0}, {'customer': 'Revival Lighting', 'revenue': 1299.0}, {'customer': 'Posh HB LLC DBA Posh Home and Bath', 'revenue': 1299.0}, {'customer': 'Kendall Electric', 'revenue': 1299.0}, {'customer': 'Aura Interiors Inc', 'revenue': 1299.0}, {'customer': 'The Jarrell Company', 'revenue': 1299.0}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 1299.0}, {'customer': 'At Home LLC DBA Home Lighting', 'revenue': 1299.0}, {'customer': 'Styled Interiors', 'revenue': 1236.6}, {'customer': 'Lighting Direct NJ LLC', 'revenue': 1235.89}, {'customer': 'Lighting First - Bonita', 'revenue': 1208.07}, {'customer': 'Southern Lights', 'revenue': 1208.07}, {'customer': 'Capitol Lighting Gallery', 'revenue': 1208.07}, {'customer': 'Valencia Lighting & Design', 'revenue': 1208.07}, {'customer': 'Kitchen Concepts & Designs, LL', 'revenue': 1208.07}, {'customer': 'Light Art of Durango', 'revenue': 1208.07}, {'customer': 'Christies Lighting Gallery,LLC', 'revenue': 1208.07}, {'customer': 'Robinson Lighting Centre', 'revenue': 1208.07}, {'customer': 'Progressive Lighting', 'revenue': 1169.1}, {'customer': 'Capitol Lighting-ASN', 'revenue': 1169.1}, {'customer': 'Metro Showroom West County', 'revenue': 1169.1}, {'customer': 'Dolan NW LLC', 'revenue': 1169.1}, {'customer': 'Electric Supply Lighting', 'revenue': 1149.0}, {'customer': 'Urban Lights', 'revenue': 1149.0}, {'customer': 'Bee Ridge Lighting & Design', 'revenue': 1149.0}, {'customer': 'Capital Electric', 'revenue': 1149.0}, {'customer': 'The Lighting Hut by Wilson', 'revenue': 1149.0}, {'customer': 'Pine Lighting', 'revenue': 1149.0}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 1149.0}, {'customer': 'Davids Furniture Ltd.', 'revenue': 1149.0}, {'customer': 'Safavieh Outlet', 'revenue': 1149.0}, {'customer': 'One Stop Lighting', 'revenue': 1149.0}, {'customer': 'Elan Studio Lighting', 'revenue': 1149.0}, {'customer': 'Kim E Courtney Interiors', 'revenue': 1149.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1149.0}, {'customer': 'CES Aquisition LLC', 'revenue': 1149.0}, {'customer': 'Georgia Lighting', 'revenue': 1149.0}, {'customer': 'Capital City Lighting', 'revenue': 1149.0}, {'customer': 'BBC Lighting Company', 'revenue': 1149.0}, {'customer': 'Stokes Lighting Center', 'revenue': 1149.0}, {'customer': 'Sun Lighting', 'revenue': 1149.0}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 1149.0}, {'customer': 'Lighting First Naples', 'revenue': 1149.0}, {'customer': 'ABC Lighting Inc', 'revenue': 1149.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 1099.0}, {'customer': 'Dement Lighting', 'revenue': 1099.0}, {'customer': 'The Design Firm. Inc.', 'revenue': 1099.0}, {'customer': 'Cleveland Lighting', 'revenue': 1091.55}, {'customer': 'Amber Dawn Designs', 'revenue': 1070.01}, {'customer': '2514004  Ontario Inc O/A iLITE', 'revenue': 1068.57}, {'customer': 'Pine Tree Lighting', 'revenue': 1068.57}, {'customer': 'Elume Distinctive Lighting**', 'revenue': 1068.57}, {'customer': 'Lighting Superstore', 'revenue': 1068.57}, {'customer': 'Porter Lighting Sales, Inc.', 'revenue': 1039.2}, {'customer': 'Lofings Lighting Inc', 'revenue': 1022.07}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 1022.07}, {'customer': 'Luxury Lighting', 'revenue': 659.4}, {'customer': 'Shades of Light', 'revenue': 0.0}, {'customer': 'Lighting, Inc', 'revenue': 0.0}, {'customer': 'Galleria Lighting  E MAIL', 'revenue': 0.0}, {'customer': 'Light Bulbs Unlimited', 'revenue': 0.0}, {'customer': 'Tec of North Little Rock', 'revenue': 0.0}, {'customer': 'Moreau Enterprises/Aggieland', 'revenue': 0.0}, {'customer': 'Winsupply Owensboro KY Co', 'revenue': 0.0}, {'customer': 'McLoughlan Supplies Limited', 'revenue': 0.0}, {'customer': 'Lighting Connection', 'revenue': 0.0}, {'customer': 'Prima Lighting', 'revenue': 0.0}, {'customer': 'Naples Lamp Shop', 'revenue': 0.0}, {'customer': 'Lighting Design Center', 'revenue': 0.0}, {'customer': "Hinkley's Lighting Factory", 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
| SHY-10907-SG | Shyla 24'' Soft Gold Chandelier | SHYLA | 292,247.01 | 657 | — | 2026-6-23 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 22511.75}, {'customer': 'Build Drop Ship EDI', 'revenue': 21032.63}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 19488.29}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 12424.76}, {'customer': 'Lightopia, LLC.', 'revenue': 10343.07}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 9050.66}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 8043.93}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 6700.5}, {'customer': 'Decorative Lighting Inc', 'revenue': 6505.21}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 5743.49}, {'customer': 'Lighting First - Bonita', 'revenue': 4922.49}, {'customer': 'Melrose & Madison (AMZ)', 'revenue': 4891.63}, {'customer': 'Union Lighting & Home', 'revenue': 4700.7}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 4696.0}, {'customer': 'Lightology, LLC.com', 'revenue': 4039.5}, {'customer': 'One Kings Lane.com-ASN', 'revenue': 3910.5}, {'customer': "Graham's Living", 'revenue': 3903.21}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 3761.07}, {'customer': 'Foundrylighting.com', 'revenue': 3428.5}, {'customer': 'Southern Lights', 'revenue': 3426.28}, {'customer': 'Lights Unlimited', 'revenue': 2945.0}, {'customer': 'Lighting First Naples', 'revenue': 2499.78}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 2494.13}, {'customer': 'First Coast Lighting & Fans', 'revenue': 2316.5}, {'customer': 'Montreal Luminaire', 'revenue': 2088.0}, {'customer': 'Progressive Lighting', 'revenue': 2069.1}, {'customer': 'Decorum', 'revenue': 1810.71}, {'customer': 'Dominion Electric', 'revenue': 1800.0}, {'customer': 'Brothers Lighting &Fan Gallery', 'revenue': 1638.07}, {'customer': 'M&M Lighting Co', 'revenue': 1638.07}, {'customer': 'Vida Events & Design LLC', 'revenue': 1610.0}, {'customer': 'Union Lighting & Home', 'revenue': 1531.71}, {'customer': 'Daniel House Club', 'revenue': 1497.0}, {'customer': "Montgomery's Furniture", 'revenue': 1497.0}, {'customer': 'Nova Lighting', 'revenue': 1497.0}, {'customer': 'Lifestyles Stores, Inc', 'revenue': 1497.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 1448.0}, {'customer': 'Grand Rapids Lighting', 'revenue': 1448.0}, {'customer': 'Kathy Kuo Home', 'revenue': 1432.12}, {'customer': 'Low Country Lighting Studio', 'revenue': 1399.0}, {'customer': 'Home Depot-ASN', 'revenue': 1350.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 1347.3}, {'customer': 'Lights of Oconee', 'revenue': 1332.57}, {'customer': 'Dolan NW LLC', 'revenue': 1303.2}, {'customer': 'Metro Showroom West County', 'revenue': 1215.0}, {'customer': 'Union Lighting & Furnishings', 'revenue': 1158.4}, {'customer': 'Kristen Morrison Interiors', 'revenue': 1148.0}, {'customer': 'Elements', 'revenue': 1003.62}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 998.0}, {'customer': 'Mathes of Alabama Electric Supply Co., Inc.', 'revenue': 998.0}, {'customer': 'The Lighting Marketplace DBA Fixture Farm', 'revenue': 998.0}, {'customer': 'Sundial Home Products LLC', 'revenue': 998.0}, {'customer': 'City Plumbing & Electric', 'revenue': 998.0}, {'customer': 'Cape Electrical Sup(Southfork)', 'revenue': 998.0}, {'customer': 'Lighting Etc.', 'revenue': 998.0}, {'customer': 'Lighting Connection', 'revenue': 998.0}, {'customer': 'Luxur Lighting', 'revenue': 949.0}, {'customer': 'JCM Lighting and Design, DBA The Local Lighting Shop', 'revenue': 949.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 949.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 928.14}, {'customer': 'Candelabra Light & Design.com DBA Meadow Blu', 'revenue': 917.5}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 900.0}, {'customer': 'Frooogal -DBA  France & Son', 'revenue': 900.0}, {'customer': 'Avenue Lighting & Design', 'revenue': 899.1}, {'customer': 'Lamps.com', 'revenue': 883.02}, {'customer': 'Paradise Lighting', 'revenue': 880.02}, {'customer': 'Beautiful Lights', 'revenue': 869.07}, {'customer': 'Classic Lighting & Design, Inc', 'revenue': 868.5}, {'customer': "Efird's Interiors, Inc.", 'revenue': 854.1}, {'customer': 'Brandywine Lighting Gallery', 'revenue': 837.0}, {'customer': 'Capital Electric', 'revenue': 814.0}, {'customer': "Mahlander's Appliance Lighting", 'revenue': 814.0}, {'customer': 'The Lighting Studio', 'revenue': 814.0}, {'customer': 'Winsupply Owensboro KY Co', 'revenue': 814.0}, {'customer': 'Lighting By Design - Dec Den', 'revenue': 769.0}, {'customer': 'Lando Lighting', 'revenue': 769.0}, {'customer': 'Accent Lighting, Inc.', 'revenue': 748.5}, {'customer': 'Hye Lighting', 'revenue': 720.0}, {'customer': 'Light Bulbs Etc (Montclair)', 'revenue': 699.05}, {'customer': 'Prima Lighting', 'revenue': 675.0}, {'customer': 'Redefined Lighting, LLC', 'revenue': 624.0}, {'customer': 'Monet Design', 'revenue': 574.0}, {'customer': 'The Beach Home, LLC', 'revenue': 574.0}, {'customer': 'Brick House Designs', 'revenue': 574.0}, {'customer': 'Crampton Lighting Design, Inc.', 'revenue': 574.0}, {'customer': 'Asburys Furnishings & Design', 'revenue': 574.0}, {'customer': 'Crimson Design Group', 'revenue': 574.0}, {'customer': 'Kelly Lord Designs', 'revenue': 574.0}, {'customer': 'Oak Highland Design dba Dec De', 'revenue': 563.0}, {'customer': 'Abode Made LLC', 'revenue': 563.0}, {'customer': 'JMH Designs', 'revenue': 563.0}, {'customer': 'CasaBella', 'revenue': 563.0}, {'customer': 'KV Design Co', 'revenue': 563.0}, {'customer': 'Mckenzie Baker Interiors', 'revenue': 563.0}, {'customer': 'Techtron Products, Inc', 'revenue': 563.0}, {'customer': 'West Coast Cabinets', 'revenue': 563.0}, {'customer': 'Inside Source LLC', 'revenue': 519.01}, {'customer': 'Carlyle Design Studio', 'revenue': 518.0}, {'customer': 'J and G Central Coast Interiors DBA Chic Interiors', 'revenue': 518.0}, {'customer': 'Serenity Design', 'revenue': 518.0}, {'customer': 'Kelley Elizabeth Interiors', 'revenue': 518.0}, {'customer': 'Cozy Development', 'revenue': 518.0}, {'customer': 'The Ervin Group', 'revenue': 518.0}, {'customer': 'Rast Road LLC DBA Emily Wood Design Co.', 'revenue': 518.0}, {'customer': 'Craven Gardner Design & Build', 'revenue': 518.0}, {'customer': 'Coastline Copper DBA The Henry Haus', 'revenue': 518.0}, {'customer': 'Lighting World Decorator', 'revenue': 499.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 499.0}, {'customer': 'Cregger Company, LLC', 'revenue': 499.0}, {'customer': 'IBS Lighting', 'revenue': 499.0}, {'customer': 'Burgess Lighting', 'revenue': 499.0}, {'customer': 'Creative Interiors, LTD', 'revenue': 499.0}, {'customer': 'Raymond Desteiger, Inc.', 'revenue': 499.0}, {'customer': 'Shannon Terry Interiors', 'revenue': 499.0}, {'customer': 'Light Bulbs, Etc. (Orange)', 'revenue': 499.0}, {'customer': 'Design Trade Service', 'revenue': 499.0}, {'customer': 'Chroma Home, LLC', 'revenue': 499.0}, {'customer': 'Light Idaho, LLC DBA Wolfe Lighting Twin Falls', 'revenue': 499.0}, {'customer': 'Lumi Lighting & Home Design', 'revenue': 499.0}, {'customer': 'The Jarrell Company', 'revenue': 499.0}, {'customer': 'Fort Worth Lighting', 'revenue': 499.0}, {'customer': 'Masterpiece Lighting Inc', 'revenue': 499.0}, {'customer': 'Magnolia Lighting & Electric', 'revenue': 499.0}, {'customer': 'Sun Lighting', 'revenue': 499.0}, {'customer': 'The Shallotte Electric Store', 'revenue': 499.0}, {'customer': 'Wasatch Lighting, Inc', 'revenue': 499.0}, {'customer': 'Littman Bros Lighting', 'revenue': 499.0}, {'customer': 'Construction Resources Company LLC', 'revenue': 499.0}, {'customer': 'Electrimat', 'revenue': 495.0}, {'customer': 'S. Mahoney Designs LLC DBA Mahoney Design Studio', 'revenue': 478.55}, {'customer': 'Haus Appeal LLC', 'revenue': 474.05}, {'customer': 'Litemode Limited', 'revenue': 464.07}, {'customer': 'Minnesota Lighting Fireplace', 'revenue': 464.07}, {'customer': "Hinkley's Lighting Factory", 'revenue': 464.07}, {'customer': 'Cleveland Lighting', 'revenue': 464.07}, {'customer': 'Broadway Showroom', 'revenue': 464.07}, {'customer': 'Energy Plus', 'revenue': 450.0}, {'customer': 'Thompson Supply Co.', 'revenue': 450.0}, {'customer': 'SideDoor', 'revenue': 450.0}, {'customer': 'CAI Designs', 'revenue': 450.0}, {'customer': 'Pelican Equipment Rentals, Inc', 'revenue': 450.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 450.0}, {'customer': 'Good Friend Electric', 'revenue': 450.0}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 450.0}, {'customer': 'Reflections L+M', 'revenue': 450.0}, {'customer': 'Best Lighting', 'revenue': 450.0}, {'customer': 'Crystorama Accm', 'revenue': 450.0}, {'customer': 'Warshauer Electric', 'revenue': 450.0}, {'customer': 'LJP dba Southside Lighting', 'revenue': 450.0}, {'customer': 'BBC Lighting Company', 'revenue': 450.0}, {'customer': 'Prosource , LLC', 'revenue': 450.0}, {'customer': 'Radue Homes Inc dba Inspired Spaces', 'revenue': 450.0}, {'customer': 'Standard Electric', 'revenue': 450.0}, {'customer': 'Briggs Inc of Omaha', 'revenue': 450.0}, {'customer': 'Ricks Lighting and Supply', 'revenue': 450.0}, {'customer': 'Rittenhouse Electric Supply Co', 'revenue': 450.0}, {'customer': 'Coley Electric & Plumbing Sup', 'revenue': 450.0}, {'customer': 'Net Retailers dba Luxe Decor', 'revenue': 450.0}, {'customer': 'Lighting Connection', 'revenue': 450.0}, {'customer': 'Signature Lighting and Fans', 'revenue': 450.0}, {'customer': 'Nantucket Lightshop', 'revenue': 450.0}, {'customer': 'The Saltbox', 'revenue': 450.0}, {'customer': 'SKD Studios', 'revenue': 450.0}, {'customer': "Wilkinson's House of Lights", 'revenue': 450.0}, {'customer': 'Manasquan Lighting', 'revenue': 450.0}, {'customer': 'Overstock.com, Inc-Auto EDI', 'revenue': 450.0}, {'customer': 'Fanwerks & Lighting Inc', 'revenue': 450.0}, {'customer': 'Broad Street Interiors', 'revenue': 450.0}, {'customer': 'Urban Lights', 'revenue': 450.0}, {'customer': 'Fifth and College Tile and Design Co.', 'revenue': 450.0}, {'customer': 'Gallery South Inc', 'revenue': 450.0}, {'customer': 'Flemington Lighting & Fan', 'revenue': 450.0}, {'customer': 'Madison Lighting', 'revenue': 450.0}, {'customer': 'J & B Supply Inc.', 'revenue': 450.0}, {'customer': 'Joseph Electric Company', 'revenue': 450.0}, {'customer': "Horton's Home Lighting", 'revenue': 427.5}, {'customer': 'Mars Electric Co.', 'revenue': 418.5}, {'customer': 'The Lighting Design Co.', 'revenue': 418.5}, {'customer': 'Lighting First Ft. Myers', 'revenue': 418.5}, {'customer': 'LDB Holdings, LLC', 'revenue': 405.0}, {'customer': 'Wilson Lighting - St Louis', 'revenue': 405.0}, {'customer': 'Brandino Brass Co', 'revenue': 405.0}, {'customer': 'Lighting, Inc', 'revenue': 405.0}, {'customer': 'Wilson Fans And Lighting', 'revenue': 405.0}, {'customer': 'Precision Diamante', 'revenue': 382.5}, {'customer': 'Live Edge USA DBA Brick Mill', 'revenue': 349.3}, {'customer': 'Hampton Home Dinettes', 'revenue': 349.3}, {'customer': 'Richards Lighting', 'revenue': 349.3}, {'customer': 'Made New Interiors and Decor, LLC', 'revenue': 349.3}, {'customer': 'The Electrical &Plumbing Store', 'revenue': 315.0}, {'customer': 'Designer Blvd, LLC', 'revenue': 315.0}, {'customer': 'Interior Design House', 'revenue': 315.0}, {'customer': 'Plumb Supply Co', 'revenue': 299.4}, {'customer': "Graham's Lighting", 'revenue': 249.5}, {'customer': '43rd Street Lighting, Inc.', 'revenue': 225.0}, {'customer': 'One Stop Lighting', 'revenue': 225.0}, {'customer': 'Lighting Emporium', 'revenue': 225.0}, {'customer': 'Lighting Aura', 'revenue': 225.0}, {'customer': 'Bird Stairs', 'revenue': 0.0}, {'customer': 'Julie Bova Interior Design', 'revenue': 0.0}, {'customer': 'Carrington Lighting', 'revenue': 0.0}] | [{'item': 'SHY-10909-SG', 'desc': "Shyla 32'' Soft Gold Chandelier", 'available': 44}] |
| ARA-10269-MK-ST | Aragon 58.75'' LED Matte Black Chandelier | COL127 | 265,753.16 | 102 | — | 2026-8-18 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 21074.15}, {'customer': 'Capital Electric', 'revenue': 19662.0}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 15561.77}, {'customer': 'Lightology, LLC.com', 'revenue': 11387.71}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 11270.93}, {'customer': 'Elements', 'revenue': 9959.3}, {'customer': 'Passion Lighting', 'revenue': 9947.0}, {'customer': 'Build Drop Ship EDI', 'revenue': 9086.56}, {'customer': 'IBS Lighting', 'revenue': 8805.91}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 8547.0}, {'customer': 'Dolan NW LLC', 'revenue': 7602.3}, {'customer': 'North Coast Lighting', 'revenue': 7275.0}, {'customer': "Graham's Living", 'revenue': 6975.0}, {'customer': 'Construction Resources Company LLC', 'revenue': 5698.0}, {'customer': 'Urban Lights', 'revenue': 5648.0}, {'customer': 'Yellow Pine LLC', 'revenue': 5299.0}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 5077.52}, {'customer': 'Hobrecht Lighting Co., Inc.', 'revenue': 5000.0}, {'customer': 'CoCo Curtain Studio', 'revenue': 5000.0}, {'customer': 'Lightstyle of Orlando', 'revenue': 3749.5}, {'customer': 'Swine Design LLC', 'revenue': 3366.79}, {'customer': 'Lee Douglas Interiors, Inc.', 'revenue': 3277.0}, {'customer': 'Designs with you in Mind', 'revenue': 3222.98}, {'customer': 'Inside Source LLC', 'revenue': 3124.0}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 3020.18}, {'customer': 'Crystorama Accm', 'revenue': 2995.0}, {'customer': 'Light Idaho, LLC DBA Wolfe Lighting Twin Falls', 'revenue': 2895.05}, {'customer': 'CES Aquisition LLC', 'revenue': 2849.0}, {'customer': 'Northern Lighting', 'revenue': 2849.0}, {'customer': 'M&M Lighting Co', 'revenue': 2849.0}, {'customer': 'Jerome Lessard Design', 'revenue': 2812.32}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 2799.0}, {'customer': 'Luminous Trends Inc DBA Modern Luxury by LT)', 'revenue': 2799.0}, {'customer': 'Royce Collection Inc.', 'revenue': 2799.0}, {'customer': 'LJP dba Southside Lighting', 'revenue': 2799.0}, {'customer': 'Nimbus Nine Inc.', 'revenue': 2749.0}, {'customer': 'Vogue Lighting', 'revenue': 2749.0}, {'customer': 'Lights Unlimited', 'revenue': 2749.0}, {'customer': 'Lighting Innovation', 'revenue': 2671.92}, {'customer': 'Imagine More', 'revenue': 2603.07}, {'customer': "Mahlander's Appliance Lighting", 'revenue': 2500.0}, {'customer': 'Dominion Electric', 'revenue': 2500.0}, {'customer': 'The Lighting Design Co.', 'revenue': 2500.0}, {'customer': 'Lighting, Inc', 'revenue': 2474.1}, {'customer': 'Wilson Fans And Lighting', 'revenue': 2474.1}, {'customer': 'Christies Lighting Gallery,LLC', 'revenue': 2325.0}, {'customer': 'Krell Lighting & Electric Supp', 'revenue': 2250.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 2250.0}, {'customer': 'Lightopia, LLC.', 'revenue': 2250.0}, {'customer': 'Robert Sales Inc #109', 'revenue': 1875.0}, {'customer': 'Hajoca Corporation', 'revenue': 1750.0}, {'customer': 'Accent Lighting Galleries', 'revenue': 0.0}, {'customer': 'Brad Ramsey Interiors', 'revenue': 0.0}] | [{'item': 'ARA-10261-SB-ST', 'desc': "Aragon 4.5'' LED Soft Brass Sconce", 'available': 85}, {'item': 'ARA-10261-MK-ST', 'desc': "Aragon 4.5'' LED Matte Black Sconce", 'available': 70}, {'item': 'ARA-10261-MK', 'desc': "Aragon 4.5'' LED Matte Black Sconce", 'available': 63}, {'item': 'ARA-10261-SB', 'desc': "Aragon 4.5'' LED Soft Brass Sconce", 'available': 51}, {'item': 'ARA-10266-MK', 'desc': "Aragon 48'' LED Matte Black Chandelier", 'available': 44}, {'item': 'ARA-10267-MK-ST', 'desc': "Aragon 56'' LED Matte Black Linear Chandelier", 'available': 43}, {'item': 'ARA-10266-MK-ST', 'desc': "Aragon 46.75'' LED Matte Black Chandelier", 'available': 37}, {'item': 'ARA-10266-SB-ST', 'desc': "Aragon 46.75'' LED Soft Brass Chandelier", 'available': 32}, {'item': 'ARA-10267-SB-ST', 'desc': "Aragon 56'' LED Soft Brass Linear Chandelier", 'available': 28}, {'item': 'ARA-10267-SB', 'desc': "Aragon 56'' LED Soft Brass Linear Chandelier", 'available': 23}, {'item': 'ARA-10265-MK-ST', 'desc': "Aragon 34.75'' LED Matte Black Chandelier", 'available': 22}, {'item': 'ARA-10266-SB', 'desc': "Aragon 48'' LED Soft Brass Chandelier", 'available': 18}, {'item': 'ARA-10265-SB-ST', 'desc': "Aragon 34.75'' LED Soft Brass Chandelier", 'available': 17}, {'item': 'ARA-10265-MK', 'desc': "Aragon 36'' LED Matte Black Chandelier", 'available': 14}, {'item': 'ARA-10267-MK', 'desc': "Aragon 56'' LED Matte Black Linear Chandelier", 'available': 13}, {'item': 'ARA-10265-SB', 'desc': "Aragon 36'' LED Soft Brass Chandelier", 'available': 11}, {'item': 'ARA-10268-SB', 'desc': "Aragon 48'' LED Soft Brass Chandelier", 'available': 3}, {'item': 'ARA-10264-SB-ST', 'desc': "Aragon 22.75'' LED Soft Brass Chandelier", 'available': 3}, {'item': 'ARA-10268-SB-ST', 'desc': "Aragon 46.75'' LED Soft Brass Chandelier", 'available': 3}, {'item': 'ARA-10269-SB', 'desc': "Aragon 60'' LED Soft Brass Chandelier", 'available': 2}, {'item': 'ARA-10269-SB-ST', 'desc': "Aragon 58.75'' LED Soft Brass Chandelier", 'available': 2}] |
| 505-MT | Broche 16'' Matte White Semi Flush Mount | COL100 | 230,169.06 | 971 | — | 2026-6-26 | [{'customer': 'Melrose & Madison (AMZ)', 'revenue': 39184.64}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 25107.36}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 23650.0}, {'customer': 'Shades of Light', 'revenue': 17460.0}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 16329.25}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 16039.95}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 10662.5}, {'customer': 'Build Drop Ship EDI', 'revenue': 8137.5}, {'customer': 'Houzz.com-Auto EDI', 'revenue': 5987.5}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 5563.72}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 4050.0}, {'customer': 'Foundrylighting.com', 'revenue': 3162.5}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 2250.0}, {'customer': 'Lightology, LLC.com', 'revenue': 1930.0}, {'customer': 'Lighting Etc.', 'revenue': 1750.0}, {'customer': 'Lamps.com', 'revenue': 1627.5}, {'customer': 'Lightopia, LLC.', 'revenue': 1622.5}, {'customer': 'Interior Design House', 'revenue': 1500.0}, {'customer': 'Overstock.com, Inc-Auto EDI', 'revenue': 1250.0}, {'customer': "Fleming's of Cohasset, Inc.", 'revenue': 1250.0}, {'customer': 'Tout Le Monde Interiors LLC', 'revenue': 1152.0}, {'customer': 'Kendall Electric', 'revenue': 1000.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1000.0}, {'customer': 'Continental Lighting Corp.', 'revenue': 1000.0}, {'customer': "Horton's Home Lighting", 'revenue': 950.0}, {'customer': 'Cates Lighting at Elements', 'revenue': 750.0}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 750.0}, {'customer': 'Manasquan Lighting', 'revenue': 750.0}, {'customer': 'Wostbrock Home', 'revenue': 750.0}, {'customer': 'Ocean Pacific Lighting', 'revenue': 750.0}, {'customer': 'Brooke & Lou', 'revenue': 750.0}, {'customer': 'Wilson Fans And Lighting', 'revenue': 675.0}, {'customer': 'Connecticut Lighting Center', 'revenue': 675.0}, {'customer': 'RAINBOW LIGHTING INC', 'revenue': 600.0}, {'customer': 'Voss Designs', 'revenue': 576.0}, {'customer': 'Union Lighting & Home', 'revenue': 511.5}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 500.0}, {'customer': 'Dominion Electric', 'revenue': 500.0}, {'customer': 'Home Lighting of Frazer', 'revenue': 500.0}, {'customer': 'Gross Lighting & Home', 'revenue': 500.0}, {'customer': 'James and Company Ltd.', 'revenue': 500.0}, {'customer': 'Candelabra Light & Design.com DBA Meadow Blu', 'revenue': 500.0}, {'customer': 'Southern Lights', 'revenue': 482.5}, {'customer': 'Paramont-Evergreen Oak Inc.', 'revenue': 482.5}, {'customer': 'Raymond Desteiger, Inc.', 'revenue': 475.0}, {'customer': 'Fan & Lighting World', 'revenue': 475.0}, {'customer': 'Shop Freely LLC.com', 'revenue': 470.0}, {'customer': 'Del Mar Designs.com', 'revenue': 470.0}, {'customer': 'M&M Lighting Co', 'revenue': 465.0}, {'customer': '1 800 MY LAMPS.com', 'revenue': 465.0}, {'customer': 'Wilson Lighting - St Louis', 'revenue': 450.0}, {'customer': 'Progressive Lighting', 'revenue': 450.0}, {'customer': '2514004  Ontario Inc O/A iLITE', 'revenue': 429.29}, {'customer': 'Wage Lighting & Design', 'revenue': 425.0}, {'customer': 'Tide & Table', 'revenue': 400.0}, {'customer': 'Naples Lamp Shop', 'revenue': 375.0}, {'customer': 'Kate.H.Design', 'revenue': 313.0}, {'customer': 'Westend Interiors', 'revenue': 313.0}, {'customer': 'Stewart Design Group', 'revenue': 313.0}, {'customer': 'Moss Aaron', 'revenue': 313.0}, {'customer': 'Dianne Davant and Associates', 'revenue': 313.0}, {'customer': 'Fashion Light Center, LLC', 'revenue': 300.0}, {'customer': 'Koval Building & Plumbing Supply Co.', 'revenue': 288.0}, {'customer': 'Ashley Wells Design', 'revenue': 288.0}, {'customer': 'The Beach Home, LLC', 'revenue': 288.0}, {'customer': 'Blufish Designs', 'revenue': 288.0}, {'customer': 'Annie Baker Design', 'revenue': 288.0}, {'customer': 'River City Lighting', 'revenue': 266.05}, {'customer': 'Lighting By Fox, LLC', 'revenue': 250.0}, {'customer': 'Neenas Lighting', 'revenue': 250.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 250.0}, {'customer': 'Desert Lighting Solutions', 'revenue': 250.0}, {'customer': 'The Light House of Lewes', 'revenue': 250.0}, {'customer': 'Pine Lighting', 'revenue': 250.0}, {'customer': 'Scott Electric', 'revenue': 250.0}, {'customer': 'Decorum', 'revenue': 250.0}, {'customer': 'CoCo Curtain Studio', 'revenue': 250.0}, {'customer': 'Bayside Electric Supply', 'revenue': 250.0}, {'customer': 'Cregger Company, LLC', 'revenue': 250.0}, {'customer': 'Erwin Development, DBA The Lighting Studio', 'revenue': 250.0}, {'customer': 'Cayce Mill Supply Co.', 'revenue': 250.0}, {'customer': 'City Lights', 'revenue': 250.0}, {'customer': 'Coastal Lighting and Supply', 'revenue': 250.0}, {'customer': 'Illuminate Lighting Design, Formerly 17-90 Lighting Inc.', 'revenue': 250.0}, {'customer': 'U.S. 31 Supply Inc', 'revenue': 250.0}, {'customer': 'Rite Rug Co', 'revenue': 250.0}, {'customer': 'CES Aquisition LLC', 'revenue': 250.0}, {'customer': 'Pelican Equipment Rentals, Inc', 'revenue': 250.0}, {'customer': 'Logan Square DBA Studio 41', 'revenue': 250.0}, {'customer': 'Greer Lighting Center', 'revenue': 250.0}, {'customer': 'PAYNES GRAY', 'revenue': 250.0}, {'customer': 'Dulles Electric Supply', 'revenue': 250.0}, {'customer': 'Elektra Lights and Fans', 'revenue': 250.0}, {'customer': 'El Design', 'revenue': 250.0}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 250.0}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 250.0}, {'customer': 'King Electric Company Inc.', 'revenue': 250.0}, {'customer': 'Lighting & Lamps', 'revenue': 250.0}, {'customer': 'Biggins Lighting & Electric Su', 'revenue': 250.0}, {'customer': 'Lighting Emporium', 'revenue': 250.0}, {'customer': 'Lighting Showcase', 'revenue': 250.0}, {'customer': 'Alex Dee Home Accessories &Ltg', 'revenue': 250.0}, {'customer': 'Magnolia Lighting & Electric', 'revenue': 250.0}, {'customer': 'Premier Bath Lighting&Hardware', 'revenue': 250.0}, {'customer': 'Rittenhouse Electric Supply Co', 'revenue': 250.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 250.0}, {'customer': 'The Light Center', 'revenue': 250.0}, {'customer': 'The Light Post', 'revenue': 250.0}, {'customer': 'Lighting By Lavonne', 'revenue': 250.0}, {'customer': 'Cleveland Lighting', 'revenue': 250.0}, {'customer': 'Just Lights', 'revenue': 250.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 250.0}, {'customer': 'Retail Convergence.com, LP ASN (Rue La La)', 'revenue': 250.0}, {'customer': 'Inline Electric Supply', 'revenue': 250.0}, {'customer': 'Standard Electric', 'revenue': 250.0}, {'customer': 'Urban Lights', 'revenue': 250.0}, {'customer': 'North Coast Lighting', 'revenue': 242.5}, {'customer': 'Georgia Lighting', 'revenue': 232.5}, {'customer': 'Mayson Enterprise dba Aura Lighting', 'revenue': 232.5}, {'customer': "Graham's Living", 'revenue': 232.5}, {'customer': 'Galaxie Lighting', 'revenue': 232.5}, {'customer': 'Robinson Lighting Centre', 'revenue': 232.5}, {'customer': 'Littman Bros Lighting.com', 'revenue': 232.5}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 232.5}, {'customer': 'Haus Appeal LLC', 'revenue': 232.5}, {'customer': 'Tidewater Lighting & Design', 'revenue': 232.5}, {'customer': 'Aladdin Lighting & Supply, Inc', 'revenue': 232.5}, {'customer': 'Wilson Lighting of Naples', 'revenue': 225.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 225.0}, {'customer': "Efird's Interiors, Inc.", 'revenue': 225.0}, {'customer': 'RLA Lighting', 'revenue': 200.0}, {'customer': 'Made New Interiors and Decor, LLC', 'revenue': 175.0}, {'customer': 'Harbour Lighting LLC', 'revenue': 175.0}, {'customer': 'Prima Lighting', 'revenue': 125.0}, {'customer': 'The Glow Works Inc', 'revenue': 125.0}, {'customer': 'The Electrical &Plumbing Store', 'revenue': 86.8}, {'customer': 'Rhobin Delacruz Designs', 'revenue': 0.0}, {'customer': 'The Newburyport Lighting Co', 'revenue': 0.0}, {'customer': 'Haven and Dwell', 'revenue': 0.0}] | [{'item': '531-GA', 'desc': "Broche 6'' Antique Gold Sconce", 'available': 581}, {'item': '501-GA', 'desc': "Broche 8.5'' Antique Gold Sconce", 'available': 372}, {'item': '531-MT', 'desc': "Broche 6'' Matte White Sconce", 'available': 236}, {'item': '505-GA', 'desc': "Broche 16'' Antique Gold Semi Flush Mount", 'available': 212}, {'item': '531-SA', 'desc': "Broche 6'' Antique Silver Sconce", 'available': 210}, {'item': '517-GA_CEILING', 'desc': "Broche 24.5'' Antique Gold Semi Flush Mount", 'available': 203}, {'item': '517-GA', 'desc': "Broche 24.5'' Antique Gold Chandelier", 'available': 202}, {'item': '533-GA', 'desc': "Broche 27'' Antique Gold Chandelier", 'available': 172}, {'item': '519-GA_CEILING', 'desc': "Broche 30'' Antique Gold Semi Flush Mount", 'available': 150}, {'item': '519-GA', 'desc': "Broche 30'' Antique Gold Chandelier", 'available': 147}, {'item': '507-GA', 'desc': "Broche 24'' Antique Gold Semi Flush Mount", 'available': 142}, {'item': '566-MT', 'desc': "Broche 23'' Matte White Chandelier", 'available': 120}, {'item': '513-GA', 'desc': "Broche 14'' Antique Gold Chandelier", 'available': 113}, {'item': '513-GA_CEILING', 'desc': "Broche 14'' Antique Gold Semi Flush Mount", 'available': 113}, {'item': '534-MT', 'desc': "Broche 28'' Matte White Chandelier", 'available': 105}, {'item': '500W-MT', 'desc': "Broche 11'' Matte White Sconce", 'available': 100}, {'item': '500-MT', 'desc': "Broche 11'' Matte White Flush Mount", 'available': 100}, {'item': '510-GA', 'desc': "Broche 16'' Antique Gold Flush Mount", 'available': 95}, {'item': '514-GA', 'desc': "Broche 11'' Antique Gold Chandelier", 'available': 92}, {'item': '561-GA', 'desc': "Broche 8.25'' Antique Gold Sconce", 'available': 92}, {'item': '562-GA', 'desc': "Broche 12'' Antique Gold Sconce", 'available': 87}, {'item': '566-CT', 'desc': "Broche 23'' Champagne Green Tea Chandelier", 'available': 83}, {'item': '568-GA', 'desc': "Broche 32'' Antique Gold Chandelier", 'available': 83}, {'item': '566-GA', 'desc': "Broche 23'' Antique Gold Chandelier", 'available': 82}, {'item': '562-MT', 'desc': "Broche 12'' Matte White Sconce", 'available': 74}, {'item': '501-SA', 'desc': "Broche 8.5'' Antique Silver Sconce", 'available': 70}, {'item': '517-MT_CEILING', 'desc': "Broche 24.5'' Matte White Semi Flush Mount", 'available': 70}, {'item': '517-MT', 'desc': "Broche 24.5'' Matte White Chandelier", 'available': 70}, {'item': '537-GA', 'desc': "Broche 53.5'' Antique Gold Linear Chandelier", 'available': 69}, {'item': '531-OP-MT', 'desc': "Broche 6'' Matte White Sconce", 'available': 64}, {'item': '511-MT', 'desc': "Broche 8'' Matte White Sconce", 'available': 56}, {'item': 'BRH-M520-GA', 'desc': "Broche 20'' Antique Gold Mirror", 'available': 56}, {'item': '510-MT', 'desc': "Broche 16'' Matte White Flush Mount", 'available': 55}, {'item': '517-SA_CEILING', 'desc': "Broche 24.5'' Antique Silver Semi Flush Mount", 'available': 54}, {'item': '516-GA', 'desc': "Broche 16'' Antique Gold Chandelier", 'available': 54}, {'item': '517-SA', 'desc': "Broche 24.5'' Antique Silver Chandelier", 'available': 54}, {'item': '564-GA', 'desc': "Broche 18'' Antique Gold Pendant", 'available': 52}, {'item': '531-OP-SA', 'desc': "Broche 6'' Antique Silver Sconce", 'available': 50}, {'item': '501-EB', 'desc': "Broche 8.5'' English Bronze Sconce", 'available': 49}, {'item': '518-SA', 'desc': "Broche 24'' Antique Silver Chandelier", 'available': 48}, {'item': '560-GA', 'desc': "Broche 20.75'' Antique Gold Semi Flush Mount", 'available': 48}, {'item': '518-GA', 'desc': "Broche 24'' Antique Gold Chandelier", 'available': 48}, {'item': '573-OP-SA', 'desc': "Broche 25'' Antique Silver Bathroom Vanity", 'available': 47}, {'item': '500W-GA', 'desc': "Broche 11'' Antique Gold Sconce", 'available': 46}, {'item': '500-GA', 'desc': "Broche 11'' Antique Gold Flush Mount", 'available': 46}, {'item': '505-SA', 'desc': "Broche 16'' Antique Silver Semi Flush Mount", 'available': 44}, {'item': 'BRH-M520-MT', 'desc': "Broche 20'' Matte White Mirror", 'available': 42}, {'item': '504-EB-GA', 'desc': "Broche 16'' English Bronze + Antique Gold Chandelier", 'available': 41}, {'item': '503-GA-SA', 'desc': "Broche 18'' Antique Gold + Antique Silver Bathroom Vanity", 'available': 41}, {'item': '533-MT', 'desc': "Broche 27'' Matte White Chandelier", 'available': 40}, {'item': 'BRH-M520-SA', 'desc': "Broche 20'' Antique Silver Mirror", 'available': 40}, {'item': '571-OP-MT', 'desc': "Broche 6.5'' Matte White Sconce", 'available': 38}, {'item': '511-SA', 'desc': "Broche 8'' Antique Silver Sconce", 'available': 37}, {'item': '534-GA', 'desc': "Broche 28'' Antique Gold Chandelier", 'available': 35}, {'item': 'BRH-M530-GA', 'desc': "Broche 30'' Antique Gold Mirror", 'available': 33}, {'item': '533-SA', 'desc': "Broche 27'' Antique Silver Chandelier", 'available': 30}, {'item': '506-EB-GA', 'desc': "Broche 21'' English Bronze + Antique Gold Chandelier", 'available': 29}, {'item': 'BRH-M524-MT', 'desc': "Broche 24'' Matte White Mirror", 'available': 29}, {'item': '571-OP-GA', 'desc': "Broche 6.5'' Antique Gold Sconce", 'available': 28}, {'item': 'BRH-M530-SA', 'desc': "Broche 30'' Antique Silver Mirror", 'available': 27}, {'item': '566-SA', 'desc': "Broche 23'' Antique Silver Chandelier", 'available': 26}, {'item': 'BRH-M524-GA', 'desc': "Broche 24'' Antique Gold Mirror", 'available': 25}, {'item': '561-MT', 'desc': "Broche 8.25'' Matte White Sconce", 'available': 24}, {'item': '561-SA', 'desc': "Broche 8.25'' Antique Silver Sconce", 'available': 24}, {'item': '565-MT_CEILING', 'desc': "Broche 9'' Matte White Semi Flush Mount", 'available': 23}, {'item': '535-MT', 'desc': "Broche 18'' LED Matte White Chandelier", 'available': 23}, {'item': '535-MT_CEILING', 'desc': "Broche 18'' LED Matte White Semi Flush Mount", 'available': 23}, {'item': '515-GA', 'desc': "Broche 29'' Antique Gold Chandelier", 'available': 22}, {'item': '565-MT', 'desc': "Broche 9'' Matte White Chandelier", 'available': 22}, {'item': 'BRH-M530-MT', 'desc': "Broche 30'' Matte White Mirror", 'available': 22}, {'item': '537-SA', 'desc': "Broche 53.5'' Antique Silver Linear Chandelier", 'available': 22}, {'item': '501-MT', 'desc': "Broche 8.5'' Matte White Sconce", 'available': 21}, {'item': '560-MT', 'desc': "Broche 20.75'' Matte White Semi Flush Mount", 'available': 20}, {'item': '534-SA', 'desc': "Broche 28'' Antique Silver Chandelier", 'available': 20}, {'item': '507-SA', 'desc': "Broche 24'' Antique Silver Semi Flush Mount", 'available': 18}, {'item': '519-SA', 'desc': "Broche 30'' Antique Silver Chandelier", 'available': 18}, {'item': '562-SA', 'desc': "Broche 12'' Antique Silver Sconce", 'available': 18}, {'item': '519-SA_CEILING', 'desc': "Broche 30'' Antique Silver Semi Flush Mount", 'available': 17}, {'item': '535-SA', 'desc': "Broche 18'' LED Antique Silver Chandelier", 'available': 16}, {'item': 'BRH-M524-SA', 'desc': "Broche 24'' Antique Silver Mirror", 'available': 16}, {'item': '513-SA', 'desc': "Broche 14'' Antique Silver Chandelier", 'available': 16}, {'item': '535-SA_CEILING', 'desc': "Broche 18'' LED Antique Silver Semi Flush Mount", 'available': 16}, {'item': '569-MT', 'desc': "Broche 42'' Matte White Chandelier", 'available': 15}, {'item': '513-SA_CEILING', 'desc': "Broche 14'' Antique Silver Semi Flush Mount", 'available': 15}, {'item': '508-GA-SA', 'desc': "Broche 31'' Antique Gold + Antique Silver Bathroom Vanity", 'available': 15}, {'item': '569-GA', 'desc': "Broche 42'' Antique Gold Chandelier", 'available': 14}, {'item': '515-SA', 'desc': "Broche 29'' Antique Silver Chandelier", 'available': 13}, {'item': '567-MT', 'desc': "Broche 50.5'' Matte White Linear Chandelier", 'available': 12}, {'item': '536-GA', 'desc': "Broche 24'' Antique Gold Chandelier", 'available': 12}, {'item': '536-GA_CEILING', 'desc': "Broche 24'' Antique Gold Semi Flush Mount", 'available': 12}, {'item': '568-MT', 'desc': "Broche 32'' Matte White Chandelier", 'available': 11}, {'item': '500-SA', 'desc': "Broche 11'' Antique Silver Flush Mount", 'available': 11}, {'item': '511-GA', 'desc': "Broche 8'' Antique Gold Sconce", 'available': 11}, {'item': '561-CT', 'desc': "Broche 8.25'' Champagne Green Tea Sconce", 'available': 11}, {'item': 'BRH-M546-SA', 'desc': "Broche 46.75'' Antique Silver Mirror", 'available': 9}, {'item': '533-CT', 'desc': "Broche 27'' Champagne Green Tea Chandelier", 'available': 9}, {'item': '500W-SA', 'desc': "Broche 11'' Antique Silver Sconce", 'available': 9}, {'item': '564-MT', 'desc': "Broche 18'' Matte White Pendant", 'available': 8}, {'item': '536-MT', 'desc': "Broche 24'' Matte White Chandelier", 'available': 8}, {'item': 'BRH-M546-MT', 'desc': "Broche 46.75'' Matte White Mirror", 'available': 8}, {'item': '536-MT_CEILING', 'desc': "Broche 24'' Matte White Semi Flush Mount", 'available': 8}, {'item': '538-MT', 'desc': "Broche 33.5'' Matte White Chandelier", 'available': 6}, {'item': '538-SA_CEILING', 'desc': "Broche 33.5'' Antique Silver Semi Flush Mount", 'available': 6}, {'item': '538-MT_CEILING', 'desc': "Broche 33.5'' Matte White Semi Flush Mount", 'available': 6}, {'item': 'BRH-M546-GA', 'desc': "Broche 46.75'' Antique Gold Mirror", 'available': 6}, {'item': '569-SA', 'desc': "Broche 42'' Antique Silver Chandelier", 'available': 6}, {'item': '537-MT', 'desc': "Broche 53.5'' Matte White Linear Chandelier", 'available': 5}, {'item': '535-GA', 'desc': "Broche 18'' LED Antique Gold Chandelier", 'available': 5}, {'item': '565-SA_CEILING', 'desc': "Broche 9'' Antique Silver Semi Flush Mount", 'available': 5}, {'item': '538-SA', 'desc': "Broche 33.5'' Antique Silver Chandelier", 'available': 5}, {'item': '519-MT_CEILING', 'desc': "Broche 30'' Matte White Semi Flush Mount", 'available': 5}, {'item': '504-MT', 'desc': "Broche 16'' Matte White Chandelier", 'available': 4}, {'item': '536-SA', 'desc': "Broche 24'' Antique Silver Chandelier", 'available': 3}, {'item': '506-MT', 'desc': "Broche 21'' Matte White Chandelier", 'available': 3}, {'item': '538-GA', 'desc': "Broche 33.5'' Antique Gold Chandelier", 'available': 3}, {'item': '538-GA_CEILING', 'desc': "Broche 33.5'' Antique Gold Semi Flush Mount", 'available': 3}, {'item': '565-GA_CEILING', 'desc': "Broche 9'' Antique Gold Semi Flush Mount", 'available': 3}, {'item': '536-SA_CEILING', 'desc': "Broche 24'' Antique Silver Semi Flush Mount", 'available': 3}, {'item': '565-SA', 'desc': "Broche 9'' Antique Silver Chandelier", 'available': 2}, {'item': '568-SA', 'desc': "Broche 32'' Antique Silver Chandelier", 'available': 2}, {'item': '535-GA_CEILING', 'desc': "Broche 18'' LED Antique Gold Semi Flush Mount", 'available': 2}, {'item': '519-MT', 'desc': "Broche 30'' Matte White Chandelier", 'available': 1}] |
| ADD-317-AG-AU | Addis 51.75'' Aged Brass Linear Chandelier | ADDIS | 207,762.55 | 183 | — | 2026-6-29 | [{'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 14843.0}, {'customer': 'Shades of Light', 'revenue': 11291.1}, {'customer': 'Light Lab Design', 'revenue': 9220.05}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 8826.24}, {'customer': 'Lighting, Inc', 'revenue': 6409.5}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 6112.84}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 4996.0}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 4955.21}, {'customer': 'Georgia Lighting', 'revenue': 4171.5}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 4114.89}, {'customer': 'Union Lighting & Furnishings', 'revenue': 3916.8}, {'customer': 'Reflections L+M', 'revenue': 3747.0}, {'customer': "Graham's Living", 'revenue': 3624.21}, {'customer': 'Lighting Superstore', 'revenue': 3597.0}, {'customer': 'Capitol Lighting-ASN', 'revenue': 3507.3}, {'customer': "Hinkley's Lighting Factory", 'revenue': 3484.71}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 3147.48}, {'customer': 'Lando Lighting', 'revenue': 3107.4}, {'customer': 'Urban Lights', 'revenue': 2598.0}, {'customer': "Elaine Everett's Lighting", 'revenue': 2448.0}, {'customer': 'Light Source Lighting', 'revenue': 2448.0}, {'customer': 'Lights Unlimited', 'revenue': 2448.0}, {'customer': 'Build Drop Ship EDI', 'revenue': 2438.84}, {'customer': 'Foundrylighting.com', 'revenue': 2367.57}, {'customer': 'Butler Electric Supply', 'revenue': 2325.6}, {'customer': 'IB Lighting Supply', 'revenue': 2298.0}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 2217.57}, {'customer': 'First Coast Lighting & Fans', 'revenue': 2217.57}, {'customer': 'Universal Lights, Inc.', 'revenue': 2208.3}, {'customer': 'Elements', 'revenue': 1794.03}, {'customer': 'Y Factor Studio, LLC', 'revenue': 1624.0}, {'customer': 'The Lighting Marketplace DBA Fixture Farm', 'revenue': 1494.0}, {'customer': 'The Lighting Shoppe', 'revenue': 1425.15}, {'customer': 'Holland Custom Designs', 'revenue': 1374.0}, {'customer': 'Li Luxe', 'revenue': 1335.0}, {'customer': 'Her Home Design Boutique', 'revenue': 1322.0}, {'customer': 'Farrell Architecture', 'revenue': 1321.0}, {'customer': 'Houston LIght Bulb CO', 'revenue': 1299.0}, {'customer': 'M&M Lighting Co', 'revenue': 1299.0}, {'customer': 'Daniel House Club', 'revenue': 1299.0}, {'customer': 'Lighting By Fox, LLC', 'revenue': 1299.0}, {'customer': 'Hampton Home Dinettes', 'revenue': 1299.0}, {'customer': 'Accent Lighting Galleries', 'revenue': 1299.0}, {'customer': 'Wiseway Supply', 'revenue': 1299.0}, {'customer': 'The Jarrell Company', 'revenue': 1299.0}, {'customer': 'Posh HB LLC DBA Posh Home and Bath', 'revenue': 1299.0}, {'customer': 'Lighting World Decorator', 'revenue': 1299.0}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 1299.0}, {'customer': 'Cates Lighting at Elements', 'revenue': 1299.0}, {'customer': 'Design Lighting Sales, Ltd.', 'revenue': 1299.0}, {'customer': 'Idlewood Electric Supply', 'revenue': 1299.0}, {'customer': 'Front Street Lighting', 'revenue': 1299.0}, {'customer': 'House of Lights Inc', 'revenue': 1208.07}, {'customer': 'Illuminating Expressions', 'revenue': 1208.07}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 1208.07}, {'customer': 'Ultimate USA Bulb DBA', 'revenue': 1208.07}, {'customer': 'Gross Lighting & Home', 'revenue': 1208.07}, {'customer': 'The Brecher Company', 'revenue': 1208.07}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 1208.07}, {'customer': 'Lightstyle of Orlando', 'revenue': 1208.07}, {'customer': 'Wilson Lighting of Naples', 'revenue': 1169.1}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 1169.1}, {'customer': 'The Lighting Design Co.', 'revenue': 1149.0}, {'customer': 'Kirby Risk Corporation', 'revenue': 1149.0}, {'customer': 'Anthology Lighting', 'revenue': 1149.0}, {'customer': 'Brand Lighting Corporation', 'revenue': 1149.0}, {'customer': 'Paramont-Evergreen Oak Inc.', 'revenue': 1149.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 1149.0}, {'customer': 'Dominion Electric', 'revenue': 1149.0}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1149.0}, {'customer': 'LyteWorks', 'revenue': 1149.0}, {'customer': 'Lightopia, LLC.', 'revenue': 1149.0}, {'customer': 'Lighting By Design', 'revenue': 1149.0}, {'customer': 'Fan & Lighting World', 'revenue': 1149.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 1149.0}, {'customer': 'Lighting Solutions', 'revenue': 1099.0}, {'customer': 'White House Furniture Inc.', 'revenue': 1099.0}, {'customer': 'The Light House', 'revenue': 1099.0}, {'customer': 'Northwest Interiors', 'revenue': 1099.0}, {'customer': '43rd Street Lighting, Inc.', 'revenue': 1068.57}, {'customer': 'One Stop Lighting', 'revenue': 1068.57}, {'customer': 'Curb Ease, LLC dba Fixture This', 'revenue': 1068.57}, {'customer': "Graham's Lighting", 'revenue': 1068.57}, {'customer': 'House of Carpets, Inc.', 'revenue': 1068.57}, {'customer': 'Watts Current Inc.', 'revenue': 1068.57}, {'customer': "Mahlander's Appliance Lighting", 'revenue': 1068.57}, {'customer': 'The Light Brothers', 'revenue': 1068.57}, {'customer': 'Krell Lighting & Electric Supp', 'revenue': 1034.1}, {'customer': 'Progressive Lighting', 'revenue': 1034.1}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 1034.1}, {'customer': 'Sun Lighting', 'revenue': 1034.1}, {'customer': 'Premier Lighting', 'revenue': 1022.07}, {'customer': 'LDB Holdings, LLC', 'revenue': 989.1}, {'customer': 'Marx Fireplace and Lighting', 'revenue': 779.4}, {'customer': 'ABC Creations', 'revenue': 689.4}, {'customer': 'Plumb Supply Co', 'revenue': 0.0}, {'customer': 'Lightology, LLC.com', 'revenue': 0.0}, {'customer': 'Shades of Light', 'revenue': 0.0}, {'customer': 'Dolan NW LLC', 'revenue': 0.0}, {'customer': 'Lighting By Design - Dec Den', 'revenue': 0.0}, {'customer': 'Garden of the Gods Lighting', 'revenue': 0.0}, {'customer': 'Hye Lighting', 'revenue': 0.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 0.0}, {'customer': 'Teela Bennett Design', 'revenue': 0.0}, {'customer': 'Elektra Lights and Fans', 'revenue': 0.0}, {'customer': 'Lighting First - Bonita', 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
| ADD-317-AG-AM | Addis 51.75'' Aged Brass Linear Chandelier | ADDIS | 188,094.15 | 162 | — | 2026-8-6 | [{'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 12506.66}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 11995.83}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 9823.16}, {'customer': 'Build Drop Ship EDI', 'revenue': 8961.06}, {'customer': 'Foundrylighting.com', 'revenue': 7333.14}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 5806.53}, {'customer': "Hinkley's Lighting Factory", 'revenue': 5458.74}, {'customer': 'Shades of Light', 'revenue': 5440.5}, {'customer': 'Daniel House Club', 'revenue': 5046.0}, {'customer': 'Lightopia, LLC.', 'revenue': 4890.12}, {'customer': 'Lightology, LLC.com', 'revenue': 4805.07}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 4015.31}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 3897.0}, {'customer': 'Hudson Parc Lighting and Design', 'revenue': 2357.07}, {'customer': 'CES Aquisition LLC', 'revenue': 2298.0}, {'customer': 'Imagine More', 'revenue': 2276.64}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 2203.2}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 1911.89}, {'customer': 'Union Lighting & Furnishings', 'revenue': 1838.4}, {'customer': 'Elements', 'revenue': 1713.6}, {'customer': 'Freestyle Interiors', 'revenue': 1624.0}, {'customer': 'Luxe Living Interiors', 'revenue': 1494.0}, {'customer': 'Roz Murphy Design', 'revenue': 1436.0}, {'customer': 'The Sitting Room', 'revenue': 1436.0}, {'customer': 'Tiffany Skilling Interiors', 'revenue': 1322.0}, {'customer': 'J&L Interiors', 'revenue': 1321.0}, {'customer': 'Coffman Home Decor, LLC', 'revenue': 1299.0}, {'customer': 'Lifestyles Stores, Inc', 'revenue': 1299.0}, {'customer': 'Stewart Lighting, Inc.', 'revenue': 1299.0}, {'customer': 'Gateway Lighting & Design', 'revenue': 1299.0}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 1299.0}, {'customer': 'Urban Lights', 'revenue': 1299.0}, {'customer': 'Robinson Lighting Centre', 'revenue': 1299.0}, {'customer': 'Hall Electric Co, Inc', 'revenue': 1299.0}, {'customer': 'Plumbing Distributors Inc.', 'revenue': 1299.0}, {'customer': 'Lighting Getz DBA Hello Lighting', 'revenue': 1299.0}, {'customer': 'Norwood Furniture Sales', 'revenue': 1299.0}, {'customer': 'Chroma Home, LLC', 'revenue': 1299.0}, {'customer': 'PAYNES GRAY', 'revenue': 1299.0}, {'customer': 'The Jarrell Company', 'revenue': 1299.0}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 1299.0}, {'customer': 'Lucia Lighting', 'revenue': 1299.0}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 1299.0}, {'customer': 'Littman Bros Lighting', 'revenue': 1299.0}, {'customer': 'Overstock.com, Inc-Auto EDI', 'revenue': 1299.0}, {'customer': 'Kathy Kuo Home', 'revenue': 1214.56}, {'customer': 'Mountain Lighting & Dsgn Ctr', 'revenue': 1208.07}, {'customer': 'The Saltbox', 'revenue': 1208.07}, {'customer': 'Lights on Design', 'revenue': 1208.07}, {'customer': 'Lightstyle of Orlando', 'revenue': 1208.07}, {'customer': 'First Coast Lighting & Fans', 'revenue': 1208.07}, {'customer': 'Pine Lighting', 'revenue': 1195.08}, {'customer': 'Progressive Lighting', 'revenue': 1169.1}, {'customer': 'Royal Lighting', 'revenue': 1169.1}, {'customer': 'Metro Showroom West County', 'revenue': 1169.1}, {'customer': 'Wilson Fans And Lighting', 'revenue': 1169.1}, {'customer': 'Capitol Lighting-ASN', 'revenue': 1169.1}, {'customer': 'Horchow - DIP 20-32519', 'revenue': 1149.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 1149.0}, {'customer': 'JCM Lighting and Design, DBA The Local Lighting Shop', 'revenue': 1149.0}, {'customer': 'Southern Lights', 'revenue': 1149.0}, {'customer': 'Gerrie Electric', 'revenue': 1149.0}, {'customer': "Wilkinson's House of Lights", 'revenue': 1149.0}, {'customer': 'Dominion Electric', 'revenue': 1149.0}, {'customer': 'Coast Lighting', 'revenue': 1149.0}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 1149.0}, {'customer': 'Lighting By Fox, LLC', 'revenue': 1149.0}, {'customer': 'North Valley Fans and Blinds', 'revenue': 1149.0}, {'customer': 'ARC DEST/ FOUNDRY NY', 'revenue': 1149.0}, {'customer': 'Ellen Lighting & Hardware', 'revenue': 1149.0}, {'customer': 'Furniture Land South', 'revenue': 1149.0}, {'customer': 'Rite Rug Co', 'revenue': 1149.0}, {'customer': 'Northeast Electrical formerly Rockingham Electrical Supply', 'revenue': 1149.0}, {'customer': 'William Hart Designs, LLC', 'revenue': 1149.0}, {'customer': 'R. Bdelaa Lighting', 'revenue': 1149.0}, {'customer': 'Newton Electrical Company', 'revenue': 1099.0}, {'customer': 'Lighting By Design - Exton PA', 'revenue': 1099.0}, {'customer': 'Chloe Winston Lighting Design', 'revenue': 1068.57}, {'customer': 'Wyckoff Lighting', 'revenue': 1068.57}, {'customer': 'Posh Lighting', 'revenue': 1068.57}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 1068.57}, {'customer': 'Reflections L+M', 'revenue': 1034.1}, {'customer': 'Prima Lighting', 'revenue': 1034.1}, {'customer': 'Lamps.com', 'revenue': 1023.17}, {'customer': 'Kaleidoscope', 'revenue': 1022.07}, {'customer': "Graham's Living", 'revenue': 1022.07}, {'customer': 'Rainbow Lighting II LLC (NY)', 'revenue': 919.2}, {'customer': 'Courtesy Lighting', 'revenue': 824.25}, {'customer': 'M&M Lighting Co', 'revenue': 649.5}, {'customer': 'Moreau Enterprises/Aggieland', 'revenue': 649.5}, {'customer': 'Hye Lighting', 'revenue': 574.5}, {'customer': 'Nova Lighting', 'revenue': 0.0}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 0.0}, {'customer': 'Shades of Light', 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
| ARC-1919-GA-CL-MWP | Arcadia 46.25'' Antique Gold Chandelier | COL70 | 180,660.39 | 110 | — | 2026-7-27 | [{'customer': 'Progressive Lighting', 'revenue': 18694.8}, {'customer': 'Build Drop Ship EDI', 'revenue': 13864.72}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 13063.83}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 11829.35}, {'customer': 'Connecticut Lighting Center', 'revenue': 11322.9}, {'customer': 'Georgia Lighting', 'revenue': 9626.97}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 7104.64}, {'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 6050.52}, {'customer': "Carol's Lighting & Fan Shop", 'revenue': 5249.07}, {'customer': 'TRI-Supply LLC', 'revenue': 5193.0}, {'customer': 'Elements', 'revenue': 4746.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 3444.0}, {'customer': 'Notoco-Baton Rouge', 'revenue': 3390.0}, {'customer': 'The Brecher Company', 'revenue': 3325.35}, {'customer': 'House of Carpets, Inc.', 'revenue': 3274.5}, {'customer': 'The Parker Company', 'revenue': 2187.0}, {'customer': 'FS DESIGN  GROUP', 'revenue': 2012.0}, {'customer': 'J&L Interiors', 'revenue': 2012.0}, {'customer': 'Foundrylighting.com', 'revenue': 1999.0}, {'customer': 'M&M Lighting Co', 'revenue': 1999.0}, {'customer': 'Retail Convergence.com, LP ASN (Rue La La)', 'revenue': 1999.0}, {'customer': 'One Stop Lighting', 'revenue': 1999.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 1999.0}, {'customer': 'O&I Design Group, LLC DBA The Elements', 'revenue': 1949.0}, {'customer': 'Lighting, Inc', 'revenue': 1799.1}, {'customer': 'Lighting Superstore', 'revenue': 1749.0}, {'customer': 'PC Building Materials', 'revenue': 1749.0}, {'customer': 'Universal Lights, Inc.', 'revenue': 1749.0}, {'customer': 'Elan Studio Lighting', 'revenue': 1749.0}, {'customer': 'Broad Street Interiors', 'revenue': 1749.0}, {'customer': 'Home Depot-ASN', 'revenue': 1695.0}, {'customer': 'Posh Places', 'revenue': 1695.0}, {'customer': 'Net Retailers dba Luxe Decor', 'revenue': 1695.0}, {'customer': 'Coastal Lighting Supply', 'revenue': 1695.0}, {'customer': 'Armstrong Supply Co.', 'revenue': 1695.0}, {'customer': 'Royce Collection Inc.', 'revenue': 1695.0}, {'customer': 'Farreys Wholesale', 'revenue': 1695.0}, {'customer': 'Magnolia Lighting & Electric', 'revenue': 1695.0}, {'customer': 'Lighting Efx', 'revenue': 1626.57}, {'customer': 'Lightology, LLC.com', 'revenue': 1626.57}, {'customer': "Graham's Living", 'revenue': 1576.35}, {'customer': 'Quinn Wholesale dba Lamp Outlet', 'revenue': 1576.35}, {'customer': 'Rittenhouse Electric Supply Co', 'revenue': 1576.35}, {'customer': 'Alibaba Lighting & Furniture', 'revenue': 1576.35}, {'customer': 'We Got Lites, Inc.', 'revenue': 1576.35}, {'customer': 'Pine Grove Electrical Supply', 'revenue': 1576.35}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 1574.1}, {'customer': 'The Lighting Warehouse', 'revenue': 1525.5}, {'customer': 'Lighting & Lamps', 'revenue': 1224.3}, {'customer': 'Wage Lighting & Design', 'revenue': 1186.5}, {'customer': 'Plumbing Overstock, LLC', 'revenue': 0.0}] | [{'item': 'ARC-1900-SA-CL-MWP', 'desc': "Arcadia 15'' Antique Silver Semi Flush Mount", 'available': 42}, {'item': 'ARC-1900-GA-CL-MWP', 'desc': "Arcadia 15'' Antique Gold Semi Flush Mount", 'available': 24}, {'item': 'ARC-1909-SA-CL-MWP', 'desc': "Arcadia 32.5'' Antique Silver Chandelier", 'available': 21}, {'item': 'ARC-1917-SA-CL-MWP', 'desc': "Arcadia 24'' Antique Silver Chandelier", 'available': 19}, {'item': 'ARC-1908-SA-CL-MWP', 'desc': "Arcadia 26.75'' Antique Silver Chandelier", 'available': 17}, {'item': 'ARC-1902-GA-CL-MWP', 'desc': "Arcadia 11.25'' Antique Gold Sconce", 'available': 17}, {'item': 'ARC-1905-SA-CL-MWP', 'desc': "Arcadia 23.5'' Antique Silver Chandelier", 'available': 17}, {'item': 'ARC-1917-GA-CL-MWP', 'desc': "Arcadia 24'' Antique Gold Chandelier", 'available': 16}, {'item': 'ARC-1902-SA-CL-MWP', 'desc': "Arcadia 11.25'' Antique Silver Sconce", 'available': 15}, {'item': 'ARC-1905-GA-CL-MWP', 'desc': "Arcadia 23.5'' Antique Gold Chandelier", 'available': 12}, {'item': 'ARC-1907-SA-CL-MWP', 'desc': "Arcadia 18'' Antique Silver Chandelier", 'available': 12}, {'item': 'ARC-1929-GA-CL-MWP', 'desc': "Arcadia 61'' Antique Gold Chandelier", 'available': 11}, {'item': 'ARC-1908-GA-CL-MWP', 'desc': "Arcadia 26.75'' Antique Gold Chandelier", 'available': 9}, {'item': 'ARC-1929-SA-CL-MWP', 'desc': "Arcadia 61'' Antique Silver Chandelier", 'available': 7}, {'item': 'ARC-1919-SA-CL-MWP', 'desc': "Arcadia 46.25'' Antique Silver Chandelier", 'available': 5}] |
| HAY-1409-PN | Hayes 40.5'' Polished Nickel Chandelier | HAYES | 177,252.20 | 87 | — | 2026-7-14 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 16207.38}, {'customer': 'Build Drop Ship EDI', 'revenue': 15702.51}, {'customer': 'Meridien Marketing and Logisti', 'revenue': 15493.0}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 7404.17}, {'customer': 'Anthology Lighting', 'revenue': 6247.0}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 6166.47}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 5932.16}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 5775.06}, {'customer': 'Lighting, Inc', 'revenue': 5397.3}, {'customer': 'Midwest Lighting Solutions', 'revenue': 4598.0}, {'customer': 'Cleveland Lighting', 'revenue': 4135.55}, {'customer': 'Lighting First - Bonita', 'revenue': 4090.57}, {'customer': 'Fan & Lighting World', 'revenue': 3998.0}, {'customer': 'Robinson Lighting Centre', 'revenue': 3998.0}, {'customer': 'Wilson Lighting of Naples', 'revenue': 3598.2}, {'customer': 'Elements', 'revenue': 3370.4}, {'customer': 'Beckland Creations LLC', 'revenue': 2889.32}, {'customer': 'LF Design', 'revenue': 2499.0}, {'customer': 'Earth and Images', 'revenue': 2499.0}, {'customer': 'Denali Lighting', 'revenue': 2299.0}, {'customer': 'CAI Designs', 'revenue': 2299.0}, {'customer': 'Franklin Lighting', 'revenue': 2299.0}, {'customer': 'Gallery of Lighting', 'revenue': 2299.0}, {'customer': 'Lucia Lighting', 'revenue': 2299.0}, {'customer': 'Acker Bryant Design', 'revenue': 2299.0}, {'customer': 'The Lighting Shoppe', 'revenue': 2249.0}, {'customer': 'Tazz Lighting, Inc.', 'revenue': 2249.0}, {'customer': 'Endacott Lighting', 'revenue': 2249.0}, {'customer': 'Hobrecht Lighting Co., Inc.', 'revenue': 2249.0}, {'customer': 'Universal Lamps', 'revenue': 2249.0}, {'customer': 'Suburban Wholesale Lighting', 'revenue': 2249.0}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 2133.86}, {'customer': 'Lightology, LLC.com', 'revenue': 2091.57}, {'customer': 'Littman Bros Lighting', 'revenue': 2091.57}, {'customer': 'Fort Worth Lighting', 'revenue': 2091.57}, {'customer': 'W.T. Lighting', 'revenue': 2069.1}, {'customer': 'The Lighting Warehouse', 'revenue': 2024.1}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 1999.0}, {'customer': 'Beautiful Things', 'revenue': 1999.0}, {'customer': 'ARC DEST/ FOUNDRY NY', 'revenue': 1999.0}, {'customer': 'Village Lighting & Supply, Inc', 'revenue': 1859.07}, {'customer': "Hinkley's Lighting Factory", 'revenue': 1859.07}, {'customer': 'Shades of Light', 'revenue': 1799.1}, {'customer': 'Progressive Lighting', 'revenue': 1799.1}, {'customer': 'Metro Showroom West County', 'revenue': 1799.1}, {'customer': 'Lando Lighting', 'revenue': 1199.4}, {'customer': 'Naples Lamp Shop', 'revenue': 1149.5}, {'customer': 'Lowes Companies , Inc', 'revenue': 0.0}] | [{'item': 'HAY-1402-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 102}, {'item': 'HAY-1401-AG', 'desc': "Hayes 8'' Aged Brass Chandelier", 'available': 75}, {'item': 'HAY-1402-AG', 'desc': "Hayes 7.5'' Aged Brass Sconce", 'available': 61}, {'item': 'HAY-1411-PN', 'desc': "Hayes 7.5'' Polished Nickel Sconce", 'available': 39}, {'item': 'HAY-1401-PN', 'desc': "Hayes 8'' Polished Nickel Chandelier", 'available': 33}, {'item': 'HAY-1400-AG', 'desc': "Hayes 16'' Aged Brass Flush Mount", 'available': 30}, {'item': 'HAY-1409-AG', 'desc': "Hayes 40.5'' Aged Brass Chandelier", 'available': 29}, {'item': 'HAY-1407-PN', 'desc': "Hayes 28'' Polished Nickel Chandelier", 'available': 28}, {'item': 'HAY-1407-AG', 'desc': "Hayes 28'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1405-AG', 'desc': "Hayes 22'' Aged Brass Chandelier", 'available': 26}, {'item': 'HAY-1403-AG', 'desc': "Hayes 18'' Aged Brass Flush Mount", 'available': 24}, {'item': 'HAY-1403-PN', 'desc': "Hayes 18'' Polished Nickel Flush Mount", 'available': 17}, {'item': 'HAY-1413-PN', 'desc': "Hayes 23.5'' Polished Nickel Bathroom Vanity", 'available': 12}, {'item': 'HAY-1405-PN', 'desc': "Hayes 22'' Polished Nickel Chandelier", 'available': 12}, {'item': 'HAY-1400-PN', 'desc': "Hayes 16'' Polished Nickel Flush Mount", 'available': 10}, {'item': 'HAY-1415-PN', 'desc': "Hayes 31.5'' Polished Nickel Bathroom Vanity", 'available': 9}, {'item': 'HAY-1417-PN', 'desc': "Hayes 50'' Polished Nickel Linear Chandelier", 'available': 8}, {'item': 'HAY-1415-AG', 'desc': "Hayes 31.5'' Aged Brass Bathroom Vanity", 'available': 8}, {'item': 'HAY-1413-AG', 'desc': "Hayes 23.5'' Aged Brass Bathroom Vanity", 'available': 6}, {'item': 'HAY-1419-AG', 'desc': "Hayes 24'' Aged Brass Chandelier", 'available': 1}] |
| ADD-308-AG-WH | Addis 22'' Aged Brass Chandelier | ADDIS | 136,284.81 | 234 | — | 2026-6-29 | [{'customer': 'Ferguson Entrprise-Hampton-ASN', 'revenue': 11495.62}, {'customer': 'Lighting New York-Auto EDI', 'revenue': 8489.15}, {'customer': 'Build Drop Ship EDI', 'revenue': 7613.91}, {'customer': 'Y Design/Lumens, Inc.com-ASN', 'revenue': 6932.23}, {'customer': 'Wayfair.com-Auto EDI', 'revenue': 6072.26}, {'customer': 'Lightstyle of Orlando', 'revenue': 4642.56}, {'customer': 'Lamps Plus.com-Auto ASN', 'revenue': 3966.07}, {'customer': 'Haus Appeal LLC', 'revenue': 3554.38}, {'customer': 'Belami.com (1 Stop) - ASN', 'revenue': 3144.96}, {'customer': 'Dominion Electric', 'revenue': 2969.87}, {'customer': 'Idlewood Electric Supply', 'revenue': 2450.57}, {'customer': 'LDB Holdings, LLC', 'revenue': 2396.0}, {'customer': 'Lightopia, LLC.', 'revenue': 2310.87}, {'customer': 'Melrose & Madison (AMZ)', 'revenue': 2161.99}, {'customer': 'Newton Electrical Company', 'revenue': 2097.0}, {'customer': 'B.A. Robinson Co. Ltd.', 'revenue': 1947.0}, {'customer': 'IBS Lighting', 'revenue': 1897.0}, {'customer': 'Lightology, LLC.com', 'revenue': 1847.0}, {'customer': 'PC Building Materials', 'revenue': 1847.0}, {'customer': "Horton's Home Lighting", 'revenue': 1802.15}, {'customer': 'The Lighting Design Co.', 'revenue': 1801.57}, {'customer': 'BBC Lighting Company', 'revenue': 1797.0}, {'customer': 'Capitol Lighting-Dropship-ASN', 'revenue': 1662.3}, {'customer': 'Union Lighting & Home', 'revenue': 1326.87}, {'customer': 'Xpress Lighting of Texas', 'revenue': 1298.0}, {'customer': 'Cleveland Lighting', 'revenue': 1265.55}, {'customer': 'Texas Bright Ideas', 'revenue': 1252.57}, {'customer': 'Light Brite Distributing, Inc', 'revenue': 1248.0}, {'customer': 'Cates Lighting at Elements', 'revenue': 1248.0}, {'customer': 'Pine Tree Lighting', 'revenue': 1248.0}, {'customer': 'Ancelran, Inc. DBA Muska Lighting Center', 'revenue': 1248.0}, {'customer': 'Montreal Luminaire', 'revenue': 1225.74}, {'customer': 'Christies Lighting Gallery,LLC', 'revenue': 1207.14}, {'customer': 'Jackson Lighting', 'revenue': 1207.14}, {'customer': 'Valencia Lighting & Design', 'revenue': 1202.57}, {'customer': 'Lights of Oconee', 'revenue': 1202.57}, {'customer': 'Dement Lighting', 'revenue': 1198.0}, {'customer': "Efird's Interiors, Inc.", 'revenue': 1123.2}, {'customer': 'Connecticut Lighting Center', 'revenue': 1123.2}, {'customer': 'Stokes Lighting Center', 'revenue': 1018.3}, {'customer': 'Hermitage Lighting Gallery', 'revenue': 948.5}, {'customer': 'Elements', 'revenue': 873.6}, {'customer': 'Great Neighborhood Homes', 'revenue': 749.0}, {'customer': 'Jill Heaton Interiors', 'revenue': 747.0}, {'customer': 'J. Adams Interiors', 'revenue': 747.0}, {'customer': 'Loudoun Interiors LLC', 'revenue': 747.0}, {'customer': 'Winsupply Owensboro KY Co', 'revenue': 649.0}, {'customer': 'Ocean Pacific Lighting', 'revenue': 649.0}, {'customer': 'White Star Supply LLC', 'revenue': 649.0}, {'customer': 'Hubbard Kitchen & BathShowroom', 'revenue': 649.0}, {'customer': 'Hydrologic Distribution Co.', 'revenue': 649.0}, {'customer': 'Light Bulbs, Etc. (Orange)', 'revenue': 649.0}, {'customer': 'Wiseway Supply', 'revenue': 649.0}, {'customer': 'Uncommon Living Inc.', 'revenue': 649.0}, {'customer': 'Lighting Etc.', 'revenue': 649.0}, {'customer': 'Modern Lighting', 'revenue': 649.0}, {'customer': 'Paradise Lighting', 'revenue': 649.0}, {'customer': 'Kathy Kuo Home', 'revenue': 606.81}, {'customer': 'Ambient Lighting DBA Lights.com', 'revenue': 603.57}, {'customer': 'Littman Bros Lighting', 'revenue': 603.57}, {'customer': 'JCM Lighting and Design, DBA The Local Lighting Shop', 'revenue': 603.57}, {'customer': 'Lowes Companies , Inc', 'revenue': 599.0}, {'customer': 'Hajoca Corporation', 'revenue': 599.0}, {'customer': 'Elan Studio Lighting', 'revenue': 599.0}, {'customer': 'Hobrecht Lighting Co., Inc.', 'revenue': 599.0}, {'customer': 'Inline Electric of Montgomery', 'revenue': 599.0}, {'customer': 'Design Trade Service', 'revenue': 599.0}, {'customer': 'Frank Souder Designs', 'revenue': 599.0}, {'customer': 'River Cities Lighting', 'revenue': 599.0}, {'customer': 'Capitol Lighting Gallery', 'revenue': 599.0}, {'customer': 'M&M Lighting Co', 'revenue': 599.0}, {'customer': 'William Hart Designs, LLC', 'revenue': 599.0}, {'customer': 'Coley Electric & Plumbing Sup', 'revenue': 599.0}, {'customer': 'Legacy Lighting', 'revenue': 599.0}, {'customer': 'Decorum', 'revenue': 599.0}, {'customer': 'Net Retailers dba Luxe Decor', 'revenue': 599.0}, {'customer': 'Kendall Electric', 'revenue': 599.0}, {'customer': 'The Brecher Company', 'revenue': 599.0}, {'customer': 'Dhillon Lighting Inc. of Calgary', 'revenue': 599.0}, {'customer': 'Lee Supply Corporate', 'revenue': 599.0}, {'customer': 'Metro Showroom West County', 'revenue': 584.1}, {'customer': 'Progressive Lighting', 'revenue': 584.1}, {'customer': 'Rensen House Lights', 'revenue': 557.07}, {'customer': 'CAI Designs', 'revenue': 557.07}, {'customer': 'Litemode Limited', 'revenue': 557.07}, {'customer': 'Foundrylighting.com', 'revenue': 557.07}, {'customer': 'Dolan NW LLC', 'revenue': 539.1}, {'customer': 'Prima Lighting', 'revenue': 539.1}, {'customer': 'Union Lighting & Furnishings', 'revenue': 519.2}, {'customer': 'Gerrie Electric', 'revenue': 0.0}, {'customer': 'KLS dba Spectrum Lighting', 'revenue': 0.0}, {'customer': 'Bright Light Design Center DBA Colonial Lighting', 'revenue': 0.0}, {'customer': 'The Lighting Warehouse', 'revenue': 0.0}] | [{'item': 'ADD-306-AG-AU', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 117}, {'item': 'ADD-312-AG-AM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 83}, {'item': 'ADD-300-AG-AU_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 65}, {'item': 'ADD-300-AG-AU', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 65}, {'item': 'ADD-302-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 57}, {'item': 'ADD-300-AG-AM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 55}, {'item': 'ADD-302-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 51}, {'item': 'ADD-300-AG-AM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 51}, {'item': 'ADD-312-AG-WH', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 36}, {'item': 'ADD-302-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 35}, {'item': 'ADD-300-AG-WH_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 35}, {'item': 'ADD-300-AG-WH', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 35}, {'item': 'ADD-300-AG-SP', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 31}, {'item': 'ADD-300-AG-SP_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 31}, {'item': 'ADD-300-AG-SM_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 30}, {'item': 'ADD-306-CH-WH', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 28}, {'item': 'ADD-306-AG-WH', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 28}, {'item': 'ADD-300-AG-SM', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL', 'desc': "Addis 17.75'' Aged Brass Chandelier", 'available': 27}, {'item': 'ADD-300-AG-CL_CEILING', 'desc': "Addis 17.75'' Aged Brass Semi Flush Mount", 'available': 26}, {'item': 'ADD-303-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-AG-SM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 24}, {'item': 'ADD-303-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 23}, {'item': 'ADD-317-AG-WH', 'desc': "Addis 51.75'' Aged Brass Linear Chandelier", 'available': 23}, {'item': 'ADD-312-CH-WH', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 23}, {'item': 'ADD-319-AG-WH', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 22}, {'item': 'ADD-321-AG-CL', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 21}, {'item': 'ADD-302-CH-CL', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 21}, {'item': 'ADD-306-AG-SM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 21}, {'item': 'ADD-303-AG-AM', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 20}, {'item': 'ADD-303-AG-CL', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 19}, {'item': 'ADD-303-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 18}, {'item': 'ADD-303-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 18}, {'item': 'ADD-302-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 17}, {'item': 'ADD-302-AG-WH', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 17}, {'item': 'ADD-319-CH-CL', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-303-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 16}, {'item': 'ADD-306-CH-SM', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 16}, {'item': 'ADD-316-AG-CL', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 15}, {'item': 'ADD-308-CH-SM', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-308-CH-WH', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-316-CH-SP', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 15}, {'item': 'ADD-302-AG-SP', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 14}, {'item': 'ADD-302-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-302-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 13}, {'item': 'ADD-331-CH-SM', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 13}, {'item': 'ADD-302-AG-AU', 'desc': "Addis 14.5'' Aged Brass Sconce", 'available': 12}, {'item': 'ADD-316-AG-WH', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 12}, {'item': 'ADD-302-CH-WH', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 11}, {'item': 'ADD-306-CH-AU', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-306-AG-AM', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-308-AG-AU', 'desc': "Addis 22'' Aged Brass Chandelier", 'available': 11}, {'item': 'ADD-306-CH-CL', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 11}, {'item': 'ADD-312-AG-SM', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-306-AG-CL', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 10}, {'item': 'ADD-331-AG-CL', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 10}, {'item': 'ADD-319-CH-AU', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-321-CH-AU', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-321-CH-SP', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 10}, {'item': 'ADD-306-CH-SP', 'desc': "Addis 19.75'' Polished Chrome Chandelier", 'available': 10}, {'item': 'ADD-317-CH-CL', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 10}, {'item': 'ADD-316-CH-CL', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-308-CH-SP', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 9}, {'item': 'ADD-312-AG-CL', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 9}, {'item': 'ADD-303-CH-SP', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 9}, {'item': 'ADD-317-CH-AU', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 8}, {'item': 'ADD-319-AG-CL', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 8}, {'item': 'ADD-331-AG-WH', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 7}, {'item': 'ADD-300-CH-AU', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-AU_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 7}, {'item': 'ADD-312-CH-CL', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 7}, {'item': 'ADD-300-CH-SM_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-316-CH-WH', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-316-CH-AU', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-308-CH-CL', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-WH_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 6}, {'item': 'ADD-300-CH-WH', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-300-CH-SM', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AU', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-319-AG-AM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-331-CH-WH', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-303-CH-SM', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 6}, {'item': 'ADD-319-CH-SP', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-WH', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-319-CH-SM', 'desc': "Addis 31.5'' Polished Chrome Chandelier", 'available': 6}, {'item': 'ADD-317-CH-WH', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-317-CH-SM', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 6}, {'item': 'ADD-321-CH-CL', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-331-CH-SP', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 6}, {'item': 'ADD-316-AG-SP', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 6}, {'item': 'ADD-300-CH-CL', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-303-CH-AU', 'desc': "Addis 14.5'' Polished Chrome Sconce", 'available': 5}, {'item': 'ADD-316-AG-AU', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SP', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-312-CH-SM', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 5}, {'item': 'ADD-306-AG-SP', 'desc': "Addis 19.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-312-AG-SP', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-316-AG-SM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 5}, {'item': 'ADD-331-AG-AM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-AG-AU', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 5}, {'item': 'ADD-331-CH-AU', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 5}, {'item': 'ADD-316-CH-SM', 'desc': "Addis 32'' Polished Chrome Chandelier", 'available': 4}, {'item': 'ADD-331-AG-SM', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 4}, {'item': 'ADD-317-CH-SP', 'desc': "Addis 51.75'' Polished Chrome Linear Chandelier", 'available': 4}, {'item': 'ADD-312-AG-AU', 'desc': "Addis 26.75'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-321-CH-WH', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 4}, {'item': 'ADD-316-AG-AM', 'desc': "Addis 32'' Aged Brass Chandelier", 'available': 4}, {'item': 'ADD-300-CH-CL_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 4}, {'item': 'ADD-319-AG-SP', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 3}, {'item': 'ADD-300-CH-SP_CEILING', 'desc': "Addis 17.75'' Polished Chrome Semi Flush Mount", 'available': 3}, {'item': 'ADD-300-CH-SP', 'desc': "Addis 17.75'' Polished Chrome Chandelier", 'available': 3}, {'item': 'ADD-312-CH-AU', 'desc': "Addis 26.75'' Polished Chrome Chandelier", 'available': 2}, {'item': 'ADD-319-AG-SM', 'desc': "Addis 31.5'' Aged Brass Chandelier", 'available': 2}, {'item': 'ADD-327-AG-AU', 'desc': "Addis 49'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-331-AG-SP', 'desc': "Addis 32'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-329-AG-WH', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SP', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-SM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-CL', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AU', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-329-AG-AM', 'desc': "Addis 62'' Aged Brass Chandelier", 'available': 1}, {'item': 'ADD-327-CH-WH', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-AU', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-AM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-AG-AU', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-321-CH-SM', 'desc': "Addis 22.25'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-331-CH-CL', 'desc': "Addis 32'' Polished Chrome Flush Mount", 'available': 1}, {'item': 'ADD-308-CH-AU', 'desc': "Addis 22'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-321-AG-SM', 'desc': "Addis 22.25'' Aged Brass Flush Mount", 'available': 1}, {'item': 'ADD-327-CH-SP', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}, {'item': 'ADD-327-CH-CL', 'desc': "Addis 49'' Polished Chrome Chandelier", 'available': 1}] |
