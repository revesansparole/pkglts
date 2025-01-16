import pytest
from pkglts.config_management import Config
from pkglts.option.src.option import OptionSrc


@pytest.fixture()
def opt():
    return OptionSrc("src")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["src"]) == 1


def test_config_check_pkg_names(opt, cfg):
    cfg["src"] = {"namespace_method": "toto"}
    assert "src.namespace_method" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
