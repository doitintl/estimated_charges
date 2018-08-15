import os
import logging
from flask import Flask
from es_io.bigqueryio import get_data_from_bq
from es_io.stackdriverio import StackDriverWriter
from metrics.metrics import MetricCalculator

app = Flask(__name__)
project_id = os.getenv("PROJECT_ID")

# TODO: Add cron


def init():
    # [START init]
    MetricCalculator.init_custom_metric(project_id=project_id)
    # [END init]


@app.route('/', methods=['GET'])
def query_costs():
    # [START query_costs]
    df_result = get_data_from_bq(project_id=project_id, billing_table=os.getenv("GCP_MONTH_BILLING_TABLE"))
    ts_list = MetricCalculator.calculate_custom_metric(df_results=df_result)
    StackDriverWriter.write_custom_metric(ts_list=ts_list, project_id=project_id)
    return ""
    # [END query_costs]


if __name__ == "__main__":
    try:
        init()
        app.run()
        # app.run(debug=False)
    except Exception as e:
        logging.error(e)
