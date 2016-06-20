.. include:: ../README.rst

Upgrade Package Structure
=========================

Packages generated with Package Builder contains three different types of files:

 - 'pkg_cfg.json', a resource file that contains the information you entered
   at some stage during the configuration phase of adding an option.
 - generated files, susceptible to be regenerated at any time or with version
   change and not meant to be modified by user. These files are generated
   automatically by the package builder using templates provided with the package.
 - developer data and modules edited by hand which contains the actual python
   code of the package independently of the structure of the package. pkglts_git_
   will never touch them. If they conflict with some files used by a newly
   added option, the user will be prompted and will have to solve the conflict
   to install the option.

A call to the 'update' command will check for new versions of the package or any
available option::

    (dvlpt)toto$ pmg update

This command requires an internet connection since local installation will be
compared to current code on github.

If a newer version exists, you will be prompted for installation. After a successful
installation you will be prompted for new arguments if the configuration of one
of your installed options was upgraded in the process.

If update is successful, a call to regenerate is mandatory to rebuilt the package
structural files::

    (dvlpt)toto$ pmg regenerate

This phase will never overwrite any files you modified or created. You'll be prompted
in case of conflicts but it is your responsibility to solve them and relaunch the
command.

.. _pkglts_git: https://github.com/revesansparole/pkglts

.. _pkg_struct_func:

Add Package Structure Functionality
===================================

Package Builder provide a set of options to introduce new functionality to an
already existing package:

 - :doc:`option/base/main`: base option, basic package management
 - :doc:`option/license/main`: will help the developer to choose a license and add the relevant
   files
 - :doc:`option/doc/main`: Add some documentation to your package
 - :doc:`option/test/main`: basic unitests using Nose_
 - :doc:`option/coverage/main`: add code coverage_ to the basic test configuration
 - :doc:`option/pysetup/main`: make your package distributable with setuptools (i.e. setup.py)
 - :doc:`option/data/main`: will guide through all the steps to add non python files to a package
 - :doc:`option/github/main`: will guide through all the step to safely store the package on Github_
 - :doc:`option/readthedocs/main`: step by step guide to have your documentation on ReadTheDocs_
 - :doc:`option/travis/main`: will guide through all the steps to compile the code on Travis-CI_
 - :doc:`option/tox/main`: defines config files to use multi environment testing, Tox_
 - :doc:`option/flake8/main`: install and config Flake8_ tools to check for code compliance to PEP8_
   guidelines.
 - :doc:`option/pypi/main`: step by step guide and configuration to upload package on PyPi_.

.. _Travis-CI: http://travis-ci.org/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _ReadTheDocs: https://readthedocs.org/
.. _Github: https://github.com/
.. _Nose: https://nose.readthedocs.org/en/latest/
.. _coverage: https://pypi.python.org/pypi/coverage
.. _Flake8: https://pypi.python.org/pypi/flake8
.. _PyPi: https://pypi.python.org/pypi
.. _PEP8: https://www.python.org/dev/peps/pep-0008/

Install a new option
--------------------

To install a new option call the 'add' action::

    (dvlpt)toto$ pmg add license

The script will perform different tasks sequentially:

 - Check if this option requires other options in order to be installed:
   e.g. the 'pysetup' option requires all 'base, 'doc', 'test', 'license' and 'version'
   in order to run properly.
 - Check if this option requires some extra packages in order to setup:
   e.g. the 'license' option depends on the lice_ package to function properly.
 - Run a basic config script to ask you for specific details relative to this option
   e.g. the 'license' option will ask for the license name.


.. note:: Nothing will be installed without your consent

Multiple call to add options can be serialized but you explicitly needs to call
regenerate to see the action of the new options on your package::

    (dvlpt)toto$ pmg regenerate


.. _lice: https://github.com/licenses/lice

Install example files
---------------------

Some options come with example files that can be installed with the special
directive::

    (dvlpt)toto$ pmg example test


The files will be directly installed without the need to a regenerate call. You
can reinstall them at any time (you'll be prompted for action if conflicts occur).

Edit an option
--------------

You can simply edit an option (e.g. license) by running the command::

    (dvlpt)toto$ pmg edit license

You'll be re-prompted for the values of arguments of this option with default to
previously entered values.

Extra services
==============

.. warning:: Work In Progress

Package Builder also provides a few useful services to check that the python
modules follow code best practices:

 - 'add_object': will create a new python module with the proper headers and
   a skeleton of a python class.
 - 'add_plugin': will wrap a given python class into a usable plugin_.
 - 'add_script': will wrap a given python functionality into a command line
   script.
 - 'reset_file_header': will loop through all python modules and try to rewrite
   file header to match current best practices.
 - fmt_doc: check code documentation and format it according to given standard
   if possible. Requires some already good documentation, just a quick fix to
   pass from one style to another (e.g. google to numpy).

.. _plugin: openalea.plugin

Contributing
============

You can contribute to this package by:

 - improving the documentation
 - correcting some bugs
 - closing a few issues
 - implementing a new option to add a new functionality to package structures


.. :begin_links_section:
.. _base: http://pkglts.readthedocs.org/en/latest/option/base/main.html
