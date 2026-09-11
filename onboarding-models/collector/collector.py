#!/usr/bin/env python3
"""
Onboarding Phase Progression collector.

Runs the framework's Postgres reads inside the VPN and emits a dated snapshot,
optionally loading it to BigQuery so an out-of-network agent can read it.

WHY THIS EXISTS
    mcp-postgres-tools.tools.supercatsolutions.com is split-horizon DNS —
    NXDOMAIN on public resolvers, resolvable only through the VPN (verified
    2026-08-18). Nothing outside the network can reach Postgres. So the
    collector runs inside, and the snapshot travels out.

    This mirrors preflight_gate.py's --live-state contract: live state is
    passed in, never queried by the consumer. The snapshot is dated, so a
    reader can never mistake stale state for current.

TWO WAYS TO RUN, because you have no direct DB credentials today:

  A) Direct (needs DATABASE_URL + psycopg2) — cron-able, no human:
       DATABASE_URL=postgres://... ./collector.py --orgs mali,tcd,pebl,drf --load-bq

  B) Via the MCP (works right now, zero new credentials):
       ./collector.py --orgs mali,tcd,pebl,drf --emit-sql > plan.json
       # run each statement through the supercat-postgres-vpn MCP, save as results.json
       ./collector.py --from-results results.json --load-bq

BACKTESTING
    --as-of YYYY-MM-DD filters every append-only source. Mutable tables cannot
    be reconstructed; they are captured as-of-today and tagged CURRENT_STATE so
    a backtest scores them honestly instead of pretending they are historical.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tomllib
from datetime import datetime, timezone, date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import queries as Q  # noqa: E402

SCHEMA_VERSION = "1.0.0"
FRAMEWORK_VERSION = "v3.5"

BQ_PROJECT = "supercat-data-pipeline"
BQ_DATASET = "onboarding_assessment"
BQ_TABLE = "org_state_snapshots"

# The service account the bigquery-admin MCP already uses. Portable to eve as-is.
DEFAULT_SA_KEY = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0/integrations/"
    "bigquery/service-account/supercat-data-pipeline-ac0671b8d44a.json"
)


# ------------------------------------------------------------------ helpers

def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _jsonable(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, dict):
        return {k: _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    return o


class NotCaptured(dict):
    """A metric that could not be read. Never a zero, always a reason."""

    def __init__(self, reason: str):
        super().__init__(status="NOT_CAPTURED", reason=reason)


# -------------------------------------------------- import_events YAML blocks

_BLOCK_START = re.compile(r"^- - (?P<type>[A-Za-z][A-Za-z ]*?)\s*$", re.MULTILINE)
_TIERS = (":fatal", ":error", ":warning")


def split_import_blocks(data: str) -> dict[str, str]:
    """Split one import_events.data blob into {file_type: block_body}.

    The verified YAML shape is a list of [type, entries] pairs:

        ---
        - - Products
          - - - :warning
              - 'Line 1: Custom field ...'

    A single row can carry several types (Products + Inventory + Stories).
    Phase 3 resolves "most recent" per BLOCK, so the caller needs them split.
    """
    if not data:
        return {}
    marks = list(_BLOCK_START.finditer(data))
    out: dict[str, str] = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(data)
        out[m.group("type").strip()] = data[m.start():end]
    return out


def block_tier(block_body: str) -> str:
    """Worst tier present in one block: fatal > error > warning > clean."""
    low = block_body.lower()
    for tier in _TIERS:
        if tier in low:
            return tier.lstrip(":")
    return "clean"


def summarize_import_events(rows: list[dict]) -> dict:
    """Most-recent block per file type, plus per-type history counts.

    rows must be ordered newest-first (the IMPORT_EVENTS query does this).
    """
    latest: dict[str, dict] = {}
    counts: dict[str, int] = {}
    for row in rows:
        created = row.get("created_at")
        blocks = split_import_blocks(row.get("data") or "")
        for ftype, body in blocks.items():
            counts[ftype] = counts.get(ftype, 0) + 1
            if ftype not in latest:  # newest-first, so first seen wins
                latest[ftype] = {
                    "tier": block_tier(body),
                    "created_at": created,
                    "event_id": row.get("id"),
                }
    return {
        "latest_block_by_type": latest,
        "event_counts_by_type": counts,
        "total_events_scanned": len(rows),
    }


# --------------------------------------------------------- domain resolution

def resolve_client_domains(org: dict, admin_domains: list[dict],
                           overrides: dict) -> dict:
    """Phase_Anchors.md § Resolving client_domains[].

    First non-empty SOURCE wins outright. Do NOT merge across sources.
    HubSpot (step 3 in the original spec) is dropped — see RECONCILIATION.md.
    """
    shortname = org["shortname"]

    ov = (overrides.get("client_domains") or {}).get(shortname)
    if ov:
        return {"domains": [d.lower() for d in ov], "source": "overrides.toml",
                "flags": []}

    rcpt = (org.get("order_email_recipient") or "").strip()
    if rcpt and "@" in rcpt:
        dom = rcpt.split("@")[-1].lower()
        placeholder = (
            dom in Q.PERSONAL_EMAIL_DOMAINS
            or dom == "supercatsolutions.com"
            or dom == "example.com"
            or "test" in dom
        )
        if not placeholder:
            return {"domains": [dom], "source": "order_email_recipient",
                    "flags": []}

    # Fallback: admin email domains, personal providers excluded.
    doms = [
        r["domain"] for r in admin_domains
        if r.get("domain") and r["domain"] not in Q.PERSONAL_EMAIL_DOMAINS
    ]
    flags = []
    if len(doms) >= 2:
        flags.append({
            "code": "MULTI_DOMAIN_FALLBACK_UNVERIFIED",
            "detail": f"admin-email fallback yielded {len(doms)}: {', '.join(doms)}",
        })
    if not doms:
        return {"domains": [], "source": "none",
                "flags": [{"code": "NO_CLIENT_DOMAIN_RESOLVED",
                           "detail": "no override, no order email, no admin domains"}]}
    return {"domains": doms, "source": "admin_email_fallback", "flags": flags}


# ------------------------------------------------------------------ backends

class PostgresBackend:
    """Direct psycopg2. Needs DATABASE_URL. Read-only session."""

    name = "postgres"

    def __init__(self, dsn: str):
        try:
            import psycopg2
            import psycopg2.extras
        except ImportError:
            sys.exit(
                "psycopg2 is not installed.\n"
                "  pip install psycopg2-binary\n"
                "Or use --emit-sql / --from-results to go through the MCP instead."
            )
        self._psycopg2 = psycopg2
        self.conn = psycopg2.connect(dsn)
        self.conn.set_session(readonly=True, autocommit=True)

    def run(self, sql: str, params: dict) -> list[dict]:
        import psycopg2.extras
        with self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return [dict(r) for r in cur.fetchall()]

    def close(self):
        self.conn.close()


class ResultsBackend:
    """Replays a results.json produced by running --emit-sql through the MCP."""

    name = "mcp-results"

    def __init__(self, path: str):
        with open(path) as f:
            payload = json.load(f)
        self.results = payload.get("results", payload)

    def run_key(self, key: str) -> list[dict] | NotCaptured:
        if key not in self.results:
            return NotCaptured(f"key '{key}' absent from results file")
        val = self.results[key]
        if isinstance(val, dict) and val.get("status") == "NOT_CAPTURED":
            return NotCaptured(val.get("reason", "marked NOT_CAPTURED upstream"))
        return val if isinstance(val, list) else [val]

    def close(self):
        pass


# ---------------------------------------------------------------- collection

def build_plan(orgs: list[dict], as_of: datetime) -> dict:
    """The --emit-sql payload: every statement, fully parameterized, per org."""
    plan = {
        "schema_version": SCHEMA_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "as_of": as_of.isoformat(),
        "generated_at": _utcnow().isoformat(),
        "statements": [],
        "instructions": (
            "Run each statement read-only through the supercat-postgres-vpn MCP. "
            "Save {\"results\": {\"<key>\": <rows>}} to results.json, then run "
            "collector.py --from-results results.json. A statement you could not "
            "run must be recorded as {\"status\":\"NOT_CAPTURED\",\"reason\":\"...\"} "
            "— never omitted, never zeroed."
        ),
    }
    for org in orgs:
        for key, sql, temporal, _many in Q.QUERY_REGISTRY:
            params = {"org_id": org["id"], "as_of": as_of.isoformat()}
            rendered = sql
            for pname, pval in params.items():
                token = f"%({pname})s"
                if token in rendered:
                    lit = f"'{pval}'" if isinstance(pval, str) else str(pval)
                    rendered = rendered.replace(token, lit)
            plan["statements"].append({
                "key": f"{org['shortname']}::{key}",
                "org": org["shortname"],
                "metric": key,
                "temporal": temporal,
                "sql": rendered.replace("%%", "%").strip(),
            })
    return plan


def collect_org(org: dict, backend, as_of: datetime, overrides: dict) -> dict:
    """One org -> one snapshot record."""
    shortname = org["shortname"]
    raw: dict[str, object] = {}
    not_captured: list[dict] = []

    for key, sql, temporal, many in Q.QUERY_REGISTRY:
        try:
            if isinstance(backend, ResultsBackend):
                rows = backend.run_key(f"{shortname}::{key}")
            else:
                rows = backend.run(sql, {"org_id": org["id"], "as_of": as_of})
        except Exception as exc:  # a broken query must not kill the run
            rows = NotCaptured(f"{type(exc).__name__}: {exc}")

        if isinstance(rows, NotCaptured):
            not_captured.append({"metric": key, "reason": rows["reason"]})
            raw[key] = rows
            continue
        raw[key] = rows if many else (rows[0] if rows else {})

    # -- derived --------------------------------------------------------
    domains = resolve_client_domains(
        org,
        raw.get("admin_email_domains") if isinstance(raw.get("admin_email_domains"), list) else [],
        overrides,
    )

    imports = (
        summarize_import_events(raw["import_events"])
        if isinstance(raw.get("import_events"), list)
        else NotCaptured("import_events unavailable")
    )

    catalog = raw.get("catalog_counts") or {}
    active = catalog.get("active_products") or 0
    with_img = catalog.get("products_with_images") or 0
    visible = catalog.get("visible_products") or 0

    reps = raw.get("reps") if isinstance(raw.get("reps"), list) else []
    rep_summary = summarize_reps(reps, domains["domains"], as_of)

    price_levels = raw.get("price_levels") if isinstance(raw.get("price_levels"), list) else []

    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "framework_version": FRAMEWORK_VERSION,
        "captured_at": _utcnow().isoformat(),
        "as_of": as_of.isoformat(),
        "backend": backend.name,

        "org_shortname": shortname,
        "org_id": org["id"],
        "org_name": org.get("name"),
        "org_status": org.get("status"),
        "org_created_at": org.get("created_at"),
        "order_email_recipient": org.get("order_email_recipient"),
        "import_active": org.get("import_active"),
        "send_order_email_on_submit": org.get("send_order_email_on_submit"),

        "client_domains": domains["domains"],
        "client_domains_source": domains["source"],

        "imports": imports,

        "catalog": {
            "active_products": active,
            "products_with_images": with_img,
            "visible_products": visible,
            "image_coverage_pct": round(with_img / active * 100, 2) if active else None,
            "visible_products_pct": round(visible / active * 100, 2) if active else None,
        },
        "pricing": {
            "price_level_count": len(price_levels),
            "price_level_codes": [p.get("code") for p in price_levels],
            "hidden_price_levels": [p.get("code") for p in price_levels if p.get("hidden")],
        },
        "customers": raw.get("customer_counts") or {},
        "options": raw.get("option_counts") or {},
        "inventory": raw.get("inventory_counts") or {},
        "org_flags": raw.get("org_feature_flags") or {},
        "reps": rep_summary,
        "user_types": raw.get("user_type_counts") or {},
        "ipad_reports": (raw.get("ipad_report_count") or {}).get("ipad_reports"),
        "orders": raw.get("orders_matched") or {},
        "unmatched_order_names": raw.get("unmatched_order_names") or [],

        "flags": domains["flags"],
        "not_captured": not_captured,
        "completeness": {
            "metrics_expected": len(Q.QUERY_REGISTRY),
            "metrics_captured": len(Q.QUERY_REGISTRY) - len(not_captured),
        },
        "temporal_warning": (
            "CURRENT_STATE metrics (catalog, pricing, customers, options, "
            "inventory, reps, user_types, ipad_reports) reflect captured_at, "
            "NOT as_of. Only imports and orders are reconstructed to as_of."
        ) if as_of.date() != _utcnow().date() else None,
    }
    return snapshot


def summarize_reps(reps: list[dict], client_domains: list[str], as_of: datetime) -> dict:
    """Phase 5. rep_subtype is informational; all subtypes count toward the anchor."""
    from datetime import timedelta
    cutoff = as_of - timedelta(days=30)
    out = {"total": len(reps), "by_subtype": {"external": 0, "in_house": 0,
                                              "personal_email": 0},
           "ever_logged_in": 0, "active_30d": 0,
           # D14: an org with eCat Online has TWO login surfaces. Reporting only
           # the iPad silently calls a live brand dead -- mali's ML Reps showed
           # 0 of 5 on iPad and 4 of 5 on eOL.
           "ever_logged_in_ipad": 0, "ever_logged_in_eol": 0,
           "ever_logged_in_any_surface": 0}
    for r in reps:
        dom = (r.get("domain") or "").lower()
        if dom in Q.PERSONAL_EMAIL_DOMAINS:
            out["by_subtype"]["personal_email"] += 1
        elif dom in client_domains:
            out["by_subtype"]["in_house"] += 1
        else:
            out["by_subtype"]["external"] += 1

        eol = r.get("last_ecat_online_login_at")
        if eol:
            out["ever_logged_in_eol"] += 1
        last = r.get("last_ipad_login_at")
        if last:
            out["ever_logged_in_ipad"] += 1
        if last or eol:
            out["ever_logged_in_any_surface"] += 1
        if last:
            out["ever_logged_in"] += 1
            if isinstance(last, str):
                try:
                    last = datetime.fromisoformat(last.replace("Z", "+00:00"))
                except ValueError:
                    last = None
            if last:
                if last.tzinfo is None:
                    last = last.replace(tzinfo=timezone.utc)
                if last >= cutoff:
                    out["active_30d"] += 1
    return out


# ------------------------------------------------------------------ bigquery

def load_to_bigquery(snapshots: list[dict], sa_key: str) -> str:
    from google.cloud import bigquery
    from google.oauth2 import service_account

    creds = service_account.Credentials.from_service_account_file(sa_key)
    client = bigquery.Client(credentials=creds, project=BQ_PROJECT)
    table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"

    # One JSON column keeps the loader immune to framework schema churn; the
    # scalar columns are the ones queries filter and join on.
    schema = [
        bigquery.SchemaField("captured_at", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("as_of", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("org_shortname", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("org_id", "INTEGER"),
        bigquery.SchemaField("org_status", "STRING"),
        bigquery.SchemaField("schema_version", "STRING"),
        bigquery.SchemaField("framework_version", "STRING"),
        bigquery.SchemaField("metrics_expected", "INTEGER"),
        bigquery.SchemaField("metrics_captured", "INTEGER"),
        bigquery.SchemaField("snapshot", "JSON"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(field="captured_at")
    table.clustering_fields = ["org_shortname"]
    client.create_table(table, exists_ok=True)

    rows = [{
        "captured_at": s["captured_at"],
        "as_of": s["as_of"],
        "org_shortname": s["org_shortname"],
        "org_id": s["org_id"],
        "org_status": s["org_status"],
        "schema_version": s["schema_version"],
        "framework_version": s["framework_version"],
        "metrics_expected": s["completeness"]["metrics_expected"],
        "metrics_captured": s["completeness"]["metrics_captured"],
        "snapshot": json.dumps(_jsonable(s)),
    } for s in snapshots]

    errors = client.insert_rows_json(table_id, rows)
    if errors:
        raise RuntimeError(f"BigQuery insert failed: {errors}")
    return table_id


# ---------------------------------------------------------------------- main

class OverridesUnavailable(RuntimeError):
    """Raised rather than returning {}. See load_overrides."""


def load_overrides(path: str, allow_missing: bool = False) -> dict:
    """Load overrides.toml, or REFUSE.

    ## Why this raises instead of returning {}

    It used to catch ImportError on PyYAML, warn to stderr and return `{}`.
    Downstream, `{}` is indistinguishable from "no overrides are declared" — so
    a missing dependency silently converted every human-confirmed fact back
    into an unknown. For as long as that ran here:

      * `net_price_only_confirmed` was empty, so SINGLE_PRICE_LEVEL_UNCONFIRMED
        could fire on an org confirmed by design;
      * `integration_status` was empty, so INTEGRATION_OWNER_UNCLEAR could fire
        on libco, which is tracked;
      * `project_start_date` was empty — and D19's at-risk fix DEPENDS on it.
        Without it the regression rule false-positives on pre-sales orgs, which
        is the nine-month false alarm D19 exists to prevent.

    None of that was visible: one stderr line that scrolls past, then silence.

    ## TOML, since 2026-09-05

    `tomllib` is stdlib from Python 3.11, so the dependency that caused all of
    the above no longer exists. PyYAML could not be installed here in any case —
    Homebrew's Python is externally managed (PEP 668). TOML also has no implicit
    typing, where YAML 1.1 turns bare `N` / `NO` / `ON` / `OFF` into booleans;
    this config names eCat things, and `N` is a literal eCat boolean token.

    Note `project_start_date` values are QUOTED strings. TOML has a native date
    type, so a bare `2026-06-19` would parse to `datetime.date` rather than the
    string every consumer here expects.

    A caller that genuinely wants to proceed without overrides must pass
    `allow_missing=True` and say so in its own output. Never by default.
    """
    if not os.path.exists(path):
        if allow_missing:
            return {}
        raise OverridesUnavailable(
            f"{path} not found. Refusing to continue: an absent overrides file is "
            f"indistinguishable from an org with no overrides, and that difference "
            f"is what the file is for. Pass allow_missing=True to proceed anyway."
        )
    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise OverridesUnavailable(
            f"{path} is not valid TOML: {exc}. Refusing to continue — an overrides "
            f"file that half-parses is how a human-confirmed fact silently reverts "
            f"to unknown."
        ) from exc
    if not data:
        raise OverridesUnavailable(
            f"{path} parsed as empty. Refusing to treat that as 'no overrides'."
        )
    return data


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--orgs", help="comma-separated shortnames; omit for the auto-cohort")
    ap.add_argument("--orgs-file", help='JSON {"orgs":[...]} of org rows, for the MCP path')
    ap.add_argument("--as-of", help="YYYY-MM-DD; backtest date (default: now)")
    ap.add_argument("--emit-sql", action="store_true",
                    help="print the statement plan for MCP execution and exit")
    ap.add_argument("--from-results", help="results.json produced from an --emit-sql plan")
    ap.add_argument("--load-bq", action="store_true", help="append snapshots to BigQuery")
    ap.add_argument("--sa-key", default=DEFAULT_SA_KEY)
    ap.add_argument("--overrides", default=os.path.join(os.path.dirname(here), "overrides.toml"))
    ap.add_argument("--no-overrides", action="store_true",
                    help="proceed WITHOUT overrides.toml. Every declaration in it is "
                         "inactive and the run says so. Never the default.")
    ap.add_argument("--out", help="write snapshots JSON here (default: stdout)")
    args = ap.parse_args()

    as_of = (
        datetime.fromisoformat(args.as_of).replace(tzinfo=timezone.utc)
        if args.as_of else _utcnow()
    )
    try:
        overrides = load_overrides(args.overrides, allow_missing=args.no_overrides)
    except OverridesUnavailable as exc:
        print(f"OVERRIDES UNAVAILABLE — refusing to run.\n  {exc}", file=sys.stderr)
        return 2
    if args.no_overrides:
        print("!! overrides.toml NOT APPLIED (--no-overrides): every human-confirmed "
              "fact in it is inactive for this run.", file=sys.stderr)
    shortnames = [s.strip() for s in args.orgs.split(",")] if args.orgs else None

    # -- resolve the org list -------------------------------------------
    dsn = os.environ.get("DATABASE_URL")
    if args.from_results:
        with open(args.from_results) as f:
            payload = json.load(f)
        orgs = payload.get("orgs")
        if not orgs:
            sys.exit("results.json must carry an \"orgs\" list (copy it from the plan).")
        backend = ResultsBackend(args.from_results)
    elif args.orgs_file:
        with open(args.orgs_file) as f:
            orgs = json.load(f).get("orgs") or []
        backend = None  # only valid with --emit-sql; enforced below
    elif dsn:
        backend = PostgresBackend(dsn)
        orgs = (backend.run(Q.ORGS_BY_SHORTNAME, {"shortnames": shortnames})
                if shortnames else backend.run(Q.COHORT, {}))
    else:
        sys.exit(
            "No DATABASE_URL, no --from-results, no --orgs-file.\n\n"
            "Use the MCP path (no credentials needed):\n"
            "  1. Run this through the supercat-postgres-vpn MCP:\n"
            "       SELECT id, shortname, name, created_at, properties->>'status' AS status,\n"
            "              order_email_recipient, import_active, send_order_email_on_submit\n"
            "       FROM organizations WHERE shortname = ANY(ARRAY['mali','tcd','pebl','drf']);\n"
            "  2. Save as orgs.json:  {\"orgs\": [ ...those rows... ]}\n"
            "  3. ./collector.py --orgs-file orgs.json --emit-sql > plan.json\n"
            "  4. Run plan.json's statements through the MCP -> results.json\n"
            "  5. ./collector.py --from-results results.json --load-bq"
        )

    if not orgs:
        print("No orgs matched. The auto-cohort is empty when every client has "
              "graduated to status='active'.", file=sys.stderr)
        return 0

    if args.emit_sql:
        plan = build_plan(orgs, as_of)
        plan["orgs"] = _jsonable(orgs)
        print(json.dumps(plan, indent=2, default=str))
        return 0

    if backend is None:
        sys.exit("--orgs-file is only usable with --emit-sql "
                 "(there is no connection to run the statements).")

    snapshots = [collect_org(o, backend, as_of, overrides) for o in orgs]
    backend.close()

    # -- report ----------------------------------------------------------
    for s in snapshots:
        c = s["completeness"]
        status = "OK" if not s["not_captured"] else f"{len(s['not_captured'])} GAPS"
        print(f"  {s['org_shortname']:<8} {c['metrics_captured']}/{c['metrics_expected']} "
              f"metrics  domains={','.join(s['client_domains']) or '-'} "
              f"({s['client_domains_source']})  [{status}]", file=sys.stderr)
        for nc in s["not_captured"]:
            print(f"      NOT_CAPTURED {nc['metric']}: {nc['reason']}", file=sys.stderr)
        for fl in s["flags"]:
            print(f"      FLAG {fl['code']}: {fl['detail']}", file=sys.stderr)

    payload = json.dumps(_jsonable(snapshots), indent=2, default=str)
    if args.out:
        with open(args.out, "w") as f:
            f.write(payload)
        print(f"  -> {args.out}", file=sys.stderr)
    else:
        print(payload)

    if args.load_bq:
        table_id = load_to_bigquery(snapshots, args.sa_key)
        print(f"  -> loaded {len(snapshots)} snapshot(s) to {table_id}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
