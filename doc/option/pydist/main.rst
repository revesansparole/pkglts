pydist
======

Add a 'setup.py' to your package to make it compliant with setuptools_. This
will allow an easy distribution of your package. Since this option requires most
basic options, it's a good proxy to add to a newly created package to avoid
multiple 'manage add -opt' commands.

Quick setup::

    (dvlpt)$ pmg add pydist
    > intended versions [27]:
    ...
    (dvlpt)$ pmg regenerate

.. _setuptools: https://pypi.python.org/pypi/setuptools
