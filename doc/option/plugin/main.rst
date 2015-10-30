plugin
======

This option will search your package for specific objects (i.e. plugins as defined
in openalea_), cache them in a specific 'yourpkg_plugin' folder and expose them
through the entry points mechanism. Plugins can then be discovered later
without importing any function in your module, speeding up the parsing process.

Have a look at the provided examples associated with this option for more information.

Alternatively, the :doc:`plugin_tutorial` tutorial will guide you through all the
steps to define your own plugins.

.. _openalea: http://openalea.gforge.inria.fr/wiki/doku.php?id=documentation:documentation
