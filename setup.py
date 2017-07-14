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
]

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
