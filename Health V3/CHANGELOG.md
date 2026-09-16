# Changelog — Health V3

All notable changes to the Health V3 operator and surrounding artifacts. Newest entries first.

## 3.2.13 — 2026-05-13

**Doc-only. Scoring math and canonical SHA unchanged: `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8`**

### Documentation
- `README.md` §6 output field list: added `composite_narrative` (between `health_band` and `ghost_account`) and `support_fire_days_open` (between `support_fire_notes` and `support_data_available`). Field list now reflects all 28 canonical columns.
- `README.md` §10 Operational Roadmap: rewritten to separate what has shipped (V3.0 scores, V3.1 interpretive narratives, V3.2.x audit arc, V3.2.12 fire-days column) from what is next (trigger detection → save plays) from what is aspirational (churn pattern recognition, requires 12+ months of history). Removed the prior roadmap table whose "V3.2" row described unshipped churn-pattern work under a version label the audit arc had already used.
- `README.md` line 195: removed stale note claiming interpretive narrative is a "V3.1 target" not produced by the V3.0 operator. Interpretive narratives have shipped since V3.1.
- `FRESH_RUN_GUIDE.md`: corrected canonical column count 27 → 28 and formatted column count 19 → 20 (lines 39, 40, 92, 93). Added `python3 check_consistency.py` step to monthly checklist.
- `OPERATOR_PATCH_PROMPT.md` Step 5.4: replaced hardcoded dashboard filename and line number with a `grep -n "SHA-256:"` instruction so Branch B footer updates remain correct after any dashboard rebuild.

## 3.2.12 — 2026-05-13

**New column: `support_fire_days_open`. Canonical SHA shifts; band assignments unchanged.**

Adds an integer-valued, nullable `support_fire_days_open` column to both the canonical and formatted CSVs. Records days since the most recently opened fire-tagged HelpScout conversation, as of `--score-date`. Null for orgs without an active fire flag. `support_fire` was previously a boolean; the age signal was already computed inside `fires_by_org` via `most_recent_open_at` but discarded — three days vs. forty-seven days is a materially different CS conversation, and this exposes that distinction without changing scoring math.

### Operator
- `health_operator_v3.py` lines 1486–1496: support-fire block now derives `support_fire_days_open = (score_date_dt - fire_ts).days` when a fire is active, where `fire_ts = pd.Timestamp(fire["most_recent_open_at"]).replace(tzinfo=None)`. The `tzinfo=None` normalization makes the math safe across both cache mode (timezone-naive timestamps parsed by `_read_cache_csv` with `parse_dates=["most_recent_open_at"]`) and live BigQuery mode (UTC-aware). Null when `support_fire = False`.
- `health_operator_v3.py` line 1515: new key `"support_fire_days_open"` added to the canonical row-dict, positioned between `support_fire_notes` and `support_data_available`.
- `health_operator_v3.py` line 1555: new entry `"support_fire_days_open"` added to `_fmt_cols`, positioned between `support_fire_notes` and `bundle_config_mismatch`. Formatted CSV grows from 19 to 20 columns.
- No scoring math change. No narrative change. No override behavior change. Purely additive informational column.

### Verification
- **Two-pass byte-identical determinism** confirmed at SHA `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8` under the patched code (`/tmp/health_v3_patch_run_a` vs `/tmp/health_v3_patch_run_b`, same cache, same `--score-date 2026-05-13`).
- **Diff vs V3.2.11**: only structural change is the new `support_fire_days_open` column at position 22. All 27 prior columns retain byte-identical values across all 104 rows. All other column ordering preserved.
- **Column population check**: 9 of 9 orgs with `support_fire = True` have a non-null integer `support_fire_days_open` (range: 7–39 days). 95 of 95 orgs with `support_fire = False` have null `support_fire_days_open`.
- **Old canonical SHA (V3.2.11):** `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`
- **New canonical SHA (V3.2.12):** `b48e3a5f7354ee8d769b764e24ca6195a2424ec5f1416891da9877d6011efcb8`

### Distribution (104 orgs scored — unchanged from V3.2.11)

| Band | V3.2.11 | V3.2.12 | Δ | % |
|---|---|---|---|---|
| Thriving | 57 | 57 | 0 | 54.8% |
| Healthy | 31 | 31 | 0 | 29.8% |
| Watch | 14 | 14 | 0 | 13.5% |
| At Risk | 1 | 1 | 0 | 1.0% |
| Critical | 1 | 1 | 0 | 1.0% |

Behavioral floor: 7 (unchanged). Ghost: 0 (unchanged). Support fire flags: 9 (unchanged). Bundle/config mismatches: 3 (unchanged). Zero per-org band transitions vs V3.2.11.

### Out of scope
- No change to the `support_fire`, `support_fire_notes`, or `support_data_available` semantics. The new column is purely additive.
- The HelpScout SQL and `fires_by_org` aggregation are unchanged — `most_recent_open_at` was already collected; only its consumption changed.
- Narrative engine (`_build_composite_narrative` and per-dimension narrative builders) is unchanged. Fire age is recorded as structured data only; surfacing it in narrative is a future task.

---

## 3.2.11 — 2026-05-13

**New tooling: `check_consistency.py`.**

### Added
- `Health V3/check_consistency.py` — stdlib-only script that verifies eight cross-file invariants identified by the V3.2.x audit arc: version coherence, canonical SHA presence in top CHANGELOG entry, CSV header alignment with operator code, absence of stale column-name references (outside `CHANGELOG.md` and archived paths), dashboard footer SHA agreement with live canonical (with version-lag note), formatted-CSV header alignment with `_fmt_cols`, `--score-date` required-arg enforcement, and floor sub-shape name presence in both operator and README §6.5.

### Documentation
- `README.md` §6.6 gains a "Consistency checking" subsection describing the script and its invariants.

### Verification
- Script run against V3.2.11 state: all 8 checks PASS, exit 0. Invariant 5 prints one `[NOTE]` confirming the dashboard footer (V3.2.8) lags the current system version — expected since V3.2.9 and V3.2.10 were SHA-neutral.
- Deliberate-break tests confirmed for Invariants 1, 2, 4, 7: each correctly returns exit 1 with the failing invariant named in the output.
- Canonical SHA unchanged: `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf` (script is purely additive, no operator code change).

---

## 3.2.10 — 2026-05-13

**Breaking CLI change. `--score-date` is now required.**

### Operator
- `health_operator_v3.py` line 633: `--score-date` no longer defaults to `date.today().isoformat()` (local time). The operator now refuses to run without `--score-date`. Help text updated to reflect that the argument anchors all scoring math and is required for deterministic output.

### Rationale
- README §6.6 makes determinism a core contract. The prior implicit default silently anchored freshness math to the host's local wall-clock date, contradicting the contract. The default was never intentionally used — every documented invocation in the repo and every archived `run_metadata.md` passes `--score-date` explicitly.

### Verification
- Argparse rejection confirmed: invocations without `--score-date` exit 2 with `error: the following arguments are required: --score-date`.
- Canonical SHA unchanged: `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`.
- Two-pass cache-mode verification with `--score-date 2026-05-13`: byte-identical to V3.2.9 baseline.

### Migration note
- Any operator caller that previously omitted `--score-date` will now fail at argparse. None exist in the repo. External callers (none documented) must add the argument.

---

## 3.2.9 — 2026-05-13

**Dead-code and stale-comment cleanup. No scoring math or canonical output change.**

### Operator
- `score_adoption()`: removed third return value `bundle_config_mismatch` (always `False`, discarded by caller, computed independently in `main()` at line 1488).
- `load_pg_orders()`: removed unused `all_orders_90d` SQL output column. Existing `cache/2026-05-13/pg_orders.csv` retains the column; pandas ignores it on load. Next live-PG cache repopulate will produce a 2-column `pg_orders.csv`.
- Stale comment at line ~1540 updated: `# Formatted CSV: ... renamed, ...` → `# Formatted CSV: ... reordered for stakeholder readability` (the rename map was removed in V3.2.8).

### Verification
- Canonical SHA unchanged: `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`.
- Two-pass cache-mode verification: byte-identical to V3.2.8 baseline.

---

## 3.2.8 — 2026-05-13

**Schema migration — BREAKING CHANGE for downstream CSV consumers.**

Canonical CSV column renames:
- `health_score` → `composite_score`
- `score_date` → `run_date`
- `support_fire_note` → `support_fire_notes`

The formatted CSV (`*_formatted.csv`) column names are unchanged — it now becomes a pure column-subset-and-reorder of canonical with no rename map. The two-schema design collapses to one.

- **Operator change:** `health_operator_v3.py` `main()` row-dict keys updated; `_fmt_renames` dict removed.
- **Old canonical SHA (V3.2.7):** `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53`
- **New canonical SHA (V3.2.8):** `63148feb319f4dc434d249ecc47ed90df1adc4c19cf5fc36b9d258bbfcea8ddf`
- **Determinism:** two-pass cache-mode verification confirms byte-identical reproducibility under new code.
- **Out of scope:** `outcomes.csv` `prior_health_score` / `prior_health_band` snapshot columns remain (no join semantics affected). Internal Python variable `score_date` retained (CLI arg `--score-date` unchanged).

---

## 3.2.7 — 2026-05-13 (README §6.5 documents V3.2.4 floor sub-shapes)

### Documentation
- `README.md` §6.5 "Composite Narrative" Override paths section now enumerates all four behavioral-floor sub-shapes (critically-low, full-adoption-dark, clean-infrastructure-dark, standard) with the exact thresholds the operator uses. Previously the README described only "standard" and "very low," reflecting the V3.2.3 binary split rather than the V3.2.4 four-way refactor.
- No code change. Canonical SHA unchanged from V3.2.4: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53`.
- The README table now references operator line numbers (~1414–1463) and explicitly states that any future change to the conditions or narrative framings must update both files together.

---

## 3.2.6 — 2026-05-13 (deterministic tiebreaker in domain map SQL)

### Operator
- `build_domain_map()` SQL now uses `ORDER BY n DESC, org_shortname ASC` inside the `ranked` CTE. Previously, when two orgs shared the same user count for a domain, the `ROW_NUMBER()` assignment was not deterministic — a forward-looking hole in the live extract that did not affect cache-mode runs (which read `pg_domain_map.csv` as-is) but could have produced silently different cache files across repopulation runs.
- Affects live-mode runs and any future cache repopulation. Cache-mode canonical output against `cache/2026-05-13/` is unchanged.
- Canonical SHA: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53` (unchanged).

---

## 3.2.5 — 2026-05-13 (run_metadata.md fidelity fix)

### Operator metadata
- `run_metadata.md` `Command:` line now records `--cache --cache-dir` when those flags were used. Previously the recorded command silently omitted them, so the metadata trail was not replayable.
- Affects `runs/{date}/run_metadata.md` only. Canonical CSV and SHA are unchanged from V3.2.4.
- Canonical SHA: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53` (unchanged).

---

## 3.2.4 — 2026-05-13

### Composite narrative rewrite — exec-readable, one field

- Rewrote `_build_composite_narrative()` to produce plain-English narratives
  readable by both CS reps and exec/CEO audiences. No internal jargon
  ("behavioral floor," "capping," "save play," etc.) in any output.
  Shape logic (5 shapes + fallback) is preserved; output language is new.
- Removed `exec_narrative` field (added in V3.2.3). The rewritten
  `composite_narrative` supersedes it — one field now serves both audiences.
- Three specific quality fixes applied:
  1. Floor accounts now differentiated by profile (full-adoption-dark,
     clean-infra-dark, critically-low, standard) instead of identical text.
  2. "Near the boundary" framing restricted to composites 80–84 only.
     Composites 85+ use "mixed profile Thriving" framing.
  3. Value delivery = 0 now named explicitly ("no measurable business
     outcomes") rather than described as "primary liability."
- Formatted CSV returns to 19 columns (exec_narrative removed).
- All score and band columns are byte-identical to V3.2.3.
  New canonical SHA: `e016ed8a5af2e9f64c0f7e7d11217198dae50000df797e79b1e96639aae63c53`

---

## 3.2.3 — 2026-05-13

### New field: exec_narrative

- Added `exec_narrative` column to the **formatted CSV only** (`_formatted.csv`). Plain-English per-org summary (1–2 sentences, no internal jargon) for non-CS audiences. Written by a new `_build_exec_narrative()` function using the same shape-driven approach as `_build_composite_narrative()` but with exec-audience framing.
- `composite_narrative` is unchanged — this is a purely additive column.
- `exec_narrative` is computed in `main()` immediately after `composite_narrative` and stored in the working DataFrame, but excluded from the canonical CSV write via `df.drop(columns=["exec_narrative"]).to_csv(...)`. This keeps the canonical record stable and its SHA unaffected by additive narrative columns.
- Formatted CSV now has 20 columns (`exec_narrative` at position 9, after `composite_narrative`).
- Canonical SHA unchanged: `5d7dc1fdbe70f42f9931665abfbc785b2fa5dc5c988b43123401eadf89e519fc` (verified two-pass).

---

## 3.2.2 — 2026-05-13 (first canonical on fresh data + cache-population workflow documented)

The V3.2.1 canonical was built against `cache/2026-05-11/`. This version supersedes it with the first canonical produced via the architecturally correct workflow: MCP-driven cache population followed by the deterministic cache-mode operator run. **Operator code is unchanged from V3.2.1** — this is a canonical-artifact refresh and a documentation patch, not a code change.

### What changed

- **New canonical artifact:** `runs/2026-05-13/client_health_scores_2026-05-13.csv` — SHA-256 `5d7dc1fdbe70f42f9931665abfbc785b2fa5dc5c988b43123401eadf89e519fc`. Built from `cache/2026-05-13/` (10 CSVs populated via the `user-supercat-postgres-vpn` and `user-bigquery-vpn` MCPs).
- **README — new section "How to populate the cache"** added before the existing "How to run" section. Documents the 10-file MCP-driven workflow (loader-function mapping, named-param substitution, format requirements, post-write verification, sanity checks). Closes the documentation gap that surfaced when the first attempt at the live extract assumed the operator could populate its own cache (it cannot — see §6.6).
- **README version bumped to 3.2.2 and date to 2026-05-13.** Status text updated to remove the "for initial CEO read" qualifier; the system is now production-ready for routine use.
- **V3.2.1 cache-mode baselines archived:**
  - `runs/2026-05-11/` → `_archive/runs/v3.2.1-cache-baseline_2026-05-11/`
  - `cache/2026-05-11/` → `_archive/cache/v3.2.1-cache-baseline_2026-05-11/`

### Score-date anchor

`$SCORE_DATE` was determined via `date -u +%F` and resolved to **2026-05-13** (UTC). This intentionally diverges from the local-time date because the data inside Postgres queries is anchored to PG `NOW()` (UTC); aligning the cache directory name and `--score-date` with the data's actual anchor preserves the determinism contract.

### Distribution (104 orgs scored)

| Band | V3.2.1 (cache 2026-05-11) | V3.2.2 (cache 2026-05-13) | Δ |
|---|---|---|---|
| Thriving | 57 | 57 | 0 |
| Healthy | 32 | 31 | -1 |
| Watch | 13 | 14 | +1 |
| At Risk | 1 | 1 | 0 |
| Critical | 1 | 1 | 0 |

Behavioral floor: 7 (identical cohort: `cf, hh, hmjc, krb, mfc, st, tel`). Ghost: 0. Net band shift: 1 Healthy → 1 Watch.

### Delta vs V3.2.1 baseline

**5 band changes** (3 are sub-2-point boundary brushes; 2 are real value-delivery swings):

| Org | V3.2.1 | V3.2.2 | Composite Δ | Driver |
|---|---|---|---|---|
| `ap` | Healthy | Watch | 60.6 → 59.4 (−1.2) | ops (−4.8), crossed 60 boundary |
| `asi` | Thriving | Healthy | 84.3 → 78.9 (−5.4) | value delivery (−20.0) |
| `eglo_can` | Healthy | Thriving | 78.1 → 89.0 (+10.9) | value (+33.3), engagement (+10) |
| `sca` | Thriving | Healthy | 80.9 → 79.8 (−1.1) | ops (−4.4), crossed 80 boundary |
| `yw` | Healthy | Thriving | 79.0 → 80.7 (+1.7) | ops (+3.6), crossed 80 boundary |

**6 composite shifts > 5 points** (all bands unchanged unless listed above):

| Org | Composite Δ | Driver |
|---|---|---|
| `eglo_can` | +10.9 | value +33.3, engagement +10.0 |
| `mli` | −8.4 | value −33.3 |
| `ssi` | −8.4 | value −33.4 |
| `etl` | +6.9 | ops +27.7 |
| `soi` | +5.9 | ops +23.6 |
| `asi` | −5.4 | value −20.0 |

All shifts concentrated in `value_delivery` and `operational_health` — the two inherently volatile dimensions (a single order or import-feed event crossing a 90-day window can produce a 20–33pt step on small denominators). 98 of 104 orgs (94%) shifted composite by < 5 points.

### Cache deltas vs `cache/2026-05-11/`

| File | 05-11 | 05-13 | Δ |
|---|---|---|---|
| pg_org_config | 248 | 248 | 0 |
| pg_engagement | 248 | 248 | 0 |
| pg_smart_stacks | 181 | 181 | 0 |
| pg_orders | 186 | 186 | 0 |
| pg_portal_orders | 35 | 35 | 0 |
| pg_catalog | 233 | 233 | 0 |
| pg_imports | 759 | 758 | -1 |
| pg_domain_map | 4,848 | 4,850 | +2 |
| bq_mp_sharing | 106 | 107 | +1 |
| bq_helpscout_fires | 10 | 10 | 0 |

All deltas under 1%, well inside the 50% suspicion threshold.

### Validation

- **Two-pass byte-identical determinism** confirmed at SHA `5d7dc1fdbe70f42f9931665abfbc785b2fa5dc5c988b43123401eadf89e519fc`.
- **Independent cold-read review** (separate agent, 9 checks) cleared all checks. Notable verification: `mfc` operational_health jumped 46.7 → 64.8 between the two runs, but the composite remained floor-capped at 40 with band unchanged at Watch. The +18 ops jump is backed by 3 new successful Products import runs in `cache/2026-05-13/pg_imports.csv` (most recent on 2026-05-12, one day before score date) — a real cache-level activity change, not a calculation artifact.
- **All 7 narrative spot-checks preserved expected shape.** The two with shifted wording (`kii`, `mfc`) shifted only because dimension scores ticked, not because the narrative branch changed.

---

## 3.2.1 — 2026-05-12 (post-review polish)

Triaged from a cold-read review of V3.2.0. All findings were minor (no scoring or pipeline blockers). This patch addresses the items that change CSV content or that the CHANGELOG misstated.

### Narrative engine

- **Re-introduced engagement-rate qualifier in Shape 2 (breadth gap).** The first sentence now reads `"<org>'s reps are logging in at a limited rate (engagement <e>)"` when `engagement < 70`, or `"...consistently (engagement <e>)"` when `engagement ≥ 70`. The V3.2.0 simplification had dropped the qualifier entirely, which preserved the semantic intent (no overstatement of activity) but lost the spec'd phrasing for borderline-engagement accounts. Verified across all 10 breadth-gap accounts in the canonical run: 3 correctly receive "at a limited rate" (`gc`, `ihm`, `sp`), 7 correctly receive "consistently" (`bp`, `yw`, `ah`, `soi`, `eli`, `arl`, `gcl`).
- **Docstring fix:** `_build_composite_narrative` docstring now says "Five shape categories" (was "Four"). Stale text from an earlier draft of the V3.2 refactor.

### Documentation

- **Softened the threshold-stripping claim** in V3.2.0's `METHODOLOGY.md` bullet. Was "Stripped of all specific numerical thresholds." Now reflects reality: stripped of fine-grained per-signal thresholds; composite-level thresholds (band cutoffs, dimension weights) retained because they belong in an executive explainer.
- **Corrected the line-count claim** for the simplified narrative engine (`140` → `~165`). The 244 → 167 reduction is real (32% fewer lines, 7 patterns → 5 shapes + fallback); the round number was just imprecise.

### Determinism — verified end to end

- **Two-pass byte-identical reproduction** at `--score-date 2026-05-11` against the existing cache: SHA `d1f03c2f886f875faeb51e66abf124bf91a13c0188b8343b7380393d7f2e221d` reproduced exactly.
- **Future-date dry run** at `--score-date 2026-06-12` against the same cache: also two-pass byte-identical (SHA `bc816777efd436622ae225f8ba923173474553601ba3aa6db7036a6f94ab99db`). Confirmed all expected drifts are anchored to score-date math, not wall-clock:
  - Day counts in `operational_health_narrative` advanced by exactly 32 days (e.g., `dals` Products feed: `73d ago` → `105d ago`).
  - `engagement_score`, `adoption_score`, `value_delivery_score` unchanged across all 104 orgs (zero wall-clock dependence).
  - `operational_health_score` shifted for 91 of 104 orgs (correct behavior — feeds that are 60d fresh today will be 92d stale a month from now).
  - Behavioral floor count unchanged (7 → 7) — floor depends on engagement and value delivery, not freshness.
  - Test artifacts archived to `_archive/determinism_tests/2026-05-12/future_date_06-12/`.

### Canonical run

- V3.2.1 canonical CSV — SHA-256: `d1f03c2f886f875faeb51e66abf124bf91a13c0188b8343b7380393d7f2e221d`. Replaces the V3.2.0 SHA `c85e7a3cce14333a65e6c40482e99af1338e590c8917bedc066d17bec3b2ab20` (only the `composite_narrative` column changed for the 10 breadth-gap orgs; all scores and bands are unchanged). Originally at `runs/2026-05-11/client_health_scores_2026-05-11.csv`; archived under V3.2.2 to `_archive/runs/v3.2.1-cache-baseline_2026-05-11/client_health_scores_2026-05-11.csv`.

### Distribution (unchanged from V3.2.0)

| Band | Count |
|---|---|
| Thriving | 57 |
| Healthy | 32 |
| Watch | 13 |
| At Risk | 1 |
| Critical | 1 |

Ghost: 0. Behavioral floor: 7. Support fire flags: 9. Bundle/config mismatches: 3.

---

## 3.2.0 — 2026-05-12

### Operator behavior

- **Behavioral floor override (§5.2 in `README.md`).** When `engagement < 55` AND `value_delivery < 40`, the composite score is capped at 40 (top of Watch) regardless of how strong adoption or operational health are. Prevents an account where reps have effectively gone dark from scoring Healthy on the strength of clean infrastructure.
- **Deterministic cache-mode runs.** All wall-clock time dependencies in scoring and narrative logic now anchor to `--score-date` rather than `datetime.utcnow()`. Cache-mode runs are now byte-identical regardless of when the operator is invoked. Previously, freshness-based ops sub-signals drifted by 1–6 points per dimension depending on the gap between data extraction and operator execution; that drift is gone. Verified by SHA-256 comparison across multiple runs against the same cache.
  - Specific changes in `health_operator_v3.py`:
    - `score_operational_health` and `_build_ops_narrative` now take an `as_of` parameter (passed `score_date_dt` from `main`) and use it for all freshness math.
    - New-org exclusion in `main` now compares against `score_date_dt`, not `today`.
- **Idempotent output directory.** Re-running with `--output-dir runs/2026-05-11` no longer creates a `runs/2026-05-11/2026-05-11/` nest. The operator now writes to `{output_dir}/{score_date}/` only when `{output_dir}` doesn't already end in the score date.

### Composite narrative engine — simplified

- The composite narrative engine in `_build_composite_narrative()` was rewritten to be score-shape driven rather than pattern-template driven:
  - **Before**: 7 patterns (244 lines), with `Pattern 1` lumping all all-strong accounts into a single narrative regardless of whether the composite was 81 or 98, and a 25-entry `action_map` lookup.
  - **After**: 5 explicit shapes + a mixed-profile fallback (~165 lines). All-strong accounts split into three sub-shapes (clean Thriving, borderline Thriving, all-strong Healthy) that each warrant a different action tone. Fallback uses a 12-entry band-aware action lookup.
- **Differentiated all-strong narratives.** Previously, `ih` (composite 98, all dims 91+) and `gl` (composite 81, engagement 72) received the *identical* "performing at a high level… consistent performance across every pillar" narrative. Now `ih` reads "performing across the board, no CS action required" and `gl` reads "in the Thriving band, but near the boundary — engagement (72) is the relative drag… a check-in would solidify Thriving status before drift sets in."
- **Score-aware override paths.** The behavioral-floor narrative used to be a single template string that produced identical text for every floor-applied account. Now:
  - `tel` (composite 15, engagement 13, value delivery 0) reads "Behavioral floor applied, but the composite (15) is well below the floor cap on its own merits… immediate save-play candidate."
  - `mfc` (composite 40, engagement 50, value delivery 33) reads "Behavioral floor applied — engagement (50) and value delivery (33) are both below threshold… CS should treat this as a near-ghost."
- **Numbers are surfaced in every narrative.** Each shape now embeds the actual dimension scores (e.g., "engagement (67)", "ops (10)") rather than referring to dimensions abstractly. Makes the narrative interpretable without cross-referencing the score columns.

### Narrative content fixes (carried forward from earlier V3.2.x work)

- `asi.ops_narrative` names Portal Invoices as the outlier feed instead of declaring all feeds "running on cadence."
- `sbl.ops_narrative` uses "critical" (not "declining") for the Customers feed.
- `ihm.adoption_narrative` enumerates all three unused features (Smart Stacks, Inventory Management, Sales Data).
- `dals.ops_narrative` includes a day count for the errored Products feed.
- `asi.value_delivery_narrative` says "no portal orders in 90d" rather than "haven't opened it" when Sales Portal engagement is a gap.
- `dals.composite_narrative` includes an explicit critical-ops sentence when ops_score is 10.
- `ihm.composite_narrative` uses "at a limited rate" rather than "consistently" when reps are logging in below threshold.

### Documentation

- **`README.md` is now the single authoritative spec.** Sections updated for V3.2: §5.2 Behavioral Floor Override, §6.5 Composite Narrative (rewritten to describe the simplified engine), §6.6 Determinism and Reproducibility. Stale §11 Cache Regeneration Note removed.
- **`METHODOLOGY.md` is the executive-facing explainer.** Restored from the archive after a brief attempt to merge it into `README.md`. Stripped of fine-grained per-signal thresholds (login bands, ratio bands, freshness bands) — those live in `README.md`. Composite-level thresholds (band cutoffs, dimension weights) are retained because they belong in an executive explainer. The methodology file now explains *what each dimension means and why* without duplicating the per-signal spec.

### Data hygiene

- **`outcomes.csv` created** with the header `org_shortname,outcome_date,outcome_type,prior_health_score,prior_health_band,notes`. Empty for now — will be populated as labeled outcomes (churn / renewal / expansion / save) become available, to support V3.3 weight calibration.

### Cleanup

- **`_archive/` directory** created. Moved into it:
  - Pre-cleanup full backup tarball (`Health_V3_pre_cleanup_2026-05-12.tar.gz`).
  - Transient audit/review docs: `COLD_READ_AUDIT.md`, `NARRATIVE_FIX_REVIEW_2026-05-12.md`, `OPERATOR_AUDIT_2026-05-12.md`, `HANDOFF_TO_RUN_AGENT.md`, `METHODOLOGY.html`.
  - Old `raw_signals_extractor.py` (functionality is folded into the operator).
  - All intermediate `runs/` subfolders (`v3.1`, `v3.1-narratives`, `v3.2-composite-narrative`, `raw_2026-05-11`, `research_2026-05-11`, `test_2026-05-11`, `spot_check_7_clients_2026-05-12_folder`, etc.) and the initial pre-V3.2 `2026-05-11` run.
  - `_preview_narratives_2026-05-12.md` (the 7-org side-by-side used to validate the simplified engine before implementation).
- The canonical V3.2 output had CSV checksum (SHA-256): `c85e7a3cce14333a65e6c40482e99af1338e590c8917bedc066d17bec3b2ab20`. Originally at `runs/2026-05-11/`; superseded by V3.2.1 at the same path on the same day, then archived under V3.2.2 to `_archive/runs/v3.2.1-cache-baseline_2026-05-11/`.

### Distribution (104 orgs scored)

| Band | Count |
|---|---|
| Thriving | 57 |
| Healthy | 32 |
| Watch | 13 |
| At Risk | 1 |
| Critical | 1 |

Ghost accounts: 0. Behavioral floor applied: 7. Support fire flags: 9. Bundle/config mismatches: 3.

---

## 3.1 — 2026-05-11 (earlier same-week iteration, archived)

Initial post-cleanup narrative pass. State is preserved in `_archive/runs/v3.1/` and `_archive/runs/v3.1-narratives/` for reference. Superseded by 3.2.

---

## 3.0 — 2026-05-10 (initial V3 run)

First end-to-end V3 run. Preserved in `_archive/runs/initial_2026-05-11/`. Superseded.
