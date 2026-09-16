# Section 2 Context Bundle — RENWIL (rw)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: True; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | False | portal_order_count=0, portal_order_gmv=$0 |
| HAS_INVENTORY | True | inventory_count=2048 |
| HAS_SALES_DATA | False | sales_data_count=0 |
| HAS_SALES_SECTION | True | qualifying_reps=46 (threshold: >=5) |
| HAS_PEER_DATA | True | segment_peer_comparison row found, segment=Platform-Embedded |
| BENCHMARK_ELIGIBLE | True |  |
| BENCHMARK_CONFIDENCE | N/A |  |
| PEER_GROUP_LEVEL | N/A |  |
| PEER_GROUP_N | 0 |  |
| PEER_GROUP_ID_EFFECTIVE | N/A |  |
| CLICKY_PREFIX | renwil_rw_eol |  |

## Derived Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| VM45_GATE_1 | SKIP |  |
| VM45_GATE_2 | SKIP |  |
| VM45_RENDER | False |  |
| QUALIFYING_REP_COUNT | 46 | 46 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 90 rows |
| SHOWROOM_EXCLUSIONS | 1 | 1 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 8667, Mixpanel total submit_order (Q-01): 9991 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=93.3%, ambiguous_rate=1.2%, showroom_event_share=6.4% |
| USER_GROUP_JOIN_RATE | 93% | 84 of 90 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 6% | showroom+admin share of matched events: 6.4% |
| ADMIN_REPS_IN_LEADERBOARD | True | 3 admin/showroom users in leaderboard: Suzanne Hogan, Chuck Wiebe, Haris Baig |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | False |  |
| PORTAL_REP_DATA_PRESENT | False |  |
| PORTAL_CUSTOMER_DATA_PRESENT | False |  |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=184 |
| HAS_BUYER_DATA | False | distinct_buyers_6mo=0 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | STRONG | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | PARTIAL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | PARTIAL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: RENWIL
- **Shortname**: rw
- **Org ID**: 248
- **Bundle**: 7
- **Bundle label for report**: 7

## Validation Log

- portal_orders LTM count=0, gmv=0.0 — HAS_PORTAL_ORDERS overridden to false

## Section Confidence

# Section Confidence Tiers — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16

## Input Flags

| Flag | Value |
| --- | --- |
| HAS_SALES_SECTION | True |
| MIXPANEL_USER_DATA_PRESENT | True |
| PORTAL_REP_DATA_PRESENT | False |
| PORTAL_CUSTOMER_DATA_PRESENT | False |
| PORTAL_ORDERS_FRESH | False |
| HAS_PORTAL_ORDERS | False |
| HAS_INVENTORY | True |
| HAS_SALES_DATA | False |
| INVENTORY_FRESH | True |
| SALES_DATA_FRESH | False |
| CUSTOMER_DATA_FRESH | True |

## Computed Tiers

| Section | Tier | Determining Condition |
| --- | --- | --- |
| §2 Sales Team | STRONG | See Derived Gate 6 §2 formula |
| §3 Customer | PARTIAL | See Derived Gate 6 §3 formula |
| §4 Product | STRONG | See Derived Gate 6 §4 formula |
| §5 Commerce | PARTIAL | See Derived Gate 6 §5 formula |

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

# Q-01-S1 Results — RENWIL (rw, org_id=248)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 90
- **Run date**: 2026-06-16


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| louisep | 359 | 14,457 | 2025-02-12 09:40 | 2026-06-15 12:25 | 4,152 | 1,632 | 2,520 | 5,562 | 5,553 | 9 | 1,572 | 1,572 | 0 | 0 | 24 | 8 | 15 | 1 | 85 | 57 | 7 | 21 | 0 | 0 | 1 | 594 | 1,243 |
| roxannet | 246 | 11,763 | 2025-02-18 13:36 | 2026-06-15 19:01 | 5,087 | 922 | 4,165 | 88 | 49 | 39 | 972 | 972 | 0 | 0 | 1 | 0 | 1 | 0 | 163 | 91 | 16 | 0 | 0 | 0 | 6 | 285 | 706 |
| sandran | 339 | 11,482 | 2025-02-10 15:10 | 2026-06-15 14:43 | 2,883 | 946 | 1,937 | 4,223 | 4,177 | 45 | 1,164 | 1,164 | 0 | 0 | 10 | 4 | 3 | 3 | 188 | 180 | 9 | 24 | 0 | 1 | 5 | 340 | 1,307 |
| denisef | 340 | 10,665 | 2025-02-26 13:01 | 2026-06-15 19:17 | 3,143 | 1,158 | 1,985 | 1,188 | 1,166 | 22 | 324 | 324 | 0 | 0 | 96 | 0 | 87 | 8 | 157 | 157 | 76 | 3 | 0 | 0 | 21 | 298 | 97 |
| torontoshowroom | 338 | 10,540 | 2025-02-19 11:05 | 2026-06-15 19:27 | 3,468 | 1,190 | 2,278 | 3,040 | 3,017 | 22 | 1,696 | 1,696 | 0 | 0 | 5 | 0 | 5 | 0 | 99 | 60 | 5 | 9 | 0 | 2 | 15 | 290 | 811 |
| smethurst | 205 | 8,659 | 2025-04-29 14:03 | 2026-06-15 15:30 | 2,454 | 545 | 1,909 | 3,028 | 3,022 | 5 | 1,860 | 1,860 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 6 | 0 | 0 | 0 | 3 | 229 | 375 |
| robt | 293 | 8,278 | 2025-02-10 17:53 | 2026-06-15 13:10 | 1,966 | 841 | 1,125 | 2,836 | 2,823 | 1 | 1,032 | 1,032 | 0 | 0 | 60 | 1 | 56 | 3 | 176 | 159 | 1 | 73 | 0 | 1 | 6 | 286 | 616 |
| pauld | 261 | 8,222 | 2025-03-06 11:11 | 2026-06-15 17:00 | 3,708 | 792 | 2,916 | 2,154 | 2,149 | 5 | 502 | 502 | 0 | 0 | 37 | 1 | 36 | 0 | 37 | 31 | 8 | 0 | 0 | 0 | 9 | 360 | 583 |
| suzanneh | 142 | 6,072 | 2025-02-12 12:40 | 2026-06-15 18:11 | 810 | 224 | 586 | 1,230 | 1,177 | 52 | 221 | 221 | 0 | 0 | 142 | 11 | 120 | 10 | 34 | 34 | 33 | 36 | 0 | 0 | 0 | 111 | 55 |
| pgould | 216 | 5,077 | 2024-12-20 19:10 | 2026-06-11 10:54 | 1,012 | 445 | 567 | 2,111 | 2,109 | 2 | 711 | 711 | 0 | 0 | 11 | 11 | 0 | 0 | 29 | 29 | 1 | 0 | 0 | 0 | 4 | 12 | 683 |
| marcg | 176 | 4,141 | 2025-04-25 11:10 | 2026-06-15 16:44 | 1,434 | 400 | 1,034 | 289 | 287 | 2 | 418 | 418 | 0 | 0 | 30 | 1 | 27 | 2 | 6 | 6 | 12 | 20 | 0 | 0 | 2 | 69 | 223 |
| neil513 | 304 | 3,909 | 2024-12-30 15:40 | 2026-06-15 14:57 | 1,175 | 436 | 739 | 1,282 | 1,275 | 7 | 214 | 214 | 0 | 0 | 6 | 5 | 0 | 1 | 70 | 68 | 4 | 4 | 0 | 0 | 11 | 48 | 146 |
| roxannep | 231 | 3,688 | 2025-02-11 16:42 | 2026-06-11 22:42 | 406 | 401 | 5 | 1,298 | 1,266 | 32 | 294 | 294 | 0 | 0 | 19 | 9 | 10 | 0 | 399 | 309 | 10 | 27 | 0 | 0 | 19 | 197 | 262 |
| jfraser | 228 | 3,539 | 2025-01-08 17:37 | 2026-06-15 17:47 | 504 | 335 | 169 | 1,460 | 1,460 | 0 | 424 | 424 | 0 | 0 | 63 | 2 | 60 | 1 | 34 | 26 | 18 | 16 | 0 | 1 | 1 | 12 | 179 |
| jeanb | 150 | 3,366 | 2025-02-18 10:15 | 2026-06-12 09:00 | 284 | 173 | 111 | 250 | 236 | 13 | 513 | 513 | 0 | 0 | 20 | 1 | 19 | 0 | 21 | 19 | 29 | 9 | 0 | 0 | 5 | 30 | 104 |
| sandyg | 162 | 3,061 | 2025-02-15 12:21 | 2026-06-12 10:11 | 670 | 271 | 399 | 1,120 | 1,101 | 19 | 435 | 435 | 0 | 0 | 5 | 2 | 3 | 0 | 102 | 95 | 15 | 3 | 0 | 3 | 2 | 13 | 165 |
| areiman | 185 | 3,033 | 2025-02-04 15:54 | 2026-06-11 17:44 | 874 | 314 | 560 | 912 | 912 | 0 | 419 | 419 | 0 | 0 | 0 | 0 | 0 | 0 | 11 | 10 | 3 | 0 | 0 | 0 | 1 | 24 | 224 |
| samantham | 187 | 2,754 | 2025-01-14 15:57 | 2026-06-15 17:50 | 547 | 247 | 300 | 1,017 | 962 | 55 | 151 | 151 | 0 | 0 | 67 | 4 | 57 | 3 | 92 | 88 | 10 | 74 | 0 | 4 | 1 | 23 | 189 |
| rgould | 201 | 2,677 | 2024-12-30 09:49 | 2026-06-15 19:53 | 623 | 279 | 344 | 951 | 951 | 0 | 230 | 230 | 0 | 0 | 8 | 4 | 4 | 0 | 48 | 46 | 4 | 0 | 0 | 0 | 5 | 47 | 295 |
| theresah | 172 | 2,585 | 2025-02-13 10:37 | 2026-06-04 09:03 | 625 | 267 | 358 | 742 | 736 | 6 | 195 | 195 | 0 | 0 | 26 | 4 | 21 | 1 | 91 | 79 | 5 | 28 | 0 | 0 | 2 | 74 | 84 |
| tmatchunis | 161 | 2,538 | 2025-02-19 14:23 | 2026-06-15 17:27 | 839 | 264 | 575 | 733 | 727 | 4 | 207 | 207 | 0 | 0 | 1 | 0 | 1 | 0 | 41 | 38 | 31 | 0 | 0 | 0 | 0 | 79 | 162 |
| jgerber | 239 | 2,436 | 2025-02-11 14:50 | 2026-06-15 15:18 | 1,139 | 218 | 921 | 373 | 369 | 4 | 14 | 14 | 0 | 0 | 4 | 0 | 0 | 4 | 5 | 4 | 0 | 15 | 0 | 0 | 3 | 42 | 149 |
| mh-dewing | 153 | 2,334 | 2025-01-22 11:29 | 2026-06-15 16:27 | 603 | 151 | 452 | 697 | 686 | 11 | 74 | 74 | 0 | 0 | 41 | 2 | 39 | 0 | 58 | 51 | 38 | 38 | 0 | 0 | 2 | 39 | 53 |
| tannerg | 206 | 2,331 | 2024-12-20 13:02 | 2026-06-15 13:33 | 531 | 203 | 328 | 810 | 802 | 8 | 237 | 237 | 0 | 0 | 13 | 7 | 6 | 0 | 29 | 29 | 0 | 1 | 0 | 0 | 9 | 10 | 163 |
| marieandersen | 150 | 2,243 | 2025-02-16 12:51 | 2026-06-02 15:04 | 248 | 233 | 15 | 713 | 710 | 0 | 236 | 236 | 0 | 0 | 22 | 17 | 5 | 0 | 102 | 91 | 1 | 6 | 0 | 0 | 9 | 165 | 65 |
| haris | 150 | 2,014 | 2024-11-28 12:03 | 2026-06-11 15:21 | 486 | 159 | 327 | 386 | 354 | 32 | 35 | 35 | 0 | 0 | 19 | 4 | 14 | 1 | 95 | 88 | 27 | 25 | 0 | 0 | 0 | 24 | 31 |
| renwil | 122 | 1,943 | 2025-03-10 13:18 | 2026-02-09 16:18 | 365 | 146 | 219 | 333 | 307 | 26 | 77 | 77 | 0 | 0 | 13 | 1 | 11 | 0 | 68 | 68 | 48 | 48 | 0 | 5 | 0 | 27 | 35 |
| lreinhardt | 43 | 1,918 | 2025-02-11 16:02 | 2026-06-10 19:31 | 46 | 37 | 9 | 948 | 935 | 13 | 622 | 622 | 0 | 0 | 3 | 1 | 1 | 1 | 16 | 15 | 7 | 26 | 0 | 5 | 0 | 15 | 4 |
| pattyj | 90 | 1,812 | 2025-01-27 18:03 | 2026-06-12 15:38 | 253 | 173 | 80 | 398 | 377 | 19 | 152 | 152 | 0 | 0 | 14 | 3 | 10 | 1 | 115 | 115 | 18 | 29 | 0 | 3 | 6 | 105 | 30 |
| mandanas | 123 | 1,803 | 2025-02-14 11:40 | 2026-06-11 12:13 | 375 | 188 | 187 | 632 | 628 | 4 | 210 | 210 | 0 | 0 | 0 | 0 | 0 | 0 | 65 | 63 | 12 | 0 | 0 | 0 | 4 | 118 | 110 |
| tdufresne | 178 | 1,744 | 2025-02-15 11:30 | 2026-06-11 11:37 | 242 | 163 | 79 | 663 | 653 | 10 | 154 | 154 | 0 | 0 | 5 | 5 | 0 | 0 | 116 | 95 | 18 | 0 | 0 | 0 | 3 | 34 | 101 |
| seth | 323 | 1,639 | 2025-02-03 20:16 | 2026-06-15 15:32 | 288 | 129 | 159 | 285 | 283 | 1 | 67 | 67 | 0 | 0 | 0 | 0 | 0 | 0 | 149 | 149 | 8 | 0 | 0 | 0 | 0 | 11 | 34 |
| larryg | 90 | 1,571 | 2025-02-11 09:03 | 2025-11-01 09:52 | 887 | 146 | 741 | 208 | 206 | 2 | 141 | 141 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 1 | 26 | 107 |
| dennisg | 101 | 1,564 | 2025-02-25 06:50 | 2026-06-13 07:26 | 366 | 280 | 86 | 292 | 253 | 38 | 45 | 45 | 0 | 0 | 121 | 80 | 39 | 2 | 13 | 13 | 14 | 21 | 0 | 1 | 1 | 15 | 74 |
| melissak | 76 | 1,426 | 2025-04-21 11:00 | 2025-11-13 15:04 | 573 | 122 | 451 | 170 | 166 | 4 | 141 | 141 | 0 | 0 | 6 | 0 | 6 | 0 | 13 | 13 | 5 | 0 | 0 | 0 | 0 | 26 | 47 |
| walfab_central | 83 | 1,176 | 2025-11-13 15:07 | 2026-06-10 13:07 | 499 | 143 | 356 | 332 | 332 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 3 | 0 | 0 | 6 | 18 | 84 |
| wendybuzzard | 142 | 1,158 | 2025-01-01 09:42 | 2026-06-08 09:02 | 165 | 48 | 117 | 268 | 249 | 19 | 24 | 24 | 0 | 0 | 10 | 2 | 8 | 0 | 143 | 136 | 10 | 1 | 0 | 0 | 3 | 21 | 15 |
| bgraham | 103 | 1,098 | 2025-01-02 14:33 | 2026-06-11 15:57 | 102 | 53 | 49 | 152 | 140 | 12 | 28 | 28 | 0 | 0 | 95 | 46 | 47 | 1 | 140 | 136 | 3 | 10 | 0 | 0 | 0 | 5 | 8 |
| tamig708 | 128 | 932 | 2025-02-14 12:46 | 2026-06-14 14:26 | 298 | 107 | 191 | 267 | 266 | 1 | 21 | 21 | 0 | 0 | 0 | 0 | 0 | 0 | 11 | 8 | 0 | 1 | 0 | 0 | 0 | 13 | 62 |
| brandonk | 103 | 923 | 2025-02-20 16:17 | 2026-06-10 11:06 | 139 | 55 | 84 | 238 | 233 | 5 | 104 | 104 | 0 | 0 | 9 | 6 | 0 | 3 | 70 | 51 | 4 | 6 | 0 | 0 | 3 | 13 | 31 |
| annacowan | 92 | 815 | 2025-01-01 12:51 | 2025-11-21 13:39 | 240 | 77 | 163 | 180 | 178 | 1 | 84 | 84 | 0 | 0 | 2 | 0 | 2 | 0 | 11 | 11 | 0 | 0 | 0 | 0 | 4 | 15 | 14 |
| bbonardelli | 50 | 808 | 2025-05-06 11:32 | 2026-06-12 10:50 | 261 | 47 | 214 | 259 | 258 | 1 | 110 | 110 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 42 |
| jimmileak | 50 | 806 | 2025-06-18 11:11 | 2026-05-20 10:56 | 156 | 79 | 77 | 100 | 100 | 0 | 126 | 126 | 0 | 0 | 16 | 3 | 13 | 0 | 89 | 59 | 2 | 3 | 0 | 0 | 0 | 17 | 14 |
| ljfunk | 71 | 643 | 2024-12-26 11:27 | 2026-06-01 09:02 | 318 | 69 | 249 | 80 | 76 | 4 | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 9 | 29 |
| cezar | 115 | 592 | 2025-02-18 14:28 | 2026-06-12 23:57 | 25 | 11 | 14 | 163 | 162 | 1 | 1 | 1 | 0 | 0 | 3 | 0 | 3 | 0 | 84 | 77 | 0 | 0 | 0 | 0 | 0 | 5 | 6 |
| adriant | 28 | 513 | 2025-06-18 13:15 | 2026-06-05 13:12 | 53 | 40 | 13 | 88 | 88 | 0 | 17 | 17 | 0 | 0 | 9 | 0 | 9 | 0 | 6 | 6 | 3 | 1 | 0 | 0 | 1 | 10 | 4 |
| carlac | 74 | 503 | 2025-02-20 16:10 | 2026-06-12 14:37 | 149 | 33 | 116 | 108 | 101 | 7 | 2 | 2 | 0 | 0 | 4 | 1 | 3 | 0 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 16 | 1 |
| jjastal | 88 | 465 | 2024-12-31 14:13 | 2026-06-15 13:34 | 148 | 31 | 117 | 59 | 59 | 0 | 6 | 6 | 0 | 0 | 1 | 0 | 1 | 0 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 5 | 15 |
| jonathan | 97 | 452 | 2025-01-07 22:19 | 2026-04-13 09:47 | 61 | 7 | 54 | 79 | 65 | 7 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 15 | 13 | 2 | 0 | 0 | 0 | 0 | 1 | 1 |
| carlosb | 51 | 436 | 2025-02-20 16:23 | 2026-06-04 14:46 | 143 | 19 | 124 | 96 | 63 | 21 | 9 | 9 | 0 | 0 | 2 | 2 | 0 | 0 | 34 | 33 | 3 | 1 | 0 | 0 | 0 | 3 | 4 |
| dianecresante | 95 | 334 | 2025-02-10 17:00 | 2026-06-14 08:37 | 42 | 17 | 25 | 55 | 53 | 2 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 19 | 19 | 2 | 0 | 0 | 0 | 0 | 3 | 1 |
| lance | 95 | 324 | 2025-02-11 12:07 | 2026-06-15 10:59 | 27 | 27 | 0 | 71 | 67 | 4 | 5 | 5 | 0 | 0 | 1 | 0 | 0 | 1 | 9 | 7 | 7 | 3 | 0 | 0 | 0 | 10 | 15 |
| carolynl | 60 | 314 | 2025-02-24 13:45 | 2026-06-10 01:13 | 29 | 1 | 28 | 166 | 164 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 |
| robertbonardelli | 40 | 294 | 2025-01-22 14:48 | 2025-10-20 20:04 | 21 | 17 | 4 | 10 | 3 | 5 | 2 | 2 | 0 | 0 | 33 | 30 | 3 | 0 | 54 | 53 | 0 | 0 | 0 | 0 | 0 | 19 | 0 |
| mestrin | 67 | 258 | 2025-02-17 09:51 | 2026-04-29 11:15 | 44 | 34 | 10 | 37 | 37 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 14 |
| cherylg | 29 | 240 | 2025-02-19 14:41 | 2026-05-28 10:23 | 71 | 32 | 39 | 39 | 30 | 9 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 2 | 22 | 22 |
| jeanetterg | 19 | 222 | 2025-03-16 21:30 | 2025-09-18 15:46 | 37 | 21 | 16 | 39 | 30 | 9 | 33 | 33 | 0 | 0 | 3 | 0 | 3 | 0 | 13 | 12 | 2 | 0 | 0 | 0 | 0 | 12 | 7 |
| yurit | 5 | 214 | 2025-06-19 12:59 | 2025-10-25 07:58 | 16 | 3 | 13 | 60 | 60 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| bethk | 12 | 210 | 2025-02-20 17:50 | 2026-04-26 15:04 | 11 | 3 | 8 | 108 | 103 | 4 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 7 | 7 | 2 | 3 | 0 | 0 | 0 | 0 | 0 |
| judy | 21 | 202 | 2025-07-28 17:52 | 2026-06-08 20:29 | 61 | 22 | 39 | 52 | 49 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 10 | 0 | 0 | 0 | 0 | 3 | 17 |
| mikej | 23 | 195 | 2025-02-17 14:09 | 2026-04-09 15:05 | 99 | 1 | 98 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 31 | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jonv | 25 | 180 | 2024-11-25 17:52 | 2026-06-04 11:51 | 15 | 15 | 0 | 27 | 3 | 24 | 3 | 3 | 0 | 0 | 12 | 3 | 9 | 0 | 21 | 17 | 1 | 4 | 0 | 0 | 0 | 1 | 4 |
| danbrungardt | 34 | 173 | 2026-01-06 16:53 | 2026-06-15 14:20 | 53 | 18 | 35 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 5 | 0 | 0 | 0 | 0 | 10 | 3 |
| amandagreenfield | 7 | 169 | 2025-09-25 15:46 | 2026-02-03 11:35 | 18 | 6 | 12 | 48 | 41 | 7 | 0 | 0 | 0 | 0 | 3 | 0 | 3 | 0 | 25 | 25 | 0 | 8 | 0 | 0 | 0 | 5 | 0 |
| susan_h | 17 | 166 | 2026-04-29 18:16 | 2026-06-11 17:39 | 95 | 16 | 79 | 20 | 20 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 9 |
| amy@reimansco.com | 16 | 163 | 2026-04-29 18:36 | 2026-05-30 22:36 | 49 | 21 | 28 | 38 | 38 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 1 | 9 | 25 |
| kessler | 26 | 159 | 2025-02-18 19:30 | 2025-09-18 09:59 | 46 | 2 | 44 | 22 | 13 | 9 | 7 | 7 | 0 | 0 | 1 | 0 | 1 | 0 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 6 | 1 |
| bfrance | 42 | 159 | 2025-02-15 09:12 | 2025-12-10 13:19 | 29 | 8 | 21 | 25 | 25 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 2 | 5 |
| khare | 15 | 144 | 2025-02-19 14:20 | 2026-06-04 18:09 | 44 | 13 | 31 | 29 | 26 | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 2 | 0 | 1 | 1 | 4 | 10 |
| renwilmedia | 8 | 113 | 2025-02-12 11:16 | 2025-07-15 13:13 | 18 | 3 | 15 | 32 | 31 | 1 | 27 | 27 | 0 | 0 | 2 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 0 |
| tewing | 20 | 90 | 2025-01-15 16:31 | 2026-06-04 12:00 | 23 | 18 | 5 | 3 | 0 | 3 | 0 | 0 | 0 | 0 | 4 | 0 | 4 | 0 | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| toddtracy | 12 | 85 | 2025-05-14 09:32 | 2026-01-21 20:21 | 29 | 2 | 27 | 6 | 5 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 6 | 1 | 0 | 0 | 0 | 5 | 3 |
| cdufresne | 9 | 85 | 2025-09-25 13:32 | 2025-11-10 16:20 | 30 | 9 | 21 | 13 | 13 | 0 | 11 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 5 |
| swt | 12 | 75 | 2024-12-03 10:17 | 2025-06-17 19:11 | 5 | 5 | 0 | 14 | 2 | 12 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 7 | 5 | 0 | 6 | 0 | 1 | 0 | 3 | 0 |
| jerretjastal | 5 | 75 | 2026-04-27 08:46 | 2026-06-13 18:24 | 55 | 4 | 51 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 |
| hollyh | 5 | 56 | 2025-05-06 18:48 | 2026-02-09 11:46 | 43 | 3 | 40 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| cbenefield | 6 | 50 | 2026-02-11 13:04 | 2026-06-12 15:39 | 9 | 5 | 4 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 3 | 0 | 0 | 0 | 0 | 3 | 2 |
| kyla | 9 | 46 | 2025-09-26 10:26 | 2026-06-10 11:20 | 2 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 7 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| davidgonzalez | 5 | 38 | 2025-02-10 12:20 | 2025-09-23 21:53 | 17 | 3 | 14 | 3 | 3 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 2 |
| brentsanders | 7 | 30 | 2025-12-17 13:51 | 2026-06-09 10:49 | 9 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| finad | 2 | 18 | 2025-06-26 10:00 | 2025-08-21 16:32 | 8 | 1 | 7 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| chuck-user | 14 | 18 | 2024-12-05 16:02 | 2025-10-13 11:37 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pchambers | 5 | 12 | 2025-08-08 08:26 | 2025-10-29 11:28 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| smcivor1 | 2 | 10 | 2026-03-23 21:51 | 2026-03-27 09:18 | 0 | 0 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kjael | 2 | 4 | 2026-04-23 10:15 | 2026-04-25 10:28 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| yokot | 1 | 2 | 2025-06-18 13:22 | 2025-06-18 13:23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rickj | 1 | 2 | 2025-02-10 14:26 | 2025-02-10 14:26 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| des | 1 | 2 | 2025-04-03 16:01 | 2025-04-03 16:02 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cwiebe | 1 | 1 | 2025-10-03 14:32 | 2025-10-03 14:32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| brucew | 1 | 1 | 2026-01-16 11:03 | 2026-01-16 11:03 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Q-01_step2_results.md

# Q-01-S2 Results — RENWIL (rw, org_id=248)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 66
- **Run date**: 2026-06-16


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Sheryl Lowe | 613 | $1.3M | $2,083 | 157 |
| Louise Presseau | 1,154 | $1.0M | $890 | 110 |
| Paul deBellefeuille | 572 | $796,299 | $1,392 | 18 |
| Roxanne Toledo | 650 | $786,676 | $1,210 | 108 |
| Cindy Smethurst | 363 | $700,263 | $1,929 | 66 |
| Sandra Nash Braden | 1,088 | $658,909 | $606 | 51 |
| Penny Gould | 613 | $592,367 | $966 | 8 |
| Rob Trottier | 560 | $498,060 | $889 | 73 |
| Suzanne Hogan | 48 | $341,150 | $7,107 | 13 |
| Roxanna Page | 259 | $302,862 | $1,169 | 23 |
| Marc Gilbert | 222 | $287,186 | $1,294 | 39 |
| John Fraser | 150 | $265,232 | $1,768 | 26 |
| Sandy Gerlock | 165 | $250,071 | $1,516 | 44 |
| Jean Beaulieu | 87 | $228,045 | $2,621 | 19 |
| Neil Wasserman | 120 | $205,716 | $1,714 | 32 |
| Amy Reiman | 168 | $167,453 | $997 | 28 |
| Tanner Gould | 143 | $161,505 | $1,129 | 17 |
| Denise Fraley | 75 | $154,189 | $2,056 | 21 |
| Mandana Saxton | 93 | $151,119 | $1,625 | 22 |
| Ted Dufresne | 101 | $142,261 | $1,409 | 24 |
| Theresa Hackett | 78 | $137,440 | $1,762 | 16 |
| Tim Matchunis | 143 | $135,964 | $951 | 13 |
| Dan Ewing | 50 | $132,027 | $2,641 | 11 |
| Jesse Gerber | 104 | $130,786 | $1,258 | 28 |
| Samantha Murray | 180 | $126,991 | $706 | 24 |
| Ben Bonardelli | 42 | $82,890 | $1,974 | 16 |
| Tami  Gleason | 53 | $70,986 | $1,339 | 9 |
| Larry Gerber | 132 | $67,880 | $514 | 32 |
| Patty Jesse | 28 | $62,788 | $2,242 | 2 |
| Jimmilea King | 14 | $62,776 | $4,484 | 5 |
| The Walfab Company | 85 | $61,245 | $721 | 23 |
| Marie Andersen | 38 | $60,704 | $1,597 | 9 |
| Randy Gould | 57 | $54,834 | $962 | 8 |
| Wendy Buzzard | 11 | $52,664 | $4,788 | 1 |
| Brandon Kraese | 31 | $47,096 | $1,519 | 5 |
| Dennis Grant | 72 | $39,418 | $547 | 2 |
| Melissa Klinger | 44 | $38,027 | $864 | 18 |
| Haris Baig | 44 | $38,009 | $864 | 13 |
| Seth Neumann | 31 | $25,822 | $833 | 4 |
| Linda Cezar | 3 | $24,722 | $8,241 | 2 |
| Anna Cowan | 9 | $18,453 | $2,050 | 4 |
| Lori Funk | 26 | $16,068 | $618 | 9 |
| B Graham | 7 | $12,585 | $1,798 | 0 |
| Lance Bissell | 14 | $10,177 | $727 | 3 |
| Judy Embury | 18 | $9,689 | $538 | 1 |
| Jeannette Grude | 5 | $8,722 | $1,744 | 2 |
| Cheryl Gross | 17 | $8,136 | $479 | 5 |
| Bianca Sanz | 4 | $8,093 | $2,023 | 2 |
| Susan Hatch | 9 | $7,592 | $844 | 4 |
| Joshua Jastal | 13 | $6,648 | $511 | 7 |
| Katherine Hare | 10 | $5,966 | $597 | 3 |
| Christian Dufresne | 5 | $4,703 | $941 | 2 |
| Michael Estrin | 13 | $3,452 | $266 | 7 |
| Laurie Reinhardt | 4 | $3,448 | $862 | 1 |
| Carlos Bohorquez | 4 | $3,188 | $797 | 2 |
| B. Graham | 1 | $2,347 | $2,347 | 1 |
| Jerret Jastal | 3 | $1,915 | $638 | 0 |
| Bill France | 3 | $1,845 | $615 | 2 |
| Todd Tracy | 3 | $1,781 | $594 | 0 |
| Dan Brungardt | 3 | $1,728 | $576 | 2 |
| Kenneth and Linda Cezar | 2 | $1,277 | $638 | 1 |
| Carla Benefield | 2 | $1,181 | $590 | 1 |
| Chuck Wiebe | 5 | $1,155 | $231 | 1 |
| Fina Donoff | 1 | $424 | $424 | 0 |
| Test Sales Portal | 1 | $313 | $313 | 0 |
| David Gonzalez | 1 | $0 | $0 | 1 |

### Q-04_results.md

# Q-04 Results — RENWIL (rw, org_id=248)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 90
- **Run date**: 2026-06-16


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| louisep | 359 | 14,457 | 1,243 | 5,553 | 57 | 28 | 15 | 0 | 7 | 21 | Selling Rep |
| roxannet | 246 | 11,763 | 706 | 49 | 91 | 72 | 1 | 0 | 16 | 0 | Selling Rep |
| sandran | 339 | 11,482 | 1,307 | 4,177 | 180 | 8 | 3 | 0 | 9 | 25 | Selling Rep |
| denisef | 340 | 10,665 | 97 | 1,166 | 157 | 0 | 87 | 1 | 76 | 3 | Selling Rep |
| torontoshowroom | 338 | 10,540 | 811 | 3,017 | 60 | 39 | 5 | 0 | 5 | 11 | Selling Rep |
| smethurst | 205 | 8,659 | 375 | 3,022 | 4 | 0 | 0 | 0 | 6 | 0 | Selling Rep |
| robt | 293 | 8,278 | 616 | 2,823 | 159 | 17 | 56 | 0 | 1 | 74 | Selling Rep |
| pauld | 261 | 8,222 | 583 | 2,149 | 31 | 6 | 36 | 0 | 8 | 0 | Selling Rep |
| suzanneh | 142 | 6,072 | 55 | 1,177 | 34 | 0 | 120 | 1 | 33 | 36 | Selling Rep |
| pgould | 216 | 5,077 | 683 | 2,109 | 29 | 0 | 0 | 0 | 1 | 0 | Selling Rep |
| marcg | 176 | 4,141 | 223 | 287 | 6 | 0 | 27 | 0 | 12 | 20 | Selling Rep |
| neil513 | 304 | 3,909 | 146 | 1,275 | 68 | 2 | 0 | 0 | 4 | 4 | Selling Rep |
| roxannep | 231 | 3,688 | 262 | 1,266 | 309 | 90 | 10 | 0 | 10 | 27 | Selling Rep |
| jfraser | 228 | 3,539 | 179 | 1,460 | 26 | 8 | 60 | 0 | 18 | 17 | Selling Rep |
| jeanb | 150 | 3,366 | 104 | 236 | 19 | 2 | 19 | 0 | 29 | 9 | Selling Rep |
| sandyg | 162 | 3,061 | 165 | 1,101 | 95 | 7 | 3 | 0 | 15 | 6 | Selling Rep |
| areiman | 185 | 3,033 | 224 | 912 | 10 | 1 | 0 | 0 | 3 | 0 | Selling Rep |
| samantham | 187 | 2,754 | 189 | 962 | 88 | 4 | 57 | 3 | 10 | 78 | Selling Rep |
| rgould | 201 | 2,677 | 295 | 951 | 46 | 2 | 4 | 0 | 4 | 0 | Selling Rep |
| theresah | 172 | 2,585 | 84 | 736 | 79 | 12 | 21 | 0 | 5 | 28 | Selling Rep |
| tmatchunis | 161 | 2,538 | 162 | 727 | 38 | 3 | 1 | 0 | 31 | 0 | Selling Rep |
| jgerber | 239 | 2,436 | 149 | 369 | 4 | 1 | 0 | 0 | 0 | 15 | Selling Rep |
| mh-dewing | 153 | 2,334 | 53 | 686 | 51 | 7 | 39 | 0 | 38 | 38 | Selling Rep |
| tannerg | 206 | 2,331 | 163 | 802 | 29 | 0 | 6 | 0 | 0 | 1 | Selling Rep |
| marieandersen | 150 | 2,243 | 65 | 710 | 91 | 11 | 5 | 0 | 1 | 6 | Selling Rep |
| haris | 150 | 2,014 | 31 | 354 | 88 | 7 | 14 | 0 | 27 | 25 | Selling Rep |
| renwil | 122 | 1,943 | 35 | 307 | 68 | 0 | 11 | 1 | 48 | 53 | Selling Rep |
| lreinhardt | 43 | 1,918 | 4 | 935 | 15 | 1 | 1 | 0 | 7 | 31 | Selling Rep |
| pattyj | 90 | 1,812 | 30 | 377 | 115 | 0 | 10 | 0 | 18 | 32 | Selling Rep |
| mandanas | 123 | 1,803 | 110 | 628 | 63 | 2 | 0 | 0 | 12 | 0 | Selling Rep |
| tdufresne | 178 | 1,744 | 101 | 653 | 95 | 21 | 0 | 0 | 18 | 0 | Selling Rep |
| seth | 323 | 1,639 | 34 | 283 | 149 | 0 | 0 | 0 | 8 | 0 | Selling Rep |
| larryg | 90 | 1,571 | 107 | 206 | 0 | 0 | 0 | 0 | 6 | 0 | Selling Rep |
| dennisg | 101 | 1,564 | 74 | 253 | 13 | 0 | 39 | 0 | 14 | 22 | Selling Rep |
| melissak | 76 | 1,426 | 47 | 166 | 13 | 0 | 6 | 0 | 5 | 0 | Selling Rep |
| walfab_central | 83 | 1,176 | 84 | 332 | 0 | 0 | 0 | 0 | 1 | 3 | Selling Rep |
| wendybuzzard | 142 | 1,158 | 15 | 249 | 136 | 7 | 8 | 0 | 10 | 1 | Selling Rep |
| bgraham | 103 | 1,098 | 8 | 140 | 136 | 4 | 47 | 1 | 3 | 10 | Selling Rep |
| tamig708 | 128 | 932 | 62 | 266 | 8 | 3 | 0 | 0 | 0 | 1 | Selling Rep |
| brandonk | 103 | 923 | 31 | 233 | 51 | 19 | 0 | 0 | 4 | 6 | Selling Rep |
| annacowan | 92 | 815 | 14 | 178 | 11 | 0 | 2 | 0 | 0 | 0 | Selling Rep |
| bbonardelli | 50 | 808 | 42 | 258 | 0 | 0 | 1 | 0 | 7 | 0 | Selling Rep |
| jimmileak | 50 | 806 | 14 | 100 | 59 | 30 | 13 | 0 | 2 | 3 | Selling Rep |
| ljfunk | 71 | 643 | 29 | 76 | 2 | 2 | 0 | 0 | 2 | 0 | Selling Rep |
| cezar | 115 | 592 | 6 | 162 | 77 | 7 | 3 | 0 | 0 | 0 | Selling Rep |
| adriant | 28 | 513 | 4 | 88 | 6 | 0 | 9 | 0 | 3 | 1 | Selling Rep |
| carlac | 74 | 503 | 1 | 101 | 25 | 0 | 3 | 0 | 0 | 0 | Sales Support/Inside Sales |
| jjastal | 88 | 465 | 15 | 59 | 17 | 0 | 1 | 0 | 0 | 0 | Selling Rep |
| jonathan | 97 | 452 | 1 | 65 | 13 | 2 | 3 | 0 | 2 | 0 | Low-Activity User |
| carlosb | 51 | 436 | 4 | 63 | 33 | 1 | 0 | 0 | 3 | 1 | Selling Rep |
| dianecresante | 95 | 334 | 1 | 53 | 19 | 0 | 0 | 0 | 2 | 0 | Low-Activity User |
| lance | 95 | 324 | 15 | 67 | 7 | 2 | 0 | 0 | 7 | 3 | Selling Rep |
| carolynl | 60 | 314 | 0 | 164 | 4 | 1 | 0 | 0 | 4 | 0 | Low-Activity User |
| robertbonardelli | 40 | 294 | 0 | 3 | 53 | 1 | 3 | 0 | 0 | 0 | Low-Activity User |
| mestrin | 67 | 258 | 14 | 37 | 0 | 0 | 0 | 0 | 4 | 0 | Selling Rep |
| cherylg | 29 | 240 | 22 | 30 | 0 | 0 | 0 | 0 | 2 | 0 | Selling Rep |
| jeanetterg | 19 | 222 | 7 | 30 | 12 | 1 | 3 | 0 | 2 | 0 | Selling Rep |
| yurit | 5 | 214 | 0 | 60 | 0 | 0 | 2 | 0 | 2 | 0 | Inactive |
| bethk | 12 | 210 | 0 | 103 | 7 | 0 | 4 | 0 | 2 | 3 | Inactive |
| judy | 21 | 202 | 17 | 49 | 1 | 0 | 0 | 0 | 10 | 0 | Selling Rep |
| mikej | 23 | 195 | 0 | 18 | 30 | 1 | 0 | 0 | 0 | 0 | Inactive |
| jonv | 25 | 180 | 4 | 3 | 17 | 4 | 9 | 0 | 1 | 4 | Selling Rep |
| danbrungardt | 34 | 173 | 3 | 16 | 6 | 0 | 0 | 0 | 5 | 0 | Selling Rep |
| amandagreenfield | 7 | 169 | 0 | 41 | 25 | 0 | 3 | 0 | 0 | 8 | Inactive |
| susan_h | 17 | 166 | 9 | 20 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| amy@reimansco.com | 16 | 163 | 25 | 38 | 3 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| bfrance | 42 | 159 | 5 | 25 | 5 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| kessler | 26 | 159 | 1 | 13 | 11 | 0 | 1 | 0 | 0 | 0 | Inactive |
| khare | 15 | 144 | 10 | 26 | 3 | 1 | 0 | 0 | 0 | 3 | Selling Rep |
| renwilmedia | 8 | 113 | 0 | 31 | 0 | 0 | 2 | 0 | 0 | 0 | Inactive |
| tewing | 20 | 90 | 0 | 0 | 2 | 0 | 4 | 0 | 2 | 0 | Inactive |
| toddtracy | 12 | 85 | 3 | 5 | 1 | 0 | 0 | 0 | 6 | 1 | Selling Rep |
| cdufresne | 9 | 85 | 5 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| jerretjastal | 5 | 75 | 3 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| swt | 12 | 75 | 0 | 2 | 5 | 2 | 0 | 0 | 0 | 7 | Inactive |
| hollyh | 5 | 56 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| cbenefield | 6 | 50 | 2 | 6 | 3 | 0 | 0 | 0 | 3 | 0 | Inactive |
| kyla | 9 | 46 | 0 | 1 | 7 | 5 | 0 | 0 | 3 | 0 | Inactive |
| davidgonzalez | 5 | 38 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 7 | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 14 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| finad | 2 | 18 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pchambers | 5 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| smcivor1 | 2 | 10 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kjael | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| rickj | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| yokot | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| des | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| cwiebe | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brucew | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — RENWIL (rw, org_id=248)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 83 | 65 | 50 |

### Q-06_results.md

# Q-06 Results — RENWIL (rw, org_id=248)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 72
- **Run date**: 2026-06-16


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Louise Presseau | 139 | 133 | -4.30 | 249 | 341 | 36.90 | $297,812 |
| Sandra Nash Braden | 105 | 98 | -6.70 | 241 | 313 | 29.90 | $177,975 |
| Roxanne Toledo | 71 | 98 | 38 | 138 | 179 | 29.70 | $248,648 |
| Rob Trottier | 145 | 131 | -9.70 | 138 | 173 | 25.40 | $135,688 |
| Sheryl Lowe | 81 | 77 | -4.90 | 122 | 165 | 35.20 | $336,069 |
| Penny Gould | 62 | 65 | 4.80 | 151 | 158 | 4.60 | $154,270 |
| Paul deBellefeuille | 95 | 102 | 7.40 | 161 | 136 | -15.50 | $158,731 |
| Cindy Smethurst | 68 | 58 | -14.70 | 99 | 98 | -1 | $132,962 |
| Marc Gilbert | 79 | 78 | -1.30 | 46 | 65 | 41.30 | $100,044 |
| Roxanna Page | 60 | 60 | 0 | 70 | 61 | -12.90 | $51,969 |
| Sandy Gerlock | 37 | 50 | 35.10 | 30 | 44 | 46.70 | $63,280 |
| Samantha Murray | 37 | 47 | 27 | 36 | 43 | 19.40 | $28,806 |
| Tim Matchunis | 46 | 38 | -17.40 | 54 | 40 | -25.90 | $35,220 |
| Amy Reiman | 64 | 77 | 20.30 | 38 | 37 | -2.60 | $38,998 |
| Neil Wasserman | 71 | 121 | 70.40 | 26 | 36 | 38.50 | $67,595 |
| Tanner Gould | 48 | 34 | -29.20 | 26 | 36 | 38.50 | $44,518 |
| John Fraser | 55 | 59 | 7.30 | 36 | 35 | -2.80 | $62,133 |
| Dennis Grant | 13 | 52 | 300 | 4 | 34 | 750 | $24,657 |
| Larry Gerber | 0 | 41 | — | 0 | 33 | — | $19,650 |
| Jesse Gerber | 56 | 21 | -62.50 | 48 | 32 | -33.30 | $21,494 |
| The Walfab Company | 45 | 42 | -6.70 | 40 | 27 | -32.50 | $21,359 |
| Ted Dufresne | 52 | 64 | 23.10 | 27 | 24 | -11.10 | $39,280 |
| Theresa Hackett | 40 | 44 | 10 | 18 | 23 | 27.80 | $32,808 |
| Denise Fraley | 118 | 123 | 4.20 | 15 | 21 | 40 | $58,753 |
| Mandana Saxton | 49 | 25 | -49 | 29 | 21 | -27.60 | $35,901 |
| Randy Gould | 32 | 33 | 3.10 | 14 | 20 | 42.90 | $24,456 |
| Jean Beaulieu | 36 | 28 | -22.20 | 28 | 18 | -35.70 | $37,404 |
| Judy Embury | 1 | 23 | 2,200 | 0 | 17 | — | $9,365 |
| Tami  Gleason | 25 | 28 | 12 | 17 | 14 | -17.60 | $33,130 |
| Dan Ewing | 52 | 50 | -3.80 | 13 | 10 | -23.10 | $37,565 |
| Susan Hatch | 0 | 15 | — | 0 | 9 | — | $7,592 |
| Ben Bonardelli | 9 | 12 | 33.30 | 7 | 8 | 14.30 | $17,000 |
| Suzanne Hogan | 43 | 44 | 2.30 | 2 | 8 | 300 | $36,448 |
| Haris Baig | 120 | 68 | -43.30 | 10 | 7 | -30 | $1,741 |
| Haris Baig | 19 | 0 | -100 | 10 | 7 | -30 | $1,741 |
| Lori Funk | 9 | 10 | 11.10 | 3 | 7 | 133.30 | $2,705 |
| Marie Andersen | 41 | 36 | -12.20 | 7 | 6 | -14.30 | $9,939 |
| Lance Bissell | 15 | 21 | 40 | 1 | 5 | 400 | $2,347 |
| B Graham | 32 | 36 | 12.50 | 2 | 5 | 150 | $8,637 |
| Joshua Jastal | 13 | 17 | 30.80 | 2 | 4 | 100 | $2,603 |
| Seth Neumann | 115 | 101 | -12.20 | 12 | 4 | -66.70 | $1,386 |
| Patty Jesse | 50 | 19 | -62 | 4 | 4 | 0 | $9,631 |
| Bianca Sanz | 0 | 25 | — | 0 | 4 | — | $8,093 |
| Cheryl Gross | 5 | 9 | 80 | 3 | 4 | 33.30 | $1,965 |
| Wendy Buzzard | 24 | 29 | 20.80 | 1 | 3 | 200 | $16,992 |
| Jerret Jastal | 0 | 5 | — | 0 | 3 | — | $1,915 |
| Jimmilea King | 20 | 5 | -75 | 5 | 3 | -40 | $2,612 |
| Linda Cezar | 0 | 28 | — | 0 | 3 | — | $24,722 |
| Katherine Hare | 5 | 2 | -60 | 3 | 2 | -33.30 | $1,107 |
| Carla Benefield | 5 | 4 | -20 | 0 | 2 | — | $1,181 |
| Dan Brungardt | 29 | 13 | -55.20 | 2 | 1 | -50 | $808 |
| Laurie Reinhardt | 31 | 4 | -87.10 | 2 | 1 | -50 | $424 |
| Kenneth and Linda Cezar | 17 | 2 | -88.20 | 2 | 0 | -100 | $0 |
| Brandon Kraese | 16 | 12 | -25 | 4 | 0 | -100 | $0 |
| Michael Estrin | 14 | 5 | -64.30 | 2 | 0 | -100 | $0 |
| Todd Tracy | 3 | 0 | -100 | — | — | — | — |
| Kyla Bosch | 15 | 2 | -86.70 | — | — | — | — |
| Beth Keller | 0 | 4 | — | — | — | — | — |
| Carlos Bohorquez | 4 | 6 | 50 | — | — | — | — |
| Amanda Greenfield | 4 | 0 | -100 | — | — | — | — |
| SHARI MCIVOR | 0 | 2 | — | — | — | — | — |
| Brent Sanders | 5 | 5 | 0 | — | — | — | — |
| Kjael Skaalerud | 0 | 3 | — | — | — | — | — |
| Jon Vanderberg | 0 | 2 | — | — | — | — | — |
| Mike Jeffcoat | 4 | 2 | -50 | — | — | — | — |
| Andrian Trejo | 0 | 10 | — | — | — | — | — |
| Carloyn Lewis | 7 | 17 | 142.90 | — | — | — | — |
| Diane Cresante | 16 | 9 | -43.80 | — | — | — | — |
| Terry Ewing | 6 | 1 | -83.30 | — | — | — | — |
| Carla Cooper | 8 | 18 | 125 | — | — | — | — |
| Holly Harrington | 2 | 0 | -100 | — | — | — | — |
| Jonathan Wilner | 7 | 3 | -57.10 | — | — | — | — |

### Q-43_step2_results.md

# Q-43-S2 Results — RENWIL (rw, org_id=248)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16
- **Total flagged**: 1
- **Aggregate GMV**: $313

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |
| Test Sales Portal | 1 | $313 | keyword | confirmed_operational |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### Q-51_results.md

(not present — file does not exist or is empty)

### Q-62_results.md

(not present — file does not exist or is empty)

### Q-63_results.md

# Q-63 Results — RENWIL (rw, org_id=248)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| louisep | 59 | 1,142 | 317 | 537.30 | 27.80 | 1,141 | 0 | 1 |
| sandran | 22 | 738 | 308 | 1,400 | 41.70 | 738 | 0 | 0 |
| pauld | 9 | 553 | 133 | 1,477.80 | 24.10 | 537 | 16 | 0 |
| smethurst | 22 | 543 | 84 | 381.80 | 15.50 | 543 | 0 | 0 |
| torontoshowroom | 51 | 468 | 116 | 227.50 | 24.80 | 468 | 0 | 0 |
| robt | 33 | 455 | 158 | 478.80 | 34.70 | 455 | 0 | 0 |
| pgould | 2 | 427 | 152 | 7,600 | 35.60 | 427 | 0 | 0 |
| denisef | 22 | 380 | 10 | 45.50 | 2.60 | 371 | 9 | 0 |
| neil513 | 18 | 260 | 32 | 177.80 | 12.30 | 260 | 0 | 0 |
| sandyg | 18 | 226 | 38 | 211.10 | 16.80 | 226 | 0 | 0 |
| jfraser | 12 | 210 | 28 | 233.30 | 13.30 | 207 | 3 | 0 |
| roxannep | 9 | 200 | 52 | 577.80 | 26 | 200 | 0 | 0 |
| tmatchunis | 8 | 161 | 37 | 462.50 | 23 | 160 | 1 | 0 |
| jgerber | 11 | 155 | 43 | 390.90 | 27.70 | 155 | 0 | 0 |
| areiman | 12 | 155 | 27 | 225 | 17.40 | 155 | 0 | 0 |
| tdufresne | 12 | 140 | 19 | 158.30 | 13.60 | 140 | 0 | 0 |
| walfab_central | 10 | 136 | 21 | 210 | 15.40 | 136 | 0 | 0 |
| tannerg | 8 | 133 | 32 | 400 | 24.10 | 133 | 0 | 0 |
| suzanneh | 9 | 117 | 1 | 11.10 | 0.90 | 94 | 19 | 4 |
| samantham | 10 | 116 | 41 | 410 | 35.30 | 115 | 1 | 0 |

### Q-64_results.md

(not present — file does not exist or is empty)

### Q-65_results.md

# Q-65 Results — RENWIL (rw, org_id=248)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| smethurst | 1,431 | 1,312 | 119 | 91.70 | 8.30 |
| louisep | 2,877 | 2,634 | 243 | 91.60 | 8.40 |
| pgould | 874 | 782 | 92 | 89.50 | 10.50 |
| pauld | 1,791 | 1,601 | 190 | 89.40 | 10.60 |
| robt | 1,620 | 1,418 | 202 | 87.50 | 12.50 |
| jgerber | 927 | 809 | 118 | 87.30 | 12.70 |
| sandran | 1,973 | 1,701 | 272 | 86.20 | 13.80 |
| roxannet | 2,455 | 2,094 | 361 | 85.30 | 14.70 |
| jerretjastal | 75 | 64 | 11 | 85.30 | 14.70 |
| torontoshowroom | 1,622 | 1,376 | 246 | 84.80 | 15.20 |
| tmatchunis | 609 | 504 | 105 | 82.80 | 17.20 |
| ljfunk | 90 | 74 | 16 | 82.20 | 17.80 |
| bbonardelli | 123 | 100 | 23 | 81.30 | 18.70 |
| tannerg | 327 | 266 | 61 | 81.30 | 18.70 |
| mandanas | 195 | 157 | 38 | 80.50 | 19.50 |
| walfab_central | 448 | 358 | 90 | 79.90 | 20.10 |
| suzanneh | 1,104 | 877 | 227 | 79.40 | 20.60 |
| areiman | 449 | 355 | 94 | 79.10 | 20.90 |
| marcg | 720 | 567 | 153 | 78.80 | 21.30 |
| susan_h | 166 | 128 | 38 | 77.10 | 22.90 |

### Q-70_results.md

(not present — file does not exist or is empty)

### user_group_mapping.md

# User Group Mapping — RENWIL (rw, org_id=248)
- **Run date**: 2026-06-16
- **Total Postgres users**: 103
- **Matched to Mixpanel (Q-01 Step 1)**: 84 of 90 (93%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Reps USA | field_rep | 58 |
| Reps Canada | field_rep | 14 |
| Renwil Internal | admin_internal | 12 |
| z-SuperCat | admin_internal | 6 |
| Reps Quebec | field_rep | 4 |
| 1-Default eOL User Group | admin_internal | 3 |
| Admin Group | admin_internal | 2 |
| Ferguson | other | 1 |
| Reps US/CAN | field_rep | 1 |
| Reps US/CAN | admin_internal | 1 |
| eOL Public Site | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 70 | 158,233 | 92.7% |
| admin_internal | 13 | 10,933 | 6.4% |
| other | 1 | 1,564 | 0.9% |
