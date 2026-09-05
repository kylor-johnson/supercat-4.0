#!/usr/bin/env python3
"""
Query the most recent Help Scout tickets from BigQuery
"""

import os
from google.cloud import bigquery
from google.oauth2 import service_account

# Service account path
SERVICE_ACCOUNT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "integrations/bigquery/service-account/supercat-data-pipeline-dbfab43c27bb.json"
)

# Create credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH,
    scopes=["https://www.googleapis.com/auth/bigquery"]
)

# Create BigQuery client
client = bigquery.Client(credentials=credentials, project="supercat-data-pipeline")

# Query for most recent Help Scout tickets
query = """
SELECT DISTINCT
  conversation_id,
  ticket_number,
  ticket_subject,
  ticket_status,
  ticket_preview,
  conv_customer_organization,
  conv_customer_email,
  agent_name,
  ticket_created_at,
  thread_count,
  (SELECT STRING_AGG(tag.tag_name, ', ')
   FROM UNNEST(ticket_tags) as tag) as all_tags
FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
ORDER BY ticket_created_at DESC
LIMIT 25
"""

print("Querying BigQuery for most recent Help Scout tickets...\n")
print("=" * 80)

try:
    results = client.query(query).result()
    
    for row in results:
        print(f"\n📧 Ticket #{row.ticket_number}")
        print(f"   Subject: {row.ticket_subject}")
        print(f"   Status: {row.ticket_status}")
        print(f"   Customer: {row.conv_customer_organization or row.conv_customer_email or 'Unknown'}")
        print(f"   Agent: {row.agent_name or 'Unassigned'}")
        print(f"   Created: {row.ticket_created_at}")
        print(f"   Threads: {row.thread_count}")
        if row.all_tags:
            print(f"   Tags: {row.all_tags}")
        if row.ticket_preview:
            preview = row.ticket_preview[:150] + "..." if len(row.ticket_preview) > 150 else row.ticket_preview
            print(f"   Preview: {preview}")
        print("-" * 80)
    
    print(f"\n✅ Retrieved {results.total_rows} most recent tickets")
    
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}")
