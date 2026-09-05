"""Phase 2.5 (feature usage per tenant) + Phase 2.6 probe 2 (offline evidence).

Writes CSV/JSON to out/ rather than returning through the agent context, so the
full per-tenant tables survive at full fidelity.

Probe 2 rationale: the Mixpanel iOS SDK queues events on-device and flushes when
it can reach the network. `time` is stamped by the client when the event occurs;
`mp_api_timestamp_ms` is stamped by Mixpanel's ingest on receipt. Their
difference is time the device spent unable to deliver -- a direct measurement of
disconnected operation, and independent of the orders-table probe, which can
only see submit -> arrival.
"""
import csv
import json
import os

from bq import q

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
os.makedirs(OUT, exist_ok=True)
SRC = "`supercat-data-pipeline.WELD_RAW.mixpanel__events`"
result = {}


def write_csv(name, rows):
    if not rows:
        return
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"wrote {name}: {len(rows)} rows")


# --- window and volume ---------------------------------------------------
result["window"] = q(f"""
    select count(*) as events,
           count(distinct lower(coalesce(current_organization_shortname,
                                         organization_shortname))) as orgs,
           count(distinct lower(username)) as usernames,
           count(distinct device_id) as devices,
           date(timestamp_seconds(cast(min(time) as int64))) as first_event,
           date(timestamp_seconds(cast(max(time) as int64))) as last_event
    from {SRC}
""")[0]

# --- event catalog: every distinct event, its reach ----------------------
events = q(f"""
    select event_name,
           count(*) as events,
           count(distinct lower(coalesce(current_organization_shortname,
                                         organization_shortname))) as orgs,
           count(distinct lower(username)) as users,
           date(timestamp_seconds(cast(min(time) as int64))) as first_seen,
           date(timestamp_seconds(cast(max(time) as int64))) as last_seen
    from {SRC}
    group by 1 order by 3 desc, 2 desc
""")
write_csv("mp_event_catalog.csv", events)
result["event_catalog_count"] = len(events)

# --- per-org feature usage (the prebuilt 38-feature view) ----------------
usage = q("select * from `supercat-data-pipeline.mixpanel.org_feature_usage_report`")
write_csv("mp_org_feature_usage.csv", usage)
result["orgs_in_feature_view"] = len(usage)

# --- per-org x per-event matrix, last 12 months --------------------------
matrix = q(f"""
    select lower(coalesce(current_organization_shortname,
                          organization_shortname)) as org,
           event_name, count(*) as n,
           count(distinct lower(username)) as users
    from {SRC}
    where time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
      and coalesce(current_organization_shortname,
                   organization_shortname) is not null
    group by 1, 2
""")
write_csv("mp_org_event_matrix_12mo.csv", matrix)
result["org_event_pairs_12mo"] = len(matrix)

# --- Phase 2.6 probe 2: client-to-ingest delivery delay ------------------
result["delivery_delay"] = q(f"""
    with e as (
      select lower(coalesce(current_organization_shortname,
                            organization_shortname)) as org,
             (mp_api_timestamp_ms/1000.0) - time as delay_s
      from {SRC}
      where mp_api_timestamp_ms is not null and time is not null
        and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                               interval 365 day))
    )
    select count(*) as n,
           count(distinct org) as orgs,
           countif(delay_s < 0) as negative,
           countif(delay_s between 0 and 300) as le_5min,
           countif(delay_s > 300 and delay_s <= 3600) as m5_to_1h,
           countif(delay_s > 3600 and delay_s <= 86400) as h1_to_24h,
           countif(delay_s > 86400 and delay_s <= 259200) as d1_to_3d,
           countif(delay_s > 259200 and delay_s <= 604800) as d3_to_7d,
           countif(delay_s > 604800 and delay_s <= 2592000) as d7_to_30d,
           countif(delay_s > 2592000) as gt_30d
    from e
""")[0]

# per-org version of the same probe: which tenants actually run disconnected
write_csv("mp_delivery_delay_by_org.csv", q(f"""
    with e as (
      select lower(coalesce(current_organization_shortname,
                            organization_shortname)) as org,
             (mp_api_timestamp_ms/1000.0) - time as delay_s
      from {SRC}
      where mp_api_timestamp_ms is not null and time is not null
        and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                               interval 365 day))
        and coalesce(current_organization_shortname,
                     organization_shortname) is not null
    )
    select org, count(*) as n,
           countif(delay_s > 300) as gt_5min,
           countif(delay_s > 3600) as gt_1h,
           countif(delay_s > 86400) as gt_24h,
           countif(delay_s > 259200) as gt_3d,
           round(max(delay_s)/86400.0, 1) as max_delay_days
    from e group by 1 order by gt_24h desc
"""))

# --- probe 3: connectivity flag carried on the event ---------------------
result["wifi_flag"] = q(f"""
    select cast(wifi as string) as wifi, count(*) as events,
           count(distinct lower(coalesce(current_organization_shortname,
                                         organization_shortname))) as orgs
    from {SRC}
    where time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
    group by 1 order by 2 desc
""")

# --- device / OS fleet (constrains what a web target may assume) ---------
write_csv("mp_device_fleet.csv", q(f"""
    select coalesce(model, mp_device_model, '<null>') as model,
           coalesce(os, '<null>') as os,
           split(coalesce(os_version, '<null>'), '.')[offset(0)] as os_major,
           count(*) as events,
           count(distinct device_id) as devices,
           count(distinct lower(coalesce(current_organization_shortname,
                                         organization_shortname))) as orgs
    from {SRC}
    where time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
    group by 1, 2, 3 order by devices desc
"""))

# --- screen geometry: what the responsive target must actually cover -----
result["screen_geometry"] = q(f"""
    select cast(screen_width as int64) as w, cast(screen_height as int64) as h,
           count(distinct device_id) as devices, count(*) as events
    from {SRC}
    where screen_width is not null
      and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
    group by 1, 2 order by devices desc limit 25
""")

with open(os.path.join(OUT, "mp_scalars.json"), "w") as fh:
    json.dump(result, fh, indent=2, default=str)
print(json.dumps(result, indent=2, default=str))
