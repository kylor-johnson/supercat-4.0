"""Validate (or invalidate) the Mixpanel delivery-delay probe.

Every event landed in one 1h-24h bucket, which no real queueing process would
produce. Check whether the offset is a fixed constant (timezone/clock skew ->
probe is unusable) or genuinely dispersed (probe is real).
"""
from bq import q

SRC = "`supercat-data-pipeline.WELD_RAW.mixpanel__events`"

print("--- delay in hours, rounded, top 30 by frequency")
for r in q(f"""
    select round(((mp_api_timestamp_ms/1000.0) - time)/3600.0, 2) as delay_h,
           count(*) as n
    from {SRC}
    where mp_api_timestamp_ms is not null and time is not null
      and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
    group by 1 order by 2 desc limit 30
"""):
    print(f"  {r['delay_h']:>10} h  n={r['n']}")

print("\n--- is mp_processing_time_ms a better server clock?")
for r in q(f"""
    select round(((mp_processing_time_ms/1000.0) - time)/3600.0, 2) as delay_h,
           count(*) as n
    from {SRC}
    where mp_processing_time_ms is not null and time is not null
      and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
    group by 1 order by 2 desc limit 15
"""):
    print(f"  {r['delay_h']:>10} h  n={r['n']}")

print("\n--- per-event-name spread of the mp_api offset (a real queue would "
      "differ by event; a clock offset would not)")
for r in q(f"""
    select event_name,
           round(min(((mp_api_timestamp_ms/1000.0) - time))/3600.0, 2) as min_h,
           round(max(((mp_api_timestamp_ms/1000.0) - time))/3600.0, 2) as max_h,
           count(*) as n
    from {SRC}
    where mp_api_timestamp_ms is not null and time is not null
      and time >= unix_seconds(timestamp_sub(current_timestamp(),
                                             interval 365 day))
    group by 1 order by n desc limit 12
"""):
    print(f"  {r['event_name']:<34} min={r['min_h']:>8} max={r['max_h']:>8} "
          f"n={r['n']}")
