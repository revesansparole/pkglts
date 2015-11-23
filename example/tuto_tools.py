from os import chdir, getcwd, mkdir
from os.path import exists
from shutil import rmtree
from subprocess import call
import sys
from sys import argv


pkg_dir = "pkg_tata"
venv_dir = "venv_toto"


def activate_venv():
    execfile("%s/Scripts/activate_this.py" % venv_dir,
             dict(__file__="%s/Scripts/activate_this.py" % venv_dir))


def create_venv(install_extra):
    try:
        if exists(venv_dir):
            rmtree(venv_dir)

    except OSError:
        print("unable to create dir")
        sys.exit(0)

    call("virtualenv %s" % venv_dir, shell=True)

    # install requirements from local depot
    activate_venv()
    if install_extra:
        reqs = ["nose", "coverage", "mock", "tox", "lice", "github3.py",
                "flake8", "sphinx"]
        for name in reqs:
            call("pip install --no-index --find-links=wheels %s" % name)


def initialize(install_extra=True):
    # parse arguments

    # clean previous build
    try:
        if exists(pkg_dir):
            rmtree(pkg_dir)

        mkdir(pkg_dir)
    except OSError:
        print("unable to create dir")
        sys.exit(0)

    # generate virtual env for this session
    if len(argv) > 2:
        create_venv(install_extra)
    else:
        activate_venv()

    # install new version of package
    cwd = getcwd()

    # install pkglts
    if len(argv) > 1:
        chdir("..")
        call("python setup.py %s" % argv[1], shell=True)

    # generate new package
    chdir(cwd + "/" + pkg_dir)

    call("pmg init")


def rg():
    """Regenerate package
    """
    call("pmg rg")
