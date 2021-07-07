import pytest
from pkglts.config_management import Config
from pkglts.option.requires.option import OptionRequires


@pytest.fixture()
def opt():
    return OptionRequires('requires')


@pytest.fixture()
def cfg():
    return Config()


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 2


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
