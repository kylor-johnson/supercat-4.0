# Health V3 run metadata — 2026-09-01

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-09-16_canonical.csv" --score-date 2026-09-01 --cache --cache-dir "cache/historical/2026-09-01" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-09-16_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2026-09-01/client_health_scores_2026-09-01.csv`
- Rows scored: 114
- Rows skipped (new-org exclusion or not in Postgres): 0

## Distribution

Health band counts: {'Thriving': 53, 'Healthy': 40, 'Watch': 13, 'Critical': 4, 'At Risk': 4}
Scoring status counts: {'complete': 114}
Ghost accounts: 4
Behavioral floor applied: 11
Support fire flags: 0
Bundle/config mismatches: 0

---

## Historical run — required disclosures

> **Historical runs are approximate.** They are fit for trend and trigger
> detection, not for a client-facing number. The limitations below are real and
> must be restated in every `run_metadata.md` you produce.

### Known limitations of historical runs

| Dimension | Limitation |
|-----------|------------|
| Engagement | Accurate — `login_events` are timestamped, trailing windows correctly anchored |
| Adoption | Approximately accurate — feature flags (`mobile_sites`) reflect **current** config, not historical. An org that has since disabled a feature will show it disabled, understating its historical adoption. |
| Value Delivery | Accurate — `orders` and `portal_orders` are timestamped |
| Ops Health (imports) | Accurate — `import_events` are timestamped |
| Ops Health (catalog) | **Not historical** — catalog completeness reflects today's catalog. Treat ops scores as approximate for catalog-heavy orgs. |
| Support Fire | Approximately accurate — the query sees only conversations still open. Ones open then but closed since do not appear. |
| MAL | **Whichever MAL you pass** — orgs that churned and were dropped from it will not appear at all. Orgs added after the score date will appear but are usually caught by the 90-day new-org gate. |

### Supersedes a rejected run

This is the **second** 2026-09-01 run. The first (SHA `304f413f…`) anchored the
`NOW()`-based loaders at the *start* of the score date and was rejected before
folding into the series; it is quarantined at
`_archive/rejected/2026-09-01_wrong_anchor/` with its full rationale. Do not use
those numbers.

### Score-date anchoring (windows actually used)

Per `HISTORICAL_RUN_GUIDE.md` §"The historical cutoff substitution rule", the two
anchor families were applied separately:

| Loader | SQL anchor | Historical anchor | Window |
|---|---|---|---|
| `load_pg_engagement` | `NOW()` | `DATE '2026-09-01' + INTERVAL '1 day'` | `[(D+1)−N, 2026-09-02)` |
| `load_pg_orders` | `NOW()` | `DATE '2026-09-01' + INTERVAL '1 day'` | `[2026-06-04, 2026-09-02)` |
| `load_pg_imports` | `NOW()` | `DATE '2026-09-01' + INTERVAL '1 day'` | `[(D+1)−N, 2026-09-02)` |
| `load_pg_portal_orders` | `CURRENT_DATE` | `DATE '2026-09-01'` | `[2026-06-03, 2026-09-01)` |
| `load_bq_mp_sharing` | `CURRENT_DATE()` | `DATE('2026-09-01')` | `[2026-06-03, 2026-09-01)` |

Concrete `NOW()`-family windows: 30d `[2026-08-03, 2026-09-02)` · 90d
`[2026-06-04, 2026-09-02)` · 180d `[2026-03-06, 2026-09-02)` · 365d
`[2025-09-02, 2026-09-02)`. The one-day difference between the two families is a
genuine inconsistency in the model that every committed snapshot reproduces; it
was **not** reconciled here.

The explicit upper bound the SQL does not contain was added to both loaders whose
`MAX/MIN(created_at)` sit outside the `FILTER` clauses:
`WHERE created_at < DATE '2026-09-01' + INTERVAL '1 day'`.

**Convention independently re-derived before use.** Against the committed
2026-04-30 cache, org 1 (`logins_90d = 6028`):

| Convention | logins_90d | Reproduces committed cache? |
|---|---|---|
| `[D−90, D)` | 6048 | no |
| `[D−90, D+1)` (91d) | 6112 | no |
| `[(D+1)−90, D+1)` | **6028** | **yes** |

The full 2026-04-30 org-1 row reproduces under `anchor = D+1`: `logins_30d` 2067,
`logins_180d` 10283, `active_users_90d` 59, `active_users_365d` 78, and
`last_login_at` `2026-04-30T23:42:06.106595` to the microsecond.

**Empirical verification of this cache:**

| Assertion | Value | Pass |
|---|---|---|
| `max(pg_engagement.last_login_at)` falls **on** 2026-09-01 | `2026-09-01 23:59:51.840729` | yes |
| `max(pg_imports.last_run_at)` ≤ 2026-09-01 23:59:59 | `2026-09-01 23:58:22.658027` | yes |
| `min(pg_imports.first_run_at)` ≈ (D+1) − 180d = 2026-03-06 | `2026-03-06 00:03:20.329264` | yes |
| org 1 `logins_90d` cross-check against live Postgres | **4789** | yes |

No `NOW()` or `CURRENT_DATE` survived in any query run.

### MAL used

`inputs/master_account_list_2026-09-16_canonical.csv` (114 orgs) — the September
canonical, dated fifteen days **after** this score date. That is intentional and
matches the other three backfill months: all 114 orgs were paying customers by
2026-06-01, so the roster holds the population constant from 2026-06-01 through
the 2026-09-21 canonical.

**Consequence:** `hmjc` and `tel` are absent; both churned earlier in 2026 and
were dropped from the MAL. Standard "current MAL only" limitation.

Unlike 2026-06-01 (111 scored), 2026-07-01 (112) and 2026-08-01 (113), **all 114
orgs clear the 90-day new-org gate by this date** — `tcs`, the last to clear, does
so on 2026-08-03. No `skipped_new_orgs.csv` was written.

### Determinism

| Pass | Output | SHA-256 |
|---|---|---|
| 1 | `runs/historical/2026-09-01/client_health_scores_2026-09-01.csv` | `670d8774d097b7dfe6174f36daa402face9545a5719b32f399c3eb26019d8e6b` |
| 2 | `/tmp/healthv3-2026-09-01/pass2/2026-09-01/client_health_scores_2026-09-01.csv` | `670d8774d097b7dfe6174f36daa402face9545a5719b32f399c3eb26019d8e6b` |

**Byte-identical.** Differs from the rejected `304f413f…` as required.

### Interpreter

Python 3.9.6 · pandas 2.3.3 · numpy 2.0.2, via `.venv/bin/python3`
(`/Library/Developer/CommandLineTools/usr/bin/python3`). Matches `ENVIRONMENT.md`.

### Cache file checksums (README rule 8)

| File | Rows | file_md5 | content_ck | Provenance |
|---|---:|---|---|---|
| `pg_engagement.csv` | 258 | `26f8a7e775c66bd7dee0248937c43574` | `1e0d5449799e23fdabf8067b9798216c` | re-pulled, anchor `D+1` |
| `pg_orders.csv` | 197 | `a03f973fea145e35947a4c665bdb4156` | `8f08e15cf879ae777cfe714a1ef6841c` | re-pulled, anchor `D+1` |
| `pg_imports.csv` | 776 | `e9ad5ca018378d407a8a62a94394d107` | `e7caa7482ddbeb211f6bab480cba33d9` | re-pulled, anchor `D+1` |
| `pg_portal_orders.csv` | 38 | `b9b8198e62a0e8bab6f5779424b7a2f0` | `c7c29b4a4a8db50aecee9a1527a8fa3d` | re-pulled, anchor `D` |
| `bq_mp_sharing.csv` | 116 | `472080b94cd10fb607bb3dce71e71259` | `7583101c09c6c2f2bfd4da59fdc64aed` | re-pulled, anchor `D` |
| `pg_org_config.csv` | 258 | `d6ee64acb2f3531f5d149fd15955a91b` | `0758f1272e133bc8d3cd23687187279d` | reused, no date filter |
| `pg_smart_stacks.csv` | 191 | `95ddd4486631af7c09415d9204c938c2` | `21656974e674a05d75863cda6a1a1cf5` | reused, no date filter |
| `pg_domain_map.csv` | 4979 | `47b3b4fb8f5ca759d8b3b1c7992d5100` | `d8a765e91404201bcd09924ad228b7b3` | reused, no date filter |
| `pg_catalog.csv` | 242 | `53c83a32d030394cffb68c30e58ae5fb` | `15750d19e6b63a5c85c3380c7459517a` | reused, no date filter |
| `bq_helpscout_fires.csv` | 0 | `f8cf7591e6c393a2f0a9514c781d70ad` | *(empty result set)* | reused, no date filter |

Checksum rendering contract, both sides: `concat_ws('|', COALESCE(col::text,''), …)`
per row, timestamps `to_char(…,'YYYY-MM-DD HH24:MI:SS.US')`, booleans lowercased,
rows sorted by the **rendered line** under `COLLATE "C"`, joined with `\n`. Local
side rendered from `pandas.read_csv(dtype=str, keep_default_na=False)`.

The five **re-pulled** files were each verified against a fresh server-side
checksum computed in the same statement as the data, and all five matched on the
first attempt. The five **reused** files were verified against the md5 table in
the re-run brief — a file-integrity check on a snapshot already proven by
server-side checksum during the rejected run, deliberately *not* re-proven against
the server, since those five loaders read current state and have legitimately
drifted since. `bq_mp_sharing.csv` is the exception: its anchor is `D` and was
already correct, so it was re-pulled, its fresh server checksum matched the
archived file exactly, and the archived file was copied forward rather than
re-transcribed.

Keeping the five current-state files unchanged holds this snapshot inside the same
populate window as its three sibling backfill months (19:36–21:06Z on 2026-09-21),
so a month-over-month delta cannot be an artifact of populate order.

### Cache-population wall clock

| | UTC |
|---|---|
| Rejected run (current-state files date from here) | 2026-09-21T20:49:06Z → 21:06:01Z |
| This run (five re-pulled files) | **2026-09-21T21:41:46Z → 21:53:26Z** |

Five of the ten loaders read **current** state rather than the score date —
`pg_org_config`, `pg_catalog`, `pg_smart_stacks`, `pg_domain_map` and
`bq_helpscout_fires`. At 20 days, this is the least approximate of the four
backfill months on those five dimensions.

`bq_helpscout_fires` is **empty**: the single open fire conversation present in the
`cache/2026-09-21/` canonical cache was closed before this backfill ran, so Support
Fire is 0 for this snapshot. That is a populate-time artifact, **not** a real
09-01 → 09-21 change. `2026-06-01`, `2026-07-01` and `2026-08-01` carry the same
artifact.

### Scope

Written only to `cache/historical/2026-09-01/` and `runs/historical/2026-09-01/`.
Nothing in `_archive/rejected/` was modified. No shared file, no other month's
cache or run, no code, no CHANGELOG, no version bump, no dashboard, no
`trigger_reports/` regeneration. `check_consistency.py` after scoring: **9 pass /
0 fail**, unchanged. Not committed.
