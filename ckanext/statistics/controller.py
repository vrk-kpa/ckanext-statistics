import ckan.plugins.toolkit as tk
import ckan.lib.base as base

from ckan import authz

render = base.render
c = tk.c


class StatisticsController(tk.BaseController):

    def statistics_read(self):
        if authz.auth_is_loggedin_user():
            try:
                from ckanext.googleanalytics.reports import google_analytics_location_report
                location_data = google_analytics_location_report()
            except ImportError:
                location_data = {}

            return render('statistics/statistics_read.html', extra_vars={"data": location_data})

        return tk.abort(403, tk._("User must be logged in to view this page"))

    def reports_read(self):
        return render('statistics/reports_read.html', extra_vars={})
