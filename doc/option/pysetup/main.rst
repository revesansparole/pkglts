pysetup
=======

Add a 'setup.py' to your package to make it compliant with setuptools_. This
will allow an easy distribution of your package. Since this option requires most
basic options, it's a good proxy to add to a newly created package to avoid
multiple 'manage add opt' commands.

Quick setup::

    (dvlpt)$ pmg add pysetup
    > intended versions [27]:
    ...
    (dvlpt)$ pmg rg

Modifications
-------------

.. raw:: html
    :file: modifications.html

Requirements files
------------------

Requirements for your projects are stored in your config in order to generate
two requirements files:

    - "requirements.txt" that contains all the requirements to use your package,
      play the examples, run the tests and compile the documentation.
    - "requirements_minimal.txt" that contains the bare minimal requirements to
      use your package. Think of it as the minimal requirements that will be used
      on a production server for example.

.. _setuptools: https://pypi.python.org/pypi/setuptools
