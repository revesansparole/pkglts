import pytest
from pkglts.config_management import Config
from pkglts.option.appveyor.option import OptionAppveyor


@pytest.fixture()
def opt():
    return OptionAppveyor("appveyor")


@pytest.fixture()
def cfg():
    return Config(dict(base={}, travis={}))


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["appveyor"]) == 1


def test_config_does_nothing(opt, cfg):
    cfg["appveyor"] = {"token": "toto"}
    assert len(opt.check(cfg)) == 0


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 3


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
