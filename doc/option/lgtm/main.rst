lgtm
====

This option add the relevant files to let your package use lgtm_, a web service
that will extend pylint_ and check on the validity of your code. This option
install local configuration files but you still need to register by hand. Have a
look at the `Lgtm Documentation`_::

    (dvlpt)$ pmg add lgtm
    (dvlpt)$ pmg rg

    $ git add --all
    $ git commit -m"added lgtm support"
    $ git push


.. _lgtm: https://lgtm.com/
.. _`Lgtm Documentation`: https://lgtm.com/help/lgtm/about-lgtm
.. _pylint: https://www.pylint.org/
