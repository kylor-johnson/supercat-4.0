"""
Insightful Product 2.0 — Stage 1 Data Gatherer

Runs all preflight checks, executes queries in parallel batches, computes
derived gates, and writes cache files in the locked markdown format.

Postgres: via MCP server (supercat-postgres-vpn, no credentials needed).
BigQuery: via google-cloud-bigquery with service account key.

Usage:
    python data_gather.py --shortname pf --org-id 123 --run-date 2026-06-15
    python data_gather.py --shortname pf --org-id 123 --run-date 2026-06-15 --dry-run
    python data_gather.py --shortname pf --org-id 123 --run-date 2026-06-15 \\
        --period-start 2025-06-15 --period-end 2026-06-15 --client-name "Palecek"
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

from google.cloud import bigquery
from mcp import ClientSession
from mcp.client.sse import sse_client

log = logging.getLogger("data_gather")

MCP_PG_URL = "https://mcp-postgres-tools.tools.supercatsolutions.com/sse"

_PG_SEMAPHORE = threading.Semaphore(4)

BQ_KEY_FILE = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS",
    str(
        Path.home()
        / "Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
        / "integrations/bigquery/service-account"
        / "supercat-data-pipeline-ac0671b8d44a.json"
    ),
)

# ---------------------------------------------------------------------------
# Query Library Parser
# ---------------------------------------------------------------------------

def parse_query_library(path: Path) -> dict[str, str]:
    """Extract SQL blocks from authority/query_library.md keyed by Q-ID."""
    text = path.read_text(encoding="utf-8")
    queries: dict[str, str] = {}
    header_re = re.compile(r"^###\s+(Q-[\w-]+(?:\s+(?:Step\s+\d+|Part\s+[A-Z]))?):", re.MULTILINE)
    sql_block_re = re.compile(r"```sql\s*\n(.*?)```", re.DOTALL)

    sections = list(header_re.finditer(text))
    for i, m in enumerate(sections):
        q_id = m.group(1).strip()
        start = m.end()
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        section_text = text[start:end]
        for sql_match in sql_block_re.finditer(section_text):
            sql = sql_match.group(1).strip()
            if sql.startswith("--") and all(
                line.strip().startswith("--") or line.strip() == "" for line in sql.splitlines()
            ):
                continue
            sub_key = q_id
            if sub_key in queries:
                suffix = 2
                while f"{sub_key}_{suffix}" in queries:
                    suffix += 1
                sub_key = f"{sub_key}_{suffix}"
            queries[sub_key] = sql
    return queries


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class GateFlags:
    """All gate flags computed during the run."""
    report_mode: int = 1
    mode_label: str = "Mode 1: Standard Intelligence Report"

    # primary
    HAS_CLICKY: bool = False
    HAS_CART: bool = False
    HAS_PORTAL_ORDERS: bool = False
    HAS_INVENTORY: bool = False
    HAS_SALES_DATA: bool = False
    HAS_SALES_SECTION: bool = False
    HAS_PEER_DATA: bool = False
    BENCHMARK_ELIGIBLE: bool = False
    BENCHMARK_CONFIDENCE: str = ""
    PEER_GROUP_LEVEL: str = ""
    PEER_GROUP_N: int = 0
    PEER_GROUP_ID_EFFECTIVE: str = ""
    CLICKY_PREFIX: str = ""

    # derived
    VM45_GATE_1: str = "SKIP"
    VM45_GATE_2: str = "SKIP"
    VM45_RENDER: bool = False
    QUALIFYING_REP_COUNT: int = 0
    MIXPANEL_USER_DATA_PRESENT: bool = False
    SHOWROOM_EXCLUSIONS: int = 0
    MIXPANEL_ORDER_TRACKING_GAP: bool = False
    USER_GROUP_SPLIT_AVAILABLE: bool = False
    USER_GROUP_JOIN_RATE: str = "N/A"
    USER_GROUP_SHOWROOM_EVENT_SHARE: str = "N/A"
    ADMIN_REPS_IN_LEADERBOARD: bool = False

    # ERP enrichment
    PORTAL_ORDERS_FRESH: bool = False
    PORTAL_REP_DATA_PRESENT: bool = False
    PORTAL_CUSTOMER_DATA_PRESENT: bool = False
    INVENTORY_FRESH: bool = False
    SALES_DATA_FRESH: bool = False
    CUSTOMER_DATA_FRESH: bool = False
    HAS_COMMITMENT_DATA: bool = False
    HAS_NEW_ITEMS: bool = False
    HAS_BUYER_DATA: bool = False

    # confidence tiers
    SECTION_CONFIDENCE_2: str = ""
    SECTION_CONFIDENCE_3: str = ""
    SECTION_CONFIDENCE_4: str = ""
    SECTION_CONFIDENCE_5: str = ""

    # evidence strings for gate_flags.md
    evidence: dict[str, str] = field(default_factory=dict)
    validation_log: list[str] = field(default_factory=list)

    # mode 2/3 extras
    alltime_ecat_orders: int = 0
    alltime_ecat_gmv: float = 0.0
    last_ecat_order_date: str | None = None
    ltm_ecat_orders: int = 0
    ltm_erp_orders: int = 0


@dataclass
class RunContext:
    shortname: str
    org_id: int
    run_date: date
    period_start: date
    period_end: date
    client_name: str
    bundle_label: str
    cache_dir: Path
    dry_run: bool
    query_lib: dict[str, str]
    gates: GateFlags = field(default_factory=GateFlags)
    org_summary: dict[str, Any] = field(default_factory=dict)
    q08_results: list[dict] = field(default_factory=list)
    failed_queries: list[dict[str, str]] = field(default_factory=list)
    completed_queries: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def _substitute_params(sql: str, params: tuple) -> str:
    """Replace %s placeholders with literal values for MCP (no parameterized queries)."""
    result = sql
    for val in params:
        if val is None:
            literal = "NULL"
        elif isinstance(val, (int, float)):
            literal = str(val)
        elif isinstance(val, str):
            literal = "'" + val.replace("'", "''") + "'"
        else:
            literal = "'" + str(val).replace("'", "''") + "'"
        result = result.replace("%s", literal, 1)
    return result


class McpSessionManager:
    """Maintains a single persistent MCP SSE connection across all queries.

    Runs its own asyncio event loop on a dedicated daemon thread.  Callers
    use the synchronous ``run_sync(sql)`` wrapper — the semaphore in
    ``run_pg`` still limits concurrency.
    """

    _MAX_RECONNECT = 2

    def __init__(self, url: str) -> None:
        self._url = url
        self._loop: asyncio.AbstractEventLoop | None = None
        self._thread: threading.Thread | None = None
        self._session: ClientSession | None = None
        self._sse_cm: Any = None
        self._session_cm: Any = None
        self._streams: Any = None
        self._ready = threading.Event()
        self._closed = False
        self._lock = asyncio.Lock()  # guards reconnect

    # -- lifecycle -----------------------------------------------------------

    def start(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._run_loop, daemon=True, name="mcp-pg-loop",
        )
        self._thread.start()
        if not self._ready.wait(timeout=30):
            raise RuntimeError("McpSessionManager failed to connect within 30 s")
        if self._session is None:
            raise RuntimeError("McpSessionManager: session is None after start")

    def _run_loop(self) -> None:
        assert self._loop is not None
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._open())
        self._ready.set()
        self._loop.run_forever()

    async def _open(self) -> None:
        self._sse_cm = sse_client(self._url)
        self._streams = await self._sse_cm.__aenter__()
        self._session_cm = ClientSession(*self._streams)
        self._session = await self._session_cm.__aenter__()
        await self._session.initialize()
        log.info("MCP persistent session opened → %s", self._url)

    async def _close_session(self) -> None:
        try:
            if self._session_cm:
                await self._session_cm.__aexit__(None, None, None)
        except Exception:
            pass
        try:
            if self._sse_cm:
                await self._sse_cm.__aexit__(None, None, None)
        except Exception:
            pass
        self._session = None
        self._session_cm = None
        self._sse_cm = None
        self._streams = None

    async def _reconnect(self) -> None:
        log.warning("MCP session lost — reconnecting…")
        await self._close_session()
        await self._open()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._loop and self._loop.is_running():
            future = asyncio.run_coroutine_threadsafe(
                self._close_session(), self._loop,
            )
            try:
                future.result(timeout=10)
            except Exception:
                pass
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

    # -- query execution -----------------------------------------------------

    async def execute(self, sql: str) -> list[dict]:
        for attempt in range(1 + self._MAX_RECONNECT):
            try:
                assert self._session is not None
                result = await self._session.call_tool("execute_sql", {"sql": sql})
                if not result.content:
                    return []
                return _parse_mcp_text(result.content[0].text)
            except Exception as exc:
                if attempt < self._MAX_RECONNECT and not self._closed:
                    async with self._lock:
                        if self._session is None or attempt > 0:
                            await self._reconnect()
                    continue
                raise RuntimeError(
                    f"MCP query failed after {attempt + 1} attempt(s): {exc}"
                ) from exc
        return []  # unreachable, satisfies type checker

    def run_sync(self, sql: str) -> list[dict]:
        assert self._loop is not None and self._loop.is_running()
        future = asyncio.run_coroutine_threadsafe(self.execute(sql), self._loop)
        return future.result(timeout=120)


_pg_manager: McpSessionManager | None = None


def _parse_mcp_text(text: str) -> list[dict]:
    """Parse the MCP Postgres server response, which may contain Python types."""
    # Try standard JSON first
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        pass
    # Server returns Python repr with Decimal(), datetime.datetime(), etc.
    # Normalize to JSON-safe types before parsing
    normalized = text
    normalized = re.sub(r"Decimal\('([^']*)'\)", r"\1", normalized)
    normalized = re.sub(
        r"datetime\.datetime\((\d+),\s*(\d+),\s*(\d+),?\s*(\d+)?,?\s*(\d+)?,?\s*(\d+)?,?\s*(\d+)?\)",
        _datetime_replacer,
        normalized,
    )
    normalized = re.sub(r"datetime\.date\((\d+),\s*(\d+),\s*(\d+)\)", r"'\1-\2-\3'", normalized)
    normalized = normalized.replace("None", "null").replace("True", "true").replace("False", "false")
    # Single quotes to double quotes (careful with apostrophes in values)
    normalized = re.sub(r"'([^']*)'(?=\s*[:,\]\}])", r'"\1"', normalized)
    normalized = re.sub(r"(?<=[\[,{])\s*'([^']*)'", r' "\1"', normalized)
    try:
        data = json.loads(normalized)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        pass
    # Last resort: ast.literal_eval with Decimal/datetime in namespace
    try:
        from decimal import Decimal  # noqa: F811
        ns = {"Decimal": Decimal, "datetime": __import__("datetime")}
        data = eval(text, {"__builtins__": {}}, ns)  # noqa: S307
        if isinstance(data, list):
            return [_coerce_row(r) for r in data]
        if isinstance(data, dict):
            return [_coerce_row(data)]
        return [{"value": data}]
    except Exception:
        log.warning("MCP returned unparseable response: %s", text[:300])
        return []


def _datetime_replacer(m: re.Match) -> str:
    parts = [int(p) for p in m.groups() if p is not None]
    if len(parts) >= 6:
        return f"'{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d} {parts[3]:02d}:{parts[4]:02d}:{parts[5]:02d}'"
    elif len(parts) >= 3:
        return f"'{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}'"
    return f"'{'-'.join(str(p) for p in parts)}'"


def _coerce_row(row: dict) -> dict:
    """Convert Decimal/datetime values to JSON-friendly types."""
    from decimal import Decimal as Dec
    out = {}
    for k, v in row.items():
        if isinstance(v, Dec):
            out[k] = float(v)
        elif isinstance(v, datetime):
            out[k] = v.isoformat()
        elif isinstance(v, date):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out


def run_pg(sql: str, params: tuple | None = None) -> list[dict]:
    if params:
        sql = _substitute_params(sql, params)
    _PG_SEMAPHORE.acquire()
    try:
        assert _pg_manager is not None, "McpSessionManager not started"
        return _pg_manager.run_sync(sql)
    finally:
        _PG_SEMAPHORE.release()


_bq_client: bigquery.Client | None = None
_bq_lock = threading.Lock()


def get_bq_client() -> bigquery.Client:
    global _bq_client
    if _bq_client is None:
        with _bq_lock:
            if _bq_client is None:
                if BQ_KEY_FILE and Path(BQ_KEY_FILE).exists():
                    os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", BQ_KEY_FILE)
                project = os.environ.get("GOOGLE_CLOUD_PROJECT", "supercat-data-pipeline")
                _bq_client = bigquery.Client(project=project)
    return _bq_client


def run_bq(sql: str) -> list[dict]:
    client = get_bq_client()
    result = client.query(sql).result()
    return [dict(row) for row in result]


def _bind(sql: str, ctx: RunContext) -> str:
    """Replace template placeholders with actual values."""
    s = sql
    s = s.replace("{{ORG_ID}}", str(ctx.org_id))
    s = s.replace("{{ORG_SHORTNAME}}", ctx.shortname)
    s = s.replace("{{CLIENT_NAME}}", ctx.client_name)
    s = s.replace("{{PERIOD_START}}", ctx.period_start.isoformat())
    s = s.replace("{{PERIOD_END}}", ctx.period_end.isoformat())
    s = s.replace("{{YYYY-MM-DD}}", ctx.run_date.isoformat())
    if ctx.gates.CLICKY_PREFIX:
        s = s.replace("{{CLICKY_PREFIX}}", ctx.gates.CLICKY_PREFIX)
    if ctx.org_summary.get("segment"):
        s = s.replace("{{SEGMENT}}", ctx.org_summary["segment"])
    brand = ctx.client_name.split()[0].upper() if ctx.client_name else ctx.shortname.upper()
    s = s.replace("{{ORG_BRAND_NAME}}", brand)
    return s


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def fmt_dollar(val: Any) -> str:
    if val is None:
        return "—"
    try:
        v = float(val)
    except (TypeError, ValueError):
        return str(val)
    if abs(v) >= 1_000_000:
        return f"${v / 1_000_000:,.1f}M"
    return f"${v:,.0f}"


def fmt_val(val: Any) -> str:
    if val is None:
        return "—"
    if isinstance(val, float):
        if val == int(val):
            return f"{int(val):,}"
        return f"{val:,.2f}"
    if isinstance(val, int):
        return f"{val:,}"
    if isinstance(val, datetime):
        return val.strftime("%Y-%m-%d %H:%M")
    if isinstance(val, date):
        return val.isoformat()
    return str(val)


DOLLAR_COLS = {
    "total_gmv", "gmv", "avg_order_value", "total_ecat_gmv", "ecat_gmv",
    "ecat_aov", "total_erp_gmv", "erp_gmv", "total_erp_sales", "sales_per_item",
    "erp_sales", "total_erp_invoiced", "historical_ecat_gmv", "ecat_gmv_12mo",
    "gmv_current_90d", "gmv_prev_90d", "sales_per_new_item", "total_amount",
    "ecat_originated_gmv", "portal_order_gmv",
    "territory_gmv", "customer_spend", "peak_spend", "gap_to_peak",
}


def format_cell(col: str, val: Any) -> str:
    col_lower = col.lower()
    if col_lower in DOLLAR_COLS or col_lower.endswith("_gmv") or col_lower.endswith("_sales"):
        return fmt_dollar(val)
    return fmt_val(val)


# ---------------------------------------------------------------------------
# Cache file writer
# ---------------------------------------------------------------------------

def write_cache_file(
    ctx: RunContext,
    filename: str,
    q_id: str,
    description: str,
    rows: list[dict],
    extra_header: str = "",
) -> None:
    """Write a Q-XX_results.md cache file in the locked format."""
    path = ctx.cache_dir / filename
    cols = list(rows[0].keys()) if rows else []
    header = (
        f"# {q_id} Results — {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})\n"
        f"- **Query**: {q_id} — {description}\n"
        f"- **Period**: LTM ({ctx.period_start} to {ctx.period_end})\n"
        f"- **Row count**: {len(rows)}\n"
        f"- **Run date**: {ctx.run_date}\n"
    )
    if extra_header:
        header += extra_header
    header += "\n"

    if rows:
        col_header = "| " + " | ".join(cols) + " |"
        col_sep = "| " + " | ".join("---" for _ in cols) + " |"
        lines = [header, col_header, col_sep]
        for row in rows:
            cells = [format_cell(c, row[c]) for c in cols]
            lines.append("| " + " | ".join(cells) + " |")
        content = "\n".join(lines) + "\n"
    else:
        content = header + "\n*(No data returned)*\n"

    path.write_text(content, encoding="utf-8")
    log.info("Wrote %s (%d rows)", filename, len(rows))


# ---------------------------------------------------------------------------
# Query execution with retry
# ---------------------------------------------------------------------------

def _execute_query(
    ctx: RunContext,
    q_id: str,
    description: str,
    sql: str,
    source: str,
    filename: str,
    extra_header: str = "",
) -> tuple[str, list[dict] | None]:
    """Run a query with retry + backoff on failure. Returns (q_id, rows_or_None)."""
    cache_path = ctx.cache_dir / filename
    if cache_path.exists():
        text = cache_path.read_text(encoding="utf-8")
        if f"# {q_id}" in text and "Row count" in text:
            log.info("Skipping %s — already cached", q_id)
            return q_id, None

    if ctx.dry_run:
        log.info("[DRY-RUN] Would run %s (%s) via %s", q_id, description, source)
        return q_id, None

    bound_sql = _bind(sql, ctx)
    runner = run_bq if source == "bigquery" else run_pg
    max_attempts = 3 if source == "postgres" else 2
    backoff_secs = [0, 5, 15]

    for attempt in range(max_attempts):
        try:
            if attempt > 0 and backoff_secs[attempt] > 0:
                log.info("Query %s — backoff %ds before retry %d", q_id, backoff_secs[attempt], attempt + 1)
                time.sleep(backoff_secs[attempt])
            rows = runner(bound_sql)
            write_cache_file(ctx, filename, q_id, description, rows, extra_header)
            ctx.completed_queries.append(q_id)
            return q_id, rows
        except Exception as exc:
            if attempt < max_attempts - 1:
                log.warning("Query %s failed (attempt %d/%d), retrying: %s", q_id, attempt + 1, max_attempts, exc)
            else:
                log.error("Query %s failed after %d attempts: %s", q_id, max_attempts, exc)
                ctx.failed_queries.append({
                    "q_id": q_id,
                    "reason": str(exc)[:200],
                    "retry": "y",
                })
                return q_id, None
    return q_id, None


# ---------------------------------------------------------------------------
# Preflight: Stage 0 + Stage 1
# ---------------------------------------------------------------------------

def run_stage0(ctx: RunContext) -> None:
    """Minimum-commerce gate — determine report mode."""
    log.info("=== Stage 0: Minimum-Commerce Gate ===")

    ltm_ecat = run_pg(
        "SELECT COUNT(*) AS ltm_ecat_orders FROM orders "
        "WHERE organization_id = %s AND is_submitted = true "
        "AND (is_marked_deleted = false OR is_marked_deleted IS NULL) "
        "AND created_at >= NOW() - INTERVAL '12 months'",
        (ctx.org_id,),
    )
    ctx.gates.ltm_ecat_orders = ltm_ecat[0]["ltm_ecat_orders"]

    ltm_erp = run_pg(
        "SELECT COUNT(*) AS ltm_erp_orders FROM portal_orders "
        "WHERE organization_id = %s AND order_date >= NOW() - INTERVAL '12 months'",
        (ctx.org_id,),
    )
    ctx.gates.ltm_erp_orders = ltm_erp[0]["ltm_erp_orders"]

    alltime = run_pg(
        "SELECT COUNT(*) AS alltime_ecat_orders, "
        "ROUND(COALESCE(SUM(total), 0)::numeric, 2) AS alltime_ecat_gmv, "
        "MAX(created_at) AS last_ecat_order_date "
        "FROM orders WHERE organization_id = %s AND is_submitted = true "
        "AND (is_marked_deleted = false OR is_marked_deleted IS NULL)",
        (ctx.org_id,),
    )
    ctx.gates.alltime_ecat_orders = alltime[0]["alltime_ecat_orders"]
    ctx.gates.alltime_ecat_gmv = float(alltime[0]["alltime_ecat_gmv"] or 0)
    last_date = alltime[0]["last_ecat_order_date"]
    if last_date:
        ctx.gates.last_ecat_order_date = str(last_date)[:10] if isinstance(last_date, str) else str(last_date.date())
    else:
        ctx.gates.last_ecat_order_date = None

    if ctx.gates.ltm_ecat_orders > 0 or ctx.gates.ltm_erp_orders > 0:
        ctx.gates.report_mode = 1
        ctx.gates.mode_label = "Mode 1: Standard Intelligence Report"
    elif ctx.gates.alltime_ecat_orders == 0:
        ctx.gates.report_mode = 2
        ctx.gates.mode_label = "Mode 2: Platform Activation Report"
    else:
        ctx.gates.report_mode = 3
        ctx.gates.mode_label = "Mode 3: Platform Reactivation Report"

    log.info("Report mode: %s", ctx.gates.mode_label)


def run_preflight(ctx: RunContext) -> None:
    """Stage 1 preflight: org identity, BigQuery org_summary, data presence, rep qualification."""
    log.info("=== Stage 1: Preflight ===")

    # §1.1 — org identity (already resolved via CLI args, but fetch name if needed)
    if not ctx.client_name or ctx.client_name == "":
        org_row = run_pg(
            "SELECT id, shortname, name FROM organizations WHERE id = %s LIMIT 1",
            (ctx.org_id,),
        )
        if org_row:
            ctx.client_name = org_row[0]["name"]

    # §1.2 — BigQuery org_summary
    log.info("Fetching org_summary from BigQuery...")
    org_summary_sql = (
        "SELECT * FROM `supercat-data-pipeline.insightful_product.org_summary` "
        f"WHERE org_shortname = '{ctx.shortname}'"
    )
    try:
        os_rows = run_bq(org_summary_sql)
        if os_rows:
            ctx.org_summary = dict(os_rows[0])
            rs = str(ctx.org_summary.get("recurring_services", "") or "")
            ctx.gates.HAS_CLICKY = bool(ctx.org_summary.get("has_clicky_portal"))
            ctx.gates.HAS_CART = "B2B Cart" in rs
            ctx.gates.HAS_PORTAL_ORDERS = "Portal" in rs
            if ctx.org_summary.get("clicky_prefix"):
                ctx.gates.CLICKY_PREFIX = str(ctx.org_summary["clicky_prefix"])
            if not ctx.bundle_label:
                ctx.bundle_label = str(ctx.org_summary.get("feature_depth", "") or "")
            if ctx.org_summary.get("segment"):
                ctx.gates.evidence["segment"] = ctx.org_summary["segment"]
            if not ctx.client_name and ctx.org_summary.get("org_name"):
                ctx.client_name = str(ctx.org_summary["org_name"])
            ctx.gates.evidence["HAS_CLICKY"] = f"has_clicky_portal={ctx.org_summary.get('has_clicky_portal')}"
            ctx.gates.evidence["HAS_CART"] = f"recurring_services contains B2B Cart: {'B2B Cart' in rs}"
            ctx.gates.evidence["HAS_PORTAL_ORDERS_org_summary"] = f"recurring_services contains Portal: {'Portal' in rs}"
        else:
            log.warning("No org_summary row found for shortname=%s", ctx.shortname)
    except Exception as exc:
        log.error("BigQuery org_summary lookup failed: %s", exc)

    # Clicky prefix resolution
    if ctx.gates.HAS_CLICKY and not ctx.gates.CLICKY_PREFIX:
        log.info("Resolving Clicky prefix...")
        try:
            tables = run_bq(
                "SELECT table_name "
                "FROM `supercat-data-pipeline.clicky_analytics.INFORMATION_SCHEMA.TABLES` "
                "WHERE table_name LIKE '%_daily_metrics' ORDER BY table_name"
            )
            for t in tables:
                tn = t["table_name"]
                if ctx.shortname in tn:
                    ctx.gates.CLICKY_PREFIX = tn.replace("_daily_metrics", "")
                    log.info("Resolved CLICKY_PREFIX=%s", ctx.gates.CLICKY_PREFIX)
                    break
            if not ctx.gates.CLICKY_PREFIX:
                log.warning("Could not resolve Clicky prefix — disabling HAS_CLICKY")
                ctx.gates.HAS_CLICKY = False
        except Exception as exc:
            log.error("Clicky prefix resolution failed: %s", exc)
            ctx.gates.HAS_CLICKY = False

    # §1.3 — data presence checks (Postgres)
    log.info("Running data presence checks...")

    inv_rows = run_pg(
        "SELECT COUNT(*) AS inventory_count FROM inventories WHERE organization_id = %s",
        (ctx.org_id,),
    )
    ctx.gates.HAS_INVENTORY = inv_rows[0]["inventory_count"] > 0
    ctx.gates.evidence["HAS_INVENTORY"] = f"inventory_count={inv_rows[0]['inventory_count']}"

    portal_rows = run_pg(
        "SELECT COUNT(*) AS portal_order_count, "
        "COALESCE(SUM(total_amount), 0) AS portal_order_gmv "
        "FROM portal_orders WHERE organization_id = %s "
        "AND order_date >= NOW() - INTERVAL '12 months'",
        (ctx.org_id,),
    )
    po_count = portal_rows[0]["portal_order_count"]
    po_gmv = float(portal_rows[0]["portal_order_gmv"] or 0)
    if po_count == 0 or po_gmv == 0:
        ctx.gates.HAS_PORTAL_ORDERS = False
        ctx.gates.validation_log.append(
            f"portal_orders LTM count={po_count}, gmv={po_gmv} — HAS_PORTAL_ORDERS overridden to false"
        )
    else:
        ctx.gates.HAS_PORTAL_ORDERS = True
    ctx.gates.evidence["HAS_PORTAL_ORDERS"] = f"portal_order_count={po_count}, portal_order_gmv={fmt_dollar(po_gmv)}"

    sales_rows = run_pg(
        "SELECT COUNT(*) AS sales_data_count FROM sales_data WHERE organization_id = %s",
        (ctx.org_id,),
    )
    ctx.gates.HAS_SALES_DATA = sales_rows[0]["sales_data_count"] > 0
    ctx.gates.evidence["HAS_SALES_DATA"] = f"sales_data_count={sales_rows[0]['sales_data_count']}"

    server_rows = run_pg(
        "SELECT COUNT(*) AS server_order_count FROM orders "
        "WHERE organization_id = %s AND is_submitted = true "
        "AND (is_marked_deleted = false OR is_marked_deleted IS NULL) "
        "AND order_source = 'server'",
        (ctx.org_id,),
    )
    if server_rows[0]["server_order_count"] == 0:
        ctx.gates.HAS_CART = False
        ctx.gates.evidence["HAS_CART"] += f"; server_order_count=0 — overridden to false"

    # §1.3a — ERP enrichment preflight
    if ctx.gates.HAS_PORTAL_ORDERS:
        log.info("Running ERP enrichment preflight...")
        erp_pf = run_pg(
            "SELECT MAX(order_date) AS most_recent_erp_order, "
            "EXTRACT(DAY FROM NOW() - MAX(order_date))::int AS days_since_last_erp_order, "
            "COUNT(DISTINCT CASE WHEN rep_name IS NOT NULL AND rep_name != '' THEN rep_name END) AS distinct_rep_names, "
            "COUNT(DISTINCT CASE WHEN customer_bill_to_number IS NOT NULL THEN customer_bill_to_number END) AS distinct_bill_to_customers "
            "FROM portal_orders WHERE organization_id = %s AND order_date >= NOW() - INTERVAL '12 months'",
            (ctx.org_id,),
        )
        if erp_pf:
            row = erp_pf[0]
            days_since = row["days_since_last_erp_order"] or 9999
            ctx.gates.PORTAL_ORDERS_FRESH = days_since <= 60
            ctx.gates.PORTAL_REP_DATA_PRESENT = (row["distinct_rep_names"] or 0) > 0
            ctx.gates.PORTAL_CUSTOMER_DATA_PRESENT = (row["distinct_bill_to_customers"] or 0) > 0
            ctx.gates.evidence["PORTAL_ORDERS_FRESH"] = f"days_since_last_erp_order={days_since} (threshold: <=60)"
            ctx.gates.evidence["PORTAL_REP_DATA_PRESENT"] = f"distinct_rep_names={row['distinct_rep_names']}"
            ctx.gates.evidence["PORTAL_CUSTOMER_DATA_PRESENT"] = f"distinct_bill_to_customers={row['distinct_bill_to_customers']}"

    # §1.3b — Commitment data availability
    commit_rows = run_pg(
        "SELECT COUNT(*) AS commit_count FROM commitment_reports WHERE organization_id = %s",
        (ctx.org_id,),
    )
    commit_count = commit_rows[0]["commit_count"] if commit_rows else 0
    ctx.gates.HAS_COMMITMENT_DATA = commit_count > 0
    ctx.gates.evidence["HAS_COMMITMENT_DATA"] = f"commitment_reports_count={commit_count}"

    # §1.3c — New items availability
    new_item_rows = run_pg(
        "SELECT COUNT(*) AS cnt FROM products WHERE organization_id = %s AND new_item = true AND (deleted = false OR deleted IS NULL)",
        (ctx.org_id,),
    )
    new_item_count = new_item_rows[0]["cnt"] if new_item_rows else 0
    ctx.gates.HAS_NEW_ITEMS = new_item_count > 0
    ctx.gates.evidence["HAS_NEW_ITEMS"] = f"new_item_count={new_item_count}"

    # §1.3d — Buyer name availability (for buyer-within-account intelligence)
    buyer_rows = run_pg(
        "SELECT COUNT(DISTINCT LOWER(TRIM(buyer_name))) AS cnt FROM portal_orders WHERE organization_id = %s AND buyer_name IS NOT NULL AND TRIM(buyer_name) != '' AND order_date >= NOW() - INTERVAL '6 months'",
        (ctx.org_id,),
    )
    buyer_count = buyer_rows[0]["cnt"] if buyer_rows else 0
    ctx.gates.HAS_BUYER_DATA = buyer_count >= 10
    ctx.gates.evidence["HAS_BUYER_DATA"] = f"distinct_buyers_6mo={buyer_count}"

    # §1.3e — Mixpanel data presence preflight (must run before build_query_plan)
    log.info("Checking Mixpanel data presence...")
    try:
        mp_check = run_bq(
            "SELECT COUNT(*) AS n "
            "FROM `supercat-data-pipeline.WELD_RAW.mixpanel__events` "
            f"WHERE LOWER(COALESCE(current_organization_shortname, organization_shortname)) = '{ctx.shortname}' "
            "AND TIMESTAMP_SECONDS(CAST(time AS INT64)) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY) "
            "LIMIT 1"
        )
        mp_count = mp_check[0]["n"] if mp_check else 0
        ctx.gates.MIXPANEL_USER_DATA_PRESENT = mp_count > 0
        ctx.gates.evidence["MIXPANEL_USER_DATA_PRESENT_preflight"] = f"Mixpanel events (LTM): {mp_count}"
        log.info("Mixpanel preflight: %d events found → MIXPANEL_USER_DATA_PRESENT=%s", mp_count, ctx.gates.MIXPANEL_USER_DATA_PRESENT)
    except Exception as exc:
        log.warning("Mixpanel preflight check failed: %s — will recheck after Q-01", exc)

    # §1.4 — Peer benchmark availability (BigQuery only, per instructions)
    log.info("Checking peer benchmark availability...")
    try:
        peer_rows = run_bq(
            "SELECT org_shortname, segment, peer_standing "
            "FROM `supercat-data-pipeline.insightful_product.segment_peer_comparison` "
            f"WHERE org_shortname = '{ctx.shortname}'"
        )
        ctx.gates.HAS_PEER_DATA = len(peer_rows) > 0
        if peer_rows:
            ctx.gates.BENCHMARK_ELIGIBLE = True
            ctx.gates.evidence["HAS_PEER_DATA"] = f"segment_peer_comparison row found, segment={peer_rows[0].get('segment')}"
            if peer_rows[0].get("segment"):
                ctx.org_summary["segment"] = peer_rows[0]["segment"]
        else:
            ctx.gates.evidence["HAS_PEER_DATA"] = "No segment_peer_comparison row found"
    except Exception as exc:
        log.warning("Peer benchmark check failed: %s", exc)
        ctx.gates.HAS_PEER_DATA = False
        ctx.gates.evidence["HAS_PEER_DATA"] = f"BigQuery query failed: {str(exc)[:100]}"

    # §1.5 — qualifying reps
    log.info("Checking qualifying rep count...")
    qual_rows = run_pg(
        "SELECT COUNT(*) AS n FROM ("
        "  SELECT COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep "
        "  FROM orders WHERE organization_id = %s AND is_submitted = true "
        "  AND (is_marked_deleted = false OR is_marked_deleted IS NULL) "
        "  AND order_source = 'ipad' AND created_at >= NOW() - INTERVAL '12 months' "
        "  GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) "
        "  HAVING COUNT(*) >= 10"
        ") sub",
        (ctx.org_id,),
    )
    ctx.gates.QUALIFYING_REP_COUNT = qual_rows[0]["n"]
    ctx.gates.HAS_SALES_SECTION = ctx.gates.QUALIFYING_REP_COUNT >= 5
    ctx.gates.evidence["HAS_SALES_SECTION"] = f"qualifying_reps={ctx.gates.QUALIFYING_REP_COUNT} (threshold: >=5)"
    ctx.gates.evidence["QUALIFYING_REP_COUNT"] = str(ctx.gates.QUALIFYING_REP_COUNT)


# ---------------------------------------------------------------------------
# Inline preflight SQL (queries NOT in query_library.md)
# ---------------------------------------------------------------------------

# These are defined as functions that return SQL because they use %s params
# and are run during preflight, not from the query library.

# ---------------------------------------------------------------------------
# Query Batch Execution
# ---------------------------------------------------------------------------

def _q_spec(
    q_id: str,
    desc: str,
    sql: str,
    source: str,
    filename: str,
    extra_header: str = "",
) -> dict:
    return {
        "q_id": q_id,
        "description": desc,
        "sql": sql,
        "source": source,
        "filename": filename,
        "extra_header": extra_header,
    }


def build_query_plan(ctx: RunContext) -> list[list[dict]]:
    """Build parallel batches of queries based on gate flags.

    Returns a list of batches; each batch is a list of query specs
    that can be run concurrently.
    """
    ql = ctx.query_lib
    batches: list[list[dict]] = []

    # ── Batch A: Platform Health (always) ──
    batch_a: list[dict] = []
    for q_id, desc, filename in [
        ("Q-07", "Catalog Completeness Score", "Q-07_results.md"),
        ("Q-08", "Data Freshness Monitor", "Q-08_results.md"),
        ("Q-10", "Feature Enablement Gap Analysis", "Q-10_results.md"),
        ("Q-11", "Configuration Completeness", "Q-11_results.md"),
    ]:
        sql = _find_sql(ql, q_id)
        if sql:
            batch_a.append(_q_spec(q_id, desc, sql, "postgres", filename))

    # Q-09 has two sub-queries — import trend + recent imports
    q09_trend = _find_sql(ql, "Q-09")
    q09_recent = _find_sql(ql, "Q-09", idx=1)
    if q09_trend:
        batch_a.append(_q_spec("Q-09", "Import Health — Monthly Trend", q09_trend, "postgres", "Q-09_results.md"))
    if q09_recent:
        batch_a.append(_q_spec("Q-09-recent", "Import Health — Recent Errors", q09_recent, "postgres", "Q-09_recent_results.md"))

    batches.append(batch_a)

    # ── Batch B: Customer + Commerce (always) ──
    batch_b: list[dict] = []
    for q_id, desc, filename in [
        ("Q-12", "Customer Activation & ERP Penetration", "Q-12_results.md"),
        ("Q-20", "eCat AOV Analysis", "Q-20_results.md"),
        ("Q-21", "eCat Order Type & Workflow Analysis", "Q-21_results.md"),
    ]:
        sql = _find_sql(ql, q_id)
        if sql:
            batch_b.append(_q_spec(q_id, desc, sql, "postgres", filename))

    # Q-22 (BigQuery)
    q22_sql = _find_sql(ql, "Q-22")
    if q22_sql:
        batch_b.append(_q_spec("Q-22", "Feature Usage Depth", q22_sql, "bigquery", "Q-22_results.md"))

    # Q-18 Part A (always) and Part B (conditional)
    q18a = _find_sql(ql, "Q-18")
    if q18a:
        batch_b.append(_q_spec("Q-18-A", "eCat Order Velocity — Part A", q18a, "postgres", "Q-18_partA_results.md"))
    if ctx.gates.HAS_PORTAL_ORDERS:
        q18b = _find_sql(ql, "Q-18", idx=1)
        if q18b:
            batch_b.append(_q_spec("Q-18-B", "eCat Order Velocity — Part B (ERP)", q18b, "postgres", "Q-18_partB_results.md"))

    batches.append(batch_b)

    # ── Batch C: Customer Behavioral ──
    batch_c1: list[dict] = []
    for q_id, desc, filename in [
        ("Q-13", "Customer Concentration Risk", "Q-13_results.md"),
        ("Q-14", "Customer Reorder Frequency", "Q-14_results.md"),
    ]:
        sql = _find_sql(ql, q_id)
        if sql:
            batch_c1.append(_q_spec(q_id, desc, sql, "postgres", filename))

    # Q-14b: Account velocity deceleration (gated on portal_orders)
    if ctx.gates.HAS_PORTAL_ORDERS:
        q14b = _find_sql(ql, "Q-14b")
        if q14b:
            batch_c1.append(_q_spec("Q-14b", "Account Velocity Deceleration Detection", q14b, "postgres", "Q-14b_results.md"))

    batches.append(batch_c1)

    batch_c2: list[dict] = []
    # Q-17 has two sub-queries: lapsed + at-risk
    q17_lapsed = _find_sql(ql, "Q-17")
    q17_atrisk = _find_sql(ql, "Q-17", idx=1)
    if q17_lapsed:
        batch_c2.append(_q_spec("Q-17", "Dormant eCat Customers — Lapsed", q17_lapsed, "postgres", "Q-17_results.md"))
    if q17_atrisk:
        batch_c2.append(_q_spec("Q-17-atrisk", "Dormant eCat Customers — At-Risk", q17_atrisk, "postgres", "Q-17_atrisk_results.md"))

    # Q-41 has two sub-queries: by month/channel + by rep
    q41_channel = _find_sql(ql, "Q-41")
    q41_rep = _find_sql(ql, "Q-41", idx=1)
    if q41_channel:
        batch_c2.append(_q_spec("Q-41", "First-Time eCat Orderers — By Channel", q41_channel, "postgres", "Q-41_results.md"))
    if q41_rep:
        batch_c2.append(_q_spec("Q-41-rep", "First-Time eCat Orderers — By Rep", q41_rep, "postgres", "Q-41_rep_results.md"))
    batches.append(batch_c2)

    # Q-40 (always)
    q40 = _find_sql(ql, "Q-40")
    if q40:
        batches.append([_q_spec("Q-40", "Regional Sales Distribution", q40, "postgres", "Q-40_results.md")])

    # ── Batch D: Conditional queries ──
    batch_d: list[dict] = []

    # Q-01 Step 1 (BigQuery Mixpanel) — gated on HAS_SALES_SECTION
    if ctx.gates.HAS_SALES_SECTION:
        q01_s1 = _find_sql(ql, "Q-01")
        if q01_s1:
            batch_d.append(_q_spec("Q-01-S1", "Rep Behavioral Scorecard — Step 1 (Mixpanel)", q01_s1, "bigquery", "Q-01_step1_results.md"))

    # Q-06 — gated on HAS_SALES_SECTION
    if ctx.gates.HAS_SALES_SECTION:
        q06 = _find_sql(ql, "Q-06")
        if q06:
            batch_d.append(_q_spec("Q-06", "Rep Engagement Trajectory", q06, "postgres", "Q-06_results.md"))

    # Q-05 (always for seat utilization)
    q05 = _find_sql(ql, "Q-05")
    if q05:
        batch_d.append(_q_spec("Q-05", "Seat Utilization", q05, "postgres", "Q-05_results.md"))

    # Q-47 smart stacks
    q47 = _find_sql(ql, "Q-47")
    if q47:
        batch_d.append(_q_spec("Q-47", "Smart Stack Effectiveness", q47, "postgres", "Q-47_results.md"))

    # Q-50 library documents
    q50 = _find_sql(ql, "Q-50")
    if q50:
        batch_d.append(_q_spec("Q-50", "Library / Document Inventory", q50, "postgres", "Q-50_results.md"))

    # Q-04 non-selling user classification (BigQuery, gated on HAS_SALES_SECTION)
    if ctx.gates.HAS_SALES_SECTION:
        q04 = _find_sql(ql, "Q-04")
        if q04:
            batch_d.append(_q_spec("Q-04", "Non-Selling User Role Classification", q04, "bigquery", "Q-04_results.md"))

    if batch_d:
        batches.append(batch_d)

    # ── Batch E: HAS_SALES_SECTION dependent (Q-01 Step 2 must follow Step 1) ──
    # This runs sequentially after batch D so Q-01 Step 1 is done
    batch_e: list[dict] = []
    if ctx.gates.HAS_SALES_SECTION:
        q01_s2 = _find_sql(ql, "Q-01", idx=1)
        if q01_s2:
            batch_e.append(_q_spec("Q-01-S2", "Rep Behavioral Scorecard — Step 2 (Orders)", q01_s2, "postgres", "Q-01_step2_results.md"))

    # Q-43 territory coverage — needs preflight check
    if ctx.gates.HAS_SALES_SECTION:
        # Step 2 (always the same)
        q43_s2 = _find_sql(ql, "Q-43", idx=2)  # Step 2 eCat order activity
        if q43_s2:
            batch_e.append(_q_spec("Q-43-S2", "Territory — eCat Order Activity", q43_s2, "postgres", "Q-43_step2_results.md"))

    if batch_e:
        batches.append(batch_e)

    # ── Batch F: Portal orders conditional ──
    batch_f: list[dict] = []

    if ctx.gates.HAS_PORTAL_ORDERS:
        q16 = _find_sql(ql, "Q-16")
        if q16:
            batch_f.append(_q_spec("Q-16", "ERP Total Business Visibility", q16, "postgres", "Q-16_results.md"))

    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.PORTAL_REP_DATA_PRESENT:
        q51 = _find_sql(ql, "Q-51")
        if q51:
            batch_f.append(_q_spec("Q-51", "Rep-Level eCat Capture", q51, "postgres", "Q-51_results.md"))

    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.PORTAL_CUSTOMER_DATA_PRESENT:
        for q_id, desc, filename in [
            ("Q-52", "Customer-Level eCat Penetration", "Q-52_results.md"),
            ("Q-53", "Unactivated High-Value ERP Accounts", "Q-53_results.md"),
            ("Q-54", "Geographic eCat Penetration", "Q-54_results.md"),
        ]:
            sql = _find_sql(ql, q_id)
            if sql:
                batch_f.append(_q_spec(q_id, desc, sql, "postgres", filename))

    # Q-55: Category-level competitive displacement (requires portal_orders)
    if ctx.gates.HAS_PORTAL_ORDERS:
        q55 = _find_sql(ql, "Q-55")
        if q55:
            batch_f.append(_q_spec("Q-55", "Category-Level Competitive Displacement", q55, "postgres", "Q-55_results.md"))

    # Q-56: Per-rep capture rate trend (requires portal_orders + rep data)
    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.PORTAL_REP_DATA_PRESENT:
        q56 = _find_sql(ql, "Q-56")
        if q56:
            batch_f.append(_q_spec("Q-56", "Per-Rep Capture Rate Trend", q56, "postgres", "Q-56_results.md"))

    # Q-57: Cross-sell whitespace by category (requires portal_orders + customer data)
    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.PORTAL_CUSTOMER_DATA_PRESENT:
        q57 = _find_sql(ql, "Q-57")
        if q57:
            batch_f.append(_q_spec("Q-57", "Cross-Sell Whitespace by Category", q57, "postgres", "Q-57_results.md"))

    # Q-49 buyer repeat purchase (conditional on buyer attribution)
    if ctx.gates.HAS_PORTAL_ORDERS:
        q49 = _find_sql(ql, "Q-49")
        # The full Q-49 is the repeat purchase query; there's also a gate check
        q49_gate = _find_sql(ql, "Q-49", idx=0)
        if q49_gate:
            batch_f.append(_q_spec("Q-49-gate", "Buyer Attribution Gate Check", q49_gate, "postgres", "Q-49_gate_results.md"))

    if batch_f:
        batches.append(batch_f)

    # ── Batch G: Inventory + Sales Data conditional ──
    batch_g: list[dict] = []
    if ctx.gates.HAS_INVENTORY and ctx.gates.HAS_SALES_DATA:
        q37 = _find_sql(ql, "Q-37")
        if q37:
            batch_g.append(_q_spec("Q-37", "Inventory × Sales Intelligence (OOS Top Sellers)", q37, "postgres", "Q-37_results.md"))
    if ctx.gates.HAS_SALES_DATA:
        q39_cat = _find_sql(ql, "Q-39")
        q39_col = _find_sql(ql, "Q-39", idx=1)
        if q39_cat:
            batch_g.append(_q_spec("Q-39-cat", "Line Analysis by Category", q39_cat, "postgres", "Q-39_category_results.md"))
        if q39_col:
            batch_g.append(_q_spec("Q-39-col", "Line Analysis by Collection", q39_col, "postgres", "Q-39_collection_results.md"))
        q42 = _find_sql(ql, "Q-42")
        if q42:
            batch_g.append(_q_spec("Q-42", "New Item Performance", q42, "postgres", "Q-42_results.md"))

    # Q-38a — portal_order_items conditional
    q38a = _find_sql(ql, "Q-38a")
    if q38a:
        # Check if portal_order_items exist
        try:
            poi_rows = run_pg(
                "SELECT COUNT(*) AS n FROM portal_order_items WHERE organization_id = %s",
                (ctx.org_id,),
            )
            if poi_rows[0]["n"] > 0:
                batch_g.append(_q_spec("Q-38a", "Product Velocity Trend", q38a, "postgres", "Q-38a_results.md"))
        except Exception:
            pass

    # Q-40 regional × category cross-tab (requires sales_data)
    if ctx.gates.HAS_SALES_DATA:
        q40_xtab = _find_sql(ql, "Q-40", idx=1)
        if q40_xtab:
            batch_g.append(_q_spec("Q-40-xtab", "Regional × Category Cross-tab", q40_xtab, "postgres", "Q-40_crosstab_results.md"))

    # Q-59: Fill Rate & Backorder Revenue Impact (requires portal_order_items)
    if ctx.gates.HAS_PORTAL_ORDERS:
        q59 = _find_sql(ql, "Q-59")
        if q59:
            batch_g.append(_q_spec("Q-59", "Fill Rate & Backorder Revenue Impact", q59, "postgres", "Q-59_results.md"))

    if batch_g:
        batches.append(batch_g)

    # ── Batch H: Clicky (HAS_CLICKY) ──
    if ctx.gates.HAS_CLICKY:
        batch_h: list[dict] = []
        for q_id, desc, filename in [
            ("Q-CL-01", "Portal Traffic Health", "Q-CL-01_results.md"),
            ("Q-CL-03", "Geographic Demand Map", "Q-CL-03_results.md"),
            ("Q-CL-05", "Traffic Source Intelligence", "Q-CL-05_results.md"),
        ]:
            sql = _find_sql(ql, q_id)
            if sql:
                batch_h.append(_q_spec(q_id, desc, sql, "bigquery", filename))
        if batch_h:
            batches.append(batch_h)

    # ── Batch I: Peer Benchmark (HAS_PEER_DATA) ──
    if ctx.gates.HAS_PEER_DATA:
        batch_i: list[dict] = []
        for q_id, desc, filename in [
            ("Q-CI-02", "Peer Comparison", "Q-CI-02_results.md"),
            ("Q-CI-03", "Feature Adoption Benchmarking", "Q-CI-03_results.md"),
            ("Q-CI-05, Q-CI-06", "Top Performers & Best Practices", "Q-CI-05_results.md"),
        ]:
            sql = _find_sql(ql, q_id)
            if sql:
                batch_i.append(_q_spec(q_id, desc, sql, "bigquery", filename))

        # Q-CI-03 also needs segment_benchmarks_monthly
        if ctx.org_summary.get("segment"):
            q_ci03_bench = _find_sql(ql, "Q-CI-03", idx=1)
            if q_ci03_bench:
                batch_i.append(_q_spec("Q-CI-03-bench", "Segment Benchmarks Monthly", q_ci03_bench, "bigquery", "Q-CI-03_benchmarks_results.md"))
        if batch_i:
            batches.append(batch_i)

    # ── Batch J: VM-45 capture rate (conditional on denominator gates) ──
    if ctx.gates.HAS_PORTAL_ORDERS:
        q45 = _find_sql(ql, "Q-45")
        if q45:
            batches.append([_q_spec("Q-45", "eCat Capture Rate vs. Total Business", q45, "postgres", "Q-45_results.md")])

    # ── Batch J2: Market Commitment Conversion (HAS_COMMITMENT_DATA) ──
    if ctx.gates.HAS_COMMITMENT_DATA:
        q58 = _find_sql(ql, "Q-58")
        if q58:
            batches.append([_q_spec("Q-58", "Market Commitment Conversion", q58, "postgres", "Q-58_results.md")])

    # ── Batch J3: Uncommitted Market Items In Stock (HAS_COMMITMENT_DATA + HAS_INVENTORY) ──
    if ctx.gates.HAS_COMMITMENT_DATA and ctx.gates.HAS_INVENTORY:
        q58b = _find_sql(ql, "Q-58b")
        if q58b:
            batches.append([_q_spec("Q-58b", "Uncommitted Market Items In Stock", q58b, "postgres", "Q-58b_results.md")])

    # ── Batch J4: Price Erosion / Trade-Down Detection (HAS_PORTAL_ORDERS) ──
    if ctx.gates.HAS_PORTAL_ORDERS:
        q60 = _find_sql(ql, "Q-60")
        if q60:
            batches.append([_q_spec("Q-60", "Price Erosion / Trade-Down Detection", q60, "postgres", "Q-60_results.md")])

    # ── Batch J5: New Intro Adoption Gap (HAS_PORTAL_ORDERS + HAS_NEW_ITEMS) ──
    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.HAS_NEW_ITEMS:
        q61 = _find_sql(ql, "Q-61")
        if q61:
            batches.append([_q_spec("Q-61", "New Introduction Adoption Gap", q61, "postgres", "Q-61_results.md")])

    # ── Batch J6: Product Launch Velocity by Rep (HAS_PORTAL_ORDERS + HAS_NEW_ITEMS) ──
    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.HAS_NEW_ITEMS:
        q62 = _find_sql(ql, "Q-62")
        if q62:
            batches.append([_q_spec("Q-62", "Product Launch Velocity by Rep", q62, "postgres", "Q-62_results.md")])

    # ── Batch L: Mixpanel Behavioral — Presentation-to-Order + Selling Time ──
    if ctx.gates.MIXPANEL_USER_DATA_PRESENT:
        batch_l: list[dict] = []
        q63 = _find_sql(ql, "Q-63")
        if q63:
            batch_l.append(_q_spec("Q-63", "Presentation-to-Order Conversion", q63, "bigquery", "Q-63_results.md"))
        q65 = _find_sql(ql, "Q-65")
        if q65:
            batch_l.append(_q_spec("Q-65", "Selling vs Admin Time Ratio", q65, "bigquery", "Q-65_results.md"))
        if batch_l:
            batches.append(batch_l)

    # ── Batch L2: Rep Engagement vs Account Revenue (MIXPANEL + PORTAL) ──
    if ctx.gates.MIXPANEL_USER_DATA_PRESENT and ctx.gates.HAS_PORTAL_ORDERS:
        q64 = _find_sql(ql, "Q-64")
        if q64:
            batches.append([_q_spec("Q-64", "Rep Engagement vs Account Revenue", q64, "bigquery", "Q-64_results.md")])

    # ── Batch M: Account-Level Intelligence (Postgres) ──
    if ctx.gates.HAS_PORTAL_ORDERS:
        batch_m: list[dict] = []
        q66 = _find_sql(ql, "Q-66")
        if q66 and ctx.gates.HAS_BUYER_DATA:
            batch_m.append(_q_spec("Q-66", "Buyer-Within-Account Intelligence", q66, "postgres", "Q-66_results.md"))
        q67 = _find_sql(ql, "Q-67")
        if q67 and ctx.gates.PORTAL_CUSTOMER_DATA_PRESENT:
            batch_m.append(_q_spec("Q-67", "Geographic Revenue Displacement", q67, "postgres", "Q-67_results.md"))
        q68 = _find_sql(ql, "Q-68")
        if q68 and ctx.gates.PORTAL_CUSTOMER_DATA_PRESENT:
            batch_m.append(_q_spec("Q-68", "Spending Contraction Detection", q68, "postgres", "Q-68_results.md"))
        if batch_m:
            batches.append(batch_m)

    # ── Batch N: New queries (Q-69 order timing, Q-70 inactive reps) ──
    batch_n: list[dict] = []
    q69 = _find_sql(ql, "Q-69")
    if q69:
        batch_n.append(_q_spec("Q-69", "Order Timing Distribution", q69, "postgres", "Q-69_results.md"))

    if ctx.gates.HAS_PORTAL_ORDERS and ctx.gates.PORTAL_REP_DATA_PRESENT:
        q70 = _find_sql(ql, "Q-70")
        if q70:
            batch_n.append(_q_spec("Q-70", "Inactive Reps with Territory Revenue", q70, "postgres", "Q-70_results.md"))

    if batch_n:
        batches.append(batch_n)

    # ── Batch K: Q-46 workflow maturity (Postgres + BigQuery) ──
    q46_pg = _find_sql(ql, "Q-46")
    q46_bq = _find_sql(ql, "Q-46", idx=1)
    batch_k: list[dict] = []
    if q46_pg:
        batch_k.append(_q_spec("Q-46-pg", "Workflow Maturity — Postgres", q46_pg, "postgres", "Q-46_pg_results.md"))
    if q46_bq:
        batch_k.append(_q_spec("Q-46-bq", "Workflow Maturity — Mixpanel", q46_bq, "bigquery", "Q-46_bq_results.md"))
    if batch_k:
        batches.append(batch_k)

    return batches


def _find_sql(ql: dict[str, str], q_id: str, idx: int = 0) -> str | None:
    """Find a SQL block from the parsed query library by Q-ID.

    idx selects which SQL block under that header (0 = first, 1 = second, etc.).
    Falls back to numbered keys for multi-block headers.
    """
    if idx == 0:
        if q_id in ql:
            return ql[q_id]
        # Try partial match for compound IDs like "Q-CI-05, Q-CI-06"
        for key in ql:
            if q_id.replace(" ", "") in key.replace(" ", ""):
                return ql[key]
        return None

    # For idx > 0, look for the _N suffixed keys
    target_key = f"{q_id}_{idx + 1}"
    if target_key in ql:
        return ql[target_key]

    # Or try scanning for keys that start with q_id
    matches = sorted(k for k in ql if k.startswith(q_id))
    if len(matches) > idx:
        return ql[matches[idx]]
    return None


def execute_batches(ctx: RunContext, batches: list[list[dict]]) -> dict[str, list[dict] | None]:
    """Execute query batches, returning {q_id: rows} for queries that returned data.

    Late batches (after batch 6) use reduced parallelism and inter-batch cooldown
    to avoid exhausting the MCP Postgres connection pool.
    """
    results: dict[str, list[dict] | None] = {}

    for batch_num, batch in enumerate(batches, 1):
        if not batch:
            continue

        has_pg = any(s["source"] == "postgres" for s in batch)
        if batch_num > 4 and has_pg:
            max_workers = min(len(batch), 3)
        else:
            max_workers = min(len(batch), 5)

        log.info("--- Batch %d: %d queries (max_workers=%d) ---", batch_num, len(batch), max_workers)

        if ctx.dry_run:
            for spec in batch:
                log.info("[DRY-RUN] %s — %s (%s)", spec["q_id"], spec["description"], spec["source"])
            continue

        if batch_num > 4 and has_pg:
            log.info("Inter-batch cooldown (1s) before batch %d...", batch_num)
            time.sleep(1)

        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {}
            for spec in batch:
                f = pool.submit(
                    _execute_query,
                    ctx,
                    spec["q_id"],
                    spec["description"],
                    spec["sql"],
                    spec["source"],
                    spec["filename"],
                    spec.get("extra_header", ""),
                )
                futures[f] = spec["q_id"]

            for f in as_completed(futures):
                q_id = futures[f]
                try:
                    returned_id, rows = f.result()
                    results[returned_id] = rows
                except Exception as exc:
                    log.error("Unexpected error running %s: %s", q_id, exc)
                    ctx.failed_queries.append({"q_id": q_id, "reason": str(exc)[:200], "retry": "n"})

    return results


# ---------------------------------------------------------------------------
# Showroom Scan (Derived Gate 2)
# ---------------------------------------------------------------------------

def run_showroom_scan(ctx: RunContext) -> None:
    """Pass 1 keyword scan and Pass 2 brand-name scan for operational accounts."""
    if not ctx.gates.HAS_SALES_SECTION or ctx.dry_run:
        return
    log.info("Running showroom/operational account scan...")

    # Pass 1 — keyword scan
    pass1_sql = (
        "SELECT COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name, "
        "COUNT(*) AS order_count, ROUND(SUM(total)::numeric, 2) AS gmv "
        "FROM orders WHERE organization_id = %s AND is_submitted = true "
        "AND (is_marked_deleted = false OR is_marked_deleted IS NULL) "
        "AND created_at >= NOW() - INTERVAL '12 months' "
        "AND (rep_first_name ILIKE '%%showroom%%' OR rep_last_name ILIKE '%%showroom%%' "
        "OR rep_first_name ILIKE '%%admin%%' OR rep_first_name ILIKE '%%marketing%%' "
        "OR rep_first_name ILIKE '%%training%%' OR rep_first_name ILIKE '%%test%%' "
        "OR rep_first_name ILIKE '%%demo%%' OR rep_first_name ILIKE '%%market helper%%' "
        "OR rep_last_name ILIKE '%%market helper%%' OR rep_first_name ILIKE '%%helper%%' "
        "OR rep_first_name ILIKE '%%office%%' OR rep_last_name ILIKE '%%office%%') "
        "GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) "
        "ORDER BY gmv DESC"
    )
    pass1_rows = run_pg(pass1_sql, (ctx.org_id,))

    # Pass 2 — brand name scan
    brand = ctx.client_name.split()[0].upper() if ctx.client_name else ctx.shortname.upper()
    pass2_sql = (
        "SELECT COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) AS rep_name, "
        "COUNT(*) AS order_count, ROUND(SUM(total)::numeric, 2) AS gmv "
        "FROM orders WHERE organization_id = %s AND is_submitted = true "
        "AND (is_marked_deleted = false OR is_marked_deleted IS NULL) "
        "AND created_at >= NOW() - INTERVAL '12 months' "
        f"AND rep_first_name ILIKE '%%{brand}%%' "
        "GROUP BY COALESCE(rep_first_name || ' ' || rep_last_name, CAST(org_user_id AS text)) "
        "ORDER BY gmv DESC"
    )
    pass2_rows = run_pg(pass2_sql, (ctx.org_id,))

    # Pass 1b — placeholder (requires LLM judgment for name classification)
    log.info("Pass 1b (non-person entity scan) requires agent review — skipping")

    # Merge and deduplicate
    all_flagged: dict[str, dict] = {}
    for row in pass1_rows + pass2_rows:
        name = row["rep_name"]
        if name not in all_flagged:
            all_flagged[name] = {
                "rep_name": name,
                "order_count": row["order_count"],
                "gmv": row["gmv"],
                "source": "keyword" if row in pass1_rows else "brand",
                "classification": "confirmed_operational",
            }

    ctx.gates.SHOWROOM_EXCLUSIONS = len(all_flagged)
    ctx.gates.evidence["SHOWROOM_EXCLUSIONS"] = f"{len(all_flagged)} accounts flagged"

    # Write showroom_scan_results.md
    lines = [
        f"# Showroom Scan Results — {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.run_date}",
        f"- **Total flagged**: {len(all_flagged)}",
        f"- **Aggregate GMV**: {fmt_dollar(sum(r['gmv'] for r in all_flagged.values()))}",
        "",
        "| Rep Name | Orders | GMV | Source | Classification |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in sorted(all_flagged.values(), key=lambda x: float(x["gmv"]), reverse=True):
        lines.append(f"| {r['rep_name']} | {r['order_count']} | {fmt_dollar(r['gmv'])} | {r['source']} | {r['classification']} |")
    lines.append("")
    lines.append("**Note**: Pass 1b (non-person entity scan) requires agent review — not executed.")

    (ctx.cache_dir / "showroom_scan_results.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote showroom_scan_results.md (%d flagged accounts)", len(all_flagged))


# ---------------------------------------------------------------------------
# Derived Gate Computation
# ---------------------------------------------------------------------------

def compute_vm45_gate(ctx: RunContext) -> None:
    """VM-45 denominator validity gate."""
    if not ctx.gates.HAS_PORTAL_ORDERS:
        ctx.gates.VM45_GATE_1 = "SKIP"
        ctx.gates.VM45_GATE_2 = "SKIP"
        ctx.gates.VM45_RENDER = False
        return

    if ctx.dry_run:
        return

    try:
        ecat_gmv_rows = run_pg(
            "SELECT COALESCE(SUM(total), 0) AS ecat_gmv FROM orders "
            "WHERE organization_id = %s AND is_submitted = true "
            "AND (is_marked_deleted = false OR is_marked_deleted IS NULL) "
            "AND created_at >= NOW() - INTERVAL '12 months'",
            (ctx.org_id,),
        )
        ecat_gmv = float(ecat_gmv_rows[0]["ecat_gmv"])

        erp_gmv_rows = run_pg(
            "SELECT COALESCE(SUM(total_amount), 0) AS erp_gmv FROM portal_orders "
            "WHERE organization_id = %s AND order_date >= NOW() - INTERVAL '12 months'",
            (ctx.org_id,),
        )
        erp_gmv = float(erp_gmv_rows[0]["erp_gmv"])

        gate1 = erp_gmv > ecat_gmv
        gate2 = ecat_gmv >= 0.05 * erp_gmv if erp_gmv > 0 else False

        ctx.gates.VM45_GATE_1 = "PASS" if gate1 else "FAIL"
        ctx.gates.VM45_GATE_2 = "PASS" if gate2 else "FAIL"
        ctx.gates.VM45_RENDER = gate1 and gate2

        ctx.gates.evidence["VM45_GATE_1"] = f"erp_gmv={fmt_dollar(erp_gmv)} > ecat_gmv={fmt_dollar(ecat_gmv)}: {gate1}"
        ctx.gates.evidence["VM45_GATE_2"] = f"ecat_gmv >= 5% of erp_gmv: {gate2}"
        ctx.gates.evidence["VM45_RENDER"] = f"Both gates {'pass' if ctx.gates.VM45_RENDER else 'fail'}"

        if not ctx.gates.VM45_RENDER:
            ctx.gates.validation_log.append(
                f"VM-45 skipped: Gate1={'PASS' if gate1 else 'FAIL'}, Gate2={'PASS' if gate2 else 'FAIL'}"
            )
    except Exception as exc:
        log.error("VM-45 gate computation failed: %s", exc)
        ctx.gates.VM45_RENDER = False


def compute_mixpanel_gap(ctx: RunContext) -> None:
    """Mixpanel order-tracking gap check (Derived Gate 4)."""
    q01_step1_path = ctx.cache_dir / "Q-01_step1_results.md"
    q22_path = ctx.cache_dir / "Q-22_results.md"

    postgres_orders = ctx.gates.ltm_ecat_orders
    mixpanel_submit = 0

    if ctx.gates.HAS_SALES_SECTION and q01_step1_path.exists():
        # Sum submit_order from Q-01 Step 1 results
        text = q01_step1_path.read_text(encoding="utf-8")
        mixpanel_submit = _sum_column_from_cache(text, "submit_order")
        ctx.gates.evidence["MIXPANEL_ORDER_TRACKING_GAP"] = (
            f"Postgres LTM orders: {postgres_orders}, Mixpanel total submit_order (Q-01): {mixpanel_submit}"
        )
    elif q22_path.exists():
        text = q22_path.read_text(encoding="utf-8")
        mixpanel_submit = _sum_column_from_cache(text, "submit_order")
        ctx.gates.evidence["MIXPANEL_ORDER_TRACKING_GAP"] = (
            f"Postgres LTM orders: {postgres_orders}, Mixpanel submit_order (Q-22): {mixpanel_submit}"
        )
    else:
        ctx.gates.evidence["MIXPANEL_ORDER_TRACKING_GAP"] = "No Mixpanel data available for check"
        return

    ctx.gates.MIXPANEL_ORDER_TRACKING_GAP = postgres_orders > 0 and mixpanel_submit == 0


def _sum_column_from_cache(text: str, col_name: str) -> int:
    """Sum integer values from a specific column in a markdown table cache file."""
    lines = text.splitlines()
    header_idx = None
    col_idx = None

    for i, line in enumerate(lines):
        if line.startswith("|") and col_name in line and "---" not in line:
            cols = [c.strip() for c in line.split("|")]
            try:
                col_idx = cols.index(col_name)
                header_idx = i
                break
            except ValueError:
                continue

    if header_idx is None or col_idx is None:
        return 0

    total = 0
    for line in lines[header_idx + 2:]:  # skip separator
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.split("|")]
        if col_idx < len(cells):
            try:
                val = cells[col_idx].replace(",", "").replace("—", "0")
                total += int(float(val))
            except (ValueError, IndexError):
                pass
    return total


def compute_mixpanel_user_data(ctx: RunContext) -> None:
    """Derived Gate 3 — Mixpanel user data check."""
    q01_step1_path = ctx.cache_dir / "Q-01_step1_results.md"
    if q01_step1_path.exists():
        text = q01_step1_path.read_text(encoding="utf-8")
        row_match = re.search(r"Row count\*?\*?:\s*(\d+)", text)
        count = int(row_match.group(1)) if row_match else 0
        ctx.gates.MIXPANEL_USER_DATA_PRESENT = count > 0
        ctx.gates.evidence["MIXPANEL_USER_DATA_PRESENT"] = f"Q-01 Step 1 returned {count} rows"
    else:
        ctx.gates.MIXPANEL_USER_DATA_PRESENT = False
        ctx.gates.evidence["MIXPANEL_USER_DATA_PRESENT"] = "Q-01 Step 1 not executed"


def compute_staleness_flags(ctx: RunContext) -> None:
    """Derived Gate §1.3b — data staleness from Q-08 results."""
    q08_path = ctx.cache_dir / "Q-08_results.md"
    if not q08_path.exists():
        ctx.gates.evidence["INVENTORY_FRESH"] = "Q-08 not available"
        ctx.gates.evidence["SALES_DATA_FRESH"] = "Q-08 not available"
        ctx.gates.evidence["CUSTOMER_DATA_FRESH"] = "Q-08 not available"
        return

    text = q08_path.read_text(encoding="utf-8")
    entity_freshness: dict[str, int] = {}

    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "entity_type" in line:
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) >= 5:
            entity = cells[1].strip().lower()
            try:
                days = int(cells[3].replace(",", "").strip())
                entity_freshness[entity] = days
            except (ValueError, IndexError):
                pass

    for entity, flag_attr, threshold in [
        ("inventories", "INVENTORY_FRESH", 30),
        ("sales_data", "SALES_DATA_FRESH", 30),
        ("customers", "CUSTOMER_DATA_FRESH", 30),
    ]:
        days = entity_freshness.get(entity)
        if days is not None:
            setattr(ctx.gates, flag_attr, days <= threshold)
            ctx.gates.evidence[flag_attr] = f"{entity} last_updated {days}d ago (threshold: <={threshold}d)"
        else:
            setattr(ctx.gates, flag_attr, False)
            ctx.gates.evidence[flag_attr] = f"{entity} not found in Q-08 data_versions"


def compute_confidence_tiers(ctx: RunContext) -> None:
    """Derived Gate 6 — section confidence tiers."""
    g = ctx.gates

    # §2 Sales Team
    if not g.HAS_SALES_SECTION:
        g.SECTION_CONFIDENCE_2 = ""
    elif g.MIXPANEL_USER_DATA_PRESENT and g.PORTAL_REP_DATA_PRESENT and g.PORTAL_ORDERS_FRESH:
        g.SECTION_CONFIDENCE_2 = "FULL"
    elif g.MIXPANEL_USER_DATA_PRESENT and (not g.PORTAL_REP_DATA_PRESENT or not g.PORTAL_ORDERS_FRESH):
        g.SECTION_CONFIDENCE_2 = "STRONG"
    elif not g.MIXPANEL_USER_DATA_PRESENT:
        g.SECTION_CONFIDENCE_2 = "PARTIAL"
    else:
        g.SECTION_CONFIDENCE_2 = "PARTIAL"

    # §3 Customer — check LIMITED first
    q08_path = ctx.cache_dir / "Q-08_results.md"
    customer_entity_days = _get_entity_days(q08_path, "customers")
    if g.ltm_ecat_orders > 0 and not g.CUSTOMER_DATA_FRESH and customer_entity_days is not None and customer_entity_days > 180:
        g.SECTION_CONFIDENCE_3 = "LIMITED"
    elif g.ltm_ecat_orders > 0 and g.PORTAL_CUSTOMER_DATA_PRESENT and g.PORTAL_ORDERS_FRESH and g.CUSTOMER_DATA_FRESH:
        g.SECTION_CONFIDENCE_3 = "FULL"
    elif g.ltm_ecat_orders > 0 and g.PORTAL_CUSTOMER_DATA_PRESENT and (not g.PORTAL_ORDERS_FRESH or not g.CUSTOMER_DATA_FRESH):
        g.SECTION_CONFIDENCE_3 = "STRONG"
    elif g.ltm_ecat_orders > 0 and not g.PORTAL_CUSTOMER_DATA_PRESENT:
        g.SECTION_CONFIDENCE_3 = "PARTIAL"
    else:
        g.SECTION_CONFIDENCE_3 = "PARTIAL"

    # §4 Product — check LIMITED first
    inv_days = _get_entity_days(q08_path, "inventories")
    sd_days = _get_entity_days(q08_path, "sales_data")
    limited_4 = False
    if g.HAS_INVENTORY and inv_days is not None and inv_days > 180:
        limited_4 = True
    if g.HAS_SALES_DATA and sd_days is not None and sd_days > 180:
        limited_4 = True

    if limited_4:
        g.SECTION_CONFIDENCE_4 = "LIMITED"
    elif g.HAS_INVENTORY and g.HAS_SALES_DATA and g.INVENTORY_FRESH and g.SALES_DATA_FRESH:
        g.SECTION_CONFIDENCE_4 = "FULL"
    elif (g.HAS_INVENTORY or g.HAS_SALES_DATA) and not limited_4:
        g.SECTION_CONFIDENCE_4 = "STRONG"
    else:
        g.SECTION_CONFIDENCE_4 = "PARTIAL"

    # §5 Commerce
    if g.ltm_ecat_orders > 0 and g.HAS_PORTAL_ORDERS and g.PORTAL_ORDERS_FRESH and g.PORTAL_CUSTOMER_DATA_PRESENT:
        g.SECTION_CONFIDENCE_5 = "FULL"
    elif g.ltm_ecat_orders > 0 and g.HAS_PORTAL_ORDERS and (not g.PORTAL_ORDERS_FRESH or not g.PORTAL_CUSTOMER_DATA_PRESENT):
        g.SECTION_CONFIDENCE_5 = "STRONG"
    elif g.ltm_ecat_orders > 0 and not g.HAS_PORTAL_ORDERS:
        g.SECTION_CONFIDENCE_5 = "PARTIAL"
    else:
        g.SECTION_CONFIDENCE_5 = "PARTIAL"


def _get_entity_days(q08_path: Path, entity: str) -> int | None:
    """Extract days_since_update for a given entity from Q-08 cache."""
    if not q08_path.exists():
        return None
    text = q08_path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "entity_type" in line:
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) >= 5 and entity in cells[1].lower():
            try:
                return int(cells[3].replace(",", "").strip())
            except (ValueError, IndexError):
                return None
    return None


def run_user_group_mapping(ctx: RunContext) -> None:
    """Derived Gate 5 — user group mapping and admin-in-leaderboard cross-reference."""
    if not ctx.gates.HAS_SALES_SECTION or ctx.dry_run:
        ctx.gates.USER_GROUP_SPLIT_AVAILABLE = False
        return

    log.info("Building user group mapping...")
    try:
        mapping_rows = run_pg(
            "SELECT u.username, u.first_name, u.last_name, "
            "ut.name AS user_group, ut.show_mode, ut.primary_rep_group, ou.is_admin "
            "FROM org_users ou "
            "JOIN users u ON u.id = ou.user_id "
            "JOIN user_types ut ON ut.id = ou.user_type_id "
            "WHERE ou.organization_id = %s ORDER BY ut.name, u.username",
            (ctx.org_id,),
        )
    except Exception as exc:
        log.error("User group mapping query failed: %s", exc)
        ctx.gates.USER_GROUP_SPLIT_AVAILABLE = False
        return

    if not mapping_rows:
        ctx.gates.USER_GROUP_SPLIT_AVAILABLE = False
        return

    def classify_bucket(row: dict) -> str:
        group_name = (row.get("user_group") or "").lower()
        is_admin = bool(row.get("is_admin"))
        primary_rep = bool(row.get("primary_rep_group"))

        is_showroom = "showroom" in group_name
        is_admin_internal = (
            is_admin
            or any(kw in group_name for kw in [
                "admin", "supercat", "internal", "customer service",
                "it staff", "ecat online", "public site", "marketing",
                "order entry", "product development",
            ])
        )
        is_field = (
            primary_rep
            or any(kw in group_name for kw in [
                "sales rep", "reps", "account executive", "rep ",
            ])
            or ("sales" in group_name and "showroom" not in group_name)
        )

        if is_showroom:
            return "showroom"
        if is_admin_internal:
            return "admin_internal"
        if is_field:
            return "field_rep"
        return "other"

    for row in mapping_rows:
        row["bucket"] = classify_bucket(row)

    # Read Q-01 Step 1 to compute join rate
    q01_path = ctx.cache_dir / "Q-01_step1_results.md"
    mixpanel_usernames: set[str] = set()
    mixpanel_events: dict[str, int] = {}
    if q01_path.exists():
        text = q01_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not line.startswith("|") or "---" in line or "username" in line.lower():
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 4:
                uname = cells[1].strip()
                if uname:
                    mixpanel_usernames.add(uname.lower())
                    try:
                        mixpanel_events[uname.lower()] = int(cells[3].replace(",", "").strip())
                    except (ValueError, IndexError):
                        pass

    pg_user_lookup: dict[str, dict] = {}
    for row in mapping_rows:
        uname = (row.get("username") or "").lower()
        if uname:
            pg_user_lookup[uname] = row

    matched_count = sum(1 for u in mixpanel_usernames if u in pg_user_lookup)
    total_mp_users = len(mixpanel_usernames)
    join_rate = matched_count / total_mp_users if total_mp_users > 0 else 0

    ambiguous_count = sum(1 for u in mixpanel_usernames if u in pg_user_lookup and pg_user_lookup[u]["bucket"] == "other")
    ambiguous_rate = ambiguous_count / matched_count if matched_count > 0 else 0

    showroom_events = sum(
        mixpanel_events.get(u, 0) for u in mixpanel_usernames
        if u in pg_user_lookup and pg_user_lookup[u]["bucket"] in ("showroom", "admin_internal")
    )
    total_matched_events = sum(mixpanel_events.get(u, 0) for u in mixpanel_usernames if u in pg_user_lookup)
    showroom_event_share = showroom_events / total_matched_events if total_matched_events > 0 else 0

    ctx.gates.USER_GROUP_JOIN_RATE = f"{join_rate:.0%}"
    ctx.gates.USER_GROUP_SHOWROOM_EVENT_SHARE = f"{showroom_event_share:.0%}"
    ctx.gates.USER_GROUP_SPLIT_AVAILABLE = (
        join_rate >= 0.90 and ambiguous_rate == 0 and showroom_event_share >= 0.10
    )

    ctx.gates.evidence["USER_GROUP_SPLIT_AVAILABLE"] = (
        f"join_rate={join_rate:.1%}, ambiguous_rate={ambiguous_rate:.1%}, "
        f"showroom_event_share={showroom_event_share:.1%}"
    )
    ctx.gates.evidence["USER_GROUP_JOIN_RATE"] = f"{matched_count} of {total_mp_users} Mixpanel users matched"
    ctx.gates.evidence["USER_GROUP_SHOWROOM_EVENT_SHARE"] = f"showroom+admin share of matched events: {showroom_event_share:.1%}"

    # Admin-in-leaderboard cross-reference
    q01_s2_path = ctx.cache_dir / "Q-01_step2_results.md"
    if q01_s2_path.exists():
        s2_text = q01_s2_path.read_text(encoding="utf-8")
        leaderboard_names: set[str] = set()
        for line in s2_text.splitlines():
            if not line.startswith("|") or "---" in line or "rep_name" in line.lower():
                continue
            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 2:
                leaderboard_names.add(cells[1].strip().lower())

        admin_in_lb = []
        for row in mapping_rows:
            if row["bucket"] in ("admin_internal", "showroom"):
                full_name = f"{row.get('first_name', '')} {row.get('last_name', '')}".strip().lower()
                if full_name in leaderboard_names:
                    admin_in_lb.append(f"{row.get('first_name', '')} {row.get('last_name', '')}".strip())

        ctx.gates.ADMIN_REPS_IN_LEADERBOARD = len(admin_in_lb) > 0
        ctx.gates.evidence["ADMIN_REPS_IN_LEADERBOARD"] = (
            f"{len(admin_in_lb)} admin/showroom users in leaderboard" +
            (f": {', '.join(admin_in_lb[:5])}" if admin_in_lb else "")
        )

    # Write user_group_mapping.md
    group_counts: dict[str, dict[str, int]] = {}
    for row in mapping_rows:
        group = row.get("user_group", "Unknown")
        bucket = row["bucket"]
        key = f"{group}|{bucket}"
        if key not in group_counts:
            group_counts[key] = {"group": group, "bucket": bucket, "count": 0}
        group_counts[key]["count"] += 1

    confidence = "HIGH" if ctx.gates.USER_GROUP_SPLIT_AVAILABLE else "LOW"
    lines = [
        f"# User Group Mapping — {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.run_date}",
        f"- **Total Postgres users**: {len(mapping_rows)}",
        f"- **Matched to Mixpanel (Q-01 Step 1)**: {matched_count} of {total_mp_users} ({join_rate:.0%})",
        f"- **Classification confidence**: {confidence}",
        f"- **Split available**: {ctx.gates.USER_GROUP_SPLIT_AVAILABLE}",
        "",
        "## Group Classification",
        "",
        "| User Group (Admin Console) | Bucket | User Count |",
        "| --- | --- | --- |",
    ]
    for gc in sorted(group_counts.values(), key=lambda x: x["count"], reverse=True):
        lines.append(f"| {gc['group']} | {gc['bucket']} | {gc['count']} |")

    bucket_agg: dict[str, dict[str, int]] = {}
    for u in mixpanel_usernames:
        if u in pg_user_lookup:
            b = pg_user_lookup[u]["bucket"]
            if b not in bucket_agg:
                bucket_agg[b] = {"users": 0, "events": 0}
            bucket_agg[b]["users"] += 1
            bucket_agg[b]["events"] += mixpanel_events.get(u, 0)

    lines.extend([
        "",
        "## Aggregate Split",
        "",
        "| Bucket | Users | Total Events | Event Share |",
        "| --- | --- | --- | --- |",
    ])
    for b in ["field_rep", "showroom", "admin_internal", "other"]:
        if b in bucket_agg:
            share = bucket_agg[b]["events"] / total_matched_events * 100 if total_matched_events > 0 else 0
            lines.append(f"| {b} | {bucket_agg[b]['users']} | {bucket_agg[b]['events']:,} | {share:.1f}% |")

    (ctx.cache_dir / "user_group_mapping.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote user_group_mapping.md")


# ---------------------------------------------------------------------------
# Output Writers
# ---------------------------------------------------------------------------

def write_gate_flags(ctx: RunContext) -> None:
    """Write cache/gate_flags.md."""
    g = ctx.gates
    lines = [
        f"# Gate Flags — {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.run_date}",
        f"- **Report mode**: {g.mode_label}",
        "",
        "## Primary Gates",
        "",
        "| Flag | Value | Evidence |",
        "| --- | --- | --- |",
    ]

    primary_flags = [
        ("HAS_CLICKY", g.HAS_CLICKY),
        ("HAS_CART", g.HAS_CART),
        ("HAS_PORTAL_ORDERS", g.HAS_PORTAL_ORDERS),
        ("HAS_INVENTORY", g.HAS_INVENTORY),
        ("HAS_SALES_DATA", g.HAS_SALES_DATA),
        ("HAS_SALES_SECTION", g.HAS_SALES_SECTION),
        ("HAS_PEER_DATA", g.HAS_PEER_DATA),
        ("BENCHMARK_ELIGIBLE", g.BENCHMARK_ELIGIBLE),
        ("BENCHMARK_CONFIDENCE", g.BENCHMARK_CONFIDENCE or "N/A"),
        ("PEER_GROUP_LEVEL", g.PEER_GROUP_LEVEL or "N/A"),
        ("PEER_GROUP_N", g.PEER_GROUP_N),
        ("PEER_GROUP_ID_EFFECTIVE", g.PEER_GROUP_ID_EFFECTIVE or "N/A"),
        ("CLICKY_PREFIX", g.CLICKY_PREFIX or "N/A"),
    ]
    for name, val in primary_flags:
        ev = g.evidence.get(name, "")
        lines.append(f"| {name} | {val} | {ev} |")

    lines.extend([
        "",
        "## Derived Gates",
        "",
        "| Flag | Value | Evidence |",
        "| --- | --- | --- |",
    ])
    derived_flags = [
        ("VM45_GATE_1", g.VM45_GATE_1),
        ("VM45_GATE_2", g.VM45_GATE_2),
        ("VM45_RENDER", g.VM45_RENDER),
        ("QUALIFYING_REP_COUNT", g.QUALIFYING_REP_COUNT),
        ("MIXPANEL_USER_DATA_PRESENT", g.MIXPANEL_USER_DATA_PRESENT),
        ("SHOWROOM_EXCLUSIONS", g.SHOWROOM_EXCLUSIONS),
        ("MIXPANEL_ORDER_TRACKING_GAP", g.MIXPANEL_ORDER_TRACKING_GAP),
        ("USER_GROUP_SPLIT_AVAILABLE", g.USER_GROUP_SPLIT_AVAILABLE),
        ("USER_GROUP_JOIN_RATE", g.USER_GROUP_JOIN_RATE),
        ("USER_GROUP_SHOWROOM_EVENT_SHARE", g.USER_GROUP_SHOWROOM_EVENT_SHARE),
        ("ADMIN_REPS_IN_LEADERBOARD", g.ADMIN_REPS_IN_LEADERBOARD),
    ]
    for name, val in derived_flags:
        ev = g.evidence.get(name, "")
        lines.append(f"| {name} | {val} | {ev} |")

    lines.extend([
        "",
        "## ERP Enrichment Gates",
        "",
        "| Flag | Value | Evidence |",
        "| --- | --- | --- |",
    ])
    erp_flags = [
        ("PORTAL_ORDERS_FRESH", g.PORTAL_ORDERS_FRESH),
        ("PORTAL_REP_DATA_PRESENT", g.PORTAL_REP_DATA_PRESENT),
        ("PORTAL_CUSTOMER_DATA_PRESENT", g.PORTAL_CUSTOMER_DATA_PRESENT),
        ("INVENTORY_FRESH", g.INVENTORY_FRESH),
        ("SALES_DATA_FRESH", g.SALES_DATA_FRESH),
        ("CUSTOMER_DATA_FRESH", g.CUSTOMER_DATA_FRESH),
        ("HAS_COMMITMENT_DATA", g.HAS_COMMITMENT_DATA),
        ("HAS_NEW_ITEMS", g.HAS_NEW_ITEMS),
        ("HAS_BUYER_DATA", g.HAS_BUYER_DATA),
    ]
    for name, val in erp_flags:
        ev = g.evidence.get(name, "")
        lines.append(f"| {name} | {val} | {ev} |")

    lines.extend([
        "",
        "## Confidence Tiers",
        "",
        "| Flag | Value | Formula Inputs |",
        "| --- | --- | --- |",
    ])
    for section_num, tier_val in [
        (2, g.SECTION_CONFIDENCE_2 or "—"),
        (3, g.SECTION_CONFIDENCE_3),
        (4, g.SECTION_CONFIDENCE_4),
        (5, g.SECTION_CONFIDENCE_5),
    ]:
        lines.append(f"| SECTION_CONFIDENCE_{section_num} | {tier_val} | See Derived Gate 6 §{section_num} formula |")

    lines.extend([
        "",
        "## Org Identity",
        "",
        f"- **Client name**: {ctx.client_name}",
        f"- **Shortname**: {ctx.shortname}",
        f"- **Org ID**: {ctx.org_id}",
        f"- **Bundle**: {ctx.bundle_label}",
        f"- **Bundle label for report**: {ctx.bundle_label}",
        "",
        "## Validation Log",
        "",
    ])
    for entry in g.validation_log:
        lines.append(f"- {entry}")
    if not g.validation_log:
        lines.append("- (none)")

    (ctx.cache_dir / "gate_flags.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote gate_flags.md")


def write_section_manifest(ctx: RunContext) -> None:
    """Write cache/section_manifest.md."""
    g = ctx.gates
    has_product = g.HAS_INVENTORY or g.HAS_SALES_DATA

    sections = [
        ("1", "Executive Summary", "STAGE 4", "Always (written last)", "stage4_assembly.md"),
        ("2", "Sales Team Performance", "INCLUDE" if g.HAS_SALES_SECTION else "SKIP", "HAS_SALES_SECTION", "section_02_sales_team.md"),
        ("3", "Customer & Buyer Intelligence", "INCLUDE", "Always", "section_03_customers.md"),
        ("4", "Product & Inventory Intelligence", "INCLUDE" if has_product else "SKIP", "HAS_INVENTORY OR HAS_SALES_DATA", "section_04_product.md"),
        ("5", "Commerce Analytics", "INCLUDE", "Always", "section_05_commerce.md"),
        ("6", "Demand Signal Intelligence", "INCLUDE" if g.HAS_CLICKY else "SKIP", "HAS_CLICKY", "section_06_portal.md"),
        ("7", "Peer Benchmarking", "SKIP", "Disabled", "section_07_peer.md"),
        ("8", "Platform & Feature Utilization", "INCLUDE", "Always", "section_08_platform.md"),
        ("9", "Appendix", "STAGE 4", "Always", "stage4_assembly.md"),
    ]

    lines = [
        f"# Section Manifest — {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.run_date}",
        f"- **Report mode**: {g.mode_label}",
        "",
        "| § | Section | Status | Gate | Agent File |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in sections:
        lines.append(f"| {s[0]} | {s[1]} | {s[2]} | {s[3]} | {s[4]} |")

    (ctx.cache_dir / "section_manifest.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote section_manifest.md")


def write_section_confidence(ctx: RunContext) -> None:
    """Write cache/section_confidence.md."""
    g = ctx.gates
    lines = [
        f"# Section Confidence Tiers — {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})",
        f"- **Run date**: {ctx.run_date}",
        "",
        "## Input Flags",
        "",
        "| Flag | Value |",
        "| --- | --- |",
    ]
    input_flags = [
        ("HAS_SALES_SECTION", g.HAS_SALES_SECTION),
        ("MIXPANEL_USER_DATA_PRESENT", g.MIXPANEL_USER_DATA_PRESENT),
        ("PORTAL_REP_DATA_PRESENT", g.PORTAL_REP_DATA_PRESENT),
        ("PORTAL_CUSTOMER_DATA_PRESENT", g.PORTAL_CUSTOMER_DATA_PRESENT),
        ("PORTAL_ORDERS_FRESH", g.PORTAL_ORDERS_FRESH),
        ("HAS_PORTAL_ORDERS", g.HAS_PORTAL_ORDERS),
        ("HAS_INVENTORY", g.HAS_INVENTORY),
        ("HAS_SALES_DATA", g.HAS_SALES_DATA),
        ("INVENTORY_FRESH", g.INVENTORY_FRESH),
        ("SALES_DATA_FRESH", g.SALES_DATA_FRESH),
        ("CUSTOMER_DATA_FRESH", g.CUSTOMER_DATA_FRESH),
    ]
    for name, val in input_flags:
        lines.append(f"| {name} | {val} |")

    lines.extend([
        "",
        "## Computed Tiers",
        "",
        "| Section | Tier | Determining Condition |",
        "| --- | --- | --- |",
    ])
    for section_name, section_num, tier in [
        ("§2 Sales Team", 2, g.SECTION_CONFIDENCE_2 or "—"),
        ("§3 Customer", 3, g.SECTION_CONFIDENCE_3),
        ("§4 Product", 4, g.SECTION_CONFIDENCE_4),
        ("§5 Commerce", 5, g.SECTION_CONFIDENCE_5),
    ]:
        lines.append(f"| {section_name} | {tier} | See Derived Gate 6 §{section_num} formula |")

    (ctx.cache_dir / "section_confidence.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote section_confidence.md")


def write_run_status(ctx: RunContext) -> None:
    """Write cache/_run_status.md."""
    status = "COMPLETE" if not ctx.failed_queries else f"PARTIAL — outstanding: {', '.join(f['q_id'] for f in ctx.failed_queries)}"
    lines = [
        f"# Run Status — {ctx.client_name} ({ctx.shortname})",
        f"- **Run date**: {ctx.run_date}",
        f"- **Status**: {status}",
        f"- **Completed queries**: {len(ctx.completed_queries)}",
        f"- **Failed queries**: {len(ctx.failed_queries)}",
        "",
    ]
    if ctx.failed_queries:
        lines.extend([
            "## Failed Queries",
            "",
            "| Q-ID | Reason | Retry Attempted |",
            "| --- | --- | --- |",
        ])
        for f in ctx.failed_queries:
            lines.append(f"| {f['q_id']} | {f['reason']} | {f['retry']} |")

    (ctx.cache_dir / "_run_status.md").write_text("\n".join(lines), encoding="utf-8")
    log.info("Wrote _run_status.md")


# ---------------------------------------------------------------------------
# Mode 2/3 minimal output
# ---------------------------------------------------------------------------

def handle_non_standard_mode(ctx: RunContext) -> None:
    """For Mode 2/3, write minimal gate_flags and exit."""
    write_gate_flags(ctx)

    # Write minimal _run_status.md
    (ctx.cache_dir / "_run_status.md").write_text(
        f"# Run Status — {ctx.client_name} ({ctx.shortname})\n"
        f"- **Run date**: {ctx.run_date}\n"
        f"- **Status**: COMPLETE\n"
        f"- **Report mode**: {ctx.gates.mode_label}\n"
        f"- **Note**: Stages 1-4 of standard pipeline do not apply to this mode.\n",
        encoding="utf-8",
    )

    print(f"\n{'='*60}")
    print(f"  {ctx.gates.mode_label}")
    print(f"  Org: {ctx.client_name} ({ctx.shortname}, org_id={ctx.org_id})")
    print(f"  All-time eCat orders: {ctx.gates.alltime_ecat_orders}")
    if ctx.gates.last_ecat_order_date:
        print(f"  Last eCat order: {ctx.gates.last_ecat_order_date}")
    print(f"  Gate flags written to: {ctx.cache_dir / 'gate_flags.md'}")
    print(f"{'='*60}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Insightful Product 2.0 — Stage 1 Data Gatherer",
    )
    parser.add_argument("--shortname", required=True, help="Org shortname (e.g. 'pf')")
    parser.add_argument("--org-id", required=True, type=int, help="Organization ID (integer)")
    parser.add_argument("--run-date", required=True, help="Report run date (YYYY-MM-DD)")
    parser.add_argument("--period-start", help="LTM period start (default: 12 months before run-date)")
    parser.add_argument("--period-end", help="LTM period end (default: run-date)")
    parser.add_argument("--client-name", default="", help="Client display name (default: looked up from org)")
    parser.add_argument("--bundle-label", default="", help="Bundle label (default: from org_summary)")
    parser.add_argument("--dry-run", action="store_true", help="Print query plan without executing")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    run_dt = date.fromisoformat(args.run_date)
    period_end = date.fromisoformat(args.period_end) if args.period_end else run_dt
    period_start = date.fromisoformat(args.period_start) if args.period_start else run_dt - timedelta(days=365)

    # Parse query library
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    ql_path = project_root / "authority" / "query_library.md"
    if not ql_path.exists():
        log.error("Query library not found at %s", ql_path)
        sys.exit(1)

    log.info("Parsing query library...")
    query_lib = parse_query_library(ql_path)
    log.info("Loaded %d SQL blocks from query library", len(query_lib))

    cache_dir = project_root / "runs" / f"{args.shortname}_{args.run_date}" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    # Start persistent MCP session (skip for dry-run — no DB calls)
    global _pg_manager
    if not args.dry_run:
        _pg_manager = McpSessionManager(MCP_PG_URL)
        _pg_manager.start()

    try:
        _run(args, run_dt, period_start, period_end, cache_dir, query_lib)
    finally:
        if _pg_manager is not None:
            _pg_manager.close()


def _run(
    args: argparse.Namespace,
    run_dt: date,
    period_start: date,
    period_end: date,
    cache_dir: Path,
    query_lib: dict[str, str],
) -> None:
    """Core execution body — separated so main() can wrap with session lifecycle."""
    # Verify org_id matches shortname before proceeding
    if not args.dry_run:
        log.info("Verifying org_id=%d matches shortname=%s ...", args.org_id, args.shortname)
        try:
            _verify_rows = run_pg(
                "SELECT id, shortname, name FROM organizations WHERE shortname = %s LIMIT 1",
                (args.shortname,),
            )
            if _verify_rows:
                db_id = _verify_rows[0]["id"]
                db_name = _verify_rows[0]["name"]
                if db_id != args.org_id:
                    log.warning(
                        "ORG_ID MISMATCH: --org-id %d but DB says shortname '%s' → id=%d (%s). Using DB id=%d.",
                        args.org_id, args.shortname, db_id, db_name, db_id,
                    )
                    args.org_id = db_id
                else:
                    log.info("Verified: shortname=%s → org_id=%d (%s)", args.shortname, db_id, db_name)
                if not args.client_name:
                    args.client_name = db_name
            else:
                log.warning("No organization found with shortname='%s' — proceeding with --org-id %d", args.shortname, args.org_id)
        except Exception as exc:
            log.warning("Org verification query failed: %s — proceeding with --org-id %d", exc, args.org_id)

    ctx = RunContext(
        shortname=args.shortname,
        org_id=args.org_id,
        run_date=run_dt,
        period_start=period_start,
        period_end=period_end,
        client_name=args.client_name,
        bundle_label=args.bundle_label,
        cache_dir=cache_dir,
        dry_run=args.dry_run,
        query_lib=query_lib,
    )

    start_time = time.monotonic()

    try:
        if not ctx.dry_run:
            run_stage0(ctx)
        else:
            log.info("[DRY-RUN] Skipping Stage 0 (requires DB connection)")
            ctx.gates.report_mode = 1

        if ctx.gates.report_mode != 1:
            handle_non_standard_mode(ctx)
            return

        if not ctx.dry_run:
            run_preflight(ctx)
        else:
            log.info("[DRY-RUN] Skipping preflight (requires DB connection)")

        # Build and execute query plan
        log.info("=== Building query plan ===")
        batches = build_query_plan(ctx)
        total_queries = sum(len(b) for b in batches)
        log.info("Query plan: %d batches, %d total queries", len(batches), total_queries)

        if ctx.dry_run:
            for i, batch in enumerate(batches, 1):
                print(f"\nBatch {i}:")
                for spec in batch:
                    print(f"  {spec['q_id']:15s} {spec['source']:10s} {spec['description']}")
            print(f"\nTotal: {total_queries} queries across {len(batches)} batches")
            return

        log.info("=== Executing queries ===")
        execute_batches(ctx, batches)

        # Derived gates (order matters)
        log.info("=== Computing derived gates ===")
        compute_vm45_gate(ctx)
        run_showroom_scan(ctx)
        compute_mixpanel_user_data(ctx)
        compute_mixpanel_gap(ctx)
        compute_staleness_flags(ctx)
        run_user_group_mapping(ctx)
        compute_confidence_tiers(ctx)

        # Write output files
        log.info("=== Writing output files ===")
        write_gate_flags(ctx)
        write_section_manifest(ctx)
        write_section_confidence(ctx)
        write_run_status(ctx)

        elapsed = time.monotonic() - start_time

        # Print summary
        print(f"\n{'='*60}")
        print(f"  Stage 1 Complete — {ctx.client_name} ({ctx.shortname})")
        print(f"{'='*60}")
        print(f"  Mode:       {ctx.gates.mode_label}")
        print(f"  Org ID:     {ctx.org_id}")
        print(f"  Period:     {ctx.period_start} to {ctx.period_end}")
        print(f"  Cache dir:  {ctx.cache_dir}")
        print(f"  Elapsed:    {elapsed:.1f}s")
        print(f"  Completed:  {len(ctx.completed_queries)} queries")
        if ctx.failed_queries:
            print(f"  Failed:     {len(ctx.failed_queries)} queries")
            for f in ctx.failed_queries:
                print(f"    - {f['q_id']}: {f['reason'][:80]}")
        print()
        print("  Gate Summary:")
        print(f"    HAS_SALES_SECTION:     {ctx.gates.HAS_SALES_SECTION}")
        print(f"    HAS_PORTAL_ORDERS:     {ctx.gates.HAS_PORTAL_ORDERS}")
        print(f"    HAS_INVENTORY:         {ctx.gates.HAS_INVENTORY}")
        print(f"    HAS_SALES_DATA:        {ctx.gates.HAS_SALES_DATA}")
        print(f"    HAS_CLICKY:            {ctx.gates.HAS_CLICKY}")
        print(f"    HAS_PEER_DATA:         {ctx.gates.HAS_PEER_DATA}")
        print(f"    VM45_RENDER:           {ctx.gates.VM45_RENDER}")
        print(f"    MIXPANEL_USER_DATA:    {ctx.gates.MIXPANEL_USER_DATA_PRESENT}")
        print(f"    MIXPANEL_ORDER_GAP:    {ctx.gates.MIXPANEL_ORDER_TRACKING_GAP}")
        print(f"    USER_GROUP_SPLIT:      {ctx.gates.USER_GROUP_SPLIT_AVAILABLE}")
        print()
        print("  Confidence Tiers:")
        for s, t in [
            ("§2 Sales", ctx.gates.SECTION_CONFIDENCE_2 or "—"),
            ("§3 Customer", ctx.gates.SECTION_CONFIDENCE_3),
            ("§4 Product", ctx.gates.SECTION_CONFIDENCE_4),
            ("§5 Commerce", ctx.gates.SECTION_CONFIDENCE_5),
        ]:
            print(f"    {s:15s} {t}")
        print(f"{'='*60}")

    except KeyboardInterrupt:
        log.warning("Interrupted by user — writing partial status")
        ctx.gates.validation_log.append("Run interrupted by user (KeyboardInterrupt)")
        write_run_status(ctx)
        sys.exit(130)
    except Exception as exc:
        log.error("Fatal error: %s", exc, exc_info=True)
        ctx.failed_queries.append({"q_id": "FATAL", "reason": str(exc)[:200], "retry": "n"})
        write_run_status(ctx)
        sys.exit(1)


if __name__ == "__main__":
    main()
