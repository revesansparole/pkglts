test
====

Simple testing facilities making extensive use of the nose_ extension. Two different
ways to run the tests, either through the setuptools call to setup.py::

    (dvlpt)$ python setup.py test

or through the use of the 'nosetests' command line argument::

    (dvlpt)$ nosetests

Have a look at nose_cmd_ for more information on the way to use nose_.

Quick tutorial
--------------

Follow these steps for a quick setup (do :doc:`../base/main` quick tutorial first
if you haven't done it yet)::

    (dvlpt)$ manage add -opt test
    (dvlpt)$ manage regenerate
    (dvlpt)$ manage add -opt example
    > option name [base]: test

    (dvlpt)$ nosetests

.. image:: test_nosetests_result.png

.. _nose: https://nose.readthedocs.org/en/latest/
.. _nose_cmd: http://nose.readthedocs.org/en/latest/usage.html
