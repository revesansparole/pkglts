import pytest
from pkglts.config_management import Config
from pkglts.option.github.option import OptionGithub


@pytest.fixture()
def opt():
    return OptionGithub('github')


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg['github']) == 3


def test_config_check_project_exists(opt, cfg):
    cfg['github'] = {'owner': "", 'project': "", "url": ""}
    assert 'github.project' in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
