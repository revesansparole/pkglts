#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments
{% if 'data' is available %}
from os import walk
from os.path import abspath, normpath, splitext
from os.path import join as pj
{% endif %}
from setuptools import setup, find_packages


short_descr = "{{ doc.description }}"
readme = open('README.{{ doc.fmt }}').read()
history = open('HISTORY.{{ doc.fmt }}').read()

# find packages
pkgs = find_packages('src')

{% if 'data' is available -%}
pkg_data = {}

nb = len(normpath(abspath("{{ base.src_pth }}"))) + 1
data_rel_pth = lambda pth: normpath(abspath(pth))[nb:]

data_files = []
for root, dnames, fnames in walk("{{ base.src_pth }}"):
    for name in fnames:
        if splitext(name)[-1] in {{ data.filetype }}:
            data_files.append(data_rel_pth(pj(root, name)))


pkg_data['{{ base.pkg_full_name }}'] = data_files

{%- if data.use_ext_dir %}
nb = len(normpath(abspath("src/{{ base.pkgname }}_data"))) + 1
data_rel_pth = lambda pth: normpath(abspath(pth))[nb:]

data_files = []
for root, dnames, fnames in walk("src/{{ base.pkgname }}_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


pkg_data['{{ base.pkgname }}_data'] = data_files
{%- endif -%}
{%- endif %}

setup_kwds = dict(
    name='{{ base.pkg_full_name }}',
    version="{{ version.major }}.{{ version.minor }}.{{ version.post }}",
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="{{ base.authors[0][0] }}",
    author_email="{{ base.authors[0][1] }}",
    url='{{ pysetup.pkg_url }}',
    license='{{ license.name }}',
    zip_safe=False,

    packages=pkgs,
    {%- if base.namespace is not none %}
    {% if base.namespace_method == 'setuptools' -%}
    namespace_packages=['{{ base.namespace }}'],
    {%- endif %}
    {%- endif %}
    package_dir={'': 'src'},
    {% if 'data' is available %}
    {% if data.use_ext_dir %}
    include_package_data=True,
    {% endif %}
    package_data=pkg_data,
    {% endif -%}
    setup_requires=[
        {% if 'test' is available -%}
        {% if test.suite_name == 'pytest' -%}
        "pytest-runner",
        {% endif -%}
        {% endif -%}
    ],
    install_requires=[
        {% for dep in pysetup.requirements('install') -%}
        {% if dep.is_pip(strict=False) -%}
        "{{ dep.fmt_pip_requirement() }}",
        {% endif -%}
        {%- endfor %}],
    tests_require=[
        {% for dep in pysetup.requirements('test') -%}
        {% if dep.is_pip(strict=False) -%}
        "{{ dep.fmt_pip_requirement() }}",
        {% endif -%}
        {%- endfor %}],
    entry_points={},
    keywords='{{ doc.keywords|join(", ") }}',
    {% if 'pypi' is available %}
    classifiers=[
        {%- for kwd in pypi.auto_classifiers %}
        "{{ kwd }}",
        {%- endfor %}
    ],
    {% endif -%}
    {% if 'test' is available -%}
    {% if test.suite_name == 'nose' %}
    test_suite='nose.collector',
    {% endif -%}
    {% endif -%}
)
# #}
# change setup_kwds below before the next pkglts tag

# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
