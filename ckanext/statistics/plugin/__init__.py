import sys
import os
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

from ckan.lib.plugins import DefaultTranslation
from ckanext.statistics.logic.get import get_all_public_datasets

from ckanext.statistics import auth
import logging
log = logging.getLogger(__name__)


if toolkit.check_ckan_version('2.9'):
    from . import flask_plugin as platform
else:
    from . import pylons_plugin as platform


class StatisticsPlugin(platform.MixinPlugin, plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    if toolkit.check_ckan_version(min_version='2.5.0'):
        plugins.implements(plugins.ITranslation, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, '../templates')
        toolkit.add_resource('../fanstatic', 'statistics')

    # IActions
    def get_actions(self):
        return {'get_all_public_datasets': get_all_public_datasets}

    # IAuthFunctions

    def get_auth_functions(self):
        return {'statistics_read': auth.statistics_read}

    # ITranslator

    # The following methods are copied from ckan.lib.plugins.DefaultTranslation
    # and have been modified to fix a bug in CKAN 2.5.1 that prevents CKAN from
    # starting. In addition by copying these methods, it is ensured that Data
    # Requests can be used even if Itranslation isn't available (less than 2.5)

    def i18n_directory(self):
        '''Change the directory of the *.mo translation files
        The default implementation assumes the plugin is
        ckanext/myplugin/plugin.py and the translations are stored in
        i18n/
        '''
        # assume plugin is called ckanext.<myplugin>.<...>.PluginClass
        extension_module_name = '.'.join(self.__module__.split('.')[:3])
        module = sys.modules[extension_module_name]
        return os.path.join(os.path.dirname(module.__file__), '../i18n')


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
