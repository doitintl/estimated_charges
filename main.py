import os
import time
from google.cloud import bigquery
from google.cloud import monitoring_v3
from flask import Flask

app = Flask(__name__)
project_id = os.getenv("PROJECT_ID")

# TODO: credits.amount

CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"
METRIC_TYPE = "{}/{}".format(CUSTOM_METRIC_DOMAIN, os.getenv("METRIC_NAME"))
QUERY_TEMPLATE = os.getenv("QUERY_TEMPLATE")
QUERY = QUERY_TEMPLATE.format(project_id, os.getenv("GCP_MONTH_BILLING_TABLE"))

metric_descriptor = {
    "description": "Recent cost",
    "metric_kind": monitoring_v3.enums.MetricDescriptor.MetricKind.GAUGE,
    "name": "cost",
    "value_type": monitoring_v3.enums.MetricDescriptor.ValueType.DOUBLE,
    "type": METRIC_TYPE,
    "labels": [
        {
            "key": "Service",
            "description": "Service in use"
        }
    ]
}


def write_custom_metric(results):
    # [START write_custom_metric]
    client = monitoring_v3.MetricServiceClient().from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    project_name = client.project_path(project_id)
    now = time.time()

    # TODO: load all number in one run
    for row in results:
        if row['cost'] != 0:
            time_series = monitoring_v3.types.TimeSeries()
            time_series.metric.type = METRIC_TYPE
            time_series.metric.labels['service'] = row['service']
            point = time_series.points.add()
            point.value.double_value = row['cost']
            point.interval.end_time.seconds = int(now)
            point.interval.end_time.nanos = int(
                (now - point.interval.end_time.seconds) * 10 ** 9)
            client.create_time_series(project_name, [time_series])

    # [END write_custom_metric]


def get_data_from_bq():
    # [START get_data_from_bq]
    bq_client = bigquery.Client().from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    query_job = bq_client.query(QUERY)
    results = query_job.result()  # Waits for job to complete.

    return results
    # [END get_data_from_bq]


def init():
    # [START init]
    client = monitoring_v3.MetricServiceClient().from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    project_name = client.project_path(project_id)

    try:
        metric_descriptors = client.get_metric_descriptor("{}/metricDescriptors/{}".format(project_name, metric_descriptor["type"]))
        print("Found: {}".format(metric_descriptors))
    except:
        client.create_metric_descriptor(project_name, metric_descriptor)
        print("Create: {}/metricDescriptors/{}".format(project_name, metric_descriptor["type"]))
    # [END init]


init()


@app.route('/', methods=['GET'])
def query_costs():
    # [START query_costs]
    results = get_data_from_bq()
    write_custom_metric(results)
    return ""
    # [END query_costs]


if __name__ == "__main__":
    app.run()
#    app.run(debug=False)
