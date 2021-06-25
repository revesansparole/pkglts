import pytest
from pkglts.config_management import Config
from pkglts.option.git.option import OptionGit


@pytest.fixture()
def opt():
    return OptionGit('git')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['git']) == 0


def test_config_check_nothing(opt, cfg):
    cfg['git'] = {}
    assert len(opt.check(cfg)) == 0


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
