import pytest
from pkglts.config_management import Config
from pkglts.option.conda.option import OptionConda


@pytest.fixture()
def opt():
    return OptionConda('conda')


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
