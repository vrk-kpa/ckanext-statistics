import ckan.plugins.toolkit as tk
from . import utils


class StatisticsController(tk.BaseController):

    def statistics_read(self):
        return utils.statistics_read()

    def reports_read(self):
        return utils.reports_read()
