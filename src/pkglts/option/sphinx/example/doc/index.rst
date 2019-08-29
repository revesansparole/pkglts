Welcome to {{ base.pkg_full_name }}'s documentation!
====================================================

{%- if sphinx.gallery != "" %}
.. toctree::
   :caption: User's documentation
   :maxdepth: 2

   _gallery/index
{%- endif %}

{%- if sphinx.autodoc_dvlpt %}
.. toctree::
   :caption: Developper's documentation
   :maxdepth: 4

   Sources <_dvlpt/modules>
{%- endif %}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
