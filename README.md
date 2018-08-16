# Estimated Charges metric for GCP

## General
As some of you might already know, DoiT International is the engineering power behind [reOptimize](http://www.reoptimize.io/) — Cost Discovery and Optimization SaaS for Google Cloud Platform.
With [reOptimize](http://www.reoptimize.io/) you can get instant insights on your Google Cloud Platform billing, manage budgets, set up cost allocations and explore different cost optimization strategies.

While [reOptimize](http://www.reoptimize.io/) gives you the full view and the ability to slice and dice the costs, sometimes all you need is a simple tool to show your expences over time.

Here come the Estimated Charges metric to the rescue.

"Estimated Charges" metric takes the billing data [exported](https://cloud.google.com/billing/docs/how-to/export-data-bigquery) to [BigQuery](https://cloud.google.com/bigquery) by Google and load it as a metric to [StackDriver](https://cloud.google.com/stackdriver/).
 This is done per service so you can see how much each of the services cost per hour.
The metric is build using a scheduled job running on [app engine](https://cloud.google.com/appengine/) Standard environment.

## Setup
[![Open in Cloud Shell][shell_img]][shell_link]

[shell_img]: http://gstatic.com/cloudssh/images/open-btn.png
[shell_link]: https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/doitintl/estimated_charges&page=editor&open_in_editor=README.md

Make sure you have the [Google Cloud SDK](https://cloud.google.com/sdk/) installed. You'll need this to test and deploy your App Engine app.

### Export Billing Data to BigQuery
Follow the instructions described in the [Export Billing Data to BigQuery](https://cloud.google.com/billing/docs/how-to/export-data-bigquery) document 

### Install dependencies
Before running or deploying this application, install the dependencies using [pip](http://pip.readthedocs.io/en/stable/):
```
mkdir lib
pip install -t lib/ -r requirements.txt
```

### Setting up some parameters
Before deploying the service you will need to set some values in the app.yaml file.
* `PROJECT_ID`: "YOUR_PROJECT_ID" as written in the [Project Settings](https://console.cloud.google.com/iam-admin/settings/project?project=yoram-playground). This is the project in which you would like to see the metric
* `GCP_MONTH_BILLING_TABLE`: Source Table id for the BigQuery table in format: project_id.dataset_name.table_name. The source table may sit in a different project then the one creating and showing the metric.

### Running the app locally
```
dev_appserver.py .
```
    
### Deploy the app
To deploy your version into your project run:
```
gcloud app deploy app.yaml cron.yaml
```

### Setting up a report on stackdriver's metrics-explorer
* Go to [stackdriver's metrics-explorer](https://app.google.stackdriver.com/metrics-explorer) page
* Enter estimated_charges for metric type
