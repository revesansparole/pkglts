import pytest
from pkglts.config_management import Config
from pkglts.option.gitlab.option import OptionGitlab


@pytest.fixture()
def opt():
    return OptionGitlab("gitlab")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["gitlab"]) == 4


def test_config_check_project_exists(opt, cfg):
    cfg["gitlab"] = {"owner": "", "project": "", "server": "", "url": ""}
    assert "gitlab.project" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
