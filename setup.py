#!/usr/bin/env python

from __future__ import absolute_import, unicode_literals

from codecs import open

from wagtailmodelchoosers import __version__

try:
    from setuptools import find_packages, setup
except ImportError:
    from distutils.core import setup


install_requires = [
    'wagtail>=2.13,<2.14',  # Depends on Wagtail's Django and Django RestFramework depencencies
    'django-filter>=2.4.0,<2.5.0'
]

# Testing dependencies
testing_extras = [
    # Required for running the tests
    'tox==3.23.1',

    # For coverage and PEP8 linting
    'coverage==5.5',
    'flake8==3.9.2',
    # 'flake8-colors>=0.1.9,<1',
    'isort==5.8.0',
]

# Documentation dependencies
documentation_extras = [

]

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='wagtailmodelchoosers',
    version=__version__,
    description='A Wagtail app to pick generic models (rather than snippets or pages)',
    author='Springload',
    author_email='hello@springload.co.nz',
    url='https://github.com/springload/wagtailmodelchoosers',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    long_description=readme,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Editors :: Word Processors',
    ],
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        'docs': documentation_extras,
    },
    zip_safe=False,
)
