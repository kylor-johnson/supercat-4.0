# Section 2 Context Bundle — Universal Furniture (ufi)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=60988, portal_order_gmv=$137.9M |
| HAS_INVENTORY | True | inventory_count=2148 |
| HAS_SALES_DATA | True | sales_data_count=104838 |
| HAS_SALES_SECTION | True | qualifying_reps=17 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | ufi_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | PASS | erp_gmv=$137.9M > ecat_gmv=$13.4M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 17 | 17 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 103 rows |
| SHOWROOM_EXCLUSIONS | 0 | 0 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 2131, Mixpanel total submit_order (Q-01): 3593 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=82.5%, ambiguous_rate=15.3%, showroom_event_share=14.7% |
| USER_GROUP_JOIN_RATE | 83% | 85 of 103 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 15% | showroom+admin share of matched events: 14.7% |
| ADMIN_REPS_IN_LEADERBOARD | False | 0 admin/showroom users in leaderboard |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | False | distinct_rep_names=0 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=4382 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | True | commitment_reports_count=4255 |
| HAS_NEW_ITEMS | False | new_item_count=0 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Universal Furniture
- **Shortname**: ufi
- **Org ID**: 18
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16

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

## Section Guide — section_02_sales_team.md

# Section Guide: §2 — Sales Team Performance
> **v2.0** — updated 2026-06-17 (CCI hardening + Phase 1 behavioral queries Q-63/64/65). Last validated: 2026-04-17 (RENWIL).

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
- `cache/gate_flags.md` — for `MIXPANEL_USER_DATA_PRESENT`, `QUALIFYING_REP_COUNT`, `SHOWROOM_EXCLUSIONS`, `MIXPANEL_ORDER_TRACKING_GAP`, `PORTAL_REP_DATA_PRESENT`, `ADMIN_REPS_IN_LEADERBOARD`
- `cache/Q-51_results.md` — Rep eCat adoption vs. total business (**MANDATORY when gate met**: if `PORTAL_REP_DATA_PRESENT = true` in `gate_flags.md` AND this file contains data rows, subsection 1b MUST be rendered)
- `cache/Q-62_results.md` — Product launch velocity by rep `[COLLAPSE]` (conditional: render subsection 7 if `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND data rows exist)
- `cache/Q-63_results.md` — Presentation-to-order conversion (**MANDATORY when gate met**: if `MIXPANEL_USER_DATA_PRESENT = true` AND this file contains data rows, subsection 8 MUST be rendered)
- `cache/Q-64_results.md` — Rep engagement vs account revenue `[COLLAPSE]` (conditional: render subsection 9 if `MIXPANEL_USER_DATA_PRESENT = true` AND `HAS_PORTAL_ORDERS = true` AND data rows exist)
- `cache/Q-65_results.md` — Selling vs admin time ratio (**MANDATORY when gate met**: if `MIXPANEL_USER_DATA_PRESENT = true` AND this file contains data rows, subsection 10 MUST be rendered)
- `cache/Q-70_results.md` — Inactive reps with territory revenue (conditional: new query, render subsection 10 if `HAS_PORTAL_ORDERS = true` AND `PORTAL_REP_DATA_PRESENT = true` AND data rows exist)
- `cache/section_confidence.md` — for `SECTION_CONFIDENCE_2` tier

Also read (for derivation rules only — not a cache file):
- `authority/query_library.md` — Q-02 and Q-03 sections contain the classification rules and funnel gap thresholds you apply to Q-01 Step 1 data when building subsections 2, 3, and 4. These are not pre-computed by Stage 1.

## PRE-BUILD GATE CHECK — Complete Before Writing Any HTML

**Before generating any HTML**, read `gate_flags.md` and check each cache file below. Record which MANDATORY subsections will render. Skipping a MANDATORY subsection when its gate is met = defective fragment.

| Cache File | Gate Condition | If gate met + data rows exist → | Subsection |
|---|---|---|---|
| `Q-51_results.md` | `PORTAL_REP_DATA_PRESENT = true` | **MUST render** | 1b (Rep eCat Adoption vs Total Business) |
| `Q-63_results.md` | `MIXPANEL_USER_DATA_PRESENT = true` | **MUST render** | 8 (Presentation-to-Order Conversion) |
| `Q-64_results.md` | `MIXPANEL_USER_DATA_PRESENT = true` + `HAS_PORTAL_ORDERS = true` | Render inside `[COLLAPSE]` | 9 (Rep Engagement vs Revenue) |
| `Q-65_results.md` | `MIXPANEL_USER_DATA_PRESENT = true` | **MUST render** | 10 (Selling vs Admin Time) |

**Write down your list of MANDATORY subsections that will render before proceeding.** Use this list as a checklist while building.

## CRITICAL REQUIREMENTS — Read Before Building

These rules are non-negotiable. Failing ANY of them produces a defective fragment:

1. **DEDUP**: The leaderboard table must have exactly ONE row per rep. Scan for duplicates after building.
2. **ADMIN DISCLOSURE**: If `ADMIN_REPS_IN_LEADERBOARD = true` in `gate_flags.md`, the `§2-ADMIN-DISCLOSURE` text MUST appear in the confidence footer. Do not skip it.
3. **ERP ENRICHMENT SUBSECTIONS**: Every row in the Pre-Build Gate Check table above where the gate is met AND the cache file has data rows MUST produce a rendered subsection. If you skip one, the fragment is defective.
4. **CONFIDENCE FOOTER**: Every §2 fragment MUST contain a confidence footer. Read `SECTION_CONFIDENCE_2` from `section_confidence.md` — use the EXACT tier value, do NOT infer it from gate flags. Position: FULL=bottom, STRONG/PARTIAL/LIMITED=top (after metrics, before first subsection).
5. **VERIFICATION**: After building, run through the Conditional Subsection Checklist at the bottom of this guide. Cross-check against your Pre-Build Gate Check list. Fix any failures before saving.
8. **WHAT-THIS-MEANS QUALITY BAR**: Every `<div class="what-this-means">` block must read like a smart analyst talking to a VP — ground it in the specific numbers from this org's data and draw an actionable implication. Do not write data labels or restate the table header.
   - **FORBIDDEN**: Restating the top row of the table. The reader already read the table — your job is to tell them what it MEANS, not what it SAYS. If the what-this-means text could be derived by reading the first row of the table aloud, it is restating, not interpreting.
   - **BAD**: "This table shows your top 10 reps by GMV."
   - **BAD**: "Your top performer generates $765K in iPad orders across 131 customers." (This is literally reading the table back.)
   - **BAD**: "These results display the conversion rates for each rep."
   - **GOOD**: "The $485K gap between #1 and #10 suggests significant room to elevate mid-tier reps through coaching on customer targeting."
   - **GOOD**: "Your most active rep presented to 49 accounts but only 3.6% of presentations converted to orders — high effort, lower yield. Meanwhile, your most efficient closer converts at 26.8% with far fewer presentations, suggesting targeted demos outperform high-volume prospecting."
   - Every subsection except §2.3 Coaching Opportunities must end with exactly one `what-this-means` block that follows this quality bar.

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

## Subsection Order (do not reorder — render every subsection whose gate is met)

### 1. Rep Activity Ladder (Q-01)

Build from `Q-01_step2_results.md` — the leaderboard after operational exclusions are applied. This is the primary iPad rep performance table.

Show top 10 reps by iPad GMV. If more than 10 qualify, show top 10 visible and remaining in a collapsed `<details>` element.

**Dedup rule**: The leaderboard table must contain exactly ONE row per rep. If the same rep name appears in multiple source queries (e.g., Q-01 Step 1 and Step 2), merge their data into a single row — do not emit duplicate rows. After building the table, scan for duplicate `rep_name` values and collapse any repeats.

**ADMIN DISCLOSURE CHECK (do this immediately after building the leaderboard table):** Read `ADMIN_REPS_IN_LEADERBOARD` from `gate_flags.md`. If `true`, you MUST include the `§2-ADMIN-DISCLOSURE` text in the confidence footer at the end of this section. Do not forget or defer — flag it now, render it in the footer block below. The disclosure text is: "Note: This section includes ordering activity from users assigned to internal or administrative roles in your platform configuration. Their activity reflects real orders but may include test or operational transactions."

### 1b. Rep eCat Adoption vs. Total Business (Q-51)

**MANDATORY RENDER**: If `cache/Q-51_results.md` exists AND contains data rows AND `PORTAL_REP_DATA_PRESENT = true` in `gate_flags.md`, this subsection MUST appear in the fragment. Omit ONLY when the file is absent, contains zero rows, or the gate is false.

**Data source**: `cache/Q-51_results.md`

**Rendering**: Table with columns:

| Column | Content |
|--------|---------|
| Rep Name | Rep display name (never expose `rep_number`) |
| Total Business Orders | All-channel order count from synced business data |
| Total Business GMV | All-channel GMV |
| eCat Orders | eCat-originated order count |
| eCat GMV | eCat-originated GMV |
| eCat Capture % | `ecat_gmv / total_business_gmv × 100` |

Sort by total business GMV descending (`erp_gmv DESC`). Show top 10 visible. If more than 10 reps exist, remaining in a collapsed `<details>` element. Highlight reps with eCat Capture > 50% using `.row-highlight` class.

**Framing principle**: The capture rate spread across reps is the most actionable insight. Lead with the competitive dynamic: "Your top digital adopter captures X% of their total business through the platform. Your lowest captures Y%. That spread isn't a territory difference — it's a workflow difference, and closing it is the fastest path to platform-attributed revenue growth." This frames rep-level capture as an internal competition where laggards have a clear playbook (the top adopter's behavior).

**Claim rules**: "Rep X processes Y% of their total business through eCat." Reps with 0% capture are legitimate — they sell but haven't adopted the platform yet. Frame constructively as adoption opportunity, not failure. Never expose `rep_number` in client-facing output. The what-this-means should quantify the spread: "If your bottom-quartile reps matched your median capture rate of Z%, that would add an estimated $W in platform-attributed GMV annually."

### 2. Behavioral Scorecard Spotlight (Q-01 + Q-03 derivation)

**Gate**: `MIXPANEL_USER_DATA_PRESENT = true` (check `gate_flags.md`)

Apply the Q-03 funnel gap analysis rules from `authority/query_library.md` to Q-01 Step 1 behavioral data. **Scope**: only classify the top 20 reps by iPad GMV from Q-01 Step 2 — do not process the full Q-01 Step 1 dataset. For each of those reps with `submit_order > 5`, compute the dimensional ratios and identify funnel gaps. Use the results to spotlight reps with notable behavioral patterns — high browse but low submission, strong configuration activity, or engagement trajectory divergence.

### 3. Coaching Opportunities & Selling Archetypes (Q-02 + Q-03 derivation)

**Gate**: `MIXPANEL_USER_DATA_PRESENT = true` (check `gate_flags.md`)

This subsection merges archetype classification into coaching cards — the archetype label becomes a badge on each coaching card rather than a separate table. Archetypes provide the "why" framing; coaching provides the "what to do."

**Step 1 — Classify archetypes** (Q-02 derivation): Apply the Q-02 archetype classification rules from `authority/query_library.md` to Q-01 Step 1 behavioral data. **Scope**: only classify the top 20 reps by iPad GMV from Q-01 Step 2. If fewer than 3 selling reps have Mixpanel data, skip archetype badges silently — coaching cards still render without them.

**Step 2 — Team-level coaching rollup**: Before individual coaching cards, render a `.callout.opportunity` with the combined coaching upside:

```
"Combined coaching upside across N priority reps: $X in potential annual incremental GMV.
That's Y% of your current eCat revenue from behavioral coaching alone — with zero new
customer acquisition required."
```

Compute by summing the individual coaching upside values (from Q-03 funnel gap analysis). Tag the total with `[HYPOTHETICAL]` in cache. Use hedging language ("potential," "estimated") in client-facing HTML.

**Step 3 — Individual coaching cards**: Using the Q-03 funnel gap results derived in subsection 2 above (top 20 reps only), select the 3–5 reps with the most actionable coaching gaps. For each, render a `.coaching-card` stating:
- **Rep name** in `.coaching-name` — with a `.badge` showing their archetype classification (e.g., `<span class="badge info">Volume Relationship Seller</span>`). If the rep has no archetype (insufficient data), omit the badge.
- **Gap location** in the funnel
- **Quantified AOV or GMV upside** if the gap is closed — frame as "potential" (e.g., "+$68K potential annual GMV"), not guaranteed. Tag with `[HYPOTHETICAL]`.
- **Recommended coaching action** — tailor to the archetype. A Volume Coverage Seller needs AOV support, not breadth training; a Precision Closer needs frequency incentives, not configuration coaching.

Use the `.coaching-card` / `.coaching-header` / `.coaching-name` / `.coaching-body` / `.coaching-action` / `.coaching-impact` class structure.

This subsection does NOT end with a `what-this-means` block — the team rollup callout and coaching cards are self-contained action items.

### 4. Rep Engagement Trajectory (Q-06)

Build from `Q-06_results.md`. Show how rep engagement has trended over time — identify reps trending up, trending down, or stable.

Show top 5 accelerating reps and bottom 5 declining reps only. Do not show all reps from the cache file. `[COLLAPSE]`

### 5. Territory Coverage (Q-43)

**Gate**: Territory data present in `Q-43_results.md`.

Build from `Q-43_results.md`. Surface territory coverage patterns, dormant territories, and geographic distribution of rep activity.

Show top 10 territories by coverage metrics. Include a `what-this-means` close. `[COLLAPSE]`

### 6. New Item Launch Velocity by Rep (Q-62) `[COLLAPSE]`

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `HAS_NEW_ITEMS = true` AND `cache/Q-62_results.md` has data rows.

**Disposition**: Good data but secondary to archetypes — §2 overload risk. Wrap in an inner `<details>` per shared_rules §I.

**Data source**: `cache/Q-62_results.md`

**Data shape**: `rep_name` (display name, ALL-CAPS — title-case before rendering), `new_items_sold`, `total_new_items`, `adoption_pct`, `customers_buying_new`, `new_item_qty`, `new_item_revenue`, `orders_with_new_items`.

**Rendering**: Open with a `.callout.insight` titled "New Item Adoption by Rep" summarizing: "Your catalog has X new introductions. Your top seller has placed orders for Y of them (Z% adoption). The bottom quartile has sold fewer than W."

Then render a table:

| Column | Content |
|--------|---------|
| Rep | `rep_name` (title-cased) |
| New Items Sold | `new_items_sold` of `total_new_items` |
| Adoption % | `adoption_pct` with `.badge.ok` if ≥30%, `.badge.warn` if 15–29%, `.badge.danger` if <15% |
| Customers | `customers_buying_new` |
| Revenue | `new_item_revenue` formatted as currency |

Show top 10 visible; remaining in a collapsed `<details>` within the already-collapsed subsection.

After the table, include a `what-this-means` close grounded in this org's specific numbers (see Critical Requirement #8 quality bar).

**Claim rules**: Never name individual reps by real name in the callout insight — use "your top performer" / "bottom quartile" language. Table rows may use title-cased rep names. Never expose internal codes. Frame as coaching opportunity, not judgment.

### 7. Presentation-to-Order Conversion (Q-63) — **MANDATORY when gate met**

**Gate**: Render ONLY if `MIXPANEL_USER_DATA_PRESENT = true` AND `cache/Q-63_results.md` has data rows. **This is one of the highest-signal behavioral subsections — do not skip when the gate is met.**

**Data source**: `cache/Q-63_results.md`

**Data shape**: `rep` (username slug, NOT a display name — e.g., "staciebaker"), `accounts_engaged`, `total_presentations`, `total_orders`, `order_rate_pct` (orders/accounts × 100), `conversion_rate_pct` (orders/presentations × 100), `total_searches`, `total_catalogs`, `total_emails`.

**Username → Display Name**: The `rep` column contains platform usernames, not display names. Cross-reference against `Q-01_step2_results.md` rep names for display-name mapping. If no match is found, use anonymized labels ("Rep A", "Rep B"). Never render raw usernames (e.g., "staciebaker") in client-facing output.

**Showroom Exclusion**: Showroom/operational accounts may appear in Q-63 data (e.g., username patterns containing "showroom", "dallas", city names). Apply the same exclusion logic as the showroom pre-check: exclude from the table, do not count in summary statistics.

**Rendering**: Open with a `.callout.insight` titled "Presentation-to-Order Efficiency" with a data-grounded headline contrasting specific conversion patterns. Example tone: "Your most active rep presented to 49 accounts but only 3.6% of customer-facing presentations converted to orders. Meanwhile, your most efficient closer converts at 26.8% with targeted presentations — fewer demos, better outcomes."

Then render a table:

| Column | Content |
|--------|---------|
| Rep | Display name from cross-ref (or anonymized label) |
| Accounts Engaged | `accounts_engaged` |
| Presentations | `total_presentations` |
| Orders | `total_orders` |
| Conversion Rate | `conversion_rate_pct` with `.badge.ok` if ≥5%, `.badge.warn` if 2–4.9%, `.badge.danger` if <2% |

Show top 10 visible; remaining in a collapsed `<details>`. Sort by `total_presentations` descending (most active first — the conversion contrast is the story).

After the table, include a `what-this-means` close that is specific to this org's conversion range (see Critical Requirement #8). Do NOT use generic coaching boilerplate. Ground the insight in the actual spread between highest and lowest conversion reps and what that spread implies for coaching prioritization.

**Claim rules**: Never render raw usernames in client-facing output. Never expose `selected_bill_to_code` or event-name literals. Say "customer-facing presentations" not "product_search events." Say "platform engagement data" not "Mixpanel." Frame low conversion constructively as coaching opportunity.

### 8. Rep Engagement vs Account Revenue (Q-64) `[COLLAPSE]`

**Gate**: Render ONLY if `MIXPANEL_USER_DATA_PRESENT = true` AND `HAS_PORTAL_ORDERS = true` AND `cache/Q-64_results.md` has data rows.

**Disposition**: Useful engagement-depth view but secondary to Q-63 (conversion efficiency). Wrap in an inner `<details>` per shared_rules §I to avoid §2 overload.

**Data source**: `cache/Q-64_results.md`

**Data shape**: `rep` (username slug — same cross-ref rules as Q-63), `accounts_touched`, `avg_touches_per_account`, `avg_days_per_account`, `high_engagement_accounts` (8+ touches), `low_engagement_accounts` (<3 touches). Note: this query does not include revenue columns — do not fabricate revenue data. The "vs Account Revenue" framing comes from correlating engagement depth with order data from Q-01 Step 2.

**Username → Display Name**: Same rules as Q-63 — cross-reference `Q-01_step2_results.md` for display names. Never render raw usernames.

**Showroom Exclusion**: Showroom accounts may appear (e.g., usernames containing "showroom", city/location patterns). Exclude from the table and summary statistics.

**Rendering**: Open with a `.callout.insight` summarizing the engagement distribution: "X accounts receive 8+ platform touches (high engagement). Y accounts receive fewer than 3 (under-served). Your most engaged rep averages Z touches per account across N accounts."

Then render a table of reps by engagement metrics:

| Column | Content |
|--------|---------|
| Rep | Display name from cross-ref (or anonymized label) |
| Accounts Touched | `accounts_touched` |
| Avg Touches/Acct | `avg_touches_per_account` |
| High Engagement | `high_engagement_accounts` (8+ touches) |
| Low Engagement | `low_engagement_accounts` (<3 touches) |

Show top 10 visible; remaining in a collapsed `<details>`. Sort by `accounts_touched` descending.

After the table, include a `what-this-means` close grounded in this org's specific engagement spread (see Critical Requirement #8). Reference the actual range between the most- and least-engaged reps.

**Claim rules**: Always use "correlate" not "cause." Never render raw usernames. Never expose customer codes. Say "platform engagement data" not "Mixpanel." Frame under-engagement as opportunity, not failure.

### 9. Selling vs Admin Time (Q-65) — **MANDATORY when gate met AND spread gate passes**

**Gate**: Render ONLY if ALL of the following are true:
1. `MIXPANEL_USER_DATA_PRESENT = true`
2. `cache/Q-65_results.md` has data rows
3. **Spread gate**: The difference between the highest and lowest `selling_pct` values across qualifying reps exceeds 20 percentage points (e.g., if the range is 74%–89%, the 15pp spread fails this gate — skip silently). If the spread is ≤20pp, the data does not surface a meaningful coaching differentiation and the subsection adds length without insight.

**Data source**: `cache/Q-65_results.md`

**Data shape**: `rep` (username slug — same cross-ref rules as Q-63), `total_events`, `selling_events`, `admin_events`, `selling_pct`, `admin_pct`. Note: some orgs may have duplicate user identifiers (e.g., "alexsislopez" and "alexsislopez@gmail.com" for the same person). Merge rows with matching base usernames before rendering — sum events, recompute percentages.

**Username → Display Name**: Same rules as Q-63 — cross-reference `Q-01_step2_results.md` for display names. Never render raw usernames or email addresses.

**Showroom Exclusion**: Showroom accounts may appear (e.g., "ccdallasshowroom"). Exclude from the table and summary statistics — their selling/admin ratios reflect operational patterns, not rep behavior.

**Rendering**: Open with a `.callout.insight` titled "Time Allocation: Selling vs. Administration" with a data-grounded headline. Example tone: "Your top performers spend 92% of platform time on customer-facing activities vs. 8% administration. The bottom quartile averages X% — a gap that correlates with significantly lower order volume."

Then render a table:

| Column | Content |
|--------|---------|
| Rep | Display name from cross-ref (or anonymized label) |
| Total Activity | `total_events` |
| Selling | `selling_events` |
| Admin | `admin_events` |
| Selling % | `selling_pct` with `.badge.ok` if ≥70%, `.badge.warn` if 50–69%, `.badge.danger` if <50% |

Show top 10 visible; remaining in a collapsed `<details>`. Sort by `selling_pct` descending (most efficient sellers first).

After the table, include a `what-this-means` close grounded in this org's actual top-to-bottom spread (see Critical Requirement #8). Reference the specific percentage gap and frame it as a process-improvement opportunity. Do NOT use generic boilerplate.

**Claim rules**: Never render raw usernames or email addresses. Never use event_name literals in prose — say "customer-facing activities" and "administrative tasks." Say "platform engagement data" not "Mixpanel." Frame as process improvement opportunity, not individual failure. Always hedge correlations ("correlates with," not "causes").

### 10. Inactive Reps with Territory Revenue (Q-70) `[COLLAPSE]`

**Gate**: Render ONLY if `HAS_PORTAL_ORDERS = true` AND `PORTAL_REP_DATA_PRESENT = true` AND `cache/Q-70_results.md` exists AND contains data rows.

**Data source**: `cache/Q-70_results.md`

**Status**: New query — requires integration into `data_gather.py` before this subsection will render.

**Rendering**: Open with a `.callout.alert` titled "Platform Adoption Gap: Active Sellers, Offline Workflow" summarizing: "X reps with $Y in combined territory revenue haven't used the platform in 90+ days. These aren't inactive territories — they're active sellers managing their business entirely offline."

Then render a table:

| Column | Content |
|--------|---------|
| Rep | Rep display name (never expose user IDs) |
| Last Active | Days since last login, formatted as "X days ago" or "Last active [month]" |
| Territory Orders | All-channel order count (trailing 12 months) |
| Territory GMV | All-channel GMV formatted as currency |

Sort by territory GMV descending (highest-value inactive reps first). Show top 5 visible; remaining in collapsed `<details>`.

After the table, render a `<div class="what-this-means">`: "These reps are actively selling but not using the platform — their customer relationships are strong, but every order flows through phone, email, or manual processes. Re-engaging even N of these reps would add an estimated $X in platform-attributed revenue with zero new customer acquisition. The conversation isn't 'start using the app' — it's 'your peers are closing faster because they use the app.'"

**Claim rules**: Frame as activation opportunity, not performance criticism. Never say "these reps are failing" — say "these sellers manage their business offline." Never expose user IDs, login timestamps, or internal role codes. Use "haven't used the platform" not "haven't logged in" in client-facing prose.

## Mixpanel Dependency Note

Subsections 2 (Behavioral Scorecard), 3 (Selling Archetypes), and 4 (Coaching Opportunities) require BigQuery Mixpanel per-user data from Q-01 Step 1 (`user_feature_usage_report`). If Q-01 Step 1 returned zero rows for this org, `MIXPANEL_USER_DATA_PRESENT` will be `false` in `gate_flags.md` — omit subsections 2–4 silently. Do not attempt to build archetypes or coaching content from Postgres order data alone. Subsection 1 (Rep Activity Ladder) and subsection 5 (Rep Engagement Trajectory) can still be built from Postgres data only.

**Mixpanel Order-Tracking Gap**: If `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md`, Mixpanel is not tracking iPad order submissions for this org (all users show `submit_order = 0` despite real Postgres orders). When this flag is true:
- Q-02 archetype rules that use `submit_order` as a threshold (e.g., "submit_order > 5") should fall back to Postgres `total_orders` from Q-01 Step 2 as the qualifying signal instead.
- Q-03 funnel gap analysis should skip the "Presentation → Orders" ratio (`submit_order / presentation`) — it will be zero for all reps regardless of actual behavior.
- Do NOT state that reps have "zero ordering activity" in the behavioral scorecard — that contradicts the Postgres order data. Instead, note that behavioral ordering metrics are unavailable for this org.

## Section-Specific Rules

- **Clamp**: Do not carry specific rep names, GMV figures, or archetypes from prior reports. Every generation is fresh from current query data.
- Do not surface showroom exclusion methodology, qualifying-threshold explanations (e.g., "44 reps met the qualifying threshold of ≥10 iPad orders"), or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference the exclusion count (e.g., "1 showroom excluded") but not the methodology or threshold logic.
- **`portal_orders` terminology**: `portal_orders` represents ERP-synced all-channel total business. In client-facing prose, say "total business" or "all-channel sales." Never call it "portal ordering," "portal orders," or "buyer self-service."
- **No "ERP"**: Never use "ERP" in client-facing text. Use "total business," "all-channel sales," "your business system," or "your account base."
- **No "Mixpanel"**: Never use "Mixpanel" in client-facing text. Use "platform engagement data," "engagement events," or "behavioral analytics."
- **No internal identifiers**: Never surface health scores, segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused), VM codes, query IDs (Q-63, Q-65, etc.), table/column names, org IDs, or dataset paths in client-facing output.
- **Username handling in Q-63/64/65**: These queries return platform usernames (slugs), not display names. Always cross-reference `Q-01_step2_results.md` to resolve to display names. Never render raw usernames or email addresses.

## Data Confidence Footer (CRITICAL — includes admin disclosure)

**You MUST render this footer.** Follow the numbered steps below exactly. Do NOT skip or reorder them.

**STEP 1 — Read the tier (MANDATORY).** Open `cache/section_confidence.md` and read the EXACT value of `SECTION_CONFIDENCE_2`. It is one of: `FULL`, `STRONG`, `PARTIAL`, `LIMITED`. **Use THIS value. Do NOT infer or recompute the tier from gate flags — the data gathering script already computed it.**

**STEP 2 — Read the admin flag.** Read `ADMIN_REPS_IN_LEADERBOARD` from `cache/gate_flags.md`.

**STEP 3 — Select the template** matching the tier from STEP 1:

| STEP 1 value | Template | Label |
|---|---|---|
| `FULL` | `§2-FULL` (or `§2-FULL-NO-ERP` if `PORTAL_REP_DATA_PRESENT = false`) | `FULL PICTURE` |
| `STRONG` | `§2-STRONG` | `STRONG VIEW` |
| `PARTIAL` | `§2-PARTIAL` | `PARTIAL VIEW` |
| `LIMITED` | `§2-PARTIAL` (with `.limited` class) | `LIMITED VIEW` |

Resolve template variables: `{{MIXPANEL_USER_COUNT}}` from `gate_flags.md`.

**STEP 4 — Append admin disclosure if needed.** If `ADMIN_REPS_IN_LEADERBOARD = true` (from STEP 2), append the `§2-ADMIN-DISCLOSURE` text as a `<br>` line inside the same `.data-confidence-action` span. This applies at ALL tiers.

**STEP 5 — Position the footer:**
- If STEP 1 value is **FULL** → place the footer as the **last element** in the section fragment, after all subsection content.
- If STEP 1 value is **STRONG / PARTIAL / LIMITED** → place the footer **immediately after the key metrics row**, before the first subsection.

**STEP 6 — Build the HTML:**

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

If STEP 4 applied (admin disclosure), the action span looks like: `{{TEMPLATE_TEXT}}<br>Note: This section includes...`

If STEP 1 value is `LIMITED`, use `<div class="data-confidence limited">` instead.

## DOES NOT COVER (hard boundaries)

This section does NOT produce:
1. Customer-level activation, penetration, or dormancy analysis → belongs in §3 Customer & Buyer Intelligence
2. Per-customer eCat penetration of total business → belongs in §3 (Q-52 primary owner)
3. Commerce channel analysis, capture rate, or order trends → belongs in §5 Commerce Analytics
4. Product catalog health, inventory, or sales-line analysis → belongs in §4 Product & Inventory
5. Portal traffic, Clicky analytics, or geographic demand → belongs in §6 Demand Signal Intelligence
6. Platform feature utilization or data freshness → belongs in §8 Platform & Feature
7. Peer benchmarking or cohort comparisons → belongs in §7 Peer Benchmarking
8. Health score, churn risk, or expansion signals → internal only (GUARDRAILS.md §5)

Read: `GUARDRAILS.md` for the full query ownership table (§8) and rule set.

---

## Conditional Subsection Checklist (verify before saving fragment)

Before writing `fragments/section_02.html`, confirm every item below. Any failure = defective fragment.

### Subsection Registry

| # | Subsection | Query | Gate(s) | Status | Collapse? |
|---|-----------|-------|---------|--------|-----------|
| 1 | Rep Activity Ladder | Q-01 Step 2 | `HAS_SALES_SECTION = true` | **Always rendered** (section gate) | No |
| 1b | Rep eCat Adoption vs Total Business | Q-51 | `PORTAL_REP_DATA_PRESENT = true` + data rows | **MANDATORY** when gate met | No |
| 2 | Behavioral Scorecard Spotlight | Q-01 + Q-03 derivation | `MIXPANEL_USER_DATA_PRESENT = true` | Conditional | No |
| 3 | Coaching Opportunities & Selling Archetypes | Q-02 + Q-03 derivation | `MIXPANEL_USER_DATA_PRESENT = true` | Conditional (no `what-this-means`) | No |
| 4 | Rep Engagement Trajectory | Q-06 | Data present | Conditional | **Yes** `[COLLAPSE]` |
| 5 | Territory Coverage | Q-43 | Territory data present | Conditional | **Yes** `[COLLAPSE]` |
| 6 | New Item Launch Velocity | Q-62 | `HAS_PORTAL_ORDERS = true` + `HAS_NEW_ITEMS = true` + data rows | Conditional | **Yes** `[COLLAPSE]` |
| 7 | Presentation-to-Order Conversion | Q-63 | `MIXPANEL_USER_DATA_PRESENT = true` + data rows | **MANDATORY** when gate met | No |
| 8 | Rep Engagement vs Account Revenue | Q-64 | `MIXPANEL_USER_DATA_PRESENT = true` + `HAS_PORTAL_ORDERS = true` + data rows | Conditional | **Yes** `[COLLAPSE]` |
| 9 | Selling vs Admin Time | Q-65 | `MIXPANEL_USER_DATA_PRESENT = true` + data rows + spread >20pp | **MANDATORY** when gate met | No |
| 10 | Inactive Reps with Territory Revenue | Q-70 | `HAS_PORTAL_ORDERS = true` + `PORTAL_REP_DATA_PRESENT = true` + data rows | Conditional (new query) | **Yes** `[COLLAPSE]` |

### Pre-Save Verification

- [ ] **Q-51 (1b)**: `PORTAL_REP_DATA_PRESENT = true` + data rows → rendered? (or gate false / 0 rows → correctly skipped?)
- [ ] **Q-62 (6)**: `HAS_PORTAL_ORDERS = true` + `HAS_NEW_ITEMS = true` + data rows → rendered inside `[COLLAPSE]`? (or gate false / 0 rows → correctly skipped?)
- [ ] **Q-63 (7)**: `MIXPANEL_USER_DATA_PRESENT = true` + data rows → **MANDATORY** rendered? (omit ONLY when gate false or 0 rows)
- [ ] **Q-64 (8)**: `MIXPANEL_USER_DATA_PRESENT = true` + `HAS_PORTAL_ORDERS = true` + data rows → rendered inside `[COLLAPSE]`? (or gate false / 0 rows → correctly skipped?)
- [ ] **Q-65 (9)**: `MIXPANEL_USER_DATA_PRESENT = true` + data rows + selling_pct spread >20pp → **MANDATORY** rendered? (omit when gate false, 0 rows, or spread ≤20pp)
- [ ] **ADMIN_REPS_IN_LEADERBOARD** = true → disclosure appended as `<br>` line inside confidence footer at all tiers (FULL, STRONG, PARTIAL)
- [ ] **Leaderboard dedup**: subsection 1 table has no duplicate rep names (scan column 1)
- [ ] **Showroom exclusion**: Q-63/64/65 tables exclude showroom/operational accounts identified in `showroom_scan_results.md`
- [ ] **Username resolution**: Q-63/64/65 tables show display names (not raw usernames or emails) — cross-ref Q-01 Step 2
- [ ] **what-this-means count**: number of `what-this-means` divs = number of `subsection` divs minus §2.3 Coaching Opportunities & Selling Archetypes
- [ ] **what-this-means quality**: each block references specific org data points, not generic boilerplate (Critical Requirement #8)
- [ ] **Confidence footer**: present and matches `SECTION_CONFIDENCE_2` tier
- [ ] **section-contents**: middot list reflects ONLY rendered subsections (not skipped ones)
- [ ] **Forbidden phrases**: no "ERP," "Mixpanel," "portal ordering," health scores, segment labels, query IDs, raw usernames, or literal `[HYPOTHETICAL]`/`[ESTIMATED]` tags in HTML

## Shared Rules

# Shared Rules — All Section Agents
> **v1.1** — updated 2026-06-16. Scoped forbidden-phrase canonical claim, confidence footer scope.

> **Note:** This file is a runtime guide consumed by section-building agents. The
> canonical rule definitions live in [`GUARDRAILS.md`](../../../GUARDRAILS.md). If
> this file and `GUARDRAILS.md` conflict, `GUARDRAILS.md` wins.

## A. Semantic Guardrails

| Term | Correct Meaning | Never Use For |
|------|----------------|--------------|
| `orders` | eCat-originated orders only | ERP or total-business data |
| `order_source = 'ipad'` | Rep-submitted iPad orders | Online or self-service orders |
| `order_source = 'server'` | eCat Online / B2B Cart buyer self-service | Rep orders |
| `portal_orders` | ERP-synced all-channel total business | Buyer activity, "portal ordering," self-service |
| `Sales Portal` | Internal BI dashboard for client team | A buyer-facing ordering channel |
| `self-service` | B2B Cart / eCat Online only | Sales Portal, portal_orders |
| Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) | Internal classification only — never in external output | Every section including Peer Benchmarking — in §7, use plain-language cohort framing derived from `peer_group_id_effective` |
| Health score | Never in Phase 1 external report | Any external output |
| `benchmark_confidence` | Internal rendering signal only — governs section inclusion and phrasing | Never as a visible label in client output |
| `peer_group_level` | Internal gating signal only | Never in client output (not even paraphrased as "tier 1/2/3") |
| `peer_group_n` | Internal calibration signal — governs framing strength | Never as a raw count in client-facing output. Use to calibrate plain-language phrasing only. |

## B. Hard Rules

Invariant. No exception, no workaround, no soft reference:

1. Never surface health score, health band, or health classification in any external output
2. Never surface VM-27, VM-28, VM-29, VM-36, VM-48 content externally
3. If `has_clicky = false`, the Demand Signal Intelligence section does not exist. No placeholder. No mention of Clicky anywhere.
4. `portal_orders` is never buyer activity. Never "portal ordering adoption."
5. Segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) are internal classification terms and must never appear anywhere in the external report — including the Peer Benchmarking section. In §7, describe the peer group using plain-language framing derived from `peer_group_id_effective` (e.g., "Lighting manufacturers on the same platform bundle") — not the raw label or segment classification terms.
6. Executive Summary is always written last
7. Every metric must include a time qualifier (e.g., "trailing 12 months," "last 90 days")
8. Every projection must be hedged with appropriate language ("potential," "estimated," "projected," "roughly," "could," "up to") in client-facing HTML. The literal tags `[HYPOTHETICAL]` and `[ESTIMATED]` are **internal pipeline markers only** — they appear in `cache/` highlight files and priority action candidates so validators and the Stage 4 assembler can track projections, but they must **never appear as visible text in HTML fragments**. If the literal string `[HYPOTHETICAL]` or `[ESTIMATED]` appears in a fragment, it is a rendering defect.
9. Every extrapolation must be hedged with appropriate language in client-facing HTML (same rule as #8 — see above).
10. Do not improvise around missing data — mark as N/A or omit per blueprint rules
11. `benchmark_confidence`, `peer_group_level`, and `peer_group_n` are internal signals only. Never expose these as labels in client-facing HTML — not in prose, callouts, section headers, or footnotes. Use them to calibrate plain-language benchmark framing only.

## C. Forbidden Phrases

> **Runtime copy of the canonical list in GUARDRAILS.md §4.** The post-build check in `qa/eval/check_static.sh` mirrors this list. If you add or remove a forbidden phrase, update GUARDRAILS.md first, then this file and the shell script.

Never in client-facing HTML:

- "health score" / "health scores"
- "portal orders" / "portal ordering" as buyer activity or entity label
- "net-new customers"
- "ERP" in any client-facing text — use "total business," "all-channel sales," "your business system," "your account base"
- "Mixpanel" — use "platform engagement data" or "engagement events"
- "Clicky" — never in delivered HTML
- Segment labels: "Platform-Embedded", "Commerce-Active", "Catalog-Focused"
- Internal identifiers: VM codes, query IDs, table names, column names, org IDs, dataset paths
- "bounce_rate"
- `order_source = 'ipad'` and similar code literals in client-facing prose
- "benchmark_confidence", "peer_group_level", "peer_group_n" as labels
- Literal `[HYPOTHETICAL]` or `[ESTIMATED]` tags — these are internal pipeline markers and must never appear in client-facing HTML

## D. Universal Formatting Rules

- Every metric has a time qualifier (Hard Rule #7)
- Projections use hedging language in HTML; `[HYPOTHETICAL]` tags in cache/highlights only — never in fragments (Hard Rule #8)
- Extrapolations use hedging language in HTML; `[ESTIMATED]` tags in cache/highlights only — never in fragments (Hard Rule #9)
- Dollar formatting: `$X,XXX` or `$X.XM`
- Do not improvise around missing data (Hard Rule #10)
- Every subsection ends with a "What this tells you" close (1–3 sentences, actionable implication)
- One `what-this-means` per subsection. Do not add a second section-level `what-this-means` after the last subsection's close.
- Coaching Opportunities & Selling Archetypes (§2.3) is the one exception to the `what-this-means` rule: coaching cards are self-contained action items and do NOT end with a `what-this-means` block.
- Do not surface operational exclusion methodology, showroom scan details, qualifying threshold explanations, or internal pipeline context in client-facing prose. The `section-sub` one-liner may reference an exclusion count (e.g., "1 showroom excluded") but not the methodology.

## E. Fragment Contract

Every section agent produces an HTML fragment in this exact wrapper:

```html
<details class="section-collapse" id="{{SECTION_ID}}">
  <summary>
    <div>
      <h2 class="section-title"><span class="section-num">§{{N}}</span> {{SECTION_TITLE}}</h2>
      <div class="section-sub">{{KEY_STATS_ONE_LINE}}</div>
      <div class="section-contents">{{SUBSECTION_LIST_MIDDOT_SEPARATED}}</div>
    </div>
    <span class="expand-hint">&#9662; Click to expand</span>
  </summary>
  <section class="section" style="margin-bottom:0;border-top:none;border-radius:0 0 var(--r) var(--r);">
    {{SUBSECTION_CONTENT}}
  </section>
</details>
```

**Section IDs (locked):** `§2=sales`, `§3=customers`, `§4=product`, `§5=commerce`, `§6=portal`, `§7=peer`, `§8=platform`

**Fragment rules:**
- Starts with `<details`, ends with `</details>` — nothing before or after
- No `<html>`, `<head>`, `<body>`, or `<style>` tags
- No HTML comments (`<!-- -->`)
- `section-contents`: every rendered subsection name, separated by ` · ` (`&middot;`) — must reflect ONLY subsections that actually appear in the fragment (not skipped subsections)
- `section-sub`: data-dense one-liner, not a generic description
- Every subsection: `<div class="subsection">` with `<div class="subsection-title">` as first child
- Every subsection ends with `<div class="what-this-means">` (exception: §2.3 Coaching Opportunities & Selling Archetypes — coaching cards are self-contained and omit what-this-means per Section D above)
- **Structural self-check before saving**: count of `what-this-means` divs must equal count of `subsection` divs minus any coaching-card subsections. If you have more `what-this-means` than subsections, you have a duplicate — remove it. If fewer, a subsection is missing its close.

## F. CSS Class Quick-Reference

From `authority/html_report_template.html` (aligned with gold reference `clm_2026-04-14`). Use these class names exactly.

| Class | Renders |
|-------|---------|
| `.subsection` | Subsection container (24px top margin) |
| `.subsection-title` | Bold 15px subsection heading |
| `.what-this-means` | Amber left-bordered panel box for actionable close |
| `.metrics-grid` | Auto-fill responsive grid of metric cards |
| `.metric-card` | Panel-bg rounded card for a single metric |
| `.metric-val` | Bold 24px metric number |
| `.metric-label` | Mono 9px uppercase muted label |
| `.metric-note` | 11px muted annotation; variants `.ok` / `.warn` / `.danger` |
| `.callout` + `.callout-title` | Rounded box with left border accent; 600-weight 13px title |
| `.callout.insight` | Panel bg + amber left border |
| `.callout.alert` | Danger-bg + red left border (use instead of `.callout.warning`) |
| `.callout.opportunity` | Ok-bg + green left border (use instead of `.callout.action`) |
| `.badge` | Inline mono 10px uppercase pill |
| `.badge.ok` / `.badge.warn` / `.badge.danger` / `.badge.info` / `.badge.muted` | Status pills (dot notation — space-separated classes) |
| `.coaching-card` | White card with warn-colored 3px top border |
| `.coaching-header` / `.coaching-name` | Flex header row; bold 15px name |
| `.coaching-body` / `.coaching-action` / `.coaching-impact` | 13px body; medium-weight action; mono green impact pill |
| `.prose` | 13.5px secondary-color paragraph with 16px bottom margin |
| `<details>` (inner) | Panel-bg summary with arrow and click-to-expand pattern |
| `.row-highlight` | Table row with green (`--ok-bg`) emphasis |
| `.section-num` | Mono 11px muted section number prefix (e.g., §2) |
| `.peer-hero` | Panel-bg flex container for hero benchmark stat |
| `.peer-hero-pctile` | 13px mono pill badge; `.above` (green) / `.below` (red) / `.on-par` (muted) |
| `.peer-metric-row` | 3-column grid row for benchmark breakdown |
| `.peer-metric-title` | 12px metric name |
| `.peer-range-bar` / `.peer-range-marker` | 6px bar with positioned dot; `.above` / `.below` / `.on-par` |
| `.quartile-pill` / `.peer-quartile-pill` | 9px mono uppercase pill; `.q4` (green) / `.q3` (blue) / `.q2` (amber) / `.q1` (red) |
| `.priorities` / `.priority` | Grid container; 3-column card (badge / title+desc / impact) |
| `.priority-badge` | Mono 9px urgency pill; `.high` (red) / `.medium` (amber) / `.low` (muted) |
| `.priority-title` / `.priority-desc` / `.priority-impact` | Bold 14px title; 13px desc; mono 11px muted impact |
| `.highlights` | Counter-numbered list (amber-circled counters, light bottom borders) |
| `.top-performer-list` | Container for top-performer behavioral pattern rows (§7.4) |
| `.top-performer-row` | Flex row: icon + text, bottom-bordered |
| `.top-performer-icon` | 26px accent-glow rounded icon cell (use Unicode arrows/symbols) |
| `.top-performer-text` | 13px secondary prose with bold strong elements |
| `.data-confidence` | Info-bg panel at bottom of section body, 12px muted text, info left-border |
| `.data-confidence.limited` | Warn-bg variant with warn left-border (staleness/quality issues) |
| `.data-confidence-label` | Mono 9px uppercase badge prefix (tier label) |
| `.data-confidence-action` | 12px medium-weight text for "what would complete this" line |

## G. Highlight Candidate Format

Each section agent outputs `cache/section_NN_highlights.md` alongside its fragment.

```markdown
# §N Section Title — Highlight Candidates

1. **Bold headline** — one sentence of context with data. [→ §section-id]
2. **Bold headline** — one sentence of context with data. [→ §section-id]

## Priority Action Candidate
- **URGENCY**: Action statement with quantified impact [HYPOTHETICAL]. [→ §section-id]
```

**Note:** `[HYPOTHETICAL]` tags in highlight/priority candidates are correct — these are internal cache files consumed by the Stage 4 assembler, not client-facing HTML. The assembler strips or replaces tags with hedging language when building the Executive Summary.

**Rules:**
- 2–4 highlight candidates per section, ranked by signal strength
- Each: **bold headline**, one sentence of context, section link
- 0–1 priority action candidates per section with urgency level
- Stage 4 assembler selects top 5–6 highlights and 2–4 priority actions from all candidates
- Section agents do not write the Executive Summary — they only propose candidates

**Anti-repetition rule:** Executive summary highlights must NOT be repeated verbatim as section-level introductory callouts. A stat may appear in both the executive summary and a section, but the section must present the underlying data table — the `what-this-means` box must add **new interpretation** beyond what the executive summary already stated. If the `what-this-means` text could be copy-pasted into the executive summary without losing meaning, it is restating, not interpreting. The reader already read the table; the `what-this-means` job is to tell them what it MEANS, not what it SAYS.

## H. Display Limits

- Maximum 15 rows displayed per table. Default visible rows: 5. If showing top 10, show 5 visible + remaining 5 in a collapsed `<details>` element. Section-specific display limits in individual section guides take precedence over these defaults.
- Do not dump all cache file rows into tables. The section guide specifies how many to show per subsection.

## I. Progressive Disclosure — Subsection Collapse

- Subsections marked `[COLLAPSE]` in their section guide are wrapped in an inner `<details>` element within the parent section body (inside the outer `<details class="section-collapse">`).
- Collapsed subsections still appear in the `section-contents` middot list.
- When the user opens the parent section, `[COLLAPSE]` subsections remain closed until individually expanded.

## J. Data Confidence Framework

The Data Confidence Framework provides deterministic, per-section disclosure about what data sources are present, their freshness, and what additional data would make the picture more complete. It is formula-driven — no judgment calls, no improvisation.

### J.1 Tier Definitions

| Tier | Condition | Visual Treatment | Footer Rendered? |
|------|-----------|-----------------|-----------------|
| FULL | All primary + enrichment sources present and fresh (≤30 days) | `.data-confidence` footer | Yes — positive-tone data provenance |
| STRONG | Primary sources present; enrichment source stale (31-180d) or one source missing | `.data-confidence` footer | Yes — with source list |
| PARTIAL | Core eCat data only; ERP context unavailable | `.data-confidence` footer + "what would complete this" | Yes — with action |
| LIMITED | Core data stale (>180d) or known quality issues | `.data-confidence.limited` footer with staleness callout | Yes — with warn styling |

### J.2 Rendering Rules

1. **FULL** — render a `.data-confidence` footer with label `FULL PICTURE` and a positive-tone data sources summary listing what went into the analysis. No "To see X, do Y" action prompt — just a clean statement of what's there. **Position: bottom** of the section (after all subsections).
2. **STRONG / PARTIAL** — render a `.data-confidence` footer with a data sources summary AND an action prompt explaining what additional data would complete the picture. **Position: top** of the section (immediately after the key metrics row, before the first subsection). The reader sees upfront that data is incomplete before investing attention in the analysis.

```html
<div class="data-confidence">
  <span class="data-confidence-label">{{TIER_LABEL}}</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

All four tiers use this structure. `{{TIER_LABEL}}` is one of: `FULL PICTURE` / `STRONG VIEW` / `PARTIAL VIEW` / `LIMITED VIEW`.

3. **LIMITED** — same structure but with the `.limited` modifier:

```html
<div class="data-confidence limited">
  <span class="data-confidence-label">LIMITED VIEW</span>
  <span class="data-confidence-action">{{TEMPLATE_TEXT}}</span>
</div>
```

4. The confidence footer is part of the section fragment. The assembler pastes it verbatim — it does not modify, strip, or relocate it.
5. Never use "ERP" in any confidence footer text — this is client-facing. Use "your business system," "total business," or "all-channel" per Section C.
6. Confidence tier labels (`FULL PICTURE`, etc.) must not appear anywhere else in the report — they are reserved for this footer.

### J.3 Locked Template Strings

Section builders use these exact strings based on their section ID and tier. Do not paraphrase, shorten, or editorialize.

**§2 Sales Team:**
- `§2-FULL`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users), all-channel order data with rep attribution. Complete data for this section."
- `§2-FULL-NO-ERP`: "Data sources: eCat iPad orders, platform behavioral analytics ({{MIXPANEL_USER_COUNT}} active users). Complete eCat data for this section."
- `§2-PARTIAL`: "Data sources: eCat iPad orders. To see behavioral analytics and selling archetypes, ensure reps are using the eCat iPad app. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-STRONG`: "Data sources: eCat iPad orders, platform behavioral analytics. To see how eCat adoption compares to each rep's total business, sync order data with rep attribution via your business system."
- `§2-ADMIN-DISCLOSURE`: "Note: This section includes ordering activity from users assigned to internal or administrative roles in your platform configuration. Their activity reflects real orders but may include test or operational transactions."

The `§2-ADMIN-DISCLOSURE` template is an **additive append** — it is rendered as a second line inside the same `.data-confidence` div when `ADMIN_REPS_IN_LEADERBOARD = true`, regardless of tier. At FULL tier, append the disclosure as a `<br>` line inside the FULL PICTURE footer. At STRONG/PARTIAL, append as a `<br>` line inside the existing footer.

Use `§2-FULL` when `PORTAL_REP_DATA_PRESENT = true`. Use `§2-FULL-NO-ERP` when `PORTAL_REP_DATA_PRESENT = false` (eCat + Mixpanel data present, but no all-channel rep attribution).

**§3 Customer:**
- `§3-FULL`: "Data sources: eCat order history, account records ({{CUSTOMER_COUNT}} accounts), all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§3-PARTIAL`: "Data sources: eCat order history, account records. To see customer-level penetration of your total business and identify high-value unactivated accounts, sync order data via your business system."
- `§3-STRONG`: "Data sources: eCat order history, account records, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current total-business context."

**§4 Product:**
- `§4-FULL`: "Data sources: Product catalog ({{PRODUCT_COUNT}} items), inventory data, sales history. Complete data for this section."
- `§4-PARTIAL`: "Data sources: Product catalog. To see inventory status and sales performance by category, import inventory and sales history data."
- `§4-STRONG`: "Data sources: Product catalog, {{SOURCES_PRESENT}}. {{STALE_SOURCE}} was last updated {{STALE_DATE}} — refresh for current analysis."

**§5 Commerce:**
- `§5-FULL`: "Data sources: eCat orders, all-channel order data (last synced {{LAST_PORTAL_ORDER_DATE}}). Complete data for this section."
- `§5-PARTIAL`: "Data sources: eCat orders by channel and type. To see eCat's share of your total business and per-customer penetration, sync order data via your business system."
- `§5-STRONG`: "Data sources: eCat orders, all-channel order data. Order data was last synced {{LAST_PORTAL_ORDER_DATE}} — refresh for current context."

### J.4 Template Variable Resolution

- `{{LAST_PORTAL_ORDER_DATE}}` — from the ERP enrichment preflight (`most_recent_erp_order`), formatted as "Month DD, YYYY"
- `{{SOURCES_PRESENT}}` — comma-separated list of present sources (e.g., "inventory data, sales history")
- `{{STALE_SOURCE}}` — the specific source that is stale (e.g., "Inventory data", "Sales history")
- `{{STALE_DATE}}` — from Q-08 data_versions, formatted as "Month DD, YYYY"
- `{{MIXPANEL_USER_COUNT}}` — from `gate_flags.md` evidence for `MIXPANEL_USER_DATA_PRESENT` (the row count from Q-01 Step 1). If unavailable, omit the parenthetical from the FULL template and just say "platform behavioral analytics".
- `{{CUSTOMER_COUNT}}` — from `gate_flags.md` evidence for customer base count (Q-10 or equivalent). If unavailable, omit the parenthetical from the FULL template.
- `{{PRODUCT_COUNT}}` — from `gate_flags.md` evidence for product count (Q-08 catalog count). If unavailable, omit the parenthetical from the FULL template.

If a template variable cannot be resolved (source missing), use the PARTIAL template instead — never render a STRONG or FULL template with unresolved variables. For FULL templates, the parenthetical counts (`{{MIXPANEL_USER_COUNT}}`, `{{CUSTOMER_COUNT}}`, `{{PRODUCT_COUNT}}`) are the only exception — those may be gracefully omitted while keeping the FULL template.

### J.4b PARTIAL-Tier "What You'd See" Teaser

When a subsection is gated out due to missing data (e.g., `HAS_PORTAL_ORDERS = false` suppresses capture rate), section builders at PARTIAL or LIMITED tier MAY include a single `.callout.opportunity` teaser at the point where the gated subsection would appear. This makes the data-enrichment value proposition concrete without being salesy.

**Template:**

```html
<div class="callout opportunity">
  <div class="callout-title">What this section would show with connected data</div>
  <p>{{TEASER_TEXT}}</p>
</div>
```

**Per-section teaser text (use verbatim or adapt to context):**

- **§2 (rep capture):** "If total-business order data with rep attribution were connected, this section would show each rep's capture rate — what percentage of their territory's full revenue flows through the platform. Clients with this data typically discover a 5–30× spread across their team."
- **§3 (customer penetration):** "If total-business order data were connected, this section would show which of your highest-value accounts have never placed a platform order — and the combined revenue they represent through other channels."
- **§5 (capture rate):** "If total-business order data were connected, this section would show your platform capture rate — how much of your full revenue flows through the platform. Clients with this data typically discover 70–90% of their business is invisible to their digital ordering tools."

**Rules:**
- Maximum ONE teaser per section (not per gated subsection)
- Only at PARTIAL or LIMITED tier — never at STRONG or FULL
- Never in §6, §7, or §8 (no confidence framework)
- The teaser replaces the gated subsection's slot — do not leave a gap AND show a teaser

### J.5 Section Builder Contract

Each section builder that has a confidence tier (§2, §3, §4, §5):

1. Reads its tier from `cache/section_confidence.md` (e.g., `SECTION_CONFIDENCE_3`)
2. If tier is FULL — selects the matching `§X-FULL` template from J.3, resolves variables, and places the `.data-confidence` div with label `FULL PICTURE` as the **last element** in the section fragment (after all subsections)
3. If tier is STRONG or PARTIAL — selects the matching template from §J.3, resolves variables, and places the `.data-confidence` div **immediately after the key metrics row, before the first subsection**
4. If tier is LIMITED — uses the `.data-confidence.limited` variant with warn styling, positioned at the **top** (same as STRONG/PARTIAL)
5. Every section fragment for §2–§5 MUST contain exactly one `.data-confidence` footer. §6, §7, and §8 do not have confidence tiers and omit the footer

## Authority — Q-02 & Q-03 Derivation Rules

These classification and funnel-gap rules are applied to Q-01 Step 1 data when building subsections 2, 3, and 4. They are not pre-computed by Stage 1.


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

### Q-01_step1_results.md

# Q-01-S1 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 103
- **Run date**: 2026-06-16


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| terrilucas | 539 | 21,319 | 2024-11-01 09:52 | 2026-06-15 21:00 | 2,844 | 854 | 1,990 | 7,191 | 7,013 | 165 | 0 | 0 | 0 | 0 | 576 | 58 | 401 | 4 | 2,921 | 2,908 | 16 | 375 | 0 | 42 | 5 | 90 | 413 |
| rharding | 565 | 16,617 | 2024-11-01 10:19 | 2026-06-15 19:30 | 795 | 229 | 566 | 5,023 | 5,009 | 0 | 0 | 0 | 0 | 0 | 1,182 | 585 | 594 | 0 | 846 | 832 | 3 | 3,110 | 0 | 107 | 0 | 4 | 49 |
| neilphillips | 450 | 15,736 | 2024-11-01 07:41 | 2026-06-15 17:18 | 3,661 | 1,461 | 2,200 | 7,764 | 7,731 | 33 | 0 | 0 | 0 | 0 | 82 | 55 | 27 | 0 | 645 | 644 | 5 | 1 | 0 | 0 | 0 | 0 | 1,081 |
| masonoconnor | 389 | 14,971 | 2024-11-01 12:13 | 2026-06-08 13:11 | 1,410 | 565 | 845 | 9,035 | 9,021 | 8 | 0 | 0 | 0 | 0 | 250 | 0 | 243 | 7 | 1,127 | 1,126 | 9 | 675 | 0 | 49 | 0 | 3 | 4 |
| jacksonkeziah | 436 | 13,825 | 2024-11-01 13:18 | 2026-06-15 11:44 | 1,732 | 606 | 1,126 | 5,773 | 5,429 | 225 | 0 | 0 | 0 | 0 | 793 | 0 | 778 | 1 | 1,707 | 1,660 | 9 | 142 | 0 | 15 | 0 | 14 | 14 |
| johnnord | 485 | 13,355 | 2024-11-01 10:26 | 2026-06-15 15:45 | 1,773 | 578 | 1,195 | 6,563 | 5,819 | 0 | 0 | 0 | 0 | 0 | 273 | 2 | 271 | 0 | 1,225 | 1,099 | 12 | 121 | 0 | 0 | 2 | 19 | 313 |
| jacobennis | 395 | 11,621 | 2024-11-01 10:21 | 2026-06-15 19:47 | 1,685 | 556 | 1,129 | 4,683 | 4,229 | 154 | 0 | 0 | 0 | 0 | 469 | 58 | 411 | 0 | 1,705 | 1,704 | 11 | 29 | 0 | 0 | 1 | 106 | 1 |
| eileenfilloy | 183 | 10,320 | 2024-11-04 15:49 | 2026-06-09 16:53 | 18 | 15 | 3 | 3,061 | 3,041 | 16 | 0 | 0 | 0 | 0 | 286 | 1 | 193 | 2 | 1,026 | 1,025 | 14 | 537 | 0 | 114 | 5 | 4 | 0 |
| grantford | 443 | 9,841 | 2024-11-01 09:36 | 2026-06-15 17:10 | 2,874 | 845 | 2,029 | 3,360 | 3,358 | 1 | 0 | 0 | 0 | 0 | 93 | 1 | 90 | 2 | 889 | 885 | 3 | 227 | 0 | 0 | 2 | 4 | 5 |
| hdesk | 82 | 9,492 | 2024-12-09 15:56 | 2026-04-29 13:55 | 124 | 24 | 100 | 1,854 | 1,741 | 25 | 0 | 0 | 0 | 0 | 13 | 0 | 4 | 0 | 2,668 | 2,668 | 16 | 28 | 0 | 0 | 0 | 5 | 0 |
| kaitlinb | 383 | 9,327 | 2024-11-01 13:47 | 2026-06-11 11:16 | 615 | 470 | 145 | 3,506 | 3,497 | 3 | 0 | 0 | 0 | 0 | 240 | 0 | 240 | 0 | 1,153 | 1,151 | 22 | 20 | 0 | 3 | 2 | 16 | 2 |
| frankladonna | 482 | 9,171 | 2024-11-01 10:12 | 2026-06-15 21:00 | 646 | 205 | 441 | 4,414 | 4,376 | 24 | 0 | 0 | 0 | 0 | 259 | 3 | 210 | 0 | 521 | 514 | 27 | 2 | 0 | 0 | 1 | 11 | 21 |
| dhadad | 340 | 8,162 | 2024-11-01 13:36 | 2026-06-15 12:52 | 1,301 | 214 | 1,087 | 2,534 | 2,439 | 14 | 0 | 0 | 0 | 0 | 138 | 1 | 137 | 0 | 1,851 | 1,840 | 186 | 63 | 0 | 0 | 0 | 9 | 78 |
| sally-simerson | 385 | 7,780 | 2024-11-01 09:06 | 2026-06-15 17:45 | 1,273 | 470 | 803 | 3,170 | 3,161 | 7 | 0 | 0 | 0 | 0 | 72 | 8 | 63 | 1 | 1,071 | 1,045 | 49 | 16 | 0 | 0 | 0 | 143 | 19 |
| danielmeyer | 466 | 7,350 | 2024-11-01 12:43 | 2026-06-15 21:23 | 424 | 66 | 358 | 3,093 | 3,077 | 6 | 0 | 0 | 0 | 0 | 188 | 53 | 134 | 0 | 1,138 | 1,113 | 28 | 1 | 0 | 0 | 0 | 0 | 0 |
| mburcin | 402 | 7,127 | 2024-11-03 15:54 | 2026-06-15 18:42 | 261 | 114 | 147 | 3,953 | 3,879 | 74 | 0 | 0 | 0 | 0 | 183 | 0 | 183 | 0 | 496 | 496 | 5 | 0 | 0 | 0 | 0 | 6 | 0 |
| markdimitshteyn | 434 | 7,125 | 2024-11-01 07:50 | 2026-06-15 19:15 | 1,235 | 316 | 919 | 2,134 | 2,131 | 3 | 0 | 0 | 0 | 0 | 259 | 3 | 256 | 0 | 767 | 764 | 15 | 0 | 0 | 0 | 1 | 5 | 218 |
| jgrothman | 481 | 6,996 | 2024-11-01 12:07 | 2026-06-15 15:26 | 501 | 438 | 63 | 1,308 | 1,300 | 8 | 0 | 0 | 0 | 0 | 218 | 52 | 166 | 0 | 501 | 494 | 9 | 162 | 0 | 0 | 0 | 30 | 207 |
| ajfilloy | 306 | 6,933 | 2024-11-04 08:22 | 2026-06-09 16:19 | 5 | 2 | 3 | 4,164 | 4,163 | 1 | 0 | 0 | 0 | 0 | 148 | 57 | 88 | 0 | 669 | 666 | 18 | 13 | 0 | 0 | 0 | 0 | 0 |
| jamieschreiter | 436 | 6,550 | 2024-11-01 14:03 | 2026-06-15 15:55 | 386 | 151 | 235 | 2,017 | 2,015 | 0 | 0 | 0 | 0 | 0 | 678 | 645 | 32 | 1 | 938 | 936 | 4 | 17 | 0 | 1 | 0 | 35 | 4 |
| jhelton | 479 | 6,218 | 2024-11-01 12:39 | 2026-06-15 16:42 | 442 | 395 | 47 | 705 | 687 | 8 | 0 | 0 | 0 | 0 | 187 | 184 | 3 | 0 | 2,053 | 2,041 | 49 | 0 | 0 | 0 | 0 | 5 | 63 |
| chrise | 373 | 6,103 | 2024-11-01 09:59 | 2026-06-15 14:29 | 149 | 81 | 68 | 2,396 | 2,377 | 19 | 0 | 0 | 0 | 0 | 165 | 0 | 162 | 3 | 947 | 946 | 46 | 112 | 0 | 4 | 0 | 11 | 0 |
| glesser | 475 | 6,072 | 2024-11-01 08:14 | 2026-06-15 19:58 | 351 | 333 | 18 | 173 | 165 | 4 | 0 | 0 | 0 | 0 | 576 | 531 | 45 | 0 | 2,133 | 1,975 | 13 | 2 | 0 | 0 | 0 | 3 | 160 |
| paulcomer | 367 | 5,890 | 2024-11-03 22:09 | 2026-06-15 13:05 | 212 | 212 | 0 | 2,709 | 2,685 | 24 | 0 | 0 | 0 | 0 | 131 | 0 | 131 | 0 | 696 | 679 | 13 | 0 | 0 | 0 | 0 | 0 | 74 |
| jasonk | 311 | 5,532 | 2024-11-01 11:52 | 2026-06-15 21:29 | 552 | 193 | 359 | 2,864 | 2,796 | 14 | 0 | 0 | 0 | 0 | 92 | 6 | 86 | 0 | 387 | 387 | 13 | 74 | 0 | 5 | 1 | 10 | 0 |
| bbowman | 417 | 5,456 | 2024-11-01 08:41 | 2026-06-15 14:39 | 403 | 387 | 16 | 1,176 | 1,166 | 5 | 0 | 0 | 0 | 0 | 220 | 159 | 61 | 0 | 584 | 525 | 12 | 757 | 0 | 3 | 0 | 0 | 347 |
| jderaad | 294 | 5,133 | 2024-11-01 11:05 | 2026-06-15 15:35 | 888 | 327 | 561 | 1,800 | 1,781 | 9 | 0 | 0 | 0 | 0 | 66 | 2 | 64 | 0 | 606 | 588 | 3 | 1 | 0 | 0 | 3 | 43 | 92 |
| kirschint | 440 | 4,770 | 2024-11-01 14:33 | 2026-06-13 12:26 | 120 | 89 | 31 | 830 | 706 | 10 | 0 | 0 | 0 | 0 | 184 | 172 | 11 | 1 | 1,131 | 1,119 | 20 | 1 | 0 | 0 | 0 | 8 | 67 |
| jacki | 323 | 4,537 | 2024-11-01 14:30 | 2026-06-15 16:23 | 643 | 217 | 426 | 2,197 | 2,196 | 0 | 0 | 0 | 0 | 0 | 59 | 1 | 58 | 0 | 312 | 304 | 3 | 0 | 0 | 0 | 9 | 26 | 124 |
| ggeraci | 425 | 4,451 | 2024-11-01 10:33 | 2026-06-15 18:30 | 615 | 60 | 555 | 1,551 | 1,537 | 6 | 0 | 0 | 0 | 0 | 146 | 77 | 69 | 0 | 305 | 301 | 34 | 94 | 0 | 10 | 5 | 7 | 20 |
| arodriguez | 150 | 4,399 | 2024-11-06 08:05 | 2026-06-15 17:06 | 48 | 42 | 6 | 1,429 | 1,328 | 3 | 0 | 0 | 0 | 0 | 216 | 35 | 181 | 0 | 394 | 392 | 12 | 115 | 0 | 20 | 0 | 3 | 0 |
| phauerbach | 360 | 4,182 | 2024-11-04 09:07 | 2026-06-15 16:08 | 97 | 25 | 72 | 1,049 | 1,042 | 5 | 0 | 0 | 0 | 0 | 299 | 133 | 163 | 3 | 812 | 772 | 3 | 92 | 0 | 0 | 3 | 6 | 4 |
| jwagers | 215 | 4,009 | 2024-11-04 09:03 | 2026-06-15 16:44 | 0 | 0 | 0 | 2,944 | 2,940 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 337 | 336 | 7 | 23 | 0 | 0 | 0 | 0 | 0 |
| jeffc | 116 | 3,826 | 2024-11-01 07:04 | 2025-03-21 13:57 | 288 | 120 | 168 | 2,279 | 872 | 15 | 0 | 0 | 0 | 0 | 131 | 40 | 91 | 0 | 166 | 165 | 1 | 145 | 0 | 16 | 0 | 3 | 47 |
| perickson | 230 | 3,806 | 2025-04-07 08:00 | 2026-06-11 13:54 | 88 | 49 | 39 | 1,194 | 1,176 | 18 | 0 | 0 | 0 | 0 | 65 | 1 | 64 | 0 | 420 | 419 | 14 | 285 | 0 | 3 | 3 | 24 | 1 |
| jasonvanderhorst | 177 | 3,460 | 2024-11-01 11:09 | 2026-04-22 22:56 | 543 | 275 | 268 | 858 | 839 | 16 | 0 | 0 | 0 | 0 | 149 | 0 | 148 | 0 | 247 | 243 | 3 | 248 | 0 | 4 | 3 | 87 | 108 |
| amandae | 324 | 3,316 | 2024-11-01 14:49 | 2026-06-15 13:53 | 3 | 2 | 1 | 1,437 | 1,434 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 501 | 497 | 0 | 2 | 0 | 0 | 0 | 5 | 0 |
| fschacter | 317 | 2,969 | 2024-11-01 16:41 | 2026-06-15 17:39 | 97 | 72 | 25 | 1,080 | 1,077 | 1 | 0 | 0 | 0 | 0 | 196 | 185 | 9 | 2 | 340 | 332 | 5 | 10 | 0 | 0 | 0 | 0 | 43 |
| davep | 459 | 2,560 | 2024-11-01 10:39 | 2026-06-15 07:05 | 290 | 76 | 214 | 97 | 86 | 11 | 0 | 0 | 0 | 0 | 309 | 309 | 0 | 0 | 216 | 210 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| bradm | 149 | 2,500 | 2025-10-08 14:54 | 2026-06-15 17:05 | 38 | 13 | 25 | 1,264 | 1,108 | 32 | 0 | 0 | 0 | 0 | 101 | 5 | 55 | 3 | 218 | 216 | 8 | 57 | 0 | 0 | 0 | 3 | 0 |
| khelton | 225 | 2,283 | 2024-11-01 10:44 | 2025-10-22 18:33 | 83 | 26 | 57 | 574 | 563 | 4 | 0 | 0 | 0 | 0 | 66 | 66 | 0 | 0 | 667 | 659 | 3 | 0 | 0 | 0 | 0 | 8 | 3 |
| lmoreno | 205 | 2,250 | 2024-11-04 14:43 | 2026-06-11 14:28 | 3 | 0 | 3 | 1,111 | 1,103 | 0 | 0 | 0 | 0 | 0 | 41 | 0 | 41 | 0 | 62 | 55 | 4 | 24 | 0 | 2 | 0 | 0 | 0 |
| shannonl | 316 | 2,217 | 2024-11-01 09:56 | 2026-06-14 04:51 | 0 | 0 | 0 | 1,115 | 1,114 | 0 | 0 | 0 | 0 | 0 | 29 | 7 | 22 | 0 | 10 | 10 | 4 | 22 | 0 | 0 | 0 | 0 | 0 |
| soconnor | 266 | 2,061 | 2024-11-04 16:56 | 2026-06-15 16:25 | 2 | 2 | 0 | 935 | 920 | 4 | 0 | 0 | 0 | 0 | 55 | 5 | 50 | 0 | 101 | 99 | 7 | 3 | 0 | 0 | 0 | 0 | 0 |
| jacobkohns | 141 | 2,007 | 2025-07-09 14:37 | 2026-06-15 11:01 | 1 | 1 | 0 | 975 | 920 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 472 | 471 | 11 | 0 | 0 | 0 | 0 | 0 | 0 |
| christinas | 123 | 1,967 | 2024-11-26 15:51 | 2026-03-23 09:13 | 14 | 2 | 12 | 459 | 431 | 8 | 0 | 0 | 0 | 0 | 92 | 11 | 80 | 1 | 380 | 380 | 4 | 82 | 0 | 6 | 0 | 0 | 0 |
| meberlein | 413 | 1,893 | 2024-11-01 12:09 | 2026-06-15 04:42 | 0 | 0 | 0 | 809 | 35 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kimtraver | 320 | 1,869 | 2024-11-01 07:14 | 2026-06-11 07:53 | 6 | 2 | 4 | 149 | 147 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 550 | 548 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| aerickson | 104 | 1,834 | 2025-04-07 07:30 | 2026-06-03 10:55 | 71 | 49 | 22 | 300 | 279 | 15 | 0 | 0 | 0 | 0 | 14 | 0 | 13 | 1 | 285 | 284 | 45 | 35 | 0 | 0 | 3 | 11 | 4 |
| ammax | 165 | 1,834 | 2024-11-06 21:27 | 2026-06-12 09:57 | 25 | 9 | 16 | 808 | 631 | 0 | 0 | 0 | 0 | 0 | 84 | 1 | 83 | 0 | 188 | 188 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| bretwarren | 131 | 1,696 | 2024-11-01 16:12 | 2025-08-05 12:37 | 92 | 89 | 3 | 757 | 754 | 2 | 0 | 0 | 0 | 0 | 68 | 10 | 53 | 5 | 223 | 221 | 8 | 48 | 0 | 2 | 0 | 10 | 2 |
| ashleyskinner | 149 | 1,613 | 2024-11-04 13:40 | 2026-06-15 11:16 | 0 | 0 | 0 | 1,088 | 1,084 | 2 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 63 | 63 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| nathalie | 148 | 1,536 | 2024-11-02 13:25 | 2026-01-30 08:49 | 11 | 5 | 6 | 922 | 920 | 0 | 0 | 0 | 0 | 0 | 98 | 82 | 12 | 4 | 67 | 67 | 7 | 8 | 0 | 0 | 0 | 0 | 0 |
| jimroberts | 140 | 1,532 | 2024-11-04 16:38 | 2026-06-15 14:18 | 5 | 3 | 2 | 717 | 714 | 0 | 0 | 0 | 0 | 0 | 17 | 5 | 10 | 2 | 184 | 184 | 5 | 11 | 0 | 0 | 0 | 0 | 0 |
| karat | 54 | 1,314 | 2024-11-01 09:19 | 2026-04-29 19:10 | 17 | 9 | 8 | 667 | 640 | 3 | 0 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 248 | 246 | 9 | 15 | 0 | 0 | 1 | 3 | 0 |
| joemcmenemy | 96 | 1,261 | 2024-11-01 09:48 | 2025-03-28 14:20 | 70 | 35 | 35 | 521 | 507 | 2 | 0 | 0 | 0 | 0 | 41 | 30 | 9 | 2 | 94 | 93 | 0 | 18 | 0 | 0 | 0 | 11 | 1 |
| vwagoner | 196 | 1,161 | 2024-11-04 09:20 | 2026-06-15 21:04 | 4 | 1 | 3 | 492 | 486 | 6 | 0 | 0 | 0 | 0 | 19 | 11 | 3 | 0 | 37 | 28 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| kristenb | 71 | 849 | 2024-11-04 15:19 | 2026-03-30 16:34 | 299 | 8 | 291 | 146 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 183 | 156 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| joecryan | 97 | 814 | 2024-11-01 22:43 | 2026-06-15 19:54 | 108 | 47 | 61 | 142 | 139 | 2 | 0 | 0 | 0 | 0 | 12 | 2 | 10 | 0 | 118 | 115 | 3 | 3 | 0 | 0 | 2 | 9 | 2 |
| richardlovegrove | 113 | 807 | 2024-11-21 17:59 | 2026-06-09 09:06 | 0 | 0 | 0 | 308 | 279 | 17 | 0 | 0 | 0 | 0 | 10 | 1 | 9 | 0 | 54 | 54 | 1 | 12 | 0 | 0 | 0 | 0 | 0 |
| tracyp | 108 | 805 | 2024-11-04 08:17 | 2026-05-12 07:58 | 2 | 0 | 2 | 346 | 343 | 3 | 0 | 0 | 0 | 0 | 7 | 7 | 0 | 0 | 98 | 98 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| juneou | 88 | 777 | 2025-04-25 08:43 | 2026-06-11 23:35 | 0 | 0 | 0 | 344 | 263 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 139 | 139 | 2 | 3 | 0 | 0 | 0 | 0 | 0 |
| jerryburnsrep | 54 | 706 | 2025-08-07 13:07 | 2026-05-06 13:06 | 115 | 71 | 44 | 59 | 28 | 31 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 145 | 145 | 41 | 0 | 0 | 0 | 54 | 4 | 0 |
| samantham | 86 | 661 | 2024-11-01 11:46 | 2026-06-08 19:31 | 24 | 15 | 9 | 303 | 302 | 1 | 0 | 0 | 0 | 0 | 12 | 0 | 12 | 0 | 56 | 55 | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| kellywu | 142 | 655 | 2024-11-01 23:42 | 2026-06-11 22:42 | 0 | 0 | 0 | 322 | 319 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| brents | 99 | 586 | 2024-11-04 15:14 | 2026-06-15 16:10 | 0 | 0 | 0 | 164 | 164 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 60 | 60 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| tpait | 69 | 576 | 2024-11-07 13:40 | 2026-06-15 16:49 | 0 | 0 | 0 | 305 | 301 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 63 | 63 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| mrohearn | 86 | 564 | 2024-11-07 11:41 | 2026-05-13 22:41 | 0 | 0 | 0 | 55 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 207 | 207 | 6 | 0 | 0 | 0 | 0 | 0 | 0 |
| bretwallace | 137 | 557 | 2024-11-04 10:15 | 2026-06-15 13:27 | 25 | 2 | 23 | 25 | 3 | 6 | 0 | 0 | 0 | 0 | 82 | 71 | 10 | 1 | 48 | 48 | 8 | 17 | 0 | 0 | 0 | 4 | 0 |
| kellymagnussen | 70 | 554 | 2024-11-01 06:51 | 2026-06-12 10:37 | 17 | 10 | 7 | 67 | 40 | 26 | 0 | 0 | 0 | 0 | 34 | 2 | 30 | 1 | 3 | 3 | 8 | 56 | 0 | 0 | 0 | 3 | 0 |
| lafond | 35 | 502 | 2026-02-25 09:52 | 2026-06-11 20:19 | 26 | 0 | 26 | 131 | 129 | 2 | 0 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 68 | 68 | 11 | 5 | 0 | 0 | 0 | 0 | 0 |
| christinag | 28 | 487 | 2026-04-13 10:54 | 2026-06-15 13:24 | 0 | 0 | 0 | 103 | 103 | 0 | 0 | 0 | 0 | 0 | 17 | 0 | 17 | 0 | 110 | 110 | 0 | 15 | 0 | 0 | 0 | 0 | 0 |
| charlenegarcia | 21 | 394 | 2026-04-07 11:51 | 2026-06-05 15:31 | 0 | 0 | 0 | 245 | 244 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 68 | 68 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| torifarlow | 20 | 389 | 2024-11-12 13:17 | 2025-03-27 15:59 | 0 | 0 | 0 | 293 | 287 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 6 | 0 | 28 | 28 | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| kvarner | 4 | 378 | 2025-02-17 11:14 | 2025-03-10 12:01 | 0 | 0 | 0 | 174 | 173 | 1 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 11 | 11 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| jessiestroud | 32 | 371 | 2025-08-19 11:34 | 2026-04-25 15:34 | 0 | 0 | 0 | 175 | 158 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 75 | 75 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| wrivera | 30 | 347 | 2024-11-04 13:11 | 2025-03-31 06:20 | 3 | 3 | 0 | 143 | 124 | 19 | 0 | 0 | 0 | 0 | 50 | 14 | 36 | 0 | 24 | 24 | 1 | 0 | 0 | 0 | 0 | 0 | 1 |
| gracepolin | 61 | 315 | 2024-11-04 11:27 | 2025-10-07 09:38 | 0 | 0 | 0 | 19 | 10 | 1 | 0 | 0 | 0 | 0 | 11 | 0 | 11 | 0 | 92 | 92 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| devynbrown | 24 | 300 | 2025-06-25 09:01 | 2025-10-28 13:36 | 0 | 0 | 0 | 91 | 90 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 104 | 104 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tdoherty | 61 | 283 | 2025-08-18 09:22 | 2026-01-22 17:28 | 2 | 0 | 2 | 66 | 63 | 1 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 2 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| canonthysene | 57 | 259 | 2024-11-12 11:44 | 2026-06-05 12:26 | 0 | 0 | 0 | 36 | 17 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 40 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jerryburns | 23 | 202 | 2025-07-09 11:52 | 2026-06-15 15:39 | 38 | 1 | 37 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 46 | 46 | 5 | 0 | 0 | 0 | 0 | 0 | 0 |
| aidazamani | 37 | 163 | 2024-11-01 10:05 | 2025-05-01 09:20 | 0 | 0 | 0 | 67 | 67 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| michelem | 24 | 158 | 2024-11-13 15:01 | 2026-06-03 21:06 | 9 | 1 | 8 | 10 | 6 | 1 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 64 | 64 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| jmabe | 19 | 156 | 2024-11-14 08:48 | 2026-05-27 09:22 | 0 | 0 | 0 | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 78 | 78 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rcool01 | 38 | 136 | 2025-03-12 16:03 | 2025-11-21 11:55 | 1 | 1 | 0 | 19 | 18 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| bhinesley | 15 | 124 | 2025-01-03 15:15 | 2025-10-21 16:12 | 0 | 0 | 0 | 72 | 68 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 12 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| dovk | 10 | 93 | 2024-11-07 00:35 | 2025-10-23 02:04 | 9 | 9 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 24 | 3 | 0 | 0 | 0 | 0 | 17 | 1 |
| jonv | 12 | 72 | 2025-04-24 06:23 | 2025-11-11 15:08 | 10 | 9 | 1 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 11 | 0 | 1 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| chuck-user | 3 | 44 | 2025-04-01 17:07 | 2025-10-16 17:21 | 15 | 6 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kyla | 5 | 36 | 2025-11-25 15:04 | 2026-05-13 16:59 | 9 | 2 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| dplocki | 4 | 35 | 2024-11-20 10:54 | 2025-03-12 14:57 | 0 | 0 | 0 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kaylam | 8 | 33 | 2025-01-14 15:49 | 2026-05-06 15:56 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dougjermyn | 6 | 20 | 2024-11-27 14:27 | 2025-10-22 11:30 | 0 | 0 | 0 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| robmcsr | 1 | 18 | 2024-11-02 11:23 | 2024-11-02 11:59 | 1 | 1 | 0 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 4 | 0 | 0 | 0 | 0 | 0 |
| veeceeharris | 1 | 17 | 2026-03-13 15:08 | 2026-03-13 15:54 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| adamv | 5 | 16 | 2026-05-27 14:34 | 2026-06-05 14:56 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| swt | 3 | 7 | 2025-01-05 18:20 | 2025-04-17 14:48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| brentsanders | 1 | 6 | 2026-02-28 19:18 | 2026-02-28 19:19 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kjael | 1 | 5 | 2026-05-12 16:29 | 2026-05-12 19:15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| dkirsch | 2 | 3 | 2026-03-06 15:16 | 2026-04-22 17:30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| monicachen | 1 | 2 | 2024-11-09 02:24 | 2024-11-09 02:25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jordanjohnson | 1 | 1 | 2025-01-27 11:55 | 2025-01-27 11:55 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Q-01_step2_results.md

# Q-01-S2 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 29
- **Run date**: 2026-06-16


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Neil Phillips | 607 | $2.8M | $4,669 | 101 |
| Brad Bowman | 211 | $2.5M | $11,856 | 56 |
| Ray Harding | 26 | $1.2M | $48,023 | 0 |
| Julie Grothman | 140 | $865,373 | $6,181 | 31 |
| John Nord | 188 | $832,547 | $4,428 | 48 |
| Terri Lucas | 245 | $811,093 | $3,311 | 72 |
| Gregg Lesser | 108 | $756,185 | $7,002 | 32 |
| Jason Vanderhorst | 49 | $499,310 | $10,190 | 16 |
| Jerilyn DeRaad | 55 | $483,844 | $8,797 | 21 |
| Joe Helton | 34 | $421,200 | $12,388 | 0 |
| Mark Dimitshteyn | 141 | $415,053 | $2,944 | 51 |
| David Hadad | 58 | $414,158 | $7,141 | 32 |
| David Kirsch | 63 | $320,350 | $5,085 | 25 |
| Jacki Huelsenbeck | 87 | $291,596 | $3,352 | 32 |
| Fred  Schacter | 17 | $222,736 | $13,102 | 0 |
| Paul Comer | 36 | $166,023 | $4,612 | 19 |
| Sally Simerson | 9 | $108,143 | $12,016 | 7 |
| Frank LaDonna | 16 | $48,285 | $3,018 | 2 |
| Kaitlin Britz | 2 | $34,740 | $17,370 | 2 |
| Jackson Keziah | 5 | $28,010 | $5,602 | 5 |
| Peter Hauerbach | 4 | $26,100 | $6,525 | 0 |
| Mason OConnor | 3 | $24,635 | $8,212 | 2 |
| Jamie Schreiter | 4 | $19,972 | $4,993 | 0 |
| Grant Ford | 3 | $13,620 | $4,540 | 3 |
| Joe Cryan | 5 | $12,330 | $2,466 | 4 |
| Gary Geraci | 6 | $11,638 | $1,940 | 2 |
| Alan Erickson | 4 | $11,415 | $2,854 | 3 |
| Pierce Erickson | 1 | $1,515 | $1,515 | 1 |
| Dov Kessler | 1 | $1,185 | $1,185 | 1 |

### Q-04_results.md

# Q-04 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 103
- **Run date**: 2026-06-16


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| terrilucas | 539 | 21,319 | 413 | 7,013 | 2,908 | 13 | 401 | 113 | 16 | 417 | Selling Rep |
| rharding | 565 | 16,617 | 49 | 5,009 | 832 | 14 | 594 | 3 | 3 | 3,217 | Selling Rep |
| neilphillips | 450 | 15,736 | 1,081 | 7,731 | 644 | 1 | 27 | 0 | 5 | 1 | Selling Rep |
| masonoconnor | 389 | 14,971 | 4 | 9,021 | 1,126 | 1 | 243 | 0 | 9 | 724 | Selling Rep |
| jacksonkeziah | 436 | 13,825 | 14 | 5,429 | 1,660 | 47 | 778 | 14 | 9 | 157 | Selling Rep |
| johnnord | 485 | 13,355 | 313 | 5,819 | 1,099 | 126 | 271 | 0 | 12 | 121 | Selling Rep |
| jacobennis | 395 | 11,621 | 1 | 4,229 | 1,704 | 1 | 411 | 0 | 11 | 29 | Content/Library Manager |
| eileenfilloy | 183 | 10,320 | 0 | 3,041 | 1,025 | 1 | 193 | 90 | 14 | 651 | Content/Library Manager |
| grantford | 443 | 9,841 | 5 | 3,358 | 885 | 4 | 90 | 0 | 3 | 227 | Selling Rep |
| hdesk | 82 | 9,492 | 0 | 1,741 | 2,668 | 0 | 4 | 9 | 16 | 28 | Content/Library Manager |
| kaitlinb | 383 | 9,327 | 2 | 3,497 | 1,151 | 2 | 240 | 0 | 22 | 23 | Content/Library Manager |
| frankladonna | 482 | 9,171 | 21 | 4,376 | 514 | 7 | 210 | 46 | 27 | 2 | Selling Rep |
| dhadad | 340 | 8,162 | 78 | 2,439 | 1,840 | 11 | 137 | 0 | 186 | 63 | Selling Rep |
| sally-simerson | 385 | 7,780 | 19 | 3,161 | 1,045 | 26 | 63 | 0 | 49 | 16 | Selling Rep |
| danielmeyer | 466 | 7,350 | 0 | 3,077 | 1,113 | 25 | 134 | 1 | 28 | 1 | Content/Library Manager |
| mburcin | 402 | 7,127 | 0 | 3,879 | 496 | 0 | 183 | 0 | 5 | 0 | Content/Library Manager |
| markdimitshteyn | 434 | 7,125 | 218 | 2,131 | 764 | 3 | 256 | 0 | 15 | 0 | Selling Rep |
| jgrothman | 481 | 6,996 | 207 | 1,300 | 494 | 7 | 166 | 0 | 9 | 162 | Selling Rep |
| ajfilloy | 306 | 6,933 | 0 | 4,163 | 666 | 3 | 88 | 3 | 18 | 13 | Content/Library Manager |
| jamieschreiter | 436 | 6,550 | 4 | 2,015 | 936 | 2 | 32 | 0 | 4 | 18 | Selling Rep |
| jhelton | 479 | 6,218 | 63 | 687 | 2,041 | 12 | 3 | 0 | 49 | 0 | Selling Rep |
| chrise | 373 | 6,103 | 0 | 2,377 | 946 | 1 | 162 | 0 | 46 | 116 | Content/Library Manager |
| glesser | 475 | 6,072 | 160 | 165 | 1,975 | 158 | 45 | 0 | 13 | 2 | Selling Rep |
| paulcomer | 367 | 5,890 | 74 | 2,685 | 679 | 17 | 131 | 0 | 13 | 0 | Selling Rep |
| jasonk | 311 | 5,532 | 0 | 2,796 | 387 | 0 | 86 | 0 | 13 | 79 | Content/Library Manager |
| bbowman | 417 | 5,456 | 347 | 1,166 | 525 | 59 | 61 | 0 | 12 | 760 | Selling Rep |
| jderaad | 294 | 5,133 | 92 | 1,781 | 588 | 18 | 64 | 0 | 3 | 1 | Selling Rep |
| kirschint | 440 | 4,770 | 67 | 706 | 1,119 | 12 | 11 | 0 | 20 | 1 | Selling Rep |
| jacki | 323 | 4,537 | 124 | 2,196 | 304 | 8 | 58 | 0 | 3 | 0 | Selling Rep |
| ggeraci | 425 | 4,451 | 20 | 1,537 | 301 | 4 | 69 | 0 | 34 | 104 | Selling Rep |
| arodriguez | 150 | 4,399 | 0 | 1,328 | 392 | 2 | 181 | 0 | 12 | 135 | Content/Library Manager |
| phauerbach | 360 | 4,182 | 4 | 1,042 | 772 | 40 | 163 | 0 | 3 | 92 | Selling Rep |
| jwagers | 215 | 4,009 | 0 | 2,940 | 336 | 1 | 0 | 0 | 7 | 23 | Content/Library Manager |
| jeffc | 116 | 3,826 | 47 | 872 | 165 | 1 | 91 | 0 | 1 | 161 | Selling Rep |
| perickson | 230 | 3,806 | 1 | 1,176 | 419 | 1 | 64 | 0 | 14 | 288 | Content/Library Manager |
| jasonvanderhorst | 177 | 3,460 | 108 | 839 | 243 | 4 | 148 | 1 | 3 | 252 | Selling Rep |
| amandae | 324 | 3,316 | 0 | 1,434 | 497 | 4 | 0 | 0 | 0 | 2 | Content/Library Manager |
| fschacter | 317 | 2,969 | 43 | 1,077 | 332 | 8 | 9 | 0 | 5 | 10 | Selling Rep |
| davep | 459 | 2,560 | 0 | 86 | 210 | 6 | 0 | 0 | 1 | 0 | Content/Library Manager |
| bradm | 149 | 2,500 | 0 | 1,108 | 216 | 2 | 55 | 38 | 8 | 57 | Content/Library Manager |
| khelton | 225 | 2,283 | 3 | 563 | 659 | 8 | 0 | 0 | 3 | 0 | Selling Rep |
| lmoreno | 205 | 2,250 | 0 | 1,103 | 55 | 7 | 41 | 0 | 4 | 26 | Catalog/Data Manager |
| shannonl | 316 | 2,217 | 0 | 1,114 | 10 | 0 | 22 | 0 | 4 | 22 | Catalog/Data Manager |
| soconnor | 266 | 2,061 | 0 | 920 | 99 | 2 | 50 | 0 | 7 | 3 | Catalog/Data Manager |
| jacobkohns | 141 | 2,007 | 0 | 920 | 471 | 1 | 0 | 0 | 11 | 0 | Content/Library Manager |
| christinas | 123 | 1,967 | 0 | 431 | 380 | 0 | 80 | 0 | 4 | 88 | Content/Library Manager |
| meberlein | 413 | 1,893 | 0 | 35 | 4 | 0 | 0 | 0 | 0 | 0 | Sales Support/Inside Sales |
| kimtraver | 320 | 1,869 | 0 | 147 | 548 | 2 | 0 | 0 | 0 | 3 | Content/Library Manager |
| ammax | 165 | 1,834 | 0 | 631 | 188 | 0 | 83 | 0 | 4 | 0 | Catalog/Data Manager |
| aerickson | 104 | 1,834 | 4 | 279 | 284 | 1 | 13 | 0 | 45 | 35 | Selling Rep |
| bretwarren | 131 | 1,696 | 2 | 754 | 221 | 2 | 53 | 0 | 8 | 50 | Content/Library Manager |
| ashleyskinner | 149 | 1,613 | 0 | 1,084 | 63 | 0 | 3 | 0 | 3 | 0 | Sales Support/Inside Sales |
| nathalie | 148 | 1,536 | 0 | 920 | 67 | 0 | 12 | 0 | 7 | 8 | Sales Support/Inside Sales |
| jimroberts | 140 | 1,532 | 0 | 714 | 184 | 0 | 10 | 0 | 5 | 11 | Sales Support/Inside Sales |
| karat | 54 | 1,314 | 0 | 640 | 246 | 2 | 6 | 0 | 9 | 15 | Content/Library Manager |
| joemcmenemy | 96 | 1,261 | 1 | 507 | 93 | 1 | 9 | 0 | 0 | 18 | Sales Support/Inside Sales |
| vwagoner | 196 | 1,161 | 0 | 486 | 28 | 9 | 3 | 5 | 2 | 2 | Sales Support/Inside Sales |
| kristenb | 71 | 849 | 0 | 145 | 156 | 27 | 0 | 0 | 0 | 0 | Content/Library Manager |
| joecryan | 97 | 814 | 2 | 139 | 115 | 3 | 10 | 0 | 3 | 3 | Sales Support/Inside Sales |
| richardlovegrove | 113 | 807 | 0 | 279 | 54 | 0 | 9 | 0 | 1 | 12 | Sales Support/Inside Sales |
| tracyp | 108 | 805 | 0 | 343 | 98 | 0 | 0 | 0 | 6 | 0 | Sales Support/Inside Sales |
| juneou | 88 | 777 | 0 | 263 | 139 | 0 | 0 | 0 | 2 | 3 | Sales Support/Inside Sales |
| jerryburnsrep | 54 | 706 | 0 | 28 | 145 | 0 | 0 | 0 | 41 | 0 | Sales Support/Inside Sales |
| samantham | 86 | 661 | 0 | 302 | 55 | 1 | 12 | 0 | 1 | 4 | Sales Support/Inside Sales |
| kellywu | 142 | 655 | 0 | 319 | 9 | 0 | 0 | 0 | 0 | 0 | Sales Support/Inside Sales |
| brents | 99 | 586 | 0 | 164 | 60 | 0 | 0 | 0 | 4 | 0 | Sales Support/Inside Sales |
| tpait | 69 | 576 | 0 | 301 | 63 | 0 | 0 | 0 | 3 | 0 | Sales Support/Inside Sales |
| mrohearn | 86 | 564 | 0 | 40 | 207 | 0 | 0 | 0 | 6 | 0 | Content/Library Manager |
| bretwallace | 137 | 557 | 0 | 3 | 48 | 0 | 10 | 0 | 8 | 17 | Sales Support/Inside Sales |
| kellymagnussen | 70 | 554 | 0 | 40 | 3 | 0 | 30 | 1 | 8 | 56 | Catalog/Data Manager |
| lafond | 35 | 502 | 0 | 129 | 68 | 0 | 6 | 0 | 11 | 5 | Sales Support/Inside Sales |
| christinag | 28 | 487 | 0 | 103 | 110 | 0 | 17 | 0 | 0 | 15 | Inactive |
| charlenegarcia | 21 | 394 | 0 | 244 | 68 | 0 | 0 | 0 | 0 | 0 | Inactive |
| torifarlow | 20 | 389 | 0 | 287 | 28 | 0 | 6 | 0 | 1 | 4 | Inactive |
| kvarner | 4 | 378 | 0 | 173 | 11 | 0 | 3 | 0 | 0 | 5 | Inactive |
| jessiestroud | 32 | 371 | 0 | 158 | 75 | 0 | 0 | 0 | 2 | 0 | Low-Activity User |
| wrivera | 30 | 347 | 1 | 124 | 24 | 0 | 36 | 0 | 1 | 0 | Catalog/Data Manager |
| gracepolin | 61 | 315 | 0 | 10 | 92 | 0 | 11 | 0 | 0 | 1 | Low-Activity User |
| devynbrown | 24 | 300 | 0 | 90 | 104 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tdoherty | 61 | 283 | 0 | 63 | 2 | 0 | 4 | 0 | 2 | 2 | Low-Activity User |
| canonthysene | 57 | 259 | 0 | 17 | 40 | 0 | 0 | 0 | 0 | 0 | Low-Activity User |
| jerryburns | 23 | 202 | 0 | 13 | 46 | 0 | 0 | 1 | 5 | 0 | Inactive |
| aidazamani | 37 | 163 | 0 | 67 | 9 | 0 | 0 | 0 | 0 | 0 | Low-Activity User |
| michelem | 24 | 158 | 0 | 6 | 64 | 0 | 0 | 0 | 1 | 0 | Inactive |
| jmabe | 19 | 156 | 0 | 22 | 78 | 0 | 0 | 0 | 0 | 0 | Inactive |
| rcool01 | 38 | 136 | 0 | 18 | 4 | 0 | 0 | 0 | 2 | 0 | Low-Activity User |
| bhinesley | 15 | 124 | 0 | 68 | 12 | 0 | 0 | 0 | 1 | 0 | Inactive |
| dovk | 10 | 93 | 1 | 6 | 24 | 0 | 0 | 0 | 3 | 0 | Inactive |
| jonv | 12 | 72 | 0 | 0 | 3 | 0 | 1 | 10 | 0 | 0 | Inactive |
| chuck-user | 3 | 44 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kyla | 5 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | Inactive |
| dplocki | 4 | 35 | 0 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kaylam | 8 | 33 | 0 | 5 | 6 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dougjermyn | 6 | 20 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| robmcsr | 1 | 18 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 4 | Inactive |
| veeceeharris | 1 | 17 | 0 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| adamv | 5 | 16 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| swt | 3 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 1 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kjael | 1 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | Inactive |
| dkirsch | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| monicachen | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jordanjohnson | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 85 | 76 | 23 |

### Q-06_results.md

# Q-06 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 81
- **Run date**: 2026-06-16


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Neil Phillips | 205 | 227 | 10.70 | 106 | 206 | 94.30 | $1.1M |
| Terri Lucas | 264 | 398 | 50.80 | 47 | 67 | 42.60 | $190,954 |
| Brad Bowman | 117 | 142 | 21.40 | 53 | 66 | 24.50 | $938,525 |
| Mark Dimitshteyn | 92 | 164 | 78.30 | 20 | 51 | 155 | $180,535 |
| John Nord | 142 | 184 | 29.60 | 41 | 42 | 2.40 | $200,700 |
| Julie Grothman | 196 | 233 | 18.90 | 34 | 34 | 0 | $238,944 |
| Gregg Lesser | 162 | 165 | 1.90 | 21 | 32 | 52.40 | $261,835 |
| David Kirsch | 125 | 155 | 24 | 20 | 25 | 25 | $117,750 |
| David Hadad | 87 | 110 | 26.40 | 5 | 21 | 320 | $129,687 |
| Jacki Huelsenbeck | 85 | 67 | -21.20 | 30 | 20 | -33.30 | $60,900 |
| Paul Comer | 74 | 111 | 50 | 8 | 14 | 75 | $27,285 |
| Frank LaDonna | 137 | 205 | 49.60 | 1 | 13 | 1,200 | $17,950 |
| Joe Helton | 236 | 248 | 5.10 | 8 | 11 | 37.50 | $149,765 |
| Ray Harding | 459 | 535 | 16.60 | 4 | 10 | 150 | $606,660 |
| Jerilyn DeRaad | 77 | 107 | 39 | 21 | 9 | -57.10 | $115,900 |
| Fred  Schacter | 72 | 92 | 27.80 | 2 | 5 | 150 | $70,595 |
| Jackson Keziah | 105 | 147 | 40 | 1 | 2 | 100 | $24,640 |
| Sally Simerson | 85 | 169 | 98.80 | 4 | 2 | -50 | $4,720 |
| Joe Cryan | 27 | 26 | -3.70 | 3 | 1 | -66.70 | $4,155 |
| Pierce Erickson | 54 | 60 | 11.10 | 0 | 1 | — | $1,515 |
| Jamie Schreiter | 106 | 118 | 11.30 | 0 | 1 | — | $11,142 |
| Peter Hauerbach | 96 | 158 | 64.60 | 1 | 1 | 0 | $3,075 |
| Kaitlin Britz | 85 | 110 | 29.40 | 0 | 1 | — | $3,615 |
| Jason Vanderhorst | 19 | 6 | -68.40 | 17 | 0 | -100 | $0 |
| Mason OConnor | 74 | 109 | 47.30 | 1 | 0 | -100 | $0 |
| Alan Erickson | 5 | 38 | 660 | 1 | 0 | -100 | $0 |
| Grant Ford | 128 | 144 | 12.50 | 1 | 0 | -100 | $0 |
| Sean O'Connor | 53 | 41 | -22.60 | — | — | — | — |
| Kristen Bruce | 14 | 6 | -57.10 | — | — | — | — |
| Richard Lovegrove | 22 | 29 | 31.80 | — | — | — | — |
| Tim Pait | 1 | 2 | 100 | — | — | — | — |
| Kyla Bosch | 0 | 5 | — | — | — | — | — |
| Gary Geraci | 96 | 93 | -3.10 | — | — | — | — |
| AJ Filloy | 106 | 129 | 21.70 | — | — | — | — |
| Valerie Wagoner | 13 | 50 | 284.60 | — | — | — | — |
| Ashley Skinner | 14 | 38 | 171.40 | — | — | — | — |
| Taylor  Doherty | 8 | 0 | -100 | — | — | — | — |
| Brent Schiedel | 12 | 53 | 341.70 | — | — | — | — |
| Brad Miller | 56 | 109 | 94.60 | — | — | — | — |
| Jacob Ennis | 65 | 138 | 112.30 | — | — | — | — |
| Christina Grove | 0 | 51 | — | — | — | — | — |
| Alvin Rodriguez | 31 | 65 | 109.70 | — | — | — | — |
| Chan Anonthysene | 0 | 10 | — | — | — | — | — |
| Jason Kaiser | 59 | 95 | 61 | — | — | — | — |
| Chris Elliott | 94 | 128 | 36.20 | — | — | — | — |
| Janine Wagers | 31 | 32 | 3.20 | — | — | — | — |
| Kim Traver | 69 | 81 | 17.40 | — | — | — | — |
| Lina Moreno | 29 | 32 | 10.30 | — | — | — | — |
| Mike Eberlein | 91 | 113 | 24.20 | — | — | — | — |
| Rachel Lafond | 12 | 35 | 191.70 | — | — | — | — |
| Samantha Murray | 5 | 16 | 220 | — | — | — | — |
| Jacob Kohns | 59 | 91 | 54.20 | — | — | — | — |
| VeeCee Harris | 1 | 0 | -100 | — | — | — | — |
| Christina Smith | 22 | 13 | -40.90 | — | — | — | — |
| David Pianezza | 94 | 136 | 44.70 | — | — | — | — |
| Bret Wallace | 26 | 27 | 3.80 | — | — | — | — |
| Daniel Meyer | 126 | 154 | 22.20 | — | — | — | — |
| Matt O'Hearn | 13 | 14 | 7.70 | — | — | — | — |
| Michele Morgan | 9 | 7 | -22.20 | — | — | — | — |
| Eileen Filloy | 58 | 85 | 46.60 | — | — | — | — |
| Michael Burcin | 94 | 120 | 27.70 | — | — | — | — |
| Amanda Edwards | 92 | 95 | 3.30 | — | — | — | — |
| Shannon Lookabill | 73 | 63 | -13.70 | — | — | — | — |
| Tracy Pekkala | 3 | 15 | 400 | — | — | — | — |
| Jessie Stroud | 2 | 7 | 250 | — | — | — | — |
| Kayla Miller | 4 | 2 | -50 | — | — | — | — |
| Charlene Garcia | 0 | 29 | — | — | — | — | — |
| Jerry Burns (Rep) | 11 | 12 | 9.10 | — | — | — | — |
| Adam Varner | 0 | 6 | — | — | — | — | — |
| Brent Sanders | 3 | 0 | -100 | — | — | — | — |
| June Ou | 14 | 80 | 471.40 | — | — | — | — |
| Kjael Skaalerud | 0 | 2 | — | — | — | — | — |
| Kelly Wu | 13 | 17 | 30.80 | — | — | — | — |
| Jerry Burns (Admin) | 2 | 33 | 1,550 | — | — | — | — |
| Nathalie Hetu | 10 | 0 | -100 | — | — | — | — |
| Jim Roberts | 22 | 57 | 159.10 | — | — | — | — |
| Max Amini | 33 | 53 | 60.60 | — | — | — | — |
| Kelly Magnussen | 11 | 19 | 72.70 | — | — | — | — |
| Kara Tracey | 0 | 25 | — | — | — | — | — |
| Jack Mabe | 3 | 3 | 0 | — | — | — | — |
| Samson Helpdesk | 0 | 240 | — | — | — | — | — |

### Q-43_step2_results.md

# Q-43-S2 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16
- **Total flagged**: 0
- **Aggregate GMV**: $0

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### Q-51_results.md

(not present — file does not exist or is empty)

### Q-62_results.md

(not present — file does not exist or is empty)

### Q-63_results.md

# Q-63 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| neilphillips | 57 | 1,146 | 180 | 315.80 | 15.70 | 1,142 | 0 | 4 |
| masonoconnor | 21 | 607 | 0 | 0 | 0 | 588 | 19 | 0 |
| kaitlinb | 18 | 595 | 1 | 5.60 | 0.20 | 574 | 21 | 0 |
| jacksonkeziah | 31 | 591 | 2 | 6.50 | 0.30 | 556 | 35 | 0 |
| sally-simerson | 20 | 588 | 2 | 10 | 0.30 | 587 | 1 | 0 |
| jacobennis | 28 | 579 | 0 | 0 | 0 | 568 | 11 | 0 |
| johnnord | 19 | 570 | 37 | 194.70 | 6.50 | 562 | 8 | 0 |
| grantford | 40 | 521 | 0 | 0 | 0 | 511 | 10 | 0 |
| terrilucas | 32 | 360 | 55 | 171.90 | 15.30 | 350 | 9 | 1 |
| markdimitshteyn | 17 | 246 | 40 | 235.30 | 16.30 | 233 | 13 | 0 |
| mburcin | 12 | 245 | 0 | 0 | 0 | 237 | 8 | 0 |
| jasonk | 13 | 207 | 0 | 0 | 0 | 207 | 0 | 0 |
| paulcomer | 14 | 202 | 11 | 78.60 | 5.40 | 187 | 15 | 0 |
| frankladonna | 15 | 200 | 13 | 86.70 | 6.50 | 191 | 9 | 0 |
| jgrothman | 17 | 137 | 25 | 147.10 | 18.20 | 137 | 0 | 0 |
| dhadad | 10 | 132 | 14 | 140 | 10.60 | 127 | 4 | 1 |
| bbowman | 18 | 119 | 41 | 227.80 | 34.50 | 114 | 2 | 3 |
| jderaad | 14 | 111 | 6 | 42.90 | 5.40 | 97 | 14 | 0 |
| fschacter | 4 | 101 | 5 | 125 | 5 | 91 | 5 | 5 |
| jacki | 7 | 97 | 17 | 242.90 | 17.50 | 94 | 3 | 0 |

### Q-64_results.md

# Q-64 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| hdesk | 1 | 62 | 1 | 1 | 0 |
| arodriguez | 5 | 50.60 | 1 | 3 | 2 |
| kaitlinb | 28 | 46.30 | 3.60 | 19 | 5 |
| masonoconnor | 23 | 36 | 2.90 | 20 | 1 |
| davep | 5 | 36 | 4.40 | 4 | 0 |
| sally-simerson | 27 | 35.70 | 3 | 18 | 3 |
| mburcin | 14 | 31.60 | 1.90 | 12 | 0 |
| frankladonna | 20 | 30.40 | 2.80 | 17 | 1 |
| dhadad | 18 | 30.30 | 2.50 | 13 | 2 |
| jacobennis | 33 | 30.10 | 2.70 | 29 | 0 |
| ammax | 1 | 30 | 4 | 1 | 0 |
| jimroberts | 3 | 28.70 | 2 | 2 | 1 |
| johnnord | 42 | 25.30 | 2 | 21 | 9 |
| chrise | 3 | 23.70 | 2.30 | 2 | 0 |
| neilphillips | 83 | 22.60 | 2.40 | 54 | 10 |
| grantford | 68 | 21.70 | 2.50 | 40 | 6 |
| fschacter | 9 | 20.60 | 1.30 | 4 | 2 |
| lafond | 6 | 19.20 | 1.50 | 2 | 1 |
| jderaad | 29 | 19.10 | 1.90 | 19 | 5 |
| paulcomer | 27 | 18.60 | 1.90 | 12 | 4 |

### Q-65_results.md

# Q-65 Results — Universal Furniture (ufi, org_id=18)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| neilphillips | 2,968 | 2,321 | 647 | 78.20 | 21.80 |
| jwagers | 774 | 587 | 187 | 75.80 | 24.20 |
| ashleyskinner | 388 | 288 | 100 | 74.20 | 25.80 |
| masonoconnor | 1,651 | 1,149 | 502 | 69.60 | 30.40 |
| karat | 452 | 303 | 149 | 67 | 33 |
| jasonk | 1,150 | 768 | 382 | 66.80 | 33.20 |
| jacobennis | 2,144 | 1,405 | 739 | 65.50 | 34.50 |
| grantford | 1,918 | 1,208 | 710 | 63 | 37 |
| jacki | 761 | 477 | 284 | 62.70 | 37.30 |
| johnnord | 2,623 | 1,637 | 986 | 62.40 | 37.60 |
| sally-simerson | 1,776 | 1,101 | 675 | 62 | 38 |
| charlenegarcia | 394 | 244 | 150 | 61.90 | 38.10 |
| samantham | 147 | 89 | 58 | 60.50 | 39.50 |
| mburcin | 1,558 | 909 | 649 | 58.30 | 41.70 |
| ajfilloy | 1,011 | 581 | 430 | 57.50 | 42.50 |
| jacksonkeziah | 2,834 | 1,623 | 1,211 | 57.30 | 42.70 |
| shannonl | 242 | 133 | 109 | 55 | 45 |
| markdimitshteyn | 1,504 | 802 | 702 | 53.30 | 46.70 |
| jacobkohns | 728 | 386 | 342 | 53 | 47 |
| vwagoner | 256 | 135 | 121 | 52.70 | 47.30 |

### Q-70_results.md

(not present — file does not exist or is empty)

### user_group_mapping.md

# User Group Mapping — Universal Furniture (ufi, org_id=18)
- **Run date**: 2026-06-16
- **Total Postgres users**: 120
- **Matched to Mixpanel (Q-01 Step 1)**: 85 of 103 (83%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| UFI Sales Reps | field_rep | 36 |
| Admin UFI | admin_internal | 35 |
| UFI Sales Reps - Portal Testers | field_rep | 8 |
| BYC Canada General Rep | other | 7 |
| Lacquercraft Admin | admin_internal | 7 |
| Sales Portal Testers | admin_internal | 6 |
| International 1 | other | 3 |
| Sales VP - East | admin_internal | 3 |
| Sales VP - West | admin_internal | 3 |
| z-SuperCat | admin_internal | 3 |
| BYC Canada Admin | admin_internal | 2 |
| BYC Canada Leons | other | 1 |
| BYC Canada The Bay | other | 1 |
| International 2 | other | 1 |
| LQ Special DC-WH | other | 1 |
| Sales Portal Testers | field_rep | 1 |
| UFII Contract Business | other | 1 |
| eCat Online | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 35 | 254,470 | 76.6% |
| admin_internal | 37 | 48,862 | 14.7% |
| other | 13 | 28,922 | 8.7% |
