# Stage 1: Preflight, Queries & Cache

> This guide governs the data-gathering agent. You have MCP access to:
> - **Postgres**: `user-supercat-postgres-vpn`
> - **BigQuery**: `user-bigquery-admin`
>
> Your job: resolve org identity, determine report mode, run all preflight gates,
> execute all queries, compute derived gates, and write cache files.
> You do NOT generate any HTML or narrative.

---

## Read Chain

Read these files before executing any steps:

1. **`SKILL.md`** — data sources, MCP targets, schema notes, semantic guardrails
2. **`report-system/query_library.md`** — audited SQL reference for all queries (Q-01 through Q-45, Q-CL-*, Q-CI-*)
3. **This file** (`stage1_preflight_and_queries.md`) — execution logic, gates, cache format

Do **not** read at runtime:
- Section guides (`section_02_sales_team.md`, etc.) — those are for Stage 2
- `shared_rules.md` — that is for Stage 2/3/4
- `report-system/html_report_template.html` — that is for Stage 4
- `dependencies/PEER_BENCHMARK.md` — consumed by the §7 section builder, not Stage 1
- Gold reference HTML — that is for Stage 4

---

## MCP Failure & Resume Policy

MCP calls (Postgres `user-supercat-postgres-vpn`, BigQuery `user-bigquery-admin`) can fail mid-run — VPN drop, timeout, transient connection error. Handle failures deterministically so a run is always either complete or cleanly resumable. **Never fabricate, estimate, or carry forward stale data to cover a failed call.**

**The cache dir is the resume ledger.** A query is "done" only when its `cache/Q-*_results.md` exists with a complete header (query ID, org, period, row count, run date) and body. Treat a present-but-truncated or empty-bodied file as NOT done.

- **Empty result vs. failure.** A query that runs and returns 0 rows IS done — write the file with `Row count: 0`. A query that errors out is NOT done — do **not** write its file (a missing file is the signal to retry on resume). Never write a placeholder or empty Q file.
- **Per-query failure.** On a failed call: retry once. If it still fails, record the Q-ID and the error in `cache/_run_status.md` (see below), skip it, and continue with queries that do not depend on it. Do not abort the whole run for one independent query.
- **Dependency-aware skips.** If a failed query is a prerequisite for others (e.g., `Q-01_step1_results.md` feeds the user-group split; a gate-source query feeds a `HAS_*` flag), mark the dependents BLOCKED — do not compute a gate or derived value from missing data. A gate inferred from an absent query is a defect.
- **Connection-level failure.** If the VPN/MCP connection is unavailable at preflight (before any query succeeds), STOP and report `BLOCKED: MCP unavailable` — do not produce a partial cache.
- **Gate integrity.** Only write `cache/gate_flags.md` once every gate-source query has a complete result file (or a documented, mode-appropriate skip). If any primary gate's source is in the failed/blocked set, stop before writing `gate_flags.md` and report which Q-IDs are outstanding — **Stage 2-4 must never run on a partial gate set.**

**Resume.** Re-running this guide against the same `runs/{{shortname}}_{{YYYY-MM-DD}}/` is idempotent: for each query, if its complete cache file already exists, skip it; otherwise run it. Only the previously failed/missing Q-IDs are re-executed. After a resume clears all outstanding Q-IDs, compute derived gates and write `gate_flags.md` / `section_manifest.md` as normal.

**`cache/_run_status.md`** (written whenever any query fails or is skipped):
- Run status: `COMPLETE` | `PARTIAL — outstanding: {Q-IDs}` | `BLOCKED: {reason}`
- One row per failed/skipped Q-ID: `Q-ID · reason (timeout / connection / dependency-blocked / mode-skip) · retry attempted (y/n)`

When a later run brings status to `COMPLETE`, note it and proceed. This file is internal only — it never appears in the delivered report or Appendix.

---

## Stage 0: Minimum-Commerce Gate

Run this immediately after resolving org identity (§1.1). This gate determines the report mode. Once the mode is selected, it governs everything that follows — do not mix mode behavior.

### 0.1 Query LTM and all-time eCat and ERP order activity

```sql
-- LTM eCat orders
SELECT COUNT(*) AS ltm_ecat_orders
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at >= NOW() - INTERVAL '12 months';

-- LTM ERP orders
SELECT COUNT(*) AS ltm_erp_orders
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months';

-- All-time eCat orders (used for activation vs. reactivation routing)
SELECT COUNT(*) AS alltime_ecat_orders,
       MAX(created_at) AS last_ecat_order_date
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL);
```

### 0.2 Mode routing

| Condition | Mode |
|---|---|
| `ltm_ecat_orders > 0` OR `ltm_erp_orders > 0` | **Mode 1: Standard Intelligence Report** — continue to Stage 1 |
| Both = 0, AND `alltime_ecat_orders = 0` | **Mode 2: Platform Activation Report** — account has no commerce history |
| Both = 0, AND `alltime_ecat_orders > 0` | **Mode 3: Platform Reactivation Report** — account has lapsed |

**After Stage 0**: If Mode 2 or Mode 3, complete the mode-specific assembly below and save the report. **STOP.** Stages 1–4 of the staged pipeline apply only to Mode 1.

---

## Mode 2: Platform Activation Report (self-contained)

**Stop standard report generation.** Generate the Activation Report instead.

**Narrative**: The client is configured but has no eCat commerce history. The report surfaces platform readiness and what activation looks like — not commerce analysis that doesn't exist.

**Tone**: Constructive and forward-looking. "Here's what's ready. Here's what to activate first."

**Section assembly for activation mode** (follow this order, no others):

| # | Section | Behavior |
|---|---------|----------|
| 1 | Activation Summary | Replaces Executive Summary. See §0.4a below. |
| 2 | Platform Readiness | Platform configuration, catalog health, data freshness (from Q-08, Q-09, Q-10, Q-11). |
| 3 | Peer Benchmarking | Include if HAS_PEER_DATA = true. Frame as "how similar accounts have activated." |
| 4 | Appendix | Platform data sources, staleness disclosures, required Appendix note. |

**Sections to exclude entirely** (do not include, do not reference):
- §2 Sales Team Performance
- §3 Customer & Buyer Intelligence
- §4 Product & Inventory Intelligence
- §5 Commerce Analytics
- §6 Portal Engagement

**TOC strip**: Include only links to sections that are actually rendered.

**Header and badge**:
- Report type label: `Platform Activation Report`
- Report badge: `Activation Stage · No eCat Commerce History`

**Required disclosure note — render as a callout inside the Activation Summary section, NOT in the Appendix**:
> "This report reflects platform configuration and readiness context. Commerce sections are not included as no eCat ordering activity has been recorded for this account."
>
> The Appendix remains attribution-only in Mode 2. It contains only data source rows for sources actually used. Do not add mode explanation, omission rationale, or any non-attribution content to the Appendix.

### Activation Summary (replaces Executive Summary)

Write this last, after Platform Readiness and Peer Benchmarking are drafted.

Include:
- 3–4 highlights about what is configured and ready (catalog, product data, features)
- 1 highlight about peer context (if available) — how similar-stage accounts compare
- 1–2 Priority Actions focused on first activation steps (e.g., first rep training, first pilot buyer group)
- The period label should be "Platform Configuration as of {{REPORT_DATE}}" — not a trailing 12 months header, because there is no commerce period to report

Do not include:
- Any commerce figures (there are none)
- Health score
- Internal segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) anywhere — these must not appear even in Peer Benchmarking; in §7 describe the cohort in plain language derived from `peer_group_id_effective`

---

## Mode 3: Platform Reactivation Report (self-contained)

**Stop standard report generation.** Generate the Reactivation Report instead.

**Narrative**: The client used the platform before and went quiet. The report is honest about what lapsed, references historical context, surfaces what's still in place, and frames re-engagement clearly.

**Tone**: Direct, honest, constructive. "The platform was active. It went quiet. Here's the current state and what re-engagement looks like." Do not apologize for the gap. Do not manufacture urgency.

**Historical context query** (run before section assembly):

```sql
-- Last active period and all-time eCat GMV
SELECT
  COUNT(*) AS alltime_ecat_orders,
  ROUND(SUM(total)::numeric, 2) AS alltime_ecat_gmv,
  MAX(created_at)::date AS last_ecat_order_date,
  DATE_TRUNC('month', MAX(created_at))::date AS last_active_month
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL);
```

Use `last_active_month` to anchor the reactivation narrative ("Last eCat activity: [MONTH YEAR]").

### Mixpanel Order-Tracking Gap Check (Mode 3)

After running the historical context query above AND Q-22 (Feature Usage Depth), compare:
- **Postgres all-time eCat orders**: `alltime_ecat_orders` from the historical context query
- **Mixpanel Order Submission events**: `submit_order` from Q-22 results

If `alltime_ecat_orders > 0` AND Q-22 `submit_order = 0`, set `MIXPANEL_ORDER_TRACKING_GAP = true` in `gate_flags.md`.

Record in `gate_flags.md`:

| Flag | Value | Evidence |
|------|-------|----------|
| MIXPANEL_ORDER_TRACKING_GAP | true/false | Postgres all-time orders: N, Q-22 submit_order: M |

This check uses Q-22 (org-level feature usage from `mixpanel.org_feature_usage_report`) instead of Q-01 (per-user behavioral data) because Q-01 is gated on `HAS_SALES_SECTION` and does not run for Mode 3 accounts.

**Section assembly for reactivation mode** (follow this order, no others):

| # | Section | Behavior |
|---|---------|----------|
| 1 | Overview | Replaces Executive Summary. See §0.5a below. |
| 2 | Historical Commerce Context | Lightweight all-time context. See §0.5b below. |
| 3 | Platform Status | Platform configuration, catalog health, data freshness — with staleness emphasis. |
| 4 | Peer Benchmarking | Include if HAS_PEER_DATA = true. Add caveat: "Peer benchmarks reflect current platform use, not the lapsed period." |
| 5 | Appendix | Data sources, staleness disclosures, last-active date, required Appendix note. |

**Sections to exclude entirely** (do not include, do not reference):
- §2 Sales Team Performance
- §3 Customer & Buyer Intelligence (no LTM data)
- §4 Product & Inventory Intelligence (skip if inventory is stale >180 days)
- §5 Commerce Analytics (no LTM data)
- §6 Portal Engagement

**TOC strip**: Include only links to sections that are actually rendered.

**Header and badge**:
- Report type label: `Partnership Overview`
- Report badge: `Partnership Overview · Platform Configuration as of {{REPORT_DATE}}`

**Required disclosure note — render as a callout inside the Overview section, NOT in the Appendix**:
> "This report reflects platform configuration and historical activity context. Commerce sections are not included as no eCat ordering activity has been recorded in the trailing 12 months. Last recorded eCat activity: [DATE]."
>
> The Appendix remains attribution-only in Mode 3. It contains only data source rows for sources actually used. Do not add mode explanation, omission rationale, or any non-attribution content to the Appendix.

**Staleness handling in reactivation mode**: Core data entities often go stale for lapsed accounts. In Platform Status:
- Apply the 3-label freshness scale (Fresh / Monitor / Stale) from Q-08 as normal
- If products, inventories, or customers are Stale (>180 days): call this out explicitly in the Overview — refreshing stale catalog data is a prerequisite for re-engagement
- If inventory is Stale (>180 days): do not include Product & Inventory section even if `HAS_INVENTORY = true`

**Mixpanel order-tracking gap handling in reactivation mode**: If `MIXPANEL_ORDER_TRACKING_GAP = true` (set by the Mode 3 gap check above), apply the handling rules from `section_08_platform.md` when building Platform Status:
- Remove the "Order Submission" row from Q-22 feature usage — do not display "0"
- Do not frame order submission as absent or characterize the platform as non-transactional
- The Historical Commerce Context section already uses Postgres data (all-time eCat orders, GMV) — ensure Platform Status does not contradict it

**Mixpanel order-tracking gap handling in peer benchmarking**: If `MIXPANEL_ORDER_TRACKING_GAP = true`, apply the order submission gap guardrail from `section_07_peer.md` subsection 4 when building the "What Top Performers Do" narrative. Frame order submission as maintaining or resuming activity, not as a new behavior to adopt. The Historical Commerce Context section establishes that this account has placed orders — peer narratives must not contradict that.

### Overview (replaces Executive Summary)

Write this last, after Historical Commerce Context and Platform Status are drafted.

Include:
- 1 highlight: last-active period and all-time eCat context ("As of [DATE], no eCat orders have been placed in the past 12 months. The account last recorded activity in [LAST ACTIVE MONTH].")
- 1–2 highlights: current platform state (what's configured, what's stale, what needs refresh)
- 1 highlight about peer context (if available)
- 1–2 Priority Actions focused on re-engagement steps (e.g., data refresh, rep re-training, pilot buyer outreach)
- The period label should be "Platform Status as of {{REPORT_DATE}}" plus "Last active: [LAST ACTIVE MONTH]"

Do not include:
- LTM commerce figures (there are none)
- Health score
- Internal segment labels (Platform-Embedded, Commerce-Active, Catalog-Focused) anywhere — these must not appear even in Peer Benchmarking; in §7 describe the cohort in plain language derived from `peer_group_id_effective`

### Historical Commerce Context (lightweight — reactivation mode only)

This section provides honest historical context without manufacturing analysis from absent data.

Include only:
- All-time eCat order count
- All-time eCat GMV (mark as `[HISTORICAL — all-time through last active date]`)
- Last active period (month/year of last eCat order)
- A brief note on what channel(s) were used (iPad / server), if determinable from all-time data

Do not include:
- LTM figures (they are zero — state this once; do not repeat)
- Monthly trends (no LTM period to trend)
- Rep-level figures (not in scope without LTM context)
- Any analysis implying current commerce activity

Format: 2–4 metric cards with clear source labels, plus 1–2 sentences of context. No large tables.

---

## Stage 1: Preflight — Configuration & Data Availability

Before running any queries, resolve the full configuration and data availability picture.

### 1.1 Resolve org identity

```sql
-- Get org_id by shortname or client name
SELECT id, shortname, name, created_at
FROM organizations
WHERE shortname = '{{ORG_SHORTNAME}}'
   OR name ILIKE '%{{CLIENT_NAME}}%'
LIMIT 5;
```

Confirm: `ORG_ID` (integer) and `ORG_SHORTNAME` (string) are known.

### 1.2 Check product flags (BigQuery `org_summary`)

```sql
-- MCP target: user-bigquery-admin   (migrated 2026-06-03 from user-bigquery-vpn)
-- Dataset: supercat-data-pipeline.insightful_product
-- Schema note (audited 2026-06-03): org_summary keys on org_shortname (there is NO org_id),
-- and has_cart/has_portal/has_cpq are NOT columns — derive them from recurring_services (below).
-- This mirrors query_library.md Q-PC-01, the authoritative preflight query.
SELECT
  org_shortname,
  org_name,
  has_clicky_portal AS has_clicky,
  clicky_prefix,
  recurring_services,
  order_configured_item
FROM `supercat-data-pipeline.insightful_product.org_summary`
WHERE org_shortname = '{{ORG_SHORTNAME}}'
LIMIT 1;
```

Set these gate flags (org_summary has no boolean `has_cart`/`has_portal`/`has_cpq` columns — derive from `recurring_services`, per query_library Q-PC-01):
- `HAS_CLICKY` — gates Portal Engagement section (binary: absent if false); from the `has_clicky_portal` column
- `HAS_CART` — `recurring_services` contains `B2B Cart` (confirm with server order count > 0); gates eCat Online channel column in Commerce Analytics
- `HAS_PORTAL` / `HAS_PORTAL_ORDERS` — `recurring_services` contains `Portal`; gates ERP total-business context and VM-45
- `HAS_CPQ` — `recurring_services` contains `Configurable` OR `order_configured_item > 0`; gates CPQ-specific content (not relevant to Phase 1 external VMs)

**If HAS_CLICKY = true — resolve `CLICKY_PREFIX` now:**

```sql
-- MCP target: user-bigquery-admin
-- List Clicky tables for this org. The prefix is the part before '_daily_metrics'.
-- Convention: typically matches org shortname (e.g., 'sccon', 'ali') but may differ.
-- INFORMATION_SCHEMA is supported on admin (unlike the old Windmill/vpn connection).
SELECT table_name
FROM `supercat-data-pipeline.clicky_analytics.INFORMATION_SCHEMA.TABLES`
WHERE table_name LIKE '%_daily_metrics'
ORDER BY table_name;
```

Match the returned table name to the org. Set `CLICKY_PREFIX` to the prefix portion (e.g., if the table is `sccon_ecat_online_daily_metrics`, the prefix is `sccon_ecat_online`). If no table matches the org shortname, check for partial matches or confirm with the person who set up the Clicky integration. Do not proceed with Clicky queries until `CLICKY_PREFIX` is confirmed.

### 1.3 Check data presence (Postgres)

Run these targeted checks against `user-supercat-postgres-vpn`:

```sql
-- Does this org have any submitted eCat orders?
SELECT COUNT(*) AS order_count
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at >= NOW() - INTERVAL '12 months';

-- Does this org have inventory data?
SELECT COUNT(*) AS inventory_count
FROM inventories
WHERE organization_id = {{ORG_ID}};

-- Does this org have portal_orders (ERP-synced)?
SELECT COUNT(*) AS portal_order_count
FROM portal_orders
WHERE organization_id = {{ORG_ID}}
  AND order_date >= NOW() - INTERVAL '12 months';

-- Does this org have sales_data?
SELECT COUNT(*) AS sales_data_count
FROM sales_data
WHERE organization_id = {{ORG_ID}};
```

Set:
- `HAS_INVENTORY` — true if inventory_count > 0
- `HAS_SALES_DATA` — true if sales_data_count > 0
- Override `HAS_PORTAL_ORDERS` to false if portal_order_count = 0 regardless of org_summary flag

**Validation log diagnostic**: If `org_summary` reports `has_portal = true` but the §1.3 LTM `portal_order_count = 0`, record in the validation log: "portal_orders entity exists but LTM count = 0 — HAS_PORTAL_ORDERS overridden to false. Q-16 and VM-45 skipped." This note does not appear in the delivered report or Appendix — it is an internal diagnostic only.

> **Enrollment excluded**: VM-15 and VM-44 (enrollment funnel and onboarding velocity) are intentionally out of scope for the external report. Do not query `enrollment_applicants` as part of this operator.

### 1.4 Check peer benchmark availability

Check whether a peer benchmark output file exists for this org:
- Look for `peer_benchmark_YYYY-MM-DD.csv` in the `reports/` directory (or the location where the Peer Benchmark system writes its outputs, per `SuperCat 4.0/Peer Benchmark/`)
- OR query BigQuery peer benchmark table if pipeline has run

Set:
- `HAS_PEER_DATA` — true if peer file present AND not stale (>90 days old)
- `BENCHMARK_ELIGIBLE` — from `benchmark_eligible` column in the benchmark CSV (boolean)
- `PEER_GROUP_N` — from `peer_group_n` column (**internal use only** — calibrates plain-language framing strength; never exposed as a literal number in client-facing output)
- `PEER_GROUP_ID_EFFECTIVE` — from `peer_group_id_effective` column (source value for building plain-language cohort framing in §7; never exposed as a raw label in client-facing prose)
- `BENCHMARK_CONFIDENCE` — from `benchmark_confidence` column (**internal use only** — governs section inclusion and plain-language phrasing calibration; never surfaces as a label in client output)
- `PEER_GROUP_LEVEL` — from `peer_group_level` column (**internal use only** — used for gating and framing decisions; never surfaces externally)

### 1.5 Determine active selling reps (Sales Team Performance gate)

```sql
SELECT COUNT(DISTINCT COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))) AS qualifying_reps
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND order_source = 'ipad'
  AND created_at >= NOW() - INTERVAL '12 months'
GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))
HAVING COUNT(*) >= 10;
```

Set:
- `HAS_SALES_SECTION` — true if the count of qualifying reps >= 5, false otherwise
- If false, omit the Sales Team section silently — no note in delivered report.

---

## Stage 2: Query Execution Plan

Based on Stage 1 flags, determine which queries to run. **For each query, consult `report-system/query_library.md` for the exact SQL.** This section specifies WHICH queries to run based on gates — the query library specifies HOW.

### 2.1 Always-run queries

These run for all orgs regardless of flags:

| Query ID | Description | Output Used In |
|----------|-------------|----------------|
| Q-07 | Catalog completeness | §4 Product, §8 Platform |
| Q-08 | Data freshness (last updated per entity type) | §8 Platform |
| Q-09 | Import pipeline health | §8 Platform |
| Q-10 | Catalog completeness | §8 Platform |
| Q-11 | Configuration completeness | §8 Platform |
| Q-12 | Customer activation network health | §3 Customers |
| Q-13 | Customer concentration risk (top-buyer eCat GMV share) | §5 Commerce |
| Q-14 | Reorder velocity / early warning | §3 Customers |
| Q-17 | Dormant high-value buyers | §3 Customers |
| Q-18 | eCat order trend (Part A — eCat-only if no portal_orders) | §5 Commerce |
| Q-20 | AOV by order segment | §5 Commerce |
| Q-21 | Order type & workflow | §5 Commerce |
| Q-41 | New eCat buyer acquisition | §3 Customers |
| Q-22 | Feature usage depth | §8 Platform |

### 2.2 Conditional queries (run only if gate = true)

| Query ID | Gate | Description | Section |
|----------|------|-------------|---------|
| Q-01 | HAS_SALES_SECTION | Rep activity leaderboard (Postgres orders) + per-user behavioral data (BigQuery Mixpanel `user_feature_usage_report`) — both steps required, see query library Q-01 Steps 1 & 2 | §2 Sales |
| Q-06 | HAS_SALES_SECTION | Rep engagement trajectory | §2 Sales |
| Q-43 | HAS_SALES_SECTION | Territory coverage & dormancy | §2 Sales |
| Q-16 | HAS_PORTAL_ORDERS | ERP total business visibility | §5 Commerce |
| Q-18 Part B | HAS_PORTAL_ORDERS | eCat share of total business trend | §5 Commerce |
| Q-45 | HAS_PORTAL_ORDERS **+ denominator validity gate** | eCat capture rate | §5 Commerce |
| Q-37 | HAS_INVENTORY AND HAS_SALES_DATA | OOS top sellers | §4 Product |
| Q-39 | HAS_SALES_DATA | Line analysis by category & collection | §4 Product |
| Q-42 | HAS_SALES_DATA | New introduction performance | §4 Product |
| Q-38a | portal_order_items confirmed present | Product velocity trend | §4 Product |
| Q-40 | Always (eCat orders) | Geographic distribution | §3 Customers |
| Q-CL-01 | HAS_CLICKY | Portal traffic trend | §6 Portal |
| Q-CL-03 | HAS_CLICKY | Geographic portal demand | §6 Portal |
| Q-CL-05 | HAS_CLICKY | Traffic sources | §6 Portal |
| Q-CI-03 | HAS_PEER_DATA | Feature adoption benchmarking | §7 Peer |
| Q-CI-05 | HAS_PEER_DATA | Top-performer patterns | §7 Peer |

### 2.2a Stage 2 derivations (NOT run by Stage 1)

These are derived from Q-01 behavioral data by the §2 section builder during Stage 2 — they are NOT standalone SQL queries. Stage 1 does not produce cache files for them. The §2 builder reads Q-01 Step 1 results + the derivation rules from `report-system/query_library.md` and applies the classification inline.

| Query ID | Derived From | Description | Consumer |
|----------|-------------|-------------|----------|
| Q-02 | Q-01 Step 1 | Selling archetype classification (behavioral ratio rules) | §2 subsection 3 |
| Q-03 | Q-01 Step 1 | Behavioral funnel gap analysis (dimensional score ratios) | §2 subsections 2, 4 |

Do not attempt to run Q-02 or Q-03 as SQL queries — they have no SQL. Do not produce Q-02_results.md or Q-03_results.md cache files.

### 2.3 Queries not to run (pending or internal-only)

Do not attempt to run these — mark sections as pending:

| Query ID | Reason | VM Affected |
|----------|--------|-------------|
| Q-38b | `pending_engineering` — no `invoice_date` in `sales_data` | VM-38b |
| VM-27 queries | `internal_only` — health score | VM-27 |
| VM-29 queries | `internal_only` — churn risk | VM-29 |
| VM-28 queries | `internal_only` — expansion readiness | VM-28 |
| VM-36 queries | `internal_only` — portal traffic decline signal | VM-36 |
| VM-48 queries | `internal_only` — HubSpot expansion signals | VM-48 |
| Q-CI-04 | `pending` — requires 2+ monthly peer benchmark snapshots. Target: May 2026 | VM-CI-04 (§7 Growth Trajectory) |

---

## Stage 3: Data Validation

For each query result, validate before caching:

1. **Null check**: If a query returns zero rows or all-null totals for a core required field, do not surface that section. Omit silently — no note in the delivered report.
2. **Semantic check**: Confirm that `portal_orders` results are never framed as buyer activity. Confirm `order_source` attribution is correct (iPad ≠ server).
3. **Inventory snapshot caveat**: If using inventory data, confirm this is a point-in-time snapshot — we cannot know how long items have been OOS.
4. **Portal_orders framing check**: Before writing any ERP total-business context, confirm you are using only allowed framing from `query_library.md` global guardrails.
5. **Rep name normalization** (apply to Q-01 Step 2 results AND showroom scan results BEFORE writing cache files):
   - **Collapse whitespace**: Replace all consecutive whitespace (double-spaces, tabs, etc.) with a single space. Trim leading/trailing whitespace. Example: `"Lynn  Ross"` → `"Lynn Ross"`, `"Mark  Holliday  "` → `"Mark Holliday"`.
   - **Case-insensitive dedup**: After whitespace normalization, group rows by `LOWER(rep_name)`. If two or more rows resolve to the same name (e.g., `"Lorraine Hayes"` and `"lorraine hayes"`), merge them into a single row: sum `total_orders` and `total_gmv`, take `MAX(unique_customers)`, recalculate `avg_order_value` as `total_gmv / total_orders`. Use the title-cased version of the name (first letter of each word capitalized) as the canonical display name.
   - **Mangled-name merge**: If a rep name contains ` - ` followed by text that looks like a middle segment from a CRM artifact (e.g., `"Jessica - Ricci sales Mason"` alongside a clean `"Jessica Mason"`), merge the mangled entry into the clean entry using the same sum/recalculate rules above. Flag the merge in the validation log: `"Merged mangled rep name: [original] → [canonical]"`.
   - **Write order**: Apply normalization BEFORE writing `Q-01_step2_results.md`. The cache file should contain only canonical, deduplicated names.

---

## Derived Gate Computation

> *Consolidated from v2 operator §4.2 (showroom scan) and §4.5 (VM-45 denominator gate). These rules exist in the v2 operator as part of section assembly — they are moved here so Stage 1 pre-computes them. The rules themselves are unchanged.*

Section agents consume pre-computed booleans from `gate_flags.md` — they never re-derive gates from raw query data. All derived gates MUST be resolved in Stage 1.

### 1. VM-45 Denominator Gate (source: v2 operator §4.5)

Compute LTM eCat GMV (from `orders`) and LTM ERP GMV (from `portal_orders`) separately, then apply:

- **Gate 1**: `portal_orders_gmv > ecat_gmv` — if eCat GMV equals or exceeds ERP GMV, the ERP sync is partial (the denominator is a subset, not total business). Skip Q-45.
- **Gate 2**: `ecat_gmv >= 0.05 × portal_orders_gmv` — if eCat is less than 5% of ERP total, the capture rate is not interpretable. Skip Q-45.

Set:
- `VM45_GATE_1` — PASS / FAIL
- `VM45_GATE_2` — PASS / FAIL
- `VM45_RENDER` — true only when **both gates pass**. If either gate fails, record the skip reason in the validation log (not in the delivered report).

### 2. Showroom / Operational Account Scan (source: v2 operator §4.2)

Run before the rep leaderboard data is cached. Two-pass scan:

**Pass 1 — keyword scan:**

```sql
SELECT
  COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name,
  COUNT(*) AS order_count,
  ROUND(SUM(total)::numeric, 2) AS gmv
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at >= NOW() - INTERVAL '12 months'
  AND (
    rep_first_name ILIKE '%showroom%'
    OR rep_last_name ILIKE '%showroom%'
    OR rep_first_name ILIKE '%admin%'
    OR rep_first_name ILIKE '%marketing%'
    OR rep_first_name ILIKE '%training%'
    OR rep_first_name ILIKE '%test%'
    OR rep_first_name ILIKE '%demo%'
    OR rep_first_name ILIKE '%market helper%'
    OR rep_last_name ILIKE '%market helper%'
    OR rep_first_name ILIKE '%helper%'
    OR rep_first_name ILIKE '%office%'
    OR rep_last_name ILIKE '%office%'
  )
GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))
ORDER BY gmv DESC;
```

**Pass 1b — non-person entity scan (catches company/org names used as rep identities):**

After Pass 1 results are collected, run this additional check across ALL rep names from Q-01 Step 2 results. Flag any `rep_name` where:
- The name contains "Company", "Corp", "Inc", "LLC", "Ltd", "Associates", "Group", "Interiors", "Furniture", "Lighting", or "& " (ampersand followed by space)
- The name matches a pattern like `{{BRAND_NAME}}[0-9]+` (numbered corporate accounts, e.g., "Visual Comfort1", "Visual Comfort5")
- The name has no space (single-word name that is not a plausible first name) AND `total_orders < 10`

For each flagged name, classify as:
- **Confirmed operational** — if the name clearly is not a person (e.g., "The Walfab Company", "Ashley Interiors", "Market Helper 1") AND has corroborating evidence (low unique_customers, non-person naming pattern). Exclude from rep leaderboard.
- **Ambiguous — flagged for CSM review** — if the name could be a multi-line rep agency (e.g., "Dunn Lighting", "Martha Graham & Associates Office"). Include in leaderboard but record the flag in `showroom_scan_results.md`.

Record all flagged names in `showroom_scan_results.md` with classification and reasoning.

**Pass 2 — brand-name showroom scan (catches patterns like "PALECEK SAN FRANCISCO"):**

```sql
SELECT
  COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name,
  COUNT(*) AS order_count,
  ROUND(SUM(total)::numeric, 2) AS gmv
FROM orders
WHERE organization_id = {{ORG_ID}}
  AND is_submitted = true
  AND (is_marked_deleted = false OR is_marked_deleted IS NULL)
  AND created_at >= NOW() - INTERVAL '12 months'
  AND rep_first_name ILIKE '%{{ORG_BRAND_NAME}}%'
GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text))
ORDER BY gmv DESC;
```

Replace `{{ORG_BRAND_NAME}}` with the org's primary brand name (typically the org name, not the shortname — e.g., `PALECEK` for org `pf`). Review results manually: if `rep_last_name` contains a city, location, or physical venue (e.g., "SAN FRANCISCO", "DALLAS", "LOS ANGELES", "DESIGN CENTER"), treat as a showroom record.

**Classification rules** (apply to matching accounts from either pass):
- **Include** in total org eCat GMV (these are real orders)
- **Exclude** from individual rep leaderboard and archetype analysis only when corroborating evidence exists beyond the name pattern (e.g., city/location string in last name, no individual contact, shared-location account pattern). Name alone is insufficient — classify as "ambiguous — flagged for CSM review" if no corroborating signal exists.
- **Record** in the validation log — account name, GMV, order count, and the specific evidence that confirmed operational status.

Write results to `cache/showroom_scan_results.md`.

Set `SHOWROOM_EXCLUSIONS` = count of confirmed excluded accounts in `gate_flags.md`.

### 3. Mixpanel User Data Check (source: v2 operator §4.2 Mixpanel dependency note)

After running Q-01 Step 1 (BigQuery `user_feature_usage_report`), check if it returned rows.

Set:
- `MIXPANEL_USER_DATA_PRESENT` — true if Q-01 Step 1 returned > 0 rows, false otherwise
- `QUALIFYING_REP_COUNT` — the count of qualifying reps from §1.5 results

### 4. Mixpanel Order-Tracking Gap Check

After running Q-01 Step 1 (Mixpanel) and Q-01 Step 2 (Postgres), compare:
- **Postgres iPad orders LTM**: total row count from Q-01 Step 2 (`SUM(total_orders)` across all reps)
- **Mixpanel submit_order total**: `SUM(submit_order)` across all users from Q-01 Step 1

If **Postgres iPad orders > 0** AND **Mixpanel total submit_order = 0** (every single user has `submit_order = 0`), this indicates Mixpanel is not tracking iPad order submissions for this org. The behavioral scorecards will show zero ordering activity for all users, which is misleading alongside their actual Postgres orders.

Set:
- `MIXPANEL_ORDER_TRACKING_GAP` — true if Postgres orders > 0 but org-wide Mixpanel submit_order = 0, false otherwise

Record in `gate_flags.md`:

| Flag | Value | Evidence |
|------|-------|----------|
| MIXPANEL_ORDER_TRACKING_GAP | true/false | Postgres LTM orders: N, Mixpanel total submit_order: M |

**Impact on downstream sections**: When `MIXPANEL_ORDER_TRACKING_GAP = true`:
- §2 Sales Team: Archetype classification (Q-02) should NOT use `submit_order` as a signal — it will be zero for all reps regardless of actual ordering behavior. The section builder should note this in the fragment.
- §8 Platform: Feature adoption metrics should caveat that order submission events are not tracked via Mixpanel for this org. Postgres order data is the authoritative source.

**Fallback when Q-01 is not available**: If `HAS_SALES_SECTION = false` and Q-01 was skipped, use Q-22 as the Mixpanel source instead:
- **Postgres orders**: LTM eCat orders from §1.3 data presence check (or `alltime_ecat_orders` for Mode 3)
- **Mixpanel submit_order**: `submit_order` value from Q-22 results (org-level, all-time)

If Postgres orders > 0 AND Q-22 `submit_order = 0`, set `MIXPANEL_ORDER_TRACKING_GAP = true`. Record both values as evidence.

This fallback ensures the gap is detected regardless of whether Q-01 ran. For Mode 3, the dedicated check in the Mode 3 block (Mixpanel Order-Tracking Gap Check) takes precedence.

### 5. Platform Activity Composition (User Group Mapping)

Query the admin console's user group assignments to build a reliable mapping between Mixpanel usernames and user classification. This enables §8 to display an aggregate split of platform activity between field reps and showroom/operational accounts.

**Query** (run against `user-supercat-postgres-vpn`):

```sql
SELECT
  u.username,
  u.first_name,
  u.last_name,
  ut.name       AS user_group,
  ut.show_mode,
  ut.primary_rep_group,
  ou.is_admin
FROM org_users ou
JOIN users u    ON u.id = ou.user_id
JOIN user_types ut ON ut.id = ou.user_type_id
WHERE ou.organization_id = {{ORG_ID}}
ORDER BY ut.name, u.username;
```

**Classification rules** — for each `user_group` name, assign exactly one bucket:

| Bucket | Matching signals (any one is sufficient) |
|--------|------------------------------------------|
| **field_rep** | Group name contains "Sales Rep", "Reps", "Account Executive", "Rep " (trailing space), "Sales" (case-insensitive, but NOT if the name also contains "Showroom"), or `primary_rep_group = true` |
| **showroom** | Group name contains "Showroom" (case-insensitive) |
| **admin_internal** | Group name contains "Admin", "SuperCat", "Internal", "Customer Service", "IT Staff", "eCat Online", "Public Site", "Marketing", "Order Entry", "Product Development", or `is_admin = true` |
| **other** | Does not match any pattern above |

If a user's group matches multiple buckets, apply this priority: showroom > admin_internal > field_rep > other.

**Confidence gate** — compute these metrics after classification:

1. `join_rate` = (count of Q-01 Step 1 usernames that match a `username` in the mapping) / (total Q-01 Step 1 rows). Use case-insensitive matching.
2. `ambiguous_rate` = (count of users whose group classified as `other`) / (total matched users).
3. `showroom_event_share` = (sum of `total_events` from Q-01 Step 1 for users classified as `showroom` or `admin_internal`) / (sum of `total_events` for all matched users).

Set in `gate_flags.md`:

| Flag | Value | Evidence |
|------|-------|----------|
| USER_GROUP_SPLIT_AVAILABLE | true/false | See conditions below |
| USER_GROUP_JOIN_RATE | X% | N of M Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | X% | Showroom+admin share of matched events |

`USER_GROUP_SPLIT_AVAILABLE = true` ONLY when ALL of these hold:
- `join_rate >= 0.90` (≥90% of Mixpanel users matched to a Postgres user group)
- `ambiguous_rate = 0` (zero users landed in the `other` bucket)
- `showroom_event_share >= 0.10` (showroom+admin accounts contribute ≥10% of events — otherwise the split adds no value)

If ANY condition fails, set `USER_GROUP_SPLIT_AVAILABLE = false`. The §8 builder will skip the split and render the section identically to the current behavior. No trace of the failed gate appears in the delivered report.

**Cache output**: Write results to `cache/user_group_mapping.md` with this format:

```markdown
# User Group Mapping — {{CLIENT_NAME}} ({{shortname}}, org_id={{ORG_ID}})
- **Run date**: {{YYYY-MM-DD}}
- **Total Postgres users (all, including disabled)**: N
- **Matched to Mixpanel (Q-01 Step 1)**: M of P (X%)
- **Classification confidence**: HIGH / LOW
- **Split available**: true / false

## Group Classification

| User Group (Admin Console) | Bucket | User Count |
|---------------------------|--------|------------|
| Sales Reps | field_rep | 38 |
| Showroom Managers | showroom | 10 |
| Admin | admin_internal | 22 |
| ... | ... | ... |

## Per-User Classification (matched to Mixpanel only)

| Username | User Group | Bucket | Total Events |
|----------|-----------|--------|-------------|
| jchappell | Direct Sales Force | field_rep | 14,082 |
| dclevenger | Showroom Mgr | showroom | 23,425 |
| ... | ... | ... | ... |

## Aggregate Split

| Bucket | Users | Total Events | Event Share |
|--------|-------|-------------|-------------|
| field_rep | X | Y | Z% |
| showroom | X | Y | Z% |
| admin_internal | X | Y | Z% |
```

**Dependency note**: This query requires `Q-01_step1_results.md` to already exist (for the join-rate and event-share calculations). Run AFTER Q-01 Step 1 completes. If `HAS_SALES_SECTION = false` (meaning Q-01 was skipped), set `USER_GROUP_SPLIT_AVAILABLE = false` and skip this query entirely.

---

## Cache Output Format

All output files are written to `runs/{{shortname}}_{{YYYY-MM-DD}}/cache/`.

### 1. `cache/gate_flags.md` (format from ARCHITECTURE.md §4)

```markdown
# Gate Flags — {{CLIENT_NAME}} ({{shortname}}, org_id={{ORG_ID}})
- **Run date**: {{YYYY-MM-DD}}
- **Report mode**: Mode 1: Standard Intelligence Report

## Primary Gates

| Flag | Value | Evidence |
|------|-------|----------|
| HAS_CLICKY | ... | ... |
| HAS_CART | ... | ... |
| HAS_PORTAL_ORDERS | ... | ... |
| HAS_INVENTORY | ... | ... |
| HAS_SALES_DATA | ... | ... |
| HAS_SALES_SECTION | ... | ... |
| HAS_PEER_DATA | ... | ... |
| BENCHMARK_ELIGIBLE | ... | ... |
| BENCHMARK_CONFIDENCE | ... | Internal only — not in delivered HTML |
| PEER_GROUP_LEVEL | ... | Internal only — not in delivered HTML |
| PEER_GROUP_N | ... | Internal only — not in delivered HTML |
| PEER_GROUP_ID_EFFECTIVE | ... | Source for plain-language cohort framing |
| CLICKY_PREFIX | ... | N/A if HAS_CLICKY = false |

## Derived Gates (pre-computed — section agents consume these directly)

| Flag | Value | Evidence |
|------|-------|----------|
| VM45_GATE_1 | ... | ... |
| VM45_GATE_2 | ... | ... |
| VM45_RENDER | ... | Both gates pass/fail — render capture rate subsection or skip |
| QUALIFYING_REP_COUNT | ... | Number of reps with ≥10 iPad orders LTM |
| MIXPANEL_USER_DATA_PRESENT | ... | Q-01 Step 1 returned N rows |
| SHOWROOM_EXCLUSIONS | ... | See showroom_scan_results.md for names + evidence |
| MIXPANEL_ORDER_TRACKING_GAP | ... | Postgres LTM orders vs Mixpanel total submit_order |
| USER_GROUP_SPLIT_AVAILABLE | ... | join_rate ≥90%, ambiguous_rate = 0, showroom_event_share ≥10% |
| USER_GROUP_JOIN_RATE | ... | N of M Mixpanel users matched |
| USER_GROUP_SHOWROOM_EVENT_SHARE | ... | Showroom+admin share of matched events |

## Org Identity

- **Client name**: ...
- **Shortname**: ...
- **Org ID**: ...
- **Bundle**: ...
- **Bundle label for report**: ...

## Validation Log

- portal_orders: [diagnostic entry]
- Showroom scan: [diagnostic entry]
- VM-45: [diagnostic entry if gate failed]
```

### 2. `cache/section_manifest.md` (format from ARCHITECTURE.md §5)

| § | Section | Status | Gate | Agent File |
|---|---------|--------|------|-----------|
| 1 | Executive Summary | STAGE 4 | Always (written last) | stage4_assembly.md |
| 2 | Sales Team Performance | INCLUDE/SKIP | HAS_SALES_SECTION | section_02_sales_team.md |
| 3 | Customer & Buyer Intelligence | INCLUDE | Always | section_03_customers.md |
| 4 | Product & Inventory Intelligence | INCLUDE/SKIP | HAS_INVENTORY OR HAS_SALES_DATA | section_04_product.md |
| 5 | Commerce Analytics | INCLUDE | Always | section_05_commerce.md |
| 6 | Portal Engagement | INCLUDE/SKIP | HAS_CLICKY | section_06_portal.md |
| 7 | Peer Benchmarking | INCLUDE/SKIP | HAS_PEER_DATA + ELIGIBLE + not tier4 | section_07_peer.md |
| 8 | Platform & Feature Utilization | INCLUDE | Always | section_08_platform.md |
| 9 | Appendix | STAGE 4 | Always | stage4_assembly.md |

Include the **query-to-section mapping** table listing which cache files each section agent reads (per ARCHITECTURE.md §5).

### 3. `cache/Q-*_results.md` (format from ARCHITECTURE.md §3)

Rules for all cache files:
- **Header**: query ID, org context, period, row count, run date, any exclusions applied
- **Body**: markdown table with all result columns
- **No truncation**: include all rows returned by the query (the section agent decides what to display)
- **No interpretation**: raw data only — no narrative, no "What this tells you," no analysis
- **Dollar formatting**: use `$X,XXX` or `$X.XM` consistently
- **Null handling**: show `—` for null values, never omit the row

File naming convention (locked):
- `Q-{ID}_results.md` — single-step queries (e.g., `Q-08_results.md`)
- `Q-{ID}_step{N}_results.md` — multi-step queries (e.g., `Q-01_step1_results.md`)
- `Q-CL-{ID}_results.md` — Clicky queries (e.g., `Q-CL-01_results.md`)
- `Q-CI-{ID}_results.md` — peer benchmark queries (e.g., `Q-CI-03_results.md`)

### 4. `cache/peer_benchmark_extract.md`

Pre-extracted peer data from the benchmark CSV. Include all applicable metrics for the org with peer median, p25, p75, org value, quartile assignment, and percentile.

### 5. `cache/showroom_scan_results.md`

Exclusion evidence with: account names, GMV, order counts, and classification reasoning (confirmed / ambiguous). Header states total excluded count and aggregate GMV.

### 6. `cache/user_group_mapping.md`

Admin-console user group classification with per-user Mixpanel join results, aggregate split by bucket, and confidence metrics. Only produced when `HAS_SALES_SECTION = true` (Q-01 data exists). See Derived Gate 5 for format and confidence gate logic.
