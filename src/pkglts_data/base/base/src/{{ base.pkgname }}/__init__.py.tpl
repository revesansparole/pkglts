# {# pkglts, base
{% if 'version' is available %}
from . import version

__version__ = version.__version__
{% endif %}
# #}
