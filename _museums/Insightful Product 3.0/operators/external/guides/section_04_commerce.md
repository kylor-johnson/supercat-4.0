# Section Guide: Commerce Patterns
> **v3.0** — signal-first architecture. Only non-obvious patterns a client can't see in their own systems.

## Section Identity

- **id**: `commerce`
- **title**: Commerce Patterns
- **section number**: 4
- **include when**: `signal_rank.md` shows ≥ 1 P0/P1 signal with `Section Home = Commerce Patterns`, OR at least 3 of the 12 subsections below pass their individual gates
- **skip when**: 0 relevant P0/P1 signals AND fewer than 3 subsections have data

## Query Inputs

Read these cache files:

- `cache/signal_rank.md` — ranked signal manifest
- `cache/Q-13_results.md` — Customer concentration risk (top-buyer eCat GMV share)
- `cache/Q-18_results.md` — eCat order trend, channel breakdown, and rep-level performance
- `cache/Q-19_results.md` — Order channel mix (iPad vs eCat Online vs other)
- `cache/Q-20_results.md` — Order type breakdown (Confirmed, Quote, etc.)
- `cache/Q-21_results.md` — Order type & workflow distribution
- `cache/Q-41_results.md` — New eCat buyer acquisition trend
- `cache/Q-45_results.md` — eCat capture rate
- `cache/Q-52_results.md` — eCat penetration of total business by customer (**MANDATORY when gate met**: if `PORTAL_CUSTOMER_DATA_PRESENT = true` AND this file contains data rows, subsection 4 Top Buyers table MUST include enrichment columns)
- `cache/Q-55_results.md` — Category-level competitive displacement (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains displacement rows, subsection 9 MUST be rendered)
- `cache/Q-56_results.md` — Per-rep capture rate trend (conditional: render Part B of subsection 9 if `PORTAL_REP_DATA_PRESENT = true` AND data rows show declining reps)
- `cache/Q-58_results.md` — Market commitment conversion (**MANDATORY when gate met**: if `HAS_COMMITMENT_DATA = true` AND this file contains data rows, subsection 11 MUST be rendered)
- `cache/Q-58b_results.md` — Uncommitted market items in stock (conditional: render Part B of subsection 11 if `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND data rows exist)
- `cache/Q-60_results.md` — Price erosion / trade-down detection (**MANDATORY when gate met**: if `HAS_PORTAL_ORDERS = true` AND this file contains data rows, subsection 10 MUST be rendered)
- `cache/Q-69_results.md` — Order timing distribution (reserved for future use)
- `cache/Q-ORG-VELOCITY_results.md` — Account velocity patterns
- `cache/gate_flags.md` — data availability gates
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_4` tier

## CRITICAL REQUIREMENTS — Read Before Building

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **Q-52 MANDATORY ENRICHMENT**: If `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `Q-52_results.md` has data rows, the Top Buyers table (subsection 4) MUST include "Total Business" and "eCat Share" columns.
2. **HAS_PORTAL_ORDERS GATE**: If `HAS_PORTAL_ORDERS = false`, subsections 1 (Part B of eCat Capture Rate), 3 (Channel Migration share-of-total overlay), 9 (Competitive Displacement), and 10 (Price Erosion) are ALL skipped. Do not mention total business anywhere.
3. **Q-55 COMPETITIVE DISPLACEMENT**: If `HAS_PORTAL_ORDERS = true` AND `Q-55_results.md` has rows where total grew but eCat share shrank, subsection 9 MUST be rendered. MANDATORY.
4. **Q-60 PRICE EROSION**: If `HAS_PORTAL_ORDERS = true` AND `Q-60_results.md` has data rows, subsection 10 MUST be rendered. MANDATORY.
5. **Q-58 MARKET ATTRIBUTION**: If `HAS_COMMITMENT_DATA = true` AND `Q-58_results.md` has data rows, subsection 11 MUST be rendered. MANDATORY.
6. **Q-58b IN-STOCK ITEMS**: If `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND `Q-58b_results.md` has data rows, subsection 11 Part B MUST be rendered.
7. **CONFIDENCE HEADER**: Every §4 fragment MUST contain a confidence header **at the top of the section** (immediately after the header metrics, before any subsection content). This is NOT optional — if the confidence header is missing, the fragment is defective. Read `SECTION_CONFIDENCE_4` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags.

---

## PRE-BUILD GATE CHECK

> Follow `section_shared_contract.md` §1 for the gate check process.

| Flag | Used by |
|------|---------|
| `HAS_PORTAL_ORDERS` | Subsections 1 (Part B), 3 (share overlay), 9, 10 |
| `HAS_CART` | Subsection 3 (channel breakdown) |
| `HAS_COMMITMENT_DATA` | Subsection 11 |
| `HAS_INVENTORY` | Subsection 11 (Part B) |
| `VM45_RENDER` | Subsection 1 (capture rate denominator validity) |
| `PORTAL_CUSTOMER_DATA_PRESENT` | Subsection 4 (Q-52 enrichment) |
| `PORTAL_REP_DATA_PRESENT` | Subsection 9 (Part B) |

---

## Fragment Structure

Uses the standard `<details class="section-collapse">` wrapper per shared_rules.md Section E.

```
Section ID: commerce
Section Number: §4
```

---

## Guiding Principle

**Our value = cross-system patterns only our data position enables.** If a client could pull this from their own dashboard, don't show it. Every subsection must reveal something that requires cross-referencing eCat behavioral data, multi-source order data, or platform-specific intelligence.

---

## Content Blocks (render in NARRATIVE ARC order — each is independently gated)

**Rendering order within this section (strength → intelligence → opportunity → risk):**
0. Order Channel Mix (CONTEXT — the FULL digital picture + the digital-enablement opportunity; render FIRST)
1. eCat Footprint (CONTEXT — eCat's volume as a tool in the mix, NOT a share-to-grow)
2. eCat Order Trend (STRENGTH — the growth trajectory, framed as "more orders digitized")
4. Top Buyers & Concentration (INTELLIGENCE — who's buying)
6. Order Type & Workflow (INTELLIGENCE — how they're buying)
3. Channel Migration (INTELLIGENCE — where they're buying)
11. Market Commitment Attribution (OPPORTUNITY — pipeline conversion)
5. Quote Economics (OPPORTUNITY — conversion upside)
8. AOV Spread by Rep (OPPORTUNITY — coaching upside)
12. First-Time Buyer Acquisition (INTELLIGENCE — pipeline health)
7. Seasonal Timing (INTELLIGENCE — timing patterns)
9. Competitive Displacement (RISK — render late)
10. Price Erosion (RISK — render last)

### 0. Order Channel Mix (conditional — render FIRST when present)

**Gate**: `HAS_PORTAL_ORDERS = true` AND `cache/Q-CHANNEL-MIX_results.md` exists with data rows.

**FRAMING — THIS IS A CORE EDITORIAL RULE FOR THE WHOLE SECTION:** eCat is ONE of several
channels a customer can order through. Most clients also run their OWN digital channels — a B2B
web storefront, EDI / drop-ship integrations — and a large share of their orders are **already
digital, just not through eCat**. NEVER assume or imply that orders outside eCat are "manual,"
"offline," "phone," "paper," or "non-digital." This subsection shows the real channel mix so eCat
is positioned honestly.

`Q-CHANNEL-MIX_results.md` classifies total business (the ERP loop-back) into: eCat · Your B2B web
storefront · EDI/drop-ship · Trade markets/showrooms · Rep- or ERP-entered · Unclassified.

**If the file does NOT contain a `DATA NOTE`** (i.e., the ERP feed distinguishes channels — only
some clients): render the channel table and lead with the honest picture.

```html
<div class="subsection">
  <div class="subsection-title">Order Channel Mix</div>
  <table>
    <thead><tr><th>Channel</th><th>Orders (LTM)</th><th>GMV (LTM)</th><th>% of Total Business</th></tr></thead>
    <tbody>{{rows from Q-CHANNEL-MIX; row-highlight the largest digital channel}}</tbody>
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> {{State the split: e.g. "$44.4M (50%) of your business is already ordered
    through self-service digital channels — your own B2B web ($23.7M), EDI/drop-ship ($12.6M), and eCat
    ($8.0M)."}} {{Name the opportunity as the rep-/back-office-entered volume: "The bigger opportunity is
    the $25.2M (29%) still entered by reps or the back office — typically phone and email orders keyed in
    by hand. Moving part of that to digital ordering — eCat for rep-assisted and field orders, your own web
    for self-service buyers — removes order-entry time and errors."}} {{Name eCat's specific strength
    (rep-assisted/field/showroom/visual selling) so it reads as a tool, not a quota.}}
  </div>
</div>
```

**Rules — THE THESIS (read carefully):** The story is **digital enablement, not eCat market share.**
1. Lead with what's ALREADY self-service digital (eCat + web + EDI) — that volume is healthy, leave it be.
2. Name the **opportunity as the rep-/back-office-entered volume** (where the channel data shows it) —
   the phone/email/manually-keyed orders. Streamlining those into digital commerce is the value:
   less manual entry, fewer errors, faster turnaround.
3. Both **eCat AND the client's own web** are valid digital paths — eCat for rep-assisted/field/showroom/
   visual selling, their web for self-service. Do NOT pitch moving orders FROM the client's web TO eCat.
4. **NEVER** frame this as "grow eCat's share / capture rate / each point is worth $X / lift from A% to B%."
   The goal is less manual order entry, not more eCat. And NEVER call the rep/back-office volume "manual"
   as a certainty if you can't see it — say "rep- or back-office-entered" and note it often starts as phone/email.
5. Do not make eCat look obsolete or redundant — always name where it specifically helps.

**If the file CONTAINS a `DATA NOTE`** (>80% Rep/ERP/Unclassified — the ERP feed lacks channel
detail, true for most clients): SKIP the table. Render one honest paragraph instead:
> "Your ERP feed doesn't yet break out how orders are placed, so we're showing eCat ordering on its
> own below. Orders outside eCat run through your reps, back office, and — for many distributors —
> your own digital or B2B channels; we just can't separate them from this feed yet. Connecting
> richer order-origin data would let us show your full channel mix and position eCat precisely within it."

**Data source**: `Q-CHANNEL-MIX_results.md`

---

### 1. eCat Footprint (conditional)

**Gate**: `HAS_PORTAL_ORDERS = true` (from gate_flags) AND gate_flags shows commerce data sufficient for the computation.

eCat's volume within the order mix — descriptive context for the channel-mix story above. This is
eCat's **footprint as a tool**, NOT a "share to grow." Do not turn it into a capture-rate quota.

```html
<div class="subsection">
  <div class="subsection-title">eCat Footprint</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val">{{ECAT_GMV}}</div>
      <div class="metric-label">Orders Placed Through eCat</div>
      <div class="metric-note">Trailing 12 months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">{{CAPTURE_PCT}}%</div>
      <div class="metric-label">Of Total Business</div>
      <div class="metric-note">{{eCat alongside the client's other digital + rep channels}}</div>
    </div>
  </div>
```

Show eCat's footprint factually. If a quarterly trend exists, show the trajectory in a `.callout.insight`
(growth is good news — celebrate it — but frame it as "more orders digitized," not "share captured").
Do NOT render an "Adoption Stage" ladder or any "Early/Emerging/Dominant" grow-the-share classification.

If `VM45_RENDER = false` (denominator gate failed): show eCat's standalone volume and add one prose line:
"A precise eCat-vs-total-business view needs consistent data between eCat and total-business records —
available when data synchronization is validated."

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{Describe eCat's role in the mix, then point at the enablement opportunity:
    e.g. "eCat handles $8.0M today, concentrated in rep-assisted and field orders. The opportunity isn't
    a bigger eCat number for its own sake — it's the rep-/back-office-entered volume (phone and email
    orders keyed by hand) that eCat or your own web could absorb, cutting entry time and errors."}}
    {{NEVER "growing eCat from X% to Y% adds $Z."}}
  </div>
</div>
```

**Data source**: `Q-45_results.md`, `Q-16_results.md`, `Q-CHANNEL-MIX_results.md`

**Claim rules — enablement, not adoption:**
- This is eCat's **footprint**, not "the digital share" and not a capture target. **Never** use "capture rate,"
  "adoption stage," "each point is worth $X," or "grow/lift eCat from A% to B%."
- The opportunity is **digitizing the rep-/phone-/email-entered order flow** (see Order Channel Mix) — and
  eCat **and the client's own web** are both valid paths for that. Don't pitch share migration between the
  client's own digital channels.
- **Never** imply orders outside eCat are non-digital/manual/offline as a certainty — many are the client's
  own web/EDI (already digital). Where the feed can't distinguish, say "rep- or back-office-entered."
- Celebrate real eCat growth as "more orders digitized / less manual entry," and always name eCat's specific
  strength (rep-assisted/field/showroom/visual selling) so it never reads as obsolete.

---

### 2. eCat Order Trend (always)

**Gate**: Always render Part A. Part B conditional on `HAS_PORTAL_ORDERS = true`.

**Data source**: `Q-18_results.md`

**Part A** (always): eCat order trend — eCat-originated orders only. Show monthly or quarterly volume over time.

```html
<div class="subsection">
  <div class="subsection-title">eCat Order Trend</div>
  <table>
    <tr><th>Period</th><th>eCat Orders</th><th>eCat GMV</th><th>Avg Order Value</th></tr>
    {{ROWS — one per month/quarter, chronological}}
  </table>
```

**Part B** (only if `HAS_PORTAL_ORDERS = true`): Add eCat share of total business trend alongside Part A. Extend the table with additional columns:

```html
  <table>
    <tr><th>Period</th><th>eCat Orders</th><th>eCat GMV</th><th>Total Business</th><th>eCat Share</th><th>Avg Order Value</th></tr>
    {{ROWS — one per month/quarter, chronological, with total business and share columns}}
  </table>
```

**What-this-means guidance**: Frame like an analyst comparing seasonality to growth. Highlight peak months, note partial-period artifacts, and contextualize whether the trend is stable, accelerating, or cyclical. Example: "eCat ordering peaked in [month] with consistent monthly volume of X–Y orders. The partial-month dip at period boundaries reflects data truncation, not declining demand."

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{TREND_NARRATIVE — contextualize whether volume is stable, accelerating, seasonal, or cyclical. Highlight the peak period and note any partial-period artifacts at data boundaries.}}
  </div>
</div>
```

**Claim rules**: Never attribute a partial-period drop to declining demand without explicit evidence. Always note when the first or last period in the range is truncated. If Part B is present, frame the eCat share trajectory — is it growing, flat, or declining relative to total business?

---

### 3. Channel Migration / Channel Breakdown (conditional)

**Gate**: `order_origin` or `order_source` populated across orders, with at least 2 distinct channels AND 6+ months of history. If `HAS_CART = true`, render iPad vs eCat Online channel split from Q-18 data.

**Data source**: `Q-18_results.md`, `Q-19_results.md`

Shifts between iPad / eCat Online / other channels over time.

```html
<div class="subsection">
  <div class="subsection-title">Channel Migration</div>
  <table>
    <tr><th>Channel</th><th>Prior Period GMV</th><th>Current Period GMV</th><th>Share Change</th><th>Order Count Change</th></tr>
    {{ROWS — one per channel}}
  </table>
```

Key question to answer: Is self-service (eCat Online) growing relative to rep-mediated (iPad)? Frame the shift narrative:

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CHANNEL_SHIFT_NARRATIVE — e.g., "Self-service ordering grew from X% to Y% of platform volume. Your buyers are increasingly comfortable ordering without rep involvement — protect this by ensuring the online catalog and pricing are current."}}
  </div>
</div>
```

**Channel attribution statement** (required when `HAS_CART = true`): "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." Do not use code literals like `order_source = 'ipad'` in client-facing prose.

**What-this-means guidance**: Frame the channel mix as adoption signal. If one channel dominates, explain what that implies about buyer behavior. Example: "100% iPad ordering reflects a rep-driven sales model. Activating eCat Online would add a self-service channel for reorders and lower-touch accounts without displacing rep relationships."

**Claim rules**: Never use "portal ordering" — say "self-service ordering" or "eCat Online." Frame channel shifts as adoption evolution, not channel conflict.

---

### 4. Top Buyers & Concentration (always)

**Gate**: Always render. Q-52 enrichment is MANDATORY when `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-52_results.md` exists with data rows.

**Data source**: `Q-13_results.md`, `Q-52_results.md` (when gate met)

Show top 10 buyers by eCat GMV with these exact columns:

| Column | Content |
|--------|---------|
| Customer | Buyer name |
| Orders | eCat order count |
| GMV | eCat GMV |
| % of eCat GMV | Buyer's share of total eCat GMV |

```html
<div class="subsection">
  <div class="subsection-title">Top Buyers & Concentration</div>
```

Include a concentration callout if top-5 buyers exceed 25% of total eCat GMV:

```html
  <div class="callout insight">
    <div class="callout-title">Revenue Concentration</div>
    <p>Your top 5 eCat buyers account for {{TOP5_PCT}}% of total platform GMV (${{TOP5_GMV}} of ${{TOTAL_GMV}}). {{CONCENTRATION_IMPLICATION}}.</p>
  </div>
```

```html
  <table>
    <tr><th>Customer</th><th>Orders</th><th>GMV</th><th>% of eCat GMV</th></tr>
    {{ROWS — top 10 by GMV, sorted descending}}
  </table>
```

**MANDATORY ENRICHMENT** (when `PORTAL_CUSTOMER_DATA_PRESENT = true` AND `cache/Q-52_results.md` exists with data rows): You MUST add two columns to the table using `cache/Q-52_results.md` data joined on customer identifier — "Total Business" (all-channel GMV) and "eCat Share" (`ecat_gmv / total_business_gmv × 100`). When `PORTAL_CUSTOMER_DATA_PRESENT = false` OR the file is absent OR it contains zero rows, render the Q-13-only table unchanged — do not add empty columns or placeholders.

Enriched table header when Q-52 is available:

```html
  <table>
    <tr><th>Customer</th><th>Orders</th><th>GMV</th><th>% of eCat GMV</th><th>Total Business</th><th>eCat Share</th></tr>
    {{ROWS — top 10 by GMV, sorted descending, with total business and penetration columns from Q-52}}
  </table>
```

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CONCENTRATION_NARRATIVE — assess concentration risk like a portfolio analyst. Low concentration = stability but broad-based growth needed. High concentration = key-account dependency risk. When enrichment is present, highlight penetration gaps: "Your largest eCat buyer generates $X on the platform but $Y in total business — there's headroom to capture more of their spend digitally."}}
  </div>
</div>
```

**Claim rules**: Never expose internal customer identifiers (`customer_bill_to_number`, etc.). Use buyer names only. Frame concentration as portfolio risk analysis. When enrichment is present, frame penetration gaps as growth opportunity.

---

### 5. Quote Economics (conditional)

**Gate**: `Q-20_results.md` or `Q-45_results.md` shows Quote-type orders AND Confirmed-type orders with sufficient volume (10+ quotes).

**Data source**: `Q-20_results.md`, `Q-45_results.md`

The spread between Quote AOV and Confirmed AOV, and the dollar opportunity if conversion improved.

```html
<div class="subsection">
  <div class="subsection-title">Quote Economics</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val">${{QUOTE_AOV}}</div>
      <div class="metric-label">Avg Quote Value</div>
      <div class="metric-note">{{QUOTE_COUNT}} quotes, trailing 12 months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${{CONFIRMED_AOV}}</div>
      <div class="metric-label">Avg Confirmed Order Value</div>
      <div class="metric-note">{{CONFIRMED_COUNT}} orders, trailing 12 months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${{SPREAD}}</div>
      <div class="metric-label">AOV Spread</div>
      <div class="metric-note">Quotes {{HIGHER_OR_LOWER}} than confirmed</div>
    </div>
  </div>
  <p class="prose">If quote-to-confirmed conversion improved by 10 percentage points, that's an estimated ${{INCREMENTAL}} in incremental annual revenue.</p>
  <div class="what-this-means">
    <strong>Action:</strong> {{QUOTE_ECONOMICS_IMPLICATION — e.g., "Quotes are 40% larger than confirmed orders on average, which means your highest-value opportunities are the ones most likely to stall. Focus rep follow-up on quotes > $X to capture the top of the pipeline."}}
  </div>
</div>
```

Hedge the 10pp improvement projection with "estimated" language.

**Claim rules**: Always hedge conversion improvement projections. Never promise specific ROI — use "estimated," "potential," "approximately."

---

### 6. Order Type & Workflow (always)

**Gate**: Always render. Build from `Q-21_results.md`.

**Data source**: `Q-21_results.md`

**Framing principle**: Lead with the quote premium insight — the AOV difference between quote orders and confirmed orders. The full type distribution table is supporting detail, not the headline. Most clients already know their team places confirmed orders; what they don't know is the dollar multiplier on quotes.

**Required content:**
- `.callout.insight` leading with the quote premium: "Your quote orders average $X — Nx the standard confirmed order value ($Y). Increasing quote-to-confirmed conversion is your highest-leverage volume opportunity." If no quote orders exist, lead with the dominant workflow pattern instead.
- Full order type distribution table inside a collapsed `<details>` block with summary "View order type breakdown":

| Column | Content |
|--------|---------|
| Order Type | Type name (Confirmed, Quote, HFC, etc.) |
| Orders | Count |
| Share | Percentage of total orders |
| Avg Order Value | AOV for that type |

```html
<div class="subsection">
  <div class="subsection-title">Order Type & Workflow</div>
  <div class="callout insight">
    <div class="callout-title">Quote Premium</div>
    <p>Your quote orders average ${{QUOTE_AOV}} — {{MULTIPLIER}}x the standard confirmed order value (${{CONFIRMED_AOV}}). Increasing quote-to-confirmed conversion is your highest-leverage volume opportunity.</p>
  </div>
  <details>
    <summary>View order type breakdown</summary>
    <table>
      <tr><th>Order Type</th><th>Orders</th><th>Share</th><th>Avg Order Value</th></tr>
      {{ROWS — one per order type, sorted by order count descending}}
    </table>
  </details>
```

- If HFC (Hold for Confirmation) orders exist, note in prose that the approval workflow serves compliance or high-value transaction governance.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{ORDER_TYPE_IMPLICATION — Focus on the actionable insight from the type distribution, not the distribution itself. Example: "The Nx AOV premium on quotes means each converted quote is worth N standard orders. If even X% more quotes converted to confirmed, that would add $Y in platform GMV." Do not restate "96% of your orders are confirmed" — the reader can see that in the collapsed table.}}
  </div>
</div>
```

**Claim rules**: Lead with the non-obvious insight (quote premium multiplier), not the obvious (order type distribution). Hedge conversion improvement estimates. Never expose internal order type codes.

---

### 7. Seasonal Timing (conditional)

**Gate**: 12+ months of order data available (check Q-21 for monthly time series spanning at least 12 months).

**Data source**: `Q-21_results.md`

Monthly revenue pattern with peak identification.

```html
<div class="subsection">
  <div class="subsection-title">Ordering Seasonality</div>
  <table>
    <tr><th>Month</th><th>Avg Monthly Revenue</th><th>% of Annual</th><th>Relative Intensity</th></tr>
    {{12 ROWS — one per month, averaged across available years}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> Your ordering peaks in {{PEAK_MONTHS}} — align inventory builds, rep outreach campaigns, and new product launches to lead these peaks by 4–6 weeks. {{TROUGH_INSIGHT — e.g., "The Q3 trough (July–August) may be an opportunity for targeted promotions to flatten the curve."}}
  </div>
</div>
```

"Relative Intensity" column: show as a visual indicator. Use `.badge.ok` for peak months (> 10% of annual), `.badge.muted` for average months, `.badge.warn` for trough months (< 6% of annual). `[COLLAPSE]`

**Claim rules**: Frame troughs as promotional opportunities, not failures. Never attribute seasonality to a single cause without evidence.

---

### 8. AOV Spread by Rep (conditional)

**Gate**: `Q-18_results.md` shows rep-level AOV data AND the spread between highest and lowest active rep AOV is > 2x.

**SKIP if spread ≤ 2x.** A small spread is normal and not actionable.

**Data source**: `Q-18_results.md`

```html
<div class="subsection">
  <div class="subsection-title">Average Order Value Spread by Rep</div>
  <div class="callout insight">
    <div class="callout-title">{{SPREAD_RATIO}}x AOV gap across your team</div>
    <p>Your highest-AOV rep averages ${{HIGH_AOV}} per order. Your lowest: ${{LOW_AOV}}. If the bottom quartile matched the median (${{MEDIAN_AOV}}), that's an estimated ${{UPSIDE}} in incremental annual revenue.</p>
  </div>
  <table>
    <tr><th>Rep</th><th>Orders (LTM)</th><th>GMV (LTM)</th><th>AOV</th><th>vs Median</th></tr>
    {{ROWS — sorted by AOV desc, top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> A large AOV spread usually means reps are selling into different customer segments, or some reps are better at bundling and upselling. Investigate whether low-AOV reps are serving smaller accounts (normal) or leaving money on the table with the same customers (coachable).
  </div>
</div>
```

"vs Median" column: `.badge.ok` if above median, `.badge.warn` if below. Show as percentage above/below.

**Claim rules**: Frame AOV gaps as coaching opportunity, not rep failure. Always acknowledge that customer mix may explain differences.

---

### 9. Competitive Displacement Signals (conditional) — MANDATORY WHEN GATE MET

**Gate**: `HAS_PORTAL_ORDERS = true` — if false, skip this entire subsection silently.

**MANDATORY RENDER**: If `cache/Q-55_results.md` exists AND contains data rows showing at least one category where `total_growth_pct > 0` AND `ecat_share_change_ppts < 0`, this subsection MUST appear. If no category meets the displacement criteria (total grew but eCat share shrank), skip silently — no false alarm.

**Data sources**: `cache/Q-55_results.md` (category displacement), `cache/Q-56_results.md` (rep capture trend)

**Part A — Category Displacement (Q-55):**

Open with a `.callout.insight` (NOT `.callout.alert`) titled "Channel Share Opportunity". Frame as recapturable revenue, not loss.

```html
<div class="subsection">
  <div class="subsection-title">Channel Share Opportunity</div>
  <div class="callout insight">
    <div class="callout-title">Platform Share Gap in Growing Categories</div>
    <p>In {{COUNT}} categories, total business grew while platform share declined — an estimated ${{DISPLACED_TOTAL}} in additional platform revenue is available if channel share is recovered.</p>
  </div>
  <table>
    <tr>
      <th>Category</th>
      <th>Total Business (Current Qtr)</th>
      <th>Total Growth</th>
      <th>Platform Share (Prior)</th>
      <th>Platform Share (Current)</th>
      <th>Share Change</th>
      <th>Est. Displaced</th>
    </tr>
    {{ROWS — categories where total_growth_pct > 0 AND ecat_share_change_ppts < 0}}
  </table>
```

Render table with categories that show displacement (where `total_growth_pct > 0` AND `ecat_share_change_ppts < 0`):

| Column | Content |
|--------|---------|
| Category | Product category name |
| Total Business (Current Qtr) | `current_total_gmv` |
| Total Growth | `total_growth_pct` with `.badge.ok` |
| Platform Share (Prior) | `prior_ecat_share_pct` |
| Platform Share (Current) | `current_ecat_share_pct` |
| Share Change | `ecat_share_change_ppts` with `.badge.danger` (negative = red) |
| Est. Displaced | Calculated: `(prior_ecat_share_pct/100 × current_total_gmv) - current_ecat_gmv` |

Show all displacement categories (typically 3–8). If more than 5, collapse remaining in `<details>`.

**Part B — Rep Capture Rate Trend (Q-56, conditional):**

If `cache/Q-56_results.md` exists AND contains data rows AND `PORTAL_REP_DATA_PRESENT = true`, render a supplementary table showing reps whose capture rate declined:

| Column | Content |
|--------|---------|
| Rep | Rep name (never expose internal identifiers) |
| Total Business (Current) | `current_total_gmv` |
| Prior Capture % | `prior_capture_pct` |
| Current Capture % | `current_capture_pct` |
| Change | `capture_change_ppts` with badge (`.badge.danger` if ≤ -5, `.badge.warn` if -5 to 0) |

```html
  <h4>Rep Capture Rate Trend</h4>
  <table>
    <tr>
      <th>Rep</th>
      <th>Total Business (Current)</th>
      <th>Prior Capture %</th>
      <th>Current Capture %</th>
      <th>Change</th>
    </tr>
    {{ROWS — reps where capture_change_ppts < 0, sorted by current_total_gmv desc, top 5 visible}}
  </table>
```

Show only reps where `capture_change_ppts < 0` (declining), sorted by `current_total_gmv` descending. Top 5 visible, remaining in `<details>`. If no reps show decline, omit Part B silently.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{DISPLACEMENT_NARRATIVE — investigative, not accusatory. Example: "In X categories, total business grew while your platform share declined. This pattern may reflect buyers shifting to alternative ordering channels, seasonal procurement timing, or competitive displacement — it warrants rep-level follow-up to understand the root cause." For Part B: "These reps manage growing accounts but are capturing less of that growth on the platform — a focused enablement conversation could recapture share."}}
  </div>
</div>
```

**Claim rules**: "Total business in [Category] grew X%, but your platform captured Y fewer percentage points of that growth — an estimated $Z shifted to other channels." ALWAYS hedge: "estimated," "may have shifted," "suggests." Never say definitively "lost to competitors" — could be channel shift, timing, or seasonal patterns. Frame rep-level data as coaching opportunity, not failure. Never use "ERP," "portal_orders," or "portal ordering." Use "total business" and "all-channel."

---

### 10. Price Erosion / Trade-Down Detection (conditional) — MANDATORY WHEN GATE MET

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `cache/Q-60_results.md` has data rows.

**Data source**: `cache/Q-60_results.md` (deduplicated rows — one row per account showing QoQ avg unit price decline ≥ 4%)

**Rendering**: Open with a `.callout.insight` (NOT `.callout.warn`) titled "Product Mix Shift" — frame as an investigative finding, not an alarm.

```html
<div class="subsection">
  <div class="subsection-title">Product Mix & Pricing Trends</div>
  <div class="callout insight">
    <div class="callout-title">Product Mix Shift</div>
    <p>{{COUNT}} accounts show declining average unit prices quarter-over-quarter — combined current-quarter business: ${{COMBINED_GMV}}. This may indicate competitive pressure, shifting buyer mix, or product substitution.</p>
  </div>
  <table>
    <tr>
      <th>Account</th>
      <th>Prior Avg Price</th>
      <th>Current Avg Price</th>
      <th>Change</th>
      <th>Current Quarter GMV</th>
      <th>Orders</th>
    </tr>
    {{ROWS — sorted by current_quarter_gmv desc, top 5 visible, rest in <details>}}
  </table>
```

| Column | Content |
|--------|---------|
| Account | `customer_bill_to_name` |
| Prior Avg Price | `prior_avg_price` formatted as currency |
| Current Avg Price | `current_avg_price` formatted as currency |
| Change | `price_change_pct` with `.badge.danger` styling (all values are negative — use badge for visual urgency) |
| Current Quarter GMV | `current_quarter_gmv` formatted as currency |
| Orders | `current_orders` |

After the table, add a `.callout.insight` titled "Investigative Context":

```html
  <div class="callout insight">
    <div class="callout-title">Investigative Context</div>
    <p>Declining unit prices may reflect several dynamics: competitive pricing pressure driving buyers to request discounts, a natural shift toward lower-priced product tiers, changing buyer mix within an account, or seasonal promotional activity. These patterns warrant individual account review — they are signals to investigate, not conclusions to act on.</p>
  </div>
  <div class="what-this-means">
    <strong>Action:</strong> {{PRICE_EROSION_NARRATIVE — investigative, measured, multi-causal. Example: "X accounts are trending toward lower unit prices. This could reflect competitive pricing pressure, a shift toward different product tiers, or evolving buyer preferences within these accounts. The pattern is worth a focused conversation — particularly for accounts where current-quarter volume remains strong, suggesting the relationship is active but the product mix is shifting."}}
  </div>
</div>
```

**Tone**: Investigative, not alarmist. The `.badge.danger` on percentage declines provides visual urgency but the prose must remain measured and multi-causal. Never say "price erosion alert" in a way that implies the client is failing — frame as "pattern worth understanding."

**Part B — Category-Level Pricing Trends (render when Q-60 gate met AND category/collection data available from Q-39)**

This provides the diagnostic the user actually needs: are prices going up while units drop? Is volume loss in specific categories masking overall AOV changes?

**Data source**: Derive from `Q-60_results.md` aggregated by category, cross-referenced with `Q-39_results.md` for category-level unit volume.

```html
  <h4>Category-Level AOV Trends</h4>
  <div class="callout insight">
    <div class="callout-title">Price vs. Volume by Category</div>
    <p>{{DIAGNOSTIC_HEADLINE — e.g., "Your average selling price for Pendants increased 8% while units sold dropped 12%. In Chandeliers, both price and volume grew. The category-level view reveals whether AOV changes reflect intentional pricing strategy or demand erosion."}}</p>
  </div>
  <table>
    <tr>
      <th>Category</th>
      <th>Prior Avg Unit Price</th>
      <th>Current Avg Unit Price</th>
      <th>Price Change</th>
      <th>Prior Units</th>
      <th>Current Units</th>
      <th>Unit Change</th>
      <th>Diagnosis</th>
    </tr>
    {{ROWS — categories with meaningful price OR volume shifts, sorted by revenue impact desc}}
  </table>
```

**Diagnosis column** (computed per category):
| Pattern | Diagnosis | Badge |
|---------|-----------|-------|
| Price ↑, Units ↑ | "Healthy growth" | `.badge.ok` |
| Price ↑, Units ↓ | "Price sensitivity — may be losing volume to pricing" | `.badge.warn` |
| Price ↓, Units ↑ | "Volume play — lower prices driving adoption" | `.badge.muted` |
| Price ↓, Units ↓ | "Category contraction — investigate competitive pressure" | `.badge.danger` |
| Price flat, Units ↓ | "Demand erosion — not a price issue" | `.badge.warn` |

Only show categories where EITHER price change > 5% OR unit change > 10% — minor fluctuations are noise.

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{CATEGORY_PRICING_NARRATIVE — specific to org. Example: "Your Pendants category shows classic price sensitivity: an 8% price increase correlated with a 12% unit drop, netting a 5% revenue decline. Meanwhile, Bath Lighting grew both price (+3%) and volume (+18%) — suggesting strong market fit. The categories showing 'price sensitivity' are where competitor pricing comparisons would be most valuable."}}
  </div>
```

**When category data is insufficient**: If Q-39 doesn't have enough granularity to break pricing trends by category, omit Part B silently — the account-level view (Part A) still renders.

**Claim rules**: Always hedge — "correlated with" not "caused by." Frame price sensitivity as a hypothesis requiring investigation. Never definitively state "you raised prices too high" — say "the price increase correlated with volume loss in this category." Always hedge: "may reflect," "suggests," "warrants investigation."

---

### 11. Market Commitment Attribution (conditional) — MANDATORY WHEN GATE MET

**Gate**: `HAS_COMMITMENT_DATA = true` (read from `gate_flags.md`) — if false, skip this entire subsection silently.

**MANDATORY RENDER**: If `cache/Q-58_results.md` exists AND contains data rows, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-58_results.md`, `cache/Q-58b_results.md`

**Rendering**: Open with a `.callout.insight` block titled "Market Commitment Conversion" with a summary computed from the most recent market row: "At [market_code], your accounts committed to X items. Within 90 days, Y% converted to orders — Z items remain unrealized."

```html
<div class="subsection">
  <div class="subsection-title">Market Commitment Attribution</div>
  <div class="callout insight">
    <div class="callout-title">Market Commitment Conversion</div>
    <p>At {{MOST_RECENT_MARKET}}, your accounts committed to {{TOTAL_COMMITTED}} items. Within 90 days, {{CONVERSION_PCT}}% converted to orders — {{UNREALIZED}} items remain unrealized.</p>
  </div>
  <table>
    <tr>
      <th>Market</th>
      <th>Date</th>
      <th>Customers</th>
      <th>Items Committed</th>
      <th>Items Converted</th>
      <th>Conversion Rate</th>
      <th>Unrealized Items</th>
    </tr>
    {{ROWS — all market rows, typically 2–6}}
  </table>
```

| Column | Content |
|--------|---------|
| Market | `market_code` (e.g., "High Point April 2026") — format nicely from code |
| Date | `market_start_date` formatted as month/year |
| Customers | `customers_committing` |
| Items Committed | `total_committed_items` |
| Items Converted | `items_converted` |
| Conversion Rate | `item_conversion_pct` with `.badge.ok` if ≥ 70%, `.badge.warn` if 40–69%, `.badge.danger` if < 40% |
| Unrealized Items | `unrealized_items` — committed items with zero follow-through |

Show all market rows (no collapse unless > 6 rows).

After the table, include a `.callout.insight` summary:

```html
  <div class="callout insight">
    <div class="callout-title">Unrealized Pipeline</div>
    <p>Across all markets, {{TOTAL_UNREALIZED}} total items remain committed-but-not-ordered. These represent buying intent that was expressed but not yet fulfilled — ideal targets for rep follow-up.</p>
  </div>
```

**Part B — In-Stock Actionable Items (Q-58b)**

**Gate**: Render ONLY if `HAS_COMMITMENT_DATA = true` AND `HAS_INVENTORY = true` AND `cache/Q-58b_results.md` has data rows.

**Data source**: `cache/Q-58b_results.md`

**Rendering**: After the market conversion table, add a `.callout.opportunity` block titled "Immediate Action: Committed Items Currently In Stock". Open with: "These items were committed at market, never ordered, and are sitting in your warehouse right now — the shortest path from intent to revenue."

```html
  <div class="callout opportunity">
    <div class="callout-title">Immediate Action: Committed Items Currently In Stock</div>
    <p>These items were committed at market, never ordered, and are sitting in your warehouse right now — the shortest path from intent to revenue.</p>
  </div>
  <table>
    <tr>
      <th>Item</th>
      <th>Market</th>
      <th>Accounts</th>
      <th>Committed Qty</th>
      <th>In Stock</th>
      <th>Stock Value</th>
    </tr>
    {{ROWS — all in-stock actionable items}}
  </table>
  <p class="prose">Total actionable value: ${{TOTAL_STOCK_VALUE}} across {{ITEM_COUNT}} items.</p>
```

| Column | Content |
|--------|---------|
| Item | `item_description` (fall back to `item_number` if blank) |
| Market | `market_code` formatted as readable name |
| Accounts | `customers_committed` |
| Committed Qty | `total_committed_qty` |
| In Stock | `current_stock` |
| Stock Value | `stock_value` formatted as currency |

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{MARKET_COMMITMENT_NARRATIVE — Frame market conversion as pipeline visibility. Example: "Market commitments represent explicit buying intent captured at the point of enthusiasm. The X% conversion rate means Y items still have unrealized demand — these are warm leads that require re-engagement, not cold outreach." For Part B, emphasize zero-friction: "These items are already in your warehouse with committed buyers — they represent revenue waiting to be invoiced."}}
  </div>
</div>
```

**Claim rules**: Never expose `item_number` as raw internal code — use `item_description` in prose. Frame as the lowest-friction opportunity available. Never use "ERP." Use `.callout.opportunity` (green border) for Part B — NOT `.callout.success`.

---

### 12. First-Time Buyer Acquisition Trend (conditional)

**Gate**: `Q-41_results.md` has monthly new buyer counts spanning 6+ months.

**Data source**: `Q-41_results.md`

New eCat buyers per month with NAMED accounts and their growth trajectories. Aggregate counts alone are vanity metrics — the intelligence value is WHO the new buyers are and what they became.

**⚠ CRITICAL FRAMING**: "2-8 new buyers per month" without naming them is NOT intelligence. Every new buyer acquisition section MUST include named accounts showing their trajectory from first order to current state. If Q-41 includes account-level detail, use it. If it only has aggregates, supplement with data from Q-12 or Q-ORG-VELOCITY to identify specific accounts that first ordered within the reporting window and show their growth arc.

```html
<div class="subsection">
  <div class="subsection-title">New Buyer Acquisition & Growth</div>
  <div class="metrics-grid">
    <div class="metric-card">
      <div class="metric-val">{{AVG_MONTHLY_NEW_BUYERS}}</div>
      <div class="metric-label">Avg New Buyers / Month</div>
      <div class="metric-note">Trailing {{N}} months</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">{{TREND_DIRECTION}}</div>
      <div class="metric-label">Acquisition Trend</div>
      <div class="metric-note {{ok_or_warn}}>{{FIRST_HALF_VS_SECOND_HALF}}</div>
    </div>
    <div class="metric-card">
      <div class="metric-val">${{TOP_NEW_BUYER_GMV}}</div>
      <div class="metric-label">Best New Buyer (LTM)</div>
      <div class="metric-note">{{TOP_NEW_BUYER_NAME}}</div>
    </div>
  </div>
```

**Named Account Trajectories (MANDATORY when data available)**:

Show the top 5 new buyers by current LTM revenue with their growth trajectory from first order:

```html
  <div class="callout insight">
    <div class="callout-title">New Buyer Growth Stories</div>
    <p>Your strongest recent acquisitions aren't just new — they're growing. {{TOP_BUYER_NAME}} started with ${{FIRST_ORDER}} and has grown to ${{CURRENT_LTM}} in {{MONTHS}} months. These trajectories prove your acquisition funnel produces real, growing relationships.</p>
  </div>
  <table>
    <tr><th>Account</th><th>First Order</th><th>First Order Value</th><th>Current LTM Revenue</th><th>Growth</th><th>Orders (LTM)</th></tr>
    {{ROWS — top 5 new buyers by current LTM revenue, showing trajectory}}
  </table>
```

"Growth" column: Show as multiplier if meaningful (e.g., "12x first order") with `.badge.ok`. If account has only 1-2 orders, show "Early" with `.badge.muted`.

If declining (second-half average < first-half average by > 25%):

```html
  <div class="callout alert">
    <div class="callout-title">Acquisition Rate Declining</div>
    <p>New buyer acquisition dropped from {{FIRST_HALF_AVG}} per month ({{FIRST_HALF_PERIOD}}) to {{SECOND_HALF_AVG}} per month ({{SECOND_HALF_PERIOD}}). At this rate, natural attrition may outpace new buyer onboarding.</p>
  </div>
```

```html
  <div class="what-this-means">
    <strong>Action:</strong> {{ACQUISITION_NARRATIVE — MUST reference specific named accounts. Example: "Your acquisition funnel is producing winners: Graham's Lighting went from $53K first quarter to $100K LTM, and Royaume grew to $72K from a standing start. But the acquisition rate is declining — you're getting fewer shots on goal each month. The question isn't whether your new buyers grow (they do), it's whether you're finding enough of them."}}
  </div>
</div>
```

**Claim rules**: Frame declining acquisition as pipeline risk, not operational failure. Hedge attrition projections. ALWAYS name specific accounts — aggregate counts without names are filler, not intelligence. If account-level trajectory data is unavailable, state it explicitly: "Account-level trajectory data would show which new buyers are growing fastest — request customer-level first-order dates for the next cycle."

---

## Section-Level What-This-Means (MANDATORY)

After all subsections, one `.what-this-means` for the entire section. Max 3 sentences:

1. The most important commerce pattern insight (capture rate trajectory, channel shift, displacement signal, or AOV opportunity)
2. The dollar implication of the pattern continuing
3. (Optional) What additional data would enable (e.g., order_origin for precise channel attribution)

---

## Data Confidence Header (MANDATORY — ALWAYS AT TOP)

**⚠ ENFORCEMENT: If this header is missing from the rendered section, the fragment is DEFECTIVE. Do NOT skip it under any circumstances.**

> Follow `section_shared_contract.md` §2 for the confidence header process.

**Template selection** for `SECTION_CONFIDENCE_4`:

| Tier value | Template | Label |
|---|---|---|
| `FULL` | `§4-FULL` | `FULL PICTURE` |
| `STRONG` | `§4-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§4-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§4-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

**Variable resolution**: `{{LAST_PORTAL_ORDER_DATE}}` from enrichment preflight in `gate_flags.md`. If it can't be resolved for FULL or STRONG, fall back to `§4-PARTIAL`.

---

## Highlight File Output

> Follow `section_shared_contract.md` §4 for the highlight file format.

Save `cache/section_04_highlights.md` with 2–4 candidates from the strongest commerce signals. Deep-link: `[→ §commerce]`.

---

## Section-Specific Rules

**If `HAS_PORTAL_ORDERS = false`**: Commerce Patterns shows eCat-only data. Do not mention total business or all-channel anywhere in this section. Subsections 1 (Part B of Capture Rate), 9 (Competitive Displacement), and 10 (Price Erosion) are all skipped. Channel Migration (subsection 3) renders eCat channel split only without share-of-total overlay.

**Channel attribution statement** (required in section body when `HAS_CART = true`): "All eCat orders originate from one of two sources: iPad (rep-submitted) or eCat Online (buyer self-service)." Do not use code literals like `order_source = 'ipad'` in client-facing prose.

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Rep-level performance, coaching, or behavioral analysis → belongs in §5 Team Intelligence
2. Customer activation, dormancy, or buyer-level analysis → belongs in §2 Account Intelligence
3. Product catalog health, inventory status, or sales-line analysis → belongs in §3 Product Intelligence
4. Portal traffic or geographic demand → belongs in Demand Signal Intelligence
5. ~~Peer benchmarking or cohort comparisons~~ → **EXCLUDED from all reports** (data unreliable)
6. Platform feature utilization or data freshness → belongs in Platform & Feature
7. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md)

Read: `GUARDRAILS.md` for the full query ownership table and rule set.

---

## Conditional Subsection Checklist

| # | Subsection | Gate Condition | Action When Met | Action When Not Met |
|---|-----------|----------------|-----------------|---------------------|
| 1 | Digital Ordering Share | `HAS_PORTAL_ORDERS = true` | Render ordering share metrics + classification badge | Skip silently |
| 1+ | Ordering Share (VM45) | `VM45_RENDER = true` | Include ordering share calculation | Render total business context only (no share) |
| 2A | eCat Order Trend | Always | Render eCat-only trend table | — |
| 2B | eCat Share of Total Trend | `HAS_PORTAL_ORDERS = true` | Add total business + share columns to trend | Skip Part B silently |
| 3 | Channel Migration / Breakdown | `HAS_CART = true` OR 2+ channels with 6+ months | Render channel split table | Skip silently |
| 4 | Top Buyers (base) | Always | Render Q-13 top-10 table | — |
| 4+ | Top Buyers enrichment | `PORTAL_CUSTOMER_DATA_PRESENT = true` + `Q-52` has rows | Add "Total Business" + "eCat Share" columns | Render Q-13-only table |
| 5 | Quote Economics | 10+ quotes + confirmed orders exist | Render quote vs confirmed AOV spread | Skip silently |
| 6 | Order Type & Workflow | Always | Render quote premium callout + collapsed type table | — |
| 7 | Seasonal Timing | 12+ months of monthly data | Render seasonality table with intensity badges. `[COLLAPSE]` | Skip silently |
| 8 | AOV Spread by Rep | Spread > 2x between highest and lowest rep AOV | Render AOV spread callout + rep table | Skip silently (spread ≤ 2x is normal) |
| 9A | Category Displacement | `HAS_PORTAL_ORDERS = true` + `Q-55` has displacement rows | Render `.callout.insight` + displacement table. **MANDATORY.** | Skip silently |
| 9B | Rep Capture Trend | `PORTAL_REP_DATA_PRESENT = true` + `Q-56` has declining reps | Render rep decline table | Skip Part B silently |
| 10 | Price Erosion | `HAS_PORTAL_ORDERS = true` + `Q-60` has rows | Render `.callout.insight` + accounts table + `.callout.insight`. **MANDATORY.** | Skip silently |
| 11 | Market Commitment | `HAS_COMMITMENT_DATA = true` + `Q-58` has rows | Render market conversion table. **MANDATORY.** | Skip silently |
| 11B | In-Stock Actionable | `HAS_COMMITMENT_DATA = true` + `HAS_INVENTORY = true` + `Q-58b` has rows | Render `.callout.opportunity` + in-stock table | Skip Part B silently |
| 12 | First-Time Buyer Acquisition | 6+ months of monthly new buyer data | Render acquisition trend. Decline flagged if > 25% drop. `[COLLAPSE]` | Skip silently |
