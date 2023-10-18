sphinx
======

Extend basic documentation to use the sphinx_ set of tools. This option will use
the theme set in the `.pkglts/pkg_cfg.json` file to compile the doc. The theme by
default is 'default' instead of 'classic' to ensure that the right theme
will be selected on readthedocs_. If the 'autodoc_dvlpt' parameter is set to True,
then docstrings will also be compiled.

Modifications
-------------

.. raw:: html
    :file: modifications.html


Quick tutorial
--------------

Follow these steps to build your first comprehensive documentation. I assume
you also install the attached example files::

    (dvlpt)$ pmg add sphinx
    (dvlpt)$ pmg rg
    (dvlpt)$ pmg example sphinx

Then, you simply need to run the make command from the doc directory::

    (dvlpt)$ cd doc
    (dvplt) doc$ make

This will produce a build directory with a set of html pages in 'build/sphinx'.
Open the 'index.html' file in the 'html' sub directory to access the main index.
Alternatively you'll find another 'index.html' file in the 'docexample' directory
that provide examples of sphinx extensions usage.

.. _readthedocs: http://docs.readthedocs.org/en/latest/index.html
.. _sphinx: http://sphinx-doc.org/
