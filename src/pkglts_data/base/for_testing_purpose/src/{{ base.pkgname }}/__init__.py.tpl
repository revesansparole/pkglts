# {# pkglts, base1
{% if 'version' is available %}
from . import version

__version__ = version.__version__
{% endif %}
# #}

# {# pkglts, base2
{% if 'github' is available %}
'github'
{% endif %}
# #}
