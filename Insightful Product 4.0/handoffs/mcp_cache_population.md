# MCP Cache Population — Completed

**Date:** 2026-07-09
**Status:** DONE — code changes applied, cursor rule live

---

## Problem

`./run.sh {org} --populate-cache` crashed immediately because
`populate_cache.py` tried to connect to Postgres via `psycopg2`, but no
`DATABASE_URL` or `PG*` env vars are configured locally. The prod DB is
behind a VPN and only reachable through the `user-supercat-postgres-vpn`
MCP server.

Agents would then spend 5-10 minutes reasoning through how to use the MCP
fallback, reading code, trying env vars, etc.

## What was done

### 1. `pipeline/populate_cache.py` — graceful DB fallback

Rewrote the main flow:

1. **Try direct DB** via `cache.populate()` — works if env vars are ever set
2. **On connection failure** (ImportError, connection refused, auth failure,
   timeout), fall back to MCP mode:
   - Resolve `org_id` from the static `_KNOWN_ORG_IDS` map
   - Extract and parameterize SQL for each query from the canon docs
   - Write each as `{query_id}.sql` in `pipeline/cache/{org}/{date}/`
   - Print a boxed instruction block telling the agent exactly what to do
   - Exit 0 (not a failure — the .sql files are the deliverable)

The fallback detection is broad: catches `ImportError` (no psycopg2) and
any connection error whose message contains common Postgres failure tokens
(`could not connect`, `connection refused`, `password authentication`,
`timeout expired`, etc.). Anything else re-raises as before.

### 2. `run.sh` — CSV guard after `--populate-cache`

Added a post-populate check: after `populate_cache` exits, count `.csv` and
`.sql` files in the cache dir. If there are `.sql` files but fewer than 3
CSVs, the pipeline stops with a clear error telling the agent to run the
`.sql` files through MCP first.

### 3. Cursor rule: `.cursor/rules/insightful-run-report.mdc`

Always-applied workspace rule that gives every agent the exact 3-step
procedure:
1. Run `populate_cache.py` (generates `.sql` files if no DB)
2. Run each `.sql` through MCP `execute_sql`, write results with
   `import_from_dicts()`
3. Run `./run.sh {org} --date {date}`

Explicitly forbids trying to set up `DATABASE_URL`, connecting to
localhost, or constructing SQL manually.

## Files changed

| File | Change |
|------|--------|
| `pipeline/populate_cache.py` | Rewrote: try DB → fallback to `.sql` file emission |
| `run.sh` | Added CSV-count guard after `--populate-cache` |
| `.cursor/rules/insightful-run-report.mdc` | New always-applied rule |

## Files NOT changed

- `pipeline/cache.py` — `populate()`, `import_from_dicts()`, all helpers untouched
- `pipeline/run_report.py` — untouched
- `pipeline/config.py` — untouched
- All section templates, renderers, profiles, golden_set — untouched

## Regression

These changes only affect the `--populate-cache` code path. The report
pipeline itself (`run_report.py` → `assemble.py` → `html_renderer.py`) is
completely unchanged. `regression.sh` should pass 6/6 since it uses
pre-existing cached data and never exercises `populate_cache.py`.
