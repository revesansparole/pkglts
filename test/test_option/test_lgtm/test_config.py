import pytest
from pkglts.config_management import Config
from pkglts.option.lgtm.option import OptionLgtm


@pytest.fixture()
def opt():
    return OptionLgtm('lgtm')


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 2


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
