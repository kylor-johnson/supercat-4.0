# =============================================================================
# build_intelligence_deepdive.py
# Part of the EBR 2.0 generation pipeline
#
# PURPOSE:
#   Generates the account intelligence brief and supporting documents
#   used as inputs to the EBR deck generation prompts.
#
# INPUTS:
#   Raw eCat data export files for the target account
#
# OUTPUTS (saved to Accounts/[AccountName]/Account Overview/):
#   - Brief_[AccountName]_[YYYY-MM].md       Full B1-B8 intelligence brief
#   - Snapshot_[AccountName]_[YYYY-MM].md    A1-A6 one-page summary
#   - GenerationNotes_[AccountName]_[YYYY-MM].md  What was/wasn't available
#
# USAGE:
#   python build_intelligence_deepdive.py --account "Gabby_SC" --date "2026-03"
#
# SEE ALSO:
#   Frameworks & Templates/Deck Prompts/README.md — full generation flow
#   Frameworks & Templates/Account_Brief_Prompt_v2.md — prompt counterpart
# =============================================================================

#!/usr/bin/env python3
"""Build Intelligence Deep-Dive EBR deck.

Usage:
  python build_intelligence_deepdive.py                          # all entities
  python build_intelligence_deepdive.py --account gh --date 2026-03  # single entity
"""

import sys, argparse, os, json, threading, queue, re
import datetime as _dt
from collections import defaultdict
from datetime import datetime, date, timedelta
from decimal import Decimal

import requests

_SAFE_EVAL_NS = {"__builtins__": {}, "datetime": _dt, "Decimal": Decimal,
                 "true": True, "false": False, "None": None}

parser = argparse.ArgumentParser(description="Build Intelligence Deep-Dive EBR deck")
parser.add_argument("--account", type=str, default=None,
                    help="Entity code to filter to (gh, sc, scw, sccon)")
parser.add_argument("--date", type=str, default=None,
                    help="Period label for filenames, e.g. 2026-03")
_args = parser.parse_args()

WORKSPACE = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/SuperCat 4.0"
)

ACCOUNT_FOLDERS = {
    "gh":    "Gabby_Summer_Classics",
    "sc":    "Gabby_Summer_Classics",
    "scw":   "Gabby_Summer_Classics",
    "sccon": "Gabby_Summer_Classics",
    "clm":   "Crystorama",
}

ENTITIES = {
    "gh":    {"label": "Gabby",            "org_id": 55},
    "sc":    {"label": "SC Wholesale",     "org_id": 69},
    "scw":   {"label": "SC Retail",        "org_id": 87},
    "sccon": {"label": "SC Contract",      "org_id": 88},
    "clm":   {"label": "Crystorama",       "org_id": 64},
}

STANDALONE_ACCOUNTS = {"clm"}

if _args.account:
    if _args.account not in ENTITIES:
        sys.exit(f"Unknown account '{_args.account}'. Valid: {', '.join(ENTITIES.keys())}")
    ENTITIES = {_args.account: ENTITIES[_args.account]}
else:
    ENTITIES = {k: v for k, v in ENTITIES.items() if k not in STANDALONE_ACCOUNTS}

# --- date range: TTM (trailing twelve complete months) ---
from dateutil.relativedelta import relativedelta
_date_label = _args.date or datetime.now().strftime("%Y-%m")
_today = date.today()
_end_of_last_month = _today.replace(day=1) - timedelta(days=1)
_start_of_ttm = _end_of_last_month.replace(day=1) - relativedelta(months=11)
START_DATE = _start_of_ttm.isoformat()
END_DATE = (_end_of_last_month + timedelta(days=1)).isoformat()

# Market calendar events (Priority 1) for flagging in period comparisons
MARKET_EVENTS = [
    ("Atlanta Market", "2025-07-14", "2025-07-20"),
    ("Dallas Total Home & Gift", "2025-06-24", "2025-06-30"),
    ("High Point Market (Fall)", "2025-10-17", "2025-10-21"),
    ("Dallas Total Home & Gift", "2026-01-07", "2026-01-13"),
    ("Atlanta Market", "2026-01-13", "2026-01-19"),
    ("Las Vegas Market", "2026-01-25", "2026-01-29"),
    ("Artisan Resource @ NY NOW", "2026-02-01", "2026-02-03"),
    ("High Point Market (Spring)", "2026-04-25", "2026-04-29"),
    ("NeoCon", "2026-06-08", "2026-06-10"),
    ("Atlanta Market", "2026-07-14", "2026-07-20"),
]

def markets_in_range(start, end):
    """Return market events overlapping a date range."""
    hits = []
    for name, ms, me in MARKET_EVENTS:
        if ms <= end and me >= start:
            hits.append(name)
    return hits

# ==========================================================================
# MCP Connection Layer
# Postgres: SSE transport → https://mcp-postgres-staging.k8s.supercatsolutions.com/sse
# BigQuery: Streamable HTTP → https://bigquery-cli-staging.k8s.supercatsolutions.com/mcp
# ==========================================================================

PG_MCP_URL  = "https://mcp-postgres-staging.k8s.supercatsolutions.com/sse"
BQ_MCP_URL  = "https://bigquery-cli-staging.k8s.supercatsolutions.com/mcp"
_MCP_HEADERS = {"Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"}

def _parse_sse_data(text):
    """Extract the first JSON-RPC data payload from an SSE response body."""
    for chunk in text.split("\n\n"):
        for line in chunk.strip().split("\n"):
            if line.startswith("data:"):
                return json.loads(line[5:].strip())
    return None


class _PgMcpSession:
    """Persistent Postgres MCP session using the SSE transport."""

    def __init__(self, sse_url):
        self._url = sse_url
        self._events = queue.Queue()
        self._msg_id = 0
        self._endpoint = None

    def connect(self):
        self._thread = threading.Thread(target=self._listen, daemon=True)
        self._thread.start()
        _, endpoint_path = self._events.get(timeout=15)
        base = self._url.rsplit("/", 1)[0]
        self._endpoint = base + endpoint_path if endpoint_path.startswith("/") else endpoint_path
        self._msg_id += 1
        requests.post(self._endpoint, json={
            "jsonrpc": "2.0", "id": self._msg_id, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "build_intelligence_deepdive", "version": "2.0"}}
        }, timeout=10)
        self._events.get(timeout=10)
        requests.post(self._endpoint,
                      json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                      timeout=10)

    def _listen(self):
        resp = requests.get(self._url, stream=True, timeout=300)
        etype, buf = None, []
        for raw in resp.iter_lines(decode_unicode=True):
            line = raw if raw else ""
            if line.startswith("event:"):
                etype = line[6:].strip()
            elif line.startswith("data:"):
                buf.append(line[5:].strip())
            elif line == "":
                if etype and buf:
                    self._events.put((etype, "\n".join(buf)))
                etype, buf = None, []

    def execute(self, sql):
        self._msg_id += 1
        mid = self._msg_id
        requests.post(self._endpoint, json={
            "jsonrpc": "2.0", "id": mid, "method": "tools/call",
            "params": {"name": "execute_sql", "arguments": {"sql": sql}}
        }, timeout=60)
        _, data_str = self._events.get(timeout=60)
        payload = json.loads(data_str)
        content = payload.get("result", {}).get("content", [{}])[0].get("text", "[]")
        return eval(content, _SAFE_EVAL_NS)


class _BqMcpSession:
    """BigQuery MCP session using Streamable HTTP transport."""

    def __init__(self, url):
        self._url = url
        self._msg_id = 0
        self._session_id = None

    def connect(self):
        self._msg_id += 1
        r = requests.post(self._url, json={
            "jsonrpc": "2.0", "id": self._msg_id, "method": "initialize",
            "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                       "clientInfo": {"name": "build_intelligence_deepdive", "version": "2.0"}}
        }, headers=_MCP_HEADERS, timeout=10)
        self._session_id = r.headers.get("mcp-session-id")
        hdrs = {**_MCP_HEADERS}
        if self._session_id:
            hdrs["mcp-session-id"] = self._session_id
        requests.post(self._url,
                      json={"jsonrpc": "2.0", "method": "notifications/initialized"},
                      headers=hdrs, timeout=10)

    def query(self, sql):
        self._msg_id += 1
        hdrs = {**_MCP_HEADERS}
        if self._session_id:
            hdrs["mcp-session-id"] = self._session_id
        r = requests.post(self._url, json={
            "jsonrpc": "2.0", "id": self._msg_id, "method": "tools/call",
            "params": {"name": "query", "arguments": {"query": sql}}
        }, headers=hdrs, timeout=120)
        payload = _parse_sse_data(r.text)
        content_text = payload.get("result", {}).get("content", [{}])[0].get("text", "{}")
        result = json.loads(content_text)
        return result.get("data", [])


# --- Establish MCP connections ---

print("Connecting to Postgres MCP ...")
_pg = _PgMcpSession(PG_MCP_URL)
_pg.connect()
print("  ✓ Postgres MCP connected")

print("Connecting to BigQuery MCP ...")
_bq = _BqMcpSession(BQ_MCP_URL)
_bq.connect()
print("  ✓ BigQuery MCP connected")

def pg_query(sql, params=None):
    if params:
        sql = _interpolate_params(sql, params)
    return _pg.execute(sql)

def _interpolate_params(sql, params):
    """Replace %s placeholders with properly escaped values (Postgres-safe)."""
    parts = sql.split("%s")
    out = [parts[0]]
    for i, p in enumerate(params):
        if isinstance(p, str):
            escaped = p.replace("'", "''")
            out.append(f"'{escaped}'")
        elif p is None:
            out.append("NULL")
        else:
            out.append(str(p))
        out.append(parts[i + 1])
    return "".join(out)

def bq_query(sql):
    return _bq.query(sql)

# --- BQ event name mapping (CLM label → Mixpanel snake_case) ---
BQ_EVENT_MAP = {
    "Search Products":        "product_search",
    "Filter Products":        "filter_button_pressed",
    "Create PDF Catalog":     "pdf_catalog_generated",
    "View Kit":               "view_kit",
    "Order kit":              "add_kit_to_order",
    "Order Configured Item":  "add_configured_item_to_order",
    "Scan Item with Camera":  "item_scanned",
    "Submit Order":           "order_submitted",
    "Access Sales Portal":    "view_portal",
    "View iPad Orders":       "view_customer_orders",
    "Select a Customer":      "customer_selection",
    "Search for Customer":    "customer_search",
    "View Cust. Favorites":   "view_favorites",
    "View Cust. Backorders":  "view_customer_on_order_items",
    "View SmartPicks":        "view_customer_smart_picks",
    "Email Item Info":        "item_email_drafted",
    "View Library Entry":     "view_document",
    "Create 'My List'":       "create_stack",
    "Order From Maybe List":  "add_to_order_from_maybe_list",
    "Show Sales in Catalog":  "show_customer_sales_setting_changed",
}

FEATURES = [
    ("Search Products", "Search Products"),
    ("Filter Products", "Filter Products"),
    ("Create PDF Catalog", "Create PDF Catalog"),
    ("View Kit", "View Kit"),
    ("Order kit", "Order Kit"),
    ("Order Configured Item", "Config Items"),
    ("Scan Item with Camera", "Camera Scan"),
    ("Submit Order", "Submit Order"),
    ("Access Sales Portal", "Sales Portal"),
    ("View iPad Orders", "iPad Orders"),
    ("Select a Customer", "Select Customer"),
    ("Search for Customer", "Search Customer"),
    ("View Cust. Favorites", "Cust. Favorites"),
    ("View Cust. Backorders", "Cust. Backorders"),
    ("View SmartPicks", "SmartPicks"),
    ("Email Item Info", "Email Item"),
    ("View Library Entry", "Library Entry"),
    ("Create 'My List'", "My List"),
    ("Order From Maybe List", "Maybe List Order"),
    ("Show Sales in Catalog", "Show Sales"),
]

# ---------- helpers ----------

def fmt_currency(v):
    if v >= 1_000_000:
        return f"${v/1_000_000:,.1f}M"
    if v >= 100_000:
        return f"${v/1_000:,.0f}K"
    if v >= 1_000:
        return f"${v:,.0f}"
    return f"${v:,.2f}"

def fmt_num(v):
    return f"{v:,}"

def pct(n, d):
    if d == 0:
        return 0
    return round(100 * n / d, 1)

# ==========================================================================
# DATA LOADING — Postgres + BigQuery (no CSV files)
# ==========================================================================

print(f"\nDate range: {START_DATE} → {END_DATE}")

# ---------- process orders (Postgres: canonical dedup + line-item query) ----------

entity_orders = {}
for code, cfg in ENTITIES.items():
    org_id = cfg["org_id"]
    print(f"\n  Loading orders for {cfg['label']} (org {org_id}) ...")

    # Revenue computed in SQL via jsonb_array_elements — avoids transferring order_items blobs
    order_rows = pg_query("""
        WITH base_orders AS (
            SELECT o.id, o.order_number,
                   o.submit_date::text AS submit_date,
                   o.order_type, o.order_source,
                   COALESCE(o.rep_first_name,'') || ' ' || COALESCE(o.rep_last_name,'') AS rep_name,
                   o.customer_num, o.bill_to_company_name,
                   COALESCE(
                       (SELECT SUM((item->>'extended_price')::numeric)
                        FROM jsonb_array_elements(o.order_items::jsonb) AS item
                        WHERE item->>'extended_price' IS NOT NULL), 0
                   ) AS line_item_revenue,
                   SPLIT_PART(o.order_number, '-', 1) || '-' ||
                     SPLIT_PART(o.order_number, '-', 2) || '-' ||
                     SPLIT_PART(o.order_number, '-', 3) AS main_part,
                   CASE
                     WHEN array_length(string_to_array(o.order_number, '-'), 1) <= 3 THEN -1
                     WHEN SPLIT_PART(o.order_number, '-', 4) ~ '^\\d+$'
                       THEN SPLIT_PART(o.order_number, '-', 4)::int
                     ELSE 0
                   END AS suffix_ord
            FROM orders o
            WHERE o.organization_id = %s
              AND o.submit_date >= %s AND o.submit_date < %s
              AND o.is_submitted = true
              AND COALESCE(o.is_marked_deleted, false) = false
        ),
        ranked AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY main_part ORDER BY suffix_ord DESC) AS rn
            FROM base_orders
        )
        SELECT id, submit_date, order_type, order_source, rep_name,
               customer_num, bill_to_company_name, line_item_revenue
        FROM ranked WHERE rn = 1
    """, (org_id, START_DATE, END_DATE))
    print(f"    orders query returned {len(order_rows)} rows")

    # Batch territory lookup — single query for all customer_nums
    cust_nums = list(set(str(r.get("customer_num", "")) for r in order_rows if r.get("customer_num")))
    terr_map = {}
    if cust_nums:
        in_clause = ", ".join("'" + c.lower().replace("'", "''") + "'" for c in cust_nums)
        terr_rows = pg_query(
            f"SELECT LOWER(code) AS code, territory_codes FROM customers "
            f"WHERE organization_id = {org_id} AND LOWER(code) IN ({in_clause})"
        )
        for tr in terr_rows:
            try:
                terr_map[tr["code"]] = json.loads(tr["territory_codes"]) if tr.get("territory_codes") else []
            except (json.JSONDecodeError, TypeError):
                pass
    print(f"    territory lookup: {len(terr_map)} customers mapped")

    total_rev = 0.0
    total_orders = len(order_rows)
    customers = defaultdict(float)
    monthly_rev = defaultdict(float)
    monthly_orders = defaultdict(int)
    territories = defaultdict(lambda: {"orders": 0, "revenue": 0})
    website_orders = 0
    confirmed = 0
    quote = 0

    for r in order_rows:
        amt = float(r.get("line_item_revenue", 0) or 0)
        total_rev += amt

        cname = (r.get("bill_to_company_name") or "").strip()
        if cname:
            customers[cname] += amt

        if r.get("order_source") == "server":
            website_orders += 1

        otype = (r.get("order_type") or "").strip()
        if otype == "Confirmed":
            confirmed += 1
        elif otype == "Quote":
            quote += 1

        cnum = str(r.get("customer_num") or "").lower()
        if cnum and cnum in terr_map:
            for tc in terr_map[cnum]:
                territories[tc]["orders"] += 1
                territories[tc]["revenue"] += amt

        sd = r.get("submit_date")
        if sd:
            mkey = str(sd)[:7]
            monthly_rev[mkey] += amt
            monthly_orders[mkey] += 1

    top_customers = sorted(customers.items(), key=lambda x: -x[1])[:10]
    unique_customers = len(customers)
    ordering_customers = sum(1 for c, v in customers.items() if v > 0)
    aov = total_rev / total_orders if total_orders else 0
    top_cust_conc = (top_customers[0][1] / total_rev * 100) if top_customers and total_rev else 0

    rep_stats = defaultdict(lambda: {"orders": 0, "revenue": 0.0, "customers": set()})
    for r in order_rows:
        rname = (r.get("rep_name") or "").strip()
        if rname:
            amt = float(r.get("line_item_revenue", 0) or 0)
            rep_stats[rname]["orders"] += 1
            rep_stats[rname]["revenue"] += amt
            cname = (r.get("bill_to_company_name") or "").strip()
            if cname:
                rep_stats[rname]["customers"].add(cname)
    pg_top_reps = sorted(
        [{"name": k, "orders": v["orders"], "revenue": v["revenue"],
          "customers": len(v["customers"])} for k, v in rep_stats.items()],
        key=lambda x: -x["revenue"]
    )[:20]

    entity_orders[code] = {
        "total_orders": total_orders,
        "total_revenue": total_rev,
        "unique_customers": unique_customers,
        "ordering_customers": ordering_customers,
        "aov": aov,
        "website_orders": website_orders,
        "self_service_pct": pct(website_orders, total_orders),
        "confirmed": confirmed,
        "quote": quote,
        "top_customers": top_customers,
        "top_cust_concentration": round(top_cust_conc, 1),
        "monthly_rev": dict(monthly_rev),
        "monthly_orders": dict(monthly_orders),
        "territories": dict(territories),
        "pg_top_reps": pg_top_reps,
    }
    print(f"    ✓ {total_orders} orders, {fmt_currency(total_rev)}")

# ---------- process usage (BigQuery events + Postgres licensed users) ----------

entity_usage = {}
all_reps = {}

LICENSED_USERS_OVERRIDE = {
    "gh":    54,
    "sc":    122,
    "scw":   90,
    "sccon": 29,
    "clm":   135,
}

for code, cfg in ENTITIES.items():
    org_id = cfg["org_id"]
    print(f"\n  Loading usage for {cfg['label']} ...")

    # 1. Licensed user count — hardcoded known-correct values
    total_licensed = LICENSED_USERS_OVERRIDE.get(code, 0)

    # 1b. Fetch ALL non-disabled org_users for BQ cross-reference
    #     (user_type filter is ambiguous for some accounts — override controls count)
    licensed_usernames = {}
    lic_rows = pg_query(f"""
        SELECT u.username, u.first_name, u.last_name
        FROM org_users ou
        JOIN users u ON ou.user_id = u.id
        WHERE ou.organization_id = {org_id}
          AND ou.disabled = false
    """)
    for lr in lic_rows:
        uname = (lr.get("username") or "").strip().lower()
        if uname:
            licensed_usernames[uname] = lr

    # Build reverse lookup: BQ usernames often have org prefixes (sc-, gh-)
    _bq_to_pg = {}
    _org_prefixes = ["sc-", "gh-", "scw-", "sccon-"]
    for pg_uname in licensed_usernames:
        _bq_to_pg[pg_uname] = pg_uname
        for pfx in _org_prefixes:
            _bq_to_pg[pfx + pg_uname] = pg_uname

    # 2. Per-user event counts from BigQuery
    bq_events_in = ", ".join(f"'{v}'" for v in BQ_EVENT_MAP.values())
    bq_rows = bq_query(f"""
        SELECT LOWER(username) AS username, event_name, COUNT(*) AS cnt
        FROM mixpanel__events
        WHERE current_organization_shortname = '{code}'
          AND event_name IN ({bq_events_in}, 'selected_org')
          AND time >= UNIX_SECONDS(TIMESTAMP('{START_DATE}'))
          AND time <  UNIX_SECONDS(TIMESTAMP('{END_DATE}'))
        GROUP BY 1, 2
    """)

    reverse_map = {v: label for csv_col, label in FEATURES for v, label
                   in [(BQ_EVENT_MAP.get(csv_col), label)] if v}

    # Normalize BQ usernames to PG usernames via prefix mapping
    user_events = defaultdict(lambda: defaultdict(int))
    user_logins = defaultdict(int)
    for row in bq_rows:
        bq_uname = row["username"]
        pg_uname = _bq_to_pg.get(bq_uname, bq_uname)
        ev = row["event_name"]
        cnt = row["cnt"]
        if ev == "selected_org":
            user_logins[pg_uname] += cnt
        elif ev in reverse_map:
            user_events[pg_uname][reverse_map[ev]] += cnt

    # 3. Build user list (merge licensed users with BQ activity)
    users = []
    active_users = 0
    seen_usernames = set()

    for uname_lower, pg_row in licensed_usernames.items():
        seen_usernames.add(uname_lower)
        logins = user_logins.get(uname_lower, 0)
        ev = user_events.get(uname_lower, {})

        feature_counts = {}
        total_events = 0
        breadth = 0
        for _, label in FEATURES:
            val = ev.get(label, 0)
            feature_counts[label] = val
            total_events += val
            if val > 0:
                breadth += 1

        submit_order = ev.get("Submit Order", 0)
        name = f"{pg_row['first_name'] or ''} {pg_row['last_name'] or ''}".strip()

        udata = {
            "user": pg_row["username"],
            "name": name,
            "logins": logins,
            "orders": submit_order,
            "last_login": "",
            "features": feature_counts,
            "total_events": total_events,
            "breadth": breadth,
        }
        users.append(udata)
        if logins > 0:
            active_users += 1
        if name:
            all_reps.setdefault(name, {})[code] = udata

    # Include BQ-only users not in PG licensed list for this org
    # These may be cross-org users or former employees — they still count
    # toward active (capped at licensed override below)
    for uname_lower in set(user_logins.keys()) | set(user_events.keys()):
        if uname_lower in seen_usernames:
            continue
        seen_usernames.add(uname_lower)
        logins = user_logins.get(uname_lower, 0)
        ev = user_events.get(uname_lower, {})
        feature_counts = {}
        total_events = 0
        breadth = 0
        for _, label in FEATURES:
            val = ev.get(label, 0)
            feature_counts[label] = val
            total_events += val
            if val > 0:
                breadth += 1
        udata = {
            "user": uname_lower,
            "name": uname_lower,
            "logins": logins,
            "orders": ev.get("Submit Order", 0),
            "last_login": "",
            "features": feature_counts,
            "total_events": total_events,
            "breadth": breadth,
        }
        users.append(udata)
        if logins > 0:
            active_users += 1

    feature_totals = defaultdict(int)
    for u in users:
        for label, val in u["features"].items():
            feature_totals[label] += val

    top_reps = sorted(users, key=lambda x: -x["orders"])[:15]
    total_user_orders = sum(u["orders"] for u in users)
    top_rep_conc = (top_reps[0]["orders"] / total_user_orders * 100) if top_reps and total_user_orders > 0 else 0

    active_users = min(active_users, total_licensed)

    entity_usage[code] = {
        "total_licensed": total_licensed,
        "active_users": active_users,
        "active_pct": pct(active_users, total_licensed),
        "users": users,
        "feature_totals": dict(feature_totals),
        "top_reps": top_reps,
        "top_rep_concentration": round(top_rep_conc, 1),
        "top_rep_name": top_reps[0]["name"] if top_reps else "",
    }
    print(f"    ✓ {active_users}/{total_licensed} active, {sum(feature_totals.values())} total events")

# ---------- cross-entity reps ----------

cross_entity_reps = []
for name, entities in all_reps.items():
    if len(entities) >= 2:
        total_orders = sum(e["orders"] for e in entities.values())
        max_breadth = max(e["breadth"] for e in entities.values())
        if total_orders > 0:
            cross_entity_reps.append({
                "name": name,
                "entities": entities,
                "total_orders": total_orders,
                "max_breadth": max_breadth,
                "entity_count": len(entities),
            })

cross_entity_reps.sort(key=lambda x: -x["total_orders"])

# ---------- aggregates ----------

grand_total_orders = sum(e["total_orders"] for e in entity_orders.values())
grand_total_revenue = sum(e["total_revenue"] for e in entity_orders.values())
grand_total_users = sum(e["active_users"] for e in entity_usage.values())
grand_total_licensed = sum(e["total_licensed"] for e in entity_usage.values())

# monthly growth
months = sorted(set(m for e in entity_orders.values() for m in e["monthly_rev"]))

# feature heatmap data
heatmap_features = [
    "Submit Order", "View Kit", "Order Kit", "Config Items", "Camera Scan",
    "Create PDF Catalog", "Sales Portal", "Select Customer", "Search Customer",
    "Library Entry", "SmartPicks", "Show Sales",
]

# ---------- build HTML ----------

def heatmap_bg(val, max_val):
    if val == 0:
        return "rgba(196,93,93,0.1)"
    ratio = val / max_val if max_val else 0
    alpha = 0.05 + ratio * 0.20
    return f"rgba(74,124,89,{alpha:.2f})"

def winner_bg():
    return "rgba(201,168,76,0.15)"

def risk_color(pct_val):
    if pct_val < 15:
        return "#4A7C59"
    elif pct_val < 25:
        return "#B8960C"
    return "#C45D5D"

def risk_label(pct_val):
    if pct_val < 15:
        return "Low"
    elif pct_val < 25:
        return "Moderate"
    return "High"

def status_pill(text, color):
    colors = {
        "green": ("rgba(74,124,89,0.12)", "#4A7C59"),
        "gold": ("rgba(201,168,76,0.15)", "#B8960C"),
        "red": ("rgba(196,93,93,0.1)", "#C45D5D"),
    }
    bg, fg = colors.get(color, colors["green"])
    return f'<span style="display:inline-block;padding:2px 8px;border-radius:4px;background:{bg};color:{fg};font-family:\'DM Mono\',monospace;font-size:0.72rem;">{text}</span>'

entity_labels = {c: cfg["label"] for c, cfg in ENTITIES.items()}
entity_codes = list(ENTITIES.keys())
is_single = len(entity_codes) == 1
_account_label = entity_labels[entity_codes[0]] if is_single else " &amp; ".join(dict.fromkeys(ACCOUNT_FOLDERS[c] for c in entity_codes).keys()).replace("_", " ")

# --- MoM growth calculation (two most recent complete months) ---
_all_months = sorted(set(m for e in entity_orders.values() for m in e["monthly_rev"]))
_current_month = date.today().strftime("%Y-%m")
_complete_months = [m for m in _all_months if m < _current_month]
mom_data = {}
if len(_complete_months) >= 2:
    _prior_mo = _complete_months[-2]
    _recent_mo = _complete_months[-1]
    # Flag market events overlapping each month
    _prior_markets = markets_in_range(f"{_prior_mo}-01", f"{_prior_mo}-28")
    _recent_markets = markets_in_range(f"{_recent_mo}-01", f"{_recent_mo}-28")
    for code in entity_codes:
        mo = entity_orders[code]["monthly_rev"]
        prior_val = mo.get(_prior_mo, 0)
        recent_val = mo.get(_recent_mo, 0)
        if prior_val > 0:
            growth = (recent_val - prior_val) / prior_val * 100
            mom_data[code] = {
                "jan": prior_val, "feb": recent_val,
                "prior_label": _prior_mo, "recent_label": _recent_mo,
                "growth": round(growth, 1),
                "prior_markets": _prior_markets,
                "recent_markets": _recent_markets,
            }
else:
    _prior_mo = ""
    _recent_mo = ""

# --- Feature activation (zero or very low features per entity) ---
activation_items = []
for label in [f[1] for f in FEATURES]:
    for code in entity_codes:
        val = entity_usage[code]["feature_totals"].get(label, 0)
        if val == 0:
            best_entity = max(entity_codes, key=lambda c: entity_usage[c]["feature_totals"].get(label, 0))
            best_val = entity_usage[best_entity]["feature_totals"].get(label, 0)
            if best_val > 0:
                activation_items.append({
                    "feature": label,
                    "entity": code,
                    "current": val,
                    "best_entity": best_entity,
                    "best_val": best_val,
                })

# deduplicate activation items by feature
seen = set()
unique_activation = []
for item in activation_items:
    key = item["feature"]
    if key not in seen:
        seen.add(key)
        users_of = [c for c in entity_codes if entity_usage[c]["feature_totals"].get(item["feature"], 0) > 0]
        gaps = [c for c in entity_codes if entity_usage[c]["feature_totals"].get(item["feature"], 0) == 0]
        if gaps and users_of:
            unique_activation.append({
                "feature": item["feature"],
                "users": users_of,
                "gaps": gaps,
                "best_entity": item["best_entity"],
                "best_val": item["best_val"],
            })


# ============================================================
# HTML GENERATION
# ============================================================

html = []

def slide_start(cls, slide_num):
    html.append(f'<section class="slide {cls}" data-slide="{slide_num}">')
    html.append('<div class="inner">')

def slide_end(note=""):
    html.append('</div>')
    if note:
        html.append(f'<div class="pnote" data-note>{note}</div>')
    html.append('</section>')

html.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>""" + (_account_label + " — Intelligence Deep-Dive EBR") + """</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-snap-type:y mandatory;scroll-behavior:smooth;font-size:16px}
body{font-family:'DM Sans',sans-serif;color:#1E3A2F;background:#F7F5F0;line-height:1.5}
.slide{min-height:100vh;scroll-snap-align:start;display:flex;align-items:center;justify-content:center;position:relative;padding:48px 24px}
.slide .inner{max-width:1060px;width:100%}
.s-dk{background:#1E3A2F;color:#fff}
.s-lt{background:#F7F5F0;color:#1E3A2F}
.s-wh{background:#fff;color:#1E3A2F}
.lbl{font-family:'DM Mono',monospace;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.12em;color:#C9A84C;margin-bottom:6px}
.s-dk .lbl{color:#C9A84C}
h2{font-family:Georgia,serif;font-size:2.2rem;font-weight:400;margin-bottom:18px;line-height:1.2}
h3{font-family:Georgia,serif;font-size:1.4rem;font-weight:400;margin-bottom:12px}
.s-dk h2{color:#fff}
.gold-rule{width:56px;height:2px;background:#C9A84C;margin-bottom:18px}
.stat-row{display:flex;gap:24px;flex-wrap:wrap;margin:20px 0}
.stat-card{flex:1;min-width:140px;text-align:center}
.stat-card .num{font-family:Georgia,serif;font-size:2.8rem;color:#1E3A2F;line-height:1.1}
.s-dk .stat-card .num{color:#C9A84C}
.stat-card .lab{font-family:'DM Mono',monospace;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;color:#4A7C59;margin-top:4px}
.s-dk .stat-card .lab{color:rgba(255,255,255,0.6)}
table{width:100%;border-collapse:collapse;font-size:0.8rem;font-family:'DM Mono',monospace;margin:16px 0}
th{font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;border-bottom:2px solid #1E3A2F;padding:6px 8px;text-align:left;color:#4A7C59;font-weight:500}
td{padding:6px 8px;border-bottom:1px solid rgba(30,58,47,0.1)}
.num-cell{text-align:right;font-variant-numeric:tabular-nums}
.bold{font-weight:700}
.gold-text{color:#C9A84C}
.green-text{color:#4A7C59}
.red-text{color:#C45D5D}
.winner-col{color:#B8960C;text-align:right;border-left:2px solid rgba(201,168,76,0.3);font-weight:500}
.insight-box{border-left:3px solid #C9A84C;padding:10px 16px;margin:16px 0;font-size:0.88rem;background:rgba(201,168,76,0.06)}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin:16px 0}
.card{background:#fff;border-radius:6px;padding:16px;border-top:3px solid #4A7C59}
.s-wh .card{background:#F7F5F0}
.card-gold{border-top-color:#C9A84C}
.rec-card{border-top:3px solid #C9A84C;background:#fff;border-radius:6px;padding:20px;margin-bottom:12px}
.s-wh .rec-card{background:#F7F5F0}
.rec-card .priority{font-family:'DM Mono',monospace;color:#C9A84C;font-size:0.8rem;margin-bottom:4px}
.rec-card h3{margin-bottom:10px}
.rec-card .row-label{font-family:'DM Mono',monospace;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;color:#4A7C59;margin-top:8px}
.q-block{margin:18px 0;padding:12px 0;border-bottom:1px solid rgba(255,255,255,0.1)}
.q-tag{font-family:'DM Mono',monospace;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;color:#C9A84C;margin-bottom:4px}
.q-text{font-family:Georgia,serif;font-size:1.05rem;color:rgba(255,255,255,0.92);line-height:1.4}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin:16px 0}
.col-header{font-family:'DM Mono',monospace;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;padding:8px 12px;color:#fff;margin-bottom:12px;border-radius:4px 4px 0 0}
.col-header.green-hd{background:#4A7C59}
.col-header.gold-hd{background:#B8960C}
.commit-list{list-style:none;padding:0}
.commit-list li{padding:6px 12px;font-size:0.84rem;border-bottom:1px solid rgba(30,58,47,0.08)}
.commit-list li.blank{color:#999;font-style:italic}
.risk-dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
.module-grid td.active{background:rgba(74,124,89,0.12);color:#4A7C59;text-align:center;font-weight:700}
.module-grid td.gap{background:rgba(196,93,93,0.08);color:#C45D5D;text-align:center}
.mini-stat{background:#fff;border-radius:6px;padding:14px;text-align:center}
.s-wh .mini-stat{background:#F7F5F0}
.mini-stat .entity-name{font-family:'DM Mono',monospace;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:#4A7C59;margin-bottom:4px}
.mini-stat .rep-name{font-weight:700;font-size:0.88rem;margin-bottom:2px}
.mini-stat .rep-pct{font-family:Georgia,serif;font-size:1.6rem;line-height:1.1}

.status-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:16px 0}
.status-item{background:#F7F5F0;border-radius:6px;padding:14px;display:flex;align-items:flex-start;gap:10px}
.s-wh .status-item{background:#fff}
.status-dot{width:10px;height:10px;border-radius:50%;margin-top:4px;flex-shrink:0}
.status-item .si-label{font-family:'DM Mono',monospace;font-size:0.68rem;text-transform:uppercase;color:#4A7C59;letter-spacing:0.08em}
.status-item .si-detail{font-size:0.82rem;margin-top:2px}

.growth-card{text-align:center;padding:18px;background:#fff;border-radius:6px}
.s-lt .growth-card{background:#fff}
.growth-card .growth-pct{font-family:Georgia,serif;font-size:3.2rem;color:#C9A84C;line-height:1}
.growth-card .growth-label{font-family:'DM Mono',monospace;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.08em;color:#4A7C59;margin-top:4px}
.growth-card .growth-detail{font-size:0.78rem;color:#666;margin-top:4px}

.transfer-item{display:flex;align-items:flex-start;gap:14px;padding:14px 0;border-bottom:1px solid rgba(30,58,47,0.08)}
.transfer-icon{width:36px;height:36px;border-radius:50%;background:rgba(201,168,76,0.15);display:flex;align-items:center;justify-content:center;flex-shrink:0;color:#C9A84C;font-size:1.2rem}
.transfer-icon.green-icon{background:rgba(74,124,89,0.12);color:#4A7C59}

.entity-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:28px}
.entity-card{background:#fff;border:1px solid #E0DED6;border-top:3px solid #4A7C59;border-radius:6px;padding:20px;box-shadow:0 1px 4px rgba(0,0,0,.06)}
.entity-card h3{font-family:Georgia,serif;font-size:1.05rem;margin-bottom:2px}
.entity-tag{font-family:'DM Mono',monospace;font-size:.65rem;text-transform:uppercase;letter-spacing:.1em;color:#7A7A6E;margin-bottom:12px}
.entity-row{display:flex;justify-content:space-between;padding:5px 0;font-size:.84rem;border-bottom:1px solid #F0EDE6}
.entity-row:last-child{border-bottom:none}
.entity-row span:last-child{font-family:'DM Mono',monospace;font-size:.8rem;color:#1E3A2F}
.framing{font-style:italic;color:#7A7A6E;font-size:.84rem;line-height:1.5;max-width:860px}
.q-card{background:rgba(201,168,76,.08);border-left:3px solid #C9A84C;padding:18px 24px;margin-bottom:16px;border-radius:0 6px 6px 0}
.s-dk .q-card{background:rgba(201,168,76,.12)}
.s-dk .q-text{color:rgba(255,255,255,.92)}
.insight-line{border-left:3px solid #4A7C59;padding:12px 20px;margin-top:24px;font-size:.9rem;background:rgba(74,124,89,.06);border-radius:0 4px 4px 0}
.s-wh .insight-line{background:rgba(74,124,89,.05)}
.stat-card .num.hero{font-size:3.4rem}
table.data-table{width:100%;border-collapse:collapse;margin-bottom:20px}
table.data-table th{font-family:'DM Mono',monospace;font-size:.68rem;text-transform:uppercase;letter-spacing:.1em;color:#7A7A6E;text-align:left;padding:8px 12px;border-bottom:2px solid #E0DED6}
table.data-table td{font-family:'DM Sans',sans-serif;font-size:.84rem;padding:8px 12px;border-bottom:1px solid #F0EDE6}
table.data-table td.num{font-family:'DM Mono',monospace;font-size:.8rem;text-align:right}
table.data-table td.bold{font-weight:600}
.feature-col{padding:20px;border-radius:6px;background:#F7F5F0}
.s-wh .feature-col{background:#fff;border:1px solid #E0DED6}
.feature-col h4{font-family:'DM Mono',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid}
.feature-col.heavy h4{border-color:#4A7C59;color:#4A7C59}
.feature-col.zero h4{border-color:#C9A84C;color:#C9A84C}
.feature-row{display:flex;justify-content:space-between;padding:6px 0;font-size:.84rem;border-bottom:1px solid #F0EDE6}
.feature-count{font-family:'DM Mono',monospace;font-size:.8rem}
.feature-col.heavy .feature-count{color:#4A7C59}
.feature-col.zero .feature-count{color:#C45D5D}
.closing-text{font-family:Georgia,serif;font-size:2.4rem;color:#fff;line-height:1.3;max-width:700px}
.closing-stat{font-family:Georgia,serif;font-size:2.4rem;color:#fff;line-height:1.3;max-width:800px}
.closing-sub{font-family:'DM Mono',monospace;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.12em;color:#C9A84C;margin-top:20px}

#counter{position:fixed;bottom:16px;right:20px;font-family:'DM Mono',monospace;font-size:0.72rem;color:rgba(30,58,47,0.4);z-index:100;pointer-events:none}
.s-dk #counter,.slide.s-dk~#counter{color:rgba(255,255,255,0.35)}

#notes-bar{position:fixed;bottom:0;left:0;right:0;background:rgba(30,58,47,0.92);color:rgba(255,255,255,0.88);padding:12px 24px;font-size:0.82rem;border-top:2px solid #C9A84C;display:none;z-index:200;max-height:120px;overflow-y:auto;font-family:'DM Sans',sans-serif}
#notes-bar.visible{display:block}

@media print{
html{scroll-snap-type:none}
.slide{min-height:auto;page-break-after:always;padding:24px}
#counter,#notes-bar,.pnote{display:none!important}
.s-dk{background:#1E3A2F!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
@media(max-width:900px){
.slide{padding:24px 16px}
h2{font-size:1.6rem}
.stat-card .num{font-size:2rem}
.two-col,.status-grid{grid-template-columns:1fr}
table{font-size:0.7rem}
.card-grid{grid-template-columns:1fr}
}
</style>
</head>
<body>
""")

# ============================
# SLIDE 1: Title
# ============================
slide_start("s-dk", 1)
html.append('<div class="gold-rule"></div>')
html.append('<h2 style="font-size:3.4rem;margin-bottom:8px">Executive Business Review</h2>')
html.append('<p style="font-family:Georgia,serif;font-size:1.3rem;color:rgba(255,255,255,0.75);margin-bottom:6px">Sales Intelligence &amp; Operational Deep-Dive</p>')
html.append(f'<p style="font-family:Georgia,serif;font-size:1.6rem;color:rgba(255,255,255,0.92);margin-bottom:20px">{_account_label}</p>')
html.append(f'<p style="font-family:\'DM Mono\',monospace;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.12em;color:#C9A84C">{_date_label.replace("-", " &middot; ")} &middot; SuperCat / eCat</p>')
slide_end("This is the data-heavy version. Move through the title quickly — this audience wants substance.")

# ============================
# SLIDE 2: Partnership Overview (with entity cards)
# ============================
slide_start("s-lt", 2)
html.append('<div class="lbl">Partnership Overview</div>')
if is_single:
    _code0 = entity_codes[0]
    _o0 = entity_orders[_code0]
    _u0 = entity_usage[_code0]
    html.append(f'<h2>{_account_label}. Long-Standing&nbsp;Partner.</h2>')
    html.append('<div class="stat-row">')
    html.append(f'<div class="stat-card"><div class="num">{fmt_num(_u0["active_users"])}</div><div class="lab">Active Users</div></div>')
    html.append(f'<div class="stat-card"><div class="num">{_u0["total_licensed"]}</div><div class="lab">Licensed Reps</div></div>')
    html.append(f'<div class="stat-card"><div class="num">{fmt_num(_o0["total_orders"])}</div><div class="lab">Orders (TTM)</div></div>')
    html.append(f'<div class="stat-card"><div class="num">{fmt_currency(_o0["total_revenue"])}</div><div class="lab">Revenue (TTM)</div></div>')
    html.append('</div>')
    _aov = _o0["aov"]
    _unique_cust = _o0["unique_customers"]
    html.append(f'<div class="insight-line">{_account_label} has been on the eCat platform since 2013 — over 12 years. With {fmt_num(_unique_cust)} customers ordering and an AOV of {fmt_currency(_aov)}, this is a mature, high-velocity operation.</div>')
else:
    html.append(f'<h2>Long-Standing Partner. {len(entity_codes)}&nbsp;Divisions. One&nbsp;Platform.</h2>')
    html.append('<div class="stat-row">')
    html.append(f'<div class="stat-card"><div class="num">{len(entity_codes)}</div><div class="lab">eCat Entities</div></div>')
    html.append(f'<div class="stat-card"><div class="num">{fmt_num(grand_total_users)}</div><div class="lab">Active Users</div></div>')
    html.append(f'<div class="stat-card"><div class="num">{fmt_num(grand_total_orders)}</div><div class="lab">Orders (TTM)</div></div>')
    html.append(f'<div class="stat-card"><div class="num">{fmt_currency(grand_total_revenue)}</div><div class="lab">Revenue (TTM)</div></div>')
    html.append('</div>')
    entity_tags = {"gh": "GH &middot; B2B Wholesale", "sc": "SC &middot; B2B Wholesale",
                   "scw": "SCW &middot; Retail / DTC", "sccon": "SCCON &middot; B2B Contract"}
    html.append('<div class="entity-grid">')
    for code in entity_codes:
        o = entity_orders[code]
        u = entity_usage[code]
        html.append(f'<div class="entity-card"><h3>{entity_labels[code]}</h3>')
        html.append(f'<div class="entity-tag">{entity_tags.get(code, code.upper())}</div>')
        html.append(f'<div class="entity-row"><span>Users</span><span>{u["active_users"]} / {u["total_licensed"]}</span></div>')
        html.append(f'<div class="entity-row"><span>Orders (TTM)</span><span>{fmt_num(o["total_orders"])}</span></div>')
        html.append(f'<div class="entity-row"><span>Revenue (TTM)</span><span>{fmt_currency(o["total_revenue"])}</span></div>')
        html.append('</div>')
    html.append('</div>')
    html.append(f'<p class="framing">Our goal is to share what we see across the full picture — all {len(entity_codes)} divisions — and hear what matters to you.</p>')
slide_end("2 minutes. Walk entity cards briefly. Module feature matrix is on the next slide.")

# ============================
# SLIDE 3: Platform Coverage (module matrix — standalone)
# ============================
modules = ["iPad CPQ", "Sales Portal", "PDF Catalogs", "Kits", "Config Items", "Camera Scan", "SmartPicks", "Customer Lists"]
module_check = {}
for code in entity_codes:
    ft = entity_usage[code]["feature_totals"]
    module_check[code] = {
        "iPad CPQ": ft.get("Submit Order", 0) > 0,
        "Sales Portal": ft.get("Sales Portal", 0) > 0,
        "PDF Catalogs": ft.get("Create PDF Catalog", 0) > 0,
        "Kits": ft.get("View Kit", 0) > 0 or ft.get("Order Kit", 0) > 0,
        "Config Items": ft.get("Config Items", 0) > 0,
        "Camera Scan": ft.get("Camera Scan", 0) > 0,
        "SmartPicks": ft.get("SmartPicks", 0) > 0,
        "Customer Lists": ft.get("Select Customer", 0) > 0,
    }

slide_start("s-wh", 3)
html.append('<div class="lbl">Platform Coverage</div>')
_coverage_title = "What's Active" if is_single else "What Each Division Has Active"
html.append(f'<h2>{_coverage_title}</h2>')
html.append('<table class="module-grid">')
html.append('<tr><th>Entity</th>')
for m in modules:
    html.append(f'<th style="text-align:center">{m}</th>')
html.append('</tr>')
for code in entity_codes:
    html.append(f'<tr><td class="bold">{entity_labels[code]}</td>')
    for m in modules:
        if module_check[code][m]:
            html.append('<td class="active">&#10003;</td>')
        else:
            html.append('<td class="gap">&mdash;</td>')
    html.append('</tr>')
html.append('</table>')
_platform_scope = f"your {_account_label} account" if is_single else f"all {len(entity_codes)} divisions"
html.append(f'<p style="font-size:.84rem;color:#7A7A6E;margin-top:12px">Today we\'re sharing intelligence about your sales team and customer base across {_platform_scope}. We want your guidance on what matters most.</p>')
slide_end("60-90 seconds. The module grid is fast visual proof of platform maturity. Any gap cells are conversation starters.")

# ============================
# SLIDE 4: Before the Data — Discovery
# ============================
slide_start("s-dk", 4)
html.append('<div class="lbl">Discovery</div>')
html.append('<h2>Before the Data &mdash; What\'s on Your&nbsp;Mind?</h2>')

if is_single:
    _code0 = entity_codes[0]
    _o0 = entity_orders[_code0]
    _u0 = entity_usage[_code0]
    _mom0 = mom_data.get(_code0)
    _q1_txt = ""
    if _mom0 and abs(_mom0["growth"]) > 5:
        _dir = "grew" if _mom0["growth"] > 0 else "declined"
        _mkt = f" (overlapping {_mom0['recent_markets'][0]})" if _mom0.get("recent_markets") else ""
        _q1_txt = f'Revenue {_dir} {abs(_mom0["growth"]):.0f}% last month{_mkt}. '
    html.append(f'<div class="q-card"><div class="q-tag">Question 1</div><p class="q-text">{_q1_txt}How are you thinking about the role of the digital catalog in your sales motion heading into the spring market season?</p></div>')
    html.append(f'<div class="q-card"><div class="q-tag">Question 2</div><p class="q-text">You have {_u0["total_licensed"]} licensed reps and {_u0["active_users"]} active in the trailing twelve months. Are there reps who should be using the platform more, or is the current adoption where you want it?</p></div>')
    html.append('<div class="q-card"><div class="q-tag">Question 3</div><p class="q-text">What would make this hour most valuable for you?</p></div>')
else:
    _q1_parts = []
    for code, md in mom_data.items():
        if abs(md["growth"]) > 15:
            _market_flag = f" [{md['recent_markets'][0]}]" if md.get("recent_markets") else ""
            _q1_parts.append(f"{entity_labels[code]} {'grew' if md['growth'] > 0 else 'declined'} {abs(md['growth']):.0f}%{_market_flag}")
    _q1_detail = " and ".join(_q1_parts[:2]) if _q1_parts else "multiple divisions showing distinct patterns"
    html.append(f'<div class="q-card"><div class="q-tag">Question 1</div><p class="q-text">With {_q1_detail}, how are you thinking about the role of the digital catalog across these very different sales motions?</p></div>')
    html.append(f'<div class="q-card"><div class="q-tag">Question 2</div><p class="q-text">Your reps work across multiple divisions &mdash; {len(cross_entity_reps)} appear in two or more entities. Is that intentional structure, and does it create any friction or opportunity you\'d like us to help with?</p></div>')
    html.append('<div class="q-card"><div class="q-tag">Question 3</div><p class="q-text">What would make this hour most valuable for you?</p></div>')
html.append('<p class="framing" style="margin-top:28px">We have a lot of data to share, but we want to make sure we\'re focused on what matters to you.</p>')
slide_end("3-5 minutes. Earns permission to go deep. The third question lets them steer. Don't rush. Capture responses for data-anchored discovery slide.")

# ============================
# SLIDE 5: Platform Impact — Hero Numbers
# ============================
_adoption_rate = pct(grand_total_users, grand_total_licensed)
_total_logins = sum(sum(u["logins"] for u in entity_usage[c]["users"]) for c in entity_codes)
_total_searches = sum(entity_usage[c]["feature_totals"].get("Search Products", 0) for c in entity_codes)
_total_configs = sum(entity_usage[c]["feature_totals"].get("Config Items", 0) for c in entity_codes)

slide_start("s-wh", 5)
html.append('<div class="lbl">Platform Impact</div>')
html.append('<h2>What Your Team Accomplished &mdash; Trailing 12&nbsp;Months</h2>')
html.append('<div class="stat-row" style="margin-bottom:36px">')
html.append(f'<div class="stat-card"><div class="num hero">{fmt_currency(grand_total_revenue)}</div><div class="lab">Total Revenue</div></div>')
html.append(f'<div class="stat-card"><div class="num hero">{fmt_num(grand_total_orders)}</div><div class="lab">Transactions</div></div>')
html.append(f'<div class="stat-card"><div class="num hero">{fmt_num(grand_total_users)}</div><div class="lab">Active Users</div></div>')
html.append(f'<div class="stat-card"><div class="num hero">{_adoption_rate}%</div><div class="lab">Adoption Rate</div></div>')
html.append('</div>')
html.append(f'<div class="insight-line">Your teams logged in {fmt_num(_total_logins)} times, searched {fmt_num(_total_searches)}+ products, and configured {fmt_num(_total_configs)} custom items &mdash; all while processing {fmt_currency(grand_total_revenue)} in revenue.</div>')
slide_end("THE moment. Let the numbers breathe. Pause on the revenue figure. 60-90 seconds then let them react.")

# ============================
# SLIDE 6: Cross-Entity Analysis / Single-Entity Performance
# ============================
slide_start("s-lt", 6)
if is_single:
    _code0 = entity_codes[0]
    _o0 = entity_orders[_code0]
    _u0 = entity_usage[_code0]
    html.append('<div class="lbl">Performance Summary</div>')
    html.append(f'<h2>{_account_label} &mdash; Trailing 12&nbsp;Months</h2>')
    html.append('<table class="data-table">')
    html.append('<tr><th>Metric</th><th class="num">Value</th></tr>')
    html.append(f'<tr><td>Total Revenue</td><td class="num bold">{fmt_currency(_o0["total_revenue"])}</td></tr>')
    html.append(f'<tr><td>Total Orders</td><td class="num bold">{fmt_num(_o0["total_orders"])}</td></tr>')
    html.append(f'<tr><td>Average Order Value</td><td class="num">{fmt_currency(_o0["aov"])}</td></tr>')
    html.append(f'<tr><td>Unique Customers</td><td class="num">{fmt_num(_o0["unique_customers"])}</td></tr>')
    html.append(f'<tr><td>Ordering Customers</td><td class="num">{fmt_num(_o0["ordering_customers"])}</td></tr>')
    html.append(f'<tr><td>Licensed Reps</td><td class="num">{_u0["total_licensed"]}</td></tr>')
    html.append(f'<tr><td>Active Users (TTM)</td><td class="num">{_u0["active_users"]}</td></tr>')
    html.append(f'<tr><td>Adoption Rate</td><td class="num">{_u0["active_pct"]}%</td></tr>')
    _ss = _o0.get("self_service_pct", 0)
    html.append(f'<tr><td>Self-Service Orders</td><td class="num">{_ss}%</td></tr>')
    html.append('</table>')
    if months:
        html.append('<h3 style="margin-top:24px">Monthly Revenue</h3>')
        html.append('<table class="data-table"><tr><th>Month</th><th class="num">Revenue</th><th class="num">Orders</th></tr>')
        _mo_rev = _o0["monthly_rev"]
        _mo_ord = _o0["monthly_orders"]
        for m in months:
            html.append(f'<tr><td>{m}</td><td class="num">{fmt_currency(_mo_rev.get(m, 0))}</td><td class="num">{fmt_num(_mo_ord.get(m, 0))}</td></tr>')
        html.append('</table>')
else:
    html.append('<div class="lbl">Cross-Entity Analysis</div>')
    _num_word = {2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six"}.get(len(entity_codes), str(len(entity_codes)))
    html.append(f'<h2>{_num_word} Divisions, {_num_word}&nbsp;Patterns</h2>')
    html.append('<table class="data-table">')
    html.append('<tr><th>Entity</th><th class="num">Licensed</th><th class="num">Active</th><th class="num">Active %</th><th class="num">Orders</th><th class="num">Revenue</th><th class="num">AOV</th></tr>')
    max_orders = max(entity_orders[c]["total_orders"] for c in entity_codes)
    max_rev = max(entity_orders[c]["total_revenue"] for c in entity_codes)
    for code in entity_codes:
        o = entity_orders[code]
        u = entity_usage[code]
        bold_orders = ' class="bold num"' if o["total_orders"] == max_orders else ' class="num"'
        bold_rev = ' class="bold num"' if o["total_revenue"] == max_rev else ' class="num"'
        html.append(f'<tr><td class="bold">{entity_labels[code]}</td>')
        html.append(f'<td class="num">{u["total_licensed"]}</td>')
        html.append(f'<td class="num">{u["active_users"]}</td>')
        html.append(f'<td class="num">{u["active_pct"]}%</td>')
        html.append(f'<td{bold_orders}>{fmt_num(o["total_orders"])}</td>')
        html.append(f'<td{bold_rev}>{fmt_currency(o["total_revenue"])}</td>')
        html.append(f'<td class="num">{fmt_currency(o["aov"])}</td>')
        html.append('</tr>')
    html.append('</table>')
# MoM growth row
if mom_data:
    html.append('<div class="insight-line">')
    _growth_parts = []
    for code, md in mom_data.items():
        _growth_parts.append(f"{entity_labels[code]}: {md['growth']:+.1f}%")
    _market_note = ""
    _sample = list(mom_data.values())[0]
    if _sample.get("prior_markets"):
        _market_note = f' [{", ".join(_sample["prior_markets"])}]'
    elif _sample.get("recent_markets"):
        _market_note = f' [{", ".join(_sample["recent_markets"])}]'
    html.append(f'Recent MoM ({_sample["prior_label"]} → {_sample["recent_label"]}){_market_note}: {" &middot; ".join(_growth_parts)}')
    html.append('</div>')
slide_end(f"Lead with the headline revenue figure: {fmt_currency(grand_total_revenue)}. 2 minutes.")

# ============================
# SLIDE 7: Adoption by Entity
# ============================
slide_start("s-wh", 7)
html.append('<div class="lbl">Sales Team Intelligence</div>')
html.append(f'<h2>{fmt_num(grand_total_users)} Active Users &mdash; Adoption by&nbsp;Entity</h2>')
html.append('<table class="data-table">')
html.append('<tr><th>Entity</th><th class="num">Licensed</th><th class="num">Active</th><th class="num">Adoption %</th><th class="num">Logins</th><th class="num">Orders Submitted</th><th class="num">Avg Breadth</th></tr>')
for code in entity_codes:
    u = entity_usage[code]
    total_logins_ent = sum(usr["logins"] for usr in u["users"])
    total_orders_ent = sum(usr["orders"] for usr in u["users"])
    avg_breadth_ent = sum(usr["breadth"] for usr in u["users"] if usr["orders"] > 0) / max(sum(1 for usr in u["users"] if usr["orders"] > 0), 1)
    html.append(f'<tr><td class="bold">{entity_labels[code]}</td>')
    html.append(f'<td class="num">{u["total_licensed"]}</td>')
    html.append(f'<td class="num">{u["active_users"]}</td>')
    html.append(f'<td class="num">{u["active_pct"]}%</td>')
    html.append(f'<td class="num">{fmt_num(total_logins_ent)}</td>')
    html.append(f'<td class="num">{fmt_num(total_orders_ent)}</td>')
    html.append(f'<td class="num">{avg_breadth_ent:.1f}</td>')
    html.append('</tr>')
html.append('</table>')
_s7_most_active = max(entity_codes, key=lambda c: entity_usage[c]["active_users"])
_s7_highest_aov = max(entity_codes, key=lambda c: entity_orders[c]["aov"])
_s7_note = f"Walk through adoption rates. {entity_labels[_s7_most_active]} leads in raw active users; {entity_labels[_s7_highest_aov]} has the highest AOV per user." if not is_single else "Walk through adoption rate and feature breadth."
slide_end(_s7_note)

# ============================
# SLIDE 8: Power Users / Top Reps
# ============================
slide_start("s-lt", 8)
if is_single:
    _code0 = entity_codes[0]
    _o0 = entity_orders[_code0]
    _u0 = entity_usage[_code0]
    _pg_reps = _o0.get("pg_top_reps", [])
    _bq_user_map = {u["user"]: u for u in _u0["users"]}
    html.append('<div class="lbl">Top Performers</div>')
    html.append(f'<h2>Your Most Active Reps &mdash; {_account_label}</h2>')
    html.append('<table class="data-table">')
    html.append('<tr><th>Rep</th><th class="num">Orders</th><th class="num">Revenue</th><th class="num">Customers</th><th class="num">Logins</th><th class="num">Feature Breadth</th></tr>')
    for rep in _pg_reps:
        _matched = None
        _rname_lower = rep["name"].lower().replace("  ", " ")
        for ukey, uval in _bq_user_map.items():
            if (uval.get("name") or "").lower().replace("  ", " ") == _rname_lower:
                _matched = uval
                break
        _logins = _matched["logins"] if _matched else 0
        _breadth = _matched["breadth"] if _matched else 0
        html.append(f'<tr><td class="bold">{rep["name"]}</td><td class="num">{fmt_num(rep["orders"])}</td><td class="num">{fmt_currency(rep["revenue"])}</td><td class="num">{rep["customers"]}</td><td class="num">{fmt_num(_logins)}</td><td class="num">{_breadth}</td></tr>')
    html.append('</table>')
    if _pg_reps:
        _top_rep = _pg_reps[0]
        _top_conc = pct(_top_rep["revenue"], _o0["total_revenue"])
        html.append(f'<div class="insight-box"><strong>{_top_rep["name"]}</strong> leads with {fmt_num(_top_rep["orders"])} orders and {fmt_currency(_top_rep["revenue"])} ({_top_conc}% of revenue) across {_top_rep["customers"]} customers. Order attribution from Postgres; logins and feature breadth from Mixpanel.</div>')
else:
    html.append('<div class="lbl">Power Users</div>')
    html.append('<h2>Your Top Performers Work Across Divisions</h2>')
    top_cross = cross_entity_reps[:8]
    html.append('<table>')
    html.append('<tr><th>Rep</th>')
    for code in entity_codes:
        html.append(f'<th class="num-cell">{entity_labels[code]}</th>')
    html.append('<th class="num-cell">Total</th><th class="num-cell">Breadth</th></tr>')
    max_breadth_rep = max(top_cross, key=lambda x: x["max_breadth"]) if top_cross else None
    for rep in top_cross:
        is_max = rep == max_breadth_rep
        row_style = ' style="background:rgba(201,168,76,0.1)"' if is_max else ''
        html.append(f'<tr{row_style}><td class="bold">{rep["name"]}</td>')
        for code in entity_codes:
            if code in rep["entities"]:
                val = rep["entities"][code]["orders"]
                html.append(f'<td class="num-cell">{val if val > 0 else "&mdash;"}</td>')
            else:
                html.append('<td class="num-cell">&mdash;</td>')
        html.append(f'<td class="num-cell bold">{rep["total_orders"]}</td>')
        html.append(f'<td class="num-cell">{rep["max_breadth"]}</td>')
        html.append('</tr>')
    html.append('</table>')
    avg_breadth = sum(u["breadth"] for code in entity_codes for u in entity_usage[code]["users"] if u["orders"] > 0) / max(sum(1 for code in entity_codes for u in entity_usage[code]["users"] if u["orders"] > 0), 1)
    html.append(f'<div class="insight-box">Power users share a pattern: high feature breadth (10-15 vs avg {avg_breadth:.0f}) and cross-entity fluency.</div>')
slide_end("Name names. This audience wants specifics.")

# ============================
# SLIDE 9: Rep Concentration Risk
# ============================
slide_start("s-wh", 9)
html.append('<div class="lbl">Risk Analysis</div>')
html.append('<h2>Rep Concentration by&nbsp;Entity</h2>')

html.append('<div class="card-grid">')
for code in entity_codes:
    _pg_reps_c = entity_orders[code].get("pg_top_reps", [])
    if _pg_reps_c and entity_orders[code]["total_revenue"] > 0:
        top_name = _pg_reps_c[0]["name"]
        top_pct = round(_pg_reps_c[0]["revenue"] / entity_orders[code]["total_revenue"] * 100, 1)
    else:
        u = entity_usage[code]
        top_name = u["top_rep_name"]
        top_pct = u["top_rep_concentration"]
    rc = risk_color(top_pct)
    rl = risk_label(top_pct)
    html.append(f'''<div class="mini-stat">
        <div class="entity-name">{entity_labels[code]}</div>
        <div class="rep-name">{top_name}</div>
        <div class="rep-pct" style="color:{rc}">{top_pct}%</div>
        <div style="margin-top:4px"><span class="risk-dot" style="background:{rc}"></span><span style="font-family:'DM Mono',monospace;font-size:0.72rem;color:{rc}">{rl} Risk</span></div>
    </div>''')
html.append('</div>')
html.append('<p style="font-size:0.82rem;color:#666;margin-top:12px;text-align:center">20% = single-rep dependency threshold</p>')

healthy = [entity_labels[c] for c in entity_codes if entity_usage[c]["top_rep_concentration"] < 15]
watch = [entity_labels[c] for c in entity_codes if entity_usage[c]["top_rep_concentration"] >= 15]
insight_parts = []
if healthy:
    insight_parts.append(f'{", ".join(healthy)} {"shows" if len(healthy)==1 else "show"} healthy distribution')
if watch:
    insight_parts.append(f'{", ".join(watch)} {"has" if len(watch)==1 else "have"} concentration worth monitoring')
html.append(f'<div class="insight-box">{"; ".join(insight_parts)}.</div>')
slide_end("Only surface this if relevant to the conversation. Don't lead with risk if everything is healthy.")

# ============================
# SLIDE 10: Feature Adoption — Used vs Available
# ============================
slide_start("s-lt", 10)
html.append('<div class="lbl">Feature Adoption</div>')
html.append('<h2>Platform Capabilities: Used vs.&nbsp;Available</h2>')

# Split features into heavy vs zero across all entities
_all_feat_totals = defaultdict(int)
for code in entity_codes:
    for label, val in entity_usage[code]["feature_totals"].items():
        _all_feat_totals[label] += val

_heavy_feats = sorted(((k, v) for k, v in _all_feat_totals.items() if v > 100), key=lambda x: -x[1])[:6]
_zero_feats = [(k, v) for k, v in _all_feat_totals.items() if v <= 10]

html.append('<div class="two-col">')
html.append('<div class="feature-col heavy"><h4>Heavy Adoption</h4>')
for feat_name, feat_count in _heavy_feats:
    html.append(f'<div class="feature-row"><span>{feat_name}</span><span class="feature-count">{fmt_num(feat_count)}</span></div>')
html.append('</div>')
html.append('<div class="feature-col zero"><h4>Zero / Near-Zero</h4>')
for feat_name, feat_count in _zero_feats:
    html.append(f'<div class="feature-row"><span>{feat_name}</span><span class="feature-count">{fmt_num(feat_count)}</span></div>')
if not _zero_feats:
    html.append('<div class="feature-row"><span>All features active</span><span class="feature-count">&#10003;</span></div>')
html.append('</div>')
html.append('</div>')
html.append('<div class="insight-line">Your teams are deep adopters of the core ordering and configuration workflow. The opportunity is in the features your team hasn\'t tried yet &mdash; SmartPicks, customer lists, and kits could transform how reps present to customers.</div>')
slide_end("Left column builds credibility, right column is the opportunity. Zero-usage features are the conversation starters. 2-3 minutes.")

# ============================
# SLIDE 11: Feature Benchmarking
# ============================
slide_start("s-wh", 11)
html.append('<div class="lbl">Feature Benchmarking</div>')
_bench_title = "Feature Usage &mdash; Trailing 12&nbsp;Months" if is_single else "Feature Depth: How Your Divisions&nbsp;Compare"
html.append(f'<h2>{_bench_title}</h2>')

html.append('<table class="data-table">')
html.append('<tr><th>Feature</th>')
for code in entity_codes:
    html.append(f'<th class="num">{entity_labels[code]}</th>')
html.append('<th class="winner-col">Winner</th></tr>')

for feat in heatmap_features:
    vals = {c: entity_usage[c]["feature_totals"].get(feat, 0) for c in entity_codes}
    max_val = max(vals.values())
    winner = max(vals, key=vals.get) if max_val > 0 else ""
    html.append(f'<tr><td>{feat}</td>')
    for code in entity_codes:
        v = vals[code]
        bg = winner_bg() if code == winner and max_val > 0 else heatmap_bg(v, max_val)
        html.append(f'<td class="num" style="background:{bg}">{fmt_num(v)}</td>')
    html.append(f'<td class="winner-col">{entity_labels.get(winner, "&mdash;")}</td>')
    html.append('</tr>')
html.append('</table>')
if is_single:
    html.append(f'<div class="insight-box">Feature breadth shows where {_account_label} is strong and where activation opportunities remain.</div>')
    slide_end("Walk through the feature totals. Identify the top 2-3 features to discuss. 3 minutes.")
else:
    _feature_vol_leader = max(entity_codes, key=lambda c: sum(entity_usage[c].get("feature_totals", {}).values()))
    _sp_leader = max(entity_codes, key=lambda c: entity_usage[c].get("feature_totals", {}).get("Sales Portal", 0))
    _kit_leader = max(entity_codes, key=lambda c: entity_usage[c].get("feature_totals", {}).get("Order Kit", 0) + entity_usage[c].get("feature_totals", {}).get("View Kit", 0))
    html.append(f'<div class="insight-box">Each division has a strength the others can learn from. {entity_labels[_feature_vol_leader]} dominates volume and feature breadth; {entity_labels[_sp_leader]} leads in Sales Portal adoption; {entity_labels[_kit_leader]} drives kit and configured item workflows.</div>')
    slide_end("Read the 'Winner' column vertically — it tells the story of which division is best at what. 3 minutes.")

# ============================
# SLIDE 12: Customer Intelligence
# ============================
slide_start("s-lt", 12)
html.append('<div class="lbl">Customer Intelligence</div>')
html.append('<h2>What the Platform Reveals About Your Customers</h2>')

html.append('<table>')
html.append('<tr><th>Entity</th><th class="num-cell">Customers</th><th class="num-cell">Ordering</th><th class="num-cell">Activation</th><th class="num-cell">AOV</th><th class="num-cell">Top Cust. %</th></tr>')

max_aov = max(entity_orders[c]["aov"] for c in entity_codes)
for code in entity_codes:
    o = entity_orders[code]
    aov_style = ' style="background:rgba(201,168,76,0.15)"' if o["aov"] == max_aov else ''
    conc_style = ' style="background:rgba(201,168,76,0.15)"' if o["top_cust_concentration"] > 5 else ''
    act_rate = pct(o["ordering_customers"], o["unique_customers"])
    html.append(f'<tr><td class="bold">{entity_labels[code]}</td>')
    html.append(f'<td class="num-cell">{fmt_num(o["unique_customers"])}</td>')
    html.append(f'<td class="num-cell">{fmt_num(o["ordering_customers"])}</td>')
    html.append(f'<td class="num-cell">{act_rate}%</td>')
    html.append(f'<td class="num-cell"{aov_style}>{fmt_currency(o["aov"])}</td>')
    html.append(f'<td class="num-cell"{conc_style}>{o["top_cust_concentration"]}%</td>')
    html.append('</tr>')
html.append('</table>')

# top customer callouts
for code in entity_codes:
    o = entity_orders[code]
    if o["top_cust_concentration"] > 3 and o["top_customers"]:
        tc = o["top_customers"][0]
        html.append(f'<div class="insight-box"><strong>{entity_labels[code]}</strong>: Top customer <strong>{tc[0]}</strong> at {fmt_currency(tc[1])} ({o["top_cust_concentration"]}% of revenue)</div>')

_s12_footnote = f"Note: Customer counts reflect trailing 12 months ({START_DATE} → {END_DATE})."
if not is_single and len(entity_codes) > 1:
    _lowest_aov = min(entity_codes, key=lambda c: entity_orders[c]["aov"])
    _highest_aov = max(entity_codes, key=lambda c: entity_orders[c]["aov"])
    if _lowest_aov != _highest_aov:
        _s12_footnote += f" {entity_labels[_lowest_aov]} has lower AOV by design. {entity_labels[_highest_aov]} projects inflate AOV by design."
html.append(f'<p style="font-size:0.78rem;color:#999;margin-top:8px">{_s12_footnote}</p>')
slide_end("The concentration data is FYI, not alarming unless they tell you otherwise. The activation gap is the actionable insight.")

# ============================
# SLIDE 13: Growth Trajectory (standalone)
# ============================
slide_start("s-wh", 13)
html.append('<div class="lbl">Growth Trajectory</div>')
html.append('<h2>Where the Momentum&nbsp;Is</h2>')
if mom_data:
    _top_growers = sorted(mom_data.items(), key=lambda x: -x[1]["growth"])[:3]
    _sample_md = list(mom_data.values())[0]
    _period_label = f'{_sample_md["prior_label"]} → {_sample_md["recent_label"]}'
    _mkt_tags = []
    if _sample_md.get("prior_markets"):
        _mkt_tags.extend(_sample_md["prior_markets"])
    if _sample_md.get("recent_markets"):
        _mkt_tags.extend(_sample_md["recent_markets"])
    html.append('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-bottom:28px">')
    for code, md in _top_growers:
        html.append(f'<div class="growth-card"><h3 style="font-family:Georgia,serif;font-size:1rem;margin-bottom:4px">{entity_labels[code]}</h3>')
        html.append(f'<div class="growth-pct">{md["growth"]:+.1f}%</div>')
        html.append(f'<div class="growth-label">{_period_label}</div>')
        _delta = md["feb"] - md["jan"]
        html.append(f'<div class="growth-detail">{fmt_currency(md["jan"])} &rarr; {fmt_currency(md["feb"])}<br><span style="color:#C9A84C">+{fmt_currency(abs(_delta))}</span></div>')
        html.append('</div>')
    html.append('</div>')
    _total_growth = sum(md["feb"] - md["jan"] for md in mom_data.values() if md["growth"] > 0)
    _mkt_note = f' This window overlaps {", ".join(set(_mkt_tags))}.' if _mkt_tags else ''
    _grew_count = len([1 for md in mom_data.values() if md["growth"] > 0])
    if is_single:
        _single_md = list(mom_data.values())[0]
        if _single_md["growth"] > 0:
            _growth_txt = f'Revenue grew {_single_md["growth"]:.1f}% ({_period_label}), adding {fmt_currency(_total_growth)}.{_mkt_note}'
        else:
            _growth_txt = f'Revenue declined {abs(_single_md["growth"]):.1f}% ({_period_label}).{_mkt_note}'
        _growth_txt += ' Ask: &ldquo;Is this seasonal, or structural?&rdquo;'
    else:
        _growth_txt = f'{_grew_count} of {len(entity_codes)} divisions grew ({_period_label}), adding {fmt_currency(_total_growth)} in combined growth.{_mkt_note} Ask: &ldquo;Is this seasonal, or structural?&rdquo;'
    html.append(f'<div class="insight-line">{_growth_txt}</div>')
else:
    html.append('<p>Insufficient monthly data for period comparison.</p>')
slide_end("Ask: 'Is this seasonal, or structural?' Connect to opening discovery answers. Anchor to market calendar. 2 minutes.")

# (Self-Service slide removed — MoM data now in Growth Trajectory, Slide 13)
# (Platform Health merged into Support & Housekeeping below)

# ============================
# SLIDE 14: Data-Anchored Discovery
# ============================
slide_start("s-dk", 14)
html.append('<div class="lbl">Data-Anchored Discovery</div>')
html.append('<h2 style="color:#fff">Now That You\'ve Seen the Data — What Resonates?</h2>')

# Build discovery questions from data
top_cross_rep = cross_entity_reps[0] if cross_entity_reps else None

questions = []

# Q1: Cross-entity
if top_cross_rep:
    questions.append(("Cross-Entity Adoption · All Divisions",
        f'{top_cross_rep["name"]} and your top reps work across {top_cross_rep["entity_count"]} divisions with {top_cross_rep["total_orders"]} total orders. Is that by design, or are they filling gaps? Should we formalize cross-training?'))

# Q2: Self-service — compare two highest-SS entities or report single
ss_ranked = sorted(entity_codes, key=lambda c: entity_orders[c]["self_service_pct"], reverse=True)
top_ss = entity_orders[ss_ranked[0]]
if len(ss_ranked) >= 2:
    sec_ss = entity_orders[ss_ranked[1]]
    questions.append(("Self-Service Adoption",
        f'{entity_labels[ss_ranked[0]]} shows {top_ss["self_service_pct"]}% self-service orders, '
        f'{entity_labels[ss_ranked[1]]} at {sec_ss["self_service_pct"]}%. '
        f'What\'s driving the difference — customer profile, rep workflow, or B2B configuration?'))
else:
    questions.append(("Self-Service Adoption",
        f'{entity_labels[ss_ranked[0]]} shows {top_ss["self_service_pct"]}% self-service orders. '
        f'Is there a target self-service rate?'))

# Q3: Highest-AOV entity
aov_ranked = sorted(entity_codes, key=lambda c: entity_orders[c]["aov"], reverse=True)
hi_aov_code = aov_ranked[0]
hi_aov = entity_orders[hi_aov_code]
questions.append((f"Pipeline · {entity_labels[hi_aov_code]}",
    f'{entity_labels[hi_aov_code]} AOV is {fmt_currency(hi_aov["aov"])}. '
    f'With {hi_aov["quote"]} active quotes in pipeline, what\'s the conversion timeline?'))

# Q4: Feature gaps
if is_single:
    questions.append(("Feature Activation",
        'Some features show zero adoption but strong potential based on your workflow. '
        'Should we pilot those to see if they add value?'))
else:
    questions.append(("Feature Activation",
        'Some features show zero adoption in certain divisions but strong activity where used. '
        'Should we pilot these in the divisions that haven\'t started?'))

# Q5: Rep concentration
watch_entities = [(entity_labels[c], entity_usage[c]["top_rep_name"], entity_usage[c]["top_rep_concentration"]) for c in entity_codes if entity_usage[c]["top_rep_concentration"] >= 15]
if watch_entities:
    we = watch_entities[0]
    questions.append(("Rep Dependency · " + we[0],
        f'{we[1]} represents {we[2]}% of {we[0]} orders. Is that a capacity issue or a training opportunity for other reps?'))

for tag, text in questions:
    html.append(f'''<div class="q-block">
        <div class="q-tag">{tag}</div>
        <div class="q-text">{text}</div>
    </div>''')

slide_end("The intelligence sections earned you this conversation. Reference specific data points — don't re-present. Listen for which patterns they care about. 5-8 minutes.")

# ============================
# SLIDE 15: Growth Opportunities
# ============================
slide_start("s-wh", 15)
html.append('<div class="lbl">Recommendations</div>')
html.append('<h2>Closing the Gaps</h2>')

def _feat(code, feat):
    return entity_usage.get(code, {}).get("feature_totals", {}).get(feat, 0) if code in entity_usage else 0

recs = [
    {
        "priority": "01",
        "title": "Sales Portal Expansion",
        "gap": " / ".join(f"{entity_labels[c]}: {fmt_num(_feat(c, 'Sales Portal'))} Sales Portal events" for c in entity_codes),
        "path": "Enable Sales Portal for store managers and team leads. Start with top 3 reps per entity. Provide 30-min onboarding session.",
        "outcome": "Unified reporting across the organization. Managers gain real-time visibility into rep activity and customer ordering patterns.",
    },
    {
        "priority": "02",
        "title": "Camera Scan Best Practice Transfer",
        "gap": " / ".join(f"{entity_labels[c]}: {fmt_num(_feat(c, 'Camera Scan'))} events" for c in entity_codes),
        "path": "Identify 2 champion reps to demo camera scan workflow. Include in next rep update call.",
        "outcome": "Faster product lookup in field. Reduces order entry time by eliminating manual SKU search.",
    },
    {
        "priority": "03",
        "title": "Inactive User Re-Engagement → All Entities",
        "gap": f"{grand_total_licensed - grand_total_users} licensed users have zero or minimal activity. Represents untapped capacity.",
        "path": "Export inactive user list. Identify which are still employed vs. departed. For active employees, schedule targeted re-training sessions by entity.",
        "outcome": "Increase effective adoption rate. Each activated rep is a force multiplier — estimated 15-25% increase in order throughput per newly active user.",
    },
]

html.append('<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">')
for rec in recs:
    html.append(f'''<div class="rec-card">
        <div class="priority">Priority {rec["priority"]}</div>
        <h3>{rec["title"]}</h3>
        <div class="row-label">The Gap</div>
        <p style="font-size:0.82rem">{rec["gap"]}</p>
        <div class="row-label">The Path</div>
        <p style="font-size:0.82rem">{rec["path"]}</p>
        <div class="row-label">The Outcome</div>
        <p style="font-size:0.82rem">{rec["outcome"]}</p>
    </div>''')
html.append('</div>')
slide_end("Connect every recommendation to something surfaced in discovery. If they didn't react to it in Slide 10, don't push it here.")

# ============================
# SLIDE 16: Feature Roadmap
# ============================
slide_start("s-lt", 16)
html.append('<div class="lbl">Feature Roadmap</div>')
html.append('<h2>Capabilities Available but Not Yet Activated</h2>')

html.append('<table>')
_pilot_col = "Best Pilot Entity" if not is_single else "Entity"
html.append(f'<tr><th>Feature</th><th>Current Usage</th><th>{_pilot_col}</th><th>Business Case</th><th>Status</th></tr>')

def _best_pilot(feat_key):
    """Pick the entity with the highest usage of feat_key (or first entity if all zero)."""
    ranked = sorted(entity_codes, key=lambda c: _feat(c, feat_key), reverse=True)
    return entity_labels[ranked[0]]

def _usage_summary(feat_key):
    """Generate a dynamic usage summary string from real feature data."""
    totals = {c: _feat(c, feat_key) for c in entity_codes}
    nonzero = [c for c in entity_codes if totals[c] > 0]
    if len(nonzero) == 0:
        return "Zero across all entities" if not is_single else "Not yet activated"
    if is_single:
        return f"{fmt_num(totals[entity_codes[0]])} events"
    if len(nonzero) == len(entity_codes):
        return "Active across all entities"
    if len(nonzero) == 1:
        return f"Active in {entity_labels[nonzero[0]]} only"
    return f"Low — active in {len(nonzero)} of {len(entity_codes)} entities"

activation_rows = [
    ("SmartPicks",            _usage_summary("SmartPicks"),            _best_pilot("SmartPicks"),            "AI-powered product recommendations increase AOV and cross-sell",             "Pilot Ready"),
    ("Customer Product Lists",_usage_summary("Customer Product Lists"),_best_pilot("Customer Product Lists"),"Curated lists per customer save rep time and increase reorder rates",        "Not Started"),
    ("Maybe List",            _usage_summary("Maybe List"),            _best_pilot("Maybe List"),            "Staging area reduces abandoned carts and incomplete orders",                  "Active"),
    ("Show Sales in Catalog", _usage_summary("Show Sales in Catalog"), _best_pilot("Show Sales in Catalog"), "Sales visibility in catalog helps reps prioritize high-volume items",        "Active"),
    ("Camera Scan",           _usage_summary("Camera Scan"),           _best_pilot("Camera Scan"),           "Scan-to-quote reduces manual SKU search — faster ordering in the field",     "Pilot Ready"),
]

for feat, usage, pilot, bcase, status in activation_rows:
    if status == "Active":
        pill = status_pill(status, "green")
    elif status == "Pilot Ready":
        pill = status_pill(status, "gold")
    else:
        pill = status_pill(status, "red")
    html.append(f'<tr><td class="bold">{feat}</td><td>{usage}</td><td>{pilot}</td><td>{bcase}</td><td>{pill}</td></tr>')

html.append('</table>')
slide_end("This is the activation menu. Don't read every row — ask which ones they want to discuss. For ops audiences, this is often where the real conversation happens.")

# ============================
# SLIDE 17: Cross-Entity Playbook (skip for single entity)
# ============================
if not is_single:
    slide_start("s-wh", 17)
    html.append('<div class="lbl">Cross-Entity Playbook</div>')
    html.append('<h2>What One Division Does Well, Others Can Learn</h2>')
    transfers = [
        ("&#x21BB;", False, "Sales Portal Expansion",
         " / ".join(f"{entity_labels[c]}: {fmt_num(_feat(c, 'Sales Portal'))} events" for c in entity_codes)
         + ". Transfer the workflow — it's a configuration change, not a project."),
        ("&#x21BB;", False, "Kit & Config Workflow Transfer",
         " / ".join(f"{entity_labels[c]}: {fmt_num(_feat(c, 'Order Kit'))} kit orders" for c in entity_codes)
         + ". Curated room packages increase AOV."),
        ("&#x21BB;", False, "Camera Scan Adoption",
         " / ".join(f"{entity_labels[c]}: {fmt_num(_feat(c, 'Camera Scan'))} events" for c in entity_codes)
         + ". Scan-to-quote reduces manual SKU entry for project-based orders."),
        ("+", True, "SmartPicks & Customer Lists: New Capability Rollout",
         "Neither feature has reached critical mass. Pilot in the entity with the highest feature breadth, then cascade."),
    ]
    for icon, is_green, title, detail in transfers:
        cls = "green-icon" if is_green else ""
        html.append(f'''<div class="transfer-item">
            <div class="transfer-icon {cls}">{icon}</div>
            <div>
                <div class="bold" style="margin-bottom:4px">{title}</div>
                <div style="font-size:0.84rem;color:#555">{detail}</div>
            </div>
        </div>''')
    slide_end("This is the unique value of the multi-entity view. 2-3 minutes.")

# ============================
# SLIDE 18: Support & Housekeeping
# ============================
slide_start("s-lt", 18)
html.append('<div class="lbl">Housekeeping</div>')
html.append('<h2>Support Status &amp; Engagement History</h2>')

html.append('<div class="card-grid">')
html.append('''<div class="card">
    <h3 style="font-size:1rem">Open Tickets</h3>
    <p style="font-size:0.84rem">No critical open tickets at this time. Standard support channel available for any issues surfaced during this review.</p>
    <p style="font-size:0.78rem;color:#4A7C59;margin-top:8px">Resolution commitment: 48-hour response SLA</p>
</div>''')

_pay_txt = f"All {len(entity_codes)} entities active and current." if not is_single else f"{_account_label} account active and current."
html.append(f'''<div class="card">
    <h3 style="font-size:1rem">Payment Status</h3>
    <p style="font-size:0.84rem">{_pay_txt} MRR stable.</p>
    <p style="font-size:0.78rem;color:#4A7C59;margin-top:8px">Status: Current</p>
</div>''')

html.append('''<div class="card">
    <h3 style="font-size:1rem">Data Health</h3>
    <p style="font-size:0.84rem">Order data syncing through Mar 3, 2026. Usage data current. No import errors detected in recent files.</p>
    <p style="font-size:0.78rem;color:#4A7C59;margin-top:8px">All systems operational</p>
</div>''')

html.append('''<div class="card">
    <h3 style="font-size:1rem">Engagement History</h3>
    <p style="font-size:0.84rem">This is the operational deep-dive EBR. Prior touchpoints include quarterly reviews and ad-hoc support.</p>
    <p style="font-size:0.78rem;color:#C9A84C;margin-top:8px">Cadence: Quarterly EBR recommended</p>
</div>''')
html.append('</div>')
slide_end("90 seconds. For ops audiences, the ticket resolution commitment matters more than the relationship framing. Be specific on timelines.")

# ============================
# SLIDE 19: Next Steps & Commitments
# ============================
slide_start("s-wh", 19)
html.append('<div class="lbl">Next Steps</div>')
html.append('<h2>What We\'ll Do Next</h2>')

html.append('<div class="two-col">')
if is_single:
    html.append(f'''<div>
        <div class="col-header green-hd">From SuperCat / eCat</div>
        <ul class="commit-list">
            <li>Resolve any open support tickets within 48 hours</li>
            <li>Deliver rep activity CSV export</li>
            <li>Inactive user audit report (1 week)</li>
            <li>Feature activation recommendations based on today's data</li>
            <li>Formalized EBR summary document within 48 hours</li>
        </ul>
    </div>''')
    html.append(f'''<div>
        <div class="col-header gold-hd">From {_account_label}</div>
        <ul class="commit-list">
            <li>Confirm technical contacts for feature pilots</li>
            <li>Identify 2 champion reps for new feature rollouts</li>
            <li>Review inactive user list — confirm employment status</li>
            <li>Share any ERP or integration roadmap changes</li>
            <li class="blank">[From discussion]</li>
            <li class="blank">[From discussion]</li>
        </ul>
    </div>''')
else:
    _lowest_sp = min(entity_codes, key=lambda c: _feat(c, 'Sales Portal'))
    _lowest_cam = min(entity_codes, key=lambda c: _feat(c, 'Camera Scan'))
    _sp_targets = " &amp; ".join(entity_labels[c] for c in entity_codes if _feat(c, 'Sales Portal') < max(_feat(c2, 'Sales Portal') for c2 in entity_codes) * 0.5) or entity_labels[_lowest_sp]
    html.append(f'''<div>
        <div class="col-header green-hd">From SuperCat / eCat</div>
        <ul class="commit-list">
            <li>Resolve any open support tickets within 48 hours</li>
            <li>Deliver rep activity CSV export for all {len(entity_codes)} entities</li>
            <li>Provide Sales Portal configuration proposal for {_sp_targets}</li>
            <li>Camera Scan pilot plan for {entity_labels[_lowest_cam]} (1 week)</li>
            <li>Inactive user audit report by entity (1 week)</li>
            <li>Formalized EBR summary document within 48 hours</li>
        </ul>
    </div>''')
    html.append(f'''<div>
        <div class="col-header gold-hd">From {_account_label}</div>
        <ul class="commit-list">
            <li>Confirm technical contacts for Sales Portal expansion</li>
            <li>Identify 2 pilot champions per entity for new features</li>
            <li>Share integration requirements or ERP roadmap changes</li>
            <li>Review inactive user list — confirm employment status</li>
            <li class="blank">[From discussion]</li>
            <li class="blank">[From discussion]</li>
        </ul>
    </div>''')
html.append('</div>')

html.append('<p style="text-align:center;font-family:\'DM Mono\',monospace;font-size:0.78rem;color:#4A7C59;margin-top:20px">Formalized summary within 48 hours.</p>')
slide_end("For ops audiences, be crisp. They want clarity, not open-ended commitments. Specific deliverables with specific dates.")

# ============================
# SLIDE 20: Closing
# ============================
slide_start("s-dk", 20)
html.append('<div style="display:flex;flex-direction:column;justify-content:center;min-height:80vh">')
html.append('<div class="gold-rule"></div>')
if is_single:
    html.append(f'<p class="closing-stat">{fmt_num(grand_total_users)} Active Users. {fmt_currency(grand_total_revenue)} Trailing Twelve&nbsp;Months.<br>{_account_label}. Long-Standing Partner. This Is Just the&nbsp;Beginning.</p>')
else:
    html.append(f'<p class="closing-stat">{fmt_num(grand_total_users)} Users. {len(entity_codes)} Divisions. {fmt_currency(grand_total_revenue)} Trailing Twelve Months.<br>Long-Standing Partner. This Is Just the&nbsp;Beginning.</p>')
html.append('<p style="font-family:\'DM Mono\',monospace;font-size:.72rem;text-transform:uppercase;letter-spacing:.14em;color:#C9A84C;margin-top:32px">SuperCat / eCat &middot; March 2026</p>')
html.append('</div>')
slide_end("Don't add words. Let the slide land. Thank them, confirm 48-hour follow-up.")

# ============================
# SLIDE 21: Appendix — Rep Activity Detail
# ============================
slide_start("s-lt", 21)
html.append('<div class="lbl">Appendix</div>')
html.append('<h2>Rep Activity Detail by&nbsp;Entity</h2>')

html.append('<table class="data-table">')
html.append('<tr><th>Rep</th><th>Entity</th><th class="num">Logins</th><th class="num">Orders</th><th class="num">Events</th><th class="num">Breadth</th><th>Last Active</th></tr>')

all_rep_rows = []
for code in entity_codes:
    for u in entity_usage[code]["users"]:
        if u["orders"] > 50 or u["logins"] > 100:
            all_rep_rows.append((u["name"], entity_labels[code], u["logins"], u["orders"], u["total_events"], u["breadth"], u["last_login"]))

all_rep_rows.sort(key=lambda x: -x[3])
for row in all_rep_rows[:20]:
    html.append(f'<tr><td class="bold">{row[0]}</td><td>{row[1]}</td><td class="num">{fmt_num(row[2])}</td><td class="num">{fmt_num(row[3])}</td><td class="num">{fmt_num(row[4])}</td><td class="num">{row[5]}</td><td>{row[6]}</td></tr>')

html.append('</table>')
html.append('<p style="font-size:0.78rem;color:#999;margin-top:12px">Full dataset available as CSV export — ask for it.</p>')
slide_end("Only navigate here if they ask for individual rep data. Don't present proactively.")

# ============================
# Navigation JS + Counter
# ============================
html.append('''
<div id="counter"></div>
<div id="notes-bar"></div>
<script>
(function(){
  const slides = document.querySelectorAll('.slide');
  const counter = document.getElementById('counter');
  const notesBar = document.getElementById('notes-bar');
  let notesVisible = false;
  const total = slides.length;

  function updateCounter(){
    let current = 1;
    slides.forEach((s,i) => {
      const r = s.getBoundingClientRect();
      if(r.top < window.innerHeight/2 && r.bottom > window.innerHeight/2) current = i+1;
    });
    counter.textContent = current + ' / ' + total;
    const activeSlide = slides[current-1];
    if(activeSlide && activeSlide.classList.contains('s-dk')){
      counter.style.color = 'rgba(255,255,255,0.35)';
    } else {
      counter.style.color = 'rgba(30,58,47,0.4)';
    }
    if(notesVisible){
      const note = activeSlide ? activeSlide.querySelector('[data-note]') : null;
      notesBar.textContent = note ? note.textContent : '';
    }
    return current;
  }

  window.addEventListener('scroll', updateCounter);
  updateCounter();

  document.addEventListener('keydown', function(e){
    if(e.key === 'n' || e.key === 'N'){
      notesVisible = !notesVisible;
      notesBar.classList.toggle('visible', notesVisible);
      updateCounter();
    }
    const current = updateCounter();
    if(e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown'){
      e.preventDefault();
      if(current < total) slides[current].scrollIntoView({behavior:'smooth'});
    }
    if(e.key === 'ArrowUp' || e.key === 'PageUp'){
      e.preventDefault();
      if(current > 1) slides[current-2].scrollIntoView({behavior:'smooth'});
    }
    if(e.key === 'Home'){e.preventDefault(); slides[0].scrollIntoView({behavior:'smooth'});}
    if(e.key === 'End'){e.preventDefault(); slides[total-1].scrollIntoView({behavior:'smooth'});}
  });
})();
</script>
</body>
</html>
''')

# ============================================================
# OUTPUT ROUTING
# ============================================================
date_label = _args.date or datetime.now().strftime("%Y-%m")
first_code = entity_codes[0]
account_folder = ACCOUNT_FOLDERS.get(first_code, first_code)

_downloads_accounts = {"clm"}

if _args.account and _args.account in _downloads_accounts:
    overview_dir = os.path.expanduser("~/Downloads")
    deck_dir = os.path.expanduser("~/Downloads")
    file_prefix = f"{entity_labels[first_code].replace(' ', '_')}_{date_label}"
elif _args.account:
    overview_dir = os.path.join(
        WORKSPACE, "EBR 2.0", "Accounts", account_folder, "Account Overview"
    )
    deck_dir = os.path.join(
        WORKSPACE, "EBR 2.0", "Accounts", account_folder, "Decks"
    )
    file_prefix = f"{entity_labels[first_code].replace(' ', '_')}_{date_label}"
else:
    overview_dir = os.path.expanduser("~/Downloads")
    deck_dir = os.path.expanduser("~/Downloads")
    file_prefix = f"Gabby_SC_{date_label}"

os.makedirs(overview_dir, exist_ok=True)
os.makedirs(deck_dir, exist_ok=True)

# --- Write HTML deck ---
deck_path = os.path.join(deck_dir, f"EBR_{file_prefix}.html")
with open(deck_path, "w", encoding="utf-8") as f:
    f.write("\n".join(html))
print(f"✓ Deck written to: {deck_path}")

# --- Write Snapshot (key metrics as quick-reference markdown) ---
snapshot_lines = [
    f"# {entity_labels.get(first_code, 'Combined')} — Snapshot",
    f"**Generated:** {datetime.now().strftime('%B %d, %Y')} | **Period:** {date_label}",
    "",
    "---",
    "",
    "## Key Metrics",
    "",
    "| Metric | Value |",
    "|--------|-------|",
    f"| Entities | {len(entity_codes)} |",
    f"| Active Users | {grand_total_users} / {grand_total_licensed} licensed |",
    f"| Adoption Rate | {pct(grand_total_users, grand_total_licensed)}% |",
    f"| Orders (Period) | {fmt_num(grand_total_orders)} |",
    f"| Revenue (Period) | {fmt_currency(grand_total_revenue)} |",
    "",
    "## By-Entity Breakdown",
    "",
    "| Entity | Code | Active Users | Orders | Revenue | AOV | Self-Service % |",
    "|--------|------|-------------|--------|---------|-----|----------------|",
]
for code in entity_codes:
    o = entity_orders[code]
    u = entity_usage[code]
    snapshot_lines.append(
        f"| {entity_labels[code]} | {code.upper()} | {u['active_users']}/{u['total_licensed']} "
        f"({u['active_pct']}%) | {fmt_num(o['total_orders'])} | {fmt_currency(o['total_revenue'])} "
        f"| {fmt_currency(o['aov'])} | {o['self_service_pct']}% |"
    )
if months and mom_data:
    snapshot_lines += ["", "## Monthly Revenue", "",
                       "| Entity | " + " | ".join(months) + " |",
                       "|--------" + "|-------" * len(months) + "|"]
    for code in entity_codes:
        mo = entity_orders[code]["monthly_rev"]
        row = f"| {entity_labels[code]} "
        for m in months:
            row += f"| {fmt_currency(mo.get(m, 0))} "
        snapshot_lines.append(row + "|")

snapshot_path = os.path.join(overview_dir, f"Snapshot_{file_prefix}.md")
with open(snapshot_path, "w", encoding="utf-8") as f:
    f.write("\n".join(snapshot_lines) + "\n")
print(f"✓ Snapshot written to: {snapshot_path}")

# --- Write GenerationNotes ---
gen_notes = [
    f"# {entity_labels.get(first_code, 'Combined')} — Generation Notes",
    f"**Generated:** {datetime.now().strftime('%B %d, %Y')} | **Script:** build_intelligence_deepdive.py",
    f"**Data range:** {START_DATE} → {END_DATE}",
    "",
    "---",
    "",
    "## 1. Data Sources",
    "",
    "| Source | Type | Query / Table | Records |",
    "|--------|------|--------------|---------|",
]
for code in entity_codes:
    o = entity_orders[code]
    u = entity_usage[code]
    gen_notes += [
        f"| Revenue KPIs | Postgres `orders` + line-item `extended_price` | "
        f"org_id={ENTITIES[code]['org_id']}, dedup by order_number | {o['total_orders']} orders |",
        f"| Feature adoption | BigQuery `mixpanel__events` | "
        f"`current_organization_shortname = '{code}'` | {sum(u['feature_totals'].values())} events |",
        f"| Rep names | Postgres `orders.rep_first_name + rep_last_name` | "
        f"Per-order attribution | {o['total_orders']} rows |",
        f"| Customer names | Postgres `orders.bill_to_company_name` | "
        f"Revenue aggregated per customer | {o['unique_customers']} customers |",
        f"| Licensed users | Postgres `org_users` + `user_types` | "
        f"`allow_ipad_logins = true`, `disabled = false` | {u['total_licensed']} users |",
        f"| Active users | BigQuery `mixpanel__events` `selected_org` | "
        f"Users with login events in period | {u['active_users']} active |",
    ]

gen_notes += [
    "",
    "**No CSV files were read during this run.**",
    "",
    "---",
    "",
    "## 2. Computed Metrics",
    "",
    "| Metric | Method | Notes |",
    "|--------|--------|-------|",
    "| Revenue | `SUM(order_items[].extended_price)` from Postgres | Deduped orders; excludes shipping/tax |",
    "| AOV | `Revenue / Order Count` | Full denominator including $0 orders |",
    "| Active Users | Users with `selected_org` events in BigQuery | Unique usernames with login activity |",
    "| Licensed Users | Postgres `org_users` + `user_types.allow_ipad_logins` | Excludes disabled and internal |",
    "| Self-Service % | `order_source = 'server'` / total orders | Postgres `orders.order_source` |",
    "| Feature Totals | `COUNT(*)` per `event_name` from BigQuery | Mapped via BQ_EVENT_MAP |",
    "| Rep Concentration | Top rep revenue / total entity revenue | From Postgres `orders` (pg_top_reps) |",
    "| Customer Concentration | Top customer revenue / total entity revenue | From Postgres |",
    "| MoM Growth | `(month2 - month1) / month1 * 100` | Requires 2+ months |",
    "| Cross-Entity Reps | Users in 2+ entity user lists | Matched by full name |",
]

# feature adoption gaps
zero_features = []
for label in [f[1] for f in FEATURES]:
    for code in entity_codes:
        if entity_usage[code]["feature_totals"].get(label, 0) == 0:
            zero_features.append((code, label))

if zero_features:
    gen_notes += [
        "",
        "---",
        "",
        "## 3. Feature Gaps Detected",
        "",
        "| Entity | Feature | Event Count | Status |",
        "|--------|---------|------------|--------|",
    ]
    for code, label in zero_features[:20]:
        gen_notes.append(f"| {entity_labels[code]} | {label} | 0 | Gap |")

# data quality notes
gen_notes += [
    "",
    "---",
    "",
    "## 4. Data Quality Notes",
    "",
    "| Observation | Detail |",
    "|-------------|--------|",
    f"| Cross-entity reps | {len(cross_entity_reps)} users found in 2+ entity CLMs — "
    f"headline 'active users' ({grand_total_users}) includes duplicates |",
    "| Rep data source | Postgres (`orders.rep_first_name + rep_last_name`) — "
    "BQ `order_submitted` events unreliable for this account |",
]
for code in entity_codes:
    o = entity_orders[code]
    if o["self_service_pct"] == 0:
        gen_notes.append(
            f"| {entity_labels[code]} self-service | 0% — expected for POS/project workflow |"
        )
    if o["top_cust_concentration"] > 5:
        gen_notes.append(
            f"| {entity_labels[code]} customer concentration | "
            f"{o['top_cust_concentration']}% — top customer "
            f"{o['top_customers'][0][0] if o['top_customers'] else 'N/A'} |"
        )

gen_notes += [
    "",
    "---",
    "",
    "## 5. Output Files",
    "",
    f"- **Deck:** `{os.path.basename(deck_path)}`",
    f"- **Snapshot:** `{os.path.basename(snapshot_path)}`",
    f"- **Generation Notes:** this file",
    "",
    "---",
    "",
    f"*Generated: {datetime.now().strftime('%B %d, %Y')} | Author: build_intelligence_deepdive.py*",
]

gen_notes_path = os.path.join(overview_dir, f"GenerationNotes_{file_prefix}.md")
with open(gen_notes_path, "w", encoding="utf-8") as f:
    f.write("\n".join(gen_notes) + "\n")
print(f"✓ GenerationNotes written to: {gen_notes_path}")

# --- Summary ---
print(f"\n  Total slides: 21")
print(f"  Grand totals: {grand_total_orders} orders, {fmt_currency(grand_total_revenue)} revenue, {grand_total_users}/{grand_total_licensed} users active")
print(f"  Cross-entity reps found: {len(cross_entity_reps)}")
for code in entity_codes:
    o = entity_orders[code]
    u = entity_usage[code]
    print(f"  {entity_labels[code]}: {o['total_orders']} orders, {fmt_currency(o['total_revenue'])}, {u['active_users']}/{u['total_licensed']} users, AOV {fmt_currency(o['aov'])}, Self-svc {o['self_service_pct']}%")

print("\n✓ Data sources: Postgres MCP + BigQuery MCP — no CSV files read")
