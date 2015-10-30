#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Setup script has been generated automatically
# do not modify

from os import walk
from os.path import abspath, normpath
from os.path import join as pj
from setuptools import setup, find_packages


short_descr = "Building packages with long term support"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

# find version number in /src/$pkg_pth/version.py
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


setup(
    name='pkglts',
    
    version=version["__version__"],
    
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="base.author_name",
    author_email='base.author_email',
    url='',
    license="mit",
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    
    include_package_data=True,
    package_data={'pkglts_data': data_files},
    
    install_requires=open("requirements.txt").read().split("\n"),
    tests_require=[],
        entry_points={
        'console_scripts': [
            'manage = pkglts.manage_script:main',
        ],
    },

    keywords='packaging, package builder',
    
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    
    test_suite='nose.collector',
)
