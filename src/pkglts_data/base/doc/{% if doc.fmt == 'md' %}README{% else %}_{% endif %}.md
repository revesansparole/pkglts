# {{ base.pkg_full_name }}

[//]: # ({# pkglts, doc)
{%- if 'readthedocs' is available %}
{{ readthedocs.badge }}
{% endif %}
{%- if 'travis' is available %}
{{ travis.badge }}
{% endif %}
{%- if 'coveralls' is available %}
{{ coveralls.badge }}
{% endif %}
{%- if 'landscape' is available %}
{{ landscape.badge }}
{% endif %}
{%- if 'pypi' is available %}
{{ pypi.badge }}
{% endif -%}
{%- if 'requires' is available %}
{{ requires.badge }}
{% endif -%}

[//]: # (#})

{{ doc.description }}

