import pytest
from pkglts.config_management import Config
from pkglts.option.flake8.option import OptionFlake8


@pytest.fixture()
def opt():
    return OptionFlake8('flake8')


@pytest.fixture()
def cfg():
    return Config()


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
