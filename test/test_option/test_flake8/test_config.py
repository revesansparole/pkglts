import pytest
from pkglts.config_management import Config
from pkglts.option.flake8.option import OptionFlake8


@pytest.fixture()
def opt():
    return OptionFlake8('flake8')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require(opt):
    cfg = Config(dict(base={}, flake8={}))

    assert len(opt.require('option', cfg)) == 1
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 1
