import json
from os.path import exists
from os.path import join as pj

import pytest
import semver
from pkglts.config import pkg_version_file, pkglts_dir
from pkglts.config_management import Config, DEFAULT_CFG
from pkglts.small_tools import ensure_created, rmdir
from pkglts.version import __version__
from pkglts.version_management import load_pkg_version, option_current_version, outdated_options, write_pkg_version


@pytest.fixture()
def tmp_dir():
    pth = "toto_mg_ver"
    ensure_created(pth)
    ensure_created(pj(pth, ".pkglts"))

    yield pth

    if exists(pth):
        rmdir(pth)


@pytest.fixture()
def tmp_cfg():
    pkg_cfg = dict(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname="toto", namespace="nm",
                           url=None, authors=[("moi", "moi@aussi")])
    pkg_cfg['license'] = dict(name="CeCILL-C", organization="org",
                              project="{{ base.pkgname }}", year="2015")

    cfg = Config(pkg_cfg)
    return cfg


def test_pkglts_options_use_pkglts_version():
    assert option_current_version('base') == __version__


def test_freshly_regenerated_package_have_not_outdated_options(tmp_cfg, tmp_dir):
    write_pkg_version(tmp_cfg, tmp_dir)

    assert len(outdated_options(tmp_cfg, tmp_dir)) == 0


def test_outdated_options_handles_no_version_file(tmp_cfg, tmp_dir):
    assert len(outdated_options(tmp_cfg, tmp_dir)) == 0


def test_old_regenerated_package_have_outdated_options(tmp_cfg, tmp_dir):
    write_pkg_version(tmp_cfg, tmp_dir)
    ver = load_pkg_version(tmp_dir)
    ver['base'] = semver.bump_major(ver['base'])
    json.dump(ver, open(pj(tmp_dir, pkglts_dir, pkg_version_file), 'w'))

    assert 'base' in outdated_options(tmp_cfg, tmp_dir)


def test_old_regenerated_handles_unknown_options(tmp_cfg, tmp_dir):
    write_pkg_version(tmp_cfg, tmp_dir)
    ver = load_pkg_version(tmp_dir)
    del ver['base']
    json.dump(ver, open(pj(tmp_dir, pkglts_dir, pkg_version_file), 'w'))

    assert 'base' not in outdated_options(tmp_cfg, tmp_dir)
