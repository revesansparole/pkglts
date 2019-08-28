import pytest
from pkglts.config_management import Config
from pkglts.option.github.option import OptionGithub


@pytest.fixture()
def opt():
    return OptionGithub('github')


def test_version_is_defined(opt):
    assert opt.version() != "0.0.0"


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['github']) == 3


def test_config_check_project_exists(opt):
    cfg = Config(dict(github={'owner': "", 'project': "", "url": ""}))
    assert 'github.project' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
