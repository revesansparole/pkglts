plugin_project
==============

Create a scaffold to write a plugin for `pkglts`

Modifications
-------------


If namespace is None:

.. raw:: html
    :file: modifications.html


Quick tutorial
--------------

Follow these steps for a quick setup that will create a plugin called **plugin_name**::

    (dvlpt)$ mkdir plugin_name
    (dvlpt)$ cd plugin_name
    (dvlpt) \plugin_name\$ pmg init plugin_project

Edit your package config file ('pkg_cfg.json' in ".pkglts" directory at the root
of your package) using your favorite json editor (a normal text editor will do).

Do not change sections starting with "_" (e.g. '_pkglts'), they are private sections
used by pkglts as configuration. Change owner for your own name and "pkgname" for
the name of your plugin (by default this one must be the name of the directory
in which you started to code).

Then::

    (dvlpt) \plugin_name\$ pmg rg

If you want your plugin to generate some files, you can install an example of them using::

    (dvlpt) \plugin_name\$ pmg example plugin_project
