import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckanext.statistics.logic.get import get_all_public_datasets

import logging
log = logging.getLogger(__name__)


class StatisticsPlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    if toolkit.check_ckan_version(min_version='2.5.0'):
        plugins.implements(plugins.ITranslation, inherit=True)
    plugins.implements(plugins.IActions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_resource('fanstatic', 'statistics')

    # IRoutes

    def before_map(self, map):
        map.connect('/statistics',
                    controller='ckanext.statistics.controller:StatisticsController',
                    action='statistics_read')

        map.connect('/statistics/internal',
                    controller='ckanext.statistics.controller:StatisticsController',
                    action='reports_read')

        return map

    # IActions
    def get_actions(self):
        return {'get_all_public_datasets': get_all_public_datasets}


class PublisherActivityReportPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.ITemplateHelpers)

    try:
        from ckanext.report.interfaces import IReport
        plugins.implements(IReport)

        # IReport
        def register_reports(self):
            from reports import publisher_activity_report_info
            return [publisher_activity_report_info]
    except ImportError:
        log.warning("ckanext-report is not installed, reports are not available")
        pass

    # ITemplateHelpers
    def get_helpers(self):

        return {
            "report_match_rows": report_match_rows,
            "report_timestamps_split": report_timestamps_split
        }


def report_match_rows(rows, type_, quarter):
    return [row for row in rows if (row[3] == type_ and row[4] == quarter)]


def report_timestamps_split(timestamps):
    return [render_datetime(timestamp) for timestamp in timestamps.split(' ')]


def render_datetime(datetime_, date_format=None, with_hours=False):
    '''Render a datetime object or timestamp string as a pretty string
    (Y-m-d H:m).
    If timestamp is badly formatted, then a blank string is returned.
    This is a wrapper on the CKAN one which has an American date_format.
    '''
    if not date_format:
        date_format = '%d %b %Y'
        if with_hours:
            date_format += ' %H:%M'

    from ckan.lib.helpers import render_datetime
    return render_datetime(datetime_, date_format)
