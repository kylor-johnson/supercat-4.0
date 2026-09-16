# Section 2 Context Bundle — Hubbardton Forge (hfg)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | True | has_clicky_portal=True |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=22104, portal_order_gmv=$42.2M |
| HAS_INVENTORY | False | inventory_count=0 |
| HAS_SALES_DATA | True | sales_data_count=44934 |
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
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 1871, Mixpanel total submit_order (Q-01): 3113 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=86.1%, ambiguous_rate=88.1%, showroom_event_share=3.5% |
| USER_GROUP_JOIN_RATE | 86% | 118 of 137 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 3% | showroom+admin share of matched events: 3.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 2 admin/showroom users in leaderboard: Shannon Rose, Retha Boles |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=47 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=2590 |
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
- **Run date**: 2026-06-16

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

# Q-01-S1 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 137
- **Run date**: 2026-06-16


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bkrieger | 448 | 15,923 | 2024-12-10 14:35 | 2026-06-15 21:30 | 6,182 | 1,455 | 4,727 | 2,072 | 2,028 | 31 | 1,133 | 1,133 | 0 | 0 | 45 | 11 | 34 | 0 | 1,147 | 1,115 | 689 | 22 | 0 | 0 | 48 | 104 | 30 |
| jgannon | 525 | 12,712 | 2024-11-01 07:05 | 2026-06-15 12:36 | 2,483 | 834 | 1,649 | 2,420 | 2,396 | 18 | 982 | 982 | 0 | 0 | 14 | 10 | 3 | 1 | 2,909 | 2,893 | 1,006 | 18 | 0 | 0 | 68 | 184 | 179 |
| mgoffice | 362 | 12,679 | 2024-11-01 09:52 | 2026-06-15 17:02 | 6,516 | 1,712 | 4,804 | 2,198 | 2,197 | 1 | 1,438 | 1,438 | 0 | 0 | 0 | 0 | 0 | 0 | 93 | 93 | 74 | 0 | 0 | 0 | 4 | 755 | 8 |
| steven | 408 | 11,920 | 2024-11-01 09:21 | 2026-06-15 17:26 | 5,115 | 911 | 4,204 | 1,527 | 1,345 | 2 | 123 | 123 | 0 | 0 | 10 | 2 | 7 | 1 | 2,350 | 2,339 | 164 | 8 | 0 | 0 | 14 | 22 | 0 |
| dunnlighting | 425 | 9,558 | 2024-11-01 13:53 | 2026-06-15 15:39 | 2,757 | 958 | 1,799 | 1,514 | 1,348 | 0 | 965 | 965 | 0 | 0 | 24 | 1 | 23 | 0 | 1,414 | 1,383 | 244 | 17 | 0 | 0 | 15 | 45 | 120 |
| amymatteson | 432 | 7,855 | 2024-11-01 10:11 | 2026-06-15 18:48 | 3,385 | 1,023 | 2,362 | 1,407 | 1,402 | 5 | 811 | 811 | 0 | 0 | 5 | 0 | 5 | 0 | 470 | 456 | 4 | 0 | 0 | 0 | 0 | 10 | 50 |
| rgould | 473 | 6,999 | 2024-11-01 13:08 | 2026-06-15 19:52 | 1,720 | 715 | 1,005 | 1,299 | 1,296 | 3 | 672 | 672 | 0 | 0 | 76 | 34 | 42 | 0 | 1,098 | 1,034 | 95 | 3 | 0 | 0 | 37 | 118 | 77 |
| wguthrie | 304 | 5,857 | 2024-11-01 09:31 | 2026-06-15 16:19 | 2,929 | 597 | 2,332 | 1,013 | 1,011 | 2 | 750 | 750 | 0 | 0 | 0 | 0 | 0 | 0 | 133 | 111 | 2 | 0 | 0 | 0 | 0 | 64 | 525 |
| kgannon | 396 | 4,576 | 2024-11-02 13:19 | 2026-06-15 09:12 | 683 | 311 | 372 | 919 | 916 | 3 | 550 | 550 | 0 | 0 | 18 | 18 | 0 | 0 | 714 | 670 | 460 | 15 | 0 | 0 | 2 | 16 | 90 |
| gduguid | 254 | 3,946 | 2024-11-04 14:32 | 2026-06-11 20:00 | 1,428 | 350 | 1,078 | 777 | 765 | 1 | 614 | 614 | 0 | 0 | 2 | 0 | 2 | 0 | 285 | 285 | 9 | 0 | 0 | 0 | 17 | 35 | 23 |
| sherrij | 308 | 3,741 | 2024-11-01 13:20 | 2026-06-09 12:45 | 1,430 | 438 | 992 | 654 | 654 | 0 | 436 | 436 | 0 | 0 | 1 | 1 | 0 | 0 | 36 | 34 | 1 | 0 | 0 | 0 | 2 | 83 | 306 |
| kclegg | 314 | 3,551 | 2024-11-01 08:22 | 2026-06-12 11:07 | 498 | 283 | 215 | 550 | 533 | 11 | 316 | 316 | 0 | 0 | 0 | 0 | 0 | 0 | 774 | 721 | 191 | 1 | 0 | 0 | 1 | 7 | 217 |
| tannerg | 306 | 3,511 | 2024-11-01 14:28 | 2026-06-15 18:05 | 937 | 324 | 613 | 928 | 914 | 14 | 500 | 500 | 0 | 0 | 22 | 6 | 15 | 0 | 131 | 129 | 69 | 6 | 0 | 0 | 15 | 14 | 72 |
| robantonecchia | 286 | 3,458 | 2024-11-04 07:25 | 2026-06-15 09:34 | 683 | 255 | 428 | 645 | 620 | 7 | 394 | 394 | 0 | 0 | 27 | 0 | 26 | 0 | 758 | 755 | 70 | 4 | 0 | 0 | 5 | 17 | 1 |
| tminutelli | 253 | 3,387 | 2024-11-01 12:54 | 2026-06-15 17:54 | 1,488 | 502 | 986 | 408 | 405 | 1 | 322 | 322 | 0 | 0 | 3 | 0 | 3 | 0 | 11 | 11 | 1 | 0 | 0 | 0 | 0 | 16 | 382 |
| lbelesky | 279 | 3,367 | 2025-02-05 17:17 | 2026-06-15 13:04 | 824 | 232 | 592 | 620 | 456 | 3 | 389 | 389 | 0 | 0 | 15 | 4 | 11 | 0 | 345 | 324 | 199 | 4 | 0 | 0 | 14 | 36 | 87 |
| jenmccarty | 220 | 3,219 | 2025-06-13 16:19 | 2026-06-15 14:35 | 159 | 149 | 10 | 416 | 413 | 2 | 210 | 210 | 0 | 0 | 88 | 2 | 74 | 6 | 827 | 808 | 275 | 138 | 0 | 7 | 12 | 41 | 17 |
| lynnr1 | 201 | 3,195 | 2024-11-02 15:02 | 2026-06-11 16:33 | 1,305 | 383 | 922 | 493 | 493 | 0 | 440 | 440 | 0 | 0 | 0 | 0 | 0 | 0 | 10 | 9 | 0 | 0 | 0 | 0 | 0 | 48 | 319 |
| codyadler | 270 | 3,155 | 2024-11-01 12:12 | 2026-06-12 13:03 | 450 | 112 | 338 | 532 | 526 | 3 | 14 | 14 | 0 | 0 | 32 | 1 | 31 | 0 | 1,178 | 1,154 | 19 | 51 | 0 | 0 | 4 | 4 | 0 |
| gschwartz1 | 150 | 2,968 | 2024-12-10 14:40 | 2025-07-22 17:59 | 778 | 199 | 579 | 466 | 422 | 15 | 149 | 149 | 0 | 0 | 31 | 5 | 20 | 4 | 428 | 402 | 135 | 38 | 0 | 2 | 34 | 50 | 6 |
| jfs | 288 | 2,708 | 2024-11-05 10:47 | 2026-06-12 15:52 | 860 | 139 | 721 | 532 | 524 | 3 | 71 | 71 | 0 | 0 | 5 | 0 | 5 | 0 | 426 | 421 | 4 | 4 | 0 | 0 | 1 | 7 | 4 |
| jimhickey | 326 | 2,704 | 2024-11-06 07:54 | 2026-06-15 09:11 | 345 | 211 | 134 | 221 | 221 | 0 | 148 | 148 | 0 | 0 | 0 | 0 | 0 | 0 | 778 | 676 | 315 | 0 | 0 | 0 | 3 | 15 | 9 |
| aknapp | 169 | 2,594 | 2024-11-06 16:26 | 2026-05-18 09:10 | 274 | 56 | 218 | 333 | 254 | 52 | 112 | 112 | 0 | 0 | 62 | 4 | 56 | 0 | 1,036 | 1,033 | 22 | 45 | 0 | 0 | 45 | 32 | 0 |
| broche | 231 | 2,587 | 2024-11-06 11:07 | 2026-06-14 14:08 | 261 | 256 | 5 | 637 | 634 | 3 | 544 | 544 | 0 | 0 | 23 | 0 | 23 | 0 | 496 | 468 | 11 | 0 | 0 | 0 | 9 | 15 | 3 |
| etibbetts | 168 | 2,408 | 2024-11-01 13:06 | 2026-06-03 11:20 | 435 | 139 | 296 | 293 | 271 | 11 | 133 | 133 | 0 | 0 | 25 | 2 | 23 | 0 | 762 | 753 | 53 | 23 | 0 | 0 | 9 | 27 | 0 |
| mberesford | 196 | 2,270 | 2024-11-01 09:16 | 2025-11-12 12:12 | 788 | 139 | 649 | 313 | 310 | 1 | 56 | 56 | 0 | 0 | 3 | 3 | 0 | 0 | 497 | 481 | 66 | 0 | 0 | 0 | 5 | 15 | 6 |
| jreibel | 502 | 2,182 | 2024-11-01 09:40 | 2026-06-15 15:44 | 453 | 116 | 337 | 457 | 450 | 0 | 97 | 97 | 0 | 0 | 21 | 19 | 2 | 0 | 86 | 72 | 107 | 1 | 0 | 0 | 0 | 0 | 1 |
| dpritchard | 319 | 2,179 | 2024-11-04 13:06 | 2026-06-11 08:38 | 578 | 100 | 478 | 284 | 281 | 1 | 79 | 79 | 0 | 0 | 7 | 5 | 2 | 0 | 200 | 178 | 213 | 3 | 0 | 0 | 1 | 3 | 0 |
| jchon | 200 | 2,134 | 2024-11-01 18:14 | 2026-02-11 15:25 | 1,022 | 260 | 762 | 306 | 305 | 0 | 216 | 216 | 0 | 0 | 0 | 0 | 0 | 0 | 45 | 45 | 1 | 3 | 0 | 0 | 1 | 50 | 5 |
| tstauffacher | 195 | 2,045 | 2024-11-01 15:47 | 2026-06-12 13:45 | 271 | 155 | 116 | 334 | 322 | 9 | 216 | 216 | 0 | 0 | 8 | 4 | 4 | 0 | 602 | 570 | 78 | 10 | 0 | 0 | 3 | 7 | 9 |
| apoindexter | 300 | 2,038 | 2024-11-01 14:38 | 2026-06-15 15:44 | 530 | 145 | 385 | 375 | 372 | 3 | 124 | 124 | 0 | 0 | 63 | 59 | 4 | 0 | 142 | 138 | 61 | 2 | 0 | 0 | 9 | 24 | 4 |
| amcguire | 179 | 1,822 | 2024-11-01 09:58 | 2026-06-15 14:18 | 180 | 38 | 142 | 235 | 234 | 0 | 62 | 62 | 0 | 0 | 19 | 0 | 19 | 0 | 733 | 725 | 7 | 0 | 0 | 0 | 5 | 5 | 1 |
| kimartin | 162 | 1,638 | 2024-11-12 09:58 | 2025-12-26 15:40 | 301 | 91 | 210 | 258 | 256 | 1 | 230 | 230 | 0 | 0 | 12 | 0 | 12 | 0 | 389 | 382 | 0 | 2 | 0 | 0 | 0 | 0 | 14 |
| kgrillo | 155 | 1,630 | 2024-11-01 13:24 | 2026-06-07 17:32 | 236 | 82 | 154 | 227 | 219 | 1 | 86 | 86 | 0 | 0 | 34 | 1 | 33 | 0 | 559 | 557 | 2 | 51 | 0 | 0 | 0 | 6 | 0 |
| starrylightssupport | 126 | 1,613 | 2024-11-04 11:27 | 2025-06-26 13:02 | 322 | 99 | 223 | 477 | 462 | 0 | 160 | 160 | 0 | 0 | 17 | 2 | 15 | 0 | 229 | 228 | 3 | 5 | 0 | 0 | 0 | 3 | 1 |
| ctwigg | 168 | 1,593 | 2024-11-01 12:59 | 2026-06-12 10:42 | 270 | 250 | 20 | 357 | 357 | 0 | 304 | 304 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 3 | 0 | 0 | 0 | 0 | 1 | 65 | 205 |
| lross | 137 | 1,567 | 2024-11-01 12:19 | 2026-06-11 12:02 | 527 | 187 | 340 | 281 | 280 | 1 | 243 | 243 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 11 | 2 | 0 | 0 | 0 | 0 | 30 | 171 |
| smicheal | 152 | 1,537 | 2024-11-07 11:34 | 2026-06-15 15:23 | 688 | 139 | 549 | 298 | 298 | 0 | 204 | 204 | 0 | 0 | 0 | 0 | 0 | 0 | 26 | 26 | 0 | 0 | 0 | 0 | 2 | 6 | 3 |
| jeffizower | 116 | 1,479 | 2024-11-01 09:46 | 2026-06-10 14:28 | 302 | 67 | 235 | 216 | 212 | 4 | 161 | 161 | 0 | 0 | 17 | 0 | 17 | 0 | 466 | 465 | 18 | 12 | 0 | 3 | 2 | 5 | 6 |
| pgould | 85 | 1,433 | 2024-12-09 16:32 | 2026-05-18 13:08 | 195 | 54 | 141 | 162 | 162 | 0 | 84 | 84 | 0 | 0 | 8 | 8 | 0 | 0 | 742 | 741 | 3 | 6 | 0 | 0 | 8 | 6 | 17 |
| lightingrep | 90 | 1,424 | 2024-11-04 10:24 | 2026-03-04 20:53 | 234 | 83 | 151 | 353 | 353 | 0 | 195 | 195 | 0 | 0 | 28 | 11 | 16 | 0 | 55 | 48 | 0 | 56 | 0 | 0 | 0 | 183 | 0 |
| vingato | 199 | 1,400 | 2024-11-01 09:25 | 2026-06-12 10:10 | 229 | 229 | 0 | 324 | 311 | 2 | 342 | 342 | 0 | 0 | 1 | 1 | 0 | 0 | 31 | 30 | 6 | 0 | 0 | 0 | 0 | 5 | 14 |
| astauffacher | 77 | 1,347 | 2024-12-30 16:17 | 2026-06-15 10:46 | 73 | 43 | 30 | 124 | 124 | 0 | 74 | 74 | 0 | 0 | 0 | 0 | 0 | 0 | 884 | 872 | 28 | 0 | 0 | 0 | 0 | 0 | 3 |
| jessicam | 120 | 1,189 | 2024-11-01 13:56 | 2026-06-15 10:13 | 372 | 103 | 269 | 138 | 134 | 0 | 114 | 114 | 0 | 0 | 2 | 0 | 2 | 0 | 266 | 265 | 3 | 3 | 0 | 0 | 0 | 2 | 7 |
| sschwartz1 | 93 | 1,143 | 2024-11-01 14:13 | 2026-04-01 17:59 | 196 | 57 | 139 | 153 | 144 | 9 | 185 | 185 | 0 | 0 | 6 | 0 | 6 | 0 | 375 | 336 | 8 | 0 | 0 | 0 | 0 | 0 | 2 |
| ccoxworth | 151 | 1,137 | 2024-11-05 13:41 | 2026-06-15 12:46 | 89 | 59 | 30 | 215 | 215 | 0 | 0 | 0 | 0 | 0 | 4 | 4 | 0 | 0 | 475 | 459 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| grillocs | 335 | 1,032 | 2024-11-01 08:57 | 2026-06-15 09:08 | 232 | 87 | 145 | 132 | 132 | 0 | 78 | 78 | 0 | 0 | 1 | 0 | 1 | 0 | 43 | 43 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| tripm | 78 | 1,016 | 2024-11-17 10:41 | 2026-05-29 10:21 | 305 | 66 | 239 | 161 | 159 | 1 | 188 | 188 | 0 | 0 | 14 | 2 | 10 | 0 | 94 | 93 | 2 | 3 | 0 | 0 | 0 | 1 | 5 |
| bpeel | 223 | 949 | 2024-11-04 11:36 | 2026-06-10 11:07 | 171 | 165 | 6 | 167 | 167 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 24 | 24 | 147 | 0 | 0 | 0 | 1 | 0 | 0 |
| nstory | 54 | 937 | 2024-11-06 18:20 | 2025-05-28 18:17 | 183 | 34 | 149 | 85 | 85 | 0 | 61 | 61 | 0 | 0 | 0 | 0 | 0 | 0 | 458 | 455 | 12 | 0 | 0 | 0 | 0 | 8 | 0 |
| lightingvision | 38 | 838 | 2024-11-06 22:59 | 2026-02-13 11:18 | 28 | 28 | 0 | 76 | 76 | 0 | 145 | 145 | 0 | 0 | 0 | 0 | 0 | 0 | 417 | 413 | 3 | 0 | 0 | 0 | 0 | 1 | 3 |
| dougg | 59 | 817 | 2024-12-08 15:05 | 2026-06-04 14:40 | 169 | 53 | 116 | 109 | 96 | 9 | 203 | 203 | 0 | 0 | 6 | 0 | 6 | 0 | 112 | 109 | 0 | 0 | 0 | 0 | 2 | 9 | 9 |
| rocher | 71 | 811 | 2024-11-11 09:36 | 2026-04-25 09:18 | 47 | 25 | 22 | 102 | 102 | 0 | 28 | 28 | 0 | 0 | 1 | 0 | 1 | 0 | 436 | 422 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| williamsl | 159 | 800 | 2024-11-11 10:11 | 2026-06-12 14:18 | 186 | 161 | 25 | 190 | 187 | 0 | 25 | 25 | 0 | 0 | 2 | 1 | 1 | 0 | 55 | 47 | 16 | 0 | 0 | 0 | 0 | 0 | 5 |
| kaceywilliams | 64 | 796 | 2024-11-07 12:35 | 2026-06-15 16:47 | 74 | 33 | 41 | 207 | 207 | 0 | 45 | 45 | 0 | 0 | 1 | 0 | 1 | 0 | 253 | 252 | 22 | 4 | 0 | 0 | 8 | 3 | 0 |
| lmalchus | 62 | 787 | 2024-11-04 11:09 | 2025-11-21 11:49 | 149 | 54 | 95 | 114 | 111 | 1 | 19 | 19 | 0 | 0 | 14 | 4 | 9 | 1 | 287 | 287 | 2 | 15 | 0 | 0 | 0 | 3 | 0 |
| todd_m | 59 | 715 | 2024-11-01 10:27 | 2026-06-11 13:54 | 22 | 10 | 12 | 30 | 29 | 1 | 10 | 10 | 0 | 0 | 1 | 0 | 1 | 0 | 500 | 497 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| dsouthwickdrew | 63 | 712 | 2024-11-15 09:38 | 2026-04-27 14:02 | 49 | 11 | 38 | 37 | 35 | 2 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 396 | 396 | 9 | 1 | 0 | 0 | 7 | 12 | 2 |
| nickc | 212 | 707 | 2024-11-06 14:13 | 2026-06-15 14:50 | 19 | 19 | 0 | 95 | 93 | 2 | 11 | 11 | 0 | 0 | 5 | 0 | 5 | 0 | 103 | 101 | 34 | 1 | 0 | 0 | 0 | 3 | 0 |
| czaya | 72 | 683 | 2024-11-03 18:30 | 2025-04-01 18:56 | 132 | 132 | 0 | 99 | 99 | 0 | 58 | 58 | 0 | 0 | 0 | 0 | 0 | 0 | 159 | 159 | 0 | 0 | 0 | 0 | 0 | 0 | 16 |
| rhailpern | 89 | 674 | 2024-11-05 17:02 | 2026-05-18 16:24 | 49 | 47 | 2 | 106 | 106 | 0 | 52 | 52 | 0 | 0 | 0 | 0 | 0 | 0 | 246 | 214 | 1 | 0 | 0 | 0 | 1 | 14 | 2 |
| agautzsch | 19 | 643 | 2024-11-07 22:27 | 2026-04-24 08:44 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 591 | 588 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| vwalker1 | 48 | 582 | 2024-11-19 15:19 | 2025-03-14 16:25 | 265 | 67 | 198 | 73 | 70 | 3 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 38 | 38 | 0 | 0 | 0 | 0 | 3 | 38 | 3 |
| srose1 | 64 | 554 | 2024-11-07 12:13 | 2026-06-10 13:04 | 7 | 6 | 1 | 151 | 138 | 13 | 4 | 4 | 0 | 0 | 65 | 0 | 65 | 0 | 84 | 84 | 5 | 2 | 0 | 0 | 0 | 0 | 1 |
| ptodoroff | 115 | 547 | 2024-11-01 16:17 | 2026-06-09 10:12 | 0 | 0 | 0 | 156 | 155 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 175 | 173 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| carterl | 63 | 508 | 2024-11-08 16:32 | 2026-06-15 10:57 | 51 | 51 | 0 | 138 | 136 | 0 | 55 | 55 | 0 | 0 | 2 | 0 | 2 | 0 | 87 | 78 | 14 | 0 | 0 | 0 | 0 | 0 | 5 |
| cframburg | 10 | 466 | 2024-11-05 13:59 | 2024-11-27 11:07 | 0 | 0 | 0 | 177 | 177 | 0 | 0 | 0 | 0 | 0 | 10 | 10 | 0 | 0 | 14 | 11 | 2 | 79 | 0 | 2 | 0 | 0 | 0 |
| jewet4924 | 47 | 452 | 2025-01-10 08:23 | 2026-04-07 20:01 | 49 | 34 | 15 | 105 | 99 | 5 | 39 | 39 | 0 | 0 | 6 | 0 | 6 | 0 | 132 | 127 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| rhiggins | 45 | 426 | 2024-11-01 11:11 | 2025-06-06 15:45 | 38 | 14 | 24 | 61 | 39 | 14 | 26 | 26 | 0 | 0 | 5 | 1 | 4 | 0 | 188 | 185 | 4 | 1 | 0 | 0 | 0 | 0 | 1 |
| jfangman | 38 | 388 | 2024-11-13 13:27 | 2026-05-18 18:39 | 129 | 31 | 98 | 81 | 81 | 0 | 79 | 79 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 23 |
| maggiem | 36 | 372 | 2024-11-04 11:31 | 2026-03-26 09:48 | 76 | 26 | 50 | 52 | 48 | 0 | 24 | 24 | 0 | 0 | 14 | 0 | 14 | 0 | 31 | 29 | 19 | 15 | 0 | 0 | 0 | 0 | 0 |
| tammymartindsg | 20 | 371 | 2024-11-04 11:54 | 2025-08-26 16:45 | 25 | 11 | 14 | 70 | 70 | 0 | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 | 214 | 214 | 0 | 0 | 0 | 0 | 1 | 2 | 0 |
| clscott | 37 | 361 | 2024-11-04 10:16 | 2026-06-06 15:31 | 11 | 0 | 11 | 27 | 16 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 237 | 237 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| khastings | 39 | 307 | 2024-11-11 12:02 | 2026-04-16 09:46 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 213 | 213 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| nickbrown | 9 | 303 | 2024-11-01 11:47 | 2024-11-26 14:56 | 37 | 1 | 36 | 93 | 93 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 5 | 0 | 82 | 81 | 1 | 10 | 0 | 0 | 0 | 0 | 0 |
| calberg | 27 | 271 | 2024-11-01 11:27 | 2026-01-27 15:55 | 50 | 26 | 24 | 49 | 43 | 6 | 46 | 46 | 0 | 0 | 0 | 0 | 0 | 0 | 26 | 25 | 7 | 0 | 0 | 0 | 0 | 7 | 10 |
| rboles | 27 | 270 | 2024-11-14 11:05 | 2026-04-30 14:12 | 15 | 6 | 9 | 17 | 15 | 2 | 10 | 10 | 0 | 0 | 5 | 0 | 5 | 0 | 116 | 116 | 10 | 1 | 0 | 0 | 0 | 1 | 4 |
| donna_s | 48 | 268 | 2024-11-07 13:53 | 2025-11-06 16:21 | 9 | 9 | 0 | 44 | 44 | 0 | 101 | 101 | 0 | 0 | 3 | 0 | 3 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| bgrillo | 120 | 257 | 2024-12-02 19:35 | 2026-06-15 10:04 | 13 | 3 | 10 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 32 | 32 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| lcarmichael | 27 | 250 | 2025-06-19 15:38 | 2026-06-15 15:51 | 32 | 9 | 23 | 37 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 92 | 85 | 8 | 0 | 0 | 0 | 9 | 4 | 0 |
| matt | 25 | 239 | 2024-11-18 16:49 | 2026-04-28 12:35 | 10 | 10 | 0 | 31 | 31 | 0 | 34 | 34 | 0 | 0 | 3 | 0 | 3 | 0 | 64 | 64 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| mgraham | 35 | 237 | 2024-11-01 12:08 | 2026-05-08 14:02 | 89 | 19 | 70 | 22 | 20 | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 23 | 3 | 0 | 0 | 0 | 1 | 1 | 3 |
| vcollins | 41 | 233 | 2025-02-17 18:21 | 2026-06-12 12:26 | 66 | 21 | 45 | 57 | 46 | 1 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 12 | 3 | 1 | 0 | 0 | 0 | 0 | 0 |
| kellyk | 19 | 230 | 2024-11-01 12:22 | 2024-11-26 15:23 | 62 | 12 | 50 | 15 | 15 | 0 | 7 | 7 | 0 | 0 | 3 | 3 | 0 | 0 | 60 | 56 | 9 | 0 | 0 | 0 | 0 | 0 | 0 |
| kathys | 20 | 205 | 2024-11-04 11:10 | 2025-01-06 21:53 | 5 | 5 | 0 | 127 | 127 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 17 | 15 | 10 | 0 | 0 | 0 | 0 | 0 | 0 |
| pres81224 | 21 | 178 | 2025-01-08 08:08 | 2026-06-11 12:47 | 28 | 6 | 22 | 25 | 23 | 2 | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 61 | 59 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| troyk | 30 | 177 | 2024-11-04 10:56 | 2026-06-12 17:42 | 14 | 4 | 10 | 61 | 61 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 9 | 18 | 0 | 0 | 0 | 0 | 0 | 0 |
| liz_n | 75 | 177 | 2024-11-03 11:09 | 2025-12-09 19:33 | 10 | 7 | 3 | 21 | 21 | 0 | 13 | 13 | 0 | 0 | 2 | 0 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| starrylights | 9 | 173 | 2024-12-09 11:19 | 2025-01-22 19:56 | 8 | 7 | 1 | 45 | 45 | 0 | 39 | 39 | 0 | 0 | 0 | 0 | 0 | 0 | 44 | 41 | 4 | 0 | 0 | 0 | 0 | 0 | 2 |
| mmccarthy1 | 24 | 164 | 2024-11-01 10:08 | 2025-04-21 15:59 | 30 | 30 | 0 | 34 | 34 | 0 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 18 |
| sorourke | 12 | 150 | 2024-11-01 14:27 | 2026-05-05 16:55 | 6 | 2 | 4 | 43 | 23 | 20 | 8 | 8 | 0 | 0 | 24 | 0 | 24 | 0 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pjames1 | 16 | 130 | 2025-02-07 09:59 | 2026-06-03 15:09 | 30 | 10 | 20 | 32 | 31 | 0 | 23 | 23 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 1 | 0 | 0 | 0 | 2 | 2 | 0 |
| jose | 27 | 114 | 2024-11-26 12:26 | 2026-06-14 08:51 | 10 | 3 | 7 | 1 | 1 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 41 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| monicam | 11 | 108 | 2024-11-04 14:33 | 2025-06-17 15:46 | 2 | 2 | 0 | 6 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 75 | 71 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kmurphy4 | 18 | 100 | 2024-11-12 09:21 | 2026-04-22 23:36 | 2 | 2 | 0 | 30 | 30 | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 2 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 |
| eddiev | 18 | 95 | 2024-11-05 23:03 | 2025-01-28 23:35 | 10 | 10 | 0 | 41 | 41 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 1 | 2 | 0 |
| aminkhan | 53 | 93 | 2024-11-04 11:23 | 2026-06-10 13:06 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| rschwartz1 | 4 | 88 | 2024-11-04 14:14 | 2026-06-11 09:23 | 8 | 2 | 6 | 34 | 34 | 0 | 34 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 3 | 0 | 0 | 0 | 0 | 1 | 0 |
| zcarranta | 12 | 82 | 2025-11-14 12:50 | 2026-05-29 14:01 | 5 | 3 | 2 | 3 | 3 | 0 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jlindquist | 8 | 79 | 2024-11-13 10:47 | 2025-01-15 12:12 | 13 | 3 | 10 | 21 | 21 | 0 | 17 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| hschwartz1 | 36 | 75 | 2024-11-12 07:30 | 2026-06-11 05:58 | 0 | 0 | 0 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| stevelinder | 28 | 72 | 2025-01-02 15:43 | 2026-06-15 18:04 | 2 | 2 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 | 0 | 0 | 0 | 0 | 1 | 1 | 0 |
| pcarlson | 30 | 72 | 2024-11-12 14:44 | 2026-05-22 19:01 | 14 | 4 | 10 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| aframburg | 9 | 70 | 2024-11-05 10:54 | 2024-12-05 15:53 | 11 | 5 | 6 | 21 | 19 | 0 | 3 | 3 | 0 | 0 | 2 | 0 | 1 | 1 | 1 | 1 | 0 | 3 | 0 | 0 | 0 | 0 | 0 |
| terry | 11 | 64 | 2024-11-28 23:05 | 2025-09-05 12:29 | 6 | 6 | 0 | 10 | 7 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 2 | 2 | 0 |
| rluttrell1 | 7 | 64 | 2025-01-07 09:49 | 2026-01-15 12:01 | 11 | 3 | 8 | 12 | 12 | 0 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 12 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| sarahp | 8 | 64 | 2026-04-09 12:13 | 2026-06-10 10:37 | 17 | 4 | 13 | 9 | 9 | 0 | 2 | 2 | 0 | 0 | 1 | 0 | 1 | 0 | 5 | 5 | 0 | 4 | 0 | 0 | 1 | 2 | 0 |
| bstout | 7 | 53 | 2024-11-27 11:05 | 2025-01-30 11:36 | 20 | 15 | 5 | 8 | 8 | 0 | 10 | 10 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| layla_c | 15 | 52 | 2024-11-05 15:12 | 2024-12-19 11:54 | 6 | 2 | 4 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tbierowski | 16 | 47 | 2024-12-30 12:31 | 2026-06-15 11:23 | 3 | 3 | 0 | 6 | 6 | 0 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| nandrus1 | 7 | 45 | 2026-04-25 16:35 | 2026-05-12 18:28 | 17 | 3 | 14 | 2 | 2 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 3 | 0 |
| alarrick | 8 | 43 | 2025-01-06 18:18 | 2025-03-31 14:20 | 14 | 4 | 10 | 7 | 7 | 0 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| martinb | 10 | 34 | 2024-11-08 14:11 | 2025-01-04 20:42 | 4 | 4 | 0 | 7 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| zachscar | 1 | 34 | 2026-02-02 18:51 | 2026-02-02 20:07 | 1 | 1 | 0 | 12 | 12 | 0 | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| earp727 | 13 | 32 | 2025-01-15 14:57 | 2026-04-17 14:35 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dkapalka | 6 | 28 | 2024-11-04 10:53 | 2025-01-10 14:33 | 3 | 3 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jwilson | 3 | 25 | 2025-06-16 14:08 | 2026-01-28 15:06 | 2 | 1 | 1 | 9 | 9 | 0 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| philcook | 15 | 25 | 2025-01-23 12:18 | 2026-02-02 22:05 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jarnoldenlight | 9 | 22 | 2025-01-07 21:01 | 2026-04-02 15:26 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mote1 | 8 | 22 | 2025-02-04 11:12 | 2026-03-05 22:55 | 6 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| ptheos | 3 | 21 | 2025-10-16 09:24 | 2026-04-20 16:35 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jskula | 5 | 17 | 2025-01-02 12:33 | 2026-04-07 15:01 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jonv | 9 | 15 | 2025-01-06 15:01 | 2026-01-24 12:09 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| swt | 7 | 15 | 2024-11-04 08:52 | 2025-06-18 06:23 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| brittainc | 3 | 14 | 2024-11-12 09:24 | 2024-12-10 13:57 | 1 | 1 | 0 | 5 | 5 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| tess | 5 | 13 | 2026-01-20 10:22 | 2026-04-17 10:20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| brentsanders | 3 | 13 | 2025-09-22 11:58 | 2026-02-28 14:18 | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mmullen1 | 2 | 12 | 2024-12-04 20:21 | 2024-12-09 08:47 | 0 | 0 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| bodonnell | 3 | 11 | 2025-01-16 16:02 | 2026-04-14 15:59 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mrose1 | 2 | 10 | 2025-11-18 17:36 | 2026-03-03 13:56 | 3 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| aheald | 1 | 8 | 2026-06-12 10:43 | 2026-06-12 10:45 | 1 | 1 | 0 | 2 | 2 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| tburgess | 3 | 6 | 2024-11-06 09:52 | 2025-09-21 21:39 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| pmarr | 2 | 6 | 2025-08-12 10:17 | 2025-08-14 10:37 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| rphillips1 | 2 | 4 | 2025-08-25 11:52 | 2026-04-20 12:49 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| djorge | 1 | 2 | 2026-06-09 12:24 | 2026-06-09 12:24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| thel84 | 1 | 2 | 2025-12-30 14:52 | 2025-12-30 14:53 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| dougy | 1 | 1 | 2025-01-15 13:24 | 2025-01-15 13:24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Q-01_step2_results.md

# Q-01-S2 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 41
- **Run date**: 2026-06-16


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Wayne Guthrie | 337 | $7.0M | $20,662 | 40 |
| Tony Minutelli | 207 | $2.1M | $10,114 | 38 |
| Lynn  Ross | 226 | $1.4M | $6,220 | 47 |
| Karen Clegg | 148 | $1.3M | $9,117 | 41 |
| Sherri Juhl | 175 | $1.1M | $6,073 | 25 |
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
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 137
- **Run date**: 2026-06-16


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bkrieger | 448 | 15,923 | 30 | 2,028 | 1,115 | 32 | 34 | 0 | 689 | 22 | Selling Rep |
| jgannon | 525 | 12,712 | 179 | 2,396 | 2,893 | 16 | 3 | 0 | 1,006 | 18 | Selling Rep |
| mgoffice | 362 | 12,679 | 8 | 2,197 | 93 | 0 | 0 | 0 | 74 | 0 | Selling Rep |
| steven | 408 | 11,920 | 0 | 1,345 | 2,339 | 11 | 7 | 0 | 164 | 8 | Content/Library Manager |
| dunnlighting | 425 | 9,558 | 120 | 1,348 | 1,383 | 31 | 23 | 0 | 244 | 17 | Selling Rep |
| amymatteson | 432 | 7,855 | 50 | 1,402 | 456 | 14 | 5 | 0 | 4 | 0 | Selling Rep |
| rgould | 473 | 6,999 | 77 | 1,296 | 1,034 | 64 | 42 | 0 | 95 | 3 | Selling Rep |
| wguthrie | 304 | 5,857 | 525 | 1,011 | 111 | 22 | 0 | 0 | 2 | 0 | Selling Rep |
| kgannon | 396 | 4,576 | 90 | 916 | 670 | 44 | 0 | 0 | 460 | 15 | Selling Rep |
| gduguid | 254 | 3,946 | 23 | 765 | 285 | 0 | 2 | 0 | 9 | 0 | Selling Rep |
| sherrij | 308 | 3,741 | 306 | 654 | 34 | 2 | 0 | 0 | 1 | 0 | Selling Rep |
| kclegg | 314 | 3,551 | 217 | 533 | 721 | 53 | 0 | 0 | 191 | 1 | Selling Rep |
| tannerg | 306 | 3,511 | 72 | 914 | 129 | 2 | 15 | 1 | 69 | 6 | Selling Rep |
| robantonecchia | 286 | 3,458 | 1 | 620 | 755 | 3 | 26 | 1 | 70 | 4 | Content/Library Manager |
| tminutelli | 253 | 3,387 | 382 | 405 | 11 | 0 | 3 | 0 | 1 | 0 | Selling Rep |
| lbelesky | 279 | 3,367 | 87 | 456 | 324 | 21 | 11 | 0 | 199 | 4 | Selling Rep |
| jenmccarty | 220 | 3,219 | 17 | 413 | 808 | 19 | 74 | 6 | 275 | 145 | Selling Rep |
| lynnr1 | 201 | 3,195 | 319 | 493 | 9 | 1 | 0 | 0 | 0 | 0 | Selling Rep |
| codyadler | 270 | 3,155 | 0 | 526 | 1,154 | 24 | 31 | 0 | 19 | 51 | Content/Library Manager |
| gschwartz1 | 150 | 2,968 | 6 | 422 | 402 | 26 | 20 | 2 | 135 | 40 | Selling Rep |
| jfs | 288 | 2,708 | 4 | 524 | 421 | 5 | 5 | 0 | 4 | 4 | Selling Rep |
| jimhickey | 326 | 2,704 | 9 | 221 | 676 | 102 | 0 | 0 | 315 | 0 | Selling Rep |
| aknapp | 169 | 2,594 | 0 | 254 | 1,033 | 3 | 56 | 2 | 22 | 45 | Content/Library Manager |
| broche | 231 | 2,587 | 3 | 634 | 468 | 28 | 23 | 0 | 11 | 0 | Selling Rep |
| etibbetts | 168 | 2,408 | 0 | 271 | 753 | 9 | 23 | 0 | 53 | 23 | Content/Library Manager |
| mberesford | 196 | 2,270 | 6 | 310 | 481 | 16 | 0 | 0 | 66 | 0 | Selling Rep |
| jreibel | 502 | 2,182 | 1 | 450 | 72 | 14 | 2 | 0 | 107 | 1 | Analytics/Portal User |
| dpritchard | 319 | 2,179 | 0 | 281 | 178 | 22 | 2 | 0 | 213 | 3 | Content/Library Manager |
| jchon | 200 | 2,134 | 5 | 305 | 45 | 0 | 0 | 0 | 1 | 3 | Selling Rep |
| tstauffacher | 195 | 2,045 | 9 | 322 | 570 | 32 | 4 | 0 | 78 | 10 | Selling Rep |
| apoindexter | 300 | 2,038 | 4 | 372 | 138 | 4 | 4 | 0 | 61 | 2 | Selling Rep |
| amcguire | 179 | 1,822 | 1 | 234 | 725 | 8 | 19 | 0 | 7 | 0 | Content/Library Manager |
| kimartin | 162 | 1,638 | 14 | 256 | 382 | 7 | 12 | 0 | 0 | 2 | Selling Rep |
| kgrillo | 155 | 1,630 | 0 | 219 | 557 | 2 | 33 | 0 | 2 | 51 | Content/Library Manager |
| starrylightssupport | 126 | 1,613 | 1 | 462 | 228 | 1 | 15 | 0 | 3 | 5 | Content/Library Manager |
| ctwigg | 168 | 1,593 | 205 | 357 | 3 | 1 | 0 | 0 | 0 | 0 | Selling Rep |
| lross | 137 | 1,567 | 171 | 280 | 11 | 1 | 0 | 0 | 2 | 0 | Selling Rep |
| smicheal | 152 | 1,537 | 3 | 298 | 26 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| jeffizower | 116 | 1,479 | 6 | 212 | 465 | 1 | 17 | 0 | 18 | 15 | Selling Rep |
| pgould | 85 | 1,433 | 17 | 162 | 741 | 1 | 0 | 0 | 3 | 6 | Selling Rep |
| lightingrep | 90 | 1,424 | 0 | 353 | 48 | 7 | 16 | 1 | 0 | 56 | Merchandising/List Curator |
| vingato | 199 | 1,400 | 14 | 311 | 30 | 1 | 0 | 0 | 6 | 0 | Selling Rep |
| astauffacher | 77 | 1,347 | 3 | 124 | 872 | 12 | 0 | 0 | 28 | 0 | Selling Rep |
| jessicam | 120 | 1,189 | 7 | 134 | 265 | 1 | 2 | 0 | 3 | 3 | Selling Rep |
| sschwartz1 | 93 | 1,143 | 2 | 144 | 336 | 39 | 6 | 0 | 8 | 0 | Content/Library Manager |
| ccoxworth | 151 | 1,137 | 0 | 215 | 459 | 16 | 0 | 0 | 1 | 1 | Content/Library Manager |
| grillocs | 335 | 1,032 | 0 | 132 | 43 | 0 | 1 | 0 | 1 | 1 | Sales Support/Inside Sales |
| tripm | 78 | 1,016 | 5 | 159 | 93 | 1 | 10 | 2 | 2 | 3 | Selling Rep |
| bpeel | 223 | 949 | 0 | 167 | 24 | 0 | 0 | 0 | 147 | 0 | Analytics/Portal User |
| nstory | 54 | 937 | 0 | 85 | 455 | 3 | 0 | 0 | 12 | 0 | Content/Library Manager |
| lightingvision | 38 | 838 | 3 | 76 | 413 | 4 | 0 | 0 | 3 | 0 | Selling Rep |
| dougg | 59 | 817 | 9 | 96 | 109 | 3 | 6 | 0 | 0 | 0 | Selling Rep |
| rocher | 71 | 811 | 1 | 102 | 422 | 14 | 1 | 0 | 0 | 0 | Content/Library Manager |
| williamsl | 159 | 800 | 5 | 187 | 47 | 8 | 1 | 0 | 16 | 0 | Selling Rep |
| kaceywilliams | 64 | 796 | 0 | 207 | 252 | 1 | 1 | 0 | 22 | 4 | Content/Library Manager |
| lmalchus | 62 | 787 | 0 | 111 | 287 | 0 | 9 | 0 | 2 | 15 | Content/Library Manager |
| todd_m | 59 | 715 | 0 | 29 | 497 | 3 | 1 | 0 | 0 | 0 | Content/Library Manager |
| dsouthwickdrew | 63 | 712 | 2 | 35 | 396 | 0 | 0 | 0 | 9 | 1 | Content/Library Manager |
| nickc | 212 | 707 | 0 | 93 | 101 | 2 | 5 | 0 | 34 | 1 | Sales Support/Inside Sales |
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
| bgrillo | 120 | 257 | 0 | 2 | 32 | 0 | 0 | 0 | 2 | 0 | Low-Activity User |
| lcarmichael | 27 | 250 | 0 | 36 | 85 | 7 | 0 | 0 | 8 | 0 | Inactive |
| matt | 25 | 239 | 0 | 31 | 64 | 0 | 3 | 0 | 0 | 2 | Inactive |
| mgraham | 35 | 237 | 3 | 20 | 23 | 2 | 0 | 0 | 3 | 0 | Selling Rep |
| vcollins | 41 | 233 | 0 | 46 | 12 | 0 | 0 | 0 | 3 | 1 | Low-Activity User |
| kellyk | 19 | 230 | 0 | 15 | 56 | 4 | 0 | 0 | 9 | 0 | Inactive |
| kathys | 20 | 205 | 0 | 127 | 15 | 2 | 0 | 0 | 10 | 0 | Inactive |
| pres81224 | 21 | 178 | 0 | 23 | 59 | 2 | 0 | 0 | 0 | 0 | Inactive |
| troyk | 30 | 177 | 0 | 61 | 9 | 4 | 0 | 0 | 18 | 0 | Inactive |
| liz_n | 75 | 177 | 0 | 21 | 1 | 0 | 2 | 0 | 0 | 0 | Low-Activity User |
| starrylights | 9 | 173 | 2 | 45 | 41 | 3 | 0 | 0 | 4 | 0 | Inactive |
| mmccarthy1 | 24 | 164 | 18 | 34 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| sorourke | 12 | 150 | 0 | 23 | 13 | 0 | 24 | 0 | 0 | 0 | Catalog/Data Manager |
| pjames1 | 16 | 130 | 0 | 31 | 7 | 0 | 0 | 0 | 1 | 0 | Inactive |
| jose | 27 | 114 | 1 | 1 | 40 | 1 | 0 | 0 | 0 | 0 | Inactive |
| monicam | 11 | 108 | 0 | 5 | 71 | 4 | 0 | 0 | 0 | 0 | Inactive |
| kmurphy4 | 18 | 100 | 0 | 30 | 0 | 0 | 2 | 0 | 2 | 1 | Inactive |
| eddiev | 18 | 95 | 0 | 41 | 6 | 0 | 0 | 0 | 0 | 0 | Inactive |
| aminkhan | 53 | 93 | 0 | 3 | 0 | 0 | 0 | 0 | 1 | 0 | Low-Activity User |
| rschwartz1 | 4 | 88 | 0 | 34 | 1 | 0 | 0 | 0 | 3 | 0 | Inactive |
| zcarranta | 12 | 82 | 0 | 3 | 25 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jlindquist | 8 | 79 | 0 | 21 | 6 | 0 | 0 | 0 | 0 | 0 | Inactive |
| hschwartz1 | 36 | 75 | 0 | 2 | 2 | 0 | 0 | 0 | 0 | 1 | Low-Activity User |
| pcarlson | 30 | 72 | 0 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | Inactive |
| stevelinder | 28 | 72 | 0 | 5 | 8 | 0 | 0 | 0 | 0 | 0 | Inactive |
| aframburg | 9 | 70 | 0 | 19 | 1 | 0 | 1 | 0 | 0 | 3 | Inactive |
| rluttrell1 | 7 | 64 | 0 | 12 | 12 | 0 | 0 | 0 | 1 | 0 | Inactive |
| sarahp | 8 | 64 | 0 | 9 | 5 | 0 | 1 | 0 | 0 | 4 | Inactive |
| terry | 11 | 64 | 0 | 7 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| bstout | 7 | 53 | 0 | 8 | 0 | 0 | 1 | 0 | 0 | 0 | Inactive |
| layla_c | 15 | 52 | 0 | 18 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tbierowski | 16 | 47 | 0 | 6 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| nandrus1 | 7 | 45 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| alarrick | 8 | 43 | 3 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| zachscar | 1 | 34 | 0 | 12 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| martinb | 10 | 34 | 0 | 7 | 2 | 0 | 0 | 0 | 0 | 0 | Inactive |
| earp727 | 13 | 32 | 0 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dkapalka | 6 | 28 | 0 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| philcook | 15 | 25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jwilson | 3 | 25 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jarnoldenlight | 9 | 22 | 0 | 0 | 9 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mote1 | 8 | 22 | 0 | 0 | 1 | 0 | 0 | 0 | 2 | 0 | Inactive |
| ptheos | 3 | 21 | 0 | 0 | 13 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jskula | 5 | 17 | 0 | 0 | 4 | 3 | 0 | 0 | 0 | 0 | Inactive |
| swt | 7 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| jonv | 9 | 15 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brittainc | 3 | 14 | 0 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brentsanders | 3 | 13 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tess | 5 | 13 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| mmullen1 | 2 | 12 | 0 | 5 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| bodonnell | 3 | 11 | 0 | 1 | 1 | 2 | 0 | 0 | 0 | 0 | Inactive |
| mrose1 | 2 | 10 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | Inactive |
| aheald | 1 | 8 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| tburgess | 3 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| pmarr | 2 | 6 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| rphillips1 | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| thel84 | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| djorge | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| dougy | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 57 | 88 | 26 |

### Q-06_results.md

# Q-06 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 104
- **Run date**: 2026-06-16


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Wayne Guthrie | 53 | 60 | 13.20 | 70 | 95 | 35.70 | $4.0M |
| Lynn  Ross | 44 | 35 | -20.50 | 64 | 52 | -18.80 | $361,368 |
| Sherri Juhl | 63 | 52 | -17.50 | 53 | 37 | -30.20 | $190,903 |
| Karen Clegg | 72 | 56 | -22.20 | 52 | 35 | -32.70 | $280,300 |
| Tony Minutelli | 75 | 38 | -49.30 | 70 | 32 | -54.30 | $514,283 |
| Chris Twigg | 34 | 38 | 11.80 | 28 | 28 | 0 | $244,086 |
| Dunn Lighting | 269 | 184 | -31.60 | 19 | 26 | 36.80 | $65,614 |
| Julie Gannon | 316 | 297 | -6 | 23 | 23 | 0 | $84,126 |
| Lynn Ross | 27 | 12 | -55.60 | 34 | 21 | -38.20 | $97,928 |
| Kevin Gannon | 210 | 188 | -10.50 | 23 | 20 | -13 | $46,410 |
| Tanner Gould | 86 | 72 | -16.30 | 8 | 14 | 75 | $58,536 |
| Brad Krieger | 618 | 487 | -21.20 | 10 | 12 | 20 | $142,844 |
| Lisa Belesky | 106 | 75 | -29.20 | 20 | 10 | -50 | $47,178 |
| Randy Gould | 206 | 223 | 8.30 | 13 | 9 | -30.80 | $30,345 |
| Jenifer McCarty | 142 | 171 | 20.40 | 5 | 6 | 20 | $8,832 |
| Amy Matteson | 162 | 132 | -18.50 | 4 | 6 | 50 | $23,767 |
| Martha Graham & Associates Office | 129 | 116 | -10.10 | 1 | 3 | 200 | $14,942 |
| John Fangman | 0 | 5 | — | 0 | 2 | — | $2,844 |
| Doug Glassman | 27 | 6 | -77.80 | 4 | 2 | -50 | $16,887 |
| Grant Duguid | 77 | 47 | -39 | 0 | 2 | — | $15,604 |
| Tami Stauffacher | 43 | 32 | -25.60 | 3 | 2 | -33.30 | $10,141 |
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
| Vincent Ingato | 75 | 31 | -58.70 | — | — | — | — |
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
| Kirk Martin | 4 | 0 | -100 | — | — | — | — |
| Melanie Rose | 2 | 0 | -100 | — | — | — | — |
| Todd Bierowski | 5 | 3 | -40 | — | — | — | — |

### Q-43_step2_results.md

# Q-43-S2 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16
- **Total flagged**: 1
- **Aggregate GMV**: $20,656

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |
| Martha Graham & Associates Office | 5 | $20,656 | keyword | confirmed_operational |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### Q-51_results.md

# Q-51 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-51 — Rep-Level eCat Capture
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| rep_name | rep_number | erp_orders | erp_gmv | erp_customers | ecat_orders | ecat_gmv | ecat_customers | ecat_capture_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BrandJump, LLC | 42586 | 5,332 | $5.6M | 11 | 0 | $0 | 0 | 0 |
| Martha Graham & Assoc: Martha | 12328 | 1,555 | $3.8M | 173 | 0 | $0 | 0 | 0 |
| Grillo Group | 42333 | 212 | $3.3M | 40 | 0 | $0 | 0 | 0 |
| Speckk Brands | 45123 | 1,737 | $3.2M | 190 | 0 | $0 | 0 | 0 |
| Glassman Brands | 11998 | 1,473 | $3.0M | 226 | 0 | $0 | 0 | 0 |
| Lighting Vision, Inc | 44079 | 981 | $2.6M | 145 | 0 | $0 | 0 | 0 |
| Gannon Sales Agency | 42332 | 1,557 | $2.4M | 202 | 0 | $0 | 0 | 0 |
| Dunn Lighting | 41168 | 1,112 | $2.2M | 188 | 76 | $294,335 | 50 | 13.50 |
| Ricci Sales Agency | 11871 | 968 | $1.8M | 212 | 0 | $0 | 0 | 0 |
| Stander Associates, Inc. | 40550 | 911 | $1.6M | 79 | 0 | $0 | 0 | 0 |
| Gould Associates | 12225 | 560 | $1.6M | 117 | 0 | $0 | 0 | 0 |
| Carolina Fixture Sales | 37184 | 531 | $1.0M | 117 | 0 | $0 | 0 | 0 |
| Enlightening Sales | 41451 | 429 | $1.0M | 137 | 0 | $0 | 0 | 0 |
| Adler Lighting Sales, LLC. | 43090 | 409 | $792,813 | 102 | 0 | $0 | 0 | 0 |
| Vincent Ingato Sales | 12868 | 387 | $694,891 | 62 | 0 | $0 | 0 | 0 |
| Guthrie & Associates | 12367 | 170 | $640,494 | 64 | 0 | $0 | 0 | 0 |
| Decor Lighting Sales | 42067 | 280 | $617,564 | 47 | 0 | $0 | 0 | 0 |
| Williams Lighting Source | 41148 | 187 | $455,826 | 36 | 0 | $0 | 0 | 0 |
| Larrick Design Resources | 16998 | 99 | $318,998 | 38 | 0 | $0 | 0 | 0 |
| Apex Lighting Solutions | 13794 | 103 | $302,164 | 36 | 0 | $0 | 0 | 0 |
| Exclusively Lighting Inc. | 37385 | 33 | $266,241 | 13 | 0 | $0 | 0 | 0 |
| WE Hospitality | 12185 | 83 | $246,129 | 35 | 0 | $0 | 0 | 0 |
| Lighting Environments | 42952 | 35 | $207,265 | 14 | 0 | $0 | 0 | 0 |
| Enterprise Lighting Sales Corp | 43184 | 59 | $203,319 | 25 | 0 | $0 | 0 | 0 |
| SJ Concepts | 12457 | 78 | $196,074 | 31 | 0 | $0 | 0 | 0 |

### Q-62_results.md

# Q-62 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### Q-63_results.md

# Q-63 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bkrieger | 40 | 322 | 10 | 25 | 3.10 | 321 | 1 | 0 |
| mgoffice | 38 | 216 | 2 | 5.30 | 0.90 | 216 | 0 | 0 |
| dunnlighting | 20 | 163 | 12 | 60 | 7.40 | 163 | 0 | 0 |
| steven | 29 | 161 | 0 | 0 | 0 | 161 | 0 | 0 |
| rgould | 25 | 145 | 5 | 20 | 3.40 | 138 | 0 | 7 |
| amymatteson | 15 | 138 | 3 | 20 | 2.20 | 138 | 0 | 0 |
| jenmccarty | 7 | 124 | 8 | 114.30 | 6.50 | 111 | 13 | 0 |
| wguthrie | 15 | 120 | 71 | 473.30 | 59.20 | 120 | 0 | 0 |
| jgannon | 11 | 100 | 7 | 63.60 | 7 | 100 | 0 | 0 |
| robantonecchia | 8 | 96 | 0 | 0 | 0 | 95 | 1 | 0 |
| tannerg | 12 | 94 | 10 | 83.30 | 10.60 | 90 | 2 | 2 |
| kgannon | 14 | 75 | 15 | 107.10 | 20 | 75 | 0 | 0 |
| ctwigg | 1 | 65 | 27 | 2,700 | 41.50 | 65 | 0 | 0 |
| sherrij | 8 | 64 | 30 | 375 | 46.90 | 64 | 0 | 0 |
| jeffizower | 3 | 52 | 1 | 33.30 | 1.90 | 50 | 2 | 0 |
| lbelesky | 4 | 51 | 7 | 175 | 13.70 | 51 | 0 | 0 |
| gduguid | 5 | 48 | 2 | 40 | 4.20 | 48 | 0 | 0 |
| kclegg | 7 | 45 | 25 | 357.10 | 55.60 | 45 | 0 | 0 |
| etibbetts | 1 | 38 | 0 | 0 | 0 | 37 | 1 | 0 |
| lynnr1 | 5 | 36 | 35 | 700 | 97.20 | 36 | 0 | 0 |

### Q-64_results.md

# Q-64 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| ctwigg | 1 | 189 | 25 | 1 | 0 |
| sorourke | 1 | 37 | 1 | 1 | 0 |
| jenmccarty | 14 | 27.20 | 2.60 | 6 | 2 |
| dougg | 3 | 25 | 1 | 2 | 0 |
| kaceywilliams | 3 | 23.30 | 2 | 2 | 0 |
| kclegg | 19 | 16.90 | 3.40 | 10 | 4 |
| lynnr1 | 21 | 16.50 | 3 | 11 | 1 |
| wguthrie | 32 | 16.30 | 2.80 | 16 | 2 |
| jessicam | 12 | 16.30 | 1.90 | 3 | 1 |
| sherrij | 20 | 16.30 | 3 | 12 | 2 |
| lbelesky | 20 | 15.90 | 2.40 | 10 | 3 |
| jeffizower | 14 | 13.60 | 1.10 | 4 | 6 |
| lross | 12 | 12.40 | 2.20 | 8 | 0 |
| pgould | 6 | 11.80 | 1.70 | 1 | 1 |
| robantonecchia | 38 | 11.70 | 1.50 | 12 | 8 |
| gduguid | 20 | 11.20 | 1.80 | 8 | 2 |
| bkrieger | 164 | 11.10 | 2.10 | 73 | 26 |
| mgoffice | 105 | 10.80 | 2.50 | 53 | 13 |
| etibbetts | 8 | 10.80 | 1.60 | 2 | 2 |
| bgrillo | 2 | 10.50 | 4 | 2 | 0 |

### Q-65_results.md

# Q-65 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| wguthrie | 948 | 869 | 79 | 91.70 | 8.30 |
| mgoffice | 1,901 | 1,672 | 229 | 88 | 12 |
| dougg | 99 | 87 | 12 | 87.90 | 12.10 |
| lross | 179 | 148 | 31 | 82.70 | 17.30 |
| tminutelli | 287 | 236 | 51 | 82.20 | 17.80 |
| lynnr1 | 403 | 329 | 74 | 81.60 | 18.40 |
| gduguid | 408 | 324 | 84 | 79.40 | 20.60 |
| sherrij | 420 | 330 | 90 | 78.60 | 21.40 |
| tripm | 154 | 117 | 37 | 76 | 24 |
| lcarmichael | 37 | 28 | 9 | 75.70 | 24.30 |
| ctwigg | 248 | 187 | 61 | 75.40 | 24.60 |
| smicheal | 194 | 146 | 48 | 75.30 | 24.70 |
| rhailpern | 24 | 18 | 6 | 75 | 25 |
| sorourke | 42 | 31 | 11 | 73.80 | 26.20 |
| amymatteson | 987 | 707 | 280 | 71.60 | 28.40 |
| tannerg | 475 | 339 | 136 | 71.40 | 28.60 |
| nandrus1 | 45 | 31 | 14 | 68.90 | 31.10 |
| kaceywilliams | 90 | 62 | 28 | 68.90 | 31.10 |
| jfs | 524 | 353 | 171 | 67.40 | 32.60 |
| vcollins | 142 | 92 | 50 | 64.80 | 35.20 |

### Q-70_results.md

# Q-70 Results — Hubbardton Forge (hfg, org_id=165)
- **Query**: Q-70 — Inactive Reps with Territory Revenue
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### user_group_mapping.md

# User Group Mapping — Hubbardton Forge (hfg, org_id=165)
- **Run date**: 2026-06-16
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
| admin_internal | 14 | 6,574 | 3.5% |
| other | 104 | 182,073 | 96.5% |
