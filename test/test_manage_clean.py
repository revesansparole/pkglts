from os import listdir, mkdir
from os.path import exists

import pytest
from pkglts.manage import clean
from pkglts.small_tools import ensure_created, rmdir


@pytest.fixture()
def tmp_dir():
    pth = 'toto_manage_clean'
    ensure_created(pth)

    yield pth

    rmdir(pth)


def test_clean_remove_pyc_files(tmp_dir):
    name = tmp_dir + "/" + "toto.pyc"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert not exists(name)


def test_clean_remove_pycache_directories(tmp_dir):
    pycache = tmp_dir + "/" + "__pycache__"
    mkdir(pycache)
    name = pycache + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert not exists(pycache)
    assert not exists(name)


def test_clean_do_not_remove_py_files(tmp_dir):
    name = tmp_dir + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(name)


def test_clean_do_not_remove_hidden_files(tmp_dir):
    name = tmp_dir + "/" + ".toto.pyc"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(name)


def test_clean_do_not_explore_hidden_directories(tmp_dir):
    hidden = tmp_dir + "/" + ".test"
    mkdir(hidden)
    name = hidden + "/" + "toto.py"
    with open(name, 'w') as f:
        f.write("toto")

    clean(tmp_dir)
    assert exists(hidden)
    assert exists(name)


def test_clean_do_not_explore_clean_no_directories(tmp_dir):
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


def test_clean_remove_dist_build_directories(tmp_dir):
    for name in ("dist", "build"):
        mkdir(tmp_dir + "/" + name)

    clean(tmp_dir)
    assert len(listdir(tmp_dir)) == 0
