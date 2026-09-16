# Section 2 Context Bundle — Craftmade (clli)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=168198, portal_order_gmv=$47.7M |
| HAS_INVENTORY | True | inventory_count=2867 |
| HAS_SALES_DATA | True | sales_data_count=508787 |
| HAS_SALES_SECTION | True | qualifying_reps=9 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Commerce-Active |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | clli_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$47.7M > ecat_gmv=$881,333: True |
| VM45_GATE_2 | FAIL | ecat_gmv >= 5% of erp_gmv: False |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 9 | 9 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 91 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 228, Mixpanel total submit_order (Q-01): 371 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=83.5%, ambiguous_rate=15.8%, showroom_event_share=7.3% |
| USER_GROUP_JOIN_RATE | 84% | 76 of 91 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 7% | showroom+admin share of matched events: 7.3% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: David Raushchuber, Kevin Ailara, Andrew  Rivera, Shayna Petty |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1722 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=289 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Craftmade
- **Shortname**: clli
- **Org ID**: 149
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- VM-45 skipped: Gate1=PASS, Gate2=FAIL

## Section Confidence

# Section Confidence Tiers — Craftmade (clli, org_id=149)
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

# Signal Rank — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Total signals fired**: 51 (P0: 36, P1: 13, P2: 2)
- **Org GMV**: $0.9M eCat LTM, $47.7M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders | P1 | §2 Accounts | 8.3 | $8,279,294 | 2.0 | 137,093,418 | POSITIVE |
| 2 | SIG-MOM-01 | Account Acceleration —  3 consecutive QoQ acceleration quarters, $622,312 peak quarter (+180% QoQ) | P0 | §2 Accounts | 6.0 | $622,312 | 3.0 | 11,195,390 | POSITIVE |
| 3 | SIG-DECAY-04 | Spending Contraction —  -89.7% YoY ($899,202→$92,187), $807,015 gap | P0 | §2 Accounts | 4.5 | $807,015 | 3.0 | 10,858,392 | RISK |
| 4 | SIG-DECAY-04 | Spending Contraction —  -59.2% YoY ($1,788,691→$729,998), $1,058,693 gap | P0 | §2 Accounts | 3.0 | $1,058,693 | 3.0 | 9,401,193 | RISK |
| 5 | SIG-DECAY-04 | Spending Contraction —  -78.3% YoY ($957,251→$208,171), $749,080 gap | P0 | §2 Accounts | 3.9 | $749,080 | 3.0 | 8,797,942 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available | P0 | §3 Product | 10.0 | $281,687 | 3.0 | 8,450,620 | RISK |
| 7 | SIG-DECAY-04 | Spending Contraction —  -61.5% YoY ($1,414,384→$545,054), $869,331 gap | P0 | §2 Accounts | 3.1 | $869,331 | 3.0 | 8,019,576 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available | P0 | §3 Product | 10.0 | $266,996 | 3.0 | 8,009,889 | RISK |
| 9 | SIG-COMMERCE-01 | Capture Rate — eCat captures 1.8% of $48M total business; each +1pt = $477K | P0 | §4 Commerce | 4.9 | $477,000 | 3.0 | 7,022,800 | POSITIVE |
| 10 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $104,278 peak quarter (+594% QoQ) | P0 | §2 Accounts | 19.8 | $104,278 | 3.0 | 6,188,876 | POSITIVE |
| 11 | SIG-ANOMALY-02 | Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available | P0 | §3 Product | 10.0 | $193,427 | 3.0 | 5,802,810 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 19624BNK3 (Drake 3 Light Vanity in Brushed Polished) $174,443 LTM, 0 available | P0 | §3 Product | 10.0 | $174,443 | 3.0 | 5,233,279 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — BSCB-B (Surface Mount Die-Cast Builder's Series ) $162,869 LTM, 0 available | P0 | §3 Product | 10.0 | $162,869 | 3.0 | 4,886,060 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — Z402-TB (2 Light Directional Bullet in Textured B) $146,102 LTM, 0 available | P0 | §3 Product | 10.0 | $146,102 | 3.0 | 4,383,061 | RISK |
| 15 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $83,118 peak quarter (+490% QoQ) | P0 | §2 Accounts | 16.3 | $83,118 | 3.0 | 4,073,595 | POSITIVE |
| 16 | SIG-ANOMALY-02 | Stock Out — PH-2BZ (2 Light PAR Holder in Bronze) $132,167 LTM, 0 available | P0 | §3 Product | 10.0 | $132,167 | 3.0 | 3,964,999 | RISK |
| 17 | SIG-DECAY-04 | Spending Contraction —  -33.2% YoY ($1,528,897→$1,021,173), $507,724 gap | P0 | §2 Accounts | 1.7 | $507,724 | 3.0 | 2,528,463 | RISK |
| 18 | SIG-DECAY-04 | Spending Contraction —  -59.4% YoY ($403,858→$164,014), $239,843 gap | P0 | §2 Accounts | 3.0 | $239,843 | 3.0 | 2,137,005 | RISK |
| 19 | SIG-DECAY-04 | Spending Contraction —  -55.6% YoY ($422,120→$187,615), $234,505 gap | P0 | §2 Accounts | 2.8 | $234,505 | 3.0 | 1,955,775 | RISK |
| 20 | SIG-MOM-01 | Account Acceleration —  2 consecutive QoQ acceleration quarters, $87,277 peak quarter (+164% QoQ) | P0 | §2 Accounts | 5.5 | $87,277 | 3.0 | 1,428,729 | POSITIVE |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 28 | 1 | 0 | 29 | |
| §3 Product Intelligence | 7 | 0 | 1 | 8 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 1 | 12 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration —  3 consecutive QoQ acceleration quarters, $622,312 peak quarter (+180% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Capture Rate — eCat captures 1.8% of $48M total business; each +1pt = $477K
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### top_accounts.md

# Top 10 Accounts for Mini-Briefs — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Selection criteria**: Per-account signal density (accounts appearing across multiple signal types)

| Rank | Customer Name | Signal Count | Signals | Max Dollar Impact |
| --- | --- | --- | --- | --- |
| 1 | 20 accounts | 1 | OPP-02 | $8,279,294 |

### Q-12_results.md

# Q-12 Results — Craftmade (clli, org_id=149)
- **Query**: Q-12 — Customer Activation & ERP Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| total_erp_customers | total_ever_ordered_via_ecat | active_12mo | active_6mo | active_3mo |
| --- | --- | --- | --- | --- |
| 5,183 | 344 | 148 | 127 | 4 |

### Q-14_results.md

# Q-14 Results — Craftmade (clli, org_id=149)
- **Query**: Q-14 — Customer Reorder Frequency
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 17
- **Run date**: 2026-06-17


| customer_num | bill_to_company_name | ecat_order_count | ecat_gmv | first_ecat_order | last_ecat_order | avg_days_between_ecat_orders |
| --- | --- | --- | --- | --- | --- | --- |
| 9800 | FERGUSON ENTERPRISES INC | 7 | $16,270 | 2026-01-11 19:51:46 | 2026-03-20 15:58:57 | 11.30 |
| 44067 | JD DESIGNS INC | 6 | $2,970 | 2025-08-13 00:17:14 | 2026-04-02 19:50:52 | 46.60 |
| 43128 | WHITE OAK COTTAGE | 5 | $9,554 | 2025-07-02 22:26:15 | 2025-11-24 13:50:19 | 36.20 |
| 26190 | SONEPAR-USA | 3 | $1,176 | 2026-01-11 17:46:44 | 2026-01-11 21:15:43 | 0.10 |
| 30352 | TRI SUPPLY | 3 | $4,430 | 2025-06-18 17:55:43 | 2026-01-10 22:13:14 | 103.10 |
| 30800 | COASTAL LIGHTING, LLC | 3 | $14,184 | 2026-01-11 16:38:45 | 2026-01-15 01:05:40 | 1.70 |
| 4006 | CONCEPT LUMINAIRE | 3 | $962 | 2026-01-09 17:44:27 | 2026-01-12 17:34:48 | 1.50 |
| 2 | Craftmade Sample Account | 3 | $183,193 | 2025-07-28 23:19:57 | 2025-12-18 15:44:52 | 71.30 |
| 44168 | KINGSTON LIGHTING | 3 | $3,561 | 2026-01-11 23:39:51 | 2026-02-23 15:36:06 | 21.30 |
| 44169 | LADY HOME | 3 | $43,442 | 2025-07-29 21:46:32 | 2025-07-29 22:20:42 | 0 |
| 46005 | THE GALLERIES | 3 | $6,277 | 2026-01-10 17:47:14 | 2026-01-13 17:18:15 | 1.50 |
| 50891 | GW KEETER LIGHTING & HOME | 3 | $9,670 | 2025-06-19 18:06:14 | 2026-01-29 21:14:29 | 112.10 |
| 50900 | HAJOCA CORP | 3 | $10,786 | 2025-06-18 15:07:46 | 2026-01-11 19:04:14 | 103.60 |
| 60600 | BUTLERS ELECTRIC SUPPLY- | 3 | $2,153 | 2025-06-20 16:59:34 | 2025-08-20 19:17:02 | 30.50 |
| 43564 | 4 U LIGHTING & DESIGN | 3 | $6,944 | 2025-06-24 18:07:40 | 2026-01-11 22:07:26 | 100.60 |
| 20501 | PINE GROVE ELEC SPLY | 3 | $13,910 | 2026-01-13 22:44:50 | 2026-01-23 16:12:22 | 4.90 |
| 2473 | LIGHTSTYLE OF ORLANDO | 3 | $9,133 | 2025-06-20 13:25:49 | 2025-06-20 13:38:36 | 0 |

### Q-14b_results.md

# Q-14b Results — Craftmade (clli, org_id=149)
- **Query**: Q-14b — Account Velocity Deceleration Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_bill_to_number | customer_bill_to_name | total_intervals | historical_avg_interval | recent_avg_interval | deceleration_ratio | annual_gmv |
| --- | --- | --- | --- | --- | --- | --- |
| 70018 |  | 1,439 | 0.30 | 0.50 | 1.67 | $915,460 |
| 15225 |  | 1,143 | 0.40 | 0.60 | 1.50 | $416,289 |
| 31413 |  | 2,892 | 0.20 | 0.30 | 1.50 | $358,911 |
| 44030 |  | 71 | 5.70 | 13.10 | 2.30 | $301,482 |
| 2071 |  | 3,503 | 0.10 | 0.20 | 2 | $251,197 |
| 44042 |  | 107 | 3.90 | 8 | 2.05 | $222,290 |
| 5282 |  | 1,779 | 0.20 | 0.60 | 3 | $208,171 |
| 34678 |  | 492 | 0.90 | 1.40 | 1.56 | $177,139 |
| 4245 |  | 251 | 1.80 | 3.40 | 1.89 | $164,014 |
| 33398 |  | 237 | 1.90 | 3.80 | 2 | $142,592 |
| 218 |  | 37 | 11.70 | 19.10 | 1.63 | $107,752 |
| 1667 |  | 3,946 | 0.10 | 0.40 | 4 | $92,187 |
| 40562 |  | 311 | 1.50 | 2.40 | 1.60 | $87,680 |
| 40350 |  | 55 | 7.70 | 15.10 | 1.96 | $81,908 |
| 44027 |  | 16 | 27.30 | 49.50 | 1.81 | $78,171 |

### Q-17_results.md

# Q-17 Results — Craftmade (clli, org_id=149)
- **Query**: Q-17 — Dormant eCat Customers — Lapsed
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | last_ecat_order_date | historical_ecat_orders | historical_ecat_gmv |
| --- | --- | --- | --- | --- | --- |
| 2 | Craftmade Sample Account | TX | 2025-12-18 15:44:52 | 3 | $183,193 |
| 93510 | ROYAUME LUMINAIRE LANDAUDIERE | QC | 2026-01-12 15:07:08 | 1 | $43,518 |
| 44169 | LADY HOME | TX | 2025-07-29 22:20:42 | 3 | $43,442 |
| 94530 | ROYAUME LUMINAIRE SHERBROOKE | QC | 2026-01-12 15:06:43 | 1 | $22,506 |
| 44515 | FORT WORTH LIGHTING | TX | 2025-06-23 17:04:10 | 1 | $20,576 |
| 93011 | ROYAUME LUMINAIRE DRUMMONDVILL | QC | 2026-01-12 15:11:22 | 1 | $20,293 |
| 93512 | ROYAUME LUMINAIRE BEAUPORT INC | QC | 2026-01-12 15:12:02 | 1 | $19,180 |
| 1 | Craftmade Warranty Account | TX | 2025-06-20 14:10:28 | 1 | $17,765 |
| 93511 | ROYAUME LUMINAIRE J D INC | QC | 2026-01-12 15:08:43 | 1 | $17,066 |
| 4023 | ROYAUME LUMINAIRE-TROIS | QC | 2026-01-12 15:12:07 | 1 | $16,375 |
| 93515 | ROYAUME LUMINAIRE STE JULIE | QC | 2026-01-12 15:11:05 | 1 | $14,430 |
| 30800 | COASTAL LIGHTING, LLC | TX | 2026-01-15 01:05:40 | 3 | $14,184 |
| 20501 | PINE GROVE ELEC SPLY | LA | 2026-01-23 16:12:22 | 3 | $13,910 |
| 20328 | HOUSE OF CARPETS INC | LA | 2026-01-13 22:50:10 | 2 | $12,687 |
| 50900 | HAJOCA CORP | LA | 2026-01-11 19:04:14 | 3 | $10,786 |
| 42179 | FAN DEPOT | DN | 2025-11-20 20:06:47 | 1 | $9,916 |
| 34381 | GRAND RAPIDS LIGHTING CTR INC | MI | 2026-01-14 13:26:28 | 1 | $9,727 |
| 50891 | GW KEETER LIGHTING & HOME | AR | 2026-01-29 21:14:29 | 3 | $9,670 |
| 43128 | WHITE OAK COTTAGE | FL | 2025-11-24 13:50:19 | 5 | $9,554 |
| 2473 | LIGHTSTYLE OF ORLANDO | FL | 2025-06-20 13:38:36 | 3 | $9,133 |
| 18720 | METRO LIGHTING | MO | 2026-01-10 21:31:46 | 2 | $9,060 |
| 70056 | INLINE ELECTRIC SUPPLY | AL | 2026-01-11 21:14:37 | 2 | $8,272 |
| 1017 | Q E D | CO | 2026-01-11 21:37:03 | 1 | $7,178 |
| 4029 | HEARTH & HOME | AR | 2026-01-11 16:17:26 | 1 | $7,112 |
| 43564 | 4 U LIGHTING & DESIGN | FL | 2026-01-11 22:07:26 | 3 | $6,944 |

### Q-17_atrisk_results.md

# Q-17-atrisk Results — Craftmade (clli, org_id=149)
- **Query**: Q-17-atrisk — Dormant eCat Customers — At-Risk
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_num | customer_name | billing_state | ecat_gmv_12mo | last_ecat_order_date | days_since_last_ecat_order |
| --- | --- | --- | --- | --- | --- |
| 2 | Craftmade Sample Account | TX | $183,193 | 2025-12-18 15:44:52 | 181 |
| 93510 | ROYAUME LUMINAIRE LANDAUDIERE | QC | $43,518 | 2026-01-12 15:07:08 | 156 |
| 44169 | LADY HOME | TX | $43,442 | 2025-07-29 22:20:42 | 322 |
| 94530 | ROYAUME LUMINAIRE SHERBROOKE | QC | $22,506 | 2026-01-12 15:06:43 | 156 |
| 44515 | FORT WORTH LIGHTING | TX | $20,576 | 2025-06-23 17:04:10 | 359 |
| 93011 | ROYAUME LUMINAIRE DRUMMONDVILL | QC | $20,293 | 2026-01-12 15:11:22 | 156 |
| 93512 | ROYAUME LUMINAIRE BEAUPORT INC | QC | $19,180 | 2026-01-12 15:12:02 | 156 |
| 1 | Craftmade Warranty Account | TX | $17,765 | 2025-06-20 14:10:28 | 362 |
| 93511 | ROYAUME LUMINAIRE J D INC | QC | $17,066 | 2026-01-12 15:08:43 | 156 |
| 4023 | ROYAUME LUMINAIRE-TROIS | QC | $16,375 | 2026-01-12 15:12:07 | 156 |
| 93515 | ROYAUME LUMINAIRE STE JULIE | QC | $14,430 | 2026-01-12 15:11:05 | 156 |
| 30800 | COASTAL LIGHTING, LLC | TX | $14,184 | 2026-01-15 01:05:40 | 153 |
| 20501 | PINE GROVE ELEC SPLY | LA | $13,910 | 2026-01-23 16:12:22 | 145 |
| 20328 | HOUSE OF CARPETS INC | LA | $12,687 | 2026-01-13 22:50:10 | 154 |
| 50900 | HAJOCA CORP | LA | $10,786 | 2026-01-11 19:04:14 | 157 |
| 42179 | FAN DEPOT | DN | $9,916 | 2025-11-20 20:06:47 | 209 |
| 34381 | GRAND RAPIDS LIGHTING CTR INC | MI | $9,727 | 2026-01-14 13:26:28 | 154 |
| 50891 | GW KEETER LIGHTING & HOME | AR | $9,670 | 2026-01-29 21:14:29 | 138 |
| 43128 | WHITE OAK COTTAGE | FL | $9,554 | 2025-11-24 13:50:19 | 205 |
| 2473 | LIGHTSTYLE OF ORLANDO | FL | $9,133 | 2025-06-20 13:38:36 | 362 |

### Q-40_results.md

# Q-40 Results — Craftmade (clli, org_id=149)
- **Query**: Q-40 — Regional Sales Distribution
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | customer_count | ecat_order_count | ecat_gmv |
| --- | --- | --- | --- |
| TX | 23 | 37 | $324,110 |
| QC | 10 | 12 | $164,672 |
| LA | 6 | 11 | $48,962 |
| AR | 9 | 14 | $43,207 |
| FL | 9 | 24 | $31,429 |
| MO | 7 | 10 | $22,089 |
| MI | 4 | 4 | $18,838 |
| VA | 1 | 7 | $16,270 |
| TN | 6 | 6 | $15,789 |
| KS | 5 | 6 | $15,168 |
| MN | 5 | 6 | $13,666 |
| ON | 4 | 6 | $12,411 |
| UT | 4 | 6 | $12,108 |
| AL | 2 | 3 | $11,644 |
| AB | 3 | 3 | $10,116 |
| DN | 1 | 1 | $9,916 |
| CO | 3 | 4 | $9,856 |
| NC | 5 | 6 | $7,022 |
| IL | 3 | 3 | $6,829 |
| SC | 6 | 11 | $6,138 |

### Q-41_results.md

# Q-41 Results — Craftmade (clli, org_id=149)
- **Query**: Q-41 — First-Time eCat Orderers — By Channel
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 9
- **Run date**: 2026-06-17


| month | acquisition_channel | first_time_ecat_buyers |
| --- | --- | --- |
| 2025-03-01 | Rep-Acquired (iPad) | 1 |
| 2025-04-01 | Rep-Acquired (iPad) | 3 |
| 2025-05-01 | Rep-Acquired (iPad) | 1 |
| 2025-06-01 | Rep-Acquired (iPad) | 9 |
| 2025-09-01 | Rep-Acquired (iPad) | 2 |
| 2025-10-01 | Rep-Acquired (iPad) | 1 |
| 2026-01-01 | Rep-Acquired (iPad) | 24 |
| 2026-02-01 | Rep-Acquired (iPad) | 4 |
| 2026-03-01 | Rep-Acquired (iPad) | 1 |

### Q-41_rep_results.md

# Q-41-rep Results — Craftmade (clli, org_id=149)
- **Query**: Q-41-rep — First-Time eCat Orderers — By Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| rep | new_ecat_buyers_acquired |
| --- | --- |
| Ron Iversen | 4 |
| Harold Ballow | 4 |
| Hudson Williams | 4 |
| Tom Gray | 3 |
| Mike Elford | 3 |
| Keith Eichenblatt | 2 |
| Chris Wilga | 2 |
| David Raushchuber | 2 |
| Doeren Carsten | 2 |
| Alex Miranda | 2 |
| Mike Jeffcoat | 2 |
| Newell King | 2 |
| Nick Brown | 2 |
| Kevin Ailara | 1 |
| Laura Ford | 1 |
| Linda Huffman | 1 |
| Bryan  Greenway | 1 |
| Barb Roemerman | 1 |
| Shayna Petty | 1 |
| Andrew  Rivera | 1 |
| Patty Lingwall | 1 |
| Cathy/Chad Teiber | 1 |
| Jerry Sharp | 1 |
| Joe Glatthaar | 1 |
| Peter Saiolla | 1 |

### Q-52_results.md

# Q-52 Results — Craftmade (clli, org_id=149)
- **Query**: Q-52 — Customer-Level eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9800 |  |  | 5,814 | $2.6M | 7 | $16,270 | 0.60 |
| 6050 |  |  | 14,076 | $2.0M | 0 | $0 | 0 |
| 9996 |  |  | 198 | $1.5M | 0 | $0 | 0 |
| 10106 |  |  | 587 | $1.2M | 1 | $2,242 | 0.20 |
| 9802 |  |  | 7,601 | $1.0M | 0 | $0 | 0 |
| 44515 |  |  | 530 | $923,090 | 1 | $20,576 | 2.20 |
| 70018 |  |  | 952 | $915,460 | 0 | $0 | 0 |
| 60572 |  |  | 194 | $751,233 | 0 | $0 | 0 |
| 106010 |  |  | 6,247 | $729,998 | 0 | $0 | 0 |
| 7005 |  |  | 5,789 | $722,780 | 0 | $0 | 0 |
| 3919 |  |  | 6,239 | $666,618 | 0 | $0 | 0 |
| 9708 |  |  | 482 | $649,701 | 0 | $0 | 0 |
| 44004 |  |  | 164 | $545,054 | 0 | $0 | 0 |
| 60559 |  |  | 611 | $535,915 | 0 | $0 | 0 |
| 20698 |  |  | 791 | $515,701 | 1 | $2,050 | 0.40 |
| 70680 |  |  | 555 | $506,450 | 1 | $2,335 | 0.50 |
| 43553 |  |  | 2,822 | $453,227 | 0 | $0 | 0 |
| 15225 |  |  | 737 | $416,289 | 0 | $0 | 0 |
| 40138 |  |  | 263 | $397,394 | 1 | $3,280 | 0.80 |
| 70056 |  |  | 491 | $392,829 | 2 | $8,272 | 2.10 |
| 70330 |  |  | 267 | $384,395 | 0 | $0 | 0 |
| 26190 |  |  | 403 | $375,867 | 3 | $1,176 | 0.30 |
| 31413 |  |  | 1,793 | $358,911 | 0 | $0 | 0 |
| 44950 |  |  | 199 | $355,067 | 0 | $0 | 0 |
| 4029 |  |  | 92 | $332,416 | 1 | $7,112 | 2.10 |
| 4035 |  |  | 121 | $324,451 | 1 | $1,390 | 0.40 |
| 10102 |  |  | 339 | $316,950 | 1 | $2,311 | 0.70 |
| 18720 |  |  | 555 | $306,262 | 2 | $9,060 | 3 |
| 44030 |  |  | 36 | $301,482 | 0 | $0 | 0 |
| 50891 |  |  | 127 | $285,994 | 3 | $9,670 | 3.40 |

### Q-53_results.md

# Q-53 Results — Craftmade (clli, org_id=149)
- **Query**: Q-53 — Unactivated High-Value ERP Accounts
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_code | customer_name | state | erp_orders | erp_gmv |
| --- | --- | --- | --- | --- |
| 9802 |  |  | 7,601 | $1.0M |
| 60572 |  |  | 194 | $751,233 |
| 106010 |  |  | 6,247 | $729,998 |
| 3919 |  |  | 6,239 | $666,618 |
| 44004 |  |  | 164 | $545,054 |
| 60559 |  |  | 611 | $535,915 |
| 43553 |  |  | 2,822 | $453,227 |
| 31413 |  |  | 1,793 | $358,911 |
| 44950 |  |  | 199 | $355,067 |
| 44030 |  |  | 36 | $301,482 |
| 1120 |  |  | 263 | $282,861 |
| 44910 |  |  | 328 | $278,311 |
| 13801 |  |  | 137 | $277,163 |
| 43880 |  |  | 36 | $272,755 |
| 31900 |  |  | 926 | $260,028 |
| 44506 |  |  | 142 | $255,756 |
| 2071 |  |  | 1,979 | $251,197 |
| 70076 |  |  | 204 | $248,616 |
| 70116 |  |  | 33 | $229,814 |
| 50017 |  |  | 82 | $225,288 |

*(Truncated: showing top 20 of 20 rows. Full data in cache file.)*

### Q-54_results.md

# Q-54 Results — Craftmade (clli, org_id=149)
- **Query**: Q-54 — Geographic eCat Penetration
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| state | erp_customers | erp_orders | erp_gmv | ecat_customers | ecat_orders | ecat_gmv | ecat_penetration_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AB | 0 | 0 | $0 | 3 | 3 | $10,116 | — |
| AL | 0 | 0 | $0 | 2 | 3 | $11,644 | — |
| AR | 0 | 0 | $0 | 9 | 14 | $43,207 | — |
| AZ | 0 | 0 | $0 | 4 | 4 | $4,987 | — |
| BC | 0 | 0 | $0 | 3 | 3 | $4,692 | — |
| CA | 0 | 0 | $0 | 2 | 2 | $3,462 | — |
| CO | 0 | 0 | $0 | 3 | 4 | $9,856 | — |
| DN | 0 | 0 | $0 | 1 | 1 | $9,916 | — |
| FL | 0 | 0 | $0 | 9 | 24 | $31,429 | — |
| GA | 0 | 0 | $0 | 3 | 3 | $3,951 | — |
| IA | 0 | 0 | $0 | 2 | 2 | $1,816 | — |
| ID | 0 | 0 | $0 | 1 | 1 | $3,313 | — |
| IL | 0 | 0 | $0 | 3 | 3 | $6,829 | — |
| KS | 0 | 0 | $0 | 5 | 6 | $15,168 | — |
| LA | 0 | 0 | $0 | 6 | 11 | $48,962 | — |
| MB | 0 | 0 | $0 | 2 | 2 | $4,655 | — |
| ME | 0 | 0 | $0 | 1 | 2 | $3,171 | — |
| MI | 0 | 0 | $0 | 4 | 4 | $18,838 | — |
| MN | 0 | 0 | $0 | 5 | 6 | $13,666 | — |
| MO | 0 | 0 | $0 | 7 | 10 | $22,089 | — |

### Q-57_results.md

# Q-57 Results — Craftmade (clli, org_id=149)
- **Query**: Q-57 — Cross-Sell Whitespace by Category
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-66_results.md

(not present — file does not exist or is empty)

### Q-67_results.md

# Q-67 Results — Craftmade (clli, org_id=149)
- **Query**: Q-67 — Geographic Revenue Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| state | prior_gmv | current_gmv | gmv_change_pct | current_customers | prior_customers | customer_change | current_orders |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TX | $2.6M | $3.2M | 21.90 | 164 | 148 | 16 | 4,231 |
| GA | $917,563 | $1.0M | 9.70 | 91 | 90 | 1 | 3,254 |
| NC | $1.1M | $907,001 | -14.90 | 95 | 81 | 14 | 1,563 |
| Unknown | $1.3M | $893,590 | -30 | 102 | 103 | -1 | 13,680 |
| AR | $645,871 | $658,906 | 2 | 48 | 48 | 0 | 619 |
| OK | $657,759 | $575,295 | -12.50 | 38 | 41 | -3 | 588 |
| FL | $788,901 | $553,907 | -29.80 | 133 | 130 | 3 | 1,534 |
| AL | $502,866 | $539,805 | 7.30 | 51 | 48 | 3 | 546 |
| TN | $529,053 | $491,359 | -7.10 | 66 | 59 | 7 | 953 |
| CA | $343,865 | $477,911 | 39 | 157 | 91 | 66 | 1,474 |
| MO | $323,636 | $402,877 | 24.50 | 66 | 59 | 7 | 604 |
| IN | $277,049 | $385,812 | 39.30 | 57 | 54 | 3 | 486 |
| OH | $223,174 | $355,551 | 59.30 | 90 | 75 | 15 | 790 |
| SC | $395,524 | $353,360 | -10.70 | 67 | 61 | 6 | 847 |
| VA | $290,025 | $346,635 | 19.50 | 58 | 56 | 2 | 862 |
| KS | $268,320 | $322,436 | 20.20 | 37 | 36 | 1 | 336 |
| KY | $281,478 | $312,796 | 11.10 | 46 | 48 | -2 | 541 |
| UT | $278,924 | $281,343 | 0.90 | 46 | 49 | -3 | 456 |
| PA | $128,079 | $267,066 | 108.50 | 64 | 57 | 7 | 661 |
| LA | $254,650 | $239,767 | -5.80 | 66 | 54 | 12 | 531 |
| IL | $269,039 | $238,810 | -11.20 | 70 | 68 | 2 | 622 |
| AZ | $187,859 | $230,652 | 22.80 | 64 | 64 | 0 | 526 |
| NY | $202,764 | $187,311 | -7.60 | 77 | 66 | 11 | 716 |
| MS | $139,444 | $184,743 | 32.50 | 31 | 30 | 1 | 304 |
| CO | $91,187 | $177,381 | 94.50 | 60 | 62 | -2 | 392 |

### Q-68_results.md

# Q-68 Results — Craftmade (clli, org_id=149)
- **Query**: Q-68 — Spending Contraction Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| customer_bill_to_name | primary_state | customer_spend | peak_spend | gap_to_peak | current_vs_peak_pct | active_months |
| --- | --- | --- | --- | --- | --- | --- |
|  | Unknown | $834,749 | $1.7M | $839,383 | 49.90 | 13 |
|  | TX | $203,242 | $1.0M | $806,943 | 20.10 | 13 |
|  | AZ | $14,445 | $628,491 | $614,046 | 2.30 | 5 |
|  | Unknown | $367,817 | $874,328 | $506,511 | 42.10 | 13 |
|  | WV | $58,793 | $394,550 | $335,757 | 14.90 | 12 |
|  | VA | $320,975 | $645,917 | $324,942 | 49.70 | 13 |
|  | AR | $223,860 | $546,540 | $322,679 | 41 | 13 |
|  | WV | $54,891 | $354,802 | $299,911 | 15.50 | 5 |
|  | WA | $5,355 | $304,531 | $299,176 | 1.80 | 6 |
|  | TX | $86,267 | $358,745 | $272,477 | 24 | 13 |
|  | WA | $20,422 | $290,665 | $270,243 | 7 | 10 |
|  | WA | $272,285 | $540,624 | $268,339 | 50.40 | 13 |
|  | SC | $36,057 | $302,169 | $266,111 | 11.90 | 13 |
|  | UT | $72,622 | $322,582 | $249,959 | 22.50 | 9 |
|  | Unknown | $169,488 | $419,121 | $249,633 | 40.40 | 13 |
|  | VA | $3,992 | $250,289 | $246,297 | 1.60 | 5 |
|  | AZ | $483,174 | $727,668 | $244,494 | 66.40 | 9 |
|  | FL | $2,079 | $244,456 | $242,377 | 0.90 | 1 |
|  | Unknown | $129,036 | $365,399 | $236,363 | 35.30 | 13 |
|  | VA | $208,816 | $433,307 | $224,491 | 48.20 | 10 |

### Q-ORG-DECAY_results.md

# Q-ORG-DECAY Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-DECAY — Account Reorder Decay Detection
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-DECAY_items_results.md

# Q-ORG-DECAY-items Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-DECAY-items — Item-Level Reorder Decay
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| customer_code | customer_name | item_number | description | reorder_count | avg_interval | days_since_last | decay_ratio | ltm_revenue | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 44030 |  | PHA52BNK3-BNGW | Phaze 3 blade 52" fan - | 8 | 11.30 | 322 | 28.50 | 63,459.26 | DECAY_DETECTED |
| 70076 |  | DCF52BNK5C1W | Decorators Choice 52" w/ | 89 | 4.60 | 139 | 30.20 | 45,567.60 | DECAY_DETECTED |
| 31900 |  | HE52BNK5-LED | 52" Helios fan - BNK | 22 | 14.70 | 215 | 14.60 | 79,383.50 | DECAY_DETECTED |
| 44030 |  | PHZ52BNK3-BNGW | Phaze II 3 blade fan | 19 | 21.40 | 139 | 6.50 | 144,947.22 | DECAY_DETECTED |
| 106010 |  | TMPH52OB5 | Tempo Hugger 52" fan - | 62 | 4.40 | 271 | 61.60 | 13,898.50 | DECAY_DETECTED |
| 44515 |  | Z421-MN-LED | Single LED Flood | 140 | 3.60 | 49 | 13.60 | 56,377.44 | DECAY_DETECTED |
| 9996 |  | EPHA52FB3 | Phaze 3 blade 52" fan - | 10 | 25.10 | 253 | 10.10 | 61,435.20 | DECAY_DETECTED |
| 44004 |  | CK1000-W | Builder Chime KIT - W | 39 | 12.50 | 40 | 3.20 | 174,297.90 | DECAY_DETECTED |
| 106010 |  | CE3-WSB | 3 Tube Eighties Redux | 51 | 4.50 | 159 | 35.30 | 11,567.50 | DECAY_DETECTED |
| 50201 |  | INS54W3 | Inspo 54" fan - W | 27 | 13.90 | 163 | 11.70 | 28,423 | DECAY_DETECTED |
| 2071 |  | ECF104FB5-FBGW | EOS fan with clear | 58 | 6.60 | 161 | 24.40 | 12,901 | DECAY_DETECTED |
| 106010 |  | CE3-FBSB | 3 Tube Eighties Redux | 34 | 4.90 | 198 | 40.40 | 7,766.75 | DECAY_DETECTED |
| 70018 |  | INT52ESP3 | Intrepid 52" fan - ESP | 10 | 13.90 | 184 | 13.20 | 22,862.25 | DECAY_DETECTED |
| 106010 |  | CA4-RC | CARVED WESTMINSTER-LONG | 23 | 5.30 | 218 | 41.10 | 7,216 | DECAY_DETECTED |
| 9800 |  | LAV44MWW4LK-LED | 44" Laval fan w/ light | 29 | 16.30 | 64 | 3.90 | 73,481.50 | DECAY_DETECTED |
| 70018 |  | P211FB5-52FBGW | Pro Plus fan with white | 49 | 10.30 | 42 | 4.10 | 70,623.42 | DECAY_DETECTED |
| 9996 |  | EPHA52BNK5-BNGW | Phaze 5 blade 52" fan - | 12 | 21 | 274 | 13 | 20,736.80 | DECAY_DETECTED |
| 44910 |  | Z422-MN-LED | Double LED Flood | 50 | 9.60 | 64 | 6.70 | 40,471.20 | DECAY_DETECTED |
| 3919 |  | CTPAB-BK | Patina Aged Brs Resonanc | 108 | 3.50 | 150 | 42.90 | 6,155.11 | DECAY_DETECTED |
| 6050 |  | CPT52FB5 | Captivate 52" fan - FB | 34 | 7.50 | 283 | 37.70 | 5,756.80 | DECAY_DETECTED |
| 44515 |  | P104FB5-52FBGW | Pro Plus fan with 4 | 137 | 3.90 | 12 | 3.10 | 70,074.94 | DECAY_DETECTED |
| 9800 |  | TEA52ESP4 | Teana 52" fan - ESP | 52 | 9.90 | 28 | 2.80 | 70,505 | SLOWING |
| 9800 |  | P112ESP5-52ESPWLN | Pro Plus fan with slim | 5 | 18 | 315 | 17.50 | 11,144.19 | DECAY_DETECTED |
| 3919 |  | LK2802-FB-LED | 2 light LED bowl LK w/ | 97 | 4.40 | 104 | 23.60 | 7,416.12 | DECAY_DETECTED |
| 44030 |  | PHA52FB3 | Phaze 3 blade 52" fan - | 7 | 27 | 230 | 8.50 | 20,332.40 | DECAY_DETECTED |
| 9800 |  | EPHA52BNK5-BNGW | Phaze 5 blade 52" fan - | 46 | 10.70 | 55 | 5.10 | 33,484.65 | DECAY_DETECTED |
| 40138 |  | MCY52FB4 | McCoy 52" fan with | 20 | 20.70 | 54 | 2.60 | 58,075.60 | SLOWING |
| 9800 |  | P211BNK5-52BNGW | Pro Plus fan with white | 22 | 10.10 | 232 | 23 | 6,455.39 | DECAY_DETECTED |
| 70018 |  | PHA52FB5 | Phaze 5 blade 52" fan - | 20 | 20.80 | 54 | 2.60 | 54,676 | SLOWING |
| 31413 |  | P2001-NT | Pendant 1 light - | 51 | 7.20 | 176 | 24.40 | 5,529.59 | DECAY_DETECTED |

### Q-ORG-NBP_results.md

# Q-ORG-NBP Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-NBP — Next Best Product — Collaborative Filtering
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-ORG-CONTRACTION_results.md

# Q-ORG-CONTRACTION Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-CONTRACTION — Account Spending Contraction & Displacement
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| customer_code | customer_name | state | total_ltm | total_prior | total_yoy_pct | ecat_ltm | ecat_prior | ecat_yoy_pct | signal_type |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 106010 |  |  | 729,998.18 | 1,788,691.14 | -59.20 | 0 | 0 | — | CONTRACTING |
| 44004 |  |  | 545,053.65 | 1,414,384.33 | -61.50 | 0 | 0 | — | CONTRACTING |
| 1667 |  |  | 92,186.61 | 899,201.97 | -89.70 | 0 | 0 | — | CONTRACTING |
| 5282 |  |  | 208,171.11 | 957,250.85 | -78.30 | 0 | 0 | — | CONTRACTING |
| 9802 |  |  | 1,021,173.22 | 1,528,896.74 | -33.20 | 0 | 0 | — | CONTRACTING |
| 21883 |  |  | 273,503.07 | 14,760.69 | 1,752.90 | 0 | 3,219 | -100 | COMPETITIVE_DISPLACEMENT |
| 4245 |  |  | 164,014.47 | 403,857.86 | -59.40 | 0 | 0 | — | CONTRACTING |
| 200001 |  |  | 49,617.01 | 286,645.60 | -82.70 | 0 | 0 | — | CONTRACTING |
| 34145 |  |  | 187,614.70 | 422,120.06 | -55.60 | 0 | 0 | — | CONTRACTING |
| 3919 |  |  | 666,618.29 | 897,412.84 | -25.70 | 0 | 0 | — | CONTRACTING |
| 44950 |  |  | 355,067.10 | 581,832.82 | -39 | 0 | 0 | — | CONTRACTING |
| 31900 |  |  | 260,028.48 | 462,590.27 | -43.80 | 0 | 0 | — | CONTRACTING |
| 44010 |  |  | 41,502.69 | 241,615.93 | -82.80 | 0 | 0 | — | CONTRACTING |
| 60602 |  |  | 32,721.31 | 215,763.75 | -84.80 | 0 | 0 | — | CONTRACTING |
| 60559 |  |  | 535,914.56 | 685,557.49 | -21.80 | 0 | 0 | — | CONTRACTING |
| 46075 |  |  | 31,113.02 | 180,322.02 | -82.70 | 0 | 0 | — | CONTRACTING |
| 4034 |  |  | 159,608.46 | 306,649.07 | -48 | 6,463.75 | 4,732.50 | 36.60 | CONTRACTING |
| 60547 |  |  | 25,143.04 | 170,599.58 | -85.30 | 949.88 | 0 | — | CONTRACTING |
| 5088 |  |  | 75,001.03 | 214,347.65 | -65 | 2,163.03 | 0 | — | CONTRACTING |
| 13010 |  |  | 161,731.50 | 300,961.38 | -46.30 | 0 | 0 | — | CONTRACTING |
| 70056 |  |  | 392,828.68 | 515,415.12 | -23.80 | 8,272.25 | 2,642 | 213.10 | CONTRACTING |
| 15225 |  |  | 416,289.15 | 527,097.11 | -21 | 0 | 0 | — | CONTRACTING |
| 43880 |  |  | 272,754.94 | 379,726.51 | -28.20 | 0 | 0 | — | CONTRACTING |
| 44030 |  |  | 301,482.21 | 407,879.18 | -26.10 | 0 | 0 | — | CONTRACTING |
| 22490 |  |  | 25,561.64 | 128,557.39 | -80.10 | 0 | 0 | — | CONTRACTING |

### Q-ORG-VELOCITY_results.md

# Q-ORG-VELOCITY Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-VELOCITY — Account Quarterly Velocity Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 15
- **Run date**: 2026-06-17


| customer_code | customer_name | accel_quarters | peak_quarter_revenue | max_qoq | trajectory |
| --- | --- | --- | --- | --- | --- |
| 9996 |  | 3 | 622,311.85 | 179.90 | [{'quarter': '2025-07-01', 'revenue': 511637.4, 'qoq_pct': 87.1}, {'quarter': '2025-10-01', 'revenue': 152989.91, 'qoq_pct': -70.1}, {'quarter': '2026-01-01', 'revenue': 222322.9, 'qoq_pct': 45.3}, {'quarter': '2026-04-01', 'revenue': 622311.85, 'qoq_pct': 179.9}] |
| 18755 |  | 2 | 122,883.26 | 6,048.80 | [{'quarter': '2025-07-01', 'revenue': 14014.9, 'qoq_pct': 6048.8}, {'quarter': '2025-10-01', 'revenue': 5070.15, 'qoq_pct': -63.8}, {'quarter': '2026-01-01', 'revenue': 122883.26, 'qoq_pct': 2323.7}, {'quarter': '2026-04-01', 'revenue': 1320.9, 'qoq_pct': -98.9}] |
| 10102 |  | 2 | 118,617.94 | 49.30 | [{'quarter': '2025-07-01', 'revenue': 79468.63, 'qoq_pct': -45.1}, {'quarter': '2025-10-01', 'revenue': 118617.94, 'qoq_pct': 49.3}, {'quarter': '2026-01-01', 'revenue': 45721.59, 'qoq_pct': -61.5}, {'quarter': '2026-04-01', 'revenue': 60854.23, 'qoq_pct': 33.1}] |
| 49325 |  | 3 | 108,009.14 | 2,905.70 | [{'quarter': '2025-07-01', 'revenue': 158.25, 'qoq_pct': None}, {'quarter': '2025-10-01', 'revenue': 843.0, 'qoq_pct': 432.7}, {'quarter': '2026-01-01', 'revenue': 25337.96, 'qoq_pct': 2905.7}, {'quarter': '2026-04-01', 'revenue': 108009.14, 'qoq_pct': 326.3}] |
| 31900 |  | 2 | 106,274.74 | 46.50 | [{'quarter': '2025-07-01', 'revenue': 106274.74, 'qoq_pct': 25.9}, {'quarter': '2025-10-01', 'revenue': 32302.15, 'qoq_pct': -69.6}, {'quarter': '2026-01-01', 'revenue': 47321.87, 'qoq_pct': 46.5}, {'quarter': '2026-04-01', 'revenue': 69136.08, 'qoq_pct': 46.1}] |
| 50017 |  | 2 | 104,277.60 | 593.50 | [{'quarter': '2025-07-01', 'revenue': 104277.6, 'qoq_pct': 512.0}, {'quarter': '2025-10-01', 'revenue': 12986.07, 'qoq_pct': -87.5}, {'quarter': '2026-01-01', 'revenue': 90054.94, 'qoq_pct': 593.5}, {'quarter': '2026-04-01', 'revenue': 17662.09, 'qoq_pct': -80.4}] |
| 50200 |  | 2 | 102,376.70 | 67.30 | [{'quarter': '2025-07-01', 'revenue': 102376.7, 'qoq_pct': 66.7}, {'quarter': '2025-10-01', 'revenue': 37040.75, 'qoq_pct': -63.8}, {'quarter': '2026-01-01', 'revenue': 28946.24, 'qoq_pct': -21.9}, {'quarter': '2026-04-01', 'revenue': 48425.62, 'qoq_pct': 67.3}] |
| 40000 |  | 2 | 97,493.13 | 35 | [{'quarter': '2025-07-01', 'revenue': 97493.13, 'qoq_pct': 1.4}, {'quarter': '2025-10-01', 'revenue': 27775.31, 'qoq_pct': -71.5}, {'quarter': '2026-01-01', 'revenue': 37496.72, 'qoq_pct': 35.0}, {'quarter': '2026-04-01', 'revenue': 49389.47, 'qoq_pct': 31.7}] |
| 1120 |  | 2 | 87,277.28 | 163.70 | [{'quarter': '2025-07-01', 'revenue': 64622.9, 'qoq_pct': 163.7}, {'quarter': '2025-10-01', 'revenue': 66613.1, 'qoq_pct': 3.1}, {'quarter': '2026-01-01', 'revenue': 87277.28, 'qoq_pct': 31.0}, {'quarter': '2026-04-01', 'revenue': 63414.36, 'qoq_pct': -27.3}] |
| 43971 |  | 2 | 83,117.62 | 490.10 | [{'quarter': '2025-07-01', 'revenue': 14086.22, 'qoq_pct': -83.8}, {'quarter': '2025-10-01', 'revenue': 83117.62, 'qoq_pct': 490.1}, {'quarter': '2026-01-01', 'revenue': 5890.92, 'qoq_pct': -92.9}, {'quarter': '2026-04-01', 'revenue': 26509.17, 'qoq_pct': 350.0}] |
| 44027 |  | 2 | 76,514.14 | 26,550.70 | [{'quarter': '2025-07-01', 'revenue': 217.75, 'qoq_pct': -99.4}, {'quarter': '2025-10-01', 'revenue': 1151.54, 'qoq_pct': 428.8}, {'quarter': '2026-01-01', 'revenue': 287.1, 'qoq_pct': -75.1}, {'quarter': '2026-04-01', 'revenue': 76514.14, 'qoq_pct': 26550.7}] |
| 44506 |  | 2 | 72,969.77 | 58.90 | [{'quarter': '2025-07-01', 'revenue': 72969.77, 'qoq_pct': 58.9}, {'quarter': '2025-10-01', 'revenue': 58320.31, 'qoq_pct': -20.1}, {'quarter': '2026-01-01', 'revenue': 50798.92, 'qoq_pct': -12.9}, {'quarter': '2026-04-01', 'revenue': 71720.62, 'qoq_pct': 41.2}] |
| 43638 |  | 2 | 70,897.40 | 56.90 | [{'quarter': '2025-07-01', 'revenue': 45385.52, 'qoq_pct': -5.7}, {'quarter': '2025-10-01', 'revenue': 29639.3, 'qoq_pct': -34.7}, {'quarter': '2026-01-01', 'revenue': 45196.37, 'qoq_pct': 52.5}, {'quarter': '2026-04-01', 'revenue': 70897.4, 'qoq_pct': 56.9}] |
| 40350 |  | 2 | 69,543.65 | 4,534.30 | [{'quarter': '2025-07-01', 'revenue': 7599.87, 'qoq_pct': 99.2}, {'quarter': '2025-10-01', 'revenue': 2498.75, 'qoq_pct': -67.1}, {'quarter': '2026-01-01', 'revenue': 1500.63, 'qoq_pct': -39.9}, {'quarter': '2026-04-01', 'revenue': 69543.65, 'qoq_pct': 4534.3}] |
| 30055 |  | 2 | 58,054.30 | 7,785.10 | [{'quarter': '2025-07-01', 'revenue': 736.25, 'qoq_pct': 68.6}, {'quarter': '2026-01-01', 'revenue': 58054.3, 'qoq_pct': 7785.1}, {'quarter': '2026-04-01', 'revenue': 117.74, 'qoq_pct': -99.8}] |

### Q-ORG-STOCKOUT_results.md

# Q-ORG-STOCKOUT Results — Craftmade (clli, org_id=149)
- **Query**: Q-ORG-STOCKOUT — Stock-Out Impact with Customer Mapping
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 7
- **Run date**: 2026-06-17


| item_number | long_description | collection_code | ltm_revenue | ltm_units | qty_on_backorder | next_scheduled_receipt_date | top_customers | alternatives |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BW414AG3 | Bellows IV 14" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Aged Bronze Textured w/ Aged Bronze Blades; Not Light Kit Adaptable | COL53 | 281,687.35 | 1,562 | 10 | 2026-07-20 | [{'customer': '1STOPLIGHTING-I', 'revenue': 52219.38}, {'customer': 'FERGUSONHOME.COM', 'revenue': 27861.72}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 19799.79}, {'customer': 'DELMAR FANS', 'revenue': 12045.15}, {'customer': 'WAYFAIR LLC-I', 'revenue': 11717.96}, {'customer': 'LUMENS LIGHT + LIVING-I', 'revenue': 7606.36}, {'customer': 'LIGHTING INC.', 'revenue': 7605.0}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 7374.85}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 4563.0}, {'customer': 'LAMPS PLUS', 'revenue': 4212.0}, {'customer': 'JABEN HOLDINGS INC-I', 'revenue': 3861.0}, {'customer': 'ELLER ENTERPRISES', 'revenue': 3716.7}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 3705.0}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 3120.0}, {'customer': 'HOUZZ SHOP LLC', 'revenue': 3120.0}, {'customer': 'DESIGN LIGHTING GROUP LLC-C', 'revenue': 3120.0}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 2730.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 2593.5}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 2535.0}, {'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 2363.4}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 2340.0}, {'customer': 'TRI SUPPLY', 'revenue': 2340.0}, {'customer': 'PASSION LIGHTING', 'revenue': 2340.0}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 2340.0}, {'customer': "GRAHAM'S LIGHTING INC", 'revenue': 2145.0}, {'customer': 'VILLA LIGHTING SUPPLY INC', 'revenue': 1950.0}, {'customer': 'MASTERPIECE LIGHTING', 'revenue': 1950.0}, {'customer': 'NET RETAILERS LLC-CII ONLY', 'revenue': 1950.0}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 1766.7}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 1755.0}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 1755.0}, {'customer': 'CAPITOL LIGHTING', 'revenue': 1755.0}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 1725.75}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 1560.0}, {'customer': 'AA PORTER', 'revenue': 1560.0}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 1376.7}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 1365.0}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 1365.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 1335.75}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 1318.98}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 1269.45}, {'customer': 'GOING DECOR', 'revenue': 1170.0}, {'customer': 'VALUE LIGHTING INC', 'revenue': 1170.0}, {'customer': 'LOWE ELECTRIC SUPPLY CO', 'revenue': 1170.0}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 1170.0}, {'customer': 'A & W LIGHTING', 'revenue': 1170.0}, {'customer': 'SONEPAR-USA', 'revenue': 1170.0}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 1170.0}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 1038.9}, {'customer': 'MAYER ELECTRIC SUPPLY CO INC', 'revenue': 975.0}, {'customer': 'STATE ELECTRIC SUPPLY CO', 'revenue': 945.75}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 945.75}, {'customer': 'ATHENIA MASON SUPPLY WILMINGTO', 'revenue': 928.2}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 877.5}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 803.4}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 780.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 780.0}, {'customer': 'MADISON LIGHTING', 'revenue': 780.0}, {'customer': 'MANASQUAN LIGHTING', 'revenue': 780.0}, {'customer': 'LIGHTING INC', 'revenue': 780.0}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 780.0}, {'customer': 'GREER LIGHTING CENTER LLC', 'revenue': 780.0}, {'customer': 'AFFORDABLE LIGHTING', 'revenue': 780.0}, {'customer': 'LIGHTING ETC', 'revenue': 780.0}, {'customer': 'CAJUN ELECTRIC, LLC', 'revenue': 780.0}, {'customer': 'WILLIAM L HART DESIGNS LLC', 'revenue': 780.0}, {'customer': 'LEGACY LIGHTING LLC', 'revenue': 716.0}, {'customer': 'POWER DESIGN RESOURCES', 'revenue': 704.0}, {'customer': 'PROGRESSIVE LIGHTING-I', 'revenue': 702.0}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 686.4}, {'customer': 'RGM DISTRIBUTION INC-I', 'revenue': 620.1}, {'customer': 'PINE GROVE ELEC SPLY', 'revenue': 585.0}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 585.0}, {'customer': "RON'S LUMBER AND HOME CENTER", 'revenue': 585.0}, {'customer': 'AMERICAN LIGHTING', 'revenue': 585.0}, {'customer': 'MATHES OF ALABAMA', 'revenue': 585.0}, {'customer': 'THE LIGHTING STUDIO, LLC', 'revenue': 585.0}, {'customer': 'KEIDEL SUPPLY CO INC', 'revenue': 585.0}, {'customer': 'T J S SUPPLY CO', 'revenue': 585.0}, {'customer': 'LED CAPSTONE INC.', 'revenue': 585.0}, {'customer': 'FAN DIEGO INC', 'revenue': 569.0}, {'customer': 'DUNCAN LIGHTING & HOME-I', 'revenue': 555.75}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 549.9}, {'customer': 'CAPE ELECTRIC SUPPLY', 'revenue': 538.2}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 526.5}, {'customer': 'ARCADIAN LIGHTING INC-I', 'revenue': 526.5}, {'customer': 'HOUSE ACCOUNT', 'revenue': 427.34}, {'customer': 'MENARDS - CRAFTMADE', 'revenue': 407.32}, {'customer': 'LIGHTING WORLD DECORATOR', 'revenue': 390.0}, {'customer': 'JPR LIGHTING INC', 'revenue': 390.0}, {'customer': 'SOUTHERN LTG GALLERY', 'revenue': 390.0}, {'customer': "FARREY'S WHOLESALE HARDWARE", 'revenue': 390.0}, {'customer': 'ONE SOURCE LIGHTING', 'revenue': 390.0}, {'customer': 'BES LIGHTING & HOME', 'revenue': 390.0}, {'customer': 'BUILD IT FAB INC', 'revenue': 390.0}, {'customer': 'HALL ELECTRIC', 'revenue': 390.0}, {'customer': 'SHEALY ELECTRIC CO', 'revenue': 390.0}, {'customer': 'TEC OF JONESBORO INC', 'revenue': 390.0}, {'customer': 'TECHE ELECTRIC', 'revenue': 390.0}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 390.0}, {'customer': 'BETTER HOMES SUPPLY', 'revenue': 390.0}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 390.0}, {'customer': 'LIGHTING CORNER, THE', 'revenue': 390.0}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 390.0}, {'customer': 'HAYNEEDLE,INC-I', 'revenue': 390.0}, {'customer': 'LOW COUNTRY LIGHTING INC', 'revenue': 390.0}, {'customer': 'ZORO TOOLS, INC. DBA ZORO', 'revenue': 390.0}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 390.0}, {'customer': 'ECHO ELECTRIC SUPPLY', 'revenue': 390.0}, {'customer': None, 'revenue': 390.0}, {'customer': 'CR LIGHTING', 'revenue': 390.0}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 390.0}, {'customer': 'LIGHTING PLUS', 'revenue': 390.0}, {'customer': 'LIGHT HOUSE, THE', 'revenue': 390.0}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 390.0}, {'customer': 'MADDUX LIGHTING GALLERY& SUPPL', 'revenue': 390.0}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 390.0}, {'customer': "LYDIA'S", 'revenue': 390.0}, {'customer': 'LIGHT DEPOT LLC', 'revenue': 390.0}, {'customer': 'METRO LIGHTING', 'revenue': 370.5}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 351.0}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 351.0}, {'customer': 'RICHARDSON HOUSE OF FIXTURES', 'revenue': 214.5}, {'customer': 'UNION LUMINAIRES ET DECOR', 'revenue': 214.5}, {'customer': 'ROYAUME LUMINAIRE LANDAUDIERE', 'revenue': 214.5}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 206.7}, {'customer': 'FREY ELECTRIC INC', 'revenue': 195.0}, {'customer': 'FORD BOYD INTERIORS DBA VERVE', 'revenue': 195.0}, {'customer': 'DOMINION ELECTRIC SUPPLY CO', 'revenue': 195.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 195.0}, {'customer': 'IDAHO DREAMING', 'revenue': 195.0}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 195.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 195.0}, {'customer': 'WINSUPPLY INC', 'revenue': 195.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 195.0}, {'customer': 'WEST BROWARD BULB INC', 'revenue': 195.0}, {'customer': 'KENYON-NOBLE LUMBER CO', 'revenue': 195.0}, {'customer': 'JOHNSON BURKS SUPPLY COMPANY', 'revenue': 195.0}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 195.0}, {'customer': 'VILLAGE LIGHTING & SUPPLY INC', 'revenue': 195.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 195.0}, {'customer': 'HYE LIGHTING CO INC', 'revenue': 195.0}, {'customer': 'NORTHWOOD LIGHTING', 'revenue': 195.0}, {'customer': 'M & M LIGHTING LP', 'revenue': 195.0}, {'customer': 'TEC OF NORTH LITTLE ROCK', 'revenue': 195.0}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 195.0}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 195.0}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 195.0}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 195.0}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 195.0}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 195.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 195.0}, {'customer': 'WILSON LIGHTING STL', 'revenue': 195.0}, {'customer': 'R WILSON INC', 'revenue': 195.0}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 195.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 195.0}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 195.0}, {'customer': 'COLEY ELECTRIC-WAYCROSS', 'revenue': 195.0}, {'customer': 'J. H. LARSON COMPANY', 'revenue': 195.0}, {'customer': 'LUMENAREA', 'revenue': 195.0}, {'customer': 'C.E.S. CO NC DIVISION', 'revenue': 195.0}, {'customer': 'C.E.D.', 'revenue': 195.0}, {'customer': 'USESI', 'revenue': 195.0}, {'customer': 'FILAMENT INC', 'revenue': 195.0}, {'customer': 'KINGS WAGON YARD', 'revenue': 195.0}, {'customer': 'LIGHTING ORIGINALS INC.', 'revenue': 193.05}, {'customer': 'ROYAUME LUMINAIRE STE JULIE', 'revenue': 171.6}, {'customer': 'FANS PLUS', 'revenue': 169.65}, {'customer': 'LOFINGS LIGHTING', 'revenue': 167.7}, {'customer': 'CUSTOMER SERVICE ELECTRIC SUPP', 'revenue': 156.0}, {'customer': 'Craftmade Warranty Account', 'revenue': 0.0}] | [{'item': 'BW414BNK3', 'desc': 'Bellows IV 14" 3-Blade Ceiling Fan in Brushed Polished Nickel w/ Brushed Polished Nickel Blades; Not Light Kit Adaptable', 'available': 110}] |
| BW321AG3 | Bellows III 18" 3-Blade Indoor/Outdoor (Damp) Ceiling Fan in Aged Bronze Textured w/ Aged Bronze Blades; Not Light Kit Adaptable | COL52 | 266,996.31 | 1,143 | 12 | 2026-07-20 | [{'customer': '1STOPLIGHTING-I', 'revenue': 30920.77}, {'customer': 'WAYFAIR LLC-I', 'revenue': 26810.83}, {'customer': 'FERGUSONHOME.COM', 'revenue': 18009.6}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 12092.4}, {'customer': 'LAMPS PLUS', 'revenue': 7497.99}, {'customer': 'LUMENS LIGHT + LIVING-I', 'revenue': 6942.6}, {'customer': 'TECHE ELECTRIC', 'revenue': 6552.0}, {'customer': 'LIGHTING INC.', 'revenue': 6360.4}, {'customer': 'DELMAR FANS', 'revenue': 6350.4}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 6299.9}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 4929.35}, {'customer': 'SPECIALTY LIGHTING GROUP LLC', 'revenue': 4536.0}, {'customer': 'AA PORTER', 'revenue': 4536.0}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 4095.0}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 3742.2}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 3558.2}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 3528.0}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 3276.0}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3192.8}, {'customer': "GRAHAM'S LIGHTING INC", 'revenue': 3024.0}, {'customer': 'NOTOCO INDUSTRIES', 'revenue': 2802.2}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 2802.2}, {'customer': 'PARALLAX INDUSTRIES, INC.', 'revenue': 2797.2}, {'customer': 'ELLER ENTERPRISES', 'revenue': 2772.0}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 2764.0}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 2721.6}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 2520.0}, {'customer': "ELAINE EVERETT'S LIGHTING", 'revenue': 2520.0}, {'customer': 'PASSION LIGHTING', 'revenue': 2016.0}, {'customer': 'LOWE ELECTRIC SUPPLY CO', 'revenue': 1764.0}, {'customer': "HAGEN'S", 'revenue': 1764.0}, {'customer': 'GOING DECOR', 'revenue': 1542.2}, {'customer': 'GALLERY OF LTG', 'revenue': 1512.0}, {'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 1512.0}, {'customer': 'ABC LIGHTING', 'revenue': 1512.0}, {'customer': 'M & M LIGHTING LP', 'revenue': 1512.0}, {'customer': 'DESIGN LIGHTING GROUP LLC-C', 'revenue': 1512.0}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 1499.4}, {'customer': 'LIGHTOLOGY LLC', 'revenue': 1421.28}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 1260.0}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 1260.0}, {'customer': 'TEC OF JONESBORO INC', 'revenue': 1260.0}, {'customer': 'FAN DIEGO INC', 'revenue': 1199.5}, {'customer': 'METRO LIGHTING', 'revenue': 1134.0}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 1105.2}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 1008.0}, {'customer': "ARMSTRONG'S SUPPLY CO", 'revenue': 1008.0}, {'customer': "JOSEPH'S ELECTRICAL CENTER", 'revenue': 1008.0}, {'customer': 'LIGHTING SHOWROOM INC', 'revenue': 1008.0}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 1008.0}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 1008.0}, {'customer': 'LABELLE CABINETRY & LTG-', 'revenue': 1008.0}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 1008.0}, {'customer': 'SOUTHLAND PLUMBING SUPPLY INC', 'revenue': 1008.0}, {'customer': 'LIGHTS OF OCONEE LLC', 'revenue': 1008.0}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 937.44}, {'customer': 'JABEN HOLDINGS INC-I', 'revenue': 907.2}, {'customer': 'MULTI LUMINAIRE ST. HUBERT', 'revenue': 881.43}, {'customer': 'LIGHTSHINE INC', 'revenue': 771.1}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 756.0}, {'customer': "CAPPADONNA'S OF ARIZONA", 'revenue': 756.0}, {'customer': 'NORTHERN LIGHTS & FANS LLC', 'revenue': 756.0}, {'customer': 'MID-SOUTH LIGHTING', 'revenue': 756.0}, {'customer': "ISABELLE'S LIGHTING INC.", 'revenue': 756.0}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 756.0}, {'customer': 'GADSDEN LIGHTING', 'revenue': 756.0}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 756.0}, {'customer': 'C.E.S.TX DIV', 'revenue': 756.0}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 756.0}, {'customer': None, 'revenue': 756.0}, {'customer': 'SANDERS SUPPLY INC', 'revenue': 756.0}, {'customer': 'ELITEFIXTURES.COM-I', 'revenue': 756.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 756.0}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 756.0}, {'customer': 'GATEWAY LTG & DESIGN INC', 'revenue': 756.0}, {'customer': 'LIGHTING WORKS', 'revenue': 756.0}, {'customer': 'HARDWOOD FLOORS & MORE-CXT', 'revenue': 756.0}, {'customer': 'ELLEN LIGHTING & HARDWARE', 'revenue': 756.0}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 756.0}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 748.0}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 703.08}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 680.4}, {'customer': 'DORIAN DRAKE INTERNATIONAL INC', 'revenue': 642.6}, {'customer': 'BLACK DIAMOND ACQUISITIONS', 'revenue': 504.0}, {'customer': "LYDIA'S", 'revenue': 504.0}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 504.0}, {'customer': 'COLEY ELECTRIC-WAYCROSS', 'revenue': 504.0}, {'customer': 'HI-LIGHT DECORATING', 'revenue': 504.0}, {'customer': 'REVERE ELECTRIC SUPPLY', 'revenue': 504.0}, {'customer': 'UNIVERSAL LIGHTS INC', 'revenue': 504.0}, {'customer': 'LIGHTING & REFLECTIONS', 'revenue': 504.0}, {'customer': 'STEVENS LIGHTING FIXTURE CO', 'revenue': 504.0}, {'customer': 'GROSS LIGHTING & HOME', 'revenue': 504.0}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 504.0}, {'customer': 'COMPLETE LIGHTING OF TAMPA', 'revenue': 504.0}, {'customer': 'CAPISTRANO LIGHTING', 'revenue': 504.0}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 504.0}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 504.0}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 504.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 504.0}, {'customer': 'HOUSE OF LIGHTS OF SANFORD INC', 'revenue': 504.0}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 504.0}, {'customer': 'HOME LIGHTING & SUPPLY INC', 'revenue': 504.0}, {'customer': 'SOUTHSIDE LIGHTING GALLERY', 'revenue': 504.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 478.8}, {'customer': 'CAPE ELECTRIC SUPPLY', 'revenue': 463.68}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 443.52}, {'customer': 'PC HOME CENTER', 'revenue': 428.4}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 424.12}, {'customer': 'ELFORD/TEIBER', 'revenue': 403.2}, {'customer': 'HOUSE ACCOUNT', 'revenue': 376.0}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 277.2}, {'customer': 'LUMINAIRES PAUL GREGOIRE INC', 'revenue': 277.2}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 267.1}, {'customer': 'TLC LIGHTING ON, LLC', 'revenue': 252.0}, {'customer': 'SHEALY ELECTRIC CO', 'revenue': 252.0}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 252.0}, {'customer': "RICK'S LIGHTING & SUPPLIES INC", 'revenue': 252.0}, {'customer': 'WEST BROWARD BULB INC', 'revenue': 252.0}, {'customer': 'LIGHTING EFX INC', 'revenue': 252.0}, {'customer': 'LIGHTING PLUS INC', 'revenue': 252.0}, {'customer': 'C.A.I. DESIGNS', 'revenue': 252.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 252.0}, {'customer': 'CONSTANT ELECTRIC', 'revenue': 252.0}, {'customer': 'QUIGLEY LIGHTING CO', 'revenue': 252.0}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 252.0}, {'customer': '1-800 MY LAMPS-I', 'revenue': 252.0}, {'customer': 'PRESTIGE LIGHTING AND DESIGN L', 'revenue': 252.0}, {'customer': 'NORTH AND SOUTH SALES', 'revenue': 252.0}, {'customer': 'CAROLINA LANTERNS & LIGHTING', 'revenue': 252.0}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 252.0}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 252.0}, {'customer': 'CAROLINA SUPPLY HOUSE INC', 'revenue': 252.0}, {'customer': 'LITE HOUSE INC', 'revenue': 252.0}, {'customer': 'ARIZONA LIGHTING CO OF YUMA', 'revenue': 252.0}, {'customer': 'PREMIER BATH, LTG & HDW LLC', 'revenue': 252.0}, {'customer': 'BEAUTIFUL THINGS', 'revenue': 252.0}, {'customer': 'HENSONS CARPET ONE', 'revenue': 252.0}, {'customer': 'EAST VALLEY FANS & BLINDS', 'revenue': 252.0}, {'customer': 'CAJUN ELECTRIC, LLC', 'revenue': 252.0}, {'customer': 'EDWARD JOY LIGHTING & ELEC SUP', 'revenue': 239.4}, {'customer': 'RE-LIGHTING', 'revenue': 235.62}, {'customer': None, 'revenue': 226.8}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 226.8}, {'customer': 'PROGRESSIVE LIGHTING-I', 'revenue': 226.8}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 226.8}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 214.2}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 214.2}, {'customer': 'HOME LIGHTING', 'revenue': 0.0}, {'customer': 'ECHO ELECTRIC SUPPLY', 'revenue': 0.0}, {'customer': 'IMAGINE MORE SERVICE CORP.', 'revenue': 0.0}, {'customer': 'Craftmade Warranty Account', 'revenue': 0.0}] | — |
| 50504-FB | Bolden 4 Light Vanity in Flat Black | COL234 | 193,427.01 | 3,290 | 3 | 2026-06-30 | [{'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 25723.39}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 15830.26}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 10297.33}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 9329.35}, {'customer': 'FERGUSONHOME.COM', 'revenue': 7044.93}, {'customer': 'LUXUR LIGHTING', 'revenue': 5460.9}, {'customer': 'METRO LIGHTING', 'revenue': 5371.26}, {'customer': 'T J S SUPPLY CO', 'revenue': 5276.0}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 4473.58}, {'customer': 'WAYFAIR LLC-I', 'revenue': 4341.11}, {'customer': 'TRI SUPPLY', 'revenue': 3660.5}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 3560.84}, {'customer': 'PREMIER INDUSTRIES INC', 'revenue': 3108.18}, {'customer': 'HEARTH & HOME', 'revenue': 2877.25}, {'customer': 'LIGHTING INC.', 'revenue': 2838.0}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 2784.35}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 2744.75}, {'customer': 'RICHARDSON LIGHTING LTD', 'revenue': 2698.95}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 2298.54}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 2290.39}, {'customer': 'CLARKSVILLE LIGHTING', 'revenue': 2271.75}, {'customer': 'AMERICAN LIGHTING', 'revenue': 2271.75}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 2053.32}, {'customer': '1STOPLIGHTING-I', 'revenue': 1968.79}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 1775.5}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 1681.08}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 1645.0}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 1514.5}, {'customer': None, 'revenue': 1285.0}, {'customer': 'R.D.H.S.INC', 'revenue': 1172.0}, {'customer': 'PASSION LIGHTING', 'revenue': 1165.0}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 1139.36}, {'customer': 'COFFMAN HOME DECOR-', 'revenue': 1106.75}, {'customer': 'DUNCAN CORPORATION', 'revenue': 1100.34}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 1097.45}, {'customer': 'TLC LIGHTING ON, LLC', 'revenue': 1048.5}, {'customer': 'AT HOME, LLC DBA HOME LIGHTING', 'revenue': 1048.5}, {'customer': 'ENCORE FLOORING & BLDG PROD', 'revenue': 1048.5}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 1025.25}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 990.25}, {'customer': 'Q E D', 'revenue': 932.0}, {'customer': 'ILLUMINATIONS', 'revenue': 929.07}, {'customer': 'W T LIGHTING', 'revenue': 880.75}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 851.62}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 830.05}, {'customer': "HAGEN'S", 'revenue': 815.5}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 796.29}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 792.78}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 745.25}, {'customer': 'SMITHFIELD LIGHTING CENTER', 'revenue': 699.0}, {'customer': 'LIGHTING EMPORIUM', 'revenue': 689.65}, {'customer': 'PC HOME CENTER', 'revenue': 647.75}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 644.25}, {'customer': 'PARALLAX INDUSTRIES, INC.', 'revenue': 616.51}, {'customer': "KELLY'S HOME CENTER", 'revenue': 613.8}, {'customer': 'PLATT ELECTRIC SUPPLY', 'revenue': 611.0}, {'customer': 'NOVA LIGHTING', 'revenue': 596.5}, {'customer': 'DELMAR FANS', 'revenue': 596.2}, {'customer': 'LITE HOUSE INC', 'revenue': 582.5}, {'customer': '43RD STREET LIGHTING', 'revenue': 582.5}, {'customer': 'C.E.S. CO NC DIVISION', 'revenue': 558.2}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 548.82}, {'customer': 'BRANDON LIGHTING INC', 'revenue': 545.25}, {'customer': 'LIGHTING & REFLECTIONS', 'revenue': 543.25}, {'customer': 'GOING DECOR', 'revenue': 542.0}, {'customer': 'BRAZORIA COUNTY LIGHTING', 'revenue': 542.0}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 527.75}, {'customer': 'COASTAL LIGHTING & SUPPLY INC', 'revenue': 524.25}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 524.25}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 505.61}, {'customer': None, 'revenue': 480.55}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 473.0}, {'customer': 'AA PORTER', 'revenue': 466.0}, {'customer': 'AMC LIGHTING & DECOR, INC.', 'revenue': 452.02}, {'customer': 'M.C.I. INC', 'revenue': 410.55}, {'customer': 'LOYDS ELECTRIC SUPPLY INC', 'revenue': 407.75}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 407.75}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 407.75}, {'customer': 'LUMEN NATION LLC', 'revenue': 406.5}, {'customer': "Dianna's Lighting Design & Con", 'revenue': 384.8}, {'customer': 'FLOOR BROKERS, THE', 'revenue': 359.0}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 353.0}, {'customer': 'KIRBY RISK SUPPLY CO INC', 'revenue': 349.5}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 349.5}, {'customer': 'HALL ELECTRIC', 'revenue': 349.5}, {'customer': 'RITE RUG CO.', 'revenue': 338.75}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 338.75}, {'customer': 'RIMROCK LIGHTING', 'revenue': 338.75}, {'customer': 'RE-LIGHTING', 'revenue': 332.02}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 328.59}, {'customer': 'KENYON-NOBLE LUMBER CO', 'revenue': 309.75}, {'customer': 'AMOS ELECTRIC SUPPLY COMPANY', 'revenue': 291.25}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 291.25}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 291.25}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 291.25}, {'customer': 'SUNDIAL LIGHTING LTD', 'revenue': 291.25}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 282.51}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 271.0}, {'customer': 'VILLAGE HOME STORES', 'revenue': 271.0}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 242.5}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 236.5}, {'customer': 'BETTER HOMES SUPPLY', 'revenue': 233.0}, {'customer': 'LIGHTING SPECIALTIES WAREHOUSE', 'revenue': 233.0}, {'customer': 'PARAMONT-EO INC', 'revenue': 233.0}, {'customer': 'COVERINGS LLC', 'revenue': 233.0}, {'customer': 'HERITAGE LIGHTING, LLC', 'revenue': 233.0}, {'customer': 'LIGHT HOUSE OF SUMTER, LLC', 'revenue': 226.59}, {'customer': 'ILLUMINATIONS INC', 'revenue': 206.78}, {'customer': 'ALPHA  SUPPLY CORP', 'revenue': 203.25}, {'customer': 'SOUTHSIDE LIGHTING GALLERY', 'revenue': 178.25}, {'customer': 'SIOUX EMPIRE LIGHTING', 'revenue': 178.25}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 178.25}, {'customer': 'PINE LIGHTING LTD', 'revenue': 178.25}, {'customer': None, 'revenue': 174.75}, {'customer': 'LIGHTING WORLD INC', 'revenue': 174.75}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 174.75}, {'customer': 'CENTURY LIGHTING CENTER', 'revenue': 174.75}, {'customer': 'GALAXIE LIGHTING INC', 'revenue': 174.75}, {'customer': 'MAYER ELECTRIC SUPPLY CO INC', 'revenue': 174.75}, {'customer': 'WINSUPPLY INC', 'revenue': 174.75}, {'customer': 'LIGHTSHINE INC', 'revenue': 174.75}, {'customer': 'GALLERIA LIGHTING', 'revenue': 174.75}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 174.75}, {'customer': 'EXPRESSIONS HOME LTG & DECOR', 'revenue': 174.75}, {'customer': 'TRINITY WHOLESALE DIST INC', 'revenue': 166.01}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 166.01}, {'customer': 'HARDWOOD FLOORS & MORE-CXT', 'revenue': 143.6}, {'customer': 'DESIGNER LIGHTING & FAN', 'revenue': 135.5}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 135.5}, {'customer': 'NORTHERN LIGHTS & FANS LLC', 'revenue': 135.5}, {'customer': 'KLS,LLC dba SPECTRUM LIGHTING', 'revenue': 135.5}, {'customer': "MAHLANDER'S", 'revenue': 135.5}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 135.5}, {'customer': 'FISHTRAP CREEK LIGHTING', 'revenue': 135.5}, {'customer': 'CAPITOL LIGHTING', 'revenue': 135.5}, {'customer': 'EDWARD JOY LIGHTING & ELEC SUP', 'revenue': 123.5}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 123.5}, {'customer': 'FARMVILLE WHOL ELEC SUPPLY CO', 'revenue': 120.0}, {'customer': 'BRITE WHOLESALE ELEC SUPPLY', 'revenue': 120.0}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 116.5}, {'customer': 'A & M ILLUMINATION', 'revenue': 116.5}, {'customer': 'GATEWAY LTG & DESIGN INC', 'revenue': 116.5}, {'customer': 'TECHE ELECTRIC', 'revenue': 116.5}, {'customer': 'FIXTURE THIS INC', 'revenue': 116.5}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 116.5}, {'customer': 'G & G ELECTRIC & PLUMBING', 'revenue': 116.5}, {'customer': 'THOMSON PREMIER LTG', 'revenue': 116.5}, {'customer': 'CHADWICK DESIGN', 'revenue': 116.5}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 116.5}, {'customer': 'SONEPAR-USA', 'revenue': 116.5}, {'customer': 'ACCENT LIGHTING INC', 'revenue': 116.5}, {'customer': 'R & R SUPPLY CO', 'revenue': 116.5}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 116.5}, {'customer': 'CITY LIGHTZ', 'revenue': 116.5}, {'customer': 'THE PLUMBING WAREHOUSE', 'revenue': 116.5}, {'customer': 'THE BUILDING CENTER, INC.', 'revenue': 116.5}, {'customer': 'USESI', 'revenue': 116.5}, {'customer': None, 'revenue': 116.5}, {'customer': 'LIGHTING ETC', 'revenue': 116.5}, {'customer': 'LEBANON ELECTRIC SUPPLY', 'revenue': 116.5}, {'customer': 'C.E.D.', 'revenue': 116.5}, {'customer': 'MOUNTAIN LIGHTING', 'revenue': 99.02}, {'customer': 'FACTORY LIGHTING OUTLET INC', 'revenue': 99.02}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 67.75}, {'customer': 'LIGHTS & MORE', 'revenue': 67.75}, {'customer': 'HOME LIGHTING', 'revenue': 67.75}, {'customer': 'ROYAL ENTERPRISES', 'revenue': 67.75}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 67.75}, {'customer': 'FELT LIGHTING CO', 'revenue': 67.75}, {'customer': 'DISPLAY MERCHANDISE-10', 'revenue': 67.75}, {'customer': 'MADISON LIGHTING', 'revenue': 67.75}, {'customer': 'FIRST SUPPLY LLC', 'revenue': 67.75}, {'customer': 'LOW ENERGY HOMES', 'revenue': 67.75}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 67.75}, {'customer': 'RADUE HOMES DBA INSPIRED SPACE', 'revenue': 67.75}, {'customer': 'THAXPACK, LLC DBA HOME LUXE', 'revenue': 67.75}, {'customer': 'LIGHTING SOUTH, LLC', 'revenue': 67.75}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 67.75}, {'customer': 'THE LIGHT HOUSE GALLERY', 'revenue': 67.75}, {'customer': 'CAROLINA LTG GALLERY', 'revenue': 67.75}, {'customer': 'CARDELLO ELECTRIC SUPPLY CO.', 'revenue': 64.0}, {'customer': 'COVENTRY LIGHTING INC', 'revenue': 64.0}, {'customer': 'LIGHTING EFX INC', 'revenue': 61.75}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 61.75}, {'customer': 'CONNECTICUT LIGHTING CTR INC', 'revenue': 60.98}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 60.98}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 60.97}, {'customer': 'COASTAL LIGHTING SUPPLY CO INC', 'revenue': 58.25}, {'customer': 'TEC OF NORTH LITTLE ROCK', 'revenue': 58.25}, {'customer': 'HUNZICKER BROTHERS', 'revenue': 58.25}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 58.25}, {'customer': 'SOUTHEAST ELECTRIC & PLUMBING', 'revenue': 58.25}, {'customer': 'HENSONS CARPET ONE', 'revenue': 58.25}, {'customer': 'BEST LIGHTING AND ACCESSORIES', 'revenue': 58.25}, {'customer': 'LIGHTING CONCEPTS LLC', 'revenue': 58.25}, {'customer': 'DUNCAN LIGHTING & HOME-I', 'revenue': 58.25}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 58.25}, {'customer': 'IDAHO DREAMING', 'revenue': 58.25}, {'customer': 'LIGHT SYSTEMS INC', 'revenue': 58.25}, {'customer': 'HOBRECHT LIGHTING CO INC', 'revenue': 58.25}, {'customer': 'WOLFE LIGHTING & ACCENTS LLC', 'revenue': 58.25}, {'customer': 'ALL ABOUT LIGHTS', 'revenue': 58.25}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 58.25}, {'customer': 'WOLFF BROS. SUPPLY, INC', 'revenue': 58.25}, {'customer': 'SORLIEN ELECTRIC INC', 'revenue': 58.25}, {'customer': 'MID-SOUTH LIGHTING', 'revenue': 58.25}, {'customer': 'A & A LIGHTING, LLP', 'revenue': 58.25}, {'customer': 'ILLUMINATIONS OF THE TRIAD', 'revenue': 58.25}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 58.25}, {'customer': 'LIGHTING WORKS', 'revenue': 58.25}, {'customer': 'GRAND RAPIDS LIGHTING CTR INC', 'revenue': 58.25}, {'customer': 'HOME CENTER INC', 'revenue': 58.25}, {'customer': 'ROYAUME LUMINAIRE STE JULIE', 'revenue': 54.2}, {'customer': 'ROYAUME SOREL-TRACEY', 'revenue': 49.51}, {'customer': 'FURNITURE SHOWCASE', 'revenue': 0.0}] | [{'item': '50503-BNK-WG', 'desc': 'Bolden 3 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 1440}, {'item': '50502-FB', 'desc': 'Bolden 2 Light Vanity in Flat Black', 'available': 505}, {'item': '50504-BNK', 'desc': 'Bolden 4 Light Vanity in Brushed Polished Nickel', 'available': 490}, {'item': '50503-BNK', 'desc': 'Bolden 3 Light Vanity in Brushed Polished Nickel', 'available': 363}, {'item': '50503-SB', 'desc': 'Bolden 3 Light Vanity in Satin Brass', 'available': 323}, {'item': '50503-FB', 'desc': 'Bolden 3 Light Vanity in Flat Black', 'available': 302}, {'item': '50591-FB-WG', 'desc': 'Bolden 1 Light Mini Pendant in Flat Black (White Glass)', 'available': 261}, {'item': '50591-BNK', 'desc': 'Bolden 1 Light Mini Pendant in Brushed Polished Nickel', 'available': 232}, {'item': '50504-FB-WG', 'desc': 'Bolden 4 Light Vanity in Flat Black (White Glass)', 'available': 179}, {'item': '50503-FB-WG', 'desc': 'Bolden 3 Light Vanity in Flat Black (White Glass)', 'available': 178}, {'item': '50523-FB', 'desc': 'Bolden 3 Light Chandelier in Flat Black', 'available': 171}, {'item': '50502-FB-WG', 'desc': 'Bolden 2 Light Vanity in Flat Black (White Glass)', 'available': 157}, {'item': '50523-BNK', 'desc': 'Bolden 3 Light Chandelier in Brushed Polished Nickel', 'available': 147}, {'item': '50525-SB', 'desc': 'Bolden 5 Light Chandelier in Satin Brass', 'available': 142}, {'item': '50591-FB', 'desc': 'Bolden 1 Light Mini Pendant in Flat Black', 'available': 141}, {'item': '50524-SB', 'desc': 'Bolden 4 Light Chandelier in Satin Brass', 'available': 127}, {'item': '50525-BNK', 'desc': 'Bolden 5 Light Chandelier in Brushed Polished Nickel', 'available': 119}, {'item': '50523-BNK-WG', 'desc': 'Bolden 3 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 116}, {'item': '50552-FB', 'desc': 'Bolden 2 Light Convertible Semi Flush in Flat Black', 'available': 113}, {'item': '50525-FB', 'desc': 'Bolden 5 Light Chandelier in Flat Black', 'available': 112}, {'item': '50501-SB', 'desc': 'Bolden 1 Light Wall Sconce in Satin Brass', 'available': 108}, {'item': '50524-FB', 'desc': 'Bolden 4 Light Chandelier in Flat Black', 'available': 105}, {'item': '50552-FB-WG', 'desc': 'Bolden 2 Light Convertible Semi Flush in Flat Black (White Glass)', 'available': 103}, {'item': '50536-FB', 'desc': 'Bolden 6 Light Foyer in Flat Black', 'available': 98}, {'item': '50525-BNK-WG', 'desc': 'Bolden 5 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 90}, {'item': '50536-SB', 'desc': 'Bolden 6 Light Foyer in Satin Brass', 'available': 88}, {'item': '50591-SB', 'desc': 'Bolden 1 Light Mini Pendant in Satin Brass', 'available': 85}, {'item': '50502-SB', 'desc': 'Bolden 2 Light Vanity in Satin Brass', 'available': 81}, {'item': '50552-BNK-WG', 'desc': 'Bolden 2 Light Convertible Semi Flush in Brushed Polished Nickel (White Glass)', 'available': 80}, {'item': '50501-FB-WG', 'desc': 'Bolden 1 Light Vanity in Flat Black (White Glass)', 'available': 79}, {'item': '50552-BNK', 'desc': 'Bolden 2 Light Convertible Semi Flush in Brushed Polished Nickel', 'available': 76}, {'item': '50533-FB', 'desc': 'Bolden 3 Light Foyer in Flat Black', 'available': 75}, {'item': '50529-FB', 'desc': 'Bolden 9 Light Chandelier in Flat Black', 'available': 75}, {'item': '50536-BNK', 'desc': 'Bolden 6 Light Foyer in Brushed Polished Nickel', 'available': 65}, {'item': '50523-FB-WG', 'desc': 'Bolden 3 Light Chandelier in Flat Black (White Glass)', 'available': 60}, {'item': '50529-BNK', 'desc': 'Bolden 9 Light Chandelier in Brushed Polished Nickel', 'available': 59}, {'item': '50552-SB', 'desc': 'Bolden 2 Light Convertible Semiflush in Satin Brass', 'available': 51}, {'item': '50528-FB-WG', 'desc': 'Bolden 8 Light Chandelier in Flat Black (White Glass)', 'available': 51}, {'item': '50528-BNK-WG', 'desc': 'Bolden 8 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 50}, {'item': '50528-SB', 'desc': 'Bolden 8 Light Chandelier in Satin Brass', 'available': 50}, {'item': '50524-FB-WG', 'desc': 'Bolden 4 Light Chandelier in Flat Black (White Glass)', 'available': 48}, {'item': '50525-FB-WG', 'desc': 'Bolden 5 Light Chandelier in Flat Black (White Glass)', 'available': 45}, {'item': '50533-SB', 'desc': 'Bolden 3 Light Foyer in Satin Brass', 'available': 42}, {'item': '50502-BNK-WG', 'desc': 'Bolden 2 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 38}, {'item': '50533-BNK', 'desc': 'Bolden 3 Light Foyer in Brushed Polished Nickel', 'available': 34}, {'item': '50524-BNK', 'desc': 'Bolden 4 Light Chandelier in Brushed Polished Nickel', 'available': 28}, {'item': '50528-BNK', 'desc': 'Bolden 8 Light Chandelier in Brushed Polished Nickel', 'available': 26}, {'item': '50501-BNK', 'desc': 'Bolden 1 Light Vanity in Brushed Polished Nickel', 'available': 25}, {'item': '50529-BNK-WG', 'desc': 'Bolden 9 Light Chandelier in Brushed Polished Nickel (White Glass)', 'available': 20}, {'item': '50504-BNK-WG', 'desc': 'Bolden 4 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 18}, {'item': '50591-BNK-WG', 'desc': 'Bolden 1 Light Mini Pendant in Brushed Polished Nickel (White Glass)', 'available': 17}, {'item': '50528-FB', 'desc': 'Bolden 8 Light Chandelier in Flat Black', 'available': 17}, {'item': '50523-SB', 'desc': 'Bolden 3 Light Chandelier in Satin Brass', 'available': 16}, {'item': '50529-SB', 'desc': 'Bolden 9 Light Chandelier in Satin Brass', 'available': 14}, {'item': '50502-BNK', 'desc': 'Bolden 2 Light Vanity in Brushed Polished Nickel', 'available': 12}, {'item': '50501-FB', 'desc': 'Bolden 1 Light Vanity in Flat Black', 'available': 11}, {'item': '50504-SB', 'desc': 'Bolden 4 Light Vanity in Satin Brass', 'available': 8}, {'item': '50529-FB-WG', 'desc': 'Bolden 9 Light Chandelier in Flat Black (White Glass)', 'available': 4}, {'item': '50501-BNK-WG', 'desc': 'Bolden 1 Light Vanity in Brushed Polished Nickel (White Glass)', 'available': 2}] |
| 19624BNK3 | Drake 3 Light Vanity in Brushed Polished Nickel | DRAKE | 174,442.62 | 3,817 | 2 | 2026-07-12 | [{'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 23098.7}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 19782.3}, {'customer': 'GREER LIGHTING CENTER LLC', 'revenue': 11565.6}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 9456.5}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 9183.54}, {'customer': 'HEARTH & HOME', 'revenue': 7068.0}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 5528.07}, {'customer': 'BAYSIDE ELECTRIC SUPPLY CO INC', 'revenue': 4702.1}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 4306.28}, {'customer': 'BEST LIGHTING AND ACCESSORIES', 'revenue': 4097.6}, {'customer': 'G & G ELECTRIC & PLUMBING', 'revenue': 3925.57}, {'customer': 'PREMIER LIGHTING LLC', 'revenue': 3911.93}, {'customer': 'HUNZICKER BROTHERS', 'revenue': 3269.0}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 3196.52}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3046.72}, {'customer': 'TRI SUPPLY', 'revenue': 2806.8}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 2745.84}, {'customer': 'METRO LIGHTING', 'revenue': 2519.4}, {'customer': 'SOUTHERN LIGHTS', 'revenue': 2371.5}, {'customer': 'HALL ELECTRIC', 'revenue': 2079.5}, {'customer': 'PC HOME CENTER', 'revenue': 1614.99}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 1576.36}, {'customer': 'FERGUSONHOME.COM', 'revenue': 1451.27}, {'customer': 'ILLUMINATIONS INC', 'revenue': 1367.12}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 1208.09}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 1200.66}, {'customer': 'LUXUR LIGHTING', 'revenue': 1187.03}, {'customer': 'LIGHTING WORLD INC', 'revenue': 1162.5}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 1134.62}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 1121.6}, {'customer': 'BRANDON LIGHTING INC', 'revenue': 1117.89}, {'customer': 'WAYFAIR LLC-I', 'revenue': 955.19}, {'customer': 'LIGHTING ETC', 'revenue': 930.0}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 851.88}, {'customer': 'WOLFE LIGHTING & ACCENTS LLC', 'revenue': 837.0}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 795.18}, {'customer': 'CAPITAL CITY DESIGN CENTER', 'revenue': 697.5}, {'customer': 'ALL ABOUT LIGHTS', 'revenue': 687.62}, {'customer': '1STOPLIGHTING-I', 'revenue': 672.46}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 651.0}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 644.03}, {'customer': 'PASSION LIGHTING', 'revenue': 604.5}, {'customer': 'LIGHTING PLUS', 'revenue': 604.5}, {'customer': 'FIXTURE THIS INC', 'revenue': 604.5}, {'customer': 'CHADWELL SUPPLY INC', 'revenue': 528.0}, {'customer': 'GALLERY OF LTG', 'revenue': 517.1}, {'customer': 'STEINKAMP HOME CENTER', 'revenue': 511.5}, {'customer': 'HUMMELL BROTHERS ELEC SUPPLY', 'revenue': 471.0}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 465.0}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 457.15}, {'customer': 'DELMAR FANS', 'revenue': 428.4}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 421.3}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 418.5}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 418.5}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 418.5}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 416.21}, {'customer': 'TECHE ELECTRIC', 'revenue': 374.8}, {'customer': 'PREMIER INDUSTRIES INC', 'revenue': 372.0}, {'customer': 'RIMROCK LIGHTING', 'revenue': 367.5}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 348.75}, {'customer': 'COASTAL LIGHTING SUPPLY CO INC', 'revenue': 339.45}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 337.5}, {'customer': "HAGEN'S", 'revenue': 325.5}, {'customer': 'TIMELESS DESIGNS LP', 'revenue': 325.5}, {'customer': 'HOME LIGHTING & SUPPLY INC', 'revenue': 325.5}, {'customer': 'PARALLAX INDUSTRIES, INC.', 'revenue': 283.5}, {'customer': 'LIGHTING CONCEPTS LLC', 'revenue': 279.0}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 279.0}, {'customer': 'TEAM ELECTRIC SUPPLY LLC', 'revenue': 279.0}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 279.0}, {'customer': 'KLS,LLC dba SPECTRUM LIGHTING', 'revenue': 262.5}, {'customer': 'ROBINSON LIGHTING LTD', 'revenue': 236.25}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 232.5}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 232.5}, {'customer': None, 'revenue': 232.5}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 232.5}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 232.5}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 210.0}, {'customer': 'B & H ELECTRIC SUPPLY', 'revenue': 210.0}, {'customer': 'BRILLANT LIGHTING CENTER', 'revenue': 210.0}, {'customer': 'CITY LIGHTZ', 'revenue': 206.01}, {'customer': 'HERITAGE LIGHTING, LLC', 'revenue': 191.6}, {'customer': 'BRIGHT IDEAS LTG & MORE', 'revenue': 186.0}, {'customer': 'BENDER MANAGEMENT INC', 'revenue': 186.0}, {'customer': 'HOME LIGHTING', 'revenue': 186.0}, {'customer': 'SORLIEN ELECTRIC INC', 'revenue': 186.0}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 186.0}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 186.0}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 186.0}, {'customer': 'DUNCAN CORPORATION', 'revenue': 186.0}, {'customer': 'TKL SOLUTIONS INC', 'revenue': 179.03}, {'customer': 'LANTERN HOUSE INC', 'revenue': 162.75}, {'customer': 'FISHTRAP CREEK LIGHTING', 'revenue': 157.5}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 157.5}, {'customer': 'CAPITOL LIGHTING', 'revenue': 157.5}, {'customer': 'RADUE HOMES DBA INSPIRED SPACE', 'revenue': 157.5}, {'customer': 'VISIONS LTG & ACCESSORIES', 'revenue': 157.5}, {'customer': 'COCOON INTERIORS INC.', 'revenue': 157.5}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 145.5}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 142.3}, {'customer': 'DE.KOR LIGHTING BOUTIQUE LTD.', 'revenue': 141.76}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 141.75}, {'customer': 'MEDINA LIGHTING INC', 'revenue': 139.5}, {'customer': 'KAMLOOPS LAMPOST THE', 'revenue': 139.5}, {'customer': 'APPLICO APPLIANCE & LTG', 'revenue': 139.5}, {'customer': 'RAYMOND DESTEIGER INC', 'revenue': 139.5}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 139.5}, {'customer': 'LIGHTING INC.', 'revenue': 139.5}, {'customer': 'CHATELAINE LIGHTING SUPPLY LTD', 'revenue': 139.5}, {'customer': 'MOUNTAIN LIGHTING', 'revenue': 139.5}, {'customer': 'PINE STATE ELEC SUPPLY', 'revenue': 139.5}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 139.5}, {'customer': 'AT HOME, LLC DBA HOME LIGHTING', 'revenue': 139.5}, {'customer': 'LIGHTING EFX INC', 'revenue': 139.5}, {'customer': 'U.S. 31 SUPPLY INC', 'revenue': 132.53}, {'customer': 'HOUSE OF LIGHTS OF SANFORD INC', 'revenue': 129.75}, {'customer': 'BLACK DIAMOND ACQUISITIONS', 'revenue': 105.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 105.0}, {'customer': 'M.C.I. INC', 'revenue': 105.0}, {'customer': 'THE SALT BOX', 'revenue': 105.0}, {'customer': 'ROYAL ENTERPRISES', 'revenue': 105.0}, {'customer': 'BGZA INC', 'revenue': 105.0}, {'customer': 'LESSMAN ELECTRIC SUPPLY CO', 'revenue': 105.0}, {'customer': 'GARDEN OF THE GODS LIGHTING', 'revenue': 105.0}, {'customer': 'NORTHERN LGTS & FURNISHINGS', 'revenue': 105.0}, {'customer': 'HOUSE ACCOUNT', 'revenue': 97.7}, {'customer': 'LYONS ELECTRICAL', 'revenue': 95.8}, {'customer': 'FIRST SUPPLY LLC', 'revenue': 95.56}, {'customer': 'CMC SUPPLY, INC.', 'revenue': 93.0}, {'customer': 'HOME BUILDERS SUPPLY INC', 'revenue': 93.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 93.0}, {'customer': 'SUNDIAL LIGHTING LTD', 'revenue': 93.0}, {'customer': 'AMOS ELECTRIC SUPPLY COMPANY', 'revenue': 93.0}, {'customer': 'W T LIGHTING', 'revenue': 93.0}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 93.0}, {'customer': 'IDAHO DREAMING', 'revenue': 93.0}, {'customer': 'QUARLES SUPPLY CO INC', 'revenue': 93.0}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 93.0}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 86.49}, {'customer': 'PIONEER LIGHTING INC', 'revenue': 55.7}, {'customer': 'HOUSE OF LIGHTS OF CARY INC', 'revenue': 52.5}, {'customer': 'ELAN STUDIO LIGHTING', 'revenue': 52.5}, {'customer': 'DISPLAY MERCHANDISE-10', 'revenue': 52.5}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 52.5}, {'customer': 'ELEMENTS OF DESIGN', 'revenue': 52.5}, {'customer': 'FLOOR BROKERS, THE', 'revenue': 52.5}, {'customer': "MAHLANDER'S", 'revenue': 52.5}, {'customer': 'PREMIER BATH, LTG & HDW LLC', 'revenue': 52.5}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 49.3}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 48.82}, {'customer': 'LIGHT HOUSE THE', 'revenue': 48.82}, {'customer': 'LIGHTING SHOPPE CHATHAM, LLC', 'revenue': 47.25}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 47.25}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 46.5}, {'customer': 'PARAMONT-EO INC', 'revenue': 46.5}, {'customer': 'BETTER HOMES SUPPLY', 'revenue': 46.5}, {'customer': 'STATEWIDE LIGHTING-RENO', 'revenue': 46.5}, {'customer': None, 'revenue': 46.5}, {'customer': 'ELECTRIC SUPPLY LIGHTING', 'revenue': 46.5}, {'customer': 'FANS & LIGHTING MINN. LLC', 'revenue': 46.5}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 46.5}, {'customer': 'STATE ELECTRIC SUPPLY CO', 'revenue': 46.5}, {'customer': 'LIGHTSHINE INC', 'revenue': 46.5}, {'customer': 'ONE SOURCE LIGHTING INC', 'revenue': 46.5}, {'customer': 'WOLBERG ELECTRIC SUPPLY CO', 'revenue': 46.5}, {'customer': 'COVERINGS LLC', 'revenue': 46.5}, {'customer': 'A & W LIGHTING', 'revenue': 46.5}, {'customer': 'HOUSE OF LIGHTS', 'revenue': 46.5}, {'customer': 'GROSS LIGHTING & HOME', 'revenue': 46.5}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 46.5}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 46.5}, {'customer': 'CR LIGHTING', 'revenue': 46.5}, {'customer': 'RE-LIGHTING', 'revenue': 46.5}, {'customer': 'WHOLESALE SUPPLY GROUP INC', 'revenue': 46.5}, {'customer': '43RD STREET LIGHTING', 'revenue': 46.5}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 46.5}, {'customer': 'PLYLER SUPPLY CO', 'revenue': 44.63}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 37.2}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 26.25}, {'customer': 'BULB BIN INC', 'revenue': 0.0}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 0.0}, {'customer': 'C.E.D.', 'revenue': 0.0}, {'customer': 'FURNITURE SHOWCASE', 'revenue': 0.0}, {'customer': 'J. H. LARSON COMPANY', 'revenue': 0.0}] | [{'item': '19616BNK2', 'desc': 'Drake 2 Light Vanity in Brushed Polished Nickel', 'available': 91}, {'item': '19606BNK1', 'desc': 'Drake 1 Light Wall Sconce in Brushed Polished Nickel', 'available': 78}, {'item': '19633FB4', 'desc': 'Drake 4 Light Vanity in Flat Black', 'available': 60}, {'item': '19606FB1', 'desc': 'Drake 1 Light Wall Sconce in Flat Black', 'available': 53}, {'item': '19633BNK4', 'desc': 'Drake 4 Light Vanity in Brushed Polished Nickel', 'available': 48}, {'item': '19624FB3', 'desc': 'Drake 3 Light Vanity in Flat Black', 'available': 46}, {'item': '19642FB5', 'desc': 'Drake 5 Light Vanity in Flat Black', 'available': 24}, {'item': '19642BNK5', 'desc': 'Drake 5 Light Vanity in Brushed Polished Nickel', 'available': 12}] |
| BSCB-B | Surface Mount Die-Cast Builder's Series LED Lighted Push Button in Matte Black | COL335 | 162,868.66 | 32,229 | 4,421 | 2026-09-20 | [{'customer': 'LIGHTING CONNECTION LLC', 'revenue': 34633.5}, {'customer': 'C.E.D.', 'revenue': 21288.7}, {'customer': 'STAR LIGHT DISTRIBUTION INC', 'revenue': 8690.4}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 8386.98}, {'customer': 'DELMAR FANS', 'revenue': 5430.85}, {'customer': 'CR LIGHTING', 'revenue': 4926.05}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3208.35}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 3155.59}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 3089.3}, {'customer': 'FERGUSONHOME.COM', 'revenue': 3030.5}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 2861.1}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 2739.05}, {'customer': 'LUMINAIRES PAUL GREGOIRE INC', 'revenue': 2668.8}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 2624.4}, {'customer': 'LIGHTS UNLIMITED', 'revenue': 2426.7}, {'customer': 'R WILSON INC', 'revenue': 2118.2}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 2034.3}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 1806.73}, {'customer': 'DESIGNS BY ANN INC', 'revenue': 1637.4}, {'customer': 'ELLEN LIGHTING & HARDWARE', 'revenue': 1545.5}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 1504.75}, {'customer': "HAGEN'S", 'revenue': 1398.15}, {'customer': 'LIGHTING WORLD INC', 'revenue': 1364.75}, {'customer': 'HUNZICKER BROTHERS', 'revenue': 1300.5}, {'customer': 'RENSEN HOUSE OF LIGHTS', 'revenue': 1213.98}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 1160.8}, {'customer': 'ROYAUME LUMINAIRE LANDAUDIERE', 'revenue': 1108.5}, {'customer': 'KBL DESIGN CENTER', 'revenue': 938.25}, {'customer': 'LORD HENRY ENTERPRISES INC-I', 'revenue': 892.05}, {'customer': 'TEC OF NORTH LITTLE ROCK', 'revenue': 890.7}, {'customer': 'SHANOR ELECTRIC SUPPLY INC', 'revenue': 859.75}, {'customer': 'LUMBER ONE HOME CENTER, INC.', 'revenue': 854.72}, {'customer': None, 'revenue': 845.79}, {'customer': 'OLYMPIA LIGHTING CENTER INC', 'revenue': 810.9}, {'customer': 'LUXUR LIGHTING', 'revenue': 742.8}, {'customer': 'METRO LIGHTING', 'revenue': 739.94}, {'customer': 'A & A LIGHTING, LLP', 'revenue': 719.55}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 708.25}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 694.3}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 690.8}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 653.9}, {'customer': "BRECHER'S LIGHTING, THE", 'revenue': 630.9}, {'customer': 'LIGHTING INC.', 'revenue': 565.8}, {'customer': 'SONEPAR-USA', 'revenue': 560.6}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 560.05}, {'customer': 'HERITAGE LIGHTING, LLC', 'revenue': 558.0}, {'customer': 'HOME CENTER INC', 'revenue': 555.24}, {'customer': 'AMC LIGHTING & DECOR, INC.', 'revenue': 532.2}, {'customer': 'HENSONS CARPET ONE', 'revenue': 513.0}, {'customer': 'R.D.H.S.INC', 'revenue': 508.5}, {'customer': 'PINE GROVE ELEC SPLY', 'revenue': 494.05}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 471.3}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 462.25}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 430.05}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 412.86}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 402.85}, {'customer': 'PACE LIGHTING INC', 'revenue': 399.75}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 393.84}, {'customer': 'PARK LIGHTING', 'revenue': 379.53}, {'customer': 'ALL ABOUT LIGHTS', 'revenue': 373.2}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 364.0}, {'customer': 'DESIGN LIGHTING SALES LTD', 'revenue': 334.72}, {'customer': 'FRONT STREET LIGHTING', 'revenue': 333.3}, {'customer': 'RITE RUG CO.', 'revenue': 330.7}, {'customer': 'SOUTHSIDE ELECTRIC', 'revenue': 321.1}, {'customer': 'DECO LUMINAIRE QUEBEC', 'revenue': 311.55}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 308.4}, {'customer': "GRAHAM'S LIGHTING INC", 'revenue': 306.4}, {'customer': 'T J S SUPPLY CO', 'revenue': 294.05}, {'customer': 'A & W LIGHTING', 'revenue': 291.6}, {'customer': 'MULTI LUMINAIRE ST. HUBERT', 'revenue': 291.6}, {'customer': 'BRANDON LIGHTING INC', 'revenue': 286.0}, {'customer': 'LITE HOUSE INC', 'revenue': 285.9}, {'customer': 'ROBINSON LIGHTING LTD', 'revenue': 272.21}, {'customer': 'BEAULIEU & LAMOUREUX INC', 'revenue': 270.9}, {'customer': 'CREATIVE LIGHTING, INC.', 'revenue': 264.0}, {'customer': 'GREER LIGHTING CENTER LLC', 'revenue': 257.2}, {'customer': 'LIGHTING GALLERY INC', 'revenue': 253.2}, {'customer': 'SUPER-LITE LIGHTING LTD-T', 'revenue': 251.7}, {'customer': 'CRESCENT LIGHTING SUPPLY INC', 'revenue': 240.9}, {'customer': 'CAJUN ELECTRIC, LLC', 'revenue': 236.6}, {'customer': 'DUNCAN CORPORATION', 'revenue': 227.75}, {'customer': 'GALLERY OF LTG', 'revenue': 218.1}, {'customer': 'IMAGINE MORE SERVICE CORP.', 'revenue': 206.15}, {'customer': 'SHOPFREELY.COM-I', 'revenue': 191.7}, {'customer': 'UNITED ELECTRIC SUPPLY', 'revenue': 181.9}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 178.8}, {'customer': 'GATEWAY LTG & DESIGN INC', 'revenue': 176.7}, {'customer': 'LIGHT CENTER, THE', 'revenue': 175.85}, {'customer': 'LOW COUNTRY LIGHTING INC', 'revenue': 170.0}, {'customer': 'ENCORE FLOORING & BLDG PROD', 'revenue': 165.3}, {'customer': 'THE LIGHTING GALLERY LLC', 'revenue': 159.64}, {'customer': 'LIGHTING GALLERY INC, THE', 'revenue': 154.8}, {'customer': 'ILLUMINATING EXPRESSIONS LLC', 'revenue': 149.4}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 145.8}, {'customer': 'RICHARDS LIGHTING', 'revenue': 144.95}, {'customer': 'AA PORTER', 'revenue': 140.9}, {'customer': 'HEARTH & HOME', 'revenue': 140.12}, {'customer': 'SHOWCASE LIGHTING BY 3-G LTD', 'revenue': 139.7}, {'customer': 'WISEWAY SUPPLY', 'revenue': 138.9}, {'customer': "LOWE'S CABINETS & LIGHTING GAL", 'revenue': 138.9}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 138.05}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 133.05}, {'customer': 'HALL ELECTRIC', 'revenue': 131.7}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 131.22}, {'customer': 'SCOTT ELECTRIC', 'revenue': 130.2}, {'customer': 'PROSOURCE SUPPLY', 'revenue': 118.2}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 114.85}, {'customer': 'RACHELS LTG & HOME ACCESSORIES', 'revenue': 114.3}, {'customer': "EFIRD'S INTERIOR", 'revenue': 112.22}, {'customer': 'CROWN ELECTRIC SUPPLY CO', 'revenue': 109.15}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 107.4}, {'customer': 'LIGHTING SOLUTIONS DESIGN GALL', 'revenue': 105.9}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 102.85}, {'customer': 'LOGAN ELECTRIC COMPANY INC', 'revenue': 100.5}, {'customer': 'ECLAIRAGE MODERNE SARAN INC', 'revenue': 99.0}, {'customer': 'CAPITOL LIGHTING GALLERY', 'revenue': 98.15}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 95.85}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 87.75}, {'customer': 'J & K ELECTRICAL SUPPLY CO INC', 'revenue': 87.04}, {'customer': 'CENTURY LIGHTING CENTER', 'revenue': 84.45}, {'customer': 'LESSMAN ELECTRIC SUPPLY CO', 'revenue': 79.8}, {'customer': None, 'revenue': 79.8}, {'customer': 'PINE TREE FURN & LIGHTING INC', 'revenue': 76.65}, {'customer': 'WILSON LIGHTING CO INC', 'revenue': 76.2}, {'customer': 'SHOALS LIGHTING', 'revenue': 76.2}, {'customer': '1STOPLIGHTING-I', 'revenue': 72.37}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 71.88}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 70.6}, {'customer': None, 'revenue': 69.85}, {'customer': 'LUMEN NATION LLC', 'revenue': 69.45}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 69.3}, {'customer': 'HUMMELL BROTHERS ELEC SUPPLY', 'revenue': 69.3}, {'customer': 'MAYER ELECTRIC SUPPLY CO INC', 'revenue': 68.75}, {'customer': 'COLEY ELECTRIC', 'revenue': 66.0}, {'customer': 'AIKEN ELECTRICAL  WHOLSALE INC', 'revenue': 66.0}, {'customer': 'CORNWALL LTG & ELEC CTR', 'revenue': 66.0}, {'customer': 'THE LIGHTING HUT INC', 'revenue': 66.0}, {'customer': 'BGZA INC', 'revenue': 59.6}, {'customer': 'ACCENT LIGHTING INC', 'revenue': 57.2}, {'customer': 'MCCAFFETY ELECTRIC CO INC', 'revenue': 55.25}, {'customer': 'BRUNEAU LUMINAIRE INC', 'revenue': 55.0}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 55.0}, {'customer': 'ROYAUME LUMINAIRE STE JULIE', 'revenue': 53.2}, {'customer': 'TRI SUPPLY', 'revenue': 52.55}, {'customer': 'PASSION LIGHTING', 'revenue': 52.05}, {'customer': 'SEQUEL ELECTRICAL SUPPLY, LLC', 'revenue': 52.0}, {'customer': 'LIGHTING PLUS', 'revenue': 52.0}, {'customer': 'BURGESS LIGHTING & DIST', 'revenue': 50.9}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 50.3}, {'customer': 'CMC SUPPLY, INC.', 'revenue': 49.7}, {'customer': 'TURN-ON LIGHTING', 'revenue': 48.8}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 46.55}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 44.0}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 41.95}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 41.6}, {'customer': 'LIGHT INNOVATIONS INC', 'revenue': 41.6}, {'customer': 'LIGHTING ETC', 'revenue': 41.0}, {'customer': 'MURRAY SUPPLY/WHOLESALE ELEC', 'revenue': 39.9}, {'customer': 'COVENTRY LIGHTING INC', 'revenue': 39.9}, {'customer': 'LIGHTING CONCEPTS', 'revenue': 39.9}, {'customer': 'HOUSE ELECTRIC LLC', 'revenue': 38.1}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 38.1}, {'customer': 'APPLICO APPLIANCE & LTG', 'revenue': 38.1}, {'customer': 'TIMELESS DESIGNS LP', 'revenue': 38.1}, {'customer': 'LIGHTING & REFLECTIONS', 'revenue': 38.1}, {'customer': 'ILLUMINATIONS OF THE TRIAD', 'revenue': 38.1}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 36.45}, {'customer': 'BRIGHT IDEAS LTG & MORE', 'revenue': 36.4}, {'customer': 'LUMINAIRE REPENTIGNY INC', 'revenue': 34.8}, {'customer': 'THOMSON PREMIER LTG', 'revenue': 33.9}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 33.25}, {'customer': 'BAYSIDE ELECTRIC SUPPLY CO INC', 'revenue': 33.25}, {'customer': 'CLASSIC LIGHTING & DESIGN INC', 'revenue': 33.0}, {'customer': 'RICHARDSON HOUSE OF FIXTURES', 'revenue': 33.0}, {'customer': 'DOMINION ELECTRIC SUPPLY CO', 'revenue': 33.0}, {'customer': 'HOUSE OF LIGHTS OF CARY INC', 'revenue': 32.1}, {'customer': "MIKE'S LIGHTING & ELECTRICAL", 'revenue': 31.75}, {'customer': 'LIGHT HOUSE', 'revenue': 31.2}, {'customer': 'LIGHT HOUSE OF SUMTER, LLC', 'revenue': 27.5}, {'customer': 'WILLIAM L HART DESIGNS LLC', 'revenue': 26.6}, {'customer': 'LIGHTSHINE INC', 'revenue': 26.6}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 26.6}, {'customer': 'UNIVERSITY LIGHTS-EJT', 'revenue': 26.6}, {'customer': 'TOPS ELECTRIC SUPPLY', 'revenue': 24.3}, {'customer': 'GORDON ELECTRIC SUPPLY', 'revenue': 22.0}, {'customer': 'LOFINGS LIGHTING', 'revenue': 22.0}, {'customer': 'FISHTRAP CREEK LIGHTING', 'revenue': 22.0}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 19.95}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 18.8}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 18.8}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 17.94}, {'customer': 'FARMVILLE WHOL ELEC SUPPLY CO', 'revenue': 16.75}, {'customer': 'DECORATIVE LIGHTING', 'revenue': 16.5}, {'customer': 'LIGHTS N SUCH INC', 'revenue': 16.5}, {'customer': 'CLEVELAND LIGHTING CENTER', 'revenue': 13.3}, {'customer': 'DECO LUMINAIRE', 'revenue': 13.3}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 12.7}, {'customer': 'NACOGDOCHES HOME DESIGN CENTER', 'revenue': 12.7}, {'customer': 'LIGHTHOUSE DIST-DOORBELLSDIREC', 'revenue': 12.7}, {'customer': 'DUNCAN LIGHTING & HOME-I', 'revenue': 12.64}, {'customer': 'USESI', 'revenue': 12.15}, {'customer': 'JUST LIGHTS, INC.', 'revenue': 12.15}, {'customer': None, 'revenue': 11.0}, {'customer': 'LIGHT SYSTEMS INC', 'revenue': 11.0}, {'customer': 'TECHE ELECTRIC', 'revenue': 11.0}, {'customer': "JOSEPH'S ELECTRICAL CENTER", 'revenue': 11.0}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 10.4}, {'customer': 'THE BUILDING CENTER, INC.', 'revenue': 10.4}, {'customer': 'MADISON LIGHTING', 'revenue': 6.65}, {'customer': 'LIGHT WORKS OF STEAMBOAT', 'revenue': 6.65}, {'customer': 'CHRISTIES LTG GALLERY LLC', 'revenue': 6.65}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 6.65}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 6.65}, {'customer': 'TRINITY WHOLESALE DIST INC', 'revenue': 6.35}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 6.35}, {'customer': 'COASTAL LIGHTING, LLC', 'revenue': 6.35}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 6.35}, {'customer': 'ELECTRICAL & PLBG STORE', 'revenue': 6.32}, {'customer': 'LAMPS PLUS', 'revenue': 5.98}, {'customer': 'MILLIKEN HOME CENTER', 'revenue': 5.5}, {'customer': 'ELITEFIXTURES.COM-I', 'revenue': 5.5}, {'customer': 'LIGHTING SHOWCASE', 'revenue': 5.5}, {'customer': 'STEVENS LIGHTING FIXTURE CO', 'revenue': 5.5}, {'customer': 'THE PLUMBING WAREHOUSE', 'revenue': 5.5}, {'customer': 'HOBRECHT LIGHTING CO INC', 'revenue': 5.5}, {'customer': 'DECO LUMINAIRE-BROSSARD', 'revenue': 5.5}, {'customer': 'BUTLERS ELECTRIC SUPPLY-', 'revenue': 5.4}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 5.4}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 5.11}, {'customer': 'LIGHTSTYLE OF ORLANDO', 'revenue': 4.95}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 4.95}, {'customer': 'BLACK DIAMOND ACQUISITIONS', 'revenue': 0.0}, {'customer': 'Craftmade Warranty Account', 'revenue': 0.0}] | [{'item': 'BS6-W', 'desc': 'Surface Mount Rectangle Lighted Push Button in White', 'available': 145}] |
| Z402-TB | 2 Light Directional Bullet in Textured Black | CAST | 146,102.04 | 7,363 | 48 | 2026-09-25 | [{'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 23404.02}, {'customer': 'WAYFAIR LLC-I', 'revenue': 17110.4}, {'customer': 'FERGUSONHOME.COM', 'revenue': 16244.25}, {'customer': 'DEMENT LIGHTING INC', 'revenue': 13228.5}, {'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 12237.03}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 4445.46}, {'customer': 'METRO LIGHTING', 'revenue': 3371.01}, {'customer': 'CR LIGHTING', 'revenue': 3291.75}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 3074.14}, {'customer': "HAGEN'S", 'revenue': 2752.75}, {'customer': 'DELMAR FANS', 'revenue': 2730.2}, {'customer': 'LIGHTING INC.', 'revenue': 1925.0}, {'customer': 'FORESIGHT LIGHTING', 'revenue': 1815.63}, {'customer': 'BRAZORIA COUNTY LIGHTING', 'revenue': 1721.25}, {'customer': 'MARS ELECTRIC CO', 'revenue': 1673.75}, {'customer': 'BBC LIGHTING & SUPPLY', 'revenue': 1656.25}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 1564.99}, {'customer': 'KANSAS LIGHTING DIST INC', 'revenue': 1542.11}, {'customer': 'MORRISON SUPPLY COMPANY', 'revenue': 1501.5}, {'customer': 'AMERICAN LIGHTING', 'revenue': 1369.25}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 1289.75}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 1092.82}, {'customer': 'MY KNOBS.COM INC-I', 'revenue': 1078.0}, {'customer': 'HAUS APPEAL, LLC- I', 'revenue': 1039.51}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 920.2}, {'customer': '1STOPLIGHTING-I', 'revenue': 828.45}, {'customer': 'LIGHTING EFX INC', 'revenue': 828.22}, {'customer': 'ROBINSON LIGHTING LTD', 'revenue': 765.2}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 755.03}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 698.0}, {'customer': 'NOVA LIGHTING', 'revenue': 672.3}, {'customer': 'MADISON LIGHTING', 'revenue': 658.75}, {'customer': 'THE PLUMBING WAREHOUSE', 'revenue': 654.5}, {'customer': 'THE SALT BOX', 'revenue': 636.0}, {'customer': 'LIGHTING ETC', 'revenue': 635.25}, {'customer': 'ALDRIDGE APPLIANCE', 'revenue': 631.0}, {'customer': 'STOKES LIGHTING CENTER', 'revenue': 539.0}, {'customer': 'HILL COUNTRY LIGHTING CTR INC', 'revenue': 469.69}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 463.53}, {'customer': 'SOUTHSIDE LIGHTING GALLERY', 'revenue': 449.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 365.75}, {'customer': 'C.E.D.', 'revenue': 365.75}, {'customer': 'CRESCENT ELECTRIC SUPPLY CO', 'revenue': 361.25}, {'customer': 'SOUTHEAST ELECTRIC & PLUMBING', 'revenue': 336.9}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 326.08}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 309.25}, {'customer': None, 'revenue': 308.0}, {'customer': 'LIGHT CENTER, THE', 'revenue': 308.0}, {'customer': 'QUARLES SUPPLY CO INC', 'revenue': 299.33}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 288.75}, {'customer': 'LUXUR LIGHTING', 'revenue': 269.5}, {'customer': 'LIGHTING GALLERY', 'revenue': 255.0}, {'customer': 'M.C.I. INC', 'revenue': 255.0}, {'customer': 'LIGHTING SHOPPE INC', 'revenue': 252.16}, {'customer': 'LIGHTINGFRONT.COM-I', 'revenue': 233.75}, {'customer': 'GORDON ELECTRIC SUPPLY', 'revenue': 233.75}, {'customer': 'LIGHTING INC', 'revenue': 231.0}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 224.4}, {'customer': 'TALLAHASSEE LIGHT, FAN & BLADE', 'revenue': 212.5}, {'customer': 'THE GALLERIES', 'revenue': 211.75}, {'customer': 'HENSONS CARPET ONE', 'revenue': 211.75}, {'customer': 'USESI', 'revenue': 192.5}, {'customer': 'DUNCAN CORPORATION', 'revenue': 192.5}, {'customer': 'DESIGNS BY ANN INC', 'revenue': 192.5}, {'customer': 'BRIGGS INC OF OMAHA', 'revenue': 191.25}, {'customer': 'CAPITOL LIGHTING', 'revenue': 188.25}, {'customer': 'HAJOCA CORP', 'revenue': 170.0}, {'customer': 'TECHE ELECTRIC', 'revenue': 154.0}, {'customer': 'EDWARD JOY LIGHTING & ELEC SUP', 'revenue': 154.0}, {'customer': 'HALL ELECTRIC', 'revenue': 154.0}, {'customer': 'WOLFF BROS. SUPPLY, INC', 'revenue': 154.0}, {'customer': 'INLINE ELECTRIC SUPPLY', 'revenue': 154.0}, {'customer': "EFIRD'S INTERIOR", 'revenue': 151.11}, {'customer': 'J. H. LARSON COMPANY', 'revenue': 148.75}, {'customer': 'FIVE OAK CONSTRUCTION', 'revenue': 148.75}, {'customer': 'NORTHERN LIGHTING & SUPPLY', 'revenue': 148.0}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 138.34}, {'customer': 'CREATIVE LIGHTING', 'revenue': 134.75}, {'customer': 'KWK INVESTMENTS LLC', 'revenue': 134.75}, {'customer': 'WINSUPPLY INC', 'revenue': 134.75}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 133.91}, {'customer': 'THE LIGHTING GALLERY LLC', 'revenue': 129.83}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 129.75}, {'customer': 'FACILITY SOLUTIONS GROUP INC', 'revenue': 127.5}, {'customer': 'ANTHOLOGY LIGHTING', 'revenue': 127.5}, {'customer': 'FLECO INDUSTRIES INC', 'revenue': 115.5}, {'customer': 'J.D. HILL ELECTRIC, INC', 'revenue': 115.5}, {'customer': 'BRIDGE STREET ELECTRIC', 'revenue': 115.5}, {'customer': 'LITE HOUSE INC', 'revenue': 115.5}, {'customer': 'GOING DECOR', 'revenue': 106.25}, {'customer': 'LIGHTING CONNECTION LLC', 'revenue': 99.0}, {'customer': 'HOUSE OF CARPETS INC', 'revenue': 96.25}, {'customer': 'LIGHTING DESIGN  LLC', 'revenue': 96.25}, {'customer': 'PREMIER LIGHTING LLC', 'revenue': 96.25}, {'customer': 'KENDALL ELECTRIC INC', 'revenue': 96.25}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 96.25}, {'customer': 'LUMENAREA', 'revenue': 96.25}, {'customer': 'WOLBERG ELECTRIC SUPPLY CO', 'revenue': 96.25}, {'customer': 'FIXTURE THIS INC', 'revenue': 96.25}, {'customer': 'BUTLERS ELECTRIC SUPPLY', 'revenue': 96.25}, {'customer': 'BGZA INC', 'revenue': 85.0}, {'customer': 'DOMINION ELECTRIC SUPPLY CO', 'revenue': 85.0}, {'customer': 'HEIGHTS LIGHTS & THINGS', 'revenue': 85.0}, {'customer': 'HAYNEEDLE,INC-I', 'revenue': 84.25}, {'customer': 'THE LAMP & LIGHTHOUSE', 'revenue': 83.5}, {'customer': 'SOUTHERN INTERIORS & LIGHTING', 'revenue': 78.25}, {'customer': 'LIGHTSHINE INC', 'revenue': 77.0}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 77.0}, {'customer': 'TRI SUPPLY', 'revenue': 77.0}, {'customer': 'LIGHTING BY DESIGN', 'revenue': 77.0}, {'customer': 'LIGHT HOUSE', 'revenue': 77.0}, {'customer': 'VILLAGE LIGHTING & SUPPLY INC', 'revenue': 77.0}, {'customer': 'LIGHTING CONCEPTS INC', 'revenue': 77.0}, {'customer': 'LIGHT BRITE DISTRIBUTING INC', 'revenue': 77.0}, {'customer': 'BRIGHT IDEAS OF ROCHESTER', 'revenue': 63.75}, {'customer': 'LIGHT SOURCE LIGHTING-I', 'revenue': 63.75}, {'customer': 'LOFINGS LIGHTING', 'revenue': 63.75}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 63.75}, {'customer': 'RIMROCK LIGHTING', 'revenue': 63.75}, {'customer': 'STEVENS LIGHTING FIXTURE CO', 'revenue': 63.75}, {'customer': 'BUILD IT FAB INC', 'revenue': 63.75}, {'customer': 'RITE RUG CO.', 'revenue': 63.75}, {'customer': 'LAMP SHOP/BRIGHT IDEAS, THE', 'revenue': 61.75}, {'customer': 'ELLIOTT ELECTRIC', 'revenue': 61.5}, {'customer': 'W T LIGHTING', 'revenue': 57.75}, {'customer': 'PRICE WHOLESALE LIGHTING', 'revenue': 57.75}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 57.75}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 57.75}, {'customer': 'MCMANUS LAMPLIGHTER', 'revenue': 57.75}, {'customer': 'THE BUILDING CENTER, INC.', 'revenue': 57.75}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 57.75}, {'customer': 'ILLUMINATIONS INC', 'revenue': 57.75}, {'customer': 'SOUTHERN LIGHTING GALLERY INC', 'revenue': 57.75}, {'customer': 'LUMEN NATION LLC', 'revenue': 42.5}, {'customer': 'LIGHTING PLUS INC', 'revenue': 42.5}, {'customer': 'CEILING FAN COMPANY INC', 'revenue': 42.5}, {'customer': 'KINGS WAGON YARD', 'revenue': 38.5}, {'customer': 'STEINKAMP HOME CENTER', 'revenue': 38.5}, {'customer': 'HEARTH & HOME', 'revenue': 38.5}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 38.5}, {'customer': 'Peak Lighting Bulbs & Ballast', 'revenue': 38.5}, {'customer': 'BROADWAY SHOWROOM', 'revenue': 38.5}, {'customer': 'GALLERIA LIGHTING', 'revenue': 38.5}, {'customer': 'J & B SUPPLY INC', 'revenue': 38.5}, {'customer': 'WESTERN MONTANA LIGHTING', 'revenue': 38.5}, {'customer': 'COLEY ELECTRIC-WAYCROSS', 'revenue': 38.5}, {'customer': 'VALLEY LIGHTS INC', 'revenue': 38.5}, {'customer': 'BIGGINS LIGHTING & ELECTRIC', 'revenue': 38.5}, {'customer': 'DUNAMIS INTERIORS INC-C', 'revenue': 21.25}, {'customer': 'SUN LIGHTING CO-TUCSON', 'revenue': 21.25}, {'customer': 'FAN DIEGO INC', 'revenue': 21.25}, {'customer': 'HARTVILLE HARDWARE', 'revenue': 21.25}, {'customer': 'DISTINCTIVE LIGHTING', 'revenue': 21.25}, {'customer': 'CAROLINA LANTERNS & LIGHTING', 'revenue': 21.25}, {'customer': 'HOME CONCEPTS-I', 'revenue': 21.25}, {'customer': 'AMINIS HOME, RUG & GAME', 'revenue': 21.25}, {'customer': '43RD STREET LIGHTING', 'revenue': 20.5}, {'customer': 'HOME CENTER INC', 'revenue': 19.25}, {'customer': 'GW KEETER LIGHTING & HOME', 'revenue': 19.25}, {'customer': 'MAGNOLIA LIGHTING INC', 'revenue': 19.25}, {'customer': 'RADUE HOMES DBA INSPIRED SPACE', 'revenue': 19.25}, {'customer': 'LIGHTING SPECIALIST INC', 'revenue': 19.25}, {'customer': 'DISPLAY MERCHANDISE-10', 'revenue': 19.25}, {'customer': 'ALL-LITE', 'revenue': 19.25}, {'customer': 'MOUNTAIN LIGHTING', 'revenue': 19.25}, {'customer': 'BRIGHTER HOMES LIGHTING', 'revenue': 19.25}, {'customer': 'TURN-ON LIGHTING', 'revenue': 19.25}, {'customer': "METTE'S DISTINCTIVE LIGHTING", 'revenue': 18.29}] | [{'item': 'Z103-TB', 'desc': "Contractor's 1 Light Small Outdoor Wall Mount in Textured Black", 'available': 442}, {'item': 'Z402-DTZ', 'desc': '2 Light Directional Bullet in Dark Textured Bronze', 'available': 365}, {'item': 'Z402-TW', 'desc': '2 Light Directional Bullet in Textured White', 'available': 275}, {'item': 'Z433-TB', 'desc': 'Bent Glass 3 Light Flushmount in Textured Black', 'available': 241}] |
| PH-2BZ | 2 Light PAR Holder in Bronze | COL346 | 132,166.63 | 17,134 | 68 | — | [{'customer': 'FERGUSON ENTERPRISES INC', 'revenue': 25128.12}, {'customer': 'SUNBELT FANS & LIGHTING', 'revenue': 22121.7}, {'customer': 'SCARBORO LIGHTING', 'revenue': 11531.35}, {'customer': "HAGEN'S", 'revenue': 7663.2}, {'customer': 'TEXAS BRIGHT IDEAS, INC', 'revenue': 6020.7}, {'customer': 'DEALERS ELECTRICAL SUPPLY', 'revenue': 5404.8}, {'customer': 'WILKINSON ELECTRIC INC', 'revenue': 4633.2}, {'customer': 'FORT WORTH LIGHTING', 'revenue': 4424.8}, {'customer': 'ENTERPRISE WHOLESALE INC', 'revenue': 3607.2}, {'customer': 'R.D.H.S.INC', 'revenue': 2876.35}, {'customer': 'RIVER CITIES LIGHTING & RUG', 'revenue': 2454.9}, {'customer': 'GORMAN BROS', 'revenue': 2416.8}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 2364.0}, {'customer': 'LIFESTYLES  STORES INC', 'revenue': 2233.25}, {'customer': "CAROL'S LIGHTING & FAN SHOP", 'revenue': 2204.4}, {'customer': 'SOUTHERN LIGHTING LLC', 'revenue': 1845.35}, {'customer': 'CLARKSVILLE LIGHTING', 'revenue': 1803.6}, {'customer': "LOWE'S CO.- SOS CRAFTMADE", 'revenue': 1665.03}, {'customer': 'ROYAL ENTERPRISES', 'revenue': 1618.75}, {'customer': 'APPLICO APPLIANCE & LTG', 'revenue': 1603.2}, {'customer': 'JOHN WARD INTERIORS & GIFTS', 'revenue': 1402.8}, {'customer': 'THE LIGHTING GALLERY LLC', 'revenue': 1291.4}, {'customer': 'WOLFE LIGHTING & ACCENTS LLC', 'revenue': 1235.0}, {'customer': 'THE GALLERY OF LIGHTS', 'revenue': 1227.6}, {'customer': 'LANTERN HOUSE INC', 'revenue': 1202.4}, {'customer': 'HAMBUCHEN LIGHTING CO', 'revenue': 840.0}, {'customer': 'FIXTURE THIS INC', 'revenue': 813.6}, {'customer': 'C.E.D.', 'revenue': 729.6}, {'customer': 'HALL ELECTRIC', 'revenue': 717.6}, {'customer': 'AMOS ELECTRIC SUPPLY COMPANY', 'revenue': 626.25}, {'customer': 'BRIGHT IDEAS LTG & MORE', 'revenue': 518.4}, {'customer': 'KWK INVESTMENTS LLC', 'revenue': 501.0}, {'customer': 'IBS LIGHTING LTD.', 'revenue': 501.0}, {'customer': 'TRI SUPPLY', 'revenue': 444.55}, {'customer': 'COASTAL LIGHTING, LLC', 'revenue': 430.86}, {'customer': 'FERGUSONHOME.COM', 'revenue': 428.79}, {'customer': 'TRINITY WHOLESALE DIST INC', 'revenue': 425.85}, {'customer': 'LIGHTING INC.', 'revenue': 416.7}, {'customer': 'LIGHTING CONCEPTS LLC', 'revenue': 400.8}, {'customer': 'AMERICAN LIGHTING', 'revenue': 308.95}, {'customer': 'LIGHTS OF OCONEE LLC', 'revenue': 275.55}, {'customer': 'ENDACOTT LIGHTING AND LAMPS', 'revenue': 233.8}, {'customer': 'LIGHTING ETC', 'revenue': 233.8}, {'customer': 'HOUSE OF LIGHTS OF CARY INC', 'revenue': 227.5}, {'customer': 'PRICE WHOLESALE LIGHTING', 'revenue': 212.4}, {'customer': 'FACTORY LIGHTING OUTLET INC', 'revenue': 212.1}, {'customer': 'CREGGER COMPANY LLC', 'revenue': 210.0}, {'customer': 'LIGHT SYSTEMS INC', 'revenue': 199.95}, {'customer': 'PROGRESSIVE LTG - DROPSHIP', 'revenue': 189.12}, {'customer': 'TIMBERLAKE LTG-LYNCHBURG', 'revenue': 188.4}, {'customer': 'RDT LIGHTING & ELECTRIC LTD', 'revenue': 184.7}, {'customer': 'DOLAN NORTHWEST, LLC', 'revenue': 168.0}, {'customer': 'RICHARDS LIGHTING', 'revenue': 167.0}, {'customer': 'CUSTOM LIGHTING INC', 'revenue': 135.2}, {'customer': 'BRAZORIA COUNTY LIGHTING', 'revenue': 131.25}, {'customer': 'BULB BIN INC', 'revenue': 116.9}, {'customer': 'HEIGHTS LIGHTS & THINGS', 'revenue': 105.0}, {'customer': 'J & B SUPPLY INC', 'revenue': 100.2}, {'customer': 'SEQUEL ELECTRICAL SUPPLY, LLC', 'revenue': 100.2}, {'customer': 'TLC LIGHTING ON, LLC', 'revenue': 100.2}, {'customer': "GRAHAM'S LIGHTING FIXTURES INC", 'revenue': 83.5}, {'customer': 'BELLACOR.COM INC-I', 'revenue': 61.6}, {'customer': 'HAYNEEDLE,INC-I', 'revenue': 53.05}, {'customer': 'WAYFAIR LLC-I', 'revenue': 51.56}, {'customer': '1STOPLIGHTING-I', 'revenue': 47.61}, {'customer': 'KINGS WAGON YARD', 'revenue': 41.75}, {'customer': 'LIGHTING BY LAVONNE', 'revenue': 33.4}, {'customer': 'COBURN SUPPLY COMPANY INC', 'revenue': 25.05}, {'customer': 'OLDE PARSONAGE THE', 'revenue': 25.05}, {'customer': 'METRO LIGHTING', 'revenue': 25.05}, {'customer': 'LDB HOLDINGS, LLC', 'revenue': 16.7}, {'customer': 'PLUMBING DISTRIBUTORS INC', 'revenue': 16.7}, {'customer': 'LIGHTING BY JARED, INC.-I', 'revenue': 15.75}, {'customer': "GARBE'S LIGHTING AND HARDWARE", 'revenue': 15.2}, {'customer': 'PARKER COUNTY GALLERY OF LIGHT', 'revenue': 15.2}, {'customer': 'KEITH EICHENBLATT', 'revenue': 14.0}, {'customer': 'FELT LIGHTING CO', 'revenue': 8.75}, {'customer': 'RITE RUG CO.', 'revenue': 8.75}, {'customer': 'FURNITURE SHOWCASE', 'revenue': 8.75}, {'customer': 'Peak Lighting Bulbs & Ballast', 'revenue': 8.35}, {'customer': 'FERGUSONSHOWROOMS.COM', 'revenue': 8.14}, {'customer': 'PROGRESSIVE LIGHTING INC', 'revenue': 7.6}] | — |
