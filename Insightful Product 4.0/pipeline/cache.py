"""Cache layer: extract SQL from canon docs, run against Postgres,
write CSVs to cache/{org}/{date}/{query_id}.csv.

Single responsibility: data acquisition. This module:
  - extracts named SQL blocks from canon (query_library_v2.md,
    rep_copilot_operator.md, selling_customer_exception_layer.md)
  - parameterizes {{ORG_ID}} / {{ORG_SHORTNAME}}
  - executes via psycopg2 (or emits SQL for MCP-mediated population)
  - writes results as CSVs

What this module DOES NOT do (surface ownership):
  - parse query results into typed structures (gather.py)
  - decide what gates pass (preflight.py)
  - render anything

Immutability contract (Health V3 pattern, verbatim):
  Once cache/{org}/{date}/ exists, it is never modified. To re-run with
  fresher data, populate a NEW dated directory.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from . import config


# ─── Cache paths ───────────────────────────────────────────────────────────
@dataclass
class CachePaths:
    org: str
    date: str  # YYYY-MM-DD, UTC
    dir: Path

    @classmethod
    def for_run(cls, org: str, date) -> "CachePaths":
        date_str = date.isoformat() if hasattr(date, "isoformat") else str(date)
        d = config.CACHE_DIR / org / date_str
        return cls(org=org, date=date_str, dir=d)

    def csv_for(self, query_id: str) -> Path:
        return self.dir / f"{query_id}.csv"

    def exists(self) -> bool:
        return self.dir.exists() and any(self.dir.glob("*.csv"))


# ─── SQL extraction ────────────────────────────────────────────────────────
# Canon documents to search, in priority order.
_CANON_DOCS = [
    config.QUERY_LIBRARY_MD,
    config.OPERATORS_DIR / "rep_copilot_operator.md",
    config.FOUNDATION_DIR / "selling_customer_exception_layer.md",
    config.OPERATORS_DIR / "rung4_option_a_operator.md",
]

# Match: `### Q-ECON-00`, `### Q-ECON-00:`, `### Q-ECON-00 — title`, `## Org Lookup`
# Up to 4 `#`s; anchored to start of line.
_HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$", re.M)

# Match a ```sql ... ``` fenced block. Non-greedy.
_SQL_FENCE_RE = re.compile(r"```sql\s*\n(.*?)\n```", re.S)


def _heading_tokens(heading: str) -> list[str]:
    """`3. RS-01 — re-anchored rep leaderboard` → ['3.', 'RS-01', '—', 're-anchored', ...]
    `Q-ECON-00: Economics Preflight Gate (...)` → ['Q-ECON-00:', 'Economics', ...]
    We then strip trailing punctuation on each token to match query IDs.
    """
    raw = re.split(r"\s+", heading.strip())
    return [t.rstrip(":.,;").lstrip(".") for t in raw]


def _find_block_in_doc(text: str, query_id: str) -> Optional[str]:
    """Search a doc for a heading whose first token == query_id, return the
    first ```sql block that follows it (before the next heading at the same
    level or higher).

    Fallback: if no `### {qid}` heading exists, look for `**{qid}` (bold
    label form used in operators/rep_copilot_operator.md for RP-2 etc.) and
    take the next ```sql block.
    """
    matches = list(_HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        tokens = _heading_tokens(m.group(2))
        if query_id not in tokens:
            continue
        level = len(m.group(1))
        start = m.end()
        end = len(text)
        for nm in matches[i + 1 :]:
            if len(nm.group(1)) <= level:
                end = nm.start()
                break
        section = text[start:end]
        sql_match = _SQL_FENCE_RE.search(section)
        if sql_match:
            return sql_match.group(1).strip()

    # Fallback: bold-label form (e.g. `**RP-2 ...**` in rep_copilot_operator.md).
    # Take the FIRST ```sql block after the first occurrence.
    label_re = re.compile(rf"\*\*{re.escape(query_id)}\b")
    lm = label_re.search(text)
    if lm:
        sql_match = _SQL_FENCE_RE.search(text, pos=lm.end())
        if sql_match:
            return sql_match.group(1).strip()

    return None


def extract_sql(query_id: str, *, source_paths: Optional[list[Path]] = None) -> str:
    """Locate query_id in the canon docs and return its SQL body verbatim
    (less the ```sql fence). Caller substitutes {{ORG_ID}} / {{ORG_SHORTNAME}}
    so substitution is local + visible.

    Raises FileNotFoundError if no canon doc holds the query_id.
    """
    docs = source_paths or _CANON_DOCS
    for path in docs:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        sql = _find_block_in_doc(text, query_id)
        if sql:
            return sql
    raise FileNotFoundError(
        f"No SQL block found for query_id={query_id!r} in canon docs: "
        f"{[str(p) for p in docs]}"
    )


def parameterize(sql: str, org_id: int, org_shortname: str) -> str:
    """Replace {{ORG_ID}} / {{ORG_SHORTNAME}} tokens. Other tokens (e.g.
    {{ECAT_SALE_FILTER}}) are left intact — they're block-shared SQL that
    the library expands inline, and the current query suite doesn't depend
    on macro substitution."""
    return (
        sql.replace("{{ORG_ID}}", str(org_id))
        .replace("{{ORG_SHORTNAME}}", f"'{org_shortname}'")
    )


# ─── Org resolution ────────────────────────────────────────────────────────
# Static map for the five known orgs (avoids a DB roundtrip for the most
# common case). Run-time lookup falls back to the Org Lookup query.
_KNOWN_ORG_IDS = {
    "sarreid": 1,     # Sarreid Ltd
    "bmc": 11,        # Bassett Mirror
    "cci": 161,       # Currey & Company
    "hfg": 165,       # Hubbardton Forge
    "kal": 146,       # Kalco Lighting / Allegri Crystal
    "sca": 90,        # Shadow Catchers
    "ali": 127,       # Access Lighting
    "bri": 222,       # Bulbrite
    "da": 62,         # Dainolite Ltd.
}

# Display names for the same known orgs. Used to auto-populate profiles
# (see run_report._emit_inline_draft_profile) so the SHIP filename and
# profile H1 show a real client name instead of `org.title()`.
_KNOWN_ORG_NAMES = {
    "sarreid": "Sarreid, Ltd.",
    "bmc": "Bassett Mirror",
    "cci": "Currey & Company",
    "hfg": "Hubbardton Forge",
    "kal": "Kalco Lighting / Allegri Crystal",
    "sca": "Shadow Catchers",
    "ali": "Access Lighting",
    "bri": "Bulbrite",
    "da": "Dainolite Ltd.",
}


def resolve_org_name(shortname: str, *, conn=None) -> str:
    """Map shortname → display name. Hits the static map first; falls back
    to a DB lookup (organizations.name) if a connection is given, then to a
    title-cased shortname as a last resort.
    """
    if shortname in _KNOWN_ORG_NAMES:
        return _KNOWN_ORG_NAMES[shortname]
    file_map = config.load_org_ids()
    if shortname in file_map and file_map[shortname].get("name"):
        return str(file_map[shortname]["name"])
    if conn is None:
        return shortname.replace("_", " ").title()
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM organizations WHERE shortname = %s", (shortname,))
        row = cur.fetchone()
        return row[0] if row else shortname.replace("_", " ").title()


def resolve_org_id(shortname: str, *, conn=None) -> int:
    """Map shortname → organization_id. Hits the static map first; falls
    back to running the Org Lookup query if we have a connection.
    """
    if shortname in _KNOWN_ORG_IDS:
        return _KNOWN_ORG_IDS[shortname]
    file_map = config.load_org_ids()
    if shortname in file_map:
        return int(file_map[shortname]["id"])
    if conn is None:
        raise ValueError(
            f"Unknown shortname {shortname!r} and no DB connection. "
            f"Add it to config/org_ids.json (id + name), add to _KNOWN_ORG_IDS, "
            f"or pass conn=psycopg2.connect(...)."
        )
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM organizations WHERE shortname = %s",
            (shortname,),
        )
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Org not found for shortname={shortname!r}")
        return int(row[0])


# ─── Execution ─────────────────────────────────────────────────────────────
def _connect():
    """Open a psycopg2 connection from env vars. Raises if no DSN is set."""
    import psycopg2  # local import so the module loads without psycopg2

    dsn = config.pg_dsn()
    if isinstance(dsn, str):
        return psycopg2.connect(dsn)
    return psycopg2.connect(**dsn)


def execute(sql: str, *, conn=None) -> tuple[list[str], list[tuple]]:
    """Run a SELECT and return (column_names, rows). Read-only — does not
    issue COMMIT. Caller manages the connection lifecycle.
    """
    own_conn = conn is None
    if own_conn:
        conn = _connect()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            cols = [d[0] for d in (cur.description or [])]
            rows = cur.fetchall()
        return cols, rows
    finally:
        if own_conn:
            conn.close()


def write_csv(path: Path, cols: list[str], rows: Iterable[tuple]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])


# Minimum file size (bytes) for a CSV to be considered a real cached result.
# An empty result from import_from_dicts writes csv.writer.writerow([]) → 2 bytes (\r\n).
# Any real query result has at least a header row (typically 30–200+ bytes).
# Stubs at or below this threshold are treated as missing and re-populated.
_CSV_MIN_BYTES = 3


def import_from_dicts(
    query_id: str,
    org: str,
    date: str,
    rows: list[dict],
) -> Path:
    """MCP-mediated cache population: take the list-of-dicts returned by
    the `user-supercat-postgres-vpn` `execute_sql` tool and write it as
    cache/{org}/{date}/{query_id}.csv.

    Use this when DB credentials are not set up locally and the agent is
    running queries through the MCP. Column order is taken from the first
    row's keys.

    WARNING: if rows is empty, this writes a stub CSV (header-only or empty).
    Stub CSVs cause blank report sections. The caller should verify that an
    empty result is truly expected (e.g. a query that legitimately returns no
    rows) rather than a failed or timed-out MCP call.
    """
    paths = CachePaths.for_run(org, date)
    if not rows:
        print(
            f"  WARN  import_from_dicts: {query_id} for {org}/{date} got 0 rows — "
            f"writing stub. If this is unexpected, re-run the MCP query and call "
            f"import_from_dicts again (stub is below _CSV_MIN_BYTES and will be "
            f"overwritten on next --populate-cache).",
            file=sys.stderr,
        )
        cols: list[str] = []
        tuples: list[tuple] = []
    else:
        cols = list(rows[0].keys())
        tuples = [tuple(r.get(c) for c in cols) for r in rows]
    out = paths.csv_for(query_id)
    write_csv(out, cols, tuples)
    return out


def populate(
    org: str,
    date: str,
    query_ids: Optional[list[str]] = None,
    *,
    conn=None,
    skip_existing: bool = True,
    dry_run: bool = False,
) -> CachePaths:
    """Populate cache/{org}/{date}/ with CSVs for the given query_ids.

    Immutability: skip queries whose CSV already exists by default. Pass
    skip_existing=False only to overwrite within the same date (the
    contract still says "use a new date for fresh data" — skip_existing
    exists for iteration during development).

    dry_run=True emits the SQL to stdout instead of executing; useful when
    DB creds aren't set up and SQL will be run via the MCP.
    """
    if query_ids is None:
        query_ids = config.QUERIES_ALL

    paths = CachePaths.for_run(org, date)
    paths.dir.mkdir(parents=True, exist_ok=True)

    org_id = resolve_org_id(org, conn=conn)

    own_conn = conn is None and not dry_run
    if own_conn:
        conn = _connect()
    try:
        for qid in query_ids:
            csv_path = paths.csv_for(qid)
            if skip_existing and csv_path.exists() and csv_path.stat().st_size > _CSV_MIN_BYTES:
                print(f"  skip  {qid}  (exists)")
                continue
            try:
                sql = extract_sql(qid)
            except FileNotFoundError as e:
                print(f"  MISS  {qid}  ({e})")
                continue
            sql = parameterize(sql, org_id, org)
            if dry_run:
                print(f"  --- {qid} ---")
                print(sql)
                print()
                continue
            cols, rows = execute(sql, conn=conn)
            write_csv(csv_path, cols, rows)
            print(f"  ok    {qid}  ({len(rows)} rows -> {csv_path.name})")
    finally:
        if own_conn and conn is not None:
            conn.close()

    return paths
