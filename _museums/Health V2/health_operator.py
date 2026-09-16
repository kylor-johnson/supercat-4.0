#!/usr/bin/env python3
"""
Health Intelligence v2 — Operator

Reads README.md (scoring spec) and QUERIES.md (data retrieval spec),
executes all queries, scores every eligible entity, outputs a single CSV.

Usage:
    python health_operator.py --mal /path/to/master_account_list.csv
    python health_operator.py --mal /path/to/mal.csv --skip-postgres
    python health_operator.py --mal /path/to/mal.csv --exclusion-list /path/to/exclusions.csv

Requirements:
    pip install google-cloud-bigquery psycopg2-binary pandas numpy
"""

import argparse
import os
import sys
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from google.cloud import bigquery

# ============================================================================
# SECTION 0 — CONFIGURATION, THRESHOLDS, BUNDLE DEFINITIONS
# ============================================================================

BQ_PROJECT = "supercat-data-pipeline"

# --- §4.1 Engagement: login_intensity thresholds ---
LOGIN_INTENSITY_THRESHOLDS = [(50, 100), (35, 80), (20, 60), (10, 40), (0.01, 20), (0, 0)]

# --- §4.1 Engagement: active_user_ratio thresholds ---
ACTIVE_USER_RATIO_THRESHOLDS = [(0.30, 100), (0.20, 80), (0.10, 60), (0.05, 40), (0.001, 20), (0, 0)]

# --- §4.3 Value Delivery: presentation_actions thresholds ---
PRESENTATION_THRESHOLDS = [(1000, 100), (500, 80), (100, 60), (50, 40), (0.01, 20), (0, 0)]

# --- §4.3 Value Delivery: order_volume thresholds ---
ORDER_VOLUME_THRESHOLDS = [(500, 100), (200, 80), (50, 60), (20, 40), (0.01, 20), (0, 0)]

# --- §4.3 Value Delivery: customer_activation_rate thresholds ---
CUSTOMER_ACTIVATION_THRESHOLDS = [(0.30, 100), (0.20, 80), (0.10, 60), (0.05, 40), (0.001, 20), (0, 0)]

# --- §4.3 Value Delivery: eol_share thresholds ---
EOL_SHARE_THRESHOLDS = [(0.40, 100), (0.25, 80), (0.15, 60), (0.05, 40), (0.001, 20), (0, 0)]

# --- §4.3 Value Delivery: portal_engagement thresholds ---
PORTAL_ENGAGEMENT_THRESHOLDS = [(300, 100), (150, 80), (50, 60), (20, 40), (0.01, 20), (0, 0)]

# --- §4.4 Operational Health: catalog_completeness thresholds ---
CATALOG_COMPLETENESS_THRESHOLDS = [(0.95, 100), (0.85, 80), (0.75, 60), (0.60, 40), (0.40, 20), (0, 0)]

# --- §4.4 Operational Health: data_freshness (days_since) thresholds ---
# Lower is better, so order is reversed
DATA_FRESHNESS_THRESHOLDS = [(7, 100), (30, 80), (60, 60), (90, 40), (180, 20)]
DATA_FRESHNESS_DEFAULT = 0  # > 180 days

# --- §4.5 Trajectory: value_trend thresholds ---
VALUE_TREND_THRESHOLDS = [(0.20, 100), (0.10, 80), (-0.05, 60), (-0.15, 40), (-0.30, 20)]
VALUE_TREND_DEFAULT = 0

# --- §4.5 Trajectory: login_trend thresholds ---
LOGIN_TREND_THRESHOLDS = [(0.15, 100), (0.05, 80), (-0.05, 60), (-0.15, 40), (-0.30, 20)]
LOGIN_TREND_DEFAULT = 0

# --- §6.3 Customer Headroom: dormant_customers thresholds ---
DORMANT_THRESHOLDS = [(100, 100), (50, 80), (20, 60), (5, 40), (0.01, 20), (0, 0)]

# --- §6.3 Customer Headroom: activation_headroom (1 - activation_rate) thresholds ---
ACTIVATION_HEADROOM_THRESHOLDS = [(0.80, 100), (0.60, 80), (0.40, 60), (0.20, 40), (0, 20)]

# --- §6.3 Customer Headroom: geographic_cv thresholds ---
GEOGRAPHIC_CV_THRESHOLDS = [(1.0, 100), (0.7, 80), (0.5, 60), (0.3, 40), (0, 20)]

# --- §4 Health dimension weights ---
HEALTH_WEIGHTS = {
    "engagement": 0.25,
    "adoption": 0.20,
    "value_delivery": 0.30,
    "operational_health": 0.15,
    "trajectory": 0.10,
}

# --- §6 Growth component base weights ---
GROWTH_WEIGHTS = {
    "bundle_upgrade_signal": 0.30,
    "feature_gap": 0.25,
    "customer_headroom": 0.25,
    "peer_benchmark_gap": 0.20,
}

# --- §7 Health bands ---
HEALTH_BANDS = [(80, "Thriving"), (60, "Healthy"), (40, "Watch"), (20, "At Risk"), (0, "Critical")]

# --- §7 Growth bands ---
GROWTH_BANDS = [(80, "Prime"), (60, "Ready"), (40, "Developing"), (0, "Not Ready")]

# --- §2 Bundle definitions ---
# features_available: list of feature numbers (1-10) that apply
# value_delivery_type: which formula to use
# growth_components: which Growth components apply
# primary_value_metric: for trajectory
BUNDLE_CONFIG = {
    "iPad-only": {
        "features_available": [1, 2, 3, 4, 5, 6, 7],
        "value_delivery_type": "presentation",
        "growth_components": ["bundle_upgrade_signal", "feature_gap", "peer_benchmark_gap"],
        "primary_value_metric": "presentation_actions",
    },
    "iPad+Catalog": {
        "features_available": [1, 2, 3, 4, 5, 6, 7, 8],
        "value_delivery_type": "presentation",
        "growth_components": ["bundle_upgrade_signal", "feature_gap", "peer_benchmark_gap"],
        "primary_value_metric": "presentation_actions",
    },
    "iPad+Catalog+Cart": {
        "features_available": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "value_delivery_type": "order",
        "growth_components": ["bundle_upgrade_signal", "feature_gap", "customer_headroom", "peer_benchmark_gap"],
        "primary_value_metric": "orders_90d",
    },
    "iPad+Catalog+Portal": {
        "features_available": [1, 2, 3, 4, 5, 6, 7, 8, 10],
        "value_delivery_type": "presentation_portal",
        "growth_components": ["bundle_upgrade_signal", "feature_gap", "peer_benchmark_gap"],
        "primary_value_metric": "presentation_portal_avg",
    },
    "Full": {
        "features_available": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "value_delivery_type": "full",
        "growth_components": ["feature_gap", "customer_headroom", "peer_benchmark_gap"],
        "primary_value_metric": "orders_90d",
    },
}

# --- §4.2 Adoption: feature definitions ---
# Maps feature number to (metric_name, threshold, special_rule)
FEATURE_CATALOG = {
    1: ("mp_search_products", 50, None),
    2: ("mp_select_a_customer", 20, None),
    3: ("mp_item_added_via_magic_button", 20, None),
    4: ("mp_item_email_drafted", 10, None),
    5: ("mp_create_pdf_catalog", 5, None),
    6: ("mp_view_document", 50, None),
    7: ("smart_stack_count", 0, "gte1"),  # ≥ 1
    8: (None, None, "ecat_online"),  # has_catalog AND portal_visitors > 0
    9: ("mp_submit_order", 10, None),
    10: ("mp_access_sales_portal", 10, None),
}

# --- §2 QUERIES.md validated Mixpanel event mapping ---
EXPECTED_MIXPANEL_EVENTS = [
    "api_access",
    "product_search",
    "customer_selection",
    "item_added_via_magic_button",
    "item_email_drafted",
    "pdf_catalog_generated",
    "view_document",
    "order_submitted",
    "view_portal",
    "add_configured_item_to_order",
    "document_email_drafted",
]

# --- MAL column aliases (known variant column names) ---
MAL_COLUMN_ALIASES = {
    "stack": "bundle",
    "ord_id": "org_shortname",
}

# --- MAL bundle normalization (stack values → canonical bundle names) ---
BUNDLE_NORMALIZATION = {
    "ipad-only": "iPad-only",
    "ipad only": "iPad-only",
    "ipad+catalog": "iPad+Catalog",
    "ipad + catalog": "iPad+Catalog",
    "ipad+catalog+cart": "iPad+Catalog+Cart",
    "ipad + catalog + cart": "iPad+Catalog+Cart",
    "ipad+catalog+portal": "iPad+Catalog+Portal",
    "ipad + catalog + portal": "iPad+Catalog+Portal",
    "full": "Full",
    "full (cart+portal)": "Full",
    "full (cart + portal)": "Full",
}
VALID_BUNDLES = set(BUNDLE_CONFIG.keys())

# --- MAL company → org_shortname override for names that don't exact-match org_summary ---
MAL_COMPANY_OVERRIDES = {
    "designer's fountain": "df",
    "america's backyards": "abol",
    "globalux": "gblx",
    "summer classics ( wholesale)": "scw",
    "summer classics (wholesale)": "scw",
    "sabine pools, spas, & furnitur": "sp",
}

# --- §1 Exclusion patterns (safety net; primary gate is subscriptions.status) ---
SHORTNAME_EXCLUDE_PATTERNS = ["test", "demo", "staging", "sandbox", "template"]
ORGNAME_EXCLUDE_PATTERNS = ["test account", "demo org", "sample", "don't use", "for jimmy"]

# Non-real orgs: demo, staging, internal, and template accounts.
# This set is the primary defence against non-real orgs leaking into scoring.
# Updated 2026-04-06 to include all audited non-real orgs from the full org list.
KNOWN_INTERNAL_ORGS = {
    # Legacy internal / template
    "bmc2", "bmc3", "temp", "tmpl", "tmpo", "tech", "tle", "vc", "wmo",
    # Explicit demo accounts
    "demo", "demo1", "demo2", "demo3", "demolighting", "ei", "hl", "kylademo",
    "emerydemo", "waledemo",
    # Client-specific test/staging environments
    "ahtest", "bc2", "bri_test", "clctest", "pf_test", "wwtest", "ufitest",
    "ufistaging", "mhstage", "fmsstaging", "tlastaging", "vcgstaging",
    "fccstaging", "bpstaging", "tam-staging", "cfsd", "slusa",
    # Other non-real
    "gww", "sc_test", "sic", "ctest", "test1", "omc",
}


# ============================================================================
# SECTION 1 — CONNECTION SETUP
# ============================================================================

def connect_bigquery() -> bigquery.Client:
    """Connect to BigQuery using google-cloud-bigquery client.

    Relies on GOOGLE_APPLICATION_CREDENTIALS env var or Application Default
    Credentials.
    """
    try:
        client = bigquery.Client(project=BQ_PROJECT)
        client.query("SELECT 1").result()
        print("[OK] BigQuery connected")
        return client
    except Exception as e:
        print(f"[FATAL] BigQuery connection failed: {e}")
        sys.exit(1)


def connect_postgres(skip_postgres: bool):
    """Connect to Postgres following existing repo convention.

    Checks DATABASE_URL first, then PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD.
    Returns connection or None (if --skip-postgres).
    """
    if skip_postgres:
        print("[WARN] --skip-postgres passed. All Postgres-dependent metrics will be missing.")
        print("       Scoring status will be forced to 'partial' for all entities.")
        return None

    try:
        import psycopg2
    except ImportError:
        print("[FATAL] psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(1)

    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            conn = psycopg2.connect(db_url)
            conn.set_session(readonly=True, autocommit=True)
            print("[OK] Postgres connected via DATABASE_URL")
            return conn
        except Exception as e:
            print(f"[FATAL] Postgres connection via DATABASE_URL failed: {e}")
            sys.exit(1)

    pg_host = os.environ.get("PGHOST")
    pg_port = os.environ.get("PGPORT", "5432")
    pg_db = os.environ.get("PGDATABASE", "supercat_production")
    pg_user = os.environ.get("PGUSER", "postgres")
    pg_pass = os.environ.get("PGPASSWORD", "")

    if not pg_host:
        print("[FATAL] No Postgres credentials found.")
        print("        Set DATABASE_URL or PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD.")
        print("        Or pass --skip-postgres to run without Postgres (partial scoring).")
        sys.exit(1)

    try:
        conn = psycopg2.connect(
            host=pg_host, port=pg_port, dbname=pg_db,
            user=pg_user, password=pg_pass,
        )
        conn.set_session(readonly=True, autocommit=True)
        print(f"[OK] Postgres connected ({pg_host}:{pg_port}/{pg_db})")
        return conn
    except Exception as e:
        print(f"[FATAL] Postgres connection failed: {e}")
        print("        Pass --skip-postgres to run without Postgres (partial scoring).")
        sys.exit(1)


# ============================================================================
# SECTION 2 — PREFLIGHT CHECKS
# ============================================================================

def preflight_hubspot_join(bq: bigquery.Client) -> bool:
    """PF-1: Verify org_summary → hubspot.company join key coverage."""
    query = """
    SELECT
      COUNT(*) AS total_orgs,
      COUNTIF(hubspot_company_id IS NOT NULL) AS with_hs_id
    FROM `supercat-data-pipeline.insightful_product.org_summary`
    """
    row = next(bq.query(query).result())
    total = row["total_orgs"]
    with_id = row["with_hs_id"]
    ratio = with_id / total if total > 0 else 0
    if ratio < 0.80:
        print(f"[FAIL] PF-1: HubSpot join key coverage {ratio:.0%} < 80% ({with_id}/{total})")
        return False
    print(f"[PASS] PF-1: HubSpot join key coverage {ratio:.0%} ({with_id}/{total})")
    return True


def preflight_mixpanel_attribution(bq: bigquery.Client) -> bool:
    """PF-2: Verify combined Mixpanel org attribution (both fields) covers ≥100 distinct orgs."""
    query = """
    SELECT COUNT(DISTINCT COALESCE(
      NULLIF(organization_shortname, ''),
      NULLIF(current_organization_shortname, '')
    )) AS org_count
    FROM `supercat-data-pipeline.mixpanel.events`
    WHERE DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))
          >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
      AND COALESCE(
            NULLIF(organization_shortname, ''),
            NULLIF(current_organization_shortname, '')
          ) IS NOT NULL
    """
    row = next(bq.query(query).result())
    org_count = row["org_count"]
    if org_count < 100:
        print(f"[FAIL] PF-2: Mixpanel org attribution covers {org_count} orgs (need ≥100)")
        return False
    print(f"[PASS] PF-2: Mixpanel org attribution covers {org_count} orgs")
    return True


def preflight_mixpanel_event_map(bq: bigquery.Client) -> bool:
    """PF-3: Verify all expected Mixpanel event names exist in recent data."""
    events_str = ", ".join(f"'{e}'" for e in EXPECTED_MIXPANEL_EVENTS)
    query = f"""
    SELECT event_name, COUNT(*) AS cnt
    FROM `supercat-data-pipeline.mixpanel.events`
    WHERE event_name IN ({events_str})
      AND DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))
          >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    GROUP BY event_name
    """
    result = bq.query(query).result()
    found = {row["event_name"] for row in result}
    missing = set(EXPECTED_MIXPANEL_EVENTS) - found
    if len(missing) >= 3:
        print(f"[FAIL] PF-3: {len(missing)} expected Mixpanel events missing: {sorted(missing)}")
        return False
    if missing:
        print(f"[WARN] PF-3: Missing Mixpanel events (non-fatal): {sorted(missing)}")
    else:
        print(f"[PASS] PF-3: All {len(EXPECTED_MIXPANEL_EVENTS)} expected Mixpanel events present")
    return True


def preflight_postgres_orgs(pg) -> bool:
    """PF-4: Verify organizations.shortname is populated."""
    if pg is None:
        print("[SKIP] PF-4: Postgres not connected (cache mode or --skip-postgres)")
        return True
    cur = pg.cursor()
    cur.execute("SELECT COUNT(*) FROM organizations WHERE shortname IS NOT NULL AND shortname != ''")
    count = cur.fetchone()[0]
    cur.close()
    if count < 50:
        print(f"[FAIL] PF-4: Only {count} orgs with shortname in Postgres (need ≥50)")
        return False
    print(f"[PASS] PF-4: {count} orgs with shortname in Postgres")
    return True


def run_preflight(bq: bigquery.Client, pg) -> None:
    """Run all preflight checks. Halt on any blocking failure."""
    print("\n=== PREFLIGHT CHECKS ===")
    results = [
        preflight_hubspot_join(bq),
        preflight_mixpanel_attribution(bq),
        preflight_mixpanel_event_map(bq),
        preflight_postgres_orgs(pg),
    ]
    if not all(results):
        print("\n[FATAL] Preflight failed. Fix the issues above before scoring.")
        sys.exit(1)
    print("=== ALL PREFLIGHT CHECKS PASSED ===\n")


# ============================================================================
# SECTION 3 — DATA LOADERS
# ============================================================================

def load_master_account_list(path: str, bq: bigquery.Client) -> pd.DataFrame:
    """Q-MAL: Load and validate the Master Account List CSV.

    Handles column aliasing (stack → bundle) and bundle normalization.
    If org_shortname is missing, resolves company → org_shortname via org_summary.
    """
    if not os.path.exists(path):
        print(f"[FATAL] Master Account List not found: {path}")
        sys.exit(1)

    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]

    # Handle Google Sheets exports: skip empty header rows, drop index columns
    unnamed_cols = [c for c in df.columns if c.startswith("unnamed")]
    if len(unnamed_cols) == len(df.columns):
        # Header row is likely offset — re-read skipping blank rows
        df = pd.read_csv(path, skiprows=1)
        df.columns = [c.strip().lower() for c in df.columns]
    unnamed_cols = [c for c in df.columns if c.startswith("unnamed")]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    for alias, canonical in MAL_COLUMN_ALIASES.items():
        if alias in df.columns and canonical not in df.columns:
            df = df.rename(columns={alias: canonical})

    # --- Resolve org_shortname ---
    if "org_shortname" not in df.columns:
        if "company" not in df.columns:
            print("[FATAL] MAL CSV must contain 'org_shortname' or 'company' column.")
            print(f"        Found columns: {list(df.columns)}")
            sys.exit(1)

        print("[INFO] MAL lacks 'org_shortname'. Resolving 'company' via org_summary...")
        org_ref = _load_org_name_lookup(bq)
        df["company_clean"] = df["company"].str.strip().str.lower()
        df["org_shortname"] = df["company_clean"].map(MAL_COMPANY_OVERRIDES)
        override_count = df["org_shortname"].notna().sum()
        if override_count > 0:
            print(f"[OK] {override_count} company names resolved via MAL_COMPANY_OVERRIDES")
        remaining = df[df["org_shortname"].isna()].copy()
        resolved = df[df["org_shortname"].notna()].copy()
        remaining = remaining.drop(columns=["org_shortname"])
        remaining = remaining.merge(org_ref, left_on="company_clean",
                                    right_on="org_name_lower", how="left")
        df = pd.concat([resolved, remaining], ignore_index=True)
        unresolved = df[df["org_shortname"].isna()]
        if len(unresolved) > 0:
            print(f"[WARN] {len(unresolved)} MAL rows could not be resolved to org_shortname (dropped):")
            for _, row in unresolved.head(20).iterrows():
                print(f"         - {row.get('company', 'N/A')}")
            if len(unresolved) > 20:
                print(f"         ... and {len(unresolved) - 20} more")
            df = df[df["org_shortname"].notna()].copy()
        df = df.drop(columns=["company_clean", "org_name_lower"], errors="ignore")
        print(f"[OK] Resolved {len(df)} company names to org_shortname")

    # --- Normalize bundle ---
    if "bundle" not in df.columns:
        print(f"[FATAL] MAL CSV must contain 'bundle' (or 'stack') column.")
        print(f"        Found columns: {list(df.columns)}")
        sys.exit(1)

    raw_bundles = df["bundle"].str.strip()
    df["bundle"] = raw_bundles.str.lower().map(BUNDLE_NORMALIZATION)
    invalid_mask = df["bundle"].isna()
    if invalid_mask.any():
        bad_vals = raw_bundles[invalid_mask].unique().tolist()
        print(f"[FATAL] {invalid_mask.sum()} MAL rows have unrecognized bundle values: {bad_vals}")
        print("        Check BUNDLE_NORMALIZATION in operator.py or fix the MAL CSV.")
        sys.exit(1)

    if "parent_entity" not in df.columns:
        df["parent_entity"] = None

    df["org_shortname"] = df["org_shortname"].str.strip().str.lower()
    df["parent_entity"] = df["parent_entity"].fillna("").str.strip().str.lower().replace("", None)

    for col in ["arr", "mrr", "cohort_year"]:
        if col not in df.columns:
            df[col] = None

    result = df[["org_shortname", "parent_entity", "bundle", "arr", "mrr", "cohort_year"]].drop_duplicates(subset=["org_shortname"])

    for col in ["arr", "mrr"]:
        if col in result.columns:
            result[col] = pd.to_numeric(
                result[col].astype(str).str.replace(r"[$,]", "", regex=True),
                errors="coerce"
            )
    print(f"[OK] Q-MAL: {len(result)} entities loaded from Master Account List")
    for bundle, count in result["bundle"].value_counts().items():
        print(f"       {bundle}: {count}")
    return result


def _load_org_name_lookup(bq: bigquery.Client) -> pd.DataFrame:
    """Build org_name → org_shortname lookup from org_summary."""
    query = """
    SELECT org_shortname, org_name
    FROM `supercat-data-pipeline.insightful_product.org_summary`
    WHERE org_shortname IS NOT NULL AND org_name IS NOT NULL
    """
    df = bq.query(query).to_dataframe()
    df["org_name_lower"] = df["org_name"].str.strip().str.lower()
    return df[["org_shortname", "org_name_lower"]]


def load_org_reference(bq: bigquery.Client) -> pd.DataFrame:
    """Q-ORG: Load org_summary reference fields."""
    query = """
    SELECT
      org_shortname,
      org_name,
      hubspot_company_id,
      has_clicky_portal,
      portal_visitors_daily
    FROM `supercat-data-pipeline.insightful_product.org_summary`
    WHERE org_shortname IS NOT NULL
    """
    df = bq.query(query).to_dataframe()
    print(f"[OK] Q-ORG: {len(df)} rows from org_summary")
    return df


def load_hubspot_eligibility(bq: bigquery.Client) -> pd.DataFrame:
    """Q-HS: Load HubSpot eligibility fields via org_summary join."""
    query = """
    SELECT
      os.org_shortname,
      hc.properties_engagement_status AS engagement_status,
      hc.properties_type AS hs_type,
      hc.properties_annualrevenue AS hs_annual_revenue
    FROM `supercat-data-pipeline.insightful_product.org_summary` os
    JOIN `supercat-data-pipeline.hubspot.company` hc
      ON os.hubspot_company_id = hc.company_id
    WHERE os.org_shortname IS NOT NULL
      AND os.hubspot_company_id IS NOT NULL
    """
    df = bq.query(query).to_dataframe()
    df["engagement_status"] = df["engagement_status"].fillna("").str.strip()
    df["hs_type"] = df["hs_type"].fillna("").str.strip()
    print(f"[OK] Q-HS: {len(df)} rows from HubSpot")
    return df


def filter_eligible_entities(
    mal_df: pd.DataFrame,
    org_df: pd.DataFrame,
    hs_df: pd.DataFrame,
    sub_df: pd.DataFrame,
    exclusion_list: Optional[set],
) -> pd.DataFrame:
    """Intersect MAL ∩ active-subscription orgs, apply exclusions, emit HubSpot/ARR warnings.

    Eligibility gate (v2.4+):
      INCLUDE if: MAL member + valid org + at least one active subscription
                  + not demo/test/internal + not on explicit exclusion list
      EXCLUDE if: no active subscription, explicit exclusion, or known internal org

    HubSpot lifecycle status and ARR are demoted to warning flags only.
    They do NOT block scoring.
    """
    org_dedup = org_df.drop_duplicates(subset=["org_shortname"], keep="first")
    hs_dedup = hs_df.drop_duplicates(subset=["org_shortname"], keep="first")
    sub_dedup = sub_df.drop_duplicates(subset=["org_shortname"], keep="first") if len(sub_df) > 0 else pd.DataFrame(columns=["org_shortname", "has_active_sub"])

    merged = mal_df.merge(org_dedup, on="org_shortname", how="left")
    # Left-join HubSpot for warning flags only — not used for gating
    merged = merged.merge(hs_dedup[["org_shortname", "engagement_status", "hs_type"]],
                          on="org_shortname", how="left")
    # Left-join subscription status — this IS the eligibility gate
    merged = merged.merge(sub_dedup[["org_shortname", "has_active_sub"]],
                          on="org_shortname", how="left")

    initial_count = len(merged)

    # --- Primary gate: active subscription ---
    has_active = merged["has_active_sub"].infer_objects(copy=False).fillna(False).astype(bool)
    no_sub_orgs = merged.loc[~has_active, "org_shortname"].tolist()
    if no_sub_orgs:
        print(f"[EXCL] No active subscription ({len(no_sub_orgs)}): {sorted(no_sub_orgs)}")
    merged = merged[has_active].copy()
    after_sub = len(merged)

    # --- Demo/test/internal exclusion ---
    merged = apply_exclusion_patterns(merged, exclusion_list)
    after_excl = len(merged)

    # --- Warning flags: HubSpot lifecycle ---
    eng = merged["engagement_status"].fillna("")
    hs_t = merged["hs_type"].fillna("")
    merged["hs_lifecycle_stale"] = (
        eng.isin(["Lost", "Churn"])
        | ((eng == "") & (hs_t == ""))
    )
    merged["hs_join_missing"] = eng == ""

    stale_n = merged["hs_lifecycle_stale"].sum()
    missing_n = merged["hs_join_missing"].sum()
    if stale_n:
        print(f"[WARN] hs_lifecycle_stale: {stale_n} orgs have HubSpot Lost/Churn or no HS record "
              f"(not excluded, warning only)")
    if missing_n:
        print(f"[WARN] hs_join_missing: {missing_n} orgs have no HubSpot join (not excluded, warning only)")

    # --- Warning flags: ARR data ---
    if "arr" in merged.columns:
        arr_num = pd.to_numeric(merged["arr"], errors="coerce")
        merged["arr_data_gap"] = arr_num.isna() | (arr_num <= 0)
        arr_gap_n = merged["arr_data_gap"].sum()
        if arr_gap_n:
            print(f"[WARN] arr_data_gap: {arr_gap_n} orgs have NULL/zero ARR "
                  f"(not excluded, warning only)")
    else:
        merged["arr_data_gap"] = False

    print(f"[OK] Eligibility: {initial_count} MAL → {after_sub} active-subscription "
          f"→ {after_excl} after demo/test/internal exclusions  [HubSpot/ARR are warnings only]")
    return merged


def apply_exclusion_patterns(df: pd.DataFrame, exclusion_list: Optional[set]) -> pd.DataFrame:
    """Apply README §1 exclusion criteria: patterns + known internals + explicit list."""
    mask = pd.Series(True, index=df.index)

    sn = df["org_shortname"].str.lower()
    for pat in SHORTNAME_EXCLUDE_PATTERNS:
        mask &= ~sn.str.contains(pat, na=False)

    if "org_name" in df.columns:
        on = df["org_name"].fillna("").str.lower()
        for pat in ORGNAME_EXCLUDE_PATTERNS:
            mask &= ~on.str.contains(pat, na=False)

    mask &= ~df["org_shortname"].isin(KNOWN_INTERNAL_ORGS)

    if exclusion_list:
        mask &= ~df["org_shortname"].isin(exclusion_list)

    return df[mask].copy()


def _arr_source_annotation(df: pd.DataFrame) -> pd.DataFrame:
    """Annotate arr_source. ARR is now sourced from MAL CSV for all orgs."""
    df = df.copy()
    df["arr_source"] = "mal_csv"
    return df


def load_mixpanel_metrics(bq: bigquery.Client) -> pd.DataFrame:
    """Q-MP: Batch load all Mixpanel behavioral metrics with org attribution CTE."""
    query = """
    WITH all_events AS (
      SELECT
        LOWER(COALESCE(
          NULLIF(organization_shortname, ''),
          NULLIF(current_organization_shortname, '')
        )) AS org_shortname,
        event_name,
        distinct_id,
        CASE
          WHEN DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))
               >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) THEN 'current'
          ELSE 'prior'
        END AS period
      FROM `supercat-data-pipeline.mixpanel.events`
      WHERE DATE(TIMESTAMP_SECONDS(CAST(time AS INT64)))
            >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY)
        AND COALESCE(
              NULLIF(organization_shortname, ''),
              NULLIF(current_organization_shortname, '')
            ) IS NOT NULL
    ),
    login_metrics AS (
      SELECT
        org_shortname,
        COUNTIF(event_name = 'api_access' AND period = 'current') AS logins_90d,
        COUNTIF(event_name = 'api_access' AND period = 'prior') AS logins_prior_90d,
        COUNT(DISTINCT CASE
          WHEN event_name = 'api_access' AND period = 'current'
          THEN distinct_id END) AS active_users_90d
      FROM all_events
      GROUP BY org_shortname
    ),
    feature_metrics AS (
      SELECT
        org_shortname,
        COUNTIF(event_name = 'product_search' AND period = 'current') AS mp_search_products,
        COUNTIF(event_name = 'customer_selection' AND period = 'current') AS mp_select_a_customer,
        COUNTIF(event_name = 'item_added_via_magic_button' AND period = 'current') AS mp_item_added_via_magic_button,
        COUNTIF(event_name = 'item_email_drafted' AND period = 'current') AS mp_item_email_drafted,
        COUNTIF(event_name = 'pdf_catalog_generated' AND period = 'current') AS mp_create_pdf_catalog,
        COUNTIF(event_name = 'view_document' AND period = 'current') AS mp_view_document,
        COUNTIF(event_name = 'order_submitted' AND period = 'current') AS mp_submit_order,
        COUNTIF(event_name = 'view_portal' AND period = 'current') AS mp_access_sales_portal,
        COUNTIF(event_name = 'add_configured_item_to_order' AND period = 'current') AS mp_order_configured_item,
        COUNTIF(event_name = 'document_email_drafted' AND period = 'current') AS mp_document_email_drafted,
        COUNTIF(event_name = 'item_added_via_magic_button' AND period = 'prior')
        + COUNTIF(event_name = 'item_email_drafted' AND period = 'prior')
        + COUNTIF(event_name = 'pdf_catalog_generated' AND period = 'prior')
        + COUNTIF(event_name = 'document_email_drafted' AND period = 'prior')
          AS presentation_actions_prior,
        COUNTIF(event_name = 'order_submitted' AND period = 'prior') AS orders_mp_prior_90d,
        COUNTIF(event_name = 'view_portal' AND period = 'prior') AS mp_access_sales_portal_prior
      FROM all_events
      GROUP BY org_shortname
    )
    SELECT
      COALESCE(l.org_shortname, f.org_shortname) AS org_shortname,
      COALESCE(l.logins_90d, 0) AS logins_90d,
      COALESCE(l.logins_prior_90d, 0) AS logins_prior_90d,
      COALESCE(l.active_users_90d, 0) AS active_users_90d,
      COALESCE(f.mp_search_products, 0) AS mp_search_products,
      COALESCE(f.mp_select_a_customer, 0) AS mp_select_a_customer,
      COALESCE(f.mp_item_added_via_magic_button, 0) AS mp_item_added_via_magic_button,
      COALESCE(f.mp_item_email_drafted, 0) AS mp_item_email_drafted,
      COALESCE(f.mp_create_pdf_catalog, 0) AS mp_create_pdf_catalog,
      COALESCE(f.mp_view_document, 0) AS mp_view_document,
      COALESCE(f.mp_submit_order, 0) AS mp_submit_order,
      COALESCE(f.mp_access_sales_portal, 0) AS mp_access_sales_portal,
      COALESCE(f.mp_order_configured_item, 0) AS mp_order_configured_item,
      COALESCE(f.mp_document_email_drafted, 0) AS mp_document_email_drafted,
      COALESCE(f.presentation_actions_prior, 0) AS presentation_actions_prior,
      COALESCE(f.orders_mp_prior_90d, 0) AS orders_mp_prior_90d,
      COALESCE(f.mp_access_sales_portal_prior, 0) AS mp_access_sales_portal_prior
    FROM login_metrics l
    FULL OUTER JOIN feature_metrics f ON l.org_shortname = f.org_shortname
    """
    df = bq.query(query).to_dataframe()
    print(f"[OK] Q-MP: {len(df)} orgs with Mixpanel metrics")
    return df


def _pg_query(pg, sql: str) -> pd.DataFrame:
    """Execute a Postgres query and return a DataFrame, or empty DataFrame if pg is None."""
    if pg is None:
        return pd.DataFrame()
    cur = pg.cursor()
    cur.execute(sql)
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


def _load_pg_cache(cache_dir: str, key: str, pg, loader_fn) -> pd.DataFrame:
    """Load from CSV cache if available, otherwise fall back to live Postgres query."""
    csv_path = os.path.join(cache_dir, f"{key}.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"[OK] {key}: {len(df)} rows (from cache)")
        return df
    return loader_fn(pg)


def load_catalog_completeness(pg, pg_cache_dir=None) -> pd.DataFrame:
    """Q-PG-CAT: Catalog completeness from Postgres. Anchored to organizations."""
    return _pg_query(pg, """
        SELECT
          o.shortname AS org_shortname,
          COUNT(*) FILTER (WHERE p.deleted = false) AS total_active_products,
          COUNT(*) FILTER (
            WHERE p.deleted = false AND p.image_exists = true
            AND p.net_price IS NOT NULL AND p.net_price > 0
          ) AS complete_products,
          CASE WHEN COUNT(*) FILTER (WHERE p.deleted = false) = 0 THEN NULL
          ELSE ROUND(
            COUNT(*) FILTER (
              WHERE p.deleted = false AND p.image_exists = true
              AND p.net_price IS NOT NULL AND p.net_price > 0
            )::numeric / COUNT(*) FILTER (WHERE p.deleted = false)::numeric, 4)
          END AS catalog_completeness
        FROM organizations o
        LEFT JOIN products p ON p.organization_id = o.id
        GROUP BY o.shortname
    """)


def load_import_health(pg) -> pd.DataFrame:
    """Q-PG-IMP: Import health from Postgres."""
    return _pg_query(pg, """
        SELECT
          o.shortname AS org_shortname,
          COUNT(*) FILTER (
            WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
          ) AS total_imports_90d,
          COUNT(*) FILTER (
            WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
            AND ie.data NOT LIKE '%%:error%%'
            AND ie.data NOT LIKE '%%:fatal%%'
          ) AS successful_imports_90d,
          CASE WHEN COUNT(*) FILTER (
            WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days') = 0 THEN NULL
          ELSE ROUND(
            COUNT(*) FILTER (
              WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days'
              AND ie.data NOT LIKE '%%:error%%' AND ie.data NOT LIKE '%%:fatal%%'
            )::numeric / COUNT(*) FILTER (
              WHERE ie.created_at >= CURRENT_DATE - INTERVAL '90 days')::numeric, 4)
          END AS import_success_rate,
          (SELECT CASE
            WHEN ie2.data LIKE '%%:error%%' OR ie2.data LIKE '%%:fatal%%' THEN true
            ELSE false END
           FROM import_events ie2
           WHERE ie2.organization_id = o.id
           ORDER BY ie2.created_at DESC LIMIT 1
          ) AS last_import_had_errors
        FROM organizations o
        LEFT JOIN import_events ie ON ie.organization_id = o.id
        GROUP BY o.id, o.shortname
    """)


def load_order_metrics(pg) -> pd.DataFrame:
    """Q-PG-ORD: Order metrics from Postgres."""
    return _pg_query(pg, """
        SELECT
          o.shortname AS org_shortname,
          COUNT(*) FILTER (
            WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
            AND ord.order_state = 'active') AS orders_90d,
          COUNT(*) FILTER (
            WHERE ord.is_submitted = true
            AND ord.submit_date >= CURRENT_DATE - INTERVAL '180 days'
            AND ord.submit_date < CURRENT_DATE - INTERVAL '90 days'
            AND ord.order_state = 'active') AS orders_prior_90d,
          COUNT(*) FILTER (
            WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
            AND ord.order_state = 'active' AND LOWER(ord.order_source) = 'ipad') AS ipad_orders_90d,
          COUNT(*) FILTER (
            WHERE ord.is_submitted = true AND ord.submit_date >= CURRENT_DATE - INTERVAL '90 days'
            AND ord.order_state = 'active' AND LOWER(ord.order_source) != 'ipad') AS online_orders_90d,
          CASE WHEN COUNT(*) FILTER (WHERE ord.is_submitted = true) > 0
               THEN true ELSE false END AS orders_exist_any_time
        FROM organizations o
        LEFT JOIN orders ord ON ord.organization_id = o.id
        GROUP BY o.shortname
    """)


def load_customer_metrics(pg) -> pd.DataFrame:
    """Q-PG-CUST: Customer activation, dormancy, and geography."""
    return _pg_query(pg, """
        WITH customer_orders AS (
          SELECT o.shortname AS org_shortname, ord.customer_num, ord.ship_to_state,
            MAX(ord.submit_date) AS last_order_date,
            COUNT(*) FILTER (WHERE ord.submit_date >= CURRENT_DATE - INTERVAL '90 days')
              AS orders_current_period
          FROM orders ord JOIN organizations o ON ord.organization_id = o.id
          WHERE ord.is_submitted = true AND ord.order_state = 'active' AND ord.customer_num IS NOT NULL
          GROUP BY o.shortname, ord.customer_num, ord.ship_to_state
        ),
        org_customer_counts AS (
          SELECT o.shortname AS org_shortname, COUNT(c.id) AS total_customers
          FROM organizations o
          LEFT JOIN customers c ON c.organization_id = o.id
          GROUP BY o.shortname
        ),
        activation_metrics AS (
          SELECT org_shortname,
            COUNT(DISTINCT customer_num) FILTER (WHERE orders_current_period > 0) AS ordering_customers_90d,
            COUNT(DISTINCT customer_num) FILTER (
              WHERE orders_current_period = 0 AND last_order_date IS NOT NULL) AS dormant_customers
          FROM customer_orders GROUP BY org_shortname
        ),
        geographic_metrics AS (
          SELECT org_shortname,
            CASE WHEN COUNT(DISTINCT ship_to_state) < 2 THEN 0
            ELSE ROUND(STDDEV(state_order_count)::numeric
                 / NULLIF(AVG(state_order_count), 0)::numeric, 4) END AS geographic_cv
          FROM (
            SELECT org_shortname, ship_to_state, SUM(orders_current_period) AS state_order_count
            FROM customer_orders
            WHERE orders_current_period > 0 AND ship_to_state IS NOT NULL AND ship_to_state != ''
            GROUP BY org_shortname, ship_to_state
          ) state_agg GROUP BY org_shortname
        )
        SELECT occ.org_shortname, occ.total_customers,
          COALESCE(am.ordering_customers_90d, 0) AS ordering_customers_90d,
          COALESCE(am.dormant_customers, 0) AS dormant_customers,
          COALESCE(gm.geographic_cv, 0) AS geographic_cv
        FROM org_customer_counts occ
        LEFT JOIN activation_metrics am ON occ.org_shortname = am.org_shortname
        LEFT JOIN geographic_metrics gm ON occ.org_shortname = gm.org_shortname
    """)


def load_data_freshness(pg) -> pd.DataFrame:
    """Q-PG-FRESH: Data freshness from data_versions."""
    return _pg_query(pg, """
        SELECT
          o.shortname AS org_shortname,
          MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END) AS last_products_update,
          MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END) AS last_customers_update,
          MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END) AS last_inventories_update,
          EXTRACT(DAY FROM (CURRENT_TIMESTAMP - GREATEST(
            COALESCE(MAX(CASE WHEN dv.entity_type = 'products' THEN dv.timestamp END), '1970-01-01'),
            COALESCE(MAX(CASE WHEN dv.entity_type = 'customers' THEN dv.timestamp END), '1970-01-01'),
            COALESCE(MAX(CASE WHEN dv.entity_type = 'inventories' THEN dv.timestamp END), '1970-01-01')
          )))::integer AS days_since_critical_update
        FROM organizations o
        LEFT JOIN data_versions dv ON dv.organization_id = o.id
          AND dv.entity_type IN ('products', 'customers', 'inventories')
        GROUP BY o.shortname
    """)



# --- §4.1 total_users: confirmed internal/admin domains excluded from denominator ---
# Validated 2026-04-07 via V-1 domain census query.
# These domains appear across many client orgs and represent SuperCat staff,
# named seeded accounts, developer accounts, and implementation-partner admin accounts.
# They are NOT client reps and should not inflate the active_user_ratio denominator.
INTERNAL_USER_DOMAINS = frozenset([
    "supercatsolutions.com",  # SuperCat internal staff (221 orgs, 1599 rows) — confirmed
    "jimmythrasher.com",      # Named individual seeded across 47 orgs — confirmed
    "lojic.com",              # SuperCat developer account (33 orgs) — confirmed
    "railsfever.com",         # SuperCat developer account, Wale Olaleye (20 orgs) — confirmed
    "samedis.com",            # SuperCat-adjacent consultant, Rich Powell (18 orgs) — likely
    "upwardtechnologies.com", # Implementation partner, Matt Ridge (16 orgs) — likely
])


def load_user_counts(pg) -> pd.DataFrame:
    """Q-PG-USERS: Total user counts per org. Anchored to organizations.

    Excludes known internal/admin/seeded accounts from the denominator so
    active_user_ratio reflects genuine client-rep populations.
    See INTERNAL_USER_DOMAINS for the validated exclusion list.
    """
    domains_sql = ", ".join(f"'{d}'" for d in sorted(INTERNAL_USER_DOMAINS))
    return _pg_query(pg, f"""
        SELECT
          o.shortname AS org_shortname,
          COUNT(ou.id) FILTER (
            WHERE u.email IS NULL
              OR LOWER(SUBSTRING(u.email::text FROM '@(.+)$')) NOT IN ({domains_sql})
          ) AS total_users
        FROM organizations o
        LEFT JOIN org_users ou ON ou.organization_id = o.id
        LEFT JOIN users u ON u.id = ou.user_id
        GROUP BY o.shortname
    """)


def load_smart_stacks(pg) -> pd.DataFrame:
    """Q-PG-STACKS: Smart stack counts per org. Anchored to organizations."""
    return _pg_query(pg, """
        SELECT o.shortname AS org_shortname, COUNT(ss.id) AS smart_stack_count
        FROM organizations o
        LEFT JOIN smart_stacks ss ON ss.organization_id = o.id
        GROUP BY o.shortname
    """)


def load_subscription_status(pg) -> pd.DataFrame:
    """Q-PG-SUB: Subscription status per org from product billing DB.

    Returns one row per org_shortname with a boolean `has_active_sub` flag.
    An org qualifies if it has at least one subscriptions row where status = 'active'.
    Multiple subscription rows per org are handled by MAX(CASE …).
    """
    return _pg_query(pg, """
        SELECT
          o.shortname AS org_shortname,
          BOOL_OR(s.status = 'active') AS has_active_sub,
          ARRAY_AGG(DISTINCT s.status ORDER BY s.status) AS all_statuses
        FROM organizations o
        LEFT JOIN subscriptions s ON s.organization_id = o.id
        GROUP BY o.shortname
    """)


def load_support_data(bq: bigquery.Client) -> pd.DataFrame:
    """Q-HELP: Support escalations from Help Scout.

    Extracts email domains from primaryCustomer.email and detects escalations via
    TO_JSON_STRING(tags) keyword matching. Returns email_domain (not org_shortname).
    The run() function maps domains to org_shortname using cache/pg_domain_map.csv
    (Postgres-derived; generated by Q-PG-DOMAIN).
    Returns empty gracefully; RM-3 is gated by reliability check downstream.
    """
    try:
        query = """
        SELECT
          LOWER(REGEXP_EXTRACT(
            SAFE.STRING(primaryCustomer.email), r'@(.+)$'
          )) AS possible_org,
          COUNTIF(
            LOWER(TO_JSON_STRING(tags)) LIKE '%escalat%'
            OR LOWER(TO_JSON_STRING(tags)) LIKE '%urgent%'
            OR LOWER(TO_JSON_STRING(tags)) LIKE '%critical%'
          ) AS support_escalations_90d,
          COUNT(*) AS support_conversations_90d
        FROM `supercat-data-pipeline.helpscout.conversations`
        WHERE PARSE_TIMESTAMP('%Y-%m-%dT%H:%M:%S', LEFT(createdAt, 19))
              >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
          AND status != 'spam'
          AND SAFE.STRING(primaryCustomer.email) IS NOT NULL
        GROUP BY possible_org
        HAVING possible_org IS NOT NULL
        """
        df = bq.query(query).to_dataframe()
        # possible_org is email domain; try to map to org_shortname via known mapping
        # (domain mapping loaded separately and joined in main orchestrator)
        df = df.rename(columns={"possible_org": "email_domain"})
        print(f"[OK] Q-HELP: {len(df)} email domains with support data")
        return df
    except Exception as e:
        print(f"[WARN] Q-HELP failed (non-blocking): {e}")
        return pd.DataFrame(columns=["org_shortname", "support_escalations_90d",
                                     "support_conversations_90d"])


# ============================================================================
# SECTION 4 — SCORING FUNCTIONS
# ============================================================================

def threshold_lookup(value, thresholds, default=0) -> int:
    """Generic threshold lookup. Thresholds are (min_value, score) sorted descending."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return default
    for threshold, score in thresholds:
        if value >= threshold:
            return score
    return default


def threshold_lookup_ascending(value, thresholds, default=0) -> int:
    """For metrics where lower is better (e.g., days_since). Thresholds sorted ascending."""
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return default
    for threshold, score in thresholds:
        if value <= threshold:
            return score
    return default


def _safe_get(row, key, default=0):
    """Get a value from a row, returning default for NaN/None."""
    val = row.get(key, default)
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return default
    return val


def check_missing_data(row: dict, bundle: str) -> Tuple[str, List[str], List[str]]:
    """Determine scoring_status per README §3.4.

    Returns (scoring_status, blocked_dimensions, missing_data_flags).
    """
    missing_flags = []
    blocked_dims = []

    # Engagement inputs
    eng_missing = []
    if _safe_get(row, "logins_90d") == 0 and _safe_get(row, "active_users_90d") == 0:
        if row.get("logins_90d") is None or (isinstance(row.get("logins_90d"), float) and np.isnan(row.get("logins_90d", 0))):
            eng_missing.append("logins_90d")
    if _safe_get(row, "total_users") == 0:
        tu = row.get("total_users")
        if tu is None or (isinstance(tu, float) and np.isnan(tu)):
            eng_missing.append("total_users")
    if eng_missing:
        missing_flags.extend(eng_missing)
        if len(eng_missing) >= 2:
            blocked_dims.append("Engagement")

    # Adoption: check if key Mixpanel metrics are all missing
    mp_keys = ["mp_search_products", "mp_select_a_customer", "mp_item_added_via_magic_button"]
    mp_missing = [k for k in mp_keys if row.get(k) is None or
                  (isinstance(row.get(k), float) and np.isnan(row.get(k, 0)))]
    if len(mp_missing) == len(mp_keys):
        missing_flags.extend(mp_missing)
        blocked_dims.append("Adoption")

    # Value Delivery: bundle-dependent
    vd_type = BUNDLE_CONFIG[bundle]["value_delivery_type"]
    if vd_type == "presentation":
        pres_keys = ["mp_item_added_via_magic_button", "mp_item_email_drafted",
                     "mp_create_pdf_catalog", "mp_document_email_drafted"]
        pres_missing = [k for k in pres_keys if row.get(k) is None or
                        (isinstance(row.get(k), float) and np.isnan(row.get(k, 0)))]
        if len(pres_missing) == len(pres_keys):
            missing_flags.extend([f"vd_{k}" for k in pres_missing])
            blocked_dims.append("Value Delivery")
    elif vd_type in ("order", "full"):
        if row.get("orders_90d") is None or (isinstance(row.get("orders_90d"), float) and np.isnan(row.get("orders_90d", 0))):
            missing_flags.append("orders_90d")
            blocked_dims.append("Value Delivery")

    # Operational Health
    oh_missing = []
    if row.get("catalog_completeness") is None or \
       (isinstance(row.get("catalog_completeness"), float) and np.isnan(row.get("catalog_completeness", 0))):
        oh_missing.append("catalog_completeness")
    if row.get("days_since_critical_update") is None or \
       (isinstance(row.get("days_since_critical_update"), float) and np.isnan(row.get("days_since_critical_update", 0))):
        oh_missing.append("days_since_critical_update")
    if len(oh_missing) >= 2:
        missing_flags.extend(oh_missing)
        blocked_dims.append("Operational Health")

    # Trajectory
    traj_missing = []
    if row.get("logins_prior_90d") is None or \
       (isinstance(row.get("logins_prior_90d"), float) and np.isnan(row.get("logins_prior_90d", 0))):
        traj_missing.append("logins_prior_90d")
    if len(traj_missing) > 0 and len(eng_missing) > 0:
        missing_flags.extend(traj_missing)
        blocked_dims.append("Trajectory")

    if len(blocked_dims) >= 3:
        return "blocked", blocked_dims, missing_flags
    elif missing_flags:
        return "partial", blocked_dims, missing_flags
    return "complete", [], []


def score_engagement(row: dict) -> int:
    """§4.1 Engagement (25%). Returns 0-100."""
    logins = _safe_get(row, "logins_90d")
    active = _safe_get(row, "active_users_90d")
    total = _safe_get(row, "total_users")

    login_intensity = logins / active if active > 0 else 0
    active_ratio = active / total if total > 0 else 0

    li_score = threshold_lookup(login_intensity, LOGIN_INTENSITY_THRESHOLDS)
    ar_score = threshold_lookup(active_ratio, ACTIVE_USER_RATIO_THRESHOLDS)

    return round((li_score + ar_score) / 2)


def score_adoption(row: dict, bundle: str) -> int:
    """§4.2 Adoption (20%). Returns 0-100."""
    features = BUNDLE_CONFIG[bundle]["features_available"]
    used = 0
    for fnum in features:
        metric, threshold, special = FEATURE_CATALOG[fnum]
        if special == "gte1":
            if _safe_get(row, metric) >= 1:
                used += 1
        elif special == "ecat_online":
            has_catalog = bundle != "iPad-only"
            visitors = _safe_get(row, "portal_visitors_daily")
            if has_catalog and visitors > 0:
                used += 1
        else:
            if _safe_get(row, metric) > threshold:
                used += 1

    return round((used / len(features)) * 100) if features else 0


def score_value_delivery(row: dict, bundle: str) -> int:
    """§4.3 Value Delivery (30%). Returns 0-100."""
    vd_type = BUNDLE_CONFIG[bundle]["value_delivery_type"]

    pres_actions = (_safe_get(row, "mp_item_added_via_magic_button") +
                    _safe_get(row, "mp_item_email_drafted") +
                    _safe_get(row, "mp_create_pdf_catalog") +
                    _safe_get(row, "mp_document_email_drafted"))
    pres_score = threshold_lookup(pres_actions, PRESENTATION_THRESHOLDS)

    orders = _safe_get(row, "orders_90d")
    order_score = threshold_lookup(orders, ORDER_VOLUME_THRESHOLDS)

    total_cust = _safe_get(row, "total_customers")
    ordering_cust = _safe_get(row, "ordering_customers_90d")
    activation_rate = ordering_cust / total_cust if total_cust > 0 else 0
    activation_score = threshold_lookup(activation_rate, CUSTOMER_ACTIVATION_THRESHOLDS)

    online = _safe_get(row, "online_orders_90d")
    eol_share = online / orders if orders > 0 else 0
    eol_score = threshold_lookup(eol_share, EOL_SHARE_THRESHOLDS)

    portal = _safe_get(row, "mp_access_sales_portal")
    portal_score = threshold_lookup(portal, PORTAL_ENGAGEMENT_THRESHOLDS)

    if vd_type == "presentation":
        return pres_score
    elif vd_type == "order":
        return round((order_score + activation_score + eol_score) / 3)
    elif vd_type == "presentation_portal":
        return round((pres_score + portal_score) / 2)
    elif vd_type == "full":
        return round((order_score + activation_score + eol_score + portal_score) / 4)
    return 0


def score_operational_health(row: dict) -> int:
    """§4.4 Operational Health (15%). Returns 0-100."""
    total_imports = _safe_get(row, "total_imports_90d")
    success_rate = _safe_get(row, "import_success_rate")
    last_had_errors = _safe_get(row, "last_import_had_errors", False)
    cat_comp = _safe_get(row, "catalog_completeness")
    days_since = _safe_get(row, "days_since_critical_update")

    cat_score = threshold_lookup(cat_comp, CATALOG_COMPLETENESS_THRESHOLDS)
    fresh_score = threshold_lookup_ascending(days_since, DATA_FRESHNESS_THRESHOLDS,
                                            default=DATA_FRESHNESS_DEFAULT)

    if total_imports == 0 or total_imports is None:
        return round(cat_score * 0.60 + fresh_score * 0.40)

    if success_rate is None:
        import_score = 0
    elif success_rate >= 0.95 and not last_had_errors:
        import_score = 100
    elif success_rate >= 0.95:
        import_score = 80
    elif success_rate >= 0.80:
        import_score = 60
    elif success_rate >= 0.60:
        import_score = 40
    else:
        import_score = 20

    return round(import_score * 0.50 + cat_score * 0.30 + fresh_score * 0.20)


def _pct_change(current, prior):
    """Calculate % change, handling zero prior."""
    if prior == 0 and current > 0:
        return 1.0  # +100%
    if prior == 0 and current == 0:
        return 0.0
    return (current - prior) / prior


def score_trajectory(row: dict, bundle: str) -> int:
    """§4.5 Trajectory (10%). Returns 0-100."""
    logins_cur = _safe_get(row, "logins_90d")
    logins_prior = _safe_get(row, "logins_prior_90d")
    login_change = _pct_change(logins_cur, logins_prior)

    config = BUNDLE_CONFIG[bundle]
    pvm = config["primary_value_metric"]

    if pvm == "presentation_actions":
        cur_val = (_safe_get(row, "mp_item_added_via_magic_button") +
                   _safe_get(row, "mp_item_email_drafted") +
                   _safe_get(row, "mp_create_pdf_catalog") +
                   _safe_get(row, "mp_document_email_drafted"))
        prior_val = _safe_get(row, "presentation_actions_prior")
    elif pvm == "orders_90d":
        cur_val = _safe_get(row, "orders_90d")
        prior_val = _safe_get(row, "orders_prior_90d")
    elif pvm == "presentation_portal_avg":
        pres_cur = (_safe_get(row, "mp_item_added_via_magic_button") +
                    _safe_get(row, "mp_item_email_drafted") +
                    _safe_get(row, "mp_create_pdf_catalog") +
                    _safe_get(row, "mp_document_email_drafted"))
        portal_cur = _safe_get(row, "mp_access_sales_portal")
        cur_val = (pres_cur + portal_cur) / 2
        pres_prior = _safe_get(row, "presentation_actions_prior")
        portal_prior = _safe_get(row, "mp_access_sales_portal_prior")
        prior_val = (pres_prior + portal_prior) / 2
    else:
        cur_val, prior_val = 0, 0

    value_change = _pct_change(cur_val, prior_val)

    value_trend = threshold_lookup(value_change, [(t, s) for t, s in VALUE_TREND_THRESHOLDS],
                                   default=VALUE_TREND_DEFAULT)
    login_trend = threshold_lookup(login_change, [(t, s) for t, s in LOGIN_TREND_THRESHOLDS],
                                   default=LOGIN_TREND_DEFAULT)

    return round((value_trend + login_trend) / 2)


def evaluate_risk_modifiers(row: dict, dimension_scores: dict, bundle: str) -> Tuple[int, Optional[str], Optional[str]]:
    """§5 Risk Modifiers. Returns (cap, modifier_id, severity)."""
    cap = 100
    modifier_id = None
    severity = None

    arr = _safe_get(row, "arr")
    logins = _safe_get(row, "logins_90d")

    # RM-1: High ARR + zero logins
    if arr > 5000 and logins == 0:
        cap, modifier_id, severity = 20, "RM-1", "immediate"

    # RM-2: Severe value decline
    config = BUNDLE_CONFIG[bundle]
    pvm = config["primary_value_metric"]
    if pvm == "presentation_actions":
        cur_val = (_safe_get(row, "mp_item_added_via_magic_button") +
                   _safe_get(row, "mp_item_email_drafted") +
                   _safe_get(row, "mp_create_pdf_catalog") +
                   _safe_get(row, "mp_document_email_drafted"))
        prior_val = _safe_get(row, "presentation_actions_prior")
    elif pvm == "orders_90d":
        cur_val = _safe_get(row, "orders_90d")
        prior_val = _safe_get(row, "orders_prior_90d")
    elif pvm == "presentation_portal_avg":
        pres_cur = (_safe_get(row, "mp_item_added_via_magic_button") +
                    _safe_get(row, "mp_item_email_drafted") +
                    _safe_get(row, "mp_create_pdf_catalog") +
                    _safe_get(row, "mp_document_email_drafted"))
        portal_cur = _safe_get(row, "mp_access_sales_portal")
        cur_val = (pres_cur + portal_cur) / 2
        pres_prior = _safe_get(row, "presentation_actions_prior")
        portal_prior = _safe_get(row, "mp_access_sales_portal_prior")
        prior_val = (pres_prior + portal_prior) / 2
    else:
        cur_val, prior_val = 1, 1

    pv_change = _pct_change(cur_val, prior_val)
    vd_score = dimension_scores.get("value_delivery", 100)
    if pv_change < -0.60 and vd_score < 20:
        if cap > 20:
            cap, modifier_id, severity = 20, "RM-2", "immediate"

    # RM-3: Support escalations (GATED — only fires if data is reliable)
    escalations = _safe_get(row, "support_escalations_90d")
    support_reliable = row.get("_support_data_reliable", False)
    if support_reliable and escalations >= 5:
        if cap > 30:
            cap, modifier_id, severity = 30, "RM-3", "near-term"

    # RM-4: Stale data (2+ entity types > 180 days)
    stale_count = 0
    for col in ["last_products_update", "last_customers_update", "last_inventories_update"]:
        ts = row.get(col)
        if ts is not None and not (isinstance(ts, float) and np.isnan(ts)):
            try:
                days = (datetime.now() - pd.Timestamp(ts).to_pydatetime()).days
                if days > 180:
                    stale_count += 1
            except Exception:
                pass
    if stale_count >= 2:
        if cap > 30:
            cap, modifier_id, severity = 30, "RM-4", "near-term"

    return cap, modifier_id, severity


def score_bundle_upgrade_signal(row: dict, bundle: str, dimension_scores: dict) -> Optional[int]:
    """§6.1 Bundle Upgrade Signal (30%). Returns 0-100 or None for Full."""
    if bundle == "Full":
        return None

    signals = 0
    active_users = _safe_get(row, "active_users_90d")
    pres_actions = (_safe_get(row, "mp_item_added_via_magic_button") +
                    _safe_get(row, "mp_item_email_drafted") +
                    _safe_get(row, "mp_create_pdf_catalog") +
                    _safe_get(row, "mp_document_email_drafted"))
    orders_exist = _safe_get(row, "orders_exist_any_time", False)
    mp_submit = _safe_get(row, "mp_submit_order")

    if bundle == "iPad-only":
        if orders_exist and mp_submit == 0:
            signals += 1
        if mp_submit > 0:
            signals += 1
        if pres_actions > 500:
            signals += 1
        if active_users >= 10:
            signals += 1
    elif bundle == "iPad+Catalog":
        if orders_exist:
            signals += 1
        if _safe_get(row, "portal_visitors_daily") >= 30:
            signals += 1
        if active_users >= 10:
            signals += 1
    elif bundle == "iPad+Catalog+Cart":
        if active_users >= 10:
            signals += 1
        adoption = dimension_scores.get("adoption", 0)
        if adoption >= 70 and active_users >= 8:
            signals += 1
    elif bundle == "iPad+Catalog+Portal":
        if orders_exist and mp_submit == 0:
            signals += 1
        mp_customer = _safe_get(row, "mp_select_a_customer")
        if mp_customer > 100 and pres_actions > 300:
            signals += 1
        portal_accesses = _safe_get(row, "mp_access_sales_portal")
        adoption = dimension_scores.get("adoption", 0)
        if portal_accesses >= 150 and adoption >= 80:
            signals += 1

    if signals >= 3:
        return 100
    elif signals == 2:
        return 75
    elif signals == 1:
        return 50
    return 0


def score_feature_gap(row: dict, bundle: str) -> int:
    """§6.2 Feature Gap (25%). Returns 0-100."""
    signals = 0

    if bundle in ("iPad+Catalog+Cart", "Full"):
        cpq_events = _safe_get(row, "mp_order_configured_item")
        if cpq_events > 50:
            signals += 1

    pdf_count = _safe_get(row, "mp_create_pdf_catalog")
    if pdf_count > 100:
        signals += 1

    if signals >= 3:
        return 100
    elif signals == 2:
        return 75
    elif signals == 1:
        return 50
    return 0


def score_customer_headroom(row: dict, bundle: str) -> Optional[int]:
    """§6.3 Customer Headroom (25%). Returns 0-100 or None for non-ordering bundles."""
    if bundle not in ("iPad+Catalog+Cart", "Full"):
        return None

    dormant = _safe_get(row, "dormant_customers")
    total_cust = _safe_get(row, "total_customers")
    ordering_cust = _safe_get(row, "ordering_customers_90d")
    activation_rate = ordering_cust / total_cust if total_cust > 0 else 0
    geo_cv = _safe_get(row, "geographic_cv")

    dormant_score = threshold_lookup(dormant, DORMANT_THRESHOLDS)
    headroom = 1 - activation_rate
    headroom_score = threshold_lookup(headroom, ACTIVATION_HEADROOM_THRESHOLDS)
    geo_score = threshold_lookup(geo_cv, GEOGRAPHIC_CV_THRESHOLDS)

    return round((dormant_score + headroom_score + geo_score) / 3)


# ============================================================================
# SECTION 5 — PEER BENCHMARK (SECOND PASS)
# ============================================================================

def compute_bundle_medians(df: pd.DataFrame) -> Dict[str, Dict]:
    """Compute per-bundle p25/p50/p75 from raw metrics for peer benchmark gap."""
    medians = {}
    for bundle in VALID_BUNDLES:
        bdf = df[df["bundle"] == bundle].copy()
        if len(bdf) < 10:
            medians[bundle] = {"small_sample": True, "n": len(bdf)}
            continue

        def _col(c):
            return bdf[c].fillna(0) if c in bdf.columns else pd.Series(0, index=bdf.index)

        pvm = BUNDLE_CONFIG[bundle]["primary_value_metric"]
        if pvm == "presentation_actions":
            bdf["_pvm"] = (_col("mp_item_added_via_magic_button") +
                           _col("mp_item_email_drafted") +
                           _col("mp_create_pdf_catalog") +
                           _col("mp_document_email_drafted"))
        elif pvm == "orders_90d":
            bdf["_pvm"] = _col("orders_90d")
        elif pvm == "presentation_portal_avg":
            bdf["_pvm"] = ((_col("mp_item_added_via_magic_button") +
                            _col("mp_item_email_drafted") +
                            _col("mp_create_pdf_catalog") +
                            _col("mp_document_email_drafted")) +
                           _col("mp_access_sales_portal")) / 2
        else:
            bdf["_pvm"] = 0

        active = _col("active_users_90d")
        logins = _col("logins_90d")
        bdf["_login_intensity"] = np.where(active > 0, logins / active, 0)

        medians[bundle] = {
            "small_sample": False,
            "n": len(bdf),
            "login_intensity": {
                "p25": bdf["_login_intensity"].quantile(0.25),
                "p50": bdf["_login_intensity"].quantile(0.50),
                "p75": bdf["_login_intensity"].quantile(0.75),
            },
            "primary_value": {
                "p25": bdf["_pvm"].quantile(0.25),
                "p50": bdf["_pvm"].quantile(0.50),
                "p75": bdf["_pvm"].quantile(0.75),
            },
            "adoption_score": {
                "p25": bdf["_adoption_score"].quantile(0.25) if "_adoption_score" in bdf.columns else 0,
                "p50": bdf["_adoption_score"].quantile(0.50) if "_adoption_score" in bdf.columns else 50,
                "p75": bdf["_adoption_score"].quantile(0.75) if "_adoption_score" in bdf.columns else 100,
            },
        }
    return medians


def _percentile_gap_score(value, percentiles: dict) -> int:
    """§6.4: Map entity position vs peer percentiles to gap score."""
    if value < percentiles["p25"]:
        return 100
    elif value < percentiles["p50"]:
        return 75
    elif value < percentiles["p75"]:
        return 40
    return 10


def score_peer_benchmark_gap(row: dict, bundle: str, bundle_medians: dict) -> Tuple[int, bool]:
    """§6.4 Peer Benchmark Gap (20%). Returns (score, small_sample_flag)."""
    bm = bundle_medians.get(bundle, {})
    if bm.get("small_sample", True):
        return 50, True

    active = _safe_get(row, "active_users_90d")
    logins = _safe_get(row, "logins_90d")
    login_intensity = logins / active if active > 0 else 0

    pvm = BUNDLE_CONFIG[bundle]["primary_value_metric"]
    if pvm == "presentation_actions":
        pv = (_safe_get(row, "mp_item_added_via_magic_button") +
              _safe_get(row, "mp_item_email_drafted") +
              _safe_get(row, "mp_create_pdf_catalog") +
              _safe_get(row, "mp_document_email_drafted"))
    elif pvm == "orders_90d":
        pv = _safe_get(row, "orders_90d")
    elif pvm == "presentation_portal_avg":
        pv = ((_safe_get(row, "mp_item_added_via_magic_button") +
               _safe_get(row, "mp_item_email_drafted") +
               _safe_get(row, "mp_create_pdf_catalog") +
               _safe_get(row, "mp_document_email_drafted")) +
              _safe_get(row, "mp_access_sales_portal")) / 2
    else:
        pv = 0

    adoption = _safe_get(row, "_adoption_score", 50)

    li_gap = _percentile_gap_score(login_intensity, bm["login_intensity"])
    pv_gap = _percentile_gap_score(pv, bm["primary_value"])
    ad_gap = _percentile_gap_score(adoption, bm["adoption_score"])

    return round((li_gap + pv_gap + ad_gap) / 3), False


def calculate_growth_score(component_scores: dict, bundle: str) -> int:
    """§6 Growth Score with weight redistribution for non-applicable components."""
    applicable = BUNDLE_CONFIG[bundle]["growth_components"]
    active_weights = {k: GROWTH_WEIGHTS[k] for k in applicable}
    total_weight = sum(active_weights.values())
    if total_weight == 0:
        return 0

    score = 0
    for comp, base_weight in active_weights.items():
        adjusted = base_weight / total_weight
        comp_score = component_scores.get(comp, 0) or 0
        score += comp_score * adjusted

    return round(score)


# ============================================================================
# SECTION 6 — CLASSIFICATION, FLAGS, EXPLANATION
# ============================================================================

def classify(health: int, growth: int) -> str:
    """§7 Quadrant classification."""
    if health >= 60 and growth >= 60:
        return "Expand"
    elif health < 60 and growth >= 60:
        return "Stabilize First"
    elif health >= 60 and growth < 60:
        return "Maintain"
    return "Intervene"


def get_band(score: int, bands: list) -> str:
    """Map a 0-100 score to a named band."""
    for threshold, name in bands:
        if score >= threshold:
            return name
    return bands[-1][1]


def assign_flags(
    health: int, growth: int,
    risk_mod: Tuple[int, Optional[str], Optional[str]],
    growth_components: dict,
) -> dict:
    """§8 Operational flags. Returns dict with all flag columns."""
    cap, mod_id, mod_severity = risk_mod
    flags = {
        "churn_risk": False,
        "churn_risk_severity": None,
        "expansion_ready": False,
        "expansion_type": None,
        "healthy_complete": False,
    }

    # Churn risk (§8.1)
    if mod_id is not None:
        flags["churn_risk"] = True
        flags["churn_risk_severity"] = mod_severity
        return flags
    if health < 20:
        flags["churn_risk"] = True
        flags["churn_risk_severity"] = "monitored"
        return flags

    # Expansion ready (§8.2)
    if health >= 60 and growth >= 60:
        flags["expansion_ready"] = True
        best_comp = max(
            [(k, v) for k, v in growth_components.items()
             if v is not None and k != "peer_benchmark_gap"],
            key=lambda x: x[1],
            default=(None, 0),
        )
        flags["expansion_type"] = best_comp[0] if best_comp[0] else None
        return flags

    # Healthy complete (§8.3)
    if health >= 70 and growth < 40:
        flags["healthy_complete"] = True
        return flags

    return flags


def generate_explanation(
    row: dict, dim_scores: dict, growth_comps: dict,
    classification: str, scoring_status: str,
    missing_flags: List[str], bundle: str,
) -> str:
    """§9 Score explanation — deterministic template."""
    org_name = row.get("org_name", row.get("org_shortname", "Unknown"))
    health = dim_scores.get("health_score", 0)
    growth = dim_scores.get("growth_score", 0)

    if scoring_status == "blocked":
        blocked = ", ".join(dim_scores.get("blocked_dimensions", []))
        return f"Scoring blocked: insufficient data for {blocked}."

    base = f"{org_name} ({bundle}) scores {health} Health / {growth} Growth → {classification}."

    dims = {
        "Engagement": dim_scores.get("engagement", 0),
        "Adoption": dim_scores.get("adoption", 0),
        "Value Delivery": dim_scores.get("value_delivery", 0),
        "Operational Health": dim_scores.get("operational_health", 0),
        "Trajectory": dim_scores.get("trajectory", 0),
    }
    sorted_dims = sorted(dims.items(), key=lambda x: x[1])
    lowest_dim = sorted_dims[0]
    highest_dim = sorted_dims[-1]

    if classification == "Stabilize First":
        detail = (f" {lowest_dim[0]} ({lowest_dim[1]}) is the primary health deficit; "
                  f"however, growth signals indicate expansion opportunity once health recovers.")
    elif classification == "Expand":
        best_growth = max(
            [(k, v) for k, v in growth_comps.items() if v is not None],
            key=lambda x: x[1], default=("none", 0)
        )
        detail = (f" {highest_dim[0]} ({highest_dim[1]}) drives health; "
                  f"{best_growth[0].replace('_', ' ')} signals growth opportunity.")
    elif classification == "Intervene":
        detail = (f" {lowest_dim[0]} ({lowest_dim[1]}) is critically low; "
                  f"immediate attention required.")
    else:
        detail = (f" {highest_dim[0]} ({highest_dim[1]}) leads health; "
                  f"stable with standard cadence.")

    if scoring_status == "partial" and missing_flags:
        detail += f" Note: partial data — missing {', '.join(missing_flags[:3])}."

    return base + detail


# ============================================================================
# SECTION 7 — MAIN ORCHESTRATOR
# ============================================================================

def _load_bq_cache(bq_cache_dir: str, key: str) -> Optional[pd.DataFrame]:
    """Load a BigQuery result from a pre-fetched CSV cache file.

    Returns None if the cache file does not exist (caller handles fallback).
    """
    csv_path = os.path.join(bq_cache_dir, f"{key}.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(f"[OK] {key}: {len(df)} rows (from BQ cache)")
        return df
    return None


def run(args) -> None:
    """Main execution pipeline."""
    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"  Health Intelligence v2 — Operator")
    print(f"  Run date: {date.today().isoformat()}")
    print(f"{'='*60}")

    # --- Step 1-2: Connect ---
    bq_cache = getattr(args, "bq_cache_dir", None)
    if bq_cache and os.path.isdir(bq_cache):
        print(f"[INFO] --bq-cache-dir set; BigQuery data will load from: {bq_cache}")
        bq = None
    else:
        bq = connect_bigquery()
    pg_cache = getattr(args, "pg_cache_dir", None)
    if pg_cache and os.path.isdir(pg_cache):
        print(f"[INFO] --pg-cache-dir set; Postgres data will load from: {pg_cache}")
        pg = None
    else:
        pg = connect_postgres(args.skip_postgres)

    # --- Step 3: Preflight ---
    if bq is not None:
        run_preflight(bq, pg)
    else:
        print("[INFO] Skipping preflight checks (BQ cache mode — no live BQ connection)")

    # --- Step 4: Load MAL ---
    print("\n=== DATA LOADING ===")
    mal_df = load_master_account_list(args.mal, bq)

    # --- Step 5-6: Load eligibility data ---
    if bq_cache and bq is None:
        cached = _load_bq_cache(bq_cache, "bq_org_ref")
        if cached is None:
            print("[FATAL] bq_org_ref.csv not found in --bq-cache-dir. Cannot load org reference.")
            sys.exit(1)
        org_df = cached
    else:
        org_df = load_org_reference(bq)
    # HubSpot: loaded for warning flags only; not an eligibility gate
    if bq_cache and bq is None:
        cached_hs = _load_bq_cache(bq_cache, "bq_hubspot")
        hs_df = cached_hs if cached_hs is not None else pd.DataFrame(
            columns=["org_shortname", "engagement_status", "hs_type", "hs_annual_revenue"])
        if cached_hs is None:
            print("[WARN] bq_hubspot.csv not found in --bq-cache-dir; HubSpot flags will be absent")
    else:
        hs_df = load_hubspot_eligibility(bq)
    # Subscription status: primary eligibility gate (subscriptions.status = 'active')
    if pg is not None:
        sub_df = load_subscription_status(pg)
        print(f"[OK] Q-PG-SUB: {len(sub_df)} org rows; "
              f"{sub_df['has_active_sub'].sum() if 'has_active_sub' in sub_df.columns else '?'} with active sub")
    elif pg_cache and os.path.isdir(pg_cache):
        sub_cache = os.path.join(pg_cache, "pg_sub.csv")
        if os.path.exists(sub_cache):
            sub_df = pd.read_csv(sub_cache)
            print(f"[OK] Q-PG-SUB (cache): {len(sub_df)} rows from {sub_cache}")
        else:
            print(
                f"\n[FATAL] pg_sub.csv not found at: {sub_cache}\n"
                "  Subscription gate is the primary eligibility control. Running without it\n"
                "  would include ineligible orgs in the scored output, which is incorrect.\n"
                "  FIX: regenerate pg_sub.csv via Q-PG-SUB before proceeding.\n"
                "  If you intentionally want to bypass the subscription gate (e.g. testing),\n"
                "  pass --no-subscription-gate explicitly (not currently implemented).\n"
            )
            sys.exit(1)
    else:
        print(
            "\n[FATAL] Postgres unavailable and no pg_cache directory found.\n"
            "  Subscription gate requires either a live Postgres connection or pg_sub.csv cache.\n"
            "  FIX: provide --pg-cache-dir pointing to a directory containing pg_sub.csv,\n"
            "  or ensure the Postgres MCP is accessible.\n"
        )
        sys.exit(1)

    exclusion_set = None
    if args.exclusion_list:
        if os.path.exists(args.exclusion_list):
            excl_df = pd.read_csv(args.exclusion_list)
            col = excl_df.columns[0]
            exclusion_set = set(excl_df[col].str.strip().str.lower())
            print(f"[OK] Loaded {len(exclusion_set)} orgs from exclusion list")
        else:
            print(f"[WARN] Exclusion list not found: {args.exclusion_list}")

    # --- Step 7: Filter eligible entities ---
    eligible_df = filter_eligible_entities(mal_df, org_df, hs_df, sub_df, exclusion_set)
    # Annotate arr_source for observability (does not exclude)
    eligible_df = _arr_source_annotation(eligible_df)
    if len(eligible_df) == 0:
        print("[FATAL] No eligible entities found. Check MAL and subscription data.")
        sys.exit(1)

    # --- Step 8: Load all remaining data ---
    print()
    if bq_cache and bq is None:
        cached_mp = _load_bq_cache(bq_cache, "bq_mp")
        if cached_mp is None:
            print("[FATAL] bq_mp.csv not found in --bq-cache-dir. Cannot load Mixpanel metrics.")
            sys.exit(1)
        mp_df = cached_mp
    else:
        mp_df = load_mixpanel_metrics(bq)

    if pg_cache and os.path.isdir(pg_cache):
        print(f"[INFO] Loading Postgres data from cache: {pg_cache}")
        cat_df = _load_pg_cache(pg_cache, "pg_cat", pg, load_catalog_completeness)
        imp_df = _load_pg_cache(pg_cache, "pg_imp", pg, load_import_health)
        ord_df = _load_pg_cache(pg_cache, "pg_ord", pg, load_order_metrics)
        cust_df = _load_pg_cache(pg_cache, "pg_cust", pg, load_customer_metrics)
        fresh_df = _load_pg_cache(pg_cache, "pg_fresh", pg, load_data_freshness)
        user_df = _load_pg_cache(pg_cache, "pg_users", pg, load_user_counts)
        stack_df = _load_pg_cache(pg_cache, "pg_stacks", pg, load_smart_stacks)
    else:
        cat_df = load_catalog_completeness(pg)
        imp_df = load_import_health(pg)
        ord_df = load_order_metrics(pg)
        cust_df = load_customer_metrics(pg)
        fresh_df = load_data_freshness(pg)
        user_df = load_user_counts(pg)
        stack_df = load_smart_stacks(pg)
    if bq_cache and bq is None:
        cached_help = _load_bq_cache(bq_cache, "bq_help")
        help_df = cached_help if cached_help is not None else pd.DataFrame(
            columns=["email_domain", "support_escalations_90d", "support_conversations_90d"])
        if cached_help is None:
            print("[WARN] bq_help.csv not found in --bq-cache-dir; support escalation data will be absent (RM-3 won't fire)")
    else:
        help_df = load_support_data(bq)

    # Map Help Scout email domains → org_shortname using domain mapping
    if len(help_df) > 0 and "email_domain" in help_df.columns:
        domain_map_path = os.path.join(pg_cache, "pg_domain_map.csv") if pg_cache else None
        if domain_map_path and os.path.exists(domain_map_path):
            dmap = pd.read_csv(domain_map_path)
            dmap_dedup = dmap.drop_duplicates(subset=["domain"], keep="first")
            help_mapped = help_df.merge(dmap_dedup, left_on="email_domain",
                                        right_on="domain", how="inner")
            help_mapped = help_mapped.groupby("org_shortname", as_index=False).agg({
                "support_escalations_90d": "sum",
                "support_conversations_90d": "sum",
            })
            print(f"[OK] Q-HELP mapped: {len(help_mapped)} orgs via domain mapping "
                  f"(from {len(help_df)} email domains)")
            help_df = help_mapped
        else:
            print("[WARN] Q-HELP: No domain mapping available — support data unattributed")
            help_df = pd.DataFrame(columns=["org_shortname", "support_escalations_90d",
                                            "support_conversations_90d"])

    pg_loaded = pg is not None or (pg_cache is not None)
    for name, df in [("Q-PG-CAT", cat_df), ("Q-PG-IMP", imp_df), ("Q-PG-ORD", ord_df),
                     ("Q-PG-CUST", cust_df), ("Q-PG-FRESH", fresh_df),
                     ("Q-PG-USERS", user_df), ("Q-PG-STACKS", stack_df)]:
        if len(df) > 0:
            print(f"[OK] {name}: {len(df)} rows")
        elif pg_loaded:
            print(f"[WARN] {name}: 0 rows returned")

    # --- Step 9: Join everything ---
    print("\n=== JOINING DATA ===")
    master = eligible_df.copy()
    for df in [mp_df, cat_df, imp_df, ord_df, cust_df, fresh_df, user_df, stack_df, help_df]:
        if len(df) > 0 and "org_shortname" in df.columns:
            master = master.merge(df, on="org_shortname", how="left", suffixes=("", "_dup"))
            dup_cols = [c for c in master.columns if c.endswith("_dup")]
            if dup_cols:
                master = master.drop(columns=dup_cols)

    # Mark support data reliability
    if len(help_df) > 0:
        master["_support_data_reliable"] = master["org_shortname"].isin(help_df["org_shortname"])
    else:
        master["_support_data_reliable"] = False

    # Cache mode satisfies Postgres data — do not force partial even if --skip-postgres was passed
    force_partial = args.skip_postgres and not (pg_cache and os.path.isdir(pg_cache))
    print(f"[OK] Master dataset: {len(master)} entities × {len(master.columns)} columns")

    # --- Step 10: FIRST PASS — Score ---
    print("\n=== SCORING (FIRST PASS) ===")
    results = []
    for _, row in master.iterrows():
        r = row.to_dict()
        bundle = r["bundle"]

        status, blocked_dims, missing_flags = check_missing_data(r, bundle)
        if force_partial and status == "complete":
            status = "partial"
            missing_flags.append("postgres_skipped")

        if status == "blocked":
            results.append(_build_blocked_row(r, bundle, blocked_dims, missing_flags))
            continue

        eng = score_engagement(r)
        adp = score_adoption(r, bundle)
        vd = score_value_delivery(r, bundle)
        oh = score_operational_health(r)
        traj = score_trajectory(r, bundle)

        dim_scores = {
            "engagement": eng, "adoption": adp, "value_delivery": vd,
            "operational_health": oh, "trajectory": traj,
        }

        risk_cap, mod_id, mod_severity = evaluate_risk_modifiers(r, dim_scores, bundle)
        health_raw = round(
            eng * HEALTH_WEIGHTS["engagement"] +
            adp * HEALTH_WEIGHTS["adoption"] +
            vd * HEALTH_WEIGHTS["value_delivery"] +
            oh * HEALTH_WEIGHTS["operational_health"] +
            traj * HEALTH_WEIGHTS["trajectory"]
        )
        health_score = min(health_raw, risk_cap)

        bus = score_bundle_upgrade_signal(r, bundle, dim_scores)
        fg = score_feature_gap(r, bundle)
        ch = score_customer_headroom(r, bundle)

        r["_adoption_score"] = adp
        r["_health_score"] = health_score
        r["_dim_scores"] = dim_scores
        r["_risk"] = (risk_cap, mod_id, mod_severity)
        r["_growth_comps_partial"] = {
            "bundle_upgrade_signal": bus,
            "feature_gap": fg,
            "customer_headroom": ch,
        }
        r["_status"] = status
        r["_blocked_dims"] = blocked_dims
        r["_missing_flags"] = missing_flags
        results.append(r)

    # --- Step 11: SECOND PASS — Peer benchmark ---
    # If --peer-benchmark is supplied, use the Peer Benchmark Layer 2 output
    # (hv2_pbg_composite_gap) as the peer benchmark gap for each org.
    # This replaces the internal bundle-median method with cohort-based benchmarking
    # (vertical × stack peer groups) computed by the standalone Peer Benchmark system.
    # For any org not in the Layer 2 output or where the value is null, the fallback
    # is 50 (same as the existing small-sample default).
    print("\n=== SCORING (SECOND PASS — PEER BENCHMARK) ===")
    peer_benchmark_lookup: dict = {}
    if args.peer_benchmark:
        pb_path = args.peer_benchmark
        if not os.path.exists(pb_path):
            print(f"[WARN] --peer-benchmark file not found: {pb_path}")
            print("       Falling back to internal bundle-median method.")
        else:
            pb_df = pd.read_csv(pb_path)
            if "hv2_pbg_composite_gap" not in pb_df.columns:
                print(f"[WARN] --peer-benchmark file missing 'hv2_pbg_composite_gap' column.")
                print("       Falling back to internal bundle-median method.")
            else:
                pb_df = pb_df.dropna(subset=["hv2_pbg_composite_gap"])
                peer_benchmark_lookup = dict(
                    zip(pb_df["org_shortname"], pb_df["hv2_pbg_composite_gap"].astype(int))
                )
                print(f"       Loaded cohort-based peer benchmark for {len(peer_benchmark_lookup)} orgs")
                print(f"       Source: {pb_path}")

    if not peer_benchmark_lookup:
        # Internal bundle-median fallback
        scored_df = pd.DataFrame([r for r in results if r.get("_status") != "blocked"])
        if len(scored_df) > 0:
            scored_df["_adoption_score"] = scored_df.get("_adoption_score", 0)
            bundle_medians = compute_bundle_medians(scored_df)
            for bname, bm in bundle_medians.items():
                n = bm.get("n", 0)
                ss = bm.get("small_sample", False)
                print(f"       {bname}: n={n}" + (" (small sample — defaulting to 50)" if ss else ""))
        else:
            bundle_medians = {}
    else:
        bundle_medians = {}

    # --- Step 12: Final scoring ---
    print("\n=== FINAL SCORING ===")
    output_rows = []
    blocked_count = 0
    partial_count = 0

    for r in results:
        if r.get("_status") == "blocked":
            output_rows.append(r)
            blocked_count += 1
            continue

        bundle = r["bundle"]
        dim_scores = r["_dim_scores"]
        risk = r["_risk"]
        health_score = r["_health_score"]
        growth_comps = r["_growth_comps_partial"]

        if peer_benchmark_lookup and r["org_shortname"] in peer_benchmark_lookup:
            pbg_score = peer_benchmark_lookup[r["org_shortname"]]
            pbg_small = False
        else:
            pbg_score, pbg_small = score_peer_benchmark_gap(r, bundle, bundle_medians)
        growth_comps["peer_benchmark_gap"] = pbg_score

        growth_score = calculate_growth_score(growth_comps, bundle)
        classification = classify(health_score, growth_score)
        flags = assign_flags(health_score, growth_score, risk, growth_comps)

        status = r["_status"]
        missing_flags = r["_missing_flags"]
        if pbg_small:
            missing_flags.append("peer_benchmark_gap_small_sample")
            if status == "complete":
                status = "partial"

        if status == "partial":
            partial_count += 1

        all_scores = {**dim_scores, "health_score": health_score, "growth_score": growth_score}
        explanation = generate_explanation(
            r, all_scores, growth_comps, classification,
            status, missing_flags, bundle,
        )

        output_rows.append({
            "org_shortname": r["org_shortname"],
            "org_name": r.get("org_name", ""),
            "parent_entity": r.get("parent_entity"),
            "bundle": bundle,
            "arr": r.get("arr", 0),
            "arr_source": r.get("arr_source", ""),
            "health_score": health_score,
            "health_band": get_band(health_score, HEALTH_BANDS),
            "growth_score": growth_score,
            "growth_band": get_band(growth_score, GROWTH_BANDS),
            "classification": classification,
            "churn_risk": flags["churn_risk"],
            "churn_risk_severity": flags["churn_risk_severity"],
            "expansion_ready": flags["expansion_ready"],
            "expansion_type": flags["expansion_type"],
            "healthy_complete": flags["healthy_complete"],
            "engagement_score": dim_scores["engagement"],
            "adoption_score": dim_scores["adoption"],
            "value_delivery_score": dim_scores["value_delivery"],
            "operational_health_score": dim_scores["operational_health"],
            "trajectory_score": dim_scores["trajectory"],
            "bundle_upgrade_signal": growth_comps.get("bundle_upgrade_signal") or 0,
            "feature_gap_score": growth_comps.get("feature_gap", 0),
            "customer_headroom_score": growth_comps.get("customer_headroom") or 0,
            "peer_benchmark_gap": pbg_score,
            "risk_modifier_applied": risk[1],
            "scoring_status": status,
            "missing_data_flags": ", ".join(missing_flags) if missing_flags else None,
            "score_explanation": explanation,
            # Eligibility warning flags
            "hs_lifecycle_stale": r.get("hs_lifecycle_stale", False),
            "hs_join_missing": r.get("hs_join_missing", False),
            "arr_data_gap": r.get("arr_data_gap", False),
        })

    # --- Step 13: Output ---
    OUTPUT_COLUMNS = [
        "org_shortname", "org_name", "parent_entity", "bundle", "arr",
        "arr_source",
        "health_score", "health_band", "growth_score", "growth_band",
        "classification", "churn_risk", "churn_risk_severity",
        "expansion_ready", "expansion_type", "healthy_complete",
        "engagement_score", "adoption_score", "value_delivery_score",
        "operational_health_score", "trajectory_score",
        "bundle_upgrade_signal", "feature_gap_score",
        "customer_headroom_score", "peer_benchmark_gap",
        "risk_modifier_applied", "scoring_status",
        "missing_data_flags", "score_explanation",
        # Eligibility warning flags (informational; do not affect scoring)
        "hs_lifecycle_stale", "hs_join_missing", "arr_data_gap",
    ]
    output_df = pd.DataFrame(output_rows)
    output_df = output_df[[c for c in OUTPUT_COLUMNS if c in output_df.columns]]
    output_file = os.path.join(
        args.output_dir, f"client_health_scores_{date.today().isoformat()}.csv"
    )
    os.makedirs(args.output_dir, exist_ok=True)
    output_df.to_csv(output_file, index=False)

    elapsed = (datetime.now() - start_time).total_seconds()

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"  SCORING COMPLETE")
    print(f"{'='*60}")
    print(f"  Output: {output_file}")
    print(f"  Entities scored: {len(output_rows)}")
    print(f"  Blocked: {blocked_count}")
    print(f"  Partial: {partial_count}")
    print(f"  Complete: {len(output_rows) - blocked_count - partial_count}")
    if pg_cache and os.path.isdir(pg_cache):
        print(f"  ✓ Postgres data loaded from cache: {pg_cache}")
    elif args.skip_postgres:
        print(f"  ⚠ RUN WAS PARTIAL (--skip-postgres — no Postgres data)")
    print()

    if "classification" in output_df.columns:
        scored = output_df[output_df["classification"] != "BLOCKED"]
        if len(scored) > 0:
            print("  Classification breakdown:")
            for cls, cnt in scored["classification"].value_counts().items():
                print(f"    {cls}: {cnt}")
            print()
            print("  Health band breakdown:")
            for band, cnt in scored["health_band"].value_counts().items():
                print(f"    {band}: {cnt}")
            print()
            print("  Growth band breakdown:")
            for band, cnt in scored["growth_band"].value_counts().items():
                print(f"    {band}: {cnt}")

    print(f"\n  Elapsed: {elapsed:.1f}s")
    print(f"{'='*60}\n")


def _build_blocked_row(r: dict, bundle: str, blocked_dims: list, missing_flags: list) -> dict:
    """Build output row for a blocked entity per README §3.4."""
    return {
        "org_shortname": r["org_shortname"],
        "org_name": r.get("org_name", ""),
        "parent_entity": r.get("parent_entity"),
        "bundle": bundle,
        "arr": r.get("arr", 0),
        "health_score": None,
        "health_band": None,
        "growth_score": None,
        "growth_band": None,
        "classification": "BLOCKED",
        "churn_risk": False,
        "churn_risk_severity": None,
        "expansion_ready": False,
        "expansion_type": None,
        "healthy_complete": False,
        "engagement_score": None,
        "adoption_score": None,
        "value_delivery_score": None,
        "operational_health_score": None,
        "trajectory_score": None,
        "bundle_upgrade_signal": None,
        "feature_gap_score": None,
        "customer_headroom_score": None,
        "peer_benchmark_gap": None,
        "risk_modifier_applied": None,
        "scoring_status": "blocked",
        "missing_data_flags": ", ".join(missing_flags) if missing_flags else None,
        "score_explanation": f"Scoring blocked: insufficient data for {', '.join(blocked_dims)}.",
        "_status": "blocked",  # internal flag, stripped before CSV output
        # Eligibility warning flags
        "arr_source": r.get("arr_source", ""),
        "hs_lifecycle_stale": r.get("hs_lifecycle_stale", False),
        "hs_join_missing": r.get("hs_join_missing", False),
        "arr_data_gap": r.get("arr_data_gap", False),
    }


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Health Intelligence v2 — Score all eligible entities and output CSV.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables for Postgres (checked in order):
  DATABASE_URL          Full connection URL (preferred)
  PGHOST, PGPORT,       Standard libpq env vars
  PGDATABASE, PGUSER,
  PGPASSWORD

Environment variables for BigQuery:
  GOOGLE_APPLICATION_CREDENTIALS   Path to service account JSON

Examples:
  python health_operator.py --mal ~/data/master_account_list.csv
  python health_operator.py --mal ~/data/mal.csv --skip-postgres --output-dir ./output
  python health_operator.py --mal ~/data/mal.csv --exclusion-list ./exclusions.csv
        """,
    )
    parser.add_argument(
        "--mal", required=True,
        help="Path to Master Account List CSV (required columns: org_shortname or company, bundle or stack, parent_entity)",
    )
    parser.add_argument(
        "--output-dir", default=".",
        help="Directory for output CSV (default: current directory)",
    )
    parser.add_argument(
        "--skip-postgres", action="store_true",
        help="Run without Postgres connection (partial scoring only)",
    )
    parser.add_argument(
        "--exclusion-list", default=None,
        help="Path to CSV with org_shortname values to exclude (single column)",
    )
    parser.add_argument(
        "--pg-cache-dir", default=None,
        help="Directory with pre-fetched Postgres CSV files (pg_cat.csv, pg_imp.csv, etc.)",
    )
    parser.add_argument(
        "--bq-cache-dir", default=None,
        help=(
            "Directory with pre-fetched BigQuery CSV files "
            "(bq_org_ref.csv, bq_hubspot.csv, bq_mp.csv, bq_help.csv). "
            "When set, skips live BigQuery connection."
        ),
    )
    parser.add_argument(
        "--peer-benchmark", default=None,
        help=(
            "Path to Peer Benchmark Layer 2 output CSV (peer_benchmark_*.csv). "
            "When provided, hv2_pbg_composite_gap replaces the internal bundle-median "
            "peer benchmark gap calculation. Falls back to the internal method (score=50) "
            "for any org not found in the file or where the value is null."
        ),
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Print additional debug output",
    )

    args = parser.parse_args()
    run(args)
