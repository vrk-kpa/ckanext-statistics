# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckanext.statistics import views


class MixinPlugin(p.SingletonPlugin):
    p.implements(p.IBlueprint)

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprint()
