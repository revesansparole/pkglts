At it simplest, a Python_ package is a mere directory with a '__init__.py' file
in it. However, this basic structure needs to be augmented as soon as more
functionality is required: i.e. create a distribution, write a comprehensive
documentation, run some tests. With time the structure of a package grows and
include more and more description files (e.g. setup.py, .gitignore, ...).

The rationale behind the creation of this 'package builder' is to keep the life
of a python programmer as easy as possible by providing two core functions:

 - a way to add more functionality to an existing package
 - a way to keep the package structure up to date with currently known best
   practices.

.. _Python: http://python.org

Quick start
===========

Create a virtual environment for development::

    $ virtualenv dvlpt

Activate it::

    $ dvlpt/Scripts/activate

Install pkglts_::

    (dvlpt)$ pip install pkglts

Create a directory for your package::

    (dvlpt)$ mkdir toto

Run 'manage' inside this directory::

    (dvlpt)$ cd toto
    (dvlpt)toto$ manage init
    (dvlpt)toto$ manage add -opt base
    (dvlpt)toto$ manage regenerate

This will create the bare basic minimum for a python package. Add more options
(see the 'Add Package Structure Functionality' below for more options) afterward.
Especially, since in the example above we just added the 'base' option that will
create a 'src' directory to put your code in it.

Upgrade Package Structure
=========================

Packages generated with Package Builder contains three different types of files:

 - 'pkg_cfg.json', a resource file that contains the information you entered
   at some stage during the configuration phase of adding an option.
 - generated files, susceptible to be regenerated at any time or with version
   change and not meant to be modified by user. These files are generated
   automatically by the package builder using templates provided with the package.
 - developer data and modules edited by hand which contains the actual python
   code of the package independently of the structure of the package. pkglts_
   will never touch them. If they conflict with some files used by a newly
   added option, the user will be prompted and will have to solve the conflict
   to install the option.

A call to the 'update' command will check for new versions of the package or any
available option::

    (dvlpt)toto$ manage update

This command requires an internet connection since local installation will be
compared to current code on github.

If a newer version exists, you will be prompted for installation. After a successful
installation you will be prompted for new arguments if the configuration of one
of your installed options was upgraded in the process.

If update is successful, a call to regenerate is mandatory to rebuilt the package
structural files::

    (dvlpt)toto$ manage regenerate

This phase will never overwrite any files you modified or created. You'll be prompted
in case of conflicts but it is your responsibility to solve them and relaunch the
command.

.. _pkglts: https://github.com/revesansparole/pkglts

.. _pkg_struct_func:

Add Package Structure Functionality
===================================

Package Builder provide a set of options to introduce new functionality to an
already existing package:

 - base: base option, basic package management
 - license: will help the developer to choose a license and add the relevant
   files
 - doc: Add some documentation to your package
 - test: basic unitests using Nose_
 - coverage: add code coverage_ to the basic test configuration
 - pydist: make your package distributable with setuptools (i.e. setup.py)
 - data: will guide through all the steps to add non python files to a package
 - github: will guide through all the step to safely store the package on Github_
 - readthedocs: step by step guide to have your documentation on ReadTheDocs_
 - travis: will guide through all the steps to compile the code on Travis-CI_
 - tox: defines config files to use multi environment testing, Tox_
 - flake8: install and config Flake8_ tools to check for code compliance to PEP8_
   guidelines.
 - pypi: step by step guide and configuration to upload package on PyPi_.

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

    (dvlpt)toto$ manage add -opt license

The script will perform different tasks sequentially:

 - Check if this option requires other options in order to be installed:
   e.g. the 'pydist' option requires all 'base, 'doc', 'test', 'license' and 'version'
   in order to run properly.
 - Check if this option requires some extra packages in order to setup:
   e.g. the 'license' option depends on the lice_ package to function properly.
 - Run a basic config script to ask you for specific details relative to this option
   e.g. the 'license' option will ask for the license name.


.. note:: Nothing will be installed without your consent

Multiple call to add options can be serialized but you explicitly needs to call
regenerate to see the action of the new options on your package::

    (dvlpt)toto$ manage regenerate


.. _lice: https://github.com/licenses/lice

Install example files
---------------------

Each option comes with some example files that can be installed with the special
directive::

    (dvlpt)toto$ manage add -opt example

You will be prompted for the name of the option of the files you want to install.

The files will be directly installed without the need to a regenerate call. They
have a special status in the sense that you can modify or even remove these files
without any complains next time you rebuild the package. You can also reinstall
them at any time (you'll be prompted for action if conflicts occur).

.. note:: If you want to avoid the interactive prompt you can use the extra args
          syntax. For example to add the example files associated with the base
          option::

          (dvlpt)toto$ manage add -opt example -e option_name base

Edit an option
--------------

You can simply edit an option (e.g. license) by running the command::

    (dvlpt)toto$ manage edit -opt license

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
