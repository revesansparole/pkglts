import pytest
from pkglts.config_management import Config
from pkglts.option.tox.option import OptionTox


@pytest.fixture()
def opt():
    return OptionTox('tox')


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
