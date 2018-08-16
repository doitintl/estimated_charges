import time
from google.cloud import monitoring_v3

CUSTOM_METRIC_DOMAIN = "custom.googleapis.com"
METRIC_NAME = "estimated_charges"
METRIC_TYPE = "{}/{}".format(CUSTOM_METRIC_DOMAIN, METRIC_NAME)

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


class MetricCalculator:
	@staticmethod
	def init_custom_metric(project_id):
		client = monitoring_v3.MetricServiceClient()
		project_name = client.project_path(project_id)

		try:
			metric_descriptors = client.get_metric_descriptor(
				"{}/metricDescriptors/{}".format(project_name, metric_descriptor["type"]))
			print("Found: {}".format(metric_descriptors))
		except:
			client.create_metric_descriptor(project_name, metric_descriptor)
			print("Create: {}/metricDescriptors/{}".format(project_name, metric_descriptor["type"]))

	@staticmethod
	def calculate_custom_metric(result):
		now = time.time()

		# TODO: load all number in one run
		ts_list = []
		for row in result:
			try:
				if row['cost'] != 0:
					time_series = monitoring_v3.types.TimeSeries()
					time_series.metric.type = METRIC_TYPE
					time_series.metric.labels['service'] = row['service']
					point = time_series.points.add()
					point.value.double_value = row['cost']
					point.interval.end_time.seconds = int(now)
					point.interval.end_time.nanos = int(
						(now - point.interval.end_time.seconds) * 10 ** 9)
					ts_list.append(time_series)
			except:
				continue

		return ts_list
