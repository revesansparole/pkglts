=======
Credits
=======

Development Lead
----------------

.. {# pkglts, doc_authors
{% for name, email in base.authors -%}
* {{ name }}, <{{ email }}>
{% endfor %}
.. #}

Contributors
------------

.. {# pkglts, doc_contributors
{% if 'github' is available -%}
{% for contributor in github.contributors -%}
* {{ contributor }}
{%- endfor %}
{%- else %}
None yet. Why not be the first?
{% endif %}
.. #}
