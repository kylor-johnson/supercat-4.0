# Health V3 — Scoring Specification

**Version:** 3.5.0
**Date:** 2026-09-21
**Status:** Production-ready. Scoring math is equal-weighted (25/25/25/25), selectable via `--weights` (see §9 and CHANGELOG 3.4.0). Cache-mode runs are deterministic — same cache + same `--score-date` + same interpreter produces byte-identical output (see §6.6 and `ENVIRONMENT.md`).

> **Producing the next monthly canonical?** Use `RUN_PROMPT.md` in this folder — copy-paste prompt that orchestrates the full Path B workflow (cache populate → operator → cold-read → CHANGELOG → archive).

---

## What This Is

A monthly scorecard for every active SuperCat client, expressed as a single composite score (0–100) plus four dimension scores and per-dimension narratives. The output is a CSV with one row per org and an exec-summary `composite_narrative` field that explains the score in plain English.

The score answers one question: **is this client actually using and benefiting from SuperCat right now?** It does *not* measure expansion or growth opportunity — those are separate concerns.

The primary use case is a ranked at-risk list for CS outreach. Any org in Watch, At Risk, or Critical (or flagged as a ghost account) shows up on the radar. The score itself does not recommend interventions — that is a downstream V3.3 capability.

### How to populate the cache

The operator does **not** open live Postgres or BigQuery connections during a canonical run. Cache files are populated by an MCP-driven workflow ahead of time, and the operator reads from them in cache mode. This is the architectural reason the canonical scorecard is deterministic — see §6.6.

**Prerequisites:**

- Postgres and BigQuery MCP servers enabled — `supercat-postgres-vpn` and `bigquery-admin` in Claude Code. Any client works; the server names above are what this workspace exposes, and `supercat-data-routing` is the routing authority if they change.
- VPN connection active (both MCPs require it).
- An empty target directory at `cache/{YYYY-MM-DD}/` ready to receive 10 CSVs.

**Score-date anchor.** Use `date -u +%F` to determine the UTC date and use that for both the cache directory name AND the `--score-date` argument. The data inside Postgres/BigQuery queries is anchored to PG `NOW()` (UTC); aligning the cache name with the data's actual anchor preserves the determinism contract. Populate close to midnight UTC of the score date when possible.

**The 10 cache files** (one per loader function in `health_operator_v3.py`):

| File                    | Source loader function       | MCP                            |
|-------------------------|------------------------------|--------------------------------|
| `pg_org_config.csv`     | `load_pg_org_config`         | `supercat-postgres-vpn`   |
| `pg_engagement.csv`     | `load_pg_engagement`         | `supercat-postgres-vpn`   |
| `pg_smart_stacks.csv`   | `load_pg_smart_stacks`       | `supercat-postgres-vpn`   |
| `pg_orders.csv`         | `load_pg_orders`             | `supercat-postgres-vpn`   |
| `pg_portal_orders.csv`  | `load_pg_portal_orders`      | `supercat-postgres-vpn`   |
| `pg_catalog.csv`        | `load_pg_catalog`            | `supercat-postgres-vpn`   |
| `pg_imports.csv`        | `load_pg_imports`            | `supercat-postgres-vpn`   |
| `pg_domain_map.csv`     | `build_domain_map`           | `supercat-postgres-vpn`   |
| `bq_mp_sharing.csv`     | `load_bq_mp_sharing`         | `bigquery-admin`            |
| `bq_helpscout_fires.csv`| `load_bq_helpscout_fires`    | `bigquery-admin`            |

**Execution rules:**

1. **Read the SQL verbatim from each loader function.** The operator is the source of truth. Do not paraphrase, do not change column aliases, do not modify WHERE clauses or LIMITs.
2. **Inline the named-parameter substitutions** (`%(internal)s`, `%(excluded)s`) as alphabetized SQL tuples — `IN ('a','b','c')`. Membership semantics are not order-dependent, but alphabetizing keeps the SQL deterministic across runs.
3. **Run each query via the appropriate MCP** and capture the result.
4. **Write each result as a CSV** with the exact filename in the table above. Column names must match what the SQL emits — the operator looks them up by name; any mismatch produces silent breakage.
5. **Format requirements** (verify against `cache/{prior-date}/` for reference):
   - Bool columns: `True`/`False` strings are fine; the operator coerces.
   - Timestamp columns (`last_login_at`, `first_login_at`, `last_run_at`, `first_run_at`, `most_recent_open_at`): ISO 8601 strings.
   - `bq_helpscout_fires.csv` `sample_tags` column: write as Python `str(list)` repr (e.g., `"['s1 - critical', 'l4 - p2']"`).
6. **Use the right converter.** `scripts/to_csv.py` is the default — it is the only one that emits
   `sample_tags` in the required Python-list-repr form. `scripts/mcp_to_csv.py` joins lists with `|`
   and lowercases booleans, so it must **not** be used for `bq_helpscout_fires.csv`.
   `scripts/bq_to_csv.py` is for raw BigQuery JSON (`{"data": [...]}`) output.
7. **After writing each file, read it back with `pandas.read_csv()`** and verify (a) row count matches what the MCP query returned, (b) column names match the SQL output, (c) dtypes look reasonable.
8. **Verify content, not just shape — this is the step that catches real corruption.**
   Rules 6–7 pass on a file whose *values* are wrong. Cache data round-trips through an agent as
   text, and the 2026-09-21 run produced three silent transcription errors in `pg_domain_map.csv`
   alone (a swapped adjacent pair and two mangled domains) — every one preserved row count and
   column names. Compute a checksum server-side and compare it against the written file:

   ```sql
   -- append to each loader query, over the same ORDER BY the CSV is written in
   SELECT md5(string_agg(col1 || '|' || col2 || '|' || ..., E'\n' ORDER BY <key>)) FROM ( <loader query> ) t;
   ```

   Then hash the same concatenation locally from the CSV and require an exact match. A corrupted
   `pg_domain_map.csv` degrades `support_data_available` for **every** org, not just the mangled
   row, so this is not a per-row risk.
9. **Do not modify the cache after the run.** Per §6.6, each `cache/{date}/` directory is immutable once populated. To rerun for the same date, point at the same cache. To use fresher data, populate a new dated directory.

**Sanity checks before running the operator:**

- Exactly 10 files in `cache/{YYYY-MM-DD}/`.
- Each readable by `pandas.read_csv` without exceptions.
- Row counts within ±50% of the prior cache for `pg_org_config` (~250), `pg_engagement` (~250), `pg_imports` (~760), `pg_catalog` (~235). A drastic delta indicates an upstream data issue and should be investigated before running the operator.

### How to run

Once `cache/{YYYY-MM-DD}/` is populated:

```bash
cd "Health V3"
.venv/bin/python3 health_operator_v3.py \
  --mal "inputs/master_account_list_{YYYY-MM-DD}_canonical.csv" \
  --score-date {YYYY-MM-DD} \
  --cache --cache-dir "cache/{YYYY-MM-DD}" \
  --output-dir "runs/{YYYY-MM-DD}"
```

Output lands at `runs/{YYYY-MM-DD}/client_health_scores_{YYYY-MM-DD}.csv`.

**`--score-date` is required.** The operator refuses to run without it (since V3.2.10). Use `date -u +%F` to produce the UTC date string, and pass the same value to both `--score-date` and `--cache-dir` so the cache name and the scoring anchor stay aligned.

**Determinism check.** Run the command twice and SHA-256 the output CSV both times. The hashes must match byte-for-byte. If they don't, there is a non-deterministic ordering or formatting issue in the cache (most likely: dict iteration order in `build_domain_map`, or timestamp serialization variance) — investigate before treating the run as canonical.

---

## Philosophy

V3 is a deliberate simplification of V2. The goal is a scoring model that:

- Produces a **composite score** (0–100) that is explainable in one sentence
- Produces a **dimension score** (0–100) for each of the 4 health pillars
- Produces a **plain-English narrative** for each dimension that says *why* the score is what it is — not a definition, an interpretation
- **Starts unweighted.** All 4 dimensions contribute equally (25% each). Weights may be added later if correlation analysis against retention/ARR supports it — not before. Any correlation analysis must be **stratified by bundle** (or include bundle as a covariate); naïve pooled correlations across the full portfolio will conflate dimension score with bundle structure.
- **Does not include Growth scoring.** Growth is a separate concern and will be addressed independently.
- **Does not include trajectory as a dimension.** Trend direction is better observed as narrative context after the fact, not as a scored input.

> The test for every scoring decision: *"Would a CS rep reading this score understand exactly why it is what it is, and know what to do about it?"* If not, simplify.

---

## Dimensions

### At a Glance

| # | Dimension | Weight | Core Question |
|---|-----------|--------|---------------|
| 1 | Engagement | 25% | Are users actually showing up? |
| 2 | Adoption | 25% | Are they using the breadth of what they have? |
| 3 | Value Delivery | 25% | Are they getting tangible outcomes? |
| 4 | Operational Health | 25% | Is the data infrastructure in good shape? |

Composite = simple average of the 4 dimension scores.

---

## §1 Engagement

**What it measures:** User activity — are people logging in, and are they doing so consistently?

### Signals

| Signal | Source | Field |
|--------|--------|-------|
| Login count (trailing 90d) | Postgres `login_events` | `COUNT(*) WHERE created_at >= NOW() - 90d` |
| Login count (trailing 30d) | Postgres `login_events` | `COUNT(*) WHERE created_at >= NOW() - 30d` |
| Login count (trailing 180d) | Postgres `login_events` | `COUNT(*) WHERE created_at >= NOW() - 180d` |
| Unique active users (trailing 90d) | Postgres `login_events` | `COUNT(DISTINCT user_id)` |
| Total enabled internal users | Postgres `org_users` + `users` | `COUNT(*) WHERE disabled = false` AND `users.email` domain not in the SuperCat-internal exclusion list (see §8). Fallback when the count is unreliable: count distinct `user_id` from `login_events` in trailing 365d. |
| Active user ratio | Derived | `min(unique_active / enabled_users, 1.0)` — capped at 100%. When raw ratio > 100%, set narrative flag `denominator_quality = stale` (the org's `disabled = false` count is suspect — typically because customer-portal accounts inflate `org_users` or active reps have stale disabled flags). For Full and iPad+Catalog+Cart bundles where enabled_users > 500, the denominator switches to active_users_365d (distinct users from login_events in the trailing 365 days). This corrects for B2B customer portal accounts inflating the org_users count for these tiers. Orgs where this switch applies will show "(denominator switched to annual active users — org_users inflated by portal accounts)" in their narrative. |
| Login velocity ratio | Derived | `(logins_30d / logins_180d) × 6` — compares the trailing 30d cadence to the trailing 6-month average monthly cadence. |

### Scoring

Three sub-signals are scored 0–100 and averaged.

**Login Count Score** — absolute logins in 90d:

| Logins | Score |
|--------|-------|
| 0 | 0 |
| 1–49 | 20 |
| 50–199 | 40 |
| 200–499 | 60 |
| 500–999 | 75 |
| 1,000–2,999 | 88 |
| 3,000+ | 100 |

**Active User Ratio Score** — unique active users / enabled users (capped at 100%):

| Ratio | Score |
|-------|-------|
| 0% | 0 |
| 1–24% | 20 |
| 25–49% | 45 |
| 50–74% | 65 |
| 75–89% | 82 |
| 90%+ | 100 |

**Login Velocity Score** — `velocity_ratio = (logins_30d / logins_180d) × 6`. The multiplier converts a 30d count into a per-180d-equivalent so a steady-state cadence yields a ratio of 1.0:

| Velocity ratio | Score |
|----------------|-------|
| ≥ 1.5 (accelerating) | 100 |
| 0.75–1.49 (steady) | 90 |
| 0.50–0.74 (cooling) | 60 |
| 0.25–0.49 (sharply decelerating) | 30 |
| > 0 but < 0.25 (near-dormant) | 10 |
| 0 or undefined (`logins_180d = 0`) | 0 |

**Interpretation:** `1.0` is steady state — last 30d matches the trailing 6-month rate. Below `0.75` is cooling off; below `0.50` is a meaningful slowdown. Above `1.5` indicates an acceleration over baseline.

`engagement_score = (login_count_score + active_user_ratio_score + login_velocity_score) / 3`

Velocity replaces the V3.0 "days since last login" recency score because recency banded 103 of 104 orgs identically (≥99% logged in within the last 7 days). Velocity captures the "logged in 500 times in month 1, then went silent" case that login-count alone misses, and discriminates across the portfolio. Edge case: if `logins_180d = 0`, `velocity_score = 0` — no other special handling is needed because new-org suppression already happens upstream at the composite level (§6 New-Org Exclusion).

### Seasonality

V3 does not attempt to model seasonality algorithmically. Instead:
- If the measurement window falls in a known slow cycle for the org's category (furniture, lighting, etc.), note it in the narrative
- Flag `seasonality_context` as a human-readable note alongside the score — it does not adjust the score
- Revisit in V3.1 once we have 12-month baselines per org to normalize against

### Narrative Pattern

> *"X logins in 90 days from Y of Z enabled users (AA% active user ratio). Velocity V.Vx trailing rate (N logins last 30d vs ~M/mo avg). [Seasonality note if applicable]."*

Example: *"2,591 logins in 90 days from 64 of 84 enabled users (76% active ratio). Velocity 1.0x trailing rate (864 logins last 30d vs ~864/mo avg)."*

Low example: *"183 logins in 90 days from 8 of 20 enabled users (40% active ratio). Velocity 0.6x trailing rate (37 logins last 30d vs ~62/mo avg)."*

Dark example: *"412 logins in 90 days from 8 of 20 enabled users (40% active ratio). Velocity 0.2x trailing rate (15 logins last 30d vs ~75/mo avg)."*

If `logins_180d = 0`, the velocity sentence reads *"Velocity: insufficient history."* and the velocity sub-signal scores 0.


---

## §2 Adoption

**What it measures:** Are they using the breadth of features that apply to their configuration?

### Design Principle

This is a **point system**, not a weighted average. Each applicable feature is worth 1 point. Used = 1, not used = 0. Score = points earned / points applicable × 100. No feature is worth more than another.

**Critical gating rule:** A feature is only "applicable" if it is both:
1. Active in the org's subscription
2. Turned ON in the org's actual `mobile_sites` configuration (or equivalent config flag)

Do not penalize an org for not using a feature that is disabled in their config.

### Feature Matrix

| Feature | Applicability Gate | Usage Signal | Source |
|---------|--------------------|--------------|--------|
| iPad App (core) | Always applicable | `logins_90d > 0` | `login_events` |
| Smart Stacks | Always applicable | `smart_stacks COUNT > 0` | `smart_stacks` |
| Sharing / quoting | Always applicable | `mp_sharing_events_90d > 0` (sum of `item_email_drafted` + `document_email_drafted`) | BigQuery `mixpanel.events` |
| eCat Online Catalog | `mobile_sites.enable_online_catalog = true` | `portal_orders_90d > 0` | `mobile_sites`, `portal_orders` |
| Online Ordering (B2B Cart) | `mobile_sites.enable_online_ordering = true` | `portal_orders_90d > 0` | `portal_orders` |
| Sales Portal | `mobile_sites.enable_sales_portal = true` | `view_portal_90d > 0` — measures rep access to the Sales Portal section of the iPad app via the Mixpanel `view_portal` event in trailing 90 days, independent of order volume | BigQuery `mixpanel.events` |
| Inventory Management | At least one Inventory `import_events` row in trailing 180 days | `inventory imports in 90d > 0` | `import_events` |
| Sales Data | `enable_sales_data = true` on org | `sales_data imports in 90d > 0` | `import_events` |

**Notes:**
- `ipad_reports` (formal presentations) is NOT scored as a feature — usage is near-zero across the portfolio and does not reflect actual product utility. The Mixpanel sharing/quoting events are the meaningful sharing signal.
- Postgres `shared_resources` is a configuration table, not an activity log, and is **not** used for scoring.
- eCat Online Catalog and Online Ordering use `portal_orders_90d > 0` as the usage signal. Sales Portal uses `view_portal_90d > 0` (the Mixpanel `view_portal` event) — this measures rep access to the Sales Portal section of the iPad app independent of order volume, and correctly credits portal-browsing activity that does not result in orders while correctly penalizing orgs where portal orders exist through the customer web portal but reps are not opening the feature.
- Online Ordering applicability requires `enable_online_ordering = true` in `mobile_sites` — a B2B Cart subscription without this flag enabled does not count as an applicable feature.
- "Inventory Management active" means at least one Inventory import has run in the trailing 180 days. Orgs whose Inventory feed lapsed years ago are not counted as having an applicable Inventory feature (mirrors the §4 active-import-type definition).
- When the MAL bundle and `mobile_sites` config disagree (e.g., MAL says iPad-only but `enable_online_ordering = true`), the `mobile_sites` flag wins for applicability gating. The mismatch is surfaced in narrative as a data-hygiene flag, not as a usage gap.

### Scoring

`adoption_score = (features_used / features_applicable) × 100`

Minimum applicable features: 3 (iPad, Smart Stacks, Sharing/quoting are always applicable).

### Narrative Pattern

> *"Using X of Y applicable features. Unused: [list]."*

Example: *"Using 6 of 8 applicable features. Unused: Sales Data feed (configured but no imports in 90 days), Online Ordering (enabled but no portal orders in 90 days)."*

---

## §3 Value Delivery

**What it measures:** Is the platform generating tangible, observable business outcomes?

### Design Principle

Same point system as Adoption — additive, no internal weighting. Each applicable delivery activity is worth 1 point. An org that processes 200 presentations and an org that submits 2,000 orders are both delivering value through their primary channel. Neither is weighted above the other.

**Applicable activities are determined by what the org is actually configured and set up to do** — same config-gating logic as Adoption.

### Delivery Activity Matrix

| Activity | Applicability Gate | Usage Threshold (= 1 point) | Source |
|----------|--------------------|-----------------------------|--------|
| Order volume (iPad) | Always applicable | `COUNT(orders WHERE LOWER(order_source) = 'ipad' AND is_submitted = true AND submit_date >= NOW() - 90d) >= 10` | `orders` |
| Sharing activity | Always applicable | `mp_sharing_events_90d >= 3` (sum of `item_email_drafted` + `document_email_drafted`) | BigQuery `mixpanel.events` |
| Online catalog active | `mobile_sites.enable_online_catalog = true` | `portal_orders_90d > 0` (portal traffic is the Postgres-derivable proxy for online catalog engagement; Clicky page-view data is not in BigQuery) | `mobile_sites`, `portal_orders` |
| Portal ordering (B2B Cart) | `mobile_sites.enable_online_ordering = true` | `portal_orders_90d > 0` | `portal_orders` |
| Sales Portal engagement | `mobile_sites.enable_sales_portal = true` | `portal_orders_90d > 0` | `portal_orders` |
| Inventory data flowing | Inventory imports active in trailing 180d | `inventory imports in 90d > 0` | `import_events` |

**Notes:**
- The "Online catalog active" channel was previously labeled "Catalog browsing / online engagement" and sourced from Clicky page views. Clicky data is not in BigQuery and there is no pipeline to land it for V1, so the channel was renamed to be honest about what V3 actually measures: portal traffic exists for this org, sourced from `portal_orders`. The narrative should not promise page-view inference the metric isn't doing.
- "Order volume (iPad)" filters to iPad-source orders only (`LOWER(order_source) = 'ipad'`). An org with high non-iPad order volume (e.g., portal/online orders bypassing the iPad app) but low iPad order volume is correctly flagged here as not converting iPad activity into orders. Portal activity is captured separately under "Portal ordering."
- `portal_orders_90d > 0` is the unified signal across Online Ordering, Sales Portal, and Online catalog active. Three channels can fire from the same underlying observation; that is intentional — they reflect three different config gates.

**Thresholds are intentionally low for V1.** The question is "is there any meaningful activity?" not "is activity high enough?" Calibrate upward in V3.1 after spot-checking.

### Scoring

`value_delivery_score = (activities_achieved / activities_applicable) × 100`

### Narrative Pattern

> *"Delivering value through X of Y applicable channels. [Specific gap callout if score < 60]."*

Example: *"Delivering value through 5 of 6 applicable channels. iPad order volume is active (2,344 iPad orders in 90d) and inventory is flowing daily. Sharing activity is at 11 sharing events in 90d (item + document email drafts), just above the threshold."*

Low example: *"Delivering value through 2 of 5 applicable channels. Online catalog is enabled but no portal traffic in 90 days. Portal ordering has been configured but no portal orders in 90 days."*

---

## §4 Operational Health

**What it measures:** Is the data infrastructure clean, current, and well-maintained?

### Three Sub-Signals

1. **Catalog Completeness** — are products properly filled out?
2. **Import Health** — are active data feeds running successfully?
3. **Data Freshness** — are active data feeds running on their expected cadence?

Each sub-signal scores 0–100. `operational_health_score = average of three sub-signal scores`.

---

### Sub-Signal 1: Catalog Completeness

**What counts as "complete" for a product** (all three required):
- `long_description` is not null/empty
- A pricing signal: `net_price > 0` **OR** `contract_pricing_enabled = true` on the org **OR** (`prices_json IS NOT NULL AND prices_json != '{}'`) — i.e., price-level pricing is in use
- `image_exists = true` on the product

The pricing clause must be evaluated with explicit precedence: any one of the three conditions satisfies the price check. Contract-pricing orgs (WAC / FAL-style) and price-level-pricing orgs (KLL / MFC-style) are not penalized for $0 `net_price`.

**Completeness percentage:** `complete_products / total_active_products × 100` (excluding `deleted = true` products).

**Step ladder** — the percentage is mapped to a band score, not used raw:

| Catalog completeness % | Score |
|------------------------|-------|
| ≥ 90% | 100 |
| 60–89% | 60 |
| < 60% | 20 |

A 75%-complete catalog scores 60 (Healthy-level — usable but with real coaching room). A 95%-complete catalog scores 100. Anything below 60% scores 20 (At Risk-level) regardless of how far below — a 10% catalog and a 50% catalog are both "not usable in the field," and the operator narrative tells CSMs which one it is.

---

### Sub-Signal 2: Import Health

**What counts as an "active import type" for this org:**
- Any import type that has run at least once in the trailing 180 days

Only score import types that are active for this org. Do not penalize an org for not having an inventory feed if they have never had one.

**For each active import type:** determine if the most recent run was successful (no `:error` entries in the `data` field, or at most warnings).

`import_health_score = (successful import types / total scoreable import types) × 100`

**Excluded import types — health scoring only:** The following types are excluded from the import-health ratio (numerator and denominator) due to known parser artifacts that produce a 100% false-error rate against `last_run_had_error`:

- `Multifile Import`
- `Import File Processing`
- `Product Image Downloads`

These three types are excluded **only from the health ratio** — their `run_count_180d`, `first_run_at`, and `last_run_at` are still used by Sub-Signal 3 (Data Freshness). Only `last_run_had_error` is unreliable for these types, not the timing fields.

V1 simplification: treat any import with only `:warning` entries (not `:error`) as successful.

---

### Sub-Signal 3: Data Freshness

**Core principle:** Freshness is measured relative to the org's own observed cadence — not against a universal clock.

**For each active import type:**

1. Calculate the **gap denominator** between import runs for this org and import type (use trailing 180d history): `gap = max(median_gap, 1.0 day)`. Use the median; if `PERCENTILE_CONT()` is unavailable in the operator's SQL surface, fall back to mean gap. The 1-day floor prevents bursty feeds (e.g., 20 runs in 2 days during an initial load) from producing degenerate ratios.
2. Calculate **days since last run** for this import type.
3. `staleness_ratio = days_since_last_run / gap`

| Staleness Ratio | Score |
|-----------------|-------|
| ≤ 1.0 (on or ahead of cadence) | 100 |
| 1.1–1.5 (slightly late) | 80 |
| 1.6–2.5 (notably late) | 50 |
| 2.6–4.0 (significantly overdue) | 20 |
| > 4.0 (stale / likely broken) | 0 |

`data_freshness_score = run_count_180d-weighted average staleness score across all measurable import types`

**When no import feed has run in the window**, both the import-health and
freshness sub-signals are `None` and the dimension score rests on catalog
completeness alone. That is recorded as `ops_measurement = "catalog_only"`, the
per-dimension narrative says the two sub-signals are unmeasured, and the
`clean_ops_dark` composite shape is suppressed (§6.5). The score is **not**
blanked — a poor catalog is still a real ops finding, as `dals` shows at ops 20 —
but it must not be read as evidence that the data infrastructure is sound.

Per-type staleness scores are aggregated via a **frequency-weighted average** — each type's score is weighted by its `run_count_180d`. A daily inventory feed (≈ 180 runs) drives the freshness signal far more than a quarterly catalog re-load (≈ 2 runs), which matches operator intuition that a stalled daily feed is a much bigger problem than a stalled quarterly one. If `total_weight = 0` (defensive fallback only), the average degrades to a simple mean.

**Minimum history required:** At least 3 import events of this type in 180d to calculate a meaningful median. If fewer than 3 events exist, treat this import type as unscored and omit from the freshness average.

**Initial-load carve-out:** If an import type has fewer than 5 runs total in trailing 180d AND all runs occurred within a 7-day burst AND `days_since_first <= 14` (i.e., the burst happened within the last 14 days), treat the type as `initial_load_only` and omit from the freshness average. A feed that just initial-loaded and is settling in is not "stale." A feed whose burst happened months or years ago is *not* carved out — its `days_since_first` will be well over 14 and the 180-day trailing window will surface its staleness normally.

> **V3.0 bug fix (2026-05-11):** The earlier carve-out condition `days_since_last == days_since_first - days_span` was an algebraic identity that is always true by definition (all three values derive from the same two timestamps). It caused the carve-out to fire for any feed with `<5` runs in a 7-day span regardless of how old the burst was, masking long-stale feeds. The fixed condition `days_since_first <= 14` correctly anchors the carve-out to *recent* bursts only.

---

### Narrative Pattern

> *"Catalog: X% complete. Imports: Y of Z active feed types healthy. Freshness: [summary]."*

Example: *"Catalog 96% complete (contract pricing in use — price check skipped). All 4 active import types healthy. Inventory feed running daily as expected."*

Example (price-level pricing): *"Catalog 92% complete — `prices_json` populated for all products (price-level pricing in use), so the price check is satisfied for every priced product."*

Low example: *"Catalog 61% complete — 1,847 active products are missing images. Imports: 3 of 4 feed types healthy; Sales Data feed last ran 14 days ago against a 2-day expected cadence."*

---

## §5 Support Modifier

Support data is **not a scored dimension.** It is a fire flag that surfaces alongside the health score without adjusting it.

**Fire flag triggers** — any open HelpScout conversation (status `active` or `pending`, not `closed` or `spam`) tagged with one of:

- `l3 - engineering intervention` (escalation: engineering)
- `l4 - strategic decision or executive involvement` (escalation: executive)
- `s1 - critical` (severity: critical)
- `s2 - high` (severity: high)

Tag matching is case-insensitive and uses prefix match — `LOWER(tag) LIKE 'l3%'` etc. — so suffix changes to the tag wording (e.g., HelpScout edits the human-readable label) do not break detection.

**When a fire flag is active:**
- Noted prominently in the score output: `support_fire: true`
- Brief description added: `support_fire_notes: "1 open L3 escalation (8 days old)"`
- Does NOT adjust the composite score in V1

**When no fire flag:**
- `support_fire: false`
- `support_fire_notes` is null

**Domain mapping for org attribution:**
- HelpScout conversations attribute to orgs via `primaryCustomer.email` domain matched against a Postgres-derived domain map
- Generic domains (`gmail.com`, `yahoo.com`, etc., plus SuperCat-internal domains) are excluded
- The domain map is regenerated at run time from `users` + `org_users` Postgres tables; the operator does not depend on a cached file
- `support_data_available = true` if the BigQuery query succeeded and at least one resolved domain exists for this org. Otherwise `false`, no flag, no penalty.

---

## §5.1 Ghost Account Override

A ghost account is an org that is **paying meaningfully** but **not using the product at all** — the highest-leverage save target in the portfolio. V3 surfaces them via a single deterministic override.

**Trigger conditions (both must be true):**
- MAL `arr >= 5000`
- `logins_90d = 0` (zero login events in trailing 90 days)

**Effect when triggered:**
- `ghost_account = true`
- `composite_score` is capped at `min(computed_composite_score, 20)` regardless of dimension scores
- `health_band = "Critical"` — **assigned directly, not derived from the cap.** 20 is the *At Risk* floor in `HEALTH_BANDS`, so `band_for_score(20)` returns `"At Risk"`; the band is set explicitly in the override. Before V3.4.1 it was not, and every ghost silently banded At Risk — undetected until 2026-09-21, the first run that produced any ghosts, which reported `Critical: 0` while carrying four.
- A ghost is the most severe state the model expresses. A paying account with zero logins outranks an account limping along at 15 with some activity.
- **The ghost condition outranks the §6 new-org gate.** It is evaluated before that gate, and a ghost is never skipped as an onboarding-window org. Without this, `aa` — $42,480 ARR, zero logins in its entire history, first subscription this year — was claimed by both rules and would have vanished from the scorecard entirely once the gate was repaired.
- `ghost_subtype` splits the two populations the ARR-plus-zero-logins condition cannot distinguish on its own:

  | Subtype | Condition | The CS conversation |
  |---|---|---|
  | `no_activity_12m` | `active_users_365d = 0` | Never activated, or dark for over a year. "Did onboarding ever happen?" |
  | `lapsed_this_quarter` | someone was active within 365d, nobody within 90d | Was using it and stopped. "What changed?" |

  Both land at the same capped score and the same Critical band — the subtype is
  the routing signal, not a severity signal. `bmc` illustrates why it matters: an
  org live since 2011 with thousands of logins behind it, now at zero, is a very
  different call from an account that never started. **Twelve months is a proxy for
  lifetime history**, which `pg_engagement` does not carry; an org dark for longer
  than a year reads as `no_activity_12m` even if it was once active.
- All four dimension scores still compute and are still shown (do not blank them — CSMs need to see why the org isn't using each surface)
- `ghost_account_note: "ARR $X, zero logins in 90d"` is added to the output

**Effect when not triggered:**
- `ghost_account = false`
- `ghost_account_note` is null
- Composite is the unmodified average of the four dimensions

**Rationale:** A high-ARR org with zero logins is broken regardless of catalog completeness or import health. Operational signals can light up green on a catalog that nobody is opening — the override prevents that misleading composite. Lower-ARR ghost accounts (`arr < 5000`) are not overridden because they may be genuinely on-pause or in a different lifecycle and don't carry the same urgency.

---

## §5.2 Behavioral Floor Override

An account whose users are not showing up and whose platform activity is producing no observable business outcomes cannot be classified as Healthy or Thriving regardless of catalog completeness or feature configuration. This override catches near-ghost accounts that fall below the ghost-account threshold (`logins_90d > 0`) but are functionally dormant.

**Trigger conditions (both must be true):**
- `engagement_score < 55`
- `value_delivery_score < 40`

> **Threshold note:** The engagement threshold is **55, not 40** — the higher value was confirmed during spot-check calibration (2026-05-11). Earlier drafts of this spec listed `< 40`; the operator has always implemented `< 55`, and the operator value is correct. The rationale: the floor is meant to catch accounts where users are not meaningfully showing up, and a 40-point engagement score still corresponds to ≈50 logins in 90 days from a small active fraction — which spot-checks established as "barely-attached but not absent." The 55 threshold catches the genuinely-near-dormant cohort.

**Effect when triggered:**
- `behavioral_floor_applied = true`
- `composite_score` is capped at `min(computed_composite_score, 40.0)` — health band cannot exceed Watch
- `health_band` is assigned after the cap and reflects the capped score
- All four dimension scores are unchanged and must be shown in full — CSMs need to see why the floor fired

**Effect when not triggered:**
- `behavioral_floor_applied = false`
- Composite is the unmodified average of the four dimensions

**Rationale:** An account whose users are not meaningfully showing up (Engagement < 55) AND whose platform activity is producing no observable business outcomes (Value Delivery < 40) cannot be classified as Healthy or Thriving regardless of catalog completeness or feature configuration. This override catches near-ghost accounts that fall below the ghost-account threshold (`logins_90d > 0`) but are functionally dormant. Operational Health and Adoption can score well on a catalog and configuration that nobody is actively using — the behavioral floor prevents that from producing a misleading composite.

**Narrative note:** When `behavioral_floor_applied = true`, the narrative should explicitly surface the floor: *"Behavioral floor applied — engagement and value delivery are both below threshold. Dimension scores are shown as computed; composite is capped at 40."*

---

## §6 Scoring Output

Each org produces one row with the following fields:

```
org_shortname
org_name
run_date                      # YYYY-MM-DD of the run
bundle                        # MAL stack column — authoritative
arr                           # MAL — authoritative
cohort_year                   # MAL — authoritative

engagement_score              # 0–100, may be null when scoring_status = blocked
engagement_narrative          # one sentence (interpretation, not definition)

adoption_score                # 0–100
adoption_narrative            # one sentence

value_delivery_score          # 0–100
value_delivery_narrative      # one sentence

operational_health_score      # 0–100
operational_health_narrative  # one sentence

composite_score               # 0–100, see scoring_status math below
health_band                   # Thriving (80+) / Healthy (60–79) / Watch (40–59) / At Risk (20–39) / Critical (<20)
composite_narrative           # 2–3 sentence plain-English explanation of why the composite landed where it did

ghost_account                 # true / false (§5.1)
ghost_account_note            # text if true, null if false
ghost_subtype                 # no_activity_12m / lapsed_this_quarter; null when not a ghost (§5.1)
behavioral_floor_applied      # true / false (§5.2)

support_fire                  # true / false
support_fire_notes            # text if true, null if false
support_fire_days_open        # integer — days since most recently opened fire-tagged HelpScout conversation, as of score_date; null if support_fire = false
support_data_available        # true / false

scoring_status                # complete / partial / blocked
dimensions_scored             # integer 0–4 — count of dimensions with a non-null score
denominator_quality           # null or "stale" — set when raw active_user_ratio > 100% before cap
ops_measurement               # "full" (all three ops sub-signals contributed) or "catalog_only"
                              #   (no import feed ran in the window — see §4)
bundle_config_mismatch        # true / false — set when MAL bundle disagrees with mobile_sites flags
```

### Health Bands

| Score | Band |
|-------|------|
| 80–100 | Thriving |
| 60–79 | Healthy |
| 40–59 | Watch |
| 20–39 | At Risk |
| 0–19 | Critical |

### Composite Math and Scoring Status

Define `dimensions_scored` = count of dimensions with a non-null score after computation.

| `dimensions_scored` | `scoring_status` | `composite_score` |
|---------------------|------------------|----------------|
| 4 | `complete` | average of all four dimension scores |
| 2 or 3 | `partial` | average of the dimensions that *did* score (denominator = `dimensions_scored`); narrative notes that the score is reduced-confidence |
| 0 or 1 | `blocked` | `null` — no band assignment, row is preserved for visibility but not scored |

A dimension is "missing" when no observation is computable — the source table doesn't exist for this org or every input query returned no usable rows. A zero-valued observation (e.g., `logins_90d = 0`) is **not** missing — it is a real signal of zero activity and scores 0.

The §5.2 Behavioral Floor override applies *after* the composite is computed and *before* the §5.1 Ghost Account override: `composite_score = min(composite_score, 40.0)` when `behavioral_floor_applied = true`. The §5.1 Ghost Account override then applies: `composite_score = min(composite_score, 20)` when `ghost_account = true`. Neither override has any effect on `scoring_status`.

### Run Cadence and History

V3 runs **monthly**. The 90-day trailing windows used by Engagement, Adoption, and Value Delivery already smooth weekly noise; running weekly produces highly correlated scores and would mostly use stale MAL data. Monthly cadence aligns with the MAL refresh cycle.

Each monthly run writes its CSV to `Health V3/runs/{YYYY-MM-DD}/client_health_scores_{YYYY-MM-DD}.csv`. History is the directory listing — no new schema is introduced. Trend analysis (V3.1+) reads any month's CSV by partition.

### New-Org Exclusion

Orgs whose oldest observed login event is less than 90 days old are written to
`runs/{date}/skipped_new_orgs.csv` with reason `onboarding_window` and excluded
from scoring. They are in the onboarding phase where TTFV is the right metric,
not health. The `subscriptions.start_date` field is *not* used for this check —
the table appears to have been backfilled in mid-2025, so it is unreliable for
older cohorts.

The gate has two conditions. Either excludes an org:

1. Its oldest observed login event is less than `NEW_ORG_DAYS` (90) old, **or**
2. It has no login events at all and its MAL `cohort_year` is the current year.

> **Fixed in V3.5.0 — condition 2 was unreachable for five months.**
> `load_pg_engagement` LEFT JOINs `organizations`, so an org with no logins gets
> `first_login_at = NULL`, which `parse_dates` turns into `NaT`. The check was
> `if first_login is not None`, and **`NaT is not None` is `True`** — so the
> `elif` on `cohort_year` was dead code in cache mode, the subtraction produced
> `nan`, and `nan < 90` is `False`. No org was ever excluded for having zero
> logins. Now `pd.notna(first_login)`.
>
> Repairing it alone would have made things worse: it would have skipped `aa`
> ($42,480 ARR, zero logins ever, current-year cohort) and removed the worst
> account in the portfolio from the scorecard. So it shipped together with
> **§5.1 taking precedence over this gate** — a paying account with zero logins
> is a ghost, never merely new.

**`--include-new-orgs` overrides the gate.** Passing it scores those orgs instead
of skipping them, and no `skipped_new_orgs.csv` is written.

| Run | Flag | Why |
|---|---|---|
| Monthly CS portfolio canonical | **omit** | An account 6 weeks in has no 90-day history; a health band would be noise, and TTFV is the right metric. |
| Onboarding early-life review | **pass** | The question there is "is this launch going well", so a nascent score is the point. Read it as directional. |

The flag changes the population, never the math. It is recorded in
`run_metadata.md` so a run's scope is never ambiguous — a canonical accidentally
produced with it would otherwise be silently non-comparable to its neighbours.

---

## §6.5 Composite Narrative

The `composite_narrative` column is the **executive summary** for each org — a 2–3 sentence plain-English read that explains *why* the composite landed where it did and what the score is telling CS at a high level. Per-dimension narratives stay available in the detail columns for analysts who want to dig in.

The composite narrative is built by `_build_composite_narrative()` in `health_operator_v3.py`. The engine checks shape categories top-to-bottom; the first match wins. Anything that doesn't fit a clean shape falls through to a mixed-profile fallback. The actual scores (engagement, adoption, value delivery, ops) are named in every narrative so the read isn't generic.

| Shape | Trigger | Frame |
|---|---|---|
| 1a — clean Thriving | Band = Thriving AND composite ≥ 90 AND every dim ≥ 80 | Performing across the board, no CS action required |
| 1b — borderline Thriving | Band = Thriving AND not 1a | In Thriving band but near the boundary — names the relative drag, recommends a check-in to solidify Thriving |
| 1c — all-strong Healthy | Band = Healthy AND every dim ≥ 70 | Solid shape with one relative drag at a coaching opportunity level |
| 2 — breadth gap | Engagement ≥ 60 AND Adoption < 60 | Reps logging in but not using the full platform — feature coaching action. Escalates to "proactive outreach" for 2023+ cohorts with Value Delivery < 40 |
| 3 — passive value | Engagement < 55 AND Value Delivery ≥ 50 | Platform producing outcomes from a small slice of the team. When Ops < 30, calls out infrastructure as constraining engagement and shifts the action to a parallel ops + rep-activation escalation |
| 4 — near-dormant | Engagement < 55 AND Value Delivery < 50 (floor not fired) | Both behavioral signals below threshold; CS should re-establish contact and assess save play |
| 5 — surface-strong with ops drag | Ops < 50 AND Engagement ≥ 60 AND Value Delivery ≥ 60 | Looks strong but infrastructure is the hidden risk — ops team escalation |
| Fallback — mixed profile | Anything else | Names strongest and weakest dimension, prescribes a band-aware action keyed off the weakest dim (`Thriving/Healthy/Watch` x 4 dims = 12-entry lookup, falls back to a severe-band escalation otherwise) |

**Override paths.** When `ghost_account = true` or `behavioral_floor_applied = true`, the composite narrative is set explicitly by the override path (in `main`, not by `_build_composite_narrative`) and uses the org's actual scores so a Watch-band account with the floor applied reads differently from a Critical-band account where the floor barely matters:
- **Ghost** — names the ARR and zero-login condition, calls for an immediate CS call.
- **Behavioral floor** — when the floor cap fires, the composite narrative is selected from one of four profile-aware sub-shapes. The sub-shapes are checked in order; the first match wins. Conditions reference the org's actual dimension scores (not the capped composite).

  | Sub-shape | Condition (first match wins) | Narrative framing |
  |---|---|---|
  | Critically low | `engagement_score < 25 AND value_delivery_score <= 10` | Essentially no active usage — platform is running but not used. Tied to ARR as an urgent recovery situation. |
  | Full adoption, users dark | `adoption_score >= 80` | Full platform configured and adopted, but rep logins have dropped off sharply. Outreach to understand whether reps have gone dark on a coverage issue or whether a more fundamental re-engagement effort is required. |
  | Clean infrastructure, users dark | `operational_health_score >= 75` **and `ops_measurement = "full"`** | Data infrastructure is healthy; reps aren't using the platform. Rules out infrastructure; frames as a rep adoption and activation conversation. The measurement condition was added in V3.5.0 — this shape cannot rule infrastructure out from a score built on catalog completeness alone, which is the shape every org with no import feed has (and every ghost). |
  | Standard floor | none of the above | Both rep activity and platform outcomes are too low to support a healthy relationship. Re-establish contact to determine whether the gap is coverage, product fit, or something else. |

  These thresholds are implemented in `health_operator_v3.py` `main()` lines ~1414–1463. Changes to the conditions or framings must update both files together.

**Bands and language.** Every action sentence is conditioned on the band so urgency matches severity — "monitor at standard cadence" at clean Thriving, "escalate to CS leadership" at floor-very-low Critical.

> **Design note:** The narrative engine is intentionally narrative-only. It does not adjust scores. Action recommendations are heuristic — they will move to the V3.3 save-plays runbook once that ships. Until then, treat the action sentence as a starting suggestion, not policy.

---

## §6.6 Determinism and Reproducibility

**Guarantee:** In cache mode, the same `cache/{date}/` directory plus the same `--score-date` produces byte-identical output, regardless of when the operator is run.

**How this is enforced.** All wall-clock time reads inside the operator (freshness math, errored-feed day counts, new-org cutoff) are anchored to the `--score-date` argument, not to `datetime.utcnow()`. Two consecutive runs an hour apart produce identical SHA-256 hashes on the output CSV.

**Why this matters.** A client's health score reflects their behavior on the score date. The score must not move because we waited an hour, a day, or a week to run the operator. Earlier versions used wall-clock time, which silently inflated staleness ratios for every active feed by the elapsed gap between cache pull and run.

**What "wall-clock-free" does NOT cover.**

- **Live mode** (`--cache` flag omitted) still uses Postgres `NOW()` in SQL queries. The 90-day rolling windows in `login_events`, `orders`, etc., move continuously. Live mode is intrinsically time-coupled and should be used only to populate the cache, not to produce the canonical scorecard.
- **Cache regeneration.** If you re-populate `cache/{date}/` tomorrow, the data inside is anchored to tomorrow's `NOW()` even though the folder still says `{date}`. **Treat each `cache/{date}/` directory as immutable once populated.** If you need fresh data, populate a new dated folder (use today's UTC date via `date -u +%F`).

**Operational discipline:**

1. Populate `cache/{date}/` once, ideally close to midnight UTC of the score date.
2. Run the operator with `--score-date {date}` and `--cache-dir cache/{date}`.
3. Never modify the cache after the run. To rerun for the same date, point at the same cache.
4. Record the interpreter alongside the SHA (see `ENVIRONMENT.md`).

**The guarantee is interpreter-scoped.** Verified 2026-09-16: the V3.2.13
canonical `b48e3a5f…` no longer reproduces. Running the *original* v3.2.x
operator against its own immutable cache under Python 3.9.6 / numpy 2.0.2 yields
`6a2f1d9f…` — three of 104 composites move by 0.1 (`all`, `bsc`, `gblx`), zero
band changes. The cause is float summation order at a `.x5` rounding boundary
under a different Python + NumPy, not a code change; the `.venv` that produced
those canonicals targeted a `python@3.14` that no longer exists.

So the contract is: **same cache + same `--score-date` + same interpreter →
byte-identical.** A canonical SHA quoted without its interpreter is not a
reproducibility claim. Pins live in `requirements.txt` / `.python-version`.

### Consistency checking

Run `.venv/bin/python3 check_consistency.py` from `Health V3/` to verify every cross-file invariant the V3.2.x audit identified:

1. Version coherence across `README.md`, `METHODOLOGY.md`, and the top `CHANGELOG.md` entry.
2. Live canonical SHA is recorded in the top `CHANGELOG.md` entry.
3. Canonical CSV header matches the operator's row-dict keys in order.
4. No stale column-name references — the pre-V3.2.8 column names retired by the schema migration — anywhere in the source-of-truth files. (Exact patterns live in `check_consistency.py`; excluded paths are `_archive/`, `cache/`, `runs/`, `outcomes.csv`, and `CHANGELOG.md`.)
5. Dashboard footer SHA matches live canonical (version label may legitimately lag if recent patches were SHA-neutral).
6. Formatted CSV header matches the operator's `_fmt_cols` list.
7. `--score-date` is `required=True` with no default in argparse.
8. Floor sub-shape names (`critically_low`, `full_adoption_dark`, `clean_ops_dark`) appear in both the operator and the §6.5 table.

Exit `0` = all checks pass. Exit `1` = at least one failed; output names the invariant and the diff. Run this after every operator patch and as a step in monthly canonical runs.

---

## §7 Known Simplifications (V1)

These are intentional shortcuts to keep V1 lean. They are candidates for V3.1 refinement after spot-checking.

| Simplification | Rationale | Revisit Trigger |
|----------------|-----------|-----------------|
| Equal 25% weights on all 4 dimensions | No empirical basis yet to weight differently | §9 Validation Plan — after retention/ARR correlation pass, stratified by bundle |
| Seasonality flagged in narrative but not modeled algorithmically | Insufficient per-org baseline history; year-over-year comparison conflates seasonality with growth/churn | Once 12-month trailing V3 history is available and we can baseline category-level seasonal patterns |
| Catalog completeness uses three binary criteria (description, price, image) | Table-stakes definition — adding polish metrics (multi-image, cross-sell, custom fields) into the score conflates "missing data" with "thin presentation" | V3.1 may surface polish metrics in narrative without changing the score |
| Import health: warnings treated as success | Avoids false negatives from persistent known-missing items | If warning noise proves misleading in practice |
| Freshness requires ≥ 3 historical events; uses 1-day floor on the gap denominator | Avoids bad estimates for low-history feeds and prevents bursty feeds from producing degenerate ratios | Could lower the run threshold to 2 with a confidence flag |
| Support modifier fires but doesn't adjust score | Keeps V1 clean; support data reliability still variable | After HelpScout domain map coverage is confirmed >90% |
| Bundle/config mismatches surfaced in narrative as data hygiene, not penalized | Mobile_sites flags are authoritative for applicability; reconciling against MAL bundle in scoring would penalize orgs for a config fact, not a usage fact | When the org-config audit is run and mismatches are corrected upstream |
| No `subscriptions` data is used for bundle/ARR | The `subscriptions` table appears backfilled in mid-2025 and is unreliable for older cohorts; MAL is authoritative | When subscription history is recovered or rebuilt for pre-2025 cohorts |

---

## §8 Data Sources

| Source | Connection | What It Provides |
|--------|------------|------------------|
| MAL CSV | Local file | **Authoritative** for `bundle` (MAL `stack` column), `arr`, `cohort_year`, `org_shortname` (MAL `ord_id` column) |
| Postgres `login_events` | MCP `supercat-postgres-vpn` | Login counts, unique active users, last login, earliest login (used for new-org detection) |
| Postgres `org_users` + `users` | MCP `supercat-postgres-vpn` | Enabled internal users per org. `users.email` domain is filtered against the SuperCat-internal exclusion list (see below). Fallback: distinct `user_id` from `login_events` in trailing 365d. |
| Postgres `organizations` | MCP `supercat-postgres-vpn` | Org config: `id`, `shortname`, `name`, `contract_pricing_enabled`, `enable_sales_data` |
| Postgres `mobile_sites` | MCP `supercat-postgres-vpn` | Feature flags: `enable_online_catalog`, `enable_online_ordering`, `enable_sales_portal` (authoritative for applicability gating in §2/§3) |
| Postgres `subscriptions` | MCP `supercat-postgres-vpn` | Reference only — not used for bundle (MAL is authoritative). Unreliable for new-org detection per §6. |
| Postgres `smart_stacks` | MCP `supercat-postgres-vpn` | Smart stack count per org |
| Postgres `orders` | MCP `supercat-postgres-vpn` | iPad order volume — filtered to `LOWER(order_source) = 'ipad' AND is_submitted = true AND order_state = 'active' AND submit_date >= NOW() - 90d` |
| Postgres `portal_orders` | MCP `supercat-postgres-vpn` | Portal/B2B cart order activity — filtered to `order_date >= NOW() - 90d` |
| Postgres `import_events` | MCP `supercat-postgres-vpn` | Import history. Type is extracted from the YAML `data` field (first entry). Status (success/warning/error) is parsed from the same field. |
| Postgres `products` | MCP `supercat-postgres-vpn` | Catalog completeness — `deleted`, `long_description`, `net_price`, `prices_json`, `image_exists` |
| BigQuery `mixpanel.events` | MCP `bigquery-admin` | Sharing/quoting events (`item_email_drafted`, `document_email_drafted`). Org attribution via `COALESCE(NULLIF(organization_shortname, ''), NULLIF(current_organization_shortname, ''))`. |
| BigQuery `helpscout.conversations` | MCP `bigquery-admin` | Support conversations and escalation/severity tags. Open conversations have `status IN ('active', 'pending')`. |

### SuperCat-Internal Domain Exclusion List

The following email domains are excluded from the `enabled internal users` count to prevent SuperCat staff and known integration partners from inflating the active-user denominator:

`supercatsolutions.com`, `lojic.com`, `railsfever.com`, `samedis.com`, `jimmythrasher.com`, `upwardtechnologies.com`

This list is also used when building the HelpScout domain-to-org mapping. The list is hard-coded in the operator and updated in lockstep with V2's `INTERNAL_USER_DOMAINS` constant.

### Removed from V3

- **Postgres `shared_resources`** — reclassified as a configuration table, not an activity log. Sharing/quoting activity is sourced from Mixpanel (`item_email_drafted`, `document_email_drafted`).
- **Postgres `product_images`** — `products.image_exists` is the direct boolean and removes the join.
- **Clicky** — page-view data is not in BigQuery and there is no pipeline to land it for V1. The "Online catalog active" channel uses `portal_orders_90d > 0` as a Postgres-derivable proxy.

---

## §9 Validation Plan

V3.0 ships unweighted (equal 25% per dimension). The validation protocol below is the pre-committed test that determines whether weighting should be introduced.

> **Status 2026-09-16 — run once, directionally, and it rejected weighting.**
> V3.3.0 introduced `25/20/35/20` weights in code on 2026-06-08 *without* running
> this test (`outcomes.csv` was empty). V3.4.0 reverted to equal weights after the
> test was finally run against 11 real outcome labels. Result: v330 matched equal
> on recall and lead time, improved AUC by at most **+0.008** against the **+0.05**
> bar below, and was **less precise in all seven months**. Full study and rerunnable
> evaluator: `runs/_weighting_study/2026-09-16/`.
>
> **This does not close §9.** 6 functional-death events is below the 30-outcome
> trigger condition. The prospective test below remains the gating test; what ran
> was the look-back option, which is directional only and cannot by itself justify
> a weighting change — which is precisely why the default reverted to the
> documented model rather than to a new weighting.
>
> The look-back also surfaced a structural finding that outlives the outcome count:
> Value Delivery scores SuperCat-submitted order volume, and Catalog-Focused
> accounts (54% of the base) are *defined* by ordering outside SuperCat. Weighting
> VAL is therefore partly a bundle/segment proxy, which is exactly the confound the
> stratification requirement below exists to prevent.

### When to run

Trigger conditions (all must be true):

1. V3 has produced at least 3 monthly snapshots
2. At least 30 orgs have a labeled outcome over the prior 12 months (churned / saved / retained / expanded)
3. The MAL has been refreshed within the past 30 days

### Protocol

For each candidate weighting scheme (at minimum: equal weights, correlation-derived weights, CS-intuition weights):

1. **Stratify by bundle** — analysis must control for product mix. Pool an iPad-only-only correlation, a Catalog-tier correlation, and a Cart/Full correlation separately, or include bundle as a covariate. A pooled cross-bundle correlation is invalid (Cart-bundle accounts have higher engagement AND higher ARR for product-mix reasons, not because engagement causes ARR).
2. **Compute correlation** between each dimension score and (a) 12-month forward retention (binary churn vs. retained) and (b) ARR change YoY (continuous).
3. **Test the weighting scheme's separation power** — AUC for the binary churn outcome, Spearman correlation for the ARR outcome.

### Decision rule

Ship the unweighted V3.0 model unless a weighted scheme **improves AUC by ≥ 0.05** over the unweighted baseline AND that improvement holds within at least two of the three bundle strata. A scheme that wins only inside one bundle is not generalizable and is rejected.

### Look-back option

A one-time look-back study can be run at any time using historical retention/ARR outcomes against the V3.0 score. Single-snapshot correlation is noise-heavy and is treated as **directional only** — it cannot trigger a weighting change on its own. The full prospective validation above is the gating test.

---

## §10 Operational Roadmap

V3 is a scoring model. Its purpose is to power downstream CS workflows. This section tracks what has shipped, what is next, and what is aspirational.

### What has shipped

| Work | Delivered in |
|------|-------------|
| Per-org scores + narratives, monthly CSV output | V3.0 |
| Interpretive composite narrative (plain-English explanation per org) | V3.1 |
| Schema migration, determinism hardening, consistency checker, dead-code cleanup | V3.2.x audit arc |
| `support_fire_days_open` column | V3.2.12 |

### What has shipped since (V3.3.x / V3.4.0)

| Work | Delivered in |
|------|-------------|
| Dimension weighting introduced (`25/20/35/20`), undocumented | V3.3.0 |
| Trigger engine + V2 quality pass (dedup, drivers, oscillation, `--current-only`) | V3.3.x |
| §9 look-back run against real outcomes; weights reverted to equal | V3.4.0 |
| Folder consolidation, interpreter pinning, MAL refresh, `outcomes.csv` populated | V3.4.0 |

### What is next: save plays

**Trigger detection has shipped** — `trigger_engine_v1.py`, outputs in
`trigger_reports/`. Run it after each monthly canonical; it refuses to compare
months scored under different weighting schemes. Trigger conditions in force:
band transition (with a 3.0-pt minimum move), composite drop ≥ 10 pts, chronic
distress, band oscillation, new ghost, and support fire open > 14 days.

**Historical note.**

The original trigger-detection spec, retained for reference:

**Trigger detection (immediate next phase).** Month-over-month comparison against the prior canonical CSV, emitting a `triggers_{date}.csv` sidecar at `runs/{date}/triggers_{date}.csv`. Trigger conditions:

- Dimension score drops ≥ 20 points month-over-month
- Band transition to Watch or worse
- Ghost-account flag fires for the first time
- Support fire flag active for > 14 days (now measurable via `support_fire_days_open`)

**Save plays.** Each trigger pattern maps to a pre-built CS intervention. Delivered as `save_plays.md` at the `Health V3/` root.

Until save plays ship, the highest-leverage save list is `health_band IN ('At Risk', 'Critical') OR ghost_account = true`, sorted by `arr DESC`.

### Aspirational (requires 12+ months of V3 history)

Cohort/churn pattern recognition — what V3 signature did orgs that churned show 30/60/90 days before churn? Requires sufficient labeled-outcome history. Not a prerequisite for trigger detection or save plays.
