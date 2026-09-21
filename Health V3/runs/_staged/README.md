# Staged runs — produced and verified, not yet promoted to canonical

A run lands here when it has been scored and checked but the decision to make it
the standing canonical is still open. Staging keeps it out of the canonical
series, so `check_consistency.py` and `trigger_engine_v1.py` both ignore it and
the folder stays green while the decision is pending.

To promote a staged run: move it to `runs/{date}/`, regenerate the dashboard and
the trigger report against it, add the CHANGELOG entry with its SHA, and bump the
version in README and METHODOLOGY. `check_consistency.py` must return 8/8 after.

## Currently staged

Nothing. `2026-09-21` was promoted to `runs/2026-09-21/` on 2026-09-21 after
clearing two independent verification passes — see `CHANGELOG.md` 3.6.0.

## Promotion checklist

1. `mv runs/_staged/{date}/ runs/{date}/`
2. Demote the prior canonical per `RUN_PROMPT.md` step 5.3 — into
   `runs/historical/` and `cache/historical/`, **not** `_archive/`, or the trigger
   series loses that month.
3. Regenerate `trigger_reports/` (no `--production-csv` needed once the run is
   canonical) and build a dashboard for the new date, archiving the prior one.
4. CHANGELOG entry with the new SHA and the distribution delta; bump the version in
   both `README.md` and `METHODOLOGY.md`.
5. `check_consistency.py` must return **9/9**.
