import pytest
from pkglts.config_management import Config
from pkglts.option.license.option import OptionLicense


@pytest.fixture()
def opt():
    return OptionLicense("license")


@pytest.fixture()
def cfg():
    return Config()


def test_update_parameters(opt, cfg):
    opt.update_parameters(cfg)
    assert len(cfg["license"]) == 4


def test_config_check_license_name_exists(opt, cfg):
    cfg["license"] = {"name": "", "year": 2015, "organization": "oa", "project": "project"}
    assert "license.name" in opt.check(cfg)

    cfg["license"] = {"name": "tugudu", "year": 2015, "organization": "oa", "project": "project"}
    assert "license.name" in opt.check(cfg)


def test_require_option(opt, cfg):
    assert len(tuple(opt.require_option(cfg))) == 1


def test_require(opt, cfg):
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
