landscape
=========

You've run the 'flake8' command after installing the :doc:`../flake8/main` option
and you don't have that many complains. Maybe now is a good time to automate the
process to keep track of how your code improve over time.

This option add the relevant files to expose your package to Landscape_io_, a web
service that will automatically check the compliance of your code with PEP8_
recommendations. This option install local configuration files but you still need
to register by hand. Have a look at the `Landscape Documentation`_ or
:doc:`landscape_tutorial` tutorial for more information::

    (dvlpt)$ pmg add landscape
    (dvlpt)$ pmg rg

    $ git add --all
    $ git commit -m"added landscape.io support"
    $ git push


Modifications
-------------

.. raw:: html
    :file: modifications.html


.. _Landscape_io: https://landscape.io/
.. _PEP8: https://www.python.org/dev/peps/pep-0008/
.. _`Landscape Documentation`: https://docs.landscape.io/
