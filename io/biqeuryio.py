from google.cloud import bigquery

def get_data_from_bq(query):

    # [START get_data_from_bq]
    bq_client = bigquery.Client().from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    query_job = bq_client.query(query)

    return query_job.to_dataframe()  # Waits for job to complete.
    # [END get_data_from_bq]