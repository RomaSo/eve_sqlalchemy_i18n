import eve_sqlalchemy_i18n

eve_sqlalchemy_i18n.locales = ['en', 'fi']
eve_sqlalchemy_i18n.default_locale = 'en'


def get_locale():
    from flask import request
    lc = request.accept_languages.best_match(eve_sqlalchemy_i18n.locales)
    return lc

eve_sqlalchemy_i18n.get_locale = get_locale
