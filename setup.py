#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Coralogix Logger Python SDK
Author: Coralogix Ltd.
Email: info@coralogix.com
"""

from setuptools import setup, find_packages
import coralogix

setup(
    name=coralogix.__name__,
    version=coralogix.__version__,
    author=coralogix.__author__,
    author_email=coralogix.__email__,
    maintainer=coralogix.__maintainer__,
    maintainer_email=coralogix.__email__,
    url='http://www.coralogix.com/',
    download_url='https://github.com/coralogix/python-coralogix-sdk/archive/master.zip',
    license=coralogix.__license__,
    description='Coralogix Python SDK',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    python_requires='>=2.7',
    install_requires=[
        'enum34==1.1.6',
        'requests==2.18.4',
    ],
    extras_require={
        'development': [
            'wheel==0.31.0',
        ],
    },
    tests_require=[
        'tox',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Manufacturing',
        'Intended Audience :: Telecommunications Industry',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: Log Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Logging',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Utilities',
    ],
    keywords=[
        'Coralogix',
        'Logging',
        'Logger',
    ],
    test_suite='coralogix.tests',
    zip_safe=False,
    include_package_data=True
)
