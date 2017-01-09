#!/usr/bin/env python

from setuptools import setup


DESCRIPTION = ("Eve SQLAlchemy i18n extension")

with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

install_requires = [
]

setup(
    name='Eve-SQLAlchemy-i18n',
    version='0.1.0',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='RomanSo',
    url='https://github.com/RomaSo/eve_sqlalchemy_i18n',
    platforms=["any"],
    packages=['eve_sqlalchemy_i18n'],
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 0 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
