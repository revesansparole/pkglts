import mock
from nose.tools import with_setup
from os import mkdir, remove
from os.path import exists
from os.path import join as pj
from shutil import rmtree

from pkglts.manage import (init_pkg, regenerate)


print(__file__)

tmp_dir = 'toto_mg_rg'
init_file = pj(tmp_dir, "src", "toto", "__init__.py")
pkg_cfg = dict(base={'pkgname': 'toto', 'namespace': None})


def addendum():
    """ modify init_file in first pkglts div
    """
    with open(init_file, 'r') as f:
        lines = f.read().splitlines()

    lines.insert(1, "addendum")

    with open(init_file, 'w') as f:
        f.write("\n".join(lines))


def setup():
    if not exists(tmp_dir):
        mkdir(tmp_dir)


def teardown():
    if exists(tmp_dir):
        rmtree(tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_pass():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)
    assert exists(init_file)


@with_setup(setup, teardown)
def test_regenerate_handle_conflicts_keep():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)

    with open(init_file, 'w') as f:
        f.write("modified")

    with mock.patch('pkglts.manage.get_user_permission',
                    return_value=False):
        regenerate(pkg_cfg, tmp_dir)

    with open(init_file, 'r') as f:
        assert f.read() == "modified"


@with_setup(setup, teardown)
def test_regenerate_handle_conflicts_overwrite():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)
    addendum()

    with mock.patch('pkglts.manage.get_user_permission',
                    return_value=True):
        regenerate(pkg_cfg, tmp_dir)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


@with_setup(setup, teardown)
def test_regenerate_handle_global_overwrite():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)
    addendum()

    regenerate(pkg_cfg, tmp_dir, overwrite=True)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


@with_setup(setup, teardown)
def test_regenerate_new_files_do_not_generate_conflicts():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)
    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate(pkg_cfg, tmp_dir)

    assert exists(new_pth)
    with open(new_pth, 'r') as f:
        txt = f.read()
        assert txt == "txt = 'addendum'"


@with_setup(setup, teardown)
def test_regenerate_remove_user_files_do_not_generate_conflicts():
    init_pkg(tmp_dir)
    regenerate(pkg_cfg, tmp_dir)
    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate(pkg_cfg, tmp_dir)

    remove(new_pth)

    regenerate(pkg_cfg, tmp_dir)
    assert not exists(new_pth)
