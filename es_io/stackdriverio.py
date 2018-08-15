import os
import logging
from google.cloud import monitoring_v3


class StackDriverWriter:
	@staticmethod
	def write_custom_metric(ts_list, project_id):
		"""
		:param sd_client:
		:param ts_list: list of time series objects
		:param project_id:
		:return:
		"""
		try:
			sd_client = monitoring_v3.MetricServiceClient().from_service_account_json(
				os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
			project_name = sd_client.project_path(project_id)
			for ts in ts_list:
				sd_client.create_time_series(project_name, [ts])
		except Exception as e:
			logging.error(e)
