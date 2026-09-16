# Section 5 Context Bundle — Gabby (gh)
Run date: 2026-06-17

## Gate Flags

# Gate Flags — Gabby (gh, org_id=55)
- **Run date**: 2026-06-17
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False |
| HAS_PORTAL_ORDERS | True | portal_order_count=25284, portal_order_gmv=$41.6M |
| HAS_INVENTORY | True | inventory_count=6857 |
| HAS_SALES_DATA | True | sales_data_count=63154 |
| HAS_SALES_SECTION | True | qualifying_reps=38 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | gabby_gh_eol_portal |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | FAIL | erp_gmv=$41.6M > ecat_gmv=$50.2M: False |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | False | Both gates fail |
| QUALIFYING_REP_COUNT | 38 | 38 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 95 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 14474, Mixpanel total submit_order (Q-01): 15645 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=68.4%, ambiguous_rate=1.5%, showroom_event_share=3.0% |
| USER_GROUP_JOIN_RATE | 68% | 65 of 95 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.0% |
| ADMIN_REPS_IN_LEADERBOARD | True | 7 admin/showroom users in leaderboard: Ben Erickson, Jonah Tibbs, Richard Bentley, Beau Taylor, Margaret Murray |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False | days_since_last_erp_order=9999 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=31 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2683 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=27 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | STRONG | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | STRONG | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Gabby
- **Shortname**: gh
- **Org ID**: 55
- **Bundle**: 8
- **Bundle label for report**: 8

## Validation Log

- VM-45 skipped: Gate1=FAIL, Gate2=PASS

## Section Confidence

# Section Confidence Tiers — Gabby (gh, org_id=55)
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

# Signal Rank — Gabby (gh, org_id=55)
- **Run date**: 2026-06-17
- **Total signals fired**: 73 (P0: 58, P1: 13, P2: 2)
- **Org GMV**: $50.2M eCat LTM, $41.6M total business LTM

## Ranked Manifest (Top 20 by SIGNAL_RANK)

| Rank | Signal ID | Description | Priority | Section | Surprise | Dollar Impact | Action | SIGNAL_RANK | Tone |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | SIG-TEAM-01 | Rep digital-enablement opportunity — 12 reps run $25.1M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion | P1 | §5 Team | 301.7 | $25,144,013 | 2.0 | 15,173,313,354 | POSITIVE |
| 2 | SIG-OPP-01 | Next Best Product — SCH-166295/ co-purchase pattern across 164 customers | P0 | §2/§3 | 16.4 | $302,760,334 | 2.0 | 9,930,538,968 | POSITIVE |
| 3 | SIG-DECAY-01 | Reorder Decay — HCD DESIGN, LLC 20.9x normal gap (182d vs 8d avg) | P0 | §2 Accounts | 20.9 | $442,894 | 3.0 | 27,769,454 | RISK |
| 4 | SIG-ANOMALY-02 | Stock Out — SCH-168190 (Strella Cabinet) $366,883 LTM, 0 available | P0 | §3 Product | 10.0 | $366,883 | 3.0 | 11,006,495 | RISK |
| 5 | SIG-ANOMALY-02 | Stock Out — SCH-175228 (Leary Sideboard - Gray) $322,414 LTM, 0 available | P0 | §3 Product | 10.0 | $322,414 | 3.0 | 9,672,430 | RISK |
| 6 | SIG-MOM-01 | Account Acceleration — BE CASUAL FURNISHINGS, INC 2 consecutive QoQ acceleration quarters, $401,957 peak quarter (+240% QoQ) | P0 | §2 Accounts | 8.0 | $401,957 | 3.0 | 9,626,880 | POSITIVE |
| 7 | SIG-OPP-02 | Unactivated High-Value Accounts — 9 non-enterprise accounts with $2.2M+ total business, zero eCat orders | P1 | §2 Accounts | 2.2 | $2,193,375 | 2.0 | 9,621,788 | POSITIVE |
| 8 | SIG-ANOMALY-02 | Stock Out — SCH-166275 (Fitzgerald Sideboard) $297,241 LTM, 0 available | P0 | §3 Product | 10.0 | $297,241 | 3.0 | 8,917,237 | RISK |
| 9 | SIG-ANOMALY-02 | Stock Out — SCH-175636 (Andrea Dresser) $235,140 LTM, 0 available | P0 | §3 Product | 10.0 | $235,140 | 3.0 | 7,054,213 | RISK |
| 10 | SIG-DECAY-04 | Spending Contraction — LITTMAN BROS -72.3% YoY ($870,472→$240,904), $629,568 gap | P0 | §2 Accounts | 3.6 | $629,568 | 3.0 | 6,827,667 | RISK |
| 11 | SIG-RISK-01 | Revenue Concentration — top 5 accounts generate 50% of eCat GMV | P1 | §4 Commerce | 1.3 | $2,593,150 | 2.0 | 6,533,100 | RISK |
| 12 | SIG-MOM-01 | Account Acceleration — ELLE DESIGN & DECOR DBA GREENE AND CO INTERIORS 2 consecutive QoQ acceleration quarters, $67,194 peak quarter (+966% QoQ) | P0 | §2 Accounts | 32.2 | $67,194 | 3.0 | 6,489,548 | POSITIVE |
| 13 | SIG-ANOMALY-02 | Stock Out — SCH-175164 (Landon Counter Stool - Gold) $205,351 LTM, 0 available | P0 | §3 Product | 10.0 | $205,351 | 3.0 | 6,160,531 | RISK |
| 14 | SIG-MOM-01 | Account Acceleration — LUMENS INC 2 consecutive QoQ acceleration quarters, $142,189 peak quarter (+378% QoQ) | P0 | §2 Accounts | 12.6 | $142,189 | 3.0 | 5,377,588 | POSITIVE |
| 15 | SIG-DECAY-03 | Rep Trajectory — Savanna Dunaway orders -68.4% QoQ, $240,486 current 90d GMV | P1 | §5 Team | 2.7 | $961,944 | 2.0 | 5,263,758 | RISK |
| 16 | SIG-ANOMALY-02 | Stock Out — SCH-175638 (Meredith Nightstand) $173,969 LTM, 0 available | P0 | §3 Product | 10.0 | $173,969 | 3.0 | 5,219,072 | RISK |
| 17 | SIG-DECAY-01 | Reorder Decay — GREEN FRONT FURNITURE CO. INC. 2.9x normal gap (15d vs 5d avg) | P0 | §2 Accounts | 2.9 | $590,939 | 3.0 | 5,141,169 | RISK |
| 18 | SIG-ANOMALY-02 | Stock Out — SCH-175456 (Victoria Chandelier) $169,086 LTM, 0 available | P0 | §3 Product | 10.0 | $169,086 | 3.0 | 5,072,587 | RISK |
| 19 | SIG-ANOMALY-02 | Stock Out — SCH-175641 (Andrea Nightstand) $166,743 LTM, 0 available | P0 | §3 Product | 10.0 | $166,743 | 3.0 | 5,002,293 | RISK |
| 20 | SIG-ANOMALY-02 | Stock Out — SCH-175458 (Teagan Chandelier) $163,968 LTM, 0 available | P0 | §3 Product | 10.0 | $163,968 | 3.0 | 4,919,030 | RISK |

## Section Signal Density Table

| Section | P0 | P1 | P2 | Total | Notes |
| --- | --- | --- | --- | --- | --- |
| §2 Account Intelligence | 37 | 1 | 0 | 38 | |
| §3 Product Intelligence | 20 | 0 | 1 | 21 | |
| §4 Commerce Patterns | 1 | 1 | 0 | 2 | |
| §5 Team Intelligence | 0 | 5 | 0 | 5 | |
| §6 Platform Context | 0 | 6 | 1 | 7 | |

**Section ORDER is FIXED (§1→§5→§2→§4→§3→§6). Density does NOT determine position.**

## Top 7 Signal Summary Candidates

Ordered by narrative arc (Momentum → Intelligence → Opportunity → Risk), NOT by raw SIGNAL_RANK:

1. **[POSITIVE/MOMENTUM]** SIG-TEAM-01: Rep digital-enablement opportunity — 12 reps run $25.1M of business entirely through other channels (web/EDI/phone/email/rep entry); rep-assisted digital ordering could streamline the manual portion
2. **[POSITIVE/MOMENTUM]** SIG-OPP-01: Next Best Product — SCH-166295/ co-purchase pattern across 164 customers
3. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — BE CASUAL FURNISHINGS, INC 2 consecutive QoQ acceleration quarters, $401,957 peak quarter (+240% QoQ)
4. **[POSITIVE/MOMENTUM]** SIG-OPP-02: Unactivated High-Value Accounts — 9 non-enterprise accounts with $2.2M+ total business, zero eCat orders
5. **[RISK]** SIG-DECAY-01: Reorder Decay — HCD DESIGN, LLC 20.9x normal gap (182d vs 8d avg)
6. **[RISK]** SIG-ANOMALY-02: Stock Out — SCH-168190 (Strella Cabinet) $366,883 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — SCH-175228 (Leary Sideboard - Gray) $322,414 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### coaching_candidates.md

# Coaching Candidates — Gabby (gh)

Deterministically computed by detect_signals.py. The section agent renders
these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,
or add reps. Archetype framing + narrative are written by the agent; the rep
set and the estimated upside dollar figures are fixed here.

- **Benchmark conversion (top-quartile of converting qualifying reps)**: 20.4%
- **Qualifying reps (>= 50 presentations)**: 15 (15 converting)
- **Upside floor**: $50,000
- **Candidates above floor**: 1

| Rank | Rep | Presentations | Conversion | Benchmark | AOV | Estimated Annual Upside |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Rob Robinson | 587 | 10.9% | 20.4% | $4,487 | $248,901 |

**Combined upside**: $248,901

### Q-01_step1_results.md

# Q-01-S1 Results — Gabby (gh, org_id=55)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 95
- **Run date**: 2026-06-17


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sc-annel | 400 | 32,590 | 2024-11-01 10:06 | 2026-06-16 16:56 | 13,410 | 3,052 | 10,358 | 9,190 | 9,181 | 9 | 1,490 | 672 | 514 | 304 | 515 | 104 | 411 | 0 | 1,050 | 736 | 2,261 | 0 | 0 | 0 | 1 | 788 | 1,410 |
| sc-ryanc | 545 | 27,293 | 2024-11-01 10:54 | 2026-06-16 20:31 | 8,826 | 2,655 | 6,171 | 7,417 | 7,404 | 13 | 2,159 | 948 | 784 | 427 | 51 | 12 | 38 | 1 | 909 | 562 | 1,737 | 115 | 0 | 4 | 0 | 21 | 1,762 |
| pbe | 437 | 24,469 | 2024-11-01 09:15 | 2026-06-16 18:44 | 7,019 | 2,258 | 4,761 | 8,964 | 8,720 | 244 | 1,422 | 569 | 499 | 354 | 169 | 0 | 169 | 0 | 534 | 298 | 837 | 0 | 0 | 0 | 346 | 269 | 1,524 |
| hr | 467 | 24,315 | 2024-11-01 07:42 | 2026-06-16 21:55 | 8,818 | 2,462 | 6,356 | 7,309 | 7,276 | 27 | 1,783 | 706 | 662 | 415 | 46 | 43 | 3 | 0 | 739 | 467 | 1,068 | 15 | 0 | 0 | 4 | 300 | 1,438 |
| sc-clarer | 432 | 22,042 | 2024-11-01 10:32 | 2026-06-16 21:42 | 7,849 | 2,052 | 5,797 | 7,489 | 7,400 | 87 | 1,261 | 520 | 459 | 282 | 135 | 0 | 135 | 0 | 373 | 237 | 707 | 0 | 0 | 0 | 50 | 306 | 922 |
| sc-savannad | 259 | 17,216 | 2025-03-19 11:03 | 2026-04-10 13:52 | 6,863 | 1,322 | 5,541 | 5,835 | 5,834 | 1 | 768 | 242 | 355 | 171 | 333 | 1 | 332 | 0 | 524 | 377 | 775 | 0 | 0 | 0 | 5 | 243 | 579 |
| sc-davids | 502 | 14,972 | 2024-11-01 07:07 | 2026-06-16 17:27 | 3,786 | 1,313 | 2,473 | 4,821 | 4,763 | 58 | 554 | 199 | 249 | 106 | 10 | 8 | 2 | 0 | 712 | 525 | 1,237 | 34 | 0 | 0 | 114 | 210 | 499 |
| sc-denaec | 427 | 14,585 | 2024-11-01 09:31 | 2026-06-16 17:54 | 4,960 | 1,521 | 3,439 | 3,266 | 3,236 | 30 | 635 | 270 | 238 | 127 | 70 | 4 | 66 | 0 | 791 | 670 | 1,055 | 8 | 0 | 1 | 9 | 236 | 560 |
| sc-tanyah | 338 | 12,873 | 2025-03-17 13:11 | 2026-06-16 15:59 | 5,361 | 1,143 | 4,218 | 2,711 | 2,629 | 82 | 497 | 163 | 219 | 115 | 49 | 36 | 13 | 0 | 1,192 | 822 | 4 | 118 | 0 | 3 | 8 | 541 | 479 |
| sc-allisonw | 407 | 12,841 | 2024-11-01 11:13 | 2026-06-16 18:24 | 6,555 | 1,489 | 5,066 | 2,179 | 2,157 | 13 | 555 | 203 | 233 | 119 | 4 | 2 | 2 | 0 | 482 | 319 | 390 | 0 | 0 | 0 | 3 | 17 | 575 |
| sc-catf | 409 | 12,695 | 2024-11-04 12:13 | 2026-06-16 15:34 | 6,127 | 1,540 | 4,587 | 2,691 | 2,688 | 3 | 453 | 144 | 220 | 89 | 52 | 16 | 36 | 0 | 532 | 377 | 18 | 16 | 0 | 0 | 51 | 297 | 347 |
| rs | 409 | 11,496 | 2024-11-01 11:57 | 2026-06-16 16:12 | 3,068 | 836 | 2,232 | 3,198 | 3,187 | 11 | 525 | 174 | 247 | 104 | 23 | 17 | 6 | 0 | 412 | 280 | 1,476 | 0 | 0 | 0 | 8 | 138 | 394 |
| rrobinson | 424 | 11,311 | 2024-11-01 14:00 | 2026-06-16 16:09 | 3,174 | 962 | 2,212 | 3,634 | 3,516 | 118 | 642 | 231 | 241 | 170 | 122 | 14 | 108 | 0 | 555 | 377 | 70 | 56 | 0 | 4 | 50 | 478 | 475 |
| sc-dianah | 424 | 10,151 | 2024-11-01 09:35 | 2026-06-16 12:10 | 2,919 | 926 | 1,993 | 2,046 | 2,031 | 15 | 629 | 237 | 235 | 157 | 19 | 2 | 17 | 0 | 816 | 522 | 455 | 0 | 0 | 0 | 0 | 1 | 587 |
| sc-kellym | 332 | 9,313 | 2024-11-01 10:24 | 2026-06-16 17:21 | 3,158 | 502 | 2,656 | 3,587 | 3,571 | 16 | 503 | 122 | 307 | 74 | 47 | 34 | 13 | 0 | 453 | 398 | 89 | 3 | 0 | 0 | 0 | 8 | 179 |
| sc-margos | 358 | 9,045 | 2024-11-01 10:20 | 2026-06-16 17:14 | 3,184 | 799 | 2,385 | 2,716 | 2,716 | 0 | 420 | 188 | 140 | 92 | 60 | 48 | 12 | 0 | 381 | 269 | 25 | 35 | 0 | 0 | 4 | 17 | 493 |
| zww | 352 | 8,914 | 2024-11-01 09:59 | 2026-06-16 18:06 | 3,634 | 763 | 2,871 | 2,454 | 2,414 | 40 | 366 | 173 | 121 | 72 | 59 | 6 | 53 | 0 | 325 | 190 | 137 | 0 | 0 | 0 | 9 | 46 | 457 |
| jeremyr | 460 | 8,286 | 2024-11-02 17:04 | 2026-06-16 17:16 | 2,129 | 583 | 1,546 | 1,685 | 1,662 | 23 | 319 | 113 | 144 | 62 | 9 | 3 | 5 | 0 | 689 | 580 | 844 | 9 | 0 | 0 | 11 | 99 | 366 |
| sc-katiewilloughby | 233 | 7,233 | 2025-02-13 12:04 | 2026-06-13 16:43 | 1,890 | 571 | 1,319 | 3,131 | 3,129 | 2 | 554 | 188 | 243 | 123 | 37 | 2 | 35 | 0 | 332 | 242 | 106 | 0 | 0 | 0 | 0 | 2 | 318 |
| sc-timb | 191 | 5,055 | 2024-11-01 07:50 | 2025-07-02 15:11 | 1,632 | 404 | 1,228 | 1,373 | 1,364 | 9 | 112 | 35 | 52 | 25 | 19 | 0 | 19 | 0 | 247 | 212 | 328 | 14 | 0 | 1 | 26 | 62 | 179 |
| sc-benjaminf | 301 | 5,032 | 2024-11-01 17:11 | 2026-06-16 14:49 | 1,542 | 345 | 1,197 | 1,309 | 1,309 | 0 | 209 | 68 | 101 | 40 | 24 | 23 | 1 | 0 | 380 | 267 | 406 | 0 | 0 | 0 | 0 | 40 | 189 |
| sc-sarahb | 290 | 4,636 | 2025-03-06 16:26 | 2026-06-16 12:08 | 1,707 | 396 | 1,311 | 731 | 704 | 21 | 193 | 73 | 88 | 32 | 18 | 1 | 17 | 0 | 278 | 222 | 251 | 0 | 0 | 0 | 12 | 50 | 228 |
| sc-ninaj | 172 | 4,448 | 2024-11-01 15:32 | 2025-07-07 12:11 | 1,268 | 408 | 860 | 950 | 937 | 13 | 156 | 48 | 71 | 37 | 43 | 12 | 31 | 0 | 159 | 98 | 41 | 146 | 0 | 19 | 6 | 11 | 126 |
| sc-beaut | 358 | 4,442 | 2024-11-01 08:42 | 2026-06-16 14:38 | 1,572 | 307 | 1,265 | 904 | 904 | 0 | 134 | 27 | 93 | 14 | 0 | 0 | 0 | 0 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 1 | 95 |
| sc-dwasserman | 271 | 4,307 | 2024-11-01 10:54 | 2026-06-16 10:43 | 1,298 | 367 | 931 | 806 | 788 | 16 | 111 | 27 | 72 | 12 | 25 | 5 | 20 | 0 | 489 | 383 | 50 | 27 | 0 | 0 | 64 | 189 | 44 |
| sc-jameso | 229 | 4,105 | 2024-11-01 16:44 | 2025-09-19 12:33 | 1,714 | 344 | 1,370 | 864 | 854 | 10 | 280 | 180 | 67 | 33 | 0 | 0 | 0 | 0 | 178 | 128 | 4 | 0 | 0 | 0 | 0 | 3 | 104 |
| sc-elizabethr | 69 | 3,843 | 2024-11-01 09:55 | 2025-02-13 10:17 | 1,006 | 287 | 719 | 1,646 | 1,643 | 3 | 132 | 46 | 54 | 32 | 96 | 0 | 96 | 0 | 125 | 99 | 245 | 0 | 0 | 0 | 0 | 7 | 139 |
| jensen | 256 | 3,808 | 2024-11-01 11:09 | 2026-04-15 13:49 | 990 | 347 | 643 | 1,123 | 1,121 | 2 | 260 | 103 | 98 | 59 | 3 | 3 | 0 | 0 | 191 | 108 | 210 | 0 | 0 | 0 | 0 | 16 | 204 |
| sc-fisherh | 192 | 3,516 | 2024-11-05 12:30 | 2025-12-19 10:58 | 1,421 | 258 | 1,163 | 934 | 934 | 0 | 157 | 47 | 76 | 34 | 2 | 1 | 1 | 0 | 119 | 60 | 92 | 0 | 0 | 0 | 13 | 23 | 176 |
| sc-mandyp | 238 | 3,094 | 2024-11-04 10:24 | 2026-06-16 16:56 | 1,281 | 292 | 989 | 696 | 696 | 0 | 163 | 60 | 67 | 36 | 0 | 0 | 0 | 0 | 140 | 121 | 4 | 0 | 0 | 0 | 0 | 55 | 86 |
| sc-howardc | 142 | 2,856 | 2025-11-19 10:35 | 2026-06-16 17:42 | 1,149 | 236 | 913 | 539 | 536 | 3 | 172 | 71 | 80 | 21 | 1 | 1 | 0 | 0 | 45 | 36 | 153 | 0 | 0 | 0 | 6 | 29 | 88 |
| sc-crystalg | 130 | 2,310 | 2025-05-23 09:44 | 2026-04-29 16:14 | 451 | 68 | 383 | 996 | 996 | 0 | 181 | 92 | 50 | 39 | 1 | 1 | 0 | 0 | 42 | 29 | 28 | 3 | 0 | 0 | 3 | 24 | 13 |
| sc-tanguliar | 301 | 2,297 | 2024-11-04 11:34 | 2026-06-16 11:46 | 714 | 187 | 527 | 365 | 365 | 0 | 190 | 52 | 113 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 55 |
| sc-margauxt | 108 | 2,088 | 2025-12-04 09:47 | 2026-06-16 14:27 | 617 | 240 | 377 | 459 | 449 | 2 | 123 | 40 | 60 | 23 | 0 | 0 | 0 | 0 | 244 | 149 | 66 | 0 | 0 | 0 | 0 | 50 | 55 |
| sc-mariannem | 64 | 2,000 | 2024-11-01 04:45 | 2025-01-31 15:33 | 549 | 182 | 367 | 406 | 398 | 8 | 127 | 41 | 56 | 30 | 2 | 0 | 1 | 0 | 151 | 121 | 195 | 0 | 0 | 0 | 3 | 54 | 134 |
| sc-jesseg | 204 | 1,953 | 2024-11-04 11:29 | 2026-06-16 13:32 | 756 | 209 | 547 | 327 | 323 | 4 | 76 | 22 | 33 | 21 | 6 | 0 | 6 | 0 | 39 | 25 | 20 | 0 | 0 | 0 | 1 | 20 | 50 |
| chadforti | 254 | 1,952 | 2024-11-01 15:16 | 2026-06-16 14:56 | 474 | 99 | 375 | 378 | 376 | 2 | 53 | 19 | 26 | 8 | 11 | 0 | 11 | 0 | 200 | 165 | 85 | 5 | 0 | 0 | 5 | 9 | 54 |
| gkaz | 131 | 1,920 | 2024-11-04 13:15 | 2025-05-16 18:02 | 558 | 148 | 410 | 431 | 424 | 6 | 88 | 27 | 47 | 14 | 4 | 2 | 2 | 0 | 67 | 41 | 209 | 7 | 0 | 1 | 0 | 37 | 30 |
| sc-kimd | 157 | 1,628 | 2025-02-17 12:00 | 2026-06-05 11:16 | 637 | 90 | 547 | 355 | 355 | 0 | 63 | 20 | 30 | 13 | 0 | 0 | 0 | 0 | 68 | 48 | 18 | 0 | 0 | 0 | 4 | 19 | 52 |
| sc-mdr | 128 | 1,137 | 2024-11-01 14:21 | 2026-06-11 10:16 | 451 | 104 | 347 | 237 | 237 | 0 | 35 | 13 | 18 | 4 | 7 | 7 | 0 | 0 | 28 | 20 | 2 | 0 | 0 | 0 | 1 | 1 | 48 |

*(Truncated: showing top 40 of 95 rows. Full data in cache file.)*

### Q-01_step2_results.md

# Q-01-S2 Results — Gabby (gh, org_id=55)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 48
- **Run date**: 2026-06-17


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Ryan Casabella | 1,173 | $5.5M | $4,690 | 167 |
| Paul Bentley | 897 | $3.9M | $4,322 | 178 |
| Heather Robert | 938 | $3.3M | $3,557 | 171 |
| Clare Colón | 664 | $2.8M | $4,264 | 119 |
| Margo Scoggins | 317 | $2.8M | $8,902 | 44 |
| Diana Horsley | 359 | $2.8M | $7,844 | 61 |
| Anne Leonard | 818 | $2.8M | $3,409 | 176 |
| Wynne White | 349 | $2.3M | $6,706 | 80 |
| Savanna Dunaway | 432 | $1.8M | $4,265 | 134 |
| Rob Robinson | 307 | $1.4M | $4,487 | 69 |
| Katie Willoughby | 192 | $1.3M | $6,930 | 47 |
| Allison Wooley | 363 | $1.3M | $3,575 | 78 |
| Tanya Houge | 376 | $1.2M | $3,203 | 89 |
| Denae Copeland | 367 | $1.1M | $3,056 | 75 |
| Sarah Balducci | 202 | $1.1M | $5,506 | 45 |
| David Sherrill | 280 | $761,162 | $2,718 | 60 |
| Jeremy Rago | 194 | $745,300 | $3,842 | 46 |
| Rick Scott | 228 | $617,064 | $2,706 | 76 |
| Cat Freund | 218 | $548,312 | $2,515 | 55 |
| Jensen Meier | 90 | $479,829 | $5,331 | 25 |
| Benjamin Forti | 127 | $472,477 | $3,720 | 46 |
| Kim Drye | 46 | $332,548 | $7,229 | 16 |
| Howard Cohen | 89 | $330,112 | $3,709 | 32 |
| Kelly McGuire | 100 | $290,963 | $2,910 | 29 |
| Crystal Gonzalez | 12 | $252,392 | $21,033 | 6 |
| Chad Forti | 35 | $212,597 | $6,074 | 9 |
| Fisher Harwell | 64 | $192,183 | $3,003 | 23 |
| James Oh | 31 | $135,439 | $4,369 | 11 |
| Mandy Piper | 52 | $123,867 | $2,382 | 20 |
| Tangulia   Rose | 34 | $105,783 | $3,111 | 21 |
| Doug Wasserman | 27 | $68,687 | $2,544 | 9 |
| Jobey Tudor | 19 | $59,929 | $3,154 | 9 |
| MD Rickers | 29 | $58,012 | $2,000 | 9 |
| Margaux Toothman | 55 | $56,196 | $1,022 | 23 |
| Jesse Gerber | 30 | $47,587 | $1,586 | 19 |
| Beau Taylor | 56 | $45,214 | $807 | 44 |
| Jonah Tibbs | 12 | $36,126 | $3,010 | 3 |
| Trade Show 2 | 2 | $34,376 | $17,188 | 0 |
| Tim Baldwin | 9 | $30,165 | $3,352 | 5 |
| Jackson Omana | 2 | $26,620 | $13,310 | 2 |
| Melissa Taylor | 4 | $16,716 | $4,179 | 3 |
| Richard Bentley | 3 | $13,354 | $4,451 | 3 |
| Ben Erickson | 7 | $8,673 | $1,239 | 3 |
| Deric Hansen | 2 | $5,606 | $2,803 | 1 |
| Alesher Wooley | 1 | $958 | $958 | 1 |
| Margaret Murray | 11 | $50 | $5 | 1 |
| Libby Brumfield | 1 | $0 | $0 | 0 |
| Lorne Gardner | 1 | $0 | $0 | 1 |

### Q-04_results.md

# Q-04 Results — Gabby (gh, org_id=55)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 95
- **Run date**: 2026-06-17


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sc-annel | 400 | 32,590 | 1,410 | 9,181 | 736 | 314 | 411 | 0 | 2,261 | 0 | Selling Rep |
| sc-ryanc | 545 | 27,293 | 1,762 | 7,404 | 562 | 347 | 38 | 0 | 1,737 | 119 | Selling Rep |
| pbe | 437 | 24,469 | 1,524 | 8,720 | 298 | 236 | 169 | 0 | 837 | 0 | Selling Rep |
| hr | 467 | 24,315 | 1,438 | 7,276 | 467 | 272 | 3 | 0 | 1,068 | 15 | Selling Rep |
| sc-clarer | 432 | 22,042 | 922 | 7,400 | 237 | 136 | 135 | 0 | 707 | 0 | Selling Rep |
| sc-savannad | 259 | 17,216 | 579 | 5,834 | 377 | 147 | 332 | 0 | 775 | 0 | Selling Rep |
| sc-davids | 502 | 14,972 | 499 | 4,763 | 525 | 187 | 2 | 0 | 1,237 | 34 | Selling Rep |
| sc-denaec | 427 | 14,585 | 560 | 3,236 | 670 | 121 | 66 | 0 | 1,055 | 9 | Selling Rep |
| sc-tanyah | 338 | 12,873 | 479 | 2,629 | 822 | 370 | 13 | 0 | 4 | 121 | Selling Rep |
| sc-allisonw | 407 | 12,841 | 575 | 2,157 | 319 | 163 | 2 | 0 | 390 | 0 | Selling Rep |
| sc-catf | 409 | 12,695 | 347 | 2,688 | 377 | 155 | 36 | 0 | 18 | 16 | Selling Rep |
| rs | 409 | 11,496 | 394 | 3,187 | 280 | 132 | 6 | 0 | 1,476 | 0 | Selling Rep |
| rrobinson | 424 | 11,311 | 475 | 3,516 | 377 | 178 | 108 | 0 | 70 | 60 | Selling Rep |
| sc-dianah | 424 | 10,151 | 587 | 2,031 | 522 | 294 | 17 | 0 | 455 | 0 | Selling Rep |
| sc-kellym | 332 | 9,313 | 179 | 3,571 | 398 | 55 | 13 | 0 | 89 | 3 | Selling Rep |
| sc-margos | 358 | 9,045 | 493 | 2,716 | 269 | 112 | 12 | 0 | 25 | 35 | Selling Rep |
| zww | 352 | 8,914 | 457 | 2,414 | 190 | 135 | 53 | 0 | 137 | 0 | Selling Rep |
| jeremyr | 460 | 8,286 | 366 | 1,662 | 580 | 109 | 5 | 1 | 844 | 9 | Selling Rep |
| sc-katiewilloughby | 233 | 7,233 | 318 | 3,129 | 242 | 90 | 35 | 0 | 106 | 0 | Selling Rep |
| sc-timb | 191 | 5,055 | 179 | 1,364 | 212 | 35 | 19 | 0 | 328 | 15 | Selling Rep |
| sc-benjaminf | 301 | 5,032 | 189 | 1,309 | 267 | 113 | 1 | 0 | 406 | 0 | Selling Rep |
| sc-sarahb | 290 | 4,636 | 228 | 704 | 222 | 56 | 17 | 0 | 251 | 0 | Selling Rep |
| sc-ninaj | 172 | 4,448 | 126 | 937 | 98 | 61 | 31 | 0 | 41 | 165 | Selling Rep |
| sc-beaut | 358 | 4,442 | 95 | 904 | 17 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-dwasserman | 271 | 4,307 | 44 | 788 | 383 | 106 | 20 | 0 | 50 | 27 | Selling Rep |
| sc-jameso | 229 | 4,105 | 104 | 854 | 128 | 50 | 0 | 0 | 4 | 0 | Selling Rep |
| sc-elizabethr | 69 | 3,843 | 139 | 1,643 | 99 | 26 | 96 | 0 | 245 | 0 | Selling Rep |
| jensen | 256 | 3,808 | 204 | 1,121 | 108 | 83 | 0 | 0 | 210 | 0 | Selling Rep |
| sc-fisherh | 192 | 3,516 | 176 | 934 | 60 | 59 | 1 | 0 | 92 | 0 | Selling Rep |
| sc-mandyp | 238 | 3,094 | 86 | 696 | 121 | 19 | 0 | 0 | 4 | 0 | Selling Rep |
| sc-howardc | 142 | 2,856 | 88 | 536 | 36 | 9 | 0 | 0 | 153 | 0 | Selling Rep |
| sc-crystalg | 130 | 2,310 | 13 | 996 | 29 | 13 | 0 | 0 | 28 | 3 | Selling Rep |
| sc-tanguliar | 301 | 2,297 | 55 | 365 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-margauxt | 108 | 2,088 | 55 | 449 | 149 | 95 | 0 | 0 | 66 | 0 | Selling Rep |
| sc-mariannem | 64 | 2,000 | 134 | 398 | 121 | 30 | 1 | 1 | 195 | 0 | Selling Rep |
| sc-jesseg | 204 | 1,953 | 50 | 323 | 25 | 14 | 6 | 0 | 20 | 0 | Selling Rep |
| chadforti | 254 | 1,952 | 54 | 376 | 165 | 35 | 11 | 0 | 85 | 5 | Selling Rep |
| gkaz | 131 | 1,920 | 30 | 424 | 41 | 26 | 2 | 0 | 209 | 8 | Selling Rep |
| sc-kimd | 157 | 1,628 | 52 | 355 | 48 | 20 | 0 | 0 | 18 | 0 | Selling Rep |
| sc-mdr | 128 | 1,137 | 48 | 237 | 20 | 8 | 0 | 0 | 2 | 0 | Selling Rep |
| sc-jobeyt | 37 | 1,082 | 20 | 216 | 152 | 8 | 3 | 0 | 9 | 0 | Selling Rep |
| sc-paigem | 36 | 1,072 | 30 | 421 | 64 | 34 | 0 | 0 | 8 | 0 | Selling Rep |
| sc-libbyb | 57 | 879 | 1 | 385 | 19 | 4 | 29 | 0 | 8 | 30 | Catalog/Data Manager |
| sc-harold | 68 | 642 | 0 | 172 | 4 | 1 | 1 | 0 | 11 | 5 | Sales Support/Inside Sales |
| sc-margaretm | 50 | 600 | 13 | 328 | 61 | 0 | 10 | 0 | 0 | 1 | Selling Rep |
| sc-calebb | 64 | 578 | 4 | 165 | 129 | 3 | 1 | 0 | 2 | 0 | Selling Rep |
| sc-coltonj | 22 | 543 | 0 | 418 | 0 | 0 | 9 | 0 | 0 | 29 | Sales Support/Inside Sales |
| sc-storym | 44 | 468 | 0 | 198 | 71 | 0 | 3 | 0 | 0 | 0 | Low-Activity User |
| jomana | 29 | 336 | 3 | 110 | 2 | 0 | 0 | 0 | 5 | 0 | Selling Rep |
| sc-mitchw | 17 | 318 | 14 | 89 | 1 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-ashleywr | 39 | 303 | 6 | 119 | 5 | 2 | 0 | 0 | 0 | 0 | Selling Rep |
| bene | 36 | 263 | 6 | 13 | 16 | 4 | 0 | 0 | 2 | 0 | Selling Rep |
| sc-melissat | 22 | 233 | 4 | 10 | 120 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-jonaht | 23 | 208 | 13 | 20 | 0 | 0 | 0 | 0 | 1 | 0 | Selling Rep |
| sc-brookehj | 13 | 199 | 0 | 11 | 134 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-derich | 24 | 172 | 2 | 9 | 66 | 7 | 0 | 0 | 0 | 0 | Inactive |
| sc-gertrudem | 39 | 172 | 0 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | Low-Activity User |
| sc-jamesa | 27 | 151 | 0 | 16 | 18 | 1 | 0 | 0 | 3 | 0 | Inactive |
| jonv | 5 | 126 | 0 | 6 | 6 | 4 | 1 | 0 | 6 | 2 | Inactive |
| sc-mallorym | 18 | 105 | 0 | 42 | 11 | 0 | 0 | 0 | 1 | 0 | Inactive |
| lornegardner | 18 | 98 | 1 | 13 | 7 | 4 | 0 | 0 | 21 | 0 | Inactive |
| ryanw | 24 | 92 | 0 | 12 | 13 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 4 | 80 | 0 | 54 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-tracyr | 8 | 77 | 0 | 22 | 4 | 2 | 0 | 0 | 6 | 0 | Inactive |
| sc-tradeshow2 | 7 | 72 | 2 | 28 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| sc-tradeshow | 5 | 69 | 1 | 22 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| sc-pamelae | 18 | 62 | 3 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-meganu | 9 | 61 | 3 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-allanb | 20 | 61 | 0 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mkazmierczak | 9 | 60 | 0 | 2 | 0 | 0 | 0 | 0 | 4 | 0 | Inactive |
| sc-richardb | 7 | 57 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sc-whitleem | 7 | 53 | 0 | 1 | 0 | 0 | 10 | 0 | 0 | 3 | Inactive |
| sc-alesherw | 7 | 47 | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-kristinc | 10 | 39 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-samr | 10 | 37 | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sdonti | 8 | 30 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-jorgannat | 4 | 28 | 0 | 2 | 5 | 0 | 0 | 0 | 2 | 0 | Inactive |
| sc-paulad | 10 | 28 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-kevina | 7 | 22 | 0 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-ericas | 6 | 17 | 0 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-nickg | 2 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-reannar | 1 | 17 | 1 | 7 | 0 | 0 | 0 | 0 | 2 | 0 | Inactive |
| sc-marydelcuerto | 3 | 16 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-aaronh | 4 | 12 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-emmaw | 3 | 11 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| swt | 4 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-jenniferc | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-tradeshow1 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kyla | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jthrasherna | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-celinal | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-daniels | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-robinh | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sc-alexise | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Gabby (gh, org_id=55)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 128 | 56 | 543 |

### Q-06_results.md

# Q-06 Results — Gabby (gh, org_id=55)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 64
- **Run date**: 2026-06-17


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ryan Casabella | 475 | 556 | 17.10 | 263 | 299 | 13.70 | $1.2M |
| Anne Leonard | 167 | 151 | -9.60 | 191 | 277 | 45 | $914,288 |
| Paul Bentley | 290 | 329 | 13.40 | 214 | 238 | 11.20 | $1.1M |
| Heather Robert | 257 | 293 | 14 | 196 | 216 | 10.20 | $628,767 |
| Clare Colón | 328 | 339 | 3.40 | 171 | 199 | 16.40 | $784,575 |
| Wynne White | 165 | 269 | 63 | 74 | 153 | 106.80 | $1.0M |
| Margo Scoggins | 80 | 196 | 145 | 41 | 141 | 243.90 | $1.2M |
| Allison Wooley | 177 | 245 | 38.40 | 96 | 132 | 37.50 | $513,183 |
| Tanya Houge | 263 | 328 | 24.70 | 91 | 121 | 33 | $417,056 |
| Diana Horsley | 227 | 272 | 19.80 | 72 | 120 | 66.70 | $930,136 |
| Denae Copeland | 308 | 322 | 4.50 | 85 | 103 | 21.20 | $341,642 |
| Sarah Balducci | 112 | 173 | 54.50 | 29 | 83 | 186.20 | $474,463 |
| Rob Robinson | 170 | 168 | -1.20 | 91 | 75 | -17.60 | $461,968 |
| David Sherrill | 353 | 401 | 13.60 | 77 | 71 | -7.80 | $204,228 |
| Rick Scott | 223 | 276 | 23.80 | 53 | 56 | 5.70 | $206,566 |
| Cat Freund | 148 | 160 | 8.10 | 56 | 54 | -3.60 | $144,330 |
| Howard Cohen | 225 | 146 | -35.10 | 42 | 46 | 9.50 | $106,429 |
| Katie Willoughby | 26 | 66 | 153.80 | 16 | 43 | 168.80 | $257,215 |
| Savanna Dunaway | 112 | 27 | -75.90 | 133 | 42 | -68.40 | $240,486 |
| Jeremy Rago | 231 | 201 | -13 | 23 | 36 | 56.50 | $116,822 |
| Benjamin Forti | 100 | 136 | 36 | 14 | 33 | 135.70 | $145,835 |
| Margaux Toothman | 130 | 193 | 48.50 | 24 | 31 | 29.20 | $15,001 |
| Kelly McGuire | 102 | 141 | 38.20 | 26 | 20 | -23.10 | $58,477 |
| Jobey Tudor | 0 | 116 | — | 0 | 19 | — | $59,929 |
| Mandy Piper | 87 | 77 | -11.50 | 18 | 19 | 5.60 | $67,471 |
| Doug Wasserman | 62 | 150 | 141.90 | 3 | 13 | 333.30 | $41,228 |
| Beau Taylor | 107 | 144 | 34.60 | 5 | 11 | 120 | $7,071 |
| Jesse Gerber | 51 | 77 | 51 | 6 | 10 | 66.70 | $12,704 |
| Jensen Meier | 48 | 29 | -39.60 | 18 | 8 | -55.60 | $86,517 |
| MD Rickers | 18 | 23 | 27.80 | 3 | 7 | 133.30 | $16,644 |
| Tangulia   Rose | 55 | 43 | -21.80 | 10 | 7 | -30 | $20,548 |
| Chad Forti | 60 | 55 | -8.30 | 6 | 7 | 16.70 | $67,834 |
| Kim Drye | 68 | 30 | -55.90 | 29 | 7 | -75.90 | $17,873 |
| Margaret Murray | 5 | 6 | 20 | 3 | 4 | 33.30 | $0 |
| Melissa Taylor | 16 | 9 | -43.80 | 2 | 2 | 0 | $15,152 |
| Trade Show 2 | 0 | 8 | — | 0 | 2 | — | $34,376 |
| Deric Hansen | 34 | 3 | -91.20 | 1 | 1 | 0 | $1,792 |
| Lorne Gardner | 0 | 24 | — | 0 | 1 | — | $0 |
| Crystal Gonzalez | 34 | 15 | -55.90 | 1 | 1 | 0 | $1,956 |
| Ben Erickson | 19 | 4 | -78.90 | 7 | 0 | -100 | $0 |
| Richard Bentley | 2 | 3 | 50 | 1 | 0 | -100 | $0 |
| Jackson Omana | 7 | 3 | -57.10 | 1 | 0 | -100 | $0 |
| Jonah Tibbs | 15 | 10 | -33.30 | 12 | 0 | -100 | $0 |
| Tracy Rickers | 0 | 5 | — | — | — | — | — |
| Whitlee Morris | 3 | 0 | -100 | — | — | — | — |
| Gertrude  Marchione | 5 | 12 | 140 | — | — | — | — |
| Harold Hudson | 16 | 23 | 43.80 | — | — | — | — |
| James Ashley | 2 | 0 | -100 | — | — | — | — |
| Jennifer Cohen | 4 | 0 | -100 | — | — | — | — |
| Erica Swinea | 3 | 1 | -66.70 | — | — | — | — |
| Aaron Hedges | 1 | 0 | -100 | — | — | — | — |
| Kevin Ashby | 5 | 0 | -100 | — | — | — | — |
| Kyla Bosch | 1 | 0 | -100 | — | — | — | — |
| Libby Brumfield | 2 | 4 | 100 | — | — | — | — |
| Mallory Thatcher | 0 | 2 | — | — | — | — | — |
| Allan Barrett | 2 | 10 | 400 | — | — | — | — |
| Colton Jones | 0 | 3 | — | — | — | — | — |
| Paula Dunklin | 0 | 10 | — | — | — | — | — |
| Celina Leopard | 0 | 1 | — | — | — | — | — |
| Brooke Hopton-Jones | 1 | 8 | 700 | — | — | — | — |
| Brent Sanders | 6 | 0 | -100 | — | — | — | — |
| Ryan Whitman | 1 | 3 | 200 | — | — | — | — |
| Sateesh Donti | 0 | 1 | — | — | — | — | — |
| Ashley West-Rogers | 1 | 0 | -100 | — | — | — | — |

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-43_results.md

(not present — file does not exist or is empty)

### Q-43_step2_results.md

# Q-43-S2 Results — Gabby (gh, org_id=55)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-51_results.md

# Q-51 Results — Gabby (gh, org_id=55)
- **Query**: Q-51 — Rep-Level eCat Capture
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 25
- **Run date**: 2026-06-17


| rep_name | rep_number | erp_orders | erp_gmv | erp_customers | ecat_orders | ecat_gmv | ecat_customers | ecat_capture_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ryan Casabella | MW-RYANC | 2,706 | $6.1M | 229 | 1,173 | $5.5M | 167 | 90.60 |
| SO: Paul Bentley | SO-PAUL | 2,164 | $4.9M | 270 | 0 | $0 | 0 | 0 |
| Vacant | V | 6,040 | $4.6M | 20 | 0 | $0 | 0 | 0 |
| SO: Heather Robert | SO-HEATHERR | 1,947 | $3.8M | 255 | 0 | $0 | 0 | 0 |
| Denae Copeland | TX-DENAEC | 1,239 | $2.6M | 127 | 367 | $1.1M | 75 | 43.60 |
| SO: Clare Ross | SO-CLARER | 1,216 | $2.4M | 134 | 0 | $0 | 0 | 0 |
| MA: Wynne White | MA-WYNNEW | 1,180 | $2.1M | 92 | 0 | $0 | 0 | 0 |
| Jeremy Rago | UMW-JEREMYR | 1,403 | $1.9M | 93 | 194 | $745,300 | 46 | 38.50 |
| Allison Wooley | TX-ALLISONW | 816 | $1.7M | 139 | 363 | $1.3M | 78 | 78 |
| MA: David Sherrill | MA-DAVIDS | 932 | $1.6M | 113 | 0 | $0 | 0 | 0 |
| TX: Anne Leonard | TX-ANNEL | 630 | $1.3M | 218 | 0 | $0 | 0 | 0 |
| MA: Rick Scott | MA-RICKS | 734 | $1.3M | 147 | 0 | $0 | 0 | 0 |
| FL: Diana Horsley | FL-DIANAH | 604 | $1.2M | 107 | 0 | $0 | 0 | 0 |
| Cat Freund | LMW-CATF | 610 | $1.1M | 93 | 218 | $548,312 | 55 | 48.20 |
| Tanya Houge | MW-TANYAH | 502 | $830,135 | 122 | 376 | $1.2M | 89 | 145.10 |
| Jobey Tudor | RM-JOBEYT | 321 | $723,285 | 80 | 19 | $59,929 | 9 | 8.30 |
| SO: Robert Robinson | SO-ROBR | 304 | $704,601 | 47 | 0 | $0 | 0 | 0 |
| House | 1 | 462 | $654,327 | 16 | 0 | $0 | 0 | 0 |
| Sarah Balducci | FL-SARAHB | 267 | $618,987 | 81 | 202 | $1.1M | 45 | 179.70 |
| NE: Chad Forti | NE-CHADF | 394 | $585,085 | 133 | 0 | $0 | 0 | 0 |
| Howard Cohen | SW-HOWARDC | 227 | $494,019 | 72 | 89 | $330,112 | 32 | 66.80 |
| Margaux Toothman | NCA-MARGAUXT | 99 | $162,310 | 37 | 55 | $56,196 | 23 | 34.60 |
| Katie Willoughby | SO-KATIEW | 50 | $101,817 | 15 | 192 | $1.3M | 47 | 1,306.90 |
| WCAN: Doug Wasserman | WCAN-DOUGW | 36 | $95,707 | 11 | 0 | $0 | 0 | 0 |
| Kim Drye | SO-KIMD | 16 | $19,706 | 4 | 46 | $332,548 | 16 | 1,687.60 |

### Q-62_results.md

# Q-62 Results — Gabby (gh, org_id=55)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 10
- **Run date**: 2026-06-17


| rep_name | new_items_sold | total_new_items | adoption_pct | customers_buying_new | new_item_qty | new_item_revenue | orders_with_new_items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SO: Paul Bentley | 2 | 27 | 7.40 | 4 | 10 | 3,605 | 4 |
| SO: Heather Robert | 1 | 27 | 3.70 | 2 | 8 | 2,620 | 2 |
| FL: Diana Horsley | 2 | 27 | 7.40 | 2 | 3 | 1,199 | 2 |
| Allison Wooley | 2 | 27 | 7.40 | 2 | 2 | 1,184 | 2 |
| Denae Copeland | 1 | 27 | 3.70 | 1 | 4 | 1,176 | 1 |
| Howard Cohen | 1 | 27 | 3.70 | 1 | 2 | 1,162 | 1 |
| Ryan Casabella | 1 | 27 | 3.70 | 1 | 3 | 834 | 1 |
| Jeremy Rago | 1 | 27 | 3.70 | 1 | 2 | 618 | 1 |
| MA: David Sherrill | 1 | 27 | 3.70 | 1 | 1 | 581 | 1 |
| Vacant | 1 | 27 | 3.70 | 1 | 0 | 0 | 1 |

### Q-63_results.md

# Q-63 Results — Gabby (gh, org_id=55)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| sc-clarer | 74 | 1,480 | 183 | 247.30 | 12.40 | 1,465 | 15 | 0 |
| pbe | 90 | 1,461 | 207 | 230 | 14.20 | 1,440 | 21 | 0 |
| sc-annel | 93 | 1,286 | 238 | 255.90 | 18.50 | 1,255 | 24 | 7 |
| sc-ryanc | 88 | 1,117 | 260 | 295.50 | 23.30 | 1,117 | 0 | 0 |
| hr | 76 | 1,031 | 189 | 248.70 | 18.30 | 1,029 | 0 | 2 |
| sc-margos | 52 | 702 | 105 | 201.90 | 15 | 700 | 0 | 2 |
| zww | 38 | 669 | 118 | 310.50 | 17.60 | 663 | 5 | 1 |
| sc-davids | 32 | 590 | 60 | 187.50 | 10.20 | 590 | 0 | 0 |
| rrobinson | 34 | 587 | 64 | 188.20 | 10.90 | 584 | 2 | 1 |
| rs | 51 | 545 | 46 | 90.20 | 8.40 | 543 | 1 | 1 |
| sc-tanyah | 40 | 457 | 73 | 182.50 | 16 | 450 | 0 | 7 |
| sc-allisonw | 40 | 419 | 113 | 282.50 | 27 | 419 | 0 | 0 |
| sc-denaec | 30 | 353 | 84 | 280 | 23.80 | 350 | 3 | 0 |
| sc-kellym | 34 | 319 | 16 | 47.10 | 5 | 314 | 1 | 4 |
| sc-dianah | 25 | 251 | 70 | 280 | 27.90 | 246 | 5 | 0 |
| sc-katiewilloughby | 17 | 226 | 32 | 188.20 | 14.20 | 226 | 0 | 0 |
| sc-benjaminf | 21 | 223 | 22 | 104.80 | 9.90 | 223 | 0 | 0 |
| sc-catf | 19 | 212 | 49 | 257.90 | 23.10 | 208 | 4 | 0 |
| jeremyr | 8 | 195 | 29 | 362.50 | 14.90 | 195 | 0 | 0 |
| sc-margauxt | 19 | 183 | 21 | 110.50 | 11.50 | 183 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Gabby (gh, org_id=55)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| sc-clarer | 169 | 22.60 | 2.80 | 99 | 19 |
| sc-davids | 95 | 17.60 | 2.90 | 53 | 5 |
| sc-ryanc | 226 | 17.50 | 2.70 | 134 | 23 |
| zww | 146 | 16.80 | 2.30 | 77 | 12 |
| sc-annel | 167 | 16.20 | 2.30 | 89 | 29 |
| sc-denaec | 94 | 15.80 | 3 | 51 | 12 |
| pbe | 199 | 15.60 | 2.30 | 104 | 26 |
| hr | 156 | 15.20 | 2.50 | 78 | 22 |
| rrobinson | 88 | 15.20 | 1.80 | 40 | 13 |
| sc-katiewilloughby | 34 | 15.10 | 1.80 | 22 | 1 |
| sc-allisonw | 109 | 14.70 | 2.80 | 58 | 17 |
| rs | 102 | 14.60 | 2.10 | 66 | 10 |
| sc-margos | 145 | 14.50 | 1.70 | 67 | 15 |
| sc-crystalg | 4 | 14 | 2.50 | 3 | 0 |
| sc-dwasserman | 61 | 13.20 | 2.70 | 21 | 23 |
| sc-jobeyt | 52 | 13.10 | 2.30 | 27 | 11 |
| sc-tradeshow2 | 3 | 13 | 1.70 | 2 | 0 |
| sc-dianah | 124 | 12.80 | 2 | 62 | 15 |
| jeremyr | 28 | 12.60 | 1.60 | 7 | 10 |
| sc-kellym | 82 | 11.90 | 1.40 | 46 | 15 |

### Q-65_results.md

# Q-65 Results — Gabby (gh, org_id=55)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| sc-annel | 5,935 | 5,002 | 933 | 84.30 | 15.70 |
| pbe | 4,250 | 3,573 | 677 | 84.10 | 15.90 |
| sc-margos | 2,548 | 2,119 | 429 | 83.20 | 16.80 |
| sc-savannad | 887 | 736 | 151 | 83 | 17 |
| sc-clarer | 4,139 | 3,413 | 726 | 82.50 | 17.50 |
| sc-kellym | 1,600 | 1,318 | 282 | 82.40 | 17.60 |
| hr | 3,615 | 2,913 | 702 | 80.60 | 19.40 |
| zww | 2,710 | 2,182 | 528 | 80.50 | 19.50 |
| sc-allisonw | 2,574 | 2,046 | 528 | 79.50 | 20.50 |
| rrobinson | 1,704 | 1,334 | 370 | 78.30 | 21.70 |
| sc-tanyah | 2,565 | 2,005 | 560 | 78.20 | 21.80 |
| sc-katiewilloughby | 850 | 663 | 187 | 78 | 22 |
| sc-mandyp | 662 | 515 | 147 | 77.80 | 22.20 |
| sc-catf | 1,325 | 1,008 | 317 | 76.10 | 23.90 |
| sc-ryanc | 4,742 | 3,592 | 1,150 | 75.70 | 24.30 |
| sc-howardc | 1,196 | 886 | 310 | 74.10 | 25.90 |
| sc-tradeshow2 | 69 | 51 | 18 | 73.90 | 26.10 |
| sc-margaretm | 45 | 33 | 12 | 73.30 | 26.70 |
| sc-jonaht | 60 | 43 | 17 | 71.70 | 28.30 |
| sc-sarahb | 1,406 | 981 | 425 | 69.80 | 30.20 |

### Q-70_results.md

# Q-70 Results — Gabby (gh, org_id=55)
- **Query**: Q-70 — Inactive Reps with Territory Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — Gabby (gh, org_id=55)
- **Run date**: 2026-06-17
- **Total flagged**: 0
- **Aggregate GMV**: $0

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### user_group_mapping.md

# User Group Mapping — Gabby (gh, org_id=55)
- **Run date**: 2026-06-17
- **Total Postgres users**: 7984
- **Matched to Mixpanel (Q-01 Step 1)**: 65 of 95 (68%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Customer Portal | other | 7863 |
| Employee - Customer Service | admin_internal | 49 |
| Reps | field_rep | 28 |
| Reps - All Accounts | field_rep | 13 |
| z-SuperCat  | admin_internal | 13 |
| Automation | admin_internal | 5 |
| Employee - Admin | admin_internal | 4 |
| Customer Portal View Only | other | 3 |
| Employee - User Setup | other | 2 |
| Customer Portal | admin_internal | 1 |
| Employee - Customer Service + Approve Logins | admin_internal | 1 |
| Kiosk Mode | other | 1 |
| Meridian | other | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 39 | 306,844 | 97.0% |
| admin_internal | 25 | 9,391 | 3.0% |
| other | 1 | 92 | 0.0% |
