# -*- coding: utf-8 -*-
"""
    Eve SQLAlchemy i18n extension.
    Enables i18n support to eve_sqlalchemy

    :copyright: (c) 2017 RomanSo (CrabTulip Team)
"""
from sqlalchemy_utils import TranslationHybrid
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm.attributes import InstrumentedAttribute

from . import get_locale, default_locale

try:
    from sqlalchemy_i18n import Translatable
except ImportError:
    Translatable = None

translation_hybrid = None

def make_translation_hybrid(column):
    global translation_hybrid
    if translation_hybrid is None:
        translation_hybrid = TranslationHybrid(
            current_locale=get_locale,
            default_locale=default_locale
        )
    return translation_hybrid(column)

def make_trans_hybrid_attr(name, column ):
    c = make_translation_hybrid(column)
    c.__name__ = name
    c.__is_translatable_column__  = True
    column.__translations_store__ = True
    return c

def eve_domain_resource_enable_sqlalchemyi18n(domain_model, model, hide_translations):
    if Translatable is not None and issubclass(model, Translatable):
        return

    for prop in class_mapper(model).all_orm_descriptors:
        # allow write
        if isinstance(prop, hybrid_property) and hasattr(prop, '__is_translatable_column__'):
            del domain_model['schema'][prop.__name__]['readonly']
        # set projection to 0 and change type to dict
        if isinstance(prop, InstrumentedAttribute) and hasattr(prop, '__translations_store__'):
            domain_model['schema'][prop.key]['type'] = 'dict'
            if hide_translations:
                domain_model['datasource']['projection'][prop.key] = 0
            else:
                domain_model['datasource']['projection'][prop.key] = 1

