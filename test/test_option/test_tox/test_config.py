import pytest
from pkglts.config_management import Config
from pkglts.option.tox.option import OptionTox


@pytest.fixture()
def opt():
    return OptionTox('tox')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require(opt):
    cfg = Config(dict(base={}, tox={}))

    assert len(opt.require('option', cfg)) == 1
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 1
