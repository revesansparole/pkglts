import pytest
from pkglts.config_management import Config
from pkglts.option.readthedocs.option import OptionReadthedocs


@pytest.fixture()
def opt():
    return OptionReadthedocs('readthedocs')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['readthedocs']) == 1


def test_config_check_project_exists(opt):
    cfg = Config(dict(readthedocs={'project': ""}))
    assert 'readthedocs.project' in opt.check(cfg)


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(opt.require('option', cfg)) == 4
    assert len(opt.require('setup', cfg)) == 0
    assert len(opt.require('install', cfg)) == 0
    assert len(opt.require('dvlpt', cfg)) == 0
