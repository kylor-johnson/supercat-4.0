# Section 5 Context Bundle — Savoy House Lighting (shl)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=209029, portal_order_gmv=$50.0M |
| HAS_INVENTORY | True | inventory_count=3139 |
| HAS_SALES_DATA | True | sales_data_count=140638 |
| HAS_SALES_SECTION | True | mode=orders order_reps=18 engagement_reps=0 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | shl_ecat_online |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$50.0M > ecat_gmv=$3.4M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 18 | 18 |
| ENGAGEMENT_REP_COUNT | 0 |  |
| SALES_SECTION_MODE | orders | orders |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 84 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 653, Mixpanel total submit_order (Q-01): 543 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=89.3%, ambiguous_rate=6.7%, showroom_event_share=0.6% |
| USER_GROUP_JOIN_RATE | 89% | 75 of 84 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 1% | showroom+admin share of matched events: 0.6% |
| ADMIN_REPS_IN_LEADERBOARD | True | 1 admin/showroom users in leaderboard: Jessica Romero |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=1139 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=827 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Savoy House Lighting
- **Shortname**: shl
- **Org ID**: 41
- **Bundle**: 6
- **Bundle label for report**: 6

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Savoy House Lighting (shl, org_id=41)
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

# Signal Rank — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Total signals fired**: 59 (P0: 45, P1: 13, P2: 1)
- **Org GMV**: $3.4M eCat LTM, $50.0M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders | P1 | §2 Accounts | 8.3 | $8,268,334 | 2.0 | 136,730,694 | POSITIVE |
| 2 | SIG-ANOMALY-02 | Stock Out — 9-302-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $507,979 LTM, 0 available | P0 | §3 Product | 10.0 | $507,979 | 3.0 | 15,239,379 | RISK |
| 3 | SIG-MOM-01 | Account Acceleration — Shades Of Light 2 consecutive QoQ acceleration quarters, $867,672 peak quarter (+119% QoQ) | P0 | §2 Accounts | 4.0 | $867,672 | 3.0 | 10,333,979 | POSITIVE |
| 4 | SIG-ANOMALY-02 | Stock Out — 1-2221-6-322 (Salerno 6-Light Chandelier in Warm Brass) $303,275 LTM, 0 available | P0 | §3 Product | 10.0 | $303,275 | 3.0 | 9,098,262 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — 7-1804-4-322 (Crawford 4-Light Pendant in Warm Brass) $286,652 LTM, 0 available | P0 | §3 Product | 10.0 | $286,652 | 3.0 | 8,599,568 | RISK |
| 6 | SIG-DECAY-04 | Spending Contraction — Shades Of Light -40.8% YoY ($2,915,999→$1,725,093), $1,190,906 gap | P0 | §2 Accounts | 2.0 | $1,190,906 | 3.0 | 7,288,344 | RISK |
| 7 | SIG-ANOMALY-02 | Stock Out — 7-1774-6-320 (Ashburn 6-Light Pendant in Warm Brass an) $233,394 LTM, 0 available | P0 | §3 Product | 10.0 | $233,394 | 3.0 | 7,001,821 | RISK |
| 8 | SIG-COMMERCE-01 | Digital order enablement — eCat handles 6.8% of $50M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix) | P0 | §4 Commerce | 4.7 | $500,000 | 3.0 | 6,990,000 | POSITIVE |
| 9 | SIG-DECAY-04 | Spending Contraction — Lighting Connection Lp -64.0% YoY ($926,397→$333,632), $592,765 gap | P0 | §2 Accounts | 3.2 | $592,765 | 3.0 | 5,690,545 | RISK |
| 10 | SIG-ANOMALY-02 | Stock Out — 1-312-15-322 (Middleton 15-Light Chandelier in Warm Br) $188,670 LTM, 0 available | P0 | §3 Product | 10.0 | $188,670 | 3.0 | 5,660,094 | RISK |
| 11 | SIG-ANOMALY-02 | Stock Out — 9-303-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $186,435 LTM, 0 available | P0 | §3 Product | 10.0 | $186,435 | 3.0 | 5,593,063 | RISK |
| 12 | SIG-ANOMALY-02 | Stock Out — M60008NB (2-Light Ceiling Light in Natural Brass) $163,303 LTM, 0 available | P0 | §3 Product | 10.0 | $163,303 | 3.0 | 4,899,087 | RISK |
| 13 | SIG-ANOMALY-02 | Stock Out — 9-7144-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $162,681 LTM, 0 available | P0 | §3 Product | 10.0 | $162,681 | 3.0 | 4,880,422 | RISK |
| 14 | SIG-ANOMALY-02 | Stock Out — 7-2918-1-156 (Alta 1-Light Pendant in Concrete and Bra) $147,450 LTM, 0 available | P0 | §3 Product | 10.0 | $147,450 | 3.0 | 4,423,505 | RISK |
| 15 | SIG-ANOMALY-03 | Competitive Displacement — Sunbelt /Mississippi total biz +39% but eCat -83% | P0 | §2 Accounts | 8.1 | $97,748 | 3.0 | 2,387,015 | RISK |
| 16 | SIG-MOM-01 | Account Acceleration — Capital Electric 2 consecutive QoQ acceleration quarters, $43,171 peak quarter (+378% QoQ) | P0 | §2 Accounts | 12.6 | $43,171 | 3.0 | 1,631,423 | POSITIVE |
| 17 | SIG-DECAY-01 | Reorder Decay — Dement Lighting 7.8x normal gap (321d vs 41d avg) | P0 | §2 Accounts | 7.8 | $58,302 | 3.0 | 1,364,267 | RISK |
| 18 | SIG-MOM-01 | Account Acceleration — BELAMI 2 consecutive QoQ acceleration quarters, $271,678 peak quarter (+48% QoQ) | P0 | §2 Accounts | 1.6 | $271,678 | 3.0 | 1,312,206 | POSITIVE |
| 19 | SIG-MOM-01 | Account Acceleration — St Louis Metro Electric 2 consecutive QoQ acceleration quarters, $69,827 peak quarter (+175% QoQ) | P0 | §2 Accounts | 5.8 | $69,827 | 3.0 | 1,221,975 | POSITIVE |
| 20 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 48% of eCat GMV | P1 | §4 Commerce | 1.2 | $410,802 | 2.0 | 995,505 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 35 | 1 | 0 | 36 | |
| §3 Product Intelligence | 9 | 0 | 1 | 10 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §6 Platform Context | 0 | 11 | 0 | 11 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $8.3M+ total business, zero eCat orders
2. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Shades Of Light 2 consecutive QoQ acceleration quarters, $867,672 peak quarter (+119% QoQ)
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Digital order enablement — eCat handles 6.8% of $50M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix)
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Capital Electric 2 consecutive QoQ acceleration quarters, $43,171 peak quarter (+378% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — 9-302-1-322 (Monroe 1-Light Wall Sconce in Warm Brass) $507,979 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — 1-2221-6-322 (Salerno 6-Light Chandelier in Warm Brass) $303,275 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 7-1804-4-322 (Crawford 4-Light Pendant in Warm Brass) $286,652 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### coaching_candidates.md

# Coaching Candidates — Savoy House Lighting (shl)

Deterministically computed by detect_signals.py. The section agent renders
these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,
or add reps. Archetype framing + narrative are written by the agent; the rep
set and the estimated upside dollar figures are fixed here.

- **Benchmark**: n/a
- **Qualifying reps (>= 50 presentations)**: 10 (0 converting)
- **Upside floor**: $50,000
- **Candidates above floor**: 0

**No coaching cards for this client — render NO coaching cards and NO coaching rollup callout.** Reason: No qualifying rep converts (>0%) — no benchmark to measure against.

### Q-01_step1_results.md

# Q-01-S1 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 84
- **Run date**: 2026-06-17


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kelley | 408 | 10,381 | 2024-11-01 09:38 | 2026-06-17 16:02 | 1,594 | 549 | 1,045 | 6,323 | 6,281 | 42 | 0 | 0 | 0 | 0 | 17 | 10 | 6 | 1 | 442 | 435 | 226 | 5 | 0 | 0 | 1 | 2 | 39 |
| wfalk1 | 346 | 6,001 | 2024-11-01 09:21 | 2026-06-17 16:12 | 871 | 159 | 712 | 1,929 | 1,919 | 10 | 0 | 0 | 0 | 0 | 54 | 4 | 50 | 0 | 433 | 426 | 14 | 124 | 0 | 0 | 32 | 13 | 24 |
| shellym | 359 | 5,316 | 2024-11-04 09:15 | 2026-06-17 18:14 | 1,621 | 448 | 1,173 | 1,725 | 1,629 | 69 | 0 | 0 | 0 | 0 | 42 | 21 | 21 | 0 | 102 | 94 | 5 | 23 | 0 | 0 | 36 | 19 | 22 |
| dakotaluxeco | 245 | 4,771 | 2024-11-07 10:33 | 2026-06-17 17:02 | 606 | 178 | 428 | 2,477 | 2,452 | 25 | 0 | 0 | 0 | 0 | 77 | 1 | 76 | 0 | 189 | 187 | 31 | 7 | 0 | 0 | 9 | 14 | 21 |
| toddt | 205 | 4,316 | 2024-11-01 09:34 | 2026-06-16 10:04 | 705 | 273 | 432 | 545 | 506 | 38 | 0 | 0 | 0 | 0 | 32 | 6 | 25 | 1 | 58 | 55 | 31 | 7 | 0 | 0 | 8 | 17 | 25 |
| adams | 122 | 4,304 | 2024-11-05 12:31 | 2026-03-22 13:42 | 222 | 88 | 134 | 1,135 | 994 | 141 | 0 | 0 | 0 | 0 | 163 | 0 | 160 | 3 | 45 | 45 | 16 | 372 | 0 | 2 | 3 | 20 | 17 |
| marym | 170 | 4,246 | 2024-12-20 07:00 | 2026-05-22 11:12 | 600 | 252 | 348 | 2,719 | 2,668 | 51 | 0 | 0 | 0 | 0 | 11 | 0 | 11 | 0 | 179 | 179 | 30 | 12 | 0 | 0 | 3 | 2 | 30 |
| libbyh | 225 | 3,958 | 2024-11-01 16:13 | 2026-06-17 17:55 | 315 | 136 | 179 | 766 | 692 | 74 | 0 | 0 | 0 | 0 | 55 | 9 | 43 | 3 | 317 | 317 | 13 | 44 | 0 | 1 | 8 | 15 | 2 |
| gpassmore | 248 | 3,919 | 2024-11-04 13:19 | 2026-06-11 20:14 | 603 | 223 | 380 | 1,321 | 1,298 | 23 | 0 | 0 | 0 | 0 | 85 | 0 | 85 | 0 | 411 | 385 | 30 | 39 | 0 | 1 | 4 | 17 | 15 |
| jeffb | 305 | 3,823 | 2024-11-01 13:11 | 2026-06-17 11:56 | 44 | 43 | 1 | 953 | 920 | 33 | 0 | 0 | 0 | 0 | 73 | 41 | 32 | 0 | 723 | 689 | 19 | 110 | 0 | 0 | 2 | 4 | 15 |
| grillocs | 357 | 3,729 | 2024-11-01 08:01 | 2026-06-17 09:18 | 1,364 | 489 | 875 | 1,205 | 1,200 | 4 | 0 | 0 | 0 | 0 | 5 | 0 | 3 | 2 | 20 | 20 | 0 | 10 | 0 | 0 | 1 | 12 | 0 |
| kgrillo | 251 | 3,684 | 2024-11-01 09:13 | 2026-06-16 17:45 | 452 | 216 | 236 | 502 | 421 | 81 | 0 | 0 | 0 | 0 | 110 | 0 | 110 | 0 | 1,003 | 1,000 | 2 | 178 | 0 | 0 | 6 | 32 | 13 |
| larosa | 256 | 3,665 | 2024-11-04 10:16 | 2026-06-17 10:56 | 325 | 236 | 89 | 1,727 | 1,636 | 87 | 0 | 0 | 0 | 0 | 53 | 10 | 43 | 0 | 452 | 448 | 25 | 2 | 0 | 0 | 19 | 24 | 10 |
| starrylightssupport | 241 | 3,629 | 2024-11-01 14:19 | 2026-06-16 08:37 | 578 | 231 | 347 | 1,647 | 1,626 | 21 | 0 | 0 | 0 | 0 | 36 | 5 | 31 | 0 | 140 | 136 | 12 | 30 | 0 | 1 | 2 | 25 | 14 |
| bjferber | 169 | 3,387 | 2024-11-04 10:11 | 2025-08-28 16:04 | 193 | 177 | 16 | 1,769 | 1,764 | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 479 | 441 | 7 | 5 | 0 | 0 | 0 | 1 | 15 |
| jenmccarty | 196 | 3,276 | 2025-06-16 14:40 | 2026-06-16 14:39 | 28 | 28 | 0 | 348 | 332 | 16 | 0 | 0 | 0 | 0 | 130 | 4 | 119 | 4 | 522 | 521 | 99 | 269 | 0 | 5 | 2 | 5 | 1 |
| jgannon | 216 | 2,892 | 2024-11-03 15:14 | 2026-06-17 11:53 | 343 | 112 | 231 | 748 | 724 | 24 | 0 | 0 | 0 | 0 | 14 | 7 | 3 | 4 | 1,028 | 1,018 | 7 | 19 | 0 | 0 | 10 | 26 | 12 |
| rjazimi | 164 | 2,828 | 2024-11-04 09:42 | 2026-06-10 11:37 | 233 | 123 | 110 | 1,357 | 1,288 | 66 | 0 | 0 | 0 | 0 | 27 | 1 | 26 | 0 | 159 | 150 | 22 | 21 | 0 | 0 | 9 | 67 | 12 |
| bbuntz | 138 | 2,744 | 2024-11-07 11:07 | 2026-06-17 14:05 | 92 | 92 | 0 | 837 | 827 | 10 | 0 | 0 | 0 | 0 | 10 | 0 | 4 | 6 | 91 | 90 | 8 | 14 | 0 | 1 | 3 | 23 | 13 |
| jerrysharp | 280 | 2,563 | 2024-11-08 17:01 | 2026-06-17 15:09 | 155 | 56 | 99 | 763 | 707 | 55 | 0 | 0 | 0 | 0 | 44 | 27 | 16 | 1 | 83 | 59 | 102 | 90 | 0 | 2 | 1 | 10 | 10 |
| jmckinley | 165 | 2,463 | 2024-11-11 09:17 | 2026-06-17 15:06 | 151 | 49 | 102 | 411 | 398 | 13 | 0 | 0 | 0 | 0 | 15 | 2 | 12 | 1 | 947 | 947 | 5 | 13 | 0 | 0 | 2 | 2 | 9 |
| kgannon | 198 | 2,163 | 2024-11-04 09:20 | 2026-06-16 11:25 | 102 | 82 | 20 | 501 | 490 | 11 | 0 | 0 | 0 | 0 | 29 | 27 | 1 | 1 | 707 | 641 | 11 | 11 | 0 | 0 | 0 | 7 | 11 |
| lbelesky | 210 | 2,158 | 2025-02-05 18:46 | 2026-06-17 16:25 | 355 | 127 | 228 | 494 | 477 | 13 | 0 | 0 | 0 | 0 | 33 | 6 | 27 | 0 | 144 | 140 | 41 | 73 | 0 | 0 | 6 | 16 | 16 |
| tomwright | 258 | 2,108 | 2024-11-02 10:06 | 2026-06-17 21:57 | 125 | 119 | 6 | 1,162 | 168 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 67 | 55 | 14 | 0 | 0 | 0 | 0 | 21 | 20 |
| altonm | 103 | 2,081 | 2024-11-04 13:08 | 2026-06-17 16:36 | 295 | 91 | 204 | 1,269 | 1,238 | 31 | 0 | 0 | 0 | 0 | 12 | 5 | 7 | 0 | 23 | 19 | 10 | 7 | 0 | 0 | 6 | 1 | 20 |
| charliek | 259 | 2,005 | 2024-11-04 12:05 | 2026-06-17 07:32 | 148 | 116 | 32 | 782 | 782 | 0 | 0 | 0 | 0 | 0 | 24 | 0 | 24 | 0 | 140 | 139 | 2 | 15 | 0 | 0 | 0 | 8 | 1 |
| trevl | 214 | 1,930 | 2024-11-04 12:17 | 2026-06-16 15:22 | 268 | 115 | 153 | 581 | 558 | 23 | 0 | 0 | 0 | 0 | 11 | 0 | 11 | 0 | 414 | 414 | 30 | 10 | 0 | 0 | 6 | 32 | 13 |
| bgrillo | 223 | 1,724 | 2024-11-01 14:58 | 2026-06-17 14:26 | 144 | 95 | 49 | 397 | 338 | 59 | 0 | 0 | 0 | 0 | 31 | 0 | 31 | 0 | 171 | 165 | 11 | 82 | 0 | 0 | 0 | 7 | 2 |
| martinb | 177 | 1,677 | 2024-11-01 10:47 | 2026-06-17 16:30 | 97 | 85 | 12 | 1,032 | 1,031 | 1 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | 1 | 46 | 46 | 0 | 3 | 0 | 0 | 0 | 5 | 14 |
| stevens | 150 | 1,646 | 2024-11-05 06:08 | 2026-06-11 14:48 | 541 | 126 | 415 | 451 | 447 | 4 | 0 | 0 | 0 | 0 | 4 | 3 | 1 | 0 | 134 | 127 | 0 | 4 | 0 | 0 | 7 | 17 | 14 |
| hmeador | 139 | 1,337 | 2024-11-04 12:40 | 2026-06-17 17:38 | 160 | 70 | 90 | 363 | 362 | 1 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 237 | 237 | 2 | 7 | 0 | 0 | 0 | 1 | 9 |
| brittainc | 149 | 1,320 | 2024-11-05 17:08 | 2026-06-02 18:16 | 38 | 32 | 6 | 299 | 243 | 56 | 0 | 0 | 0 | 0 | 23 | 1 | 22 | 0 | 172 | 171 | 20 | 3 | 0 | 0 | 2 | 1 | 9 |
| bdobson | 100 | 1,218 | 2025-06-02 17:31 | 2026-06-02 12:30 | 126 | 51 | 75 | 326 | 326 | 0 | 0 | 0 | 0 | 0 | 26 | 2 | 24 | 0 | 232 | 198 | 24 | 1 | 0 | 0 | 0 | 0 | 8 |
| kphelps | 81 | 1,166 | 2024-11-05 11:18 | 2025-08-27 14:21 | 138 | 39 | 99 | 253 | 232 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100 | 100 | 3 | 0 | 0 | 0 | 0 | 1 | 10 |
| kelsyej | 44 | 1,002 | 2024-12-09 15:13 | 2026-01-11 16:42 | 172 | 26 | 146 | 304 | 297 | 7 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 41 | 41 | 3 | 49 | 0 | 4 | 1 | 1 | 1 |
| matt | 51 | 992 | 2024-11-20 15:44 | 2026-06-17 00:11 | 100 | 97 | 3 | 123 | 120 | 3 | 0 | 0 | 0 | 0 | 11 | 1 | 10 | 0 | 10 | 10 | 5 | 23 | 0 | 0 | 0 | 1 | 18 |
| ccollier | 49 | 921 | 2025-01-07 10:05 | 2026-06-15 08:43 | 96 | 83 | 13 | 178 | 174 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 85 | 75 | 5 | 0 | 0 | 0 | 6 | 59 | 10 |
| tblount5 | 8 | 896 | 2025-01-30 12:31 | 2025-06-17 08:13 | 51 | 21 | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 0 | 0 | 6 | 7 |
| davidwinters | 63 | 882 | 2024-12-21 22:28 | 2026-06-16 14:25 | 46 | 29 | 17 | 140 | 119 | 21 | 0 | 0 | 0 | 0 | 17 | 0 | 17 | 0 | 480 | 475 | 8 | 6 | 0 | 0 | 0 | 7 | 2 |
| jdurbin | 19 | 865 | 2025-12-30 16:21 | 2026-02-24 15:38 | 78 | 39 | 39 | 607 | 603 | 4 | 0 | 0 | 0 | 0 | 16 | 0 | 16 | 0 | 18 | 18 | 2 | 4 | 0 | 0 | 0 | 0 | 3 |

*(Truncated: showing top 40 of 84 rows. Full data in cache file.)*

### Q-01_step2_results.md

# Q-01-S2 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 44
- **Run date**: 2026-06-17


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Mary McKey | 25 | $239,379 | $9,575 | 10 |
| Rob Azimi | 10 | $180,002 | $18,000 | 8 |
| Tom Wright | 13 | $170,223 | $13,094 | 7 |
| Dakota Duffield | 19 | $170,197 | $8,958 | 17 |
| Alton Mckey | 11 | $167,286 | $15,208 | 7 |
| Keeley - Luxeco  Jackson | 15 | $159,799 | $10,653 | 10 |
| Matt Rowland | 12 | $130,736 | $10,895 | 8 |
| Kathy Phelps | 7 | $125,520 | $17,931 | 6 |
| Todd Tuchfarber | 23 | $121,396 | $5,278 | 17 |
| Shelly Meshwork | 13 | $116,471 | $8,959 | 11 |
| Jessica Romero | 16 | $111,123 | $6,945 | 10 |
| Jeff Brose | 11 | $104,911 | $9,537 | 10 |
| Adams Smith | 10 | $103,459 | $10,346 | 9 |
| Customer Support | 10 | $102,885 | $10,288 | 9 |
| Cheryl LaRosa | 10 | $99,773 | $9,977 | 8 |
| Martin Blackley | 7 | $96,461 | $13,780 | 5 |
| Wayne Falk | 12 | $84,906 | $7,075 | 6 |
| Steven Shneer | 8 | $83,265 | $10,408 | 4 |
| Brittain Cherry | 8 | $72,269 | $9,034 | 6 |
| Brad Dobson | 9 | $70,121 | $7,791 | 8 |
| Keeley Jackson | 7 | $65,305 | $9,329 | 5 |
| Julie Gannon | 6 | $58,540 | $9,757 | 4 |
| Chris Collier | 11 | $57,884 | $5,262 | 6 |
| Trevor Lindsay | 12 | $57,864 | $4,822 | 7 |
| Jonathan McKinley | 4 | $52,688 | $13,172 | 4 |
| Lisa Belesky | 20 | $50,167 | $2,508 | 10 |
| BJ Ferber | 7 | $42,776 | $6,111 | 1 |
| Cimera Wilson | 3 | $40,483 | $13,494 | 3 |
| Ken Grillo | 6 | $39,028 | $6,505 | 6 |
| Brad Buntz | 6 | $38,930 | $6,488 | 5 |
| Heather Meador | 3 | $38,286 | $12,762 | 3 |
| Garrett Passmore | 5 | $34,506 | $6,901 | 4 |
| Jace Durbin | 3 | $28,887 | $9,629 | 3 |
| Jerry Sharp | 6 | $23,763 | $3,960 | 4 |
| Kevin Gannon | 4 | $21,328 | $5,332 | 4 |
| Tyler Ridgeway | 2 | $18,516 | $9,258 | 2 |
| Kevin Blackley | 3 | $14,404 | $4,801 | 2 |
| James McDowall | 1 | $10,555 | $10,555 | 1 |
| David Winters | 2 | $6,454 | $3,227 | 2 |
| Kris Roach | 1 | $5,512 | $5,512 | 1 |
| Jenifer McCarty | 2 | $3,227 | $1,613 | 2 |
| Grillo Customer Service | 5 | $1,841 | $368 | 1 |
| Amin Khan | 1 | $1,763 | $1,763 | 1 |
| Kelly Burton | 1 | $1,707 | $1,707 | 1 |

### Q-04_results.md

# Q-04 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 84
- **Run date**: 2026-06-17


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kelley | 408 | 10,381 | 39 | 6,281 | 435 | 7 | 6 | 0 | 226 | 5 | Selling Rep |
| wfalk1 | 346 | 6,001 | 24 | 1,919 | 426 | 7 | 50 | 0 | 14 | 124 | Selling Rep |
| shellym | 359 | 5,316 | 22 | 1,629 | 94 | 8 | 21 | 0 | 5 | 23 | Selling Rep |
| dakotaluxeco | 245 | 4,771 | 21 | 2,452 | 187 | 2 | 76 | 0 | 31 | 7 | Selling Rep |
| toddt | 205 | 4,316 | 25 | 506 | 55 | 3 | 25 | 0 | 31 | 7 | Selling Rep |
| adams | 122 | 4,304 | 17 | 994 | 45 | 0 | 160 | 0 | 16 | 374 | Selling Rep |
| marym | 170 | 4,246 | 30 | 2,668 | 179 | 0 | 11 | 0 | 30 | 12 | Selling Rep |
| libbyh | 225 | 3,958 | 2 | 692 | 317 | 0 | 43 | 0 | 13 | 45 | Content/Library Manager |
| gpassmore | 248 | 3,919 | 15 | 1,298 | 385 | 26 | 85 | 0 | 30 | 40 | Selling Rep |
| jeffb | 305 | 3,823 | 15 | 920 | 689 | 34 | 32 | 0 | 19 | 110 | Selling Rep |
| grillocs | 357 | 3,729 | 0 | 1,200 | 20 | 0 | 3 | 0 | 0 | 10 | Sales Support/Inside Sales |
| kgrillo | 251 | 3,684 | 13 | 421 | 1,000 | 3 | 110 | 0 | 2 | 178 | Selling Rep |
| larosa | 256 | 3,665 | 10 | 1,636 | 448 | 4 | 43 | 0 | 25 | 2 | Selling Rep |
| starrylightssupport | 241 | 3,629 | 14 | 1,626 | 136 | 4 | 31 | 0 | 12 | 31 | Selling Rep |
| bjferber | 169 | 3,387 | 15 | 1,764 | 441 | 38 | 0 | 0 | 7 | 5 | Selling Rep |
| jenmccarty | 196 | 3,276 | 1 | 332 | 521 | 1 | 119 | 3 | 99 | 274 | Content/Library Manager |
| jgannon | 216 | 2,892 | 12 | 724 | 1,018 | 10 | 3 | 0 | 7 | 19 | Selling Rep |
| rjazimi | 164 | 2,828 | 12 | 1,288 | 150 | 9 | 26 | 0 | 22 | 21 | Selling Rep |
| bbuntz | 138 | 2,744 | 13 | 827 | 90 | 1 | 4 | 0 | 8 | 15 | Selling Rep |
| jerrysharp | 280 | 2,563 | 10 | 707 | 59 | 24 | 16 | 0 | 102 | 92 | Selling Rep |
| jmckinley | 165 | 2,463 | 9 | 398 | 947 | 0 | 12 | 0 | 5 | 13 | Selling Rep |
| kgannon | 198 | 2,163 | 11 | 490 | 641 | 66 | 1 | 0 | 11 | 11 | Selling Rep |
| lbelesky | 210 | 2,158 | 16 | 477 | 140 | 4 | 27 | 0 | 41 | 73 | Selling Rep |
| tomwright | 258 | 2,108 | 20 | 168 | 55 | 12 | 0 | 0 | 14 | 0 | Selling Rep |
| altonm | 103 | 2,081 | 20 | 1,238 | 19 | 4 | 7 | 0 | 10 | 7 | Selling Rep |
| charliek | 259 | 2,005 | 1 | 782 | 139 | 1 | 24 | 0 | 2 | 15 | Catalog/Data Manager |
| trevl | 214 | 1,930 | 13 | 558 | 414 | 0 | 11 | 0 | 30 | 10 | Selling Rep |
| bgrillo | 223 | 1,724 | 2 | 338 | 165 | 6 | 31 | 0 | 11 | 82 | Catalog/Data Manager |
| martinb | 177 | 1,677 | 14 | 1,031 | 46 | 0 | 0 | 0 | 0 | 3 | Selling Rep |
| stevens | 150 | 1,646 | 14 | 447 | 127 | 7 | 1 | 0 | 0 | 4 | Selling Rep |
| hmeador | 139 | 1,337 | 9 | 362 | 237 | 0 | 3 | 0 | 2 | 7 | Selling Rep |
| brittainc | 149 | 1,320 | 9 | 243 | 171 | 1 | 22 | 0 | 20 | 3 | Selling Rep |
| bdobson | 100 | 1,218 | 8 | 326 | 198 | 34 | 24 | 0 | 24 | 1 | Selling Rep |
| kphelps | 81 | 1,166 | 10 | 232 | 100 | 0 | 0 | 0 | 3 | 0 | Selling Rep |
| kelsyej | 44 | 1,002 | 1 | 297 | 41 | 0 | 4 | 0 | 3 | 53 | Merchandising/List Curator |
| matt | 51 | 992 | 18 | 120 | 10 | 0 | 10 | 0 | 5 | 23 | Selling Rep |
| ccollier | 49 | 921 | 10 | 174 | 75 | 10 | 1 | 0 | 5 | 0 | Selling Rep |
| tblount5 | 8 | 896 | 7 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | Selling Rep |
| davidwinters | 63 | 882 | 2 | 119 | 475 | 5 | 17 | 0 | 8 | 6 | Content/Library Manager |
| jdurbin | 19 | 865 | 3 | 603 | 18 | 0 | 16 | 0 | 2 | 4 | Selling Rep |
| zrapp | 53 | 827 | 0 | 158 | 164 | 13 | 2 | 0 | 65 | 3 | Sales Support/Inside Sales |
| tridgway | 47 | 651 | 3 | 353 | 70 | 0 | 2 | 0 | 1 | 1 | Selling Rep |
| krisroach | 35 | 595 | 2 | 45 | 23 | 0 | 0 | 0 | 5 | 21 | Sales Support/Inside Sales |
| kblackley1 | 64 | 557 | 5 | 312 | 49 | 0 | 0 | 0 | 1 | 0 | Selling Rep |
| katiewilliams | 34 | 517 | 0 | 154 | 61 | 0 | 6 | 0 | 6 | 4 | Sales Support/Inside Sales |
| lbellanti | 29 | 494 | 0 | 10 | 408 | 0 | 0 | 0 | 1 | 0 | Content/Library Manager |
| aminkhan | 76 | 450 | 3 | 83 | 27 | 7 | 0 | 0 | 6 | 1 | Selling Rep |
| gsharp1 | 51 | 433 | 0 | 9 | 139 | 2 | 0 | 0 | 2 | 0 | Low-Activity User |
| jessicar | 28 | 428 | 8 | 147 | 7 | 0 | 0 | 0 | 13 | 0 | Selling Rep |
| sourceltg | 26 | 387 | 0 | 162 | 0 | 0 | 7 | 0 | 2 | 10 | Inactive |
| jmcdowall | 50 | 362 | 0 | 135 | 54 | 5 | 5 | 0 | 3 | 1 | Low-Activity User |
| jessp | 5 | 342 | 4 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Selling Rep |
| barbaraj | 71 | 279 | 2 | 44 | 12 | 0 | 0 | 0 | 3 | 0 | Low-Activity User |
| ccoxworth | 14 | 271 | 0 | 42 | 177 | 11 | 0 | 0 | 0 | 0 | Inactive |
| cimera | 7 | 241 | 3 | 132 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| cgecowets | 33 | 233 | 0 | 22 | 63 | 0 | 6 | 0 | 0 | 0 | Low-Activity User |
| mikebush | 32 | 186 | 0 | 15 | 0 | 0 | 35 | 0 | 8 | 0 | Catalog/Data Manager |
| nickmansfield | 5 | 170 | 0 | 105 | 0 | 0 | 12 | 0 | 0 | 22 | Inactive |
| cmagana | 14 | 122 | 0 | 43 | 26 | 0 | 0 | 0 | 1 | 0 | Inactive |
| jedson | 53 | 118 | 0 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | Low-Activity User |
| starrylights | 13 | 114 | 4 | 42 | 9 | 0 | 0 | 0 | 2 | 0 | Selling Rep |
| rolandh | 27 | 105 | 0 | 20 | 20 | 0 | 0 | 0 | 1 | 0 | Inactive |
| brianm | 7 | 102 | 2 | 48 | 4 | 0 | 0 | 0 | 1 | 0 | Inactive |
| peterz | 11 | 70 | 0 | 36 | 0 | 0 | 0 | 0 | 4 | 0 | Inactive |
| brianmayer | 4 | 48 | 0 | 0 | 29 | 0 | 0 | 0 | 0 | 0 | Inactive |
| khale1 | 12 | 44 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dvaccaroiscool | 5 | 38 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | 0 | Inactive |
| oxshl | 21 | 35 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| ctwigg | 5 | 28 | 0 | 9 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| layla_c | 8 | 23 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| codyadler | 2 | 20 | 0 | 0 | 16 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jgardnersavoy | 1 | 19 | 0 | 0 | 0 | 0 | 8 | 0 | 1 | 0 | Inactive |
| katyrumford | 3 | 15 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| lcarmichael | 6 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| derich | 1 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dougy | 2 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 1 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dszekely | 3 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| swt | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| ttitizian2 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jstarry | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kjael | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| markp | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 251 | 51 | 45 |

### Q-06_results.md

# Q-06 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 60
- **Run date**: 2026-06-17


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Lisa Belesky | 92 | 50 | -45.70 | 6 | 4 | -33.30 | $5,059 |
| Tom Wright | 73 | 41 | -43.80 | 9 | 2 | -77.80 | $1,250 |
| Brad Dobson | 48 | 20 | -58.30 | 5 | 1 | -80 | $3,374 |
| Matt Rowland | 20 | 4 | -80 | 12 | 0 | -100 | $0 |
| David Winters | 25 | 6 | -76 | 2 | 0 | -100 | $0 |
| Brittain Cherry | 56 | 15 | -73.20 | 7 | 0 | -100 | $0 |
| Jonathan McKinley | 56 | 21 | -62.50 | 4 | 0 | -100 | $0 |
| Jeff Brose | 126 | 109 | -13.50 | 11 | 0 | -100 | $0 |
| Julie Gannon | 68 | 43 | -36.80 | 5 | 0 | -100 | $0 |
| Kris Roach | 8 | 6 | -25 | 1 | 0 | -100 | $0 |
| Mary McKey | 113 | 42 | -62.80 | 16 | 0 | -100 | $0 |
| Martin Blackley | 59 | 13 | -78 | 4 | 0 | -100 | $0 |
| Kevin Blackley | 22 | 4 | -81.80 | 3 | 0 | -100 | $0 |
| Rob Azimi | 64 | 43 | -32.80 | 7 | 0 | -100 | $0 |
| Chris Collier | 19 | 15 | -21.10 | 7 | 0 | -100 | $0 |
| Customer Support | 91 | 55 | -39.60 | 10 | 0 | -100 | $0 |
| Garrett Passmore | 74 | 19 | -74.30 | 4 | 0 | -100 | $0 |
| Wayne Falk | 153 | 199 | 30.10 | 7 | 0 | -100 | $0 |
| Jenifer McCarty | 111 | 93 | -16.20 | 1 | 0 | -100 | $0 |
| Ken Grillo | 83 | 76 | -8.40 | 6 | 0 | -100 | $0 |
| Jerry Sharp | 84 | 82 | -2.40 | 5 | 0 | -100 | $0 |
| Dakota Duffield | 66 | 83 | 25.80 | 14 | 0 | -100 | $0 |
| Todd Tuchfarber | 123 | 36 | -70.70 | 16 | 0 | -100 | $0 |
| Shelly Meshwork | 146 | 111 | -24 | 13 | 0 | -100 | $0 |
| Cimera Wilson | 5 | 0 | -100 | 3 | 0 | -100 | $0 |
| Keeley - Luxeco  Jackson | 152 | 131 | -13.80 | 15 | 0 | -100 | $0 |
| Adams Smith | 35 | 1 | -97.10 | 5 | 0 | -100 | $0 |
| Jessica Romero | 20 | 2 | -90 | 16 | 0 | -100 | $0 |
| Cheryl LaRosa | 114 | 89 | -21.90 | 6 | 0 | -100 | $0 |
| Kevin Gannon | 76 | 42 | -44.70 | 3 | 0 | -100 | $0 |
| Heather Meador | 45 | 26 | -42.20 | 2 | 0 | -100 | $0 |
| James McDowall | 22 | 20 | -9.10 | 1 | 0 | -100 | $0 |
| Brad Buntz | 36 | 30 | -16.70 | 3 | 0 | -100 | $0 |
| Alton Mckey | 29 | 17 | -41.40 | 8 | 0 | -100 | $0 |
| Steven Shneer | 52 | 49 | -5.80 | 8 | 0 | -100 | $0 |
| Amin Khan | 30 | 11 | -63.30 | 1 | 0 | -100 | $0 |
| Jace Durbin | 47 | 0 | -100 | 3 | 0 | -100 | $0 |
| Trevor Lindsay | 59 | 35 | -40.70 | 7 | 0 | -100 | $0 |
| Chris Twigg | 2 | 0 | -100 | — | — | — | — |
| Libby Hancock | 68 | 33 | -51.50 | — | — | — | — |
| Cynthia  Magana  | 6 | 10 | 66.70 | — | — | — | — |
| Lisa Carmichael | 2 | 0 | -100 | — | — | — | — |
| Roland Huang | 9 | 0 | -100 | — | — | — | — |
| Nick Mansfield | 4 | 0 | -100 | — | — | — | — |
| Kelsye  Jones | 13 | 0 | -100 | — | — | — | — |
| Katie Williams | 47 | 16 | -66 | — | — | — | — |
| Brent Sanders | 3 | 0 | -100 | — | — | — | — |
| John Edson | 10 | 8 | -20 | — | — | — | — |
| Grillo Customer Service | 101 | 157 | 55.40 | — | — | — | — |
| Carole Gecowets | 12 | 23 | 91.70 | — | — | — | — |
| Jerry Starry | 3 | 0 | -100 | — | — | — | — |
| Brian Mayer | 0 | 5 | — | — | — | — | — |
| Beto Grillo | 85 | 65 | -23.50 | — | — | — | — |
| Lina Bellanti | 2 | 11 | 450 | — | — | — | — |
| Kelly Burton | 2 | 5 | 150 | — | — | — | — |
| Mike Bush | 6 | 11 | 83.30 | — | — | — | — |
| Greg Sharp | 41 | 17 | -58.50 | — | — | — | — |
| Charlie Kissel | 85 | 52 | -38.80 | — | — | — | — |
| Zachary Rapp | 0 | 138 | — | — | — | — | — |
| Dana Vaccaro | 0 | 3 | — | — | — | — | — |

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-43_results.md

(not present — file does not exist or is empty)

### Q-43_step2_results.md

# Q-43-S2 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-51_results.md

(not present — file does not exist or is empty)

### Q-62_results.md

# Q-62 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-63_results.md

# Q-63 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| shellym | 11 | 310 | 0 | 0 | 0 | 304 | 5 | 1 |
| bbuntz | 2 | 183 | 0 | 0 | 0 | 183 | 0 | 0 |
| marym | 5 | 167 | 0 | 0 | 0 | 167 | 0 | 0 |
| wfalk1 | 6 | 142 | 0 | 0 | 0 | 140 | 2 | 0 |
| kelley | 11 | 128 | 0 | 0 | 0 | 128 | 0 | 0 |
| dakotaluxeco | 11 | 117 | 0 | 0 | 0 | 102 | 15 | 0 |
| larosa | 6 | 113 | 0 | 0 | 0 | 108 | 5 | 0 |
| grillocs | 11 | 105 | 0 | 0 | 0 | 105 | 0 | 0 |
| starrylightssupport | 10 | 94 | 0 | 0 | 0 | 94 | 0 | 0 |
| trevl | 5 | 54 | 0 | 0 | 0 | 54 | 0 | 0 |
| kgrillo | 6 | 46 | 0 | 0 | 0 | 38 | 8 | 0 |
| bdobson | 3 | 40 | 0 | 0 | 0 | 39 | 1 | 0 |
| rjazimi | 2 | 34 | 0 | 0 | 0 | 33 | 1 | 0 |
| lbelesky | 3 | 34 | 0 | 0 | 0 | 32 | 2 | 0 |
| stevens | 3 | 27 | 0 | 0 | 0 | 27 | 0 | 0 |
| sourceltg | 2 | 27 | 0 | 0 | 0 | 27 | 0 | 0 |
| jgannon | 3 | 25 | 0 | 0 | 0 | 24 | 0 | 1 |
| toddt | 4 | 19 | 0 | 0 | 0 | 19 | 0 | 0 |
| zrapp | 3 | 19 | 0 | 0 | 0 | 16 | 2 | 1 |
| gpassmore | 2 | 17 | 0 | 0 | 0 | 17 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| bbuntz | 4 | 48.80 | 1.80 | 1 | 2 |
| bgrillo | 3 | 46.30 | 4.30 | 1 | 0 |
| kgrillo | 13 | 42.30 | 2 | 6 | 4 |
| toddt | 7 | 26 | 1 | 5 | 0 |
| gsharp1 | 1 | 19 | 1 | 1 | 0 |
| dakotaluxeco | 23 | 17.70 | 2.50 | 14 | 3 |
| lbellanti | 5 | 15.40 | 1.80 | 2 | 3 |
| kelley | 29 | 15.20 | 2.40 | 17 | 3 |
| martinb | 1 | 15 | 1 | 1 | 0 |
| shellym | 47 | 14 | 2.10 | 14 | 12 |
| jgannon | 10 | 13.60 | 1.30 | 3 | 4 |
| marym | 19 | 13 | 1.40 | 6 | 9 |
| rjazimi | 15 | 12.70 | 1.50 | 6 | 6 |
| wfalk1 | 19 | 12.60 | 1.10 | 7 | 8 |
| larosa | 18 | 12.20 | 2.30 | 6 | 4 |
| jerrysharp | 2 | 11 | 2.50 | 1 | 1 |
| sourceltg | 3 | 10.70 | 1 | 2 | 0 |
| trevl | 19 | 10.60 | 1.60 | 7 | 4 |
| starrylightssupport | 20 | 9.30 | 1.90 | 7 | 2 |
| bdobson | 6 | 9.20 | 1.30 | 2 | 2 |

### Q-65_results.md

# Q-65 Results — Savoy House Lighting (shl, org_id=41)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| bbuntz | 393 | 333 | 60 | 84.70 | 15.30 |
| sourceltg | 45 | 37 | 8 | 82.20 | 17.80 |
| stevens | 250 | 169 | 81 | 67.60 | 32.40 |
| grillocs | 496 | 315 | 181 | 63.50 | 36.50 |
| marym | 487 | 309 | 178 | 63.40 | 36.60 |
| shellym | 972 | 612 | 360 | 63 | 37 |
| starrylightssupport | 316 | 190 | 126 | 60.10 | 39.90 |
| bdobson | 138 | 74 | 64 | 53.60 | 46.40 |
| dakotaluxeco | 643 | 333 | 310 | 51.80 | 48.20 |
| wfalk1 | 1,418 | 670 | 748 | 47.20 | 52.80 |
| aminkhan | 34 | 16 | 18 | 47.10 | 52.90 |
| kelley | 624 | 288 | 336 | 46.20 | 53.80 |
| larosa | 656 | 279 | 377 | 42.50 | 57.50 |
| cmagana | 48 | 20 | 28 | 41.70 | 58.30 |
| lbelesky | 277 | 111 | 166 | 40.10 | 59.90 |
| trevl | 235 | 92 | 143 | 39.10 | 60.90 |
| martinb | 45 | 17 | 28 | 37.80 | 62.20 |
| charliek | 143 | 54 | 89 | 37.80 | 62.20 |
| gpassmore | 118 | 43 | 75 | 36.40 | 63.60 |
| jerrysharp | 322 | 117 | 205 | 36.30 | 63.70 |

### Q-70_results.md

(not present — file does not exist or is empty)

### showroom_scan_results.md

# Showroom Scan Results — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Total flagged**: 0
- **Aggregate GMV**: $0

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### user_group_mapping.md

# User Group Mapping — Savoy House Lighting (shl, org_id=41)
- **Run date**: 2026-06-17
- **Total Postgres users**: 2147
- **Matched to Mixpanel (Q-01 Step 1)**: 75 of 84 (89%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Cust - DN - Freight | other | 518 |
| Cust - DN - FFA | other | 409 |
| Cust - DN - Discounts | other | 211 |
| Cust - Ferguson | other | 187 |
| Cust - DN - L1 - Discounts | other | 142 |
| Cust - DN - L1 - FFA | other | 117 |
| Cust - NSD - Freight | other | 111 |
| Sales Reps SH/Mer/L1 | field_rep | 90 |
| Cust - Wholesale - FFA - US | other | 73 |
| Cust - CDN - Freight | other | 53 |
| Cust - CDN - FFA | other | 46 |
| Cust - CDN - Discounts | other | 44 |
| Cust - eCommerce | other | 44 |
| Employees - SH (View All) | other | 26 |
| Cust - DN - L1 - Freight | other | 18 |
| Employees - Showroom | showroom | 10 |
| ADMIN | admin_internal | 8 |
| Cust - CDN - L1 - Discounts | other | 8 |
| Cust - Wholesale - Freight - CAN | other | 8 |
| z-SuperCat | admin_internal | 7 |
| Employees - SH (View All) | admin_internal | 6 |
| Sales Reps - Wholesale - SH/Mer/L1 | field_rep | 3 |
| Cust - NSD - FFA | other | 2 |
| Cust - CDN - L1 - FFA | other | 1 |
| Cust - eCommerce | admin_internal | 1 |
| z - Liquidation of Value Guide | other | 1 |
| z-Hide Prices | other | 1 |
| z-OrderXpert - Showroom | showroom | 1 |
| z-eOL Public Site - Savoy House | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 62 | 108,490 | 93.1% |
| showroom | 1 | 35 | 0.0% |
| admin_internal | 7 | 635 | 0.5% |
| other | 5 | 7,311 | 6.3% |
