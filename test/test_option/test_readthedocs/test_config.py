import pytest
from pkglts.config_management import Config
from pkglts.option.readthedocs.option import OptionReadthedocs


@pytest.fixture()
def opt():
    return OptionReadthedocs('readthedocs')


@pytest.fixture()
def cfg():
    return Config(dict(github={}))


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['readthedocs']) == 1


def test_config_check_project_exists(opt, cfg):
    cfg['readthedocs'] = {'project': ""}
    assert 'readthedocs.project' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 3


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
