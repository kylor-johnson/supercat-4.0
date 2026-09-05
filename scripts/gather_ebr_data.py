
import os
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, timedelta

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

DATASET = "supercat-data-pipeline.WELD_RAW"

def run_query(query):
    try:
        results = client.query(query).result()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"Error running query: {e}")
        return []

def get_helpscout_data():
    print("Querying Help Scout...")
    query = f"""
    SELECT 
        ticket_status,
        ticket_subject,
        conv_customer_organization,
        ticket_created_at
    FROM `{DATASET}.helpscout__help_scout_tickets`
    WHERE (LOWER(conv_customer_organization) LIKE '%gabby%' 
       OR LOWER(conv_customer_organization) LIKE '%summer classic%'
       OR LOWER(conv_customer_organization) LIKE '%gabriella white%')
      AND ticket_created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
    ORDER BY ticket_created_at DESC
    LIMIT 1000
    """
    return run_query(query)

def get_fathom_data():
    print("Querying Fathom...")
    query = f"""
    SELECT 
        `Meeting Title`,
        `External Domain Names`,
        `Meeting Start Time`,
        `AI Summary Plaintext Formatted`
    FROM `{DATASET}.fathom__ai_summaries`
    WHERE (LOWER(`Meeting Title`) LIKE '%gabby%' 
       OR LOWER(`Meeting Title`) LIKE '%summer classic%'
       OR LOWER(`Meeting Title`) LIKE '%gabriella white%'
       OR LOWER(`External Domain Names`) LIKE '%gabby%'
       OR LOWER(`External Domain Names`) LIKE '%summerclassic%'
       OR LOWER(`External Domain Names`) LIKE '%gabriellawhite%')
      AND `Meeting Start Time` >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
    ORDER BY `Meeting Start Time` DESC
    LIMIT 50
    """
    return run_query(query)

def get_mixpanel_data():
    print("Querying Mixpanel...")
    # Get monthly active users and event counts per brand
    query = f"""
    SELECT 
        organization_shortname,
        FORMAT_TIMESTAMP('%Y-%m', _weld_synced) as month,
        COUNT(*) as event_count,
        COUNT(DISTINCT username) as active_users
    FROM `{DATASET}.mixpanel__events`
    WHERE organization_shortname IN ('gh', 'scw', 'sccon', 'sc')
      AND _weld_synced >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 365 DAY)
    GROUP BY organization_shortname, month
    ORDER BY organization_shortname, month
    """
    return run_query(query)

def main():
    data = {
        "helpscout": get_helpscout_data(),
        "fathom": get_fathom_data(),
        "mixpanel": get_mixpanel_data()
    }
    
    # Custom serializer for datetime objects
    def default(o):
        if isinstance(o, (datetime, datetime.date)):
            return o.isoformat()
        raise TypeError(f"Type {type(o)} not serializable")

    with open("scripts/ebr_data_output.json", "w") as f:
        json.dump(data, f, indent=2, default=default)
    
    print("Data saved to scripts/ebr_data_output.json")

if __name__ == "__main__":
    main()
