
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

def find_org_names():
    print("Searching for Organization Names in Help Scout...")
    query = """
    SELECT DISTINCT conv_customer_organization
    FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets`
    WHERE LOWER(conv_customer_organization) LIKE '%gabby%' 
       OR LOWER(conv_customer_organization) LIKE '%summer classic%'
       OR LOWER(conv_customer_organization) LIKE '%gabriella white%'
    LIMIT 50
    """
    try:
        results = client.query(query).result()
        for row in results:
            print(f"Help Scout Org: {row.conv_customer_organization}")
    except Exception as e:
        print(f"Error querying Help Scout: {e}")

    print("\nSearching for External Domains in Fathom...")
    query = """
    SELECT DISTINCT `External Domain Names`
    FROM `supercat-data-pipeline.hevo_dataset_supercat_data_pipeline_Slhk.fathom__ai_summaries`
    WHERE LOWER(`External Domain Names`) LIKE '%gabby%' 
       OR LOWER(`External Domain Names`) LIKE '%summerclassic%'
       OR LOWER(`External Domain Names`) LIKE '%gabriellawhite%'
    LIMIT 50
    """
    try:
        results = client.query(query).result()
        for row in results:
            print(f"Fathom Domain: {row['External Domain Names']}")
    except Exception as e:
        print(f"Error querying Fathom: {e}")

if __name__ == "__main__":
    find_org_names()
