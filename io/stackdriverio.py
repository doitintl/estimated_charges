
class StackDriverWriter:

    @staticmethod
    def write_custom_metric(client, ts_list, project_name):
        """

        :param client:
        :param ts_list: list of time series objects
        :param project_name:
        :return:
        """
        for ts in ts_list:
            client.create_time_series(project_name, [ts])
