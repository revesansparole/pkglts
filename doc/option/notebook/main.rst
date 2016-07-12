notebook
========

This option allow to convert recursively each notebook (.ipynb) specified in the
src_directory parameters of notebook option (default : "example") to rst format.

After that, each rst file is write in "doc/_notebook" folder. (The previous
files organization is kept in this folder). More, a index.rst is generated,
referencing all the rst file generated.

Command line
------------

.. code::

    (dvlpt)$ pmg rg notebook
