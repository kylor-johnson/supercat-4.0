# Section 5 Context Bundle — Sarreid, Ltd. (fal)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Sarreid, Ltd. (fal, org_id=1)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=10907, portal_order_gmv=$15.6M |
| HAS_INVENTORY | True | inventory_count=5860 |
| HAS_SALES_DATA | True | sales_data_count=44746 |
| HAS_SALES_SECTION | True | qualifying_reps=12 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$15.6M > ecat_gmv=$2.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 12 | 12 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 65 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 604, Mixpanel total submit_order (Q-01): 3612 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=6.2%, ambiguous_rate=0.0%, showroom_event_share=100.0% |
| USER_GROUP_JOIN_RATE | 6% | 4 of 65 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 100% | showroom+admin share of matched events: 100.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Matthew Eatmon |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=39 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1370 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=112 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Sarreid, Ltd.
- **Shortname**: fal
- **Org ID**: 1
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Sarreid, Ltd. (fal, org_id=1)
- **Run date**: 2026-06-17

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | True |
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

## Section Guide — section_05_team.md

# Section Guide: Team Intelligence
> **v3.0** — signal-first architecture. Lean: only coaching interventions worth > $50K estimated upside.

## Section Identity

- **id**: `team`
- **title**: Team Intelligence
- **section number**: 5
- **include when**: `signal_rank.md` shows ≥ 1 P0/P1 signal with `Section Home = Team Intelligence`, OR 5+ active reps with orders
- **skip when**: < 5 active reps (insufficient team size for meaningful patterns)

## Query Inputs

Read these cache files:

- `cache/signal_rank.md` — ranked signal manifest
- `cache/coaching_candidates.md` — **deterministic coaching-card set + upside** (computed by detect_signals.py; the Coaching subsection renders exactly these reps — see subsection 3)
- `cache/Q-01_step1_results.md` — Mixpanel behavioral data (user events, presentations, engagement)
- `cache/Q-01_step2_results.md` — Mixpanel behavioral data (continued); also used as display-name cross-reference for username slugs returned by Q-63/64/65
- `cache/Q-05_results.md` — User analysis (roles, activity levels)
- `cache/Q-06_results.md` — Engagement trajectory (QoQ rep activity change)
- `cache/Q-18_results.md` — Order outcomes by rep (GMV, order count, AOV, customers)
- `cache/Q-43_results.md` — Territory/rep-to-customer mapping
- `cache/Q-51_results.md` — Rep eCat adoption vs. total business (**MANDATORY when gate met**: if `PORTAL_REP_DATA_PRESENT = true` in `gate_flags.md` AND this file contains data rows, subsection 1b MUST be rendered)
- `cache/Q-62_results.md` — Product launch velocity by rep `[COLLAPSE]` (conditional: render subsection 6 if `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND data rows exist)
- `cache/Q-63_results.md` — Presentation-to-order conversion (used in Presentation-to-Close subsection)
- `cache/Q-64_results.md` — Rep engagement vs account revenue `[COLLAPSE]` (conditional: render subsection 7 if `MIXPANEL_USER_DATA_PRESENT = true` AND `HAS_PORTAL_ORDERS = true` AND data rows exist)
- `cache/Q-65_results.md` — Selling vs admin time ratio (conditional: render subsection 8 if `MIXPANEL_USER_DATA_PRESENT = true` AND data rows exist AND spread >20pp)
- `cache/Q-70_results.md` — Inactive reps with territory revenue `[COLLAPSE]` (conditional: render subsection 9 if `HAS_PORTAL_ORDERS = true` AND `PORTAL_REP_DATA_PRESENT = true` AND data rows exist)
- `cache/gate_flags.md` — data availability gates (check `MIXPANEL_USER_DATA_PRESENT`, `PORTAL_REP_DATA_PRESENT`, `HAS_PORTAL_ORDERS`, `HAS_NEW_ITEMS`, `ADMIN_REPS_IN_LEADERBOARD`)
- `cache/showroom_scan_results.md` — Operational account exclusion evidence

Also read (for derivation rules only — not a cache file):
- `authority/query_library.md` — Q-02 and Q-03 sections contain the classification rules and funnel gap thresholds you apply to Q-01 Step 1 data when building subsections 2 and 3.

---

## MODE CHECK — Read `SALES_SECTION_MODE` in `gate_flags.md` FIRST

This section renders in one of two modes. Read `SALES_SECTION_MODE` from `gate_flags.md`:

- **`orders`** — the team has 5+ reps placing eCat orders. Build the section exactly as
  specified below (order-GMV leaderboard, etc.). This is the default.
- **`engagement`** — the team places few/no eCat orders yet (`order_reps` < 5) but has
  5+ reps actively *using the app* (`ENGAGEMENT_REP_COUNT` ≥ 5). eCat ordering is still
  ramping, so an order-GMV leaderboard would be empty and misleading. Build the section
  around **app selling-activity** instead, using these adjustments:

  1. **Rep Leaderboard** — rank by app activity from `Q-01_step1_results.md`, NOT order GMV.
     Use columns: `# · Rep · Days Active · Customer Selections (select_a_customer) ·
     Product Searches (search_products) · Presentations (create_pdf_catalog + email_item_info
     + share_my_list) · Total Events`. Sub-label: "Ranked by app selling activity (LTM)".
     Top 5 visible / collapsed middle / bottom 5, sorted by Total Events desc. Drop the
     Orders/GMV/AOV/Unique-Customers columns (they would be ~0).
  2. **Lead framing** — one sentence under the confidence header: this team is actively
     presenting and selling through the app while eCat ordering ramps; the view reflects
     engagement, not yet order volume. Do NOT imply reps aren't working.
  3. **Subsection 1b (Rep eCat Adoption)** — skip (no portal/order data).
  4. **Coaching Cards (subsection 3)** — still render exactly per `coaching_candidates.md`;
     if it lists 0 candidates, skip the subsection (engagement-mode orgs usually list 0).
  5. **Behavioral Archetypes (2), Presentation-to-Close (2b), Engagement Trajectory (4),
     Selling vs Admin Time (8)** — already built from Q-01 Step 1 / Q-06 / Q-63 / Q-65, so
     they render normally where their data/gates allow.
  6. Everything else (forbidden terms, what-this-means rules, thead/tbody, exemptions for
     the leaderboard + coaching cards) is unchanged.

---

## PRE-BUILD GATE CHECK — Complete Before Writing Any HTML

> Follow `section_shared_contract.md` §1 for the gate check process.

| Cache File | Gate Condition | If gate met + data rows exist → | Subsection |
|---|---|---|---|
| `Q-51_results.md` | `PORTAL_REP_DATA_PRESENT = true` | **MUST render** | 1b (Rep eCat Adoption vs Total Business) |
| `coaching_candidates.md` | file lists ≥1 candidate | **MUST render** (one card per listed rep); if 0 candidates, **skip the whole subsection** | 3 (Coaching Cards) |
| `Q-63_results.md` | `MIXPANEL_USER_DATA_PRESENT = true` | Used in subsection 2b (Presentation-to-Close) | 2b |
| `Q-64_results.md` | `MIXPANEL_USER_DATA_PRESENT = true` + `HAS_PORTAL_ORDERS = true` | Render inside `[COLLAPSE]` | 7 (Rep Engagement vs Revenue) |
| `Q-65_results.md` | `MIXPANEL_USER_DATA_PRESENT = true` + data rows + spread >20pp | **CONDITIONAL**: render when spread gate passes | 8 (Selling vs Admin Time) |
| `Q-70_results.md` | `HAS_PORTAL_ORDERS = true` + `PORTAL_REP_DATA_PRESENT = true` | Render inside `[COLLAPSE]` | 9 (Inactive Reps with Territory Revenue) |

---

## Fragment Structure

Uses the standard `<details class="section-collapse">` wrapper per shared_rules.md Section E.

```
Section ID: team
Section Number: §5
```

---

## CRITICAL REQUIREMENTS — Read Before Building

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **DEDUP**: The leaderboard table must have exactly ONE row per rep. Scan for duplicates after building.
2. **CONFIDENCE HEADER**: Every §5 fragment MUST contain a confidence header **at the top of the section** (immediately after the header metrics, before any subsection content). This is NOT optional — if the confidence header is missing, the fragment is defective. Read `SECTION_CONFIDENCE_5` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags.
3. **ADMIN DISCLOSURE**: If `ADMIN_REPS_IN_LEADERBOARD = true` in `gate_flags.md`, the admin disclosure text MUST appear in the confidence header. Do not skip it.
4. **ERP ENRICHMENT SUBSECTIONS**: Every row in the Pre-Build Gate Check table above where the gate is met AND the cache file has data rows MUST produce a rendered subsection. If you skip one, the fragment is defective.
5. **WHAT-THIS-MEANS QUALITY BAR**: Every `<div class="what-this-means">` block must read like a smart analyst talking to a VP — ground it in the specific numbers from this org's data and draw an actionable implication. Do not write data labels or restate the table header.
   - **FORBIDDEN**: Restating the top row of the table. The reader already read the table — your job is to tell them what it MEANS, not what it SAYS. If the what-this-means text could be derived by reading the first row of the table aloud, it is restating, not interpreting.
   - **BAD**: "This table shows your top 10 reps by GMV."
   - **BAD**: "Your top performer generates $765K in iPad orders across 131 customers." (This is literally reading the table back.)
   - **GOOD**: "The $485K gap between #1 and #10 suggests significant room to elevate mid-tier reps through coaching on customer targeting."
   - **GOOD**: "Your most active rep presented to 49 accounts but only 3.6% of presentations converted to orders — high effort, lower yield. Meanwhile, your most efficient closer converts at 26.8% with far fewer presentations, suggesting targeted demos outperform high-volume prospecting."
   - Every subsection except the **Rep Leaderboard** and **Coaching Cards** must end with exactly one `what-this-means` block that follows this quality bar. (The Rep Leaderboard is a pure ranking table — exempt per the gold standard; Coaching Cards are exempt per Section D.)

---

## Showroom / Operational Account Pre-Check

Stage 1 runs a two-pass scan before building the rep leaderboard. The section agent reads the pre-computed results from `cache/showroom_scan_results.md` — it does not re-run the scan.

**What the scan does (for interpretation):**
- **Pass 1 — keyword scan**: Flags rep names matching operational keywords (showroom, admin, marketing, training, test, demo).
- **Pass 2 — brand-name scan**: Catches patterns where the org's brand name appears in `rep_first_name` with a city or location in `rep_last_name` (e.g., "PALECEK SAN FRANCISCO"). These are missed by the keyword scan.

**How to use the pre-computed results:**
- **Include** flagged accounts in total org eCat GMV (these are real orders).
- **Exclude** from individual rep leaderboard and archetype analysis only when the scan confirmed corroborating evidence beyond the name pattern (e.g., city/location string in last name, no individual contact, shared-location account pattern). Name alone is insufficient.
- Accounts classified as "ambiguous — flagged for CSM review" remain in the leaderboard.
- The `showroom_scan_results.md` header states how many accounts were excluded and their aggregate GMV/order counts. Reference this in the `section-sub` one-liner if exclusions exist (e.g., "21 active reps · 1 showroom excluded · $4.65M iPad GMV").

---

## Content Blocks (render in NARRATIVE ARC order)

**Rendering order within this section (strength → opportunity → intelligence → risk):**
1. Rep Leaderboard (STRENGTH — celebrate the top, flag the bottom)
3. Coaching Cards (OPPORTUNITY — the VP action items, immediately after leaderboard)
1b. Rep eCat Adoption vs Total Business (INTELLIGENCE — compact metrics, not a table)
2. Behavioral Scorecard (INTELLIGENCE — how they sell)
2b. Presentation-to-Close Conversion (INTELLIGENCE + OPPORTUNITY)
4. Engagement Trajectory (INTELLIGENCE — lead with accelerating reps)
6. New Item Launch Velocity (INTELLIGENCE — collapsed)
7. Rep Engagement vs Account Revenue (INTELLIGENCE — collapsed)
8. Selling vs Admin Time (OPPORTUNITY)
5. Territory Coverage (OPPORTUNITY — collapsed)
9. Inactive Reps with Territory Revenue (OPPORTUNITY — collapsed, NOT risk)

### 0. Data Confidence Header (MANDATORY — ALWAYS AT TOP)

> Follow `section_shared_contract.md` §2 for the confidence header process.

Read `SECTION_CONFIDENCE_5` from `cache/section_confidence.md`.

| Tier | Template | Label |
|---|---|---|
| `FULL` | `§5-FULL` | `FULL PICTURE` |
| `STRONG` | `§5-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§5-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§5-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

Resolve template variables from `gate_flags.md`. If variables can't be resolved for FULL or STRONG, fall back to `§5-PARTIAL`.

If `ADMIN_REPS_IN_LEADERBOARD = true`, append the admin disclosure text to the confidence header div.

---

### 1. Rep Leaderboard (MANDATORY when 5+ active reps)

Source: `Q-18_results.md`. Show **top 5 by eCat GMV** (visible) and **bottom 5 by eCat GMV** (visible), with the middle collapsed.

> **ENGAGEMENT MODE** (`SALES_SECTION_MODE = engagement`): ignore the GMV instruction above. Source `Q-01_step1_results.md`, rank by **Total Events** (app activity), and use the engagement column set defined in the MODE CHECK block. Same top-5/collapsed-middle/bottom-5 structure. Still exempt from what-this-means.

**Dedup rule**: The leaderboard table must contain exactly ONE row per rep. If the same rep name appears in multiple source queries, merge their data into a single row — do not emit duplicate rows. After building the table, scan for duplicate `rep_name` values and collapse any repeats.

**Structure: Top 5 → collapsed middle → Bottom 5**

```html
<div class="subsection">
  <div class="subsection-title">Rep Leaderboard</div>
  <div class="sub-label">Ranked by eCat Sales LTM</div>
  <table>
    <tr><th>#</th><th>Rep</th><th>Orders (LTM)</th><th>GMV (LTM)</th><th>AOV</th><th>Unique Customers</th></tr>
    {{TOP 5 ROWS — always visible, numbered 1-5}}
  </table>
  <details>
    <summary>{{N}} additional reps · combined ${{MIDDLE_GMV}} GMV</summary>
    <table>
      <tr><th>#</th><th>Rep</th><th>Orders (LTM)</th><th>GMV (LTM)</th><th>AOV</th><th>Unique Customers</th></tr>
      {{MIDDLE ROWS — reps 6 through N-5, sorted by GMV desc}}
    </table>
  </details>
  <div class="sub-label" style="margin-top:16px;">Bottom 5 by eCat GMV</div>
  <table>
    <tr><th>#</th><th>Rep</th><th>Orders (LTM)</th><th>GMV (LTM)</th><th>AOV</th><th>Unique Customers</th></tr>
    {{BOTTOM 5 ROWS — always visible, numbered from bottom}}
  </table>
```

The VP sees who's winning (top 5) and who needs attention (bottom 5). The middle is available but doesn't dominate the view.

**NO `what-this-means` block on the Rep Leaderboard.** Per the gold standard, pure
ranking tables are self-explanatory and are exempt from the per-subsection
`what-this-means` requirement. Do NOT append one here. The performance-shape
interpretation (concentration, AOV spread, archetype split) belongs in the
**section-level `what-this-means`** at the end of §5 — fold it in there.

When writing that section-level interpretation, answer these specific questions from the data:

- **Concentration**: Does the top rep generate > 30% of total GMV? (If yes, SIG-RISK-04 likely fired — reference it.)
- **AOV spread**: Is the gap between highest and lowest AOV > 2x? (Signals different selling behaviors.)
- **Volume vs precision**: Are there high-order-count / low-AOV reps vs low-order-count / high-AOV reps? (Signals selling archetype differences.)
- **eCat-only leaderboard**: This leaderboard shows reps ranked by eCat GMV specifically (not total business). If the org has reps who are top sellers in total business but absent from this leaderboard (zero eCat orders), address this explicitly: "This shows your eCat-active team. [N] additional reps manage $X in total business but have not yet adopted the platform — their onboarding is covered in subsection 1b below."

**ADMIN DISCLOSURE CHECK (do this immediately after building the leaderboard table):** Read `ADMIN_REPS_IN_LEADERBOARD` from `gate_flags.md`. If `true`, you MUST include the admin disclosure text in the confidence header at the top of this section. Do not forget or defer — flag it now, render it in the header block.

---

### 1b. Rep eCat Adoption vs Total Business (Q-51)

**MANDATORY RENDER**: If `cache/Q-51_results.md` exists AND contains data rows AND `PORTAL_REP_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-51_results.md`

**Rendering**: 4 metric cards + a focused enablement callout. Do NOT render a full roster table — this is a summary view, not a second leaderboard.

**FRAMING (matches §4's thesis):** This is **digital enablement, not an eCat adoption quota.** Reps whose
books run off eCat aren't "failing to capture" — their orders flow through the client's own web, EDI,
phone, email, and back-office entry. The opportunity is streamlining the **rep-assisted / manually-keyed**
portion into digital ordering (eCat for rep-assisted/field orders). Never frame this as "get reps to
use the app more" or a "capture-rate gap."

```html
<div class="subsection">
  <div class="subsection-title">How Reps' Orders Come In</div>
  <div class="metrics">
    <div class="metric-card">
      <div class="metric-value">{{OVERALL_CAPTURE_PCT}}%</div>
      <div class="metric-label">eCat Share of Team Business</div>
      <div class="metric-note">${{ECAT_GMV}} of ${{TOTAL_BIZ_GMV}} (rest via web/EDI/rep entry)</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">{{TOP_QUARTILE_PCT}}%</div>
      <div class="metric-label">Top Quartile (eCat)</div>
      <div class="metric-note">{{TOP_Q_COUNT}} reps avg</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">{{BOTTOM_QUARTILE_PCT}}%</div>
      <div class="metric-label">Bottom Quartile (eCat)</div>
      <div class="metric-note">{{BOTTOM_Q_COUNT}} reps avg</div>
    </div>
    <div class="metric-card">
      <div class="metric-value">{{GAP_MULTIPLIER}}×</div>
      <div class="metric-label">Top-to-Bottom Range</div>
      <div class="metric-note">how reps differ in eCat use</div>
    </div>
  </div>
  <div class="callout action">
    <div class="callout-title">Reps Whose Books Run Off eCat — Enablement Opportunity</div>
    <p>{{N_ZERO_CAPTURE}} reps move ${{ZERO_CAPTURE_GMV}} of combined business entirely through other channels (their own web, EDI, phone/email, rep entry). The rep-assisted portion of that is where eCat can cut manual order-entry time and errors:</p>
    <ol>
      <li><strong>{{REP_1}}</strong> — ${{REP_1_GMV}} total business, none yet through eCat</li>
      <li><strong>{{REP_2}}</strong> — ${{REP_2_GMV}} total business, none yet through eCat</li>
      <li><strong>{{REP_3}}</strong> — ${{REP_3_GMV}} total business, none yet through eCat</li>
      <li><strong>{{REP_4}}</strong> — ${{REP_4_GMV}} total business, none yet through eCat</li>
      <li><strong>{{REP_5}}</strong> — ${{REP_5_GMV}} total business, none yet through eCat</li>
    </ol>
  </div>
  <div class="what-this-means">
    <strong>Action:</strong> {{ENABLEMENT_NARRATIVE — specific to org. Frame as reducing manual/phone/email order entry for the rep-assisted portion of these books, NOT "get reps to adopt the app." Name a specific rep + dollar figure. Acknowledge much of their volume may legitimately belong on the client's own web/EDI and should stay there.}}
  </div>
</div>
```

If fewer than 5 reps run entirely off eCat, show only those that do. If none do, replace the enablement callout with a "lowest eCat use" callout showing the 5 reps with the lowest eCat share.

**Claim rules**: Digital enablement, NOT adoption. Never use "capture rate," "activation target," "untapped," or "adoption gap." Never imply a rep's off-eCat business is manual/offline as a certainty — name it "other channels." Never expose `rep_number`. Never say "ERP" — use "total business"/"all-channel sales." Never say "platform" standalone — use "eCat" or "the app."

---

### 2. Behavioral Scorecard Spotlight (Q-01 + Q-03 derivation)

**Gate**: `MIXPANEL_USER_DATA_PRESENT = true` (check `gate_flags.md`)

Apply the Q-03 funnel gap analysis rules from `authority/query_library.md` to Q-01 Step 1 behavioral data. **Scope**: only classify the top 20 reps by iPad GMV from Q-01 Step 2 — do not process the full Q-01 Step 1 dataset. For each of those reps with `submit_order > 5`, compute the dimensional ratios and identify funnel gaps. Use the results to spotlight reps with notable behavioral patterns — high browse but low submission, strong configuration activity, or engagement trajectory divergence.

**Archetype identification**: Using the Q-03 derivation rules, classify each qualifying rep into one of these behavioral patterns:

| Archetype | Pattern | Badge Class |
|-----------|---------|-------------|
| High Activity / Low Presentation | Above-median total events but below-median customer-facing presentations (catalogs, emails, shares) | `.badge.warn` |
| Discovery-Driven Closer | High search/browse ratio relative to presentations; above-median conversion rate | `.badge.ok` |
| Order-Direct Pattern | Low presentation + low browse but consistent submit_order activity — rep uses eCat purely for order entry | `.badge.info` |
| Volume Relationship Seller | High customer count, high order count, below-median AOV — breadth over depth | `.badge.muted` |
| Precision Closer | Low customer count, low order count, above-median AOV — depth over breadth | `.badge.ok` |

```html
<div class="subsection">
  <div class="subsection-title">Behavioral Archetypes</div>
  <div class="callout insight">
    <div class="callout-title">{{N}} distinct selling patterns identified across your top performers</div>
    <p>Your reps' eCat usage data shows how they actually use the app — not just what they sell, but how they sell. {{N_HIGH_ACTIVITY_LOW_CLOSE}} reps show high app activity with below-peer conversion, suggesting engagement without follow-through. {{N_ORDER_DIRECT}} reps use eCat exclusively for order entry, bypassing its presentation capabilities entirely.</p>
  </div>
  <table>
    <tr><th>Rep</th><th>Archetype</th><th>Total Events</th><th>Presentations</th><th>Orders</th><th>Conversion</th><th>Key Gap</th></tr>
    {{ROWS — top 20 reps by GMV with archetype badge and primary funnel gap}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> {{ARCHETYPE_NARRATIVE — specific to data. E.g., "Your team splits into two dominant patterns: 4 reps operate as high-volume relationship sellers (averaging 89 customers each at $X AOV) while 3 operate as precision closers (averaging 12 customers at $Y AOV). Neither is wrong, but the Order-Direct pattern — 3 reps who never present, only submit — represents untapped engagement. If those reps used even basic presentation workflows, peer conversion data suggests a $Z annual upside."}}
  </div>
</div>
```

**Mixpanel Order-Tracking Gap**: If `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md`, Mixpanel is not tracking iPad order submissions for this org (all users show `submit_order = 0` despite real Postgres orders). When this flag is true:
- Q-03 funnel gap analysis should skip the "Presentation → Orders" ratio — it will be zero for all reps regardless of actual behavior.
- Fall back to Postgres `total_orders` from Q-01 Step 2 as the qualifying signal instead of `submit_order > 5`.
- Do NOT state that reps have "zero ordering activity" — that contradicts Postgres order data.

---

### 2b. Presentation-to-Close Conversion (conditional: SIG-BEH-01 fired OR Q-63 data available)

**Gate**: `Q-01` behavioral data present AND `Q-18` order data present AND (SIG-BEH-01 fired for at least 1 rep OR `cache/Q-63_results.md` has data rows).

**Data source**: `cache/Q-63_results.md` (preferred, higher fidelity) — fall back to Q-01 Step 1 behavioral data cross-referenced with Q-18 if Q-63 unavailable.

**Data shape (Q-63)**: `rep` (username slug — NOT a display name), `accounts_engaged`, `total_presentations`, `total_orders`, `order_rate_pct`, `conversion_rate_pct`, `total_searches`, `total_catalogs`, `total_emails`.

**Username → Display Name**: The `rep` column in Q-63 contains eCat usernames, not display names. Cross-reference against `Q-01_step2_results.md` rep names for display-name mapping. If no match is found, use anonymized labels ("Rep A", "Rep B"). Never render raw usernames (e.g., "staciebaker") in client-facing output.

**Showroom Exclusion**: Showroom/operational accounts may appear in Q-63 data. Apply the same exclusion logic as the showroom pre-check: exclude from the table, do not count in summary statistics.

Reps with high presentation activity (email_item_info, create_pdf_catalog, share_my_list) but low order conversion. **Only reps with 50+ presentations qualify.**

```html
<div class="subsection">
  <div class="subsection-title">Presentation-to-Close Conversion</div>
  <div class="callout insight">
    <div class="callout-title">{{N}} reps with significant presentation activity but below-peer conversion</div>
    <p>{{DATA_GROUNDED_HEADLINE — E.g., "Your most active rep presented to 49 accounts but only 3.6% of customer-facing presentations converted to orders. Meanwhile, your most efficient closer converts at 26.8% with targeted presentations — fewer demos, better outcomes."}}</p>
  </div>
  <table>
    <tr><th>Rep</th><th>Accounts Engaged</th><th>Presentations</th><th>Orders</th><th>Conversion Rate</th><th>Team Median</th><th>Estimated Upside</th></tr>
    {{ROWS — only reps with 50+ presentations, sorted by total_presentations desc}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> {{CONVERSION_SPREAD_NARRATIVE — specific to org's conversion range. Ground the insight in the actual spread between highest and lowest conversion reps. E.g., "The 23pp gap between your best and worst converters isn't a talent problem — it's a workflow problem. High-activity/low-conversion reps are doing the hard part (customer engagement) without the closing step. A post-presentation follow-up cadence closes this gap faster than any new lead source."}}
  </div>
</div>
```

"Estimated Upside" column: `(team_median_conversion - rep_conversion) × rep_presentations × rep_aov`. Hedge with "estimated" language. Format as dollar amount.

**Claim rules**: Never render raw usernames in client-facing output. Never expose `selected_bill_to_code` or event-name literals. Say "customer-facing presentations" not "product_search events." Say "eCat usage data" not "Mixpanel" or "platform engagement data." Frame low conversion constructively as coaching opportunity.

---

### 3. Coaching Cards (rep set + upside come from `cache/coaching_candidates.md`)

**The rep set and the dollar figures are NOT yours to compute.** `detect_signals.py`
already computed them deterministically (top-quartile-conversion benchmark, $50K
upside floor, reps without order/AOV data excluded) and wrote
`cache/coaching_candidates.md`. Your job is to render exactly what that file lists
and to write the archetype framing + coaching narrative for each. Do NOT recompute
upside, re-derive the benchmark, change the threshold, or add/drop reps.

**RENDER GATE — read `cache/coaching_candidates.md` first:**
- If it lists **0 candidates** (the "No coaching cards for this client" line),
  render **NO** coaching subsection at all — no rollup callout, no cards. Skip it
  entirely. Do NOT fabricate coaching upside to fill the section. (This is correct
  behavior for low-AOV orgs — the section earns its place only when the data does.)
- If it lists **≥1 candidate**, render the subsection with one `.coaching-card`
  per listed rep, in the file's order, using the file's exact upside figures.

**Archetype classification** (for cards that render): Apply the Q-02 archetype
rules from `authority/query_library.md` to each candidate's Q-01 Step 1 behavioral
data to pick the badge + narrative. This is framing only — it does not change which
reps render or their upside.

**Subsection wrapper**: All coaching content (rollup callout + every coaching card)
lives inside ONE `<div class="subsection">` whose title is exactly
**"Coaching Opportunities"**. Open it before the rollup and close it after the last
card. Do not invent a different title ("Coaching Cards", "Coaching Interventions",
etc.).

**Step 1 — Team-level coaching rollup**: Render a `.callout.opportunity` using the
file's **Combined upside** value (sum of the listed candidates — do not recompute):

```html
<div class="subsection">
  <div class="subsection-title">Coaching Opportunities</div>
  <div class="callout opportunity">
    <div class="callout-title">Combined coaching upside across {{N}} priority reps: ${{TOTAL_UPSIDE}} in potential annual incremental GMV</div>
    <p>That's {{PCT}}% of your current eCat sales from coaching alone — with zero new customer acquisition required.</p>
  </div>
  <!-- coaching cards follow, then close this </div> -->
```

`{{N}}`, `{{TOTAL_UPSIDE}}` come straight from `coaching_candidates.md`. Use
hedging language ("potential," "estimated") in client-facing HTML.

**Step 2 — Individual coaching cards**: One `.coaching-card` per rep listed in
`coaching_candidates.md` (already filtered, sorted by upside desc, capped at 5).
Use the file's `Estimated Annual Upside` value verbatim for `coaching-impact`:

```html
<div class="coaching-card">
  <div class="coaching-header">
    <div class="coaching-name">{{REP_NAME}}</div>
    <span class="badge {{ARCHETYPE_COLOR}}">{{ARCHETYPE}}</span>
  </div>
  <div class="coaching-body">
    <p>{{BEHAVIORAL_PATTERN_DESCRIPTION — tailored to the archetype. A Volume Relationship Seller needs AOV support, not breadth training; a Precision Closer needs frequency incentives, not configuration coaching.}}</p>
    <div class="coaching-action"><strong>Coaching action:</strong> {{SPECIFIC_ACTION — must be actionable this week by a sales manager}}</div>
    <div class="coaching-impact">${{ESTIMATED_IMPACT}} estimated annual upside</div>
  </div>
</div>
```

**Archetype badges** (assign based on data pattern — these merge archetype classification INTO coaching cards rather than a separate table):
- **High Activity / Low Close**: `.badge.warn` — Rep with above-median presentations but below-median conversion
- **Discovery-Driven Closer**: `.badge.ok` — High search/browse, above-median conversion
- **Order-Direct Pattern**: `.badge.info` — Low presentation, consistent order entry
- **Volume Relationship Seller**: `.badge.muted` — High order count, low AOV, high customer count
- **Precision Closer**: `.badge.ok` — Low customer count, high AOV
- **Declining Engagement**: `.badge.danger` — Rep with QoQ activity decline > 25%
- **Narrow Account Base**: `.badge.info` — Above-median GMV but fewer than median unique customers

**Rules:**
- Render exactly the reps in `coaching_candidates.md` — the file is already
  capped at 5 and sorted by upside descending. Do not add, drop, or reorder.
- Use the file's upside figures verbatim. Never invent a dollar figure.
- Coaching cards do NOT get a `.what-this-means` close (per shared_rules.md Section D exception)
- Every coaching action must be specific enough for a sales manager to act on this week
- Every coaching action names a specific rep and specific behavior — no generic "improve performance"
- The archetype badge provides the "why" framing; the coaching action provides the "what to do"

---

### 4. Engagement Trajectory (conditional: Q-06 data available with 6+ months history)

**Gate**: `Q-06_results.md` has QoQ engagement change data for active reps.

Top 5 accelerating reps and top 5 declining reps with QoQ order change and current GMV.

```html
<div class="subsection">
  <div class="subsection-title">Engagement Trajectory</div>

  <div class="callout opportunity">
    <div class="callout-title">Accelerating Reps</div>
  </div>
  <table>
    <tr><th>Rep</th><th>Prior 90d Orders</th><th>Current 90d Orders</th><th>QoQ Change</th><th>Current GMV (LTM)</th></tr>
    {{TOP 5 ACCELERATING REPS}}
  </table>

  <div class="callout insight">
    <div class="callout-title">Reps Needing Attention</div>
  </div>
  <table>
    <tr><th>Rep</th><th>Prior 90d Orders</th><th>Current 90d Orders</th><th>QoQ Change</th><th>Current GMV (LTM)</th></tr>
    {{TOP 5 DECLINING REPS — only those with SIG-DECAY-03 or meaningful decline}}
  </table>

  <div class="what-this-means">
    <strong>Action:</strong> {{TRAJECTORY_NARRATIVE — focused on who needs immediate attention. E.g., "[REP_A] declined 40% QoQ and manages $X in annual accounts — a conversation now prevents a customer relationship gap from forming. [REP_B]'s acceleration is the kind of momentum to protect with recognition and expanded territory."}}
  </div>
</div>
```

QoQ Change: `.badge.ok` for positive, `.badge.warn` for -1% to -25%, `.badge.danger` for < -25%.

---

### 5. Territory Coverage (conditional: territory data + dormant territory value)

**Gate**: `Q-43_results.md` has territory/rep assignment data AND accounts exist that are assigned to reps but have never ordered via eCat.

```html
<div class="subsection">
  <div class="subsection-title">Territory Coverage Gaps</div>
  <div class="callout insight">
    <div class="callout-title">{{N}} assigned accounts with zero eCat orders</div>
    <p>{{N}} accounts are assigned to your reps' territories but have never placed an order through eCat. {{IF portal_orders available: "Combined total-business value of dormant territory accounts: ${{DORMANT_VALUE}} (trailing 12 months)."}}</p>
  </div>
  <table>
    <tr><th>Rep</th><th>Assigned Accounts</th><th>Active Accounts</th><th>Coverage %</th><th>Dormant Account Value</th></tr>
    {{ROWS — sorted by dormant value desc, top 5 visible, rest in <details>}}
  </table>
  <div class="what-this-means">
    <strong>Action:</strong> Territory coverage gaps are the lowest-friction growth opportunity — these are accounts already assigned to reps, often with existing business relationships through other channels. The gap between assignment and activation is the conversion target.
  </div>
</div>
```

"Dormant Account Value" column: only populated if `portal_orders` available. Otherwise show "—" and note in callout that total-business data would quantify the opportunity. `[COLLAPSE]`

---

### 6. New Item Launch Velocity by Rep (Q-62) `[COLLAPSE]`

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND `cache/Q-62_results.md` has data rows.

**Disposition**: Good data but secondary to archetypes — section overload risk. Wrap in an inner `<details>` per shared_rules §I.

**Data source**: `cache/Q-62_results.md`

**Data shape**: `rep_name` (display name, ALL-CAPS — title-case before rendering), `new_items_sold`, `total_new_items`, `adoption_pct`, `customers_buying_new`, `new_item_qty`, `new_item_revenue`, `orders_with_new_items`.

**Rendering**: Open with a `.callout.insight` titled "New Item Adoption by Rep" summarizing: "Your catalog has X new introductions. Your top seller has placed orders for Y of them (Z% adoption). The bottom quartile has sold fewer than W."

```html
<details class="inner-collapse">
  <summary>New Item Launch Velocity &#9662;</summary>
  <div class="subsection">
    <div class="subsection-title">New Item Launch Velocity by Rep</div>
    <div class="callout insight">
      <div class="callout-title">New Item Adoption by Rep</div>
      <p>Your catalog has {{TOTAL_NEW_ITEMS}} new introductions. Your top seller has placed orders for {{MAX_NEW_SOLD}} of them ({{MAX_ADOPTION_PCT}}% adoption). The bottom quartile has sold fewer than {{BOTTOM_QUARTILE_COUNT}}.</p>
    </div>
    <table>
      <tr><th>Rep</th><th>New Items Sold</th><th>Adoption %</th><th>Customers</th><th>Revenue</th></tr>
      {{TOP 10 ROWS — sorted by adoption_pct desc}}
    </table>
    <details>
      <summary>All remaining reps ({{N}}) &#9662;</summary>
      <table>
        {{REMAINING REP ROWS}}
      </table>
    </details>
    <div class="what-this-means">
      <strong>Action:</strong> {{NEW_ITEM_NARRATIVE — specific to org data. Ground in the adoption spread and its revenue implications. E.g., "Your top adopter has sold 34 of 52 new introductions generating $X in new-item revenue. Your bottom 5 reps have collectively sold 3 new items. New product launches only work when the field sells them — this spread identifies who needs product training vs who can champion new introductions."}}
    </div>
  </div>
</details>
```

Badge rules for Adoption %: `.badge.ok` if ≥30%, `.badge.warn` if 15–29%, `.badge.danger` if <15%.

**Claim rules**: Never name individual reps by real name in the callout insight — use "your top performer" / "bottom quartile" language. Table rows may use title-cased rep names. Never expose internal codes. Frame as coaching opportunity, not judgment.

---

### 7. Rep Engagement vs Account Revenue (Q-64) `[COLLAPSE]`

**Gate**: Render ONLY if `MIXPANEL_USER_DATA_PRESENT = true` AND `HAS_PORTAL_ORDERS = true` AND `cache/Q-64_results.md` has data rows.

**Disposition**: Useful engagement-depth view but secondary to conversion efficiency. Wrap in an inner `<details>` per shared_rules §I to avoid section overload.

**Data source**: `cache/Q-64_results.md`

**Data shape**: `rep` (username slug — same cross-ref rules as Q-63), `accounts_touched`, `avg_touches_per_account`, `avg_days_per_account`, `high_engagement_accounts` (8+ touches), `low_engagement_accounts` (<3 touches). Note: this query does not include revenue columns — do not fabricate revenue data. The "vs Account Revenue" framing comes from correlating engagement depth with order data from Q-01 Step 2.

**Username → Display Name**: Cross-reference `Q-01_step2_results.md` for display names. Never render raw usernames or email addresses.

**Showroom Exclusion**: Showroom accounts may appear (e.g., usernames containing "showroom", city/location patterns). Exclude from the table and summary statistics.

```html
<details class="inner-collapse">
  <summary>Rep Engagement vs Account Revenue &#9662;</summary>
  <div class="subsection">
    <div class="subsection-title">Engagement Depth by Rep</div>
    <div class="callout insight">
      <div class="callout-title">Engagement Distribution</div>
      <p>{{X}} accounts receive 8+ eCat interactions (high engagement). {{Y}} accounts receive fewer than 3 (under-served). Your most engaged rep averages {{Z}} interactions per account across {{N}} accounts.</p>
    </div>
    <table>
      <tr><th>Rep</th><th>Accounts Touched</th><th>Avg Touches/Acct</th><th>High Engagement</th><th>Low Engagement</th></tr>
      {{TOP 10 ROWS — sorted by accounts_touched desc}}
    </table>
    <details>
      <summary>All remaining reps ({{N}}) &#9662;</summary>
      <table>
        {{REMAINING REP ROWS}}
      </table>
    </details>
    <div class="what-this-means">
      <strong>Action:</strong> {{ENGAGEMENT_NARRATIVE — specific to org's engagement spread. E.g., "The rep averaging 14.2 touches per account generates $X per account in annual orders. The rep averaging 2.1 touches generates $Y. Engagement depth correlates with revenue per account — reps with more frequent customer contact capture more wallet share. The gap between your deepest and shallowest engagers suggests $Z in addressable revenue from increased touch frequency."}}
    </div>
  </div>
</details>
```

**Claim rules**: Always use "correlate" not "cause." Never render raw usernames. Never expose customer codes. Say "app usage data" not "Mixpanel." Frame under-engagement as opportunity, not failure.

---

### 8. Selling vs Admin Time (Q-65)

**Gate**: Render ONLY if ALL of the following are true:
1. `MIXPANEL_USER_DATA_PRESENT = true`
2. `cache/Q-65_results.md` has data rows
3. **Spread gate**: The difference between the highest and lowest `selling_pct` values across qualifying reps exceeds 20 percentage points (e.g., if the range is 74%–89%, the 15pp spread fails this gate — skip silently). If the spread is ≤20pp, the data does not surface a meaningful coaching differentiation and the subsection adds length without insight.

**Data source**: `cache/Q-65_results.md`

**Data shape**: `rep` (username slug — same cross-ref rules as Q-63), `total_events`, `selling_events`, `admin_events`, `selling_pct`, `admin_pct`. Note: some orgs may have duplicate user identifiers (e.g., "alexsislopez" and "alexsislopez@gmail.com" for the same person). Merge rows with matching base usernames before rendering — sum events, recompute percentages.

**Username → Display Name**: Cross-reference `Q-01_step2_results.md` for display names. Never render raw usernames or email addresses.

**Showroom Exclusion**: Showroom accounts may appear (e.g., "ccdallasshowroom"). Exclude from the table and summary statistics — their selling/admin ratios reflect operational patterns, not rep behavior.

```html
<div class="subsection">
  <div class="subsection-title">How Reps Spend Their Time in the App</div>
  <div class="callout insight">
    <div class="callout-title">Platform Time Allocation</div>
    <p>Your top performers spend {{MAX_SELLING_PCT}}% of platform time on customer-facing activities vs. {{MAX_ADMIN_PCT_COMPLEMENT}}% administration. The bottom quartile averages {{BOTTOM_Q_SELLING_PCT}}% — a {{SPREAD}}pp gap that correlates with significantly lower order volume.</p>
  </div>
  <table>
    <tr><th>Rep</th><th>Total Activity</th><th>Selling</th><th>Admin</th><th>Selling %</th></tr>
    {{TOP 10 ROWS — sorted by selling_pct desc (most efficient sellers first)}}
  </table>
  <details>
    <summary>All remaining reps ({{N}}) &#9662;</summary>
    <table>
      {{REMAINING REP ROWS}}
    </table>
  </details>
  <div class="what-this-means">
    <strong>Action:</strong> {{SELLING_ADMIN_NARRATIVE — specific to org's actual spread. E.g., "A 28pp gap between your most and least efficient sellers means your bottom-quartile reps spend nearly half their platform time on administrative tasks. That's not laziness — it's a process problem. Reps who spend more time on admin typically lack templates, saved lists, or established workflows. A 30-minute workflow training session for your bottom 3 reps would shift an estimated $X in annual productivity toward customer-facing activity."}}
  </div>
</div>
```

Badge rules for Selling %: `.badge.ok` if ≥70%, `.badge.warn` if 50–69%, `.badge.danger` if <50%.

**Claim rules**: Never render raw usernames or email addresses. Never use event_name literals in prose — say "customer-facing activities" and "administrative tasks." Say "app usage data" not "Mixpanel." Frame as process improvement opportunity, not individual failure. Always hedge correlations ("correlates with," not "causes").

---

### 9. Inactive Reps with Territory Revenue (Q-70) `[COLLAPSE]`

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `PORTAL_REP_DATA_PRESENT = true` AND `cache/Q-70_results.md` exists AND contains data rows.

**Data source**: `cache/Q-70_results.md`

**Rendering**: Open with a `.callout.alert` titled "Platform Adoption Gap: Active Sellers, Offline Workflow" summarizing: "X reps with $Y in combined territory revenue haven't used the platform in 90+ days. These aren't inactive territories — they're active sellers managing their business entirely offline."

```html
<details class="inner-collapse">
  <summary>Inactive Reps with Territory Revenue &#9662;</summary>
  <div class="subsection">
    <div class="subsection-title">Platform Adoption Gap</div>
    <div class="callout alert">
      <div class="callout-title">Active Sellers, Offline Workflow</div>
      <p>{{N}} reps with ${{COMBINED_TERRITORY_GMV}} in combined territory revenue haven't used the platform in 90+ days. These aren't inactive territories — they're active sellers managing their business entirely offline.</p>
    </div>
    <table>
      <tr><th>Rep</th><th>Last Active</th><th>Territory Orders (LTM)</th><th>Territory GMV (LTM)</th></tr>
      {{TOP 5 ROWS — sorted by territory GMV desc (highest-value inactive reps first)}}
    </table>
    <details>
      <summary>All remaining inactive reps ({{N}}) &#9662;</summary>
      <table>
        {{REMAINING ROWS}}
      </table>
    </details>
    <div class="what-this-means">
      <strong>Action:</strong> {{INACTIVE_REP_NARRATIVE — specific to org. E.g., "These reps are actively selling but not using the platform — their customer relationships are strong, but every order flows through phone, email, or manual processes. Re-engaging even 2 of these reps would add an estimated $X in platform-attributed revenue with zero new customer acquisition. The conversation isn't 'start using the app' — it's 'your peers are closing faster because they use the app.'"}}
    </div>
  </div>
</details>
```

"Last Active" column: Format as "X days ago" or "Last active [month]" — never expose raw timestamps or login dates.

**Claim rules**: Frame as activation opportunity, not performance criticism. Never say "these reps are failing" — say "these sellers manage their business offline." Never expose user IDs, login timestamps, or internal role codes. Use "haven't used the platform" not "haven't logged in" in client-facing prose.

---

## Section-Level What-This-Means (MANDATORY)

After all subsections, one `.what-this-means` for the entire section. Max 3 sentences:

1. The highest-ROI coaching or team intervention available
2. The dollar concentration risk if the top rep disengages
3. (Optional) What additional behavioral data would enable

---

## Highlight File Output

> Follow `section_shared_contract.md` §4 for the highlight file format.

Save `cache/section_05_highlights.md` with 2–4 candidate highlights from the strongest team/behavioral signals.

---

## Section-Specific Rules

- **Clamp**: Do not carry specific rep names, GMV figures, or archetypes from prior reports. Every generation is fresh from current query data.
- Do not surface showroom exclusion methodology, qualifying-threshold explanations, or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference the exclusion count (e.g., "21 active reps · 1 showroom excluded · $4.65M platform GMV") but not the methodology or threshold logic.
- See `shared_rules.md` and `section_shared_contract.md` §6 for the complete terminology and forbidden terms rules.
- **Username handling in Q-63/64/65**: These queries return platform usernames (slugs), not display names. Always cross-reference `Q-01_step2_results.md` to resolve to display names. Never render raw usernames or email addresses.

---

## Conditional Subsection Checklist

### Subsection Registry

| # | Subsection | Query | Gate(s) | Status | Collapse? |
|---|-----------|-------|---------|--------|-----------|
| 1 | Rep Leaderboard | Q-18 | 5+ active reps | **Always rendered** (section gate) | Partial (top 5 visible, 6-10 collapsed, rest collapsed) |
| 1b | Rep eCat Adoption vs Total Business | Q-51 | `PORTAL_REP_DATA_PRESENT = true` + data rows | **MANDATORY** when gate met | No |
| 2 | Behavioral Scorecard Spotlight | Q-01 + Q-03 derivation | `MIXPANEL_USER_DATA_PRESENT = true` | Conditional | No |
| 2b | Presentation-to-Close Conversion | Q-63 (or Q-01 + Q-18 fallback) | Behavioral data + order data + (SIG-BEH-01 or Q-63 rows) | Conditional | No |
| 3 | Coaching Opportunities | `coaching_candidates.md` (deterministic) | file lists ≥1 candidate | **MANDATORY** when ≥1 candidate; skip entirely when 0 (no `what-this-means`) | No |
| 4 | Engagement Trajectory | Q-06 | QoQ data with 6+ months history | Conditional | No |
| 5 | Territory Coverage | Q-43 | Territory data + dormant accounts | Conditional | **Yes** `[COLLAPSE]` |
| 6 | New Item Launch Velocity | Q-62 | `HAS_PORTAL_ORDERS = true` + `HAS_NEW_ITEMS = true` + data rows | Conditional | **Yes** `[COLLAPSE]` |
| 7 | Rep Engagement vs Account Revenue | Q-64 | `MIXPANEL_USER_DATA_PRESENT = true` + `HAS_PORTAL_ORDERS = true` + data rows | Conditional | **Yes** `[COLLAPSE]` |
| 8 | Selling vs Admin Time | Q-65 | `MIXPANEL_USER_DATA_PRESENT = true` + data rows + spread >20pp | **Conditional** (spread >20pp required) | No |
| 9 | Inactive Reps with Territory Revenue | Q-70 | `HAS_PORTAL_ORDERS = true` + `PORTAL_REP_DATA_PRESENT = true` + data rows | Conditional | **Yes** `[COLLAPSE]` |

## TARGET STRUCTURE — Gold Standard (MATCH THIS MARKUP EXACTLY)

This is the corresponding section from the canonical reference report. It is the source of truth for HTML structure: tag nesting, class names, column headers, subsection order, which subsections carry a `what-this-means` block, and the `<thead>`/`<tbody>`/`row-highlight` patterns. The data values below are illustrative — replace them with this client's data — but reproduce the STRUCTURE exactly. Where this target and the prose guide disagree on markup, THIS WINS.

```html
<details class="section-collapse" id="team">
  <summary>
    <div class="section-title">Team Intelligence</div>
    <div class="section-sub">32 active reps &middot; $8.6M eCat sales LTM &middot; behavioral patterns from app usage data</div>
    <div class="section-contents">Rep leaderboard, adoption metrics, behavioral archetypes, coaching opportunities, engagement trajectory</div>
    <span class="expand-hint">Expand section</span>
  </summary>
  <div class="section">

    <div class="data-confidence">
      <span class="data-confidence-label">Full Picture</span>
      This section combines eCat order data, all-channel sales from your total business feed, and app usage behavioral data. All 32 active reps have complete profiles across all three sources.
    </div><div class="subsection">
      <div class="subsection-title">Rep Leaderboard</div>
      <div class="sub-label">Ranked by eCat Sales LTM</div>
      <table>
        <thead>
          <tr><th>#</th><th>Rep</th><th>eCat Sales LTM</th><th>All-Channel LTM</th><th>Digital Share</th><th>YoY Change</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td>1</td><td><strong>Rachel Simmons</strong></td><td>$1,124,000</td><td>$2,890,000</td><td>38.9%</td><td class="metric-note ok">+24.2%</td></tr>
          <tr class="row-highlight"><td>2</td><td><strong>James Whitfield</strong></td><td>$892,000</td><td>$3,410,000</td><td>26.2%</td><td class="metric-note ok">+19.8%</td></tr>
          <tr><td>3</td><td><strong>Patricia Nakamura</strong></td><td>$738,000</td><td>$2,140,000</td><td>34.5%</td><td class="metric-note ok">+31.4%</td></tr>
          <tr><td>4</td><td><strong>David Chen</strong></td><td>$612,000</td><td>$1,960,000</td><td>31.2%</td><td class="metric-note ok">+12.7%</td></tr>
          <tr><td>5</td><td><strong>Maria Gonzalez</strong></td><td>$534,000</td><td>$2,280,000</td><td>23.4%</td><td class="metric-note ok">+8.9%</td></tr>
        </tbody>
      </table>

      <details>
        <summary>Reps 6&ndash;10</summary>
        <table>
          <thead>
            <tr><th>#</th><th>Rep</th><th>eCat Sales LTM</th><th>All-Channel LTM</th><th>Digital Share</th><th>YoY Change</th></tr>
          </thead>
          <tbody>
            <tr><td>6</td><td><strong>Kevin Park</strong></td><td>$487,000</td><td>$1,740,000</td><td>28.0%</td><td class="metric-note ok">+15.3%</td></tr>
            <tr><td>7</td><td><strong>Sarah Mitchell</strong></td><td>$461,000</td><td>$1,520,000</td><td>30.3%</td><td class="metric-note ok">+22.1%</td></tr>
            <tr><td>8</td><td><strong>Tom Bradley</strong></td><td>$398,000</td><td>$2,080,000</td><td>19.1%</td><td class="metric-note warn">+3.2%</td></tr>
            <tr><td>9</td><td><strong>Lisa Fernandez</strong></td><td>$372,000</td><td>$1,380,000</td><td>27.0%</td><td class="metric-note ok">+18.6%</td></tr>
            <tr><td>10</td><td><strong>Robert Kim</strong></td><td>$341,000</td><td>$1,610,000</td><td>21.2%</td><td class="metric-note ok">+9.4%</td></tr>
          </tbody>
        </table>
      </details>

      <details>
        <summary>Full roster (reps 11&ndash;32)</summary>
        <table>
          <thead>
            <tr><th>#</th><th>Rep</th><th>eCat Sales LTM</th><th>All-Channel LTM</th><th>Digital Share</th><th>YoY Change</th></tr>
          </thead>
          <tbody>
            <tr><td>11</td><td>Angela Torres</td><td>$318,000</td><td>$1,290,000</td><td>24.7%</td><td>+14.1%</td></tr>
            <tr><td>12</td><td>Brian Walsh</td><td>$294,000</td><td>$1,180,000</td><td>24.9%</td><td>+11.3%</td></tr>
            <tr><td>13</td><td>Jennifer Liu</td><td>$276,000</td><td>$980,000</td><td>28.2%</td><td>+20.4%</td></tr>
            <tr><td>14</td><td>Mark Stevens</td><td>$248,000</td><td>$1,420,000</td><td>17.5%</td><td>+5.6%</td></tr>
            <tr><td>15</td><td>Nicole Brown</td><td>$231,000</td><td>$890,000</td><td>26.0%</td><td>+16.8%</td></tr>
            <tr><td>16</td><td>Chris Anderson</td><td>$214,000</td><td>$1,040,000</td><td>20.6%</td><td>+7.2%</td></tr>
            <tr><td>17</td><td>Amy Richardson</td><td>$198,000</td><td>$760,000</td><td>26.1%</td><td>+19.2%</td></tr>
            <tr><td>18</td><td>Daniel Hayes</td><td>$182,000</td><td>$920,000</td><td>19.8%</td><td>+4.8%</td></tr>
            <tr><td>19</td><td>Stephanie Cole</td><td>$167,000</td><td>$680,000</td><td>24.6%</td><td>+13.9%</td></tr>
            <tr><td>20</td><td>William Foster</td><td>$153,000</td><td>$840,000</td><td>18.2%</td><td>+6.1%</td></tr>
            <tr><td>21</td><td>Lauren Perry</td><td>$142,000</td><td>$590,000</td><td>24.1%</td><td>+17.3%</td></tr>
            <tr><td>22</td><td>Jason Cooper</td><td>$128,000</td><td>$710,000</td><td>18.0%</td><td>+8.7%</td></tr>
            <tr><td>23</td><td>Michelle Reed</td><td>$114,000</td><td>$520,000</td><td>21.9%</td><td>+12.4%</td></tr>
            <tr><td>24</td><td>Andrew Bell</td><td>$98,000</td><td>$640,000</td><td>15.3%</td><td>+2.1%</td></tr>
            <tr><td>25</td><td>Kimberly Ross</td><td>$86,000</td><td>$480,000</td><td>17.9%</td><td>+9.6%</td></tr>
            <tr><td>26</td><td>Marcus Hill</td><td>$12,000</td><td>$1,180,000</td><td>1.0%</td><td class="metric-note danger">&minus;62.4%</td></tr>
            <tr><td>27</td><td>Diane Ortiz</td><td>$8,400</td><td>$940,000</td><td>0.9%</td><td class="metric-note danger">&minus;78.1%</td></tr>
            <tr><td>28</td><td>Greg Hutchins</td><td>$6,200</td><td>$420,000</td><td>1.5%</td><td class="metric-note danger">&minus;44.8%</td></tr>
            <tr><td>29</td><td>Paula Vernon</td><td>$4,800</td><td>$380,000</td><td>1.3%</td><td class="metric-note danger">&minus;51.2%</td></tr>
            <tr><td>30</td><td>Scott Meyers</td><td>$3,100</td><td>$310,000</td><td>1.0%</td><td class="metric-note danger">&minus;68.9%</td></tr>
            <tr><td>31</td><td>Carol Dunn</td><td>$1,800</td><td>$240,000</td><td>0.8%</td><td class="metric-note danger">&minus;82.3%</td></tr>
            <tr><td>32</td><td>Randy Flores</td><td>$900</td><td>$180,000</td><td>0.5%</td><td class="metric-note danger">&minus;91.0%</td></tr>
          </tbody>
        </table>
      </details>
    </div><div class="subsection">
      <div class="subsection-title">How Much Business Goes Through eCat</div>
      <div class="sub-label">What percentage of each rep&rsquo;s total sales are being placed through eCat vs phone/fax/email</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">Team Average</div>
          <div class="metric-value">23.1%</div>
          <div class="metric-note ok">Up from 20.7% last quarter</div>
        </div>
        <div class="metric">
          <div class="metric-label">Top Reps (Best 8)</div>
          <div class="metric-value">33.7%</div>
          <div class="metric-note">Placing 1 in 3 dollars through eCat</div>
        </div>
        <div class="metric">
          <div class="metric-label">Bottom Reps (Lowest 7)</div>
          <div class="metric-value">2.8%</div>
          <div class="metric-note danger">Barely using eCat at all</div>
        </div>
        <div class="metric">
          <div class="metric-label">Gap Between Top &amp; Bottom</div>
          <div class="metric-value">30.9 pts</div>
          <div class="metric-note warn">Was 22 pts last year &mdash; growing</div>
        </div>
      </div>
      <div class="what-this-means">
        <strong>Action:</strong> Your best reps place a third of their business through eCat. Your worst barely touch it. Marcus Hill has $1.18M in total sales but only 1% goes through eCat. Diane Ortiz has $940K total but only 0.9% digital. If you can get those two reps to even 15%, that&rsquo;s roughly $290K more flowing through eCat per year &mdash; visible, trackable, and reportable.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Behavioral Archetypes</div>
      <div class="sub-label">Based on app usage patterns over trailing 90 days</div>
      <table>
        <thead>
          <tr><th>Archetype</th><th>Reps</th><th>Behavior Pattern</th><th>Avg eCat Sales LTM</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td><span class="badge ok">Power User</span></td><td>8</td><td>Daily sessions, builds presentations, uses saved carts</td><td>$682,000</td></tr>
          <tr><td><span class="badge info">Steady Performer</span></td><td>11</td><td>3&ndash;4 sessions/week, primarily order entry and catalog browse</td><td>$284,000</td></tr>
          <tr><td><span class="badge warn">Sporadic</span></td><td>6</td><td>1&ndash;2 sessions/week, mostly at appointments</td><td>$142,000</td></tr>
          <tr class="row-warn"><td><span class="badge danger">Dormant</span></td><td>7</td><td>No sessions in 45+ days</td><td>$5,300</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Your 8 Power Users average $682K each through eCat while Steady Performers average $284K &mdash; a 2.4x multiplier. Move 3 Steady Performers (Tom Bradley, Mark Stevens, Chris Anderson) to Power User behavior by training them on presentation-building and saved carts; their high all-channel volumes ($2.08M, $1.42M, $1.04M respectively) suggest they have the customer base to convert.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Presentation-to-Close Conversion</div>
      <table>
        <thead>
          <tr><th>Rep</th><th>Presentations Created</th><th>Orders Within 14 Days</th><th>Conversion Rate</th><th>Avg Order Value</th></tr>
        </thead>
        <tbody>
          <tr class="row-highlight"><td><strong>Rachel Simmons</strong></td><td>142</td><td>126</td><td>88.7%</td><td>$2,840</td></tr>
          <tr><td><strong>Patricia Nakamura</strong></td><td>98</td><td>79</td><td>80.6%</td><td>$2,180</td></tr>
          <tr><td><strong>James Whitfield</strong></td><td>118</td><td>89</td><td>75.4%</td><td>$3,210</td></tr>
          <tr><td><strong>David Chen</strong></td><td>84</td><td>61</td><td>72.6%</td><td>$2,460</td></tr>
          <tr><td><strong>Maria Gonzalez</strong></td><td>72</td><td>48</td><td>66.7%</td><td>$1,920</td></tr>
        </tbody>
      </table>
      <div class="what-this-means">
        <strong>Action:</strong> Rachel Simmons converts 89% of her presentations into orders at $2,840 average &mdash; significantly above the team mean of 61%. Share her presentation templates (she builds curated room-scene collections rather than full-catalog walks) with Patricia Nakamura and James Whitfield, who have the volume but lower conversion.
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Engagement Trajectory</div>
      <div class="sub-label">Quarter-over-quarter session trend</div>

      <div class="callout opportunity">
        <div class="callout-title">Accelerating (9 reps)</div>
        <ul>
          <li><strong>Patricia Nakamura:</strong> Sessions up 42% QoQ, eCat sales following with +31% YoY &mdash; on pace to break into top 2 by Q4</li>
          <li><strong>Jennifer Liu:</strong> Sessions up 38% QoQ after completing advanced training in February</li>
          <li><strong>Amy Richardson:</strong> Sessions up 34% QoQ, new territory assignment driving exploration</li>
        </ul>
      </div>

      <div class="callout insight">
        <div class="callout-title">Declining (5 reps &mdash; not yet dormant)</div>
        <ul>
          <li><strong>Tom Bradley:</strong> Sessions down 28% QoQ despite $2.08M all-channel. Likely ordering by phone/email &mdash; not lost business, but lost visibility</li>
          <li><strong>Andrew Bell:</strong> Sessions down 31% QoQ, coincides with paternity leave &mdash; expected to recover Q3</li>
          <li><strong>Mark Stevens:</strong> Sessions down 22% QoQ, territory restructuring may have disrupted routine</li>
        </ul>
      </div>
    </div><div class="subsection">
      <div class="subsection-title">Coaching Opportunities</div>
      <div class="sub-label">Reps with highest estimated upside from targeted intervention</div>

      <div class="coaching-card">
        <div class="coaching-header">
          <div class="coaching-name">Tom Bradley</div>
          <span class="badge warn">Sporadic User</span>
        </div>
        <div class="coaching-body">
          Tom manages $2.08M in all-channel business but only 19.1% flows through eCat ($398K). His app sessions dropped 28% this quarter, yet his total sales are stable. He&rsquo;s taking orders by phone that could be tracked digitally.
        </div>
        <div class="coaching-action">Recommended: Set up his top 15 accounts with saved carts pre-loaded with their reorder history. Show him that re-ordering takes 2 taps instead of a phone call.</div>
        <div class="coaching-impact">+$124K estimated annual shift to eCat</div>
      </div>

      <div class="coaching-card">
        <div class="coaching-header">
          <div class="coaching-name">Marcus Hill</div>
          <span class="badge danger">Dormant</span>
        </div>
        <div class="coaching-body">
          Marcus covers the Southeast Hospitality territory ($1.18M all-channel) but has placed only $12K through eCat this year &mdash; a 62% decline from last year. His territory includes Heritage Hospitality Group and 3 other high-value accounts ordering entirely by fax.
        </div>
        <div class="coaching-action">Recommended: Schedule a 1:1 session focused on the Modern Collection launch + hospitality-specific presentations. His accounts are already buying &mdash; the app just isn&rsquo;t part of his workflow.</div>
        <div class="coaching-impact">+$178K estimated annual shift to eCat</div>
      </div>

      <div class="coaching-card">
        <div class="coaching-header">
          <div class="coaching-name">Diane Ortiz</div>
          <span class="badge danger">Dormant</span>
        </div>
        <div class="coaching-body">
          Diane&rsquo;s Mid-Atlantic Residential territory generates $940K in all-channel sales, but her digital share collapsed to 0.9%. She was an active user 8 months ago (averaging 12 sessions/week) before an iPad hardware failure. She never re-logged in after getting a replacement device.
        </div>
        <div class="coaching-action">Recommended: IT confirms her credentials are still active. A 15-minute &ldquo;welcome back&rdquo; call to restore her saved presentations and demonstrate the new Quick Order feature could reactivate her immediately.</div>
        <div class="coaching-impact">+$142K estimated annual shift to eCat</div>
      </div>
    </div><div class="subsection">
      <div class="subsection-title">How Reps Spend Their Time in the App</div>
      <div class="sub-label">We classify every app session as either &ldquo;selling&rdquo; (showing products, building presentations, placing orders) or &ldquo;admin&rdquo; (looking up accounts, checking order history, pulling reports). Here&rsquo;s the split over the last 90 days.</div>
      <div class="metrics">
        <div class="metric">
          <div class="metric-label">Avg Selling Time</div>
          <div class="metric-value">68%</div>
          <div class="metric-note">Showing products, building orders</div>
        </div>
        <div class="metric">
          <div class="metric-label">Avg Admin Time</div>
          <div class="metric-value">32%</div>
          <div class="metric-note">Looking up accounts, checking history</div>
        </div>
        <div class="metric">
          <div class="metric-label">Most Efficient Rep</div>
          <div class="metric-value">82 / 18</div>
          <div class="metric-note">Rachel Simmons</div>
        </div>
        <div class="metric">
          <div class="metric-label">Most Admin-Heavy Rep</div>
          <div class="metric-value">41 / 59</div>
          <div class="metric-note warn">Daniel Hayes</div>
        </div>
      </div>
      <div class="what-this-means">
        <strong>Action:</strong> Daniel Hayes spends 59% of his app time just looking things up instead of selling. Building him a custom SmartList of his top 20 accounts with pre-filtered inventory views could flip that closer to 60/40 and free up roughly 3 hours/week he could spend in front of buyers.
      </div>
    </div><details>
      <summary>Territory Coverage</summary>
      <table>
        <thead>
          <tr><th>Territory</th><th>Rep(s)</th><th>Accounts</th><th>All-Channel LTM</th><th>eCat Sales LTM</th><th>Digital Share</th></tr>
        </thead>
        <tbody>
          <tr><td>Northeast Hospitality</td><td>Rachel Simmons</td><td>186</td><td>$2,890,000</td><td>$1,124,000</td><td>38.9%</td></tr>
          <tr><td>West Coast Contract</td><td>James Whitfield</td><td>214</td><td>$3,410,000</td><td>$892,000</td><td>26.2%</td></tr>
          <tr><td>Pacific Northwest</td><td>Patricia Nakamura</td><td>142</td><td>$2,140,000</td><td>$738,000</td><td>34.5%</td></tr>
          <tr><td>Southwest Residential</td><td>David Chen</td><td>168</td><td>$1,960,000</td><td>$612,000</td><td>31.2%</td></tr>
          <tr><td>Great Lakes</td><td>Maria Gonzalez</td><td>198</td><td>$2,280,000</td><td>$534,000</td><td>23.4%</td></tr>
          <tr><td>Southeast Hospitality</td><td>Marcus Hill</td><td>156</td><td>$1,180,000</td><td>$12,000</td><td class="metric-note danger">1.0%</td></tr>
          <tr><td>Mid-Atlantic Residential</td><td>Diane Ortiz</td><td>134</td><td>$940,000</td><td>$8,400</td><td class="metric-note danger">0.9%</td></tr>
        </tbody>
      </table>
    </details><details>
      <summary>Inactive Reps (45+ days since last session)</summary>
      <table>
        <thead>
          <tr><th>Rep</th><th>Days Inactive</th><th>All-Channel LTM</th><th>Last eCat Order</th><th>Likely Cause</th></tr>
        </thead>
        <tbody>
          <tr class="row-danger"><td><strong>Marcus Hill</strong></td><td>52</td><td>$1,180,000</td><td>Apr 26, 2026</td><td>Workflow preference (phone/fax)</td></tr>
          <tr class="row-danger"><td><strong>Diane Ortiz</strong></td><td>58</td><td>$940,000</td><td>Apr 20, 2026</td><td>iPad hardware replacement &mdash; never re-logged in</td></tr>
          <tr><td>Greg Hutchins</td><td>47</td><td>$420,000</td><td>May 1, 2026</td><td>Unknown &mdash; investigate</td></tr>
          <tr><td>Paula Vernon</td><td>61</td><td>$380,000</td><td>Apr 17, 2026</td><td>Territory transition in progress</td></tr>
          <tr><td>Scott Meyers</td><td>73</td><td>$310,000</td><td>Apr 5, 2026</td><td>Semi-retirement announced</td></tr>
          <tr><td>Carol Dunn</td><td>89</td><td>$240,000</td><td>Mar 20, 2026</td><td>Extended medical leave</td></tr>
          <tr><td>Randy Flores</td><td>104</td><td>$180,000</td><td>Mar 5, 2026</td><td>Transitioning off the team</td></tr>
        </tbody>
      </table>
    </details>

    <div class="what-this-means" style="margin-top:24px;">
      <strong>Bottom line:</strong> Your top quartile is pulling away from the pack &mdash; 8 Power Users now drive 63% of all eCat revenue. The fastest win isn&rsquo;t recruiting new reps; it&rsquo;s getting Tom Bradley, Marcus Hill, and Diane Ortiz (combined $4.1M all-channel) using the tools their peers already rely on daily.
    </div>

    <div class="callout note" style="margin-top:20px;">
      <div class="callout-title">With Connected Data</div>
      Connecting your CRM (meeting logs, call notes) would let us correlate in-person visits with same-week eCat orders &mdash; showing which reps use the app as a follow-up tool vs. a replacement for in-person selling.
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

## D. Dollar Math Rules

- **`[HYPOTHETICAL]`** on all projections (any dollar figure not directly
  measured from source data).
- **`[ESTIMATED]`** on extrapolations (figures derived from incomplete data
  via scaling or inference).
- Inline tag + sentence = complete disclosure. No separate Appendix entry needed.
- eCat figures are **eCat-channel only** unless explicitly stated otherwise.
- `portal_orders` figures = **total ERP business across all channels**.
- Never claim broader than data supports.

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


## Authority — Q-02 & Q-03 Derivation Rules

These classification and funnel-gap rules are applied to Q-01 Step 1 data when building the Behavioral Scorecard and Coaching subsections. They are not pre-computed by Stage 1.


### Q-02: Selling Archetype Classification
**Maps to**: VM-02 | **Audience**: external | **Status**: live (derived from Q-01)

No separate query — archetypes are derived from Q-01 behavioral ratios. Classification rules:

| Archetype | Detection Rule |
|-----------|----------------|
| Deep-Account Specialist | High `customer_targeting` + high orders + `unique_customers ≤ 3` |
| Curated Discovery Seller | Top-quartile `presentation` + high `product_discovery` + `avg_order_value` above org median |
| Volume Relationship Seller | Highest `days_active` or `total_events` + broadest `unique_customers` + AOV below org median |
| Precision Closer | Low `product_discovery` + high `config_bundling` per order + AOV well above org median |
| Non-Selling Role | `submit_order ≤ 2` + `total_events > 500` — route to Q-04 |

**Gate**: Requires 3+ active selling reps. VM-02 requires VM-01 first.

### Q-03: Behavioral Funnel Gap Analysis
**Maps to**: VM-03 | **Audience**: external | **Status**: live (derived from Q-01)

Derived from Q-01 dimensional scores. For each selling rep (`submit_order > 5`), assess ratio of each dimension to upstream:

1. Customer Targeting → Product Discovery: `product_discovery / customer_targeting` — if < 3:1, rep isn't discovering enough after selecting customers.
2. Product Discovery → Configuration: `config_bundling / product_discovery` — if < 0.1, browses but doesn't build complex orders.
3. Configuration → Presentation: `presentation / config_bundling` — if < 0.1, configures but doesn't share.
4. Presentation → Orders: `submit_order / presentation` — disproportionately low = closure gap.

Flag reps with any funnel ratio in the bottom quartile for the org.

**External claim rules**: Per-rep funnel gap with specific behavioral data. Quantified upside using peer AOV differences — always tag `[HYPOTHETICAL]`.

## Cache Data

### signal_rank.md

# Signal Rank — Sarreid, Ltd. (fal, org_id=1)
- **Run date**: 2026-06-17
- **Total signals fired**: 72 (P0: 53, P1: 18, P2: 1)
- **Org GMV**: $2.6M eCat LTM, $15.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep digital-enablement opportunity — 2 reps run $7.6M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion | P1 | §5 Team | 15.2 | $7,600,000 | 2.0 | 231,040,000 | POSITIVE |
| 2 | SIG-OPP-02 | Unactivated High-Value Accounts — 12 non-enterprise accounts with $6.6M+ total business, zero eCat orders | P1 | §2 Accounts | 6.6 | $6,615,227 | 2.0 | 87,522,457 | POSITIVE |
| 3 | SIG-ANOMALY-02 | Stock Out — 52760 (Lilac Sideboard, Blue Finish) $475,590 LTM, 0 available | P0 | §3 Product | 10.0 | $475,590 | 3.0 | 14,267,694 | RISK |
| 4 | SIG-OPP-01 | Next Best Product — 52760/26715-5 co-purchase pattern across 16 customers | P0 | §2/§3 | 1.6 | $3,426,152 | 2.0 | 10,963,686 | POSITIVE |
| 5 | SIG-ANOMALY-02 | Stock Out — 26715-5 (Ciborium Chest Of Drawers, Fruitwood) $202,685 LTM, 0 available | P0 | §3 Product | 10.0 | $202,685 | 3.0 | 6,080,554 | RISK |
| 6 | SIG-ANOMALY-02 | Stock Out — 53008 (Chamberlain Chest Of Drawers) $122,222 LTM, 0 available | P0 | §3 Product | 10.0 | $122,222 | 3.0 | 3,666,673 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 27844 (Caracole Credenza, Driftwood Finish) $113,249 LTM, 0 available | P0 | §3 Product | 10.0 | $113,249 | 3.0 | 3,397,456 | RISK |
| 8 | SIG-ANOMALY-02 | Stock Out — 54201-LM (Casual Jupe Dining Table,Light Mink,Lg) $110,748 LTM, 0 available | P0 | §3 Product | 10.0 | $110,748 | 3.0 | 3,322,425 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — 53862 (Harper Sideboard) $108,949 LTM, 0 available | P0 | §3 Product | 10.0 | $108,949 | 3.0 | 3,268,472 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 53888 (Bronson Swivel Chair) $108,747 LTM, 0 available | P0 | §3 Product | 10.0 | $108,747 | 3.0 | 3,262,423 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 53846 (Nolan Chair) $107,284 LTM, 0 available | P0 | §3 Product | 10.0 | $107,284 | 3.0 | 3,218,516 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — 26792 (Capital Serving Cart, Fruitwood Finish) $96,998 LTM, 0 available | P0 | §3 Product | 10.0 | $96,998 | 3.0 | 2,909,941 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 54174 (Hugo Oval Side Chair, Cortina White) $92,566 LTM, 0 available | P0 | §3 Product | 10.0 | $92,566 | 3.0 | 2,776,966 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 53311 (San Marco Bungalow Credenza) $92,535 LTM, 0 available | P0 | §3 Product | 10.0 | $92,535 | 3.0 | 2,776,050 | RISK |
| 15 | SIG-ANOMALY-02 | Stock Out — 53130 (Tufted English Club Sofa, Cuba Brown) $89,806 LTM, 0 available | P0 | §3 Product | 10.0 | $89,806 | 3.0 | 2,694,192 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — 29541 (Studded Gentleman's Chest) $86,997 LTM, 0 available | P0 | §3 Product | 10.0 | $86,997 | 3.0 | 2,609,913 | RISK |
| 17 | SIG-ANOMALY-02 | Stock Out — 52744 (Refined Arches Tall Bookcase) $86,462 LTM, 0 available | P0 | §3 Product | 10.0 | $86,462 | 3.0 | 2,593,851 | RISK |
| 18 | SIG-ANOMALY-02 | Stock Out — 52982 (Shagreen Gold & Gray Console) $78,875 LTM, 0 available | P0 | §3 Product | 10.0 | $78,875 | 3.0 | 2,366,245 | RISK |
| 19 | SIG-ANOMALY-02 | Stock Out — 29780 (Welsh Chair) $77,328 LTM, 0 available | P0 | §3 Product | 10.0 | $77,328 | 3.0 | 2,319,842 | RISK |
| 20 | SIG-ANOMALY-02 | Stock Out — 53643 (Guillermo Dining Table) $73,761 LTM, 0 available | P0 | §3 Product | 10.0 | $73,761 | 3.0 | 2,212,841 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 32 | 1 | 0 | 33 | |
| §3 Product Intelligence | 20 | 0 | 1 | 21 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 2 | 0 | 2 | |
| §6 Platform Context | 0 | 14 | 0 | 14 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep digital-enablement opportunity — 2 reps run $7.6M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion
2. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 12 non-enterprise accounts with $6.6M+ total business, zero eCat orders
3. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 52760/26715-5 co-purchase pattern across 16 customers
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Digital order enablement — eCat handles 16.7% of $16M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 52760 (Lilac Sideboard, Blue Finish) $475,590 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 26715-5 (Ciborium Chest Of Drawers, Fruitwood) $202,685 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 53008 (Chamberlain Chest Of Drawers) $122,222 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### coaching_candidates.md

# Coaching Candidates — Sarreid, Ltd. (fal)

Deterministically computed by detect_signals.py. The section agent renders
these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,
or add reps. Archetype framing + narrative are written by the agent; the rep
set and the estimated upside dollar figures are fixed here.

- **Benchmark conversion (top-quartile of converting qualifying reps)**: 11.7%
- **Qualifying reps (>= 50 presentations)**: 7 (6 converting)
- **Upside floor**: $50,000
- **Candidates above floor**: 0

**No coaching cards for this client — render NO coaching cards and NO coaching rollup callout.** Reason: No qualifying rep's estimated upside clears the $50,000 floor (benchmark 11.7%; low AOV / presentation volume).

### Q-01_step1_results.md

# Q-01-S1 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 65
- **Run date**: 2026-06-17


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mroman | 415 | 11,780 | 2024-11-01 13:44 | 2026-06-16 14:48 | 6,237 | 1,715 | 4,522 | 1,553 | 1,531 | 10 | 109 | 109 | 0 | 0 | 3 | 0 | 3 | 0 | 696 | 589 | 0 | 0 | 0 | 0 | 2 | 44 | 1,081 |
| bkrieger | 445 | 6,840 | 2024-11-01 08:29 | 2026-06-16 18:03 | 2,908 | 813 | 2,095 | 1,008 | 1,001 | 6 | 34 | 34 | 0 | 0 | 2 | 2 | 0 | 0 | 276 | 260 | 0 | 1 | 0 | 0 | 4 | 67 | 74 |
| dhalpern | 355 | 6,554 | 2024-11-05 09:51 | 2026-06-12 19:23 | 2,628 | 798 | 1,830 | 1,089 | 1,071 | 8 | 83 | 83 | 0 | 0 | 53 | 20 | 32 | 1 | 734 | 651 | 0 | 4 | 0 | 0 | 10 | 252 | 250 |
| steven | 352 | 5,725 | 2024-11-01 14:06 | 2026-06-16 16:12 | 2,394 | 384 | 2,010 | 635 | 582 | 5 | 13 | 13 | 0 | 0 | 17 | 6 | 11 | 0 | 1,239 | 1,235 | 0 | 14 | 0 | 0 | 0 | 24 | 16 |
| lnagel | 328 | 4,991 | 2024-11-02 11:26 | 2026-06-16 13:51 | 2,049 | 1,094 | 955 | 535 | 506 | 13 | 23 | 20 | 3 | 0 | 68 | 51 | 17 | 0 | 213 | 202 | 0 | 34 | 0 | 0 | 13 | 631 | 105 |
| imendoza | 340 | 4,964 | 2024-11-04 18:08 | 2026-06-16 17:51 | 1,797 | 623 | 1,174 | 746 | 742 | 3 | 38 | 38 | 0 | 0 | 160 | 99 | 61 | 0 | 488 | 474 | 0 | 36 | 0 | 1 | 0 | 361 | 124 |
| acawley | 354 | 4,247 | 2024-11-01 14:46 | 2026-06-16 20:07 | 948 | 721 | 227 | 865 | 850 | 15 | 39 | 39 | 0 | 0 | 31 | 24 | 6 | 1 | 609 | 523 | 0 | 5 | 0 | 0 | 0 | 25 | 462 |
| lseamon | 388 | 4,166 | 2024-11-01 18:19 | 2026-06-15 12:48 | 958 | 943 | 15 | 1,318 | 1,306 | 12 | 21 | 21 | 0 | 0 | 17 | 2 | 15 | 0 | 315 | 289 | 0 | 4 | 0 | 0 | 0 | 231 | 72 |
| coylej | 234 | 3,945 | 2024-11-04 13:03 | 2025-12-18 20:50 | 1,946 | 568 | 1,378 | 734 | 723 | 2 | 54 | 54 | 0 | 0 | 0 | 0 | 0 | 0 | 138 | 133 | 0 | 4 | 0 | 0 | 1 | 23 | 234 |
| rgould | 298 | 2,566 | 2024-11-04 13:42 | 2026-06-16 12:06 | 745 | 447 | 298 | 563 | 559 | 1 | 35 | 35 | 0 | 0 | 28 | 10 | 17 | 1 | 298 | 256 | 0 | 4 | 0 | 0 | 1 | 112 | 35 |
| agavino | 174 | 2,335 | 2024-11-04 13:15 | 2026-06-16 14:13 | 850 | 261 | 589 | 321 | 289 | 16 | 35 | 35 | 0 | 0 | 82 | 16 | 66 | 0 | 335 | 303 | 0 | 1 | 0 | 0 | 4 | 62 | 52 |
| murkassoc | 208 | 2,215 | 2024-11-04 10:30 | 2026-06-15 11:09 | 546 | 253 | 293 | 302 | 289 | 7 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 681 | 638 | 0 | 1 | 0 | 0 | 1 | 55 | 112 |
| halld | 156 | 1,860 | 2024-11-01 10:15 | 2026-05-01 15:13 | 641 | 213 | 428 | 379 | 370 | 9 | 27 | 27 | 0 | 0 | 16 | 5 | 11 | 0 | 244 | 227 | 0 | 6 | 0 | 0 | 5 | 19 | 70 |
| bbeckermann | 193 | 1,824 | 2024-11-02 19:07 | 2026-06-16 18:20 | 389 | 257 | 132 | 251 | 244 | 2 | 23 | 23 | 0 | 0 | 11 | 0 | 11 | 0 | 388 | 380 | 0 | 1 | 0 | 0 | 1 | 51 | 156 |
| lfaria | 174 | 1,806 | 2024-11-01 08:26 | 2026-06-16 10:34 | 431 | 120 | 311 | 277 | 275 | 2 | 16 | 16 | 0 | 0 | 17 | 4 | 13 | 0 | 328 | 327 | 0 | 3 | 0 | 0 | 1 | 24 | 18 |
| dunnlighting | 201 | 1,603 | 2024-11-04 17:46 | 2026-06-15 19:57 | 448 | 188 | 260 | 316 | 273 | 0 | 9 | 9 | 0 | 0 | 7 | 0 | 7 | 0 | 248 | 239 | 0 | 5 | 0 | 0 | 1 | 6 | 22 |
| mberesford | 122 | 1,569 | 2024-11-01 09:40 | 2025-11-12 12:13 | 638 | 94 | 544 | 134 | 131 | 3 | 6 | 6 | 0 | 0 | 7 | 7 | 0 | 0 | 488 | 483 | 0 | 1 | 0 | 0 | 1 | 12 | 10 |
| jschardar | 152 | 1,538 | 2024-11-13 17:19 | 2026-06-05 15:50 | 664 | 213 | 451 | 268 | 255 | 4 | 37 | 37 | 0 | 0 | 4 | 0 | 4 | 0 | 28 | 27 | 0 | 0 | 0 | 0 | 1 | 54 | 110 |
| jessicam | 155 | 1,521 | 2024-11-04 13:13 | 2026-06-15 10:44 | 666 | 213 | 453 | 244 | 243 | 1 | 20 | 20 | 0 | 0 | 3 | 0 | 3 | 0 | 107 | 107 | 0 | 2 | 0 | 0 | 0 | 31 | 63 |
| mperez-caromano | 89 | 1,355 | 2025-02-12 13:11 | 2026-01-02 13:39 | 418 | 57 | 361 | 259 | 252 | 0 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 333 | 333 | 0 | 1 | 0 | 0 | 1 | 12 | 18 |
| sandy | 189 | 1,324 | 2024-11-04 12:48 | 2026-04-20 15:40 | 246 | 122 | 124 | 302 | 300 | 2 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 213 | 209 | 0 | 1 | 0 | 0 | 0 | 27 | 64 |
| jeffizower | 109 | 1,252 | 2024-11-01 09:46 | 2026-06-16 11:10 | 336 | 109 | 227 | 401 | 391 | 4 | 8 | 8 | 0 | 0 | 10 | 2 | 8 | 0 | 101 | 101 | 0 | 36 | 0 | 4 | 2 | 25 | 63 |
| lhalpern | 64 | 1,098 | 2024-11-01 14:39 | 2025-02-17 10:46 | 463 | 136 | 327 | 210 | 196 | 6 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 41 | 27 | 0 | 0 | 0 | 0 | 12 | 92 | 59 |
| robantonecchia | 154 | 1,018 | 2024-11-04 06:11 | 2026-06-16 14:02 | 202 | 91 | 111 | 231 | 213 | 13 | 2 | 2 | 0 | 0 | 8 | 0 | 8 | 0 | 191 | 191 | 0 | 0 | 0 | 0 | 0 | 6 | 21 |
| kkepley | 92 | 954 | 2025-07-16 11:41 | 2026-04-27 10:44 | 307 | 74 | 233 | 224 | 220 | 3 | 5 | 5 | 0 | 0 | 37 | 37 | 0 | 0 | 116 | 114 | 0 | 0 | 0 | 0 | 2 | 20 | 27 |
| gnover | 100 | 936 | 2024-11-01 07:20 | 2026-05-29 11:16 | 74 | 74 | 0 | 146 | 132 | 13 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 412 | 399 | 0 | 0 | 0 | 0 | 0 | 16 | 1 |
| r_garcia | 41 | 924 | 2026-03-19 13:11 | 2026-06-16 19:36 | 481 | 91 | 390 | 176 | 175 | 1 | 12 | 12 | 0 | 0 | 2 | 1 | 1 | 0 | 58 | 56 | 0 | 1 | 0 | 0 | 1 | 19 | 16 |
| bsheffield | 69 | 905 | 2026-01-10 10:48 | 2026-06-15 10:44 | 424 | 132 | 292 | 94 | 93 | 1 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 121 | 111 | 0 | 0 | 0 | 0 | 0 | 19 | 26 |
| rhiggins | 54 | 875 | 2024-11-12 10:40 | 2025-07-08 17:22 | 134 | 42 | 92 | 194 | 174 | 2 | 1 | 1 | 0 | 0 | 6 | 0 | 6 | 0 | 355 | 353 | 0 | 1 | 0 | 0 | 0 | 1 | 22 |
| pcladis | 49 | 779 | 2025-12-05 14:21 | 2026-05-07 17:24 | 247 | 68 | 179 | 129 | 128 | 1 | 3 | 1 | 2 | 0 | 1 | 1 | 0 | 0 | 153 | 144 | 0 | 0 | 0 | 0 | 7 | 50 | 26 |
| etsarkov | 70 | 738 | 2024-11-01 14:39 | 2026-01-28 06:02 | 139 | 44 | 95 | 102 | 95 | 2 | 0 | 0 | 0 | 0 | 9 | 1 | 8 | 0 | 236 | 233 | 0 | 17 | 0 | 1 | 1 | 30 | 23 |
| shelly | 64 | 544 | 2024-11-04 11:57 | 2026-04-15 17:43 | 125 | 66 | 59 | 95 | 94 | 1 | 3 | 3 | 0 | 0 | 1 | 0 | 1 | 0 | 152 | 133 | 0 | 0 | 0 | 0 | 0 | 5 | 8 |
| hesslerj | 58 | 497 | 2024-11-01 13:20 | 2026-01-10 15:24 | 73 | 20 | 53 | 101 | 92 | 5 | 0 | 0 | 0 | 0 | 11 | 1 | 9 | 1 | 78 | 75 | 0 | 19 | 0 | 0 | 0 | 0 | 6 |
| tannerg | 86 | 416 | 2024-11-05 15:43 | 2026-06-16 12:05 | 50 | 17 | 33 | 111 | 111 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 77 | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 4 |
| osimonova | 25 | 395 | 2024-11-16 14:02 | 2026-04-16 14:24 | 35 | 19 | 16 | 58 | 51 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 182 | 177 | 0 | 11 | 0 | 2 | 3 | 5 | 8 |
| bmarketing | 49 | 387 | 2024-11-01 12:37 | 2025-11-27 18:07 | 73 | 41 | 32 | 38 | 27 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 101 | 90 | 0 | 0 | 0 | 0 | 0 | 9 | 17 |
| ktekworth | 34 | 384 | 2025-02-10 14:25 | 2025-09-05 17:18 | 121 | 39 | 82 | 27 | 25 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 42 | 36 | 0 | 0 | 0 | 0 | 13 | 36 | 23 |
| williamsl | 58 | 379 | 2024-11-06 09:21 | 2026-01-01 08:08 | 75 | 68 | 7 | 89 | 89 | 0 | 3 | 3 | 0 | 0 | 2 | 2 | 0 | 0 | 31 | 24 | 0 | 0 | 0 | 0 | 0 | 1 | 16 |
| l_ashley | 25 | 306 | 2024-11-04 12:01 | 2025-02-05 17:13 | 101 | 39 | 62 | 42 | 40 | 1 | 13 | 13 | 0 | 0 | 4 | 2 | 2 | 0 | 37 | 37 | 0 | 2 | 0 | 0 | 0 | 9 | 16 |
| rabikhalil | 32 | 301 | 2024-12-08 12:50 | 2026-06-15 07:55 | 92 | 36 | 56 | 100 | 86 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 10 |

*(Truncated: showing top 40 of 65 rows. Full data in cache file.)*

### Q-01_step2_results.md

# Q-01-S2 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 37
- **Run date**: 2026-06-17


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Clyde Barnard | 75 | $555,103 | $7,401 | 27 |
| John Anhut | 82 | $268,420 | $3,273 | 28 |
| Danielle Green | 47 | $195,716 | $4,164 | 15 |
| Deborah Klein | 58 | $169,127 | $2,916 | 24 |
| Stan Terry | 36 | $167,487 | $4,652 | 18 |
| Rip Nance | 33 | $141,577 | $4,290 | 16 |
| Charity Queen | 44 | $128,070 | $2,911 | 17 |
| Ryan  McWilliams | 37 | $119,243 | $3,223 | 16 |
| Jenny Bowers | 15 | $116,198 | $7,747 | 10 |
| Joan Harrison | 31 | $91,422 | $2,949 | 10 |
| Carmy Muller | 9 | $69,475 | $7,720 | 7 |
| April Davis | 9 | $65,887 | $7,321 | 8 |
| Bridget Delaney | 7 | $49,126 | $7,018 | 5 |
| Kip Meyer | 6 | $46,056 | $7,676 | 4 |
| Anne Schroth | 7 | $43,383 | $6,198 | 5 |
| Beth Sartore | 1 | $36,028 | $36,028 | 0 |
| James  Bertelsen | 7 | $25,691 | $3,670 | 6 |
| Dan Linker | 10 | $25,080 | $2,508 | 6 |
| David Holbrook | 11 | $24,948 | $2,268 | 7 |
| Andrew Cymrot | 8 | $22,942 | $2,868 | 3 |
| Bert Wood | 3 | $21,475 | $7,158 | 2 |
| Hannah Hoxworth | 7 | $20,442 | $2,920 | 3 |
| Kirsten Seidl | 8 | $19,774 | $2,472 | 6 |
| Maria Oloffo | 7 | $19,365 | $2,766 | 5 |
| Chet Linker | 9 | $18,560 | $2,062 | 6 |
| Beth Maffei | 5 | $14,611 | $2,922 | 3 |
| Steve Knaak | 4 | $13,784 | $3,446 | 2 |
| Roxanne  Fernandini | 7 | $12,732 | $1,819 | 4 |
| Maddie Cannon | 5 | $12,457 | $2,491 | 4 |
| Matthew Eatmon | 1 | $9,595 | $9,595 | 1 |
| Kurt Muller | 3 | $8,714 | $2,905 | 2 |
| Doug Kauffman | 4 | $7,749 | $1,937 | 3 |
| Johnathan Graubart | 4 | $7,427 | $1,857 | 2 |
| Cerice  Odegaard | 1 | $3,862 | $3,862 | 1 |
| Cookie Birardi | 1 | $2,296 | $2,296 | 0 |
| Ryan Moeller | 1 | $935 | $935 | 1 |
| Kristen Miletich | 1 | $263 | $263 | 1 |

### Q-04_results.md

# Q-04 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 65
- **Run date**: 2026-06-17


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mroman | 415 | 11,780 | 1,081 | 1,531 | 589 | 107 | 3 | 0 | 0 | 0 | Selling Rep |
| bkrieger | 445 | 6,840 | 74 | 1,001 | 260 | 16 | 0 | 0 | 0 | 1 | Selling Rep |
| dhalpern | 355 | 6,554 | 250 | 1,071 | 651 | 83 | 32 | 0 | 0 | 4 | Selling Rep |
| steven | 352 | 5,725 | 16 | 582 | 1,235 | 4 | 11 | 0 | 0 | 14 | Selling Rep |
| lnagel | 328 | 4,991 | 105 | 506 | 202 | 11 | 17 | 0 | 0 | 34 | Selling Rep |
| imendoza | 340 | 4,964 | 124 | 742 | 474 | 14 | 61 | 0 | 0 | 37 | Selling Rep |
| acawley | 354 | 4,247 | 462 | 850 | 523 | 86 | 6 | 0 | 0 | 5 | Selling Rep |
| lseamon | 388 | 4,166 | 72 | 1,306 | 289 | 26 | 15 | 0 | 0 | 4 | Selling Rep |
| coylej | 234 | 3,945 | 234 | 723 | 133 | 5 | 0 | 0 | 0 | 4 | Selling Rep |
| rgould | 298 | 2,566 | 35 | 559 | 256 | 42 | 17 | 0 | 0 | 4 | Selling Rep |
| agavino | 174 | 2,335 | 52 | 289 | 303 | 32 | 66 | 0 | 0 | 1 | Selling Rep |
| murkassoc | 208 | 2,215 | 112 | 289 | 638 | 43 | 0 | 0 | 0 | 1 | Selling Rep |
| halld | 156 | 1,860 | 70 | 370 | 227 | 17 | 11 | 0 | 0 | 6 | Selling Rep |
| bbeckermann | 193 | 1,824 | 156 | 244 | 380 | 8 | 11 | 0 | 0 | 1 | Selling Rep |
| lfaria | 174 | 1,806 | 18 | 275 | 327 | 1 | 13 | 0 | 0 | 3 | Selling Rep |
| dunnlighting | 201 | 1,603 | 22 | 273 | 239 | 9 | 7 | 0 | 0 | 5 | Selling Rep |
| mberesford | 122 | 1,569 | 10 | 131 | 483 | 5 | 0 | 0 | 0 | 1 | Selling Rep |
| jschardar | 152 | 1,538 | 110 | 255 | 27 | 1 | 4 | 0 | 0 | 0 | Selling Rep |
| jessicam | 155 | 1,521 | 63 | 243 | 107 | 0 | 3 | 0 | 0 | 2 | Selling Rep |
| mperez-caromano | 89 | 1,355 | 18 | 252 | 333 | 0 | 0 | 0 | 0 | 1 | Selling Rep |
| sandy | 189 | 1,324 | 64 | 300 | 209 | 4 | 0 | 0 | 0 | 1 | Selling Rep |
| jeffizower | 109 | 1,252 | 63 | 391 | 101 | 0 | 8 | 0 | 0 | 40 | Selling Rep |
| lhalpern | 64 | 1,098 | 59 | 196 | 27 | 14 | 0 | 0 | 0 | 0 | Selling Rep |
| robantonecchia | 154 | 1,018 | 21 | 213 | 191 | 0 | 8 | 0 | 0 | 0 | Selling Rep |
| kkepley | 92 | 954 | 27 | 220 | 114 | 2 | 0 | 0 | 0 | 0 | Selling Rep |
| gnover | 100 | 936 | 1 | 132 | 399 | 13 | 0 | 0 | 0 | 0 | Content/Library Manager |
| r_garcia | 41 | 924 | 16 | 175 | 56 | 2 | 1 | 0 | 0 | 1 | Selling Rep |
| bsheffield | 69 | 905 | 26 | 93 | 111 | 10 | 0 | 0 | 0 | 0 | Selling Rep |
| rhiggins | 54 | 875 | 22 | 174 | 353 | 2 | 6 | 0 | 0 | 1 | Selling Rep |
| pcladis | 49 | 779 | 26 | 128 | 144 | 9 | 0 | 0 | 0 | 0 | Selling Rep |
| etsarkov | 70 | 738 | 23 | 95 | 233 | 3 | 8 | 0 | 0 | 18 | Selling Rep |
| shelly | 64 | 544 | 8 | 94 | 133 | 19 | 1 | 0 | 0 | 0 | Selling Rep |
| hesslerj | 58 | 497 | 6 | 92 | 75 | 3 | 9 | 0 | 0 | 19 | Selling Rep |
| tannerg | 86 | 416 | 4 | 111 | 72 | 5 | 0 | 0 | 0 | 0 | Selling Rep |
| osimonova | 25 | 395 | 8 | 51 | 177 | 5 | 0 | 0 | 0 | 13 | Selling Rep |
| bmarketing | 49 | 387 | 17 | 27 | 90 | 11 | 0 | 0 | 0 | 0 | Selling Rep |
| ktekworth | 34 | 384 | 23 | 25 | 36 | 6 | 0 | 0 | 0 | 0 | Selling Rep |
| williamsl | 58 | 379 | 16 | 89 | 24 | 7 | 0 | 0 | 0 | 0 | Selling Rep |
| l_ashley | 25 | 306 | 16 | 40 | 37 | 0 | 2 | 0 | 0 | 2 | Selling Rep |
| rabikhalil | 32 | 301 | 10 | 86 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| allerj | 24 | 296 | 23 | 7 | 26 | 5 | 11 | 0 | 0 | 2 | Selling Rep |
| lgoldblum | 53 | 283 | 8 | 3 | 67 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| kmoretti | 21 | 280 | 8 | 58 | 17 | 0 | 7 | 0 | 0 | 0 | Selling Rep |
| kaceywilliams | 23 | 238 | 1 | 29 | 138 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mmoeller | 17 | 198 | 6 | 34 | 13 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| fmorales | 5 | 186 | 6 | 12 | 82 | 1 | 0 | 0 | 0 | 1 | Selling Rep |
| sschwartz1 | 6 | 150 | 0 | 5 | 113 | 1 | 0 | 0 | 0 | 0 | Inactive |
| kwebb1 | 6 | 139 | 0 | 7 | 93 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jensenltg | 17 | 132 | 7 | 25 | 28 | 4 | 0 | 0 | 0 | 1 | Selling Rep |
| kingh | 11 | 130 | 2 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tcapallia | 5 | 109 | 0 | 3 | 39 | 0 | 0 | 0 | 0 | 0 | Inactive |
| abrazhnikov | 46 | 108 | 8 | 18 | 1 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| k_killgore | 9 | 105 | 0 | 19 | 21 | 0 | 0 | 0 | 0 | 0 | Inactive |
| carterl | 24 | 105 | 2 | 23 | 13 | 0 | 0 | 0 | 0 | 0 | Inactive |
| hschwartz1 | 6 | 77 | 0 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jonv | 17 | 67 | 0 | 0 | 11 | 0 | 0 | 0 | 0 | 0 | Inactive |
| morganb | 14 | 48 | 0 | 6 | 13 | 1 | 0 | 0 | 0 | 0 | Inactive |
| swt | 4 | 42 | 1 | 0 | 6 | 2 | 0 | 0 | 0 | 4 | Inactive |
| kyla | 8 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pgould | 10 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 8 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 2 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pres81224 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| rschwartz1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jewet4924 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 94 | 60 | 26 |

### Q-06_results.md

# Q-06 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 64
- **Run date**: 2026-06-17


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Clyde Barnard | 272 | 252 | -7.40 | 10 | 20 | 100 | $156,740 |
| Deborah Klein | 189 | 218 | 15.30 | 10 | 16 | 60 | $43,929 |
| Jenny Bowers | 127 | 240 | 89 | 0 | 8 | — | $55,028 |
| Joan Harrison | 284 | 259 | -8.80 | 8 | 7 | -12.50 | $27,296 |
| Anne Schroth | 0 | 23 | — | 0 | 7 | — | $43,383 |
| Carmy Muller | 1 | 18 | 1,700 | 0 | 7 | — | $64,038 |
| Danielle Green | 275 | 257 | -6.50 | 13 | 6 | -53.80 | $27,402 |
| Ryan  McWilliams | 251 | 291 | 15.90 | 6 | 6 | 0 | $14,318 |
| Rip Nance | 93 | 103 | 10.80 | 9 | 6 | -33.30 | $21,667 |
| April Davis | 19 | 35 | 84.20 | 0 | 6 | — | $35,420 |
| Stan Terry | 293 | 370 | 26.30 | 7 | 6 | -14.30 | $20,271 |
| Kip Meyer | 0 | 110 | — | 0 | 6 | — | $46,056 |
| Dan Linker | 307 | 340 | 10.70 | 2 | 6 | 200 | $13,937 |
| James  Bertelsen | 113 | 310 | 174.30 | 2 | 5 | 150 | $23,718 |
| Maddie Cannon | 0 | 98 | — | 0 | 5 | — | $12,457 |
| Beth Maffei | 0 | 78 | — | 0 | 5 | — | $14,611 |
| Chet Linker | 274 | 275 | 0.40 | 0 | 4 | — | $12,194 |
| Bridget Delaney | 0 | 11 | — | 0 | 4 | — | $12,731 |
| Doug Kauffman | 246 | 195 | -20.70 | 1 | 3 | 200 | $5,624 |
| Charity Queen | 310 | 78 | -74.80 | 13 | 3 | -76.90 | $7,113 |
| John Anhut | 301 | 41 | -86.40 | 23 | 2 | -91.30 | $6,725 |
| Steve Knaak | 35 | 72 | 105.70 | 3 | 1 | -66.70 | $10,164 |
| Kristen Miletich | 72 | 130 | 80.60 | 0 | 1 | — | $263 |
| Matthew Eatmon | 13 | 18 | 38.50 | 0 | 1 | — | $9,595 |
| Cerice  Odegaard | 27 | 78 | 188.90 | 0 | 1 | — | $3,862 |
| Bert Wood | 0 | 20 | — | 0 | 1 | — | $6,546 |
| Andrew Cymrot | 35 | 34 | -2.90 | 1 | 0 | -100 | $0 |
| David Holbrook | 73 | 63 | -13.70 | 2 | 0 | -100 | $0 |
| Sheryl Madonna | 0 | 3 | — | — | — | — | — |
| Hannah Hoxworth | 10 | 1 | -90 | — | — | — | — |
| Sarreid Showroom | 0 | 1 | — | — | — | — | — |
| Nathan Godwin | 15 | 58 | 286.70 | — | — | — | — |
| Kirsten Seidl | 2 | 0 | -100 | — | — | — | — |
| Steadman Lanier | 79 | 62 | -21.50 | — | — | — | — |
| Loretta Allen | 0 | 13 | — | — | — | — | — |
| Sunil Chauhan | 6 | 14 | 133.30 | — | — | — | — |
| Vinod Sankara | 2 | 5 | 150 | — | — | — | — |
| Brad Cates | 59 | 43 | -27.10 | — | — | — | — |
| Nathan Godwin | 72 | 69 | -4.20 | — | — | — | — |
| Rachel Phillips | 115 | 100 | -13 | — | — | — | — |
| Show Room-4 | 0 | 13 | — | — | — | — | — |
| Beth Sartore | 0 | 16 | — | — | — | — | — |
| Matt Eatmon | 4 | 6 | 50 | — | — | — | — |
| Mickey Sharpe | 158 | 157 | -0.60 | — | — | — | — |
| Karen Wheeler | 0 | 2 | — | — | — | — | — |
| Lavida Williams | 30 | 36 | 20 | — | — | — | — |
| Laura Kelly | 0 | 15 | — | — | — | — | — |
| Bruce White | 0 | 2 | — | — | — | — | — |
| Brent Sanders | 3 | 0 | -100 | — | — | — | — |
| master pack | 2 | 0 | -100 | — | — | — | — |
| Denise  White | 130 | 159 | 22.30 | — | — | — | — |
| Shonta Daniels | 123 | 162 | 31.70 | — | — | — | — |
| Ryan Moeller | 3 | 0 | -100 | — | — | — | — |
| Kayla Smith | 4 | 5 | 25 | — | — | — | — |
| Maricella Robles | 75 | 59 | -21.30 | — | — | — | — |
| Charles Hoffman | 36 | 26 | -27.80 | — | — | — | — |
| Cooper WareHouse 1 | 41 | 45 | 9.80 | — | — | — | — |
| Alex Sarratt | 65 | 18 | -72.30 | — | — | — | — |
| Show Room-3 | 0 | 10 | — | — | — | — | — |
| Jose Gomez | 167 | 157 | -6 | — | — | — | — |
| Larry Sandwick | 2 | 2 | 0 | — | — | — | — |
| AC WareHouse3 | 101 | 115 | 13.90 | — | — | — | — |
| Brenda Ramirez | 41 | 50 | 22 | — | — | — | — |
| Travis Coley | 37 | 44 | 18.90 | — | — | — | — |

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-43_results.md

(not present — file does not exist or is empty)

### Q-43_step2_results.md

# Q-43-S2 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-51_results.md

# Q-51 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-51 — Rep-Level eCat Capture
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| rep_name | rep_number | erp_orders | erp_gmv | erp_customers | ecat_orders | ecat_gmv | ecat_customers | ecat_capture_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Charles Hoffman | 099 | 6,212 | $6.1M | 73 | 0 | $0 | 0 | 0 |
| Deborah Klien | 022 | 1,112 | $1.5M | 86 | 0 | $0 | 0 | 0 |
| Clyde Barnard | 198 | 503 | $1.5M | 147 | 75 | $555,103 | 27 | 36.80 |
| Stan Terry | 032 | 644 | $949,065 | 88 | 36 | $167,487 | 18 | 17.60 |
| Dan Linker | 056 | 418 | $874,661 | 134 | 10 | $25,080 | 6 | 2.90 |
| John Anhut | 016 | 326 | $758,033 | 158 | 82 | $268,420 | 28 | 35.40 |
| Rip Nance | 055 | 227 | $561,188 | 105 | 33 | $141,577 | 16 | 25.20 |
| Joan Harrison | 030 | 258 | $556,820 | 124 | 31 | $91,422 | 10 | 16.40 |
| Danielle Green | 010 | 194 | $531,456 | 87 | 47 | $195,716 | 15 | 36.80 |
| Doug Kauffman | 058 | 217 | $392,337 | 38 | 4 | $7,749 | 3 | 2 |
| Ryan McWilliams | 034 | 128 | $362,421 | 54 | 0 | $0 | 0 | 0 |
| David Holbrook | 025 | 112 | $240,655 | 68 | 11 | $24,948 | 7 | 10.40 |
| Hannah Hoxworth | 050 | 82 | $141,799 | 57 | 7 | $20,442 | 3 | 14.40 |
| John Anhut | 061 | 35 | $109,783 | 23 | 82 | $268,420 | 28 | 244.50 |
| Steve Knaak | 057 | 32 | $92,168 | 24 | 4 | $13,784 | 2 | 15 |
| Roxanne Fernandini | 035 | 43 | $68,869 | 20 | 0 | $0 | 0 | 0 |
| Rafe Bethell | 053 | 33 | $58,079 | 4 | 0 | $0 | 0 | 0 |
| Andy Cymrot | 051 | 24 | $57,460 | 10 | 0 | $0 | 0 | 0 |
| Hannah Hoxworth | 060 | 27 | $52,292 | 18 | 7 | $20,442 | 3 | 39.10 |
| John Anhut | 062 | 28 | $49,216 | 25 | 82 | $268,420 | 28 | 545.40 |
| Maria Oloffo | 036 | 26 | $47,944 | 15 | 7 | $19,365 | 5 | 40.40 |
| Heather Jakusz-Brunning | 039 | 1 | $40,037 | 1 | 0 | $0 | 0 | 0 |
| Johnathan Graubart | 038 | 22 | $39,522 | 19 | 4 | $7,427 | 2 | 18.80 |
| Denise White | 026 | 10 | $30,243 | 8 | 0 | $0 | 0 | 0 |
| Ryan Moeller | 043 | 13 | $28,581 | 10 | 1 | $935 | 1 | 3.30 |

### Q-62_results.md

# Q-62 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 18
- **Run date**: 2026-06-17


| rep_name | new_items_sold | total_new_items | adoption_pct | customers_buying_new | new_item_qty | new_item_revenue | orders_with_new_items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Charles Hoffman | 35 | 112 | 31.30 | 15 | 128 | 106,293.70 | 69 |
| Clyde Barnard | 28 | 112 | 25 | 23 | 89 | 78,546.30 | 34 |
| Danielle Green | 15 | 112 | 13.40 | 13 | 60 | 44,028.20 | 15 |
| Dan Linker | 18 | 112 | 16.10 | 18 | 60 | 42,971.30 | 23 |
| Rip Nance | 11 | 112 | 9.80 | 11 | 31 | 37,487.30 | 14 |
| John Anhut | 18 | 112 | 16.10 | 13 | 31 | 35,868.20 | 15 |
| Deborah Klien | 16 | 112 | 14.30 | 11 | 42 | 33,916.20 | 18 |
| Ryan McWilliams | 13 | 112 | 11.60 | 11 | 42 | 31,564.40 | 14 |
| Stan Terry | 15 | 112 | 13.40 | 12 | 31 | 31,488 | 17 |
| Doug Kauffman | 10 | 112 | 8.90 | 7 | 24 | 25,496.20 | 11 |
| Joan Harrison | 10 | 112 | 8.90 | 9 | 18 | 23,689.10 | 11 |
| David Holbrook | 3 | 112 | 2.70 | 2 | 3 | 7,023.90 | 3 |
| Hannah Hoxworth | 4 | 112 | 3.60 | 3 | 5 | 5,718.70 | 4 |
| Steve Knaak | 1 | 112 | 0.90 | 2 | 2 | 5,026.50 | 2 |
| Donald DiLauro | 1 | 112 | 0.90 | 1 | 1 | 4,379.50 | 1 |
| Andy Cymrot | 1 | 112 | 0.90 | 1 | 4 | 2,400 | 1 |
| Johnathan Graubart | 2 | 112 | 1.80 | 2 | 3 | 1,089.90 | 2 |
| Irena Garcia | 1 | 112 | 0.90 | 1 | 2 | 797.20 | 1 |

### Q-63_results.md

# Q-63 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r_garcia | 18 | 143 | 13 | 72.20 | 9.10 | 143 | 0 | 0 |
| dhalpern | 19 | 103 | 13 | 68.40 | 12.60 | 97 | 4 | 2 |
| mroman | 17 | 101 | 14 | 82.40 | 13.90 | 101 | 0 | 0 |
| imendoza | 12 | 74 | 0 | 0 | 0 | 59 | 3 | 12 |
| lnagel | 8 | 74 | 5 | 62.50 | 6.80 | 59 | 7 | 8 |
| agavino | 8 | 69 | 1 | 12.50 | 1.40 | 48 | 15 | 6 |
| rgould | 10 | 68 | 1 | 10 | 1.50 | 63 | 4 | 1 |
| bkrieger | 10 | 49 | 5 | 50 | 10.20 | 49 | 0 | 0 |
| lseamon | 4 | 47 | 0 | 0 | 0 | 47 | 0 | 0 |
| steven | 8 | 44 | 0 | 0 | 0 | 44 | 0 | 0 |
| acawley | 9 | 41 | 11 | 122.20 | 26.80 | 41 | 0 | 0 |
| halld | 1 | 31 | 0 | 0 | 0 | 30 | 1 | 0 |
| bsheffield | 5 | 27 | 0 | 0 | 0 | 27 | 0 | 0 |
| murkassoc | 4 | 23 | 1 | 25 | 4.30 | 23 | 0 | 0 |
| jschardar | 3 | 18 | 3 | 100 | 16.70 | 18 | 0 | 0 |
| bbeckermann | 4 | 18 | 3 | 75 | 16.70 | 18 | 0 | 0 |
| jessicam | 3 | 18 | 0 | 0 | 0 | 18 | 0 | 0 |
| jeffizower | 3 | 17 | 2 | 66.70 | 11.80 | 17 | 0 | 0 |
| dunnlighting | 3 | 16 | 2 | 66.70 | 12.50 | 16 | 0 | 0 |
| k_killgore | 2 | 16 | 0 | 0 | 0 | 16 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| halld | 2 | 23 | 3 | 1 | 1 |
| fmorales | 2 | 23 | 1 | 2 | 0 |
| pcladis | 11 | 14.40 | 1.70 | 6 | 1 |
| r_garcia | 50 | 13.90 | 1.80 | 28 | 8 |
| agavino | 24 | 13.70 | 2.30 | 13 | 5 |
| imendoza | 31 | 12.50 | 2.60 | 18 | 2 |
| bbeckermann | 14 | 11.90 | 3.10 | 6 | 4 |
| lnagel | 37 | 10.60 | 2.30 | 14 | 14 |
| mroman | 72 | 9.60 | 2.30 | 31 | 15 |
| bsheffield | 33 | 9.40 | 2 | 17 | 3 |
| kwebb1 | 3 | 8.70 | 1.30 | 2 | 0 |
| dhalpern | 44 | 8.60 | 1.90 | 21 | 10 |
| murkassoc | 14 | 6.70 | 1.80 | 3 | 6 |
| sandy | 2 | 6.50 | 1 | 1 | 0 |
| jeffizower | 8 | 6.50 | 2.40 | 3 | 0 |
| jessicam | 16 | 6.40 | 1.80 | 4 | 4 |
| lseamon | 19 | 6.30 | 2.50 | 3 | 7 |
| steven | 90 | 6.20 | 1.60 | 23 | 34 |
| sschwartz1 | 5 | 6 | 1 | 1 | 2 |
| rabikhalil | 4 | 6 | 2.30 | 1 | 0 |

### Q-65_results.md

# Q-65 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| fmorales | 73 | 64 | 9 | 87.70 | 12.30 |
| r_garcia | 874 | 708 | 166 | 81 | 19 |
| halld | 98 | 76 | 22 | 77.60 | 22.40 |
| jschardar | 131 | 100 | 31 | 76.30 | 23.70 |
| mroman | 1,218 | 876 | 342 | 71.90 | 28.10 |
| jessicam | 138 | 99 | 39 | 71.70 | 28.30 |
| kkepley | 193 | 132 | 61 | 68.40 | 31.60 |
| jeffizower | 84 | 57 | 27 | 67.90 | 32.10 |
| dhalpern | 1,036 | 701 | 335 | 67.70 | 32.30 |
| agavino | 514 | 343 | 171 | 66.70 | 33.30 |
| rgould | 500 | 333 | 167 | 66.60 | 33.40 |
| imendoza | 541 | 359 | 182 | 66.40 | 33.60 |
| bsheffield | 492 | 319 | 173 | 64.80 | 35.20 |
| rabikhalil | 51 | 33 | 18 | 64.70 | 35.30 |
| mmoeller | 24 | 15 | 9 | 62.50 | 37.50 |
| lnagel | 751 | 453 | 298 | 60.30 | 39.70 |
| lseamon | 198 | 119 | 79 | 60.10 | 39.90 |
| abrazhnikov | 60 | 36 | 24 | 60 | 40 |
| bkrieger | 871 | 513 | 358 | 58.90 | 41.10 |
| murkassoc | 365 | 209 | 156 | 57.30 | 42.70 |

### Q-70_results.md

# Q-70 Results — Sarreid, Ltd. (fal, org_id=1)
- **Query**: Q-70 — Inactive Reps with Territory Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — Sarreid, Ltd. (fal, org_id=1)
- **Run date**: 2026-06-17
- **Total flagged**: 0
- **Aggregate GMV**: $0

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### user_group_mapping.md

# User Group Mapping — Sarreid, Ltd. (fal, org_id=1)
- **Run date**: 2026-06-17
- **Total Postgres users**: 144
- **Matched to Mixpanel (Q-01 Step 1)**: 4 of 65 (6%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Rep | other | 53 |
| Sales Assistants | field_rep | 15 |
| Admin | admin_internal | 9 |
| VP - Group | other | 8 |
| Sub Management | other | 7 |
| CSR's | other | 6 |
| z-SuperCat | admin_internal | 6 |
| Dealer - Individual | other | 4 |
| Market Podium | other | 4 |
| Vendor - Arda - 2578 | other | 4 |
| Management - Graphics | other | 3 |
| China - 2623 | other | 2 |
| Management - CEO | admin_internal | 2 |
| Rep No-Disc | field_rep | 2 |
| Sankara-Orders | other | 2 |
| Super Sales | field_rep | 2 |
| Vendor - Italy | other | 2 |
| eOL Public Site | admin_internal | 2 |
| China - MgMt | other | 1 |
| FLS | other | 1 |
| ManageMent Super | other | 1 |
| ManageMent Super | admin_internal | 1 |
| Management - ARS | other | 1 |
| Management - CEO | other | 1 |
| OrderXpert | admin_internal | 1 |
| Rep | admin_internal | 1 |
| Rep - All Disc | field_rep | 1 |
| Sub Rep | other | 1 |
| Vendor - Aria - 1755 | other | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| admin_internal | 4 | 90 | 100.0% |
