"""Simple front end to emulate all environment modification
by printing the required operations.
"""
from os import listdir
from os.path import basename, splitext
import sys


def installed_packages():
    """Iterate on all packages installed in the current python environment.

    .. warning: extremely simple implementation that list the content
                of site-packages only.

    return:
        (list of str)
    """
    for pth in sys.path:
        name = basename(pth)
        if name == "site-packages":
            for pkg in listdir(pth):
                pkgname, ext = splitext(pkg)
                if ext in ("", ".py", ".egg", ".egg-link"):
                    if "-" in pkgname:
                        pkgname = pkgname.split("-")[0]

                    yield pkgname


def install(name):
    """Install a package in the current python environment.

    arg:
     - name (str): name of the package

    return:
     - (bool): whether installation was successful or not
    """
    print("install %s" % name)
