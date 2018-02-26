import pytest
from pkglts.config_management import Config
from pkglts.option.pypi.option import OptionPypi


@pytest.fixture()
def opt():
    return OptionPypi('pypi')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['pypi']) == 2


def test_config_check_classifiers_exists(opt):
    cfg = Config(dict(pypi={'classifiers': []}))
    assert 'pypi.classifiers' in opt.check(cfg)


def test_require(opt):
    cfg = Config(dict(pypi={}))

    assert len(opt.require('option', cfg)) == 2
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 1
