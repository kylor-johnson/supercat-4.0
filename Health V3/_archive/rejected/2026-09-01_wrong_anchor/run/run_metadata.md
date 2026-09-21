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

### MAL used

`inputs/master_account_list_2026-09-16_canonical.csv` (114 orgs) — the September
canonical, dated fifteen days **after** this score date. That is intentional and
matches the other three backfill months: all 114 orgs were paying customers by
2026-06-01, so the roster holds the population constant from 2026-06-01 through
the 2026-09-21 canonical.

**Consequence:** `hmjc` and `tel` are absent from this snapshot; both churned
earlier in 2026 and were dropped from the MAL. This is the standard "current MAL
only" limitation in the table above.

Unlike 2026-07-01 (112 scored, 2 skipped) and 2026-08-01 (113 scored, 1 skipped),
**every one of the 114 orgs clears the 90-day new-org gate by this date** — `tcs`,
the last to clear, does so on 2026-08-03. No `skipped_new_orgs.csv` was written.

### Score-date anchoring (windows actually used)

`NOW()` / `CURRENT_DATE` / `CURRENT_DATE()` were substituted with **`DATE '2026-09-01'`**,
per the substitution table in `HISTORICAL_RUN_GUIDE.md` §"The historical cutoff
substitution rule". Every windowed loader additionally carries an explicit upper
bound at `< 2026-09-01 00:00`, which the live SQL does not need because `NOW()` is
its own ceiling.

| Window | Interval actually measured |
|---|---|
| 30d  | 2026-08-02 00:00:00 → 2026-08-31 23:59:59.999999 |
| 90d  | 2026-06-03 00:00:00 → 2026-08-31 23:59:59.999999 |
| 180d | 2026-03-05 00:00:00 → 2026-08-31 23:59:59.999999 |
| 365d | 2025-09-01 00:00:00 → 2026-08-31 23:59:59.999999 |

Verified: `MAX(last_login_at)` across the cache is `2026-08-31 23:59:50.742642`
and `MAX(last_run_at)` is `2026-08-31 23:58:19.725050`. No value in any cache file
post-dates the anchor. No `NOW()` or `CURRENT_DATE` survived in any query run.

> **Divergence from the neighbouring backfill months — read this before comparing
> snapshots.** `runs/historical/2026-07-01/` and `runs/historical/2026-08-01/`
> both anchored on the **end** of their score date (`DATE '<score_date>' +
> INTERVAL '1 day'`), giving 90d lower bounds of 2026-04-03 and 2026-05-04. This
> run anchors on the **start** of the score date, as `HISTORICAL_RUN_GUIDE.md`
> and `README.md` specify. The two conventions differ by one day of data; for this
> date that is 3,947 login events on 2026-09-01 itself, which this snapshot
> excludes. The series is therefore internally inconsistent by one day at
> 2026-07-01 and 2026-08-01 relative to the documented rule. Flagged, not
> silently reconciled — resolving it means rescoring those two months.

### Determinism

Two passes against the same cache under the pinned interpreter:

| Pass | Output | SHA-256 |
|---|---|---|
| 1 | `runs/historical/2026-09-01/client_health_scores_2026-09-01.csv` | `304f413ffb6131e49532a11813a0f61653c619fbad63aa6e4d6ab29478e2894f` |
| 2 | `/tmp/healthv3-2026-09-01/pass2/2026-09-01/client_health_scores_2026-09-01.csv` | `304f413ffb6131e49532a11813a0f61653c619fbad63aa6e4d6ab29478e2894f` |

**Byte-identical.**

### Interpreter

Python 3.9.6 · pandas 2.3.3 · numpy 2.0.2, via `.venv/bin/python3`
(`/Library/Developer/CommandLineTools/usr/bin/python3`). Matches `ENVIRONMENT.md`.

### Cache file checksums (README rule 8)

Every file was verified against a **server-side** content checksum computed in
Postgres/BigQuery over the same rendering, and every one matched on the first
attempt. `file_md5` is the md5 of the CSV on disk; `content_ck` is the rule-8
content checksum that both sides agreed on.

| File | Rows | file_md5 | content_ck (server == local) |
|---|---:|---|---|
| `pg_org_config.csv` | 258 | `d6ee64acb2f3531f5d149fd15955a91b` | `0758f1272e133bc8d3cd23687187279d` |
| `pg_engagement.csv` | 258 | `82c137a3d373a4343b8a23bea1ddb4fd` | `317aada1a9fbe5c66b317f2d62f1091a` |
| `pg_smart_stacks.csv` | 191 | `95ddd4486631af7c09415d9204c938c2` | `21656974e674a05d75863cda6a1a1cf5` |
| `pg_orders.csv` | 197 | `e8a7df4b49f65e932cd92e12e0c7ed69` | `1c1212c9e4a0707adbfc8e3bc4a183f2` |
| `pg_portal_orders.csv` | 38 | `b9b8198e62a0e8bab6f5779424b7a2f0` | `c7c29b4a4a8db50aecee9a1527a8fa3d` |
| `pg_catalog.csv` | 242 | `53c83a32d030394cffb68c30e58ae5fb` | `15750d19e6b63a5c85c3380c7459517a` |
| `pg_imports.csv` | 777 | `b1fdc7ba517580c2ea0d982b40e2d18a` | `98166715597813b3066da5129da1000f` |
| `pg_domain_map.csv` | 4979 | `47b3b4fb8f5ca759d8b3b1c7992d5100` | `d8a765e91404201bcd09924ad228b7b3` |
| `bq_mp_sharing.csv` | 116 | `472080b94cd10fb607bb3dce71e71259` | `7583101c09c6c2f2bfd4da59fdc64aed` |
| `bq_helpscout_fires.csv` | 0 | `f8cf7591e6c393a2f0a9514c781d70ad` | *(empty result set — header only)* |

Checksum rendering contract used on both sides: `concat_ws('|', COALESCE(col::text,''), …)`
per row (`COALESCE` inside `concat_ws`, so a NULL becomes an empty **field** rather
than vanishing or shifting the field positions), timestamps as
`to_char(…,'YYYY-MM-DD HH24:MI:SS.US')`, booleans lowercased, rows sorted by the
**rendered line** under `COLLATE "C"` (byte order) and joined with `\n`. The local
side was rendered from `pandas.read_csv(dtype=str, keep_default_na=False)`.

Three of the four current-state PG files (`pg_org_config`, `pg_smart_stacks`,
`pg_domain_map`) were populated by copying `cache/historical/2026-08-01/` and then
**proving** equality to a freshly computed server-side checksum, rather than
re-transcribing ~5,200 rows through the agent. This eliminates the transcription
channel that produced the only silent corruption this programme has seen (README
rule 8 preamble). `pg_catalog` did **not** match and was pulled fresh.

Note: `cache/historical/2026-07-01/pg_org_config.csv` and
`cache/historical/2026-08-01/pg_org_config.csv` have different **file** md5s but
identical **content** checksums — 07-01 wrote booleans as `True`/`False`, 08-01 as
`true`/`false`. The operator coerces both. Compare cache files across months by
`content_ck`, never by `file_md5`.

### Cache-population wall clock

| | UTC |
|---|---|
| Start | **2026-09-21T20:49:06Z** |
| End | **2026-09-21T21:06:01Z** |

Five of the ten loaders read **current** state rather than the score date —
`pg_org_config`, `pg_catalog`, `pg_smart_stacks`, `pg_domain_map` and
`bq_helpscout_fires`. At 20 days, **this snapshot is the least approximate of the
four backfill months on those five dimensions**; 2026-06-01 carries ~16 weeks of
staleness on the same fields.

**Current-state drift actually observed** (vs. the `cache/2026-09-21/` canonical
cache, populated ~9.5h earlier):

- `pg_org_config` — one cell: org 288 (`libco`) `enable_sales_data` `False` → `true`.
- `pg_domain_map` — one new domain (`delanceyhouse.com` → `scw`), 4978 → 4979 rows.
- `pg_catalog` — 4 orgs moved (120, 161, 224, 235); largest is org 120
  `complete_products` 1582 → 1623.
- `pg_smart_stacks` — no change.
- `bq_helpscout_fires` — the single open fire conversation in the 09-21 canonical
  cache has since been closed, so this file is **empty**. Support Fire is therefore
  0 for this snapshot. That is a populate-time artifact, **not** a real 09-01 → 09-21
  change; per the limitations table this dimension only ever sees conversations
  still open at populate time. `runs/historical/2026-07-01/` and `2026-08-01/`
  carry the same artifact.

### Scope

Written only to `cache/historical/2026-09-01/` and `runs/historical/2026-09-01/`.
No shared file, no other month's cache or run, no code, no CHANGELOG, no version
bump, no dashboard, no `trigger_reports/` regeneration. `check_consistency.py`
re-run after scoring: **9 pass / 0 fail**, unchanged (it evaluates the latest
`YYYY-MM-DD` directory under `runs/`, which remains `2026-09-21`). Not committed.
