{% if 'doc' is available -%}
"""
{{ doc.description }}
"""
{% endif -%}
# {# pkglts, base
{% if 'version' is available %}
from . import version

__version__ = version.__version__
{% endif %}
# #}
