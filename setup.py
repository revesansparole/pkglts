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

# find packages
pkgs = find_packages('src')

pkg_data = {}

nb = len(normpath(abspath("src/pkglts"))) + 1
data_rel_pth = lambda pth: normpath(abspath(pth))[nb:]

data_files = []
for root, dnames, fnames in walk("src/pkglts"):
    for name in fnames:
        if splitext(name)[-1] in ['', '.bat', '.cfg', '.json', '.md', '.in', '.ini', '.png', '.ps1', '.rst', '.sh', '.tpl', '.txt', '.yaml', '.yml']:
            data_files.append(data_rel_pth(pj(root, name)))


pkg_data['pkglts'] = data_files

setup_kwds = dict(
    name='pkglts',
    version="4.6.0",
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="revesansparole",
    author_email="revesansparole@gmail.com",
    url='https://github.com/revesansparole/pkglts',
    license='CeCILL-C',
    zip_safe=False,

    packages=pkgs,
    package_dir={'': 'src'},
    
    
    package_data=pkg_data,
    setup_requires=[
        "pytest-runner",
        ],
    install_requires=[
        "jinja2",
        "requests",
        "semver",
        "unidecode",
        ],
    tests_require=[
        "coverage",
        "coveralls",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "tox",
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
        "Programming Language :: Python :: 3.6",
    ],
    )
# #}
# change setup_kwds below before the next pkglts tag

setup_kwds['entry_points']['console_scripts'] = ['pmg = pkglts.manage_script:main']
setup_kwds['entry_points']['pkglts'] = [
    'base = pkglts.option.base.option:OptionBase',
    'appveyor = pkglts.option.appveyor.option:OptionAppveyor',
    'conda = pkglts.option.conda.option:OptionConda',
    'coverage = pkglts.option.coverage.option:OptionCoverage',
    'coveralls = pkglts.option.coveralls.option:OptionCoveralls',
    'data = pkglts.option.data.option:OptionData',
    'doc = pkglts.option.doc.option:OptionDoc',
    'flake8 = pkglts.option.flake8.option:OptionFlake8',
    'git = pkglts.option.git.option:OptionGit',
    'github = pkglts.option.github.option:OptionGithub',
    'gitlab = pkglts.option.gitlab.option:OptionGitlab',
    'landscape = pkglts.option.landscape.option:OptionLandscape',
    'license = pkglts.option.license.option:OptionLicense',
    'notebook = pkglts.option.notebook.option:OptionNotebook',
    'plugin_project = pkglts.option.plugin_project.option:OptionPluginProject',
    'pypi = pkglts.option.pypi.option:OptionPypi',
    'pysetup = pkglts.option.pysetup.option:OptionPysetup',
    'readthedocs = pkglts.option.readthedocs.option:OptionReadthedocs',
    'requires = pkglts.option.requires.option:OptionRequires',
    'sphinx = pkglts.option.sphinx.option:OptionSphinx',
    'test = pkglts.option.test.option:OptionTest',
    'tox = pkglts.option.tox.option:OptionTox',
    'travis = pkglts.option.travis.option:OptionTravis',
    'version = pkglts.option.version.option:OptionVersion',
]

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
