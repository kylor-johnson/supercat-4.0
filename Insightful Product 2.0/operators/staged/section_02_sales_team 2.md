# Section Guide: §2 — Sales Team Performance
> **v1.0** — validated 2026-04-17 (RENWIL run). Last updated: 2026-04-17.

## Section Identity
- **id**: `sales`
- **title**: Sales Team Performance
- **section number**: 2
- **include when**: `HAS_SALES_SECTION = true`
- **skip when**: `HAS_SALES_SECTION = false` — omit silently, no note in delivered report

## Query Inputs

Read these cache files:
- `cache/Q-01_step1_results.md` — BigQuery Mixpanel per-user behavioral data (also the source for Q-02 and Q-03 derivations — see below)
- `cache/Q-01_step2_results.md` — Postgres rep activity leaderboard
- `cache/Q-06_results.md` — Rep engagement trajectory
- `cache/Q-43_results.md` — Territory coverage & dormancy
- `cache/showroom_scan_results.md` — Operational account exclusion evidence
- `cache/gate_flags.md` — for `MIXPANEL_USER_DATA_PRESENT`, `QUALIFYING_REP_COUNT`, `SHOWROOM_EXCLUSIONS`, `MIXPANEL_ORDER_TRACKING_GAP`

Also read (for derivation rules only — not a cache file):
- `report-system/query_library.md` — Q-02 and Q-03 sections contain the classification rules and funnel gap thresholds you apply to Q-01 Step 1 data when building subsections 2, 3, and 4. These are not pre-computed by Stage 1.

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

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Rep Activity Ladder (Q-01)

Build from `Q-01_step2_results.md` — the leaderboard after operational exclusions are applied. This is the primary iPad rep performance table.

Show top 10 reps by iPad GMV. If more than 10 qualify, show top 10 visible and remaining in a collapsed `<details>` element.

### 2. Behavioral Scorecard Spotlight (Q-01 + Q-03 derivation)

**Gate**: `MIXPANEL_USER_DATA_PRESENT = true` (check `gate_flags.md`)

Apply the Q-03 funnel gap analysis rules from `report-system/query_library.md` to Q-01 Step 1 behavioral data. **Scope**: only classify the top 20 reps by iPad GMV from Q-01 Step 2 — do not process the full Q-01 Step 1 dataset. For each of those reps with `submit_order > 5`, compute the dimensional ratios and identify funnel gaps. Use the results to spotlight reps with notable behavioral patterns — high browse but low submission, strong configuration activity, or engagement trajectory divergence.

### 3. Selling Archetypes (Q-02 derivation)

**Gate**: `MIXPANEL_USER_DATA_PRESENT = true` (check `gate_flags.md`)

Apply the Q-02 archetype classification rules from `report-system/query_library.md` to Q-01 Step 1 behavioral data. **Scope**: only classify the top 20 reps by iPad GMV from Q-01 Step 2 — these are the reps with enough order volume to produce meaningful behavioral signal. Do not classify reps outside the top 20. Evaluate the behavioral ratio rules to assign an archetype. Render as a table with these exact columns:

| Column | Content |
|--------|---------|
| Archetype | Classification name |
| Rep(s) | Rep names that qualify for this archetype |
| Signature | The behavioral pattern that triggered the classification |
| Implication | Coaching or strategic takeaway for this archetype |

Include only archetypes where at least one rep qualifies. Follow with an insight callout explaining that archetypes are coaching tools, not performance labels — coaching should be adapted to selling style (e.g., a Volume Coverage Seller needs AOV support, not breadth training; a Precision Closer needs frequency incentives, not configuration coaching).

**Omission rule**: If fewer than 3 selling reps have Mixpanel data, omit this subsection silently — archetype classification requires enough reps to form meaningful clusters.

### 4. Coaching Opportunities (Q-03 derivation)

**Gate**: `MIXPANEL_USER_DATA_PRESENT = true` (check `gate_flags.md`)

Build as a **distinct subsection** with individual `.coaching-card` elements — NOT folded into "What this tells you" boxes. This is a separate subsection from the Behavioral Scorecard.

Using the Q-03 funnel gap results derived in subsection 2 above (top 20 reps only), select the 3–5 reps with the most actionable coaching gaps. For each, render a coaching card stating:
- **Gap location** in the funnel
- **Quantified AOV or GMV upside** if the gap is closed — frame as "potential" (e.g., "+$68K potential annual GMV"), not guaranteed. Tag with `[HYPOTHETICAL]`.
- **Recommended coaching action**

Use the `.coaching-card` / `.coaching-header` / `.coaching-name` / `.coaching-body` / `.coaching-action` / `.coaching-impact` class structure.

This subsection does NOT end with a `what-this-means` block — coaching cards are self-contained action items.

### 5. Rep Engagement Trajectory (Q-06)

Build from `Q-06_results.md`. Show how rep engagement has trended over time — identify reps trending up, trending down, or stable.

Show top 5 accelerating reps and bottom 5 declining reps only. Do not show all reps from the cache file. `[COLLAPSE]`

### 6. Territory Coverage (Q-43)

**Gate**: Territory data present in `Q-43_results.md`.

Build from `Q-43_results.md`. Surface territory coverage patterns, dormant territories, and geographic distribution of rep activity.

Show top 10 territories by coverage metrics. Include a `what-this-means` close. `[COLLAPSE]`

## Mixpanel Dependency Note

Subsections 2 (Behavioral Scorecard), 3 (Selling Archetypes), and 4 (Coaching Opportunities) require BigQuery Mixpanel per-user data from Q-01 Step 1 (`user_feature_usage_report`). If Q-01 Step 1 returned zero rows for this org, `MIXPANEL_USER_DATA_PRESENT` will be `false` in `gate_flags.md` — omit subsections 2–4 silently. Do not attempt to build archetypes or coaching content from Postgres order data alone. Subsection 1 (Rep Activity Ladder) and subsection 5 (Rep Engagement Trajectory) can still be built from Postgres data only.

**Mixpanel Order-Tracking Gap**: If `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md`, Mixpanel is not tracking iPad order submissions for this org (all users show `submit_order = 0` despite real Postgres orders). When this flag is true:
- Q-02 archetype rules that use `submit_order` as a threshold (e.g., "submit_order > 5") should fall back to Postgres `total_orders` from Q-01 Step 2 as the qualifying signal instead.
- Q-03 funnel gap analysis should skip the "Presentation → Orders" ratio (`submit_order / presentation`) — it will be zero for all reps regardless of actual behavior.
- Do NOT state that reps have "zero ordering activity" in the behavioral scorecard — that contradicts the Postgres order data. Instead, note that behavioral ordering metrics are unavailable for this org.

## Section-Specific Rules

- **Clamp**: Do not carry specific rep names, GMV figures, or archetypes from prior reports. Every generation is fresh from current query data.
- Do not surface showroom exclusion methodology, qualifying-threshold explanations (e.g., "44 reps met the qualifying threshold of ≥10 iPad orders"), or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference the exclusion count (e.g., "1 showroom excluded") but not the methodology or threshold logic.
