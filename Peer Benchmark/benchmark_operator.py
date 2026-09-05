"""
Peer Benchmark — Layer 2: Benchmark Metric Calculation
=======================================================
Consumes the Layer 1 cohort assignment output and computes per-org benchmark
comparisons: cohort percentile rank, delta vs median, and quartile position
for each metric in the v1 benchmark metric set.

Usage:
  python benchmark_operator.py \\
    --cohort-output "./runs/2026-04-03_v1.0.1/peer_cohort_assignments_2026-04-03.csv" \\
    --health-output "/path/to/Health V2/runs/.../client_health_scores_*.csv" \\
    --pg-cache-dir "/path/to/Health V2/cache" \\
    --output-dir "./runs/2026-04-03_v1.0.1"

Outputs (written to --output-dir):
  peer_benchmark_YYYY-MM-DD.csv        Wide format: one row per org, all benchmark stats
  peer_benchmark_long_YYYY-MM-DD.csv   Long format: one row per org × metric (audit/report use)

Dependencies:
  pip install pandas numpy
"""

import argparse
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

# ── Version ───────────────────────────────────────────────────────────────────

VERSION = "1.1.0"
LAYER1_VERSION = "1.0.1"

# ── Bundle primary value metric mapping (mirrors Health V2 BUNDLE_CONFIG) ─────
#
# Health V2 peer_benchmark_gap compares three dimensions:
#   1. login_intensity         (all bundles)
#   2. primary_value_metric    (bundle-specific, see below)
#   3. adoption_score          (all bundles)
#
# primary_value_metric by bundle:
#   iPad-only, iPad+Catalog:         presentation_actions
#   iPad+Catalog+Cart, Full:         orders_90d
#   iPad+Catalog+Portal:             presentation_portal_avg
#
# Layer 2 exposes these three dimensions explicitly so Health V2 can replace
# its current bundle-median method with peer-cohort percentile ranks.
# Do NOT use health_score_pctile for this — health_score already aggregates
# multiple dimensions and using it here would create circularity.
#
BUNDLE_PRIMARY_VALUE_METRIC = {
    "iPad-only":             "presentation_actions",
    "iPad+Catalog":          "presentation_actions",
    "iPad+Catalog+Cart":     "orders_90d",
    "iPad+Catalog+Portal":   "presentation_portal_avg",
    "Full":                  "orders_90d",
}

# ── Metric definitions ────────────────────────────────────────────────────────
#
# Each metric entry:
#   source:       "hv2" | "cache" | "mp_cache" | "derived"
#   cache_file:   filename if source == "cache" or "mp_cache"
#   cache_col:    column name in cache file
#   applies_to:   set of bundles where this metric is meaningful, or None (all bundles)
#   direction:    "higher_better" | "lower_better"
#   label:        human-readable label for reporting
#   hv2_pbg_dim:  True if this metric is one of the three Health V2 peer benchmark gap dimensions
#
# Metrics are split into two groups:
#   REPORT_METRICS  — report-oriented (existing Layer 2 v1.0.0 output)
#   HV2_PBG_METRICS — Health V2 peer_benchmark_gap dimensions (added in v1.1.0)
#
REPORT_METRICS = [
    {
        "id": "health_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Overall Health Score",
    },
    {
        "id": "value_delivery_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Value Delivery Score",
    },
    {
        "id": "adoption_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Feature Adoption Score",
    },
    {
        "id": "engagement_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Rep Engagement Score",
    },
    {
        "id": "operational_health_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Operational Health Score",
    },
    {
        "id": "trajectory_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Trajectory Score",
    },
    {
        "id": "orders_90d",
        "source": "cache",
        "cache_file": "pg_ord.csv",
        "cache_col": "orders_90d",
        "applies_to": {"iPad+Catalog+Cart", "Full"},
        "direction": "higher_better",
        "label": "Orders (Last 90 Days)",
    },
    {
        "id": "orders_per_user",
        "source": "derived",
        "numerator": "orders_90d",
        "denominator": "total_users",
        "applies_to": {"iPad+Catalog+Cart", "Full"},
        "direction": "higher_better",
        "label": "Orders per User (Last 90 Days)",
    },
    {
        "id": "catalog_completeness",
        "source": "cache",
        "cache_file": "pg_cat.csv",
        "cache_col": "catalog_completeness",
        "applies_to": {"iPad+Catalog", "iPad+Catalog+Cart", "iPad+Catalog+Portal", "Full"},
        "direction": "higher_better",
        "label": "Catalog Completeness",
    },
]

# Health V2 peer_benchmark_gap dimensions.
# These three metrics are the ONLY ones Health V2 should use to replace peer_benchmark_gap.
# They correspond exactly to the three dimensions in Health V2's score_peer_benchmark_gap().
HV2_PBG_METRICS = [
    {
        "id": "login_intensity",
        "source": "mp_cache",
        "cache_file": "bq_mp_pbg.csv",
        "cache_col": "login_intensity",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Login Intensity (logins / active user)",
        "hv2_pbg_dim": True,
        "hv2_note": "Dimension 1 of 3 in Health V2 peer_benchmark_gap",
    },
    {
        "id": "primary_value_metric",
        "source": "bundle_routed",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Primary Value Metric (bundle-specific)",
        "hv2_pbg_dim": True,
        "hv2_note": (
            "Dimension 2 of 3 in Health V2 peer_benchmark_gap. "
            "iPad-only/iPad+Catalog: presentation_actions. "
            "Cart/Full: orders_90d. "
            "Portal: presentation_portal_avg."
        ),
    },
    {
        "id": "adoption_score",
        "source": "hv2",
        "applies_to": None,
        "direction": "higher_better",
        "label": "Feature Adoption Score",
        "hv2_pbg_dim": True,
        "hv2_note": "Dimension 3 of 3 in Health V2 peer_benchmark_gap (same as REPORT_METRICS adoption_score)",
    },
]

# Combined metric list (report metrics first, then HV2 PBG-specific ones)
# adoption_score appears in both; it is computed once from REPORT_METRICS and reused.
METRICS = REPORT_METRICS + [m for m in HV2_PBG_METRICS if m["id"] not in {r["id"] for r in REPORT_METRICS}]

# Index by id for quick lookup
METRIC_INDEX = {m["id"]: m for m in METRICS}


# ── Loaders ───────────────────────────────────────────────────────────────────

def load_cohort(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"[FATAL] Cohort file not found: {path}")
        sys.exit(1)
    df = pd.read_csv(path)
    required = {"org_shortname", "benchmark_eligible", "peer_orgs", "peer_group_id_effective",
                "peer_group_level", "peer_group_n", "benchmark_confidence", "bundle"}
    missing = required - set(df.columns)
    if missing:
        print(f"[FATAL] Cohort file missing columns: {missing}")
        sys.exit(1)
    print(f"[OK] Cohort: {len(df)} orgs, Layer 1 source loaded")
    return df


def load_health_output(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"[FATAL] Health V2 output not found: {path}")
        sys.exit(1)
    df = pd.read_csv(path)
    print(f"[OK] Health V2 output: {len(df)} orgs")
    return df


def load_pg_cache(cache_dir: str, filename: str) -> pd.DataFrame:
    path = os.path.join(cache_dir, filename)
    if not os.path.exists(path):
        print(f"[WARN] Cache file missing: {path} — affected metrics will be null")
        return pd.DataFrame(columns=["org_shortname"])
    df = pd.read_csv(path)
    print(f"[OK] {filename}: {len(df)} rows (from cache)")
    return df


# ── Metric value assembly ─────────────────────────────────────────────────────

def assemble_metric_values(df: pd.DataFrame, hv2: pd.DataFrame,
                            pg_ord: pd.DataFrame, pg_cat: pd.DataFrame,
                            pg_users: pd.DataFrame, mp_pbg: pd.DataFrame) -> pd.DataFrame:
    """
    Join all metric sources onto the cohort DataFrame.
    Returns df with one raw-value column per metric.

    mp_pbg contains the Health V2 peer_benchmark_gap dimensions:
      login_intensity, presentation_actions, presentation_portal_avg
    These are sourced from BigQuery (org_summary + mixpanel.events, 90d window).
    """
    hv2_cols = ["org_shortname", "health_score", "value_delivery_score", "adoption_score",
                "engagement_score", "operational_health_score", "trajectory_score", "growth_score"]
    hv2_sub = hv2[[c for c in hv2_cols if c in hv2.columns]]
    df = df.merge(hv2_sub, on="org_shortname", how="left")

    if "orders_90d" in pg_ord.columns:
        df = df.merge(pg_ord[["org_shortname", "orders_90d"]], on="org_shortname", how="left")
    else:
        df["orders_90d"] = np.nan

    if "catalog_completeness" in pg_cat.columns:
        df = df.merge(pg_cat[["org_shortname", "catalog_completeness"]], on="org_shortname", how="left")
    else:
        df["catalog_completeness"] = np.nan

    if "total_users" in pg_users.columns:
        df = df.merge(pg_users[["org_shortname", "total_users"]], on="org_shortname", how="left")
    else:
        df["total_users"] = np.nan

    # Derived: orders_per_user (report metric)
    df["orders_per_user"] = (
        df["orders_90d"] / df["total_users"].replace(0, np.nan)
    ).round(3)

    # Merge Health V2 peer benchmark gap dimensions from Mixpanel + org_summary cache
    mp_cols = ["org_shortname", "login_intensity", "presentation_actions",
               "mp_access_sales_portal", "presentation_portal_avg"]
    mp_sub = mp_pbg[[c for c in mp_cols if c in mp_pbg.columns]]
    df = df.merge(mp_sub, on="org_shortname", how="left")

    # Bundle-routed primary_value_metric: resolves to the correct raw column per bundle
    # This mirrors Health V2's BUNDLE_CONFIG primary_value_metric exactly.
    def resolve_primary_value(row):
        pvm = BUNDLE_PRIMARY_VALUE_METRIC.get(row["bundle"])
        if pvm == "presentation_actions":
            return row.get("presentation_actions", np.nan)
        elif pvm == "orders_90d":
            return row.get("orders_90d", np.nan)
        elif pvm == "presentation_portal_avg":
            return row.get("presentation_portal_avg", np.nan)
        return np.nan

    df["primary_value_metric"] = df.apply(resolve_primary_value, axis=1)

    return df


# ── Benchmark computation ─────────────────────────────────────────────────────

def metric_applies(metric_def: dict, bundle: str) -> bool:
    """Returns True if this metric is applicable for the given bundle."""
    if metric_def["applies_to"] is None:
        return True
    return bundle in metric_def["applies_to"]


def compute_benchmark_for_metric(df: pd.DataFrame, metric_id: str) -> dict:
    """
    For each eligible org, compute benchmark stats for one metric.
    Returns dict: {org_shortname -> {org_value, peer_p25, peer_median, peer_p75,
                                     percentile_rank, delta_vs_median, quartile,
                                     metric_applicable, n_peers_with_data}}
    """
    metric_def = METRIC_INDEX[metric_id]
    results = {}

    for _, row in df.iterrows():
        org = row["org_shortname"]
        applicable = metric_applies(metric_def, row["bundle"])

        if not row["benchmark_eligible"] or not applicable:
            results[org] = {
                "org_value": row.get(metric_id, np.nan),
                "peer_p25": np.nan,
                "peer_median": np.nan,
                "peer_p75": np.nan,
                "percentile_rank": np.nan,
                "delta_vs_median": np.nan,
                "quartile": None,
                "metric_applicable": applicable,
                "n_peers_with_data": 0,
            }
            continue

        peer_list = [p for p in str(row["peer_orgs"]).split("|") if p]
        org_val = row.get(metric_id, np.nan)

        if not peer_list:
            results[org] = {
                "org_value": org_val,
                "peer_p25": np.nan, "peer_median": np.nan, "peer_p75": np.nan,
                "percentile_rank": np.nan, "delta_vs_median": np.nan,
                "quartile": None, "metric_applicable": True, "n_peers_with_data": 0,
            }
            continue

        # Get peer values, excluding nulls from both the peer list and from applicability
        peer_rows = df[df["org_shortname"].isin(peer_list)]
        peer_applicable = peer_rows[
            peer_rows["bundle"].apply(lambda b: metric_applies(metric_def, b))
        ]
        peer_vals = peer_applicable[metric_id].dropna()

        n_peers = len(peer_vals)

        if n_peers == 0 or pd.isna(org_val):
            results[org] = {
                "org_value": org_val,
                "peer_p25": np.nan, "peer_median": np.nan, "peer_p75": np.nan,
                "percentile_rank": np.nan, "delta_vs_median": np.nan,
                "quartile": None, "metric_applicable": True, "n_peers_with_data": 0,
            }
            continue

        p25 = float(peer_vals.quantile(0.25))
        p50 = float(peer_vals.quantile(0.50))
        p75 = float(peer_vals.quantile(0.75))
        pctile = float((peer_vals <= float(org_val)).mean())
        delta = float(org_val) - p50

        if pctile >= 0.75:
            quartile = "Q4"
        elif pctile >= 0.50:
            quartile = "Q3"
        elif pctile >= 0.25:
            quartile = "Q2"
        else:
            quartile = "Q1"

        results[org] = {
            "org_value": float(org_val),
            "peer_p25": round(p25, 2),
            "peer_median": round(p50, 2),
            "peer_p75": round(p75, 2),
            "percentile_rank": round(pctile, 3),
            "delta_vs_median": round(delta, 2),
            "quartile": quartile,
            "metric_applicable": True,
            "n_peers_with_data": n_peers,
        }

    return results


# ── Output builders ───────────────────────────────────────────────────────────

def build_wide_output(df: pd.DataFrame, benchmark_results: dict,
                      run_date: date) -> pd.DataFrame:
    """
    One row per org. Five columns per metric:
      {metric}_org, {metric}_peer_median, {metric}_pctile,
      {metric}_vs_median, {metric}_quartile

    Also includes three composite HV2 peer benchmark gap columns:
      hv2_pbg_login_intensity_pctile      — Dimension 1
      hv2_pbg_primary_value_pctile        — Dimension 2 (bundle-routed)
      hv2_pbg_adoption_pctile             — Dimension 3
      hv2_pbg_composite_gap               — Average of the three (0-100, higher = larger gap)
      hv2_pbg_primary_value_metric_id     — Which raw metric primary_value_metric resolved to

    These HV2 columns are the direct replacement for Health V2's peer_benchmark_gap.
    They are non-circular: they use underlying dimensions, not the rolled-up health_score.
    """
    context_cols = ["org_shortname", "org_name", "bundle", "vertical",
                    "peer_group_id_effective", "peer_group_level", "peer_group_n",
                    "benchmark_eligible", "benchmark_confidence"]
    ctx = df[[c for c in context_cols if c in df.columns]].copy()

    for metric_id, org_results in benchmark_results.items():
        ctx[f"{metric_id}_org"]        = ctx["org_shortname"].map(
            lambda o: org_results.get(o, {}).get("org_value"))
        ctx[f"{metric_id}_peer_median"] = ctx["org_shortname"].map(
            lambda o: org_results.get(o, {}).get("peer_median"))
        ctx[f"{metric_id}_pctile"]     = ctx["org_shortname"].map(
            lambda o: org_results.get(o, {}).get("percentile_rank"))
        ctx[f"{metric_id}_vs_median"]  = ctx["org_shortname"].map(
            lambda o: org_results.get(o, {}).get("delta_vs_median"))
        ctx[f"{metric_id}_quartile"]   = ctx["org_shortname"].map(
            lambda o: org_results.get(o, {}).get("quartile"))

    # ── Health V2 peer_benchmark_gap replacement columns ──────────────────────
    # Expose each of the three HV2 gap dimensions as named aliases,
    # plus the composite gap score that replicates the existing scoring formula.
    #
    # Health V2's _percentile_gap_score maps:
    #   below p25  → 100 (large gap)
    #   p25–p50    →  75
    #   p50–p75    →  40
    #   above p75  →  10 (small/no gap)
    # peer_benchmark_gap = mean of 3 dimension gap scores
    #
    # Here we output the raw pctile for each dimension (for maximum flexibility)
    # plus a pre-computed composite_gap that matches Health V2's existing formula,
    # so it can be dropped in as a direct replacement with no further arithmetic.

    def pbg_gap_score(pctile):
        """Replicates Health V2 _percentile_gap_score from percentile rank."""
        if pd.isna(pctile):
            return 50  # Health V2 default for missing data
        if pctile < 0.25:
            return 100
        elif pctile < 0.50:
            return 75
        elif pctile < 0.75:
            return 40
        return 10

    li_pctile  = benchmark_results.get("login_intensity", {})
    pv_pctile  = benchmark_results.get("primary_value_metric", {})
    ad_pctile  = benchmark_results.get("adoption_score", {})

    ctx["hv2_pbg_login_intensity_pctile"] = ctx["org_shortname"].map(
        lambda o: li_pctile.get(o, {}).get("percentile_rank"))
    ctx["hv2_pbg_primary_value_pctile"] = ctx["org_shortname"].map(
        lambda o: pv_pctile.get(o, {}).get("percentile_rank"))
    ctx["hv2_pbg_adoption_pctile"] = ctx["org_shortname"].map(
        lambda o: ad_pctile.get(o, {}).get("percentile_rank"))

    # Which raw metric did primary_value_metric resolve to for this org?
    ctx["hv2_pbg_primary_value_metric_id"] = ctx["bundle"].map(BUNDLE_PRIMARY_VALUE_METRIC)

    # Composite gap: mean of three dimension gap scores (matches Health V2 formula)
    def compute_composite_gap(row):
        if not row.get("benchmark_eligible", False):
            return None
        li = pbg_gap_score(row["hv2_pbg_login_intensity_pctile"])
        pv = pbg_gap_score(row["hv2_pbg_primary_value_pctile"])
        ad = pbg_gap_score(row["hv2_pbg_adoption_pctile"])
        return round((li + pv + ad) / 3)

    ctx["hv2_pbg_composite_gap"] = ctx.apply(compute_composite_gap, axis=1)

    ctx["run_date"] = run_date.isoformat()
    ctx["benchmark_month"] = run_date.strftime("%Y-%m")
    return ctx


def build_long_output(df: pd.DataFrame, benchmark_results: dict,
                      run_date: date) -> pd.DataFrame:
    """
    One row per org × metric. Includes metric_applicable flag and raw peer distribution.
    """
    rows = []
    for metric_id, metric_def in METRIC_INDEX.items():
        org_results = benchmark_results.get(metric_id, {})
        for _, org_row in df.iterrows():
            org = org_row["org_shortname"]
            r = org_results.get(org, {})
            rows.append({
                "org_shortname": org,
                "org_name": org_row.get("org_name"),
                "bundle": org_row.get("bundle"),
                "vertical": org_row.get("vertical"),
                "peer_group_id_effective": org_row.get("peer_group_id_effective"),
                "peer_group_level": org_row.get("peer_group_level"),
                "peer_group_n": org_row.get("peer_group_n"),
                "benchmark_eligible": org_row.get("benchmark_eligible"),
                "benchmark_confidence": org_row.get("benchmark_confidence"),
                "metric": metric_id,
                "metric_label": metric_def["label"],
                "metric_applicable": r.get("metric_applicable", False),
                "org_value": r.get("org_value"),
                "peer_p25": r.get("peer_p25"),
                "peer_median": r.get("peer_median"),
                "peer_p75": r.get("peer_p75"),
                "percentile_rank": r.get("percentile_rank"),
                "delta_vs_median": r.get("delta_vs_median"),
                "quartile": r.get("quartile"),
                "n_peers_with_data": r.get("n_peers_with_data", 0),
                "run_date": run_date.isoformat(),
                "benchmark_month": run_date.strftime("%Y-%m"),
            })
    return pd.DataFrame(rows)


# ── Summary ───────────────────────────────────────────────────────────────────

def print_summary(wide: pd.DataFrame, long_df: pd.DataFrame, run_date: date):
    print(f"\n{'='*60}")
    print(f"  BENCHMARK CALCULATION COMPLETE")
    print(f"{'='*60}")
    print(f"  Orgs processed: {len(wide)}")
    eligible = wide[wide["benchmark_eligible"] == True]
    print(f"  Benchmark eligible: {len(eligible)}")
    print()

    print("  Quartile distribution by metric (eligible only):")
    for m in METRICS:
        mid = m["id"]
        col = f"{mid}_quartile"
        if col not in eligible.columns:
            continue
        dist = eligible[col].value_counts().reindex(["Q1","Q2","Q3","Q4"]).fillna(0).astype(int)
        non_null = eligible[col].notna().sum()
        print(f"    {mid:35s}: Q1={dist['Q1']} Q2={dist['Q2']} Q3={dist['Q3']} Q4={dist['Q4']}  (n={non_null})")

    print()
    print("  Health score benchmark summary (top/bottom 5 by pctile, eligible):")
    col = "health_score_pctile"
    if col in eligible.columns:
        ranked = eligible[["org_shortname","bundle","peer_group_id_effective",
                           "health_score_org","health_score_peer_median",
                           "health_score_pctile","health_score_quartile"]].dropna(subset=[col])
        ranked = ranked.sort_values(col, ascending=False)
        print("  Top 5:")
        print(ranked.head(5).to_string(index=False))
        print("  Bottom 5:")
        print(ranked.tail(5).to_string(index=False))

    print()
    print("  HV2 peer_benchmark_gap replacement fields (eligible only):")
    for col in ["hv2_pbg_login_intensity_pctile","hv2_pbg_primary_value_pctile","hv2_pbg_adoption_pctile"]:
        if col in eligible.columns:
            n = eligible[col].notna().sum()
            med = eligible[col].median()
            print(f"    {col}: {n} orgs with value, median pctile={med:.2f}")
    if "hv2_pbg_composite_gap" in eligible.columns:
        comp = eligible["hv2_pbg_composite_gap"]
        print(f"    hv2_pbg_composite_gap: min={comp.min():.0f}, median={comp.median():.0f}, max={comp.max():.0f}")

    print(f"\n  Long format rows: {len(long_df)}")
    print(f"{'='*60}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def run(args):
    run_date = date.today()

    print(f"\n{'='*60}")
    print(f"  Peer Benchmark Layer 2 v{VERSION}")
    print(f"  Benchmark Metric Calculation")
    print(f"  Run date: {run_date}")
    print(f"{'='*60}")

    # Load inputs
    print("\n=== DATA LOADING ===")
    cohort = load_cohort(args.cohort_output)
    hv2 = load_health_output(args.health_output)
    cache_dir = args.pg_cache_dir
    pg_ord   = load_pg_cache(cache_dir, "pg_ord.csv")
    pg_cat   = load_pg_cache(cache_dir, "pg_cat.csv")
    pg_users = load_pg_cache(cache_dir, "pg_users.csv")
    mp_pbg   = load_pg_cache(cache_dir, "bq_mp_pbg.csv")
    if "login_intensity" not in mp_pbg.columns:
        print("[WARN] bq_mp_pbg.csv missing expected columns — HV2 PBG dimensions will be null")
        print("       Regenerate with: see QUERIES.md Q-MP-PBG")

    # Assemble metric values onto cohort
    print("\n=== ASSEMBLING METRICS ===")
    df = assemble_metric_values(cohort, hv2, pg_ord, pg_cat, pg_users, mp_pbg)
    for m in METRICS:
        mid = m["id"]
        if mid in df.columns:
            non_null = df[mid].notna().sum()
            print(f"  {mid}: {non_null}/{len(df)} orgs have values")
        else:
            print(f"  {mid}: NOT FOUND in assembled data")

    # Compute benchmarks per metric
    print("\n=== COMPUTING BENCHMARKS ===")
    benchmark_results = {}
    for m in METRICS:
        mid = m["id"]
        if mid not in df.columns:
            print(f"  [SKIP] {mid}: column not available")
            continue
        benchmark_results[mid] = compute_benchmark_for_metric(df, mid)
        eligible_count = sum(
            1 for r in benchmark_results[mid].values()
            if r.get("percentile_rank") is not None and not (
                isinstance(r["percentile_rank"], float) and np.isnan(r["percentile_rank"])
            )
        )
        print(f"  [OK] {mid}: {eligible_count} orgs with benchmark result")

    # Build outputs
    print("\n=== BUILDING OUTPUT ===")
    wide = build_wide_output(df, benchmark_results, run_date)
    long_df = build_long_output(df, benchmark_results, run_date)

    # Write
    os.makedirs(args.output_dir, exist_ok=True)
    wide_path = os.path.join(args.output_dir, f"peer_benchmark_{run_date.isoformat()}.csv")
    long_path = os.path.join(args.output_dir, f"peer_benchmark_long_{run_date.isoformat()}.csv")
    wide.to_csv(wide_path, index=False)
    long_df.to_csv(long_path, index=False)

    print_summary(wide, long_df, run_date)
    print(f"  Wide output:  {wide_path}")
    print(f"  Long output:  {long_path}")
    print(f"  Wide columns: {len(wide.columns)}")
    print(f"  Long rows:    {len(long_df)}")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Peer Benchmark Layer 2 — Benchmark Metric Calculation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python benchmark_operator.py \\
    --cohort-output "./runs/2026-04-03_v1.0.1/peer_cohort_assignments_2026-04-03.csv" \\
    --health-output "/path/to/Health V2/runs/.../client_health_scores_2026-04-03.csv" \\
    --pg-cache-dir "/path/to/Health V2/cache" \\
    --output-dir "./runs/2026-04-03_v1.0.1"

Output files:
  peer_benchmark_YYYY-MM-DD.csv        Wide: one row per org, all benchmark stats
  peer_benchmark_long_YYYY-MM-DD.csv   Long: one row per org × metric (audit/report)
        """,
    )
    parser.add_argument(
        "--cohort-output", required=True,
        help="Path to Layer 1 peer_cohort_assignments_*.csv",
    )
    parser.add_argument(
        "--health-output", required=True,
        help="Path to Health V2 client_health_scores_*.csv",
    )
    parser.add_argument(
        "--pg-cache-dir", required=True,
        help="Path to directory containing pg_ord.csv, pg_cat.csv, pg_users.csv",
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Directory to write peer_benchmark_*.csv outputs",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
