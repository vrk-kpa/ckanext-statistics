from ckan.plugins import toolkit as tk
from ckan import model


def statistics_read():
    try:
        context = {'model': model, 'session': model.Session,
                   'user': tk.c.user, 'auth_user_obj': tk.c.userobj}
        tk.check_access('statistics_read', context)
        if 'matomo' in tk.config.get('ckan.plugins', '').split():
            try:
                location_data = tk.get_action('report_data_get')({}, {'id': 'matomo-location'})[0]
            except (tk.NotAuthorized, tk.ObjectNotFound):
                location_data = {}
        else:
            location_data = {}

        return tk.render('statistics/statistics_read.html', extra_vars={"data": location_data})
    except tk.NotAuthorized:
        return tk.abort(403, tk._("User must be logged in to view this page"))


def reports_read():
    return tk.render('statistics/reports_read.html', extra_vars={})
