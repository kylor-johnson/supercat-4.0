# Section 5 Context Bundle — Craftmade (clli)
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
| 9 | SIG-COMMERCE-01 | Digital order enablement — eCat handles 1.8% of $48M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix) | P0 | §4 Commerce | 4.9 | $477,000 | 3.0 | 7,022,800 | POSITIVE |
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
3. **[POSITIVE/MOMENTUM]** SIG-COMMERCE-01: Digital order enablement — eCat handles 1.8% of $48M total business; streamlining rep-, phone- and email-entered orders into digital commerce is the upside (see channel mix)
4. **[POSITIVE/MOMENTUM]** SIG-OPP-04: New Item Adoption Gap — 30 new items with $0 platform orders
5. **[RISK]** SIG-ANOMALY-02: Stock Out — BW414AG3 (Bellows IV 14" 3-Blade Indoor/Outdoor (D) $281,687 LTM, 0 available
6. **[RISK]** SIG-ANOMALY-02: Stock Out — BW321AG3 (Bellows III 18" 3-Blade Indoor/Outdoor () $266,996 LTM, 0 available
7. **[RISK]** SIG-ANOMALY-02: Stock Out — 50504-FB (Bolden 4 Light Vanity in Flat Black) $193,427 LTM, 0 available

**Balance check**: 4 positive (slots 1-4), 3 risk (slots 5-7). Finding #1 is positive. ✓

## Sections to Skip

None — all sections have ≥1 fired signal or their alternate include gate passes.

### coaching_candidates.md

# Coaching Candidates — Craftmade (clli)

Deterministically computed by detect_signals.py. The section agent renders
these reps as coaching cards EXACTLY as listed — do NOT recompute, re-filter,
or add reps. Archetype framing + narrative are written by the agent; the rep
set and the estimated upside dollar figures are fixed here.

- **Benchmark conversion (top-quartile of converting qualifying reps)**: 1.3%
- **Qualifying reps (>= 50 presentations)**: 7 (2 converting)
- **Upside floor**: $50,000
- **Candidates above floor**: 0

**No coaching cards for this client — render NO coaching cards and NO coaching rollup callout.** Reason: No qualifying rep's estimated upside clears the $50,000 floor (benchmark 1.3%; low AOV / presentation volume).

### Q-01_step1_results.md

# Q-01-S1 Results — Craftmade (clli, org_id=149)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 91
- **Run date**: 2026-06-17


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cathychad | 435 | 9,314 | 2024-11-01 10:13 | 2026-06-16 11:46 | 371 | 227 | 144 | 4,425 | 4,352 | 70 | 0 | 0 | 0 | 0 | 66 | 6 | 60 | 0 | 979 | 944 | 77 | 46 | 0 | 0 | 0 | 20 | 7 |
| broem | 403 | 8,121 | 2024-11-01 10:14 | 2026-06-16 21:56 | 98 | 81 | 17 | 2,189 | 2,189 | 0 | 0 | 0 | 0 | 0 | 278 | 42 | 236 | 0 | 239 | 236 | 5 | 665 | 0 | 130 | 0 | 0 | 28 |
| keith | 309 | 4,901 | 2024-11-01 06:21 | 2026-06-16 08:14 | 792 | 242 | 550 | 1,727 | 1,619 | 105 | 0 | 0 | 0 | 0 | 35 | 4 | 31 | 0 | 810 | 767 | 197 | 7 | 0 | 0 | 0 | 2 | 65 |
| doerenc | 247 | 3,683 | 2024-11-01 12:21 | 2026-06-15 17:01 | 809 | 406 | 403 | 672 | 580 | 90 | 0 | 0 | 0 | 0 | 122 | 0 | 122 | 0 | 499 | 486 | 23 | 0 | 0 | 0 | 0 | 7 | 14 |
| spetty | 111 | 3,566 | 2024-12-17 10:30 | 2026-06-16 09:24 | 203 | 81 | 122 | 178 | 162 | 16 | 0 | 0 | 0 | 0 | 4 | 2 | 2 | 0 | 134 | 130 | 3 | 0 | 0 | 0 | 0 | 3 | 0 |
| rreindl | 448 | 3,484 | 2024-11-01 01:55 | 2026-06-16 18:18 | 42 | 42 | 0 | 541 | 527 | 14 | 0 | 0 | 0 | 0 | 22 | 22 | 0 | 0 | 1,280 | 1,237 | 5 | 0 | 0 | 0 | 3 | 5 | 3 |
| melford | 198 | 3,445 | 2024-11-04 11:48 | 2026-02-06 11:29 | 169 | 153 | 16 | 941 | 911 | 30 | 0 | 0 | 0 | 0 | 34 | 4 | 27 | 3 | 826 | 815 | 15 | 43 | 0 | 1 | 10 | 38 | 23 |
| petercs | 297 | 3,354 | 2024-11-01 16:29 | 2026-06-16 16:38 | 55 | 27 | 28 | 816 | 808 | 7 | 0 | 0 | 0 | 0 | 44 | 38 | 6 | 0 | 1,147 | 1,142 | 145 | 4 | 0 | 0 | 1 | 6 | 6 |
| kellyc | 217 | 3,261 | 2024-11-07 09:37 | 2026-03-31 21:57 | 329 | 110 | 219 | 887 | 844 | 42 | 0 | 0 | 0 | 0 | 49 | 40 | 9 | 0 | 426 | 420 | 128 | 42 | 0 | 0 | 53 | 50 | 8 |
| broche | 299 | 3,122 | 2024-11-06 15:27 | 2026-06-16 07:31 | 220 | 213 | 7 | 1,233 | 1,075 | 158 | 0 | 0 | 0 | 0 | 88 | 1 | 87 | 0 | 246 | 222 | 4 | 75 | 0 | 4 | 10 | 19 | 1 |
| christinew | 351 | 3,084 | 2024-11-01 11:02 | 2026-06-16 15:55 | 108 | 108 | 0 | 1,238 | 1,234 | 4 | 0 | 0 | 0 | 0 | 62 | 0 | 62 | 0 | 146 | 114 | 398 | 1 | 0 | 0 | 0 | 0 | 0 |
| jglatthaar | 344 | 2,979 | 2024-11-01 09:44 | 2026-06-16 10:35 | 125 | 59 | 66 | 787 | 769 | 13 | 0 | 0 | 0 | 0 | 35 | 2 | 33 | 0 | 729 | 672 | 100 | 3 | 0 | 0 | 0 | 3 | 4 |
| lbhuffman | 291 | 2,955 | 2024-11-01 09:59 | 2026-06-16 16:53 | 44 | 35 | 9 | 1,327 | 1,323 | 4 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 213 | 210 | 291 | 7 | 0 | 0 | 0 | 5 | 7 |
| thel70 | 255 | 2,529 | 2024-11-05 10:17 | 2026-06-16 13:57 | 170 | 155 | 15 | 1,046 | 1,043 | 3 | 0 | 0 | 0 | 0 | 18 | 14 | 2 | 2 | 73 | 67 | 5 | 0 | 0 | 0 | 0 | 7 | 13 |
| vlearned2 | 295 | 2,482 | 2024-11-01 12:20 | 2026-06-16 14:57 | 14 | 14 | 0 | 685 | 685 | 0 | 0 | 0 | 0 | 0 | 32 | 8 | 24 | 0 | 495 | 495 | 151 | 12 | 0 | 0 | 0 | 1 | 0 |
| hudsonw | 187 | 2,468 | 2025-02-03 15:01 | 2026-06-16 13:40 | 402 | 162 | 240 | 912 | 911 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 486 | 482 | 83 | 0 | 0 | 0 | 0 | 11 | 20 |
| mitchellk | 361 | 2,366 | 2024-11-01 09:00 | 2026-06-16 11:44 | 15 | 6 | 9 | 415 | 389 | 26 | 0 | 0 | 0 | 0 | 9 | 9 | 0 | 0 | 716 | 671 | 48 | 7 | 0 | 0 | 0 | 0 | 5 |
| glennq | 168 | 2,332 | 2024-11-05 10:09 | 2026-06-16 14:40 | 1 | 1 | 0 | 1,350 | 1,341 | 9 | 0 | 0 | 0 | 0 | 19 | 17 | 0 | 2 | 310 | 274 | 135 | 36 | 0 | 0 | 0 | 0 | 0 |
| johnboyd | 217 | 2,316 | 2024-11-06 10:41 | 2026-06-10 11:34 | 157 | 150 | 7 | 632 | 624 | 1 | 0 | 0 | 0 | 0 | 36 | 18 | 17 | 1 | 498 | 452 | 83 | 24 | 0 | 0 | 9 | 27 | 7 |
| dparkin | 383 | 2,089 | 2024-11-01 12:47 | 2026-06-16 13:39 | 119 | 119 | 0 | 762 | 759 | 3 | 0 | 0 | 0 | 0 | 8 | 0 | 8 | 0 | 163 | 140 | 14 | 4 | 0 | 0 | 3 | 21 | 0 |
| drauschuber | 211 | 2,012 | 2024-11-10 10:52 | 2026-06-16 12:22 | 99 | 26 | 73 | 734 | 727 | 7 | 0 | 0 | 0 | 0 | 8 | 4 | 4 | 0 | 259 | 257 | 17 | 36 | 0 | 1 | 4 | 3 | 3 |
| hmelzer | 127 | 1,976 | 2024-11-01 17:23 | 2026-06-09 18:15 | 45 | 40 | 5 | 289 | 240 | 49 | 0 | 0 | 0 | 0 | 118 | 12 | 105 | 1 | 348 | 328 | 23 | 132 | 0 | 0 | 8 | 25 | 0 |
| dvheady | 251 | 1,957 | 2024-11-01 09:45 | 2026-06-10 14:00 | 94 | 94 | 0 | 522 | 522 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 396 | 394 | 96 | 0 | 0 | 0 | 0 | 0 | 0 |
| ptjohnson | 272 | 1,939 | 2024-11-05 16:59 | 2026-01-15 15:53 | 0 | 0 | 0 | 299 | 295 | 3 | 0 | 0 | 0 | 0 | 27 | 24 | 3 | 0 | 530 | 439 | 300 | 0 | 0 | 0 | 0 | 0 | 0 |
| schaefer | 238 | 1,876 | 2024-11-01 09:51 | 2026-06-16 17:01 | 159 | 111 | 48 | 666 | 646 | 20 | 0 | 0 | 0 | 0 | 37 | 13 | 24 | 0 | 102 | 99 | 26 | 4 | 0 | 0 | 3 | 9 | 7 |
| cstock | 169 | 1,784 | 2024-11-05 10:40 | 2026-06-15 11:05 | 519 | 43 | 476 | 123 | 119 | 1 | 0 | 0 | 0 | 0 | 8 | 3 | 0 | 5 | 593 | 588 | 1 | 4 | 0 | 0 | 1 | 1 | 0 |
| mikej | 152 | 1,706 | 2024-11-04 14:50 | 2026-06-12 14:10 | 70 | 70 | 0 | 230 | 217 | 13 | 0 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 655 | 643 | 4 | 3 | 0 | 0 | 4 | 21 | 16 |
| mirandaa | 99 | 1,652 | 2024-11-04 10:50 | 2026-05-06 11:52 | 76 | 76 | 0 | 220 | 209 | 11 | 0 | 0 | 0 | 0 | 76 | 0 | 76 | 0 | 264 | 263 | 8 | 70 | 0 | 4 | 0 | 11 | 10 |
| tgray | 67 | 1,623 | 2024-11-07 15:16 | 2025-12-18 10:10 | 351 | 75 | 276 | 194 | 182 | 12 | 0 | 0 | 0 | 0 | 26 | 18 | 4 | 4 | 122 | 119 | 13 | 78 | 0 | 13 | 2 | 9 | 11 |
| chrisw | 185 | 1,544 | 2024-11-02 10:43 | 2026-06-16 13:25 | 24 | 22 | 2 | 298 | 297 | 1 | 0 | 0 | 0 | 0 | 59 | 16 | 43 | 0 | 19 | 6 | 28 | 58 | 0 | 0 | 0 | 1 | 7 |
| jeffb | 282 | 1,534 | 2024-11-01 13:14 | 2026-06-16 09:05 | 17 | 17 | 0 | 189 | 184 | 5 | 0 | 0 | 0 | 0 | 64 | 39 | 25 | 0 | 505 | 478 | 1 | 19 | 0 | 0 | 0 | 0 | 0 |
| riveraa | 17 | 1,440 | 2025-01-08 07:43 | 2026-01-12 12:31 | 118 | 37 | 81 | 188 | 188 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 27 | 27 | 1 | 0 | 0 | 0 | 0 | 2 | 0 |
| greenwayb | 94 | 1,364 | 2025-02-18 09:08 | 2026-05-19 08:11 | 65 | 20 | 45 | 286 | 255 | 31 | 0 | 0 | 0 | 0 | 71 | 9 | 57 | 5 | 134 | 133 | 6 | 124 | 0 | 6 | 1 | 10 | 3 |
| roniversen | 74 | 1,274 | 2024-11-04 18:28 | 2026-06-10 18:56 | 86 | 76 | 10 | 297 | 290 | 6 | 0 | 0 | 0 | 0 | 79 | 0 | 79 | 0 | 45 | 29 | 1 | 0 | 0 | 0 | 1 | 7 | 19 |
| newell | 70 | 1,091 | 2025-12-22 13:33 | 2026-06-16 15:18 | 63 | 63 | 0 | 502 | 502 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 40 | 39 | 20 | 6 | 0 | 0 | 1 | 14 | 7 |
| jerrysharp | 202 | 1,082 | 2024-11-08 17:35 | 2026-06-16 15:24 | 34 | 12 | 22 | 349 | 326 | 22 | 0 | 0 | 0 | 0 | 5 | 1 | 4 | 0 | 53 | 39 | 40 | 10 | 0 | 0 | 0 | 6 | 1 |
| lauraf | 120 | 1,052 | 2024-11-15 09:51 | 2026-03-27 16:13 | 25 | 25 | 0 | 308 | 280 | 2 | 0 | 0 | 0 | 0 | 23 | 0 | 23 | 0 | 67 | 67 | 3 | 88 | 0 | 0 | 1 | 4 | 2 |
| nickbrown | 113 | 925 | 2024-11-26 14:18 | 2026-06-15 12:09 | 50 | 15 | 35 | 273 | 224 | 25 | 0 | 0 | 0 | 0 | 10 | 0 | 10 | 0 | 271 | 269 | 5 | 3 | 0 | 0 | 0 | 0 | 2 |
| nades | 143 | 877 | 2024-11-01 11:37 | 2026-05-21 09:36 | 25 | 0 | 25 | 416 | 393 | 23 | 0 | 0 | 0 | 0 | 19 | 8 | 11 | 0 | 32 | 31 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| lindsey | 38 | 808 | 2025-01-05 01:58 | 2026-05-06 16:26 | 51 | 51 | 0 | 119 | 117 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 106 | 106 | 0 | 27 | 0 | 0 | 1 | 5 | 17 |

*(Truncated: showing top 40 of 91 rows. Full data in cache file.)*

### Q-01_step2_results.md

# Q-01-S2 Results — Craftmade (clli, org_id=149)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 34
- **Run date**: 2026-06-17


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Shayna Petty | 13 | $261,427 | $20,110 | 6 |
| Andrew  Rivera | 9 | $157,432 | $17,492 | 9 |
| Harold Ballow | 12 | $48,193 | $4,016 | 9 |
| Mike Jeffcoat | 14 | $43,207 | $3,086 | 9 |
| Barb Roemerman | 15 | $40,256 | $2,684 | 12 |
| Keith Eichenblatt | 26 | $32,501 | $1,250 | 8 |
| Mike Elford | 15 | $31,575 | $2,105 | 8 |
| Cathy/Chad Teiber | 4 | $26,776 | $6,694 | 4 |
| Ron Iversen | 10 | $23,984 | $2,398 | 9 |
| John Boyd | 4 | $21,143 | $5,286 | 2 |
| Jerome Collins | 6 | $19,209 | $3,202 | 5 |
| Dennis Morgan | 4 | $18,838 | $4,710 | 4 |
| Lindsey Olsen | 8 | $18,100 | $2,262 | 6 |
| Hudson Williams | 20 | $12,944 | $647 | 9 |
| Doeren Carsten | 11 | $12,908 | $1,173 | 10 |
| Jean-Patrick Robert | 5 | $12,154 | $2,431 | 4 |
| Chris Wilga | 5 | $11,870 | $2,374 | 5 |
| Tom Gray | 2 | $10,221 | $5,111 | 2 |
| Peter Saiolla | 4 | $9,156 | $2,289 | 3 |
| Alex Miranda | 6 | $8,779 | $1,463 | 4 |
| Newell King | 7 | $7,274 | $1,039 | 6 |
| Doeren Sales | 2 | $7,216 | $3,608 | 2 |
| Ron Reindl | 1 | $7,178 | $7,178 | 1 |
| Linda Huffman | 4 | $6,735 | $1,684 | 4 |
| Kelly Casagrande | 2 | $5,612 | $2,806 | 1 |
| Kevin Ailara | 1 | $5,066 | $5,066 | 1 |
| Nick Brown | 2 | $5,039 | $2,519 | 2 |
| Bryan  Greenway | 2 | $3,878 | $1,939 | 2 |
| Patty Lingwall | 2 | $3,592 | $1,796 | 1 |
| Laura Ford | 2 | $3,171 | $1,586 | 1 |
| Angie Schaefer | 3 | $1,804 | $601 | 2 |
| David Raushchuber | 4 | $1,720 | $430 | 3 |
| Joe Glatthaar | 2 | $1,265 | $633 | 2 |
| Bryan Coker | 1 | $1,111 | $1,111 | 1 |

### Q-04_results.md

# Q-04 Results — Craftmade (clli, org_id=149)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 91
- **Run date**: 2026-06-17


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cathychad | 435 | 9,314 | 7 | 4,352 | 944 | 35 | 60 | 0 | 77 | 46 | Selling Rep |
| broem | 403 | 8,121 | 28 | 2,189 | 236 | 3 | 236 | 0 | 5 | 795 | Selling Rep |
| keith | 309 | 4,901 | 65 | 1,619 | 767 | 43 | 31 | 0 | 197 | 7 | Selling Rep |
| doerenc | 247 | 3,683 | 14 | 580 | 486 | 13 | 122 | 0 | 23 | 0 | Selling Rep |
| spetty | 111 | 3,566 | 0 | 162 | 130 | 4 | 2 | 0 | 3 | 0 | Sales Support/Inside Sales |
| rreindl | 448 | 3,484 | 3 | 527 | 1,237 | 43 | 0 | 0 | 5 | 0 | Selling Rep |
| melford | 198 | 3,445 | 23 | 911 | 815 | 11 | 27 | 0 | 15 | 44 | Selling Rep |
| petercs | 297 | 3,354 | 6 | 808 | 1,142 | 5 | 6 | 0 | 145 | 4 | Selling Rep |
| kellyc | 217 | 3,261 | 8 | 844 | 420 | 6 | 9 | 0 | 128 | 42 | Selling Rep |
| broche | 299 | 3,122 | 1 | 1,075 | 222 | 24 | 87 | 0 | 4 | 79 | Content/Library Manager |
| christinew | 351 | 3,084 | 0 | 1,234 | 114 | 32 | 62 | 0 | 398 | 1 | Content/Library Manager |
| jglatthaar | 344 | 2,979 | 4 | 769 | 672 | 57 | 33 | 0 | 100 | 3 | Selling Rep |
| lbhuffman | 291 | 2,955 | 7 | 1,323 | 210 | 3 | 1 | 0 | 291 | 7 | Selling Rep |
| thel70 | 255 | 2,529 | 13 | 1,043 | 67 | 6 | 2 | 0 | 5 | 0 | Selling Rep |
| vlearned2 | 295 | 2,482 | 0 | 685 | 495 | 0 | 24 | 0 | 151 | 12 | Content/Library Manager |
| hudsonw | 187 | 2,468 | 20 | 911 | 482 | 4 | 0 | 0 | 83 | 0 | Selling Rep |
| mitchellk | 361 | 2,366 | 5 | 389 | 671 | 45 | 0 | 0 | 48 | 7 | Selling Rep |
| glennq | 168 | 2,332 | 0 | 1,341 | 274 | 36 | 0 | 0 | 135 | 36 | Content/Library Manager |
| johnboyd | 217 | 2,316 | 7 | 624 | 452 | 46 | 17 | 0 | 83 | 24 | Selling Rep |
| dparkin | 383 | 2,089 | 0 | 759 | 140 | 23 | 8 | 0 | 14 | 4 | Content/Library Manager |
| drauschuber | 211 | 2,012 | 3 | 727 | 257 | 2 | 4 | 0 | 17 | 37 | Selling Rep |
| hmelzer | 127 | 1,976 | 0 | 240 | 328 | 20 | 105 | 0 | 23 | 132 | Content/Library Manager |
| dvheady | 251 | 1,957 | 0 | 522 | 394 | 2 | 0 | 0 | 96 | 0 | Content/Library Manager |
| ptjohnson | 272 | 1,939 | 0 | 295 | 439 | 91 | 3 | 0 | 300 | 0 | Content/Library Manager |
| schaefer | 238 | 1,876 | 7 | 646 | 99 | 3 | 24 | 0 | 26 | 4 | Selling Rep |
| cstock | 169 | 1,784 | 0 | 119 | 588 | 5 | 0 | 0 | 1 | 4 | Content/Library Manager |
| mikej | 152 | 1,706 | 16 | 217 | 643 | 12 | 0 | 0 | 4 | 3 | Selling Rep |
| mirandaa | 99 | 1,652 | 10 | 209 | 263 | 1 | 76 | 0 | 8 | 74 | Selling Rep |
| tgray | 67 | 1,623 | 11 | 182 | 119 | 3 | 4 | 0 | 13 | 91 | Selling Rep |
| chrisw | 185 | 1,544 | 7 | 297 | 6 | 13 | 43 | 0 | 28 | 58 | Selling Rep |
| jeffb | 282 | 1,534 | 0 | 184 | 478 | 27 | 25 | 0 | 1 | 19 | Content/Library Manager |
| riveraa | 17 | 1,440 | 0 | 188 | 27 | 0 | 0 | 0 | 1 | 0 | Sales Support/Inside Sales |
| greenwayb | 94 | 1,364 | 3 | 255 | 133 | 1 | 57 | 0 | 6 | 130 | Selling Rep |
| roniversen | 74 | 1,274 | 19 | 290 | 29 | 16 | 79 | 0 | 1 | 0 | Selling Rep |
| newell | 70 | 1,091 | 7 | 502 | 39 | 1 | 6 | 0 | 20 | 6 | Selling Rep |
| jerrysharp | 202 | 1,082 | 1 | 326 | 39 | 14 | 4 | 0 | 40 | 10 | Sales Support/Inside Sales |
| lauraf | 120 | 1,052 | 2 | 280 | 67 | 0 | 23 | 0 | 3 | 88 | Catalog/Data Manager |
| nickbrown | 113 | 925 | 2 | 224 | 269 | 2 | 10 | 0 | 5 | 3 | Content/Library Manager |
| nades | 143 | 877 | 0 | 393 | 31 | 1 | 11 | 0 | 5 | 0 | Sales Support/Inside Sales |
| lindsey | 38 | 808 | 17 | 117 | 106 | 0 | 6 | 0 | 0 | 27 | Selling Rep |
| dmorg | 131 | 795 | 5 | 110 | 76 | 0 | 0 | 0 | 6 | 0 | Selling Rep |
| onealc | 100 | 786 | 2 | 387 | 51 | 5 | 0 | 0 | 73 | 0 | Sales Support/Inside Sales |
| bcoker | 73 | 776 | 1 | 125 | 36 | 0 | 9 | 1 | 91 | 0 | Sales Support/Inside Sales |
| cframburg | 120 | 738 | 0 | 248 | 84 | 2 | 7 | 0 | 2 | 2 | Sales Support/Inside Sales |
| patty | 140 | 708 | 2 | 198 | 74 | 19 | 15 | 1 | 1 | 0 | Sales Support/Inside Sales |
| jprobert | 19 | 690 | 26 | 138 | 2 | 0 | 2 | 0 | 3 | 4 | Selling Rep |
| jcoll | 30 | 668 | 11 | 5 | 277 | 1 | 0 | 0 | 2 | 2 | Selling Rep |
| rocher | 64 | 660 | 0 | 54 | 323 | 2 | 1 | 0 | 0 | 0 | Content/Library Manager |
| jeff_dalton | 110 | 655 | 0 | 304 | 9 | 27 | 0 | 0 | 7 | 0 | Content/Library Manager |
| mitchc | 73 | 632 | 0 | 214 | 133 | 4 | 5 | 0 | 3 | 1 | Sales Support/Inside Sales |
| bllinc | 67 | 483 | 3 | 64 | 8 | 0 | 0 | 0 | 1 | 0 | Selling Rep |
| dfullerton | 64 | 480 | 0 | 58 | 152 | 44 | 6 | 0 | 15 | 4 | Content/Library Manager |
| pmackey | 98 | 475 | 0 | 178 | 53 | 4 | 0 | 0 | 9 | 0 | Low-Activity User |
| ecalaiacovo | 19 | 454 | 0 | 37 | 2 | 0 | 32 | 0 | 0 | 37 | Catalog/Data Manager |
| pmarenghi | 49 | 414 | 5 | 92 | 51 | 1 | 0 | 0 | 2 | 0 | Selling Rep |
| loganboyd | 49 | 390 | 0 | 109 | 112 | 1 | 0 | 0 | 0 | 0 | Low-Activity User |
| egibson26 | 7 | 387 | 0 | 317 | 11 | 0 | 0 | 0 | 4 | 0 | Inactive |
| rickj | 56 | 262 | 0 | 106 | 9 | 0 | 0 | 0 | 5 | 0 | Low-Activity User |
| bobsm | 29 | 234 | 0 | 69 | 64 | 0 | 0 | 0 | 1 | 1 | Inactive |
| rogerh | 13 | 228 | 0 | 2 | 12 | 1 | 0 | 0 | 6 | 0 | Inactive |
| kimj | 27 | 216 | 0 | 45 | 3 | 0 | 0 | 0 | 2 | 17 | Inactive |
| aframburg | 26 | 200 | 0 | 37 | 36 | 0 | 2 | 0 | 0 | 3 | Inactive |
| kris | 26 | 190 | 0 | 24 | 33 | 0 | 2 | 0 | 16 | 1 | Inactive |
| melford2 | 17 | 150 | 0 | 55 | 3 | 0 | 5 | 0 | 0 | 10 | Inactive |
| stanf | 15 | 88 | 0 | 10 | 38 | 1 | 0 | 0 | 1 | 0 | Inactive |
| jonesr | 13 | 82 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 12 | Inactive |
| kailara | 4 | 72 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| edmymoreno | 5 | 69 | 0 | 13 | 0 | 2 | 2 | 0 | 3 | 1 | Inactive |
| mrothman | 5 | 65 | 0 | 10 | 1 | 1 | 3 | 0 | 0 | 6 | Inactive |
| davrob | 9 | 65 | 0 | 16 | 18 | 0 | 0 | 0 | 3 | 0 | Inactive |
| sbak | 9 | 60 | 0 | 5 | 25 | 0 | 0 | 0 | 1 | 0 | Inactive |
| jonv | 18 | 57 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | Inactive |
| sstraughan | 2 | 23 | 0 | 2 | 0 | 0 | 0 | 0 | 3 | 0 | Inactive |
| swt | 7 | 16 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jridings | 6 | 15 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 4 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| draus | 2 | 10 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | Inactive |
| dalebrown | 1 | 8 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | Inactive |
| engelhartb | 1 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kjael | 3 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| zwickzack | 2 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| mkraus | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pfrazier | 3 | 4 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| nickmansfield | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kylor_johnson | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Inactive |
| jsutter | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jjonesc | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| dmfine | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| gobrien | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| vlearned | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Craftmade (clli, org_id=149)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 1
- **Run date**: 2026-06-17


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 685 | 55 | 3 |

### Q-06_results.md

# Q-06 Results — Craftmade (clli, org_id=149)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 70
- **Run date**: 2026-06-17


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Keith Eichenblatt | 65 | 45 | -30.80 | 8 | 2 | -75 | $1,206 |
| Kelly Casagrande | 45 | 12 | -73.30 | 0 | 2 | — | $5,612 |
| Mike Jeffcoat | 57 | 24 | -57.90 | 11 | 1 | -90.90 | $166 |
| Hudson Williams | 101 | 42 | -58.40 | 16 | 1 | -93.80 | $783 |
| Chris Wilga | 44 | 38 | -13.60 | 4 | 0 | -100 | $0 |
| Patty Lingwall | 24 | 15 | -37.50 | 1 | 0 | -100 | $0 |
| Mike Elford | 75 | 0 | -100 | 8 | 0 | -100 | $0 |
| Alex Miranda | 41 | 4 | -90.20 | 6 | 0 | -100 | $0 |
| Harold Ballow | 81 | 51 | -37 | 12 | 0 | -100 | $0 |
| Ron Iversen | 23 | 7 | -69.60 | 10 | 0 | -100 | $0 |
| Linda Huffman | 66 | 70 | 6.10 | 4 | 0 | -100 | $0 |
| Lindsey Olsen | 19 | 9 | -52.60 | 7 | 0 | -100 | $0 |
| Ron Reindl | 148 | 99 | -33.10 | 1 | 0 | -100 | $0 |
| Jerome Collins | 9 | 4 | -55.60 | 5 | 0 | -100 | $0 |
| Angie Schaefer | 78 | 26 | -66.70 | 1 | 0 | -100 | $0 |
| Dennis Morgan | 29 | 13 | -55.20 | 4 | 0 | -100 | $0 |
| Shayna Petty | 60 | 35 | -41.70 | 4 | 0 | -100 | $0 |
| Nick Brown | 30 | 24 | -20 | 2 | 0 | -100 | $0 |
| Barb Roemerman | 114 | 121 | 6.10 | 13 | 0 | -100 | $0 |
| Jean-Patrick Robert | 14 | 0 | -100 | 5 | 0 | -100 | $0 |
| Newell King | 96 | 59 | -38.50 | 7 | 0 | -100 | $0 |
| Mike Elford | 17 | 12 | -29.40 | 8 | 0 | -100 | $0 |
| Laura Ford | 44 | 2 | -95.50 | 2 | 0 | -100 | $0 |
| Joe Glatthaar | 87 | 122 | 40.20 | 2 | 0 | -100 | $0 |
| David Raushchuber | 46 | 43 | -6.50 | 1 | 0 | -100 | $0 |
| John Boyd | 57 | 32 | -43.90 | 4 | 0 | -100 | $0 |
| Kevin Ailara | 5 | 0 | -100 | 1 | 0 | -100 | $0 |
| Peter Saiolla | 82 | 55 | -32.90 | 4 | 0 | -100 | $0 |
| Cathy/Chad Teiber | 161 | 89 | -44.70 | 2 | 0 | -100 | $0 |
| Doeren Carsten | 84 | 41 | -51.20 | 11 | 0 | -100 | $0 |
| Andrew  Rivera | 25 | 0 | -100 | 9 | 0 | -100 | $0 |
| Brian Roche | 81 | 56 | -30.90 | — | — | — | — |
| Nick Mansfield | 3 | 0 | -100 | — | — | — | — |
| Mitchell Kraus | 79 | 57 | -27.80 | — | — | — | — |
| Erin Gibson | 0 | 8 | — | — | — | — | — |
| Chuck Wiebe | 2 | 0 | -100 | — | — | — | — |
| Nick Ades | 28 | 8 | -71.40 | — | — | — | — |
| Jeff Dalton | 18 | 27 | 50 | — | — | — | — |
| Bryan Coker | 10 | 0 | -100 | — | — | — | — |
| Cary Stock | 33 | 44 | 33.30 | — | — | — | — |
| Jeff Brose | 92 | 82 | -10.90 | — | — | — | — |
| Jason Ridings | 4 | 0 | -100 | — | — | — | — |
| Dennis  Parkin | 63 | 76 | 20.60 | — | — | — | — |
| VERN LEARNED | 62 | 58 | -6.50 | — | — | — | — |
| Bryan  Greenway | 22 | 8 | -63.60 | — | — | — | — |
| Glenn Quintana | 45 | 24 | -46.70 | — | — | — | — |
| Jon Vanderberg | 5 | 2 | -60 | — | — | — | — |
| Stan Framburg | 6 | 2 | -66.70 | — | — | — | — |
| Mitch Colker | 30 | 10 | -66.70 | — | — | — | — |
| Roger Hoskins | 2 | 0 | -100 | — | — | — | — |
| Eileen Calaiacovo | 7 | 2 | -71.40 | — | — | — | — |
| Kylor  Johnson | 1 | 0 | -100 | — | — | — | — |
| Jerry Sharp | 45 | 51 | 13.30 | — | — | — | — |
| Collin Framburg | 34 | 26 | -23.50 | — | — | — | — |
| Paul Mackey | 10 | 17 | 70 | — | — | — | — |
| Shelley Straughan | 9 | 0 | -100 | — | — | — | — |
| Christine Wall | 98 | 99 | 1 | — | — | — | — |
| O'Neal Clamp | 2 | 0 | -100 | — | — | — | — |
| David Heady | 91 | 97 | 6.60 | — | — | — | — |
| Heather Melzer | 28 | 25 | -10.70 | — | — | — | — |
| Brent Sanders | 5 | 0 | -100 | — | — | — | — |
| Kris Quackenbush | 10 | 26 | 160 | — | — | — | — |
| Kjael Skaalerud | 0 | 2 | — | — | — | — | — |
| Annie Framburg | 15 | 3 | -80 | — | — | — | — |
| Renee Roche | 5 | 2 | -60 | — | — | — | — |
| Terry Johnson | 14 | 0 | -100 | — | — | — | — |
| Randy  Jones | 3 | 0 | -100 | — | — | — | — |
| Logan Boyd | 21 | 48 | 128.60 | — | — | — | — |
| Rick Jeffcoat | 11 | 16 | 45.50 | — | — | — | — |
| Doug Fullerton | 2 | 4 | 100 | — | — | — | — |

### Q-18_results.md

(not present — file does not exist or is empty)

### Q-43_results.md

(not present — file does not exist or is empty)

### Q-43_step2_results.md

# Q-43-S2 Results — Craftmade (clli, org_id=149)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-51_results.md

(not present — file does not exist or is empty)

### Q-62_results.md

# Q-62 Results — Craftmade (clli, org_id=149)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 0
- **Run date**: 2026-06-17


*(No data returned)*

### Q-63_results.md

# Q-63 Results — Craftmade (clli, org_id=149)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| egibson26 | 1 | 183 | 0 | 0 | 0 | 183 | 0 | 0 |
| hudsonw | 9 | 117 | 1 | 11.10 | 0.90 | 117 | 0 | 0 |
| newell | 5 | 83 | 0 | 0 | 0 | 82 | 1 | 0 |
| keith | 5 | 73 | 1 | 20 | 1.40 | 73 | 0 | 0 |
| doerenc | 4 | 65 | 0 | 0 | 0 | 58 | 7 | 0 |
| broche | 7 | 61 | 0 | 0 | 0 | 54 | 7 | 0 |
| thel70 | 5 | 55 | 0 | 0 | 0 | 55 | 0 | 0 |
| christinew | 2 | 38 | 0 | 0 | 0 | 34 | 4 | 0 |
| kellyc | 2 | 23 | 2 | 100 | 8.70 | 20 | 0 | 3 |
| johnboyd | 3 | 19 | 0 | 0 | 0 | 16 | 2 | 1 |
| petercs | 2 | 18 | 0 | 0 | 0 | 17 | 0 | 1 |
| kris | 1 | 14 | 0 | 0 | 0 | 14 | 0 | 0 |
| chrisw | 2 | 12 | 0 | 0 | 0 | 8 | 4 | 0 |
| jerrysharp | 1 | 11 | 0 | 0 | 0 | 11 | 0 | 0 |
| broem | 1 | 10 | 0 | 0 | 0 | 10 | 0 | 0 |
| mikej | 2 | 9 | 0 | 0 | 0 | 9 | 0 | 0 |
| loganboyd | 2 | 7 | 0 | 0 | 0 | 7 | 0 | 0 |
| hmelzer | 1 | 4 | 0 | 0 | 0 | 3 | 1 | 0 |
| schaefer | 1 | 4 | 0 | 0 | 0 | 4 | 0 | 0 |
| lbhuffman | 1 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Craftmade (clli, org_id=149)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| spetty | 1 | 111 | 1 | 1 | 0 |
| kellyc | 3 | 51.70 | 3 | 2 | 1 |
| egibson26 | 5 | 49 | 2.20 | 3 | 2 |
| keith | 6 | 23.80 | 2 | 5 | 0 |
| broem | 1 | 18 | 3 | 1 | 0 |
| chrisw | 2 | 17.50 | 4 | 2 | 0 |
| jglatthaar | 1 | 16 | 1 | 1 | 0 |
| hudsonw | 13 | 14.30 | 2.10 | 6 | 3 |
| mikej | 5 | 13.20 | 2 | 2 | 1 |
| jerrysharp | 1 | 13 | 1 | 1 | 0 |
| christinew | 7 | 13 | 2.30 | 3 | 3 |
| lindsey | 3 | 12.30 | 1 | 2 | 1 |
| petercs | 3 | 11.30 | 1.30 | 2 | 0 |
| newell | 17 | 11.30 | 1.30 | 4 | 8 |
| kris | 3 | 10.70 | 2 | 1 | 2 |
| cstock | 2 | 10.50 | 2 | 1 | 0 |
| thel70 | 7 | 9.60 | 1 | 3 | 2 |
| johnboyd | 8 | 9.30 | 1.80 | 3 | 2 |
| rreindl | 3 | 9.30 | 2 | 1 | 0 |
| loganboyd | 9 | 9 | 1.70 | 7 | 0 |

### Q-65_results.md

# Q-65 Results — Craftmade (clli, org_id=149)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-17 to 2026-06-17)
- **Row count**: 20
- **Run date**: 2026-06-17


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| egibson26 | 387 | 348 | 39 | 89.90 | 10.10 |
| hudsonw | 396 | 280 | 116 | 70.70 | 29.30 |
| thel70 | 279 | 180 | 99 | 64.50 | 35.50 |
| spetty | 270 | 158 | 112 | 58.50 | 41.50 |
| lbhuffman | 413 | 233 | 180 | 56.40 | 43.60 |
| glennq | 159 | 88 | 71 | 55.30 | 44.70 |
| nades | 46 | 25 | 21 | 54.30 | 45.70 |
| melford2 | 67 | 36 | 31 | 53.70 | 46.30 |
| cstock | 315 | 167 | 148 | 53 | 47 |
| newell | 401 | 209 | 192 | 52.10 | 47.90 |
| schaefer | 159 | 82 | 77 | 51.60 | 48.40 |
| doerenc | 238 | 122 | 116 | 51.30 | 48.70 |
| rickj | 40 | 17 | 23 | 42.50 | 57.50 |
| drauschuber | 229 | 96 | 133 | 41.90 | 58.10 |
| christinew | 487 | 195 | 292 | 40 | 60 |
| broche | 378 | 148 | 230 | 39.20 | 60.80 |
| cathychad | 414 | 162 | 252 | 39.10 | 60.90 |
| johnboyd | 216 | 82 | 134 | 38 | 62 |
| broem | 1,249 | 471 | 778 | 37.70 | 62.30 |
| mitchc | 50 | 18 | 32 | 36 | 64 |

### Q-70_results.md

(not present — file does not exist or is empty)

### showroom_scan_results.md

# Showroom Scan Results — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Total flagged**: 0
- **Aggregate GMV**: $0

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### user_group_mapping.md

# User Group Mapping — Craftmade (clli, org_id=149)
- **Run date**: 2026-06-17
- **Total Postgres users**: 1713
- **Matched to Mixpanel (Q-01 Step 1)**: 76 of 91 (84%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Customers | other | 1400 |
| Canadian Customers | other | 100 |
| Reps | field_rep | 98 |
| Hospitality 1.4xDN | other | 39 |
| Management | other | 22 |
| Admins | admin_internal | 17 |
| Power Design Group | other | 11 |
| Discounted Hospitality 1.2xDN | other | 10 |
| Customer Service Reps | admin_internal | 5 |
| Designer Group | other | 4 |
| Customers-IMAP | other | 2 |
| z-SuperCat | admin_internal | 2 |
| Passion Lighting | other | 1 |
| Showroom | showroom | 1 |
| eOL Public Site | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 55 | 89,256 | 90.2% |
| admin_internal | 9 | 7,184 | 7.3% |
| other | 12 | 2,462 | 2.5% |
