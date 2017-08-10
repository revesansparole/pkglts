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

{% if 'github' is available %}
Contribute
==========

Fork this project on github_

.. _github: {{ github.url }}

{% endif %}

Acknowledgments
===============
