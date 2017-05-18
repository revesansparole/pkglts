license
=======

Use the same approach than the dead project lice_ to add a license to your package.
The name of the license is case insensitive (i.e. CeCILL-C and cecill-c refer to
the same license in the end).

Quick setup::

    (dvlpt)$ pmg add license

.. code-block:: javascript

    "license": {
        "name": "CeCILL-C",
        "organization": "organization name",
        "project": "{{key, base.pkgname}}",
        "year": "2015"
    }

Then::

    (dvlpt)$ pmg regenerate


Modifications
-------------

.. raw:: html
    :file: modifications.html

The list of templates for all available licenses in former project lice_ can be
found here_. They have been copied and extended into this project.
Available licenses:

.. toctree::
   :maxdepth: 1

   license_list

.. _here: https://github.com/licenses/license-templates/tree/master/templates
.. _lice: https://github.com/licenses/lice
