from google.cloud import monitoring_v3
import time


class MetricCalculator:

    @staticmethod
    def calculate_custom_metric(df_results, metric_type):

        # [START write_custom_metric]

        now = time.time()

        # TODO: load all number in one run
        ts_list = []
        for row in df_results.itterows():
            row = row[1]
            if row['cost'] != 0:
                try:

                    time_series = monitoring_v3.types.TimeSeries()
                    time_series.metric.type = metric_type
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
        # [END write_custom_metric]