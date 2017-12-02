Install
=======

Download sources and use setup::

    $ python setup.py install
    or
    $ python setup.py develop

{% if 'pypi' is available %}
Use pip to install this package::

    $ pip install {{ base.pkgname }}

{% endif %}
Use
===

Simple usage:

.. code-block:: python

    from {{ base.pkg_full_name }} import *

{% if 'github' is available or 'gitlab' is available%}
Contribute
==========

Fork this project on {% if 'github' is available %}github_{% elif 'gitlab' is available %}gitlab_{% endif %}

{% if 'github' is available %}
.. _github: {{ github.url }}
{% elif 'gitlab' is available %}
.. _gitlab: {{ github.url }}
{% endif %}

{% endif %}

Acknowledgments
===============
