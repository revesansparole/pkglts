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

Use the :doc:`nbcompile` tool provided with this option to recompile the notebooks
into restructured text files as explained above.

.. code::

    (dvlpt)$ pmg nbcompile

User Warnings
-------------

1. Each notebook need a title to be referenced in the index

Then you need to rebuild the documentation to integrate the notebooks:

.. code::

    (dvlpt)$ cd doc
    (dvlpt) doc $ make html

Example
-------

.. toctree::
   :maxdepth: 2

   ../../_notebook/index
