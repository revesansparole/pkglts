import pytest
from pkglts.config_management import Config
from pkglts.option.appveyor.option import OptionAppveyor


@pytest.fixture()
def opt():
    return OptionAppveyor('appveyor')


def test_version_is_defined(opt):
    assert opt.version() != "0.0.0"


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['appveyor']) == 1


def test_config_does_nothing(opt):
    cfg = Config(dict(appveyor={'token': 'toto'}))
    assert len(opt.check(cfg)) == 0


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 3


def test_require(opt):
    cfg = Config(dict(base={}, travis={}))
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
