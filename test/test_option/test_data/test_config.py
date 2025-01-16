import pytest
from pkglts.config_management import Config
from pkglts.option.data.option import OptionData


@pytest.fixture()
def opt():
    return OptionData("data")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["data"]) == 2


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
