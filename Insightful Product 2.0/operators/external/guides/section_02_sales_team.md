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
