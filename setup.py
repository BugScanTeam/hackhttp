#!/usr/bin/env python
# coding:utf-8
from setuptools import setup
from hackhttp import (
    __title__, __version__, __author__, __url__,
    __author_email__, __license__)
setup(
    name=__title__,
    version=__version__,
    description="Hackhttp is an HTTP library, written in Python.",
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    package_data={'hackhttp': ['*.md']},
    package_dir={'hackhttp': 'hackhttp'},
    packages=['hackhttp'],
    include_package_data=True,
    keywords='http',
)
