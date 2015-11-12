#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {{pkglts pysetup,
from os import walk
from os.path import abspath, normpath
from os.path import join as pj
from setuptools import setup, find_packages


short_descr = "{{key, doc.description}}"
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

# {{version rm,
# find version number in /src/$pkg_pth/version.py
version = {}
with open("{{src_pth, }}/version.py") as fp:
    exec(fp.read(), version)
# }}


# {{data rm,
data_files = []

nb = len(normpath(abspath("src/{{key, base.pkgname}}_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]


for root, dnames, fnames in walk("src/{{key, base.pkgname}}_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))

# }}

setup(
    name='{{key, base.pkg_fullname}}',
    # {{version rm,
    version=version["__version__"],
    # }}
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="{{key, pysetup.author_name}}",
    author_email='{{key, pysetup.author_email}}',
    url='{{pkg_url, }}',
    # {{license.setup,
    license="None",
    # }}
    zip_safe=False,

    packages=find_packages('src'),
    package_dir={'': 'src'},
    # {{data rm,
    include_package_data=True,
    package_data={'{{key, base.pkgname}}_data': data_files},
    # }}
    install_requires=parse_requirements("requirements.txt"),
    tests_require=parse_requirements("dvlpt_requirements.txt"),
    # {{plugin.setup pysetup.extra rm,
    entry_points={
        # 'console_scripts': [
        #       'fake_script = openalea.fakepackage.amodule:console_script', ],
        # 'gui_scripts': [
        #      'fake_gui = openalea.fakepackage.amodule:gui_script',],
        #      'wralea': wralea_entry_points
    },
    # }}
    keywords='{{key, doc.keywords}}',
    # {{pypi rm,
    classifiers=[# {{pypi.classifiers,
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        # }}
    ],
    # }}
    test_suite='nose.collector',
)
# }}
