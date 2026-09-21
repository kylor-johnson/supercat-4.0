# Health V3 run metadata — 2026-07-01

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-09-16_canonical.csv" --score-date 2026-07-01 --cache --cache-dir "cache/historical/2026-07-01" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-09-16_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2026-07-01/client_health_scores_2026-07-01.csv`
- Rows scored: 112
- Rows skipped (new-org exclusion or not in Postgres): 2

## Distribution

Health band counts: {'Thriving': 55, 'Healthy': 35, 'Watch': 13, 'At Risk': 5, 'Critical': 4}
Scoring status counts: {'complete': 112}
Ghost accounts: 4
Behavioral floor applied: 14
Support fire flags: 0
Bundle/config mismatches: 0

---

## Historical run — appended per `HISTORICAL_RUN_GUIDE.md`

**Historical runs are approximate.** Fit for trend and trigger detection, not for a
client-facing number. Not to be presented to a client.

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
canonical, not the April one. All 114 of its orgs were paying customers by
2026-06-01 (verified against `subscriptions.start_date`), so using it across all
four backfill months holds the population constant from 2026-06-01 through the
2026-09-21 canonical, leaving one clean discontinuity at 2026-05-13 → 2026-06-01
rather than a smeared one.

**Consequence:** `hmjc` and `tel` are absent from this snapshot even though `tel`
was winding down that quarter. Confirmed absent from the MAL. This is the standard
"current MAL only" limitation in the table above.

### Determinism

Two passes against the same cache under the pinned interpreter:

| Pass | Output | SHA-256 |
|---|---|---|
| 1 | `runs/historical/2026-07-01/client_health_scores_2026-07-01.csv` | `1fc89d37fe4cca93594edc0b737ddf2651664c62ad1328847e565a568828675f` |
| 2 | `/tmp/healthv3-2026-07-01/pass2/2026-07-01/client_health_scores_2026-07-01.csv` | `1fc89d37fe4cca93594edc0b737ddf2651664c62ad1328847e565a568828675f` |

**Byte-identical.**

### Interpreter

Python 3.9.6 · pandas 2.3.3 · numpy 2.0.2, via `.venv/bin/python3`
(`/Library/Developer/CommandLineTools/usr/bin/python3`). Matches `ENVIRONMENT.md`.

### Cache file checksums (README rule 8)

Every file was verified against a **server-side** content checksum computed in
Postgres/BigQuery over the same rendering, and matched exactly. `file_md5` is the
md5 of the CSV on disk; `content_ck` is the rule-8 content checksum that both sides
agreed on.

| File | Rows | file_md5 | content_ck (server == local) |
|---|---:|---|---|
| `pg_org_config.csv` | 258 | `285529e4eb86af8e910b95020f929997` | `0758f1272e133bc8d3cd23687187279d` |
| `pg_engagement.csv` | 258 | `028d9dd3acf1e30c7b7e4c9dc20d1c31` | `5655e992c6cd26f2279aff08645cb242` |
| `pg_smart_stacks.csv` | 191 | `95ddd4486631af7c09415d9204c938c2` | `21656974e674a05d75863cda6a1a1cf5` |
| `pg_orders.csv` | 197 | `1fac9326e6e984c5be3f82372ddc87e5` | `f7506b89a83ffd9db1e4c2eb971c9f7e` |
| `pg_portal_orders.csv` | 38 | `acb490486239d1cfdf815e8fb187b817` | `da513c9b153050eac3ade3b7e8a867a3` |
| `pg_catalog.csv` | 242 | `9dd0964cccb65a68fafad43383a4f2ac` | `199059a6059c4f20bd541babd9388800` |
| `pg_imports.csv` | 774 | `16a1840e6c3ec30d945ab084363869f6` | `5b3d0caab9fbd64ce7de78a54a061a73` |
| `pg_domain_map.csv` | 4979 | `47b3b4fb8f5ca759d8b3b1c7992d5100` | `d8a765e91404201bcd09924ad228b7b3` |
| `bq_mp_sharing.csv` | 112 | `b37301d0ae9518dca2ee52d89e827c0e` | `4505461b4bc45e8c66bebf5ffb614f03` |
| `bq_helpscout_fires.csv` | 0 | `f8cf7591e6c393a2f0a9514c781d70ad` | *(empty result set — header only)* |

Checksum rendering contract used on both sides: `concat_ws('|', COALESCE(col::text,''), …)`
per row, timestamps as `to_char(…,'YYYY-MM-DD HH24:MI:SS.US')`, booleans lowercased,
rows sorted by the **rendered line** under `COLLATE "C"` (byte order) and joined with
`\n`. The local side was rendered from `pandas.read_csv(dtype=str)`.

### Cache-population wall clock

| | UTC |
|---|---|
| Start | **2026-09-21T19:39:51Z** |
| End | **2026-09-21T19:59:10Z** |

Five of the ten loaders read **current** state rather than the score date —
`pg_org_config`, `pg_catalog`, `pg_smart_stacks`, `pg_domain_map`,
`bq_helpscout_fires`. This window is the only way to distinguish a real
month-over-month move from a populate-order artifact between the four backfill
agents.

**Config drift actually observed inside this window** (vs. the `cache/2026-09-21/`
canonical cache):

- `libco` (org 288) — `enable_sales_data` flipped `False` → `true`.
- `pg_catalog` org 224 — `total_active` 442 → 448, `complete_products` 422 → 425.
- `pg_domain_map` — one new domain (`delanceyhouse.com` → `scw`), 4978 → 4979 rows.
- `bq_helpscout_fires` — the single open fire conversation in the 09-21 cache has
  since been closed, so this file is empty. Support Fire is therefore 0 for this
  snapshot; per the limitations table this dimension only ever sees conversations
  still open at populate time.

### Date-substitution rule actually applied

The live anchors were replaced as follows. **This differs from the table in
`HISTORICAL_RUN_GUIDE.md`** — see the run report for the verification that
established it.

| Live | Applied here | Concrete 90d lower bound |
|---|---|---|
| `NOW()` (pg_engagement, pg_orders, pg_imports) | `DATE '2026-07-01' + INTERVAL '1 day'` (exclusive upper) | 2026-04-03 |
| `CURRENT_DATE` (pg_portal_orders) | `DATE '2026-07-01'` | 2026-04-02 |
| BigQuery `CURRENT_DATE()` (bq_mp_sharing) | `DATE('2026-07-01')` | 2026-04-02 |

All windowed loaders additionally capped at `< 2026-07-02 00:00`. No `NOW()` or
`CURRENT_DATE` survived in any query run against a trailing window.
