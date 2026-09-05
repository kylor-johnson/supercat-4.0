"""Thin BigQuery helper for Phase 2.5 (Mixpanel tenant/feature usage).

The Postgres MCP endpoint is remote and credential-less from this machine, so
Phase 2.1-2.4 had to round-trip through MCP. BigQuery is different: the service
account key is on disk, so we query directly and write straight to files. That
keeps the full per-tenant tables out of the agent transcript.
"""
import os
import sys

from google.cloud import bigquery
from google.oauth2 import service_account

KEY = ("/Users/kylorjohnson/Library/Mobile Documents/com~apple~CloudDocs/"
       "SuperCat 4.0/integrations/bigquery/service-account/"
       "supercat-data-pipeline-ac0671b8d44a.json")
PROJECT = "supercat-data-pipeline"

_creds = service_account.Credentials.from_service_account_file(KEY)
CLIENT = bigquery.Client(credentials=_creds, project=PROJECT, location="US")


def q(sql):
    return [dict(r) for r in CLIENT.query(sql).result()]


if __name__ == "__main__":
    # Discovery mode: enumerate datasets and tables with row counts so we know
    # what the Mixpanel export actually looks like before writing real queries.
    out = []
    for ds in CLIENT.list_datasets():
        dsid = ds.dataset_id
        try:
            tables = list(CLIENT.list_tables(dsid))
        except Exception as e:  # noqa: BLE001 - report, don't guess
            out.append(f"{dsid}\tLIST_FAILED\t{e}")
            continue
        out.append(f"=== dataset {dsid} ({len(tables)} tables)")
        for t in tables:
            full = CLIENT.get_table(t.reference)
            out.append(f"  {t.table_id}\trows={full.num_rows}\t"
                       f"cols={len(full.schema)}\ttype={full.table_type}")
    print("\n".join(out))
