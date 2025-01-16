import pytest
from pkglts.config_management import Config
from pkglts.option.coverage.option import OptionCoverage


@pytest.fixture()
def opt():
    return OptionCoverage("coverage")


@pytest.fixture()
def cfg():
    return Config()


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    cfg["test"] = {"suite_name": "pytest"}
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 2

    cfg["test"] = {"suite_name": "nose"}
    opt.update_parameters(cfg)
    assert len(tuple(opt.require(cfg))) == 1
