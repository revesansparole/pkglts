============
Installation
============

Download source then, at the command line::

    $ python setup.py


Alternatively the command line::

    $ easy_install pkglts

Or::

    $ pip install pkglts

Preferred method use virtual environments::

    $ virtualenv 'myenv'
    $ myenv/scripts/activate
    (myenv)$ pip install pkglts


or conda_ environments::

    $ conda create -n toto pkglts -c defaults -c revesansparole -c conda-forge

If you already have an existing environment 'toto'::

    $ activate toto
    (toto) $ pip install pkglts

    $ activate toto
    (toto) $ conda install pkglts -c defaults -c revesansparole -c conda-forge

.. _conda: https://conda.io/miniconda.html