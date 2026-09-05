"""Phase 2.6 probe 2, corrected: on-device event queue delay.

First attempt put 100% of events in one 1h-24h bucket. Diagnosis (see
out/bq_delay_check.txt): mixpanel `time` is stamped in the project's US/Eastern
local time while `mp_api_timestamp_ms` is UTC, so every delay carries a constant
+4h (EDT) or +5h (EST) offset. The floor is exactly 4.00 / 5.00 for every event
name, which is what a fixed clock offset looks like and what a queue does not.

Correction: for each calendar date, the minimum observed offset IS that date's
timezone offset. Subtracting it per date removes the artifact and leaves the
real on-device queue delay, without hardcoding a DST calendar.

Remaining limitation, stated not patched: the Mixpanel SDK caps its local queue,
so long disconnections can be truncated or dropped. Every number here is a LOWER
bound on disconnected duration.
"""
import csv
import json
import os

from bq import q

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
SRC = "`supercat-data-pipeline.WELD_RAW.mixpanel__events`"

BASE = f"""
  with raw as (
    select lower(coalesce(current_organization_shortname,
                          organization_shortname)) as org,
           event_name, device_id,
           date(timestamp_seconds(cast(time as int64))) as d,
           (mp_api_timestamp_ms/1000.0) - time as raw_delay_s
    from {SRC}
    where mp_api_timestamp_ms is not null and time is not null
      and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
  ),
  offs as (select d, min(raw_delay_s) as tz_offset_s from raw group by d),
  e as (
    select r.org, r.event_name, r.device_id, r.d,
           r.raw_delay_s - o.tz_offset_s as delay_s
    from raw r join offs o using (d)
  )
"""


def write_csv(name, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if v is None else v) for k, v in r.items()})
    print(f"wrote {name}: {len(rows)} rows")


res = {}

res["queue_delay_buckets"] = q(BASE + """
    select count(*) as n, count(distinct org) as orgs,
           count(distinct device_id) as devices,
           countif(delay_s <= 60) as le_1min,
           countif(delay_s > 60 and delay_s <= 300) as m1_to_5min,
           countif(delay_s > 300 and delay_s <= 3600) as m5_to_1h,
           countif(delay_s > 3600 and delay_s <= 14400) as h1_to_4h,
           countif(delay_s > 14400 and delay_s <= 86400) as h4_to_24h,
           countif(delay_s > 86400 and delay_s <= 259200) as d1_to_3d,
           countif(delay_s > 259200 and delay_s <= 604800) as d3_to_7d,
           countif(delay_s > 604800) as gt_7d,
           round(max(delay_s)/86400.0, 2) as max_delay_days
    from e
""")[0]

# Per device: the longest single disconnected stretch we can observe.
res["device_max_gap"] = q(BASE + """
    , per_device as (
      select device_id, org, max(delay_s) as max_delay_s
      from e where device_id is not null group by 1, 2
    )
    select count(*) as devices,
           countif(max_delay_s <= 300) as never_exceeded_5min,
           countif(max_delay_s > 300 and max_delay_s <= 3600) as peak_5min_1h,
           countif(max_delay_s > 3600 and max_delay_s <= 86400) as peak_1h_24h,
           countif(max_delay_s > 86400 and max_delay_s <= 259200) as peak_1d_3d,
           countif(max_delay_s > 259200) as peak_gt_3d
    from per_device
""")[0]

write_csv("mp_queue_delay_by_org.csv", q(BASE + """
    select org, count(*) as n, count(distinct device_id) as devices,
           countif(delay_s > 300) as gt_5min,
           countif(delay_s > 3600) as gt_1h,
           countif(delay_s > 86400) as gt_24h,
           countif(delay_s > 259200) as gt_3d,
           round(max(delay_s)/86400.0, 2) as max_delay_days
    from e where org is not null group by 1 order by gt_24h desc
"""))

# Does order_submitted specifically get held? That is the revenue-bearing path.
res["order_submitted_delay"] = q(BASE + """
    select count(*) as n, count(distinct org) as orgs,
           countif(delay_s <= 300) as le_5min,
           countif(delay_s > 300 and delay_s <= 3600) as m5_to_1h,
           countif(delay_s > 3600 and delay_s <= 86400) as h1_to_24h,
           countif(delay_s > 86400) as gt_24h,
           round(max(delay_s)/86400.0, 2) as max_delay_days
    from e where event_name = 'order_submitted'
""")[0]

with open(os.path.join(OUT, "mp_offline_probe.json"), "w") as fh:
    json.dump(res, fh, indent=2, default=str)
print(json.dumps(res, indent=2, default=str))
