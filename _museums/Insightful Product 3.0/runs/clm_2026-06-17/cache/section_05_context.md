# Section 5 Context Bundle — Crystorama (clm)
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
| 9 | SIG-COMMERCE-01 | Digital order enablement — eCat handles 1.4% of $40M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix) | P0 | §4 Commerce | 4.9 | $403,000 | 3.0 | 5,962,242 | POSITIVE |
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
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Digital order enablement — eCat handles 1.4% of $40M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix)
4. **[POSITIVE/MOMENTUM]** SIG-MOM-01: Account Acceleration — Crystorama Accm 2 consecutive QoQ acceleration quarters, $61,836 peak quarter (+432% QoQ)
5. **[RISK]** SIG-ANOMALY-02: Stock Out — HAY-1417-AG (Hayes 50'' Aged Brass Linear Chandelier) $491,812 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — ADD-317-AG-CL (Addis 51.75'' Aged Brass Linear Chandeli) $296,813 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — SHY-10907-SG (Shyla 24'' Soft Gold Chandelier) $292,247 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### coaching_candidates.md

# Coaching Candidates — Crystorama (clm)

Deterministically computed by detect_signals.py. The section agent renders
these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,
or add reps. Archetype framing + narrative are written by the agent; the rep
set and the estimated upside dollar figures are fixed here.

- **Benchmark**: n/a
- **Qualifying reps (>= 50 presentations)**: 6 (0 converting)
- **Upside floor**: $50,000
- **Candidates above floor**: 0

**No coaching cards for this client — render NO coaching cards and NO coaching rollup callout.** Reason: No qualifying rep converts (>0%) — no benchmark to measure against.

### Q-01_step1_results.md

# Q-01-S1 Results — Crystorama (clm, org_id=64)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 100
- **Run date**: 2026-06-17


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| steven | 382 | 6,023 | 2024-11-01 15:33 | 2026-06-16 14:29 | 2,250 | 371 | 1,879 | 787 | 737 | 1 | 0 | 0 | 0 | 0 | 8 | 1 | 7 | 0 | 700 | 693 | 66 | 2 | 0 | 0 | 9 | 18 | 0 |
| bkrieger | 462 | 5,901 | 2024-11-01 07:57 | 2026-06-16 10:59 | 1,192 | 365 | 827 | 659 | 634 | 22 | 0 | 0 | 0 | 0 | 15 | 4 | 10 | 1 | 394 | 371 | 239 | 18 | 0 | 1 | 1 | 22 | 0 |
| zrapp | 356 | 4,779 | 2024-11-01 09:53 | 2026-06-16 09:25 | 844 | 338 | 506 | 983 | 935 | 16 | 0 | 0 | 0 | 0 | 49 | 17 | 30 | 2 | 438 | 353 | 445 | 16 | 0 | 0 | 10 | 107 | 0 |
| chardy | 258 | 3,990 | 2024-11-01 15:43 | 2026-06-16 16:20 | 180 | 173 | 7 | 1,534 | 1,109 | 72 | 0 | 0 | 0 | 0 | 179 | 105 | 69 | 5 | 49 | 47 | 21 | 89 | 0 | 3 | 0 | 2 | 0 |
| asharma | 83 | 3,595 | 2024-11-04 12:04 | 2026-06-11 11:39 | 93 | 33 | 60 | 2,955 | 2,811 | 48 | 0 | 0 | 0 | 0 | 76 | 6 | 53 | 1 | 65 | 65 | 13 | 25 | 0 | 0 | 0 | 5 | 0 |
| jpnich | 195 | 3,284 | 2024-11-01 08:55 | 2026-06-11 12:07 | 260 | 150 | 110 | 619 | 582 | 20 | 0 | 0 | 0 | 0 | 51 | 0 | 51 | 0 | 56 | 56 | 2 | 219 | 0 | 2 | 0 | 9 | 0 |
| vinceh | 197 | 2,454 | 2024-11-01 15:01 | 2026-06-11 19:10 | 137 | 70 | 67 | 597 | 597 | 0 | 0 | 0 | 0 | 0 | 87 | 41 | 45 | 1 | 180 | 178 | 11 | 172 | 0 | 6 | 1 | 56 | 0 |
| ptheos | 216 | 2,164 | 2024-11-05 18:42 | 2026-06-06 08:35 | 455 | 304 | 151 | 729 | 722 | 7 | 0 | 0 | 0 | 0 | 7 | 6 | 0 | 1 | 103 | 103 | 14 | 0 | 0 | 0 | 13 | 108 | 0 |
| ryanranzino | 161 | 1,962 | 2024-11-01 12:06 | 2026-06-14 21:55 | 21 | 8 | 13 | 726 | 708 | 17 | 0 | 0 | 0 | 0 | 41 | 18 | 15 | 0 | 113 | 107 | 6 | 79 | 0 | 0 | 0 | 6 | 0 |
| ktaylor | 286 | 1,831 | 2024-11-01 15:51 | 2026-06-16 08:10 | 141 | 72 | 69 | 454 | 449 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 196 | 186 | 237 | 0 | 0 | 0 | 0 | 0 | 0 |
| megany | 132 | 1,824 | 2024-11-01 15:53 | 2026-06-12 09:37 | 124 | 58 | 66 | 300 | 273 | 11 | 0 | 0 | 0 | 0 | 46 | 4 | 39 | 3 | 146 | 145 | 2 | 132 | 0 | 0 | 0 | 0 | 0 |
| katymccully | 203 | 1,695 | 2024-11-04 08:52 | 2026-06-08 11:06 | 189 | 128 | 61 | 574 | 571 | 3 | 0 | 0 | 0 | 0 | 9 | 0 | 9 | 0 | 204 | 204 | 9 | 9 | 0 | 0 | 3 | 21 | 0 |
| amymatteson | 220 | 1,668 | 2024-11-08 17:22 | 2026-06-08 14:11 | 578 | 194 | 384 | 329 | 313 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 151 | 145 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| nickbrown | 157 | 1,636 | 2024-11-01 07:54 | 2026-06-03 15:01 | 135 | 25 | 110 | 493 | 424 | 7 | 0 | 0 | 0 | 0 | 20 | 0 | 20 | 0 | 235 | 233 | 39 | 42 | 0 | 0 | 0 | 7 | 0 |
| robantonecchia | 220 | 1,574 | 2024-11-04 06:11 | 2026-06-16 11:57 | 191 | 78 | 113 | 398 | 373 | 25 | 0 | 0 | 0 | 0 | 18 | 0 | 18 | 0 | 235 | 231 | 55 | 2 | 0 | 0 | 3 | 16 | 0 |
| cindyvackar | 222 | 1,504 | 2024-11-01 15:54 | 2026-06-08 12:17 | 211 | 209 | 2 | 525 | 525 | 0 | 0 | 0 | 0 | 0 | 19 | 16 | 3 | 0 | 122 | 111 | 5 | 4 | 0 | 0 | 6 | 6 | 0 |
| kyork | 148 | 1,491 | 2024-11-01 13:23 | 2026-06-16 09:43 | 127 | 66 | 61 | 347 | 338 | 1 | 0 | 0 | 0 | 0 | 14 | 1 | 13 | 0 | 125 | 121 | 17 | 28 | 0 | 0 | 4 | 9 | 0 |
| mtrosclair | 40 | 1,478 | 2024-11-04 12:07 | 2026-02-17 08:27 | 96 | 22 | 74 | 1,005 | 1,003 | 1 | 0 | 0 | 0 | 0 | 17 | 2 | 15 | 0 | 16 | 16 | 9 | 3 | 0 | 0 | 10 | 12 | 0 |
| dunnlighting | 227 | 1,444 | 2024-11-05 19:16 | 2026-06-16 12:15 | 208 | 99 | 109 | 180 | 149 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 5 | 0 | 231 | 221 | 135 | 2 | 0 | 0 | 0 | 1 | 0 |
| cframburg | 132 | 1,409 | 2024-11-06 11:02 | 2026-06-11 17:22 | 15 | 9 | 6 | 402 | 401 | 1 | 0 | 0 | 0 | 0 | 35 | 1 | 34 | 0 | 143 | 129 | 31 | 115 | 0 | 8 | 0 | 0 | 0 |
| cindyr | 237 | 1,407 | 2024-11-01 12:42 | 2026-06-10 14:32 | 98 | 98 | 0 | 171 | 162 | 9 | 0 | 0 | 0 | 0 | 89 | 65 | 23 | 1 | 156 | 103 | 18 | 38 | 0 | 0 | 0 | 4 | 0 |
| stevelinder | 193 | 1,313 | 2024-11-15 09:43 | 2026-06-16 08:39 | 18 | 18 | 0 | 255 | 254 | 1 | 0 | 0 | 0 | 0 | 23 | 23 | 0 | 0 | 231 | 195 | 65 | 10 | 0 | 3 | 1 | 10 | 0 |
| kcavanagh | 204 | 1,242 | 2024-11-01 11:24 | 2026-06-15 12:18 | 144 | 129 | 15 | 343 | 342 | 1 | 0 | 0 | 0 | 0 | 38 | 27 | 11 | 0 | 168 | 163 | 1 | 4 | 0 | 0 | 0 | 3 | 0 |
| rrobert | 211 | 1,237 | 2024-11-04 10:53 | 2026-06-11 15:12 | 56 | 49 | 7 | 248 | 246 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 139 | 133 | 160 | 0 | 0 | 0 | 0 | 5 | 0 |
| mberesford | 167 | 1,202 | 2024-11-01 09:13 | 2025-11-12 10:15 | 270 | 42 | 228 | 135 | 131 | 2 | 0 | 0 | 0 | 0 | 5 | 4 | 1 | 0 | 264 | 258 | 21 | 0 | 0 | 0 | 4 | 14 | 0 |
| forrestdenbow | 120 | 1,155 | 2024-11-04 11:46 | 2026-06-11 13:37 | 45 | 37 | 8 | 599 | 599 | 0 | 0 | 0 | 0 | 0 | 45 | 37 | 8 | 0 | 116 | 109 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| shelly | 158 | 1,128 | 2024-11-01 13:55 | 2026-06-12 23:42 | 107 | 55 | 52 | 174 | 172 | 0 | 0 | 0 | 0 | 0 | 17 | 7 | 9 | 1 | 196 | 171 | 38 | 1 | 0 | 0 | 0 | 4 | 0 |
| mpoire | 164 | 1,100 | 2024-11-01 15:35 | 2026-06-15 15:16 | 2 | 2 | 0 | 232 | 224 | 8 | 0 | 0 | 0 | 0 | 13 | 12 | 1 | 0 | 291 | 283 | 62 | 9 | 0 | 0 | 0 | 0 | 0 |
| eduardoa | 161 | 1,085 | 2024-11-05 16:20 | 2026-06-15 17:07 | 92 | 34 | 58 | 274 | 274 | 0 | 0 | 0 | 0 | 0 | 8 | 5 | 3 | 0 | 173 | 157 | 10 | 4 | 0 | 0 | 0 | 8 | 0 |
| aframburg | 106 | 1,013 | 2024-11-12 11:35 | 2026-06-08 10:22 | 306 | 90 | 216 | 289 | 285 | 3 | 0 | 0 | 0 | 0 | 11 | 0 | 10 | 1 | 52 | 52 | 0 | 27 | 0 | 0 | 0 | 0 | 0 |
| gellis | 143 | 950 | 2024-11-05 16:33 | 2026-06-16 18:41 | 52 | 27 | 25 | 121 | 117 | 3 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 349 | 328 | 11 | 4 | 0 | 0 | 0 | 1 | 0 |
| stevejones | 186 | 950 | 2024-11-11 13:32 | 2026-06-16 11:29 | 27 | 24 | 3 | 89 | 83 | 5 | 0 | 0 | 0 | 0 | 15 | 15 | 0 | 0 | 125 | 109 | 157 | 0 | 0 | 0 | 0 | 17 | 0 |
| bdobson2 | 40 | 734 | 2025-06-12 15:15 | 2026-04-27 09:44 | 99 | 28 | 71 | 223 | 222 | 1 | 0 | 0 | 0 | 0 | 12 | 0 | 12 | 0 | 127 | 110 | 12 | 7 | 0 | 0 | 0 | 4 | 0 |
| jrichenburg | 108 | 697 | 2024-11-01 08:50 | 2026-06-01 11:21 | 26 | 20 | 6 | 284 | 284 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 2 | 0 | 79 | 78 | 11 | 1 | 0 | 0 | 0 | 6 | 0 |
| mlights | 112 | 689 | 2024-11-02 11:25 | 2026-06-10 15:04 | 33 | 1 | 32 | 67 | 59 | 8 | 0 | 0 | 0 | 0 | 25 | 24 | 0 | 1 | 194 | 76 | 67 | 0 | 0 | 0 | 0 | 0 | 0 |
| stephencaplight | 53 | 678 | 2024-11-07 07:31 | 2026-06-01 15:43 | 34 | 24 | 10 | 211 | 207 | 2 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 202 | 188 | 1 | 3 | 0 | 0 | 1 | 3 | 0 |
| classoff | 95 | 664 | 2024-11-15 14:03 | 2026-06-16 11:18 | 50 | 38 | 12 | 245 | 245 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 106 | 105 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| jskula | 56 | 656 | 2024-12-30 11:21 | 2026-05-08 12:25 | 61 | 31 | 30 | 138 | 134 | 4 | 0 | 0 | 0 | 0 | 8 | 8 | 0 | 0 | 139 | 127 | 9 | 11 | 0 | 0 | 5 | 22 | 0 |
| jmckinley | 103 | 638 | 2024-11-11 09:34 | 2026-05-27 07:30 | 52 | 24 | 28 | 106 | 106 | 0 | 0 | 0 | 0 | 0 | 5 | 1 | 4 | 0 | 170 | 170 | 3 | 1 | 0 | 0 | 3 | 7 | 0 |
| jessicam | 71 | 595 | 2024-11-04 09:56 | 2026-06-16 12:48 | 200 | 39 | 161 | 88 | 87 | 0 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 69 | 69 | 9 | 2 | 0 | 0 | 0 | 1 | 0 |

*(Truncated: showing top 40 of 100 rows. Full data in cache file.)*

### Q-01_step2_results.md

# Q-01-S2 Results — Crystorama (clm, org_id=64)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 30
- **Run date**: 2026-06-17


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Jeff Nicholson | 20 | $73,197 | $3,660 | 20 |
| Chas Lassoff | 11 | $58,374 | $5,307 | 7 |
| Steve Linder | 6 | $56,623 | $9,437 | 5 |
| Katy McCully | 38 | $56,371 | $1,483 | 16 |
| Brad Dobson | 4 | $49,831 | $12,458 | 4 |
| Vince  Hall | 9 | $34,470 | $3,830 | 9 |
| Megan  Trosclair | 5 | $28,132 | $5,626 | 5 |
| Matt Sullivan | 11 | $24,584 | $2,235 | 9 |
| Mike Hemsarth | 5 | $22,616 | $4,523 | 2 |
| Zachary Rapp | 11 | $22,434 | $2,039 | 5 |
| Shelly Orban | 6 | $19,845 | $3,308 | 5 |
| Cindy Vackar | 2 | $16,792 | $8,396 | 2 |
| Jeff Izower | 3 | $12,496 | $4,165 | 1 |
| Forrest Denbow | 2 | $10,988 | $5,494 | 1 |
| HighPoint Showroom | 2 | $8,084 | $4,042 | 1 |
| Collin Framburg | 2 | $7,338 | $3,669 | 1 |
| Nick Brown | 2 | $6,876 | $3,438 | 2 |
| Brad Krieger | 2 | $6,348 | $3,174 | 2 |
| Kevin  Taylor | 2 | $6,155 | $3,078 | 2 |
| Kelly York | 2 | $6,021 | $3,011 | 2 |
| Pauline Theos | 1 | $4,573 | $4,573 | 1 |
| Amy Matteson | 5 | $4,206 | $841 | 2 |
| Kristen Cavanagh | 1 | $3,362 | $3,362 | 1 |
| Rob Hailpern | 1 | $2,813 | $2,813 | 1 |
| Sebastian Castrillon | 1 | $2,650 | $2,650 | 1 |
| Cindy Rogers | 5 | $2,560 | $512 | 4 |
| Gary Ellis | 1 | $1,320 | $1,320 | 1 |
| Steve Jones | 3 | $1,199 | $400 | 2 |
| Amit Sharma | 1 | $1,148 | $1,148 | 1 |
| Dunn Lighting | 1 | $316 | $316 | 1 |

### Q-04_results.md

# Q-04 Results — Crystorama (clm, org_id=64)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 100
- **Run date**: 2026-06-17


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| steven | 382 | 6,023 | 0 | 737 | 693 | 7 | 7 | 0 | 66 | 2 | Content/Library Manager |
| bkrieger | 462 | 5,901 | 0 | 634 | 371 | 23 | 10 | 0 | 239 | 19 | Content/Library Manager |
| zrapp | 356 | 4,779 | 0 | 935 | 353 | 85 | 30 | 0 | 445 | 16 | Content/Library Manager |
| chardy | 258 | 3,990 | 0 | 1,109 | 47 | 2 | 69 | 0 | 21 | 92 | Catalog/Data Manager |
| asharma | 83 | 3,595 | 0 | 2,811 | 65 | 0 | 53 | 16 | 13 | 25 | Catalog/Data Manager |
| jpnich | 195 | 3,284 | 0 | 582 | 56 | 0 | 51 | 0 | 2 | 221 | Catalog/Data Manager |
| vinceh | 197 | 2,454 | 0 | 597 | 178 | 2 | 45 | 0 | 11 | 178 | Catalog/Data Manager |
| ptheos | 216 | 2,164 | 0 | 722 | 103 | 0 | 0 | 0 | 14 | 0 | Sales Support/Inside Sales |
| ryanranzino | 161 | 1,962 | 0 | 708 | 107 | 6 | 15 | 8 | 6 | 79 | Merchandising/List Curator |
| ktaylor | 286 | 1,831 | 0 | 449 | 186 | 10 | 1 | 0 | 237 | 0 | Analytics/Portal User |
| megany | 132 | 1,824 | 0 | 273 | 145 | 1 | 39 | 0 | 2 | 132 | Catalog/Data Manager |
| katymccully | 203 | 1,695 | 0 | 571 | 204 | 0 | 9 | 0 | 9 | 9 | Content/Library Manager |
| amymatteson | 220 | 1,668 | 0 | 313 | 145 | 6 | 0 | 0 | 4 | 0 | Sales Support/Inside Sales |
| nickbrown | 157 | 1,636 | 0 | 424 | 233 | 2 | 20 | 0 | 39 | 42 | Content/Library Manager |
| robantonecchia | 220 | 1,574 | 0 | 373 | 231 | 4 | 18 | 0 | 55 | 2 | Content/Library Manager |
| cindyvackar | 222 | 1,504 | 0 | 525 | 111 | 11 | 3 | 0 | 5 | 4 | Sales Support/Inside Sales |
| kyork | 148 | 1,491 | 0 | 338 | 121 | 4 | 13 | 0 | 17 | 28 | Sales Support/Inside Sales |
| mtrosclair | 40 | 1,478 | 0 | 1,003 | 16 | 0 | 15 | 0 | 9 | 3 | Sales Support/Inside Sales |
| dunnlighting | 227 | 1,444 | 0 | 149 | 221 | 10 | 5 | 0 | 135 | 2 | Content/Library Manager |
| cframburg | 132 | 1,409 | 0 | 401 | 129 | 14 | 34 | 0 | 31 | 123 | Catalog/Data Manager |
| cindyr | 237 | 1,407 | 0 | 162 | 103 | 53 | 23 | 0 | 18 | 38 | Content/Library Manager |
| stevelinder | 193 | 1,313 | 0 | 254 | 195 | 36 | 0 | 0 | 65 | 13 | Content/Library Manager |
| kcavanagh | 204 | 1,242 | 0 | 342 | 163 | 5 | 11 | 0 | 1 | 4 | Sales Support/Inside Sales |
| rrobert | 211 | 1,237 | 0 | 246 | 133 | 6 | 0 | 0 | 160 | 0 | Analytics/Portal User |
| mberesford | 167 | 1,202 | 0 | 131 | 258 | 6 | 1 | 0 | 21 | 0 | Content/Library Manager |
| forrestdenbow | 120 | 1,155 | 0 | 599 | 109 | 7 | 8 | 0 | 1 | 0 | Sales Support/Inside Sales |
| shelly | 158 | 1,128 | 0 | 172 | 171 | 25 | 9 | 0 | 38 | 1 | Content/Library Manager |
| mpoire | 164 | 1,100 | 0 | 224 | 283 | 8 | 1 | 0 | 62 | 9 | Content/Library Manager |
| eduardoa | 161 | 1,085 | 0 | 274 | 157 | 16 | 3 | 0 | 10 | 4 | Sales Support/Inside Sales |
| aframburg | 106 | 1,013 | 0 | 285 | 52 | 0 | 10 | 0 | 0 | 27 | Sales Support/Inside Sales |
| gellis | 143 | 950 | 0 | 117 | 328 | 21 | 4 | 0 | 11 | 4 | Content/Library Manager |
| stevejones | 186 | 950 | 0 | 83 | 109 | 16 | 0 | 0 | 157 | 0 | Analytics/Portal User |
| bdobson2 | 40 | 734 | 0 | 222 | 110 | 17 | 12 | 0 | 12 | 7 | Sales Support/Inside Sales |
| jrichenburg | 108 | 697 | 0 | 284 | 78 | 1 | 2 | 0 | 11 | 1 | Sales Support/Inside Sales |
| mlights | 112 | 689 | 0 | 59 | 76 | 118 | 0 | 0 | 67 | 0 | Content/Library Manager |
| stephencaplight | 53 | 678 | 0 | 207 | 188 | 14 | 0 | 0 | 1 | 3 | Sales Support/Inside Sales |
| classoff | 95 | 664 | 0 | 245 | 105 | 1 | 1 | 0 | 3 | 0 | Sales Support/Inside Sales |
| jskula | 56 | 656 | 0 | 134 | 127 | 12 | 0 | 0 | 9 | 11 | Sales Support/Inside Sales |
| jmckinley | 103 | 638 | 0 | 106 | 170 | 0 | 4 | 0 | 3 | 1 | Sales Support/Inside Sales |
| jessicam | 71 | 595 | 0 | 87 | 69 | 0 | 3 | 0 | 9 | 2 | Sales Support/Inside Sales |
| donporter | 67 | 586 | 0 | 68 | 128 | 9 | 13 | 0 | 1 | 9 | Sales Support/Inside Sales |
| brucekremer | 108 | 561 | 0 | 164 | 56 | 10 | 0 | 0 | 4 | 2 | Sales Support/Inside Sales |
| smicheal | 68 | 503 | 0 | 154 | 8 | 0 | 0 | 0 | 0 | 0 | Sales Support/Inside Sales |
| eric_m | 49 | 471 | 0 | 73 | 50 | 1 | 15 | 0 | 2 | 32 | Low-Activity User |
| jeffizower | 64 | 470 | 0 | 58 | 144 | 0 | 5 | 0 | 7 | 13 | Low-Activity User |
| rhiggins | 41 | 460 | 0 | 64 | 82 | 1 | 2 | 0 | 0 | 0 | Low-Activity User |
| clscott | 74 | 441 | 0 | 80 | 32 | 0 | 1 | 0 | 2 | 36 | Low-Activity User |
| hpshow | 10 | 379 | 2 | 326 | 0 | 1 | 1 | 2 | 1 | 1 | Inactive |
| hmeador | 68 | 377 | 0 | 67 | 87 | 0 | 3 | 0 | 0 | 2 | Low-Activity User |
| btuminello | 5 | 365 | 0 | 193 | 0 | 0 | 1 | 3 | 0 | 3 | Inactive |
| mseidel | 22 | 354 | 0 | 76 | 125 | 0 | 0 | 0 | 7 | 42 | Inactive |
| mattsullivan | 55 | 341 | 0 | 134 | 4 | 0 | 2 | 0 | 0 | 0 | Low-Activity User |
| ekorn | 112 | 333 | 0 | 24 | 30 | 0 | 0 | 0 | 17 | 1 | Low-Activity User |
| mlieb | 49 | 330 | 0 | 48 | 63 | 0 | 0 | 0 | 2 | 0 | Low-Activity User |
| carlosl | 72 | 329 | 0 | 44 | 30 | 21 | 1 | 0 | 1 | 0 | Content/Library Manager |
| katiewilliams | 13 | 318 | 0 | 88 | 71 | 0 | 5 | 0 | 0 | 0 | Inactive |
| mayerbrian | 23 | 309 | 0 | 54 | 106 | 5 | 0 | 0 | 1 | 8 | Inactive |
| christiet | 22 | 298 | 0 | 44 | 13 | 3 | 8 | 0 | 2 | 27 | Inactive |
| sebastianc | 33 | 251 | 0 | 49 | 67 | 0 | 0 | 0 | 1 | 0 | Low-Activity User |
| philcook | 51 | 250 | 0 | 20 | 65 | 1 | 0 | 0 | 6 | 0 | Low-Activity User |
| lightingvision | 27 | 248 | 0 | 7 | 138 | 0 | 0 | 0 | 0 | 0 | Inactive |
| earp727 | 14 | 242 | 0 | 20 | 10 | 0 | 3 | 0 | 1 | 7 | Inactive |
| debbrahm | 47 | 237 | 0 | 33 | 25 | 0 | 0 | 0 | 12 | 0 | Low-Activity User |
| rhailpern | 26 | 228 | 0 | 77 | 50 | 5 | 0 | 0 | 1 | 0 | Inactive |
| stanf | 23 | 227 | 0 | 4 | 46 | 0 | 0 | 0 | 0 | 2 | Inactive |
| danapoe | 10 | 205 | 0 | 44 | 31 | 0 | 3 | 0 | 1 | 5 | Inactive |
| stevecapitummino | 43 | 191 | 0 | 20 | 50 | 0 | 0 | 0 | 1 | 0 | Low-Activity User |
| trevor_d | 11 | 155 | 0 | 36 | 2 | 0 | 4 | 0 | 1 | 11 | Inactive |
| kelsyej | 18 | 97 | 0 | 2 | 5 | 0 | 2 | 0 | 0 | 0 | Inactive |
| mikehemsarth | 5 | 92 | 0 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| sourceltg | 15 | 81 | 0 | 28 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chermclelland | 11 | 53 | 0 | 1 | 17 | 0 | 0 | 0 | 0 | 0 | Inactive |
| earp27 | 19 | 51 | 0 | 1 | 6 | 0 | 0 | 0 | 4 | 0 | Inactive |
| pmorris | 4 | 45 | 0 | 37 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| calebr | 9 | 44 | 0 | 0 | 26 | 0 | 0 | 0 | 0 | 0 | Inactive |
| aspinelli | 6 | 44 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| zcarranta | 6 | 39 | 0 | 0 | 27 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 5 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mattd | 2 | 26 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| rboyd1 | 3 | 23 | 0 | 3 | 1 | 0 | 0 | 0 | 4 | 0 | Inactive |
| rmckillen | 3 | 20 | 0 | 9 | 0 | 0 | 2 | 0 | 0 | 0 | Inactive |
| dalshow | 5 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| darlene | 4 | 15 | 0 | 0 | 5 | 0 | 0 | 0 | 1 | 0 | Inactive |
| vwalker1 | 6 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jonv | 5 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| mishir1 | 3 | 12 | 0 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dahibbs | 5 | 12 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 5 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| swt | 4 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| daleb | 2 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| j_wilson | 3 | 6 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| alejandrofranco | 2 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mzumbrun | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| robertgarcia | 1 | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dplocki | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| cwiebe | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| khale1 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| des | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| emery | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jlindquist | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Crystorama (clm, org_id=64)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 138 | 60 | 7 |

### Q-06_results.md

# Q-06 Results — Crystorama (clm, org_id=64)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 77
- **Run date**: 2026-06-17


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Katy McCully | 61 | 39 | -36.10 | 17 | 8 | -52.90 | $7,798 |
| Jeff Nicholson | 109 | 37 | -66.10 | 16 | 4 | -75 | $9,452 |
| Sebastian Castrillon | 13 | 1 | -92.30 | 0 | 1 | — | $2,650 |
| Zachary Rapp | 169 | 154 | -8.90 | 4 | 1 | -75 | $560 |
| Kristen Cavanagh | 38 | 28 | -26.30 | 0 | 1 | — | $3,362 |
| Matt Sullivan | 21 | 2 | -90.50 | 6 | 1 | -83.30 | $904 |
| Vince  Hall | 69 | 14 | -79.70 | 7 | 1 | -85.70 | $2,063 |
| Forrest Denbow | 59 | 19 | -67.80 | 2 | 0 | -100 | $0 |
| Kevin  Taylor | 90 | 62 | -31.10 | 2 | 0 | -100 | $0 |
| Shelly Orban | 72 | 26 | -63.90 | 3 | 0 | -100 | $0 |
| Pauline Theos | 59 | 46 | -22 | 1 | 0 | -100 | $0 |
| Brad Dobson | 31 | 1 | -96.80 | 4 | 0 | -100 | $0 |
| Mike Hemsarth | 12 | 0 | -100 | 5 | 0 | -100 | $0 |
| Steve Linder | 50 | 29 | -42 | 6 | 0 | -100 | $0 |
| Steve Jones | 41 | 32 | -22 | 1 | 0 | -100 | $0 |
| Brad Krieger | 324 | 262 | -19.10 | 2 | 0 | -100 | $0 |
| Collin Framburg | 49 | 13 | -73.50 | 2 | 0 | -100 | $0 |
| Jeff Izower | 23 | 2 | -91.30 | 1 | 0 | -100 | $0 |
| Kelly York | 66 | 18 | -72.70 | 2 | 0 | -100 | $0 |
| Cindy Vackar | 81 | 44 | -45.70 | 1 | 0 | -100 | $0 |
| Chas Lassoff | 46 | 9 | -80.40 | 11 | 0 | -100 | $0 |
| Nick Brown | 46 | 22 | -52.20 | 2 | 0 | -100 | $0 |
| Cindy Rogers | 87 | 50 | -42.50 | 1 | 0 | -100 | $0 |
| Megan  Trosclair | 29 | 0 | -100 | 5 | 0 | -100 | $0 |
| Rob Hailpern | 20 | 2 | -90 | 1 | 0 | -100 | $0 |
| Don Porter | 13 | 7 | -46.20 | — | — | — | — |
| Trevor Davidson | 7 | 6 | -14.30 | — | — | — | — |
| Stan Framburg | 4 | 0 | -100 | — | — | — | — |
| Zander Carranta | 6 | 0 | -100 | — | — | — | — |
| Ryan Mckillen | 0 | 4 | — | — | — | — | — |
| Ben Tuminello | 2 | 0 | -100 | — | — | — | — |
| Amit Sharma | 12 | 14 | 16.70 | — | — | — | — |
| Randy Robert | 43 | 54 | 25.60 | — | — | — | — |
| Steve Capitummino | 10 | 5 | -50 | — | — | — | — |
| Kevin Morrison | 30 | 18 | -40 | — | — | — | — |
| Eric Manzo | 14 | 16 | 14.30 | — | — | — | — |
| Rob Antonecchia | 83 | 49 | -41 | — | — | — | — |
| Mindi Seidel | 7 | 1 | -85.70 | — | — | — | — |
| David Hibbs | 2 | 0 | -100 | — | — | — | — |
| Alejandro Franco | 3 | 0 | -100 | — | — | — | — |
| Charles Earp | 1 | 4 | 300 | — | — | — | — |
| Amy Matteson | 48 | 32 | -33.30 | — | — | — | — |
| Matt  Poire | 40 | 31 | -22.50 | — | — | — | — |
| Claire Scott | 15 | 5 | -66.70 | — | — | — | — |
| Shelley Aldridge | 13 | 0 | -100 | — | — | — | — |
| Gary Ellis | 32 | 35 | 9.40 | — | — | — | — |
| Dunn Lighting | 70 | 49 | -30 | — | — | — | — |
| Brent Sanders | 3 | 0 | -100 | — | — | — | — |
| Kelly Burton | 4 | 6 | 50 | — | — | — | — |
| Heather Meador | 10 | 8 | -20 | — | — | — | — |
| Eric Korn | 14 | 18 | 28.60 | — | — | — | — |
| Katie Williams | 29 | 4 | -86.20 | — | — | — | — |
| Jonathan McKinley | 26 | 6 | -76.90 | — | — | — | — |
| Bruce Kremer | 17 | 14 | -17.60 | — | — | — | — |
| Megan Young | 26 | 21 | -19.20 | — | — | — | — |
| Ryan Ranzino | 26 | 20 | -23.10 | — | — | — | — |
| Stephen Capitummino | 10 | 13 | 30 | — | — | — | — |
| Annie Framburg | 20 | 6 | -70 | — | — | — | — |
| Darlene Hibbs | 1 | 0 | -100 | — | — | — | — |
| CLINT HARDY | 67 | 66 | -1.50 | — | — | — | — |
| Eduardo Armenta | 38 | 18 | -52.60 | — | — | — | — |
| Kelsye  Jones | 5 | 0 | -100 | — | — | — | — |
| Stacey  Micheal | 15 | 14 | -6.70 | — | — | — | — |
| Phil Cook | 11 | 5 | -54.50 | — | — | — | — |
| Deborah Brahm | 3 | 1 | -66.70 | — | — | — | — |
| Patrick Brockamp | 9 | 3 | -66.70 | — | — | — | — |
| Steve Ricci | 213 | 211 | -0.90 | — | — | — | — |
| Josh Skula | 15 | 8 | -46.70 | — | — | — | — |
| Jessica - Ricci sales Mason | 20 | 25 | 25 | — | — | — | — |
| John Richenburg | 22 | 7 | -68.20 | — | — | — | — |
| Dallas Showroom | 3 | 0 | -100 | — | — | — | — |
| Emery Rust | 1 | 0 | -100 | — | — | — | — |
| Jimmy  Wilson | 2 | 0 | -100 | — | — | — | — |
| Melissa Leib | 10 | 4 | -60 | — | — | — | — |
| Caleb Reiss | 4 | 0 | -100 | — | — | — | — |
| Robin  Boyd | 1 | 0 | -100 | — | — | — | — |
| Carlos Leon | 6 | 0 | -100 | — | — | — | — |

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-43_results.md

(not present — file does not exist or is empty)

### Q-43_step2_results.md

# Q-43-S2 Results — Crystorama (clm, org_id=64)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-51_results.md

(not present — file does not exist or is empty)

### Q-62_results.md

# Q-62 Results — Crystorama (clm, org_id=64)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-63_results.md

# Q-63 Results — Crystorama (clm, org_id=64)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chardy | 7 | 137 | 0 | 0 | 0 | 125 | 0 | 12 |
| steven | 16 | 109 | 0 | 0 | 0 | 109 | 0 | 0 |
| kcavanagh | 4 | 108 | 0 | 0 | 0 | 108 | 0 | 0 |
| megany | 4 | 94 | 0 | 0 | 0 | 78 | 14 | 2 |
| ptheos | 6 | 93 | 0 | 0 | 0 | 93 | 0 | 0 |
| zrapp | 8 | 84 | 0 | 0 | 0 | 84 | 0 | 0 |
| bkrieger | 8 | 46 | 0 | 0 | 0 | 46 | 0 | 0 |
| bdobson2 | 1 | 45 | 0 | 0 | 0 | 45 | 0 | 0 |
| stephencaplight | 1 | 35 | 0 | 0 | 0 | 35 | 0 | 0 |
| smicheal | 6 | 34 | 0 | 0 | 0 | 34 | 0 | 0 |
| ktaylor | 4 | 25 | 0 | 0 | 0 | 25 | 0 | 0 |
| asharma | 1 | 23 | 0 | 0 | 0 | 23 | 0 | 0 |
| robantonecchia | 5 | 23 | 0 | 0 | 0 | 21 | 2 | 0 |
| dunnlighting | 2 | 19 | 0 | 0 | 0 | 18 | 1 | 0 |
| sourceltg | 2 | 19 | 0 | 0 | 0 | 19 | 0 | 0 |
| jpnich | 3 | 17 | 0 | 0 | 0 | 17 | 0 | 0 |
| katymccully | 2 | 16 | 0 | 0 | 0 | 16 | 0 | 0 |
| sebastianc | 1 | 16 | 0 | 0 | 0 | 16 | 0 | 0 |
| mattsullivan | 1 | 9 | 0 | 0 | 0 | 9 | 0 | 0 |
| jessicam | 2 | 8 | 0 | 0 | 0 | 8 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Crystorama (clm, org_id=64)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| stephencaplight | 1 | 98 | 11 | 1 | 0 |
| bdobson2 | 1 | 45 | 1 | 1 | 0 |
| megany | 9 | 35.20 | 2.40 | 6 | 2 |
| asharma | 1 | 23 | 1 | 1 | 0 |
| chardy | 19 | 20.90 | 1.90 | 8 | 6 |
| eric_m | 2 | 20.50 | 2 | 1 | 0 |
| kcavanagh | 13 | 13.70 | 2.20 | 6 | 4 |
| ptheos | 11 | 13.30 | 2.40 | 5 | 1 |
| zrapp | 38 | 10.50 | 1.90 | 12 | 11 |
| mlieb | 3 | 10 | 1 | 2 | 1 |
| sebastianc | 2 | 9.50 | 1 | 1 | 1 |
| sourceltg | 3 | 9 | 2.70 | 2 | 1 |
| donporter | 5 | 8 | 1 | 2 | 2 |
| mattsullivan | 2 | 7.50 | 2 | 1 | 1 |
| steven | 109 | 7.10 | 1.80 | 38 | 27 |
| eduardoa | 4 | 6.50 | 1 | 1 | 2 |
| nickbrown | 2 | 6 | 1.50 | 1 | 1 |
| dunnlighting | 28 | 5.50 | 1.60 | 5 | 12 |
| jessicam | 17 | 5.10 | 1.40 | 3 | 8 |
| vinceh | 3 | 5 | 1 | 0 | 1 |

### Q-65_results.md

# Q-65 Results — Crystorama (clm, org_id=64)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| bdobson2 | 54 | 52 | 2 | 96.30 | 3.70 |
| sebastianc | 23 | 18 | 5 | 78.30 | 21.70 |
| smicheal | 94 | 73 | 21 | 77.70 | 22.30 |
| jessicam | 194 | 128 | 66 | 66 | 34 |
| ptheos | 262 | 173 | 89 | 66 | 34 |
| sourceltg | 46 | 30 | 16 | 65.20 | 34.80 |
| katymccully | 183 | 113 | 70 | 61.70 | 38.30 |
| rmckillen | 20 | 12 | 8 | 60 | 40 |
| kcavanagh | 219 | 129 | 90 | 58.90 | 41.10 |
| steven | 1,064 | 596 | 468 | 56 | 44 |
| mlieb | 52 | 27 | 25 | 51.90 | 48.10 |
| amymatteson | 138 | 70 | 68 | 50.70 | 49.30 |
| zrapp | 862 | 393 | 469 | 45.60 | 54.40 |
| nickbrown | 108 | 49 | 59 | 45.40 | 54.60 |
| cframburg | 158 | 71 | 87 | 44.90 | 55.10 |
| vinceh | 65 | 29 | 36 | 44.60 | 55.40 |
| philcook | 38 | 16 | 22 | 42.10 | 57.90 |
| chardy | 754 | 305 | 449 | 40.50 | 59.50 |
| robantonecchia | 203 | 81 | 122 | 39.90 | 60.10 |
| brucekremer | 48 | 19 | 29 | 39.60 | 60.40 |

### Q-70_results.md

(not present — file does not exist or is empty)

### showroom_scan_results.md

# Showroom Scan Results — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Total flagged**: 1
- **Aggregate GMV**: $8,084

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |
| HighPoint Showroom | 2 | $8,084 | keyword | confirmed_operational |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### user_group_mapping.md

# User Group Mapping — Crystorama (clm, org_id=64)
- **Run date**: 2026-06-17
- **Total Postgres users**: 772
- **Matched to Mixpanel (Q-01 Step 1)**: 90 of 100 (90%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Customers_Yellow | other | 480 |
| Sales Reps | field_rep | 133 |
| Customers_Blue | other | 77 |
| Customers_Green | other | 31 |
| Internal Employees | admin_internal | 19 |
| z-SuperCat | admin_internal | 12 |
| Customers_Blue | admin_internal | 4 |
| Customers_Quebec | other | 3 |
| Sales Reps | admin_internal | 2 |
| Touchscreen Accounts - Yellow | other | 2 |
| Touchscreen Imap | other | 2 |
| eCat Online Public Site | admin_internal | 2 |
| Customers_Yellow | admin_internal | 1 |
| IMAP | other | 1 |
| Rep (Crysto Staff) | admin_internal | 1 |
| Touchscreen Account - Blue | other | 1 |
| Touchscreen Accounts - Green | other | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 80 | 74,756 | 93.5% |
| admin_internal | 10 | 5,206 | 6.5% |
