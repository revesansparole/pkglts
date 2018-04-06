# {# pkglts, test.pytest
import os


def pytest_cmdline_preparse(args):
    {% if 'coverage' is available -%}
    if 'PYCHARM_HOSTED' not in os.environ:
        args.append("--cov={{ base.pkg_full_name }}")
    {% else %}
    pass
    {%- endif %}

# #}
