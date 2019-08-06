from setuptools import setup, find_packages

setup(
    name='brainvisa_auth',
    version='0.0.1',
    #author=__author__,
    #author_email=__email__,
    description='The BrainVISA authentication and authorization service',
    #long_description=readme() + '\n\n' + changes(),
    #license=__license__,
    #url='https://github.com/brainvisa/brainvisa_rest',
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    keywords='rest web flask',
    packages=find_packages(),
    #include_package_data=True,
    #zip_safe=False,
    install_requires=[
        'flask >= 1.0',
        #'flask-login',
        #'flask-wtf',
        #'psycopg2-binary >= 2.7',
        #'click >= 5.0',
        'gunicorn',
        #'pgpy',
    ],
    #extras_require={
        #'testing': [
            ##'WebTest >= 1.3.1',  # py3 compat
            ##'pytest',
            ##'pytest-cov',
        #],
    #},
)
