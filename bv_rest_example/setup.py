from setuptools import setup, find_packages

setup(
    name='bv_rest',
    version='0.0.1',
    description='Test web services with sample pseudo scientific data',
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    keywords='rest web flask',
    packages=find_packages(),
    install_requires=[
        'flask >= 1.0',
        'gunicorn',
    ],
)
