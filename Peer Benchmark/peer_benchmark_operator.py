"""
Peer Benchmark v1 — Cohort Assignment Operator
================================================
Layer 1: assigns every eligible org to a peer cohort.
Answers: "Who should this org be compared against?"

Usage:
  python peer_benchmark_operator.py \\
    --health-output "/path/to/client_health_scores_YYYY-MM-DD.csv" \\
    --pg-cache-dir "/path/to/Health V2/cache" \\
    --output-dir "./runs/YYYY-MM-DD_v1.0.0"

Environment:
  GOOGLE_APPLICATION_CREDENTIALS   Path to BigQuery service account JSON

Dependencies:
  pip install google-cloud-bigquery pandas numpy db-dtypes
"""

import argparse
import os
import sys
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

try:
    from google.cloud import bigquery
except ImportError:
    print("[FATAL] google-cloud-bigquery not installed. Run: pip install google-cloud-bigquery")
    sys.exit(1)

# ── Version ──────────────────────────────────────────────────────────────────

VERSION = "1.0.1"
README_VERSION = "1.0.0"

# ── Cohort confidence thresholds ─────────────────────────────────────────────

COHORT_HIGH_N = 8
COHORT_MEDIUM_N = 5

# ── ARR band thresholds (annual) ──────────────────────────────────────────────

def arr_band(arr):
    if pd.isna(arr) or arr == 0:
        return "unknown"
    if arr < 5000:
        return "<5K"
    if arr < 15000:
        return "5-15K"
    if arr < 30000:
        return "15-30K"
    return "30K+"


def catalog_scale_band(n):
    if pd.isna(n):
        return "unknown"
    n = int(n)
    if n < 500:
        return "<500"
    if n < 5000:
        return "500-5K"
    if n < 25000:
        return "5K-25K"
    return "25K+"


def customer_scale_band(n):
    if pd.isna(n):
        return "unknown"
    n = int(n)
    if n < 100:
        return "<100"
    if n < 500:
        return "100-500"
    if n < 2000:
        return "500-2K"
    return "2K+"


def tenure_band(created_at_str):
    if not created_at_str or pd.isna(created_at_str):
        return "unknown"
    try:
        if hasattr(created_at_str, "date"):
            created = created_at_str.date()
        else:
            created = datetime.strptime(str(created_at_str)[:10], "%Y-%m-%d").date()
        days = (date.today() - created).days
        years = days / 365.25
        if years < 1:
            return "<1yr"
        if years < 2:
            return "1-2yr"
        if years < 4:
            return "2-4yr"
        return "4yr+"
    except Exception:
        return "unknown"


# ── BigQuery connection ───────────────────────────────────────────────────────

def connect_bigquery() -> bigquery.Client:
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds or not os.path.exists(creds):
        print("[FATAL] GOOGLE_APPLICATION_CREDENTIALS not set or file not found.")
        print("        Set it to the path of your BigQuery service account JSON.")
        sys.exit(1)
    try:
        client = bigquery.Client()
        print("[OK] BigQuery connected")
        return client
    except Exception as e:
        print(f"[FATAL] BigQuery connection failed: {e}")
        sys.exit(1)


# ── Data loaders ─────────────────────────────────────────────────────────────

def load_health_output(path: str) -> pd.DataFrame:
    """Q-HV2: Load Health V2 scored output CSV."""
    if not os.path.exists(path):
        print(f"[FATAL] Health V2 output not found: {path}")
        sys.exit(1)
    df = pd.read_csv(path)
    required = {"org_shortname", "org_name", "bundle", "arr"}
    missing = required - set(df.columns)
    if missing:
        print(f"[FATAL] Health V2 output missing required columns: {missing}")
        sys.exit(1)
    print(f"[OK] Q-HV2: {len(df)} entities from Health V2 output")
    return df


def load_vertical_signals(bq: bigquery.Client) -> pd.DataFrame:
    """Q-VERT: Pull vertical, lifecycle, tenure, and provisioning signals from BigQuery.

    Tenure source: hc.properties_createdate (HubSpot company create date — best proxy
    for go-live date available without a live Postgres connection).
    Provisioning signals: not available in org_summary; stack mismatch check skipped.
    Vertical: hc.properties_segment (authoritative per QUERIES.md DQ-1).
    """
    query = """
    SELECT
      os.org_shortname,
      hc.properties_segment                AS vertical_raw,
      hc.properties_lifecyclestage         AS hs_lifecyclestage,
      hc.properties_createdate             AS org_created_at,
      os.feature_depth,
      os.billing_status,
      os.is_active
    FROM `supercat-data-pipeline.insightful_product.org_summary` os
    LEFT JOIN `supercat-data-pipeline.hubspot.company` hc
      ON os.hubspot_company_id = hc.company_id
    WHERE os.org_shortname IS NOT NULL
    """
    try:
        df = bq.query(query).to_dataframe()
        print(f"[OK] Q-VERT: {len(df)} rows from org_summary + HubSpot")
        return df
    except Exception as e:
        print(f"[FATAL] Q-VERT failed: {e}")
        sys.exit(1)


def load_pg_cache(cache_dir: str, filename: str, required_cols: list) -> pd.DataFrame:
    """Load a Postgres cache CSV. Returns empty DataFrame if missing."""
    path = os.path.join(cache_dir, filename)
    if not os.path.exists(path):
        print(f"[WARN] Cache file missing: {path} — affected fields will be 'unknown'")
        return pd.DataFrame(columns=["org_shortname"] + required_cols)
    df = pd.read_csv(path)
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"[WARN] {filename} missing columns {missing} — affected fields will be 'unknown'")
    print(f"[OK] {filename}: {len(df)} rows (from cache)")
    return df


# ── Lifecycle assignment ──────────────────────────────────────────────────────

def assign_lifecycle(row) -> str:
    """
    Assign lifecycle stage from created_at + HubSpot lifecyclestage.
    onboarding: created < 90 days ago OR lifecyclestage = 'evangelist'
    ramping:    tenure < 1 year (and not onboarding)
    steady_state: tenure >= 1 year (or created_at unknown — conservative default)
    """
    hs_stage = str(row.get("hs_lifecyclestage", "") or "").strip().lower()
    created_at = row.get("org_created_at")

    if hs_stage == "evangelist":
        return "onboarding"

    if not created_at or pd.isna(created_at):
        return "steady_state"

    try:
        if hasattr(created_at, "date"):
            created = created_at.date()
        else:
            created = datetime.strptime(str(created_at)[:10], "%Y-%m-%d").date()
        days = (date.today() - created).days
        if days < 90:
            return "onboarding"
        if days < 365:
            return "ramping"
        return "steady_state"
    except Exception:
        return "steady_state"


# ── Stack mismatch detection ──────────────────────────────────────────────────

def check_stack_mismatch(bundle: str, has_catalog, has_cart, has_portal):
    """
    Compare MAL bundle against org_summary provisioning signals.
    Returns (mismatch_flag, confidence).
    None values = signals unavailable.
    """
    if pd.isna(has_catalog) and pd.isna(has_cart) and pd.isna(has_portal):
        return None, "medium"

    mismatch = False

    if not pd.isna(has_portal) and has_portal and bundle in ("iPad-only", "iPad+Catalog"):
        mismatch = True
    if not pd.isna(has_cart) and not has_cart and bundle in ("iPad+Catalog+Cart", "Full"):
        mismatch = True
    if not pd.isna(has_catalog) and not has_catalog and bundle != "iPad-only":
        mismatch = True

    confidence = "medium" if mismatch else "high"
    return mismatch, confidence


# ── Cohort assignment ─────────────────────────────────────────────────────────

def _resolve_cohort(
    tier1_id: str,
    vertical: str,
    bundle: str,
    lifecycle: str,
    t1_n: int,
    t2_n: int,
    t3_n: int,
) -> dict:
    """Resolve effective cohort level, id, peer count, eligibility, and confidence.

    Single canonical implementation of the README §3 fallback hierarchy and lifecycle
    eligibility rules. Called by assign_cohorts() and re-called post-self-removal in
    build_peer_org_lists().

    Parameters
    ----------
    tier1_id  : canonical Tier 1 peer_group_id ("vertical / bundle")
    vertical  : resolved vertical string (empty string if unresolved)
    bundle    : bundle string
    lifecycle : "steady_state" | "ramping" | "onboarding"
    t1_n      : steady_state peer count for the Tier 1 group, EXCLUDING self
    t2_n      : steady_state peer count for the vertical (Tier 2), EXCLUDING self
    t3_n      : steady_state peer count for the bundle (Tier 3), EXCLUDING self

    All three counts must exclude the org being resolved. Callers are responsible
    for subtracting self before calling.

    Returns
    -------
    dict with keys: effective_id, level, cohort_n, benchmark_eligible,
                    benchmark_confidence
    """
    # ── Fallback hierarchy (README §3) ──────────────────────────────────────
    # t*_n already exclude self, so cohort_n == t*_n directly.
    if not vertical:
        # No vertical resolved — skip Tier 1 and Tier 2, go straight to Tier 3
        if t3_n >= COHORT_MEDIUM_N:
            effective_id = bundle
            level = "tier3"
            cohort_n = t3_n
            confidence = "low"
        else:
            effective_id = tier1_id
            level = "tier4"
            cohort_n = 0
            confidence = "none"
    elif t1_n >= COHORT_MEDIUM_N:
        effective_id = tier1_id
        level = "tier1"
        cohort_n = t1_n
        confidence = "high" if t1_n >= COHORT_HIGH_N else "medium"
    elif t2_n >= COHORT_MEDIUM_N:
        effective_id = vertical
        level = "tier2"
        cohort_n = t2_n
        confidence = "low"
    elif t3_n >= COHORT_MEDIUM_N:
        effective_id = bundle
        level = "tier3"
        cohort_n = t3_n
        confidence = "low"
    else:
        effective_id = tier1_id
        level = "tier4"
        cohort_n = 0
        confidence = "none"

    # ── Lifecycle eligibility (README §2 Axis 5) ────────────────────────────
    if lifecycle == "onboarding":
        benchmark_eligible = False
        confidence = "none"
    elif lifecycle == "ramping":
        # Ramping orgs are only eligible if the final effective cohort is viable.
        benchmark_eligible = cohort_n >= COHORT_MEDIUM_N
        confidence = "low" if benchmark_eligible else "none"
    else:
        # steady_state: eligible unless no viable cohort exists
        benchmark_eligible = level != "tier4"

    return {
        "effective_id": effective_id,
        "level": level,
        "cohort_n": max(cohort_n, 0),
        "benchmark_eligible": benchmark_eligible,
        "benchmark_confidence": confidence,
    }


def assign_cohorts(df: pd.DataFrame) -> tuple:
    """Apply the five-axis cohort assignment logic per README §3.

    df must have: org_shortname, bundle, vertical, vertical_source, lifecycle_stage

    Returns (df_with_cohorts, tier_counts) where tier_counts is a dict containing
    the pre-self-removal steady_state counts needed for post-self-removal correction:
      {"tier1": {...}, "tier2": {...}, "tier3": {...}}
    """
    # Build Tier 1 peer_group_id
    df["peer_group_id"] = df.apply(
        lambda r: f"{r['vertical']} / {r['bundle']}"
        if pd.notna(r["vertical"]) and r["vertical"]
        else f"UNRESOLVED / {r['bundle']}",
        axis=1,
    )

    # Count steady_state entities per tier (pre-self-removal)
    steady = df[df["lifecycle_stage"] == "steady_state"]
    tier1_counts = steady.groupby("peer_group_id")["org_shortname"].count().to_dict()
    tier2_counts = steady.groupby("vertical")["org_shortname"].count().to_dict()
    tier3_counts = steady.groupby("bundle")["org_shortname"].count().to_dict()

    rows = []
    for _, row in df.iterrows():
        r = row.to_dict()
        tier1_id = r["peer_group_id"]
        vertical = r.get("vertical") or ""
        bundle = r["bundle"]
        lifecycle = r["lifecycle_stage"]
        is_steady = lifecycle == "steady_state"

        # _resolve_cohort expects counts excluding self; subtract 1 for steady_state
        # orgs (ramping/onboarding orgs are not in the steady_state counts at all).
        t1_pre = tier1_counts.get(tier1_id, 0)
        t2_pre = tier2_counts.get(vertical, 0)
        t3_pre = tier3_counts.get(bundle, 0)
        resolved = _resolve_cohort(
            tier1_id=tier1_id,
            vertical=vertical,
            bundle=bundle,
            lifecycle=lifecycle,
            t1_n=t1_pre - (1 if is_steady else 0),
            t2_n=t2_pre - (1 if is_steady and vertical else 0),
            t3_n=t3_pre - (1 if is_steady else 0),
        )

        r["peer_group_id_effective"] = resolved["effective_id"]
        r["peer_group_level"] = resolved["level"]
        r["peer_group_n"] = resolved["cohort_n"]
        r["benchmark_eligible"] = resolved["benchmark_eligible"]
        r["benchmark_confidence"] = resolved["benchmark_confidence"]
        rows.append(r)

    tier_counts = {
        "tier1": tier1_counts,
        "tier2": tier2_counts,
        "tier3": tier3_counts,
    }
    return pd.DataFrame(rows), tier_counts


def build_peer_org_lists(df: pd.DataFrame, tier_counts: dict) -> pd.DataFrame:
    """Build pipe-separated peer org lists for each entity, excluding self.

    After building peer_orgs (and thereby establishing the true post-self-removal
    peer count), any Tier 1 row whose peer_group_n has dropped below COHORT_MEDIUM_N
    is re-resolved through the full documented fallback hierarchy using _resolve_cohort
    with the actual post-self-removal t1_n. This ensures peer_group_level,
    peer_group_id_effective, benchmark_eligible, and benchmark_confidence all use the
    same counting basis as the displayed peer_group_n.

    Three separate maps are built from the full steady-state population:
    - tier1_map: keyed by peer_group_id (Vertical / Bundle)
    - tier2_map: keyed by vertical
    - tier3_map: keyed by bundle

    For a fallback row (tier2/tier3), peers are drawn from the full vertical or
    bundle map — not from the small subset of other fallback orgs. This ensures
    peer_orgs is consistent with peer_group_n.

    Semantics:
    - peer_orgs: steady_state members of the effective cohort, EXCLUDING self.
    - peer_group_n: count of peer_orgs entries (i.e., excludes self).
      Invariant: for all benchmark_eligible rows, peer_group_n == len(peer_orgs.split('|')).
    - Non-eligible rows (onboarding, tier4, ramping with no viable cohort): peer_orgs = "".
    """
    steady = df[df["lifecycle_stage"] == "steady_state"]

    # Build all three maps from the full steady-state population
    tier1_map: dict[str, list] = {}
    tier2_map: dict[str, list] = {}
    tier3_map: dict[str, list] = {}

    for _, row in steady.iterrows():
        org = row["org_shortname"]
        tier1_map.setdefault(row["peer_group_id"], []).append(org)
        if pd.notna(row.get("vertical")) and row["vertical"]:
            tier2_map.setdefault(row["vertical"], []).append(org)
        tier3_map.setdefault(row["bundle"], []).append(org)

    def get_peers(row):
        if not row["benchmark_eligible"]:
            return ""
        level = row["peer_group_level"]
        org = row["org_shortname"]
        if level == "tier1":
            members = tier1_map.get(row["peer_group_id"], [])
        elif level == "tier2":
            members = tier2_map.get(row.get("vertical", ""), [])
        elif level == "tier3":
            members = tier3_map.get(row["bundle"], [])
        else:
            return ""
        return "|".join(sorted(m for m in members if m != org))

    df["peer_orgs"] = df.apply(get_peers, axis=1)

    # Recompute peer_group_n to be consistent with peer_orgs
    def recount_n(row):
        if not row["benchmark_eligible"] or row["peer_orgs"] == "":
            return 0
        return len(row["peer_orgs"].split("|"))

    df["peer_group_n"] = df.apply(recount_n, axis=1)

    # ── Post-self-removal correction for Tier 1 rows ────────────────────────
    # For any Tier 1 row whose post-self-removal peer_group_n is now below
    # COHORT_MEDIUM_N, re-run the full fallback hierarchy via _resolve_cohort
    # with post-self-removal counts for ALL three tiers (t1, t2, t3) so that
    # Tier 2 / Tier 3 viability is evaluated on the same excluding-self basis.
    # peer_orgs is then rebuilt for any demoted rows.
    needs_rebuild = False
    rows = df.to_dict("records")
    for r in rows:
        if r["peer_group_level"] != "tier1":
            continue
        actual_n = r["peer_group_n"]  # post-self-removal count
        if actual_n >= COHORT_MEDIUM_N:
            # Still viable — only confidence band may need updating (high vs medium)
            r["benchmark_confidence"] = (
                "high" if actual_n >= COHORT_HIGH_N else "medium"
            )
            continue
        # Tier 1 peer count fell below threshold after self-removal. Re-resolve
        # through the full hierarchy to get the correct level, eligibility, and
        # confidence. _resolve_cohort expects excluding-self counts for all tiers;
        # deduct self from the pre-self-removal tier2/tier3 counts here.
        # Ramping/onboarding orgs are not included in steady_state counts, so no
        # deduction is needed for them.
        vertical = r.get("vertical") or ""
        bundle = r["bundle"]
        is_steady = r["lifecycle_stage"] == "steady_state"
        t2_pre = tier_counts["tier2"].get(vertical, 0)
        t3_pre = tier_counts["tier3"].get(bundle, 0)
        t2_actual = t2_pre - (1 if is_steady and vertical else 0)
        t3_actual = t3_pre - (1 if is_steady else 0)
        resolved = _resolve_cohort(
            tier1_id=r["peer_group_id"],
            vertical=vertical,
            bundle=bundle,
            lifecycle=r["lifecycle_stage"],
            t1_n=actual_n,
            t2_n=t2_actual,
            t3_n=t3_actual,
        )
        r["peer_group_id_effective"] = resolved["effective_id"]
        r["peer_group_level"] = resolved["level"]
        r["peer_group_n"] = resolved["cohort_n"]
        r["benchmark_eligible"] = resolved["benchmark_eligible"]
        r["benchmark_confidence"] = resolved["benchmark_confidence"]
        r["peer_orgs"] = ""  # will be rebuilt below
        needs_rebuild = True

    df = pd.DataFrame(rows)

    if needs_rebuild:
        # Rebuild peer_orgs and peer_group_n for any demoted rows. Undisturbed rows
        # already have correct peer_orgs; the second pass is cheap because get_peers
        # is a pure lookup and recount_n is a string split.
        df["peer_orgs"] = df.apply(get_peers, axis=1)
        df["peer_group_n"] = df.apply(recount_n, axis=1)

    return df


# ── Rollup flag ───────────────────────────────────────────────────────────────

def assign_rollup_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag entities that participate in a real parent/child rollup structure.

    parent_entity in the Health V2 output is a company-name reference field, not a
    reliable rollup indicator on its own. Many entities self-reference (parent_entity
    equals their own org_name, lowercased). We only flag genuine rollup participation:

    - A CHILD: its parent_entity resolves (by org_name case-insensitive match) to a
      *different* org_shortname in the same universe.
    - A PARENT: another entity's parent_entity resolves to this entity's org_shortname.

    Entities whose parent_entity does not resolve to any org in the universe (including
    self-references) are NOT flagged.
    """
    # Build name → org_shortname lookup for the scoring universe
    name_to_short = {}
    for _, row in df.iterrows():
        name = str(row.get("org_name") or "").strip().lower()
        if name:
            name_to_short[name] = row["org_shortname"]

    def resolved_parent(row):
        parent_raw = str(row.get("parent_entity") or "").strip().lower()
        if not parent_raw:
            return None
        resolved = name_to_short.get(parent_raw)
        # Only a real parent if it resolves to a *different* org in this universe
        if resolved and resolved != row["org_shortname"]:
            return resolved
        return None

    df["_resolved_parent"] = df.apply(resolved_parent, axis=1)

    # Entities that are children (have a real parent in the universe)
    df["_is_child"] = df["_resolved_parent"].notna()

    # Entities that are referenced as a parent by at least one child
    real_parents = set(df["_resolved_parent"].dropna())
    df["_is_parent"] = df["org_shortname"].isin(real_parents)

    df["rollup_flag"] = df["_is_child"] | df["_is_parent"]
    df.drop(columns=["_resolved_parent", "_is_child", "_is_parent"], inplace=True)
    return df


# ── Run summary ───────────────────────────────────────────────────────────────

def print_summary(df: pd.DataFrame, unresolved_vertical: int, null_tenure: int):
    print(f"\n{'='*60}")
    print(f"  COHORT ASSIGNMENT COMPLETE")
    print(f"{'='*60}")
    print(f"  Entities processed: {len(df)}")
    print(f"  Unresolved vertical: {unresolved_vertical} "
          f"({'%.0f' % (unresolved_vertical/len(df)*100)}%)")
    print(f"  NULL tenure (defaulted to steady_state): {null_tenure}")
    print()

    lc = df["lifecycle_stage"].value_counts()
    print("  Lifecycle breakdown:")
    for stage, cnt in lc.items():
        print(f"    {stage}: {cnt}")

    print()
    eligible = df[df["benchmark_eligible"]]
    print(f"  Benchmark eligible: {len(eligible)} / {len(df)}")

    conf = eligible["benchmark_confidence"].value_counts()
    print("  Confidence breakdown (eligible only):")
    for c, cnt in conf.items():
        print(f"    {c}: {cnt}")

    print()
    level_counts = df["peer_group_level"].value_counts()
    print("  Cohort level breakdown (all entities):")
    for lvl, cnt in level_counts.items():
        print(f"    {lvl}: {cnt}")

    print()
    print("  Cohort sizes (Tier 1, steady_state orgs):")
    tier1 = df[(df["peer_group_level"] == "tier1") & (df["lifecycle_stage"] == "steady_state")]
    for gid, grp in tier1.groupby("peer_group_id_effective"):
        print(f"    {gid}: n={len(grp)}")

    mismatch = df["stack_mismatch_flag"].sum()
    print(f"\n  Stack mismatch flags: {int(mismatch) if pd.notna(mismatch) else 0}")
    print(f"  Rollup participants: {df['rollup_flag'].sum()}")
    print(f"{'='*60}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def run(args):
    run_date = date.today()
    benchmark_month = run_date.strftime("%Y-%m")

    print(f"\n{'='*60}")
    print(f"  Peer Benchmark v{VERSION} — Cohort Assignment")
    print(f"  Run date: {run_date}")
    print(f"{'='*60}")

    bq_cache_dir = getattr(args, "bq_cache_dir", None)
    if bq_cache_dir and os.path.isdir(bq_cache_dir):
        print(f"[INFO] --bq-cache-dir set; BigQuery data will load from: {bq_cache_dir}")
        bq = None
    else:
        bq = connect_bigquery()

    # Step 1 — Load Health V2 output
    print("\n=== DATA LOADING ===")
    hv2 = load_health_output(args.health_output)

    # Step 2 — Load vertical + lifecycle signals
    if bq_cache_dir and bq is None:
        vert_cache_path = os.path.join(bq_cache_dir, "bq_vert.csv")
        if not os.path.exists(vert_cache_path):
            print(f"[FATAL] bq_vert.csv not found in --bq-cache-dir: {bq_cache_dir}")
            sys.exit(1)
        vert_df = pd.read_csv(vert_cache_path)
        print(f"[OK] Q-VERT: {len(vert_df)} rows (from BQ cache)")
    else:
        vert_df = load_vertical_signals(bq)

    # Step 3 — Load Postgres cache
    cache_dir = args.pg_cache_dir
    cat_df = load_pg_cache(cache_dir, "pg_cat.csv", ["total_active_products"])
    cust_df = load_pg_cache(cache_dir, "pg_cust.csv", ["total_customers"])

    # Step 4 — Merge all inputs onto HV2 universe
    print("\n=== BUILDING COHORT INPUT ===")
    df = hv2[["org_shortname", "org_name", "bundle", "arr",
               "parent_entity"]].copy()

    # Ensure parent_entity column exists
    if "parent_entity" not in df.columns:
        df["parent_entity"] = None

    # Merge vertical signals
    vert_dedup = vert_df.drop_duplicates(subset=["org_shortname"], keep="first")
    df = df.merge(vert_dedup, on="org_shortname", how="left")

    # Resolve vertical
    df["vertical"] = df["vertical_raw"].where(
        df["vertical_raw"].notna() & (df["vertical_raw"].str.strip() != ""), other=None
    )
    df["vertical_source"] = df["vertical"].apply(
        lambda v: "hubspot_live" if v else "unresolved"
    )

    unresolved_vertical = (df["vertical_source"] == "unresolved").sum()
    null_tenure = df["org_created_at"].isna().sum()

    print(f"[OK] Vertical resolved: {len(df) - unresolved_vertical} / {len(df)}")
    if unresolved_vertical > 0:
        unresolved_orgs = df[df["vertical_source"] == "unresolved"]["org_shortname"].tolist()
        print(f"[WARN] {unresolved_vertical} orgs with unresolved vertical: {unresolved_orgs}")
    if null_tenure > 0:
        print(f"[WARN] {null_tenure} orgs with NULL created_at — defaulted to steady_state")

    # Assign lifecycle stage
    df["lifecycle_stage"] = df.apply(assign_lifecycle, axis=1)

    # Assign stack mismatch
    # has_catalog/has_cart/has_portal are not available in org_summary;
    # all orgs default to confidence=medium, flag=None unless Postgres cache provides them.
    def mismatch_row(row):
        flag, conf = check_stack_mismatch(
            row["bundle"],
            row.get("has_catalog", np.nan),
            row.get("has_cart", np.nan),
            row.get("has_portal", np.nan),
        )
        return pd.Series({"stack_mismatch_flag": flag,
                          "stack_assignment_confidence": conf})

    mismatch_cols = df.apply(mismatch_row, axis=1)
    df["stack_mismatch_flag"] = mismatch_cols["stack_mismatch_flag"]
    df["stack_assignment_confidence"] = mismatch_cols["stack_assignment_confidence"]

    mismatches = df["stack_mismatch_flag"].sum()
    if mismatches and mismatches > 0:
        print(f"[WARN] Stack mismatch detected for {int(mismatches)} orgs")

    # Merge catalog and customer scale
    if "total_active_products" in cat_df.columns:
        df = df.merge(cat_df[["org_shortname", "total_active_products"]],
                      on="org_shortname", how="left")
    else:
        df["total_active_products"] = None

    if "total_customers" in cust_df.columns:
        df = df.merge(cust_df[["org_shortname", "total_customers"]],
                      on="org_shortname", how="left")
    else:
        df["total_customers"] = None

    # Compute commercial profile bands
    df["arr_band"] = df["arr"].apply(arr_band)
    df["catalog_scale"] = df["total_active_products"].apply(catalog_scale_band)
    df["customer_scale"] = df["total_customers"].apply(customer_scale_band)
    df["tenure_band"] = df["org_created_at"].apply(tenure_band)

    # Step 5 — Assign rollup flags
    df = assign_rollup_flag(df)

    # Step 6 — Assign cohorts
    print("\n=== COHORT ASSIGNMENT ===")
    df, tier_counts = assign_cohorts(df)
    df = build_peer_org_lists(df, tier_counts)

    # Step 7 — Build final output
    df["run_date"] = run_date.isoformat()
    df["benchmark_month"] = benchmark_month

    output_cols = [
        "org_shortname", "org_name", "vertical", "vertical_source",
        "bundle", "stack_assignment_confidence", "stack_mismatch_flag",
        "peer_group_id", "peer_group_id_effective", "peer_group_level",
        "peer_group_n", "benchmark_eligible", "benchmark_confidence",
        "lifecycle_stage", "peer_orgs",
        "arr_band", "catalog_scale", "customer_scale", "tenure_band",
        "rollup_flag", "run_date", "benchmark_month",
    ]

    # Only include columns that exist
    output_cols = [c for c in output_cols if c in df.columns]
    output_df = df[output_cols].copy()
    # Ensure peer_orgs is always a string (no NaN)
    output_df["peer_orgs"] = output_df["peer_orgs"].fillna("")

    # Step 8 — Write output
    os.makedirs(args.output_dir, exist_ok=True)
    output_file = os.path.join(
        args.output_dir, f"peer_cohort_assignments_{run_date.isoformat()}.csv"
    )
    output_df.to_csv(output_file, index=False)

    print_summary(df, unresolved_vertical, null_tenure)
    print(f"  Output: {output_file}")
    print(f"  Entities: {len(output_df)}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Peer Benchmark v1 — Cohort Assignment Operator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python peer_benchmark_operator.py \\
    --health-output "../Health V2/runs/2026-04-03_v2.0.1/client_health_scores_2026-04-03.csv" \\
    --pg-cache-dir "../Health V2/cache" \\
    --output-dir "./runs/2026-04-03_v1.0.0"

Environment variables:
  GOOGLE_APPLICATION_CREDENTIALS   Path to BigQuery service account JSON (required)
        """,
    )
    parser.add_argument(
        "--health-output",
        required=True,
        help="Path to Health V2 scored output CSV (client_health_scores_*.csv)",
    )
    parser.add_argument(
        "--pg-cache-dir",
        required=True,
        help="Path to directory containing pg_cat.csv and pg_cust.csv",
    )
    parser.add_argument(
        "--output-dir",
        default="./runs",
        help="Directory to write peer_cohort_assignments_*.csv (default: ./runs)",
    )
    parser.add_argument(
        "--bq-cache-dir",
        default=None,
        help="Directory with pre-fetched BigQuery CSV files (bq_vert.csv). When set, skips live BigQuery connection.",
    )

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
