# {# pkglts, pysetup.kwds
# format setup arguments
{% if 'data' is available %}
from pathlib import Path
{% endif %}
from setuptools import setup, find_packages


short_descr = "{{ doc.description }}"
readme = open('README.{{ doc.fmt }}').read()
history = open('HISTORY.{{ doc.fmt }}').read()

# find packages
pkgs = find_packages('src')

{% if 'data' is available -%}
src_dir = Path("{{ src.src_pth }}")

data_files = []
for pth in src_dir.glob("**/*.*"):
    if pth.suffix in {{ data.filetype }}:
        data_files.append(str(pth.relative_to(src_dir)))

pkg_data= {'{{ base.pkg_full_name }}': data_files}

{%- if data.use_ext_dir %}
data_dir = Path("src/{{ base.pkgname }}_data")

data_files = []
for pth in src_dir.glob("**/*.*"):
    data_files.append(str(pth.relative_to(src_dir)))


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
    {%- if src.namespace is not none %}
    {% if src.namespace_method == 'setuptools' -%}
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
        {% for dep in reqs.requirements('install') -%}
        {% if dep.is_pip(strict=False) -%}
        "{{ dep.fmt_pip_requirement() }}",
        {% endif -%}
        {%- endfor %}],
    tests_require=[
        {% for dep in reqs.requirements('test') -%}
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
