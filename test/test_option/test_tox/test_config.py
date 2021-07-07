import pytest
from pkglts.config_management import Config
from pkglts.option.tox.option import OptionTox


@pytest.fixture()
def opt():
    return OptionTox('tox')


@pytest.fixture()
def cfg():
    return Config()


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
