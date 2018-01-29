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
        if splitext(name)[-1] in ['', '.bat', '.cfg', '.json', '.md', '.in', '.ini', '.png', '.ps1', '.rst', '.sh', '.tpl', '.txt', '.yaml', '.yml']:
            data_files.append(data_rel_pth(pj(root, name)))


pkg_data['pkglts'] = data_files

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
        "flake8",
        "nbconvert",
        "pytest",
        "pytest-cov",
        "pytest-mock",
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
    'appveyor.root = pkglts.option.appveyor',
    'appveyor.update_parameters = pkglts.option.appveyor.config:update_parameters',
    'appveyor.check = pkglts.option.appveyor.config:check',
    'appveyor.require = pkglts.option.appveyor.config:require',
    'appveyor.environment_extensions = pkglts.option.appveyor.handlers:environment_extensions',

    'base.root = pkglts.option.base',
    'base.update_parameters = pkglts.option.base.config:update_parameters',
    'base.check = pkglts.option.base.config:check',
    'base.require = pkglts.option.base.config:require',
    'base.environment_extensions = pkglts.option.base.handlers:environment_extensions',

    'conda.root = pkglts.option.conda',
    'conda.require = pkglts.option.conda.config:require',

    'coverage.root = pkglts.option.coverage',
    'coverage.require = pkglts.option.coverage.config:require',

    'coveralls.root = pkglts.option.coveralls',
    'coveralls.require = pkglts.option.coveralls.config:require',
    'coveralls.environment_extensions = pkglts.option.coveralls.handlers:environment_extensions',

    'data.root = pkglts.option.data',
    'data.update_parameters = pkglts.option.data.config:update_parameters',
    'data.check = pkglts.option.data.config:check',
    'data.require = pkglts.option.data.config:require',

    'doc.root = pkglts.option.doc',
    'doc.update_parameters = pkglts.option.doc.config:update_parameters',
    'doc.check = pkglts.option.doc.config:check',
    'doc.require = pkglts.option.doc.config:require',

    'flake8.root = pkglts.option.flake8',
    'flake8.require = pkglts.option.flake8.config:require',

    'git.root = pkglts.option.git',
    'git.update_parameters = pkglts.option.git.config:update_parameters',
    'git.check = pkglts.option.git.config:check',
    'git.require = pkglts.option.git.config:require',
    'git.environment_extensions = pkglts.option.git.handlers:environment_extensions',

    'github.root = pkglts.option.github',
    'github.update_parameters = pkglts.option.github.config:update_parameters',
    'github.check = pkglts.option.github.config:check',
    'github.require = pkglts.option.github.config:require',

    'gitlab.root = pkglts.option.gitlab',
    'gitlab.update_parameters = pkglts.option.gitlab.config:update_parameters',
    'gitlab.check = pkglts.option.gitlab.config:check',
    'gitlab.require = pkglts.option.gitlab.config:require',
    'gitlab.environment_extensions = pkglts.option.gitlab.handlers:environment_extensions',

    'landscape.root = pkglts.option.landscape',
    'landscape.require = pkglts.option.landscape.config:require',
    'landscape.environment_extensions = pkglts.option.landscape.handlers:environment_extensions',

    'license.root = pkglts.option.license',
    'license.update_parameters = pkglts.option.license.config:update_parameters',
    'license.check = pkglts.option.license.config:check',
    'license.require = pkglts.option.license.config:require',
    'license.environment_extensions = pkglts.option.license.handlers:environment_extensions',

    'notebook.root = pkglts.option.notebook',
    'notebook.update_parameters = pkglts.option.notebook.config:update_parameters',
    'notebook.check = pkglts.option.notebook.config:check',
    'notebook.require = pkglts.option.notebook.config:require',
    'notebook.regenerate = pkglts.option.notebook.regenerate:main',

    'plugin_project.root = pkglts.option.plugin_project',
    'plugin_project.update_parameters = pkglts.option.plugin_project.config:update_parameters',
    'plugin_project.check = pkglts.option.plugin_project.config:check',
    'plugin_project.require = pkglts.option.plugin_project.config:require',

    'pypi.root = pkglts.option.pypi',
    'pypi.update_parameters = pkglts.option.pypi.config:update_parameters',
    'pypi.check = pkglts.option.pypi.config:check',
    'pypi.require = pkglts.option.pypi.config:require',
    'pypi.environment_extensions = pkglts.option.pypi.handlers:environment_extensions',

    'pysetup.root = pkglts.option.pysetup',
    'pysetup.update_parameters = pkglts.option.pysetup.config:update_parameters',
    'pysetup.check = pkglts.option.pysetup.config:check',
    'pysetup.require = pkglts.option.pysetup.config:require',
    'pysetup.environment_extensions = pkglts.option.pysetup.handlers:environment_extensions',

    'readthedocs.root = pkglts.option.readthedocs',
    'readthedocs.update_parameters = pkglts.option.readthedocs.config:update_parameters',
    'readthedocs.check = pkglts.option.readthedocs.config:check',
    'readthedocs.require = pkglts.option.readthedocs.config:require',
    'readthedocs.environment_extensions = pkglts.option.readthedocs.handlers:environment_extensions',

    'requires.root = pkglts.option.requires',
    'requires.require = pkglts.option.requires.config:require',
    'requires.environment_extensions = pkglts.option.requires.handlers:environment_extensions',

    'sphinx.root = pkglts.option.sphinx',
    'sphinx.update_parameters = pkglts.option.sphinx.config:update_parameters',
    'sphinx.check = pkglts.option.sphinx.config:check',
    'sphinx.require = pkglts.option.sphinx.config:require',

    'test.root = pkglts.option.test',
    'test.update_parameters = pkglts.option.test.config:update_parameters',
    'test.check = pkglts.option.test.config:check',
    'test.require = pkglts.option.test.config:require',

    'tox.root = pkglts.option.tox',
    'tox.require = pkglts.option.tox.config:require',

    'travis.root = pkglts.option.travis',
    'travis.require = pkglts.option.travis.config:require',
    'travis.environment_extensions = pkglts.option.travis.handlers:environment_extensions',

    'version.root = pkglts.option.version',
    'version.update_parameters = pkglts.option.version.config:update_parameters',
    'version.check = pkglts.option.version.config:check',
    'version.require = pkglts.option.version.config:require',
]

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
