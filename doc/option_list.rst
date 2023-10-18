===================================
List of currently available options
===================================

Basic
=====

Basic options help you organize your code and provide core 'good practices'
functionality in your package.

.. toctree::
   :maxdepth: 1

   option/base/main
   option/test/main
   option/doc/main
   option/license/main
   option/version/main
   option/git/main

Extended
========

Based on the previous options, a few tools make your life easier and extend
basic functionalities.

.. toctree::
   :maxdepth: 1

   option/sphinx/main
   option/notebook/main
   option/data/main

Distributing your code
======================

The base of distributing your code comes with:

.. toctree::
   :maxdepth: 1

   option/pysetup/main


In order to make your package easily accessible for others, these options help
you host your code on a distant server:

.. toctree::
   :maxdepth: 1

   option/github/main
   option/gitlab/main


These options help you organize the structure to be PyPi_ ready:

.. toctree::
   :maxdepth: 1

   option/coverage/main
   option/tox/main
   option/flake8/main

Then you can use the 'pypi' option to help you put your package on the cheese shop:

.. toctree::
   :maxdepth: 1

   option/pypi/main

Alternatively, if you chose to use 'conda' as your package manager:

.. toctree::
   :maxdepth: 1

   option/conda/main


Web services
============

Once your code is registered on GitHub_, a set of options helps you benefit from
already developed online tools:

.. toctree::
   :maxdepth: 1

   option/travis/main
   option/readthedocs/main
   option/landscape/main
   option/lgtm/main
   option/coveralls/main
   option/requires/main

External options
================

Options developed for specific purposes. Why not consider adding your option? You can easily
customize  `pkglts` for your very own purpose by creating a plugin. The `plugin_project`
option allow you to easily create such package for extending `pkglts`.

.. toctree::
   :maxdepth: 1

   option/plugin_project/main


.. _GitHub: https://github.com/
.. _PyPi: https://pypi.python.org/pypi
