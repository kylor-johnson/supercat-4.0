#!/usr/bin/env python3
"""Phase 5: name the tenants behind each low-reach feature.

The kill list must name tenants, not count them. This pulls per-org event
counts for the lowest-reach features straight from Mixpanel and writes
scripts/kill_named.json.
"""
import json
import os

from bq import q

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = "`supercat-data-pipeline.WELD_RAW.mixpanel__events`"

# The features that drive Phase 5, with the unit each maps to.
# Event names verified against the live catalog (out/p5_event_catalog.txt, 50
# distinct names). The Phase 2 view used different labels for several of these;
# these are the names the raw events actually carry.
FEATURES = {
    "flipbook_add_to_list": "Flipbook",
    "flipbook_add_to_order": "Flipbook",
    "view_flipbook": "Flipbook",
    "view_commitments": "Commitments",
    "smart_search_toggled": "SemanticSearch",
    "smart_search_embeddings_generated": "SemanticSearch",
    "show_on_display_setting_changed": "ShowroomCart",
    "view_customer_placements": "Placements",
    "add_kit_to_order": "Kit/Options related",
    "view_kit": "Kit/Options related",
    "add_configured_item_to_order": "Kit/Options related",
    "generate_xlsx_catalog": "Reporting and Email Generation",
    "csv_report_generated": "Reporting and Email Generation",
    "search_settings_saved": "SemanticSearch",
    "reload_button_pressed": "Sync",
    "view_notifications": "SuperCat Notices",
}

names = "', '".join(FEATURES)
SQL = f"""
with e as (
  select lower(coalesce(current_organization_shortname,
                        organization_shortname)) as org,
         event_name,
         device_id,
         cast(time as int64) as t
  from {SRC}
  where event_name in ('{names}')
    and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                           interval 365 day))
)
select event_name,
       org,
       count(*) as events,
       count(distinct device_id) as devices,
       date(timestamp_seconds(max(t))) as last_seen
from e
where org is not null
group by 1, 2
order by 1, events desc
"""

rows = q(SQL)

# what event names actually exist, so "0 orgs" is distinguishable from
# "event never instrumented"
CAT = q(f"""
select event_name, count(*) as events,
       count(distinct lower(coalesce(current_organization_shortname,
                                     organization_shortname))) as orgs
from {SRC}
where time >= unix_seconds(timestamp_sub(current_timestamp(),
                                         interval 365 day))
group by 1 order by 2 desc
""")
catalog = {r["event_name"]: r for r in CAT}

per_feature = {}
for f, unit in FEATURES.items():
    hits = [r for r in rows if r["event_name"] == f]
    per_feature[f] = {
        "unit": unit,
        "instrumented": f in catalog,
        "orgs": len(hits),
        "total_events": sum(h["events"] for h in hits),
        "tenants": [
            {"shortname": h["org"], "events": h["events"],
             "devices": h["devices"], "last_seen": str(h["last_seen"])}
            for h in hits],
    }

out = {
    "method": "BigQuery mixpanel mp_master_event, trailing 365 days, grouped "
              "by event_name and org shortname",
    "source": "scripts/p5_named.py via scripts/p2_bq.py service account",
    "event_catalog_distinct_names": len(catalog),
    "per_feature": per_feature,
}
with open(os.path.join(HERE, "kill_named.json"), "w") as fh:
    json.dump(out, fh, indent=1, default=str)

for f, v in per_feature.items():
    flag = "" if v["instrumented"] else "  [EVENT NAME NOT IN TELEMETRY]"
    print(f"\n{f}  ({v['unit']})  orgs={v['orgs']} "
          f"events={v['total_events']}{flag}")
    for t in v["tenants"]:
        print(f"    {t['shortname']:<24} events={t['events']:>7} "
              f"devices={t['devices']:>3} last_seen={t['last_seen']}")
