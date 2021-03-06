from google.cloud import bigquery

QUERY = """SELECT
				service.description AS service,
				SUM(cost + IFNULL((
					SELECT
						SUM(IF(credit.name LIKE "Committed Usage Discount%"
							OR credit.name = "Sustained Usage Discount", credit.amount, 0))
					FROM
						UNNEST(credits) AS credit), 0)) AS cost
			FROM
				`{}`
			WHERE
				cost <> 0
				AND invoice.month = FORMAT_DATE("%Y%m",CURRENT_DATE())
			GROUP BY
				service"""


def get_data_from_bq(billing_table):
	"""

	:param billing_table: The dataset and table name containing the billing data
	:return: BQ result set in dataframe format
	"""
	bq_client = bigquery.Client()
	query_job = bq_client.query(QUERY.format(billing_table))

	return query_job  # Waits for job to complete.
