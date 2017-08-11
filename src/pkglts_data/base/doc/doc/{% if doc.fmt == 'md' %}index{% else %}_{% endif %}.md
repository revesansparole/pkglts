# Welcome to {{ base.pkg_full_name }}'s documentation!

## Contents

- [readme](../README.md)
- [installation](installation.md)
- [usage](usage.md)
{%- if 'notebook' is available %}
- [notebook](_notebook/index.md)
{%- endif %}
- [contributing](../CONTRIBUTING.md)
- [authors](../AUTHORS.md)
- [history](../HISTORY.md)

{% if 'sphinx' is available %}
{% if sphinx.autodoc_dvlpt %}
## Sources

[modules](_dvlpt/{{ base.pkgname }}.rst)

{% endif %}
{% endif %}


## Indices and tables

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
