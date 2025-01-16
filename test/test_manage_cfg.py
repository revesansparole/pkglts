from pathlib import Path

import pytest
from pkglts.config import pkglts_dir
from pkglts.manage import get_pkg_config, get_pkg_hash, init_pkg
from pkglts.small_tools import ensure_created, rmdir


@pytest.fixture()
def tmp_dir():
    pth = Path("toto_manage_cfg")
    ensure_created(pth)
    init_pkg(pth)

    yield pth

    rmdir(pth)


def test_manage_init_create_pkg_config(tmp_dir):
    cfg = get_pkg_config(tmp_dir)
    assert cfg is not None
    assert "_pkglts" in cfg


def test_manage_init_create_pkg_hash(tmp_dir):
    hm = get_pkg_hash(tmp_dir)
    assert hm is not None


def test_manage_init_protect_pkglts_dir_from_modif(tmp_dir):
    assert "regenerate.no" in [pth.name for pth in (tmp_dir / pkglts_dir).iterdir()]
    assert "clean.no" in [pth.name for pth in (tmp_dir / pkglts_dir).iterdir()]


# def test_manage_pkg_config(tmp_dir):
#     cfg = get_pkg_config(tmp_dir)
#     cfg.template()['toto'] = dict(toto=1)
#     write_pkg_config(cfg, tmp_dir)
#
#     new_cfg = get_pkg_config(tmp_dir)
#     import json
#     print(json.dumps(cfg, indent=2))
#     print(json.dumps(new_cfg, indent=2))
#     assert new_cfg == cfg
#
# @with_setup(setup, teardown)
# def test_manage_pkg_config_fmt_templates():
#     cfg = dict(default_cfg)
#     cfg['base'] = dict(pkg='custom')
#     cfg['toto'] = dict(base=10, toto="{{key, base.pkg}}")
#     write_pkg_config(cfg, tmp_dir)
#
#     cfg = get_pkg_config(tmp_dir)['toto']
#     assert 'base' in cfg
#     assert 'toto' in cfg
#     assert cfg['toto'] == "custom"
#
#
# @with_setup(setup, teardown)
# def test_manage_cfg_store_any_item():
#     algo = sha512()
#     algo.update(("lorem ipsum\n" * 10).encode("latin1"))
#
#     cfg = dict(default_cfg)
#     cfg['toto'] = dict(simple=1,
#                        txt="lorem ipsum\n" * 4,
#                        hash=b64encode(algo.digest()).decode('utf-8'))
#
#     write_pkg_config(cfg, tmp_dir)
#
#     new_cfg = get_pkg_config(tmp_dir)
#     assert new_cfg == cfg
#
#     algo = sha512()
#     algo.update(("lorem ipsum\n" * 10).encode("latin1"))
#     sha = b64encode(algo.digest()).decode('utf-8')
#     assert sha == new_cfg['toto']['hash']
#
#
# @with_setup(setup, teardown)
# def test_manage_cfg_do_store_private_item():
#     cfg = dict(default_cfg)
#     cfg['toto'] = {}
#     cfg['_toto'] = {}
#     write_pkg_config(cfg, tmp_dir)
#
#     new_cfg = get_pkg_config(tmp_dir)
#     assert '_toto' in new_cfg
#
#
# @with_setup(setup, teardown)
# def test_manage_cfg_restore_templates_on_writing():
#     cfg = dict(default_cfg)
#     cfg['base'] = dict(pkg='custom')
#     cfg['toto'] = dict(base=10, toto="{{key, base.pkg}}")
#     write_pkg_config(cfg, tmp_dir)
#
#     pkg_cfg = get_pkg_config(tmp_dir)
#     assert pkg_cfg['toto']['toto'] == "custom"
#
#     pkg_cfg['base']['pkg'] = "another"
#     write_pkg_config(pkg_cfg, tmp_dir)
#
#     pkg_cfg = get_pkg_config(tmp_dir)
#     assert pkg_cfg['toto']['toto'] == "another"
