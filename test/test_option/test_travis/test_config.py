import pytest
from pkglts.config_management import Config
from pkglts.option.travis.option import OptionTravis


@pytest.fixture()
def opt():
    return OptionTravis('travis')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_require(opt):
    cfg = Config(dict(base={}, travis={}))

    assert len(opt.require('option', cfg)) == 3
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 0
