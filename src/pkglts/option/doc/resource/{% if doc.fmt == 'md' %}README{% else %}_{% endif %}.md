# {{ base.pkg_full_name }}

[//]: # ({# pkglts, doc)
{% for badge in doc.badges -%}
{{ badge.format(doc.fmt) }}
{% endfor %}

[//]: # (#})

{{ doc.description }}

