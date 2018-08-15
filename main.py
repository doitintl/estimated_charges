import os
import time
from google.cloud import monitoring_v3
from flask import Flask
import logging

from io.biqeuryio import get_data_from_bq
from metrics.metrics import MetricCalculator

app = Flask(__name__)
project_id = os.getenv("PROJECT_ID")

# TODO: credits.amount

CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"
METRIC_TYPE = "{}/{}".format(CUSTOM_METRIC_DOMAIN, os.getenv("METRIC_NAME"))
QUERY_TEMPLATE = os.getenv("QUERY_TEMPLATE")
QUERY = QUERY_TEMPLATE.format(project_id, os.getenv("GCP_MONTH_BILLING_TABLE"))

default_metric_descriptor = {
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



def init():
    # [START init]
    client = monitoring_v3.MetricServiceClient().from_service_account_json(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    project_name = client.project_path(project_id)

    try:
        metric_descriptors = client.get_metric_descriptor("{}/metricDescriptors/{}".format(project_name, default_metric_descriptor["type"]))
        print("Found: {}".format(metric_descriptors))
    except:
        client.create_metric_descriptor(project_name, default_metric_descriptor)
        print("Create: {}/metricDescriptors/{}".format(project_name, default_metric_descriptor["type"]))
    # [END init]


@app.route('/', methods=['GET'])
def query_costs():
    # [START query_costs]
    df_result = get_data_from_bq(QUERY)

    client = monitoring_v3.MetricServiceClient().from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    project_name = client.project_path(project_id)

    ts_list = MetricCalculator.calculate_custom_metric(client=client,
                                                       df_results=df_result,
                                                       metric_type=METRIC_TYPE)
    MetricCalculator.calculate_custom_metric(client, ts_list, project_name)
    return ""
    # [END query_costs]


if __name__ == "__main__":

    try:
        init()
        app.run()
    except Exception as e:
        logging.error(e)
#   app.run(debug=False)
