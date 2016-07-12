notebook
========

This option allows to convert all notebooks (.ipynb) specified in the
src_directory parameter of the 'notebook' option (default : "example") to
RestructuredText (.rst) format.

Each rst file produced is writen in "doc/_notebook" folder reproducing the
hierarchy of files found in src_directory. An 'index.rst' file is also generated
to list all the notebooks.

Command line
------------

.. code::

    (dvlpt)$ pmg rg notebook

Then you need to rebuild the documentation to integrate the notebooks:

.. code::

    (dvlpt)$ python setup.py build_sphinx
