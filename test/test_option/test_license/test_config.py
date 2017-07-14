from pkglts.config_management import Config
from pkglts.option.license.config import check, parameters, require


def test_parameters():
    assert len(parameters) == 4


def test_config_check_license_name_exists():
    cfg = Config(dict(license={'name': "", 'year': 2015,
                               'organization': "oa", 'project': "project"}))
    assert 'name' in check(cfg)

    cfg = Config(dict(license={'name': "tugudu", 'year': 2015,
                               'organization': "oa", 'project': "project"}))
    assert 'name' in check(cfg)


def test_require():
    cfg = Config(dict(license={}))

    assert len(require('option', cfg)) == 1
    assert len(require('setup', cfg)) == 0
    assert len(require('install', cfg)) == 0
    assert len(require('dvlpt', cfg)) == 0
