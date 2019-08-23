from setuptools import setup, find_packages

setup(
    name='bv_admin',
    version='0.0.1',
    description='Project and users administration for BrainVISA services',
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    keywords='rest web flask',
    packages=['bv_admin'],
    install_requires=['bv_rest'],
)
