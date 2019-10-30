======
pkglts
======

.. {# pkglts, doc


.. image:: https://coveralls.io/repos/github/revesansparole/pkglts/badge.svg?branch=master
    :alt: Coverage report status
    :target: https://coveralls.io/github/revesansparole/pkglts?branch=master


.. image:: https://readthedocs.org/projects/pkglts/badge/?version=latest
    :alt: Documentation status
    :target: https://pkglts.readthedocs.io/en/latest/?badge=latest


.. image:: https://travis-ci.org/revesansparole/pkglts.svg?branch=master
    :alt: Travis build status
    :target: https://travis-ci.org/revesansparole/pkglts


.. image:: https://landscape.io/github/revesansparole/pkglts/master/landscape.svg?style=flat
    :alt: Code health status
    :target: https://landscape.io/github/revesansparole/pkglts/master


.. image:: https://requires.io/github/revesansparole/pkglts/requirements.svg?branch=master
    :alt: Requirements status
    :target: https://requires.io/github/revesansparole/pkglts/requirements/?branch=master


.. image:: https://badge.fury.io/py/pkglts.svg
    :alt: PyPI version
    :target: https://badge.fury.io/py/pkglts


.. image:: https://ci.appveyor.com/api/projects/status/hrwjhn2oe0q4oaf2/branch/master?svg=true
    :alt: Appveyor build status
    :target: https://ci.appveyor.com/project/revesansparole/pkglts/branch/master
.. #}

.. image:: https://anaconda.org/revesansparole/pkglts/badges/version.svg
    :alt: Anaconda version
    :target: https://anaconda.org/revesansparole/pkglts

Building packages with long term support


.. image:: https://raw.githubusercontent.com/revesansparole/pkglts/master/avatar.png
    :align: right
    :width: 256px

The rationale behind the creation of this 'package builder' is to keep the life
of a python programmer as easy as possible by providing three core functions:

 - A way to add more functionality to an existing package.
 - A way to keep the package structure up to date with currently known best
   practices.
 - Remove repetitive tasks that can be automated from the list of things to do.

.. _Python: http://python.org

Quick start
===========

Create a virtual environment for development::

    $ virtualenv dvlpt

Activate it::

    $ (on windows)dvlpt\Scripts\activate
    $ (on linux)dvlpt/bin/activate

Install pkglts_::

    (dvlpt)$ pip install pkglts

Create a directory for your package::

    (dvlpt)$ mkdir toto

Run 'manage' inside this directory::

    (dvlpt)$ cd toto
    (dvlpt)toto$ pmg init
    (dvlpt)toto$ pmg add base
    (dvlpt)toto$ pmg regenerate

This will create the bare basic minimum for a python package. Add more options
(see the add_option_ for more options) afterward. Especially, since in the example
above we just added the 'base' option that will create a 'src' directory to put
your code in it.

.. _pkglts: https://pypi.python.org/pypi/pkglts/
.. _add_option: https://pkglts.readthedocs.org/en/latest/option_list.html

Documentation
=============

More documentation can be found on readthedocs_pkglts_. If you just intend to use this package
you can start with some tutorials_. However, if the core functionality are
not sufficient and you want to be part of the development you might be interested
with the developer_ section of the doc.


.. _readthedocs_pkglts: https://pkglts.readthedocs.org/en/latest
.. _tutorials: https://pkglts.readthedocs.org/en/latest/tutorials.html
.. _developer: https://pkglts.readthedocs.org/en/latest
