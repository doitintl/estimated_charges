import os
import logging
from flask import Flask
from es_io.bigqueryio import get_data_from_bq
from es_io.stackdriverio import StackDriverWriter
from metrics.metrics import MetricCalculator

app = Flask(__name__)
project_id = os.getenv("PROJECT_ID")
BILLING_TABLE = os.getenv("GCP_BILLING_TABLE")


def init():
    # [START init]
    MetricCalculator.init_custom_metric(project_id=project_id)
    # [END init]


@app.route('/', methods=['GET'])
def default():
    # [START default]
    return "Looks like you are in the wrong place..."
    # [END default]


@app.route('/estimated_charges', methods=['GET'])
def query_costs():
    # [START query_costs]
    result = get_data_from_bq(BILLING_TABLE)
    ts_list = MetricCalculator.calculate_custom_metric(result=result)
    StackDriverWriter.write_custom_metric(ts_list=ts_list, project_id=project_id)
    return ""
    # [END query_costs]


if __name__ == "__main__":
    try:
        init()
        app.run()
        # app.run(debug=False)
    except Exception as e:
        logging.error(e.with_traceback())
