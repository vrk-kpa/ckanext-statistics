from flask import Blueprint
from . import utils

statistics = Blueprint('statistics', __name__, url_prefix='/statistics')


def get_blueprint():
    return [statistics]


@statistics.route('/')
def index():
    return utils.statistics_read()


@statistics.route('/internal')
def internal():
    return utils.reports_read()
