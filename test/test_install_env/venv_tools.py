import os
from os import mkdir
from os.path import exists
from shutil import rmtree
from subprocess import call
import sys
from time import sleep


def _activate(name):
    """Internal function used to activate a virtualenv
    """
    if "win" in sys.platform:
        pth = "%s/Scripts/activate_this.py" % name
    else:
        pth = "%s/bin/activate_this.py" % name

    try:  # python27
        execfile(pth, dict(__file__=pth))
    except NameError:  # python3.x
        with open(pth) as f:
            code = compile(f.read(), pth, 'exec')
            exec(code, dict(__file__=pth))


def create_venv(name, mem):
    """Create a new virtualenv with given name and activate it

    .. warning: create a directory with given name in local dir

    ..warning: erase the content of dir 'name' before creating virtualenv

    args:
     - name (str): name of virtualenv to create
     - mem (dict): a place to store values that will be modified
    """
    try:
        if exists(name):
            rmtree(name)
        else:
            mkdir(name)
    except OSError:
        print("unable to create dir")
        sys.exit(0)

    call("virtualenv %s" % name, shell=True)

    # Save state of path
    mem["sys.path"] = tuple(sys.path)
    mem["os.environ['PATH']"] = str(os.environ["PATH"])

    _activate(name)


def clear_venv(name, mem):
    """Remove virtualenv from existence.

    args:
     - name (str): name of virtualenv
     - mem (dict): a place of values that where modified
    """
    # Restore state
    del sys.path[:]
    for item in mem["sys.path"]:
        sys.path.append(item)

    os.environ["PATH"] = str(mem["os.environ['PATH']"])

    # remove directory
    for i in range(5):
        if exists(name):
            try:
                rmtree(name)
                return
            except OSError:
                sleep(0.1)
        else:
            return

    raise OSError("unable to remove directory: %s" % name)
