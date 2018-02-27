Add data tutorial
=================

Regenerating your package after adding the option 'data' will create a
'pkgname_data' in the 'src' directory::

    (dvlpt)$ pmg add data
    (dvlpt)$ pmg rg

Just copy all your data inside this directory and they will be packaged and
installed along your package whatever method you choose to distribute your package::

    (dvlpt)$ python setup.py sdist
    (dvlpt)$ python setup.py install
    (dvlpt)$ python setup.py develop
    (dvlpt)$ python setup.py bdist_egg

Accessing data from inside the code
-----------------------------------

The recommended way to access data would be to use package_resources_. However this
method fail. Depending on the way you distribute your code, the path to your data
will be changed. We choose a simple rough approach and, along the package_data
directory, the 'data' option also create a 'data_access.py' file in your sources.
To access 'data' you just need to call the 'get_data_dir' function and you'll
be returned with a valid pth to the package_data directory.

.. _package_resources: https://pythonhosted.org/setuptools/pkg_resources.html