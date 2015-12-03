"""Pip front end to install package in current environment.
"""
import imp
import pip
from pip import get_installed_distributions
from pip import main as pip_install


def installed_packages():
    """Iterate on all packages installed in the current python environment.

    return:
        (iter of str)
    """
    pip.utils.pkg_resources = imp.reload(pip.utils.pkg_resources)
    for p in get_installed_distributions():
        yield p.project_name


def install(name):
    """Install a package in the current python environment.

    arg:
     - name (str): name of the package

    return:
     - (bool): whether installation was successful or not
    """
    pip_install(['install', name])
