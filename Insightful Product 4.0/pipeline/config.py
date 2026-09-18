"""Paths, constants, and the query-id manifest. No logic — values only.

If you find yourself adding a function here, it belongs in another module.
"""
from __future__ import annotations

import os
from pathlib import Path

# ─── Paths ─────────────────────────────────────────────────────────────────
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent  # Insightful Product 4.0/
PIPELINE_DIR = WORKSPACE_ROOT / "pipeline"
TEMPLATE_DIR = PIPELINE_DIR / "templates"
CACHE_DIR = PIPELINE_DIR / "cache"
COHORT_RUNS_DIR = PIPELINE_DIR / "cohort_runs"

FOUNDATION_DIR = WORKSPACE_ROOT / "foundation"
QUERY_LIBRARY_MD = FOUNDATION_DIR / "query_library_v2.md"
PROVENANCE_SPINE_MD = FOUNDATION_DIR / "provenance_spine.md"

PROFILES_DIR = WORKSPACE_ROOT / "profiles"
OPERATORS_DIR = WORKSPACE_ROOT / "operators"
OUTPUTS_DIR = WORKSPACE_ROOT / "outputs"
CONFIG_DIR = WORKSPACE_ROOT / "config"
HOUSE_REP_EXCLUSIONS_MD = CONFIG_DIR / "house_rep_exclusions.md"
TIER_OVERRIDES_JSON = CONFIG_DIR / "tier_overrides.json"

# ─── Postgres connection (env-var driven) ──────────────────────────────────
# Set via shell or .env (gitignored). Supports DATABASE_URL or PG* style.
#
#   DATABASE_URL=postgresql://user:pass@host:port/dbname
# or
#   PGHOST=…  PGPORT=…  PGDATABASE=…  PGUSER=…  PGPASSWORD=…
#
# VPN must be active. The MCP server `user-supercat-postgres-vpn` uses the
# same backing database; pipeline reads through psycopg2 directly so it
# does not require the agent to be in the loop during cache population.
def _load_dotenv(path: Path) -> None:
    """Read KEY=VALUE lines from a .env into os.environ, without a dependency.

    The comment above has promised .env support for a while; only os.environ
    was ever read, so a DSN written to .env silently did nothing and
    populate_cache fell through to the MCP path. A real process environment
    always wins, so exporting still overrides the file.
    """
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv(WORKSPACE_ROOT / ".env")

DATABASE_URL = os.environ.get("DATABASE_URL")


def pg_dsn() -> str | dict:
    """Return either a DSN string or a dict of connection kwargs for psycopg2."""
    if DATABASE_URL:
        return DATABASE_URL
    return {
        "host": os.environ.get("PGHOST", "localhost"),
        "port": int(os.environ.get("PGPORT", "5432")),
        "dbname": os.environ.get("PGDATABASE", "supercat"),
        "user": os.environ.get("PGUSER", ""),
        "password": os.environ.get("PGPASSWORD", ""),
    }


# ─── Query manifest ────────────────────────────────────────────────────────
# The pipeline calls these queries by name; their SQL bodies live verbatim
# in query_library_v2.md and are extracted at cache-population time by
# pipeline.cache.extract_sql(query_id).
#
# Per the cross-cutting "catalog hygiene" constraint: new entries are added
# here ONLY when the corresponding SQL already exists in query_library_v2.md.
# The pipeline does not author inline SQL.

QUERIES_PREFLIGHT = [
    "Q-ECON-00",       # economics preflight: TOTAL_BUSINESS_SOURCE, n_inv, inv_ltm_net,
                       #   report_through_date, commerce_confidence, side-channel flags
    "Q-CHAN-00",       # channel availability + eCat reconciliation
    "Q-CHAN-06",       # F1 — eCat-SALE confirmed-ratio pre-check (blank-order_type default share)
    "RP-2",            # rep identity tier (distinct_repnum, name_bridge_pct → tier 0/1/2)
]

# QUERIES_GATHER: every entry MUST have a corresponding SQL block in canon.
# Per the catalog-hygiene cross-cutting constraint, never add a name here
# without verifying cache.extract_sql({qid}) returns SQL.
QUERIES_GATHER = [
    "Q-ECON-LEAK",     # org-wide leakage (also rolled to rep for §6 cards)
    "Q-ECON-CONC",     # customer concentration probe (top-1 / top-10 / HHI)
    "Q-ECON-NRR",      # same-base retention math
    "Q-ECON-CONTRIB",  # top-15 by $ contribution (lifters/decliners)
    "RS-01",           # rep leaderboard, invoiced LTM, named via Tier-2 bridge
    "S1",              # per-account decay: equal 6mo windows, $-at-risk = LTM rev
    "C2",              # leakage by rep (component of §6 coaching cards)
    "Q-CHAN-10",       # channel mix by canonical channel (LTM $)
    "Q-CHAN-05",       # eCat vs non-eCat split
    "Q-PROD-TOP",     # top items LTM by revenue/units/dealers
    "Q-PROD-FAMILY",  # family rollups by collection_code (LTM + YoY)
    "Q-CROSS-SELL",   # anchor-SKU dealers who have NOT bought target family
    "Q-DEALER-COHORT",  # dealer cohort flow + cadence + same-base lift
    "Q-53",            # high-value accounts with no confirmed platform order ever
]

QUERIES_PLATFORM = [
    "Q-08",            # data freshness monitor (entity staleness per data_versions)
    "Q-09",            # import health & sync reliability (monthly import counts)
    "Q-10",            # feature enablement gap analysis (flags + feature counts)
    "Q-11",            # configuration completeness (stale entities >30 days)
    # Rep behavior floor — OWNED, always-on, ERP-optional (VM-R1/R2/R4)
    "Q-R1",            # rep activity & cadence (active seats, logins, quiet seats)
    "Q-R2",            # coverage / territory penetration (customers touched 90d)
    "Q-R4",            # quote→submit discipline (confirmed vs. draft orders 90d)
]

QUERIES_ALL = QUERIES_PREFLIGHT + QUERIES_GATHER + QUERIES_PLATFORM

# ─── Determinism / sanity constants (mirror query_library_v2.md guardrails) ─
ORDER_CAP = 5_000_000               # per-row sanity cap
DATE_CLAMP_START = "2010-01-01"
DATE_CLAMP_FORWARD_DAYS = 90

# Confidence-tier ordering, used by REPORT_INTELLIGENCE_TIER = LEAST(mass, confidence)
CONFIDENCE_RANK = {"NONE": 0, "LIMITED": 1, "PARTIAL": 2, "STRONG": 3}
TIER_NAMES = {0: "NONE", 1: "LIMITED", 2: "PARTIAL", 3: "STRONG"}

# Rep-identity tier thresholds (Spine §7.1)
REP_TIER_2_MIN_NAME_BRIDGE = 0.80  # ≥80% → Tier 2 named
REP_TIER_1_MIN_NAME_BRIDGE = 0.00  # >0 and <0.80 → Tier 1 (rep_number grain)


_tier_overrides_cache: dict | None = None

def load_tier_overrides() -> dict:
    """Load tier override config (config/tier_overrides.json).
    Contains deadband carry-overs and dormant org flags per rep_copilot_operator.md §1.
    """
    global _tier_overrides_cache
    if _tier_overrides_cache is None:
        import json
        if not TIER_OVERRIDES_JSON.exists():
            _tier_overrides_cache = {}
            return _tier_overrides_cache
        with TIER_OVERRIDES_JSON.open("r", encoding="utf-8") as f:
            _tier_overrides_cache = json.load(f)
    return _tier_overrides_cache

HOUSE_REP_EXCLUSIONS_JSON = CONFIG_DIR / "house_rep_exclusions.json"
PROFILE_SCHEMA_JSON = CONFIG_DIR / "profile_schema.json"

# Optional file-backed org map for one-off clients not in cache._KNOWN_ORG_IDS.
# Shape: { "<shortname>": {"id": <int>, "name": "<display name>"} }.
# Lets any client resolve its organization_id/name without a live DB connection
# (the static map in cache.py is still checked first). Populate it once per new
# client via the Postgres MCP: SELECT id, name FROM organizations WHERE shortname=…
ORG_IDS_JSON = CONFIG_DIR / "org_ids.json"

_org_ids_cache: dict | None = None


def load_org_ids() -> dict:
    """Load the optional file-backed org map (config/org_ids.json). Cached after
    first load; returns {} when the file is absent."""
    global _org_ids_cache
    if _org_ids_cache is None:
        import json
        if ORG_IDS_JSON.exists():
            _org_ids_cache = json.loads(ORG_IDS_JSON.read_text(encoding="utf-8"))
        else:
            _org_ids_cache = {}
    return _org_ids_cache


_house_exclusions_cache: dict | None = None


def load_house_exclusions() -> dict:
    """Load the machine-readable house-rep exclusions (config/house_rep_exclusions.json).
    Cached after first load. The .md file remains the human-readable authority.
    """
    global _house_exclusions_cache
    if _house_exclusions_cache is None:
        import json
        with HOUSE_REP_EXCLUSIONS_JSON.open("r", encoding="utf-8") as f:
            _house_exclusions_cache = json.load(f)
    return _house_exclusions_cache


# ─── Query column schemas (validated at gather time) ─────────────────────
QUERY_SCHEMAS: dict[str, dict] = {
    "S1": {"required": ["subject", "dollar_impact", "days_silent", "recent_6mo", "prior_6mo"],
           "aliases": {"subject": ["bill_to_number", "customer_bill_to_number"],
                       "dollar_impact": ["ltm_rev", "dollars_at_risk"],
                       "who_to_call": ["rep_number"]}},
    # RS-01 also emits `prior_ltm_invoiced` (prior matching 12mo) — consumed by
    # gather.load_reps() for a real YoY %. Kept OPTIONAL (not required) so orgs whose
    # RS-01 cache predates the prior-window change still validate; load_reps defaults it to 0.0.
    "RS-01": {"required": ["rep_label", "invoiced_net_ltm"],
              "aliases": {"invoiced_net_ltm": ["ltm_invoiced", "net_amount"],
                          "accounts": ["customer_count", "n_customers"]}},
    "C2": {"required": ["who_to_call", "dollar_impact"],
           "aliases": {"who_to_call": ["rep_number"]}},
    "Q-ECON-CONC": {"required": ["top1_pct"],
                    "aliases": {}},
    "Q-ECON-NRR": {"required": ["prior_cohort_custs", "prior_base", "retained_plus_expansion", "nrr_pct"],
                   "aliases": {}},
    "Q-ECON-LEAK": {"required": ["customer_bill_to_number", "leakage_dollars", "skus_underpriced"],
                    "aliases": {"customer_bill_to_number": ["cust"]}},
    "Q-ECON-CONTRIB": {"required": ["customer_bill_to_number", "ltm_net", "contribution_proxy", "rank_shift"],
                       "aliases": {}},
    "Q-PROD-TOP": {"required": ["item_number", "ltm_revenue"],
                   "aliases": {}},
    "Q-PROD-FAMILY": {"required": ["family_label", "ltm_revenue"],
                      "aliases": {}},
    "Q-CHAN-10": {"required": ["booked_dollars"],
                 "aliases": {"canonical_channel": ["channel", "order_origin"]}},
    "Q-CHAN-05": {"required": ["total_business_gmv", "ecat_gmv", "non_ecat_gmv", "report_decision"],
                  "aliases": {}},
    "Q-CHAN-06": {"required": ["confirmed_gmv", "all_ecat_gmv", "blank_default_share_pct"],
                  "aliases": {}},
    "Q-DEALER-COHORT": {"required": ["active_ltm"],
                        "aliases": {}},
    # Rep behavior floor schemas (Q-R1/R2/R4)
    "Q-R1": {"required": ["active_seats", "order_authors_90d"],
             "aliases": {}},
    "Q-R2": {"required": ["total_customers", "touched_customers"],
             "aliases": {}},
    "Q-R4": {"required": ["total_orders", "confirmed_orders", "submit_rate_pct"],
             "aliases": {}},
}
