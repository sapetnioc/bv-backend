#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='bv_services',
    description='description',
    long_description='',
    license='',
    # package_dir = {'': 'python'},
    packages=['bv_services'],
    install_requires=['fastapi', 'uvicorn[standard]', "jinja2"],
)
