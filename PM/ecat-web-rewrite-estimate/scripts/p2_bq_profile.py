"""Phase 2.5 profiling: shape of mixpanel.events and the org mapping tables."""
from bq import q

out = []

for tbl in ("events", "organization_customer_mapping", "user_org_mapping",
            "people"):
    out.append(f"\n=== schema mixpanel.{tbl}")
    rows = q(f"""
        select column_name, data_type
        from mixpanel.INFORMATION_SCHEMA.COLUMNS
        where table_name = '{tbl}'
        order by ordinal_position
    """)
    for r in rows:
        out.append(f"  {r['column_name']}\t{r['data_type']}")

out.append("\n=== ddl of the two usage views (they encode the intended join)")
for v in ("org_feature_usage_report", "user_feature_usage_report"):
    rows = q(f"""
        select ddl from mixpanel.INFORMATION_SCHEMA.TABLES
        where table_name = '{v}'
    """)
    out.append(f"\n--- {v}\n{rows[0]['ddl'] if rows else 'NO DDL'}")

print("\n".join(out))
