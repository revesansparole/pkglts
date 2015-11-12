readthedocs
===========

You've built your documentation using :doc:`../sphinx/main`, It looks perfect! Now maybe the right
time to use the ReadTheDocs_ web service to perform this task automatically and
expose your documentation to the rest of the world.

This option add the relevant files to expose your package to ReadTheDocs_, a web
service that will automatically compile and store your documentation. You still
need to perform the registration by hand. Look at :doc:`readthedocs_tutorial` for
a step by step guide::

    (dvlpt)$ pmg add readthedocs
    (dvlpt)$ pmg regenerate

    $ git add --all
    $ git commit -m"added readthedocs support"
    $ git push

.. _ReadTheDocs: https://readthedocs.org/
