import json
from pathlib import Path

import pytest
from pkglts.config import pkg_cfg_file, pkglts_dir
from pkglts.config_management import Config, write_pkg_config
from pkglts.hash_management import get_pkg_hash
from pkglts.manage import init_pkg, regenerate_package, reset_package
from pkglts.small_tools import ensure_created, rmdir


@pytest.fixture()
def tmp_pths():
    pth = Path('toto_mg_rg')
    ensure_created(pth)
    init_pkg(pth)
    with open((pth / pkglts_dir / pkg_cfg_file), 'r') as fhr:
        pkg_cfg = json.load(fhr)

    pkg_cfg['base'] = dict(pkgname='toto',
                           namespace=None,
                           authors=[('moi', 'moi@email.com')],
                           url=None)
    pkg_cfg['src'] = dict(namespace_method="pkg_util")

    cfg = Config(pkg_cfg)
    write_pkg_config(cfg, pth)
    regenerate_package(cfg, pth)

    init_file = pth / "src/toto/__init__.py"

    yield pth, init_file

    rmdir(pth)


def test_reset_removes_files(tmp_pths):
    tmp_dir, init_file = tmp_pths
    with open(tmp_dir / pkglts_dir / pkg_cfg_file, 'r') as fhr:
        pkg_cfg = json.load(fhr)

    tpl_pths = [Path(pth) for pth in get_pkg_hash(tmp_dir)]

    for pth in tpl_pths:
        assert pth.exists()

    cfg = Config(pkg_cfg)
    reset_package(cfg, tmp_dir)

    for pth in tpl_pths:
        assert not pth.exists()


def test_reset_does_not_touch_non_templated_files(tmp_pths):
    tmp_dir, init_file = tmp_pths
    with open(tmp_dir / pkglts_dir / pkg_cfg_file, 'r') as fhr:
        pkg_cfg = json.load(fhr)

    non_tpl_file = init_file.parent / "toto.py"
    non_tpl_file.write_text("# Toto was here")

    assert non_tpl_file.exists()

    cfg = Config(pkg_cfg)
    reset_package(cfg, tmp_dir)

    assert non_tpl_file.exists()
