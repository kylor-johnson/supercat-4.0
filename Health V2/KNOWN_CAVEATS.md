# Health V2 + Peer Benchmark — Known Caveats and Backlog

Last updated: 2026-04-14 (v2.5.1 — ARR sourced from MAL CSV, C-3 resolved)
Status: Non-blocking. All items below are data hygiene or interpretation issues. Neither system is broken.

---

## Operational Caveats

### 1. HubSpot join key gaps (15 orgs)
`org_summary.hubspot_company_id` is missing for 15 orgs. These orgs:
- Score normally (subscription gate passes)
- Carry `hs_join_missing = true` in Health V2 output
- Fall to Tier 3 bundle-only cohort in Peer Benchmark
- Receive `benchmark_confidence = low`

**Fix:** Populate `hubspot_company_id` in the pipeline. Affects Peer Benchmark vertical assignment.

### 2. Stale HubSpot lifecycle (31 orgs as of 2026-04-06)
31 orgs have `hs_lifecycle_stale = true` — HubSpot shows "Lost", "Churn", or no status, but all have active subscriptions. HubSpot lifecycle data lags operational reality.

**Do not use `hs_lifecycle_stale` to infer churn risk.** Use `churn_risk` and `health_score` instead.

### 3. NULL/zero ARR (21 orgs) — **RESOLVED 2026-04-14**
`arr_data_gap = true` for 21 orgs in runs prior to 2026-04-14. The RM-1 risk modifier (ARR > $5K AND zero logins) could not fire for these orgs. RM-1 was underreported.

**Resolved (2026-04-14):** ARR is now sourced from the MAL CSV (pricing master data), not `org_summary`. All 104 scored orgs have contracted `arr` and `mrr` values. `arr_data_gap` should be 0 in runs using the 2026-04-14 canonical MAL. Note: the 21 previously gap'd orgs all have active Mixpanel login data — RM-1 will only fire for orgs where `logins_90d = 0` is independently true, which was confirmed not to be the case for these orgs.

### 4. `Generic B2B Wholesale` vertical (2 orgs: `lpf` / Linon-Powell, `mpc` / Pioneer Morton)
HubSpot vertical is resolved but is a catch-all bucket. Falls to Tier 3. Should be recategorized in HubSpot to `Furniture` / `Home & Decor`.

### 5. Small Portal and Full Tier 1 cohorts
iPad+Catalog+Portal Tier 1 cohorts: Furniture n=4, Lighting n=5.
Full Tier 1 cohorts: Furniture n=6, Lighting n=8.

Percentile ranks are valid but carry high variance at these sizes. **Always surface `peer_group_n` in downstream reports when n < 8.**

---

## Runtime / Engineering Caveats

### 6. `operator.py` filename conflict — resolved

Both scripts were previously named `operator.py`, shadowing Python's stdlib `operator` module when the script's parent directory is in `sys.path`. Running either script from its own directory caused a circular import error, requiring a `/tmp` copy workaround.

**Resolved (2026-04-07):** Both files have been renamed:
- `Health V2/operator.py` → `Health V2/health_operator.py`
- `Peer Benchmark/operator.py` → `Peer Benchmark/peer_benchmark_operator.py`

The old `operator.py` files have been deleted. All documented examples now use the new names. Both operators can now be run directly from their own directories without any workaround.

### 7. `pg_sub.csv` required in cache (resolved v2.5.0)
`Health V2/cache/` previously did not contain `pg_sub.csv`. If a run used `--pg-cache-dir` pointing to the static cache, the subscription gate silently passed all MAL orgs.

**Resolved:** As of v2.5.0, the operator exits with `[FATAL]` if `pg_sub.csv` is absent in cache mode. `pg_sub.csv` must be regenerated before each canonical run. See QUERIES.md cache file table for the Q-PG-SUB query.

---

---

## Resolved Items (v2.5.0 — 2026-04-07)

The following issues were confirmed and resolved as part of the 2026-04-07 Data Trust Audit sequence:

| Issue | Status | Fix |
|---|---|---|
| `total_users` inflated by internal/admin users | **Resolved** | Q-PG-USERS now excludes 6 confirmed/likely internal domains. See QUERIES.md Q-PG-USERS. |
| RM-2 not firing for Portal-bundle orgs | **Resolved** | `presentation_portal_avg` branch added to `evaluate_risk_modifiers()` in `health_operator.py`. |
| `pg_sub.csv` absence causes silent pass-through | **Resolved** | Operator now exits with `[FATAL]` if `pg_sub.csv` is absent in cache mode. |
| `gblx`, `soi`, `tel` partial scoring (absent from pg_users.csv) | **Resolved** | Cache regenerated with corrected Q-PG-USERS query; all three orgs now appear with valid counts. |

---

## Interpretation Notes

### Catalog Completeness: Zero-Scored Orgs Are Often Accurate

Validation (V-3 query, 2026-04-07) confirmed that several orgs with `catalog_completeness = 0` or near-zero are accurately scored — their product records have `net_price = 0.00` or `image_exists = false` for all active SKUs. This is a real data state, not a query bug.

**Interpretation rule:** When `catalog_completeness` is near zero, do NOT assume a query artifact. Check whether the client's catalog records include pricing and images before diagnosing a systemic issue.

**This is expected behavior for:** `cf`, `hh`, `krb`, `pw`, `st`, `jc`, and similar orgs with unpopulated pricing or image fields.

---

## Interpretation Rules for Downstream Consumers

Any report or tool consuming Peer Benchmark output **must surface these three fields** alongside benchmark results:

| Field | Purpose |
|---|---|
| `benchmark_confidence` | `high` = Tier 1 n≥8. `medium` = Tier 1 n 5–7. `low` = fallback or ramping. Do not present `low`-confidence results at the same visual weight as `high`. |
| `peer_group_level` | `tier1` = vertical × bundle. `tier2` = vertical-only. `tier3` = bundle-only. |
| `peer_group_n` | Actual number of steady-state peers used for percentile math. Use this — not `peer_group_level` — to assess statistical reliability. |

**Tier 3 is not automatically worse than Tier 1.** The iPad-only Tier 3 cohort (n=50) is larger than any Tier 1 cohort in the current portfolio. Use `peer_group_n` to assess reliability, not the tier number.

---

## Prioritized Backlog

| Priority | Item | Status | Effort |
|---|---|---|---|
| High | Populate `hubspot_company_id` for 15 orgs missing the join key | Open | Low — pipeline config fix |
| High | Add explicit warning when `pg_sub.csv` is absent from `--pg-cache-dir` | **Done v2.5.0** | — |
| High | Exclude internal/admin users from `total_users` denominator | **Done v2.5.0** | — |
| High | Fix RM-2 for Portal-bundle orgs | **Done v2.5.0** | — |
| High | Fix NULL/zero ARR for 21 orgs blocking RM-1 (C-3) | **Done v2.5.1** | — |
| Medium | Recategorize `lpf` and `mpc` HubSpot verticals | Open | Low — HubSpot data entry |
| Medium | Rename `operator.py` files to avoid stdlib conflict | **Done 2026-04-07** | — |
| Low | Update HubSpot `properties_segment` for `mli` (Maxim Lighting) | Open | Low — HubSpot data entry |
| Low | Calibrate Health V2 absolute thresholds (OD-1) against v2.5.0 run distribution | Open | Medium — analysis pass |
