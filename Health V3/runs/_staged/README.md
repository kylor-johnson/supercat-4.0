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
| SHA-256 | `9fc4b51925cbe39a49965410b9d2d950e737d1b4f05d50cb4499e1c4ccb71a09` |
| Engine | V3.5.0, `--weights equal` |
| MAL | `master_account_list_2026-09-16_canonical.csv` — 114 orgs, first use |
| Rows | 114, `scoring_status = complete` for all |
| Bands | 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** |
| Determinism | byte-identical on a second pass against the same cache |
| Cache | `cache/2026-09-21/`, immutable since population |

**All three V3.5.0 blockers are now cleared** (ghost banding, `new_ghost`
reachability, the new-org gate + ghost precedence, ops measurement honesty, and
`ghost_subtype`). This run was rescored under V3.5.0 and remains staged only
because promoting it is a decision — it changes the live canonical from a 104-org
April-MAL snapshot to a 114-org September one, and the deltas against it span four
months, not one.

Bands: 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** (the four
ghosts, sub-typed: `aa` and `pol` `no_activity_12m`, `bmc` and `blh`
`lapsed_this_quarter`).

Provenance for the run itself, including the three transcription errors caught by
server-side checksums during cache population, is in `run_metadata.md`.

**Read the deltas as four-month moves.** The prior snapshot is 2026-05-13. The
trigger engine treats consecutive snapshots as adjacent regardless of calendar
distance, so every "month-over-month" figure in the staged trigger report spans
May → September.
