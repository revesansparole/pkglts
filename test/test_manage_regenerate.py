import json
from pathlib import Path

import pytest
from pkglts.config import pkg_cfg_file, pkglts_dir
from pkglts.config_management import Config, get_pkg_config, write_pkg_config
from pkglts.manage import init_pkg, regenerate_option, regenerate_package
from pkglts.small_tools import ensure_created, rmdir


def addendum(init_file):
    """modify init_file in first pkglts div"""
    with open(init_file, "r") as fhr:
        lines = fhr.read().splitlines()

    lines.insert(1, "addendum")

    with open(init_file, "w") as fhw:
        fhw.write("\n".join(lines))
        fhw.write("\n")


@pytest.fixture()
def tmp_pths():
    pth = Path("toto_mg_rg")
    ensure_created(pth)
    init_pkg(pth)
    with open((pth / pkglts_dir / pkg_cfg_file), "r") as fhr:
        pkg_cfg = json.load(fhr)

    pkg_cfg["base"] = dict(pkgname="toto", namespace=None, authors=[("moi", "moi@email.com")], url=None)
    pkg_cfg["src"] = dict(namespace_method="pkg_util")

    cfg = Config(pkg_cfg)
    write_pkg_config(cfg, pth)
    regenerate_package(cfg, pth)

    init_file = pth / "src/toto/__init__.py"

    yield pth, init_file

    rmdir(pth)


def test_regenerate_pass(tmp_pths):
    tmp_dir, init_file = tmp_pths
    with open(tmp_dir / pkglts_dir / pkg_cfg_file, "r") as fhr:
        pkg_cfg = json.load(fhr)

    cfg = Config(pkg_cfg)
    regenerate_package(cfg, tmp_dir)
    assert init_file.exists()


def test_regenerate_check_pkg_cfg_validity(tmp_pths):
    tmp_dir, init_file = tmp_pths
    with open(tmp_dir / pkglts_dir / pkg_cfg_file, "r") as fhr:
        pkg_cfg = json.load(fhr)

    pkg_cfg["base"]["pkgname"] = "1toto"

    cfg = Config(pkg_cfg)
    assert not regenerate_package(cfg, tmp_dir)


def test_regenerate_handle_conflicts_keep(tmp_pths, mocker):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    init_file.write_text("modified")

    mocker.patch("pkglts.manage.get_user_permission", return_value=False)
    regenerate_package(cfg, tmp_dir)

    assert init_file.read_text() == "modified"


def test_regenerate_handle_conflicts_overwrite(tmp_pths, mocker):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    addendum(init_file)

    mocker.patch("pkglts.manage.get_user_permission", return_value=True)
    regenerate_package(cfg, tmp_dir)

    assert "modified" not in init_file.read_text()


def test_regenerate_handle_global_overwrite(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    addendum(init_file)

    regenerate_package(cfg, tmp_dir, overwrite=True)

    assert "modified" not in init_file.read_text()


def test_regenerate_new_files_do_not_generate_conflicts(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    new_pth = tmp_dir / "src/toto/new_file.py"
    new_pth.write_text("txt = 'addendum'")

    regenerate_package(cfg, tmp_dir)

    assert new_pth.exists()
    assert new_pth.read_text() == "txt = 'addendum'"


def test_regenerate_remove_user_files_do_not_generate_conflicts(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    new_pth = tmp_dir / "src/toto/new_file.py"
    new_pth.write_text("txt = 'addendum'")

    regenerate_package(cfg, tmp_dir)

    new_pth.unlink()

    regenerate_package(cfg, tmp_dir)
    assert not new_pth.exists()


def test_regenerate_remove_tpl_files_do_not_generate_conflicts(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    regenerate_package(cfg, tmp_dir)

    init_file.unlink()

    regenerate_package(cfg, tmp_dir)
    assert init_file.exists()


def test_regenerate_fail_if_permanent_section_ids_have_been_modified(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    with open(init_file, "a") as fhw:
        fhw.write("\n# {# pkglts, test\na = 1\n# #}\n")

    with pytest.raises(UserWarning):
        regenerate_package(cfg, tmp_dir, overwrite=True)


def test_regenerate_option_fails_if_option_not_available(tmp_pths):
    tmp_dir, init_file = tmp_pths
    cfg = get_pkg_config(tmp_dir)

    regenerate_option(cfg, "base", tmp_dir)

    with pytest.raises(KeyError):
        regenerate_option(cfg, "toto", tmp_dir)
