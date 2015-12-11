"""List data in current directory and sub package
"""

from os import listdir
from os.path import dirname, splitext
from os.path import join as pj


loc_dir = dirname(__file__)


def list_data():
    """Iterate on all files in current directory and sub directory
    that are not python files.
    """
    for fname in listdir(loc_dir):
        if splitext(fname)[1] not in (".py", ".pyc", ".pyo"):
            yield fname

    for fname in listdir(pj(loc_dir, "sub")):
        if splitext(fname)[1] not in (".py", ".pyc", ".pyo"):
            yield pj("sub", fname)
