from os import mkdir
from os.path import exists
from shutil import rmtree
from subprocess import call
import sys
from time import sleep


def activate_venv(venv_dir):
    """Activate a virtualenv.

    args:
     - venv_dir (str): root directory of virtual env
    """
    execfile("%s/Scripts/activate_this.py" % venv_dir,
             dict(__file__="%s/Scripts/activate_this.py" % venv_dir))


def create_venv(name):
    """Create a new virtualenv with given name

    .. warning: create a directory with given name in local dir

    ..warning: erase the content of dir 'name' before creating virtualenv

    args:
     - name (str): name of virtualenv to create
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


def clear_venv(name):
    """Remove virtualenv from existence.

    args:
         - name (str): name of virtualenv
    """
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
