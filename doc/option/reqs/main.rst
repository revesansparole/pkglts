reqs
====

Add package requirements to your project.

Quick setup::

    (dvlpt)$ pmg add reqs
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

To help you keep track of your dependencies, you can use the :doc:`reqs_tool` tool
provided with this option.

.. _setuptools: https://pypi.python.org/pypi/setuptools
