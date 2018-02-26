import pytest
from pkglts.config_management import Config
from pkglts.option.coverage.option import OptionCoverage


@pytest.fixture()
def opt():
    return OptionCoverage('coverage')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require(opt):
    cfg = Config(dict(coverage={}, test={'suite_name': 'pytest'}))

    assert len(opt.require('option', cfg)) == 1
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 2

    cfg = Config(dict(coverage={}, test={'suite_name': 'nose'}))
    assert len(opt.require('dvlpt', cfg)) == 1
