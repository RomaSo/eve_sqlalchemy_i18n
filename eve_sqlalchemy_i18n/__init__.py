# -*- coding: utf-8 -*-
"""
    Eve SQLAlchemy i18n extension.
    Enables i18n support to eve_sqlalchemy

    :copyright: (c) 2017 RomanSo (CrabTulip Team)
"""
__version__ = '0.1.1'

from sqlalchemy_utils.functions import get_class_by_table

get_locale = None
default_locale = 'en'
locales = ['en']

def eve_domain_enable_sqlalchemyi18n(eve_domain, base, patch_function, hide_translations=False):

    def make_pair(v):
        c = get_class_by_table(base, v[1])
        return (c.__name__, c)

    models_by_name = dict(map(make_pair, base.metadata.tables.items()))

    for resource in eve_domain:
        source = eve_domain[resource]['datasource']['source']
        if source in models_by_name:
            patch_function(eve_domain[resource], models_by_name[source], hide_translations)
