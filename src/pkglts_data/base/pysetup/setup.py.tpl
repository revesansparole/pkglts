#!/usr/bin/env python
# -*- coding: utf-8 -*-

# {# pkglts, pysetup.kwds
# format setup arguments
{% if 'data' is available %}
from os import walk
from os.path import abspath, normpath
from os.path import join as pj
{% endif %}
from setuptools import setup, find_packages


short_descr = "{{ doc.description }}"
readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


# find version number in {{ base.src_pth }}/version.py
version = {}
with open("{{ base.src_pth }}/version.py") as fp:
    exec(fp.read(), version)


{% if 'data' is available -%}
data_files = []

nb = len(normpath(abspath("src/{{ base.pkgname }}_data"))) + 1


def data_rel_pth(pth):
    """ Return path relative to pkg_data
    """
    abs_pth = normpath(abspath(pth))
    return abs_pth[nb:]


for root, dnames, fnames in walk("src/{{ base.pkgname }}_data"):
    for name in fnames:
        data_files.append(data_rel_pth(pj(root, name)))


{% endif -%}

setup_kwds = dict(
    name='{{ base.pkg_full_name }}',
    version=version["__version__"],
    description=short_descr,
    long_description=readme + '\n\n' + history,
    author="{% for author, email in base.authors%}{{author}}, {% endfor %}",
    author_email="{% for author, email in base.authors%}{{email}}, {% endfor %}",
    url='{{ pysetup.pkg_url }}',
    license='{{ license.name }}',
    zip_safe=False,

    packages=find_packages('src'),
    {%- if base.namespace is not none %}
    namespace_packages=['{{ base.namespace }}'],
    {%- endif %}
    package_dir={'': 'src'},
    {% if 'data' is available %}
    include_package_data=True,
    package_data={'{{ base.pkgname }}_data': data_files},
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
        {% if dep.package_manager == 'pip' or dep.package_manager is none -%}
        "{{ dep.name }}",
        {% endif -%}
        {%- endfor %}],
    tests_require=[
        {% for dep in pysetup.requirements('dvlpt') -%}
        {% if dep.package_manager == 'pip' or dep.package_manager is none -%}
        "{{ dep.name }}",
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
{% if 'plugin_project' is available %}
setup_kwds['entry_points']['pkglts'] = [
    '{{ base.pkg_full_name }}.require = {{ base.pkg_full_name }}.config:require',
    '{{ base.pkg_full_name }}.files_dir = {{ base.pkg_full_name }}_data',
]
{% endif %}
# do not change things below
# {# pkglts, pysetup.call
setup(**setup_kwds)
# #}
