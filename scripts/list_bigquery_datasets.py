
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

print("Listing datasets in project 'supercat-data-pipeline':")
for dataset in client.list_datasets():
    print(dataset.dataset_id)
