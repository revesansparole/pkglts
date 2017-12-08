
Example of 'inheritance-diagram' usage
======================================

see `inheritance extension page`_ for more documentation.

Construct inheritance diagram for objects passed as arguments (require graphviz).

.. inheritance-diagram:: {{ base.pkg_full_name }}.example_inheritance1 {{ base.pkg_full_name }}.example_inheritance2.Node2

Same diagram without the package name prepended

.. inheritance-diagram:: {{ base.pkg_full_name }}.example_inheritance1 {{ base.pkg_full_name }}.example_inheritance2.Node2
    :parts: 2

Same diagram with just the class names

.. inheritance-diagram:: {{ base.pkg_full_name }}.example_inheritance1 {{ base.pkg_full_name }}.example_inheritance2.Node2
    :parts: 1

.. _`inheritance extension page`: http://www.sphinx-doc.org/en/stable/ext/inheritance.html
