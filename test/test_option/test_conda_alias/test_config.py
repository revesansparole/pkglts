import pytest
from pkglts.config_management import Config
from pkglts.option.conda_alias.option import OptionCondaAlias


@pytest.fixture()
def opt():
    return OptionCondaAlias('conda_alias')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['conda_alias']) == 0


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
