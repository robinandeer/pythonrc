#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The setup script for rc
"""
import os
import sys
from setuptools import setup, find_packages

import rc

# Shortcut for publishing to Pypi
# Source: https://github.com/kennethreitz/tablib/blob/develop/setup.py
if sys.argv[-1] == 'publish':
  os.system('python setup.py sdist upload')
  sys.exit()

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as stream:
  README = stream.read()
with open(os.path.join(here, 'CHANGELOG.txt')) as stream:
  CHANGELOG = stream.read()

setup(
  name='rc',
  version=rc.__version__,
  description='rc is a Python package that ...',
  long_description=README + '\n\n' + CHANGELOG,
  classifiers=[
    # From http://pypi.python.org/pypi?%3Aaction=list_classifiers
    'Development Status :: 3 - Alpha',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
    'License :: OSI Approved :: MIT License'
  ],
  keywords='',
  author=rc.__author__,
  author_email='robin.andeer@gmail.com',
  url=rc.__url__,
  license=rc.__license__,
  py_modules=['rc'],
  scripts=[],

  # Project dependencies
  install_requires=[
    'path.py',
    'PyYAML'
  ],

  # <optional-feature>: [<dependencies>]
  extras_require={

  },

  # Packages required for testing
  tests_require=[
    'pytest'
  ],
  platforms='any',
  test_suite='test_rc',

  # 'include_package_dat = True' or
  package_data={
    # If any package contains *.txt or *.rst files, include them:
    "": ["*.txt", "*.rst"],
    # And include any *.msg files found in the 'hello' package, too:
    "hello": ["*.msg"]
  },

  # The project can be safely installed and run from a zip file
  zip_safe=False,
)
