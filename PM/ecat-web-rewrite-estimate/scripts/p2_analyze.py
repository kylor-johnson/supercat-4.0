"""Phase 2 assembly: distributions, coverage reconciliation, 02_TENANT_CENSUS.json.

Percentiles are computed here rather than in SQL because the Postgres MCP query
validator rejects `percentile_cont(...) WITHIN GROUP`. Inputs are the verbatim
strings in p2_pg_raw.py and the CSVs written by the BigQuery scripts.
"""
import csv
import json
import os

import p2_pg_raw as raw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "out")
DEST = os.path.join(HERE, "..", "02_TENANT_CENSUS.json")

TOTAL_ORGS = raw.SCALARS["orgs_total"]


def parse(s):
    """'12:34 56:78' -> {12: 34, 56: 78}"""
    d = {}
    for tok in s.split():
        k, _, v = tok.partition(":")
        d[int(k)] = int(v)
    return d


def pct(sorted_vals, p):
    """Linear-interpolated percentile. Defined locally; see module docstring."""
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    i = p * (len(sorted_vals) - 1)
    lo, hi = int(i), min(int(i) + 1, len(sorted_vals) - 1)
    return round(sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (i - lo), 1)


def dist(name, s, source):
    d = parse(s)
    vals = sorted(d.values())
    return {
        "metric": name,
        "orgs_with_nonzero": len(d),
        "orgs_with_zero_or_absent": TOTAL_ORGS - len(d),
        "grand_total": sum(vals),
        "min": vals[0], "p10": pct(vals, .10), "median": pct(vals, .50),
        "p90": pct(vals, .90), "max": vals[-1],
        "top5_org_ids": [k for k, _ in sorted(d.items(), key=lambda kv: -kv[1])[:5]],
        "per_tenant": d,
        "source": source,
    }


SRC_PG = ("MCP user-supercat-postgres-vpn execute_sql, 2026-08-08; "
          "SQL in scripts/p2_pg_raw.py SQL_LOG; verbatim result in "
          "scripts/p2_pg_raw.py")

METRICS = [
    ("skus_active", raw.SKUS_ACTIVE), ("product_images", raw.PRODUCT_IMAGES),
    ("options", raw.OPTIONS), ("option_groups", raw.OPTION_GROUPS),
    ("option_mappings", raw.OPTION_MAPPINGS), ("kit_items", raw.KIT_ITEMS),
    ("matrix_options", raw.MATRIX_OPTIONS),
    ("contract_prices", raw.CONTRACT_PRICES), ("customers", raw.CUSTOMERS),
    ("inventories", raw.INVENTORIES), ("price_levels", raw.PRICE_LEVELS),
    ("taxonomies", raw.TAXONOMIES),
    ("distribution_centers", raw.DISTRIBUTION_CENTERS),
    ("user_types", raw.USER_TYPES), ("shared_resources", raw.SHARED_RESOURCES),
    ("surcharge_types", raw.SURCHARGE_TYPES),
    ("smart_stacks", raw.SMART_STACKS), ("ipad_reports", raw.IPAD_REPORTS),
    ("showroom_locations", raw.SHOWROOM_LOCATIONS),
    ("commitment_reports", raw.COMMITMENT_REPORTS),
    ("placement_reports", raw.PLACEMENT_REPORTS),
    ("rma_requests", raw.RMA_REQUESTS), ("mobile_sites", raw.MOBILE_SITES),
    ("product_custom_fields", raw.PRODUCT_CUSTOM_FIELDS),
    ("customer_custom_fields", raw.CUSTOMER_CUSTOM_FIELDS),
    ("inventory_custom_fields", raw.INVENTORY_CUSTOM_FIELDS),
    ("option_custom_fields", raw.OPTION_CUSTOM_FIELDS),
    ("order_custom_fields", raw.ORDER_CUSTOM_FIELDS),
]

out = {"generated": "2026-08-08", "orgs_total_postgres": TOTAL_ORGS,
       "distributions": {}, "sources": {"postgres": SRC_PG}}

for name, s in METRICS:
    out["distributions"][name] = dist(name, s, SRC_PG)

# --- blast radius table --------------------------------------------------
br, by_short, by_id = [], {}, {}
for tok in raw.BLAST_RADIUS.split():
    p = tok.split(":")
    rec = {"shortname": p[0], "org_id": int(p[1]), "org_users": int(p[2]),
           "ipad_ever": int(p[3]), "ipad_active_30d": int(p[4]),
           "eol_ever": int(p[5]), "orders_12mo": int(p[6])}
    br.append(rec)
    by_short[rec["shortname"]] = rec
    by_id[rec["org_id"]] = rec
out["blast_radius"] = {"per_tenant": br, "source": SRC_PG}

# --- orders / login activity --------------------------------------------
orders = {}
for tok in raw.ORDERS.split():
    p = tok.split(":")
    orders[int(p[0])] = {"orders_all": int(p[1]), "submitted": int(p[2]),
                         "last_order": p[3]}
logins = {}
for tok in raw.LOGIN_EVENTS.split():
    p = tok.split(":")
    logins[int(p[0])] = {"events": int(p[1]), "users": int(p[2]),
                         "devices": int(p[3]), "last_seen": p[4],
                         "first_seen": p[5]}
out["orders_lifetime"] = {"per_tenant": orders, "source": SRC_PG}
out["login_events"] = {
    "per_tenant": logins, "source": SRC_PG,
    "coverage_note": "min(created_at) clusters at 2025-02-08 for 150+ orgs; "
                     "that is the login_events retention floor, not tenant age."}

# --- activity classification (definitions are categorical, not temporal
#     judgements about effort) ------------------------------------------
buckets = {"ipad_active_30d": [], "ipad_ever_never_recent": [],
           "no_ipad_user_ever": [], "orders_but_no_ipad": []}
for r in br:
    if r["ipad_active_30d"] > 0:
        buckets["ipad_active_30d"].append(r["shortname"])
    elif r["ipad_ever"] > 0:
        buckets["ipad_ever_never_recent"].append(r["shortname"])
    else:
        buckets["no_ipad_user_ever"].append(r["shortname"])
out["activity_classification"] = {
    "counts": {k: len(v) for k, v in buckets.items()},
    "members": buckets,
    "definition": {
        "ipad_active_30d": "org has >=1 org_user with last_ipad_login_at "
                           "within 30 days of 2026-08-08",
        "ipad_ever_never_recent": "org has org_users that logged into iPad at "
                                  "some point, none within 30 days",
        "no_ipad_user_ever": "no org_user has a non-null last_ipad_login_at"},
    "source": SRC_PG}

# --- Mixpanel side -------------------------------------------------------
def read_csv(name):
    with open(os.path.join(OUT, name)) as fh:
        return list(csv.DictReader(fh))


SRC_BQ = ("BigQuery supercat-data-pipeline via local service account; "
          "queries in scripts/p2_bq_usage.py + p2_bq_offline.py; "
          "raw outputs in out/*.csv")

catalog = read_csv("mp_event_catalog.csv")
out["mixpanel_event_catalog"] = {
    "events": [{k: (int(v) if k in ("events", "orgs", "users") else v)
                for k, v in r.items()} for r in catalog],
    "distinct_events": len(catalog), "source": SRC_BQ}

usage_rows = read_csv("mp_org_feature_usage.csv")
feature_cols = [c for c in usage_rows[0]
                if c not in ("org_shortname", "org_name", "hubspot_company_id",
                             "total_users", "active_users", "total_logins",
                             "total_events")]
feature_reach = []
for c in feature_cols:
    n = sum(1 for r in usage_rows if r[c] and int(r[c]) > 0)
    feature_reach.append({"feature": c, "orgs_with_any_use": n,
                          "orgs_with_zero": len(usage_rows) - n,
                          "total_events": sum(int(r[c] or 0) for r in usage_rows)})
feature_reach.sort(key=lambda x: x["orgs_with_any_use"])

# The prebuilt view has two defects, verified in out/ (p2_bq_stackcheck.py).
# Correct them rather than publishing the view's zeros as findings.
VIEW_CORRECTIONS = {
    "create_my_list": (129, 15927, "view filters create_stack on "
                       "type='my_list'; the column actually holds 'user'"),
    "create_customer_product_list": (101, 4194, "view filters on "
                                     "type='customer_product_list'; actual "
                                     "value is 'customer'"),
    "create_maybe_list": (72, 453, "view filters on type='maybe_list'; actual "
                          "value is 'maybe'"),
}
for f in feature_reach:
    if f["feature"] in VIEW_CORRECTIONS:
        orgs, events, why = VIEW_CORRECTIONS[f["feature"]]
        f["view_reported_orgs"] = f["orgs_with_any_use"]
        f["view_reported_events"] = f["total_events"]
        f["orgs_with_any_use"] = orgs
        f["total_events"] = events
        f["orgs_with_zero"] = len(usage_rows) - orgs
        f["correction"] = why
feature_reach.sort(key=lambda x: x["orgs_with_any_use"])

out["mixpanel_feature_reach"] = {
    "features": feature_reach, "orgs_in_view": len(usage_rows),
    "view_defects": [
        "create_my_list / create_customer_product_list / create_maybe_list all "
        "returned exactly 0 orgs because the view discriminates create_stack on "
        "type values ('my_list','customer_product_list','maybe_list') that do "
        "not exist; the column holds 'user','customer','maybe'. Corrected "
        "above from the raw event table.",
        "view_cust_product_list and view_cust_backorders are both defined as "
        "COUNTIF(event_name='view_customer_on_order_items'). They are one "
        "event counted twice, not two independently measured features.",
    ],
    "source": SRC_BQ + " (view mixpanel.org_feature_usage_report, corrected "
                       "against WELD_RAW.mixpanel__events)"}

# --- coverage reconciliation: Postgres 255 vs Mixpanel 192 ---------------
mp_orgs = {r["org_shortname"] for r in usage_rows if r["org_shortname"]}
pg_shorts = set(by_short)
out["coverage"] = {
    "orgs_in_postgres": len(pg_shorts),
    "orgs_in_mixpanel": len(mp_orgs),
    "in_both": len(pg_shorts & mp_orgs),
    "postgres_only": sorted(pg_shorts - mp_orgs),
    "mixpanel_only": sorted(mp_orgs - pg_shorts),
    "postgres_only_with_ipad_active_30d": sorted(
        s for s in pg_shorts - mp_orgs if by_short[s]["ipad_active_30d"] > 0),
    "interpretation": "Tenants present in Postgres but absent from Mixpanel "
                      "emitted no telemetry in the window. For those, feature "
                      "usage is UNKNOWN, not zero.",
    "source": SRC_PG + " | " + SRC_BQ}

# --- config surface ------------------------------------------------------
dead_bools = [k for k, v in raw.BOOLEAN_FLAG_TRUE_COUNTS.items() if v == 0]
near_dead = {k: v for k, v in raw.BOOLEAN_FLAG_TRUE_COUNTS.items()
             if 0 < v <= 20}
never_true = [k for k, (_, t, _) in raw.JSON_FLAGS.items() if t == 0]
never_false = [k for k, (_, _, f) in raw.JSON_FLAGS.items() if f == 0]
out["configuration"] = {
    "boolean_columns": len(raw.BOOLEAN_FLAG_TRUE_COUNTS),
    "json_flag_keys": len(raw.JSON_FLAGS),
    "json_property_keys": raw.SCALARS["json_property_keys"],
    "total_flag_surface": len(raw.BOOLEAN_FLAG_TRUE_COUNTS) + len(raw.JSON_FLAGS),
    "distinct_actual_boolean_configs": raw.SCALARS["distinct_boolean_flag_configs"],
    "orgs_total": TOTAL_ORGS,
    "boolean_true_counts": raw.BOOLEAN_FLAG_TRUE_COUNTS,
    "json_flags": {k: {"orgs_with_key": a, "true": b, "false": c}
                   for k, (a, b, c) in raw.JSON_FLAGS.items()},
    "permanently_false_boolean_columns": dead_bools,
    "near_dead_boolean_columns_le20": near_dead,
    "json_flags_never_true": never_true,
    "json_flags_never_false": never_false,
    "source": SRC_PG}

# --- offline evidence ----------------------------------------------------
with open(os.path.join(OUT, "mp_offline_probe.json")) as fh:
    probe2 = json.load(fh)
with open(os.path.join(OUT, "mp_scalars.json")) as fh:
    mp_scalars = json.load(fh)

out["offline_evidence"] = {
    "probe_1_order_hold_postgres": {
        "measures": "orders.created_at - orders.submit_date, iPad-sourced "
                    "orders created in the trailing 12 months",
        "buckets": raw.HOLD_GAP_IPAD,
        "server_sourced_control": raw.HOLD_GAP_SERVER,
        "blind_spot": "Cannot see time spent BUILDING an order before submit. "
                      "A rep who composes offline for two days and submits on "
                      "reconnect registers a near-zero gap.",
        "source": SRC_PG},
    "probe_2_event_queue_bigquery": {
        "measures": "mp_api_timestamp_ms - time per event, corrected for a "
                    "constant US/Eastern project-clock offset by subtracting "
                    "each calendar date's minimum observed offset",
        "buckets": probe2["queue_delay_buckets"],
        "per_device_peak": probe2["device_max_gap"],
        "order_submitted_only": probe2["order_submitted_delay"],
        "artifact_found_and_corrected": "First run placed 100% of events in a "
            "single 1h-24h bucket with an exact 4.00/5.00 hour floor per event "
            "name. That is a fixed timezone offset, not queueing. See "
            "out/bq_delay_check.txt.",
        "blind_spot": "Mixpanel's on-device queue is bounded, so very long "
                      "disconnections may be truncated or dropped. These are "
                      "LOWER bounds.",
        "source": SRC_BQ},
    "probe_3_configured_policy": {
        "measures": "organizations.properties->force_sync_threshold_days, the "
                    "tenant-configured ceiling on disconnected operation, and "
                    "the require_online_order_submission flag",
        "force_sync_threshold_days": raw.FORCE_SYNC_THRESHOLD_DAYS,
        "require_online_order_submission": {
            "orgs_with_key": raw.JSON_FLAGS["require_online_order_submission"][0],
            "true": raw.JSON_FLAGS["require_online_order_submission"][1],
            "false": raw.JSON_FLAGS["require_online_order_submission"][2]},
        "disable_sync_true": raw.SCALARS["disable_sync_true"],
        "source": SRC_PG},
    "probe_4_connectivity_flag": {
        "measures": "mixpanel events wifi boolean, trailing 12 months",
        "buckets": mp_scalars["wifi_flag"],
        "caveat": "wifi=false means not on wifi, which includes cellular. It "
                  "is not equivalent to disconnected.",
        "source": SRC_BQ},
    "what_no_source_can_answer": [
        "Count of orders built and abandoned on-device without submission - "
        "drafts never leave the iPad, so the server has no row.",
        "Duration of a selling session between syncs - no session-boundary "
        "event exists in either telemetry source.",
        "Whether a disconnection was involuntary (no signal) or voluntary "
        "(airplane mode / app closed)."]}

out["screen_geometry"] = {"per_geometry": mp_scalars["screen_geometry"],
                          "source": SRC_BQ}

fleet = read_csv("mp_device_fleet.csv")
by_major = {}
for r in fleet:
    by_major[r["os_major"]] = by_major.get(r["os_major"], 0) + int(r["devices"])
out["device_fleet"] = {
    "distinct_model_os_combinations": len(fleet),
    "devices_total": sum(int(r["devices"]) for r in fleet),
    "devices_by_os_major": dict(sorted(by_major.items(),
                                       key=lambda kv: -kv[1])),
    "detail_csv": "out/mp_device_fleet.csv",
    "source": SRC_BQ}

out["user_fleet"] = {k: raw.SCALARS[k] for k in (
    "org_users_total", "org_users_disabled", "org_users_ever_ipad_login",
    "org_users_ever_eol_login", "org_users_ipad_login_le_3d",
    "org_users_ipad_login_le_7d", "org_users_ipad_login_le_30d",
    "org_users_ipad_login_le_180d", "orgs_ipad_active_30d")}
out["user_fleet"]["source"] = SRC_PG
out["mixpanel_window"] = dict(mp_scalars["window"], source=SRC_BQ)
out["sync_entity_types"] = {"entities": raw.SYNC_ENTITY_TYPES,
                            "count": len(raw.SYNC_ENTITY_TYPES),
                            "source": SRC_PG + " (table data_versions)"}
out["order_source_12mo"] = {"buckets": raw.ORDER_SOURCE_12MO, "source": SRC_PG}

with open(DEST, "w") as fh:
    json.dump(out, fh, indent=2, default=str)

# --- console summary for the writeup ------------------------------------
print(f"orgs PG={len(pg_shorts)} MP={len(mp_orgs)} both={len(pg_shorts & mp_orgs)}")
print("activity:", {k: len(v) for k, v in buckets.items()})
print("\nscale distributions (nonzero orgs | min/median/p90/max):")
for name, _ in METRICS:
    d = out["distributions"][name]
    print(f"  {name:<26} {d['orgs_with_nonzero']:>4} | {d['min']:>7} "
          f"{d['median']:>9} {d['p90']:>10} {d['max']:>9}")
print("\nlowest-reach features (of 192 telemetry orgs):")
for f in feature_reach[:14]:
    print(f"  {f['feature']:<34} orgs={f['orgs_with_any_use']:>4} "
          f"events={f['total_events']}")
print("\ndead boolean columns:", dead_bools)
print("json flags never true:", never_true)
print(f"\nwrote {DEST}")
