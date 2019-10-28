import pytest
from pkglts.config_management import Config
from pkglts.option.pysetup.option import OptionPysetup


@pytest.fixture()
def opt():
    return OptionPysetup('pysetup')


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['pysetup']) == 1


def test_config_check_intended_version_exists(opt):
    cfg = Config(dict(pysetup={'intended_versions': []}))
    assert 'pysetup.intended_versions' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 5


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
