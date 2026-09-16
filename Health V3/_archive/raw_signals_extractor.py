#!/usr/bin/env python3
"""
Health V3 — Raw Signals Extractor (no banding, no composite)

Re-reads the same V3 cache (Postgres + BigQuery CSVs) that the operator uses,
but emits the *raw* underlying values for every signal per org instead of
band-compressed scores. Used to evaluate whether the current band breakpoints
are well-placed against the actual data distribution.

Usage:
    python raw_signals_extractor.py \
        --mal "Health V2/inputs/master_account_list_2026-04-14_canonical.csv" \
        --cache-dir "Health V3/cache/2026-05-11" \
        --score-date 2026-05-11 \
        --output-dir "Health V3/runs/raw_2026-05-11"
"""

import argparse
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

BUNDLE_MAP = {
    "iPad-only": "iPad-only", "iPad+Catalog": "iPad+Catalog",
    "iPad+Catalog+Cart": "iPad+Catalog+Cart",
    "iPad+Catalog+Portal": "iPad+Catalog+Portal", "Full": "Full",
}

NEW_ORG_DAYS = 90
GHOST_ARR_THRESHOLD = 5000


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--mal", required=True)
    p.add_argument("--cache-dir", required=True)
    p.add_argument("--score-date", required=True)
    p.add_argument("--output-dir", required=True)
    return p.parse_args()


def load_mal(path):
    df = pd.read_csv(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.rename(columns={"ord_id": "org_shortname", "stack": "bundle"})
    df["org_shortname"] = df["org_shortname"].astype(str).str.lower().str.strip()
    df["bundle"] = df["bundle"].astype(str).str.strip().map(BUNDLE_MAP).fillna(df["bundle"])
    df["arr"] = pd.to_numeric(
        df["arr"].astype(str).str.replace("[$,]", "", regex=True), errors="coerce"
    ).fillna(0)
    df["cohort_year"] = pd.to_numeric(df["cohort_year"], errors="coerce").fillna(0).astype(int)
    return df[["org_shortname", "company", "bundle", "arr", "cohort_year"]]


def to_naive(ts):
    if ts is None or pd.isna(ts):
        return None
    if hasattr(ts, "tzinfo") and ts.tzinfo is not None:
        return ts.replace(tzinfo=None)
    return ts


def compute_freshness(org_imports_df, now):
    """Return list of (import_type, ratio) for feeds meeting the operator's
    min-history + initial-load carve-out criteria."""
    out = []
    for _, r in org_imports_df.iterrows():
        runs = int(r["run_count_180d"])
        if runs < 3:
            continue
        first_run = to_naive(r["first_run_at"])
        last_run = to_naive(r["last_run_at"])
        if first_run is None or last_run is None:
            continue
        days_span = (last_run - first_run).total_seconds() / 86400
        days_since_first = (now - first_run).total_seconds() / 86400
        days_since_last = (now - last_run).total_seconds() / 86400
        # operator's initial-load carve-out
        if runs < 5 and days_span <= 7 and days_since_first <= 14:
            continue
        mean_gap = days_span / max(runs - 1, 1)
        gap = max(mean_gap, 1.0)
        ratio = days_since_last / gap
        out.append((r["import_type"], ratio))
    return out


def main():
    args = parse_args()
    cache_dir = Path(args.cache_dir)
    score_date = args.score_date

    print(f"[INFO] Raw-signal extract — {score_date}")
    print(f"[INFO] Cache: {cache_dir}")

    mal = load_mal(args.mal)
    print(f"[OK] MAL: {len(mal)} orgs")

    org_cfg = pd.read_csv(cache_dir / "pg_org_config.csv")
    for c in [
        "contract_pricing_enabled", "enable_sales_data",
        "enable_online_catalog", "enable_online_ordering", "enable_sales_portal",
    ]:
        org_cfg[c] = org_cfg[c].astype(str).str.strip().str.lower().isin({"true", "1", "t", "yes", "y"})
    org_cfg["org_shortname"] = org_cfg["org_shortname"].astype(str).str.lower().str.strip()
    org_cfg = org_cfg.set_index("org_shortname")

    eng = pd.read_csv(
        cache_dir / "pg_engagement.csv",
        parse_dates=["last_login_at", "first_login_at"],
    ).set_index("organization_id")

    ss = pd.read_csv(cache_dir / "pg_smart_stacks.csv").set_index("organization_id")
    orders = pd.read_csv(cache_dir / "pg_orders.csv").set_index("organization_id")
    portal = pd.read_csv(cache_dir / "pg_portal_orders.csv").set_index("organization_id")
    cat = pd.read_csv(cache_dir / "pg_catalog.csv").set_index("organization_id")
    imp = pd.read_csv(
        cache_dir / "pg_imports.csv",
        parse_dates=["last_run_at", "first_run_at"],
    )
    imp["last_run_had_error"] = imp["last_run_had_error"].astype(str).str.strip().str.lower().isin({"true", "1", "t"})

    mp = pd.read_csv(cache_dir / "bq_mp_sharing.csv")
    mp["org_shortname"] = mp["org_shortname"].astype(str).str.lower().str.strip()
    mp = mp.set_index("org_shortname")

    now = datetime.utcnow()
    rows = []
    current_year = int(score_date[:4])

    for _, m in mal.iterrows():
        org = m["org_shortname"]
        if org not in org_cfg.index:
            continue
        cfg = org_cfg.loc[org]
        if isinstance(cfg, pd.DataFrame):
            cfg = cfg.iloc[0]
        cfg = cfg.to_dict()
        org_id = cfg["organization_id"]

        eng_row = eng.loc[org_id].to_dict() if org_id in eng.index else {}
        logins_90d = int(eng_row.get("logins_90d") or 0)
        active_90d = int(eng_row.get("active_users_90d") or 0)
        enabled = int(eng_row.get("enabled_users") or 0)
        au_365d = int(eng_row.get("active_users_365d") or 0)

        # Operator-matching fallback: when enabled=0 but 365d users exist,
        # use them as the denominator. Keep raw enabled_users separate.
        effective_denom = enabled
        denom_fallback_applied = False
        if enabled == 0 and au_365d > 0:
            effective_denom = au_365d
            denom_fallback_applied = True

        if effective_denom > 0:
            active_user_ratio = active_90d / effective_denom
        else:
            active_user_ratio = None

        last_login = to_naive(eng_row.get("last_login_at"))
        first_login = to_naive(eng_row.get("first_login_at"))
        days_since_last_login = (now - last_login).days if last_login is not None else None
        days_since_first_login = (now - first_login).days if first_login is not None else None

        # New-org exclusion
        if first_login is not None and days_since_first_login < NEW_ORG_DAYS:
            new_org_excluded = True
        elif first_login is None and int(m["cohort_year"]) == current_year:
            new_org_excluded = True
        else:
            new_org_excluded = False

        ss_count = int(ss.loc[org_id, "smart_stack_count"]) if org_id in ss.index else 0
        ipad_orders_90d = int(orders.loc[org_id, "ipad_orders_90d"]) if org_id in orders.index else 0
        portal_orders_90d = int(portal.loc[org_id, "portal_orders_90d"]) if org_id in portal.index else 0

        mp_row = mp.loc[org].to_dict() if org in mp.index else {}
        mp_item = int(mp_row.get("mp_item_email_drafted_90d") or 0)
        mp_doc = int(mp_row.get("mp_document_email_drafted_90d") or 0)
        mp_share_90d = mp_item + mp_doc

        # Imports for this org
        org_imp = imp[imp["organization_id"] == org_id]
        import_types_present = set(org_imp["import_type"].dropna().tolist())
        inv_in_history = "Inventory" in import_types_present
        inv_runs_90d = int(org_imp.loc[org_imp["import_type"] == "Inventory", "run_count_90d"].sum()) if inv_in_history else 0
        sd_in_history = "Sales Data" in import_types_present
        sd_runs_90d = int(org_imp.loc[org_imp["import_type"] == "Sales Data", "run_count_90d"].sum()) if sd_in_history else 0

        # Adoption features (1/0/-1)
        eoc = bool(cfg.get("enable_online_catalog"))
        eoo = bool(cfg.get("enable_online_ordering"))
        esp = bool(cfg.get("enable_sales_portal"))
        esd = bool(cfg.get("enable_sales_data"))

        feat_ipad = 1 if logins_90d > 0 else 0
        feat_smart_stacks = 1 if ss_count > 0 else 0
        feat_sharing = 1 if mp_share_90d > 0 else 0
        feat_ecat_catalog = (1 if portal_orders_90d > 0 else 0) if eoc else -1
        feat_online_ordering = (1 if portal_orders_90d > 0 else 0) if eoo else -1
        feat_sales_portal = (1 if portal_orders_90d > 0 else 0) if esp else -1
        feat_inventory_mgmt = (1 if inv_runs_90d > 0 else 0) if inv_in_history else -1
        feat_sales_data = (1 if sd_runs_90d > 0 else 0) if esd else -1

        feat_flags = [
            feat_ipad, feat_smart_stacks, feat_sharing,
            feat_ecat_catalog, feat_online_ordering, feat_sales_portal,
            feat_inventory_mgmt, feat_sales_data,
        ]
        features_applicable = sum(1 for f in feat_flags if f >= 0)
        features_used = sum(1 for f in feat_flags if f == 1)

        # Value-delivery channels (matches operator's score_value_delivery)
        channels = []
        channels.append(("Order volume (iPad)", True, ipad_orders_90d >= 10))
        channels.append(("Sharing activity", True, mp_share_90d >= 3))
        channels.append(("Online catalog active", eoc, portal_orders_90d > 0))
        channels.append(("Portal ordering", eoo, portal_orders_90d > 0))
        channels.append(("Sales Portal engagement", esp, portal_orders_90d > 0))
        channels.append(("Inventory data flowing", inv_in_history, inv_runs_90d > 0))
        channels_applicable = sum(1 for _, a, _ in channels if a)
        channels_achieved = sum(1 for _, a, u in channels if a and u)

        # Operational health raw
        if org_id in cat.index:
            cat_row = cat.loc[org_id]
            cat_total = int(cat_row["total_active"]) if not pd.isna(cat_row["total_active"]) else 0
            cat_complete = int(cat_row["complete_products"]) if not pd.isna(cat_row["complete_products"]) else 0
        else:
            cat_total = 0
            cat_complete = 0
        catalog_pct = (cat_complete / cat_total) if cat_total > 0 else None

        import_types_active = len(org_imp)
        import_types_healthy = int((~org_imp["last_run_had_error"]).sum()) if import_types_active > 0 else 0
        import_health_pct = (import_types_healthy / import_types_active) if import_types_active > 0 else None

        fresh = compute_freshness(org_imp, now)
        freshness_feeds_scored = len(fresh)
        if fresh:
            ratios = [r for _, r in fresh]
            freshness_avg_staleness_ratio = sum(ratios) / len(ratios)
            worst_name, worst_ratio = max(fresh, key=lambda x: x[1])
        else:
            freshness_avg_staleness_ratio = None
            worst_name = None
            worst_ratio = None

        ghost = bool(m["arr"] >= GHOST_ARR_THRESHOLD and logins_90d == 0)

        rows.append({
            "org_shortname": org,
            "org_name": cfg.get("org_name") or m["company"],
            "bundle": m["bundle"],
            "arr": float(m["arr"]),
            "cohort_year": int(m["cohort_year"]),

            "logins_90d": logins_90d,
            "active_users_90d": active_90d,
            "enabled_users": enabled,
            "active_users_365d": au_365d,
            "denom_fallback_applied": denom_fallback_applied,
            "active_user_ratio": round(active_user_ratio, 2) if active_user_ratio is not None else None,
            "days_since_last_login": days_since_last_login,

            "feat_ipad": feat_ipad,
            "feat_smart_stacks": feat_smart_stacks,
            "feat_sharing": feat_sharing,
            "feat_ecat_catalog": feat_ecat_catalog,
            "feat_online_ordering": feat_online_ordering,
            "feat_sales_portal": feat_sales_portal,
            "feat_inventory_mgmt": feat_inventory_mgmt,
            "feat_sales_data": feat_sales_data,
            "smart_stack_count": ss_count,
            "mp_share_events_90d": mp_share_90d,
            "features_applicable": features_applicable,
            "features_used": features_used,

            "ipad_orders_90d": ipad_orders_90d,
            "portal_orders_90d": portal_orders_90d,
            "channels_applicable": channels_applicable,
            "channels_achieved": channels_achieved,

            "catalog_total_active": cat_total,
            "catalog_complete": cat_complete,
            "catalog_pct": round(catalog_pct, 4) if catalog_pct is not None else None,
            "import_types_active": import_types_active,
            "import_types_healthy": import_types_healthy,
            "import_health_pct": round(import_health_pct, 4) if import_health_pct is not None else None,
            "freshness_feeds_scored": freshness_feeds_scored,
            "freshness_avg_staleness_ratio": round(freshness_avg_staleness_ratio, 3) if freshness_avg_staleness_ratio is not None else None,
            "freshness_worst_feed": worst_name,
            "freshness_worst_ratio": round(worst_ratio, 3) if worst_ratio is not None else None,

            "ghost_account": ghost,
            "new_org_excluded": new_org_excluded,

            "enable_online_catalog": eoc,
            "enable_online_ordering": eoo,
            "enable_sales_portal": esp,
            "enable_sales_data": esd,
        })

    df = pd.DataFrame(rows)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f"raw_signals_{score_date}.csv"
    df.to_csv(out_csv, index=False)
    print(f"[OK] Wrote {out_csv} ({len(df)} rows)")

    # ----------------------------------------------------------------------
    # Distribution summary
    # ----------------------------------------------------------------------
    def quantiles(series, label):
        s = series.dropna()
        if len(s) == 0:
            return None
        return {
            "signal": label,
            "n": int(len(s)),
            "min": float(s.min()),
            "p10": float(s.quantile(0.10)),
            "p25": float(s.quantile(0.25)),
            "median": float(s.median()),
            "p75": float(s.quantile(0.75)),
            "p90": float(s.quantile(0.90)),
            "max": float(s.max()),
        }

    adoption_ratio = df["features_used"] / df["features_applicable"]
    value_ratio = df["channels_achieved"] / df["channels_applicable"]

    summaries = [
        quantiles(df["logins_90d"], "logins_90d"),
        quantiles(df["active_user_ratio"], "active_user_ratio"),
        quantiles(df["days_since_last_login"], "days_since_last_login"),
        quantiles(df["catalog_pct"], "catalog_pct"),
        quantiles(df["freshness_avg_staleness_ratio"], "freshness_avg_staleness_ratio"),
        quantiles(adoption_ratio, "features_used/features_applicable"),
        quantiles(value_ratio, "channels_achieved/channels_applicable"),
    ]
    summary_df = pd.DataFrame([s for s in summaries if s is not None])
    summary_csv = out_dir / "distribution_summary.csv"
    summary_df.to_csv(summary_csv, index=False)
    print(f"[OK] Wrote {summary_csv}")

    # Auxiliary % stats
    n = len(df)
    pct_zero_logins = (df["logins_90d"] == 0).sum() / n * 100
    pct_zero_ipad = (df["ipad_orders_90d"] == 0).sum() / n * 100
    portal_configured = df[df["enable_online_catalog"] | df["enable_online_ordering"] | df["enable_sales_portal"]]
    if len(portal_configured) > 0:
        pct_zero_portal = (portal_configured["portal_orders_90d"] == 0).sum() / len(portal_configured) * 100
    else:
        pct_zero_portal = None
    cat_with_data = df[df["catalog_pct"].notna()]
    pct_cat_85 = (cat_with_data["catalog_pct"] >= 0.85).sum() / len(cat_with_data) * 100 if len(cat_with_data) > 0 else None
    imp_with_data = df[df["import_types_active"] > 0]
    pct_with_error = ((imp_with_data["import_types_active"] - imp_with_data["import_types_healthy"]) > 0).sum() / len(imp_with_data) * 100 if len(imp_with_data) > 0 else None

    aux = pd.DataFrame([
        {"metric": "pct_orgs_logins_90d_zero", "value_pct": pct_zero_logins, "n": n},
        {"metric": "pct_orgs_ipad_orders_90d_zero", "value_pct": pct_zero_ipad, "n": n},
        {"metric": "pct_portal_configured_with_zero_portal_orders",
         "value_pct": pct_zero_portal, "n": int(len(portal_configured))},
        {"metric": "pct_orgs_catalog_pct_gte_0.85",
         "value_pct": pct_cat_85, "n": int(len(cat_with_data))},
        {"metric": "pct_orgs_with_at_least_one_import_error",
         "value_pct": pct_with_error, "n": int(len(imp_with_data))},
    ])
    aux_csv = out_dir / "aux_stats.csv"
    aux.to_csv(aux_csv, index=False)
    print(f"[OK] Wrote {aux_csv}")


if __name__ == "__main__":
    main()
