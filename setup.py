#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {{pkglts pydist,
from os import walk
from os.path import abspath, normpath
from os.path import join as pj
from setuptools import setup, find_packages


short_descr = "Building packages with long term support"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def parse_requirements(fname):
    with open(fname, 'r') as f:
        txt = f.read()

    reqs = []
    for line in txt.splitlines():
        line = line.strip()
        if len(line) > 0 and not line.startswith("#"):
            reqs.append(line)

    return reqs

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
    author="revesansparole",
    author_email='revesansparole@gmail.com',
    url='',
    license="mit",
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    package_data={'pkglts_data': data_files},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    entry_points={
        'console_scripts': [
            'pmg = pkglts.manage_script:main',
        ],
    },

    keywords='packaging, package builder',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='nose.collector',
)
# }}
