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
| SHA-256 | `2850025eb9de25926e4c633e3d0aed8f39a4010d874cc6e2935b4e176069896e` |
| Engine | V3.5.1, `--weights equal` |
| MAL | `master_account_list_2026-09-16_canonical.csv` — 114 orgs, first use |
| Rows | 114, `scoring_status = complete` for all |
| Bands | 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** |
| Determinism | byte-identical on a second pass against the same cache |
| Cache | `cache/2026-09-21/`, immutable since population |

**All findings from both verification passes are cleared.** V3.4.1 fixed ghost
banding and `new_ghost` reachability; V3.5.0 fixed the new-org gate + ghost
precedence, ops measurement honesty, and added `ghost_subtype`; V3.5.1 closed the
three items the second pass found. This run was rescored under V3.5.1 and remains
staged only
because promoting it is a decision — it changes the live canonical from a 104-org
April-MAL snapshot to a 114-org September one, and the deltas against it span four
months, not one.

Bands: 52 Thriving · 40 Healthy · 14 Watch · 4 At Risk · **4 Critical** (the four
ghosts, sub-typed: `aa` and `pol` `no_activity_12m`, `bmc` and `blh`
`lapsed`).

Provenance for the run itself is in `run_metadata.md` (command, MAL, counts,
distribution). The three transcription errors caught by server-side checksums
during cache population are recorded **only in `CHANGELOG.md` 3.4.1** —
`run_metadata.md` is operator-generated and never contained them. README rule 8
now requires per-file md5s in `run_metadata.md` so a future run's provenance
lives beside the run.

**Read the deltas as four-month moves.** The prior snapshot is 2026-05-13. The
trigger engine treats consecutive snapshots as adjacent regardless of calendar
distance, so every "month-over-month" figure in the staged trigger report spans
May → September.

## Including a staged run in a trigger report

`--history-dir runs/_staged` is a **no-op** — `_staged` is excluded
unconditionally, and before V3.5.1 the engine did not say so, which produced a
confidently wrong report (7 snapshots, the staged month simply absent). It now
warns. Pass the staged run as `--production-csv`, and remember `--history-dir runs`
so the live canonical is included too:

```bash
.venv/bin/python3 trigger_engine_v1.py \
  --history-dir runs/historical --history-dir runs \
  --production-csv runs/_staged/2026-09-21/client_health_scores_2026-09-21.csv \
  --output-dir /tmp/staged-triggers
# expect: 8 snapshots, 107 triggers
```

`trigger_report_2026-09-21.csv` in this folder was produced exactly that way.
