# Staged runs — produced and verified, not yet promoted to canonical

A run lands here when it has been scored and checked but the decision to make it
the standing canonical is still open. Staging keeps it out of the canonical
series, so `check_consistency.py` and `trigger_engine_v1.py` both ignore it and
the folder stays green while the decision is pending.

To promote a staged run: move it to `runs/{date}/`, regenerate the dashboard and
the trigger report against it, add the CHANGELOG entry with its SHA, and bump the
version in README and METHODOLOGY. `check_consistency.py` must return 8/8 after.

## 2026-09-21 — first run on the September MAL

| | |
|---|---|
| SHA-256 | `592c1bdbaf3cac1d19da9e74a2c6a3d945fe874a0c3382e9a0e8ca89154abf9d` |
| Engine | V3.4.1, `--weights equal` |
| MAL | `master_account_list_2026-09-16_canonical.csv` — 114 orgs, first use |
| Rows | 114, `scoring_status = complete` for all |
| Bands | 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** |
| Determinism | byte-identical on a second pass against the same cache |
| Cache | `cache/2026-09-21/`, immutable since population |

**Why it is staged and not promoted.** Two of the four V3.4.1 findings are fixed
(ghost banding, `new_ghost` reachability); two remain open and both can move
scores, so promoting now would mean promoting twice:

1. The NaT/`None` new-org gate bug, which has to ship together with giving the
   ghost override precedence over the gate — see README §"New-Org Exclusion".
2. `operational_health_score = 100` for orgs with zero import rows, which the
   `clean_ops_dark` narrative then reports as "infrastructure is healthy". All
   four ghosts have this shape, so it is concentrated in the worst accounts.

Provenance for the run itself, including the three transcription errors caught by
server-side checksums during cache population, is in `run_metadata.md`.

**Read the deltas as four-month moves.** The prior snapshot is 2026-05-13. The
trigger engine treats consecutive snapshots as adjacent regardless of calendar
distance, so every "month-over-month" figure in the staged trigger report spans
May → September.
