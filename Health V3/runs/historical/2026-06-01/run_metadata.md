# Health V3 run metadata — 2026-06-01

- Command: `python health_operator_v3.py --mal "inputs/master_account_list_2026-09-16_canonical.csv" --score-date 2026-06-01 --cache --cache-dir "cache/historical/2026-06-01" --weights equal --output-dir "runs/historical"`
- MAL: `inputs/master_account_list_2026-09-16_canonical.csv`
- Weighting scheme: `equal` — ENG 0.25 / ADO 0.25 / VAL 0.25 / OPS 0.25
- New-org window: excluded (90-day gate)
- Output CSV: `runs/historical/2026-06-01/client_health_scores_2026-06-01.csv`
- Rows scored: 111
- Rows skipped (new-org exclusion or not in Postgres): 3

## Distribution

Health band counts: {'Thriving': 56, 'Healthy': 33, 'Watch': 14, 'Critical': 4, 'At Risk': 4}
Scoring status counts: {'complete': 111}
Ghost accounts: 4
Behavioral floor applied: 16
Support fire flags: 0
Bundle/config mismatches: 0

---

## Known limitations of historical runs

Restated verbatim from `HISTORICAL_RUN_GUIDE.md` §"Known limitations of historical runs":

| Dimension | Limitation |
|-----------|------------|
| Engagement | Accurate — `login_events` are timestamped, trailing windows correctly anchored |
| Adoption | Approximately accurate — feature flags (`mobile_sites`) reflect **current** config, not historical. An org that has since disabled a feature will show it disabled, understating its historical adoption. |
| Value Delivery | Accurate — `orders` and `portal_orders` are timestamped |
| Ops Health (imports) | Accurate — `import_events` are timestamped |
| Ops Health (catalog) | **Not historical** — catalog completeness reflects today's catalog. Treat ops scores as approximate for catalog-heavy orgs. |
| Support Fire | Approximately accurate — the query sees only conversations still open. Ones open then but closed since do not appear. |
| MAL | **Whichever MAL you pass** — orgs that churned and were dropped from it will not appear at all. Orgs added after the score date will appear but are usually caught by the 90-day new-org gate. |

**Not client-facing.** Trend and trigger detection only, per `MAINTENANCE.md`.

## MAL used, and the `hmjc` / `tel` consequence

MAL: `inputs/master_account_list_2026-09-16_canonical.csv` (114 orgs) — the September
canonical, deliberately used for all four backfill months rather than the April MAL.
All 114 of its orgs were paying customers by 2026-06-01 (verified against
`subscriptions.start_date`; `drf` starts exactly on the score date). Holding the
population constant from 06-01 through the 09-21 canonical leaves **one clean
population discontinuity at 2026-05-13 → 2026-06-01** (104 → 111 scored) rather than
smearing it across four months.

Consequence: **`hmjc` and `tel` are absent** from this snapshot even though `tel` was
still winding down in June 2026. That is the standard "current MAL only" limitation —
orgs that churned before the MAL was cut do not appear at all.

## Determinism

Two passes against the same immutable cache, same interpreter:

| Pass | Output | SHA-256 |
|---|---|---|
| 1 (canonical) | `runs/historical/2026-06-01/client_health_scores_2026-06-01.csv` | `9989b259e8b9b9ef2d2f9f2edd86b57a7f39da1c6c828d80e19364e10bf16703` |
| 2 (verification) | `/tmp/healthv3-2026-06-01/pass2/2026-06-01/client_health_scores_2026-06-01.csv` | `9989b259e8b9b9ef2d2f9f2edd86b57a7f39da1c6c828d80e19364e10bf16703` |

`cmp` reports byte-identical. **PASS.**

## Interpreter

| Component | Version |
|---|---|
| Python | 3.9.6 (`.venv/bin/python3`, `--system-site-packages` off `/usr/bin/python3`) |
| pandas | 2.3.3 |
| numpy | 2.0.2 |

Matches the `ENVIRONMENT.md` environment of record. Determinism is interpreter-scoped;
the SHA above is only a reproducibility claim under this interpreter.

## Cache provenance — README rule 8 content checksums

Every file verified with a **server-side content checksum** compared against the
written CSV, per README rule 8. Server side used
`md5(string_agg(line, E'\n' ORDER BY line COLLATE "C"))` over
`concat_ws('|', COALESCE(col::text,''), …)`; BigQuery used
`TO_HEX(MD5(STRING_AGG(line, '\n' ORDER BY line)))`. Timestamps normalised with
`to_char(…,'YYYY-MM-DD HH24:MI:SS.US')` on the server and re-rendered from
`pandas.read_csv(dtype=str)` locally, so nothing is re-typed on the round trip.

| File | Rows | Content md5 | Server match |
|---|---:|---|---|
| `pg_org_config.csv` | 258 | `0758f1272e133bc8d3cd23687187279d` | ✅ exact |
| `pg_engagement.csv` | 258 | `413ae72251b7a967e1e48ba59b967cb9` | ✅ exact |
| `pg_smart_stacks.csv` | 191 | `21656974e674a05d75863cda6a1a1cf5` | ✅ exact |
| `pg_orders.csv` | 197 | `0ebb03450d6d294eb0efeb8d18d4178b` | ✅ exact |
| `pg_portal_orders.csv` | 38 | `6a0791984dc06a6e8ebec3e1c8e48107` | ✅ exact |
| `pg_catalog.csv` | 242 | `15750d19e6b63a5c85c3380c7459517a` | ✅ exact |
| `pg_imports.csv` | 769 | `8d15c9ae1b35742c3be1873e716384a1` | ✅ exact |
| `pg_domain_map.csv` | 4979 | `d8a765e91404201bcd09924ad228b7b3` | ✅ exact |
| `bq_mp_sharing.csv` | 108 | `1803bc47fc09bbc09b238debc14fbaa7` | ✅ exact |
| `bq_helpscout_fires.csv` | 0 | *(empty set — see note)* | ✅ both sides 0 rows |

Zero mismatches; nothing had to be re-pulled and corrected.

`bq_helpscout_fires.csv` is **header-only**: the loader's `status IN ('active','pending')`
filter returned no conversation carrying an `l3`/`l4`/`s1`/`s2` tag at populate time.
Verified not to be a query fault — the table is live (40 active/pending rows, newest
`createdAt` 2026-09-21T17:46Z) and tag extraction works, but the only severities
currently open are `l1`, `s3`, `s4`. Consequence: **`support_fire` is `False` for all
111 orgs.** md5 of the file's bytes is `264f29fadc02cb545ff41ccbdd4b94b4`; a server-side
`string_agg` over an empty set is `NULL`, so rule 8's recipe degenerates here and row
count is the only available equality check.

### `pg_domain_map.csv` — how the 4,979 rows were transferred

This is the file that produced the only silent corruption this programme has seen
(three transcription errors in the 2026-09-21 run). Rather than re-transcribe ~5,000
rows, the file was built by **verified-bucket splice**:

1. Server-side md5 + row count per `LEFT(domain,1)` bucket (32 buckets) was compared
   against the same per-bucket rendering of `cache/2026-09-21/pg_domain_map.csv`.
2. **31 of 32 buckets matched byte-for-byte** and were reused as-is.
3. Only bucket `d` differed (server 295 rows vs 294). That bucket alone was
   transferred and spliced in.
4. The whole-file checksum then matched the server exactly.

The single real change versus the 09-21 cache is one added row,
`delanceyhouse.com,scw`. 4,684 of 4,979 rows therefore carried **zero**
transcription exposure.

## Cache-population wall clock

| | UTC |
|---|---|
| Populate start | **2026-09-21T20:27:50Z** |
| Populate end | **2026-09-21T20:46:12Z** |

This matters because **five of the ten loaders read *current* state, not the score
date**: `pg_org_config`, `pg_catalog`, `pg_smart_stacks`, `pg_domain_map` and
`bq_helpscout_fires` carry no date filter in `health_operator_v3.py`. If org config,
catalogue contents or HelpScout status change while the four backfill months are being
populated, this timestamp is the only way to distinguish a genuine month-over-month
move from a populate-order artifact between the four agents.

Two such artifacts are already visible in this snapshot and are **not** client
behaviour:

- `bundle_config_mismatch = 0`, against **3** at both 2026-04-30 and 2026-05-13. The
  live 2026-09-21 canonical is also 0, so this reflects present-day config, not a
  June change.
- `support_fire = 0`, against 1 at 2026-04-30 and 9 at 2026-05-13 (the latter
  populated live on its score date). Purely a function of what was open at populate
  time.

## Window convention actually used — differs from the guide's substitution table

The anchor applied to every trailing window was **`DATE '2026-06-02'`**, i.e.
`score_date + 1 day` as an exclusive upper bound, giving windows of exactly N days that
**include the whole of the score date**:

| Window | Interval |
|---|---|
| 30d | `[2026-05-03 00:00, 2026-06-02 00:00)` |
| 90d | `[2026-03-04 00:00, 2026-06-02 00:00)` |
| 180d | `[2025-12-04 00:00, 2026-06-02 00:00)` |
| 365d | `[2025-06-02 00:00, 2026-06-02 00:00)` |

`HISTORICAL_RUN_GUIDE.md` instead specifies `NOW()` → `'{score_date}'::date`, which
would put the upper bound at 2026-06-01 **00:00** and silently score the day *before*
the score date. That form does not reproduce the existing series — see the
"Documentation defects" note below. Verified: `created_at < DATE '2026-06-02'` also
bounds the unfiltered `MIN`/`MAX(created_at)` that produce `first_login_at` /
`last_login_at`, which the guide's table does not mention at all.

## Ghost detail

| Org | ARR | Subtype | Days dark | Band |
|---|---:|---|---:|---|
| `aa` | $42,480 | `never_activated` | never logged in | Critical |
| `bmc` | $21,720 | `lapsed` | 179 | Critical |
| `blh` | $10,620 | `lapsed` | 115 | Critical |
| `pol` | $8,700 | `lapsed` | 319 | Critical |

Critical ARR $83,520. `aa` is correctly **scored, not skipped**: it has no login event
ever and a 2026 cohort year, so the new-org gate claims it, but §5.1 ghost precedence
outranks the gate (`ghost` is evaluated before the gate in `main()`).

`pol` scores `lapsed`, **not** `dark_12m_plus` — see "Documentation defects".

## Additional limitation found in this run — `login_events` retention

`login_events` is subject to a rolling purge. At populate time the earliest surviving
row for any org is **2025-03-21**, so `first_login_at` is left-truncated for every
long-tenured org. The committed 2026-03-31 and 2026-04-30 caches, populated
2026-09-16, still show `first_login_at` back to 2024-11-13; that history is now gone.

No scoring impact on this snapshot — the 90-day new-org gate keys off
`first_login_at`, and 2025-03-21 is 437 days before the score date, so no org flips —
and all four trailing windows (max 365d, back to 2025-06-02) sit inside the retained
range. But `first_login_at` is **not** comparable across snapshots populated at
different times, and a future backfill reaching further back will silently lose window
coverage. This bears on `MAINTENANCE.md` open item 6 (lifetime login counts).

## Documentation defects found — see the run report

1. `HISTORICAL_RUN_GUIDE.md`'s substitution table gives no **upper** bound and, read
   literally, scores the day before the score date.
2. The same table omits that the unfiltered `MIN`/`MAX(created_at)` in
   `load_pg_engagement` must also be bounded.
3. README rule 8's `concat_ws` recipe collapses NULLs ambiguously; this run used
   `concat_ws('|', COALESCE(col::text,''), …)`.
4. README rule 8 has no defined behaviour for an empty result set.
5. `HISTORICAL_RUN_GUIDE.md` Step 3 says `check_consistency.py` is **8/8**; it is 9/9
   (Invariant 9 was added in V3.5.x).

Nothing in this run required a code change. `health_operator_v3.py`,
`trigger_engine_v1.py` and `check_consistency.py` were not modified.
