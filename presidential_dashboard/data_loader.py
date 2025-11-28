from google.cloud import bigquery, secretmanager
import pandas as pd
import os
import json
import tempfile

def load_data():
    # Fetch secret (service account key) from Google Cloud Secret Manager
    secret_client = secretmanager.SecretManagerServiceClient()
    project_id = "dashboard-254616"
    secret_id = "STREAMLIT_DASHBOARD_KEY"
    secret_version = "latest"
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{secret_version}"

    response = secret_client.access_secret_version(request={"name": secret_name})
    dashboard_key = response.payload.data.decode("UTF-8")

    # Write the service account JSON to a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as tmp:
        tmp.write(dashboard_key)
        tmp.flush()
        key_path = tmp.name

    # Set environment variable for credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    query = """
        SELECT * FROM `dashboard-254616.donations.donations_time_period_with_prov`
    """
    results = client.query(query).to_dataframe()
    return results