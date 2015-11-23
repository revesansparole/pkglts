from os import mkdir
from os.path import dirname, exists
from shutil import rmtree
from time import sleep


def ensure_created(dname):
    if not exists(dname):
        mkdir(dname)


def rmdir(dname):
    for i in range(5):
        if exists(dname):
            try:
                rmtree(dname)
                return
            except OSError:
                sleep(0.1)
        else:
            return

    raise OSError("unable to remove directory: %s" % dname)


def ensure_path(pth):
    dname = dirname(pth)
    if not exists(dname):
        ensure_path(dname)
        mkdir(dname)
