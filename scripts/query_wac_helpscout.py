#!/usr/bin/env python3
"""
Query WAC-specific Help Scout tickets from BigQuery
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

# Query for WAC Help Scout tickets
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
WHERE LOWER(conv_customer_organization) LIKE '%wac%'
   OR LOWER(conv_customer_organization) LIKE '%modern forms%'
ORDER BY ticket_created_at DESC
LIMIT 50
"""

print("Querying BigQuery for WAC/Modern Forms Help Scout tickets...\n")
print("=" * 80)

try:
    results = client.query(query).result()
    
    # Count by status
    status_counts = {}
    q4_count = 0
    all_time_count = 0
    
    tickets = []
    for row in results:
        tickets.append(row)
        all_time_count += 1
        
        # Count Q4 2025 tickets (Oct 1 - Dec 31, 2025)
        if row.ticket_created_at and row.ticket_created_at.year == 2025 and row.ticket_created_at.month >= 10:
            q4_count += 1
        
        # Count by status
        status = row.ticket_status or 'unknown'
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Print summary
    print(f"\n📊 WAC/Modern Forms Support Ticket Summary")
    print(f"   Total Tickets Found: {all_time_count}")
    print(f"   Q4 2025 Tickets (Oct-Dec): {q4_count}")
    print(f"\n   Status Breakdown:")
    for status, count in sorted(status_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"      {status}: {count}")
    
    print(f"\n" + "=" * 80)
    print(f"\n📋 Recent Tickets:\n")
    
    # Print individual tickets
    for i, row in enumerate(tickets[:20], 1):  # Show first 20
        print(f"\n{i}. 📧 Ticket #{row.ticket_number}")
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
    
    if len(tickets) > 20:
        print(f"\n... and {len(tickets) - 20} more tickets")
    
    print(f"\n✅ Query completed successfully")
    
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}")
    import traceback
    traceback.print_exc()
