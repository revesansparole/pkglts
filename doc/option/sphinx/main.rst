sphinx
======

Extend basic documentation to use the sphinx_ set of tools.

Quick tutorial
--------------

Follow these steps to build your first comprehensive documentation. I assume
you already installed the :doc:`../test/main` option and attached example files::

    (dvlpt)$ pmg add sphinx
    (dvlpt)$ pmg regenerate

If you already installed the :doc:`../pysetup/main` option::

    (dvlpt)$ python setup.py build_sphinx

will produce a set of html pages in 'build/sphinx'. Open the 'index.html' file in
the 'html' sub directory to access the main index.

If you don't want to install the :doc:`../pysetup/main` option, you simply need to
run the make command from the doc directory::

    (dvlpt)$ cd doc
    (dvplt) doc$ make

This will produce a build directory with the same architecture as explained
above.

.. _sphinx: http://sphinx-doc.org/
