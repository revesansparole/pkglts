from nose.tools import with_setup
from os import listdir, mkdir
from os.path import exists
from shutil import rmtree

from pkglts.manage import clean


print(__file__)

tmp_dir = 'toto_manage_clean'


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


@with_setup(setup, teardown)
def test_clean_remove_pyc_files():
    name = tmp_dir + "/" + "toto.pyc"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert not exists(name)


@with_setup(setup, teardown)
def test_clean_remove_pycache_directories():
    pycache = tmp_dir + "/" + "__pycache__"
    mkdir(pycache)
    name = pycache + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert not exists(pycache)
    assert not exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_remove_py_files():
    name = tmp_dir + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_remove_hidden_files():
    name = tmp_dir + "/" + ".toto.pyc"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_explore_hidden_directories():
    hidden = tmp_dir + "/" + ".test"
    mkdir(hidden)
    name = hidden + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(hidden)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_do_not_explore_clean_no_directories():
    hidden = tmp_dir + "/" + "test"
    mkdir(hidden)
    name = hidden + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    with open(hidden + "/" + "clean.no", 'w') as f:
        f.write("")

    clean(tmp_dir)
    assert exists(hidden)
    assert exists(name)


@with_setup(setup, teardown)
def test_clean_remove_dist_build_directories():
    for name in ("dist", "build"):
        mkdir(tmp_dir + "/" + name)

    clean(tmp_dir)
    assert len(listdir(tmp_dir)) == 0
