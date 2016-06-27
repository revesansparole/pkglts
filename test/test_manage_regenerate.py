import json
import mock
from nose.tools import assert_raises, with_setup
from os import remove
from os.path import exists
from os.path import join as pj

from pkglts.config import pkglts_dir, pkg_cfg_file
from pkglts.config_management import create_env, get_pkg_config, write_pkg_config
from pkglts.manage import (init_pkg, regenerate_package)

from .small_tools import ensure_created, rmdir


tmp_dir = 'toto_mg_rg'
init_file = pj(tmp_dir, "src", "toto", "__init__.py")


def addendum():
    """ modify init_file in first pkglts div
    """
    with open(init_file, 'r') as f:
        lines = f.read().splitlines()

    lines.insert(1, "addendum")

    with open(init_file, 'w') as f:
        f.write("\n".join(lines))


def setup():
    ensure_created(tmp_dir)
    init_pkg(tmp_dir)
    with open(pj(tmp_dir, pkglts_dir, pkg_cfg_file), 'r') as f:
        cfg = json.load(f)

    cfg['base'] = dict(pkgname='toto', namespace=None,
                       authors=[('moi', 'moi@email.com')], url=None)
    env = create_env(cfg)
    write_pkg_config(env, tmp_dir)
    regenerate_package(env, tmp_dir)


def teardown():
    rmdir(tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_pass():
    with open(pj(tmp_dir, pkglts_dir, pkg_cfg_file), 'r') as f:
        cfg = json.load(f)

    cfg['base'] = dict(pkgname='toto', namespace=None,
                       authors=[('moi', 'moi@email.com')], url=None)
    env = create_env(cfg)
    regenerate_package(env, tmp_dir)
    assert exists(init_file)


@with_setup(setup, teardown)
def test_regenerate_check_pkg_cfg_validity():
    with open(pj(tmp_dir, pkglts_dir, pkg_cfg_file), 'r') as f:
        cfg = json.load(f)

    cfg['base'] = dict(pkgname='1toto', namespace=None,
                       authors=[('moi', 'moi@email.com')], url=None)
    env = create_env(cfg)
    assert not regenerate_package(env, tmp_dir)


@with_setup(setup, teardown)
def test_regenerate_handle_conflicts_keep():
    env = get_pkg_config(tmp_dir)

    with open(init_file, 'w') as f:
        f.write("modified")

    with mock.patch('pkglts.manage.get_user_permission',
                    return_value=False):
        regenerate_package(env, tmp_dir)

    with open(init_file, 'r') as f:
        assert f.read() == "modified"


@with_setup(setup, teardown)
def test_regenerate_handle_conflicts_overwrite():
    env = get_pkg_config(tmp_dir)

    addendum()

    with mock.patch('pkglts.manage.get_user_permission',
                    return_value=True):
        regenerate_package(env, tmp_dir)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


@with_setup(setup, teardown)
def test_regenerate_handle_global_overwrite():
    env = get_pkg_config(tmp_dir)

    addendum()

    regenerate_package(env, tmp_dir, overwrite=True)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


@with_setup(setup, teardown)
def test_regenerate_new_files_do_not_generate_conflicts():
    env = get_pkg_config(tmp_dir)

    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate_package(env, tmp_dir)

    assert exists(new_pth)
    with open(new_pth, 'r') as f:
        txt = f.read()
        assert txt == "txt = 'addendum'"


@with_setup(setup, teardown)
def test_regenerate_remove_user_files_do_not_generate_conflicts():
    env = get_pkg_config(tmp_dir)

    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate_package(env, tmp_dir)

    remove(new_pth)

    regenerate_package(env, tmp_dir)
    assert not exists(new_pth)


@with_setup(setup, teardown)
def test_regenerate_fail_if_permanent_section_ids_have_been_modified():
    env = get_pkg_config(tmp_dir)

    with open(init_file, 'a') as f:
        f.write("\n# {# pkglts, test\na = 1\n# #}\n")

    assert_raises(KeyError, lambda: regenerate_package(env, tmp_dir, overwrite=True))
