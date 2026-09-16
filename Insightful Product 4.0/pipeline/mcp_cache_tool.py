"""Agent-mediated cache population helper (no local DB creds needed).

For one-off clients when there's no direct psycopg2 connection. Pairs with the
`user-supercat-postgres-vpn` MCP server. Two steps:

  1. emit-batch: prints ONE combined SQL statement that wraps every query as
     `json_agg(row_to_json(...))`, so a single MCP `execute_sql` call returns
     every query's rows as clean JSON (no Decimal/date repr, no 24 round-trips).

         .venv-renderer/bin/python -m pipeline.mcp_cache_tool emit-batch --org clc --date 2026-07-09

  2. import-batch: reads the MCP result (saved as a JSON file — the single row of
     {qid: [rows]}) and writes each query's cache CSV via cache.import_from_dicts.

         .venv-renderer/bin/python -m pipeline.mcp_cache_tool import-batch --org clc --date 2026-07-09 --result /tmp/clc_result.json

Requires the org to resolve via cache.resolve_org_id (static map or
config/org_ids.json). Emit reads the parameterized .sql files produced by
`python -m pipeline.populate_cache --org {org} --date {date}` (MCP fallback).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import cache, config


def _sql_path(org: str, date: str, qid: str) -> Path:
    return config.CACHE_DIR / org / date / f"{qid}.sql"


def _strip_trailing_semicolon(sql: str) -> str:
    return sql.strip().rstrip(";").strip()


def emit_batch(org: str, date: str, qids: list[str], report_through_date: str | None = None) -> str:
    """Build one SELECT whose columns are each query's rows as a JSON array.

    Gather queries carry the gate token {{REPORT_THROUGH_DATE}} (the R1 window
    anchor resolved by preflight Q-ECON-00.report_through_date). Neither
    populate_cache nor cache.parameterize substitutes it, so it must be supplied
    here. Falls back to SQL `CURRENT_DATE` (the documented default) when omitted.
    """
    rtd_sql = f"'{report_through_date}'" if report_through_date else "CURRENT_DATE"
    cols = []
    for qid in qids:
        p = _sql_path(org, date, qid)
        if not p.exists():
            print(f"  WARN missing {p.name} — run populate_cache first", file=sys.stderr)
            continue
        body = _strip_trailing_semicolon(p.read_text(encoding="utf-8"))
        body = body.replace("{{REPORT_THROUGH_DATE}}", rtd_sql)
        # column alias must be a valid identifier; keep the qid verbatim in quotes
        cols.append(f'(SELECT json_agg(row_to_json(_q)) FROM (\n{body}\n) _q) AS "{qid}"')
    return "SELECT\n" + ",\n".join(cols) + ";"


def import_batch(org: str, date: str, result_path: Path) -> int:
    """Read the MCP execute_sql result (a JSON list with one dict of {qid: rows})
    and write each query's CSV. Returns the count of CSVs written."""
    text = result_path.read_text(encoding="utf-8").strip()
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        # MCP returns rows as a Python-literal repr (single quotes, None, True/False).
        import ast
        raw = ast.literal_eval(text)
    row = raw[0] if isinstance(raw, list) else raw
    written = 0
    for qid, rows in row.items():
        rows = rows or []
        cache.import_from_dicts(qid, org, date, rows)
        print(f"  wrote {qid}.csv ({len(rows)} rows)")
        written += 1
    return written


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("emit-batch")
    e.add_argument("--org", required=True)
    e.add_argument("--date", required=True)
    e.add_argument("--queries", default=None, help="Comma-separated qids (default: config.QUERIES_ALL)")
    e.add_argument("--report-through-date", default=None, help="YYYY-MM-DD gate anchor for {{REPORT_THROUGH_DATE}} (default: SQL CURRENT_DATE)")
    e.add_argument("--out", default=None, help="Write SQL to this file instead of stdout")

    i = sub.add_parser("import-batch")
    i.add_argument("--org", required=True)
    i.add_argument("--date", required=True)
    i.add_argument("--result", required=True, help="Path to the saved MCP JSON result")

    args = p.parse_args()

    if args.cmd == "emit-batch":
        qids = [q.strip() for q in args.queries.split(",")] if args.queries else config.QUERIES_ALL
        sql = emit_batch(args.org, args.date, qids, args.report_through_date)
        if args.out:
            Path(args.out).write_text(sql, encoding="utf-8")
            print(f"wrote {args.out} ({len(qids)} queries)")
        else:
            print(sql)
        return 0

    if args.cmd == "import-batch":
        n = import_batch(args.org, args.date, Path(args.result))
        print(f"imported {n} CSVs into cache/{args.org}/{args.date}/")
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
