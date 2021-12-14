# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='bv-backend',
    description='description',
    long_description='',
    license='',
    packages=['bv_backend'],
    install_requires=['fastapi', 'uvicorn[standard]', "jinja2"],
)
