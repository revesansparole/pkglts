"""Pip front end to install package in current environment.
"""
import imp
import pip
## Dealing with pip 10.* api changes
## The solution is from:
## https://github.com/naiquevin/pipdeptree/blob/master/pipdeptree.py
try:
    from pip._internal import get_installed_distributions
except ImportError:
    from pip import get_installed_distributions
try:
    from pip._internal import main as pip_install
except:
    from pip import main as pip_install


def installed_packages():
    """Iterate on all packages installed in the current python environment.

    return:
        (iter of str)
    """
    pip.utils.pkg_resources = imp.reload(pip.utils.pkg_resources)
    for pjt in get_installed_distributions():
        yield pjt.project_name


def install(name):
    """Install a package in the current python environment.

    arg:
     - name (str): name of the package

    return:
     - (bool): whether installation was successful or not
    """
    pip_install(['install', name])
