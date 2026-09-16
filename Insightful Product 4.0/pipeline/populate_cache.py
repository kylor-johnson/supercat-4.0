"""CLI: populate cache/{org}/{date}/ with the standard query suite.

    .venv-renderer/bin/python -m pipeline.populate_cache --org sarreid
    .venv-renderer/bin/python -m pipeline.populate_cache --org cci --date 2026-06-30
    .venv-renderer/bin/python -m pipeline.populate_cache --org hfg --queries Q-ECON-00,Q-CHAN-00,RP-2

Default --date is today's UTC date (matching the Health V3 score-date
convention).

DB connection: Tries psycopg2 via DATABASE_URL / PG* env vars. When no
connection is available (the normal case — the prod DB is only reachable
through the VPN MCP server), falls back to writing parameterized .sql files
and printing step-by-step MCP instructions for the agent.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

from . import cache, config


def _try_direct_db(org: str, date: str, query_ids: list[str]) -> cache.CachePaths | None:
    """Attempt cache population via direct psycopg2 connection.
    Returns CachePaths on success, None if DB is unreachable.
    """
    try:
        return cache.populate(org=org, date=date, query_ids=query_ids)
    except ImportError:
        return None
    except Exception as e:
        # Any psycopg2 OperationalError or InterfaceError is a connection
        # problem — the DB isn't reachable locally.
        cls = type(e).__name__
        if cls in ("OperationalError", "InterfaceError"):
            return None
        raise


def _emit_sql_files(org: str, date: str, query_ids: list[str]) -> int:
    """Write parameterized .sql files and print MCP-mediated population
    instructions. Returns the count of .sql files written.
    """
    org_id = cache.resolve_org_id(org)
    paths = cache.CachePaths.for_run(org, date)
    paths.dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    missed = 0

    for qid in query_ids:
        csv_path = paths.csv_for(qid)
        if csv_path.exists() and csv_path.stat().st_size > cache._CSV_MIN_BYTES:
            print(f"  skip  {qid}  (CSV already cached)")
            skipped += 1
            continue
        try:
            sql = cache.extract_sql(qid)
        except FileNotFoundError:
            print(f"  MISS  {qid}  (no SQL in canon)")
            missed += 1
            continue
        sql = cache.parameterize(sql, org_id, org)
        sql_path = paths.dir / f"{qid}.sql"
        sql_path.write_text(sql, encoding="utf-8")
        print(f"  emit  {qid}  -> {qid}.sql")
        written += 1

    return written


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--org", required=True, help="Org shortname (sarreid, cci, hfg, kal, sca, ...)")
    p.add_argument("--date", default=None, help="YYYY-MM-DD (UTC). Defaults to today UTC.")
    p.add_argument(
        "--queries",
        default=None,
        help="Comma-separated query IDs. Defaults to config.QUERIES_ALL.",
    )
    p.add_argument(
        "--preflight-only",
        action="store_true",
        help="Just Q-ECON-00, Q-CHAN-00, RP-2 (Phase 1 smoke).",
    )
    args = p.parse_args()

    score_date = args.date or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")

    if args.preflight_only:
        query_ids = config.QUERIES_PREFLIGHT
    elif args.queries:
        query_ids = [q.strip() for q in args.queries.split(",") if q.strip()]
    else:
        query_ids = config.QUERIES_ALL

    print(f"populate_cache: org={args.org} date={score_date} queries={len(query_ids)}")

    # ── Try direct DB first ──────────────────────────────────────────────
    result = _try_direct_db(args.org, score_date, query_ids)
    if result is not None:
        print(f"  wrote: {result.dir}")
        return 0

    # ── No DB — write .sql files for MCP-mediated population ─────────────
    print(f"  no DB connection (DATABASE_URL not set / psycopg2 unavailable)")
    print(f"  falling back to MCP-mediated population\n")

    written = _emit_sql_files(args.org, score_date, query_ids)

    if written == 0:
        print("\n  all queries already cached — no MCP work needed")
        return 0

    cache_dir = config.CACHE_DIR / args.org / score_date
    print(f"""
  ┌──────────────────────────────────────────────────────────────┐
  │  MCP-MEDIATED CACHE POPULATION                              │
  │                                                              │
  │  {written} parameterized .sql files written to:                  │
  │  {cache_dir.relative_to(config.WORKSPACE_ROOT)!s:<56s} │
  │                                                              │
  │  For each .sql file:                                         │
  │  1. Read the SQL from the file                               │
  │  2. Run it via MCP: user-supercat-postgres-vpn execute_sql   │
  │  3. Write the result:                                        │
  │     cache.import_from_dicts(qid, '{args.org}', '{score_date}', rows) │
  │                                                              │
  │  After all CSVs exist, re-run:                               │
  │     ./run.sh {args.org} --date {score_date}                            │
  └──────────────────────────────────────────────────────────────┘""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
