import pytest
from pkglts.config_management import Config
from pkglts.option.coverage.option import OptionCoverage


@pytest.fixture()
def opt():
    return OptionCoverage('coverage')


def test_version_is_defined(opt):
    assert opt.version() != "0.0.0"


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config(dict(test={'suite_name': 'pytest'}))
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 2

    cfg = Config(dict(test={'suite_name': 'nose'}))
    opt.update_parameters(cfg)
    assert len(tuple(opt.require(cfg))) == 1
