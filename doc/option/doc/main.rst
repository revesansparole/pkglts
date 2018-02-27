doc
===

Add some documentation in your package:

 - a brief description
 - readme headers
 - list of authors
 - history
 - contributing

The examples associated with this option provide a scaffold for a more complete
documentation in the doc directory:

 - a basic index file

Modifications
-------------

.. raw:: html
    :file: modifications.html

Configuration
-------------

You need to decide rapidly (aka before regenerating the package) the format you
intend to use to write the documentation:

 - Complete documentation of code, use the default 'rst' (only one that actually
   work with sphinx).
 - webpages (aka user oriented documentation), then you can use 'md'

Quick tutorial
--------------

Follow these steps to install this option and the associated files::

     (dvlpt)$ pmg add doc
     (dvlpt)$ pmg regenerate

Meaning of pieces of information
--------------------------------

Readme
******

Provided as an example file, a basic body for the readme file with different
sections depending on the installed options. The README.rst file is regenerated
automatically so out of reach. However, it simply add a few headers to a README_body
file located in the 'doc' directory. We encourage you to modify this file to suit
your needs.

Authors
*******

The author list is automatically generated from the author_name, author_email
information stored in the 'base' part of the package configuration.

If your package is stored on GitHub or Gitlab, the complete list of authors and
contributors will be retrieved from the website.

Contributing
************

An example file describing how people can contribute to the package is available
as an example::

    (dvlpt)$ pmg example doc

This file makes more sense if you already installed the 'github' or 'gitlab' option.

History
*******

History of your package is generated automatically from the github or gitlab
commit tags and messages if possible. See :doc:`history` for a tool
that will perform this operation.
