
Example of 'intersphinx' usage
==============================

see `intersphinx extension page`_ for more documentation.

Usage is simple: whenever Sphinx encounters a cross-reference that has no matching target in the current documentation set, it looks for targets in the documentation sets configured in intersphinx_mapping. A reference like `:py:class:`zipfile.ZipFile`` (:py:class:`zipfile.ZipFile`) can then link to the Python documentation for the ZipFile class, without you having to specify where it is located exactly.

.. _`intersphinx extension page`: http://www.sphinx-doc.org/en/stable/ext/intersphinx.html
