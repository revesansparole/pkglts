sphinx
======

Extend basic documentation to use the sphinx_ set of tools. This option will use
the 'default' theme by default instead of 'classic' to ensure that the right theme
will be selected on readthedocs_.

Modifications
-------------

.. raw:: html
    :file: modifications.html


Quick tutorial
--------------

Follow these steps to build your first comprehensive documentation. I assume
you also install the attached example files::

    (dvlpt)$ pmg add sphinx
    (dvlpt)$ pmg regenerate
    (dvlpt)$ pmg example sphinx

If you already installed the :doc:`../pysetup/main` option::

    (dvlpt)$ python setup.py build_sphinx

will produce a set of html pages in 'build/sphinx'. Open the 'index.html' file in
the 'html' sub directory to access the main index. Alternatively you'll find
another 'index.html' file in the 'docexample' directory that provide examples
of sphinx extensions usage.

If you don't want to install the :doc:`../pysetup/main` option, you simply need to
run the make command from the doc directory::

    (dvlpt)$ cd doc
    (dvplt) doc$ make

This will produce a build directory with the same architecture as explained
above.

.. _readthedcos: http://docs.readthedocs.org/en/latest/index.html
.. _sphinx: http://sphinx-doc.org/
