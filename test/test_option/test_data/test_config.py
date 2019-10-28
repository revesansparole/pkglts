import pytest
from pkglts.config_management import Config
from pkglts.option.data.option import OptionData


@pytest.fixture()
def opt():
    return OptionData('data')


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['data']) == 2


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
