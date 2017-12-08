
Example of 'graphviz' usage
===========================

see `graphviz extension page`_ for more documentation.

A small graph must be displayed after this:

.. graphviz::
   
    digraph foo {
        "bar" -> "baz"
    }

A bigger one after this:

.. graphviz:: workflow.dot


.. _`graphviz extension page`: http://www.sphinx-doc.org/en/stable/ext/graphviz.html
