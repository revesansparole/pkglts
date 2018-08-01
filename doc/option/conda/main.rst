conda
=====

Install a Conda_ recipe in the package to generate Conda_ packages. Additionally,
this option also propose two requirements files stored along the recipe in the conda
directory which use the conda syntax to install the requirements instead of a
simple list as in 'requirements.txt'. The main benefit is to allow to install
both 'conda' dependencies and 'pip' dependencies with the same command::

    (myenv) $ conda env update --file conda/requirements.yml


Modifications
-------------

.. raw:: html
    :file: modifications.html



.. _Conda: http://conda.pydata.org/docs/intro.html
