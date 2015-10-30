version
=======

Simple versioning system for your package. Use of a generated 'version.py' file
to store the '__version__' attribute of your package::

    (dvlpt)$ manage add -opt version
    > auto [off]
    ....
    (dvlpt)$ manage regenerate

By default, the system keep track of a version number major.minor.post. Each number
needs to be entered manually with a call to edit option::

    (dvlpt)$ manage edit -opt version
    > auto [off]
    > major [0]:
    ...
    (dvlpt)$ manage regenerate

.. note:: Experimental:
          If your package is hosted on github you can set this option to
          go and fetch these numbers automatically each time you regenerate your
          package.
