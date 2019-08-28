import json
from os import remove
from os.path import exists
from os.path import join as pj

import pytest
from pkglts.config import pkg_cfg_file, pkglts_dir
from pkglts.config_management import Config, get_pkg_config, write_pkg_config
from pkglts.manage import init_pkg, regenerate_package
from pkglts.small_tools import ensure_created, rmdir


def addendum(init_file):
    """ modify init_file in first pkglts div
    """
    with open(init_file, 'r') as f:
        lines = f.read().splitlines()

    lines.insert(1, "addendum")

    with open(init_file, 'w') as f:
        f.write("\n".join(lines))
        f.write("\n")


@pytest.fixture()
def tmp_pths():
    pth = 'toto_mg_rg'
    ensure_created(pth)
    init_pkg(pth)
    with open(pj(pth, pkglts_dir, pkg_cfg_file), 'r') as f:
        pkg_cfg = json.load(f)

    pkg_cfg['base'] = dict(pkgname='toto',
                           namespace=None,
                           authors=[('moi', 'moi@email.com')],
                           url=None)
    pkg_cfg['src'] = dict(namespace_method="pkg_util")

    cfg = Config(pkg_cfg)
    write_pkg_config(cfg, pth)
    regenerate_package(cfg, pth)

    init_file = pj(pth, "src", "toto", "__init__.py")

    yield pth, init_file

    rmdir(pth)


def test_regenerate_pass(tmp_pths):
    tmp_dir, init_file = tmp_pths
    with open(pj(tmp_dir, pkglts_dir, pkg_cfg_file), 'r') as f:
        pkg_cfg = json.load(f)

    cfg = Config(pkg_cfg)
    regenerate_package(cfg, tmp_dir)
    assert exists(init_file)


def test_regenerate_check_pkg_cfg_validity(tmp_pths):
    tmp_dir, init_file = tmp_pths
    with open(pj(tmp_dir, pkglts_dir, pkg_cfg_file), 'r') as f:
        pkg_cfg = json.load(f)

    pkg_cfg['base']['pkgname'] = '1toto'

    cfg = Config(pkg_cfg)
    assert not regenerate_package(cfg, tmp_dir)


def test_regenerate_handle_conflicts_keep(tmp_pths, mocker):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    with open(init_file, 'w') as f:
        f.write("modified")

    with mocker.patch('pkglts.manage.get_user_permission',
                      return_value=False):
        regenerate_package(cfg, tmp_dir)

    with open(init_file, 'r') as f:
        assert f.read() == "modified"


def test_regenerate_handle_conflicts_overwrite(tmp_pths, mocker):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    addendum(init_file)

    with mocker.patch('pkglts.manage.get_user_permission',
                      return_value=True):
        regenerate_package(cfg, tmp_dir)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


def test_regenerate_handle_global_overwrite(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    addendum(init_file)

    regenerate_package(cfg, tmp_dir, overwrite=True)

    with open(init_file, 'r') as f:
        txt = f.read()
        assert "modified" not in txt


def test_regenerate_new_files_do_not_generate_conflicts(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate_package(cfg, tmp_dir)

    assert exists(new_pth)
    with open(new_pth, 'r') as f:
        txt = f.read()
        assert txt == "txt = 'addendum'"


def test_regenerate_remove_user_files_do_not_generate_conflicts(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    new_pth = pj(tmp_dir, "src", "toto", "new_file.py")
    with open(new_pth, 'w') as f:
        f.write("txt = 'addendum'")

    regenerate_package(cfg, tmp_dir)

    remove(new_pth)

    regenerate_package(cfg, tmp_dir)
    assert not exists(new_pth)


def test_regenerate_fail_if_permanent_section_ids_have_been_modified(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    with open(init_file, 'a') as f:
        f.write("\n# {# pkglts, test\na = 1\n# #}\n")

    with pytest.raises(UserWarning):
        regenerate_package(cfg, tmp_dir, overwrite=True)
