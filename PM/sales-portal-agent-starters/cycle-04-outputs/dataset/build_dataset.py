#!/usr/bin/env python3
"""Generate the stamped dataset behind sales-portal-client-review-v2.html.

Implements the single-dataset rule from CLIENT-REVIEW-HTML-BRIEF.md §3: the
artifact loads exactly one dataset of atomic rows and derives every figure from
it in the page. No total is ever stored that is also displayed for invoice-
derived heroes. Team and settings are reconciled snapshots (config / activity),
gated by independent control queries the same way invoices are.

Metric law (CLIENT-REVIEW-HTML-BRIEF.md §7):
    sales / invoiced = SUM(portal_invoices.net_amount)
    clamped to report_through_date, $5,000,000 per-row sanity cap,
    confidence ceiling STRONG (never FULL)
    backlog ≠ sales; quotes ≠ sales

Masking (§6, §7) is applied here at generation, never in the HTML. The
real -> synthetic map is written outside design-system/ and must not be
committed alongside the artifact.

Usage:
    python3 build_dataset.py --org wwjc --since 2025-01-01
    python3 build_dataset.py --org wwjc --since 2025-01-01 --no-mask
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[3]  # SuperCat 4.0/
ARTIFACT_DIR = WORKSPACE / "design-system" / "app"
SALT_FILE = HERE / ".mask_salt"
MAP_FILE = HERE / "mask_map.private.json"
FEATURES_RB = Path(
    "/Users/kylorjohnson/supercat-code/supercat_server/config/initializers/enabled_features.rb"
)

ORDER_CAP = 5_000_000
CONFIDENCE_CEILING = "STRONG"

# Feature flags surfaced in Settings → Experiments / Reports (human labels only).
FEATURE_LABELS = {
    "advanced_reports": "Advanced reports",
    "portal_portal": "Territory dashboard",
    "eol_customer_graph": "Customer sales graph",
    "link_to_customer_dashboard": "Customer dashboard link",
    "force_portal_display": "Force portal display",
    "backlog_instead_of_amount_invoiced": "Orders page shows backlog instead of invoiced",
    "enable_disable_portal_export_by_user_group": "Export gated by user group",
    "eol_dashboard_filters": "Dashboard filters (legacy flag)",
    "tcgc_name_fields": "TCGC name fields (legacy flag)",
    "allow_user_group_from_selecting_price_levels": "Price-level select (legacy flag)",
    "sales_quotas": "Sales quotas flag",
    "option_mapping": "Option mapping flag",
    "avery_5392_landscape": "Avery 5392 landscape labels",
    "xlsx_export": "XLSX export",
    "territory_access_via_rep_number": "Territory match via rep number",
}

DEAD_FLAGS = {
    "eol_dashboard_filters",
    "tcgc_name_fields",
    "allow_user_group_from_selecting_price_levels",
    "sales_quotas",
    "option_mapping",
}

SYNCHING_LABEL = {"a": "All customers", "o": "Associated customers", "n": "None", "s": "Associated"}


# ── connection ──────────────────────────────────────────────────────────────

def make_runner():
    """Return a callable(sql) -> list[dict], preferring a direct DB connection."""
    dsn = os.environ.get("DATABASE_URL")
    if dsn or os.environ.get("PGHOST"):
        try:
            import psycopg2
            import psycopg2.extras

            conn = psycopg2.connect(dsn) if dsn else psycopg2.connect(
                host=os.environ.get("PGHOST", "localhost"),
                port=int(os.environ.get("PGPORT", "5432")),
                dbname=os.environ.get("PGDATABASE", "supercatprod"),
                user=os.environ.get("PGUSER", ""),
                password=os.environ.get("PGPASSWORD", ""),
            )
            conn.set_session(readonly=True, autocommit=True)

            def run_pg(sql: str):
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    cur.execute(sql)
                    return [dict(r) for r in cur.fetchall()]

            print("source: psycopg2 (DATABASE_URL/PG*)", file=sys.stderr)
            return run_pg
        except Exception as exc:
            print(f"psycopg2 unavailable ({exc}); falling back to MCP", file=sys.stderr)

    import mcp_sql

    session = mcp_sql.connect()
    print("source: Postgres MCP (read-only, VPN)", file=sys.stderr)
    return session.execute_sql


# ── masking ─────────────────────────────────────────────────────────────────

ADJ = [
    "Alder", "Ambleside", "Ashcroft", "Ashford", "Bellhaven", "Birchwood",
    "Blackstone", "Briarwood", "Brookfield", "Cedarline", "Clayborne", "Coventry",
    "Cranbrook", "Draycott", "Dovetail", "Eastgate", "Elmsworth", "Fairmont",
    "Fallbrook", "Glenrock", "Granville", "Greystone", "Harborview", "Hartfield",
    "Havenwood", "Highgate", "Hollowell", "Ironwood", "Kingsley", "Kirkstone",
    "Langford", "Larkspur", "Laurelton", "Linden", "Marbury", "Meridian",
    "Millbrook", "Northfield", "Oakhurst", "Old Mill", "Pemberton", "Pinehurst",
    "Quarry", "Ravenswood", "Redfern", "Ridgeway", "Rosemont", "Saltmarsh",
    "Sandstone", "Shorewood", "Silverbirch", "Stonebridge", "Summerfield",
    "Thatcher", "Thornbury", "Tidewater", "Underhill", "Vandermeer", "Waverly",
    "Wellsley", "Westbrook", "Wharton", "Whitmore", "Willowbank", "Windermere",
    "Winterbourne", "Woodmere", "Yardley", "Abbotsford", "Barrowfield",
    "Chandlery", "Deepwater",
]
NOUN = [
    "Interiors", "Home", "Furnishings", "Design", "Living", "Galleries",
    "Trading", "Collection", "Studio", "Décor", "Furniture", "House",
    "Home Furnishings", "Fine Furniture", "Interior Design", "Design Studio",
    "Home Store", "Furniture Gallery", "Home Collection", "Interiors Studio",
    "Design House", "Home Design", "Furniture Studio", "Décor Studio",
    "Home Gallery", "Design Gallery",
]
PATTERNS = ["{a} {b}", "{a} {b} Co.", "The {a} {b}", "{a} {b} Group"]
SURNAME = [
    "Ashby", "Bramwell", "Carrington", "Delacroix", "Ellsworth", "Fairbanks",
    "Grayson", "Hollister", "Inglewood", "Jardine", "Kensington", "Lindqvist",
    "Marchetti", "Norwood", "Ottoline", "Pruitt", "Rennick", "Sandoval",
    "Thorne", "Vasquez", "Whitfield", "Yarrow", "Bellamy", "Calloway",
    "Duquesne", "Everly", "Fontaine", "Halloran", "Ivers", "Kirkland",
]
AGENCY = ["Group", "& Associates", "Sales Co.", "Partners", "Rep Group", "LLC"]


def load_salt() -> bytes:
    if SALT_FILE.exists():
        return SALT_FILE.read_bytes()
    salt = secrets.token_bytes(32)
    SALT_FILE.write_bytes(salt)
    SALT_FILE.chmod(0o600)
    print(f"created new mask salt at {SALT_FILE}", file=sys.stderr)
    return salt


def digest(salt: bytes, value: str) -> int:
    return int.from_bytes(
        hmac.new(salt, value.encode("utf-8"), hashlib.sha256).digest()[:8], "big"
    )


class Masker:
    """Deterministic, salt-stable pseudonyms so a returning client sees the same
    accounts across sessions. Disabled entirely with --no-mask."""

    def __init__(self, salt: bytes, enabled: bool = True):
        self.salt = salt
        self.enabled = enabled
        self.map: dict[str, dict] = {
            "customers": {}, "territories": {}, "reps": {},
        }
        self._used: set[str] = set()

    @staticmethod
    def _compose(idx: int) -> str:
        a = ADJ[idx % len(ADJ)]
        b = NOUN[(idx // len(ADJ)) % len(NOUN)]
        pat = PATTERNS[(idx // (len(ADJ) * len(NOUN))) % len(PATTERNS)]
        return pat.format(a=a, b=b)

    def _unique(self, seed: int) -> str:
        space = len(ADJ) * len(NOUN) * len(PATTERNS)
        for k in range(space):
            name = self._compose((seed + k) % space)
            if name not in self._used:
                self._used.add(name)
                return name
        raise SystemExit("pseudonym space exhausted; widen ADJ/NOUN/PATTERNS")

    def customer(self, code: str, real_name: str) -> tuple[str, str]:
        if not self.enabled:
            return code, (real_name or code)
        if code in self.map["customers"]:
            e = self.map["customers"][code]
            return e["key"], e["name"]
        name = self._unique(digest(self.salt, "cust:" + code))
        key = str(900000 + (len(self.map["customers"]) + 1))
        self.map["customers"][code] = {"key": key, "name": name, "real_name": real_name}
        return key, name

    def territory(self, code: str, index: int) -> str:
        if not self.enabled:
            return code
        if code in self.map["territories"]:
            return self.map["territories"][code]["label"]
        h = digest(self.salt, "terr:" + code)
        person = SURNAME[h % len(SURNAME)]
        suffix = AGENCY[(h >> 8) % len(AGENCY)]
        label = f"T-{index:02d} · {person} {suffix}".replace("  ", " ")
        self.map["territories"][code] = {"label": label, "real_code": code}
        return label

    def rep(self, code: str) -> str:
        """Return a masked rep label (Rep 015 style). Never a person name."""
        code = (code or "").strip() or "—"
        if not self.enabled:
            return f"Rep {code}"
        if code in self.map["reps"]:
            return self.map["reps"][code]["label"]
        h = digest(self.salt, "rep:" + code)
        label = f"Rep {(h % 900) + 100:03d}"
        self.map["reps"][code] = {"label": label, "real_code": code}
        return label

    def write_map(self, path: Path, meta: dict) -> None:
        if not self.enabled:
            return
        payload = {
            "_warning": "Contains the real->synthetic mapping. Never commit next to the artifact; never send to a client.",
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "meta": meta,
            **self.map,
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        path.chmod(0o600)


# ── feature-flag YAML (deploy config, not DB) ───────────────────────────────

def parse_org_features(org: str) -> dict[str, bool]:
    """Which ENABLED_FEATURES_BY_ORGANIZATION flags include this org shortname."""
    if not FEATURES_RB.exists():
        print(f"warn: {FEATURES_RB} missing; feature flags empty", file=sys.stderr)
        return {}
    text = FEATURES_RB.read_text(encoding="utf-8")
    m = re.search(
        r"ENABLED_FEATURES_BY_ORGANIZATION\s*=\s*YAML\.load\s*<<-?YAML\n(.*?)\nYAML",
        text,
        re.S,
    )
    if not m:
        return {}
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(m.group(1)) or {}
    except Exception:
        # Minimal parser: :flag:\n- org lines
        data = {}
        cur = None
        for line in m.group(1).splitlines():
            if line.startswith(":"):
                cur = line.strip().strip(":").rstrip(":")
                data[cur] = []
            elif line.startswith("- ") and cur is not None:
                data[cur].append(line[2:].strip())
    out = {}
    for flag, orgs in (data or {}).items():
        key = str(flag).lstrip(":")
        out[key] = org in [str(o) for o in (orgs or [])]
    return out


# ── stamped SQL ─────────────────────────────────────────────────────────────

SQL_META = """
SELECT o.id, o.shortname, o.name,
       o.properties AS org_properties,
       (SELECT max(invoice_date) FROM portal_invoices
         WHERE organization_id=o.id AND invoice_date <= current_date) AS report_through_date
FROM organizations o WHERE o.shortname = '{org}'
"""

SQL_SITE = """
SELECT ms.enable_sales_portal,
       ms.properties AS site_properties
FROM mobile_sites ms
WHERE ms.organization_id = {oid}
ORDER BY ms.id
LIMIT 1
"""

SQL_CUSTOMERS = """
SELECT c.code, c.name, c.billing_state AS state, c.territory_codes
FROM customers c
WHERE c.organization_id = {oid}
  AND c.code IN (
        SELECT DISTINCT customer_bill_to_number FROM portal_invoices
         WHERE organization_id = {oid}
           AND invoice_date BETWEEN '{since}' AND '{rtd}'
        UNION
        SELECT DISTINCT customer_bill_to_number FROM portal_orders
         WHERE organization_id = {oid}
           AND order_date BETWEEN '{since}' AND '{rtd}'
      )
"""

SQL_INVOICES = """
SELECT i.invoice_number,
       i.invoice_date,
       i.customer_bill_to_number AS bill_to,
       i.customer_bill_to_name   AS bill_to_name,
       LEAST(i.net_amount, {cap})::numeric AS net_amount
FROM portal_invoices i
WHERE i.organization_id = {oid}
  AND i.invoice_date BETWEEN '{since}' AND '{rtd}'
  AND i.net_amount IS NOT NULL
ORDER BY i.invoice_date, i.invoice_number
"""

SQL_INV_CONTROL = """
SELECT count(*) AS n,
       round(sum(LEAST(net_amount, {cap})), 2)::text AS net,
       count(DISTINCT customer_bill_to_number) AS billtos
FROM portal_invoices
WHERE organization_id = {oid}
  AND invoice_date BETWEEN '{since}' AND '{rtd}'
  AND net_amount IS NOT NULL
"""

SQL_ORDERS = """
SELECT o.order_number,
       o.order_date,
       o.customer_bill_to_number AS bill_to,
       o.customer_bill_to_name   AS bill_to_name,
       o.status::text            AS status,
       o.order_origin,
       o.rep_number,
       LEAST(COALESCE(o.total_amount, 0), {cap})::numeric AS total_amount
FROM portal_orders o
WHERE o.organization_id = {oid}
  AND o.order_date BETWEEN '{since}' AND '{rtd}'
ORDER BY o.order_date, o.order_number
"""

SQL_ORD_CONTROL = """
SELECT count(*) AS n,
       round(sum(LEAST(COALESCE(total_amount, 0), {cap})), 2)::text AS total
FROM portal_orders
WHERE organization_id = {oid}
  AND order_date BETWEEN '{since}' AND '{rtd}'
"""

SQL_USER_TYPES = """
SELECT ut.name,
       ut.customer_synching,
       ut.properties,
       ut.permissions::text AS permissions,
       (SELECT count(*) FROM org_users ou
         WHERE ou.user_type_id = ut.id
           AND NOT COALESCE(ou.disabled, false)) AS users
FROM user_types ut
WHERE ut.organization_id = {oid}
ORDER BY users DESC, ut.name
"""

SQL_TEAM = """
SELECT
  count(*) FILTER (
    WHERE last_ecat_online_login_at IS NOT NULL
      AND NOT COALESCE(disabled, false)
      AND (customer_number IS NULL OR customer_number = '')
  ) AS active_seats,
  count(*) FILTER (
    WHERE last_ecat_online_login_at >= date '{rtd}' - 30
      AND NOT COALESCE(disabled, false)
      AND (customer_number IS NULL OR customer_number = '')
  ) AS logins_30d,
  count(*) FILTER (
    WHERE last_ecat_online_login_at < date '{rtd}' - 30
      AND last_ecat_online_login_at >= date '{rtd}' - 90
      AND NOT COALESCE(disabled, false)
      AND (customer_number IS NULL OR customer_number = '')
  ) AS quiet_31_90,
  count(*) FILTER (
    WHERE (last_ecat_online_login_at < date '{rtd}' - 90
           OR last_ecat_online_login_at IS NULL)
      AND NOT COALESCE(disabled, false)
      AND (customer_number IS NULL OR customer_number = '')
      AND last_ipad_login_at IS NOT NULL
  ) AS dark_gt90
FROM org_users
WHERE organization_id = {oid}
"""

SQL_WRITERS = """
SELECT COALESCE(NULLIF(trim(rep_number), ''), '—') AS rep_number,
       count(*) AS orders,
       round(sum(LEAST(COALESCE(total_amount, 0), {cap})), 2)::text AS gmv
FROM portal_orders
WHERE organization_id = {oid}
  AND order_date BETWEEN date '{rtd}' - 29 AND date '{rtd}'
  AND (
        lower(COALESCE(order_origin, '')) LIKE '%ecat%'
     OR lower(COALESCE(order_origin, '')) LIKE '%eol%'
  )
  AND lower(COALESCE(status::text, '')) NOT LIKE '%quote%'
  AND lower(COALESCE(status::text, '')) NOT LIKE '%cancel%'
GROUP BY 1
ORDER BY sum(LEAST(COALESCE(total_amount, 0), {cap})) DESC
LIMIT 8
"""

SQL_WRITERS_CONTROL = """
SELECT count(DISTINCT COALESCE(NULLIF(trim(rep_number), ''), '—')) AS writers,
       count(*) AS orders
FROM portal_orders
WHERE organization_id = {oid}
  AND order_date BETWEEN date '{rtd}' - 29 AND date '{rtd}'
  AND (
        lower(COALESCE(order_origin, '')) LIKE '%ecat%'
     OR lower(COALESCE(order_origin, '')) LIKE '%eol%'
  )
  AND lower(COALESCE(status::text, '')) NOT LIKE '%quote%'
  AND lower(COALESCE(status::text, '')) NOT LIKE '%cancel%'
"""

SQL_PORTAL_COUNTS = """
SELECT
  (SELECT count(*) FROM portal_orders WHERE organization_id = {oid}) AS orders_n,
  (SELECT count(*) FROM portal_invoices WHERE organization_id = {oid}) AS invoices_n
"""


def as_date(v) -> dt.date:
    if isinstance(v, dt.date):
        return v
    return dt.date.fromisoformat(str(v)[:10])


def parse_territories(raw) -> list[str]:
    if not raw:
        return []
    if isinstance(raw, list):
        vals = raw
    else:
        s = str(raw).strip()
        if not s.startswith("["):
            return []
        try:
            vals = json.loads(s)
        except json.JSONDecodeError:
            return []
    return [str(v).strip() for v in vals if str(v).strip()]


def as_dict(v) -> dict:
    if v is None:
        return {}
    if isinstance(v, dict):
        return v
    if isinstance(v, str):
        try:
            return json.loads(v) if v.strip() else {}
        except json.JSONDecodeError:
            return {}
    return {}


def prop_list(v) -> list:
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v]
    if isinstance(v, str):
        s = v.strip()
        if not s:
            return []
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                return [str(x) for x in parsed]
        except json.JSONDecodeError:
            return [p.strip() for p in s.split(",") if p.strip()]
    return [str(v)]


def flag_of(props: dict, key: str, default=None):
    flags = props.get("flags") if isinstance(props.get("flags"), dict) else {}
    if key in flags:
        return flags[key]
    if key in props:
        return props[key]
    return default


# ── build ───────────────────────────────────────────────────────────────────

def build(org: str, since: str, mask: bool) -> dict:
    run = make_runner()

    meta_rows = run(SQL_META.format(org=org))
    if not meta_rows:
        raise SystemExit(f"org {org!r} not found")
    m = meta_rows[0]
    oid, rtd = m["id"], as_date(m["report_through_date"])
    org_props = as_dict(m.get("org_properties"))
    print(f"org {org} (id={oid}) report_through_date={rtd}", file=sys.stderr)

    site = run(SQL_SITE.format(oid=oid))
    site_row = site[0] if site else {}
    site_props = as_dict(site_row.get("site_properties"))

    cust_rows = run(SQL_CUSTOMERS.format(oid=oid, since=since, rtd=rtd))
    inv_rows = run(SQL_INVOICES.format(oid=oid, since=since, rtd=rtd, cap=ORDER_CAP))
    inv_control = run(SQL_INV_CONTROL.format(oid=oid, since=since, rtd=rtd, cap=ORDER_CAP))[0]
    ord_rows = run(SQL_ORDERS.format(oid=oid, since=since, rtd=rtd, cap=ORDER_CAP))
    ord_control = run(SQL_ORD_CONTROL.format(oid=oid, since=since, rtd=rtd, cap=ORDER_CAP))[0]
    print(
        f"extracted {len(inv_rows)} invoices, {len(ord_rows)} orders, {len(cust_rows)} customers",
        file=sys.stderr,
    )

    masker = Masker(load_salt(), enabled=mask)

    terr_counts: dict[str, int] = {}
    for c in cust_rows:
        for t in parse_territories(c.get("territory_codes")):
            terr_counts[t] = terr_counts.get(t, 0) + 1
    ordered_terr = sorted(terr_counts, key=lambda t: (-terr_counts[t], t))
    terr_index = {t: i for i, t in enumerate(ordered_terr)}
    territories = [masker.territory(t, i + 1) for i, t in enumerate(ordered_terr)]

    cust_by_code: dict[str, dict] = {}
    for c in cust_rows:
        cust_by_code[str(c["code"])] = {
            "state": (c.get("state") or "").strip().upper()[:2],
            "terr": [terr_index[t] for t in parse_territories(c.get("territory_codes"))],
        }

    window_start = as_date(since)
    customers: list[list] = []
    cust_slot: dict[str, int] = {}
    invoices: list[list] = []
    invoice_numbers: list[str] = []
    orphan_customers = 0
    orphan_rows = 0

    def ensure_customer(code: str, bill_to_name: str) -> int:
        nonlocal orphan_customers
        if code in cust_slot:
            return cust_slot[code]
        info = cust_by_code.get(code)
        if info is None:
            info = {"state": "", "terr": []}
            orphan_customers += 1
        key, name = masker.customer(code, bill_to_name)
        cust_slot[code] = len(customers)
        customers.append([name, key, info["state"], info["terr"]])
        return cust_slot[code]

    for r in inv_rows:
        code = str(r["bill_to"] or "")
        idx = ensure_customer(code, str(r.get("bill_to_name") or ""))
        if not customers[idx][3]:
            orphan_rows += 1
        day = (as_date(r["invoice_date"]) - window_start).days
        cents = int(round(float(r["net_amount"]) * 100))
        invoices.append([day, idx, cents])
        invoice_numbers.append(
            f"INV-{len(invoice_numbers) + 1:06d}" if mask else str(r["invoice_number"])
        )

    # Orders — status dimension + atomic rows. Backlog exclusion is stored so
    # the page can label backlog without merging it into invoiced.
    excl_backlog = prop_list(org_props.get("excluded_portal_order_backlog_order_statuses"))
    excl_set = {s.lower() for s in excl_backlog}
    status_order: list[str] = []
    status_index: dict[str, int] = {}
    orders: list[list] = []
    order_numbers: list[str] = []

    for r in ord_rows:
        code = str(r["bill_to"] or "")
        idx = ensure_customer(code, str(r.get("bill_to_name") or ""))
        status = str(r.get("status") or "—")
        if status not in status_index:
            status_index[status] = len(status_order)
            status_order.append(status)
        day = (as_date(r["order_date"]) - window_start).days
        cents = int(round(float(r["total_amount"]) * 100))
        is_quote = 1 if "quote" in status.lower() else 0
        is_backlog = 0 if status.lower() in excl_set else 1
        orders.append([day, idx, cents, status_index[status], is_quote, is_backlog])
        order_numbers.append(
            f"ORD-{len(order_numbers) + 1:06d}" if mask else str(r["order_number"])
        )

    # Team pulse
    team_row = run(SQL_TEAM.format(oid=oid, rtd=rtd))[0]
    writers = run(SQL_WRITERS.format(oid=oid, rtd=rtd, cap=ORDER_CAP))
    writers_ctl = run(SQL_WRITERS_CONTROL.format(oid=oid, rtd=rtd))[0]
    top_writers = []
    for w in writers:
        top_writers.append([
            masker.rep(str(w["rep_number"])),
            int(w["orders"]),
            int(round(float(w["gmv"]) * 100)),
        ])
    team = {
        "active_seats": int(team_row["active_seats"] or 0),
        "logins_30d": int(team_row["logins_30d"] or 0),
        "quiet_31_90": int(team_row["quiet_31_90"] or 0),
        "dark_gt90": int(team_row["dark_gt90"] or 0),
        "writers_30d": int(writers_ctl["writers"] or 0),
        "writer_orders_30d": int(writers_ctl["orders"] or 0),
        "top_writers": top_writers,
        "as_of": rtd.isoformat(),
    }

    # Settings snapshot — this org's real config
    ut_rows = run(SQL_USER_TYPES.format(oid=oid))
    portal_counts = run(SQL_PORTAL_COUNTS.format(oid=oid))[0]
    org_flags = org_props.get("flags") if isinstance(org_props.get("flags"), dict) else {}
    site_flags = site_props.get("flags") if isinstance(site_props.get("flags"), dict) else {}
    feature_map = parse_org_features(org)

    user_types = []
    portal_on = portal_off = dash_on = totals_off = 0
    for ut in ut_rows:
        props = as_dict(ut.get("properties"))
        perms = as_dict(ut.get("permissions"))
        esp = bool(flag_of(props, "enable_sales_portal", True))
        epd = bool(flag_of(props, "enable_portal_dashboard", False))
        dst = bool(flag_of(props, "display_sales_portal_totals", True))
        export = bool(flag_of(props, "can_export_eol_data", False))
        synch = str(ut.get("customer_synching") or "")
        users = int(ut["users"] or 0)
        if esp:
            portal_on += 1
        else:
            portal_off += 1
        if epd:
            dash_on += 1
        if not dst:
            totals_off += 1
        user_types.append({
            "name": str(ut["name"]),
            "users": users,
            "portal": esp,
            "dashboard": epd,
            "totals": dst,
            "export": export,
            "synching": SYNCHING_LABEL.get(synch, synch or "—"),
            "all_totals": bool(perms.get("access_all_customer_sales_totals")),
        })

    experiments = []
    for flag, label in FEATURE_LABELS.items():
        on = bool(feature_map.get(flag))
        # org-level flag properties can also turn some on (link_to_customer_dashboard)
        if flag == "link_to_customer_dashboard" and org_flags.get("link_to_customer_dashboard"):
            on = True
        if flag == "backlog_instead_of_amount_invoiced" and (
            feature_map.get(flag) or org_flags.get("backlog_instead_of_amount_invoiced")
        ):
            on = True
        status = "dead" if flag in DEAD_FLAGS else ("on" if on else "off")
        if flag in DEAD_FLAGS and not on:
            # Still list dead flags only when historically relevant; skip empty noise
            if flag not in feature_map:
                continue
        experiments.append({
            "flag": flag,
            "label": label,
            "status": status,
            "on": on,
        })

    site_enabled = bool(site_row.get("enable_sales_portal"))
    org_dash = bool(org_flags.get("enable_portal_dashboard"))
    settings = {
        "site_portal_enabled": site_enabled,
        "org_dashboard_enabled": org_dash,
        "currency": org_props.get("sales_portal_currency_code") or "USD",
        "display_qty_available": bool(site_flags.get("display_quantity_available", False)),
        "display_qty_backordered": bool(site_flags.get("display_quantity_backordered", False)),
        "eol_customer_graph": bool(feature_map.get("eol_customer_graph")),
        "link_to_customer_dashboard": bool(
            feature_map.get("link_to_customer_dashboard")
            or org_flags.get("link_to_customer_dashboard")
        ),
        "advanced_reports": bool(feature_map.get("advanced_reports")),
        "territory_dashboard_flag": bool(feature_map.get("portal_portal")),
        "territory_match_via_rep": bool(feature_map.get("territory_access_via_rep_number")),
        "excluded_backlog_statuses": excl_backlog,
        "portal_data_type": org_props.get("portal_data_type") or "OVERLAPS (default)",
        "portal_calculations": org_props.get("portal_calculations") or "Modern (default)",
        "max_age_months": org_props.get("max_portal_data_age_months") or "",
        "backlog_instead_of_invoiced": bool(
            feature_map.get("backlog_instead_of_amount_invoiced")
        ),
        "user_types": user_types,
        "user_type_summary": {
            "portal_on": portal_on,
            "portal_off": portal_off,
            "dashboard_on": dash_on,
            "totals_off": totals_off,
            "types": len(user_types),
        },
        "portal_orders_n": int(portal_counts["orders_n"] or 0),
        "portal_invoices_n": int(portal_counts["invoices_n"] or 0),
        "experiments": experiments,
        "features": {
            k: bool(v) for k, v in feature_map.items()
            if k in FEATURE_LABELS
        },
    }

    dataset = {
        "meta": {
            "org_label": (org.upper() if mask else str(m["name"] or org)),
            "org_shortname": org,
            "organization_id": int(oid),
            "masked": mask,
            "window_start": window_start.isoformat(),
            "report_through_date": rtd.isoformat(),
            "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "confidence": CONFIDENCE_CEILING,
            "total_business_source": "portal_invoices.net_amount",
            "feed_completeness": round(
                100.0 * (len(invoices) - orphan_rows) / max(len(invoices), 1), 2
            ),
            "row_cap": ORDER_CAP,
            "row_count": len(invoices),
            "order_count": len(orders),
            "unassigned_customers": orphan_customers,
            "unassigned_rows": orphan_rows,
        },
        "territories": territories,
        "customers": customers,
        "invoices": invoices,
        "invoice_numbers": invoice_numbers,
        "order_statuses": status_order,
        "orders": orders,
        "order_numbers": order_numbers,
        "team": team,
        "settings": settings,
    }

    verify(dataset, inv_control, ord_control, team, writers_ctl)
    masker.write_map(MAP_FILE, {
        "org": org, "oid": oid, "since": since, "rtd": rtd.isoformat(),
    })
    return dataset


def verify(dataset, inv_control, ord_control, team, writers_ctl) -> None:
    """Prove emitted blocks reproduce independent SQL control totals."""
    n = len(dataset["invoices"])
    cents = sum(r[2] for r in dataset["invoices"])
    got = round(cents / 100.0, 2)
    want = round(float(inv_control["net"]), 2)
    print(f"verify invoices rows   : dataset={n} control={inv_control['n']}", file=sys.stderr)
    print(f"verify invoices dollars: dataset={got:,.2f} control={want:,.2f}", file=sys.stderr)
    if n != int(inv_control["n"]):
        raise SystemExit("FAIL: invoice row count does not match control query")
    if abs(got - want) > 0.01:
        raise SystemExit("FAIL: invoice dollar total does not match control query")

    on = len(dataset["orders"])
    ocents = sum(r[2] for r in dataset["orders"])
    ogot = round(ocents / 100.0, 2)
    owant = round(float(ord_control["total"]), 2)
    print(f"verify orders rows   : dataset={on} control={ord_control['n']}", file=sys.stderr)
    print(f"verify orders dollars: dataset={ogot:,.2f} control={owant:,.2f}", file=sys.stderr)
    if on != int(ord_control["n"]):
        raise SystemExit("FAIL: order row count does not match control query")
    if abs(ogot - owant) > 0.01:
        raise SystemExit("FAIL: order dollar total does not match control query")

    if team["writers_30d"] != int(writers_ctl["writers"] or 0):
        raise SystemExit("FAIL: writers_30d does not match control")
    if team["writer_orders_30d"] != int(writers_ctl["orders"] or 0):
        raise SystemExit("FAIL: writer_orders_30d does not match control")

    print("verify OK: dataset reconciles to stamped SQL", file=sys.stderr)


def emit(dataset: dict, out_path: Path) -> None:
    payload = json.dumps(dataset, separators=(",", ":"))
    banner = (
        "/* Generated by PM/sales-portal-agent-starters/cycle-04-outputs/dataset/build_dataset.py\n"
        "   Do not edit by hand. Regenerate to change any figure. */\n"
    )
    out_path.write_text(f"{banner}window.SP_DATASET = {payload};\n", encoding="utf-8")
    size = out_path.stat().st_size
    print(f"wrote {out_path} ({size / 1024:.0f} KB)", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--org", default="wwjc")
    ap.add_argument("--since", default="2025-01-01")
    ap.add_argument("--no-mask", dest="mask", action="store_false")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    dataset = build(args.org, args.since, args.mask)
    out = Path(args.out) if args.out else ARTIFACT_DIR / "sales-portal-client-review-v2.data.js"
    emit(dataset, out)


if __name__ == "__main__":
    main()
