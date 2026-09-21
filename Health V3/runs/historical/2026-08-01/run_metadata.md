# Health V3 run metadata — 2026-08-01

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-09-16_canonical.csv" --score-date 2026-08-01 --cache --cache-dir "cache/historical/2026-08-01" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-09-16_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2026-08-01/client_health_scores_2026-08-01.csv`
- Rows scored: 113
- Rows skipped (new-org exclusion or not in Postgres): 1

## Distribution

Health band counts: {'Thriving': 52, 'Healthy': 39, 'Watch': 15, 'Critical': 4, 'At Risk': 3}
Scoring status counts: {'complete': 113}
Ghost accounts: 4
Behavioral floor applied: 15
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

### MAL used

`inputs/master_account_list_2026-09-16_canonical.csv` — 114 orgs.

The **September** MAL was used deliberately rather than the April one: all 114 of
its orgs were paying customers by 2026-06-01 (verified against
`subscriptions.start_date`). Using it for all four backfill months keeps the
population constant from 06-01 through the 09-21 canonical, leaving one clean
discontinuity at 05-13 → 06-01 rather than a smeared one.

**Consequence:** `hmjc` and `tel` are absent from this run — both churned earlier
in the year and were dropped from the September MAL. Confirmed absent from the
MAL used here. This is the standard "current MAL only" limitation in the table
above, not a data error.

### Score-date anchoring (windows actually used)

`NOW()` was substituted with the **end** of the score date — anchor
`A = DATE '2026-08-01' + INTERVAL '1 day'` — and every trailing window measured
back from `A`, with `created_at < A` bounding the upper edge. This convention was
not taken from the runbook; it was **derived empirically by reproducing the
existing `cache/historical/2026-04-30/`, `2026-03-31/` and `2026-02-28/` caches
byte-for-byte** (see "Runbook deviations" below).

| Window | Range used |
|---|---|
| 30d  | 2026-07-03 00:00:00 → 2026-08-01 23:59:59.999999 |
| 90d  | 2026-05-04 00:00:00 → 2026-08-01 23:59:59.999999 |
| 180d | 2026-02-03 00:00:00 → 2026-08-01 23:59:59.999999 |
| 365d | 2025-08-02 00:00:00 → 2026-08-01 23:59:59.999999 |

`pg_portal_orders` (`order_date`, a DATE column, live form `CURRENT_DATE`) and
`bq_mp_sharing` (BigQuery `CURRENT_DATE()`) instead use the literal rule —
`>= score_date - 90 days`, i.e. from **2026-05-03** — which is what reproduced
the prior months for those two loaders. The one-day difference in window start
between the `NOW()` loaders and the `CURRENT_DATE` loaders is inherited from the
existing series, not introduced here.

Verified post-write: max `last_login_at` = 2026-08-01 23:59:27.945614, max
`last_run_at` = 2026-08-01 23:52:58.623800, min `first_run_at` = 2026-02-03
00:03:17.643776 (= anchor − 180d). No value in any cache file post-dates the
score date.

### Determinism

Two independent passes against the same immutable cache, same interpreter:

| Pass | Output | SHA-256 |
|---|---|---|
| 1 | `runs/historical/2026-08-01/client_health_scores_2026-08-01.csv` | `72c7f4039a72285318bace5121951af267257920eea3cd7bbfce73f9f2f84288` |
| 2 | `/tmp/healthv3-2026-08-01/pass2/2026-08-01/client_health_scores_2026-08-01.csv` | `72c7f4039a72285318bace5121951af267257920eea3cd7bbfce73f9f2f84288` |

**Byte-identical.**

### Interpreter

Python 3.9.6 · pandas 2.3.3 · numpy 2.0.2, via `.venv/bin/python3`
(the environment of record per `ENVIRONMENT.md`). The `.venv` was verified
present, not created.

### Cache file checksums (README rule 8)

`content_md5` is the server-side content checksum
(`md5(string_agg(concat_ws('|', coalesce(col::text,''), …), E'\n' ORDER BY line))`)
computed **in Postgres/BigQuery** and compared against the same rendering of the
written CSV read back with `pandas.read_csv(dtype=str, keep_default_na=False)`.
**All ten matched on the first attempt; no mismatches, no re-transcriptions.**

| File | Rows | content_md5 (server == local) | file_md5 |
|---|---:|---|---|
| `bq_helpscout_fires.csv` | 0 | n/a — zero rows (header only) | `f8cf7591e6c393a2f0a9514c781d70ad` |
| `bq_mp_sharing.csv` | 113 | `e48b3adf18ac71ba5fef81a7f1c67d9e` | `431a64c9c474153711653ecf5f99085a` |
| `pg_catalog.csv` | 242 | `199059a6059c4f20bd541babd9388800` | `9dd0964cccb65a68fafad43383a4f2ac` |
| `pg_domain_map.csv` | 4979 | `d8a765e91404201bcd09924ad228b7b3` | `47b3b4fb8f5ca759d8b3b1c7992d5100` |
| `pg_engagement.csv` | 258 | `80056f7ebb165cd40f5a14af9fa511e4` | `7cbe38c6a763d98f17b8c4e9acafd1a4` |
| `pg_imports.csv` | 781 | `9bdc85b49dd3d15f51f6e19d8dba5b65` | `c1e2cd1fad3820c2d6694bce3d3b9878` |
| `pg_orders.csv` | 197 | `987409a329a02f7fa243e13d82692464` | `89cbd478d20b9e867494d680f1046402` |
| `pg_org_config.csv` | 258 | `0758f1272e133bc8d3cd23687187279d` | `d6ee64acb2f3531f5d149fd15955a91b` |
| `pg_portal_orders.csv` | 39 | `bccf0de7af51f25287d11dec9c6047da` | `8ebcb69d6dc08eee57a05f9a5c3a0208` |
| `pg_smart_stacks.csv` | 191 | `21656974e674a05d75863cda6a1a1cf5` | `95ddd4486631af7c09415d9204c938c2` |

`concat_ws` + `coalesce(col::text,'')` was used rather than the bare `concat_ws`
in the README recipe. `concat_ws` alone keeps a NULL-bearing row in the checksum
(which is the failure the rule exists to prevent) but **skips** the NULL argument,
so `a,NULL,b` and `a,b` render identically. Wrapping each argument in `coalesce`
preserves column position as well as row presence. This is strictly stronger than
the documented recipe and matters here: 74 of 258 `pg_engagement` rows have NULL
`first_login_at`/`last_login_at`, including `aa`, the highest-ARR ghost.

### Cache population wall-clock (UTC)

| | |
|---|---|
| Start | **2026-09-21T19:36:33Z** |
| End | **2026-09-21T19:47:05Z** |
| Duration | ~10.5 minutes |

Five of the ten loaders read **current** state rather than the score date —
`pg_org_config`, `pg_catalog`, `pg_smart_stacks`, `pg_domain_map`,
`bq_helpscout_fires`. If configuration changed mid-backfill while the other
months were being populated in parallel, this window is the only way to
distinguish a real month-over-month move from a populate-order artifact.

**This already bit `bq_helpscout_fires` in this run.** The `cache/2026-09-21/`
canonical cache, populated earlier the same day, captured one open fire
(`renwil.com`, 2 conversations). By 19:44Z the verbatim loader query returned
**zero** rows — those conversations had been closed in the interim. The support-fire
signal is therefore populate-time-sensitive to within hours, not just months.
Five of the seven prior historical caches also have zero helpscout rows, so an
empty file is precedented and the operator handles it.

### Additional limitation observed — `login_events` retention

`min(first_login_at)` across all 258 orgs is **2025-03-21 00:37:31**, and a large
number of long-tenured orgs share that exact date floor. The same orgs showed
first-login dates in 2024-11 in `cache/historical/2026-04-30/pg_engagement.csv`,
which was populated on 2026-09-16. `login_events` is therefore being pruned on a
rolling ~18-month retention, and `first_login_at` is **left-censored at
~2025-03-21** in this cache.

No scoring impact for this month: the new-org gate and `dark_12m_plus` both key
off dates later than the censor point for every affected org (`tcs` first login
2026-05-05; `pol` last login 2025-07-16). But this window closes over time, and a
re-run of an older historical month will not reproduce its original
`first_login_at` values. Relevant to `MAINTENANCE.md` open item 6.

### Scope

Only `cache/historical/2026-08-01/` and `runs/historical/2026-08-01/` were
written. No shared file, no other month's cache or run, no code, no CHANGELOG, no
version bump, no `trigger_reports/`, no dashboard. `check_consistency.py`
re-run after scoring: **9 pass / 0 fail**, unchanged.
