import pytest
from pkglts.config_management import Config
from pkglts.option.pyproject.option import OptionPyproject


@pytest.fixture()
def opt():
    return OptionPyproject("pyproject")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["pyproject"]) == 1


def test_config_check_intended_version_exists(opt, cfg):
    cfg["pyproject"] = {"intended_versions": []}
    assert "pyproject.intended_versions" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 5


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
