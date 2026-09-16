# Section 2 Context Bundle — Currey & Company (cci)
Run date: 2026-06-16

## Gate Flags

# Gate Flags — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-16
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| HAS_CLICKY | False | has_clicky_portal=False |
| HAS_CART | False | recurring_services contains B2B Cart: False; server_order_count=0 — overridden to false |
| HAS_PORTAL_ORDERS | True | portal_order_count=57914, portal_order_gmv=$88.1M |
| HAS_INVENTORY | True | inventory_count=3441 |
| HAS_SALES_DATA | True | sales_data_count=110629 |
| HAS_SALES_SECTION | True | qualifying_reps=37 (threshold: >=5) |
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
| VM45_GATE_1 | PASS | erp_gmv=$88.1M > ecat_gmv=$8.6M: True |
| VM45_GATE_2 | PASS | ecat_gmv >= 5% of erp_gmv: True |
| VM45_RENDER | True | Both gates pass |
| QUALIFYING_REP_COUNT | 37 | 37 |
| MIXPANEL_USER_DATA_PRESENT | True | Q-01 Step 1 returned 76 rows |
| SHOWROOM_EXCLUSIONS | 3 | 3 accounts flagged |
| MIXPANEL_ORDER_TRACKING_GAP | False | Postgres LTM orders: 3983, Mixpanel total submit_order (Q-01): 6587 |
| USER_GROUP_SPLIT_AVAILABLE | False | join_rate=97.4%, ambiguous_rate=0.0%, showroom_event_share=8.5% |
| USER_GROUP_JOIN_RATE | 97% | 74 of 76 Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | 9% | showroom+admin share of matched events: 8.5% |
| ADMIN_REPS_IN_LEADERBOARD | True | 4 admin/showroom users in leaderboard: Atlanta Showroom, CC Dallas Showroom, Highpoint Showroom, Allan Otto |

## ERP Enrichment Gates

| Flag | Value | Evidence |
| --- | --- | --- |
| PORTAL_ORDERS_FRESH | True | days_since_last_erp_order=1 (threshold: <=60) |
| PORTAL_REP_DATA_PRESENT | True | distinct_rep_names=53 |
| PORTAL_CUSTOMER_DATA_PRESENT | True | distinct_bill_to_customers=7919 |
| INVENTORY_FRESH | True | inventories last_updated 0d ago (threshold: <=30d) |
| SALES_DATA_FRESH | False | sales_data not found in Q-08 data_versions |
| CUSTOMER_DATA_FRESH | True | customers last_updated 0d ago (threshold: <=30d) |
| HAS_COMMITMENT_DATA | False | commitment_reports_count=0 |
| HAS_NEW_ITEMS | True | new_item_count=369 |
| HAS_BUYER_DATA | True | distinct_buyers_6mo=3204 |

## Confidence Tiers

| Flag | Value | Formula Inputs |
| --- | --- | --- |
| SECTION_CONFIDENCE_2 | FULL | See Derived Gate 6 §2 formula |
| SECTION_CONFIDENCE_3 | FULL | See Derived Gate 6 §3 formula |
| SECTION_CONFIDENCE_4 | STRONG | See Derived Gate 6 §4 formula |
| SECTION_CONFIDENCE_5 | FULL | See Derived Gate 6 §5 formula |

## Org Identity

- **Client name**: Currey & Company
- **Shortname**: cci
- **Org ID**: 161
- **Bundle**: 5
- **Bundle label for report**: 5

## Validation Log

- (none)

## Section Confidence

# Section Confidence Tiers — Currey & Company (cci, org_id=161)
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
| HAS_INVENTORY | True |
| HAS_SALES_DATA | True |
| INVENTORY_FRESH | True |
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

# Q-01-S1 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-01-S1 — Rep Behavioral Scorecard — Step 1 (Mixpanel)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 76
- **Run date**: 2026-06-16


| username | days_active | total_events | first_event | last_event | customer_targeting | select_a_customer | search_for_customer | product_discovery | search_products | filter_products | config_bundling | order_configured_item | view_kit | order_kit | presentation | email_item_info | create_pdf_catalog | share_my_list | information | view_library_entry | access_sales_portal | view_my_list | create_my_list | edit_my_list | view_cust_favorites | view_ipad_orders | submit_order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| staciebaker | 394 | 15,536 | 2024-11-01 00:06 | 2026-06-14 23:39 | 3,782 | 964 | 2,818 | 4,083 | 4,022 | 61 | 0 | 0 | 0 | 0 | 239 | 64 | 175 | 0 | 299 | 289 | 7 | 142 | 0 | 0 | 32 | 78 | 439 |
| ripnance | 394 | 12,358 | 2024-11-04 09:17 | 2026-06-15 19:21 | 4,073 | 1,148 | 2,925 | 3,282 | 3,246 | 36 | 0 | 0 | 0 | 0 | 57 | 5 | 52 | 0 | 76 | 69 | 17 | 107 | 0 | 2 | 23 | 48 | 525 |
| sglosson | 330 | 9,190 | 2024-11-01 07:58 | 2026-05-27 16:43 | 5,092 | 954 | 4,138 | 2,025 | 2,014 | 11 | 0 | 0 | 0 | 0 | 6 | 5 | 1 | 0 | 110 | 71 | 37 | 4 | 0 | 0 | 6 | 13 | 422 |
| mindymcentire | 417 | 7,958 | 2024-11-01 15:13 | 2026-06-15 15:43 | 2,460 | 867 | 1,593 | 2,479 | 2,390 | 89 | 0 | 0 | 0 | 0 | 68 | 68 | 0 | 0 | 47 | 45 | 13 | 0 | 0 | 0 | 10 | 71 | 251 |
| carriehaymore | 357 | 7,669 | 2024-11-04 07:27 | 2026-06-15 10:04 | 2,950 | 739 | 2,211 | 2,214 | 2,212 | 2 | 0 | 0 | 0 | 0 | 25 | 0 | 25 | 0 | 183 | 183 | 4 | 43 | 0 | 0 | 1 | 13 | 332 |
| lesleyblair | 359 | 7,514 | 2024-11-01 12:48 | 2026-06-15 17:32 | 2,574 | 748 | 1,826 | 2,745 | 2,683 | 62 | 0 | 0 | 0 | 0 | 79 | 1 | 78 | 0 | 145 | 134 | 13 | 1 | 0 | 0 | 6 | 30 | 254 |
| vivimiraculmer | 227 | 6,865 | 2024-11-01 10:39 | 2026-06-13 10:35 | 1,486 | 388 | 1,098 | 2,214 | 2,158 | 56 | 0 | 0 | 0 | 0 | 77 | 2 | 73 | 2 | 7 | 6 | 11 | 207 | 0 | 0 | 15 | 39 | 26 |
| ccdallasshowroom | 315 | 6,617 | 2025-02-11 12:45 | 2026-06-15 13:57 | 2,929 | 677 | 2,252 | 1,442 | 1,434 | 8 | 0 | 0 | 0 | 0 | 35 | 15 | 20 | 0 | 117 | 108 | 9 | 1 | 0 | 0 | 5 | 11 | 540 |
| stewhaviland | 335 | 6,563 | 2024-11-01 10:18 | 2026-06-15 10:18 | 2,459 | 659 | 1,800 | 1,589 | 1,576 | 13 | 0 | 0 | 0 | 0 | 55 | 40 | 14 | 1 | 164 | 114 | 10 | 139 | 0 | 0 | 6 | 10 | 241 |
| rgould | 390 | 6,321 | 2024-11-01 16:36 | 2026-06-15 14:46 | 2,216 | 664 | 1,552 | 1,971 | 1,944 | 27 | 0 | 0 | 0 | 0 | 174 | 104 | 69 | 1 | 142 | 125 | 2 | 13 | 0 | 0 | 132 | 54 | 207 |
| kinshasafloyd | 369 | 5,883 | 2024-11-02 13:50 | 2026-06-12 14:30 | 1,947 | 698 | 1,249 | 1,667 | 1,648 | 19 | 0 | 0 | 0 | 0 | 47 | 2 | 45 | 0 | 95 | 93 | 8 | 61 | 0 | 1 | 66 | 26 | 197 |
| pattymiller | 304 | 5,288 | 2024-11-01 16:48 | 2026-06-15 16:09 | 2,649 | 513 | 2,136 | 851 | 732 | 119 | 0 | 0 | 0 | 0 | 36 | 0 | 36 | 0 | 9 | 9 | 7 | 0 | 0 | 0 | 2 | 5 | 158 |
| timshelton | 401 | 5,211 | 2024-11-01 06:32 | 2026-06-15 13:52 | 2,678 | 787 | 1,891 | 739 | 700 | 39 | 0 | 0 | 0 | 0 | 14 | 9 | 5 | 0 | 18 | 14 | 7 | 0 | 0 | 0 | 70 | 6 | 24 |
| russjones | 401 | 4,967 | 2024-11-01 07:29 | 2026-06-15 16:08 | 1,979 | 763 | 1,216 | 1,054 | 1,053 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 229 |
| margarethemartin | 264 | 4,706 | 2024-11-01 09:28 | 2026-06-10 09:03 | 1,745 | 401 | 1,344 | 1,663 | 1,660 | 3 | 0 | 0 | 0 | 0 | 6 | 3 | 3 | 0 | 67 | 51 | 16 | 5 | 0 | 1 | 8 | 9 | 235 |
| ccatlantashowroom | 198 | 4,110 | 2025-05-30 11:04 | 2026-06-15 14:10 | 2,016 | 308 | 1,708 | 737 | 735 | 2 | 0 | 0 | 0 | 0 | 45 | 10 | 31 | 4 | 173 | 126 | 37 | 67 | 0 | 0 | 5 | 26 | 132 |
| sandynakatsu | 74 | 3,704 | 2024-11-01 12:54 | 2026-04-23 10:16 | 957 | 266 | 691 | 1,852 | 1,780 | 72 | 0 | 0 | 0 | 0 | 23 | 0 | 21 | 2 | 14 | 14 | 5 | 49 | 0 | 0 | 7 | 27 | 5 |
| korison | 309 | 3,569 | 2024-11-01 14:38 | 2026-06-15 12:44 | 1,158 | 362 | 796 | 1,067 | 1,061 | 6 | 0 | 0 | 0 | 0 | 2 | 2 | 0 | 0 | 13 | 13 | 0 | 52 | 0 | 0 | 3 | 8 | 201 |
| jodieveeder | 260 | 3,568 | 2024-11-01 10:10 | 2026-06-15 17:12 | 1,438 | 311 | 1,127 | 864 | 850 | 14 | 0 | 0 | 0 | 0 | 13 | 5 | 7 | 1 | 145 | 136 | 19 | 42 | 0 | 1 | 2 | 11 | 121 |
| bettyrobbins | 189 | 3,385 | 2024-11-01 07:42 | 2026-06-14 10:55 | 1,762 | 257 | 1,505 | 695 | 631 | 64 | 0 | 0 | 0 | 0 | 5 | 3 | 2 | 0 | 76 | 72 | 16 | 0 | 0 | 0 | 0 | 3 | 131 |
| staceychiavetta | 229 | 3,213 | 2024-11-01 12:58 | 2026-06-15 20:28 | 1,366 | 434 | 932 | 859 | 859 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 35 | 35 | 3 | 1 | 0 | 0 | 0 | 11 | 283 |
| tannerg | 278 | 3,063 | 2024-11-01 11:56 | 2026-06-15 15:38 | 761 | 263 | 498 | 918 | 901 | 17 | 0 | 0 | 0 | 0 | 60 | 22 | 38 | 0 | 67 | 66 | 0 | 33 | 0 | 3 | 35 | 9 | 106 |
| joaniemartin | 198 | 3,036 | 2024-11-01 10:42 | 2026-06-08 14:54 | 1,302 | 339 | 963 | 740 | 731 | 9 | 0 | 0 | 0 | 0 | 4 | 2 | 0 | 2 | 12 | 12 | 5 | 2 | 0 | 0 | 10 | 21 | 225 |
| michaelmosko | 198 | 2,726 | 2024-11-01 11:43 | 2026-06-15 15:48 | 1,197 | 270 | 927 | 680 | 680 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 49 | 46 | 4 | 4 | 0 | 0 | 0 | 4 | 220 |
| shephallijain | 180 | 2,653 | 2024-11-01 09:50 | 2026-06-15 16:45 | 874 | 282 | 592 | 862 | 825 | 37 | 0 | 0 | 0 | 0 | 39 | 1 | 35 | 3 | 1 | 1 | 8 | 12 | 0 | 0 | 0 | 2 | 222 |
| marymiller | 163 | 2,640 | 2024-11-01 10:33 | 2026-06-15 17:03 | 1,454 | 276 | 1,178 | 390 | 389 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 7 | 5 | 0 | 0 | 0 | 7 | 58 | 201 |
| cindyr | 299 | 2,556 | 2024-11-01 09:42 | 2026-06-12 12:11 | 386 | 327 | 59 | 808 | 805 | 3 | 0 | 0 | 0 | 0 | 107 | 84 | 22 | 1 | 103 | 57 | 4 | 28 | 0 | 0 | 3 | 5 | 24 |
| robnance | 198 | 2,300 | 2024-11-11 12:53 | 2026-06-15 15:47 | 811 | 250 | 561 | 734 | 693 | 41 | 0 | 0 | 0 | 0 | 7 | 7 | 0 | 0 | 27 | 20 | 8 | 0 | 0 | 0 | 7 | 18 | 116 |
| nicolecasanova | 83 | 1,701 | 2024-11-04 13:34 | 2026-06-11 12:07 | 252 | 113 | 139 | 1,076 | 1,050 | 26 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19 | 18 | 1 | 0 | 0 | 0 | 5 | 1 | 1 |
| leekram | 206 | 1,621 | 2024-11-01 12:24 | 2026-06-15 18:38 | 307 | 107 | 200 | 466 | 449 | 17 | 0 | 0 | 0 | 0 | 28 | 3 | 24 | 1 | 3 | 3 | 3 | 24 | 0 | 0 | 1 | 3 | 55 |
| nancyhubbard | 203 | 1,613 | 2024-11-01 10:28 | 2026-06-15 16:32 | 331 | 88 | 243 | 111 | 111 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 475 | 226 | 0 | 0 | 0 | 0 | 2 | 1 | 49 |
| brigettefontenot | 138 | 1,560 | 2024-11-02 16:24 | 2026-06-10 10:13 | 413 | 116 | 297 | 501 | 491 | 5 | 0 | 0 | 0 | 0 | 20 | 12 | 7 | 1 | 32 | 31 | 12 | 9 | 0 | 0 | 3 | 15 | 19 |
| kristinireland | 67 | 1,436 | 2024-11-14 13:48 | 2026-06-04 21:23 | 212 | 84 | 128 | 151 | 122 | 29 | 0 | 0 | 0 | 0 | 42 | 30 | 12 | 0 | 0 | 0 | 0 | 80 | 0 | 0 | 35 | 6 | 18 |
| cchighpointshowroom | 61 | 1,309 | 2025-07-21 10:46 | 2026-06-11 11:28 | 153 | 36 | 117 | 715 | 708 | 7 | 0 | 0 | 0 | 0 | 9 | 0 | 9 | 0 | 51 | 49 | 1 | 21 | 0 | 0 | 0 | 8 | 13 |
| lorimccarver | 62 | 1,257 | 2024-11-01 09:59 | 2025-02-07 11:09 | 664 | 133 | 531 | 220 | 220 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 113 |
| allanotto | 80 | 1,188 | 2025-01-07 13:59 | 2026-06-05 16:35 | 439 | 114 | 325 | 104 | 55 | 49 | 0 | 0 | 0 | 0 | 50 | 44 | 5 | 1 | 21 | 19 | 8 | 3 | 0 | 0 | 17 | 43 | 3 |
| deborahwilson | 95 | 1,134 | 2025-06-02 15:14 | 2026-06-10 19:06 | 530 | 139 | 391 | 224 | 214 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 | 11 | 0 | 0 | 0 | 1 | 9 | 25 |
| ornellaavakian | 55 | 977 | 2024-12-05 23:13 | 2026-06-04 13:59 | 200 | 73 | 127 | 453 | 442 | 11 | 0 | 0 | 0 | 0 | 15 | 5 | 10 | 0 | 5 | 5 | 0 | 0 | 0 | 0 | 7 | 3 | 33 |
| bobulrich | 34 | 961 | 2024-12-02 15:32 | 2026-04-17 16:07 | 379 | 37 | 342 | 224 | 172 | 52 | 0 | 0 | 0 | 0 | 20 | 11 | 6 | 3 | 6 | 6 | 16 | 11 | 0 | 1 | 7 | 13 | 0 |
| remillardjess | 70 | 833 | 2025-10-09 13:25 | 2026-06-15 17:41 | 244 | 63 | 181 | 232 | 219 | 13 | 0 | 0 | 0 | 0 | 7 | 5 | 1 | 1 | 1 | 1 | 6 | 15 | 0 | 0 | 18 | 15 | 22 |
| pgould | 103 | 832 | 2024-11-11 16:10 | 2026-06-11 10:57 | 268 | 91 | 177 | 222 | 219 | 3 | 0 | 0 | 0 | 0 | 7 | 7 | 0 | 0 | 11 | 10 | 1 | 2 | 0 | 0 | 9 | 2 | 51 |
| nataliemurphy | 40 | 827 | 2026-01-07 16:35 | 2026-06-05 13:50 | 312 | 85 | 227 | 256 | 247 | 9 | 0 | 0 | 0 | 0 | 26 | 1 | 25 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 2 | 21 |
| careyyount | 69 | 772 | 2024-11-01 14:28 | 2025-05-29 15:39 | 344 | 90 | 254 | 175 | 174 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 23 | 22 | 1 | 0 | 0 | 0 | 0 | 11 | 21 |
| bethcousins | 26 | 726 | 2024-11-04 17:16 | 2026-06-08 17:25 | 122 | 24 | 98 | 190 | 184 | 6 | 0 | 0 | 0 | 0 | 7 | 5 | 2 | 0 | 17 | 11 | 8 | 5 | 0 | 0 | 1 | 9 | 6 |
| meenabowser | 66 | 716 | 2024-11-04 16:54 | 2026-03-21 07:11 | 212 | 58 | 154 | 119 | 118 | 1 | 0 | 0 | 0 | 0 | 33 | 22 | 11 | 0 | 23 | 23 | 2 | 48 | 0 | 0 | 4 | 7 | 0 |
| elizabrantley | 67 | 619 | 2024-11-05 09:37 | 2025-07-15 18:51 | 323 | 87 | 236 | 108 | 108 | 0 | 0 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 1 | 1 | 0 | 2 | 0 | 0 | 0 | 0 | 37 |
| chloelester | 50 | 310 | 2024-11-11 11:57 | 2025-07-10 13:42 | 15 | 3 | 12 | 58 | 45 | 13 | 0 | 0 | 0 | 0 | 5 | 1 | 4 | 0 | 62 | 61 | 0 | 7 | 0 | 1 | 0 | 0 | 0 |
| lisamcwilliams | 41 | 257 | 2025-01-09 12:33 | 2026-01-07 15:50 | 100 | 18 | 82 | 55 | 54 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 2 | 3 | 0 | 0 | 0 | 1 | 3 | 0 |
| alexsislopez | 12 | 250 | 2026-06-01 14:41 | 2026-06-15 19:37 | 148 | 28 | 120 | 45 | 45 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20 |
| andreacombet | 35 | 236 | 2024-11-13 10:15 | 2026-04-15 17:25 | 21 | 6 | 15 | 56 | 42 | 13 | 0 | 0 | 0 | 0 | 7 | 6 | 1 | 0 | 29 | 28 | 0 | 4 | 0 | 0 | 0 | 0 | 0 |
| sherrij | 31 | 164 | 2024-11-09 11:32 | 2026-04-16 10:20 | 45 | 17 | 28 | 58 | 58 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| leighjanko | 32 | 162 | 2024-11-13 20:45 | 2026-03-09 08:02 | 27 | 11 | 16 | 48 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 5 | 5 | 0 | 0 | 0 | 0 | 1 | 0 |
| richardpenna | 24 | 138 | 2025-03-05 13:21 | 2026-06-02 18:06 | 14 | 3 | 11 | 22 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 40 | 30 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kyla | 12 | 117 | 2025-09-23 15:48 | 2026-05-22 12:19 | 50 | 11 | 39 | 10 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kerrishay | 12 | 116 | 2024-11-05 08:40 | 2025-09-17 12:52 | 14 | 5 | 9 | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 50 | 50 | 2 | 1 | 0 | 0 | 0 | 1 | 0 |
| tracyleskauskas | 20 | 102 | 2025-01-17 19:37 | 2026-01-07 00:35 | 5 | 5 | 0 | 9 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 28 | 27 | 10 | 0 | 0 | 0 | 0 | 1 | 2 |
| royhinze | 30 | 94 | 2024-12-13 14:35 | 2026-02-11 15:11 | 17 | 14 | 3 | 6 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 1 | 0 |
| davidbartucci | 9 | 91 | 2024-11-04 16:28 | 2024-12-20 13:31 | 41 | 7 | 34 | 18 | 17 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 6 |
| mgamboa1 | 2 | 84 | 2025-10-08 17:30 | 2025-10-15 01:55 | 19 | 7 | 12 | 48 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| kristasonnier | 1 | 79 | 2025-05-21 09:26 | 2025-05-21 15:31 | 30 | 5 | 25 | 4 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 23 | 23 | 1 | 2 | 0 | 0 | 0 | 2 | 0 |
| juliapeterson | 5 | 46 | 2025-08-15 13:29 | 2026-04-18 14:14 | 1 | 1 | 0 | 4 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| annahudson | 5 | 44 | 2025-03-06 11:05 | 2026-02-25 09:55 | 10 | 3 | 7 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 13 | 13 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| kellyfox | 6 | 43 | 2024-11-08 13:50 | 2025-03-05 16:18 | 14 | 5 | 9 | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |
| swt | 8 | 38 | 2024-11-13 09:02 | 2025-06-18 06:27 | 0 | 0 | 0 | 10 | 0 | 10 | 0 | 0 | 0 | 0 | 2 | 1 | 1 | 0 | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| lujahfontaine | 5 | 32 | 2026-04-14 10:44 | 2026-05-21 13:07 | 7 | 3 | 4 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 0 |
| alexsislopez@gmail.com | 1 | 26 | 2026-06-01 14:33 | 2026-06-01 15:50 | 18 | 3 | 15 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 |
| troyhewett | 5 | 26 | 2024-11-06 13:23 | 2024-12-11 15:10 | 0 | 0 | 0 | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| janciecampbell | 3 | 21 | 2024-12-06 15:17 | 2025-11-10 00:53 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 11 | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| jonv | 7 | 16 | 2025-01-06 14:47 | 2026-01-06 14:55 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| brentsanders | 2 | 8 | 2026-02-26 16:45 | 2026-02-28 12:25 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| mridge | 1 | 6 | 2024-11-12 11:21 | 2024-11-12 12:54 | 0 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| brucew | 1 | 5 | 2026-05-22 12:05 | 2026-05-22 12:10 | 0 | 0 | 0 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| chuck-user | 2 | 4 | 2024-11-13 12:57 | 2025-06-27 22:26 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| shelbykramlich | 1 | 2 | 2024-11-05 16:06 | 2024-11-05 16:09 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| kylor_johnson | 1 | 2 | 2025-12-23 22:12 | 2025-12-23 22:14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cariegorkos | 1 | 1 | 2025-03-07 15:20 | 2025-03-07 15:20 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### Q-01_step2_results.md

# Q-01-S2 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-01-S2 — Rep Behavioral Scorecard — Step 2 (Orders)
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 43
- **Run date**: 2026-06-16


| rep_name | total_orders | total_gmv | avg_order_value | unique_customers |
| --- | --- | --- | --- | --- |
| Stacie Baker | 285 | $766,349 | $2,689 | 130 |
| CC Dallas Showroom | 407 | $725,284 | $1,782 | 206 |
| Rip Nance | 328 | $558,907 | $1,704 | 88 |
| Lesley Blair | 179 | $471,030 | $2,631 | 95 |
| Sandy Glosson | 235 | $433,574 | $1,845 | 67 |
| Carrie Haymore | 187 | $403,973 | $2,160 | 68 |
| Atlanta Showroom | 119 | $403,695 | $3,392 | 70 |
| Margarethe Martin | 159 | $365,244 | $2,297 | 63 |
| Stacey Chiavetta | 175 | $317,861 | $1,816 | 79 |
| Shephalli Jain | 104 | $307,042 | $2,952 | 76 |
| Kinshasa Floyd | 111 | $294,091 | $2,649 | 65 |
| Russ Jones | 131 | $280,757 | $2,143 | 64 |
| Michael  Mosko | 133 | $279,647 | $2,103 | 56 |
| Joanie Martin | 146 | $275,393 | $1,886 | 84 |
| Randy Gould | 121 | $264,577 | $2,187 | 53 |
| Mindy McEntire | 142 | $264,256 | $1,861 | 48 |
| Stewart Haviland | 130 | $249,771 | $1,921 | 73 |
| Betty Robbins | 81 | $225,411 | $2,783 | 56 |
| Rob Nance | 83 | $209,532 | $2,524 | 48 |
| Kristy Orison | 118 | $188,118 | $1,594 | 40 |
| Mary Miller | 108 | $160,572 | $1,487 | 37 |
| Patty Miller | 92 | $158,494 | $1,723 | 22 |
| Tanner Gould | 57 | $137,780 | $2,417 | 36 |
| Jodie Veeder | 66 | $135,271 | $2,050 | 42 |
| Highpoint Showroom | 13 | $83,644 | $6,434 | 10 |
| Nancy Hubbard | 31 | $60,789 | $1,961 | 23 |
| Lee Kram | 32 | $54,711 | $1,710 | 19 |
| Natalie Murphy | 22 | $45,466 | $2,067 | 16 |
| Penny Gould | 31 | $45,226 | $1,459 | 18 |
| Ornella Avakian | 18 | $44,828 | $2,490 | 12 |
| Deborah Wilson | 25 | $43,161 | $1,726 | 21 |
| Vivi Mira-Culmer | 11 | $42,599 | $3,873 | 10 |
| Kristin Ireland | 12 | $40,756 | $3,396 | 10 |
| Brigette Fontenot | 8 | $38,854 | $4,857 | 8 |
| Jess Remillard | 25 | $38,098 | $1,524 | 9 |
| Alexsis Lopez | 20 | $36,480 | $1,824 | 18 |
| Sandy Nakatsu | 4 | $33,186 | $8,296 | 4 |
| Beth Cousins | 4 | $24,824 | $6,206 | 4 |
| Tim Shelton | 12 | $23,287 | $1,941 | 10 |
| Cindy Rogers | 15 | $22,701 | $1,513 | 8 |
| Nicole Casanova | 1 | $2,039 | $2,039 | 1 |
| Eliza Brantley | 1 | $890 | $890 | 1 |
| Allan Otto | 1 | $594 | $594 | 1 |

### Q-04_results.md

# Q-04 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-04 — Non-Selling User Role Classification
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 76
- **Run date**: 2026-06-16


| username | days_active | total_events | submit_order | search_products | view_library_entry | library_emails | create_pdf_catalog | data_exports | access_sales_portal | my_list_activity | classified_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| staciebaker | 394 | 15,536 | 439 | 4,022 | 289 | 10 | 175 | 0 | 7 | 142 | Selling Rep |
| ripnance | 394 | 12,358 | 525 | 3,246 | 69 | 7 | 52 | 0 | 17 | 109 | Selling Rep |
| sglosson | 330 | 9,190 | 422 | 2,014 | 71 | 39 | 1 | 0 | 37 | 4 | Selling Rep |
| mindymcentire | 417 | 7,958 | 251 | 2,390 | 45 | 2 | 0 | 0 | 13 | 0 | Selling Rep |
| carriehaymore | 357 | 7,669 | 332 | 2,212 | 183 | 0 | 25 | 0 | 4 | 43 | Selling Rep |
| lesleyblair | 359 | 7,514 | 254 | 2,683 | 134 | 11 | 78 | 0 | 13 | 1 | Selling Rep |
| vivimiraculmer | 227 | 6,865 | 26 | 2,158 | 6 | 1 | 73 | 0 | 11 | 207 | Selling Rep |
| ccdallasshowroom | 315 | 6,617 | 540 | 1,434 | 108 | 9 | 20 | 0 | 9 | 1 | Selling Rep |
| stewhaviland | 335 | 6,563 | 241 | 1,576 | 114 | 50 | 14 | 0 | 10 | 139 | Selling Rep |
| rgould | 390 | 6,321 | 207 | 1,944 | 125 | 17 | 69 | 0 | 2 | 13 | Selling Rep |
| kinshasafloyd | 369 | 5,883 | 197 | 1,648 | 93 | 2 | 45 | 0 | 8 | 62 | Selling Rep |
| pattymiller | 304 | 5,288 | 158 | 732 | 9 | 0 | 36 | 0 | 7 | 0 | Selling Rep |
| timshelton | 401 | 5,211 | 24 | 700 | 14 | 4 | 5 | 0 | 7 | 0 | Selling Rep |
| russjones | 401 | 4,967 | 229 | 1,053 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| margarethemartin | 264 | 4,706 | 235 | 1,660 | 51 | 16 | 3 | 0 | 16 | 6 | Selling Rep |
| ccatlantashowroom | 198 | 4,110 | 132 | 735 | 126 | 47 | 31 | 0 | 37 | 67 | Selling Rep |
| sandynakatsu | 74 | 3,704 | 5 | 1,780 | 14 | 0 | 21 | 0 | 5 | 49 | Selling Rep |
| korison | 309 | 3,569 | 201 | 1,061 | 13 | 0 | 0 | 0 | 0 | 52 | Selling Rep |
| jodieveeder | 260 | 3,568 | 121 | 850 | 136 | 9 | 7 | 0 | 19 | 43 | Selling Rep |
| bettyrobbins | 189 | 3,385 | 131 | 631 | 72 | 4 | 2 | 0 | 16 | 0 | Selling Rep |
| staceychiavetta | 229 | 3,213 | 283 | 859 | 35 | 0 | 0 | 0 | 3 | 1 | Selling Rep |
| tannerg | 278 | 3,063 | 106 | 901 | 66 | 1 | 38 | 0 | 0 | 36 | Selling Rep |
| joaniemartin | 198 | 3,036 | 225 | 731 | 12 | 0 | 0 | 0 | 5 | 2 | Selling Rep |
| michaelmosko | 198 | 2,726 | 220 | 680 | 46 | 3 | 0 | 0 | 4 | 4 | Selling Rep |
| shephallijain | 180 | 2,653 | 222 | 825 | 1 | 0 | 35 | 0 | 8 | 12 | Selling Rep |
| marymiller | 163 | 2,640 | 201 | 389 | 7 | 0 | 0 | 0 | 5 | 0 | Selling Rep |
| cindyr | 299 | 2,556 | 24 | 805 | 57 | 46 | 22 | 0 | 4 | 28 | Selling Rep |
| robnance | 198 | 2,300 | 116 | 693 | 20 | 7 | 0 | 0 | 8 | 0 | Selling Rep |
| nicolecasanova | 83 | 1,701 | 1 | 1,050 | 18 | 1 | 0 | 0 | 1 | 0 | Sales Support/Inside Sales |
| leekram | 206 | 1,621 | 55 | 449 | 3 | 0 | 24 | 0 | 3 | 24 | Selling Rep |
| nancyhubbard | 203 | 1,613 | 49 | 111 | 226 | 249 | 0 | 0 | 0 | 0 | Selling Rep |
| brigettefontenot | 138 | 1,560 | 19 | 491 | 31 | 1 | 7 | 0 | 12 | 9 | Selling Rep |
| kristinireland | 67 | 1,436 | 18 | 122 | 0 | 0 | 12 | 0 | 0 | 80 | Selling Rep |
| cchighpointshowroom | 61 | 1,309 | 13 | 708 | 49 | 2 | 9 | 0 | 1 | 21 | Selling Rep |
| lorimccarver | 62 | 1,257 | 113 | 220 | 0 | 0 | 0 | 0 | 1 | 0 | Selling Rep |
| allanotto | 80 | 1,188 | 3 | 55 | 19 | 2 | 5 | 0 | 8 | 3 | Selling Rep |
| deborahwilson | 95 | 1,134 | 25 | 214 | 8 | 0 | 0 | 0 | 11 | 0 | Selling Rep |
| ornellaavakian | 55 | 977 | 33 | 442 | 5 | 0 | 10 | 0 | 0 | 0 | Selling Rep |
| bobulrich | 34 | 961 | 0 | 172 | 6 | 0 | 6 | 0 | 16 | 12 | Sales Support/Inside Sales |
| remillardjess | 70 | 833 | 22 | 219 | 1 | 0 | 1 | 0 | 6 | 15 | Selling Rep |
| pgould | 103 | 832 | 51 | 219 | 10 | 1 | 0 | 0 | 1 | 2 | Selling Rep |
| nataliemurphy | 40 | 827 | 21 | 247 | 0 | 0 | 25 | 0 | 1 | 0 | Selling Rep |
| careyyount | 69 | 772 | 21 | 174 | 22 | 1 | 0 | 0 | 1 | 0 | Selling Rep |
| bethcousins | 26 | 726 | 6 | 184 | 11 | 6 | 2 | 0 | 8 | 5 | Selling Rep |
| meenabowser | 66 | 716 | 0 | 118 | 23 | 0 | 11 | 0 | 2 | 48 | Sales Support/Inside Sales |
| elizabrantley | 67 | 619 | 37 | 108 | 1 | 0 | 0 | 0 | 0 | 2 | Selling Rep |
| chloelester | 50 | 310 | 0 | 45 | 61 | 1 | 4 | 0 | 0 | 8 | Low-Activity User |
| lisamcwilliams | 41 | 257 | 0 | 54 | 2 | 0 | 0 | 0 | 3 | 0 | Low-Activity User |
| alexsislopez | 12 | 250 | 20 | 45 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| andreacombet | 35 | 236 | 0 | 42 | 28 | 1 | 1 | 0 | 0 | 4 | Low-Activity User |
| sherrij | 31 | 164 | 0 | 58 | 0 | 0 | 0 | 0 | 0 | 0 | Low-Activity User |
| leighjanko | 32 | 162 | 0 | 48 | 5 | 3 | 0 | 0 | 5 | 0 | Low-Activity User |
| richardpenna | 24 | 138 | 0 | 22 | 30 | 10 | 0 | 0 | 0 | 0 | Inactive |
| kyla | 12 | 117 | 0 | 10 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kerrishay | 12 | 116 | 0 | 9 | 50 | 0 | 0 | 0 | 2 | 1 | Inactive |
| tracyleskauskas | 20 | 102 | 2 | 8 | 27 | 1 | 0 | 0 | 10 | 0 | Inactive |
| royhinze | 30 | 94 | 0 | 6 | 0 | 0 | 0 | 0 | 2 | 0 | Inactive |
| davidbartucci | 9 | 91 | 6 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| mgamboa1 | 2 | 84 | 0 | 48 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kristasonnier | 1 | 79 | 0 | 1 | 23 | 0 | 0 | 0 | 1 | 2 | Inactive |
| juliapeterson | 5 | 46 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| annahudson | 5 | 44 | 0 | 3 | 13 | 0 | 0 | 0 | 2 | 0 | Inactive |
| kellyfox | 6 | 43 | 3 | 15 | 0 | 0 | 0 | 0 | 0 | 0 | Selling Rep |
| swt | 8 | 38 | 0 | 0 | 4 | 1 | 1 | 0 | 1 | 0 | Inactive |
| lujahfontaine | 5 | 32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| troyhewett | 5 | 26 | 0 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | Inactive |
| alexsislopez@gmail.com | 1 | 26 | 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| janciecampbell | 3 | 21 | 0 | 1 | 9 | 2 | 0 | 0 | 0 | 0 | Inactive |
| jonv | 7 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | Inactive |
| brentsanders | 2 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| mridge | 1 | 6 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| brucew | 1 | 5 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| chuck-user | 2 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| kylor_johnson | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| shelbykramlich | 1 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |
| cariegorkos | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Inactive |

### Q-05_results.md

# Q-05 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-05 — Seat Utilization
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 1
- **Run date**: 2026-06-16


| active_org_users | logged_in_90d | ordering_users_90d |
| --- | --- | --- |
| 72 | 51 | 37 |

### Q-06_results.md

# Q-06 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-06 — Rep Engagement Trajectory
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 58
- **Run date**: 2026-06-16


| rep_name | logins_prev_90d | logins_current_90d | login_change_pct | orders_prev_90d | orders_current_90d | order_change_pct | gmv_current_90d |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CC Dallas Showroom | 110 | 89 | -19.10 | 81 | 106 | 30.90 | $199,791 |
| Stacie Baker | 81 | 116 | 43.20 | 66 | 77 | 16.70 | $158,715 |
| Stacey Chiavetta | 37 | 74 | 100 | 26 | 63 | 142.30 | $123,785 |
| Lesley Blair | 73 | 113 | 54.80 | 32 | 57 | 78.10 | $199,015 |
| Rip Nance | 122 | 146 | 19.70 | 84 | 56 | -33.30 | $107,908 |
| Sandy Glosson | 107 | 85 | -20.60 | 72 | 48 | -33.30 | $69,002 |
| Russ Jones | 103 | 109 | 5.80 | 27 | 43 | 59.30 | $134,030 |
| Joanie Martin | 24 | 46 | 91.70 | 23 | 38 | 65.20 | $72,448 |
| Shephalli Jain | 19 | 39 | 105.30 | 15 | 36 | 140 | $196,317 |
| Mindy McEntire | 139 | 126 | -9.40 | 26 | 36 | 38.50 | $58,088 |
| Kinshasa Floyd | 83 | 88 | 6 | 24 | 34 | 41.70 | $95,243 |
| Margarethe Martin | 58 | 38 | -34.50 | 48 | 33 | -31.30 | $66,627 |
| Stewart Haviland | 85 | 100 | 17.60 | 28 | 32 | 14.30 | $63,156 |
| Randy Gould | 132 | 137 | 3.80 | 25 | 32 | 28 | $61,785 |
| Michael  Mosko | 33 | 35 | 6.10 | 30 | 31 | 3.30 | $66,233 |
| Kristy Orison | 55 | 37 | -32.70 | 29 | 29 | 0 | $50,367 |
| Mary Miller | 21 | 25 | 19 | 27 | 29 | 7.40 | $40,132 |
| Carrie Haymore | 80 | 77 | -3.80 | 50 | 29 | -42 | $87,684 |
| Patty Miller | 43 | 58 | 34.90 | 13 | 28 | 115.40 | $60,892 |
| Atlanta Showroom | 72 | 71 | -1.40 | 36 | 23 | -36.10 | $93,804 |
| Rob Nance | 33 | 29 | -12.10 | 18 | 22 | 22.20 | $47,595 |
| Alexsis Lopez | 0 | 19 | — | 0 | 20 | — | $36,480 |
| Betty Robbins | 47 | 33 | -29.80 | 26 | 18 | -30.80 | $74,617 |
| Tanner Gould | 95 | 40 | -57.90 | 15 | 14 | -6.70 | $50,159 |
| Jess Remillard | 27 | 38 | 40.70 | 10 | 12 | 20 | $20,332 |
| Natalie Murphy | 28 | 16 | -42.90 | 11 | 11 | 0 | $27,952 |
| Lee Kram | 16 | 36 | 125 | 2 | 10 | 400 | $11,845 |
| Ornella Avakian | 7 | 10 | 42.90 | 0 | 10 | — | $20,524 |
| Jodie Veeder | 17 | 12 | -29.40 | 20 | 8 | -60 | $29,590 |
| Nancy Hubbard | 57 | 42 | -26.30 | 10 | 7 | -30 | $16,188 |
| Highpoint Showroom | 18 | 16 | -11.10 | 3 | 7 | 133.30 | $9,909 |
| Penny Gould | 17 | 10 | -41.20 | 5 | 5 | 0 | $2,900 |
| Brigette Fontenot | 15 | 36 | 140 | 1 | 5 | 400 | $20,672 |
| Deborah Wilson | 29 | 23 | -20.70 | 1 | 5 | 400 | $9,186 |
| Vivi Mira-Culmer | 37 | 56 | 51.40 | 1 | 5 | 400 | $10,980 |
| Tim Shelton | 115 | 106 | -7.80 | 5 | 2 | -60 | $980 |
| Beth Cousins | 9 | 5 | -44.40 | 2 | 2 | 0 | $14,406 |
| Kristin Ireland | 8 | 7 | -12.50 | 2 | 0 | -100 | $0 |
| Nicole Casanova | 11 | 11 | 0 | 1 | 0 | -100 | $0 |
| Sandy Nakatsu | 29 | 12 | -58.60 | 1 | 0 | -100 | $0 |
| Cindy Rogers | 83 | 52 | -37.30 | 6 | 0 | -100 | $0 |
| Bruce White | 0 | 1 | — | — | — | — | — |
| Brent Sanders | 3 | 0 | -100 | — | — | — | — |
| Kyla Bosch | 1 | 12 | 1,100 | — | — | — | — |
| Lujah Fontaine | 0 | 5 | — | — | — | — | — |
| Sherri Juhl | 2 | 1 | -50 | — | — | — | — |
| Meena Bowser | 7 | 1 | -85.70 | — | — | — | — |
| Allan Otto | 17 | 15 | -11.80 | — | — | — | — |
| Tracy Leskauskas | 1 | 0 | -100 | — | — | — | — |
| Anna Hudson | 2 | 0 | -100 | — | — | — | — |
| Bob Ulrich | 3 | 1 | -66.70 | — | — | — | — |
| Lisa McWilliams | 3 | 0 | -100 | — | — | — | — |
| Kylor  Johnson | 1 | 0 | -100 | — | — | — | — |
| Roy Hinze | 4 | 0 | -100 | — | — | — | — |
| Julia Peterson | 0 | 2 | — | — | — | — | — |
| Jon Vanderberg | 1 | 0 | -100 | — | — | — | — |
| Richard Pena | 4 | 5 | 25 | — | — | — | — |
| Andrea Combet | 6 | 1 | -83.30 | — | — | — | — |

### Q-43_step2_results.md

# Q-43-S2 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-43-S2 — Territory — eCat Order Activity
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### showroom_scan_results.md

# Showroom Scan Results — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-16
- **Total flagged**: 3
- **Aggregate GMV**: $1.2M

| Rep Name | Orders | GMV | Source | Classification |
| --- | --- | --- | --- | --- |
| CC Dallas Showroom | 407 | $725,284 | keyword | confirmed_operational |
| Atlanta Showroom | 119 | $403,695 | keyword | confirmed_operational |
| Highpoint Showroom | 13 | $83,644 | keyword | confirmed_operational |

**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.

### Q-51_results.md

# Q-51 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-51 — Rep-Level eCat Capture
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 25
- **Run date**: 2026-06-16


| rep_name | rep_number | erp_orders | erp_gmv | erp_customers | ecat_orders | ecat_gmv | ecat_customers | ecat_capture_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HOUSE ACCOUNT | HOUS | 17,183 | $13.1M | 115 | 0 | $0 | 0 | 0 |
| VIVI MIRA-CULMER | VIVI | 2,397 | $5.5M | 374 | 11 | $42,599 | 10 | 0.80 |
| BETTY ROBBINS | ROBB | 2,399 | $4.8M | 485 | 81 | $225,411 | 56 | 4.70 |
| STACIE BAKER | SBAK | 2,158 | $4.8M | 430 | 285 | $766,349 | 130 | 15.90 |
| RICHARD PENA | PENA | 2,039 | $4.2M | 657 | 0 | $0 | 0 | 0 |
| RIP NANCE JR | RIPJ | 1,925 | $3.7M | 289 | 0 | $0 | 0 | 0 |
| ROB NANCE | NANC | 1,525 | $3.3M | 388 | 83 | $209,532 | 48 | 6.40 |
| BRIGETTE FONTENOT | FONT | 1,509 | $3.2M | 312 | 8 | $38,854 | 8 | 1.20 |
| MARGARETHE MARTIN | MART | 1,579 | $3.0M | 282 | 159 | $365,244 | 63 | 12 |
| STEW HAVILAND | HAVI | 1,672 | $3.0M | 567 | 0 | $0 | 0 | 0 |
| JOANIE MARTIN | JMAR | 1,653 | $2.9M | 398 | 146 | $275,393 | 84 | 9.40 |
| KINSHASA FLOYD | KFLO | 1,915 | $2.8M | 240 | 111 | $294,091 | 65 | 10.50 |
| JODIE VEEDER | JVEE | 1,511 | $2.7M | 335 | 66 | $135,271 | 42 | 5 |
| TIMOTHY K SHELTON | SHEL | 1,351 | $2.7M | 316 | 0 | $0 | 0 | 0 |
| NICOLE CASANOVA | NCAS | 1,949 | $2.5M | 259 | 1 | $2,039 | 1 | 0.10 |
| STACEY CHIAVETTA | SCHI | 1,620 | $2.3M | 258 | 175 | $317,861 | 79 | 13.90 |
| RANDY GOULD | GOUL | 895 | $2.2M | 253 | 121 | $264,577 | 53 | 12 |
| LESLEY BLAIR | LBLA | 923 | $2.2M | 207 | 179 | $471,030 | 95 | 21.60 |
| MICHAEL MOSKO | MOSK | 1,179 | $2.0M | 238 | 0 | $0 | 0 | 0 |
| MINDY MCENTIRE | MMCE | 1,165 | $1.7M | 160 | 142 | $264,256 | 48 | 15.60 |
| KRISTY ORISON | KORI | 872 | $1.6M | 134 | 118 | $188,118 | 40 | 12 |
| KRISTIN IRELAND-SAVA | GLEN | 793 | $1.5M | 152 | 0 | $0 | 0 | 0 |
| ANDREA R COMBET | COMB | 2,243 | $1.5M | 18 | 0 | $0 | 0 | 0 |
| RUSS JONES | RJON | 981 | $1.2M | 139 | 131 | $280,757 | 64 | 23.80 |
| SANDY NAKATSU | SNAK | 786 | $1.1M | 97 | 4 | $33,186 | 4 | 3.10 |

### Q-62_results.md

# Q-62 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-62 — Product Launch Velocity by Rep
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep_name | new_items_sold | total_new_items | adoption_pct | customers_buying_new | new_item_qty | new_item_revenue | orders_with_new_items |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VIVI MIRA-CULMER | 175 | 369 | 47.40 | 48 | 398 | 257,050.30 | 71 |
| STACIE BAKER | 155 | 369 | 42 | 46 | 278 | 226,944.10 | 61 |
| RIP NANCE JR | 97 | 369 | 26.30 | 25 | 337 | 200,257.70 | 61 |
| BETTY ROBBINS | 100 | 369 | 27.10 | 45 | 170 | 135,327.84 | 54 |
| BRIGETTE FONTENOT | 71 | 369 | 19.20 | 29 | 184 | 114,974 | 39 |
| MARGARETHE MARTIN | 80 | 369 | 21.70 | 37 | 126 | 90,601.20 | 46 |
| JOANIE MARTIN | 90 | 369 | 24.40 | 35 | 144 | 82,114.40 | 37 |
| LESLEY BLAIR | 73 | 369 | 19.80 | 35 | 127 | 80,379.65 | 47 |
| ROB NANCE | 73 | 369 | 19.80 | 37 | 136 | 79,765.90 | 44 |
| RANDY GOULD | 92 | 369 | 24.90 | 18 | 170 | 79,510.98 | 26 |
| RICHARD PENA | 66 | 369 | 17.90 | 32 | 104 | 76,162.90 | 38 |
| STACEY CHIAVETTA | 51 | 369 | 13.80 | 24 | 77 | 63,818.20 | 29 |
| TIMOTHY K SHELTON | 79 | 369 | 21.40 | 29 | 125 | 61,796.56 | 37 |
| MELISSA DENTON | 42 | 369 | 11.40 | 13 | 54 | 60,685.20 | 16 |
| KINSHASA FLOYD | 80 | 369 | 21.70 | 23 | 121 | 60,593.59 | 30 |
| KRISTY ORISON | 67 | 369 | 18.20 | 12 | 83 | 51,529.55 | 14 |
| JODIE VEEDER | 63 | 369 | 17.10 | 18 | 92 | 51,041.83 | 20 |
| KRISTIN IRELAND-SAVA | 58 | 369 | 15.70 | 17 | 82 | 45,827.45 | 18 |
| RUSS JONES | 45 | 369 | 12.20 | 7 | 55 | 42,735 | 9 |
| CINDY ROGERS | 56 | 369 | 15.20 | 11 | 70 | 39,226.46 | 16 |

### Q-63_results.md

# Q-63 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-63 — Presentation-to-Order Conversion
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_engaged | total_presentations | total_orders | order_rate_pct | conversion_rate_pct | total_searches | total_catalogs | total_emails |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| staciebaker | 49 | 1,247 | 45 | 91.80 | 3.60 | 1,170 | 74 | 3 |
| vivimiraculmer | 17 | 646 | 3 | 17.60 | 0.50 | 634 | 12 | 0 |
| rgould | 23 | 511 | 22 | 95.70 | 4.30 | 484 | 21 | 6 |
| lesleyblair | 40 | 505 | 42 | 105 | 8.30 | 475 | 30 | 0 |
| ripnance | 31 | 399 | 33 | 106.50 | 8.30 | 388 | 8 | 3 |
| carriehaymore | 16 | 264 | 15 | 93.80 | 5.70 | 264 | 0 | 0 |
| kinshasafloyd | 19 | 236 | 25 | 131.60 | 10.60 | 226 | 10 | 0 |
| mindymcentire | 15 | 196 | 21 | 140 | 10.70 | 190 | 0 | 6 |
| stewhaviland | 12 | 189 | 7 | 58.30 | 3.70 | 175 | 12 | 2 |
| timshelton | 10 | 160 | 1 | 10 | 0.60 | 160 | 0 | 0 |
| russjones | 16 | 157 | 25 | 156.30 | 15.90 | 157 | 0 | 0 |
| shephallijain | 18 | 144 | 20 | 111.10 | 13.90 | 142 | 2 | 0 |
| staceychiavetta | 19 | 142 | 38 | 200 | 26.80 | 142 | 0 | 0 |
| ccdallasshowroom | 21 | 124 | 53 | 252.40 | 42.70 | 124 | 0 | 0 |
| sglosson | 15 | 124 | 32 | 213.30 | 25.80 | 121 | 0 | 3 |
| joaniemartin | 17 | 110 | 10 | 58.80 | 9.10 | 110 | 0 | 0 |
| michaelmosko | 11 | 106 | 17 | 154.50 | 16 | 105 | 0 | 1 |
| pattymiller | 14 | 103 | 25 | 178.60 | 24.30 | 98 | 5 | 0 |
| korison | 12 | 96 | 21 | 175 | 21.90 | 96 | 0 | 0 |
| tannerg | 6 | 93 | 6 | 100 | 6.50 | 92 | 1 | 0 |

### Q-64_results.md

# Q-64 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-64 — Rep Engagement vs Account Revenue
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | accounts_touched | avg_touches_per_account | avg_days_per_account | high_engagement_accounts | low_engagement_accounts |
| --- | --- | --- | --- | --- | --- |
| bethcousins | 3 | 61.70 | 1 | 3 | 0 |
| kristinireland | 4 | 39.30 | 1 | 2 | 0 |
| allanotto | 3 | 35.70 | 3.30 | 2 | 0 |
| staciebaker | 83 | 35.70 | 2 | 49 | 13 |
| vivimiraculmer | 38 | 32.30 | 1.40 | 15 | 12 |
| sandynakatsu | 4 | 30 | 2.50 | 2 | 2 |
| ripnance | 85 | 19.90 | 2.10 | 51 | 6 |
| meenabowser | 1 | 19 | 2 | 1 | 0 |
| kyla | 2 | 17.50 | 2.50 | 1 | 0 |
| brigettefontenot | 11 | 17 | 1.50 | 4 | 3 |
| cchighpointshowroom | 7 | 14.10 | 2.70 | 4 | 0 |
| carriehaymore | 44 | 13.60 | 1.70 | 22 | 8 |
| pattymiller | 25 | 13.10 | 2.90 | 12 | 7 |
| kinshasafloyd | 40 | 12.70 | 2 | 18 | 11 |
| marymiller | 21 | 12.70 | 2 | 16 | 1 |
| mindymcentire | 48 | 12.30 | 2.30 | 14 | 14 |
| lesleyblair | 75 | 12.20 | 1.80 | 34 | 8 |
| stewhaviland | 42 | 12.10 | 1.50 | 13 | 10 |
| korison | 23 | 12.10 | 2.40 | 11 | 3 |
| ccatlantashowroom | 21 | 11.20 | 1.70 | 5 | 7 |

### Q-65_results.md

# Q-65 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-65 — Selling vs Admin Time Ratio
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 20
- **Run date**: 2026-06-16


| rep | total_events | selling_events | admin_events | selling_pct | admin_pct |
| --- | --- | --- | --- | --- | --- |
| bobulrich | 50 | 46 | 4 | 92 | 8 |
| jodieveeder | 302 | 268 | 34 | 88.70 | 11.30 |
| alexsislopez@gmail.com | 26 | 23 | 3 | 88.50 | 11.50 |
| alexsislopez | 250 | 213 | 37 | 85.20 | 14.80 |
| sandynakatsu | 182 | 155 | 27 | 85.20 | 14.80 |
| joaniemartin | 588 | 479 | 109 | 81.50 | 18.50 |
| rgould | 1,198 | 973 | 225 | 81.20 | 18.80 |
| staceychiavetta | 675 | 545 | 130 | 80.70 | 19.30 |
| ccdallasshowroom | 1,055 | 846 | 209 | 80.20 | 19.80 |
| allanotto | 196 | 157 | 39 | 80.10 | 19.90 |
| lesleyblair | 1,843 | 1,467 | 376 | 79.60 | 20.40 |
| margarethemartin | 476 | 376 | 100 | 79 | 21 |
| marymiller | 316 | 249 | 67 | 78.80 | 21.20 |
| sglosson | 867 | 671 | 196 | 77.40 | 22.60 |
| nataliemurphy | 188 | 144 | 44 | 76.60 | 23.40 |
| carriehaymore | 897 | 685 | 212 | 76.40 | 23.60 |
| shephallijain | 598 | 453 | 145 | 75.80 | 24.20 |
| timshelton | 766 | 580 | 186 | 75.70 | 24.30 |
| kyla | 83 | 62 | 21 | 74.70 | 25.30 |
| tannerg | 328 | 242 | 86 | 73.80 | 26.20 |

### Q-70_results.md

# Q-70 Results — Currey & Company (cci, org_id=161)
- **Query**: Q-70 — Inactive Reps with Territory Revenue
- **Period**: LTM (2025-06-16 to 2026-06-16)
- **Row count**: 0
- **Run date**: 2026-06-16


*(No data returned)*

### user_group_mapping.md

# User Group Mapping — Currey & Company (cci, org_id=161)
- **Run date**: 2026-06-16
- **Total Postgres users**: 108
- **Matched to Mixpanel (Q-01 Step 1)**: 74 of 76 (97%)
- **Classification confidence**: LOW
- **Split available**: False

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
| --- | --- | --- |
| Sales Reps | field_rep | 47 |
| Sales Reps - Contract | field_rep | 17 |
| System Administrators | admin_internal | 14 |
| Showroom Managers | showroom | 10 |
| Account Executives | admin_internal | 6 |
| Order Entry Team | admin_internal | 5 |
| Account Executives | field_rep | 3 |
| Product Development & Design | admin_internal | 3 |
| Marketing Team | admin_internal | 1 |
| eOL Public Site | admin_internal | 1 |
| z-SuperCat | admin_internal | 1 |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
| --- | --- | --- | --- |
| field_rep | 55 | 159,602 | 91.5% |
| showroom | 8 | 12,589 | 7.2% |
| admin_internal | 11 | 2,297 | 1.3% |
