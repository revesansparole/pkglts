
Example of 'ifconfig' usage
===========================

see `ifconfig extension page`_ for more documentation.

Include content based on configuration.

.. ifconfig:: keep_warnings

   This stuff is only included if the parameter 'keep_warnings' is True.

.. ifconfig:: not keep_warnings

   This stuff is only included if the parameter 'keep_warnings' is False.

.. _`ifconfig extension page`: http://www.sphinx-doc.org/en/stable/ext/ifconfig.html
