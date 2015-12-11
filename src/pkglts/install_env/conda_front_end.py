"""Pip front end to install package in current environment.
"""
from json import loads
from subprocess import Popen, PIPE


def installed_packages():
    """Iterate on all packages installed in the current python environment.

    return:
        (iter of str)
    """
    p = Popen(["conda", "list", "--json"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate("")
    rc = p.returncode
    if rc != 0:
        raise UserWarning("unable to execute 'conda list'")

    for pkg in loads(output):
        yield pkg.split("-")[0]


def install(name):
    """Install a package in the current python environment.

    arg:
     - name (str): name of the package

    return:
     - (bool): whether installation was successful or not
    """
    p = Popen(["conda", "install", name], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    p.communicate("")
    rc = p.returncode
    return rc == 0
