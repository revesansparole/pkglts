from copy import deepcopy
from os import listdir
from os.path import exists
from os.path import join as pj
import pytest

from pkglts.config_management import create_env, default_cfg, pkg_env
from pkglts.manage import install_example_files

from .small_tools import ensure_created, rmdir


@pytest.fixture()
def tmp_dir():
    pth = "tmp_cfgex"
    ensure_created(pth)

    yield pth

    rmdir(pth)


def test_install_example_returns_false_if_option_not_already_installed(tmp_dir):
    env = create_env(default_cfg)
    ans = install_example_files('option', env, tmp_dir)
    assert not ans


def test_install_example_ok_if_option_do_not_provide_examples(tmp_dir):
    cfg = deepcopy(default_cfg)
    cfg['base'] = dict()
    env = create_env(cfg)
    ans = install_example_files('base', env, tmp_dir)
    assert not ans


def test_install_example_copy_files(tmp_dir):
    cfg = deepcopy(default_cfg)
    cfg['base'] = dict(pkgname='toto', namespace=None)
    cfg['test'] = dict(suite_name='nose')
    env = pkg_env(cfg)

    assert len(listdir(tmp_dir)) == 0
    install_example_files('test', env, tmp_dir)
    assert len(listdir(tmp_dir)) > 0
    assert exists(pj(tmp_dir, "src", "toto", "example.py"))
    assert exists(pj(tmp_dir, "test", "test_example.py"))


def test_install_example_copy_binary_files(tmp_dir):
    cfg = deepcopy(default_cfg)
    cfg['base'] = dict(pkgname='toto', namespace=None)
    cfg['data'] = dict()
    env = pkg_env(cfg)

    assert len(listdir(tmp_dir)) == 0
    install_example_files('data', env, tmp_dir)
    assert len(listdir(tmp_dir)) > 0
    assert exists(pj(tmp_dir, "src", "toto_data", "ext_data.png"))


def test_install_example_do_not_complain_if_file_already_exists(tmp_dir):
    cfg = deepcopy(default_cfg)
    cfg['base'] = dict(pkgname='toto', namespace=None)
    cfg['test'] = dict(suite_name='nose')
    env = pkg_env(cfg)

    assert install_example_files('test', env, tmp_dir)
    assert install_example_files('test', env, tmp_dir)


def test_install_example_handles_namespace(tmp_dir):
    cfg = deepcopy(default_cfg)
    cfg['base'] = dict(pkgname='toto', namespace='oa', namespace_method='pkg_utils')
    cfg['test'] = dict(suite_name='nose')
    env = pkg_env(cfg)

    install_example_files('test', env, tmp_dir)
    assert exists(pj(tmp_dir, "test", "test_example.py"))
    assert not exists(pj(tmp_dir, "src", "toto", "example.py"))
    assert exists(pj(tmp_dir, "src", "oa", "toto", "example.py"))
