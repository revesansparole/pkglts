nbcompile
=========

Transform notebooks into restructured texts ready for inclusion in sphinx documentation.

Modifications
-------------


This tool will parse all notebook files (`*.ipynb`) in src_directory as specified
in the 'notebook' option (default : "example") to RestructuredText (.rst) format.
Each rst file produced is writen in "doc/_notebook" folder reproducing the
hierarchy of files found in src_directory. An 'index.rst' file is also generated
to list all the notebooks.

Quick tutorial
--------------

Just call the tool at the root of your package::

    (dvlpt)$ pmg nbcompile

Include a reference to the generated 'index.rst' file somewhere in your documentation,
presumably in a table of content block, if not done already. Then recompile your
documentation::

    (dvlpt)$ python setup.py build_sphinx

