# REJECTED — 2026-09-01, wrong window anchor

Scored 2026-09-21 as part of the Jun–Sep backfill, then rejected before being
folded into the series. **Do not use these numbers.**

## What went wrong

The run used the **literal** reading of `HISTORICAL_RUN_GUIDE.md`'s substitution
table — `NOW()` → `DATE '2026-09-01'` — which bounds the window at the *start* of
the score date and therefore excludes the score date's own activity.

The series convention, verified against every committed snapshot, is
**`anchor = score_date + 1 day`** for the `NOW()`-based loaders. Proof, org 1 at
the already-committed 2026-04-30:

| Convention | logins_90d | Matches committed cache (6028)? |
|---|---|---|
| `[D−90, D)` — the literal guide reading | 6048 | no |
| `[D−90, D+1)` — 91 days | 6112 | no |
| `[(D+1)−90, D+1)` — **anchor = D+1** | **6028** | **yes** |

The other three backfill months (06-01, 07-01, 08-01) each derived this
independently and used it; all three reproduce the convention exactly. This run is
the only outlier.

## Why it mattered enough to reject

The offset is small per-org but broad, and it lands on the one comparison the run
existed to make (09-01 vs the 09-21 canonical):

- 98 of 188 orgs differ on `logins_90d` (mean |Δ| 3.26, max 53)
- **15 orgs differ on `active_users_90d`**, which feeds the active-user ratio directly
- **101 orgs differ on `last_login_at`**, so `days_dark` — and potentially
  `ghost_subtype` — is off by a day for most of the book
- 3,947 login events on 2026-09-01 itself were excluded

The whole point of this backfill was removing spurious month-over-month deltas. A
one-day-offset snapshot at the tightest seam in the series reintroduces exactly
that artifact.

Rejected SHA: `304f413ffb6131e49532a11813a0f61653c619fbad63aa6e4d6ab29478e2894f`

## Reusable on re-run

Five loaders carry no date filter and are therefore anchor-independent. These
files were checksum-verified by the original agent and can be copied forward
rather than re-pulled, provided a fresh server-side checksum is re-proven at the
time of reuse:

- `cache/pg_org_config.csv` · `pg_smart_stacks.csv` · `pg_domain_map.csv`
  (4,979 rows — the expensive one) · `pg_catalog.csv` · `bq_helpscout_fires.csv` (empty)

These five must be re-pulled with the corrected anchor:

| File | Anchor |
|---|---|
| `pg_engagement.csv` | `D+1`, **and** bound `MIN/MAX(created_at)` with an explicit `WHERE` |
| `pg_orders.csv` | `D+1` |
| `pg_imports.csv` | `D+1`, **and** bound `MIN/MAX(created_at)` |
| `pg_portal_orders.csv` | `D` — this loader uses `CURRENT_DATE`, not `NOW()` |
| `bq_mp_sharing.csv` | `D` — BigQuery `CURRENT_DATE()` |
