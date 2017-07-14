#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from os import walk
from os.path import abspath, normpath
from os.path import join as pj

from setuptools import setup, find_packages


short_descr = "Building packages with long term support"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in src/pkglts/version.py
version = {}
with open("src/pkglts/version.py") as fp:
    exec(fp.read(), version)


data_files = []

nb = len(normpath(abspath("src/pkglts_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]


for root, dnames, fnames in walk("src/pkglts_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


setup_kwds = dict(
    name='pkglts',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole, ",
    author_email="revesansparole@gmail.com, ",
    url='https://github.com/revesansparole/pkglts',
    license='CeCILL-C',
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    
    include_package_data=True,
    package_data={'pkglts_data': data_files},
    setup_requires=[
        "pytest-runner",
        ],
    install_requires=[
        "jinja2",
        ],
    tests_require=[
        "coverage",
        "coveralls",
        "flake8",
        "mock",
        "nbconvert",
        "pytest",
        "pytest-cov",
        "sphinx",
        "tox",
        "twine",
        ],
    entry_points={},
    keywords='packaging, package builder',
    
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    )
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['console_scripts'] = ['pmg = pkglts.manage_script:main']
setup_kwds['entry_points']['pkglts'] = [
    'base.parameters = pkglts.option.base.config:parameters',
    'base.check = pkglts.option.base.config:check',
    'base.require = pkglts.option.base.config:require',
    'base.environment_extensions = pkglts.option.base.handlers:environment_extensions',

    'conda.require = pkglts.option.conda.config:require',

    'coverage.require = pkglts.option.coverage.config:require',

    'coveralls.require = pkglts.option.coveralls.config:require',
    'coveralls.environment_extensions = pkglts.option.coveralls.handlers:environment_extensions',

    'data.require = pkglts.option.data.config:require',

    'doc.parameters = pkglts.option.doc.config:parameters',
    'doc.check = pkglts.option.doc.config:check',
    'doc.require = pkglts.option.doc.config:require',

    'flake8.require = pkglts.option.flake8.config:require',

    'github.parameters = pkglts.option.github.config:parameters',
    'github.check = pkglts.option.github.config:check',
    'github.require = pkglts.option.github.config:require',

    'landscape.require = pkglts.option.landscape.config:require',
    'landscape.environment_extensions = pkglts.option.landscape.handlers:environment_extensions',

    'license.parameters = pkglts.option.license.config:parameters',
    'license.check = pkglts.option.license.config:check',
    'license.require = pkglts.option.license.config:require',
    'license.environment_extensions = pkglts.option.license.handlers:environment_extensions',

    'notebook.parameters = pkglts.option.notebook.config:parameters',
    'notebook.check = pkglts.option.notebook.config:check',
    'notebook.require = pkglts.option.notebook.config:require',
    'notebook.regenerate = pkglts.option.notebook.regenerate:main',

    'pypi.parameters = pkglts.option.pypi.config:parameters',
    'pypi.check = pkglts.option.pypi.config:check',
    'pypi.require = pkglts.option.pypi.config:require',
    'pypi.environment_extensions = pkglts.option.pypi.handlers:environment_extensions',

    'pysetup.parameters = pkglts.option.pysetup.config:parameters',
    'pysetup.check = pkglts.option.pysetup.config:check',
    'pysetup.require = pkglts.option.pysetup.config:require',
    'pysetup.environment_extensions = pkglts.option.pysetup.handlers:environment_extensions',

    'readthedocs.parameters = pkglts.option.readthedocs.config:parameters',
    'readthedocs.check = pkglts.option.readthedocs.config:check',
    'readthedocs.require = pkglts.option.readthedocs.config:require',
    'readthedocs.environment_extensions = pkglts.option.readthedocs.handlers:environment_extensions',

    'sphinx.parameters = pkglts.option.sphinx.config:parameters',
    'sphinx.check = pkglts.option.sphinx.config:check',
    'sphinx.require = pkglts.option.sphinx.config:require',

    'test.parameters = pkglts.option.test.config:parameters',
    'test.check = pkglts.option.test.config:check',
    'test.require = pkglts.option.test.config:require',

    'tox.require = pkglts.option.tox.config:require',

    'travis.require = pkglts.option.travis.config:require',
    'travis.environment_extensions = pkglts.option.travis.handlers:environment_extensions',

    'version.parameters = pkglts.option.version.config:parameters',
    'version.check = pkglts.option.version.config:check',
    'version.require = pkglts.option.version.config:require',
]

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
