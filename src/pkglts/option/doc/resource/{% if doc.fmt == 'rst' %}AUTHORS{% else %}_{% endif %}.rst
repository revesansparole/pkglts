=======
Credits
=======

Development Lead
----------------

.. {# pkglts, doc.authors

{% for name, email in base.authors -%}
* {{ name }}, <{{ email }}>
{% endfor %}
.. #}

Contributors
------------

.. {# pkglts, doc.contributors
{% if 'git' is available %}
{% for name, email in git.contributors -%}
* {{ name }} <{{ email }}>
{% endfor %}
{%- else %}
None yet. Why not be the first?
{% endif %}
.. #}
