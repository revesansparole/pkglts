import pytest
from pkglts.config_management import Config
from pkglts.option.pysetup.option import OptionPysetup


@pytest.fixture()
def opt():
    return OptionPysetup('pysetup')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['pysetup']) == 1


def test_config_check_intended_version_exists(opt, cfg):
    cfg['pysetup'] = {'intended_versions': []}
    assert 'pysetup.intended_versions' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 5


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
