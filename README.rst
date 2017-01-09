==============================
Eve SQLAlchemy i18n extension
==============================

This extension allows to include i18n support in eve sqlalchemy.

Installation
------------

.. code-block:: console

    git clone https://github.com/RomaSo/eve_sqlalchemy_i18n.git

    cd eve_sqlalchemy_i18n

    python setup.py install


Configuration
-------------

Eve SQLAlchemy i18n with sqlalchemy_utils i18n (PostgreSQL HSTOR)

* Example translation model

.. code-block:: python

    from sqlalchemy import Column, BIGINT
    from sqlalchemy.dialects.postgresql import HSTORE
    from sqlalchemy.ext.mutable import MutableDict
    from eve_sqlalchemy_i18n.pgsql_hstor import make_trans_hybrid_attr

    from models import Base

    class ExampleTranslationModel(Base):
        __tablename__ = 'example_translation_model'
        __name_translations__  = Column(MutableDict.as_mutable(HSTORE))
        _id                    = Column(BIGINT, primary_key=True, autoincrement=True)
        name                   = make_trans_hybrid_attr('name', __name_translations__)

* Example of eve settings.py file

.. code-block:: python

    import translations
    from eve_sqlalchemy_i18n import eve_domain_enable_sqlalchemyi18n
    from eve_sqlalchemy_i18n.pgsql_hstor import eve_domain_resource_enable_sqlalchemyi18n
    from models import Base

    #import eve_sqlalchemy models here
    from models import ExampleTranslationModel

    #register eve_sqlalchemy models here
    registerSchema('ExampleTranslationModel')(ExampleTranslationModel)

    #setup eve domain
    DOMAIN = {
        'example_translation_model': ExampleTranslationModel._eve_schema['ExampleTranslationModel']
    }

    #enable eve_sqlaclhemy_i18n
    eve_domain_enable_sqlalchemyi18n(DOMAIN, Base, eve_domain_resource_enable_sqlalchemyi18n)

* Example of translations.py file

.. code-block:: python

    import eve_sqlalchemy_i18n


    eve_sqlalchemy_i18n.locales = ['en', 'fi']
    eve_sqlalchemy_i18n.default_locale = 'en'

    def get_locale():
        from flask import request
        lc = request.accept_languages.best_match(eve_sqlalchemy_i18n.locales)
        return lc

    eve_sqlalchemy_i18n.get_locale = get_locale


Eve SQLAlchemy i18n with sqlalchemy_i18n

* Example translation model

.. code-block:: python

    import eve_sqlalchemy_i18n
    from eve_sqlalchemy_i18n.sqlalchemy_i18n import EveSQLAlchemyi18n
    from sqlalchemy import Column, BIGINT, Unicode
    from sqlalchemy_i18n import Translatable, translation_base
    from models import Base


    class ExampleTranslationModel(EveSQLAlchemyi18n, Translatable, Base):
        __tablename__ = 'example_translation_model'
        __translatable__ = { 'locales': eve_sqlalchemy_i18n.locales }
        __BASE__ = Base #EveSQLAlchemyi18n.__init__ call __BASE__.__init__

        locale = eve_sqlalchemy_i18n.default_locale

        id = Column(BIGINT, primary_key=True, autoincrement=True)

    class ExampleTranslationModelTranslation(translation_base(ExampleTranslationModel)):
        __tablename__ = 'example_translation_model_translation'

        name = Column(Unicode(255))

* Example of eve settings.py file

.. code-block:: python

    import translations
    from eve_sqlalchemy_i18n import eve_domain_enable_sqlalchemyi18n
    from eve_sqlalchemy_i18n.sqlalchemy_i18n import eve_domain_resource_enable_sqlalchemyi18n
    from models import Base

    #import eve_sqlalchemy models here
    from models import ExampleTranslationModel

    #register eve_sqlalchemy models here
    registerSchema('ExampleTranslationModel')(ExampleTranslationModel)

    #setup eve domain
    DOMAIN = {
        'example_translation_model': ExampleTranslationModel._eve_schema['ExampleTranslationModel']
    }

    #enable eve_sqlaclhemy_i18n
    eve_domain_enable_sqlalchemyi18n(DOMAIN, Base, eve_domain_resource_enable_sqlalchemyi18n)


* Example of translations.py file

.. code-block:: python

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

Usage
-----

* post with all translations

.. code-block:: console

    curl -H "Content-Type: application/json" -X POST -d '{"__name_translations__":{"en":"en_name", "fi":"fi_name"}}' http://localhost:5000/api/example_translation_model

* post with current translation

.. code-block:: console

    curl -H "Content-Type: application/json" -X POST -d '{"name":"en_name"}' http://localhost:5000/api/example_translation_model

* example output of get request

.. code-block:: json

    {
      "_items": [
        {
          "__name_translations__": {
            "en": "en_name",
            "fi": "fi_name"
          },
          "_created": "2017-01-09 14:28:28",
          "_etag": "deb95f5e07166bb0ada64834790e26be0062575e",
          "_id": 1,
          "_links": {
            "self": {
              "href": "example_translation_model/1",
              "title": "example_translation_model"
            }
          },
          "_updated": "2017-01-09 14:28:28",
          "name": "en_name"
        }
      ],
      "_links": {
        "parent": {
          "href": "/",
          "title": "home"
        },
        "self": {
          "href": "example_translation_model",
          "title": "example_translation_model"
        }
      },
      "_meta": {
        "max_results": 25,
        "page": 1,
        "total": 1
      }
    }

