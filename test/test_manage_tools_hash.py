from nose.tools import with_setup
from os import mkdir
from os.path import join as pj

from pkglts.manage_tools import package_hash_keys

from .small_tools import ensure_created, ensure_path, rmdir


tmp_dir = "takapouet_hash"
ref_txt = "# {{pkglts upper, toto}}"
pths = [pj(tmp_dir, n).replace("\\", "/")
        for n in ("test1.py", "test2.py", "tot/test3.py", "tot/test4.py")]


def setup():
    ensure_created(tmp_dir)

    for pth in pths:
        ensure_path(pth)
        with open(pth, 'w') as f:
            f.write(ref_txt)


def teardown():
    rmdir(tmp_dir)


@with_setup(setup, teardown)
def test_pkg_hash_same_if_no_modifications():
    hm1 = package_hash_keys(tmp_dir)
    hm2 = package_hash_keys(tmp_dir)
    assert hm1 == hm2


@with_setup(setup, teardown)
def test_pkg_hash_change_if_modifications():
    hm1 = package_hash_keys(tmp_dir)

    with open(pths[0], 'w') as f:
        f.write("modified")

    hm2 = package_hash_keys(tmp_dir)
    assert hm1 != hm2

    assert hm1[pths[0]] != hm2[pths[0]]

    for pth in pths[1:]:
        assert hm1[pth] == hm2[pth]


@with_setup(setup, teardown)
def test_pkg_hash_walk_all_files_by_default():
    hm = package_hash_keys(tmp_dir)

    for pth in pths:
        assert pth in hm


@with_setup(setup, teardown)
def test_pkg_hash_pkg_exclude_protected_dirs():
    with open(pj(tmp_dir, "tot", "regenerate.no"), 'w') as f:
        f.write("")

    hm = package_hash_keys(tmp_dir)

    for pth in pths[:2]:
        assert pth in hm

    for pth in pths[2:]:
        assert pth not in hm


@with_setup(setup, teardown)
def test_pkg_hash_pkg_exclude_hidden_dirs():
    mkdir(pj(tmp_dir, ".mydir"))
    pth = pj(tmp_dir, ".mydir", "toto.py").replace("\\", "/")

    with open(pth, 'w') as f:
        f.write(ref_txt)

    hm = package_hash_keys(tmp_dir)

    assert pth not in hm
