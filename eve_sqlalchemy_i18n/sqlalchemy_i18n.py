# -*- coding: utf-8 -*-
"""
    Eve SQLAlchemy i18n extension
    Enables i18n support to eve_sqlalchemy

    :copyright: (c) 2017 RomanSo (CrabTulip Team)
"""
from sqlalchemy_i18n.utils import all_translated_columns
from sqlalchemy_i18n import Translatable
from sqlalchemy.ext.hybrid import hybrid_property


def eve_domain_resource_enable_sqlalchemyi18n(domain, translatable_model, hide_translations):
    if not issubclass(translatable_model, Translatable):
        return

    if hasattr(translatable_model, 'translations' ):
        domain['datasource']['projection']['translations'] = 0

    if hasattr(translatable_model, 'current_translation' ):
        domain['datasource']['projection']['current_translation'] = 0

    if hasattr(translatable_model, 'fallback_translation' ):
        domain['datasource']['projection']['fallback_translation'] = 0

    for col in all_translated_columns(translatable_model):
        column_translations_name = "__{0}_translations__".format(col.name)

        class make_translations_dict_getter:

            def __init__(self, name):
                self.name = name

            def __call__(self, obj):
                def make_pair(lc):
                    return (lc, getattr(obj.translations[lc], self.name))
                return dict(map( make_pair, obj.__translatable__['locales'] ))


        class make_translations_dict_setter:

            def __init__(self, name):
                self.name = name

            def __call__(self, obj, val):
                for x,y in val.items():
                    setattr(obj.translations[x], self.name, y)

        hp = hybrid_property(
            fget=make_translations_dict_getter(col.name),
            fset=make_translations_dict_setter(col.name)
            # expr=
        )

        hp.__name__ = column_translations_name

        setattr(translatable_model, column_translations_name, hp )

        domain['datasource']['projection'][col.name] = 1
        domain['schema'][col.name] = {
            'type':'string'
            ,'unique':False
            ,'required':False
            ,'readonly':False
        }

        domain['schema'][column_translations_name] = {
            'type':'dict'
            ,'unique':False
            ,'required':False
            ,'readonly':False
        }

        if hide_translations:
            domain['datasource']['projection'][column_translations_name] = 0
        else:
            domain['datasource']['projection'][column_translations_name] = 1
