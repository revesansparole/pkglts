============
Installation
============

Use virtual environments::

    $ virtualenv 'myenv'
    $ myenv/scripts/activate
    (myenv) $ pip install pkglts


Alternatively download source code, cd into root directory and install in editable mode::

    (myenv) $ cd pkglts
    (myenv) pkglts $ pip install -e .

or conda_ environments::

    $ conda create -n toto pkglts -c defaults -c revesansparole -c conda-forge

If you already have an existing environment 'toto'::

    $ activate toto
    (toto) $ pip install pkglts

    $ activate toto
    (toto) $ conda install pkglts -c defaults -c revesansparole -c conda-forge

.. _conda: https://conda.io/miniconda.html