"""Phase 2.5 discovery: what does the Mixpanel/BigQuery side actually hold?

Uses INFORMATION_SCHEMA (one query per dataset) instead of list_tables +
get_table per table. The per-table walk was still running after 500s, which
suggests date-sharded tables; a metadata query sidesteps that entirely.
"""
import sys

from bq import CLIENT, q

lines = []
datasets = [ds.dataset_id for ds in CLIENT.list_datasets()]
lines.append(f"datasets ({len(datasets)}): {', '.join(datasets)}")

for dsid in datasets:
    lines.append(f"\n=== {dsid}")
    try:
        rows = q(f"""
            select table_name, table_type, ddl is not null as has_ddl
            from `{dsid}`.INFORMATION_SCHEMA.TABLES
            order by table_name
        """)
    except Exception as e:  # noqa: BLE001
        lines.append(f"  TABLES_QUERY_FAILED: {e}")
        continue
    lines.append(f"  {len(rows)} tables/views")
    for r in rows[:400]:
        lines.append(f"    {r['table_name']}\t{r['table_type']}")
    if len(rows) > 400:
        lines.append(f"    ... {len(rows) - 400} more")

print("\n".join(lines))
