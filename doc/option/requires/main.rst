requires
========

requires_io_ is a web service that scan your code every time you push on GitHub_,
detect all your dependencies and check wether they are still up to date.

This option add the relevant files to let your package use requires_io_. This
option install local configuration files but you still need to register your
project by hand. Have a look at the `Requires.io Documentation`_ or
:doc:`requires_tutorial` tutorial for more information::

    (dvlpt)$ pmg add requires
    (dvlpt)$ pmg regenerate

    $ git add --all
    $ git commit -m"added requires support"
    $ git push


.. _GitHub: https://github.com/
.. _requires_io: https://requires.io/
.. _`Requires.io Documentation`: https://requires.io/features/
