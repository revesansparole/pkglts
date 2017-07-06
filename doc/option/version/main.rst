version
=======

Simple versioning system for your package. Use of a generated 'version.py' file
to store the '__version__' attribute of your package::

    (dvlpt)$ pmg version
    (dvlpt)$ pmg regenerate

By default, the system keep track of a version number major.minor.post. Each number
needs to be entered manually by editing the config file then regenerating the package.

.. note:: Experimental:
          If your package is hosted on github you can set this option to
          go and fetch these numbers automatically each time you regenerate your
          package.

Modifications
-------------

.. raw:: html
    :file: modifications.html

