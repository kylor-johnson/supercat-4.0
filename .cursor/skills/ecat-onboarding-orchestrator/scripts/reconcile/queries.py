#!/usr/bin/env python3
"""Named query library for eCat / SuperCat Postgres audits.

Schema archaeology encoded here once so it is never rediscovered in a session:

  1. `organizations.state` is GEOGRAPHIC (CA, TX, Ontario) — NOT lifecycle.
     Lifecycle is `properties->>'status'` = 'onboarding' | 'active' | 'fully_suspended'.
     `WHERE o.state = 'onboarding'` silently returns 0 rows. Verified: Appendix A.

  2. `customers` key column is `code`, NOT `customer_number`.

  3. `import_events` has exactly four columns: id, created_at, organization_id, data.
     The columns `file_type`, `num_warnings`, `num_errors`, `warning_message`,
     `error_message` documented in RUN_PROMPT.md v3.5 DO NOT EXIST. `data` is a YAML
     text blob; parse it with parse_import_tiers() below.

  4. `price_levels` has `code`, `name`, `pl_type`, `factor` — NO `description` column.

  5. Product images are in `product_images` (flat, filename-keyed, no product_id FK).
     `images_json` holds image filenames on the product row — NOT `image_file_name`.

  6. Products carry a serialized YAML `options` column — NOT separate OptionSet1..5.
     A product with no options has `---\\n:custom: false\\n` in that column.
     The Smart SKU builder is in `properties->>'configured_item_number_builder'`.

  7. Taxonomy groups (categories nest under them) NEVER auto-create from a product
     import. A missing group is a fatal import error. Real fatal in mali's log.

  8. `import_events.data` tier markers: `:fatal`, `:error`, `:warning`, `:information`.
     Use parse_import_tiers() to extract counts from the YAML text.

Usage patterns:

  Via MCP (user-supercat-postgres-vpn) — copy-paste the .sql attribute of any named
  query, replacing %(param)s with the literal value:
      PRODUCT_COUNTS → paste sql, replace %(org_id)s with the integer org id

  Via CLI — profile.py wraps this library and connects automatically:
      python scripts/reconcile/profile.py --shortname mali --emit-live-state

  Print any query's SQL from the command line:
      python scripts/reconcile/queries.py --print ORG_BY_SHORTNAME
      python scripts/reconcile/queries.py --list
"""

import datetime
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Query registry: name -> (sql, description)
# ---------------------------------------------------------------------------

#: All named queries keyed by constant name.
QUERIES: Dict[str, Tuple[str, str]] = {}


def _q(name: str, sql: str, description: str) -> Tuple[str, str]:
    """Register a named query and return it as a (sql, description) tuple."""
    entry = (sql.strip(), description.strip())
    QUERIES[name] = entry
    return entry


# ---------------------------------------------------------------------------
# Org identity
# ---------------------------------------------------------------------------

ORG_BY_SHORTNAME = _q(
    "ORG_BY_SHORTNAME",
    """
    SELECT
        id,
        shortname,
        name,
        state               AS geographic_state,
        properties->>'status' AS lifecycle_status,
        import_active
    FROM organizations
    WHERE shortname = %(shortname)s
    """,
    "Resolve org id and lifecycle status from shortname. "
    "NOTE: `state` is geographic (TX/CA/Ontario), not lifecycle — "
    "lifecycle is `properties->>'status'` = onboarding | active | fully_suspended. "
    "Verified Appendix A of IMPLEMENTATION_PLAN.md.",
)

# ---------------------------------------------------------------------------
# Catalog & images
# ---------------------------------------------------------------------------

PRODUCT_COUNTS = _q(
    "PRODUCT_COUNTS",
    """
    SELECT
        COUNT(*)                                    AS total_products,
        COUNT(*) FILTER (WHERE NOT deleted)         AS active_products,
        COUNT(*) FILTER (WHERE deleted)             AS hidden_products,
        COUNT(*) FILTER (WHERE NOT deleted
                           AND image_exists)        AS active_with_images,
        COUNT(*) FILTER (WHERE NOT deleted
                           AND NOT image_exists)    AS active_missing_images
    FROM products
    WHERE organization_id = %(org_id)s
    """,
    "Product counts: total, active, hidden, image coverage. "
    "`image_exists` tracks only the FIRST filename in images_json — alternate images "
    "do not satisfy it. eOL suppresses imageless products from search.",
)

IMAGE_EXISTS_SPLIT = _q(
    "IMAGE_EXISTS_SPLIT",
    """
    SELECT
        image_exists,
        COUNT(*) AS product_count
    FROM products
    WHERE organization_id = %(org_id)s
      AND NOT deleted
    GROUP BY image_exists
    ORDER BY image_exists DESC
    """,
    "Verified mechanism (libco, 832 products, zero exceptions): "
    "image_exists=false always means the primary filename is absent from product_images.",
)

PRODUCT_KEYS_SAMPLE = _q(
    "PRODUCT_KEYS_SAMPLE",
    """
    SELECT item_number
    FROM products
    WHERE organization_id = %(org_id)s
      AND NOT deleted
      AND item_number IS NOT NULL
    ORDER BY item_number
    """,
    "All active product item_numbers (BaseItemCodes) for the org fingerprint check. "
    "Full list, not a sample — the fingerprint check needs it to detect a wrong-org file.",
)

PRODUCTS_WITH_OPTIONS = _q(
    "PRODUCTS_WITH_OPTIONS",
    """
    SELECT COUNT(*) AS products_with_options
    FROM products
    WHERE organization_id = %(org_id)s
      AND NOT deleted
      AND options IS NOT NULL
      AND options NOT LIKE '%%:custom: false%%'
    """,
    "Products whose options YAML contains actual option group references. "
    "If this returns 0 while ORPHAN_OPTIONS shows groups exist, all groups are "
    "orphaned POC residue that only clears when you re-send options.csv.",
)

# ---------------------------------------------------------------------------
# Import events
# ---------------------------------------------------------------------------

IMPORT_EVENTS_RECENT = _q(
    "IMPORT_EVENTS_RECENT",
    """
    SELECT
        id,
        created_at,
        left(data, 6000) AS data_preview
    FROM import_events
    WHERE organization_id = %(org_id)s
    ORDER BY created_at DESC
    LIMIT %(limit)s
    """,
    "Most recent import_events rows. `data` is a YAML text blob — use "
    "parse_import_tiers() to count :fatal / :error / :warning / :information markers. "
    "The columns file_type / num_warnings / num_errors in RUN_PROMPT.md v3.5 DO NOT EXIST.",
)

IMPORT_EVENTS_BY_TYPE = _q(
    "IMPORT_EVENTS_BY_TYPE",
    """
    SELECT
        id,
        created_at,
        left(data, 8000) AS data
    FROM import_events
    WHERE organization_id = %(org_id)s
      AND (
            data ILIKE '%%Products%%'
         OR data ILIKE '%%Inventory%%'
         OR data ILIKE '%%Customers%%'
         OR data ILIKE '%%Options%%'
         OR data ILIKE '%%Images%%'
         OR data ILIKE '%%Stories%%'
      )
    ORDER BY created_at DESC
    LIMIT 50
    """,
    "Recent import events filtered to the six main eCat file types. "
    "Parse data text for '- - Products', '- - Inventory', etc. to bucket by type, "
    "then count :fatal / :error / :warning markers per event.",
)

# ---------------------------------------------------------------------------
# Pricing & customers
# ---------------------------------------------------------------------------

PRICE_LEVELS = _q(
    "PRICE_LEVELS",
    """
    SELECT code, name, pl_type, factor
    FROM price_levels
    WHERE organization_id = %(org_id)s
    ORDER BY code
    """,
    "All price levels for the org. NOTE: no `description` column — verified Appendix A. "
    "DefaultPriceCode in customers.csv must match a code here — "
    "a mismatch (e.g. '0' from an ERP) caused tcd's 100% customer rejection.",
)

CUSTOMER_COUNT = _q(
    "CUSTOMER_COUNT",
    """
    SELECT COUNT(*) AS total_customers
    FROM customers
    WHERE organization_id = %(org_id)s
    """,
    "Total customer rows. Column is `code` NOT `customer_number` — verified Appendix A.",
)

CUSTOMER_KEYS_SAMPLE = _q(
    "CUSTOMER_KEYS_SAMPLE",
    """
    SELECT code
    FROM customers
    WHERE organization_id = %(org_id)s
      AND code IS NOT NULL
    ORDER BY code
    """,
    "All customer BillToCodes for the org fingerprint check. "
    "Column is `code`, not `customer_number` — verified Appendix A.",
)

# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------

INVENTORY_COUNTS = _q(
    "INVENTORY_COUNTS",
    """
    SELECT COUNT(*) AS total_inventory_rows
    FROM inventories
    WHERE organization_id = %(org_id)s
    """,
    "Total inventory rows. Confirm freshness by checking recent IMPORT_EVENTS_BY_TYPE. "
    "inventory.csv hard-deletes all rows and reloads — the mali/leg wipe (Appendix B) "
    "produced 694 → 0 matched rows in minutes.",
)

ORPHAN_INVENTORY = _q(
    "ORPHAN_INVENTORY",
    """
    SELECT COUNT(*) AS orphan_inventory_rows
    FROM inventories i
    WHERE i.organization_id = %(org_id)s
      AND NOT EXISTS (
        SELECT 1
        FROM products p
        WHERE p.organization_id = %(org_id)s
          AND NOT p.deleted
          AND p.item_number = i.item_number
      )
    """,
    "Inventory rows with no matching active product (cross-file referential integrity). "
    "Live counts 2026-07-27 (verified by query): leg=247, libco=83, tcd=30, mali=11. "
    "The mali count of 11 was 1,194 the day of the wrong-org import — fixed same day.",
)

# ---------------------------------------------------------------------------
# Options & groups
# ---------------------------------------------------------------------------

ORPHAN_OPTIONS = _q(
    "ORPHAN_OPTIONS",
    """
    SELECT
        (SELECT COUNT(*) FROM option_groups
         WHERE organization_id = %(org_id)s)        AS total_option_groups,
        (SELECT COUNT(*) FROM options
         WHERE organization_id = %(org_id)s)        AS total_options,
        (SELECT COUNT(*)
         FROM products
         WHERE organization_id = %(org_id)s
           AND NOT deleted
           AND options IS NOT NULL
           AND options NOT LIKE '%%:custom: false%%') AS products_referencing_options
    """,
    "Option groups, options, and product-option references in one pass. "
    "If products_referencing_options = 0 and total_option_groups > 0, all groups are "
    "orphaned POC residue — permanent until you re-send options.csv (which hard-deletes). "
    "Verified: tcd has 222 options / 98 groups / 0 product references; "
    "leg has 29 options / 11 groups / 0 references — all pre-cutover.",
)

# ---------------------------------------------------------------------------
# Images
# ---------------------------------------------------------------------------

UPLOADED_IMAGES = _q(
    "UPLOADED_IMAGES",
    """
    SELECT filename
    FROM product_images
    WHERE organization_id = %(org_id)s
    ORDER BY filename
    """,
    "All uploaded image filenames for the org. product_images is flat and filename-keyed "
    "with no product_id FK — verified §4.3. Used by the primary-image set diff check. "
    "NOTE: if query fails, verify column name (may be `name` instead of `filename`).",
)

MISSING_IMAGES = _q(
    "MISSING_IMAGES",
    """
    SELECT item_number, images_json
    FROM products
    WHERE organization_id = %(org_id)s
      AND NOT deleted
      AND NOT image_exists
    ORDER BY item_number
    """,
    "Active products with image_exists = false. The primary filename from images_json "
    "is absent from product_images. eOL suppresses these from search. "
    "NOTE: images_json holds the filenames, not `image_file_name` — verified Appendix A.",
)

# ---------------------------------------------------------------------------
# Custom fields
# ---------------------------------------------------------------------------

CUSTOM_FIELDS_PRODUCTS = _q(
    "CUSTOM_FIELDS_PRODUCTS",
    """
    -- NOTE: Verify the table name against supercat_server schema.
    -- Hint: SELECT table_name FROM information_schema.tables
    --       WHERE table_name ILIKE '%%custom_field%%' AND table_schema = 'public';
    SELECT name
    FROM product_custom_field_definitions
    WHERE organization_id = %(org_id)s
      AND send_to_ipad = true
    ORDER BY name
    """,
    "Product custom fields registered in Admin with 'Send to iPad' enabled. "
    "Must be pre-registered before import — an unregistered column produces a warning "
    "and a warning-tier import skips all deletes of omitted records. "
    "Table name unverified — check supercat_server for the exact name.",
)

CUSTOM_FIELDS_CUSTOMERS = _q(
    "CUSTOM_FIELDS_CUSTOMERS",
    """
    -- NOTE: Verify the table name against supercat_server schema.
    SELECT name
    FROM customer_custom_field_definitions
    WHERE organization_id = %(org_id)s
    ORDER BY name
    """,
    "Customer custom fields registered in Admin. "
    "Table name unverified — check supercat_server for the exact name.",
)

CUSTOM_FIELDS_INVENTORY = _q(
    "CUSTOM_FIELDS_INVENTORY",
    """
    -- NOTE: Verify the table name against supercat_server schema.
    SELECT name
    FROM inventory_custom_field_definitions
    WHERE organization_id = %(org_id)s
    ORDER BY name
    """,
    "Inventory custom fields registered in Admin. "
    "Table name unverified — check supercat_server for the exact name.",
)

# ---------------------------------------------------------------------------
# Taxonomy
# ---------------------------------------------------------------------------

TAXONOMY_CODES_LIVE = _q(
    "TAXONOMY_CODES_LIVE",
    """
    SELECT DISTINCT trade_name_code AS code, 'trade_name' AS source
    FROM products
    WHERE organization_id = %(org_id)s
      AND NOT deleted
      AND trade_name_code IS NOT NULL
      AND trade_name_code != ''

    UNION

    SELECT DISTINCT trim(c.code) AS code, 'collection_or_category' AS source
    FROM products p
    CROSS JOIN LATERAL (
        SELECT trim(unnest(string_to_array(
            COALESCE(p.collection_codes, '') || ',' ||
            COALESCE(p.category_codes,   ''), ','
        ))) AS code
    ) c
    WHERE p.organization_id = %(org_id)s
      AND NOT p.deleted
      AND trim(c.code) != ''

    ORDER BY code
    """,
    "Distinct taxonomy codes (TradeNameCode + CollectionCodes + CategoryCodes) used by "
    "active products. Under Standard method every code must be pre-registered in Admin. "
    "NOTE: column names trade_name_code / collection_codes / category_codes need "
    "verification — the import CSV uses TradeNameCode / CollectionCodes / CategoryCodes "
    "but the DB columns may differ (snake_case). Check products table schema if this fails.",
)

TAXONOMY_GROUPS = _q(
    "TAXONOMY_GROUPS",
    """
    -- NOTE: Verify table name. Groups (categories nest under them) are in Admin:
    -- Products → Groups. They NEVER auto-create from a product import.
    -- Candidate tables: groups, product_groups, taxonomy_groups.
    SELECT code
    FROM product_groups
    WHERE organization_id = %(org_id)s
    ORDER BY code
    """,
    "Admin taxonomy groups (not option groups — these are the top-level grouping that "
    "categories nest under). Groups never auto-create from a product import — "
    "a missing group is a fatal error. Table name unverified.",
)

# ---------------------------------------------------------------------------
# User groups
# ---------------------------------------------------------------------------

USER_GROUPS = _q(
    "USER_GROUPS",
    """
    SELECT
        id,
        name,
        distribution_centers_auth
    FROM user_types
    WHERE organization_id = %(org_id)s
    ORDER BY name
    """,
    "User groups (user_types table). distribution_centers_auth: 'a' = all DCs, "
    "'c' = custom (restricted). Reps in DefaultUserGroup bypass DC restrictions. "
    "The rep-view vs Admin-view gate depends on non-Admin rep profiles existing per brand "
    "(mali: one profile per brand ML/NSL).",
)

PLACEHOLDER_PRICES = _q(
    "PLACEHOLDER_PRICES",
    """
    -- Detect products whose price columns contain placeholder values (0.0, 1.0,
    -- suspiciously round uniform prices across many SKUs). Adapt the column list to
    -- match the org's actual price level codes (see PRICE_LEVELS query).
    --
    -- NOTE: price data is in product columns named price_<code> or in a prices JSONB.
    -- Verify exact column names against the products table schema.
    --
    -- Pattern to look for in prices JSONB:
    SELECT
        item_number,
        prices
    FROM products
    WHERE organization_id = %(org_id)s
      AND NOT deleted
      AND prices IS NOT NULL
      AND (
          prices::text LIKE '%%"0.0"%%'
          OR prices::text LIKE '%%"1.0"%%'
          OR prices::text LIKE '%%: 0%%'
          OR prices::text LIKE '%%: 1%%'
      )
    ORDER BY item_number
    LIMIT 50
    """,
    "Products whose price data contains placeholder values (0.0, 1.0). "
    "A large count suggests the pricing pass is incomplete. "
    "NOTE: column name for prices needs verification against schema.",
)

# ---------------------------------------------------------------------------
# Helpers: import event tier parsing
# ---------------------------------------------------------------------------

#: Tier markers that appear in import_events.data YAML.
#: Verified against IMPLEMENTATION_PLAN.md §6.2 and Phase_Anchors.md.
TIER_MARKERS = (":fatal", ":error", ":warning", ":information")

#: File-type header patterns in import_events.data.
FILE_TYPE_PATTERNS = (
    "- - Products",
    "- - Inventory",
    "- - Customers",
    "- - Options",
    "- - Option Groups",
    "- - Stories",
    "- - Images",
    "- - Product Images",
    "- - order_data",
    "- - invoice_data",
)


def parse_import_tiers(data_text: str) -> Dict[str, int]:
    """Count tier markers in import_events.data.

    import_events.data is a YAML text blob.  The columns file_type / num_warnings /
    num_errors documented in RUN_PROMPT.md v3.5 DO NOT EXIST — parse the text instead.

    Returns dict with keys 'fatal', 'error', 'warning', 'information', 'total'.
    A clean import has fatal=0, error=0 and warning may be > 0 (warning-tier still
    imports and runs deletes).  Any fatal or error means deletes were skipped.
    """
    if not data_text:
        return {"fatal": 0, "error": 0, "warning": 0, "information": 0, "total": 0}
    text = data_text.lower()
    counts = {
        "fatal":       text.count(":fatal"),
        "error":       text.count(":error"),
        "warning":     text.count(":warning"),
        "information": text.count(":information"),
    }
    counts["total"] = sum(counts.values())
    return counts


def infer_file_type(data_text: str) -> Optional[str]:
    """Infer the file type from an import_events.data YAML text.

    Returns the matched pattern (e.g. '- - Products') or None.
    """
    for pattern in FILE_TYPE_PATTERNS:
        if pattern in (data_text or ""):
            return pattern.replace("- - ", "").strip()
    return None


def tier_summary(data_text: str) -> str:
    """Human-readable tier summary for an import_events row.

    Examples:
        'clean'
        '3 warnings'
        '1 fatal, 2 errors'
        '2 errors, 5 warnings'
    """
    counts = parse_import_tiers(data_text)
    parts = []
    if counts["fatal"]:
        parts.append(f"{counts['fatal']} fatal")
    if counts["error"]:
        parts.append(f"{counts['error']} error{'s' if counts['error'] != 1 else ''}")
    if counts["warning"]:
        parts.append(f"{counts['warning']} warning{'s' if counts['warning'] != 1 else ''}")
    return ", ".join(parts) if parts else "clean"


# ---------------------------------------------------------------------------
# Database connection
# ---------------------------------------------------------------------------

def connect(url: Optional[str] = None):
    """Return a psycopg2 connection from url or the DATABASE_URL env var.

    To connect to the SuperCat Postgres (requires VPN):
        export DATABASE_URL="postgresql://user:pass@host:5432/supercat_production"

    The MCP server name is user-supercat-postgres-vpn; use the same credentials.
    """
    db_url = url or os.environ.get("DATABASE_URL")
    if not db_url:
        raise EnvironmentError(
            "Set DATABASE_URL to your SuperCat Postgres connection string.\n"
            "  export DATABASE_URL='postgresql://user:pass@host:5432/dbname'\n"
            "The MCP server is user-supercat-postgres-vpn — same credentials."
        )
    try:
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        return conn
    except ImportError:
        raise ImportError(
            "psycopg2 is required for direct DB access.\n"
            "  pip install psycopg2-binary\n"
            "Alternatively, copy queries from this module and run them via the "
            "user-supercat-postgres-vpn MCP."
        )


# ---------------------------------------------------------------------------
# Executor: thin wrapper around a psycopg2 connection
# ---------------------------------------------------------------------------

class Executor:
    """Run named queries against a psycopg2 connection.

    query_tuple_or_sql accepts either:
      - A (sql, description) tuple from this module's named constants, or
      - A plain SQL string.

    All parameter placeholders use %(name)s style (psycopg2 default).
    """

    def __init__(self, conn):
        self._conn = conn

    def _sql(self, query_tuple_or_sql) -> str:
        if isinstance(query_tuple_or_sql, tuple):
            return query_tuple_or_sql[0]
        return query_tuple_or_sql

    def _cursor(self):
        try:
            import psycopg2.extras
            return self._conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except Exception:
            return self._conn.cursor()

    def all(self, query_tuple_or_sql, params: Optional[Dict] = None) -> List[Dict]:
        """Execute a query and return all rows as a list of dicts."""
        with self._cursor() as cur:
            cur.execute(self._sql(query_tuple_or_sql), params)
            rows = cur.fetchall()
            if rows and not isinstance(rows[0], dict):
                cols = [d[0] for d in cur.description]
                rows = [dict(zip(cols, r)) for r in rows]
            return list(rows)

    def one(self, query_tuple_or_sql, params: Optional[Dict] = None) -> Optional[Dict]:
        """Execute a query and return the first row as a dict, or None."""
        rows = self.all(query_tuple_or_sql, params)
        return rows[0] if rows else None

    def scalar(self, query_tuple_or_sql, params: Optional[Dict] = None) -> Any:
        """Execute a query and return the first column of the first row."""
        row = self.one(query_tuple_or_sql, params)
        if row is None:
            return None
        return next(iter(row.values()))


# ---------------------------------------------------------------------------
# Live-state JSON builder — assembles the preflight_gate.py contract
# ---------------------------------------------------------------------------

#: Keys that belong to the preflight_gate.py live-state JSON.
#: If a query fails, the key is omitted (degrades to gate WARNING, not FAIL).
LIVE_STATE_KEYS = (
    "shortname", "queried_at",
    "price_levels",      # list[str]  — DefaultPriceCode membership check
    "custom_fields",     # {products: [...], customers: [...], inventory: [...]}
    "taxonomy",          # {codes: [...], groups: [...]}
    "keys",              # {products.csv: [...], customers.csv: [...]}
    "counts",            # {products.csv: int, customers.csv: int}
    "uploaded_images",   # list[str]
)


def build_live_state(executor: Executor, shortname: str) -> Dict:
    """Query the live org and return the JSON that preflight_gate.py --live-state expects.

    Fields that cannot be queried (table-name unverified, query errors) are omitted
    rather than raised, so the gate degrades to WARNING for those checks rather than
    blocking on a query failure.

    The shape matches the contract in preflight_gate.py's module docstring:
        {
          "shortname": "mali",
          "queried_at": "2026-07-27T20:00:00Z",
          "price_levels": ["dn", "imap"],
          "custom_fields": {"products": ["Color"], "customers": ["BillTo_Region"]},
          "taxonomy": {"codes": ["ML", "LL"], "groups": ["MAIN"]},
          "keys": {"products.csv": ["ML-001"], "customers.csv": ["0099"]},
          "counts": {"products.csv": 683, "customers.csv": 3418},
          "uploaded_images": ["ML-001.jpg"]
        }
    """
    org = executor.one(ORG_BY_SHORTNAME, {"shortname": shortname})
    if not org:
        raise ValueError(
            f"Org '{shortname}' not found in organizations table. "
            f"Check the shortname spelling."
        )
    org_id = org["id"]

    live: Dict = {
        "shortname": shortname,
        "queried_at": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
    }

    # -- Price levels --
    try:
        rows = executor.all(PRICE_LEVELS, {"org_id": org_id})
        live["price_levels"] = [r["code"] for r in rows]
    except Exception as exc:
        live.setdefault("_warnings", []).append(f"price_levels: {exc}")

    # -- Custom fields (table names unverified — degrade gracefully) --
    custom_fields: Dict[str, List[str]] = {}
    for key, query in (
        ("products",  CUSTOM_FIELDS_PRODUCTS),
        ("customers", CUSTOM_FIELDS_CUSTOMERS),
        ("inventory", CUSTOM_FIELDS_INVENTORY),
    ):
        try:
            rows = executor.all(query, {"org_id": org_id})
            custom_fields[key] = [r["name"] for r in rows]
        except Exception as exc:
            live.setdefault("_warnings", []).append(
                f"custom_fields.{key}: {exc} — "
                f"supply via --custom-fields or verify table name"
            )
    if custom_fields:
        live["custom_fields"] = custom_fields

    # -- Taxonomy codes (from live products) --
    try:
        rows = executor.all(TAXONOMY_CODES_LIVE, {"org_id": org_id})
        live_codes = sorted({r["code"] for r in rows if r.get("code")})
    except Exception as exc:
        live_codes = []
        live.setdefault("_warnings", []).append(f"taxonomy.codes: {exc}")

    # -- Taxonomy groups --
    try:
        rows = executor.all(TAXONOMY_GROUPS, {"org_id": org_id})
        live_groups = [r["code"] for r in rows]
    except Exception as exc:
        live_groups = []
        live.setdefault("_warnings", []).append(
            f"taxonomy.groups: {exc} — verify product_groups table name"
        )

    if live_codes or live_groups:
        live["taxonomy"] = {"codes": live_codes, "groups": live_groups}

    # -- Fingerprint keys: all active product BaseItemCodes + all customer codes --
    keys: Dict[str, List[str]] = {}
    try:
        rows = executor.all(PRODUCT_KEYS_SAMPLE, {"org_id": org_id})
        keys["products.csv"] = [r["item_number"] for r in rows]
    except Exception as exc:
        live.setdefault("_warnings", []).append(f"keys.products: {exc}")

    try:
        rows = executor.all(CUSTOMER_KEYS_SAMPLE, {"org_id": org_id})
        keys["customers.csv"] = [r["code"] for r in rows]
    except Exception as exc:
        live.setdefault("_warnings", []).append(f"keys.customers: {exc}")

    if keys:
        live["keys"] = keys

    # -- Live counts (for omission / row-count checks) --
    counts: Dict[str, int] = {}
    try:
        row = executor.one(PRODUCT_COUNTS, {"org_id": org_id})
        if row:
            counts["products.csv"] = row["active_products"]
    except Exception as exc:
        live.setdefault("_warnings", []).append(f"counts.products: {exc}")

    try:
        row = executor.one(CUSTOMER_COUNT, {"org_id": org_id})
        if row:
            counts["customers.csv"] = row["total_customers"]
    except Exception as exc:
        live.setdefault("_warnings", []).append(f"counts.customers: {exc}")

    try:
        row = executor.one(INVENTORY_COUNTS, {"org_id": org_id})
        if row:
            counts["inventory.csv"] = row["total_inventory_rows"]
    except Exception as exc:
        live.setdefault("_warnings", []).append(f"counts.inventory: {exc}")

    if counts:
        live["counts"] = counts

    # -- Uploaded images (product_images table) --
    try:
        rows = executor.all(UPLOADED_IMAGES, {"org_id": org_id})
        live["uploaded_images"] = [r.get("filename") or r.get("name", "") for r in rows]
    except Exception as exc:
        live.setdefault("_warnings", []).append(
            f"uploaded_images: {exc} — "
            f"verify column name (filename vs name) in product_images"
        )

    return live


# ---------------------------------------------------------------------------
# Supplemental queries — not in live-state JSON but used by profile diff
# ---------------------------------------------------------------------------

def query_full_counts(executor: Executor, org_id: int) -> Dict:
    """Query all factual counts used by the profile reconciler.

    Returns a dict with keys matching LiveState fields.
    Missing / errored fields are absent (caller handles gracefully).
    """
    out: Dict = {}

    try:
        row = executor.one(PRODUCT_COUNTS, {"org_id": org_id})
        if row:
            out["products_active"] = row["active_products"]
            out["products_with_images"] = row["active_with_images"]
    except Exception:
        pass

    try:
        row = executor.one(CUSTOMER_COUNT, {"org_id": org_id})
        if row:
            out["customers"] = row["total_customers"]
    except Exception:
        pass

    try:
        row = executor.one(INVENTORY_COUNTS, {"org_id": org_id})
        if row:
            out["inventory_rows"] = row["total_inventory_rows"]
    except Exception:
        pass

    try:
        row = executor.one(ORPHAN_INVENTORY, {"org_id": org_id})
        if row:
            out["orphan_inventory"] = row["orphan_inventory_rows"]
    except Exception:
        pass

    try:
        rows = executor.all(PRICE_LEVELS, {"org_id": org_id})
        out["price_level_codes"] = sorted(r["code"] for r in rows)
    except Exception:
        pass

    try:
        row = executor.one(ORPHAN_OPTIONS, {"org_id": org_id})
        if row:
            out["options"] = row["total_options"]
            out["option_groups"] = row["total_option_groups"]
    except Exception:
        pass

    try:
        org_row = executor.one(
            "SELECT properties->>'status' AS lifecycle FROM organizations WHERE id = %(id)s",
            {"id": org_id},
        )
        if org_row:
            out["lifecycle"] = org_row.get("lifecycle") or "unknown"
    except Exception:
        pass

    return out


# ---------------------------------------------------------------------------
# CLI — print query SQL or list all queries
# ---------------------------------------------------------------------------

def _cli_main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Named query library — print SQL or list all queries.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--list", action="store_true",
                       help="list all named queries with descriptions")
    group.add_argument("--print", metavar="NAME",
                       help="print the SQL for a named query (e.g. PRODUCT_COUNTS)")
    args = ap.parse_args()

    if args.list:
        print(f"{'Name':<35}  Description")
        print("-" * 35 + "  " + "-" * 50)
        for name, (_, desc) in sorted(QUERIES.items()):
            short = desc.split(".")[0][:70]
            print(f"{name:<35}  {short}")
        return 0

    name = args.print.upper()
    if name not in QUERIES:
        closest = [k for k in QUERIES if name in k]
        hint = f"\nDid you mean: {closest}" if closest else ""
        print(f"Unknown query '{name}'. Run --list to see all names.{hint}",
              file=sys.stderr)
        return 1

    sql, desc = QUERIES[name]
    print(f"-- {name}")
    print(f"-- {desc}")
    print()
    print(sql)
    return 0


if __name__ == "__main__":
    sys.exit(_cli_main())
