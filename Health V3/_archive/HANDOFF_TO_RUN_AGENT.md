# Health V3 — Handoff Brief for Run + Validation Agent

**Status at handoff:** README spec is locked. Operator (`health_operator_v3.py`) is built and dry-run validated against `tam` using live MCP data. Steps 4 (full-portfolio run) and 5 (sanity check) are yours.

**Read first, in this order:**

1. `Health V3/README.md` — the locked scoring spec
2. This file
3. `Health V3/runs/test_2026-05-11/scoring_test_results.md` (reference only — that test predates the README edits, so its numbers don't match V3.0)

---

## Step 4 — Run the operator against the active portfolio

### Prerequisites

Monthly runs use a two-step cache-then-score workflow so the operator never has to open live Postgres or BigQuery connections itself. This permanently sidesteps the credential-setup blocker that has stalled prior runs.

- Python venv: re-use `Health V2/.venv` (same package set: `pandas`, `psycopg2-binary`, `google-cloud-bigquery`). The Postgres/BigQuery libraries are only imported lazily — cache mode does not require them at runtime.
- MCP servers configured in `~/.cursor/mcp.json`:
  - `supercat-postgres-vpn` — used in Step 4a to run the 8 Postgres queries
  - `bigquery-vpn` (or `bigquery-direct`) — used in Step 4a to run the 2 BigQuery queries
- A cache directory at `Health V3/cache/{score-date}/` containing 10 CSV files produced by Step 4a. The operator will fail fast in Step 4b if any of these are missing.

For one-off debugging with live credentials, the original `--pg-cache-dir`-absent invocation still works if `DATABASE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are set in the shell. Cache mode is the recommended path for monthly production runs.

### Step 4a — Populate the cache (no operator credentials needed)

Run all 10 source queries through MCP and write the results to `Health V3/cache/{score-date}/` as CSV. The query bodies are the source of truth for what to execute — copy each one **verbatim** from the corresponding loader function in `Health V3/health_operator_v3.py`, including any `%(parameter)s` bindings.

Postgres (via `supercat-postgres-vpn` MCP — `read_query` or equivalent):

| Loader function          | Cache filename            |
| ------------------------ | ------------------------- |
| `load_pg_org_config`     | `pg_org_config.csv`       |
| `load_pg_engagement`     | `pg_engagement.csv`       |
| `load_pg_smart_stacks`   | `pg_smart_stacks.csv`     |
| `load_pg_orders`         | `pg_orders.csv`           |
| `load_pg_portal_orders`  | `pg_portal_orders.csv`    |
| `load_pg_catalog`        | `pg_catalog.csv`          |
| `load_pg_imports`        | `pg_imports.csv`          |
| `build_domain_map`       | `pg_domain_map.csv`       |

BigQuery (via `bigquery-vpn` or `bigquery-direct` MCP):

| Loader function           | Cache filename            |
| ------------------------- | ------------------------- |
| `load_bq_mp_sharing`      | `bq_mp_sharing.csv`       |
| `load_bq_helpscout_fires` | `bq_helpscout_fires.csv`  |

Notes for the cache-population agent:

- Preserve column names exactly as the SQL emits them. The operator looks them up by name.
- Bool columns may be written as `True`/`False` strings — the operator coerces them back on read.
- Timestamp columns (`last_login_at`, `first_login_at`, `last_run_at`, `first_run_at`, `most_recent_open_at`) should be ISO 8601 strings; the operator passes them through `pd.read_csv(parse_dates=...)`.
- `bq_helpscout_fires.csv` includes a `sample_tags` array column — `str(list)` repr is fine, the operator parses it back.
- Reference precedent: `Health V2/runs/2026-04-06_v2.4.0_full_canonical/pg_cache/` (note V2 uses shorter filenames like `pg_cat.csv` rather than V3's `pg_catalog.csv` — use V3's names listed above).

### Step 4b — Run the operator against the cache

Use the most recent canonical MAL — `Health V2/inputs/master_account_list_2026-04-14_canonical.csv`. There is no fresher file as of handoff; if a newer canonical MAL has been written by the time you run this, use that one instead.

```bash
cd "/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"

"Health V2/.venv/bin/python" "Health V3/health_operator_v3.py" \
  --mal "Health V2/inputs/master_account_list_2026-04-14_canonical.csv" \
  --score-date "$(date -u +%F)" \
  --output-dir "Health V3/runs" \
  --pg-cache-dir "Health V3/cache/$(date -u +%F)"
```

(The flag is called `--pg-cache-dir` — same name V2 uses — even though it now also governs the BigQuery cache files. Consistency across operators is worth more than naming purity here.)

Output goes to `Health V3/runs/{score-date}/`:

- `client_health_scores_{date}.csv` — one row per scored org
- `skipped_new_orgs.csv` — orgs excluded because their oldest login is < 90 days
- `run_metadata.md` — run command, MAL version, row counts, distribution shape

### Single-org debug

If the run errors, isolate by re-running with `--single-org` against a known-good org and `--dry-run` to print to stdout instead of writing CSV:

```bash
"Health V2/.venv/bin/python" "Health V3/health_operator_v3.py" \
  --mal "Health V2/inputs/master_account_list_2026-04-14_canonical.csv" \
  --single-org tam --dry-run
```

`tam` was the dry-run validation org during build. Expected output (V3.0): `engagement 84.3, adoption 60.0, value_delivery 100.0, operational_health 100.0, composite 86.1, band Thriving, ghost_account false`. If you get materially different numbers, something has changed — root-cause before continuing.

---

## Step 5 — Sanity check the V3.0 output

Six checks. **All must pass before V3.0 is ready for CS use.** If any fails, find the root cause and rerun before delivering.

### Check 1 — Math integrity

For every row where `scoring_status = complete`:

- `health_score == round(mean([engagement_score, adoption_score, value_delivery_score, operational_health_score]), 1)` — within 0.1
- Each dimension score is in `[0, 100]`
- No nulls in scored rows; nulls only appear when `scoring_status IN ('partial', 'blocked')`

For `scoring_status = partial`:

- `health_score == round(mean(non_null_dimensions), 1)`
- `dimensions_scored IN (2, 3)`

For `scoring_status = blocked`:

- `health_score IS NULL`
- `dimensions_scored IN (0, 1)`

Exception: when `ghost_account = true`, `health_score = min(unmodified_health_score, 20)`. Verify the override is the only deviation from the average rule.

### Check 2 — Override sanity

Pull the rows where `ghost_account = true`. Confirm for each:

- MAL `arr >= 5000`
- `engagement_narrative` indicates 0 logins in 90 days (or look up `logins_90d` directly in Postgres)
- `health_score <= 20` AND `health_band == "Critical"`

Also pull a few rows where `ghost_account = false` AND `arr >= 5000` AND `health_band == "Critical"`. Confirm those orgs *do* have logins in 90 days (otherwise the override should have fired and didn't).

### Check 3 — Carveout sanity (contract pricing)

The user (Kylor) needs to provide 2–3 known contract-pricing client names — request them before running this check. Likely candidates: `wac`, `fal`. Confirm via SQL:

```sql
SELECT shortname, contract_pricing_enabled FROM organizations WHERE shortname IN ('wac', 'fal');
```

For each contract-pricing org in the V3 output, the catalog completeness percentage should treat their `net_price = 0` products as priced. The `operational_health_narrative` should mention "(contract pricing — price check skipped)" for orgs where the price check would otherwise fire.

Also pick at least one price-level pricing org (Spec Flag #1 fix: `prices_json IS NOT NULL`). Test agent identified `kll` and `mfc` as price-level. They previously scored 0% on Catalog under the old spec; under V3.0 they should score reasonably.

### Check 4 — Applicability sanity (iPad-only)

Pull a known iPad-only org. From the test set, `tam`, `gsa`, `hf` are good candidates. Confirm in their `mobile_sites` row:

```sql
SELECT enable_online_catalog, enable_online_ordering, enable_sales_portal
FROM mobile_sites WHERE organization_id = (SELECT id FROM organizations WHERE shortname = 'gsa');
```

For an org where all three flags are false/null:

- The `adoption_narrative` should not list "eCat Online Catalog" / "Online Ordering" / "Sales Portal" as unused
- The `value_delivery_narrative` should not mention "Online catalog active" / "Portal ordering" / "Sales Portal engagement"
- `bundle_config_mismatch` should be false

If the dimension narratives reference cart/portal features for a true iPad-only org, the applicability gating in the operator is broken.

`bp` is a known anomaly — MAL says iPad-only but mobile_sites has `enable_online_catalog = true` and `enable_online_ordering = true`. Per spec, this org should:

- Have catalog/ordering as applicable features (mobile_sites wins)
- Have `bundle_config_mismatch = true` in the output
- Surface the mismatch in the adoption narrative as a data-hygiene flag, NOT as a usage gap

Confirm both.

### Check 5 — Archetype reasonableness

**Ask Kylor for names before running this check.** You need:

- 5 orgs he'd call clearly **Green** (Healthy / Thriving) without seeing scores
- 5 orgs he'd call clearly **Red** (At Risk / Critical) without seeing scores
- 2–3 known **ghost** candidates (paying ARR, never logs in)
- 2–3 known **non-ghost** orgs (paying and active)

Then check the V3 output:

- For Greens: `health_band IN ('Thriving', 'Healthy')` AND `ghost_account = false`
- For Reds: `health_band IN ('At Risk', 'Critical')` OR `ghost_account = true`
- For ghost candidates: `ghost_account = true` (and verify `arr >= 5000` AND `logins_90d = 0`)
- For non-ghosts: `ghost_account = false`

**Any mismatch is a flag, not a kill.** Record the mismatches and report to Kylor with the dimension-level breakdown so he can judge whether his intuition or the model is off. The model can be wrong (calibration bug). His intuition can also be wrong (he hasn't looked at this org in months). The deliverable here is a list of "V3 says X, you said Y, here's why" — not a pass/fail.

### Check 6 — Distribution shape

Compute and report in `Health V3/runs/{date}/run_metadata.md` (the operator already does some of this — extend the file if needed):

- Band counts: Thriving / Healthy / Watch / At Risk / Critical
- `scoring_status` counts: complete / partial / blocked
- `ghost_account = true` count
- `support_fire = true` count
- `support_data_available = false` count
- `bundle_config_mismatch = true` count
- `denominator_quality = 'stale'` count

**Flag if any band is extreme** — e.g., 60% Critical or 0% Thriving suggests an operator or threshold bug, not a portfolio truth. Healthy/Watch should be the bulk of the distribution; Thriving is rare-but-present (maybe 5–15%); Critical should be a small fraction (under 10%) outside of ghost-account spikes.

---

## What's already validated

The dry-run against `tam` confirmed:

- Operator imports without error
- Postgres queries run cleanly via the MCP (operator translates these to direct psycopg2 calls)
- BigQuery queries against `mixpanel.events` and `helpscout.conversations` work via the standard `bigquery.Client`
- All six scoring helpers produce expected band scores
- Composite math + ghost override + band assignment produce sensible output for a known-healthy org
- The 6-import-type freshness calculation handles all edge cases including the 1-day floor

## Known issues / things to watch

1. **Internal-domain user filter differs from V2.** V3 uses the same exclusion list (`supercatsolutions.com`, `lojic.com`, `railsfever.com`, `samedis.com`, `jimmythrasher.com`, `upwardtechnologies.com`) but applies it slightly differently — V3 filters on `users.email` domain at the org_users join. The denominator may differ from V2 by a small number. This is correct behavior, not a bug.

2. **`tam` enabled_users diverges from the test result.** V3 returns 29 enabled internal users for `tam`; the 2026-05-11 test returned 22. Same band (50–74% → 65 score) so the dimension score is unchanged. The test agent was likely using a stricter filter; not worth reconciling.

3. **HelpScout S1/S2 reversal.** The original test results suggested dropping S1/S2 from the fire trigger because the test agent saw zero open S1/S2 conversations. Schema check (during README lock) confirmed `s1 - critical` and `s2 - high` are real, current, in-use tags (737 and 1,022 historical respectively). V3.0 keeps L3, L4, S1, AND S2 as fire triggers per the locked spec. If the run produces zero `support_fire = true` rows, that's noteworthy but not necessarily a bug.

4. **Subscription table is unreliable for older cohorts.** It was apparently backfilled in mid-2025. V3.0 does not use it for bundle (MAL is authoritative) or for new-org detection (uses `MIN(login_events.created_at)` instead). If subscription history is recovered later, the new-org filter can be tightened.

5. **Mixpanel sharing events have ~80–100 distinct orgs in 90d.** Many orgs in the portfolio will have zero Mixpanel sharing events (because they don't use the iPad sharing feature). That correctly scores 0 on the Adoption sharing point and 0 on the Value Delivery sharing channel. It is *not* a "missing data" condition — `scoring_status` does not become `partial` because of this. Zero is a real signal of zero activity per §6.

6. **V3.0 narratives are descriptive, not interpretive.** The operator reports counts, ratios, and recency (e.g., "412 logins in 90 days from 8 of 20 enabled users. Last login 47 days ago.") rather than explaining *why* a score lands where it does. Interpretive narrative ("engagement count alone overstates current health" / "consider investigating whether users are aware of recent catalog updates") is a V3.1 target. Do not represent V3.0 output to CS as "the model explains why" — it explains *what*. The README §1, §3, §4 example narratives written in interpretive voice describe the V3.1 destination, not the V3.0 output.

7. **Seasonality is acknowledged in the spec but is not modeled in V3.0.** There is no `seasonality_context` field and no per-org cadence baseline; cyclical verticals (furniture, lighting, home goods) measured in their off-season will score artificially low on Engagement and Value Delivery. For Check 5 mismatches involving orgs in those categories during a known slow window, classify the mismatch as "known seasonality gap, not a model bug" rather than chasing it as a calibration issue. Per-org seasonal normalization is a V3.1 target once 12 months of trailing V3 history exists to baseline against.

## When you're done

Update `run_metadata.md` with:

- Per-check pass/fail
- For Check 5: the archetype mismatch list (V3 said X, Kylor said Y, root cause)
- A one-line summary: "Ready for CS use" or "Blocked — see check N"

Hand the run folder back to Kylor.
