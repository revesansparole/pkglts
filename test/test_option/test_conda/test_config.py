import pytest
from pkglts.config_management import Config
from pkglts.option.conda.option import OptionConda


@pytest.fixture()
def opt():
    return OptionConda('conda')


@pytest.fixture()
def cfg():
    return Config()


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
