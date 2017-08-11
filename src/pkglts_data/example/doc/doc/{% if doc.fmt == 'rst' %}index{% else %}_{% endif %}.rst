
Welcome to {{ base.pkg_full_name }}'s documentation!
====================================================

Contents:

.. toctree::
    :maxdepth: 2

    readme
    installation
    usage
{%- if 'notebook' is available %}
    _notebook/index
{%- endif %}
    contributing
    authors
    history

{% if 'sphinx' is available %}
{% if sphinx.autodoc_dvlpt %}
Sources
=======

.. toctree::
   :maxdepth: 2

   _dvlpt/modules
{% endif %}
{% endif %}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
