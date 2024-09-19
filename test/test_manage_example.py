from copy import deepcopy
from pathlib import Path

import pytest
from pkglts import logging_tools
from pkglts.config_management import Config, DEFAULT_CFG
from pkglts.manage import install_example_files
from pkglts.small_tools import ensure_created, rmdir


@pytest.fixture()
def tmp_dir():
    pth = Path("tmp_cfgex")
    ensure_created(pth)

    yield pth

    rmdir(pth)


def test_install_example_returns_false_if_option_not_already_installed(tmp_dir):
    cfg = Config(DEFAULT_CFG)
    cfg.load_extra()
    ans = install_example_files('option', cfg, tmp_dir)
    assert not ans


def test_install_example_ok_if_option_do_not_provide_examples(tmp_dir):
    pkg_cfg = deepcopy(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace=None)
    cfg = Config(pkg_cfg)
    cfg.load_extra()

    ans = install_example_files('base', cfg, tmp_dir)
    assert not ans


def test_install_example_copy_files(tmp_dir):
    pkg_cfg = deepcopy(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace=None)
    pkg_cfg['test'] = dict(suite_name='nose')
    cfg = Config(pkg_cfg)
    cfg.load_extra()

    assert len(tuple(tmp_dir.iterdir())) == 0
    logging_tools.main(2)
    install_example_files('test', cfg, tmp_dir)
    assert len(tuple(tmp_dir.iterdir())) > 0
    assert (tmp_dir / "src/toto/example.py").exists()
    assert (tmp_dir / "test/test_example.py").exists()


def test_install_example_copy_binary_files(tmp_dir):
    pkg_cfg = deepcopy(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace=None)
    pkg_cfg['data'] = dict(filetype=[".png", ".ui"], use_ext_dir=True)
    cfg = Config(pkg_cfg)
    cfg.load_extra()

    assert len(tuple(tmp_dir.iterdir())) == 0
    install_example_files('data', cfg, tmp_dir)
    assert len(tuple(tmp_dir.iterdir())) > 0
    assert (tmp_dir / "src/toto_data/ext_data.png").exists()


def test_install_example_do_not_complain_if_file_already_exists(tmp_dir):
    pkg_cfg = deepcopy(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace=None)
    pkg_cfg['test'] = dict(suite_name='nose')
    cfg = Config(pkg_cfg)
    cfg.load_extra()

    assert install_example_files('test', cfg, tmp_dir)
    assert install_example_files('test', cfg, tmp_dir)


def test_install_example_handles_namespace(tmp_dir):
    pkg_cfg = deepcopy(DEFAULT_CFG)
    pkg_cfg['base'] = dict(pkgname='toto', namespace='oa')
    pkg_cfg['src'] = dict(namespace_method='pkg_utils')
    pkg_cfg['test'] = dict(suite_name='nose')
    cfg = Config(pkg_cfg)
    cfg.load_extra()

    install_example_files('test', cfg, tmp_dir)
    assert (tmp_dir / "test/test_example.py").exists()
    assert not (tmp_dir / "src/toto/example.py").exists()
    assert (tmp_dir / "src/oa/toto/example.py").exists()
