import pytest

from pkglts.config_management import Config
from pkglts.option.black.option import OptionBlack


@pytest.fixture()
def opt():
    return OptionBlack("black")


@pytest.fixture()
def cfg():
    return Config(dict(base={}))


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["black"]) == 0



def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    assert len(tuple(opt.require(cfg))) == 1
