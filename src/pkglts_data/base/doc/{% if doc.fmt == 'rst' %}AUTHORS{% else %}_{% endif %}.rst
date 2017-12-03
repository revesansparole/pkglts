.. {# pkglts, doc
Credits
=======

Development Lead
----------------

{% for name, email in base.authors -%}
* {{ name }}, <{{ email }}>
{% endfor %}

Contributors
------------

{% if 'github' is available -%}
{% for contributor in github.contributors -%}
* {{ contributor }}
{% endfor %}
{% endif %}
.. #}
{% if 'github' is not available -%}
None yet. Why not be the first?
{% endif %}
