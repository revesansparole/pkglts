coveralls
=========

Travis-CI_ is automatically rebuilding and testing your code every time you push
your modifications on GitHub. The :doc:`../coverage/main` option let you test
your code coverage locally. Now, if you want to get your code coverage with
every Travis-CI_ build, Coveralls_io_ is the right tool for you.

This option add the relevant files to let your package use Coveralls_io_, a web
service that will automatically check the test coverage of your code. This option
install local configuration files but you still need to register by hand. Have a
look at the `Coveralls Documentation`_ or :doc:`coveralls_tutorial` tutorial for
more information::

    (dvlpt)$ pmg add coveralls
    (dvlpt)$ pmg rg

    $ git add --all
    $ git commit -m"added coveralls support"
    $ git push


.. _Coveralls_io: https://coveralls.io/
.. _`Coveralls Documentation`: https://coveralls.zendesk.com/hc/en-us
.. _Travis-CI: http://travis-ci.org/
