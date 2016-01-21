base
====

Add some base functionality to a package, i.e.:

 - a src directory to store python files
 - some basic meta information like owner name and package name

Modifications
-------------


If namespace is None:

.. raw:: html
    :file: modifications.html

else:

.. raw:: html
    :file: modifications_namespace.html


Quick tutorial
--------------

Follow these steps for a quick setup::

    (dvlpt)$ pmg add base

Edit your package config file ('pkg_cfg.json' in ".pkglts" directory at the root
of your package) using your favorite json editor (a normal text editor will do).

.. code-block:: javascript

    {
        "_pkglts": {
            "auto_install": true,
            "install_front_end": "stdout",
            "use_prompts": false
        },
        "base": {
            "namespace": null,
            "owner": "moi",
            "pkgname": "name"
        }
    }

Do not change sections starting with "_" (e.g. '_pkglts'), they are private sections
used by pkglts as configuration. Change owner for your own name and "pkgname" for
the name of your package (by default this one must be the name of the directory
in which you started to code).

.. code-block:: javascript

    "base": {
        "namespace": null,
        "owner": "revesansparole",
        "pkgname": "mypkg"
    }

Then::

    (dvlpt)$ pmg regenerate
