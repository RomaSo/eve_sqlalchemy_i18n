import eve_sqlalchemy_i18n
import sqlalchemy_utils
from sqlalchemy_i18n import make_translatable


eve_sqlalchemy_i18n.locales = ['en', 'fi']
eve_sqlalchemy_i18n.default_locale = 'en'

def get_locale():
    from flask import request
    lc = request.accept_languages.best_match(eve_sqlalchemy_i18n.locales)
    return lc

eve_sqlalchemy_i18n.get_locale = get_locale
sqlalchemy_utils.i18n.get_locale = get_locale
make_translatable(options={'locales': eve_sqlalchemy_i18n.locales})
