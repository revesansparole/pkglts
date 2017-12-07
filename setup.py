#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments

from os import walk
from os.path import abspath, normpath, splitext
from os.path import join as pj

from setuptools import setup, find_packages


short_descr = "Building packages with long term support"
readme = open('README.rst').read()
history = open('HISTORY.rst').read()


# find version number in src/pkglts/version.py
version = {}
with open("src/pkglts/version.py") as fp:
    exec(fp.read(), version)

# find packages
pkgs = find_packages('src')

pkg_data = {}

nb = len(normpath(abspath("src/pkglts"))) + 1
data_rel_pth = lambda pth: normpath(abspath(pth))[nb:]

data_files = []
for root, dnames, fnames in walk("src/pkglts"):
    for name in fnames:
        if splitext(name)[-1] in ['.json', '.ini']:
            data_files.append(data_rel_pth(pj(root, name)))


pkg_data['pkglts'] = data_files
nb = len(normpath(abspath("src/pkglts_data"))) + 1
data_rel_pth = lambda pth: normpath(abspath(pth))[nb:]

data_files = []
for root, dnames, fnames in walk("src/pkglts_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


pkg_data['pkglts_data'] = data_files

setup_kwds = dict(
    name='pkglts',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole",
    author_email="revesansparole@gmail.com",
    url='https://github.com/revesansparole/pkglts',
    license='CeCILL-C',
    zip_safe=False,

    packages=pkgs,
    package_dir={'': 'src'},
    
    
    include_package_data=True,
    
    package_data=pkg_data,
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
    'base.update_parameters = pkglts.option.base.config:update_parameters',
    'base.check = pkglts.option.base.config:check',
    'base.require = pkglts.option.base.config:require',
    'base.environment_extensions = pkglts.option.base.handlers:environment_extensions',
    'base.files_dir = pkglts_data.base',

    'conda.require = pkglts.option.conda.config:require',
    'conda.files_dir = pkglts_data.base',

    'coverage.require = pkglts.option.coverage.config:require',
    'coverage.files_dir = pkglts_data.base',

    'coveralls.require = pkglts.option.coveralls.config:require',
    'coveralls.environment_extensions = pkglts.option.coveralls.handlers:environment_extensions',

    'data.update_parameters = pkglts.option.data.config:update_parameters',
    'data.check = pkglts.option.data.config:check',
    'data.require = pkglts.option.data.config:require',
    'data.files_dir = pkglts_data.base',

    'doc.update_parameters = pkglts.option.doc.config:update_parameters',
    'doc.check = pkglts.option.doc.config:check',
    'doc.require = pkglts.option.doc.config:require',
    'doc.files_dir = pkglts_data.base',

    'flake8.require = pkglts.option.flake8.config:require',

    'git.update_parameters = pkglts.option.git.config:update_parameters',
    'git.check = pkglts.option.git.config:check',
    'git.require = pkglts.option.git.config:require',
    'git.environment_extensions = pkglts.option.git.handlers:environment_extensions',
    'git.files_dir = pkglts_data.base',

    'github.update_parameters = pkglts.option.github.config:update_parameters',
    'github.check = pkglts.option.github.config:check',
    'github.require = pkglts.option.github.config:require',

    'gitlab.update_parameters = pkglts.option.gitlab.config:update_parameters',
    'gitlab.check = pkglts.option.gitlab.config:check',
    'gitlab.require = pkglts.option.gitlab.config:require',

    'landscape.require = pkglts.option.landscape.config:require',
    'landscape.environment_extensions = pkglts.option.landscape.handlers:environment_extensions',
    'landscape.files_dir = pkglts_data.base',

    'license.update_parameters = pkglts.option.license.config:update_parameters',
    'license.check = pkglts.option.license.config:check',
    'license.require = pkglts.option.license.config:require',
    'license.environment_extensions = pkglts.option.license.handlers:environment_extensions',
    'license.files_dir = pkglts_data.base',

    'notebook.update_parameters = pkglts.option.notebook.config:update_parameters',
    'notebook.check = pkglts.option.notebook.config:check',
    'notebook.require = pkglts.option.notebook.config:require',
    'notebook.regenerate = pkglts.option.notebook.regenerate:main',

    'plugin_project.update_parameters = pkglts.option.plugin_project.config:update_parameters',
    'plugin_project.check = pkglts.option.plugin_project.config:check',
    'plugin_project.require = pkglts.option.plugin_project.config:require',
    'plugin_project.files_dir = pkglts_data.base',

    'pypi.update_parameters = pkglts.option.pypi.config:update_parameters',
    'pypi.check = pkglts.option.pypi.config:check',
    'pypi.require = pkglts.option.pypi.config:require',
    'pypi.environment_extensions = pkglts.option.pypi.handlers:environment_extensions',
    'pypi.files_dir = pkglts_data.base',

    'pysetup.update_parameters = pkglts.option.pysetup.config:update_parameters',
    'pysetup.check = pkglts.option.pysetup.config:check',
    'pysetup.require = pkglts.option.pysetup.config:require',
    'pysetup.environment_extensions = pkglts.option.pysetup.handlers:environment_extensions',
    'pysetup.files_dir = pkglts_data.base',

    'readthedocs.update_parameters = pkglts.option.readthedocs.config:update_parameters',
    'readthedocs.check = pkglts.option.readthedocs.config:check',
    'readthedocs.require = pkglts.option.readthedocs.config:require',
    'readthedocs.environment_extensions = pkglts.option.readthedocs.handlers:environment_extensions',

    'requires.require = pkglts.option.requires.config:require',
    'requires.environment_extensions = pkglts.option.requires.handlers:environment_extensions',

    'sphinx.update_parameters = pkglts.option.sphinx.config:update_parameters',
    'sphinx.check = pkglts.option.sphinx.config:check',
    'sphinx.require = pkglts.option.sphinx.config:require',
    'sphinx.files_dir = pkglts_data.base',

    'test.update_parameters = pkglts.option.test.config:update_parameters',
    'test.check = pkglts.option.test.config:check',
    'test.require = pkglts.option.test.config:require',
    'test.files_dir = pkglts_data.base',

    'tox.require = pkglts.option.tox.config:require',
    'tox.files_dir = pkglts_data.base',

    'travis.require = pkglts.option.travis.config:require',
    'travis.environment_extensions = pkglts.option.travis.handlers:environment_extensions',
    'travis.files_dir = pkglts_data.base',

    'version.update_parameters = pkglts.option.version.config:update_parameters',
    'version.check = pkglts.option.version.config:check',
    'version.require = pkglts.option.version.config:require',
    'version.files_dir = pkglts_data.base',
]

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
