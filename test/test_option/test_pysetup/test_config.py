import pytest
from pkglts.config_management import Config
from pkglts.option.pysetup.option import OptionPysetup


@pytest.fixture()
def opt():
    return OptionPysetup('pysetup')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['pysetup']) == 2


def test_config_check_intended_version_exists(opt):
    cfg = Config(dict(pysetup={'intended_versions': [], 'require': []}))
    assert 'pysetup.intended_versions' in opt.check(cfg)
    assert 'pysetup.require' not in opt.check(cfg)

    cfg = Config(dict(pysetup={'intended_versions': ["27"],
                               'require': [{'pkg_mng': 'walou', 'name': 'numpy'}]}))
    assert 'pysetup.require' in opt.check(cfg)


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(opt.require('option', cfg)) == 5
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 0
