# Section 5 Context Bundle — Hubbardton Forge (hfg)
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

# Signal Rank — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Total signals fired**: 65 (P0: 47, P1: 18, P2: 0)
- **Org GMV**: $16.8M eCat LTM, $42.2M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep digital-enablement opportunity — 16 reps run $33.5M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion | P1 | §5 Team | 536.6 | $33,536,329 | 2.0 | 35,989,931,609 | POSITIVE |
| 2 | SIG-OPP-02 | Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders | P1 | §2 Accounts | 12.8 | $12,843,857 | 2.0 | 329,929,325 | POSITIVE |
| 3 | SIG-OPP-01 | Next Best Product — 890540/890540-BINDER co-purchase pattern across 40 customers | P0 | §2/§3 | 4.0 | $25,823,289 | 2.0 | 206,586,310 | POSITIVE |
| 4 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 68% of eCat GMV | P1 | §4 Commerce | 1.7 | $5,984,145 | 2.0 | 20,334,605 | RISK |
| 5 | SIG-DECAY-03 | Rep Trajectory — Tony Minutelli orders -54.3% QoQ, $514,283 current 90d GMV | P1 | §5 Team | 2.2 | $2,057,132 | 2.0 | 8,936,181 | RISK |
| 6 | SIG-DECAY-01 | Reorder Decay — The Hotel Design Group 30.7x normal gap (307d vs 10d avg) | P0 | §2 Accounts | 30.7 | $73,912 | 3.0 | 6,807,295 | RISK |
| 7 | SIG-ANOMALY-03 | Competitive Displacement — HF Internal - Residential Accommodation total biz +396% but eCat -100% | P0 | §2 Accounts | 33.1 | $59,206 | 3.0 | 5,872,002 | RISK |
| 8 | SIG-DECAY-01 | Reorder Decay — Tode Rubenstein 4.1x normal gap (88d vs 21d avg) | P0 | §2 Accounts | 4.1 | $411,106 | 3.0 | 5,056,604 | RISK |
| 9 | SIG-DECAY-01 | Reorder Decay — ILC Studios 8.1x normal gap (313d vs 38d avg) | P0 | §2 Accounts | 8.1 | $159,187 | 3.0 | 3,868,244 | RISK |
| 10 | SIG-DECAY-01 | Reorder Decay — Beyer Brown 2.7x normal gap (123d vs 46d avg) | P0 | §2 Accounts | 2.7 | $470,819 | 3.0 | 3,813,634 | RISK |
| 11 | SIG-COMMERCE-01 | Digital order enablement — eCat handles 39.8% of $42M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix) | P0 | §4 Commerce | 3.0 | $422,000 | 3.0 | 3,810,000 | POSITIVE |
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

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep digital-enablement opportunity — 16 reps run $33.5M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion
2. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 20 non-enterprise accounts with $12.8M+ total business, zero eCat orders
3. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — 890540/890540-BINDER co-purchase pattern across 40 customers
4. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Digital order enablement — eCat handles 39.8% of $42M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix)
5. **[RISK]** SIG-RISK-01: Revenue Concentration — top 5 accounts generate 68% of eCat GMV
6. **[RISK]** SIG-DECAY-03: Rep Trajectory — Tony Minutelli orders -54.3% QoQ, $514,283 current 90d GMV
7. **[RISK]** SIG-DECAY-01: Reorder Decay — The Hotel Design Group 30.7x normal gap (307d vs 10d avg)

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### coaching_candidates.md

# Coaching Candidates — Hubbardton Forge (hfg)

Deterministically computed by detect_signals.py. The section agent renders
these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,
or add reps. Archetype framing + narrative are written by the agent; the rep
set and the estimated upside dollar figures are fixed here.

- **Benchmark conversion (top-quartile of converting qualifying reps)**: 15.9%
- **Qualifying reps (>= 50 presentations)**: 16 (14 converting)
- **Upside floor**: $50,000
- **Candidates above floor**: 4

| Rank | Rep | Presentations | Conversion | Benchmark | AOV | Estimated Annual Upside |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Brad Krieger | 326 | 3.4% | 15.9% | $9,135 | $373,740 |
| 2 | Amy Matteson | 151 | 2.0% | 15.9% | $4,104 | $86,449 |
| 3 | Randy Gould | 145 | 3.4% | 15.9% | $4,486 | $81,634 |
| 4 | Dunn Lighting | 168 | 7.7% | 15.9% | $3,873 | $53,680 |

**Combined upside**: $595,503

### Q-01_step1_results.md

# Q-01-S1 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 137
- **Run date**: 2026-06-17


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bkrieger | 449 | 15,943 | 2024-12-10 14:35 | 2026-06-16 14:00 | 6,183 | 1,456 | 4,727 | 2,076 | 2,032 | 31 | 1,137 | 1,137 | 0 | 0 | 45 | 11 | 34 | 0 | 1,147 | 1,115 | 690 | 22 | 0 | 0 | 48 | 104 | 31 |
| jgannon | 526 | 12,740 | 2024-11-01 07:05 | 2026-06-16 15:50 | 2,490 | 837 | 1,653 | 2,424 | 2,400 | 18 | 986 | 986 | 0 | 0 | 14 | 10 | 3 | 1 | 2,911 | 2,895 | 1,010 | 18 | 0 | 0 | 68 | 185 | 179 |
| mgoffice | 363 | 12,700 | 2024-11-01 09:52 | 2026-06-16 16:54 | 6,525 | 1,714 | 4,811 | 2,200 | 2,199 | 1 | 1,438 | 1,438 | 0 | 0 | 0 | 0 | 0 | 0 | 94 | 94 | 74 | 0 | 0 | 0 | 4 | 757 | 8 |
| steven | 409 | 11,932 | 2024-11-01 09:21 | 2026-06-16 14:39 | 5,118 | 912 | 4,206 | 1,530 | 1,348 | 2 | 123 | 123 | 0 | 0 | 10 | 2 | 7 | 1 | 2,351 | 2,340 | 164 | 8 | 0 | 0 | 14 | 22 | 0 |
| dunnlighting | 426 | 9,570 | 2024-11-01 13:53 | 2026-06-16 17:58 | 2,761 | 959 | 1,802 | 1,517 | 1,351 | 0 | 968 | 968 | 0 | 0 | 24 | 1 | 23 | 0 | 1,414 | 1,383 | 244 | 17 | 0 | 0 | 15 | 45 | 120 |
| amymatteson | 433 | 7,891 | 2024-11-01 10:11 | 2026-06-16 14:57 | 3,393 | 1,025 | 2,368 | 1,421 | 1,416 | 5 | 821 | 821 | 0 | 0 | 5 | 0 | 5 | 0 | 470 | 456 | 4 | 0 | 0 | 0 | 0 | 10 | 50 |
| rgould | 474 | 7,011 | 2024-11-01 13:08 | 2026-06-16 19:26 | 1,725 | 717 | 1,008 | 1,300 | 1,297 | 3 | 672 | 672 | 0 | 0 | 76 | 34 | 42 | 0 | 1,101 | 1,037 | 95 | 3 | 0 | 0 | 37 | 118 | 77 |
| wguthrie | 305 | 5,920 | 2024-11-01 09:31 | 2026-06-16 15:49 | 2,963 | 602 | 2,361 | 1,024 | 1,022 | 2 | 759 | 759 | 0 | 0 | 0 | 0 | 0 | 0 | 135 | 113 | 2 | 0 | 0 | 0 | 0 | 64 | 531 |
| kgannon | 397 | 4,622 | 2024-11-02 13:19 | 2026-06-16 18:52 | 690 | 317 | 373 | 935 | 932 | 3 | 565 | 565 | 0 | 0 | 18 | 18 | 0 | 0 | 715 | 671 | 461 | 15 | 0 | 0 | 2 | 16 | 91 |
| gduguid | 255 | 3,953 | 2024-11-04 14:32 | 2026-06-16 13:15 | 1,430 | 351 | 1,079 | 779 | 767 | 1 | 616 | 616 | 0 | 0 | 2 | 0 | 2 | 0 | 285 | 285 | 9 | 0 | 0 | 0 | 17 | 35 | 23 |
| sherrij | 308 | 3,741 | 2024-11-01 13:20 | 2026-06-09 12:45 | 1,430 | 438 | 992 | 654 | 654 | 0 | 436 | 436 | 0 | 0 | 1 | 1 | 0 | 0 | 36 | 34 | 1 | 0 | 0 | 0 | 2 | 83 | 306 |
| kclegg | 314 | 3,551 | 2024-11-01 08:22 | 2026-06-12 11:07 | 498 | 283 | 215 | 550 | 533 | 11 | 316 | 316 | 0 | 0 | 0 | 0 | 0 | 0 | 774 | 721 | 191 | 1 | 0 | 0 | 1 | 7 | 217 |
| tannerg | 307 | 3,519 | 2024-11-01 14:28 | 2026-06-16 13:08 | 940 | 324 | 616 | 930 | 916 | 14 | 500 | 500 | 0 | 0 | 22 | 6 | 15 | 0 | 131 | 129 | 69 | 6 | 0 | 0 | 15 | 14 | 72 |
| robantonecchia | 287 | 3,485 | 2024-11-04 07:25 | 2026-06-16 17:33 | 690 | 256 | 434 | 654 | 629 | 7 | 394 | 394 | 0 | 0 | 28 | 0 | 27 | 0 | 758 | 755 | 70 | 4 | 0 | 0 | 5 | 17 | 1 |
| tminutelli | 253 | 3,387 | 2024-11-01 12:54 | 2026-06-15 17:54 | 1,488 | 502 | 986 | 408 | 405 | 1 | 322 | 322 | 0 | 0 | 3 | 0 | 3 | 0 | 11 | 11 | 1 | 0 | 0 | 0 | 0 | 16 | 382 |
| lbelesky | 280 | 3,375 | 2025-02-05 17:17 | 2026-06-16 12:15 | 824 | 232 | 592 | 620 | 456 | 3 | 389 | 389 | 0 | 0 | 15 | 4 | 11 | 0 | 350 | 329 | 199 | 4 | 0 | 0 | 14 | 36 | 87 |
| jenmccarty | 221 | 3,221 | 2025-06-13 16:19 | 2026-06-16 20:17 | 159 | 149 | 10 | 416 | 413 | 2 | 210 | 210 | 0 | 0 | 88 | 2 | 74 | 6 | 827 | 808 | 276 | 138 | 0 | 7 | 12 | 41 | 17 |
| lynnr1 | 202 | 3,202 | 2024-11-02 15:02 | 2026-06-16 14:11 | 1,307 | 384 | 923 | 494 | 494 | 0 | 441 | 441 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 9 | 0 | 0 | 0 | 0 | 0 | 48 | 320 |
| codyadler | 270 | 3,155 | 2024-11-01 12:12 | 2026-06-12 13:03 | 450 | 112 | 338 | 532 | 526 | 3 | 14 | 14 | 0 | 0 | 32 | 1 | 31 | 0 | 1,178 | 1,154 | 19 | 51 | 0 | 0 | 4 | 4 | 0 |
| gschwartz1 | 150 | 2,968 | 2024-12-10 14:40 | 2025-07-22 17:59 | 778 | 199 | 579 | 466 | 422 | 15 | 149 | 149 | 0 | 0 | 31 | 5 | 20 | 4 | 428 | 402 | 135 | 38 | 0 | 2 | 34 | 50 | 6 |
| jfs | 289 | 2,721 | 2024-11-05 10:47 | 2026-06-16 13:37 | 868 | 139 | 729 | 534 | 526 | 3 | 71 | 71 | 0 | 0 | 5 | 0 | 5 | 0 | 426 | 421 | 4 | 4 | 0 | 0 | 1 | 7 | 4 |
| jimhickey | 326 | 2,704 | 2024-11-06 07:54 | 2026-06-15 09:11 | 345 | 211 | 134 | 221 | 221 | 0 | 148 | 148 | 0 | 0 | 0 | 0 | 0 | 0 | 778 | 676 | 315 | 0 | 0 | 0 | 3 | 15 | 9 |
| aknapp | 169 | 2,594 | 2024-11-06 16:26 | 2026-05-18 09:10 | 274 | 56 | 218 | 333 | 254 | 52 | 112 | 112 | 0 | 0 | 62 | 4 | 56 | 0 | 1,036 | 1,033 | 22 | 45 | 0 | 0 | 45 | 32 | 0 |
| broche | 231 | 2,587 | 2024-11-06 11:07 | 2026-06-14 14:08 | 261 | 256 | 5 | 637 | 634 | 3 | 544 | 544 | 0 | 0 | 23 | 0 | 23 | 0 | 496 | 468 | 11 | 0 | 0 | 0 | 9 | 15 | 3 |
| etibbetts | 168 | 2,408 | 2024-11-01 13:06 | 2026-06-03 11:20 | 435 | 139 | 296 | 293 | 271 | 11 | 133 | 133 | 0 | 0 | 25 | 2 | 23 | 0 | 762 | 753 | 53 | 23 | 0 | 0 | 9 | 27 | 0 |
| mberesford | 196 | 2,270 | 2024-11-01 09:16 | 2025-11-12 12:12 | 788 | 139 | 649 | 313 | 310 | 1 | 56 | 56 | 0 | 0 | 3 | 3 | 0 | 0 | 497 | 481 | 66 | 0 | 0 | 0 | 5 | 15 | 6 |
| jreibel | 503 | 2,190 | 2024-11-01 09:40 | 2026-06-16 11:21 | 458 | 117 | 341 | 458 | 451 | 0 | 97 | 97 | 0 | 0 | 21 | 19 | 2 | 0 | 86 | 72 | 107 | 1 | 0 | 0 | 0 | 0 | 1 |
| dpritchard | 320 | 2,187 | 2024-11-04 13:06 | 2026-06-16 21:23 | 580 | 101 | 479 | 284 | 281 | 1 | 79 | 79 | 0 | 0 | 7 | 5 | 2 | 0 | 203 | 181 | 213 | 3 | 0 | 0 | 1 | 3 | 0 |
| jchon | 200 | 2,134 | 2024-11-01 18:14 | 2026-02-11 15:25 | 1,022 | 260 | 762 | 306 | 305 | 0 | 216 | 216 | 0 | 0 | 0 | 0 | 0 | 0 | 45 | 45 | 1 | 3 | 0 | 0 | 1 | 50 | 5 |
| tstauffacher | 195 | 2,045 | 2024-11-01 15:47 | 2026-06-12 13:45 | 271 | 155 | 116 | 334 | 322 | 9 | 216 | 216 | 0 | 0 | 8 | 4 | 4 | 0 | 602 | 570 | 78 | 10 | 0 | 0 | 3 | 7 | 9 |
| apoindexter | 301 | 2,042 | 2024-11-01 14:38 | 2026-06-16 10:36 | 530 | 145 | 385 | 375 | 372 | 3 | 124 | 124 | 0 | 0 | 64 | 60 | 4 | 0 | 142 | 138 | 62 | 2 | 0 | 0 | 9 | 24 | 4 |
| amcguire | 180 | 1,829 | 2024-11-01 09:58 | 2026-06-16 16:18 | 180 | 38 | 142 | 238 | 237 | 0 | 62 | 62 | 0 | 0 | 19 | 0 | 19 | 0 | 733 | 725 | 7 | 0 | 0 | 0 | 5 | 5 | 1 |
| kimartin | 162 | 1,638 | 2024-11-12 09:58 | 2025-12-26 15:40 | 301 | 91 | 210 | 258 | 256 | 1 | 230 | 230 | 0 | 0 | 12 | 0 | 12 | 0 | 389 | 382 | 0 | 2 | 0 | 0 | 0 | 0 | 14 |
| kgrillo | 155 | 1,630 | 2024-11-01 13:24 | 2026-06-07 17:32 | 236 | 82 | 154 | 227 | 219 | 1 | 86 | 86 | 0 | 0 | 34 | 1 | 33 | 0 | 559 | 557 | 2 | 51 | 0 | 0 | 0 | 6 | 0 |
| starrylightssupport | 126 | 1,613 | 2024-11-04 11:27 | 2025-06-26 13:02 | 322 | 99 | 223 | 477 | 462 | 0 | 160 | 160 | 0 | 0 | 17 | 2 | 15 | 0 | 229 | 228 | 3 | 5 | 0 | 0 | 0 | 3 | 1 |
| ctwigg | 168 | 1,593 | 2024-11-01 12:59 | 2026-06-12 10:42 | 270 | 250 | 20 | 357 | 357 | 0 | 304 | 304 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 0 | 0 | 0 | 1 | 65 | 205 |
| lross | 137 | 1,567 | 2024-11-01 12:19 | 2026-06-11 12:02 | 527 | 187 | 340 | 281 | 280 | 1 | 243 | 243 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 11 | 2 | 0 | 0 | 0 | 0 | 30 | 171 |
| smicheal | 153 | 1,538 | 2024-11-07 11:34 | 2026-06-16 10:44 | 688 | 139 | 549 | 298 | 298 | 0 | 204 | 204 | 0 | 0 | 0 | 0 | 0 | 0 | 26 | 26 | 0 | 0 | 0 | 0 | 2 | 6 | 3 |
| jeffizower | 117 | 1,486 | 2024-11-01 09:46 | 2026-06-16 16:34 | 306 | 67 | 239 | 216 | 212 | 4 | 161 | 161 | 0 | 0 | 17 | 0 | 17 | 0 | 466 | 465 | 18 | 12 | 0 | 3 | 2 | 5 | 6 |
| pgould | 85 | 1,433 | 2024-12-09 16:32 | 2026-05-18 13:08 | 195 | 54 | 141 | 162 | 162 | 0 | 84 | 84 | 0 | 0 | 8 | 8 | 0 | 0 | 742 | 741 | 3 | 6 | 0 | 0 | 8 | 6 | 17 |

*(Truncated: showing top 40 of 137 rows. Full data in cache file.)*

### Q-01_step2_results.md

# Q-01-S2 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 41
- **Run date**: 2026-06-17


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Wayne Guthrie | 337 | $7.0M | $20,662 | 40 |
| Tony Minutelli | 207 | $2.1M | $10,114 | 38 |
| Lynn  Ross | 226 | $1.4M | $6,220 | 47 |
| Karen Clegg | 148 | $1.3M | $9,117 | 41 |
| Sherri Juhl | 174 | $1.0M | $5,847 | 25 |
| Chris Twigg | 131 | $745,256 | $5,689 | 1 |
| Lynn Ross | 98 | $717,701 | $7,323 | 24 |
| Julie Gannon | 110 | $437,231 | $3,975 | 56 |
| Dunn Lighting | 76 | $294,335 | $3,873 | 50 |
| Brad Krieger | 28 | $255,773 | $9,135 | 21 |
| Randy Gould | 47 | $210,827 | $4,486 | 29 |
| Kevin Gannon | 66 | $188,322 | $2,853 | 27 |
| Lisa Belesky | 49 | $164,271 | $3,352 | 19 |
| Tanner Gould | 41 | $153,331 | $3,740 | 22 |
| John Fangman | 16 | $131,317 | $8,207 | 7 |
| Amy Matteson | 25 | $102,589 | $4,104 | 21 |
| Jenifer McCarty | 15 | $78,084 | $5,206 | 9 |
| Jessica - Ricci sales Mason | 4 | $64,445 | $16,111 | 1 |
| Geno Schwartz | 2 | $53,330 | $26,665 | 1 |
| Doug Glassman | 6 | $48,184 | $8,031 | 6 |
| Tami Stauffacher | 5 | $44,197 | $8,839 | 5 |
| Penny Gould | 8 | $34,810 | $4,351 | 6 |
| Jim Hickey | 7 | $26,798 | $3,828 | 3 |
| Grant Duguid | 5 | $24,419 | $4,884 | 3 |
| Trip McKenzie | 4 | $23,168 | $5,792 | 4 |
| Martha Graham & Associates Office | 5 | $20,656 | $4,131 | 4 |
| Carter Likes | 3 | $18,945 | $6,315 | 3 |
| Larry Williams | 2 | $14,466 | $7,233 | 1 |
| Sam  Schwartz | 1 | $11,140 | $11,140 | 0 |
| Christine Alberg | 2 | $9,146 | $4,573 | 1 |
| Vincent Ingato | 6 | $8,919 | $1,486 | 5 |
| Amy  Poindexter | 1 | $5,508 | $5,508 | 0 |
| Jose Echarte | 1 | $5,340 | $5,340 | 1 |
| Shannon Rose | 1 | $4,876 | $4,876 | 1 |
| Jeff Izower | 5 | $4,843 | $968 | 4 |
| Retha Boles | 1 | $4,303 | $4,303 | 1 |
| Alyssa  Heald | 1 | $3,840 | $3,840 | 1 |
| Jeff Stander | 2 | $2,478 | $1,239 | 2 |
| Stacey  Micheal | 1 | $2,299 | $2,299 | 1 |
| Jessica Mason | 2 | $2,093 | $1,046 | 1 |
| Denise Jorge | 1 | $1,104 | $1,104 | 1 |

### Q-04_results.md

# Q-04 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 137
- **Run date**: 2026-06-17


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bkrieger | 449 | 15,943 | 31 | 2,032 | 1,115 | 32 | 34 | 0 | 690 | 22 | Selling Rep |
| jgannon | 526 | 12,740 | 179 | 2,400 | 2,895 | 16 | 3 | 0 | 1,010 | 18 | Selling Rep |
| mgoffice | 363 | 12,700 | 8 | 2,199 | 94 | 0 | 0 | 0 | 74 | 0 | Selling Rep |
| steven | 409 | 11,932 | 0 | 1,348 | 2,340 | 11 | 7 | 0 | 164 | 8 | Content/Library Manager |
| dunnlighting | 426 | 9,570 | 120 | 1,351 | 1,383 | 31 | 23 | 0 | 244 | 17 | Selling Rep |
| amymatteson | 433 | 7,891 | 50 | 1,416 | 456 | 14 | 5 | 0 | 4 | 0 | Selling Rep |
| rgould | 474 | 7,011 | 77 | 1,297 | 1,037 | 64 | 42 | 0 | 95 | 3 | Selling Rep |
| wguthrie | 305 | 5,920 | 531 | 1,022 | 113 | 22 | 0 | 0 | 2 | 0 | Selling Rep |
| kgannon | 397 | 4,622 | 91 | 932 | 671 | 44 | 0 | 0 | 461 | 15 | Selling Rep |
| gduguid | 255 | 3,953 | 23 | 767 | 285 | 0 | 2 | 0 | 9 | 0 | Selling Rep |
| sherrij | 308 | 3,741 | 306 | 654 | 34 | 2 | 0 | 0 | 1 | 0 | Selling Rep |
| kclegg | 314 | 3,551 | 217 | 533 | 721 | 53 | 0 | 0 | 191 | 1 | Selling Rep |
| tannerg | 307 | 3,519 | 72 | 916 | 129 | 2 | 15 | 1 | 69 | 6 | Selling Rep |
| robantonecchia | 287 | 3,485 | 1 | 629 | 755 | 3 | 27 | 1 | 70 | 4 | Content/Library Manager |
| tminutelli | 253 | 3,387 | 382 | 405 | 11 | 0 | 3 | 0 | 1 | 0 | Selling Rep |
| lbelesky | 280 | 3,375 | 87 | 456 | 329 | 21 | 11 | 0 | 199 | 4 | Selling Rep |
| jenmccarty | 221 | 3,221 | 17 | 413 | 808 | 19 | 74 | 6 | 276 | 145 | Selling Rep |
| lynnr1 | 202 | 3,202 | 320 | 494 | 9 | 1 | 0 | 0 | 0 | 0 | Selling Rep |
| codyadler | 270 | 3,155 | 0 | 526 | 1,154 | 24 | 31 | 0 | 19 | 51 | Content/Library Manager |
| gschwartz1 | 150 | 2,968 | 6 | 422 | 402 | 26 | 20 | 2 | 135 | 40 | Selling Rep |
| jfs | 289 | 2,721 | 4 | 526 | 421 | 5 | 5 | 0 | 4 | 4 | Selling Rep |
| jimhickey | 326 | 2,704 | 9 | 221 | 676 | 102 | 0 | 0 | 315 | 0 | Selling Rep |
| aknapp | 169 | 2,594 | 0 | 254 | 1,033 | 3 | 56 | 2 | 22 | 45 | Content/Library Manager |
| broche | 231 | 2,587 | 3 | 634 | 468 | 28 | 23 | 0 | 11 | 0 | Selling Rep |
| etibbetts | 168 | 2,408 | 0 | 271 | 753 | 9 | 23 | 0 | 53 | 23 | Content/Library Manager |
| mberesford | 196 | 2,270 | 6 | 310 | 481 | 16 | 0 | 0 | 66 | 0 | Selling Rep |
| jreibel | 503 | 2,190 | 1 | 451 | 72 | 14 | 2 | 0 | 107 | 1 | Analytics/Portal User |
| dpritchard | 320 | 2,187 | 0 | 281 | 181 | 22 | 2 | 0 | 213 | 3 | Content/Library Manager |
| jchon | 200 | 2,134 | 5 | 305 | 45 | 0 | 0 | 0 | 1 | 3 | Selling Rep |
| tstauffacher | 195 | 2,045 | 9 | 322 | 570 | 32 | 4 | 0 | 78 | 10 | Selling Rep |
| apoindexter | 301 | 2,042 | 4 | 372 | 138 | 4 | 4 | 0 | 62 | 2 | Selling Rep |
| amcguire | 180 | 1,829 | 1 | 237 | 725 | 8 | 19 | 0 | 7 | 0 | Content/Library Manager |
| kimartin | 162 | 1,638 | 14 | 256 | 382 | 7 | 12 | 0 | 0 | 2 | Selling Rep |
| kgrillo | 155 | 1,630 | 0 | 219 | 557 | 2 | 33 | 0 | 2 | 51 | Content/Library Manager |
| starrylightssupport | 126 | 1,613 | 1 | 462 | 228 | 1 | 15 | 0 | 3 | 5 | Content/Library Manager |
| ctwigg | 168 | 1,593 | 205 | 357 | 3 | 1 | 0 | 0 | 0 | 0 | Selling Rep |
| lross | 137 | 1,567 | 171 | 280 | 11 | 1 | 0 | 0 | 2 | 0 | Selling Rep |
| smicheal | 153 | 1,538 | 3 | 298 | 26 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| jeffizower | 117 | 1,486 | 6 | 212 | 465 | 1 | 17 | 0 | 18 | 15 | Selling Rep |
| pgould | 85 | 1,433 | 17 | 162 | 741 | 1 | 0 | 0 | 3 | 6 | Selling Rep |
| lightingrep | 90 | 1,424 | 0 | 353 | 48 | 7 | 16 | 1 | 0 | 56 | Merchandising/List Curator |
| vingato | 199 | 1,400 | 14 | 311 | 30 | 1 | 0 | 0 | 6 | 0 | Selling Rep |
| astauffacher | 77 | 1,347 | 3 | 124 | 872 | 12 | 0 | 0 | 28 | 0 | Selling Rep |
| jessicam | 121 | 1,194 | 7 | 135 | 265 | 1 | 2 | 0 | 3 | 3 | Selling Rep |
| sschwartz1 | 94 | 1,145 | 2 | 144 | 336 | 39 | 6 | 0 | 8 | 0 | Content/Library Manager |
| ccoxworth | 151 | 1,137 | 0 | 215 | 459 | 16 | 0 | 0 | 1 | 1 | Content/Library Manager |
| grillocs | 336 | 1,034 | 0 | 132 | 43 | 0 | 1 | 0 | 1 | 1 | Sales Support/Inside Sales |
| tripm | 78 | 1,016 | 5 | 159 | 93 | 1 | 10 | 2 | 2 | 3 | Selling Rep |
| bpeel | 224 | 952 | 0 | 167 | 24 | 0 | 0 | 0 | 147 | 0 | Analytics/Portal User |
| nstory | 54 | 937 | 0 | 85 | 455 | 3 | 0 | 0 | 12 | 0 | Content/Library Manager |
| lightingvision | 38 | 838 | 3 | 76 | 413 | 4 | 0 | 0 | 3 | 0 | Selling Rep |
| dougg | 59 | 817 | 9 | 96 | 109 | 3 | 6 | 0 | 0 | 0 | Selling Rep |
| rocher | 71 | 811 | 1 | 102 | 422 | 14 | 1 | 0 | 0 | 0 | Content/Library Manager |
| kaceywilliams | 65 | 810 | 0 | 208 | 261 | 1 | 1 | 0 | 22 | 4 | Content/Library Manager |
| williamsl | 159 | 800 | 5 | 187 | 47 | 8 | 1 | 0 | 16 | 0 | Selling Rep |
| lmalchus | 62 | 787 | 0 | 111 | 287 | 0 | 9 | 0 | 2 | 15 | Content/Library Manager |
| todd_m | 59 | 715 | 0 | 29 | 497 | 3 | 1 | 0 | 0 | 0 | Content/Library Manager |
| dsouthwickdrew | 63 | 712 | 2 | 35 | 396 | 0 | 0 | 0 | 9 | 1 | Content/Library Manager |
| nickc | 213 | 709 | 0 | 93 | 101 | 2 | 5 | 0 | 35 | 1 | Sales Support/Inside Sales |
| czaya | 72 | 683 | 16 | 99 | 159 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| rhailpern | 89 | 674 | 2 | 106 | 214 | 32 | 0 | 0 | 1 | 0 | Content/Library Manager |
| agautzsch | 19 | 643 | 0 | 0 | 588 | 3 | 0 | 0 | 0 | 0 | Content/Library Manager |
| vwalker1 | 48 | 582 | 3 | 70 | 38 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| srose1 | 64 | 554 | 1 | 138 | 84 | 0 | 65 | 0 | 5 | 2 | Catalog/Data Manager |
| ptodoroff | 115 | 547 | 0 | 155 | 173 | 2 | 0 | 0 | 1 | 0 | Sales Support/Inside Sales |
| carterl | 63 | 508 | 5 | 136 | 78 | 9 | 2 | 0 | 14 | 0 | Selling Rep |
| cframburg | 10 | 466 | 0 | 177 | 11 | 3 | 0 | 0 | 2 | 81 | Merchandising/List Curator |
| jewet4924 | 47 | 452 | 1 | 99 | 127 | 5 | 6 | 0 | 0 | 0 | Low-Activity User |
| rhiggins | 45 | 426 | 1 | 39 | 185 | 3 | 4 | 0 | 4 | 1 | Low-Activity User |
| jfangman | 38 | 388 | 23 | 81 | 2 | 1 | 0 | 0 | 0 | 0 | Selling Rep |
| maggiem | 36 | 372 | 0 | 48 | 29 | 2 | 14 | 0 | 19 | 15 | Low-Activity User |
| tammymartindsg | 20 | 371 | 0 | 70 | 214 | 0 | 0 | 0 | 0 | 0 | Content/Library Manager |
| clscott | 37 | 361 | 0 | 16 | 237 | 0 | 0 | 0 | 0 | 2 | Content/Library Manager |
| khastings | 39 | 307 | 0 | 1 | 213 | 0 | 0 | 0 | 0 | 0 | Content/Library Manager |
| nickbrown | 9 | 303 | 0 | 93 | 81 | 1 | 5 | 0 | 1 | 10 | Inactive |
| calberg | 27 | 271 | 10 | 43 | 25 | 1 | 0 | 0 | 7 | 0 | Selling Rep |
| rboles | 27 | 270 | 4 | 15 | 116 | 0 | 5 | 0 | 10 | 1 | Selling Rep |
| donna_s | 48 | 268 | 0 | 44 | 3 | 0 | 3 | 0 | 0 | 0 | Low-Activity User |
| bgrillo | 121 | 258 | 0 | 2 | 32 | 0 | 0 | 0 | 2 | 0 | Low-Activity User |
| lcarmichael | 27 | 250 | 0 | 36 | 85 | 7 | 0 | 0 | 8 | 0 | Inactive |
| matt | 25 | 239 | 0 | 31 | 64 | 0 | 3 | 0 | 0 | 2 | Inactive |
| mgraham | 35 | 237 | 3 | 20 | 23 | 2 | 0 | 0 | 3 | 0 | Selling Rep |
| vcollins | 42 | 237 | 0 | 47 | 12 | 0 | 0 | 0 | 3 | 1 | Low-Activity User |
| kellyk | 19 | 230 | 0 | 15 | 56 | 4 | 0 | 0 | 9 | 0 | Inactive |
| kathys | 20 | 205 | 0 | 127 | 15 | 2 | 0 | 0 | 10 | 0 | Inactive |
| pres81224 | 21 | 178 | 0 | 23 | 59 | 2 | 0 | 0 | 0 | 0 | Inactive |
| troyk | 30 | 177 | 0 | 61 | 9 | 4 | 0 | 0 | 18 | 0 | Inactive |
| liz_n | 75 | 177 | 0 | 21 | 1 | 0 | 2 | 0 | 0 | 0 | Low-Activity User |
| starrylights | 9 | 173 | 2 | 45 | 41 | 3 | 0 | 0 | 4 | 0 | Inactive |
| mmccarthy1 | 24 | 164 | 18 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sorourke | 12 | 150 | 0 | 23 | 13 | 0 | 24 | 0 | 0 | 0 | Catalog/Data Manager |
| pjames1 | 16 | 130 | 0 | 31 | 7 | 0 | 0 | 0 | 1 | 0 | Inactive |
| jose | 28 | 115 | 1 | 1 | 40 | 1 | 0 | 0 | 0 | 0 | Inactive |
| monicam | 11 | 108 | 0 | 5 | 71 | 4 | 0 | 0 | 0 | 0 | Inactive |
| kmurphy4 | 18 | 100 | 0 | 30 | 0 | 0 | 2 | 0 | 2 | 1 | Inactive |
| eddiev | 18 | 95 | 0 | 41 | 6 | 0 | 0 | 0 | 0 | 0 | Inactive |
| aminkhan | 53 | 93 | 0 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | Low-Activity User |
| rschwartz1 | 4 | 88 | 0 | 34 | 1 | 0 | 0 | 0 | 3 | 0 | Inactive |
| zcarranta | 12 | 82 | 0 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jlindquist | 8 | 79 | 0 | 21 | 6 | 0 | 0 | 0 | 0 | 0 | Inactive |
| hschwartz1 | 37 | 76 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 1 | Low-Activity User |
| stevelinder | 28 | 72 | 0 | 5 | 8 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pcarlson | 30 | 72 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | Inactive |
| aframburg | 9 | 70 | 0 | 19 | 1 | 0 | 1 | 0 | 0 | 3 | Inactive |
| terry | 11 | 64 | 0 | 7 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sarahp | 8 | 64 | 0 | 9 | 5 | 0 | 1 | 0 | 0 | 4 | Inactive |
| rluttrell1 | 7 | 64 | 0 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | Inactive |
| bstout | 7 | 53 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | Inactive |
| layla_c | 15 | 52 | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tbierowski | 17 | 48 | 0 | 6 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| nandrus1 | 7 | 45 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| alarrick | 8 | 43 | 3 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| martinb | 10 | 34 | 0 | 7 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| zachscar | 1 | 34 | 0 | 12 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| earp727 | 13 | 32 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dkapalka | 6 | 28 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| philcook | 15 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jwilson | 3 | 25 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mote1 | 8 | 22 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | Inactive |
| jarnoldenlight | 9 | 22 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | Inactive |
| ptheos | 3 | 21 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jskula | 5 | 17 | 0 | 0 | 4 | 3 | 0 | 0 | 0 | 0 | Inactive |
| jonv | 9 | 15 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| swt | 7 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brittainc | 3 | 14 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tess | 5 | 13 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| brentsanders | 3 | 13 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mmullen1 | 2 | 12 | 0 | 5 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| bodonnell | 3 | 11 | 0 | 1 | 1 | 2 | 0 | 0 | 0 | 0 | Inactive |
| djorge | 2 | 10 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mrose1 | 2 | 10 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| aheald | 1 | 8 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pmarr | 2 | 6 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tburgess | 3 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| rphillips1 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| thel84 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dougy | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 57 | 88 | 26 |

### Q-06_results.md

# Q-06 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 104
- **Run date**: 2026-06-17


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Wayne Guthrie | 53 | 60 | 13.20 | 70 | 95 | 35.70 | $4.0M |
| Lynn  Ross | 44 | 35 | -20.50 | 64 | 52 | -18.80 | $361,368 |
| Sherri Juhl | 63 | 52 | -17.50 | 53 | 37 | -30.20 | $190,903 |
| Karen Clegg | 72 | 56 | -22.20 | 52 | 35 | -32.70 | $280,300 |
| Tony Minutelli | 75 | 38 | -49.30 | 70 | 32 | -54.30 | $514,283 |
| Chris Twigg | 34 | 38 | 11.80 | 28 | 28 | 0 | $244,086 |
| Dunn Lighting | 268 | 183 | -31.70 | 19 | 26 | 36.80 | $65,614 |
| Julie Gannon | 316 | 297 | -6 | 23 | 23 | 0 | $84,126 |
| Lynn Ross | 27 | 12 | -55.60 | 32 | 21 | -34.40 | $97,928 |
| Kevin Gannon | 209 | 189 | -9.60 | 23 | 20 | -13 | $46,410 |
| Tanner Gould | 86 | 72 | -16.30 | 8 | 14 | 75 | $58,536 |
| Brad Krieger | 618 | 487 | -21.20 | 10 | 12 | 20 | $142,844 |
| Lisa Belesky | 106 | 75 | -29.20 | 20 | 10 | -50 | $47,178 |
| Randy Gould | 210 | 220 | 4.80 | 13 | 9 | -30.80 | $30,345 |
| Jenifer McCarty | 142 | 172 | 21.10 | 5 | 6 | 20 | $8,832 |
| Amy Matteson | 162 | 133 | -17.90 | 4 | 6 | 50 | $23,767 |
| Martha Graham & Associates Office | 129 | 116 | -10.10 | 1 | 3 | 200 | $14,942 |
| John Fangman | 0 | 5 | — | 0 | 2 | — | $2,844 |
| Doug Glassman | 27 | 6 | -77.80 | 4 | 2 | -50 | $16,887 |
| Grant Duguid | 77 | 47 | -39 | 0 | 2 | — | $15,604 |
| Tami Stauffacher | 41 | 32 | -22 | 3 | 2 | -33.30 | $10,141 |
| Jeff Izower | 32 | 14 | -56.30 | 1 | 2 | 100 | $1,857 |
| Alyssa  Heald | 0 | 1 | — | 0 | 1 | — | $3,840 |
| Jeff Stander | 70 | 62 | -11.40 | 0 | 1 | — | $1,692 |
| Denise Jorge | 0 | 2 | — | 0 | 1 | — | $1,104 |
| Penny Gould | 21 | 7 | -66.70 | 2 | 1 | -50 | $460 |
| Jim Hickey | 81 | 59 | -27.20 | 4 | 0 | -100 | $0 |
| Trip McKenzie | 30 | 18 | -40 | 4 | 0 | -100 | $0 |
| Carter Likes | 28 | 11 | -60.70 | 3 | 0 | -100 | $0 |
| Shannon Rose | 29 | 13 | -55.20 | 1 | 0 | -100 | $0 |
| Larry Williams | 52 | 19 | -63.50 | 2 | 0 | -100 | $0 |
| Jose Echarte | 11 | 4 | -63.60 | 1 | 0 | -100 | $0 |
| Paula James | 12 | 1 | -91.70 | — | — | — | — |
| Amy McGuire | 20 | 26 | 30 | — | — | — | — |
| Kelly Murphy | 4 | 6 | 50 | — | — | — | — |
| Renee Schwartz | 2 | 0 | -100 | — | — | — | — |
| Virginia Collins | 0 | 26 | — | — | — | — | — |
| James Arnold | 0 | 2 | — | — | — | — | — |
| Pepper Carlson | 4 | 7 | 75 | — | — | — | — |
| Donny Durant | 2 | 0 | -100 | — | — | — | — |
| Josh Skula | 4 | 1 | -75 | — | — | — | — |
| Eric Tibbetts | 44 | 22 | -50 | — | — | — | — |
| Hal  Schwartz | 10 | 9 | -10 | — | — | — | — |
| Alex Gautzsch | 7 | 1 | -85.70 | — | — | — | — |
| Cody Adler | 54 | 39 | -27.80 | — | — | — | — |
| Roberta Phillips | 0 | 1 | — | — | — | — | — |
| Shelley Aldridge | 14 | 0 | -100 | — | — | — | — |
| Pauline Theos | 0 | 3 | — | — | — | — | — |
| Steve Linder | 14 | 3 | -78.60 | — | — | — | — |
| Troy  Kaup | 2 | 5 | 150 | — | — | — | — |
| Retha Boles | 2 | 4 | 100 | — | — | — | — |
| Vincent Ingato | 76 | 30 | -60.50 | — | — | — | — |
| Matt Rowland | 2 | 4 | 100 | — | — | — | — |
| Beth O'Donnell | 0 | 2 | — | — | — | — | — |
| Beth Peel | 76 | 55 | -27.60 | — | — | — | — |
| Kacey Williams | 18 | 15 | -16.70 | — | — | — | — |
| Jessica - Ricci sales Mason | 41 | 24 | -41.50 | — | — | — | — |
| Brian Roche | 71 | 35 | -50.70 | — | — | — | — |
| Zach Scarborough | 2 | 0 | -100 | — | — | — | — |
| Nick Curtis | 67 | 59 | -11.90 | — | — | — | — |
| Maggie McCrary | 17 | 1 | -94.10 | — | — | — | — |
| Natalie Andrus | 0 | 7 | — | — | — | — | — |
| Christine Alberg | 2 | 0 | -100 | — | — | — | — |
| Darla Pritchard | 86 | 48 | -44.20 | — | — | — | — |
| Andrew Knapp | 18 | 18 | 0 | — | — | — | — |
| Chris Saars | 30 | 0 | -100 | — | — | — | — |
| Philip Todoroff | 17 | 12 | -29.40 | — | — | — | — |
| Todd Martin | 12 | 5 | -58.30 | — | — | — | — |
| Cameron Adler | 31 | 11 | -64.50 | — | — | — | — |
| Stacey ORourke | 2 | 1 | -50 | — | — | — | — |
| Beto Grillo | 35 | 25 | -28.60 | — | — | — | — |
| Jordan Chon | 36 | 0 | -100 | — | — | — | — |
| Presley  Lynch | 0 | 6 | — | — | — | — | — |
| Amy  Poindexter | 61 | 78 | 27.90 | — | — | — | — |
| Stacey  Micheal | 26 | 23 | -11.50 | — | — | — | — |
| TESS MARTIN | 7 | 1 | -85.70 | — | — | — | — |
| Patrick Brockamp | 20 | 0 | -100 | — | — | — | — |
| Amin Khan | 13 | 4 | -69.20 | — | — | — | — |
| Grillo Customer Service | 53 | 85 | 60.40 | — | — | — | — |
| Rob Hailpern | 41 | 3 | -92.70 | — | — | — | — |
| Derrick Southwick-Drew | 0 | 4 | — | — | — | — | — |
| Jon Vanderberg | 1 | 0 | -100 | — | — | — | — |
| Sam  Schwartz | 18 | 4 | -77.80 | — | — | — | — |
| Jon Reibel | 145 | 119 | -17.90 | — | — | — | — |
| Lisa Carmichael | 10 | 3 | -70 | — | — | — | — |
| Claire Scott | 17 | 7 | -58.80 | — | — | — | — |
| Rachel  Luttrell | 4 | 0 | -100 | — | — | — | — |
| Brent Sanders | 3 | 0 | -100 | — | — | — | — |
| Charlie Mote | 8 | 0 | -100 | — | — | — | — |
| Renee Roche | 2 | 5 | 150 | — | — | — | — |
| Phil Cook | 2 | 0 | -100 | — | — | — | — |
| Steve Ricci | 293 | 293 | 0 | — | — | — | — |
| Allison Stauffacher | 23 | 8 | -65.20 | — | — | — | — |
| Jordan  Jewett | 6 | 1 | -83.30 | — | — | — | — |
| Martha Graham | 6 | 3 | -50 | — | — | — | — |
| Kit Hastings | 4 | 1 | -75 | — | — | — | — |
| Zander Carranta | 17 | 2 | -88.20 | — | — | — | — |
| Sarah Pocock | 0 | 8 | — | — | — | — | — |
| Ken Grillo | 21 | 22 | 4.80 | — | — | — | — |
| Rob Antonecchia | 93 | 74 | -20.40 | — | — | — | — |
| Jimmy Wilson | 2 | 0 | -100 | — | — | — | — |
| Kirk Martin | 2 | 0 | -100 | — | — | — | — |
| Melanie Rose | 2 | 0 | -100 | — | — | — | — |
| Todd Bierowski | 5 | 3 | -40 | — | — | — | — |

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-43_results.md

(not present — file does not exist or is empty)

### Q-43_step2_results.md

# Q-43-S2 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-51_results.md

# Q-51 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-51 — Rep-Level eCat Capture
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| rep_name | rep_number | erp_orders | erp_gmv | erp_customers | ecat_orders | ecat_gmv | ecat_customers | ecat_capture_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BrandJump, LLC | 42586 | 5,308 | $5.5M | 11 | 0 | $0 | 0 | 0 |
| Martha Graham & Assoc: Martha | 12328 | 1,547 | $3.8M | 173 | 0 | $0 | 0 | 0 |
| Grillo Group | 42333 | 212 | $3.3M | 40 | 0 | $0 | 0 | 0 |
| Speckk Brands | 45123 | 1,732 | $3.2M | 190 | 0 | $0 | 0 | 0 |
| Glassman Brands | 11998 | 1,468 | $3.0M | 224 | 0 | $0 | 0 | 0 |
| Lighting Vision, Inc | 44079 | 980 | $2.6M | 145 | 0 | $0 | 0 | 0 |
| Gannon Sales Agency | 42332 | 1,551 | $2.4M | 202 | 0 | $0 | 0 | 0 |
| Dunn Lighting | 41168 | 1,109 | $2.2M | 188 | 76 | $294,335 | 50 | 13.60 |
| Ricci Sales Agency | 11871 | 967 | $1.8M | 211 | 0 | $0 | 0 | 0 |
| Stander Associates, Inc. | 40550 | 909 | $1.6M | 79 | 0 | $0 | 0 | 0 |
| Gould Associates | 12225 | 560 | $1.6M | 117 | 0 | $0 | 0 | 0 |
| Carolina Fixture Sales | 37184 | 529 | $1.0M | 117 | 0 | $0 | 0 | 0 |
| Enlightening Sales | 41451 | 427 | $1.0M | 136 | 0 | $0 | 0 | 0 |
| Adler Lighting Sales, LLC. | 43090 | 406 | $783,654 | 101 | 0 | $0 | 0 | 0 |
| Vincent Ingato Sales | 12868 | 386 | $694,801 | 62 | 0 | $0 | 0 | 0 |
| Guthrie & Associates | 12367 | 170 | $640,494 | 64 | 0 | $0 | 0 | 0 |
| Decor Lighting Sales | 42067 | 279 | $617,380 | 47 | 0 | $0 | 0 | 0 |
| Williams Lighting Source | 41148 | 185 | $451,550 | 36 | 0 | $0 | 0 | 0 |
| Larrick Design Resources | 16998 | 98 | $313,760 | 38 | 0 | $0 | 0 | 0 |
| Apex Lighting Solutions | 13794 | 103 | $302,164 | 36 | 0 | $0 | 0 | 0 |
| Exclusively Lighting Inc. | 37385 | 33 | $266,241 | 13 | 0 | $0 | 0 | 0 |
| WE Hospitality | 12185 | 82 | $244,164 | 35 | 0 | $0 | 0 | 0 |
| Lighting Environments | 42952 | 35 | $207,265 | 14 | 0 | $0 | 0 | 0 |
| Enterprise Lighting Sales Corp | 43184 | 59 | $203,319 | 25 | 0 | $0 | 0 | 0 |
| SJ Concepts | 12457 | 76 | $196,074 | 30 | 0 | $0 | 0 | 0 |

### Q-62_results.md

# Q-62 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-63_results.md

# Q-63 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bkrieger | 40 | 326 | 11 | 27.50 | 3.40 | 325 | 1 | 0 |
| mgoffice | 38 | 218 | 2 | 5.30 | 0.90 | 218 | 0 | 0 |
| dunnlighting | 21 | 168 | 13 | 61.90 | 7.70 | 168 | 0 | 0 |
| steven | 30 | 164 | 0 | 0 | 0 | 164 | 0 | 0 |
| amymatteson | 15 | 151 | 3 | 20 | 2 | 151 | 0 | 0 |
| rgould | 25 | 145 | 5 | 20 | 3.40 | 138 | 0 | 7 |
| wguthrie | 17 | 129 | 75 | 441.20 | 58.10 | 129 | 0 | 0 |
| jenmccarty | 7 | 124 | 8 | 114.30 | 6.50 | 111 | 13 | 0 |
| jgannon | 12 | 106 | 7 | 58.30 | 6.60 | 106 | 0 | 0 |
| robantonecchia | 9 | 99 | 0 | 0 | 0 | 97 | 2 | 0 |
| tannerg | 12 | 94 | 10 | 83.30 | 10.60 | 90 | 2 | 2 |
| kgannon | 15 | 90 | 15 | 100 | 16.70 | 90 | 0 | 0 |
| ctwigg | 1 | 65 | 27 | 2,700 | 41.50 | 65 | 0 | 0 |
| sherrij | 8 | 64 | 30 | 375 | 46.90 | 64 | 0 | 0 |
| jeffizower | 3 | 52 | 1 | 33.30 | 1.90 | 50 | 2 | 0 |
| lbelesky | 4 | 51 | 7 | 175 | 13.70 | 51 | 0 | 0 |
| gduguid | 5 | 48 | 2 | 40 | 4.20 | 48 | 0 | 0 |
| kclegg | 7 | 45 | 25 | 357.10 | 55.60 | 45 | 0 | 0 |
| etibbetts | 1 | 38 | 0 | 0 | 0 | 37 | 1 | 0 |
| lynnr1 | 5 | 37 | 36 | 720 | 97.30 | 37 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| ctwigg | 1 | 189 | 25 | 1 | 0 |
| sorourke | 1 | 37 | 1 | 1 | 0 |
| jenmccarty | 14 | 27.20 | 2.60 | 6 | 2 |
| dougg | 3 | 25 | 1 | 2 | 0 |
| kaceywilliams | 3 | 23.30 | 2 | 2 | 0 |
| kclegg | 19 | 16.90 | 3.40 | 10 | 4 |
| lynnr1 | 21 | 16.90 | 3.10 | 11 | 1 |
| sherrij | 20 | 16.30 | 3 | 12 | 2 |
| wguthrie | 36 | 15.90 | 2.60 | 19 | 2 |
| lbelesky | 20 | 15.90 | 2.40 | 10 | 3 |
| jessicam | 14 | 14.30 | 1.80 | 3 | 2 |
| jeffizower | 15 | 13.10 | 1.10 | 4 | 6 |
| lross | 12 | 12.40 | 2.20 | 8 | 0 |
| pgould | 6 | 11.80 | 1.70 | 1 | 1 |
| robantonecchia | 40 | 11.40 | 1.50 | 12 | 8 |
| bkrieger | 164 | 11.20 | 2.10 | 74 | 26 |
| gduguid | 21 | 10.80 | 1.70 | 8 | 2 |
| etibbetts | 8 | 10.80 | 1.60 | 2 | 2 |
| mgoffice | 106 | 10.80 | 2.50 | 53 | 13 |
| amymatteson | 86 | 10.60 | 2.20 | 30 | 17 |

### Q-65_results.md

# Q-65 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| wguthrie | 1,011 | 929 | 82 | 91.90 | 8.10 |
| dougg | 99 | 87 | 12 | 87.90 | 12.10 |
| mgoffice | 1,922 | 1,685 | 237 | 87.70 | 12.30 |
| lross | 179 | 148 | 31 | 82.70 | 17.30 |
| tminutelli | 287 | 236 | 51 | 82.20 | 17.80 |
| lynnr1 | 410 | 334 | 76 | 81.50 | 18.50 |
| gduguid | 415 | 330 | 85 | 79.50 | 20.50 |
| sherrij | 420 | 330 | 90 | 78.60 | 21.40 |
| tripm | 154 | 117 | 37 | 76 | 24 |
| lcarmichael | 37 | 28 | 9 | 75.70 | 24.30 |
| ctwigg | 248 | 187 | 61 | 75.40 | 24.60 |
| rhailpern | 24 | 18 | 6 | 75 | 25 |
| smicheal | 195 | 146 | 49 | 74.90 | 25.10 |
| sorourke | 42 | 31 | 11 | 73.80 | 26.20 |
| amymatteson | 1,023 | 739 | 284 | 72.20 | 27.80 |
| tannerg | 483 | 344 | 139 | 71.20 | 28.80 |
| nandrus1 | 45 | 31 | 14 | 68.90 | 31.10 |
| jfs | 537 | 363 | 174 | 67.60 | 32.40 |
| steven | 1,841 | 1,189 | 652 | 64.60 | 35.40 |
| vcollins | 146 | 94 | 52 | 64.40 | 35.60 |

### Q-70_results.md

# Q-70 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-70 — Inactive Reps with Territory Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Total flagged**: 1
- **Aggregate GMV**: $20,656

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |
| Martha Graham & Associates Office | 5 | $20,656 | keyword | confirmed_operational |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### user_group_mapping.md

# User Group Mapping — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-17
- **Total Postgres users**: 206
- **Matched to Mixpanel (Q-01 Step 1)**: 118 of 137 (86%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| ResTradeGroup | other | 76 |
| ComGroup | other | 74 |
| ResTradeCom | other | 16 |
| AdminDefaultUserGroup | admin_internal | 11 |
| CanadaRes | other | 9 |
| InternalHFSales | admin_internal | 9 |
| 1 - Default eOL User Group | admin_internal | 4 |
| z-SuperCat | admin_internal | 4 |
| Decorating Den Group | admin_internal | 1 |
| Decorating Den Group | other | 1 |
| eCat Online Public Site | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| admin_internal | 14 | 6,581 | 3.5% |
| other | 104 | 182,467 | 96.5% |
