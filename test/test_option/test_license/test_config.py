import pytest
from pkglts.config_management import Config
from pkglts.option.license.option import OptionLicense


@pytest.fixture()
def opt():
    return OptionLicense('license')


def test_root_dir_is_defined(opt):
    assert opt.root_dir() is not None


def test_update_parameters(opt):
    cfg = {}
    opt.update_parameters(cfg)
    assert len(cfg['license']) == 4


def test_config_check_license_name_exists(opt):
    cfg = Config(dict(license={'name': "", 'year': 2015,
                               'organization': "oa", 'project': "project"}))
    assert 'license.name' in opt.check(cfg)

    cfg = Config(dict(license={'name': "tugudu", 'year': 2015,
                               'organization': "oa", 'project': "project"}))
    assert 'license.name' in opt.check(cfg)


def test_require_option(opt):
    assert len(tuple(opt.require_option())) == 1


def test_require(opt):
    cfg = Config()
    opt.update_parameters(cfg)

    assert len(tuple(opt.require(cfg))) == 0
