import pytest
from pkglts.config_management import Config
from pkglts.option.tox.option import OptionTox


@pytest.fixture()
def opt():
    return OptionTox('tox')


def test_version_is_defined(opt):
    assert opt.version() != "0.0.0"


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 1
