import pytest
from pkglts.config_management import Config
from pkglts.option.conda.option import OptionConda


@pytest.fixture()
def opt():
    return OptionConda("conda")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["conda"]) == 1


def test_config_check_env_name_exists(opt, cfg):
    cfg["conda"] = {"env_name": "myname"}
    assert cfg["conda"]["env_name"] == "myname"
    assert "conda.env_name" not in opt.check(cfg)


def test_config_check_env_name_valid(opt, cfg):
    cfg["conda"] = {"env_name": ""}
    assert "conda.env_name" in opt.check(cfg)

    cfg["conda"] = {"env_name": "\ttoto "}
    assert "conda.env_name" in opt.check(cfg)

    cfg["conda"] = {"env_name": "toto-tutu"}
    assert "conda.env_name" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
